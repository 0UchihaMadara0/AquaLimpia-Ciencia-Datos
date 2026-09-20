import numpy as np
from scipy.stats import pearsonr, zscore


def calcular_eficiencia_remocion(dbo_entrada, dbo_salida):
    """
    Calcula la eficiencia porcentual de remoción de DBO.
    """

    entrada = np.asarray(dbo_entrada, dtype=float)
    salida = np.asarray(dbo_salida, dtype=float)

    eficiencia = np.full(
        entrada.shape,
        np.nan,
        dtype=float
    )

    np.divide(
        entrada - salida,
        entrada,
        out=eficiencia,
        where=entrada != 0
    )

    eficiencia *= 100

    return eficiencia


def calcular_correlacion_pearson(variable_x, variable_y):
    """
    Calcula el coeficiente de correlación de Pearson
    y su correspondiente p-valor.
    """

    x = np.asarray(variable_x, dtype=float)
    y = np.asarray(variable_y, dtype=float)

    datos_validos = (
        np.isfinite(x)
        & np.isfinite(y)
    )

    x = x[datos_validos]
    y = y[datos_validos]

    if len(x) < 2:
        return np.nan, np.nan

    if np.std(x) == 0 or np.std(y) == 0:
        return np.nan, np.nan

    correlacion, p_valor = pearsonr(
        x,
        y
    )

    return (
        float(correlacion),
        float(p_valor)
    )


def detectar_atipicos_zscore(valores, umbral=3.0):
    """
    Detecta valores atípicos mediante Z-score.

    Se considera atípico un registro cuando el
    valor absoluto de su Z-score supera el umbral.
    """

    datos = np.asarray(
        valores,
        dtype=float
    )

    mascara_valida = np.isfinite(datos)

    resultado = np.zeros(
        len(datos),
        dtype=bool
    )

    if mascara_valida.sum() < 2:
        return resultado

    datos_validos = datos[
        mascara_valida
    ]

    if np.std(datos_validos) == 0:
        return resultado

    puntuaciones_z = zscore(
        datos_validos,
        nan_policy="omit"
    )

    resultado[mascara_valida] = (
        np.abs(puntuaciones_z)
        > umbral
    )

    return resultado