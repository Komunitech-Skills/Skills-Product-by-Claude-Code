#!/usr/bin/env python3
"""Skor & urutkan segmen pelanggan dengan matriks berbobot (Python standar saja).

Pakai:
  python3 scripts/skor_segmen.py segmen.csv
  python3 scripts/skor_segmen.py segmen.csv --bobot "daya_beli=30,persaingan=5"
  python3 scripts/skor_segmen.py segmen.csv --format json
  python3 scripts/skor_segmen.py --hitung "teks bio yang mau dicek"
(Windows: ganti python3 dengan python atau py.)

CSV: kolom `segmen` + kolom kriteria, nilai 1-5 (5 = paling menguntungkan bagi usaha).
Kriteria baku dan bobot awal (jumlah 100):
  ukuran 15, daya_beli 20, kebutuhan 20, jangkauan_kanal 15, kecocokan_produk 15, persaingan 10, kemampuan_layani 5
Catatan arah: persaingan 5 = sedikit pesaing / mudah menonjol; jangkauan_kanal 5 = mudah dijangkau.
Skor = jumlah(bobot x nilai) / jumlah(bobot) x 20  -> skala 0-100.
Bobot memakai TITIK untuk desimal (ukuran=1.5) karena koma memisahkan antar-bobot.
Nama segmen yang berisi koma wajib diberi tanda kutip: "Ibu muda, pengajian",3,3,...
Dua segmen teratas yang selisihnya <= 5 poin dianggap SETARA (lihat SKILL.md Langkah 3).
Keluar kode 0 bila sukses, 2 bila input salah (pesan jelas di stderr).
"""
import argparse
import csv
import json
import math
import sys

KRITERIA = ["ukuran", "daya_beli", "kebutuhan", "jangkauan_kanal", "kecocokan_produk",
            "persaingan", "kemampuan_layani"]
BOBOT_AWAL = {"ukuran": 15, "daya_beli": 20, "kebutuhan": 20, "jangkauan_kanal": 15,
              "kecocokan_produk": 15, "persaingan": 10, "kemampuan_layani": 5}
BATAS_SERI = 5.0  # selisih skor <= ini dianggap setara


class InputSalah(Exception):
    pass


def baca_bobot(teks):
    bobot = dict(BOBOT_AWAL)
    if not teks:
        return bobot
    for bagian in teks.split(","):
        if not bagian.strip():
            continue
        if "=" not in bagian:
            raise InputSalah(f"Bobot '{bagian.strip()}' salah format; pakai nama=angka dipisah koma, "
                             "mis. daya_beli=30,persaingan=5. Desimal pakai titik: ukuran=1.5")
        k, v = (x.strip() for x in bagian.split("=", 1))
        if k not in KRITERIA:
            raise InputSalah(f"Kriteria '{k}' tidak dikenal. Pilihan: {', '.join(KRITERIA)}")
        try:
            angka = float(v)
        except ValueError:
            raise InputSalah(f"Bobot '{k}' bukan angka: '{v}' (desimal pakai titik, mis. {k}=1.5)")
        if not math.isfinite(angka):
            raise InputSalah(f"Bobot '{k}' harus angka biasa, bukan '{v}'")
        if angka < 0:
            raise InputSalah(f"Bobot '{k}' tidak boleh negatif")
        bobot[k] = angka
    if sum(bobot.values()) <= 0:
        raise InputSalah("Jumlah bobot harus lebih dari 0")
    return bobot


def baca_csv(path):
    try:
        with open(path, newline="", encoding="utf-8-sig") as f:
            teks = f.read()
    except FileNotFoundError:
        raise InputSalah(f"File tidak ditemukan: {path}")
    except UnicodeDecodeError:
        raise InputSalah("File harus berkode UTF-8 (simpan ulang sebagai CSV UTF-8)")
    if not teks.strip():
        raise InputSalah("File kosong")
    judul = teks.splitlines()[0]
    hitung_pemisah = {p: judul.count(p) for p in (",", ";", "\t")}
    pemisah = max(hitung_pemisah, key=lambda p: (hitung_pemisah[p], p == ","))
    baca = csv.DictReader(teks.splitlines(), delimiter=pemisah)
    kolom = [(c or "").strip().lower() for c in (baca.fieldnames or [])]
    if "segmen" not in kolom:
        raise InputSalah("Kolom 'segmen' tidak ada di baris judul (pemisah kolom yang dikenali: koma, titik koma, tab)")
    ganda = sorted({k for k in kolom if k and kolom.count(k) > 1})
    if ganda:
        raise InputSalah("Judul kolom ganda: " + ", ".join(ganda) + ". Setiap kolom hanya boleh muncul sekali; "
                         "hapus atau ganti nama salah satunya")
    hilang = [k for k in KRITERIA if k not in kolom]
    if hilang:
        raise InputSalah("Kolom kriteria kurang: " + ", ".join(hilang))
    baris = []
    for no, r in enumerate(baca, start=2):
        if None in r:  # kolom berlebih: DictReader menaruh sisanya di kunci None
            raise InputSalah(f"Baris {no}: jumlah kolom lebih banyak dari judul. Nama segmen yang berisi koma "
                             "harus diberi tanda kutip \"...\" atau ganti komanya dengan '/'")
        r = {(k or "").strip().lower(): (v or "").strip() for k, v in r.items()}
        if not any(r.values()):
            continue
        baris.append((no, r))
    if not baris:
        raise InputSalah("Tidak ada baris segmen")
    return baris


def hitung(baris, bobot):
    total_bobot = sum(bobot.values())
    hasil, dilihat = [], set()
    for no, r in baris:
        nama = r["segmen"]
        if not nama:
            raise InputSalah(f"Baris {no}: nama segmen kosong")
        if nama.lower() in dilihat:
            raise InputSalah(f"Baris {no}: nama segmen '{nama}' ganda")
        dilihat.add(nama.lower())
        nilai = {}
        for k in KRITERIA:
            mentah = (r[k] or "").replace(",", ".")
            try:
                n = float(mentah)
            except ValueError:
                raise InputSalah(f"Baris {no} ({nama}): '{k}' harus angka 1-5, ditemukan '{r[k]}'")
            if not 1 <= n <= 5:
                raise InputSalah(f"Baris {no} ({nama}): '{k}' harus 1-5, ditemukan {r[k]}")
            nilai[k] = n
        skor = sum(bobot[k] * nilai[k] for k in KRITERIA) / total_bobot * 20
        hasil.append({"segmen": nama, "skor": round(skor + 1e-9, 1), "nilai": nilai})
    hasil.sort(key=lambda h: (-h["skor"], -h["nilai"]["daya_beli"], h["segmen"].lower()))
    for i, h in enumerate(hasil, start=1):
        h["peringkat"] = i
        if h["skor"] >= 75:
            h["saran"] = "Utama (layani duluan)"
        elif h["skor"] >= 60:
            h["saran"] = "Kandidat (uji kecil dulu)"
        else:
            h["saran"] = "Tunda"
        lemah = [k for k in KRITERIA if h["nilai"][k] <= 2]
        h["titik_lemah"] = lemah
    return hasil


def cek_seri(hasil):
    """Kembali pesan bila dua segmen teratas selisih <= BATAS_SERI poin, selain itu None."""
    if len(hasil) < 2:
        return None
    a, b = hasil[0], hasil[1]
    selisih = round(a["skor"] - b["skor"], 1)
    if selisih > BATAS_SERI:
        return None
    return (f"SETARA: '{a['segmen']}' dan '{b['segmen']}' hanya selisih {selisih:g} poin (<= {BATAS_SERI:g}). "
            "Skor tidak cukup untuk memilih; pilih dengan alasan yang ditulis: segmen yang sudah terbukti "
            "membeli (FAKTA), lalu yang paling murah & cepat diuji, lalu yang paling mudah dilayani.")


def hitung_karakter(teks):
    """Hitung panjang teks seperti aplikasi menghitung. Kembali dict."""
    huruf = len(teks)                                   # karakter (code point)
    utf16 = len(teks.encode("utf-16-le")) // 2          # cara hitung banyak aplikasi (emoji umum = 2)
    emoji = sum(1 for c in teks if ord(c) >= 0x1F000 or 0x2600 <= ord(c) <= 0x27BF)
    return {"karakter": huruf, "karakter_utf16": utf16, "emoji": emoji}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Skor segmen pelanggan berbobot")
    ap.add_argument("csv", nargs="?", help="file CSV segmen (tidak perlu bila memakai --hitung)")
    ap.add_argument("--hitung", metavar="TEKS", help="hitung jumlah karakter teks (bio/tagline), lalu keluar")
    ap.add_argument("--bobot", default="", help='ubah bobot, mis. "daya_beli=30,persaingan=5"')
    ap.add_argument("--format", choices=["tabel", "json"], default="tabel")
    a = ap.parse_args(argv)
    if a.hitung is not None:
        h = hitung_karakter(a.hitung)
        maks = max(h["karakter"], h["karakter_utf16"])
        print(f"Jumlah karakter: {h['karakter']} (spasi & tanda baca ikut dihitung)")
        if h["emoji"] or h["karakter_utf16"] != h["karakter"]:
            print(f"Berisi {h['emoji']} emoji/simbol. Sebagian aplikasi menghitung emoji sebagai 2 karakter atau lebih: "
                  f"anggap panjangnya {maks}.")
        print(f"Bio Instagram/TikTok maks. 150: {'MUAT' if maks <= 150 else 'KEPANJANGAN'}"
              f" (sisa {150 - maks}). Sisakan ruang +-5 karakter bila ada emoji.")
        return 0
    if not a.csv:
        print("GAGAL: sebutkan file CSV segmen, atau pakai --hitung \"teks\"", file=sys.stderr)
        return 2
    try:
        bobot = baca_bobot(a.bobot)
        hasil = hitung(baca_csv(a.csv), bobot)
    except InputSalah as e:
        print(f"GAGAL: {e}", file=sys.stderr)
        return 2
    if a.format == "json":
        print(json.dumps({"bobot": bobot, "hasil": hasil, "seri": cek_seri(hasil)}, ensure_ascii=False, indent=2))
        return 0
    print("Bobot: " + ", ".join(f"{k} {bobot[k]:g}" for k in KRITERIA))
    lebar = max(34, max(len(h["segmen"]) for h in hasil) + 1)  # nama segmen tidak pernah dipotong
    print(f"{'#':<3}{'Segmen':<{lebar}}{'Skor':>6}  Saran")
    for h in hasil:
        lemah = f"  [lemah: {', '.join(h['titik_lemah'])}]" if h["titik_lemah"] else ""
        print(f"{h['peringkat']:<3}{h['segmen']:<{lebar}}{h['skor']:>6.1f}  {h['saran']}{lemah}")
    seri = cek_seri(hasil)
    if seri:
        print(seri)
    print("Skor 0-100 dari penilaian 1-5 (penilaian = perkiraan, bukan data pasar). Pilih 1 segmen utama, maks. 2.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
