---
name: project-workflow-engine
version: 1.0.0
description: >
  A stable, reusable development workflow that converts an idea, feature request,
  repair job, migration, or existing codebase into an execution-ready project
  system with clear artifacts, phase gates, task ordering, validation, logs,
  recovery rules, and handoff documentation.
triggers:
  - start a project
  - build a new application
  - add a major feature
  - repair or stabilize a broken project
  - migrate or refactor a system
  - continue an unfinished development project
  - prepare a project for another agent or developer
---

# Project Workflow Engine

## 1. Purpose

Use this skill whenever a development project needs to be started, restarted, repaired, expanded, migrated, or handed off.

The goal is not merely to produce a plan. The goal is to create the **best next development workflow**, execute as much of it as the environment allows, and leave behind a stable operating structure that another developer or agent can continue without reconstructing the project from conversation history.

This skill must:

1. Convert vague ideas into explicit requirements.
2. Identify the current state of the project before proposing changes.
3. Produce a dependency-aware execution plan.
4. Separate facts, assumptions, decisions, risks, and unresolved questions.
5. Define measurable phase gates and completion criteria.
6. Create or update durable project artifacts.
7. Keep source code, documentation, tests, and logs synchronized.
8. Prevent repeated debugging loops and untracked changes.
9. Prefer working outputs over endless planning.
10. Produce a clean handoff state after every meaningful work session.

---

# 2. Operating Principles

## 2.1 Source of truth

Every project must define one primary source of truth for each category:

| Category | Required Source of Truth |
|---|---|
| Source code | Repository and branch |
| Requirements | `docs/PROJECT_REQUIREMENTS.md` |
| Architecture | `docs/ARCHITECTURE.md` |
| Current plan | `docs/EXECUTION_PLAN.md` |
| Decisions | `docs/DECISION_LOG.md` |
| Work history | `docs/WORK_LOG.md` |
| Environment variables | `.env.example` and environment documentation |
| Database schema | Migrations or declarative schema files |
| API contract | OpenAPI, typed interfaces, or contract document |
| Test status | Automated test output and `docs/TEST_STATUS.md` |
| Deployment state | Deployment config and release log |

Never allow multiple undocumented competing sources of truth.

## 2.2 Evidence before assumptions

Inspect the existing project before recommending major changes.

Do not assume:

- the repository is empty;
- a dependency is installed;
- a service is connected;
- an environment variable exists;
- the database schema matches documentation;
- a deployment is using the latest commit;
- a test passed because code appears correct;
- a task is complete because files were changed.

When evidence is unavailable, mark the statement as an assumption.

## 2.3 No invisible progress

Every meaningful change must produce at least one of the following:

- changed code;
- changed configuration;
- a test result;
- a migration;
- a durable document update;
- a recorded decision;
- a clearly identified blocker with evidence.

## 2.4 No endless clarification loop

Ask only questions that materially change implementation.

If minor details are missing:

1. make a reasonable assumption;
2. record the assumption;
3. continue;
4. make the assumption easy to reverse.

## 2.5 Finish the smallest complete vertical slice

Prefer a thin end-to-end working path over broad incomplete scaffolding.

A vertical slice should include, where relevant:

- user input;
- validation;
- application logic;
- persistence;
- API or service boundary;
- UI output;
- tests;
- logging;
- documentation.

---

# 3. Input Variables

Create or infer the following variables at project start.

## 3.1 Core project variables

```yaml
PROJECT_NAME: ""
PROJECT_SLUG: ""
PROJECT_TYPE: "web_app | api | worker | cli | library | data_pipeline | mobile | desktop | ai_agent | infrastructure | mixed"
PROJECT_MODE: "new | existing | repair | migration | refactor | feature | audit | handoff"
PROJECT_GOAL: ""
PRIMARY_USER: ""
PRIMARY_OUTCOME: ""
SUCCESS_METRIC: ""
NON_GOALS: []
```

## 3.2 Technical variables

```yaml
REPOSITORY_URL: ""
REPOSITORY_ROOT: "."
DEFAULT_BRANCH: "main"
WORKING_BRANCH: ""
PACKAGE_MANAGER: "npm | pnpm | yarn | bun | pip | uv | poetry | cargo | go | other"
LANGUAGES: []
FRAMEWORKS: []
RUNTIME_VERSIONS: {}
DATABASES: []
EXTERNAL_SERVICES: []
DEPLOYMENT_TARGETS: []
LOCAL_DEV_COMMAND: ""
TEST_COMMAND: ""
BUILD_COMMAND: ""
LINT_COMMAND: ""
TYPECHECK_COMMAND: ""
DEPLOY_COMMAND: ""
```

## 3.3 Constraint variables

```yaml
TIME_CONSTRAINT: ""
BUDGET_CONSTRAINT: ""
PLATFORM_CONSTRAINTS: []
SECURITY_CONSTRAINTS: []
COMPLIANCE_CONSTRAINTS: []
PERFORMANCE_TARGETS: []
COMPATIBILITY_TARGETS: []
DATA_CONSTRAINTS: []
USER_EXPERIENCE_CONSTRAINTS: []
DO_NOT_CHANGE: []
```

## 3.4 Workflow variables

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

## 3.5 State variables

```yaml
CURRENT_PHASE: 0
LAST_KNOWN_WORKING_COMMIT: ""
CURRENT_DEPLOYED_COMMIT: ""
KNOWN_BLOCKERS: []
KNOWN_DEFECTS: []
OPEN_DECISIONS: []
UNVERIFIED_ASSUMPTIONS: []
CURRENT_TEST_STATUS: "unknown"
CURRENT_BUILD_STATUS: "unknown"
CURRENT_DEPLOYMENT_STATUS: "unknown"
```

---

# 4. Variable Resolution Rules

Resolve variables in this order:

1. Explicit user instruction.
2. Existing project configuration.
3. Repository documentation.
4. Deployment configuration.
5. Package manifests and lockfiles.
6. Existing code patterns.
7. Environment documentation.
8. Conservative default.

When sources conflict:

1. identify the conflict;
2. prefer executable configuration over prose;
3. prefer current code over stale documentation;
4. update documentation after confirming the actual behavior;
5. record the decision.

---

# 5. Project Classification

Before execution, classify the project.

## 5.1 Complexity score

Calculate:

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

Interpretation:

| Score | Class | Required Workflow |
|---:|---|---|
| 0–3 | Small | Compact plan, one vertical slice |
| 4–8 | Medium | Full artifacts, phased execution |
| 9–15 | Large | Architecture review, milestones, release gates |
| 16+ | Program | Split into subprojects with separate execution plans |

## 5.2 Risk score

For each risk, assign:

```text
PROBABILITY: 1–5
IMPACT: 1–5
DETECTABILITY: 1–5
RISK_PRIORITY = PROBABILITY × IMPACT × DETECTABILITY
```

Interpretation:

| Score | Response |
|---:|---|
| 1–20 | Track |
| 21–50 | Mitigate during implementation |
| 51–90 | Resolve before release |
| 91–125 | Resolve before implementation continues |

## 5.3 Change type

Label each task as one of:

- `ADD`
- `CHANGE`
- `REMOVE`
- `MIGRATE`
- `REPAIR`
- `VERIFY`
- `DOCUMENT`
- `RELEASE`

This prevents a migration or destructive change from being disguised as a normal feature task.

---

# 6. Required Project Artifacts

Create these files when appropriate. Do not create empty filler documents.

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

For smaller projects, these may be combined into:

```text
docs/PROJECT_SYSTEM.md
```

## 6.1 `PROJECT_CONTEXT.md`

Must include:

- project purpose;
- current state;
- users;
- business or operational objective;
- repository;
- environments;
- integrations;
- known constraints;
- non-goals;
- terminology;
- current blockers.

## 6.2 `PROJECT_REQUIREMENTS.md`

Each requirement must use an identifier:

```text
FR-001  Functional requirement
NFR-001 Non-functional requirement
DATA-001 Data requirement
SEC-001 Security requirement
OPS-001 Operational requirement
UX-001 User experience requirement
```

Each requirement must contain:

```yaml
id: FR-001
title: ""
description: ""
priority: "must | should | could | later"
source: "user | existing behavior | contract | regulation | assumption"
acceptance_criteria: []
dependencies: []
status: "proposed | approved | implemented | verified | rejected"
```

## 6.3 `ARCHITECTURE.md`

Must define:

- system boundaries;
- data flow;
- component responsibilities;
- storage model;
- API boundaries;
- failure handling;
- observability;
- security boundaries;
- deployment topology;
- migration strategy;
- rollback strategy.

## 6.4 `EXECUTION_PLAN.md`

Must include:

- phases;
- task IDs;
- dependencies;
- expected files changed;
- acceptance criteria;
- test requirements;
- rollback method;
- status.

## 6.5 `DECISION_LOG.md`

Use:

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

## 6.6 `WORK_LOG.md`

Append only. Each session entry must include:

```text
Date:
Objective:
Starting state:
Actions completed:
Files changed:
Tests run:
Results:
Decisions:
New risks:
Blockers:
Next exact action:
Ending commit:
```

## 6.7 `HANDOFF.md`

Must allow another developer or agent to continue immediately.

Include:

- current branch and commit;
- what works;
- what is incomplete;
- exact commands;
- environment requirements;
- test status;
- deployment status;
- unresolved decisions;
- next three tasks;
- known dangerous areas;
- rollback point.

---

# 7. Standard Workflow

# Phase 0 — Intake and State Capture

## Objective

Understand what exists, what is wanted, and what cannot be broken.

## Actions

1. Parse the request.
2. Identify project mode.
3. Resolve core variables.
4. Inspect repository structure.
5. Inspect manifests, configuration, migrations, tests, CI, and deployment files.
6. Identify current source-of-truth locations.
7. Record missing evidence.
8. Create a project state snapshot.

## Output

```yaml
PROJECT_MODE:
CURRENT_STATE:
TARGET_STATE:
PRIMARY_GAP:
BLOCKERS:
ASSUMPTIONS:
FIRST_VERTICAL_SLICE:
```

## Exit gate

Do not leave Phase 0 until:

- the project goal is explicit;
- the current state is summarized;
- the first executable milestone is identified;
- destructive risks are known;
- the working repository and branch are identified.

---

# Phase 1 — Requirements and Acceptance Contract

## Objective

Turn the request into testable outcomes.

## Actions

1. Write functional requirements.
2. Write non-functional requirements.
3. Define non-goals.
4. Define acceptance criteria.
5. Identify user-visible behavior.
6. Identify data inputs and outputs.
7. Identify security, performance, reliability, and compatibility constraints.
8. Resolve terminology.

## Acceptance criteria format

Use Given/When/Then where practical:

```text
Given [starting condition]
When [action occurs]
Then [observable result]
And [required side effect or constraint]
```

## Exit gate

- every must-have requirement has acceptance criteria;
- success can be verified without subjective interpretation;
- scope exclusions are explicit;
- unresolved questions are either blocking or safely assumed.

---

# Phase 2 — Architecture and Dependency Map

## Objective

Choose the simplest architecture that satisfies the requirements.

## Actions

1. Map system components.
2. Map data flow.
3. Map external dependencies.
4. Identify trust boundaries.
5. Identify state ownership.
6. Define contracts between components.
7. Identify migration requirements.
8. Identify rollback points.
9. Identify observability requirements.
10. Reject unnecessary infrastructure.

## Architecture decision rule

Choose the option with the lowest:

```text
TOTAL_COST =
  IMPLEMENTATION_COST
  + OPERATING_COST
  + FAILURE_COST
  + MIGRATION_COST
  + COGNITIVE_LOAD
```

Do not optimize only for implementation speed.

## Exit gate

- each component has one clear responsibility;
- every persistent state has an owner;
- every external dependency has failure handling;
- migration and rollback paths exist;
- the first vertical slice is technically possible.

---

# Phase 3 — Execution Plan and Task Graph

## Objective

Create a dependency-aware sequence of small, verifiable tasks.

## Task format

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

## Task sizing

| Size | Expected Scope |
|---|---|
| XS | One file or isolated configuration change |
| S | Small behavior with focused tests |
| M | Multi-file behavior or one complete vertical slice |
| L | Must be split before implementation |

Never implement an `L` task directly.

## Ordering rules

Order tasks by:

1. blocker removal;
2. irreversible risk reduction;
3. architecture skeleton;
4. vertical slice completion;
5. automated validation;
6. secondary features;
7. optimization;
8. cosmetic improvements.

## Exit gate

- no active task is larger than `M`;
- task dependencies form a valid order;
- every implementation task has a test or verification method;
- rollback exists for migrations and destructive changes.

---

# Phase 4 — Environment and Baseline Validation

## Objective

Prove the starting point before changing it.

## Actions

1. Install dependencies using the repository’s package manager.
2. verify runtime versions;
3. verify environment variables without exposing secrets;
4. run lint;
5. run typecheck;
6. run unit tests;
7. run integration tests;
8. run build;
9. run the application locally when possible;
10. record all failures before modifications.

## Baseline status

```yaml
INSTALL: "pass | fail | unavailable"
LINT: "pass | fail | unavailable"
TYPECHECK: "pass | fail | unavailable"
TESTS: "pass | fail | unavailable"
BUILD: "pass | fail | unavailable"
LOCAL_RUN: "pass | fail | unavailable"
KNOWN_PREEXISTING_FAILURES: []
```

## Exit gate

- the pre-change baseline is recorded;
- new failures can be distinguished from old failures;
- required tooling is known;
- secrets are not committed.

---

# Phase 5 — Implementation Loop

Repeat for each task.

## 5.1 Before editing

1. Confirm task objective.
2. Confirm dependencies are complete.
3. Identify files likely to change.
4. Identify regression risk.
5. Identify the fastest proof of correctness.

## 5.2 Implement

1. Make the smallest coherent change.
2. Preserve existing patterns unless they are the problem.
3. Avoid unrelated refactors.
4. Add explicit error handling.
5. Add logging at system boundaries.
6. Keep configuration declarative.
7. Keep secrets out of source.
8. Update types and contracts with behavior changes.
9. Add migrations rather than manual database drift.
10. Add tests in the same task.

## 5.3 Validate

Run the narrowest test first:

```text
changed unit → related module → integration path → full suite → build
```

## 5.4 Record

Update:

- task status;
- work log;
- decisions;
- test status;
- risk register;
- handoff.

## 5.5 Commit discipline

Each commit should represent one coherent outcome.

Recommended format:

```text
type(scope): result

Examples:
feat(auth): add password reset flow
fix(parser): reject mismatched product strains
refactor(api): isolate inventory normalization service
test(pricing): add regression cases for pack-size mismatch
docs(workflow): update phase 3 completion state
```

## Exit gate

A task is not complete until:

- acceptance criteria pass;
- relevant tests pass;
- documentation reflects the change;
- no new unexplained failure exists;
- the work log records the result.

---

# Phase 6 — Integration and Regression

## Objective

Verify that completed tasks work together.

## Required checks

- end-to-end user path;
- API contract compatibility;
- database migration behavior;
- rollback behavior;
- permissions and authorization;
- failure paths;
- duplicate submission behavior;
- idempotency where required;
- concurrency where relevant;
- performance against targets;
- logs and error visibility;
- backward compatibility;
- deployment configuration.

## Regression matrix

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

## Exit gate

- the vertical slice works end to end;
- critical regressions are tested;
- migrations are proven;
- rollback is documented;
- known defects are explicitly accepted or fixed.

---

# Phase 7 — Release Readiness

## Objective

Determine whether the project is safe to deploy.

## Release gate

All must be true unless explicitly waived:

```yaml
REQUIREMENTS_VERIFIED: true
BUILD_PASSING: true
CRITICAL_TESTS_PASSING: true
MIGRATIONS_TESTED: true
ROLLBACK_TESTED: true
SECRETS_CONFIGURED: true
OBSERVABILITY_READY: true
DOCUMENTATION_UPDATED: true
HANDOFF_UPDATED: true
KNOWN_CRITICAL_DEFECTS: 0
```

## Release decision

Use one:

- `GO`
- `GO WITH ACCEPTED RISKS`
- `NO-GO`

Every accepted risk must include an owner and follow-up action.

---

# Phase 8 — Handoff and Continuation State

## Objective

Leave the project easier to continue than it was to start.

## Required final output

```yaml
STATUS: "complete | partial | blocked"
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
```

The final response must clearly distinguish:

- work actually completed;
- work only planned;
- work attempted but failed;
- work blocked by unavailable access;
- assumptions that remain unverified.

---

# 8. Failure Recovery Protocol

Use this whenever implementation stalls.

## 8.1 Classify the failure

Choose one:

- `CODE_DEFECT`
- `CONFIGURATION_ERROR`
- `ENVIRONMENT_MISMATCH`
- `DEPENDENCY_FAILURE`
- `PERMISSION_FAILURE`
- `DATA_CONTRACT_MISMATCH`
- `DEPLOYMENT_DRIFT`
- `MISSING_INFORMATION`
- `TOOL_LIMITATION`
- `EXTERNAL_SERVICE_FAILURE`

## 8.2 Recovery sequence

1. Preserve the current error output.
2. Identify the last known working state.
3. Reproduce the failure with the smallest command.
4. Separate preexisting failure from introduced failure.
5. Inspect configuration and versions.
6. Inspect changed files.
7. Test one hypothesis at a time.
8. Revert speculative changes that did not help.
9. Add a regression test after fixing.
10. Record the root cause.

## 8.3 Root cause record

```yaml
failure_id: FAIL-001
symptom: ""
root_cause: ""
trigger: ""
why_not_detected_earlier: ""
fix: ""
regression_test: ""
prevention: ""
```

## 8.4 Stop-loss rules

Stop repeating the same approach when:

- the same error occurs after two equivalent attempts;
- a fix requires changing unrelated systems;
- evidence contradicts the current hypothesis;
- the environment cannot verify the change;
- required permissions are unavailable.

When a stop-loss triggers, change strategy and document why.

---

# 9. Existing Project Repair Mode

When `PROJECT_MODE = repair`, use this order:

1. Freeze scope.
2. Capture current failures.
3. Identify last known working commit.
4. Compare current branch, deployed branch, and documented state.
5. Verify package manager and lockfile.
6. Verify runtime versions.
7. Verify environment variables.
8. Verify database migrations.
9. Verify external service credentials and endpoints.
10. Reproduce locally.
11. Fix the narrowest root cause.
12. Add regression coverage.
13. Update source-of-truth documents.
14. Only then resume feature development.

Do not add features to an unstable baseline unless the feature itself is the repair.

---

# 10. New Project Bootstrap Mode

When `PROJECT_MODE = new`, produce this minimum structure:

```text
README.md
.env.example
.gitignore
docs/
  PROJECT_CONTEXT.md
  PROJECT_REQUIREMENTS.md
  ARCHITECTURE.md
  EXECUTION_PLAN.md
  DECISION_LOG.md
  WORK_LOG.md
  HANDOFF.md
src/
tests/
```

Also configure, where appropriate:

- formatter;
- linter;
- type checking;
- test runner;
- pre-commit checks;
- CI pipeline;
- preview deployment;
- error reporting;
- structured logging;
- dependency update policy;
- database migration system.

The first implementation milestone must be a working vertical slice, not a decorative homepage or empty component shell unless that is the actual product goal.

---

# 11. Migration Mode

When `PROJECT_MODE = migration`:

1. Document source and destination.
2. Freeze the migration contract.
3. Create a mapping table.
4. Identify incompatible fields.
5. Define default values.
6. Define rejected-record handling.
7. Build dry-run mode.
8. Make the migration resumable.
9. Make writes idempotent.
10. Produce reconciliation totals.
11. Preserve rollback data.
12. Verify before switching traffic.
13. Switch gradually when possible.
14. retain an audit log.

## Migration reconciliation

```yaml
SOURCE_COUNT:
READ_COUNT:
TRANSFORMED_COUNT:
WRITTEN_COUNT:
SKIPPED_COUNT:
REJECTED_COUNT:
DUPLICATE_COUNT:
MISMATCH_COUNT:
ROLLBACK_COUNT:
```

No migration is complete without reconciliation.

---

# 12. Data Pipeline Mode

When `PROJECT_TYPE = data_pipeline`:

Define:

```yaml
SOURCE_SYSTEMS: []
INPUT_FORMATS: []
INGESTION_FREQUENCY: ""
RAW_STORAGE: ""
NORMALIZED_STORAGE: ""
IDENTITY_STRATEGY: ""
DEDUPLICATION_RULES: []
VALIDATION_RULES: []
REJECTION_RULES: []
RETRY_POLICY: ""
IDEMPOTENCY_KEY: ""
LINEAGE_FIELDS: []
REVIEW_QUEUE_RULES: []
OUTPUT_CONTRACTS: []
```

Every transformed record should retain enough lineage to answer:

- where it came from;
- when it was collected;
- which parser version processed it;
- which normalization rules were applied;
- whether it was automatically accepted;
- whether a human reviewed it;
- which source record can reproduce it.

---

# 13. AI-Assisted Development Rules

When an AI agent uses this skill:

1. Inspect before editing.
2. Do not invent file contents.
3. Do not claim tests passed unless executed.
4. Do not claim deployment succeeded unless verified.
5. Do not ask the user to perform a task when the agent has the required access.
6. Do not overwrite unrelated work.
7. Do not expose secrets.
8. Do not silently change architecture.
9. Do not create duplicate documentation systems.
10. Do not leave temporary debug code.
11. Do not stop after generating a plan when execution is possible.
12. Summarize exact changes, tests, failures, and next actions.

## Tool selection priority

Use the most direct authoritative tool:

1. repository tool for repository state;
2. filesystem for local project state;
3. database tool for schema and data state;
4. deployment tool for deployment state;
5. official documentation for current platform behavior;
6. shell or runtime for verification;
7. conversation history only as supporting context.

---

# 14. Standard Session Output

At the beginning of a work session, output:

```text
Project:
Mode:
Current phase:
Session objective:
Known baseline:
Primary risk:
Planned completion point:
```

During work, maintain:

```text
Active task:
Evidence found:
Change made:
Verification:
New issue:
```

At the end, output:

```text
Completed:
Verified:
Files changed:
Tests run:
Current blocker:
Next exact action:
Continuation command:
```

---

# 15. Workflow Output Template

Use this template whenever the user asks to start or continue a project.

## Project Workflow

### 1. Project definition

```yaml
PROJECT_NAME:
PROJECT_MODE:
PROJECT_TYPE:
PROJECT_GOAL:
PRIMARY_OUTCOME:
SUCCESS_METRIC:
NON_GOALS:
```

### 2. Current state

```yaml
REPOSITORY:
BRANCH:
LAST_WORKING_COMMIT:
BUILD_STATUS:
TEST_STATUS:
DEPLOYMENT_STATUS:
KNOWN_BLOCKERS:
```

### 3. Requirements

```text
FR-001:
NFR-001:
DATA-001:
OPS-001:
```

### 4. Architecture

```text
Components:
Data flow:
External services:
Persistence:
Security boundaries:
Failure handling:
Deployment:
Rollback:
```

### 5. Execution phases

```text
Phase 0:
Phase 1:
Phase 2:
Phase 3:
```

### 6. Immediate task graph

```text
TASK-001 → TASK-002 → TASK-003
                  ↘ TASK-004
```

### 7. First vertical slice

```text
Input:
Processing:
Storage:
Output:
Verification:
```

### 8. Risk register

```text
RISK-001:
Probability:
Impact:
Detectability:
Mitigation:
```

### 9. Completion gate

```text
Acceptance criteria:
Tests:
Build:
Migration:
Deployment:
Documentation:
Rollback:
```

### 10. Continuation state

```text
Next action:
Next three tasks:
Required access:
Files to read:
Commands:
```

---

# 16. Quality Gate Checklist

Before declaring a phase complete, verify:

## Requirements

- [ ] Goal is explicit.
- [ ] Primary user is identified.
- [ ] Success is measurable.
- [ ] Non-goals are listed.
- [ ] Acceptance criteria exist.

## Architecture

- [ ] Components have clear ownership.
- [ ] State ownership is explicit.
- [ ] Contracts are documented.
- [ ] Failure modes are handled.
- [ ] Rollback exists.

## Implementation

- [ ] Changes are scoped.
- [ ] Tests were added or updated.
- [ ] Error handling exists.
- [ ] Logs are useful.
- [ ] Secrets are excluded.
- [ ] No unrelated refactor was mixed in.

## Validation

- [ ] Narrow tests pass.
- [ ] Full relevant tests pass.
- [ ] Build passes.
- [ ] User-visible behavior was checked.
- [ ] Regression paths were checked.

## Documentation

- [ ] Requirements reflect reality.
- [ ] Architecture reflects reality.
- [ ] Decisions are recorded.
- [ ] Work log is updated.
- [ ] Handoff is current.

## Release

- [ ] Migration is tested.
- [ ] Rollback is tested.
- [ ] Deployment commit is known.
- [ ] Monitoring exists.
- [ ] Critical defects are zero or accepted.

---

# 17. Anti-Patterns

Reject these behaviors:

- planning without execution when execution is available;
- coding before inspecting the repository;
- creating a second source of truth;
- broad refactoring during a targeted repair;
- changing dependencies without checking compatibility;
- editing production data manually without a migration or audit trail;
- claiming success from static code inspection alone;
- leaving undocumented environment requirements;
- repeating failed fixes without changing the hypothesis;
- allowing tasks to remain too large to verify;
- accepting “works on my machine” without reproducible commands;
- handing off without branch, commit, tests, and next action.

---

# 18. Default Decisions

Use these defaults unless the project requires otherwise:

```yaml
DEFAULT_BRANCH_STRATEGY: "short-lived feature branches"
DEFAULT_TASK_SIZE: "S"
DEFAULT_ARCHITECTURE: "modular monolith"
DEFAULT_API_STYLE: "typed contract-first"
DEFAULT_DATABASE_CHANGE_METHOD: "versioned migrations"
DEFAULT_LOGGING: "structured logs"
DEFAULT_ERROR_HANDLING: "explicit boundary errors"
DEFAULT_TEST_PRIORITY:
  - regression tests for known failures
  - unit tests for deterministic logic
  - integration tests for boundaries
  - end-to-end tests for critical paths
DEFAULT_RELEASE_STRATEGY: "preview then staged production"
DEFAULT_ROLLBACK: "revert code plus reversible migration"
DEFAULT_DOCUMENTATION: "update during the same task"
```

Do not introduce microservices, event buses, graph databases, vector databases, orchestration systems, or additional frameworks without a requirement that justifies their operational cost.

---

# 19. Final Instruction to the Agent

When this skill is activated:

1. Build the project workflow from the variables above.
2. Inspect the actual project state.
3. Create or update the required artifacts.
4. Select the smallest complete vertical slice.
5. Execute tasks in dependency order.
6. Validate every meaningful change.
7. Record decisions and failures.
8. Keep the handoff state current.
9. End with the exact next action.
10. Never leave the project dependent on hidden conversation context.
