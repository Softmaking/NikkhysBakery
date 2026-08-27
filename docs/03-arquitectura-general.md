# Arquitectura General

## Vista General

El sistema esta compuesto por dos aplicaciones independientes:

- `NikkhysBakery-Front`: SPA Angular para sitio publico y panel administrativo.
- `NikkhysBakery-Back`: API NestJS con persistencia PostgreSQL via TypeORM.

La integracion se realiza por HTTP JSON. El frontend centraliza llamadas en
servicios API y el backend expone controladores por dominio.

## Backend

Stack:

- NestJS 11
- TypeORM 0.3
- PostgreSQL
- Passport/JWT
- Swagger/OpenAPI
- `class-validator`
- Guards, interceptors y filters propios

Documentacion tecnica:

- `NikkhysBakery-Back/docs/arquitectura-back.md`
- `NikkhysBakery-Back/docs/modelo-datos.md`
- `NikkhysBakery-Back/docs/api-endpoints.md`
- `NikkhysBakery-Back/docs/reglas-negocio.md`
- `NikkhysBakery-Back/docs/seguridad-permisos.md`
- `NikkhysBakery-Back/docs/migraciones.md`

## Frontend

Stack:

- Angular 22.0.7
- Angular Material 22.0.5
- Tailwind CSS 4.1.12
- RxJS 7
- TypeScript 6.0.3
- Signals

Documentacion tecnica:

- `NikkhysBakery-Front/docs/arquitectura-front.md`
- `NikkhysBakery-Front/docs/componentes.md`
- `NikkhysBakery-Front/docs/rutas.md`
- `NikkhysBakery-Front/docs/estado-signals.md`
- `NikkhysBakery-Front/docs/servicios-api.md`

## Integracion

- Base URL frontend por defecto: `http://localhost:3000`.
- Swagger backend: `/docs`.
- Rutas reales actuales sin prefijo global `/v1`.
- Auth por `Authorization: Bearer <token>`.
- Refresh token por cookie `HttpOnly`.
- Contexto de sucursal por `x-branch-id` cuando aplica.

## Capas de Decisiones

1. Docs raiz: negocio, flujos, contratos y decisiones fullstack.
2. Docs backend/frontend: detalle tecnico por repo.
3. Codigo: fuente final de verdad cuando docs y codigo divergen.

Cuando codigo y documentacion divergen, la tarea debe registrar la divergencia,
elegir contrato objetivo y actualizar ambos lados.
