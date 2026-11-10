"""Pilihan warna untuk customizer di app. Tiap kelompok = satu material bernama (M_*) yang di-tint app.
Preset 11 karakter boleh memakai warna di luar palet; UI sebaiknya juga menyediakan pemilih warna bebas (hex)."""

PALETTES = {
    "M_skin": ("Warna kulit", [
        ("Porselen", "#FBE0CB"), ("Cerah", "#F5CBA7"), ("Sawo muda", "#E8B98D"), ("Sawo", "#D9A97E"),
        ("Sawo matang", "#C69063"), ("Cokelat", "#A9774F"), ("Cokelat tua", "#8A5A3B"), ("Gelap", "#5E3B28")]),
    "M_hair": ("Warna rambut", [
        ("Hitam", "#141018"), ("Cokelat tua", "#2B1D14"), ("Cokelat", "#4A2C1A"), ("Cokelat muda", "#7A4B2A"),
        ("Pirang", "#C98A3E"), ("Pirang pucat", "#E8C872"), ("Jahe", "#A8431F"), ("Abu", "#8A8D93"),
        ("Putih", "#E8E8EC"), ("Ungu", "#6D28D9"), ("Pink", "#EC4899"), ("Biru", "#2563EB"), ("Toska", "#0D9488")]),
    "M_eye": ("Warna mata", [
        ("Hitam", "#1C120B"), ("Cokelat tua", "#2A1A12"), ("Cokelat", "#4A2C1A"), ("Hazel", "#7C4A1E"),
        ("Hijau", "#2F6B3F"), ("Biru", "#0F3D5E"), ("Abu", "#4B5563"), ("Ungu", "#4C1D95")]),
    "M_mouth": ("Warna bibir", [
        ("Merah bata", "#B5503E"), ("Merah muda", "#D9768A"), ("Merah", "#C8323C"), ("Cokelat", "#8C4A3A"),
        ("Koral", "#E2725B"), ("Mauve", "#A8586B")]),
    "M_blush": ("Warna pipi (blush)", [
        ("Pink", "#F28BA8"), ("Persik", "#F6A78F"), ("Pink tua", "#F472B6"), ("Koral", "#F08A7C"), ("Lembut", "#F4B6C2")]),
    "M_top": ("Warna atasan", [
        ("Navy", "#1E3A8A"), ("Biru", "#2563EB"), ("Biru langit", "#38BDF8"), ("Toska", "#0D9488"), ("Hijau", "#16A34A"),
        ("Lime", "#84CC16"), ("Kuning", "#FACC15"), ("Oranye", "#EA580C"), ("Mustard", "#D97706"), ("Merah", "#DC2626"),
        ("Pink", "#EC4899"), ("Pink muda", "#F472B6"), ("Ungu", "#7C3AED"), ("Abu", "#475569"), ("Hitam", "#1F2937"),
        ("Putih", "#F8FAFC"), ("Krem", "#F5E6C8"), ("Cokelat", "#78350F")]),
    "M_top2": ("Warna aksen atasan (kerah, garis, kancing)", [
        ("Putih", "#F8FAFC"), ("Krem", "#FEF3C7"), ("Mint", "#CCFBF1"), ("Biru muda", "#DBEAFE"), ("Pink muda", "#FCE7F3"),
        ("Oranye muda", "#FFEDD5"), ("Biru langit", "#38BDF8"), ("Kuning", "#FACC15"), ("Abu", "#CBD5E1"), ("Hitam", "#1F2937")]),
    "M_bottom": ("Warna bawahan", [
        ("Navy gelap", "#1F2A44"), ("Denim", "#334155"), ("Hitam", "#111827"), ("Abu", "#374151"), ("Krem", "#D6C3A1"),
        ("Cokelat", "#4B3B2A"), ("Khaki", "#A8956B"), ("Hijau tua", "#14532D"), ("Maroon", "#7F1D1D"), ("Ungu", "#6B5B95"),
        ("Biru", "#2563EB"), ("Putih", "#F2F2EC")]),
    "M_shoes": ("Warna sepatu", [
        ("Putih", "#F2F2EC"), ("Hitam", "#1F2937"), ("Abu", "#9CA3AF"), ("Cokelat", "#78350F"), ("Merah", "#DC2626"),
        ("Biru langit", "#38BDF8"), ("Kuning", "#FACC15"), ("Pink", "#F472B6")]),
    "M_acc": ("Warna aksesori kepala (kacamata, topi, bando)", [
        ("Emas", "#E5B93C"), ("Kuning", "#FACC15"), ("Oranye", "#F59E0B"), ("Merah", "#EF4444"), ("Pink", "#EC4899"),
        ("Ungu", "#7E22CE"), ("Biru", "#2563EB"), ("Toska", "#0D9488"), ("Hijau", "#10B981"), ("Hitam", "#1F2937"),
        ("Cokelat", "#78350F"), ("Putih", "#F8FAFC")]),
    "M_acc3": ("Warna aksesori badan (dasi, celemek, tas, syal)", [
        ("Merah", "#C9483F"), ("Ungu", "#8B5CF6"), ("Oranye", "#F59E0B"), ("Hijau", "#16A34A"), ("Biru", "#2563EB"),
        ("Pink", "#F472B6"), ("Kuning", "#E5B93C"), ("Hitam", "#1F2937"), ("Abu", "#94A3B8"), ("Putih", "#F8FAFC"),
        ("Cokelat", "#78350F"), ("Toska", "#0D9488")]),
}
# material tetap (tidak ditawarkan ke user): kilau mata putih, sol sepatu gelap, detail gelap aksesori, outline navy
TETAP = ["M_eyewhite", "M_shoes2", "M_acc2", "M_glass", "outline"]


def spec():
    return {k: {"label": lab, "pilihan": [{"nama": n, "hex": h} for n, h in cols]} for k, (lab, cols) in PALETTES.items()}
