"""Tests de la función de descarga común. No hacen peticiones reales a ninguna web.

Ejecutar desde la raíz del repo:  python -m pytest
"""

from unittest.mock import MagicMock

import pytest
import requests

from src import obtencion


def _respuesta(status: int, contenido: bytes = b"") -> MagicMock:
    r = MagicMock()
    r.status_code = status
    r.content = contenido
    if status >= 400:
        r.raise_for_status.side_effect = requests.HTTPError(f"HTTP {status}")
    return r


@pytest.fixture(autouse=True)
def sin_esperas(monkeypatch):
    """Quita las pausas para que los tests vayan rápido."""
    monkeypatch.setattr(obtencion, "PAUSA", 0)
    monkeypatch.setattr(obtencion.time, "sleep", lambda s: None)


def test_user_agent_propio():
    assert "CorunaCorreBot" in obtencion._sesion.headers["User-Agent"]


def test_ruta_raw_es_estable_y_valida_en_windows():
    ruta = obtencion.ruta_raw("https://corunacorre.com/gl/web/resultado/evento-3210?page=2")
    assert ruta.parent.name == "corunacorre.com"
    assert ruta.name == "gl_web_resultado_evento-3210_page_2.html"
    assert ruta == obtencion.ruta_raw("https://corunacorre.com/gl/web/resultado/evento-3210?page=2")


def test_guarda_en_bytes(tmp_path, monkeypatch):
    get = MagicMock(return_value=_respuesta(200, "Coruña".encode("utf-8")))
    monkeypatch.setattr(obtencion._sesion, "get", get)
    destino = tmp_path / "pagina.html"

    contenido = obtencion.descargar("https://ejemplo.test/p", destino)

    assert contenido == "Coruña".encode("utf-8")
    assert destino.read_bytes() == contenido
    assert not destino.with_name("pagina.html.part").exists()


def test_no_repite_si_ya_existe(tmp_path, monkeypatch):
    get = MagicMock()
    monkeypatch.setattr(obtencion._sesion, "get", get)
    destino = tmp_path / "pagina.html"
    destino.write_bytes(b"ya descargado")

    assert obtencion.descargar("https://ejemplo.test/p", destino) == b"ya descargado"
    get.assert_not_called()


def test_reintenta_si_el_servidor_falla(tmp_path, monkeypatch):
    get = MagicMock(side_effect=[_respuesta(503), _respuesta(200, b"ok")])
    monkeypatch.setattr(obtencion._sesion, "get", get)

    assert obtencion.descargar("https://ejemplo.test/p", tmp_path / "p.html") == b"ok"
    assert get.call_count == 2


def test_error_404_no_guarda_nada(tmp_path, monkeypatch):
    monkeypatch.setattr(obtencion._sesion, "get", MagicMock(return_value=_respuesta(404)))
    destino = tmp_path / "p.html"

    with pytest.raises(requests.HTTPError):
        obtencion.descargar("https://ejemplo.test/p", destino)
    assert not destino.exists()
