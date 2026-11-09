"""Build the Virtual Office bean-buddy avatars.

  blender -b --factory-startup --python chars/build.py -- [--glb] [--render]

Outputs (relative to the project root):
  blend/vo_avatars.blend           COL_Avatar_<id> per character (armature + rigid parts) + COL_Context
  out/avatars/av_<id>.glb          one GLB per character, clips as glTF animations     (--glb)
  out/avatars_spec.json            ids, names, height, tris, bones, clips
  renders/avatars_lineup.png       all characters, front 3/4                           (--render)
  renders/avatars_clips_<n>.png    7 clips per sheet, each at its peak pose            (--render)
  renders/avatars_context.png      sitting + typing at the kit desk/chair              (--render)

Rig: 8 bones (root, hips, spine, head, arm_L/R, leg_L/R). Every part is a rigid mesh parented
to ONE bone (no skin weights), so Three.js plays the clips with plain node transforms.
Clips (24 fps, all loop): 28 clips, see CLIPS. Seated ones ("sit*", "type") lift the root so the
seat lands on the kit office chair (seat top z=0.47); put the avatar's root on the chair pivot.
"""
import json
import math
import os
import sys

import bpy
from mathutils import Euler, Matrix, Quaternion, Vector

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "kit"))
import lib    # noqa: E402
import parts  # noqa: E402

FPS = 24
TRI_BUDGET = 12000   # body ~4-5k + 10 expression faces + hand props (folded, never all shown)
args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []

# ---------------------------------------------------------------- characters (original designs)
BASE = dict(eyes="normal", mouth="smile", brows="normal", bottom="pants", tie=False, badge=False, accs=[],
            top2="white", acc="charcoal")
CHARS = [
    dict(id="pip", role="it", name="Pip", skin="skin_1", hair="hair_brown", hair_style="short", outfit="shirt",
         top="sky", pants="charcoal", shoes="black", tie=True, acc="blue", accs=["glasses"]),
    dict(id="mochi", role="creative", name="Mochi", skin="skin_2", hair="hair_dark", hair_style="bob", outfit="cardigan",
         top="lavender", bottom="skirt", pants="sage", shoes="coral", eyes="big", mouth="open", accs=["flower"]),
    dict(id="juno", role="content", name="Juno", skin="skin_3", hair="hair_ginger", hair_style="bun", outfit="tee", top="mint",
         pants="blue", shoes="peach", acc="coral", badge=True, brows="up"),
    dict(id="bento", role="content", name="Bento", skin="skin_4", hair="hair_dark", hair_style="curly", outfit="hoodie",
         top="butter", top2="peach", pants="charcoal", shoes="blue", eyes="happy", accs=["headphones"]),
    dict(id="kiko", role="creative", name="Kiko", skin="skin_1", hair="hair_pink", hair_style="short", outfit="tee", top="blush",
         pants="lavender", shoes="black", acc="sky", accs=["beanie"], mouth="open"),
    dict(id="sol", role="sales", name="Sol", skin="skin_2", hair="hair_blonde", hair_style="tuft", outfit="shirt", top="sage",
         pants="wood_dark", shoes="charcoal", acc="blue", badge=True, eyes="big"),
    dict(id="tavi", role="it", name="Tavi", skin="skin_3", hair="hair_dark", hair_style="buzz", outfit="polo", top="coral",
         pants="grey", shoes="blue", accs=["beard"]),
    dict(id="nara", role="hr", name="Nara", skin="skin_2", hair="lavender", brow="hair_dark", hair_style="hijab",
         outfit="dress", top="blush", pants="blush", shoes="coral", eyes="big", mouth="open"),
    dict(id="ozzy", role="content", name="Ozzy", skin="skin_1", hair="hair_ginger", hair_style="spiky", outfit="hoodie", top="sky",
         pants="charcoal", shoes="coral", accs=["freckles"], mouth="open"),
    dict(id="rumi", role="exec", name="Rumi", skin="skin_4", hair="hair_dark", hair_style="afro", outfit="blazer", top="coral",
         pants="black", shoes="black", eyes="big", accs=["earrings"]),
    dict(id="lumi", role="creative", name="Lumi", skin="skin_1", hair="hair_blonde", hair_style="long", outfit="sweater",
         top="peach", bottom="skirt", pants="blue", shoes="charcoal", acc="coral", accs=["bow"], eyes="big"),
    dict(id="dodo", role="finance", name="Dodo", skin="skin_2", hair="hair_brown", hair_style="buzz", outfit="vest", top="sky",
         top2="wood_mid", pants="charcoal", shoes="wood_dark", acc="black", accs=["glasses", "mustache"]),
    dict(id="wren", role="marketing", name="Wren", skin="skin_3", hair="hair_brown", hair_style="ponytail", outfit="tee",
         top="lavender", pants="charcoal", shoes="mint", acc="butter", badge=True),
    dict(id="zara", role="creative", name="Zara", skin="skin_4", hair="hair_pink", hair_style="twintails", outfit="hoodie",
         top="lavender", top2="blush", bottom="skirt", pants="charcoal", shoes="black", acc="white", eyes="happy"),
    dict(id="budi", role="sales", name="Budi", skin="skin_3", hair="hair_dark", hair_style="swoop", outfit="shirt", top="blue",
         pants="charcoal", shoes="black", tie=True, acc="charcoal"),
    dict(id="sari", role="hr", name="Sari", skin="skin_2", hair="sky", brow="hair_dark", hair_style="hijab",
         outfit="cardigan", top="butter", pants="blue", shoes="peach", acc="coral", badge=True),
    dict(id="hana", role="finance", name="Hana", skin="skin_1", hair="hair_dark", hair_style="bob", outfit="blazer", top="lavender",
         bottom="skirt", pants="charcoal", shoes="black", acc="coral", accs=["glasses"]),
    dict(id="kai", role="content", name="Kai", skin="skin_2", hair="hair_dark", hair_style="short", outfit="tee", top="sage",
         pants="blue", shoes="black", acc="coral", accs=["cap"], mouth="open"),
    dict(id="bima", role="it", name="Bima", skin="skin_4", hair="hair_dark", hair_style="buzz", outfit="sweater", top="sage",
         pants="wood_dark", shoes="charcoal", accs=["beard", "headphones"]),
    dict(id="ayu", role="marketing", name="Ayu", skin="skin_3", hair="hair_dark", hair_style="long", outfit="dress", top="coral",
         pants="coral", shoes="peach", accs=["flower"], eyes="big"),
    dict(id="theo", role="exec", name="Theo", skin="skin_1", hair="hair_blonde", hair_style="swoop", outfit="blazer",
         top="charcoal", pants="charcoal", shoes="black", tie=True, acc="coral", brows="up"),
    dict(id="fifi", role="creative", name="Fifi", skin="skin_2", hair="hair_ginger", hair_style="curly", outfit="tee", top="butter",
         top2="coral", bottom="skirt", pants="sky", shoes="coral", acc="sky", accs=["freckles", "bow"],
         mouth="open"),
    dict(id="raka", role="it", name="Raka", skin="skin_3", hair="hair_dark", hair_style="spiky", outfit="hoodie",
         top="charcoal", top2="mint", pants="black", shoes="mint", acc="mint", accs=["headphones"]),
    dict(id="gigi", role="finance", name="Gigi", skin="skin_4", hair="hair_brown", hair_style="ponytail", outfit="vest",
         top="blush", top2="lavender", pants="charcoal", shoes="black", acc="black", accs=["glasses", "earrings"],
         scarf="mint"),
]
for _c in CHARS:
    if _c["hair_style"] == "hijab":
        _c["hijab"] = True


# ---------------------------------------------------------------- rig + parts
class Part(lib.Item):
    """lib.Item that ends up rigidly parented to one bone."""

    def __init__(self, item_id, bone, col, arm):
        super().__init__(item_id)
        self.bone, self.col, self.arm = bone, col, arm
        self.collapse = None   # pivot: store the mesh folded to parts.HIDE size (toggled faces/props)

    def done_bone(self, outline=True):
        if not outline:
            self.no_outline.update(self.bm.faces)
        ob = self.done(self.col)
        hull = ob.children[0]
        if not hull.data.polygons:
            bpy.data.objects.remove(hull)
        if self.collapse is not None:   # fold mesh AND outline hull (hull offset must scale with it)
            pv = Vector(self.collapse)
            fold = Matrix.Translation(pv) @ Matrix.Scale(parts.HIDE, 4) @ Matrix.Translation(-pv)
            for o in [ob] + list(ob.children):
                o.data.transform(fold)
        ob.parent = self.arm
        ob.parent_type = "BONE"
        ob.parent_bone = self.bone
        bpy.context.view_layer.update()
        ob.matrix_world = Matrix.Identity(4)   # rest pose == build pose
        return ob


def build_char(c, scene):
    c = {**BASE, **c}
    col = bpy.data.collections.new("COL_Avatar_" + c["id"])
    scene.collection.children.link(col)
    arm = bpy.data.objects.new("ARM_av_" + c["id"], bpy.data.armatures.new("ARM_av_" + c["id"]))
    col.objects.link(arm)
    bpy.context.view_layer.objects.active = arm
    bpy.ops.object.mode_set(mode="EDIT")
    for name, h, t, par in parts.BONES + parts.face_bones() + parts.prop_bones(c):
        b = arm.data.edit_bones.new(name)
        b.head, b.tail = h, t
        b.roll = 0
        if par:
            b.parent = arm.data.edit_bones[par]
    bpy.ops.object.mode_set(mode="OBJECT")
    for pb in arm.pose.bones:
        pb.rotation_mode = "QUATERNION"

    made = []

    def p(name, bone):
        it = Part(f"av_{c['id']}_{name.lower()}", bone, col, arm)
        made.append(it)
        return it

    parts.body(p, c)
    parts.head(p, c)
    parts.hair(p, c)
    parts.accessories(p, c)
    parts.props(p, c, aim)
    meshes = [o for o in col.objects if o.type == "MESH" and not o.name.endswith("_outline")]
    return dict(cfg=c, col=col, arm=arm, meshes=meshes)


# ---------------------------------------------------------------- animation
_BONE = {n: (Vector(h), Vector(t)) for n, h, t, _p in parts.BONES}


def aim(bone, target):
    """Armature-space rotation that points `bone` (head->tail) at `target` (rest-pose coords).
    Arms: target = where the mitten should be; the short chibi arm stops ~0.25 m from the shoulder."""
    h, t = _BONE[bone]
    return (t - h).normalized().rotation_difference((Vector(target) - h).normalized())


def mix(a, b, s):
    return tuple(x + (y - x) * s for x, y in zip(a, b))


def rot(arm, bone, deg):
    """Rotation in ARMATURE axes (relative to parent) -> bone-local quaternion.
    `deg` is XYZ euler degrees or a Quaternion from aim(). +X tilts an upward bone forward (-Y);
    for downward bones (arms, legs) -X swings them forward; arm_R raises sideways with +Y, arm_L with -Y."""
    r = deg.to_matrix() if isinstance(deg, Quaternion) else Euler([math.radians(a) for a in deg]).to_matrix()
    m = arm.data.bones[bone].matrix_local.to_3x3()
    return (m.inverted() @ r @ m).to_quaternion()


def key(arm, frame, pose, root_z=0.0, root_y=0.0):
    """pose = {bone: (x, y, z) degrees | Quaternion, "face": expr, "props": {names}}; unlisted bones rest."""
    face = pose.get("face", "neutral")
    shown = set(pose.get("props", ()))
    for pb in arm.pose.bones:
        q = rot(arm, pb.name, pose.get(pb.name, (0, 0, 0)))
        pb.rotation_quaternion = q
        pb.keyframe_insert("rotation_quaternion", frame=frame)
    rb = arm.pose.bones["root"]
    # root bone points +Z: local Y = armature Z, local Z = armature -Y
    rb.location = (0, root_z, -root_y)
    rb.keyframe_insert("location", frame=frame)
    edit = bpy.context.preferences.edit
    old, edit.keyframe_new_interpolation_type = edit.keyframe_new_interpolation_type, "CONSTANT"
    for pb in arm.pose.bones:   # toggles: faces / props (see parts.EXPRESSIONS)
        if pb.name == "face_neutral":
            v = 1.0 if face == "neutral" else parts.HIDE
        elif pb.name.startswith("face_"):
            v = 1 / parts.HIDE if pb.name == "face_" + face else 1.0
        elif pb.name.startswith("prop_"):
            v = 1 / parts.HIDE if pb.name[5:] in shown else 1.0
        else:
            continue
        pb.scale = (v, v, v)
        pb.keyframe_insert("scale", frame=frame)
    edit.keyframe_new_interpolation_type = old


def wave(t, a, phase=0.0):
    return a * math.sin(2 * math.pi * (t + phase))


def pulse(t, k=1):
    """0 -> 1 -> 0 over the clip (k pulses); loops cleanly."""
    return .5 - .5 * math.cos(2 * math.pi * k * t)


def hold(t, a=.2, b=.8):
    """0 at the ends, eases to 1 and holds between a and b: for one-shot gestures that start/end at rest."""
    if t < a:
        return .5 - .5 * math.cos(math.pi * t / a)
    if t > b:
        return .5 - .5 * math.cos(math.pi * (1 - t) / (1 - b))
    return 1.0


SIT_Z = .12   # root lift so the hips sit on a 0.47 m seat
SIT_LEGS = {"leg_L": (-82, 0, 4), "leg_R": (-82, 0, -4)}
REST_L, REST_R = (.27, -.02, .47), (-.27, -.02, .47)   # mitten targets at rest


def _sit(pose):
    return {**SIT_LEGS, **pose}


def _base_clip(name):
    """Return (length_frames, fn(t in 0..1) -> (pose, root_z, root_y)). Every clip loops (t=0 == t=1)."""
    # ---------------------------------------------------------------- locomotion / base
    if name == "idle":
        return 48, lambda t: ({"spine": (wave(t, 2), 0, 0), "head": (wave(t, -2, .15), 0, wave(t, 3, .3)),
                               "arm_L": (0, 0, 4 + wave(t, 2)), "arm_R": (0, 0, -4 - wave(t, 2))},
                              wave(t, .006, .25) - .006, 0)
    if name == "walk":
        return 24, lambda t: ({"leg_L": (wave(t, -28), 0, 0), "leg_R": (wave(t, 28), 0, 0),
                               "arm_L": (wave(t, 24), 0, 6), "arm_R": (wave(t, -24), 0, -6),
                               "spine": (4, 0, wave(t, 5)), "head": (-3, 0, wave(t, -4)),
                               "hips": (0, 0, wave(t, -4))},
                              abs(math.sin(2 * math.pi * t)) * .03, 0)
    if name == "run":
        return 16, lambda t: ({"leg_L": (wave(t, -45), 0, 0), "leg_R": (wave(t, 45), 0, 0),
                               "arm_L": (wave(t, 50) - 15, -12, 0), "arm_R": (wave(t, -50) - 15, 12, 0),
                               "spine": (12, 0, wave(t, 8)), "head": (-8, 0, wave(t, -6)),
                               "hips": (0, 0, wave(t, -6))},
                              abs(math.sin(2 * math.pi * t)) * .07, 0)
    if name == "jump":
        def f(t):
            up = max(0.0, math.sin(math.pi * (t - .25) / .6)) if .25 < t < .85 else 0.0
            crouch = pulse(t * 4) if t < .25 else 0.0
            arms = up
            return ({"arm_L": (0, -150 * arms, 0), "arm_R": (0, 150 * arms, 0),
                     "leg_L": (-20 * up, 0, 6 * up), "leg_R": (-20 * up, 0, -6 * up),
                     "spine": (10 * crouch - 6 * up, 0, 0), "head": (-8 * up, 0, 0)},
                    up * .25 - crouch * .03, 0)
        return 24, f
    if name == "dance":
        return 32, lambda t: ({"hips": (0, 0, wave(t, 12)), "spine": (0, wave(t, 10), wave(t, -8)),
                               "head": (wave(t * 2, 6), wave(t, -10), 0),
                               "arm_L": (0, -100 - wave(t * 2, 40), 0), "arm_R": (0, 100 - wave(t * 2, 40, .5), 0),
                               "leg_L": (wave(t * 2, -15), 0, 0), "leg_R": (wave(t * 2, 15), 0, 0)},
                              pulse(t, 4) * .04, 0)
    # ---------------------------------------------------------------- social / gestures (standing)
    if name == "wave":
        return 24, lambda t: ({"arm_R": (-25, 135, wave(t, 16)), "arm_L": (0, 0, 4),
                               "head": (0, wave(t, -6), 4), "spine": (0, wave(t, -3), 0)},
                              abs(math.sin(math.pi * t)) * .01, 0)
    if name == "talk":
        return 48, lambda t: ({"arm_R": aim("arm_R", mix(REST_R, (-.3, -.3, .66), pulse(t, 2) * .8 + .2)),
                               "arm_L": aim("arm_L", mix(REST_L, (.32, -.25, .6), pulse(t + .25, 2) * .6)),
                               "head": (wave(t * 4, 4), wave(t * 2, 5), wave(t, 6)), "spine": (2, 0, wave(t, 4))},
                              0, 0)
    if name == "nod":
        return 24, lambda t: ({"head": (wave(t * 2, 14) + 4, 0, 0), "spine": (wave(t * 2, 2), 0, 0),
                               "arm_L": (0, 0, 4), "arm_R": (0, 0, -4)}, 0, 0)
    if name == "shake":
        return 24, lambda t: ({"head": (2, 0, wave(t * 2, 22)), "spine": (0, 0, wave(t * 2, -3)),
                               "arm_L": (0, 0, 4), "arm_R": (0, 0, -4)}, 0, 0)
    if name == "think":
        return 48, lambda t: ({"arm_R": aim("arm_R", (-.06, -.22, .86)),
                               "arm_L": aim("arm_L", (.02, -.2, .58)),
                               "head": (-6, 10 + wave(t, 4), 8), "spine": (0, wave(t, 2), 0)},
                              0, 0)
    if name == "phone":
        return 48, lambda t: ({"arm_R": aim("arm_R", (-.26, -.06, 1.0)),
                               "arm_L": aim("arm_L", mix(REST_L, (.3, -.25, .62), pulse(t, 2) * .7)),
                               "head": (wave(t * 2, 5), -10, wave(t, 8)), "spine": (0, wave(t, 3), wave(t, 6))},
                              0, 0)
    if name == "drink":
        return 48, lambda t: ({"arm_R": aim("arm_R", mix((-.26, -.2, .6), (-.05, -.24, .9), hold(t, .3, .6))),
                               "arm_L": (0, 0, 4), "head": (-10 * hold(t, .3, .6), 0, 0)}, 0, 0)
    if name == "stretch":
        return 48, lambda t: ({"arm_L": (12 * hold(t), -135 * hold(t), 0), "arm_R": (12 * hold(t), 135 * hold(t), 0),
                               "spine": (-8 * hold(t), wave(t, 12) * hold(t), 0),
                               "head": (-12 * hold(t), wave(t, 8) * hold(t), 0)},
                              hold(t) * .02, 0)
    if name == "cheer":
        return 24, lambda t: ({"arm_L": (0, -145 + wave(t * 2, 15), 0), "arm_R": (0, 145 + wave(t * 2, 15, .5), 0),
                               "head": (-10, 0, wave(t, 6)), "leg_L": (0, 0, 6), "leg_R": (0, 0, -6)},
                              abs(math.sin(2 * math.pi * t)) * .1, 0)
    if name == "clap":
        return 16, lambda t: ({"arm_L": aim("arm_L", mix((.14, -.24, .64), (.03, -.27, .64), pulse(t, 2))),
                               "arm_R": aim("arm_R", mix((-.14, -.24, .64), (-.03, -.27, .64), pulse(t, 2))),
                               "head": (wave(t * 2, 4) - 4, 0, 0)}, pulse(t, 2) * .01, 0)
    if name == "point":
        return 24, lambda t: ({"arm_R": aim("arm_R", (-.25, -.42, .82 + wave(t * 2, .02))),
                               "arm_L": (0, 0, 4), "head": (-4, 0, -8), "spine": (4, 0, -6)}, 0, 0)
    if name == "present":
        return 48, lambda t: ({"arm_R": aim("arm_R", mix((-.4, -.08, .62), (-.45, -.15, .78), pulse(t))),
                               "arm_L": aim("arm_L", mix(REST_L, (.28, -.26, .6), pulse(t, 2) * .7)),
                               "spine": (0, 0, 18), "head": (0, 0, wave(t, 25) + 5)}, 0, 0)
    if name == "shrug":
        return 24, lambda t: ({"arm_L": aim("arm_L", mix(REST_L, (.42, -.14, .62), hold(t))),
                               "arm_R": aim("arm_R", mix(REST_R, (-.42, -.14, .62), hold(t))),
                               "head": (0, 12 * hold(t), 0), "spine": (-3 * hold(t), 0, 0)}, hold(t) * .025, 0)
    if name == "bow":
        return 48, lambda t: ({"spine": (35 * hold(t, .3, .6), 0, 0), "head": (15 * hold(t, .3, .6), 0, 0),
                               "arm_L": (-10 * hold(t, .3, .6), 0, -6), "arm_R": (-10 * hold(t, .3, .6), 0, 6)},
                              0, 0)
    if name == "sad":
        return 48, lambda t: ({"head": (22, 0, wave(t, 5)), "spine": (8, 0, 0),
                               "arm_L": aim("arm_L", (.1, -.18, .5)), "arm_R": aim("arm_R", (-.1, -.18, .5))},
                              wave(t, .005) - .01, 0)
    if name == "facepalm":
        return 48, lambda t: ({"arm_R": aim("arm_R", mix(REST_R, (-.02, -.26, 1.02), hold(t, .25, .75))),
                               "head": (18 * hold(t, .25, .75), 0, wave(t * 2, 4) * hold(t, .25, .75)),
                               "spine": (6 * hold(t, .25, .75), 0, 0), "arm_L": (0, 0, 4)}, 0, 0)
    # ---------------------------------------------------------------- seated (root lifted onto a 0.47 seat)
    if name == "sit":
        return 48, lambda t: (_sit({"spine": (wave(t, 2) - 3, 0, 0), "arm_L": (-25, 0, 10), "arm_R": (-25, 0, -10),
                                    "head": (wave(t, -2, .2), 0, wave(t, 4, .4))}), SIT_Z, 0)
    if name == "type":
        return 24, lambda t: (_sit({"spine": (8, 0, 0), "head": (6 + wave(t, 1.5), 0, 0),
                                    "arm_L": (-78 + wave(2 * t, 6), 0, -14),
                                    "arm_R": (-78 + wave(2 * t, 6, .5), 0, 14)}), SIT_Z, 0)
    if name == "sit_talk":
        return 48, lambda t: (_sit({"arm_R": aim("arm_R", mix((-.28, -.25, .62), (-.32, -.32, .72), pulse(t, 2))),
                                    "arm_L": (-25, 0, 10), "spine": (0, 0, wave(t, 6)),
                                    "head": (wave(t * 4, 4), wave(t * 2, 6), wave(t, 8))}), SIT_Z, 0)
    if name == "sit_relax":
        return 48, lambda t: (_sit({"spine": (-14, 0, 0), "head": (-8 + wave(t, 2), 0, wave(t, 6)),
                                    "arm_L": aim("arm_L", (.16, .12, 1.12)), "arm_R": aim("arm_R", (-.16, .12, 1.12))}),
                              SIT_Z, 0)
    if name == "sit_sleep":
        return 48, lambda t: (_sit({"spine": (30 + wave(t, 2), 0, 0), "head": (28, 0, 12),
                                    "arm_L": aim("arm_L", (.05, -.32, .72)), "arm_R": aim("arm_R", (-.05, -.32, .72))}),
                              SIT_Z, 0)
    if name == "sit_drink":
        return 48, lambda t: (_sit({"arm_R": aim("arm_R", mix((-.26, -.26, .62), (-.05, -.24, .9), hold(t, .3, .6))),
                                    "arm_L": (-25, 0, 10), "head": (-10 * hold(t, .3, .6), 0, 0)}), SIT_Z, 0)
    if name == "sit_wave":
        return 24, lambda t: (_sit({"arm_R": (-25, 135, wave(t, 16)), "arm_L": (-25, 0, 10),
                                    "head": (0, wave(t, -6), 4)}), SIT_Z, 0)
    raise KeyError(name)


# ---------------------------------------------------------------- facial expression per clip
def blinks(base, at=(.35, .8)):
    return lambda t, n: "blink" if any(abs(t - a) * n < 1.6 for a in at) else base


def chatter(base="neutral", alt="talk", every=4):
    return lambda t, n: alt if int(round(t * n) // every) % 2 else base


def seq(*steps):
    """seq((t_end, expr), ...) -> expression by time."""
    def f(t, n):
        for end, e in steps:
            if t < end:
                return e
        return steps[-1][1]
    return f


FACES = {
    "idle": blinks("neutral"), "walk": blinks("neutral", (.4,)), "run": blinks("focus", (.5,)),
    "jump": seq((.25, "focus"), (.85, "happy"), (1, "neutral")), "dance": lambda t, n: "happy",
    "wave": lambda t, n: "happy", "talk": chatter(), "nod": seq((.1, "neutral"), (1, "happy")),
    "shake": lambda t, n: "sad", "think": blinks("think", (.6,)), "phone": chatter(),
    "drink": seq((.3, "neutral"), (.62, "blink"), (.85, "happy"), (1, "neutral")),
    "stretch": seq((.2, "neutral"), (.8, "yawn"), (1, "blink")),
    "cheer": lambda t, n: "happy", "clap": lambda t, n: "happy", "point": lambda t, n: "surprised",
    "present": chatter("happy"), "shrug": seq((.15, "neutral"), (1, "think")),
    "bow": seq((.25, "neutral"), (.75, "blink"), (1, "happy")), "sad": blinks("sad", (.5,)),
    "facepalm": seq((.22, "surprised"), (.75, "blink"), (1, "sad")),
    "sit": blinks("neutral"), "type": blinks("focus", (.5,)), "sit_talk": chatter(),
    "sit_relax": blinks("happy", ()), "sit_sleep": lambda t, n: "sleep",
    "sit_drink": seq((.3, "neutral"), (.62, "blink"), (.85, "happy"), (1, "neutral")),
    "sit_wave": lambda t, n: "happy",
}
PROPS_IN = {"drink": {"mug"}, "sit_drink": {"mug"}, "phone": {"phone"}}


# ---------------------------------------------------------------- role work clips (props + own faces)
def _type_arms(t, k=4, amp=7):
    return {"arm_L": (-78 + wave(k * t, amp), 0, -14), "arm_R": (-78 + wave(k * t, amp, .5), 0, 14)}


def _scribble(base, t, k=6, r=.015):
    return (base[0] + r * math.cos(2 * math.pi * k * t), base[1], base[2] + r * .6 * math.sin(4 * math.pi * k * t))


def _work(name):
    if name == "work_code":         # IT: fast typing, stop to think, "aha!", back to it
        def f(t):
            think = hold(t, .48, .7) if .4 < t < .78 else 0.0
            p = _sit({**_type_arms(t, 6), "spine": (12 - 6 * think, 0, 0),
                      "head": (10 - 16 * think + wave(t * 8, 1.5), 8 * think, wave(t, 4))})
            if think > 0:
                p["arm_R"] = aim("arm_R", mix((-.12, -.32, .72), (-.06, -.22, .86), think))
            p["face"] = seq((.45, "focus"), (.7, "think"), (.8, "surprised"), (1, "happy"))(t, 48)
            if p["face"] == "focus" and abs(t - .2) * 48 < 1.6:
                p["face"] = "blink"
            return p, SIT_Z, 0
        return 48, f
    if name == "work_debug":        # IT: stuck -> scratch head -> fix -> tiny celebration
        def f(t):
            sc = hold(t, .3, .55) if .22 < t < .62 else 0.0
            yay = hold(t, .82, .95) if t > .75 else 0.0
            p = _sit({**_type_arms(t, 3, 4), "spine": (10, 0, wave(t, 4)), "head": (8 - 12 * sc, -8 * sc, 0)})
            if sc > 0:
                p["arm_R"] = aim("arm_R", mix((-.12, -.32, .72), (-.27, -.04, 1.0 + wave(t * 8, .02)), sc))
            if yay > 0:
                p["arm_L"] = (0, -140 * yay, 0)
                p["arm_R"] = (0, 140 * yay, 0)
                p["head"] = (-10 * yay, 0, 0)
            p["face"] = seq((.22, "focus"), (.62, "think"), (.75, "surprised"), (1, "happy"))(t, 48)
            return p, SIT_Z + yay * .02, 0
        return 48, f
    if name == "work_paint":        # creative: standing at an easel, brush strokes, palette in hand
        def f(t):
            stroke = (-.15 + .08 * math.cos(4 * math.pi * t), -.4, .75 + .07 * math.sin(4 * math.pi * t))
            back = hold(t, .82, .95) if t > .78 else 0.0
            p = {"arm_R": aim("arm_R", mix(stroke, (-.25, -.25, .6), back)),
                 "arm_L": aim("arm_L", (.22, -.25, .6)),
                 "spine": (4 - 8 * back, 0, wave(t, 6)), "head": (-2 - 6 * back, wave(t, 8), wave(t, 6)),
                 "props": {"brush", "palette"}}
            p["face"] = "happy" if back > .3 else blinks("focus", (.4,))(t, 48)
            return p, 0, .03 * back
        return 48, f
    if name == "work_draw":         # creative: stylus on a tablet at the desk
        def f(t):
            p = _sit({"arm_R": aim("arm_R", _scribble((-.05, -.36, .72), t, 3, .03)),
                      "arm_L": aim("arm_L", (.1, -.32, .72)), "spine": (10, 0, 0),
                      "head": (14 + wave(t * 2, 2), 0, wave(t, 5)), "props": {"stylus"}})
            p["face"] = seq((.85, "focus"), (1, "happy"))(t, 48)
            if p["face"] == "focus" and abs(t - .45) * 48 < 1.6:
                p["face"] = "blink"
            return p, SIT_Z, 0
        return 48, f
    if name == "work_photo":        # content: raise camera, frame the shot, click, check, smile
        def f(t):
            up = hold(t, .2, .65) if t < .8 else 0.0
            click = 1.0 if .44 < t < .48 else 0.0
            p = {"arm_R": aim("arm_R", mix((-.27, -.2, .6), (-.06, -.32, .98), up)),
                 "arm_L": aim("arm_L", mix(REST_L, (.08, -.3, .96), up)),
                 "spine": (6 * up + 3 * click, 0, wave(t, 4) * up), "head": (-2 * up, 0, 0),
                 "leg_L": (-6 * up, 0, 4), "leg_R": (4 * up, 0, -4), "props": {"camera"}}
            p["face"] = seq((.2, "neutral"), (.44, "focus"), (.5, "surprised"), (.66, "focus"), (1, "happy"))(t, 48)
            return p, -.02 * up, 0
        return 48, f
    if name == "work_podcast":      # content: seated, leaning into the mic, talking with the hands
        def f(t):
            p = _sit({"arm_R": aim("arm_R", mix((-.28, -.25, .62), (-.32, -.32, .74), pulse(t, 3))),
                      "arm_L": aim("arm_L", mix((.2, -.3, .62), (.26, -.3, .7), pulse(t + .3, 2))),
                      "spine": (10, 0, wave(t, 5)), "head": (6 + wave(t * 4, 3), wave(t * 2, 5), wave(t, 6))})
            p["face"] = "happy" if .66 < t < .78 else chatter()(t, 48)
            return p, SIT_Z, 0
        return 48, f
    if name == "work_brainstorm":   # marketing: scribble a sticky note, stick it on the wall, step back
        def f(t):
            reach = hold(t, .42, .6) if .32 < t < .7 else 0.0
            look = hold(t, .78, .95) if t > .7 else 0.0
            pad_r = _scribble((-.02, -.3, .64), t, 5, .015)
            p = {"arm_R": aim("arm_R", mix(pad_r, (-.15, -.45, .95), reach)),
                 "arm_L": aim("arm_L", (.14, -.26, .62)),
                 "spine": (-4 * reach - 4 * look, 0, 0), "head": (10 * (1 - reach) - 14 * reach - 10 * look, 0,
                                                                   wave(t, 6) * look),
                 "props": {"note", "notepad"}}
            p["face"] = seq((.32, "focus"), (.7, "neutral"), (.8, "think"), (1, "happy"))(t, 48)
            return p, .02 * reach, .04 * look
        return 48, f
    if name == "work_pitch":        # marketing: pitch an idea: present, point, talk, big smile
        def f(t):
            pt = hold(t, .45, .65) if .35 < t < .75 else 0.0
            p = {"arm_R": aim("arm_R", mix(mix((-.4, -.08, .62), (-.45, -.15, .78), pulse(t, 2)),
                                           (-.25, -.42, .85), pt)),
                 "arm_L": aim("arm_L", mix(REST_L, (.3, -.28, .62), pulse(t + .25, 2) * .8)),
                 "spine": (0, 0, 16 * (1 - pt)), "head": (wave(t * 4, 3), 0, wave(t, 20) * (1 - pt) + 5)}
            p["face"] = "surprised" if pt > .5 else ("happy" if t > .85 else chatter("happy")(t, 48))
            return p, 0, 0
        return 48, f
    if name == "work_calc":         # finance: tap the calculator, write it down
        def f(t):
            p = _sit({"arm_L": aim("arm_L", (.13, -.33, .72 + .02 * pulse(t, 8))),
                      "arm_R": aim("arm_R", _scribble((-.1, -.34, .72), t, 4, .02)),
                      "spine": (12, 0, 0), "head": (16, 0, wave(t, 10)), "props": {"pen"}})
            p["face"] = seq((.8, "focus"), (.9, "surprised"), (1, "happy"))(t, 48)
            if p["face"] == "focus" and abs(t - .4) * 48 < 1.6:
                p["face"] = "blink"
            return p, SIT_Z, 0
        return 48, f
    if name == "work_interview":    # HR: clipboard, nodding along, taking notes, chatting
        def f(t):
            p = _sit({"arm_L": aim("arm_L", (.08, -.3, .7)),
                      "arm_R": aim("arm_R", _scribble((-.06, -.3, .72), t, 4, .012)),
                      "spine": (4, 0, 0), "head": (wave(t * 3, 8) + 2, 0, wave(t, 6)),
                      "props": {"clipboard", "pen"}})
            p["face"] = "happy" if .45 < t < .58 else chatter("neutral", "talk", 6)(t, 48)
            return p, SIT_Z, 0
        return 48, f
    if name == "work_call":         # sales/support: headset call, typing notes, gesturing, upbeat
        def f(t):
            p = _sit({**_type_arms(t, 4, 5), "spine": (6, 0, wave(t, 4)),
                      "head": (wave(t * 3, 5), wave(t * 2, 6), wave(t, 8)), "props": {"headset"}})
            g = pulse(t, 2) if t < .5 else 0.0
            if g > 0:
                p["arm_R"] = aim("arm_R", mix((-.14, -.32, .72), (-.32, -.3, .72), g))
            p["face"] = "happy" if .75 < t < .85 else chatter()(t, 48)
            return p, SIT_Z, 0
        return 48, f
    if name == "work_sign":         # exec: read the document, sign with a flourish, satisfied
        def f(t):
            sign = hold(t, .35, .65) if .25 < t < .72 else 0.0
            fl = (-.12 + .12 * min(1, max(0, (t - .3) / .4)), -.34, .72 + .015 * math.sin(10 * math.pi * t))
            p = _sit({"arm_R": aim("arm_R", mix((-.14, -.3, .7), fl, sign)),
                      "arm_L": aim("arm_L", (.1, -.32, .72)), "spine": (8 - 10 * (t > .8), 0, 0),
                      "head": (14 - 20 * (t > .8), 0, wave(t, 8) * (t < .25)), "props": {"pen"}})
            p["face"] = seq((.25, "think"), (.72, "focus"), (.8, "neutral"), (1, "happy"))(t, 48)
            return p, SIT_Z, 0
        return 48, f
    raise KeyError(name)


ROLE_CLIPS = {"it": ["work_code", "work_debug"], "creative": ["work_paint", "work_draw"],
              "content": ["work_photo", "work_podcast"], "marketing": ["work_brainstorm", "work_pitch"],
              "finance": ["work_calc"], "hr": ["work_interview"], "sales": ["work_call"], "exec": ["work_sign"]}
WORK_CLIPS = [c for v in ROLE_CLIPS.values() for c in v]


def clip_frames(name):
    """(frames, fn(t) -> (pose, root_z, root_y)); pose carries "face" and "props" for the toggles."""
    if name in WORK_CLIPS:
        return _work(name)
    n, fn = _base_clip(name)

    def g(t):
        pose, rz, ry = fn(t)
        pose = dict(pose)
        pose.setdefault("face", FACES.get(name, lambda t, n: "neutral")(t, n))
        pose.setdefault("props", PROPS_IN.get(name, set()))
        return pose, rz, ry
    return n, g


CLIPS = ["idle", "walk", "run", "jump", "dance",
         "wave", "talk", "nod", "shake", "think", "phone", "drink", "stretch", "cheer", "clap", "point",
         "present", "shrug", "bow", "sad", "facepalm",
         "sit", "type", "sit_talk", "sit_relax", "sit_sleep", "sit_drink", "sit_wave"]
PEAK = {"jump": .55, "drink": .45, "sit_drink": .45, "bow": .45, "facepalm": .5, "stretch": .5, "shrug": .5,
        "clap": .25, "cheer": .25, "sad": .25, "run": .25, "walk": .25, "dance": .2,
        "work_code": .2, "work_debug": .4, "work_paint": .3, "work_draw": .3, "work_photo": .46,
        "work_podcast": .3, "work_brainstorm": .5, "work_pitch": .55, "work_calc": .3, "work_interview": .3,
        "work_call": .2, "work_sign": .5}   # sheet sample point


def animate(arm, clips):
    arm.animation_data_create()
    for name in clips:
        n, fn = clip_frames(name)
        act = bpy.data.actions.new(f"{arm.name}_{name}")
        arm.animation_data.action = act
        step = 2   # every 2nd frame: keeps blinks / talk flaps crisp
        for f in list(range(0, n, step)) + [n]:
            pose, rz, ry = fn(f / n)
            key(arm, f + 1, pose, rz, ry)
        tr = arm.animation_data.nla_tracks.new()
        tr.name = name
        tr.strips.new(name, 1, act)
        tr.mute = True
        arm.animation_data.action = None
    for pb in arm.pose.bones:   # back to rest
        pb.rotation_quaternion = (1, 0, 0, 0)
        pb.location = (0, 0, 0)
        pb.scale = (1, 1, 1)


def solo(arm, clip):
    for tr in arm.animation_data.nla_tracks:
        tr.mute = tr.name != clip


def step_toggles(path):
    """Patch the GLB so face_/prop_ scale channels use STEP interpolation (no in-between giant frames)."""
    import struct
    with open(path, "rb") as fh:
        data = fh.read()
    jlen = struct.unpack_from("<I", data, 12)[0]
    doc = json.loads(data[20:20 + jlen])
    rest = data[20 + jlen:]
    names = [n.get("name", "") for n in doc.get("nodes", [])]
    for an in doc.get("animations", []):
        for ch in an["channels"]:
            tg = ch["target"]
            if tg["path"] == "scale" and names[tg["node"]].startswith(("face_", "prop_")):
                an["samplers"][ch["sampler"]]["interpolation"] = "STEP"
    js = json.dumps(doc, separators=(",", ":")).encode()
    js += b" " * (-len(js) % 4)
    out = struct.pack("<III", 0x46546C67, 2, 12 + 8 + len(js) + len(rest)) + struct.pack("<II", len(js),
                                                                                      0x4E4F534A) + js + rest
    with open(path, "wb") as fh:
        fh.write(out)


# ---------------------------------------------------------------- main
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.render.fps = FPS
chars = [build_char(c, scene) for c in CHARS]
for ch in chars:
    ch["clips"] = CLIPS + ROLE_CLIPS[ch["cfg"]["role"]]
    animate(ch["arm"], ch["clips"])

spec = {"version": 1, "units": "meters", "up": "+Z blender / +Y glTF", "front": "-Y blender / +Z glTF",
        "rig": {"bones": [b[0] for b in parts.BONES], "skinning": "none (rigid parts bone-parented)",
                "toggles": "face_<expr> / prop_<name> bones switch meshes via scale; scale keys are STEP"},
        "expressions": parts.EXPRESSIONS,
        "clips": {n: {"frames": clip_frames(n)[0], "fps": FPS, "loop": True,
                      "seated": n.startswith("sit") or n == "type" or n in ("work_code", "work_debug", "work_draw",
                                                                            "work_podcast", "work_calc",
                                                                            "work_interview", "work_call",
                                                                            "work_sign")}
                  for n in CLIPS + WORK_CLIPS},
        "roles": ROLE_CLIPS,
        "sit": {"seat_top_z": .47, "root_lift": SIT_Z, "note": "place root on the chair pivot, facing chair front"},
        "outline": {"object_suffix": "_outline", "hex": lib.OUTLINE_HEX, "thickness_m": lib.OUTLINE_T},
        "avatars": []}
over = []
for ch in chars:
    t = sum(lib.tris(o) for o in ch["meshes"])
    hi = max((o.matrix_world @ Vector(v)).z for o in ch["meshes"] for v in o.bound_box)
    lo = min((o.matrix_world @ Vector(v)).z for o in ch["meshes"] for v in o.bound_box)
    if t > TRI_BUDGET:
        over.append((ch["cfg"]["id"], t))
    spec["avatars"].append({"id": ch["cfg"]["id"], "name": ch["cfg"]["name"], "file": f"av_{ch['cfg']['id']}.glb",
                            "role": ch["cfg"]["role"], "work_clips": ROLE_CLIPS[ch["cfg"]["role"]],
                            "props": parts.prop_names(ch["cfg"]),
                            "height_m": round(hi, 3), "min_z": round(lo, 3), "tris": t,
                            "parts": len(ch["meshes"])})
os.makedirs(os.path.join(ROOT, "out", "avatars"), exist_ok=True)
with open(os.path.join(ROOT, "out", "avatars_spec.json"), "w", encoding="utf-8") as f:
    json.dump(spec, f, indent=1)
for a in spec["avatars"]:
    print("AVATAR", a["id"], "tris", a["tris"], "h", a["height_m"], "minz", a["min_z"], "parts", a["parts"])
print("OVER_BUDGET", over)

if "--glb" in args:
    for ch in chars:
        for tr in ch["arm"].animation_data.nla_tracks:
            tr.mute = False
        bpy.ops.object.select_all(action="DESELECT")
        ch["arm"].select_set(True)
        for o in ch["col"].objects:
            o.select_set(True)
        path = os.path.join(ROOT, "out", "avatars", f"av_{ch['cfg']['id']}.glb")
        bpy.ops.export_scene.gltf(filepath=path, export_format="GLB", use_selection=True, export_yup=True,
                                  export_animations=True, export_animation_mode="NLA_TRACKS",
                                  export_force_sampling=True, export_apply=False)
        step_toggles(path)
        print("GLB", path, os.path.getsize(path))
        for tr in ch["arm"].animation_data.nla_tracks:
            tr.mute = True

# ---------------------------------------------------------------- lineup layout + context props
SPACING, PER_SHEET = .9, 6
for i, ch in enumerate(chars):
    ch["arm"].location.x = (i % PER_SHEET - (PER_SHEET - 1) / 2) * SPACING
    ch["arm"].rotation_euler.z = math.radians(-20)  # 3/4 turn for preview sheets (GLBs export earlier, unrotated)
    solo(ch["arm"], "idle")

ctx = bpy.data.collections.new("COL_Context")
scene.collection.children.link(ctx)
sys.path.insert(0, os.path.join(ROOT, "kit"))
import items  # noqa: E402

props = {}
for pid in ("desk", "office_chair", "monitor", "laptop"):
    it = lib.Item("ctx_" + pid)
    items.REGISTRY[pid]["fn"](it)
    props[pid] = it.done(ctx)
ctx.hide_render = True
os.makedirs(os.path.join(ROOT, "blend"), exist_ok=True)
scene.frame_set(1)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT, "blend", "vo_avatars.blend"))
print("SAVED blend")

if "--render" in args:
    scene.render.engine = "BLENDER_WORKBENCH"
    sh = scene.display.shading
    sh.light = "FLAT"
    sh.color_type = "MATERIAL"
    sh.show_backface_culling = True
    scene.view_settings.view_transform = "Standard"
    scene.world = bpy.data.worlds.new("W")
    scene.world.color = (.96, .95, .93)
    cam = bpy.data.objects.new("CAM_Preview", bpy.data.cameras.new("CAM_Preview"))
    scene.collection.objects.link(cam)
    cam.data.type = "ORTHO"
    scene.camera = cam
    os.makedirs(os.path.join(ROOT, "renders"), exist_ok=True)

    def shoot(path, target, scale, res, tilt=80, yaw=-18):
        cam.rotation_euler = (math.radians(tilt), 0, math.radians(yaw))
        cam.data.ortho_scale = scale
        d = cam.rotation_euler.to_matrix() @ Vector((0, 0, 1))
        cam.location = Vector(target) + d * 30
        scene.render.resolution_x, scene.render.resolution_y = res
        scene.render.filepath = path
        bpy.ops.render.render(write_still=True)

    labels = []

    def label(text, x, y):
        bpy.ops.object.text_add(location=(x, y, -.1))
        lb = bpy.context.active_object
        lb.data.body, lb.data.size, lb.data.align_x = text, .12, "CENTER"
        lb.data.materials.append(lib.mat("charcoal"))
        lb.rotation_euler.x = math.radians(80)
        labels.append(lb)

    # 1. lineup sheets (idle, frame 1), PER_SHEET characters each
    scene.frame_set(1)
    w = PER_SHEET * SPACING + .4
    for s0 in range(0, len(chars), PER_SHEET):
        group = chars[s0:s0 + PER_SHEET]
        for ch in chars:
            ch["col"].hide_render = ch not in group
        for lb in labels:
            bpy.data.objects.remove(lb)
        labels.clear()
        for ch in group:
            label(ch["cfg"]["name"], ch["arm"].location.x, -.5)
        n = s0 // PER_SHEET + 1
        shoot(os.path.join(ROOT, "renders", f"avatars_lineup_{n}.png"), (0, 0, .62), w,
              (1800, int(1800 * 1.75 / w)), yaw=0)
        print("RENDER lineup", n)

    # 2. clip sheets: 7 clips per sheet, each on a different character, sampled at the clip's PEAK
    F = 101
    per = 7
    sheet = [(c, chars[i % len(chars)]) for i, c in enumerate(CLIPS)]
    for role, rc in ROLE_CLIPS.items():   # k-th clip of a role -> k-th character with that role
        crew = [ch for ch in chars if ch["cfg"]["role"] == role]
        sheet += [(c, crew[k % len(crew)]) for k, c in enumerate(rc)]
    for s0 in range(0, len(sheet), per):
        for lb in labels:
            bpy.data.objects.remove(lb)
        labels.clear()
        for ch in chars:
            ch["col"].hide_render = True
        group = sheet[s0:s0 + per]
        for i, (clip, ch) in enumerate(group):
            ch["col"].hide_render = False
            solo(ch["arm"], clip)
            n = clip_frames(clip)[0]
            for tr in ch["arm"].animation_data.nla_tracks:   # shift so frame F shows this clip's peak
                tr.strips[0].frame_start_ui = F - round(PEAK.get(clip, .3) * n)
            ch["arm"].location.x = (i - (per - 1) / 2) * 1.0
            label(clip.replace("work_", "") + (f" ({ch['cfg']['role']})" if clip in WORK_CLIPS else ""),
                  ch["arm"].location.x, -.5)
        scene.frame_set(F)
        k = s0 // per + 1
        shoot(os.path.join(ROOT, "renders", f"avatars_clips_{k}.png"), (0, 0, .7), per + .4,
              (2000, int(2000 * 1.9 / (per + .4))), yaw=0)
        print("RENDER clips", k)
    for ch in chars:
        for tr in ch["arm"].animation_data.nla_tracks:
            tr.strips[0].frame_start_ui = 1

    # 3. context: typing at desk + sitting on chair
    for lb in labels:
        bpy.data.objects.remove(lb)
    for ch in chars:
        ch["col"].hide_render = True
    ctx.hide_render = False
    typist, sitter = chars[0], chars[1]
    for ch, clip, x in ((typist, "type", -.5), (sitter, "sit", .9)):
        ch["col"].hide_render = False
        solo(ch["arm"], clip)
        ch["arm"].location = (x, 0, 0)
        ch["arm"].rotation_euler.z = 0
    props["office_chair"].location = (-.5, .02, 0)
    props["desk"].location = (-.5, -.62, 0)
    props["desk"].rotation_euler.z = math.pi        # desk front faces the typist
    props["laptop"].location = (-.5, -.5, .75)
    props["laptop"].rotation_euler.z = math.pi
    props["monitor"].location = (-.15, -.85, .75)
    props["monitor"].rotation_euler.z = math.pi
    chair2 = props["office_chair"].copy()
    ctx.objects.link(chair2)
    hull2 = props["office_chair"].children[0].copy()
    ctx.objects.link(hull2)
    hull2.parent = chair2
    chair2.location = (.9, .02, 0)
    scene.frame_set(7)
    shoot(os.path.join(ROOT, "renders", "avatars_context.png"), (.2, -.3, .6), 3.4, (1600, 1100), tilt=70, yaw=-55)
    print("RENDER context")
