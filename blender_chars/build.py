"""Bangun kit karakter JagoAI: kit lengkap (semua part + 10 clip) + lineup 11 karakter.
Jalankan: blender -b --python blender_chars/build.py [-- --glb]
GLB kit hanya berisi koleksi KIT (diekspor sebelum lineup dibuat) -> blender_chars/out/.
"""
import sys, os, json, bpy
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lib, body, anim, p_hair, p_face, p_outfit, p_acc, presets
import p_extra  # noqa: F401
import catalog, colors

OUT_BLEND = r"D:/1. ASET JAGOAI/12. BLENDER/JagoAI Virtual Office/JagoAI_Characters_v2.blend"
OUT_DIR = os.path.join(HERE, "out")
OUT_GLB = os.path.join(OUT_DIR, "jagoai_chars_kit.glb")

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.context.scene.render.fps = anim.FPS

# ---- kit lengkap
kit = lib.Ctx("KIT", offset=(0, 8, 0))
body.build_body(kit)
for reg in (p_hair.HAIR, p_outfit.TOP, p_outfit.BOTTOM, p_outfit.SHOES, p_acc.ACC, p_face.FACE):
    for fn in reg.values():
        fn(kit)
for fn in p_face.MOUTH.values():
    fn(kit)
for fn in p_face.FHAIR.values():
    fn(kit)
p_face.blush(kit)
clips = anim.clips(kit.rig)


def tris(o):
    me = o.data
    me.calc_loop_triangles()
    return len(me.loop_triangles)


def slot_of(n):
    return n.split("_")[0].split(".")[0]


count = {}
for o in kit.parts:
    s = slot_of(o.name)
    count.setdefault(s, [0, 0])
    count[s][0] += 1
    count[s][1] += tris(o)
print("SLOT_PARTS", {k: v[0] for k, v in count.items()})
print("TRIS_PER_SLOT", {k: v[1] for k, v in count.items()})
print("BONES", [b.name for b in kit.rig.data.bones])
print("CLIPS", list(clips))
print("MATS", sorted(m.name for m in kit.mats.values()))

parts_mats = {o.name: sorted({m.name for m in o.data.materials if m and m.name != "outline"}) for o in kit.parts}
spec = {
    "versi": 1, "facing": "-Y blender (+Z glTF)", "tinggi_m": 1.7,
    "bones": lib.BONE_NAMES,
    "clips": {k: {"frames": v[0], "fps": anim.FPS} for k, v in clips.items()},
    "sit": {"root_z": anim.SIT_ROOT_Z, "kursi_seat_top": .49, "catatan": "turunkan/naikkan group karakter supaya root berada di root_z di atas lantai saat clip duduk"},
    "slots": {
        "HAIR": list(p_hair.HAIR), "FACE": list(p_face.FACE), "MOUTH": list(p_face.MOUTH), "FHAIR": list(p_face.FHAIR),
        "TOP": list(p_outfit.TOP), "BOTTOM": list(p_outfit.BOTTOM), "SHOES": list(p_outfit.SHOES), "ACC": list(p_acc.ACC),
        "BLUSH": ["BLUSH"],
    },
    "nama_objek": {"HAIR": "HAIR_<id> (bawah) + HAIRTOP_<id> (atas; sembunyikan jika topi)", "FACE": "FACE_<id>.eye_L|eye_R|brow (eye berpivot di pusat -> kedip = scale Z)",
                   "MOUTH": "MOUTH_<id>", "FHAIR": "FHAIR_<id>", "TOP": "TOP_<id>", "BOTTOM": "BOTTOM_<id>",
                   "SHOES": "SHOES_<id>", "ACC": "ACC_<id>", "BLUSH": "BLUSH", "BODY": "BODY (selalu tampil)"},
    "material_warna": lib.DEFAULT_COL,
    "material_slot": {"M_skin": "kulit", "M_hair": "rambut+alis+jenggot", "M_eye": "mata", "M_eyewhite": "kilau mata", "M_mouth": "mulut",
                      "M_blush": "pipi", "M_top": "warna utama atasan", "M_top2": "aksen/kerah atasan", "M_bottom": "bawahan",
                      "M_shoes": "sepatu", "M_shoes2": "sol/sepatu formal (tetap)", "M_acc": "aksesori kepala", "M_acc2": "detail gelap aksesori (tetap)",
                      "M_acc3": "aksesori badan (dasi/celemek/tas)"},
    "outline": {"material": "outline", "hex": lib.OUTLINE_HEX, "catatan": "hull terbalik di mesh yang sama; di app ganti ke MeshBasicMaterial navy"},
    "konflik": {"aksesori_topi": list(p_acc.HEAD_HAT), "topi_sembunyikan": "HAIRTOP_<gaya> (rambut tetap HAIR_<gaya> bagian bawah)",
                "grup_eksklusif_kepala": list(p_acc.HEAD_TOP), "aksesori_tak_boleh_dengan_rambut": {k: list(v) for k, v in p_acc.ACC_HAIR_CONFLICT.items()},
                "catatan": "topi cocok dgn semua rambut selama HAIRTOP_* disembunyikan; grup_eksklusif_kepala maks satu"},
    "warna": colors.spec(),
    "warna_tetap": colors.TETAP,
    "warna_catatan": "tiap kelompok = satu material M_* yang di-tint; tambahkan pemilih hex bebas. Preset boleh di luar palet.",
    "bagian_material": parts_mats,
    "presets": presets.PRESETS,
}
os.makedirs(OUT_DIR, exist_ok=True)
json.dump(spec, open(os.path.join(HERE, "kit_spec.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)

if "--glb" in sys.argv:
    bpy.ops.export_scene.gltf(filepath=OUT_GLB, export_format='GLB', export_apply=False, export_yup=True,
                              export_animation_mode='NLA_TRACKS')
    print("GLB", OUT_GLB, os.path.getsize(OUT_GLB))

# ---- lineup 11 karakter
for k, pr in presets.PRESETS.items():
    heads = [a for a in pr["acc"] if a in p_acc.HEAD_TOP]
    assert len(heads) <= 1, f"lebih dari satu aksesori kepala: {k}"
    for a in pr["acc"]:
        assert pr["hair_style"] not in p_acc.ACC_HAIR_CONFLICT.get(a, ()), f"konflik {a}/{pr['hair_style']}: {k}"


from char import make_character


chars = {}
for i, (k, pr) in enumerate(presets.PRESETS.items()):
    chars[k] = make_character(k, pr, (i - 5) * 1.25, 0)
    anim.apply(chars[k].rig, clips["idle"][1], 0)
print("KARAKTER", list(chars))

# ---- katalog: tiap part dipajang satu-satu, satu rak (baris) per slot, ditumpuk ke atas (lihat dari depan, numpad 1)
cat_col = bpy.data.collections.new("KATALOG"); bpy.context.scene.collection.children.link(cat_col)
bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children["KATALOG"]
for r, row in enumerate(catalog.ROWS):
    n = catalog.add_row(row, x0=0, y=24, z=r * 3.0)
    reg, zc, h, sp, ppm = catalog.ROWS[row]
    catalog.label(row.upper() + f"  ({n})", -(n * sp) / 2 - 1.2, 24, r * 3.0 + zc + h / 2, size=.3)
    print("KATALOG", row, n)
catalog.label("WARNA (pilihan palet per material)", -3.2, 24, len(catalog.ROWS) * 3.0 + .5, size=.3).data.align_x = 'LEFT'
catalog.add_palettes(x0=0, y=24, z=len(catalog.ROWS) * 3.0 - .3)
bpy.ops.wm.save_as_mainfile(filepath=OUT_BLEND)
