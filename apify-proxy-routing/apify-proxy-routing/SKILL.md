---
name: apify-proxy-routing
description: Configure, implement, audit, and operate Apify Proxy from external scrapers, browser workers, APIs, containers, VPS deployments, CI jobs, local applications, or Apify Actors. Use when adding residential or datacenter proxy routing, geographic targeting, sticky sessions, bounded retries, target-specific escalation, traffic and cost controls, or proxy-backed Playwright, Crawlee, Node.js, or Python scraping.
---

# Apify Proxy Routing

Use Apify as a proxy provider without making Apify Actors a required application runtime.

## Primary Reference

Read `references/proxy_foundation.md` first.

It defines:

- connection and routing variables;
- direct, datacenter, and residential tiers;
- geographic targeting;
- session lifecycle;
- retry and rotation rules;
- traffic budgets;
- failure classification;
- observability;
- resolved architectural decisions.

## Supporting References

Read only what the current implementation requires:

- `references/workflow_contract.md` — complete implementation sequence
- `references/structure_contract.md` — required artifacts and handoff structure
- `references/target_policy_contract.md` — target policy schema and routing decisions
- `references/security_contract.md` — secrets, URL validation, SSRF, and abuse prevention
- `references/testing_contract.md` — proxy and target validation
- `references/node_implementations.md` — Node.js, Playwright, Crawlee, and Undici
- `references/python_implementations.md` — Python requests, HTTPX, and Playwright
- `references/operations_runbook.md` — deployment, incidents, budgets, and continuation
- `templates/proxy_target_policies.yaml` — target policy starter
- `templates/.env.example` — environment variable starter

## Core Principle

**Apify is the proxy provider. The scraper, normalizer, database, and scheduler remain independent services.**

Keep proxy routing separate from extraction, parsing, normalization, persistence, identity, review logic, and API presentation.

## Operating Modes

```yaml
PROXY_WORK_MODE: "implement | repair | migrate | audit | document"
RUNTIME_LOCATION: "local | docker | vps | ci | serverless | apify_actor | other"
ROUTING_MODE: "off | always | fallback | target_policy"
```

### Implement

Add proxy routing to an application that does not have it.

### Repair

Diagnose credentials, sessions, routing, target blocks, traffic spikes, or connection failures.

### Migrate

Remove the scraper's dependency on Apify Actors while preserving Apify Proxy access.

### Audit

Inspect security, cost, routing, retries, sessions, and target policies without changing behavior.

### Document

Produce architecture, target policy, test status, or operations artifacts.

## Required Inputs

Resolve:

```yaml
TARGET_DOMAINS: []
HTTP_LIBRARY: ""
BROWSER_LIBRARY: ""
DEPLOYMENT_ENVIRONMENT: ""
DIRECT_BASELINE: "unknown | pass | fail"
GEOGRAPHIC_REQUIREMENT: ""
AUTHENTICATED_TARGET_SESSION: false
EXPECTED_REQUEST_VOLUME: ""
EXPECTED_RESPONSE_SIZE: ""
AVAILABLE_PROXY_GROUPS: []
SECRET_SOURCE: ""
```

Inspect the project before asking for values that are already available.

Do not invent plan access, available proxy groups, target behavior, or library versions.

## Reference Routing

### Every implementation

Read:

- `references/proxy_foundation.md`
- `references/workflow_contract.md`
- `references/target_policy_contract.md`
- `references/testing_contract.md`

### Node.js, TypeScript, Playwright, Crawlee, or Undici

Also read `references/node_implementations.md`.

### Python, requests, HTTPX, or Python Playwright

Also read `references/python_implementations.md`.

### Public API, user-controlled target, authenticated session, or production deployment

Also read:

- `references/security_contract.md`
- `references/operations_runbook.md`

### Current Apify behavior

Reverify version-sensitive facts against official Apify documentation when they materially affect implementation.

## Workflow

Follow `references/workflow_contract.md`.

The required sequence is:

1. inspect the scraper and deployment;
2. capture a direct baseline;
3. define one target policy per domain;
4. implement one central proxy abstraction;
5. select the lowest valid routing tier;
6. manage sessions coherently;
7. classify failures before retrying;
8. enforce traffic and budget limits;
9. secure the target boundary;
10. validate observed egress and target behavior;
11. update operational artifacts;
12. produce exact handoff state.

Do not use residential traffic merely because it is available.

Do not use proxy rotation to hide parser, authentication, URL, or database failures.

## Required Outputs

Depending on mode:

- central proxy routing module;
- target policy registry;
- environment example;
- connectivity and target tests;
- architecture record;
- security controls;
- operations runbook;
- verified handoff state.

Do not create duplicate artifacts when the repository already has an authoritative equivalent.

## Validation

Use `references/testing_contract.md`.

Configuration text is not proof.

At minimum verify:

- proxy connectivity;
- observed egress;
- requested geography;
- sticky session behavior;
- session rotation;
- lowest working target tier;
- resource blocking;
- budget enforcement;
- emergency disable;
- secret redaction.

## Handoff

Return:

```yaml
STATUS: "complete | partial | blocked"
RUNTIME:
TARGETS_CONFIGURED:
TARGETS_VERIFIED:
LOWEST_WORKING_TIER:
GEOGRAPHY_VERIFIED:
SESSION_MODE:
BUDGET_CONTROLS:
SECURITY_CONTROLS:
TESTS_RUN:
FAILED_TESTS:
KNOWN_BLOCKERS:
EXTERNAL_FACTS_REVERIFIED:
NEXT_ACTION:
```

## Completion Gate

```yaml
DIRECT_BASELINE_RECORDED: true
TARGET_POLICY_DEFINED: true
CENTRAL_PROXY_ABSTRACTION: true
SECRET_STORAGE_VERIFIED: true
SECRET_REDACTION_VERIFIED: true
PROXY_CONNECTIVITY_VERIFIED: true
TARGET_BEHAVIOR_VERIFIED: true
RETRY_CAP_VERIFIED: true
SESSION_RETIREMENT_VERIFIED: true
TRAFFIC_BUDGET_VERIFIED: true
EMERGENCY_DISABLE_VERIFIED: true
HANDOFF_UPDATED: true
```

## Final Instruction

Use the lowest-cost routing tier that reliably satisfies the authorized target requirement.

Do not use Apify Actors unless the project intentionally chooses Apify as the runtime.
