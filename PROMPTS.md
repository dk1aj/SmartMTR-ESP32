# PROMPTS.md

## Read-only repository audit
```text
Read AGENTS.md first.
Use RTK for repository inspection and CodeGraph for dependency analysis.

Do not change files.
Do not deploy.
Do not commit.
Do not push.

Inspect:
- git status
- relevant diffs
- recent log
- definitions/callers/consumers
- tests
- architecture dependencies

Report current state, unexpected changes, likely impact, blockers and next step.
STOP FOR REVIEW.
```

## Impact analysis before change
```text
Read AGENTS.md first.
Use CodeGraph before editing.

Map:
- definition
- callers
- consumers
- upstream producers
- downstream dependencies
- tests
- configuration

Identify canonical path, duplicate implementations and risk areas.
Do not edit until the impact map is complete.
```

## Focused implementation
```text
Read AGENTS.md first.
Implement only the requested change.

Rules:
- reuse canonical paths
- do not duplicate logic
- preserve backward compatibility
- update tests
- update docs if behavior changes

After changes:
- run relevant tests
- use CodeGraph for post-change verification
- inspect final diff with RTK
- report before/after

Do not commit/push until validation passes.
```

## Bug diagnosis only
```text
Read AGENTS.md first.
Do not modify code.

Trace the failing value/path from source to consumer.

For each stage report:
- source
- field/property name
- datatype
- freshness/state
- transformation
- consumer expectation

Classify root cause:
A. source missing
B. projection mismatch
C. UI mismatch
D. datatype error
E. scale/range error
F. stale/freshness error
G. lifecycle issue
H. other

STOP FOR REVIEW.
```

## Release closure
```text
Read AGENTS.md first.
Do not add features.

Complete release validation only.

Verify:
- runtime version
- changed feature
- critical regressions
- repository validation
- deployment state
- git status

If everything passes:
- commit
- push
- verify HEAD == origin/main
```

## SmartMTR-ESP32 host validation
```text
Read AGENTS.md and docs/TESTING.md first.
Do not change runtime behavior.

Run make -C test check and, when LVGL managed components and ImageMagick are
available, run make -C test/preview touchtest and make -C test/preview faces.
Inspect failures against the canonical implementation under main/.

Report separately:
- host/unit result
- preview interaction result
- visual render result
- ESP-IDF build result
- hardware checks not performed

Never describe a host or preview result as target-hardware validation.
```
