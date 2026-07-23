# Cadierno AI

Documentación de comandos: [GUIA_COMANDOS_CLI.md](GUIA_COMANDOS_CLI.md).

> **Pensá. Diseñá. Construí. Revisá. Evolucioná.**

Cadierno AI es un framework de Ingeniería de Software Asistida por Inteligencia Artificial.

Su objetivo es transformar asistentes como Claude Code, GitHub Copilot, Cursor o ChatGPT en un verdadero equipo de especialistas capaz de comprender proyectos, diseñar soluciones, desarrollar software, documentar cambios y revisar la calidad del código.

---

# Filosofía

La IA no reemplaza al desarrollador.

Lo potencia.

Cadierno AI propone una metodología donde cada especialista tiene una responsabilidad clara y cada tarea sigue un proceso definido.

El criterio humano siempre tiene la última palabra.

---

# Componentes

## Specialists

Equipo de especialistas que colaboran entre sí.

- Architect
- Backend Engineer
- Database Specialist
- DevOps Specialist
- QA Engineer
- Code Reviewer
- Documentation Specialist

---

## Workflows

Procesos reutilizables para resolver distintos tipos de trabajo.

Actualmente incluye:

- Bootstrap
- Maintenance
- Legacy
- Explain Code
- New Feature
- Bug Fix
- Refactor
- Audit
- New Project

---

## Playbooks

Biblioteca de conocimiento técnico reutilizable.

Incluye:

- Laravel
- Livewire
- Vue
- Docker
- MySQL
- Git
- Mercado Pago
- Testing

---

## Templates

Plantillas utilizadas para generar automáticamente la documentación de cada proyecto.

`bootstrap` genera o actualiza, en `knowledge/` del proyecto:

- `project.md`, `architecture.md`, `integrations.md`, `technical-debt.md`: contexto
  local de ESE proyecto (siempre se generan).
- `workspace.md`, `infrastructure.md`: contexto GLOBAL del workspace de
  infraestructura compartida (docker-compose, servicios hermanos, nginx),
  solo cuando `bootstrap` detecta o recibe uno — ver GUIA_COMANDOS_CLI.md.

`install` además crea `decisions.md` como stub editable a mano (convenciones y
decisiones del equipo); `bootstrap` nunca lo sobreescribe.

---

## Workspace (infraestructura compartida)

Cuando un proyecto vive dentro de una carpeta mayor con `docker-compose.yml`,
otros servicios y/o un reverse proxy (Nginx), `bootstrap` puede detectar esa
infraestructura compartida —de forma automática o indicándola explícitamente
con `--infra-root`/`--monorepo-root`— sin dejar de analizar el proyecto en sí.
Es opcional: un proyecto aislado sigue funcionando exactamente igual que
siempre. Ver la sección correspondiente en GUIA_COMANDOS_CLI.md.

> No confundir con `memory --scope workspace`: ese es un concepto distinto,
> la memoria persistente por-proyecto (ver sección "Memory" más abajo).

---

## Memory

Cadierno AI dispone de una memoria propia para almacenar preferencias, aprendizajes y contexto del desarrollador.

Esta información es independiente de cada proyecto.

---

## Styles

Permite adaptar el estilo de comunicación.

Actualmente:

- Profesional
- Argentino

---

# Roadmap

## V1

- Core Framework
- Specialists
- Workflows
- Playbooks
- Templates
- Bootstrap

## V2

- Workspace
- Persistent Memory
- Bootstrap Inteligente
- Project Scanner
- Maintenance Workflow
- Legacy Workflow
- Explain Code

## V3

- MCP
- Automatización
- Console
- Marketplace
- Integración con Mem0

Nota estado actual:

- V2.2 ya incluye memoria persistente en SQLite, comandos `memory` y servidor MCP-like local.
- V2.3 agrega soporte de workspace de **infraestructura compartida** (docker-compose,
  servicios hermanos, nginx) para proyectos dentro de un monorepo — ver `bootstrap
  --infra-root`. El ítem "Workspace" listado en V2 se refería originalmente a este
  tipo de soporte de forma genérica; el de memoria persistente por-proyecto
  (`memory --scope workspace`) es un concepto no relacionado, ya cubierto desde V2.1/V2.2.
- V3 queda orientado a integraciones avanzadas y automatizacion ampliada.

---

# Instalación

Ver:

INSTALL.md

Instalacion rapida:

```bash
git clone https://github.com/TU_USUARIO/cadierno-ai.git
cd cadierno-ai
./install/install_cli.sh
```

Cadierno usa SQLite via `sqlite3` del standard library de Python, sin instalacion extra.

---

# Licencia

MIT
