import os

import pandas as pd

RANGOS = ["0%", "1%-5%", "6%-10%", "más de 10%"]


def rango_descuento(descuento):
    if descuento == 0:
        return "0%"
    if descuento <= 0.05:
        return "1%-5%"
    if descuento <= 0.10:
        return "6%-10%"
    return "más de 10%"


def resumir(grupo):
    # Indicadores de rentabilidad de un conjunto de líneas
    ventas = grupo["Sales"].sum()
    utilidad = grupo["Profit"].sum()
    perdidas = grupo["Profit"] < 0
    return pd.Series(
        {
            "lines": len(grupo),
            "sales": round(ventas, 4),
            "profit": round(utilidad, 4),
            "profit_margin": round(utilidad / ventas, 4),
            "loss_lines": int(perdidas.sum()),
            "loss_line_rate": round(perdidas.mean(), 4),
            "lost_profit": round(-grupo.loc[perdidas, "Profit"].sum(), 4),
        }
    )


def pregunta_01() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Una cadena de suministros de oficina vende mucho, pero la gerencia
    sospecha que parte de esas ventas no deja utilidad. El archivo
    `data/superstore_orders.csv.gz` tiene una fila por línea de pedido, con
    el número de pedido (`Order ID`), las ventas (`Sales`), la utilidad
    (`Profit`), el descuento aplicado (`Discount`, como proporción), el
    segmento del cliente (`Customer Segment`) y la categoría del producto
    (`Product Category`). Una utilidad negativa significa que la línea se
    vendió con pérdida.

    Use estas definiciones:

    - Margen (`profit_margin`): utilidad sobre ventas.
    - Línea con pérdida: una línea cuya utilidad es negativa.
    - `loss_line_rate`: la proporción de líneas con pérdida.
    - `lost_profit`: la suma de las pérdidas de las líneas con pérdida,
      escrita como número positivo.
    - Rango de descuento (`discount_band`): `0%` si no hubo descuento,
      `1%-5%` si fue mayor que 0 y hasta 5 %, `6%-10%` si fue mayor que 5 % y
      hasta 10 %, y `más de 10%` en otro caso.

    Genere tres archivos en `submission/`, sin el índice de Pandas y con las
    columnas en el orden indicado:

    1. `profitability_summary.csv`, con una sola fila: `lines` (cantidad de
       líneas), `orders` (pedidos distintos), `sales`, `profit`,
       `profit_margin`, `loss_lines` (cantidad de líneas con pérdida),
       `loss_line_rate` y `lost_profit`.

    2. `discount_summary.csv`, con una fila por rango de descuento, en el
       orden en que se definieron arriba: `discount_band`, `lines`, `sales`,
       `profit`, `profit_margin`, `loss_line_rate` y `lost_profit`.

    3. `priority_segments.csv`, con los cinco segmentos segmento–categoría
       que más utilidad pierden: `Customer Segment`, `Product Category`,
       `lines`, `sales`, `profit`, `profit_margin` y `lost_profit`. Considere
       solamente segmentos con al menos 100 líneas y ordénelos por
       `lost_profit` de mayor a menor.

    La función también debe retornar las tres tablas, en el mismo orden.

    Ejemplo del formato de `discount_summary.csv`:

        discount_band,lines,sales,profit,profit_margin,loss_line_rate,...
        0%,166,170539.05,29472.3789,0.1728,0.488,...
        ...
    """

    # El archivo usa ";" como separador y "," como decimal; utf-8-sig quita el BOM
    df = pd.read_csv(
        "data/superstore_orders.csv.gz",
        sep=";",
        decimal=",",
        encoding="utf-8-sig",
    )

    # 1. Resumen general
    general = resumir(df)
    general["orders"] = df["Order ID"].nunique()
    summary = pd.DataFrame([general])[
        [
            "lines",
            "orders",
            "sales",
            "profit",
            "profit_margin",
            "loss_lines",
            "loss_line_rate",
            "lost_profit",
        ]
    ]

    # 2. Resumen por rango de descuento
    df["discount_band"] = df["Discount"].apply(rango_descuento)
    discounts = (
        df.groupby("discount_band")[["Sales", "Profit"]]
        .apply(resumir)
        .reindex(RANGOS)
        .reset_index()
    )[
        [
            "discount_band",
            "lines",
            "sales",
            "profit",
            "profit_margin",
            "loss_line_rate",
            "lost_profit",
        ]
    ]

    # 3. Segmentos segmento–categoría que más utilidad pierden
    segments = (
        df.groupby(["Customer Segment", "Product Category"])[["Sales", "Profit"]]
        .apply(resumir)
        .reset_index()
    )
    segments = segments[segments["lines"] >= 100]
    segments = segments.sort_values("lost_profit", ascending=False).head(5)
    segments = segments[
        [
            "Customer Segment",
            "Product Category",
            "lines",
            "sales",
            "profit",
            "profit_margin",
            "lost_profit",
        ]
    ].reset_index(drop=True)

    # Las cantidades de líneas se guardan como enteros
    for tabla in [summary, discounts, segments]:
        for columna in ["lines", "orders", "loss_lines"]:
            if columna in tabla:
                tabla[columna] = tabla[columna].astype(int)

    os.makedirs("submission", exist_ok=True)
    summary.to_csv("submission/profitability_summary.csv", index=False)
    discounts.to_csv("submission/discount_summary.csv", index=False)
    segments.to_csv("submission/priority_segments.csv", index=False)

    return summary, discounts, segments