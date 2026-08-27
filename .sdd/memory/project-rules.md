# Project Rules

## Scope

- The root coordinates `NikkhysBakery-Front` and `NikkhysBakery-Back` as separate repositories.
- Do not assume a root package manager, workspace, mobile app or shared-contracts package.
- Use evidence from code and current project documentation; mark unknowns as `Pending / Not evidenced`.

## Source Of Truth

1. Approved feature or bugfix artifact for the current change.
2. Backend code for API, permissions, business rules and database behavior.
3. Frontend code for implemented UI behavior.
4. `docs/05-contratos-front-back.md` for the documented cross-application contract.
5. Root and application `AGENTS.md` files.
6. Remaining documentation and task records.

Update affected documentation in the same change. Never invent endpoints or permissions.

## Backend

- NestJS controllers stay lightweight; business logic belongs in services.
- Inputs use validated DTOs, not entities.
- Schema changes require incremental TypeORM migrations.
- Authorization is role/permission based and must remain centralized and auditable.

## Frontend

- Use Angular standalone components, Signals where appropriate and separate component files.
- Keep HTTP calls in API services.
- Keep authentication and permission logic centralized.
- Current versions: Angular 22.0.7, Angular Material 22.0.5, TypeScript 6.0.3 and Tailwind CSS 4.1.12.

## Validation

- Frontend changes require the frontend build and focused type/tests when applicable.
- Backend changes require build, lint and relevant tests.
- Cross-application changes require validation of both applications.

## Git And Security

- Commit messages are written in Spanish.
- Do not commit secrets or local `.env` files.
- Keep changes minimal and avoid unrelated refactors.

## Pending / Not Evidenced

- No automated SDD workflow runner is evidenced.
- No root CI or multi-agent runtime is evidenced.
- Production domain and social-media handles require owner confirmation before deployment.
