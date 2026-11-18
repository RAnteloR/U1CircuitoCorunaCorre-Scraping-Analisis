"""Ligazón de personas entre carreras: normalización de nombres y pseudonimización.

    from src.ligazon import normalizar_nombre, clave_persona, codigo_hmac
"""

from __future__ import annotations

import hashlib
import hmac
import unicodedata

from src.config import leer_clave


def nombre_completo(nome: str, apelidos: str) -> str:
    """Une nombre y apellidos siempre en el mismo orden: "nome apelidos".

    La tabla limpia trae nome y apelidos en columnas separadas. Esta función es el único
    sitio donde se unen, para que el cruce con inscritos y la ligazón de personas
    construyan exactamente el mismo texto.
    """
    return f"{nome} {apelidos}"


def normalizar_nombre(nombre: str) -> str:
    """Devuelve el nombre en mayúsculas, sin tildes, sin guiones, sin espacios dobles y recortado.

    Ejemplo: "  María-José  Núñez " -> "MARIA JOSE NUNEZ"

    La ñ también pierde la tilde (Ñ -> N), así que "Nuñez" y "Nunez" dan la misma clave.
    El guion se cambia por un espacio, así "Pérez-Oca" y "Pérez Oca" dan la misma clave.
    """
    # NFD separa cada letra de su tilde; después se descartan las marcas (categoría Mn).
    sin_tildes = "".join(
        c for c in unicodedata.normalize("NFD", nombre) if unicodedata.category(c) != "Mn"
    )
    # split() sin argumentos descarta los espacios de los extremos y junta los dobles.
    return " ".join(sin_tildes.upper().replace("-", " ").split())


def clave_persona(
    nombre: str, dorsal: int | str, inscrito: bool, dorsal_fiable: bool = False
) -> str:
    """Devuelve el texto que identifica a una persona, antes de pseudonimizarla.

    Sigue el árbol de decisión del enunciado (figura 4):
    - inscrito en el circuito  -> dorsal (es fijo todo el circuito)
    - no inscrito, dorsal fiable (comprobado en los datos) -> dorsal
    - no inscrito, dorsal no fiable -> nombre normalizado

    El prefijo "D:" o "N:" evita que un dorsal y un nombre den la misma clave.
    """
    if inscrito or dorsal_fiable:
        return f"D:{str(dorsal).strip()}"
    return f"N:{normalizar_nombre(nombre)}"


def codigo_hmac(clave: str, llave: bytes | None = None) -> str:
    """Devuelve el código pseudónimo (12 primeros caracteres del HMAC-SHA256) de `clave`.

    `llave` es la clave secreta; si no se indica, se lee de .env con leer_clave().
    Nunca está escrita en el código ni en el repositorio.
    """
    if llave is None:
        llave = leer_clave()
    return hmac.new(llave, clave.encode("utf-8"), hashlib.sha256).hexdigest()[:12]
