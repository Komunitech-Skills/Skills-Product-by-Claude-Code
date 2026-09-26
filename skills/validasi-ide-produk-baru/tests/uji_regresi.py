#!/usr/bin/env python3
"""Uji regresi untuk parsing angka format uang Indonesia (`parse_uang`) di
scripts/hitung_validasi.py — dibuat setelah bug ditemukan uji independen
(lihat examples/HASIL-UJI.md v1.0.0 §3): "25.000" pernah terbaca 25 (salah
1000x diam-diam) karena titik dianggap desimal, bukan pemisah ribuan.

Jalankan: python3 tests/uji_regresi.py
Tidak butuh pytest — hanya library standar Python 3.8+, exit code 0 jika
semua lolos, 1 jika ada yang gagal.
"""
import importlib.util
import os
import sys
from decimal import Decimal

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT_PATH = os.path.join(SKILL_DIR, "scripts", "hitung_validasi.py")

spec = importlib.util.spec_from_file_location("hitung_validasi", SCRIPT_PATH)
hv = importlib.util.module_from_spec(spec)
spec.loader.exec_module(hv)

gagal = []


def cek_sama(deskripsi, aktual, harap):
    if Decimal(aktual) != Decimal(harap):
        gagal.append(f"{deskripsi}: dapat {aktual!r}, harap {harap!r}")


def cek_ditolak(deskripsi, nilai):
    try:
        hasil = hv.parse_uang(nilai, "harga")
        gagal.append(f"{deskripsi}: seharusnya DITOLAK (ambigu), tapi diterima jadi {hasil!r}")
    except SystemExit:
        pass  # sesuai harapan


# --- Kasus yang WAJIB diterima & dihitung BENAR ---
cek_sama('"25.000" (bug lama: terbaca 25)', hv.parse_uang("25.000", "harga"), "25000")
cek_sama('"Rp25.000"', hv.parse_uang("Rp25.000", "harga"), "25000")
cek_sama('"Rp 25.000" (spasi)', hv.parse_uang("Rp 25.000", "harga"), "25000")
cek_sama('"150.000"', hv.parse_uang("150.000", "harga"), "150000")
cek_sama('"1.234.567" (dua titik ribuan)', hv.parse_uang("1.234.567", "harga"), "1234567")
cek_sama('"25rb"', hv.parse_uang("25rb", "harga"), "25000")
cek_sama('"25ribu"', hv.parse_uang("25ribu", "harga"), "25000")
cek_sama('"1jt"', hv.parse_uang("1jt", "harga"), "1000000")
cek_sama('"1juta"', hv.parse_uang("1juta", "harga"), "1000000")
cek_sama('"1,5jt" (desimal + singkatan)', hv.parse_uang("1,5jt", "harga"), "1500000")
cek_sama('"2,5rb"', hv.parse_uang("2,5rb", "harga"), "2500")
cek_sama('angka polos "25000"', hv.parse_uang("25000", "harga"), "25000")
cek_sama("int dari JSON (25000)", hv.parse_uang(25000, "harga"), "25000")
cek_sama("float dari JSON (25000.0)", hv.parse_uang(25000.0, "harga"), "25000")

# --- Kasus yang WAJIB ditolak (ambigu — jangan ditebak) ---
cek_ditolak('"25.5" (titik desimal vs ribuan salah tulis)', "25.5")
cek_ditolak('"1.234,56" (campur titik & koma)', "1.234,56")
cek_ditolak('"25,000" (koma tanpa singkatan rb/jt)', "25,000")
cek_ditolak('".000" (tidak ada angka di depan)', ".000")
cek_ditolak('"25." (titik tanpa kelompok 3 digit)', "25.")
cek_ditolak('"25.00" (kelompok 2 digit, bukan 3)', "25.00")
cek_ditolak('"" (kosong)', "")
cek_ditolak('"abc" (bukan angka)', "abc")
cek_ditolak('"rb" (singkatan tanpa angka)', "rb")

if gagal:
    print(f"GAGAL: {len(gagal)} kasus tidak sesuai harapan\n")
    for g in gagal:
        print(f"  - {g}")
    sys.exit(1)

print(f"OK: semua kasus regresi parsing uang Indonesia lolos ({14} diterima + {9} ditolak = 23 kasus).")
sys.exit(0)
