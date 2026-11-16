# Contrato de datos (tabla limpia)

Tabla que sale de la limpieza (issue #4 / #9), una por carrera, en `datos/clean/`.
La usan C(Ismael) para ligar personas y D(Carlos) para cruzar con inscritos.
No se sube al repo porque lleva nombres.

## Columnas

| Columna | Tipo | Qué es |
|---|---|---|
| carrera_id | texto | id de la carrera (el de la web, ej. evento-3212) |
| orden | entero | orden en el circuito (1-6) |
| dorsal | texto | dorsal |
| nome | texto | nombre (solo para ligar, luego se quita) |
| apelidos | texto | apellidos (igual que nome) |
| posto | entero | puesto en la absoluta |
| sexo | texto | M o F |
| posto_sexo | entero | puesto dentro del sexo (M-3 → 3) |
| categoria | texto | SUB20, SUB23, SNR, MS1, MS2, MS3, MS4 o ESPECIAL |
| posto_categoria | entero | puesto en la categoría (MS2M-1 → 1) |
| tempo_s | entero | tiempo en segundos (00:28:36 → 1716) |
| tempo_marca | texto | ok / faltante / imposible |

## Decisiones

- El sexo lo saco de "Puesto Sexo" y miro que coincida con la letra final de la categoría (MS2**M**). Si no coincide lo apunto en el informe de calidad.
- Las categorías van con el código que usan las carreras (ver `datos/externos/categorias.csv`). Si sale alguna que no está en la tabla, la paso a ESPECIAL y lo explico.
- Los tiempos no se borran, se marcan:
  - faltante = no hay tiempo
  - imposible = 0, negativo, menos de 12 min o más de 1 h (cierre de control)
  - ok = el resto
- La categoría de una persona no debería cambiar entre carreras (art. 3 del regulamento: se fija con la edad del 14/03). Si cambia, es un problema de calidad.

## Falta por cerrar
- Cómo será el carrera_id - hablarlo con A (Raul).
- Si a C o a D les falta alguna columna.