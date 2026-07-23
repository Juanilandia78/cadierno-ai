from pathlib import Path
import hashlib
import shutil

from core.memory import add_history_event, initialize_memory, set_generated_hash


# knowledge/*.md que bootstrap regenera y rastrea por hash (ver commands/bootstrap.py).
# Se registran acá para que la primera corrida de "bootstrap" después de "install"
# no confunda el stub estático de instalación con una edición manual del usuario.
BOOTSTRAP_MANAGED_KNOWLEDGE_FILES = {
    "project.md",
    "architecture.md",
    "integrations.md",
    "technical-debt.md",
    "workspace.md",
    "infrastructure.md",
}


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


def create_file(path: Path, content: str) -> bool:
    """
    Crea un archivo únicamente si no existe. Devuelve True si lo escribió.
    """

    if path.exists():
        return False

    path.write_text(content, encoding="utf-8")
    print(f"✔ Archivo: {path.name}")
    return True


def install(path: str, infra_root: str | None = None, no_workspace: bool = False):

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

    def create_tracked_knowledge_file(relative_name: str, content: str) -> None:
        written = create_file(knowledge / relative_name, content)
        if written and relative_name in BOOTSTRAP_MANAGED_KNOWLEDGE_FILES:
            # El stub recién escrito es contenido conocido de Cadierno, no una
            # edición manual: se registra para que "bootstrap" pueda
            # sobreescribirlo con seguridad en su primera corrida.
            content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
            set_generated_hash(project, f"knowledge/{relative_name}", content_hash)

    create_tracked_knowledge_file(
        "project.md",
        "# Proyecto\n\nInformación general del proyecto.\n"
    )

    create_tracked_knowledge_file(
        "architecture.md",
        "# Arquitectura\n\nArquitectura detectada automáticamente.\n"
    )

    create_file(
        knowledge / "decisions.md",
        "# Decisiones Técnicas\n\nConvenciones detectadas.\n"
    )

    create_tracked_knowledge_file(
        "integrations.md",
        "# Integraciones\n\nServicios externos detectados.\n"
    )

    create_tracked_knowledge_file(
        "technical-debt.md",
        "# Deuda Técnica\n\nPendientes encontrados durante el análisis.\n"
    )

    create_tracked_knowledge_file(
        "workspace.md",
        "# Workspace\n\nInformación del workspace de infraestructura compartida "
        "(docker-compose, servicios hermanos, etc.). Se completa con `cadierno bootstrap`.\n"
    )

    create_tracked_knowledge_file(
        "infrastructure.md",
        "# Infraestructura del Workspace\n\nDetalle técnico de servicios, redes, volúmenes "
        "y reverse proxy del workspace compartido. Se completa con `cadierno bootstrap`.\n"
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

    if infra_root or no_workspace:
        print()
        print("• La detección de workspace/infraestructura compartida se ejecuta con 'cadierno bootstrap',")
        print("  no con 'install'. Volvé a pasar --infra-root/--monorepo-root o --no-workspace en ese comando.")

    print()
    print("===================================")
    print(" Instalación finalizada correctamente")
    print("===================================")
    print()