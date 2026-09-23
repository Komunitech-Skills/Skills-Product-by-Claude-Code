#!/usr/bin/env python3
"""Uji regresi proyeksi_kas.py. Jalankan: python3 tests/uji_regresi.py (dari folder skill).

Hanya library standar; membuat file sementara di folder temp sistem lalu menghapusnya.
"""
import json
import os
import subprocess
import sys
import tempfile

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts", "proyeksi_kas.py")
GAGAL = []


def jalankan(csv_teks, *arg):
    with tempfile.TemporaryDirectory() as d:
        f = os.path.join(d, "rencana.csv")
        with open(f, "w", encoding="utf-8") as h:
            h.write(csv_teks)
        p = subprocess.run([sys.executable, SCRIPT, f] + list(arg), capture_output=True, text=True)
        return p.returncode, (json.loads(p.stdout) if p.returncode == 0 else json.loads(p.stderr))


def cek(nama, kondisi):
    print(("OK   " if kondisi else "GAGAL") + " " + nama)
    if not kondisi:
        GAGAL.append(nama)


CONTOH = """minggu;jenis;kategori;nominal;keterangan;kritis
semua;masuk;Penjualan tunai;12.000.000;;
9;masuk;Pelunasan piutang;15.000.000;PT Sinar;
semua;keluar;Bahan baku (supplier);7.000.000;;ya
tgl:25;keluar;Gaji karyawan;18.000.000;;ya
tgl:1;keluar;Sewa;6.500.000;;ya
tgl:10;keluar;Cicilan bank;4.250.000;;ya
5;keluar;Renovasi etalase;9.000.000;;tidak
"""

# 1. Contoh SKILL.md: angka tetap
k, h = jalankan(CONTOH, "--saldo-awal", "20jt", "--mulai", "2026-10-05")
r = h["ringkasan"]
cek("contoh: saldo minggu 8 = 0", h["per_minggu"][7]["saldo_akhir"] == 0)
cek("contoh: batas aman default 14.326.923", h["asumsi_dan_sumber"]["batas_aman"] == 14326923)
cek("contoh: defisit struktural terdeteksi", r["defisit_struktural"] and r["arus_kas_bersih"] == -15250000)
op = {o["opsi"].split(" ")[0]: o for o in h["simulasi_opsi"]}
cek("contoh: supplier saldo terendah 14.000.000", op["Negosiasi"]["saldo_terendah_baru"] == 14000000)
cek("contoh: supplier tertunda 14.000.000, setelah dibayar 4.750.000",
    op["Negosiasi"]["jatuh_setelah_horizon"] == 14000000 and op["Negosiasi"]["saldo_setelah_kewajiban_tertunda"] == 4750000)
cek("contoh: supplier bukan hanya_menunda", op["Negosiasi"]["hanya_menunda"] is False)
cek("contoh: gabungan 18.750.000", op["Gabungan"]["saldo_terendah_baru"] == 18750000)
cek("contoh: peringatan cicilan jatuh setelah horizon",
    any("Cicilan bank" in p and "setelah periode" in p for p in h["peringatan"]))

# 2. Pos wajib selalu kritis, bonus bukan non-kritis
WAJIB = """minggu;jenis;kategori;nominal;kritis
semua;masuk;Penjualan;2jt;
3;keluar;Cicilan mesin jahit;2jt;
4;keluar;Pajak kendaraan (STNK);1jt;
5;keluar;Angsuran leasing kendaraan;3jt;
6;keluar;Gaji dan bonus;10jt;
7;keluar;Bonus akhir tahun karyawan;4jt;
8;keluar;THR karyawan;6jt;tidak
9;keluar;Renovasi dapur;8jt;
10;keluar;Iklan Meta;1jt;
"""
k, h = jalankan(WAJIB, "--saldo-awal", "1jt")
tunda = [o for o in h["simulasi_opsi"] if o["opsi"].startswith("Tunda")]
digeser = {x["kategori"] for o in tunda for x in o["rincian_digeser"]}
for pos in ("Cicilan mesin jahit", "Pajak kendaraan (STNK)", "Angsuran leasing kendaraan", "Gaji dan bonus",
            "Bonus akhir tahun karyawan", "THR karyawan"):
    cek(f"wajib tidak digeser: {pos}", pos not in digeser)
cek("non-kritis tebakan digeser: Renovasi dapur", "Renovasi dapur" in digeser)
cek("peringatan THR ditandai 'tidak' tetap kritis", any("THR karyawan" in p and "KRITIS" in p for p in h["peringatan"]))
cek("peringatan daftar ditebak tidak kritis",
    any("DITEBAK tidak kritis" in p and "Renovasi dapur" in p and "Iklan Meta" in p for p in h["peringatan"]))

# 3. hanya_menunda: kewajiban didorong ke luar horizon tanpa menyelesaikan masalah
TUNDA = """minggu;jenis;kategori;nominal
semua;masuk;Penjualan;5jt
semua;keluar;Belanja stok bahan;6jt
"""
k, h = jalankan(TUNDA, "--saldo-awal", "10jt", "--batas-aman", "0")
o = [x for x in h["simulasi_opsi"] if x["opsi"].startswith("Negosiasi")][0]
cek("hanya_menunda: saldo terendah tampak aman", o["saldo_terendah_baru"] >= 0)
cek("hanya_menunda: label true & saldo setelah tertunda negatif",
    o["hanya_menunda"] is True and o["saldo_setelah_kewajiban_tertunda"] < 0)
cek("defisit struktural (-13 jt)", h["ringkasan"]["defisit_struktural"] and h["ringkasan"]["arus_kas_bersih"] == -13000000)

# 4. Format minggu versi awam
AWAM = """minggu;kategori;nominal
minggu 6;Penjualan;1jt
minggu ke-3;Penjualan;2jt
mg 1-2;Penjualan;3jt
setiap 2 minggu mulai minggu 3;Penjualan;4jt
"""
k, h = jalankan(AWAM, "--saldo-awal", "0")
m = [x["masuk"] for x in h["per_minggu"]]
cek("format awam diterima tanpa baris dilewati", k == 0 and not h["baris_dilewati"])
cek("format awam: nilai per minggu", m[:7] == [3000000, 3000000, 6000000, 0, 4000000, 1000000, 4000000])

# 5. Jumlah minggu & error
k, h = jalankan(TUNDA, "--saldo-awal", "10jt", "--jumlah-minggu", "26")
cek("26 minggu", k == 0 and len(h["per_minggu"]) == 26)
k, h = jalankan(TUNDA, "--saldo-awal", "10jt", "--jumlah-minggu", "3")
cek("3 minggu ditolak", k == 2)
k, h = jalankan("a;b\n1;2\n", "--saldo-awal", "0")
cek("kolom hilang ditolak", k == 2 and "Kolom wajib" in h["error"])
k, h = jalankan(CONTOH, "--saldo-awal", "abc")
cek("saldo rusak ditolak", k == 2)

print(f"\n{'SEMUA LULUS' if not GAGAL else str(len(GAGAL)) + ' GAGAL'}")
sys.exit(1 if GAGAL else 0)
