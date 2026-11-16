"""Tests de las funciones de limpieza (issue #4). Datos inventados, sin nombres."""

from src.limpieza import tiempo_a_segundos, marcar_tiempo


def test_formato_hh_mm_ss():
    assert tiempo_a_segundos("00:28:36") == 1716


def test_formato_mm_ss():
    assert tiempo_a_segundos("28:36") == 1716


def test_quita_espacios():
    assert tiempo_a_segundos(" 00:28:36 ") == 1716


def test_vacio_devuelve_none():
    assert tiempo_a_segundos("") is None
    assert tiempo_a_segundos(None) is None
    assert tiempo_a_segundos(float("nan")) is None   # así llegan los vacíos desde pandas


def test_formato_raro_devuelve_none():
    assert tiempo_a_segundos("abc") is None
    assert tiempo_a_segundos("00:75:00") is None     # 75 minutos no es válido


def test_marcas():
    assert marcar_tiempo(1716) == "ok"
    assert marcar_tiempo(None) == "faltante"
    assert marcar_tiempo(0) == "imposible"
    assert marcar_tiempo(300) == "imposible"         # 5 min: menos que el récord del mundo
    assert marcar_tiempo(4000) == "imposible"        # más de 1 h: fuera del control