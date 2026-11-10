"""Bangun katalog perabot JagoAI: semua item (sudah dipakai + varian baru), spec JSON, GLB, dan .blend katalog.
Jalankan: blender -b --python blender_furniture/build.py [-- --glb]
GLB hanya berisi collection KIT (tiap item = 1 objek 'FURN_<id>' di titik asal, banyak slot material + 'outline')."""
import sys, os, json, bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lib, registry, catalog, colors

OUT_BLEND = r"D:/1. ASET JAGOAI/12. BLENDER/JagoAI Virtual Office/JagoAI_Furniture_v1.blend"
OUT_DIR = os.path.join(HERE, "out")
OUT_GLB = os.path.join(OUT_DIR, "jagoai_furniture_kit.glb")

bpy.ops.wm.read_factory_settings(use_empty=True)
objs = catalog.build_items()


def tris(o):
    me = o.data
    me.calc_loop_triangles()
    return len(me.loop_triangles)


items = []
bad = []
for r in registry.REG:
    o = r["obj"]
    mats = [m.name for m in o.data.materials if m and m.name != "outline"]
    for m, fam in r["tint"].items():
        if m not in mats:
            bad.append(f"{r['id']}: tint '{m}' tidak ada di item (ada: {mats})")
        if fam not in colors.FAMILIES:
            bad.append(f"{r['id']}: keluarga '{fam}' tidak ada")
    b = r["bbox"]
    items.append({
        "id": r["id"], "kategori": r["cat"], "label": r["label"], "node": "FURN_" + r["id"],
        "dipakai_di_app": r["used"], "pasang": r["mount"], "z_pasang": r["z"],
        "ukuran_m": {"lebar_x": round(b[1] - b[0], 2), "dalam_y": round(b[3] - b[2], 2), "tinggi_z": round(b[5] - b[4], 2)},
        "tris": tris(o), "material": mats,
        "warna": [{"material": m, "keluarga": fam, "default": lib.PALETTE[m][0]} for m, fam in r["tint"].items()],
    })
assert not bad, "\n".join(bad)

cats = {c: [i["id"] for i in items if i["kategori"] == c] for c in registry.CATS if any(i["kategori"] == c for i in items)}
spec = {
    "versi": 1,
    "konvensi": {
        "satuan": "meter", "up": "+Z blender (+Y glTF)", "depan_item": "+Y lokal blender (rot=0 menghadap utara)",
        "pivot": "item lantai: pusat, alas z=0. item dinding: punggung y=0, z=0 = tepi bawah item, pasang di z_pasang. langit-langit: z=0 = titik gantung/atas, pasang di z_pasang.",
        "pasang": {"floor": "berdiri di lantai", "table": "barang kecil, diletakkan di atas meja (alas z=0)", "wall": "menempel dinding", "ceiling": "langit-langit"},
        "node": "tiap item = satu objek 'FURN_<id>' (transform di GLB diabaikan: pakai pivot item); banyak slot material + slot 'outline' (hull terbalik)",
        "outline": {"material": "outline", "hex": lib.OUTLINE_HEX if hasattr(lib, "OUTLINE_HEX") else "#1B1747", "catatan": "di app ganti ke MeshBasicMaterial navy (BackSide)"},
        "boost_warna": "material memakai SAT_BOOST 1.38 di Blender; hex di spec = warna dasar sebelum boost. Di app, tint langsung pakai hex pilihan.",
    },
    "kategori": {c: {"label": registry.CAT_LABEL[c], "item": ids} for c, ids in cats.items()},
    "keluarga_warna": colors.spec(),
    "catatan_warna": "tiap item menandai material yang boleh diganti user ('warna': material + keluarga palet). Klon material per instance lalu set warna. Sediakan juga pemilih hex bebas. Material lain tetap.",
    "item": items,
}
os.makedirs(OUT_DIR, exist_ok=True)
json.dump(spec, open(os.path.join(HERE, "furniture_spec.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)

used = [i for i in items if i["dipakai_di_app"]]
print("ITEM", len(items), "dipakai", len(used), "baru", len(items) - len(used))
print("PER_KATEGORI", {c: (len(ids), sum(1 for i in items if i["kategori"] == c and i["dipakai_di_app"])) for c, ids in cats.items()})
print("TRIS_TOTAL", sum(i["tris"] for i in items), "MAX", max(items, key=lambda i: i["tris"])["id"], max(i["tris"] for i in items))
print("FAMILI", {k: len(v[1]) for k, v in colors.FAMILIES.items()})

if "--glb" in sys.argv:
    kit = bpy.data.collections["KIT"]
    bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children["KIT"]
    bpy.ops.export_scene.gltf(filepath=OUT_GLB, export_format='GLB', export_apply=False, export_yup=True, use_active_collection=True)
    print("GLB", OUT_GLB, os.path.getsize(OUT_GLB))

# ---- katalog: tiap item dipajang satu-satu, per kategori + lembar palet warna
bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection
ext = catalog.layout()
col = bpy.data.collections.get("KATALOG")
ymax = max(e[3] for e in ext.values())
pal = bpy.data.collections.new("PALET_WARNA"); bpy.context.scene.collection.children.link(pal)
catalog.label("PALET WARNA (pilihan user per keluarga material)", 0, ymax + 6, 0, size=.6, col=pal, align='LEFT')
catalog.add_palettes(x0=0, y0=ymax + 4, col=pal)
bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
print("SAVED", OUT_BLEND)
