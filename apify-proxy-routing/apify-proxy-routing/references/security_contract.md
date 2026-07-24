# Apify Proxy Security Contract

## Secrets

The Apify Proxy password must:

- remain server-side;
- come from a secret manager or protected environment;
- never appear in source control;
- never appear in client code;
- never appear in a complete logged proxy URL;
- never be passed as a visible command-line argument.

Redact:

```text
http://groups-RESIDENTIAL:***@proxy.apify.com:8000
```

## Target Allowlist

A public or user-triggered scraper endpoint must not become an open proxy.

Allow only approved hosts.

Reject:

- localhost;
- loopback;
- private IPv4 and IPv6;
- cloud metadata addresses;
- file URLs;
- non-HTTP protocols;
- embedded credentials;
- unapproved redirect hosts;
- DNS rebinding results.

Validate both the original URL and redirect destinations.

## SSRF Boundary

Resolve hostnames and reject private destinations after DNS resolution.

Re-check on redirects.

Do not trust a string-level hostname test alone.

## Authenticated Sessions

Treat as secrets:

- cookies;
- storage state;
- authorization headers;
- session tokens;
- browser traces;
- HAR files;
- screenshots containing account data.

Bind proxy session and authenticated browser state coherently.

Use only accounts the operator is authorized to access.

## Trigger Protection

High-cost proxy jobs require:

- authentication;
- authorization;
- rate limiting;
- job budget;
- target allowlist;
- audit event;
- cancellation mechanism.

## Logging

Allowed:

- target hostname;
- tier;
- hashed session ID;
- response status;
- latency;
- bytes;
- attempt;
- block signal.

Disallowed:

- password;
- full proxy URL;
- cookies;
- authorization;
- target account credentials;
- raw user-provided secret.

## Incident Response

On suspected secret exposure:

1. stop affected jobs;
2. rotate Apify Proxy password;
3. remove secret from logs and artifacts where possible;
4. inspect usage;
5. invalidate related deployment secrets;
6. document scope and prevention.
