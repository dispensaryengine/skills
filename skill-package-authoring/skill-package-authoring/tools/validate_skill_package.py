#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

FRONTMATTER_RE = re.compile(r"\A---\s*\n(?P<body>.*?)\n---\s*\n", re.S)
REFERENCE_RE = re.compile(r"`((?:references|templates|tools)/[^`\n]+)`")
SECRET_PATTERNS = [
    re.compile(r"apify_proxy_[A-Za-z0-9]{20,}"),
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"(?i)(password|token|secret)\s*[:=]\s*['\"][^<'\"{][^'\"]{7,}['\"]"),
]

def fail(errors: list[str], message: str) -> None:
    errors.append(message)

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("package", type=Path)
    parser.add_argument("--max-controller-lines", type=int, default=350)
    args = parser.parse_args()

    root = args.package.resolve()
    skill = root / "SKILL.md"
    errors: list[str] = []
    warnings: list[str] = []

    if not skill.exists():
        print("FAIL: SKILL.md is missing")
        return 1

    text = skill.read_text(encoding="utf-8")
    lines = text.splitlines()

    match = FRONTMATTER_RE.match(text)
    if not match:
        fail(errors, "Frontmatter is missing or malformed.")
        frontmatter = ""
    else:
        frontmatter = match.group("body")
        if not re.search(r"(?m)^name:\s*\S+", frontmatter):
            fail(errors, "Frontmatter name is missing.")
        if not re.search(r"(?m)^description:\s*.+", frontmatter):
            fail(errors, "Frontmatter description is missing.")

    h1 = [line for line in lines if re.match(r"^# (?!#)", line)]
    if len(h1) != 1:
        fail(errors, f"SKILL.md must contain exactly one H1; found {len(h1)}.")

    if len(lines) > args.max_controller_lines:
        warnings.append(
            f"Controller has {len(lines)} lines; review against target max "
            f"{args.max_controller_lines}."
        )

    refs = sorted(set(REFERENCE_RE.findall(text)))
    if not refs:
        warnings.append("No references/templates/tools are declared in SKILL.md.")

    for relative in refs:
        if not (root / relative).exists():
            fail(errors, f"Broken reference: {relative}")

    if "/mnt/data" in text or "sandbox:/mnt/data" in text:
        fail(errors, "Controller contains a temporary runtime path.")

    if "## Workflow" not in text:
        fail(errors, "Controller has no '## Workflow' section.")

    if "## Completion Gate" not in text:
        warnings.append("Controller has no exact '## Completion Gate' section.")

    if not re.search(r"(?i)handoff|continuation state", text):
        fail(errors, "Controller does not define handoff or continuation state.")

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        try:
            body = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(body):
                fail(errors, f"Possible embedded secret in {path.relative_to(root)}")

    if errors:
        print("NO-GO")
        for error in errors:
            print(f"ERROR: {error}")
        for warning in warnings:
            print(f"WARNING: {warning}")
        return 1

    print("GO")
    print(f"Controller lines: {len(lines)}")
    print(f"Resolved references: {len(refs)}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
