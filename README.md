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

Cadierno funciona como el cerebro externo local del proyecto: instala su
contexto en `.cadierno-ai/`, mientras que trabajás diariamente con el asistente
que prefieras (Codex, Claude o Cursor). Sus bridges y su memoria son locales y
se excluyen del repositorio del proyecto.

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

Bootstrap utiliza estos templates para crear:

- knowledge/project.md
- knowledge/architecture.md
- knowledge/decisions.md
- knowledge/patterns.md
- knowledge/integrations.md
- knowledge/technical-debt.md
- knowledge/developer.md

---

## Memory

Cadierno AI dispone de una memoria propia para almacenar preferencias, aprendizajes y contexto del desarrollador.

Esta información es independiente de cada proyecto.

## Contexto, adapters y aprendizaje

- `context.md` reúne el mapa operativo que los asistentes deben leer primero.
- Los adapters habilitan Codex, Claude y Cursor sin modificar archivos
  versionados del proyecto.
- Las skills son extensiones opcionales, verifican su origen oficial y requieren
  instalación explícita.
- El aprendizaje es supervisado: Cadierno propone decisiones, deuda o lecciones
  y una persona aprueba cada ítem antes de persistirlo.

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

- Stack local unificado en `.cadierno-ai/`
- Contexto operativo generado y adapters para Codex, Claude y Cursor
- Catálogo de skills opcionales y aprendizaje supervisado
- Console compatible con terminales modernas y modo plano para CI/logs
- Próximo: validación de fuentes, más integraciones y automatización guiada

Nota estado actual:

- V2.2 incluye memoria persistente en SQLite, comandos `memory` y servidor MCP-like local.
- V3 está en evolución; consultá la guía de comandos para el alcance operativo actual.

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
