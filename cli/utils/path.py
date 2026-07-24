from pathlib import Path

CADIERNO_DIRECTORY = ".cadierno-ai"


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


def cadierno_root(project_path: Path) -> Path:
    """Devuelve la única raíz de assets Cadierno dentro del proyecto."""
    return project_path / CADIERNO_DIRECTORY
