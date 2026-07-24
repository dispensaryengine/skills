# Apify Proxy Testing Contract

## Connectivity Tests

| ID | Case | Expected |
|---|---|---|
| PROXY-001 | Missing password | Fail before request; secret absent from output |
| PROXY-002 | External connectivity | Proxy status or browser-info succeeds |
| PROXY-003 | Observed egress | Returned client IP differs from direct baseline when expected |
| PROXY-004 | Geography | Observed location matches requested target when available |
| PROXY-005 | Sticky session | Same session generally reuses the assigned IP while alive |
| PROXY-006 | Rotation | A retired/new session can receive a new route |

## Routing Tests

| ID | Case | Expected |
|---|---|---|
| ROUTE-001 | Direct succeeds | No residential request |
| ROUTE-002 | Direct blocked | Escalation follows target policy |
| ROUTE-003 | Parser failure | No proxy escalation |
| ROUTE-004 | Permanent 404 | No rotation loop |
| ROUTE-005 | Max tier reached | Target pauses or fails explicitly |
| ROUTE-006 | Circuit opens | Residential spend stops for that target |

## Traffic Tests

| ID | Case | Expected |
|---|---|---|
| TRAFFIC-001 | Image request | Aborted when not required |
| TRAFFIC-002 | Media request | Aborted when not required |
| TRAFFIC-003 | Byte budget | Job stops or follows explicit downgrade |
| TRAFFIC-004 | Page budget | Further browser pages rejected |
| TRAFFIC-005 | Concurrency | Residential limit enforced |

## Security Tests

| ID | Case | Expected |
|---|---|---|
| SEC-001 | Full proxy URL log | Password redacted |
| SEC-002 | Unapproved host | Rejected before proxy |
| SEC-003 | Private IP | Rejected |
| SEC-004 | Redirect to private IP | Rejected |
| SEC-005 | Emergency disable | Proxy path not used |
| SEC-006 | Client bundle scan | No proxy password |

## Failure Tests

| ID | Case | Expected |
|---|---|---|
| FAIL-001 | 597 | Fail fast; credential problem reported |
| FAIL-002 | 594/595/596 | Bounded rotation/retry |
| FAIL-003 | Slow session | Retire after threshold |
| FAIL-004 | Connection interruption | Resume from persisted checkpoint |
| FAIL-005 | Budget exhaustion | Explicit budget failure |

## Release Evidence

```yaml
CONNECTIVITY:
EGRESS:
GEOGRAPHY:
SESSION_REUSE:
ROTATION:
LOWEST_WORKING_TIER:
RESOURCE_BLOCKING:
BUDGETS:
SECURITY:
EMERGENCY_DISABLE:
KNOWN_FAILURES:
RELEASE_DECISION: "GO | GO_WITH_RISKS | NO_GO"
```
