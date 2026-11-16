"""Función de descarga común del proyecto.

Todas las peticiones a la web pasan por `descargar()`, que aplica las buenas prácticas:

- User-Agent propio que identifica el proyecto y un contacto.
- Pausa mínima de PAUSA segundos entre peticiones reales (las lecturas de caché no esperan).
- Guarda la respuesta en bytes (sin decodificar) en datos/raw/.
- Si el fichero ya existe, no se vuelve a descargar: se lee del disco.

Ejemplo:
    from src.descarga import descargar, ruta_raw
    html = descargar("https://corunacorre.com/gl/web/resultado/evento-3210")
    # -> bytes; guardado en datos/raw/corunacorre.com/gl_web_resultado_evento-3210.html
"""

from __future__ import annotations

import re
import time
from pathlib import Path
from urllib.parse import urlsplit

import requests

USER_AGENT = (
    "CorunaCorreBot/0.1 (proyecto educativo Big Data; "
    "contacto: raul.antelobdi@gmail.com)"
)
PAUSA = 1.5  # segundos entre peticiones (el enunciado pide al menos 1 s)
TIMEOUT = 30  # segundos máximos esperando respuesta
REINTENTOS = 3  # intentos si el servidor falla (5xx, 429) o se cae la conexión

# Raíz del repositorio: este fichero está en <repo>/src/descarga.py
RAIZ = Path(__file__).resolve().parents[1]
DIR_RAW = RAIZ / "datos" / "raw"

_sesion = requests.Session()
_sesion.headers.update({"User-Agent": USER_AGENT})
_ultima_peticion = 0.0  # instante (time.monotonic) de la última petición real


def ruta_raw(url: str, extension: str = ".html") -> Path:
    """Devuelve la ruta en datos/raw/ donde se guarda una URL.

    Usa el dominio como carpeta y el camino + query como nombre, sustituyendo los
    caracteres no válidos en Windows. Así la misma URL siempre da el mismo fichero.
    """
    partes = urlsplit(url)
    nombre = partes.path.strip("/") or "index"
    if partes.query:
        nombre += "_" + partes.query
    nombre = re.sub(r"[^A-Za-z0-9._-]+", "_", nombre).strip("_")
    if not Path(nombre).suffix:
        nombre += extension
    return DIR_RAW / partes.netloc / nombre


def _esperar() -> None:
    """Espera lo necesario para que pasen PAUSA segundos desde la última petición."""
    global _ultima_peticion
    restante = PAUSA - (time.monotonic() - _ultima_peticion)
    if restante > 0:
        time.sleep(restante)
    _ultima_peticion = time.monotonic()


def descargar(url: str, ruta: str | Path | None = None, forzar: bool = False) -> bytes:
    """Descarga `url` y devuelve el contenido en bytes.

    - ruta: dónde guardarla. Si no se indica, se usa ruta_raw(url).
    - forzar: si es True, descarga aunque el fichero ya exista.

    Si el fichero ya existe (y no se fuerza), se lee del disco sin hacer ninguna
    petición. Lanza requests.HTTPError si la respuesta final no es 2xx.
    """
    ruta = Path(ruta) if ruta is not None else ruta_raw(url)

    if ruta.exists() and not forzar:
        return ruta.read_bytes()

    for intento in range(1, REINTENTOS + 1):
        _esperar()
        try:
            respuesta = _sesion.get(url, timeout=TIMEOUT)
        except (requests.ConnectionError, requests.Timeout):
            if intento == REINTENTOS:
                raise
            time.sleep(PAUSA * 2**intento)  # espera creciente antes de reintentar
            continue
        if respuesta.status_code in (429, 500, 502, 503, 504) and intento < REINTENTOS:
            time.sleep(PAUSA * 2**intento)
            continue
        respuesta.raise_for_status()
        break

    # Guardar primero en un temporal y luego renombrar: si el proceso se corta a
    # la mitad, no queda un fichero incompleto que después se tomaría por bueno.
    ruta.parent.mkdir(parents=True, exist_ok=True)
    temporal = ruta.with_name(ruta.name + ".part")
    temporal.write_bytes(respuesta.content)
    temporal.replace(ruta)
    return respuesta.content
