#!/usr/bin/env python3
"""Uji regresi hitung_tier.py. Jalankan: python3 uji_regresi.py  (keluar 0 bila semua lulus)."""
import csv
import json
import os
import subprocess
import sys
import tempfile

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hitung_tier.py")
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


def tier(d, nama):
    return [t for t in d["produk"][0]["tier"] if t["tier"] == nama][0]


# 1. contoh SKILL.md (mode diskon, pembulatan ke bawah)
d = js("--produk", "Serum", "--hpp", "28.000", "--eceran", "89.000", "--tier", "Dropshipper:1:15",
       "--tier", "Reseller:12:25", "--tier", "Agen:60:35", "--biaya-jual-mitra", "10")
cek(tier(d, "Dropshipper")["harga_mitra"] == 75600, "dropship 75.600")
cek(tier(d, "Reseller")["harga_mitra"] == 66700 and tier(d, "Reseller")["untung_mitra_per_unit_di_eceran"] == 13400,
    "reseller 66.700 / untung 13.400")
cek("MARGIN MITRA TIPIS" in tier(d, "Dropshipper")["status"], "dropship tipis")

# 2. ongkir ke mitra TIDAK dikenakan ke dropshipper
d = js("--hpp", "28000", "--eceran", "89000", "--tier", "Dropshipper:1:20", "--tier", "Reseller:12:25",
       "--ongkir-ke-mitra", "1.500")
cek(tier(d, "Dropshipper")["untung_mitra_per_unit_di_eceran"] == 89000 - 71200, "dropship tanpa ongkir")
cek(tier(d, "Reseller")["untung_mitra_per_unit_di_eceran"] == 89000 - 66700 - 1500, "reseller dengan ongkir")

# 3. eceran usulan memperhitungkan biaya jual & ongkir -> tier termahal tidak langsung TIPIS
d = js("--hpp", "32000", "--mode", "margin", "--tier", "Reseller:1:40", "--tier", "Agen:50:25",
       "--biaya-jual-mitra", "8", "--ongkir-ke-mitra", "1000")
p = d["produk"][0]
res = tier(d, "Reseller")
cek(p["harga_eceran_anjuran"] == 76000, "eceran usulan (53.400+1.000)/0,72 = 75.556 -> 76.000 (dapat {})".format(p["harga_eceran_anjuran"]))
cek(res["untung_mitra_persen"] >= 20, "tier termahal dapat >= target 20% bersih")

# 4. mode margin: pembulatan ke atas
d = js("--hpp", "32.000", "--mode", "margin", "--tier", "Dropshipper:1:45", "--tier", "Reseller:12:35", "--tier", "Agen:60:25")
cek(tier(d, "Dropshipper")["harga_mitra"] == 58200, "margin 45% -> 58.200")

# 5. dua tier harga sama -> peringatan
d = js("--hpp", "30000", "--eceran", "60000", "--tier", "Dropshipper:1:25", "--tier", "Reseller:6:25")
cek(any("harga mitra SAMA" in w for w in d["produk"][0]["peringatan"]), "peringatan harga sama")

# 6. CSV untuk mitra: tanpa HPP, ada keterangan asumsi
with tempfile.TemporaryDirectory() as tmp:
    path = os.path.join(tmp, "mitra.csv")
    rc, _, err = jalan("--hpp", "28000", "--eceran", "89000", "--biaya-jual-mitra", "10", "--csv-keluar", path)
    isi = open(path, encoding="utf-8-sig").read()
    cek("28.000" not in isi and "HPP" not in isi, "CSV mitra tidak memuat HPP")
    cek("setelah potongan jualan 10,0%" in isi and "bukan jaminan" in isi, "CSV memuat keterangan asumsi")
    baris = list(csv.reader(open(path, encoding="utf-8-sig"), delimiter=";"))
    cek(len(baris[0]) == 8, "kolom CSV 8")

# 7. input rusak -> exit 2
for args in (["--hpp", "abc"], ["--hpp", "0"], ["--hpp", "30000", "--mode", "diskon"],
             ["--hpp", "30000", "--eceran", "50000", "--tier", "Reseller:12"],
             ["--hpp", "30000", "--eceran", "50000", "--tier", "A:1:10", "--tier", "a:5:20"],
             ["--hpp", "30000", "--mode", "margin", "--target-margin-mitra", "60", "--biaya-jual-mitra", "45"]):
    rc, _, err = jalan(*args)
    cek(rc == 2 and "ERROR" in err, "input rusak {}".format(args))

print("Selesai: {} kasus gagal.".format(gagal) if gagal else "Semua uji regresi lulus.")
sys.exit(1 if gagal else 0)
