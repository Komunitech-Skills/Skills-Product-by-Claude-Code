#!/usr/bin/env python3
"""Uji regresi cicilan.py. Jalankan dari folder skill: python3 tests/uji_regresi.py (Windows: python/py)

Bagian A: nilai pembanding dari dokumentasi/tes numpy-financial (BSD-3-Clause; ditulis ulang tanpa
numpy/pytest, lihat ATTRIBUTION.md). Bagian lain: pembanding dihitung independen dengan float biasa.
"""
import json
import os
import subprocess
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(DIR, "..", "scripts", "cicilan.py")
sys.path.insert(0, os.path.join(DIR, "..", "scripts"))
import cicilan as C  # noqa: E402

GAGAL = []


def cek(nama, kondisi):
    print(("OK    " if kondisi else "GAGAL ") + nama)
    if not kondisi:
        GAGAL.append(nama)


def dekat(a, b, rtol=1e-7, atol=0.0):
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


def irr_float(arus):
    """Bisection float independen: i per periode agar NPV = 0."""
    lo, hi = -0.99, 10.0
    f = lambda i: sum(a / (1 + i) ** t for t, a in enumerate(arus))  # noqa: E731
    for _ in range(300):
        mid = (lo + hi) / 2
        if (f(mid) > 0) == (f(lo) > 0):
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


# ---------------------------------------------------------------- A. numpy-financial
cek("A1 pmt(8%/12, 60, 15000) = -304,145914", dekat(C.pmt(0.08 / 12, 60, 15000), -304.145914, rtol=1e-7))
cek("A2 pmt(7,5%/12, 180, 200000) = -1854,02472", dekat(C.pmt(0.075 / 12, 180, 200000), -1854.0247200054619, rtol=1e-10))
cek("A3 pmt bunga 0 = -pv/n", C.pmt(0, 60, 15000) == -250)
r = C.rate(60, -304.145914, 15000)
cek("A4 rate (bisection) kebalikan A1 = 8%/tahun", dekat(r * 12, 0.08, atol=1e-8))
r = C.rate(180, C.pmt(0.075 / 12, 180, 200000), 200000)
cek("A5 rate (bisection) kebalikan A2 = 7,5%/tahun", dekat(r * 12, 0.075, atol=1e-12))
cek("A6 rate tanpa bunga = 0", abs(float(C.rate(10, -100, 1000))) < 1e-20)

# ---------------------------------------------------------------- B. flat -> bunga efektif
k, h = jalankan("--pokok", "10jt", "--tenor", "12", "--bunga", "0,8%/bulan", "--jenis", "flat")
rg = h["ringkasan"]
cek("B1 flat 0,8%/bln 10jt 12 bln: cicilan Rp913.333, total bunga Rp960.000",
    rg["cicilan_per_bulan"] == 913333 and rg["total_bunga"] == 960000)
cek("B2 flat: selisih pembulatan Rp4 di cicilan terakhir, total pokok tepat", rg["cicilan_terakhir"] == 913337
    and rg["selisih_pembulatan_cicilan_terakhir"] == 4 and sum(x["pokok"] for x in h["jadwal"]) == 10_000_000)
i = irr_float([10_000_000] + [-913333] * 11 + [-913337])
cek("B3 flat 0,8%/bln setara efektif ±17,27%/tahun (independen)",
    dekat(rg["bunga_efektif_setara_tanpa_biaya"]["per_tahun_persen"], i * 1200, atol=1e-6)
    and 17.2 < i * 1200 < 17.4)
cek("B4 peringatan flat menyebut setara efektif", any("setara bunga efektif" in x for x in h["peringatan"]))

# ---------------------------------------------------------------- C. anuitas
k, h = jalankan("--pokok", "200000", "--tenor", "180", "--bunga", "7,5%", "--jenis", "anuitas", "--jadwal-lengkap")
rg = h["ringkasan"]
cek("C1 anuitas cicilan = round(1854,02472) = 1854", rg["cicilan_per_bulan"] == 1854)
cek("C2 anuitas: sisa akhir 0, total pokok tepat", h["jadwal"][-1]["sisa"] == 0 and sum(x["pokok"] for x in h["jadwal"]) == 200000)
cek("C3 anuitas: total bunga = total cicilan - pokok", rg["total_bunga"] == rg["total_cicilan"] - 200000)
cek("C4 anuitas tanpa biaya: bunga efektif setara ~ 7,5%",
    dekat(rg["bunga_efektif_setara_tanpa_biaya"]["per_tahun_persen"], 7.5, atol=0.01))

# ---------------------------------------------------------------- D. bunga 0
k, h = jalankan("--pokok", "6jt", "--tenor", "12", "--bunga", "0")
rg = h["ringkasan"]
cek("D1 bunga 0: cicilan Rp500.000, total bunga 0, efektif 0", rg["cicilan_per_bulan"] == 500000 and rg["total_bunga"] == 0
    and abs(rg["bunga_efektif_setara_tanpa_biaya"]["per_tahun_persen"]) < 1e-9)

# ---------------------------------------------------------------- E. biaya di muka & DP
k, h = jalankan("--harga", "25jt", "--dp", "20%", "--tenor", "36", "--bunga", "0,8%/bulan", "--jenis", "flat", "--admin", "1jt")
rg = h["ringkasan"]
cek("E1 DP 20% dari 25jt -> pokok 20jt", h["input_terbaca"]["pokok_pinjaman"] == 20_000_000 and h["input_terbaca"]["dp"] == 5_000_000)
k2, h2 = jalankan("--harga", "25jt", "--dp", "20%", "--tenor", "36", "--bunga", "0,8%/bulan", "--jenis", "flat", "--admin", "1jt", "--jadwal-lengkap")
arus = [19_000_000] + [-x["cicilan"] for x in h2["jadwal"]]
i = irr_float(arus)
cek("E2 EIR dengan admin 1jt = independen & > tanpa biaya",
    dekat(rg["bunga_efektif_setara_dengan_biaya"]["per_tahun_persen"], i * 1200, atol=1e-6)
    and rg["bunga_efektif_setara_dengan_biaya"]["per_tahun_persen"] > rg["bunga_efektif_setara_tanpa_biaya"]["per_tahun_persen"])
cek("E3 total harga kredit = DP + cicilan + admin; lebih mahal dari tunai",
    rg["total_harga_kredit"] == 5_000_000 + rg["total_cicilan"] + 1_000_000
    and rg["lebih_mahal_dari_tunai"] == rg["total_harga_kredit"] - 25_000_000)
k, h = jalankan("--pokok", "10jt", "--tenor", "12", "--bunga", "12", "--jenis", "efektif", "--admin", "500rb", "--cara-biaya", "masuk-pinjaman")
cek("E4 biaya masuk pinjaman: pokok dicicil 10,5jt, uang diterima 10jt",
    h["input_terbaca"]["pokok_yang_dicicil"] == 10_500_000 and h["ringkasan"]["uang_diterima_bersih"] == 10_000_000)

# ---------------------------------------------------------------- F. hitung balik dari cicilan (RATE)
k, h = jalankan("--pokok", "30jt", "--tenor", "24", "--cicilan", "1,5jt")
rg = h["ringkasan"]
i = irr_float([30_000_000] + [-1_500_000] * 24)
cek("F1 cicilan 1,5jt x 24 utk 30jt: bunga efektif independen", dekat(rg["bunga_tahunan_tertulis_persen"], i * 1200, atol=1e-6))
cek("F2 flat setara = 6jt/(30jt*24) = 0,8333%/bln",
    dekat(h["perbandingan"]["bunga_flat_setara_dari_cicilan_ini"]["per_bulan_persen"], 0.833333, atol=1e-5))

# ---------------------------------------------------------------- G. bunga bertahap (KPR)
k, h = jalankan("--pokok", "450jt", "--tenor", "15th", "--bunga-tahap", "5%x36;11%", "--jadwal-lengkap")
j = h["jadwal"]
c1 = round(-float(C.pmt(0.05 / 12, 180, 450_000_000)))
sisa36 = j[35]["sisa"]
c2 = round(-float(C.pmt(0.11 / 12, 144, sisa36)))
cek("G1 KPR tahap: cicilan 1-36 & 37+ dihitung ulang dari sisa", j[0]["cicilan"] == c1 and j[36]["cicilan"] == c2 and c2 > c1)
cek("G2 KPR tahap: lunas tepat", j[-1]["sisa"] == 0 and sum(x["pokok"] for x in j) == 450_000_000)

# ---------------------------------------------------------------- H. pinjaman harian
k, h = jalankan("--pokok", "2jt", "--tenor", "14hari", "--bunga", "0,3%/hari", "--admin", "100rb", "--cara-biaya", "potong")
rg = h["ringkasan"]
cek("H1 pinjol 2jt 14 hari 0,3%/hari: bunga 84rb, kembali 2.084.000, diterima 1,9jt",
    rg["bunga_total"] == 84000 and rg["total_kembali"] == 2_084_000 and rg["uang_diterima_bersih"] == 1_900_000)
cek("H2 biaya per hari = 184rb/1,9jt/14", dekat(rg["biaya_total_per_hari_persen"], 184000 / 1_900_000 / 14 * 100, atol=1e-6))
cek("H3 peringatan batas OJK + saran cek aturan terbaru", any("cek aturan OJK terbaru" in x for x in h["peringatan"]))
k, h = jalankan("--pokok", "1jt", "--tenor", "30hari", "--bunga", "0,05%/hari")
cek("H4 di bawah batas tercatat: tidak ada peringatan batas", not any("batas pinjaman daring" in x for x in h["peringatan"]))

# ---------------------------------------------------------------- I. kemampuan bayar & denda
k, h = jalankan("--pokok", "20jt", "--tenor", "24", "--bunga", "12", "--penghasilan", "6jt", "--cicilan-lain", "500rb")
kb = h["kemampuan_bayar"]
cek("I1 cicilan maks aman 30% = 1,3jt; 35% = 1,6jt", kb["cicilan_maksimal_aman"] == 1_300_000 and kb["cicilan_maksimal_batas_atas"] == 1_600_000)
pv = 1_300_000 * (1 - (1 + 0.01) ** -24) / 0.01
cek("I2 pinjaman maks aman = PV anuitas (independen)", abs(kb["pinjaman_maksimal_aman_dengan_bunga_tenor_ini"] - pv) <= 1)
cek("I3 status AMAN bila rasio <= 30%", kb["status"] == "AMAN")
k, h = jalankan("--penghasilan", "8jt", "--cicilan-lain", "1jt")
cek("I4 hanya penghasilan: cicilan maks 1,4jt", k == 0 and h["kemampuan_bayar"]["cicilan_maksimal_aman"] == 1_400_000)
k, h = jalankan("--pokok", "10jt", "--tenor", "12", "--bunga", "12", "--denda", "0,1%/hari", "--telat", "10")
cek("I5 denda 0,1%/hari x cicilan x 10 hari", h["denda_ilustrasi"]["denda"] == round(h["ringkasan"]["cicilan_per_bulan"] * 0.001 * 10))
k, h = jalankan("--pokok", "20jt", "--tenor", "24", "--bandingkan-bunga", "10;15;20")
cek("I6 ilustrasi beberapa bunga (bunga belum diketahui)", k == 0 and [x["cicilan"] for x in h["bandingkan_bunga"]]
    == [round(-float(C.pmt(t / 1200, 24, 20_000_000))) for t in (10, 15, 20)])

k, h = jalankan("--harga", "8jt", "--tenor", "12", "--ilustrasi", "hp")
bb = h["bandingkan_bunga"]
cek("I7 ilustrasi HP: flat 1,5/2/3%/bln -> Rp786.667/826.667/906.667, efektif 30-62%",
    k == 0 and [x["cicilan"] for x in bb] == [786667, 826667, 906667] and all(x["jenis"] == "flat" for x in bb)
    and 30 < bb[0]["bunga_efektif_per_tahun_persen"] < bb[-1]["bunga_efektif_per_tahun_persen"] < 62)
k, h = jalankan("--pokok", "450jt", "--tenor", "15th", "--bunga-tahap", "5%x36;11%")
jt = h["jadwal_per_tahun"]
cek("I8 KPR: catatan pergantian hanya di tahun 4, mulai bulan ke-37", jt[3]["catatan"] and "bulan ke-37" in jt[3]["catatan"]
    and "Rp4.823.129" in jt[3]["catatan"] and all(r["catatan"] is None for i, r in enumerate(jt) if i != 3))
cek("I9 rujukan pinjol SEOJK 19/SEOJK.06/2025 Romawi XIV (berlaku 31 Juli 2025; SEOJK 2023 dicabut), tanpa angka lama",
    "19/SEOJK.06/2025" in C.RUJUKAN_PINJOL and "Romawi XIV" in C.RUJUKAN_PINJOL and "31 Juli 2025" in C.RUJUKAN_PINJOL
    and "dicabut" in C.RUJUKAN_PINJOL and "6 bulan" in C.RUJUKAN_PINJOL and "Rp50 juta" in C.RUJUKAN_PINJOL
    and "1 Januari 2026" not in C.RUJUKAN_PINJOL and "0,067" not in C.RUJUKAN_PINJOL
    and "19/SEOJK.06/2025" in C.RUJUKAN_PINJOL_SINGKAT and not hasattr(C, "TENOR_MAKS_BATAS_KONSUMTIF_HARI"))
B = C.BATAS_PINJOL_HARIAN
cek("I10 tabel batas SEOJK 2025: konsumtif 0,3/0,2; produktif <= Rp50 jt 0,275/0,1; > Rp50 jt 0,1; 6 bulan = 180 hari",
    B["konsumtif"] == {"sd_6_bulan": C.D("0.3"), "di_atas_6_bulan": C.D("0.2")}
    and B["produktif_sd_50jt"] == {"sd_6_bulan": C.D("0.275"), "di_atas_6_bulan": C.D("0.1")}
    and B["produktif_di_atas_50jt"] == {"sd_6_bulan": C.D("0.1"), "di_atas_6_bulan": C.D("0.1")}
    and C.TENOR_6_BULAN_HARI == 180 and C.NILAI_PRODUKTIF_KECIL == 50_000_000)
cek("I11 pemilih batas: tenor 14/180 hari -> 0,3; 181/400 hari -> 0,2 (konsumtif); produktif 50 jt 180/181 hari -> "
    "0,275/0,1; produktif 50.000.001 tenor 30 hari -> 0,1",
    [C.batas_pinjol("konsumtif", C.D(2_000_000), h)[0] for h in (14, 180, 181, 400)]
    == [C.D("0.3"), C.D("0.3"), C.D("0.2"), C.D("0.2")]
    and [C.batas_pinjol("produktif", C.D(50_000_000), h)[0] for h in (180, 181)] == [C.D("0.275"), C.D("0.1")]
    and C.batas_pinjol("produktif", C.D(50_000_001), 30)[0] == C.D("0.1"))


def ada_batas(h):
    return any("batas pinjaman daring" in x for x in h["peringatan"])


k1, h1 = jalankan("--pokok", "2jt", "--tenor", "14hari", "--bunga", "0,3%/hari")
k2, h2 = jalankan("--pokok", "2jt", "--tenor", "90hari", "--bunga", "0,25%/hari")
cek("I12 tidak ada peringatan palsu: konsumtif 14 hari 0,3%/hari (tepat di batas) & 90 hari 0,25%/hari",
    k1 == 0 and k2 == 0 and not ada_batas(h1) and not ada_batas(h2)
    and dekat(h1["ringkasan"]["manfaat_ekonomi_per_hari_persen"], 0.3, atol=1e-9)
    and h1["ringkasan"]["batas_tercatat_per_hari_persen"] == 0.3)
k, h = jalankan("--pokok", "2jt", "--tenor", "200hari", "--bunga", "0,25%/hari")
cek("I13 konsumtif 200 hari (> 6 bulan) 0,25%/hari: di atas 0,2%, sebut tenor di atas 6 bulan + SEOJK 2025 + cek OJK",
    k == 0 and h["ringkasan"]["batas_tercatat_per_hari_persen"] == 0.2
    and any("batas pinjaman daring konsumtif, tenor di atas 6 bulan" in x and "19/SEOJK.06/2025" in x
            and "cek aturan OJK terbaru" in x.replace("Cek", "cek") for x in h["peringatan"]))
ka, ha = jalankan("--pokok", "30jt", "--tenor", "30hari", "--bunga", "0,28%/hari", "--jenis-pinjol", "produktif")
kb_, hb = jalankan("--pokok", "30jt", "--tenor", "30hari", "--bunga", "0,2%/hari", "--jenis-pinjol", "produktif")
kc, hc = jalankan("--pokok", "60jt", "--tenor", "30hari", "--bunga", "0,2%/hari", "--jenis-pinjol", "produktif")
cek("I14 produktif: 30 jt 0,28% > 0,275% (peringatan); 30 jt 0,2% (aman); 60 jt 0,2% > 0,1% (peringatan)",
    ka == kb_ == kc == 0 and ada_batas(ha) and not ada_batas(hb) and ada_batas(hc)
    and hc["ringkasan"]["batas_tercatat_per_hari_persen"] == 0.1
    and "di atas Rp50 juta" in hc["ringkasan"]["golongan_batas"])
k, h = jalankan("--pokok", "2jt", "--tenor", "10hari", "--bunga", "0,25%/hari", "--admin", "9800", "--cara-biaya", "potong")
rg = h["ringkasan"]
cek("I15 pembanding batas = (bunga + biaya) / nilai pinjaman di perjanjian / hari (59.800/2 jt/10 = 0,299%), bukan dari uang diterima",
    k == 0 and dekat(rg["manfaat_ekonomi_per_hari_persen"], 59_800 / 2_000_000 / 10 * 100, atol=1e-9)
    and rg["biaya_total_per_hari_persen"] > 0.3 and not ada_batas(h))
k, h = jalankan("--pokok", "2jt", "--tenor", "183hari", "--bunga", "0,1%/hari")
cek("I16 tenor 183 hari: asumsi 6 bulan = 180 hari + catatan batas tenor sampai 6 bulan (0,300%/hari)",
    k == 0 and any("6 bulan = 180 hari" in x and "0,300%/hari" in x for x in h["asumsi"])
    and any("6 bulan dihitung 180 hari" in x for x in h["asumsi"]))

k1, h1 = jalankan("--pokok", "2jt", "--tenor", "14hari", "--bunga", "0,3%/hari")
k2, h2 = jalankan("--pokok", "2jt", "--tenor", "14hari", "--bunga", "0,3%/hari", "--jenis-pinjol", "produktif")
cek("I17 jenis pinjol tidak disebut: konsumtif dicatat sebagai asumsi; produktif eksplisit: tanpa asumsi itu, batas 0,275%",
    k1 == k2 == 0 and any("dianggap konsumtif" in x for x in h1["asumsi"])
    and not any("dianggap konsumtif" in x for x in h2["asumsi"]) and h2["ringkasan"]["batas_tercatat_per_hari_persen"] == 0.275)

# ---------------------------------------------------------------- J. input rusak
for nama, arg in (("tenor 0", ["--pokok", "10jt", "--tenor", "0", "--bunga", "10"]),
                  ("pokok huruf", ["--pokok", "abc", "--tenor", "12", "--bunga", "10"]),
                  ("DP >= harga", ["--harga", "10jt", "--dp", "10jt", "--tenor", "12", "--bunga", "10"]),
                  ("tanpa bunga & cicilan", ["--pokok", "10jt", "--tenor", "12"]),
                  ("cicilan x tenor < pokok", ["--pokok", "10jt", "--tenor", "12", "--cicilan", "500rb"]),
                  ("bunga huruf", ["--pokok", "10jt", "--tenor", "12", "--bunga", "xx"]),
                  ("angka ambigu", ["--pokok", "10.000,000", "--tenor", "12", "--bunga", "10"]),
                  ("pokok negatif", ["--pokok=-5jt", "--tenor", "12", "--bunga", "10"]),
                  ("tahap melebihi tenor", ["--pokok", "100jt", "--tenor", "24", "--bunga-tahap", "5%x36;11%"]),
                  ("tanpa tenor", ["--pokok", "10jt", "--bunga", "10"])):
    k, h = jalankan(*arg)
    cek(f"J {nama}: kode 2 + error & saran", k == 2 and "error" in h and "saran" in h)

# ---------------------------------------------------------------- K. pembacaan angka & teks
cek("K1 baca '1,5jt', 'Rp25.000.000', '750rb'", C.parse_rupiah("1,5jt", "x") == 1_500_000
    and C.parse_rupiah("Rp25.000.000", "x") == 25_000_000 and C.parse_rupiah("750rb", "x") == 750_000)
cek("K2 baca tenor '3th' = 36 bulan, '2minggu' = 14 hari", C.parse_tenor("3th") == (36, "bulan") and C.parse_tenor("2minggu") == (14, "hari"))
k, h = jalankan("--pokok", "10jt", "--tenor", "12", "--bunga", "0,8%/bulan", "--jenis", "flat", "--format", "teks")
cek("K3 teks: format Rp tanpa spasi + disclaimer", "Rp913.333" in h["teks"] and "bukan penawaran atau nasihat keuangan" in h["teks"])

print()
print(f"{'SEMUA LULUS' if not GAGAL else str(len(GAGAL)) + ' GAGAL'}")
sys.exit(1 if GAGAL else 0)
