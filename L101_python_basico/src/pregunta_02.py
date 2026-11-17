import csv
import gzip


def pregunta_02():
    """
    Cuente cuántos registros hay para cada letra de la primera columna
    (`letter`). Retorne una lista de tuplas `(letra, cantidad)` ordenada
    alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 8), ("B", 7), ("C", 5), ...]
    """

    conteo = {}

    with gzip.open("data/data.csv.gz", mode="rt", encoding="utf-8") as file:
        for fila in csv.reader(file, delimiter="\t"):
            letra = fila[0]
            conteo[letra] = conteo.get(letra, 0) + 1

    return sorted(conteo.items())