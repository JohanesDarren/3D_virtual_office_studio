"""Atasan (6), bawahan (3), sepatu (2). Di-skin rigid ke tulang. Pakaian sedikit lebih besar dari kulit di body.py."""
T, T2 = "M_top", "M_top2"


def _torso(p, m=T, z=.745, w=.51, d=.37, h=.47, bone="spine"):
    p.box((0, 0, z), (w, d, h), m, bone, r=.09, seg=2)


def _arms(p, long=True, m=T, cuff=None):
    for sx, L in ((1, "L"), (-1, "R")):
        p.box((sx * .31, 0, .80), (.175, .175, .26), m, "arm_" + L, r=.06, seg=2)
        if long:
            p.box((sx * .31, 0, .60), (.155, .155, .22), m, "fore_" + L, r=.05, seg=2)
            if cuff:
                p.box((sx * .31, 0, .505), (.165, .165, .04), cuff, "fore_" + L, r=.01, seg=1)


def _collar(p, m=T2, z=.965):
    for sx in (1, -1):
        p.box((sx * .09, -.17, z), (.13, .05, .09), m, "spine", r=.015, seg=1, rot=(0, 0, sx * -25))


def kemeja(c):
    p = c.part("TOP_kemeja", "spine"); _torso(p); _arms(p, True, T, T2); _collar(p)
    p.box((0, -.187, .74), (.05, .02, .44), T2, "spine", r=.005, seg=1)
    for z in (.88, .76, .64):
        p.sph((0, -.2, z), (.04, .03, .04), T2, "spine", seg=6)
    p.done()


def hoodie(c):
    p = c.part("TOP_hoodie", "spine"); _torso(p, w=.54, d=.40, h=.48); _arms(p, True, T, T2)
    p.box((0, .20, .98), (.42, .16, .2), T, "spine", r=.07, seg=2)
    p.box((0, -.205, .62), (.32, .04, .13), T2, "spine", r=.03, seg=1)
    for sx in (1, -1):
        p.box((sx * .07, -.2, .90), (.025, .02, .14), T2, "spine", r=.005, seg=1)
    p.done()


def blazer(c):
    p = c.part("TOP_blazer", "spine"); _torso(p, w=.53, d=.38, h=.48); _arms(p, True, T, T2)
    p.box((0, -.185, .80), (.14, .02, .32), T2, "spine", r=.005, seg=1)   # kemeja di dalam
    for sx in (1, -1):
        p.box((sx * .115, -.2, .81), (.10, .03, .34), T, "spine", r=.01, seg=1, rot=(0, 0, sx * 18))
        p.box((sx * .20, -.195, .72), (.12, .03, .40), T, "spine", r=.02, seg=1)
    p.sph((.04, -.215, .66), (.045, .03, .045), "M_acc2", "spine", seg=6)
    p.done()


def cardigan(c):
    p = c.part("TOP_cardigan", "spine"); _torso(p, w=.54, d=.39, h=.50, z=.735); _arms(p, True, T, T2)
    p.box((0, -.2, .735), (.09, .02, .50), T2, "spine", r=.005, seg=1)
    for sx in (1, -1):
        p.box((sx * .16, -.205, .60), (.12, .02, .11), T, "spine", r=.015, seg=1)
    p.box((0, -.0, .50), (.55, .39, .035), T2, "spine", r=.01, seg=1)
    p.done()


def rompi(c):
    p = c.part("TOP_rompi", "spine")
    _arms(p, False, T2)                                     # kaos pendek di dalam
    p.box((0, 0, .745), (.49, .35, .46), T2, "spine", r=.08, seg=2)
    p.box((0, 0, .75), (.535, .385, .46), T, "spine", r=.09, seg=2)
    p.box((0, 0, .86), (.30, .395, .07), T2, "spine", r=.015, seg=1)   # strip reflektif
    p.box((0, 0, .66), (.30, .395, .07), T2, "spine", r=.015, seg=1)
    p.done()


def polo(c):
    p = c.part("TOP_polo", "spine"); _torso(p); _arms(p, False, T)
    for sx, L in ((1, "L"), (-1, "R")):
        p.box((sx * .31, 0, .71), (.185, .185, .04), T2, "arm_" + L, r=.01, seg=1)
    _collar(p); p.box((0, -.187, .88), (.05, .02, .17), T2, "spine", r=.005, seg=1)
    p.sph((0, -.2, .86), (.035, .03, .035), T2, "spine", seg=6)
    p.done()


TOP = {f.__name__: f for f in (kemeja, hoodie, blazer, cardigan, rompi, polo)}

B = "M_bottom"


def _belt(p):
    p.box((0, 0, .575), (.43, .31, .045), "M_acc2", "hips", r=.01, seg=1)


def celana(c):
    p = c.part("BOTTOM_celana", "hips")
    p.box((0, 0, .515), (.47, .345, .17), B, "hips", r=.06, seg=2); _belt(p)
    for sx, L in ((1, "L"), (-1, "R")):
        p.box((sx * .12, 0, .38), (.205, .205, .20), B, "thigh_" + L, r=.05, seg=2)
        p.box((sx * .12, 0, .215), (.185, .185, .20), B, "shin_" + L, r=.04, seg=2)
    p.done()


def rok(c):
    p = c.part("BOTTOM_rok", "hips")
    p.box((0, 0, .53), (.45, .33, .14), B, "hips", r=.05, seg=2)
    p.cyl((0, 0, .45), (.64, .52), .26, B, "hips", r2=.72, seg=16)
    p.box((0, 0, .576), (.44, .32, .04), "M_acc2", "hips", r=.01, seg=1)
    p.done()


def celana_pendek(c):
    p = c.part("BOTTOM_celana_pendek", "hips")
    p.box((0, 0, .515), (.47, .345, .17), B, "hips", r=.06, seg=2); _belt(p)
    for sx, L in ((1, "L"), (-1, "R")):
        p.box((sx * .12, 0, .385), (.205, .205, .17), B, "thigh_" + L, r=.05, seg=2)
    p.done()


BOTTOM = {"celana": celana, "rok": rok, "celana_pendek": celana_pendek}


def sneakers(c):
    p = c.part("SHOES_sneakers", "shin_L")
    for sx, L in ((1, "L"), (-1, "R")):
        p.box((sx * .12, -.045, .075), (.195, .31, .13), "M_shoes", "shin_" + L, r=.05, seg=2)
        p.box((sx * .12, -.05, .018), (.205, .325, .04), "M_shoes2", "shin_" + L, r=.015, seg=1)
        p.box((sx * .12, -.13, .115), (.15, .1, .05), "M_top2", "shin_" + L, r=.02, seg=1)
    p.done()


def formal(c):
    p = c.part("SHOES_formal", "shin_L")
    for sx, L in ((1, "L"), (-1, "R")):
        p.box((sx * .12, -.045, .07), (.18, .32, .12), "M_shoes2", "shin_" + L, r=.05, seg=2)
        p.box((sx * .12, .05, .015), (.17, .1, .035), "M_acc2", "shin_" + L, r=.01, seg=1)
    p.done()


SHOES = {"sneakers": sneakers, "formal": formal}
