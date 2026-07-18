from pathlib import Path
import shutil

from core.memory import add_history_event, initialize_memory


def copy_directory(source: Path, destination: Path):
    """
    Copia un directorio completo si no existe en destino.
    """

    if not source.exists():
        print(f"⚠ No encontrado: {source.name}")
        return

    if destination.exists():
        print(f"• Ya existe: {destination.name}")
        return

    shutil.copytree(source, destination)
    print(f"✔ Copiado: {destination.name}")


def create_directory(path: Path):
    """
    Crea un directorio si no existe.
    """

    if not path.exists():
        path.mkdir(parents=True)
        print(f"✔ Creado: {path.name}")


def create_file(path: Path, content: str):
    """
    Crea un archivo únicamente si no existe.
    """

    if path.exists():
        return

    path.write_text(content, encoding="utf-8")
    print(f"✔ Archivo: {path.name}")


def install(path: str):

    project = Path(path).resolve()

    # cli/
    cli_dir = Path(__file__).resolve().parent.parent

    # raíz del framework
    framework = cli_dir.parent

    print()
    print("===================================")
    print("     Cadierno AI Installer")
    print("===================================")
    print()

    print(f"Framework : {framework}")
    print(f"Proyecto  : {project}")
    print()

    if not project.exists():

        print("✖ La carpeta indicada no existe.")
        return

    print("Copiando framework...\n")

    copy_directory(
        framework / ".ai",
        project / ".ai"
    )

    copy_directory(
        framework / "playbooks",
        project / "playbooks"
    )

    copy_directory(
        framework / "checklists",
        project / "checklists"
    )

    print()

    create_directory(project / "knowledge")
    create_directory(project / "memory")

    knowledge = project / "knowledge"

    create_file(
        knowledge / "project.md",
        "# Proyecto\n\nInformación general del proyecto.\n"
    )

    create_file(
        knowledge / "architecture.md",
        "# Arquitectura\n\nArquitectura detectada automáticamente.\n"
    )

    create_file(
        knowledge / "decisions.md",
        "# Decisiones Técnicas\n\nConvenciones detectadas.\n"
    )

    create_file(
        knowledge / "integrations.md",
        "# Integraciones\n\nServicios externos detectados.\n"
    )

    create_file(
        knowledge / "technical-debt.md",
        "# Deuda Técnica\n\nPendientes encontrados durante el análisis.\n"
    )

    memory = project / "memory"

    create_file(
        memory / "history.md",
        "# History\n\nHistorial del proyecto.\n"
    )

    create_file(
        memory / "lessons.md",
        "# Lessons\n\nLecciones aprendidas.\n"
    )

    create_file(
        memory / "preferences.md",
        "# Preferences\n\nPreferencias del proyecto.\n"
    )

    create_file(
        memory / "profile.md",
        "# Profile\n\nInformación general del proyecto.\n"
    )

    create_file(
        memory / "snippets.md",
        "# Snippets\n\nFragmentos reutilizables.\n"
    )

    initialize_memory(project)
    add_history_event(project, "install", "Cadierno AI instalado en proyecto")

    template = framework / "templates" / "AGENTS.template.md"
    agent = project / "AGENTS.md"

    if template.exists():

        if not agent.exists():

            shutil.copy2(template, agent)
            print("✔ Archivo: AGENTS.md")

        else:

            print("• Ya existe: AGENTS.md")

    claude_template = framework / "templates" / "CLAUDE.template.md"
    claude_file = project / "CLAUDE.md"

    if claude_template.exists():

        if not claude_file.exists():

            shutil.copy2(claude_template, claude_file)
            print("✔ Archivo: CLAUDE.md (referencia a AGENTS.md para Claude Code)")

        elif "@AGENTS.md" in claude_file.read_text(encoding="utf-8", errors="ignore"):

            print("• Ya existe: CLAUDE.md (ya referencia AGENTS.md)")

        else:

            print("⚠ Ya existe CLAUDE.md sin referenciar AGENTS.md: agregá la línea '@AGENTS.md' manualmente para que Claude Code cargue el contexto de Cadierno AI")

    print()
    print("===================================")
    print(" Instalación finalizada correctamente")
    print("===================================")
    print()