# Workflow Contract

Follow these phases in order unless a mode contract explicitly requires an earlier repair or safety gate.

## Phase 0 — Intake and State Capture

### Objective

Understand what exists, what is wanted, and what cannot be broken.

### Actions

1. parse the request;
2. classify project mode and type;
3. resolve core variables;
4. identify repository, branch, and commit;
5. inspect repository structure;
6. inspect manifests and lockfiles;
7. inspect configuration and environment examples;
8. inspect migrations and schema declarations;
9. inspect tests, CI, and deployment files;
10. inspect durable project documentation;
11. identify authoritative sources;
12. identify conflicts and missing evidence;
13. capture blockers, assumptions, and defects;
14. identify the first executable milestone.

### Output

```yaml
PROJECT_MODE:
PROJECT_TYPE:
CURRENT_STATE:
TARGET_STATE:
PRIMARY_GAP:
SOURCE_OF_TRUTH:
CONFLICTS:
BLOCKERS:
ASSUMPTIONS:
FIRST_VERTICAL_SLICE:
```

### Exit gate

- project goal is explicit;
- actual state is summarized;
- repository and branch are known or explicitly unavailable;
- destructive risks are identified;
- first vertical slice is identified;
- assumptions are visible.

---

## Phase 1 — Requirements and Acceptance Contract

### Objective

Convert intent into observable outcomes.

### Actions

1. write functional requirements;
2. write non-functional requirements;
3. define non-goals;
4. identify user-visible behavior;
5. identify data inputs and outputs;
6. identify security constraints;
7. identify performance and reliability targets;
8. identify backward-compatibility obligations;
9. define acceptance criteria;
10. resolve terminology.

### Requirement IDs

```text
FR-001
NFR-001
DATA-001
SEC-001
OPS-001
UX-001
```

### Acceptance format

```text
Given [starting condition]
When [action]
Then [observable outcome]
And [required side effect or constraint]
```

### Exit gate

- every must requirement has acceptance criteria;
- success is objectively verifiable;
- scope exclusions are explicit;
- unresolved items are blockers or safely recorded assumptions.

---

## Phase 2 — Architecture and Dependency Map

### Objective

Choose the simplest system that satisfies the acceptance contract.

### Actions

1. map components and responsibilities;
2. map user and data flows;
3. identify state ownership;
4. identify service boundaries;
5. identify API and event contracts;
6. identify trust boundaries;
7. identify external dependencies;
8. define external-failure behavior;
9. identify migrations;
10. identify observability;
11. identify deployment topology;
12. define rollback points;
13. reject unnecessary infrastructure.

### Exit gate

- each component has one clear responsibility;
- persistent state has an owner;
- external dependencies have failure behavior;
- contracts are explicit;
- migration and rollback paths exist where required;
- vertical slice is technically possible.

---

## Phase 3 — Execution Plan and Task Graph

### Objective

Create dependency-aware, verifiable work.

### Actions

1. convert requirements into tasks;
2. assign task type;
3. assign dependencies;
4. identify expected files;
5. define acceptance;
6. define tests;
7. define rollback;
8. score risk;
9. split all large tasks;
10. order by blockers and irreversible risk;
11. identify the first complete slice.

### Exit gate

- no executable task is size `L`;
- dependencies form a valid order;
- every implementation task has verification;
- destructive tasks have rollback;
- the next action is exact.

---

## Phase 4 — Environment and Baseline Validation

### Objective

Prove the starting point before changing it.

### Actions

1. verify package manager;
2. verify lockfile;
3. install dependencies;
4. verify runtime versions;
5. verify required environment-variable names without exposing values;
6. run lint;
7. run typecheck;
8. run unit tests;
9. run integration tests;
10. run build;
11. run the application locally when possible;
12. inspect current deployment revision;
13. record all preexisting failures.

### Baseline record

```yaml
INSTALL: "pass | fail | unavailable"
LINT: "pass | fail | unavailable"
TYPECHECK: "pass | fail | unavailable"
UNIT_TESTS: "pass | fail | unavailable"
INTEGRATION_TESTS: "pass | fail | unavailable"
BUILD: "pass | fail | unavailable"
LOCAL_RUN: "pass | fail | unavailable"
DEPLOYED_REVISION: ""
PREEXISTING_FAILURES: []
```

### Exit gate

- pre-change state is recorded;
- introduced failures can be distinguished;
- required tooling is known;
- secrets are not committed.

---

## Phase 5 — Implementation Loop

Repeat per task.

### Before editing

1. confirm objective;
2. confirm dependencies;
3. identify likely files;
4. identify regression risk;
5. identify fastest proof;
6. identify rollback.

### Implement

1. make the smallest coherent change;
2. preserve project patterns unless they are the defect;
3. avoid unrelated refactors;
4. add boundary error handling;
5. add useful logging;
6. keep configuration declarative;
7. keep secrets outside source;
8. synchronize types and contracts;
9. use migrations for database changes;
10. add tests in the same task;
11. update relevant documentation.

### Validate

Run from narrow to broad:

```text
changed unit
→ related module
→ integration boundary
→ critical end-to-end path
→ relevant full suite
→ build
```

### Record

Update:

- task status;
- test status;
- work log;
- decisions;
- risks;
- handoff.

### Task exit gate

- acceptance criteria pass;
- relevant tests pass or failures are explained;
- documentation reflects reality;
- no new unexplained failure exists;
- rollback remains possible where required;
- work log records the result.

---

## Phase 6 — Integration and Regression

### Objective

Prove completed tasks work together.

### Required checks

- end-to-end critical path;
- API compatibility;
- database migration;
- rollback;
- authorization;
- error paths;
- duplicate requests;
- idempotency;
- concurrency;
- external-service failure;
- performance targets;
- logs and error visibility;
- backward compatibility;
- deployment configuration.

### Regression matrix

```yaml
FEATURE:
HAPPY_PATH:
INVALID_INPUT:
MISSING_DEPENDENCY:
EXTERNAL_SERVICE_FAILURE:
DUPLICATE_REQUEST:
RETRY_BEHAVIOR:
PERMISSION_FAILURE:
DATA_ROLLBACK:
LEGACY_COMPATIBILITY:
```

### Exit gate

- vertical slice works end to end;
- critical regressions are covered;
- migrations and rollback are proven;
- known defects are fixed or explicitly accepted.

---

## Phase 7 — Release Readiness

### Objective

Determine whether one exact revision is safe to deploy.

### Required checks

Use `references/testing_release_contract.md`.

Record one decision:

```text
GO
GO WITH ACCEPTED RISKS
NO-GO
```

Every accepted risk requires an owner, mitigation, and follow-up.

### Exit gate

- release revision is exact;
- tests and build are associated with that revision;
- migration and rollback are ready;
- secrets and observability are ready;
- handoff and release record are updated.

---

## Phase 8 — Handoff and Continuation

### Objective

Leave the project easier to continue than it was to start.

### Required state

```yaml
STATUS:
MODE:
CURRENT_PHASE:
WORKING_BRANCH:
WORKING_COMMIT:
DEPLOYED_COMMIT:
COMPLETED:
VERIFIED:
NOT_COMPLETED:
BLOCKERS:
KNOWN_RISKS:
NEXT_ACTION:
NEXT_THREE_TASKS:
COMMANDS_TO_CONTINUE:
FILES_TO_READ_FIRST:
ROLLBACK_POINT:
```

### Exit gate

Another developer or agent can continue without reconstructing the project from chat history.
