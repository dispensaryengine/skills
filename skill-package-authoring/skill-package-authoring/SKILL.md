---
name: modular-skill-package-authoring
description: Create, refactor, audit, and validate reusable agent skill packages that use a compact SKILL.md controller, one authoritative foundation reference, specialized contracts, optional implementation references, templates, tests, and an exact handoff state. Use when creating a new skill, converting a monolithic prompt into a maintainable skill package, standardizing multiple skills into one system, or checking whether an existing skill follows the modular package format.
---

# Modular Skill Package Authoring

Create skills as maintainable packages rather than oversized instruction files.

## Primary Reference

Read `references/skill_foundation.md` first.

It defines:

- the package architecture;
- controller responsibilities;
- reference boundaries;
- variable resolution;
- workflow phases;
- required artifacts;
- maintenance rules;
- versioning and deprecation;
- completion and handoff requirements.

## Supporting References

Read only the references needed for the current task:

- `references/structure_contract.md` — required controller and package sequence
- `references/reference_routing_contract.md` — what belongs in each file
- `references/quality_contract.md` — quality gates and anti-patterns
- `references/testing_contract.md` — package validation and behavior tests
- `templates/` — reusable file templates
- `tools/validate_skill_package.py` — static package validator

## Core Principle

The `SKILL.md` file is the controller, not the encyclopedia.

Use this model:

```text
Compact controller
    ↓
Authoritative foundation
    ↓
Specialized contracts
    ↓
Implementation references
    ↓
Templates and validation
```

A skill must remain usable when conversation history is missing.

## Operating Modes

Set:

```yaml
SKILL_AUTHORING_MODE: "create | refactor | audit | extend | repair"
TARGET_SKILL_NAME: ""
TARGET_DOMAIN: ""
PRIMARY_OUTCOME: ""
EXPECTED_RUNTIME: ""
OUTPUT_TYPES: []
SOURCE_MATERIALS: []
EXTERNAL_FACTS_REQUIRED: false
```

### Create

Build a new modular package from requirements.

### Refactor

Split a monolithic skill into controller and references without losing rules.

### Audit

Inspect an existing package and report structural, factual, operational, and maintenance problems.

### Extend

Add a capability without duplicating existing foundation rules.

### Repair

Resolve broken references, contradictory instructions, malformed frontmatter, invalid hierarchy, or missing validation.

## Reference Loading Rule

Always read:

1. `references/skill_foundation.md`
2. `references/structure_contract.md`

Then select only the domain references needed.

Do not load every reference automatically when the task only needs one.

## Workflow

### Step 1: Capture the Skill Contract

Determine:

- activation conditions;
- primary user goal;
- supported operating modes;
- required inputs;
- required outputs;
- authoritative source material;
- changeable external facts;
- implementation languages or runtimes;
- safety and security boundaries;
- completion criteria.

Record unresolved facts instead of inventing them.

### Step 2: Classify the Content

Assign every rule to one destination:

```text
Controller
Foundation
Structure contract
Style contract
Security contract
Testing contract
Operations runbook
Implementation reference
Template
Example
```

Use `references/reference_routing_contract.md` for placement rules.

### Step 3: Build the Package Skeleton

Minimum package:

```text
skill-name/
├── SKILL.md
└── references/
    ├── foundation.md
    ├── structure_contract.md
    └── testing_contract.md
```

Add only justified files.

### Step 4: Write the Controller

The controller must:

- have valid frontmatter;
- explain when the skill activates;
- identify the primary reference;
- route to supporting references;
- state the core principle;
- define operating modes;
- define the execution workflow;
- define required outputs;
- define validation and handoff.

Do not duplicate large tables, full schemas, long code examples, or platform manuals in the controller.

### Step 5: Write the Foundation

The foundation is the authoritative operational truth for the domain.

It may contain:

- terminology;
- invariants;
- variables;
- detailed process;
- data structures;
- decision rules;
- hard blockers;
- failure recovery;
- resolved domain decisions.

Do not put presentation styling in the foundation.

### Step 6: Write Specialized Contracts

Create contracts only when they represent a distinct concern:

- structure;
- style;
- security;
- testing;
- target policy;
- review handling;
- release;
- operations.

A contract should define obligations, not repeat the entire foundation.

### Step 7: Add Implementation References

Separate implementation examples by runtime or framework when appropriate.

Examples:

```text
references/node_implementations.md
references/python_implementations.md
references/supabase_implementation.md
references/playwright_implementation.md
```

Mark platform facts that require current verification.

### Step 8: Add Templates

Templates should contain placeholders and exact required sections.

Never place real secrets, live tokens, account identifiers, or project-specific credentials in templates.

### Step 9: Validate

Run:

```bash
python tools/validate_skill_package.py /path/to/skill
```

Then perform the behavioral checks in `references/testing_contract.md`.

### Step 10: Produce Handoff

Return:

```yaml
PACKAGE_PATH:
SKILL_NAME:
MODE:
FILES_CREATED:
FILES_REUSED:
PRIMARY_REFERENCE:
SPECIALIZED_REFERENCES:
VALIDATION_RESULTS:
KNOWN_LIMITATIONS:
EXTERNAL_FACTS_TO_REVERIFY:
NEXT_ACTION:
```

## Required Outputs

For a new or refactored skill, produce:

- complete folder;
- complete `SKILL.md`;
- all referenced files;
- package validation result;
- concise change summary;
- exact next action.

When practical, also produce a `.zip`.

## Completion Gate

A package is complete only when:

```yaml
FRONTMATTER_VALID: true
SINGLE_CONTROLLER_H1: true
PRIMARY_REFERENCE_EXISTS: true
ALL_REFERENCES_RESOLVE: true
CONTROLLER_IS_COMPACT: true
DOMAIN_RULES_PRESERVED: true
DUPLICATION_REVIEWED: true
EXTERNAL_FACTS_MARKED: true
TESTING_CONTRACT_EXISTS: true
HANDOFF_DEFINED: true
VALIDATOR_PASSES: true
```

## Final Instruction

Do not optimize for the fewest files. Optimize for the fewest competing sources of truth.

Keep stable domain rules authoritative, changeable platform facts isolated, and the controller easy to scan.
