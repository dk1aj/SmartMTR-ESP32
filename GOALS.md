# GOALS.md

## Project
`SmartMTR-ESP32`

## Primary goals
1. Provide a SmartMTR-style 480×480 meter, spectrum, and control interface on
   the Elecrow CrowPanel 2.1-inch ESP32-S3 rotary display.
2. Control the active FlexRadio station and its slices through AetherSDR's
   CTR2 USB relay, without requiring Wi-Fi configuration on the controller.
3. Keep radio state, menu behavior, meter ballistics, and CTR2 framing covered
   by deterministic host tests while completing hardware validation.

## Quality goals
- Preserve a single, explicit source of truth for radio state.
- Keep protocol parsing, menu command construction, and UI rendering separated.
- Bound fixed-size buffers, queues, and link payloads for embedded operation.
- Maintain reproducible ESP-IDF builds and deterministic host tests.
- Keep protocol and hardware assumptions documented alongside the code.

## Non-goals
- Direct Wi-Fi configuration or a direct radio network connection on the
  controller; the supported transport is the CTR2 USB relay through AetherSDR.
- Keying the transmitter from the menu; VOX and TUNE are deliberately omitted.
- Replacing or obscuring the original SmartMTR design attribution.

## Success criteria
A release is successful when:
- the firmware builds with the documented ESP-IDF version,
- `make -C test check` passes,
- display, touch, dial, and relayed meter behavior are verified on target
  hardware,
- critical controls and existing CTR2 behavior have no known regressions,
- documentation matches runtime behavior, and
- the release repository state is clean and understood.
