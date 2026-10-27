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
| AI HAT+ (optional) | gleiche Grundfläche wie M.2 HAT+ | [Raspberry Pi Doku](https://raspberrypi.com/documentation/accessories/ai-kit.html) |
| 2× 2,5"-Laufwerk | 69,85 × 100 mm, max. 9,5 mm hoch | SFF-8201 |
| 2× USB-SATA-Adapter | Kabeladapter mit ASMedia-Chip (ASM1153E), UASP-fähig, max. 20 mm hinter dem Laufwerk (Laufwerk + Adapter ≤ 120 mm) | [The Pi Hut: SSD to USB 3.0 Cable](https://thepihut.com/products/ssd-to-usb-3-0-cable-for-raspberry-pi) |
| Gehäuselüfter | 40 × 40 × 10 mm, 5 V (z. B. Noctua NF-A4x10 5V), M3-Schrauben, Lochabstand 32 mm | – |

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

## Offene Punkte

- **AI HAT+ und M.2 HAT+ gleichzeitig:** Beide nutzen den einzigen PCIe-Anschluss des Pi 5. Für beide zusammen ist ein PCIe-Verteiler nötig.
- Power-Knopf und microSD sind nur bei abgenommenem Deckel erreichbar.
- Kein Anschlag für die Laufwerke; sie werden nur durch das Kabel gestoppt.
- SATA-HATs über PCIe (z. B. Radxa Penta, Waveshare 2-Ch) sind keine Option, solange der M.2 HAT+ den PCIe-Anschluss belegt.
- 15-mm-Laufwerke passen nicht.
- STL-Dateien sind noch nicht exportiert.
