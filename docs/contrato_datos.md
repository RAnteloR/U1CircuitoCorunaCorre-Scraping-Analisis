# Contrato de datos

Este documento define las dos tablas finales que se guardan en `datos/clean/`
(`participaciones.csv` y `carreiras.csv`) y el método con el que se identifica a cada
persona entre carreras.

En estas tablas no figuran nombres, apellidos ni dorsales: cada persona aparece únicamente
como un código pseudónimo (`codigo_persona`).

## `participaciones.csv`

Una fila por persona y carrera.

| Columna | Tipo | Descripción |
|---|---|---|
| `codigo_persona` | texto (12 caracteres hexadecimales) | Código pseudónimo de la persona: los 12 primeros caracteres del HMAC-SHA256 de su clave de persona (ver más abajo). |
| `carrera_id` | texto | Identificador de la carrera; coincide con el de `carreiras.csv`. |
| `orden` | entero | Posición de la carrera en el circuito (1 = primera). |
| `sexo` | texto (`M` / `F`) | Sexo, extraído de la columna original de puesto por sexo (por ejemplo, `M-3`). |
| `categoria` | texto | Categoría de edad, extraída de la columna original de puesto por categoría (por ejemplo, `MS2M-1`). Las categorías especiales ("Especial", "Sen categoría") se tratan según el informe de calidad. |
| `posto` | entero | Puesto en la clasificación general de la carrera. |
| `posto_sexo` | entero | Puesto dentro de su sexo (el número de `M-3`). |
| `posto_categoria` | entero | Puesto dentro de su categoría (el número de `MS2M-1`). |
| `tempo_s` | número (segundos) | Tiempo en segundos. Queda vacío si el tiempo falta o es imposible; el motivo se documenta en el informe de calidad. |
| `tempo_marca` | texto | Estado del tiempo (por ejemplo, `ok`, `faltante`, `imposible`). Los valores definitivos se fijan en el informe de calidad. |
| `inscrito_circuito` | booleano | `True` si la persona figura en la lista de inscritos del circuito; `False` si corre solo esa prueba. |

No incluye nombre, apellidos ni dorsal.

## `carreiras.csv`

Una fila por carrera.

| Columna | Tipo | Descripción |
|---|---|---|
| `carrera_id` | texto | Identificador de la carrera. Permite unir con `participaciones.csv`. |
| `orden` | entero | Posición de la carrera en el circuito (1 = primera). |
| `fecha` | fecha (`AAAA-MM-DD`) | Día en que se corrió. |
| `distancia_km` | número | Distancia de la carrera, en kilómetros. |
| `n_participantes` | entero | Número de filas de esa carrera en `participaciones.csv`. |

Con la parte opcional O1 (meteorología), esta tabla incorpora además la temperatura y la
precipitación del día de cada carrera.

## Clave de persona

Para reconocer a una misma persona en varias carreras se necesita una clave que no cambie.
Se decide así:

1. **¿Figura en la lista de inscritos del circuito?**
   - **Sí** → la clave es el **dorsal**, que se mantiene durante todo el circuito.
   - **No** → se comprueba si el dorsal es fiable:
     - **Fiable** → la clave es el **dorsal**.
     - **No fiable** → la clave es el **nombre normalizado**.
2. Se aplica **HMAC-SHA256** a la clave, con una clave secreta, y se conservan los
   **12 primeros caracteres**. El resultado es el `codigo_persona`.

Detalles de la implementación (`src/ligazon.py`):

- **Nombre normalizado:** mayúsculas, sin tildes (la ñ pasa a N), sin espacios dobles y sin
  espacios en los extremos. Ejemplo: `"  María  Núñez "` → `"MARIA NUNEZ"`.
- **Prefijo:** la clave de persona empieza por `D:` si es un dorsal y por `N:` si es un
  nombre (`D:123`, `N:MARIA NUNEZ`), de modo que un dorsal y un nombre nunca producen la
  misma clave.
- **Clave secreta:** se lee de la variable de entorno `CHAVE`, definida en un fichero `.env`
  que no se incluye en el repositorio. No aparece en el código. Los códigos solo son
  reproducibles con la misma clave.

## Limitaciones de la ligazón

- **Falsos positivos** (dos personas tomadas como una): por ejemplo, homónimos, o dos
  nombres que solo difieren en una tilde (`Nuñez` y `Nunez`) y que la normalización iguala.
- **Falsos negativos** (una persona tomada como dos): por ejemplo, un mismo nombre escrito
  de forma distinta en dos carreras.
- La fiabilidad del dorsal de quien corre por prueba se comprueba sobre los datos; mientras
  no se haya comprobado, `clave_persona()` lo trata como no fiable y usa el nombre.
- El número de casos dudosos encontrados y la decisión tomada con ellos se documentan en el
  apartado de integración del README.
