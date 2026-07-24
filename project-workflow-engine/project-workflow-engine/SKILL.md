---
name: project-workflow-engine
description: Start, continue, repair, refactor, migrate, audit, release, or hand off a software project through a stable development operating system. Use when converting an idea or unfinished codebase into an evidence-based project state, explicit requirements, dependency-aware tasks, a smallest complete vertical slice, synchronized code and documentation, verified tests and deployment state, failure recovery, and an exact continuation handoff.
---

# Project Workflow Engine

Turn development work into a reproducible operating system rather than a conversation-dependent plan.

## Primary Reference

Read `references/project_foundation.md` first.

It defines:

- operating principles;
- source-of-truth rules;
- project variables;
- variable resolution;
- complexity and risk scoring;
- task sizing;
- default architecture decisions;
- agent behavior;
- anti-patterns.

## Supporting References

Read only what the current mode requires:

- `references/workflow_contract.md` — standard phases from intake through handoff
- `references/artifact_contract.md` — required durable project documents and schemas
- `references/mode_contracts.md` — new, existing, feature, repair, refactor, migration, data-pipeline, audit, and handoff modes
- `references/testing_release_contract.md` — baseline, regression, deployment, release, and rollback gates
- `references/failure_recovery_contract.md` — failure classification, root cause, stop-loss, and recovery
- `references/operations_runbook.md` — session discipline, work logs, commits, continuation, and operator response
- `references/migration_map.md` — mapping from the original monolithic skill into this package
- `templates/` — project-system, plan, task, risk, work-log, handoff, and release starters
- `tools/validate_project_system.py` — validates a generated project operating system

## Core Principle

Inspect reality, create the smallest complete vertical slice, verify every meaningful change, and leave an exact continuation state.

The skill must produce working evidence when execution is possible. It must not stop at planning merely because planning is easier.

## Operating Modes

```yaml
PROJECT_MODE: "new | existing | feature | repair | refactor | migration | data_pipeline | audit | release | handoff"
AUTONOMY_LEVEL: "plan_only | execute_with_review | execute_freely"
DOCUMENTATION_LEVEL: "minimal | standard | exhaustive"
```

### New

Bootstrap a project and complete the first end-to-end slice.

### Existing

Resume from the actual repository, environment, tests, and deployment state.

### Feature

Add one bounded capability without destabilizing unrelated behavior.

### Repair

Freeze scope, reproduce failures, recover the last known working path, and add regression coverage.

### Refactor

Change internal structure while preserving an explicit behavior contract.

### Migration

Move code, data, infrastructure, or platform state with dry runs, reconciliation, and rollback.

### Data Pipeline

Build or repair ingestion, transformation, lineage, identity, rejection, and review behavior.

### Audit

Compare claims, documentation, code, tests, schema, and deployment without silently changing them.

### Release

Evaluate a concrete commit against production gates and rollback readiness.

### Handoff

Package the verified continuation state for another developer or agent.

## Required Inputs

Resolve or infer:

```yaml
PROJECT_NAME: ""
PROJECT_TYPE: ""
PROJECT_GOAL: ""
PRIMARY_USER: ""
PRIMARY_OUTCOME: ""
SUCCESS_METRIC: ""
NON_GOALS: []
REPOSITORY_URL: ""
REPOSITORY_ROOT: "."
DEFAULT_BRANCH: "main"
WORKING_BRANCH: ""
LANGUAGES: []
FRAMEWORKS: []
PACKAGE_MANAGER: ""
RUNTIME_VERSIONS: {}
DATABASES: []
EXTERNAL_SERVICES: []
DEPLOYMENT_TARGETS: []
HARD_CONSTRAINTS: []
DO_NOT_CHANGE: []
LAST_KNOWN_WORKING_COMMIT: ""
CURRENT_DEPLOYED_COMMIT: ""
KNOWN_BLOCKERS: []
```

Inspect executable evidence before accepting documentation claims.

Do not fabricate a repository, dependency, environment variable, schema, service connection, test result, commit, or deployment state.

## Reference Routing

### Every project

Read:

- `references/project_foundation.md`
- `references/workflow_contract.md`
- `references/artifact_contract.md`

### New, existing, feature, refactor, migration, data-pipeline, or audit work

Also read `references/mode_contracts.md`.

### Any code or configuration change

Also read:

- `references/testing_release_contract.md`
- `references/operations_runbook.md`

### Failure, blocker, broken build, environment mismatch, or deployment drift

Also read `references/failure_recovery_contract.md`.

### Release decision

Read all of:

- `references/testing_release_contract.md`
- `references/failure_recovery_contract.md`
- `references/operations_runbook.md`

## Workflow

Follow `references/workflow_contract.md`.

Required sequence:

1. classify the mode and capture the actual state;
2. identify sources of truth and conflicting claims;
3. define testable requirements and non-goals;
4. map architecture, dependencies, ownership, failure paths, and rollback;
5. select the smallest complete vertical slice;
6. split work into dependency-aware tasks no larger than medium;
7. prove the pre-change baseline;
8. implement one coherent task at a time;
9. validate narrowly, then broadly;
10. integrate and run regression paths;
11. evaluate release and rollback readiness;
12. update durable artifacts and exact handoff state.

A task is not complete because files changed. It is complete when its acceptance criteria are verified and its continuation state is recorded.

## Required Outputs

Depending on mode, produce or update:

- project context;
- requirements;
- architecture;
- execution plan;
- decision log;
- risk register;
- test status;
- work log;
- release checklist;
- handoff;
- code and configuration;
- migrations;
- automated tests;
- deployment evidence;
- rollback instructions.

For small projects, use one `docs/PROJECT_SYSTEM.md` when that is clearer than many empty documents.

Do not create duplicate documentation when an authoritative equivalent already exists.

## Validation

Use `references/testing_release_contract.md`.

At minimum record:

```yaml
INSTALL:
LINT:
TYPECHECK:
UNIT_TESTS:
INTEGRATION_TESTS:
END_TO_END:
BUILD:
LOCAL_RUN:
MIGRATIONS:
DEPLOYMENT:
ROLLBACK:
PREEXISTING_FAILURES: []
INTRODUCED_FAILURES: []
```

Never claim a command passed unless it was executed successfully.

Never claim a deployment is current unless the deployed revision was verified.

## Handoff

Return:

```yaml
STATUS: "complete | partial | blocked"
MODE:
CURRENT_PHASE:
REPOSITORY:
WORKING_BRANCH:
WORKING_COMMIT:
LAST_KNOWN_WORKING_COMMIT:
DEPLOYED_COMMIT:
COMPLETED:
VERIFIED:
NOT_COMPLETED:
FILES_CHANGED:
TESTS_RUN:
FAILED_TESTS:
MIGRATIONS:
DEPLOYMENT_STATUS:
ROLLBACK_POINT:
DECISIONS:
ASSUMPTIONS:
KNOWN_RISKS:
BLOCKERS:
NEXT_ACTION:
NEXT_THREE_TASKS:
COMMANDS_TO_CONTINUE:
FILES_TO_READ_FIRST:
```

Clearly distinguish completed, planned, attempted, failed, blocked, and unverified work.

## Completion Gate

```yaml
ACTUAL_STATE_CAPTURED: true
SOURCE_OF_TRUTH_DEFINED: true
MUST_REQUIREMENTS_TESTABLE: true
NON_GOALS_EXPLICIT: true
VERTICAL_SLICE_IDENTIFIED: true
TASKS_DEPENDENCY_ORDERED: true
BASELINE_RECORDED: true
RELEVANT_TESTS_EXECUTED: true
NEW_FAILURES_EXPLAINED: true
DOCUMENTATION_SYNCHRONIZED: true
ROLLBACK_DEFINED_WHERE_REQUIRED: true
WORK_LOG_UPDATED: true
HANDOFF_UPDATED: true
NEXT_ACTION_EXACT: true
```

## Final Instruction

Never leave a project dependent on hidden conversation history.

The repository, durable artifacts, test evidence, deployment state, rollback point, and next action must tell the truth without needing the prior chat.
