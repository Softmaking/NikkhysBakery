# Hotfix Workflow

## Trigger

Use only for an urgent production stability or security issue requiring an abbreviated process.

## Flow

1. Orchestrator records the evidence and affected application.
2. Tech Lead defines the smallest safe fix and validation.
3. User approves the abbreviated task plan.
4. Developer implements only the approved fix.
5. QA validates the regression and affected application.
6. Complete the normal SDD artifacts retrospectively when required.

## Stop Criteria

- The issue is not evidenced or reproducible.
- The fix changes an API, database schema or security boundary without explicit approval.
- Required validation cannot be executed or documented.
