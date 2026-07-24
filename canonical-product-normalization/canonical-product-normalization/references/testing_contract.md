# Canonical Product Normalization Testing Contract

## 1. Purpose

Prove that normalization improves consistency without collapsing different sellable products.

False-positive prevention is release-critical.

---

## 2. Test Layers

```text
text cleaning
→ field parsing
→ normalized DPL
→ PEK
→ candidate retrieval
→ hard gates
→ scoring
→ decision
→ link/review/provisional MCP
→ price index
```

---

## 3. Fixture Contract

Every fixture should contain:

```yaml
fixture_id:
source_dispensary:
source_platform:
raw_title:
raw_brand:
raw_category:
raw_size:
raw_potency:
description:
expected:
  comparison_status:
  normalized_brand:
  normalized_category:
  normalized_form:
  subform:
  normalized_product_name:
  normalized_size:
  count:
  package_thc_mg:
  serving_thc_mg:
  cannabinoid_profile:
  ratio:
  extract_type:
  infusion_type:
  hardware_type:
  proposed_pek:
notes:
```

Blank expected fields must be explicit.

---

## 4. Cleaning Tests

Test:

- whitespace collapse;
- apostrophe normalization;
- dash normalization;
- Unicode normalization;
- decorative label removal;
- display case preservation;
- search text normalization.

Do not remove identity words that happen to resemble menu labels.

---

## 5. Eligibility Tests

Required:

- flower remains eligible;
- accessory remains stored but excluded;
- merchandise remains stored but excluded;
- non-cannabis device does not generate PEK;
- excluded listing does not enter review queue;
- excluded listing does not teach aliases;
- uncertain cannabis listing enters needs-review state.

---

## 6. Category and Form Tests

Required mappings:

```text
Hash Hole → Pre-Rolls / Pre-Roll / Hash Hole
Blunt → Pre-Rolls / Pre-Roll / Blunt
AIO → Vapes / Disposable Vape / AIO
Beverage → Edibles / Beverage
Capsule → Edibles / Capsule
RSO syringe → Concentrates / Concentrate / RSO
Loose moonrock → Flower
Moonrock pre-roll → Pre-Rolls
```

Required conflicts:

```text
Flower != Concentrates
Vape Cartridge != Disposable
Vape Pod != Cartridge
Gummy != Beverage
```

---

## 7. Brand Tests

Test:

- safe formatting normalization;
- approved alias;
- rejected alias;
- uncertain brand-line relationship;
- missing brand with known title prefix;
- missing brand with unsafe prefix;
- brand normalization before PEK;
- alias provenance.

---

## 8. Product Name Tests

Ensure normalized product name excludes:

- brand;
- size;
- count;
- form;
- category;
- extract;
- infusion;
- hardware;
- potency;
- sale decoration.

Ensure it preserves:

- strain;
- flavor;
- line;
- SKU;
- collab identity.

---

## 9. Size and Count Tests

Required:

```text
.5g → 0.5g
half gram → 0.5g
eighth → 3.5g
quarter → 7g
half ounce → 14g
ounce → 28g
5pk × 0.5g → count 5, unit 0.5g, total 2.5g
5pk without weight → count 5, size blank
```

Test malformed source artifacts such as 20.5g or 30.5g using data quality flags rather than silent correction unless a deterministic rule exists.

---

## 10. Edible Tests

Required:

```text
10 × 10mg → package 100mg, serving 10mg, count 10
10pk 100mg → package 100mg, count 10
5mg single beverage → package 5mg when single-serve is supported
1:1 THC:CBD → profile THC/CBD, ratio 1:1
```

Test:

- Dutchie `.01g` and `.1g` artifact ignored;
- missing mg does not become 100mg;
- New York limit used as validation only;
- THC-only differs from THC/CBD;
- 1:1 differs from 2:1.

---

## 11. Extract, Infusion, and Hardware Tests

Hard conflicts:

```text
Live Resin != Live Rosin
Live Resin != Distillate
Rosin != Resin
Badder != Sauce
Uninfused != Infused
Hash Infused != Kief Infused
Live Resin Infused != Live Rosin Infused
Cartridge != Disposable
Disposable != AIO when hardware contract treats them as distinct identity values
Cartridge != Pod
```

Unknown does not equal known for automatic matching.

---

## 12. PEK Tests

Verify:

- deterministic ordering;
- normalized values;
- blank preservation;
- category-specific fields;
- no THC percentage pollution;
- no source dispensary in product identity;
- no price in product identity;
- exact product differences create different PEKs.

---

## 13. Hard-Gate Tests

Every gate requires:

- positive compatible pair;
- negative conflict pair;
- missing-field review case;
- approved alias case where relevant.

A high fuzzy score must fail when a hard gate conflicts.

---

## 14. Regression Cases

Permanent false-positive regressions must include:

- same brand/form/size but different strain;
- same brand/strain/size but different extract;
- same brand/strain but cartridge versus disposable;
- same product but 5-pack versus single;
- THC-only versus THC/CBD;
- 1:1 versus 2:1;
- flower size mismatch;
- generic title missing identity-critical field.

Store rejected cases in both:

- automated fixtures;
- `rejected_near_matches`.

---

## 15. Decision Tests

Verify confidence transitions:

```text
95–100 → auto-link only if hard gates pass
80–94 → attach and review
60–79 → candidate only
below 60 → provisional MCP
```

If project code intentionally uses stricter thresholds, record the approved decision.

---

## 16. Review Tests

Verify:

- approval creates durable link;
- alias approval creates scoped alias;
- rejection creates rejected near-match;
- rejected pair does not reappear as automatic match;
- missing critical data remains unresolved;
- reviewer and timestamp persist;
- rule change triggers relevant regression suite.

---

## 17. Price Index Tests

A listing enters only when:

- cannabis eligible;
- valid MCP link;
- usable price;
- active/in stock when available.

Verify:

- excluded accessories absent;
- unresolved candidate absent;
- invalid price absent;
- sale price produces correct effective price;
- store URL remains store-specific;
- MCP identity remains stable.

---

## 18. Batch Reconciliation

Required totals:

```yaml
RAW_ROWS:
NORMALIZED_ROWS:
ELIGIBLE_ROWS:
EXCLUDED_ROWS:
BAD_SOURCE_ROWS:
AUTO_LINKS:
REVIEW_ITEMS:
PROVISIONAL_MCPS:
REJECTED_NEAR_MATCHES:
PRICE_INDEX_ROWS:
DUPLICATE_ROWS:
UNACCOUNTED_ROWS:
```

`UNACCOUNTED_ROWS` must be zero or explained.

---

## 19. Release Gate

```yaml
PARSER_TESTS_PASSING: true
HARD_GATE_TESTS_PASSING: true
FALSE_POSITIVE_REGRESSIONS_PASSING: true
REVIEW_TRANSITIONS_PASSING: true
PRICE_INDEX_TESTS_PASSING: true
BATCH_RECONCILIATION_COMPLETE: true
KNOWN_CRITICAL_FALSE_POSITIVES: 0
RELEASE_DECISION: "GO | GO_WITH_ACCEPTED_RISKS | NO_GO"
```
