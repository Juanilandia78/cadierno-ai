from pathlib import Path
from datetime import datetime
import subprocess
from core.memory import add_history_event, initialize_memory

from utils.path import cadierno_root
from ui import banner, console, success, warning


def propose(path: str) -> None:
    project = Path(path).resolve()
    if not project.is_dir():
        raise SystemExit("✖ Proyecto inválido.")
    learning = cadierno_root(project) / "learning"
    learning.mkdir(parents=True, exist_ok=True)
    status = subprocess.run(["git", "status", "--short"], cwd=project, capture_output=True, text=True, check=False).stdout.strip()
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    target = learning / f"proposal-{stamp}.md"
    target.write_text(f"""# Propuesta de aprendizaje

Estado: pendiente de aprobación humana
Generada: {datetime.now().isoformat(timespec='seconds')}

## Evidencia observada

```text
{status or '(sin cambios Git detectados)'}
```

## Decisiones propuestas

- [ ] Agregar decisión con evidencia y justificación.

## Deuda técnica propuesta

- [ ] Agregar deuda priorizada, impacto y siguiente paso.

## Lecciones propuestas

- [ ] Agregar lección reutilizable con contexto.

No aplicar automáticamente. Revisar con `cadierno learn apply`.
""", encoding="utf-8")
    banner(); console.print("\n[bold]Propuesta de aprendizaje[/]")
    success(f"Borrador creado: {target}")
    warning("No se modificó knowledge ni memoria. Completá y aprobá los ítems antes de aplicar.")


def apply(path: str, proposal: str) -> None:
    project = Path(path).resolve()
    source = Path(proposal).resolve()
    if not source.is_file() or cadierno_root(project) / "learning" not in source.parents:
        raise SystemExit("✖ La propuesta debe pertenecer a .cadierno-ai/learning/ del proyecto.")
    sections = {"Decisiones propuestas": "decisions.md", "Deuda técnica propuesta": "technical-debt.md", "Lecciones propuestas": "lessons.md"}
    current = None; applied = 0; rejected = 0; updated = []
    for line in source.read_text(encoding="utf-8").splitlines():
        if line.startswith("## "):
            current = line[3:]
            updated.append(line)
            continue
        if current not in sections or not line.startswith("- [ ] "):
            updated.append(line)
            continue
        item = line[6:].strip()
        if item.startswith("Agregar "):
            updated.append(line)
            continue
        choice = input(f"\n{current}: {item}\n[1] Aprobar  [2] Editar  [3] Rechazar: ").strip()
        if choice == "2":
            item = input("Texto final: ").strip()
        if choice == "3":
            updated.append(f"- [x] {item} _(rechazada)_")
            rejected += 1
            continue
        if choice not in {"1", "2"} or not item:
            updated.append(line)
            continue
        target = cadierno_root(project) / ("knowledge" if sections[current] != "lessons.md" else "memory") / sections[current]
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("a", encoding="utf-8") as file:
            file.write(f"\n- {item}\n")
        updated.append(f"- [x] {item} _(aprobada)_")
        applied += 1
    source.write_text("\n".join(updated) + "\n", encoding="utf-8")
    initialize_memory(project)
    add_history_event(project, "learn.apply", f"proposal={source.name} applied={applied} rejected={rejected}")
    banner(); success(f"Aprendizajes aplicados: {applied}; rechazados: {rejected}")
