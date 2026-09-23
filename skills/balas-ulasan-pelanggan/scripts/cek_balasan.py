#!/usr/bin/env python3
"""Periksa draf balasan ulasan publik sebelum diposting.

Yang diperiksa:
- Data pribadi/pesanan yang bocor: nomor HP, email, nomor pesanan/invoice/resi, alamat.
- Ajakan ke luar platform (di marketplace dilarang; di Google Maps boleh memakai kontak resmi usaha).
- Kalimat defensif/menyalahkan pembeli, dan janji mutlak.
- Kelengkapan: ucapan terima kasih, permintaan maaf (ulasan negatif), arahan ke chat pribadi.
- Panjang terhadap batas AMAN (bukan batas resmi; cek batas terbaru di platform).

Hanya library standar Python 3.8+. Tidak ada akses jaringan.
Contoh:
  python3 cek_balasan.py --platform shopee --jenis negatif --teks "Halo Kak, mohon maaf ..."
"""
import argparse
import json
import re
import sys

# Windows: pastikan teks Indonesia/emoji tercetak tanpa error encoding
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

BATAS_AMAN = {"shopee": 500, "tokopedia": 500, "tiktok": 500, "google": 4000, "lainnya": 1000}
MARKETPLACE = {"shopee", "tokopedia", "tiktok"}
ALIAS = {"tokped": "tokopedia", "gmaps": "google", "google-maps": "google", "maps": "google",
         "tiktokshop": "tiktok", "tts": "tiktok"}

POLA_DATA = [
    (r"(?:\+?62|\b0)8[\d\s.\-]{7,14}\d", "nomor HP"),
    (r"\b[\w.+-]+@[\w-]+\.[\w.]+\b", "alamat email"),
    (r"\bINV/[\w/]+", "nomor invoice"),
    (r"\b(?=[A-Z0-9]*\d)(?=[A-Z0-9]*[A-Z])[A-Z0-9]{10,}\b", "kode pesanan/resi"),
    (r"\b\d{10,}\b", "deretan angka panjang (nomor pesanan/resi/HP?)"),
    (r"\b(?:jl\.?|jalan|gg\.?|gang)\s+[A-Z][\w.]*(?:\s+[A-Z][\w.]*)*(?:\s+no\.?\s*\d+\w*)"
     r"|\brt\s*\.?\s*\d+\s*/\s*rw\s*\.?\s*\d+|\b(?:rt|rw)\s*\.?\s*0\d+\b|\bblok\s+[a-z]\s*-?\s*\d+|\bkel\.\s*\w+|\bkec\.\s*\w+",
     "detail alamat"),
    (r"\b(?:resi|no\.?\s*pesanan|order\s*id|nomor\s+pesanan)\s*[:#]?\s*\w+", "nomor pesanan/resi"),
]
# Perlu dicek manusia (bisa benar, bisa bocor)
POLA_CEK_DATA = [
    (r"\b(?:Kak|Kakak|Bu|Ibu|Pak|Bapak|Mbak|Mba|Mas|Bang|Teh|Sis|Gan|Om|Tante)\.?\s+[A-Z][a-z]+\s+[A-Z][a-z]+",
     "kemungkinan NAMA LENGKAP pembeli — cukup sapaan + nama panggilan/nama akun"),
    (r"\b(?:bilang|dibilang|katanya|kata\s+(?:kakak|ibu|bapak|anda)|menulis|tulis|chat(?:nya)?|di\s+chat"
     r"|pesan(?:nya)?|sms|wa(?:nya)?)\s*(?:ke\s+kami\s*)?[:,]?\s*[\"'“‘]",
     "kemungkinan KUTIPAN CHAT PRIBADI — jangan ungkap isi chat di balasan publik"),
    (r"\b(?:[Jj]l\.?|[Jj]alan|[Gg]g\.?|[Gg]ang)\s+[A-Z][a-z]+", "kemungkinan nama jalan — pastikan bukan alamat pembeli"),
]
POLA_LUAR = [
    (r"https?://\S+|www\.\S+|wa\.me\S*", "link"),
    (r"\b(?:whats\s?app|telegram|line\s*(?:id|@)|dm\s+ig|instagram)\b|\bwa\s*(?:ke|di|:|\d|kami|admin|toko)\b"
     r"|\b(?:via|lewat|hubungi|chat|kontak)\s+wa\b", "ajakan ke aplikasi lain"),
    (r"(?<![\w.])@[A-Za-z0-9_.]{2,}[A-Za-z0-9_]", "@akun"),
]
POLA_DEFENSIF = [
    r"\banda\s+salah\b", r"\bkakak\s+(?:yang\s+)?salah\b", r"\btidak\s+mungkin\b", r"\bmustahil\b",
    r"\bbukan\s+salah\s+kami\b", r"\bbukan\s+tanggung\s+jawab\s+kami\b", r"(?<!yang\s)\bseharusnya\s+(?:kakak|anda|agan|sis)\b(?!\s+(?:dapat|dapatkan|terima|alami|rasakan|nikmati))",
    r"\bbaca\s+(?:dulu\s+)?deskripsi\b", r"\bsudah\s+(?:kami\s+)?(?:jelaskan|tulis)\b", r"\bfitnah\b",
    r"\bhoaks?\b", r"\bbohong\b", r"\bkami\s+laporkan\b", r"\bpolisi\b", r"\buu\s*ite\b", r"\bmakanya\b",
    r"\bsalah\s+(?:kurir|ekspedisi)\b", r"\bpembeli\s+lain\s+(?:tidak|gak|nggak)\b", r"\bjangan\s+asal\b",
    r"\bkomplain\s+terus\b", r"\bharusnya\s+ngerti\b",
]
POLA_JANJI = [r"\bpasti\b", r"\bdijamin\b", r"\b100\s*%", r"\brefund\s+penuh\b", r"\bganti\s+rugi\b",
              r"\bgratis\s+selamanya\b"]
POLA_IMBALAN = [r"\bubah\s+(?:ulasan|review|bintang|rating)\b", r"\bganti\s+(?:bintang|rating|ulasan)\b",
                r"\bhapus\s+(?:ulasan|review)\b", r"\b(?:bintang|rating)\s*5\b.*\b(?:voucher|hadiah|cashback|bonus)\b",
                r"\b(?:voucher|hadiah|cashback|bonus)\b.*\b(?:bintang|rating)\s*5\b"]
POLA_MAAF = r"\b(?:maaf|mohon\s+maaf|meminta\s+maaf|minta\s+maaf)\b"
POLA_TERIMA_KASIH = r"\b(?:terima\s*kasih|makasih|trima\s*kasih|thank)"
POLA_ESKALASI = r"\b(?:chat|pesan|hubungi|kirim(?:kan)?\s+(?:detail|nomor)|inbox|telepon|telp|dm)\b"


def galat(pesan):
    print("ERROR: " + pesan, file=sys.stderr)
    sys.exit(1)


def panjang(t):
    return max(len(t), len(t.encode("utf-16-le")) // 2)


def temukan(pola, teks, flags=re.IGNORECASE):
    return sorted({m.group(0).strip() for m in re.finditer(pola, teks, flags)})


def periksa(teks, platform, jenis):
    temuan = []
    for pola, label in POLA_DATA:
        fl = 0 if label == "kode pesanan/resi" else re.IGNORECASE
        for x in temukan(pola, teks, fl):
            temuan.append(("GAGAL", "Kemungkinan data pribadi/pesanan terlihat publik ({}): '{}'. Hapus.".format(label, x)))
    for pola, label in POLA_CEK_DATA:
        for x in temukan(pola, teks, 0 if "NAMA" in label or "jalan" in label else re.IGNORECASE):
            temuan.append(("CEK", "PRIVASI — {}: '{}'.".format(label[0].upper() + label[1:], x)))
    for pola, label in POLA_LUAR:
        for x in temukan(pola, teks):
            if platform in MARKETPLACE:
                temuan.append(("GAGAL", "Ajakan/kontak di luar platform ({}): '{}'. Di marketplace arahkan ke fitur chat toko.".format(label, x)))
            else:
                temuan.append(("CEK", "Kontak/link ({}): '{}'. Boleh hanya jika kontak RESMI usaha, bukan data pelanggan.".format(label, x)))
    for pola in POLA_DEFENSIF:
        for x in temukan(pola, teks):
            temuan.append(("CEK", "Nada defensif/menyalahkan: '{}'. Ganti dengan pengakuan & solusi.".format(x)))
    for pola in POLA_JANJI:
        for x in temukan(pola, teks):
            temuan.append(("CEK", "Janji mutlak/kompensasi: '{}'. Pastikan pemilik usaha menyetujui & sanggup.".format(x)))
    for pola in POLA_IMBALAN:
        for x in temukan(pola, teks):
            temuan.append(("GAGAL", "Meminta ubah/hapus ulasan atau imbalan rating: '{}'. Melanggar kebijakan platform.".format(x)))

    ada_terima_kasih = bool(re.search(POLA_TERIMA_KASIH, teks, re.IGNORECASE))
    ada_maaf = bool(re.search(POLA_MAAF, teks, re.IGNORECASE))
    ada_eskalasi = bool(re.search(POLA_ESKALASI, teks, re.IGNORECASE))
    if not ada_terima_kasih:
        temuan.append(("SARAN", "Belum ada ucapan terima kasih atas ulasannya."))
    if jenis == "negatif":
        if not ada_maaf:
            temuan.append(("SARAN", "Ulasan negatif: tambahkan permintaan maaf atas pengalaman pembeli."))
        if not ada_eskalasi:
            temuan.append(("SARAN", "Ulasan negatif: arahkan ke chat pribadi untuk penyelesaian."))
    if jenis == "positif" and ada_maaf:
        temuan.append(("SARAN", "Ulasan positif tidak perlu permintaan maaf; cek lagi konteksnya."))

    n = panjang(teks)
    batas = BATAS_AMAN[platform]
    if n > batas:
        temuan.append(("GAGAL", "Panjang {} karakter melebihi batas aman {} (cek batas terbaru). Pangkas {} karakter.".format(
            n, batas, n - batas)))
    elif n > 600:
        temuan.append(("SARAN", "Balasan {} karakter; idealnya 150–600 agar tetap dibaca.".format(n)))
    elif n < 60:
        temuan.append(("SARAN", "Balasan sangat pendek ({} karakter); terasa seperti template.".format(n)))

    return {
        "platform": platform, "jenis": jenis, "panjang": n, "batas_aman": batas,
        "lulus": not any(t == "GAGAL" for t, _ in temuan),
        "perlu_dicek_privasi": any(p.startswith("PRIVASI") for _, p in temuan),
        "temuan": [{"tingkat": t, "pesan": p} for t, p in temuan],
        "catatan": "Batas panjang adalah batas aman skill, bukan batas resmi. Cek di platform.",
    }


def main():
    p = argparse.ArgumentParser(description="Periksa draf balasan ulasan pelanggan.")
    p.add_argument("--platform", required=True, help="shopee, tokopedia, tiktok, google, atau lainnya")
    p.add_argument("--jenis", required=True, choices=["positif", "netral", "negatif"], help="jenis ulasan yang dibalas")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--teks", help="teks balasan")
    g.add_argument("--file", help="file .txt berisi teks balasan")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()

    pf = ALIAS.get(a.platform.lower().strip(), a.platform.lower().strip())
    if pf not in BATAS_AMAN:
        galat("Platform '{}' tidak dikenal. Pilih: shopee, tokopedia, tiktok, google, lainnya.".format(a.platform))
    if a.file:
        try:
            with open(a.file, encoding="utf-8-sig") as f:
                teks = f.read()
        except FileNotFoundError:
            galat("File tidak ditemukan: {}".format(a.file))
        except UnicodeDecodeError:
            galat("File harus teks UTF-8.")
    else:
        teks = a.teks
    teks = (teks or "").strip()
    if not teks:
        galat("Teks balasan kosong.")

    h = periksa(teks, pf, a.jenis)
    if a.json:
        print(json.dumps(h, ensure_ascii=False, indent=2))
        return
    print("Platform: {} | Jenis: {} | Panjang: {}/{} | {}".format(
        pf, a.jenis, h["panjang"], h["batas_aman"],
        "PERLU DIPERBAIKI" if not h["lulus"] else ("PERLU DICEK (privasi)" if h["perlu_dicek_privasi"] else "LULUS")))
    if not h["temuan"]:
        print("Tidak ada temuan.")
    for t in h["temuan"]:
        print("[{}] {}".format(t["tingkat"], t["pesan"]))
    print(h["catatan"])


if __name__ == "__main__":
    main()
