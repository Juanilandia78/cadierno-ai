from pathlib import Path
import shutil


def ensure_directory(path: Path) -> None:
    """
    Crea un directorio si no existe.
    """
    path.mkdir(parents=True, exist_ok=True)


def copy_directory(source: Path, destination: Path) -> None:
    """
    Copia un directorio completo.
    Si existe, primero lo elimina.
    """

    if destination.exists():
        shutil.rmtree(destination)

    shutil.copytree(source, destination)


def copy_file(source: Path, destination: Path) -> None:
    """
    Copia un archivo.
    """

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    