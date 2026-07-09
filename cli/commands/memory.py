from pathlib import Path

from core.memory import (
    add_history_event,
    get_history,
    get_memory_status,
    initialize_memory,
    set_style,
    update_profile,
)


def memory_init(path: str):

    project_path = Path(path).resolve()

    if not project_path.exists() or not project_path.is_dir():
        print("✖ La carpeta indicada no existe o no es válida.")
        return

    initialize_memory(project_path)
    add_history_event(project_path, "memory.init", "Inicialización manual de memoria")

    print("\nMemory Init\n")
    print(f"✔ Memoria inicializada en: {project_path}")


def memory_status(path: str):

    project_path = Path(path).resolve()

    if not project_path.exists() or not project_path.is_dir():
        print("✖ La carpeta indicada no existe o no es válida.")
        return

    status = get_memory_status(project_path)

    print("\nMemory Status\n")
    print(f"Proyecto............. {status['project']}")
    print(f"Estilo efectivo...... {status['effective_style']}")
    print(f"Workspace root....... {status['workspace']['root']}")
    print(f"Workspace history.... {status['workspace']['history_count']}")
    print(f"User root............ {status['user']['root']}")
    print(f"User history......... {status['user']['history_count']}")


def memory_set_style(path: str, style: str, scope: str):

    project_path = Path(path).resolve()

    if not project_path.exists() or not project_path.is_dir():
        print("✖ La carpeta indicada no existe o no es válida.")
        return

    try:
        set_style(project_path, style, scope)
    except ValueError as exc:
        print(f"✖ {exc}")
        return

    add_history_event(project_path, "memory.style", f"Style={style} scope={scope}")

    print("\nMemory Style\n")
    print(f"✔ Estilo actualizado: {style} (scope={scope})")


def memory_set_profile(
    path: str,
    name: str | None,
    role: str | None,
    seniority: str | None,
    scope: str,
):

    project_path = Path(path).resolve()

    if not project_path.exists() or not project_path.is_dir():
        print("✖ La carpeta indicada no existe o no es válida.")
        return

    if name is None and role is None and seniority is None:
        print("✖ Debes indicar al menos un campo: --name, --role o --seniority")
        return

    update_profile(project_path, name=name, role=role, seniority=seniority, scope=scope)

    details = f"scope={scope}"
    if name is not None:
        details += f" name={name}"
    if role is not None:
        details += f" role={role}"
    if seniority is not None:
        details += f" seniority={seniority}"

    add_history_event(project_path, "memory.profile", details)

    print("\nMemory Profile\n")
    print(f"✔ Perfil actualizado ({scope})")


def memory_history(path: str, scope: str, limit: int):

    project_path = Path(path).resolve()

    if not project_path.exists() or not project_path.is_dir():
        print("✖ La carpeta indicada no existe o no es válida.")
        return

    events = get_history(project_path, scope=scope, limit=limit)

    print("\nMemory History\n")
    print(f"Scope: {scope}")
    print(f"Mostrando: {len(events)} eventos\n")

    if not events:
        print("• Sin eventos aún.")
        return

    for event in events:
        timestamp = event.get("timestamp", "")
        name = event.get("event", "")
        details = event.get("details", "")
        print(f"- [{timestamp}] {name}: {details}")
