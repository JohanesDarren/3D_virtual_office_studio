"""Virtual Office toon kit -- core helpers.

Conventions (Blender side):
  * meters, Z up; exported glTF is Y up.
  * every item is built at the origin: pivot = bottom center, floor at z=0.
  * the FRONT of every item faces -Y (Blender front view, numpad 1).
  * one mesh object per item ``SM_<id>`` (several material slots) plus a separate
    inverted-hull outline object ``SM_<id>_outline`` parented to it, so the web app can
    hide or restyle outlines without touching the item.
  * materials are plain Principled BSDF with flat base colors (roughness 1, no textures);
    in Three.js swap them for MeshToonMaterial using the same color.
"""
import math
import bmesh
import bpy
from mathutils import Euler, Matrix, Vector

OUTLINE_T = 0.009          # outline thickness in meters
SOFT = 1.5                 # global edge-roundness multiplier (v3: softer, cuter read)
OUTLINE_HEX = "#4B4E63"    # soft slate, not black: keeps the pastel read calm

# calm pastel palette (v2). Names are the material contract: MAT_<name>.
PALETTE = {
    # wood & neutrals
    "wood_light": "#EAD7BF", "wood_mid": "#D4B48C", "wood_dark": "#A98466", "cork": "#E2C49C",
    "white": "#FBF8F3", "offwhite": "#F1ECE3", "grey_light": "#DADDE3", "grey": "#AEB4BE",
    "charcoal": "#6B7180", "black": "#4A4F5C",
    # pastel fabrics / paints
    "sage": "#B9D3B8", "mint": "#BFE6D8", "sky": "#BFDDF0", "lavender": "#CFC6E8",
    "blush": "#F2C4C0", "peach": "#F7CDB0", "butter": "#F6DFA1",
    "coral": "#EE9A8F", "blue": "#8FB3E8",
    # special
    "screen": "#A9D8F5", "leaf": "#8CC49A", "leaf_dark": "#6FAF84", "pot": "#E9B79A", "soil": "#8C6E5A",
    "metal": "#C9CED6", "glass": "#D6EEF7", "paper": "#FFFDF8", "water": "#BFE4F7", "lamp_glow": "#FFF0C2",
    # avatars: skin tones, hair, cheeks
    "skin_1": "#FBE3D2", "skin_2": "#F1C9A8", "skin_3": "#D9A07A", "skin_4": "#A8734F",
    "hair_brown": "#7A5646", "hair_dark": "#4A4354", "hair_blonde": "#EBCB8B", "hair_pink": "#E9A6BB",
    "hair_ginger": "#D98A5E", "cheek": "#F5A8A2",
}


def _lin(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return [(v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4) for v in c] + [1.0]


_mats = {}


def mat(name):
    """Get or create MAT_<name> from PALETTE (or the outline material)."""
    if name in _mats:
        return _mats[name]
    hexc = OUTLINE_HEX if name == "outline" else PALETTE[name]
    m = bpy.data.materials.new("MAT_" + name)
    m.use_nodes = True
    col = _lin(hexc)
    m.diffuse_color = col
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = col
    bsdf.inputs["Roughness"].default_value = 1.0
    bsdf.inputs["Metallic"].default_value = 0.0
    if name in ("screen", "lamp_glow"):
        bsdf.inputs["Emission Color"].default_value = col
        bsdf.inputs["Emission Strength"].default_value = 0.6
    if name == "outline":
        m.use_backface_culling = True
    m["hex"] = hexc
    _mats[name] = m
    return m


class Item:
    """Collects primitives into one bmesh; material per face via slot index."""

    def __init__(self, item_id):
        self.id = item_id
        self.bm = bmesh.new()
        self.slots = []
        self.no_outline = set()   # face indices skipped by the outline hull

    def _slot(self, m):
        if m not in self.slots:
            self.slots.append(m)
        return self.slots.index(m)

    def _finish(self, before, m, smooth, outline):
        idx = self._slot(m)
        new = [v for v in self.bm.verts if v not in before]
        faces = {f for v in new for f in v.link_faces}
        for f in faces:
            f.material_index = idx
            f.smooth = smooth
        if not outline:
            self.no_outline.update(faces)

    @staticmethod
    def _mtx(c, size, rot):
        return (Matrix.Translation(c) @ Euler([math.radians(a) for a in rot]).to_matrix().to_4x4()
                @ Matrix.Diagonal((size[0], size[1], size[2], 1)))

    # ---- primitives: c = CENTER of the shape, size = full extents
    @staticmethod
    def _soft_bevel(bm, edges, r):
        """Rounded edge: more segments on big radii so large shapes read soft, small parts stay cheap."""
        seg = 3 if r >= .025 else (2 if r >= .008 else 1)
        bmesh.ops.bevel(bm, geom=edges, offset=r, segments=seg, affect="EDGES", profile=.5, clamp_overlap=True)

    def box(self, c, size, m, bevel=.02, rot=(0, 0, 0), outline=True):
        before = set(self.bm.verts)
        ret = bmesh.ops.create_cube(self.bm, size=1.0, matrix=self._mtx(c, size, rot))
        r = min(bevel * SOFT, min(size) * .45)
        if r > .002:
            self._soft_bevel(self.bm, list({e for v in ret["verts"] for e in v.link_edges}), r)
        self._finish(before, m, False, outline)

    def cyl(self, c, d, h, m, seg=16, top=1.0, rot=(0, 0, 0), bevel=0.0, outline=True):
        """Cylinder/cone along local Z, d = (diameter_x, diameter_y). bevel rounds the two rims."""
        before = set(self.bm.verts)
        ret = bmesh.ops.create_cone(self.bm, cap_ends=True, cap_tris=False, segments=seg, radius1=.5,
                                    radius2=.5 * top, depth=1.0, matrix=self._mtx(c, (d[0], d[1], h), rot))
        r = min(bevel * SOFT, h * .45, min(d) * .2)
        if r > .002:
            rim = [e for e in {e for v in ret["verts"] for e in v.link_edges}
                   if len(e.link_faces) == 2 and abs(e.link_faces[0].normal.dot(e.link_faces[1].normal)) < .5]
            self._soft_bevel(self.bm, rim, r)
        self._finish(before, m, True, outline)

    def ball(self, c, size, m, seg=12, rot=(0, 0, 0), outline=True):
        before = set(self.bm.verts)
        bmesh.ops.create_uvsphere(self.bm, u_segments=seg, v_segments=max(6, seg // 2), radius=.5,
                                  matrix=self._mtx(c, size, rot))
        self._finish(before, m, True, outline)

    def stick(self, p0, p1, d, m, seg=8, top=1.0, outline=True):
        """Cylinder from point p0 to p1 with diameter d (legs, arms, stems)."""
        p0, p1 = Vector(p0), Vector(p1)
        v = p1 - p0
        q = v.to_track_quat("Z", "Y")
        mt = (Matrix.Translation((p0 + p1) / 2) @ q.to_matrix().to_4x4()
              @ Matrix.Diagonal((d, d, v.length, 1)))
        before = set(self.bm.verts)
        bmesh.ops.create_cone(self.bm, cap_ends=True, cap_tris=False, segments=seg, radius1=.5,
                              radius2=.5 * top, depth=1.0, matrix=mt)
        self._finish(before, m, True, outline)

    def place(self, fn, loc=(0, 0, 0), rz=0.0):
        """Build another item's geometry (``fn(Item)``) and merge it here, turned rz degrees about Z
        and moved to loc. Lets workstations reuse desk/monitor/prop builders."""
        sub = Item("_sub")
        fn(sub)
        noout = sub.bm.faces.layers.int.new("noout")
        for f in sub.bm.faces:
            f[noout] = 1 if f in sub.no_outline else 0
            f.material_index = self._slot(sub.slots[f.material_index])
        bmesh.ops.transform(sub.bm, verts=sub.bm.verts,
                            matrix=Matrix.Translation(loc) @ Matrix.Rotation(math.radians(rz), 4, "Z"))
        me = bpy.data.meshes.new("_tmp")
        sub.bm.to_mesh(me)
        sub.bm.free()
        before = set(self.bm.faces)
        self.bm.from_mesh(me)
        bpy.data.meshes.remove(me)
        lay = self.bm.faces.layers.int.get("noout")
        for f in self.bm.faces:
            if f not in before and lay is not None and f[lay]:
                self.no_outline.add(f)

    # ---- object creation
    def done(self, collection):
        bm = self.bm
        bm.normal_update()
        for lay in [l for l in bm.faces.layers.int.values() if l.name == "noout"]:   # place() bookkeeping only
            bm.faces.layers.int.remove(lay)
        # outline hull: copy of outlined faces, pushed out along vertex normals, flipped
        hull = bmesh.new()
        vmap = {}
        for f in bm.faces:
            if f in self.no_outline:
                continue
            vs = []
            for v in f.verts:
                if v not in vmap:
                    vmap[v] = hull.verts.new(v.co + v.normal * OUTLINE_T)
                vs.append(vmap[v])
            try:
                hull.faces.new(vs)
            except ValueError:
                pass
        bmesh.ops.reverse_faces(hull, faces=list(hull.faces))

        me = bpy.data.meshes.new("SM_" + self.id)
        bm.to_mesh(me)
        bm.free()
        for s in self.slots:
            me.materials.append(mat(s))
        ob = bpy.data.objects.new("SM_" + self.id, me)
        collection.objects.link(ob)

        hme = bpy.data.meshes.new("SM_" + self.id + "_outline")
        hull.to_mesh(hme)
        hull.free()
        hme.materials.append(mat("outline"))
        ho = bpy.data.objects.new("SM_" + self.id + "_outline", hme)
        collection.objects.link(ho)
        ho.parent = ob
        return ob


def tris(ob):
    ob.data.calc_loop_triangles()
    return len(ob.data.loop_triangles)
