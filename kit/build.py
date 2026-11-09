"""Build the Virtual Office toon furniture kit.

  blender -b --factory-startup --python kit/build.py -- [--glb] [--render]

Outputs (relative to the project root):
  blend/vo_furniture_kit.blend      COL_Kit (items at origin) + COL_Preview_<category> rows
  out/vo_furniture_kit.glb          COL_Kit only, Y-up                       (--glb)
  out/kit_spec.json                 ids, labels, categories, mount, sizes, tris, materials
  renders/sheet_<category>.png      one labelled sheet per category          (--render)
  renders/kit_overview.png          all rows                                 (--render)
"""
import json
import math
import os
import sys

import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import lib    # noqa: E402
import items  # noqa: E402
import items_more  # noqa: E402,F401  (registers v4 items)
import items_dept  # noqa: E402,F401  (registers v5 department items + workstations)

TRI_BUDGET = 2200   # v3: softer bevels; still light for web (~1.4k avg)
CATEGORY_ORDER = ["work", "seating", "tech", "desk_gear", "meeting", "lounge", "storage", "pantry", "decor", "wall",
                  "dept_it", "dept_creative", "dept_content", "dept_marketing", "dept_finance", "dept_hr",
                  "dept_sales", "dept_exec", "station"]
BUDGETS = {"station": 9000}   # composed workstations: desk + screens + props in one mesh
args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []

bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
kit = bpy.data.collections.new("COL_Kit")
scene.collection.children.link(kit)

# ---------------------------------------------------------------- build items at origin
spec = {"version": 2, "units": "meters", "up": "+Z blender / +Y glTF", "front": "-Y blender / +Z glTF",
        "pivot": {"floor": "bottom center at floor", "table": "bottom center, set on a table top",
                  "wall": "back face on the wall plane, bottom edge at z=0; hang at mount_z"},
        "outline": {"object_suffix": "_outline", "hex": lib.OUTLINE_HEX, "thickness_m": lib.OUTLINE_T,
                    "three_js": "MeshBasicMaterial, side FrontSide (hull winding is already flipped)"},
        "items": []}
objs = {}
over = []
for item_id, r in items.REGISTRY.items():
    it = lib.Item(item_id)
    r["fn"](it)
    ob = it.done(kit)
    objs[item_id] = ob
    bb = [ob.matrix_world @ Vector(c) for c in ob.bound_box]
    lo = [min(v[i] for v in bb) for i in range(3)]
    hi = [max(v[i] for v in bb) for i in range(3)]
    t = lib.tris(ob)
    if t > BUDGETS.get(r["category"], TRI_BUDGET):
        over.append((item_id, t))
    spec["items"].append({"id": item_id, "label": r["label"], "category": r["category"], "node": ob.name,
                          "mount": r["mount"], "mount_z": r["mount_z"],
                          "size_m": {k: round(hi[i] - lo[i], 3) for i, k in enumerate("xyz")},
                          "bbox_min": [round(v, 3) for v in lo], "bbox_max": [round(v, 3) for v in hi],
                          "tris": t, "materials": [m.name for m in ob.data.materials]})
spec["palette"] = {m.name: m["hex"] for m in bpy.data.materials if "hex" in m}

os.makedirs(os.path.join(ROOT, "out"), exist_ok=True)
with open(os.path.join(ROOT, "out", "kit_spec.json"), "w", encoding="utf-8") as f:
    json.dump(spec, f, indent=1)
print("ITEMS", len(objs), "TRIS_TOTAL", sum(i["tris"] for i in spec["items"]),
      "MAX", max((i["tris"], i["id"]) for i in spec["items"]))
print("OVER_BUDGET", over)

if "--glb" in args:
    bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children["COL_Kit"]
    path = os.path.join(ROOT, "out", "vo_furniture_kit.glb")
    bpy.ops.export_scene.gltf(filepath=path, export_format="GLB", use_active_collection=True, export_yup=True,
                              export_apply=False)
    print("GLB", path, os.path.getsize(path))

# ---------------------------------------------------------------- preview rows (linked copies + labels)
label_mat = lib.mat("charcoal")
cats = [c for c in CATEGORY_ORDER if any(i["category"] == c for i in spec["items"])]
cats += [c for c in dict.fromkeys(i["category"] for i in spec["items"]) if c not in cats]
GAP, ROW_GAP = .45, 1.8
rows = {}
row_y = 0.0
for cat in cats:
    col = bpy.data.collections.new("COL_Preview_" + cat)
    scene.collection.children.link(col)
    row = [i for i in spec["items"] if i["category"] == cat]
    total = sum(i["size_m"]["x"] for i in row) + GAP * (len(row) - 1)
    depth = max(i["size_m"]["y"] for i in row)
    height = max(i["size_m"]["z"] + (.6 if i["mount"] == "wall" else 0) for i in row)
    x = -total / 2
    for i in row:
        src = objs[i["id"]]
        cx = x + i["size_m"]["x"] / 2
        lift = .6 if i["mount"] == "wall" else 0.0          # wall items float above floor on a preview wall
        root = src.copy()
        col.objects.link(root)
        root.location = (cx, row_y, lift)
        hull = src.children[0].copy()
        col.objects.link(hull)
        hull.parent = root
        bpy.ops.object.text_add(location=(cx, row_y + i["bbox_min"][1] - .22, 0))
        lbl = bpy.context.active_object
        lbl.data.body = i["label"]
        lbl.data.size = .1
        lbl.data.align_x = "CENTER"
        lbl.data.align_y = "TOP"
        lbl.data.materials.append(label_mat)
        for c in lbl.users_collection:
            c.objects.unlink(lbl)
        col.objects.link(lbl)
        x += i["size_m"]["x"] + GAP
    if cat == "wall":   # a pale backdrop so wall pieces read as hung
        bpy.ops.mesh.primitive_cube_add(size=1, location=(0, row_y + .03, 1.0))
        wall = bpy.context.active_object
        wall.scale = (total + .6, .06, 2.0)
        wall.data.materials.append(lib.mat("offwhite"))
        for c in wall.users_collection:
            c.objects.unlink(wall)
        col.objects.link(wall)
    rows[cat] = dict(col=col, y=row_y, width=total, depth=depth, height=height)
    row_y += depth + ROW_GAP
kit.hide_viewport = True
kit.hide_render = True

os.makedirs(os.path.join(ROOT, "blend"), exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT, "blend", "vo_furniture_kit.blend"))
print("SAVED blend")

# ---------------------------------------------------------------- renders
if "--render" in args:
    scene.render.engine = "BLENDER_WORKBENCH"
    sh = scene.display.shading
    sh.light = "FLAT"
    sh.color_type = "MATERIAL"
    sh.show_backface_culling = True
    sh.show_cavity = False
    scene.view_settings.view_transform = "Standard"
    scene.world = bpy.data.worlds.new("W")
    scene.world.color = (.96, .95, .93)
    cam = bpy.data.objects.new("CAM_Preview", bpy.data.cameras.new("CAM_Preview"))
    scene.collection.objects.link(cam)
    cam.data.type = "ORTHO"
    scene.camera = cam
    os.makedirs(os.path.join(ROOT, "renders"), exist_ok=True)

    def shoot(path, target, scale, res, tilt=70, yaw=-15):
        cam.rotation_euler = (math.radians(tilt), 0, math.radians(yaw))
        cam.data.ortho_scale = scale
        d = cam.rotation_euler.to_matrix() @ Vector((0, 0, 1))
        cam.location = Vector(target) + d * 40
        scene.render.resolution_x, scene.render.resolution_y = res
        scene.render.filepath = path
        bpy.ops.render.render(write_still=True)

    for cat, r in rows.items():
        for c2, r2 in rows.items():
            r2["col"].hide_render = c2 != cat
        # frame tight: width sets ortho scale, visible height (+ label strip) sets the aspect
        scale = r["width"] + .8
        vis_h = r["height"] + (r["depth"] + .5) * math.cos(math.radians(70)) + 1.0
        res_x = max(1600, min(3200, int(scale * 170)))   # long rows (stations) get more pixels
        res_y = max(400, int(res_x * vis_h / scale))
        shoot(os.path.join(ROOT, "renders", f"sheet_{cat}.png"), (0, r["y"] - .15, r["height"] * .45),
              scale, (res_x, res_y))
        print("SHEET", cat)
    for r in rows.values():
        r["col"].hide_render = False
    width = max(r["width"] for r in rows.values())
    shoot(os.path.join(ROOT, "renders", "kit_overview.png"), (0, row_y / 2 - 1.2, .5), width + 2.5, (1800, 1800),
          tilt=58, yaw=-20)
    print("OVERVIEW")
