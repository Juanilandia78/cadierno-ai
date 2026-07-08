# Playbook - Queues

## Objetivo

Ejecutar procesos pesados de forma asíncrona.

---

## Utilizar cuando

- Emails
- Importaciones
- Exportaciones
- PDFs
- APIs externas
- Imágenes

---

## Evitar

- Ejecutar procesos largos dentro de Requests HTTP.

---

## Checklist

✓ Job creado

✓ Queue configurada

✓ Manejo de errores

✓ Retries

✓ Logs

---

## Filosofía

El usuario no debe esperar procesos que pueden ejecutarse en segundo plano.