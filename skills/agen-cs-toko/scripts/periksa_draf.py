#!/usr/bin/env python3
"""
periksa_draf.py — Memeriksa draf balasan CS sebelum dikirim admin.

Memeriksa dua hal, hanya dengan Python standar (tanpa dependensi luar):
1. Nominal Rupiah yang disebut di draf tapi TIDAK ditemukan di basis
   pengetahuan (cs/PENGETAHUAN.md) -> potensi mengarang harga/stok.
2. Pola data sensitif di draf (mirip NIK/KTP 16 digit, nomor kartu,
   kata OTP/PIN/password) -> jangan sampai bocor balik ke pelanggan.

Pemakaian:
    python3 periksa_draf.py --pengetahuan cs/PENGETAHUAN.md --draf draf.txt
    python3 periksa_draf.py --pengetahuan cs/PENGETAHUAN.md --draf -   (baca draf dari stdin)

Keluaran: ringkasan teks + JSON di baris terakhir (mudah dibaca skrip lain).
Exit code: 0 = bersih, 1 = ada temuan yang perlu dicek manusia, 2 = error input.
"""

import argparse
import json
import re
import sys


def baca_teks(path):
    if path == "-":
        return sys.stdin.read()
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: file tidak ditemukan: {path}", file=sys.stderr)
        sys.exit(2)
    except OSError as e:
        print(f"Error membaca {path}: {e}", file=sys.stderr)
        sys.exit(2)


# Menangkap "Rp 22.000", "Rp22000", "22.000 rupiah", "Rp 22.000,-" dll.
POLA_RUPIAH = re.compile(
    r"(?:Rp\.?\s*)?(\d{1,3}(?:[.,]\d{3})+|\d{4,})(?:\s*(?:rupiah|,-|/-))?",
    re.IGNORECASE,
)
POLA_RP_AWALAN = re.compile(r"Rp\.?\s*\d", re.IGNORECASE)


def ekstrak_nominal(teks):
    """Ambil semua nominal Rupiah yang disebut eksplisit (didahului 'Rp' atau
    diikuti kata 'rupiah'), dinormalisasi jadi integer. Angka biasa (tanggal,
    nomor pesanan, dsb.) TIDAK ikut supaya tidak banyak salah tangkap."""
    hasil = set()
    for m in re.finditer(
        r"Rp\.?\s*(\d[\d.,]*)|(\d[\d.,]*)\s*(?:ribu|rb|rupiah)\b",
        teks,
        re.IGNORECASE,
    ):
        mentah = m.group(1) or m.group(2)
        if not mentah:
            continue
        angka = normalisasi_angka(mentah)
        if angka is not None and angka > 0:
            hasil.add(angka)
    return hasil


def normalisasi_angka(mentah):
    """Ubah '22.000' / '22,000' / '22000' / '22.000,50' jadi integer rupiah.
    Aturan: titik/koma sebagai ribuan bila diikuti persis 3 digit berulang,
    dua digit terakhir dianggap desimal (dibuang, dibulatkan ke bawah)."""
    s = mentah.strip().rstrip(".,")
    if not s:
        return None
    # Buang pemisah ribuan (titik atau koma yang diikuti 3 digit lalu batas)
    bersih = re.sub(r"[.,](?=\d{3}(\D|$))", "", s)
    # Sisa koma/titik (desimal) -> ambil bagian bulat saja
    bersih = re.split(r"[.,]", bersih)[0]
    if not bersih.isdigit():
        return None
    try:
        return int(bersih)
    except ValueError:
        return None


POLA_SENSITIF = [
    ("NIK/nomor identitas 16 digit", re.compile(r"\b\d{16}\b")),
    ("Nomor kartu (mirip kartu debit/kredit)", re.compile(r"\b(?:\d[ -]?){13,19}\b")),
    ("Kata kunci OTP", re.compile(r"\bOTP\b", re.IGNORECASE)),
    ("Kata kunci PIN", re.compile(r"\bPIN\b", re.IGNORECASE)),
    ("Kata kunci password/kata sandi", re.compile(r"\b(password|kata sandi)\b", re.IGNORECASE)),
    ("CVV/CVC kartu", re.compile(r"\bcvv\b|\bcvc\b", re.IGNORECASE)),
]


def cek_data_sensitif(teks):
    temuan = []
    for label, pola in POLA_SENSITIF:
        for m in pola.finditer(teks):
            cuplikan = teks[max(0, m.start() - 15): m.end() + 15].strip()
            temuan.append({"jenis": label, "cuplikan": cuplikan})
    return temuan


def main():
    ap = argparse.ArgumentParser(description="Periksa draf balasan CS sebelum dikirim.")
    ap.add_argument("--pengetahuan", required=True, help="Path ke cs/PENGETAHUAN.md")
    ap.add_argument("--draf", required=True, help="Path ke file draf balasan, atau - untuk stdin")
    args = ap.parse_args()

    teks_pengetahuan = baca_teks(args.pengetahuan)
    teks_draf = baca_teks(args.draf)

    nominal_pengetahuan = ekstrak_nominal(teks_pengetahuan)
    nominal_draf = ekstrak_nominal(teks_draf)
    nominal_tidak_ditemukan = sorted(nominal_draf - nominal_pengetahuan)

    temuan_sensitif = cek_data_sensitif(teks_draf)

    bersih = not nominal_tidak_ditemukan and not temuan_sensitif

    print("=== Hasil periksa draf ===")
    if nominal_tidak_ditemukan:
        print(f"[PERIKSA] {len(nominal_tidak_ditemukan)} nominal di draf TIDAK ditemukan di basis pengetahuan:")
        for n in nominal_tidak_ditemukan:
            print(f"  - Rp {n:,}".replace(",", "."))
        print("  -> Cek manual: mungkin salah ketik, atau memang belum ada di PENGETAHUAN.md (jangan kirim sebelum dicek).")
    else:
        print("[OK] Semua nominal Rupiah di draf ditemukan di basis pengetahuan (atau draf tidak menyebut nominal).")

    if temuan_sensitif:
        print(f"[PERIKSA] {len(temuan_sensitif)} kemungkinan data sensitif di draf:")
        for t in temuan_sensitif:
            print(f"  - {t['jenis']}: ...{t['cuplikan']}...")
        print("  -> Jangan kirim data ini ke pelanggan lewat chat biasa; arahkan ke kanal resmi/eskalasi.")
    else:
        print("[OK] Tidak ada pola data sensitif (NIK/kartu/OTP/PIN/password) terdeteksi di draf.")

    hasil_json = {
        "bersih": bersih,
        "nominal_tidak_ditemukan_di_pengetahuan": nominal_tidak_ditemukan,
        "data_sensitif_terdeteksi": temuan_sensitif,
    }
    print(json.dumps(hasil_json, ensure_ascii=False))

    sys.exit(0 if bersih else 1)


if __name__ == "__main__":
    main()
