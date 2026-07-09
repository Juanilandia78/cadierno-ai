from pathlib import Path
import shutil


def _remove_path(path: Path) -> bool:

    if not path.exists():
        return False

    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()

    return True


def uninstall(path: str, purge: bool = False):

    project = Path(path).resolve()

    print("\nUninstall\n")
    print(f"Proyecto: {project}\n")

    if not project.exists() or not project.is_dir():
        print("✖ La carpeta indicada no existe o no es válida.")
        return

    removed = 0

    base_targets = [
        project / ".ai",
        project / "playbooks",
        project / "checklists",
        project / "AGENTS.md",
    ]

    for target in base_targets:
        if _remove_path(target):
            print(f"✔ Eliminado: {target.name}")
            removed += 1
        else:
            print(f"• No existe: {target.name}")

    if purge:
        purge_targets = [
            project / "knowledge",
            project / "memory",
        ]

        for target in purge_targets:
            if _remove_path(target):
                print(f"✔ Eliminado (purge): {target.name}")
                removed += 1
            else:
                print(f"• No existe: {target.name}")
    else:
        print("\n• Se conservan knowledge/ y memory/ (usar --purge para eliminarlos).")

    print("\nResumen:")
    print(f"✔ Elementos eliminados: {removed}")
    print("\nUninstall finalizado.")