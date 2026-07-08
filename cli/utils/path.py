from pathlib import Path


def framework_root() -> Path:
    """
    Devuelve la carpeta raíz del framework Cadierno AI.
    """

    return Path(__file__).resolve().parents[2]


def project_root(path: str) -> Path:
    """
    Devuelve la carpeta del proyecto destino.
    """

    return Path(path).resolve()