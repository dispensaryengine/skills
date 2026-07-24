# Failure Recovery Contract

Use this contract whenever implementation, validation, migration, or deployment stalls.

## Failure Classification

Choose one primary class:

```text
CODE_DEFECT
CONFIGURATION_ERROR
ENVIRONMENT_MISMATCH
DEPENDENCY_FAILURE
PERMISSION_FAILURE
DATA_CONTRACT_MISMATCH
DATABASE_DRIFT
DEPLOYMENT_DRIFT
MISSING_INFORMATION
TOOL_LIMITATION
EXTERNAL_SERVICE_FAILURE
NETWORK_FAILURE
SECURITY_BOUNDARY_FAILURE
BUDGET_OR_QUOTA_FAILURE
```

Do not call every failure a code defect.

---

## Recovery Sequence

1. preserve exact error output;
2. record revision and environment;
3. identify last known working state;
4. reproduce with the smallest command;
5. separate preexisting from introduced failure;
6. inspect versions and configuration;
7. inspect the narrow changed path;
8. define one falsifiable hypothesis;
9. test one hypothesis at a time;
10. revert speculative changes that do not help;
11. change strategy after stop-loss;
12. add regression coverage after the fix;
13. record root cause and prevention;
14. update handoff.

---

## Root-Cause Record

```yaml
failure_id: FAIL-001
symptom: ""
classification: ""
environment: ""
revision: ""
root_cause: ""
trigger: ""
why_not_detected_earlier: ""
fix: ""
regression_test: ""
prevention: ""
status: "open | mitigated | resolved | accepted"
```

---

## Stop-Loss Rules

Stop repeating an approach when:

- the same error remains after two equivalent attempts;
- the proposed fix requires unrelated system changes;
- evidence contradicts the hypothesis;
- no new evidence was produced;
- the environment cannot verify the change;
- permissions are unavailable;
- the action would be destructive without rollback;
- cost or quota would be consumed without a changed strategy.

After stop-loss:

1. preserve the evidence;
2. state why the approach failed;
3. choose a materially different strategy;
4. reduce the reproduction further;
5. isolate the blocker.

---

## Blocker Contract

```yaml
BLOCKER_ID:
CLASSIFICATION:
EXACT_FAILURE:
REPRODUCTION_COMMAND:
ENVIRONMENT:
REVISION:
REQUIRED_CAPABILITY:
AVAILABLE_ALTERNATIVE:
WORK_COMPLETED_AROUND_BLOCKER:
NEXT_ACTION:
```

Do not write “blocked” without the exact missing capability.

---

## Environment Mismatch

Check:

- runtime version;
- package manager;
- lockfile;
- native dependencies;
- environment-variable names;
- filesystem permissions;
- network access;
- OS or architecture;
- database endpoint;
- service credentials;
- CI versus local differences.

Record the mismatch rather than patching around it invisibly.

---

## Dependency Failure

1. verify package name and version;
2. verify lockfile consistency;
3. inspect official compatibility requirements;
4. reproduce installation independently;
5. avoid random upgrades;
6. identify the narrowest compatible change;
7. update dependency documentation;
8. rerun build and tests.

---

## Database Drift

1. inspect migrations;
2. inspect actual schema;
3. compare checksums or version table;
4. identify manual changes;
5. preserve production data;
6. create a forward migration where possible;
7. test dry run;
8. reconcile;
9. update schema authority.

---

## Deployment Drift

1. identify repository revision;
2. identify intended revision;
3. identify deployed revision;
4. inspect deployment configuration;
5. inspect build source;
6. inspect environment;
7. verify health;
8. correct drift through the normal deployment path;
9. record release evidence.

---

## Permission Failure

Do not disguise missing access as a code problem.

Record:

- operation attempted;
- account or role used;
- required permission;
- current permission evidence;
- safe work that can continue;
- exact action needed to unblock.

---

## External-Service Failure

Use bounded retry only for transient failures.

Do not retry indefinitely on:

- invalid credentials;
- permanent authorization failure;
- invalid request;
- missing resource;
- incompatible contract;
- exhausted budget;
- explicit account suspension.

Use circuit breaking when repeated external failures would consume resources or damage the target system.
