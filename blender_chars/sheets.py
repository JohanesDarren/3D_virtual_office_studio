"""Lembar katalog per slot (PART SAJA + label) dan cek topi. blender -b --python blender_chars/sheets.py [-- hair top ... | cektopi]"""
import sys, os, math, bpy
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import anim, catalog
import p_extra  # noqa: F401
OUT = r"D:/1. ASET JAGOAI/12. BLENDER/JagoAI Virtual Office/renders/"
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
sc.render.engine = 'BLENDER_WORKBENCH'
sc.display.shading.light = 'STUDIO'; sc.display.shading.color_type = 'MATERIAL'
sc.display.shading.show_shadows = False; sc.display.shading.show_backface_culling = True
sc.view_settings.view_transform = 'Standard'
sc.world = bpy.data.worlds.new("w"); sc.world.color = (.86, .9, .94)
want = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []


def shot(path, cx, cz, w, h, ppm):
    c = bpy.data.cameras.new("c"); c.type = 'ORTHO'; c.ortho_scale = w
    o = bpy.data.objects.new("c", c); sc.collection.objects.link(o)
    o.location = (cx, -12, cz); o.rotation_euler = (math.radians(90), 0, 0); sc.camera = o
    sc.render.resolution_x = int(w * ppm); sc.render.resolution_y = int(h * ppm)
    sc.render.filepath = OUT + path
    bpy.ops.render.render(write_still=True)
    bpy.data.objects.remove(o)


def clear():
    for o in list(bpy.data.objects):
        bpy.data.objects.remove(o)


for name in (want or list(catalog.ROWS) + ["warna"]):
    clear()
    if name == "cektopi":
        nh, nt = catalog.cek_topi()
        for o in list(bpy.data.objects):
            if o.type == 'ARMATURE':
                anim.apply(o, lambda t: {}, 0)
        # hanya kepala+bahu: potong tampilan di sekitar kepala
        for r in range(nt):
            shot(f"chars_cektopi_{r}.png", 0, 1.55 - r * 2.4, nh * 1.3, 1.9, 150)
        print("CEKTOPI", nh, nt)
        continue
    if name == "cekwajah":
        import p_face, presets
        from char import make_character
        fs, ms = list(p_face.FACE), list(p_face.MOUTH)
        for i in range(max(len(fs), len(ms))):
            pr = dict(presets.PRESETS["baru"]); pr["face"] = fs[i % len(fs)]; pr["mouth"] = ms[i % len(ms)]; pr["blush"] = i % 3 == 1
            make_character(f"f{i:02d}", pr, (i - 5.5) * 1.0, 0)
        for o in list(bpy.data.objects):
            if o.type == 'ARMATURE':
                anim.apply(o, lambda t: {}, 0)
        shot("chars_cekwajah.png", 0, 1.25, 12.0, 1.0, 230)
        print("CEKWAJAH")
        continue
    if name == "warna":
        w, h = catalog.add_palettes(z=0)
        shot("chars_sheet_warna.png", -2.8 + (w - 3.5) / 2 + .2, -h / 2 + .55, w + .6, h + .3, 150)
        print("SHEET warna")
        continue
    reg, zc, h, sp, ppm = catalog.ROWS[name]
    n = catalog.add_row(name)
    shot(f"chars_sheet_{name}.png", 0, zc, n * sp, h, ppm)
    print("SHEET", name, n)
