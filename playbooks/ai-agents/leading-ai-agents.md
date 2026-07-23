# Responding to AI Agents

## Objetivo

Este playbook explica cómo responder correctamente a un agente de IA durante una implementación.

La mayoría de los problemas no aparecen porque el agente programe mal, sino porque recibe instrucciones ambiguas o demasiado grandes.

La regla principal es simple:

> Hablarle al agente como si fuera un integrante del equipo, no como un chat.

---

# Filosofía

El usuario actúa como:

- Product Owner
- Tech Lead
- Arquitecto

El agente actúa como:

- Backend Engineer
- Frontend Engineer
- QA
- Reviewer
- DevOps

El usuario toma decisiones.

El agente implementa.

Nunca al revés.

---

# Regla principal

Las respuestas deben ser:

- claras;
- concretas;
- con alcance definido;
- con criterio de aceptación;
- indicando cuándo detenerse.

Evitar respuestas como:

- "dale"
- "hacelo"
- "seguí"
- "perfecto"

Siempre indicar exactamente qué se espera.

---

# Estructura recomendada

Usar siempre una estructura similar.

```
Estado:

APROBADO

Alcance:

...

Restricciones:

...

Entregables:

...

Detenerse al finalizar.
```

---

# Aprobando una decisión de arquitectura

Ejemplo:

```
Aprobado.

Se adopta esta decisión de arquitectura.

No modifiques otras reglas.

Continuá con la siguiente microtarea.
```

---

# Aprobando una regla de negocio

Ejemplo:

```
Aprobado.

La regla funcional queda definida:

- ...
- ...
- ...

Esta decisión pasa a formar parte del contrato del sistema.

Podés continuar.
```

---

# Aprobando una propuesta técnica

```
La propuesta queda aprobada.

Implementala respetando la arquitectura existente.

No introduzcas refactorizaciones adicionales.

Al finalizar:

- ejecutá las pruebas;
- mostrámelas;
- detenete.
```

---

# Aprobando una microtarea

```
Microtarea aprobada.

Continuá únicamente con la siguiente microtarea.

No modifiques funcionalidades fuera del alcance.

Detenete al finalizar.

Entregá evidencia.
```

---

# Corrigiendo un defecto

```
Aprobado.

Corregí únicamente ese defecto.

No aproveches para refactorizar otras partes.

Ejecutá las pruebas afectadas.

Detenete al finalizar.
```

---

# Rechazando una propuesta

No responder solamente:

> No.

Explicar el motivo.

Ejemplo:

```
Rechazado.

Motivo:

Esta solución rompe la arquitectura definida.

Buscá una alternativa que:

- mantenga el Service Layer;
- no modifique la API pública;
- sea compatible con la implementación actual.

No implementes cambios todavía.

Presentá primero la nueva propuesta.
```

---

# Cuando el agente hace una pregunta funcional

Responder como Product Owner.

Ejemplo:

Agente:

> ¿Qué ocurre si el pago llega después de 30 minutos?

Respuesta:

```
Decisión funcional.

La reserva expira luego de 30 minutos.

Un pago posterior no reactiva automáticamente la reserva.

Debe quedar registrado como pago tardío y resolverse mediante conciliación manual.

Esta decisión pasa a formar parte del contrato funcional.

Podés continuar.
```

---

# Cuando el agente pide elegir entre varias opciones

No responder únicamente:

> Opción B.

Responder:

```
Se aprueba la opción B.

Motivos:

- menor complejidad;
- menor riesgo;
- mantiene compatibilidad;
- cumple el objetivo funcional.

Implementá únicamente esta alternativa.

Descartá las demás.
```

---

# Cuando el agente termina una fase

```
La fase queda aprobada.

No avances automáticamente.

Esperá la siguiente tarea.
```

---

# Cuando el agente termina una tarea

Nunca asumir que terminó correctamente.

Solicitar:

- pruebas;
- evidencia;
- archivos modificados;
- riesgos;
- deuda técnica;
- estado final.

Ejemplo:

```
Antes de cerrar la tarea quiero:

- pruebas ejecutadas;
- evidencia;
- riesgos;
- archivos modificados;
- deuda técnica.

No implementes cambios nuevos.

Emití una conclusión final.
```

---

# Cuando el agente propone refactorizar

Regla general:

No aceptar refactorizaciones fuera del alcance.

Ejemplo:

```
No autorizado.

La refactorización queda fuera del alcance actual.

Limitate a resolver el requerimiento solicitado.

Podrá planificarse en una tarea independiente.
```

---

# Cuando el agente intenta avanzar solo

Es habitual que un agente continúe con tareas no solicitadas.

Responder:

```
Detenerse.

No avances automáticamente.

Esperá la siguiente aprobación.
```

---

# Evidencia mínima esperada

Al finalizar una microtarea debería entregar:

- archivos modificados;
- pruebas ejecutadas;
- resultado;
- evidencia;
- riesgos;
- próximos pasos.

---

# Qué evitar

Evitar respuestas como:

- Dale.
- Seguí.
- Perfecto.
- Sí.
- No.
- Hacé lo que consideres.

Ese tipo de respuestas dejan demasiadas decisiones al agente.

---

# Principio final

Un buen agente necesita un buen Tech Lead.

La calidad de la implementación depende tanto de las instrucciones como del modelo utilizado.

Cadierno AI propone que el usuario dirija al agente como dirigiría a un desarrollador de su equipo:

- definiendo objetivos;
- aprobando decisiones;
- limitando el alcance;
- solicitando evidencia;
- cerrando tareas únicamente cuando existan pruebas suficientes.
