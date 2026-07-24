from pathlib import Path

from utils.path import cadierno_root


def generate_context(project_path: Path) -> Path:
    root = cadierno_root(project_path)
    root.mkdir(parents=True, exist_ok=True)
    target = root / "context.md"
    target.write_text("""# Cadierno Context

Este archivo es el índice operativo local del proyecto. No reemplaza la documentación: indica qué cargar según la tarea.

## Lectura obligatoria

1. `AGENTS.md` para reglas operativas.
2. `knowledge/project.md` y `knowledge/architecture.md` antes de implementar.
3. `knowledge/integrations.md` cuando haya servicios externos.
4. `knowledge/technical-debt.md` antes de tocar flujos existentes.

## Filosofía de trabajo

- Definir alcance antes de modificar código.
- Relevar y mostrar evidencia; no asumir hechos críticos.
- Trabajar en microtareas con pruebas y criterio de cierre.
- No implementar diseños ni migraciones sin aprobación explícita.
- No versionar assets de Cadierno ni bridges de asistentes.
- No eliminar datos o archivos sin validar el objetivo exacto.
- Proponer decisiones, deuda y lecciones; aplicarlas sólo tras aprobación humana.

## Estructura

- `knowledge/`: verdad documental del proyecto.
- `memory/`: historial y memoria SQLite local.
- `playbooks/`: guías técnicas curadas con fuentes oficiales.
- `skills/`: procedimientos activables compatibles con Agent Skills.
- `learning/`: propuestas pendientes de aprobación.

Generado por Cadierno AI. Regenerar con `cadierno context generate`.
""", encoding="utf-8")
    return target
