# Playbook - Service Layer

## Objetivo

Implementar lógica de negocio utilizando una capa de Services.

El objetivo es mantener Controllers livianos, reutilizar código y facilitar el mantenimiento del sistema.

---

# Cuándo utilizar este Playbook

Utilizar cuando:

- La lógica de negocio supera unas pocas líneas.
- La misma lógica será reutilizada.
- Existen múltiples pasos para completar una operación.
- Se realizan llamadas a APIs externas.
- Se utilizan transacciones.
- Se interactúa con múltiples modelos.

No utilizar cuando el Controller solamente guarda un registro sencillo.

---

# Beneficios

- Controllers pequeños.
- Código reutilizable.
- Mayor mantenibilidad.
- Tests más simples.
- Separación de responsabilidades.

---

# Estructura recomendada

```
app/
└── Services/
    └── NombreDelService.php
```

---

# Buenas prácticas

- Un Service debe tener una única responsabilidad.
- Evitar métodos demasiado largos.
- Utilizar inyección de dependencias.
- Lanzar excepciones cuando corresponda.
- Evitar acceder directamente al Request.
- Retornar objetos claros.

---

# Checklist

Antes de finalizar verificar:

- ¿El Controller quedó simple?
- ¿La lógica está desacoplada?
- ¿El código puede reutilizarse?
- ¿Se manejan correctamente los errores?
- ¿Existen Tests cuando corresponden?

---

# Especialistas involucrados

- Architect
- Backend
- QA
- Reviewer

---

# Filosofía Cadierno AI

Los Controllers coordinan.

Los Services resuelven el negocio.

Cada clase debe tener una responsabilidad clara.