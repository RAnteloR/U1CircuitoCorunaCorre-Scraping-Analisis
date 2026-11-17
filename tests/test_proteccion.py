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

    # Comprobamos que ya no están las columnas personales
    assert "nome" not in tabla_limpia.columns
    assert "apelidos" not in tabla_limpia.columns
    assert "dorsal" not in tabla_limpia.columns

    # Comprobamos que las columnas de análisis siguen intactas
    assert "posto" in tabla_limpia.columns
    assert "tempo_s" in tabla_limpia.columns