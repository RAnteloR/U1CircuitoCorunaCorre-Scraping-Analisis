# P2 · Coruña Corre — scraping y análisis

Proyecto de Sistemas de Big Data (UD1): descarga automática y responsable de los resultados
del circuito Coruña Corre, limpieza, integración entre carreras, análisis y protección de los
datos personales según el destinatario.

## Fuentes

_Pendiente._

## Estructura

```
datos/
  raw/        páginas descargadas en bytes (no se suben)
  interim/    tablas extraídas que todavía tienen nombres (no se suben)
  clean/      participacions.csv y carreiras.csv pseudonimizadas (no se suben)
  externos/   ficheros hechos por nosotros o de otras fuentes
notebooks/    notebooks numerados del pipeline
src/          código común (config.py, obtencion.py), importado desde los notebooks
tests/        tests de las funciones comunes (sin peticiones reales)
docs/         contrato de datos, informe de calidad y otra documentación
output/       entregas para cada destinatario
presentacion/ presentación en PDF
```

## Cómo ejecutarlo

1. Crear y activar el entorno (Python 3.12):
   ```powershell
   py -3.12 -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```
2. Copiar `.env.example` como `.env` y poner la clave `CHAVE` común del grupo
   (compartida por un canal privado, nunca en el repositorio).
3. Comprobar que todo funciona: `python -m pytest`
4. Ejecutar los notebooks de `notebooks/` en orden, con el kernel del `.venv`.

Las rutas de datos y la lectura de la clave están en `src/config.py`
(`from src.config import DIR_RAW, DIR_INTERIM, DIR_CLEAN, leer_clave`).

### Descarga común (`src/obtencion.py`)

La función está en un módulo `.py` y no dentro de un notebook para que **todos los notebooks
importen la misma**, sin copiarla. `notebooks/01_descarga.ipynb` explica cómo funciona y la prueba.

Todas las peticiones pasan por `descargar(url, destino=None)`:

- **User-Agent propio** que identifica el proyecto y un contacto.
- **Pausa** de 1,5 s entre peticiones reales (el mínimo pedido es 1 s).
- **Guarda en bytes** en `datos/raw/<dominio>/<camino>.html`, sin decodificar.
- **Sin repetir**: si el fichero ya existe, se lee del disco y no se hace ninguna petición.
- Reintenta hasta 3 veces, con espera creciente, si el servidor falla (429/5xx) o se cae la conexión.
- Escribe primero un `.part` y luego lo renombra, para que una descarga cortada no quede como buena.

```python
from src.obtencion import descargar
html = descargar("https://corunacorre.com/gl/web/resultado/evento-3210")  # bytes
```

### Carreras reales (`src/carreras.py`, HITO 1)

`notebooks/02_carreras.ipynb` ejecuta los tres pasos y solo muestra recuentos:

1. `descubrir_carreras()`: parte de `/web/resultado/` y sigue **Edición Actual → Por evento →
   carrera → categorías**. La Absoluta se busca por el texto del enlace y se excluye la
   carrera que aún no se ha corrido (fecha ≥ hoy). Devuelve `carrera_id, orden, fecha, url_absoluta`.
2. `descargar_todas()`: pide `?page=1, 2, ...` hasta que no hay filas o enlace «Seguinte» y
   guarda cada página en `datos/raw/<carrera_id>/pagina_N.html` (una segunda ejecución no hace peticiones).
3. `construir_todas()`: crea `datos/interim/carrera_XX.csv` (columnas crudas `posto, dorsal,
   nome, apelidos, posto_sexo, posto_categoria, tempo`) y guarda la comprobación de filas en
   `docs/comprobacion_filas.csv`.

## Legalidad y protección de datos

### 1. Revisión de `robots.txt` y condiciones técnicas de las fuentes
Antes de realizar las descargas se han comprobado los ficheros `robots.txt` y los textos legales de la web principal y de las fuentes opcionales (consultados el **17/11/2026** y **18/11/2026**):

| Fuente | URL de `robots.txt` (consulta: 17/11/2026) | Resultado técnico | Textos legales y condiciones aplicables (consulta: 18/11/2026) |
|---|---|---|---|
| **Coruña Corre** (carreras, inscritos y clasificación 04) | `https://corunacorre.com/robots.txt` | Redirige (`302`) a `/gl/robots.txt` y devuelve `404 Not Found` (no existe). | [Nota legal](https://corunacorre.com/gl/web/nota/legal/), [Política de privacidade](https://corunacorre.com/gl/web/politica/privacidad/) y [Regulamento do Circuíto (PDF)](https://ccnorte.com/uploads/eventos/liga-reglamento-69a1a19e9c6f3.pdf). Titular de la web: *MULTISPORTS GALICIA, S.L.* (plataforma *CCNorte Desarrollo* / `ccnorte.com`). |
| **San Silvestre Coruña** (Opcional 02) | `https://sansilvestrecoruna.com/robots.txt` | Redirige (`302`) a `/gl/robots.txt` y devuelve `404 Not Found` (no existe). | [Nota legal](https://sansilvestrecoruna.com/gl/web/nota/legal/), [Política de privacidade](https://sansilvestrecoruna.com/gl/web/politica/privacidad/) y [Reglamento](https://ccnorte.com/e/3395/reglamento) (plataforma `ccnorte.com`). |
| **Open-Meteo** (Fuente elegida para Opcional 01) | `https://open-meteo.com/robots.txt` | Devuelve `200 OK` con `User-agent: *` y `Allow: /`. | [Términos de uso](https://open-meteo.com/en/terms) y [Licencia](https://open-meteo.com/en/license): los **datos** meteorológicos se publican bajo licencia abierta **CC BY 4.0** (exige atribución/cita de la fuente), mientras que las **condiciones del servicio de la API gratuita** limitan su uso a fines **no comerciales** (como este proyecto académico). |
| **MeteoGalicia** (Revisada como alternativa descartada) | `https://www.meteogalicia.gal/robots.txt` | Devuelve `404 Not Found` (no existe). | [Aviso legal de la Xunta de Galicia](https://www.xunta.gal/aviso-legal-do-portal). Se descarta en favor de la API histórica de Open-Meteo por ofrecer datos tabulares directos y limpios. |

**¿Qué significa que no exista `robots.txt` (`404 Not Found`)?**
La ausencia de `robots.txt` indica que el servidor no ha definido restricciones técnicas de rastreo por rutas para bots, pero **no exime de cumplir el resto del marco legal**:
1. **Nota legal y uso responsable del servidor:** Queda prohibido realizar peticiones masivas que dañen o sobrecarguen la plataforma (`ccnorte.com` / *MULTISPORTS GALICIA, S.L.*). Nuestro módulo `src/obtencion.py` aplica una pausa mínima de 1,5 segundos entre peticiones, utiliza un `User-Agent` identificativo del proyecto académico y guarda las respuestas en caché local (`datos/raw/`) para no repetir peticiones.
2. **Propiedad intelectual (derechos sobre la web y las bases de datos):** Según la [Nota legal](https://corunacorre.com/gl/web/nota/legal/), *MULTISPORTS GALICIA, S.L.* es titular de los derechos de propiedad intelectual de la web. La extracción en este trabajo se realiza exclusivamente con fines docentes y de análisis estadístico dentro de la asignatura, citando las fuentes y fechas de acceso.
3. **Normativa de protección de datos (RGPD y LOPDGDD):** Los datos publicados en las clasificaciones mantienen su carácter de datos personales y no pueden ser republicados ni expuestos fuera de su finalidad original.

### 2. Aviso legal del circuito y tratamiento de datos personales
Según el [Regulamento do Circuíto Coruña Corre](https://ccnorte.com/uploads/eventos/liga-reglamento-69a1a19e9c6f3.pdf) y la [Política de privacidade](https://corunacorre.com/gl/web/politica/privacidad/), los participantes consienten la publicación de su **nombre, apellidos, dorsal, sexo, categoría, club y tiempos** con la finalidad de gestionar la competición y garantizar la transparencia de las clasificaciones deportivas.

En este proyecto tratamos dichos datos aplicando el principio de **minimización y protección desde el diseño**:
- **Qué datos personales aparecen en origen:** `nome`, `apelidos` y `dorsal` (junto con `sexo`, `categoria` y `tempo`).
- **Para qué se usan:** Únicamente en local dentro de las fases internas (`interim/`) para poder enlazar las participaciones de una misma persona entre distintas carreras y cruzarlas con la lista de inscritos.
- **Medidas técnicas que se aplican en el proyecto:**
  1. **No publicación en el repositorio:** `.gitignore` bloquea `datos/raw/`, `datos/interim/`, `datos/clean/` y el fichero `.env`.
  2. **Ocultación en notebooks (`src/proteccion.py`):** La función `quitar_identificadores(tabla)` elimina `nome`, `apelidos` y `dorsal` antes de mostrar cualquier tabla en pantalla.
  3. **Pseudonimización con HMAC (`src/ligazon.py`, en desarrollo en la PR #29 / Issue #5):** Los identificadores directos se sustituirán por un hash HMAC generado con una clave secreta compartida por canal privado (`CHAVE` en `.env`), impidiendo revertir el identificador sin la clave.
  4. **Generalización, agregación y $k$-anonimato en las futuras entregas (`output/`, Issue #19):** En la fase de entregas, para prensa solo se generarán datos agregados; para investigación se eliminarán identificadores directos y se verificará el $k$-anonimato sobre los cuasi-identificadores (`sexo`, `categoria`, carreras disputadas); la entrega nominal para la organización no se subirá al repositorio.
## Informe de calidad y decisiones de limpieza

_Pendiente._

## Integración y unión de personas

_Pendiente._

## Entregas por destinatario

_Pendiente._

## Partes opcionales

_Pendiente._

## Presentación

_Pendiente_ (`presentacion/`).

## Reparto del trabajo

_Pendiente._

## Uso de la IA

_Pendiente._
