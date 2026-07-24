# Modular Skill Package Foundation

## 1. Purpose

A skill package is a durable operating system for an agent task.

It must do more than provide advice. It must tell the agent:

- when to activate;
- what sources are authoritative;
- what variables to resolve;
- what workflow to execute;
- what outputs to create;
- how to validate the result;
- how to recover from failure;
- what state to leave for continuation.

The package must remain understandable without prior conversation context.

---

## 2. Package Model

Use:

```text
SKILL.md
    Controller and reference router

references/foundation.md
    Stable domain truth and operational rules

references/*_contract.md
    Narrow obligations for structure, testing, security, style, review, release, or policy

references/*_implementations.md
    Runtime- or framework-specific implementation patterns

templates/
    Reusable configuration and artifact skeletons

tools/
    Optional deterministic validators or generators
```

---

## 3. Core Variables

Resolve:

```yaml
SKILL_NAME: ""
SKILL_SLUG: ""
SKILL_VERSION: "1.0.0"
SKILL_PURPOSE: ""
PRIMARY_USER_GOAL: ""
ACTIVATION_SIGNALS: []
OPERATING_MODES: []
REQUIRED_INPUTS: []
OPTIONAL_INPUTS: []
REQUIRED_OUTPUTS: []
PRIMARY_REFERENCE: ""
SUPPORTING_REFERENCES: []
IMPLEMENTATION_REFERENCES: []
TEMPLATES: []
VALIDATION_METHODS: []
EXTERNAL_FACTS: []
SAFETY_BOUNDARIES: []
KNOWN_LIMITATIONS: []
```

---

## 4. Frontmatter Contract

Use:

```yaml
---
name: lowercase-hyphenated-name
description: One paragraph describing what the skill does and when it should activate.
---
```

### Name rules

- lowercase;
- hyphen-separated;
- descriptive;
- stable across versions;
- no marketing language;
- no file extension.

### Description rules

The description must contain:

1. the outcome;
2. the major task types;
3. the activation context;
4. important domain terminology where useful.

Do not add a separate trigger array unless the target platform requires it.

---

## 5. Controller Responsibilities

`SKILL.md` owns:

- identity;
- activation;
- reference routing;
- core principle;
- operating modes;
- high-level workflow;
- required outputs;
- completion gate;
- handoff.

`SKILL.md` does not own:

- full SQL schemas;
- giant normalization tables;
- every code example;
- full platform manuals;
- long troubleshooting catalogs;
- detailed document typography;
- exhaustive test cases;
- historical work logs.

Recommended target: 100–350 lines.

This is a guideline, not a magical law. A controller may exceed it when necessary, but every extra section must justify why it cannot live in a reference.

---

## 6. Foundation Responsibilities

The foundation owns stable domain truth:

- terminology;
- object definitions;
- pipeline;
- invariants;
- schemas;
- hard rules;
- decision logic;
- resolved assumptions;
- failure classification;
- domain-specific examples.

One foundation should be authoritative.

Do not create competing files such as:

```text
foundation.md
foundation-v2.md
final-foundation.md
actual-foundation.md
new-rules.md
```

Version the package or update the authoritative file.

---

## 7. Contract Responsibilities

A contract defines a narrow obligation.

Examples:

### Structure contract

Defines required section or execution order.

### Style contract

Defines presentation requirements for generated artifacts.

### Testing contract

Defines tests, gates, fixtures, and evidence.

### Security contract

Defines secrets, permissions, data boundaries, and abuse prevention.

### Review contract

Defines human review queues, decisions, learning, and rejected cases.

### Operations runbook

Defines setup, deployment, failure response, rollback, and continuation.

Contracts should point to the foundation rather than restating it wholesale.

---

## 8. Implementation Reference Responsibilities

Implementation references contain code and framework details.

Split when:

- multiple languages are supported;
- framework APIs change independently;
- examples exceed the controller;
- one runtime is irrelevant to another;
- platform behavior requires fresh verification.

Each implementation reference should state:

```yaml
RUNTIME:
SUPPORTED_LIBRARIES:
LAST_VERIFIED:
OFFICIAL_SOURCES:
VERSION_SENSITIVE_AREAS:
```

Do not present a version-sensitive API as timeless.

---

## 9. Reference Routing

Use conditional loading.

Example:

```text
Every task:
- foundation
- structure contract

Node.js implementation:
- node implementations
- testing contract

Formal PDF output:
- style contract

Production API exposure:
- security contract
- operations runbook
```

This reduces context waste and contradictory instructions.

---

## 10. Operating Modes

A robust skill should define modes when the workflow materially changes.

Common modes:

```text
create
inspect
implement
repair
migrate
audit
document
review
release
handoff
```

Do not create modes that only rename the same workflow.

---

## 11. Workflow Design

A reusable workflow normally follows:

```text
Inspect
→ resolve variables
→ establish baseline
→ define target state
→ execute smallest complete unit
→ validate
→ record decisions
→ produce handoff
```

Every phase needs:

- objective;
- actions;
- output;
- exit gate.

---

## 12. Evidence Rules

The skill must distinguish:

- observed;
- source-derived;
- user-confirmed;
- assumed;
- inferred;
- planned;
- implemented;
- verified.

Never allow “written” to mean “working.”

Never allow “appears correct” to mean “tests passed.”

---

## 13. External Fact Isolation

External platform details can change.

Examples:

- endpoint syntax;
- plan eligibility;
- pricing;
- SDK parameters;
- rate limits;
- supported regions;
- deployment constraints.

Put these in an implementation or platform reference with:

- official source;
- last verified date;
- instruction to re-check when material.

Stable design principles remain in the foundation.

---

## 14. Duplication Policy

Some repetition is useful for navigation.

Allowed:

- one-sentence summaries;
- key invariant repeated in controller and foundation;
- reference names and purpose;
- final completion checklist.

Not allowed:

- copied multi-page tables;
- duplicated schemas;
- conflicting threshold lists;
- parallel definitions of the same object;
- code examples copied into several references.

---

## 15. Versioning

Use semantic intent:

```text
PATCH
Typo, link, wording, non-behavioral clarification

MINOR
Backward-compatible new workflow, reference, template, or optional mode

MAJOR
Changed required behavior, terminology, object contract, or output contract
```

Record version changes in `CHANGELOG.md` when the package is actively maintained.

---

## 16. Deprecation

When replacing a reference or rule:

1. update the controller;
2. move consumers to the new authority;
3. mark the old item deprecated;
4. explain replacement and migration;
5. remove only after no references remain.

Do not leave silent dead references.

---

## 17. Package Completion State

Every created or modified package should end with:

```yaml
PACKAGE_STATUS: "complete | partial | blocked"
VERSION:
PRIMARY_REFERENCE:
CONTROLLER_LINES:
REFERENCES:
TEMPLATES:
VALIDATION:
UNRESOLVED_CONFLICTS:
EXTERNAL_FACTS_TO_REVERIFY:
NEXT_ACTION:
```

---

## 18. Final Rule

A skill package succeeds when the agent can execute it correctly without having to rediscover the domain from conversation history.

The controller tells the agent where to look.

The foundation tells the agent what is true.

The contracts tell the agent what must be satisfied.

The tests prove whether it worked.
