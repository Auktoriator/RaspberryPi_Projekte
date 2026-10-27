# Raspberry Pi 5 Mini-NAS Gehäuse

3D-druckbares Gehäuse im Stil eines kleinen 2-Bay-NAS für einen Raspberry Pi 5 mit M.2 HAT+ und zwei 2,5"-Laufwerken.

**Aktuelle Version: 3**

![Foto des aktuellen Aufbaus](IMG_3338.jpeg)

## Dateien

| Datei | Inhalt |
|---|---|
| `nas_gehaeuse.py` | Bauskript. Alle Maße als Parameter oben. Erzeugt das Modell in FreeCAD komplett neu. |
| `Pi5_NAS_Gehaeuse.FCStd` | Gespeichertes FreeCAD-Modell (Ergebnis des Skripts) |
| `CLAUDE.md` | Arbeitsanweisungen für Claude Code |
| `IMG_3338.jxl` / `.jpeg` | Foto des aktuellen Aufbaus (JPEG für die Anzeige auf GitHub) |

Modell neu erzeugen: In FreeCAD *Makro → Makros…* oder über Claude (FreeCAD-MCP) `nas_gehaeuse.py` ausführen.

## Gehäuse

- **Außenmaß:** 77 × 145 × 99 mm (B × T × H, mit Deckel und Füßen)
- **Innenmaß:** 72 × 140 × 90 mm, Wandstärke 2,5 mm

### Druckteile

| Teil | Beschreibung |
|---|---|
| Gehäuse (Wanne) | Boden, vier Wände, Laufwerksschienen, Auflageleisten für den Pi-Träger, vier Füße |
| Pi-Träger | 3 mm Einlegeplatte mit vier Abstandshaltern (6 mm, Loch für M2.5 selbstschneidend) |
| Deckel | Geschlossene Platte mit umlaufendem Steckrand |

### Aufbau von unten nach oben

1. **Laufwerk 1** liegt auf dem Boden, **Laufwerk 2** auf einer Trennschiene (12 mm Schachthöhe je Laufwerk). Einschub von vorne.
2. Dahinter 40 mm Platz: 20 mm für den USB-SATA-Adapter, 20 mm für den Kabelbogen. Die Kabel gehen durch eine Öffnung in der Rückwand nach außen.
3. **Pi-Träger** liegt auf Leisten bei 30 mm Höhe.
4. **Raspberry Pi 5** auf den Abstandshaltern, USB/Ethernet nach hinten, USB-C/Micro-HDMI nach rechts.
5. **M.2 HAT+** 15,5 mm über der Pi-Platine, SSD mit Kühlkörper knapp 15 mm hoch.
6. Reserve für einen **AI HAT+** darüber, gleicher Abstand (0,5 mm über dem SSD-Kühlkörper, 5 mm Luft bis zum Deckelrand).

### Öffnungen

- **Front:** zwei Laufwerksschächte, darüber senkrechte Lüftungsschlitze
- **Rückseite:** Ausschnitt für 2× USB + Ethernet; Kabel- und Luftöffnung hinter den Laufwerken
- **Rechts:** Ausschnitt für USB-C und 2× Micro-HDMI; Lüftungsschlitze
- **Links:** 40-mm-Lüfteröffnung mit Fingerschutz (Abluft); Lüftungsschlitze im Laufwerksbereich
- **Boden:** Lüftungsschlitze unter den Laufwerken
- **Deckel:** geschlossen (Staubschutz)

### Luftführung

Frischluft kommt durch Boden, Front und rechte Seite herein, strömt über die Laufwerke und den Pi und wird vom Lüfter links oben nach außen geblasen.

## Komponenten

| Komponente | Maße / Daten | Quelle |
|---|---|---|
| Raspberry Pi 5 | Platine 85 × 56 mm, Löcher Ø 2,7 im Raster 58 × 49 mm (3,5 mm vom Rand). Ports an der langen Kante: USB-C 11,2 / HDMI0 25,8 / HDMI1 39,2 mm. An der kurzen Kante: Ethernet 10,2 / USB 29,1 / USB 47 mm. Ports stehen 3 mm über. | [Offizielle Maßzeichnung](https://pip-assets.raspberrypi.com/categories/892-raspberry-pi-5/documents/RP-008347-DS-1-raspberry-pi-5-mechanical-drawing.pdf) |
| Raspberry Pi Active Cooler | unter dem M.2 HAT+ montiert | – |
| M.2 HAT+ (M Key) | 65 × 56,5 mm, 16-mm-Stapelheader. Gemessen: 15,5 mm über der Pi-Platine. SSD 2242 mit Metall-Kühlkörper, knapp 15 mm über dem HAT. | [Product Brief](https://cdn.sparkfun.com/assets/4/0/7/e/8/Raspberry_Pi_M.2-HAT_Product_Brief_v9.pdf) |
| AI HAT+ 2 (geplant) | Hailo-10H, 40 TOPS, 8 GB RAM. Platine 65 × 56,5 mm, 16-mm-Stapelheader. Kühlkörper (wird montiert) 42,5 × 64 mm, Push-Pins, ca. 14 mm hoch. Betrieb bis 50 °C Umgebung. | `RP-009655-MM-6-raspberry-pi-ai-hat-plus-2-product-brief.pdf` |
| 2× 2,5"-Laufwerk | 69,85 × 100 mm, max. 9,5 mm hoch | SFF-8201 |
| 2× USB-SATA-Adapter | siehe [Laufwerke und Adapter](#laufwerke-und-adapter) | – |
| Gehäuselüfter | 40 × 40 × 10 mm, 5 V (z. B. Noctua NF-A4x10 5V), M3-Schrauben, Lochabstand 32 mm | – |

## Laufwerke und Adapter

| Schacht | Laufwerk | Anschluss |
|---|---|---|
| 1 (unten) | 2,5"-HDD (vorhanden) | USB 3.0 (blau) |
| 2 (oben) | 2,5"-SATA-SSD (neu) | USB 3.0 (blau) |

**Adapter:** 2× [„SSD to USB 3.0 Cable for Raspberry Pi“ (The Pi Hut)](https://thepihut.com/products/ssd-to-usb-3-0-cable-for-raspberry-pi)

- Chip ASMedia ASM1153E / ASM225, unterstützt UASP (schneller USB-Modus); vom Händler mit dem Pi 5 getestet.
- Kabeladapter: Der Stecker sitzt direkt am Laufwerk, das Kabel führt durch die Rückwand zu den USB-3.0-Ports.
- Stromaufnahme laut Händler 0,2–0,3 A mit SSD. Eine HDD zieht beim Anlaufen deutlich mehr; HDD + SSD zusammen sollten unter dem USB-Limit des Pi 5 bleiben (1,6 A mit 27-W-Netzteil).
- Platz im Gehäuse: Laufwerk + Adapter höchstens 120 mm lang, dahinter 20 mm für den Kabelbogen.

## PCIe: M.2 HAT+ und AI HAT+ 2

Der Pi 5 hat **genau einen PCIe-Anschluss** (1 Lane, PCIe 2.0 offiziell). M.2 HAT+ und AI HAT+ 2 brauchen beide diesen Anschluss. Beim AI HAT+ 2 ist der Hailo-Chip fest aufgelötet; er lässt sich also nicht als M.2-Modul in einen anderen Steckplatz stecken.

### Variante A: AI HAT+ 2 direkt, System auf der SATA-SSD (empfohlen)

1. Raspberry Pi OS auf die neue SATA-SSD in Schacht 2 übertragen und Boot-Reihenfolge auf USB stellen (`sudo raspi-config` → *Advanced Options* → *Boot Order* → *USB Boot*).
2. M.2 HAT+ mit der 2242-NVMe ausbauen.
3. AI HAT+ 2 mit Kühlkörper an seiner Stelle montieren: 16-mm-Stapelheader, Abstandshalter und Schrauben liegen bei; der Pi Active Cooler bleibt darunter.
4. Flachbandkabel des AI HAT+ 2 an den PCIe-Anschluss des Pi stecken.

Zusätzliche Bauteile: **keine.** Das ist der offiziell unterstützte Aufbau. Der AI HAT+ 2 bekommt die volle PCIe-Bandbreite. Die SATA-SSD über USB 3.0 ist für System und Minecraft-Server schnell genug.

### Variante B: beide gleichzeitig über einen PCIe-Switch (nicht empfohlen)

Zusätzliches Bauteil: ein **PCIe-Switch** mit zwei Flachbandausgängen, z. B. **Pineboards HatBRICK! Commander** (ASMedia-Switch, PCIe 2.0, 2 Ausgänge).

Aufbau: Pi-PCIe-Anschluss → Commander → je ein Flachbandkabel zum M.2 HAT+ und zum AI HAT+ 2. Booten von einer NVMe hinter einem Switch unterstützt die Pi-Firmware seit Mai 2024.

Warum nicht empfohlen:
- Der PCIe-Anschluss des Pi liefert höchstens 1 A (5 W) für Switch, SSD und AI HAT+ 2 zusammen.
- Beide Geräte teilen sich eine Lane: jedes bekommt höchstens die halbe Bandbreite, dazu kommt Latenz durch den Switch.
- Es gibt keinen bestätigt funktionierenden Aufbau mit dem AI HAT+ 2. Ein Nutzer hat genau diese Kombination (Commander + NVMe-HAT + AI HAT+ 2) im Januar 2026 versucht; es lief immer nur eins von beiden, am Ende war die SSD defekt ([Forum](https://forums.raspberrypi.com/viewtopic.php?t=395552)).
- Mit dem älteren AI Kit (Hailo-8L) lief eine Kombination mit dem Pimoroni NVMe Base Duo ([Forum](https://forums.raspberrypi.com/viewtopic.php?t=371991)), das ist aber ein anderes Produkt.
- Mechanisch wird der Stapel aus drei Platinen plus Switch deutlich höher.

### Lüfter anschließen

Der Lüfteranschluss des Pi ist vom Active Cooler belegt. Den Gehäuselüfter deshalb an die GPIO-Pins anschließen: **Pin 4 = 5 V, Pin 6 = GND**. Er läuft dann immer mit voller Drehzahl.

### Strom

Offizielles 27-W-Netzteil (5 V / 5 A) verwenden. Damit liefern die USB-Ports zusammen 1,6 A. Zwei 2,5"-HDDs können beim Anlaufen zusammen mehr ziehen. Sicher sind eine HDD plus eine SATA-SSD, oder ein Adapter mit eigener Stromversorgung.

## Druck

- **Material:** PETG (wegen der warmen Abluft am Lüfter)
- Keine Stützen nötig: Überhänge haben 45°-Fasen.
- Steckpassungen haben 0,3 mm Spiel.
- Ausrichtung: Wanne aufrecht (Boden aufs Druckbett), Pi-Träger flach, Deckel mit der Außenseite aufs Druckbett.

## Schrauben

- 4× M2.5 × 6 (Pi auf Träger)
- 4× M3 × 16 + Muttern (Lüfter)

## Offene Aufgaben

### MUST

- **Modell auf Variante A umstellen:** M.2 HAT+ durch AI HAT+ 2 mit Kühlkörper (ca. 14 mm hoch) ersetzen und den Platz darüber neu prüfen.
- **Laufwerke sichern:** Die Laufwerke liegen lose in den Schächten. Sie brauchen einen Anschlag hinten oder eine Klemme vorne, sonst rutschen sie beim Kabelziehen.
- **Deckel befestigen:** Der Deckel liegt nur lose auf. Er braucht Clips oder Schrauben.
- **Probedruck:** Ein kleines Teststück mit Pi-Lochbild, Port-Ausschnitt und Schiene drucken, um Passung und Toleranzen zu prüfen, bevor das ganze Gehäuse gedruckt wird.
- **STL-Dateien exportieren** (Wanne, Pi-Träger, Deckel).

### SHOULD

- **Temperatur des AI HAT+ 2 prüfen:** Der Hersteller schreibt, das Gehäuse soll nicht abgedeckt sein. Der Deckel ist geschlossen; der Lüfter muss die Wärme vom Kühlkörper abführen. Eventuell Lüftungsschlitze im Deckel direkt über dem Kühlkörper.
- **Power-Knopf** von außen erreichbar machen (Loch mit Stößel).
- **Zugentlastung** für die USB-Kabel an der Rückwand.
- **Status-LEDs** des Pi sichtbar machen (Lichtleiter oder kleines Fenster).

### COULD

- Herausziehbare Laufwerksschlitten mit Griff an der Front, wie bei einer Synology.
- Gewindeeinsätze aus Messing statt selbstschneidender Schrauben.
- Staubfilter vor den Ansaugschlitzen.
- Lüfter über einen Transistor temperaturabhängig steuern statt Dauerbetrieb.
- Gestaltung der Front (Fasen, Logo, Beschriftung der Schächte).
- Zugang zur microSD (mit USB-Boot kaum noch nötig).

### WONT (in dieser Ausbaustufe)

- M.2 HAT+ und AI HAT+ 2 gleichzeitig über einen PCIe-Switch (siehe Variante B).
- SATA-HATs über PCIe (z. B. Radxa Penta, Waveshare 2-Ch): PCIe ist vom AI HAT+ 2 belegt.
- 15-mm-Laufwerke, 3,5"-Laufwerke, mehr als zwei Laufwerke.
