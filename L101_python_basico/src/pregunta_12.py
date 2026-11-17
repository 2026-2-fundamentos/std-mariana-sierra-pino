import csv
import gzip


def pregunta_12():
    """
    Para cada letra de la primera columna (`letter`), sume todos los valores
    numéricos de los pares `clave:valor` de la quinta columna (`metrics`).
    Retorne un diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"A": 177, "B": 187, "C": 114, ...}
    """

    with gzip.open("data/data.csv.gz", mode="rt", encoding="utf-8") as file:
        filas = list(csv.reader(file, delimiter="\t"))

    suma = {}
    for fila in filas:
        letra = fila[0]
        for par in fila[4].split(","):
            valor = int(par.split(":")[1])
            suma[letra] = suma.get(letra, 0) + valor

    return dict(sorted(suma.items()))