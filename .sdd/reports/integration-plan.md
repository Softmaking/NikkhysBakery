# Softmaking SDD Integration Plan

## Current Integration

- `AGENTS.md` defines the root reading order and project boundaries.
- `.sdd/README.md` defines workflow selection and artifact rules.
- `docs/` contains business, architecture, flow and cross-application contracts.
- `tasks/` contains operational backlog and completion history.
- `NikkhysBakery-Front/` and `NikkhysBakery-Back/` remain independent application repositories.

## Feature Artifacts

Use `.sdd/templates/` to create `specs/features/<feature-name>/` artifacts. Keep
requirements, implementation plans and validation evidence synchronized with the
root contract and the affected application documentation.

## Pending / Not Evidenced

- Provider-specific OpenCode automation or an SDD workflow runner.
