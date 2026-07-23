# Guía de comandos CLI — Cadierno AI

Ejecutá los ejemplos desde `cadierno-ai/cli` con `python3 cadierno.py` (o con
el Python de tu entorno virtual). Reemplazá `/ruta/proyecto` por la raíz del
proyecto destino.

## Flujo inicial recomendado

```bash
python3 cadierno.py install /ruta/proyecto
python3 cadierno.py bootstrap /ruta/proyecto
python3 cadierno.py memory init /ruta/proyecto
```

`install` instala los assets; `bootstrap` analiza el código; `memory init`
prepara memoria local. Para un proyecto vacío, creá primero el stack base y
luego ejecutá `bootstrap` nuevamente.

## Comandos de proyecto

### `install [path]`

Instala `.ai/`, playbooks, checklists, `knowledge/`, `memory/`, `AGENTS.md` y
`CLAUDE.md` si no existen. No debería pisar archivos locales.

```bash
python3 cadierno.py install /ruta/proyecto
```

### `bootstrap [path]`

Detecta stack, arquitectura, integraciones y deuda técnica; genera o completa
los archivos de `knowledge/`.

```bash
python3 cadierno.py bootstrap /ruta/proyecto
```

#### Proyectos dentro de un workspace de infraestructura compartida

> **Importante:** este "workspace" (docker-compose, servicios hermanos, nginx,
> redes) no tiene relación con el `--scope workspace` de `memory` (que es la
> memoria persistente por-proyecto, ver más abajo). Son dos conceptos
> distintos que comparten nombre por casualidad histórica.

Si tu proyecto vive dentro de una carpeta mayor con `docker-compose.yml`,
otros servicios y/o `nginx/` (por ejemplo `workspace/mi-proyecto/`), `bootstrap`
puede detectar esa infraestructura compartida además de tu proyecto:

```bash
# Detección automática: busca hacia arriba docker-compose.yml/compose.yml
# (o sus variantes .yaml) hasta encontrar evidencia fuerte, sin cruzar $HOME,
# la raíz del filesystem, ni un repo git ajeno.
python3 cadierno.py bootstrap /ruta/workspace/mi-proyecto

# Workspace explícito (--infra-root y --monorepo-root son alias del mismo flag)
python3 cadierno.py bootstrap /ruta/workspace/mi-proyecto --infra-root /ruta/workspace
python3 cadierno.py bootstrap /ruta/workspace/mi-proyecto --monorepo-root /ruta/workspace

# Forzar análisis como proyecto simple, aunque exista un workspace detectable
python3 cadierno.py bootstrap /ruta/workspace/mi-proyecto --no-workspace
```

Si no se detecta ningún workspace válido, `bootstrap` sigue funcionando
exactamente igual que en un proyecto simple (esto nunca es obligatorio). Cuando
sí detecta uno, además de los archivos habituales genera:

- `knowledge/workspace.md`: panorama del workspace (raíz detectada, evidencia,
  proyectos hermanos, qué servicio Docker corresponde a este proyecto).
- `knowledge/infrastructure.md`: detalle técnico (servicios, redes, volúmenes,
  puertos, healthchecks, reverse proxy/Nginx, nombres de variables de entorno
  del workspace — nunca sus valores).

`bootstrap` nunca sobreescribe un archivo de `knowledge/` que hayas editado a
mano: si detecta una diferencia respecto a lo último que generó, conserva tu
versión y escribe la propuesta nueva al lado, como `archivo.md.cadierno-new`,
para que la fusiones manualmente. Lo mismo aplica a la sección `## Cadierno /
Workspace` de `AGENTS.md`: solo se actualiza el contenido entre las marcas
`<!-- cadierno:managed:start/end:workspace -->`; cualquier otra parte del
archivo (incluidas tus propias notas) queda intacta.

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
`knowledge/` y `memory/`.

```bash
python3 cadierno.py uninstall /ruta/proyecto
python3 cadierno.py uninstall /ruta/proyecto --purge
```

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
python3 cadierno.py memory --help
python3 cadierno.py memory save --help
```
