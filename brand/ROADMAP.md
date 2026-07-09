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

Consolidar memoria inteligente local y dejar base estable para integraciones futuras.

### Incluye

- Provider local SQLite (base de memoria persistente)
- MCP local de memoria (save/search/context/status)
- Comando `cadierno assist` para sugerir workflow/specialists

Estado: ✅ Completado

### Backlog post V2.2

- Integración con Mem0 (opcional)
- Sistema de resúmenes automáticos
- Aprendizaje continuo

# V3.0 - Supervisor Mode

## Objetivo

Convertir Cadierno AI en un supervisor de trabajo asistido por especialistas.

Cadierno no escribe el codigo como protagonista principal.
Cadierno coordina la idea, hace preguntas cuando falta contexto, delega la ejecucion a especialistas/agentes y te devuelve una revision clara para aprobar o corregir.

### Principios

- Vos seguís siendo el dueño de la idea y de la decision final.
- Los especialistas escriben y modifican codigo.
- Cadierno organiza la tarea, guarda contexto y revisa resultados.
- Si falta claridad, Cadierno pregunta antes de avanzar.

### Incluye

- Modo idea a tarea.
- Modo preguntas antes de ejecutar.
- Delegacion a especialistas segun el tipo de trabajo.
- Modo revision de codigo y riesgos.
- Aprobacion final del usuario antes de cerrar cambios.
- Integracion mas formal con agentes externos que escriben codigo.

### Fuera de alcance

- Programacion automatica completa sin supervision.
- Reemplazar al agente principal de codigo del editor.
- Convertir Cadierno en una plataforma generalista tipo marketplace.

Estado: 📌 Backlog

---

# Nuestra prioridad

Antes de agregar nuevas funcionalidades siempre debemos preguntarnos:

- ¿Hace pensar mejor a la IA?
- ¿Hace trabajar mejor a la IA?
- ¿Hace recordar mejor a la IA?

Si la respuesta es "no", probablemente no pertenezca a Cadierno AI.