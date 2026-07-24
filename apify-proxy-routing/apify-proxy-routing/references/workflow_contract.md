# Apify Proxy Workflow Contract

## 1. Inspect the Existing Scraper

Determine:

- runtime location;
- HTTP library;
- browser library;
- target domains;
- whether JavaScript is required;
- cookies and session handling;
- retry behavior;
- current proxy code;
- secret storage;
- direct-access results;
- observed failures;
- expected scale and traffic.

Output:

```yaml
RUNTIME:
TARGETS:
CURRENT_PROXY_STATE:
DIRECT_BASELINE:
PRIMARY_FAILURE:
SECURITY_BOUNDARY:
```

Do not change architecture before capturing the current state.

---

## 2. Establish a Direct Baseline

Run the smallest valid target request without a proxy.

Classify:

```text
DIRECT_SUCCESS
GEOGRAPHIC_MISMATCH
IP_BLOCK
RATE_LIMIT
JAVASCRIPT_REQUIRED
AUTH_FAILURE
PARSER_FAILURE
TARGET_MISSING
UNKNOWN
```

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

A parser failure is not a proxy failure.

---

## 3. Define Target Policies

Create or update `proxy_target_policies.yaml`.

For every target, define:

- initial tier;
- maximum tier;
- browser requirement;
- country or US state;
- session mode;
- concurrency;
- request delay;
- retry cap;
- block signals;
- resource blocking;
- byte/request/page budget;
- direct fallback or fail-closed behavior.

Do not scatter target conditions throughout scraper files.

---

## 4. Implement One Proxy Abstraction

One provider or routing module owns:

- username construction;
- credential access;
- proxy URL or proxy object;
- tier selection;
- session identifiers;
- redaction;
- request metadata.

Extraction code requests a routing decision.

It does not reconstruct credentials.

---

## 5. Implement Tier Selection

Default order:

```text
Direct lightweight HTTP
→ direct browser when JavaScript is required
→ datacenter proxy
→ residential proxy
→ residential browser with geographic targeting
```

A target may start higher only when evidence or an explicit requirement justifies it.

Do not burn residential traffic as a reflex.

---

## 6. Implement Session Lifecycle

Choose:

```text
rotate_per_request
rotate_per_job
sticky_per_domain
sticky_per_account
```

For authenticated sessions, bind:

- cookies;
- storage;
- browser context;
- fingerprint;
- proxy session.

Retire sessions using the health rules in `proxy_foundation.md`.

---

## 7. Implement Retry, Rotation, and Circuit Breaking

Required:

- failure classification;
- capped attempts;
- exponential backoff with jitter;
- session retirement;
- no rotation for parser failures;
- fail-fast credentials;
- per-target circuit breaker;
- resumable job state.

Persist enough state to resume without restarting the entire crawl.

---

## 8. Control Traffic and Cost

Before browser navigation:

- block unneeded images;
- block unneeded media;
- block unneeded fonts;
- block known analytics and advertisements;
- preserve required scripts and stylesheets.

Enforce:

- bytes per job;
- requests per job;
- pages per job;
- residential concurrency;
- per-domain concurrency;
- retry cap.

Prefer an authorized public JSON or API response over full rendering when equivalent.

---

## 9. Secure the Boundary

Apply `security_contract.md`.

At minimum:

- server-side credential;
- redacted logs;
- allowlisted target hosts;
- private-network rejection;
- redirect validation;
- protected job triggers;
- no client-side proxy credentials;
- no secrets in process arguments.

---

## 10. Validate Proxy Behavior

Verify:

1. connectivity;
2. observed egress;
3. requested geography;
4. sticky-session reuse;
5. session rotation;
6. direct-versus-proxy target behavior;
7. lowest working tier;
8. resource blocking;
9. budget enforcement;
10. emergency disable;
11. redaction.

Do not infer success from configuration alone.

---

## 11. Update Operational Artifacts

Create or update:

```text
docs/PROXY_ARCHITECTURE.md
config/proxy_target_policies.yaml
docs/PROXY_TEST_STATUS.md
docs/PROXY_RUNBOOK.md
.env.example
```

Use existing project conventions when equivalent artifacts already exist.

---

## 12. Produce Handoff

Return:

```yaml
STATUS:
RUNTIME:
TARGETS_CONFIGURED:
TARGETS_VERIFIED:
LOWEST_WORKING_TIER:
GEOGRAPHY_VERIFIED:
SESSION_MODE:
TRAFFIC_USAGE:
BUDGET_CONTROLS:
SECURITY_CONTROLS:
TESTS_RUN:
FAILED_TESTS:
BLOCKERS:
NEXT_ACTION:
```
