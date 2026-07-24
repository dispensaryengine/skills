---
name: apify-proxy-routing
version: 1.0.0
description: >
  Configure and operate Apify Proxy from any external scraper, browser worker,
  API client, container, VPS, CI job, or local application. Provides proxy
  selection, residential escalation, geographic targeting, sticky sessions,
  retry and rotation policies, traffic-cost controls, validation, observability,
  and failure recovery without requiring Apify Actors.
triggers:
  - use Apify Proxy
  - configure residential proxies
  - add proxy rotation to a scraper
  - bypass IP-based geographic blocking
  - stabilize a blocked scraper
  - reduce residential proxy traffic
  - add sticky proxy sessions
  - migrate scraping away from Apify Actors
---

# Apify Proxy Routing Skill

## 1. Purpose

Use this skill whenever an application needs to route outbound HTTP or browser
traffic through Apify Proxy.

The application may run in:

- a local development environment;
- Docker;
- a VPS;
- Kubernetes;
- GitHub Actions;
- Factory;
- a serverless worker that supports outbound HTTP proxies;
- a scheduled job;
- a standalone Node.js or Python process;
- an Apify Actor.

Apify Actors are **not required**. Apify Proxy can be used by any application
that supports the HTTP proxy protocol.

This skill must produce a proxy implementation that is:

1. cost-aware;
2. explicit about when residential traffic is used;
3. safe with credentials;
4. observable;
5. resilient to session and connection failure;
6. capable of geographic targeting;
7. easy to disable;
8. testable without scraping the production target;
9. independent of hidden platform state;
10. compliant with the target's applicable access rules and authorization.

---

# 2. Core Architecture Rule

Treat Apify Proxy as infrastructure, not as the scraper runtime.

Preferred architecture:

```text
Scheduler / API / Queue
          ↓
Scraper Worker
HTTP client or Playwright/Crawlee
          ↓
Proxy Routing Layer
direct → datacenter → residential
          ↓
Target Website
          ↓
Raw Extraction
          ↓
Validation / Normalization / Storage
```

The proxy routing layer must remain separate from:

- parsing;
- normalization;
- product identity;
- persistence;
- business logic;
- review queues;
- API presentation.

Only outbound target requests should depend on proxy configuration.

---

# 3. Non-Negotiable Rules

1. Never hard-code the proxy password.
2. Never log the complete proxy URL.
3. Never commit `.env` files containing secrets.
4. Never send the password to a client-side browser.
5. Never use residential proxy traffic by default when direct access works.
6. Never retry indefinitely.
7. Never treat every HTTP failure as an IP block.
8. Never rotate identity halfway through a stateful browser session unless the
   session is intentionally being retired.
9. Never claim proxy routing works until the observed egress IP is verified.
10. Never use proxies to bypass authentication, authorization, paywalls, account
    restrictions, or access controls the operator is not permitted to bypass.
11. Never allow images, video, fonts, or analytics traffic through residential
    proxies unless those resources are required for extraction.
12. Never expose credentials in exception messages, telemetry, screenshots,
    process arguments, or generated documentation.

---

# 4. Configuration Variables

Resolve these variables before implementation.

## 4.1 Connection variables

```yaml
APIFY_PROXY_ENABLED: true
APIFY_PROXY_HOST: "proxy.apify.com"
APIFY_PROXY_PORT: 8000
APIFY_PROXY_PASSWORD_ENV: "APIFY_PROXY_PASSWORD"
APIFY_PROXY_PROTOCOL: "http"
APIFY_PROXY_EXTERNAL_CONNECTION: true
```

For applications running outside the Apify platform, the standard endpoint is:

```text
proxy.apify.com:8000
```

External connections require an eligible paid Apify plan.

## 4.2 Routing variables

```yaml
PROXY_MODE: "off | always | fallback | target_policy"
DEFAULT_PROXY_TIER: "direct | datacenter | residential"
ALLOW_RESIDENTIAL_ESCALATION: true
ALLOW_DATACENTER_ESCALATION: true
RESIDENTIAL_GROUP: "RESIDENTIAL"
DATACENTER_GROUP: "auto"
TARGET_PROXY_POLICIES: {}
```

Recommended default:

```yaml
PROXY_MODE: "target_policy"
DEFAULT_PROXY_TIER: "direct"
ALLOW_DATACENTER_ESCALATION: true
ALLOW_RESIDENTIAL_ESCALATION: true
```

## 4.3 Geographic variables

```yaml
PROXY_COUNTRY_CODE: ""
PROXY_US_STATE_CODE: ""
GEO_TARGET_REQUIRED: false
GEO_FALLBACK_ALLOWED: false
```

Examples:

```yaml
PROXY_COUNTRY_CODE: "US"
PROXY_US_STATE_CODE: "NY"
```

Direct username representation:

```text
groups-RESIDENTIAL,country-US_NY
```

State targeting is only available for United States residential proxies.

## 4.4 Session variables

```yaml
SESSION_MODE: "rotate_per_request | rotate_per_job | sticky_per_domain | sticky_per_account"
SESSION_PREFIX: "scraper"
SESSION_TTL_MINUTES: 25
SESSION_MAX_REQUESTS: 50
SESSION_MAX_FAILURES: 2
SESSION_MAX_LATENCY_MS: 8000
SESSION_REUSE_COOKIES: true
```

Residential sessions generally retain the assigned IP for around 30 minutes,
but the host can disappear sooner. Use a lower internal TTL than the advertised
persistence window.

Recommended:

```yaml
SESSION_TTL_MINUTES: 25
```

## 4.5 Retry variables

```yaml
MAX_REQUEST_ATTEMPTS: 4
MAX_PROXY_ATTEMPTS_PER_TIER: 2
RETRY_BASE_DELAY_MS: 1000
RETRY_MAX_DELAY_MS: 15000
RETRY_JITTER_RATIO: 0.25
ROTATE_ON_STATUS: [401, 403, 407, 429]
ROTATE_ON_PROXY_STATUS: [590, 593, 594, 595, 596, 597, 599]
RETRY_ON_STATUS: [408, 425, 429, 500, 502, 503, 504, 590, 593, 594, 595, 596, 599]
DO_NOT_RETRY_STATUS: [400, 404, 405, 410, 422]
```

These lists are defaults, not blind rules. A target may legitimately return
401, 403, or 404.

## 4.6 Browser traffic variables

```yaml
BLOCK_IMAGES: true
BLOCK_MEDIA: true
BLOCK_FONTS: true
BLOCK_ANALYTICS: true
BLOCK_ADS: true
ALLOW_STYLESHEETS: true
ALLOW_XHR: true
ALLOW_FETCH: true
ALLOW_SCRIPTS: true
MAX_PAGE_BYTES: 10000000
PAGE_TIMEOUT_MS: 60000
NAVIGATION_TIMEOUT_MS: 45000
```

## 4.7 Budget variables

```yaml
RESIDENTIAL_BUDGET_ENABLED: true
RESIDENTIAL_MAX_BYTES_PER_JOB: 50000000
RESIDENTIAL_MAX_REQUESTS_PER_JOB: 500
RESIDENTIAL_MAX_BROWSER_PAGES_PER_JOB: 100
STOP_JOB_ON_BUDGET_EXCEEDED: true
LOG_RESPONSE_BYTES: true
```

Set these values per project. Do not rely only on account-level spending limits.

## 4.8 Concurrency variables

```yaml
DIRECT_CONCURRENCY: 10
DATACENTER_CONCURRENCY: 5
RESIDENTIAL_CONCURRENCY: 2
PER_DOMAIN_CONCURRENCY: 2
MIN_DELAY_BETWEEN_REQUESTS_MS: 500
MAX_DELAY_BETWEEN_REQUESTS_MS: 2500
```

Residential traffic should normally use lower concurrency than direct requests.

## 4.9 Observability variables

```yaml
LOG_PROXY_TIER: true
LOG_SESSION_ID_HASH: true
LOG_EGRESS_COUNTRY: true
LOG_EGRESS_IP: false
LOG_RESPONSE_STATUS: true
LOG_RESPONSE_BYTES: true
LOG_ATTEMPT_NUMBER: true
LOG_PROXY_PASSWORD: false
METRICS_ENABLED: true
```

If the egress IP is logged, treat it as operational telemetry and limit its
retention.

---

# 5. Environment Contract

Create `.env.example`:

```env
APIFY_PROXY_ENABLED=true
APIFY_PROXY_HOST=proxy.apify.com
APIFY_PROXY_PORT=8000
APIFY_PROXY_PASSWORD=
APIFY_PROXY_GROUP=RESIDENTIAL
APIFY_PROXY_COUNTRY=US
APIFY_PROXY_STATE=NY
APIFY_PROXY_MODE=target_policy
```

The real secret must be provided through:

- a deployment secret manager;
- encrypted CI secrets;
- a local ignored `.env`;
- a container secret;
- a protected host environment variable.

Do not use the normal Apify account password or API token in place of the
Apify Proxy password.

---

# 6. Proxy Username Builder

The username contains routing parameters.

## 6.1 Supported patterns

Residential:

```text
groups-RESIDENTIAL
```

Residential with country:

```text
groups-RESIDENTIAL,country-US
```

Residential with US state:

```text
groups-RESIDENTIAL,country-US_NY
```

Residential with sticky session:

```text
groups-RESIDENTIAL,country-US_NY,session-dispensary_01
```

Automatic/default proxy selection:

```text
auto
```

## 6.2 Session ID restrictions

Session identifiers must:

- be at most 50 characters;
- contain only letters, numbers, `.`, `_`, or `~`;
- be deterministic when stickiness is required;
- omit user secrets and personally identifying information.

## 6.3 Sanitization algorithm

```text
1. Convert input to lowercase.
2. Replace unsupported characters with `_`.
3. Collapse repeated `_`.
4. Remove leading and trailing separators.
5. Prefix with the project/session prefix.
6. Hash sensitive identity material.
7. Truncate to 50 characters.
```

Example:

```text
scraper_disp_52_menu_20260724
```

---

# 7. Proxy URL Construction

Format:

```text
http://<username>:<password>@proxy.apify.com:8000
```

Never print the constructed URL.

## 7.1 TypeScript builder

```typescript
type ProxyTier = "direct" | "datacenter" | "residential";

interface ProxyOptions {
  tier: ProxyTier;
  countryCode?: string;
  usStateCode?: string;
  sessionId?: string;
}

function sanitizeSessionId(value: string): string {
  const sanitized = value
    .replace(/[^a-zA-Z0-9._~]/g, "_")
    .replace(/_+/g, "_")
    .replace(/^_+|_+$/g, "");

  return sanitized.slice(0, 50);
}

export function buildApifyProxyUrl(
  options: ProxyOptions,
  env: NodeJS.ProcessEnv = process.env,
): string | undefined {
  if (options.tier === "direct") return undefined;

  const password = env.APIFY_PROXY_PASSWORD;
  if (!password) {
    throw new Error("APIFY_PROXY_PASSWORD is required");
  }

  const host = env.APIFY_PROXY_HOST ?? "proxy.apify.com";
  const port = env.APIFY_PROXY_PORT ?? "8000";

  const usernameParts: string[] = [];

  if (options.tier === "residential") {
    usernameParts.push("groups-RESIDENTIAL");
  } else {
    usernameParts.push("auto");
  }

  if (options.usStateCode) {
    const state = options.usStateCode.toUpperCase();
    if (!/^[A-Z]{2}$/.test(state)) {
      throw new Error("usStateCode must be a two-letter state code");
    }
    usernameParts.push(`country-US_${state}`);
  } else if (options.countryCode) {
    const country = options.countryCode.toUpperCase();
    if (!/^[A-Z]{2}$/.test(country)) {
      throw new Error("countryCode must be a two-letter country code");
    }
    usernameParts.push(`country-${country}`);
  }

  if (options.sessionId) {
    const sessionId = sanitizeSessionId(options.sessionId);
    if (!sessionId) throw new Error("sessionId became empty after sanitization");
    usernameParts.push(`session-${sessionId}`);
  }

  const username = usernameParts.join(",");
  return `http://${encodeURIComponent(username)}:${encodeURIComponent(password)}@${host}:${port}`;
}
```

Note: Some proxy consumers accept username and password as separate fields and
should receive them separately instead of receiving a complete URL.

## 7.2 Python builder

```python
from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Literal
from urllib.parse import quote

ProxyTier = Literal["direct", "datacenter", "residential"]


@dataclass(frozen=True)
class ProxyOptions:
    tier: ProxyTier
    country_code: str | None = None
    us_state_code: str | None = None
    session_id: str | None = None


def sanitize_session_id(value: str) -> str:
    sanitized = re.sub(r"[^a-zA-Z0-9._~]", "_", value)
    sanitized = re.sub(r"_+", "_", sanitized).strip("_")
    return sanitized[:50]


def build_apify_proxy_url(options: ProxyOptions) -> str | None:
    if options.tier == "direct":
        return None

    password = os.environ.get("APIFY_PROXY_PASSWORD")
    if not password:
        raise RuntimeError("APIFY_PROXY_PASSWORD is required")

    host = os.environ.get("APIFY_PROXY_HOST", "proxy.apify.com")
    port = os.environ.get("APIFY_PROXY_PORT", "8000")

    username_parts: list[str] = [
        "groups-RESIDENTIAL" if options.tier == "residential" else "auto"
    ]

    if options.us_state_code:
        state = options.us_state_code.upper()
        if not re.fullmatch(r"[A-Z]{2}", state):
            raise ValueError("us_state_code must be a two-letter state code")
        username_parts.append(f"country-US_{state}")
    elif options.country_code:
        country = options.country_code.upper()
        if not re.fullmatch(r"[A-Z]{2}", country):
            raise ValueError("country_code must be a two-letter country code")
        username_parts.append(f"country-{country}")

    if options.session_id:
        session_id = sanitize_session_id(options.session_id)
        if not session_id:
            raise ValueError("session_id became empty after sanitization")
        username_parts.append(f"session-{session_id}")

    username = ",".join(username_parts)
    return (
        f"http://{quote(username, safe=',-_~.')}:"
        f"{quote(password, safe='')}@{host}:{port}"
    )
```

---

# 8. Routing Strategy

## 8.1 Default escalation ladder

Use:

```text
Tier 0: Direct lightweight HTTP
Tier 1: Direct browser only if JavaScript is required
Tier 2: Datacenter proxy
Tier 3: Residential proxy
Tier 4: Residential browser session with geographic targeting
```

Do not start at Tier 4 unless the target policy explicitly requires it.

## 8.2 Escalation signals

Escalate when there is evidence of:

- target-specific IP blocking;
- persistent 403 or 429 responses;
- geofenced content;
- CAPTCHA or challenge pages;
- empty/altered responses only from the server environment;
- target behavior that differs from an authorized local test;
- repeated connection resets correlated with the current egress IP.

Do not escalate solely because of:

- parser bugs;
- changed HTML selectors;
- expired authentication;
- invalid URLs;
- 404 pages;
- malformed requests;
- missing required cookies;
- application exceptions;
- database failures;
- schema mismatches.

## 8.3 Target policy registry

Maintain a target policy per platform or domain:

```yaml
targets:
  example.com:
    initial_tier: direct
    max_tier: residential
    requires_browser: false
    country_code: US
    us_state_code: NY
    session_mode: sticky_per_domain
    max_concurrency: 2
    min_delay_ms: 1200
    block_resources:
      - image
      - media
      - font
    known_block_signals:
      - status_403
      - status_429
      - challenge_page
```

This registry is the source of truth. Do not scatter target-specific proxy
decisions throughout scraper code.

---

# 9. Session Strategy

## 9.1 Rotate per request

Use when:

- requests are stateless;
- cookies are not needed;
- the target responds independently;
- IP diversity is more important than continuity.

Do not include a session ID.

## 9.2 Rotate per job

Use one session ID for a single extraction job.

Example:

```text
session-menu_52_20260724
```

Retire it after:

- job completion;
- 25 minutes;
- repeated block response;
- unacceptable latency;
- connection interruption.

## 9.3 Sticky per domain

Use one session per target domain when cookies or behavioral continuity matter.

Do not share a sticky session across unrelated target domains.

## 9.4 Sticky per account

Only use when operating an account the project is authorized to access.

Bind together:

- proxy session;
- cookie jar;
- browser fingerprint;
- local storage;
- authentication state.

If the proxy session is retired, retire or re-establish the related browser
identity coherently. Do not keep account cookies while abruptly changing the
rest of the identity unless the target tolerates it.

## 9.5 Session health

Track:

```yaml
session_id_hash:
created_at:
last_used_at:
request_count:
success_count:
failure_count:
block_count:
average_latency_ms:
last_status:
retired_reason:
```

Retire when:

```text
age > SESSION_TTL_MINUTES
OR requests >= SESSION_MAX_REQUESTS
OR failures >= SESSION_MAX_FAILURES
OR latency > SESSION_MAX_LATENCY_MS for repeated requests
OR explicit block signal occurs
```

---

# 10. Playwright Integration

## 10.1 Browser launch proxy

```typescript
import { chromium, type Browser } from "playwright";

interface BrowserProxyConfig {
  countryCode?: string;
  usStateCode?: string;
  sessionId: string;
}

export async function launchResidentialBrowser(
  config: BrowserProxyConfig,
): Promise<Browser> {
  const password = process.env.APIFY_PROXY_PASSWORD;
  if (!password) throw new Error("APIFY_PROXY_PASSWORD is required");

  const parts = ["groups-RESIDENTIAL"];

  if (config.usStateCode) {
    parts.push(`country-US_${config.usStateCode.toUpperCase()}`);
  } else if (config.countryCode) {
    parts.push(`country-${config.countryCode.toUpperCase()}`);
  }

  parts.push(`session-${sanitizeSessionId(config.sessionId)}`);

  return chromium.launch({
    headless: true,
    proxy: {
      server: "http://proxy.apify.com:8000",
      username: parts.join(","),
      password,
    },
  });
}
```

A browser normally uses one proxy identity for that browser instance. Launch a
new browser or browser process when intentionally rotating the proxy identity.

## 10.2 Resource blocking

```typescript
import type { Page, Route } from "playwright";

const BLOCKED_RESOURCE_TYPES = new Set([
  "image",
  "media",
  "font",
]);

const BLOCKED_HOST_PATTERNS = [
  /google-analytics\.com$/i,
  /googletagmanager\.com$/i,
  /doubleclick\.net$/i,
  /facebook\.net$/i,
];

export async function installTrafficControls(page: Page): Promise<void> {
  await page.route("**/*", async (route: Route) => {
    const request = route.request();
    const resourceType = request.resourceType();

    if (BLOCKED_RESOURCE_TYPES.has(resourceType)) {
      await route.abort();
      return;
    }

    try {
      const hostname = new URL(request.url()).hostname;
      if (BLOCKED_HOST_PATTERNS.some((pattern) => pattern.test(hostname))) {
        await route.abort();
        return;
      }
    } catch {
      // Continue non-standard URLs rather than breaking navigation.
    }

    await route.continue();
  });
}
```

Do not block stylesheets or scripts blindly. Some storefronts require them to
render or expose API data.

## 10.3 Context isolation

For each independent session:

```typescript
const context = await browser.newContext({
  serviceWorkers: "block",
});

const page = await context.newPage();
```

Do not reuse browser contexts across identities unless intentionally sharing
cookies and storage.

---

# 11. HTTP Client Integration

## 11.1 Node.js with `undici`

Use a proxy-aware dispatcher.

```typescript
import { ProxyAgent, request } from "undici";

export async function fetchThroughApify(
  url: string,
  sessionId: string,
): Promise<string> {
  const proxyUrl = buildApifyProxyUrl({
    tier: "residential",
    countryCode: "US",
    usStateCode: "NY",
    sessionId,
  });

  if (!proxyUrl) throw new Error("Proxy URL was not generated");

  const dispatcher = new ProxyAgent(proxyUrl);

  try {
    const response = await request(url, {
      dispatcher,
      headersTimeout: 30_000,
      bodyTimeout: 60_000,
      maxRedirections: 5,
      headers: {
        "user-agent": "Mozilla/5.0 compatible scraper",
        accept: "text/html,application/xhtml+xml",
      },
    });

    if (response.statusCode >= 400) {
      throw new Error(`Target returned HTTP ${response.statusCode}`);
    }

    return await response.body.text();
  } finally {
    await dispatcher.close();
  }
}
```

Reuse agents for repeated requests when appropriate instead of creating a new
connection pool for each request.

## 11.2 Python with `httpx`

```python
import httpx


def fetch_through_apify(url: str, session_id: str) -> str:
    proxy_url = build_apify_proxy_url(
        ProxyOptions(
            tier="residential",
            country_code="US",
            us_state_code="NY",
            session_id=session_id,
        )
    )

    if not proxy_url:
        raise RuntimeError("Proxy URL was not generated")

    timeout = httpx.Timeout(connect=20.0, read=60.0, write=30.0, pool=20.0)

    with httpx.Client(
        proxy=proxy_url,
        timeout=timeout,
        follow_redirects=True,
        headers={
            "User-Agent": "Mozilla/5.0 compatible scraper",
            "Accept": "text/html,application/xhtml+xml",
        },
    ) as client:
        response = client.get(url)
        response.raise_for_status()
        return response.text
```

Check the installed `httpx` version because proxy argument names can change
between library versions.

---

# 12. Crawlee Integration Without Actors

Crawlee can be used as a normal Node.js dependency without deploying an Actor.

```typescript
import { PlaywrightCrawler, ProxyConfiguration } from "crawlee";

const password = process.env.APIFY_PROXY_PASSWORD;
if (!password) throw new Error("APIFY_PROXY_PASSWORD is required");

const proxyConfiguration = new ProxyConfiguration({
  proxyUrls: [
    `http://groups-RESIDENTIAL,country-US_NY:${encodeURIComponent(password)}@proxy.apify.com:8000`,
  ],
});

const crawler = new PlaywrightCrawler({
  proxyConfiguration,
  useSessionPool: true,
  persistCookiesPerSession: true,
  maxConcurrency: 2,
  maxRequestRetries: 3,

  async requestHandler({ page, request, session, log }) {
    await installTrafficControls(page);

    log.info("Processing target", {
      url: request.loadedUrl ?? request.url,
      sessionId: session?.id,
    });

    // Extraction logic.
  },

  async failedRequestHandler({ request, log }) {
    log.error("Request failed", {
      url: request.url,
      errorMessages: request.errorMessages,
    });
  },
});

await crawler.run(["https://example.com"]);
```

For advanced routing, generate proxy URLs per target and session instead of
using one static URL.

---

# 13. Retry and Rotation Engine

## 13.1 Failure classification

Every failure must be classified as:

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

## 13.2 Apify proxy status handling

Apify may return proxy-specific statuses:

| Status | Meaning | Default Action |
|---:|---|---|
| 590 | Upstream non-success | Inspect target response; limited retry |
| 593 | DNS lookup/configuration problem | Validate target URL and proxy config |
| 594 | Connection refused | Rotate/retry |
| 595 | Connection reset or timeout | Rotate/retry |
| 596 | Broken pipe | Rotate/retry |
| 597 | Upstream authentication failed | Validate credentials; do not loop |
| 599 | Generic upstream error | Limited rotate/retry |

Do not treat all 590-series responses as a target block.

## 13.3 Backoff

Use exponential backoff with jitter:

```text
delay =
  min(RETRY_MAX_DELAY_MS,
      RETRY_BASE_DELAY_MS × 2^(attempt - 1))
  × random(1 - jitter, 1 + jitter)
```

## 13.4 Retry decision

```text
if credentials invalid:
    fail immediately
elif parser failed after valid response:
    do not rotate proxy
elif target returned permanent missing response:
    do not retry
elif block signal confirmed:
    retire session and escalate or rotate
elif connection failure is transient:
    retry with new session
elif budget exhausted:
    stop job
else:
    retry within attempt cap
```

## 13.5 Circuit breaker

Maintain a circuit breaker per domain.

```yaml
WINDOW_REQUESTS: 20
OPEN_WHEN_FAILURE_RATE: 0.6
OPEN_DURATION_SECONDS: 300
HALF_OPEN_PROBE_REQUESTS: 2
```

When open:

- stop burning residential traffic;
- pause the target;
- allow other targets to continue;
- emit a structured blocker event.

---

# 14. Block Detection

A block detector may inspect:

- response status;
- final URL;
- page title;
- HTML text;
- presence of CAPTCHA widgets;
- unexpectedly tiny response body;
- repeated redirect loops;
- known challenge headers;
- response differences between direct and proxy probes.

Example signals:

```yaml
status_codes: [401, 403, 429]
title_patterns:
  - "access denied"
  - "just a moment"
body_patterns:
  - "verify you are human"
  - "unusual traffic"
  - "request blocked"
```

Do not use generic words such as `error` alone.

Log the signal that caused a request to be classified as blocked.

---

# 15. Traffic and Cost Control

Residential proxy usage is charged by traffic. Therefore:

1. Prefer HTTP APIs or embedded JSON over rendered browser pages.
2. Reverse-engineer legitimate public data requests when practical.
3. Block images, video, fonts, advertisements, analytics, and trackers.
4. Avoid downloading the same assets repeatedly.
5. Reuse validated data when freshness permits.
6. Use conditional requests when supported.
7. Stop parsing as soon as required data is obtained.
8. Limit response sizes.
9. Cap pages and requests per job.
10. Measure bytes by domain, job, target, and tier.
11. Avoid screenshots through residential traffic unless required.
12. Do not run browser video recording or tracing by default.

## 15.1 Cost ledger

Track:

```yaml
job_id:
target:
proxy_tier:
requests:
successful_requests:
failed_requests:
bytes_received:
bytes_sent:
browser_pages:
sessions_created:
sessions_retired:
escalations:
```

## 15.2 Budget gate

Before each residential request:

```text
projected_total =
  current_job_bytes
  + estimated_request_bytes

if projected_total > RESIDENTIAL_MAX_BYTES_PER_JOB:
    stop or downgrade according to policy
```

Do not silently exceed the configured project budget.

---

# 16. Validation Procedure

## 16.1 Credential validation

1. Confirm `APIFY_PROXY_PASSWORD` exists.
2. Do not display it.
3. Confirm proxy host and port.
4. Confirm the account has access to the selected proxy group.
5. Confirm the deployment environment supports outbound HTTP proxy traffic.

## 16.2 Egress validation

Route a test request through the proxy to:

```text
https://api.apify.com/v2/browser-info/
```

Record:

```yaml
proxy_connected:
observed_ip_changed:
observed_country:
observed_region:
latency_ms:
session_reused:
```

## 16.3 Sticky session validation

1. Generate one session ID.
2. Send two requests using that ID.
3. Verify the same observed IP when the network remains available.
4. Generate a second session ID.
5. Verify that rotation is possible.
6. Do not fail the test solely because two random sessions happen to receive
   the same IP.

## 16.4 Geographic validation

Verify the observed location rather than assuming the username parameter was
honored.

If no proxy exists in the requested location, the connection may fail. Decide
whether to:

- fail closed;
- fall back to country-level targeting;
- fall back to no geographic targeting.

This must be explicit in `GEO_FALLBACK_ALLOWED`.

## 16.5 Target validation

Test:

```text
direct request
→ datacenter request
→ residential request
```

Record which tier first succeeds and make that the target's initial policy.

---

# 17. Logging Contract

Use structured logs:

```json
{
  "event": "proxy_request_complete",
  "jobId": "job_123",
  "target": "example.com",
  "tier": "residential",
  "sessionHash": "c4d3...",
  "attempt": 2,
  "status": 200,
  "latencyMs": 1840,
  "responseBytes": 92134,
  "blockSignal": null
}
```

Never log:

```json
{
  "proxyPassword": "...",
  "proxyUrl": "http://username:password@...",
  "authorization": "...",
  "cookies": "...",
  "accountCredentials": "..."
}
```

Redact proxy URLs before logging:

```text
http://groups-RESIDENTIAL:***@proxy.apify.com:8000
```

---

# 18. Metrics

Recommended metrics:

```text
proxy_requests_total{target,tier,status}
proxy_request_duration_ms{target,tier}
proxy_bytes_total{target,tier,direction}
proxy_sessions_created_total{target,tier}
proxy_sessions_retired_total{target,reason}
proxy_escalations_total{target,from_tier,to_tier}
proxy_blocks_total{target,signal}
proxy_budget_remaining_bytes{job}
proxy_circuit_state{target}
```

Alerts:

- residential traffic spikes;
- credential failures;
- repeated 597 responses;
- high block rate;
- high average latency;
- excessive session churn;
- budget threshold reached;
- target circuit breaker opened.

---

# 19. Security Rules

1. Store the proxy password only server-side.
2. Use the minimum deployment access necessary.
3. Rotate the password after suspected exposure.
4. Scrub it from logs and error reporting.
5. Do not include it in Docker images.
6. Do not put it in Git remotes or repository URLs.
7. Do not use it as a CLI argument visible in process listings.
8. Keep `.env`, Playwright traces, screenshots, and HAR files out of commits.
9. Treat captured cookies and authenticated browser state as secrets.
10. Restrict who can trigger high-cost residential jobs.
11. Add request and budget limits to externally callable scraping endpoints.
12. Validate target URLs to prevent open-proxy abuse or SSRF.

## 19.1 Target URL allowlist

External user input must not directly control arbitrary proxy destinations.

Use:

```yaml
ALLOWED_TARGET_HOSTS:
  - dispensary-a.example
  - dispensary-b.example
```

Reject:

- localhost;
- private network ranges;
- cloud metadata endpoints;
- file URLs;
- non-HTTP protocols;
- unapproved redirect destinations.

---

# 20. Failure Recovery

## 20.1 Authentication failure

Symptoms:

- proxy authentication error;
- repeated 407;
- proxy-specific credential failure.

Actions:

1. stop retries;
2. verify the secret name;
3. verify the proxy password, not the account password/token;
4. verify plan and proxy-group access;
5. rotate the secret if exposure is suspected.

## 20.2 Target still blocked

Actions:

1. confirm it is actually a block;
2. lower concurrency;
3. add delay;
4. retire the session;
5. verify cookies and headers are coherent;
6. verify geographic targeting;
7. use a browser only if JavaScript/challenge behavior requires it;
8. pause the target after retry cap;
9. do not create an unbounded identity-rotation loop.

## 20.3 Slow residential session

Actions:

1. run a small probe;
2. compare latency threshold;
3. retire the slow session;
4. create a new session;
5. lower request size;
6. use datacenter for large downloads when permitted.

## 20.4 Connection interruption

Actions:

1. preserve the target URL and attempt metadata;
2. retire the session;
3. retry with bounded backoff;
4. make extraction idempotent;
5. resume from the last persisted request rather than restarting the entire job.

## 20.5 Traffic spike

Actions:

1. stop or pause the job;
2. inspect resource types;
3. verify route blocking was installed before navigation;
4. inspect redirects and repeated asset loads;
5. reduce browser concurrency;
6. switch to HTTP extraction where possible;
7. lower the job budget before restarting.

---

# 21. Project Artifacts

Create or update:

```text
docs/
  PROXY_ARCHITECTURE.md
  PROXY_TARGET_POLICIES.yaml
  PROXY_RUNBOOK.md
  PROXY_TEST_STATUS.md
  PROXY_COST_LOG.md
.env.example
```

## 21.1 `PROXY_ARCHITECTURE.md`

Include:

- why proxying is required;
- which targets require which tier;
- runtime location;
- credential flow;
- session strategy;
- geographic requirements;
- retry and circuit-breaker policy;
- security boundaries;
- observability;
- budget controls.

## 21.2 `PROXY_TARGET_POLICIES.yaml`

Example:

```yaml
version: 1

defaults:
  initial_tier: direct
  max_tier: residential
  requires_browser: false
  max_attempts: 4
  max_concurrency: 2

targets:
  target.example:
    initial_tier: direct
    max_tier: residential
    country_code: US
    us_state_code: NY
    session_mode: sticky_per_domain
    requires_browser: true
    blocked_resource_types:
      - image
      - media
      - font
```

## 21.3 `PROXY_RUNBOOK.md`

Include:

- secret setup;
- connectivity test;
- location test;
- target test;
- common errors;
- credential rotation;
- emergency disable switch;
- budget shutdown;
- continuation commands.

---

# 22. Implementation Workflow

# Phase 0 — Inspect

1. Identify scraper runtime and language.
2. Identify current HTTP/browser libraries.
3. Identify target domains.
4. Identify whether each target is public and authorized.
5. Identify current block symptoms.
6. Identify required geographic location.
7. Identify current deployment secret system.
8. Identify current request volume.
9. Identify current traffic size.
10. Capture the direct-access baseline.

Exit gate:

- target list exists;
- authorization and intended access are clear;
- direct baseline is recorded;
- the proxy password storage mechanism is known.

# Phase 1 — Configure

1. Add `.env.example`.
2. Add secret to the deployment environment.
3. implement username builder;
4. implement proxy URL/provider abstraction;
5. implement target policy registry;
6. implement redaction.

Exit gate:

- proxy configuration can be enabled and disabled;
- credentials never enter logs;
- target policies are centralized.

# Phase 2 — Validate Connectivity

1. Test Apify browser-info through the proxy.
2. Verify the observed IP.
3. Verify location if configured.
4. Verify session reuse.
5. Verify session rotation.
6. Record latency.

Exit gate:

- connectivity is proven;
- location behavior is known;
- sticky session behavior is proven.

# Phase 3 — Integrate Target Routing

1. Add direct request path.
2. Add proxy path.
3. Add escalation logic.
4. Add target block detection.
5. Add bounded retry.
6. Add session retirement.
7. Add circuit breaker.

Exit gate:

- target succeeds at the lowest working tier;
- failures do not loop indefinitely;
- each escalation is logged.

# Phase 4 — Control Traffic

1. Block unnecessary browser resources.
2. add request/page/byte caps;
3. record response bytes;
4. reduce concurrency;
5. cache or deduplicate repeated requests;
6. test cost behavior.

Exit gate:

- residential traffic is measured;
- budget limits are enforced;
- unnecessary browser resources are blocked.

# Phase 5 — Production Gate

Required:

```yaml
PROXY_CONNECTIVITY_VERIFIED: true
TARGET_POLICY_DEFINED: true
SECRET_REDACTION_VERIFIED: true
RETRY_CAP_VERIFIED: true
SESSION_RETIREMENT_VERIFIED: true
CIRCUIT_BREAKER_VERIFIED: true
TRAFFIC_BLOCKING_VERIFIED: true
BUDGET_LIMIT_VERIFIED: true
DIRECT_FALLBACK_VERIFIED: true
EMERGENCY_DISABLE_VERIFIED: true
```

---

# 23. Test Matrix

```yaml
tests:
  - id: PROXY-001
    case: missing password
    expected: fail before request without exposing secret

  - id: PROXY-002
    case: residential proxy connectivity
    expected: browser-info returns successful proxy egress

  - id: PROXY-003
    case: New York state targeting
    expected: observed region matches when inventory is available

  - id: PROXY-004
    case: sticky session reuse
    expected: repeated requests reuse the same IP when session remains alive

  - id: PROXY-005
    case: session retirement
    expected: blocked session is replaced and not reused

  - id: PROXY-006
    case: direct target succeeds
    expected: no residential traffic is used

  - id: PROXY-007
    case: direct target blocked
    expected: escalation occurs within configured tier policy

  - id: PROXY-008
    case: permanent 404
    expected: no proxy rotation loop

  - id: PROXY-009
    case: proxy 597
    expected: fail fast and report credential/configuration problem

  - id: PROXY-010
    case: resource blocking
    expected: images, media, fonts, and configured trackers are aborted

  - id: PROXY-011
    case: byte budget exceeded
    expected: job stops or downgrades according to policy

  - id: PROXY-012
    case: URL not allowlisted
    expected: request rejected before proxy connection

  - id: PROXY-013
    case: emergency disable
    expected: APIFY_PROXY_ENABLED=false prevents proxy use

  - id: PROXY-014
    case: secret redaction
    expected: logs contain no proxy password or complete proxy URL
```

---

# 24. Standard Skill Output

When activated, return:

```yaml
PROXY_IMPLEMENTATION:
  runtime:
  language:
  http_library:
  browser_library:
  deployment_environment:

TARGETS:
  - domain:
    direct_baseline:
    initial_tier:
    max_tier:
    browser_required:
    geographic_target:
    session_mode:
    concurrency:
    block_signals:

CONFIGURATION:
  secret_source:
  proxy_host:
  proxy_port:
  routing_mode:
  retry_policy:
  budget_policy:

VALIDATION:
  connectivity:
  egress_ip:
  geography:
  sticky_session:
  rotation:
  target_success:
  resource_blocking:
  secret_redaction:

RISKS:
  - risk:
    mitigation:

NEXT_ACTION:
```

---

# 25. Agent Instructions

When this skill is activated:

1. Inspect the scraper before changing it.
2. Determine whether the target needs a proxy at all.
3. Keep Apify Actor dependencies out unless the runtime is intentionally an Actor.
4. Implement proxy routing behind one abstraction.
5. Add target-specific policies outside extraction code.
6. Default to direct access.
7. Escalate to residential only with evidence or explicit geographic need.
8. Use sticky sessions only where continuity is needed.
9. Block unnecessary browser traffic before the first navigation.
10. Add byte, request, page, retry, and concurrency limits.
11. Validate proxy egress with Apify browser-info.
12. Validate the actual target.
13. Record observed behavior rather than assuming configuration worked.
14. Never expose the proxy password.
15. Update the runbook, policy registry, tests, and cost controls in the same task.
16. End with the exact next action and current verified state.

---

# 26. Official References

- Apify Proxy overview: https://docs.apify.com/proxy
- Residential proxy: https://docs.apify.com/proxy/residential-proxy
- Apify Python proxy management: https://docs.apify.com/sdk/python/docs/concepts/proxy-management
