"""Gaya rambut (menempel ke tulang head, tidak di-skin). Wajah = sisi -Y, kepala pusat (0,0,1.33), puncak z=1.66.
Tiap gaya = 2 objek: HAIR_<id> (bagian bawah: sisi/belakang/kuncir yang menggantung) dan HAIRTOP_<id> (tempurung, poni, sanggul,
duri, ikal di atas). Saat karakter memakai topi, app/char.py menyembunyikan HAIRTOP_<id> -> topi menutup rambut tanpa tembus."""
H = "M_hair"


class HP:
    """Pembungkus dua Part (low/top). Primitif ber-kwarg top=True masuk HAIRTOP."""

    def __init__(s, c, name, with_top=True):
        s.low = c.part("HAIR_" + name, "head", skinned=False)
        s.top = c.part("HAIRTOP_" + name, "head", skinned=False) if with_top else None

    def _t(s, top):
        return s.top if (top and s.top is not None) else (s.low if not top else None)

    def box(s, *a, top=False, **k):
        t = s._t(top)
        if t is not None:
            t.box(*a, **k)

    def sph(s, *a, top=False, **k):
        t = s._t(top)
        if t is not None:
            t.sph(*a, **k)

    def cyl(s, *a, top=False, **k):
        t = s._t(top)
        if t is not None:
            t.cyl(*a, **k)

    def done(s):
        s.low.done()
        if s.top is not None:
            s.top.done()


def _p(c, name, top=True):
    return HP(c, name, top)


def _base(p, back_to=1.36, side_to=1.40, cap_h=.26):
    p.box((0, .02, 1.74 - cap_h / 2), (.80, .74, cap_h), H, r=.1, seg=3, top=True)
    p.box((0, .30, (1.52 + back_to) / 2), (.78, .17, 1.52 - back_to), H, r=.05)
    for sx in (1, -1):
        p.box((sx * .385, .08, (1.52 + side_to) / 2), (.08, .48, 1.52 - side_to), H, r=.03)


def _fringe(p, w=.72, h=.15, z=1.55, x=0, rot=0):
    p.box((x, -.345, z), (w, .09, h), H, r=.04, rot=(0, rot, 0), top=True)


def belah_samping(c, top=True):
    p = _p(c, "belah_samping", top); _base(p)
    p.box((.12, -.345, 1.57), (.46, .09, .16), H, r=.05, rot=(0, -12, 0), top=True)
    p.box((-.22, -.345, 1.60), (.30, .09, .10), H, r=.04, rot=(0, 10, 0), top=True)
    p.done()


def kuncir_kuda(c, top=True):
    p = _p(c, "kuncir_kuda", top); _base(p, back_to=1.46); _fringe(p, .72, .14, 1.56)
    p.box((0, .40, 1.60), (.16, .12, .14), "M_acc", r=.03, top=True)
    p.box((0, .57, 1.40), (.2, .17, .52), H, r=.07, seg=2, rot=(-18, 0, 0))
    p.done()


def ikal_pendek(c, top=True):
    p = _p(c, "ikal_pendek", top); _base(p, back_to=1.42, cap_h=.2)
    for x, y, z, d in [(-.27, -.12, 1.78, .22), (0, -.2, 1.82, .24), (.27, -.12, 1.78, .22), (-.15, .12, 1.84, .24),
                       (.15, .12, 1.84, .24), (-.34, .12, 1.64, .2), (.34, .12, 1.64, .2), (0, .28, 1.72, .22)]:
        p.sph((x, y, z), (d, d, d), H, seg=10, top=True)
    _fringe(p, .70, .12, 1.58)
    p.done()


def cebot(c, top=True):
    p = _p(c, "cebot", top); _base(p, back_to=1.42, side_to=1.44, cap_h=.24); _fringe(p, .74, .17, 1.55)
    p.done()


def sanggul(c, top=True):
    p = _p(c, "sanggul", top); _base(p, back_to=1.40); _fringe(p, .70, .12, 1.57)
    p.sph((0, .14, 1.88), (.30, .28, .26), H, seg=12, top=True)
    p.box((0, .14, 1.76), (.26, .24, .05), "M_acc", r=.02, top=True)
    p.done()


def spiky(c, top=True):
    p = _p(c, "spiky", top); _base(p, back_to=1.46, cap_h=.2)
    for x, y, rz, ry in [(-.28, -.05, 0, -22), (-.14, -.18, 0, -8), (0, -.24, 0, 0), (.14, -.18, 0, 8), (.28, -.05, 0, 22),
                         (-.14, .14, 0, -8), (.14, .14, 0, 8), (0, .02, 0, 0)]:
        p.cyl((x, y, 1.84), (.2, .2), .3, H, r2=.05, seg=6, rot=(0, ry, 0), top=True)
    _fringe(p, .6, .1, 1.60)
    p.done()


def rapi(c, top=True):
    p = _p(c, "rapi", top); _base(p, back_to=1.46, side_to=1.46, cap_h=.22)
    p.box((.08, -.30, 1.67), (.5, .16, .1), H, r=.04, rot=(8, 0, 0), top=True); _fringe(p, .66, .11, 1.60)
    p.done()


def sanggul_tinggi(c, top=True):
    p = _p(c, "sanggul_tinggi", top); _base(p, back_to=1.40); _fringe(p, .70, .14, 1.56)
    p.sph((0, .06, 1.96), (.26, .26, .30), H, seg=12, top=True)
    p.box((0, .06, 1.80), (.28, .26, .05), "M_acc", r=.02, top=True)
    p.done()


def bob(c, top=True):
    p = _p(c, "bob", top); _base(p, back_to=1.12, side_to=1.12, cap_h=.26); _fringe(p, .76, .17, 1.54)
    for sx in (1, -1):
        p.box((sx * .38, -.06, 1.30), (.1, .6, .44), H, r=.04)
    p.done()


def panjang(c, top=True):
    p = _p(c, "panjang", top); _base(p, back_to=.72, side_to=1.0); _fringe(p, .74, .16, 1.55)
    for sx in (1, -1):
        p.box((sx * .385, .02, 1.12), (.08, .36, .62), H, r=.03)
    p.done()


HAIR = {f.__name__: f for f in (belah_samping, kuncir_kuda, ikal_pendek, cebot, sanggul, spiky, rapi, sanggul_tinggi, bob, panjang)}
