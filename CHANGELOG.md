# Changelog

## v2.3.0

- Soporte de **workspace de infraestructura compartida** para proyectos dentro
  de un monorepo (docker-compose, servicios hermanos, nginx). Opcional y
  retrocompatible: un proyecto simple sigue funcionando exactamente igual.
  - `cadierno bootstrap` ahora detecta automáticamente un workspace superior
    (evidencia fuerte: `docker-compose.yml`/`.yaml`, `compose.yml`/`.yaml`;
    nunca cruza `$HOME`, la raíz del filesystem, ni un repo git ajeno).
  - Nuevos flags `--infra-root`/`--monorepo-root` (alias) y `--no-workspace`
    en `bootstrap`, `install` y `update`.
  - Nuevos `knowledge/workspace.md` y `knowledge/infrastructure.md`: contexto
    GLOBAL del workspace, separado del contexto local del proyecto.
  - Detección de servicio Docker correspondiente al proyecto (por
    `build.context` o bind-mount, con heurística de nombre como respaldo de
    baja confianza), redes, volúmenes, healthchecks, reverse proxy/Nginx.
  - Parseo de `docker-compose.yml` vía PyYAML si está disponible (dependencia
    opcional, con fallback heurístico sin PyYAML).
  - `AGENTS.md` ahora tiene una sección gestionada (`## Cadierno / Workspace`)
    que `bootstrap` actualiza sin tocar el resto del archivo ni contenido
    manual del equipo.
  - Nuevo mecanismo de hash para `knowledge/*.md` generados por `bootstrap`:
    si el archivo fue editado a mano desde la última generación, no se
    sobreescribe (se conserva el original y se escribe `archivo.md.cadierno-new`
    al lado). Esto también corrige un comportamiento previo de `bootstrap` que
    sobreescribía `knowledge/*.md` sin resguardo alguno.
  - Endurecimiento de seguridad: ningún archivo `.env` (ni sus variantes,
    p. ej. `.env.local`, `algo.env`) se vuelca nunca como contenido crudo en
    ningún buffer de análisis ni archivo generado; solo se registran nombres
    de variable, nunca valores.
  - Nuevos tests: detección de workspace, parseo de compose, extracción segura
    de variables de entorno, secciones gestionadas, e integración completa de
    `bootstrap` con workspace (incluye regresión del caso real de un compose
    compartido desactualizado respecto al proyecto).

## v2.2.0

- Memoria persistente migrada a SQLite (usuario + workspace).
- Nuevos comandos `memory` para init, status, style, profile, history, save, search y context.
- Nuevo comando `assist` para sugerencia de workflow y especialistas.
- Servidor MCP-like local por stdio JSON-RPC en `cli/mcp_memory_server.py`.
- Test suite de memoria agregada en `cli/tests/test_memory.py`.
- Instaladores locales agregados:
	- `install/install_cli.sh` (macOS/Linux)
	- `install/install_cli.ps1` (Windows)
- Documentacion de instalacion y quickstart actualizada.
- Limpieza de artefactos Python cache (`__pycache__`, `.pyc`) del repositorio.
- Playbook de ejecución por microtareas, cierre basado en evidencia e invariantes,
  mejoras de workflows y guía junior; documentación V2.2 corregida.

## v2.1.0

- Base de memoria persistente por usuario/workspace.
- Historial de eventos y preferencias de estilo.
- Mejoras iniciales de productividad para uso diario.

## v1.0.0

- Core Framework
- Specialists
- Workflows
- Playbooks
- Knowledge
- Checklists
- Bootstrap
