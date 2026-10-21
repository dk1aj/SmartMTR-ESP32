# TESTING.md

## Testing philosophy
Do not claim PASS for anything not actually tested.

Separate:
- offline/unit tests
- integration tests
- live/runtime tests
- visual/manual tests

## Minimum pre-commit checks
1. Repository state reviewed
2. Relevant tests pass
3. Impacted consumers checked
4. No unrelated files in diff
5. No sensitive/generated artifacts
6. Documentation updated if needed

## Offline tests
The primary host suite builds selected portable sources with AddressSanitizer
and UndefinedBehaviorSanitizer, then exercises SmartSDR parsing and commands,
menu behavior, model selection, meter ballistics, CTR2 framing, extensions, and
spectrum helpers.

Requirements: GNU Make and a C11 compiler with the sanitizer flags supported by
`test/Makefile`.

```bash
make -C test check
```

Clean the host binary with:

```bash
make -C test clean
```

## Integration tests
Build the firmware with ESP-IDF 6.0 or later after exporting the desired IDF
environment:

```bash
idf.py build
```

This validates component resolution and compilation, but it does not validate
the display, touch controller, dial, USB enumeration, AetherSDR relay, or radio.

## Live tests
Target-hardware validation requires the CrowPanel, AetherSDR with the CTR2
Proxy, and a compatible FlexRadio setup. Follow the connection and flashing
steps in `README.md`, then verify:

- the panel initializes at 480×480 and remains stable,
- touch orientation and swipe/tap/hold gestures are correct,
- one physical detent produces one expected tuning step,
- native USB re-enumerates as `AetherSDR AETHER_KNOB`,
- the relay binds the controller to the selected station,
- slice, transmit, menu, and meter state update without duplicate sessions,
- VITA-49 meters arrive over the relay's UDP path, and
- reconnecting the USB relay restores state cleanly.

Do not key a transmitter or alter a live station unless the test operator has
explicitly prepared a safe radio test setup.

## Visual tests
The desktop preview requires resolved LVGL sources under
`managed_components/lvgl__lvgl`. Scripted geometry and interaction checks are:

```bash
make -C test/preview touchtest
```

Rendering all documented faces additionally requires ImageMagick's `magick`
command:

```bash
make -C test/preview faces
```

Inspect the generated images for clipping, overlap, readability, correct menu
states, both spectrum spans, and bound/waiting/transmit views. Generated PPM
and PNG files are ignored and must not be committed.

## Failure handling
If a test fails:
- stop
- do not commit
- do not push
- preserve evidence
- report exact failure

## Current evidence boundary

`README.md` records that the firmware builds and the API client passes its host
tests, but it also records several hardware checks as pending. Re-run any check
needed for the current change; do not treat historical documentation as a test
result for a new commit.
