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
cek(d["pesanan_dari_iklan_bila_capai_cac"] == 118, "2.000.000/16.900=118,3 -> 118 ke bawah")
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

print("SEMUA LULUS" if not gagal else f"{gagal} GAGAL")
sys.exit(1 if gagal else 0)
