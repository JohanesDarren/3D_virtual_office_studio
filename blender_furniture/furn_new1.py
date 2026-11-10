"""Varian baru: tempat duduk, meja, penyimpanan. Semua di titik asal, depan = +Y, alas z=0."""
import math
from lib import bx, cy, sp, at
from registry import item
import furn_used as U

K = "kain"; W = "kayu"; C = "cat"; L = "logam"; S = "layar"; P = "karpet"


def _star(r=.26, m="black"):
    bx(0, 0, .05, r * 2, .06, .04, m); bx(0, 0, .05, .06, r * 2, .04, m)
    for dx, dy in ((r, 0), (-r, 0), (0, r), (0, -r)):
        cy(dx, dy, 0, .06, .06, .05, m, seg=8)


# ------------------------------------------------------------------ DUDUK
@item("duduk", "kursi_gaming", "Kursi gaming", {"fab_red": K, "black": L})
def _():
    cy(0, 0, .04, .07, .07, .38, "metal_dark"); _star()
    bx(0, 0, .42, .5, .5, .09, "fab_red")
    for s in (-1, 1):
        bx(s * .26, 0, .45, .06, .46, .1, "black")
        bx(s * .27, -.2, .52, .06, .1, .62, "black")
        bx(s * .31, .02, .62, .05, .3, .03, "black"); bx(s * .31, .02, .5, .03, .03, .13, "black")
    bx(0, -.24, .5, .46, .1, .85, "fab_red", rx=-7)
    bx(0, -.27, 1.2, .32, .08, .22, "fab_red", rx=-7)
    bx(0, -.2, .75, .12, .01, .3, "black")


@item("duduk", "kursi_eksekutif", "Kursi eksekutif", {"leather_brown": K})
def _():
    cy(0, 0, .04, .07, .07, .38, "chrome"); _star(m="chrome")
    bx(0, 0, .42, .54, .52, .1, "leather_brown")
    bx(0, -.23, .5, .5, .1, .9, "leather_brown", rx=-6)
    bx(0, -.26, 1.3, .38, .08, .22, "leather_brown", rx=-6)
    for s in (-1, 1):
        bx(s * .31, .0, .62, .06, .34, .04, "chrome"); bx(s * .31, .05, .5, .03, .03, .13, "chrome")


@item("duduk", "kursi_jaring", "Kursi jaring (ergonomis)", {"fab_teal": K})
def _():
    cy(0, 0, .04, .07, .07, .38, "metal_dark"); _star()
    bx(0, 0, .42, .5, .5, .06, "fab_teal")
    bx(0, -.24, .55, .48, .04, .62, "metal_dark", rx=-6)
    for i in range(5):
        bx(0, -.255, .6 + i * .12, .42, .02, .05, "grey", rx=-6)
    for s in (-1, 1):
        bx(s * .29, .0, .6, .04, .3, .03, "black"); bx(s * .29, .05, .5, .03, .03, .1, "black")


@item("duduk", "kursi_lipat", "Kursi lipat", {"wood": W})
def _():
    for s in (-1, 1):
        bx(s * .2, .0, 0, .03, .03, .46, "metal_dark", ry=0, rx=14); bx(s * .2, .0, 0, .03, .03, .46, "metal_dark", rx=-14)
    bx(0, 0, .43, .42, .4, .035, "wood"); bx(0, -.2, .55, .42, .03, .3, "wood")
    for s in (-1, 1):
        bx(s * .2, -.2, .43, .03, .03, .45, "metal_dark")


@item("duduk", "bangku_bar", "Bangku bar bersandar", {"fab_rose": K})
def _():
    cy(0, 0, 0, .34, .34, .03, "metal_dark")
    cy(0, 0, 0, .05, .05, .72, "metal_dark", seg=8)
    cy(0, 0, .7, .38, .38, .08, "fab_rose")
    bx(0, -.17, .85, .34, .05, .3, "fab_rose")
    bx(0, -.17, .72, .03, .03, .15, "metal_dark")
    cy(0, 0, .28, .26, .26, .02, "metal_dark")


@item("duduk", "bangku_panjang", "Bangku panjang", {"wood": W})
def _():
    bx(0, 0, .42, 1.4, .4, .05, "wood")
    for s in (-1, 1):
        bx(s * .6, 0, 0, .05, .36, .42, "metal_dark"); bx(s * .6, 0, 0, .05, .4, .04, "metal_dark")
    bx(0, 0, .15, 1.2, .04, .04, "metal_dark")


@item("duduk", "kursi_bulat", "Kursi bulat (tub)", {"fab_yellow": K})
def _():
    cy(0, 0, .1, .55, .55, .3, "fab_yellow")
    sp(0, -.08, .5, .62, .5, .55, "fab_yellow", seg=12)
    sp(0, .05, .38, .5, .5, .2, "fab_yellow", seg=10)
    for dx, dy in ((.2, .2), (-.2, .2), (.2, -.2), (-.2, -.2)):
        cy(dx, dy, 0, .05, .05, .12, "wood_dark", r2=.7, seg=6)


@item("duduk", "sofa_sudut", "Sofa sudut (L)", {"fab_grey": K, "fab_orange": K})
def _():
    c = "fab_grey"
    bx(0, 0, .1, 2.6, .9, .3, c); bx(0, -.4, .35, 2.6, .18, .5, c)
    bx(-1.25, 0, .1, .2, .9, .55, c)
    bx(1.0, 1.2, .1, .9, 1.5, .3, c); bx(1.45, 1.2, .35, .18, 1.5, .5, c)
    for dx in (-.6, .55):
        bx(dx, .05, .4, 1.05, .7, .12, c)
    bx(1.0, 1.2, .4, .7, 1.3, .12, c)
    for dx, rz in ((-.9, -8), (.3, 8)):
        bx(dx, -.25, .5, .36, .12, .36, "fab_orange", rx=-15, rz=rz)
    for dx, dy in ((-1.25, .4), (1.35, .4), (-1.25, -.4), (1.35, 1.9), (.6, 1.9)):
        bx(dx, dy, 0, .06, .06, .1, "wood_dark")


@item("duduk", "sofa_dua", "Sofa 2 dudukan", {"fab_teal": K, "fab_yellow": K})
def _():
    U.sofa(0, 0, 0, col="fab_teal", w=1.6, pillows=("fab_yellow",))


@item("duduk", "sofa_panjang", "Sofa panjang 4 dudukan", {"fab_burgundy": K, "fab_cream": K})
def _():
    U.sofa(0, 0, 0, col="fab_burgundy", w=3.2, pillows=("fab_cream", "fab_cream", "fab_cream"))


@item("duduk", "puf", "Puf / ottoman", {"fab_purple": K})
def _():
    cy(0, 0, 0, .55, .55, .4, "fab_purple", r2=.95, seg=16)
    bx(0, 0, .4, .02, .02, .02, "wood_dark")
    cy(0, 0, .39, .5, .5, .03, "fab_purple", seg=16)


@item("duduk", "beanbag_besar", "Beanbag besar", {"fab_blue": K})
def _():
    U.beanbag(0, 0, "fab_blue", 1.4)


@item("duduk", "bangku_kayu_kecil", "Bangku kayu kecil", {"wood": W})
def _():
    bx(0, 0, .3, .34, .3, .04, "wood")
    for dx in (-.13, .13):
        for dy in (-.11, .11):
            bx(dx, dy, 0, .04, .04, .3, "wood_dark", rx=dy * 40, ry=-dx * 40)


# ------------------------------------------------------------------ MEJA
@item("meja", "meja_berdiri", "Meja berdiri (standing desk)", {"desk_white": W})
def _():
    bx(0, 0, .98, 1.4, .7, .04, "desk_white")
    for s in (-1, 1):
        bx(s * .55, 0, .04, .08, .5, .94, "metal_dark"); bx(s * .55, 0, 0, .08, .66, .05, "metal_dark")
    bx(0, -.3, .9, 1.1, .02, .1, "metal_dark")
    U.monitor(0, -.18, 1.02); bx(0, .2, 1.02, .44, .15, .02, "white"); bx(.4, .22, 1.02, .06, .1, .03, "white")
    bx(.55, .0, .84, .1, .04, .06, "scr_green")


@item("meja", "meja_L", "Meja kerja bentuk L", {"desk_wood": W})
def _():
    bx(0, 0, .72, 1.8, .7, .04, "desk_wood"); bx(-.55, .95, .72, .7, 1.2, .04, "desk_wood")
    for p in ((.85, .3), (.85, -.3), (-.85, -.3), (-.85, 1.5), (-.25, 1.5)):
        bx(p[0], p[1], 0, .05, .05, .72, "metal_dark")
    bx(.3, 0, .3, .5, .6, .42, "desk_wood")
    for k in range(2):
        bx(.3, .31, .36 + k * .2, .44, .01, .16, "wood_dark"); bx(.3, .32, .42 + k * .2, .1, .01, .02, "chrome")
    U.monitor(0, -.15, .76); bx(0, .2, .76, .44, .15, .02, "white"); bx(-.55, 1.0, .76, .3, .4, .02, "paper")


@item("meja", "meja_gaming", "Meja gaming + 2 monitor", {"black": W, "neon_blue": S})
def _():
    bx(0, 0, .74, 1.8, .8, .05, "black")
    for s in (-1, 1):
        bx(s * .8, 0, 0, .06, .7, .74, "metal_dark")
    bx(0, .39, .73, 1.7, .01, .015, "neon_blue"); bx(0, -.35, .79, 1.6, .02, .015, "neon_blue")
    U.monitor(-.38, -.2, .79, "scr_violet", w=.6, h=.36); U.monitor(.38, -.2, .79, "scr_teal", w=.6, h=.36)
    bx(0, .2, .79, .5, .16, .02, "black"); bx(0, .2, .81, .46, .12, .008, "neon_pink")
    bx(.6, .15, .79, .08, .12, .03, "black"); bx(.75, -.25, .79, .22, .18, .5, "black"); bx(.75, -.14, 1.0, .02, .01, .2, "neon_green")


@item("meja", "meja_bulat_rapat", "Meja bulat rapat + 4 kursi", {"wood": W})
def _():
    cy(0, 0, .72, 1.5, 1.5, .05, "wood", seg=24); cy(0, 0, .04, .12, .12, .68, "metal_dark"); cy(0, 0, 0, .7, .7, .04, "metal_dark", seg=20)
    for k in range(4):
        t = math.radians(k * 90)
        U.chair(1.05 * math.sin(t), -1.05 * math.cos(t), k * 90, ["fab_blue", "fab_teal", "fab_rose", "fab_sage"][k])


@item("meja", "meja_lipat", "Meja lipat", {"desk_white": W})
def _():
    bx(0, 0, .72, 1.2, .6, .03, "desk_white")
    for s in (-1, 1):
        bx(s * .5, 0, 0, .03, .03, .74, "metal_dark", rx=18); bx(s * .5, 0, 0, .03, .03, .74, "metal_dark", rx=-18)
        bx(s * .5, 0, .35, .03, .45, .03, "metal_dark")


@item("meja", "meja_samping", "Meja samping bulat", {"wood": W})
def _():
    cy(0, 0, .48, .5, .5, .04, "wood", seg=18); cy(0, 0, .03, .05, .05, .45, "metal_dark", seg=8); cy(0, 0, 0, .3, .3, .03, "metal_dark", seg=14)


@item("meja", "meja_kopi_bulat", "Meja kopi bulat", {"wood": W})
def _():
    cy(0, 0, .38, .9, .9, .05, "wood", seg=20)
    for a in (0, 120, 240):
        r = math.radians(a)
        bx(.3 * math.cos(r), .3 * math.sin(r), 0, .05, .05, .39, "metal_dark")
    cy(.1, 0, .43, .12, .12, .1, "pot_w")


@item("meja", "meja_kopi_kaca", "Meja kopi kaca", {"chrome": L})
def _():
    bx(0, 0, .38, 1.1, .6, .02, "glass")
    for dx in (-.5, .5):
        for dy in (-.25, .25):
            bx(dx, dy, 0, .03, .03, .38, "chrome")
    bx(0, 0, .12, 1.0, .5, .02, "chrome")
    bx(-.2, 0, .4, .22, .16, .03, "blue"); bx(-.2, 0, .43, .2, .15, .03, "red", rz=8)


@item("meja", "meja_kerja_kecil", "Meja kerja kecil", {"desk_white": W, "desk_wood": W})
def _():
    bx(0, 0, .72, 1.1, .55, .04, "desk_white")
    bx(-.5, 0, 0, .05, .5, .72, "desk_wood"); bx(.5, 0, 0, .05, .5, .72, "desk_wood")
    bx(0, -.25, .3, 1.0, .03, .4, "desk_wood")
    bx(.3, .0, .52, .35, .5, .2, "desk_wood"); bx(.3, .26, .58, .1, .01, .02, "chrome")
    U.monitor(-.1, -.12, .76, "scr_rose", w=.5, h=.3)


@item("meja", "meja_rapat_kecil", "Meja rapat kecil + 6 kursi", {"wood": W})
def _():
    bx(0, 0, .72, 2.4, 1.1, .05, "wood")
    for dx in (-1.0, 1.0):
        bx(dx, 0, 0, .08, .9, .72, "metal_dark")
    for i in range(3):
        px = -.7 + i * .7
        U.chair(px, .95, 180, "fab_grey"); U.chair(px, -.95, 0, "fab_grey")
    bx(0, 0, .77, .4, .1, .03, "black"); cy(-.6, .15, .77, .25, .25, .28, "chrome", r2=.85)


@item("meja", "meja_makan_bulat", "Meja makan bulat + 3 kursi", {"oak": W})
def _():
    cy(0, 0, .72, 1.1, 1.1, .05, "oak", seg=20); cy(0, 0, 0, .1, .1, .72, "wood_dark", seg=8); cy(0, 0, 0, .6, .6, .04, "wood_dark", seg=16)
    cy(0, 0, .77, .14, .14, .1, "pot_w"); sp(0, 0, .95, .17, .17, .14, "leaf2", seg=6)
    for k in range(3):
        t = math.radians(k * 120)
        U.plain_chair(.85 * math.sin(t), -.85 * math.cos(t), k * 120, ["fab_teal", "fab_rose", "fab_sage"][k])


@item("meja", "meja_tinggi_pantry", "Meja tinggi + 2 bangku", {"wood": W})
def _():
    bx(0, 0, 1.0, 1.3, .6, .05, "wood")
    for dx in (-.55, .55):
        for dy in (-.22, .22):
            bx(dx, dy, 0, .05, .05, 1.0, "metal_dark")
    bx(0, 0, .3, 1.1, .4, .02, "metal_dark")
    U.stool(-.35, .7, "fab_orange", h=.65); U.stool(.35, .7, "fab_teal", h=.65)


# ------------------------------------------------------------------ SIMPAN
@item("simpan", "rak_buku_pendek", "Rak buku pendek", {"wood_dark": W, "wood": W})
def _():
    U.bookshelf(0, 0, 0, w=1.2, h=.9)


@item("simpan", "rak_buku_lebar", "Rak buku lebar", {"wood_dark": W, "wood": W})
def _():
    U.bookshelf(0, 0, 0, w=2.0, h=1.8)


@item("simpan", "rak_kubus", "Rak kubus 3x3", {"desk_white": W})
def _():
    n = 3; s = .4
    for i in range(n + 1):
        bx(0, 0, i * s, n * s + .04, .36, .035, "desk_white"); bx(-n * s / 2 + i * s, 0, 0, .035, .36, n * s + .035, "desk_white")
    bx(0, -.17, 0, n * s + .04, .02, n * s + .035, "wood")
    cols = ["red", "blue", "green", "yellow", "orange", "purple"]
    k = 0
    for r in range(n):
        for c in range(n):
            if (r + c) % 2 == 0:
                bx(-s + c * s, .0, r * s + .04, .3, .28, .22, cols[k % 6]); k += 1
            elif r == 1:
                U.figure(-s + c * s, 0, r * s + .04, 0, "red", 1.4, c % 2)


@item("simpan", "rak_metal", "Rak terbuka metal", {"metal_dark": L, "wood": W})
def _():
    for sx in (-.55, .55):
        for sy in (-.2, .2):
            bx(sx, sy, 0, .04, .04, 1.8, "metal_dark")
    for k in range(5):
        bx(0, 0, .15 + k * .4, 1.2, .46, .03, "wood")
    for k, c in enumerate(["cardboard", "crate_blue", "cardboard", "crate_orange"]):
        bx(-.25 + (k % 2) * .5, 0, .18 + k * .4, .38, .34, .22, c)


@item("simpan", "lemari_laci", "Lemari laci (dresser)", {"wood": W})
def _():
    bx(0, 0, .08, 1.0, .45, .8, "wood"); bx(0, 0, .86, 1.04, .48, .04, "oak")
    for dx in (-.15, .15):
        pass
    for k in range(3):
        bx(0, .226, .14 + k * .25, .92, .01, .21, "oak"); bx(0, .235, .22 + k * .25, .16, .02, .03, "chrome")
    for sx in (-.45, .45):
        for sy in (-.18, .18):
            bx(sx, sy, 0, .05, .05, .08, "wood_dark")


@item("simpan", "loker_2", "Loker 2 pintu", {"fab_red": C, "fab_yellow": C})
def _():
    U.locker_row(0, 0, n=2, cols=("fab_red", "fab_yellow"))


@item("simpan", "loker_6", "Loker 6 pintu (2 tingkat)", {"fab_blue": C, "fab_teal": C, "fab_sage": C})
def _():
    U.locker_row(0, 0, n=3, cols=("fab_blue", "fab_teal", "fab_sage"), h=.9)
    with at(0, 0, .9):
        U.locker_row(0, 0, n=3, cols=("fab_teal", "fab_sage", "fab_blue"), h=.9)


@item("simpan", "lemari_kaca", "Lemari pajangan kaca", {"wood": W})
def _():
    bx(0, 0, 0, 1.0, .4, 1.7, "wood")
    bx(0, .21, .08, .88, .01, 1.5, "glass")
    for k in range(4):
        bx(0, 0, .15 + k * .4, .9, .38, .02, "wood_dark")
    U.trophy(-.2, 0, .17); U.trophy(.2, 0, .57); U.figure(0, 0, .97, 0, "blue", 1.4); U.trophy(-.2, 0, 1.37)
    bx(0, .215, .75, .03, .01, .2, "chrome")


@item("simpan", "kabinet_dinding", "Kabinet dinding", {"wood": W}, "wall", 1.6)
def _():
    bx(0, 0, 0, 1.4, .35, .7, "wood")
    for s in (-1, 1):
        bx(s * .34, .18, .04, .64, .01, .62, "oak"); bx(s * .06, .19, .3, .02, .02, .14, "chrome")


@item("simpan", "rak_majalah", "Rak majalah", {"metal_dark": L})
def _():
    cy(0, 0, 0, .35, .35, .03, "metal_dark")
    bx(0, -.05, .03, .04, .04, 1.0, "metal_dark")
    for k in range(4):
        bx(0, .02, .25 + k * .22, .5, .06, .16, ["note_b", "note_p", "note_y", "note_g"][k], rx=-12)
        bx(0, .07, .22 + k * .22, .52, .02, .03, "metal_dark")


@item("simpan", "peti_tumpuk", "Peti tumpuk", {"crate_blue": C, "crate_orange": C})
def _():
    for k, (c, dx) in enumerate((("crate_blue", -.25), ("crate_orange", .25))):
        bx(dx, 0, 0, .46, .36, .3, c)
        for i in range(3):
            bx(dx, .185, .05 + i * .08, .38, .01, .03, "metal_dark")
    bx(0, 0, .3, .46, .36, .3, "crate_blue", rz=6)


@item("simpan", "rak_sepatu_tinggi", "Rak sepatu tinggi", {"wood": W})
def _():
    bx(0, 0, 0, .8, .3, 1.2, "wood")
    for k in range(5):
        bx(0, .0, .06 + k * .22, .74, .31, .02, "wood_dark")
        for i in range(2):
            bx(-.18 + i * .36, 0, .08 + k * .22, .16, .24, .1, ["red", "blue", "yellow", "green", "orange"][(i + k) % 5])


@item("simpan", "gantungan_dinding", "Gantungan dinding", {"wood": W}, "wall", 1.5)
def _():
    bx(0, 0, 0, 1.0, .03, .12, "wood")
    for k in range(4):
        bx(-.36 + k * .24, .04, .04, .03, .06, .03, "chrome")
    bx(-.12, .06, -.5, .22, .06, .54, "fab_navy"); bx(.36, .06, -.4, .22, .06, .44, "fab_red")


@item("simpan", "tong_kardus", "Kardus arsip", {"cardboard": C})
def _():
    for dx, dz, w in ((-.2, 0, .4), (.22, 0, .36), (0, .26, .38)):
        bx(dx, 0, dz, w, .34, .26, "cardboard"); bx(dx, .175, dz + .1, .16, .01, .04, "white")
