"""Funciones de limpieza de los resultados (B, issue #4)."""

import math

TIEMPO_MIN_S = 12 * 60   # 12 min: por debajo del récord del mundo en 5 km
TIEMPO_MAX_S = 60 * 60   # 1 h: cierre de control de la carrera


def tiempo_a_segundos(texto):
    """Convierte '00:28:36' o '28:36' a segundos. Si no hay tiempo o no se entiende, devuelve None."""
    if texto is None or (isinstance(texto, float) and math.isnan(texto)):
        return None
    texto = str(texto).strip()
    if texto == "":
        return None

    partes = texto.split(":")
    if len(partes) not in (2, 3) or not all(p.isdigit() for p in partes):
        return None

    numeros = [int(p) for p in partes]
    if len(numeros) == 2:          # mm:ss - le añadimos 0 horas
        numeros = [0] + numeros
    h, m, s = numeros
    if m >= 60 or s >= 60:
        return None
    return h * 3600 + m * 60 + s


def marcar_tiempo(segundos):
    """Devuelve 'ok', 'faltante' o 'imposible'. No borra nada: solo marca."""
    if segundos is None:
        return "faltante"
    if segundos < TIEMPO_MIN_S or segundos > TIEMPO_MAX_S:
        return "imposible"
    return "ok"