# Playbook - REST API

## Objetivo

Implementar APIs REST siguiendo las convenciones de Laravel y las buenas prácticas de Cadierno AI.

---

# Cuándo utilizar

Utilizar cuando se cree:

- CRUDs
- APIs públicas
- APIs privadas
- Integraciones SPA
- Integraciones móviles
- Microservicios

---

# Estructura recomendada

La funcionalidad debería organizarse utilizando:

- Controller
- Form Request
- Service
- Resource
- Policy
- Model
- Migration (si corresponde)
- Tests

---

# Flujo recomendado

1. Definir la ruta.
2. Crear el Request para validaciones.
3. Implementar la lógica en un Service.
4. Utilizar Policies para autorización.
5. Devolver Resources.
6. Manejar excepciones.
7. Crear Tests.

---

# Respuesta

Toda respuesta debería mantener un formato consistente.

Ejemplo:

```json
{
    "success": true,
    "message": "Operación realizada correctamente.",
    "data": {}
}
```

Para errores:

```json
{
    "success": false,
    "message": "Descripción del error.",
    "errors": {}
}
```

---

# Buenas prácticas

- Nunca devolver Models directamente.
- Utilizar Resources.
- Validar siempre mediante Form Requests.
- No colocar lógica de negocio en Controllers.
- Utilizar códigos HTTP correctos.
- Evitar consultas N+1.
- Mantener consistencia en todas las respuestas.

---

# Checklist

Antes de finalizar verificar:

- Rutas correctamente definidas.
- Validaciones implementadas.
- Policies aplicadas.
- Services utilizados.
- Resources implementados.
- Tests creados.
- Documentación actualizada.

---

# Especialistas involucrados

- Architect
- Backend
- Database
- QA
- Reviewer
- Documentation

---

# Filosofía Cadierno AI

Una API no solo debe funcionar.

Debe ser consistente, mantenible y predecible para cualquier cliente que la consuma.