#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

STANDARD_DOCS = [
    "PROJECT_CONTEXT.md",
    "PROJECT_REQUIREMENTS.md",
    "ARCHITECTURE.md",
    "EXECUTION_PLAN.md",
    "DECISION_LOG.md",
    "RISK_REGISTER.md",
    "TEST_STATUS.md",
    "WORK_LOG.md",
    "HANDOFF.md",
    "RELEASE_CHECKLIST.md",
]

REQUIRED_HANDOFF_TERMS = [
    "branch",
    "commit",
    "verified",
    "blocker",
    "next",
    "rollback",
]

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"(?i)(password|token|secret)\s*[:=]\s*['\"][^<'\"{][^'\"]{7,}['\"]"),
]

def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    root = args.project.resolve()
    docs = root / "docs"
    errors: list[str] = []
    warnings: list[str] = []

    if not root.exists():
        print("NO-GO")
        print(f"ERROR: Project path does not exist: {root}")
        return 1

    compact = docs / "PROJECT_SYSTEM.md"
    if compact.exists():
        artifact_paths = [compact]
        combined = read_text(compact)
        for term in ["requirement", "architecture", "execution", "test", "work log", "handoff"]:
            if term not in combined.lower():
                errors.append(f"PROJECT_SYSTEM.md is missing a visible {term} section.")
    else:
        artifact_paths = [docs / name for name in STANDARD_DOCS]
        missing = [path.name for path in artifact_paths if not path.exists()]
        if missing:
            errors.append("Missing standard project artifacts: " + ", ".join(missing))

    handoff = docs / "HANDOFF.md"
    if compact.exists():
        handoff_text = read_text(compact)
    elif handoff.exists():
        handoff_text = read_text(handoff)
    else:
        handoff_text = ""

    for term in REQUIRED_HANDOFF_TERMS:
        if term not in handoff_text.lower():
            errors.append(f"Handoff is missing required concept: {term}")

    test_status = docs / "TEST_STATUS.md"
    if compact.exists():
        test_text = read_text(compact)
    elif test_status.exists():
        test_text = read_text(test_status)
    else:
        test_text = ""

    if not re.search(r"(?i)revision|commit", test_text):
        errors.append("Test status is not bound to a revision or commit.")

    if not re.search(r"(?i)pass|fail|unavailable|not_applicable|not applicable", test_text):
        errors.append("Test status does not contain explicit test outcomes.")

    env_example = root / ".env.example"
    if not env_example.exists():
        warnings.append(".env.example is missing.")

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        body = read_text(path)
        if not body:
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(body):
                errors.append(f"Possible embedded secret in {path.relative_to(root)}")

    if args.strict:
        for path in artifact_paths:
            if path.exists() and path.stat().st_size < 80:
                errors.append(f"Artifact appears empty: {path.relative_to(root)}")

    if errors:
        print("NO-GO")
        for error in errors:
            print(f"ERROR: {error}")
        for warning in warnings:
            print(f"WARNING: {warning}")
        return 1

    print("GO")
    print("Project operating system is structurally complete.")
    for warning in warnings:
        print(f"WARNING: {warning}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
