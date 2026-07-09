from pathlib import Path

from core.memory import (
    add_history_event,
    classify_supervisor_task,
    get_effective_style,
    get_history,
    get_recent_context,
    get_memory_status,
    initialize_memory,
    save_observation,
    search_observations,
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


def memory_save(path: str, title: str, content: str, observation_type: str, tags: str | None, scope: str):

    project_path = Path(path).resolve()

    if not project_path.exists() or not project_path.is_dir():
        print("✖ La carpeta indicada no existe o no es válida.")
        return

    parsed_tags = [tag.strip() for tag in (tags or "").split(",") if tag.strip()]

    obs_id = save_observation(
        project_path,
        title=title,
        content=content,
        observation_type=observation_type,
        tags=parsed_tags,
        scope=scope,
    )

    add_history_event(project_path, "memory.save", f"obs_id={obs_id} type={observation_type} scope={scope}")

    print("\nMemory Save\n")
    print(f"✔ Observación guardada con ID: {obs_id}")


def memory_search(path: str, query: str, scope: str, limit: int):

    project_path = Path(path).resolve()

    if not project_path.exists() or not project_path.is_dir():
        print("✖ La carpeta indicada no existe o no es válida.")
        return

    rows = search_observations(project_path, query=query, scope=scope, limit=limit)

    print("\nMemory Search\n")
    print(f"Query: {query}")
    print(f"Scope: {scope}")
    print(f"Resultados: {len(rows)}\n")

    if not rows:
        print("• Sin resultados.")
        return

    for row in rows:
        content = row.get("content", "")
        if len(content) > 120:
            content = content[:120] + "..."
        print(f"- [{row['id']}] {row['title']} ({row['type']})")
        print(f"  {content}")


def memory_context(path: str, scope: str, limit: int):

    project_path = Path(path).resolve()

    if not project_path.exists() or not project_path.is_dir():
        print("✖ La carpeta indicada no existe o no es válida.")
        return

    context = get_recent_context(project_path, scope=scope, limit=limit)
    style = get_effective_style(project_path)

    print("\nMemory Context\n")
    print(f"Scope............. {context['scope']}")
    print(f"Estilo activo..... {style}")
    print(f"Eventos........... {len(context['events'])}")
    print(f"Observaciones..... {len(context['observations'])}\n")

    print("Eventos recientes:")
    if not context["events"]:
        print("- Sin eventos")
    else:
        for event in context["events"][-5:]:
            print(f"- {event['timestamp']} | {event['event']} | {event['details']}")

    print("\nObservaciones recientes:")
    if not context["observations"]:
        print("- Sin observaciones")
    else:
        for item in context["observations"][:5]:
            print(f"- [{item['id']}] {item['title']} ({item['type']})")


def assist(path: str, task: str):

    project_path = Path(path).resolve()

    if not project_path.exists() or not project_path.is_dir():
        print("✖ La carpeta indicada no existe o no es válida.")
        return

    text = task.lower()

    workflow = "maintenance"
    specialists = ["Architect", "Backend Engineer", "QA Engineer", "Code Reviewer"]

    if any(token in text for token in ["bug", "error", "fix", "falla", "rompe"]):
        workflow = "bugfix"
        specialists = ["Backend Engineer", "QA Engineer", "Code Reviewer"]
    elif any(token in text for token in ["legacy", "zend", "antiguo", "viejo"]):
        workflow = "legacy"
        specialists = ["Architect", "Backend Engineer", "QA Engineer"]
    elif any(token in text for token in ["nuevo", "feature", "funcionalidad", "crear"]):
        workflow = "new-feature"
        specialists = ["Architect", "Backend Engineer", "Database Specialist", "QA Engineer"]
    elif any(token in text for token in ["refactor", "limpiar", "cleanup", "deuda"]):
        workflow = "refactor"
        specialists = ["Architect", "Backend Engineer", "Code Reviewer"]
    elif any(token in text for token in ["auditar", "audit", "seguridad", "performance"]):
        workflow = "audit"
        specialists = ["Architect", "DevOps Specialist", "Code Reviewer"]
    elif any(token in text for token in ["explicar", "explain", "entender", "comprender"]):
        workflow = "explain-code"
        specialists = ["Documentation Specialist", "Backend Engineer"]

    add_history_event(project_path, "assist", f"workflow={workflow} task={task}")

    print("\nCadierno Assist\n")
    print(f"Tarea.............. {task}")
    print(f"Workflow sugerido.. {workflow}")
    print("Specialists........ " + ", ".join(specialists))


def supervisor(path: str, task: str):

    project_path = Path(path).resolve()

    if not project_path.exists() or not project_path.is_dir():
        print("✖ La carpeta indicada no existe o no es válida.")
        return

    plan = classify_supervisor_task(task)

    add_history_event(project_path, "supervisor", f"workflow={plan['workflow']} task={task}")

    print("\nCadierno Supervisor\n")
    print(f"Idea............... {task}")

    if plan["questions"]:
        print("Falta aclarar......")
        for question in plan["questions"]:
            print(f"- {question}")
    else:
        print("Falta aclarar...... No")

    print(f"Workflow sugerido.. {plan['workflow']}")
    print("Specialists........ " + ", ".join(plan["specialists"]))
    print("\nSiguiente paso..... Responder la duda si la hay, o delegar la implementacion al especialista indicado.")
