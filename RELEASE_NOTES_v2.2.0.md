# Cadierno AI v2.2.0

> Notas históricas de V2.2. Para el release vigente consultá `CHANGELOG.md` y
> la documentación V3 en `docs/README.md`.

Version orientada a uso diario estable, con memoria persistente mejorada e instalacion multiplataforma.

## Highlights

- Memoria persistente migrada a SQLite (usuario + workspace).
- Nuevos comandos memory: init, status, style, profile, history, save, search y context.
- Nuevo comando assist para sugerencia de workflow y especialistas.
- Servidor MCP-like local por stdio JSON-RPC en cli/mcp_memory_server.py.
- Test suite de memoria en cli/tests/test_memory.py.
- Instaladores locales:
  - install/install_cli.sh (macOS/Linux)
  - install/install_cli.ps1 (Windows)
- Documentacion de instalacion y quickstart actualizada.
- Limpieza de artefactos de cache Python (__pycache__, .pyc).

## Estado del Proyecto

- V2.2: completado y apto para trabajo diario.
- V3: queda en backlog para evolucion de plataforma e integraciones avanzadas.

## Notas Operativas

- SQLite no requiere instalacion separada: Cadierno usa sqlite3 del standard library de Python.
- El uso de .venv es recomendado (no obligatorio) para evitar conflictos de dependencias.
