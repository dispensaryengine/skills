# Proxy Target Policy Contract

## Purpose

Target-specific routing belongs in one registry, not in scattered conditional code.

## Schema

```yaml
version: 1

defaults:
  enabled: true
  initial_tier: direct
  max_tier: residential
  requires_browser: false
  session_mode: rotate_per_job
  max_attempts: 4
  max_concurrency: 2
  min_delay_ms: 500
  max_delay_ms: 2500
  geographic_fallback: fail_closed
  resource_blocking:
    images: true
    media: true
    fonts: true
    analytics: true
  budgets:
    max_bytes_per_job: 50000000
    max_requests_per_job: 500
    max_browser_pages_per_job: 100

targets:
  example.com:
    initial_tier: direct
    max_tier: residential
    requires_browser: false
    country_code: US
    subdivision_code: NY
    session_mode: sticky_per_domain
    max_concurrency: 2
    block_signals:
      status_codes: [403, 429]
      title_patterns: ["access denied"]
      body_patterns: ["verify you are human"]
```

## Allowed Values

```yaml
TIER:
  - direct
  - datacenter
  - residential

SESSION_MODE:
  - rotate_per_request
  - rotate_per_job
  - sticky_per_domain
  - sticky_per_account

GEOGRAPHIC_FALLBACK:
  - fail_closed
  - country_only
  - any_location
  - direct
```

## Policy Rules

- `initial_tier` must not exceed `max_tier`.
- authenticated targets should use a sticky mode;
- `sticky_per_account` requires the security contract;
- residential browser concurrency should remain low;
- missing location inventory must follow the explicit fallback;
- permanent 404 or 410 is not a block signal by default;
- a target may prohibit escalation beyond direct;
- a target may require residential from the first request when geography is itself the requirement.

## Policy Evidence

For every target, record:

```yaml
POLICY_SOURCE: "observed | user_required | source_documented | temporary"
LAST_VERIFIED:
DIRECT_RESULT:
DATACENTER_RESULT:
RESIDENTIAL_RESULT:
SELECTED_TIER:
REASON:
```
