"""10+ aksesori. Kepala/wajah menempel ke bone head (tidak di-skin); badan di-skin ke spine.
Konflik: topi/baret/topi_balik tidak boleh dengan rambut sanggul, sanggul_tinggi, spiky, ikal_pendek (lihat CONFLICT_HAIR)."""
import math
Y = -.355
A, A2, A3 = "M_acc", "M_acc2", "M_acc3"


def _hp(c, name):
    return c.part("ACC_" + name, "head", outline=False, skinned=False)


def kacamata_bulat(c):
    p = _hp(c, "kacamata_bulat")
    for sx in (1, -1):
        p.ring((sx * .17, Y, 1.30), .092, .018, A, seg=14)
        p.box((sx * .31, -.30, 1.31), (.015, .12, .018), A, r=.003, seg=1)
    p.box((0, Y, 1.325), (.07, .018, .018), A, r=.003, seg=1)
    p.done()


def kacamata_kotak(c):
    p = _hp(c, "kacamata_kotak")
    for sx in (1, -1):
        x = sx * .17
        for dz in (.085, -.085):
            p.box((x, Y, 1.30 + dz), (.205, .018, .018), A, r=.003, seg=1)
        for dx in (.1, -.1):
            p.box((x + dx, Y, 1.30), (.018, .018, .17), A, r=.003, seg=1)
        p.box((sx * .31, -.30, 1.31), (.015, .12, .018), A, r=.003, seg=1)
    p.box((0, Y, 1.325), (.07, .018, .018), A, r=.003, seg=1)
    p.done()


def _band(p, z=1.33, R=.42, m=A2):
    for i in range(9):
        a = math.radians(-80 + i * 20)
        p.box((R * math.sin(a), 0, z + R * math.cos(a) * .98), (.06, .08, .06), m, r=.01, seg=1,
              rot=(0, -math.degrees(a), 0))


def headset_mic(c):
    p = c.part("ACC_headset_mic", "head", skinned=False, outline=False)
    _band(p)
    for sx in (1, -1):
        p.cyl((sx * .40, 0, 1.30), (.17, .17), .08, A, seg=12, rot=(0, 90, 0))
    p.box((.37, -.18, 1.16), (.02, .26, .02), A2, r=.004, seg=1, rot=(0, 0, -25))
    p.sph((.31, -.30, 1.14), (.06, .06, .05), A, seg=8)
    p.done()


def headphone(c):
    p = c.part("ACC_headphone", "head", skinned=False, outline=False)
    _band(p, R=.44)
    for sx in (1, -1):
        p.cyl((sx * .42, 0, 1.30), (.28, .26), .10, A, seg=14, rot=(0, 90, 0))
        p.cyl((sx * .365, 0, 1.30), (.22, .20), .04, A2, seg=14, rot=(0, 90, 0))
    p.done()


def baret(c):
    p = c.part("ACC_baret", "head", skinned=False)
    p.cyl((.05, .02, 1.64), (.98, .94), .20, A, r2=.92, seg=18, rot=(0, 5, 0))
    p.cyl((.07, .02, 1.78), (.80, .76), .08, A, r2=.8, seg=16, rot=(0, 5, 0))
    p.box((.08, .02, 1.85), (.05, .05, .07), A, r=.01, seg=1)
    p.done()


def _cap(c, name, flip):
    p = c.part("ACC_" + name, "head", skinned=False)
    sg = 1 if flip else -1
    p.sph((0, .03, 1.65), (.96, .92, .66), A, seg=14)
    p.box((0, sg * .52, 1.54), (.5, .30, .045), A, r=.02, seg=1, rot=(sg * -6, 0, 0))
    p.box((0, .03, 1.98), (.05, .05, .05), A, r=.01, seg=1)
    p.done()


def topi(c):
    _cap(c, "topi", False)


def topi_balik(c):
    _cap(c, "topi_balik", True)


def dasi(c):
    p = c.part("ACC_dasi", "spine")
    p.box((0, -.205, .905), (.075, .035, .06), A3, "spine", r=.01, seg=1)
    p.box((0, -.205, .76), (.095, .03, .22), A3, "spine", r=.015, seg=1)
    p.box((0, -.205, .64), (.09, .03, .06), A3, "spine", r=.015, seg=1, rot=(0, 0, 45))
    p.done()


def kartu_id(c):
    p = c.part("ACC_kartu_id", "spine")
    for sx in (1, -1):
        p.box((sx * .075, -.19, .87), (.02, .02, .22), A3, "spine", r=.003, seg=1, rot=(0, 0, sx * -18))
    p.box((0, -.205, .70), (.14, .02, .19), "M_top2", "spine", r=.01, seg=1)
    p.box((0, -.218, .75), (.1, .012, .04), A3, "spine", r=.004, seg=1)
    p.done()


def celemek(c):
    p = c.part("ACC_celemek", "spine")
    p.box((0, -.205, .70), (.40, .03, .38), A3, "spine", r=.02, seg=1)
    p.box((0, -.205, .88), (.24, .03, .12), A3, "spine", r=.02, seg=1)
    for sx in (1, -1):
        p.box((sx * .10, -.19, .93), (.03, .02, .1), A3, "spine", r=.004, seg=1)
    p.box((0, -.225, .60), (.22, .02, .1), "M_top2", "spine", r=.015, seg=1)
    p.sph((-.1, -.224, .78), (.07, .02, .07), "M_top2", "spine", seg=6)
    p.sph((.08, -.224, .70), (.05, .02, .05), A2, "spine", seg=6)
    p.done()


def tas(c):
    p = c.part("ACC_tas", "spine")
    p.box((0, .24, .70), (.36, .13, .34), A3, "spine", r=.04, seg=2)
    p.box((0, .31, .76), (.30, .03, .10), A2, "spine", r=.01, seg=1)
    p.box((-.07, -.195, .78), (.05, .02, .42), A2, "spine", r=.004, seg=1, rot=(0, 0, 28))
    p.done()


ACC = {f.__name__: f for f in (kacamata_bulat, kacamata_kotak, headset_mic, headphone, baret, topi, topi_balik, dasi, kartu_id, celemek, tas)}
HEAD_HAT = ("baret", "topi", "topi_balik")
CONFLICT_HAIR = ("sanggul", "sanggul_tinggi", "spiky", "ikal_pendek")
