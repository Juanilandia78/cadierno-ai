# Guía de comandos CLI — Cadierno AI

Ejecutá los ejemplos desde `cadierno-ai/cli` con `python3 cadierno.py` (o con
el Python de tu entorno virtual). Reemplazá `/ruta/proyecto` por la raíz del
proyecto destino.

## Flujo inicial recomendado

```bash
python3 cadierno.py install /ruta/proyecto
python3 cadierno.py bootstrap /ruta/proyecto
python3 cadierno.py memory init /ruta/proyecto
python3 cadierno.py adapters enable codex claude cursor gemini vscode copilot --path /ruta/proyecto
```

`install` instala `.cadierno-ai/` y bridges locales ignorados por Git; `bootstrap` analiza el código; `memory init`
prepara memoria local. Para un proyecto vacío, creá primero el stack base y
luego ejecutá `bootstrap` nuevamente.

## Comandos de proyecto

### `install [path]`

Instala el stack completo dentro de `.cadierno-ai/`. Los bridges de Codex,
Claude y Cursor son locales y no se versionan.

```bash
python3 cadierno.py install /ruta/proyecto
```

### `bootstrap [path]`

Detecta stack, arquitectura, integraciones y deuda técnica; genera o completa
los archivos de `.cadierno-ai/knowledge/` y actualiza el índice operativo
`.cadierno-ai/context.md`.

```bash
python3 cadierno.py bootstrap /ruta/proyecto
```

### `doctor`

Diagnostica la instalación local de Cadierno AI.

```bash
python3 cadierno.py doctor
```

### `update [path]`

Sincroniza assets de Cadierno con un proyecto. Revisa el resumen: los conflictos
locales se preservan y deben fusionarse manualmente.

```bash
python3 cadierno.py update /ruta/proyecto
```

### `finish [path]`

Muestra el estado Git y sugiere cierre. `--push` hace push solo si el repo está
limpio; `--branch` y `--tag` son opcionales.

```bash
python3 cadierno.py finish /ruta/proyecto
python3 cadierno.py finish /ruta/proyecto --push --tag v2.2.0
```

### `uninstall [path]`

Elimina assets de Cadierno. Usá `--purge` únicamente si también querés borrar
`.cadierno-ai/knowledge/` y `.cadierno-ai/memory/`.

```bash
python3 cadierno.py uninstall /ruta/proyecto
python3 cadierno.py uninstall /ruta/proyecto --purge
```

## Adaptadores y contexto

### `adapters enable`

Configura bridges locales para que Codex, Claude, Cursor, Gemini CLI y
VS Code/GitHub Copilot encuentren las instrucciones de Cadierno. Los archivos
generados se excluyen del Git local:
no se agregan al `.gitignore` versionado ni se suben al repositorio.

```bash
python3 cadierno.py adapters enable codex claude cursor gemini vscode copilot --path /ruta/proyecto
```

### `context generate [path]`

Regenera `.cadierno-ai/context.md`, el índice breve que indica a cualquier
asistente dónde leer el contexto, la filosofía de trabajo y los límites de
seguridad del proyecto.

```bash
python3 cadierno.py context generate /ruta/proyecto
```

## Skills opcionales

Las skills amplían capacidades puntuales, pero nunca se instalan solas. Primero
se sugieren según la tarea y luego requieren confirmación explícita.

```bash
python3 cadierno.py skills suggest "Consultar documentación actual de Laravel" --path /ruta/proyecto
python3 cadierno.py skills verify context7 --path /ruta/proyecto
python3 cadierno.py skills install context7 --path /ruta/proyecto --scope project
```

`--scope project` las instala en `.cadierno-ai/skills/`; `--scope global` las
instala en el perfil local del usuario. Revisá siempre origen y permisos antes
de confirmar una instalación. `skills verify` consulta el origen remoto y
comprueba que coincide con el proveedor oficial registrado antes de instalar.

## Aprendizaje supervisado

Al cerrar una tarea, Cadierno puede proponer decisiones, deuda o lecciones,
pero no actualiza conocimiento por su cuenta. La persona revisa y aprueba cada
ítem.

```bash
python3 cadierno.py learn propose /ruta/proyecto
python3 cadierno.py learn apply .cadierno-ai/learning/proposal-AAAAMMDD-HHMMSS.md --path /ruta/proyecto
```

Los ítems aprobados se agregan localmente a `.cadierno-ai/knowledge/decisions.md`,
`.cadierno-ai/knowledge/technical-debt.md` o `.cadierno-ai/memory/lessons.md`,
según corresponda.

## Ayuda para trabajar

### `assist <tarea> [path]`

Sugiere workflow y specialists según la tarea y la memoria disponible.

```bash
python3 cadierno.py assist "Agregar expiración de pagos pendientes" /ruta/proyecto
```

### `supervisor <tarea> [path]`

Inicia el flujo supervisor para organizar una idea o tarea compleja.

```bash
python3 cadierno.py supervisor "Implementar reservas online" /ruta/proyecto
```

## Memoria persistente

La memoria usa SQLite y tiene alcance `workspace` (un proyecto) o `user`
(todos los proyectos). La configuración de workspace tiene prioridad.

### Inicializar y consultar

```bash
python3 cadierno.py memory init /ruta/proyecto
python3 cadierno.py memory status /ruta/proyecto
python3 cadierno.py memory context /ruta/proyecto --scope workspace --limit 10
```

### Estilo y perfil

```bash
python3 cadierno.py memory style argentino /ruta/proyecto --scope workspace
python3 cadierno.py memory profile /ruta/proyecto --name "Juan" --role "Backend Engineer" --seniority "Senior" --scope user
```

Los estilos disponibles son `argentino` y `professional`.

### Historial, guardar y buscar

```bash
python3 cadierno.py memory history /ruta/proyecto --scope workspace --limit 20
python3 cadierno.py memory save /ruta/proyecto --title "Decisión" --content "Usar una capa de servicio" --type decision --tags arquitectura,backend
python3 cadierno.py memory search "capa de servicio" /ruta/proyecto --scope workspace --limit 10
```

Guardá decisiones, convenciones y contexto reusable; no guardes secretos,
credenciales ni conversaciones completas innecesarias.

## Ayuda integrada

```bash
python3 cadierno.py --help
python3 cadierno.py --plain doctor
python3 cadierno.py memory --help
python3 cadierno.py memory save --help
```
