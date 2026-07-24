# Normalization Foundation v1

The goal of the PEK/MCP system:

Raw Dispensary Product Listing --> normalized DPL --> cannabis eligibility gate --> brand normalization --> product/form/size/mg extraction --> PEK generation --> hard rule matching --> MCP candidate creation --> review queue or auto-link --> price comparison index

The most important rule: **Minimize shopper categories. Preserve exact product differences inside PEK fields.**

We do **not** create endless categories like Hash Hole, Blunt, AIO, Moonrock, Beverage, Capsule, etc. Those become **form, subform, infusion, extract, or hardware fields**.

---

## 1. Core Object Definitions

### DPL -- Dispensary Product Listing

A DPL is the raw product as shown by one dispensary. It keeps store-specific information:

- source dispensary
- raw title
- raw brand
- raw category
- price
- sale price
- menu URL
- image URL
- description
- raw platform data

A DPL is **not** the canonical product. It is just a store-level sighting.

### MCP -- Master Canonical Product

An MCP is the clean product card representing the real-world sellable product.

Example: `MFNY 0.5g Hash Burger Live Resin Vape Cartridge`

Multiple DPLs can connect to one MCP if they represent the same exact product.

### PEK -- Product Equality Key

The PEK is the product fingerprint used for matching. It should describe the **exact sellable product**, not just a vague shopper category.

General PEK structure:

```
normalized_brand
| normalized_category
| normalized_form
| subform
| normalized_size
| normalized_product_name
| extract_type
| infusion_type
| hardware_type
| count
| cannabinoid_profile
| ratio
```

Blank fields stay blank. We do **not** fabricate missing facts.

---

## 2. Pipeline Overview

### Step 1 -- Ingest raw menus

Every product row from a dispensary menu enters a raw staging table exactly as received. Do not clean destructively at this stage.

**Schema: raw_dispensary_product_listings**

```sql
CREATE TABLE raw_dispensary_product_listings (
    raw_dpl_id TEXT PRIMARY KEY,
    batch_id TEXT NOT NULL,
    source_dispensary TEXT NOT NULL,
    source_menu_name TEXT,
    source_platform TEXT,
    source_product_title TEXT NOT NULL,
    source_brand TEXT,
    source_category TEXT,
    source_subcategory TEXT,
    price NUMERIC,
    sale_price NUMERIC,
    currency TEXT DEFAULT 'USD',
    thc_raw TEXT,
    cbd_raw TEXT,
    weight_raw TEXT,
    size_raw TEXT,
    count_raw TEXT,
    image_url_if_available TEXT,
    product_url_if_available TEXT,
    description TEXT,
    raw_payload JSONB,
    first_seen TIMESTAMP,
    last_seen TIMESTAMP,
    ingest_status TEXT DEFAULT 'ingested'
);
```

Purpose: Keep source truth untouched. All later normalization should be reproducible.

---

## 3. Pre-normalization Cleaning

Before extracting fields, clean the title and text fields.

### Text Normalization Rules

Apply to title, brand, category, description:

- trim whitespace
- collapse repeated spaces
- normalize apostrophes
- normalize dashes
- remove repeated separators
- preserve meaningful separators like |, -, :, /
- standardize unicode characters
- standardize case for matching but preserve display case separately

Examples:

`"Veteran’s Choice - Blue Dream 1G Cart"`
- display title: `"Veteran's Choice - Blue Dream 1G Cart"`
- search title: `"veterans choice blue dream 1g cart"`

### Remove Noisy Menu Decorations

Strip or ignore: SALE, NEW, Staff Pick, Best Seller, Limited, BOGO, Online Only, Vendor Day, Fresh Drop

Do not remove these if they are part of the product name, but normally they are menu labels.

---

## 4. Cannabis Eligibility Gate

Before creating MCPs, determine whether the listing is eligible for cannabis price comparison.

### Eligible Cannabis Categories

Use minimized top-level categories:

- Flower
- Pre-Rolls
- Vapes
- Concentrates
- Edibles
- Topicals
- Tinctures

Optional later: CBD / Hemp, Medical. But for now, keep the core cannabis categories tight.

### Excluded From Cannabis MCP Matching

These can remain in raw inventory but should not create cannabis MCPs or PEKs:

- Accessories, Merchandise, Apparel, Glassware, Rolling Papers, Wraps, Cones
- Batteries, Chargers, Lighters, Torches, Grinders, Trays, Storage Containers, Stash Jars
- Dab Tools, Cleaning Supplies
- Devices not containing cannabis

### Rule

If listing is accessory/merch/non-cannabis:

- keep raw DPL
- create normalized DPL with comparison_status = excluded_non_cannabis
- do not create cannabis PEK
- do not create cannabis MCP
- do not enter cannabis review queue
- do not learn cannabis brand/product aliases

### Field: comparison_status

- eligible_cannabis
- excluded_accessory
- excluded_merchandise
- excluded_non_cannabis
- needs_review
- bad_source_data

---

## 5. Category Normalization

Use broad shopper/menu buckets.

### Canonical Category Map

| Raw/menu concept | Normalized category |
|---|---|
| Flower, Bud, Small Buds, Smalls, Shake, Ground Flower | Flower |
| Pre-roll, Preroll, Joint, Blunt, Infused Pre-Roll, Hash Hole | Pre-Rolls |
| Vape, Cart, Cartridge, Disposable, AIO, Pod | Vapes |
| Concentrate, Rosin, Resin, Badder, Sauce, Diamonds, Hash, RSO | Concentrates |
| Edible, Gummies, Chocolate, Beverage, Capsule, Tablet, Lozenge, Oral | Edibles |
| Topical, Balm, Lotion, Salve | Topicals |
| Tincture, Drops | Tinctures |
| Battery, Paper, Glass, Lighter, Grinder, Tray | Excluded accessory |
| Shirt, Hat, Hoodie, Merch | Excluded merchandise |

---

## 6. Form and Subform Normalization

Categories stay broad. Forms and subforms carry product detail.

### Flower

| Title/source keyword | Category | Normalized form | Subform |
|---|---|---|---|
| flower, bud | Flower | Flower | |
| eighth, 3.5g | Flower | Flower | Eighth |
| smalls, small buds | Flower | Flower | Small Buds |
| shake | Flower | Flower | Shake |
| ground flower | Flower | Flower | Ground Flower |
| moonrock, moon rock as loose flower | Flower | Flower | Moonrocks |

### Pre-Rolls

| Title/source keyword | Category | Normalized form | Subform |
|---|---|---|---|
| pre-roll, preroll, joint | Pre-Rolls | Pre-Roll | |
| blunt | Pre-Rolls | Pre-Roll | Blunt |
| hash hole, hash-hole, hashhole | Pre-Rolls | Pre-Roll | Hash Hole |
| infused pre-roll | Pre-Rolls | Pre-Roll | Infused |
| dogwalker | Pre-Rolls | Pre-Roll | Dogwalker |
| mini pre-roll | Pre-Rolls | Pre-Roll | Mini |
| moonrock pre-roll | Pre-Rolls | Pre-Roll | Moonrock |

Important: Infused Pre-Roll is not a top-level category. It is category = Pre-Rolls, normalized_form = Pre-Roll, infusion_type = Infused.

### Vapes

| Title/source keyword | Category | Normalized form | Hardware type |
|---|---|---|---|
| cart, cartridge, 510 | Vapes | Vape Cartridge | 510 Cartridge |
| disposable | Vapes | Disposable Vape | Disposable |
| AIO, all-in-one | Vapes | Disposable Vape | AIO |
| pod | Vapes | Vape Pod | Pod |
| starter kit | Vapes | Vape Kit | Kit |

Important: AIO, Cartridge, Pod, Disposable are vape keyphrases/hardware types. They help define PEK identity but do not become top-level categories.

### Concentrates

| Title/source keyword | Category | Normalized form | Extract type |
|---|---|---|---|
| live resin | Concentrates | Concentrate | Live Resin |
| cured resin | Concentrates | Concentrate | Cured Resin |
| resin | Concentrates | Concentrate | Resin |
| live rosin | Concentrates | Concentrate | Live Rosin |
| rosin | Concentrates | Concentrate | Rosin |
| badder, batter | Concentrates | Concentrate | Badder |
| budder | Concentrates | Concentrate | Budder |
| sauce | Concentrates | Concentrate | Sauce |
| diamonds | Concentrates | Concentrate | Diamonds |
| crumble | Concentrates | Concentrate | Crumble |
| hash | Concentrates | Concentrate | Hash |
| RSO, Rick Simpson Oil, RSO syringe | Concentrates | Concentrate | RSO |

Important: RSO syringe always maps to Concentrates. Syringe can be stored as subform/hardware/package style.

### Edibles

Top-level category: Edibles

| Title/source keyword | Category | Normalized form |
|---|---|---|
| gummy, gummies | Edibles | Gummy |
| chocolate | Edibles | Chocolate |
| beverage, drink, seltzer, lemonade, tea | Edibles | Beverage |
| capsule | Edibles | Capsule |
| tablet | Edibles | Tablet |
| lozenge | Edibles | Lozenge |
| oral | Edibles | Oral |
| baked good, cookie, brownie | Edibles | Baked Good |

Important: Beverage and oral products live under Edibles. They remain distinct through normalized_form/subform.

---

## 7. Brand Normalization

Brand normalization must happen **before** PEK generation.

### Brand Normalization Flow

raw_brand --> clean formatting --> check approved brand alias table --> check title prefix if raw brand is missing --> assign normalized_brand --> assign brand_confidence

### Brand Alias Levels

**Level 1 -- automatic formatting normalization**

Safe changes: case normalization, apostrophe normalization, spacing cleanup, accent normalization, common punctuation cleanup.

Examples:
- OFF HOURS --> Off Hours
- STIIIZY --> Stiiizy
- House Of Sacci --> House of Sacci

**Level 2 -- approved aliases**

Approved once, then reused.

Examples:
- Veteran's Choice --> Veterans Choice
- Vet Choice --> Veterans Choice
- VCC --> Veterans Choice
- ElectraLeaf --> Electraleaf
- Pearl by Gron --> Pearls by Groen
- 6 Point Cannabis --> 6 Points Cannabis

**Level 3 -- uncertain aliases**

These go to review if they might be: brand, product line, collab, store label, strain name.

### Schema: brands

```sql
CREATE TABLE brands (
    brand_id TEXT PRIMARY KEY,
    canonical_brand_name TEXT NOT NULL,
    normalized_brand_key TEXT UNIQUE NOT NULL,
    brand_status TEXT DEFAULT 'active',
    notes TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### Schema: brand_aliases

```sql
CREATE TABLE brand_aliases (
    brand_alias_id TEXT PRIMARY KEY,
    raw_brand_value TEXT NOT NULL,
    normalized_raw_value TEXT NOT NULL,
    canonical_brand_id TEXT REFERENCES brands(brand_id),
    canonical_brand_name TEXT NOT NULL,
    alias_type TEXT,
    alias_confidence NUMERIC,
    approval_status TEXT NOT NULL,
    approved_by TEXT,
    approved_at TIMESTAMP,
    example_dpl_ids TEXT[],
    notes TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

Recommended approval_status values: `auto_normalized`, `approved`, `needs_review`, `rejected`, `deprecated`

Recommended alias_type values: `case_variant`, `punctuation_variant`, `abbreviation`, `misspelling`, `legacy_name`, `brand_line`, `manual_alias`

---

## 8. Brand Extraction From Title When Brand is Blank

If source_brand is blank and product is eligible cannabis, attempt title-based extraction.

### Patterns

Brand | Product
Brand - Product
Brand: Product
Brand / Product

Examples:

- `New York Honey | Cured Resin SS13` --> Brand: New York Honey, Product: SS13, Extract type: Cured Resin
- `Ichi Roll | Uninfused 4pk | Afterglow Haze` --> Brand: Ichi Roll, Product: Afterglow Haze, Count: 4, Infusion type: None

### Rule

Only extract title-prefix brand if:
- prefix matches known brand alias, OR
- prefix appears repeatedly as a brand-like value, OR
- source pattern strongly indicates brand separator

If not confident:
- normalized_brand = blank
- comparison_status = needs_review
- review issue = missing_critical_data

---

## 9. Product Name / Strain Normalization

The normalized product name should represent the strain, flavor, product line, or SKU name.

### Remove From Product Name

Do not let these pollute the product name: brand, size, weight, count, form, category, extract type, infusion type, hardware type, THC/CBD values, sale labels.

Example:

Raw: `"MFNY Hash Burger Live Resin 510 Cartridge 0.5g"`

Extract:
- brand = MFNY
- product_name = Hash Burger
- extract_type = Live Resin
- hardware_type = 510 Cartridge
- normalized_form = Vape Cartridge
- size = 0.5g

### Preserve Actual Product Identity Words

Keep: strain names, flavors, product lines, SKU names, collab names, ratio names when branded.

Examples: Blue Dream, Hash Burger, Watermelon Z, Pineapple Mango, Go, Chill, Sleep, Blue Raspberry, Apple Fritter

---

## 10. Product/Strain/Flavor Alias System

This should grow over time. Do **not** over-merge product names automatically.

### Alias Types

- strain_alias
- flavor_alias
- product_line_alias
- spelling_variant
- punctuation_variant
- abbreviation
- brand_specific_alias

### Examples

Likely safe after review:
- Red Headed Stranger --> Redheaded Stranger
- Biscotti Pancake --> Biscotti Pancakes
- Lilac Diesel --> Liliac Diesel

More dangerous (may need brand-specific approval):
- Blue Razz --> Blue Raspberry
- Plant of the Grapes --> Planet of the Grapes

### Rule

Brand aliases can often be global. Product/flavor aliases should usually be brand-scoped unless obviously identical.

### Schema: product_aliases

```sql
CREATE TABLE product_aliases (
    product_alias_id TEXT PRIMARY KEY,
    alias_type TEXT NOT NULL,
    raw_value TEXT NOT NULL,
    normalized_raw_value TEXT NOT NULL,
    canonical_value TEXT NOT NULL,
    brand_scope_id TEXT REFERENCES brands(brand_id),
    form_scope TEXT,
    category_scope TEXT,
    approval_status TEXT NOT NULL,
    confidence NUMERIC,
    example_dpl_ids TEXT[],
    notes TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

Recommended approval_status values: `approved_alias`, `needs_review`, `rejected_alias`, `brand_specific_alias`, `deprecated`

---

## 11. Size Normalization

Size means different things depending on category.

### Flower / Pre-Rolls / Vapes / Concentrates

Normalize weight to grams.

Examples:
- 1/8 --> 3.5g
- eighth --> 3.5g
- 3.5 grams --> 3.5g
- half gram --> 0.5g
- .5g --> 0.5g
- 1 gram --> 1g
- 2 gram --> 2g
- quarter --> 7g
- half ounce --> 14g
- ounce --> 28g

### Size Table

| Raw | Normalized |
|---|---|
| .5g | 0.5g |
| 0.5 gram | 0.5g |
| half gram | 0.5g |
| 1 gram | 1g |
| 1g | 1g |
| eighth | 3.5g |
| 1/8 | 3.5g |
| quarter | 7g |
| 1/4 | 7g |
| half oz | 14g |
| ounce | 28g |

### Pre-Roll Count and Total Weight

For pre-rolls, parse both individual unit size and count.

Examples:

`5pk 0.5g` --> count = 5, unit_weight = 0.5g, total_weight = 2.5g, normalized_size = 2.5g, package_descriptor = 5pk x 0.5g

`4pk 1g` --> count = 4, unit_weight = 1g, total_weight = 4g

If title only says `5pk`: count = 5, normalized_size = blank unless total weight is stated. Do not invent total grams.

---

## 12. Edible Milligram Normalization

For edibles, size is not flower-style weight. Use: total package cannabinoid mg, serving mg, count, ratio, cannabinoid profile.

### Edible Parser Should Extract

- package_thc_mg, serving_thc_mg
- package_cbd_mg, serving_cbd_mg
- package_cbn_mg, serving_cbn_mg
- package_cbg_mg, serving_cbg_mg
- count, ratio, cannabinoid_profile

### Ignore Dutchie Gram Artifacts

For edibles and beverages, ignore these unless title confirms real package weight: .01g, .1g, 0.01g, 0.1g. These are usually platform artifacts, not product size.

### Edible MG Patterns

| Raw title pattern | Extraction |
|---|---|
| 100mg | package_thc_mg = 100, if THC implied |
| 100mg THC | package_thc_mg = 100 |
| 10pk 100mg | count = 10, package_thc_mg = 100 |
| 10ct 100mg | count = 10, package_thc_mg = 100 |
| 10 x 10mg | count = 10, serving_thc_mg = 10, package_thc_mg = 100 |
| 10 gummies 10mg each | count = 10, serving_thc_mg = 10, package_thc_mg = 100 |
| 5mg Beverage | package_thc_mg = 5 if single-serve |
| 2.5mg THC : 2.5mg CBD | serving_thc_mg = 2.5, serving_cbd_mg = 2.5 |
| 1:1 THC:CBD | ratio = 1:1, cannabinoid_profile = THC/CBD |
| THC:CBN | cannabinoid_profile = THC/CBN |

### New York Adult-Use Edible Rule

Use this as validation, not invention:
- Expected adult-use edible max: serving THC <= 10mg, package THC <= 100mg
- Rule: Do not auto-fill 100mg just because a NY edible is missing mg. Use 100mg as a ceiling / validation rule only.

### Edible Normalized Size Examples

- 100mg THC
- 10mg THC
- 100mg THC / 100mg CBD
- 20pk / 100mg THC
- 10pk x 10mg THC
- 5mg THC

---

## 13. Extract Type Normalization

Extract type is matching-critical.

### Extract Type Values

- Distillate, Live Resin, Cured Resin, Resin, Live Rosin, Rosin
- Liquid Diamonds, Diamonds, Sauce, Badder, Budder, Crumble
- Hash, Bubble Hash, Kief, RSO, Unknown

### Alias Examples

- batter --> Badder
- badder --> Badder
- live resin sauce --> Live Resin + Sauce
- live rosin --> Live Rosin
- LR --> Live Resin only if brand/title context supports it

### Hard Rule

Unknown extract_type does not equal known extract_type.

So: `Blue Dream 1g Cartridge` does not automatically match `Blue Dream 1g Live Resin Cartridge`.

---

## 14. Infusion Type Normalization

Infusion type is especially important for pre-rolls.

### Infusion Values

- None, Infused, Hash Infused, Kief Infused
- Live Resin Infused, Live Rosin Infused, Rosin Infused
- Diamond Infused, Moonrock Infused, Terpene Infused, Unknown

### Rules

- Uninfused != Infused
- Hash Infused != Kief Infused unless approved
- Live Resin Infused != Live Rosin Infused
- Generic Infused != specific infusion type unless brand/product confirms equivalence

### Hash Hole Rule

hash hole / hash-hole / hashhole --> category = Pre-Rolls, normalized_form = Pre-Roll, subform = Hash Hole, infusion_type = Hash Infused, Rosin Infused, Live Rosin Infused, or Infused depending on title

---

## 15. Hardware Type Normalization

Mainly for vapes.

### Hardware Values

- 510 Cartridge, Disposable, AIO, Pod, Vape Kit, Unknown

### Rules

- AIO = All-In-One Disposable Vape
- Cart / Cartridge / 510 = Vape Cartridge
- Pod = Vape Pod
- Do not merge different hardware types

These are separate MCPs:
- Jaunty Blue Dream 1g Vape Cartridge
- Jaunty Blue Dream 1g AIO Disposable Vape
- Jaunty Blue Dream 1g Vape Pod

---

## 16. Dominance / Type Normalization

Useful but not always matching-critical.

### Values

- Indica, Sativa, Hybrid, Indica Hybrid, Sativa Hybrid, CBD, THC, Balanced, Unknown

### Rule

Use dominance/type as supporting evidence. Do not block a match only because one menu says Hybrid and another omits it. But flag contradictions: same PEK candidate where one says Indica and one says Sativa --> dominance_conflict review.

---

## 17. Normalized DPL Schema

This is the cleaned row-level object before MCP grouping.

```sql
CREATE TABLE normalized_dispensary_product_listings (
    dpl_id TEXT PRIMARY KEY,
    raw_dpl_id TEXT REFERENCES raw_dispensary_product_listings(raw_dpl_id),
    batch_id TEXT NOT NULL,
    source_dispensary TEXT NOT NULL,
    source_menu_name TEXT,
    source_product_title TEXT NOT NULL,
    normalized_title TEXT,
    source_brand TEXT,
    normalized_brand TEXT,
    brand_id TEXT,
    brand_confidence NUMERIC,
    raw_category TEXT,
    normalized_category TEXT,
    normalized_form TEXT,
    subform TEXT,
    product_name_or_strain TEXT,
    normalized_product_name TEXT,
    size_value NUMERIC,
    size_unit TEXT,
    normalized_size TEXT,
    unit_weight_value NUMERIC,
    unit_weight_unit TEXT,
    total_weight_value NUMERIC,
    total_weight_unit TEXT,
    count INTEGER,
    package_thc_mg NUMERIC,
    serving_thc_mg NUMERIC,
    package_cbd_mg NUMERIC,
    serving_cbd_mg NUMERIC,
    package_cbn_mg NUMERIC,
    serving_cbn_mg NUMERIC,
    package_cbg_mg NUMERIC,
    serving_cbg_mg NUMERIC,
    cannabinoid_profile TEXT,
    ratio TEXT,
    extract_type TEXT,
    infusion_type TEXT,
    hardware_type TEXT,
    dominance_or_type TEXT,
    thc_value TEXT,
    cbd_value TEXT,
    price NUMERIC,
    sale_price NUMERIC,
    effective_price NUMERIC,
    image_url_if_available TEXT,
    product_url_if_available TEXT,
    description TEXT,
    comparison_status TEXT,
    proposed_pek TEXT,
    extraction_confidence NUMERIC,
    source_notes TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

---

## 18. PEK Generation

Only generate PEK for cannabis-eligible DPLs.

### General PEK

```
normalized_brand
| normalized_category
| normalized_form
| subform
| normalized_size
| normalized_product_name
| extract_type
| infusion_type
| hardware_type
| count
| cannabinoid_profile
| ratio
```

### Flower PEK

Brand | Flower | Form/Subform | Size | Strain/Product Name

Example: `Veterans Choice | Flower | Small Buds | 7g | Apple Fritter`

### Pre-Roll PEK

Brand | Pre-Rolls | Pre-Roll | Subform | Total Size | Count | Strain/Product Name | Infusion Type

Example: `Ichi Roll | Pre-Rolls | Pre-Roll | | | 4 | Afterglow Haze | None`

Hash hole example: `Brand | Pre-Rolls | Pre-Roll | Hash Hole | 2g | 1 | Strain | Live Rosin Infused`

### Vape PEK

Brand | Vapes | Normalized Form | Hardware Type | Size | Product/Strain | Extract Type

Example: `MFNY | Vapes | Vape Cartridge | 510 Cartridge | 0.5g | Hash Burger | Live Resin`

### Concentrate PEK

Brand | Concentrates | Concentrate | Size | Product/Strain | Extract Type | Subform

Example: `New York Honey | Concentrates | Concentrate | 1g | SS13 | Cured Resin |`

### Edible PEK

Brand | Edibles | Normalized Form | Flavor/Product Line | Package MG | Count | Cannabinoid Profile | Ratio

Example: `Off Hours | Edibles | Gummy | Blue Raspberry | 100mg THC | 10 | THC |`

Beverage example: `Ayrloom | Edibles | Beverage | Honeycrisp | 10mg THC | 1 | THC/CBD | 1:1`

---

## 19. Hard Rule Gates Before Matching

False positives are worse than missed matches. Before fuzzy matching or embeddings, apply hard gates.

| Gate | Name | Rule |
|------|------|------|
| 1 | Cannabis eligibility | Excluded accessory/merch/non-cannabis cannot match cannabis MCP |
| 2 | Brand compatibility | Brands must match exactly after alias normalization |
| 3 | Category compatibility | Categories must match after minimized category normalization |
| 4 | Form compatibility | Forms must match where form is identity-critical |
| 5 | Size compatibility | Usually size must match |
| 6 | Product/strain/flavor compatibility | Must match or be an approved alias |
| 7 | Extract compatibility | Must match for vapes, concentrates, infused pre-rolls |
| 8 | Infusion compatibility | Must match for pre-rolls and infused products |
| 9 | Hardware compatibility | For vapes: Cartridge != Disposable != AIO != Pod |
| 10 | Ratio/cannabinoid compatibility | For edibles: THC != THC/CBD, 1:1 != 2:1 |

### Gate Details

**Gate 2 examples:**
- Allowed: Veteran's Choice = Veterans Choice, Vet Choice = Veterans Choice
- Not allowed: similar-looking but unapproved brand names

**Gate 3 examples:**
- Allowed: Beverage --> Edibles, Capsule --> Edibles, Blunt --> Pre-Rolls, Hash Hole --> Pre-Rolls, RSO --> Concentrates
- Not allowed: Flower != Concentrates, Vapes != Concentrates, Pre-Rolls != Flower

**Gate 4 examples:**
- Vape Cartridge != Disposable Vape
- Vape Pod != Vape Cartridge
- Gummy != Beverage
- Capsule != Chocolate

**Gate 5 examples:**
- 0.5g != 1g, 3.5g != 7g, 10mg != 100mg, 5pk != 10pk
- If size is missing on one side, send to review rather than auto-match

**Gate 6 examples:**
- Blue Dream != Sour Diesel
- Blue Raspberry != Watermelon
- Hash Burger != Honey Banana

**Gate 7 examples (hard no):**
- Live Resin != Live Rosin
- Live Resin != Distillate
- Rosin != Resin
- Badder != Sauce
- Diamonds != Hash

**Gate 8 examples (hard no):**
- Uninfused != Infused
- Hash Infused != Kief Infused
- Live Resin Infused != Live Rosin Infused

**Gate 10 examples:**
- THC != THC/CBD
- 1:1 != 2:1
- THC/CBN != THC-only

---

## 20. Matching Confidence Framework

After hard gates pass, score candidate matches.

### Suggested Scoring

| Signal | Weight |
|--------|--------|
| Brand exact/approved alias | Required |
| Category match | Required |
| Form match | Required |
| Size/mg/count match | High |
| Product/strain/flavor match | High |
| Extract/infusion match | High where relevant |
| Hardware match | High for vapes |
| Ratio/cannabinoid profile match | High for edibles |
| Title similarity | Medium |
| Description similarity | Low/medium |
| Image similarity | Supporting only |
| THC/CBD lab value similarity | Low/supporting |

### Confidence Bands

- 95-100 = auto-match
- 80-94 = match but needs review
- 60-79 = candidate only
- below 60 = provisional new MCP

But even a high score cannot override a hard gate conflict.

---

## 21. MCP Creation

When no safe existing MCP match exists, create a provisional MCP.

### Canonical Title Structure

Use: Brand + Size/MG/Count + Product Name + Modifier + Form

Keep titles readable.

Examples:
- MFNY 0.5g Hash Burger Live Resin Vape Cartridge
- Off Hours 100mg Blue Raspberry Gummies 10pk
- Ayrloom 10mg Honeycrisp 1:1 THC:CBD Beverage
- Veterans Choice 7g Apple Fritter Small Buds Flower
- Ichi Roll 4pk Afterglow Haze Pre-Rolls
- New York Honey 1g SS13 Cured Resin Concentrate

### MCP Schema

```sql
CREATE TABLE master_canonical_products (
    mcp_id TEXT PRIMARY KEY,
    pek TEXT UNIQUE,
    canonical_title TEXT NOT NULL,
    search_title TEXT,
    brand_id TEXT REFERENCES brands(brand_id),
    normalized_brand TEXT NOT NULL,
    normalized_category TEXT NOT NULL,
    normalized_form TEXT NOT NULL,
    subform TEXT,
    canonical_product_name TEXT NOT NULL,
    size_value NUMERIC,
    size_unit TEXT,
    normalized_size TEXT,
    unit_weight_value NUMERIC,
    total_weight_value NUMERIC,
    count INTEGER,
    package_thc_mg NUMERIC,
    serving_thc_mg NUMERIC,
    package_cbd_mg NUMERIC,
    serving_cbd_mg NUMERIC,
    package_cbn_mg NUMERIC,
    serving_cbn_mg NUMERIC,
    package_cbg_mg NUMERIC,
    serving_cbg_mg NUMERIC,
    cannabinoid_profile TEXT,
    ratio TEXT,
    extract_type TEXT,
    infusion_type TEXT,
    hardware_type TEXT,
    dominance_or_type TEXT,
    canonical_image_id TEXT,
    canonical_image_url TEXT,
    image_status TEXT,
    confidence_score NUMERIC,
    review_status TEXT,
    first_seen TIMESTAMP,
    last_seen TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

Recommended review_status values: `approved`, `provisional`, `needs_review`, `rejected_duplicate`, `deprecated`

---

## 22. Linking DPLs to MCPs

Once a DPL is matched to an MCP, store the relationship.

### Schema: mcp_dpl_links

```sql
CREATE TABLE mcp_dpl_links (
    link_id TEXT PRIMARY KEY,
    mcp_id TEXT REFERENCES master_canonical_products(mcp_id),
    dpl_id TEXT REFERENCES normalized_dispensary_product_listings(dpl_id),
    match_confidence NUMERIC,
    match_method TEXT,
    match_reasons TEXT[],
    needs_review BOOLEAN DEFAULT FALSE,
    review_status TEXT,
    linked_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

Recommended match_method values: `exact_pek`, `approved_alias`, `high_confidence_match`, `manual_review`, `provisional_new_mcp`

---

## 23. Review Queue

Every uncertain case should be reviewable.

### Review Issue Types

- possible_duplicate
- possible_same_product
- brand_alias_uncertain
- strain_conflict
- flavor_conflict
- size_conflict
- form_conflict
- category_conflict
- dominance_conflict
- extract_type_conflict
- infusion_type_conflict
- hardware_conflict
- ratio_conflict
- missing_critical_data
- bad_source_data
- price_outlier
- excluded_non_cannabis

### Schema: product_review_queue

```sql
CREATE TABLE product_review_queue (
    review_id TEXT PRIMARY KEY,
    batch_id TEXT,
    issue_type TEXT NOT NULL,
    risk_level TEXT NOT NULL,
    dpl_ids TEXT[],
    candidate_mcp_ids TEXT[],
    source_titles_compared TEXT[],
    reason_for_review TEXT,
    recommended_action TEXT,
    status TEXT DEFAULT 'open',
    reviewed_by TEXT,
    reviewed_at TIMESTAMP,
    resolution_notes TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

Recommended risk_level values: `low`, `medium`, `high`, `critical`

---

## 24. Rejected Near-Matches

This is important because it teaches the system what **not** to merge.

### Examples

- Same brand + strain + size, but cartridge vs disposable
- Same brand + strain + size, but live resin vs distillate
- Same brand + flavor + mg, but 1:1 vs THC-only
- Same brand + strain, but 3.5g flower vs 7g small buds

### Schema: rejected_near_matches

```sql
CREATE TABLE rejected_near_matches (
    rejected_match_id TEXT PRIMARY KEY,
    dpl_id_1 TEXT,
    dpl_id_2 TEXT,
    mcp_id_1 TEXT,
    mcp_id_2 TEXT,
    title_1 TEXT,
    title_2 TEXT,
    why_they_look_similar TEXT,
    why_they_should_not_match TEXT,
    rule_learned TEXT,
    confidence NUMERIC,
    created_at TIMESTAMP
);
```

---

## 25. Data Quality Flags

These are not always matching problems, but they should be tracked.

### Common Flags

- missing_brand, missing_size, missing_mg, missing_count
- bad_edible_weight_artifact
- conflicting_category, conflicting_form
- conflicting_extract_type, conflicting_infusion_type
- possible_wrong_source_category, possible_wrong_brand
- price_outlier, duplicate_listing, title_too_generic

### Schema: data_quality_flags

```sql
CREATE TABLE data_quality_flags (
    flag_id TEXT PRIMARY KEY,
    batch_id TEXT,
    dpl_id TEXT,
    source_dispensary TEXT,
    problem_type TEXT NOT NULL,
    problem_description TEXT,
    suggested_fix TEXT,
    confidence NUMERIC,
    status TEXT DEFAULT 'open',
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

---

## 26. Price Comparison Index

Only eligible cannabis MCPs should enter price comparison.

### Rule

A DPL enters price comparison only if:
- comparison_status = eligible_cannabis
- linked to valid MCP
- product has usable price or sale price
- product is in stock / active if stock data exists

### Schema: price_comparison_index

```sql
CREATE TABLE price_comparison_index (
    price_index_id TEXT PRIMARY KEY,
    mcp_id TEXT REFERENCES master_canonical_products(mcp_id),
    dpl_id TEXT REFERENCES normalized_dispensary_product_listings(dpl_id),
    source_dispensary TEXT,
    source_menu_name TEXT,
    canonical_title TEXT,
    normalized_brand TEXT,
    normalized_category TEXT,
    normalized_form TEXT,
    normalized_size TEXT,
    price NUMERIC,
    sale_price NUMERIC,
    effective_price NUMERIC,
    product_url TEXT,
    image_url_from_store TEXT,
    in_stock BOOLEAN,
    last_seen TIMESTAMP,
    last_checked TIMESTAMP,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

---

## 27. Recommended Processing Order

This is the full operational flow:

1. Ingest raw menu rows.
2. Store untouched source data in raw DPL table.
3. Clean title/brand/category text.
4. Detect accessory/merch/non-cannabis exclusions.
5. Normalize broad category.
6. Normalize form, subform, hardware, extract, infusion.
7. Normalize brand using brand alias table.
8. If brand missing, attempt title-prefix extraction.
9. Extract product name / strain / flavor.
10. Normalize product aliases if approved.
11. Extract size:
    - flower/pre-roll/vape/concentrate = grams/count
    - edibles = mg/count/ratio/cannabinoid profile
12. Ignore edible gram artifacts.
13. Generate normalized DPL row.
14. If excluded_non_cannabis, stop cannabis matching.
15. Generate PEK for eligible cannabis row.
16. Search existing MCPs by PEK and alias candidates.
17. Apply hard gates.
18. Score candidate matches.
19. Auto-link, review, or create provisional MCP.
20. Create rejected near-match records where useful.
21. Update brand/product alias suggestions.
22. Update price comparison index.
23. Export review queue and data quality flags.

---

## 28. Current Resolved System Rules

These are now foundation rules:

- Accessories and merchandise are excluded from cannabis MCP price comparison.
- Hash hole maps to Pre-Rolls category.
- Hash hole is an infused pre-roll subform/identity marker.
- Blunt maps to Pre-Rolls category.
- Blunt is a subform, not a category.
- Moonrocks map according to sellable form:
  - moonrock pre-roll/blunt/joint --> Pre-Rolls
  - loose moonrock flower --> Flower
- RSO syringe maps to Concentrates.
- AIO maps to Vapes.
- AIO is hardware/subform for Disposable Vape.
- Cartridge, pod, disposable, AIO are vape identity fields.
- Beverage, oral, capsule, tablet, lozenge all live under Edibles.
- Edibles normalize by milligrams/count/ratio, not gram weight.
- NY edible 100mg package max is a validation rule, not an automatic inferred size.
- Brand aliases are required and must normalize before PEK generation.
- Extract and infusion conflicts block automatic matching.
- Different strains/flavors should not merge unless approved alias exists.
- Different sizes/counts should not merge.
- Unknown extract type does not equal known extract type.

---

## 29. Minimal Category Philosophy

Use this:

- Flower
- Pre-Rolls
- Vapes
- Concentrates
- Edibles
- Topicals
- Tinctures
- Accessories - excluded
- Merchandise - excluded

Avoid this:

- Hash Hole as category
- Blunt as category
- AIO as category
- Beverage as top-level category
- Capsule as top-level category
- Moonrock as top-level category
- RSO as top-level category

The product identity still remains precise because PEK uses:

- normalized_form
- subform
- extract_type
- infusion_type
- hardware_type
- size
- count
- mg
- ratio
- product name

That is the foundation: **fewer categories, stronger PEK fields.**
