# Operations Runbook

## Session Start

Record:

```yaml
PROJECT:
MODE:
CURRENT_PHASE:
SESSION_OBJECTIVE:
REPOSITORY:
BRANCH:
STARTING_COMMIT:
DEPLOYED_COMMIT:
KNOWN_BASELINE:
PRIMARY_RISK:
PLANNED_COMPLETION_POINT:
```

Read the latest work log and handoff before changing the project.

---

## Work Updates

Maintain:

```yaml
ACTIVE_TASK:
EVIDENCE_FOUND:
CHANGE_MADE:
VERIFICATION:
NEW_ISSUE:
DECISION:
NEXT_SUBSTEP:
```

Do not flood the log with low-level noise. Record meaningful state changes.

---

## Commit Discipline

Each commit represents one coherent outcome.

Format:

```text
type(scope): result
```

Examples:

```text
feat(auth): add password reset flow
fix(parser): reject mismatched product strains
refactor(api): isolate inventory normalization service
test(pricing): add pack-size regression
docs(workflow): update phase completion state
```

Do not combine unrelated refactors, dependencies, schema changes, and features in one commit.

---

## Work Log

Append after every meaningful session:

```text
Date:
Objective:
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

## Resume Procedure

1. read `HANDOFF.md`;
2. read the latest `WORK_LOG.md` entry;
3. verify branch and commit;
4. verify working tree;
5. verify deployed revision if relevant;
6. run the narrow continuation command;
7. confirm blockers still exist;
8. continue the exact next task.

If reality differs from the handoff, update the handoff before proceeding.

---

## End-of-Session Output

```yaml
COMPLETED:
VERIFIED:
FILES_CHANGED:
MIGRATIONS:
TESTS_RUN:
FAILED_TESTS:
CURRENT_BLOCKER:
NEXT_EXACT_ACTION:
NEXT_THREE_TASKS:
CONTINUATION_COMMANDS:
ENDING_BRANCH:
ENDING_COMMIT:
DEPLOYMENT_STATUS:
ROLLBACK_POINT:
```

---

## Partial Completion

When a session cannot finish:

1. preserve working changes;
2. identify what is actually complete;
3. identify what is unverified;
4. record exact failure;
5. record next executable command;
6. avoid promising background completion;
7. leave rollback or cleanup instructions.

Partial completion is valid when it tells the truth.

---

## Dangerous Change Procedure

Before destructive schema, data, infrastructure, auth, or deployment changes:

1. capture current revision;
2. capture current data or configuration state;
3. define rollback;
4. identify blast radius;
5. test in a non-production environment;
6. verify backups or reversibility;
7. record decision;
8. execute the smallest change;
9. validate immediately;
10. stop on unexplained drift.

---

## Documentation Synchronization

Update documentation in the same task as behavior.

Do not leave:

- stale commands;
- stale environment names;
- stale schema;
- stale architecture;
- stale deployment revision;
- stale next action.

---

## Handoff Standard

The handoff must answer:

- Where is the project?
- Which branch and commit?
- What works?
- What was actually tested?
- What failed?
- What is deployed?
- What is dangerous?
- What is the rollback point?
- What should happen next?
- Which commands continue the work?
