"""Katalog PART SAJA (tanpa manekin): tiap part dipajang satu-satu di baris per slot, lengkap dgn label.
Part berada di tinggi aslinya (koordinat karakter), jadi tinggal dipakai di app tanpa geser.
Juga cek_topi(): grid topi x rambut memakai karakter lengkap (hanya untuk uji tembus)."""
import bpy, math
import lib, p_hair, p_face, p_outfit, p_acc, presets
from char import make_character

# row -> (registry, zc tengah tampilan, h tinggi tampilan, spacing, piksel per meter)
ROWS = {
    "hair": (lambda: p_hair.HAIR, 1.50, 1.60, 1.30, 130),
    "face": (lambda: p_face.FACE, 1.32, .60, .70, 330),
    "mouth": (lambda: p_face.MOUTH, 1.10, .40, .50, 420),
    "fhair": (lambda: p_face.FHAIR, 1.10, .50, .60, 380),
    "top": (lambda: p_outfit.TOP, .72, .95, 1.30, 150),
    "bottom": (lambda: p_outfit.BOTTOM, .38, .75, 1.30, 170),
    "shoes": (lambda: p_outfit.SHOES, .16, .45, .80, 300),
    "acc": (lambda: p_acc.ACC, 1.20, 2.30, 1.60, 100),
}
_label_mat = None


def _mat():
    global _label_mat
    if _label_mat is None:
        _label_mat = bpy.data.materials.new("M_label"); _label_mat.diffuse_color = (.1, .09, .28, 1)
    return _label_mat


def label(text, x, y, z, size=.14):
    bpy.ops.object.text_add(location=(x, y, z), rotation=(math.radians(90), 0, 0))
    o = bpy.context.active_object
    o.data.body = text; o.data.size = size; o.data.align_x = 'CENTER'; o.data.align_y = 'TOP'
    o.data.materials.append(_mat()); o.name = "LBL_" + text
    return o


def _colors():
    col = presets.colors(presets.PRESETS["baru"])
    col.update({"M_hair": "#2B1D14", "M_acc": "#E5B93C", "M_acc3": "#C9483F", "M_top": "#5B7BA8", "M_bottom": "#3B4660"})
    return col


def add_row(row, x0=0.0, y=0.0, z=0.0):
    """Satu baris part-saja, pusat x0, dasar z. Mengembalikan jumlah item."""
    reg, zc, h, sp, ppm = ROWS[row]
    items = list(reg().items())
    for i, (name, fn) in enumerate(items):
        x = x0 + (i - (len(items) - 1) / 2) * sp
        c = lib.Ctx(f"P_{row}_{i:02d}_{name}", tag=f"@{row}{i}", colors=_colors(), offset=(x, y, z))
        fn(c)
        c.rig.hide_set(True)   # rangka tak perlu tampil di katalog
        label(f"{i + 1}. {name}", x, y - .5, z + zc - h / 2 + .07 * h + .09, size=.07 * h + .05)
    return len(items)


def cek_topi(x0=0.0, y=0.0, z=0.0):
    """Grid: baris = topi, kolom = rambut, karakter lengkap dgn HAIRTOP disembunyikan (seperti di app)."""
    hairs = list(p_hair.HAIR)
    hats = list(p_acc.HEAD_HAT)
    for r, hat in enumerate(hats):
        for i, hs in enumerate(hairs):
            pr = dict(presets.PRESETS["baru"]); pr["hair_style"] = hs; pr["acc"] = [hat]; pr["acc_c"] = "#E5B93C"
            make_character(f"hat{r}_{i:02d}", pr, x0 + (i - (len(hairs) - 1) / 2) * 1.3, y, z - r * 2.4)
    return len(hairs), len(hats)


def add_palettes(x0=0.0, y=0.0, z=0.0, sp=.62):
    """Lembar warna: satu baris per kelompok material (kulit, rambut, ...), cakram warna + nama + hex. Mengembalikan (lebar, tinggi)."""
    import colors
    row_h = .98
    wmax = 0
    for r, (key, (lab, cols)) in enumerate(colors.PALETTES.items()):
        zr = z - r * row_h
        wmax = max(wmax, len(cols) * sp)
        label(f"{lab}  [{key}]", x0 - 2.8, y, zr + .42, size=.11).data.align_x = 'LEFT'
        for i, (nm, hx) in enumerate(cols):
            x = x0 + (i + .5) * sp - 2.6
            bpy.ops.mesh.primitive_cylinder_add(radius=.2, depth=.04, location=(x, y, zr), rotation=(math.radians(90), 0, 0), vertices=24)
            o = bpy.context.active_object; o.name = f"SW_{key}_{i:02d}"
            o.data.materials.append(lib.make_mat(f"SW_{key}_{i:02d}", hx))
            label(nm, x, y - .05, zr - .24, size=.055)
            label(hx, x, y - .05, zr - .32, size=.045)
    return wmax + 3.5, len(colors.PALETTES) * row_h
