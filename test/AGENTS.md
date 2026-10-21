# test/AGENTS.md

Scope: host and desktop-preview tests under `test/`.

- Keep fixtures deterministic and synthetic.
- Do not weaken assertions to accommodate a behavior change.
- Run `make -C test check` for portable protocol/model/menu/meter changes.
- Run `make -C test/preview touchtest` for UI geometry or interaction changes
  when the managed LVGL component is available.
- Run `make -C test/preview faces` and inspect the images for visual changes
  when ImageMagick is available.
- Host and preview results are not substitutes for target-hardware validation.
