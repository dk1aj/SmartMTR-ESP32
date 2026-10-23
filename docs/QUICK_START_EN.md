# SmartMTR-ESP32 Quick Start

> Controls and displays are derived from the current source. Display bring-up, touch orientation, encoder counts, and the meter path have not yet been fully verified on hardware.

![SmartMTR-ESP32 UI overview](../output/images/SmartMTR-ESP32_UI_Collage.png)

## First connection

1. Connect SmartMTR-ESP32 to the AetherSDR PC through **USB-5V-IN**.
2. Start AetherSDR and connect it to the FlexRadio.
3. Open the **CTR2 Proxy** applet in AetherSDR.
4. Select **USB** as the mode.
5. Select **AetherKnob** (`AETHER_KNOB`) as the device.
6. Press **Start**.
7. Expect **Waiting for AetherSDR** first; the main display appears after the station binding succeeds.
8. Activate the required slice in AetherSDR. Its frequency and meter data appear on the controller.
9. Turn the rotary dial and verify that the active slice tunes by the displayed step.
10. If required, tap a slice's **TX** area to select it as the TX slice. This does not key the transmitter.

## Compact control reference

| Action | Result |
| --- | --- |
| Turn rotary dial | Tune active slice; adjust value in parameter/menu edit mode |
| Short dial click | Next tuning step; leave parameter edit mode |
| Hold dial for 0.6 s | Toggle tune lock; go back/close while in the menu |
| Tap a tile | Select parameter for the dial; yellow outline |
| Hold AF/AGC | Step through AGC mode |
| Hold FILT | Select next tuning step |
| Hold NR/NB/ANF | Toggle the function |
| Swipe down | Open menu when the radio link is bound |
| Swipe sideways | Switch between tiles and spectrum |
| Tap a TX area | Select TX slice; does not key transmitter |

If the spectrum is absent, the tiles remain available. If **Waiting for AetherSDR** remains on screen, stop CTR2 Proxy, check the USB device and mode, then start it again. Safe restart: stop the proxy, briefly press **RESET**, wait for `AETHER_KNOB`, and restart the proxy.
