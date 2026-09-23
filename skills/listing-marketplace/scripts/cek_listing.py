#!/usr/bin/env python3
"""Periksa draf listing marketplace (judul + deskripsi) sebelum ditempel ke Seller Center.

Yang diperiksa:
- Panjang judul & deskripsi terhadap batas AMAN per platform (bisa diubah lewat argumen).
- Info kontak / ajakan transaksi di luar platform (nomor HP, link, @akun, "chat WA").
- Kata berisiko: klaim superlatif, klaim kesehatan, label resmi (halal/BPOM/SNI) yang wajib punya bukti.
- Judul: huruf kapital berlebihan, kata diulang (keyword stuffing), simbol/emoji.
- Kata kunci: mana yang sudah masuk judul/deskripsi, dan apakah kata kunci utama ada di awal judul.

Hanya memakai library standar Python (3.8+). Tidak ada akses jaringan.
Contoh:
  python3 cek_listing.py --platform tokopedia --judul "Kemeja Batik Pria Lengan Pendek" \
      --deskripsi-file deskripsi.txt --kata-kunci "kemeja batik pria,batik lengan pendek"
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

# Batas AMAN yang dipakai skill (bukan klaim batas resmi). Cek batas terbaru di Seller Center.
BATAS = {
    "shopee": {"judul_min": 0, "judul_maks": 100, "deskripsi_maks": 3000},
    "tokopedia": {"judul_min": 0, "judul_maks": 70, "deskripsi_maks": 2000},
    "tiktok": {"judul_min": 25, "judul_maks": 100, "deskripsi_maks": 2000},
}
NAMA_PLATFORM = {"shopee": "Shopee", "tokopedia": "Tokopedia", "tiktok": "TikTok Shop"}
ALIAS = {"tiktokshop": "tiktok", "tiktok-shop": "tiktok", "tts": "tiktok", "tokped": "tokopedia"}
AREA_TERLIHAT = 40  # perkiraan karakter judul yang terlihat di kartu hasil pencarian HP

POLA_KONTAK = [
    (r"(?<!\d)(?<!barcode )(?<!ean )(?<!sku )(?:\+?62[\s.\-]?|\b0)8(?:[\s.\-]?\d){7,11}(?![\d])", "nomor HP/WA"),
    (r"(?:https?://|www\.)\S+?(?=[.,;!?)]?(?:\s|$))|(?<![@\w.\-])[\w\-]+(?:\.[\w\-]+)*\.(?:com|id|co\.id|net|me|ly)\b", "link/alamat situs"),
    (r"(?<![\w.])@[A-Za-z0-9_.]{2,}[A-Za-z0-9_]", "@akun media sosial"),
    (r"\b(?:wa\.me|whats\s?app|chat\s+wa|hubungi\s+wa|dm\s+ig|line\s*id|telegram)\b", "ajakan chat di luar platform"),
    (r"\b(?:via|order|pesan|lewat|hubungi|kontak)\s+(?:wa|whatsapp|dm|ig|instagram)\b", "ajakan chat di luar platform"),
    (r"\b[\w.+-]+@[\w-]+\.[\w.]+\b", "alamat email"),
]
POLA_BERISIKO = [
    (r"\bter(?:murah|laris|baik|laku|ampuh|aman)\b", "superlatif — pakai hanya jika ada data/bukti"),
    (r"\bno\.?\s?1\b|\bnomor\s+satu\b|\b#1\b", "klaim nomor 1 — butuh bukti"),
    (r"\b(?:menyembuhkan|sembuhkan|obat|mengobati|anti\s?kanker|detoks|detox|pelangsing|melangsingkan|diabetes|hipertensi"
     r"|kolesterol|asam\s+urat|imunitas|kekebalan|herbal|khasiat|berkhasiat|terapi|stroke|maag|jantung)\b",
     "klaim kesehatan/medis — butuh bukti & izin edar yang sesuai"),
    (r"\b(?:menurunkan|turunkan|meningkatkan|tingkatkan|mencegah|cegah|menghilangkan|hilangkan|mengatasi|atasi"
     r"|menambah|mengontrol)\b.{0,25}?\b(?:kolesterol|gula\s+darah|imun|daya\s+tahan|jerawat|berat\s+badan|asam\s+urat"
     r"|tekanan\s+darah|flek|kerutan|rambut\s+rontok|stamina|nafsu\s+makan|penyakit|kanker|virus)\b",
     "klaim kesehatan/kecantikan — butuh bukti & izin edar yang sesuai"),
    (r"\baman\s+(?:untuk|bagi|buat)\s+(?:ibu\s+hamil|bumil|busui|ibu\s+menyusui|bayi|balita|anak|penderita)\b",
     "klaim keamanan untuk kelompok rentan — butuh bukti/izin"),
    (r"\b(?:halal|bpom|sni|pirt|p-irt|sertifikat)\b", "label resmi — pastikan pengguna punya nomor/sertifikat"),
    (r"(?<!rasa )(?<!varian )(?<!/)\b(?:original|ori|100%\s*asli|authentic)\b(?!\s*/)",
     "klaim keaslian — pastikan barang memang asli"),
    (r"\b(?:cod\s+luar|transfer\s+langsung|rekening)\b", "ajakan transaksi di luar platform"),
    (r"\b(?:garansi\s+seumur\s+hidup|dijamin\s+100%)\b", "janji mutlak — pastikan bisa dipenuhi"),
]
# Barang tiruan: melanggar hak merek & kebijakan marketplace -> GAGAL
POLA_TIRUAN = [
    (r"\b(?:kw\s*\d*|kw\s*super|replika|replica|grade\s*ori|ori\s*grade|mirror|premium\s+copy|1\s*:\s*1)\b"
     r"|\bmirip\s+(?:aslinya|asli|original|[A-Z][\w]+)", "indikasi barang tiruan — marketplace melarang"),
]
POLA_SIMBOL = re.compile(r"[^\w\s\-/&+,.()'\"%:]", re.UNICODE)


def panjang(teks):
    """Hitung aman: ambil yang terbesar antara jumlah karakter dan unit UTF-16 (emoji dihitung 2)."""
    return max(len(teks), len(teks.encode("utf-16-le")) // 2)


def baca_file(path):
    try:
        with open(path, encoding="utf-8-sig") as f:
            return f.read()
    except FileNotFoundError:
        galat("File tidak ditemukan: {}".format(path))
    except UnicodeDecodeError:
        galat("File {} bukan teks UTF-8. Simpan ulang sebagai .txt (UTF-8).".format(path))
    except OSError as e:
        galat("Gagal membaca {}: {}".format(path, e))


def galat(pesan):
    print("ERROR: " + pesan, file=sys.stderr)
    sys.exit(1)


def cari(pola_list, teks):
    hasil = []
    for pola, alasan in pola_list:
        for m in re.finditer(pola, teks, flags=re.IGNORECASE):
            hasil.append({"teks": m.group(0).strip(), "alasan": alasan})
    # buang duplikat
    unik, lihat = [], set()
    for h in hasil:
        k = (h["teks"].lower(), h["alasan"])
        if k not in lihat:
            lihat.add(k)
            unik.append(h)
    return unik


def periksa(platform, judul, deskripsi, kata_kunci, batas):
    temuan = []  # (tingkat, pesan)
    info = {}

    pj = panjang(judul)
    info["panjang_judul"] = pj
    info["batas_judul"] = batas["judul_maks"]
    if pj == 0:
        temuan.append(("GAGAL", "Judul kosong."))
    elif pj > batas["judul_maks"]:
        temuan.append(("GAGAL", "Judul {} karakter, melebihi batas aman {}. Pangkas {} karakter.".format(
            pj, batas["judul_maks"], pj - batas["judul_maks"])))
    if 0 < pj < batas["judul_min"]:
        temuan.append(("GAGAL", "Judul {} karakter, kurang dari minimum {} (cek batas terbaru).".format(
            pj, batas["judul_min"])))

    if deskripsi is not None:
        pd = panjang(deskripsi)
        info["panjang_deskripsi"] = pd
        info["batas_deskripsi"] = batas["deskripsi_maks"]
        if pd > batas["deskripsi_maks"]:
            temuan.append(("GAGAL", "Deskripsi {} karakter, melebihi batas aman {}. Pangkas {} karakter.".format(
                pd, batas["deskripsi_maks"], pd - batas["deskripsi_maks"])))
        elif pd < 300:
            temuan.append(("SARAN", "Deskripsi hanya {} karakter; idealnya 600+ agar info lengkap.".format(pd)))

    gabungan = judul + "\n" + (deskripsi or "")
    for h in cari(POLA_KONTAK, gabungan):
        temuan.append(("GAGAL", "Info kontak/di luar platform: '{}' ({}). Hapus — melanggar aturan marketplace.".format(
            h["teks"], h["alasan"])))
    for h in cari(POLA_TIRUAN, gabungan):
        temuan.append(("GAGAL", "'{}' — {}. Jangan dibuatkan listing untuk barang tiruan.".format(h["teks"], h["alasan"])))
    for h in cari(POLA_BERISIKO, gabungan):
        temuan.append(("CEK", "'{}' — {}.".format(h["teks"], h["alasan"])))

    huruf = [c for c in judul if c.isalpha()]
    if len(huruf) >= 10 and sum(c.isupper() for c in huruf) / len(huruf) > 0.5:
        temuan.append(("SARAN", "Judul didominasi HURUF KAPITAL; pakai Huruf Awal Kapital."))
    kata = re.findall(r"[a-z0-9]+", judul.lower())
    abaikan = {"dan", "untuk", "di", "ke", "dengan", "yang", "isi", "pcs", "x", "cm", "ml", "gr", "kg"}
    ulang = sorted({k for k in kata if k not in abaikan and len(k) > 2 and kata.count(k) > 2})
    if ulang:
        temuan.append(("CEK", "Kata diulang >2 kali di judul (terlihat seperti spam kata kunci): {}.".format(
            ", ".join(ulang))))
    simbol = sorted(set(POLA_SIMBOL.findall(judul)))
    if simbol:
        temuan.append(("SARAN", "Simbol/emoji di judul: {} — sebagian platform menolak atau memotongnya.".format(
            " ".join(simbol))))

    if kata_kunci:
        jl, gl = judul.lower(), gabungan.lower()
        status = []
        for i, kk in enumerate(kata_kunci):
            pos = jl.find(kk.lower())
            status.append({
                "kata_kunci": kk,
                "di_judul": pos >= 0,
                "semua_kata_di_judul": all(w in jl.split() or w in jl for w in kk.lower().split()),
                "posisi_di_judul": pos if pos >= 0 else None,
                "di_deskripsi": (deskripsi or "").lower().find(kk.lower()) >= 0,
                "total_muncul": gl.count(kk.lower()),
            })
            if i == 0 and (pos < 0 or pos >= AREA_TERLIHAT) and not (
                    pos < 0 and all(jl.find(w) != -1 and jl.find(w) < AREA_TERLIHAT for w in kk.lower().split())):
                temuan.append(("SARAN", "Kata kunci utama '{}' belum ada di {} karakter pertama judul.".format(
                    kk, AREA_TERLIHAT)))
            if gl.count(kk.lower()) > 6:
                temuan.append(("CEK", "Kata kunci '{}' muncul {} kali — kurangi agar tidak dianggap spam.".format(
                    kk, gl.count(kk.lower()))))
        info["kata_kunci"] = status

    gagal = sum(1 for t in temuan if t[0] == "GAGAL")
    return {
        "platform": NAMA_PLATFORM[platform],
        "lulus": gagal == 0,
        "info": info,
        "temuan": [{"tingkat": t, "pesan": p} for t, p in temuan],
        "catatan": "Batas yang dipakai adalah batas AMAN skill, bukan batas resmi. Cek batas terbaru di Seller Center.",
    }


def cetak_teks(hasil_list):
    for h in hasil_list:
        i = h["info"]
        print("=== {} === {}".format(h["platform"], "LULUS" if h["lulus"] else "PERLU DIPERBAIKI"))
        print("Judul     : {}/{} karakter".format(i["panjang_judul"], i["batas_judul"]))
        if "panjang_deskripsi" in i:
            print("Deskripsi : {}/{} karakter".format(i["panjang_deskripsi"], i["batas_deskripsi"]))
        for k in i.get("kata_kunci", []):
            print("  - kata kunci '{}': judul={} deskripsi={} muncul={}x".format(
                k["kata_kunci"], "ya" if k["di_judul"] else ("semua kata ada (tidak berurutan)"
                                                             if k["semua_kata_di_judul"] else "tidak"),
                "ya" if k["di_deskripsi"] else "tidak", k["total_muncul"]))
        if not h["temuan"]:
            print("Tidak ada temuan.")
        for t in h["temuan"]:
            print("[{}] {}".format(t["tingkat"], t["pesan"]))
        print(h["catatan"])
        print()


def main():
    p = argparse.ArgumentParser(description="Cek draf listing marketplace (Shopee, Tokopedia, TikTok Shop).")
    p.add_argument("--platform", required=True,
                   help="shopee, tokopedia, tiktok, atau beberapa dipisah koma (mis. shopee,tokopedia)")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--judul", help="teks judul produk")
    g.add_argument("--judul-file", help="file .txt berisi judul")
    p.add_argument("--deskripsi", help="teks deskripsi (untuk teks pendek)")
    p.add_argument("--deskripsi-file", help="file .txt berisi deskripsi")
    p.add_argument("--kata-kunci", help="daftar kata kunci dipisah koma; yang pertama = kata kunci utama")
    p.add_argument("--batas-judul", type=int, help="ganti batas maksimal judul (mis. batas terbaru dari Seller Center)")
    p.add_argument("--batas-deskripsi", type=int, help="ganti batas maksimal deskripsi")
    p.add_argument("--json", action="store_true", help="keluarkan hasil dalam JSON")
    a = p.parse_args()

    platforms = []
    for x in a.platform.lower().replace(" ", "").split(","):
        if not x:
            continue
        x = ALIAS.get(x, x)
        if x == "semua":
            platforms += list(BATAS)
        elif x in BATAS:
            platforms.append(x)
        else:
            galat("Platform '{}' tidak dikenal. Pilih: shopee, tokopedia, tiktok, atau semua.".format(x))
    if not platforms:
        galat("Isi --platform, mis. --platform shopee")
    for nama, nilai in (("--batas-judul", a.batas_judul), ("--batas-deskripsi", a.batas_deskripsi)):
        if nilai is not None and nilai <= 0:
            galat("{} harus angka lebih dari 0.".format(nama))

    judul = (a.judul if a.judul is not None else baca_file(a.judul_file)).strip()
    if a.deskripsi is not None and a.deskripsi_file:
        galat("Pilih salah satu: --deskripsi atau --deskripsi-file.")
    deskripsi = a.deskripsi if a.deskripsi is not None else (baca_file(a.deskripsi_file) if a.deskripsi_file else None)
    if deskripsi is not None:
        deskripsi = deskripsi.strip()
    kk = [k.strip() for k in (a.kata_kunci or "").split(",") if k.strip()]

    hasil = []
    for pf in dict.fromkeys(platforms):
        b = dict(BATAS[pf])
        if a.batas_judul:
            b["judul_maks"] = a.batas_judul
        if a.batas_deskripsi:
            b["deskripsi_maks"] = a.batas_deskripsi
        hasil.append(periksa(pf, judul, deskripsi, kk, b))

    if a.json:
        print(json.dumps(hasil, ensure_ascii=False, indent=2))
    else:
        cetak_teks(hasil)


if __name__ == "__main__":
    main()
