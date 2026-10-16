#!/usr/bin/env python3
"""Uji regresi alokasi_anggaran.py. Jalankan: python3 uji_regresi.py  (keluar 0 bila semua lulus)."""
import json
import os
import subprocess
import sys

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alokasi_anggaran.py")
gagal = 0


def jalan(*args):
    r = subprocess.run([sys.executable, SCRIPT] + list(args), capture_output=True, text=True, encoding="utf-8")
    return r.returncode, r.stdout, r.stderr


def js(*args):
    rc, out, err = jalan(*(list(args) + ["--format", "json"]))
    assert rc == 0, err
    return json.loads(out)


def cek(kondisi, pesan):
    global gagal
    if not kondisi:
        gagal += 1
        print("GAGAL: " + pesan)


# 1. alokasi: 6 jt, cadangan 10% = 600.000; sisa 5.400.000 dibagi 30/25/15/20/10
d = js("alokasi", "--anggaran", "Rp 6.000.000", "--bulan", "3", "--kanal", "Meta Ads=30,TikTok=25,WA=15,Konten=20,Google Maps=10")
tot = {k["kanal"]: k["rupiah_total"] for k in d["kanal"]}
cek(d["cadangan_eksperimen"] == 600000, "cadangan 600.000")
cek(tot == {"Meta Ads": 1620000, "TikTok": 1350000, "WA": 810000, "Konten": 1080000, "Google Maps": 540000}, "pembagian kanal")
cek(sum(tot.values()) + d["cadangan_eksperimen"] == 6000000, "jumlah = anggaran")

# 2. sisa pembulatan: 1.000.001 dibagi 3 kanal sama -> jumlah tetap pas
d = js("alokasi", "--anggaran", "1000001", "--kanal", "A=33.3,B=33.3,C=33.4", "--cadangan-eksperimen", "0")
cek(sum(k["rupiah_total"] for k in d["kanal"]) == 1000001, "sisa pembulatan habis dibagi")

# 3. persen tidak 100 -> error jelas, kode 2
rc, out, err = jalan("alokasi", "--anggaran", "1000000", "--kanal", "A=50,B=40")
cek(rc == 2 and "100" in err, "persen != 100 ditolak")
rc, out, err = jalan("alokasi", "--anggaran", "abc", "--kanal", "A=100")
cek(rc == 2 and "bukan angka" in err, "anggaran rusak ditolak")
rc, out, err = jalan("alokasi", "--anggaran", "1000000", "--kanal", "A=100,a=0.0001")
cek(rc == 2, "kanal ganda / persen salah ditolak")
rc, out, err = jalan("alokasi", "--anggaran", "-5", "--kanal", "A=100")
cek(rc == 2, "anggaran negatif ditolak")

# 4. target: 45.000 - 18.000 - 8% (3.600) - 1.500 = 21.900; ROAS impas 45000/21900 = 2,0548 -> 2,06 (ke atas)
d = js("target", "--harga-jual", "45000", "--hpp", "18000", "--biaya-platform", "8", "--biaya-per-pesanan", "1500",
       "--laba-target-per-pesanan", "5000", "--anggaran-iklan", "2000000", "--target-omzet", "30000000", "--pembelian-ulang", "0,5")
cek(d["margin_kontribusi_per_pesanan"] == 21900, "margin 21.900")
cek(d["cac_impas_pesanan_pertama"] == 21900 and d["roas_impas_pesanan_pertama"] == "2.06", "CAC & ROAS impas")
cek(d["cac_target"] == 16900 and d["roas_target"] == "2.67", "CAC & ROAS target (45000/16900=2,663 -> 2,67)")
cek(d["cac_impas_dengan_pembelian_ulang"] == 32850, "CAC impas + repeat")
cek(d["pesanan_dari_iklan_bila_capai_cac"] == 119, "2.000.000/16.900=118,3 -> 119 ke atas (minimal balik modal)")
cek(d["pesanan_dibutuhkan"] == 667, "30.000.000/45.000=666,7 -> 667 ke atas")
cek(d["anggaran_iklan_maks_impas"] == 667 * 21900, "anggaran maks impas")

# 5. margin negatif -> RUGI, tanpa angka CAC
d = js("target", "--harga-jual", "20000", "--hpp", "19000", "--biaya-platform", "10")
cek(d["status"] == "RUGI" and "cac_impas_pesanan_pertama" not in d, "rugi dilaporkan")
# 6. laba target >= margin
d = js("target", "--harga-jual", "50000", "--hpp", "30000", "--laba-target-per-pesanan", "20000")
cek(d["status"] == "TARGET LABA TIDAK MUNGKIN", "laba target mustahil")
rc, out, err = jalan("target", "--harga-jual", "0", "--hpp", "1")
cek(rc == 2, "harga 0 ditolak")
rc, out, err = jalan("target", "--harga-jual", "1000", "--hpp", "1", "--biaya-platform", "100")
cek(rc == 2, "platform 100% ditolak")

# 7. funnel: 300 <- 30% -> 1000 <- 20% -> 5000 <- 2% -> 250000
d = js("funnel", "--target-pesanan", "300", "--tahap", "Jangkauan>Klik=2", "--tahap", "Klik>Chat=20", "--tahap", "Chat>Pesanan=30")
cek(d["jumlah_awal_dibutuhkan"] == 250000, "funnel mundur 250.000")
d = js("funnel", "--target-pesanan", "10", "--tahap", "Chat>Pesanan=30")
cek(d["jumlah_awal_dibutuhkan"] == 34, "10/0,3=33,3 -> 34 ke atas")
rc, out, err = jalan("funnel", "--target-pesanan", "10", "--tahap", "Chat>Pesanan=150")
cek(rc == 2, "konversi >100% ditolak")
rc, out, err = jalan("funnel", "--target-pesanan", "10", "--tahap", "salah")
cek(rc == 2, "format tahap salah ditolak")

# 8. format angka Indonesia
d = js("target", "--harga-jual", "Rp 1.500.000", "--hpp", "900.000,50")
cek(d["hpp"] == 900001, "format angka Indonesia")

# 9. regresi v1.0.1: --bulan tidak valid ditolak dengan GAGAL (bukan traceback)
for bad in ("0,5", "1,5", "0", "-2", "abc"):
    rc, out, err = jalan("alokasi", "--anggaran", "1000000", "--kanal", "A=100", "--bulan", bad)
    cek(rc == 2 and "GAGAL" in err and "Traceback" not in err, f"--bulan {bad} ditolak dengan GAGAL")
rc, out, err = jalan("alokasi", "--anggaran", "1000000", "--kanal", "A=100", "--bulan", "3")
cek(rc == 0, "--bulan 3 tetap diterima")
rc, out, err = jalan("alokasi", "--anggaran", "0,4", "--kanal", "A=100")
cek(rc == 2, "anggaran < Rp 1 ditolak")
rc, out, err = jalan("alokasi", "--anggaran", "1e40", "--kanal", "A=100")
cek(rc == 2 and "Traceback" not in err, "angka ekstrem tidak crash")
rc, out, err = jalan("funnel", "--target-pesanan", "10", "--tahap", ">Chat=10")
cek(rc == 2, "nama tahap kosong ditolak")

# 10. ambang margin satu set: <15 TERLALU TIPIS, 15-<25 TIPIS, >=25 AMAN
for hpp, harapan in (("8600", "TERLALU TIPIS"), ("8500", "TIPIS"), ("7600", "TIPIS"), ("7500", "AMAN")):
    d = js("target", "--harga-jual", "10000", "--hpp", hpp)
    cek(d["status"] == harapan, f"margin {d['margin_persen']}% -> {harapan} (dapat {d['status']})")

# 11. label keluaran teks = batas minimal/atas, bukan perkiraan
rc, out, err = jalan("target", "--harga-jual", "25000", "--hpp", "9000", "--biaya-platform", "20", "--biaya-per-pesanan", "1000",
                     "--laba-target-per-pesanan", "3000", "--anggaran-iklan", "1350000", "--target-omzet", "30000000")
cek(rc == 0 and "Minimal pelanggan agar sesuai target" in out and "Batas atas anggaran iklan" in out
    and "BUKAN perkiraan" in out and "Pesanan dari iklan:" not in out, "label minimal/batas atas")
# v1.0.7: dengan laba target, angka minimal BUKAN titik impas -> label jelas, tidak lagi "balik modal"
cek("balik modal" not in out and "Titik impas iklan" in out, "dengan laba target: tidak ada label 'balik modal', ada titik impas iklan")
# 12. contoh kedai kopi konsisten: margin 10.000 -> CAC impas 10.000, CAC target 7.000
d = js("target", "--harga-jual", "25000", "--hpp", "9000", "--biaya-platform", "20", "--biaya-per-pesanan", "1000",
       "--laba-target-per-pesanan", "3000")
cek(d["cac_impas_pesanan_pertama"] == 10000 and d["cac_target"] == 7000, "contoh kedai kopi: CAC impas 10.000, target 7.000")

# 13. regresi: minimal pesanan balik modal dibulatkan ke ATAS (472.500 / 42.000 = 11,25 -> 12; 11 x 42.000 < 472.500)
d = js("target", "--harga-jual", "100000", "--hpp", "58000", "--anggaran-iklan", "472500")
cek(d["cac_impas_pesanan_pertama"] == 42000 and d["pesanan_dari_iklan_bila_capai_cac"] == 12
    and d["pesanan_dari_iklan_bila_capai_cac"] * 42000 >= 472500, "minimal pesanan balik modal dibulatkan ke atas (12)")
d = js("target", "--harga-jual", "25000", "--hpp", "9000", "--biaya-platform", "20", "--biaya-per-pesanan", "1000",
       "--laba-target-per-pesanan", "3000", "--anggaran-iklan", "1350000")
cek(d["pesanan_dari_iklan_bila_capai_cac"] == 193 and d["omzet_dari_iklan"] == 4825000, "kedai kopi: minimal 193 pesanan")
d = js("target", "--harga-jual", "25000", "--hpp", "9000", "--biaya-platform", "20", "--biaya-per-pesanan", "1000",
       "--anggaran-iklan", "1350000")
cek(d["pesanan_dari_iklan_bila_capai_cac"] == 135, "anggaran pas habis dibagi tidak naik")

# 14. v1.0.7 warung bakso (gelombang 18): margin 10.000, anggaran iklan 3.240.000
#     titik impas = 3.240.000 / 10.000 = 324; sesuai target (CAC maks 8.000, laba 2.000) = 3.240.000 / 8.000 = 405
args14 = ("target", "--harga-jual", "20000", "--hpp", "9000", "--biaya-per-pesanan", "1000", "--laba-target-per-pesanan", "2000",
          "--anggaran-iklan", "3240000")
d = js(*args14)
cek(d["pesanan_impas_iklan"] == 324 and d["pesanan_dari_iklan_bila_capai_cac"] == 405 and d["omzet_dari_iklan"] == 8100000,
    "bakso: titik impas 324, sesuai target 405, omzet 8.100.000")
rc, out, err = jalan(*args14)
cek(rc == 0 and "Titik impas iklan (pelanggan agar biaya iklan tertutup margin, tanpa laba target; bukan perkiraan): 324" in out
    and "Minimal pelanggan agar sesuai target (biaya iklan maks. Rp 8.000/pelanggan, laba Rp 2.000/pelanggan; bukan perkiraan): 405" in out
    and "balik modal" not in out and "Omzet minimal dari iklan" not in out, "bakso: label teks jelas")
# GoFood: margin 6.000 -> impas 2.025.000 / 6.000 = 337,5 -> 338 (ke ATAS); target CAC 5.000 -> 405
d = js("target", "--harga-jual", "20000", "--hpp", "9000", "--biaya-platform", "20", "--biaya-per-pesanan", "1000",
       "--laba-target-per-pesanan", "1000", "--anggaran-iklan", "2025000")
cek(d["pesanan_impas_iklan"] == 338 and d["pesanan_dari_iklan_bila_capai_cac"] == 405
    and d["pesanan_impas_iklan"] * 6000 >= 2025000 > (d["pesanan_impas_iklan"] - 1) * 6000, "GoFood: titik impas 338 dibulatkan ke atas, target 405")
# tanpa laba target: label lama tetap benar (minimal = titik impas), tanpa baris titik impas ganda
rc, out, err = jalan("target", "--harga-jual", "25000", "--hpp", "9000", "--biaya-platform", "20", "--biaya-per-pesanan", "1000",
                     "--anggaran-iklan", "1350000")
cek(rc == 0 and "Minimal pesanan agar balik modal iklan (bukan perkiraan): 135" in out and "Titik impas iklan" not in out
    and "sesuai target" not in out, "tanpa laba target: label balik modal tetap, tanpa baris ganda")
d = js("target", "--harga-jual", "100000", "--hpp", "58000", "--anggaran-iklan", "472500")
cek(d["pesanan_impas_iklan"] == 12 == d["pesanan_dari_iklan_bila_capai_cac"], "tanpa laba target: titik impas = minimal (12)")
# tanpa anggaran iklan: tidak ada angka pelanggan/impas
d = js("target", "--harga-jual", "20000", "--hpp", "9000", "--laba-target-per-pesanan", "2000")
cek("pesanan_impas_iklan" not in d and "pesanan_dari_iklan_bila_capai_cac" not in d, "tanpa anggaran iklan: tidak ada angka pelanggan")

print("SEMUA LULUS" if not gagal else f"{gagal} GAGAL")
sys.exit(1 if gagal else 0)
