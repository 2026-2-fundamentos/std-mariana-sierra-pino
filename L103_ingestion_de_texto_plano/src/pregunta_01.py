import re

import pandas as pd


def pregunta_01():
    """
    El archivo `data/clusters_report.txt` es un reporte de clústeres de
    palabras clave pensado para ser leído por una persona, no por un programa:
    los encabezados ocupan varias líneas, las columnas están alineadas con
    espacios y la lista de palabras clave de un clúster continúa en las líneas
    siguientes.

    Su tarea es convertir ese reporte en un DataFrame de Pandas con una fila
    por clúster y las columnas:

    - `cluster`: número del clúster, como entero.
    - `cantidad_de_palabras_clave`: como entero.
    - `porcentaje_de_palabras_clave`: como número decimal; por ejemplo, el
      texto `15,9 %` debe quedar como `15.9`.
    - `principales_palabras_clave`: todas las palabras clave del clúster en un
      solo texto, separadas por una coma y un único espacio.

    Retorne el DataFrame.

    Ejemplo del formato de la respuesta (se omite la última columna):

           cluster  cantidad_de_palabras_clave  porcentaje_de_palabras_clave
        0        1                         105                          15.9
        1        2                         102                          15.4
        ...
    """

    with open("data/clusters_report.txt", encoding="utf-8") as file:
        lineas = file.readlines()[4:]  # se saltan las 4 líneas del encabezado

    clusters = []
    for linea in lineas:
        if not linea.strip():
            continue

        # Una línea que empieza con "número número porcentaje %" abre un clúster
        inicio = re.match(r"^\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%\s*(.*)$", linea)
        if inicio:
            clusters.append(
                {
                    "cluster": int(inicio.group(1)),
                    "cantidad_de_palabras_clave": int(inicio.group(2)),
                    "porcentaje_de_palabras_clave": float(
                        inicio.group(3).replace(",", ".")
                    ),
                    "principales_palabras_clave": inicio.group(4),
                }
            )
        else:
            # Las demás líneas continúan las palabras clave del clúster actual
            clusters[-1]["principales_palabras_clave"] += " " + linea.strip()

    for cluster in clusters:
        texto = cluster["principales_palabras_clave"]
        texto = re.sub(r"\s+", " ", texto).strip().rstrip(".")
        palabras = [palabra.strip() for palabra in texto.split(",")]
        cluster["principales_palabras_clave"] = ", ".join(palabras)

    return pd.DataFrame(clusters)