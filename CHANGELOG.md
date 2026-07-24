# Changelog

## v0.3.0

- Stack de proyecto unificado bajo `.cadierno-ai/`.
- Bridges locales e ignorados por Git para Codex, Claude, Cursor, Gemini CLI y
  VS Code/GitHub Copilot.
- Índice operativo `.cadierno-ai/context.md`, actualizado por install,
  bootstrap y update.
- Catálogo de skills opcionales con sugerencia, verificación de origen oficial
  e instalación confirmada.
- Aprendizaje supervisado: propuestas y aplicación individual con aprobación
  humana.
- Salida de consola mejorada con Rich y `--plain` para CI y logs.
- Pruebas V3 para contexto y catálogo de skills.

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
