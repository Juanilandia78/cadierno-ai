from pathlib import Path
import hashlib
import shutil

from core.gitignore import ensure_gitignore_entries
from core.memory import add_history_event, initialize_memory, mark_workspace_event


_MANAGED_SECTION_MARKER = "<!-- cadierno:managed:start:"


SYNC_DIRECTORIES = [
    ".ai",
    "playbooks",
    "checklists",
]


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as file:
        for block in iter(lambda: file.read(8192), b""):
            digest.update(block)

    return digest.hexdigest()


def _safe_copy_tree(source: Path, destination: Path) -> tuple[int, int, int]:
    copied = 0
    unchanged = 0
    skipped = 0

    for source_file in source.rglob("*"):
        if source_file.is_dir():
            continue

        relative = source_file.relative_to(source)
        destination_file = destination / relative
        destination_file.parent.mkdir(parents=True, exist_ok=True)

        if not destination_file.exists():
            shutil.copy2(source_file, destination_file)
            copied += 1
            continue

        if _hash_file(source_file) == _hash_file(destination_file):
            unchanged += 1
            continue

        skipped += 1

    return copied, unchanged, skipped


def _safe_copy_file(source: Path, destination: Path) -> str:
    destination.parent.mkdir(parents=True, exist_ok=True)

    if not destination.exists():
        shutil.copy2(source, destination)
        return "copied"

    if _hash_file(source) == _hash_file(destination):
        return "unchanged"

    return "skipped"


def update(path: str, infra_root: str | None = None, no_workspace: bool = False):

    project = Path(path).resolve()
    framework = Path(__file__).resolve().parent.parent.parent

    print("\nUpdate\n")
    print(f"Framework : {framework}")
    print(f"Proyecto  : {project}\n")

    if not project.exists() or not project.is_dir():
        print("✖ La carpeta indicada no existe o no es válida.")
        return

    initialize_memory(project)

    total_copied = 0
    total_unchanged = 0
    total_skipped = 0

    print("Sincronizando directorios base...\n")

    for directory in SYNC_DIRECTORIES:
        source = framework / directory
        destination = project / directory

        if not source.exists():
            print(f"⚠ No encontrado en framework: {directory}")
            continue

        copied, unchanged, skipped = _safe_copy_tree(source, destination)
        total_copied += copied
        total_unchanged += unchanged
        total_skipped += skipped

        print(f"• {directory}: +{copied} | ={unchanged} | !{skipped}")

    print("\nSincronizando AGENTS.md...\n")

    template = framework / "templates" / "AGENTS.template.md"
    target_agents = project / "AGENTS.md"

    if template.exists():
        result = _safe_copy_file(template, target_agents)

        if result == "copied":
            print("✔ AGENTS.md copiado")
            total_copied += 1
        elif result == "unchanged":
            print("• AGENTS.md sin cambios")
            total_unchanged += 1
        else:
            existing = target_agents.read_text(encoding="utf-8", errors="ignore") if target_agents.exists() else ""
            if _MANAGED_SECTION_MARKER in existing:
                print("• AGENTS.md contiene secciones gestionadas (bootstrap): se conserva sin tocar")
            else:
                print("⚠ AGENTS.md personalizado: se conserva archivo local")
            total_skipped += 1
    else:
        print("⚠ No se encontró templates/AGENTS.template.md")

    print("\nSincronizando CLAUDE.md...\n")

    claude_template = framework / "templates" / "CLAUDE.template.md"
    target_claude = project / "CLAUDE.md"

    if claude_template.exists():
        result = _safe_copy_file(claude_template, target_claude)

        if result == "copied":
            print("✔ CLAUDE.md copiado (referencia a AGENTS.md)")
            total_copied += 1
        elif result == "unchanged":
            print("• CLAUDE.md sin cambios")
            total_unchanged += 1
        else:
            print("⚠ CLAUDE.md personalizado: se conserva archivo local")
            total_skipped += 1
    else:
        print("⚠ No se encontró templates/CLAUDE.template.md")

    print("\nResumen:")
    print(f"✔ Nuevos archivos copiados: {total_copied}")
    print(f"• Archivos sin cambios: {total_unchanged}")
    print(f"⚠ Archivos locales preservados (conflicto): {total_skipped}")

    gitignore_result = ensure_gitignore_entries(project)
    if gitignore_result == "created":
        print("✔ .gitignore creado (ignora lo instalado por Cadierno)")
    elif gitignore_result == "updated":
        print("✔ .gitignore actualizado (ignora lo instalado por Cadierno)")
    else:
        print("• .gitignore sin cambios")

    mark_workspace_event(project, "update")
    add_history_event(
        project,
        "update",
        f"copied={total_copied} unchanged={total_unchanged} skipped={total_skipped}",
    )

    if infra_root or no_workspace:
        print()
        print("• La detección de workspace/infraestructura compartida se ejecuta con 'cadierno bootstrap',")
        print("  no con 'update'. Volvé a pasar --infra-root/--monorepo-root o --no-workspace en ese comando.")

    print("\nUpdate finalizado (modo seguro).")
