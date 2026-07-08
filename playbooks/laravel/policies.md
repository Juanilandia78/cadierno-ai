# Playbook - Policies

## Objetivo

Toda autorización debe implementarse mediante Policies.

Nunca realizar verificaciones de permisos directamente en Controllers.

---

## Cuándo utilizar

- CRUD
- Recursos privados
- Multiusuario
- Multiempresa

---

## Reglas

- Una Policy por modelo.
- Utilizar authorize().
- Evitar lógica duplicada.
- Reutilizar Gates cuando corresponda.

---

## Checklist

✓ Policy creada

✓ Métodos implementados

✓ Permisos validados

✓ Tests

---

## Filosofía Cadierno AI

La autorización pertenece a las Policies.

No al Controller.