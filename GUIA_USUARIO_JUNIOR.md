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

## Filosofia de uso

Cadierno AI no es una lista de prompts sueltos, es una forma de trabajar. La idea de fondo (el detalle completo queda instalado en `.ai/CADIERNO.md` de cada proyecto) se resume en:

1. **La IA es un companero, no un reemplazo.** Las decisiones importantes son tuyas.
2. **Pensar antes de programar.** Arquitectura primero, implementacion despues.
3. **El contexto manda sobre la tecnologia.** Cada proyecto tiene su propia historia, su propio stack y sus propias convenciones (Laravel clasico, Livewire, multi-tenant con `stancl/tenancy`, lo que sea). Cadierno AI se adapta al proyecto, no al reves.
4. **Simplicidad por sobre complejidad innecesaria.**
5. **Calidad no negociable**: arquitectura, seguridad, legibilidad, mantenibilidad, rendimiento.
6. **Documentacion y pruebas son parte del trabajo**, no un extra.

Por eso tiene sentido ajustar `knowledge/` y los detectores de `bootstrap` a como trabajas vos en el dia a dia (por ejemplo, sumar deteccion de multi-tenancy si tus proyectos usan ese patron). Adaptar la herramienta a tu flujo real es exactamente lo que la filosofia pide, no es "usarla mal".

---

## Idea principal

Cadierno AI funciona como un equipo virtual:

- Specialists (roles)
- Workflows (proceso)
- Playbooks (conocimiento tecnico)
- Knowledge (contexto del proyecto)

Si usas estas cuatro piezas juntas, la IA trabaja con mucha mas calidad.

## Rutina diaria

1. Describí el requerimiento y elegí el workflow.
2. Analizá impacto y dividí en microtareas si hay riesgo.
3. Implementá una microtarea por vez; ejecutá pruebas y guardá evidencia.
4. Validá invariantes, QA y Code Review.
5. Emití un cierre explícito y actualizá knowledge si cambió algo relevante.

Checklist de cierre: caso feliz, errores, rollback, concurrencia cuando aplique,
invariantes, ausencia de estados intermedios, QA, review, evidencia,
documentación y conclusión aprobada o rechazada.

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
- crea CLAUDE.md (solo una linea: `@AGENTS.md`)

Importante: **`.ai/`, `playbooks/` y `checklists/` los crea `install`, no `bootstrap`.** Si corres `bootstrap` sobre un proyecto donde nunca corriste `install`, vas a terminar con `knowledge/` y `memory/` pero sin `.ai/`, `playbooks/` ni `checklists/`. Son dos pasos independientes a proposito: `install` monta el framework (roles, playbooks, checklists), `bootstrap` analiza el codigo. Si ya tenes `knowledge/` porque corriste `bootstrap` solo, podes correr `install` despues sin perder nada (no pisa archivos existentes).

Sobre `AGENTS.md` puntualmente: `install` es quien lo crea por primera vez (a partir de la plantilla). `bootstrap` no genera el archivo completo, pero sí actualiza una sección puntual y delimitada (`## Cadierno / Workspace`, entre marcas `<!-- cadierno:managed:... -->`) con el proyecto detectado y, si corresponde, el workspace de infraestructura compartida. El resto del archivo (los demas encabezados y cualquier nota manual tuya) `bootstrap` nunca lo toca. Si corres `bootstrap` sin haber corrido `install` antes, vas a terminar con un `AGENTS.md` minimo que solo tiene esa seccion — segui recomendando correr `install` primero para tener el archivo completo.

Sobre `CLAUDE.md`: Claude Code (el agente con el que estas hablando ahora mismo) no lee `AGENTS.md` solo, unicamente lee `CLAUDE.md` al arrancar sesion. Por eso `install` te crea un `CLAUDE.md` con la linea `@AGENTS.md`, que es la sintaxis de import de Claude Code: hace que todo el contenido de `AGENTS.md` (y por lo tanto, indirectamente, la filosofia y el contexto de Cadierno) se cargue solo en cada sesion, sin que tengas que pedirlo vos cada vez. Si ya tenias un `CLAUDE.md` propio con contenido distinto, `install`/`update` no lo pisan: te avisan para que agregues la linea `@AGENTS.md` a mano.

---

## 2) Analizar el proyecto (bootstrap)

```bash
python cadierno.py bootstrap /ruta/al/proyecto
```

Que detecta:

- lenguaje (PHP, JavaScript/TypeScript)
- framework (Laravel, Symfony, Zend, React, Vue)
- frontend
- base de datos (MySQL/PostgreSQL, por docker-compose o dependencias)
- infraestructura (Docker, Nginx, Apache)
- arquitectura basica: Controllers, Models, Services, Repositories, Policies, Middleware, Jobs, Events, Livewire, Actions, Mail, Notifications, Providers, View Components
- multi-tenant: si detecta paquetes conocidos (`stancl/tenancy`, `spatie/laravel-multitenancy`, `tenancy/tenancy`, `hyn/multi-tenant`) o estructura tipica (modelo `Tenant`, migraciones separadas, `routes/tenant.php`, `config/tenancy.php`), y si puede determinar la estrategia (por ejemplo, base de datos por tenant)
- integraciones (Mercado Pago, Stripe, AWS, Cloudflare, SMTP, Redis, RabbitMQ, Elasticsearch, Meilisearch, OpenAI, Firebase)
- deuda tecnica inicial (marcadores TODO/FIXME/HACK y controllers muy extensos)

Que genera:

- knowledge/project.md
- knowledge/architecture.md (incluye la seccion Multi-tenant)
- knowledge/integrations.md
- knowledge/technical-debt.md

Nota: la deteccion es heuristica, basada en carpetas y dependencias conocidas. Si tu proyecto usa una convencion de carpetas distinta a las estandar de Laravel (por ejemplo, un modulo propio que no es `app/Services` ni `app/Livewire`), no lo va a reconocer solo; se corrige manualmente en `knowledge/architecture.md` o se agrega el patron al scanner (`cli/core/scanner.py`).

---

## 3) Empezar a trabajar

Cuando ya existe knowledge/, pedi tareas usando workflows.

Ejemplos:

- "Ejecuta workflow Bugfix para este error..."
- "Ejecuta workflow New Feature para este requerimiento..."
- "Ejecuta workflow Maintenance para este ticket..."
- "Ejecuta workflow Explain Code sobre este modulo..."

---

## Preguntas frecuentes

## No me genero un AGENTS.md completo despues de bootstrap

Esperable: `bootstrap` solo escribe/actualiza la sección `## Cadierno / Workspace` de `AGENTS.md` (o crea un `AGENTS.md` minimo con solo esa sección, si el archivo no existia). No genera el resto de los encabezados (Framework, Backend, Convenciones, etc.). Corre `install` sobre el mismo proyecto para tener el archivo completo (no rompe lo que ya tenes en `knowledge/` o `memory/`, ni la sección que ya escribio `bootstrap`).

## Bootstrap no detecta todo lo que tengo en app/

Revisa si esas carpetas tienen nombres estandar (Controllers, Models, Services, Repositories, Policies, Middleware, Jobs, Events, Livewire, Actions, Mail, Notifications, Providers, View Components). Si tu carpeta no matchea ninguno de esos patrones, hoy no se detecta sola. Se puede sumar el patron nuevo en `ARCHITECTURE_DIR_PATTERNS` de `cli/core/scanner.py`.

## Mi proyecto es multi-tenant, con base por tenant, ¿lo detecta?

Si usas `stancl/tenancy`, `spatie/laravel-multitenancy`, `tenancy/tenancy` o `hyn/multi-tenant`, o tenes la estructura tipica (`app/Models/Tenant.php`, `database/migrations/tenant/`, `routes/tenant.php`, `config/tenancy.php`), `bootstrap` lo marca en `knowledge/architecture.md` junto con la estrategia (por ejemplo, "Base de datos por tenant"). Si usas una libreria propia o una convencion distinta, hoy no se detecta sola.

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

Si el proyecto vive dentro de una carpeta mayor con `docker-compose.yml` y
otros servicios (un monorepo), `bootstrap` intenta detectar ese workspace
automaticamente y agrega `knowledge/workspace.md` + `knowledge/infrastructure.md`.
Es opcional: `--infra-root`/`--monorepo-root <ruta>` para indicarlo a mano,
`--no-workspace` para forzar el analisis como proyecto simple. Ver
GUIA_COMANDOS_CLI.md para el detalle.

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
- CLAUDE.md (solo si es el bridge generado por Cadierno, `@AGENTS.md` sin cambios; si le agregaste contenido propio, se conserva)

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

Guardar una observacion (decision, bugfix, etc.):

```bash
python cadierno.py memory save /ruta/proyecto --title "Decision de arquitectura" --content "Usar Service Layer" --type decision --tags arquitectura,backend
```

Buscar observaciones:

```bash
python cadierno.py memory search "Service Layer" /ruta/proyecto --scope workspace --limit 10
```

Ver contexto reciente:

```bash
python cadierno.py memory context /ruta/proyecto --scope workspace --limit 10
```

Sugerencia automática de workflow + specialists:

```bash
python cadierno.py assist "Hay un bug de pagos duplicados" /ruta/proyecto
```

Mem0 no es necesario para esto.

Todo funciona localmente en V2.1.

En V2.2, la persistencia local usa SQLite.

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
- playbooks/laravel/multitenancy.md
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
3. revisar knowledge/project.md y knowledge/architecture.md (incluida la seccion Multi-tenant)
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

## Caso 5: proyecto multi-tenant

Prompt sugerido:

"Este proyecto usa stancl/tenancy con base de datos por tenant. Antes de tocar codigo, confirmame si el cambio afecta la conexion central o la de tenant, y si hace falta correr migraciones en `database/migrations/tenant`."

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
2. Asumir que bootstrap instala el framework completo (eso lo hace install).
3. No leer knowledge antes de implementar.
4. Mezclar varios cambios grandes en una sola tarea.
5. No validar regresiones.
6. No actualizar technical-debt.md cuando descubris riesgos.

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
