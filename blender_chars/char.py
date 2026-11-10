"""Rakit satu karakter dari preset."""
import lib, body, p_hair, p_face, p_outfit, p_acc, presets
import p_extra  # noqa: F401  (mendaftarkan part gelombang 2)


def make_character(key, pr, x, y=0, z=0):
    c = lib.Ctx(f"CH_{key}", tag=f"@{key}", colors=presets.colors(pr), offset=(x, y, z))
    body.build_body(c)
    hat = any(a in p_acc.HEAD_HAT for a in pr["acc"])
    p_hair.HAIR[pr["hair_style"]](c, top=not hat)   # topi menutup rambut -> HAIRTOP tidak dibuat
    p_face.FACE[pr["face"]](c)
    p_face.MOUTH[pr["mouth"]](c)
    if pr["blush"]:
        p_face.blush(c)
    if pr["fhair"]:
        p_face.FHAIR[pr["fhair"]](c)
    p_outfit.TOP[pr["top"]](c)
    p_outfit.BOTTOM[pr["bottom"]](c)
    p_outfit.SHOES[pr["shoes"]](c)
    for a in pr["acc"]:
        p_acc.ACC[a](c)
    return c
