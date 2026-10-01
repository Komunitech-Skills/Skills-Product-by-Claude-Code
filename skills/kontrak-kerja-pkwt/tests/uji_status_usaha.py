#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Uji scripts/status_usaha.py (hanya library standar). Jalankan: python3 tests/uji_status_usaha.py
Angka harapan dihitung manual dari PP 7/2021 Pasal 35 dan PP 36/2021 Pasal 36."""
import os
import subprocess
import sys

SINI = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(SINI)
SCRIPTS = os.path.join(SKILL, "scripts")
sys.dont_write_bytecode = True
sys.path.insert(0, SCRIPTS)
import status_usaha as su  # noqa: E402
from hitung_pkwt import InputError  # noqa: E402

GAGAL, N = [], [0]


def cek(nama, kondisi, info=""):
    N[0] += 1
    if not kondisi:
        GAGAL.append("{} {}".format(nama, info))


def harus_error(nama, f, potongan):
    N[0] += 1
    try:
        f()
    except InputError as e:
        if potongan.lower() not in str(e).lower():
            GAGAL.append("{}: pesan tanpa '{}': {}".format(nama, potongan, e))
        return
    GAGAL.append(nama + ": seharusnya error")


# --- batas omzet (ayat 5): mikro <= 2 M; kecil > 2 M s.d. 15 M; menengah > 15 M s.d. 50 M
for omzet, harap in (("2 miliar", "mikro"), ("2.000.000.001", "kecil"), ("3,5 miliar", "kecil"),
                     ("15 miliar", "kecil"), ("15.000.000.001", "menengah"), ("50M", "menengah"),
                     ("51 miliar", "besar"), ("800jt", "mikro")):
    h = su.hitung(omzet=omzet)
    cek("omzet " + omzet, h["kelas_omzet"] == harap, h["kelas_omzet"])
# Regresi uji OpenClaw 2026-10-01: omzet > Rp2 miliar BUKAN otomatis "bukan UMK"
h = su.hitung(omzet="3 miliar")
cek("omzet 3 M tetap usaha kecil → umk", h["umk"] is True and "usaha mikro/kecil" in h["status"], h["status"])
h = su.hitung(omzet="20 miliar")
cek("omzet 20 M bukan umk", h["umk"] is False and "bukan usaha mikro/kecil" in h["status"])

# --- batas modal (ayat 3)
for modal, harap in (("1 miliar", "mikro"), ("1,2 miliar", "kecil"), ("5 miliar", "kecil"),
                     ("6 miliar", "menengah"), ("10 miliar", "menengah"), ("11 miliar", "besar")):
    cek("modal " + modal, su.hitung(modal=modal)["kelas_modal"] == harap)

# --- kriteria berbeda → tidak memutuskan
h = su.hitung(omzet="1 miliar", modal="7 miliar")
cek("beda kriteria tidak pasti", h["umk"] is None and "TIDAK PASTI" in h["status"])
cek("beda kriteria rujuk NIB", any("NIB/OSS" in p for p in h["peringatan"]))
# --- tanpa data → tidak menyimpulkan
h = su.hitung()
cek("tanpa data", h["umk"] is None and h["status"] == "belum bisa dihitung")
cek("selalu minta konfirmasi NIB/OSS", "NIB/OSS" in su.teks(su.hitung(omzet="1 miliar")))

# --- batas upah UMK: maks(50% konsumsi, 125% GK), dibulatkan ke atas
h = su.hitung(omzet="800jt", upah="3jt", konsumsi="1.650.000", garis_kemiskinan="560.000", provinsi="Jawa Barat")
bu = h["batas_upah_umk"]
cek("50% konsumsi", bu["batas_50_konsumsi"] == 825000, bu)
cek("125% GK", bu["batas_125_garis_kemiskinan"] == 700000, bu)
cek("batas = maks", bu["batas"] == 825000 and bu["memenuhi"] is True, bu)
h = su.hitung(upah="600rb", konsumsi="1.000.001", garis_kemiskinan="600.001", provinsi="Jawa Tengah")
bu = h["batas_upah_umk"]
cek("pembulatan ke atas 50%", bu["batas_50_konsumsi"] == 500001, bu)
cek("pembulatan ke atas 125%", bu["batas_125_garis_kemiskinan"] == 750002, bu)  # 750001,25 → 750002
cek("upah di bawah batas", bu["memenuhi"] is False and any("di bawah" in p for p in h["peringatan"]))
h = su.hitung(konsumsi="1jt")
cek("satu angka = batas sementara", h["batas_upah_umk"]["batas"] is None
    and h["batas_upah_umk"]["batas_sementara"] == 500000)

# --- wilayah wajib provinsi, bukan kota
harus_error("kota ditolak", lambda: su.hitung(konsumsi="1jt", provinsi="Kota Bekasi"), "PROVINSI")
harus_error("kabupaten ditolak", lambda: su.hitung(provinsi="Kabupaten Bogor"), "PROVINSI")
cek("teks tingkat provinsi", "tingkat PROVINSI" in su.teks(su.hitung()))
harus_error("omzet negatif", lambda: su.hitung(omzet="-5 miliar"), "negatif")
harus_error("omzet bukan angka", lambda: su.hitung(omzet="banyak"), "bukan angka")

# --- dokumen skill tidak lagi memuat ambang keliru
for nama in ("SKILL.md", os.path.join("templates", "kerangka-pkwt.md"), os.path.join("references", "checklist-periksa.md")):
    isi = open(os.path.join(SKILL, nama), encoding="utf-8").read()
    cek(nama + " tanpa 'omzet di atas Rp2 miliar'", "di atas Rp2 miliar" not in isi and "> Rp2 miliar/tahun" not in isi)
tpl = open(os.path.join(SKILL, "templates", "kerangka-pkwt.md"), encoding="utf-8").read()
cek("template upah UMK tingkat provinsi", "tingkat provinsi" in tpl)
sk = open(os.path.join(SKILL, "SKILL.md"), encoding="utf-8").read()
cek("SKILL.md memakai status_usaha.py", "status_usaha.py" in sk)

# --- CLI
p = subprocess.run([sys.executable, os.path.join(SCRIPTS, "status_usaha.py"), "--omzet", "3,5 miliar"],
                   capture_output=True, text=True, encoding="utf-8")
cek("cli ok", p.returncode == 0 and "kecil" in p.stdout and "NIB/OSS" in p.stdout, p.stdout + p.stderr)
p = subprocess.run([sys.executable, os.path.join(SCRIPTS, "status_usaha.py"), "--provinsi", "Kota Bekasi"],
                   capture_output=True, text=True, encoding="utf-8")
cek("cli kota ramah", p.returncode == 2 and "Traceback" not in p.stderr, p.stderr)

if GAGAL:
    print("GAGAL {} dari {} cek:".format(len(GAGAL), N[0]))
    for g in GAGAL:
        print(" - " + g)
    sys.exit(1)
print("LULUS semua {} cek.".format(N[0]))
