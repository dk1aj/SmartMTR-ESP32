# main/AGENTS.md

Scope: ESP-IDF firmware under `main/`.

- Preserve the canonical path `usb_link` → `flex_api` → locked `model` → UI.
- Keep SmartSDR parsing and command generation out of LVGL event handlers.
- Keep menu metadata and command rules centralized in `menu_items.c`.
- Access `knob_model_t` under `model_lock()` and render from a snapshot; do not
  hold the model lock while drawing.
- Keep queues, protocol frames, string buffers, retry timing, and arrays bounded.
- Preserve CTR2 wire compatibility and the MIT notices in `ctr2_link.{c,h}`.
- Update `test/host_test.c` for portable protocol, model, menu, meter, or CTR2
  behavior changes.
