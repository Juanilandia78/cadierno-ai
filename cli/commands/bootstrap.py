from pathlib import Path
import hashlib

from core.compose import ComposeService
from core.gitignore import ensure_gitignore_entries
from core.managed_sections import upsert_managed_section
from core.memory import (
    add_history_event,
    get_generated_hash,
    initialize_memory,
    mark_workspace_event,
    set_generated_hash,
    set_infra_workspace_metadata,
)
from core.scanner import scan
from core.workspace import (
    WorkspaceDetection,
    WorkspaceError,
    WorkspaceInfo,
    detect_workspace,
    scan_workspace,
)


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
- Este documento describe el contexto LOCAL de este proyecto. Si el proyecto
  forma parte de una infraestructura compartida, ver knowledge/workspace.md
  y knowledge/infrastructure.md para el contexto GLOBAL (no mezclar ambos).
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


def _render_service_block(name: str, service: ComposeService, is_matched: bool) -> str:

    marker = "  ← servicio de este proyecto" if is_matched else ""
    ports = ", ".join(service.ports) if service.ports else "No definidos"
    volumes = "\n".join(f"  - {volume}" for volume in service.volumes) if service.volumes else "  - No definidos"
    networks = ", ".join(service.networks) if service.networks else "No definidas"
    depends_on = ", ".join(service.depends_on) if service.depends_on else "Ninguna"
    env_names = ", ".join(service.environment_var_names) if service.environment_var_names else "Ninguna"
    env_files = ", ".join(service.env_files) if service.env_files else "Ninguno"

    return f"""### {name}{marker}

- Imagen: {service.image or 'N/A (build local)'}
- Build context: {service.build_context or 'N/A'}
- Container name: {service.container_name or 'N/A'}
- Puertos: {ports}
- Volúmenes:
{volumes}
- Redes: {networks}
- Depends on: {depends_on}
- Healthcheck: {'Sí' if service.healthcheck else 'No'}
- Variables de entorno (solo nombres): {env_names}
- env_file: {env_files}
"""


def _render_workspace_markdown(workspace_info: WorkspaceInfo, project_name: str) -> str:

    siblings = workspace_info.sibling_projects
    siblings_section = (
        "\n".join(f"- {sibling.name} ({', '.join(sibling.markers)})" for sibling in siblings)
        if siblings else "- No se detectaron otros proyectos dentro del workspace."
    )

    match = workspace_info.matched_service
    match_section = (
        f"- Servicio: {match.service_name or 'No identificado'}\n"
        f"- Confianza: {match.confidence}\n"
        f"- Motivo: {match.reason}"
    )

    env_files_section = (
        "\n".join(f"- {env_file}" for env_file in workspace_info.root_env_files)
        if workspace_info.root_env_files else "- No se encontraron archivos .env en la raíz del workspace."
    )

    evidence_section = ", ".join(workspace_info.evidence) if workspace_info.evidence else "N/A"

    return f"""# Workspace

## Estado de detección

- Proyecto: {project_name}
- Método de detección: {workspace_info.detection_method}
- Raíz del workspace: {workspace_info.root}
- Evidencia: {evidence_section}

## Proyectos y servicios en el workspace

{siblings_section}

## Servicio Docker de este proyecto

{match_section}

## Reverse proxy / Nginx

- Detectado: {'Sí' if workspace_info.nginx.detected else 'No'}
- Ver knowledge/infrastructure.md para el detalle de configuración y upstreams.

## Variables de entorno (solo nombres — ver knowledge/infrastructure.md)

{env_files_section}

## Observaciones

- Archivo generado automáticamente por cadierno bootstrap.
- Este documento describe el CONTEXTO GLOBAL del workspace compartido.
- Para el contexto y las convenciones de ESTE proyecto puntual, ver knowledge/project.md,
  architecture.md y decisions.md — no mezclar ambos contextos.
- Para el detalle técnico de servicios/redes/volúmenes/proxy, ver knowledge/infrastructure.md.
"""


def _render_infrastructure_markdown(workspace_info: WorkspaceInfo) -> str:

    compose = workspace_info.compose

    if compose is None:
        compose_summary = "No se encontró un archivo docker-compose/compose en la raíz del workspace."
        services_section = "- No aplica."
        networks_section = "- No aplica."
        volumes_section = "- No aplica."
    else:
        mode = (
            "YAML completo (PyYAML)"
            if compose.parsed
            else "heurístico (PyYAML no disponible o el archivo no se pudo parsear; solo nombres de servicio)"
        )
        compose_summary = f"Ruta: {workspace_info.compose_file}\nModo de parseo: {mode}"

        if compose.services:
            services_section = "\n".join(
                _render_service_block(name, service, name == workspace_info.matched_service.service_name)
                for name, service in compose.services.items()
            )
        elif compose.heuristic_service_names:
            services_section = "\n".join(
                f"- {name} (heurístico, sin detalle porque no hay PyYAML disponible)"
                for name in compose.heuristic_service_names
            )
        else:
            services_section = "- No se detectaron servicios."

        networks_section = (
            "\n".join(f"- {network}" for network in compose.networks)
            if compose.networks else "- No definidas explícitamente (o red externa/`external: true`)."
        )
        volumes_section = (
            "\n".join(f"- {volume}" for volume in compose.volumes)
            if compose.volumes else "- No definidos."
        )

    nginx = workspace_info.nginx
    nginx_files = "\n".join(f"- {file}" for file in nginx.config_files) if nginx.config_files else "- Ninguno"
    nginx_upstreams = (
        "\n".join(f"- {upstream}" for upstream in nginx.upstreams)
        if nginx.upstreams else "- No detectados"
    )

    if workspace_info.root_env_files:
        env_lines = []
        for env_file in workspace_info.root_env_files:
            names = workspace_info.root_env_var_names.get(env_file, [])
            names_text = ", ".join(names) if names else "Sin variables detectadas"
            env_lines.append(f"- {env_file}: {names_text}")
        env_section = "\n".join(env_lines)
    else:
        env_section = "- No se encontraron archivos .env en la raíz del workspace."

    return f"""# Infraestructura del Workspace

## Docker Compose

{compose_summary}

## Servicios detectados

{services_section}

## Redes

{networks_section}

## Volúmenes

{volumes_section}

## Reverse proxy / Nginx

- Detectado: {'Sí' if nginx.detected else 'No'}
- Archivos de configuración:
{nginx_files}
- Upstreams (heurístico, vía proxy_pass; validar manualmente):
{nginx_upstreams}

## Variables de entorno del workspace (solo nombres, nunca valores)

{env_section}

## Observaciones

- Nunca se registran valores de variables de entorno, solo nombres.
- El matching de servicio y la detección de Nginx son heurísticos: validar manualmente
  ante configuraciones complejas (includes, anchors YAML, condicionales, etc.).
- Archivo generado automáticamente por cadierno bootstrap. Contexto GLOBAL del workspace:
  no mezclar con las convenciones propias de este proyecto (ver knowledge/decisions.md).
"""


def _render_agents_workspace_section(project_path: Path, project, detection: WorkspaceDetection, workspace_info: WorkspaceInfo | None) -> str:

    lines: list[str] = []

    lines.append("### Proyecto actual\n")
    lines.append(f"- Nombre: {project.name}")
    lines.append(f"- Ruta: {project_path}\n")

    if workspace_info is not None and detection.root is not None:
        evidence = ", ".join(detection.evidence) if detection.evidence else "N/A"
        lines.append("### Workspace raíz\n")
        lines.append(f"- Ruta: {detection.root}")
        lines.append(f"- Método de detección: {detection.method}")
        lines.append(f"- Evidencia: {evidence}\n")

        match = workspace_info.matched_service
        lines.append("### Servicio Docker de este proyecto\n")
        lines.append(f"- Servicio: {match.service_name or 'No identificado'}")
        lines.append(f"- Confianza: {match.confidence}\n")

        lines.append("### Documentos de conocimiento a leer\n")
        lines.append("- knowledge/project.md, architecture.md, integrations.md, decisions.md, technical-debt.md: contexto de ESTE proyecto.")
        lines.append("- knowledge/workspace.md, infrastructure.md: contexto GLOBAL del workspace compartido. No mezclar convenciones de otros servicios con las de este proyecto.\n")
    else:
        lines.append("### Workspace raíz\n")
        lines.append("- No se detectó un workspace de infraestructura compartida para este proyecto. Se analiza como proyecto simple.")
        lines.append(f"- Motivo: {detection.reason}")
        lines.append("- Si este proyecto SÍ forma parte de una infraestructura compartida, ejecutá `cadierno bootstrap --infra-root <ruta>` (alias `--monorepo-root`).\n")

        lines.append("### Documentos de conocimiento a leer\n")
        lines.append("- knowledge/project.md, architecture.md, integrations.md, decisions.md, technical-debt.md: contexto de este proyecto.\n")

    lines.append("### Fuera del alcance normal del proyecto\n")
    lines.append("- Código fuente de otros servicios/proyectos dentro del workspace.")
    lines.append("- docker-compose.yml, nginx/ y demás infraestructura compartida: son de LECTURA para dar contexto; no se modifican como parte del trabajo normal de este proyecto.\n")

    lines.append("### Gobernanza de infraestructura\n")
    lines.append("- Se puede proponer cambios a infraestructura compartida (docker-compose.yml, nginx, redes, variables de entorno) únicamente cuando el pedido del usuario lo requiere explícitamente para ESTE proyecto.")
    lines.append("- Pedir aprobación humana antes de modificar cualquier archivo fuera de la carpeta de este proyecto.")
    lines.append("- Nunca modificar otro servicio del workspace sin autorización explícita del usuario.")

    return "\n".join(lines)


def _update_agents_workspace_section(project_path: Path, project, detection: WorkspaceDetection, workspace_info: WorkspaceInfo | None) -> None:

    agents_path = project_path / "AGENTS.md"
    existing = agents_path.read_text(encoding="utf-8", errors="ignore") if agents_path.exists() else ""

    section_content = _render_agents_workspace_section(project_path, project, detection, workspace_info)
    updated = upsert_managed_section(existing, "workspace", section_content)

    if updated == existing:
        print("• AGENTS.md: sección Workspace sin cambios")
        return

    agents_path.write_text(updated, encoding="utf-8")
    print("✔ AGENTS.md: sección Workspace actualizada")


def _write_knowledge_file(project_path: Path, knowledge_dir: Path, relative_name: str, content: str) -> None:

    target = knowledge_dir / relative_name
    tracking_key = f"knowledge/{relative_name}"
    new_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

    if target.exists():
        existing_content = target.read_text(encoding="utf-8", errors="ignore")
        current_hash = hashlib.sha256(existing_content.encode("utf-8")).hexdigest()

        if current_hash == new_hash:
            set_generated_hash(project_path, tracking_key, new_hash)
            print(f"• knowledge/{relative_name} sin cambios")
            return

        last_hash = get_generated_hash(project_path, tracking_key)

        if last_hash is None or current_hash != last_hash:
            backup_target = knowledge_dir / f"{relative_name}.cadierno-new"
            backup_target.write_text(content, encoding="utf-8")
            print(f"⚠ knowledge/{relative_name} personalizado: se conserva, nueva versión en {relative_name}.cadierno-new")
            return

    target.write_text(content, encoding="utf-8")
    set_generated_hash(project_path, tracking_key, new_hash)
    print(f"✔ knowledge/{relative_name} generado")


def bootstrap(path: str, infra_root: str | None = None, no_workspace: bool = False):

    project_path = Path(path).resolve()

    print("\nBootstrap\n")
    print(f"Proyecto: {project_path}")

    if not project_path.exists() or not project_path.is_dir():
        print("✖ La carpeta indicada no existe o no es válida.")
        return

    explicit_root = Path(infra_root).resolve() if infra_root else None

    try:
        detection = detect_workspace(project_path, explicit_root, no_workspace)
    except WorkspaceError as exc:
        print(f"✖ {exc}")
        return

    initialize_memory(project_path)

    project = scan(project_path)

    workspace_info: WorkspaceInfo | None = None
    if detection.method in ("explicit", "auto"):
        workspace_info = scan_workspace(detection, project_path)

    knowledge_dir = project_path / "knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)

    generated_files = {
        "project.md": _render_project_markdown(project),
        "architecture.md": _render_architecture_markdown(project),
        "integrations.md": _render_integrations_markdown(project),
        "technical-debt.md": _render_technical_debt_markdown(project),
    }

    if workspace_info is not None:
        generated_files["workspace.md"] = _render_workspace_markdown(workspace_info, project.name)
        generated_files["infrastructure.md"] = _render_infrastructure_markdown(workspace_info)

    print()
    for relative_name, content in generated_files.items():
        _write_knowledge_file(project_path, knowledge_dir, relative_name, content)

    _update_agents_workspace_section(project_path, project, detection, workspace_info)

    gitignore_result = ensure_gitignore_entries(project_path)
    if gitignore_result == "created":
        print("✔ .gitignore creado (ignora lo instalado por Cadierno)")
    elif gitignore_result == "updated":
        print("✔ .gitignore actualizado (ignora lo instalado por Cadierno)")

    set_infra_workspace_metadata(project_path, str(detection.root) if detection.root else None, detection.method)
    mark_workspace_event(project_path, "bootstrap")
    add_history_event(project_path, "bootstrap", "Análisis y generación de knowledge ejecutados")

    print("\nResultado:")
    print("✔ Proyecto analizado")

    if workspace_info is not None:
        print(f"✔ Workspace detectado ({detection.method}): {detection.root}")
        match = workspace_info.matched_service
        if match.service_name:
            print(f"✔ Servicio Docker identificado: {match.service_name} (confianza: {match.confidence})")
        else:
            print("• Servicio Docker: no se identificó ninguno para este proyecto")
    elif detection.method == "disabled":
        print("• Workspace: análisis deshabilitado explícitamente (--no-workspace)")
    else:
        print(f"• Workspace: {detection.reason}")
