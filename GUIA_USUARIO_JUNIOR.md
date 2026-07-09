# Guia de Usuario Junior - Cadierno AI

## Para que sirve Cadierno AI

Cadierno AI es un framework de trabajo con IA para desarrollar mejor software.

No reemplaza al desarrollador.

Te ayuda a trabajar con metodo en:

- bugs;
- nuevas funcionalidades;
- mantenimiento;
- sistemas legacy;
- documentacion tecnica.

Tu rol sigue siendo decidir.

Cadierno AI te ordena el proceso.

---

## Idea principal

Cadierno AI funciona como un equipo virtual:

- Specialists (roles)
- Workflows (proceso)
- Playbooks (conocimiento tecnico)
- Knowledge (contexto del proyecto)

Si usas estas cuatro piezas juntas, la IA trabaja con mucha mas calidad.

---

## Instalacion y primeros pasos

## 1) Instalar Cadierno AI en un proyecto

Desde la carpeta cli de cadierno-ai:

```bash
python cadierno.py install /ruta/al/proyecto
```

Que hace:

- copia .ai/
- copia playbooks/
- copia checklists/
- crea knowledge/
- crea memory/
- crea AGENTS.md

---

## 2) Analizar el proyecto (bootstrap)

```bash
python cadierno.py bootstrap /ruta/al/proyecto
```

Que detecta:

- lenguaje
- framework
- frontend
- base de datos
- infraestructura
- arquitectura basica
- integraciones
- deuda tecnica inicial

Que genera:

- knowledge/project.md
- knowledge/architecture.md
- knowledge/integrations.md
- knowledge/technical-debt.md

---

## 3) Empezar a trabajar

Cuando ya existe knowledge/, pedi tareas usando workflows.

Ejemplos:

- "Ejecuta workflow Bugfix para este error..."
- "Ejecuta workflow New Feature para este requerimiento..."
- "Ejecuta workflow Maintenance para este ticket..."
- "Ejecuta workflow Explain Code sobre este modulo..."

---

## Comandos CLI (todos)

## cadierno install

Instala Cadierno AI en un proyecto.

```bash
python cadierno.py install /ruta/proyecto
```

---

## cadierno bootstrap

Analiza proyecto y genera archivos de conocimiento.

```bash
python cadierno.py bootstrap /ruta/proyecto
```

---

## cadierno update

Actualiza assets de Cadierno sin romper customizaciones locales.

```bash
python cadierno.py update /ruta/proyecto
```

Modo seguro:

- copia archivos nuevos;
- no pisa archivos distintos del proyecto;
- reporta conflictos preservados.

---

## cadierno uninstall

Desinstala Cadierno del proyecto.

```bash
python cadierno.py uninstall /ruta/proyecto
```

Elimina:

- .ai/
- playbooks/
- checklists/
- AGENTS.md

Con purge total:

```bash
python cadierno.py uninstall /ruta/proyecto --purge
```

Tambien elimina:

- knowledge/
- memory/

---

## cadierno doctor

Muestra estado general del framework.

```bash
python cadierno.py doctor
```

---

## cadierno memory

Gestiona memoria persistente de usuario/workspace.

Inicializar memoria:

```bash
python cadierno.py memory init /ruta/proyecto
```

Ver estado:

```bash
python cadierno.py memory status /ruta/proyecto
```

Configurar estilo Argentino o Professional:

```bash
python cadierno.py memory style argentino /ruta/proyecto --scope workspace
python cadierno.py memory style professional /ruta/proyecto --scope user
```

Configurar perfil:

```bash
python cadierno.py memory profile /ruta/proyecto --name "Tu Nombre" --role "Software Engineer" --seniority "Senior" --scope user
```

Ver historial:

```bash
python cadierno.py memory history /ruta/proyecto --scope workspace --limit 20
```

Mem0 no es necesario para esto.

Todo funciona localmente en V2.1.

---

## Glosario simple (fundamental)

## Que es un Workflow

Es el proceso paso a paso para resolver un tipo de trabajo.

Ejemplos:

- bugfix.md
- new-feature.md
- maintenance.md
- legacy.md
- explain-code.md

Piensalo como "receta de trabajo".

---

## Que es un Playbook

Es conocimiento tecnico reutilizable para un tema concreto.

Ejemplos:

- playbooks/laravel/service-layer.md
- playbooks/mysql/indexes.md
- playbooks/git/release.md
- playbooks/mercadopago/refunds.md

Piensalo como "biblioteca de buenas practicas".

---

## Que es un Specialist

Es un rol tecnico virtual (arquitecto, backend, dba, qa, reviewer, etc.).

Cada specialist tiene foco y limites claros.

---

## Que es Knowledge

Es el contexto vivo del proyecto, para que la IA no improvise.

Si knowledge esta bien, las respuestas mejoran mucho.

---

## Como trabajar en el dia a dia (rutina recomendada)

## Al entrar a un proyecto nuevo

1. install
2. bootstrap
3. revisar knowledge/project.md
4. corregir manualmente objetivo/dominio si hace falta

---

## Al empezar una tarea

1. describir requerimiento
2. elegir workflow correcto
3. pedir analisis de impacto antes de tocar codigo
4. implementar
5. validar (QA + reviewer)
6. actualizar knowledge si cambio algo importante

---

## Cada semana

1. correr bootstrap si cambio stack o infra
2. revisar technical-debt.md
3. priorizar 1 o 2 deudas tecnicas reales

---

## Casos reales de uso

## Caso 1: tengo un bug

Prompt sugerido:

"Usa workflow Bugfix. Problema: al confirmar reserva se duplica el cobro si refrescan la pagina. Quiero causa raiz, fix seguro, riesgos y pruebas."

Salida esperada:

- causa raiz
- archivos afectados
- fix propuesto
- casos de prueba
- riesgos de regresion

---

## Caso 2: nueva funcionalidad chica

Prompt sugerido:

"Usa workflow New Feature. Necesito filtro por fecha en listado de reservas, sin romper paginado actual."

Salida esperada:

- diseno tecnico
- impacto en backend/frontend
- cambios por archivo
- pruebas minimas

---

## Caso 3: proyecto viejo y riesgoso

Prompt sugerido:

"Usa workflow Legacy para agregar validacion sin cambiar comportamiento existente. Priorizo compatibilidad y rollback facil."

---

## Caso 4: no entiendo un modulo

Prompt sugerido:

"Usa workflow Explain Code sobre este controlador. Explica flujo feliz, errores, side effects y riesgos."

---

## Estilo de comunicacion (Argentino o Profesional)

Cadierno AI tiene 2 estilos definidos:

- .ai/styles/argentino.md
- .ai/styles/professional.md

## Para estilo argentino

Pedi al inicio:

"Desde ahora usa estilo Argentino de .ai/styles/argentino.md"

## Para estilo profesional

Pedi al inicio:

"Desde ahora usa estilo Profesional de .ai/styles/professional.md"

## Para dejarlo fijo por proyecto

Recomendado en V2.1:

```bash
python cadierno.py memory style argentino /ruta/proyecto --scope workspace
```

O profesional:

```bash
python cadierno.py memory style professional /ruta/proyecto --scope workspace
```

---

## Recomendacion por contexto laboral

## Employee Mode (empresa)

Enfocar en:

- maintenance
- bugfix
- explain-code
- cambios chicos y seguros

Prompt base:

"Modo Employee: prioriza compatibilidad, bajo riesgo y documentacion minima."

## Freelance Mode

Enfocar en:

- new-feature
- maintenance
- bootstrap frecuente
- deploy y documentacion operativa

Prompt base:

"Modo Freelance: prioriza velocidad con calidad, arquitectura clara y salida deployable."

## Founder Mode

Enfocar en:

- new-project
- roadmap tecnico
- decisiones de arquitectura
- time-to-market

Prompt base:

"Modo Founder: prioriza MVP rapido, decisiones claras y escalabilidad progresiva."

---

## Errores comunes y como evitarlos

1. Pedir codigo sin bootstrap previo.
2. No leer knowledge antes de implementar.
3. Mezclar varios cambios grandes en una sola tarea.
4. No validar regresiones.
5. No actualizar technical-debt.md cuando descubris riesgos.

---

## Checklist rapido antes de cerrar una tarea

1. El requerimiento quedo cumplido.
2. No rompiste compatibilidad.
3. Probaste caso feliz y error.
4. Identificaste riesgos.
5. Documentaste cambios relevantes.

---

## Flujo minimo para usar Cadierno todos los dias

1. install (solo una vez por proyecto)
2. bootstrap
3. elegir workflow por tipo de tarea
4. implementar con specialists
5. validar
6. actualizar knowledge

Si haces esto de forma consistente, Cadierno AI se vuelve una herramienta real de trabajo diario y no solo un set de prompts.
