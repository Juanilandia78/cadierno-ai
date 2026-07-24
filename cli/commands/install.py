from pathlib import Path
import shutil

from core.memory import add_history_event, initialize_memory
from utils.path import cadierno_root
from utils.git import ensure_local_cadierno_excludes
from core.context import generate_context
from ui import banner, success, info, warning


def copy_directory(source: Path, destination: Path):
    """
    Copia un directorio completo si no existe en destino.
    """

    if not source.exists():
        warning(f"No encontrado: {source.name}")
        return

    if destination.exists():
        info(f"Ya existe: {destination.name}")
        return

    shutil.copytree(source, destination)
    success(f"Copiado: {destination.name}")


def create_directory(path: Path):
    """
    Crea un directorio si no existe.
    """

    if not path.exists():
        path.mkdir(parents=True)
        success(f"Creado: {path.name}")


def create_file(path: Path, content: str):
    """
    Crea un archivo únicamente si no existe.
    """

    if path.exists():
        return

    path.write_text(content, encoding="utf-8")
    success(f"Archivo: {path.name}")


def install(path: str):

    project = Path(path).resolve()

    # cli/
    cli_dir = Path(__file__).resolve().parent.parent

    # raíz del framework
    framework = cli_dir.parent

    banner()

    print(f"Framework : {framework}")
    print(f"Proyecto  : {project}")
    print()

    if not project.exists():

        print("✖ La carpeta indicada no existe.")
        return

    if ensure_local_cadierno_excludes(project):
        print("✔ Exclusiones locales Git configuradas")
    else:
        print("• Proyecto sin Git: no se requieren exclusiones locales")

    print("Copiando framework...\n")

    cadierno = cadierno_root(project)
    create_directory(cadierno)
    copy_directory(framework / ".ai", cadierno / "ai")
    copy_directory(framework / "playbooks", cadierno / "playbooks")
    copy_directory(framework / "checklists", cadierno / "checklists")
    copy_directory(framework / "skills", cadierno / "skills")

    print()

    create_directory(cadierno / "knowledge")
    create_directory(cadierno / "memory")

    knowledge = cadierno / "knowledge"

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

    memory = cadierno / "memory"

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
    generate_context(project)
    add_history_event(project, "install", "Cadierno AI instalado en proyecto")

    template = framework / "templates" / "AGENTS.template.md"
    agent = cadierno / "AGENTS.md"

    if template.exists():

        if not agent.exists():

            shutil.copy2(template, agent)
            print("✔ Archivo: .cadierno-ai/AGENTS.md")

        else:

            print("• Ya existe: .cadierno-ai/AGENTS.md")

        root_agent = project / "AGENTS.md"
        if not root_agent.exists():
            shutil.copy2(template, root_agent)
            print("✔ Bridge local: AGENTS.md")
        else:
            print("• Se conserva AGENTS.md existente")

    claude_template = framework / "templates" / "CLAUDE.template.md"
    claude_file = cadierno / "CLAUDE.md"

    if claude_template.exists():

        if not claude_file.exists():

            shutil.copy2(claude_template, claude_file)
            print("✔ Archivo: .cadierno-ai/CLAUDE.md")

        elif "@AGENTS.md" in claude_file.read_text(encoding="utf-8", errors="ignore"):

            print("• Ya existe: .cadierno-ai/CLAUDE.md")

        else:

            print("⚠ Ya existe CLAUDE.md sin referenciar AGENTS.md: agregá la línea '@AGENTS.md' manualmente para que Claude Code cargue el contexto de Cadierno AI")

        root_claude = project / "CLAUDE.md"
        if not root_claude.exists():
            root_claude.write_text("@.cadierno-ai/AGENTS.md\n", encoding="utf-8")
            print("✔ Bridge local: CLAUDE.md")
        else:
            print("• Se conserva CLAUDE.md existente")

    print()
    print("===================================")
    print(" Instalación finalizada correctamente")
    print("===================================")
    print()
