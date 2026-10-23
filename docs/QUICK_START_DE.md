# SmartMTR-ESP32 – Quick Start

> Bedienlogik und Anzeige sind aus dem aktuellen Quelltext abgeleitet. Display, Touch-Ausrichtung, Drehgeberzählung und der Messwertpfad sind noch nicht vollständig an Hardware verifiziert.

![SmartMTR-ESP32 UI-Übersicht](../output/images/SmartMTR-ESP32_UI_Collage.png)

## Erste Verbindung

1. SmartMTR-ESP32 über **USB-5V-IN** mit dem PC verbinden, auf dem AetherSDR läuft.
2. AetherSDR starten und die Verbindung zum FlexRadio herstellen.
3. In AetherSDR das Applet **CTR2 Proxy** öffnen.
4. Als Mode **USB** wählen.
5. Als Gerät **AetherKnob** (`AETHER_KNOB`) auswählen.
6. **Start** drücken.
7. Auf dem Controller zuerst **Waiting for AetherSDR** erwarten; nach erfolgreicher Bindung erscheint die Hauptanzeige.
8. Den gewünschten Slice in AetherSDR aktivieren. Seine Frequenz und Messwerte erscheinen am Controller.
9. Drehknopf drehen und prüfen, ob der aktive Slice um die angezeigte Schrittweite abgestimmt wird.
10. Bei Bedarf auf die **TX**-Fläche eines Slice tippen, um ihn als TX-Slice zu wählen. Das tastet den Sender nicht.

## Kompakte Bedienreferenz

| Aktion | Ergebnis |
| --- | --- |
| Drehknopf drehen | Aktiven Slice abstimmen; im Parameter-/Menümodus Wert ändern |
| Drehknopf kurz klicken | Nächste Schrittweite; Parameterbearbeitung verlassen |
| Drehknopf 0,6 s halten | Tune Lock ein/aus; im Menü zurück bzw. schließen |
| Kachel antippen | Parameter für den Drehknopf wählen; gelbe Umrandung |
| AF/AGC halten | AGC-Modus weiterschalten |
| FILT halten | Nächste Schrittweite |
| NR/NB/ANF halten | Funktion ein-/ausschalten |
| Nach unten wischen | Menü öffnen, wenn die Funkverbindung gebunden ist |
| Seitlich wischen | Zwischen Kacheln und Spektrum wechseln |
| TX-Fläche antippen | TX-Slice wählen; keine Sendertastung |

Fehlt das Spektrum, bleiben die Kacheln verfügbar. Bleibt **Waiting for AetherSDR** stehen, CTR2 Proxy stoppen, USB-Gerät und Mode prüfen und erneut starten. Sicherer Neustart: Proxy stoppen, **RESET** kurz drücken, auf `AETHER_KNOB` warten und Proxy wieder starten.
