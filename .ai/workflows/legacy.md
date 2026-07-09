# Workflow - Legacy

## Objetivo

Trabajar sobre sistemas legacy minimizando riesgo de regresiones.

Este workflow aplica cuando:

- el código tiene alta antigüedad;
- hay baja cobertura de tests;
- existen dependencias viejas o acopladas;
- no hay documentación suficiente.

Nunca iniciar con cambios grandes.

Primero estabilizar.

---

## Paso 1 - Entender el alcance

Definir con precisión:

- qué se necesita corregir o mejorar;
- qué comportamiento actual no puede romperse;
- qué partes están fuera de alcance.

---

## Paso 2 - Levantar contexto mínimo

Leer:

- knowledge/project.md
- knowledge/architecture.md
- knowledge/technical-debt.md

Si falta contexto:

ejecutar Bootstrap.

---

## Paso 3 - Trazar flujo actual

Identificar:

- punto de entrada;
- dependencias directas;
- efectos secundarios;
- datos afectados.

Documentar flujo antes de cambiar código.

---

## Paso 4 - Diseñar cambio incremental

Planificar un cambio pequeño y reversible.

Priorizar:

- compatibilidad;
- bajo impacto;
- facilidad de rollback.

---

## Paso 5 - Implementar con protección

Aplicar cambios acotados.

Agregar validaciones defensivas cuando corresponda.

Evitar refactors masivos en la misma tarea.

---

## Paso 6 - Validar regresión

Verificar:

- caso original;
- caso corregido;
- permisos;
- datos persistidos.

Si no hay tests automáticos, ejecutar checklist manual.

---

## Paso 7 - Registrar decisiones

Actualizar:

- knowledge/decisions.md
- knowledge/technical-debt.md

Dejar claro:

- qué se tocó;
- por qué;
- qué quedó pendiente.

---

## Resultado esperado

- problema resuelto sin romper comportamiento existente;
- impacto controlado;
- deuda técnica documentada;
- base lista para iteración siguiente.
