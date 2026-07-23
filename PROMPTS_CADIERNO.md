# Inicio de tarea técnica

Este proyecto usa Cadierno AI.

Leé primero:
- AGENTS.md
- knowledge/project.md
- knowledge/architecture.md
- knowledge/integrations.md
- knowledge/technical-debt.md

Actuá como [ROL] de Cadierno AI.


------------------------------------

Después reemplazás [ROL] por:
Architect
Backend Engineer
QA
Code Reviewer
Tech Lead

--------------------------------------

Cuando la IA propone una decisión de arquitectura.
Respondé así:

Aprobado.

Se adopta como regla de negocio:

- La reserva expira a los 30 minutos desde su creación.
- Un pago aprobado luego del vencimiento no reactiva automáticamente la reserva.
- Debe registrarse como pago tardío para conciliación manual.
- No modifiques otras reglas de negocio.

Continuá con la siguiente microtarea.

--------------------------------------

2. Cuando termina una microtarea

Microtarea aprobada.

Continuá únicamente con la siguiente microtarea.

No modifiques funcionalidades fuera del alcance actual.

Detenete al finalizar y entregá evidencia.

--------------------------------------

3. Cuando propone una solución

La propuesta queda aprobada.

Implementala respetando la arquitectura existente.

No introduzcas refactorizaciones adicionales.

Al finalizar:

- ejecutá las pruebas correspondientes;
- mostrámelas;
- detenete.

--------------------------------------

4. Cuando termina una fase

La fase queda aprobada.

No avances automáticamente.

Esperá la siguiente tarea.

--------------------------------------

5. Cuando detecta un problema

Aprobado.

Corregí únicamente ese defecto.

No aproveches para refactorizar otras partes.

Ejecutá las pruebas afectadas.

Detenete al finalizar.

--------------------------------------

6. Cuando hace preguntas funcionales

Por ejemplo:

¿Qué pasa si paga después de 30 minutos?

Respondé como Product Owner:

Decisión funcional:

...

Esta decisión pasa a formar parte del contrato del sistema.

Podés continuar.

--------------------------------------

El patrón que se usaría siempre

Estado:

APROBADO

Alcance:

...

Restricciones:

...

Entregables:

...

Detenerse al finalizar.

Por ejemplo:

Estado:

APROBADO.

Alcance:

Implementar únicamente ReservationService.

Restricciones:

- No modificar controladores fuera de lo necesario.
- No cambiar reglas de negocio.
- No refactorizar módulos no relacionados.

Entregables:

- Código.
- Pruebas.
- Evidencia.

Detenerse al finalizar.