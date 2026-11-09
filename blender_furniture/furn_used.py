"""Perabot modular v5. Semua fungsi menerima (x, y, rot) dunia + opsi.
Depan item = +Y lokal. Meja: sisi pengguna = +Y."""
import random
from lib import bx, cy, sp, at, empty, mat

R = random.Random(7)


# ---------------------------------------------------------------- kursi & meja
def chair(x, y, rot=0, col="fab_blue", z=0):
    """Kursi putar. Depan (lutut) = +Y, sandaran di -Y."""
    with at(x, y, z, rot):
        cy(0, 0, .04, .07, .07, .38, "metal_dark")
        bx(0, 0, .05, .52, .06, .04, "black"); bx(0, 0, .05, .06, .52, .04, "black")
        for dx, dy in ((.26, 0), (-.26, 0), (0, .26), (0, -.26)):
            cy(dx, dy, 0, .06, .06, .05, "black", seg=8)
        bx(0, 0, .42, .46, .46, .07, col)
        bx(0, -.22, .5, .44, .06, .46, col)
        bx(.25, 0, .52, .04, .3, .03, "black"); bx(-.25, 0, .52, .04, .3, .03, "black")


def plain_chair(x, y, rot=0, col="wood", z=0):
    with at(x, y, z, rot):
        for dx in (-.18, .18):
            for dy in (-.18, .18):
                bx(dx, dy, 0, .04, .04, .42, "metal_dark")
        bx(0, 0, .42, .42, .42, .05, col)
        bx(0, -.2, .47, .42, .04, .42, col)


def stool(x, y, col="fab_orange", h=.65, z=0):
    with at(x, y, z):
        cy(0, 0, 0, .05, .05, h, "metal_dark", seg=8)
        cy(0, 0, h - .02, .36, .36, .08, col)
        cy(0, 0, 0, .34, .34, .03, "metal_dark")


def monitor(lx, ly, lz, scr="scr_blue", w=.56, h=.34):
    """Layar menghadap +Y lokal."""
    bx(lx, ly, lz, .22, .14, .02, "metal")
    bx(lx, ly, lz, .04, .04, .2, "metal")
    bx(lx, ly, lz + .12, w, .04, h, "black")
    bx(lx, ly + .022, lz + .15, w - .06, .01, h - .06, scr)


def desk(x, y, rot=0, scr="scr_blue", col="desk_white", tag=None):
    """Meja kerja lengkap + kursi pengguna. Sisi pengguna = +Y. Mengembalikan posisi kursi."""
    with at(x, y, 0, rot):
        bx(0, 0, .72, 1.5, .75, .04, col)
        bx(-.7, 0, 0, .05, .7, .72, "desk_wood")
        bx(.55, 0, 0, .4, .68, .72, "desk_wood")
        for k in range(3):
            bx(.55, .345, .08 + k * .22, .34, .01, .18, "wood_dark")
            bx(.55, .352, .15 + k * .22, .1, .01, .02, "chrome")
        bx(-.05, -.3, .22, 1.2, .03, .45, "desk_wood")
        monitor(0, -.18, .76, scr)
        bx(-.58, -.15, .76, .2, .38, .42, "black")           # PC tower
        bx(-.58, .045, .98, .08, .01, .02, "scr_green")
        bx(0, .2, .76, .44, .15, .02, "white")                # keyboard
        bx(.0, .2, .775, .4, .11, .01, "grey")
        bx(.38, .22, .76, .06, .1, .03, "white")              # mouse
        cy(-.4, .25, .76, .09, .09, .1, "fab_orange")          # mug
        figure(.62, .12, .76, -20, ["red", "blue", "green", "purple", "orange"][R.randrange(5)], .9, R.randrange(2))
        bx(-.2, .15, .76, .21, .29, .008, "paper")
        bx(.1, .3, .76, .21, .29, .008, "paper")
        cy(.62, -.25, .76, .13, .13, .02, "black")              # lampu meja
        bx(.62, -.25, .77, .02, .02, .3, "metal_dark")
        bx(.62, -.18, 1.04, .04, .16, .04, "metal_dark")
        bx(.62, -.12, 1.0, .12, .08, .04, "light")
        chair(0, .85, 180, ["fab_blue", "fab_teal", "fab_rose", "fab_sage", "fab_purple", "fab_orange"][R.randrange(6)])
        if tag:
            empty(f"SEAT_{tag}", 0, .85, 0, 180)


def partition_low(x, y, rot=0, w=1.6, col="fab_sage", h=.5):
    """Sekat rendah antar-meja."""
    with at(x, y, 0, rot):
        bx(0, 0, .72, w, .04, h, col)
        bx(0, 0, .72, w, .05, .03, "metal_dark")
        bx(-w / 2, 0, .72, .03, .08, h, "metal_dark"); bx(w / 2, 0, .72, .03, .08, h, "metal_dark")


# ---------------------------------------------------------------- tempat duduk santai
def sofa(x, y, rot=0, col="fab_navy", w=2.2, pillows=("fab_orange", "fab_cream"), z=0):
    with at(x, y, z, rot):
        bx(0, 0, .1, w, .9, .3, col)
        bx(0, -.4, .35, w, .18, .5, col)
        bx(-w / 2 + .1, 0, .1, .2, .9, .55, col); bx(w / 2 - .1, 0, .1, .2, .9, .55, col)
        for dx in (-w / 4 + .02, w / 4 - .02):
            bx(dx, .05, .4, w / 2 - .22, .7, .12, col)
        for i, pc in enumerate(pillows):
            bx(-w / 2 + .45 + i * (w - .9) / max(1, len(pillows) - 1), -.25, .5, .36, .12, .36, pc, rx=-15, rz=(8 if i % 2 else -8))
        bx(-w / 2 + .1, .4, 0, .06, .06, .1, "wood_dark"); bx(w / 2 - .1, .4, 0, .06, .06, .1, "wood_dark")
        bx(-w / 2 + .1, -.4, 0, .06, .06, .1, "wood_dark"); bx(w / 2 - .1, -.4, 0, .06, .06, .1, "wood_dark")


def armchair(x, y, rot=0, col="fab_rose", z=0):
    sofa(x, y, rot, col, w=.95, pillows=("fab_cream",), z=z)


def beanbag(x, y, col="fab_red", s=1.0):
    sp(x, y, .32 * s, .9 * s, .9 * s, .62 * s, col, seg=12)
    sp(x - .05 * s, y - .05 * s, .52 * s, .6 * s, .6 * s, .32 * s, col, seg=10)


def coffee_table(x, y, rot=0, w=1.1, d=.6, z=0):
    with at(x, y, z, rot):
        bx(0, 0, .35, w, d, .05, "wood")
        for dx in (-w / 2 + .05, w / 2 - .05):
            for dy in (-d / 2 + .05, d / 2 - .05):
                bx(dx, dy, 0, .05, .05, .35, "metal_dark")
        cy(.2, .0, .4, .12, .12, .1, "pot_w")


def rug(x, y, w, d, col="rug_red", border="rug_cream", rot=0, z=0):
    with at(x, y, z, rot):
        bx(0, 0, .02, w, d, .015, border)
        bx(0, 0, .035, w - .3, d - .3, .01, col)
        bx(0, 0, .045, w - .7, d - .7, .005, border)


# ---------------------------------------------------------------- dekor dinding
def frame(x, y, z, rot=0, w=.6, h=.45, pic="note_b", fr="wood_dark", pic2="red"):
    with at(x, y, z, rot):
        bx(0, 0, 0, w, .04, h, fr)
        bx(0, .022, .04, w - .08, .01, h - .08, "white")
        bx(0, .03, .08, w - .18, .01, h - .16, pic)
        bx(-w * .15, .035, .12, w * .25, .01, h * .3, pic2)


def team_photo(x, y, z, rot=0):
    """Foto tim: figur-figur kecil dalam bingkai besar."""
    with at(x, y, z, rot):
        bx(0, 0, 0, 1.2, .05, .8, "wood_dark")
        bx(0, .026, .05, 1.1, .01, .7, "wall_sky")
        bx(0, .03, .05, 1.1, .01, .2, "fl_a")
        cols = ["red", "blue", "green", "yellow", "purple", "orange", "pink", "cyan"]
        for i in range(8):
            px = -.46 + i * .13
            bx(px, .04, .12, .09, .01, .22, cols[i])
            sp(px, .042, .42, .08, .02, .09, "skin", seg=8)


def certificate(x, y, z, rot=0, w=.55, h=.4):
    with at(x, y, z, rot):
        bx(0, 0, 0, w, .03, h, "gold")
        bx(0, .02, .03, w - .06, .01, h - .06, "paper")
        bx(0, .03, h - .14, w * .55, .01, .03, "metal_dark")
        bx(0, .03, h - .22, w * .7, .01, .015, "grey")
        bx(0, .03, h - .27, w * .6, .01, .015, "grey")
        sp(w * .28, .03, .09, .07, .02, .07, "red", seg=8)


def org_chart(x, y, z, rot=0):
    """Bagan struktur tim ('chart') di dinding."""
    with at(x, y, z, rot):
        bx(0, 0, 0, 1.3, .04, .85, "wood_dark")
        bx(0, .022, .04, 1.22, .01, .77, "white")
        bx(0, .03, .6, .34, .01, .12, "blue")
        for dx in (-.4, 0, .4):
            bx(dx, .03, .3, .3, .01, .1, "green")
            bx(dx, .03, .5, .01, .01, .1, "metal_dark")
        bx(0, .03, .47, .8, .01, .01, "metal_dark")
        for dx in (-.5, -.3, -.1, .1, .3, .5):
            bx(dx, .03, .1, .17, .01, .08, "orange"); bx(dx, .03, .2, .01, .01, .1, "metal_dark")


def clock(x, y, z, rot=0):
    with at(x, y, z, rot):
        cy(0, 0, 0, .4, .04, .4, "wood_dark", rx=90)
        cy(0, .015, 0, .34, .04, .34, "white", rx=90)
        bx(0, .03, .0, .015, .01, .13, "black")
        bx(0, .03, .0, .1, .01, .015, "black", rz=0)


def whiteboard(x, y, z, rot=0, w=2.0, h=1.1, scribble=True):
    with at(x, y, z, rot):
        bx(0, 0, 0, w, .05, h, "metal")
        bx(0, .03, .04, w - .08, .01, h - .08, "board")
        bx(0, .04, -.03, w * .6, .08, .04, "metal")
        if scribble:
            for i, c in enumerate(["blue", "red", "green", "blue", "orange"]):
                bx(-w * .3 + (i % 3) * .1, .04, h - .25 - i * .13, w * (.3 + .05 * ((i * 3) % 4)), .01, .025, c)
            bx(w * .25, .04, .3, .4, .01, .3, "note_y")
            bx(w * .3, .04, .55, .25, .01, .25, "note_p")
        for i, c in enumerate(["red", "blue", "green"]):
            bx(-w * .15 + i * .1, .08, -.01, .09, .03, .02, c)


def task_board(x, y, z, rot=0, kind="daily"):
    """Papan tugas harian (3 kolom) / mingguan (5 kolom) berisi sticky note."""
    cols = 3 if kind == "daily" else 5
    w = 1.5 if kind == "daily" else 2.3
    h = 1.0
    heads = ["red", "orange", "green"] if kind == "daily" else ["blue", "cyan", "green", "yellow", "purple"]
    notes = ["note_y", "note_p", "note_g", "note_b", "note_o"]
    with at(x, y, z, rot):
        bx(0, 0, 0, w, .05, h, "wood_dark")
        bx(0, .028, .04, w - .08, .01, h - .08, "board_cork")
        cw = (w - .12) / cols
        for c in range(cols):
            cx = -w / 2 + .06 + cw * (c + .5)
            bx(cx, .036, h - .2, cw - .06, .008, .13, heads[c])
            if c:
                bx(cx - cw / 2, .036, .06, .012, .006, h - .3, "white")
            for k in range(R.randint(2, 4)):
                bx(cx + R.uniform(-.04, .04), .042, h - .4 - k * .2, .13, .006, .13, notes[R.randrange(5)],
                   rz=R.uniform(-6, 6))


def ac_unit(x, y, z, rot=0):
    with at(x, y, z, rot):
        bx(0, 0, 0, 1.0, .25, .3, "white")
        bx(0, .13, .04, .9, .01, .06, "grey")
        bx(0, .13, .12, .9, .01, .012, "grey"); bx(0, .13, .16, .9, .01, .012, "grey")
        bx(.38, .13, .21, .06, .01, .02, "scr_green")


def curtain(x, y, z, rot=0, w=1.8, h=1.6, col="fab_rose"):
    with at(x, y, z, rot):
        bx(0, 0, h, w + .2, .05, .04, "metal_dark")
        for s in (-1, 1):
            for k in range(3):
                bx(s * (w / 2 - .12 - k * .1), .02 + (k % 2) * .02, 0, .1, .05, h, col)


# ---------------------------------------------------------------- tanaman & kecil
def plant(x, y, s=1.0, z=0, kind=0):
    with at(x, y, z):
        cy(0, 0, 0, .34 * s, .34 * s, .38 * s, "pot", r2=.8)
        cy(0, 0, .36 * s, .3 * s, .3 * s, .03 * s, "soil")
        if kind == 0:
            for i, (dx, dy, hh) in enumerate([(0, 0, .6), (.1, .06, .45), (-.1, -.05, .5), (.04, -.1, .4)]):
                sp(dx * s, dy * s, (.36 + hh) * s, .34 * s, .34 * s, (.55 + .1 * (i % 2)) * s, ["leaf", "leaf2", "leaf3", "leaf"][i], seg=8)
        elif kind == 1:   # pohon tinggi
            cy(0, 0, .38 * s, .06 * s, .06 * s, .9 * s, "wood_dark", seg=6)
            for i, (dx, dy, dz) in enumerate([(0, 0, 1.45), (.2, .05, 1.2), (-.2, -.06, 1.15), (.0, -.2, 1.3), (.05, .2, 1.05)]):
                sp(dx * s, dy * s, dz * s, .5 * s, .5 * s, .45 * s, ["leaf", "leaf2", "leaf3"][i % 3], seg=8)
        else:             # sukulen
            for i in range(5):
                cy(R.uniform(-.06, .06) * s, R.uniform(-.06, .06) * s, .38 * s, .06 * s, .06 * s, R.uniform(.2, .4) * s, "leaf2", r2=.5, seg=6, rx=R.uniform(-15, 15))


def figure(x, y, z, rot=0, col="red", s=1.0, kind=0):
    """Action figure kecil di rak/meja."""
    with at(x, y, z, rot):
        cy(0, 0, 0, .1 * s, .1 * s, .015 * s, "black", seg=10)
        bx(-.015 * s, 0, .015 * s, .02 * s, .02 * s, .07 * s, "blue"); bx(.015 * s, 0, .015 * s, .02 * s, .02 * s, .07 * s, "blue")
        bx(0, 0, .085 * s, .06 * s, .035 * s, .08 * s, col)
        bx(-.045 * s, 0, .09 * s, .02 * s, .02 * s, .07 * s, col); bx(.045 * s, 0, .09 * s, .02 * s, .02 * s, .07 * s, col)
        sp(0, 0, .19 * s, .06 * s, .06 * s, .06 * s, "skin", seg=8)
        if kind == 1:
            cy(0, 0, .21 * s, .07 * s, .07 * s, .035 * s, "black", seg=8)


def trophy(x, y, z, rot=0):
    with at(x, y, z, rot):
        bx(0, 0, 0, .12, .12, .03, "wood_dark")
        cy(0, 0, .03, .03, .03, .1, "gold", seg=8)
        cy(0, 0, .13, .12, .12, .1, "gold", r2=.6, seg=10)


def bookshelf(x, y, rot=0, w=1.2, h=2.0, d=.35, z=0, fill=True, figs=False):
    with at(x, y, z, rot):
        bx(-w / 2 + .02, 0, 0, .04, d, h, "wood_dark"); bx(w / 2 - .02, 0, 0, .04, d, h, "wood_dark")
        bx(0, -d / 2 + .01, 0, w, .02, h, "wood")
        n = int(h / .38)
        for i in range(n + 1):
            bx(0, 0, i * (h - .04) / n, w - .04, d, .04, "wood_dark")
        if fill:
            cols = ["red", "blue", "green", "yellow", "purple", "orange", "fab_teal", "pink"]
            for i in range(n):
                zb = i * (h - .04) / n + .04
                if figs and i % 2 == 1:
                    figure(-w * .25, 0, zb, 0, cols[i % 8], 1.0, i % 2)
                    figure(w * .0, 0, zb, 0, cols[(i + 3) % 8], 1.1)
                    trophy(w * .28, 0, zb)
                    continue
                px = -w / 2 + .06
                while px < w / 2 - .12:
                    bw = R.uniform(.04, .08)
                    bx(px + bw / 2, .0, zb, bw, d * .8, R.uniform(.22, .3), cols[R.randrange(8)])
                    px += bw + .005


PAL_ok = {"red", "blue", "green", "yellow", "purple", "orange", "pink"}


def book_stack(lx, ly, lz):
    bx(lx, ly, lz, .22, .16, .03, "blue"); bx(lx, ly, lz + .03, .2, .15, .03, "red", rz=8); bx(lx, ly, lz + .06, .21, .15, .03, "green", rz=-5)


# ---------------------------------------------------------------- pantry & istirahat
def fridge(x, y, rot=0):
    with at(x, y, 0, rot):
        bx(0, 0, 0, .8, .7, 1.8, "white")
        bx(0, .351, .0, .8, .005, .01, "grey"); bx(0, .352, 1.17, .8, .005, .01, "grey")
        bx(.3, .36, .3, .03, .03, .5, "chrome"); bx(.3, .36, 1.3, .03, .03, .3, "chrome")
        bx(-.1, .355, 1.5, .25, .005, .2, "note_y"); bx(0, .355, .6, .12, .005, .1, "red")


def microwave(x, y, z, rot=0):
    with at(x, y, z, rot):
        bx(0, 0, 0, .52, .38, .3, "white")
        bx(-.07, .191, .04, .3, .005, .22, "scr_dark")
        bx(.19, .191, .04, .09, .005, .22, "grey")
        bx(.19, .195, .2, .05, .004, .03, "scr_green")


def vending_machine(x, y, rot=0, col="red"):
    with at(x, y, 0, rot):
        bx(0, 0, 0, 1.0, .8, 1.9, col)
        bx(-.1, .401, .45, .66, .01, 1.3, "scr_dark")
        sh = ["blue", "yellow", "green", "orange", "pink", "cyan"]
        for r in range(5):
            bx(-.1, .405, .5 + r * .25, .66, .01, .02, "chrome")
            for c in range(5):
                bx(-.37 + c * .135, .41, .53 + r * .25, .08, .05, .17, sh[(r + c) % 6])
        bx(.38, .402, .9, .16, .01, .5, "black")
        bx(.38, .41, 1.1, .1, .01, .1, "scr_green")
        bx(.38, .41, .95, .1, .01, .1, "chrome")
        bx(-.1, .405, .05, .66, .01, .26, "black")
        bx(-.1, .43, .12, .6, .04, .08, "metal_dark")
        bx(0, 0, 1.9, 1.0, .8, .06, "metal_dark")


def kitchen_counter(x, y, rot=0, w=2.4, sink=True):
    with at(x, y, 0, rot):
        bx(0, 0, 0, w, .65, .85, "wood")
        bx(0, 0, .85, w + .04, .7, .05, "counter")
        for i in range(int(w / .6)):
            bx(-w / 2 + .3 + i * .6, .326, .08, .52, .005, .7, "wood_dark")
            bx(-w / 2 + .3 + i * .6, .332, .7, .12, .005, .02, "chrome")
        if sink:
            bx(-.5, 0, .88, .5, .38, .02, "metal"); cy(-.5, -.2, .9, .04, .04, .2, "chrome", seg=8); bx(-.5, -.1, 1.08, .04, .2, .04, "chrome")
        bx(.55, -.1, .9, .3, .25, .3, "black")   # mesin kopi
        bx(.55, -.1 + .13, .98, .2, .01, .12, "scr_blue")
        cy(.9, .1, .9, .1, .1, .12, "fab_orange")


def snack_bar(x, y, rot=0, w=2.8):
    """Meja bar camilan + 3 stool."""
    with at(x, y, 0, rot):
        bx(0, 0, 0, w, .5, 1.0, "wood_dark")
        bx(0, .02, 1.0, w + .1, .7, .05, "counter")
        for i, c in enumerate(["red", "yellow", "green", "blue", "orange"]):
            cy(-w / 2 + .4 + i * .45, -.1, 1.05, .16, .16, .2, "glass")
            cy(-w / 2 + .4 + i * .45, -.1, 1.05, .14, .14, .12, c)
            cy(-w / 2 + .4 + i * .45, -.1, 1.25, .17, .17, .03, "metal")
        bx(w / 2 - .45, .1, 1.05, .35, .25, .06, "fab_orange"); bx(w / 2 - .45, .1, 1.11, .3, .2, .06, "fab_yellow")
        for i in range(3):
            stool(-w / 2 + .6 + i * (w - 1.2) / 2, .75, ["fab_orange", "fab_teal", "fab_rose"][i])


def dining_table(x, y, rot=0, w=1.6, d=.9, chairs=4):
    with at(x, y, 0, rot):
        bx(0, 0, .72, w, d, .05, "oak")
        for dx in (-w / 2 + .08, w / 2 - .08):
            for dy in (-d / 2 + .08, d / 2 - .08):
                bx(dx, dy, 0, .06, .06, .72, "wood_dark")
        cy(0, 0, .77, .12, .12, .1, "pot_w"); sp(0, 0, .95, .15, .15, .12, "leaf2", seg=6)
        for i in range(chairs):
            sx = -w / 4 + (i % 2) * w / 2
            if i < 2:
                plain_chair(sx, d / 2 + .4, 180, ["fab_teal", "fab_rose"][i % 2])
            else:
                plain_chair(sx, -d / 2 - .4, 0, ["fab_sage", "fab_orange"][i % 2])


def tv(x, y, rot=0, w=1.6, z=0):
    """TV + meja rendah + konsol."""
    with at(x, y, z, rot):
        bx(0, 0, 0, w + .4, .45, .45, "wood_dark")
        bx(-w * .3, .226, .1, .5, .005, .12, "black")
        bx(0, .0, .45, .5, .25, .02, "metal_dark")
        bx(0, 0, .47, .06, .06, .1, "metal_dark")
        bx(0, 0, .55, w, .06, .9, "black")
        bx(0, .032, .6, w - .1, .01, .8, "scr_blue")
        bx(-.2, .04, .75, .5, .01, .3, "scr_violet")
        bx(.3, .04, .9, .3, .01, .2, "scr_warm")
        # konsol
        bx(w * .3, .05, .47, .4, .28, .05, "ps_white"); bx(w * .3, .05, .47, .38, .26, .012, "black")  # PlayStation
        bx(w * .3 - .12, .19, .495, .01, .01, .01, "scr_blue")
        bx(w * .3 + .45, .05, .47, .26, .12, .17, "metal_dark")                                       # Nintendo dock
        bx(w * .3 + .45, .115, .5, .22, .01, .12, "scr_dark")
        bx(w * .3 + .45 - .22, .1, .48, .04, .05, .15, "red"); bx(w * .3 + .45 + .22, .1, .48, .04, .05, .15, "blue")


def game_board(x, y, rot=0, z=0):
    """Meja pendek dengan papan permainan + bidak + dadu."""
    with at(x, y, z, rot):
        bx(0, 0, .3, 1.0, 1.0, .05, "wood")
        for dx in (-.42, .42):
            for dy in (-.42, .42):
                bx(dx, dy, 0, .05, .05, .3, "wood_dark")
        bx(0, 0, .35, .8, .8, .02, "fab_cream")
        for i in range(4):
            for j in range(4):
                if (i + j) % 2:
                    bx(-.3 + i * .2, -.3 + j * .2, .37, .2, .2, .005, "red")
        for i, c in enumerate(["blue", "yellow", "green"]):
            cy(-.2 + i * .25, -.2 + i * .15, .37, .06, .06, .08, c, seg=8)
        bx(.3, .3, .37, .05, .05, .05, "white", rz=20)
        for dx, dy in ((-.8, 0), (.8, 0)):
            cy(dx, dy, 0, .6, .6, .3, "fab_orange", r2=.9)


def console_shelf(x, y, rot=0, z=0):
    bookshelf(x, y, rot, w=1.2, h=1.1, d=.35, z=z, fill=False)
    with at(x, y, z, rot):
        for i, c in enumerate(["red", "blue", "green", "yellow", "purple", "orange", "pink", "cyan"]):
            bx(-.5 + i * .13, .0, .04, .09, .3, .2, c)
            bx(-.5 + i * .13, .0, .48, .09, .3, .2, c)
        cy(0.3, 0, .9, .12, .12, .02, "black")
        figure(0.3, 0, .92, 0, "red", 1.2)


def gamepad(lx, ly, lz, col="blue"):
    bx(lx, ly, lz, .15, .09, .03, col)
    bx(lx - .05, ly, lz + .03, .03, .03, .01, "black"); bx(lx + .05, ly, lz + .03, .03, .03, .01, "black")


# ---------------------------------------------------------------- tidur
def bunk_bed(x, y, rot=0, c1="fab_blue", c2="fab_sage"):
    with at(x, y, 0, rot):
        for dx in (-.5, .5):
            for dy in (-1.0, 1.0):
                bx(dx, dy, 0, .08, .08, 1.9, "wood_dark")
        for z0, c in ((.3, c1), (1.2, c2)):
            bx(0, 0, z0, 1.0, 2.0, .1, "wood")
            bx(0, 0, z0 + .1, .94, 1.96, .16, "bed_white")
            bx(0, .2, z0 + .26, .92, 1.5, .05, c)
            bx(0, -.8, z0 + .26, .5, .3, .12, "white", rx=-5)
            bx(.5, 0, z0 + .1, .03, 2.0, .35, "wood_dark")
        bx(.55, -.85, .3, .04, .04, 1.5, "metal")
        for k in range(5):
            bx(.55, 1.0, .25 + k * .3, .06, .3, .03, "metal")
        bx(-.5, 0, .3, .04, 2.0, .3, "wood_dark")
        bx(-.5, 0, 1.2, .04, 2.0, .3, "wood_dark")
        sp(0, 0.2, 1.62, .5, .3, .3, c2, seg=6)


def single_bed(x, y, rot=0, col="fab_teal"):
    with at(x, y, 0, rot):
        bx(0, 0, .2, 1.0, 2.0, .15, "wood")
        bx(0, 0, .35, .94, 1.96, .16, "bed_white")
        bx(0, .25, .51, .92, 1.45, .05, col)
        bx(0, -.8, .51, .5, .3, .12, "white", rx=-5)
        bx(0, -1.0, .2, 1.0, .06, .7, "wood_dark")
        bx(0, 1.0, .2, 1.0, .06, .4, "wood_dark")
        for dx in (-.46, .46):
            bx(dx, -.97, 0, .06, .06, .2, "wood_dark"); bx(dx, .97, 0, .06, .06, .2, "wood_dark")


def locker_row(x, y, rot=0, n=4, cols=("fab_blue", "fab_teal", "fab_sage", "fab_orange"), h=1.9):
    with at(x, y, 0, rot):
        for i in range(n):
            px = (i - (n - 1) / 2) * .42
            bx(px, 0, 0, .4, .5, h, cols[i % len(cols)])
            bx(px, .26, h - .5, .22, .005, .04, "scr_dark")
            bx(px, .26, h - .9, .22, .005, .04, "scr_dark")
            bx(px + .12, .262, h * .55, .03, .02, .15, "chrome")
            bx(px, .26, .02, .3, .005, .05, "scr_dark")


def wardrobe(x, y, rot=0):
    with at(x, y, 0, rot):
        bx(0, 0, 0, 1.5, .6, 2.1, "wood")
        bx(-.38, .305, .05, .72, .01, 2.0, "oak"); bx(.38, .305, .05, .72, .01, 2.0, "oak")
        bx(-.05, .32, 1.0, .03, .03, .2, "chrome"); bx(.05, .32, 1.0, .03, .03, .2, "chrome")


def nightstand(x, y, rot=0):
    with at(x, y, 0, rot):
        bx(0, 0, 0, .45, .4, .5, "wood")
        bx(0, .201, .25, .3, .005, .02, "chrome")
        cy(0, 0, .5, .12, .12, .02, "black"); bx(0, 0, .52, .02, .02, .2, "metal_dark"); cy(0, 0, .7, .2, .2, .16, "light", r2=.7)


# ---------------------------------------------------------------- rapat & studio
def meeting_table(x, y, rot=0, w=5.6, d=1.5):
    """Meja panjang + 11 kursi (5+5+1)."""
    with at(x, y, 0, rot):
        bx(0, 0, .74, w, d, .06, "wood_dark")
        bx(0, 0, .72, w - .1, d - .1, .03, "wood")
        for dx in (-w / 2 + .5, w / 2 - .5):
            bx(dx, 0, 0, .1, d - .5, .74, "metal_dark")
            bx(dx, 0, 0, .1, d - .2, .06, "metal_dark")
        for i in range(5):
            px = -w / 2 + .6 + i * (w - 1.2) / 4
            plain_chair_row(px, d / 2 + .5, 180)
            plain_chair_row(px, -d / 2 - .5, 0)
        plain_chair_row(w / 2 + .6, 0, 90)
        for i in range(3):
            cy(-1.2 + i * 1.2, 0, .8, .25, .25, .3, "chrome", r2=.85, seg=10)    # air minum
            bx(-1.2 + i * 1.2 + .3, .3, .8, .3, .22, .01, "paper")
        bx(1.8, -.3, .8, .32, .22, .015, "metal_dark"); bx(1.8, -.15, .82, .32, .01, .2, "scr_blue", rx=-100)   # laptop
        bx(-.2, 0, .8, .4, .12, .04, "black")


def plain_chair_row(x, y, rot):
    chair(x, y, rot, ["fab_navy", "fab_grey"][int(abs(x * 2)) % 2])


def projector_screen(x, y, z, rot=0, w=2.4, h=1.4):
    with at(x, y, z, rot):
        bx(0, 0, h, w + .2, .1, .08, "metal_dark")
        bx(0, .0, 0, w, .03, h, "board")
        bx(0, .02, .15, w - .3, .01, h - .3, "scr_blue")
        bx(-.3, .03, .5, .8, .01, .08, "white"); bx(-.3, .03, .75, .6, .01, .05, "white")
        bx(.3, .03, .4, .6, .01, .5, "scr_teal")


def ceiling_projector(x, y, z):
    with at(x, y, z):
        bx(0, 0, 0, .4, .35, .12, "white"); cy(0, .2, .03, .12, .12, .08, "black", rx=90)


def backdrop_stand(x, y, rot=0, w=3.6, h=2.6, col="green_screen"):
    with at(x, y, 0, rot):
        bx(-w / 2 - .1, 0, 0, .06, .06, h + .2, "metal_dark"); bx(w / 2 + .1, 0, 0, .06, .06, h + .2, "metal_dark")
        bx(0, 0, h + .14, w + .3, .05, .05, "metal_dark")
        bx(0, 0, 0, w, .04, h + .1, col)
        bx(0, -.02, 0, w + .1, .3, .02, col)   # lantai sapuan


def softbox(x, y, rot=0, h=1.9):
    with at(x, y, 0, rot):
        for a in (0, 120, 240):
            import math
            bx(.25 * math.cos(math.radians(a)), .25 * math.sin(math.radians(a)), 0, .04, .04, .35, "metal_dark", rz=a)
        cy(0, 0, 0, .06, .06, h, "metal_dark", seg=8)
        bx(0, .0, h - .35, .8, .25, .8, "black")
        bx(0, .13, h - .3, .7, .02, .7, "light")


def tripod_camera(x, y, rot=0, h=1.4):
    with at(x, y, 0, rot):
        import math
        for a in (0, 120, 240):
            bx(.18 * math.cos(math.radians(a)), .18 * math.sin(math.radians(a)), 0, .03, .03, h * .75, "metal_dark",
               rx=14 * math.cos(math.radians(a)), ry=-14 * math.sin(math.radians(a)))
        cy(0, 0, h * .75, .12, .12, .08, "metal_dark", seg=8)
        bx(0, 0, h * .82, .28, .18, .2, "black")
        cy(0, .18, h * .85, .13, .13, .18, "black", rx=-90, seg=10)
        cy(0, .27, h * .86, .11, .11, .02, "scr_blue", rx=-90, seg=10)


def director_chair(x, y, rot=0):
    with at(x, y, 0, rot):
        for dx in (-.25, .25):
            bx(dx, .0, 0, .04, .5, .04, "wood_dark", rz=0); bx(dx, -.25, 0, .04, .04, .9, "wood_dark")
            bx(dx, .25, 0, .04, .04, .45, "wood_dark")
        bx(0, 0, .45, .5, .5, .03, "fab_red"); bx(0, -.25, .6, .5, .03, .25, "fab_red")


def reception_counter(x, y, rot=0, w=3.4):
    with at(x, y, 0, rot):
        bx(0, 0, 0, w, .8, 1.05, "wood")
        bx(0, .0, 1.05, w + .1, .9, .05, "counter")
        bx(0, -.401, .1, w - .2, .005, .8, "wood_dark")
        bx(0, -.41, .55, 1.1, .01, .3, "note_b")                     # logo
        bx(0, -.415, .6, .8, .012, .08, "white")
        monitor(.7, -.1, 1.1, "scr_teal"); bx(.7, .15, 1.1, .42, .14, .02, "white")
        bx(-.9, -.1, 1.1, .2, .2, .1, "black"); bx(-.9, -.1, 1.1 + .1, .02, .02, .22, "metal"); bx(-.9, 0, 1.3, .14, .14, .03, "red")  # lonceng/telepon
        cy(-1.3, .1, 1.1, .1, .1, .12, "fab_orange")
        book_stack(-.4, .2, 1.1)


def brochure_rack(x, y, rot=0):
    with at(x, y, 0, rot):
        bx(0, 0, 0, .6, .28, .1, "metal_dark")
        bx(0, 0, .1, .04, .04, 1.2, "metal_dark")
        for k in range(4):
            bx(0, .06, .4 + k * .25, .5, .1, .2, ["note_y", "note_b", "note_p", "note_g"][k])
            bx(0, .0, .35 + k * .25, .54, .16, .02, "metal_dark")


def shoe_rack(x, y, rot=0):
    with at(x, y, 0, rot):
        bx(0, 0, 0, 1.2, .35, .8, "wood")
        for k in range(3):
            bx(0, .0, .05 + k * .25, 1.1, .36, .02, "wood_dark")
            for i in range(3):
                bx(-.4 + i * .4, 0, .07 + k * .25, .16, .26, .1, ["red", "blue", "yellow"][(i + k) % 3])


def water_dispenser(x, y, rot=0):
    with at(x, y, 0, rot):
        bx(0, 0, 0, .35, .35, 1.0, "white")
        cy(0, 0, 1.0, .3, .3, .4, "glass")
        bx(-.07, .18, .75, .05, .03, .04, "blue"); bx(.07, .18, .75, .05, .03, .04, "red")


def shelf_wall(x, y, z, rot=0, w=1.2):
    with at(x, y, z, rot):
        bx(0, .0, 0, w, .22, .04, "wood_dark")
        bx(-w * .35, -.05, -.1, .04, .04, .1, "metal"); bx(w * .35, -.05, -.1, .04, .04, .1, "metal")


# ---------------------------------------------------------------- pelengkap kantor
def filing_cabinet(x, y, rot=0, col="metal"):
    with at(x, y, 0, rot):
        bx(0, 0, 0, .5, .6, 1.3, col)
        for k in range(3):
            bx(0, .301, .08 + k * .4, .44, .005, .34, "grey")
            bx(0, .31, .22 + k * .4, .16, .02, .03, "black")


def printer_station(x, y, rot=0):
    with at(x, y, 0, rot):
        bx(0, 0, 0, .9, .55, .7, "desk_wood")
        bx(0, 0, .7, .6, .42, .22, "white")
        bx(0, .0, .92, .56, .38, .04, "grey")
        bx(0, .22, .78, .3, .01, .02, "black")
        bx(.22, .22, .86, .06, .01, .04, "scr_green")
        bx(0, .0, .96, .3, .25, .01, "paper")


def bin_(x, y, col="grey"):
    with at(x, y, 0):
        cy(0, 0, 0, .3, .3, .4, col, r2=1.15, seg=10)


def coat_rack(x, y, rot=0):
    with at(x, y, 0, rot):
        cy(0, 0, 0, .35, .35, .03, "metal_dark", seg=8)
        cy(0, 0, 0, .04, .04, 1.7, "metal_dark", seg=6)
        for k, c in enumerate(["fab_navy", "fab_red", "fab_sage"]):
            bx(.12 * (k - 1), 0, 1.15 - .1 * (k % 2), .1, .08, .5, c)
        for a in (0, 90, 180, 270):
            bx(0, 0, 1.65, .24, .03, .03, "metal_dark", rz=a)


def poster(x, y, z, rot=0, col="blue", w=.5, h=.7):
    with at(x, y, z, rot):
        bx(0, 0, 0, w, .02, h, "white")
        bx(0, .012, .05, w - .1, .01, h * .5, col)
        bx(0, .012, h * .65, w - .2, .01, .05, "grey")
        bx(0, .012, h * .75, w - .3, .01, .05, "grey")


def tv_wall(x, y, z, rot=0, w=1.4):
    with at(x, y, z, rot):
        bx(0, 0, 0, w, .06, w * .56, "black")
        bx(0, .032, .04, w - .08, .01, w * .56 - .08, "scr_blue")
        bx(-.2, .04, .25, .5, .01, .25, "scr_violet")
