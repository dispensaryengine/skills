# Style Contract

Extracted from the reference PDF "Master Canonical Product System" (14 pages). Fonts verified via PyMuPDF/fitz page-level font extraction.

## Reference Typography

- **Primary font family:** Arial (confirmed via fitz as Arial-BoldMT and ArialMT)
  - All headings: Arial Bold
  - Body text: Arial Regular
  - Bold inline text: Arial Bold
  - Code/JSON: RobotoMono-Regular (used for one JSON object example only)
- **Font substitution guidance:** When CJK content is present, replace Arial with a CJK-capable sans-serif (Noto Sans CJK, Microsoft YaHei, or PingFang SC). Maintain the same weight hierarchy. Do NOT use LiberationSans, Calibri, or Helvetica as substitutes.

## Page Composition

- **Background:** Pure white
- **Margins:** Generous (~1 inch / 72pt minimum on all sides)
- **Whitespace:** Ample vertical space between sections; horizontal rule separators between major sections
- **No header/footer content** — clean pages with body content only
- **No page numbers visible**
- **No cover page** — document opens directly with the title heading
- **No subtitle** — the reference document has only a title, no subtitle line (e.g., no "System Specification Document" or similar)

## Heading Hierarchy

| Level | Size | Weight | Usage |
|-------|------|--------|-------|
| Page title | ~26pt | Bold | Major section openers (e.g., "Product Card Title Template", "MCP Data Structure") |
| Section header | ~17pt | Bold | Sub-sections (e.g., "Title Components", "Brand") |
| Sub-header | ~14pt | Bold | Sub-sub-sections (e.g., "Product Data", "Final MCP Title") |

Headings are left-aligned with no numbering.

## Body Text

- **Font:** Arial Regular
- **Size:** ~11-12pt
- **Line spacing:** ~1.3-1.5x (comfortable, not dense)
- **Alignment:** Left-aligned, ragged right
- **Paragraph spacing:** Distinct gap between paragraphs (no first-line indent)

## Key Term Emphasis

- First mention of terminology uses **bold inline** (e.g., "The **Master Canonical Product** is the actual product card")
- Acronyms introduced with full name bold, acronym bold: "**MCP** — **Master Canonical Product**"
- Formula statements use bold for structural emphasis: "**Brand + Size + Strain/Product Line + Modifier + Form**"

## Lists

- **Unordered lists:** Filled circular bullets (solid dot)
- **Ordered lists:** Arabic numerals with period (1. 2. 3.)
- **Indentation:** Consistent ~0.5 inch indent from left margin
- **List item spacing:** Tight — bullet items are closer together than paragraph spacing. The reference shows minimal vertical gap between consecutive bullet items.

## Separators

- Horizontal rule (thin line, ~1px, full or near-full width) between major document sections
- No decorative elements, no colored bars, no icons

## Code/Structured Data Blocks

- **JSON objects:** RobotoMono-Regular font, left-aligned, no background shading, no syntax highlighting
- **Field lists (vertical enumeration):** Arial Regular, one field name per line — this is a vertical stack, not a table
- **Alias arrays:** Rendered as plain text with bracket delimiters, not styled as code blocks

## Color Palette

| Element | Color |
|---------|-------|
| All text | Black (#000000) |
| Background | White (#FFFFFF) |
| Horizontal rules | Black or dark gray |

Zero accent colors. Purely monochrome.

## Visual Density

Low-to-medium density. The document prioritizes readability and clear section separation over compactness. Each major section starts with a bold heading and is separated by horizontal rules. White space is used as a deliberate structural cue.

## Product Card Title Example Layout (Critical)

This section has a specific two-line-per-field format that must be followed exactly:

1. "**Product Data**" appears as a sub-header (bold, ~14pt)
2. Each field follows this pattern:
   - Line 1: Field label in regular weight (e.g., "Brand:", "Size:", "Strain/Product Line:", "Modifier:", "Form:")
   - Line 2: Field value in **bold** (e.g., "**Stiiizy**", "**1g**", "**Watermelon Z**")
3. "**Final MCP Title**" appears as a sub-header (bold, ~14pt)
4. The assembled title appears on the following line in **bold**

**Do NOT** use inline "Brand: **Stiiizy**" format. The label and value must be on separate lines.

Correct format:
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
