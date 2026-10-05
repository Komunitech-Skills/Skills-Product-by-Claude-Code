#!/usr/bin/env python3
"""Uji regresi scripts/rasio.py (library standar saja).

Jalankan dari mana saja:  python3 tests/uji_regresi.py   (Windows: python / py)
Keluar 0 bila semua lulus. Angka harapan dihitung manual (dicatat di komentar) dan dicek ulang
dengan Fraction (pecahan persis), bukan dengan fungsi script itu sendiri.
Data uji ditulis ke folder sementara dan dihapus setelah selesai.
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
from decimal import Decimal
from fractions import Fraction as F

SINI = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(SINI, "..", "scripts", "rasio.py")
spec = importlib.util.spec_from_file_location("rasio", SCRIPT)
rasio = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rasio)

GAGAL = []
JUMLAH = [0]
TMP = tempfile.mkdtemp(prefix="uji-rasio-")


def cek(nama, kondisi, info=""):
    JUMLAH[0] += 1
    print(("OK    " if kondisi else "GAGAL ") + nama + ("" if kondisi else "  → " + str(info)))
    if not kondisi:
        GAGAL.append(nama)


def jalankan(*arg):
    p = subprocess.run([sys.executable, SCRIPT] + list(arg), capture_output=True, text=True, cwd=TMP)
    return p.returncode, p.stdout, p.stderr


def json_run(*arg):
    k, out, err = jalankan(*(list(arg) + ["--format", "json"]))
    return k, (json.loads(out) if k == 0 else json.loads(err or "{}"))


def tulis(nama, isi, mode="w"):
    path = os.path.join(TMP, nama)
    with open(path, mode) as f:
        f.write(isi)
    return path


def r_(h, kode, i=-1):
    return next((r for r in h["periode"][i]["rasio"] if r["kode"] == kode), None)


def dekat(a, b, tol=F(1, 10000)):
    return a is not None and abs(F(str(a)) - F(b)) <= tol


# ---------------------------------------------------------------- kasus A: Toko sembako (dagang, 12 bulan)
# Penjualan 480 jt, HPP 408 jt, laba bersih 24 jt. Kas 12, piutang 6, persediaan 40, aset tetap 42 (jt)
# → aset lancar 58, total aset 100. Utang usaha 20 + utang lancar lain 5 = UL 25; UJP 15 → utang 40; modal 60.
TOKO = ["--jenis", "warung", "--penjualan", "Rp 480.000.000", "--hpp", "408jt", "--laba-bersih", "24.000.000",
        "--kas", "12jt", "--piutang", "6 juta", "--persediaan", "40jt", "--aset-tetap", "42jt",
        "--utang-usaha", "20jt", "--utang-lancar-lain", "5jt", "--utang-jangka-panjang", "15jt",
        "--modal", "60jt", "--bulan", "12"]
k, h = json_run(*TOKO)
cek("A0 jalan tanpa galat, jenis 'warung' → dagang", k == 0 and h["jenis_usaha"] == "dagang", h)
cek("A1 rasio lancar = 58/25 = 2,32", dekat(r_(h, "rasio_lancar")["nilai"], F(58, 25)))
cek("A2 rasio cepat = (58−40)/25 = 0,72", dekat(r_(h, "rasio_cepat")["nilai"], F(18, 25)))
cek("A3 rasio kas = 12/25 = 0,48", dekat(r_(h, "rasio_kas")["nilai"], F(12, 25)))
cek("A4 modal kerja = 58 − 25 = Rp 33.000.000", r_(h, "modal_kerja")["nilai"] == 33000000)
cek("A5 margin kotor = 72/480 = 15,0% (tepat di batas → baik)",
    dekat(r_(h, "margin_kotor")["nilai"], 15) and r_(h, "margin_kotor")["status"] == "baik")
cek("A6 margin bersih = 24/480 = 5,0%", dekat(r_(h, "margin_bersih")["nilai"], 5))
cek("A7 ROA = 24/100 = 24%, ROE = 24/60 = 40%",
    dekat(r_(h, "roa")["nilai"], 24) and dekat(r_(h, "roe")["nilai"], 40))
cek("A8 DER = 40/60 = 0,6667 baik; DAR = 40%",
    dekat(r_(h, "der")["nilai"], F(2, 3)) and r_(h, "der")["status"] == "baik" and dekat(r_(h, "dar")["nilai"], 40))
cek("A9 umur stok = 40×365/408 = 35,78 hari → waspada (dagang 30–60)",
    dekat(r_(h, "hari_persediaan")["nilai"], F(40 * 365, 408)) and r_(h, "hari_persediaan")["status"] == "waspada")
cek("A10 hari piutang = 6×365/480 = 4,5625; hari utang = 20×365/408",
    dekat(r_(h, "hari_piutang")["nilai"], F(6 * 365, 480)) and dekat(r_(h, "hari_utang")["nilai"], F(20 * 365, 408)))
cek("A11 siklus kas = stok + piutang − utang = 22,45 hari",
    dekat(r_(h, "siklus_kas")["nilai"], F(40 * 365, 408) + F(6 * 365, 480) - F(20 * 365, 408), F(3, 10000)))
cek("A12 perputaran aset = 480/100 = 4,8x", dekat(r_(h, "perputaran_aset")["nilai"], F(24, 5)))
cek("A13 saran pertama untuk umur stok", h["saran"][0]["rasio"].startswith("Umur stok"))

# Kesiapan kredit: laba/bulan 2 jt; cicilan 500 rb = 25% AMAN; 3 jt = 150% ⛔
k, h = json_run(*(TOKO + ["--cicilan-bulanan", "500rb"]))
kk = h["periode"][-1]["kesiapan_kredit"]
cek("B1 cicilan 500rb / laba 2 jt per bulan = 25,0% → AMAN",
    kk["laba_bersih_per_bulan"] == 2000000 and kk["rasio_cicilan_persen"] == 25.0 and "AMAN" in kk["status_cicilan"])
cek("B2 kesimpulan ANGKA CUKUP SEHAT", kk["kesimpulan"].startswith("ANGKA CUKUP SEHAT"), kk["kesimpulan"])
k, h = json_run(*(TOKO + ["--cicilan-bulanan", "3jt"]))
kk = h["periode"][-1]["kesiapan_kredit"]
cek("B3 cicilan 3 jt = 150% → ⛔ & BELUM SIAP",
    kk["rasio_cicilan_persen"] == 150.0 and "⛔" in kk["status_cicilan"] and kk["kesimpulan"].startswith("BELUM"))
cek("B3b saran pertama = 'Rencana cicilan' bila cicilan > 30% laba", h["saran"][0]["rasio"] == "Rencana cicilan")
k, h = json_run(*(TOKO + ["--cicilan-bulanan", "800rb"]))
cek("B4 cicilan 800rb = 40% → BERAT (🟡)", "BERAT" in h["periode"][-1]["kesiapan_kredit"]["status_cicilan"])

# ---------------------------------------------------------------- kasus C: pembagian nol & angka negatif
k, h = json_run("--penjualan", "10jt", "--laba-bersih", "1jt", "--kas", "2jt", "--aset-tetap", "5jt",
                "--utang-lancar", "0", "--modal", "7jt")
cek("C1 utang lancar 0 → rasio lancar tidak dibagi nol, status info (aman)",
    r_(h, "rasio_lancar")["nilai"] is None and r_(h, "rasio_lancar")["status"] == "info")
k, h = json_run("--penjualan", "0", "--hpp", "0", "--laba-bersih", "-500rb", "--kas", "1jt", "--modal", "1jt",
                "--bulan", "1")
cek("C2 penjualan 0 → margin tidak dihitung (bukan 0%)",
    r_(h, "margin_bersih")["nilai"] is None and "penjualan Rp 0" in r_(h, "margin_bersih")["alasan_tidak_dihitung"])
k, h = json_run("--penjualan", "50jt", "--hpp", "45jt", "--laba-bersih", "(8.000.000)", "--kas", "1jt",
                "--persediaan", "5jt", "--aset-tetap", "10jt", "--utang-lancar", "20jt", "--modal", "-4jt",
                "--bulan", "6")
cek("C3 '(8.000.000)' dibaca rugi; margin bersih −16%", dekat(r_(h, "margin_bersih")["nilai"], -16))
cek("C4 modal −4 jt → ROE & DER tidak dihitung, status bahaya",
    r_(h, "roe")["nilai"] is None and r_(h, "roe")["status"] == "bahaya"
    and r_(h, "der")["nilai"] is None and r_(h, "der")["status"] == "bahaya")
cek("C5 DAR = 20/16 = 125%", dekat(r_(h, "dar")["nilai"], 125))
cek("C6 ROA 6 bulan disetahunkan: −8/16 × 365/182,5 = −100%", dekat(r_(h, "roa")["nilai"], -100))
cek("C7 saran diawali 'Usaha rugi' lalu 'Modal habis', maksimal 5 + 1 ringkasan",
    h["saran"][0]["rasio"] == "Usaha rugi" and h["saran"][1]["rasio"].startswith("Modal") and len(h["saran"]) <= 6)
kk = h["periode"][-1]["kesiapan_kredit"]
cek("C8 kesiapan kredit BELUM SIAP saat rugi & modal negatif", kk["kesimpulan"].startswith("BELUM"))
k, h = json_run("--kas", "-5jt", "--persediaan", "3jt", "--utang-lancar", "2jt", "--aset-tetap", "10jt",
                "--penjualan", "10jt", "--laba-bersih", "1jt")
cek("C9 kas negatif = mustahil → rasio lancar/ROA tidak dihitung, ada peringatan",
    r_(h, "rasio_lancar")["nilai"] is None and r_(h, "roa")["nilai"] is None
    and any("mustahil" in w for w in h["periode"][0]["peringatan"]) and h["status_data"] == "SEMENTARA")

# ---------------------------------------------------------------- kasus D: tabel multi-periode (tren, rata-rata)
LAUNDRY = """Pos;2024;2025
Pendapatan;Rp 180.000.000;Rp 216.000.000
HPP;54jt;71.280.000
Laba bersih;27.000.000;23.760.000
Kas;8jt;4jt
Piutang;3jt;9jt
Persediaan;2jt;3jt
Aset tetap;60jt;75jt
Utang usaha;4jt;6jt
Utang bank jangka pendek;6jt;12jt
Utang jangka panjang;20jt;35jt
Modal;43jt;38jt
Catatan kaki;x;y
"""
path = tulis("laundry.csv", LAUNDRY)
k, h = json_run(path, "--jenis", "laundry")
cek("D1 dua periode terbaca, jenis laundry → jasa", k == 0 and len(h["periode"]) == 2 and h["jenis_usaha"] == "jasa")
cek("D2 rasio lancar 2025 = 16/18 = 0,889 → bahaya (jasa < 1,0)",
    dekat(r_(h, "rasio_lancar")["nilai"], F(16, 18)) and r_(h, "rasio_lancar")["status"] == "bahaya")
cek("D3 ROE 2025 pakai rata-rata modal: 23,76/((43+38)/2) = 58,67%",
    dekat(r_(h, "roe")["nilai"], F(2376, 100) / F(81, 2) * 100))
cek("D4 ROA 2025 pakai rata-rata aset (73+91)/2 = 82 → 28,98%", dekat(r_(h, "roa")["nilai"], F(2376, 82)))
tr = {t["kode"]: t for t in h["tren"]}
cek("D5 tren: penjualan +20,0%, laba −12,0%, DER memburuk",
    tr["penjualan"]["pertumbuhan_persen"] == 20.0 and tr["laba_bersih"]["pertumbuhan_persen"] == -12.0
    and tr["der"]["arah"].startswith("memburuk"))
cek("D6 baris tak dikenal dilaporkan, tidak bikin galat",
    any("Catatan kaki" in c for c in h["catatan_input"]))

# Markdown table ditempel dari chat
MD = """| Pos | Nilai |
|---|---|
| Penjualan | 120.000.000 |
| Laba bersih | 6.000.000 |
| Total aset | 60.000.000 |
| Total utang | 20.000.000 |
| Modal | 40.000.000 |
"""
k, h = json_run(tulis("tempel.md", MD))
cek("D7 tabel Markdown: ROA 10%, DER 0,5; peringatan utang lancar tidak ada",
    dekat(r_(h, "roa")["nilai"], 10) and dekat(r_(h, "der")["nilai"], F(1, 2))
    and any("utang lancar" in w for w in h["periode"][0]["peringatan"]))

# Neraca tidak seimbang
k, h = json_run("--total-aset", "100jt", "--total-utang", "30jt", "--modal", "60jt", "--laba-bersih", "5jt",
                "--penjualan", "50jt")
cek("D8 neraca tidak seimbang → selisih Rp 10.000.000 dilaporkan",
    h["periode"][0]["selisih_neraca"] == 10000000 and any("TIDAK SEIMBANG" in w for w in h["periode"][0]["peringatan"]))

# ---------------------------------------------------------------- kasus E: output laporan-keuangan-emkm
EMKM = {"nama_usaha": "Katering Bu Rina", "status": "LENGKAP",
        "periode": {"awal": "2026-01-01", "akhir": "2026-03-31", "teks": "1 Januari 2026 s.d. 31 Maret 2026",
                    "jumlah_bulan": 3},
        "laba_rugi": {"pendapatan_usaha_bersih": 12000000, "penjualan_tempo": 0, "beban_pokok_penjualan": 3700000,
                      "laba_kotor": 8300000, "laba_usaha": 5000000, "beban_keuangan": 0,
                      "beban_pajak_penghasilan": 0, "laba_bersih": 5000000},
        "posisi_keuangan": {"aset": {"kas_dan_setara_kas": 12500000, "piutang_usaha": 0, "piutang_lain": 0,
                                     "persediaan": 800000, "aset_tetap_nilai_buku": 6000000, "total_aset": 19300000},
                            "liabilitas": {"utang_usaha": 0, "utang_bank_pinjaman": 10000000,
                                           "utang_pajak_daerah_titipan": 0, "total_liabilitas": 10000000},
                            "ekuitas": {"modal_akhir": 9300000}},
        "saldo_awal": {"persediaan": 0, "piutang": 0, "modal": 5000000}}
path = tulis("emkm.json", json.dumps(EMKM))
k, h = json_run(path, "--jenis", "katering")
cek("E1 EMKM: nama usaha & 90 hari terbaca; utang bank dianggap lancar → rasio lancar 13,3/10 = 1,33",
    h["nama_usaha"] == "Katering Bu Rina" and dekat(r_(h, "rasio_lancar")["nilai"], F(133, 100)))
k, h = json_run(path, "--jenis", "katering", "--bagian-lancar-utang-bank", "4jt", "--cicilan-bulanan", "950rb")
cek("E2 bagian lancar utang bank 4 jt → rasio lancar 13,3/4 = 3,325",
    dekat(r_(h, "rasio_lancar")["nilai"], F(133, 40)))
kk = h["periode"][-1]["kesiapan_kredit"]
cek("E3 laba/bulan = 5 jt/3 = 1.666.667; cicilan 950rb = 57,0% → TERLALU BERAT",
    kk["laba_bersih_per_bulan"] == 1666667 and kk["rasio_cicilan_persen"] == 57.0 and "TERLALU" in kk["status_cicilan"])
cek("E4 umur stok pakai rata-rata (0+0,8)/2 × 90 / 3,7 = 9,73 hari",
    dekat(r_(h, "hari_persediaan")["nilai"], F(4, 10) * 90 / F(37, 10)))

# ---------------------------------------------------------------- kasus F: input rusak & format angka
for teks, harap in (("Rp 1.500.000", 1500000), ("1,5jt", 1500000), ("150rb", 150000), ("2 juta", 2000000),
                    ("(15.000)", -15000), ("1.250.000,50", Decimal("1250000.50")), ("15.000,-", 15000),
                    ("1,2 M", 1200000000), ("abc", None), ("1.2.3", None)):
    cek("F parse '%s' → %s" % (teks, harap), rasio.parse_angka(teks) == (Decimal(harap) if harap is not None
                                                                           else None), rasio.parse_angka(teks))
k, out, err = jalankan(tulis("kosong.csv", ""))
cek("F11 file kosong → GALAT, kode 2, tanpa traceback", k == 2 and "GALAT" in err and "Traceback" not in err)
k, out, err = jalankan(tulis("x.xlsx", b"PK\x03\x04abc", "wb"))
cek("F12 file Excel → GALAT minta simpan CSV", k == 2 and "CSV" in err and "Traceback" not in err)
k, out, err = jalankan("tidak-ada.csv")
cek("F13 file tidak ada → GALAT", k == 2 and "tidak ditemukan" in err)
k, out, err = jalankan("--jenis", "roket", "--penjualan", "1jt")
cek("F14 jenis usaha tak dikenal → GALAT dengan pilihan", k == 2 and "dagang" in err)
k, h = json_run("--kas", "abc", "--penjualan", "10jt", "--laba-bersih", "1jt")
cek("F15 angka tak terbaca → peringatan, bukan galat", k == 0 and any("tidak terbaca" in w
                                                                    for w in h["periode"][0]["peringatan"]))
k, out, err = jalankan(*TOKO)
cek("F16 keluaran teks memuat disclaimer & bagian KUR",
    k == 0 and "Bukan nasihat investasi" in out and "Kesiapan pengajuan KUR" in out and "Rp 33.000.000" in out)

# ---------------------------------------------------------------- kasus G: temuan uji independen v1.0.0 (v1.0.1)
# G1–G3 tren basis sama (uji 03 warung): basis saldo akhir kedua periode.
# 2024: aset 8+2+35+20 = 65 → ROA 14,4/65 = 22,154%; 2025: aset 6,5+4,2+48+18 = 76,7 → 16,8/76,7 = 21,904% (turun)
WARUNG = """Pos;2024;2025
Omzet;Rp 360.000.000;Rp 420.000.000
HPP;306.000.000;361.200.000
Laba bersih;14.400.000;16.800.000
Kas;8.000.000;6.500.000
Piutang;2.000.000;4.200.000
Stok barang;35.000.000;48.000.000
Peralatan;20.000.000;18.000.000
Utang supplier;15.000.000;26.000.000
Utang lain;2.000.000;3.000.000
Utang jangka panjang;0;0
Modal;48.000.000;47.700.000
Bulan;12;12
"""
k, h = json_run(tulis("warung.csv", WARUNG), "--jenis", "warung sembako")
tr = {t["kode"]: t for t in h["tren"]}
cek("G1 tren ROA basis saldo akhir: 22,15% → 21,90% = memburuk",
    dekat(tr["roa"]["nilai"][0], F(1440, 65)) and dekat(tr["roa"]["nilai"][1], F(16800, 767))
    and tr["roa"]["arah"].startswith("memburuk"), tr["roa"])
cek("G2 tren umur stok basis akhir 2025 = 48×365/361,2 = 48,50 hari (memburuk)",
    dekat(tr["hari_persediaan"]["nilai"][1], F(48 * 365 * 10, 3612)) and tr["hari_persediaan"]["arah"].startswith("memburuk"))
cek("G3 tabel utama 2025 tetap rata-rata aset (65+76,7)/2 → 23,71%; basis tren ditulis",
    dekat(r_(h, "roa")["nilai"], F(1680, F(1417, 20)), F(1, 1000)) and "saldo AKHIR" in (h["basis_tren"] or ""))
# G4 hari piutang konveksi: basis akhir 2025 (bukan rata-rata)
KONV = """Pos;Sem1;Sem2
Penjualan;150jt;160jt
Penjualan tempo;100jt;110jt
HPP;105jt;112jt
Laba bersih;12jt;11jt
Kas;5jt;4jt
Piutang;30jt;45jt
Persediaan;40jt;50jt
Aset tetap;60jt;58jt
Utang lancar;35jt;52jt
Utang jangka panjang;20jt;20jt
Modal;80jt;85jt
Bulan;6;6
"""
k, h = json_run(tulis("konv.csv", KONV), "--jenis", "konveksi")
tr = {t["kode"]: t for t in h["tren"]}
cek("G4 tren lama piutang Sem2 = 45×182,5/110 = 74,66 hari (basis akhir), tabel utama rata-rata 62,2",
    dekat(tr["hari_piutang"]["nilai"][1], F(45) * F(3650, 20) / 110)
    and dekat(r_(h, "hari_piutang")["nilai"], F(75, 2) * F(3650, 20) / 110))
# G5–G7 CSV koma tanpa kutip → ditolak jelas, tidak ditebak
k, out, err = jalankan(tulis("koma.csv", "Pos,2025\nKas,1,250,000\nPenjualan,100000000\n"))
cek("G5 'Kas,1,250,000' tanpa kutip → GALAT (bukan kas Rp 1 diam-diam)",
    k == 2 and "pemisah ribuan" in err and "TIDAK ditebak" in err and "Traceback" not in err, err)
k, h = json_run(tulis("koma-kutip.csv", 'Pos,2025\nKas,"1,250,000"\nPenjualan,100000000\nLaba bersih,5000000\n'))
cek("G6 dengan tanda kutip → kas Rp 1.250.000", k == 0 and h["periode"][0]["data"]["kas"] == 1250000)
k, h = json_run(tulis("koma-ekor.csv", "Pos,2025,,\nKas,1250000,,\nLaba bersih,5000000,,\n"))
cek("G7 kolom kosong di ujung (ekspor Excel) tidak dianggap rusak", k == 0 and h["periode"][0]["data"]["kas"] == 1250000)
# G8–G10 data minim
k, h = json_run("--penjualan", "20jt", "--laba-bersih", "2jt", "--bulan", "1")
cek("G8 data minim → status DATA BELUM CUKUP, ringkasan tidak 'pertahankan'",
    h["status_data"] == "DATA BELUM CUKUP" and "DATA BELUM CUKUP" in h["ringkasan_awam"]
    and "pertahankan" not in h["ringkasan_awam"].lower(), h["ringkasan_awam"])
cek("G9 saran pertama 'Lengkapi data' menyebut pos kosong; tidak ada saran 'Pertahankan'",
    h["saran"][0]["rasio"] == "Lengkapi data" and "Modal" in h["saran"][0]["saran"]
    and not any("Pertahankan" in x["saran"] for x in h["saran"]))
kk = h["periode"][-1]["kesiapan_kredit"]
cek("G10 kesiapan KUR 'DATA BELUM CUKUP' + pos kosong di Asumsi",
    kk["kesimpulan"].startswith("DATA BELUM CUKUP") and any("Pos tidak diisi" in a for a in h["periode"][0]["asumsi"]))
# G11–G12 saran kontekstual (uji 04 laundry: stok 1,2 jt dari aset lancar 9,8 jt, utang lancar 23,4 jt)
LAUNDRY_B = ["--jenis", "laundry", "--penjualan", "186jt", "--hpp", "41jt", "--laba-bersih", "19,2jt",
             "--laba-usaha", "26,4jt", "--beban-bunga", "7,2jt", "--kas", "5,5jt", "--piutang", "3,1jt",
             "--persediaan", "1,2jt", "--aset-tetap", "118jt", "--utang-usaha", "2,4jt",
             "--utang-lancar-lain", "21jt", "--utang-jangka-panjang", "64jt", "--modal", "40,4jt", "--bulan", "12"]
k, h = json_run(*LAUNDRY_B)
sr = next(x for x in h["saran"] if x["rasio"].startswith("Rasio cepat"))
cek("G11 laundry stok kecil: saran rasio cepat fokus utang/kas, bukan 'kurangi stok'",
    "stok bukan penyebabnya" in sr["saran"] and "Kurangi belanja stok" not in sr["saran"])
k, h = json_run("--jenis", "dagang", "--penjualan", "300jt", "--hpp", "270jt", "--laba-bersih", "6jt", "--kas", "1jt",
                "--piutang", "1jt", "--persediaan", "30jt", "--aset-tetap", "5jt", "--utang-lancar", "20jt",
                "--modal", "17jt")
sr = next(x for x in h["saran"] if x["rasio"].startswith("Rasio cepat"))
cek("G12 toko stok besar (30 dari 32 jt aset lancar): saran rasio cepat tetap soal stok",
    "tertahan di stok" in sr["saran"])
# G13–G15 temuan ringan
k, h = json_run(path_emkm := tulis("emkm2.json", json.dumps(EMKM)), "--bagian-lancar-utang-bank", "999jt")
cek("G13 bagian lancar > utang bank → peringatan, bukan dipotong diam-diam",
    any("lebih besar dari utang bank" in w for w in h["periode"][0]["peringatan"]))
k, h = json_run(*(TOKO[:-2] + ["--bulan", "1"]))
cek("G14 periode 1 bulan: catatan musiman tidak membuat status SEMENTARA",
    h["status_data"] == "LENGKAP" and any("Periode pendek" in x for x in h["periode"][0]["info"]))
cek("G15 tebak jenis kata utuh: 'jasa fotokopi'→jasa, 'jasa katering'/'toko kue'/'warung kopi'→manufaktur",
    [rasio.tebak_jenis(x) for x in ("jasa fotokopi", "jasa katering", "toko kue", "warung kopi", "warung sembako")]
    == ["jasa", "manufaktur", "manufaktur", "manufaktur", "dagang"])

# ---------------------------------------------------------------- kasus H: temuan uji ulang v1.0.1 (v1.0.2)
# H1 koma ribuan pecah PAS jumlah kolom (tabel 2 periode, tanpa baris Modal) → ditolak, bukan Rp 250 diam-diam
B14 = ("Pos,2024,2025\nPenjualan,100000000,120000000\nLaba bersih,5000000,6000000\nKas,250,000\n"
       "Persediaan,10000000,12000000\nAset tetap,20000000,20000000\nUtang usaha,5000000,6000000\n")
k, out, err = jalankan(tulis("b14.csv", B14))
cek("H1 'Kas,250,000' pada tabel 2 periode → GALAT koma ribuan (tidak terbaca Rp 250)",
    k == 2 and "1–3 digit" in err and "TIDAK ditebak" in err and "Traceback" not in err, err)
k, h = json_run(tulis("b14-ok.csv", B14.replace("Kas,250,000", 'Kas,"250,000","300,000"')))
cek("H2 versi dikutip terbaca Rp 250.000 & Rp 300.000", k == 0 and h["periode"][0]["data"]["kas"] == 250000
    and h["periode"][1]["data"]["kas"] == 300000)
k, h = json_run(tulis("bulan.csv", "Pos,2025\nPenjualan,100000000\nLaba bersih,5000000\nBulan,12\nHari,365\n"))
cek("H3 baris Bulan/Hari (angka kecil yang sah) tidak ikut ditolak", k == 0)
k, h = json_run(tulis("kecil-titikkoma.csv", "Pos;2025\nPenjualan;100.000.000\nLaba bersih;5.000.000\nKas;250\n"))
cek("H4 tabel ';' dengan nilai < Rp 1.000 → catatan 'sangat kecil' & status SEMENTARA",
    k == 0 and any("sangat kecil" in c for c in h["catatan_input"]) and h["status_data"] == "SEMENTARA")
k, h = json_run(tulis("kurang-kolom.csv", "Pos;2024;2025\nPenjualan;100jt;120jt\nHPP;70jt\nLaba bersih;5jt;6jt\n"))
cek("H5 baris dengan kolom kurang diberi catatan 'TIDAK DIISI (bukan nol)'",
    any("hanya berisi 1 dari 2 periode" in c for c in h["catatan_input"]))
# H6–H9 kosong ≠ nol (uji ulang c2): stok, aset tetap, modal tidak disebut → tidak boleh "modal habis"
k, h = json_run("--jenis", "dagang", "--penjualan", "240jt", "--hpp", "200jt", "--laba-bersih", "12jt", "--kas", "5jt",
                "--utang-usaha", "8jt")
cek("H6 pos wajib kosong → status DATA BELUM CUKUP (bukan LENGKAP)", h["status_data"] == "DATA BELUM CUKUP")
cek("H7 modal TIDAK dihitung (bukan −Rp 3.000.000), tidak ada saran 'Modal habis'",
    "modal" not in h["periode"][0]["data"] and not any(x["rasio"].startswith("Modal") for x in h["saran"]))
cek("H8 rasio lancar & ROA tidak dihitung dengan alasan 'tidak diisi (tulis 0 bila memang nol)'",
    r_(h, "rasio_lancar")["nilai"] is None and "tulis 0 bila memang nol" in r_(h, "rasio_lancar")["alasan_tidak_dihitung"]
    and r_(h, "roa")["nilai"] is None)
kk = h["periode"][-1]["kesiapan_kredit"]
cek("H9 KUR: DATA BELUM CUKUP menyebut Persediaan & Aset tetap",
    kk["kesimpulan"].startswith("DATA BELUM CUKUP") and "Persediaan" in kk["kesimpulan"] and "Aset tetap" in kk["kesimpulan"])
k, h = json_run("--jenis", "dagang", "--penjualan", "240jt", "--hpp", "200jt", "--laba-bersih", "12jt", "--kas", "5jt",
                "--persediaan", "0", "--aset-tetap", "0", "--utang-usaha", "8jt")
cek("H10 bila pengguna MENULIS 0 → dihitung: modal = 5 − 8 = −Rp 3.000.000 (modal habis)",
    h["periode"][0]["data"]["modal"] == -3000000 and any(x["rasio"].startswith("Modal") for x in h["saran"]))
k, h = json_run("--jenis", "jasa", "--penjualan", "100jt", "--hpp", "20jt", "--laba-bersih", "15jt", "--kas", "10jt",
                "--piutang", "5jt", "--aset-tetap", "40jt", "--utang-lancar", "8jt", "--modal", "47jt")
cek("H11 usaha jasa tanpa baris persediaan tetap dihitung lengkap (stok bukan pos wajib jasa)",
    dekat(r_(h, "rasio_lancar")["nilai"], F(15, 8)) and h["status_data"] == "LENGKAP")

# ---------------------------------------------------------------- kasus I: uji OpenClaw 2026-10-01 (v1.0.4)
# I1–I5 bahan komisaris: kas 420 jt < utang bank jatuh tempo ≤ 12 bln 900 jt. Rasio kas 420/1.660 = 0,253 (≥ 0,2
# biasanya "baik") → wajib turun ke waspada; kas menutup 420/900 = 46,7% ≈ 47%; kas + piutang = 1.770 ≥ 1.660 → SEDANG.
KOM = ["--jenis", "dagang", "--kas", "420jt", "--piutang", "1,35M", "--persediaan", "980jt", "--aset-lancar", "2,75M",
       "--aset-tetap", "3,2M", "--total-aset", "5,95M", "--utang-usaha", "760jt", "--utang-bank-pendek", "900jt",
       "--utang-lancar", "1,66M", "--utang-jangka-panjang", "1,8M", "--modal", "2,49M", "--penjualan", "9,6M",
       "--hpp", "7,44M", "--laba-usaha", "710jt", "--beban-bunga", "310jt", "--laba-bersih", "312jt", "--bulan", "12"]
k, h = json_run(*KOM)
ak = h["periode"][-1]
cek("I1 rasio kas 0,253 diturunkan ke waspada karena kas < utang bank jatuh tempo",
    dekat(r_(h, "rasio_kas")["nilai"], F(420, 1660)) and r_(h, "rasio_kas")["status"] == "waspada")
cek("I2 cek likuiditas tingkat SEDANG + rincian 'kas menutup 47%'",
    ak["cek_likuiditas"]["tingkat"] == "SEDANG" and any("menutup 47%" in x for x in ak["cek_likuiditas"]["rincian"]))
cek("I3 saran pertama = utang bank jatuh tempo > kas; KUR bukan 'ANGKA CUKUP SEHAT'",
    h["saran"][0]["rasio"].startswith("Utang bank") and not ak["kesiapan_kredit"]["kesimpulan"].startswith("ANGKA"))
k, out, err = jalankan(*KOM)
cek("I4 teks tidak pernah berisi 'tidak ada risiko' sebagai kesimpulan & ada pemeriksaan kas vs utang",
    k == 0 and "Risiko likuiditas jangka pendek SEDANG" in out and "tidak ada risiko gagal" not in out.lower())
cek("I5 skala dari penjualan 9,6 M/tahun = kecil (PP 7/2021: > 2 M s.d. 15 M)", h["skala_usaha"] == "kecil")
# I6 baris tabel "Utang bank jangka pendek" dikenali terpisah & ikut total utang lancar: 760 + 900 + 50 = 1.710 jt
k, h = json_run(tulis("bank.csv", "Pos;2025\nPenjualan;9.600.000.000\nLaba bersih;312.000.000\nKas;420.000.000\n"
                                  "Persediaan;980.000.000\nPiutang;1.350.000.000\nAset tetap;3.200.000.000\n"
                                  "Utang usaha;760.000.000\nUtang bank jangka pendek;900.000.000\n"
                                  "Utang pajak;50.000.000\nModal;2.440.000.000\n"))
cek("I6 tabel: utang bank jangka pendek = pos sendiri, utang lancar = 1.710.000.000",
    k == 0 and h["periode"][0]["data"]["utang_bank_pendek"] == 900000000
    and h["periode"][0]["data"]["utang_lancar"] == 1710000000, h)
# I7 skala menengah (penjualan 20 M): rasio kas 0,25 → waspada (ambang 0,3); cakupan bunga 1,8 → bahaya (ambang 2)
MEN = ["--jenis", "dagang", "--penjualan", "20M", "--hpp", "16M", "--laba-usaha", "900jt", "--beban-bunga", "500jt",
       "--laba-bersih", "300jt", "--kas", "250jt", "--piutang", "800jt", "--persediaan", "900jt", "--aset-tetap", "2M",
       "--utang-usaha", "1M", "--utang-jangka-panjang", "1M", "--modal", "1,95M"]
k, h = json_run(*MEN)
cek("I7 skala menengah: rasio kas 0,25 waspada & cakupan bunga 1,8 bahaya (ambang menengah)",
    h["skala_usaha"] == "menengah" and r_(h, "rasio_kas")["status"] == "waspada"
    and dekat(r_(h, "cakupan_bunga")["nilai"], F(900, 500)) and r_(h, "cakupan_bunga")["status"] == "bahaya", h["skala_usaha"])
# I8 kas ≥ utang lancar → RENDAH, tetap tanpa frasa "tidak ada risiko"
k, h = json_run("--jenis", "jasa", "--penjualan", "100jt", "--hpp", "20jt", "--laba-bersih", "15jt", "--kas", "10jt",
                "--piutang", "5jt", "--aset-tetap", "40jt", "--utang-lancar", "8jt", "--modal", "47jt")
cl = h["periode"][-1]["cek_likuiditas"]
cek("I8 kas 10 jt ≥ utang lancar 8 jt → tingkat RENDAH, bukan 'tidak ada risiko'",
    cl["tingkat"] == "RENDAH" and "tidak ada risiko" not in cl["kalimat"].lower())

shutil.rmtree(TMP, ignore_errors=True)
print("\n%d uji, %d gagal." % (JUMLAH[0], len(GAGAL)))
if GAGAL:
    print("GAGAL:", ", ".join(GAGAL))
    sys.exit(1)
print("SEMUA UJI LULUS")
