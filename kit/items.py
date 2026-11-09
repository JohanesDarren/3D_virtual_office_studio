"""Furniture items (v2, calm pastel). Each builder fills an Item.

Floor/table items: pivot bottom center, floor (or table top) at z=0, front faces -Y.
Wall items: back face on y=0 (wall at +Y), item extends toward -Y, z=0 = bottom edge;
the app hangs them at ``mount_z`` meters above the floor.
Real-world sizes, softened edges, chunky but calm proportions.
"""
import math
from lib import Item  # noqa: F401  (type of `it`)

REGISTRY = {}   # id -> dict(label, category, mount, mount_z, fn)


def item(item_id, label, category, mount="floor", mount_z=0.0):
    def deco(fn):
        assert item_id not in REGISTRY, item_id
        REGISTRY[item_id] = dict(label=label, category=category, mount=mount, mount_z=mount_z, fn=fn)
        return fn
    return deco


def _polar(r, deg, z=0.0):
    a = math.radians(deg)
    return (r * math.cos(a), r * math.sin(a), z)


def _star_base(it, r=.3, z=.07, m="charcoal", wheel="black"):
    """5-arm caster base for swivel chairs."""
    for i in range(5):
        deg = 90 + i * 72
        it.box(_polar(r / 2, deg, z), (r, .05, .035), m, bevel=0, rot=(0, 0, deg))
        it.cyl(_polar(r, deg, .035), (.06, .06), .04, wheel, seg=6, rot=(90, 0, deg))
    it.cyl((0, 0, z), (.1, .1), .05, m, seg=12)


def _book_row(it, x0, x1, z, depth, cols, k=0, lean_last=False):
    """Fill a shelf from x0 to x1 with books of varied height/width standing at z."""
    x = x0
    i = 0
    while True:
        bw = .045 + ((k + i) % 3) * .012
        bh = .26 - ((k + i) % 4) * .03
        if x + bw > x1:
            break
        it.box((x + bw / 2, 0, z + bh / 2), (bw, depth, bh), cols[(k + i) % len(cols)], bevel=0)
        x += bw + .006
        i += 1
    if lean_last and x + .1 < x1:
        it.box((x + .07, 0, z + .115), (.045, depth, .24), cols[(k + i) % len(cols)], bevel=0, rot=(0, 22, 0))
    return i


BOOKS = ["coral", "blue", "butter", "sage", "lavender", "peach", "sky"]


# =========================================================================== WORK
@item("desk", "Work desk", "work")
def desk(it):
    w, d, h = 1.4, .7, .75
    it.box((0, 0, h - .03), (w, d, .06), "wood_light", bevel=.02)
    it.box((0, -d / 2 + .004, h - .03), (w - .06, .01, .02), "white", bevel=0, outline=False)   # edge band
    it.cyl((-.5, .22, h + .001), (.07, .07), .004, "charcoal", seg=12, outline=False)          # cable grommet
    for sx in (-1, 1):   # slim metal frame: two legs + foot rail per side
        for sy in (-1, 1):
            it.box((sx * (w / 2 - .06), sy * (d / 2 - .06), (h - .05) / 2), (.04, .04, h - .05), "grey", bevel=.012)
        it.box((sx * (w / 2 - .06), 0, .05), (.04, d - .12, .03), "grey", bevel=.01)
    it.box((0, d / 2 - .06, h - .07), (w - .12, .04, .04), "grey", bevel=.01)
    # hanging drawer pedestal (right)
    it.box((.4, -.02, .5), (.42, .58, .4), "offwhite", bevel=.02)
    for z in (.6, .4):
        it.box((.4, -.31, z), (.38, .02, .17), "sage", bevel=.015)
        it.ball((.4, -.325, z + .03), (.035, .02, .035), "wood_dark", seg=8)


@item("standing_desk", "Standing desk", "work")
def standing_desk(it):
    w, d, h = 1.4, .7, 1.05
    it.box((0, 0, h - .025), (w, d, .05), "wood_light", bevel=.02)
    for sx in (-1, 1):   # telescoping T-legs
        it.box((sx * .55, 0, .02), (.08, d - .05, .04), "charcoal", bevel=.015)
        it.box((sx * .55, 0, .3), (.09, .07, .52), "charcoal", bevel=.015)
        it.box((sx * .55, 0, .77), (.07, .055, .48), "grey", bevel=.012)
    it.box((0, 0, h - .08), (1.0, .07, .06), "charcoal", bevel=.012)    # crossbar
    it.box((.5, -d / 2 + .02, h - .065), (.12, .04, .025), "black", bevel=.008)   # control pad
    it.box((.47, -d / 2 + .002, h - .062), (.02, .01, .012), "sky", bevel=0, outline=False)


@item("office_chair", "Office chair", "work")
def office_chair(it):
    _star_base(it)
    it.cyl((0, 0, .17), (.08, .08), .12, "charcoal", seg=10, top=.8)        # lift cover
    it.cyl((0, 0, .31), (.045, .045), .18, "metal", seg=10)
    it.box((0, 0, .41), (.3, .3, .03), "black", bevel=.01)
    it.box((0, -.01, .47), (.5, .48, .09), "mint", bevel=.04)              # seat
    it.box((0, -.255, .47), (.42, .004, .012), "sage", bevel=0, outline=False)   # front stitch
    it.box((0, .236, .9), (.38, .004, .36), "sage", bevel=0, rot=(-10, 0, 0), outline=False)  # back panel
    it.box((0, .28, .6), (.07, .04, .28), "black", bevel=.012, rot=(-6, 0, 0))   # spine
    it.box((0, .27, .86), (.46, .08, .48), "mint", bevel=.04, rot=(-10, 0, 0))   # back
    for sx in (-1, 1):
        it.box((sx * .27, .03, .56), (.04, .04, .14), "black", bevel=.01)
        it.box((sx * .27, 0, .645), (.07, .28, .035), "black", bevel=.015)


@item("partition_panel", "Acoustic partition", "work")
def partition_panel(it):
    w, h = 1.2, 1.2
    it.box((0, 0, h / 2 + .08), (w, .05, h), "sky", bevel=.025)
    it.box((0, 0, h + .09), (w + .02, .06, .03), "white", bevel=.012)     # top cap
    for sx in (-1, 1):
        it.box((sx * (w / 2 + .005), 0, h / 2 + .08), (.03, .06, h + .02), "white", bevel=.01)
        it.box((sx * (w / 2 - .1), 0, .02), (.08, .36, .04), "charcoal", bevel=.012)
        it.box((sx * (w / 2 - .1), 0, .06), (.04, .04, .06), "charcoal", bevel=.01)
    for x, z, c in ((-.3, .95, "butter"), (-.15, .9, "blush"), (.2, .98, "paper")):   # pinned notes
        it.box((x, -.03, z), (.12, .01, .12), c, bevel=0, rot=(0, (x * 30) % 7 - 3, 0), outline=False)


@item("bookshelf", "Bookshelf", "work")
def bookshelf(it):
    w, d, h = .9, .32, 1.8
    for sx in (-1, 1):
        it.box((sx * (w / 2 - .02), 0, h / 2), (.04, d, h), "wood_mid", bevel=.012)
    it.box((0, d / 2 - .01, h / 2), (w - .04, .02, h - .02), "wood_dark", bevel=0)
    it.box((0, -.01, .04), (w - .04, d - .02, .08), "wood_mid", bevel=.01)        # plinth
    shelves = [.08, .5, .92, 1.34, h - .02]
    for z in shelves[1:]:
        it.box((0, 0, z), (w - .04, d, .035), "wood_mid", bevel=.008)
    _book_row(it, -w / 2 + .05, .05, .1, d - .12, BOOKS, k=0, lean_last=True)
    _book_row(it, -w / 2 + .05, -.08, .52, d - .12, BOOKS, k=3)
    _book_row(it, -.05, w / 2 - .05, .94, d - .12, BOOKS, k=5, lean_last=True)
    it.box((.24, -.02, .58), (.24, .22, .16), "white", bevel=.03)                   # storage box
    it.box((.24, -.135, .6), (.08, .01, .03), "charcoal", bevel=0, outline=False)
    it.cyl((-.22, -.02, 1.43), (.13, .13), .14, "pot", seg=12)                      # small plant
    it.ball((-.22, -.02, 1.56), (.2, .2, .15), "leaf", seg=10)
    it.cyl((.2, -.02, 1.46), (.1, .1), .2, "lavender", seg=12, top=.6)            # vase
    it.box((.24, -.02, .3), (.2, .2, .2), "butter", bevel=.03)                     # basket


@item("filing_cabinet", "Filing cabinet", "work")
def filing_cabinet(it):
    w, d, h = .45, .55, 1.0
    it.box((0, 0, h / 2 + .02), (w, d, h - .04), "grey_light", bevel=.02)
    it.box((0, 0, .02), (w - .04, d - .04, .04), "charcoal", bevel=.01)
    for i in range(3):
        z = .19 + i * .31
        it.box((0, -d / 2, z), (w - .05, .025, .27), "sky", bevel=.015)
        it.cyl((0, -d / 2 - .03, z + .06), (.02, .02), .16, "white", seg=8, rot=(0, 90, 0))
        it.box((0, -d / 2 - .015, z - .04), (.1, .01, .045), "paper", bevel=0, outline=False)


# =========================================================================== TECH (table items)
@item("monitor", "Monitor", "tech", mount="table")
def monitor(it):
    it.cyl((0, 0, .01), (.24, .17), .02, "charcoal", seg=16)
    it.box((0, .03, .15), (.05, .03, .26), "charcoal", bevel=.012)
    it.box((0, .045, .33), (.28, .04, .18), "charcoal", bevel=.02)                 # back bump
    it.box((0, 0, .33), (.62, .03, .37), "charcoal", bevel=.015)
    it.box((0, -.016, .335), (.58, .01, .32), "screen", bevel=.004, outline=False)
    it.box((-.12, -.022, .4), (.18, .004, .03), "white", bevel=0, outline=False)    # UI hints
    it.box((-.12, -.022, .35), (.26, .004, .02), "blue", bevel=0, outline=False)
    it.ball((0, -.018, .508), (.025, .012, .018), "black", seg=8, outline=False)       # webcam
    it.ball((.26, -.018, .158), (.012, .006, .012), "mint", seg=6, outline=False)      # power LED


@item("laptop", "Laptop", "tech", mount="table")
def laptop(it):
    it.box((0, 0, .01), (.34, .24, .02), "grey_light", bevel=.01)
    it.box((0, -.025, .021), (.28, .1, .003), "grey", bevel=0, outline=False)
    it.box((0, -.095, .021), (.1, .04, .002), "grey", bevel=0, outline=False)      # trackpad
    it.box((0, .12, .125), (.34, .015, .22), "grey_light", bevel=.008, rot=(-14, 0, 0))
    it.box((0, .11, .128), (.3, .006, .18), "screen", bevel=0, rot=(-14, 0, 0), outline=False)
    it.ball((0, .145, .13), (.05, .006, .05), "white", seg=10, rot=(-14, 0, 0), outline=False)   # lid logo
    it.box((-.11, -.11, .021), (.04, .002, .004), "mint", bevel=0, outline=False)              # status light


@item("desk_lamp", "Desk lamp", "tech", mount="table")
def desk_lamp(it):
    it.cyl((0, .04, .015), (.16, .16), .03, "butter", seg=16)
    it.ball((0, .04, .04), (.04, .04, .04), "white", seg=8)
    it.stick((0, .04, .04), (0, -.02, .32), .025, "butter")
    it.ball((0, -.02, .32), (.04, .04, .04), "white", seg=8)
    it.stick((0, -.02, .32), (0, -.18, .36), .025, "butter")
    # shade: narrow end up-back at the joint, opening faces down-front
    it.cyl((0, -.21, .31), (.17, .17), .11, "butter", seg=16, top=.45, rot=(-30, 0, 0))
    it.cyl((0, -.237, .263), (.13, .13), .01, "lamp_glow", seg=16, rot=(-30, 0, 0), outline=False)


@item("plant_small", "Desk plant", "tech", mount="table")
def plant_small(it):
    it.cyl((0, 0, .06), (.12, .12), .12, "white", seg=14, top=1.1)
    it.cyl((0, 0, .12), (.12, .12), .005, "soil", seg=14, outline=False)
    for i in range(5):
        deg = i * 72 + 15
        it.ball(_polar(.035, deg, .16), (.1, .05, .02), "leaf" if i % 2 else "leaf_dark", seg=8,
                rot=(0, -35, deg))
    it.ball((0, 0, .2), (.05, .05, .08), "leaf", seg=8)


# =========================================================================== MEETING
@item("meeting_table", "Meeting table", "meeting")
def meeting_table(it):
    w, d, h = 2.4, 1.1, .75
    it.cyl((0, 0, h - .03), (w, d), .06, "wood_mid", seg=40)                  # oval top
    for sx in (-1, 1):
        it.cyl((sx * .6, 0, .37), (.14, .14), .62, "grey", seg=14)
        it.box((sx * .6, 0, .025), (.14, .7, .05), "grey", bevel=.02)
        it.cyl((sx * .6, 0, .69), (.3, .3), .04, "grey", seg=14)
    it.box((0, 0, h + .002), (.3, .14, .01), "charcoal", bevel=.004, outline=False)   # power hatch


@item("meeting_chair", "Meeting chair", "meeting")
def meeting_chair(it):
    for sx in (-1, 1):
        for sy in (-1, 1):
            it.stick((sx * .2, sy * .2, .012), (sx * .17, sy * .17, .43), .03, "metal")
    it.box((0, 0, .45), (.46, .44, .04), "metal", bevel=.012)
    it.box((0, -.01, .5), (.46, .44, .07), "lavender", bevel=.03)
    it.box((0, -.235, .5), (.38, .004, .01), "white", bevel=0, outline=False)   # piping
    for sx in (-1, 1):
        it.stick((sx * .17, .19, .45), (sx * .19, .25, .82), .03, "metal")
    it.box((0, .25, .74), (.46, .06, .26), "lavender", bevel=.03, rot=(-10, 0, 0))


@item("tv_stand", "Presentation TV", "meeting")
def tv_stand(it):
    it.box((0, 0, .1), (.9, .55, .05), "charcoal", bevel=.02)
    for sx in (-1, 1):
        for sy in (-1, 1):
            it.cyl((sx * .4, sy * .22, .04), (.07, .07), .05, "black", seg=8, rot=(90, 0, 0))
        it.box((sx * .2, .05, .85), (.06, .06, 1.45), "grey", bevel=.015)
    it.box((0, .02, 1.25), (1.3, .06, .76), "black", bevel=.02)
    it.box((0, -.012, 1.25), (1.24, .01, .7), "screen", bevel=.004, outline=False)
    it.box((-.3, -.018, 1.38), (.4, .004, .05), "white", bevel=0, outline=False)   # slide hints
    for i, c in enumerate(("coral", "butter", "mint")):
        it.box((-.35 + i * .15, -.018, 1.12 + i * .03), (.1, .004, .1 + i * .06), c, bevel=0, outline=False)
    it.box((0, .0, .6), (.36, .3, .03), "grey", bevel=.01)                    # shelf


@item("whiteboard", "Whiteboard", "meeting")
def whiteboard(it):
    for sx in (-1, 1):
        it.box((sx * .7, 0, .93), (.05, .05, 1.76), "grey", bevel=.015)
        it.box((sx * .7, 0, .06), (.06, .5, .04), "grey", bevel=.015)
        for sy in (-1, 1):
            it.cyl((sx * .7, sy * .22, .035), (.06, .06), .04, "charcoal", seg=8, rot=(0, 90, 0))
    it.box((0, 0, 1.2), (1.36, .04, .9), "white", bevel=.015)
    it.box((0, -.021, 1.2), (1.28, .01, .82), "paper", bevel=.004, outline=False)
    it.box((0, -.04, .74), (1.1, .07, .025), "grey", bevel=.008)
    for i, cm in enumerate(("coral", "blue", "black")):
        it.cyl((-.3 + i * .1, -.04, .76), (.018, .018), .12, cm, seg=6, rot=(0, 90, 0), outline=False)
    for x, z, w, c in ((-.35, 1.45, .4, "blue"), (-.3, 1.33, .3, "blue"), (.25, 1.4, .35, "coral")):
        it.box((x, -.027, z), (w, .004, .02), c, bevel=0, outline=False)
    it.ball((.28, -.027, 1.12), (.22, .004, .22), "butter", seg=12, outline=False)


# =========================================================================== LOUNGE
@item("sofa", "Sofa 2-seat", "lounge")
def sofa(it):
    w, d = 1.7, .85
    for sx in (-1, 1):
        for sy in (-1, 1):
            it.cyl((sx * (w / 2 - .1), sy * (d / 2 - .1), .05), (.05, .05), .1, "wood_dark", seg=8, top=.7)
    it.box((0, 0, .2), (w, d, .2), "sage", bevel=.04)
    for sx in (-1, 1):
        it.box((sx * .37, -.06, .36), (.72, .62, .13), "sage", bevel=.05)
        it.box((sx * .37, -.375, .36), (.6, .004, .012), "mint", bevel=0, outline=False)   # piping
        it.box((sx * .37, .27, .58), (.72, .2, .38), "sage", bevel=.06, rot=(-8, 0, 0))
        for bx in (-.18, .18):   # tufted buttons
            it.ball((sx * .37 + bx, .165, .6), (.03, .015, .03), "mint", seg=8, outline=False)
        it.box((sx * .79, 0, .42), (.16, d, .44), "sage", bevel=.07)
    it.box((-.5, .1, .56), (.34, .12, .32), "butter", bevel=.06, rot=(-12, 0, 10))
    it.box((.52, .1, .56), (.34, .12, .32), "blush", bevel=.06, rot=(-12, 0, -10))


@item("armchair", "Armchair", "lounge")
def armchair(it):
    w, d = .85, .8
    for sx in (-1, 1):
        for sy in (-1, 1):
            it.stick((sx * .3, sy * .28, .14), (sx * .34, sy * .32, .012), .045, "wood_dark", top=.7)
    it.box((0, 0, .22), (w, d, .16), "peach", bevel=.04)
    it.box((0, -.05, .36), (.55, .6, .13), "peach", bevel=.05)
    it.box((0, .3, .6), (.62, .2, .44), "peach", bevel=.07, rot=(-10, 0, 0))
    for bx in (-.15, 0, .15):   # tufted buttons
        it.ball((bx, .19, .7), (.028, .014, .028), "blush", seg=8, outline=False)
    it.box((0, -.355, .36), (.48, .004, .012), "blush", bevel=0, outline=False)   # piping
    for sx in (-1, 1):
        it.box((sx * .36, 0, .42), (.14, d, .38), "peach", bevel=.06)
    it.box((0, .14, .55), (.3, .1, .26), "lavender", bevel=.05, rot=(-12, 0, 0))


@item("beanbag", "Beanbag", "lounge")
def beanbag(it):
    it.ball((0, 0, .2), (.9, .85, .4), "lavender", seg=16)                       # slumped base
    it.ball((0, .17, .42), (.72, .42, .62), "lavender", seg=14, rot=(-18, 0, 0))   # backrest lump
    it.ball((0, -.32, .26), (.08, .03, .12), "white", seg=8, outline=False)        # tag


@item("coffee_table", "Coffee table", "lounge")
def coffee_table(it):
    it.cyl((0, 0, .4), (.8, .8), .045, "wood_light", seg=28)
    it.cyl((0, 0, .17), (.6, .6), .025, "wood_light", seg=24)                 # lower shelf
    for i in range(3):
        deg = 90 + i * 120
        it.stick(_polar(.3, deg, .38), _polar(.34, deg, .012), .045, "wood_mid", top=.75)
    it.box((.12, .05, .44), (.22, .16, .03), "blue", bevel=.008)               # books on top
    it.box((.13, .05, .465), (.2, .14, .02), "butter", bevel=.006, rot=(0, 0, 8))
    it.cyl((-.16, -.08, .465), (.08, .08), .09, "white", seg=12)              # mug


@item("rug", "Rug", "lounge")
def rug(it):
    it.box((0, 0, .006), (2.0, 1.4, .012), "blush", bevel=.004)
    it.box((0, 0, .0125), (1.8, 1.2, .002), "offwhite", bevel=0, outline=False)
    it.box((0, 0, .0145), (1.6, 1.0, .002), "blush", bevel=0, outline=False)
    for i in range(5):
        it.ball(((i - 2) * .3, 0, .016), (.14, .14, .002), "butter", seg=12, outline=False)
    for sx in (-1, 1):   # tassels on the short ends
        for j in range(9):
            it.box((sx * 1.025, -.6 + j * .15, .004), (.05, .018, .006), "offwhite", bevel=0, outline=False)


@item("floor_lamp", "Floor lamp", "lounge")
def floor_lamp(it):
    it.cyl((0, 0, .02), (.3, .3), .04, "charcoal", seg=18)
    it.stick((0, 0, .04), (0, 0, 1.3), .03, "grey")
    it.cyl((0, 0, 1.43), (.42, .42), .3, "butter", seg=20, top=.7)
    it.cyl((0, 0, 1.285), (.36, .36), .01, "lamp_glow", seg=20, outline=False)
    it.stick((.05, -.03, 1.0), (.05, -.03, .82), .008, "charcoal", seg=4, outline=False)   # pull cord


@item("stool", "Round stool", "lounge")
def stool(it):
    it.cyl((0, 0, .41), (.36, .36), .03, "wood_mid", seg=20)
    it.cyl((0, 0, .45), (.38, .38), .07, "coral", seg=20, top=.9)
    for i in range(3):
        deg = 90 + i * 120
        it.stick(_polar(.1, deg, .4), _polar(.16, deg, .012), .035, "wood_mid")
    it.cyl((0, 0, .18), (.27, .27), .02, "wood_mid", seg=16)


@item("plant_tall", "Floor plant", "lounge")
def plant_tall(it):
    it.cyl((0, 0, .19), (.36, .36), .38, "pot", seg=18, top=1.12)
    it.cyl((0, 0, .16), (.388, .388), .05, "white", seg=18, top=1.02, outline=False)   # painted band
    it.cyl((0, 0, .39), (.43, .43), .04, "pot", seg=18, bevel=.008)
    it.cyl((0, 0, .408), (.37, .37), .01, "soil", seg=18, outline=False)
    leaves = [(0, .22, .95, 35), (72, .26, .78, 50), (144, .2, 1.1, 25), (216, .25, .85, 45),
              (288, .22, 1.0, 30), (36, .12, 1.25, 15), (200, .1, 1.3, 10)]
    for i, (deg, r, z, droop) in enumerate(leaves):
        tip = _polar(r, deg, z)
        it.stick((0, 0, .41), (tip[0] * .8, tip[1] * .8, z - .05), .018, "leaf_dark", seg=5, outline=False)
        it.ball(tip, (.36, .2, .04), "leaf" if i % 2 == 0 else "leaf_dark", seg=10, rot=(0, droop, deg))


# =========================================================================== PANTRY
@item("fridge", "Fridge", "pantry")
def fridge(it):
    w, d, h = .7, .68, 1.8
    it.box((0, 0, h / 2 + .03), (w, d, h - .06), "mint", bevel=.05)
    it.box((0, 0, .03), (w - .06, d - .06, .06), "charcoal", bevel=.01)
    it.box((0, -d / 2, 1.24), (w - .03, .02, .02), "white", bevel=0, outline=False)   # door split
    for z0, z1 in ((1.32, 1.6), (.7, 1.12)):
        it.box((-w / 2 + .09, -d / 2 - .03, (z0 + z1) / 2), (.04, .04, z1 - z0), "white", bevel=.015)
    for x, z, c in ((.12, 1.0, "butter"), (.2, .88, "blush"), (.1, 1.45, "sky")):    # magnets
        it.box((x, -d / 2 - .006, z), (.09, .012, .09), c, bevel=.004, outline=False)
    it.box((.2, -d / 2 - .003, 1.68), (.12, .006, .03), "white", bevel=.002, outline=False)    # badge
    for sx in (-1, 1):   # little feet
        it.cyl((sx * .26, -.26, .02), (.05, .05), .04, "charcoal", seg=8)


@item("kitchen_counter", "Kitchen counter + sink", "pantry")
def kitchen_counter(it):
    w, d, h = 1.8, .6, .9
    it.box((0, .02, .05), (w - .04, d - .1, .1), "charcoal", bevel=.01)            # toe kick
    it.box((0, 0, .48), (w, d, .76), "offwhite", bevel=.02)
    for i in range(3):
        x = -w / 3 + i * w / 3
        it.box((x, -d / 2, .48), (w / 3 - .03, .025, .7), "sage", bevel=.015)
        it.box((x + (.2 if i < 2 else -.2), -d / 2 - .025, .7), (.02, .02, .12), "white", bevel=.006)
    it.box((0, 0, h - .02), (w + .04, d + .04, .04), "wood_light", bevel=.012)       # worktop
    it.box((-.35, 0, h + .001), (.5, .38, .006), "grey_light", bevel=0, outline=False)   # sink
    it.box((-.35, 0, h + .004), (.44, .32, .004), "grey", bevel=0, outline=False)
    it.stick((-.35, .22, h), (-.35, .22, h + .3), .03, "metal")                   # faucet
    it.stick((-.35, .22, h + .3), (-.35, .07, h + .3), .025, "metal")
    it.stick((-.35, .07, h + .3), (-.35, .07, h + .24), .025, "metal")
    it.cyl((.45, .05, h + .07), (.12, .12), .14, "coral", seg=14)                 # kettle
    it.box((.45, -.03, h + .12), (.02, .05, .04), "coral", bevel=.006)
    it.box((.7, .1, h + .1), (.18, .12, .2), "white", bevel=.02)                 # jar
    for i in range(9):   # tiled backsplash
        for j in range(2):
            it.box((-w / 2 + .1 + i * .2, d / 2 - .01, h + .07 + j * .12), (.19, .02, .11),
                   "sky" if (i + j) % 2 else "white", bevel=0)


@item("microwave", "Microwave", "pantry", mount="table")
def microwave(it):
    it.box((0, 0, .155), (.5, .36, .29), "white", bevel=.03)
    it.box((-.06, -.18, .155), (.33, .02, .22), "charcoal", bevel=.015)
    it.box((-.06, -.192, .155), (.27, .006, .16), "glass", bevel=0, outline=False)
    it.box((.09, -.2, .155), (.02, .025, .14), "grey_light", bevel=.006)          # door handle
    it.box((.17, -.19, .265), (.08, .004, .025), "mint", bevel=0, outline=False)     # display
    it.box((.17, -.182, .155), (.1, .01, .22), "grey_light", bevel=.008)
    for i in range(3):
        it.cyl((.17, -.19, .22 - i * .06), (.035, .035), .012, "peach" if i else "coral", seg=10, rot=(90, 0, 0))
    for sx in (-1, 1):
        it.box((sx * .2, 0, .005), (.04, .3, .01), "charcoal", bevel=0)


@item("coffee_machine", "Coffee machine", "pantry", mount="table")
def coffee_machine(it):
    it.box((0, 0, .015), (.28, .32, .03), "charcoal", bevel=.01)
    it.box((0, -.06, .035), (.2, .14, .015), "grey", bevel=.005)                 # drip tray
    it.box((0, .07, .22), (.28, .18, .44), "peach", bevel=.035)
    it.box((0, -.04, .4), (.28, .16, .09), "peach", bevel=.03)
    it.box((.09, .1, .5), (.08, .1, .1), "glass", bevel=.02)                      # water tank
    it.cyl((0, -.07, .33), (.045, .045), .05, "charcoal", seg=10)
    it.cyl((0, -.08, .09), (.08, .08), .1, "white", seg=14)                      # cup
    it.box((.045, -.08, .09), (.02, .03, .05), "white", bevel=.006)
    it.ball((-.08, -.12, .41), (.035, .02, .035), "mint", seg=8)
    it.ball((-.03, -.12, .41), (.035, .02, .035), "butter", seg=8)


@item("water_dispenser", "Water dispenser", "pantry")
def water_dispenser(it):
    it.box((0, 0, .5), (.34, .34, 1.0), "white", bevel=.035)
    it.box((0, -.17, .62), (.22, .02, .16), "grey_light", bevel=.01)
    for sx, cm in ((-1, "blue"), (1, "coral")):
        it.box((sx * .05, -.19, .63), (.045, .035, .05), cm, bevel=.01)
    it.box((0, -.15, .4), (.24, .1, .025), "grey", bevel=.008)                    # drip tray
    it.cyl((0, 0, 1.2), (.28, .28), .38, "water", seg=18, top=.9)
    it.cyl((0, 0, 1.06), (.28, .28), .04, "water", seg=18, top=1.05)
    it.cyl((0, 0, 1.42), (.12, .12), .06, "blue", seg=12)
    it.ball((0, -.172, .85), (.09, .004, .09), "sky", seg=12, outline=False)        # droplet logo
    it.ball((0, -.174, .835), (.04, .004, .05), "white", seg=8, outline=False)


@item("trash_bin", "Trash bin", "pantry")
def trash_bin(it):
    it.cyl((0, 0, .21), (.3, .3), .38, "sage", seg=16, top=1.12)
    it.cyl((0, 0, .42), (.36, .36), .05, "white", seg=16, top=.92)               # lid
    it.box((0, 0, .45), (.14, .04, .02), "charcoal", bevel=.006)
    it.box((0, -.18, .03), (.12, .08, .025), "charcoal", bevel=.008)             # pedal
    it.cyl((0, 0, .015), (.32, .32), .03, "charcoal", seg=16)
    it.box((0, -.163, .22), (.1, .004, .1), "white", bevel=0, rot=(-4, 0, 0), outline=False)   # recycle tag
    it.box((0, -.166, .22), (.05, .004, .05), "mint", bevel=0, rot=(-4, 0, 45), outline=False)


# =========================================================================== WALL DECOR
@item("wall_clock", "Wall clock", "wall", mount="wall", mount_z=2.0)
def wall_clock(it):
    r = .36
    it.cyl((0, -.025, r / 2), (r, r), .05, "wood_mid", seg=24, rot=(90, 0, 0))
    it.cyl((0, -.051, r / 2), (r - .04, r - .04), .004, "white", seg=24, rot=(90, 0, 0), outline=False)
    for i in range(12):
        deg = i * 30
        x, _, z = _polar(.13, deg)
        big = i % 3 == 0
        it.box((x, -.054, r / 2 + z), (.012 if big else .007, .002, .03 if big else .015), "charcoal",
               bevel=0, rot=(0, -deg + 90, 0), outline=False)
    it.box((.035, -.057, r / 2 + .02), (.09, .003, .012), "charcoal", bevel=0, rot=(0, -30, 0), outline=False)
    it.box((0, -.058, r / 2 + .055), (.008, .003, .11), "charcoal", bevel=0, outline=False)
    it.cyl((0, -.06, r / 2), (.02, .02), .006, "coral", seg=8, rot=(90, 0, 0), outline=False)


@item("picture_frame", "Picture frame", "wall", mount="wall", mount_z=1.4)
def picture_frame(it):
    w, h = .5, .4
    it.box((0, -.015, h / 2), (w, .03, h), "wood_light", bevel=.008)
    it.box((0, -.031, h / 2), (w - .07, .002, h - .07), "sky", bevel=0, outline=False)
    it.ball((.1, -.033, h / 2 + .07), (.07, .002, .07), "butter", seg=12, outline=False)
    it.ball((-.06, -.034, .085), (.36, .002, .16), "sage", seg=14, outline=False)
    it.ball((.1, -.035, .07), (.3, .002, .1), "leaf", seg=14, outline=False)


@item("poster", "Poster", "wall", mount="wall", mount_z=1.3)
def poster(it):
    w, h = .5, .7
    it.box((0, -.005, h / 2), (w, .01, h), "lavender", bevel=.003)
    it.ball((0, -.012, .45), (.28, .002, .28), "peach", seg=16, outline=False)
    it.ball((0, -.013, .45), (.16, .002, .16), "butter", seg=16, outline=False)
    for i, ww in enumerate((.34, .26, .3)):
        it.box((0, -.012, .2 - i * .05), (ww, .002, .025), "white", bevel=0, outline=False)


@item("wall_shelf", "Wall shelf", "wall", mount="wall", mount_z=1.5)
def wall_shelf(it):
    w, d, b = .8, .22, .12          # b = bracket height; board sits on top, bottom edge of item at z=0
    for sx in (-1, 1):   # brackets
        it.box((sx * .28, -.01, b / 2), (.03, .02, b), "charcoal", bevel=.006)
        it.box((sx * .28, -.07, b - .006), (.03, .12, .012), "charcoal", bevel=.004)
    it.box((0, -d / 2, b + .015), (w, d, .03), "wood_light", bevel=.01)
    for i, c in enumerate(("blue", "coral", "butter")):
        it.box((-.3 + i * .05, -.11, b + .14), (.04, .16, .22 - i * .02), c, bevel=0)
    it.cyl((.05, -.11, b + .1), (.12, .12), .14, "pot", seg=12)
    it.ball((.05, -.11, b + .22), (.18, .18, .14), "leaf", seg=10)
    it.cyl((.26, -.11, b + .075), (.08, .08), .09, "white", seg=12)
    it.box((.305, -.11, b + .075), (.02, .03, .05), "white", bevel=.006)


@item("notice_board", "Notice board", "wall", mount="wall", mount_z=1.2)
def notice_board(it):
    w, h = .9, .6
    it.box((0, -.015, h / 2), (w, .03, h), "wood_mid", bevel=.008)
    it.box((0, -.031, h / 2), (w - .06, .002, h - .06), "cork", bevel=0, outline=False)
    notes = [(-.28, .42, "butter", 4), (-.08, .44, "sky", -5), (.15, .4, "blush", 3), (.32, .44, "paper", -3),
             (-.22, .2, "mint", -4), (.02, .2, "paper", 6), (.26, .18, "lavender", -2)]
    for x, z, c, rr in notes:
        it.box((x, -.034, z), (.14, .002, .14), c, bevel=0, rot=(0, rr, 0), outline=False)
        it.ball((x, -.038, z + .055), (.02, .01, .02), "coral", seg=6, outline=False)
