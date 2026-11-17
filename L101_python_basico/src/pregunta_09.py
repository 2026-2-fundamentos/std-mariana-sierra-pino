import csv
import gzip


def pregunta_09():
    """
    Cuente cuántas veces aparece cada clave en la quinta columna (`metrics`)
    de todo el archivo. Retorne un diccionario `{clave: cantidad}` con las
    claves en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"aaa": 13, "bbb": 16, "ccc": 23, ...}
    """

    with gzip.open("data/data.csv.gz", mode="rt", encoding="utf-8") as file:
        filas = list(csv.reader(file, delimiter="\t"))

    conteo = {}
    for fila in filas:
        for par in fila[4].split(","):
            clave = par.split(":")[0]
            conteo[clave] = conteo.get(clave, 0) + 1

    return dict(sorted(conteo.items()))