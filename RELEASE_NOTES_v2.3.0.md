# Cadierno AI v2.3.0

Version orientada a proyectos que viven dentro de un workspace de infraestructura
compartida (docker-compose, servicios hermanos, nginx), manteniendo intacto el
flujo simple de un proyecto aislado.

## Highlights

- Soporte de **workspace de infraestructura compartida**, opcional y retrocompatible:
  - `cadierno bootstrap` detecta automaticamente un workspace superior (evidencia
    fuerte: `docker-compose.yml`/`.yaml`, `compose.yml`/`.yaml`; nunca cruza `$HOME`,
    la raiz del filesystem, ni un repositorio git ajeno).
  - Nuevos flags `--infra-root`/`--monorepo-root` (alias) y `--no-workspace` en
    `bootstrap`, `install` y `update`.
  - Nuevos `knowledge/workspace.md` y `knowledge/infrastructure.md`: contexto
    GLOBAL del workspace, separado del contexto local del proyecto.
  - Identifica que servicio Docker corresponde al proyecto (por `build.context`
    o bind-mount, con heuristica de nombre de baja confianza como respaldo;
    nunca inventa un match sin evidencia), redes, volumenes, healthchecks,
    reverse proxy/Nginx y proyectos hermanos.
  - Parseo de `docker-compose.yml` via PyYAML si esta disponible (dependencia
    opcional, con fallback heuristico sin PyYAML).
  - `AGENTS.md` ahora tiene una seccion gestionada (`## Cadierno / Workspace`)
    que `bootstrap` actualiza sin tocar el resto del archivo ni contenido
    manual del equipo.
- Mecanismo de hash para `knowledge/*.md` generados por `bootstrap`: si el
  archivo fue editado a mano desde la ultima generacion, no se sobreescribe
  (se conserva el original y se escribe `archivo.md.cadierno-new` al lado).
  Corrige un comportamiento previo donde `bootstrap` sobreescribia
  `knowledge/*.md` sin resguardo alguno.
- `install`, `bootstrap` y `update` gestionan un bloque en el `.gitignore` del
  proyecto para que `.ai/`, `playbooks/`, `checklists/`, `knowledge/`, `memory/`,
  `AGENTS.md` y `CLAUDE.md` nunca terminen commiteados al repo del proyecto
  (se reinstalan con `cadierno install` + `cadierno bootstrap` en cada checkout
  que los necesite). No toca ninguna otra regla que el `.gitignore` ya tuviera.
- Endurecimiento de seguridad: ningun archivo `.env` (ni variantes, p. ej.
  `.env.local`, `algo.env`) se vuelca nunca como contenido crudo en ningun
  buffer de analisis ni archivo generado; solo se registran nombres de
  variable, nunca valores.
- Suite de tests ampliada a 60 casos (deteccion de workspace, parseo de
  compose, extraccion segura de variables de entorno, secciones gestionadas,
  gitignore gestionado, e integracion completa de `bootstrap` con workspace).

## Estado del Proyecto

- V2.3: soporte de workspace de infraestructura compartida completado,
  retrocompatible con proyectos simples.
- V3: sigue en backlog para integraciones avanzadas y automatizacion ampliada.

## Notas Operativas

- El soporte de workspace es opcional: si no se detecta ninguno, `bootstrap`
  sigue funcionando exactamente igual que en un proyecto aislado.
- PyYAML es opcional: sin el, la deteccion de docker-compose usa un modo
  heuristico mas limitado (nombres de servicio, sin el resto del detalle).
  Los instaladores intentan instalarlo, pero no es obligatorio.
- No confundir el workspace de infraestructura compartida con
  `memory --scope workspace` (memoria persistente por-proyecto): son dos
  conceptos distintos que comparten nombre por casualidad historica.
