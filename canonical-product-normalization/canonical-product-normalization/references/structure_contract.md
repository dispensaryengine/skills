# Structure Contract

Defines the section hierarchy, data structures, and content patterns for canonical product normalization documentation.

For the full operational specification (SQL schemas, normalization tables, hard rules, processing pipeline), see `references/normalization_foundation.md`.

## Document Section Sequence

The document follows this exact order. Adapt section names to the target domain while preserving the structural flow:

### 1. System Overview

- Open with the core idea in 1-2 sentences
- Define the key terminology objects:
  - **DPL** (Dispensary Product Listing) -- the raw store-level sighting
  - **MCP** (Master Canonical Product) -- the clean, system-wide canonical record
  - **PEK** (Product Equality Key) -- the fingerprint matching logic
- For each term: bold name, brief definition, 1-line example
- State the most important rule: minimize shopper categories, preserve exact product differences inside PEK fields

### 2. Product Card Title Template

- State the title formula in two equivalent forms:
  - **Concatenated:** Brand + Size/MG/Count + Product Name + Modifier + Form
  - **Templated:** {Brand} {Size} {Line / Strain / Product Name} {Modifier} {Form}

### 3. Title Components

Define each of the five components as a sub-section. Each sub-section contains:
- **Name** as bold heading
- One-sentence definition
- "Examples:" label followed by bullet list of realistic values

**Standard five components:**

| # | Component | Purpose | Example Values |
|---|-----------|---------|----------------|
| 1 | Brand | Company or product brand | Stiiizy, MFNY, Ayrloom |
| 2 | Size / Weight / Count / Volume / MG | Sellable unit size | 1g, 0.5g, 3.5g, 10pk, 100mg, 12oz |
| 3 | Strain or Product Line | Strain name, flavor, product line | Watermelon Z, Blue Dream, Hash Burger |
| 4 | Extract / Infusion / Modifier | Product style, extract type, infusion | Liquid Diamonds, Live Resin, Distillate, THC |
| 5 | Product Form | Shopper-facing product type | Vape Pod, Disposable, Cartridge, Gummy, Flower |

### 4. Product Card Title Example (Worked Example)

This section has a specific required layout. See `references/style_contract.md` for the exact visual format.

Structure:
- "**Product Data**" as a bold sub-header
- Each field uses a two-line pattern:
  - Line 1: Field label in regular weight (e.g., "Brand:", "Size:", "Strain/Product Line:", "Modifier:", "Form:")
  - Line 2: Field value in **bold**
- "**Final MCP Title**" as a bold sub-header
- The assembled title in **bold** on the following line

Example:

```
Product Data

Brand:
Stiiizy

Size:
1g

Strain/Product Line:
Watermelon Z

Modifier:
Liquid Diamonds

Form:
Vape Pod

Final MCP Title
Stiiizy 1g Watermelon Z Liquid Diamonds Vape Pod
```

### 5. More Product Title Examples

- Bullet list of 8-10 full canonical titles showing variety across brands, sizes, forms
- Each example should exercise different combinations of components
- Include examples from different categories (Flower, Pre-Roll, Vape, Concentrate, Edible)
- Tight bullet spacing -- items close together vertically

### 6. Category vs. Form

- Explain the distinction:
  - **Category** = broad product class (Flower, Pre-Rolls, Vapes, Concentrates, Edibles, Topicals, Tinctures)
  - **Form** = exact product type (Vape Pod, Disposable, Cartridge, Gummy, Chocolate, Infused Pre-Roll, Hash Hole)
- State that the visible MCP title uses the form, and search filters use both
- Reference the minimal category philosophy: fewer categories, stronger PEK fields
- List what is excluded from cannabis MCP matching (accessories, merchandise, etc.)

### 7. Product Normalization Flow

- Describe the end-to-end process:
  1. Scraped menu item becomes a raw DPL (untouched source truth)
  2. Pre-normalization cleaning (trim, collapse spaces, strip noisy decorations)
  3. Cannabis eligibility gate (exclude non-cannabis)
  4. Category/form/subform normalization
  5. Brand normalization (3 levels: auto-format, approved aliases, uncertain)
  6. Product name / strain / flavor extraction
  7. Size/mg normalization
  8. Generate PEK
  9. Compare against existing MCPs using hard-rule gates + scoring
  10. Decision: auto-link / review queue / create provisional MCP
- List the downstream systems powered by MCP (search, price comparison, availability, reviews, SEO, brand/category/deal pages)

### 8. MCP Data Structure

- Introductory text: "The MCP should hold a stable product identity"
- List the field names vertically (one per line) in this order:

```
mcp_id
pek
canonical_title
search_title
brand_id
normalized_brand
normalized_category
normalized_form
subform
canonical_product_name
size_value
size_unit
normalized_size
unit_weight_value
total_weight_value
count
package_thc_mg
serving_thc_mg
package_cbd_mg
serving_cbd_mg
cannabinoid_profile
ratio
extract_type
infusion_type
hardware_type
dominance_or_type
canonical_image_url
confidence_score
review_status
first_seen
last_seen
```

### 9. MCP Example

- Show a concrete example:
  - "Master Canonical Product" as bold sub-header
  - Product name in **bold** (e.g., "**STIIIZY Blue Dream Vape Pod 1g**")
  - "Connected Dispensary Listings" as bold sub-header
  - 3+ bullet points showing variant store titles with quotation marks
  - Closing sentence explaining why they all connect to one MCP

### 10. Dispensary Product Listing Data Structure

- Introductory text explaining volatile store-specific data
- Distinguish raw DPL (untouched source) from normalized DPL (cleaned, extracted fields)
- List normalized DPL field names vertically:

```
dpl_id
raw_dpl_id
batch_id
source_dispensary
source_product_title
normalized_title
normalized_brand
brand_id
normalized_category
normalized_form
subform
normalized_product_name
normalized_size
count
package_thc_mg
serving_thc_mg
cannabinoid_profile
ratio
extract_type
infusion_type
hardware_type
dominance_or_type
price
sale_price
effective_price
comparison_status
proposed_pek
extraction_confidence
```

- Closing sentence: "The DPL is not the product truth object. It is the store-level sighting of that product."

### 11. PEK Generation

- Explain the PEK concept: the product fingerprint for matching
- Show the general PEK structure with pipe separators
- Show category-specific PEK formats:
  - Flower: Brand | Flower | Form/Subform | Size | Strain
  - Pre-Roll: Brand | Pre-Rolls | Pre-Roll | Subform | Size | Count | Strain | Infusion
  - Vape: Brand | Vapes | Form | Hardware | Size | Strain | Extract
  - Concentrate: Brand | Concentrates | Concentrate | Size | Strain | Extract
  - Edible: Brand | Edibles | Form | Flavor | Package MG | Count | Profile | Ratio

### 12. Hard-Rule Matching Gates

- Opening principle: "False positives are worse than missed matches. Apply hard gates before fuzzy matching."
- Numbered list of the 10 gates (concise form):
  1. Cannabis eligibility
  2. Brand compatibility (exact after alias normalization)
  3. Category compatibility (Flower != Concentrates)
  4. Form compatibility (Cartridge != Disposable)
  5. Size compatibility (0.5g != 1g)
  6. Product/strain compatibility (Blue Dream != Sour Diesel)
  7. Extract compatibility (Live Resin != Live Rosin)
  8. Infusion compatibility (Uninfused != Infused)
  9. Hardware compatibility (Cartridge != Pod)
  10. Ratio/cannabinoid compatibility (THC != THC/CBD)

### 13. Matching Confidence Rules

- Present as four threshold statements (not a table):

```
95-100 confidence = auto-attach to MCP
80-94 confidence   = attach but mark as needs review
60-79 confidence   = candidate match only
Below 60 confidence = create provisional MCP
```

- Include a note about preventing false matches (the "raccoon-in-a-server-room" metaphor or domain-appropriate equivalent)
- Note: high scores cannot override hard gate conflicts

### 14. Alias Learning

- Explain that MCP absorbs aliases over time
- Show brand alias examples (level 1-3 normalization)
- Show product/strain alias examples
- Closing sentence about the engine getting smarter

### 15. Recommended Database Tables

Present tables in sequence. For each table:
- Table name as bold heading (e.g., **master_canonical_products**)
- One-sentence purpose
- Vertical list of column names

**Table list:**
1. `master_canonical_products` -- product card table
2. `brands` -- canonical brand registry
3. `brand_aliases` -- known brand variants and alternate names
4. `product_aliases` -- known product/strain/flavor variants
5. `raw_dispensary_product_listings` -- untouched source data
6. `normalized_dispensary_product_listings` -- cleaned store-specific versions
7. `mcp_dpl_links` -- DPL-to-MCP relationships
8. `product_review_queue` -- uncertain matches for human review
9. `rejected_near_matches` -- teaches system what NOT to merge
10. `data_quality_flags` -- tracks data quality issues
11. `price_comparison_index` -- eligible products for price comparison

For full SQL schemas with all columns and data types, see `references/normalization_foundation.md`.

### 16. Suggested MCP Title Fields

- Explain the system should store title parts, not just the final title
- List the decomposed field names vertically:

```
brand
size_value
size_unit
strain_or_line
product_modifier
form
category
cannabinoid_profile
ratio
canonical_title
search_title
```

### 17. MCP Title Field Example

- Present a JSON object showing all fields populated with values from the worked example
- Use a monospace font (RobotoMono-Regular or compatible)
- Include both `canonical_title` (proper case) and `search_title` (lowercase)

### 18. Matching Consequence / False-Match Prevention

- Opening sentence: "The title structure helps prevent dangerous false matches."
- "These should **not** collapse into one product card:"
- Bullet list of 4-5 products that share brand and strain but are different sellable products:
  - Same brand + strain + size, but cartridge vs disposable
  - Same brand + strain + size, but live resin vs distillate
  - Same brand + flavor + mg, but 1:1 vs THC-only
  - Same brand + strain, but 3.5g flower vs 7g small buds
- Closing: "Same brand. Same strain. Different sellable product. Different MCPs."

### 19. Final Rule

- One-paragraph summary restating the core formula
- "Clean formula:" label
- The clean formula in **bold**: **Brand + Size/MG/Count + Strain/Product Line + Modifier + Form**
- "That becomes the name of the truth object."
- "The messy dispensary titles become aliases underneath it."
- Restate the minimal category philosophy: fewer categories, stronger PEK fields.

## Content Patterns

### Acronym Introduction Pattern
Always introduce acronyms as: **Full Name** (bold) followed by explanation, then use acronym alone.

### Example Pattern
- Label "Example:" on its own line in regular weight
- Bold value on the next line
- Context sentence below if needed

### Field List Pattern
Schema fields are listed as a vertical stack (one per line), not in a table. This is intentional -- it reads as a field enumeration rather than a data grid.

### Separator Pattern
Every major section is preceded by a horizontal rule. Sub-sections within a major section do not use separators.
