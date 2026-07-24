# Product Normalization Review Contract

## 1. Review Queue Purpose

The review queue exists for uncertainty that cannot safely be resolved automatically.

It is not a dumping ground for parser failures that should be deterministic.

## 2. Review Issue Types

```text
uncertain_match
missing_critical_data
possible_brand_alias
possible_product_alias
category_conflict
form_conflict
size_conflict
extract_conflict
infusion_conflict
hardware_conflict
ratio_conflict
dominance_conflict
bad_source_data
possible_duplicate
```

## 3. Review Decisions

```text
approve_match
reject_match
approve_brand_alias
reject_brand_alias
approve_product_alias
reject_product_alias
create_new_mcp
exclude_non_cannabis
mark_bad_source_data
defer
```

## 4. Required Decision Record

```yaml
REVIEW_ID:
DPL_ID:
CANDIDATE_MCP_ID:
ISSUE_TYPE:
EVIDENCE:
DECISION:
REVIEWER:
DECIDED_AT:
CONFIDENCE:
ALIAS_SCOPE:
RULE_LEARNED:
REGRESSION_FIXTURE_ID:
NOTES:
```

## 5. Alias Scope

Brand aliases may be global when approved.

Product, strain, flavor, and line aliases should normally be scoped by:

- brand;
- category;
- form;
- or another identity boundary.

Do not make a dangerous product alias global merely because it matched once.

## 6. Rejection Learning

A rejected near-match must preserve:

- both DPL/MCP identities;
- why they looked similar;
- why they differ;
- hard gate or learned rule;
- reviewer;
- confidence;
- timestamp.

The same rejected pair or equivalent rule must not return as an automatic match after the next run.

## 7. Batch Review Summary

After review, report:

```yaml
ITEMS_REVIEWED:
MATCHES_APPROVED:
MATCHES_REJECTED:
BRAND_ALIASES_APPROVED:
BRAND_ALIASES_REJECTED:
PRODUCT_ALIASES_APPROVED:
PRODUCT_ALIASES_REJECTED:
NEW_MCPS:
EXCLUSIONS:
BAD_SOURCE:
RULES_ADDED:
REGRESSION_FIXTURES_ADDED:
ITEMS_REMAINING:
```

## 8. Final Rule

Review decisions must improve future behavior.

A human decision that disappears after the current batch is a broken learning system.
