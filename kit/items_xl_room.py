"""Kit v8, part 2: room building blocks -- architecture, lighting, facility, prayer room, lobby, outdoor.

Architecture pieces are the parts rooms get assembled from later: walls sit on a 1 m grid
(0.12 m thick, 2.8 m tall), centered on x, back face on y=+0.06 so two walls meet cleanly.
Ceiling lights are built hanging DOWN from z = their mount height (mount "ceiling", pivot at the top).
"""
import math

from items import BOOKS, _polar, item
from items_xl_furn import cushion, legs4, pedestal, top_slab

WALL_H, WALL_T = 2.8, .12


def wall(it, w, m="offwhite", h=WALL_H, skirting=True):
    it.box((0, 0, h / 2), (w, WALL_T, h), m, bevel=.004)
    if skirting:
        for sy in (-1, 1):
            it.box((0, sy * (WALL_T / 2 + .006), .05), (w, .012, .1), "wood_light", bevel=0, outline=False)


# =========================================================================== ARCHITECTURE
@item("wall_1m", "Wall 1 m", "architecture")
def wall_1m(it):
    wall(it, 1.0)


@item("wall_2m", "Wall 2 m", "architecture")
def wall_2m(it):
    wall(it, 2.0)


@item("wall_half", "Half-height wall", "architecture")
def wall_half(it):
    wall(it, 2.0, h=1.1)
    it.box((0, 0, 1.12), (2.04, .2, .04), "wood_mid", bevel=.008)


@item("wall_corner", "Wall corner", "architecture")
def wall_corner(it):
    it.box((0, 0, WALL_H / 2), (1.0, WALL_T, WALL_H), "offwhite", bevel=.004)
    it.box((.44, -.44, WALL_H / 2), (WALL_T, 1.0, WALL_H), "offwhite", bevel=.004)
    it.box((.44, 0, .05), (WALL_T + .03, WALL_T + .03, .1), "wood_light", bevel=0, outline=False)


@item("wall_accent_slats", "Accent wall (wood slats)", "architecture")
def wall_accent_slats(it):
    wall(it, 2.0, "sage", skirting=False)
    for i in range(16):
        it.box((-.94 + i * .125, -.075, WALL_H / 2), (.06, .03, WALL_H - .1), "wood_mid", bevel=0)


@item("wall_brick", "Brick accent wall", "architecture")
def wall_brick(it):
    wall(it, 2.0, "peach", skirting=False)
    for r in range(14):
        for c in range(8):
            x = -.94 + c * .25 + (.125 if r % 2 else 0)
            if x > .9:
                continue
            it.box((x, -.065, .1 + r * .19), (.23, .012, .16), "coral", bevel=0, outline=False)


@item("wall_window", "Wall with window", "architecture")
def wall_window(it):
    it.box((0, 0, .45), (2.0, WALL_T, .9), "offwhite", bevel=.004)
    it.box((0, 0, 2.55), (2.0, WALL_T, .5), "offwhite", bevel=.004)
    for sx in (-1, 1):
        it.box((sx * .9, 0, 1.65), (.2, WALL_T, 1.4), "offwhite", bevel=.004)
    it.box((0, 0, 1.65), (1.6, .02, 1.4), "glass", bevel=0)
    it.box((0, -.02, 1.65), (.04, .06, 1.4), "white", bevel=0)
    it.box((0, -.1, .9), (1.7, .16, .04), "white", bevel=.006)


@item("wall_door_frame", "Wall with door opening", "architecture")
def wall_door_frame(it):
    for sx in (-1, 1):
        it.box((sx * .75, 0, WALL_H / 2), (.5, WALL_T, WALL_H), "offwhite", bevel=.004)
    it.box((0, 0, 2.45), (1.0, WALL_T, .7), "offwhite", bevel=.004)
    for sx in (-1, 1):
        it.box((sx * .5, 0, 1.05), (.04, WALL_T + .03, 2.1), "wood_light", bevel=.004)
    it.box((0, 0, 2.12), (1.04, WALL_T + .03, .04), "wood_light", bevel=.004)


@item("partition_glass", "Glass partition", "architecture")
def partition_glass(it):
    it.box((0, 0, .03), (2.0, .08, .06), "charcoal", bevel=.004)
    it.box((0, 0, 2.77), (2.0, .08, .06), "charcoal", bevel=.004)
    for sx in (-1, 0, 1):
        it.box((sx * .98, 0, 1.4), (.04, .08, 2.7), "charcoal", bevel=0)
    it.box((0, 0, 1.4), (1.96, .015, 2.68), "glass", bevel=0)
    it.box((0, -.01, 1.1), (1.9, .004, .08), "white", bevel=0, outline=False)    # frosted band


@item("door_single", "Door", "architecture")
def door_single(it):
    for sx in (-1, 1):
        it.box((sx * .47, 0, 1.06), (.06, .14, 2.12), "wood_light", bevel=.006)
    it.box((0, 0, 2.15), (1.0, .14, .06), "wood_light", bevel=.006)
    it.box((0, 0, 1.05), (.86, .04, 2.08), "wood_mid", bevel=.006)
    it.box((0, -.025, 1.5), (.6, .01, .7), "wood_light", bevel=0, outline=False)
    it.box((0, -.025, .55), (.6, .01, .6), "wood_light", bevel=0, outline=False)
    it.ball((.34, -.05, 1.0), (.05, .05, .05), "metal", seg=8)


@item("door_double_glass", "Double glass door", "architecture")
def door_double_glass(it):
    for sx in (-1, 1):
        it.box((sx * .92, 0, 1.1), (.06, .14, 2.2), "charcoal", bevel=.004)
        it.box((sx * .45, 0, 1.08), (.86, .05, 2.14), "glass", bevel=0)
        it.box((sx * .45, 0, 1.08), (.86, .055, .04), "charcoal", bevel=0, outline=False)
        it.box((sx * .06, -.06, 1.05), (.03, .03, .7), "metal", bevel=0)
    it.box((0, 0, 2.22), (1.9, .14, .06), "charcoal", bevel=.004)


@item("door_sliding_barn", "Sliding barn door", "architecture")
def door_sliding_barn(it):
    it.box((0, -.03, 2.2), (2.0, .04, .06), "black", bevel=0)
    for i in range(6):
        it.box((-.42 + i * .17, -.08, 1.06), (.16, .04, 2.06), "wood_mid", bevel=.004)
    for z in (.4, 1.7):
        it.box((0, -.105, z), (1.0, .01, .1), "wood_dark", bevel=0)
    it.box((0, -.105, 1.05), (1.15, .01, .1), "wood_dark", bevel=0, rot=(0, 52, 0))
    for sx in (-1, 1):
        it.cyl((sx * .35, -.06, 2.2), (.1, .1), .02, "black", seg=10, rot=(90, 0, 0))
    it.box((-.38, -.12, 1.0), (.03, .03, .3), "black", bevel=0)


@item("window_tall", "Tall window", "architecture", mount="wall", mount_z=.5)
def window_tall(it):
    it.box((0, -.04, 1.0), (1.0, .08, 2.0), "white", bevel=.006)
    it.box((0, -.08, 1.0), (.9, .01, 1.9), "glass", bevel=0, outline=False)
    it.box((0, -.09, 1.0), (.04, .02, 1.9), "white", bevel=0)
    it.box((0, -.09, 1.3), (.9, .02, .04), "white", bevel=0)


@item("window_round", "Round window", "architecture", mount="wall", mount_z=1.2)
def window_round(it):
    it.cyl((0, -.04, .4), (.8, .8), .08, "white", seg=24, rot=(90, 0, 0))
    it.cyl((0, -.08, .4), (.7, .7), .01, "glass", seg=24, rot=(90, 0, 0), outline=False)
    it.box((0, -.09, .4), (.7, .02, .03), "white", bevel=0)
    it.box((0, -.09, .4), (.03, .02, .7), "white", bevel=0)


@item("window_blinds", "Window with blinds", "architecture", mount="wall", mount_z=.9)
def window_blinds(it):
    it.box((0, -.04, .7), (1.4, .08, 1.4), "white", bevel=.006)
    it.box((0, -.08, .7), (1.3, .01, 1.3), "glass", bevel=0, outline=False)
    for i in range(10):
        it.box((0, -.1, 1.3 - i * .07), (1.32, .03, .015), "offwhite", bevel=0, rot=(25, 0, 0))
    it.stick((.6, -.12, 1.35), (.6, -.12, .7), .008, "grey", seg=4)


@item("column_round", "Round column", "architecture")
def column_round(it):
    it.cyl((0, 0, 1.4), (.4, .4), 2.8, "offwhite", seg=20)
    for z in (.05, 2.75):
        it.cyl((0, 0, z), (.48, .48), .1, "white", seg=20, bevel=.01)


@item("column_square", "Square column", "architecture")
def column_square(it):
    it.box((0, 0, 1.4), (.45, .45, 2.8), "offwhite", bevel=.008)
    it.box((0, 0, .05), (.49, .49, .1), "wood_light", bevel=0, outline=False)


@item("stairs_straight", "Stairs (straight)", "architecture")
def stairs_straight(it):
    for i in range(8):
        it.box((0, -.7 + i * .25, .1 + i * .18), (1.0, .27, .2 + i * 0), "wood_light", bevel=.006)
        it.box((0, -.7 + i * .25, (.1 + i * .18) / 2), (1.0, .25, .1 + i * .18), "offwhite", bevel=0)
    for sx in (-1, 1):
        it.stick((sx * .48, -.8, 1.0), (sx * .48, 1.1, 2.3), .04, "charcoal", seg=6)
        it.stick((sx * .48, -.8, .1), (sx * .48, -.8, 1.0), .03, "charcoal", seg=6)
        it.stick((sx * .48, 1.1, 1.4), (sx * .48, 1.1, 2.3), .03, "charcoal", seg=6)


@item("railing_glass", "Glass railing", "architecture")
def railing_glass(it):
    it.box((0, 0, .02), (2.0, .08, .04), "metal", bevel=0)
    it.box((0, 0, .5), (1.96, .02, .9), "glass", bevel=0)
    it.box((0, 0, 1.0), (2.0, .06, .05), "wood_mid", bevel=.01)


@item("floor_tile_wood", "Floor tile 1 m (wood)", "architecture")
def floor_tile_wood(it):
    for i in range(5):
        it.box((0, -.4 + i * .2, .01), (1.0, .195, .02), ("wood_light", "wood_mid")[i % 2], bevel=0)


@item("floor_tile_carpet", "Floor tile 1 m (carpet)", "architecture")
def floor_tile_carpet(it):
    it.box((0, 0, .01), (1.0, 1.0, .02), "grey_light", bevel=0)
    for i in range(4):
        it.box((-.375 + i * .25, 0, .021), (.02, 1.0, .002), "grey", bevel=0, outline=False)


@item("floor_tile_terrazzo", "Floor tile 1 m (terrazzo)", "architecture")
def floor_tile_terrazzo(it):
    it.box((0, 0, .01), (1.0, 1.0, .02), "offwhite", bevel=0)
    for i in range(14):
        x, y = ((i * 37) % 90) / 100 - .45, ((i * 53) % 90) / 100 - .45
        it.box((x, y, .021), (.04, .03, .002), BOOKS[i % 7], bevel=0, outline=False, rot=(0, 0, i * 25))


@item("ceiling_tile", "Ceiling panel 1 m", "architecture", mount="ceiling", mount_z=2.8)
def ceiling_tile(it):
    it.box((0, 0, -.015), (1.0, 1.0, .03), "white", bevel=0)
    it.box((0, 0, -.032), (.6, .6, .004), "lamp_glow", bevel=0, outline=False)


@item("baseboard_heater", "Air conditioner (floor)", "architecture")
def baseboard_heater(it):
    it.box((0, 0, .9), (.45, .35, 1.8), "white", bevel=.03)
    for i in range(6):
        it.box((0, -.18, 1.3 + i * .06), (.36, .01, .02), "grey_light", bevel=0, outline=False)
    it.box((0, -.18, .8), (.12, .01, .08), "screen", bevel=0, outline=False)


@item("pillar_planter", "Column with planter ring", "architecture")
def pillar_planter(it):
    it.box((0, 0, 1.4), (.4, .4, 2.8), "offwhite", bevel=.008)
    it.cyl((0, 0, .25), (1.0, 1.0), .5, "wood_light", seg=20, bevel=.02)
    for i in range(10):
        x, y, _ = _polar(.38, i * 36)
        it.ball((x, y, .6), (.22, .22, .24), "leaf" if i % 2 else "leaf_dark", seg=8)


# =========================================================================== LIGHTING
@item("pendant_dome", "Dome pendant", "lighting", mount="ceiling", mount_z=2.8)
def pendant_dome(it):
    it.stick((0, 0, 0), (0, 0, -.9), .01, "black", seg=4)
    it.cyl((0, 0, -.02), (.12, .12), .04, "black", seg=10)
    it.ball((0, 0, -1.0), (.5, .5, .36), "sage", seg=16)
    it.cyl((0, 0, -1.1), (.4, .4), .02, "lamp_glow", seg=16, outline=False)


@item("pendant_cone", "Cone pendant", "lighting", mount="ceiling", mount_z=2.8)
def pendant_cone(it):
    it.stick((0, 0, 0), (0, 0, -.8), .01, "black", seg=4)
    it.cyl((0, 0, -.95), (.35, .35), .3, "coral", seg=16, top=.25)
    it.cyl((0, 0, -1.1), (.3, .3), .01, "lamp_glow", seg=16, outline=False)


@item("pendant_cluster", "Globe cluster pendant", "lighting", mount="ceiling", mount_z=2.8)
def pendant_cluster(it):
    it.cyl((0, 0, -.02), (.3, .3), .04, "black", seg=12)
    for i, (r, deg, dz) in enumerate(((.1, 0, .6), (.12, 120, .9), (.11, 240, .75), (0, 0, 1.05))):
        x, y, _ = _polar(r, deg)
        it.stick((x, y, 0), (x, y, -dz), .008, "black", seg=4)
        it.ball((x, y, -dz - .08), (.16, .16, .16), "lamp_glow", seg=10)


@item("pendant_linear", "Linear pendant", "lighting", mount="ceiling", mount_z=2.8)
def pendant_linear(it):
    for sx in (-1, 1):
        it.stick((sx * .6, 0, 0), (sx * .6, 0, -.7), .008, "metal", seg=4)
    it.box((0, 0, -.73), (1.4, .08, .05), "charcoal", bevel=.01)
    it.box((0, 0, -.757), (1.36, .06, .005), "lamp_glow", bevel=0, outline=False)


@item("ceiling_panel_light", "Ceiling panel light", "lighting", mount="ceiling", mount_z=2.8)
def ceiling_panel_light(it):
    it.box((0, 0, -.02), (.6, .6, .04), "white", bevel=.006)
    it.box((0, 0, -.042), (.54, .54, .005), "lamp_glow", bevel=0, outline=False)


@item("track_light", "Track spotlights", "lighting", mount="ceiling", mount_z=2.8)
def track_light(it):
    it.box((0, 0, -.02), (1.5, .05, .04), "black", bevel=0)
    for i in range(4):
        x = -.55 + i * .37
        it.stick((x, 0, -.04), (x, -.03, -.12), .015, "black", seg=4)
        it.cyl((x, -.06, -.17), (.08, .08), .14, "black", seg=10, rot=(30, 0, 0))


@item("ceiling_fan", "Ceiling fan", "lighting", mount="ceiling", mount_z=2.8)
def ceiling_fan(it):
    it.stick((0, 0, 0), (0, 0, -.35), .03, "wood_dark", seg=6)
    it.cyl((0, 0, -.4), (.2, .2), .1, "wood_dark", seg=12)
    for i in range(4):
        x, y, _ = _polar(.4, i * 90)
        it.box((x, y, -.42), (.6, .14, .015), "wood_mid", bevel=.004, rot=(0, 0, i * 90))
    it.ball((0, 0, -.5), (.14, .14, .1), "lamp_glow", seg=10)


@item("chandelier_ring", "Ring chandelier", "lighting", mount="ceiling", mount_z=2.8)
def chandelier_ring(it):
    for i in range(3):
        x, y, _ = _polar(.35, 90 + i * 120)
        it.stick((0, 0, 0), (x, y, -.8), .008, "metal", seg=4)
    for i in range(16):
        a0, a1 = i * 22.5, (i + 1) * 22.5
        it.stick(_polar(.42, a0, -.82), _polar(.42, a1, -.82), .04, "butter", seg=5)
    for i in range(8):
        it.ball(_polar(.42, i * 45, -.88), (.06, .06, .06), "lamp_glow", seg=6)


@item("wall_sconce", "Wall sconce", "lighting", mount="wall", mount_z=1.7)
def wall_sconce(it):
    it.cyl((0, -.01, 0), (.1, .1), .02, "black", seg=10, rot=(90, 0, 0))
    it.stick((0, -.02, 0), (0, -.12, .05), .015, "black", seg=4)
    it.cyl((0, -.14, .1), (.14, .14), .14, "butter", seg=12, top=.7)
    it.ball((0, -.14, .06), (.06, .06, .06), "lamp_glow", seg=6)


@item("desk_lamp_arch", "Arched desk lamp", "lighting")
def desk_lamp_arch(it):
    it.cyl((0, .1, .015), (.14, .14), .03, "white", seg=12, bevel=.006)
    pts = [(0, .1 - .22 * (1 - math.cos(math.radians(a))), .03 + .4 * math.sin(math.radians(a))) for a in range(0, 91, 15)]
    for p0, p1 in zip(pts, pts[1:]):
        it.stick(p0, p1, .015, "white", seg=4)
    it.ball((0, -.12, .38), (.14, .14, .09), "white", seg=10)
    it.cyl((0, -.12, .335), (.1, .1), .005, "lamp_glow", seg=10, outline=False)


@item("desk_lamp_mushroom", "Mushroom table lamp", "lighting")
def desk_lamp_mushroom(it):
    it.cyl((0, 0, .1), (.12, .12), .2, "butter", seg=12, top=.8)
    it.ball((0, 0, .24), (.3, .3, .2), "butter", seg=14)
    it.cyl((0, 0, .17), (.26, .26), .01, "lamp_glow", seg=14, outline=False)


@item("table_lamp_ceramic", "Ceramic table lamp", "lighting")
def table_lamp_ceramic(it):
    it.ball((0, 0, .14), (.2, .2, .26), "sky", seg=12)
    it.stick((0, 0, .26), (0, 0, .36), .015, "metal", seg=4)
    it.cyl((0, 0, .45), (.3, .3), .22, "offwhite", seg=14, top=.75)


@item("floor_lamp_arc", "Arc floor lamp", "lighting")
def floor_lamp_arc(it):
    it.cyl((-.5, 0, .04), (.3, .3), .08, "charcoal", seg=14, bevel=.01)
    pts = [(-.5 + math.sin(math.radians(a)) * .6 * (1 if a < 90 else 1), 0,
            .08 + math.sin(math.radians(min(a, 90))) * 1.6 + (0 if a < 90 else -math.sin(math.radians(a - 90)) * .3))
           for a in range(0, 151, 25)]
    for p0, p1 in zip(pts, pts[1:]):
        it.stick(p0, p1, .025, "metal", seg=5)
    it.ball((pts[-1][0], 0, pts[-1][2] - .12), (.3, .3, .2), "white", seg=12)


@item("floor_lamp_tripod", "Tripod floor lamp", "lighting")
def floor_lamp_tripod(it):
    for deg in (90, 210, 330):
        it.stick(_polar(.3, deg, 0), (0, 0, 1.15), .03, "wood_mid", seg=5)
    it.cyl((0, 0, 1.35), (.45, .45), .35, "offwhite", seg=16, top=.85)


@item("floor_lamp_paper", "Paper lantern floor lamp", "lighting")
def floor_lamp_paper(it):
    it.cyl((0, 0, .02), (.25, .25), .04, "wood_mid", seg=12)
    it.stick((0, 0, .04), (0, 0, .3), .02, "wood_mid", seg=4)
    it.cyl((0, 0, .8), (.36, .36), 1.0, "paper", seg=16, bevel=.04)
    for i in range(5):
        it.cyl((0, 0, .35 + i * .22), (.37, .37), .01, "wood_light", seg=16, outline=False)


@item("lantern_floor", "Floor lantern", "lighting")
def lantern_floor(it):
    it.box((0, 0, .3), (.3, .3, .5), "black", bevel=.008)
    it.box((0, 0, .3), (.26, .32, .44), "lamp_glow", bevel=0, outline=False)
    it.box((0, 0, .3), (.32, .26, .44), "lamp_glow", bevel=0, outline=False)
    it.cyl((0, 0, .6), (.36, .36), .1, "black", seg=4, top=.3, rot=(0, 0, 45))
    it.cyl((0, 0, .03), (.34, .34), .06, "black", seg=4, rot=(0, 0, 45))


@item("neon_sign_wall", "Neon sign (wave)", "lighting", mount="wall", mount_z=1.6)
def neon_sign_wall(it):
    it.box((0, -.01, 0), (.9, .02, .4), "glass", bevel=0)
    pts = [(-.35 + i * .07, -.04, math.sin(i * .9) * .1) for i in range(11)]
    for p0, p1 in zip(pts, pts[1:]):
        it.stick(p0, p1, .025, "blush", seg=5)


@item("string_lights", "String lights", "lighting", mount="wall", mount_z=2.2)
def string_lights(it):
    pts = [(-1 + i * .2, -.05, -abs(math.sin(i * math.pi / 5)) * .2) for i in range(11)]
    for i, (p0, p1) in enumerate(zip(pts, pts[1:])):
        it.stick(p0, p1, .008, "charcoal", seg=4)
        it.ball((p0[0] + .1, -.05, (p0[2] + p1[2]) / 2 - .04), (.05, .05, .07), "lamp_glow", seg=6)


@item("light_uplight", "Uplight column", "lighting")
def light_uplight(it):
    it.cyl((0, 0, .5), (.16, .16), 1.0, "white", seg=4, rot=(0, 0, 45))
    it.cyl((0, 0, 1.02), (.15, .15), .02, "lamp_glow", seg=4, rot=(0, 0, 45), outline=False)


@item("spotlight_floor", "Floor spotlight", "lighting")
def spotlight_floor(it):
    it.cyl((0, 0, .02), (.2, .2), .04, "black", seg=10)
    it.stick((0, 0, .04), (0, 0, .25), .02, "black", seg=4)
    it.cyl((0, -.03, .3), (.16, .16), .2, "black", seg=12, rot=(60, 0, 0))
    it.cyl((0, -.12, .35), (.13, .13), .01, "lamp_glow", seg=12, rot=(60, 0, 0), outline=False)


# =========================================================================== FACILITY
@item("fire_extinguisher", "Fire extinguisher", "facility")
def fire_extinguisher(it):
    it.cyl((0, 0, .25), (.16, .16), .45, "coral", seg=12, bevel=.04)
    it.cyl((0, 0, .5), (.05, .05), .06, "black", seg=8)
    it.box((0, -.03, .55), (.12, .03, .03), "black", bevel=0)
    it.stick((.05, 0, .52), (.1, -.06, .3), .015, "black", seg=4)
    it.box((0, -.08, .25), (.08, .005, .1), "white", bevel=0, outline=False)


@item("first_aid_box", "First-aid box", "facility", mount="wall", mount_z=1.4)
def first_aid_box(it):
    it.box((0, -.06, 0), (.36, .12, .3), "white", bevel=.012)
    it.box((0, -.122, 0), (.14, .004, .04), "coral", bevel=0, outline=False)
    it.box((0, -.122, 0), (.04, .004, .14), "coral", bevel=0, outline=False)


@item("exit_sign", "Exit sign", "facility", mount="wall", mount_z=2.3)
def exit_sign(it):
    it.box((0, -.03, 0), (.36, .06, .16), "white", bevel=.006)
    it.box((0, -.062, 0), (.32, .004, .12), "leaf", bevel=0, outline=False)
    it.box((-.08, -.065, 0), (.07, .004, .07), "white", bevel=0, outline=False)


@item("nap_pod", "Nap pod", "facility")
def nap_pod(it):
    it.box((0, .1, .2), (.9, 1.9, .4), "white", bevel=.04)
    cushion(it, (0, .1, .45), (.8, 1.8, .12), "sky")
    it.ball((0, .7, .8), (1.0, .9, 1.0), "white", seg=16)
    it.ball((0, .6, .75), (.8, .8, .8), "lavender", seg=14)
    it.box((0, .8, .55), (.5, .25, .1), "offwhite", bevel=.04)


@item("massage_chair", "Massage chair", "facility")
def massage_chair(it):
    it.box((0, 0, .25), (.75, .9, .4), "charcoal", bevel=.04)
    cushion(it, (0, -.05, .5), (.55, .6, .12), "wood_mid")
    it.box((0, .38, .95), (.6, .3, .9), "charcoal", bevel=.06, rot=(-18, 0, 0))
    cushion(it, (0, .28, .9), (.48, .1, .7), "wood_mid", bevel=.03)
    for sx in (-1, 1):
        it.box((sx * .33, 0, .6), (.14, .7, .3), "charcoal", bevel=.04)
    it.box((0, -.55, .2), (.45, .35, .35), "charcoal", bevel=.04, rot=(-25, 0, 0))


@item("treadmill", "Treadmill", "facility")
def treadmill(it):
    it.box((0, 0, .12), (.75, 1.8, .2), "charcoal", bevel=.03)
    it.box((0, 0, .225), (.55, 1.6, .02), "black", bevel=0, outline=False)
    for sx in (-1, 1):
        it.stick((sx * .33, -.7, .2), (sx * .3, -.8, 1.2), .05, "grey", seg=6)
    it.box((0, -.82, 1.25), (.7, .25, .12), "grey", bevel=.03, rot=(30, 0, 0))
    it.box((0, -.84, 1.3), (.3, .01, .1), "screen", bevel=0, outline=False, rot=(30, 0, 0))


@item("exercise_bike", "Exercise bike", "facility")
def exercise_bike(it):
    it.box((0, 0, .03), (.5, 1.0, .06), "charcoal", bevel=.01)
    it.cyl((0, -.35, .3), (.08, .5), .5, "charcoal", seg=14, rot=(0, 90, 0))
    it.stick((0, .2, .06), (0, .1, .8), .06, "grey", seg=6)
    it.stick((0, -.3, .5), (0, -.35, 1.05), .05, "grey", seg=6)
    it.box((0, .08, .84), (.2, .3, .06), "black", bevel=.02)
    it.box((0, -.38, 1.08), (.45, .06, .04), "black", bevel=.01)


@item("dumbbell_rack", "Dumbbell rack", "facility")
def dumbbell_rack(it):
    for sx in (-1, 1):
        it.box((sx * .5, 0, .35), (.05, .4, .7), "charcoal", bevel=0)
    for k, z in enumerate((.3, .6)):
        it.box((0, 0, z), (1.0, .35, .03), "grey", bevel=0, rot=(-10, 0, 0))
        for i in range(4):
            x = -.36 + i * .24
            for sx in (-1, 1):
                it.cyl((x + sx * .06, -.02, z + .05), (.08, .08), .04, BOOKS[(i + k) % 7], seg=10, rot=(0, 90, 0))
            it.stick((x - .06, -.02, z + .05), (x + .06, -.02, z + .05), .025, "metal", seg=4)


@item("yoga_mats", "Yoga mats in basket", "facility")
def yoga_mats(it):
    it.cyl((0, 0, .2), (.4, .4), .4, "cork", seg=14)
    for i, m in enumerate(("mint", "lavender", "coral", "sky")):
        x, y, _ = _polar(.09, i * 90)
        it.cyl((x, y, .45), (.13, .13), .62, m, seg=10, rot=((i - 1.5) * 4, (i % 2) * 6 - 3, 0))


@item("bike_rack", "Bike rack", "facility")
def bike_rack(it):
    for i in range(4):
        x = -.6 + i * .4
        it.stick((x, -.15, 0), (x, -.15, .6), .04, "metal", seg=6)
        it.stick((x, .15, 0), (x, .15, .6), .04, "metal", seg=6)
        it.stick((x, -.15, .6), (x, .15, .6), .04, "metal", seg=6)
    it.box((0, 0, .02), (1.5, .4, .04), "grey", bevel=.006)


@item("scooter_kick", "Kick scooter", "facility")
def scooter_kick(it):
    it.box((0, 0, .08), (.12, .7, .03), "black", bevel=.006)
    for sy in (-1, 1):
        it.cyl((0, sy * .35, .06), (.12, .12), .04, "charcoal", seg=10, rot=(0, 90, 0))
    it.stick((0, -.35, .1), (0, -.3, .95), .03, "coral", seg=6)
    it.stick((-.2, -.3, .95), (.2, -.3, .95), .03, "black", seg=5)


@item("cleaning_cart", "Cleaning cart", "facility")
def cleaning_cart(it):
    it.box((0, 0, .5), (.9, .45, .8), "butter", bevel=.01)
    it.cyl((.25, 0, .95), (.35, .35), .25, "sky", seg=12)
    it.stick((-.3, 0, .9), (-.3, .05, 1.5), .03, "wood_mid", seg=5)
    it.box((-.3, .05, .92), (.18, .1, .05), "blue", bevel=.02)
    for sx in (-1, 1):
        for sy in (-1, 1):
            it.cyl((sx * .38, sy * .18, .04), (.07, .07), .03, "black", seg=8, rot=(0, 90, 0))


@item("wet_floor_sign", "Wet floor sign", "facility")
def wet_floor_sign(it):
    for sy in (-1, 1):
        it.box((0, sy * .1, .32), (.3, .02, .62), "butter", bevel=.006, rot=(sy * 12, 0, 0))
        it.box((0, sy * .118, .38), (.14, .004, .14), "charcoal", bevel=0, outline=False, rot=(sy * 12, 0, 0))


@item("robot_vacuum", "Robot vacuum", "facility")
def robot_vacuum(it):
    it.cyl((0, 0, .045), (.34, .34), .09, "white", seg=20, bevel=.02)
    it.cyl((0, -.06, .095), (.08, .08), .01, "charcoal", seg=10, outline=False)
    it.box((0, -.16, .05), (.2, .02, .05), "charcoal", bevel=0, outline=False)


@item("air_purifier", "Air purifier", "facility")
def air_purifier(it):
    it.box((0, 0, .35), (.3, .3, .7), "white", bevel=.06)
    it.cyl((0, 0, .7), (.24, .24), .01, "grey", seg=14, outline=False)
    for i in range(6):
        it.box((0, -.152, .15 + i * .07), (.2, .004, .02), "grey_light", bevel=0, outline=False)
    it.ball((0, -.152, .6), (.04, .01, .04), "leaf", seg=6, outline=False)


@item("humidifier", "Humidifier", "facility")
def humidifier(it):
    it.cyl((0, 0, .12), (.2, .2), .24, "mint", seg=14, bevel=.03)
    it.ball((0, 0, .25), (.16, .16, .1), "white", seg=10)
    it.ball((0, 0, .36), (.08, .08, .14), "water", seg=8)


@item("recycle_station", "Recycling station", "facility")
def recycle_station(it):
    for i, m in enumerate(("sky", "butter", "leaf", "grey")):
        x = -.54 + i * .36
        it.box((x, 0, .38), (.34, .4, .76), m, bevel=.02)
        it.box((x, -.05, .77), (.2, .2, .02), "black", bevel=0, outline=False)
        it.box((x, -.205, .5), (.14, .004, .14), "white", bevel=0, outline=False)


@item("mail_cart", "Mail cart", "facility")
def mail_cart(it):
    it.box((0, 0, .55), (.7, .45, .55), "grey_light", bevel=.01)
    for i in range(6):
        it.box((-.25 + i * .1, -.02, .85), (.08, .3, .02), BOOKS[i], bevel=0, rot=(70, 0, 0))
    it.stick((-.3, .22, .8), (-.3, .3, 1.0), .03, "black", seg=5)
    it.stick((.3, .22, .8), (.3, .3, 1.0), .03, "black", seg=5)
    it.stick((-.3, .3, 1.0), (.3, .3, 1.0), .03, "black", seg=5)
    for sx in (-1, 1):
        for sy in (-1, 1):
            it.cyl((sx * .3, sy * .18, .05), (.08, .08), .03, "black", seg=8, rot=(0, 90, 0))
        it.box((sx * .34, 0, .2), (.02, .4, .3), "grey", bevel=0)


@item("security_gate", "Security gate", "facility")
def security_gate(it):
    for sx in (-1, 1):
        it.box((sx * .45, 0, .5), (.18, .9, 1.0), "white", bevel=.03)
        it.box((sx * .45, 0, 1.01), (.16, .86, .02), "charcoal", bevel=0, outline=False)
        it.box((sx * .45, -.3, 1.02), (.1, .1, .02), "leaf", bevel=0, outline=False)
    for sx in (-1, 1):
        it.box((sx * .18, .1, .8), (.36, .02, .5), "glass", bevel=0)


@item("water_gallon", "Gallon water dispenser", "facility")
def water_gallon(it):
    it.box((0, 0, .5), (.32, .32, 1.0), "white", bevel=.03)
    it.box((0, -.17, .62), (.2, .02, .18), "charcoal", bevel=0)
    for sx in (-1, 1):
        it.box((sx * .05, -.18, .66), (.03, .04, .05), ("coral", "sky")[(sx + 1) // 2], bevel=0)
    it.cyl((0, 0, 1.25), (.27, .27), .45, "water", seg=14, bevel=.06)
    it.cyl((0, 0, 1.03), (.08, .08), .06, "sky", seg=10)


# =========================================================================== PRAYER ROOM (mushola)
@item("prayer_mat", "Prayer mat (sajadah)", "mushola")
def prayer_mat(it):
    it.box((0, 0, .006), (.65, 1.15, .012), "sage", bevel=0)
    it.box((0, 0, .013), (.55, 1.05, .002), "leaf_dark", bevel=0, outline=False)
    it.box((0, .4, .015), (.25, .18, .002), "butter", bevel=0, outline=False)
    it.cyl((0, .48, .015), (.25, .12), .002, "butter", seg=12, outline=False)
    for sy in (-1, 1):
        for i in range(6):
            it.box((-.27 + i * .108, sy * .585, .006), (.02, .03, .006), "offwhite", bevel=0, outline=False)


@item("prayer_mat_row", "Prayer mats row (5)", "mushola")
def prayer_mat_row(it):
    for i in range(5):
        x = -1.4 + i * .7
        m = ("sage", "blue", "coral", "lavender", "wood_mid")[i]
        it.box((x, 0, .006), (.62, 1.15, .012), m, bevel=0)
        it.cyl((x, .45, .014), (.28, .14), .002, "butter", seg=12, outline=False)


@item("mukena_rack", "Prayer garment rack", "mushola")
def mukena_rack(it):
    for sx in (-1, 1):
        it.box((sx * .5, 0, .8), (.04, .4, 1.6), "wood_mid", bevel=.006)
    it.stick((-.5, 0, 1.5), (.5, 0, 1.5), .03, "metal", seg=6)
    for i in range(4):
        x = -.33 + i * .22
        it.cyl((x, 0, 1.05), (.2, .12), .85, ("white", "offwhite", "sky", "white")[i], seg=10, top=.4)
    it.box((0, 0, .15), (1.0, .4, .03), "wood_light", bevel=.004)
    for i in range(3):
        it.box((-.3 + i * .3, 0, .22), (.25, .3, .1), ("sage", "blue", "coral")[i], bevel=.02)


@item("quran_shelf", "Quran & book shelf", "mushola")
def quran_shelf(it):
    it.box((0, 0, .5), (.9, .3, 1.0), "wood_dark", bevel=.008)
    for i in range(3):
        z = .05 + i * .32
        it.box((0, -.02, z + .14), (.84, .27, .28), "wood_mid", bevel=0, outline=False)
        x = -.38
        for k in range(10):
            it.box((x, -.04, z + .12), (.05, .2, .24), ("leaf_dark", "wood_dark", "sage", "butter")[(k + i) % 4],
                   bevel=.004)
            x += .07
    it.box((.15, -.02, 1.05), (.3, .2, .08), "leaf_dark", bevel=.01, rot=(0, 0, -6))      # rehal stand on top


@item("rehal_stand", "Book stand (rehal)", "mushola")
def rehal_stand(it):
    for sy in (-1, 1):
        it.box((0, sy * .07, .12), (.3, .02, .3), "wood_mid", bevel=.004, rot=(sy * 40, 0, 0))
    it.box((0, -.05, .22), (.26, .12, .03), "leaf_dark", bevel=.006, rot=(-40, 0, 0))
    it.box((0, .05, .22), (.26, .12, .03), "leaf_dark", bevel=.006, rot=(40, 0, 0))


@item("wudu_station", "Ablution station", "mushola")
def wudu_station(it):
    it.box((0, .15, .45), (1.8, .3, .9), "offwhite", bevel=.01)
    it.box((0, -.15, .3), (1.8, .3, .06), "sky", bevel=.01)
    it.box((0, -.15, .27), (1.7, .26, .02), "water", bevel=0, outline=False)
    for i in range(3):
        x = -.6 + i * .6
        it.stick((x, .3, 1.0), (x, -.05, 1.0), .03, "metal", seg=6)
        it.stick((x, -.05, 1.0), (x, -.05, .9), .03, "metal", seg=6)
        it.box((x, -.45, .2), (.3, .3, .4), "grey_light", bevel=.04)       # little stool
    it.box((0, .31, 1.6), (1.8, .02, 1.2), "sky", bevel=.004)


@item("sandal_shelf", "Sandal shelf", "mushola")
def sandal_shelf(it):
    for i in range(3):
        z = .05 + i * .2
        it.box((0, 0, z), (1.2, .3, .02), "wood_light", bevel=.004)
        for k in range(4):
            for sx in (-1, 1):
                it.box((-.45 + k * .3 + sx * .05, -.02, z + .025), (.08, .22, .03), BOOKS[(i + k) % 7], bevel=.004)
    for sx in (-1, 1):
        it.box((sx * .6, 0, .3), (.03, .3, .6), "wood_mid", bevel=0)


@item("prayer_partition", "Prayer room partition", "mushola")
def prayer_partition(it):
    for i in range(3):
        x = -.62 + i * .62
        it.box((x, 0, .9), (.6, .04, 1.6), "wood_light", bevel=.008)
        for r in range(5):
            it.box((x, -.025, .3 + r * .3), (.5, .01, .18), "wood_mid", bevel=0, outline=False)
        it.box((x, 0, .05), (.6, .3, .04), "wood_dark", bevel=.004)


@item("qibla_marker", "Qibla direction marker", "mushola", mount="wall", mount_z=2.0)
def qibla_marker(it):
    it.box((0, -.01, 0), (.4, .02, .25), "leaf_dark", bevel=.006)
    it.stick((-.12, -.025, 0), (.1, -.025, 0), .025, "butter", seg=5)
    it.cyl((.13, -.025, 0), (.07, .07), .03, "butter", seg=3, rot=(90, 0, 90))


@item("tasbih_bowl", "Prayer beads bowl", "mushola")
def tasbih_bowl(it):
    it.cyl((0, 0, .03), (.2, .2), .06, "wood_mid", seg=14, top=1.3)
    for i in range(12):
        x, y, _ = _polar(.06, i * 30)
        it.ball((x, y, .065), (.025, .025, .025), ("sage", "wood_dark")[i % 2], seg=6, outline=False)


@item("prayer_clock", "Prayer times board", "mushola", mount="wall", mount_z=1.6)
def prayer_clock(it):
    it.box((0, -.02, 0), (.7, .04, .4), "charcoal", bevel=.008)
    for i in range(6):
        it.box((-.25 + i * .1, -.045, .05), (.07, .004, .12), "lamp_glow", bevel=0, outline=False)
    it.box((0, -.045, -.12), (.5, .004, .06), "butter", bevel=0, outline=False)


# =========================================================================== LOBBY
@item("lobby_logo_wall", "Logo wall", "lobby")
def lobby_logo_wall(it):
    it.box((0, 0, 1.3), (2.6, .15, 2.6), "wood_mid", bevel=.01)
    for i in range(20):
        it.box((-1.24 + i * .13, -.08, 1.3), (.06, .02, 2.5), "wood_dark", bevel=0, outline=False)
    it.cyl((-.5, -.12, 1.6), (.35, .35), .05, "sage", seg=20, rot=(90, 0, 0))
    it.box((.3, -.12, 1.6), (1.0, .05, .18), "white", bevel=.01)
    it.box((.2, -.12, 1.35), (.8, .05, .08), "white", bevel=.006)


@item("visitor_kiosk", "Visitor check-in kiosk", "lobby")
def visitor_kiosk(it):
    pedestal(it, .9, .45, "white")
    it.box((0, 0, 1.1), (.45, .1, .35), "black", bevel=.02, rot=(-25, 0, 0))
    it.box((0, -.05, 1.1), (.4, .01, .3), "screen", bevel=0, outline=False, rot=(-25, 0, 0))


@item("queue_post", "Queue stanchions", "lobby")
def queue_post(it):
    for sx in (-1, 1):
        it.cyl((sx * .6, 0, .015), (.3, .3), .03, "metal", seg=14, bevel=.008)
        it.cyl((sx * .6, 0, .48), (.06, .06), .92, "metal", seg=10)
        it.ball((sx * .6, 0, .95), (.08, .08, .08), "metal", seg=8)
    for i in range(6):
        a0, a1 = i / 6, (i + 1) / 6
        z0, z1 = .88 - math.sin(a0 * math.pi) * .12, .88 - math.sin(a1 * math.pi) * .12
        it.stick((-.6 + a0 * 1.2, 0, z0), (-.6 + a1 * 1.2, 0, z1), .04, "coral", seg=5)


@item("brochure_wall", "Brochure wall rack", "lobby", mount="wall", mount_z=.9)
def brochure_wall(it):
    it.box((0, -.01, .5), (.6, .02, 1.0), "white", bevel=.004)
    for r in range(4):
        for c in range(3):
            x, z = -.19 + c * .19, .15 + r * .23
            it.box((x, -.05, z), (.17, .05, .02), "glass", bevel=0)
            it.box((x, -.04, z + .08), (.14, .015, .18), BOOKS[(r + c) % 7], bevel=0, rot=(-8, 0, 0))


@item("info_screen_totem", "Info screen totem", "lobby")
def info_screen_totem(it):
    it.box((0, 0, .9), (.6, .12, 1.8), "charcoal", bevel=.02)
    it.box((0, -.065, 1.1), (.52, .01, 1.0), "screen", bevel=0, outline=False)
    it.box((0, -.07, 1.4), (.4, .004, .1), "white", bevel=0, outline=False)
    it.box((0, 0, .02), (.7, .4, .04), "charcoal", bevel=.008)


@item("sanitizer_stand", "Hand sanitizer stand", "lobby")
def sanitizer_stand(it):
    it.cyl((0, 0, .015), (.3, .3), .03, "white", seg=14)
    it.cyl((0, 0, .55), (.05, .05), 1.05, "white", seg=8)
    it.box((0, -.04, 1.1), (.14, .1, .25), "white", bevel=.02)
    it.box((0, -.095, 1.05), (.06, .02, .03), "sky", bevel=0)


@item("plant_divider", "Planter divider", "lobby")
def plant_divider(it):
    it.box((0, 0, .3), (1.6, .35, .6), "wood_light", bevel=.015)
    for i in range(8):
        x = -.7 + i * .2
        it.ball((x, 0, .75 + (i % 3) * .08), (.26, .26, .35), ("leaf", "leaf_dark", "sage")[i % 3], seg=8)


@item("lobby_bench_round", "Round lobby bench", "lobby")
def lobby_bench_round(it):
    it.cyl((0, 0, .21), (1.6, 1.6), .42, "offwhite", seg=24, bevel=.04)
    for i in range(8):
        x, y, _ = _polar(.6, i * 45)
        cushion(it, (x, y, .46), (.42, .36, .08), BOOKS[i % 7], bevel=.025)
    it.cyl((0, 0, .6), (.6, .6), .4, "wood_light", seg=16)
    it.ball((0, 0, 1.05), (.7, .7, .6), "leaf", seg=12)


@item("umbrella_bag_stand", "Umbrella bag dispenser", "lobby")
def umbrella_bag_stand(it):
    it.box((0, 0, .5), (.35, .25, 1.0), "grey_light", bevel=.02)
    it.box((0, -.13, .8), (.25, .02, .15), "sky", bevel=0)
    it.box((0, -.14, .4), (.2, .02, .3), "paper", bevel=0, outline=False)


@item("lobby_magazine_table", "Lobby magazine table", "lobby")
def lobby_magazine_table(it):
    it.cyl((0, 0, .2), (.9, .9), .4, "wood_dark", seg=24, top=.9)
    it.cyl((0, 0, .41), (.9, .9), .02, "wood_light", seg=24)
    for i in range(3):
        it.box((-.15 + i * .15, -.05, .43 + i * .015), (.22, .3, .012), BOOKS[i + 1], bevel=0, rot=(0, 0, i * 20 - 15))


@item("bell_counter", "Concierge bell counter", "lobby")
def bell_counter(it):
    it.box((0, 0, .55), (1.2, .5, 1.1), "sage", bevel=.02)
    top_slab(it, 1.3, .6, 1.14, "wood_light", t=.04)
    it.cyl((.3, 0, 1.16), (.12, .12), .02, "metal", seg=12)
    it.ball((.3, 0, 1.2), (.1, .1, .08), "butter", seg=10)
    it.box((-.25, 0, 1.2), (.25, .18, .08), "white", bevel=.01)


# =========================================================================== OUTDOOR / TERRACE
@item("patio_umbrella", "Patio umbrella", "outdoor")
def patio_umbrella(it):
    it.cyl((0, 0, .05), (.5, .5), .1, "charcoal", seg=14, bevel=.02)
    it.stick((0, 0, .1), (0, 0, 2.3), .04, "wood_mid", seg=6)
    it.cyl((0, 0, 2.15), (2.2, 2.2), .35, "butter", seg=8, top=.05)
    it.cyl((0, 0, 1.98), (2.2, 2.2), .02, "coral", seg=8, outline=False)


@item("outdoor_bench", "Park bench", "outdoor")
def outdoor_bench(it):
    for i in range(4):
        it.box((0, -.15 + i * .1, .45), (1.5, .08, .03), "wood_mid", bevel=.004)
    for i in range(3):
        it.box((0, .22, .6 + i * .12), (1.5, .03, .08), "wood_mid", bevel=.004, rot=(-10, 0, 0))
    for sx in (-1, 1):
        it.box((sx * .65, 0, .23), (.05, .45, .45), "black", bevel=0)
        it.stick((sx * .65, .2, .45), (sx * .65, .25, .9), .04, "black", seg=5)


@item("garden_planter_box", "Garden planter box", "outdoor")
def garden_planter_box(it):
    it.box((0, 0, .25), (1.2, .5, .5), "wood_dark", bevel=.01)
    for i in range(6):
        it.box((-.5 + i * .2, -.255, .25), (.18, .01, .46), "wood_mid", bevel=0, outline=False)
    it.box((0, 0, .49), (1.12, .42, .02), "soil", bevel=0, outline=False)
    for i in range(5):
        x = -.45 + i * .22
        it.stick((x, 0, .5), (x, 0, .75), .015, "leaf_dark", seg=4)
        it.ball((x, 0, .8), (.1, .1, .1), ("coral", "butter", "lavender", "blush", "sky")[i], seg=8)


@item("hammock_stand", "Hammock on stand", "outdoor")
def hammock_stand(it):
    for sx in (-1, 1):
        it.stick((sx * 1.4, 0, 0), (sx * 1.1, 0, 1.1), .06, "wood_mid", seg=6)
        it.box((sx * 1.2, 0, .03), (.4, .7, .06), "wood_mid", bevel=.01)
    it.box((0, 0, .03), (2.4, .1, .06), "wood_mid", bevel=.01)
    for i in range(8):
        a0, a1 = i / 8, (i + 1) / 8
        z0, z1 = 1.05 - math.sin(a0 * math.pi) * .5, 1.05 - math.sin(a1 * math.pi) * .5
        it.stick((-1.05 + a0 * 2.1, 0, z0), (-1.05 + a1 * 2.1, 0, z1), .7 if 0 < i < 7 else .2, "sky", seg=6)


@item("lamp_post", "Garden lamp post", "outdoor")
def lamp_post(it):
    it.cyl((0, 0, .08), (.3, .3), .16, "black", seg=8, bevel=.01)
    it.cyl((0, 0, 1.2), (.08, .08), 2.1, "black", seg=8)
    it.box((0, 0, 2.4), (.3, .3, .35), "lamp_glow", bevel=.006)
    it.cyl((0, 0, 2.65), (.42, .42), .15, "black", seg=4, top=.2, rot=(0, 0, 45))


@item("trash_outdoor", "Outdoor bin", "outdoor")
def trash_outdoor(it):
    it.cyl((0, 0, .45), (.5, .5), .9, "leaf_dark", seg=16)
    for i in range(8):
        x, y, _ = _polar(.25, i * 45)
        it.box((x, y, .45), (.04, .04, .85), "wood_mid", bevel=0, rot=(0, 0, i * 45))
    it.ball((0, 0, .92), (.54, .54, .2), "black", seg=14)


@item("deck_chair", "Deck chair", "outdoor")
def deck_chair(it):
    for sx in (-1, 1):
        it.stick((sx * .28, -.5, 0), (sx * .28, .3, .9), .04, "wood_mid", seg=5)
        it.stick((sx * .28, .2, 0), (sx * .28, -.3, .45), .04, "wood_mid", seg=5)
    it.box((0, -.05, .55), (.5, .9, .02), "coral", bevel=0, rot=(-40, 0, 0))
    for i in range(4):
        it.box((0, -.05 + i * .02, .55 + i * .0), (.52, .9, .004), ("coral", "white")[i % 2], bevel=0,
               outline=False, rot=(-40, 0, 0))


@item("swing_bench", "Swing bench", "outdoor")
def swing_bench(it):
    for sx in (-1, 1):
        it.stick((sx * .9, -.5, 0), (sx * .9, 0, 2.0), .07, "wood_dark", seg=6)
        it.stick((sx * .9, .5, 0), (sx * .9, 0, 2.0), .07, "wood_dark", seg=6)
        it.stick((sx * .6, 0, 1.97), (sx * .6, 0, .9), .015, "metal", seg=4)
    it.stick((-.95, 0, 2.0), (.95, 0, 2.0), .08, "wood_dark", seg=6)
    it.box((0, 0, .5), (1.3, .5, .05), "wood_mid", bevel=.006)
    it.box((0, .23, .75), (1.3, .05, .45), "wood_mid", bevel=.006, rot=(-10, 0, 0))
    cushion(it, (0, 0, .56), (1.2, .45, .07), "sage", bevel=.02)


@item("fountain_small", "Small fountain", "outdoor")
def fountain_small(it):
    it.cyl((0, 0, .2), (1.0, 1.0), .4, "grey_light", seg=20, bevel=.03)
    it.cyl((0, 0, .38), (.88, .88), .02, "water", seg=20, outline=False)
    it.cyl((0, 0, .6), (.12, .12), .45, "grey_light", seg=10)
    it.cyl((0, 0, .85), (.45, .45), .1, "grey_light", seg=14, top=1.4)
    it.ball((0, 0, 1.0), (.12, .12, .2), "water", seg=8)


@item("stepping_stones", "Stepping stones", "outdoor")
def stepping_stones(it):
    for i in range(5):
        it.cyl(((i % 2) * .2 - .1, -.8 + i * .4, .02), (.35 + (i % 3) * .05, .3), .04, "grey", seg=10, bevel=.01,
               rot=(0, 0, i * 30))


@item("fence_section", "Wooden fence", "outdoor")
def fence_section(it):
    for i in range(9):
        x = -.88 + i * .22
        it.box((x, 0, .45), (.14, .03, .9), "wood_light", bevel=.004)
        it.cyl((x, 0, .92), (.14, .03), .06, "wood_light", seg=4, top=.1, rot=(0, 0, 45))
    for z in (.25, .7):
        it.box((0, .03, z), (2.0, .03, .08), "wood_mid", bevel=0)


@item("outdoor_table_set", "Outdoor table set", "outdoor")
def outdoor_table_set(it):
    round_top = .8
    it.cyl((0, 0, .73), (round_top, round_top), .03, "white", seg=20)
    it.cyl((0, 0, .36), (.06, .06), .72, "white", seg=8)
    it.cyl((0, 0, .02), (.4, .4), .04, "white", seg=12)
    for k in range(2):
        deg = 90 + k * 180
        x, y, _ = _polar(.75, deg)
        it.box((x, y, .45), (.42, .42, .03), "white", bevel=.006, rot=(0, 0, deg))
        bx, by, _ = _polar(.95, deg)
        it.box((bx, by, .7), (.42, .03, .45), "white", bevel=.006, rot=(0, 0, deg - 90))
        legs_c = [(x + sx * .17, y + sy * .17) for sx in (-1, 1) for sy in (-1, 1)]
        for lx, ly in legs_c:
            it.stick((lx, ly, 0), (lx, ly, .44), .025, "white", seg=4)
