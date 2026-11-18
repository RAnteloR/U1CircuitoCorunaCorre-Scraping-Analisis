# Contrato de datos

Este documento define las tablas del proyecto en el orden en que se generan:

1. **Tabla limpia por carrera** (`datos/interim/`): resultados ya limpios, todavía con nombres.
2. **Tablas finales** (`datos/clean/`): `participaciones.csv` y `carreiras.csv`, sin nombres
   ni dorsales; cada persona aparece solo como un código pseudónimo (`codigo_persona`).

Ni los ficheros de `datos/interim/` ni los de `datos/clean/` se suben al repositorio.

## 1. Tabla limpia por carrera

Sale de la limpieza, una por carrera, en `datos/interim/carrera_XX_limpia.csv`.
La usan C (Ismael) para ligar personas y D (Carlos) para cruzar con la lista de inscritos.
No se sube al repositorio porque lleva nombres.

| Columna | Tipo | Descripción |
|---|---|---|
| `carrera_id` | texto | Identificador de la carrera: `carrera_01` … `carrera_06`. |
| `orden` | entero | Orden en el circuito (1-6). |
| `dorsal` | texto | Dorsal. |
| `nome` | texto | Nombre; solo sirve para ligar personas y después se elimina. |
| `apelidos` | texto | Apellidos; igual que `nome`. |
| `posto` | entero | Puesto en la clasificación absoluta. |
| `sexo` | texto | `M` o `F`. |
| `posto_sexo` | entero | Puesto dentro del sexo (`M-3` → 3). |
| `categoria` | texto | `SUB20`, `SUB23`, `SNR`, `MS1`, `MS2`, `MS3`, `MS4`, `ESP` o `SIN_CATEGORIA`. |
| `posto_categoria` | entero | Puesto dentro de la categoría (`MS2M-1` → 1). |
| `tempo_s` | entero | Tiempo en segundos (`00:28:36` → 1716). |
| `tempo_marca` | texto | `ok`, `faltante` o `imposible`. |

### Decisiones de limpieza

- El sexo se extrae de "Puesto Sexo" y se comprueba que coincida con la letra final de la
  categoría (`MS2`**`M`**). Si no coincide, se anota en el informe de calidad.
- Las categorías usan el código de las carreras (ver `datos/externos/categorias.csv`).
- En los datos reales aparecen dos valores especiales: `ESP` (`ESPM`/`ESPF`, 3 filas) y `NO`
  (17 filas, sin categoría). `ESP` se conserva como categoría; `NO` pasa a `SIN_CATEGORIA`
  con `posto_categoria` vacío. Cualquier otro valor que no esté en la tabla se explica en el
  informe de calidad.
- Los tiempos no se borran, se marcan:
  - `faltante`: no hay tiempo.
  - `imposible`: negativo, por debajo de 2:30 min/km según la distancia de la carrera
    (12 min si no se conoce la distancia) o más de 1 h (cierre de control). Las distancias
    están en `datos/externos/distancias.csv`.
  - `ok`: el resto.
- La categoría de una persona no debería cambiar entre carreras (art. 3 del regulamento: se
  fija con la edad del 14/03). Si cambia, se considera un problema de calidad.

## 2. `participaciones.csv`

Una fila por persona y carrera. No incluye nombre, apellidos ni dorsal.

| Columna | Tipo | Descripción |
|---|---|---|
| `codigo_persona` | texto (12 caracteres hexadecimales) | Código pseudónimo de la persona: los 12 primeros caracteres del HMAC-SHA256 de su clave de persona (ver sección 4). |
| `carrera_id` | texto | Identificador de la carrera; coincide con el de `carreiras.csv`. |
| `orden` | entero | Posición de la carrera en el circuito (1 = primera). |
| `sexo` | texto (`M` / `F`) | Sexo, tal como figura en la tabla limpia. |
| `categoria` | texto | Categoría de edad, tal como figura en la tabla limpia. |
| `posto` | entero | Puesto en la clasificación general de la carrera. |
| `posto_sexo` | entero | Puesto dentro de su sexo. |
| `posto_categoria` | entero | Puesto dentro de su categoría; vacío si la categoría es `SIN_CATEGORIA`. |
| `tempo_s` | entero (segundos) | Tiempo en segundos. |
| `tempo_marca` | texto | `ok`, `faltante` o `imposible`, con el significado de la sección 1. |
| `inscrito_circuito` | booleano | `True` si la persona figura en la lista de inscritos del circuito; `False` si corre solo esa prueba. |

## 3. `carreiras.csv`

Una fila por carrera.

| Columna | Tipo | Descripción |
|---|---|---|
| `carrera_id` | texto | Identificador de la carrera. Permite unir con `participaciones.csv`. |
| `orden` | entero | Posición de la carrera en el circuito (1 = primera). |
| `fecha` | fecha (`AAAA-MM-DD`) | Día en que se corrió (de `datos/externos/distancias.csv`). |
| `distancia_km` | número | Distancia en kilómetros: es `distancia_m` de `distancias.csv` dividida entre 1000. Vacía en la carrera sin regulamento publicado. |
| `n_participantes` | entero | Número de filas de esa carrera en `participaciones.csv`. |

Con la parte opcional O1 (meteorología), esta tabla incorpora además la temperatura y la
precipitación del día de cada carrera.

## 4. Clave de persona

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

- **Nombre completo:** `nombre_completo(nome, apelidos)` une nombre y apellidos siempre
  en el mismo orden (`"nome apelidos"`). Es la única función que los une, y la usan tanto el
  cruce con la lista de inscritos como la ligazón de personas.
- **Nombre normalizado:** mayúsculas, sin tildes (la ñ pasa a N), con el guion cambiado por
  un espacio, sin espacios dobles y sin espacios en los extremos.
  Ejemplo: `"  María-José  Núñez "` → `"MARIA JOSE NUNEZ"`.
- **Prefijo:** la clave de persona empieza por `D:` si es un dorsal y por `N:` si es un
  nombre (`D:123`, `N:MARIA NUNEZ`), de modo que un dorsal y un nombre nunca producen la
  misma clave.
- **Clave secreta:** se lee de la variable de entorno `CHAVE`, definida en un fichero `.env`
  que no se incluye en el repositorio. No aparece en el código. Los códigos solo son
  reproducibles con la misma clave.

## 5. Limitaciones de la ligazón

- **Falsos positivos** (dos personas tomadas como una): por ejemplo, homónimos, o dos
  nombres que solo difieren en una tilde (`Nuñez` y `Nunez`) y que la normalización iguala.
- **Falsos negativos** (una persona tomada como dos): por ejemplo, un mismo nombre escrito
  de forma distinta en dos carreras.
- La fiabilidad del dorsal de quien corre por prueba se comprueba sobre los datos; mientras
  no se haya comprobado, `clave_persona()` lo trata como no fiable y usa el nombre.
- El número de casos dudosos encontrados y la decisión tomada con ellos se documentan en el
  apartado de integración del README.
