from dataclasses import dataclass, field


@dataclass
class Project:

    name: str = ""
    path: str = ""

    language: str = ""
    framework: str = ""

    backend: str = ""
    frontend: str = ""

    database: str = ""

    infrastructure: str = ""

    detected_files: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    architecture_components: list[str] = field(default_factory=list)
    integrations: list[str] = field(default_factory=list)
    