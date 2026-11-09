"""Render uji. blender -b --python blender_chars/render.py -- lineup | sit | turn | anim
Membuka JagoAI_Characters_v2.blend (kit di koleksi KIT disembunyikan untuk lineup/sit)."""
import bpy, sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import anim
OUT = r"D:/1. ASET JAGOAI/12. BLENDER/JagoAI Virtual Office/renders/"
args = sys.argv[sys.argv.index("--") + 1:]
bpy.ops.wm.open_mainfile(filepath=r"D:/1. ASET JAGOAI/12. BLENDER/JagoAI Virtual Office/JagoAI_Characters_v2.blend")
sc = bpy.context.scene
sc.render.engine = 'BLENDER_WORKBENCH'
sc.display.shading.light = 'STUDIO'; sc.display.shading.color_type = 'MATERIAL'
sc.display.shading.show_shadows = False; sc.display.shading.show_cavity = False
sc.display.shading.show_backface_culling = True
sc.world = bpy.data.worlds.new("w"); sc.world.color = (.86, .9, .94)


def cam(loc, rot, scale):
    c = bpy.data.cameras.new("c"); c.type = 'ORTHO'; c.ortho_scale = scale
    o = bpy.data.objects.new("c", c); sc.collection.objects.link(o)
    o.location = loc; o.rotation_euler = [math.radians(r) for r in rot]; sc.camera = o


def shot(path, loc, rot, scale, w, h):
    sc.render.resolution_x, sc.render.resolution_y = w, h
    cam(loc, rot, scale); sc.render.filepath = OUT + path
    bpy.ops.render.render(write_still=True); bpy.data.objects.remove(sc.camera)


for o in bpy.data.objects:
    if o.type == 'ARMATURE': o.hide_render = True
chars = {o.name[3:-4]: o for o in bpy.data.objects if o.type == 'ARMATURE' and o.name.startswith("CH_")}
kit_rig = bpy.data.objects["KIT_rig"]
kit_rig.animation_data_clear()
fns = anim.clips(kit_rig, bake=False)
for o in list(bpy.data.collections["KIT"].all_objects):
    if o is not None: o.hide_render = True


def hide_chars(keep):
    for k, r in chars.items():
        for o in list(bpy.data.collections[f"CH_{k}"].all_objects):
            if o is not None and o.type != 'ARMATURE':
                o.hide_render = k not in keep


for kind in args:
    if kind == "lineup":
        for k, r in chars.items():
            anim.apply(r, fns["idle"][1], 0)
        shot("chars_lineup.png", (0, -14, 1.0), (90, 0, 0), 15.5, 2600, 520)
        shot("chars_lineup_back.png", (0, 14, 1.0), (90, 0, 180), 15.5, 2600, 520)
    elif kind == "sit":
        # kursi + meja sederhana (dudukan 0.49 = furn.chair); 8 karakter, 8 state, dari depan
        order = [("mira", "type"), ("rian", "think"), ("nadia", "review"), ("bayu", "coffee"), ("sinta", "ship"), ("doni", "error"), ("omar", "sleep"), ("kiki", "sit_idle")]
        hide_chars({k for k, _ in order})
        for i, (k, st) in enumerate(order):
            r = chars[k]
            r.location.z = anim.SIT_ROOT_Z
            anim.apply(r, fns[st][1], .25)
            x = r.location.x
            for sz, loc in (((.46, .46, .07), (x, 0.0, .455)), ((.44, .06, .46), (x, .22, .72))):
                bpy.ops.mesh.primitive_cube_add(size=1, location=loc); b = bpy.context.active_object; b.scale = sz
            bpy.ops.mesh.primitive_cube_add(size=1, location=(x, -.62, .72)); d = bpy.context.active_object; d.scale = (1.0, .6, .04)
        shot("chars_sit.png", (0, -14, 1.0), (90, 0, 0), 11, 2200, 600)
        shot("chars_sit_side.png", (14, 0, 1.0), (90, 0, 90), 11, 1800, 600)
    elif kind == "turn":
        r = chars["mira"]; hide_chars({"mira"}); anim.apply(r, fns["idle"][1], 0)
        loc = r.location
        for nm, (dx, dy, rz) in {"front": (0, -10, 0), "side": (10, 0, 90), "back": (0, 10, 180)}.items():
            shot(f"chars_turn_{nm}.png", (loc.x + dx, loc.y + dy, 1.0), (90, 0, rz), 2.4, 700, 900)
    elif kind == "anim":
        hide_chars({"mira"}); r = chars["mira"]; loc = r.location
        for name, (n, fn) in fns.items():
            anim.apply(r, fn, .25)
            shot(f"chars_anim_{name}.png", (loc.x + 10, loc.y, 1.0), (90, 0, 90), 2.4, 500, 600)
