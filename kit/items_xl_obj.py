"""Kit v8, part 3: objects -- tech, desk gear, pantry, recreation, decor, wall pieces."""
import math

from items import BOOKS, _book_row, _polar, item
from items_xl_furn import cabinet, cushion, doors_front, legs4, pedestal, top_slab

PASTEL = ["coral", "peach", "butter", "sage", "sky", "lavender", "blush", "mint"]


def screen_face(it, c, w, h, rot=(0, 0, 0)):
    it.box(c, (w, .006, h), "screen", bevel=0, outline=False, rot=rot)


def leaf_ball(it, c, s, k=0):
    it.ball(c, s, ("leaf", "leaf_dark")[k % 2], seg=8)


def pot(it, d, h, m="pot", z0=0.0, top=1.15):
    it.cyl((0, 0, z0 + h / 2), (d, d), h, m, seg=14, top=top, bevel=.01)
    it.cyl((0, 0, z0 + h - .01), (d * top * .92, d * top * .92), .01, "soil", seg=14, outline=False)


# =========================================================================== TECH
@item("projector_ceiling", "Ceiling projector", "tech", mount="ceiling", mount_z=2.8)
def projector_ceiling(it):
    it.stick((0, 0, 0), (0, 0, -.4), .04, "grey", seg=6)
    it.box((0, 0, -.48), (.35, .3, .12), "white", bevel=.02)
    it.cyl((0, -.16, -.48), (.08, .08), .04, "black", seg=12, rot=(90, 0, 0))


@item("projector_screen", "Pull-down projector screen", "tech", mount="wall", mount_z=2.4)
def projector_screen(it):
    it.cyl((0, -.06, 0), (.1, .1), 2.2, "white", seg=10, rot=(0, 90, 0))
    it.box((0, -.07, -.7), (2.0, .01, 1.3), "offwhite", bevel=0)
    it.box((0, -.07, -1.37), (2.0, .03, .03), "black", bevel=0)


@item("tv_wall_large", "Wall TV 75\"", "tech", mount="wall", mount_z=1.0)
def tv_wall_large(it):
    it.box((0, -.04, .48), (1.7, .05, .98), "black", bevel=.01)
    screen_face(it, (0, -.066, .49), 1.64, .92)
    it.box((-.4, -.07, .7), (.5, .004, .2), "sky", bevel=0, outline=False)


@item("tv_cart", "TV on rolling cart", "tech")
def tv_cart(it):
    it.box((0, 0, .04), (.8, .55, .05), "charcoal", bevel=.01)
    for sx in (-1, 1):
        it.box((sx * .25, 0, .8), (.06, .06, 1.5), "charcoal", bevel=0)
        for sy in (-1, 1):
            it.cyl((sx * .33, sy * .22, .03), (.06, .06), .03, "black", seg=8, rot=(0, 90, 0))
    it.box((0, -.04, 1.35), (1.3, .05, .75), "black", bevel=.01)
    screen_face(it, (0, -.066, 1.35), 1.24, .69)
    it.box((0, .0, .7), (.6, .4, .02), "grey", bevel=0)


@item("video_wall", "Video wall 2x2", "tech")
def video_wall(it):
    it.box((0, .1, .5), (.3, .2, 1.0), "charcoal", bevel=.01)
    for r in range(2):
        for c in range(2):
            x, z = -.5 + c * 1.0, 1.25 + r * .58
            it.box((x, 0, z), (.98, .05, .56), "black", bevel=.004)
            screen_face(it, (x, -.027, z), .95, .53)
    it.box((0, .1, .02), (1.0, .6, .04), "charcoal", bevel=.006)


@item("webcam_light", "Webcam with light", "tech")
def webcam_light(it):
    it.cyl((0, 0, .01), (.08, .08), .02, "black", seg=10)
    it.stick((0, 0, .02), (0, 0, .12), .012, "black", seg=4)
    it.box((0, 0, .14), (.12, .05, .045), "black", bevel=.015)
    it.cyl((0, -.026, .14), (.03, .03), .006, "glass", seg=10, rot=(90, 0, 0), outline=False)


@item("docking_station", "Laptop dock", "tech")
def docking_station(it):
    it.box((0, 0, .015), (.25, .08, .03), "grey", bevel=.008)
    it.box((0, -.041, .015), (.18, .004, .01), "black", bevel=0, outline=False)
    it.box((0, .05, .14), (.32, .02, .22), "grey_light", bevel=.006, rot=(-10, 0, 0))


@item("laptop_stand_open", "Laptop on riser", "tech")
def laptop_stand_open(it):
    for sx in (-1, 1):
        it.box((sx * .12, .02, .07), (.02, .2, .14), "metal", bevel=0, rot=(-20, 0, 0))
    it.box((0, .02, .14), (.32, .22, .012), "grey", bevel=.004, rot=(-20, 0, 0))
    it.box((0, .14, .3), (.32, .012, .22), "grey", bevel=.004, rot=(10, 0, 0))
    screen_face(it, (0, .132, .3), .29, .19, rot=(10, 0, 0))


@item("router_wifi", "Wi-Fi router", "tech")
def router_wifi(it):
    it.box((0, 0, .02), (.22, .14, .04), "white", bevel=.012)
    for sx in (-1, 1):
        it.stick((sx * .09, .06, .04), (sx * .1, .07, .2), .012, "white", seg=4)
    for i in range(3):
        it.ball((-.04 + i * .04, -.071, .02), (.012, .004, .012), "leaf", seg=4, outline=False)


@item("smart_speaker", "Smart speaker", "tech")
def smart_speaker(it):
    it.cyl((0, 0, .09), (.12, .12), .18, "grey_light", seg=14, bevel=.03)
    it.cyl((0, 0, .181), (.09, .09), .004, "sky", seg=14, outline=False)


@item("conference_phone", "Conference phone", "tech")
def conference_phone(it):
    for i in range(3):
        it.box(_polar(.08, 90 + i * 120, .02), (.12, .08, .03), "charcoal", bevel=.01, rot=(0, 0, i * 120))
    it.cyl((0, 0, .025), (.1, .1), .04, "black", seg=12)
    it.cyl((0, 0, .046), (.04, .04), .004, "leaf", seg=10, outline=False)


@item("printer_3d", "3D printer", "tech")
def printer_3d(it):
    it.box((0, 0, .04), (.45, .45, .08), "charcoal", bevel=.01)
    for sx in (-1, 1):
        it.box((sx * .2, .2, .3), (.03, .03, .55), "black", bevel=0)
    it.box((0, .2, .56), (.45, .04, .04), "black", bevel=0)
    it.box((0, .1, .4), (.1, .1, .08), "coral", bevel=.01)
    it.box((0, 0, .1), (.32, .32, .01), "grey", bevel=0)
    it.cyl((0, 0, .15), (.1, .1), .1, "mint", seg=8)


@item("scanner_flatbed", "Flatbed scanner", "tech")
def scanner_flatbed(it):
    it.box((0, 0, .04), (.45, .32, .08), "grey_light", bevel=.012)
    it.box((0, .0, .085), (.42, .29, .01), "grey", bevel=.004)
    it.box((-.15, -.161, .05), (.06, .004, .015), "leaf", bevel=0, outline=False)


@item("label_printer", "Label printer", "tech")
def label_printer(it):
    it.box((0, 0, .06), (.12, .18, .12), "white", bevel=.03)
    it.box((0, -.095, .07), (.08, .03, .005), "paper", bevel=0, rot=(-20, 0, 0))


@item("ups_box", "UPS battery", "tech")
def ups_box(it):
    it.box((0, 0, .17), (.16, .4, .34), "black", bevel=.012)
    it.box((0, -.201, .25), (.08, .004, .05), "screen", bevel=0, outline=False)
    it.ball((0, -.205, .16), (.03, .01, .03), "leaf", seg=6, outline=False)


@item("vr_headset_stand", "VR headset on stand", "tech")
def vr_headset_stand(it):
    it.cyl((0, 0, .01), (.14, .14), .02, "white", seg=12)
    it.stick((0, 0, .02), (0, 0, .25), .02, "white", seg=5)
    it.box((0, -.03, .3), (.2, .1, .1), "charcoal", bevel=.03)
    it.cyl((0, .03, .3), (.22, .14), .03, "grey", seg=12, rot=(90, 0, 0))


@item("drone", "Drone", "tech")
def drone(it):
    it.box((0, 0, .06), (.12, .16, .05), "grey_light", bevel=.015)
    for i in range(4):
        x, y, _ = _polar(.14, 45 + i * 90)
        it.stick((0, 0, .06), (x, y, .07), .015, "grey", seg=4)
        it.cyl((x, y, .085), (.12, .12), .005, "charcoal", seg=12, outline=False)
        it.cyl((x, y, .035), (.02, .02), .07, "grey", seg=6)
    it.ball((0, -.09, .045), (.04, .04, .04), "black", seg=6)


@item("game_console", "Game console & TV", "tech")
def game_console(it):
    cabinet(it, 1.4, .45, .5, "wood_light")
    it.box((0, 0, .9), (1.2, .04, .7), "black", bevel=.01)
    screen_face(it, (0, -.023, .9), 1.14, .64)
    it.cyl((0, 0, .53), (.2, .1), .04, "black", seg=8)
    it.box((-.4, 0, .54), (.3, .2, .06), "white", bevel=.02)
    for sx in (-1, 1):
        it.ball((.3 + sx * .07, -.05, .53), (.1, .06, .03), ("coral", "sky")[(sx + 1) // 2], seg=8)


@item("server_cabinet_small", "Wall network cabinet", "tech", mount="wall", mount_z=1.6)
def server_cabinet_small(it):
    it.box((0, -.2, 0), (.6, .4, .45), "charcoal", bevel=.01)
    it.box((0, -.405, 0), (.52, .01, .38), "glass", bevel=0, outline=False)
    for i in range(3):
        it.box((0, -.38, .1 - i * .1), (.5, .02, .06), "black", bevel=0)
        for k in range(6):
            it.ball((-.2 + k * .06, -.39, .1 - i * .1), (.01, .004, .01), ("leaf", "sky")[k % 2], seg=4,
                    outline=False)


# =========================================================================== DESK GEAR (more)
@item("pencil_cup", "Pencil cup", "desk_gear")
def pencil_cup(it):
    it.cyl((0, 0, .05), (.08, .08), .1, "sage", seg=12)
    for i, m in enumerate(("coral", "blue", "butter", "black")):
        x, y, _ = _polar(.018, i * 90)
        it.stick((x, y, .02), (x * 2.5, y * 2.5, .17 + (i % 2) * .02), .01, m, seg=5)


@item("stapler_set", "Stapler & tape", "desk_gear")
def stapler_set(it):
    it.box((-.06, 0, .02), (.05, .16, .04), "coral", bevel=.012)
    it.box((-.06, -.005, .05), (.045, .15, .02), "charcoal", bevel=.006, rot=(-4, 0, 0))
    it.box((.07, 0, .035), (.06, .12, .07), "charcoal", bevel=.015)
    it.cyl((.07, 0, .06), (.05, .05), .04, "glass", seg=10, rot=(0, 90, 0))


@item("desk_organizer", "Desk organizer", "desk_gear")
def desk_organizer(it):
    it.box((0, 0, .04), (.3, .14, .08), "wood_light", bevel=.006)
    it.box((-.08, .02, .1), (.12, .1, .12), "wood_light", bevel=.006)
    for i in range(3):
        it.box((.05 + i * .035, -.01, .1), (.025, .1, .12), "paper", bevel=0, rot=(0, (i - 1) * 5, 0))
    it.stick((-.1, .02, .1), (-.11, .02, .22), .01, "coral", seg=4)


@item("letter_tray_stack", "Letter tray stack", "desk_gear")
def letter_tray_stack(it):
    for i in range(3):
        it.box((0, 0, .02 + i * .07), (.26, .34, .015), "white", bevel=.004)
        it.box((0, .0, .04 + i * .07), (.22, .3, .01), "paper", bevel=0, outline=False)
    for sx in (-1, 1):
        it.box((sx * .13, 0, .11), (.01, .34, .2), "glass", bevel=0)


@item("paper_ream_stack", "Paper ream stack", "desk_gear")
def paper_ream_stack(it):
    for i in range(4):
        it.box((0, 0, .03 + i * .055), (.3, .21, .052), ("paper", "sky", "paper", "butter")[i], bevel=.004,
               rot=(0, 0, (i % 2) * 4 - 2))


@item("notebook_stack", "Notebook stack", "desk_gear")
def notebook_stack(it):
    for i in range(5):
        it.box((0, 0, .008 + i * .017), (.21 - (i % 2) * .02, .28 - (i % 3) * .02, .015), PASTEL[i], bevel=.003,
               rot=(0, 0, (i * 7) % 11 - 5))
    it.stick((-.05, -.1, .1), (.08, .05, .1), .01, "charcoal", seg=4)


@item("sticky_note_pads", "Sticky note pads", "desk_gear")
def sticky_note_pads(it):
    for i, m in enumerate(("butter", "blush", "mint", "sky")):
        it.box(((i % 2) * .09 - .045, (i // 2) * .09 - .045, .012 + (i % 3) * .002), (.076, .076, .024), m,
               bevel=.002, rot=(0, 0, i * 8))


@item("desk_clock_flip", "Flip desk clock", "desk_gear")
def desk_clock_flip(it):
    it.box((0, 0, .06), (.18, .08, .12), "white", bevel=.02)
    for sx in (-1, 1):
        it.box((sx * .042, -.041, .065), (.07, .004, .08), "charcoal", bevel=0, outline=False)


@item("desk_fan", "Desk fan", "desk_gear")
def desk_fan(it):
    it.cyl((0, 0, .015), (.16, .16), .03, "white", seg=12)
    it.stick((0, 0, .03), (0, 0, .2), .025, "white", seg=6)
    it.cyl((0, -.02, .28), (.26, .26), .06, "mint", seg=16, rot=(90, 0, 0))
    for i in range(3):
        it.box(_polar(.06, 90 + i * 120, 0), (.1, .01, .05), "white", bevel=0, outline=False,
               rot=(90, 0, i * 120))
    it.cyl((0, -.06, .28), (.05, .05), .03, "white", seg=10, rot=(90, 0, 0))


@item("water_bottle", "Water bottle", "desk_gear")
def water_bottle(it):
    it.cyl((0, 0, .11), (.075, .075), .22, "sky", seg=12, bevel=.015)
    it.cyl((0, 0, .235), (.055, .055), .03, "charcoal", seg=10)
    it.stick((-.02, 0, .25), (.02, 0, .25), .01, "charcoal", seg=4)


@item("lunch_box", "Lunch box", "desk_gear")
def lunch_box(it):
    it.box((0, 0, .04), (.22, .15, .08), "mint", bevel=.02)
    it.box((0, 0, .085), (.23, .16, .02), "coral", bevel=.008)
    it.box((0, 0, .1), (.24, .02, .02), "white", bevel=0)
    it.box((.1, -.12, .02), (.18, .02, .005), "metal", bevel=0, rot=(0, 0, 20))     # spoon


@item("tissue_box", "Tissue box", "desk_gear")
def tissue_box(it):
    it.box((0, 0, .05), (.22, .12, .1), "blush", bevel=.012)
    it.ball((0, 0, .11), (.06, .03, .05), "paper", seg=6)


@item("photo_frame_desk", "Desk photo frame", "desk_gear")
def photo_frame_desk(it):
    it.box((0, 0, .08), (.14, .02, .17), "wood_mid", bevel=.004, rot=(-10, 0, 0))
    it.box((0, -.011, .08), (.11, .004, .14), "sky", bevel=0, outline=False, rot=(-10, 0, 0))
    it.ball((0, -.014, .065), (.05, .004, .06), "butter", seg=6, outline=False)
    it.stick((0, .01, .08), (0, .06, .0), .01, "wood_mid", seg=4)


@item("desk_mat", "Desk mat", "desk_gear")
def desk_mat(it):
    it.box((0, 0, .002), (.9, .4, .004), "lavender", bevel=0)
    it.box((0, 0, .0045), (.86, .36, .001), "blush", bevel=0, outline=False)


@item("monitor_riser", "Monitor riser", "desk_gear")
def monitor_riser(it):
    it.box((0, 0, .1), (.6, .24, .025), "wood_light", bevel=.006)
    for sx in (-1, 1):
        it.box((sx * .28, 0, .045), (.03, .22, .09), "wood_light", bevel=0)
    it.box((0, 0, .03), (.3, .18, .06), "white", bevel=.01)


@item("footrest", "Footrest", "desk_gear")
def footrest(it):
    it.box((0, 0, .08), (.45, .32, .05), "charcoal", bevel=.01, rot=(-12, 0, 0))
    for sx in (-1, 1):
        it.box((sx * .2, 0, .03), (.03, .3, .06), "grey", bevel=0)


@item("cable_tray", "Cable tray", "desk_gear", mount="wall", mount_z=.6)
def cable_tray(it):
    it.box((0, -.08, 0), (1.0, .16, .015), "grey", bevel=0)
    it.box((0, -.155, .05), (1.0, .01, .1), "grey", bevel=0)
    for i in range(3):
        it.stick((-.45, -.1 + i * .02, .02), (.45, -.1 + i * .02, .02), .015, ("black", "blue", "coral")[i], seg=4)


@item("headphones_desk", "Headphones on desk", "desk_gear")
def headphones_desk(it):
    for i in range(7):
        a0, a1 = math.radians(i * 25.7), math.radians((i + 1) * 25.7)
        it.stick((math.cos(a0) * .09, 0, .03 + math.sin(a0) * .02), (math.cos(a1) * .09, 0, .03 + math.sin(a1) * .02),
                 .02, "charcoal", seg=4)
    for sx in (-1, 1):
        it.cyl((sx * .09, 0, .025), (.08, .08), .045, "coral", seg=12, bevel=.01)


# =========================================================================== PANTRY (more)
@item("dishwasher", "Dishwasher", "pantry")
def dishwasher(it):
    it.box((0, 0, .43), (.6, .6, .86), "white", bevel=.012)
    it.box((0, -.305, .78), (.56, .01, .1), "grey_light", bevel=0)
    it.box((0, -.315, .7), (.4, .02, .02), "metal", bevel=0)
    for i in range(3):
        it.ball((-.2 + i * .05, -.31, .79), (.012, .004, .012), "leaf", seg=4, outline=False)


@item("sink_counter", "Sink counter", "pantry")
def sink_counter(it):
    cabinet(it, 1.2, .6, .88, "sky")
    doors_front(it, 1.1, .1, .82, -.31, "sky", n=2)
    top_slab(it, 1.24, .64, .92, "offwhite", t=.04)
    it.box((0, 0, .9), (.5, .38, .02), "metal", bevel=0, outline=False)
    it.stick((0, .25, .92), (0, .25, 1.18), .03, "metal", seg=6)
    it.stick((0, .25, 1.18), (0, .1, 1.12), .025, "metal", seg=6)


@item("oven_tower", "Oven tower", "pantry")
def oven_tower(it):
    cabinet(it, .65, .6, 2.1, "white")
    it.box((0, -.31, 1.1), (.56, .02, .5), "black", bevel=.01)
    it.box((0, -.32, 1.1), (.42, .01, .3), "glass", bevel=0, outline=False)
    it.box((0, -.33, 1.37), (.4, .02, .02), "metal", bevel=0)
    doors_front(it, .6, .1, .8, -.31, "white", n=1)
    doors_front(it, .6, 1.4, 2.05, -.31, "white", n=1)


@item("toaster", "Toaster", "pantry")
def toaster(it):
    it.box((0, 0, .1), (.28, .17, .2), "peach", bevel=.05)
    for sx in (-1, 1):
        it.box((sx * .05, 0, .2), (.03, .12, .01), "charcoal", bevel=0, outline=False)
    it.box((.15, 0, .12), (.02, .03, .04), "charcoal", bevel=0)
    it.box((-.05, 0, .23), (.02, .1, .06), "wood_light", bevel=.008)


@item("kettle", "Electric kettle", "pantry")
def kettle(it):
    it.cyl((0, 0, .015), (.18, .18), .03, "black", seg=12)
    it.cyl((0, 0, .13), (.16, .16), .2, "white", seg=14, top=.8, bevel=.02)
    it.box((.09, 0, .14), (.03, .04, .16), "black", bevel=.01)
    it.cyl((-.08, 0, .2), (.03, .03), .06, "white", seg=6, rot=(0, -50, 0))


@item("rice_cooker", "Rice cooker", "pantry")
def rice_cooker(it):
    it.cyl((0, 0, .11), (.3, .3), .22, "white", seg=16, bevel=.04)
    it.ball((0, 0, .23), (.28, .28, .1), "coral", seg=14)
    it.box((0, -.15, .12), (.1, .02, .05), "charcoal", bevel=.004)
    it.box((0, 0, .29), (.08, .03, .03), "charcoal", bevel=.008)


@item("blender_jug", "Blender", "pantry")
def blender_jug(it):
    it.box((0, 0, .06), (.16, .16, .12), "charcoal", bevel=.03)
    it.cyl((0, 0, .24), (.13, .13), .24, "glass", seg=12, top=1.2)
    it.cyl((0, 0, .37), (.16, .16), .03, "black", seg=12)
    it.cyl((0, 0, .18), (.1, .1), .08, "blush", seg=10, outline=False)


@item("fruit_bowl", "Fruit bowl", "pantry")
def fruit_bowl(it):
    it.cyl((0, 0, .04), (.3, .3), .08, "wood_light", seg=16, top=1.4)
    for i, m in enumerate(("coral", "butter", "leaf", "peach", "coral")):
        x, y, _ = _polar(.07 if i < 4 else 0, i * 90)
        it.ball((x, y, .1 + (.04 if i == 4 else 0)), (.08, .08, .08), m, seg=8)


@item("snack_shelf", "Snack shelf", "pantry")
def snack_shelf(it):
    it.box((0, 0, .7), (.9, .35, 1.4), "wood_light", bevel=.008)
    for i in range(4):
        z = .12 + i * .33
        it.box((0, -.02, z + .14), (.84, .3, .3), "offwhite", bevel=0, outline=False)
        for k in range(5):
            it.box((-.34 + k * .17, -.06, z + .08), (.12, .1, .14 + (k % 2) * .04), PASTEL[(i + k) % 8], bevel=.004)


@item("vending_machine", "Vending machine", "pantry")
def vending_machine(it):
    it.box((0, 0, .95), (.9, .8, 1.9), "coral", bevel=.02)
    it.box((-.1, -.405, 1.15), (.6, .01, 1.3), "glass", bevel=0, outline=False)
    for r in range(5):
        for c in range(4):
            it.cyl((-.32 + c * .15, -.36, .6 + r * .26), (.07, .07), .14, PASTEL[(r + c) % 8], seg=8)
    it.box((.32, -.41, 1.3), (.14, .01, .3), "charcoal", bevel=0)
    it.box((-.1, -.41, .25), (.5, .02, .14), "charcoal", bevel=0)


@item("cups_dispenser", "Cup dispenser", "pantry", mount="wall", mount_z=1.2)
def cups_dispenser(it):
    for i in range(3):
        x = -.1 + i * .1
        it.cyl((x, -.06, 0), (.08, .08), .4, "glass", seg=10)
        for k in range(5):
            it.cyl((x, -.06, -.12 + k * .06), (.07, .07), .05, "paper", seg=10, top=1.2, outline=False)
    it.box((0, -.01, 0), (.34, .02, .45), "white", bevel=.004)


@item("dish_rack", "Dish rack", "pantry")
def dish_rack(it):
    it.box((0, 0, .015), (.45, .3, .03), "grey_light", bevel=.006)
    for i in range(5):
        it.cyl((-.15 + i * .06, .05, .12), (.2, .2), .015, PASTEL[i], seg=14, rot=(90, 0, 0))
    for i in range(3):
        it.cyl((.16, -.08 + i * .0, .06 + i * .04), (.09, .09), .1, PASTEL[i + 4], seg=10)


@item("tea_set", "Tea set", "pantry")
def tea_set(it):
    it.cyl((0, 0, .01), (.36, .26), .02, "wood_mid", seg=16)
    it.ball((0, 0, .08), (.13, .13, .11), "offwhite", seg=12)
    it.cyl((.07, 0, .1), (.025, .025), .06, "offwhite", seg=6, rot=(0, 50, 0))
    it.ball((0, 0, .14), (.04, .04, .03), "sage", seg=6)
    for sx in (-1, 1):
        it.cyl((sx * .12, -.06, .045), (.06, .06), .05, "offwhite", seg=10, top=1.2)


@item("bread_box", "Bread box", "pantry")
def bread_box(it):
    it.box((0, 0, .08), (.36, .22, .16), "wood_light", bevel=.04)
    it.box((0, -.11, .1), (.1, .01, .02), "wood_dark", bevel=0)
    it.ball((.1, 0, .2), (.2, .1, .08), "wood_mid", seg=8)


@item("cookie_jar", "Cookie jar", "pantry")
def cookie_jar(it):
    it.cyl((0, 0, .1), (.18, .18), .2, "glass", seg=14, bevel=.02)
    it.cyl((0, 0, .21), (.19, .19), .03, "wood_mid", seg=14)
    it.ball((0, 0, .235), (.04, .04, .03), "wood_mid", seg=8)
    for i in range(4):
        it.cyl((0, 0, .03 + i * .03), (.12, .12), .02, "wood_light", seg=10, rot=(i * 10, 0, 0), outline=False)


@item("pantry_cabinet_tall", "Tall pantry cabinet", "pantry")
def pantry_cabinet_tall(it):
    cabinet(it, .8, .55, 2.1, "sage")
    doors_front(it, .76, .08, 2.06, -.28, "sage", n=2)


@item("bar_counter", "Coffee bar counter", "pantry")
def bar_counter(it):
    cabinet(it, 2.0, .6, .9, "wood_dark")
    top_slab(it, 2.1, .7, .95, "offwhite", t=.04)
    for i in range(4):
        it.box((-.75 + i * .5, -.31, .5), (.46, .02, .7), "wood_mid", bevel=.004)
    it.box((-.6, 0, 1.15), (.35, .35, .4), "charcoal", bevel=.02)
    for i in range(4):
        it.cyl((.3 + i * .14, .1, 1.0), (.08, .08), .1, PASTEL[i], seg=10)


@item("juice_dispenser", "Drink dispenser", "pantry")
def juice_dispenser(it):
    it.box((0, 0, .05), (.4, .25, .1), "metal", bevel=.01)
    for sx in (-1, 1):
        it.cyl((sx * .1, 0, .3), (.17, .17), .4, "glass", seg=14)
        it.cyl((sx * .1, 0, .22), (.15, .15), .22, ("butter", "coral")[(sx + 1) // 2], seg=14, outline=False)
        it.box((sx * .1, -.1, .13), (.03, .05, .03), "black", bevel=0)


@item("microwave_shelf", "Microwave cart", "pantry")
def microwave_shelf(it):
    legs4(it, .6, .45, .9, "black", dia=.025, inset=.03)
    for z in (.3, .9):
        it.box((0, 0, z), (.6, .45, .02), "wood_light", bevel=.004)
    it.box((0, 0, 1.06), (.48, .36, .3), "white", bevel=.02)
    it.box((-.05, -.181, 1.06), (.3, .004, .2), "glass", bevel=0, outline=False)
    for i in range(3):
        it.box((-.2 + i * .2, 0, .4), (.14, .3, .18), PASTEL[i + 2], bevel=.015)


@item("ice_cream_freezer", "Chest freezer", "pantry")
def ice_cream_freezer(it):
    it.box((0, 0, .42), (1.0, .65, .84), "white", bevel=.02)
    it.box((0, 0, .85), (.96, .61, .02), "glass", bevel=0)
    for i in range(6):
        it.box((-.35 + i * .14, 0, .8), (.1, .4, .06), PASTEL[i], bevel=.01, outline=False)
    it.box((0, -.33, .5), (.6, .01, .2), "sky", bevel=0, outline=False)


# =========================================================================== RECREATION
@item("pingpong_table", "Table tennis table", "recreation")
def pingpong_table(it):
    top_slab(it, 2.74, 1.52, .76, "blue", t=.03, bevel=.004)
    it.box((0, 0, .763), (2.72, .02, .003), "white", bevel=0, outline=False)
    it.box((0, 0, .763), (.02, 1.5, .003), "white", bevel=0, outline=False)
    it.box((0, 0, .84), (.02, 1.7, .15), "white", bevel=0)
    for sx in (-1, 1):
        it.box((sx * .9, 0, .37), (.06, 1.2, .06), "black", bevel=0)
        for sy in (-1, 1):
            it.box((sx * .9, sy * .55, .37), (.05, .05, .74), "black", bevel=0)


@item("foosball_table", "Foosball table", "recreation")
def foosball_table(it):
    it.box((0, 0, .8), (1.2, .7, .25), "wood_mid", bevel=.015)
    it.box((0, 0, .9), (1.1, .6, .02), "leaf", bevel=0, outline=False)
    legs4(it, 1.1, .6, .7, "wood_dark", dia=.08, inset=.06)
    for i in range(8):
        x = -.49 + i * .14
        it.stick((x, -.5, .92), (x, .5, .92), .015, "metal", seg=4)
        it.box((x, -.55 + (i % 2) * 1.1, .92), (.03, .06, .03), "black", bevel=0)
        for k in range(2):
            it.box((x, -.12 + k * .24, .88), (.03, .03, .08), ("coral", "sky")[i % 2], bevel=0)


@item("arcade_cabinet", "Arcade cabinet", "recreation")
def arcade_cabinet(it):
    it.box((0, 0, .9), (.7, .75, 1.8), "lavender", bevel=.02)
    it.box((0, -.3, 1.3), (.6, .1, .5), "black", bevel=.01, rot=(-12, 0, 0))
    screen_face(it, (0, -.36, 1.3), .5, .4, rot=(-12, 0, 0))
    it.box((0, -.4, .95), (.66, .25, .06), "charcoal", bevel=.01, rot=(15, 0, 0))
    it.stick((-.15, -.45, .98), (-.15, -.45, 1.06), .02, "black", seg=4)
    it.ball((-.15, -.45, 1.07), (.04, .04, .04), "coral", seg=6)
    for i in range(3):
        it.ball((.05 + i * .07, -.45, .99), (.04, .04, .02), PASTEL[i], seg=6)
    it.box((0, -.3, 1.68), (.66, .1, .18), "butter", bevel=.01)


@item("dartboard", "Dartboard", "recreation", mount="wall", mount_z=1.73)
def dartboard(it):
    it.cyl((0, -.02, 0), (.6, .6), .04, "wood_dark", seg=20, rot=(90, 0, 0))
    for i, (d, m) in enumerate(((.45, "black"), (.32, "offwhite"), (.18, "coral"), (.05, "leaf"))):
        it.cyl((0, -.04 - i * .002, 0), (d, d), .004, m, seg=20, rot=(90, 0, 0), outline=False)
    for k in range(2):
        it.stick((.05 * k, -.05, .03 - .05 * k), (.05 * k, -.14, .05 - .05 * k), .008, "butter", seg=4)


@item("board_game_shelf", "Board game shelf", "recreation")
def board_game_shelf(it):
    it.box((0, 0, .6), (.9, .35, 1.2), "wood_light", bevel=.008)
    for i in range(3):
        z = .1 + i * .38
        it.box((0, -.02, z + .17), (.84, .3, .34), "offwhite", bevel=0, outline=False)
        for k in range(5):
            it.box((-.3, -.04, z + .02 + k * .055), (.3 + (k % 2) * .06, .26, .05), PASTEL[(i * 5 + k) % 8],
                   bevel=.004)
        it.box((.25, -.04, z + .12), (.3, .26, .2), PASTEL[(i + 3) % 8], bevel=.008)


@item("guitar_stand", "Guitar on stand", "recreation")
def guitar_stand(it):
    for deg in (60, 120, 270):
        it.stick(_polar(.2, deg, 0), (0, .05, .3), .025, "black", seg=4)
    it.stick((0, .05, .3), (0, .1, .95), .025, "black", seg=4)
    it.ball((0, 0, .32), (.38, .1, .36), "wood_light", seg=12)
    it.ball((0, 0, .58), (.3, .1, .28), "wood_light", seg=12)
    it.cyl((0, -.05, .48), (.09, .09), .01, "black", seg=10, rot=(90, 0, 0), outline=False)
    it.box((0, .0, .95), (.05, .03, .5), "wood_dark", bevel=.004)
    it.box((0, .0, 1.24), (.08, .03, .12), "wood_dark", bevel=.01)


@item("keyboard_piano", "Digital piano", "recreation")
def keyboard_piano(it):
    it.box((0, 0, .75), (1.35, .35, .12), "black", bevel=.01)
    it.box((0, -.1, .815), (1.25, .15, .01), "white", bevel=0, outline=False)
    for i in range(18):
        if i % 7 in (2, 6):
            continue
        it.box((-.58 + i * .07, -.06, .825), (.03, .08, .012), "black", bevel=0, outline=False)
    for sx in (-1, 1):
        it.box((sx * .6, 0, .35), (.05, .35, .7), "black", bevel=.006)
    it.box((0, .15, .9), (.4, .03, .2), "black", bevel=.004, rot=(-15, 0, 0))


@item("karaoke_mic_stand", "Mic stand & speaker", "recreation")
def karaoke_mic_stand(it):
    for deg in (90, 210, 330):
        it.stick(_polar(.25, deg, 0), (0, 0, .15), .02, "black", seg=4)
    it.stick((0, 0, .15), (0, 0, 1.45), .025, "black", seg=5)
    it.ball((0, -.04, 1.5), (.06, .06, .1), "metal", seg=8)
    it.box((.55, .1, .35), (.38, .35, .7), "charcoal", bevel=.03)
    for z in (.25, .55):
        it.cyl((.55, -.08, z), (.22 if z < .3 else .12, .22 if z < .3 else .12), .01, "black", seg=14,
               rot=(90, 0, 0), outline=False)


@item("basketball_hoop_mini", "Mini basketball hoop", "recreation", mount="wall", mount_z=2.0)
def basketball_hoop_mini(it):
    it.box((0, -.02, .1), (.6, .03, .4), "white", bevel=.006)
    it.box((0, -.04, .02), (.2, .004, .14), "coral", bevel=0, outline=False)
    for i in range(12):
        a0, a1 = i * 30, (i + 1) * 30
        it.stick(_polar(.12, a0, -.08), _polar(.12, a1, -.08), .012, "coral", seg=4)
    for i in range(12):
        x, y, _ = _polar(.12, i * 30)
        it.stick((x, y - .14, -.08), (x * .6, y * .6 - .14, -.25), .006, "white", seg=3)


@item("chess_table", "Chess table", "recreation")
def chess_table(it):
    pedestal(it, .7, .4, "wood_dark")
    it.box((0, 0, .72), (.6, .6, .04), "wood_mid", bevel=.008)
    for r in range(8):
        for c in range(8):
            if (r + c) % 2:
                it.box((-.2275 + c * .065, -.2275 + r * .065, .741), (.065, .065, .002), "wood_dark", bevel=0,
                       outline=False)
    for i in range(4):
        it.cyl((-.2 + i * .13, -.23, .77), (.035, .035), .05, "offwhite", seg=6, top=.5)
        it.cyl((-.2 + i * .13, .23, .77), (.035, .035), .05, "black", seg=6, top=.5)


@item("puzzle_table", "Jigsaw puzzle table", "recreation")
def puzzle_table(it):
    top_slab(it, 1.0, .7, .72, "wood_light", t=.03)
    legs4(it, 1.0, .7, .7, "wood_mid", dia=.04, inset=.05)
    it.box((0, 0, .723), (.8, .5, .004), "sky", bevel=0, outline=False)
    it.box((-.1, .05, .726), (.4, .25, .004), "leaf", bevel=0, outline=False)
    for i in range(6):
        it.box((.3 + (i % 2) * .05, -.2 + i * .05, .727), (.04, .04, .004), PASTEL[i], bevel=0, outline=False,
               rot=(0, 0, i * 20))


@item("bean_bag_cluster", "Bean bag cluster", "recreation")
def bean_bag_cluster(it):
    for i, m in enumerate(("coral", "sky", "butter")):
        x, y, _ = _polar(.55, 90 + i * 120)
        it.ball((x, y, .25), (.75, .75, .5), m, seg=12)
        it.ball((x * 1.25, y * 1.25, .45), (.55, .55, .4), m, seg=10)
    it.cyl((0, 0, .15), (.5, .5), .3, "wood_light", seg=14)


@item("plush_corner", "Plushie corner", "recreation")
def plush_corner(it):
    it.cyl((0, 0, .03), (.9, .9), .06, "blush", seg=16, bevel=.02)
    for i, m in enumerate(("butter", "sky", "lavender")):
        x, y, _ = _polar(.22, 90 + i * 120)
        it.ball((x, y, .2), (.24, .2, .24), m, seg=10)
        it.ball((x, y - .02, .38), (.2, .18, .18), m, seg=10)
        for sx in (-1, 1):
            it.ball((x + sx * .06, y, .47), (.06, .05, .06), m, seg=6)
        it.ball((x, y - .1, .38), (.06, .02, .03), "black", seg=6, outline=False)


@item("pool_table_mini", "Billiard table", "recreation")
def pool_table_mini(it):
    it.box((0, 0, .7), (2.2, 1.2, .16), "wood_dark", bevel=.02)
    it.box((0, 0, .785), (2.0, 1.0, .02), "leaf_dark", bevel=0, outline=False)
    for sx in (-1, 1):
        it.box((sx * .9, 0, .32), (.15, .9, .6), "wood_dark", bevel=.02)
    for i, m in enumerate(("butter", "coral", "blue", "white", "black")):
        it.ball((.3 + (i % 3) * .06, -.1 + i * .05, .82), (.06, .06, .06), m, seg=8)
    it.stick((-.8, .3, .8), (.1, -.1, .82), .02, "wood_mid", seg=4)


# =========================================================================== DECOR (more plants & objects)
@item("plant_monstera", "Monstera", "decor")
def plant_monstera(it):
    pot(it, .36, .35, "offwhite")
    for i in range(7):
        deg = i * 51
        x, y, _ = _polar(.25, deg)
        z = .65 + (i % 3) * .2
        it.stick((0, 0, .33), (x * .8, y * .8, z), .015, "leaf_dark", seg=4)
        it.ball((x, y, z + .05), (.32, .32, .06), "leaf" if i % 2 else "leaf_dark", seg=10,
                rot=(30 * math.sin(math.radians(deg)), -30 * math.cos(math.radians(deg)), 0))


@item("plant_fiddle_leaf", "Fiddle leaf fig", "decor")
def plant_fiddle_leaf(it):
    pot(it, .34, .38, "charcoal")
    it.stick((0, 0, .36), (0, 0, 1.4), .04, "wood_dark", seg=5)
    for i in range(10):
        z = .8 + i * .07
        x, y, _ = _polar(.14, i * 75)
        it.ball((x, y, z), (.16, .1, .22), "leaf_dark" if i % 2 else "leaf", seg=8, rot=(0, 0, i * 75))


@item("plant_palm", "Areca palm", "decor")
def plant_palm(it):
    pot(it, .45, .4, "white")
    for i in range(9):
        deg = i * 40
        x, y, _ = _polar(.5, deg)
        it.stick((0, 0, .38), (x * .7, y * .7, 1.3 + (i % 3) * .1), .015, "leaf_dark", seg=4)
        it.ball((x * .55, y * .55, 1.15 + (i % 3) * .1), (.4, .1, .06), "leaf", seg=8, rot=(0, 30, deg))


@item("plant_bamboo", "Lucky bamboo", "decor")
def plant_bamboo(it):
    it.cyl((0, 0, .08), (.18, .18), .16, "glass", seg=12)
    it.cyl((0, 0, .05), (.17, .17), .08, "water", seg=12, outline=False)
    for i in range(5):
        x, y, _ = _polar(.04, i * 72)
        h = .3 + (i % 3) * .12
        it.cyl((x, y, h / 2 + .02), (.025, .025), h, "leaf", seg=6)
        it.ball((x + .03, y, h), (.08, .03, .04), "leaf_dark", seg=6)


@item("plant_olive", "Olive tree", "decor")
def plant_olive(it):
    pot(it, .4, .35, "pot")
    it.stick((0, 0, .33), (.03, 0, 1.0), .04, "wood_mid", seg=5)
    for i in range(8):
        x, y, _ = _polar(.2, i * 45)
        it.ball((x, y, 1.0 + (i % 3) * .12), (.3, .3, .2), "sage", seg=8)


@item("plant_rubber", "Rubber plant", "decor")
def plant_rubber(it):
    pot(it, .3, .3, "butter")
    for i in range(3):
        x, y, _ = _polar(.05, i * 120)
        it.stick((x, y, .28), (x * 2, y * 2, .9 + i * .1), .025, "wood_dark", seg=4)
        for k in range(3):
            lx, ly, _ = _polar(.1, i * 120 + k * 120)
            it.ball((x * 2 + lx, y * 2 + ly, .6 + i * .1 + k * .12), (.16, .06, .22), "black", seg=8)


@item("terrarium", "Terrarium", "decor")
def terrarium(it):
    it.ball((0, 0, .15), (.3, .3, .3), "glass", seg=14)
    it.cyl((0, 0, .02), (.2, .2), .04, "soil", seg=12, outline=False)
    for i in range(3):
        x, y, _ = _polar(.05, i * 120)
        leaf_ball(it, (x, y, .08), (.07, .07, .08), i)
    it.cyl((0, 0, .29), (.08, .08), .03, "wood_mid", seg=10)


@item("aquarium", "Aquarium", "decor")
def aquarium(it):
    cabinet(it, 1.0, .4, .75, "wood_dark")
    it.box((0, 0, 1.0), (.96, .38, .5), "glass", bevel=.004)
    it.box((0, 0, .92), (.92, .34, .3), "water", bevel=0, outline=False)
    it.box((0, 0, 1.27), (1.0, .4, .04), "black", bevel=.004)
    for i, m in enumerate(("coral", "butter", "sky")):
        it.ball((-.25 + i * .25, -.05, .95 + (i % 2) * .08), (.08, .03, .05), m, seg=6)
    for i in range(4):
        it.stick((-.4 + i * .25, .1, .78), (-.38 + i * .25, .1, .98), .02, "leaf", seg=4)


@item("sculpture_abstract", "Abstract sculpture", "decor")
def sculpture_abstract(it):
    it.box((0, 0, .4), (.35, .35, .8), "white", bevel=.01)
    it.ball((0, 0, .95), (.25, .25, .25), "coral", seg=12)
    it.cyl((.05, 0, 1.15), (.18, .18), .04, "butter", seg=12, rot=(30, 20, 0))
    it.box((-.04, 0, 1.25), (.08, .08, .15), "sky", bevel=.02, rot=(0, 20, 30))


@item("vase_floor_branches", "Floor vase with branches", "decor")
def vase_floor_branches(it):
    it.cyl((0, 0, .3), (.25, .25), .6, "sage", seg=14, top=.6, bevel=.02)
    for i in range(5):
        x, y, _ = _polar(.25, i * 72)
        it.stick((0, 0, .55), (x, y, 1.3 + (i % 2) * .15), .015, "wood_dark", seg=4)
        it.ball((x, y, 1.3 + (i % 2) * .15), (.06, .06, .06), "blush", seg=6)


@item("vase_trio", "Vase trio", "decor")
def vase_trio(it):
    for i, (x, h, m) in enumerate(((-.1, .3, "sky"), (.04, .2, "butter"), (.14, .14, "blush"))):
        it.cyl((x, 0, h / 2), (.1, .1), h, m, seg=12, top=.5 + i * .2, bevel=.01)


@item("candle_set", "Candle set", "decor")
def candle_set(it):
    it.cyl((0, 0, .01), (.3, .3), .02, "wood_mid", seg=16)
    for i, h in enumerate((.18, .12, .08)):
        x, y, _ = _polar(.07, 90 + i * 120)
        it.cyl((x, y, .02 + h / 2), (.06, .06), h, "offwhite", seg=10)
        it.ball((x, y, .03 + h), (.015, .015, .03), "lamp_glow", seg=6)


@item("bookends_books", "Bookends with books", "decor")
def bookends_books(it):
    for sx in (-1, 1):
        it.box((sx * .18, 0, .08), (.03, .14, .16), "charcoal", bevel=.006)
    _book_row(it, -.16, .16, 0, .12, BOOKS, k=3)


@item("hourglass", "Hourglass", "decor")
def hourglass(it):
    for z in (.01, .25):
        it.cyl((0, 0, z), (.12, .12), .02, "wood_mid", seg=10)
    it.cyl((0, 0, .07), (.08, .08), .1, "glass", seg=10, top=.15)
    it.cyl((0, 0, .19), (.012, .012), .1, "glass", seg=10, top=6.6)
    it.cyl((0, 0, .04), (.06, .06), .04, "butter", seg=8, top=.6, outline=False)
    for i in range(3):
        it.stick(_polar(.05, i * 120, .02), _polar(.05, i * 120, .24), .01, "wood_mid", seg=4)


@item("lava_lamp", "Lava lamp", "decor")
def lava_lamp(it):
    it.cyl((0, 0, .06), (.12, .12), .12, "metal", seg=12, top=.6)
    it.cyl((0, 0, .22), (.08, .08), .22, "glass", seg=12, top=.6)
    for z in (.17, .25):
        it.ball((0, 0, z), (.04, .04, .05), "coral", seg=6, outline=False)
    it.cyl((0, 0, .35), (.05, .05), .05, "metal", seg=10, top=.4)


@item("cat_figurine", "Lucky cat figurine", "decor")
def cat_figurine(it):
    it.ball((0, 0, .08), (.14, .12, .16), "white", seg=10)
    it.ball((0, 0, .2), (.13, .12, .11), "white", seg=10)
    for sx in (-1, 1):
        it.cyl((sx * .04, 0, .26), (.04, .03), .04, "white", seg=4, top=.1)
    it.ball((.06, -.04, .18), (.04, .04, .06), "white", seg=6)
    it.box((0, -.06, .1), (.06, .01, .02), "coral", bevel=0, outline=False)
    it.ball((0, -.06, .07), (.04, .02, .04), "butter", seg=6, outline=False)


@item("planter_long", "Long planter trough", "decor")
def planter_long(it):
    it.box((0, 0, .2), (1.4, .3, .4), "charcoal", bevel=.01)
    it.box((0, 0, .395), (1.34, .26, .01), "soil", bevel=0, outline=False)
    for i in range(10):
        x = -.6 + i * .135
        it.stick((x, 0, .4), (x, 0, .7 + (i % 3) * .08), .03, ("leaf", "leaf_dark")[i % 2], seg=4)
        it.ball((x, 0, .72 + (i % 3) * .08), (.08, .03, .12), ("leaf", "leaf_dark")[i % 2], seg=6)


@item("planter_round_large", "Large round planter", "decor")
def planter_round_large(it):
    pot(it, .7, .5, "wood_light", top=1.0)
    for i in range(7):
        x, y, _ = _polar(.18 if i else 0, i * 60)
        leaf_ball(it, (x, y, .7 + (0 if i else .15)), (.35, .35, .4), i)


@item("plant_cactus_tall", "Tall cactus", "decor")
def plant_cactus_tall(it):
    pot(it, .3, .25, "peach")
    it.cyl((0, 0, .75), (.16, .16), 1.0, "leaf", seg=10, bevel=.06)
    for sx, z in ((-1, .8), (1, 1.0)):
        it.stick((0, 0, z), (sx * .16, 0, z), .1, "leaf", seg=8)
        it.cyl((sx * .16, 0, z + .14), (.1, .1), .3, "leaf", seg=8, bevel=.04)
    it.ball((0, 0, 1.27), (.08, .08, .06), "blush", seg=6)


@item("succulent_trio", "Succulent trio", "decor")
def succulent_trio(it):
    for i, m in enumerate(("white", "sky", "blush")):
        x = -.12 + i * .12
        it.cyl((x, 0, .04), (.09, .09), .08, m, seg=10, bevel=.01)
        for k in range(5):
            lx, ly, _ = _polar(.02, k * 72)
            it.ball((x + lx, ly, .09), (.04, .04, .025), ("sage", "leaf", "mint")[i], seg=6,
                    rot=(0, 30, k * 72))


@item("plant_lavender", "Lavender pot", "decor")
def plant_lavender(it):
    pot(it, .2, .16, "offwhite")
    for i in range(9):
        x, y, _ = _polar(.05, i * 40)
        it.stick((x * .4, y * .4, .15), (x, y, .38 + (i % 3) * .03), .008, "sage", seg=3)
        it.cyl((x, y, .4 + (i % 3) * .03), (.025, .025), .07, "lavender", seg=5)


@item("plant_zz", "ZZ plant", "decor")
def plant_zz(it):
    pot(it, .24, .22, "black")
    for i in range(6):
        x, y, _ = _polar(.1, i * 60)
        it.stick((0, 0, .2), (x, y, .6), .012, "leaf_dark", seg=3)
        for k in range(4):
            t = .3 + k * .18
            it.ball((x * t, y * t, .2 + .4 * t), (.05, .03, .03), "leaf_dark", seg=5, rot=(0, 0, i * 60))


@item("plant_bird_paradise", "Bird of paradise", "decor")
def plant_bird_paradise(it):
    pot(it, .42, .4, "sage")
    for i in range(6):
        deg = i * 60
        x, y, _ = _polar(.2, deg)
        it.stick((0, 0, .38), (x, y, 1.2 + (i % 2) * .2), .02, "leaf_dark", seg=4)
        it.ball((x * 1.1, y * 1.1, 1.35 + (i % 2) * .2), (.14, .04, .5), "leaf", seg=8, rot=(0, 15, deg))
    it.box((.1, 0, 1.1), (.15, .04, .06), "coral", bevel=.01, rot=(0, -30, 0))


@item("tree_indoor", "Indoor tree", "decor")
def tree_indoor(it):
    pot(it, .6, .5, "wood_mid", top=1.0)
    it.stick((0, 0, .48), (0, 0, 1.6), .1, "wood_dark", seg=6)
    for i in range(3):
        x, y, _ = _polar(.25, i * 120)
        it.stick((0, 0, 1.3), (x, y, 1.8), .05, "wood_dark", seg=5)
    for i in range(6):
        x, y, _ = _polar(.35, i * 60)
        leaf_ball(it, (x, y, 2.0 + (i % 2) * .15), (.6, .6, .5), i)
    leaf_ball(it, (0, 0, 2.3), (.7, .7, .5), 1)


@item("flower_bouquet", "Flower bouquet vase", "decor")
def flower_bouquet(it):
    it.cyl((0, 0, .12), (.13, .13), .24, "glass", seg=12, top=.8)
    for i in range(7):
        x, y, _ = _polar(.07 if i else 0, i * 60)
        it.stick((0, 0, .2), (x, y, .42 + (i % 2) * .04), .008, "leaf_dark", seg=3)
        it.ball((x, y, .44 + (i % 2) * .04), (.07, .07, .06), ("coral", "butter", "blush", "lavender")[i % 4], seg=8)


@item("globe_small", "Desk globe", "decor")
def globe_small(it):
    it.cyl((0, 0, .015), (.14, .14), .03, "wood_dark", seg=12)
    it.stick((0, 0, .03), (0, 0, .08), .02, "wood_dark", seg=4)
    it.ball((0, 0, .2), (.22, .22, .22), "sky", seg=14)
    for i in range(3):
        x, y, _ = _polar(.09, i * 120)
        it.ball((x * .9, y * .9, .2 + (i - 1) * .06), (.08, .06, .06), "leaf", seg=6, outline=False)
    for i in range(6):
        a0, a1 = math.radians(-60 + i * 25), math.radians(-60 + (i + 1) * 25)
        it.stick((math.sin(a0) * .13, 0, .2 + math.cos(a0) * .13), (math.sin(a1) * .13, 0, .2 + math.cos(a1) * .13),
                 .012, "metal", seg=3)


# =========================================================================== WALL (more)
@item("wall_art_triptych", "Triptych wall art", "wall", mount="wall", mount_z=1.3)
def wall_art_triptych(it):
    for i, m in enumerate(("sky", "butter", "blush")):
        x = -.5 + i * .5
        it.box((x, -.02, .35), (.42, .04, .6), "white", bevel=.006)
        it.box((x, -.042, .35), (.36, .004, .54), m, bevel=0, outline=False)
        it.ball((x, -.046, .3 + (i % 2) * .1), (.15, .004, .15), PASTEL[(i + 4) % 8], seg=10, outline=False)


@item("wall_art_abstract", "Abstract canvas", "wall", mount="wall", mount_z=1.2)
def wall_art_abstract(it):
    it.box((0, -.02, .45), (1.0, .04, .8), "offwhite", bevel=.006)
    it.box((-.2, -.042, .55), (.4, .004, .4), "coral", bevel=0, outline=False, rot=(0, 15, 0))
    it.ball((.2, -.044, .35), (.35, .004, .35), "sage", seg=14, outline=False)
    it.box((.1, -.046, .65), (.5, .004, .05), "charcoal", bevel=0, outline=False)


@item("wall_tapestry", "Woven tapestry", "wall", mount="wall", mount_z=1.0)
def wall_tapestry(it):
    it.stick((-.4, -.03, 1.0), (.4, -.03, 1.0), .03, "wood_mid", seg=5)
    it.box((0, -.02, .65), (.7, .015, .7), "offwhite", bevel=0)
    for i in range(3):
        it.box((0, -.03, .85 - i * .18), (.7, .006, .06), ("peach", "sage", "coral")[i], bevel=0, outline=False)
    for i in range(10):
        it.stick((-.32 + i * .07, -.02, .3), (-.32 + i * .07, -.02, .15), .015, "offwhite", seg=3)


@item("acoustic_panels", "Acoustic panel set", "wall", mount="wall", mount_z=1.0)
def acoustic_panels(it):
    for r in range(2):
        for c in range(3):
            it.box((-.42 + c * .42, -.025, .2 + r * .42), (.4, .05, .4), PASTEL[(r * 3 + c) % 8], bevel=.02)


@item("pegboard_tools", "Pegboard", "wall", mount="wall", mount_z=1.0)
def pegboard_tools(it):
    it.box((0, -.01, .4), (.9, .02, .8), "wood_light", bevel=.004)
    for r in range(5):
        for c in range(7):
            it.ball((-.36 + c * .12, -.021, .1 + r * .15), (.012, .002, .012), "wood_dark", seg=4, outline=False)
    it.box((-.25, -.05, .55), (.25, .08, .02), "wood_mid", bevel=0)
    for i in range(3):
        it.cyl((-.32 + i * .07, -.05, .6), (.05, .05), .1, PASTEL[i], seg=8)
    it.stick((.2, -.03, .7), (.2, -.03, .4), .02, "coral", seg=4)
    it.box((.3, -.04, .3), (.18, .04, .12), "sky", bevel=.01)


@item("wall_planter_trio", "Wall planter trio", "wall", mount="wall", mount_z=1.2)
def wall_planter_trio(it):
    for i in range(3):
        x, z = -.3 + i * .3, (i % 2) * .2
        it.cyl((x, -.08, z), (.16, .16), .14, "white", seg=12)
        leaf_ball(it, (x, -.08, z + .12), (.18, .16, .14), i)
        it.box((x, -.01, z), (.04, .02, .14), "wood_mid", bevel=0)


@item("clock_digital_wall", "Digital wall clock", "wall", mount="wall", mount_z=2.0)
def clock_digital_wall(it):
    it.box((0, -.02, 0), (.5, .04, .18), "charcoal", bevel=.01)
    for i in range(4):
        it.box((-.16 + i * .1 + (.02 if i > 1 else 0), -.042, 0), (.07, .004, .11), "lamp_glow", bevel=0,
               outline=False)


@item("map_world", "World map", "wall", mount="wall", mount_z=1.2)
def map_world(it):
    it.box((0, -.015, .4), (1.4, .03, .8), "wood_mid", bevel=.006)
    it.box((0, -.032, .4), (1.34, .004, .74), "sky", bevel=0, outline=False)
    for (x, z, w, h) in ((-.4, .55, .3, .2), (-.3, .25, .15, .25), (.05, .5, .2, .25), (.1, .25, .12, .2),
                         (.35, .5, .35, .2), (.45, .2, .12, .1)):
        it.ball((x, -.035, z), (w, .004, h), "sage", seg=10, outline=False)


@item("motivational_sign", "Letterboard sign", "wall", mount="wall", mount_z=1.3)
def motivational_sign(it):
    it.box((0, -.02, .25), (.6, .04, .45), "wood_mid", bevel=.008)
    it.box((0, -.042, .25), (.54, .004, .39), "black", bevel=0, outline=False)
    for r in range(3):
        for c in range(6 - r):
            it.box((-.2 + c * .07 + r * .03, -.046, .38 - r * .12), (.045, .004, .06), "white", bevel=0, outline=False)


@item("cork_strip", "Cork strip with notes", "wall", mount="wall", mount_z=1.4)
def cork_strip(it):
    it.box((0, -.01, 0), (1.2, .02, .15), "cork", bevel=.004)
    for i in range(6):
        it.box((-.5 + i * .2, -.024, -.03 * (i % 2)), (.12, .004, .12), PASTEL[i], bevel=0, outline=False,
               rot=(0, (i % 3) * 5 - 5, 0))
        it.ball((-.5 + i * .2, -.03, .04 - .03 * (i % 2)), (.02, .02, .02), "coral", seg=4)


@item("shelf_floating_trio", "Floating shelves trio", "wall", mount="wall", mount_z=1.0)
def shelf_floating_trio(it):
    for i, (x, z) in enumerate(((-.3, 0), (.15, .35), (-.15, .7))):
        it.box((x, -.1, z), (.6, .2, .03), "wood_mid", bevel=.006)
        if i == 0:
            _book_row(it, x - .25, x + .1, z + .015, .14, BOOKS, k=2)
        elif i == 1:
            leaf_ball(it, (x, -.1, z + .12), (.16, .16, .18), 0)
            it.cyl((x, -.1, z + .06), (.12, .12), .1, "white", seg=10)
        else:
            it.ball((x - .1, -.1, z + .07), (.1, .1, .12), "blush", seg=8)
            it.box((x + .12, -.1, z + .08), (.12, .02, .15), "wood_dark", bevel=.004)


@item("coat_hooks", "Coat hook rail", "wall", mount="wall", mount_z=1.6)
def coat_hooks(it):
    it.box((0, -.015, 0), (1.0, .03, .1), "wood_mid", bevel=.006)
    for i in range(5):
        x = -.4 + i * .2
        it.stick((x, -.03, 0), (x, -.1, .04), .02, "black", seg=4)
        if i in (1, 3):
            it.box((x, -.08, -.35), (.3, .1, .6), ("sky", "coral")[i // 3], bevel=.04)


@item("mirror_rect", "Arched mirror", "wall", mount="wall", mount_z=.8)
def mirror_rect(it):
    it.box((0, -.02, .5), (.6, .04, 1.0), "wood_light", bevel=.008)
    it.cyl((0, -.02, 1.0), (.6, .6), .04, "wood_light", seg=16, rot=(90, 0, 0))
    it.box((0, -.042, .5), (.52, .004, .94), "glass", bevel=0, outline=False)
    it.cyl((0, -.042, 1.0), (.52, .52), .004, "glass", seg=16, rot=(90, 0, 0), outline=False)


@item("ac_split_unit", "Split air conditioner", "wall", mount="wall", mount_z=2.3)
def ac_split_unit(it):
    it.box((0, -.11, .14), (.9, .22, .28), "white", bevel=.04)
    it.box((0, -.22, .04), (.8, .02, .03), "grey_light", bevel=0, rot=(-30, 0, 0))
    it.ball((.35, -.222, .18), (.02, .004, .02), "leaf", seg=4, outline=False)


@item("thermostat_panel", "Thermostat & switches", "wall", mount="wall", mount_z=1.3)
def thermostat_panel(it):
    it.box((0, -.01, 0), (.12, .02, .12), "white", bevel=.01)
    it.cyl((0, -.022, 0), (.08, .08), .004, "screen", seg=12, rot=(90, 0, 0), outline=False)
    for i in range(2):
        it.box((.15 + i * .1, -.01, 0), (.08, .02, .12), "white", bevel=.008)
        it.box((.15 + i * .1, -.022, 0), (.03, .004, .05), "grey_light", bevel=0, outline=False)


@item("wall_fan", "Wall fan", "wall", mount="wall", mount_z=2.2)
def wall_fan(it):
    it.box((0, -.03, 0), (.12, .06, .12), "white", bevel=.02)
    it.stick((0, -.05, 0), (0, -.15, -.05), .03, "white", seg=5)
    it.cyl((0, -.2, -.08), (.4, .4), .08, "sky", seg=16, rot=(70, 0, 0))
    it.cyl((0, -.24, -.09), (.08, .08), .03, "white", seg=10, rot=(70, 0, 0))


@item("whiteboard_small", "Small whiteboard", "wall", mount="wall", mount_z=1.2)
def whiteboard_small(it):
    it.box((0, -.015, .3), (.8, .03, .6), "grey", bevel=.006)
    it.box((0, -.032, .3), (.76, .004, .56), "white", bevel=0, outline=False)
    it.box((0, -.05, .01), (.6, .05, .02), "grey", bevel=0)
    for i, m in enumerate(("coral", "blue", "black")):
        it.stick((-.2 + i * .1, -.05, .03), (-.12 + i * .1, -.05, .03), .015, m, seg=4)
    it.box((-.1, -.035, .4), (.4, .002, .03), "blue", bevel=0, outline=False)


@item("calendar_board", "Month planner board", "wall", mount="wall", mount_z=1.2)
def calendar_board(it):
    it.box((0, -.015, .4), (1.0, .03, .7), "white", bevel=.006)
    it.box((0, -.032, .7), (.96, .004, .08), "sage", bevel=0, outline=False)
    for r in range(5):
        for c in range(7):
            it.box((-.42 + c * .14, -.032, .58 - r * .11), (.12, .004, .09), "offwhite", bevel=0, outline=False)
            if (r * 7 + c) % 5 == 0:
                it.box((-.42 + c * .14, -.035, .58 - r * .11), (.08, .004, .04), PASTEL[(r + c) % 8], bevel=0,
                       outline=False)
