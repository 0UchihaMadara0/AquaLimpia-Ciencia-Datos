from pathlib import Path

from joblib import dump, load


def guardar_resultados(objeto, ruta_archivo):
    """
    Guarda un objeto de Python mediante Joblib.
    """

    ruta = Path(
        ruta_archivo
    )

    ruta.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    dump(
        objeto,
        ruta
    )

    return ruta


def cargar_resultados(ruta_archivo):
    """
    Recupera un objeto almacenado previamente
    mediante Joblib.
    """

    ruta = Path(
        ruta_archivo
    )

    if not ruta.exists():
        raise FileNotFoundError(
            f"No se encontró el archivo: {ruta}"
        )

    return load(
        ruta
    )