# Guía de trabajo en equipo con Cadierno AI

Esta guía explica cómo trabajar con IA en un proyecto que usa Cadierno AI.
Aplica para Codex, Claude, Cursor, Gemini CLI y VS Code/GitHub Copilot.

## Idea central

Cadierno es el cerebro externo local del proyecto. Guarda contexto, reglas,
conocimiento y memoria dentro de `.cadierno-ai/`.

El asistente es quien conversa y programa. Cadierno le indica qué leer y cómo
trabajar. La persona responsable conserva siempre la aprobación final.

## Antes de empezar

El líder técnico prepara Cadierno una única vez por proyecto:

```bash
cadierno install /ruta/proyecto
cadierno bootstrap /ruta/proyecto
cadierno adapters enable codex claude cursor gemini vscode copilot --path /ruta/proyecto
```

Si usás el repositorio local en vez de un comando global, reemplazá `cadierno`
por `./.venv/bin/python cli/cadierno.py` desde la raíz de Cadierno AI.

Abrí el editor en la raíz del proyecto, no sólo en un subdirectorio. Por ejemplo:

```bash
cd /ruta/CarpaClick
code .
```

No agregar a Git: `.cadierno-ai/`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, reglas
de Cursor ni `.github/copilot-instructions.md`. Cadierno los excluye localmente.

## Cómo empezar una tarea

Para una tarea con impacto, no pidas código de entrada. Usá este mensaje:

```text
Este proyecto usa Cadierno AI.

Quiero analizar [descripción concreta de la tarea].
Leé primero el contexto y la documentación relevante.
No escribas código todavía.

Entregame:
- flujo actual;
- archivos involucrados;
- riesgos y edge cases;
- propuesta técnica;
- pruebas necesarias;
- microtareas con criterio de cierre.

Detenete al terminar el análisis y esperá mi aprobación.
```

El bridge de Cadierno ya le indica al asistente leer `.cadierno-ai/context.md`.
No hace falta pegar la documentación en cada conversación.

## Cómo aprobar e implementar

Cuando el diseño es correcto, aprobá sólo una parte concreta:

```text
Aprobado.

Implementá únicamente la microtarea 1.
No modifiques módulos fuera del alcance.
No cambies reglas de negocio no aprobadas.
Ejecutá las pruebas afectadas, mostrámelas y detenete.
```

Para una tarea pequeña y de bajo riesgo, podés pedir directamente una
microtarea, pero siempre exigí pruebas y evidencia.

## Flujo recomendado

1. Relevamiento: entender código, estados, integraciones y riesgos.
2. Diseño: acordar alcance, decisiones, datos y pruebas.
3. Microtarea: implementar una unidad verificable.
4. QA y revisión: ejecutar pruebas y revisar cambios.
5. Cierre: mostrar evidencia y esperar aprobación.
6. Aprendizaje: proponer decisiones o lecciones reutilizables.

## Cierre y aprendizaje

Después de una tarea importante:

```bash
cadierno learn propose /ruta/proyecto
cadierno learn apply /ruta/proyecto/.cadierno-ai/learning/proposal-AAAAMMDD-HHMMSS.md --path /ruta/proyecto
```

Cadierno pregunta ítem por ítem. Podés aprobar, editar o rechazar. Nunca debe
incorporar decisiones, deuda técnica o lecciones sin autorización humana.

## Usar documentación actual

Si la tarea requiere una API o librería actual, primero consultá skills:

```bash
cadierno skills suggest "Documentación actual de Laravel" --path /ruta/proyecto
cadierno skills verify context7 --path /ruta/proyecto
```

Instalá una skill sólo después de revisar su origen y aprobarla.

## Errores a evitar

- Implementar sin haber entendido el flujo actual.
- Pedir un refactor general cuando el alcance es puntual.
- Aprobar cambios sin pruebas o sin revisar el diff.
- Guardar contraseñas, tokens o datos sensibles en knowledge o memory.
- Versionar los archivos locales de Cadierno.
- Confundir una sugerencia de la IA con una decisión aprobada.

## Ayuda rápida

- Preparar Cadierno: [QUICKSTART.md](QUICKSTART.md)
- Instalarlo en una máquina: [INSTALL.md](INSTALL.md)
- Consultar todos los comandos: [GUIA_COMANDOS_CLI.md](GUIA_COMANDOS_CLI.md)
- Ver cambios entre versiones: [CHANGELOG.md](CHANGELOG.md)
