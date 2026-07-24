# Apify Proxy Operations Runbook

## Setup

1. Confirm eligible Apify plan.
2. Confirm available proxy groups in Apify Console.
3. Store `APIFY_PROXY_PASSWORD` in the deployment secret system.
4. create `.env.example`;
5. configure target policies;
6. run connectivity tests;
7. run target tests.

## Emergency Disable

Set:

```env
APIFY_PROXY_ENABLED=false
```

Expected:

- no proxy request is constructed;
- target policy reports proxy disabled;
- jobs either use allowed direct routing or stop explicitly.

## Common Failures

### 407 or authentication failure

- stop retries;
- verify secret source;
- verify proxy password;
- verify plan/group access;
- rotate secret if exposed.

### 403 or 429 from target

- confirm block signal;
- inspect direct baseline;
- inspect cookie/session coherence;
- lower concurrency;
- retire session;
- escalate only within target policy.

### 593

- validate target hostname;
- validate DNS;
- validate proxy-chain configuration;
- reject malformed or private target.

### 594–596

- preserve evidence;
- retire session;
- bounded retry;
- open circuit after threshold.

### Traffic spike

- pause job;
- inspect blocked resource configuration;
- inspect redirects;
- lower concurrency;
- switch to HTTP extraction where possible;
- lower per-job budget.

### Slow session

- run a small probe;
- retire session above latency threshold;
- avoid large transfer over residential when another tier works.

## Work Log Entry

```yaml
DATE:
JOB:
TARGET:
STARTING_TIER:
FINAL_TIER:
SESSIONS_CREATED:
BYTES:
REQUESTS:
BLOCK_SIGNALS:
FAILURES:
TESTS:
DECISIONS:
NEXT_ACTION:
```

## Handoff

```yaml
CURRENT_STATE:
CONFIG_PATH:
SECRET_SOURCE:
TARGETS:
VERIFIED_TIER:
GEOGRAPHY:
SESSION_MODE:
CIRCUIT_STATE:
BUDGET_REMAINING:
KNOWN_FAILURES:
NEXT_EXACT_ACTION:
```
