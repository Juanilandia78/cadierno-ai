from pathlib import Path
import shutil

from core.memory import add_history_event
from utils.path import cadierno_root


def _remove_path(path: Path) -> bool:

    if not path.exists():
        return False

    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()

    return True


def _remove_claude_bridge(path: Path) -> str:
    """
    Elimina CLAUDE.md solo si es el bridge generado por Cadierno (@AGENTS.md).
    Si el usuario le agregó contenido propio, se conserva.
    """

    if not path.exists():
        return "missing"

    content = path.read_text(encoding="utf-8", errors="ignore").strip()

    if content != "@AGENTS.md":
        return "customized"

    path.unlink()
    return "removed"


def uninstall(path: str, purge: bool = False):

    project = Path(path).resolve()

    print("\nUninstall\n")
    print(f"Proyecto: {project}\n")

    if not project.exists() or not project.is_dir():
        print("✖ La carpeta indicada no existe o no es válida.")
        return

    add_history_event(project, "uninstall.start", f"purge={purge}")

    removed = 0

    cadierno = cadierno_root(project)
    base_targets = [
        cadierno / "ai",
        cadierno / "playbooks",
        cadierno / "checklists",
        cadierno / "AGENTS.md",
    ]

    for target in base_targets:
        if _remove_path(target):
            print(f"✔ Eliminado: {target.name}")
            removed += 1
        else:
            print(f"• No existe: {target.name}")

    claude_result = _remove_claude_bridge(cadierno / "CLAUDE.md")

    if claude_result == "removed":
        print("✔ Eliminado: CLAUDE.md")
        removed += 1
    elif claude_result == "customized":
        print("⚠ CLAUDE.md personalizado: se conserva (no se toca)")
    else:
        print("• No existe: CLAUDE.md")

    if purge:
        purge_targets = [cadierno / "knowledge", cadierno / "memory"]

        for target in purge_targets:
            if _remove_path(target):
                print(f"✔ Eliminado (purge): {target.name}")
                removed += 1
            else:
                print(f"• No existe: {target.name}")
    else:
        print("\n• Se conserva .cadierno-ai/knowledge y .cadierno-ai/memory (usar --purge para eliminarlos).")

    print("\nResumen:")
    print(f"✔ Elementos eliminados: {removed}")

    # Si purge=True, la memoria de workspace puede desaparecer luego de este punto.
    add_history_event(None, "uninstall.finish", f"project={project} removed={removed} purge={purge}")

    print("\nUninstall finalizado.")
