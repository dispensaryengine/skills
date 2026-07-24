# Mode Contracts

Apply the common workflow plus the selected mode.

## New Project

1. define primary outcome and non-goals;
2. choose the smallest justified stack;
3. initialize repository and branch;
4. create environment contract;
5. configure formatter, lint, typecheck, tests, and build;
6. configure versioned migrations when persistence exists;
7. create the minimum durable artifacts;
8. implement one complete vertical slice;
9. add CI or reproducible validation;
10. verify local run;
11. create handoff.

Minimum structure:

```text
README.md
.env.example
.gitignore
docs/
src/
tests/
```

Do not make a decorative landing page the first milestone unless that is the product.

---

## Existing Project

1. inspect current branch and repository;
2. identify last known working revision;
3. compare code, documentation, tests, schema, and deployment;
4. capture baseline;
5. identify stale or competing sources of truth;
6. choose the next smallest complete slice;
7. continue without rewriting unrelated architecture.

---

## Feature

1. define user-visible behavior;
2. identify affected boundaries;
3. identify backward compatibility;
4. add acceptance and regression tests;
5. implement the narrowest complete path;
6. avoid unrelated cleanup;
7. verify existing critical paths;
8. update documentation and handoff.

---

## Repair

1. freeze feature scope;
2. capture exact failures;
3. identify last known working revision;
4. compare working, current, and deployed states;
5. verify package manager and lockfile;
6. verify runtimes;
7. verify environment-variable names;
8. verify migrations;
9. verify service endpoints and permissions;
10. reproduce with the smallest command;
11. fix the narrowest root cause;
12. add regression coverage;
13. update source-of-truth artifacts;
14. resume feature work only after baseline stability.

Do not add features to an unstable baseline unless the feature is the repair.

---

## Refactor

1. write the preserved behavior contract;
2. add missing characterization tests;
3. identify public interfaces;
4. define incremental structural changes;
5. avoid changing behavior and structure in the same uncontrolled step;
6. validate after every step;
7. measure performance when relevant;
8. preserve rollback;
9. update architecture after the structure is proven.

---

## Migration

Document:

```yaml
SOURCE:
DESTINATION:
MAPPING:
INCOMPATIBILITIES:
DEFAULTS:
REJECTION_HANDLING:
DRY_RUN:
IDEMPOTENCY:
RESUME_KEY:
AUDIT_LOG:
ROLLBACK:
CUTOVER:
```

Required sequence:

1. freeze migration contract;
2. create field or component mapping;
3. identify incompatible data;
4. define defaults without inventing business facts;
5. build dry-run mode;
6. make execution resumable;
7. make writes idempotent;
8. preserve source lineage;
9. produce reconciliation;
10. validate before cutover;
11. switch gradually where practical;
12. retain rollback data;
13. verify post-cutover state.

Reconciliation:

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

## Data Pipeline

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

Every transformed record must retain enough lineage to determine:

- source;
- collection time;
- parser or transformer version;
- rules applied;
- acceptance state;
- review state;
- source record needed for reproduction.

---

## Audit

1. do not modify by default;
2. inventory claimed and actual state;
3. compare documentation to executable evidence;
4. compare schema to migrations;
5. compare tests to critical behavior;
6. compare repository revision to deployed revision;
7. identify broken references;
8. identify hidden manual steps;
9. identify security and secret risks;
10. classify findings by severity;
11. provide exact repair tasks.

Audit statuses:

```text
CONFIRMED
STALE
CONTRADICTED
UNVERIFIED
MISSING
```

---

## Release

1. identify exact release revision;
2. verify clean build from that revision;
3. run critical tests;
4. verify migrations;
5. verify rollback;
6. verify secrets and environment;
7. verify observability;
8. verify deployment configuration;
9. review defects and risks;
10. issue `GO`, `GO WITH ACCEPTED RISKS`, or `NO-GO`;
11. update release and handoff artifacts.

---

## Handoff

Do not make broad changes.

1. inspect current state;
2. validate branch, commit, tests, and deployment;
3. collect exact commands;
4. identify incomplete work;
5. identify dangerous areas;
6. identify rollback point;
7. define next three dependency-ordered tasks;
8. update durable handoff.
