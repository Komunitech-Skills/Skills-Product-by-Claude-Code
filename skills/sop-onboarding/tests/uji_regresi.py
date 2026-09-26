#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Uji regresi scripts/jadwal_onboarding.py (hanya library standar).

Jalankan dari mana saja:  python3 tests/uji_regresi.py   (Windows: python atau py)
Keluar 0 bila semua lulus.
"""
import csv
import json
import os
import random
import subprocess
import sys
import tempfile
from datetime import date, timedelta

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
# Batas hukum akhir masa percobaan: 28 Sep + 3 bulan = 28 Des, dikurangi 1 hari = 27 Des 2026
batas = cari(h, "batas_percobaan")
cek("batas hukum percobaan pkwtt", batas["tanggal_target"] == "2026-12-27", batas)
cek("batas hukum tidak digeser walau bukan hari kerja", batas["digeser"] is False)
evaluasi = cari(h, "evaluasi_percobaan")
cek("evaluasi percobaan pkwtt (5 hari kerja sebelum batas)", evaluasi["tanggal_disesuaikan"] == "2026-12-21",
    evaluasi)
cek("evaluasi percobaan <= batas hukum", evaluasi["tanggal_disesuaikan"] <= batas["tanggal_disesuaikan"])
h90_dasar = cari(h, "hari90")
cek("checkpoint 90 hari 28 Sep melewati batas -> ada peringatan",
    h90_dasar["tanggal_disesuaikan"] == "2026-12-28" and "SETELAH batas hukum" in h90_dasar["catatan"],
    h90_dasar)
cek("peringatan global memuat checkpoint90", any("SETELAH batas hukum" in p for p in h["peringatan"]))

# ------------------------------------------------------------ PKWT tanpa masa percobaan
h2 = H(mulai, jenis="pkwt")
ap2 = cari(h2, "percobaan_pkwt")
cek("pkwt tanpa tanggal percobaan", ap2["tanggal_target"] is None and "DILARANG" in ap2["catatan"])
cek("pkwt tidak punya baris batas_percobaan", not any(t["kode"] == "batas_percobaan" for t in h2["tahapan"]))

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

# ------------------------------------------------------------ evaluasi akhir percobaan mundur dari batas
# mulai 2026-06-28 (Minggu) -> batas hukum = +3 bulan - 1 hari = 27 Sep 2026 (Minggu, TIDAK digeser).
# Evaluasi = 5 hari kerja mundur dari batas -> 21 Sep 2026 (Senin).
h7 = H(date(2026, 6, 28), hari_kerja=5, jenis="pkwtt")
batas7 = cari(h7, "batas_percobaan")
cek("batas hukum tetap walau minggu, tidak digeser", batas7["tanggal_target"] == "2026-09-27"
    and batas7["digeser"] is False, batas7)
evaluasi7 = cari(h7, "evaluasi_percobaan")
cek("evaluasi percobaan 5 hari kerja sebelum batas", evaluasi7["tanggal_disesuaikan"] == "2026-09-21", evaluasi7)

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

# ------------------------------------------------------------ h1 di hari libur -> peringatan (P2-1)
h_minggu = H(date(2026, 10, 4), hari_kerja=5)  # 4 Okt 2026 = Minggu
cek("h1 minggu ada peringatan", any("hari libur/akhir pekan" in p for p in h_minggu["peringatan"]))
cek("h1 minggu tidak digeser sendiri", cari(h_minggu, "h1")["tanggal_disesuaikan"] == "2026-10-04")
h_kerja_normal = H(date(2026, 9, 28), hari_kerja=5, jenis="pkwt")  # Senin, hari kerja, pkwt (tanpa cek batas)
cek("h1 hari kerja tidak ada peringatan", h_kerja_normal["peringatan"] == [])

# ------------------------------------------------------------ definisi batas hukum akhir masa percobaan
BH = jo.hitung_batas_hukum_percobaan
cek("batas 14 Des 2026 -> 13 Mar 2027", BH(date(2026, 12, 14)) == date(2027, 3, 13))
cek("batas 31 Jan 2027 -> 30 Apr 2027 (akhir bulan)", BH(date(2027, 1, 31)) == date(2027, 4, 30))
cek("batas 30 Nov 2027 -> 29 Feb 2028 (akhir bulan, leap)", BH(date(2027, 11, 30)) == date(2028, 2, 29))
cek("batas 29 Feb 2028 -> 28 Mei 2028", BH(date(2028, 2, 29)) == date(2028, 5, 28))

# ------------------------------------------------------------ P1-1: evaluasi akhir percobaan SELALU <= batas hukum
kasus_p1_1 = [
    date(2026, 12, 14),  # contoh eksplisit + rentang libur Lebaran 2027
    date(2027, 1, 31),
    date(2028, 2, 29),
    date(2026, 10, 4),   # H1 di hari Minggu
    date(2027, 2, 10),
    date(2027, 11, 30),
]
random.seed(42)
basis = date(2026, 1, 1)
for _ in range(8):
    kasus_p1_1.append(basis + timedelta(days=random.randint(0, 900)))

for hk in (5, 6):
    for mulai_kasus in kasus_p1_1:
        libur_default, _, _ = jo.libur_bawaan(mulai_kasus.year, mulai_kasus.year + 1)
        h_kasus = H(mulai_kasus, hari_kerja=hk, jenis="pkwtt", libur=libur_default)
        batas = cari(h_kasus, "batas_percobaan")
        evaluasi = cari(h_kasus, "evaluasi_percobaan")
        cek("evaluasi percobaan <= batas hukum ({}, hk={})".format(mulai_kasus, hk),
            date.fromisoformat(evaluasi["tanggal_disesuaikan"]) <= date.fromisoformat(batas["tanggal_disesuaikan"]),
            (mulai_kasus, hk, evaluasi["tanggal_disesuaikan"], batas["tanggal_disesuaikan"]))
        cek("batas hukum tidak pernah digeser ({}, hk={})".format(mulai_kasus, hk),
            batas["digeser"] is False)
        h90 = cari(h_kasus, "hari90")
        if date.fromisoformat(h90["tanggal_disesuaikan"]) > date.fromisoformat(batas["tanggal_disesuaikan"]):
            cek("peringatan checkpoint90 > batas muncul ({}, hk={})".format(mulai_kasus, hk),
                any("Checkpoint 90 hari" in p and "SETELAH batas hukum" in p for p in h_kasus["peringatan"]))
            cek("catatan hari90 memuat peringatan ({}, hk={})".format(mulai_kasus, hk),
                "SETELAH batas hukum" in h90["catatan"])

# Kasus rentang libur Lebaran 2027 (SKB 3 Menteri): 14 Des 2026, hari_kerja 5, pakai libur bawaan
libur_2026_2027, ditemukan, tidak_ada = jo.libur_bawaan(2026, 2027)
cek("libur bawaan 2026 & 2027 ditemukan", ditemukan == [2026, 2027], ditemukan)
h_lebaran = H(date(2026, 12, 14), hari_kerja=5, jenis="pkwtt", libur=libur_2026_2027)
batas_lebaran = cari(h_lebaran, "batas_percobaan")
eval_lebaran = cari(h_lebaran, "evaluasi_percobaan")
cek("batas hukum 14 Des 2026 = 13 Mar 2027 (Sabtu, tidak digeser)",
    batas_lebaran["tanggal_disesuaikan"] == "2027-03-13")
cek("evaluasi percobaan 14 Des 2026 mundur dari libur Lebaran <= batas",
    date.fromisoformat(eval_lebaran["tanggal_disesuaikan"]) <= date(2027, 3, 13), eval_lebaran)

# ------------------------------------------------------------ libur bawaan dimuat otomatis lewat CLI
p_bawaan = cli(["--mulai", "2026-12-14", "--jenis", "pkwtt", "--format", "json"])
if p_bawaan.returncode == 0:
    j_bawaan = json.loads(p_bawaan.stdout)
    cek("cli muat libur bawaan otomatis", j_bawaan["libur_bawaan_ditemukan"] == [2026, 2027], j_bawaan)
    cek("cli jumlah libur > 0", j_bawaan["jumlah_hari_libur_dimuat"] > 0)
p_tanpa = cli(["--mulai", "2026-12-14", "--jenis", "pkwtt", "--tanpa-libur-bawaan", "--format", "json"])
if p_tanpa.returncode == 0:
    j_tanpa = json.loads(p_tanpa.stdout)
    cek("cli --tanpa-libur-bawaan menonaktifkan", j_tanpa["jumlah_hari_libur_dimuat"] == 0)

# ------------------------------------------------------------ v1.0.2: P3 tanggal tahun 9999 / di luar rentang
harus_error("tahun 9999 tidak crash", lambda: T("9999-12-31"), "di luar rentang")
harus_error("tahun 1800 di luar rentang bawah", lambda: T("1800-01-01"), "di luar rentang")
cek("tahun batas bawah 1900 diterima", T("1900-01-01").isoformat() == "1900-01-01")
cek("tahun batas atas 9900 diterima", T("9900-01-01").isoformat() == "9900-01-01")
p_9999 = cli(["--mulai", "9999-12-31"], kode=2)
cek("cli tahun 9999 pesan ramah, tanpa Traceback",
    "ERROR" in p_9999.stderr and "Traceback" not in p_9999.stderr and "di luar rentang" in p_9999.stderr,
    p_9999.stderr)
p_1800 = cli(["--mulai", "1800-01-01"], kode=2)
cek("cli tahun 1800 pesan ramah, tanpa Traceback",
    "ERROR" in p_1800.stderr and "Traceback" not in p_1800.stderr, p_1800.stderr)

# ------------------------------------------------------------ v1.0.2: P3 CSV libur berpemisah titik-koma
with tempfile.TemporaryDirectory() as td:
    path_titik_koma = os.path.join(td, "libur_titik_koma.csv")
    with open(path_titik_koma, "w", encoding="utf-8", newline="") as f:
        f.write("tanggal;keterangan\n25/12/2026;Natal\n1/1/2027;Tahun Baru\n")
    libur_tk = jo.baca_libur(path_titik_koma)
    cek("csv titik-koma terbaca 2 tanggal", libur_tk == {date(2026, 12, 25), date(2027, 1, 1)}, libur_tk)

    # Delimiter koma tetap berfungsi seperti sebelumnya (tidak boleh berubah)
    path_koma = os.path.join(td, "libur_koma.csv")
    with open(path_koma, "w", encoding="utf-8", newline="") as f:
        f.write("tanggal,keterangan\n25/12/2026,Natal\n")
    cek("csv koma tetap terbaca", jo.baca_libur(path_koma) == {date(2026, 12, 25)})

# ------------------------------------------------------------ v1.0.2: P2 cuti bersama fakultatif (swasta)
with tempfile.TemporaryDirectory() as td:
    path_campuran = os.path.join(td, "libur_campuran.csv")
    with open(path_campuran, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["tanggal", "jenis", "keterangan"])
        w.writerow(["2026-12-24", "cuti", "Cuti bersama Natal"])
        w.writerow(["2026-12-25", "libur", "Hari Natal"])
    libur_default = jo.baca_libur(path_campuran)
    cek("default: cuti bersama tetap dihitung libur",
        libur_default == {date(2026, 12, 24), date(2026, 12, 25)}, libur_default)
    libur_dikecualikan = jo.baca_libur(path_campuran, kecualikan_cuti_bersama=True)
    cek("--cuti-bersama-hari-kerja: baris 'cuti' dikecualikan, 'libur' tetap ada",
        libur_dikecualikan == {date(2026, 12, 25)}, libur_dikecualikan)

# CLI: libur bawaan 2026 berkurang saat cuti bersama dianggap hari kerja
p_cb_default = cli(["--mulai", "2026-02-10", "--jenis", "pkwtt", "--format", "json"])
p_cb_flag = cli(["--mulai", "2026-02-10", "--jenis", "pkwtt", "--cuti-bersama-hari-kerja", "--format", "json"])
if p_cb_default.returncode == 0 and p_cb_flag.returncode == 0:
    j_cb_default = json.loads(p_cb_default.stdout)
    j_cb_flag = json.loads(p_cb_flag.stdout)
    cek("cli --cuti-bersama-hari-kerja mengurangi jumlah hari libur dimuat",
        j_cb_flag["jumlah_hari_libur_dimuat"] < j_cb_default["jumlah_hari_libur_dimuat"],
        (j_cb_default["jumlah_hari_libur_dimuat"], j_cb_flag["jumlah_hari_libur_dimuat"]))
    cek("cli metadata cuti_bersama_dianggap_hari_kerja",
        j_cb_flag["cuti_bersama_dianggap_hari_kerja"] is True
        and j_cb_default["cuti_bersama_dianggap_hari_kerja"] is False)

# ------------------------------------------------------------ v1.0.2: P3 B-3 kejelasan "hari kerja ke-5 mundur"
# Verifikasi independen definisi: hari kerja terakhir <= batas hukum dihitung sebagai hari kerja KE-1
# (bukan ke-0), lalu mundur satu per satu sampai hari kerja ke-5. Batas 2026-12-27 (Minggu, hk=5, tanpa
# libur tambahan): ke-1=25 Des (Jum), ke-2=24 Des (Kam), ke-3=23 Des (Rab), ke-4=22 Des (Sel), ke-5=21 Des
# (Sen).
cek("mundur_n_hari_kerja: hari kerja ke-1 = hari kerja terakhir <= batas",
    jo.mundur_n_hari_kerja(date(2026, 12, 27), 1, 5, set()) == date(2026, 12, 25))
cek("mundur_n_hari_kerja: hari kerja ke-5 mundur dari batas",
    jo.mundur_n_hari_kerja(date(2026, 12, 27), 5, 5, set()) == date(2026, 12, 21))
# hitung_jadwal (kasus dasar mulai 28 Sep 2026, hk=5, pkwtt, tanpa libur) harus memakai definisi yang sama:
# batas hukum = 27 Des 2026, evaluasi = hari kerja ke-5 mundur = 21 Des 2026 (sudah diuji di atas juga).
h_b3 = H(date(2026, 9, 28), hari_kerja=5, jenis="pkwtt")
evaluasi_b3 = cari(h_b3, "evaluasi_percobaan")
cek("evaluasi_percobaan hitung_jadwal cocok dengan mundur_n_hari_kerja",
    evaluasi_b3["tanggal_disesuaikan"] == "2026-12-21", evaluasi_b3)

# ------------------------------------------------------------ hasil
if GAGAL:
    print("GAGAL {} dari {} cek:".format(len(GAGAL), JUMLAH[0]))
    for g in GAGAL:
        print(" - " + g)
    sys.exit(1)
print("LULUS semua {} cek.".format(JUMLAH[0]))
