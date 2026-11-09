"""Clip animasi kit karakter (NLA track per clip). Rotasi dinyatakan di sumbu DUNIA (derajat), dikonversi ke
lokal tulang. Karakter menghadap -Y: rotasi X negatif pada tulang menggantung = ayun ke DEPAN.
Rumus: lokal = R_rest^-1 @ R_dunia @ R_rest.
"""
import bpy
import math
from mathutils import Euler, Vector, Quaternion

FPS = 24
# tinggi akar saat duduk (root naik ke atas lantai); dicatat di kit_spec.json
SIT_ROOT_Z = .20
SIT_HIPS_DZ = -.16


def _rest3(rig, bn):
    return rig.data.bones[bn].matrix_local.to_3x3()


def pose(rig, bn, rx=0, ry=0, rz=0, loc=None, f=None):
    pb = rig.pose.bones[bn]
    R = _rest3(rig, bn)
    Rw = Euler((math.radians(rx), math.radians(ry), math.radians(rz)), 'XYZ').to_matrix()
    pb.rotation_mode = 'QUATERNION'
    pb.rotation_quaternion = (R.inverted() @ Rw @ R).to_quaternion()
    pb.keyframe_insert("rotation_quaternion", frame=f)
    if loc is not None:
        pb.location = R.inverted() @ Vector(loc)
        pb.keyframe_insert("location", frame=f)


def _reset(rig, f):
    for pb in rig.pose.bones:
        pose(rig, pb.name, 0, 0, 0, loc=(0, 0, 0), f=f)


def key(rig, f, **b):
    """b: nama_tulang=(rx,ry,rz) atau (rx,ry,rz,(lx,ly,lz)). Tulang lain di-reset ke 0."""
    for pb in rig.pose.bones:
        v = b.get(pb.name, (0, 0, 0))
        loc = v[3] if len(v) > 3 else (0, 0, 0)
        pose(rig, pb.name, v[0], v[1], v[2], loc=loc, f=f)


def _clip(rig, name, n, fn, loop=True):
    ad = rig.animation_data_create()
    act = bpy.data.actions.new(name)
    ad.action = act
    frames = sorted(set(list(range(1, n + 1, max(1, n // 12))) + [n]))
    for f in frames:
        t = (f - 1) / (n - 1) if n > 1 else 0
        key(rig, f, **fn(t))
    ad.action = None
    tr = ad.nla_tracks.new()
    tr.name = name
    st = tr.strips.new(name, 1, act)
    st.name = name
    return act


def S(x):
    return math.sin(2 * math.pi * x)


def clips(rig, bake=True):
    out = {}

    def idle(t):
        return {"spine": (S(t) * 1.2, 0, 0), "head": (S(t + .25) * 2, 0, S(t) * 2), "arm_L": (0, 0, -3), "arm_R": (0, 0, 3),
                "hips": (0, 0, 0, (0, 0, S(t) * .004))}

    def walk(t):
        a = S(t)
        b = S(t + .5)
        return {"hips": (0, S(t * 2) * 2, S(t) * 5, (0, 0, abs(S(t)) * .035)),
                "spine": (0, 0, -S(t) * 4), "head": (0, 0, S(t) * 3),
                "thigh_L": (-a * 34, 0, 0), "shin_L": (max(0, a) * 38, 0, 0),
                "thigh_R": (-b * 34, 0, 0), "shin_R": (max(0, b) * 38, 0, 0),
                "arm_L": (b * 38, 0, -4), "fore_L": (-18 + b * -8, 0, 0),
                "arm_R": (a * 38, 0, 4), "fore_R": (-18 + a * -8, 0, 0)}

    sit_base = {"hips": (0, 0, 0, (0, 0, SIT_HIPS_DZ)), "thigh_L": (-90, 0, 0), "thigh_R": (-90, 0, 0),
                "shin_L": (90, 0, 0), "shin_R": (90, 0, 0)}

    def sit(t):
        d = dict(sit_base)
        d.update({"spine": (S(t) * 1.0, 0, 0), "head": (S(t + .25) * 2, 0, 0), "arm_L": (-25, 0, -4), "arm_R": (-25, 0, 4),
                  "fore_L": (-35, 0, 0), "fore_R": (-35, 0, 0)})
        return d

    def typ(t):
        d = dict(sit_base)
        a, b = S(t * 3), S(t * 3 + .5)
        d.update({"spine": (-4, 0, 0), "head": (-8 + S(t * 1.5) * 2, 0, 0), "arm_L": (-50, 0, -6), "arm_R": (-50, 0, 6),
                  "fore_L": (-55 + a * 12, 0, 0), "fore_R": (-55 + b * 12, 0, 0)})
        return d

    def think(t):
        d = dict(sit_base)
        d.update({"spine": (1, 0, 0), "head": (-6, 0, 12 + S(t) * 3), "arm_L": (-35, 0, -4), "fore_L": (-35, 0, 0),
                  "arm_R": (-70, 0, 6), "fore_R": (-125, 0, 0)})
        return d

    def review(t):
        d = dict(sit_base)
        d.update({"spine": (-3, 0, 0), "head": (-10 + S(t) * 6, 0, 0), "arm_L": (-60, 0, -6), "fore_L": (-70, 0, 0),
                  "arm_R": (-60, 0, 6), "fore_R": (-70 + S(t) * 10, 0, 0)})
        return d

    def ship(t):
        d = dict(sit_base)
        up = max(0, S(t))
        d.update({"spine": (0, 0, 0), "head": (0, 0, S(t) * 4), "arm_L": (-160 * up - 20, 0, -8), "fore_L": (-10 * up, 0, 0),
                  "arm_R": (-160 * up - 20, 0, 8), "fore_R": (-10 * up, 0, 0), "hips": (0, 0, 0, (0, 0, SIT_HIPS_DZ + up * .03))})
        return d

    def error(t):
        d = dict(sit_base)
        sh = S(t * 6) * 4
        d.update({"spine": (0, 0, sh), "head": (6, 0, sh * 1.5), "arm_L": (-70, 0, 6), "fore_L": (-120, 0, 0),
                  "arm_R": (-70, 0, -6), "fore_R": (-120, 0, 0)})
        return d

    def coffee(t):
        d = dict(sit_base)
        sip = max(0, S(t))
        d.update({"spine": (0, 0, 0), "head": (-5 * sip, 0, 0), "arm_L": (-25, 0, -4), "fore_L": (-35, 0, 0),
                  "arm_R": (-50 - sip * 20, 0, 6), "fore_R": (-100 - sip * 30, 0, 0)})
        return d

    def sleep(t):
        d = dict(sit_base)
        d.update({"spine": (12 + S(t) * 1.5, 0, 0), "head": (28 + S(t) * 2, 0, 8), "arm_L": (-20, 0, -3), "arm_R": (-20, 0, 3),
                  "fore_L": (-30, 0, 0), "fore_R": (-30, 0, 0)})
        return d

    spec = [("idle", 48, idle), ("walk", 24, walk), ("sit_idle", 48, sit), ("type", 24, typ), ("think", 48, think),
            ("review", 48, review), ("ship", 36, ship), ("error", 24, error), ("coffee", 48, coffee), ("sleep", 72, sleep)]
    for name, n, fn in spec:
        out[name] = (n, fn)
        if bake:
            _clip(rig, name, n, fn)
    return out


def apply(rig, fn, t):
    """Pasang pose clip pada waktu t (0..1) untuk render uji (tanpa keyframe)."""
    for pb in rig.pose.bones:
        pb.rotation_mode = 'QUATERNION'
        pb.rotation_quaternion = (1, 0, 0, 0)
        pb.location = (0, 0, 0)
    for bn, v in fn(t).items():
        R = _rest3(rig, bn)
        Rw = Euler((math.radians(v[0]), math.radians(v[1]), math.radians(v[2])), 'XYZ').to_matrix()
        rig.pose.bones[bn].rotation_quaternion = (R.inverted() @ Rw @ R).to_quaternion()
        if len(v) > 3:
            rig.pose.bones[bn].location = R.inverted() @ Vector(v[3])
    bpy.context.view_layer.update()
