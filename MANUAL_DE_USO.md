# Manual de Uso - Cadierno AI

## Objetivo

Este manual explica como usar Cadierno AI en su version V2.1 para trabajo diario real en proyectos existentes sin cambiar arquitectura innecesariamente.

Cadierno AI en V2.1 se centra en cerrar este flujo:

1. Instalar assets base de Cadierno AI en el proyecto.
2. Ejecutar bootstrap para detectar stack y generar conocimiento inicial.
3. Empezar a trabajar con Specialists + Workflows usando el contexto generado.

---

## Alcance de V2.1

Estado de comandos CLI:

- cadierno install: funcional
- cadierno bootstrap: funcional
- cadierno doctor: funcional
- cadierno uninstall: funcional
- cadierno update: funcional (modo seguro)
- cadierno memory: funcional
- cadierno assist: funcional

Lo que V2.1 SI resuelve:

- Inicializacion rapida del proyecto con .ai, playbooks y checklists.
- Creacion de knowledge/ y memory/.
- Generacion de AGENTS.md.
- Deteccion automatica de stack base y generacion de knowledge/project.md.
- Generacion inicial de knowledge/architecture.md, knowledge/integrations.md y knowledge/technical-debt.md.
- Memoria persistente de usuario y workspace.
- Perfil de desarrollador editable por CLI.
- Historial de eventos entre proyectos.

Lo que V2.1 todavia NO resuelve:

- Integración con Mem0/MCP (opcional y futuro).
- Automatización completa de specialists/workflows.

---

## Avances de V2.2

Actualmente Cadierno incluye mejoras V2.2 sobre memoria:

- Backend de memoria local en SQLite.
- MCP local (stdio) para herramientas de memoria en `cli/mcp_memory_server.py`.
- Operaciones de observaciones: save/search/context.
- Sugerencia automática de workflow/specialists con `cadierno assist`.

---

## Requisitos

- Python 3.10+.
- Acceso al repositorio cadierno-ai.
- Proyecto destino con permisos de lectura/escritura.

---

## Instalacion de Cadierno AI en un proyecto

Desde la carpeta cli de cadierno-ai:

```bash
python cadierno.py install /ruta/al/proyecto
```

Resultado esperado:

- Copia: .ai/, playbooks/, checklists/
- Crea: knowledge/, memory/
- Genera: AGENTS.md

Notas:

- No sobrescribe carpetas que ya existen.
- Crea archivos base solo si no existen.

---

## Bootstrap del proyecto

Ejecutar:

```bash
python cadierno.py bootstrap /ruta/al/proyecto
```

Bootstrap detecta automaticamente archivos clave (si existen):

- composer.json
- package.json
- docker-compose.yml
- Dockerfile
- README.md

Con esto intenta identificar:

- lenguaje
- framework
- frontend
- base de datos
- infraestructura

Y genera:

- knowledge/project.md
- knowledge/architecture.md
- knowledge/integrations.md
- knowledge/technical-debt.md

---

## Memoria persistente (V2.1)

Cadierno AI guarda memoria en dos niveles:

- Usuario global: ~/.cadierno-ai
- Workspace/proyecto: /ruta/proyecto/memory/.cadierno

Comandos principales:

```bash
python cadierno.py memory init /ruta/al/proyecto
python cadierno.py memory status /ruta/al/proyecto
python cadierno.py memory style argentino /ruta/al/proyecto --scope workspace
python cadierno.py memory profile /ruta/al/proyecto --name "Tu Nombre" --role "Software Engineer" --seniority "Senior" --scope user
python cadierno.py memory history /ruta/al/proyecto --scope workspace --limit 20
python cadierno.py memory save /ruta/al/proyecto --title "Decisión" --content "Usar service layer" --type decision --tags arquitectura,backend
python cadierno.py memory search "service layer" /ruta/al/proyecto --scope workspace --limit 10
python cadierno.py memory context /ruta/al/proyecto --scope workspace --limit 10
python cadierno.py assist "Hay un bug en pagos duplicados" /ruta/al/proyecto
```

El estilo de comunicación efectivo se resuelve por prioridad:

1. workspace
2. user
3. professional por defecto

---

## Uso recomendado diario

Flujo de trabajo sugerido por sprint:

1. Ejecutar install (solo una vez por proyecto).
2. Ejecutar bootstrap al inicio o cuando el stack cambie.
3. Pedir tareas al asistente usando Workflows y Specialists.
4. Mantener knowledge/ actualizado para mejorar decisiones de IA.

Prompts utiles:

- "Ejecuta el workflow New Feature para este requerimiento..."
- "Ejecuta el workflow Bugfix sobre este error..."
- "Actua como Code Reviewer sobre este PR..."
- "Actualiza knowledge/project.md si cambie infraestructura..."

---

## Verificacion rapida

Checklist minimo despues de bootstrap:

1. Existe knowledge/project.md.
2. El stack detectado coincide con el proyecto real.
3. AGENTS.md existe en la raiz del proyecto.
4. .ai/, playbooks/ y checklists/ estan disponibles.

Si algo no coincide:

1. Corregir manualmente knowledge/project.md.
2. Volver a ejecutar bootstrap.
3. Reportar ajuste para mejorar reglas de deteccion.

---

## Troubleshooting

Caso: "No detectado" en varias secciones.

- Verificar que los archivos clave existan en el proyecto.
- Verificar que los archivos JSON sean validos.
- Reintentar bootstrap apuntando a la carpeta raiz correcta.

Caso: install no copia una carpeta.

- Verificar permisos de escritura en proyecto destino.
- Verificar que la carpeta fuente exista en cadierno-ai.

Caso: salida inesperada en bootstrap.

- Revisar knowledge/project.md y archivos detectados en Observaciones.
- Ajustar reglas de scanner en una iteracion posterior.

---

## Estado de cierre V2.1

Cadierno AI esta en estado utilizable para V2.1 si tu objetivo es:

- instalar metodologia en un proyecto existente;
- detectar stack base y generar knowledge;
- persistir perfil/estilo/historial en uso diario.

Mem0 no es obligatorio para V2.1.

Es opcional para V2.2 cuando quieras memoria externalizada y aprendizaje cross-device.

---

## Mejoras recomendadas (sin sobrearquitectura)

Prioridad alta:

1. Completar update para sincronizacion segura de assets sin romper customizaciones locales.
2. Extender bootstrap para detectar arquitectura e integraciones en knowledge/architecture.md e integrations.md.
3. Agregar tests unitarios del scanner para casos Laravel, Symfony, Zend, PHP puro, Vue y React.

Prioridad media:

1. Mejorar deteccion de frontend (Livewire, Blade, Inertia, Alpine).
2. Mejorar deteccion de bases (SQLite, SQL Server, MariaDB).
3. Agregar bandera --dry-run en bootstrap para ver deteccion sin escribir archivos.

Prioridad baja:

1. Exportar reporte bootstrap en JSON para integraciones externas.
2. Mostrar score de confianza por cada deteccion.