"""Daftar item katalog. Tiap item dibangun di titik asal: alas z=0, depan = +Y. Item dinding: punggung di y=0 menghadap +Y,
z=0 = tepi bawah item (app memasang di tinggi z_pasang)."""
REG = []   # dict(id, cat, label, fn, tint, mount, z, used)

CATS = ["duduk", "meja", "simpan", "dapur", "tidur", "dinding", "tanaman", "karpet", "meja_kecil", "lampu", "studio", "struktur"]
CAT_LABEL = {"duduk": "Tempat duduk", "meja": "Meja", "simpan": "Penyimpanan", "dapur": "Pantry & dapur", "tidur": "Tempat tidur",
             "dinding": "Dekorasi dinding", "tanaman": "Tanaman", "karpet": "Karpet & lantai", "meja_kecil": "Barang di meja / elektronik",
             "lampu": "Lampu & pendingin", "studio": "Studio & rapat", "struktur": "Struktur (pintu, jendela, tangga)"}
MOUNT_Z = {"floor": 0.0, "table": 0.0, "wall": 1.2, "ceiling": 3.2}


def reg(cat, id, label, fn, tint=None, mount="floor", used=False, z=None):
    assert cat in CATS, cat
    assert all(r["id"] != id for r in REG), "id ganda " + id
    REG.append(dict(id=id, cat=cat, label=label, fn=fn, tint=tint or {}, mount=mount, used=used, z=MOUNT_Z[mount] if z is None else z))


def item(cat, id, label, tint=None, mount="floor", z=None):
    def d(fn):
        reg(cat, id, label, fn, tint, mount, False, z)
        return fn
    return d
