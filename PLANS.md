# PLANS.md

## Current stable version
`<UNKNOWN — no release tag or version declaration is present in the repository>`

## Current phase
Host-tested firmware implementation; target-hardware validation remains.

## Roadmap

### Stage 1 — Firmware foundation
Status: `DONE`
Goals:
- ESP-IDF project configuration for the ESP32-S3 CrowPanel.
- CTR2 framing, USB HID transport, shared model, and SmartSDR client.

Acceptance:
- Firmware sources and dependencies are defined by CMake and
  `main/idf_component.yml`.
- The host test exercises the protocol, model, menu, meter, and CTR2 paths.

### Stage 2 — SmartMTR controls and UI
Status: `DONE` for the implemented source; hardware verification is pending.

- SmartMTR-style face, meters, spectrum, touch controls, rotary-dial controls,
  and swipe-down menu are implemented.
- The desktop preview and scripted interaction checks are available under
  `test/preview/`.

### Stage 3 — Target-hardware validation
Status: `PLANNED`

- Verify display bring-up and touch orientation.
- Calibrate encoder counts per detent.
- Exercise meters over the CTR2 relay's UDP path on hardware.

### Stage 4 — Release hardening
Status: `PLANNED`

- Re-run the firmware build and all offline checks in the release environment.
- Record a stable version only after the project owner chooses a versioning
  scheme and the hardware checks pass.

## Known blockers
- Hardware validation evidence is not present for display bring-up, encoder
  calibration, touch orientation, or relayed UDP meters.
- A stable release version and versioning policy have not been declared.

## Deferred work
- No additional deferred features are documented as commitments.

## Decision log

### 2026-10-21
Decision: Keep the stable version explicitly unknown.
Reason: The repository contains no release tag or source version declaration;
inventing one would misrepresent project state.
