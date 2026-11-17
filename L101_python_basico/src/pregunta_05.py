import csv
import gzip


def pregunta_05():
    """
    Para cada letra de la primera columna (`letter`), encuentre el valor
    máximo y el valor mínimo de la segunda columna (`value`). Retorne una lista
    de tuplas `(letra, máximo, mínimo)` ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 9, 2), ("B", 9, 1), ...]
    """

    with gzip.open("data/data.csv.gz", mode="rt", encoding="utf-8") as file:
        filas = list(csv.reader(file, delimiter="\t"))

    valores = {}
    for fila in filas:
        valores.setdefault(fila[0], []).append(int(fila[1]))

    return [(letra, max(v), min(v)) for letra, v in sorted(valores.items())]