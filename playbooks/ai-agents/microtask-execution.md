# Ejecución por Microtareas con Agentes de IA

## Objetivo

Evitar que un agente se bloquee, repita análisis o declare una tarea incompleta
cuando recibe una implementación demasiado grande.

Este playbook aplica especialmente a agentes como:

- Codex
- Cursor Agent
- Claude Code
- agentes de VS Code
- asistentes que modifican código directamente

---

## Principio principal

Una tarea grande debe dividirse en microtareas concretas, ejecutables y verificables.

No se debe pedir al agente:

> Implementá toda la funcionalidad y cerrá la tarea.

Se recomienda avanzar mediante pasos independientes:

1. Implementación.
2. Prueba del caso feliz.
3. Prueba de rollback.
4. Prueba de concurrencia.
5. Prueba de conflictos.
6. Validación de invariantes.
7. Revisión final.
8. Cierre documentado.

---

## Regla de avance

Cada microtarea debe indicar:

- alcance exacto;
- qué puede modificar;
- qué no debe modificar;
- criterio de aceptación;
- pruebas que debe ejecutar;
- evidencia que debe entregar;
- punto en el que debe detenerse.

Ejemplo:

```text
Implementá únicamente la prueba de rollback.

Verificá:

- que no quede una reserva persistida;
- que no quede una clave de idempotencia;
- que no queden registros processing.

Ejecutá la prueba, informá el resultado y detenete.
No avances todavía a las pruebas de concurrencia.
```

## Cierre basado en evidencia

Implementar no equivale a cerrar. Una microtarea se cierra solo con criterio de
aceptación satisfecho, pruebas reproducibles, invariantes validados, QA, Code
Review y evidencia. Los únicos estados finales son **APROBADA Y CERRADA** y
**RECHAZADA**.

Para rollback, comprobar que no queden efectos persistidos. Para concurrencia,
usar conexiones independientes del motor real cuando el motor de pruebas no
represente locks. Para conflictos, probar el mismo identificador con contexto
distinto. La auditoría final revisa diff, migraciones, secretos, archivos
temporales, documentación y resultados de prueba.
