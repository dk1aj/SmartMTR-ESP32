# AGENTS.md

## Project
Project: `SmartMTR-ESP32` (firmware project name: `aetherknob`)
Repository root: repository top level (`git rev-parse --show-toplevel`)
Purpose: ESP32-S3 firmware for a SmartMTR-style FlexRadio controller on the
Elecrow CrowPanel 2.1-inch rotary display, connected through AetherSDR's CTR2
USB relay.

Read this file before code, config, deployment or documentation changes.

## General rules
- Inspect repository state before editing.
- Prefer canonical existing paths over duplicate implementations.
- Do not invent runtime semantics.
- Keep changes focused on requested scope.
- Do not mix unrelated work into one change set.
- If repository state materially differs from the task, STOP and report.

## RTK
Use RTK for supported repository/Git work where practical.

Prefer:
```bash
rtk git status
rtk git diff
rtk git log -5 --oneline
rtk gain --project --format json
```

Use RTK for compact status/log/diff/search/test output when supported.
RTK savings are compression metrics, not API billing.

## CodeGraph
Use CodeGraph before non-trivial runtime or architecture changes.

Before editing map:
- definitions
- callers
- consumers
- dependencies
- tests
- configuration
- canonical producers and data paths

Prefer reuse over duplicate:
- parsers
- subscriptions
- state machines
- caches
- business logic

After changes, use CodeGraph again to verify no duplicate paths or unexpected dependencies were introduced.

## Repository safety
Before changes:
- inspect `git status`
- inspect relevant diff
- inspect recent log
- identify unrelated uncommitted work

Never overwrite unrelated user work.

Do not commit:
- credentials
- tokens
- passwords
- session IDs
- private keys
- generated DBs
- runtime logs
- temp files
- local evidence
- machine-specific artifacts

## Implementation
- Make the smallest coherent change.
- Keep source-of-truth logic centralized.
- Prefer explicit state over hidden side effects.
- Keep cleanup idempotent where lifecycle code is involved.
- Bound arrays, caches, queues, timers and retries.
- Avoid duplicate network clients and polling.
- Treat `main/model.{c,h}` as the canonical shared radio/UI state.
- Keep radio protocol parsing and command generation in `main/flex_api.c` and
  menu command rules in `main/menu_items.c`; do not duplicate either in UI code.
- Preserve the SmartMTR attribution in `README.md` and `NOTICE.md`.
- Preserve the MIT notices in `main/ctr2_link.{c,h}`; the remainder of the
  project is GPL-3.0.

## Testing
Follow `docs/TESTING.md`.

The primary offline check is:

```bash
make -C test check
```

At minimum:
- run relevant offline/unit tests
- validate changed path
- validate impacted consumers
- run regression checks
- report what was not tested

Never claim PASS for a test not actually performed.

## Deployment
Deploy only when required and validation has passed.

After deploy verify:
- runtime startup
- changed functionality
- critical existing functionality
- no duplicate connections/subscriptions
- no unexpected runtime errors

If deployment breaks existing functionality:
STOP, restore last known-good state, report exact failure.

## Documentation
Keep:
- `GOALS.md` for objectives
- `PLANS.md` for roadmap
- `docs/architecture.md` for architecture
- `docs/TESTING.md` for testing
- `PROMPTS.md` for reusable Codex prompts
- `docs/smartsdr-api-notes.md` for protocol facts used by the implementation

## Commit / Push
Before commit:
- run tests
- inspect final diff
- verify no unrelated/sensitive/generated files

After push verify:
- `HEAD == origin/main` or project default branch
- working tree state understood

## Before / After report
For non-trivial changes report:

### Before
- previous behavior
- limitation/problem
- relevant architecture

### After
- new behavior
- architectural impact
- compatibility impact

## Efficiency report
Where available:

### RTK
Run:
```bash
rtk gain --project --format json
```

Report:
- commands
- input tokens
- output tokens
- tokens saved
- savings percent

Clarify that values are RTK compression metrics, not API billing.

### CodeGraph
Report:
- query count
- symbols/files returned
- major areas narrowed

Do not invent CodeGraph token savings if unavailable.

## STOP conditions
STOP before editing/deploying when:
- repository state contradicts the task
- semantics are unknown
- dependency/runtime blocker exists
- a second competing implementation would be needed
- unrelated work would be overwritten
