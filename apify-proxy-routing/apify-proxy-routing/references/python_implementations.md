# Apify Proxy Python Implementations

Last reviewed: 2026-07-24

Check the installed library version before choosing argument names.

## Shared Builder

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
    value = re.sub(r"[^a-zA-Z0-9._~]", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value[:50]


def build_apify_proxy_url(options: ProxyOptions) -> str | None:
    if options.tier == "direct":
        return None

    password = os.environ.get("APIFY_PROXY_PASSWORD")
    if not password:
        raise RuntimeError("APIFY_PROXY_PASSWORD is required")

    host = os.environ.get("APIFY_PROXY_HOST", "proxy.apify.com")
    port = os.environ.get("APIFY_PROXY_PORT", "8000")

    parts = [
        "groups-RESIDENTIAL"
        if options.tier == "residential"
        else "auto"
    ]

    if options.us_state_code:
        state = options.us_state_code.upper()
        if not re.fullmatch(r"[A-Z]{2}", state):
            raise ValueError("Invalid US state code")
        parts.append(f"country-US_{state}")
    elif options.country_code:
        country = options.country_code.upper()
        if not re.fullmatch(r"[A-Z]{2}", country):
            raise ValueError("Invalid country code")
        parts.append(f"country-{country}")

    if options.session_id:
        session = sanitize_session_id(options.session_id)
        if not session:
            raise ValueError("Invalid empty proxy session")
        parts.append(f"session-{session}")

    username = ",".join(parts)
    return (
        f"http://{quote(username, safe=',._~-')}:"
        f"{quote(password, safe='')}@{host}:{port}"
    )
```

Do not log the returned URL.

## requests

```python
import requests

proxy_url = build_apify_proxy_url(
    ProxyOptions(
        tier="residential",
        country_code="US",
        us_state_code="NY",
        session_id="menu_52",
    )
)

proxies = {
    "http": proxy_url,
    "https": proxy_url,
}

response = requests.get(
    "https://api.apify.com/v2/browser-info/",
    proxies=proxies,
    timeout=(20, 60),
)
response.raise_for_status()
```

## HTTPX

The accepted proxy parameter differs across HTTPX versions.

Check the installed version and use the supported constructor or transport configuration.

Cover this adapter with a live proxy connectivity test.

## Python Playwright

```python
from playwright.async_api import async_playwright

proxy_url = build_apify_proxy_url(
    ProxyOptions(
        tier="residential",
        us_state_code="NY",
        session_id="menu_52",
    )
)

async with async_playwright() as playwright:
    browser = await playwright.chromium.launch(
        headless=True,
        proxy={"server": proxy_url},
    )
```

Prefer separate username and password fields when the installed API supports them.

Install route blocking before navigation.

## Python Version-Sensitive Areas

Verify:

- requests proxy behavior;
- HTTPX proxy argument names;
- Playwright proxy fields;
- async timeout handling;
- streamed response byte accounting;
- redirect validation.

Official sources:

- https://docs.apify.com/proxy
- https://docs.apify.com/proxy/residential-proxy
- installed library documentation
