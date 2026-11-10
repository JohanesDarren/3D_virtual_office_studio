"""Bangun semua item (registry) + tata letak katalog. Item dibangun di titik asal -> KIT (untuk GLB, tanpa rotasi);
KATALOG = salinan berputar 180 (menghadap kamera selatan) dengan label, dikelompokkan per kategori."""
import bpy, math
import lib
import registry
import items_used  # noqa: F401
for _m in ('furn_new1', 'furn_new2', 'furn_new3'):
    try:
        __import__(_m)
    except ModuleNotFoundError as _e:
        if _e.name != _m:
            raise

MAXW = 24.0
GAP = .7
ROWGAP = 1.3
DISPLAY_Z = {"floor": 0.0, "table": 0.0, "wall": .5, "ceiling": .5}


def build_items():
    """Kembalikan {id: obj} di collection KIT (semua di titik asal)."""
    kit = bpy.data.collections.get("KIT") or bpy.data.collections.new("KIT")
    if kit.name not in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.link(kit)
    lib.CUR_COL = kit
    for r in registry.REG:
        lib.group("FURN_" + r["id"])
        r["fn"]()
    objs = lib.flush()
    out = {}
    for r in registry.REG:
        o = objs["FURN_" + r["id"]]
        r["obj"] = o
        out[r["id"]] = o
        vs = [o.matrix_world @ __import__("mathutils").Vector(c) for c in o.bound_box]
        r["bbox"] = (min(v.x for v in vs), max(v.x for v in vs), min(v.y for v in vs), max(v.y for v in vs), min(v.z for v in vs), max(v.z for v in vs))
    return out


_label_mat = None


def _mat():
    global _label_mat
    if _label_mat is None:
        _label_mat = bpy.data.materials.new("M_label"); _label_mat.diffuse_color = (.1, .09, .28, 1)
    return _label_mat


def label(text, x, y, z, size=.14, col=None, align='CENTER'):
    bpy.ops.object.text_add(location=(x, y, z), rotation=(math.radians(90), 0, 0))
    o = bpy.context.active_object
    o.data.body = text; o.data.size = size; o.data.align_x = align; o.data.align_y = 'TOP'
    o.data.materials.append(_mat()); o.name = "LBL_" + text
    if col:
        col.objects.link(o); bpy.context.scene.collection.objects.unlink(o)
    return o


def layout(cats=None, y0=0.0, x0=0.0, col=None, names=True):
    """Susun KATALOG (salinan) per kategori. Mengembalikan {cat: (x0, x1, y0, y1)}."""
    if col is None:
        col = bpy.data.collections.new("KATALOG"); bpy.context.scene.collection.children.link(col)
    y = y0
    ext = {}
    for cat in registry.CATS:
        if cats and cat not in cats:
            continue
        items = [r for r in registry.REG if r["cat"] == cat]
        if not items:
            continue
        ystart = y
        label(registry.CAT_LABEL[cat].upper() + f"  ({len(items)})", x0, y - .2, 0, size=.55, col=col, align='LEFT')
        y += 1.6
        cx = x0; rowd = 0; rowh = 0; row = []
        xmax = x0

        def place(row, ytop, depth):
            for r, xx in row:
                o = r["obj"].copy(); o.data = r["obj"].data
                o.rotation_euler = (0, 0, math.pi)
                b = r["bbox"]
                o.location = (xx + b[1], ytop + b[3] - (depth - (b[3] - b[2])) * 0, DISPLAY_Z[r["mount"]])
                col.objects.link(o)
                o.name = "KAT_" + r["id"]
                if names:
                    label(r["id"], xx + (b[1] - b[0]) / 2, ytop - .35, 0, size=max(.08, min(.17, (b[1] - b[0] + GAP * .9) / (len(r['id']) * .6))), col=col)
        for r in items:
            b = r["bbox"]; w = b[1] - b[0]; d = b[3] - b[2]
            if cx + w > x0 + MAXW and row:
                place(row, y, rowd); y += rowd + rowh * 1.0 + .5; cx = x0; rowd = 0; rowh = 0; row = []
            row.append((r, cx)); cx += w + GAP; rowd = max(rowd, d); rowh = max(rowh, b[5] + DISPLAY_Z[r['mount']]); xmax = max(xmax, cx)
        place(row, y, rowd); yend = y + rowd
        y = yend + ROWGAP + 1.0
        ext[cat] = (x0, xmax - GAP, ystart - .6, yend)
    return ext


def add_palettes(x0=0.0, y0=0.0, sp=.7, col=None):
    """Lembar warna: satu baris per keluarga, cakram + nama + hex. Datar di lantai? tidak: berdiri menghadap selatan."""
    import colors
    z = 0.0
    wmax = 0
    for key, (lab, cols) in colors.FAMILIES.items():
        wmax = max(wmax, len(cols) * sp)
        label(f"{lab}  [{key}]", x0, y0, z + .45, size=.16, col=col, align='LEFT')
        for i, (nm, hx) in enumerate(cols):
            x = x0 + (i + .5) * sp
            bpy.ops.mesh.primitive_cylinder_add(radius=.23, depth=.04, location=(x, y0, z), rotation=(math.radians(90), 0, 0), vertices=24)
            o = bpy.context.active_object; o.name = f"SW_{key}_{i:02d}"
            o.data.materials.append(lib.make_mat(f"SW_{key}_{i:02d}", hx) if hasattr(lib, "make_mat") else _plain(f"SW_{key}_{i:02d}", hx))
            col.objects.link(o); bpy.context.scene.collection.objects.unlink(o)
            label(nm, x, y0 - .05, z - .27, size=.065, col=col)
            label(hx, x, y0 - .05, z - .37, size=.055, col=col)
        z -= 1.15
    return wmax + .6, -z


def _plain(name, hx):
    m = bpy.data.materials.new(name)
    c = lib.hexrgb(hx, boost=False)
    m.diffuse_color = c
    return m
