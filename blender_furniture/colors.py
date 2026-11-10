"""Palet pilihan warna untuk customizer. Tiap keluarga = daftar (nama, hex). Item menandai material mana yang bisa diganti user
dan keluarga palet-nya (kunci 'tint'). Hex = warna dasar material (app boleh menambah pemilih hex bebas)."""
FAMILIES = {
    "kain": ("Kain / bantalan / kulit", [
        ("Biru", "#6E8CA8"), ("Navy", "#4A5C77"), ("Toska", "#6F9E9A"), ("Hijau sage", "#96AB8C"), ("Hijau", "#6FA36B"),
        ("Kuning", "#E2BE5A"), ("Oranye", "#D68F5E"), ("Merah", "#B9574F"), ("Rose", "#C98F94"), ("Ungu", "#9D8BAF"),
        ("Krem", "#E9DCC6"), ("Abu", "#9AA0A8"), ("Charcoal", "#454B55"), ("Burgundy", "#7A2E3A"), ("Zaitun", "#7A7A3A"),
        ("Cokelat kulit", "#7A4A2E"), ("Hitam", "#2A2E34"), ("Putih", "#F4F0E8")]),
    "kayu": ("Kayu / permukaan meja", [
        ("Oak", "#D2B48C"), ("Kayu sedang", "#A9825A"), ("Kayu tua", "#6A4E34"), ("Kayu meja", "#C09A6B"), ("Putih gading", "#EDE6D8"),
        ("Walnut", "#5A3A29"), ("Eboni", "#2E2420"), ("Birch", "#E8D9B8"), ("Ceri", "#8A4B38"), ("Abu kayu", "#A8A39A"),
        ("Hitam", "#2A2E34"), ("Pinus", "#DDBE8C")]),
    "cat": ("Warna cat / plastik / aksen", [
        ("Merah", "#C9483F"), ("Biru", "#3F6FB5"), ("Kuning", "#E5B93C"), ("Hijau", "#4E9A5A"), ("Oranye", "#E08A3C"),
        ("Pink", "#E48FA6"), ("Ungu", "#8A68B8"), ("Cyan", "#44A8C4"), ("Putih", "#F5F5F2"), ("Abu", "#8E949B"),
        ("Hitam", "#2A2E34"), ("Navy", "#2F4B7C"), ("Mint", "#8FD3B6"), ("Krem", "#EFE3C8")]),
    "logam": ("Logam / rangka", [
        ("Perak", "#B7BBC1"), ("Abu logam", "#5C626B"), ("Krom", "#D5D9DD"), ("Hitam", "#2A2E34"), ("Putih", "#F5F5F2"),
        ("Emas", "#D4AF37"), ("Kuningan", "#C9A24D"), ("Tembaga", "#B87333"), ("Biru logam", "#3E5C8A"), ("Hijau logam", "#3E7A52")]),
    "layar": ("Warna layar / lampu", [
        ("Biru", "#4F86C6"), ("Toska", "#3FA79B"), ("Hangat", "#E0A35A"), ("Rose", "#C97F8F"), ("Hijau", "#6FA86B"),
        ("Violet", "#8A6FC0"), ("Putih hangat", "#FFF3C9"), ("Putih dingin", "#E8F2FF")]),
    "karpet": ("Karpet / tirai / tekstil", [
        ("Merah", "#A85B52"), ("Toska", "#4E7E7A"), ("Krem", "#E2D4B9"), ("Rose", "#BD8A94"), ("Sage", "#8CA07F"),
        ("Biru", "#5F7E9E"), ("Navy", "#3E4F6B"), ("Mustard", "#C79A3C"), ("Abu", "#9AA0A8"), ("Charcoal", "#454B55"),
        ("Ungu", "#8B77A8"), ("Oranye", "#D68F5E")]),
    "daun": ("Warna daun", [
        ("Hijau", "#4F8A4B"), ("Hijau muda", "#6FA85A"), ("Hijau tua", "#3E7A52"), ("Zaitun", "#6B7A3A"), ("Hijau biru", "#3F8F7A"),
        ("Variegata", "#9CC47A"), ("Merah anggur", "#7A3A4A")]),
    "pot": ("Warna pot / vas", [
        ("Terakota", "#B5694A"), ("Putih", "#E8E2D6"), ("Hitam", "#2A2E34"), ("Abu", "#8E949B"), ("Biru", "#5F7E9E"),
        ("Hijau sage", "#96AB8C"), ("Kuning", "#E5B93C"), ("Pink", "#E48FA6")]),
    "dinding": ("Warna dinding / panel", [
        ("Navy", "#44546E"), ("Krem", "#F2E8D6"), ("Putih", "#FBF8F1"), ("Sage", "#C9D6C0"), ("Peach", "#EFCDB4"),
        ("Langit", "#CBDDE8"), ("Butter", "#F0E2A8"), ("Lilac", "#D9CFE6")]),
    "lantai": ("Warna lantai", [
        ("Kayu terang", "#C9A77C"), ("Kayu tengah", "#BF9B6F"), ("Kayu tua", "#7C6347"), ("Abu", "#B9BDC2"), ("Ubin putih", "#EFE9DD"),
        ("Ubin hijau", "#9FB5A8"), ("Biru", "#A6C9E2"), ("Sage", "#AFD0A4"), ("Peach", "#EDBF9C"), ("Lilac", "#C2B0DC"), ("Butter", "#F0D98E")]),
}


def spec():
    return {k: {"label": lab, "pilihan": [{"nama": n, "hex": h} for n, h in cols]} for k, (lab, cols) in FAMILIES.items()}
