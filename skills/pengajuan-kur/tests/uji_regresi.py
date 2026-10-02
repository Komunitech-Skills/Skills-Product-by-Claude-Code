#!/usr/bin/env python3
"""Uji regresi simulasi_kur.py. Jalankan: python3 tests/uji_regresi.py (dari folder skill)."""
import json
import os
import subprocess
import sys

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts", "simulasi_kur.py")
GAGAL = []


def jalankan(*arg):
    p = subprocess.run([sys.executable, SCRIPT] + list(arg), capture_output=True, text=True)
    return p.returncode, (json.loads(p.stdout) if p.returncode == 0 else json.loads(p.stderr or "{}"))


def cek(nama, kondisi):
    print(("OK   " if kondisi else "GAGAL") + " " + nama)
    if not kondisi:
        GAGAL.append(nama)


# Angka dasar (diverifikasi independen: anuitas P*r/(1-(1+r)^-n))
k, h = jalankan("--plafon", "10jt", "--bunga", "3", "--tenor", "36", "--metode", "anuitas")
cek("anuitas 10 jt 3% 36 bln = Rp 290.812", h["hasil"]["anuitas"]["cicilan_per_bulan"] == 290812)
k, h = jalankan("--plafon", "50jt", "--bunga", "6", "--tenor", "36", "--laba-bersih", "7,5jt")
a, f = h["hasil"]["anuitas"], h["hasil"]["flat"]
cek("anuitas 50 jt 6% 36 = 1.521.097; flat = 1.638.889", a["cicilan_per_bulan"] == 1521097 and f["cicilan_per_bulan"] == 1638889)
cek("total pokok = plafon", a["cek_total_pokok_sama_plafon"] and f["cek_total_pokok_sama_plafon"])
cek("rasio 20,3% AMAN", a["kemampuan_bayar"]["rasio_cicilan_terhadap_laba_persen"] == 20.3)

# 'persen' bukan 'per bulan'
for teks, harap in (("5 persen", 5.0), ("6 persen per tahun", 6.0), ("6% efektif", 6.0),
                    ("0,5 persen per bulan", 6.0), ("0,5%/bulan", 6.0), ("1% sebulan", 12.0)):
    k, h = jalankan("--plafon", "10jt", "--bunga", teks, "--tenor", "12", "--metode", "anuitas")
    cek(f"bunga '{teks}' → {harap}%/tahun", k == 0 and h["input"]["bunga_per_tahun_persen"] == harap)

# Bunga acuan Permenko 1/2026
def acuan(*arg):
    k, h = jalankan("--tenor", "36", "--kur", "--metode", "anuitas", *arg)
    return h["input"]["bunga_per_tahun_persen"] if k == 0 else None

cek("super mikro 3%", acuan("--plafon", "10jt") == 3.0)
cek("mikro produksi 6%", acuan("--plafon", "50jt", "--sektor", "produksi") == 6.0)
cek("mikro dagang akad 2 = 7%", acuan("--plafon", "50jt", "--sektor", "perdagangan", "--akad-ke", "2") == 7.0)
cek("mikro dagang akad 3 ditolak", acuan("--plafon", "50jt", "--sektor", "perdagangan", "--akad-ke", "3") is None)
cek("kecil dagang akad 4 = 9%", acuan("--plafon", "200jt", "--sektor", "perdagangan", "--akad-ke", "4") == 9.0)
cek("naik kelas: mikro terakhir 7% → kecil akad 1 = 8%",
    acuan("--plafon", "200jt", "--sektor", "perdagangan", "--bunga-mikro-terakhir", "7") == 8.0)
cek("naik kelas: maks 9%",
    acuan("--plafon", "200jt", "--sektor", "perdagangan", "--akad-ke", "3", "--bunga-mikro-terakhir", "7") == 9.0)
cek("kecil produksi tetap 6% walau pernah mikro",
    acuan("--plafon", "200jt", "--sektor", "produksi", "--bunga-mikro-terakhir", "7") == 6.0)

# Penggunaan campuran: cek tenor per porsi
k, h = jalankan("--plafon", "100jt", "--tenor", "60", "--kur", "--sektor", "produksi", "--metode", "anuitas",
                "--rincian-dana", "Mesin [inv]=70jt; Stok [mk]=30jt")
per = " ".join(h["cek_ketentuan_kur"]["perhatian"])
cek("porsi modal kerja 60 bln > 36 bln diperingatkan", "modal-kerja" in per and "36 bulan" in per)
cek("porsi tercatat", h["rencana_penggunaan_dana"]["porsi"] == {"investasi": 70000000, "modal-kerja": 30000000})

# Laba negatif tanpa '=' & plafon maks 0 dijelaskan
k, h = jalankan("--plafon", "20jt", "--bunga", "6", "--tenor", "24", "--laba-bersih", "-2jt", "--metode", "anuitas")
cek("laba -2jt diterima", k == 0 and h["hasil"]["anuitas"]["kemampuan_bayar"]["laba_bersih_per_bulan"] == -2000000)
k, h = jalankan("--plafon", "20jt", "--bunga", "6", "--tenor", "24", "--laba-bersih", "3jt", "--cicilan-lain", "1jt",
                "--metode", "anuitas")
cek("plafon maks 0 dijelaskan", "cicilan lain" in h["hasil"]["anuitas"]["plafon_maks_pada_target_rasio"]["catatan"])

# v1.2.3: opsi pisah akad (modal kerja 36 bln + investasi 60 bln), diverifikasi independen
k, h = jalankan("--plafon", "75jt", "--tenor", "36", "--kur", "--sektor", "produksi", "--akad-ke", "1",
                "--laba-bersih", "6,5jt", "--rincian-dana", "Kompresor [inv]=30jt; Sparepart [mk]=45jt")
ps = h.get("opsi_pisah_akad") or {}
fas = {f["jenis"]: f for f in ps.get("fasilitas", [])}
cek("pisah akad: mk 45jt/36 = 1.368.987; inv 30jt/60 = 579.984",
    fas.get("modal-kerja", {}).get("cicilan_per_bulan") == 1368987 and fas.get("investasi", {}).get("cicilan_per_bulan") == 579984)
cek("pisah akad: tahap 1 Rp 1.948.971 = 30,0% AMAN; sesudah bln 36 Rp 579.984",
    ps.get("cicilan_tahap_1") == 1948971 and ps.get("rasio_tahap_1_persen") == 30.0 and
    ps.get("cicilan_setelah_bulan_36") == 579984)
k, h = jalankan("--plafon", "50jt", "--bunga", "6", "--tenor", "36", "--rincian-dana", "Bahan [mk]=50jt")
cek("tanpa dana campuran: tidak ada opsi pisah akad", k == 0 and h["opsi_pisah_akad"] is None)

# Error
cek("bunga 72% ditolak", jalankan("--plafon", "10jt", "--bunga", "72", "--tenor", "12")[0] == 2)
cek("> Rp500 jt dengan --kur ditolak", jalankan("--plafon", "600jt", "--tenor", "36", "--kur")[0] == 2)
cek("tenor 0 ditolak", jalankan("--plafon", "10jt", "--bunga", "6", "--tenor", "0")[0] == 2)

print(f"\n{'SEMUA LULUS' if not GAGAL else str(len(GAGAL)) + ' GAGAL'}")
sys.exit(1 if GAGAL else 0)
