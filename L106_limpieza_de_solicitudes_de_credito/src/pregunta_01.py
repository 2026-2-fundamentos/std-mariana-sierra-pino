import os

import pandas as pd

COLUMNAS = [
    "sexo",
    "tipo_de_emprendimiento",
    "idea_negocio",
    "barrio",
    "estrato",
    "comuna_ciudadano",
    "fecha_de_beneficio",
    "monto_del_credito",
    "línea_credito",
]

COLUMNAS_TEXTO = [
    "sexo",
    "tipo_de_emprendimiento",
    "idea_negocio",
    "barrio",
    "línea_credito",
]


def limpiar_texto(serie):
    # minúsculas, "_" y "-" pasan a espacio, y se deja un solo espacio entre palabras
    return (
        serie.str.lower()
        .str.replace(r"[_\-]", " ", regex=True)
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()
    )


def limpiar_fecha(serie):
    # Las fechas vienen como DD/MM/AAAA o como AAAA/MM/DD
    dia_primero = pd.to_datetime(serie, format="%d/%m/%Y", errors="coerce")
    anio_primero = pd.to_datetime(serie, format="%Y/%m/%d", errors="coerce")
    return dia_primero.fillna(anio_primero).dt.strftime("%Y-%m-%d")


def limpiar_monto(serie):
    # "$ 7,000,000.00" -> 7000000
    return (
        serie.astype(str)
        .str.replace(r"[$,\s]", "", regex=True)
        .astype(float)
        .astype(int)
    )


def pregunta_01():
    """
    El archivo `data/solicitudes_de_credito.csv.gz` contiene las solicitudes de
    un programa de crédito, pero llegó sucio: tiene una columna de índice que
    no pertenece a los datos, registros duplicados, registros incompletos y
    valores que representan lo mismo escritos de formas distintas en los
    campos de texto, las fechas, el estrato y el monto.

    Su tarea es limpiarlo y guardar el resultado en
    `submission/solicitudes_de_credito.csv`, usando punto y coma (`;`) como
    separador y sin el índice de Pandas.

    El archivo limpio debe cumplir lo siguiente:

    - Contiene solamente las nueve columnas `sexo`, `tipo_de_emprendimiento`,
      `idea_negocio`, `barrio`, `estrato`, `comuna_ciudadano`,
      `fecha_de_beneficio`, `monto_del_credito` y `línea_credito`, en ese
      orden.
    - Los campos de texto están en minúsculas y sus palabras separadas por
      espacios.
    - `estrato` y `monto_del_credito` son números enteros, sin símbolos ni
      separadores de miles.
    - Todas las fechas de `fecha_de_beneficio` usan un mismo formato, por
      ejemplo `AAAA-MM-DD`.
    - No hay registros incompletos. La única excepción es
      `comuna_ciudadano`: sus valores faltantes son parte de los datos
      originales y deben conservarse.
    - No hay registros duplicados.

    Ejemplo del formato del archivo:

        sexo;tipo_de_emprendimiento;idea_negocio;barrio;estrato;...
        femenino;comercio;almacen de ropa en;los cerros el vergel;2;...
        ...
    """

    # index_col=0 descarta la columna de índice que no pertenece a los datos
    df = pd.read_csv(
        "data/solicitudes_de_credito.csv.gz", sep=";", index_col=0
    )
    df = df[COLUMNAS].copy()

    for columna in COLUMNAS_TEXTO:
        df[columna] = limpiar_texto(df[columna])

    df["estrato"] = df["estrato"].astype(int)
    df["comuna_ciudadano"] = df["comuna_ciudadano"].astype("Int64")
    df["fecha_de_beneficio"] = limpiar_fecha(df["fecha_de_beneficio"])
    df["monto_del_credito"] = limpiar_monto(df["monto_del_credito"])

    # Registros incompletos (sin contar comuna_ciudadano) y duplicados
    columnas_obligatorias = [c for c in COLUMNAS if c != "comuna_ciudadano"]
    df = df.dropna(subset=columnas_obligatorias)
    df = df.drop_duplicates()

    os.makedirs("submission", exist_ok=True)
    df.to_csv("submission/solicitudes_de_credito.csv", sep=";", index=False)