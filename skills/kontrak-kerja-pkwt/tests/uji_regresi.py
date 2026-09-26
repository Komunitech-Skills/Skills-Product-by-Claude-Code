#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Uji regresi scripts/hitung_pkwt.py (hanya library standar).

Jalankan dari mana saja:  python3 tests/uji_regresi.py   (Windows: python atau py)
Keluar 0 bila semua lulus. Angka harapan dihitung manual (lihat komentar tiap kasus).
"""
import json
import os
import subprocess
import sys

SINI = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(os.path.dirname(SINI), "scripts")
SCRIPT = os.path.join(SCRIPTS, "hitung_pkwt.py")
sys.dont_write_bytecode = True
sys.path.insert(0, SCRIPTS)
import hitung_pkwt as hp  # noqa: E402

GAGAL = []
JUMLAH = [0]


def cek(nama, kondisi, info=""):
    JUMLAH[0] += 1
    if not kondisi:
        GAGAL.append("{} {}".format(nama, info))


def harus_error(nama, fungsi, potongan_pesan=""):
    JUMLAH[0] += 1
    try:
        fungsi()
    except hp.InputError as e:
        if potongan_pesan and potongan_pesan.lower() not in str(e).lower():
            GAGAL.append("{}: pesan error tidak memuat '{}': {}".format(nama, potongan_pesan, e))
        return
    GAGAL.append("{}: seharusnya error".format(nama))


def cli(args, kode=0):
    p = subprocess.run([sys.executable, SCRIPT] + args, capture_output=True, text=True, encoding="utf-8")
    JUMLAH[0] += 1
    if p.returncode != kode:
        GAGAL.append("CLI {} -> kode {} (harap {}): {}".format(args, p.returncode, kode, p.stderr.strip()))
    return p


# ------------------------------------------------------------ parsing tanggal
T = hp.parse_tanggal
cek("tgl iso", T("2026-01-01").isoformat() == "2026-01-01")
cek("tgl dd/mm/yyyy", T("01/02/2026").isoformat() == "2026-02-01")
cek("tgl d-m-yyyy", T("1-2-2026").isoformat() == "2026-02-01")
cek("tgl indo panjang", T("1 Januari 2026").isoformat() == "2026-01-01")
cek("tgl indo singkat", T("17 Agt 2026").isoformat() == "2026-08-17")
cek("tgl pebruari", T("3 Pebruari 2026").isoformat() == "2026-02-03")
cek("tgl nopember", T("30 Nopember 2026").isoformat() == "2026-11-30")
cek("tgl dengan hari", T("Senin, 5 Oktober 2026").isoformat() == "2026-10-05")
cek("tgl huruf besar", T("1 JANUARI 2026").isoformat() == "2026-01-01")
cek("tgl inggris", T("1 March 2026").isoformat() == "2026-03-01")
harus_error("tgl 31 Feb", lambda: T("31/02/2026"), "tidak ada di kalender")
harus_error("tgl 29 Feb non-kabisat", lambda: T("29 Februari 2026"), "kalender")
cek("tgl 29 Feb kabisat", T("29 Februari 2028").isoformat() == "2028-02-29")
harus_error("tgl bulan ngawur", lambda: T("1 Janubari 2026"), "bulan")
harus_error("tgl kosong", lambda: T(""), "kosong")
harus_error("tgl teks", lambda: T("besok"), "tidak dikenali")

# ------------------------------------------------------------ parsing rupiah
R = hp.parse_rupiah
cek("rp titik", R("Rp5.000.000") == 5000000)
cek("rp spasi", R("Rp 5.000.000") == 5000000)
cek("rp koma desimal", R("5.000.000,00") == 5000000)
cek("rp polos", R("5000000") == 5000000)
cek("rp jt", R("5jt") == 5000000)
cek("rp koma jt", R("5,5jt") == 5500000)
cek("rp titik jt", R("5.5 juta") == 5500000)
cek("rp rb", R("500rb") == 500000)
cek("rp ribu", R("750 ribu") == 750000)
cek("rp k", R("250k") == 250000)
cek("rp gaya inggris", R("5,000,000") == 5000000)
cek("rp IDR", R("IDR 4.250.000") == 4250000)
cek("rp kosong -> None", R("") is None and R(None) is None)
harus_error("rp negatif", lambda: R("-5jt"), "negatif")
harus_error("rp negatif rp", lambda: R("Rp-100.000"), "negatif")
harus_error("rp teks", lambda: R("lima juta"), "bukan angka")
harus_error("rp ambigu", lambda: R("5.5.5jt"), "membingungkan")

# ------------------------------------------------------------ masa (bulan penuh + sisa hari, inklusif)
D = hp.parse_tanggal
cek("masa 1 Jan-31 Des", hp.masa(D("1/1/2026"), D("31/12/2026"))[:2] == (12, 0))
cek("masa 1-31 Jan", hp.masa(D("1/1/2026"), D("31/1/2026"))[:2] == (1, 0))
cek("masa 1-30 Jan", hp.masa(D("1/1/2026"), D("30/1/2026"))[:2] == (0, 30))
cek("masa 15 Mar-14 Sep", hp.masa(D("15/3/2026"), D("14/9/2026"))[:2] == (6, 0))
# 1 Jan - 15 Mar 2026: 2 bulan penuh (s.d. 28 Feb), sisa 15 hari dari bulan berjalan 1-31 Mar (31 hari)
cek("masa sisa hari", hp.masa(D("1/1/2026"), D("15/3/2026")) == (2, 15, 31))
# 31 Jan - 27 Feb 2026: 31 Jan + 1 bulan = 28 Feb (dipotong) -> 1 bulan penuh
cek("masa akhir bulan", hp.masa(D("31/1/2026"), D("27/2/2026"))[:2] == (1, 0))
cek("masa 1 hari", hp.masa(D("5/5/2026"), D("5/5/2026"))[:2] == (0, 1))

# ------------------------------------------------------------ kompensasi
H = hp.hitung
h = H(["1 Januari 2026 s.d. 31 Desember 2026"], gaji_pokok="5jt", tunjangan_tetap="500rb")
cek("12 bulan = 1x upah", h["total_kompensasi"] == 5500000, h["total_kompensasi"])
cek("upah = pokok + tunjangan tetap", h["upah_sebulan"] == 5500000)
cek("tidak melebihi 5 th", h["total_pkwt"]["melebihi_5_tahun"] is False)

# 6 bulan: 6/12 x 4.000.000 = 2.000.000
h = H(["1/1/2026 s.d. 30/6/2026"], upah="4jt")
cek("6 bulan", h["total_kompensasi"] == 2000000, h["total_kompensasi"])

# 18 bulan tanpa perpanjangan: 18/12 x 3.000.000 = 4.500.000
h = H(["1/1/2025 s.d. 30/6/2026"], upah="3jt")
cek("18 bulan > 12", h["total_kompensasi"] == 4500000, h["total_kompensasi"])

# 7 bulan: 7/12 x 3.500.000 = 2.041.666,67 -> 2.041.667 (pembulatan terdekat)
h = H(["1/1/2026 s.d. 31/7/2026"], upah="3.500.000")
cek("pembulatan ke atas", h["total_kompensasi"] == 2041667, h["total_kompensasi"])

# 5 bulan: 5/12 x 3.100.000 = 1.291.666,67 -> 1.291.667 ; 1 bulan x 3.100.001/12 = 258.333,4 -> 258.333
h = H(["1/1/2026 s.d. 31/1/2026"], upah="3100001")
cek("pembulatan ke bawah", h["total_kompensasi"] == 258333, h["total_kompensasi"])

# < 1 bulan: tidak berhak
h = H(["1/1/2026 s.d. 30/1/2026"], upah="5jt")
cek("< 1 bulan tidak berhak", h["total_kompensasi"] == 0 and h["rincian_kompensasi"][0]["berhak"] is False)

# Sisa hari metode pecahan: 1 Jan - 15 Mar 2026 = 2 + 15/31 bulan; x 6.200.000 / 12
# = (77/31) x 6.200.000 / 12 = 1.283.333,33 -> 1.283.333
h = H(["1 Januari 2026 s.d. 15 Maret 2026"], upah="6,2jt")
cek("pecahan sisa hari", h["total_kompensasi"] == 1283333, h["total_kompensasi"])
# v1.0.2 (R-baru-3): metode bulan-penuh dihapus (tidak aditif) -> error ramah, bukan angka diam-diam
harus_error("metode bulan-penuh dihapus", lambda: H(["1 Januari 2026 s.d. 15 Maret 2026"], upah="6,2jt",
                                                     metode="bulan-penuh"), "dihapus")

# Perpanjangan: kompensasi per periode
h = H(["1/1/2025 s.d. 31/12/2025", "1/1/2026 s.d. 30/6/2026"], upah="4,8jt")
k = [r["kompensasi"] for r in h["rincian_kompensasi"]]
cek("perpanjangan per periode", k == [4800000, 2400000], k)
cek("perpanjangan total", h["total_kompensasi"] == 7200000)

# Periode diinput tidak urut -> diurutkan + peringatan
h = H(["1/1/2026 s.d. 30/6/2026", "1/1/2025 s.d. 31/12/2025"], upah="4,8jt")
cek("urut ulang", h["rincian_kompensasi"][0]["mulai"] == "2025-01-01"
    and any("diurutkan" in p for p in h["peringatan"]))

# Tumpang tindih -> error
harus_error("tumpang tindih", lambda: H(["1/1/2025 s.d. 31/12/2025", "1/12/2025 s.d. 30/6/2026"], upah="4jt"),
            "tumpang tindih")
# Jeda -> peringatan
h = H(["1/1/2025 s.d. 31/12/2025", "1/2/2026 s.d. 31/7/2026"], upah="4jt")
cek("jeda peringatan", any("jeda 31 hari" in p for p in h["peringatan"]))

# ------------------------------------------------------------ batas 5 tahun
h = H(["1/1/2022 s.d. 31/12/2026"], upah="5jt")  # tepat 60 bulan
cek("tepat 5 tahun OK", h["total_pkwt"]["melebihi_5_tahun"] is False and h["total_kompensasi"] == 25000000)
h = H(["1/1/2022 s.d. 31/12/2026", "1/1/2027 s.d. 31/1/2027"], upah="5jt")
cek("lebih 5 tahun ditandai", h["total_pkwt"]["melebihi_5_tahun"] is True
    and h["total_pkwt"]["batas_akhir_5_tahun"] == "2026-12-31"
    and any("MELEBIHI" in p for p in h["peringatan"]))
h = H(["1/1/2022 s.d. 1/1/2027"], upah="5jt")  # lebih 1 hari
cek("lebih 1 hari ditandai", h["total_pkwt"]["melebihi_5_tahun"] is True)

# ------------------------------------------------------------ pengakhiran dini & ganti rugi Pasal 62
# Kontrak 1 Jan - 31 Des 2026, upah 6jt, berhenti 30 Jun 2026 (diakhiri pengusaha)
# Kompensasi 6/12 x 6jt = 3jt ; sisa 1 Jul - 31 Des = 6 bulan -> ganti rugi 36jt
h = H(["1/1/2026 s.d. 31/12/2026"], upah="6jt", berhenti="30/6/2026", pihak="pengusaha")
cek("dini kompensasi", h["total_kompensasi"] == 3000000, h["total_kompensasi"])
g = h["ganti_rugi_pasal_62"]
cek("dini ganti rugi", g["nilai"] == 36000000 and g["sisa_masa"] == "6 bulan", g)
cek("dini arah pengusaha", "pengusaha membayar ke pekerja" in g["arah"])

h = H(["1/1/2026 s.d. 31/12/2026"], upah="6jt", berhenti="30/6/2026", pihak="pekerja")
cek("dini arah pekerja", "pekerja membayar ke pengusaha" in h["ganti_rugi_pasal_62"]["arah"]
    and h["total_kompensasi"] == 3000000)

# Sisa dengan hari (v1.0.1, temuan S1): periode 1 Jan - 30 Jun 2026 = 6 bulan; dijalani 1 Jan - 15 Mar
# = 2 + 15/31 bulan; sisa = 6 - (2 + 15/31) = 3 + 16/31 = 3,5161 bulan -> 109/31 x 4.800.000 = 16.877.419,35
# -> Rp16.877.419. (v1.0.0 memberi 3,5 bulan = Rp16.800.000 karena sisa dijangkar dari 16 Mar sehingga
# dijalani + sisa = 5,9839 bulan, bukan 6; pekerja kurang dibayar Rp77.419.)
h = H(["1/1/2025 s.d. 31/12/2025", "1/1/2026 s.d. 30/6/2026"], upah="Rp4.800.000", berhenti="15/03/2026",
      pihak="pengusaha")
cek("dini sisa hari", h["ganti_rugi_pasal_62"]["nilai"] == 16877419, h["ganti_rugi_pasal_62"])
cek("dini kompensasi perpanjangan", [r["kompensasi"] for r in h["rincian_kompensasi"]] == [4800000, 993548])

# Tanpa pihak -> peringatan
h = H(["1/1/2026 s.d. 31/12/2026"], upah="6jt", berhenti="30/6/2026")
cek("dini tanpa pihak", any("Pihak yang mengakhiri" in p for p in h["peringatan"]))
# Berhenti = akhir -> normal
h = H(["1/1/2026 s.d. 31/12/2026"], upah="6jt", berhenti="31/12/2026")
cek("berhenti = akhir normal", h["ganti_rugi_pasal_62"] is None and h["total_kompensasi"] == 6000000)
# Berhenti sebelum periode perpanjangan dimulai
h = H(["1/1/2025 s.d. 31/12/2025", "1/1/2026 s.d. 31/12/2026"], upah="4jt", berhenti="30/6/2025",
      pihak="pengusaha")
cek("perpanjangan belum mulai", h["rincian_kompensasi"][1]["kompensasi"] == 0
    and h["ganti_rugi_pasal_62"]["nilai"] == 24000000
    and any("belum dimulai" in p for p in h["peringatan"]))
harus_error("berhenti sebelum mulai", lambda: H(["1/1/2026 s.d. 31/12/2026"], upah="6jt", berhenti="1/12/2025"),
            "lebih awal")
harus_error("berhenti setelah akhir", lambda: H(["1/1/2026 s.d. 31/12/2026"], upah="6jt", berhenti="1/1/2027"),
            "bukan pengakhiran dini")
harus_error("berhenti di jeda", lambda: H(["1/1/2025 s.d. 31/12/2025", "1/2/2026 s.d. 31/7/2026"], upah="4jt",
                                          berhenti="15/1/2026"), "jeda")

# ------------------------------------------------------------ input buruk lain
harus_error("tanggal terbalik", lambda: H(["31/12/2026 s.d. 1/1/2026"], upah="5jt"), "tertukar")
harus_error("periode tanpa pemisah", lambda: H(["1/1/2026 31/12/2026"], upah="5jt"), "s.d.")
harus_error("tanpa upah", lambda: H(["1/1/2026 s.d. 31/12/2026"]), "gaji-pokok")
harus_error("upah nol", lambda: H(["1/1/2026 s.d. 31/12/2026"], upah="0"), "lebih dari")
harus_error("upah negatif", lambda: H(["1/1/2026 s.d. 31/12/2026"], gaji_pokok="-3000000"), "negatif")
harus_error("upah ganda", lambda: H(["1/1/2026 s.d. 31/12/2026"], upah="5jt", gaji_pokok="4jt"), "salah satu")
harus_error("tanpa periode", lambda: H([], upah="5jt"), "periode")
harus_error("pihak salah", lambda: H(["1/1/2026 s.d. 31/12/2026"], upah="5jt", pihak="bos"), "pengusaha")

# Peringatan upah
h = H(["1/1/2026 s.d. 31/12/2026"], gaji_pokok="2jt", tunjangan_tetap="1,5jt")
cek("pokok < 75%", any("75%" in p for p in h["peringatan"]))
h = H(["1/1/2026 s.d. 31/12/2026"], upah="2jt", upah_minimum="Rp3.000.000")
cek("di bawah upah minimum", any("di bawah upah minimum" in p for p in h["peringatan"]))
h = H(["1/1/2026 s.d. 31/12/2026"], upah="2jt", harian=True)
cek("harian lepas peringatan", any("21 hari" in p for p in h["peringatan"]))

# Pemisah periode lain
for pem in (" sampai ", " sampai dengan ", " s/d ", " sd ", " - ", " .. ", " – "):
    try:
        h = H(["1/1/2026" + pem + "31/12/2026"], upah="1,2jt")
        cek("pemisah '{}'".format(pem.strip()), h["total_kompensasi"] == 1200000)
    except hp.InputError as e:
        cek("pemisah '{}'".format(pem.strip()), False, str(e))

# ============================================================ REGRESI TEMUAN UJI v1.0.1
from fractions import Fraction  # noqa: E402
import datetime  # noqa: E402
import random  # noqa: E402

# --- S1: kasus yang dilaporkan penguji. Kontrak 1 Jan - 31 Mar 2026 (3 bulan), upah 3 jt, pekerja berhenti
# 15 Feb. Dijalani = 1 + 15/28; sisa = 3 - (1 + 15/28) = 1 + 13/28 = 41/28 bulan
# -> 41/28 x 3.000.000 = 4.392.857,14 -> Rp4.392.857 (v1.0.0: Rp4.548.387, pekerja bayar Rp155.530 lebih).
h = H(["1/1/2026 s.d. 31/3/2026"], upah="3jt", berhenti="15/2/2026", pihak="pekerja")
cek("S1 kasus penguji 15 Feb", h["ganti_rugi_pasal_62"]["nilai"] == 4392857, h["ganti_rugi_pasal_62"]["nilai"])
cek("S1 kasus penguji pecahan", h["ganti_rugi_pasal_62"]["bulan_pecahan"] == [41, 28])
# Skenario 03 varian: periode 2 1 Jan - 30 Jun 2027, berhenti 15 Mar 2027, upah 5 jt.
# sisa = 6 - (2 + 15/31) = 109/31 -> 17.580.645,16 -> Rp17.580.645 (v1.0.0: Rp17.500.000)
h = H(["1/1/2026 s.d. 31/12/2026", "1/1/2027 s.d. 30/6/2027"], gaji_pokok="4,5jt", tunjangan_tetap="500rb",
      berhenti="15/3/2027", pihak="pengusaha")
cek("S1 skenario 03 varian", h["ganti_rugi_pasal_62"]["nilai"] == 17580645, h["ganti_rugi_pasal_62"]["nilai"])
# Skenario 03 utama TIDAK berubah: 5.000.000 + 1.250.000, ganti rugi 3 bulan x 5 jt = 15.000.000
h = H(["1/1/2026 s.d. 31/12/2026", "1/1/2027 s.d. 30/6/2027"], gaji_pokok="4,5jt", tunjangan_tetap="500rb",
      berhenti="31/3/2027", pihak="pengusaha")
cek("S1 skenario 03 tetap", [r["kompensasi"] for r in h["rincian_kompensasi"]] == [5000000, 1250000]
    and h["ganti_rugi_pasal_62"]["nilai"] == 15000000, h["ganti_rugi_pasal_62"])
# Skenario 01 TIDAK berubah: 12 bulan, 3,9 jt + 250 rb -> Rp4.150.000 per orang
h = H(["1 Oktober 2026 s.d. 30 September 2027"], gaji_pokok="3,9jt", tunjangan_tetap="250rb")
cek("S1 skenario 01 tetap", h["total_kompensasi"] == 4150000, h["total_kompensasi"])


def _bln(a, b):
    return hp.bulan_desimal(*hp.masa(a, b), metode="pecahan")


# --- S1 tes properti: dijalani + sisa = panjang periode berjalan PERSIS (seed tetap, 3.000 kasus)
acak = random.Random(20260925)
salah = []
awal = datetime.date(2024, 1, 1)
for _ in range(3000):
    m = awal + datetime.timedelta(days=acak.randrange(0, 365 * 5))
    a = m + datetime.timedelta(days=acak.randrange(1, 800))
    b = m + datetime.timedelta(days=acak.randrange(0, (a - m).days))  # berhenti < akhir
    upah = acak.choice(["1000001", "3jt", "4.150.000", "7777777"])
    h = H(["{} s.d. {}".format(m.strftime("%d/%m/%Y"), a.strftime("%d/%m/%Y"))], upah=upah,
          berhenti=b.strftime("%d/%m/%Y"), pihak="pengusaha")
    g = h["ganti_rugi_pasal_62"]
    sisa = Fraction(*g["bulan_pecahan"])
    if _bln(m, b) + sisa != _bln(m, a) or sisa <= 0:
        salah.append((m, a, b))
    # nilai rupiah = pembulatan (sisa x upah) persis
    if g["nilai"] != hp.rupiah_bulat(sisa * h["upah_sebulan"]):
        salah.append(("nilai", m, a, b))
cek("S1 properti dijalani + sisa = total (3.000 kasus acak)", not salah, salah[:3])
# Properti juga berlaku di periode perpanjangan (berhenti di periode ke-2)
salah = []
for _ in range(1000):
    m1 = awal + datetime.timedelta(days=acak.randrange(0, 365 * 3))
    a1 = m1 + datetime.timedelta(days=acak.randrange(30, 400))
    m2 = a1 + datetime.timedelta(days=1)
    a2 = m2 + datetime.timedelta(days=acak.randrange(1, 400))
    b = m2 + datetime.timedelta(days=acak.randrange(0, (a2 - m2).days))
    h = H(["{} s.d. {}".format(m1.isoformat(), a1.isoformat()), "{} s.d. {}".format(m2.isoformat(), a2.isoformat())],
          upah="5jt", berhenti=b.isoformat(), pihak="pekerja")
    if _bln(m2, b) + Fraction(*h["ganti_rugi_pasal_62"]["bulan_pecahan"]) != _bln(m2, a2):
        salah.append((m2, a2, b))
cek("S1 properti di periode perpanjangan (1.000 kasus)", not salah, salah[:3])

# --- S3: dua periode 20 hari berurutan tanpa jeda -> Rp0 per periode + peringatan PERLU REVIEW
# Gabungan 1 Jan - 9 Feb 2026 = 1 bulan 9 hari = 1 + 9/28 -> 37/28 / 12 x 5 jt = 550.595,24 -> Rp550.595
h = H(["1/1/2026 s.d. 20/1/2026", "21/1/2026 s.d. 9/2/2026"], upah="5jt")
cek("S3 tetap Rp0 per periode", h["total_kompensasi"] == 0)
pr = [p for p in h["peringatan"] if "PERLU REVIEW" in p]
cek("S3 peringatan ada", len(pr) == 1, h["peringatan"])
cek("S3 peringatan isi", pr and "terus-menerus" in pr[0] and "Pasal 15" in pr[0] and "(a)" in pr[0]
    and "(b)" in pr[0] and "Rp550.595" in pr[0], pr)
# Dengan jeda 1 hari -> tidak ada peringatan gabungan (tidak terus-menerus)
h = H(["1/1/2026 s.d. 20/1/2026", "22/1/2026 s.d. 10/2/2026"], upah="5jt")
cek("S3 ada jeda tanpa peringatan gabungan", not any("PERLU REVIEW" in p for p in h["peringatan"]))
# Gabungan tetap < 1 bulan -> tidak perlu peringatan
h = H(["1/1/2026 s.d. 10/1/2026", "11/1/2026 s.d. 20/1/2026"], upah="5jt")
cek("S3 gabungan < 1 bulan tanpa peringatan", not any("PERLU REVIEW" in p for p in h["peringatan"]))
# Semua periode sudah berhak -> tidak perlu peringatan
h = H(["1/1/2025 s.d. 31/12/2025", "1/1/2026 s.d. 30/6/2026"], upah="4,8jt")
cek("S3 periode normal tanpa peringatan", not any("PERLU REVIEW" in p for p in h["peringatan"]))
# Periode pendek di akhir rantai (12 bulan + 20 hari) -> peringatan
h = H(["1/1/2025 s.d. 31/12/2025", "1/1/2026 s.d. 20/1/2026"], upah="4,8jt")
cek("S3 periode pendek setelah periode panjang", any("PERLU REVIEW" in p for p in h["peringatan"]))

# --- R1: penulisan rupiah umum & periode tanpa spasi
cek("R1 rp koma strip", R("Rp 5.000.000,-") == 5000000)
cek("R1 rp titik strip", R("Rp5.000.000.-") == 5000000)
cek("R1 rp ,00", R("Rp5.000.000,00") == 5000000)
cek("R1 rp spasi ,00", R("Rp 5.000.000,00") == 5000000)
h = H(["1/1/2026-31/12/2026"], upah="Rp 5.000.000,-")
cek("R1 periode tanpa spasi", h["total_kompensasi"] == 5000000)
h = H(["2026-01-01-2026-12-31"], upah="5jt")
cek("R1 periode iso tanpa spasi", h["total_kompensasi"] == 5000000)
h = H(["1-1-2026-31-12-2026"], upah="5jt")
cek("R1 periode d-m-y tanpa spasi", h["total_kompensasi"] == 5000000)
harus_error("R1 teks tetap ditolak", lambda: R("lima juta,-"), "bukan angka")

# --- R2: upah terlalu kecil -> peringatan (tidak diam)
h = H(["1/1/2026 s.d. 31/12/2026"], upah="4.500")
pr = [p for p in h["peringatan"] if "PERIKSA UPAH" in p]
cek("R2 upah 4.500 diperingatkan", h["upah_sebulan"] == 4500 and pr and "Rp4.500.000" in pr[0], h["peringatan"])
h = H(["1/1/2026 s.d. 31/12/2026"], upah="350rb")
cek("R2 upah < 500rb diperingatkan", any("PERIKSA UPAH" in p for p in h["peringatan"]))
h = H(["1/1/2026 s.d. 31/12/2026"], gaji_pokok="5.000")
cek("R2 gaji pokok kecil diperingatkan", any("PERIKSA UPAH" in p for p in h["peringatan"]))
h = H(["1/1/2026 s.d. 31/12/2026"], upah="2,1jt")
cek("R2 upah wajar tanpa peringatan", not any("PERIKSA UPAH" in p for p in h["peringatan"]))

# --- R5: melebihi 5 tahun -> kalimat ilustrasi
h = H(["1/1/2022 s.d. 31/12/2026", "1/1/2027 s.d. 31/12/2027"], upah="3jt")
cek("R5 ilustrasi setelah batas", any("hanya ilustrasi" in p for p in h["peringatan"]))
h = H(["1/1/2026 s.d. 31/12/2026"], upah="3jt")
cek("R5 tidak muncul bila OK", not any("hanya ilustrasi" in p for p in h["peringatan"]))

# --- S2: checklist jam kerja tidak lagi menulis "7 jam x 6 hari"
_ck = open(os.path.join(os.path.dirname(SINI), "references", "checklist-periksa.md"), encoding="utf-8").read()
cek("S2 checklist tanpa 7 jam x 6 hari", "7 jam × 6 hari" not in _ck and "7 jam x 6 hari" not in _ck)
cek("S2 checklist 40 jam/minggu 6 hari", "Pasal 21" in _ck and "40 jam/minggu" in _ck)

# --- R3/R4: panduan di SKILL.md
_sk = open(os.path.join(os.path.dirname(SINI), "SKILL.md"), encoding="utf-8").read()
cek("R3 panduan beberapa pekerja", "Beberapa pekerja sekaligus" in _sk)
cek("R4 panduan tanggal mulai tidak diketahui", "Tanggal mulai belum diketahui" in _sk)

# --- v1.0.2 perbaikan kecil (uji ulang 06)
# Angka pengunci metode default TIDAK berubah
h = H(["1/1/2026 s.d. 31/3/2026"], upah="3jt", berhenti="15/2/2026", pihak="pekerja")
g = h["ganti_rugi_pasal_62"]
cek("v102 kunci 4.392.857", g["nilai"] == 4392857, g)
# R-baru-1: label memakai pecahan yang dipakai (1,4643), bukan "1 bulan 16 hari"
cek("R-baru-1 label pecahan", "1,4643 bulan" in g["sisa_masa"] and "1 bulan 16 hari" not in g["sisa_masa"]
    and "1,5357" in g["sisa_masa"] and g["sisa_hari_kalender"] == 44, g["sisa_masa"])
p = cli(["--periode", "1/1/2026 s.d. 31/3/2026", "--upah", "3jt", "--berhenti", "15/2/2026",
         "--pihak-mengakhiri", "pekerja"])
cek("R-baru-1 teks tanpa label hari-bulan", "1 bulan 16 hari" not in p.stdout and "(3 - 1,5357) = 1,4643 bulan" in p.stdout
    and "hari hanya informasi" in p.stdout, p.stdout)
# R-baru-2: sisa 0 -> tidak ada rentang terbalik
h = H(["1/1/2026 s.d. 31/12/2026", "1/1/2027 s.d. 31/12/2027"], upah="5jt", berhenti="31/12/2026", pihak="pengusaha")
g = h["ganti_rugi_pasal_62"]
cek("R-baru-2 nilai 0 & tanpa rentang", g["nilai"] == 0 and g["sisa_dari"] is None and g["sisa_sampai"] is None, g)
p = cli(["--periode", "1/1/2026 s.d. 31/12/2026", "--periode", "1/1/2027 s.d. 31/12/2027", "--upah", "5jt",
         "--berhenti", "31/12/2026", "--pihak-mengakhiri", "pengusaha"])
cek("R-baru-2 teks tidak terbalik", "1 Januari 2027 s.d. 31 Desember 2026" not in p.stdout
    and "Tidak ada sisa di periode berjalan" in p.stdout, p.stdout)
# R-baru-3: CLI --metode bulan-penuh -> pesan ramah, exit 2
p = cli(["--periode", "1/1/2026 s.d. 15/3/2026", "--upah", "6,2jt", "--metode", "bulan-penuh"], kode=2)
cek("R-baru-3 cli pesan dihapus", "dihapus" in p.stderr and "Traceback" not in p.stderr, p.stderr)
# R-baru-4: "4,5" -> saran Rp4.500.000 (bukan Rp5.000)
h = H(["1/1/2026 s.d. 31/12/2026"], upah="4,5")
pr = [x for x in h["peringatan"] if "PERIKSA UPAH" in x]
cek("R-baru-4 saran juta", pr and "Rp4.500.000" in pr[0] and "Rp5.000?" not in pr[0], pr)
h = H(["1/1/2026 s.d. 31/12/2026"], upah="4.5")
pr = [x for x in h["peringatan"] if "PERIKSA UPAH" in x]
cek("R-baru-4 saran juta titik", pr and "Rp4.500.000" in pr[0], pr)
# R-baru-5: checklist B5 membedakan "tidak disebut" (🟠) vs "dikecualikan" (🔴)
_b5 = [b for b in _ck.splitlines() if b.startswith("| B5")]
cek("R-baru-5 B5 jelas", _b5 and "tidak disebut sama sekali" in _b5[0] and "🟠" in _b5[0] and "🔴" in _b5[0], _b5)
# SKILL.md tidak lagi menawarkan --metode bulan-penuh
cek("R-baru-3 SKILL.md tanpa opsi bulan-penuh", "`--harian` · `--metode bulan-penuh`" not in _sk and "dihapus sejak v1.0.2" in _sk)

# --- v1.0.3: usaha mikro/kecil (PP 35/2021 Pasal 16 ayat (6): besaran kompensasi = kesepakatan)
# Angka rupiah metode default TIDAK berubah dengan/tanpa opsi; hanya label & catatan.
for _umk in (False, True):
    h = H(["1/10/2026 s.d. 30/9/2027"], gaji_pokok="3,8jt", tunjangan_tetap="300rb", usaha_mikro_kecil=_umk)
    cek("v103 kunci 4.100.000 umk={}".format(_umk), h["total_kompensasi"] == 4100000, h["total_kompensasi"])
    h = H(["1/1/2026 s.d. 31/3/2026"], upah="3jt", berhenti="15/2/2026", pihak="pekerja", usaha_mikro_kecil=_umk)
    cek("v103 kunci 4.392.857 umk={}".format(_umk), h["ganti_rugi_pasal_62"]["nilai"] == 4392857)
h = H(["1/1/2026 s.d. 31/12/2026"], upah="5jt")
cek("v103 default bukan umk", h["usaha_mikro_kecil"] is False and "Pasal 16 ayat (1)" in h["status_kompensasi"]
    and not any("USAHA MIKRO/KECIL" in x for x in h["peringatan"]))
h = H(["1/1/2026 s.d. 31/12/2026"], upah="5jt", usaha_mikro_kecil=True)
_pu = [x for x in h["peringatan"] if x.startswith("USAHA MIKRO/KECIL")]
cek("v103 umk catatan kesepakatan", h["usaha_mikro_kecil"] is True and h["total_kompensasi"] == 5000000
    and _pu and "Pasal 16 ayat (6)" in _pu[0] and "KESEPAKATAN" in _pu[0] and "ACUAN" in _pu[0]
    and "BUKAN jumlah yang diwajibkan" in _pu[0] and "kesepakatan" in h["status_kompensasi"], h["peringatan"])
p = cli(["--periode", "1/1/2026 s.d. 30/6/2026", "--upah", "3jt", "--usaha-mikro-kecil"])
cek("v103 cli umk label acuan", "ACUAN KOMPENSASI" in p.stdout and "Rp1.500.000" in p.stdout
    and "TOTAL KOMPENSASI (dibayar" not in p.stdout and "Pasal 16 ayat (6)" in p.stdout, p.stdout)
p = cli(["--periode", "1/1/2026 s.d. 30/6/2026", "--upah", "3jt", "--usaha-mikro-kecil", "--format", "json"])
if p.returncode == 0:
    j = json.loads(p.stdout)
    cek("v103 cli json umk", j["usaha_mikro_kecil"] is True and j["total_kompensasi"] == 1500000)
p = cli(["--periode", "1/1/2026 s.d. 30/6/2026", "--upah", "3jt"])
cek("v103 cli default tetap total + petunjuk umk", "TOTAL KOMPENSASI (dibayar pengusaha ke pekerja): Rp1.500.000"
    in p.stdout and "--usaha-mikro-kecil" in p.stdout, p.stdout)
# SKILL.md, checklist, template menyebut usaha mikro/kecil & Pasal 16 ayat (6)
_tp = open(os.path.join(os.path.dirname(SINI), "templates", "kerangka-pkwt.md"), encoding="utf-8").read()
cek("v103 SKILL.md umk", "--usaha-mikro-kecil" in _sk and _sk.count("Pasal 16 ayat (6)") >= 3)
cek("v103 checklist umk", "Pasal 16 ayat (6)" in _ck and "usaha mikro" in _ck.lower())
cek("v103 template klausul kesepakatan", "Pasal 16 ayat (6)" in _tp and "disepakati" in _tp)
# Rujukan pasal sesuai naskah resmi: 1/173 = PP 35/2021 Pasal 32 ayat (2); tidak ada klaim "rata-rata 12 bulan"
cek("v103 1/173 Pasal 32", "Pasal 32 ayat (2)" in _tp and "Pasal 32 ayat (2)" in _ck)
# "rata-rata 12 bulan terakhir" hanya boleh muncul sebagai koreksi yang menunjuk Pasal 33 ayat (2) (upah lembur)
_baris12 = [x for x in (_sk + _tp + _ck).splitlines() if "12 bulan terakhir" in x]
cek("v103 rata-rata 12 bulan = Pasal 33(2) lembur", all("Pasal 33 ayat (2)" in x and "lembur" in x for x in _baris12),
    _baris12)

# --- v1.0.4: konsistensi istilah acuan UMK, judul kolom, tanggal dicek
p = cli(["--periode", "1/1/2026 s.d. 30/6/2026", "--upah", "3jt", "--usaha-mikro-kecil"])
cek("v104 umk kolom acuan", "| Kompensasi (acuan) |" in p.stdout and "Rp1.500.000" in p.stdout, p.stdout)
cek("v104 umk tanpa batas bawah praktik", "batas bawah praktik" not in p.stdout
    and "BUKAN batas bawah wajib" in p.stdout, p.stdout)
cek("v104 footer dicek 26 Sep", "dicek 26 September 2026" in p.stdout and "25 September 2026" not in p.stdout)
p = cli(["--periode", "1/1/2026 s.d. 30/6/2026", "--upah", "3jt"])
cek("v104 non-umk kolom biasa", "| Kompensasi |" in p.stdout and "(acuan)" not in p.stdout, p.stdout)
cek("v104 SKILL.md konsisten B4a", "batas bawah praktik" not in _sk and "bukan batas bawah wajib" in _sk)
_scr = open(os.path.join(os.path.dirname(SINI), "scripts", "hitung_pkwt.py"), encoding="utf-8").read()
cek("v104 script tanpa batas bawah praktik", "batas bawah praktik" not in _scr)

# ------------------------------------------------------------ CLI
p = cli(["--periode", "1 Januari 2026 s.d. 31 Desember 2026", "--gaji-pokok", "5jt", "--tunjangan-tetap", "500rb",
         "--format", "json"])
if p.returncode == 0:
    j = json.loads(p.stdout)
    cek("cli json total", j["total_kompensasi"] == 5500000)
p = cli(["--periode", "1 Januari 2026 s.d. 31 Desember 2026", "--upah", "Rp5.500.000"])
cek("cli teks memuat total", "TOTAL KOMPENSASI" in p.stdout and "Rp5.500.000" in p.stdout)
cek("cli teks memuat disclaimer", "Bukan nasihat hukum" in p.stdout)
p = cli(["--periode", "31/12/2026 s.d. 1/1/2026", "--upah", "5jt"], kode=2)
cek("cli error ramah", "ERROR" in p.stderr and "Traceback" not in p.stderr)
p = cli(["--periode", "1/1/2026 s.d. 31/12/2026", "--upah=-5jt"], kode=2)
cek("cli negatif ramah", "negatif" in p.stderr and "Traceback" not in p.stderr)

# ------------------------------------------------------------ hasil
if GAGAL:
    print("GAGAL {} dari {} cek:".format(len(GAGAL), JUMLAH[0]))
    for g in GAGAL:
        print(" - " + g)
    sys.exit(1)
print("LULUS semua {} cek.".format(JUMLAH[0]))
