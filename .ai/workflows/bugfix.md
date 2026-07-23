# Workflow - Bug Fix

## Metadata

**Prioridad:** Alta

**Especialista Líder:** QA

**Participantes**

- Architect
- Backend
- Database
- Reviewer
- Documentation

---

## Objetivo

Corregir un error sin introducir regresiones.

---

## Cuándo utilizar

- Bugs.
- Errores.
- Excepciones.
- Problemas funcionales.

---

## Flujo

> Si hay transacciones, concurrencia, integraciones o varios escenarios de prueba,
> usar [Ejecución por Microtareas](../../playbooks/ai-agents/microtask-execution.md):
> dividir, validar cada paso, recopilar evidencia y auditar antes del cierre.

### 1. QA

- Reproducir.
- Documentar.

---

### 2. Architect

- Analizar origen.
- Definir estrategia.

---

### 3. Backend

- Corregir.

---

### 4. Database

Si aplica.

---

### 5. QA

- Validar corrección.
- Ejecutar regresión.

---

### 6. Reviewer

Revisar calidad.

---

### 7. Documentation

Actualizar CHANGELOG si corresponde.

---

## Criterios

✓ Bug solucionado

✓ No rompe otra funcionalidad

✓ Existe explicación de la causa
