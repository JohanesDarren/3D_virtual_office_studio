"""5 gaya mata+alis (FACE_<id>.eye_L/.eye_R/.brow; mata berpivot di pusatnya agar bisa kedip lewat scale Z),
mulut bersama (MOUTH_<id>), blush (BLUSH), rambut wajah (FHAIR_<id>). Tanpa outline. Depan wajah y=-.34."""
Y = -.345
EX, EZ = .17, 1.30


def _eye(c, fid, side, build):
    sx = 1 if side == "L" else -1
    p = c.part(f"FACE_{fid}.eye_{side}", "head", outline=False, skinned=False)
    build(p, sx)
    p.done(pivot=(sx * EX, Y, EZ))


def _brow(c, fid, w, h, tilt, z=1.47):
    p = c.part(f"FACE_{fid}.brow", "head", outline=False, skinned=False)
    for sx in (1, -1):
        p.box((sx * EX, Y, z), (w, .03, h), "M_hair", r=.01, seg=1, rot=(0, -sx * tilt, 0))
    p.done()


def _mk(c, fid, eye, brow):
    for side in ("L", "R"):
        _eye(c, fid, side, eye)
    _brow(c, fid, *brow)


def ramah(c):
    def e(p, sx):
        p.box((sx * EX, Y, EZ), (.10, .03, .13), "M_eye", r=.04, seg=2)
        p.box((sx * EX - .02, Y - .012, EZ + .03), (.035, .02, .045), "M_eyewhite", r=.01, seg=1)
    _mk(c, "ramah", e, (.15, .035, 6))


def besar(c):
    def e(p, sx):
        p.box((sx * EX, Y, EZ), (.15, .03, .18), "M_eye", r=.06, seg=2)
        p.box((sx * EX - .03, Y - .012, EZ + .045), (.05, .02, .06), "M_eyewhite", r=.02, seg=1)
        p.box((sx * EX + .03, Y - .012, EZ - .04), (.03, .02, .03), "M_eyewhite", r=.01, seg=1)
        p.box((sx * EX, Y - .004, EZ + .105), (.17, .03, .03), "M_eye", r=.01, seg=1)
    _mk(c, "besar", e, (.13, .025, 0, 1.50))


def dot(c):
    def e(p, sx):
        p.sph((sx * EX, Y, EZ), (.085, .04, .085), "M_eye", seg=10)
    _mk(c, "dot", e, (.15, .04, 0))


def tajam(c):
    def e(p, sx):
        p.box((sx * EX, Y, EZ), (.14, .03, .075), "M_eye", r=.025, seg=2, rot=(0, -sx * 14, 0))
        p.box((sx * EX - .02, Y - .012, EZ + .012), (.035, .02, .025), "M_eyewhite", r=.01, seg=1)
    _mk(c, "tajam", e, (.17, .04, -16, 1.44))


def sipit(c):
    def e(p, sx):
        p.box((sx * EX, Y, EZ - .01), (.14, .03, .03), "M_eye", r=.012, seg=1)
        p.box((sx * EX - .06, Y, EZ - .0), (.05, .03, .03), "M_eye", r=.01, seg=1, rot=(0, 30, 0))
        p.box((sx * EX + .06, Y, EZ - .0), (.05, .03, .03), "M_eye", r=.01, seg=1, rot=(0, -30, 0))
    _mk(c, "sipit", e, (.13, .025, 4))


FACE = {f.__name__: f for f in (ramah, besar, dot, tajam, sipit)}


def _mouth(c, mid, build):
    p = c.part("MOUTH_" + mid, "head", outline=False, skinned=False)
    build(p)
    p.done()


def mouth_smile(c):
    def b(p):
        p.box((0, Y, 1.095), (.08, .03, .025), "M_mouth", r=.01, seg=1)
        for sx in (1, -1):
            p.box((sx * .058, Y, 1.115), (.055, .03, .025), "M_mouth", r=.01, seg=1, rot=(0, -sx * 35, 0))
    _mouth(c, "smile", b)


def mouth_flat(c):
    _mouth(c, "flat", lambda p: p.box((0, Y, 1.10), (.10, .03, .022), "M_mouth", r=.008, seg=1))


def mouth_open(c):
    _mouth(c, "open", lambda p: p.sph((0, Y, 1.09), (.10, .035, .08), "M_mouth", seg=10))


def mouth_sleep(c):
    _mouth(c, "sleep", lambda p: p.box((0, Y, 1.10), (.05, .03, .02), "M_mouth", r=.008, seg=1))


MOUTH = {"smile": mouth_smile, "flat": mouth_flat, "open": mouth_open, "sleep": mouth_sleep}


def blush(c):
    p = c.part("BLUSH", "head", outline=False, skinned=False)
    for sx in (1, -1):
        p.sph((sx * .27, Y + .004, 1.17), (.11, .025, .055), "M_blush", seg=10)
    p.done()


def kumis(c):
    p = c.part("FHAIR_kumis", "head", outline=False, skinned=False)
    for sx in (1, -1):
        p.box((sx * .05, Y - .004, 1.165), (.10, .04, .035), "M_hair", r=.012, seg=1, rot=(0, -sx * 12, 0))
    p.done()


def jenggot_tipis(c):
    p = c.part("FHAIR_jenggot_tipis", "head", outline=False, skinned=False)
    p.box((0, -.325, 1.03), (.36, .07, .07), "M_hair", r=.025, seg=1)
    for sx in (1, -1):
        p.box((sx * .20, -.30, 1.10), (.06, .09, .13), "M_hair", r=.02, seg=1)
    p.box((0, Y - .004, 1.165), (.18, .04, .03), "M_hair", r=.01, seg=1)
    p.done()


FHAIR = {"kumis": kumis, "jenggot_tipis": jenggot_tipis}
