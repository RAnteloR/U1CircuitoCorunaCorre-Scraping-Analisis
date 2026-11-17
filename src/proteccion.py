"""Funciones de protección de datos y estilo común de gráficas (Persona D).

Incluye:
- quitar_identificadores(tabla): elimina columnas con datos personales antes de mostrar.
- configurar_estilo_graficas(): aplica colores, fuente y tamaño comunes para todo el grupo.
- guardar_figura(figura, nombre_archivo): guarda la gráfica limpia en la carpeta output/.
"""

from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

from src.config import DIR_OUTPUT

# Lista de columnas que identifican a una persona y nunca deben salir en pantalla
COLUMNAS_IDENTIFICADORAS = [
    "nome",
    "apelidos",
    "dorsal",
    "nombre",
    "apellidos",
    "nome_completo",
]

# Paleta de colores común del grupo (accesible y clara para comparar categorías/sexos)
PALETA_COLORES = [
    "#1f77b4",  # Azul principal
    "#ff7f0e",  # Naranja contraste
    "#2ca02c",  # Verde
    "#d62728",  # Rojo
    "#9467bd",  # Morado
    "#8c564b",  # Marrón
    "#e377c2",  # Rosa
    "#7f7f7f",  # Gris
]


def quitar_identificadores(tabla: pd.DataFrame) -> pd.DataFrame:
    """Elimina las columnas de nombre, apellidos y dorsal antes de enseñar una tabla.

    Se usa siempre en los notebooks antes de hacer un .head(), .sample() o mostrar
    cualquier fila, para cumplir con el RGPD y las normas del proyecto.
    """
    # Creamos una copia para no borrar sin querer los datos de la variable original
    tabla_segura = tabla.copy()

    # Buscamos cuáles de las columnas prohibidas están presentes en esta tabla
    columnas_a_borrar = [
        columna
        for columna in COLUMNAS_IDENTIFICADORAS
        if columna in tabla_segura.columns
    ]

    # Las eliminamos si existen
    if columnas_a_borrar:
        tabla_segura = tabla_segura.drop(columns=columnas_a_borrar)

    return tabla_segura


def configurar_estilo_graficas() -> None:
    """Configura el tamaño, letra y colores de matplotlib para que todas las gráficas
    del grupo parezcan hechas por la misma persona.
    """
    plt.rcParams["figure.figsize"] = (10, 6)
    plt.rcParams["figure.dpi"] = 120
    plt.rcParams["font.size"] = 11
    plt.rcParams["axes.titlesize"] = 14
    plt.rcParams["axes.titleweight"] = "bold"
    plt.rcParams["axes.labelsize"] = 12
    plt.rcParams["axes.grid"] = True
    plt.rcParams["grid.alpha"] = 0.3
    plt.rcParams["axes.prop_cycle"] = plt.cycler(color=PALETA_COLORES)


def guardar_figura(
    figura: plt.Figure,
    nombre_archivo: str,
    carpeta_destino: Path = DIR_OUTPUT,
) -> Path:
    """Guarda una gráfica en formato PNG con buena calidad y sin bordes cortados.

    Si el nombre no termina en .png, se lo añade automáticamente.
    """
    # Nos aseguramos de que la carpeta de salida exista
    carpeta_destino.mkdir(parents=True, exist_ok=True)

    # Añadimos la extensión .png si alguien se olvida de ponerla
    if not nombre_archivo.endswith(".png"):
        nombre_archivo = f"{nombre_archivo}.png"

    ruta_completa = carpeta_destino / nombre_archivo

    # bbox_inches="tight" evita que se corten los textos de los ejes al guardar
    figura.savefig(ruta_completa, dpi=150, bbox_inches="tight")
    return ruta_completa