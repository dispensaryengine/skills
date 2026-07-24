# Artifact Contract

Durable artifacts keep the project independent from hidden conversation state.

## Source-of-Truth Matrix

Identify the authoritative artifact for:

```yaml
SOURCE_CODE:
REQUIREMENTS:
ARCHITECTURE:
EXECUTION_PLAN:
DECISIONS:
RISKS:
WORK_HISTORY:
ENVIRONMENT:
DATABASE_SCHEMA:
API_CONTRACT:
TEST_STATUS:
DEPLOYMENT_STATE:
HANDOFF:
```

Do not create a duplicate when an authoritative equivalent exists.

---

## Standard Artifact Set

```text
docs/
  PROJECT_CONTEXT.md
  PROJECT_REQUIREMENTS.md
  ARCHITECTURE.md
  EXECUTION_PLAN.md
  DECISION_LOG.md
  RISK_REGISTER.md
  TEST_STATUS.md
  WORK_LOG.md
  HANDOFF.md
  RELEASE_CHECKLIST.md
```

Small projects may use:

```text
docs/PROJECT_SYSTEM.md
```

The combined document must still contain the required information.

---

## Project Context

Must contain:

- purpose;
- current state;
- target state;
- primary users;
- primary outcome;
- success metric;
- repository;
- environments;
- dependencies;
- constraints;
- non-goals;
- terminology;
- blockers;
- source-of-truth map.

---

## Requirements

Each requirement:

```yaml
id: FR-001
title: ""
description: ""
priority: "must | should | could | later"
source: "user | existing_behavior | contract | regulation | assumption"
acceptance_criteria: []
dependencies: []
status: "proposed | approved | implemented | verified | rejected"
```

Required families:

```text
FR
NFR
DATA
SEC
OPS
UX
```

---

## Architecture

Must define:

- system boundaries;
- component responsibilities;
- state ownership;
- data flow;
- API or event contracts;
- storage model;
- trust boundaries;
- external dependencies;
- failure behavior;
- observability;
- deployment topology;
- migration strategy;
- rollback strategy.

Architecture documentation must describe the implementation that exists or the explicitly approved target state.

---

## Execution Plan

Each task:

```yaml
id: TASK-001
type: "ADD | CHANGE | REMOVE | MIGRATE | REPAIR | VERIFY | DOCUMENT | RELEASE"
title: ""
objective: ""
dependencies: []
inputs: []
expected_files: []
implementation_steps: []
acceptance_criteria: []
tests: []
rollback: ""
risk_score: 0
estimated_size: "XS | S | M | L"
status: "queued | active | blocked | complete | verified"
```

The plan must show dependency order and the first vertical slice.

---

## Decision Log

Append decisions:

```text
DEC-001
Date:
Decision:
Context:
Options considered:
Reason:
Consequences:
Reversal cost:
Status:
```

Do not erase a prior decision because it was reversed. Add a new decision that supersedes it.

---

## Risk Register

```yaml
id: RISK-001
description: ""
probability: 1
impact: 1
detectability: 1
priority_score: 1
mitigation: ""
owner: ""
trigger: ""
status: "open | mitigated | accepted | closed"
```

---

## Test Status

Record:

```yaml
REVISION:
ENVIRONMENT:
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
LAST_VERIFIED_AT:
```

Test status without a revision is incomplete.

---

## Work Log

Append only:

```text
Date:
Session objective:
Starting branch:
Starting commit:
Starting state:
Actions completed:
Files changed:
Migrations:
Tests run:
Results:
Decisions:
New risks:
Blockers:
Next exact action:
Ending branch:
Ending commit:
Deployment state:
```

---

## Handoff

Must contain:

- mode and phase;
- branch and commit;
- deployed commit;
- what works;
- what was verified;
- what is incomplete;
- exact commands;
- environment requirements;
- migration state;
- test state;
- deployment state;
- unresolved decisions;
- assumptions;
- next three tasks;
- dangerous areas;
- rollback point.

---

## Release Checklist

Must identify one revision and include:

- requirements verified;
- critical tests;
- build;
- migrations;
- rollback;
- secrets;
- observability;
- documentation;
- handoff;
- defects;
- accepted risks;
- release decision.

---

## Artifact Synchronization Rule

A behavior-changing task must update all affected authorities in the same task.

Examples:

- API change → code, contract, tests, architecture, work log;
- schema change → migration, schema types, tests, rollback, work log;
- environment change → `.env.example`, deployment secret list, runbook;
- release → revision, deployment evidence, test status, release checklist, handoff.
