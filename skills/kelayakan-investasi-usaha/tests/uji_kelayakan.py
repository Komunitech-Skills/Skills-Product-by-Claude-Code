#!/usr/bin/env python3
"""Uji regresi kelayakan.py. Jalankan dari folder skill: python3 tests/uji_kelayakan.py

Kasus A berasal dari contoh/tes numpy-financial (BSD-3-Clause, ditulis ulang tanpa numpy;
lihat ATTRIBUTION.md). Kasus lain dihitung manual secara independen (float biasa) di file ini.
"""
import json
import os
import subprocess
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(DIR, "..", "scripts", "kelayakan.py")
sys.path.insert(0, os.path.join(DIR, "..", "scripts"))
import kelayakan as K  # noqa: E402

GAGAL = []


def cek(nama, kondisi):
    print(("OK    " if kondisi else "GAGAL ") + nama)
    if not kondisi:
        GAGAL.append(nama)


def dekat(a, b, rtol=1e-6, atol=0.0):
    return a is not None and abs(float(a) - b) <= max(atol, rtol * abs(b))


def jalankan(*arg):
    p = subprocess.run([sys.executable, SCRIPT] + list(arg), capture_output=True, text=True)
    if p.returncode == 0:
        try:
            return 0, json.loads(p.stdout)
        except ValueError:
            return 0, {"teks": p.stdout}
    try:
        return p.returncode, json.loads(p.stderr)
    except ValueError:
        return p.returncode, {"error": p.stderr}


def npv_manual(r, vals):
    return sum(v / (1 + r) ** t for t, v in enumerate(vals))


# ---------------------------------------------------------------- A. kasus numpy-financial
cek("A1 npv 5% [-15000,1500,2500,3500,4500,6000] ~ 122,89", dekat(K.npv(0.05, [-15000, 1500, 2500, 3500, 4500, 6000]), 122.89, rtol=1e-2))
cek("A2 npv 8% [-40000,5000,8000,12000,30000] = 3065,22267", dekat(K.npv(0.08, [-40000, 5000, 8000, 12000, 30000]), 3065.22267, atol=1e-5))
cek("A3 npv 0% = jumlah biasa", K.npv(0, [-4000, 500, 800]) == -2700)
cek("A4 npv 10% [-5000,600,900] = -3710,74", dekat(K.npv(0.10, [-5000, 600, 900]), -3710.74, atol=0.005))
cek("A5 pmt(8%/12, 60, 15000) = -304,145914", dekat(K.pmt(0.08 / 12, 60, 15000), -304.145914, rtol=1e-7))
cek("A6 pmt(7,5%/12, 180, 200000) = -1854,02472", dekat(K.pmt(0.075 / 12, 180, 200000), -1854.0247200054619, rtol=1e-10))
cek("A7 pmt rate 0 = -250", K.pmt(0, 60, 15000) == -250)
for vals, harap in (([-150000, 15000, 25000, 35000, 45000, 60000], 0.0524),
                    ([-100, 0, 0, 74], -0.0955),
                    ([-100, 39, 59, 55, 20], 0.28095),
                    ([-100, 100, 0, -7], -0.0833),
                    ([-100, 100, 0, 7], 0.06206),
                    ([-5, 10.5, 1, -8, 1], 0.0886),
                    ([-5, 10.5, 1, -8, 1, 0, 0, 0], 0.0886),
                    ([-1678.87, 771.96, 1814.05, 3520.30, 3552.95, 3584.99, 4789.91, -1], 1.00426)):
    cek(f"A8 irr {vals} ~ {harap}", dekat(K.irr(vals), harap, rtol=1e-2))
gh39 = [-217500.0, -217500.0, 108466.80462450592, 101129.96439328062, 93793.12416205535,
        86456.28393083003, 79119.44369960476, 71782.60346837944, 64445.76323715414, 57108.92300592884,
        49772.08277470355, 42435.24254347826, 35098.40231225296, 27761.56208102766, 20424.721849802358,
        13087.88161857707, 5751.041387351768, -1585.7988438735192, -8922.639075098821, -16259.479306324123,
        -23596.31953754941, -30933.159768774713, -38270.0, -45606.8402312253, -52943.680462450604,
        -60280.520693675906, -67617.36092490121]
cek("A9 irr gh-39 (arus kas berganti tanda) = 12%", dekat(K.irr(gh39), 0.12, rtol=1e-6))
cf = [-40000, 5000, 8000, 12000, 30000]
cek("A10 NPV(IRR) = 0", abs(float(K.npv(K.irr(cf), cf))) < 1e-6)
cek("A11 IRR tidak ada bila semua arus kas positif", K.irr([1, 2, 3]) is None and K.irr([40000, 5000, 8000, 12000, 30000]) is None)
cek("A12 IRR tidak ada bila semua negatif", K.irr([-1, -2, -3]) is None)
cek("A13 IRR tidak ada bila semua nol", K.irr([0, 0, 0]) is None)
try:
    K.npv(-1, [1, 2])
    ditolak = False
except ValueError:
    ditolak = True
cek("A14 npv rate -100% ditolak", ditolak)

# ---------------------------------------------------------------- B. payback
cek("B1 payback 100 / 40;40;40 = 2,5 tahun", K.payback([40, 40, 40], 100) == 2.5)
cek("B2 payback tidak tercapai", K.payback([10, 10], 100) is None)
cek("B3 payback tepat di akhir tahun 2", K.payback([50, 50, 50], 100) == 2)
cek("B4 teks 1,5 tahun", K.teks_tahun(1.5) == "1 tahun 6 bulan")
cek("B5 teks 0,97 tahun dibulatkan 1 tahun", K.teks_tahun(0.97) == "1 tahun")
cek("B6 arus negatif di tengah", dekat(K.payback([60, -20, 70], 100), 2 + 60 / 70, rtol=1e-12))

# ---------------------------------------------------------------- C. contoh 01 mesin kopi, verifikasi manual
k, h = jalankan("--investasi", "45jt", "--omzet", "6jt/bulan", "--hpp-persen", "40", "--biaya", "1,2jt/bulan",
                "--tahun", "5", "--nilai-residu", "5jt", "--pajak-persen", "0,5")
omzet, var, tetap = 72_000_000, 28_800_000, 14_400_000
pajak = 360_000  # 0,5% x 72 jt
arus = omzet - var - tetap - pajak  # 28.440.000
vals = [-45_000_000] + [arus] * 4 + [arus + 5_000_000]
cek("C1 kode 0 & arus kas tahun 1 = 28.440.000", k == 0 and h["tabel_arus_kas"][0]["arus_kas_bersih"] == arus)
cek("C2 penyusutan (45jt-5jt)/5 = 8jt", h["hasil"]["penyusutan_per_tahun"] == 8_000_000)
cek("C3 nilai sisa garis lurus = residu 5jt", h["hasil"]["nilai_sisa"] == 5_000_000)
cek("C4 NPV = manual", h["hasil"]["npv"] == round(npv_manual(0.12, vals)))
cek("C5 IRR manual (NPV di IRR ~ 0)", abs(npv_manual(h["hasil"]["irr_persen"] / 100, vals)) < 45_000_000 * 1e-4)
cek("C6 payback = 45/28,44", h["hasil"]["payback_tahun"] == round(45_000_000 / arus, 2))
pv = [arus / 1.12 ** t for t in range(1, 6)]
sisa, t = 45_000_000, 0
while sisa > pv[t]:
    sisa -= pv[t]
    t += 1
cek("C7 payback terdiskonto manual", h["hasil"]["payback_diskonto_tahun"] == round(t + sisa / pv[t], 2))
cek("C8 PI = PV masuk / investasi", h["hasil"]["pi"] == round(sum(v / 1.12 ** i for i, v in enumerate(vals) if i) / 45e6, 2))
cek("C9 BEP akuntansi = (14,4jt+8jt)/(1-0,4-0,005)", h["hasil"]["bep_akuntansi_omzet_per_tahun"] == round(22_400_000 / 0.595))
eac = (45e6 - 5e6 / 1.12 ** 5) * 0.12 / (1 - 1.12 ** -5)
cek("C10 BEP ekonomi ~ (biaya tetap + biaya modal setara)/marjin", abs(h["hasil"]["bep_ekonomi_omzet_per_tahun"] - (14.4e6 + eac) / 0.595) < 10)
cek("C11 status LAYAK", h["kesimpulan"]["status"] == "LAYAK")
s10 = [s for s in h["sensitivitas"] if s["skenario"] == "Omzet -10%"][0]
arus10 = 64_800_000 - 25_920_000 - 14_400_000 - 324_000
cek("C12 sensitivitas omzet -10% = manual", s10["npv"] == round(npv_manual(0.12, [-45e6] + [arus10] * 4 + [arus10 + 5e6])))
sb = [s for s in h["sensitivitas"] if s["skenario"] == "Biaya +10%"][0]
arusb = 72_000_000 - 31_680_000 - 15_840_000 - 360_000
cek("C13 sensitivitas biaya +10% = manual", sb["npv"] == round(npv_manual(0.12, [-45e6] + [arusb] * 4 + [arusb + 5e6])))
f = 1 - h["hasil"]["batas_penurunan_persen"] / 100
aruf = 72e6 * f * 0.595 - 14.4e6
cek("C14 batas penurunan omzet membuat NPV ~ 0", abs(npv_manual(0.12, [-45e6] + [aruf] * 4 + [aruf + 5e6])) < 0.002 * 45e6)
cek("C15 ringkasan berlabel UNTUK AGENT SAJA", h["ringkasan_untuk_agent"].startswith("[UNTUK AGENT SAJA"))
cek("C16 disclaimer ada", "Bukan nasihat keuangan" in h["disclaimer"])

# ---------------------------------------------------------------- D. mode arus kas, pajak laba, status
k, h = jalankan("--investasi", "100jt", "--arus-kas", "30jt;40jt;50jt", "--diskonto", "10")
vals = [-100e6, 30e6, 40e6, 50e6]
cek("D1 mode arus: NPV manual", k == 0 and h["hasil"]["npv"] == round(npv_manual(0.10, vals)))
cek("D2 mode arus: IRR = 8,9%", dekat(h["hasil"]["irr_persen"], 8.9, atol=0.01))
cek("D3 NPV negatif -> TIDAK LAYAK", h["kesimpulan"]["status"] == "TIDAK LAYAK")
cek("D4 kenaikan yang diperlukan dihitung", h["hasil"]["kenaikan_diperlukan_persen"] is not None)
k, h = jalankan("--investasi", "180jt", "--arus-kas", "45jt", "--tahun", "5", "--umur-ekonomis", "8",
                "--pajak-persen", "22", "--dasar-pajak", "laba")
dep = 22_500_000
pj = int(0.22 * (45e6 - dep))
cek("D5 pajak laba = 22% x (arus - penyusutan), dibulatkan ke bawah", h["tabel_arus_kas"][0]["pajak"] == pj)
cek("D6 nilai sisa garis lurus 180jt x 3/8 = 67,5jt", h["hasil"]["nilai_sisa"] == 67_500_000)
cek("D7 masa proyek dari --tahun", h["input"]["masa_proyek_tahun"] == 5 and len(h["tabel_arus_kas"]) == 5)
cek("D8 sensitivitas mode arus tanpa skenario biaya", [s["jenis"] for s in h["sensitivitas"]] == ["arus", "arus"])
k, h = jalankan("--investasi", "50jt", "--arus-kas=-5jt;-5jt", "--diskonto", "10")
cek("D9 semua arus kas negatif: IRR tidak ada, TIDAK LAYAK", k == 0 and h["hasil"]["irr_persen"] is None and h["kesimpulan"]["status"] == "TIDAK LAYAK")
k, h = jalankan("--investasi", "250jt", "--omzet", "380jt;470jt;500jt;520jt;540jt", "--hpp-persen", "45",
                "--biaya", "14,5jt/bulan", "--kenaikan-biaya", "5", "--nilai-sisa", "40jt", "--pajak-persen", "0,5")
cek("D10 cabang: KURANG LAYAK (rapuh di omzet -10%)", h["kesimpulan"]["status"] == "KURANG LAYAK")
cek("D11 biaya tetap naik 5%/tahun", h["tabel_arus_kas"][1]["biaya_tetap"] == round(174e6 * 1.05))
k, h = jalankan("--investasi", "100jt", "--arus-kas", "10jt", "--tahun", "5", "--nilai-sisa", "100jt", "--diskonto", "5")
cek("D12 NPV positif hanya karena nilai sisa -> bukan LAYAK", h["hasil"]["npv"] > 0 and h["kesimpulan"]["status"] == "KURANG LAYAK")
k, h = jalankan("--investasi", "10jt", "--arus-kas", "4jt", "--tahun", "3", "--diskonto", "0")
cek("D13 diskonto 0: NPV = jumlah biasa", h["hasil"]["npv"] == 2_000_000)

# ---------------------------------------------------------------- E. format angka
for teks, harap in (("Rp 45.000.000", 45_000_000), ("45jt", 45_000_000), ("45 juta", 45_000_000),
                    ("1,5jt", 1_500_000), ("2.5jt", 2_500_000), ("150rb", 150_000), ("1,2M", 1_200_000_000),
                    ("45000000", 45_000_000), ("45,000,000", 45_000_000), ("(5jt)", -5_000_000),
                    ("minus 5jt", -5_000_000), ("Rp45.000.000,00", 45_000_000)):
    cek(f"E1 '{teks}' -> {harap}", K.parse_rupiah(teks, "x")[0] == harap)
cek("E2 '/bulan' terdeteksi", K.parse_rupiah("9jt/bulan", "x") == (9_000_000, "bulan"))
cek("E3 'per bulan' terdeteksi", K.parse_rupiah("9 jt per bulan", "x")[1] == "bulan")
cek("E4 daftar koma bersufiks", [int(x) for x in K.daftar_rupiah("15jt, 18jt, 20jt", "x")[0]] == [15e6, 18e6, 20e6])
k, h = jalankan("--investasi", "45jt", "--arus-kas", "1jt/bulan", "--tahun", "2", "--diskonto", "12%")
cek("E5 arus kas per bulan dikali 12", h["tabel_arus_kas"][0]["arus_kas_bersih"] == 12_000_000)

# ---------------------------------------------------------------- F. data rusak -> kode 2 + pesan
for nama, arg in (("investasi kosong", ["--arus-kas", "10jt"]),
                  ("investasi 0", ["--investasi", "0", "--arus-kas", "10jt"]),
                  ("investasi negatif", ["--investasi", "-5jt", "--arus-kas", "10jt"]),
                  ("arus kas kosong", ["--investasi", "10jt"]),
                  ("dua mode", ["--investasi", "10jt", "--arus-kas", "5jt", "--omzet", "9jt"]),
                  ("angka sampah", ["--investasi", "sepuluh juta", "--arus-kas", "5jt"]),
                  ("koma ambigu", ["--investasi", "45,000", "--arus-kas", "5jt"]),
                  ("tahun 0", ["--investasi", "10jt", "--arus-kas", "5jt", "--tahun", "0"]),
                  ("tahun 31", ["--investasi", "10jt", "--arus-kas", "5jt", "--tahun", "31"]),
                  ("panjang daftar beda", ["--investasi", "10jt", "--arus-kas", "5jt;6jt", "--tahun", "3"]),
                  ("diskonto 150", ["--investasi", "10jt", "--arus-kas", "5jt", "--diskonto", "150"]),
                  ("pajak 80", ["--investasi", "10jt", "--arus-kas", "5jt", "--pajak-persen", "80"]),
                  ("pajak omzet di mode arus", ["--investasi", "10jt", "--arus-kas", "5jt", "--pajak-persen", "0,5"]),
                  ("omzet negatif", ["--investasi", "10jt", "--omzet", "-5jt"]),
                  ("hpp 100%", ["--investasi", "10jt", "--omzet", "50jt", "--hpp-persen", "100"]),
                  ("nilai sisa negatif", ["--investasi", "10jt", "--arus-kas", "5jt", "--nilai-sisa", "-1jt"]),
                  ("residu > investasi", ["--investasi", "10jt", "--arus-kas", "5jt", "--nilai-residu", "20jt"]),
                  ("daftar dipisah spasi", ["--investasi", "10jt", "--arus-kas", "5000000 6000000"]),
                  ("sensitivitas rusak", ["--investasi", "10jt", "--arus-kas", "5jt", "--sensitivitas", "turun banyak"])):
    k, h = jalankan(*arg)
    cek(f"F {nama}: kode 2 + pesan", k == 2 and h.get("error"))

# ---------------------------------------------------------------- G. lain-lain
k, h = jalankan("--investasi", "45jt", "--omzet", "6jt/bulan", "--hpp-persen", "40", "--biaya", "1,2jt/bulan", "--format", "teks")
cek("G1 format teks berlabel untuk agent", k == 0 and h["teks"].startswith("[UNTUK AGENT SAJA"))
k, h = jalankan("--investasi", "45jt", "--omzet", "72jt", "--biaya", "30jt")
cek("G2 tanpa --tahun: default 5 tahun + asumsi", h["input"]["masa_proyek_tahun"] == 5 and any("5 tahun" in s for s in h["asumsi"]))
cek("G3 tanpa diskonto: default 12% + penjelasan", h["input"]["diskonto_persen"] == 12 and any("KUR" in s for s in h["asumsi"]))
cek("G4 semua biaya dianggap tetap disebut", any("dianggap tetap" in s for s in h["asumsi"]))
k, h = jalankan("--investasi", "45jt", "--omzet", "72jt", "--biaya-variabel", "28,8jt", "--biaya", "14,4jt")
cek("G5 biaya variabel rupiah -> 40%", h["input"]["biaya_variabel_persen_omzet"] == 40.0)
k, h = jalankan("--investasi", "45jt", "--arus-kas", "20jt", "--tahun", "8", "--umur-ekonomis", "5")
cek("G6 masa > umur ekonomis: peringatan", any("umur ekonomis" in s for s in h["peringatan"]))
cek("G7 penyusutan berhenti setelah umur ekonomis", h["tabel_arus_kas"][5]["penyusutan"] == 0)

# ---------------------------------------------------------------- H. cari minimal (input tidak lengkap)
k, h = jalankan("--investasi", "85jt", "--cari-minimal")
crf = 0.12 / (1 - 1.12 ** -5)
cek("H1 arus kas minimal layak = 85jt x CRF(12%, 5)", k == 0 and h["hasil"]["arus_kas_minimal_layak_per_tahun"] == round(85e6 * crf))
cek("H2 minimal balik modal = 85jt/5/12", h["hasil"]["arus_kas_minimal_balik_modal_per_bulan"] == round(85e6 / 60))
k2, h2 = jalankan("--investasi", "85jt", "--arus-kas", str(h["hasil"]["arus_kas_minimal_layak_per_tahun"]), "--tahun", "5")
cek("H3 memakai arus kas minimal -> NPV ~ 0", k2 == 0 and abs(h2["hasil"]["npv"]) <= 3)
k, h = jalankan("--cari-minimal")
cek("H4 cari minimal tanpa investasi -> kode 2", k == 2)

k, h = jalankan("--investasi", "1jt", "--arus-kas", "50jt", "--tahun", "3")
cek("H5 IRR sangat besar: LAYAK + catatan > 1000%", k == 0 and h["kesimpulan"]["status"] == "LAYAK" and "irr_catatan" in h["hasil"])

print()
print(f"{'SEMUA LULUS' if not GAGAL else str(len(GAGAL)) + ' GAGAL'}")
sys.exit(1 if GAGAL else 0)
