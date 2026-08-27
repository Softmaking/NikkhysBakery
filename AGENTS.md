# AGENTS

Guia raiz para trabajar el proyecto NikkhysBakery con enfoque spec-driven
development.

## Alcance

Esta raiz coordina dos repositorios separados:

- `NikkhysBakery-Front`: Angular, UI, rutas, estado, servicios HTTP.
- `NikkhysBakery-Back`: NestJS, API, seguridad, reglas, datos y migraciones.

No asumir que la raiz es un monorepo versionado. Si se agregan archivos raiz,
validar despues como se versionaran.

## Orden de Trabajo

1. Leer `README.md`.
2. Leer `docs/01-contexto-negocio.md`.
3. Revisar `docs/05-contratos-front-back.md` si el cambio toca API o UI.
4. Revisar `tasks/current-task.md`.
5. Entrar al subproyecto afectado y leer su `AGENTS.md`.
6. Leer `.sdd/README.md` y la memoria `.sdd/memory/` antes de seleccionar un workflow.

## Fuentes de Verdad

- Negocio y flujos: `docs/01-contexto-negocio.md` y `docs/04-flujos-end-to-end.md`.
- Requerimientos generales: `docs/02-requerimientos-generales.md`.
- Arquitectura fullstack: `docs/03-arquitectura-general.md`.
- Contratos front-back: `docs/05-contratos-front-back.md`.
- Detalle backend: `NikkhysBakery-Back/docs/`.
- Detalle frontend: `NikkhysBakery-Front/docs/`.

## Reglas

- No inventar endpoints: verificar controlador backend y servicio Angular.
- No inventar permisos: verificar migraciones, IAM y guards.
- Si cambia un contrato, actualizar backend docs, frontend docs y contrato raiz.
- Si cambia modelo de datos, actualizar `NikkhysBakery-Back/docs/modelo-datos.md`
  y `NikkhysBakery-Back/docs/migraciones.md`.
- Si cambia una ruta o pantalla, actualizar `NikkhysBakery-Front/docs/rutas.md`
  y/o `NikkhysBakery-Front/docs/componentes.md`.
- Registrar decisiones pendientes en `tasks/current-task.md`.
- Los mensajes de commit deben escribirse siempre en español.

## Criterio de Cierre

Una tarea se considera cerrada cuando:

- el comportamiento esperado esta especificado,
- el contrato front-back esta claro,
- codigo y documentacion coinciden,
- se ejecutaron validaciones razonables,
- el resultado queda registrado en `tasks/done.md`.
