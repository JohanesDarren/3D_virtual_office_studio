"""Varian baru: barang meja/elektronik, lampu & pendingin, studio/rapat, struktur (pintu, jendela, tangga, panel)."""
import math
from lib import bx, cy, sp, at
from registry import item
import furn_used as U

K = "kain"; W = "kayu"; C = "cat"; L = "logam"; S = "layar"; P = "karpet"; D = "daun"; PT = "pot"; DW = "dinding"; LT = "lantai"


# ------------------------------------------------------------------ BARANG MEJA / ELEKTRONIK
@item("meja_kecil", "laptop", "Laptop", {"metal": L, "scr_blue": S}, "table")
def _():
    bx(0, 0, 0, .34, .24, .015, "metal"); bx(0, .02, .015, .3, .1, .005, "grey")
    bx(0, -.12, .015, .34, .012, .22, "metal", rx=-12)
    bx(0, -.114, .03, .3, .006, .18, "scr_blue", rx=-12)


@item("meja_kecil", "monitor_lebar", "Monitor ultrawide", {"scr_teal": S}, "table")
def _():
    U.monitor(0, 0, 0, "scr_teal", w=.9, h=.36)


@item("meja_kecil", "keyboard_mekanik", "Keyboard mekanik", {"black": L, "neon_blue": S}, "table")
def _():
    bx(0, 0, 0, .44, .15, .025, "black")
    for r in range(3):
        for i in range(10):
            bx(-.19 + i * .042, -.04 + r * .04, .025, .032, .03, .012, "neon_blue" if (i + r) % 4 == 0 else "grey")


@item("meja_kecil", "mouse_gaming", "Mouse gaming", {"black": L, "neon_pink": S}, "table")
def _():
    sp(0, 0, .022, .07, .11, .044, "black", seg=8); bx(0, -.01, .04, .005, .04, .006, "neon_pink")
    bx(-.0, .0, .0, .26, .22, .004, "metal_dark")


@item("meja_kecil", "headset_stand", "Headset + stand", {"black": L, "neon_blue": S}, "table")
def _():
    cy(0, 0, 0, .16, .16, .02, "metal_dark", seg=10); bx(0, 0, .02, .02, .02, .26, "metal_dark")
    sp(0, 0, .31, .2, .06, .22, "black", seg=10); sp(-.1, 0, .22, .06, .09, .1, "black", seg=6); sp(.1, 0, .22, .06, .09, .1, "black", seg=6)
    bx(0, 0, .43, .005, .005, .005, "neon_blue")


@item("meja_kecil", "speaker_meja", "Speaker meja (sepasang)", {"black": L}, "table")
def _():
    for dx in (-.35, .35):
        bx(dx, 0, 0, .15, .15, .25, "black"); cy(dx, .076, .05, .1, .01, .1, "metal_dark", rx=90, seg=10); cy(dx, .078, .17, .05, .01, .05, "grey", rx=90, seg=8)


@item("meja_kecil", "router", "Router wifi", {"white": C}, "table")
def _():
    bx(0, 0, 0, .22, .14, .035, "white")
    for dx in (-.08, 0, .08):
        bx(dx, -.05, .035, .012, .012, .2, "black")
    for i in range(4):
        bx(-.07 + i * .035, .072, .012, .015, .002, .01, "scr_green")


@item("meja_kecil", "printer_kecil", "Printer kecil", {"white": C}, "table")
def _():
    bx(0, 0, 0, .42, .3, .16, "white"); bx(0, -.05, .16, .34, .15, .02, "grey"); bx(0, .1, .02, .3, .12, .02, "metal_dark")
    bx(.15, .152, .1, .05, .004, .03, "scr_green"); bx(0, .22, .0, .3, .16, .008, "paper", rx=0)


@item("meja_kecil", "telepon_meja", "Telepon meja", {"black": L}, "table")
def _():
    bx(0, 0, 0, .2, .22, .06, "black"); bx(0, 0, .06, .05, .18, .03, "black"); bx(-.09, 0, .06, .05, .2, .04, "black")
    for i in range(3):
        for j in range(4):
            bx(.0 + i * .04, .02 - j * .035 + .05, .06, .03, .025, .01, "grey")


@item("meja_kecil", "jam_meja", "Jam meja", {"white": C}, "table")
def _():
    bx(0, 0, 0, .14, .06, .14, "white"); bx(0, .032, .02, .1, .005, .1, "scr_dark"); bx(0, .036, .08, .01, .003, .04, "white"); bx(.02, .036, .07, .04, .003, .01, "white")


@item("meja_kecil", "kotak_tisu", "Kotak tisu", {"cream": C}, "table")
def _():
    bx(0, 0, 0, .24, .12, .09, "cream"); bx(0, 0, .09, .14, .04, .06, "white", rz=10)


@item("meja_kecil", "tempat_pena", "Tempat pena", {"fab_teal": C}, "table")
def _():
    cy(0, 0, 0, .09, .09, .11, "fab_teal", seg=10)
    for i, (dx, c) in enumerate(((-.02, "red"), (.02, "blue"), (0, "yellow"), (.01, "green"))):
        bx(dx, (i % 2 - .5) * .02, .09, .012, .012, .12, c, rx=(i - 1.5) * 8)


@item("meja_kecil", "tablet_stand", "Tablet + stand", {"black": L, "scr_violet": S}, "table")
def _():
    bx(0, 0, 0, .18, .12, .015, "metal"); bx(0, -.02, .015, .02, .02, .1, "metal"); bx(0, -.04, .08, .26, .015, .18, "black", rx=-18)
    bx(0, -.032, .09, .24, .004, .16, "scr_violet", rx=-18)


@item("meja_kecil", "mug_kopi", "Mug kopi", {"fab_orange": C}, "table")
def _():
    cy(0, 0, 0, .09, .09, .1, "fab_orange", seg=10); bx(.06, 0, .03, .02, .02, .05, "fab_orange"); cy(0, 0, .09, .07, .07, .006, "soil", seg=8)


@item("meja_kecil", "botol_minum", "Botol minum", {"cyan": C}, "table")
def _():
    cy(0, 0, 0, .08, .08, .26, "cyan", seg=10); cy(0, 0, .26, .05, .05, .04, "black", seg=8); bx(.05, 0, .22, .03, .01, .04, "black")


@item("meja_kecil", "tray_dokumen", "Tray dokumen", {"metal_dark": L}, "table")
def _():
    for k in range(3):
        bx(0, 0, k * .09, .34, .26, .02, "metal_dark"); bx(0, .0, k * .09 + .02, .3, .22, .015, "paper", rz=k * 3)
        bx(-.16, 0, k * .09, .02, .26, .08, "metal_dark"); bx(.16, 0, k * .09, .02, .26, .08, "metal_dark")


@item("meja_kecil", "pc_tower", "PC tower (RGB)", {"black": L, "neon_blue": S}, "floor")
def _():
    bx(0, 0, 0, .24, .5, .5, "black"); bx(0, .251, .06, .16, .005, .38, "glass"); bx(0, .256, .18, .14, .004, .02, "neon_blue"); bx(0, .256, .3, .14, .004, .02, "neon_pink")
    bx(-.05, .25, .44, .04, .004, .02, "scr_green")


@item("meja_kecil", "shredder", "Mesin penghancur kertas", {"black": L}, "floor")
def _():
    bx(0, 0, 0, .42, .28, .5, "black"); bx(0, 0, .5, .46, .32, .05, "metal_dark"); bx(0, 0, .55, .3, .02, .01, "grey")
    bx(.15, .141, .3, .04, .004, .03, "scr_green")


@item("meja_kecil", "tv_rak_rendah", "TV + rak rendah (tanpa konsol)", {"wood_dark": W, "scr_blue": S}, "floor")
def _():
    w = 1.8
    bx(0, 0, 0, w + .2, .4, .4, "wood_dark")
    for s in (-1, 1):
        bx(s * (w / 4), .201, .05, w / 2 - .1, .005, .3, "wood"); bx(s * .1, .21, .2, .03, .02, .03, "chrome")
    bx(0, 0, .4, .5, .22, .02, "metal_dark"); bx(0, 0, .42, .06, .06, .1, "metal_dark")
    bx(0, 0, .5, w - .2, .06, 1.0, "black"); bx(0, .032, .55, w - .3, .01, .9, "scr_blue"); bx(-.2, .04, .75, .6, .01, .35, "scr_violet")


# ------------------------------------------------------------------ LAMPU & PENDINGIN
@item("lampu", "lampu_meja", "Lampu meja", {"metal_dark": L, "light": S}, "table")
def _():
    cy(0, 0, 0, .14, .14, .02, "metal_dark"); bx(0, 0, .02, .02, .02, .3, "metal_dark"); bx(0, .07, .32, .02, .18, .02, "metal_dark", rx=-20)
    bx(0, .15, .3, .1, .08, .06, "metal_dark"); bx(0, .15, .295, .08, .06, .01, "light")


@item("lampu", "lampu_meja_bulat", "Lampu meja (kap bulat)", {"wood_dark": W, "light": S}, "table")
def _():
    cy(0, 0, 0, .12, .12, .02, "wood_dark", seg=10); cy(0, 0, .02, .04, .04, .2, "wood_dark", seg=8)
    sp(0, 0, .34, .24, .24, .22, "light", seg=10)


@item("lampu", "lampu_lantai", "Lampu lantai", {"metal_dark": L, "fab_cream": K})
def _():
    cy(0, 0, 0, .3, .3, .03, "metal_dark", seg=12); cy(0, 0, .03, .03, .03, 1.45, "metal_dark", seg=6)
    cy(0, 0, 1.4, .36, .36, .3, "fab_cream", r2=.7, seg=12); cy(0, 0, 1.42, .3, .3, .02, "light", seg=12)


@item("lampu", "lampu_lantai_arc", "Lampu lantai lengkung", {"black": L})
def _():
    cy(0, 0, 0, .36, .36, .06, "stone", seg=12); cy(0, 0, .06, .04, .04, 1.8, "black", seg=6)
    bx(0, .3, 1.84, .03, .7, .03, "black", rx=-4); cy(0, .72, 1.52, .3, .3, .22, "black", r2=.6, seg=10); cy(0, .72, 1.5, .24, .24, .02, "light", seg=10)


@item("lampu", "lampu_gantung_bulat", "Lampu gantung bulat", {"light": S, "black": L}, "ceiling", 2.3)
def _():
    cy(0, 0, .5, .02, .02, .5, "black", seg=6); sp(0, 0, .35, .4, .4, .35, "light", seg=12); cy(0, 0, .5, .08, .08, .04, "black", seg=8)


@item("lampu", "lampu_gantung_kerucut", "Lampu gantung kerucut", {"metal": L, "light": S}, "ceiling", 2.3)
def _():
    cy(0, 0, .5, .02, .02, .6, "black", seg=6); cy(0, 0, .15, .5, .5, .35, "metal", r2=.15, seg=14); cy(0, 0, .15, .3, .3, .03, "light", seg=12)


@item("lampu", "lampu_panel", "Lampu panel langit-langit", {"led_cool": S}, "ceiling", 3.25)
def _():
    bx(0, 0, 0, .6, .6, .05, "white"); bx(0, 0, -.005, .54, .54, .01, "led_cool")


@item("lampu", "lampu_sorot_rel", "Lampu sorot rel", {"black": L}, "ceiling", 3.1)
def _():
    bx(0, 0, .15, 1.6, .05, .04, "black")
    for dx in (-.55, 0, .55):
        bx(dx, 0, .12, .02, .02, .05, "black"); cy(dx, .08, 0, .1, .1, .16, "black", r2=.8, rx=30, seg=8); cy(dx, .12, .02, .08, .02, .02, "light", rx=30, seg=8)


@item("lampu", "kipas_berdiri", "Kipas berdiri", {"white": C})
def _():
    cy(0, 0, 0, .4, .4, .04, "white", seg=12); cy(0, 0, .04, .05, .05, 1.0, "metal", seg=6)
    cy(0, .04, 1.0, .5, .1, .5, "grey", rx=90, seg=18); cy(0, .09, 1.0, .46, .02, .46, "white", rx=90, seg=18)
    sp(0, .09, 1.25, .1, .06, .1, "white", seg=6)


@item("lampu", "kipas_meja", "Kipas meja", {"white": C}, "table")
def _():
    cy(0, 0, 0, .16, .16, .03, "white", seg=10); bx(0, 0, .03, .03, .03, .12, "white")
    cy(0, .03, .1, .26, .06, .26, "grey", rx=90, seg=14); cy(0, .06, .1, .22, .02, .22, "white", rx=90, seg=14)


@item("lampu", "kipas_langit", "Kipas langit-langit", {"wood": W}, "ceiling", 3.0)
def _():
    cy(0, 0, .15, .03, .03, .15, "metal_dark", seg=6); cy(0, 0, .05, .2, .2, .1, "metal_dark", seg=10)
    for a in range(0, 360, 90):
        bx(.4 * math.cos(math.radians(a)), .4 * math.sin(math.radians(a)), .08, .6, .14, .015, "wood", rz=a + 0)


@item("lampu", "ac_standing", "AC berdiri", {"white": C})
def _():
    bx(0, 0, 0, .5, .35, 1.7, "white"); bx(0, .176, 1.0, .4, .005, .4, "grey")
    for k in range(6):
        bx(0, .18, 1.05 + k * .06, .38, .005, .015, "metal_dark")
    bx(.12, .178, .5, .08, .004, .06, "scr_green"); bx(0, .178, .15, .4, .004, .25, "metal")


@item("lampu", "ac_kaset", "AC kaset langit-langit", {"white": C}, "ceiling", 3.2)
def _():
    bx(0, 0, 0, 1.0, 1.0, .1, "white"); bx(0, 0, -.01, .6, .6, .02, "grey")
    for a in (0, 90, 180, 270):
        bx(.42 * math.cos(math.radians(a)), .42 * math.sin(math.radians(a)), .0, .5, .04, .015, "metal_dark", rz=a + 90)


# ------------------------------------------------------------------ STUDIO & RAPAT
@item("studio", "ring_light", "Ring light + tripod", {"black": L, "led_cool": S})
def _():
    for a in (0, 120, 240):
        r = math.radians(a)
        bx(.18 * math.cos(r), .18 * math.sin(r), 0, .03, .03, 1.1, "black", rx=12 * math.cos(r), ry=-12 * math.sin(r))
    cy(0, 0, 1.0, .05, .05, .6, "metal_dark", seg=6)
    cy(0, 0, 1.65, .55, .06, .55, "led_cool", rx=90, seg=24)


@item("studio", "boom_mic", "Mic boom + pop filter", {"black": L})
def _():
    cy(0, 0, 0, .4, .4, .04, "metal_dark", seg=12); cy(0, 0, .04, .04, .04, 1.4, "metal_dark", seg=6)
    bx(0, .3, 1.46, .03, .7, .03, "metal_dark", rx=-5); cy(0, .64, 1.34, .1, .1, .16, "black", seg=8)
    cy(0, .72, 1.22, .24, .02, .24, "grey", rx=90, seg=14)


@item("studio", "light_panel", "Panel LED + tripod", {"black": L, "led_cool": S})
def _():
    for a in (0, 120, 240):
        r = math.radians(a)
        bx(.2 * math.cos(r), .2 * math.sin(r), 0, .03, .03, 1.5, "black", rx=10 * math.cos(r), ry=-10 * math.sin(r))
    bx(0, 0, 1.4, .05, .05, .3, "metal_dark"); bx(0, .0, 1.55, .7, .06, .45, "black"); bx(0, .035, 1.6, .62, .01, .36, "led_cool")


@item("studio", "reflektor", "Reflektor bulat + stand", {"white": C})
def _():
    cy(0, 0, 0, .4, .4, .04, "metal_dark", seg=10); cy(0, 0, .04, .04, .04, 1.2, "metal_dark", seg=6)
    cy(0, .03, 1.15, .9, .04, .9, "white", rx=90, seg=24); cy(0, .0, 1.15, .94, .03, .94, "metal_dark", rx=90, seg=24)


@item("studio", "clapperboard", "Clapperboard", {"black": L}, "table")
def _():
    bx(0, 0, 0, .3, .015, .22, "black")
    for i in range(6):
        bx(-.12 + i * .048, .01, .22, .04, .005, .03, "white" if i % 2 else "black")
    bx(0, .0, .25, .3, .016, .04, "black", rx=-18)
    bx(0, .01, .05, .22, .004, .02, "white"); bx(0, .01, .12, .22, .004, .02, "white")


@item("studio", "podium", "Podium / lectern", {"wood": W})
def _():
    bx(0, 0, 0, .6, .45, 1.0, "wood"); bx(0, -.02, 1.0, .66, .5, .05, "wood_dark")
    bx(0, .05, 1.05, .5, .3, .03, "wood", rx=-15); bx(0, .24, .1, .3, .005, .35, "gold")
    cy(.15, -.1, 1.07, .02, .02, .2, "metal", seg=6)


@item("studio", "flipchart", "Flipchart + easel", {"white": C})
def _():
    for a in (0, 120, 240):
        r = math.radians(a)
        bx(.25 * math.cos(r), .25 * math.sin(r) - .1, 0, .04, .04, 1.9, "wood_dark")
    bx(0, 0, .8, .8, .03, 1.0, "white"); bx(0, .02, .9, .7, .005, .06, "blue"); bx(0, .02, 1.2, .5, .005, .02, "red"); bx(0, .02, 1.5, .6, .005, .02, "green")
    bx(0, .03, .75, .8, .05, .04, "metal_dark")


@item("studio", "meja_podcast", "Meja podcast + 2 mic", {"wood_dark": W, "black": L})
def _():
    bx(0, 0, .72, 1.8, .8, .05, "wood_dark")
    for dx in (-.8, .8):
        bx(dx, 0, 0, .06, .7, .72, "metal_dark")
    for dx in (-.5, .5):
        bx(dx, -.2, .77, .02, .02, .35, "black"); bx(dx, -.05, 1.1, .02, .3, .02, "black", rx=-5); cy(dx, .1, 1.05, .07, .07, .1, "black", seg=8)
    bx(0, .1, .77, .5, .3, .05, "black"); bx(0, -.3, .77, .6, .015, .3, "scr_dark", rx=-10)


@item("studio", "panel_akustik", "Panel akustik", {"fab_navy": K}, "wall", 1.3)
def _():
    for i in range(3):
        bx(-.6 + i * .6, 0, 0, .56, .06, 1.1, "fab_navy")
        for k in range(3):
            bx(-.6 + i * .6, .035, .15 + k * .3, .5, .01, .05, "fab_charcoal")


@item("studio", "backdrop_putih", "Backdrop putih", {"white": C})
def _():
    U.backdrop_stand(0, 0, w=3.0, h=2.4, col="white")


@item("studio", "backdrop_biru", "Backdrop biru", {"backdrop": C})
def _():
    U.backdrop_stand(0, 0, col="backdrop")


@item("studio", "banner_rollup", "Roll-up banner", {"fab_teal": C})
def _():
    bx(0, 0, 0, .9, .2, .06, "metal_dark"); bx(0, 0, .06, .8, .02, 1.9, "fab_teal"); bx(0, .012, .9, .5, .006, .4, "white"); bx(0, .014, 1.5, .5, .006, .1, "yellow")
    bx(0, .014, .3, .6, .006, .3, "fab_cream")


# ------------------------------------------------------------------ STRUKTUR (pintu & jendela: punggung y=0, menghadap +Y)
def _door_frame(w, h, m="trim"):
    bx(-w / 2 - .04, 0, 0, .08, .16, h + .08, m); bx(w / 2 + .04, 0, 0, .08, .16, h + .08, m); bx(0, 0, h, w + .16, .16, .08, m)


@item("struktur", "pintu_kayu", "Pintu kayu", {"door": W, "trim": W}, "wall", 0)
def _():
    _door_frame(.9, 2.1)
    bx(0, .02, 0, .9, .05, 2.1, "door")
    for dx in (-.2, .2):
        bx(dx, .05, .15, .3, .01, .8, "wood_dark"); bx(dx, .05, 1.2, .3, .01, .7, "wood_dark")
    sp(.36, .09, 1.0, .07, .06, .07, "brass", seg=6)


@item("struktur", "pintu_kaca", "Pintu kaca + rangka logam", {"metal_dark": L}, "wall", 0)
def _():
    _door_frame(1.0, 2.1, "metal_dark")
    bx(0, .02, 0, 1.0, .05, 2.1, "metal_dark"); bx(0, .03, .08, .84, .04, 1.9, "glass")
    bx(.38, .06, .95, .03, .03, .5, "chrome"); bx(0, .05, 1.0, .84, .01, .03, "metal_dark")


@item("struktur", "pintu_ganda", "Pintu ganda", {"door": W, "trim": W}, "wall", 0)
def _():
    _door_frame(1.8, 2.2)
    for s in (-1, 1):
        bx(s * .45, .02, 0, .9, .05, 2.2, "door")
        for dz in (.2, 1.2):
            bx(s * .45, .05, dz, .6, .01, .8, "wood_dark")
        bx(s * .08, .08, 1.0, .03, .03, .2, "brass")


@item("struktur", "pintu_geser_kaca", "Pintu geser kaca", {"metal": L}, "wall", 0)
def _():
    bx(0, 0, 2.1, 2.2, .14, .12, "metal"); bx(0, 0, 0, 2.2, .14, .04, "metal_dark")
    for s in (-1, 1):
        bx(s * .5, .02 + (s > 0) * .03, .04, 1.0, .03, 2.06, "metal"); bx(s * .5, .035 + (s > 0) * .03, .1, .88, .01, 1.9, "glass")
    bx(0, .1, 2.0, .3, .02, .1, "scr_green")


@item("struktur", "jendela_kotak", "Jendela kotak", {"trim": W}, "wall", .9)
def _():
    w, h = 1.2, 1.2
    bx(0, 0, 0, w + .16, .16, .08, "trim"); bx(0, 0, h + .08, w + .16, .16, .08, "trim")
    bx(-w / 2 - .04, 0, .08, .08, .16, h, "trim"); bx(w / 2 + .04, 0, .08, .08, .16, h, "trim")
    bx(0, 0, .08, w, .03, h, "glass"); bx(0, .05, .08, .03, .04, h, "trim"); bx(0, .05, .08 + h / 2, w, .04, .03, "trim")
    bx(0, .12, -.03, w + .3, .22, .04, "trim")


@item("struktur", "jendela_lebar", "Jendela lebar", {"trim": W}, "wall", 1.0)
def _():
    w, h = 2.6, .9
    bx(0, 0, 0, w + .16, .16, .08, "trim"); bx(0, 0, h + .08, w + .16, .16, .08, "trim")
    for s in (-1, 1):
        bx(s * (w / 2 + .04), 0, .08, .08, .16, h, "trim")
    bx(0, 0, .08, w, .03, h, "glass")
    for dx in (-.43, .43):
        bx(dx, .05, .08, .04, .04, h, "trim")
    bx(0, .12, -.03, w + .3, .22, .04, "trim")


@item("struktur", "jendela_kisi", "Jendela berkisi", {"trim": W}, "wall", .9)
def _():
    w, h = 1.0, 1.4
    bx(0, 0, 0, w + .16, .16, .08, "trim"); bx(0, 0, h + .08, w + .16, .16, .08, "trim")
    for s in (-1, 1):
        bx(s * (w / 2 + .04), 0, .08, .08, .16, h, "trim")
    bx(0, 0, .08, w, .03, h, "glass")
    for i in range(1, 3):
        bx(-w / 2 + i * w / 3, .05, .08, .03, .03, h, "white")
    for i in range(1, 4):
        bx(0, .05, .08 + i * h / 4, w, .03, .03, "white")
    bx(0, .12, -.03, w + .3, .2, .04, "trim")


@item("struktur", "jendela_bulat", "Jendela bulat", {"brass": L}, "wall", 1.2)
def _():
    cy(0, 0, 0, 1.0, .12, 1.0, "brass", rx=90, seg=24); cy(0, .02, .04, .88, .06, .88, "glass", rx=90, seg=24)
    bx(0, .05, .06, .03, .03, .88, "brass"); bx(0, .05, .5 - .015, .88, .03, .03, "brass")


@item("struktur", "tangga_lurus", "Tangga lurus (8 anak tangga)", {"wood": W, "metal_dark": L})
def _():
    n = 8; rise = .22; run = .3
    for i in range(n):
        bx(0, i * run, i * rise, 1.2, run, rise, "wood")
        bx(0, i * run + run / 2, i * rise + rise - .01, 1.2, run - .02, .02, "oak")
    for s in (-1, 1):
        for i in range(0, n, 2):
            bx(s * .6, i * run + .1, i * rise + rise, .03, .03, .85, "metal_dark")
        bx(s * .6, n * run / 2, n * rise / 2 + rise + .83, .04, n * run, .04, "wood_dark", rx=math.degrees(math.atan2(rise, run)))


@item("struktur", "pilar", "Pilar", {"wall_cream": DW}, "floor")
def _():
    cy(0, 0, 0, .5, .5, .1, "trim", seg=12); cy(0, 0, .1, .4, .4, 3.1, "wall_cream", seg=12); cy(0, 0, 3.2, .5, .5, .1, "trim", seg=12)


@item("struktur", "panel_dinding", "Panel dinding (wainscot + cat)", {"wall_cream": DW, "wainscot": W})
def _():
    bx(0, 0, 0, 2.0, .15, 1.05, "wainscot"); bx(0, 0, 1.05, 2.0, .15, 2.25, "wall_cream"); bx(0, .09, 1.02, 2.0, .04, .05, "trim"); bx(0, .09, 0, 2.0, .04, .08, "skirt")


@item("struktur", "partisi_kaca", "Partisi kaca", {"metal_dark": L})
def _():
    bx(0, 0, 0, 2.0, .06, .9, "wainscot"); bx(0, 0, .9, 2.0, .05, 1.5, "glass")
    for dx in (-1.0, 0, 1.0):
        bx(dx, 0, 0, .05, .08, 2.4, "metal_dark")
    bx(0, 0, 2.4, 2.05, .08, .05, "metal_dark")


@item("struktur", "ubin_kayu", "Lantai papan kayu 2x2", {"fl_a": LT, "fl_b": LT, "fl_c": LT})
def _():
    for i in range(8):
        for j in range(2):
            bx(-.75 + i * .25 + (j % 2) * 0, -.5 + j * 1.0 + (i % 2) * .0, 0, .24, .98, .04, ["fl_a", "fl_b", "fl_c"][(i + j) % 3])


@item("struktur", "ubin_keramik", "Lantai keramik 2x2", {"tile_w": LT, "tile_g": LT})
def _():
    for i in range(4):
        for j in range(4):
            bx(-.75 + i * .5, -.75 + j * .5, 0, .48, .48, .04, "tile_w" if (i + j) % 2 else "tile_g")


@item("struktur", "tiang_antrean", "Tiang pembatas antrean", {"chrome": L})
def _():
    for dx in (-.6, .6):
        cy(dx, 0, 0, .3, .3, .03, "chrome", seg=12); cy(dx, 0, .03, .04, .04, .95, "chrome", seg=8); sp(dx, 0, 1.0, .08, .08, .08, "chrome", seg=6)
    bx(0, 0, .8, 1.2, .02, .04, "red")
