"""Varian baru: pantry/dapur, tidur, dekorasi dinding, tanaman, karpet."""
import math
from lib import bx, cy, sp, at
from registry import item
import furn_used as U

K = "kain"; W = "kayu"; C = "cat"; L = "logam"; S = "layar"; P = "karpet"; D = "daun"; PT = "pot"


# ------------------------------------------------------------------ DAPUR
@item("dapur", "kulkas_mini", "Kulkas mini", {"white": C})
def _():
    bx(0, 0, 0, .52, .5, .85, "white"); bx(0, .251, .55, .5, .005, .01, "grey")
    bx(.2, .26, .62, .03, .03, .15, "chrome"); bx(.2, .26, .3, .03, .03, .15, "chrome")
    bx(-.05, .256, .15, .2, .005, .15, "note_y")


@item("dapur", "kulkas_besar", "Kulkas 2 pintu", {"metal": L})
def _():
    bx(0, 0, 0, 1.0, .72, 1.85, "metal")
    bx(0, .361, .02, .01, .005, 1.8, "black")
    for s in (-1, 1):
        bx(s * .08, .37, .8, .03, .03, .4, "chrome")
    bx(-.25, .365, 1.5, .3, .005, .22, "scr_dark"); bx(-.25, .372, 1.6, .06, .005, .04, "scr_blue")
    for dx in (-.4, .4):
        bx(dx, 0, 0, .12, .6, .06, "black")


@item("dapur", "mesin_kopi", "Mesin kopi", {"black": L}, "table")
def _():
    bx(0, 0, 0, .34, .3, .06, "metal_dark"); bx(0, -.06, .06, .34, .18, .36, "black")
    bx(0, .04, .26, .3, .1, .08, "black"); bx(0, .1, .26, .03, .03, .06, "chrome")
    bx(.07, .1, .12, .12, .1, .005, "metal"); cy(0, .11, .07, .09, .09, .1, "fab_orange")
    bx(-.08, .12, .3, .1, .01, .06, "scr_green")


@item("dapur", "ketel_listrik", "Ketel listrik", {"white": C}, "table")
def _():
    cy(0, 0, 0, .2, .2, .22, "white", r2=.8, seg=14); cy(0, 0, .22, .1, .1, .04, "black", seg=10)
    bx(.12, 0, .05, .04, .03, .16, "black"); bx(-.12, .02, .15, .08, .03, .03, "white")
    cy(0, 0, 0, .24, .24, .03, "black", seg=14)


@item("dapur", "toaster", "Pemanggang roti", {"chrome": L}, "table")
def _():
    bx(0, 0, 0, .3, .18, .18, "chrome"); bx(-.06, 0, .18, .08, .02, .01, "black"); bx(.06, 0, .18, .08, .02, .01, "black")
    bx(.15, 0, .08, .02, .06, .04, "black"); bx(.1, .095, .08, .05, .01, .05, "scr_warm")
    bx(-.06, 0, .17, .08, .04, .06, "cardboard", rz=0)


@item("dapur", "rak_piring", "Rak piring", {"metal_dark": L}, "table")
def _():
    bx(0, 0, 0, .5, .3, .03, "metal_dark")
    for k in range(5):
        bx(-.18 + k * .09, 0, .03, .01, .22, .02, "metal_dark")
        bx(-.18 + k * .09, 0, .05, .02, .2, .2, "white")


@item("dapur", "tempat_sampah_pedal", "Tempat sampah pedal", {"metal": L})
def _():
    cy(0, 0, 0, .34, .34, .55, "metal", r2=1.05, seg=16); cy(0, 0, .55, .36, .36, .05, "metal_dark", seg=16)
    bx(0, .12, 0, .1, .1, .03, "black"); bx(0, .0, .6, .05, .05, .03, "black")


@item("dapur", "tong_sampah_kotak", "Tong sampah kotak", {"grey": C})
def _():
    bx(0, 0, 0, .38, .3, .55, "grey"); bx(0, 0, .55, .4, .32, .04, "metal_dark"); bx(0, .17, .3, .2, .01, .12, "black")


@item("dapur", "pulau_dapur", "Pulau dapur + 2 bangku", {"wood": W, "counter": W})
def _():
    bx(0, 0, 0, 1.8, .8, .9, "wood"); bx(0, 0, .9, 1.9, .9, .05, "counter")
    for k in range(3):
        bx(-.55 + k * .55, .401, .1, .5, .005, .72, "wood_dark"); bx(-.55 + k * .55, .408, .7, .1, .005, .02, "chrome")
    cy(.5, .1, .95, .3, .3, .06, "white"); cy(-.4, 0, .95, .22, .22, .14, "pot_w"); sp(-.4, 0, 1.2, .2, .2, .16, "leaf2", seg=6)
    U.stool(-.4, -.8, "fab_orange", h=.72); U.stool(.4, -.8, "fab_teal", h=.72)


@item("dapur", "kompor_counter", "Kompor + counter", {"wood": W, "counter": W})
def _():
    bx(0, 0, 0, 1.2, .65, .85, "wood"); bx(0, 0, .85, 1.24, .7, .05, "counter")
    bx(0, .1, .9, .7, .45, .03, "black")
    for dx, dy in ((-.2, .05), (.2, .05), (-.2, .25), (.2, .25)):
        cy(dx, dy, .93, .14, .14, .015, "metal_dark", seg=12)
    cy(-.2, .05, .94, .22, .22, .12, "chrome", r2=.9); bx(-.2 - .18, .05, 1.0, .1, .03, .02, "black")
    for i in range(4):
        cy(-.3 + i * .2, .326, .6, .05, .05, .02, "chrome", rx=90, seg=8)
    bx(0, .328, .08, 1.0, .005, .45, "wood_dark")


@item("dapur", "wastafel", "Wastafel kantor", {"counter": W})
def _():
    bx(0, 0, 0, 1.0, .5, .85, "wood"); bx(0, 0, .85, 1.04, .54, .04, "counter")
    bx(0, 0, .88, .4, .3, .02, "metal"); cy(0, -.18, .9, .04, .04, .2, "chrome", seg=8); bx(0, -.1, 1.08, .04, .2, .04, "chrome")
    bx(0, -.27, .9, 1.04, .03, .35, "counter")
    bx(0, .252, .1, .9, .005, .7, "wood_dark")


@item("dapur", "vending_teal", "Vending machine (teal)", {"fab_teal": C})
def _():
    U.vending_machine(0, 0, 0, "fab_teal")


@item("dapur", "vending_kuning", "Vending machine (kuning)", {"fab_yellow": C})
def _():
    U.vending_machine(0, 0, 0, "fab_yellow")


@item("dapur", "galon_dispenser", "Dispenser galon", {"white": C})
def _():
    bx(0, 0, 0, .34, .34, .95, "white"); cy(0, 0, .95, .26, .26, .4, "glass"); cy(0, 0, .95, .22, .22, .3, "cyan", r2=.9)
    bx(0, .18, .78, .05, .04, .05, "blue"); bx(.08, .18, .78, .05, .04, .05, "red"); bx(0, .0, .24, .2, .18, .1, "grey")


@item("dapur", "rak_pantry", "Rak pantry (toples)", {"wood": W})
def _():
    for sx in (-.45, .45):
        bx(sx, 0, 0, .04, .3, 1.6, "wood_dark")
    for k in range(4):
        bx(0, 0, .1 + k * .45, .94, .3, .03, "wood")
        for i in range(4):
            cy(-.33 + i * .22, 0, .13 + k * .45, .14, .14, .2, "glass"); cy(-.33 + i * .22, 0, .13 + k * .45, .12, .12, .12,
                                                                          ["red", "yellow", "green", "orange", "pink"][(i + k) % 5])
            cy(-.33 + i * .22, 0, .33 + k * .45, .15, .15, .02, "metal")


@item("dapur", "kitchen_pendek", "Kitchen counter pendek", {"wood": W, "counter": W})
def _():
    U.kitchen_counter(0, 0, w=1.2, sink=False)


# ------------------------------------------------------------------ TIDUR
@item("tidur", "ranjang_double", "Ranjang double", {"fab_rose": K})
def _():
    bx(0, 0, .2, 1.6, 2.0, .15, "wood"); bx(0, 0, .35, 1.54, 1.96, .18, "bed_white")
    bx(0, .3, .53, 1.52, 1.4, .06, "fab_rose")
    for s in (-1, 1):
        bx(s * .4, -.78, .53, .5, .3, .12, "white", rx=-5)
    bx(0, -1.0, .2, 1.7, .08, 1.0, "wood_dark"); bx(0, 1.0, .2, 1.7, .06, .45, "wood_dark")
    for dx in (-.78, .78):
        bx(dx, -.97, 0, .08, .08, .2, "wood_dark"); bx(dx, .97, 0, .08, .08, .2, "wood_dark")


@item("tidur", "kasur_lantai", "Kasur lantai (futon)", {"fab_blue": K})
def _():
    bx(0, 0, 0, .95, 1.9, .14, "bed_white"); bx(0, .25, .14, .93, 1.4, .05, "fab_blue")
    bx(0, -.8, .14, .5, .3, .1, "white", rx=-5)


@item("tidur", "ranjang_anak", "Ranjang kecil + pagar", {"fab_yellow": K})
def _():
    bx(0, 0, .15, .8, 1.5, .1, "wood"); bx(0, 0, .25, .76, 1.46, .12, "bed_white"); bx(0, .1, .37, .74, 1.0, .04, "fab_yellow")
    bx(0, -.55, .37, .4, .25, .1, "white", rx=-5)
    for s in (-1, 1):
        bx(s * .39, 0, .25, .03, 1.5, .35, "wood_dark")
        for k in range(6):
            bx(s * .39, -.6 + k * .24, .25, .03, .03, .35, "wood")


@item("tidur", "kapsul_tidur", "Kapsul tidur (pod)", {"fab_navy": K})
def _():
    bx(0, 0, 0, 1.1, 2.2, .3, "metal_dark")
    sp(0, 0, .75, 1.0, 2.1, .9, "white", seg=16)
    bx(0, .8, .5, .7, .02, .3, "glass"); bx(0, .0, .31, .9, 1.9, .08, "fab_navy")
    bx(0, 1.05, .6, .3, .02, .06, "scr_teal")


# ------------------------------------------------------------------ DINDING (z=0 tepi bawah, punggung y=0)
def _frame(w, h, fr="wood_dark", pic="note_b", pic2="red"):
    U.frame(0, 0, 0, w=w, h=h, pic=pic, fr=fr, pic2=pic2)


@item("dinding", "bingkai_lanskap", "Bingkai lanskap", {"wood_dark": W, "note_g": C}, "wall")
def _():
    _frame(1.0, .5, pic="note_g", pic2="blue")


@item("dinding", "bingkai_potret", "Bingkai potret", {"wood_dark": W}, "wall")
def _():
    _frame(.45, .65, pic="note_p", pic2="purple")


@item("dinding", "bingkai_set3", "Bingkai set 3", {"wood_dark": W}, "wall")
def _():
    for dx, w, h, p in ((-.5, .4, .5, "note_y"), (0, .45, .65, "note_b"), (.5, .4, .5, "note_g")):
        with at(dx, 0, 0):
            U.frame(0, 0, 0, w=w, h=h, pic=p, pic2="orange")


@item("dinding", "bingkai_bulat", "Cermin/bingkai bulat", {"brass": L}, "wall")
def _():
    cy(0, 0, 0, .6, .04, .6, "brass", rx=90, seg=24); cy(0, .015, 0, .52, .02, .52, "mirror", rx=90, seg=24)


@item("dinding", "jam_kotak", "Jam kotak", {"wood": W}, "wall", 2.2)
def _():
    bx(0, 0, 0, .45, .05, .45, "wood"); bx(0, .026, .04, .37, .01, .37, "white")
    bx(0, .035, .225, .015, .01, .12, "black"); bx(.05, .035, .225, .1, .01, .015, "black")
    for a in (0, 90, 180, 270):
        bx(.15 * math.sin(math.radians(a)), .035, .225 + .15 * math.cos(math.radians(a)) - .02, .02, .008, .04, "metal_dark")


@item("dinding", "jam_digital", "Jam digital", {"black": L}, "wall", 2.4)
def _():
    bx(0, 0, 0, .6, .06, .2, "black"); bx(0, .032, .03, .54, .01, .14, "scr_dark")
    for i, dx in enumerate((-.2, -.08, .08, .2)):
        bx(dx, .04, .06, .06, .005, .08, "red")
    cy(0, .04, .1, .02, .02, .02, "red", seg=6, rx=90)


@item("dinding", "papan_pengumuman", "Papan pengumuman gabus", {"wood": W}, "wall")
def _():
    bx(0, 0, 0, 1.2, .05, .8, "wood"); bx(0, .028, .04, 1.12, .01, .72, "board_cork")
    for i, (dx, dz, c) in enumerate(((-.35, .45, "note_y"), (0, .35, "paper"), (.35, .42, "note_b"), (-.2, .12, "note_p"), (.25, .12, "note_g"))):
        bx(dx, .04, dz, .26, .006, .22, c, rz=(i * 7) % 11 - 5); cy(dx, .048, dz + .17, .03, .03, .015, "red", rx=90, seg=6)


@item("dinding", "papan_kaca", "Papan kaca (glassboard)", {"metal": L}, "wall")
def _():
    bx(0, 0, 0, 1.8, .05, 1.0, "metal"); bx(0, .028, .03, 1.74, .01, .94, "glass")
    for i, c in enumerate(["blue", "red", "green"]):
        bx(-.4 + i * .1, .04, .55 + i * .12, .6 - i * .1, .006, .02, c)
    bx(.45, .04, .2, .4, .006, .3, "note_y"); bx(0, .06, -.02, .5, .08, .03, "metal")


@item("dinding", "rak_melayang_3", "Rak melayang 3 tingkat", {"wood": W}, "wall", 1.2)
def _():
    for k in range(3):
        bx(0, 0, k * .4, 1.0, .22, .035, "wood")
    U.book_stack(-.3, .05, .035); cy(.2, .0, .035, .13, .13, .14, "pot_w"); sp(.2, 0, .27, .15, .15, .12, "leaf2", seg=6)
    U.figure(0, .0, .435, 0, "blue", 1.4); U.trophy(-.3, 0, .435)
    U.book_stack(.2, .05, .835); cy(-.25, 0, .835, .1, .1, .12, "fab_orange")


@item("dinding", "poster_lebar", "Poster lebar", {"blue": C}, "wall")
def _():
    U.poster(0, 0, 0, w=.9, h=.5, col="blue")


@item("dinding", "poster_tinggi", "Poster tinggi", {"red": C}, "wall")
def _():
    U.poster(0, 0, 0, w=.5, h=.9, col="red")


@item("dinding", "poster_set3", "Poster set 3", {"green": C}, "wall")
def _():
    for i, c in enumerate(("green", "green", "green")):
        U.poster(-.6 + i * .6, 0, 0, w=.5, h=.7, col=c)


@item("dinding", "cermin_tinggi", "Cermin tinggi", {"wood_dark": W}, "wall", .2)
def _():
    bx(0, 0, 0, .55, .04, 1.5, "wood_dark"); bx(0, .022, .05, .45, .01, 1.4, "mirror")


@item("dinding", "kalender", "Kalender dinding", {"red": C}, "wall")
def _():
    bx(0, 0, 0, .4, .02, .55, "white"); bx(0, .012, .4, .4, .01, .15, "red")
    for i in range(4):
        for j in range(3):
            bx(-.13 + i * .09, .014, .06 + j * .09, .05, .005, .05, "grey")
    cy(0, .02, .54, .03, .03, .02, "metal_dark", rx=90, seg=6)


@item("dinding", "papan_tanda", "Papan nama kantor", {"wood_dark": W, "gold": L}, "wall", 2.0)
def _():
    bx(0, 0, 0, 1.6, .06, .35, "wood_dark")
    for i in range(8):
        bx(-.64 + i * .18, .035, .08, .12, .01, .19, "gold")


@item("dinding", "neon_sign", "Neon sign (bintang & garis)", {"neon_pink": S}, "wall")
def _():
    bx(0, 0, 0, 1.0, .02, .6, "black")
    for i in range(5):
        a = math.radians(i * 72 + 90)
        bx(.18 * math.cos(a), .02, .3 + .18 * math.sin(a), .04, .02, .22, "neon_pink", ry=math.degrees(-a) + 90 + 0)
    bx(.0, .02, .08, .8, .02, .03, "neon_blue")


@item("dinding", "tanaman_gantung_dinding", "Pot tanaman dinding", {"pot": PT, "leaf": D}, "wall", 1.5)
def _():
    bx(0, 0, 0, .3, .03, .5, "wood_dark")
    cy(0, .15, 0, .26, .26, .18, "pot", r2=.8)
    for i in range(4):
        sp((i - 1.5) * .06, .15, .26, .14, .14, .3, "leaf" if i % 2 else "leaf2", seg=6)
    for i in range(3):
        bx((i - 1) * .06, .17, -.2 - i * .1, .05, .03, .24 + i * .1, "leaf3")


@item("dinding", "lampu_dinding", "Lampu dinding", {"brass": L, "light": S}, "wall", 1.8)
def _():
    bx(0, 0, 0, .1, .03, .25, "brass"); cy(0, .08, .1, .06, .06, .1, "brass", rx=90, seg=8)
    cy(0, .18, .05, .2, .2, .22, "light", r2=.6, seg=10)


@item("dinding", "rambu_keluar", "Rambu EXIT", {"green": C}, "wall", 2.4)
def _():
    bx(0, 0, 0, .5, .06, .2, "green"); bx(0, .032, .03, .44, .01, .14, "white")
    bx(-.1, .04, .06, .12, .006, .06, "green"); bx(.1, .04, .08, .14, .006, .03, "green")


@item("dinding", "tirai_roman", "Tirai roman", {"fab_cream": P}, "wall")
def _():
    bx(0, 0, 1.2, 1.5, .05, .04, "metal_dark")
    for k in range(5):
        bx(0, .02 + (k % 2) * .01, 1.2 - .1 - k * .22, 1.4, .05, .2, "fab_cream")


@item("dinding", "tirai_gulung", "Tirai gulung", {"fab_sage": P}, "wall")
def _():
    bx(0, 0, 1.35, 1.4, .08, .08, "metal_dark")
    bx(0, .02, .3, 1.3, .02, 1.07, "fab_sage"); bx(0, .02, .26, 1.3, .03, .04, "metal_dark"); bx(0, .04, .1, .03, .01, .16, "white")


@item("dinding", "papan_kpi", "Papan KPI (grafik)", {"wood_dark": W}, "wall")
def _():
    bx(0, 0, 0, 1.6, .05, .9, "wood_dark"); bx(0, .028, .04, 1.52, .01, .82, "white")
    for i, h in enumerate((.2, .35, .28, .5, .6)):
        bx(-.6 + i * .15, .04, .12, .1, .01, h, ["blue", "cyan", "green", "orange", "red"][i])
    bx(.45, .04, .12, .45, .01, .5, "scr_teal")
    bx(.45, .05, .55, .3, .01, .03, "white"); bx(.45, .05, .4, .35, .01, .03, "white")


@item("dinding", "layar_status", "Layar status (dashboard)", {"scr_blue": S}, "wall")
def _():
    bx(0, 0, 0, 2.0, .07, 1.1, "black"); bx(0, .038, .05, 1.9, .01, 1.0, "scr_blue")
    for i, (w, c) in enumerate(((.55, "scr_green"), (.55, "scr_warm"), (.55, "scr_rose"))):
        bx(-.65 + i * .65, .05, .6, w, .01, .3, c)
    bx(0, .05, .15, 1.7, .01, .3, "scr_violet")


@item("dinding", "tv_dinding_besar", "TV dinding besar", {"scr_blue": S}, "wall")
def _():
    U.tv_wall(0, 0, 0, w=2.0)


# ------------------------------------------------------------------ TANAMAN
@item("tanaman", "monstera", "Monstera", {"pot": PT, "leaf": D, "leaf2": D}, "floor")
def _():
    cy(0, 0, 0, .4, .4, .4, "pot", r2=.8); cy(0, 0, .38, .34, .34, .03, "soil")
    for i in range(7):
        a = i * 51
        r = math.radians(a)
        bx(.08 * math.cos(r), .08 * math.sin(r), .4, .03, .03, .5 + (i % 3) * .1, "leaf3", rx=math.cos(r) * 20, ry=-math.sin(r) * 20)
        sp(.28 * math.cos(r), .28 * math.sin(r), .9 + (i % 3) * .12, .42, .42, .06, "leaf" if i % 2 else "leaf2", seg=8,
           rx=math.cos(r) * 25, ry=-math.sin(r) * 25)


@item("tanaman", "kaktus", "Kaktus", {"pot": PT, "cactus": D}, "floor")
def _():
    cy(0, 0, 0, .3, .3, .28, "pot", r2=.85); cy(0, 0, .26, .26, .26, .03, "soil")
    cy(0, 0, .28, .16, .16, .6, "cactus", seg=10); sp(0, 0, .88, .16, .16, .1, "cactus", seg=8)
    cy(.14, 0, .5, .08, .08, .2, "cactus", seg=8); bx(.07, 0, .5, .12, .06, .06, "cactus"); sp(.14, 0, .72, .08, .08, .06, "cactus", seg=6)


@item("tanaman", "bambu_pot", "Bambu dalam pot", {"pot_w": PT, "bamboo": D}, "floor")
def _():
    cy(0, 0, 0, .4, .4, .35, "pot_w", r2=.9); cy(0, 0, .33, .34, .34, .03, "soil")
    for i, (dx, dy, h) in enumerate(((0, 0, 1.4), (.08, .06, 1.1), (-.08, .05, 1.25), (.02, -.09, .95))):
        cy(dx, dy, .35, .05, .05, h, "bamboo", seg=6)
        for k in range(1, 4):
            cy(dx, dy, .35 + k * h / 4, .065, .065, .025, "leaf3", seg=6)
        sp(dx, dy, .35 + h, .14, .14, .2, "leaf2", seg=6)


@item("tanaman", "ficus_tinggi", "Ficus tinggi", {"pot_w": PT, "leaf": D, "leaf2": D}, "floor")
def _():
    cy(0, 0, 0, .5, .5, .45, "pot_w", r2=.85); cy(0, 0, .43, .44, .44, .03, "soil")
    cy(0, 0, .45, .07, .07, 1.2, "wood_dark", seg=6)
    for i, (dx, dy, dz, r) in enumerate(((0, 0, 1.95, .8), (.3, .1, 1.65, .6), (-.3, -.1, 1.6, .6), (.05, -.3, 1.4, .55), (-.1, .3, 1.35, .5))):
        sp(dx, dy, dz, r, r, r * .85, ["leaf", "leaf2", "leaf3"][i % 3], seg=8)


@item("tanaman", "palem", "Palem", {"pot": PT, "leaf": D}, "floor")
def _():
    cy(0, 0, 0, .5, .5, .4, "pot", r2=.85); cy(0, 0, .38, .44, .44, .03, "soil")
    cy(0, 0, .4, .08, .08, 1.0, "wood_dark", seg=6)
    for i in range(8):
        r = math.radians(i * 45)
        bx(.35 * math.cos(r), .35 * math.sin(r), 1.5 - (.1 if i % 2 else 0), .06, .5, .04, "leaf" if i % 2 else "leaf2",
           rz=i * 45 + 90)
        sp(.5 * math.cos(r), .5 * math.sin(r), 1.45 - (.12 if i % 2 else 0), .55, .16, .05, "leaf" if i % 2 else "leaf3", seg=6, rz=i * 45)
    sp(0, 0, 1.45, .2, .2, .16, "leaf2", seg=6)


@item("tanaman", "bunga_vas", "Bunga dalam vas", {"pot_w": PT, "pink": C}, "table")
def _():
    cy(0, 0, 0, .14, .14, .2, "pot_w", r2=.7, seg=10)
    for i, (dx, dy, h, c) in enumerate(((0, 0, .45, "pink"), (.05, .03, .38, "yellow"), (-.05, -.03, .4, "red"), (.02, -.05, .33, "pink"))):
        bx(dx * .6, dy * .6, .2, .01, .01, h - .1, "leaf3")
        sp(dx, dy, .2 + h - .08, .09, .09, .07, c, seg=6)


@item("tanaman", "bonsai", "Bonsai", {"pot": PT}, "table")
def _():
    bx(0, 0, 0, .3, .2, .06, "pot"); cy(0, 0, .06, .02, .02, .1, "wood_dark", seg=6)
    cy(.02, 0, .15, .04, .04, .14, "wood_dark", seg=6, rx=0, ry=15)
    for dx, dz, r in ((0, .3, .2), (.12, .24, .13), (-.1, .22, .12)):
        sp(dx, 0, dz, r, r, r * .7, "leaf", seg=7)


@item("tanaman", "tanaman_meja", "Tanaman meja kecil", {"pot": PT, "leaf2": D}, "table")
def _():
    cy(0, 0, 0, .14, .14, .12, "pot", r2=.8, seg=10)
    for i in range(5):
        r = math.radians(i * 72)
        sp(.04 * math.cos(r), .04 * math.sin(r), .2, .08, .08, .14, "leaf2", seg=6, rx=0)


@item("tanaman", "planter_panjang", "Kotak tanaman panjang", {"pot": PT, "leaf": D}, "floor")
def _():
    bx(0, 0, 0, 1.4, .35, .4, "pot"); bx(0, 0, .38, 1.34, .29, .03, "soil")
    for i in range(6):
        sp(-.55 + i * .22, 0, .6 + (i % 2) * .08, .26, .24, .3, ["leaf", "leaf2", "leaf3"][i % 3], seg=7)


@item("tanaman", "tanaman_gantung", "Tanaman gantung (langit-langit)", {"pot": PT, "leaf2": D}, "ceiling", 2.0)
def _():
    bx(0, 0, .75, .02, .02, .5, "metal_dark"); bx(0, 0, .65, .03, .03, .1, "metal_dark")
    cy(0, 0, .3, .3, .3, .22, "pot", r2=.7, seg=10)
    for i in range(6):
        r = math.radians(i * 60)
        bx(.12 * math.cos(r), .12 * math.sin(r), .0 - (i % 3) * .1, .04, .04, .35 + (i % 3) * .1, "leaf2")
    sp(0, 0, .55, .3, .3, .2, "leaf", seg=7)


# ------------------------------------------------------------------ KARPET
@item("karpet", "karpet_bulat", "Karpet bulat", {"rug_teal": P, "rug_cream": P})
def _():
    cy(0, 0, .02, 1.8, 1.8, .015, "rug_cream", seg=32); cy(0, 0, .035, 1.5, 1.5, .01, "rug_teal", seg=32); cy(0, 0, .045, 1.0, 1.0, .005, "rug_cream", seg=32)


@item("karpet", "karpet_garis", "Karpet garis", {"rug_blue": P, "rug_cream": P})
def _():
    bx(0, 0, .02, 2.2, 1.5, .015, "rug_cream")
    for i in range(5):
        bx(0, -.6 + i * .3, .035, 2.2, .14, .008, "rug_blue")


@item("karpet", "karpet_lari", "Karpet lari (runner)", {"rug_mustard": P, "rug_cream": P})
def _():
    bx(0, 0, .02, .9, 3.0, .015, "rug_cream"); bx(0, 0, .035, .72, 2.82, .01, "rug_mustard")
    for k in range(5):
        bx(0, -1.0 + k * .5, .045, .5, .08, .006, "rug_cream")


@item("karpet", "karpet_kotak", "Karpet kotak-kotak", {"rug_navy": P, "rug_cream": P})
def _():
    n = 6; s = .3
    for i in range(n):
        for j in range(n):
            bx((i - (n - 1) / 2) * s, (j - (n - 1) / 2) * s, .02, s, s, .012, "rug_navy" if (i + j) % 2 else "rug_cream")


@item("karpet", "keset", "Keset pintu", {"rug_charcoal": P})
def _():
    bx(0, 0, .02, .8, .5, .025, "rug_charcoal"); bx(0, 0, .045, .7, .4, .008, "rug_grey")
    bx(0, 0, .053, .5, .05, .005, "rug_charcoal")


@item("karpet", "karpet_besar_oval", "Karpet oval besar", {"rug_rose": P, "rug_cream": P})
def _():
    sp(0, 0, .03, 3.0, 2.0, .04, "rug_cream", seg=14); sp(0, 0, .04, 2.6, 1.6, .04, "rug_rose", seg=14)
    sp(0, 0, .05, 1.8, .9, .04, "rug_cream", seg=14)
