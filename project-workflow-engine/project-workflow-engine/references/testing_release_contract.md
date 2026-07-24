# Testing and Release Contract

Configuration and code inspection are not proof.

## Baseline

Before implementation, record:

```yaml
REVISION:
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
PREEXISTING_FAILURES: []
```

Use:

```text
pass
fail
unavailable
not_applicable
```

Do not convert `unavailable` into `pass`.

---

## Validation Ladder

Run the narrowest useful proof first:

1. changed function or unit;
2. related module;
3. boundary integration;
4. critical end-to-end path;
5. relevant full suite;
6. build;
7. local runtime;
8. preview or staged deployment;
9. production verification.

A later broad pass does not remove the value of a narrow regression test.

---

## Regression Contract

For each critical feature:

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
OBSERVABILITY:
```

Test only relevant dimensions, but document why omitted dimensions are not applicable.

---

## Migration Validation

Verify:

- dry-run output;
- source count;
- transformed count;
- written count;
- rejected count;
- duplicate count;
- mismatch count;
- idempotent rerun;
- resume behavior;
- rollback behavior;
- post-migration reads;
- compatibility with old clients where required.

---

## Deployment Validation

A deployment is verified only when:

- target environment is known;
- deployed revision is known;
- revision matches intended release;
- health or smoke check passes;
- critical configuration is present;
- migration state is known;
- logs or monitoring show no immediate critical failure.

“Deployment command succeeded” is not sufficient by itself.

---

## Rollback Contract

For every destructive or production-impacting change, define:

```yaml
ROLLBACK_TRIGGER:
CODE_ROLLBACK:
SCHEMA_ROLLBACK:
DATA_RECOVERY:
CONFIG_ROLLBACK:
TRAFFIC_ROLLBACK:
VERIFICATION:
OWNER:
```

A rollback that cannot restore data must state that limitation before release.

---

## Release Gate

All must be true or explicitly waived:

```yaml
RELEASE_REVISION_IDENTIFIED: true
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

Allowed decisions:

```text
GO
GO WITH ACCEPTED RISKS
NO-GO
```

An accepted risk includes:

```yaml
RISK:
OWNER:
IMPACT:
MITIGATION:
FOLLOW_UP:
DUE_POINT:
```

---

## Quality Checklist

### Requirements

- goal explicit;
- primary user identified;
- success measurable;
- non-goals listed;
- acceptance criteria present.

### Architecture

- responsibilities clear;
- state ownership explicit;
- contracts documented;
- failure paths handled;
- rollback defined.

### Implementation

- change scoped;
- tests updated;
- errors handled;
- logs useful;
- secrets excluded;
- unrelated refactors excluded.

### Validation

- narrow tests executed;
- relevant broad tests executed;
- build executed;
- user-visible behavior checked;
- regression paths checked;
- introduced failures explained.

### Documentation

- requirements match reality;
- architecture matches reality;
- decisions recorded;
- work log updated;
- handoff current.

### Release

- migration tested;
- rollback tested;
- deployed revision known;
- monitoring available;
- critical defects zero or formally accepted.

---

## No-Go Conditions

Issue `NO-GO` when:

- intended revision is unknown;
- critical tests fail without accepted waiver;
- migration has no reconciliation;
- destructive change has no viable rollback or declared limitation;
- secrets are missing or exposed;
- production behavior cannot be observed;
- a critical security boundary is unverified;
- deployed revision differs unexpectedly;
- known critical defects remain unowned.
