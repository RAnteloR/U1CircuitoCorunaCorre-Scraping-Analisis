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
src/          código común (descarga.py), importado desde los notebooks
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
2. Copiar `.env.example` como `.env` y poner la clave `CHAVE_HMAC` común del grupo
   (compartida por un canal privado, nunca en el repositorio).
3. Ejecutar los notebooks de `notebooks/` en orden, con el kernel del `.venv`.

### Descarga común (`src/descarga.py`)

La función está en un módulo `.py` y no dentro de un notebook para que **todos los notebooks
importen la misma**, sin copiarla. `notebooks/01_descarga.ipynb` explica cómo funciona y la prueba.

Todas las peticiones pasan por `descargar(url)`:

- **User-Agent propio** que identifica el proyecto y un contacto.
- **Pausa** de 1,5 s entre peticiones reales (el mínimo pedido es 1 s).
- **Guarda en bytes** en `datos/raw/<dominio>/<camino>.html`, sin decodificar.
- **Sin repetir**: si el fichero ya existe, se lee del disco y no se hace ninguna petición.
- Reintenta hasta 3 veces, con espera creciente, si el servidor falla (429/5xx) o se cae la conexión.
- Escribe primero un `.part` y luego lo renombra, para que una descarga cortada no quede como buena.

```python
from src.descarga import descargar
html = descargar("https://corunacorre.com/gl/web/resultado/evento-3216")  # bytes
```

## Legalidad y protección de datos

_Pendiente._

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
