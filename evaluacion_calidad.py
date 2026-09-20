from pathlib import Path

import pandas as pd

from src.funciones_analisis import detectar_atipicos_zscore


# ==========================================================
# 1. CONFIGURACIÓN DE RUTAS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

archivo = BASE_DIR / "dataset_set_A_aguas_residuales.xlsx"

carpeta_salidas = BASE_DIR / "outputs"
carpeta_salidas.mkdir(parents=True, exist_ok=True)

archivo_salida = carpeta_salidas / "informe_calidad_datos.xlsx"


# ==========================================================
# 2. CARGA DEL DATASET
# ==========================================================

if not archivo.exists():
    raise FileNotFoundError(
        f"No se encontró el archivo:\n{archivo}"
    )

df = pd.read_excel(archivo)

print("=" * 65)
print("EVALUACIÓN DE CALIDAD DE DATOS - AQUALIMPIA S.A.")
print("=" * 65)

print(f"\nRegistros analizados: {len(df)}")
print(f"Cantidad de columnas: {len(df.columns)}")


# ==========================================================
# 3. VALORES NULOS
# ==========================================================

nulos_por_columna = df.isnull().sum()
total_nulos = int(nulos_por_columna.sum())


# ==========================================================
# 4. REGISTROS DUPLICADOS
# ==========================================================

duplicados = int(df.duplicated().sum())


# ==========================================================
# 5. VALIDACIÓN DE FECHAS
# ==========================================================

fecha_original = df["fecha_registro"].copy()

fecha_convertida = pd.to_datetime(
    fecha_original,
    errors="coerce"
)

fechas_invalidas = int(
    (
        fecha_original.notna()
        & fecha_convertida.isna()
    ).sum()
)


# ==========================================================
# 6. VALIDACIÓN DE CUMPLIMIENTO
# ==========================================================

cumplimiento_invalido = int(
    (
        df["cumplimiento_norma"].notna()
        & ~df["cumplimiento_norma"].isin([0, 1])
    ).sum()
)


# ==========================================================
# 7. VALIDACIÓN DE VALORES NEGATIVOS
# ==========================================================

columnas_no_negativas = [
    "caudal_entrada_m3_d",
    "DBO_entrada_mg_L",
    "DBO_salida_mg_L",
    "energia_aeracion_kWh",
    "lodos_generados_kg_d",
]

negativos_por_columna = {}

for columna in columnas_no_negativas:
    if columna in df.columns:
        negativos_por_columna[columna] = int(
            (df[columna] < 0).sum()
        )

total_negativos = sum(negativos_por_columna.values())


# ==========================================================
# 8. CONSISTENCIA ENTRE DBO DE ENTRADA Y SALIDA
# ==========================================================

dbo_salida_mayor_entrada = int(
    (
        df["DBO_salida_mg_L"]
        > df["DBO_entrada_mg_L"]
    ).sum()
)


# ==========================================================
# 9. DETECCIÓN DE VALORES ATÍPICOS
# ==========================================================

df["atipico_dbo_salida"] = detectar_atipicos_zscore(
    df["DBO_salida_mg_L"],
    umbral=3.0
)

atipicos_dbo = int(
    df["atipico_dbo_salida"].sum()
)


# ==========================================================
# 10. RESUMEN DE CALIDAD
# ==========================================================

resumen = pd.DataFrame(
    {
        "Indicador de calidad": [
            "Registros analizados",
            "Valores nulos",
            "Registros duplicados",
            "Fechas inválidas",
            "Valores de cumplimiento inválidos",
            "Valores negativos",
            "Registros con DBO salida > DBO entrada",
            "Valores potencialmente atípicos en DBO de salida",
        ],
        "Resultado": [
            len(df),
            total_nulos,
            duplicados,
            fechas_invalidas,
            cumplimiento_invalido,
            total_negativos,
            dbo_salida_mayor_entrada,
            atipicos_dbo,
        ],
    }
)


# ==========================================================
# 11. RESULTADOS EN CONSOLA
# ==========================================================

print("\n" + "=" * 65)
print("RESUMEN DE LA EVALUACIÓN")
print("=" * 65)

print(f"Valores nulos: {total_nulos}")
print(f"Registros duplicados: {duplicados}")
print(f"Fechas inválidas: {fechas_invalidas}")
print(
    "Valores de cumplimiento inválidos: "
    f"{cumplimiento_invalido}"
)
print(f"Valores negativos detectados: {total_negativos}")
print(
    "Registros con DBO salida > DBO entrada: "
    f"{dbo_salida_mayor_entrada}"
)
print(
    "Valores potencialmente atípicos en DBO de salida: "
    f"{atipicos_dbo}"
)

print("\nVALORES NULOS POR COLUMNA")
print("-" * 65)
print(nulos_por_columna)

print("\nVALORES NEGATIVOS POR COLUMNA")
print("-" * 65)

for columna, cantidad in negativos_por_columna.items():
    print(f"{columna}: {cantidad}")


# ==========================================================
# 12. EXPORTACIÓN DEL INFORME
# ==========================================================

registros_revision = df[
    df["atipico_dbo_salida"]
    | (
        df["DBO_salida_mg_L"]
        > df["DBO_entrada_mg_L"]
    )
].copy()

with pd.ExcelWriter(
    archivo_salida,
    engine="openpyxl"
) as writer:

    resumen.to_excel(
        writer,
        sheet_name="Resumen",
        index=False
    )

    nulos_por_columna.rename(
        "Valores nulos"
    ).to_excel(
        writer,
        sheet_name="Nulos_por_columna"
    )

    registros_revision.to_excel(
        writer,
        sheet_name="Registros_revision",
        index=False
    )


print("\n" + "=" * 65)
print("EVALUACIÓN FINALIZADA CORRECTAMENTE")
print("=" * 65)

print(
    "\nInforme generado en:\n"
    f"{archivo_salida}"
)