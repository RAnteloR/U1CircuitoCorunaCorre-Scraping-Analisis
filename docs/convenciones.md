# Convenciones de gráficas, notebooks y privacidad

Documento común del grupo (Issue #6) para que todos los notebooks y gráficas sigan el mismo formato y cumplan con las reglas de protección de datos.

## 1. Nombres de los notebooks
Cada persona numera sus notebooks anteponiendo su letra asignada (A, B, C, D) para evitar conflictos de Git:
- A (RAnteloR): A_01_descarga.ipynb, A_02_carreras.ipynb, A_03_analisis_p5_p6_p7.ipynb, A_04_opcional_edicion_anterior.ipynb
- B (raquelccarreraA): B_01_limpieza_calidad.ipynb, B_02_analisis_p8_p9.ipynb, A/B según reparto
- C (ilensf): C_01_ligazon_hmac.ipynb, C_02_analisis_p1_p2.ipynb, C_03_opcional_san_silvestre.ipynb
- D (carlosOvies-dev): D_01_inscritos_cruce.ipynb, D_02_analisis_p3_p4.ipynb, D_03_entregas.ipynb, D_04_opcional_meteorologia.ipynb

(Nota: los notebooks iniciales 01_descarga.ipynb y 02_carreras.ipynb corresponden a la Persona A).

## 2. Regla estricta de privacidad en notebooks
Nunca se puede mostrar en la salida de una celda ningún nombre (nome, apelidos) ni dorsal. Antes de hacer .head(), .sample() o mostrar cualquier DataFrame de interim/, es obligatorio pasar la tabla por quitar_identificadores():

```python
from src.proteccion import quitar_identificadores

# Correcto: muestra la tabla sin columnas personales
display(quitar_identificadores(tabla_carrera).head())
```

## 3. Estilo común de gráficas
Todas las gráficas del grupo usan la configuración centralizada en src/proteccion.py y se guardan en `output/figuras/` mediante `guardar_figura()`:
- Tamaño por defecto: 10x6 pulgadas (120 dpi en pantalla, 150 dpi al guardar).
- Paleta común (PALETA_COLORES): Azul (#1f77b4), Naranja (#ff7f0e), Verde (#2ca02c), Rojo (#d62728), Morado (#9467bd).
- Elementos obligatorios en cada gráfica:
  1. Título descriptivo (ax.set_title(...)).
  2. Etiquetas en ambos ejes indicando las unidades (ax.set_xlabel("Tiempo (segundos)"), ax.set_ylabel("Número de corredores")).
  3. Leyenda (ax.legend()) siempre que se comparen dos o más grupos (por ejemplo, sexo M/F o inscritos vs. por prueba).

Ejemplo de uso en los notebooks:

```python
import matplotlib.pyplot as plt
from src.proteccion import configurar_estilo_graficas, guardar_figura

configurar_estilo_graficas()

figura, eje = plt.subplots()
# ... código de la gráfica ...
eje.set_title("Participación por carrera y sexo")
eje.set_xlabel("Carrera del circuito")
eje.set_ylabel("Participantes (nº de personas)")
eje.legend(title="Sexo")

# Guarda automáticamente en output/figuras/p1_participacion_sexo.png
guardar_figura(figura, "p1_participacion_sexo.png")
```

## 4. Repositorio, acceso del docente y entrega en Moodle
- Enlace del repositorio para Moodle: https://github.com/RAnteloR/p2-coruna-corre
- Acceso del docente: El repositorio es público, por lo que el docente tiene acceso completo de lectura a todo el código, commits, issues y pull requests sin necesidad de invitación manual.
- Protección de archivos: El fichero .gitignore bloquea datos/raw/*, datos/interim/*, datos/clean/* y .env. Se ha verificado con git log --stat que no existe ningún dato personal ni clave en el historial de commits.
