import csv
import gzip


def pregunta_06():
    """
    La quinta columna (`metrics`) contiene pares `clave:valor` separados por
    comas. Para cada clave, encuentre el valor mínimo y el valor máximo que
    aparecen en todo el archivo. Retorne una lista de tuplas
    `(clave, mínimo, máximo)` ordenada alfabéticamente por la clave.

    Observe que el orden es mínimo y luego máximo, al contrario de la
    pregunta 5.

    Ejemplo del formato de la respuesta:

        [("aaa", 1, 9), ("bbb", 1, 9), ...]
    """

    with gzip.open("data/data.csv.gz", mode="rt", encoding="utf-8") as file:
        filas = list(csv.reader(file, delimiter="\t"))

    valores = {}
    for fila in filas:
        for par in fila[4].split(","):
            clave, valor = par.split(":")
            valores.setdefault(clave, []).append(int(valor))

    return [(clave, min(v), max(v)) for clave, v in sorted(valores.items())]