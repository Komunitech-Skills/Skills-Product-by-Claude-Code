#!/usr/bin/env python3
"""Uji regresi cek_promo.py. Jalankan: python3 uji_regresi.py  (keluar 0 bila semua lulus)."""
import json
import os
import subprocess
import sys
import tempfile

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cek_promo.py")
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


# 1. contoh SKILL.md: 89.000 diskon 25% -> 66.800; laba 6.870; impas 59.167; diskon maks 33,5
d = js("margin", "--harga-normal", "Rp 89.000", "--hpp", "52.000", "--diskon-persen", "25", "--biaya-platform", "10",
       "--biaya-per-pesanan", "1.250")["produk"][0]
cek(d["harga_efektif_per_unit"] == 66800, "harga promo 66.800")
cek(d["laba_per_unit_promo"] == 6870, "laba 6.870")
cek(d["harga_impas_per_unit"] == 59167 and d["diskon_maksimal_agar_tidak_rugi_persen"] == 33.5, "impas & diskon maks")
cek(d["diskon_boleh_diklaim_persen"] == 24, "klaim dibulatkan ke bawah (24%)")

# 2. beli 2 gratis 1 tidak error pecahan; laba 0 -> TIPIS
d = js("margin", "--harga-normal", "25.000", "--hpp", "15.000", "--beli-gratis", "2+1", "--biaya-platform", "10")["produk"][0]
cek(d["laba_per_unit_promo"] == 0 and d["status"] == "TIPIS", "beli 2 gratis 1 impas")

# 3. voucher: label total & diskon maksimal bila voucher tetap jalan
rc, out, _ = jalan("margin", "--harga-normal", "89000", "--hpp", "52000", "--diskon-persen", "10", "--voucher", "20.000",
                   "--biaya-platform", "10", "--biaya-per-pesanan", "1.250")
cek("TOTAL (termasuk voucher): 33,5%" in out, "label diskon total termasuk voucher")
cek("diskon harga maksimal hanya: 11,0%" in out, "diskon maks bila voucher tetap jalan")

# 4. '1,250' diberi peringatan
rc, out, _ = jalan("margin", "--harga-normal", "89000", "--hpp", "52000", "--biaya-per-pesanan", "1,250")
cek("PERINGATAN INPUT" in out and "1.250" in out, "peringatan koma 3 digit")

# 5. config berisi opsi untuk produk sama -> tidak dijumlah
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
    json.dump({"produk": [
        {"produk": "Kaos", "harga_normal": "89000", "hpp": "52000", "diskon_persen": "20", "target_unit": "100"},
        {"produk": "Kaos", "harga_normal": "89000", "hpp": "52000", "bundling": "3=229000", "target_unit": "90"}]}, f)
    cfg = f.name
try:
    r = js("margin", "--config", cfg)["ringkasan"]
    cek(r.get("mode") == "perbandingan_opsi" and "total_target_unit" not in r, "opsi tidak dijumlah")
finally:
    os.unlink(cfg)

# 6. jadwal: fase lewat digeser, urutan tetap, tidak ada tanggal < dari
j = js("jadwal", "--momen", "11.11", "--dari", "2026-11-05")
tgl = [b["tanggal"] for b in j["linimasa"]]
cek(all(t >= "2026-11-05" for t in tgl), "tidak ada fase sebelum tanggal acuan")
cek(tgl == sorted(tgl), "urutan fase tetap")
cek(sum(b["digeser"] for b in j["linimasa"]) == 2, "2 fase digeser")

# 7. gajian sisa < 7 hari -> bulan berikutnya
j = js("jadwal", "--momen", "gajian", "--dari", "2026-10-20")
cek(j["hari_h"] == "2026-11-25", "gajian pindah ke bulan berikutnya")
j = js("jadwal", "--momen", "gajian", "--dari", "2026-12-28")
cek(j["hari_h"] == "2027-01-25", "gajian lintas tahun")

# 8. --sampai: fase sesudah H dihitung dari tanggal akhir
j = js("jadwal", "--momen", "11.11", "--tanggal", "2026-11-10", "--sampai", "2026-11-12", "--dari", "2026-09-23")
cek(j["linimasa"][-1]["tanggal"] == "2026-11-19", "evaluasi = sampai + 7")

# 9. input rusak -> exit 2
for args in (["margin", "--harga-normal", "abc", "--hpp", "1"],
             ["margin", "--harga-normal", "50000", "--hpp", "30000", "--diskon-persen", "10", "--harga-promo", "40000"],
             ["margin", "--harga-normal", "50000", "--hpp", "30000", "--bundling", "3-100"],
             ["margin", "--harga-normal", "50,000.50", "--hpp", "1"],
             ["jadwal", "--momen", "lebaran"],
             ["jadwal", "--momen", "10.10", "--tanggal", "2026-10-10", "--sampai", "2026-10-01"]):
    rc, _, err = jalan(*args)
    cek(rc == 2 and "ERROR" in err, "input rusak {}".format(args))

print("Selesai: {} kasus gagal.".format(gagal) if gagal else "Semua uji regresi lulus.")
sys.exit(1 if gagal else 0)
