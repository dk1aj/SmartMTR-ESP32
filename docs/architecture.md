# Architecture

## Overview
Project: `SmartMTR-ESP32` (ESP-IDF project name: `aetherknob`)

Purpose: run a SmartMTR-style FlexRadio meter and controller on an Elecrow
CrowPanel 2.1-inch ESP32-S3 rotary display. The device uses native USB vendor
HID to exchange CTR2 messages with AetherSDR; it does not open its own network
connection to the radio.

## Main components

| Component | Responsibility | Source of truth |
|---|---|---|
| Board support | Panel power, RGB display, touch, dial, and backlight | `main/board.c` |
| USB/CTR2 transport | TinyUSB HID lifecycle, link task, bounded action queue | `main/usb_link.c` |
| CTR2 codec | Framing, sequencing, capability negotiation, spectrum extension | `main/ctr2_link.c` |
| SmartSDR client | Status parsing, binding, commands, VITA-49 meter updates | `main/flex_api.c` |
| Shared state | Radio, slice, meter, link, and spectrum state | `main/model.c`, `main/model.h` |
| Menu rules | Row metadata, value projection, and command construction | `main/menu_items.c` |
| UI | LVGL face, spectrum, meter rendering, and input dispatch | `main/ui.c`, `main/menu.c` |

## Data flow
```text
FlexRadio ↔ AetherSDR CTR2 Proxy ↔ USB HID / usb_link
                                         │
                                         ▼
                              flex_api + ctr2_link
                                         │
                                         ▼
                                  shared model
                                         │
                                         ▼
                              LVGL face/menu rendering

Touch + rotary dial → UI/menu actions → usb_link action queue
                    → flex_api commands → CTR2 USB relay → FlexRadio
```

## Canonical paths
- Incoming SmartSDR lines and VITA-49 datagrams are normalized only by
  `main/flex_api.c`.
- `knob_model_t` in `main/model.h` is the canonical runtime state shared by the
  radio task and UI. Access is serialized by `model_lock()`.
- Menu metadata and radio command construction are centralized in
  `main/menu_items.c`; `main/menu.c` renders and edits those definitions.
- CTR2 wire framing and extension validation are centralized in
  `main/ctr2_link.c`.
- Protocol facts relied on by the client are recorded in
  `docs/smartsdr-api-notes.md`.

## State ownership

| State | Owner | Consumers |
|---|---|---|
| `knob_model_t` | Radio task through `flex_api.c`, under model lock | `ui.c`, `menu.c` via a locked snapshot |
| CTR2 receive/transmit state | `usb_link.c` | USB callbacks and radio task |
| Menu definition table | `menu_items.c` | `menu.c`, `flex_api.c`, host tests |
| UI interaction state | `ui.c`, `menu.c` | LVGL callbacks and refresh timer |

## Persistence
The firmware has no documented database or persistent application store.
Runtime state is held in bounded static structures. Local ESP-IDF build output,
resolved components, SDK configuration, host binaries, and preview images are
excluded by `.gitignore`.

## External dependencies

| Dependency | Version | Purpose |
|---|---:|---|
| ESP-IDF | `>=6.0` | ESP32-S3 runtime and build system |
| `espressif/esp_lcd_st7701` | `^2` | ST7701 display support |
| `espressif/esp_lvgl_port` | `^2` | LVGL integration |
| LVGL | `^9.2` | User interface |
| `espressif/esp_tinyusb` | `^2` | Native USB vendor HID |
| `espressif/esp_lcd_panel_io_additions` | `^1` | Panel I/O support |
| AetherSDR CTR2 Proxy | compatible CTR2 USB link v0 | Relay between USB HID and the FlexRadio network connection |

## Lifecycle
1. `app_main()` creates the model lock, initializes the board and LVGL UI, and
   starts the USB link task.
2. The USB task initializes the SmartSDR client and CTR2 receiver, negotiates
   supported extensions, and waits for the AetherSDR relay.
3. On a relay connection, the client binds to a GUI station, subscribes to
   client/slice/transmit/meter state, enables keepalives, and updates the model.
4. The UI periodically copies the model while holding its lock, then renders
   from the snapshot without holding the lock.
5. Dial and touch actions enter a bounded queue; the radio task converts them
   to SmartSDR commands.
6. Disconnects clear connection-dependent model state. CTR2 framing errors
   restart the link state machine; registration and keepalive traffic is
   rate-limited by the task's periodic timing.

## Known limitations
- Display bring-up, encoder detents, touch orientation, and relayed UDP meters
  are not yet documented as verified on target hardware.
- The controller depends on AetherSDR's CTR2 Proxy; it has no standalone radio
  network transport.
