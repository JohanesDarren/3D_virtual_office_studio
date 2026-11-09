"""Perabot yang SUDAH dipakai di kantor v5/v6 (furn_used.py = salinan blender_v5/furn.py, tidak diubah)."""
import furn_used as F
from registry import reg

K = "kain"; W = "kayu"; C = "cat"; L = "logam"; S = "layar"; P = "karpet"; D = "daun"; PT = "pot"


def u(cat, id, label, fn, tint=None, mount="floor", z=None):
    reg(cat, id, label, fn, tint, mount, True, z)


# duduk
u("duduk", "kursi_putar", "Kursi putar", lambda: F.chair(0, 0), {"fab_blue": K})
u("duduk", "kursi_kayu", "Kursi kayu", lambda: F.plain_chair(0, 0), {"wood": W})
u("duduk", "bangku_bulat", "Bangku bulat", lambda: F.stool(0, 0), {"fab_orange": K})
u("duduk", "sofa_3", "Sofa 3 dudukan", lambda: F.sofa(0, 0), {"fab_navy": K, "fab_orange": K, "fab_cream": K})
u("duduk", "kursi_santai", "Kursi santai (armchair)", lambda: F.armchair(0, 0), {"fab_rose": K, "fab_cream": K})
u("duduk", "beanbag", "Beanbag", lambda: F.beanbag(0, 0), {"fab_red": K})
u("duduk", "kursi_sutradara", "Kursi sutradara", lambda: F.director_chair(0, 0), {"fab_red": K})
# meja
u("meja", "meja_kerja", "Meja kerja + kursi + PC", lambda: F.desk(0, 0), {"desk_white": W, "desk_wood": W, "scr_blue": S})
u("meja", "sekat_rendah", "Sekat rendah", lambda: F.partition_low(0, 0), {"fab_sage": K})
u("meja", "meja_kopi", "Meja kopi", lambda: F.coffee_table(0, 0), {"wood": W})
u("meja", "meja_makan", "Meja makan + 4 kursi", lambda: F.dining_table(0, 0), {"oak": W})
u("meja", "meja_rapat", "Meja rapat + 11 kursi", lambda: F.meeting_table(0, 0), {"wood": W, "wood_dark": W})
u("meja", "meja_resepsionis", "Meja resepsionis", lambda: F.reception_counter(0, 0), {"wood": W, "counter": W})
u("meja", "meja_bar", "Meja bar camilan + stool", lambda: F.snack_bar(0, 0), {"wood_dark": W, "counter": W})
u("meja", "meja_game", "Meja papan permainan", lambda: F.game_board(0, 0), {"wood": W})
u("meja", "meja_printer", "Meja printer", lambda: F.printer_station(0, 0), {"desk_wood": W})
# simpan
u("simpan", "rak_buku", "Rak buku (berisi)", lambda: F.bookshelf(0, 0), {"wood_dark": W, "wood": W})
u("simpan", "rak_pajangan", "Rak buku + figur", lambda: F.bookshelf(0, 0, figs=True), {"wood_dark": W, "wood": W})
u("simpan", "rak_konsol", "Rak konsol game", lambda: F.console_shelf(0, 0), {"wood_dark": W, "wood": W})
u("simpan", "loker_4", "Loker 4 pintu", lambda: F.locker_row(0, 0), {"fab_blue": C, "fab_teal": C, "fab_sage": C, "fab_orange": C})
u("simpan", "lemari_pakaian", "Lemari pakaian", lambda: F.wardrobe(0, 0), {"wood": W, "oak": W})
u("simpan", "nakas", "Nakas + lampu", lambda: F.nightstand(0, 0), {"wood": W})
u("simpan", "lemari_arsip", "Lemari arsip", lambda: F.filing_cabinet(0, 0), {"metal": L})
u("simpan", "rak_sepatu", "Rak sepatu", lambda: F.shoe_rack(0, 0), {"wood": W})
u("simpan", "rak_brosur", "Rak brosur", lambda: F.brochure_rack(0, 0), {"metal_dark": L})
u("simpan", "gantungan_baju", "Gantungan baju", lambda: F.coat_rack(0, 0), {"metal_dark": L})
u("simpan", "rak_dinding", "Rak dinding", lambda: F.shelf_wall(0, 0, 0), {"wood_dark": W}, "wall")
# dapur
u("dapur", "kulkas", "Kulkas", lambda: F.fridge(0, 0), {"white": C})
u("dapur", "microwave", "Microwave", lambda: F.microwave(0, 0, 0), {"white": C}, "table")
u("dapur", "vending", "Vending machine", lambda: F.vending_machine(0, 0), {"red": C})
u("dapur", "kitchen_set", "Kitchen counter + mesin kopi", lambda: F.kitchen_counter(0, 0), {"wood": W, "counter": W})
u("dapur", "dispenser_air", "Dispenser air", lambda: F.water_dispenser(0, 0), {"white": C})
u("dapur", "tempat_sampah", "Tempat sampah", lambda: F.bin_(0, 0), {"grey": C})
# tidur
u("tidur", "ranjang_tingkat", "Ranjang tingkat", lambda: F.bunk_bed(0, 0), {"fab_blue": K, "fab_sage": K})
u("tidur", "ranjang_single", "Ranjang single", lambda: F.single_bed(0, 0), {"fab_teal": K})
# dinding
u("dinding", "bingkai", "Bingkai foto", lambda: F.frame(0, 0, 0), {"wood_dark": W}, "wall")
u("dinding", "foto_tim", "Foto tim", lambda: F.team_photo(0, 0, 0), {"wood_dark": W}, "wall")
u("dinding", "sertifikat", "Sertifikat", lambda: F.certificate(0, 0, 0), {"gold": L}, "wall")
u("dinding", "bagan_org", "Bagan struktur", lambda: F.org_chart(0, 0, 0), {"wood_dark": W}, "wall")
u("dinding", "jam_dinding", "Jam dinding", lambda: F.clock(0, 0, 0), {"wood_dark": W}, "wall", 2.2)
u("dinding", "whiteboard", "Whiteboard", lambda: F.whiteboard(0, 0, 0), {"metal": L}, "wall")
u("dinding", "papan_tugas_harian", "Papan tugas harian", lambda: F.task_board(0, 0, 0, kind="daily"), {"wood_dark": W}, "wall")
u("dinding", "papan_tugas_mingguan", "Papan tugas mingguan", lambda: F.task_board(0, 0, 0, kind="weekly"), {"wood_dark": W}, "wall")
u("dinding", "poster", "Poster", lambda: F.poster(0, 0, 0), {"blue": C}, "wall")
u("dinding", "tv_dinding", "TV dinding", lambda: F.tv_wall(0, 0, 0), {"scr_blue": S}, "wall")
u("dinding", "layar_proyektor", "Layar proyektor", lambda: F.projector_screen(0, 0, 0), {"scr_blue": S}, "wall")
u("dinding", "gorden", "Gorden", lambda: F.curtain(0, 0, 0), {"fab_rose": P}, "wall")
# tanaman
u("tanaman", "tanaman_hias", "Tanaman hias", lambda: F.plant(0, 0), {"pot": PT, "leaf": D, "leaf2": D, "leaf3": D})
u("tanaman", "pohon_dalam", "Pohon dalam ruang", lambda: F.plant(0, 0, kind=1), {"pot": PT, "leaf": D, "leaf2": D, "leaf3": D})
u("tanaman", "sukulen", "Sukulen", lambda: F.plant(0, 0, kind=2), {"pot": PT, "leaf2": D})
# karpet
u("karpet", "karpet_3_lapis", "Karpet 3 lapis", lambda: F.rug(0, 0, 2.4, 1.6), {"rug_red": P, "rug_cream": P})
# meja kecil / elektronik
u("meja_kecil", "monitor", "Monitor", lambda: F.monitor(0, 0, 0), {"scr_blue": S}, "table")
u("meja_kecil", "figur", "Action figure", lambda: F.figure(0, 0, 0, col="red", s=1.6), {"red": C}, "table")
u("meja_kecil", "piala", "Piala", lambda: F.trophy(0, 0, 0), {"gold": L}, "table")
u("meja_kecil", "tumpukan_buku", "Tumpukan buku", lambda: F.book_stack(0, 0, 0), {"blue": C, "red": C, "green": C}, "table")
u("meja_kecil", "gamepad", "Gamepad", lambda: F.gamepad(0, 0, 0), {"blue": C}, "table")
u("meja_kecil", "tv_konsol", "TV + meja + konsol", lambda: F.tv(0, 0), {"wood_dark": W, "scr_blue": S})
# lampu / pendingin
u("lampu", "ac_dinding", "AC dinding", lambda: F.ac_unit(0, 0, 0), {"white": C}, "wall", 2.5)
u("lampu", "proyektor_langit", "Proyektor langit-langit", lambda: F.ceiling_projector(0, 0, 0), {"white": C}, "ceiling")
# studio
u("studio", "backdrop", "Backdrop green screen", lambda: F.backdrop_stand(0, 0), {"green_screen": C})
u("studio", "softbox", "Softbox", lambda: F.softbox(0, 0), {"black": L})
u("studio", "tripod_kamera", "Tripod kamera", lambda: F.tripod_camera(0, 0), {"black": L})
