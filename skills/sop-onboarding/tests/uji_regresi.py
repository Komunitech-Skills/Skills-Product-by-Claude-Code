#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Uji regresi scripts/jadwal_onboarding.py (hanya library standar).

Jalankan dari mana saja:  python3 tests/uji_regresi.py   (Windows: python atau py)
Keluar 0 bila semua lulus.
"""
import csv
import json
import os
import subprocess
import sys
import tempfile
from datetime import date

SINI = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(os.path.dirname(SINI), "scripts")
SCRIPT = os.path.join(SCRIPTS, "jadwal_onboarding.py")
sys.dont_write_bytecode = True
sys.path.insert(0, SCRIPTS)
import jadwal_onboarding as jo  # noqa: E402

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
    except jo.InputSalah as e:
        if potongan_pesan and potongan_pesan.lower() not in str(e).lower():
            GAGAL.append("{}: pesan error tidak memuat '{}': {}".format(nama, potongan_pesan, e))
        return
    GAGAL.append("{}: seharusnya error".format(nama))


def cli(args, kode=0):
    proc = subprocess.run([sys.executable, SCRIPT] + args, capture_output=True, text=True, encoding="utf-8")
    JUMLAH[0] += 1
    if proc.returncode != kode:
        GAGAL.append("CLI {} -> kode {} (harap {}): {}".format(args, proc.returncode, kode, proc.stderr.strip()))
    return proc


def cari(hasil, kode):
    for t in hasil["tahapan"]:
        if t["kode"] == kode:
            return t
    raise KeyError(kode)


# ------------------------------------------------------------ parsing tanggal
T = jo.parse_tanggal
cek("tgl iso", T("2026-09-28").isoformat() == "2026-09-28")
cek("tgl dd/mm/yyyy", T("28/09/2026").isoformat() == "2026-09-28")
cek("tgl indo panjang", T("28 September 2026").isoformat() == "2026-09-28")
cek("tgl indo singkat", T("5 Okt 2026").isoformat() == "2026-10-05")
cek("tgl dengan hari", T("Senin, 28 September 2026").isoformat() == "2026-09-28")
harus_error("tgl 31 Feb", lambda: T("31/02/2026"), "tidak ada di kalender")
harus_error("tgl kosong", lambda: T(""), "kosong")
harus_error("tgl teks", lambda: T("besok"), "tidak dikenali")
harus_error("tgl bulan ngawur", lambda: T("1 Janubari 2026"), "bulan")

# ------------------------------------------------------------ hitung_jadwal dasar (Senin 28 Sep 2026)
H = jo.hitung_jadwal
mulai = date(2026, 9, 28)
h = H(mulai, hari_kerja=5, jenis="pkwtt")
cek("h1 = mulai", cari(h, "h1")["tanggal_disesuaikan"] == "2026-09-28")
cek("minggu1 = mulai+6", cari(h, "minggu1")["tanggal_target"] == "2026-10-04")
cek("hari30 = mulai+29", cari(h, "hari30")["tanggal_target"] == "2026-10-27")
cek("hari60 = mulai+59", cari(h, "hari60")["tanggal_target"] == "2026-11-26")
cek("hari90 = mulai+89", cari(h, "hari90")["tanggal_target"] == "2026-12-26")
# Akhir masa percobaan: 28 Sep + 3 bulan = 28 Des, dikurangi 1 hari = 27 Des 2026
ap = cari(h, "akhir_percobaan")
cek("akhir percobaan pkwtt", ap["tanggal_target"] == "2026-12-27", ap)
cek("akhir percobaan tidak digeser walau bukan hari kerja", ap["tanggal_target"] is not None)

# ------------------------------------------------------------ PKWT tanpa masa percobaan
h2 = H(mulai, jenis="pkwt")
ap2 = cari(h2, "akhir_percobaan")
cek("pkwt tanpa tanggal percobaan", ap2["tanggal_target"] is None and "DILARANG" in ap2["catatan"])

# ------------------------------------------------------------ penyesuaian akhir pekan (geser maju)
# 1 Jan 2026 = Kamis. minggu1 target = 1+6 = 7 Jan (Rabu, hari kerja) -> tidak digeser.
# Pilih kasus yang jatuh Sabtu: mulai 1 Sep 2026 (Selasa) -> hari30 = mulai+29 = 30 Sep (Rabu, kerja).
# Uji eksplisit dengan tanggal yang pasti jatuh akhir pekan: mulai 2026-09-01 (Selasa),
# minggu1 = 2026-09-07 (Senin, kerja, cek tidak digeser dulu)
h3 = H(date(2026, 9, 1), hari_kerja=5)
cek("minggu1 senin tidak digeser", cari(h3, "minggu1")["digeser"] is False)
# Cari kasus akhir pekan: mulai Senin 2026-08-31 -> minggu1 target = 2026-09-06 (Minggu) -> digeser ke Senin 07
h4 = H(date(2026, 8, 31), hari_kerja=5)
m1 = cari(h4, "minggu1")
cek("minggu1 minggu digeser ke senin", m1["tanggal_target"] == "2026-09-06"
    and m1["tanggal_disesuaikan"] == "2026-09-07" and m1["digeser"] is True, m1)

# hari_kerja=6: hanya Minggu libur. mulai Senin 2026-08-31, minggu1 target 2026-09-06 (Minggu) -> digeser Senin 07
h5 = H(date(2026, 8, 31), hari_kerja=6)
m1b = cari(h5, "minggu1")
cek("hari_kerja 6 hanya minggu libur", m1b["tanggal_disesuaikan"] == "2026-09-07")
# Sabtu harus dianggap kerja saat hari_kerja=6
cek("sabtu kerja saat hari_kerja=6", jo.hari_kerja_p(date(2026, 9, 5), 6, set()) is True)
cek("sabtu libur saat hari_kerja=5", jo.hari_kerja_p(date(2026, 9, 5), 5, set()) is False)

# ------------------------------------------------------------ hari libur dari file CSV
with tempfile.TemporaryDirectory() as td:
    path = os.path.join(td, "libur.csv")
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["tanggal"])
        w.writerow(["2026-10-27"])  # sengaja bertepatan dengan hari30 di kasus dasar
    libur = jo.baca_libur(path)
    cek("baca libur 1 tanggal", libur == {date(2026, 10, 27)})
    h6 = H(mulai, hari_kerja=5, libur=libur)
    h30 = cari(h6, "hari30")
    cek("hari30 digeser karena libur", h30["tanggal_target"] == "2026-10-27"
        and h30["tanggal_disesuaikan"] == "2026-10-28" and h30["digeser"] is True, h30)

    path2 = os.path.join(td, "libur_kosong.csv")
    with open(path2, "w", encoding="utf-8") as f:
        f.write("# tidak ada libur\n\n")
    cek("libur file kosong/komentar", jo.baca_libur(path2) == set())

    path3 = os.path.join(td, "libur_salah.csv")
    with open(path3, "w", encoding="utf-8") as f:
        f.write("tanggal\nbukan-tanggal\n")
    harus_error("libur isi salah", lambda: jo.baca_libur(path3), "tidak dikenali")

harus_error("libur file tidak ada", lambda: jo.baca_libur("/tidak/ada/file.csv"), "tidak bisa membaca")

# ------------------------------------------------------------ evaluasi akhir percobaan digeser mundur
# Cari kasus akhir_percobaan jatuh di akhir pekan: mulai 2026-06-28 (Minggu) -> +3 bulan = 28 Sep - 1 hari
# = 27 Sep 2026 (Minggu) -> evaluasi disarankan digeser MUNDUR ke Sabtu 26? Sabtu bukan hari kerja (hari_kerja=5)
# -> lanjut mundur ke Jumat 25 Sep 2026.
h7 = H(date(2026, 6, 28), hari_kerja=5, jenis="pkwtt")
ap7 = cari(h7, "akhir_percobaan")
cek("akhir percobaan hukum tidak digeser (tetap minggu)", ap7["tanggal_target"] == "2026-09-27")
cek("evaluasi disarankan digeser mundur ke hari kerja", ap7["tanggal_disesuaikan"] == "2026-09-25"
    and ap7["digeser"] is True, ap7)

# ------------------------------------------------------------ input salah lainnya
harus_error("hari_kerja invalid", lambda: H(mulai, hari_kerja=7), "5 atau 6")
harus_error("jenis invalid", lambda: H(mulai, jenis="magang"), "pkwt")

# ------------------------------------------------------------ output markdown & csv
md = jo.ke_markdown(h, nama_karyawan="Rina")
cek("markdown ada judul nama", "Rina" in md)
cek("markdown ada tabel", "| Tahap |" in md)
cek("markdown ada catatan percobaan", "Pasal 60" in md)
csv_out = jo.ke_csv(h)
cek("csv ada header", csv_out.splitlines()[0].startswith("kode,tahap"))
cek("csv jumlah baris = jumlah tahapan", len(csv_out.strip().splitlines()) - 1 == len(h["tahapan"]))

# ------------------------------------------------------------ CLI
p = cli(["--mulai", "2026-09-28", "--format", "json"])
if p.returncode == 0:
    j = json.loads(p.stdout)
    cek("cli json mulai", j["tanggal_mulai"] == "2026-09-28")
p = cli(["--mulai", "2026-09-28", "--jenis", "pkwt", "--format", "markdown"])
cek("cli markdown pkwt tanpa percobaan", "DILARANG" in p.stdout)
p = cli(["--mulai", "2026-09-28", "--format", "csv"])
cek("cli csv header", p.stdout.startswith("kode,tahap"))
p = cli(["--mulai", "31/02/2026"], kode=2)
cek("cli error ramah", "ERROR" in p.stderr and "Traceback" not in p.stderr)
p = cli(["--mulai", "2026-09-28", "--hari-kerja", "7"], kode=2)
cek("cli hari-kerja invalid", p.returncode == 2)

# ------------------------------------------------------------ hasil
if GAGAL:
    print("GAGAL {} dari {} cek:".format(len(GAGAL), JUMLAH[0]))
    for g in GAGAL:
        print(" - " + g)
    sys.exit(1)
print("LULUS semua {} cek.".format(JUMLAH[0]))
