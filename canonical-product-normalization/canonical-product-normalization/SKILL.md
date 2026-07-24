---
name: canonical-product-normalization
description: Design, implement, audit, document, and operate a Master Canonical Product system that transforms messy multi-source product listings into normalized Dispensary Product Listings, Product Equality Keys, exact Master Canonical Products, review decisions, rejected near-matches, and a price comparison index. Use for cannabis menu normalization, product title parsing, brand and product aliases, cross-store deduplication, hard-rule matching, PEK/MCP workflows, normalization regression testing, or equivalent multi-source product identity systems.
---

# Canonical Product Normalization

Build and operate a product identity system that preserves exact sellable-product differences while minimizing shopper-facing categories.

## Primary Reference

Read `references/normalization_foundation.md` first for cannabis implementations.

It is the authoritative operational specification for:

- DPL, MCP, and PEK definitions;
- raw and normalized schemas;
- the 23-step processing order;
- cannabis eligibility;
- category, form, subform, size, mg, extract, infusion, and hardware rules;
- brand and product alias systems;
- hard-rule gates;
- confidence bands;
- review queues;
- rejected near-matches;
- data quality flags;
- price comparison indexing;
- resolved foundation decisions.

## Supporting References

Read only what the task requires:

- `references/workflow_contract.md` — operational implementation and batch sequence
- `references/structure_contract.md` — formal documentation sequence
- `references/style_contract.md` — formal PDF/DOCX visual output only
- `references/testing_contract.md` — parser, matching, regression, and release validation
- `references/review_contract.md` — review queue, approvals, rejections, and learning
- `references/operations_runbook.md` — batch processing, work logs, recovery, and handoff
- `templates/normalization_config.yaml` — implementation configuration starter
- `templates/batch_work_log.md` — batch update starter

## Core Principle

**Minimize shopper categories. Preserve exact product differences inside PEK fields.**

The pipeline begins with untouched source truth and ends with:

```text
auto-link
attach and review
candidate only
provisional MCP
excluded non-cannabis
bad source data
```

## Operating Modes

```yaml
NORMALIZATION_MODE: "implement | process_batch | review | repair | audit | document | migrate"
PRODUCT_DOMAIN: "cannabis | other"
OUTPUT_MODE: "code | database | markdown | pdf | docx | mixed"
```

### Implement

Build or extend normalization code, schemas, registries, review systems, or matching logic.

### Process Batch

Process one or more menus while preserving reconciliation and a batch work log.

### Review

Resolve candidate matches, aliases, missing data, false positives, and quality flags.

### Repair

Diagnose parser, schema, rule, alias, matching, or index failures.

### Audit

Compare actual behavior against the foundation without silently changing rules.

### Document

Generate system documentation. Load the style contract only for a formal styled artifact.

### Migrate

Move legacy product data into the DPL/PEK/MCP model with reconciliation and rollback.

## Required Inputs

Resolve:

```yaml
SOURCE_DISPENSARIES: []
SOURCE_PLATFORMS: []
INPUT_FILES_OR_TABLES: []
TARGET_DATABASE: ""
CURRENT_SCHEMAS: []
CURRENT_PARSER_VERSION: ""
CURRENT_RULESET_VERSION: ""
BRAND_ALIAS_SOURCE: ""
PRODUCT_ALIAS_SOURCE: ""
GOLDEN_DATASET: ""
REVIEW_QUEUE_LOCATION: ""
PRICE_INDEX_LOCATION: ""
```

Inspect existing sources first.

Do not fabricate missing brand, size, mg, count, strain, flavor, extract, infusion, hardware, ratio, or cannabinoid facts.

## Reference Routing

### Every cannabis task

Read `references/normalization_foundation.md`.

### Implementation, batch processing, repair, migration, or release

Also read:

- `references/workflow_contract.md`
- `references/testing_contract.md`
- `references/operations_runbook.md`

### Human review or alias learning

Also read `references/review_contract.md`.

### Formal system document

Also read:

- `references/structure_contract.md`
- `references/style_contract.md`

### Non-cannabis domain

Reuse the object model and workflow, but explicitly replace cannabis-specific categories and rules.

Do not silently apply cannabis or New York edible rules to another domain.

## Workflow

Follow `references/workflow_contract.md`.

Required sequence:

1. inspect current schemas, code, registries, tests, and batch state;
2. preserve raw source truth;
3. apply cannabis eligibility before matching;
4. normalize category, form, and identity fields;
5. normalize brand before PEK;
6. generate normalized DPL;
7. generate source-supported PEK;
8. retrieve candidates;
9. apply hard gates before scoring;
10. decide link, review, provisional MCP, exclusion, or bad source;
11. preserve approvals and rejections as learning;
12. update price comparison only for valid links;
13. run regression and reconciliation;
14. update work log and handoff.

False positives are worse than missed matches.

A high similarity score cannot override a hard-gate conflict.

## Required Outputs

Depending on mode:

- code and migrations;
- normalized rows;
- PEKs and MCP links;
- review exports;
- rejected near-matches;
- alias updates;
- regression fixtures;
- price index changes;
- reconciliation;
- batch work log;
- formal documentation;
- exact handoff state.

Do not default to PDF when the request is implementation work.

## Validation

Use `references/testing_contract.md`.

At minimum verify:

- cleaning and parsing;
- eligibility;
- category/form mapping;
- size/count/mg extraction;
- alias behavior;
- deterministic PEK;
- all hard gates;
- permanent false-positive regressions;
- review state transitions;
- price-index eligibility;
- batch reconciliation.

## Batch Update Contract

After every menu or CSV, report:

```yaml
SOURCE_ROWS:
ELIGIBLE:
EXCLUDED:
BRAND_TALLIES:
NEW_ALIASES:
CHANGED_ALIASES:
AUTO_LINKS:
REVIEW_QUEUE_CHANGES:
PROVISIONAL_MCPS:
REJECTED_FALSE_POSITIVES:
PARSER_RULE_IMPACTS:
HARD_BLOCKER_IMPACTS:
DATA_QUALITY_FLAGS:
ITEMS_NEEDING_CONFIRMATION:
TEST_STATUS:
RECONCILIATION:
```

## Handoff

Return:

```yaml
STATUS: "complete | partial | blocked"
BATCH:
SOURCE_ROWS:
NORMALIZED_ROWS:
ELIGIBLE:
EXCLUDED:
AUTO_LINKED:
REVIEW_QUEUE:
PROVISIONAL_MCPS:
REJECTED_NEAR_MATCHES:
NEW_ALIASES:
RULE_CHANGES:
TESTS:
RECONCILIATION:
BLOCKERS:
NEXT_ACTION:
```

## Completion Gate

```yaml
RAW_SOURCE_PRESERVED: true
ELIGIBILITY_APPLIED: true
BRAND_NORMALIZED_BEFORE_PEK: true
PEK_FIELDS_SOURCE_SUPPORTED: true
HARD_GATES_APPLIED: true
MATCH_REASONS_RECORDED: true
REJECTIONS_PRESERVED: true
PRICE_INDEX_ELIGIBILITY_VERIFIED: true
REGRESSION_TESTS_PASSING: true
BATCH_RECONCILED: true
WORK_LOG_UPDATED: true
HANDOFF_UPDATED: true
```

## Final Instruction

Never force two listings into one MCP because their titles look similar.

Same brand and form are not enough when strain, size, count, extract, infusion, hardware, mg, profile, or ratio differs.
