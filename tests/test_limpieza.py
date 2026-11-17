"""Tests de las funciones de limpieza (issue #4). Datos inventados, sin nombres."""

from src.limpieza import (
    tiempo_a_segundos,
    marcar_tiempo,
    parsear_posto_sexo,
    parsear_posto_categoria,
)


# --- Tiempos ------

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
    assert marcar_tiempo(4000) == "imposible"        # + de 1 h: fuera del control


# --- Posto por sexo (M-3) ------

def test_posto_sexo():
    assert parsear_posto_sexo("M-3") == ("M", 3)
    assert parsear_posto_sexo("F-229") == ("F", 229)
    assert parsear_posto_sexo(" m-548 ") == ("M", 548)   # espacios y minus


def test_posto_sexo_raro():
    assert parsear_posto_sexo("") == (None, None)
    assert parsear_posto_sexo(None) == (None, None)
    assert parsear_posto_sexo("X-3") == (None, None)     # sexo desconocido
    assert parsear_posto_sexo("M3") == (None, None)      # sin guion


# --- Posto por categoría (MS2M-1) ------

def test_posto_categoria():
    assert parsear_posto_categoria("MS2M-1") == ("MS2", "M", 1)
    assert parsear_posto_categoria("SNRF-80") == ("SNR", "F", 80)
    assert parsear_posto_categoria("SUB23M-6") == ("SUB23", "M", 6)
    assert parsear_posto_categoria("M1M-2") == ("M1", "M", 2)   # formato de la clasificación del circuito


def test_posto_categoria_raro():
    assert parsear_posto_categoria("") == (None, None, None)
    assert parsear_posto_categoria(None) == (None, None, None)
    assert parsear_posto_categoria("MS2-1") == (None, None, None)   # falta el sexo


def test_categorias_especiales():
    assert parsear_posto_categoria("ESPM-1") == ("ESP", "M", 1)     # Especial
    assert parsear_posto_categoria("NO") == (None, None, None)      # sin categoría

def test_tiempo_negativo_es_imposible():
    assert tiempo_a_segundos("-5:00") == -300
    assert marcar_tiempo(tiempo_a_segundos("-5:00")) == "imposible"


def test_bordes_de_los_limites():
    assert marcar_tiempo(12 * 60) == "ok"              # justo 12:00 vale
    assert marcar_tiempo(12 * 60 - 1) == "imposible"
    assert marcar_tiempo(60 * 60) == "ok"              # justo 1:00:00 vale
    assert marcar_tiempo(60 * 60 + 1) == "imposible"