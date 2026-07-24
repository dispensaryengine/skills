# Skill Package Structure Contract

## Required Package Sequence

### 1. Frontmatter

- `name`
- `description`

### 2. Title

Exactly one top-level `#` heading in `SKILL.md`.

### 3. Purpose

One or two sentences describing the operational outcome.

### 4. Primary Reference

Name the authoritative foundation and explain what it contains.

### 5. Supporting References

Route references by concern.

### 6. Core Principle

State the central invariant in a compact form.

### 7. Operating Modes

Define only materially different modes.

### 8. Inputs and Variables

List required variables or tell the agent where their detailed definitions live.

### 9. Workflow

Use ordered phases or steps.

Every step should include:

- objective;
- required actions;
- output or state change;
- exit condition where needed.

### 10. Required Outputs

Define artifacts and state the skill must produce.

### 11. Validation

Reference deterministic and behavioral tests.

### 12. Handoff

Define exact continuation state.

### 13. Completion Gate

List conditions that must be true before declaring completion.

---

## Recommended Folder Layout

```text
skill-name/
├── SKILL.md
├── CHANGELOG.md                         optional
├── references/
│   ├── foundation.md                   required
│   ├── structure_contract.md           required
│   ├── testing_contract.md             required
│   ├── style_contract.md               optional
│   ├── security_contract.md            optional
│   ├── review_contract.md              optional
│   ├── operations_runbook.md           optional
│   └── *_implementations.md            optional
├── templates/
│   └── reusable artifacts              optional
└── tools/
    └── deterministic validators         optional
```

---

## Heading Rules

`SKILL.md`:

```text
# Skill Title
## Major Section
### Workflow Step
```

Do not use several top-level `#` headings.

Reference documents may use one top-level title and standard nested headings.

---

## Controller Size Rule

Preferred:

```yaml
MIN_LINES: 80
TARGET_MAX_LINES: 350
```

A shorter controller is acceptable when complete.

A longer controller must be reviewed for content that belongs in references.

---

## Reference Naming

Use descriptive lowercase names:

```text
foundation.md
structure_contract.md
security_contract.md
testing_contract.md
operations_runbook.md
node_implementations.md
```

Avoid:

```text
misc.md
notes.md
stuff.md
new.md
final.md
final2.md
```

---

## Reference Link Rules

All referenced paths must:

- be relative to package root;
- exist with exact capitalization;
- use forward slashes;
- avoid links to temporary `/mnt/data` paths;
- avoid hidden conversation-only resources.

---

## Template Rules

Templates must:

- use visible placeholders;
- contain no real secret;
- identify optional sections;
- preserve required field order;
- be directly copyable.

---

## Final Structural Gate

```yaml
ONE_H1_IN_CONTROLLER: true
PRIMARY_REFERENCE_DECLARED: true
PRIMARY_REFERENCE_EXISTS: true
SUPPORTING_REFERENCES_RESOLVE: true
NO_TEMPORARY_PATHS: true
NO_SECRET_VALUES: true
NO_COMPETING_FOUNDATIONS: true
WORKFLOW_PRESENT: true
VALIDATION_PRESENT: true
HANDOFF_PRESENT: true
```
