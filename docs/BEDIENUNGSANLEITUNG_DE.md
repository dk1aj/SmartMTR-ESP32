# SmartMTR-ESP32 – Bedienungsanleitung

Diese Anleitung beschreibt den derzeit im Repository implementierten Stand des
SmartMTR-ESP32 („AetherKnob“). Sie richtet sich an Funkamateure, die das Gerät
mit AetherSDR und einem FlexRadio bedienen möchten.

## Geltungsbereich und Prüfstatus

Die Bedienlogik, das SmartSDR-Protokoll, die Menübefehle, die Messinstrument-
Ballistik, die CTR2-Übertragung und die Spektrum-Hilfsfunktionen sind im
Quelltext umgesetzt und durch Offline-Tests abgedeckt. Eine PC-Vorschau mit
skriptgesteuerten Touch- und Drehknopfaktionen ist ebenfalls vorhanden.

Noch nicht am Zielgerät nachgewiesen sind Display-Inbetriebnahme,
Touch-Ausrichtung, Drehgeberzählung pro Rastung und die über CTR2 weitergeleiteten
UDP-Messwerte. Entsprechende Funktionen werden in dieser Anleitung als
**implementiert, aber noch nicht hardwareverifiziert** bezeichnet. Ein
Firmware-Build oder eine PC-Vorschau ersetzt diese Hardwareprüfung nicht.

## UI-Übersicht

![Sechs Zustände der SmartMTR-ESP32-Bedienoberfläche](../output/images/SmartMTR-ESP32_UI_Collage.png)

*Quelltextbasierte UI-Darstellungen, keine Hardware-Fotos.*

## 1. Geräteübersicht

SmartMTR-ESP32 ist ein Bedien- und Anzeigegerät für eine FlexRadio-Station. Es
läuft auf dem **Elecrow CrowPanel 2.1\" HMI ESP32 Rotary Display** (DHE03921D)
mit ESP32-S3, rundem 480×480-IPS-Touchdisplay und einem drückbaren Drehgeber.
Die Gestaltung der Rundanzeige basiert auf SmartMTR von Dariusz Socha, SQ5X.

Das Gerät baut keine eigene WLAN- oder LAN-Verbindung zum Funkgerät auf. Es
wird per USB mit dem PC verbunden, auf dem AetherSDR läuft. Das Applet
**CTR2 Proxy** in AetherSDR überträgt Status, Messwerte und Bedienbefehle
zwischen AetherKnob und FlexRadio. Dabei arbeitet AetherKnob als eigener
SmartSDR-API-Client und bindet sich an die in AetherSDR beziehungsweise
SmartSDR aktive GUI-Station.

## 2. Anschlüsse und Bedienelemente

| Element | Funktion |
| --- | --- |
| Runddisplay | Zeigt bis zu zwei Slices, Messinstrumente, Spektrum/Kacheln, Status und Menü. |
| Touchdisplay | Tippen, Berühren und Halten sowie Wischgesten. |
| Drehgeber | Abstimmen, Parameter ändern und im Menü navigieren. Eine mechanische Rastung soll genau einen Bedienschritt auslösen; dies ist noch nicht hardwareverifiziert. |
| Drucktaster im Drehgeber | Kurzer Klick oder Gedrückthalten ab 0,6 s. |
| **USB-5V-IN** (4-polig, MX1.25) | Stromversorgung und native USB-Verbindung zum PC über das mitgelieferte MX1.25-USB-Kabel. Dient zugleich zum Flashen. |
| **UART** (4-polig: RX, TX, 5V, GND) | Diagnoseausgaben mit 115200 Baud. Nur einen 3,3-V-USB-Seriell-Adapter verwenden und dessen Versorgung nicht mit dem 5-V-Pin verbinden. |
| **I2C** (4-polig: SCL, SDA, 5V, GND) | Freier Erweiterungsanschluss; derselbe Bus wird intern bereits für Touch (Adresse 0x15) und PCF8574 (0x21) verwendet. |
| **RESET** | Startet das Gerät neu. Zusammen mit BOOT zum Aufrufen des ROM-Downloadmodus. |
| **BOOT** | Beim Zurücksetzen gedrückt halten, um den Flashmodus aufzurufen. |

Die USB-Funktion der laufenden Firmware ist ein herstellerspezifisches
HID-Gerät. Die normale USB-Verbindung stellt deshalb keine serielle Konsole
bereit; Protokollausgaben liegen am UART-Anschluss an.

## 3. Einschalten und Verbindung herstellen

1. FlexRadio einschalten und AetherSDR auf dem PC starten.
2. AetherSDR mit der gewünschten FlexRadio-Station verbinden.
3. AetherKnob über **USB-5V-IN** mit dem PC verbinden.
4. In AetherSDR das Applet **CTR2 Proxy** öffnen.
5. Als **Mode** den Eintrag **USB** wählen.
6. Als Gerät **AetherKnob** beziehungsweise das USB-Produkt
   **AETHER_KNOB** wählen.
7. **Start** drücken.

Erwartete Anzeigen:

| Anzeige | Bedeutung |
| --- | --- |
| `AetherKnob – Plug into the PC running AetherSDR` | Kein USB-Host verbunden oder USB-Verbindung getrennt. |
| `Waiting for AetherSDR` mit Hinweis auf CTR2 Proxy | USB ist vorhanden; CTR2 Proxy hat die Verbindung noch nicht gestartet. |
| `Radio connected – Waiting for a SmartSDR or AetherSDR station` | Das Radio ist über den Proxy erreichbar, aber noch keine passende GUI-Station gebunden. |
| Rundanzeige ohne Statusfenster | AetherKnob ist an eine Station gebunden. |

Die Start- und Bindefunktion ist implementiert und offline getestet; die
vollständige Verbindungskette mit echter Hardware ist laut Repository noch
nicht als Live-Test nachgewiesen.

## 4. Hauptanzeige

Die obere Slice-Anzeige gehört zum aktiven Slice der gebundenen Station. Falls
kein Slice als aktiv gemeldet wird, verwendet AetherKnob das erste zu dieser
Station gehörende Slice. Unten erscheint, sofern vorhanden, ein weiteres Slice
derselben Station.

| Anzeige | Bedeutung |
| --- | --- |
| Große Frequenz | Slice-Frequenz im Format `MHz.kHz.Hz`. |
| Slice-Buchstabe und Betriebsart | Zum Beispiel `A USB`. |
| Filter-/Antennenzeile | Untere und obere Filtergrenze sowie RX-Antenne. |
| S-Meter-Bögen | Empfangspegel des jeweiligen Slice, linear in dB von S0 bis S9+40. Der weiße Marker zeigt den gehaltenen Spitzenwert. |
| **SWR** | Stehwellenverhältnis, Skala 1 bis 3. |
| **COMP** | Kompressionspegel, Skala 0 bis 25 dB. |
| **PWR** | Vorwärtsleistung, Skala 0 bis 100 W. |
| **MIC** | Mikrofonpegel, Skala −40 bis 0 dB. |
| **TX** am Slice | Kennzeichnet und wählt das Sendeslice; Einzelheiten siehe Abschnitt 11. |
| `STEP … Hz` | Aktuelle Abstimmschrittweite. |
| `DIAL ADJUSTS` | Drehgeber befindet sich im Parameter- statt im Abstimm-Modus. |
| `LOCKED` | Abstimmung des aktiven Slice ist gesperrt. |
| Mitte | Audiospektrum oder sechs Schnellfunktions-Kacheln. |

## 5. Bedienung mit dem Drehknopf

### Auf der Hauptanzeige

| Bedienung | Wirkung |
| --- | --- |
| Drehen | Stimmt das aktive Slice um eine Schrittweite je erkannter Rastung ab. Eine gesperrte Abstimmung ignoriert die Drehbewegung. |
| Kurz klicken | Wechselt zur nächsten Schrittweite: 10, 50, 100, 500, 1000, 5000, 10000 Hz und danach wieder 10 Hz. |
| Mindestens 0,6 s gedrückt halten | Schaltet **Tune lock** für das aktive Slice ein oder aus. |
| Drehen bei gelb markierter Kachel | Ändert den gewählten Parameter statt der Frequenz. |
| Kurz klicken im Parameter-Modus | Verlässt den Parameter-Modus; der Drehgeber stimmt danach wieder ab. |

Ein Tippen auf dieselbe bereits gelb markierte Kachel schaltet ebenfalls zurück
auf Abstimmung. Die Richtung und die Zahl der gezählten Impulse pro mechanischer
Rastung sind im Code festgelegt, aber noch nicht am Zielgerät bestätigt.

### Im Menü

Ohne gelben Bearbeitungsrahmen bewegt Drehen den weißen Auswahlrahmen. Ein
kurzer Klick übernimmt die markierte Zeile zur Bearbeitung. Danach ändert
Drehen den Wert. Einzelheiten stehen in Abschnitt 8.

## 6. Touch-Bedienung

| Geste | Wirkung auf der Hauptanzeige |
| --- | --- |
| Kachel antippen | Wählt ihren Parameter für den Drehgeber; gelber Rahmen. Erneutes Antippen derselben Kachel beendet den Parameter-Modus. |
| Kachel berühren und halten | Führt die jeweilige Schnellaktion aus; siehe Abschnitt 7. |
| **TX** antippen | Macht das betreffende, zur gebundenen Station gehörende Slice zum Sendeslice. |
| Nach unten wischen | Öffnet das Menü, sofern die Station gebunden ist. |
| Seitlich wischen | Schaltet zwischen Spektrum und Kacheln um. Ohne aktuelle Spektrumdaten bleiben die Kacheln sichtbar. |
| Spektrum antippen | Zeigt die Kacheln. |

Im Menü scrollt eine vertikale Wischbewegung die Liste. Auch eine auf einem
Schieberegler begonnene vertikale Bewegung darf das Scrollen übernehmen.
Schieberegler werden seitlich gezogen; Schalter und der AGC-Modusknopf werden
angetippt.

Touch-Ausrichtung und Gestenerkennung sind implementiert und in der
PC-Vorschau prüfbar, jedoch noch nicht auf dem CrowPanel hardwareverifiziert.

## 7. Kacheln und Schnellfunktionen

Der angezeigte Zahlenwert gehört immer zum aktiven Slice.

| Kachel | Kurzes Tippen, danach Drehgeber | Berühren und Halten |
| --- | --- | --- |
| **AF** | Audiopegel 0–100 ändern | AGC-Modus weiterschalten: off → slow → med → fast → off. AF besitzt keinen eigenen Ein/Aus-Schalter. |
| **AGC** | AGC-Schwelle 0–100 ändern; bei AGC `off` wird stattdessen der feste Empfangspegel geändert | AGC-Modus weiterschalten. |
| **FILT** | Filterbreite symmetrisch um die Passbandmitte in 50-Hz-Schritten ändern, begrenzt auf 50–12000 Hz | Nächste Abstimmschrittweite wählen. |
| **NR** | NR-Pegel 0–100 ändern | NR ein-/ausschalten. |
| **NB** | NB-Pegel 0–100 ändern | NB ein-/ausschalten. |
| **ANF** | ANF-Pegel 0–100 ändern | ANF ein-/ausschalten. |

Eine aktive Funktion erhält einen hervorgehobenen Kachelhintergrund. Der gelbe
Rahmen bedeutet ausschließlich: Dieser Parameter liegt aktuell auf dem
Drehgeber.

## 8. Menü

### Öffnen, schließen und scrollen

- Auf der gebundenen Hauptanzeige nach unten wischen, um das Menü zu öffnen.
- In der Liste nach oben oder unten wischen, um zu scrollen.
- Zum Schließen den Griff am unteren Rand antippen oder dort nach oben wischen.
- Alternativ den Drehknopf lange drücken, wenn gerade keine Zeile bearbeitet
  wird.
- Nach 8 Sekunden ohne Touch- oder Drehknopfaktivität schließt das Menü
  automatisch. Es schließt auch, wenn die Stationsbindung verloren geht.

Beim normalen Schließen werden bereits vorgewählte Listenwerte bestätigt. Ein
Langdruck während der Bearbeitung verlässt dagegen nur die Bearbeitung und
verwirft einen noch nicht gesendeten Vorschauwert.

### Bedienung per Touch

- Eine Wert- oder Auswahlzeile antippen: Zeile für den Drehknopf auswählen.
- Dieselbe Zeile erneut antippen: Bearbeitung beenden.
- Einen Regler seitlich ziehen: Pegel sofort ändern. Bei Auswahllisten wird der
  gelb dargestellte Vorschauwert erst beim Loslassen gesendet.
- Einen Schalter antippen: Funktion ein- oder ausschalten.
- Den kleinen AGC-Modusknopf antippen: `Off`, `Slow`, `Med`, `Fast`
  weiterschalten.
- Bei einer kombinierten Pegel-/Schalterzeile kann langes Berühren der Zeile
  ebenfalls die Ein/Aus-Funktion umschalten.

### Bedienung per Drehknopf

- **Weißer Rahmen:** Zeile ist nur markiert. Drehen bewegt die Markierung und
  scrollt die Liste mit.
- **Gelber Rahmen:** Zeile ist im Bearbeitungsmodus. Drehen ändert Pegel oder
  Auswahl. Bei einem reinen Ein/Aus-Eintrag bedeutet rechts drehen „Ein“ und
  links drehen „Aus“.
- Kurzer Klick auf eine weiß markierte Zeile: Bearbeitung beginnen.
- Kurzer Klick während einer kombinierten Pegel-/Schalterzeile: Schalter
  umlegen, Pegel bleibt auf dem Drehgeber.
- Kurzer Klick bei AGC: Modus weiterschalten, Pegel bleibt auf dem Drehgeber.
- Kurzer Klick bei anderen Zeilen: Bearbeitung beenden und eine Vorschau sofort
  übernehmen. Ohne Klick wird eine Drehknopf-Auswahl nach 0,7 s Stillstand
  gesendet.
- Langer Klick während der Bearbeitung: zurück, noch nicht gesendete Auswahl
  verwerfen.

Gelb dargestellter Text ist ein noch nicht endgültig gesendeter Listenwert.
Ein farblich hervorgehobener Zeilenhintergrund zeigt eine eingeschaltete
Funktion und ist nicht mit dem gelben Bearbeitungsrahmen gleichzusetzen.

## 9. Menüeinträge

Die englischen Namen entsprechen exakt der Geräteanzeige.

### Receive

| Eintrag | Wirkung und Werte |
| --- | --- |
| **Mode** | Betriebsart aus der vom Radio gelieferten Liste wählen. |
| **RX antenna** | Empfangsantenne aus der vom Radio gelieferten Liste wählen. |
| **Band** | 160 m, 80 m, 60 m, 40 m, 30 m, 20 m, 17 m, 15 m, 12 m, 10 m, 6 m, WWV oder GEN. Das Radio kann dabei den Bandstack abrufen und das Slice neu anlegen. |
| **RIT** | Ein/Aus und −9990 bis +9990 Hz in 10-Hz-Schritten. |
| **Filter low** | Untere Filtergrenze −12000 bis +12000 Hz, Schritt 50 Hz. In FM/NFM ausgeblendet. |
| **Filter high** | Obere Filtergrenze −12000 bis +12000 Hz, Schritt 50 Hz. In FM/NFM ausgeblendet. Mindestbreite 50 Hz; zulässige Grenzen hängen von Betriebsart und bei CW von der Tonhöhe ab. |
| **AGC** | Modus Off/Slow/Med/Fast und Pegel 0–100. Bei Off ist der Pegel der feste Empfangsgewinn, sonst die AGC-Schwelle. |
| **Squelch** | Ein/Aus und Schwelle 0–100. |
| **NR mode** | Off, NR, NRL, NRS, RNN oder NRF. NRL/NRS/RNN/NRF sind FLEX-8000/Aurora-Funktionen und werden von einem FLEX-6000 ignoriert. |
| **NR amount** | Pegel 0–100 der aktiven NR-Variante, sofern diese einen einstellbaren Pegel besitzt. |
| **ANF mode** | Off, ANF, ANFL oder ANFT. ANFL/ANFT sind FLEX-8000/Aurora-Funktionen und werden von einem FLEX-6000 ignoriert. |
| **ANF amount** | Pegel 0–100 der aktiven ANF-Variante, sofern diese einen einstellbaren Pegel besitzt. |
| **WNB** | Wide Noise Blanker ein/aus und Pegel 0–100. |
| **APF** | Audio Peak Filter ein/aus und Pegel 0–100; nur in CW-Betriebsarten sichtbar. |
| **Mute** | Audio des aktiven Slice ein-/ausschalten. |
| **Pan** | Stereoposition 0–100 in Zweierschritten; Anzeige `L100` bis `L2`, `C` oder `R2` bis `R100`. |
| **Diversity** | Diversity für das aktive Slice ein-/ausschalten. |
| **DAX channel** | Off oder Kanal 1–8. |
| **Tune lock** | Frequenzabstimmung des aktiven Slice sperren/freigeben. |

### Transmit

| Eintrag | Wirkung und Werte |
| --- | --- |
| **RF power** | Sendeleistung 0–100. |
| **Tune power** | TUNE-Leistung 0–100. Dieser Eintrag stellt nur den Leistungswert ein und startet kein TUNE. |
| **Mic gain** | Mikrofonverstärkung 0–100. |
| **Compander** | Ein/Aus und Pegel 0–100. |
| **Monitor** | Sendemonitor ein/aus und Pegel 0–100. |
| **TX antenna** | Sendeantenne aus der vom Radio gelieferten Liste wählen. |
| **XIT** | Ein/Aus und −9990 bis +9990 Hz in 10-Hz-Schritten. |

### Nur bei CW

| Eintrag | Wirkung und Werte |
| --- | --- |
| **CW speed** | 5–100 WPM in Einerschritten. |
| **CW pitch** | 100–6000 Hz in 10-Hz-Schritten. |
| **Break-in** | CW Break-in ein-/ausschalten. |

## 10. Spektrumanzeige

Wenn AetherSDR die ausgehandelte Spektrum-Erweiterung liefert, zeigt die Mitte
ein 32-Balken-Audiospektrum mit weißer Spitzenwertanzeige. Das RX-Spektrum
stellt das empfangene Audiosignal nach DSP, Rauschminderung und RX-Kette bis
einschließlich Equalizer dar. Im Sendebetrieb wird stattdessen das TX-Audio rot
über der TX-Filterbreite dargestellt.

Im Empfang reicht die Frequenzachse von 0 Hz bis zur Filterbreite des aktiven
Slice, höchstens jedoch 12 kHz. Die Balken sind logarithmisch über die Frequenz
verteilt; der untere nutzbare Rand liegt ungefähr bei einem Sechzigstel der
Spanne. Die Achsenbeschriftung passt sich an. Die Balkenhöhe entspricht einem
dB-Wert. Die Spitzenwerte sinken schrittweise ab.

- Spektrum antippen: Kacheln anzeigen.
- Seitlich wischen: zwischen Spektrum und Kacheln wechseln.
- Werden die Kacheln 8 Sekunden nicht benutzt und liegt ein stabiles Spektrum
  vor, erscheint das Spektrum wieder. Solange eine Kachel dem Drehgeber
  zugeordnet ist, erfolgt kein automatischer Rücksprung.
- Nach 5 Sekunden ohne neuen Spektrumrahmen wechselt die Anzeige zu den
  Kacheln. Ein neuer Datenstrom muss 1,5 Sekunden stabil sein, bevor
  automatisch zurückgeschaltet wird.
- Liefert AetherSDR keine Erweiterungsdaten, bleiben die Kacheln sichtbar.

Spektrumerzeugung und -auswertung sind implementiert und offline getestet. Der
reale Datenweg über USB/CTR2 ist noch nicht auf Hardware verifiziert. Ein
klassisches CTR2 liefert diese proprietäre Erweiterung nicht.

## 11. Verhalten beim Senden

Jede dargestellte Slice-Zeile besitzt eine **TX**-Marke:

| Darstellung | Bedeutung |
| --- | --- |
| Grau umrandet | Dieses Slice ist nicht das Sendeslice. Antippen wählt es als TX-Slice. |
| Rot umrandet | Dieses Slice ist als Sendeslice gewählt, sendet aber gerade nicht. |
| Rot gefüllt, weiße Schrift | Das Radio meldet Sendebetrieb auf diesem TX-Slice. |

Nur ein zur gebundenen GUI-Station gehörendes, vorhandenes Slice kann über die
Anzeige als TX-Slice gesetzt werden. Die TX-Anzeige meldet einen Zustand; sie
ist kein PTT-Taster.

**Das Menü tastet den Sender nicht.** Es enthält weder einen VOX-Schalter noch
einen Befehl zum Starten von TUNE. Der Menüpunkt **Tune power** verändert nur
den für TUNE vorgesehenen Leistungswert. Sendebetrieb muss weiterhin über die
dafür vorgesehene PTT-, VOX- oder TUNE-Bedienung außerhalb dieses Menüs
ausgelöst werden.

## 12. Statusanzeigen und typische Zustände

| Zustand | Erkennung | Maßnahme |
| --- | --- | --- |
| Kein USB-Host | Hinweis `Plug into the PC running AetherSDR` | USB-Kabel und PC prüfen. |
| Warten auf AetherSDR | `Waiting for AetherSDR` | CTR2 Proxy auf USB/AetherKnob stellen und starten. |
| Radio, aber keine Station | `Radio connected … Waiting for a … station` | In AetherSDR/SmartSDR eine GUI-Station verbinden beziehungsweise auswählen. |
| Verbunden | Statusfenster verschwindet, Rundanzeige erscheint | Gerät ist betriebsbereit. |
| Gesperrt | `LOCKED` in Gelb | Drehknopf lange drücken oder **Tune lock** im Menü ausschalten. |
| Senden | TX-Marke rot gefüllt; Spektrumbalken rot, falls TX-Spektrum vorhanden | Reine Statusanzeige, keine Sendertastung. |
| Kein Spektrum | Kacheln bleiben sichtbar | Verbindung kann trotzdem vollständig bedienbar sein; Spektrum-Erweiterung prüfen. |

## 13. Fehlerbehebung

### Gerät wird vom PC nicht erkannt

1. Das Kabel am Anschluss **USB-5V-IN** verwenden und eine direkte
   PC-Verbindung testen.
2. Prüfen, ob Display oder Hintergrundbeleuchtung startet. Bleibt alles aus,
   Stromversorgung und Kabel prüfen.
3. **RESET** kurz drücken und die USB-Erkennung erneut abwarten.
4. Wird stattdessen `USB JTAG/serial debug unit` angezeigt, siehe den Abschnitt
   zum Bootloader weiter unten.

### CTR2 Proxy zeigt AetherKnob nicht an

- AetherSDR muss AetherKnob anhand des Produktstrings **AETHER_KNOB**
  unterstützen.
- In CTR2 Proxy **Mode: USB** wählen und die Geräteliste erneut öffnen.
- Andere Programme schließen, die das HID-Gerät exklusiv geöffnet haben
  könnten, USB abziehen, wieder verbinden und CTR2 Proxy neu starten.
- Prüfen, ob das Gerät versehentlich noch als ROM-USB-Seriell/JTAG-Gerät läuft.

### Anzeige bleibt bei „Waiting for AetherSDR“

- CTR2 Proxy öffnen, USB-Modus und AetherKnob wählen, dann **Start** drücken.
- Stop/Start im Proxy ausführen oder AetherKnob einmal sicher neu verbinden.
- Erscheint anschließend `Radio connected`, besteht der USB/CTR2-Weg; dann
  fehlt noch die gebundene AetherSDR-/SmartSDR-GUI-Station.

### Touchrichtung ist falsch

Die Firmware übernimmt die vom Touchcontroller gelieferten X/Y-Koordinaten
derzeit ohne Benutzerkalibrierung oder Drehtransformation. Eine falsche
Orientierung ist eine bekannte, noch offene Hardwareprüfung und kann nicht im
Gerätemenü korrigiert werden. Fehlerbild und tatsächliche Bewegungsrichtungen
notieren, bevor die Firmwarekonfiguration korrigiert wird.

### Drehgeber zählt falsch oder läuft verkehrt

Eine Rastung ist derzeit auf vier Quadraturflanken eingestellt; die
Zählrichtung wird im Boardtreiber invertiert. Beides ist noch nicht
hardwareverifiziert und nicht über das Gerätemenü einstellbar. Prüfen, ob jede
Rastung genau einen Schritt erzeugt und ob Rechtsdrehen Frequenz beziehungsweise
Wert erhöht. Abweichungen sind ein Firmware-/Boardabgleich, kein Funkgerätfehler.

### Gerät bleibt im Bootloader oder im USB-JTAG-/Seriell-Modus

- **BOOT** loslassen und **RESET** einmal kurz drücken.
- Falls nötig: `python -m esptool --port <COM-Port> --after watchdog-reset chip-id`
  ausführen und danach erneut **RESET** drücken.
- Im normalen Betrieb muss das Gerät wieder als **AetherSDR AETHER_KNOB** und
  nicht als `USB JTAG/serial debug unit` erscheinen.

### Spektrum fehlt

- Die Funksteuerung kann trotzdem funktionieren; ohne aktuelle Spektrumdaten
  zeigt das Gerät absichtlich die Kacheln.
- Eine seitliche Wischbewegung kann das Spektrum nur wählen, wenn aktuelle
  Daten vorliegen.
- AetherSDR und CTR2 Proxy müssen die AetherKnob-Spektrum-Erweiterung
  aushandeln. Ein klassisches CTR2 liefert sie nicht.
- Bleibt auch nach einigen Sekunden Verbindung kein Spektrum, die restliche
  Steuerung testen und den noch nicht hardwareverifizierten Erweiterungs-/UDP-
  Datenweg als Fehlerquelle betrachten.

### Keine Funksteuerung

- Statusanzeige unterscheiden: `Waiting for AetherSDR`, `Radio connected` oder
  vollständige Rundanzeige.
- Sicherstellen, dass in AetherSDR eine passende GUI-Station und mindestens ein
  Slice vorhanden sind. AetherKnob steuert nur Slices der gebundenen Station.
- Bei `LOCKED` ist nur die Frequenzabstimmung gesperrt; andere Befehle sollten
  weiterhin möglich sein.
- CTR2 Proxy stoppen, AetherKnob per RESET neu starten beziehungsweise USB
  einmal trennen, danach Proxy erneut auf USB/AetherKnob starten.

### Sicher zurücksetzen und neu verbinden

1. Falls gesendet wird, Sendung über die normale PTT-/VOX-/TUNE-Bedienung
   beenden.
2. CTR2 Proxy stoppen.
3. **RESET** kurz drücken; falls nötig USB trennen und wieder verbinden.
4. Auf `Waiting for AetherSDR` warten.
5. CTR2 Proxy erneut mit USB/AetherKnob starten.

## 14. Firmware aktualisieren / flashen

Voraussetzung ist eine ESP-IDF-Umgebung ab Version 6.0. Der aktuelle
Repository-Stand nennt keine stabile Releaseversion.

1. AetherKnob per USB mit dem PC verbinden.
2. **BOOT** gedrückt halten.
3. **RESET** kurz drücken und loslassen.
4. **BOOT** loslassen. Das ESP32-S3-ROM meldet sich nun als USB-Seriell-/JTAG-
   Gerät und stellt unter Windows einen COM-Port bereit.
5. Den neu erschienenen COM-Port ermitteln.
6. In einer für ESP-IDF eingerichteten Konsole im Projektverzeichnis bauen und
   flashen:

   ```powershell
   idf.py build
   idf.py -p COMx flash
   ```

   `COMx` durch den tatsächlichen Port ersetzen.
7. Nach erfolgreichem Flashen **RESET** kurz drücken.
8. Bis etwa 3 Sekunden auf die erneute USB-Anmeldung warten. Erwartet wird das
   HID-Gerät **AetherSDR AETHER_KNOB** beziehungsweise der Produktname
   **AETHER_KNOB**.

Bleibt das Gerät als `USB JTAG/serial debug unit` sichtbar, war es nach dem
Flashen noch im Downloadmodus. **BOOT** loslassen und **RESET** erneut drücken;
gegebenenfalls den im Fehlerbehebungsabschnitt genannten `esptool`-Befehl
verwenden. Laufzeitprotokolle stehen anschließend nicht am nativen USB-HID,
sondern am UART-Anschluss mit 115200 Baud bereit.

## 15. Bekannte Einschränkungen

- Display-Inbetriebnahme auf dem echten CrowPanel ist im Repository noch nicht
  als verifiziert dokumentiert.
- Touch-Ausrichtung und Gesten sind noch nicht am Zielgerät bestätigt; es gibt
  keine Benutzerkalibrierung im Menü.
- Drehgeberrichtung und vier Zählimpulse pro Rastung sind noch nicht am
  Zielgerät kalibriert.
- Messwerte über den weitergeleiteten UDP-Pfad und damit die reale Meter-
  Aktualisierung sind noch nicht hardwareverifiziert.
- Der Spektrumpfad ist implementiert und offline getestet, die reale
  AetherSDR-/USB-Verbindung dafür aber noch nicht hardwareverifiziert.
- Das Gerät ist auf AetherSDR CTR2 Proxy angewiesen und besitzt keine eigene
  Funkgerät-Netzwerkverbindung.
- Erweiterte NR-/ANF-Varianten NRL, NRS, RNN, NRF, ANFL und ANFT sind für
  FLEX-8000/Aurora vorgesehen; ein FLEX-6000 ignoriert diese Befehle.
- Das Menü tastet den Sender nicht; VOX und das Auslösen von TUNE fehlen
  absichtlich.
- Eine stabile Releaseversion ist im Repository nicht deklariert.

## 16. Kurzreferenz

| Aktion | Ergebnis |
| --- | --- |
| Drehknopf drehen | Frequenz um aktuelle Schrittweite ändern. |
| Drehknopf kurz klicken | Nächste Schrittweite; im Parameter-Modus zurück zur Abstimmung. |
| Drehknopf mindestens 0,6 s halten | Tune lock ein/aus; im Menü zurück beziehungsweise schließen. |
| Kachel antippen | Parameter auf den Drehknopf legen; erneut tippen beendet den Modus. |
| NR/NB/ANF halten | Funktion ein/aus. |
| AF/AGC halten | AGC-Modus weiterschalten. |
| FILT halten | Nächste Abstimmschrittweite. |
| TX-Marke antippen | Dieses Slice als TX-Slice wählen. |
| Nach unten wischen | Menü öffnen. |
| Seitlich wischen | Spektrum/Kacheln wechseln, sofern Spektrum vorhanden. |
| Spektrum antippen | Kacheln anzeigen. |
| Menü nach oben/unten wischen | Liste scrollen. |
| Weißer Menürand | Zeile markiert, Drehknopf navigiert. |
| Gelber Menürand | Zeile wird mit dem Drehknopf bearbeitet. |
| Griff unten antippen/nach oben wischen | Menü schließen. |

## 17. Checkliste für die erste Inbetriebnahme

- [ ] FlexRadio einschalten.
- [ ] AetherSDR starten und mit der gewünschten Station verbinden.
- [ ] AetherKnob über **USB-5V-IN** mit dem PC verbinden.
- [ ] Auf `Waiting for AetherSDR` warten.
- [ ] In AetherSDR **CTR2 Proxy** öffnen.
- [ ] **Mode: USB** wählen.
- [ ] **AetherKnob / AETHER_KNOB** auswählen.
- [ ] **Start** drücken.
- [ ] Warten, bis das Statusfenster verschwindet und die Rundanzeige erscheint.
- [ ] Prüfen, ob oben das gewünschte aktive Slice angezeigt wird.
- [ ] Drehknopf vorsichtig um eine Rastung drehen und Frequenzänderung prüfen.
- [ ] Bei falschem Slice dieses zunächst in AetherSDR aktivieren; die TX-Marke
      nur dann antippen, wenn auch das Sendeslice bewusst geändert werden soll.

