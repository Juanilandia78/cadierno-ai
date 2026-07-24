# Manual de uso V3

Cadierno AI es el contexto, memoria y método local de un proyecto. No reemplaza
al asistente: trabajás con Codex, Claude, Cursor, Gemini CLI o VS Code/Copilot;
Cadierno les da un marco consistente y vos conservás la decisión final.

## La regla principal

1. Relevar antes de cambiar.
2. Diseñar antes de implementar cambios sensibles.
3. Dividir en microtareas, probar y mostrar evidencia.
4. Proponer decisiones, deuda y lecciones; nunca aplicarlas sin aprobación.

## Preparación inicial de un proyecto

Desde el repositorio de Cadierno AI:

```bash
./.venv/bin/python cli/cadierno.py install /ruta/proyecto
./.venv/bin/python cli/cadierno.py bootstrap /ruta/proyecto
./.venv/bin/python cli/cadierno.py adapters enable codex claude cursor gemini vscode copilot --path /ruta/proyecto
```

`install` instala el stack local; `bootstrap` releva el código; los adapters
conectan los asistentes. Los tres pasos son seguros frente a Git: Cadierno usa
`.git/info/exclude`, no modifica el `.gitignore` versionado y preserva bridges
que ya existían.

## Qué queda en el proyecto

```text
.cadierno-ai/
  context.md        índice de lectura para los asistentes
  AGENTS.md         reglas operativas locales
  knowledge/        proyecto, arquitectura, integraciones y deuda
  memory/           SQLite, historial y lecciones aprobadas
  playbooks/        guías técnicas
  skills/           catálogo e skills opcionales
  learning/         propuestas a revisar
```

Los bridges de raíz (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, reglas de Cursor y
`copilot-instructions.md`) son locales y no se publican.

## Flujo de trabajo real

Ejemplo: agregar expiración de una reserva pendiente de pago.

1. Pedile al asistente análisis y propuesta; no código todavía.
2. Revisá estados, webhook, idempotencia y riesgo de pago tardío.
3. Aprobá el diseño y pedí una microtarea concreta.
4. Exigí pruebas y evidencia al finalizar.
5. Si el aprendizaje es reusable, generá propuesta y aprobá sólo lo útil:

```bash
./.venv/bin/python cli/cadierno.py learn propose /ruta/proyecto
./.venv/bin/python cli/cadierno.py learn apply /ruta/proyecto/.cadierno-ai/learning/proposal-AAAAMMDD-HHMMSS.md --path /ruta/proyecto
```

## Usar conocimiento y memoria

Antes de una tarea, el asistente debe leer `context.md` y los archivos que éste
señale. Para inspeccionar la memoria manualmente:

```bash
./.venv/bin/python cli/cadierno.py memory context /ruta/proyecto --scope workspace --limit 10
./.venv/bin/python cli/cadierno.py memory search "Mercado Pago" /ruta/proyecto --scope workspace
```

Guardá observaciones manuales sólo si son reutilizables y no contienen secretos:

```bash
./.venv/bin/python cli/cadierno.py memory save /ruta/proyecto \
  --title "Decisión de pagos" \
  --content "Las reservas vencidas no se reactivan por un pago tardío." \
  --type decision --tags pagos,reservas
```

## Skills y documentación actual

Cuando una tarea depende de documentación de una librería, pedí sugerencias y
verificá el origen antes de instalar una skill:

```bash
./.venv/bin/python cli/cadierno.py skills suggest "Documentación actual de Laravel" --path /ruta/proyecto
./.venv/bin/python cli/cadierno.py skills verify context7 --path /ruta/proyecto
./.venv/bin/python cli/cadierno.py skills install context7 --path /ruta/proyecto --scope project
```

## Operación y actualización

```bash
./.venv/bin/python cli/cadierno.py doctor
./.venv/bin/python cli/cadierno.py update /ruta/proyecto
./.venv/bin/python cli/cadierno.py finish /ruta/proyecto
```

`finish` ayuda a revisar estado Git y cierre; no sustituye tu revisión de pull
request, pruebas de CI ni criterios de release.

## Dónde consultar cada cosa

- Instalación: [INSTALL.md](INSTALL.md)
- Primer uso: [QUICKSTART.md](QUICKSTART.md)
- Referencia total de flags y comandos: [GUIA_COMANDOS_CLI.md](GUIA_COMANDOS_CLI.md)
- Forma de trabajo explicada para quien empieza: [GUIA_USUARIO_JUNIOR.md](GUIA_USUARIO_JUNIOR.md)
