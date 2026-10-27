# Raspberry Pi 5 Mini-NAS Gehäuse, Version 3
# V3: gemessene HAT-Höhen, 12 mm mehr Tiefe für USB-SATA-Adapter + Kabelbogen
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

# Pi 5 laut offizieller Zeichnung (px entlang 85 mm, py entlang 56 mm, py=0 = HDMI-Kante)
PI_Y0 = D + T - 88            # Pi px=0 so, dass die Ports (3 mm Überstand) bündig mit der Rückwand abschließen
PI_X0 = W - 2                 # py=0 (HDMI-Kante) liegt 2 mm vor der rechten Wand
def pi(px, py):              # Pi-Koordinate -> Gehäuse (X, Y); gedreht, nicht gespiegelt
    return PI_X0 - py, PI_Y0 + px
PCB_Z = TRAY_Z + TRAY_T + STANDOFF_H     # Unterseite Pi-Platine
PCB_TOP = PCB_Z + PCB_T

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

# ---------- Gehäuse (Wanne) ----------
tub = box(-T, -T, -T, W + T, D + T, H).cut(box(0, 0, 0, W, D, H + 1))
cuts = []
# vorne: zwei Laufwerksschächte
mx = (W - (DRV_W + 1.2)) / 2
cuts.append(box(mx, -T - 1, 0, W - mx, 1, SLOT_H))
cuts.append(box(mx, -T - 1, SLOT_H + RAIL, W - mx, 1, 2 * SLOT_H + RAIL))
# vorne: Lüftungsschlitze oberhalb der Schächte
for x in range(10, W - 9, 6):
    cuts.append(box(x, -T - 1, 34, x + 3, 1, 82))
# hinten: Öffnung für Pi-Anschlüsse (USB, USB, Ethernet)
x_a, _ = pi(0, 1); x_b, _ = pi(0, 55)
cuts.append(box(x_a, D - 1, PCB_TOP - 1, x_b, D + T + 1, PCB_TOP + 17))
# hinten: Kabeldurchlass + Luft hinter den Laufwerken
cuts.append(box(8, D - 1, 2, W - 8, D + T + 1, 2 * SLOT_H + RAIL))
# rechts: USB-C + 2x Micro-HDMI
_, y_a = pi(2, 0); _, y_b = pi(48, 0)
cuts.append(box(W - 1, y_a, PCB_Z - 1.5, W + T + 1, y_b, PCB_TOP + 11))
# Seitenschlitze: Laufwerksbereich (beide Seiten) + Pi-Bereich
for y in range(10, int(D) - 10, 7):
    cuts.append(box(-T - 1, y, 3, 0, y + 3, 2 * SLOT_H))
    cuts.append(box(W, y, 3, W + T + 1, y + 3, 2 * SLOT_H))
    if not (y_a - 4 < y < y_b + 1):
        cuts.append(box(W, y, 45, W + T + 1, y + 3, 82))
    else:
        cuts.append(box(W, y, PCB_TOP + 14, W + T + 1, y + 3, 82))
# Boden: Schlitze unter den Laufwerken
for y in range(8, int(D) - 8, 7):
    cuts.append(box(10, y, -T - 1, W - 10, y + 3, 1))
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
# Füße, damit Luft von unten durch den Boden kommt
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
tray = tray.removeSplitter()

# ---------- Deckel ----------
lid = box(-T, -T, H, W + T, D + T, H + T)
lip = box(FIT, FIT, H - 4, W - FIT, D - FIT, H).cut(box(FIT + 2, FIT + 2, H - 5, W - FIT - 2, D - FIT - 2, H + 1))
lid = lid.fuse(lip).removeSplitter()   # geschlossen: kein Staub von oben

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
    "AI_HAT_Reserve": pi_box(0, 0, 65, 56.5, PCB_TOP + 2 * HAT_GAP + 1.6, PCB_TOP + 2 * HAT_GAP + 3.2),
    "AI_HAT_Chip_Reserve": pi_box(10, 10, 50, 46, PCB_TOP + 2 * HAT_GAP + 3.2, PCB_TOP + 2 * HAT_GAP + 9),
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
for n, s in refs.items():
    col = (0.2, 0.6, 0.3) if n.startswith(("Pi5_Plat", "M2_HAT", "AI_HAT_R")) else (0.3, 0.3, 0.3)
    if n.startswith("HDD"):
        col = (0.6, 0.6, 0.65)
    add(n, s, col, 40 if n.startswith("AI") else 0, referenz)
doc.recompute()

# ---------- Selbsttest: keine Überschneidungen ----------
problems = []
for part in ("Gehaeuse", "Pi_Traeger", "Deckel"):
    ps = doc.getObject(part).Shape
    assert ps.isValid(), part + " ungültig"
    for n, s in refs.items():
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
