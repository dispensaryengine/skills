# Apify Proxy Foundation

Last official documentation review: 2026-07-24

## 1. Purpose

This file is the authoritative operational specification for using Apify Proxy in the project.

Stable architectural rules and project defaults live here.

Version-sensitive library examples live in separate implementation references.

---

## 2. System Boundary

Preferred architecture:

```text
Scheduler / API / Queue
          ↓
Scraper Worker
          ↓
Proxy Routing Layer
direct / datacenter / residential
          ↓
Authorized Target
          ↓
Raw Extraction
          ↓
Validation / Normalization / Storage
```

The proxy routing layer must not own domain normalization or storage decisions.

---

## 3. Official Connection Facts

For an external connection:

```yaml
HOST: "proxy.apify.com"
PORT: 8000
PROTOCOL: "http"
PASSWORD_SOURCE: "Apify Console proxy credential"
```

The username carries proxy parameters.

Examples:

```text
auto
groups-RESIDENTIAL
groups-RESIDENTIAL,country-US
groups-RESIDENTIAL,country-US_NY
groups-RESIDENTIAL,country-US_NY,session-menu_52
```

Important:

- the username is not the Apify account username;
- the password is not the normal Apify account password;
- external connections require eligible paid access;
- the project must verify current plan and group access;
- the credential must remain server-side.

Official references:

- https://docs.apify.com/proxy
- https://docs.apify.com/proxy/residential-proxy
- https://docs.apify.com/proxy/datacenter-proxy

---

## 4. Core Variables

### Connection

```yaml
APIFY_PROXY_ENABLED: true
APIFY_PROXY_HOST: "proxy.apify.com"
APIFY_PROXY_PORT: 8000
APIFY_PROXY_PASSWORD_ENV: "APIFY_PROXY_PASSWORD"
APIFY_PROXY_GROUP: "RESIDENTIAL"
```

### Routing

```yaml
PROXY_MODE: "target_policy"
DEFAULT_PROXY_TIER: "direct"
ALLOW_DATACENTER_ESCALATION: true
ALLOW_RESIDENTIAL_ESCALATION: true
```

### Geography

```yaml
PROXY_COUNTRY_CODE: ""
PROXY_US_STATE_CODE: ""
GEO_TARGET_REQUIRED: false
GEO_FALLBACK_ALLOWED: false
```

### Sessions

```yaml
SESSION_MODE: "rotate_per_job"
SESSION_PREFIX: "scraper"
SESSION_TTL_MINUTES: 25
SESSION_MAX_REQUESTS: 50
SESSION_MAX_FAILURES: 2
SESSION_MAX_LATENCY_MS: 8000
```

Residential proxy sessions generally persist around 30 minutes, but hosts can disappear sooner. A shorter internal TTL is a conservative project policy.

### Retry

```yaml
MAX_REQUEST_ATTEMPTS: 4
MAX_PROXY_ATTEMPTS_PER_TIER: 2
RETRY_BASE_DELAY_MS: 1000
RETRY_MAX_DELAY_MS: 15000
RETRY_JITTER_RATIO: 0.25
```

### Traffic

```yaml
BLOCK_IMAGES: true
BLOCK_MEDIA: true
BLOCK_FONTS: true
BLOCK_ANALYTICS: true
BLOCK_ADS: true
MAX_PAGE_BYTES: 10000000
RESIDENTIAL_MAX_BYTES_PER_JOB: 50000000
RESIDENTIAL_MAX_REQUESTS_PER_JOB: 500
RESIDENTIAL_MAX_BROWSER_PAGES_PER_JOB: 100
STOP_JOB_ON_BUDGET_EXCEEDED: true
```

These are starter values. Set per project and target.

### Concurrency

```yaml
DIRECT_CONCURRENCY: 10
DATACENTER_CONCURRENCY: 5
RESIDENTIAL_CONCURRENCY: 2
PER_DOMAIN_CONCURRENCY: 2
MIN_DELAY_BETWEEN_REQUESTS_MS: 500
MAX_DELAY_BETWEEN_REQUESTS_MS: 2500
```

---

## 5. Username Contract

### Required parts

Residential:

```text
groups-RESIDENTIAL
```

Country:

```text
country-CC
```

US state:

```text
country-US_XX
```

Session:

```text
session-SESSION_ID
```

### Session ID rules

Session IDs:

- may contain letters;
- may contain numbers;
- may contain `.`, `_`, or `~`;
- must not exceed 50 characters;
- must not contain secrets or raw personal identifiers.

### Sanitization

```text
1. Convert unsupported characters to `_`.
2. Collapse repeated separators.
3. Trim separators.
4. Add a project prefix.
5. Hash sensitive source material.
6. Truncate to 50 characters.
```

---

## 6. Routing Tiers

### Tier 0 — Direct HTTP

Use for:

- public HTML;
- public JSON;
- stable lightweight endpoints;
- targets that do not require JavaScript.

### Tier 1 — Direct Browser

Use when:

- JavaScript generates required data;
- the browser reveals a public network request;
- rendering is necessary.

### Tier 2 — Datacenter Proxy

Use when:

- direct egress is blocked;
- residential identity is not required;
- speed and lower cost matter.

### Tier 3 — Residential Proxy

Use when:

- datacenter IPs are blocked;
- residential origin is required;
- geographic residential targeting is required.

### Tier 4 — Residential Browser

Use only when both browser behavior and residential routing are necessary.

---

## 7. Escalation Rules

Escalate on evidence of:

- persistent target-specific IP block;
- persistent rate limit tied to egress;
- geofenced content;
- challenge page;
- server-environment response that differs from an authorized local baseline.

Do not escalate on:

- invalid selector;
- malformed request;
- missing URL;
- expired login;
- parser exception;
- database error;
- schema mismatch;
- permanent product removal.

---

## 8. Target Block Classification

A block detector may use:

```yaml
STATUS_CODES: [401, 403, 429]
TITLE_PATTERNS:
  - "access denied"
  - "just a moment"
BODY_PATTERNS:
  - "verify you are human"
  - "unusual traffic"
  - "request blocked"
OTHER:
  - repeated redirect loop
  - challenge widget
  - unexpectedly small body
```

A status code alone is not always a block.

Log the exact signal.

---

## 9. Session Modes

### Rotate per request

No explicit session ID.

Use for stateless requests.

### Rotate per job

One session per extraction job.

Use for a coherent crawl that does not need long-term identity.

### Sticky per domain

One session per target domain.

Use when cookies or continuity matter.

### Sticky per account

Use only for an account the operator is authorized to access.

Bind:

- proxy session;
- cookies;
- local storage;
- authentication state;
- browser context;
- fingerprint strategy.

---

## 10. Session Health

Track:

```yaml
SESSION_HASH:
CREATED_AT:
LAST_USED_AT:
REQUEST_COUNT:
SUCCESS_COUNT:
FAILURE_COUNT:
BLOCK_COUNT:
AVERAGE_LATENCY_MS:
LAST_STATUS:
RETIRED_REASON:
```

Retire when:

```text
age exceeds internal TTL
OR request cap reached
OR failure cap reached
OR repeated block signal occurs
OR latency remains above threshold
OR connection is destroyed
```

---

## 11. Retry and Rotation

Classify:

```text
TARGET_RESPONSE
TARGET_BLOCK
PROXY_AUTH
PROXY_CONNECTION
DNS_FAILURE
TIMEOUT
PARSER_FAILURE
BROWSER_FAILURE
APPLICATION_FAILURE
BUDGET_FAILURE
```

Decision:

```text
credentials invalid
    → stop immediately

valid response but parser failed
    → do not rotate proxy

permanent missing target
    → do not retry

confirmed block
    → retire session and escalate within policy

transient connection failure
    → bounded retry with backoff

budget exhausted
    → stop or downgrade according to policy
```

Backoff:

```text
delay =
min(max_delay, base_delay × 2^(attempt - 1))
× random(1 - jitter, 1 + jitter)
```

---

## 12. Apify 590–599 Statuses

Apify documents proxy-specific statuses:

```text
590  upstream returned non-success
591  reserved
592  upstream status outside expected range
593  DNS lookup failure
594  connection refused
595  connection reset or timeout
596  broken pipe
597  upstream authentication failed
598  reserved
599  generic upstream error
```

Project behavior:

- `590` and `592`: inspect upstream result; do not automatically rotate forever;
- `593`: validate destination and proxy configuration;
- `594`, `595`, `596`: bounded rotation/retry;
- `597`: fail fast and inspect credentials;
- `599`: bounded retry, then open circuit.

Verify current meanings against official docs before relying on exact semantics in production.

---

## 13. Circuit Breaker

Per domain starter policy:

```yaml
WINDOW_REQUESTS: 20
OPEN_WHEN_FAILURE_RATE: 0.60
OPEN_DURATION_SECONDS: 300
HALF_OPEN_PROBE_REQUESTS: 2
```

When open:

- stop residential spending for that target;
- allow unrelated targets to continue;
- record a blocker;
- probe only after the open interval.

---

## 14. Traffic Control

Residential proxy is traffic-priced.

Therefore:

1. prefer public JSON/API responses;
2. block unnecessary assets before navigation;
3. cap response bytes;
4. cap requests and pages;
5. avoid screenshots, traces, and video by default;
6. deduplicate URLs;
7. cache where freshness permits;
8. stop when required data is obtained;
9. use datacenter for larger transfers when it satisfies the requirement;
10. record traffic by job, domain, and tier.

---

## 15. Cost Ledger

Track:

```yaml
JOB_ID:
TARGET:
PROXY_TIER:
REQUESTS:
SUCCESSES:
FAILURES:
BYTES_RECEIVED:
BYTES_SENT:
BROWSER_PAGES:
SESSIONS_CREATED:
SESSIONS_RETIRED:
ESCALATIONS:
```

Do not depend only on account-level limits.

---

## 16. Observability

Structured event:

```json
{
  "event": "proxy_request_complete",
  "jobId": "job_123",
  "target": "example.com",
  "tier": "residential",
  "sessionHash": "c4d3",
  "attempt": 2,
  "status": 200,
  "latencyMs": 1840,
  "responseBytes": 92134,
  "blockSignal": null
}
```

Recommended metrics:

```text
proxy_requests_total
proxy_request_duration_ms
proxy_bytes_total
proxy_sessions_created_total
proxy_sessions_retired_total
proxy_escalations_total
proxy_blocks_total
proxy_budget_remaining_bytes
proxy_circuit_state
```

---

## 17. Validation Endpoint

For proxy egress testing, Apify documents:

```text
https://api.apify.com/v2/browser-info/
```

Validation must observe actual results.

Do not expose the full proxy URL in test output.

---

## 18. Resolved Architecture Rules

- Apify Actors are optional.
- External applications can use Apify Proxy.
- Proxy routing is a separate infrastructure layer.
- Direct access is the default project tier.
- Residential proxy is an escalation tier unless a target policy proves otherwise.
- Target policies are centralized.
- Session identity is not scattered through extraction code.
- Browser traffic is controlled before navigation.
- Retries are bounded.
- Budgets are enforced inside the job.
- Credential or target access failures are not disguised as parser failures.

---

## 19. Final Rule

**Use the lowest-cost routing tier that reliably returns the authorized target data, and prove the observed behavior before declaring the proxy configuration complete.**
