# Module Generation Workflow

## Trigger

Use when generating a reusable domain module that may affect backend, frontend, database, permissions, audit, and documentation.

## Agents Involved

- Orchestrator
- Product Owner
- Business Analyst
- Architect
- Tech Lead
- Developer
- QA

## Flow

1. Orchestrator confirms a module is required by an approved spec.
2. Product Owner defines module scope and non-goals.
3. Business Analyst defines business rules, actors, permissions, and audit impact.
4. Architect defines bounded context, root contract impact, database design and backend/frontend impact.
5. Tech Lead creates ordered tasks.
6. Approval gate before implementation.
7. Developer updates the root contract first when applicable, then database, backend, frontend, tests and docs.
8. QA validates complete module behavior.

## Expected Artifacts

- Feature spec.
- Technical design.
- Task plan.
- Test plan.
- Implementation report.
- Architecture decision update if applicable.

## Approval Gates

Mandatory:

- Module scope approved before technical design.
- Cross-application contract design approved before implementation when applicable.
- Migration plan approved before database changes.
- QA approval required before completion.

## Stop Criteria

- Module is project-specific and not backed by a spec.
- Active multi-tenancy is assumed without approval.
- Scope exceeds the approved backend/frontend boundaries.
- Permissions or audit strategy is unclear.
