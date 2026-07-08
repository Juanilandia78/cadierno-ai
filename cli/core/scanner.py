from pathlib import Path

from core.project import Project


def scan(path: Path) -> Project:

    project = Project()

    project.path = str(path)
    project.name = path.name

    return project
    