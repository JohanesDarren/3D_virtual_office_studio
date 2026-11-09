"""Render lembar katalog per kategori + palet warna. blender -b --python blender_furniture/sheets.py [-- duduk meja ... warna]"""
import sys, os, math, bpy
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import lib, registry, catalog
OUT = r"D:/1. ASET JAGOAI/12. BLENDER/JagoAI Virtual Office/renders/"
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'BLENDER_WORKBENCH'
sc.display.shading.light = 'STUDIO'; sc.display.shading.color_type = 'MATERIAL'
sc.display.shading.show_shadows = False; sc.display.shading.show_backface_culling = True
sc.view_settings.view_transform = 'Standard'
sc.world = bpy.data.worlds.new("w"); sc.world.color = (.86, .9, .94)
want = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
PPM = float(os.environ.get("PPM", 90))
TILT = 45


def shot(path, cx, cy, W, D, zmax=2.6, tilt=TILT, zc=None, H=None):
    rx = math.radians(tilt)
    c = bpy.data.cameras.new("c"); c.type = 'ORTHO'; c.ortho_scale = W
    o = bpy.data.objects.new("c", c); sc.collection.objects.link(o)
    d = (0, math.sin(rx), -math.cos(rx))
    t = (cx, cy, zmax * .35 if zc is None else zc)
    o.location = (t[0] - d[0] * 60, t[1] - d[1] * 60, t[2] - d[2] * 60)
    o.rotation_euler = (rx, 0, 0); sc.camera = o
    H = H or ((D * math.cos(rx) + zmax * math.sin(rx)) + .8)
    sc.render.resolution_x = int(W * PPM); sc.render.resolution_y = int(H * PPM)
    sc.render.filepath = OUT + path
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(o)


catalog.build_items()
bpy.data.collections["KIT"].hide_render = True
for cat in (want or registry.CATS + ["warna"]):
    if cat == "warna":
        col = bpy.data.collections.new("PAL"); sc.collection.children.link(col)
        w, h = catalog.add_palettes(col=col)
        shot("furn_sheet_warna.png", w / 2, 0, w, 0, tilt=90, zc=-h / 2 + .6, H=h + .8)
        print("SHEET warna"); col.hide_render = True
        continue
    col = bpy.data.collections.new("C_" + cat); sc.collection.children.link(col)
    ext = catalog.layout(cats=[cat], col=col).get(cat)
    if not ext:
        continue
    x0, x1, y0, y1 = ext
    shot(f"furn_sheet_{cat}.png", (x0 + x1) / 2, (y0 + y1) / 2, x1 - x0 + 1, y1 - y0)
    col.hide_render = True
    print("SHEET", cat, x1 - x0, y1 - y0)
