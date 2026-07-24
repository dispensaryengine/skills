# Canonical Product Normalization Operations Runbook

## 1. Batch Start

Record:

```yaml
BATCH_ID:
SOURCE_DISPENSARY:
SOURCE_PLATFORM:
SOURCE_FILE_OR_TABLE:
SOURCE_ROW_COUNT:
PARSER_VERSION:
RULESET_VERSION:
STARTED_AT:
```

## 2. Baseline

Before processing:

- verify source file/table readable;
- verify raw staging writable;
- verify alias registries readable;
- verify schemas/migrations current;
- verify golden regression suite;
- verify review queue available;
- verify price index target;
- record preexisting failures.

## 3. Processing Order

Follow `normalization_foundation.md` Section 27 exactly unless an approved decision changes the foundation.

Do not skip raw staging.

Do not generate PEK before brand normalization.

Do not score candidates before hard gates.

## 4. Batch Checkpoints

Checkpoint after:

1. raw ingest;
2. normalized DPL generation;
3. PEK generation;
4. candidate generation;
5. hard gates;
6. decisions;
7. review export;
8. price index update;
9. reconciliation;
10. regression suite.

A failed later phase should not require destructive re-ingest.

## 5. Idempotency

Use stable keys for:

- raw source row;
- normalized DPL;
- batch;
- link;
- review item;
- price index record.

Re-running a batch must not multiply the same source row or link.

## 6. Failure Recovery

### Parser failure

- preserve raw row;
- record parser version;
- create data quality/error record;
- repair deterministic parser;
- add fixture;
- rerun affected rows.

### Schema mismatch

- stop writes;
- inspect migrations;
- do not manually drift production;
- create migration;
- test rollback;
- rerun from checkpoint.

### False-positive match

- unlink if safe;
- create rejected near-match;
- add hard rule or scoped alias rejection;
- add regression fixture;
- identify affected prior links;
- reconcile price index.

### Missing critical data

- keep normalized DPL;
- leave critical field blank;
- send to review;
- do not invent value;
- exclude from automatic link if hard rule requires the field.

### Batch total mismatch

- stop release;
- compare raw, normalized, excluded, bad-source, and duplicate counts;
- resolve unaccounted rows;
- update reconciliation.

## 7. Release Order

```text
development database
→ golden regression
→ sample batch
→ reconciliation
→ review inspection
→ production migration
→ canary batch
→ full batch
→ price index verification
```

## 8. Rollback

Rollback must identify:

- code commit;
- ruleset version;
- parser version;
- migrations;
- affected batch;
- affected links;
- affected MCPs;
- affected price index rows.

Do not delete raw source truth.

## 9. Batch Work Log

After each menu or CSV, record:

- source count;
- brand tally;
- alias additions/changes;
- auto-link count;
- review queue changes;
- provisional MCP count;
- rejected false positives;
- parser impacts;
- hard-blocker impacts;
- data quality flags;
- items needing confirmation;
- tests;
- reconciliation;
- next exact action.

## 10. Handoff

```yaml
CURRENT_BATCH:
LAST_COMPLETED_PHASE:
RAW_ROWS:
NORMALIZED_ROWS:
AUTO_LINKS:
REVIEW_ITEMS:
PROVISIONAL_MCPS:
REJECTED_NEAR_MATCHES:
RULESET_VERSION:
PARSER_VERSION:
TEST_STATUS:
RECONCILIATION:
KNOWN_BLOCKERS:
FILES_OR_TABLES_TO_READ:
NEXT_EXACT_ACTION:
```
