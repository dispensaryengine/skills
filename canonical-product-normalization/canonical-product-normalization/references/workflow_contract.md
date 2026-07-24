# Canonical Product Normalization Workflow Contract

## 1. Inspect the Current System

Identify:

- raw source schema;
- normalized schema;
- MCP schema;
- PEK generation;
- brand aliases;
- product aliases;
- hard blockers;
- scoring;
- review queue;
- rejected near-matches;
- quality flags;
- price index;
- tests;
- batch state.

Distinguish implemented behavior from documentation.

---

## 2. Preserve Raw Source Truth

Every source row enters raw staging without destructive cleanup.

Preserve:

- source identifier;
- dispensary;
- platform;
- raw title;
- raw brand;
- raw category;
- raw size and potency;
- price;
- URLs;
- image;
- description;
- raw payload;
- batch;
- first and last seen.

---

## 3. Apply Eligibility

Classify before cannabis MCP matching.

Excluded rows remain traceable but do not:

- generate cannabis PEKs;
- generate cannabis MCPs;
- enter cannabis review;
- teach cannabis aliases;
- enter cannabis price comparison.

---

## 4. Normalize Category and Form

Use minimized top-level categories.

Preserve exact detail in:

- form;
- subform;
- extract;
- infusion;
- hardware;
- size;
- count;
- mg;
- profile;
- ratio;
- product name.

Foundation examples:

```text
Hash Hole → Pre-Rolls
Blunt → Pre-Rolls
AIO → Vapes
Beverage → Edibles
RSO → Concentrates
```

---

## 5. Normalize Brand

Order:

```text
format cleanup
→ approved alias
→ justified title-prefix extraction
→ review when uncertain
```

Brand normalization occurs before PEK generation.

Rejected aliases remain rejected.

---

## 6. Extract Product Identity

Extract:

- product name;
- strain;
- flavor;
- product line;
- size;
- count;
- package and serving mg;
- cannabinoid profile;
- ratio;
- extract;
- infusion;
- hardware;
- supporting dominance/type.

Remove already-extracted structural terms from normalized product name.

Do not remove actual identity words.

---

## 7. Generate Normalized DPL

The normalized DPL is a cleaned store-level sighting.

It is not the product truth object.

Record extraction confidence, comparison status, and source notes.

---

## 8. Generate PEK

Only eligible cannabis rows receive cannabis PEKs.

Use category-specific structures from the foundation.

Blank fields stay blank.

Do not invent facts to complete a key.

---

## 9. Retrieve Candidates

Search existing MCPs using:

- exact PEK;
- approved aliases;
- scoped normalized fields;
- compatible retrieval signals.

Candidate retrieval may be fuzzy.

Final automatic matching may not violate hard gates.

---

## 10. Apply Hard Gates

Apply all ten foundation gates before scoring.

Block or review conflicts in:

- eligibility;
- brand;
- category;
- form;
- size/count/mg;
- product/strain/flavor;
- extract;
- infusion;
- hardware;
- ratio/profile.

---

## 11. Score Compatible Candidates

Use approved confidence bands.

Record match reasons.

A number without evidence is not enough.

---

## 12. Decide

Choose:

```text
auto-link
attach and review
candidate only
provisional MCP
excluded
bad source data
```

Create a provisional MCP rather than forcing an unsafe merge.

---

## 13. Preserve Review Learning

Store:

- approved aliases;
- rejected aliases;
- rejected near-matches;
- rule learned;
- example DPL IDs;
- reviewer;
- timestamp;
- confidence;
- scope.

A rejection is durable system knowledge.

---

## 14. Update Price Comparison

A row enters the price index only when:

- eligible;
- linked to valid MCP;
- usable price;
- active or in stock when available.

Store-specific price and availability remain volatile.

MCP identity remains stable.

---

## 15. Validate

Run:

- parser fixtures;
- category/form tests;
- size and mg tests;
- alias tests;
- PEK tests;
- hard-gate tests;
- false-positive regressions;
- duplicate tests;
- review transition tests;
- price-index tests;
- batch reconciliation.

---

## 16. Update Batch State

After each menu or CSV, record:

- source totals;
- eligible/excluded totals;
- brand tallies;
- alias changes;
- auto-links;
- review changes;
- provisional MCPs;
- rejected false positives;
- parser and hard-blocker impacts;
- quality flags;
- confirmation items;
- regression result.

---

## 17. Produce Handoff

```yaml
STATUS:
BATCH:
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
BLOCKERS:
NEXT_ACTION:
```
