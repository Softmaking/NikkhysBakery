# NikkhysBakery SDD

Softmaking SDD is the development process for the NikkhysBakery fullstack project.
The root folder coordinates two separate application repositories:

- `NikkhysBakery-Front`: Angular public site and administration panel.
- `NikkhysBakery-Back`: NestJS API, PostgreSQL data model and business rules.

## Mandatory Context

Before planning a change, use repository evidence in this order:

1. `AGENTS.md`
2. `docs/01-contexto-negocio.md`
3. `docs/02-requerimientos-generales.md`
4. `docs/03-arquitectura-general.md`
5. `docs/04-flujos-end-to-end.md`
6. `docs/05-contratos-front-back.md` when the change affects the API or UI
7. `tasks/current-task.md`
8. The `AGENTS.md` of each affected application
9. Relevant application documentation and source code

The root documentation coordinates the project. The backend code is authoritative
for API and database behavior, while frontend code is authoritative for implemented
UI behavior. Cross-application contracts are documented in
`docs/05-contratos-front-back.md`; there is no shared-contracts package.

## Workflow

Classify every change as New Feature, Bugfix, Refactor, Module Generation or Hotfix.
Use the corresponding file under `.sdd/workflows/`. Non-trivial cross-application,
database or security changes require approved specification artifacts before code
is modified. Documentation-only maintenance may use the lightweight bugfix flow.

Feature artifacts belong under `specs/features/<feature-name>/` and use the templates
in `.sdd/templates/`. `tasks/` remains the operational backlog and completion log.

## Repository Boundaries

- Modify only the application repository assigned by the approved task.
- For cross-application changes, update the root contract first, then backend and
  frontend in that order, followed by documentation and validation.
- Database schema changes require an incremental migration in the backend.
- Backend permissions and guards remain authoritative over frontend route guards.
- No mobile application, monorepo workspace or shared contract package is part of
  the current project scope.

## Validation

- Frontend: `npm run build` and, when relevant, `npx tsc -p tsconfig.app.json --noEmit`.
- Backend: `npm run build`, `npm run lint` and relevant Jest tests.
- Cross-application changes: validate both applications and the root contract docs.

## Language

Project documentation and SDD artifacts use Spanish unless an artifact explicitly
requires another language. Domain names and API identifiers remain unchanged.
