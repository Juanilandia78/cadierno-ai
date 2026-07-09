# Manual de Uso - Cadierno AI

## Objetivo

Este manual explica como usar Cadierno AI en su version V1 para iniciar trabajo real en un proyecto existente sin cambiar su arquitectura.

Cadierno AI en V1 se centra en cerrar este flujo:

1. Instalar assets base de Cadierno AI en el proyecto.
2. Ejecutar bootstrap para detectar stack y generar conocimiento inicial.
3. Empezar a trabajar con Specialists + Workflows usando el contexto generado.

---

## Alcance de V1

Estado de comandos CLI:

- cadierno install: funcional
- cadierno bootstrap: funcional
- cadierno doctor: funcional
- cadierno uninstall: funcional
- cadierno update: funcional (modo seguro)

Lo que V1 SI resuelve:

- Inicializacion rapida del proyecto con .ai, playbooks y checklists.
- Creacion de knowledge/ y memory/.
- Generacion de AGENTS.md.
- Deteccion automatica de stack base y generacion de knowledge/project.md.
- Generacion inicial de knowledge/architecture.md, knowledge/integrations.md y knowledge/technical-debt.md.

Lo que V1 todavia NO resuelve:

- Analisis profundo de arquitectura, integraciones, deuda tecnica y patrones.
- Actualizacion automatica (update).

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

## Estado de cierre V1

Cadierno AI esta en estado utilizable para V1 si tu objetivo es:

- instalar metodologia en un proyecto existente;
- detectar stack base;
- arrancar trabajo asistido por especialistas con contexto inicial.

No esta cerrado para analisis profundo automatico (eso queda para proxima version).

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