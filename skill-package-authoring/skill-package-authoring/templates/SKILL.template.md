---
name: {{skill-slug}}
description: {{what the skill does, major outcomes, and when it activates}}
---

# {{Skill Title}}

{{One or two sentence operational purpose.}}

## Primary Reference

Read `references/{{foundation_name}}.md` first.

It defines:

- {{foundation concern}}
- {{foundation concern}}
- {{foundation concern}}

## Supporting References

Read only what the current task requires:

- `references/structure_contract.md` — {{purpose}}
- `references/testing_contract.md` — {{purpose}}
- `references/security_contract.md` — {{optional purpose}}
- `references/operations_runbook.md` — {{optional purpose}}
- `references/{{runtime}}_implementations.md` — {{optional purpose}}

## Core Principle

**{{Central invariant.}}**

## Operating Modes

```yaml
MODE: "{{mode-a}} | {{mode-b}} | {{mode-c}}"
```

### {{Mode A}}

{{Difference in behavior.}}

## Inputs

```yaml
{{VARIABLE}}: ""
{{VARIABLE}}: []
```

## Workflow

### Step 1: Inspect

{{Actions.}}

### Step 2: Define Target State

{{Actions.}}

### Step 3: Execute

{{Actions.}}

### Step 4: Validate

{{Actions.}}

### Step 5: Handoff

{{Actions.}}

## Required Outputs

- {{artifact}}
- {{artifact}}
- {{state}}

## Completion Gate

```yaml
{{CONDITION}}: true
{{CONDITION}}: true
```

## Final Instruction

{{Exact agent behavior at activation.}}
