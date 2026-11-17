"""Tests de la ligazón de personas. Solo usan nombres inventados.

Ejecutar desde la raíz del repo:  python -m pytest
"""

import pytest

from src.ligazon import normalizar_nombre


@pytest.mark.parametrize(
    "entrada, esperado",
    [
        ("  María  Núñez ", "MARIA NUNEZ"),    # tildes, ñ, espacios dobles y extremos
        ("ana lópez", "ANA LOPEZ"),             # minúsculas
        ("JOSÉ  PÉREZ", "JOSE PEREZ"),          # ya en mayúsculas
        ("Iván\tGómez\n", "IVAN GOMEZ"),        # tabuladores y saltos de línea
        ("", ""),                               # vacío
    ],
)
def test_normalizar_nombre(entrada, esperado):
    assert normalizar_nombre(entrada) == esperado


def test_normalizar_nombre_es_idempotente():
    una_vez = normalizar_nombre("  Lúa  Ñande ")
    assert normalizar_nombre(una_vez) == una_vez


# --- clave_persona y codigo_hmac (clave secreta inventada, solo para los tests) ---

from src.ligazon import clave_persona, codigo_hmac  # noqa: E402

CHAVE_TEST = b"clave-inventada-solo-para-tests"


def test_clave_inscrito_usa_dorsal():
    assert clave_persona("Ana López", 123, inscrito=True) == "D:123"


def test_clave_no_inscrito_dorsal_fiable_usa_dorsal():
    assert clave_persona("Ana López", "123", inscrito=False, dorsal_fiable=True) == "D:123"


def test_clave_no_inscrito_dorsal_no_fiable_usa_nombre_normalizado():
    assert clave_persona("  Ana  López ", 123, inscrito=False) == "N:ANA LOPEZ"


def test_codigo_hmac_tiene_12_caracteres_hexadecimales():
    codigo = codigo_hmac("N:ANA LOPEZ", CHAVE_TEST)
    assert len(codigo) == 12
    int(codigo, 16)  # lanza error si no es hexadecimal


def test_codigo_hmac_es_determinista_y_depende_de_la_clave_y_del_dato():
    a = codigo_hmac("N:ANA LOPEZ", CHAVE_TEST)
    assert a == codigo_hmac("N:ANA LOPEZ", CHAVE_TEST)
    assert a != codigo_hmac("N:ANA LOPES", CHAVE_TEST)
    assert a != codigo_hmac("N:ANA LOPEZ", b"otra-clave-inventada")


def test_codigo_hmac_lee_la_clave_de_la_variable_chave(monkeypatch):
    monkeypatch.setenv("CHAVE", CHAVE_TEST.decode())
    assert codigo_hmac("D:123") == codigo_hmac("D:123", CHAVE_TEST)
