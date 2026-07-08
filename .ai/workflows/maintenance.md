# Workflow - Maintenance

## Objetivo

Resolver tareas de mantenimiento sobre proyectos existentes de forma segura.

Este Workflow está pensado para:

- corrección de bugs;
- pequeñas funcionalidades;
- refactors controlados;
- mantenimiento evolutivo;
- sistemas legacy.

Nunca comenzar implementando.

Primero comprender.

---

# Paso 1 - Comprender el requerimiento

Analizar el pedido del usuario.

Responder:

- ¿Cuál es el problema?
- ¿Cuál es el resultado esperado?
- ¿Qué información falta?

Si existen dudas:

detenerse y preguntar.

---

# Paso 2 - Comprender el proyecto

Leer:

- knowledge/project.md
- knowledge/architecture.md
- knowledge/decisions.md

Si no existen:

ejecutar Bootstrap.

---

# Paso 3 - Localizar el código

Buscar:

- Controllers
- Services
- Models
- Componentes
- APIs
- Rutas
- Consultas SQL

Explicar dónde se encuentra la lógica relacionada.

---

# Paso 4 - Analizar el impacto

Responder:

- ¿Qué módulos podrían verse afectados?
- ¿Qué riesgos existen?
- ¿Puede romper compatibilidad?
- ¿Existen efectos secundarios?

---

# Paso 5 - Diseñar la solución

Proponer una estrategia.

Explicar:

- qué archivos serán modificados;
- por qué;
- alternativas descartadas.

Esperar aprobación cuando el cambio sea significativo.

---

# Paso 6 - Implementar

Delegar al Specialist correspondiente.

Respetar:

- arquitectura;
- convenciones;
- estilo existente.

Nunca reescribir código innecesariamente.

---

# Paso 7 - Validación

Delegar a QA.

Verificar:

- caso feliz;
- casos de error;
- permisos;
- regresiones.

---

# Paso 8 - Revisión

Delegar al Code Reviewer.

Analizar:

- calidad;
- mantenibilidad;
- seguridad;
- performance.

---

# Paso 9 - Documentación

Si el cambio modifica el comportamiento del sistema:

actualizar documentación.

---

# Resultado esperado

Toda tarea de mantenimiento debe finalizar con:

- problema resuelto;
- riesgos identificados;
- pruebas realizadas;
- documentación actualizada cuando corresponda.