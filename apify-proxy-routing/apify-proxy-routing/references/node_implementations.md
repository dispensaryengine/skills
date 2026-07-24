# Apify Proxy Node.js Implementations

Last reviewed: 2026-07-24

Version-sensitive APIs must be checked against installed package versions.

## Shared Builder

```typescript
export type ProxyTier = "direct" | "datacenter" | "residential";

export interface ProxyOptions {
  tier: ProxyTier;
  countryCode?: string;
  usStateCode?: string;
  sessionId?: string;
}

export function sanitizeSessionId(value: string): string {
  return value
    .replace(/[^a-zA-Z0-9._~]/g, "_")
    .replace(/_+/g, "_")
    .replace(/^_+|_+$/g, "")
    .slice(0, 50);
}

export function buildProxyCredentials(options: ProxyOptions): {
  server: string;
  username: string;
  password: string;
} | undefined {
  if (options.tier === "direct") return undefined;

  const password = process.env.APIFY_PROXY_PASSWORD;
  if (!password) throw new Error("APIFY_PROXY_PASSWORD is required");

  const host = process.env.APIFY_PROXY_HOST ?? "proxy.apify.com";
  const port = process.env.APIFY_PROXY_PORT ?? "8000";
  const parts: string[] = [
    options.tier === "residential" ? "groups-RESIDENTIAL" : "auto",
  ];

  if (options.usStateCode) {
    const state = options.usStateCode.toUpperCase();
    if (!/^[A-Z]{2}$/.test(state)) {
      throw new Error("usStateCode must be a two-letter US state code");
    }
    parts.push(`country-US_${state}`);
  } else if (options.countryCode) {
    const country = options.countryCode.toUpperCase();
    if (!/^[A-Z]{2}$/.test(country)) {
      throw new Error("countryCode must be a two-letter code");
    }
    parts.push(`country-${country}`);
  }

  if (options.sessionId) {
    const session = sanitizeSessionId(options.sessionId);
    if (!session) throw new Error("Invalid empty proxy session");
    parts.push(`session-${session}`);
  }

  return {
    server: `http://${host}:${port}`,
    username: parts.join(","),
    password,
  };
}
```

Prefer separate proxy fields when the library supports them.

## Playwright

```typescript
import { chromium } from "playwright";

const proxy = buildProxyCredentials({
  tier: "residential",
  countryCode: "US",
  usStateCode: "NY",
  sessionId: "dispensary_52",
});

const browser = await chromium.launch({
  headless: true,
  proxy,
});

const context = await browser.newContext({
  serviceWorkers: "block",
});

const page = await context.newPage();
```

A browser process normally holds one proxy configuration. Rotate intentionally by creating a new browser process or architecture-approved isolation boundary.

## Resource Blocking

```typescript
import type { Page } from "playwright";

const blockedTypes = new Set(["image", "media", "font"]);
const blockedHosts = [
  /google-analytics\.com$/i,
  /googletagmanager\.com$/i,
  /doubleclick\.net$/i,
];

export async function installTrafficControls(page: Page): Promise<void> {
  await page.route("**/*", async (route) => {
    const request = route.request();

    if (blockedTypes.has(request.resourceType())) {
      await route.abort();
      return;
    }

    try {
      const hostname = new URL(request.url()).hostname;
      if (blockedHosts.some((pattern) => pattern.test(hostname))) {
        await route.abort();
        return;
      }
    } catch {
      // Continue non-standard URLs unless project policy says otherwise.
    }

    await route.continue();
  });
}
```

Install before navigation.

Do not blindly block scripts or stylesheets.

## Undici

Check the installed Undici version.

```typescript
import { ProxyAgent, request } from "undici";

const credentials = buildProxyCredentials({
  tier: "residential",
  usStateCode: "NY",
  sessionId: "menu_52",
});

if (!credentials) throw new Error("Proxy is required");

const proxyUrl =
  `${credentials.server.replace("://", `://${encodeURIComponent(credentials.username)}:`)}`;

// Prefer a tested URL builder rather than string manipulation in production.
// Never log the resulting URL.
```

Because proxy-agent constructor behavior is version-sensitive, implement one tested adapter and cover it with integration tests.

## Crawlee Outside Actors

Crawlee can run as a normal Node.js package.

Use `ProxyConfiguration` or a custom `newUrlFunction` according to the installed Crawlee version.

Requirements:

- target policy controls tier;
- SessionPool identity matches proxy session;
- cookies persist only in the intended session;
- failed request handler records evidence;
- proxy password remains outside source;
- residential concurrency remains capped.

## Node Version-Sensitive Areas

Verify:

- Playwright proxy object behavior;
- Undici `ProxyAgent` constructor;
- Crawlee `ProxyConfiguration`;
- Crawlee `SessionPool`;
- service worker blocking;
- response byte measurement.

Official sources:

- https://docs.apify.com/proxy
- https://docs.apify.com/proxy/residential-proxy
- https://crawlee.dev/
- installed library documentation
