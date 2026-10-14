#!/usr/bin/env python3
"""Uji regresi rencana_restok.py. Jalankan dari folder skill: python3 tests/uji_regresi.py (Windows: python / py).

Angka pembanding dihitung ulang secara independen di file ini (float, math, statistics),
bukan disalin dari keluaran script.
"""
import json
import math
import os
import statistics
import subprocess
import sys
import tempfile
import zipfile
from datetime import date, timedelta

DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(DIR, "..", "scripts", "rencana_restok.py")
TMP = tempfile.mkdtemp()
GAGAL = []
Z95 = 1.65


def cek(nama, kondisi):
    print(("OK    " if kondisi else "GAGAL ") + nama)
    if not kondisi:
        GAGAL.append(nama)


def tulis(nama, isi, biner=False):
    p = os.path.join(TMP, nama)
    with open(p, "wb" if biner else "w", encoding=None if biner else "utf-8") as f:
        f.write(isi)
    return p


def jalan(*arg):
    p = subprocess.run([sys.executable, SCRIPT] + list(arg), capture_output=True, text=True, encoding="utf-8")
    if p.returncode == 0:
        try:
            return 0, json.loads(p.stdout)
        except ValueError:
            return 0, {"teks": p.stdout}
    try:
        return p.returncode, json.loads(p.stderr)
    except ValueError:
        return p.returncode, {"error": p.stderr}


def brg(h, kunci):
    return next(x for x in h["barang"] if x["sku"] == kunci or x["nama"] == kunci)


def deret_csv(mulai, pola_per_sku, hari):
    """pola_per_sku: {sku: fungsi(i)->qty}. Hari qty 0 tidak ditulis (seperti ekspor kasir)."""
    rows = ["tanggal;sku;nama;qty"]
    for i in range(hari):
        t = mulai + timedelta(days=i)
        for sku, f in pola_per_sku.items():
            q = f(i)
            if q:
                rows.append(f"{t.isoformat()};{sku};Barang {sku};{q}")
    return "\n".join(rows)


def harapan(series, L, H, stok, dp=0, z=Z95):
    mu = sum(series) / len(series)
    sd = statistics.stdev(series)
    ss = z * sd * math.sqrt(L)
    rop = math.ceil(mu * L + ss)
    tgt = math.ceil(mu * (L + H) + ss)
    return {"mu": mu, "sd": sd, "ss": math.ceil(ss), "rop": rop, "tgt": tgt, "posisi": stok + dp}


M0 = date(2026, 8, 3)

# ---------------------------------------------------------------- A. kasus normal (pola stabil)
POLA_A = [3, 5, 2, 0, 4, 6, 8]
POLA_B = [1, 0, 2, 1, 0, 1, 2]
jual_a = tulis("a.csv", deret_csv(M0, {"A1": lambda i: POLA_A[i % 7], "B1": lambda i: POLA_B[i % 7]}, 56))
barang_a = tulis("a_barang.csv", "sku;nama;stok;harga_beli;pemasok\nA1;Kaos Hitam M;20;Rp 10.000;Toko P1\nB1;Tote Bag;25;5rb;Toko P1\n")
k, h = jalan("--file", jual_a, "--barang", barang_a)
cek("A0 jalan", k == 0)
sa = [POLA_A[i % 7] for i in range(56)]
e = harapan(sa, 7, 14, 20)
a1 = brg(h, "A1")
cek("A1 rata-rata harian = 4", a1["rata_rata_harian"] == 4)
cek("A2 simpangan sampel", abs(a1["simpangan_harian"] - round(e["sd"], 2)) < 0.006)
cek("A3 tren stabil (faktor 1)", a1["tren"] == "stabil" and a1["faktor_tren"] == 1)
cek("A4 stok pengaman = ceil(1,65 x sd x akar 7)", a1["stok_pengaman"] == e["ss"])
cek("A5 titik pesan ulang", a1["titik_pesan_ulang"] == e["rop"])
cek("A6 stok target", a1["stok_target"] == e["tgt"])
cek("A7 kelompok PESAN SEKARANG", a1["kelompok"] == "PESAN_SEKARANG")
cek("A8 jumlah pesan = target - stok", a1["jumlah_pesan"] == e["tgt"] - 20)
cek("A9 nilai pesanan = jumlah x Rp10.000", a1["nilai_pesanan"] == (e["tgt"] - 20) * 10000)
cek("A10 habis dalam floor(20/4) = 5 hari", a1["habis_dalam_hari"] == 5)
cek("A11 kosong sebelum barang datang (5 < 7)", a1["kosong_sebelum_barang_datang"] is True)
sb = [POLA_B[i % 7] for i in range(56)]
eb = harapan(sb, 7, 14, 25)
b1 = brg(h, "B1")
hari_ke_rop = math.floor((25 - eb["rop"]) / 1)
kel_b = "PESAN_SEKARANG" if 25 <= eb["rop"] or hari_ke_rop < 1 else ("PESAN_MINGGU_DEPAN" if hari_ke_rop <= 7 else "AMAN")
cek("A12 barang B: ROP & kelompok", b1["titik_pesan_ulang"] == eb["rop"] and b1["kelompok"] == kel_b)
g = h["pesanan_per_pemasok"][0]
cek("A13 pesanan per pemasok", g["pemasok"] == "Toko P1" and g["total_nilai"] == a1["nilai_pesanan"] + (b1["nilai_pesanan"] or 0))
cek("A14 draf WA berisi pemasok, jumlah, isian", "Toko P1" in g["draf_wa"] and f"{e['tgt'] - 20} pcs" in g["draf_wa"] and "[isian:" in g["draf_wa"])
cek("A15 acuan = tanggal terakhir data", h["rentang_data"]["tanggal_acuan"] == (M0 + timedelta(days=55)).isoformat())
k, t = jalan("--file", jual_a, "--barang", barang_a, "--format", "teks")
cek("A16 teks berlabel UNTUK AGENT SAJA", k == 0 and t["teks"].startswith("[UNTUK AGENT SAJA") and "PESAN SEKARANG" in t["teks"])
k, h90 = jalan("--file", jual_a, "--barang", barang_a, "--layanan", "99")
cek("A17 layanan 99% -> z 2,33", brg(h90, "A1")["stok_pengaman"] == math.ceil(2.33 * e["sd"] * math.sqrt(7)))
k, h14 = jalan("--file", jual_a, "--barang", barang_a, "--hari-ini", (M0 + timedelta(days=70)).isoformat())
cek("A18 hari ini jauh dari akhir data -> catatan", any("hari sebelum hari ini" in c for c in h14["catatan"]))

# ---------------------------------------------------------------- C. lead time beda per barang
pola = {s: (lambda i: POLA_A[i % 7]) for s in ("X", "Y", "Z", "W")}
jual_c = tulis("c.csv", deret_csv(M0, pola, 56))
barang_c = tulis("c_barang.csv", "sku;stok;lead time (hari);pemasok\nX;100;3;\nY;100;2 minggu;\nZ;100;;Grosir Zed\nW;100;;\n")
pemasok_c = tulis("c_pemasok.csv", "pemasok;lead_time_hari\nGrosir Zed;10\n")
k, h = jalan("--file", jual_c, "--barang", barang_c, "--pemasok", pemasok_c)
cek("C0 jalan", k == 0)
for sku, L, sumber in (("X", 3, "data barang"), ("Y", 14, "data barang"), ("Z", 10, "data pemasok"), ("W", 7, "default")):
    e = harapan(sa, L, 14, 100)
    x = brg(h, sku)
    cek(f"C1 {sku}: lead time {L} ({sumber})", x["lead_time_hari"] == L and x["sumber_lead_time"] == sumber)
    cek(f"C2 {sku}: stok pengaman & ROP sesuai lead time {L}", x["stok_pengaman"] == e["ss"] and x["titik_pesan_ulang"] == e["rop"])
k, h = jalan("--file", jual_c, "--barang", barang_c, "--lead-time", "5")
cek("C3 --lead-time 5 untuk barang tanpa lead time", brg(h, "W")["lead_time_hari"] == 5)

# ---------------------------------------------------------------- D. stok sekarang tidak ada
k, h = jalan("--file", jual_a)
d = brg(h, "A1")
e = harapan(sa, 7, 14, 0)
cek("D1 kelompok STOK BELUM DIKETAHUI", d["kelompok"] == "STOK_BELUM_DIKETAHUI")
cek("D2 jumlah pesan tidak dikira", d["jumlah_pesan"] is None and d["nilai_pesanan"] is None)
cek("D3 ROP & target tetap dihitung", d["titik_pesan_ulang"] == e["rop"] and d["stok_target"] == e["tgt"])
cek("D4 pertanyaan pertama soal stok", "stok sekarang" in h["pertanyaan_usulan"][0])
cek("D5 isian kosong stok", any("stok sekarang" in x for x in h["isian_kosong"]))
cek("D6 maksimal 3 pertanyaan", len(h["pertanyaan_usulan"]) <= 3)

# ---------------------------------------------------------------- E. data rusak & tanggal campur
excel = 46268  # nomor seri Excel
tgl_excel = date(1899, 12, 30) + timedelta(days=excel)
data_e = "\n".join([
    "No. Pesanan;Tanggal;SKU;Nama Barang;Qty;Status",
    "INV-1;2026-09-01;K1;Kopi Susu;3;Selesai",
    "INV-2;02/09/2026;K1;Kopi Susu;2 pcs;Selesai",
    "INV-3;3 Sep 2026;K1;Kopi Susu;4;Selesai",
    "INV-4;04-09-2026 13:22;K1;Kopi Susu;1;Selesai",
    "INV-5;Kamis, 5 September 2026;K1;Kopi Susu;5;Selesai",
    "INV-6;2026/09/06;K1;Kopi Susu;2;Selesai",
    f"INV-7;{excel};K1;Kopi Susu;1;Selesai",
    "INV-8;09/13/2026;K1;Kopi Susu;6;Selesai",
    "INV-9;kemarin;K1;Kopi Susu;3;Selesai",
    "INV-10;2026-09-07;K1;Kopi Susu;abc;Selesai",
    "INV-11;2026-09-08;K1;Kopi Susu;;Selesai",
    "INV-12;2026-09-09;K1;Kopi Susu;10;Batal",
    "INV-1;2026-09-01;K1;Kopi Susu;3;Selesai",
    "INV-13;2026-09-10;;;2;Selesai",
])
k, h = jalan("--data", data_e)
cek("E0 jalan walau ada baris rusak", k == 0)
e1 = brg(h, "K1")
cek("E1 total terjual hanya baris sah", e1["data"]["total_terjual"] == 3 + 2 + 4 + 1 + 5 + 2 + 1 + 6)
cek("E2 nomor seri Excel terbaca", h["rentang_data"]["dari"] == min(date(2026, 9, 1), tgl_excel).isoformat())
cek("E3 tanggal bulan/hari (09/13/2026) -> 13 Sep", h["rentang_data"]["sampai"] == "2026-09-13")
cek("E4 baris dilewati: tanggal, jumlah, kosong, barang", h["dilewati"]["jumlah"] == 4)
cek("E5 catatan status batal", any("Batal".lower() in c.lower() and "status" in c for c in h["catatan"]))
cek("E6 catatan baris dobel", any("dobel" in c for c in h["catatan"]))
cek("E7 catatan format bulan/tanggal", any("bulan/tanggal" in c for c in h["catatan"]))
cek("E8 data < 14 hari -> DATA BELUM CUKUP", e1["kelompok"] == "DATA_BELUM_CUKUP")
for nama, arg in [("E9 kosong", ["--data", ""]),
                  ("E10 tanpa kolom qty", ["--data", "tanggal;nama\n2026-09-01;Kopi"]),
                  ("E11 semua tanggal rusak", ["--data", "tanggal;nama;qty\nkemarin;Kopi;2\nbesok;Kopi;3"]),
                  ("E12 layanan 93%", ["--file", jual_a, "--layanan", "93"]),
                  ("E13 faktor musim 0", ["--file", jual_a, "--faktor-musim", "0"]),
                  ("E14 file .xls lama", ["--file", tulis("lama.xls", "x")]),
                  ("E15 file tidak ada", ["--file", os.path.join(TMP, "tidak-ada.csv")])]:
    k, e = jalan(*arg)
    cek(nama + " -> kode 2 + saran", k == 2 and "error" in e and "saran" in e)

# ---------------------------------------------------------------- F. permintaan nol / barang mati
data_f = deret_csv(M0, {"L1": lambda i: 2, "OLD": lambda i: 3 if i < 5 else 0, "OLD0": lambda i: 1 if i < 5 else 0}, 70)
barang_f = tulis("f_barang.csv", "sku;nama;stok;harga_beli\nL1;Laris;100;1000\nOLD;Lama;25;34rb\nOLD0;Lama Habis;0;5000\nNOL;Tidak Pernah Laku;10;20.000\n")
k, h = jalan("--data", data_f, "--barang", barang_f)
cek("F0 jalan", k == 0)
nol = brg(h, "NOL")
cek("F1 tidak pernah laku 70 hari + stok -> BARANG MATI", nol["kelompok"] == "BARANG_MATI" and nol["nilai_tertahan"] == 200000)
old = brg(h, "OLD")
cek("F2 terakhir laku 65 hari lalu -> BARANG MATI", old["kelompok"] == "BARANG_MATI" and old["data"]["hari_tanpa_penjualan"] == 65)
cek("F3 modal tertahan = 25 x Rp34.000", old["nilai_tertahan"] == 850000)
cek("F4 stok habis + tidak laku -> TIDAK ADA PENJUALAN (tidak dipesan)", brg(h, "OLD0")["kelompok"] == "TIDAK_ADA_PENJUALAN" and brg(h, "OLD0")["jumlah_pesan"] is None)
cek("F5 total modal tertahan", h["ringkasan"]["nilai_barang_mati"] == 1050000)
cek("F6b catatan barang daftar yang tidak ada di penjualan", any("Tidak Pernah Laku" in c and "tidak muncul" in c for c in h["catatan"]))
cek("F6 barang mati tidak ikut daftar laris", "Lama" not in h["barang_laris_untuk_bundling"] and "Laris" in h["barang_laris_untuk_bundling"])
data_f2 = deret_csv(M0, {"L1": lambda i: 2}, 30)
k, h = jalan("--data", data_f2, "--barang-data", "sku;nama;stok\nL1;Laris;5\nBARU;Belum Laku;8")
cek("F7 belum laku tapi data < 60 hari -> TIDAK ADA PENJUALAN (bukan barang mati)", brg(h, "BARU")["kelompok"] == "TIDAK_ADA_PENJUALAN")
k, h = jalan("--data", data_f2, "--barang-data", "sku;stok\nL1;5", "--batas-mati", "20")
cek("F8 --batas-mati diubah", k == 0 and h["parameter"]["batas_barang_mati_hari"] == 20)

# ---------------------------------------------------------------- G. MOQ & kelipatan (permintaan tetap 1/hari -> simpangan 0)
pola_g = {s: (lambda i: 1) for s in ("G0", "G1", "G2", "G3", "G4")}
jual_g = tulis("g.csv", deret_csv(M0, pola_g, 28))
barang_g = tulis("g_barang.csv", "sku;stok;kelipatan;moq;harga_beli\nG0;5;;;7500\nG1;5;12;;7500\nG2;5;12;50;7500\nG3;5;;20;7500\nG4;5;0,5;;7500\n")
k, h = jalan("--file", jual_g, "--barang", barang_g, "--horizon", "11")
cek("G0 jalan", k == 0)
g0 = brg(h, "G0")
cek("G1 simpangan 0 -> stok pengaman 0, ROP 7, target 18", g0["stok_pengaman"] == 0 and g0["titik_pesan_ulang"] == 7 and g0["stok_target"] == 18)
cek("G2 tanpa kemasan: pesan 13", g0["jumlah_pesan"] == 13 and g0["nilai_pesanan"] == 13 * 7500)
cek("G3 kelipatan 12: 13 -> 24", brg(h, "G1")["jumlah_pesan"] == 24 and brg(h, "G1")["nilai_pesanan"] == 180000)
cek("G3b jumlah kemasan 24/12 = 2", brg(h, "G1")["jumlah_kemasan"] == 2 and brg(h, "G0")["jumlah_kemasan"] is None)
cek("G4 MOQ 50 + kelipatan 12 -> 60", brg(h, "G2")["jumlah_pesan"] == 60)
cek("G5 MOQ 20 -> 20 + keterangan", brg(h, "G3")["jumlah_pesan"] == 20 and any("minimal order" in x for x in brg(h, "G3")["penyesuaian_jumlah"]))
cek("G6 kelipatan 0,5 -> tetap 13", brg(h, "G4")["jumlah_pesan"] == 13)
pemasok_g = tulis("g_pemasok.csv", "pemasok;lead_time;minimal belanja\nToko Gx;7;Rp500.000\n")
barang_g2 = tulis("g_barang2.csv", "sku;stok;harga_beli;pemasok\nG0;5;7500;Toko Gx\n")
k, h = jalan("--file", jual_g, "--barang", barang_g2, "--horizon", "11", "--pemasok", pemasok_g)
gp = h["pesanan_per_pemasok"][0]
cek("G7 kurang dari minimal belanja", gp["minimal_belanja"] == 500000 and gp["kurang_dari_minimal_belanja"] == 500000 - 13 * 7500)

# ---------------------------------------------------------------- Q. minggu depan, aman, stok berlebih, dalam pesanan
pola_q = {s: (lambda i: 2) for s in ("Q1", "Q2", "Q3", "Q4")}
jual_q = tulis("q.csv", deret_csv(M0, pola_q, 28))
barang_q = tulis("q_barang.csv", "sku;stok;dalam pesanan;harga beli\nQ1;20;;1000\nQ2;40;;1000\nQ3;300;;1000\nQ4;6;10;1000\n")
k, h = jalan("--file", jual_q, "--barang", barang_q)
akhir_q = M0 + timedelta(days=27)
q1 = brg(h, "Q1")
cek("Q1 ROP 14, ROP tercapai 3 hari lagi -> MINGGU DEPAN", q1["kelompok"] == "PESAN_MINGGU_DEPAN" and q1["tanggal_pesan"] == (akhir_q + timedelta(days=3)).isoformat())
cek("Q2 jumlah minggu depan = 42 - (20 - 2x3)", q1["jumlah_pesan"] == 42 - (20 - 6))
cek("Q3 ROP 13 hari lagi -> AMAN", brg(h, "Q2")["kelompok"] == "AMAN")
q3 = brg(h, "Q3")
cek("Q4 stok 150 hari -> stok berlebih, kelebihan 258", q3.get("stok_berlebih") is True and q3["kelebihan_stok"] == 258 and q3["nilai_kelebihan"] == 258000)
q4 = brg(h, "Q4")
k, hm = jalan("--file", jual_q, "--barang-data", "sku;stok\nQ1;-3")
cek("Q6 stok minus: jumlah = 42 - (-3) = 45 + catatan", brg(hm, "Q1")["jumlah_pesan"] == 45 and any("stok minus" in c for c in brg(hm, "Q1")["catatan"]))
cek("Q5 dalam pesanan ikut posisi stok (6+10=16 -> ROP 1 hari lagi -> minggu depan)", q4["posisi_stok"] == 16 and q4["kelompok"] == "PESAN_MINGGU_DEPAN")

# ---------------------------------------------------------------- H. data belum cukup / barang baru / mulai jual
data_h = deret_csv(M0, {"LAMA": lambda i: 2, "BARU": lambda i: 3 if i >= 51 else 0}, 60)
k, h = jalan("--data", data_h, "--barang-data", "sku;stok\nLAMA;50\nBARU;4")
bh = brg(h, "BARU")
cek("H1 barang baru 9 hari -> DATA BELUM CUKUP", bh["kelompok"] == "DATA_BELUM_CUKUP" and bh["jumlah_pesan"] is None)
cek("H2 laju sementara 27/9 = 3, stok 4 habis 1 hari", bh["pengamatan"]["laju_sementara_per_hari"] == 3 and bh["pengamatan"]["habis_dalam_hari_laju_sementara"] == 1)
cek("H3 pertanyaan barang baru", any("barang baru" in q for q in h["pertanyaan_usulan"]))
mulai = (M0 + timedelta(days=40)).isoformat()
k, h = jalan("--data", data_h, "--barang-data", f"sku;stok;mulai jual\nLAMA;50;\nBARU;4;{mulai}")
bh = brg(h, "BARU")
cek("H4 mulai jual diisi -> dihitung dari tanggal itu (27/20 hari)", bh["kelompok"] != "DATA_BELUM_CUKUP" and abs(bh["rata_rata_harian"] - round(27 / 20, 2)) < 0.006)

# ---------------------------------------------------------------- I. tren
data_i = deret_csv(M0, {"N1": lambda i: 4 if i < 42 else 8, "N2": lambda i: 2 if i < 42 else 20, "N3": lambda i: 6 if i < 42 else 3}, 70)
k, h = jalan("--data", data_i)
n1, n2, n3 = brg(h, "N1"), brg(h, "N2"), brg(h, "N3")
cek("I1 rata-rata keseluruhan 5,6", n1["rata_rata_harian"] == 5.6)
cek("I2 tren naik (8 vs 4 = +100 %), dipakai rata-rata 4 minggu (8), tidak dibatasi", n1["tren"] == "naik" and n1["rata_rata_dipakai"] == 8
    and n1["faktor_tren"] == 2 and n1["tren_dibatasi"] is False)
mu2 = (42 * 2 + 28 * 20) / 70
cek("I3 tren naik dibatasi 2x rata-rata seluruh data + disebut terbuka", n2["tren_dibatasi"] is True
    and abs(n2["rata_rata_dipakai"] - round(mu2 * 2, 2)) < 0.006 and "dibatasi" in n2["kalimat_tren"] and "20/hari" in n2["kalimat_tren"].replace(",00", ""))
mu3 = (42 * 6 + 28 * 3) / 70
cek("I4 tren turun (3/4,8 = 0,625)", n3["tren"] == "turun" and abs(n3["rata_rata_dipakai"] - 3) < 0.006 and abs(mu3 - 4.8) < 1e-9)
k, h = jalan("--data", data_i, "--tanpa-tren")
cek("I5 --tanpa-tren memakai rata-rata keseluruhan", brg(h, "N1")["rata_rata_dipakai"] == 5.6)
k, h = jalan("--data", data_i, "--tanpa-tren", "--faktor-musim", "1,5")
cek("I6 faktor musim 1,5 dikalikan", brg(h, "N1")["rata_rata_dipakai"] == 8.4)
k, h = jalan("--data", deret_csv(M0, {"S1": lambda i: 4 if i < 20 else 8}, 30))
cek("I7 data < 42 hari -> tren tidak dihitung", brg(h, "S1")["tren"] == "tidak dihitung")

# ---------------------------------------------------------------- J. ekspor mutasi buku-stok
rows_j = ["tanggal;sku;arah;jenis;qty;harga;hpp;stok_sesudah;ref;catatan",
          "2026-08-01;LAIN;masuk;saldo-awal;50;;10000;50;;"]
stok = 0
mulai_j = date(2026, 8, 11)
rows_j.append(f"{mulai_j.isoformat()};KAOS-HT-M;masuk;saldo-awal;100;;35000;100;;")
stok = 100
hpp = 35000
for i in range(30):
    t = mulai_j + timedelta(days=i)
    stok -= 2
    rows_j.append(f"{t.isoformat()};KAOS-HT-M;keluar;jual-mp;-2;59000;{hpp};{stok};SHP-{i};")
    if i == 10:
        stok += 2
        rows_j.append(f"{t.isoformat()};KAOS-HT-M;masuk;batal-pesanan;2;;{hpp};{stok};SHP-{i};batal")
    if i == 20:
        stok += 50
        hpp = 34662
        rows_j.append(f"{t.isoformat()};KAOS-HT-M;masuk;beli;50;34000;{hpp};{stok};NOTA-1;")
    rows_j.append(f"{t.isoformat()};LAIN;keluar;jual;-1;20000;10000;0;;")
k, h = jalan("--data", "\n".join(rows_j))
j = brg(h, "KAOS-HT-M")
cek("J0 jalan", k == 0)
cek("J1 jual-mp negatif dibaca sebagai penjualan, batal mengurangi (60-2=58)", j["data"]["total_terjual"] == 58)
cek("J2 stok sekarang dari stok sesudah terakhir", j["stok_sekarang"] == stok)
cek("J3 harga beli dari HPP terakhir", j["harga_beli"] == 34662)
cek("J4 rentang barang mulai dari saldo awal", j["data"]["mulai"] == mulai_j.isoformat() and j["data"]["jumlah_hari"] == 30)
cek("J5 pembelian (beli) tidak dihitung penjualan", brg(h, "LAIN")["data"]["total_terjual"] == 30)
stok_bs = tulis("laporan-stok.csv", "\ufefflokasi;sku;nama;varian;satuan;stok;stok_min;hpp_rata2;nilai_persediaan;harga_jual;status\n"
                "A1;KAOS-HT-M;Kaos Polos Cotton 30s;Hitam M;pcs;12;10;34662;415944;59000;aman\n")
k, h = jalan("--data", "\n".join(rows_j), "--barang", stok_bs)
j = brg(h, "KAOS-HT-M")
cek("J6 ekspor laporan stok buku-stok sebagai data barang (stok 12, HPP, nama+varian)",
    k == 0 and j["stok_sekarang"] == 12 and j["harga_beli"] == 34662 and j["nama"] == "Kaos Polos Cotton 30s Hitam M"
    and "harga_jual" not in h["pemetaan_kolom"]["barang"].values())

# ---------------------------------------------------------------- K. tabel lebar, markdown, JSON, marketplace, XLSX
k, h = jalan("--data", "Nama Barang;01/09/2026;02/09/2026;03/09/2026\nKopi;3;;5\nTeh;1;2;0")
cek("K1 tabel lebar (kolom = tanggal)", k == 0 and brg(h, "Kopi")["data"]["total_terjual"] == 8 and brg(h, "Teh")["data"]["total_terjual"] == 3)
k, h = jalan("--data", "| Tanggal | Barang | Terjual |\n|---|---|---|\n| 1 Sep 2026 | Gula 1kg | 4 |\n| 2 Sep 2026 | Gula 1kg | 6 |")
cek("K2 tabel markdown tempelan chat", k == 0 and brg(h, "Gula 1kg")["data"]["total_terjual"] == 10)
k, h = jalan("--data", json.dumps([{"tanggal": "2026-09-01", "sku": "J1", "qty": 3}, {"tanggal": "2026-09-02", "sku": "J1", "qty": 2}]))
cek("K3 input JSON daftar objek", k == 0 and brg(h, "J1")["data"]["total_terjual"] == 5)
gab = tulis("gab.json", json.dumps({"penjualan": [{"tanggal": (M0 + timedelta(days=i)).isoformat(), "sku": "J2", "qty": 2} for i in range(28)],
                                    "barang": [{"sku": "J2", "stok": 10, "harga_beli": 1000, "pemasok": "PT Uji"}],
                                    "pemasok": [{"pemasok": "PT Uji", "lead_time": 3}]}))
k, h = jalan("--file", gab)
cek("K4 JSON gabungan penjualan+barang+pemasok", k == 0 and brg(h, "J2")["lead_time_hari"] == 3 and brg(h, "J2")["stok_sekarang"] == 10)
mp = "\n".join(["Laporan Pesanan Toko Contoh Fiktif", "",
                "No. Pesanan,Status Pesanan,Waktu Pesanan Dibuat,SKU Induk,Nomor Referensi SKU,Nama Produk,Nama Variasi,Jumlah",
                "260901AAA,Selesai,2026-09-01 10:11,KAOS,KAOS-HT-M,Kaos Polos,Hitam M,2",
                "260901BBB,Batal,2026-09-01 11:00,KAOS,KAOS-HT-M,Kaos Polos,Hitam M,5",
                "260902CCC,Sedang Dikirim,2026-09-02 09:00,KAOS,KAOS-HT-M,Kaos Polos,Hitam M,1",
                "260902DDD,Belum Bayar,2026-09-02 09:30,KAOS,KAOS-PT-M,Kaos Polos,Putih M,4"])
k, h = jalan("--data", mp)
cek("K5 ekspor marketplace: baris judul dicari, SKU varian dipakai", k == 0 and h["pemetaan_kolom"]["penjualan"]["sku"] == "Nomor Referensi SKU")
cek("K6 batal & belum bayar tidak dihitung", brg(h, "KAOS-HT-M")["data"]["total_terjual"] == 3 and all(x["sku"] != "KAOS-PT-M" for x in h["barang"]))
cek("K7 nama + variasi digabung", brg(h, "KAOS-HT-M")["nama"] == "Kaos Polos Hitam M")


def xlsx(path, rows):
    ss = []
    def idx(s):
        if s not in ss:
            ss.append(s)
        return ss.index(s)
    sheet = ['<?xml version="1.0" encoding="UTF-8"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>']
    for r, row in enumerate(rows, 1):
        sheet.append(f'<row r="{r}">')
        for c, v in enumerate(row):
            ref = chr(65 + c) + str(r)
            if isinstance(v, (int, float)):
                sheet.append(f'<c r="{ref}"><v>{v}</v></c>')
            else:
                sheet.append(f'<c r="{ref}" t="s"><v>{idx(v)}</v></c>')
        sheet.append("</row>")
    sheet.append("</sheetData></worksheet>")
    sst = ['<?xml version="1.0" encoding="UTF-8"?><sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">']
    sst += [f"<si><t>{s}</t></si>" for s in ss] + ["</sst>"]
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("xl/worksheets/sheet1.xml", "".join(sheet))
        z.writestr("xl/sharedStrings.xml", "".join(sst))


px = os.path.join(TMP, "jual.xlsx")
seri0 = (date(2026, 9, 1) - date(1899, 12, 30)).days
xlsx(px, [["Tanggal", "Nama Barang", "Qty"]] + [[seri0 + i, "Beras 5kg", 3] for i in range(20)])
k, h = jalan("--file", px)
cek("K8 XLSX (tanggal nomor seri) terbaca", k == 0 and brg(h, "Beras 5kg")["data"]["total_terjual"] == 60 and h["rentang_data"]["dari"] == "2026-09-01")

# ---------------------------------------------------------------- L. data per minggu / per bulan
mingguan = [28, 30, 26, 28, 32, 24, 28, 28]
data_l = "tanggal;nama;qty\n" + "\n".join(f"{(M0 + timedelta(days=7 * i)).isoformat()};Minyak 1L;{q}" for i, q in enumerate(mingguan))
k, h = jalan("--data", data_l, "--data-per", "minggu")
l1 = brg(h, "Minyak 1L")
cek("L1 mingguan: rata-rata harian = total / 56", abs(l1["rata_rata_harian"] - round(sum(mingguan) / 56, 2)) < 0.006)
cek("L2 mingguan: simpangan harian = sd mingguan / akar 7", abs(l1["simpangan_harian"] - round(statistics.stdev(mingguan) / math.sqrt(7), 2)) < 0.006)
data_m = "bulan;nama;qty\nAgustus 2026;Sabun;62\nSeptember 2026;Sabun;60"
k, h = jalan("--data", data_m, "--data-per", "bulan")
m1 = brg(h, "Sabun")
mu_m = 122 / 61
cek("L3 bulanan 2 bulan: sd diasumsikan akar rata-rata", m1["asumsi_simpangan"] is True and abs(m1["simpangan_harian"] - round(math.sqrt(mu_m), 2)) < 0.006)
k, h = jalan("--data", data_m)
cek("L4 data bulanan tanpa --data-per -> catatan", any("hanya berisi bulan" in c for c in h["catatan"]))

# ---------------------------------------------------------------- M. lonjakan & retur
data_mx = deret_csv(M0, {"P1": lambda i: 40 if i == 20 else 2}, 42)
k, h = jalan("--data", data_mx)
p1 = brg(h, "P1")
cek("M1 lonjakan terdeteksi (40 vs biasanya 2)", len(p1["lonjakan"]) == 1 and p1["lonjakan"][0]["terjual"] == 40)
cek("M2 pertanyaan lonjakan", any("borongan" in q for q in h["pertanyaan_usulan"]))
k, h2 = jalan("--data", data_mx, "--abaikan-lonjakan")
cek("M3 --abaikan-lonjakan: rata-rata jadi 2", brg(h2, "P1")["rata_rata_harian"] == 2)
data_r = deret_csv(M0, {"R1": lambda i: 2}, 28) + f"\n{(M0 + timedelta(days=27)).isoformat()};R1;Barang R1;-3"
k, h = jalan("--data", data_r)
cek("M4 qty negatif = retur mengurangi penjualan (56-3=53)", brg(h, "R1")["data"]["total_terjual"] == 53 and brg(h, "R1")["retur_batal_dikurangkan"] == 3)

# ---------------------------------------------------------------- N. ekspor bergaya AS (bulan/tanggal) seluruhnya
data_n = "Date,Item,Qty\n" + "\n".join(f"09/{d:02d}/2026,Kopi Susu,2" for d in range(1, 31))
k, h = jalan("--data", data_n)
cek("N1 seluruh file bulan/tanggal -> 1-30 Sep", k == 0 and h["rentang_data"]["dari"] == "2026-09-01" and h["rentang_data"]["sampai"] == "2026-09-30")
cek("N2 catatan gaya Amerika", any("gaya Amerika" in c for c in h["catatan"]))
cek("N3 rata-rata 2/hari", brg(h, "Kopi Susu")["rata_rata_harian"] == 2)

# ---------------------------------------------------------------- V. versi 1.0.1: akan kosong, tren, nama, lonjakan
# V1. AKAN KOSONG sebelum barang datang (dihitung script)
k, h = jalan("--file", jual_a, "--barang", barang_a)
ak = {x["nama"]: x for x in h["akan_kosong_sebelum_barang_datang"]}
cek("V1a barang normal: habis 20/4 = 5 hari < lead time 7 -> kosong ±2 hari", ak.get("Kaos Hitam M", {}).get("hari_kosong") == 2
    and brg(h, "A1")["akan_kosong_hari"] == 2 and h["ringkasan"]["AKAN_KOSONG"] == len(ak))
cek("V1b saran: pesan hari ini, pemasok lebih cepat, terima kosong", any("pesan hari ini" in x for x in ak["Kaos Hitam M"]["saran"])
    and any("lebih cepat" in x for x in ak["Kaos Hitam M"]["saran"]) and any("terima kosong" in x for x in ak["Kaos Hitam M"]["saran"]))
tee = [4, 3, 4, 4, 3, 4, 4, 3, 4, 4]
data_v = deret_csv(M0, {"LAMA": lambda i: 2, "TEE": lambda i: tee[i - 50] if i >= 50 else 0}, 60)
k, h = jalan("--data", data_v, "--barang-data", "sku;nama;stok;lead_time;kelipatan\nLAMA;Lama;500;3;\nTEE;Teether Buah;24;10;12")
tv = brg(h, "TEE")
habis_x = 24 / (37 / 10)
cek("V1c barang data pendek: laju sementara 3,7, habis 6,49 hari, lead time 10 -> kosong ±4 hari",
    tv["kelompok"] == "DATA_BELUM_CUKUP" and tv["akan_kosong_hari"] == math.ceil(10 - habis_x) == 4 and tv["jumlah_pesan"] is None)
akv = h["akan_kosong_sebelum_barang_datang"]
cek("V1d data pendek masuk daftar akan kosong + saran pesan kecil 12 pcs", len(akv) == 1 and akv[0]["nama"] == "Teether Buah"
    and "laju sementara" in akv[0]["dasar_laju"] and "12" in akv[0]["saran"][0] and "pesan kecil" in akv[0]["saran"][0])
cek("V1e stok cukup sampai barang datang -> tidak ditandai", brg(h, "LAMA").get("akan_kosong_hari") is None)
k, t = jalan("--data", data_v, "--barang-data", "sku;nama;stok;lead_time;kelipatan\nLAMA;Lama;500;3;\nTEE;Teether Buah;24;10;12", "--format", "teks")
cek("V1f teks: bagian AKAN KOSONG muncul sebelum PESAN SEKARANG", "AKAN KOSONG SEBELUM BARANG DATANG" in t["teks"]
    and t["teks"].index("AKAN KOSONG SEBELUM") < t["teks"].index("DATA BELUM CUKUP ("))

# V2. tren: 4 minggu terakhir vs sebelumnya (data mingguan seperti warung), batas 0,5-2x disebut terbuka
mingguan_v = "Minggu;Beras 5 kg (karung);Minyak Goreng 2 L;Gula Pasir 1 kg\n" + "\n".join(
    f"{(date(2026, 8, 17) + timedelta(days=7 * i)).isoformat()};{b};{m};{g}" for i, (b, m, g) in enumerate(
        [(20, 30, 40), (22, 32, 38), (19, 35, 41), (23, 33, 39), (21, 38, 42), (24, 40, 40), (22, 42, 37), (25, 45, 41)]))
k, h = jalan("--data", mingguan_v, "--data-per", "minggu", "--barang-data", "nama_barang;stok\nBeras 5 kg (karung);9\nMinyak Goreng 2 L;25\nGula Pasir 1 kg;30")
mv, gv, bv = brg(h, "Minyak Goreng 2 L"), brg(h, "Gula Pasir 1 kg"), brg(h, "Beras 5 kg (karung)")
cek("V2a tabel lebar baris=minggu, kolom=barang terbaca", k == 0 and len(h["barang"]) == 3)
cek("V2b minyak 130 -> 165 per 4 minggu = naik 27 %", mv["tren"] == "naik" and abs(mv["faktor_tren"] - round(165 / 130, 2)) < 0.006)
cek("V2c minyak dipakai laju 4 minggu terakhir 165/28", abs(mv["rata_rata_dipakai"] - round(165 / 28, 2)) < 0.006)
cek("V2d kalimat tren minyak tidak menyebut stabil", "stabil" not in mv["kalimat_tren"] and "naik 27" in mv["kalimat_tren"])
cek("V2e gula stabil memakai rata-rata seluruh data", gv["tren"] == "stabil" and abs(gv["rata_rata_dipakai"] - round(318 / 56, 2)) < 0.006
    and "stabil" in gv["kalimat_tren"])
cek("V2f catatan tren per barang menaruh minyak di 'naik'", any("naik: Minyak Goreng 2 L" in c for c in h["catatan"]))
cek("V2g satuan diambil dari nama '(karung)'", bv["satuan"] == "karung")
lama = deret_csv(M0, {"T1": lambda i: 10 if i < 36 else (4 if i < 92 else 5)}, 120)
k, h = jalan("--data", lama)
t1 = brg(h, "T1")
cek("V2h pembanding hanya 8 minggu sebelum 4 minggu terakhir (5 vs 4 = +25 %), laju 5", t1["tren"] == "naik"
    and t1["faktor_tren"] == 1.25 and t1["rata_rata_dipakai"] == 5)

# V3. pencocokan nama: tanda kurung/huruf/tanda baca; nama mirip ditandai, bukan barang mati
data_n3 = deret_csv(M0, {"x": lambda i: 0}, 1).split("\n")[:1] + [
    f"{(M0 + timedelta(days=i)).isoformat()};;{'Kaos Kaki Bayi isi 3' if i % 2 else 'kaos kaki bayi ISI 3'};2" for i in range(70)] + [
    f"{(M0 + timedelta(days=i)).isoformat()};;Kaos Polos Hitam M;3" for i in range(70)] + [
    f"{(M0 + timedelta(days=i)).isoformat()};;Popok M isi 34;5" for i in range(70)]
k, h = jalan("--data", "\n".join(data_n3), "--barang-data",
             "nama;stok;harga_beli\nKaos Kaki Bayi (isi 3);60;15000\nKaos Hitam M;30;35000\nPopok L isi 34;20;60000")
kk = brg(h, "Kaos Kaki Bayi (isi 3)")
cek("V3a '(isi 3)' = 'isi 3' = 'ISI 3': satu barang, stok 60, bukan barang mati", kk["stok_sekarang"] == 60
    and kk["data"]["total_terjual"] == 140 and kk["kelompok"] != "BARANG_MATI" and h["ringkasan"]["nilai_barang_mati"] == 1200000)
km = brg(h, "Kaos Hitam M")
cek("V3b nama mirip -> MUNGKIN BARANG YANG SAMA, bukan barang mati", km["kelompok"] == "MUNGKIN_SAMA"
    and km["mungkin_sama_dengan"] == ["Kaos Polos Hitam M"] and km.get("nilai_tertahan") is None)
cek("V3c pertanyaan apakah barang yang sama", any("barang yang sama" in q and "Kaos Hitam M" in q for q in h["pertanyaan_usulan"]))
cek("V3d ukuran beda (Popok L vs M) tidak dianggap mirip", brg(h, "Popok L isi 34")["kelompok"] == "BARANG_MATI")
k, h = jalan("--data", deret_csv(M0, {"kaos-ht-m": lambda i: 2}, 28), "--barang-data", "sku;stok\nKAOS HT M;10")
cek("V3e SKU 'kaos-ht-m' = 'KAOS HT M'", k == 0 and len(h["barang"]) == 1 and h["barang"][0]["stok_sekarang"] == 10)

# V4. lonjakan: tren karena lonjakan disebut, hasil tanpa lonjakan sebagai pembanding, ditanya promo
pola_s = [3, 5, 4, 4, 3, 5, 4]
data_s = deret_csv(M0, {"SBN": lambda i: 65 if i == 70 else pola_s[i % 7]}, 90)
k, h = jalan("--data", data_s, "--barang-data", "sku;nama;stok;harga_beli;lead_time\nSBN;Sabun Cair;70;19500;3")
sb = brg(h, "Sabun Cair")
cek("V4a lonjakan 65 terdeteksi", len(sb["lonjakan"]) == 1 and sb["lonjakan"][0]["terjual"] == 65)
cek("V4b dengan lonjakan tren naik; tanpa lonjakan stabil", sb["tren"] == "naik" and sb["tanpa_lonjakan"]["tren"] == "stabil")
cek("V4c catatan: termasuk lonjakan + tren naik karena lonjakan", any("TERMASUK lonjakan" in c and "karena lonjakan" in c for c in sb["catatan"]))
seri_tanpa = [4 if i == 70 else pola_s[i % 7] for i in range(90)]  # hari lonjakan diganti median hari laku (4)
cek("V4d pembanding tanpa lonjakan: hari lonjakan diganti median 4 (361/90)", sb["tanpa_lonjakan"]["rata_rata_dipakai"] == round(sum(seri_tanpa) / 90, 2) == 4.01)
cek("V4e pertanyaan promo/borongan + dua hasil", any("promo" in q and "tanpa lonjakan" in q for q in h["pertanyaan_usulan"]))
pola_k = [1, 2, 3, 2, 1, 2, 3]
k, h = jalan("--data", deret_csv(M0, {"KK": lambda i: 7 if i == 60 else pola_k[i % 7]}, 90))
cek("V4f angka kecil biasa (7 vs biasanya 2) tidak dianggap lonjakan", brg(h, "KK")["lonjakan"] == [])

# V5. lead time umum dari pengguna tidak ditanya ulang
k, h = jalan("--file", jual_c, "--barang", barang_c, "--lead-time", "5")
cek("V5 --lead-time dari pengguna dilabeli & tidak ditanya lagi", brg(h, "W")["sumber_lead_time"] == "lead time umum dari pengguna"
    and not any("berapa hari barang datang" in q for q in h["pertanyaan_usulan"]))

# ---------------------------------------------------------------- W. versi 1.0.2: presisi, kalimat batas, hari habis laju dibatasi
# W1. tepat kelipatan: tren naik tidak kena batas, laju 52/28, stok 260 -> tepat 140 hari (bukan 139)
pola_d = [2, 2, 2, 2, 2, 2, 1]
data_w = deret_csv(M0, {"DOT": lambda i: 1 if i < 42 else pola_d[(i - 42) % 7]}, 70)
k, h = jalan("--data", data_w, "--barang-data", "sku;nama;stok;harga_beli;lead_time\nDOT;Dot Bayi;260;9000;10")
dt = brg(h, "Dot Bayi")
akhir_w = M0 + timedelta(days=69)
cek("W1a laju 52/28, stok 260 -> habis tepat 140 hari", dt["tren"] == "naik" and dt["tren_dibatasi"] is False
    and 260 * 28 / 52 == 140 and dt["habis_dalam_hari"] == 140)
cek("W1b tanggal habis = acuan + 140 hari", dt["perkiraan_tanggal_habis"] == (akhir_w + timedelta(days=140)).isoformat())
# W1c. stabil dengan rata-rata 2/3 (20 terjual / 30 hari), stok 20 -> tepat 30 hari
k, h = jalan("--data", deret_csv(M0, {"TIGA": lambda i: [1, 0, 1][i % 3]}, 30), "--barang-data", "sku;stok\nTIGA;20")  # hari 1 & 30 ada penjualan
cek("W1c rata-rata 2/3, stok 20 -> habis tepat 30 hari", brg(h, "TIGA")["habis_dalam_hari"] == 30)
# W2. kalimat batas hanya bila batas aktif
cek("W2a naik tanpa batas: kalimat 'tidak kena batas', tanpa 'dibatasi'", "tidak kena batas" in dt["kalimat_tren"]
    and "dibatasi" not in dt["kalimat_tren"])
k, h = jalan("--data", data_i)
cek("W2b naik kena batas 2x: kalimat 'dibatasi'", brg(h, "N2")["tren_dibatasi"] is True and "dibatasi" in brg(h, "N2")["kalimat_tren"]
    and "tidak kena batas" not in brg(h, "N2")["kalimat_tren"])
# W3. turun kena batas 0,5x: hari habis menyebut laju dibatasi + hari habis dengan laju terbaru
data_w3 = deret_csv(M0, {"PEL": lambda i: 3 if i < 62 else (1 if i % 2 else 0)}, 90)
k, h = jalan("--data", data_w3, "--barang-data", "sku;nama;stok;lead_time\nPEL;Pelampung;55;10")
pl = brg(h, "Pelampung")
mu_pl = (62 * 3 + 14) / 90
laju_pl = 0.5 * mu_pl
cek("W3a turun kena batas 0,5x rata-rata", pl["tren"] == "turun" and pl["tren_dibatasi"] is True
    and abs(pl["rata_rata_dipakai"] - round(laju_pl, 2)) < 0.006)
cek("W3b hari habis dengan laju dibatasi & dengan laju terbaru (14/28 = 0,5 -> 110 hari)",
    pl["habis_dalam_hari"] == math.floor(55 / laju_pl) and pl["habis_dengan_laju_dibatasi"] is True
    and pl["habis_dalam_hari_laju_terbaru"] == 110)
k, t = jalan("--data", data_w3, "--barang-data", "sku;nama;stok;lead_time\nPEL;Pelampung;55;10", "--format", "teks")
cek("W3c teks: '(laju dibatasi; dengan laju 4 minggu terakhir ...: ±110 hari)'", "(laju dibatasi; dengan laju 4 minggu terakhir 0,5/hari: ±110 hari)" in t["teks"])
# W4. --contoh
p = subprocess.run([sys.executable, SCRIPT, "--contoh"], capture_output=True, text=True, encoding="utf-8")
cek("W4 --contoh menampilkan cara pakai", p.returncode == 0 and "Cara pakai singkat" in p.stdout and "--barang-data" in p.stdout)
cek("W5 ringkasan tanpa barang mati tidak menulis 'modal tertahan Rp0'", "modal tertahan Rp0" not in t["teks"])

# ---------------------------------------------------------------- X. versi 1.0.3: label waktu nyata, rumus per barang, draf WA
# X1. permintaan tetap 2/hari 28 hari, lead time 7, horizon 14 -> ROP 14, target 42; hari ke ROP = (stok - 14) / 2
pola_x = {s: (lambda i: 2) for s in ("B1D", "H3", "H5", "H8")}
jual_x = tulis("x.csv", deret_csv(M0, pola_x, 28))
barang_x = tulis("x_barang.csv", "sku;nama;stok;pemasok;harga_beli\nB1D;Gula;16;Grosir X;1000\nH3;Minyak;20;Grosir X;1000\n"
                 "H5;Tepung;24;Grosir Y;1000\nH8;Kecap;30;Grosir Y;1000\n")
k, h = jalan("--file", jual_x, "--barang", barang_x)
akhir_x = M0 + timedelta(days=27)
pendek = lambda t: f"{t.day} {['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des'][t.month - 1]}"  # noqa: E731
cek("X1a ROP tercapai 1 hari lagi -> 'PESAN BESOK (tgl)'", brg(h, "Gula")["label_waktu"] == f"PESAN BESOK ({pendek(akhir_x + timedelta(days=1))})")
cek("X1b 3 hari lagi -> 'PESAN 3 HARI LAGI (tgl)'", brg(h, "Minyak")["label_waktu"] == f"PESAN 3 HARI LAGI ({pendek(akhir_x + timedelta(days=3))})")
cek("X1c 5 hari lagi -> 'PESAN MINGGU DEPAN (tgl)'", brg(h, "Tepung")["label_waktu"] == f"PESAN MINGGU DEPAN ({pendek(akhir_x + timedelta(days=5))})")
cek("X1d 8 hari lagi -> AMAN", brg(h, "Kecap")["kelompok"] == "AMAN")
k, t = jalan("--file", jual_x, "--barang", barang_x, "--format", "teks")
cek("X1e teks: judul kelompok memakai waktu nyata, bukan 'PESAN MINGGU DEPAN' untuk besok",
    f"PESAN BESOK ({pendek(akhir_x + timedelta(days=1))}) (1)" in t["teks"] and f"PESAN 3 HARI LAGI ({pendek(akhir_x + timedelta(days=3))}) (1)" in t["teks"]
    and f"PESAN MINGGU DEPAN ({pendek(akhir_x + timedelta(days=5))}) (1)" in t["teks"])
# X2. rumus ringkas per barang yang dipesan (angka pembanding dihitung terpisah)
cek("X2a rumus besok: 42 - (16 - 2 x 1) = 28", brg(h, "Gula")["rumus_jumlah"] == "stok target 42 − perkiraan stok saat pesan 14 (16 − 2 × 1 hari) = pesan 28"
    and brg(h, "Gula")["jumlah_pesan"] == 42 - (16 - 2 * 1))
k, h = jalan("--file", jual_g, "--barang", barang_g, "--horizon", "11")
cek("X2b rumus sekarang: 'stok target 18 − stok 5 = pesan 13'", brg(h, "G0")["rumus_jumlah"] == "stok target 18 − stok 5 = pesan 13")
cek("X2c rumus dengan kelipatan: '= 13 → pesan 24 (dibulatkan ke kelipatan 12)'",
    brg(h, "G1")["rumus_jumlah"] == "stok target 18 − stok 5 = 13 → pesan 24 (dibulatkan ke kelipatan 12)")
k, h = jalan("--file", jual_q, "--barang", barang_q)
cek("X2d rumus dengan barang dalam pesanan", brg(h, "Q4")["rumus_jumlah"] == "stok target 42 − perkiraan stok saat pesan 14 (stok 6 + dalam pesanan 10 − 2 × 1 hari) = pesan 28")
k, h = jalan("--file", jual_q, "--barang-data", "sku;stok;dalam pesanan\nQ1;5;2")
cek("X2g rumus sekarang dengan dalam pesanan: 42 − 5 − 2 = 35", brg(h, "Q1")["rumus_jumlah"] == "stok target 42 − stok 5 − dalam pesanan 2 = pesan 35")
k, h = jalan("--file", jual_a, "--barang", barang_a)
e = harapan(sa, 7, 14, 20)
cek("X2e rumus barang A: target - stok = pesan", brg(h, "A1")["rumus_jumlah"] == f"stok target {e['tgt']} − stok 20 = pesan {e['tgt'] - 20}")
k, t = jalan("--file", jual_a, "--barang", barang_a, "--format", "teks")
cek("X2f teks memuat baris RUMUS", f"RUMUS: stok target {e['tgt']} − stok 20 = pesan {e['tgt'] - 20}" in t["teks"])
# X3. draf WA untuk semua kelompok pesan, maks. 6 baris walau barang banyak
k, h = jalan("--file", jual_x, "--barang", barang_x)
cek("X3a draf WA juga untuk pesanan besok/minggu depan", all(g.get("draf_wa") for g in h["pesanan_per_pemasok"])
    and any("Rencana pesan sekitar" in g["draf_wa"] for g in h["pesanan_per_pemasok"]))
banyak = {f"S{i}": (lambda i: 2) for i in range(7)}
k, h = jalan("--data", deret_csv(M0, banyak, 28), "--barang-data", "sku;stok;pemasok\n" + "\n".join(f"S{i};3;Grosir Z" for i in range(7)))
g = h["pesanan_per_pemasok"][0]
cek("X3b 7 barang ke satu pemasok -> draf WA <= 6 baris, semua barang tercantum",
    len(g["draf_wa"].split("\n")) <= 6 and all(f"Barang S{i}:" in g["draf_wa"] for i in range(7)))

print()
print(f"{'SEMUA LULUS' if not GAGAL else str(len(GAGAL)) + ' GAGAL'} ({len(GAGAL)} gagal)")
sys.exit(1 if GAGAL else 0)
