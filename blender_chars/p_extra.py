"""Part tambahan (gelombang 2): rambut, atasan, bawahan, sepatu, aksesori. Mendaftar sendiri ke registry modul asal.
Impor modul ini (import p_extra) sebelum membaca p_hair.HAIR dst. Koordinat/konvensi sama dgn p_hair/p_outfit/p_acc."""
import math
import p_hair, p_outfit, p_acc
from p_hair import _base, _fringe
from p_outfit import _torso, _arms, _collar, _belt

H, T, T2, B = "M_hair", "M_top", "M_top2", "M_bottom"
A, A2, A3 = "M_acc", "M_acc2", "M_acc3"
Y = -.355


# ------------------------------------------------------------------ RAMBUT
def _hp(c, name, top=True):
    return p_hair.HP(c, name, top)


def cepak(c, top=True):
    p = _hp(c, "cepak", top); _base(p, back_to=1.50, side_to=1.52, cap_h=.13)
    p.box((0, -.33, 1.63), (.62, .08, .07), H, r=.03, top=True)
    p.done()


def belah_tengah(c, top=True):
    p = _hp(c, "belah_tengah", top); _base(p, back_to=1.40)
    for sx in (1, -1):
        p.box((sx * .20, -.345, 1.57), (.38, .09, .15), H, r=.045, rot=(0, sx * -12, 0), top=True)
        p.box((sx * .365, -.22, 1.46), (.08, .26, .30), H, r=.03)
    p.done()


def mohawk(c, top=True):
    p = _hp(c, "mohawk", top); _base(p, back_to=1.50, side_to=1.52, cap_h=.12)
    for y, h in [(-.24, .22), (-.10, .30), (.04, .34), (.18, .30), (.32, .22)]:
        p.box((0, y, 1.78 + h / 2 - .05), (.17, .16, h), H, r=.035, seg=1, top=True)
    p.done()


def afro(c, top=True):
    p = _hp(c, "afro", top); _base(p, back_to=1.30, side_to=1.34, cap_h=.2)
    p.sph((0, .14, 1.78), (1.00, .90, .74), H, seg=14, top=True)
    p.sph((-.30, .04, 1.74), (.42, .42, .42), H, seg=10, top=True)
    p.sph((.30, .04, 1.74), (.42, .42, .42), H, seg=10, top=True)
    _fringe(p, .70, .12, 1.58)
    p.done()


def kuncir_dua(c, top=True):
    p = _hp(c, "kuncir_dua", top); _base(p, back_to=1.44); _fringe(p, .72, .15, 1.56)
    for sx in (1, -1):
        p.box((sx * .38, .12, 1.56), (.10, .10, .10), A, r=.03, top=True)
        p.box((sx * .49, .14, 1.28), (.16, .16, .44), H, r=.07, seg=2, rot=(0, sx * -10, 0))
    p.done()


def kepang(c, top=True):
    p = _hp(c, "kepang", top); _base(p, back_to=1.44); _fringe(p, .72, .15, 1.56)
    for sx in (1, -1):
        for i in range(4):
            p.sph((sx * (.30 - i * .02), .36, 1.40 - i * .15), (.19, .17, .19), H, seg=8)
        p.box((sx * .24, .36, 0.86), (.10, .10, .09), A, r=.02)
    p.done()


def undercut(c, top=True):
    p = _hp(c, "undercut", top); _base(p, back_to=1.50, side_to=1.52, cap_h=.13)
    p.box((0, -.02, 1.76), (.58, .62, .20), H, r=.07, seg=2, top=True)
    p.box((.02, -.30, 1.74), (.52, .16, .15), H, r=.05, rot=(-14, 0, 0), top=True)
    p.done()


def man_bun(c, top=True):
    p = _hp(c, "man_bun", top); _base(p, back_to=1.46, cap_h=.2); _fringe(p, .66, .11, 1.60)
    p.sph((0, .18, 1.86), (.26, .26, .24), H, seg=10, top=True)
    p.box((0, .17, 1.76), (.22, .20, .04), A, r=.015, top=True)
    p.done()


def ikal_panjang(c, top=True):
    p = _hp(c, "ikal_panjang", top); _base(p, back_to=.98, side_to=1.08); _fringe(p, .74, .15, 1.55)
    for sx in (1, -1):
        for i in range(3):
            p.sph((sx * (.42 - i * .01), .04, 1.34 - i * .17), (.22, .24, .22), H, seg=8)
    for x, z in ((-.2, 1.20), (.2, 1.20), (0, 1.02), (-.2, 0.96), (.2, 0.96)):
        p.sph((x, .35, z), (.24, .22, .22), H, seg=8)
    p.done()


for _f in (cepak, belah_tengah, mohawk, afro, kuncir_dua, kepang, undercut, man_bun, ikal_panjang):
    p_hair.HAIR[_f.__name__] = _f

# ------------------------------------------------------------------ ATASAN


def kaos_garis(c):
    p = c.part("TOP_kaos_garis", "spine"); _torso(p); _arms(p, False, T)
    for z in (.62, .75, .88):
        p.box((0, 0, z), (.52, .38, .05), T2, "spine", r=.01, seg=1)
    for sx, L in ((1, "L"), (-1, "R")):
        p.box((sx * .31, 0, .71), (.185, .185, .04), T2, "arm_" + L, r=.01, seg=1)
    p.done()


def jaket(c):
    p = c.part("TOP_jaket", "spine"); _torso(p, w=.55, d=.41, h=.49); _arms(p, True, T, T2)
    p.box((0, -.21, .74), (.035, .02, .46), "M_acc2", "spine", r=.004, seg=1)
    p.box((0, 0, .50), (.56, .41, .05), T2, "spine", r=.015, seg=1)
    p.box((0, 0, .985), (.36, .30, .07), T2, "spine", r=.025, seg=1)
    for sx in (1, -1):
        p.box((sx * .15, -.21, .62), (.1, .02, .1), T2, "spine", r=.01, seg=1)
    p.done()


def turtleneck(c):
    p = c.part("TOP_turtleneck", "spine"); _torso(p); _arms(p, True, T, T2)
    p.cyl((0, 0, 1.0), (.27, .25), .10, T2, "spine", seg=14)
    p.box((0, 0, .50), (.52, .37, .03), T2, "spine", r=.01, seg=1)
    p.done()


def tanktop(c):
    p = c.part("TOP_tanktop", "spine"); _torso(p, w=.46, d=.35, h=.44, z=.73)
    for sx in (1, -1):
        p.box((sx * .14, 0, .96), (.09, .31, .07), T, "spine", r=.015, seg=1)
    p.box((0, -.0, .55), (.47, .355, .03), T2, "spine", r=.01, seg=1)
    p.done()


def jas_lab(c):
    p = c.part("TOP_jas_lab", "spine")
    p.box((0, 0, .72), (.55, .41, .54), T, "spine", r=.08, seg=2)
    _arms(p, True, T, T2)
    for sx in (1, -1):
        p.box((sx * .09, -.2, .94), (.13, .04, .12), T, "spine", r=.015, seg=1, rot=(0, 0, sx * -28))
        p.box((sx * .16, -.215, .58), (.13, .02, .12), T2, "spine", r=.012, seg=1)
    p.box((0, -.205, .72), (.03, .02, .48), T2, "spine", r=.004, seg=1)
    for z in (.84, .72, .60):
        p.sph((0, -.215, z), (.04, .03, .04), "M_acc2", "spine", seg=6)
    p.done()


def overall(c):
    p = c.part("TOP_overall", "spine"); _arms(p, True, T2)
    p.box((0, 0, .745), (.50, .36, .47), T2, "spine", r=.09, seg=2)
    p.box((0, 0, .60), (.545, .395, .23), T, "spine", r=.07, seg=2)
    p.box((0, -.19, .78), (.30, .03, .30), T, "spine", r=.03, seg=1)
    for sx in (1, -1):
        p.box((sx * .12, -.14, .94), (.06, .14, .10), T, "spine", r=.01, seg=1)
        p.box((sx * .12, -.01, .985), (.06, .10, .035), T, "spine", r=.01, seg=1)
        p.sph((sx * .12, -.215, .88), (.045, .025, .045), "M_acc2", "spine", seg=6)
    p.box((0, -.215, .75), (.12, .02, .09), T2, "spine", r=.012, seg=1)
    p.done()


for _f in (kaos_garis, jaket, turtleneck, tanktop, jas_lab, overall):
    p_outfit.TOP[_f.__name__] = _f

# ------------------------------------------------------------------ BAWAHAN


def celana_kargo(c):
    p = c.part("BOTTOM_celana_kargo", "hips")
    p.box((0, 0, .515), (.47, .345, .17), B, "hips", r=.06, seg=2); _belt(p)
    for sx, L in ((1, "L"), (-1, "R")):
        p.box((sx * .12, 0, .38), (.215, .215, .20), B, "thigh_" + L, r=.05, seg=2)
        p.box((sx * .12, 0, .215), (.19, .19, .20), B, "shin_" + L, r=.04, seg=2)
        p.box((sx * .12, -.115, .36), (.14, .04, .12), "M_acc2", "thigh_" + L, r=.01, seg=1)
        p.box((sx * .12, 0, .13), (.20, .20, .03), "M_acc2", "shin_" + L, r=.008, seg=1)
    p.done()


def celana_longgar(c):
    p = c.part("BOTTOM_celana_longgar", "hips")
    p.box((0, 0, .515), (.48, .35, .17), B, "hips", r=.06, seg=2); _belt(p)
    for sx, L in ((1, "L"), (-1, "R")):
        p.box((sx * .13, 0, .38), (.25, .25, .20), B, "thigh_" + L, r=.06, seg=2)
        p.box((sx * .13, 0, .205), (.265, .265, .21), B, "shin_" + L, r=.05, seg=2)
    p.done()


def celana_cropped(c):
    p = c.part("BOTTOM_celana_cropped", "hips")
    p.box((0, 0, .515), (.47, .345, .17), B, "hips", r=.06, seg=2); _belt(p)
    for sx, L in ((1, "L"), (-1, "R")):
        p.box((sx * .12, 0, .38), (.205, .205, .20), B, "thigh_" + L, r=.05, seg=2)
        p.box((sx * .12, 0, .245), (.185, .185, .12), B, "shin_" + L, r=.04, seg=2)
        p.box((sx * .12, 0, .19), (.19, .19, .03), "M_top2", "shin_" + L, r=.008, seg=1)
    p.done()


def rok_pendek(c):
    p = c.part("BOTTOM_rok_pendek", "hips")
    p.box((0, 0, .53), (.45, .33, .13), B, "hips", r=.05, seg=2)
    p.cyl((0, 0, .47), (.60, .50), .14, B, "hips", r2=.82, seg=16)
    p.box((0, 0, .576), (.44, .32, .04), "M_acc2", "hips", r=.01, seg=1)
    p.done()


def rok_panjang(c):
    p = c.part("BOTTOM_rok_panjang", "hips")
    p.box((0, 0, .53), (.45, .33, .14), B, "hips", r=.05, seg=2)
    p.cyl((0, 0, .36), (.62, .52), .46, B, "hips", r2=.95, seg=16)
    p.box((0, 0, .576), (.44, .32, .04), "M_acc2", "hips", r=.01, seg=1)
    p.done()


for _f in (celana_kargo, celana_longgar, celana_cropped, rok_pendek, rok_panjang):
    p_outfit.BOTTOM[_f.__name__] = _f

# ------------------------------------------------------------------ SEPATU


def boots(c):
    p = c.part("SHOES_boots", "shin_L")
    for sx, L in ((1, "L"), (-1, "R")):
        p.box((sx * .12, -.045, .07), (.20, .32, .12), "M_shoes", "shin_" + L, r=.05, seg=2)
        p.box((sx * .12, 0, .22), (.205, .215, .26), "M_shoes", "shin_" + L, r=.05, seg=2)
        p.box((sx * .12, -.05, .018), (.21, .33, .04), "M_shoes2", "shin_" + L, r=.015, seg=1)
        p.box((sx * .12, 0, .355), (.22, .23, .035), "M_shoes2", "shin_" + L, r=.01, seg=1)
    p.done()


def sandal(c):
    p = c.part("SHOES_sandal", "shin_L")
    for sx, L in ((1, "L"), (-1, "R")):
        p.box((sx * .12, -.05, .02), (.20, .33, .04), "M_shoes2", "shin_" + L, r=.015, seg=1)
        p.box((sx * .12, -.12, .06), (.19, .07, .05), "M_shoes", "shin_" + L, r=.015, seg=1)
        p.box((sx * .12, .00, .06), (.19, .05, .05), "M_shoes", "shin_" + L, r=.015, seg=1)
        p.box((sx * .12, .08, .06), (.19, .05, .05), "M_shoes", "shin_" + L, r=.015, seg=1)
    p.done()


def hightop(c):
    p = c.part("SHOES_hightop", "shin_L")
    for sx, L in ((1, "L"), (-1, "R")):
        p.box((sx * .12, -.045, .075), (.195, .31, .13), "M_shoes", "shin_" + L, r=.05, seg=2)
        p.box((sx * .12, .03, .17), (.19, .17, .13), "M_shoes", "shin_" + L, r=.05, seg=2)
        p.box((sx * .12, -.05, .018), (.205, .325, .04), "M_shoes2", "shin_" + L, r=.015, seg=1)
        p.box((sx * .12, -.13, .115), (.15, .1, .05), "M_top2", "shin_" + L, r=.02, seg=1)
        p.box((sx * .12, .03, .245), (.20, .18, .03), "M_top2", "shin_" + L, r=.01, seg=1)
    p.done()


def loafer(c):
    p = c.part("SHOES_loafer", "shin_L")
    for sx, L in ((1, "L"), (-1, "R")):
        p.box((sx * .12, -.045, .07), (.185, .32, .12), "M_shoes", "shin_" + L, r=.05, seg=2)
        p.box((sx * .12, .06, .015), (.17, .10, .035), "M_shoes2", "shin_" + L, r=.01, seg=1)
        p.box((sx * .12, -.14, .12), (.12, .07, .02), "M_acc2", "shin_" + L, r=.008, seg=1)
    p.done()


for _f in (boots, sandal, hightop, loafer):
    p_outfit.SHOES[_f.__name__] = _f

# ------------------------------------------------------------------ AKSESORI


def _ph(c, name, outline=False):
    return c.part("ACC_" + name, "head", outline=outline, skinned=False)


def kacamata_hitam(c):
    p = _ph(c, "kacamata_hitam")
    for sx in (1, -1):
        x = sx * .17
        p.box((x, Y, 1.30), (.21, .02, .15), "M_acc2", r=.03, seg=2)
        p.box((x, Y - .004, 1.375), (.22, .02, .025), A, r=.005, seg=1)
        p.box((sx * .31, -.30, 1.31), (.015, .12, .018), A, r=.003, seg=1)
    p.box((0, Y, 1.325), (.07, .02, .02), A, r=.003, seg=1)
    p.done()


def bando(c):
    p = _ph(c, "bando")
    p_acc._band(p, z=1.33, R=.47, m=A)
    p.done()


def pita(c):
    p = _ph(c, "pita", True)
    for sx in (1, -1):
        p.sph((.18 + sx * .09, -.10, 1.80), (.16, .10, .15), A, seg=8, rot=(0, sx * 20, 0))
    p.sph((.18, -.10, 1.80), (.07, .08, .07), A3, seg=8)
    p.done()


def kupluk(c):
    p = _ph(c, "kupluk", True)
    p.sph((0, .03, 1.65), (.98, .94, .66), A, seg=14)
    p.cyl((0, .02, 1.56), (.90, .86), .10, A2, seg=16)
    p.sph((0, .03, 1.97), (.20, .20, .20), A3, seg=8)
    p.done()


def topi_koki(c):
    p = _ph(c, "topi_koki", True)
    p.cyl((0, .02, 1.64), (.90, .86), .24, A, seg=16)
    p.sph((0, .02, 1.96), (.98, .94, .54), A, seg=14)
    p.done()


def telinga_kucing(c):
    p = _ph(c, "telinga_kucing", True)
    p_acc._band(p, z=1.33, R=.47, m=A)
    for sx in (1, -1):
        p.cyl((sx * .22, 0, 1.93), (.26, .14), .26, A, r2=.12, seg=8, rot=(0, sx * 12, 0))
        p.cyl((sx * .22, -.04, 1.92), (.14, .06), .16, A3, r2=.15, seg=8, rot=(0, sx * 12, 0))
    p.done()


def masker(c):
    p = _ph(c, "masker")
    p.box((0, -.368, 1.12), (.34, .05, .20), A, r=.035, seg=2)
    for sx in (1, -1):
        p.box((sx * .20, -.28, 1.17), (.015, .20, .015), A, r=.003, seg=1, rot=(0, 0, sx * 25))
    p.done()


def syal(c):
    p = c.part("ACC_syal", "spine")
    p.cyl((0, 0, .97), (.36, .33), .11, A3, "spine", seg=14)
    p.box((.12, -.20, .85), (.10, .04, .30), A3, "spine", r=.015, seg=1, rot=(0, 0, -6))
    p.box((.12, -.20, .70), (.10, .04, .04), A2, "spine", r=.008, seg=1)
    p.done()


def jam_tangan(c):
    p = c.part("ACC_jam_tangan", "fore_L")
    p.box((.31, 0, .52), (.175, .175, .045), A2, "fore_L", r=.01, seg=1)
    p.box((.31, -.095, .52), (.09, .03, .075), A, "fore_L", r=.01, seg=1)
    p.done()


for _f in (kacamata_hitam, bando, pita, kupluk, topi_koki, telinga_kucing, masker, syal, jam_tangan):
    p_acc.ACC[_f.__name__] = _f

# ------------------------------------------------------------------ TOPI & KONFLIK
# Topi menutup rambut: saat salah satu HEAD_HAT dipakai, HAIRTOP_<gaya> disembunyikan (hair(c, top=False) di char.py).
# Bagian bawah rambut (HAIR_<gaya>: sisi/belakang) tetap tampak di bawah tepi topi.
p_acc.HEAD_HAT = ("baret", "topi", "topi_balik", "kupluk", "topi_koki")
p_acc.HEAD_TOP = ("baret", "topi", "topi_balik", "kupluk", "topi_koki", "bando", "pita", "telinga_kucing", "headphone", "headset_mic")  # maks satu
p_acc.CONFLICT_HAIR = ()   # topi cocok dgn semua rambut
_BIG = ("afro", "mohawk", "sanggul", "sanggul_tinggi", "man_bun")
p_acc.ACC_HAIR_CONFLICT = {"bando": _BIG, "headphone": _BIG, "headset_mic": _BIG,
                           "pita": _BIG + ("spiky", "ikal_pendek"), "telinga_kucing": _BIG + ("spiky", "ikal_pendek")}


# ------------------------------------------------------------------ WAJAH (mata+alis) tambahan
import p_face
from p_face import EX, EZ, _mk, _mouth
from p_face import Y as YF


def ceria(c):
    def e(p, sx):
        for dx, rz in ((-.04, -28), (.04, 28)):
            p.box((sx * EX + dx, YF, EZ + .012), (.085, .03, .03), "M_eye", r=.012, seg=1, rot=(0, rz, 0))
    _mk(c, "ceria", e, (.15, .035, 4, 1.47))


def kantuk(c):
    def e(p, sx):
        p.box((sx * EX, YF, EZ - .02), (.11, .03, .065), "M_eye", r=.025, seg=2)
        p.box((sx * EX, YF - .004, EZ + .02), (.14, .03, .03), "M_eye", r=.01, seg=1)
    _mk(c, "kantuk", e, (.14, .03, -6, 1.44))


def anime(c):
    def e(p, sx):
        p.box((sx * EX, YF, EZ), (.17, .03, .22), "M_eye", r=.07, seg=2)
        p.box((sx * EX - .035, YF - .012, EZ + .06), (.06, .02, .08), "M_eyewhite", r=.02, seg=1)
        p.box((sx * EX + .035, YF - .012, EZ - .06), (.035, .02, .035), "M_eyewhite", r=.01, seg=1)
        p.box((sx * EX, YF - .004, EZ + .12), (.19, .03, .035), "M_eye", r=.01, seg=1)
    _mk(c, "anime", e, (.13, .025, 0, 1.52))


def bintang(c):
    def e(p, sx):
        p.box((sx * EX, YF, EZ), (.15, .03, .17), "M_eye", r=.06, seg=2)
        p.box((sx * EX - .03, YF - .012, EZ + .035), (.075, .02, .022), "M_eyewhite", r=.006, seg=1)
        p.box((sx * EX - .03, YF - .012, EZ + .035), (.022, .02, .075), "M_eyewhite", r=.006, seg=1)
        p.box((sx * EX + .035, YF - .012, EZ - .045), (.03, .02, .03), "M_eyewhite", r=.008, seg=1)
    _mk(c, "bintang", e, (.14, .03, 4, 1.50))


def bulu_mata(c):
    def e(p, sx):
        p.box((sx * EX, YF, EZ), (.11, .03, .13), "M_eye", r=.04, seg=2)
        p.box((sx * EX - .02, YF - .012, EZ + .03), (.035, .02, .045), "M_eyewhite", r=.01, seg=1)
        p.box((sx * EX, YF - .004, EZ + .075), (.13, .03, .022), "M_eye", r=.008, seg=1)
        p.box((sx * (EX + .075), YF - .004, EZ + .08), (.055, .03, .02), "M_eye", r=.006, seg=1, rot=(0, -sx * 28, 0))
    _mk(c, "bulu_mata", e, (.14, .025, 6, 1.49))


def serius(c):
    def e(p, sx):
        p.box((sx * EX, YF, EZ), (.13, .03, .085), "M_eye", r=.01, seg=1)
        p.box((sx * EX - .03, YF - .012, EZ + .012), (.035, .02, .03), "M_eyewhite", r=.006, seg=1)
    _mk(c, "serius", e, (.19, .05, -10, 1.44))


def sedih(c):
    def e(p, sx):
        p.box((sx * EX, YF, EZ), (.10, .03, .12), "M_eye", r=.04, seg=2)
        p.box((sx * EX - .02, YF - .012, EZ + .03), (.04, .02, .05), "M_eyewhite", r=.01, seg=1)
    _mk(c, "sedih", e, (.15, .03, 16, 1.45))


for _f in (ceria, kantuk, anime, bintang, bulu_mata, serius, sedih):
    p_face.FACE[_f.__name__] = _f

# ------------------------------------------------------------------ MULUT tambahan (z 1.10; sudut naik = rot -sx*sudut)
Z0 = 1.10


def senyum_lebar(c):
    def b(p):
        p.box((0, YF, Z0 - .005), (.10, .03, .026), "M_mouth", r=.01, seg=1)
        for sx in (1, -1):
            p.box((sx * .075, YF, Z0 + .02), (.07, .03, .026), "M_mouth", r=.01, seg=1, rot=(0, -sx * 35, 0))
    _mouth(c, "senyum_lebar", b)


def tertawa(c):
    def b(p):
        p.box((0, YF, Z0 - .005), (.17, .03, .075), "M_mouth", r=.025, seg=2)
        p.box((0, YF - .009, Z0 + .02), (.15, .02, .03), "M_eyewhite", r=.006, seg=1)
        p.sph((0, YF - .006, Z0 - .03), (.08, .02, .03), "M_blush", seg=8)
    _mouth(c, "tertawa", b)


def cemberut(c):
    def b(p):
        p.box((0, YF, Z0 - .005), (.08, .03, .024), "M_mouth", r=.008, seg=1)
        for sx in (1, -1):
            p.box((sx * .06, YF, Z0 - .022), (.06, .03, .024), "M_mouth", r=.008, seg=1, rot=(0, sx * 35, 0))
    _mouth(c, "cemberut", b)


def miring(c):
    def b(p):
        p.box((-.01, YF, Z0), (.09, .03, .024), "M_mouth", r=.008, seg=1)
        p.box((.07, YF, Z0 + .022), (.055, .03, .024), "M_mouth", r=.008, seg=1, rot=(0, -35, 0))
    _mouth(c, "miring", b)


def kucing(c):
    def b(p):
        for cx in (-.05, .05):
            p.box((cx - .026, YF, Z0), (.045, .03, .022), "M_mouth", r=.006, seg=1, rot=(0, 40, 0))
            p.box((cx + .026, YF, Z0), (.045, .03, .022), "M_mouth", r=.006, seg=1, rot=(0, -40, 0))
    _mouth(c, "kucing", b)


def lidah(c):
    def b(p):
        p.box((0, YF, Z0 + .005), (.10, .03, .024), "M_mouth", r=.008, seg=1)
        for sx in (1, -1):
            p.box((sx * .065, YF, Z0 + .022), (.045, .03, .024), "M_mouth", r=.008, seg=1, rot=(0, -sx * 35, 0))
        p.box((.012, YF - .004, Z0 - .035), (.05, .025, .065), "M_blush", r=.015, seg=1)
    _mouth(c, "lidah", b)


def o_kecil(c):
    _mouth(c, "o_kecil", lambda p: p.sph((0, YF, Z0 - .01), (.055, .035, .06), "M_mouth", seg=10))


def gigi(c):
    def b(p):
        p.box((0, YF, Z0), (.15, .03, .05), "M_eyewhite", r=.006, seg=1)
        for dz in (.032, -.032):
            p.box((0, YF - .004, Z0 + dz), (.17, .03, .016), "M_mouth", r=.005, seg=1)
        p.box((0, YF - .004, Z0), (.012, .03, .05), "M_mouth", r=.003, seg=1)
    _mouth(c, "gigi", b)


for _f in (senyum_lebar, tertawa, cemberut, miring, kucing, lidah, o_kecil, gigi):
    p_face.MOUTH[_f.__name__] = _f
