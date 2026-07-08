# Playbook - Migrations

## Objetivo

Gestionar cambios en la estructura de la base de datos de forma segura y versionada.

---

## Buenas prácticas

- Una migración por cambio.
- Utilizar nombres descriptivos.
- Implementar correctamente up() y down().
- Evitar modificar migraciones ya ejecutadas en producción.

---

## Checklist

✓ up()

✓ down()

✓ Claves foráneas

✓ Índices

✓ Tipos de datos correctos

---

## Filosofía

La historia de la base de datos debe poder reproducirse desde cero.