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
h = H(["1 Januari 2026 s.d. 15 Maret 2026"], upah="6,2jt", metode="bulan-penuh")
cek("metode bulan penuh", h["total_kompensasi"] == 1033333, h["total_kompensasi"])  # 2/12 x 6.2jt
cek("metode bulan penuh ada peringatan", any("bulan-penuh" in p for p in h["peringatan"]))

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

# Sisa dengan hari: berhenti 15 Mar 2026, akhir 30 Jun 2026: sisa 16 Mar - 30 Jun = 3 bulan 15 hari
# (16 Mar + 3 bln = 16 Jun; 16-30 Jun = 15 hari dari bulan berjalan 16 Jun - 15 Jul = 30 hari) -> 3,5 x 4,8jt
h = H(["1/1/2025 s.d. 31/12/2025", "1/1/2026 s.d. 30/6/2026"], upah="Rp4.800.000", berhenti="15/03/2026",
      pihak="pengusaha")
cek("dini sisa hari", h["ganti_rugi_pasal_62"]["nilai"] == 16800000, h["ganti_rugi_pasal_62"])
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
