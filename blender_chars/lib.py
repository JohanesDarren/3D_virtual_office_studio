"""JagoAI Characters -- helper inti kit karakter chibi.

Konvensi: karakter berdiri di z=0, MENGHADAP -Y (depan Blender; di glTF jadi +Z), kiri karakter = +X.
Tinggi total ~1,7 m. Satu objek mesh per part (beberapa slot material), outline navy = hull terbalik
di mesh yang sama (slot material "outline"). Part kulit-tubuh/pakaian di-skin rigid ke tulang;
potongan wajah kecil (mata/mulut) di-parent ke tulang `head` dengan pivot di pusatnya (bisa kedip).
"""
import bpy
import bmesh
import math
import colorsys
from mathutils import Matrix, Vector, Euler

OUT_T = .016
OUTLINE_HEX = "#1B1747"

# material kit (nama = kontrak dengan app; app boleh mengganti .color per nama)
DEFAULT_COL = {
    "M_skin": "#F0C09A", "M_hair": "#3A2415", "M_eye": "#2A1A12", "M_eyewhite": "#FFFFFF",
    "M_mouth": "#B5503E", "M_blush": "#F28BA8",
    "M_top": "#3F6FB5", "M_top2": "#F2F2EC", "M_bottom": "#3B4660", "M_shoes": "#F2F2EC", "M_shoes2": "#2A2E34",
    "M_acc": "#E5B93C", "M_acc2": "#2A2E34", "M_acc3": "#C9483F", "M_glass": "#BFDDEC",
}
ROUGH = {"M_skin": .75, "M_eye": .35, "M_eyewhite": .4, "M_glass": .1}

BONES = [
    # nama, kepala, ekor, induk
    ("root", (0, 0, 0), (0, 0, .12), None),
    ("hips", (0, 0, .46), (0, 0, .56), "root"),
    ("spine", (0, 0, .56), (0, 0, .96), "hips"),
    ("head", (0, 0, .96), (0, 0, 1.70), "spine"),
    ("arm_L", (.31, 0, .91), (.31, 0, .70), "spine"), ("fore_L", (.31, 0, .70), (.31, 0, .50), "arm_L"),
    ("arm_R", (-.31, 0, .91), (-.31, 0, .70), "spine"), ("fore_R", (-.31, 0, .70), (-.31, 0, .50), "arm_R"),
    ("thigh_L", (.12, 0, .46), (.12, 0, .30), "hips"), ("shin_L", (.12, 0, .30), (.12, 0, 0), "thigh_L"),
    ("thigh_R", (-.12, 0, .46), (-.12, 0, .30), "hips"), ("shin_R", (-.12, 0, .30), (-.12, 0, 0), "thigh_R"),
]
BONE_NAMES = [b[0] for b in BONES]


def hexrgb(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return [(v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4) for v in c] + [1.0]


def make_mat(name, hexcol, rough=.7, cull=False):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    col = hexrgb(hexcol)
    m.diffuse_color = col
    n = m.node_tree.nodes.get("Principled BSDF")
    if n:
        n.inputs["Base Color"].default_value = col
        n.inputs["Roughness"].default_value = rough
        n.inputs["Metallic"].default_value = 0
    if cull:
        m.use_backface_culling = True
    return m


class Ctx:
    """Satu karakter (atau kit): rig + material + koleksi. tag='' = kit default (nama material persis)."""

    def __init__(self, name="CHAR", tag="", colors=None, offset=(0, 0, 0)):
        self.name, self.tag, self.offset = name, tag, Vector(offset)
        self.colors = dict(DEFAULT_COL)
        if colors:
            self.colors.update(colors)
        self.mats = {}
        self.coll = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(self.coll)
        self.rig = make_rig(self, name)
        self.parts = []

    def m(self, name):
        if name not in self.mats:
            if name == "outline":
                self.mats[name] = make_mat("outline" + self.tag, OUTLINE_HEX, 1.0, cull=True)
            else:
                self.mats[name] = make_mat(name + self.tag, self.colors[name], ROUGH.get(name, .7))
        return self.mats[name]

    def part(self, name, bone="head", outline=True, skinned=True):
        return Part(self, name, bone, outline, skinned)


def make_rig(ctx, name):
    arm = bpy.data.armatures.new(name + "_arm")
    ob = bpy.data.objects.new(name + "_rig", arm)
    ctx.coll.objects.link(ob)
    ob.location = ctx.offset
    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    eb = {}
    for n, h, t, p in BONES:
        b = arm.edit_bones.new(n)
        b.head, b.tail = h, t
        if p:
            b.parent = eb[p]
        eb[n] = b
    bpy.ops.object.mode_set(mode='OBJECT')
    ob.select_set(False)
    return ob


class Part:
    def __init__(s, ctx, name, bone, outline, skinned):
        s.ctx, s.name, s.bone, s.outline, s.skinned = ctx, name, bone, outline, skinned
        s.bm = bmesh.new()
        s.dl = s.bm.verts.layers.deform.verify() if skinned else None
        s.slots = []

    # ---- internals
    def _slot(s, m):
        if m not in s.slots:
            s.slots.append(m)
        return s.slots.index(m)

    def _weights(s, bone):
        if isinstance(bone, str):
            return [(BONE_NAMES.index(bone), 1.0)]
        return [(BONE_NAMES.index(b), w) for b, w in bone]

    def _fin(s, before, m, bone, smooth):
        idx = s._slot(m)
        new = [v for v in s.bm.verts if v not in before]
        fs = {f for v in new for f in v.link_faces}
        for f in fs:
            f.material_index = idx
            f.smooth = smooth
        if s.dl is None:
            return
        w = s._weights(bone or s.bone)
        for v in new:
            for gi, wt in w:
                v[s.dl][gi] = wt

    # ---- primitif (koordinat karakter, pusat)
    def box(s, c, size, m, bone=None, r=.02, seg=2, rot=(0, 0, 0)):
        mt = (Matrix.Translation(c) @ Euler([math.radians(a) for a in rot]).to_matrix().to_4x4()
              @ Matrix.Diagonal((size[0], size[1], size[2], 1)))
        before = set(s.bm.verts)
        ret = bmesh.ops.create_cube(s.bm, size=1.0, matrix=mt)
        r = min(r, min(size) * .45)
        if r > .002:
            ed = list({e for v in ret['verts'] for e in v.link_edges})
            bmesh.ops.bevel(s.bm, geom=ed, offset=r, segments=seg, affect='EDGES', profile=.6, clamp_overlap=True)
        s._fin(before, m, bone, False)

    def sph(s, c, size, m, bone=None, seg=14, rot=(0, 0, 0)):
        mt = (Matrix.Translation(c) @ Euler([math.radians(a) for a in rot]).to_matrix().to_4x4()
              @ Matrix.Diagonal((size[0], size[1], size[2], 1)))
        before = set(s.bm.verts)
        bmesh.ops.create_uvsphere(s.bm, u_segments=seg, v_segments=max(5, seg // 2), radius=.5, matrix=mt)
        s._fin(before, m, bone, True)

    def cyl(s, c, d, h, m, bone=None, r2=1.0, seg=14, rot=(0, 0, 0)):
        """Silinder/kerucut sumbu Z lokal, pusat di c; d=(dx,dy)."""
        mt = (Matrix.Translation(c) @ Euler([math.radians(a) for a in rot]).to_matrix().to_4x4()
              @ Matrix.Diagonal((d[0], d[1], h, 1)))
        before = set(s.bm.verts)
        bmesh.ops.create_cone(s.bm, cap_ends=True, cap_tris=False, segments=seg, radius1=.5, radius2=.5 * r2,
                              depth=1.0, matrix=mt)
        s._fin(before, m, bone, False)

    def ring(s, c, R, t, m, bone=None, seg=16, sq=1.0):
        """Cincin tipis bidang XZ (normal Y), mis. rangka kacamata. sq = skala tinggi (oval)."""
        for i in range(seg):
            a = 2 * math.pi * (i + .5) / seg
            ln = 2 * R * math.sin(math.pi / seg) * 1.2
            p = (c[0] + R * math.cos(a), c[1], c[2] + R * math.sin(a) * sq)
            s.box(p, (ln, t, t), m, bone, r=.003, seg=1, rot=(0, -(math.degrees(a) + 90), 0))

    # ---- selesai -> objek
    def done(s, pivot=None, rig_parent_bone=None):
        ctx = s.ctx
        bm = s.bm
        if s.outline and len(bm.faces):
            bm.normal_update()
            ret = bmesh.ops.duplicate(bm, geom=list(bm.verts) + list(bm.edges) + list(bm.faces))
            nv = [g for g in ret['geom'] if isinstance(g, bmesh.types.BMVert)]
            nf = [g for g in ret['geom'] if isinstance(g, bmesh.types.BMFace)]
            bm.normal_update()
            sh = [v.co + v.normal * OUT_T for v in nv]
            for v, c in zip(nv, sh):
                v.co = c
            bmesh.ops.reverse_faces(bm, faces=nf)
            idx = s._slot("outline")
            for f in nf:
                f.material_index = idx
                f.smooth = True
        if pivot is not None:
            bmesh.ops.translate(bm, vec=-Vector(pivot), verts=list(bm.verts))
        me = bpy.data.meshes.new(s.name + ctx.tag)
        bm.to_mesh(me)
        bm.free()
        for sl in s.slots:
            me.materials.append(ctx.m(sl))
        ob = bpy.data.objects.new(s.name + ctx.tag, me)
        ctx.coll.objects.link(ob)
        rig = ctx.rig
        if s.skinned:
            for bn in BONE_NAMES:
                ob.vertex_groups.new(name=bn)
            md = ob.modifiers.new("Armature", 'ARMATURE')
            md.object = rig
            ob.parent = rig
        else:
            bn = rig_parent_bone or s.bone
            ob.parent = rig
            ob.parent_type = 'BONE'
            ob.parent_bone = bn
            b = rig.data.bones[bn]
            ob.matrix_parent_inverse = (b.matrix_local @ Matrix.Translation((0, b.length, 0))).inverted()
            if pivot is not None:
                ob.location = Vector(pivot)
        ctx.parts.append(ob)
        return ob
