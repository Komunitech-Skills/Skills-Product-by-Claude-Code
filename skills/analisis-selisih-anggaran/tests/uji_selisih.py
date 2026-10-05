#!/usr/bin/env python3
"""Uji regresi selisih.py. Jalankan dari folder skill: python3 tests/uji_selisih.py

Angka pembanding dihitung ulang secara independen di file ini (float/int biasa), bukan
disalin dari keluaran script.
"""
import json
import os
import subprocess
import sys

DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(DIR, "..", "scripts", "selisih.py")
CONTOH = os.path.join(DIR, "..", "examples", "data")
GAGAL = []


def cek(nama, kondisi):
    print(("OK    " if kondisi else "GAGAL ") + nama)
    if not kondisi:
        GAGAL.append(nama)


def jalankan(*arg, data=None):
    a = [sys.executable, SCRIPT] + list(arg)
    if data is not None:
        a += ["--data", data]
    p = subprocess.run(a, capture_output=True, text=True)
    if p.returncode == 0:
        try:
            return 0, json.loads(p.stdout)
        except ValueError:
            return 0, {"teks": p.stdout}
    try:
        return p.returncode, json.loads(p.stderr)
    except ValueError:
        return p.returncode, {"error": p.stderr}


def pos(h, nama):
    return next(x for x in h["pos"] if x["pos"] == nama)


# A. Arah pendapatan vs biaya
k, h = jalankan(data="pos;anggaran;realisasi\nPenjualan;100jt;110jt\nBiaya bahan;40jt;44jt\nSewa;5jt;4jt\nOmzet jasa;20jt;15jt")
cek("A0 jalan", k == 0)
cek("A1 pendapatan naik = menguntungkan", pos(h, "Penjualan")["arah"] == "menguntungkan")
cek("A2 biaya naik = merugikan", pos(h, "Biaya bahan")["arah"] == "merugikan")
cek("A3 biaya turun = menguntungkan", pos(h, "Sewa")["arah"] == "menguntungkan")
cek("A4 pendapatan turun = merugikan", pos(h, "Omzet jasa")["arah"] == "merugikan")
cek("A5 dampak laba biaya bertanda terbalik", pos(h, "Biaya bahan")["dampak_laba"] == -4_000_000)
lab_ang = 120_000_000 - 45_000_000
lab_real = 125_000_000 - 48_000_000
cek("A6 selisih laba", h["total"]["laba"]["selisih"] == lab_real - lab_ang)
cek("A7 jumlah dampak = selisih laba", sum(x["dampak_laba"] for x in h["pos"]) == lab_real - lab_ang)
cek("A8 persen 1 desimal", pos(h, "Penjualan")["persen"] == "10.0")
cek("A9 retur dianggap biaya", jalankan(data="pos;anggaran;realisasi\nRetur penjualan;1jt;2jt")[1]["pos"][0]["arah"] == "merugikan")

# B. Materialitas
k, h = jalankan(data="pos;anggaran;realisasi\nPenjualan;200jt;198jt\nListrik;1jt;1,1jt\nATK;300rb;320rb\nSewa;5jt;5jt")
cek("B1 Rp2jt (1%) material krn rupiah", pos(h, "Penjualan")["material"] is True)
cek("B2 Rp100rb (10%) material krn persen", pos(h, "Listrik")["material"] is True)
cek("B3 Rp20rb (6,7%) material krn persen", pos(h, "ATK")["material"] is True)
cek("B4 nol tidak material", pos(h, "Sewa")["material"] is False)
k, h2 = jalankan("--aturan", "dan", data="pos;anggaran;realisasi\nPenjualan;200jt;198jt\nListrik;1jt;1,1jt\nIklan;2jt;3jt")
cek("B5 aturan dan: Penjualan tidak material", pos(h2, "Penjualan")["material"] is False)
cek("B6 aturan dan: Iklan (1jt, 50%) material", pos(h2, "Iklan")["material"] is True)
k, h3 = jalankan("--ambang-rp", "5jt", "--ambang-persen", "20", data="pos;anggaran;realisasi\nPenjualan;200jt;198jt\nListrik;1jt;1,1jt")
cek("B7 ambang diubah", not pos(h3, "Penjualan")["material"] and not pos(h3, "Listrik")["material"])
cek("B8 urutan material by rupiah", h["material_urut"][0] == "Penjualan")
k, h4 = jalankan(data="pos;anggaran;realisasi\nPenjualan;10jt;10jt\nBiaya admin bank;0;50rb")
cek("B9 tidak dianggarkan = material & tandai", pos(h4, "Biaya admin bank")["tidak_dianggarkan"] and pos(h4, "Biaya admin bank")["material"])

# C. Dekomposisi harga/volume (contoh buku teks: 10.000 x 50 -> 11.000 x 48)
k, h = jalankan(data="pos;unit_anggaran;unit_realisasi;harga_anggaran;harga_realisasi;anggaran;realisasi\nPenjualan A;10000;11000;50000;48000;;")
p = pos(h, "Penjualan A")
cek("C1 selisih total", p["selisih"] == 11000 * 48000 - 10000 * 50000)
cek("C2 efek volume = 1000 x 50rb", p["pemecahan"]["efek_volume"] == 1000 * 50000)
cek("C3 efek harga = -2rb x 11000", p["pemecahan"]["efek_harga"] == -2000 * 11000)
cek("C4 volume + harga = total", p["pemecahan"]["efek_volume"] + p["pemecahan"]["efek_harga"] == p["selisih"])

# D. Bauran 3 produk (contoh 02), dihitung ulang manual
k, h = jalankan("--file", os.path.join(CONTOH, "02-toko-hijab-q3.csv"))
cek("D0 jalan", k == 0)
ua = [2400, 1800, 600]; ur = [2950, 1500, 520]; pa = [85000, 65000, 245000]; pr = [79000, 66000, 245000]
B = sum(u * p for u, p in zip(ua, pa)); A = sum(u * p for u, p in zip(ur, pr))
vol_i = [(r - a) * p for a, r, p in zip(ua, ur, pa)]
vol_t = round((sum(ur) - sum(ua)) * B / sum(ua))
harga = sum((q - p) * r for p, q, r in zip(pa, pr, ur))
b = h["bauran"]
cek("D1 efek volume total", b["efek_volume_total"] == vol_t == 16_575_000)
cek("D2 efek bauran", b["efek_bauran"] == sum(vol_i) - vol_t == -8_925_000)
cek("D3 efek harga", b["efek_harga"] == harga == -16_200_000)
cek("D4 volume+bauran+harga = selisih pendapatan", b["jumlah"] == A - B == h["total"]["pendapatan"]["selisih"])
cek("D5 cek_jumlah cocok", h["cek_jumlah"] == "cocok")
f = 4970 / 4800
hpp = pos(h, "HPP")
cek("D6 HPP anggaran disesuaikan", hpp["anggaran_disesuaikan"] == round(234_000_000 * f))
cek("D7 HPP efek volume + sisa = selisih", hpp["efek_volume_penjualan"] + hpp["selisih_setelah_disesuaikan"] == hpp["selisih"])

# E. Biaya dengan kuantitas (lembur, contoh 03)
k, h = jalankan("--file", os.path.join(CONTOH, "03-jasa-kebersihan-agustus.csv"))
lb = pos(h, "Lembur petugas")["pemecahan"]
cek("E1 efek pemakaian lembur (260 jam x 25rb)", lb["efek_pemakaian"] == 260 * 25000)
cek("E2 efek harga lembur (1.500 x 410)", lb["efek_harga_input"] == 1500 * 410)
cek("E3 lembur unfavorable", pos(h, "Lembur petugas")["arah"] == "merugikan")
cek("E4 laba", h["total"]["laba"]["selisih"] == (166_500_000 - 112_365_000) - (165_000_000 - 98_510_000))

# F. Pembulatan: komponen tetap menjumlah persis
k, h = jalankan(data="pos;unit_anggaran;unit_realisasi;anggaran;realisasi\nPenjualan kue;333;347;10.000.000;10.555.555")
p = pos(h, "Penjualan kue")["pemecahan"]
cek("F1 jumlah persis walau harga pecahan", p["efek_volume"] + p["efek_harga"] == 555_555)
cek("F2 efek volume dibulatkan", p["efek_volume"] == round(14 * 10_000_000 / 333))

# G. Data rusak & format
for nama, d in [("G1 angka huruf", "pos;anggaran;realisasi\nPenjualan;abc;10jt"),
                ("G2 kolom realisasi hilang", "pos;budget\nA;1"),
                ("G3 kosong", ""),
                ("G4 negatif", "pos;anggaran;realisasi\nPenjualan;-5jt;3jt"),
                ("G5 semua realisasi kosong", "pos;anggaran;realisasi\nGaji;5jt;"),
                ("G6 jenis aneh", "pos;jenis;anggaran;realisasi\nA;xyz;1jt;2jt")]:
    k, e = jalankan(data=d)
    cek(nama + " -> kode 2 + saran", k == 2 and "error" in e and "saran" in e)
k, e = jalankan("--ambang-persen", "abc", data="pos;anggaran;realisasi\nA;1;2")
cek("G7 ambang rusak", k == 2)
k, e = jalankan("--variabel", "Tidak ada", data="pos;anggaran;realisasi\nHPP;1jt;2jt")
cek("G8 --variabel tak dikenal", k == 2)
k, h = jalankan(data="pos;anggaran;realisasi\nPenjualan;10jt;9jt\nGaji;5jt;\nLaba bersih;3jt;4jt")
cek("G9 baris tanpa realisasi dilewati", any("Gaji" in x for x in h["dilewati"]))
cek("G10 baris laba tidak dihitung sebagai pos", all(x["pos"] != "Laba bersih" for x in h["pos"]))
cek("G11 laba tabel beda -> catatan", any("BEDA" in c for c in h["catatan"]))
k, h = jalankan(data="| Pos | Anggaran | Realisasi |\n|---|---|---|\n| Penjualan | Rp 12.500.000 | Rp 11.000.000 |\n| Iklan | 1,5 jt | 2 jt |")
cek("G12 tabel markdown + Rp + jt", k == 0 and pos(h, "Iklan")["selisih"] == 500_000)
k, h = jalankan(data='Item,Budget,Actual\nSales,"45,000,000","50,000,000"\nRent,"5,000,000","5,500,000"')
cek("G13 CSV Excel Inggris", k == 0 and pos(h, "Sales")["selisih"] == 5_000_000 and pos(h, "Rent")["arah"] == "merugikan")
k, h = jalankan(data="pos\tanggaran\trealisasi\nPenjualan\t10000000\t12000000")
cek("G14 TSV", k == 0 and h["total"]["pendapatan"]["selisih"] == 2_000_000)
k, h = jalankan("--format", "teks", data="pos;anggaran;realisasi\nPenjualan;10jt;9jt")
cek("G15 teks berlabel agent", h["teks"].startswith("[UNTUK AGENT SAJA"))
k, h = jalankan(data="pos;unit_anggaran;unit_realisasi;anggaran;realisasi\nPenjualan;0;10;1jt;2jt")
cek("G16 unit 0 -> tanpa pemecahan, tetap jalan", k == 0 and "pemecahan" not in pos(h, "Penjualan"))

print()
print(f"{'SEMUA LULUS' if not GAGAL else str(len(GAGAL)) + ' GAGAL'}")
sys.exit(1 if GAGAL else 0)
