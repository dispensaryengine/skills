# Project Workflow Engine

A modular development operating system for starting, continuing, repairing, refactoring, migrating, auditing, releasing, and handing off software projects.

## Package Model

```text
SKILL.md
    ↓
project foundation
    ↓
workflow and artifact contracts
    ↓
mode, testing, recovery, and operations contracts
    ↓
templates and validation
```

## Use

Load `SKILL.md`.

The controller selects the references needed for the current project mode.

## Validate a Generated Project System

```bash
python tools/validate_project_system.py /path/to/project
```

The validator accepts either:

- the standard `docs/` artifact set; or
- a compact `docs/PROJECT_SYSTEM.md`.

## Design Goal

A project should remain understandable and continuable without access to the conversation that created it.
