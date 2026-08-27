# NikkhysBakery SDD Project Audit

## Evidence

- Root coordination docs: `AGENTS.md`, `README.md`, `docs/` and `tasks/`.
- Frontend repository: `NikkhysBakery-Front/`, Angular 22.0.7 and TypeScript 6.0.3.
- Backend repository: `NikkhysBakery-Back/`, NestJS 11.1.28 and version 0.4.2.
- Cross-application contract: `docs/05-contratos-front-back.md`.

## Findings

- Frontend and backend are separate repositories coordinated from the root.
- Backend is authoritative for API, permissions, business rules and migrations.
- Frontend consumes HTTP APIs through services and provides UX-level guards.
- No root monorepo, mobile app or shared contracts package is evidenced.
- SDD artifacts are stored under `.sdd/`; feature artifacts belong under `specs/features/`.

## Pending / Not Evidenced

- Automated SDD runner, CI integration and multi-agent runtime.
- Future application version upgrade strategy.
