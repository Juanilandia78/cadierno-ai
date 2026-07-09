# Changelog

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