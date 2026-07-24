# Apify Proxy Structure Contract

## Required Implementation Sequence

### 1. System Overview

Define:

- runtime;
- target domains;
- request technology;
- browser requirement;
- deployment environment;
- geographic requirement.

### 2. Direct Baseline

Record:

```yaml
URL:
STATUS:
FINAL_URL:
BODY_SIZE:
LATENCY:
BLOCK_SIGNAL:
PARSER_RESULT:
```

### 3. Target Policy

Define one policy per target before embedding conditions in code.

### 4. Environment Contract

Create `.env.example` and identify the real secret source.

### 5. Central Proxy Abstraction

One module owns:

- username;
- password lookup;
- URL or proxy object;
- tier;
- session;
- redaction.

### 6. Session Contract

Define session mode, TTL, failure cap, and retirement.

### 7. Retry Contract

Define retryable failure types, backoff, rotation, and circuit breaker.

### 8. Traffic Contract

Define resource blocking, request/page/byte caps, and concurrency.

### 9. Security Contract

Apply target allowlisting, redaction, and SSRF controls.

### 10. Validation Contract

Verify egress, geography, sessions, target behavior, budgets, and emergency disable.

### 11. Operational Artifacts

Create or update:

```text
docs/PROXY_ARCHITECTURE.md
config/proxy_target_policies.yaml
docs/PROXY_TEST_STATUS.md
docs/PROXY_RUNBOOK.md
.env.example
```

### 12. Handoff

```yaml
STATUS:
TARGETS_CONFIGURED:
LOWEST_WORKING_TIER:
TESTS:
TRAFFIC:
BLOCKERS:
NEXT_ACTION:
```
