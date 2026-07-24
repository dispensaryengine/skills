# Skill Package Testing Contract

## Static Validation

Required:

```text
frontmatter parses
name exists
description exists
exactly one controller H1
primary reference exists
all relative references exist
no /mnt/data links
no obvious secret assignments
controller has workflow
controller has validation
controller has handoff or continuation state
```

Use `tools/validate_skill_package.py`.

## Behavioral Validation

Test the skill with at least three scenarios:

### Nominal task

The user provides sufficient inputs.

Expected:

- correct references selected;
- workflow executed;
- required outputs produced;
- completion state accurate.

### Incomplete task

Important details are missing.

Expected:

- blocking facts identified;
- reversible assumptions used where safe;
- no invented source data;
- progress continues where possible.

### Failure task

A dependency, credential, test, or tool fails.

Expected:

- failure classified;
- retry bounded;
- evidence preserved;
- handoff updated;
- no false claim of success.

## Reference Routing Test

Provide tasks that require different references.

Expected:

- implementation task does not load style-only material;
- formal document task loads style contract;
- security-sensitive task loads security contract;
- runtime-specific task loads the matching implementation reference.

## Regression Test

When refactoring an existing skill:

1. list all original obligations;
2. map each obligation to its new file;
3. verify no obligation was silently removed;
4. flag deliberate changes;
5. run representative prompts before and after.

## Release Evidence

Return:

```yaml
STATIC_VALIDATION:
BEHAVIORAL_SCENARIOS:
REFERENCE_ROUTING:
REGRESSION_MAPPING:
KNOWN_GAPS:
RELEASE_DECISION: "GO | GO_WITH_RISKS | NO_GO"
```
