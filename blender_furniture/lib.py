"""JagoAI Virtual Office v5 -- helper inti (dibangun dari nol).

Semua geometri dikumpulkan ke bmesh per (grup, material) lalu dijadikan satu objek
per kombinasi itu -> objek sedikit, GLB ringan. Blender 5.2, jalan headless.

Konvensi lokal item: "depan" item = +Y lokal. rot=0 -> menghadap utara (+Y dunia),
rot=180 -> selatan, rot=90 -> barat (-X), rot=-90 -> timur (+X).
"""
import bpy
import bmesh
import math
import sys
import colorsys
from contextlib import contextmanager
from mathutils import Matrix, Euler, Vector

PALETTE = {
    # struktur
    "wall_navy": ("#44546E", .85), "wall_cream": ("#F2E8D6", .85), "wall_white": ("#FBF8F1", .8),
    "wall_sage": ("#C9D6C0", .85), "wall_peach": ("#EFCDB4", .85), "wall_sky": ("#CBDDE8", .85),
    "wall_butter": ("#F0E2A8", .85), "wall_lilac": ("#D9CFE6", .85), "wainscot": ("#B58B5E", .7),
    "slab": ("#BDB2A1", .9), "skirt": ("#7B5A3B", .7), "trim": ("#6B4F37", .65),
    "frame_red": ("#B8644F", .6), "door": ("#9A6B45", .6),
    "glass": ("#BFDDEC", .1, 0, None, .35),
    # lantai
    "fl_a": ("#C9A77C", .8), "fl_b": ("#BF9B6F", .8), "fl_c": ("#D3B48A", .8),
    "fl_grey_a": ("#B9BDC2", .85), "fl_grey_b": ("#A9AEB5", .85),
    "tile_w": ("#EFE9DD", .5), "tile_g": ("#9FB5A8", .5),
    "fl_dark_a": ("#7C6347", .8), "fl_dark_b": ("#725A40", .8),
    # kayu / meja
    "wood_dark": ("#6A4E34", .65), "wood": ("#A9825A", .65), "oak": ("#D2B48C", .65),
    "desk_white": ("#EDE6D8", .55), "desk_wood": ("#C09A6B", .55), "counter": ("#E5DAC4", .5),
    "paper": ("#FFFDF5", .9),
    # kain
    "fab_blue": ("#6E8CA8", .9), "fab_grey": ("#9AA0A8", .9), "fab_sage": ("#96AB8C", .9),
    "fab_rose": ("#C98F94", .9), "fab_purple": ("#9D8BAF", .9), "fab_orange": ("#D68F5E", .9),
    "fab_teal": ("#6F9E9A", .9), "fab_cream": ("#E9DCC6", .9), "fab_navy": ("#4A5C77", .9),
    "fab_red": ("#B9574F", .9), "fab_yellow": ("#E2BE5A", .9), "fab_green": ("#6FA36B", .9),
    "bed_white": ("#F4F0E8", .9),
    # perangkat keras
    "metal": ("#B7BBC1", .35, .8), "metal_dark": ("#5C626B", .4, .7), "black": ("#2A2E34", .45),
    "chrome": ("#D5D9DD", .2, .9), "white": ("#F5F5F2", .5), "grey": ("#8E949B", .6),
    # layar (emisif)
    "scr_blue": ("#4F86C6", .3, 0, "#4F86C6"), "scr_teal": ("#3FA79B", .3, 0, "#3FA79B"),
    "scr_warm": ("#E0A35A", .3, 0, "#E0A35A"), "scr_rose": ("#C97F8F", .3, 0, "#C97F8F"),
    "scr_green": ("#6FA86B", .3, 0, "#6FA86B"), "scr_violet": ("#8A6FC0", .3, 0, "#8A6FC0"),
    "scr_dark": ("#1D2228", .25), "light": ("#FFF3C9", .4, 0, "#FFF3C9"),
    # karpet
    "rug_red": ("#A85B52", .95), "rug_teal": ("#4E7E7A", .95), "rug_cream": ("#E2D4B9", .95),
    "rug_rose": ("#BD8A94", .95), "rug_sage": ("#8CA07F", .95), "rug_blue": ("#5F7E9E", .95),
    "rug_navy": ("#3E4F6B", .95), "rug_mustard": ("#C79A3C", .95),
    # tanaman
    "leaf": ("#4F8A4B", .8), "leaf2": ("#6FA85A", .8), "leaf3": ("#3E7A52", .8),
    "pot": ("#B5694A", .7), "pot_w": ("#E8E2D6", .7), "soil": ("#4A3626", 1),
    # warna aksen / benda
    "red": ("#C9483F", .5), "blue": ("#3F6FB5", .5), "yellow": ("#E5B93C", .5),
    "green": ("#4E9A5A", .5), "orange": ("#E08A3C", .5), "pink": ("#E48FA6", .5),
    "purple": ("#8A68B8", .5), "cyan": ("#44A8C4", .5), "skin": ("#E9BE9A", .8),
    "note_y": ("#F4E27A", .9), "note_p": ("#F2A7C0", .9), "note_g": ("#A9DE9A", .9),
    "note_b": ("#9CCBEF", .9), "note_o": ("#F5B87A", .9),
    "board": ("#F7F7F4", .5), "board_cork": ("#B9906A", .9), "board_green": ("#3F6B52", .8),
    "gold": ("#D4AF37", .35, .8), "ps_white": ("#EDEEF0", .4), "backdrop": ("#2F6F8F", .9),
    "green_screen": ("#2FA14A", .9),
    "outline": ("#1B1747", 1.0),
    # tambahan katalog
    "leather_brown": ("#7A4A2E", .55), "leather_black": ("#2A2E34", .5), "mirror": ("#CFE4EE", .1, .9), "rattan": ("#C9A36A", .8),
    "fab_burgundy": ("#7A2E3A", .9), "fab_charcoal": ("#454B55", .9), "rug_charcoal": ("#454B55", .95), "rug_grey": ("#9AA0A8", .95),
    "brass": ("#C9A24D", .35, .8), "bamboo": ("#A9B36A", .7), "cactus": ("#4E8A5E", .8), "leaf_var": ("#9CC47A", .8), "leaf_red": ("#7A3A4A", .8),
    "neon_pink": ("#FF5FA8", .3, 0, "#FF5FA8"), "neon_blue": ("#4FC3FF", .3, 0, "#4FC3FF"), "neon_green": ("#6BFF9A", .3, 0, "#6BFF9A"),
    "led_cool": ("#E8F2FF", .4, 0, "#E8F2FF"), "cream": ("#EFE3C8", .6), "brick": ("#B5654A", .8), "concrete": ("#A7A9A8", .9),
    "crate_blue": ("#3F6FB5", .7), "crate_orange": ("#E08A3C", .7), "cardboard": ("#C79A62", .85), "stone": ("#8E8A82", .8),
    # lantai berwarna per ruang
    "fl_sky_a": ("#A6C9E2", .8), "fl_sky_b": ("#93BAD6", .8), "fl_sage_a": ("#AFD0A4", .8), "fl_sage_b": ("#9CC290", .8),
    "fl_peach_a": ("#EDBF9C", .8), "fl_peach_b": ("#E4AF88", .8), "fl_lilac_a": ("#C2B0DC", .8), "fl_lilac_b": ("#B29DD0", .8),
    "fl_butter_a": ("#F0D98E", .8), "fl_butter_b": ("#E6CB7A", .8),
    "edge_red": ("#E2654D", .6), "edge_teal": ("#3FA79B", .6), "edge_gold": ("#E5B93C", .6),
}

_mats = {}
_bms = {}
_stack = [Matrix.Identity(4)]
GROUP = "MISC"
_cols = {}
_empties = []


SAT_BOOST = 1.38   # "beri warna": naikkan saturasi (HSV) semua material berwarna


def _boost(c):
    h, s, v = colorsys.rgb_to_hsv(*c)
    if s > .08:
        s = min(1.0, s * SAT_BOOST)
    return list(colorsys.hsv_to_rgb(h, s, v))


def hexrgb(h, boost=True):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    if boost:
        c = _boost(c)
    return [(v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4) for v in c] + [1.0]


def mat(name):
    if name in _mats:
        return _mats[name]
    spec = PALETTE[name]
    m = bpy.data.materials.new(name)
    try:
        m.use_nodes = True
    except Exception:
        pass
    n = m.node_tree.nodes.get("Principled BSDF")
    col = hexrgb(spec[0])
    m.diffuse_color = col
    if n:
        n.inputs["Base Color"].default_value = col
        n.inputs["Roughness"].default_value = spec[1]
        n.inputs["Metallic"].default_value = spec[2] if len(spec) > 2 else 0
        if len(spec) > 3 and spec[3]:
            n.inputs["Emission Color"].default_value = hexrgb(spec[3])
            n.inputs["Emission Strength"].default_value = 1.2
        if len(spec) > 4:
            n.inputs["Alpha"].default_value = spec[4]
            try:
                m.surface_render_method = 'BLENDED'
            except Exception:
                pass
    _mats[name] = m
    return m


def group(name):
    global GROUP
    GROUP = name


def set_base(z, dx=0, dy=0):
    _stack[0] = Matrix.Translation((dx, dy, z))
    del _stack[1:]


@contextmanager
def at(x=0, y=0, z=0, rot=0):
    _stack.append(_stack[-1] @ Matrix.Translation((x, y, z)) @ Matrix.Rotation(math.radians(rot), 4, 'Z'))
    try:
        yield
    finally:
        _stack.pop()


def _bm(matname):
    k = (GROUP, matname)
    if k not in _bms:
        _bms[k] = bmesh.new()
    return _bms[k]


def _m(lx, ly, lz, rx, ry, rz, sx, sy, sz, anchor_bottom=True):
    r = Euler((math.radians(rx), math.radians(ry), math.radians(rz)), 'XYZ').to_matrix().to_4x4()
    up = Matrix.Translation((0, 0, sz / 2)) if anchor_bottom else Matrix.Identity(4)
    return _stack[-1] @ Matrix.Translation((lx, ly, lz)) @ r @ up @ Matrix.Diagonal((sx, sy, sz, 1))


RECORD = []   # (grup, benda, minx, maxx, miny, maxy, minz, maxz) dunia -- untuk cek penghalang pintu


def _rec(mtx):
    f = sys._getframe(2)
    names = []
    while f and str(f.f_globals.get("__name__")).startswith(("furn", "shell", "items")):
        names.append(f.f_code.co_name)
        f = f.f_back
    top = names[-1] if names else (f.f_code.co_name if f else "?")
    ps = [mtx @ Vector((a, b, c)) for a in (-.5, .5) for b in (-.5, .5) for c in (-.5, .5)]
    RECORD.append((GROUP, top, min(p.x for p in ps), max(p.x for p in ps), min(p.y for p in ps),
                   max(p.y for p in ps), min(p.z for p in ps), max(p.z for p in ps)))


def bx(lx, ly, lz, sx, sy, sz, m, rx=0, ry=0, rz=0):
    """Kotak: pusat di (lx,ly), alas di lz, ukuran sx,sy,sz."""
    if min(sx, sy, sz) <= 0:
        return
    mt = _m(lx, ly, lz, rx, ry, rz, sx, sy, sz)
    _rec(mt)
    bmesh.ops.create_cube(_bm(m), size=1.0, matrix=mt)


def cy(lx, ly, lz, dx, dy, h, m, r2=1.0, seg=14, rx=0, ry=0, rz=0):
    """Silinder/kerucut: alas di lz, diameter dx,dy, tinggi h, r2=rasio atas."""
    mt = _m(lx, ly, lz, rx, ry, rz, dx, dy, h)
    _rec(mt)
    bmesh.ops.create_cone(_bm(m), cap_ends=True, cap_tris=False, segments=seg, radius1=.5,
                          radius2=.5 * r2, depth=1.0, matrix=mt)


def sp(lx, ly, lz, dx, dy, dz, m, seg=10, rx=0, ry=0, rz=0):
    """Elipsoid: PUSAT di lz."""
    bmesh.ops.create_uvsphere(_bm(m), u_segments=seg, v_segments=max(4, seg // 2), radius=.5,
                              matrix=_m(lx, ly, lz, rx, ry, rz, dx, dy, dz, anchor_bottom=False))


def empty(name, lx=0, ly=0, lz=0, rot=0, size=.3):
    o = bpy.data.objects.new(name, None)
    o.empty_display_size = size
    o.matrix_world = _stack[-1] @ Matrix.Translation((lx, ly, lz)) @ Matrix.Rotation(math.radians(rot), 4, 'Z')
    _empties.append((GROUP, o))
    return o


CUR_COL = None


def _col(gname):
    return CUR_COL


NO_OUTLINE_M = ("glass", "light", "outline", "paper", "note_y", "note_p", "note_g", "note_b", "note_o")
OUT_T = .035
BEV = .025


def _outline_mat():
    m = mat("outline")
    try:
        m.use_backface_culling = True
    except Exception:
        pass
    return m


def bounds(g):
    """bbox (minx,maxx,miny,maxy,minz,maxz) semua kotak/silinder grup g (dari RECORD)."""
    r = [x for x in RECORD if x[0] == g]
    if not r:
        return None
    return (min(a[2] for a in r), max(a[3] for a in r), min(a[4] for a in r), max(a[5] for a in r), min(a[6] for a in r), max(a[7] for a in r))


def flush(style=True):
    """Satu OBJEK per grup (item): banyak slot material + slot 'outline' (hull terbalik) di mesh yang sama."""
    by = {}
    for (g, mn), bm in list(_bms.items()):
        by.setdefault(g, []).append((mn, bm))
    objs = {}
    for g, lst in by.items():
        comb = bmesh.new()
        names = []
        for mn, bm in lst:
            if style and mn != "glass":
                try:
                    ed = [e for e in bm.edges if e.calc_length() > .15]
                    bmesh.ops.bevel(bm, geom=ed, offset=BEV, segments=1, affect='EDGES', clamp_overlap=True, profile=.5)
                except Exception:
                    pass
            names.append(mn)
            idx = len(names) - 1
            vm = {v: comb.verts.new(v.co) for v in bm.verts}
            for f in bm.faces:
                try:
                    nf = comb.faces.new([vm[v] for v in f.verts]); nf.material_index = idx; nf.smooth = False
                except ValueError:
                    pass
        if style:
            oi = len(names)
            has = False
            for mn, bm in lst:
                if mn in NO_OUTLINE_M:
                    continue
                ob = bm.copy()
                bmesh.ops.recalc_face_normals(ob, faces=ob.faces)
                ob.verts.ensure_lookup_table()
                for v in ob.verts:
                    v.normal_update()
                sh = [v.co + v.normal * OUT_T for v in ob.verts]
                for v, c in zip(ob.verts, sh):
                    v.co = c
                bmesh.ops.reverse_faces(ob, faces=ob.faces)
                vm = {v: comb.verts.new(v.co) for v in ob.verts}
                for f in ob.faces:
                    try:
                        nf = comb.faces.new([vm[v] for v in f.verts]); nf.material_index = oi; nf.smooth = False
                        has = True
                    except ValueError:
                        pass
                ob.free()
            if has:
                names.append("outline")
        me = bpy.data.meshes.new(g)
        comb.to_mesh(me)
        comb.free()
        for mn in names:
            me.materials.append(_outline_mat() if mn == "outline" else mat(mn))
        o = bpy.data.objects.new(g, me)
        CUR_COL.objects.link(o)
        objs[g] = o
        for _, bm in lst:
            bm.free()
    _bms.clear()
    for g, o in _empties:
        CUR_COL.objects.link(o)
    _empties.clear()
    return objs
