# Architecture Decisions

## ADR-001: Root Coordination With Separate Repositories

The root is a specification and coordination layer. Frontend and backend remain
independent repositories under `NikkhysBakery-Front/` and `NikkhysBakery-Back/`.

## ADR-002: Backend API Authority

The NestJS backend is authoritative for API behavior, validation, permissions,
business rules and PostgreSQL schema. TypeORM schema evolution uses incremental
migrations.

## ADR-003: Documented Cross-Application Contract

The canonical cross-application contract is `docs/05-contratos-front-back.md`.
There is no shared TypeScript contracts package. Contract changes update the root
document, backend implementation and frontend consumer together.

## ADR-004: Permission-Based Authorization

Backend guards enforce permissions. Frontend guards and menus provide UX support
only and must not be treated as a security boundary.

## ADR-005: Current Technology Versions

- Frontend: Angular 22.0.7, Material/CDK 22.0.5, TypeScript 6.0.3.
- Backend: NestJS 11.1.28, TypeORM 0.3.31 and TypeScript 5.7.3.
- Package installation currently uses npm and committed `package-lock.json` files.

## Pending / Not Evidenced

- Future version upgrades require a separate approved task.
- No mobile client or root monorepo workspace is currently part of the system.
