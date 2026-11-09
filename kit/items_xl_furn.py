"""Kit v8, part 1: more furniture -- tables, seating, desks, storage, meeting.

Every item is its own model (no color-only variants). Same conventions as items.py:
pivot bottom center, front -Y, meters, wall items have their back on y=0.
"""
import math

from items import BOOKS, _book_row, _polar, _star_base, item

WOOD = ("wood_light", "wood_mid", "wood_dark")


# ---------------------------------------------------------------- shared helpers
def legs4(it, w, d, h, m="charcoal", dia=.04, inset=.06, splay=0.0):
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = sx * (w / 2 - inset), sy * (d / 2 - inset)
            it.stick((x + sx * splay, y + sy * splay, 0), (x, y, h), dia, m, seg=6)


def top_slab(it, w, d, z, m="wood_light", t=.04, bevel=.012):
    it.box((0, 0, z - t / 2), (w, d, t), m, bevel=bevel)


def round_top(it, dia, z, m="wood_light", t=.04, seg=24, dy=None):
    it.cyl((0, 0, z - t / 2), (dia, dy or dia), t, m, seg=seg, bevel=.01)


def pedestal(it, z, base=.4, m="charcoal"):
    it.cyl((0, 0, .015), (base, base), .03, m, seg=16, bevel=.008)
    it.cyl((0, 0, z / 2), (.07, .07), z - .03, m, seg=10)


def cushion(it, c, size, m, bevel=.04):
    it.box(c, size, m, bevel=bevel)


def sofa_block(it, w, d, m, arm_m=None, seat_z=.42, back_h=.38, arms=(True, True), legs=True):
    arm_m = arm_m or m
    base_z = .12 if legs else 0
    it.box((0, 0, base_z + (seat_z - base_z) / 2 - .05), (w, d, seat_z - base_z - .1), m, bevel=.03)
    n = max(1, round(w / .7))
    cw = (w - (.24 if any(arms) else .04)) / n
    for i in range(n):
        x = -w / 2 + (.12 if arms[0] else .02) + cw * (i + .5)
        cushion(it, (x, -.04, seat_z - .06), (cw - .02, d - .2, .14), m)
        cushion(it, (x, d / 2 - .12, seat_z + back_h / 2 - .02), (cw - .02, .16, back_h), m)
    for k, sx in enumerate((-1, 1)):
        if arms[k]:
            it.box((sx * (w / 2 - .06), 0, seat_z - .02), (.12, d, .3), arm_m, bevel=.04)
    if legs:
        for sx in (-1, 1):
            for sy in (-1, 1):
                it.cyl((sx * (w / 2 - .08), sy * (d / 2 - .08), .05), (.04, .04), .1, "wood_dark", seg=6)


def chair_basic(it, seat_m, frame_m="charcoal", seat_z=.47, back=True, back_h=.36, w=.44, d=.44, leg_dia=.03):
    legs4(it, w, d, seat_z - .04, frame_m, dia=leg_dia, inset=.04)
    cushion(it, (0, 0, seat_z - .025), (w, d, .05), seat_m, bevel=.015)
    if back:
        it.box((0, d / 2 - .02, seat_z + back_h / 2), (w, .04, back_h), seat_m, bevel=.015, rot=(-6, 0, 0))


def doors_front(it, w, z0, z1, y, m, n=2, knob="metal"):
    dw = w / n
    for i in range(n):
        x = -w / 2 + dw * (i + .5)
        it.box((x, y, (z0 + z1) / 2), (dw - .015, .02, z1 - z0 - .015), m, bevel=.006)
        kx = x + (dw / 2 - .05) * (1 if i % 2 == 0 else -1) * (-1 if n == 1 else 1)
        it.ball((kx, y - .02, (z0 + z1) / 2), (.025, .025, .025), knob, seg=6)


def cabinet(it, w, d, h, m="white", base=.05):
    it.box((0, 0, base + (h - base) / 2), (w, d, h - base), m, bevel=.012)
    it.box((0, .01, base / 2), (w - .04, d - .04, base), "charcoal", bevel=0)


# =========================================================================== TABLES
@item("table_round_cafe", "Cafe table (round)", "tables")
def table_round_cafe(it):
    pedestal(it, .72, .44)
    round_top(it, .7, .74, "wood_light")


@item("table_bistro_marble", "Bistro table", "tables")
def table_bistro_marble(it):
    it.cyl((0, 0, .02), (.38, .38), .04, "black", seg=16, bevel=.01)
    it.cyl((0, 0, .37), (.05, .05), .66, "black", seg=8)
    it.cyl((0, 0, .58), (.18, .18), .02, "black", seg=12)
    round_top(it, .6, .74, "offwhite", t=.03)


@item("table_dining_long", "Long dining table", "tables")
def table_dining_long(it):
    top_slab(it, 2.0, .9, .75, "wood_mid", t=.05)
    for sx in (-1, 1):
        it.box((sx * .82, 0, .36), (.06, .7, .72), "wood_dark", bevel=.01)
        it.box((sx * .82, 0, .03), (.1, .8, .06), "wood_dark", bevel=.01)
    it.box((0, 0, .2), (1.6, .05, .06), "wood_dark", bevel=.008)


@item("table_dining_round", "Round dining table", "tables")
def table_dining_round(it):
    round_top(it, 1.1, .75, "wood_light", t=.05)
    for i in range(4):
        deg = 45 + i * 90
        it.stick(_polar(.36, deg, 0), _polar(.12, deg, .72), .05, "wood_mid", seg=6)


@item("table_high_bar", "High bar table", "tables")
def table_high_bar(it):
    top_slab(it, 1.4, .55, 1.05, "wood_dark", t=.05)
    for sx in (-1, 1):
        it.box((sx * .58, 0, .52), (.05, .05, 1.0), "black", bevel=0)
        it.box((sx * .58, 0, .02), (.08, .45, .04), "black", bevel=0)
    it.box((0, -.15, .3), (1.16, .03, .03), "metal", bevel=0)


@item("table_folding", "Folding table", "tables")
def table_folding(it):
    top_slab(it, 1.2, .6, .74, "offwhite", t=.03)
    for sx in (-1, 1):
        it.stick((sx * .5, -.25, 0), (sx * .5, .25, .7), .03, "grey", seg=6)
        it.stick((sx * .5, .25, 0), (sx * .5, -.25, .7), .03, "grey", seg=6)


@item("table_coffee_round", "Round coffee table", "tables")
def table_coffee_round(it):
    round_top(it, .8, .4, "wood_light", t=.05)
    it.cyl((0, 0, .17), (.6, .6), .02, "wood_mid", seg=20, bevel=.005)
    for i in range(3):
        it.stick(_polar(.3, 90 + i * 120, 0), _polar(.3, 90 + i * 120, .38), .04, "wood_dark", seg=6)


@item("table_nesting", "Nesting tables", "tables")
def table_nesting(it):
    for k, (s, h, x, m) in enumerate(((.5, .48, -.12, "wood_mid"), (.38, .38, .14, "sage"))):
        it.box((x, -k * .05, h - .015), (s, s, .03), m, bevel=.01)
        for sx in (-1, 1):
            for sy in (-1, 1):
                it.stick((x + sx * (s / 2 - .03), -k * .05 + sy * (s / 2 - .03), 0),
                         (x + sx * (s / 2 - .03), -k * .05 + sy * (s / 2 - .03), h - .03), .02, "black", seg=5)


@item("table_side_c", "C-shaped side table", "tables")
def table_side_c(it):
    it.box((0, .05, .015), (.36, .4, .03), "black", bevel=.005)
    it.box((.16, .05, .3), (.03, .03, .6), "black", bevel=0)
    it.box((.03, .05, .6), (.3, .4, .025), "wood_light", bevel=.008)


@item("table_conference_oval", "Oval conference table", "tables")
def table_conference_oval(it):
    it.cyl((0, 0, .735), (2.6, 1.2), .05, "wood_mid", seg=32, bevel=.012)
    for sx in (-1, 1):
        it.box((sx * .7, 0, .36), (.12, .5, .7), "charcoal", bevel=.02)
    it.box((0, 0, .77), (.3, .14, .02), "black", bevel=.004)          # power hub


@item("table_conference_boat", "Boat-shaped conference table", "tables")
def table_conference_boat(it):
    for i in range(7):
        x = -1.35 + i * .45
        wd = 1.25 - abs(x) * .3
        it.box((x, 0, .735), (.46, wd, .05), "wood_light", bevel=.004)
    for sx in (-1, 1):
        it.cyl((sx * .8, 0, .36), (.4, .3), .7, "white", seg=12)


@item("table_workbench", "Maker workbench", "tables")
def table_workbench(it):
    top_slab(it, 1.6, .7, .9, "wood_mid", t=.06)
    legs4(it, 1.6, .7, .87, "charcoal", dia=.06, inset=.06)
    top_slab(it, 1.46, .56, .25, "wood_light", t=.03)
    it.box((0, .33, 1.25), (1.5, .03, .7), "grey_light", bevel=.006)   # pegboard back
    for i in range(6):
        it.box((-.6 + i * .24, .3, 1.2 + (i % 2) * .15), (.03, .03, .12), BOOKS[i % 7], bevel=0)


@item("table_drafting", "Drafting table", "tables")
def table_drafting(it):
    for sx in (-1, 1):
        it.stick((sx * .45, -.25, 0), (sx * .4, .1, .85), .04, "metal", seg=6)
        it.stick((sx * .45, .3, 0), (sx * .4, .1, .85), .04, "metal", seg=6)
    it.box((0, .0, .92), (1.1, .75, .03), "offwhite", bevel=.006, rot=(20, 0, 0))
    it.box((0, -.34, .8), (1.0, .03, .03), "wood_mid", bevel=0, rot=(20, 0, 0))
    it.box((.2, -.05, .95), (.4, .3, .004), "paper", bevel=0, rot=(20, 0, 0))


@item("table_console", "Console table", "tables")
def table_console(it):
    top_slab(it, 1.2, .35, .8, "wood_dark", t=.04)
    legs4(it, 1.2, .35, .78, "black", dia=.025, inset=.03)
    top_slab(it, 1.12, .3, .2, "wood_dark", t=.025)
    it.ball((-.35, 0, .87), (.14, .14, .14), "lavender", seg=10)
    it.box((.3, 0, .84), (.28, .2, .05), BOOKS[1], bevel=.005)


@item("table_low_lesehan", "Low floor table", "tables")
def table_low_lesehan(it):
    top_slab(it, 1.2, .7, .33, "wood_mid", t=.05)
    for sx in (-1, 1):
        it.box((sx * .5, 0, .15), (.08, .55, .3), "wood_dark", bevel=.01)


@item("table_standing_round", "Standing round table", "tables")
def table_standing_round(it):
    pedestal(it, 1.05, .5, "white")
    round_top(it, .7, 1.07, "white", t=.03)
    it.cyl((0, 0, .25), (.4, .4), .02, "metal", seg=16)


@item("table_picnic", "Picnic table", "tables")
def table_picnic(it):
    top_slab(it, 1.6, .7, .75, "wood_mid", t=.05)
    for sy in (-1, 1):
        it.box((0, sy * .62, .44), (1.6, .3, .04), "wood_mid", bevel=.006)
    for sx in (-1, 1):
        it.stick((sx * .6, -.7, 0), (sx * .6, .1, .73), .06, "wood_dark", seg=6)
        it.stick((sx * .6, .7, 0), (sx * .6, -.1, .73), .06, "wood_dark", seg=6)


@item("table_glass_round", "Glass round table", "tables")
def table_glass_round(it):
    for i in range(3):
        deg = 90 + i * 120
        it.stick(_polar(.32, deg, 0), _polar(.08, deg + 60, .72), .03, "black", seg=6)
    round_top(it, .9, .75, "glass", t=.02)


@item("table_ottoman_tray", "Tray table", "tables")
def table_ottoman_tray(it):
    it.cyl((0, 0, .38), (.56, .56), .06, "butter", seg=20, bevel=.015)
    it.cyl((0, 0, .41), (.48, .48), .01, "offwhite", seg=20, outline=False)
    for i in range(4):
        it.stick(_polar(.22, 45 + i * 90, 0), _polar(.22, 45 + i * 90, .35), .035, "wood_mid", seg=6)


@item("table_counter_island", "Kitchen island", "tables")
def table_counter_island(it):
    cabinet(it, 1.6, .8, .9, "sage")
    top_slab(it, 1.7, .9, .94, "offwhite", t=.04)
    doors_front(it, 1.5, .1, .85, -.41, "sage", n=3)


# =========================================================================== SEATING (more)
@item("sofa_2seat", "Two-seat sofa", "seating")
def sofa_2seat(it):
    sofa_block(it, 1.5, .85, "sky")


@item("sofa_l_shape", "L-shaped sofa", "seating")
def sofa_l_shape(it):
    sofa_block(it, 2.2, .85, "sage", arms=(True, False))
    it.box((1.2, -.45, .25), (.8, 1.0, .3), "sage", bevel=.03)
    cushion(it, (1.2, -.5, .43), (.72, .92, .12), "sage")
    it.box((1.55, -.45, .5), (.12, 1.0, .3), "sage", bevel=.04)


@item("sofa_curved", "Curved lobby sofa", "seating")
def sofa_curved(it):
    for i in range(7):
        deg = -60 + i * 20
        x, y = math.sin(math.radians(deg)) * 1.4, -math.cos(math.radians(deg)) * 1.4 + 1.4
        it.box((x, y, .22), (.5, .7, .3), "lavender", bevel=.015, rot=(0, 0, deg))
        it.box((x + math.sin(math.radians(deg)) * .32, y - math.cos(math.radians(deg)) * -.32, .55),
               (.5, .15, .4), "lavender", bevel=.015, rot=(0, 0, deg))


@item("loveseat_round", "Round-arm loveseat", "seating")
def loveseat_round(it):
    it.box((0, 0, .26), (1.2, .78, .32), "blush", bevel=.05)
    cushion(it, (0, -.04, .46), (.92, .6, .12), "blush")
    it.cyl((0, .3, .6), (1.2, .22), .4, "blush", seg=14, bevel=.04)
    for sx in (-1, 1):
        it.cyl((sx * .58, 0, .45), (.2, .78), .2, "blush", seg=12, rot=(90, 0, 0))
    for sx in (-1, 1):
        it.cyl((sx * .5, 0, .05), (.05, .05), .1, "wood_dark", seg=6)


@item("chaise_lounge", "Chaise lounge", "seating")
def chaise_lounge(it):
    it.box((0, 0, .2), (.7, 1.6, .2), "peach", bevel=.04)
    it.box((0, .55, .45), (.7, .5, .2), "peach", bevel=.05, rot=(35, 0, 0))
    it.cyl((0, .75, .55), (.2, .2), .66, "butter", seg=12, rot=(0, 90, 0))
    for sx in (-1, 1):
        for sy in (-1, 1):
            it.cyl((sx * .28, sy * .7, .05), (.04, .04), .1, "wood_dark", seg=6)


@item("chair_rocking", "Rocking chair", "seating")
def chair_rocking(it):
    for sx in (-1, 1):
        for i in range(6):
            a0, a1 = -50 + i * 16.6, -50 + (i + 1) * 16.6
            p0 = (sx * .24, math.sin(math.radians(a0)) * .9, .95 - math.cos(math.radians(a0)) * .9 + .02)
            p1 = (sx * .24, math.sin(math.radians(a1)) * .9, .95 - math.cos(math.radians(a1)) * .9 + .02)
            it.stick(p0, p1, .04, "wood_mid", seg=5)
        it.stick((sx * .24, -.2, .08), (sx * .24, -.2, .44), .035, "wood_mid", seg=5)
        it.stick((sx * .24, .2, .08), (sx * .24, .3, .95), .035, "wood_mid", seg=5)
    cushion(it, (0, 0, .46), (.5, .46, .06), "coral", bevel=.02)
    it.box((0, .25, .72), (.5, .05, .44), "wood_mid", bevel=.01, rot=(-12, 0, 0))


@item("chair_egg", "Egg chair", "seating")
def chair_egg(it):
    pedestal(it, .25, .5, "metal")
    it.ball((0, .05, .7), (.85, .8, 1.05), "white", seg=16)
    it.ball((0, -.12, .68), (.62, .6, .8), "sky", seg=14)
    cushion(it, (0, -.1, .38), (.5, .45, .1), "sky", bevel=.03)


@item("chair_hanging", "Hanging pod chair", "seating")
def chair_hanging(it):
    it.cyl((0, .1, .02), (.6, .6), .04, "charcoal", seg=16, bevel=.01)
    it.stick((0, .3, .04), (0, .3, 1.85), .05, "charcoal", seg=8)
    it.stick((0, .3, 1.85), (0, 0, 1.95), .05, "charcoal", seg=8)
    it.stick((0, 0, 1.95), (0, 0, 1.35), .015, "metal", seg=5)
    it.ball((0, 0, .9), (.8, .75, .95), "wood_light", seg=14)
    it.ball((0, -.18, .85), (.6, .5, .7), "butter", seg=12)


@item("bean_sofa", "Bean sofa", "seating")
def bean_sofa(it):
    it.ball((0, 0, .22), (1.3, .9, .45), "coral", seg=16)
    it.ball((0, .3, .5), (1.2, .4, .55), "coral", seg=14)


@item("floor_cushion", "Floor cushion", "seating")
def floor_cushion(it):
    it.cyl((0, 0, .07), (.6, .6), .14, "butter", seg=16, bevel=.05)
    it.ball((0, 0, .14), (.06, .06, .03), "wood_dark", seg=8)


@item("ottoman_square", "Square ottoman", "seating")
def ottoman_square(it):
    it.box((0, 0, .21), (.55, .55, .34), "lavender", bevel=.05)
    for sx in (-1, 1):
        for sy in (-1, 1):
            it.cyl((sx * .22, sy * .22, .025), (.04, .04), .05, "wood_dark", seg=6)


@item("ottoman_round_tufted", "Tufted round ottoman", "seating")
def ottoman_round_tufted(it):
    it.cyl((0, 0, .2), (.6, .6), .38, "sage", seg=20, bevel=.05)
    for i in range(6):
        x, y, _ = _polar(.16, i * 60)
        it.ball((x, y, .39), (.035, .035, .02), "leaf_dark", seg=6, outline=False)


@item("bench_padded", "Padded bench", "seating")
def bench_padded(it):
    cushion(it, (0, 0, .42), (1.4, .42, .1), "blue", bevel=.03)
    legs4(it, 1.4, .42, .37, "black", dia=.03, inset=.05)


@item("bench_storage", "Storage bench", "seating")
def bench_storage(it):
    it.box((0, 0, .2), (1.0, .4, .4), "wood_light", bevel=.015)
    for i in range(3):
        it.box((-.32 + i * .32, -.19, .2), (.26, .02, .3), "offwhite", bevel=.006)
        it.box((-.32 + i * .32, -.24, .2), (.14, .06, .2), BOOKS[i], bevel=.02)
    cushion(it, (0, 0, .44), (1.0, .4, .08), "coral", bevel=.025)


@item("stool_tripod", "Tripod stool", "seating")
def stool_tripod(it):
    for i in range(3):
        deg = 90 + i * 120
        it.stick(_polar(.18, deg, 0), _polar(.1, deg, .44), .03, "wood_mid", seg=6)
    it.cyl((0, 0, .45), (.34, .34), .04, "wood_light", seg=16, bevel=.01)


@item("stool_stacking", "Stacking stools", "seating")
def stool_stacking(it):
    for k in range(3):
        z = k * .07
        it.cyl((0, 0, .44 + z), (.34, .34), .03, BOOKS[k + 2], seg=16, bevel=.008)
        for i in range(3):
            deg = 90 + i * 120
            it.stick(_polar(.14 + .01 * k, deg, z), _polar(.13, deg, .43 + z), .025, "black", seg=5)


@item("chair_kneeling", "Kneeling chair", "seating")
def chair_kneeling(it):
    for sx in (-1, 1):
        it.box((sx * .2, 0, .03), (.04, .7, .06), "wood_mid", bevel=.01)
        it.stick((sx * .2, .2, .05), (sx * .2, -.05, .55), .04, "wood_mid", seg=6)
    cushion(it, (0, -.05, .56), (.44, .34, .07), "charcoal", bevel=.02)
    cushion(it, (0, -.3, .3), (.44, .18, .06), "charcoal", bevel=.02)


@item("ball_chair_yoga", "Balance ball", "seating")
def ball_chair_yoga(it):
    it.ball((0, 0, .33), (.65, .65, .65), "mint", seg=16)
    it.cyl((0, 0, .02), (.4, .4), .04, "charcoal", seg=14, bevel=.01)


@item("chair_director", "Director chair", "seating")
def chair_director(it):
    for sx in (-1, 1):
        it.stick((sx * .25, -.22, 0), (sx * .25, .22, .45), .035, "wood_dark", seg=5)
        it.stick((sx * .25, .22, 0), (sx * .25, -.22, .45), .035, "wood_dark", seg=5)
        it.stick((sx * .25, .22, .45), (sx * .25, .24, 1.0), .035, "wood_dark", seg=5)
        it.box((sx * .25, 0, .66), (.05, .44, .04), "wood_dark", bevel=.008)
    it.box((0, 0, .47), (.5, .42, .02), "black", bevel=0)
    it.box((0, .24, .88), (.5, .02, .2), "black", bevel=0)


@item("chair_folding", "Folding chair", "seating")
def chair_folding(it):
    for sx in (-1, 1):
        it.stick((sx * .2, -.22, 0), (sx * .2, .18, .85), .025, "grey", seg=5)
        it.stick((sx * .2, .22, 0), (sx * .2, -.15, .45), .025, "grey", seg=5)
    it.box((0, -.02, .46), (.42, .38, .025), "sky", bevel=.006)
    it.box((0, .14, .76), (.42, .03, .16), "sky", bevel=.006, rot=(-15, 0, 0))


@item("chair_sling", "Sling lounge chair", "seating")
def chair_sling(it):
    for sx in (-1, 1):
        it.stick((sx * .3, -.35, 0), (sx * .3, -.25, .5), .03, "black", seg=5)
        it.stick((sx * .3, .35, 0), (sx * .3, .3, .8), .03, "black", seg=5)
        it.stick((sx * .3, -.25, .5), (sx * .3, .3, .8), .03, "black", seg=5)
    it.box((0, .0, .38), (.56, .5, .03), "wood_light", bevel=.006, rot=(-25, 0, 0))
    it.box((0, .22, .62), (.56, .03, .4), "wood_light", bevel=.006, rot=(-20, 0, 0))


@item("stool_bar_back", "Bar stool with back", "seating")
def stool_bar_back(it):
    legs4(it, .38, .38, .72, "black", dia=.025, inset=.03, splay=.03)
    it.box((0, 0, .21), (.34, .34, .02), "black", bevel=0)
    cushion(it, (0, 0, .74), (.4, .4, .06), "wood_mid", bevel=.015)
    it.box((0, .18, .92), (.38, .03, .25), "wood_mid", bevel=.01)


@item("booth_seat", "Booth seat", "seating")
def booth_seat(it):
    it.box((0, 0, .2), (1.4, .55, .4), "wood_dark", bevel=.012)
    cushion(it, (0, -.02, .45), (1.36, .5, .1), "coral")
    it.box((0, .25, .75), (1.4, .1, .6), "wood_dark", bevel=.012)
    for i in range(3):
        cushion(it, (-.45 + i * .45, .18, .75), (.42, .08, .48), "coral", bevel=.03)


@item("seat_row_auditorium", "Auditorium seat row", "seating")
def seat_row_auditorium(it):
    for i in range(3):
        x = -.55 + i * .55
        cushion(it, (x, -.05, .45), (.48, .45, .08), "blue", bevel=.025)
        it.box((x, .2, .75), (.48, .08, .55), "blue", bevel=.025, rot=(-8, 0, 0))
    for i in range(4):
        x = -.825 + i * .55
        it.box((x, 0, .35), (.05, .5, .7), "charcoal", bevel=.01)


@item("chair_lounge_wood", "Wooden lounge chair", "seating")
def chair_lounge_wood(it):
    for sx in (-1, 1):
        it.box((sx * .32, 0, .3), (.06, .7, .06), "wood_mid", bevel=.01)
        it.stick((sx * .32, -.3, 0), (sx * .32, -.3, .58), .045, "wood_mid", seg=6)
        it.stick((sx * .32, .3, 0), (sx * .32, .3, .58), .045, "wood_mid", seg=6)
        it.box((sx * .32, 0, .6), (.08, .7, .04), "wood_mid", bevel=.008)
    cushion(it, (0, -.03, .36), (.6, .6, .12), "offwhite")
    cushion(it, (0, .28, .62), (.6, .14, .46), "offwhite", bevel=.04)


# =========================================================================== DESKS (more)
@item("desk_compact", "Compact desk", "work")
def desk_compact(it):
    top_slab(it, 1.0, .55, .75, "white", t=.03)
    legs4(it, 1.0, .55, .73, "wood_light", dia=.035, inset=.05)
    it.box((.32, 0, .64), (.3, .5, .16), "white", bevel=.008)
    it.box((.32, -.255, .64), (.12, .015, .02), "metal", bevel=0)


@item("desk_writing", "Writing desk", "work")
def desk_writing(it):
    top_slab(it, 1.1, .55, .75, "wood_mid", t=.035)
    legs4(it, 1.1, .55, .73, "wood_dark", dia=.04, inset=.04)
    it.box((0, -.0, .66), (1.0, .5, .1), "wood_mid", bevel=.008)
    for sx in (-1, 1):
        it.ball((sx * .25, -.26, .66), (.03, .03, .03), "butter", seg=6)
    it.box((0, .22, .86), (1.0, .1, .2), "wood_dark", bevel=.008)


@item("desk_gaming", "Gaming desk", "work")
def desk_gaming(it):
    top_slab(it, 1.4, .7, .75, "black", t=.03)
    for sx in (-1, 1):
        it.box((sx * .6, 0, .37), (.06, .5, .02), "coral", bevel=0, rot=(0, 0, 0))
        it.stick((sx * .6, -.25, 0), (sx * .6, .25, .72), .05, "black", seg=4)
        it.stick((sx * .6, .25, 0), (sx * .6, -.25, .72), .05, "black", seg=4)
    it.box((0, -.05, .758), (1.3, .5, .006), "lavender", bevel=0, outline=False)   # big desk mat
    it.box((0, -.355, .74), (1.3, .01, .02), "sky", bevel=0, outline=False)       # light strip


@item("desk_trestle", "Trestle desk", "work")
def desk_trestle(it):
    top_slab(it, 1.5, .75, .75, "wood_light", t=.04)
    for sx in (-1, 1):
        it.stick((sx * .55, -.32, 0), (sx * .55, 0, .73), .04, "wood_mid", seg=5)
        it.stick((sx * .55, .32, 0), (sx * .55, 0, .73), .04, "wood_mid", seg=5)
        it.box((sx * .55, 0, .35), (.03, .5, .03), "wood_mid", bevel=0)


@item("desk_glass", "Glass desk", "work")
def desk_glass(it):
    top_slab(it, 1.4, .7, .75, "glass", t=.02, bevel=.004)
    for sx in (-1, 1):
        it.box((sx * .62, 0, .37), (.04, .62, .04), "metal", bevel=0)
        it.box((sx * .62, -.29, .37), (.04, .04, .72), "metal", bevel=0)
        it.box((sx * .62, .29, .37), (.04, .04, .72), "metal", bevel=0)


@item("desk_hot_4", "Hot-desk cluster (4)", "work")
def desk_hot_4(it):
    for sx in (-1, 1):
        for sy in (-1, 1):
            it.box((sx * .62, sy * .36, .735), (1.2, .7, .03), "white", bevel=.006)
    for sx in (-1, 0, 1):
        it.box((sx * 1.2, 0, .36), (.05, 1.3, .7), "charcoal", bevel=.006)
    it.box((0, 0, 1.0), (2.4, .03, .45), "sage", bevel=.012)          # center screen
    it.box((0, 0, .77), (.6, .1, .04), "black", bevel=.004)


@item("desk_cubicle", "Cubicle desk", "work")
def desk_cubicle(it):
    top_slab(it, 1.4, .7, .75, "wood_light", t=.03)
    it.box((0, .38, .62), (1.5, .05, 1.24), "sky", bevel=.012)
    for sx in (-1, 1):
        it.box((sx * .73, 0, .62), (.05, .8, 1.24), "sky", bevel=.012)
    it.box((-.4, 0, .36), (.4, .6, .7), "grey_light", bevel=.008)
    it.box((.3, .34, 1.0), (.4, .01, .3), "cork", bevel=0, outline=False)


@item("desk_u_shape", "U-shaped desk", "work")
def desk_u_shape(it):
    top_slab(it, 1.8, .7, .75, "wood_mid", t=.035)
    for sx in (-1, 1):
        it.box((sx * .55, -.75, .735), (.7, .8, .035), "wood_mid", bevel=.008)
        it.box((sx * .87, -.75, .36), (.05, .78, .72), "wood_dark", bevel=.006)
    it.box((0, .32, .36), (1.76, .04, .7), "wood_dark", bevel=.006)


@item("desk_reception_curve", "Curved reception desk", "work")
def desk_reception_curve(it):
    for i in range(7):
        deg = -45 + i * 15
        x, y = math.sin(math.radians(deg)) * 1.3, -math.cos(math.radians(deg)) * 1.3 + 1.3
        it.box((x, y - .2, .55), (.36, .1, 1.1), "white", bevel=.01, rot=(0, 0, deg))
        it.box((x, y - .1, 1.12), (.36, .3, .04), "wood_light", bevel=0, rot=(0, 0, deg))
        it.box((x, y, .74), (.36, .5, .03), "white", bevel=0, rot=(0, 0, deg))
    it.box((0, -.27, .55), (.8, .01, .08), "sage", bevel=0, outline=False)


@item("desk_with_hutch", "Desk with hutch", "work")
def desk_with_hutch(it):
    top_slab(it, 1.3, .65, .75, "wood_light", t=.03)
    for sx in (-1, 1):
        it.box((sx * .63, 0, .37), (.04, .62, .72), "wood_light", bevel=.006)
    it.box((0, .27, 1.15), (1.3, .1, .8), "wood_light", bevel=.008)
    it.box((0, .2, 1.15), (1.2, .06, .02), "wood_mid", bevel=0)
    _book_row(it, -.55, .1, 1.16, .07, BOOKS, k=1)
    it.box((.35, .2, 1.3), (.4, .02, .2), "cork", bevel=0, outline=False)


@item("desk_floating", "Wall-mounted floating desk", "work", mount="wall", mount_z=.72)
def desk_floating(it):
    it.box((0, -.25, .015), (1.1, .5, .03), "wood_mid", bevel=.008)
    it.box((0, -.04, -.06), (1.1, .08, .12), "wood_dark", bevel=.008)
    it.box((0, -.22, -.03), (.5, .4, .04), "wood_mid", bevel=.006)


@item("desk_hexagon_pod", "Hexagon desk pod", "work")
def desk_hexagon_pod(it):
    for i in range(6):
        deg = i * 60
        it.box(_polar(.55, deg, .735), (.62, .7, .03), "white", bevel=.006, rot=(0, 0, deg + 90))
        it.box(_polar(.95, deg + 30, .55), (.04, .5, 1.1), "mint", bevel=.01, rot=(0, 0, deg + 30))
    it.cyl((0, 0, .36), (.4, .4), .72, "charcoal", seg=6)


@item("desk_standing_crank", "Crank standing desk", "work")
def desk_standing_crank(it):
    top_slab(it, 1.2, .6, 1.05, "wood_light", t=.03)
    for sx in (-1, 1):
        it.box((sx * .5, 0, .5), (.07, .07, 1.0), "white", bevel=.008)
        it.box((sx * .5, 0, .02), (.08, .6, .04), "white", bevel=.008)
    it.stick((.55, -.3, .98), (.62, -.36, .9), .02, "metal", seg=5)
    it.ball((.62, -.38, .9), (.04, .04, .04), "black", seg=6)


@item("desk_kids_play", "Low activity desk", "work")
def desk_kids_play(it):
    top_slab(it, .9, .6, .5, "butter", t=.03)
    legs4(it, .9, .6, .48, "coral", dia=.05, inset=.05)
    for i, m in enumerate(("sky", "sage", "coral")):
        it.box((-.25 + i * .25, 0, .53), (.08, .08, .05), m, bevel=.01)


# =========================================================================== STORAGE (more)
@item("bookshelf_ladder", "Ladder bookshelf", "storage")
def bookshelf_ladder(it):
    for sx in (-1, 1):
        it.stick((sx * .35, -.2, 0), (sx * .35, .15, 1.8), .04, "wood_mid", seg=6)
    for i in range(4):
        z = .1 + i * .45
        y = -.18 + i * .09
        it.box((0, y + .02, z), (.7, .4 - i * .07, .025), "wood_light", bevel=.004)
        _book_row(it, -.3, .2, z + .013, .2, BOOKS, k=i)


@item("bookcase_low", "Low bookcase", "storage")
def bookcase_low(it):
    it.box((0, 0, .45), (1.2, .35, .9), "white", bevel=.01)
    for i in range(2):
        z = .06 + i * .43
        it.box((0, -.02, z + .19), (1.12, .32, .38), "offwhite", bevel=0, outline=False)
        _book_row(it, -.52, .45, z, .2, BOOKS, k=i + 2)
    it.ball((.3, 0, .99), (.16, .16, .18), "sage", seg=10)


@item("credenza", "Credenza", "storage")
def credenza(it):
    cabinet(it, 1.6, .45, .7, "wood_mid")
    for i in range(4):
        x = -.6 + i * .4
        it.box((x, -.23, .38), (.38, .02, .6), "wood_light", bevel=.006)
        it.box((x, -.25, .55), (.12, .02, .015), "black", bevel=0)
    it.cyl((-.5, 0, .82), (.14, .14), .24, "lavender", seg=10, top=.6)


@item("sideboard_slats", "Slatted sideboard", "storage")
def sideboard_slats(it):
    it.box((0, 0, .45), (1.5, .42, .6), "wood_dark", bevel=.01)
    for i in range(18):
        it.box((-.68 + i * .08, -.22, .45), (.04, .02, .54), "wood_mid", bevel=0)
    legs4(it, 1.5, .42, .15, "black", dia=.03, inset=.05)


@item("wardrobe", "Wardrobe", "storage")
def wardrobe(it):
    cabinet(it, 1.0, .6, 2.0, "offwhite")
    doors_front(it, .96, .07, 1.97, -.31, "offwhite", n=2)


@item("filing_lateral", "Lateral filing cabinet", "storage")
def filing_lateral(it):
    cabinet(it, .9, .5, 1.05, "grey")
    for i in range(3):
        z = .1 + i * .32
        it.box((0, -.255, z + .15), (.86, .02, .3), "grey_light", bevel=.006)
        it.box((0, -.27, z + .24), (.25, .02, .02), "charcoal", bevel=0)
        it.box((0, -.268, z + .1), (.12, .006, .05), "paper", bevel=0, outline=False)


@item("shelf_cube_3x3", "Cube shelf 3x3", "storage")
def shelf_cube_3x3(it):
    s, t = .36, .025
    W = 3 * s + 4 * t
    for i in range(4):
        it.box((-W / 2 + t / 2 + i * (s + t), 0, W / 2), (t, .38, W), "white", bevel=0)
        it.box((0, 0, t / 2 + i * (s + t)), (W, .38, t), "white", bevel=0)
    for r in range(3):
        for c in range(3):
            k = r * 3 + c
            x, z = -W / 2 + t + s / 2 + c * (s + t), t + s / 2 + r * (s + t)
            if k % 3 == 0:
                it.box((x, -.02, z), (s - .04, .3, s - .04), BOOKS[k % 7], bevel=.02)   # fabric bin
            elif k % 3 == 1:
                _book_row(it, x - s / 2 + .02, x + s / 2 - .02, z - s / 2, .2, BOOKS, k=k)


@item("shelf_zigzag", "Zigzag shelf", "storage")
def shelf_zigzag(it):
    for i in range(4):
        z = .1 + i * .4
        x = -.15 if i % 2 else .15
        it.box((x, 0, z), (.7, .3, .025), "wood_mid", bevel=.004)
        it.stick((x - .35 * (1 if i % 2 else -1), 0, z), (-x - .35 * (1 if i % 2 else -1) * -1, 0, z + .4), .03,
                 "black", seg=5)
        it.ball((x + .15, 0, z + .08), (.12, .12, .14), BOOKS[i], seg=8)


@item("shelf_tree", "Tree bookshelf", "storage")
def shelf_tree(it):
    it.box((0, 0, .9), (.08, .25, 1.8), "wood_mid", bevel=.008)
    it.box((0, 0, .02), (.6, .3, .04), "wood_mid", bevel=.008)
    for i, (sx, z) in enumerate(((-1, .5), (1, .85), (-1, 1.2), (1, 1.5))):
        it.box((sx * .3, 0, z), (.5, .25, .025), "wood_light", bevel=.004, rot=(0, sx * -8, 0))
        it.box((sx * .3, 0, z + .1), (.2, .18, .16), BOOKS[i], bevel=.01)


@item("mailbox_pigeonhole", "Pigeonhole mailbox", "storage")
def mailbox_pigeonhole(it):
    it.box((0, 0, .9), (1.0, .35, .9), "wood_light", bevel=.008)
    for r in range(4):
        for c in range(5):
            x, z = -.4 + c * .2, .55 + r * .2
            it.box((x, -.16, z), (.17, .04, .16), "wood_dark", bevel=0, outline=False)
            if (r + c) % 3 == 0:
                it.box((x, -.17, z - .03), (.12, .03, .07), "paper", bevel=0, outline=False)
    legs4(it, 1.0, .35, .45, "charcoal", dia=.03, inset=.04)


@item("cabinet_display", "Glass display cabinet", "storage")
def cabinet_display(it):
    it.box((0, 0, 1.8), (.8, .4, .06), "wood_dark", bevel=.008)
    it.box((0, 0, .1), (.8, .4, .2), "wood_dark", bevel=.008)
    it.box((0, .02, 1.0), (.76, .34, 1.5), "glass", bevel=0)
    for i, m in enumerate(("butter", "lavender", "sky")):
        z = .45 + i * .45
        it.box((0, 0, z), (.74, .32, .015), "white", bevel=0, outline=False)
        it.cyl((-.15 + i * .1, -.05, z + .1), (.12, .12), .18, m, seg=10, top=.5)


@item("cabinet_key", "Key cabinet", "storage", mount="wall", mount_z=1.4)
def cabinet_key(it):
    it.box((0, -.05, 0), (.35, .1, .45), "grey_light", bevel=.008)
    it.box((0, -.105, 0), (.31, .01, .41), "glass", bevel=0, outline=False)
    for r in range(3):
        for c in range(4):
            it.box((-.11 + c * .075, -.08, .12 - r * .12), (.02, .01, .05), BOOKS[(r + c) % 7], bevel=0, outline=False)


@item("magazine_rack", "Magazine rack", "storage")
def magazine_rack(it):
    for i in range(3):
        z = .25 + i * .3
        it.box((0, -.05 + i * .07, z), (.6, .03, .3), "wood_light", bevel=.006, rot=(-15, 0, 0))
        it.box((0, -.08 + i * .07, z + .07), (.5, .02, .32), BOOKS[i * 2], bevel=0, rot=(-15, 0, 0))
    for sx in (-1, 1):
        it.box((sx * .3, .05, .5), (.03, .35, 1.0), "wood_mid", bevel=.006)


@item("shoe_rack", "Shoe rack", "storage")
def shoe_rack(it):
    for i in range(3):
        z = .05 + i * .18
        it.box((0, 0, z), (.9, .3, .02), "wood_light", bevel=.004)
        for k in range(3):
            it.box((-.3 + k * .3, -.02, z + .05), (.1, .22, .08), BOOKS[(i + k) % 7], bevel=.03)
    for sx in (-1, 1):
        it.box((sx * .45, 0, .25), (.03, .3, .5), "wood_mid", bevel=0)


@item("basket_set", "Woven basket set", "storage")
def basket_set(it):
    for i, (x, s, h) in enumerate(((-.2, .35, .3), (.15, .3, .25), (.0, .22, .4))):
        it.cyl((x, (-.1 if i == 2 else .05), h / 2), (s, s), h, "cork", seg=14, top=1.1)
        it.cyl((x, (-.1 if i == 2 else .05), h - .02), (s * 1.1, s * 1.1), .03, "wood_mid", seg=14)


@item("storage_bins_stack", "Stacked storage bins", "storage")
def storage_bins_stack(it):
    for i, m in enumerate(("sky", "mint", "butter", "blush")):
        it.box((0, 0, .14 + i * .27), (.45, .35, .25), m, bevel=.015)
        it.box((0, -.18, .2 + i * .27), (.15, .02, .04), "white", bevel=0, outline=False)


@item("cabinet_tool", "Tool cabinet", "storage")
def cabinet_tool(it):
    it.box((0, 0, .5), (.7, .45, .9), "coral", bevel=.01)
    for i in range(5):
        z = .15 + i * .17
        it.box((0, -.23, z), (.66, .02, .15), "peach", bevel=.004)
        it.box((0, -.245, z + .03), (.3, .02, .02), "metal", bevel=0)
    for sx in (-1, 1):
        for sy in (-1, 1):
            it.cyl((sx * .28, sy * .18, .03), (.05, .05), .04, "black", seg=8, rot=(90, 0, 0))


@item("cabinet_flat_file", "Flat file cabinet", "storage")
def cabinet_flat_file(it):
    it.box((0, 0, .45), (1.1, .8, .8), "grey_light", bevel=.008)
    for i in range(6):
        z = .12 + i * .12
        it.box((0, -.405, z), (1.06, .015, .1), "white", bevel=.004)
        it.box((0, -.42, z), (.3, .015, .015), "charcoal", bevel=0)
    legs4(it, 1.1, .8, .05, "charcoal", dia=.04, inset=.06)


@item("locker_tall_wood", "Wooden locker column", "storage")
def locker_tall_wood(it):
    it.box((0, 0, .95), (.45, .5, 1.9), "wood_light", bevel=.01)
    for i in range(4):
        z = .3 + i * .45
        it.box((0, -.255, z), (.41, .02, .42), "wood_mid", bevel=.006)
        it.cyl((.14, -.27, z), (.04, .04), .02, "metal", seg=8, rot=(90, 0, 0))
        it.box((-.08, -.268, z + .12), (.1, .006, .05), "paper", bevel=0, outline=False)


@item("cart_book", "Book cart", "storage")
def cart_book(it):
    for i in range(2):
        z = .3 + i * .4
        it.box((0, 0, z), (.8, .35, .025), "wood_mid", bevel=.004, rot=(0, 0, 0))
        _book_row(it, -.35, .35, z + .013, .2, BOOKS, k=i * 3)
    for sx in (-1, 1):
        it.box((sx * .41, 0, .55), (.025, .35, .9), "wood_dark", bevel=0)
        for sy in (-1, 1):
            it.cyl((sx * .35, sy * .14, .04), (.07, .07), .03, "black", seg=8, rot=(0, 90, 0))


# =========================================================================== MEETING (more)
@item("flip_chart", "Flip chart", "meeting")
def flip_chart(it):
    for deg in (90, 210, 330):
        it.stick(_polar(.3, deg, 0), (0, 0, 1.2), .03, "metal", seg=5)
    it.box((0, -.08, 1.25), (.7, .03, .9), "white", bevel=.006)
    it.box((0, -.1, 1.25), (.66, .01, .86), "paper", bevel=0)
    it.box((0, -.11, 1.45), (.4, .005, .04), "coral", bevel=0, outline=False)
    it.box((-.05, -.11, 1.3), (.5, .005, .03), "blue", bevel=0, outline=False)
    it.box((0, -.08, 1.72), (.72, .05, .04), "charcoal", bevel=.006)


@item("whiteboard_glass", "Glass whiteboard", "meeting", mount="wall", mount_z=.9)
def whiteboard_glass(it):
    it.box((0, -.02, .6), (1.6, .02, 1.0), "glass", bevel=.004)
    for sx in (-1, 1):
        for sz in (0, 1):
            it.cyl((sx * .75, -.035, .15 + sz * .9), (.04, .04), .03, "metal", seg=8, rot=(90, 0, 0))
    it.box((-.3, -.035, .8), (.5, .004, .03), "coral", bevel=0, outline=False)
    it.box((.2, -.035, .5), (.6, .004, .03), "blue", bevel=0, outline=False)


@item("whiteboard_mobile", "Mobile whiteboard", "meeting")
def whiteboard_mobile(it):
    it.box((0, 0, 1.25), (1.4, .04, .9), "white", bevel=.01)
    it.box((0, -.025, 1.25), (1.34, .01, .84), "paper", bevel=0, outline=False)
    it.box((0, -.06, .79), (1.0, .08, .02), "grey", bevel=0)
    for sx in (-1, 1):
        it.box((sx * .72, 0, .9), (.04, .04, 1.6), "grey", bevel=0)
        it.box((sx * .72, 0, .06), (.06, .5, .04), "grey", bevel=0)
        for sy in (-1, 1):
            it.cyl((sx * .72, sy * .22, .03), (.05, .05), .03, "black", seg=8, rot=(0, 90, 0))
    it.box((-.3, -.03, 1.4), (.45, .004, .1), "sky", bevel=0, outline=False)


@item("podium", "Podium / lectern", "meeting")
def podium(it):
    it.box((0, 0, .55), (.6, .45, 1.0), "wood_mid", bevel=.015)
    it.box((0, .02, 1.12), (.66, .5, .05), "wood_dark", bevel=.01, rot=(-15, 0, 0))
    it.box((0, -.23, .7), (.3, .01, .15), "butter", bevel=0, outline=False)
    it.stick((.18, .1, 1.15), (.12, -.12, 1.35), .015, "black", seg=5)
    it.ball((.12, -.13, 1.36), (.04, .04, .05), "black", seg=8)


@item("screen_stand", "Presentation screen stand", "meeting")
def screen_stand(it):
    it.box((0, 0, .02), (.7, .5, .04), "charcoal", bevel=.008)
    it.box((0, 0, .7), (.1, .06, 1.3), "charcoal", bevel=.008)
    it.box((0, -.05, 1.35), (1.4, .06, .8), "black", bevel=.01)
    it.box((0, -.085, 1.35), (1.32, .01, .72), "screen", bevel=0, outline=False)
    it.box((-.3, -.09, 1.45), (.4, .005, .25), "white", bevel=0, outline=False)


@item("video_conf_bar", "Video conference bar", "meeting")
def video_conf_bar(it):
    it.box((0, 0, .04), (.8, .1, .08), "charcoal", bevel=.02)
    it.cyl((0, -.05, .04), (.05, .05), .01, "black", seg=10, rot=(90, 0, 0), outline=False)
    for sx in (-1, 1):
        it.box((sx * .25, -.052, .04), (.2, .004, .05), "grey", bevel=0, outline=False)


@item("table_mic_conf", "Conference mic", "meeting")
def table_mic_conf(it):
    it.cyl((0, 0, .015), (.14, .14), .03, "black", seg=12, bevel=.008)
    it.stick((0, 0, .03), (0, -.08, .3), .012, "charcoal", seg=5)
    it.ball((0, -.09, .31), (.03, .03, .04), "black", seg=6)
    it.ball((0, -.05, .032), (.02, .02, .01), "leaf", seg=6, outline=False)


@item("phone_booth", "Focus phone booth", "meeting")
def phone_booth(it):
    it.box((0, 0, 1.1), (1.0, 1.0, .06), "white", bevel=.01)
    it.box((0, 0, 2.15), (1.0, 1.0, .1), "white", bevel=.01)
    it.box((0, .48, 1.1), (1.0, .04, 2.1), "sage", bevel=.01)
    for sx in (-1, 1):
        it.box((sx * .48, 0, 1.1), (.04, 1.0, 2.1), "sage", bevel=.01)
    it.box((0, -.48, 1.1), (.92, .02, 2.0), "glass", bevel=0)
    it.box((0, .2, .55), (.9, .35, .04), "wood_light", bevel=.006)
    it.box((0, .3, .95), (.9, .2, .04), "wood_light", bevel=.006)
    it.box((.38, -.5, 1.1), (.03, .03, .35), "metal", bevel=0)


@item("acoustic_booth_duo", "Meeting pod (2 person)", "meeting")
def acoustic_booth_duo(it):
    it.box((0, 0, .03), (2.0, 1.4, .06), "charcoal", bevel=.01)
    it.box((0, 0, 2.2), (2.0, 1.4, .1), "white", bevel=.01)
    it.box((0, .68, 1.12), (2.0, .04, 2.1), "lavender", bevel=.01)
    for sx in (-1, 1):
        it.box((sx * .98, 0, 1.12), (.04, 1.4, 2.1), "lavender", bevel=.01)
        cushion(it, (sx * .65, .1, .45), (.5, .9, .12), "blue")
    it.box((0, -.68, 1.12), (1.92, .02, 2.0), "glass", bevel=0)
    top_slab(it, .6, .8, .75, "wood_light", t=.03)
    it.cyl((0, .1, .36), (.08, .08), .72, "charcoal", seg=8)


@item("table_huddle", "Huddle table", "meeting")
def table_huddle(it):
    pedestal(it, .72, .5, "white")
    it.cyl((0, 0, .735), (1.2, .9), .04, "sage", seg=24, bevel=.01)
    it.box((0, 0, .762), (.18, .1, .015), "black", bevel=.003)


@item("table_meeting_standing", "Standing meeting table", "meeting")
def table_meeting_standing(it):
    top_slab(it, 1.8, .8, 1.05, "wood_light", t=.04)
    for sx in (-1, 1):
        it.box((sx * .7, 0, .52), (.08, .6, 1.0), "white", bevel=.01)
    it.box((0, 0, .15), (1.4, .04, .04), "metal", bevel=0)


@item("easel_sticky", "Sticky-note easel", "meeting")
def easel_sticky(it):
    for sx in (-1, 1):
        it.stick((sx * .35, -.2, 0), (sx * .3, 0, 1.7), .03, "wood_mid", seg=5)
    it.stick((0, .35, 0), (0, 0, 1.6), .03, "wood_mid", seg=5)
    it.box((0, -.04, 1.15), (.8, .03, .8), "cork", bevel=.006, rot=(-5, 0, 0))
    for r in range(3):
        for c in range(4):
            it.box((-.27 + c * .18, -.07, .9 + r * .2), (.12, .006, .12), ("butter", "blush", "mint", "sky")[(r + c) % 4],
                   bevel=0, outline=False, rot=(-5, 0, (r * c) % 3 * 4 - 4))
