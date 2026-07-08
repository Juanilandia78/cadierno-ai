# Playbook - Docker Compose

## Objetivo

Definir una arquitectura reproducible para el entorno de desarrollo y producción utilizando Docker Compose.

---

## Buenas prácticas

- Un servicio por responsabilidad.
- Utilizar redes dedicadas.
- Persistir datos mediante Volumes.
- Utilizar variables de entorno.
- Definir depends_on cuando corresponda.
- Nombrar los servicios de forma descriptiva.

---

## Checklist

✓ Servicios separados

✓ Volumes configurados

✓ Networks configuradas

✓ Variables de entorno

✓ Healthcheck cuando corresponda

✓ Restart Policy definida

---

## Filosofía

Docker Compose debe permitir levantar todo el proyecto con un único comando.