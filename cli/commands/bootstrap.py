from pathlib import Path

from core.memory import add_history_event, initialize_memory, mark_workspace_event
from core.scanner import scan


def _render_project_markdown(project) -> str:

    dependencies = "\n".join(f"- {dep}" for dep in project.dependencies)
    if not dependencies:
        dependencies = "- No detectadas"

    detected_files = "\n".join(f"- {path}" for path in project.detected_files)
    if not detected_files:
        detected_files = "- No se encontraron archivos clave"

    return f"""# Proyecto

## Nombre

{project.name}

## Objetivo

Pendiente de completar por el equipo.

## Dominio del negocio

Pendiente de completar por el equipo.

## Stack Tecnológico

### Lenguaje

{project.language}

### Framework

{project.framework}

### Backend

{project.backend}

### Frontend

{project.frontend}

### Base de datos

{project.database}

### Infraestructura

{project.infrastructure}

## Dependencias principales

{dependencies}

## Integraciones

Pendiente de completar por el equipo.

## Arquitectura

Pendiente de completar por el equipo.

## Módulos principales

Pendiente de completar por el equipo.

## Riesgos conocidos

- Sin relevamiento aún.

## Observaciones

- Archivo generado automáticamente por cadierno bootstrap.
- Archivos detectados:
{detected_files}
"""


def _render_architecture_markdown(project) -> str:

    components = "\n".join(f"- {component}" for component in project.architecture_components)
    if not components:
        components = "- No detectados"

    tenancy_evidence = "\n".join(f"- {item}" for item in project.multitenancy_evidence)
    if not tenancy_evidence:
        tenancy_evidence = "- Sin evidencia"

    return f"""# Arquitectura

## Tipo de arquitectura

- Aplicación monolítica (estimada por estructura de carpetas).

## Multi-tenant

- Estado: {project.multitenancy}
- Estrategia: {project.multitenancy_strategy}
- Evidencia:
{tenancy_evidence}

## Estructura de carpetas

- Ruta analizada: {project.path}

## Flujo principal

- Solicitud HTTP -> capa de aplicación -> persistencia -> respuesta.

## Componentes

{components}

## Controllers

{('- Controllers detectados' if 'Controllers' in project.architecture_components else '- No detectado')}

## Services

{('- Services detectados' if 'Services' in project.architecture_components else '- No detectado')}

## Repositories

{('- Repositories detectados' if 'Repositories' in project.architecture_components else '- No detectado')}

## Models

{('- Models detectados' if 'Models' in project.architecture_components else '- No detectado')}

## Policies

{('- Policies detectadas' if 'Policies' in project.architecture_components else '- No detectado')}

## Middleware

{('- Middleware detectado' if 'Middleware' in project.architecture_components else '- No detectado')}

## Jobs

{('- Jobs detectados' if 'Jobs' in project.architecture_components else '- No detectado')}

## Events

{('- Events detectados' if 'Events' in project.architecture_components else '- No detectado')}

## Livewire

{('- Componentes Livewire detectados' if 'Livewire' in project.architecture_components else '- No detectado')}

## Actions

{('- Actions detectadas' if 'Actions' in project.architecture_components else '- No detectado')}

## Mail

{('- Mailables detectados' if 'Mail' in project.architecture_components else '- No detectado')}

## Notifications

{('- Notifications detectadas' if 'Notifications' in project.architecture_components else '- No detectado')}

## Providers

{('- Service Providers detectados' if 'Providers' in project.architecture_components else '- No detectado')}

## View Components

{('- View Components detectados' if 'View Components' in project.architecture_components else '- No detectado')}

## Dependencias entre módulos

- Pendiente de relevamiento detallado en una siguiente iteración.

## Observaciones

- Archivo generado automáticamente por cadierno bootstrap.
"""


def _render_integrations_markdown(project) -> str:

    integrations = set(project.integrations)

    apis = "\n".join(f"- {integration}" for integration in sorted(integrations))
    if not apis:
        apis = "- No detectadas"

    return f"""# Integraciones

## APIs

{apis}

## Mercado Pago

{('- Detectado' if 'Mercado Pago' in integrations else '- No detectado')}

## Stripe

{('- Detectado' if 'Stripe' in integrations else '- No detectado')}

## AWS

{('- Detectado' if 'AWS' in integrations else '- No detectado')}

## Cloudflare

{('- Detectado' if 'Cloudflare' in integrations else '- No detectado')}

## SMTP

{('- Detectado' if 'SMTP' in integrations else '- No detectado')}

## Storage

{('- S3/AWS detectado' if 'AWS' in integrations else '- No detectado')}

## Servicios externos

{apis}

## Tokens

- Pendiente de relevamiento manual seguro (sin exponer secretos).

## Observaciones

- Archivo generado automáticamente por cadierno bootstrap.
"""


def _render_technical_debt_markdown(project) -> str:

    items = "\n".join(f"- {item}" for item in project.technical_debt_items)
    if not items:
        items = "- No se detectaron marcadores de deuda técnica en esta pasada automática."

    return f"""# Deuda Técnica

## Hallazgos automáticos

{items}

## Acciones sugeridas

- Priorizar hallazgos con impacto en seguridad o datos.
- Corregir TODO/FIXME relacionados a flujos críticos.
- Dividir archivos grandes antes de agregar más funcionalidad.

## Observaciones

- Esta detección es heurística y debe validarse manualmente.
- Archivo generado automáticamente por cadierno bootstrap.
"""


def bootstrap(path: str):

    project_path = Path(path).resolve()

    print("\nBootstrap\n")
    print(f"Proyecto: {project_path}")

    if not project_path.exists() or not project_path.is_dir():
        print("✖ La carpeta indicada no existe o no es válida.")
        return

    initialize_memory(project_path)

    project = scan(project_path)

    knowledge_dir = project_path / "knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)

    target = knowledge_dir / "project.md"
    target.write_text(_render_project_markdown(project), encoding="utf-8")

    architecture_target = knowledge_dir / "architecture.md"
    architecture_target.write_text(_render_architecture_markdown(project), encoding="utf-8")

    integrations_target = knowledge_dir / "integrations.md"
    integrations_target.write_text(_render_integrations_markdown(project), encoding="utf-8")

    technical_debt_target = knowledge_dir / "technical-debt.md"
    technical_debt_target.write_text(_render_technical_debt_markdown(project), encoding="utf-8")

    mark_workspace_event(project_path, "bootstrap")
    add_history_event(project_path, "bootstrap", "Análisis y generación de knowledge ejecutados")

    print("\nResultado:")
    print("✔ Proyecto analizado")
    print("✔ knowledge/project.md generado")
    print("✔ knowledge/architecture.md generado")
    print("✔ knowledge/integrations.md generado")
    print("✔ knowledge/technical-debt.md generado")