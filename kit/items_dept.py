"""Department kit (v5): role props per department + ready-made workstations.

Categories:
  dept_it, dept_creative, dept_content, dept_marketing, dept_finance, dept_hr, dept_sales, dept_exec
      props and floor pieces that tell what a person does
  station
      one complete desk per role (desk + screens + that role's props), composed with Item.place()
      from the other items, so a room can be filled desk by desk. Chairs stay separate pieces.
Same conventions as items.py: pivot bottom center, front -Y (the side the person sits on).
"""
import math

from items import REGISTRY, _polar, _star_base, item

DESK_Z = .75
RAINBOW = ["coral", "peach", "butter", "sage", "sky", "lavender", "blush"]


def fn(item_id):
    return REGISTRY[item_id]["fn"]


def _ring(it, c, r, t, m, seg=16, outline=True):
    """Ring standing in the XZ plane (faces -Y), built from short boxes."""
    for i in range(seg):
        a = 2 * math.pi * i / seg
        it.box((c[0] + r * math.cos(a), c[1], c[2] + r * math.sin(a)), (2 * math.pi * r / seg * 1.15, t, t), m,
               bevel=0, rot=(0, -math.degrees(a) - 90, 0), outline=outline)


def _tripod(it, top_z, spread=.28, m="charcoal"):
    for i in range(3):
        deg = 90 + i * 120
        it.stick(_polar(spread, deg, .012), (0, 0, top_z * .45), .025, m, seg=6)
    it.cyl((0, 0, top_z * .45 + (top_z * .55) / 2), (.03, .03), top_z * .55, "metal", seg=8)
    it.cyl((0, 0, top_z * .45), (.06, .06), .05, m, seg=8)


def _paper(it, c, size, rot=(0, 0, 0), m="paper"):
    it.box(c, (size[0], size[1], .004), m, bevel=0, rot=rot)


# =========================================================================== IT
@item("server_rack", "Server rack", "dept_it")
def server_rack(it):
    w, d, h = .6, .8, 1.8
    it.box((0, 0, h / 2 + .04), (w, d, h - .08), "charcoal", bevel=.02)
    for sx in (-1, 1):
        for sy in (-1, 1):
            it.cyl((sx * .22, sy * .32, .026), (.05, .05), .04, "black", seg=6, rot=(0, 90, 0))
    for k in range(9):   # rack units with blinking LEDs
        z = .3 + k * .16
        it.box((0, -d / 2 + .01, z), (w - .1, .02, .12), "black", bevel=0)
        for j in range(4):
            it.box((-.2 + j * .03, -d / 2 - .002, z + .03), (.014, .004, .01),
                   ("mint", "sky", "butter", "mint")[(j + k) % 4], bevel=0, outline=False)
        it.box((.12, -d / 2 - .002, z - .02), (.14, .004, .03), "grey", bevel=0, outline=False)
    for sx in (-1, 1):                                                                  # door frame (see-through)
        it.box((sx * (w / 2 - .02), -d / 2 - .015, h / 2 + .04), (.03, .02, h - .16), "grey", bevel=.006)
    for z in (.14, h - .06):
        it.box((0, -d / 2 - .015, z), (w - .02, .02, .03), "grey", bevel=.006)
    it.box((w / 2 - .06, -d / 2 - .035, 1.0), (.025, .03, .2), "metal", bevel=.008)    # door handle


@item("mech_keyboard", "Mechanical keyboard", "dept_it", mount="table")
def mech_keyboard(it):
    it.box((0, 0, .015), (.36, .13, .03), "charcoal", bevel=.01)
    for r in range(4):
        for k in range(9):
            it.box((-.15 + k * .0375, -.045 + r * .03, .036), (.032, .026, .016), RAINBOW[(k + r) % 7], bevel=.004,
                   outline=False)
    it.box((0, -.11, .01), (.34, .06, .02), "lavender", bevel=.01)                    # wrist rest
    it.ball((.27, 0, .02), (.06, .1, .04), "charcoal", seg=10)                        # mouse
    it.box((.27, -.02, .038), (.004, .03, .004), "mint", bevel=0, outline=False)


@item("laptop_stickers", "Laptop with stickers", "dept_it", mount="table")
def laptop_stickers(it):
    it.place(fn("laptop"))
    for x, z, c, s in ((-.09, .17, "coral", .06), (.1, .19, "butter", .05), (-.06, .07, "mint", .05),
                       (.09, .08, "sky", .04)):
        y = .12 + .008 + (z - .125) * math.tan(math.radians(14))
        it.cyl((x, y, z), (s, s), .004, c, seg=8, rot=(76, 0, 0), outline=False)
    it.box((.01, .14, .12), (.07, .004, .03), "lavender", bevel=0, rot=(-14, 0, 8), outline=False)   # "{ }" tag


@item("rubber_duck", "Debug duck", "dept_it", mount="table")
def rubber_duck(it):
    it.ball((0, 0, .04), (.1, .12, .08), "butter", seg=12)
    it.ball((0, -.03, .1), (.07, .07, .07), "butter", seg=10)
    it.box((0, -.07, .095), (.035, .03, .014), "coral", bevel=.006)
    for sx in (-1, 1):
        it.ball((sx * .02, -.06, .115), (.012, .008, .012), "black", seg=6, outline=False)


@item("dev_board_kit", "Dev board kit", "dept_it", mount="table")
def dev_board_kit(it):
    it.box((0, 0, .004), (.3, .2, .008), "grey_light", bevel=0)                          # anti-static mat
    it.box((-.05, .02, .015), (.12, .08, .01), "leaf_dark", bevel=.003)                  # board
    it.box((-.07, .03, .025), (.03, .03, .01), "black", bevel=0)                         # chip
    for k in range(6):
        it.box((-.1 + k * .012, -.015, .024), (.006, .006, .01), "butter", bevel=0, outline=False)
    for k, c in enumerate(("coral", "sky", "butter")):                                  # jumper wires
        it.stick((-.0 + k * .01, .0, .024), (.06 + k * .02, -.06, .01), .006, c, seg=4, outline=False)
    it.cyl((.09, .05, .03), (.06, .06), .06, "mint", seg=12)                             # energy drink can
    it.cyl((.09, .05, .061), (.05, .05), .004, "metal", seg=12, outline=False)


@item("nas_box", "NAS storage", "dept_it", mount="table")
def nas_box(it):
    it.box((0, 0, .1), (.18, .22, .2), "black", bevel=.02)
    for k in range(4):
        it.box((-.06 + k * .04, -.111, .1), (.03, .004, .14), "charcoal", bevel=0, outline=False)
        it.box((-.06 + k * .04, -.114, .16), (.008, .004, .008), "mint", bevel=0, outline=False)


# =========================================================================== CREATIVE
@item("drawing_tablet", "Drawing tablet", "dept_creative", mount="table")
def drawing_tablet(it):
    it.box((0, 0, .006), (.36, .24, .012), "black", bevel=.008)
    it.box((.02, 0, .013), (.28, .19, .002), "charcoal", bevel=0, outline=False)
    for k in range(3):
        it.box((-.16, .06 - k * .04, .014), (.02, .025, .004), "grey", bevel=0, outline=False)
    it.stick((.08, -.13, .01), (.2, -.06, .01), .012, "grey_light", seg=6)               # stylus
    it.stick((.2, -.06, .01), (.215, -.05, .01), .008, "black", seg=5)


@item("pen_display", "Pen display", "dept_creative", mount="table")
def pen_display(it):
    it.box((0, .08, .04), (.4, .08, .08), "charcoal", bevel=.015)                        # tilt stand
    it.box((0, 0, .11), (.52, .02, .34), "black", bevel=.015, rot=(-62, 0, 0))
    it.box((0, -.01, .113), (.46, .006, .28), "screen", bevel=0, rot=(-62, 0, 0), outline=False)
    it.ball((-.08, -.04, .13), (.12, .006, .08), "coral", seg=10, rot=(-62, 0, 0), outline=False)     # a drawing
    it.ball((.06, -.03, .12), (.08, .006, .06), "butter", seg=10, rot=(-62, 0, 0), outline=False)
    it.stick((.29, -.05, .012), (.29, .1, .012), .012, "white", seg=6)                   # pen


@item("art_supplies", "Art supplies", "dept_creative", mount="table")
def art_supplies(it):
    it.cyl((-.12, 0, .06), (.08, .08), .12, "glass", seg=12)                             # brush jar
    it.cyl((-.12, 0, .04), (.07, .07), .07, "sky", seg=12, outline=False)               # rinse water
    for k, c in enumerate(("wood_mid", "wood_dark", "wood_mid")):
        it.stick((-.13 + k * .01, 0, .05), (-.15 + k * .02, .01, .22), .01, c, seg=5)
        it.cyl((-.15 + k * .02, .01, .23), (.014, .014), .03, RAINBOW[k * 2], seg=5, top=.3)
    it.cyl((.06, 0, .006), (.18, .13), .012, "white", seg=16)                            # paint palette
    for k in range(5):
        x, y, _ = _polar(.055, 20 + k * 50)
        it.ball((.06 + x, y, .014), (.03, .03, .012), RAINBOW[k], seg=8, outline=False)
    for k in range(5):                                                                   # swatch fan
        it.box((.18 + k * .006, -.06, .004 + k * .003), (.04, .12, .003), RAINBOW[k + 1], bevel=0,
               rot=(0, 0, -20 + k * 12))


@item("sketchbook", "Sketchbook + pencils", "dept_creative", mount="table")
def sketchbook(it):
    for sx in (-1, 1):
        it.box((sx * .1, 0, .014), (.2, .26, .016), "paper", bevel=.004, rot=(0, sx * -3, 0))
    it.box((0, 0, .004), (.42, .27, .008), "charcoal", bevel=.004)                       # cover
    it.ball((-.1, .02, .024), (.12, .1, .002), "grey_light", seg=12, outline=False)     # sketch
    it.ball((-.1, .05, .025), (.05, .05, .002), "grey", seg=10, outline=False)
    it.box((.1, .03, .024), (.13, .004, .002), "grey", bevel=0, outline=False)
    it.box((.1, -.01, .024), (.1, .004, .002), "grey", bevel=0, outline=False)
    for k, c in enumerate(("coral", "sky", "sage", "butter")):
        it.stick((.24 + k * .025, -.1, .006), (.27 + k * .025, .08, .006), .012, c, seg=6)


@item("easel", "Painting easel", "dept_creative")
def easel(it):
    for sx in (-1, 1):
        it.stick((sx * .28, -.1, .012), (sx * .05, -.02, 1.65), .04, "wood_mid", seg=6)
    it.stick((0, .45, .012), (0, -.02, 1.6), .035, "wood_mid", seg=6)
    it.box((0, -.13, .7), (.6, .07, .03), "wood_mid", bevel=.01)                          # ledge
    it.box((0, -.1, 1.08), (.62, .03, .72), "white", bevel=.012, rot=(-6, 0, 0))         # canvas
    it.ball((-.12, -.125, 1.0), (.32, .01, .26), "sky", seg=12, rot=(-6, 0, 0), outline=False)
    it.ball((.12, -.127, 1.12), (.2, .01, .2), "butter", seg=12, rot=(-6, 0, 0), outline=False)
    it.ball((.05, -.13, .9), (.4, .01, .12), "sage", seg=12, rot=(-6, 0, 0), outline=False)


@item("mood_board", "Mood board", "dept_creative", mount="wall", mount_z=1.2)
def mood_board(it):
    it.box((0, -.015, .44), (1.0, .03, .8), "cork", bevel=.012)
    it.box((0, -.015, .44), (1.04, .028, .84), "wood_light", bevel=.01)
    for k, (x, z, w, h) in enumerate(((-.32, .58, .26, .2), (-.02, .6, .2, .24), (.28, .55, .28, .18),
                                      (-.3, .25, .2, .22), (0, .25, .22, .16), (.3, .24, .22, .26))):
        it.box((x, -.035, z), (w, .004, h), RAINBOW[k], bevel=0, rot=(0, (k % 3 - 1) * 3, 0), outline=False)
        it.ball((x, -.04, z + h / 2 - .02), (.02, .015, .02), "coral" if k % 2 else "blue", seg=6, outline=False)
    for k in range(5):                                                                   # palette chips
        it.box((-.2 + k * .1, -.035, .07), (.07, .004, .06), RAINBOW[k + 2], bevel=0, outline=False)


@item("art_figure", "Art mannequin", "dept_creative", mount="table")
def art_figure(it):
    it.cyl((0, 0, .008), (.1, .1), .016, "wood_dark", seg=12)
    it.stick((0, 0, .016), (0, 0, .06), .01, "metal", seg=5)
    it.ball((0, 0, .1), (.05, .035, .07), "wood_light", seg=8)                          # hips
    it.ball((0, 0, .16), (.06, .04, .08), "wood_light", seg=8)                          # chest
    it.ball((0, 0, .225), (.04, .04, .05), "wood_light", seg=8)                         # head
    it.stick((.03, 0, .18), (.07, -.02, .23), .018, "wood_light", seg=6)                # waving arm
    it.stick((-.03, 0, .18), (-.04, 0, .11), .018, "wood_light", seg=6)
    for sx in (-1, 1):
        it.stick((sx * .015, 0, .08), (sx * .025, 0, .025), .02, "wood_light", seg=6)


# =========================================================================== CONTENT / MEDIA
@item("ring_light", "Ring light", "dept_content")
def ring_light(it):
    _tripod(it, 1.4)
    _ring(it, (0, 0, 1.6), .2, .05, "lamp_glow", seg=18)
    _ring(it, (0, .01, 1.6), .2, .065, "white", seg=18)
    it.stick((0, 0, 1.4), (0, 0, 1.6), .02, "metal", seg=6)
    it.box((0, -.03, 1.6), (.07, .015, .13), "black", bevel=.01)                       # phone in the middle
    it.box((0, -.04, 1.6), (.06, .004, .11), "screen", bevel=0, outline=False)


@item("camera_tripod", "Camera on tripod", "dept_content")
def camera_tripod(it):
    _tripod(it, 1.35)
    it.box((0, 0, 1.38), (.1, .1, .04), "black", bevel=.01)                             # head
    it.box((0, 0, 1.47), (.16, .1, .12), "charcoal", bevel=.025)                         # body
    it.cyl((0, -.09, 1.46), (.08, .08), .1, "black", seg=14, rot=(90, 0, 0))            # lens
    it.cyl((0, -.141, 1.46), (.06, .06), .004, "glass", seg=14, rot=(90, 0, 0), outline=False)
    it.box((.05, 0, 1.54), (.04, .04, .03), "black", bevel=.008)
    it.ball((-.06, -.05, 1.5), (.015, .006, .015), "coral", seg=6, outline=False)      # REC light


@item("podcast_mic", "Podcast mic arm", "dept_content", mount="table")
def podcast_mic(it):
    it.box((0, .1, .02), (.08, .08, .04), "black", bevel=.01)                           # desk clamp
    it.stick((0, .1, .04), (0, .02, .3), .02, "black", seg=6)
    it.stick((0, .02, .3), (0, -.18, .26), .02, "black", seg=6)
    it.ball((0, .02, .3), (.03, .03, .03), "charcoal", seg=8)
    it.cyl((0, -.2, .2), (.07, .07), .14, "charcoal", seg=12)                            # mic body
    it.ball((0, -.2, .28), (.07, .07, .06), "grey", seg=10)
    _ring(it, (0, -.29, .24), .07, .012, "black", seg=12)                                # pop filter
    it.cyl((0, -.29, .24), (.13, .13), .003, "grey_light", seg=12, rot=(90, 0, 0), outline=False)


@item("softbox_light", "Softbox light", "dept_content")
def softbox_light(it):
    _tripod(it, 1.3)
    it.box((0, .05, 1.55), (.5, .3, .5), "black", bevel=.03, rot=(-10, 0, 0))
    it.box((0, -.105, 1.53), (.46, .02, .46), "lamp_glow", bevel=.01, rot=(-10, 0, 0))


@item("green_screen", "Green screen", "dept_content")
def green_screen(it):
    w = 1.8
    for sx in (-1, 1):
        for sy in (-1, 1):
            it.stick((sx * w / 2, sy * .25, .012), (sx * w / 2, 0, .4), .025, "charcoal", seg=6)
        it.cyl((sx * w / 2, 0, 1.1), (.035, .035), 1.4, "metal", seg=8)
    it.cyl((0, 0, 1.8), (.04, .04), w + .1, "metal", seg=8, rot=(0, 90, 0))
    it.box((0, .02, 1.15), (w - .04, .02, 1.3), "leaf", bevel=.01)
    it.box((0, -.2, .2), (w - .04, .5, .02), "leaf", bevel=.01, rot=(-25, 0, 0))        # sweep onto floor


@item("clapperboard", "Clapperboard", "dept_content", mount="table")
def clapperboard(it):
    it.box((0, 0, .008), (.24, .2, .016), "black", bevel=.004)
    for k in range(3):
        it.box((0, -.04 + k * .04, .017), (.2, .006, .002), "white", bevel=0, outline=False)
    it.box((0, .11, .03), (.24, .03, .02), "black", bevel=.004, rot=(-30, 0, 0))
    for k in range(5):
        it.box((-.1 + k * .05, .11, .041), (.025, .03, .002), "white", bevel=0, rot=(-30, 0, 30), outline=False)


@item("desk_camera", "Camera + lenses", "dept_content", mount="table")
def desk_camera(it):
    for i in range(3):                                                                   # mini tripod
        it.stick(_polar(.07, 90 + i * 120, .006), (0, 0, .09), .012, "black", seg=5)
    it.box((0, 0, .15), (.14, .08, .1), "charcoal", bevel=.02)
    it.cyl((0, -.07, .145), (.07, .07), .07, "black", seg=12, rot=(90, 0, 0))
    it.cyl((0, -.106, .145), (.05, .05), .004, "glass", seg=12, rot=(90, 0, 0), outline=False)
    for k, h in enumerate((.1, .07)):                                                    # spare lenses
        it.cyl((.14 + k * .08, .02, h / 2), (.065, .065), h, "black", seg=12)
        it.cyl((.14 + k * .08, .02, h + .001), (.05, .05), .003, "glass", seg=12, outline=False)
    it.box((-.15, 0, .01), (.06, .04, .02), "coral", bevel=.006)                         # SD card case


@item("headphone_stand", "Headphone stand", "dept_content", mount="table")
def headphone_stand(it):
    it.cyl((0, 0, .01), (.12, .12), .02, "wood_dark", seg=14)
    it.cyl((0, 0, .14), (.025, .025), .26, "wood_dark", seg=8)
    for i in range(9):   # headband over the hook
        deg = -80 + i * 20
        it.box((math.sin(math.radians(deg)) * .08, 0, .23 + math.cos(math.radians(deg)) * .06), (.03, .05, .02),
               "charcoal", bevel=.006, rot=(0, deg, 0))
    for sx in (-1, 1):
        it.cyl((sx * .085, 0, .2), (.08, .08), .04, "charcoal", seg=12, rot=(0, 90, 0), bevel=.01)
        it.cyl((sx * .107, 0, .2), (.05, .05), .004, "coral", seg=12, rot=(0, 90, 0), outline=False)


# =========================================================================== MARKETING
@item("rollup_banner", "Roll-up banner", "dept_marketing")
def rollup_banner(it):
    it.box((0, 0, .04), (.85, .2, .08), "grey", bevel=.03)
    it.stick((0, .03, .08), (0, .03, 2.0), .02, "metal", seg=6)
    it.box((0, -.02, 1.04), (.8, .01, 1.92), "white", bevel=.004)
    it.box((0, -.027, 1.75), (.8, .004, .4), "coral", bevel=0, outline=False)
    it.box((0, -.028, 1.7), (.5, .004, .08), "white", bevel=0, outline=False)
    it.ball((0, -.028, 1.15), (.4, .004, .4), "butter", seg=16, outline=False)
    it.box((0, -.028, .45), (.6, .004, .12), "blue", bevel=0, outline=False)


@item("brochure_stand", "Brochure stand", "dept_marketing")
def brochure_stand(it):
    it.box((0, .05, .02), (.36, .3, .04), "charcoal", bevel=.012)
    it.box((0, .08, .7), (.3, .03, 1.36), "metal", bevel=.01, rot=(-6, 0, 0))
    for k, c in enumerate(("sky", "coral", "sage", "butter")):
        z = .45 + k * .3
        it.box((0, .02 - (z - .7) * .1, z), (.28, .04, .03), "glass", bevel=0, rot=(-6, 0, 0))
        it.box((0, .03 - (z - .7) * .1, z + .1), (.22, .015, .22), c, bevel=0, rot=(-12, 0, 0))


@item("product_boxes", "Product samples", "dept_marketing", mount="table")
def product_boxes(it):
    for (x, y, z, w, h, c) in ((-.1, 0, 0, .16, .16, "coral"), (.08, .02, 0, .14, .1, "sky"),
                               (-.1, 0, .16, .12, .1, "butter"), (.08, .02, .1, .1, .06, "mint")):
        it.box((x, y, z + h / 2), (w, w * .8, h), c, bevel=.01)
        it.box((x, y - w * .4 - .002, z + h * .55), (w * .5, .004, h * .25), "white", bevel=0, outline=False)
    it.cyl((.2, 0, .07), (.06, .06), .14, "lavender", seg=12, top=.8)                  # sample bottle
    it.cyl((.2, 0, .16), (.03, .03), .04, "white", seg=8)


@item("chart_standee", "Growth chart", "dept_marketing", mount="table")
def chart_standee(it):
    it.box((0, .05, .1), (.03, .02, .2), "wood_mid", bevel=.004, rot=(20, 0, 0))
    it.box((0, 0, .12), (.3, .015, .22), "white", bevel=.008, rot=(-10, 0, 0))
    for k, h in enumerate((.05, .08, .11, .16)):                                        # rising bars
        z = .04 + h / 2
        it.box((-.09 + k * .06, -.012 + (z - .12) * .18, z), (.04, .004, h), RAINBOW[k], bevel=0,
               rot=(-10, 0, 0), outline=False)
    it.stick((-.11, -.02, .1), (.1, -.03, .2), .008, "coral", seg=4, outline=False)    # trend line


@item("megaphone", "Megaphone", "dept_marketing", mount="table")
def megaphone(it):
    it.cyl((0, -.03, .09), (.14, .14), .2, "coral", seg=14, top=.35, rot=(80, 0, 0))
    it.cyl((0, -.13, .09), (.12, .12), .004, "white", seg=14, rot=(80, 0, 0), outline=False)
    it.box((0, .06, .03), (.03, .05, .06), "charcoal", bevel=.01)                        # grip
    it.ball((.06, .05, .02), (.04, .04, .04), "butter", seg=8)                            # stress ball


@item("sticky_wall", "Sticky-note wall", "dept_marketing", mount="wall", mount_z=1.2)
def sticky_wall(it):
    it.box((0, -.01, .35), (1.2, .02, .7), "white", bevel=.01)
    for k in range(3):
        it.box((-.4 + k * .4, -.022, .65), (.3, .004, .05), "charcoal", bevel=0, outline=False)   # column heads
    for k in range(16):
        col, row = k % 3, k // 3
        if row > 4 or (col == 2 and row > 2):
            continue
        it.box((-.4 + col * .4 + (row % 2) * .04 - .02, -.024, .53 - row * .11), (.09, .004, .09),
               ("butter", "blush", "mint", "sky")[(k + col) % 4], bevel=0, rot=(0, (k % 3 - 1) * 4, 0),
               outline=False)


# =========================================================================== FINANCE
@item("calculator", "Printing calculator", "dept_finance", mount="table")
def calculator(it):
    it.box((0, 0, .03), (.18, .24, .04), "grey_light", bevel=.012, rot=(-6, 0, 0))
    it.box((0, .07, .053), (.14, .04, .004), "screen", bevel=0, outline=False)
    for r in range(4):
        for k in range(4):
            it.box((-.05 + k * .033, .02 - r * .033, .053), (.025, .024, .008),
                   "coral" if (k == 3 and r == 3) else "white", bevel=.003, outline=False)
    it.cyl((0, .14, .05), (.06, .06), .1, "paper", seg=10, rot=(0, 90, 0))              # receipt roll
    it.box((0, .1, .09), (.08, .06, .002), "paper", bevel=0, rot=(40, 0, 0))


@item("doc_tray", "Document tray", "dept_finance", mount="table")
def doc_tray(it):
    for k, c in enumerate(("sky", "blush", "sage")):
        z = .02 + k * .07
        it.box((0, 0, z), (.26, .34, .015), c, bevel=.005)
        for sx in (-1, 1):
            it.box((sx * .125, 0, z + .03), (.01, .34, .05), c, bevel=.003)
        for j in range(3):
            _paper(it, (.005 * j, -.01, z + .012 + j * .004), (.21, .29), rot=(0, 0, j * 3))


@item("binders", "Binder row", "dept_finance", mount="table")
def binders(it):
    for k in range(6):
        c = ("blue", "coral", "sage", "butter", "lavender", "charcoal")[k]
        it.box((-.18 + k * .07, 0, .16), (.06, .26, .32), c, bevel=.008)
        it.box((-.18 + k * .07, -.131, .2), (.04, .004, .08), "white", bevel=0, outline=False)
        it.cyl((-.18 + k * .07, -.131, .07), (.03, .03), .004, "white", seg=8, rot=(90, 0, 0), outline=False)
    it.box((.27, 0, .1), (.02, .2, .2), "metal", bevel=.004)                             # bookend
    it.box((.24, 0, .006), (.08, .2, .012), "metal", bevel=.003)


@item("piggy_bank", "Piggy bank", "dept_finance", mount="table")
def piggy_bank(it):
    it.ball((0, 0, .08), (.16, .12, .12), "blush", seg=14)
    it.cyl((0, -.08, .085), (.05, .05), .03, "blush", seg=10, rot=(90, 0, 0))
    for sx in (-1, 1):
        it.ball((sx * .012, -.096, .085), (.01, .004, .014), "coral", seg=6, outline=False)
        it.ball((sx * .035, -.04, .12), (.012, .008, .012), "black", seg=6, outline=False)
        it.cyl((sx * .035, -.02, .15), (.04, .02), .04, "blush", seg=6, top=.2)        # ears
        for sy in (-1, 1):
            it.cyl((sx * .05, sy * .04, .015), (.035, .035), .03, "blush", seg=8)
    it.box((0, .01, .14), (.04, .008, .004), "coral", bevel=0, outline=False)             # coin slot
    for k in range(3):
        it.cyl((.14, .0, .006 + k * .008), (.04, .04), .007, "butter", seg=10)          # coin stack


@item("safe_box", "Office safe", "dept_finance")
def safe_box(it):
    it.box((0, 0, .3), (.5, .5, .58), "charcoal", bevel=.03)
    it.box((0, -.252, .3), (.42, .01, .5), "grey", bevel=.008)
    it.cyl((-.05, -.27, .36), (.12, .12), .03, "metal", seg=16, rot=(90, 0, 0))         # dial
    it.box((-.05, -.29, .4), (.01, .004, .03), "coral", bevel=0, outline=False)
    it.stick((.12, -.27, .3), (.12, -.3, .3), .02, "metal", seg=6)                       # handle
    it.box((.12, -.3, .3), (.1, .02, .02), "metal", bevel=.006)
    for sx in (-1, 1):
        it.box((sx * .2, 0, .006), (.06, .44, .012), "black", bevel=0)


@item("shredder", "Paper shredder", "dept_finance")
def shredder(it):
    it.box((0, 0, .25), (.36, .26, .5), "grey_light", bevel=.025)
    it.box((0, -.131, .22), (.3, .01, .3), "glass", bevel=0, outline=False)             # bin window
    for k in range(8):
        it.box((-.1 + k * .03, -.134, .15 + (k % 3) * .03), (.008, .004, .1), "paper", bevel=0, outline=False)
    it.box((0, 0, .51), (.38, .28, .04), "charcoal", bevel=.012)
    it.box((0, .02, .532), (.24, .02, .006), "black", bevel=0, outline=False)            # slot
    it.box((.13, -.08, .532), (.04, .03, .006), "mint", bevel=0, outline=False)


# =========================================================================== HR / PEOPLE
@item("candy_jar", "Candy jar", "dept_hr", mount="table")
def candy_jar(it):
    it.cyl((0, 0, .09), (.16, .16), .18, "glass", seg=16, bevel=.02)
    for k in range(10):
        x, y, _ = _polar(.04 + (k % 2) * .025, k * 37)
        it.ball((x, y - .0, .04 + (k // 3) * .03), (.035, .035, .035), RAINBOW[k % 7], seg=8, outline=False)
    it.cyl((0, 0, .195), (.12, .12), .03, "coral", seg=14, bevel=.01)
    it.ball((0, 0, .22), (.04, .04, .03), "white", seg=8)


@item("name_plate", "Desk name plate", "dept_hr", mount="table")
def name_plate(it):
    it.box((0, .01, .01), (.26, .06, .02), "wood_dark", bevel=.006)
    it.box((0, 0, .045), (.24, .015, .06), "wood_light", bevel=.006, rot=(-12, 0, 0))
    it.box((0, -.01, .047), (.16, .004, .018), "charcoal", bevel=0, rot=(-12, 0, 0), outline=False)


@item("archive_boxes", "Archive boxes", "dept_hr")
def archive_boxes(it):
    for (x, z, c) in ((-.2, 0, "cork"), (.2, 0, "cork"), (0, .3, "cork")):
        it.box((x, 0, z + .14), (.38, .3, .28), c, bevel=.012)
        it.box((x, 0, z + .27), (.39, .31, .03), "wood_mid", bevel=.008)                 # lid
        it.box((x, -.151, z + .14), (.14, .004, .06), "white", bevel=0, outline=False)
        it.box((x, -.152, z + .2), (.08, .004, .02), "charcoal", bevel=0, outline=False)   # hand hole


@item("welcome_kit", "Welcome kit", "dept_hr", mount="table")
def welcome_kit(it):
    it.box((-.08, 0, .13), (.24, .08, .26), "sage", bevel=.02)                           # tote bag
    for sx in (-1, 1):
        it.stick((-.08 + sx * .06, 0, .26), (-.08 + sx * .02, 0, .33), .012, "sage", seg=5)
    it.stick((-.08 - .02, 0, .33), (-.08 + .02, 0, .33), .012, "sage", seg=5)
    it.ball((-.08, -.042, .14), (.08, .004, .08), "white", seg=10, outline=False)       # heart logo
    it.ball((-.08, -.046, .14), (.04, .004, .035), "coral", seg=8, outline=False)
    it.cyl((.12, 0, .05), (.08, .08), .1, "white", seg=12)                               # mug
    it.box((.12, -.06, .005), (.14, .1, .01), "lavender", bevel=.003)                    # notebook


@item("team_photo", "Team photo frame", "dept_hr", mount="table")
def team_photo(it):
    it.box((0, .03, .07), (.015, .02, .14), "wood_dark", bevel=.004, rot=(18, 0, 0))
    it.box((0, 0, .09), (.22, .02, .17), "wood_light", bevel=.008, rot=(-10, 0, 0))
    it.box((0, -.012, .09), (.18, .004, .13), "sky", bevel=0, rot=(-10, 0, 0), outline=False)
    for k in range(4):   # little people silhouettes
        x = -.06 + k * .04
        it.ball((x, -.017, .1 - k % 2 * .01), (.025, .004, .025), RAINBOW[k], seg=8, rot=(-10, 0, 0),
                outline=False)
        it.ball((x, -.016, .06), (.035, .004, .04), RAINBOW[k + 2], seg=8, rot=(-10, 0, 0), outline=False)


@item("suggestion_box", "Suggestion box", "dept_hr")
def suggestion_box(it):
    it.cyl((0, 0, .4), (.06, .06), .8, "metal", seg=8)
    it.cyl((0, 0, .015), (.3, .3), .03, "charcoal", seg=14, bevel=.01)
    it.box((0, 0, .95), (.32, .26, .3), "butter", bevel=.03)
    it.box((0, 0, 1.101), (.14, .02, .004), "black", bevel=0, outline=False)
    it.ball((0, -.131, .97), (.1, .004, .09), "coral", seg=12, outline=False)          # heart / idea badge
    it.ball((0, -.134, .97), (.05, .004, .05), "white", seg=10, outline=False)


# =========================================================================== SALES / SUPPORT
@item("headset_stand", "Headset on stand", "dept_sales", mount="table")
def headset_stand(it):
    it.place(fn("headphone_stand"))
    it.stick((.085, -.02, .18), (.04, -.1, .12), .01, "charcoal", seg=5)                # mic boom
    it.ball((.04, -.1, .12), (.025, .025, .025), "black", seg=8)


@item("call_bell", "Service bell", "dept_sales", mount="table")
def call_bell(it):
    it.cyl((0, 0, .01), (.12, .12), .02, "wood_dark", seg=14)
    it.ball((0, 0, .045), (.1, .1, .07), "butter", seg=14)
    it.cyl((0, 0, .085), (.012, .012), .02, "metal", seg=6)
    it.ball((0, 0, .098), (.025, .025, .012), "metal", seg=8)


@item("trophy", "Sales trophy", "dept_sales", mount="table")
def trophy(it):
    it.box((0, 0, .03), (.12, .12, .06), "wood_dark", bevel=.008)
    it.box((0, -.061, .03), (.07, .004, .02), "butter", bevel=0, outline=False)
    it.cyl((0, 0, .09), (.04, .04), .06, "butter", seg=10, top=.6)
    it.cyl((0, 0, .17), (.14, .14), .12, "butter", seg=14, top=1.4)                     # cup
    for sx in (-1, 1):
        _ring(it, (sx * .1, 0, .18), .03, .012, "butter", seg=8)
    it.ball((0, -.09, .18), (.04, .006, .04), "white", seg=8, outline=False)            # star badge


@item("sales_board", "Sales target board", "dept_sales", mount="wall", mount_z=1.3)
def sales_board(it):
    it.box((0, -.01, .3), (.9, .02, .6), "white", bevel=.01)
    it.box((0, -.022, .53), (.8, .004, .06), "coral", bevel=0, outline=False)
    for k, f in enumerate((.9, .65, .8, .45)):
        z = .4 - k * .1
        it.box((-.15, -.022, z), (.5, .004, .05), "grey_light", bevel=0, outline=False)
        it.box((-.4 + .25 * f, -.024, z), (.5 * f, .004, .05), RAINBOW[k + 2], bevel=0, outline=False)
        it.ball((-.35, -.026, z), (.03, .004, .03), RAINBOW[k], seg=8, outline=False)
    it.ball((.3, -.026, .3), (.18, .004, .18), "butter", seg=14, outline=False)          # goal badge
    it.ball((.3, -.028, .3), (.1, .004, .1), "white", seg=12, outline=False)


# =========================================================================== EXECUTIVE
@item("exec_desk", "Executive desk", "dept_exec")
def exec_desk(it):
    w, d, h = 1.8, .85, .76
    it.box((0, 0, h - .03), (w, d, .06), "wood_dark", bevel=.02)
    it.box((0, -.005, h - .062), (w - .04, d - .04, .01), "wood_mid", bevel=0, outline=False)
    for sx in (-1, 1):                                                                   # pedestals
        it.box((sx * (w / 2 - .25), 0, (h - .06) / 2), (.46, d - .06, h - .06), "wood_dark", bevel=.02)
        for z in (.18, .42, .6):
            it.box((sx * (w / 2 - .25), -d / 2 + .02, z), (.4, .02, .16 if z > .3 else .3), "wood_mid", bevel=.01)
            it.box((sx * (w / 2 - .25), -d / 2 + .005, z + .03), (.12, .02, .015), "butter", bevel=.004)
    it.box((0, d / 2 - .08, .45), (w - .96, .03, .5), "wood_mid", bevel=.01)           # modesty panel
    it.box((0, 0, h + .002), (.5, .34, .006), "charcoal", bevel=0, outline=False)       # leather desk pad


@item("exec_chair", "Executive chair", "dept_exec")
def exec_chair(it):
    _star_base(it, r=.32, m="wood_dark", wheel="black")
    it.cyl((0, 0, .25), (.06, .06), .3, "metal", seg=10)
    it.box((0, 0, .41), (.32, .32, .03), "black", bevel=.01)
    it.box((0, -.01, .47), (.56, .52, .11), "wood_dark", bevel=.045)                    # leather seat
    for k in range(3):
        it.box((0, .27, .76 + k * .17), (.5, .1, .16), "wood_dark", bevel=.05, rot=(-8, 0, 0))   # tufted rolls
    it.box((0, .3, .86), (.52, .06, .6), "black", bevel=.02, rot=(-8, 0, 0))
    for sx in (-1, 1):
        it.box((sx * .3, .02, .58), (.06, .44, .18), "wood_dark", bevel=.03)
        it.box((sx * .3, .02, .68), (.09, .46, .04), "wood_mid", bevel=.015)


@item("globe_stand", "Floor globe", "dept_exec")
def globe_stand(it):
    for i in range(3):
        it.stick(_polar(.22, 90 + i * 120, .012), (0, 0, .35), .035, "wood_dark", seg=6)
    it.cyl((0, 0, .4), (.06, .06), .12, "wood_dark", seg=10)
    it.ball((0, 0, .72), (.5, .5, .5), "sky", seg=18)
    for (a, z, s) in ((20, .82, .2), (140, .66, .16), (250, .78, .14), (300, .6, .1)):   # continents
        x, y, _ = _polar(.235, a)
        it.ball((x, y, z), (s, s, s * .7), "leaf", seg=8, outline=False)
    _ring(it, (0, 0, .72), .28, .025, "butter", seg=18)                                  # meridian ring
    it.cyl((0, 0, .72 - .3), (.03, .03), .06, "butter", seg=8)


@item("pen_stand", "Fountain pen stand", "dept_exec", mount="table")
def pen_stand(it):
    it.box((0, 0, .015), (.22, .1, .03), "wood_dark", bevel=.01)
    for sx in (-1, 1):
        it.cyl((sx * .05, .01, .04), (.025, .025), .02, "butter", seg=8)
        it.stick((sx * .05, .01, .04), (sx * .07, -.06, .16), .016, "black", seg=6)
        it.cyl((sx * .07 - sx * .002, -.066, .17), (.012, .012), .02, "butter", seg=6, top=.3)
    it.box((0, -.051, .015), (.08, .004, .015), "butter", bevel=0, outline=False)


@item("bonsai", "Bonsai", "dept_exec", mount="table")
def bonsai(it):
    it.box((0, 0, .03), (.24, .16, .06), "charcoal", bevel=.012)
    it.box((0, 0, .061), (.21, .13, .004), "soil", bevel=0, outline=False)
    it.stick((0, 0, .06), (.04, 0, .14), .03, "wood_dark", seg=6)
    it.stick((.04, 0, .14), (-.03, 0, .21), .025, "wood_dark", seg=6)
    for (x, z, s) in ((-.06, .22, .12), (.06, .18, .1), (-.01, .26, .1)):
        it.ball((x, 0, z), (s, s * .8, s * .55), "leaf_dark", seg=10)


# =========================================================================== WORKSTATIONS (one per role)
def _desk(it):
    it.place(fn("desk"))


@item("station_it", "IT / engineering desk", "station")
def station_it(it):
    _desk(it)
    it.place(fn("monitor_dual"), (0, .14, DESK_Z))
    it.place(fn("mech_keyboard"), (-.04, -.16, DESK_Z))
    it.place(fn("rubber_duck"), (-.5, -.12, DESK_Z), rz=25)
    it.place(fn("dev_board_kit"), (.48, -.1, DESK_Z), rz=-10)
    it.place(fn("pc_tower"), (-.45, .05, 0))


@item("station_creative", "Creative / design desk", "station")
def station_creative(it):
    _desk(it)
    it.place(fn("monitor"), (-.25, .17, DESK_Z), rz=10)
    it.place(fn("pen_display"), (.05, -.12, DESK_Z))
    it.place(fn("art_supplies"), (.5, .1, DESK_Z), rz=-15)
    it.place(fn("sketchbook"), (-.42, -.15, DESK_Z), rz=12)
    it.place(fn("art_figure"), (.22, .22, DESK_Z), rz=-30)
    it.place(fn("plant_small"), (.58, -.2, DESK_Z))


@item("station_content", "Content / media desk", "station")
def station_content(it):
    _desk(it)
    it.place(fn("monitor_ultrawide"), (0, .1, DESK_Z))
    it.place(fn("keyboard_mouse"), (-.12, -.2, DESK_Z))
    it.place(fn("podcast_mic"), (.42, -.02, DESK_Z), rz=-25)
    it.place(fn("desk_camera"), (-.52, -.12, DESK_Z), rz=20)
    it.place(fn("clapperboard"), (.35, -.22, DESK_Z), rz=-15)
    it.place(fn("headphone_stand"), (-.58, .2, DESK_Z), rz=30)


@item("station_marketing", "Marketing desk", "station")
def station_marketing(it):
    it.place(fn("l_desk"))
    it.place(fn("monitor"), (.1, .15, DESK_Z))
    it.place(fn("keyboard_mouse"), (.0, -.15, DESK_Z))
    it.place(fn("chart_standee"), (-.5, .12, DESK_Z), rz=15)
    it.place(fn("product_boxes"), (-.5, -.65, DESK_Z), rz=30)
    it.place(fn("megaphone"), (.6, -.1, DESK_Z), rz=-40)


@item("station_finance", "Finance desk", "station")
def station_finance(it):
    _desk(it)
    it.place(fn("monitor"), (-.12, .17, DESK_Z))
    it.place(fn("monitor_vertical"), (.32, .17, DESK_Z), rz=-15)
    it.place(fn("keyboard_mouse"), (-.15, -.17, DESK_Z))
    it.place(fn("calculator"), (.35, -.15, DESK_Z), rz=-10)
    it.place(fn("doc_tray"), (-.53, .05, DESK_Z), rz=8)
    it.place(fn("piggy_bank"), (.58, -.2, DESK_Z), rz=-30)


@item("station_hr", "HR / people desk", "station")
def station_hr(it):
    _desk(it)
    it.place(fn("all_in_one"), (0, .15, DESK_Z))
    it.place(fn("keyboard_mouse"), (-.1, -.16, DESK_Z))
    it.place(fn("candy_jar"), (.52, -.18, DESK_Z))
    it.place(fn("name_plate"), (.4, .29, DESK_Z), rz=180)                                # faces visitors (+Y)
    it.place(fn("team_photo"), (-.5, .1, DESK_Z), rz=20)
    it.place(fn("welcome_kit"), (.48, .15, DESK_Z), rz=-15)


@item("station_sales", "Sales / support desk", "station")
def station_sales(it):
    _desk(it)
    it.place(fn("monitor"), (-.05, .17, DESK_Z))
    it.place(fn("keyboard_mouse"), (-.1, -.16, DESK_Z))
    it.place(fn("headset_stand"), (-.5, .05, DESK_Z), rz=20)
    it.place(fn("desk_phone"), (.42, -.08, DESK_Z), rz=-15)
    it.place(fn("trophy"), (.55, .18, DESK_Z))
    it.place(fn("call_bell"), (-.55, -.22, DESK_Z))


@item("station_exec", "Executive desk set", "station")
def station_exec(it):
    it.place(fn("exec_desk"))
    it.place(fn("all_in_one"), (-.2, .18, .76))
    it.place(fn("keyboard_mouse"), (-.2, -.12, .76))
    it.place(fn("pen_stand"), (.35, -.15, .76))
    it.place(fn("bonsai"), (.65, .2, .76), rz=-20)
    it.place(fn("name_plate"), (.3, .36, .76), rz=180)
    it.place(fn("binders"), (-.62, .22, .76))
