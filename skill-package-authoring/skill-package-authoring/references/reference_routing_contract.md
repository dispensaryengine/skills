# Reference Routing Contract

## Controller

Place content in `SKILL.md` when the agent needs it on nearly every activation.

Examples:

- activation;
- operating modes;
- reference map;
- high-level workflow;
- completion gate;
- handoff schema.

## Foundation

Place content in the foundation when it is stable domain truth.

Examples:

- terminology;
- object definitions;
- schemas;
- hard rules;
- pipeline;
- resolved domain decisions;
- failure categories.

## Structure Contract

Place content here when it defines sequence or organization.

Examples:

- required sections;
- field order;
- workflow phase order;
- artifact hierarchy.

## Style Contract

Place content here when it affects presentation rather than system behavior.

Examples:

- typography;
- page spacing;
- heading appearance;
- color;
- worked-example visual layout.

Do not load a style contract for ordinary source-code implementation unless its rules also govern code artifacts.

## Security Contract

Place content here when it protects credentials, data, permissions, users, or infrastructure.

Examples:

- secret storage;
- redaction;
- allowlists;
- authorization;
- SSRF protection;
- privacy;
- audit logging.

## Testing Contract

Place content here when it defines proof.

Examples:

- unit tests;
- integration tests;
- regression fixtures;
- acceptance thresholds;
- release gates;
- evidence format.

## Review Contract

Place content here when human decisions alter future behavior.

Examples:

- review queue;
- approval states;
- rejected near-matches;
- alias learning;
- decision provenance.

## Operations Runbook

Place content here when it helps deploy, operate, recover, or continue.

Examples:

- setup;
- environment variables;
- deployment;
- troubleshooting;
- rollback;
- emergency disable;
- work log;
- handoff.

## Implementation Reference

Place code and version-sensitive library behavior here.

Split by language, framework, or platform when that prevents irrelevant context.

## Template

Place skeleton content here when it is copied and filled in.

## Placement Test

Ask:

```text
Will nearly every activation need this?
    yes → controller summary
    no  → reference

Is this stable domain truth?
    yes → foundation

Is this a narrow obligation?
    yes → contract

Is this code or version-sensitive platform behavior?
    yes → implementation reference

Is this meant to be copied?
    yes → template
```
