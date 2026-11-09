"""Badan chibi dasar (kulit): kepala, leher, torso, lengan, tangan, paha, betis. Selalu tampil; pakaian menutupinya."""


def build_body(c):
    p = c.part("BODY", "spine")
    S = "M_skin"
    # kepala (bulat-kotak besar) + telinga + leher
    p.box((0, 0, 1.33), (.74, .68, .66), S, "head", r=.2, seg=3)
    p.sph((.375, 0, 1.30), (.09, .12, .16), S, "head", seg=8)
    p.sph((-.375, 0, 1.30), (.09, .12, .16), S, "head", seg=8)
    p.cyl((0, 0, .97), (.18, .16), .1, S, "spine", seg=10)
    # torso + panggul
    p.box((0, 0, .74), (.46, .32, .44), S, "spine", r=.09, seg=2)
    p.box((0, 0, .52), (.42, .30, .14), S, "hips", r=.05, seg=2)
    for sx, L in ((1, "L"), (-1, "R")):
        # lengan: atas + bawah + tangan bulat
        p.box((sx * .31, 0, .80), (.14, .14, .24), S, "arm_" + L, r=.05, seg=2)
        p.box((sx * .31, 0, .60), (.13, .13, .21), S, "fore_" + L, r=.05, seg=2)
        p.sph((sx * .31, 0, .47), (.15, .15, .15), S, "fore_" + L, seg=10)
        # kaki: paha + betis
        p.box((sx * .12, 0, .38), (.17, .17, .19), S, "thigh_" + L, r=.05, seg=2)
        p.box((sx * .12, 0, .20), (.15, .15, .18), S, "shin_" + L, r=.04, seg=2)
    return p.done()
