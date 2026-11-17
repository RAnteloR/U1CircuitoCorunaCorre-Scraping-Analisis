# Contrato de datos (tabla limpia)

Tabla que sale de la limpieza (issue #4 / #9), una por carrera, en `datos/interim/carrera_XX_limpia.csv`.
La usan C(Ismael) para ligar personas y D(Carlos) para cruzar con inscritos.
No se sube al repo porque lleva nombres.

## Columnas

| Columna | Tipo | Qué es |
|---|---|---|
| carrera_id | texto | id de la carrera: carrera_01 … carrera_06 (igual que los CSV de interim/) |
| orden | entero | orden en el circuito (1-6) |
| dorsal | texto | dorsal |
| nome | texto | nombre (solo para ligar, luego se quita) |
| apelidos | texto | apellidos (igual que nome) |
| posto | entero | puesto en la absoluta |
| sexo | texto | M o F |
| posto_sexo | entero | puesto dentro del sexo (M-3 → 3) |
| categoria | texto | SUB20, SUB23, SNR, MS1, MS2, MS3, MS4, ESP o SIN_CATEGORIA |
| posto_categoria | entero | puesto en la categoría (MS2M-1 → 1) |
| tempo_s | entero | tiempo en segundos (00:28:36 → 1716) |
| tempo_marca | texto | ok / faltante / imposible |

## Decisiones

- El sexo lo saco de "Puesto Sexo" y miro que coincida con la letra final de la categoría (MS2**M**). Si no coincide lo apunto en el informe de calidad.
- Las categorías van con el código que usan las carreras (ver `datos/externos/categorias.csv`).
- En los datos reales salen dos valores especiales: `ESP` (ESPM/ESPF, 3 filas) y `NO` (17 filas, sin categoría). `ESP` se queda como categoría; `NO` pasa a `SIN_CATEGORIA` con posto_categoria vacío. Si sale alguna otra que no esté en la tabla, lo explico en el informe de calidad.
- Los tiempos no se borran, se marcan:
  - faltante = no hay tiempo
  - imposible = negativo, por debajo de 2:30 min/km según la distancia de la carrera (12 min si no se sabe la distancia) o más de 1 h (cierre de control). Distancias en `datos/externos/distancias.csv`.
  - ok = el resto
- La categoría de una persona no debería cambiar entre carreras (art. 3 del regulamento: se fija con la edad del 14/03). Si cambia, es un problema de calidad.

## Falta por cerrar
- Si a C o a D les falta alguna columna.