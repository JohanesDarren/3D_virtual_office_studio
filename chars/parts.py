"""Bean-buddy avatar parts: round head, bean body, mitten hands, stubby legs.

Character space: stands on z=0, faces -Y, character's LEFT is +X. Height ~1.2 m.
Every part is a rigid mesh (own outline) parented to one bone, so the web app needs no skinning.
Parts are built in character space; the rig places each part's origin at the world origin
and bone-parents it with an inverse matrix, so rest pose == build pose.
"""
import math

HEAD_C = (0, 0, 1.0)      # head center
HEAD_S = (.56, .5, .5)    # head size
FACE_Y = -.245            # front of the face


def surf(x, z):
    """Front (-Y) surface of the head ellipsoid at (x, z): face features snap onto it."""
    rx, ry, rz = HEAD_S[0] / 2, HEAD_S[1] / 2, HEAD_S[2] / 2
    k = 1 - (x / rx) ** 2 - ((z - HEAD_C[2]) / rz) ** 2
    return HEAD_C[1] - ry * math.sqrt(max(k, 0.0))

# bones: name, head, tail, parent
BONES = [
    ("root", (0, 0, 0), (0, 0, .1), None),
    ("hips", (0, 0, .42), (0, 0, .5), "root"),
    ("spine", (0, 0, .5), (0, 0, .78), "hips"),
    ("head", (0, 0, .78), (0, 0, 1.25), "spine"),
    ("arm_L", (.2, 0, .72), (.26, 0, .48), "spine"),
    ("arm_R", (-.2, 0, .72), (-.26, 0, .48), "spine"),
    ("leg_L", (.1, 0, .42), (.1, 0, .06), "hips"),
    ("leg_R", (-.1, 0, .42), (-.1, 0, .06), "hips"),
]


# --------------------------------------------------------------------------- body
def body(p, c):
    """p(name, bone) -> Item. c = dict of material names for this character."""
    t = p("TORSO", "spine")
    t.ball((0, 0, .62), (.42, .34, .42), c["top"], seg=16)
    t.cyl((0, 0, .8), (.13, .13), .06, c["skin"], seg=12)                 # neck stub
    style = c["outfit"]
    if style == "shirt":
        for sx in (-1, 1):
            t.box((sx * .055, -.13, .78), (.09, .04, .06), "white", bevel=.01, rot=(20, 0, sx * -20))
        for z in (.7, .62, .54):
            t.ball((0, -.17, z), (.022, .012, .022), "white", seg=6, outline=False)
    elif style == "hoodie":
        t.ball((0, .14, .76), (.3, .14, .14), c["top"], seg=12)            # hood bunched at the back
        t.box((0, -.165, .54), (.2, .03, .08), c["top2"], bevel=.02)       # pocket
        for sx in (-1, 1):
            t.stick((sx * .05, -.15, .74), (sx * .06, -.17, .62), .012, c["top2"], seg=5, outline=False)
    elif style == "cardigan":
        t.box((0, -.168, .63), (.06, .02, .32), c["top2"], bevel=.008, outline=False)   # placket
        for z in (.72, .64, .56):
            t.ball((0, -.18, z), (.02, .012, .02), "wood_dark", seg=6, outline=False)
    elif style == "tee":
        t.ball((0, -.16, .66), (.1, .02, .1), c["top2"], seg=10, outline=False)          # chest print
    elif style == "blazer":
        t.box((0, -.155, .7), (.1, .03, .16), c["top2"], bevel=.01, outline=False)       # inner shirt V
        for sx in (-1, 1):
            t.box((sx * .055, -.16, .7), (.05, .03, .18), c["top"], bevel=.01, rot=(0, sx * -18, 0))   # lapels
        for z in (.6, .53):
            t.ball((.02, -.19, z), (.022, .012, .022), "black", seg=6, outline=False)
        t.box((.1, -.17, .7), (.06, .012, .015), "white", bevel=0, outline=False)        # pocket square
    elif style == "sweater":
        for z in (.55, .64, .73):                                                          # knit stripes
            k = math.sqrt(max(0, 1 - ((z - .62) / .21) ** 2)) * 1.015
            t.cyl((0, 0, z), (.42 * k, .34 * k), .03, c["top2"], seg=16, outline=False)
        t.cyl((0, 0, .79), (.2, .18), .04, c["top2"], seg=12)                            # rib collar
    elif style == "vest":
        t.ball((0, .0, .59), (.43, .35, .34), c["top2"], seg=16)                          # knit vest over shirt
        t.box((0, -.17, .72), (.07, .02, .1), "white", bevel=.008, outline=False)
        for sx in (-1, 1):
            t.box((sx * .055, -.13, .78), (.09, .04, .06), "white", bevel=.01, rot=(20, 0, sx * -20))
    elif style == "polo":
        for sx in (-1, 1):
            t.box((sx * .055, -.13, .78), (.09, .04, .06), c["top2"], bevel=.01, rot=(20, 0, sx * -20))
        for z in (.74, .69):
            t.ball((0, -.165, z), (.02, .012, .02), c["top2"], seg=6, outline=False)
        t.ball((.1, -.155, .66), (.04, .01, .04), c["top2"], seg=8, outline=False)       # tiny logo
    elif style == "dress":
        t.box((0, -.155, .76), (.14, .02, .03), "white", bevel=.008, outline=False)       # round collar
        t.cyl((0, 0, .5), (.4, .32), .03, c["top2"], seg=16, outline=False)                # waist ribbon
        t.ball((.1, -.155, .5), (.06, .03, .04), c["top2"], seg=8)
    if c.get("tie"):
        t.box((0, -.17, .66), (.05, .02, .16), c["acc"], bevel=.008)
        t.box((0, -.165, .75), (.06, .02, .04), c["acc"], bevel=.008)
    t.done_bone()

    h = p("HIPS", "hips")
    if c["bottom"] == "skirt" or c["outfit"] == "dress":
        h.cyl((0, 0, .43), (.42, .36), .16, c["pants"], seg=16, top=.8, bevel=.02)
    else:
        h.ball((0, 0, .45), (.38, .3, .18), c["pants"], seg=14)
    h.done_bone()

    for side, sx in (("L", 1), ("R", -1)):
        a = p("ARM_" + side, "arm_" + side)
        a.stick((sx * .2, 0, .73), (sx * .25, 0, .53), .1, c["top"], seg=10)
        a.ball((sx * .2, 0, .72), (.11, .11, .11), c["top"], seg=10)          # shoulder cap
        a.ball((sx * .262, -.005, .47), (.11, .1, .12), c["skin"], seg=10)     # mitten
        a.ball((sx * .245, -.05, .5), (.045, .04, .05), c["skin"], seg=8)      # thumb
        a.done_bone()

        leg_col = c["skin"] if (c["bottom"] == "skirt" or c["outfit"] == "dress") else c["pants"]
        g = p("LEG_" + side, "leg_" + side)
        g.stick((sx * .1, 0, .4), (sx * .1, 0, .08), .12, leg_col, seg=10)
        g.box((sx * .1, -.035, .045), (.14, .21, .09), c["shoes"], bevel=.035)
        g.box((sx * .1, -.035, .006), (.142, .212, .012), "white", bevel=.004, outline=False)   # sole
        g.done_bone()


# --------------------------------------------------------------------------- head & face
def head(p, c):
    h = p("HEAD", "head")
    h.ball(HEAD_C, HEAD_S, c["skin"], seg=20)
    for sx in (-1, 1):
        h.ball((sx * .275, .0, .98), (.08, .06, .1), c["skin"], seg=8)       # ears
    h.done_bone()

    for expr in EXPRESSIONS:
        face(p, c, expr)


# --------------------------------------------------------------------------- face expressions
# One small face mesh per expression, each on its own "face_<expr>" bone (child of head, bone head at the
# head center). Only "neutral" is unfolded in rest pose; every other face (and every prop) is stored
# folded to HIDE size around its bone head, so the rest pose stays clean. Clips switch with bone scale:
# neutral 1 (shown) / HIDE (hidden); others 1 (hidden) / 1/HIDE (shown). Exported scale keys are STEP.
EXPRESSIONS = ["neutral", "blink", "happy", "talk", "sad", "surprised", "focus", "think", "sleep", "yawn"]
HIDE = .001


def _eye_open(f, x, big=False, sx=1.0, sz=1.0, look=(0.0, 0.0)):
    ex, ez = ((.068, .094) if big else (.056, .078))
    ex, ez = ex * sx, ez * sz
    y = surf(x, .99)
    f.ball((x, y + .004, .99), (ex, .024, ez), "black", seg=12, outline=False)
    lx, lz = look
    f.ball((x - .013 + lx, y - .008, .99 + ez * .28 + lz), (.024 * sx, .01, .03 * sz), "white", seg=8,
           outline=False)
    f.ball((x + .014 + lx, y - .007, .99 - ez * .32 + lz), (.012, .008, .014), "white", seg=6, outline=False)


def _eye_arc(f, x, up=True, z=1.0, w=.042):
    """Closed eye: ^ (happy, up=True) or u (relaxed / asleep, up=False)."""
    for k in (-1, 1):
        f.box((x + k * .018, surf(x, z) - .004, z + (.006 if up else -.004)), (w, .016, .016), "black", bevel=0,
              rot=(0, (k if up else -k) * 30, 0), outline=False)


def _eye_squeeze(f, x, sx):
    """> <  squeezed shut (yawn)."""
    for k in (-1, 1):
        f.box((x - sx * .01, surf(x, 1.0) - .004, 1.0 + k * .012), (.045, .016, .014), "black", bevel=0,
              rot=(0, sx * k * 28, 0), outline=False)


def _brow(f, c, x, sx, z=1.075, tilt=-5):
    f.box((x, surf(x, z) - .003, z), (.055, .012, .014), c.get("brow") or c["hair"], bevel=0,
          rot=(0, sx * tilt, 0), outline=False)


def _mouth_w(f):
    for k, dx in ((-1, -.017), (1, -.017), (-1, .017), (1, .017)):
        f.box((dx + k * .009, surf(dx, .912) - .004, .912), (.022, .012, .009), "black", bevel=0,
              rot=(0, -k * 30, 0), outline=False)   # \/\/ = w


def _mouth_open(f, w=.055, h=.042, teeth=True):
    f.ball((0, surf(0, .905) + .002, .905), (w, .016, h), "coral", seg=10, outline=False)
    if teeth:
        f.box((0, surf(0, .918) - .005, .918), (w * .8, .006, .01), "white", bevel=0, outline=False)


def _mouth_line(f, w=.04, dx=0.0, tilt=0):
    f.box((dx, surf(dx, .91) - .004, .91), (w, .012, .01), "black", bevel=0, rot=(0, tilt, 0), outline=False)


def _mouth_frown(f):
    for k in (-1, 1):
        f.box((k * .012, surf(k * .012, .905) - .004, .905), (.028, .012, .01), "black", bevel=0,
              rot=(0, k * 28, 0), outline=False)   # /\ = frown


def face(p, c, expr):
    f = p("FACE_" + expr, "face_" + expr)
    big = c["eyes"] == "big"
    for sx in (-1, 1):
        x = sx * .095
        if expr == "neutral":
            _eye_arc(f, x) if c["eyes"] == "happy" else _eye_open(f, x, big)
            _brow(f, c, x, sx, 1.075 + (.012 if c["brows"] == "up" else 0), 10 if c["brows"] == "up" else -5)
        elif expr == "talk":
            _eye_arc(f, x) if c["eyes"] == "happy" else _eye_open(f, x, big)
            _brow(f, c, x, sx, 1.082, 6)
        elif expr == "blink":
            _eye_arc(f, x, up=False, z=.985)
            _brow(f, c, x, sx, 1.07, -5)
        elif expr == "happy":
            _eye_arc(f, x, z=1.0)
            _brow(f, c, x, sx, 1.09, 12)
        elif expr == "sad":
            _eye_open(f, x, big, sz=.85, look=(0, -.008))
            _brow(f, c, x, sx, 1.075, 22)            # inner ends up
        elif expr == "surprised":
            _eye_open(f, x, True, sx=1.1, sz=1.15)
            _brow(f, c, x, sx, 1.105, 0)
        elif expr == "focus":
            _eye_open(f, x, False, sz=.55)
            f.box((x, surf(x, 1.02) - .006, 1.02), (.064, .014, .012), "black", bevel=0, outline=False)   # lid
            _brow(f, c, x, sx, 1.06, -14)            # determined
        elif expr == "think":
            _eye_open(f, x, big, look=(-.01, .016))
            _brow(f, c, x, sx, 1.075 + (.02 if sx < 0 else 0), -5 if sx > 0 else 12)
        elif expr == "sleep":
            _eye_arc(f, x, up=False, z=.98)
            _brow(f, c, x, sx, 1.065, 4)
        elif expr == "yawn":
            _eye_squeeze(f, x, sx)
            _brow(f, c, x, sx, 1.08, 15)
        cx, cz = sx * .16, .93                                               # cheeks
        hot = expr in ("happy", "talk", "surprised")
        f.ball((cx, surf(cx, cz) + .003, cz), (.085 if hot else .075, .012, .048 if hot else .042), "cheek", seg=10,
               outline=False)
    if expr == "neutral":
        _mouth_open(f) if c["mouth"] == "open" else _mouth_w(f)
    elif expr == "talk":
        _mouth_open(f, .05, .05, teeth=False) if c["mouth"] != "open" else _mouth_w(f)
    elif expr in ("blink", "think"):
        _mouth_w(f) if expr == "blink" else _mouth_line(f, .03, .02, -12)
    elif expr == "happy":
        _mouth_open(f, .075, .05)
    elif expr == "sad":
        _mouth_frown(f)
        f.ball((.1, surf(.1, .93) - .004, .93), (.022, .012, .034), "sky", seg=8, outline=False)       # tear
    elif expr == "surprised":
        _mouth_open(f, .04, .055, teeth=False)
    elif expr == "focus":
        _mouth_line(f, .035)
    elif expr == "sleep":
        _mouth_open(f, .025, .025, teeth=False)
    elif expr == "yawn":
        _mouth_open(f, .06, .075, teeth=False)
    if expr != "neutral":
        f.collapse = HEAD_C          # stored folded; a clip shows it with bone scale 1/HIDE
    f.done_bone(outline=False)


# --------------------------------------------------------------------------- hand / head props
# Each prop sits on its own "prop_<name>" bone (child of an arm, head at the mitten) and is hidden with
# the same HIDE scale trick. Props are modelled in the GRIP pose (arm aimed at `grip`) and moved back to
# rest, so they sit right in the hand when a clip aims the arm at (about) the grip target.
MITTEN = {"arm_L": (.262, -.005, .47), "arm_R": (-.262, -.005, .47)}
ARM_HEAD = {"arm_L": (.2, 0, .72), "arm_R": (-.2, 0, .72)}
PROPS = {   # name: (parent bone, grip target or None for head props)
    "mug": ("arm_R", (-.27, -.22, .62)),
    "phone": ("arm_R", (-.26, -.06, 1.0)),
    "brush": ("arm_R", (-.15, -.4, .75)),
    "palette": ("arm_L", (.22, -.25, .6)),
    "stylus": ("arm_R", (-.05, -.36, .72)),
    "camera": ("arm_R", (-.06, -.32, .98)),
    "pen": ("arm_R", (-.08, -.34, .72)),
    "note": ("arm_R", (-.15, -.45, .95)),
    "notepad": ("arm_L", (.14, -.26, .62)),
    "clipboard": ("arm_L", (.08, -.3, .7)),
    "headset": ("head", None),
}
ROLE_PROPS = {"it": [], "creative": ["brush", "palette", "stylus"], "content": ["camera"],
              "marketing": ["note", "notepad"], "finance": ["pen"], "hr": ["pen", "clipboard"],
              "sales": ["headset"], "exec": ["pen"]}


def prop_names(c):
    return ["mug", "phone"] + ROLE_PROPS[c["role"]]


def prop_bones(c):
    out = []
    for n in prop_names(c):
        par, _g = PROPS[n]
        if par == "head":
            out.append(("prop_" + n, (0, 0, 1.0), (0, 0, 1.05), "head"))
        else:
            m = MITTEN[par]
            out.append(("prop_" + n, m, (m[0] * 1.03, m[1], m[2] - .06), par))
    return out


def face_bones():
    return [("face_" + e, (0, 0, 1.0), (0, 0, 1.05), "head") for e in EXPRESSIONS]


def props(p, c, aim):
    from mathutils import Matrix, Vector
    import bmesh
    for n in prop_names(c):
        par, grip = PROPS[n]
        it = p("PROP_" + n, "prop_" + n)
        if grip is None:   # head prop: headset
            for i in range(9):
                deg = -80 + i * 20
                it.box((math.sin(math.radians(deg)) * .31, .03, 1.02 + math.cos(math.radians(deg)) * .31),
                       (.06, .05, .035), "charcoal", bevel=.01, rot=(0, deg, 0))
            it.cyl((-.3, 0, .98), (.14, .14), .06, "charcoal", seg=12, rot=(0, 90, 0), bevel=.01)
            it.cyl((.3, 0, .98), (.14, .14), .06, "charcoal", seg=12, rot=(0, 90, 0), bevel=.01)
            it.stick((-.3, -.03, .95), (-.16, -.24, .9), .016, "charcoal", seg=6)
            it.ball((-.15, -.25, .9), (.04, .035, .035), "coral", seg=8)
            it.collapse = (0, 0, 1.0)
            it.done_bone()
            continue
        h = Vector(ARM_HEAD[par])
        q = aim(par, grip)
        m = h + q @ (Vector(MITTEN[par]) - h)        # mitten centre in the grip pose
        sx = 1 if par == "arm_L" else -1             # +1 left hand, -1 right hand
        x, y, z = m
        if n == "mug":
            it.cyl((x, y - .07, z + .01), (.08, .08), .1, "white", seg=12)
            it.cyl((x, y - .07, z + .061), (.065, .065), .004, "wood_dark", seg=12, outline=False)
            it.cyl((x, y - .07, z + .02), (.081, .081), .03, "coral", seg=12, outline=False)
        elif n == "phone":
            it.box((x + .045, y - .01, z), (.015, .07, .13), "charcoal", bevel=.008)
            it.box((x + .036, y - .01, z), (.004, .06, .11), "screen", bevel=0, outline=False)
        elif n == "brush":
            it.stick((x, y - .02, z - .02), (x + .02, y - .16, z + .12), .016, "wood_mid", seg=6)
            it.cyl((x + .023, y - .18, z + .14), (.024, .024), .05, "coral", seg=6, top=.3, rot=(-40, 0, 0))
        elif n == "palette":
            it.cyl((x - .06, y - .05, z + .03), (.22, .15), .012, "wood_light", seg=16, rot=(0, -15, 0))
            for k, col in enumerate(("coral", "butter", "sky", "sage", "lavender")):
                dx, dy, _ = (math.cos(k * 1.1) * .06, math.sin(k * 1.1) * .04, 0)
                it.ball((x - .08 + dx, y - .05 + dy, z + .04), (.03, .03, .014), col, seg=8, outline=False)
        elif n in ("stylus", "pen"):
            it.stick((x + .01, y - .05, z - .06), (x - .01, y + .03, z + .07), .014,
                     "grey_light" if n == "stylus" else "blue", seg=6)
            it.stick((x + .01, y - .05, z - .06), (x + .013, y - .06, z - .075), .008, "black", seg=5)
        elif n == "camera":
            cx = x + .07
            it.box((cx, y - .04, z), (.18, .08, .11), "charcoal", bevel=.02)
            it.cyl((cx, y - .1, z - .005), (.08, .08), .06, "black", seg=12, rot=(90, 0, 0))
            it.cyl((cx, y - .131, z - .005), (.06, .06), .004, "glass", seg=12, rot=(90, 0, 0), outline=False)
            it.box((cx - .06, y - .081, z + .035), (.03, .004, .02), "lamp_glow", bevel=0, outline=False)   # flash
        elif n == "note":
            it.box((x, y - .06, z + .02), (.08, .006, .08), "butter", bevel=0)
        elif n == "notepad":
            it.box((x - .02, y - .04, z + .03), (.1, .1, .03), "butter", bevel=.006)
        elif n == "clipboard":
            it.box((x - .04, y - .05, z + .04), (.2, .26, .012), "wood_mid", bevel=.006, rot=(25, 0, 0))
            it.box((x - .04, y - .055, z + .047), (.17, .22, .004), "paper", bevel=0, rot=(25, 0, 0),
                   outline=False)
            it.box((x - .04, y + .06, z + .1), (.07, .03, .02), "metal", bevel=.004, rot=(25, 0, 0))
        # grip pose -> rest pose, so the bone's pose brings it back into the hand
        back = Matrix.Translation(h) @ q.inverted().to_matrix().to_4x4() @ Matrix.Translation(-h)
        bmesh.ops.transform(it.bm, verts=it.bm.verts, matrix=back)
        it.collapse = MITTEN[par]
        it.done_bone()


# --------------------------------------------------------------------------- hair
def _cap(h, c, back=.04, z=1.12, size=(.6, .56, .42)):
    h.ball((0, back, z), size, c["hair"], seg=18)


def hair(p, c):
    style = c["hair_style"]
    h = p("HAIR", "head")
    if "beanie" in c.get("accs", []) or "cap" in c.get("accs", []):   # only what peeks out under the hat
        for x in ((-.12, -.04, .05, .13) if "beanie" in c["accs"] else ()):   # fringe tufts (cap brim hides them)
            h.ball((x, surf(x, 1.05) + .01, 1.05), (.1, .06, .07), c["hair"], seg=8)
        for sx in (-1, 1):
            h.ball((sx * .25, .0, 1.0), (.1, .2, .16), c["hair"], seg=10)
    elif style == "short":
        _cap(h, c)
        h.ball((-.06, -.19, 1.16), (.36, .13, .14), c["hair"], seg=12, rot=(0, 10, 0))   # side-swept fringe
        h.ball((.14, -.17, 1.18), (.2, .11, .1), c["hair"], seg=10)
    elif style == "bob":
        _cap(h, c, back=.06, z=1.1, size=(.64, .58, .46))
        for sx in (-1, 1):
            h.ball((sx * .27, .04, .93), (.14, .32, .3), c["hair"], seg=12)
        h.ball((0, -.2, 1.15), (.48, .12, .13), c["hair"], seg=14)                    # straight fringe
    elif style == "bun":
        _cap(h, c, size=(.6, .56, .4))
        h.ball((0, .1, 1.33), (.22, .22, .2), c["hair"], seg=12)
        h.cyl((0, .09, 1.24), (.12, .12), .04, c["acc"], seg=10)                        # scrunchie
        h.ball((.08, -.19, 1.15), (.32, .12, .12), c["hair"], seg=12, rot=(0, -10, 0))
    elif style == "curly":
        _cap(h, c, z=1.1, size=(.58, .54, .4))
        for i in range(10):
            a = i * 36
            x, y = math.cos(math.radians(a)) * .25, math.sin(math.radians(a)) * .23 + .03
            h.ball((x, y, 1.17 + (i % 2) * .04), (.17, .17, .15), c["hair"], seg=10)
        h.ball((0, .02, 1.27), (.26, .24, .16), c["hair"], seg=12)
    elif style == "long":
        _cap(h, c, back=.06, z=1.1, size=(.62, .58, .46))
        h.ball((0, .12, .9), (.5, .28, .52), c["hair"], seg=14)                              # back curtain
        for sx in (-1, 1):
            h.ball((sx * .26, .0, .9), (.12, .26, .4), c["hair"], seg=10)
        h.ball((.06, -.2, 1.15), (.4, .12, .13), c["hair"], seg=12, rot=(0, -8, 0))
    elif style == "ponytail":
        _cap(h, c, size=(.6, .56, .42))
        h.cyl((0, .27, 1.1), (.09, .09), .05, c["acc"], seg=10, rot=(80, 0, 0))             # hair tie
        h.ball((0, .32, 1.0), (.16, .16, .26), c["hair"], seg=10, rot=(20, 0, 0))
        h.ball((0, .34, .84), (.11, .11, .16), c["hair"], seg=8)
        h.ball((-.08, -.19, 1.15), (.34, .12, .12), c["hair"], seg=12, rot=(0, 10, 0))
    elif style == "twintails":
        _cap(h, c, back=.05, size=(.6, .56, .42))
        for sx in (-1, 1):
            h.ball((sx * .3, .06, 1.1), (.08, .08, .08), c["acc"], seg=8)
            h.ball((sx * .36, .07, .95), (.16, .15, .3), c["hair"], seg=10, rot=(0, sx * -15, 0))
        h.ball((0, -.2, 1.15), (.46, .12, .12), c["hair"], seg=14)
    elif style == "spiky":
        _cap(h, c, size=(.58, .54, .38))
        for i, (x, y, rx, ry) in enumerate(((-.15, -.1, -20, -25), (0, -.15, -35, 0), (.15, -.1, -20, 25),
                                            (-.12, .1, 25, -20), (.12, .1, 25, 20), (0, .02, 0, 0))):
            h.cyl((x, y, 1.28), (.14, .14), .16, c["hair"], seg=6, top=.1, rot=(rx, ry, 0))
        h.ball((0, -.2, 1.14), (.38, .1, .1), c["hair"], seg=10)
    elif style == "buzz":
        h.ball((0, .01, 1.03), (.575, .52, .5), c["hair"], seg=18)                          # close crop
    elif style == "afro":
        h.ball((0, .05, 1.17), (.74, .66, .56), c["hair"], seg=18)
        for x in (-.15, 0, .15):
            h.ball((x, -.22, 1.13), (.16, .1, .12), c["hair"], seg=8)
    elif style == "swoop":
        _cap(h, c, size=(.6, .56, .4))
        h.ball((.06, -.12, 1.25), (.44, .3, .2), c["hair"], seg=14, rot=(-15, -12, 0))      # big quiff
        h.ball((-.24, -.08, 1.08), (.1, .2, .2), c["hair"], seg=8)
    elif style == "hijab":
        h.ball((0, .05, 1.03), (.66, .56, .62), c["hair"], seg=20)                          # wrap around face
        h.ball((0, .1, 1.3), (.3, .26, .1), c["hair"], seg=12)                               # soft top fold
    elif style == "tuft":
        _cap(h, c, size=(.58, .54, .38))
        h.cyl((.02, -.02, 1.33), (.06, .04), .12, c["hair"], seg=6, top=.1, rot=(-25, 20, 0))   # antenna tuft
        h.ball((0, -.2, 1.14), (.3, .1, .1), c["hair"], seg=10)
    h.done_bone()


# --------------------------------------------------------------------------- accessories
def accessories(p, c):
    for acc in c.get("accs", []):
        a = p("ACC_" + acc, "head")
        if acc == "glasses":
            for sx in (-1, 1):
                a.cyl((sx * .1, FACE_Y - .012, 1.0), (.12, .12), .014, c["acc"], seg=16, rot=(90, 0, 0))
                a.cyl((sx * .1, FACE_Y - .02, 1.0), (.1, .1), .004, "glass", seg=16, rot=(90, 0, 0), outline=False)
            a.box((0, FACE_Y - .012, 1.01), (.08, .012, .012), c["acc"], bevel=0)
        elif acc == "headphones":
            for i in range(9):
                deg = -80 + i * 20
                x, z = math.sin(math.radians(deg)) * .31, math.cos(math.radians(deg)) * .31
                a.box((x, .02, 1.02 + z), (.07, .06, .04), c["acc"], bevel=.012, rot=(0, deg, 0))
            for sx in (-1, 1):
                a.cyl((sx * .29, 0, .99), (.15, .15), .07, c["acc"], seg=14, rot=(0, 90, 0), bevel=.012)
        elif acc == "beanie":
            a.ball((0, .03, 1.13), (.62, .58, .44), c["acc"], seg=18)
            a.cyl((0, .03, 1.02), (.62, .58), .07, c["acc"], seg=18, bevel=.02)
            a.ball((0, .05, 1.37), (.1, .1, .1), "white", seg=10)
        elif acc == "cap":
            a.ball((0, .02, 1.12), (.61, .57, .46), c["acc"], seg=18)
            a.box((0, -.3, 1.11), (.34, .2, .025), c["acc"], bevel=.012, rot=(-6, 0, 0))     # brim
            a.ball((0, .02, 1.35), (.05, .05, .03), "white", seg=8)
        elif acc == "bow":
            for sx in (-1, 1):
                a.ball((.18 + sx * .055, -.08, 1.24), (.1, .05, .08), c["acc"], seg=8, rot=(0, sx * 20, 0))
            a.ball((.18, -.1, 1.24), (.04, .04, .04), c["acc"], seg=8)
        elif acc == "beard":
            a.ball((0, -.13, .825), (.34, .18, .13), c["hair"], seg=14)
            for sx in (-1, 1):
                a.ball((sx * .2, -.05, .88), (.07, .12, .12), c["hair"], seg=8)
        elif acc == "mustache":
            for sx in (-1, 1):
                a.ball((sx * .028, surf(sx * .028, .94) - .006, .94), (.06, .025, .026), c["hair"], seg=8,
                       rot=(0, sx * -15, 0))
        elif acc == "freckles":
            for sx in (-1, 1):
                for dx, dz in ((0, 0), (.03, .015), (.035, -.018)):
                    x, z = sx * (.13 + dx), .96 + dz
                    a.ball((x, surf(x, z) - .002, z), (.012, .006, .012), "wood_dark", seg=6, outline=False)
        elif acc == "earrings":
            for sx in (-1, 1):
                a.ball((sx * .285, -.01, .9), (.035, .035, .035), "butter", seg=8)
        elif acc == "flower":
            for i in range(5):
                deg = i * 72
                a.ball((.2 + math.cos(math.radians(deg)) * .03, -.12, 1.2 + math.sin(math.radians(deg)) * .03),
                       (.04, .02, .04), "coral", seg=8)
            a.ball((.2, -.13, 1.2), (.03, .02, .03), "butter", seg=8)
        a.done_bone()
    if c.get("scarf"):
        b = p("ACC_scarf", "spine")
        b.cyl((0, 0, .8), (.34, .3), .08, c["scarf"], seg=16, bevel=.02)
        b.box((.08, -.16, .68), (.08, .03, .18), c["scarf"], bevel=.015, rot=(0, -8, 0))
        b.done_bone()
    if c.get("hijab"):   # drape over shoulders, matching the head wrap
        b = p("ACC_drape", "spine")
        b.ball((0, .0, .77), (.46, .38, .2), c["hair"], seg=16)
        b.ball((0, -.1, .7), (.26, .1, .2), c["hair"], seg=10)
        b.done_bone()
    if c.get("badge"):   # lanyard badge on the torso
        b = p("ACC_badge", "spine")
        for sx in (-1, 1):
            b.stick((sx * .09, -.12, .79), (sx * .02, -.18, .62), .012, c["acc"], seg=5, outline=False)
        b.box((0, -.185, .57), (.08, .015, .1), "white", bevel=.008)
        b.box((0, -.194, .59), (.05, .004, .03), c["acc"], bevel=0, outline=False)
        b.done_bone()
