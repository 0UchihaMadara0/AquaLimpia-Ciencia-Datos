from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px


# ==========================================================
# 1. CONFIGURACIÓN
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

archivo = BASE_DIR / "dataset_set_A_aguas_residuales.xlsx"

st.set_page_config(
    page_title="AquaLimpia S.A.",
    page_icon="💧",
    layout="wide"
)


# ==========================================================
# 2. TÍTULO
# ==========================================================

st.title("💧 Dashboard exploratorio - AquaLimpia S.A.")

st.write(
    """
    Este dashboard permite analizar el desempeño de las plantas
    de tratamiento de AquaLimpia S.A., considerando indicadores
    relacionados con DBO, eficiencia de remoción y cumplimiento
    normativo.
    """
)


# ==========================================================
# 3. CARGA DEL DATASET
# ==========================================================

if not archivo.exists():
    st.error(
        "No se encontró el archivo "
        "'dataset_set_A_aguas_residuales.xlsx'."
    )
    st.stop()


@st.cache_data
def cargar_datos(ruta):
    datos = pd.read_excel(ruta)

    datos["fecha_registro"] = pd.to_datetime(
        datos["fecha_registro"],
        errors="coerce"
    )

    datos = datos.sort_values(
        "fecha_registro"
    ).reset_index(drop=True)

    return datos


df = cargar_datos(archivo)


# ==========================================================
# 4. INDICADORES DERIVADOS
# ==========================================================

df["eficiencia_remocion_pct"] = (
    (
        df["DBO_entrada_mg_L"]
        - df["DBO_salida_mg_L"]
    )
    / df["DBO_entrada_mg_L"]
) * 100


df["estado_cumplimiento"] = (
    df["cumplimiento_norma"].map(
        {
            1: "Cumple",
            0: "No cumple"
        }
    )
)


# ==========================================================
# 5. FILTROS
# ==========================================================

st.sidebar.header("Filtros")

plantas_disponibles = sorted(
    df["planta"].dropna().unique()
)

plantas_seleccionadas = st.sidebar.multiselect(
    "Seleccione planta:",
    options=plantas_disponibles,
    default=plantas_disponibles
)


fecha_min = df["fecha_registro"].min().date()
fecha_max = df["fecha_registro"].max().date()

rango_fechas = st.sidebar.date_input(
    "Seleccione rango de fechas:",
    value=(fecha_min, fecha_max),
    min_value=fecha_min,
    max_value=fecha_max
)


# ==========================================================
# 6. APLICACIÓN DE FILTROS
# ==========================================================

df_filtrado = df[
    df["planta"].isin(
        plantas_seleccionadas
    )
].copy()


if len(rango_fechas) == 2:

    fecha_inicio = pd.Timestamp(
        rango_fechas[0]
    )

    fecha_fin = pd.Timestamp(
        rango_fechas[1]
    )

    df_filtrado = df_filtrado[
        (
            df_filtrado["fecha_registro"]
            >= fecha_inicio
        )
        &
        (
            df_filtrado["fecha_registro"]
            <= fecha_fin
        )
    ]


if df_filtrado.empty:
    st.warning(
        "No existen registros para los filtros seleccionados."
    )
    st.stop()


# ==========================================================
# 7. INDICADORES GENERALES
# ==========================================================

st.subheader("Indicadores generales")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Registros",
    f"{len(df_filtrado)}"
)

col2.metric(
    "DBO salida promedio",
    f"{df_filtrado['DBO_salida_mg_L'].mean():.2f} mg/L"
)

col3.metric(
    "Eficiencia promedio",
    f"{df_filtrado['eficiencia_remocion_pct'].mean():.2f}%"
)

col4.metric(
    "Cumplimiento normativo",
    f"{df_filtrado['cumplimiento_norma'].mean() * 100:.2f}%"
)


# ==========================================================
# 8. CUMPLIMIENTO POR PLANTA
# ==========================================================

st.subheader(
    "Cumplimiento normativo por planta"
)

cumplimiento_planta = (
    df_filtrado
    .groupby("planta")["cumplimiento_norma"]
    .mean()
    .mul(100)
    .reset_index()
)

cumplimiento_planta.columns = [
    "Planta",
    "Cumplimiento (%)"
]


fig_cumplimiento = px.bar(
    cumplimiento_planta,
    x="Planta",
    y="Cumplimiento (%)",
    text_auto=".1f",
    title="Porcentaje de cumplimiento normativo"
)

fig_cumplimiento.update_traces(
    texttemplate="%{y:.1f}%",
    textposition="outside"
)

st.plotly_chart(
    fig_cumplimiento,
    width="stretch"
)


# ==========================================================
# 9. DBO ENTRADA VS DBO SALIDA
# ==========================================================

st.subheader(
    "Relación entre DBO de entrada y DBO de salida"
)

fig_dbo = px.scatter(
    df_filtrado,
    x="DBO_entrada_mg_L",
    y="DBO_salida_mg_L",
    color="planta",
    hover_data=[
        "fecha_registro",
        "caudal_entrada_m3_d",
        "eficiencia_remocion_pct",
        "estado_cumplimiento"
    ],
    labels={
        "DBO_entrada_mg_L": "DBO de entrada (mg/L)",
        "DBO_salida_mg_L": "DBO de salida (mg/L)",
        "planta": "Planta"
    },
    title="DBO de entrada versus DBO de salida"
)

st.plotly_chart(
    fig_dbo,
    width="stretch"
)


# ==========================================================
# 10. EVOLUCIÓN TEMPORAL
# ==========================================================

st.subheader(
    "Evolución temporal de la DBO de salida"
)

df_temporal = df_filtrado.sort_values(
    "fecha_registro"
)

fig_temporal = px.line(
    df_temporal,
    x="fecha_registro",
    y="DBO_salida_mg_L",
    color="planta",
    markers=True,
    labels={
        "fecha_registro": "Fecha",
        "DBO_salida_mg_L": "DBO de salida (mg/L)",
        "planta": "Planta"
    },
    title="Comportamiento temporal de la DBO de salida"
)

st.plotly_chart(
    fig_temporal,
    width="stretch"
)


# ==========================================================
# 11. CAUDAL VS EFICIENCIA
# ==========================================================

st.subheader(
    "Caudal de entrada y eficiencia de remoción"
)

fig_caudal = px.scatter(
    df_filtrado,
    x="caudal_entrada_m3_d",
    y="eficiencia_remocion_pct",
    color="planta",
    hover_data=[
        "fecha_registro",
        "DBO_entrada_mg_L",
        "DBO_salida_mg_L",
        "estado_cumplimiento"
    ],
    labels={
        "caudal_entrada_m3_d": "Caudal de entrada (m³/d)",
        "eficiencia_remocion_pct": "Eficiencia de remoción (%)",
        "planta": "Planta"
    },
    title="Relación entre caudal de entrada y eficiencia"
)

st.plotly_chart(
    fig_caudal,
    width="stretch"
)


# ==========================================================
# 12. ENERGÍA DE AIREACIÓN VS DBO DE SALIDA
# ==========================================================

st.subheader(
    "Energía de aireación y calidad del efluente"
)

fig_energia = px.scatter(
    df_filtrado,
    x="energia_aeracion_kWh",
    y="DBO_salida_mg_L",
    color="planta",
    hover_data=[
        "fecha_registro",
        "eficiencia_remocion_pct",
        "estado_cumplimiento"
    ],
    labels={
        "energia_aeracion_kWh": "Energía de aireación (kWh)",
        "DBO_salida_mg_L": "DBO de salida (mg/L)",
        "planta": "Planta"
    },
    title="Energía de aireación versus DBO de salida"
)

st.plotly_chart(
    fig_energia,
    width="stretch"
)


# ==========================================================
# 13. TABLA DE REGISTROS
# ==========================================================

st.subheader(
    "Detalle de registros analizados"
)

columnas_tabla = [
    "fecha_registro",
    "planta",
    "caudal_entrada_m3_d",
    "DBO_entrada_mg_L",
    "DBO_salida_mg_L",
    "eficiencia_remocion_pct",
    "energia_aeracion_kWh",
    "lodos_generados_kg_d",
    "estado_cumplimiento"
]


tabla_dashboard = df_filtrado[
    columnas_tabla
].copy()


tabla_dashboard[
    "eficiencia_remocion_pct"
] = tabla_dashboard[
    "eficiencia_remocion_pct"
].round(2)


tabla_dashboard[
    "DBO_salida_mg_L"
] = tabla_dashboard[
    "DBO_salida_mg_L"
].round(2)


st.dataframe(
    tabla_dashboard,
    width="stretch"
)


# ==========================================================
# 14. MENSAJE FINAL
# ==========================================================

st.caption(
    "Fuente: elaboración propia a partir del dataset "
    "proporcionado para el caso AquaLimpia S.A."
)