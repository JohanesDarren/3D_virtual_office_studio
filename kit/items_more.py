"""More furniture (v4): seating, monitor variants, desk tech, desks, storage, decor.

Same conventions as items.py (pivot bottom center, front -Y, wall items back on y=0).
Every chair puts its seat top at ~0.47 m so the avatars' "sit" clip lands on it.
"""
import math

from items import BOOKS, _polar, _star_base, item

SEAT = .47


# =========================================================================== SEATING
@item("gaming_chair", "Gaming chair", "seating")
def gaming_chair(it):
    _star_base(it, m="black", wheel="charcoal")
    it.cyl((0, 0, .25), (.05, .05), .3, "metal", seg=10)
    it.box((0, 0, .41), (.3, .3, .03), "black", bevel=.01)
    it.box((0, -.01, SEAT), (.52, .5, .1), "charcoal", bevel=.04)
    for sx in (-1, 1):                                                       # raised seat bolsters
        it.box((sx * .22, -.01, SEAT + .04), (.08, .48, .06), "coral", bevel=.015)
        it.box((sx * .29, .02, .6), (.05, .05, .18), "black", bevel=.012)
        it.box((sx * .29, -.01, .69), (.08, .3, .04), "black", bevel=.015)
    it.box((0, .27, .92), (.5, .1, .82), "charcoal", bevel=.045, rot=(-8, 0, 0))   # tall back
    for sx in (-1, 1):
        it.box((sx * .2, .25, .98), (.08, .1, .6), "coral", bevel=.015, rot=(-8, 0, sx * 6))
        it.box((sx * .085, .2, 1.27), (.06, .02, .08), "black", bevel=0, outline=False)   # belt slots
    it.box((0, .2, 1.18), (.26, .08, .12), "white", bevel=.04, rot=(-8, 0, 0))    # head pillow
    it.box((0, .21, .68), (.28, .09, .1), "coral", bevel=.04, rot=(-8, 0, 0))     # lumbar pillow


@item("mesh_chair", "Ergonomic mesh chair", "seating")
def mesh_chair(it):
    _star_base(it, m="grey", wheel="charcoal")
    it.cyl((0, 0, .25), (.05, .05), .3, "metal", seg=10)
    it.box((0, 0, .41), (.3, .3, .03), "charcoal", bevel=.01)
    it.box((0, -.01, SEAT), (.5, .48, .08), "charcoal", bevel=.035)
    it.box((0, .3, .62), (.06, .04, .34), "grey", bevel=.012, rot=(-12, 0, 0))     # spine
    it.box((0, .3, .9), (.46, .04, .5), "grey", bevel=.02, rot=(-8, 0, 0))         # frame
    it.box((0, .284, .9), (.4, .01, .44), "black", bevel=0, rot=(-8, 0, 0), outline=False)   # mesh
    for k in range(5):
        z = .72 + k * .09
        it.box((0, .278, z), (.4, .004, .008), "charcoal", bevel=0,
               rot=(-8, 0, 0), outline=False)
    it.box((0, .3, 1.24), (.3, .06, .1), "charcoal", bevel=.03, rot=(-8, 0, 0))     # headrest
    it.box((0, .26, .7), (.3, .05, .08), "sky", bevel=.02)                          # lumbar
    for sx in (-1, 1):
        it.box((sx * .28, .05, .58), (.035, .035, .16), "grey", bevel=.01)
        it.box((sx * .28, .0, .67), (.07, .24, .03), "charcoal", bevel=.012)


@item("wooden_chair", "Wooden chair", "seating")
def wooden_chair(it):
    for sx in (-1, 1):
        for sy in (-1, 1):
            it.stick((sx * .19, sy * .18, .012), (sx * .17, sy * .16, SEAT - .04), .04, "wood_mid", seg=8)
        it.stick((sx * .17, .18, SEAT), (sx * .18, .23, .88), .035, "wood_mid", seg=8)   # back posts
    it.box((0, 0, SEAT - .02), (.44, .42, .04), "wood_light", bevel=.015)
    it.box((0, -.01, SEAT + .015), (.38, .36, .03), "butter", bevel=.015)           # seat pad
    for z in (.66, .76, .86):
        it.box((0, .2 + (z - .66) * .2, z), (.36, .025, .05), "wood_light", bevel=.01)
    it.box((0, 0, .18), (.36, .03, .03), "wood_mid", bevel=.008)                     # stretcher


@item("shell_chair", "Shell chair", "seating")
def shell_chair(it):
    for sx in (-1, 1):
        for sy in (-1, 1):
            it.stick((sx * .2, sy * .19, .012), (sx * .07, sy * .06, SEAT - .06), .03, "wood_light", seg=8)
    it.stick((-.15, -.14, .2), (.15, .14, .2), .012, "metal", seg=5)                 # cross wires
    it.stick((.15, -.14, .2), (-.15, .14, .2), .012, "metal", seg=5)
    it.box((0, 0, SEAT - .05), (.14, .14, .03), "black", bevel=.008)
    it.cyl((0, 0, SEAT - .01), (.48, .46), .08, "mint", seg=24, top=1.1, bevel=.025)   # seat shell
    it.box((0, .2, .68), (.46, .07, .34), "mint", bevel=.04, rot=(-14, 0, 0))         # back shell


@item("cantilever_chair", "Visitor chair", "seating")
def cantilever_chair(it):
    for sx in (-1, 1):   # one continuous chrome tube per side: floor runner, front loop, seat rail, back post
        it.stick((sx * .2, .2, .015), (sx * .2, -.22, .015), .03, "metal")
        it.stick((sx * .2, -.22, .015), (sx * .2, -.22, SEAT - .05), .03, "metal")
        it.stick((sx * .2, -.22, SEAT - .05), (sx * .2, .18, SEAT - .05), .03, "metal")
        it.stick((sx * .2, .18, SEAT - .05), (sx * .2, .24, .86), .03, "metal")
    it.box((0, -.02, SEAT - .01), (.46, .42, .07), "blush", bevel=.03)
    it.box((0, .22, .72), (.46, .06, .28), "blush", bevel=.03, rot=(-8, 0, 0))


@item("bar_stool", "Bar stool", "seating")
def bar_stool(it):
    it.cyl((0, 0, .015), (.42, .42), .03, "charcoal", seg=20, bevel=.01)
    it.cyl((0, 0, .38), (.06, .06), .7, "metal", seg=10)
    it.cyl((0, 0, .3), (.36, .36), .025, "metal", seg=16)                             # foot ring
    it.cyl((0, 0, .76), (.42, .42), .08, "peach", seg=20, bevel=.03)
    it.box((0, .17, .9), (.36, .05, .16), "peach", bevel=.025, rot=(-10, 0, 0))
    it.stick((0, .16, .78), (0, .18, .84), .04, "metal", seg=8)


@item("bench", "Padded bench", "seating")
def bench(it):
    w = 1.2
    for sx in (-1, 1):
        it.box((sx * (w / 2 - .06), 0, .2), (.05, .36, .4), "wood_mid", bevel=.015)
    it.box((0, 0, .4), (w, .38, .04), "wood_light", bevel=.015)
    it.box((0, 0, .45), (w - .06, .36, .07), "sage", bevel=.03)
    for x in (-.3, 0, .3):
        it.ball((x, 0, .487), (.03, .03, .012), "leaf_dark", seg=8, outline=False)    # buttons
    it.box((0, 0, .1), (w - .14, .3, .025), "wood_mid", bevel=.008)                   # shoe shelf


@item("pouf", "Pouf", "seating")
def pouf(it):
    it.cyl((0, 0, .21), (.5, .5), .42, "butter", seg=24, bevel=.08)
    it.cyl((0, 0, .21), (.51, .51), .02, "wood_dark", seg=24, outline=False)          # piping belt
    it.ball((0, 0, .42), (.05, .05, .02), "wood_dark", seg=8, outline=False)


@item("saddle_stool", "Saddle stool", "seating")
def saddle_stool(it):
    _star_base(it, r=.26)
    it.cyl((0, 0, .32), (.05, .05), .44, "metal", seg=10)
    it.box((0, 0, .58), (.42, .36, .08), "lavender", bevel=.035)                       # saddle
    it.box((0, 0, .6), (.12, .34, .06), "lavender", bevel=.025)


# =========================================================================== TECH: monitor variants
def _screen(it, c, w, h, frame="charcoal", rot=(0, 0, 0), ui=True):
    it.box(c, (w, .03, h), frame, bevel=.012, rot=rot)
    sc = (c[0], c[1] - .016, c[2])
    it.box(sc, (w - .04, .01, h - .04), "screen", bevel=.003, rot=rot, outline=False)
    if ui:
        it.box((c[0] - w * .2, c[1] - .022, c[2] + h * .15), (w * .3, .004, h * .08), "white", bevel=0, rot=rot,
               outline=False)


@item("monitor_dual", "Dual monitor arm", "tech", mount="table")
def monitor_dual(it):
    it.box((0, .1, .02), (.2, .14, .04), "grey", bevel=.012)                    # desk clamp base
    it.cyl((0, .1, .24), (.04, .04), .42, "grey", seg=10)
    it.box((0, .07, .4), (.62, .04, .04), "grey", bevel=.01)                     # arm bar
    for sx in (-1, 1):
        _screen(it, (sx * .3, .03, .4), .56, .34, rot=(0, 0, sx * -10))
    it.box((-.36, .005, .41), (.16, .004, .1), "coral", bevel=0, rot=(0, 0, 10), outline=False)


@item("monitor_ultrawide", "Curved ultrawide", "tech", mount="table")
def monitor_ultrawide(it):
    it.box((0, .04, .012), (.4, .18, .025), "black", bevel=.01)
    it.box((0, .06, .15), (.06, .03, .26), "black", bevel=.012)
    segs, W, R = 5, .9, 1.2
    for i in range(segs):   # faceted curve: each panel turns toward the user
        a = (i - (segs - 1) / 2) * (W / segs) / R
        x, y = R * math.sin(a), -R * math.cos(a) + R
        _screen(it, (x, y, .3), W / segs + .012, .3, frame="black", rot=(0, 0, math.degrees(a)), ui=False)
    it.box((-.25, -.03, .36), (.2, .004, .03), "white", bevel=0, rot=(0, 0, -8), outline=False)
    it.box((.15, -.02, .26), (.3, .004, .1), "blue", bevel=0, outline=False)


@item("monitor_vertical", "Portrait monitor", "tech", mount="table")
def monitor_vertical(it):
    it.cyl((0, 0, .01), (.2, .2), .02, "white", seg=16)
    it.box((0, .03, .2), (.04, .03, .36), "white", bevel=.012)
    _screen(it, (0, 0, .42), .32, .54, frame="white")
    for k in range(4):   # code lines
        it.box((-.04 + (k % 2) * .02, -.022, .55 - k * .05), (.18 - k * .02, .004, .015), "lavender", bevel=0,
               outline=False)


@item("all_in_one", "All-in-one PC", "tech", mount="table")
def all_in_one(it):
    it.box((0, .06, .01), (.22, .18, .02), "metal", bevel=.008)
    it.box((0, .07, .12), (.18, .02, .22), "metal", bevel=.008, rot=(-10, 0, 0))
    _screen(it, (0, 0, .36), .6, .34, frame="white")
    it.box((0, -.002, .17), (.6, .03, .06), "peach", bevel=.012)                 # colored chin
    it.ball((0, -.018, .52), (.02, .01, .015), "black", seg=8, outline=False)


@item("crt_monitor", "Retro monitor", "tech", mount="table")
def crt_monitor(it):
    it.box((0, .05, .03), (.36, .3, .06), "offwhite", bevel=.02)
    it.box((0, .06, .25), (.36, .36, .36), "offwhite", bevel=.05)
    it.box((0, .2, .24), (.26, .12, .26), "offwhite", bevel=.04)                 # tube back
    it.box((0, -.125, .27), (.28, .02, .24), "charcoal", bevel=.03)
    it.box((0, -.137, .27), (.24, .01, .2), "mint", bevel=.02, outline=False)
    it.box((-.04, -.143, .3), (.1, .004, .02), "white", bevel=0, outline=False)
    it.ball((.12, -.123, .11), (.02, .01, .02), "coral", seg=6, outline=False)


@item("keyboard_mouse", "Keyboard + mouse", "desk_gear", mount="table")
def keyboard_mouse(it):
    it.box((0, 0, .012), (.44, .15, .024), "white", bevel=.008)
    for r in range(4):
        for k in range(10):
            it.box((-.18 + k * .04, -.05 + r * .033, .026), (.032, .026, .008), "grey_light", bevel=0,
                   outline=False)
    it.box((0, -.053, .026), (.18, .026, .008), "grey_light", bevel=0, outline=False)   # space
    it.box((.36, 0, .004), (.24, .2, .008), "lavender", bevel=.004)               # mouse pad
    it.ball((.36, 0, .022), (.06, .1, .045), "white", seg=10)
    it.box((.36, -.025, .042), (.004, .03, .004), "grey", bevel=0, outline=False)


@item("pc_tower", "Desktop PC", "desk_gear")
def pc_tower(it):
    it.box((0, 0, .23), (.2, .44, .42), "charcoal", bevel=.025)
    for sx in (-1, 1):
        for sy in (-1, 1):
            it.box((sx * .07, sy * .17, .01), (.04, .06, .02), "black", bevel=0)
    it.box((.102, 0, .25), (.004, .34, .32), "glass", bevel=0, outline=False)     # side window
    for i, c in enumerate(("coral", "mint", "sky")):
        it.cyl((.103, -.08 + i * .08, .3), (.07, .07), .006, c, seg=12, rot=(0, 90, 0), outline=False)   # fans
    it.cyl((0, -.222, .38), (.03, .03), .008, "mint", seg=10, rot=(90, 0, 0), outline=False)    # power


@item("printer", "Printer", "desk_gear", mount="table")
def printer(it):
    it.box((0, 0, .1), (.44, .36, .2), "white", bevel=.03)
    it.box((0, .05, .21), (.38, .22, .03), "grey_light", bevel=.01)
    it.box((0, .14, .26), (.3, .02, .12), "paper", bevel=0, rot=(-15, 0, 0))     # paper in
    it.box((0, -.2, .07), (.3, .08, .01), "grey", bevel=.004)                     # out tray
    it.box((0, -.22, .085), (.26, .06, .004), "paper", bevel=0, outline=False)
    it.box((.15, -.181, .16), (.08, .004, .04), "screen", bevel=0, outline=False)
    it.ball((.08, -.181, .16), (.02, .006, .02), "mint", seg=6, outline=False)


@item("desk_phone", "Desk phone", "desk_gear", mount="table")
def desk_phone(it):
    it.box((0, 0, .045), (.2, .18, .06), "charcoal", bevel=.02, rot=(-8, 0, 0))
    it.box((-.065, 0, .09), (.06, .17, .04), "black", bevel=.018)               # handset
    for r in range(4):
        for k in range(3):
            it.box((.02 + k * .03, -.05 + r * .03, .077), (.02, .018, .006), "grey_light", bevel=0,
                   outline=False)
    it.box((.05, .065, .077), (.09, .03, .004), "screen", bevel=0, outline=False)


@item("tablet_stand", "Tablet on stand", "desk_gear", mount="table")
def tablet_stand(it):
    it.box((0, .03, .01), (.14, .1, .02), "metal", bevel=.006)
    it.box((0, .05, .06), (.08, .015, .1), "metal", bevel=.004, rot=(-20, 0, 0))
    it.box((0, .02, .15), (.26, .012, .18), "black", bevel=.012, rot=(-20, 0, 0))
    it.box((0, .013, .152), (.24, .004, .16), "screen", bevel=0, rot=(-20, 0, 0), outline=False)


@item("speakers", "Desk speakers", "desk_gear", mount="table")
def speakers(it):
    for sx in (-1, 1):
        it.box((sx * .22, 0, .1), (.11, .12, .2), "wood_mid", bevel=.02)
        it.cyl((sx * .22, -.061, .07), (.07, .07), .006, "charcoal", seg=12, rot=(90, 0, 0), outline=False)
        it.cyl((sx * .22, -.061, .155), (.035, .035), .006, "charcoal", seg=10, rot=(90, 0, 0), outline=False)


@item("mug_set", "Mug + notes", "desk_gear", mount="table")
def mug_set(it):
    it.cyl((0, 0, .05), (.08, .08), .1, "coral", seg=14)
    it.cyl((0, 0, .1), (.065, .065), .004, "wood_dark", seg=14, outline=False)   # coffee
    it.stick((.04, 0, .075), (.06, 0, .05), .014, "coral", seg=6)
    it.stick((.06, 0, .05), (.04, 0, .025), .014, "coral", seg=6)
    it.box((.15, .02, .004), (.08, .08, .008), "butter", bevel=0)                 # sticky pad
    it.cyl((-.13, .02, .05), (.07, .07), .1, "sky", seg=12)                       # pen cup
    for k, c in enumerate(("blue", "coral", "charcoal")):
        it.stick((-.13 + (k - 1) * .015, .02, .08), (-.13 + (k - 1) * .025, .02 + k * .006, .16), .01, c, seg=5)


# =========================================================================== WORK: desks
@item("l_desk", "Corner L desk", "work")
def l_desk(it):
    h = .75
    it.box((0, 0, h - .03), (1.6, .7, .06), "wood_light", bevel=.02)
    it.box((-.45, -.6, h - .03), (.7, .55, .06), "wood_light", bevel=.02)          # return wing
    for x, y in ((.74, -.29), (.74, .29), (-.74, .29), (-.74, -.82), (-.16, -.82)):
        it.box((x, y, (h - .06) / 2), (.05, .05, h - .06), "charcoal", bevel=.012)
    it.box((.45, .02, .5), (.42, .58, .4), "offwhite", bevel=.02)                  # pedestal
    for z in (.6, .4):
        it.box((.45, -.27, z), (.38, .02, .17), "peach", bevel=.015)


@item("bench_desk", "4-seat bench desk", "work")
def bench_desk(it):
    w, d, h = 2.4, 1.4, .75
    it.box((0, 0, h - .03), (w, d, .05), "wood_light", bevel=.02)
    it.box((0, 0, h + .2), (w - .1, .04, .4), "sage", bevel=.02)                  # center screen
    it.box((0, 0, h + .41), (w - .08, .05, .025), "white", bevel=.01)
    for sx in (-1, 0, 1):
        it.box((sx * (w / 2 - .06), 0, (h - .05) / 2), (.05, d - .12, .05), "grey", bevel=.012)
        for sy in (-1, 1):
            it.box((sx * (w / 2 - .06), sy * (d / 2 - .08), (h - .05) / 2), (.05, .05, h - .05), "grey",
                   bevel=.012)
    it.box((0, 0, .45), (w - .2, .2, .04), "charcoal", bevel=.01)                 # cable tray


@item("reception_desk", "Reception desk", "work")
def reception_desk(it):
    w, h = 1.8, 1.05
    it.box((0, 0, h / 2), (w, .6, h), "white", bevel=.04)
    it.box((0, -.05, h + .02), (w + .04, .5, .04), "wood_mid", bevel=.015)        # counter top
    it.box((0, .15, .74), (w - .1, .3, .03), "wood_light", bevel=.01)            # work surface (back)
    it.box((0, -.302, .5), (w - .2, .01, .2), "sky", bevel=0, outline=False)     # front stripe
    it.box((0, -.306, .5), (.36, .01, .1), "white", bevel=0, outline=False)      # logo plate
    it.cyl((.6, -.05, h + .1), (.12, .12), .12, "white", seg=12)                 # bell/plant pot
    it.ball((.6, -.05, h + .2), (.18, .18, .14), "leaf", seg=10)


@item("side_table", "Round side table", "lounge")
def side_table(it):
    it.cyl((0, 0, .015), (.32, .32), .03, "wood_dark", seg=20, bevel=.01)
    it.cyl((0, 0, .26), (.05, .05), .48, "wood_dark", seg=10)
    it.cyl((0, 0, .52), (.5, .5), .04, "wood_light", seg=24, bevel=.015)
    it.cyl((.1, .05, .58), (.08, .08), .08, "white", seg=12)                    # cup
    it.box((-.1, -.02, .545), (.18, .13, .01), "blue", bevel=0, rot=(0, 0, 12))   # magazine


# =========================================================================== STORAGE
@item("locker", "Locker (3 doors)", "storage")
def locker(it):
    w, d, h = .9, .45, 1.8
    it.box((0, 0, h / 2 + .05), (w, d, h - .1), "grey_light", bevel=.02)
    it.box((0, 0, .03), (w - .04, d - .04, .06), "charcoal", bevel=.01)
    for i, c in enumerate(("sky", "mint", "butter")):
        x = (i - 1) * .29
        it.box((x, -d / 2, h / 2 + .05), (.27, .02, h - .16), c, bevel=.015)
        for k in range(3):   # vents
            it.box((x, -d / 2 - .012, 1.6 - k * .04), (.14, .004, .015), "white", bevel=0, outline=False)
        it.box((x + .09, -d / 2 - .02, 1.0), (.03, .02, .12), "white", bevel=.006)
        it.box((x, -d / 2 - .012, 1.3), (.1, .004, .05), "paper", bevel=0, outline=False)   # name tag


@item("drawer_cart", "Drawer cart", "storage")
def drawer_cart(it):
    w, d = .4, .5
    for sx in (-1, 1):
        for sy in (-1, 1):
            it.cyl((sx * .15, sy * .2, .025), (.05, .05), .03, "black", seg=6, rot=(0, 90, 0))
    it.box((0, 0, .34), (w, d, .6), "white", bevel=.02)
    for i, c in enumerate(("coral", "butter", "sky")):
        z = .54 - i * .19
        it.box((0, -d / 2, z), (w - .04, .02, .16), c, bevel=.012)
        it.box((0, -d / 2 - .015, z + .04), (.12, .015, .02), "white", bevel=.006)


@item("cubby_shelf", "Cubby shelf", "storage")
def cubby_shelf(it):
    w, d, h, t = 1.2, .35, .8, .03
    it.box((0, d / 2 - .01, h / 2), (w, .02, h), "wood_mid", bevel=0)                   # back
    for z in (t / 2, h / 2, h - t / 2):                                                  # bottom / mid / top
        it.box((0, 0, z), (w, d, t), "wood_light", bevel=.008)
    for k in range(4):                                                                   # sides + dividers
        it.box((-w / 2 + t / 2 + k * (w - t) / 3, 0, h / 2), (t, d, h), "wood_light", bevel=.008)
    for x, z, c in ((-.39, .03, "coral"), (.39, .415, "sage"), (0, .03, "sky")):        # fabric bins
        it.box((x, -.02, z + .15), (.3, .28, .3), c, bevel=.03)
        it.box((x, -.165, z + .23), (.1, .01, .03), "white", bevel=0, outline=False)
    for k in range(5):                                                                   # books, top-left cube
        it.box((-.5 + k * .05, .0, .415 + .12 - (k % 3) * .015), (.04, .22, .24 - (k % 3) * .03), BOOKS[k],
               bevel=0)
    it.cyl((0, 0, .415 + .07), (.14, .14), .14, "pot", seg=12)                           # plant, top-middle
    it.ball((0, 0, .415 + .2), (.22, .22, .16), "leaf", seg=10)


@item("coat_rack", "Coat rack", "storage")
def coat_rack(it):
    it.cyl((0, 0, .02), (.4, .4), .04, "wood_dark", seg=20, bevel=.012)
    it.cyl((0, 0, .9), (.05, .05), 1.72, "wood_dark", seg=10)
    it.ball((0, 0, 1.78), (.08, .08, .08), "wood_dark", seg=10)
    for i in range(4):
        deg = i * 90 + 45
        p0 = _polar(.02, deg, 1.6)
        p1 = _polar(.14, deg, 1.7)
        it.stick(p0, p1, .025, "wood_dark", seg=6)
        it.ball(p1, (.04, .04, .04), "butter", seg=8)
    it.box((.12, -.05, 1.35), (.2, .14, .5), "coral", bevel=.05, rot=(0, -6, 30))   # hanging jacket
    it.ball((-.1, .06, 1.55), (.2, .18, .14), "sky", seg=10)                          # hat on a hook


@item("umbrella_stand", "Umbrella stand", "storage")
def umbrella_stand(it):
    it.cyl((0, 0, .25), (.24, .24), .5, "charcoal", seg=16, top=1.08)
    it.cyl((0, 0, .5), (.22, .22), .005, "black", seg=16, outline=False)
    for (x, y, c, lean) in ((-.04, .02, "coral", 8), (.05, -.02, "sky", -10)):
        it.stick((x, y, .1), (x + lean * .004, y, .98), .02, "black", seg=5)
        it.cyl((x + lean * .003, y, .7), (.11, .11), .4, c, seg=8, top=.25)     # furled canopy
        it.ball((x + lean * .004, y, .98), (.05, .05, .05), "wood_dark", seg=8)  # handle


# =========================================================================== DECOR
@item("cactus", "Cactus pot", "decor", mount="table")
def cactus(it):
    it.cyl((0, 0, .055), (.13, .13), .11, "pot", seg=14, top=1.1, bevel=.01)
    it.cyl((0, 0, .11), (.13, .13), .004, "soil", seg=14, outline=False)
    it.ball((0, 0, .2), (.08, .08, .2), "leaf", seg=10)
    it.ball((.05, 0, .21), (.04, .04, .09), "leaf", seg=8, rot=(0, 30, 0))
    it.ball((0, -.03, .31), (.03, .03, .03), "blush", seg=8)                    # flower


@item("flower_vase", "Flower vase", "decor", mount="table")
def flower_vase(it):
    it.cyl((0, 0, .1), (.12, .12), .2, "sky", seg=14, top=.6)
    for i, c in enumerate(("coral", "butter", "blush", "lavender")):
        deg = i * 90 + 20
        tip = _polar(.07, deg, .34 + (i % 2) * .04)
        it.stick((0, 0, .18), tip, .01, "leaf_dark", seg=5)
        it.ball(tip, (.07, .07, .05), c, seg=8)
        it.ball(tip[:2] + (tip[2] + .015,), (.025, .025, .02), "butter" if c != "butter" else "white", seg=6,
                outline=False)


@item("plant_snake", "Snake plant", "decor")
def plant_snake(it):
    it.cyl((0, 0, .17), (.3, .3), .34, "white", seg=16, top=.85, bevel=.02)
    it.cyl((0, 0, .34), (.27, .27), .004, "soil", seg=16, outline=False)
    for i in range(7):
        deg = i * 51
        h = .45 + (i % 3) * .12
        it.cyl(_polar(.09, deg, .34 + h / 2), (.07, .025), h, "leaf_dark" if i % 2 else "leaf", seg=6, top=.2,
               rot=(0, 8, deg))


@item("plant_hanging", "Hanging planter", "decor", mount="wall", mount_z=1.6)
def plant_hanging(it):
    it.box((0, -.02, .5), (.06, .04, .04), "wood_dark", bevel=.008)              # wall hook
    it.stick((0, -.04, .5), (0, -.16, .48), .015, "wood_dark", seg=5)
    for sx in (-1, 1):
        it.stick((0, -.16, .48), (sx * .09, -.16, .22), .006, "wood_light", seg=4, outline=False)
    it.stick((0, -.16, .48), (0, -.25, .22), .006, "wood_light", seg=4, outline=False)
    it.ball((0, -.16, .18), (.22, .22, .16), "white", seg=12)
    for i in range(6):   # trailing vines
        deg = i * 60
        x, y, _ = _polar(.1, deg)
        it.ball((x, -.16 + y, .24), (.08, .08, .05), "leaf", seg=8)
        it.ball((x * 1.2, -.16 + y * 1.2, .14 - (i % 3) * .04), (.05, .05, .07), "leaf_dark", seg=6)


@item("hex_panels", "Acoustic hex panels", "decor", mount="wall", mount_z=1.2)
def hex_panels(it):
    cols = ("sage", "mint", "sky", "lavender", "sage", "butter")
    cells = ((0, 0), (1, 0), (2, 0), (.5, 1), (1.5, 1), (1, 2))
    for (cx, cz), c in zip(cells, cols):
        x, z = (cx - 1) * .33, .19 + cz * .29
        it.cyl((x, -.02, z), (.36, .36), .04, c, seg=6, rot=(90, 0, 30), bevel=.008)


@item("calendar", "Wall calendar", "decor", mount="wall", mount_z=1.3)
def calendar(it):
    it.box((0, -.005, .2), (.3, .01, .4), "paper", bevel=.004)
    it.box((0, -.012, .33), (.3, .006, .14), "coral", bevel=0, outline=False)
    for r in range(4):
        for k in range(5):
            it.box((-.11 + k * .055, -.012, .21 - r * .045), (.04, .004, .03),
                   "blush" if (r, k) == (1, 2) else "grey_light", bevel=0, outline=False)
    it.cyl((0, -.012, .4), (.02, .02), .01, "charcoal", seg=8, rot=(90, 0, 0))


@item("mirror_round", "Round mirror", "decor", mount="wall", mount_z=1.2)
def mirror_round(it):
    it.cyl((0, -.02, .3), (.6, .6), .04, "wood_light", seg=32, rot=(90, 0, 0), bevel=.012)
    it.cyl((0, -.042, .3), (.52, .52), .006, "glass", seg=32, rot=(90, 0, 0), outline=False)
    it.box((-.1, -.046, .38), (.12, .004, .025), "white", bevel=0, rot=(0, 30, 0), outline=False)   # glint
