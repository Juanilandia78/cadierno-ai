# Guía práctica para empezar con Cadierno AI V3

## Qué es Cadierno

Cadierno no es un agente que decide por vos. Es el sistema local que le da a tu
asistente reglas, contexto y memoria para que trabaje de forma profesional.

La filosofía es simple:

- entender el problema antes de tocar código;
- separar análisis, diseño, implementación y revisión;
- hacer una microtarea por vez;
- probar lo afectado;
- mantener la aprobación humana para decisiones importantes.

## Primera vez en un proyecto

Seguí [QUICKSTART.md](QUICKSTART.md). Los tres comandos centrales son:

```bash
cadierno install /ruta/proyecto
cadierno bootstrap /ruta/proyecto
cadierno adapters enable codex claude cursor gemini vscode copilot --path /ruta/proyecto
```

Si ejecutás el CLI desde este repositorio, reemplazá `cadierno` por
`./.venv/bin/python cli/cadierno.py`.

## Cómo pedir una tarea bien

En lugar de “hacé el pago”, usá una secuencia explícita:

1. “Relevá el flujo actual. No escribas código.”
2. “Proponé diseño, riesgos, pruebas y criterio de cierre.”
3. “Aprobado. Implementá sólo la microtarea X.”
4. “Ejecutá pruebas, mostrámelas y detenete.”

Esto reduce cambios fuera de alcance y mantiene evidencia verificable.

## Qué archivos mira la IA

El adapter carga un bridge local. Ese bridge apunta a:

```text
.cadierno-ai/context.md
```

El contexto indica cuándo leer `knowledge/project.md`, `architecture.md`,
`integrations.md` y `technical-debt.md`. No hace falta pegar esos textos en
cada conversación.

## Qué hacer después de una tarea

Si hubo una decisión reutilizable, pedí una propuesta de aprendizaje:

```bash
cadierno learn propose /ruta/proyecto
cadierno learn apply /ruta/proyecto/.cadierno-ai/learning/proposal-AAAAMMDD-HHMMSS.md --path /ruta/proyecto
```

Cadierno te presenta cada ítem para aprobar, editar o rechazar. Nunca actualiza
conocimiento por sí solo.

## Errores comunes

- Pedir implementación antes de aprobar el diseño de una tarea riesgosa.
- Versionar `.cadierno-ai` o los bridges de asistentes.
- Guardar secretos en `memory` o `knowledge`.
- Suponer que una detección de `bootstrap` reemplaza la revisión humana.
- Aceptar una propuesta de aprendizaje sin revisar su evidencia.

## Ayuda

- [MANUAL_DE_USO.md](MANUAL_DE_USO.md): flujo real completo.
- [GUIA_COMANDOS_CLI.md](GUIA_COMANDOS_CLI.md): todos los comandos.
- `cadierno --help`: ayuda integrada.
