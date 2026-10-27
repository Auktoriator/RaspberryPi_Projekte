# Raspberry Pi 5 Mini-NAS Gehäuse, Version 4
# V4: Laufwerke verschraubt, Deckel verschraubt, Power-Stößel, Zugentlastung, Staubfilter vorne
# In FreeCAD ausführen: baut das Dokument "Projekt" komplett neu auf.
# Koordinaten: X = Breite (links->rechts), Y = Tiefe (vorne->hinten), Z = Höhe.
# Ursprung = innere vordere linke untere Ecke des Gehäuses. Alle Maße in mm.
import FreeCAD as App
import Part
from FreeCAD import Vector as V

# ---------- Parameter ----------
T = 2.5            # Wandstärke
W, D, H = 72, 140, 90   # Innenmaße Breite, Tiefe, Höhe
FIT = 0.3          # Spiel für Teile, die ineinander gesteckt werden

DRV_W, DRV_L, DRV_H = 69.85, 100.0, 9.5   # 2,5"-Laufwerk (SFF-8201), max. 9,5 mm hoch
ADAPTER_L = 20     # USB-SATA-Adapter hinter dem Laufwerk (gemessen: HDD + Adapter = 120 mm); dahinter Platz für den Kabelbogen
SLOT_H = 12        # Höhe eines Laufwerksschachts
RAIL = 2           # Dicke der Trennschiene zwischen den Schächten
RAIL_W = 4         # wie weit Schienen/Leisten aus der Wand ragen

TRAY_Z, TRAY_T = 30, 3   # Pi-Träger: Unterkante, Dicke
STANDOFF_H = 6
PCB_T = 1.6
HAT_GAP = 15.5     # Pi-Oberseite bis HAT-Unterseite (gemessen: etwas über 15 mm)
SSD_STACK = 15     # SSD + Kühlkörper über der HAT-Oberseite (gemessen: knapp 15 mm)

# Abluftlüfter 40x40x10 (z. B. Noctua NF-A4x10 5V), innen an der linken Wand, bläst nach außen
FAN, FAN_T, FAN_PITCH = 40, 10, 32   # Kantenlänge, Dicke, Lochabstand
FAN_Y, FAN_Z = D - 40, 64               # Mittelpunkt in der linken Wand (über dem Pi)

# Laufwerks-Seitenlöcher (M3, 3 mm über Unterkante). Je nach Hersteller 9,6/86,2 oder 14,0/90,6 mm
# von der Front -> Langlöcher decken beide ab.
DRV_HOLE_Z = 3.0
DRV_HOLE_Y = ((9.6, 14.0), (86.2, 90.6))

LID_BOSS_Y = (15, D - 15)   # Schraubdome für den Deckel (je links und rechts)
LID_BOSS_W = 8

FILTER_Z0, FILTER_Z1 = 47, 84.5   # Filterrahmen hinter den Front-Lüftungsschlitzen
FILTER_T = 1.4                    # Rahmendicke; Filtervlies (ca. 1 mm) liegt zwischen Wand und Rahmen

# Pi 5 laut offizieller Zeichnung (px entlang 85 mm, py entlang 56 mm, py=0 = HDMI-Kante)
PI_Y0 = D + T - 88            # Pi px=0 so, dass die Ports (3 mm Überstand) bündig mit der Rückwand abschließen
PI_X0 = W - 2                 # py=0 (HDMI-Kante) liegt 2 mm vor der rechten Wand
def pi(px, py):              # Pi-Koordinate -> Gehäuse (X, Y); gedreht, nicht gespiegelt
    return PI_X0 - py, PI_Y0 + px
PCB_Z = TRAY_Z + TRAY_T + STANDOFF_H     # Unterseite Pi-Platine
PCB_TOP = PCB_Z + PCB_T
BTN_X, BTN_Y = pi(-0.45, 18.4)            # Power-Knopf an der vorderen Pi-Kante (steht 0,45 mm über)
BTN_Z = PCB_TOP + 1.5                     # geschätzte Mitte des Knopfes

def box(x0, y0, z0, x1, y1, z1):
    x0, x1 = min(x0, x1), max(x0, x1)
    y0, y1 = min(y0, y1), max(y0, y1)
    z0, z1 = min(z0, z1), max(z0, z1)
    return Part.makeBox(x1 - x0, y1 - y0, z1 - z0, V(x0, y0, z0))

def wall_rail(z_top, right=False):
    # Leiste mit 45°-Fase unten -> ohne Stützmaterial druckbar
    s = -1 if right else 1
    x = W if right else 0
    pts = [(0, z_top), (RAIL_W, z_top), (RAIL_W, z_top - 1), (0, z_top - 1 - RAIL_W)]
    wire = Part.makePolygon([V(x + s * a, 0, b) for a, b in pts] + [V(x, 0, z_top)])
    return Part.Face(wire).extrude(V(0, D, 0))

def cut_all(shape, cutters):
    return shape.cut(Part.makeCompound(cutters)) if cutters else shape

def slot_x(x0, x1, y0, y1, zc, r):
    # Langloch in X-Richtung durch eine Seitenwand, Y von y0 bis y1
    d = V(x1 - x0, 0, 0)
    return (box(x0, y0, zc - r, x1, y1, zc + r)
            .fuse(Part.makeCylinder(r, x1 - x0, V(x0, y0, zc), d))
            .fuse(Part.makeCylinder(r, x1 - x0, V(x0, y1, zc), d)))

def boss(x_wall, yc, z_top, right=False):
    # Schraubdom an der Wand, unten 45° angefast; ca. 9 mm Gewindetiefe in der Lochmitte
    s = -1 if right else 1
    pts = [(0, z_top), (LID_BOSS_W, z_top), (LID_BOSS_W, z_top - 6), (0, z_top - 6 - LID_BOSS_W)]
    wire = Part.makePolygon([V(x_wall + s * a, yc - LID_BOSS_W / 2, b) for a, b in pts] + [V(x_wall, yc - LID_BOSS_W / 2, z_top)])
    return Part.Face(wire).extrude(V(0, LID_BOSS_W, 0))

# ---------- Gehäuse (Wanne) ----------
tub = box(-T, -T, -T, W + T, D + T, H).cut(box(0, 0, 0, W, D, H + 1))
cuts = []
# vorne: zwei Laufwerksschächte
mx = (W - (DRV_W + 1.2)) / 2
cuts.append(box(mx, -T - 1, 0, W - mx, 1, SLOT_H))
cuts.append(box(mx, -T - 1, SLOT_H + RAIL, W - mx, 1, 2 * SLOT_H + RAIL))
# vorne: Lüftungsschlitze oberhalb der Schächte (hinter dem Staubfilter)
for x in range(10, W - 12, 6):
    cuts.append(box(x, -T - 1, FILTER_Z0 + 4, x + 3, 1, FILTER_Z1 - 4.5))
# vorne: Durchführung für den Power-Stößel
cuts.append(box(BTN_X - 2.3, -T - 1, BTN_Z - 2.3, BTN_X + 2.3, 1, BTN_Z + 2.3))
# hinten: Öffnung für Pi-Anschlüsse (USB, USB, Ethernet)
x_a, _ = pi(0, 1); x_b, _ = pi(0, 55)
cuts.append(box(x_a, D - 1, PCB_TOP - 1, x_b, D + T + 1, PCB_TOP + 17))
# hinten: Kabeldurchlass für beide Laufwerkskabel (USB-A-Stecker passt durch)
CABLE_X0, CABLE_X1 = W / 2 - 11, W / 2 + 11
cuts.append(box(CABLE_X0, D - 1, 0.5, CABLE_X1, D + T + 1, 13))
# rechts: USB-C + 2x Micro-HDMI
_, y_a = pi(2, 0); _, y_b = pi(48, 0)
cuts.append(box(W - 1, y_a, PCB_Z - 1.5, W + T + 1, y_b, PCB_TOP + 11))
# links: Langlöcher für die Laufwerksschrauben (M3 x 5)
for z0 in (0, SLOT_H + RAIL):
    for ya, yb in DRV_HOLE_Y:
        cuts.append(slot_x(-T - 1, 0.5, ya, yb, z0 + DRV_HOLE_Z, 1.7))
# links: Lüfteröffnung + 4 Schraublöcher (M3)
cuts.append(Part.makeCylinder(FAN / 2 - 1, T + 2, V(-T - 1, FAN_Y, FAN_Z), V(1, 0, 0)))
for dy in (-FAN_PITCH / 2, FAN_PITCH / 2):
    for dz in (-FAN_PITCH / 2, FAN_PITCH / 2):
        cuts.append(Part.makeCylinder(1.7, T + 2, V(-T - 1, FAN_Y + dy, FAN_Z + dz), V(1, 0, 0)))
tub = cut_all(tub, cuts)
# Fingerschutz: zwei waagerechte Stege durch die Lüfteröffnung
for dz in (-7, 7):
    tub = tub.fuse(box(-T, FAN_Y - FAN / 2, FAN_Z + dz - 1, 0, FAN_Y + FAN / 2, FAN_Z + dz + 1))
# Schienen: Trennung der Schächte und Auflage für den Pi-Träger
for zt in (SLOT_H + RAIL, TRAY_Z):
    tub = tub.fuse(wall_rail(zt)).fuse(wall_rail(zt, right=True))
# Schraubdome für den Deckel
for yc in LID_BOSS_Y:
    tub = tub.fuse(boss(0, yc, H - 4.5)).fuse(boss(W, yc, H - 4.5, right=True))
tub = cut_all(tub, [Part.makeCylinder(1.25, 10, V(x, yc, H - 14.5)) for x in (LID_BOSS_W / 2 + 0.5, W - LID_BOSS_W / 2 - 0.5) for yc in LID_BOSS_Y])
# Zugentlastung: Kabelbinder-Brücke auf dem Boden vor dem Kabeldurchlass
tub = tub.fuse(cut_all(box(CABLE_X0 + 2, D - 14, 0, CABLE_X1 - 2, D - 8, 5), [box(CABLE_X0, D - 12.5, -1, CABLE_X1, D - 9.5, 2.5)]))
# Staubfilter: zwei senkrechte Führungsnuten innen an der Front, Rahmen wird von oben eingeschoben
for xa, xb, xc, xd in ((2, 8, 4, 9), (W - 8, W - 2, W - 9, W - 4)):
    tub = tub.fuse(box(xa, 0, FILTER_Z0 - 1, xb, 5, FILTER_Z1 + 0.5).cut(box(xc, -1, FILTER_Z0, xd, FILTER_T + 1.3, H)))
# Füße (Luftspalt unter dem Gehäuse)
for fx, fy in ((-T, -T), (W + T - 10, -T), (-T, D + T - 10), (W + T - 10, D + T - 10)):
    tub = tub.fuse(box(fx, fy, -T - 4, fx + 10, fy + 10, -T))
tub = tub.removeSplitter()

# ---------- Pi-Träger (Einlegeplatte) ----------
tray = box(FIT, FIT, TRAY_Z, W - FIT, D - FIT, TRAY_Z + TRAY_T)
holes = [pi(px, py) for px in (3.5, 61.5) for py in (3.5, 52.5)]
slots = []
for y in range(8, int(D) - 8, 7):
    if all(abs(y + 1.5 - hy) > 6 for _, hy in holes):
        slots.append(box(10, y, TRAY_Z - 1, W - 10, y + 3, TRAY_Z + TRAY_T + 1))
tray = cut_all(tray, slots)
for hx, hy in holes:
    tray = tray.fuse(Part.makeCylinder(3, STANDOFF_H, V(hx, hy, TRAY_Z + TRAY_T)))
tray = cut_all(tray, [Part.makeCylinder(1.25, 20, V(hx, hy, TRAY_Z - 1)) for hx, hy in holes])  # M2.5 selbstschneidend
for gy in (14, 40):   # U-Führungen für den Power-Stößel (oben offen, Stößel wird eingelegt)
    tray = tray.fuse(box(BTN_X - 4.2, gy, TRAY_Z + TRAY_T, BTN_X + 4.2, gy + 4, BTN_Z + 2)
                     .cut(box(BTN_X - 2.2, gy - 1, BTN_Z - 2.1, BTN_X + 2.2, gy + 5, BTN_Z + 10)))
tray = tray.removeSplitter()

# ---------- Power-Stößel ----------
# 4x4-Stab von außen (1,5 mm überstehend) bis 0,5 mm vor den Knopf; Bund innen verhindert Herausfallen
rod = box(BTN_X - 2, -T - 1.5, BTN_Z - 2, BTN_X + 2, BTN_Y - 0.5, BTN_Z + 2)
rod = rod.fuse(box(BTN_X - 3.5, 0.5, BTN_Z - 3.5, BTN_X + 3.5, 2.5, BTN_Z + 3.5)).removeSplitter()

# ---------- Filterrahmen ----------
fx0, fx1 = 4 + FIT, W - 4 - FIT
filt = box(fx0, 0.1, FILTER_Z0 + 0.2, fx1, 0.1 + FILTER_T, FILTER_Z1)
filt = filt.cut(box(fx0 + 3, -1, FILTER_Z0 + 3.2, fx1 - 3, 3, FILTER_Z1 - 3))
filt = filt.fuse(box((fx0 + fx1) / 2 - 1, 0.1, FILTER_Z0, (fx0 + fx1) / 2 + 1, 0.1 + FILTER_T, FILTER_Z1)).removeSplitter()

# ---------- Deckel ----------
lid = box(-T, -T, H, W + T, D + T, H + T)
lip = box(FIT, FIT, H - 4, W - FIT, D - FIT, H).cut(box(FIT + 2, FIT + 2, H - 5, W - FIT - 2, D - FIT - 2, H + 1))
lid = lid.fuse(lip)   # geschlossen: kein Staub von oben
lid = cut_all(lid, [Part.makeCylinder(1.7, T + 2, V(x, yc, H - 1)) for x in (LID_BOSS_W / 2 + 0.5, W - LID_BOSS_W / 2 - 0.5) for yc in LID_BOSS_Y]).removeSplitter()

# ---------- Referenzteile (nicht drucken) ----------
def pi_box(px0, py0, px1, py1, z0, z1):
    xa, ya = pi(px0, py0); xb, yb = pi(px1, py1)
    return box(xa, ya, z0, xb, yb, z1)
refs = {
    "Pi5_Platine": pi_box(0, 0, 85, 56, PCB_Z, PCB_TOP),
    "Pi5_Ethernet": pi_box(66, 2.2, 88, 18.2, PCB_TOP, PCB_TOP + 13.5),
    "Pi5_USB_1": pi_box(70, 21.8, 88, 36.4, PCB_TOP, PCB_TOP + 16),
    "Pi5_USB_2": pi_box(70, 39.7, 88, 54.3, PCB_TOP, PCB_TOP + 16),
    "Pi5_USB_C": pi_box(7, -1, 15.4, 7, PCB_TOP, PCB_TOP + 3.2),
    "Pi5_HDMI_0": pi_box(22.3, -1, 29.3, 7, PCB_TOP, PCB_TOP + 3.4),
    "Pi5_HDMI_1": pi_box(35.7, -1, 42.7, 7, PCB_TOP, PCB_TOP + 3.4),
    "Pi5_Aktivkuehler": pi_box(25, 12, 60, 45, PCB_TOP, PCB_TOP + 9),
    "M2_HAT": pi_box(0, 0, 65, 56.5, PCB_TOP + HAT_GAP, PCB_TOP + HAT_GAP + 1.6),
    "M2_SSD_mit_Kuehler": pi_box(10, 18, 52, 40, PCB_TOP + HAT_GAP + 1.6, PCB_TOP + HAT_GAP + 1.6 + SSD_STACK),
    "Pi5_Powerknopf": pi_box(-0.45, 16.9, 1.5, 19.9, PCB_TOP, PCB_TOP + 3),
    "Luefter_40mm": box(0, FAN_Y - FAN / 2, FAN_Z - FAN / 2, FAN_T, FAN_Y + FAN / 2, FAN_Z + FAN / 2),
    "Adapter_1": box((W - DRV_W) / 2, DRV_L, 0, (W + DRV_W) / 2, DRV_L + ADAPTER_L, DRV_H),
    "Adapter_2": box((W - DRV_W) / 2, DRV_L, SLOT_H + RAIL, (W + DRV_W) / 2, DRV_L + ADAPTER_L, SLOT_H + RAIL + DRV_H),
    "HDD_1": box((W - DRV_W) / 2, 0, 0, (W + DRV_W) / 2, DRV_L, DRV_H),
    "HDD_2": box((W - DRV_W) / 2, 0, SLOT_H + RAIL, (W + DRV_W) / 2, DRV_L, SLOT_H + RAIL + DRV_H),
}

# ---------- Dokument aufbauen ----------
doc = App.getDocument("Projekt") if "Projekt" in App.listDocuments() else App.newDocument("Projekt")
while doc.Objects:
    for o in list(doc.Objects):
        try:
            doc.removeObject(o.Name)
        except Exception:
            pass

def add(name, shape, color, transp=0, group=None):
    o = doc.addObject("Part::Feature", name)
    o.Shape = shape
    if App.GuiUp:
        o.ViewObject.ShapeColor = color
        o.ViewObject.Transparency = transp
    if group:
        group.addObject(o)
    return o

drucken = doc.addObject("App::DocumentObjectGroup", "Druckteile")
referenz = doc.addObject("App::DocumentObjectGroup", "Referenz_nicht_drucken")
add("Gehaeuse", tub, (0.85, 0.85, 0.88), 55, drucken)
add("Pi_Traeger", tray, (0.95, 0.55, 0.15), 0, drucken)
add("Deckel", lid, (0.35, 0.55, 0.85), 75, drucken)
add("Power_Stoessel", rod, (0.9, 0.2, 0.2), 0, drucken)
add("Filterrahmen", filt, (0.95, 0.85, 0.2), 0, drucken)
for n, s in refs.items():
    col = (0.2, 0.6, 0.3) if n.startswith(("Pi5_Plat", "M2_HAT")) else (0.3, 0.3, 0.3)
    if n.startswith("HDD"):
        col = (0.6, 0.6, 0.65)
    add(n, s, col, 0, referenz)
doc.recompute()

# ---------- Selbsttest: keine Überschneidungen ----------
problems = []
parts = ("Gehaeuse", "Pi_Traeger", "Deckel", "Power_Stoessel", "Filterrahmen")
for i, part in enumerate(parts):
    ps = doc.getObject(part).Shape
    assert ps.isValid(), part + " ungültig"
    others = list(refs.items()) + [(o, doc.getObject(o).Shape) for o in parts[i + 1:]]
    for n, s in others:
        v = ps.common(s).Volume
        if v > 0.01:
            problems.append(f"{part} x {n}: {v:.1f} mm3")
print("Kollisionen:", problems or "keine")
bb = tub.BoundBox
print(f"Außenmaß: {bb.XLength:.1f} x {bb.YLength:.1f} x {bb.ZLength + T:.1f} mm (B x T x H, mit Deckel)")
if App.GuiUp:
    import FreeCADGui as Gui
    Gui.activeDocument().activeView().viewIsometric()
    Gui.SendMsgToActiveView("ViewFit")
