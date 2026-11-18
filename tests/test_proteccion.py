import pandas as pd
from src.proteccion import quitar_identificadores


def test_quitar_identificadores_elimina_datos_personales():
    # Creamos una tabla de prueba con datos inventados
    tabla_con_datos = pd.DataFrame({
        "carrera_id": ["carrera_01"],
        "dorsal": ["1234"],
        "nome": ["Carlos"],
        "apelidos": ["Prueba"],
        "posto": [10],
        "tempo_s": [1500],
    })

    tabla_limpia = quitar_identificadores(tabla_con_datos)

    # Comprobamos que ya no están las columnas personales en la nueva tabla
    assert "nome" not in tabla_limpia.columns
    assert "apelidos" not in tabla_limpia.columns
    assert "dorsal" not in tabla_limpia.columns

    # Comprobamos que las columnas de análisis siguen intactas
    assert "posto" in tabla_limpia.columns
    assert "tempo_s" in tabla_limpia.columns


def test_quitar_identificadores_no_modifica_tabla_original():
    # Comprobamos que el DataFrame original conserva sus columnas intactas
    tabla_original = pd.DataFrame({
        "dorsal": ["1234"],
        "nome": ["Carlos"],
        "apelidos": ["Prueba"],
        "posto": [10],
    })

    _ = quitar_identificadores(tabla_original)

    assert "nome" in tabla_original.columns
    assert "apelidos" in tabla_original.columns
    assert "dorsal" in tabla_original.columns


def test_quitar_identificadores_en_tabla_sin_identificadores():
    # Si la tabla ya viene limpia, no debe dar error y debe quedar igual
    tabla_sin_identificadores = pd.DataFrame({
        "carrera_id": ["carrera_01"],
        "posto": [10],
        "tempo_s": [1500],
    })

    resultado = quitar_identificadores(tabla_sin_identificadores)

    assert list(resultado.columns) == ["carrera_id", "posto", "tempo_s"]
    assert len(resultado) == 1
