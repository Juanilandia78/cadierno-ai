# Playbook - Multi Tenancy

## Objetivo

Desarrollar funcionalidades compatibles con arquitecturas Multi Tenant.

---

## Reglas

- Nunca mezclar datos entre tenants.
- Respetar el contexto actual.
- Filtrar siempre por tenant.
- Validar permisos.

---

## Validar

- Consultas
- Relaciones
- Policies
- Cache
- Colas

---

## Checklist

✓ Tenant detectado

✓ Scope aplicado

✓ Sin fuga de información

✓ Tests

---

## Filosofía

El aislamiento entre tenants nunca es opcional.