from dataclasses import dataclass


@dataclass
class Project:

    name: str = ""
    path: str = ""

    backend: str = ""
    frontend: str = ""

    database: str = ""

    infrastructure: str = ""
    