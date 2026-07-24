# Project Workflow Foundation

This is the authoritative operating foundation for the Project Workflow Engine.

## Purpose

The engine converts an idea, feature request, broken system, migration, or unfinished codebase into an execution-ready and continuation-safe development state.

It must:

1. convert vague goals into explicit requirements;
2. inspect the real project before proposing changes;
3. separate facts, assumptions, decisions, risks, and unresolved questions;
4. produce dependency-aware work;
5. define measurable gates;
6. synchronize code, configuration, tests, schema, deployment state, and documentation;
7. prevent repeated debugging loops;
8. favor complete vertical slices;
9. preserve rollback and recovery paths;
10. leave a durable handoff after every meaningful session.

---

## Operating Principles

### One source of truth per concern

Every project must identify one authoritative location for each concern.

| Concern | Preferred source of truth |
|---|---|
| Source code | Repository, branch, and commit |
| Requirements | `docs/PROJECT_REQUIREMENTS.md` or an existing authoritative equivalent |
| Architecture | `docs/ARCHITECTURE.md` |
| Current execution plan | `docs/EXECUTION_PLAN.md` |
| Decisions | `docs/DECISION_LOG.md` |
| Risks | `docs/RISK_REGISTER.md` |
| Work history | `docs/WORK_LOG.md` |
| Environment contract | `.env.example` plus environment documentation |
| Database schema | Versioned migrations or declarative schema |
| API contract | OpenAPI, schema, generated types, or contract document |
| Test state | Executed automation plus `docs/TEST_STATUS.md` |
| Deployment state | Deployment provider evidence, revision, and release log |
| Continuation state | `docs/HANDOFF.md` |

Do not create a second undocumented authority.

When the project already has an equivalent artifact, update it rather than creating a duplicate.

### Evidence before assumptions

Inspect before editing.

Do not assume:

- the repository is empty;
- the visible branch is the deployed branch;
- the documented architecture matches code;
- a package is installed;
- a runtime version is correct;
- a secret exists;
- a service is connected;
- the database matches migrations;
- the latest commit is deployed;
- a command passed because code looks reasonable;
- a file change completed the task.

Mark unavailable evidence as `unknown` or `unverified`.

### No invisible progress

Every meaningful work unit must produce evidence:

- changed code;
- changed configuration;
- a migration;
- a test result;
- a build result;
- a deployment result;
- a durable document update;
- a decision record;
- a root-cause record;
- a blocker with reproduction evidence.

### No endless clarification loop

Ask only questions whose answers materially alter implementation.

When a minor detail is absent:

1. choose a conservative assumption;
2. record it;
3. keep the implementation reversible;
4. continue.

When the missing fact is destructive, security-sensitive, legally material, or impossible to reverse, treat it as a blocker.

### Smallest complete vertical slice

Prefer one thin working path over broad unfinished scaffolding.

A vertical slice may include:

- user or system input;
- validation;
- application logic;
- persistence;
- API boundary;
- output or UI;
- errors;
- logging;
- tests;
- documentation.

A slice must produce observable value or prove a critical architecture path.

### Execution over ceremonial planning

Planning is only useful when it changes execution.

When tools and access permit implementation, continue past the plan.

When execution is blocked, identify the exact missing capability and leave the smallest executable next step.

---

## Project Variables

### Core variables

```yaml
PROJECT_NAME: ""
PROJECT_SLUG: ""
PROJECT_TYPE: "web_app | api | worker | cli | library | data_pipeline | mobile | desktop | ai_agent | infrastructure | mixed"
PROJECT_MODE: "new | existing | feature | repair | refactor | migration | data_pipeline | audit | release | handoff"
PROJECT_GOAL: ""
PRIMARY_USER: ""
PRIMARY_OUTCOME: ""
SUCCESS_METRIC: ""
NON_GOALS: []
```

### Repository and runtime variables

```yaml
REPOSITORY_URL: ""
REPOSITORY_ROOT: "."
DEFAULT_BRANCH: "main"
WORKING_BRANCH: ""
LAST_KNOWN_WORKING_COMMIT: ""
CURRENT_DEPLOYED_COMMIT: ""
PACKAGE_MANAGER: "npm | pnpm | yarn | bun | pip | uv | poetry | cargo | go | other"
LANGUAGES: []
FRAMEWORKS: []
RUNTIME_VERSIONS: {}
LOCKFILES: []
LOCAL_DEV_COMMAND: ""
TEST_COMMAND: ""
BUILD_COMMAND: ""
LINT_COMMAND: ""
TYPECHECK_COMMAND: ""
DEPLOY_COMMAND: ""
```

### System variables

```yaml
DATABASES: []
EXTERNAL_SERVICES: []
DEPLOYMENT_TARGETS: []
QUEUES: []
STORAGE_SYSTEMS: []
AUTHENTICATION_SYSTEMS: []
OBSERVABILITY_SYSTEMS: []
CI_SYSTEMS: []
```

### Constraint variables

```yaml
TIME_CONSTRAINT: ""
BUDGET_CONSTRAINT: ""
PLATFORM_CONSTRAINTS: []
SECURITY_CONSTRAINTS: []
COMPLIANCE_CONSTRAINTS: []
PERFORMANCE_TARGETS: []
RELIABILITY_TARGETS: []
COMPATIBILITY_TARGETS: []
DATA_CONSTRAINTS: []
USER_EXPERIENCE_CONSTRAINTS: []
DO_NOT_CHANGE: []
```

### Workflow variables

```yaml
AUTONOMY_LEVEL: "plan_only | execute_with_review | execute_freely"
QUESTION_BUDGET: 3
MAX_TASK_SIZE_HOURS: 4
TARGET_VERTICAL_SLICE_HOURS: 8
DOCUMENTATION_LEVEL: "minimal | standard | exhaustive"
TEST_COVERAGE_TARGET: ""
RELEASE_STRATEGY: "manual | preview | staged | continuous"
ROLLBACK_REQUIRED: true
PRESERVE_BACKWARD_COMPATIBILITY: true
```

### Current-state variables

```yaml
CURRENT_PHASE: 0
KNOWN_BLOCKERS: []
KNOWN_DEFECTS: []
OPEN_DECISIONS: []
UNVERIFIED_ASSUMPTIONS: []
CURRENT_INSTALL_STATUS: "unknown"
CURRENT_LINT_STATUS: "unknown"
CURRENT_TYPECHECK_STATUS: "unknown"
CURRENT_TEST_STATUS: "unknown"
CURRENT_BUILD_STATUS: "unknown"
CURRENT_LOCAL_RUN_STATUS: "unknown"
CURRENT_DEPLOYMENT_STATUS: "unknown"
```

---

## Variable Resolution

Resolve in this order:

1. explicit user instruction;
2. executable project configuration;
3. repository state;
4. deployment provider state;
5. migrations and schema state;
6. package manifests and lockfiles;
7. automated tests;
8. current code patterns;
9. repository documentation;
10. conservative default.

When sources conflict:

1. identify the exact conflict;
2. prefer executable evidence over prose;
3. prefer deployed evidence for current production behavior;
4. prefer version-controlled schema over manually described schema;
5. do not silently rewrite history;
6. record the resolution in the decision log;
7. update stale documentation after verification.

---

## Classification

### Complexity score

```text
COMPLEXITY_SCORE =
  UI_SURFACES
  + SERVICE_BOUNDARIES
  + DATABASE_COUNT
  + EXTERNAL_INTEGRATIONS
  + DEPLOYMENT_TARGETS
  + DATA_MIGRATIONS
  + SECURITY_SENSITIVE_AREAS
```

| Score | Class | Workflow |
|---:|---|---|
| 0–3 | Small | Compact artifact set and one vertical slice |
| 4–8 | Medium | Full phased workflow |
| 9–15 | Large | Architecture review, milestones, and release gates |
| 16+ | Program | Split into separately owned subprojects |

A program must not be represented as one giant task list.

### Risk score

```text
RISK_PRIORITY =
  PROBABILITY(1–5)
  × IMPACT(1–5)
  × DETECTABILITY(1–5)
```

| Score | Required response |
|---:|---|
| 1–20 | Track |
| 21–50 | Mitigate during implementation |
| 51–90 | Resolve before release |
| 91–125 | Resolve before implementation continues |

### Change type

Every task uses one:

```text
ADD
CHANGE
REMOVE
MIGRATE
REPAIR
VERIFY
DOCUMENT
RELEASE
```

A destructive migration must not be disguised as an ordinary feature task.

---

## Task Model

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

### Task sizing

| Size | Meaning |
|---|---|
| XS | One isolated file, configuration, test, or documentation change |
| S | Focused behavior with narrow validation |
| M | Multi-file behavior or one vertical slice |
| L | Must be split before execution |

Never execute an `L` task directly.

### Task ordering

Order work by:

1. blocker removal;
2. irreversible-risk reduction;
3. restoration of a known baseline;
4. architecture skeleton;
5. vertical-slice completion;
6. automated validation;
7. secondary behavior;
8. optimization;
9. cosmetics.

---

## Architecture Decision Rule

Prefer the option with the lowest total lifecycle burden:

```text
TOTAL_COST =
  IMPLEMENTATION_COST
  + OPERATING_COST
  + FAILURE_COST
  + MIGRATION_COST
  + COGNITIVE_LOAD
```

Do not optimize only for the fastest initial code.

Default to a modular monolith unless requirements justify greater distribution.

Do not add microservices, event buses, graph databases, vector databases, workflow orchestrators, or frameworks merely because they are available.

---

## Default Decisions

```yaml
DEFAULT_BRANCH_STRATEGY: "short-lived feature branches"
DEFAULT_TASK_SIZE: "S"
DEFAULT_ARCHITECTURE: "modular monolith"
DEFAULT_API_STYLE: "typed contract-first"
DEFAULT_DATABASE_CHANGE_METHOD: "versioned migrations"
DEFAULT_LOGGING: "structured logs"
DEFAULT_ERROR_HANDLING: "explicit boundary errors"
DEFAULT_RELEASE_STRATEGY: "preview then staged production"
DEFAULT_ROLLBACK: "revert code plus reversible migration"
DEFAULT_DOCUMENTATION: "update during the same task"
DEFAULT_TEST_PRIORITY:
  - regression tests for known failures
  - unit tests for deterministic logic
  - integration tests for boundaries
  - end-to-end tests for critical paths
```

Defaults may be replaced by evidence-based project requirements.

---

## Agent Behavior

An agent using this skill must:

1. inspect before editing;
2. preserve unrelated work;
3. avoid inventing file contents;
4. avoid exposing secrets;
5. avoid silent architecture changes;
6. use migrations instead of undocumented database drift;
7. execute available validation;
8. distinguish planned from completed work;
9. record failures and decisions;
10. update handoff during the same session;
11. use the most authoritative available tool;
12. avoid asking the user to perform work the agent can perform directly.

### Tool priority

Use the most direct source:

1. repository tool for repository state;
2. filesystem for local project state;
3. database tool for schema and data;
4. deployment tool for deployed state;
5. runtime or shell for verification;
6. official documentation for current platform behavior;
7. conversation history only as supporting context.

---

## Anti-Patterns

Reject:

- planning without execution when execution is possible;
- coding before inspection;
- duplicate sources of truth;
- broad refactoring during a targeted repair;
- dependency changes without compatibility checks;
- manual production data edits without audit or migration;
- success claims based only on static inspection;
- undocumented environment requirements;
- repeated fixes without a changed hypothesis;
- giant tasks that cannot be verified;
- “works on my machine” without reproducible commands;
- deployments without a known revision;
- migrations without reconciliation;
- handoffs without branch, commit, tests, blockers, and next action;
- temporary debug code left in production paths;
- documentation that describes an architecture the code does not implement.
