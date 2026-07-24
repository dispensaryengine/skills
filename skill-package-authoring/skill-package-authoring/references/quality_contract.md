# Skill Package Quality Contract

## Quality Dimensions

Score each from 0–2:

```text
Activation clarity
Reference authority
Workflow completeness
Output specificity
Validation strength
Failure recovery
Maintainability
External fact isolation
Security boundaries
Handoff quality
```

Maximum: 20.

Interpretation:

```text
18–20  release-ready
15–17  usable with minor repairs
10–14  structurally weak
0–9    rebuild
```

## Required Quality Gates

### Activation

- The description identifies when to use the skill.
- Activation does not depend on a hidden keyword list alone.

### Authority

- One foundation is authoritative.
- Conflicts have a resolution rule.

### Execution

- Workflow is ordered.
- Each phase produces evidence.
- Completion is measurable.

### Maintainability

- Controller is scan-friendly.
- Detailed rules are not duplicated.
- References have clear purposes.

### Truthfulness

- “Implemented,” “tested,” and “deployed” are distinct.
- External facts are marked for verification.
- Missing evidence is not invented.

### Safety

- Secrets and destructive actions have boundaries.
- User-controlled inputs cannot silently expand privileges.

### Continuation

- Another agent can continue from the handoff.

## Anti-Patterns

Reject:

- one giant `SKILL.md` containing every detail;
- several competing foundation files;
- references that only repeat the controller;
- examples presented as universal rules;
- platform APIs without version context;
- a documentation-only workflow for an implementation skill;
- undefined completion language such as “finish setup”;
- tests that only inspect files and never verify behavior;
- hidden dependence on conversation memory;
- fake success claims.

## Refactor Priority

When repairing a monolith:

1. preserve behavior;
2. extract stable domain rules;
3. extract code examples;
4. extract testing;
5. extract security;
6. simplify controller;
7. validate references;
8. remove duplicate text.
