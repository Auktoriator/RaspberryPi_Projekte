# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Projekt

3D-druckbares Mini-NAS-Gehäuse für einen Raspberry Pi 5 (mit M.2 HAT+, optional AI HAT+) und zwei 2,5"-Laufwerken. Der Nutzer ist CAD-Anfänger: auf Deutsch antworten, CAD-Begriffe kurz erklären.

## Arbeitsweise

- **`nas_gehaeuse.py` ist die einzige Quelle der Wahrheit.** Das Skript baut das FreeCAD-Dokument „Projekt“ bei jedem Lauf komplett neu (löscht alle Objekte). `Pi5_NAS_Gehaeuse.FCStd` ist nur das gespeicherte Ergebnis – nie direkt in FreeCAD editieren, sonst geht die Änderung beim nächsten Lauf verloren.
- **Bauen:** FreeCAD-MCP `execute_python_file` mit dem absoluten Pfad zu `nas_gehaeuse.py`, danach `App.getDocument("Projekt").saveAs(".../Pi5_NAS_Gehaeuse.FCStd")`.
- **Selbsttest:** Das Skript prüft am Ende jedes Druckteil auf `isValid()` und auf Volumen-Überschneidung mit allen Referenzteilen und druckt `Kollisionen: keine`. Jede Änderung muss das weiterhin ausgeben. Neue Bauteile (Lüfter, HATs, Laufwerke …) als Eintrag in `refs` anlegen, dann sind sie automatisch im Test.
- **Sichtprüfung:** `Gui.activeDocument().activeView().saveImage(pfad, 900, 700, "White")` und das Bild ansehen, bevor man „fertig“ meldet.
- **Version:** Bei einer neuen Version die Kopfzeile im Skript (`Version N` + eine Zeile, was neu ist) anpassen.
- **`README.md`** beschreibt immer nur den *aktuellen* Stand (kein Changelog, keine „geändert von X auf Y“). Nach jeder Modelländerung die betroffenen Abschnitte überschreiben, inkl. Außenmaß und offener Punkte.

## Modell-Architektur (`nas_gehaeuse.py`)

- Koordinaten: X = Breite (links→rechts), Y = Tiefe (vorne→hinten), Z = Höhe; Ursprung = innere vordere linke untere Gehäuseecke. Innenmaß `W × D × H`, Wand `T`.
- Alle Maße stehen als Parameter oben. Der Pi wird über `pi(px, py)` platziert: Pi-Koordinaten aus der offiziellen Maßzeichnung (px entlang 85 mm, py entlang 56 mm, py=0 = HDMI-Kante) → Gehäuse-X/Y. Die Abbildung ist eine Drehung, keine Spiegelung – Portpositionen immer über `pi()`/`pi_box()` angeben.
- Z-Aufbau von unten: zwei Laufwerksschächte (`SLOT_H`, Trennschiene `RAIL`) → Pi-Träger auf Leisten bei `TRAY_Z` → Pi auf Abstandshaltern → M.2 HAT (`HAT_GAP`) → Reserve für AI HAT → Deckel.
- Drei Druckteile (Gruppe „Druckteile“): `Gehaeuse` (Wanne), `Pi_Traeger` (Einlegeplatte), `Deckel`. Alles in „Referenz_nicht_drucken“ sind Platzhalter-Quader nur für Kollisionstest und Optik.
- Reine Part-CSG (`box`, `cut_all`, `fuse`), kein PartDesign/Spreadsheet.

## Druckregeln

- Überhänge nur mit 45°-Fase (siehe `wall_rail`), keine Stützen nötig machen.
- Steckpassungen mit `FIT` = 0,3 mm Spiel.
- Material PETG (Abluft des Lüfters ist warm).
