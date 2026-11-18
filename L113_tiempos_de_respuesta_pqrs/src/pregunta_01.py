import os

import numpy as np
import pandas as pd

ARCHIVOS = {
    "letter": "data/historical_requests_letter.csv.gz",
    "web": "data/historical_requests_web.csv.gz",
}

DIAS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

PLAZO = 15


def leer_solicitudes():
    canales = []
    for canal, archivo in ARCHIVOS.items():
        df = pd.read_csv(archivo)
        df = df.drop_duplicates()  # filas idénticas dentro de cada canal
        df["channel"] = canal
        canales.append(df)
    df = pd.concat(canales, ignore_index=True)

    df["in_date"] = pd.to_datetime(df["in_date"])
    df["out_date"] = pd.to_datetime(df["out_date"])
    df["answered"] = df["out_date"].notna()

    # Días calendario: diferencia entre las dos fechas
    df["calendar_days"] = (df["out_date"] - df["in_date"]).dt.days

    # Días hábiles: lunes a viernes después de la entrada, hasta la respuesta
    # incluida. busday_count(a, b) cuenta los días hábiles en [a, b), por eso
    # se le suma un día a ambas fechas.
    respondidas = df["answered"]
    inicio = (df.loc[respondidas, "in_date"] + pd.Timedelta(days=1)).values
    fin = (df.loc[respondidas, "out_date"] + pd.Timedelta(days=1)).values
    df["business_days"] = np.nan
    df.loc[respondidas, "business_days"] = np.busday_count(
        inicio.astype("datetime64[D]"), fin.astype("datetime64[D]")
    )

    # Cumple el plazo si fue respondida en 15 días hábiles o menos
    df["on_time"] = df["answered"] & (df["business_days"] <= PLAZO)
    return df


def resumir(grupo):
    respondidas = grupo[grupo["answered"]]
    return pd.Series(
        {
            "requests": len(grupo),
            "answered": int(grupo["answered"].sum()),
            "pending": int((~grupo["answered"]).sum()),
            "median_calendar_days": respondidas["calendar_days"].median(),
            "median_business_days": respondidas["business_days"].median(),
            "on_time_rate": round(grupo["on_time"].mean(), 4),
        }
    )


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Una entidad pública recibe peticiones, quejas, reclamos y sugerencias
    (PQRS) por dos canales, la página web y las cartas, y la ley le da 15 días
    hábiles para responder cada una. Su tarea es medir si la entidad cumple
    ese plazo.

    Los archivos `data/historical_requests_web.csv.gz` y
    `data/historical_requests_letter.csv.gz` tienen una fila por solicitud
    recibida entre 2016 y 2021 por cada canal, con su identificador
    (`record_id`), la fecha de entrada (`in_date`), el día de la semana de
    entrada (`day_name`) y la fecha de respuesta (`out_date`). Si `out_date`
    está vacía, la solicitud todavía no ha sido respondida.

    Tenga en cuenta lo siguiente:

    - Algunas solicitudes aparecen repetidas: elimine las filas idénticas
      dentro de cada canal, para contar cada solicitud una sola vez. Las
      filas sin `record_id` son solicitudes válidas.
    - Llame `letter` al canal de las cartas y `web` al de la página web.
    - Los días hábiles de respuesta son los días de lunes a viernes
      posteriores a la fecha de entrada, hasta la fecha de respuesta
      incluida. Por ejemplo, una solicitud que entra un viernes y se responde
      el lunes siguiente tardó 1 día hábil. No considere los festivos.
    - Los días calendario de respuesta son la diferencia entre la fecha de
      respuesta y la de entrada.
    - Una solicitud cumple el plazo si fue respondida en 15 días hábiles o
      menos. Una solicitud pendiente no ha cumplido el plazo.
    - `on_time_rate` es la proporción de solicitudes que cumplen el plazo,
      sobre el total de solicitudes, incluidas las pendientes.
    - Las medianas de días se calculan solamente con las solicitudes
      respondidas.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `channel_summary.csv`, con una fila por canal, en orden alfabético:
       `channel`, `requests`, `answered`, `pending`,
       `median_business_days` y `on_time_rate`.

    2. `yearly_summary.csv`, con una fila por año de entrada y canal,
       ordenada por año y luego por canal: `year`, `channel`, `requests`,
       `pending` y `on_time_rate`.

    3. `entry_day_summary.csv`, con una fila por día de entrada, de lunes a
       domingo, con los dos canales juntos: `day_name`, `requests`,
       `median_calendar_days` y `median_business_days`.

    Observe en el tercer archivo cómo cambia la lectura del tiempo de
    respuesta según se cuenten días calendario o días hábiles.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `channel_summary.csv`:

        channel,requests,answered,pending,median_business_days,on_time_rate
        letter,28138,...
        ...
    """

    df = leer_solicitudes()
    df["year"] = df["in_date"].dt.year
    columnas = [
        "answered",
        "calendar_days",
        "business_days",
        "on_time",
    ]

    # 1. Resumen por canal
    channel_summary = (
        df.groupby("channel")[columnas].apply(resumir).reset_index()
    )[
        [
            "channel",
            "requests",
            "answered",
            "pending",
            "median_business_days",
            "on_time_rate",
        ]
    ]

    # 2. Resumen por año de entrada y canal
    yearly_summary = (
        df.groupby(["year", "channel"])[columnas].apply(resumir).reset_index()
    )[["year", "channel", "requests", "pending", "on_time_rate"]]

    # 3. Resumen por día de entrada, con los dos canales juntos
    entry_day_summary = (
        df.groupby("day_name")[columnas].apply(resumir).reindex(DIAS).reset_index()
    )[["day_name", "requests", "median_calendar_days", "median_business_days"]]

    # Los conteos se guardan como enteros
    for tabla in [channel_summary, yearly_summary, entry_day_summary]:
        for columna in ["requests", "answered", "pending"]:
            if columna in tabla:
                tabla[columna] = tabla[columna].astype(int)

    os.makedirs("submission", exist_ok=True)
    channel_summary.to_csv("submission/channel_summary.csv", index=False)
    yearly_summary.to_csv("submission/yearly_summary.csv", index=False)
    entry_day_summary.to_csv("submission/entry_day_summary.csv", index=False)

    return channel_summary, yearly_summary, entry_day_summary