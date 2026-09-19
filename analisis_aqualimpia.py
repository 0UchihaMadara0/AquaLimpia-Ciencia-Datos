from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import pearsonr


# ==========================================================
# 1. CONFIGURACIÓN DE RUTAS
# ==========================================================

# Carpeta donde está guardado este archivo .py
BASE_DIR = Path(__file__).resolve().parent

# Dataset
archivo = BASE_DIR / "dataset_set_A_aguas_residuales.xlsx"

# Carpetas para resultados
carpeta_graficos = BASE_DIR / "graficos"
carpeta_salidas = BASE_DIR / "outputs"

carpeta_graficos.mkdir(parents=True, exist_ok=True)
carpeta_salidas.mkdir(parents=True, exist_ok=True)


# ==========================================================
# 2. CARGA DEL DATASET
# ==========================================================

if not archivo.exists():
    raise FileNotFoundError(
        f"No se encontró el archivo:\n{archivo}\n\n"
        "Verifique que el Excel esté en la misma carpeta que este script."
    )

df = pd.read_excel(archivo)

print("=" * 60)
print("PROYECTO AQUÁLIMPIA S.A. - ANÁLISIS EXPLORATORIO")
print("=" * 60)

print("\nDataset cargado correctamente.")
print(f"Cantidad de registros: {len(df)}")
print(f"Cantidad de columnas: {len(df.columns)}")


# ==========================================================
# 3. VALIDACIÓN DE COLUMNAS NECESARIAS
# ==========================================================

columnas_requeridas = [
    "fecha_registro",
    "planta",
    "caudal_entrada_m3_d",
    "DBO_entrada_mg_L",
    "DBO_salida_mg_L",
    "energia_aeracion_kWh",
    "lodos_generados_kg_d",
    "cumplimiento_norma"
]

columnas_faltantes = [
    columna
    for columna in columnas_requeridas
    if columna not in df.columns
]

if columnas_faltantes:
    raise ValueError(
        "Faltan las siguientes columnas en el dataset: "
        + ", ".join(columnas_faltantes)
    )


# ==========================================================
# 4. PREPARACIÓN DE LOS DATOS
# ==========================================================

df["fecha_registro"] = pd.to_datetime(
    df["fecha_registro"],
    errors="coerce"
)

# Ordenar cronológicamente los registros
df = df.sort_values("fecha_registro").reset_index(drop=True)

# Cálculo de eficiencia de remoción de DBO
df["eficiencia_remocion_pct"] = (
    (
        df["DBO_entrada_mg_L"]
        - df["DBO_salida_mg_L"]
    )
    / df["DBO_entrada_mg_L"]
) * 100

# Crear una variable más fácil de interpretar
df["estado_cumplimiento"] = df["cumplimiento_norma"].map(
    {
        1: "Cumple",
        0: "No cumple"
    }
)


# ==========================================================
# 5. INDICADORES GENERALES
# ==========================================================

dbo_salida_promedio = df["DBO_salida_mg_L"].mean()

eficiencia_promedio = df[
    "eficiencia_remocion_pct"
].mean()

cumplimiento_general = (
    df["cumplimiento_norma"].mean() * 100
)

print("\n" + "=" * 60)
print("INDICADORES GENERALES")
print("=" * 60)

print(
    f"DBO de salida promedio: "
    f"{dbo_salida_promedio:.2f} mg/L"
)

print(
    f"Eficiencia promedio de remoción: "
    f"{eficiencia_promedio:.2f}%"
)

print(
    f"Cumplimiento normativo general: "
    f"{cumplimiento_general:.2f}%"
)


# ==========================================================
# 6. ANÁLISIS POR PLANTA
# ==========================================================

resumen_planta = (
    df.groupby("planta")
    .agg(
        registros=(
            "planta",
            "size"
        ),
        caudal_promedio=(
            "caudal_entrada_m3_d",
            "mean"
        ),
        dbo_entrada_promedio=(
            "DBO_entrada_mg_L",
            "mean"
        ),
        dbo_salida_promedio=(
            "DBO_salida_mg_L",
            "mean"
        ),
        eficiencia_promedio=(
            "eficiencia_remocion_pct",
            "mean"
        ),
        cumplimiento=(
            "cumplimiento_norma",
            "mean"
        )
    )
    .reset_index()
)

resumen_planta["cumplimiento_pct"] = (
    resumen_planta["cumplimiento"] * 100
)

print("\n" + "=" * 60)
print("RESUMEN POR PLANTA")
print("=" * 60)

print(
    resumen_planta[
        [
            "planta",
            "registros",
            "caudal_promedio",
            "dbo_entrada_promedio",
            "dbo_salida_promedio",
            "eficiencia_promedio",
            "cumplimiento_pct"
        ]
    ].round(2).to_string(index=False)
)


# ==========================================================
# 7. CORRELACIÓN DBO DE ENTRADA VS DBO DE SALIDA
# ==========================================================

datos_correlacion = df[
    [
        "DBO_entrada_mg_L",
        "DBO_salida_mg_L"
    ]
].dropna()

correlacion, p_valor = pearsonr(
    datos_correlacion["DBO_entrada_mg_L"],
    datos_correlacion["DBO_salida_mg_L"]
)

print("\n" + "=" * 60)
print("ANÁLISIS DE CORRELACIÓN")
print("=" * 60)

print(
    f"Correlación de Pearson: "
    f"{correlacion:.3f}"
)

if p_valor < 0.001:
    print("P-valor: < 0.001")
else:
    print(
        f"P-valor: "
        f"{p_valor:.3f}"
    )


# ==========================================================
# 8. GRÁFICO: CUMPLIMIENTO POR PLANTA
# ==========================================================

cumplimiento_planta = (
    df.groupby("planta")["cumplimiento_norma"]
    .mean()
    .mul(100)
)

fig, ax = plt.subplots(figsize=(9, 5))

cumplimiento_planta.plot(
    kind="bar",
    ax=ax
)

ax.set_title(
    "Cumplimiento normativo por planta"
)

ax.set_xlabel(
    "Planta de tratamiento"
)

ax.set_ylabel(
    "Cumplimiento (%)"
)

ax.tick_params(
    axis="x",
    rotation=0
)

# Mostrar el porcentaje sobre cada barra
for contenedor in ax.containers:
    ax.bar_label(
        contenedor,
        fmt="%.1f%%",
        padding=3
    )

# Agregar espacio superior
ax.set_ylim(
    0,
    cumplimiento_planta.max() + 8
)

plt.tight_layout()

ruta_grafico_1 = (
    carpeta_graficos
    / "cumplimiento_por_planta.png"
)

plt.savefig(
    ruta_grafico_1,
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# ==========================================================
# 9. GRÁFICO: DBO ENTRADA VS DBO SALIDA
# ==========================================================

fig, ax = plt.subplots(figsize=(9, 6))

for planta in sorted(df["planta"].dropna().unique()):

    datos_planta = df[
        df["planta"] == planta
    ]

    ax.scatter(
        datos_planta["DBO_entrada_mg_L"],
        datos_planta["DBO_salida_mg_L"],
        label=planta,
        alpha=0.7
    )

ax.set_title(
    "Relación entre DBO de entrada y DBO de salida"
)

ax.set_xlabel(
    "DBO de entrada (mg/L)"
)

ax.set_ylabel(
    "DBO de salida (mg/L)"
)

ax.legend(
    title="Planta"
)

ax.grid(
    alpha=0.2
)

plt.tight_layout()

ruta_grafico_2 = (
    carpeta_graficos
    / "dbo_entrada_vs_salida.png"
)

plt.savefig(
    ruta_grafico_2,
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# ==========================================================
# 10. GRÁFICO: EVOLUCIÓN TEMPORAL DE DBO DE SALIDA
# ==========================================================

fig, ax = plt.subplots(figsize=(11, 6))

for planta in sorted(df["planta"].dropna().unique()):

    datos_planta = df[
        df["planta"] == planta
    ].sort_values("fecha_registro")

    ax.plot(
        datos_planta["fecha_registro"],
        datos_planta["DBO_salida_mg_L"],
        marker="o",
        markersize=3,
        linewidth=1,
        label=planta
    )

ax.set_title(
    "Evolución temporal de la DBO de salida"
)

ax.set_xlabel(
    "Fecha de registro"
)

ax.set_ylabel(
    "DBO de salida (mg/L)"
)

ax.legend(
    title="Planta"
)

ax.grid(
    alpha=0.2
)

plt.xticks(
    rotation=45
)

plt.tight_layout()

ruta_grafico_3 = (
    carpeta_graficos
    / "evolucion_dbo_salida.png"
)

plt.savefig(
    ruta_grafico_3,
    dpi=300,
    bbox_inches="tight"
)

plt.show()
plt.close()


# ==========================================================
# 11. ARCHIVO DE SALIDA PARA OPERACIONES
# ==========================================================

operaciones = df[
    [
        "fecha_registro",
        "planta",
        "caudal_entrada_m3_d",
        "DBO_entrada_mg_L",
        "DBO_salida_mg_L",
        "energia_aeracion_kWh",
        "lodos_generados_kg_d",
        "eficiencia_remocion_pct",
        "estado_cumplimiento"
    ]
].copy()

operaciones.to_excel(
    carpeta_salidas
    / "salida_operaciones.xlsx",
    index=False
)


# ==========================================================
# 12. ARCHIVO DE SALIDA PARA GESTIÓN AMBIENTAL
# ==========================================================

gestion_ambiental = df[
    [
        "fecha_registro",
        "planta",
        "DBO_salida_mg_L",
        "eficiencia_remocion_pct",
        "estado_cumplimiento"
    ]
].copy()

gestion_ambiental.to_excel(
    carpeta_salidas
    / "salida_gestion_ambiental.xlsx",
    index=False
)


# ==========================================================
# 13. EXPORTACIÓN DEL RESUMEN POR PLANTA
# ==========================================================

resumen_exportar = resumen_planta[
    [
        "planta",
        "registros",
        "caudal_promedio",
        "dbo_entrada_promedio",
        "dbo_salida_promedio",
        "eficiencia_promedio",
        "cumplimiento_pct"
    ]
].copy()

resumen_exportar.to_excel(
    carpeta_salidas
    / "resumen_por_planta.xlsx",
    index=False
)


# ==========================================================
# 14. MENSAJE FINAL
# ==========================================================

print("\n" + "=" * 60)
print("ANÁLISIS FINALIZADO CORRECTAMENTE")
print("=" * 60)

print("\nGráficos generados:")

print(
    "- cumplimiento_por_planta.png"
)

print(
    "- dbo_entrada_vs_salida.png"
)

print(
    "- evolucion_dbo_salida.png"
)

print("\nArchivos generados:")

print(
    "- salida_operaciones.xlsx"
)

print(
    "- salida_gestion_ambiental.xlsx"
)

print(
    "- resumen_por_planta.xlsx"
)

print(
    f"\nCarpeta del proyecto:\n{BASE_DIR}"
)