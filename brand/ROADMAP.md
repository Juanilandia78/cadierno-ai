# Roadmap - Cadierno AI

> Pensá. Diseñá. Construí. Revisá. Evolucioná.

Este documento describe la evolución planificada de Cadierno AI.

---

# Visión

Cadierno AI busca convertirse en un framework de ingeniería asistida por Inteligencia Artificial.

No pretende reemplazar al desarrollador.

Pretende convertir a cualquier desarrollador en un mejor ingeniero de software.

---

# V1.0 - Core

## Objetivo

Crear la base del framework.

### Incluye

- Filosofía (CADIERNO.md)
- Specialists
- Workflows
- Styles
- Bootstrap
- Knowledge Templates
- Checklists
- Playbooks
- README
- Instalación

Estado: ✅ Completado

---

# V2.1 - Memoria Persistente

## Objetivo

Estabilizar el uso diario con memoria persistente de usuario y workspace.

### Incluye

- Memoria persistente local de usuario (`~/.cadierno-ai`)
- Memoria de workspace (`memory/.cadierno`)
- Perfil editable (nombre, rol, seniority)
- Estilo de comunicación persistente (Argentino/Professional)
- Historial de eventos (install/bootstrap/update/uninstall)
- Comando `cadierno memory` (init/status/style/profile/history)

Estado: ✅ Completado

---

# V2.2 - Intelligent Memory

## Objetivo

Agregar proveedores externos de memoria y automatización avanzada.

### Incluye

- Provider local SQLite (base de memoria persistente)
- MCP local de memoria (save/search/context/status)
- Comando `cadierno assist` para sugerir workflow/specialists
- Integración con Mem0 (opcional, fase siguiente)
- Sistema de resúmenes automáticos (fase siguiente)
- Aprendizaje continuo (fase siguiente)

Estado: 🚧 En implementación

# V3.0 - AI Engineering Platform

## Objetivo

Controlar el framework mediante comandos.

Ejemplos:

/cad bootstrap

/cad audit

/cad feature

/cad review

/cad bugfix

/cad refactor

/cad memory

Estado: 🔮 Futuro

---

# Nuestra prioridad

Antes de agregar nuevas funcionalidades siempre debemos preguntarnos:

- ¿Hace pensar mejor a la IA?
- ¿Hace trabajar mejor a la IA?
- ¿Hace recordar mejor a la IA?

Si la respuesta es "no", probablemente no pertenezca a Cadierno AI.