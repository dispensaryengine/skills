# Migration Map

The original monolithic `project-workflow-engine` skill contained 19 major sections in one 1,342-line controller.

This package preserves those responsibilities as follows.

| Original responsibility | New authoritative location |
|---|---|
| Purpose | `SKILL.md`, `references/project_foundation.md` |
| Operating principles | `references/project_foundation.md` |
| Input variables | `references/project_foundation.md`, `templates/project_variables.yaml` |
| Variable resolution | `references/project_foundation.md` |
| Project classification | `references/project_foundation.md` |
| Required artifacts | `references/artifact_contract.md` |
| Standard phases 0–8 | `references/workflow_contract.md` |
| Failure recovery | `references/failure_recovery_contract.md` |
| Existing repair mode | `references/mode_contracts.md` |
| New bootstrap mode | `references/mode_contracts.md` |
| Migration mode | `references/mode_contracts.md` |
| Data-pipeline mode | `references/mode_contracts.md` |
| Agent rules and tool priority | `references/project_foundation.md` |
| Session output | `references/operations_runbook.md` |
| Workflow output templates | `templates/` |
| Quality gates | `references/testing_release_contract.md` |
| Anti-patterns | `references/project_foundation.md` |
| Default decisions | `references/project_foundation.md` |
| Final agent instruction | `SKILL.md` |

## Corrections Applied

- reduced the active controller to one H1 and a compact routing role;
- removed malformed top-level heading repetition;
- separated stable principles from mode-specific workflows;
- separated validation and release from implementation phases;
- separated failure recovery from the normal path;
- replaced one mandatory artifact set with standard and compact options;
- added explicit audit, feature, refactor, release, and handoff modes;
- added revision-bound test and deployment evidence;
- added a project-system validator;
- preserved the original evidence, vertical-slice, recovery, migration, data-lineage, and handoff principles.
