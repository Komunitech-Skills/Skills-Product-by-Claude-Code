#!/usr/bin/env python3
"""Uji rekap_nota.py (rekap dari nota yang ditempel). Jalankan: python3 tests/uji_rekap_nota.py

Pembanding independen: data nota dibuat sebagai struktur Python (bukan teks), dihitung dengan
penjumlahan biasa di fungsi `harapan()` (tanpa memakai kode script), lalu dirender ke beberapa
gaya teks/CSV dan hasil script dibandingkan dengan harapan. Termasuk nota BATAL, nota pengganti
yang menyebut kata "batal", bon, nama & nomor WA pelanggan, menu yang muncul dua kali dalam satu nota.
"""
import io
import json
import os
import random
import subprocess
import sys
import unittest
from contextlib import redirect_stdout

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(AKAR, "scripts", "rekap_nota.py")
sys.path.insert(0, os.path.join(AKAR, "scripts"))
import rekap_nota as R  # noqa: E402

MENU = {"Kopi Susu": 18000, "Americano": 15000, "Roti Bakar Coklat": 15000, "Nasi Goreng Kampung": 25000,
        "Es Teh": 6000, "Es Kopi Susu": 20000}
PELANGGAN = [("Pak Hendra", "0812-3456-7890"), ("Bu Rina", "081398765432"), ("Mbak Sari", "+62 857 1111 2222")]


def harapan(notas, kas_awal=None, kas_fisik=None):
    """Hitung manual dari struktur data (pembanding independen)."""
    sah = [n for n in notas if not n["batal"]]
    porsi, nota_menu, omzet_menu = {}, {}, {}
    metode = {}
    for n in sah:
        jml = 0
        for nama, q in n["item"]:
            porsi[nama] = porsi.get(nama, 0) + q
            omzet_menu[nama] = omzet_menu.get(nama, 0) + q * MENU[nama]
            jml += q * MENU[nama]
        for nama in set(nama for nama, _ in n["item"]):
            nota_menu[nama] = nota_menu.get(nama, 0) + 1
        metode[n["bayar"]] = metode.get(n["bayar"], 0) + jml
    omzet = sum(metode.values())
    h = {"nota_sah": len(sah), "batal": sorted(n["id"] for n in notas if n["batal"]),
         "porsi": porsi, "nota_menu": nota_menu, "omzet_menu": omzet_menu, "metode": metode,
         "omzet": omzet, "uang_masuk": omzet - metode.get("bon", 0), "porsi_total": sum(porsi.values())}
    if kas_awal is not None:
        h["seharusnya"] = kas_awal + metode.get("tunai", 0)
        if kas_fisik is not None:
            h["selisih"] = kas_fisik - h["seharusnya"]
    return h


def render_baris(n, gaya, rnd):
    bagian = []
    for nama, q in n["item"]:
        harga = MENU[nama]
        g = rnd.choice(["@", "=", "x", "rb"]) if gaya == "acak" else gaya
        if g == "@":
            bagian.append("%d %s @%s" % (q, nama, "{:,}".format(harga).replace(",", ".")))
        elif g == "=":
            bagian.append("%d %s = %s" % (q, nama, "{:,}".format(q * harga).replace(",", ".")))
        elif g == "x":
            bagian.append("%s x%d @%drb" % (nama, q, harga // 1000))
        else:
            bagian.append("%d %s %drb" % (q, nama, q * harga // 1000))
    bayar = {"tunai": "tunai", "qris": "QRIS", "transfer": "transfer BCA", "bon": "bon, bayar akhir bulan"}[n["bayar"]]
    pel = ""
    if n.get("pelanggan"):
        pel = " - %s (%s)" % n["pelanggan"]
    status = ""
    if n["batal"]:
        status = " - BATAL (salah input, diganti nota berikutnya)"
    elif n.get("pengganti"):
        status = " (pengganti nota %s yang batal)" % n["pengganti"]
    return "Nota %s%s: %s - %s%s" % (n["id"], pel, ", ".join(bagian), bayar, status)


def buat_notas(rnd, jumlah=14):
    notas = []
    for i in range(1, jumlah + 1):
        k = rnd.randint(1, 3)
        nama_menu = rnd.sample(sorted(MENU), k)
        item = [(m, rnd.randint(1, 4)) for m in nama_menu]
        n = {"id": "%03d" % i, "item": item, "bayar": rnd.choice(["tunai", "tunai", "qris", "transfer", "bon"]),
             "batal": False}
        if n["bayar"] in ("transfer", "bon"):
            n["pelanggan"] = rnd.choice(PELANGGAN)
        notas.append(n)
    # 1-2 nota batal, nota setelahnya = pengganti yang menyebut kata "batal"
    for idx in rnd.sample(range(0, jumlah - 1, 2), 2):
        notas[idx]["batal"] = True
        notas[idx]["bayar"] = "tunai"
        notas[idx].pop("pelanggan", None)
        notas[idx + 1]["pengganti"] = notas[idx]["id"]
    return notas


def jalankan(teks, *opsi):
    buf = io.StringIO()
    with redirect_stdout(buf):
        kode = R.main(["--teks", teks, "--json"] + list(opsi))
    return kode, json.loads(buf.getvalue())


class UjiRekapNota(unittest.TestCase):
    def cocokkan(self, out, h):
        self.assertEqual(out["nota_sah"], h["nota_sah"])
        self.assertEqual(sorted(out["nota_batal"]), h["batal"])
        self.assertEqual(out["omzet_tercatat"], h["omzet"])
        self.assertEqual(out["uang_masuk"], h["uang_masuk"])
        self.assertEqual(out["porsi_total"], h["porsi_total"])
        per_menu = {m["menu"]: m for m in out["menu"]}
        self.assertEqual(set(per_menu), set(h["porsi"]))
        for nama in h["porsi"]:
            self.assertEqual(per_menu[nama]["porsi"], h["porsi"][nama], nama)
            self.assertEqual(per_menu[nama]["nota"], h["nota_menu"][nama], nama)
            self.assertEqual(per_menu[nama]["omzet"], h["omzet_menu"][nama], nama)
        for k, v in h["metode"].items():
            self.assertEqual(out["per_metode"][k]["jumlah"], v, k)
        self.assertTrue(out["rupiah_lengkap"])

    def test_acak_berbagai_gaya(self):
        for seed in range(25):
            rnd = random.Random(seed)
            notas = buat_notas(rnd)
            for gaya in ("@", "=", "x", "rb", "acak"):
                teks = "\n".join(render_baris(n, gaya, rnd) for n in notas)
                kode, out = jalankan(teks, "--kas-awal", "300rb", "--kas-fisik", "500rb")
                self.assertEqual(kode, 0)
                h = harapan(notas, 300000, 500000)
                with self.subTest(seed=seed, gaya=gaya):
                    self.cocokkan(out, h)
                    self.assertEqual(out["kas"]["seharusnya"], h["seharusnya"])
                    self.assertEqual(out["kas"]["selisih"], h["selisih"])
                    self.assertEqual(out["perlu_dicek"], [])

    def test_teks_grup_tanpa_nama_nomor_bon_per_orang(self):
        rnd = random.Random(7)
        notas = buat_notas(rnd)
        notas[1]["bayar"], notas[1]["pelanggan"] = "bon", PELANGGAN[1]
        teks = "\n".join(render_baris(n, "@", rnd) for n in notas)
        _, out = jalankan(teks)
        g = out["teks_grup"]
        self.assertIn("RINGKASAN SIAP TEMPEL untuk grup", g)
        for nama, telp in PELANGGAN:
            self.assertNotIn(nama.split()[-1], g)
            self.assertNotIn(telp[-4:], g)
            # nama pelanggan juga tidak boleh bocor ke nama menu
            for m in out["menu"]:
                self.assertNotIn(nama.split()[-1], m["menu"])
        self.assertIn("Bon belum dibayar: ", g)
        self.assertIn("(dicatat pemilik)", g)
        for n in notas:
            if n["batal"]:
                self.assertNotIn(n["id"], g)  # nomor nota batal tidak dirinci di grup

    def test_kasus_uji_gabungan_kopi_susu(self):
        # Kasus nyata uji gabungan 2026-10-03: nota BATAL ikut terhitung -> "Kopi Susu 4x" (salah).
        teks = ("Nota 001: 2 Kopi Susu @18rb, 1 Roti Bakar Coklat @15rb - tunai\n"
                "Nota 003: 3 Kopi Susu = 54.000 - qris\n"
                "Nota 008: 2 Kopi Susu @18rb - tunai\n"
                "Nota 010 - Bu Rina 081398765432 - 2 Nasi Goreng Kampung @25rb - bon, bayar akhir bulan\n"
                "Nota 011: 1 Kopi Susu @18rb - tunai - BATAL (salah input, diganti nota 012)\n"
                "Nota 012: 1 Es Kopi Susu @20rb - tunai (pengganti nota 011 yang batal)\n")
        _, out = jalankan(teks, "--kas-awal", "300.000", "--kas-fisik", "390rb")
        ks = [m for m in out["menu"] if m["menu"] == "Kopi Susu"][0]
        self.assertEqual((ks["porsi"], ks["nota"], ks["omzet"]), (7, 3, 126000))  # 2+3+2 porsi, 3 nota
        self.assertEqual(out["nota_batal"], ["011"])
        self.assertEqual(out["nota_sah"], 5)
        self.assertEqual(out["omzet_tercatat"], 36000 + 15000 + 54000 + 36000 + 50000 + 20000)
        self.assertEqual(out["uang_masuk"], 36000 + 15000 + 54000 + 36000 + 20000)
        self.assertEqual(out["kas"]["seharusnya"], 300000 + 51000 + 36000 + 20000)
        self.assertEqual(out["kas"]["selisih"], 390000 - 407000)
        self.assertIn("Kopi Susu - 7 porsi (3 nota)", out["teks_grup"])
        self.assertIn("KURANG Rp 17.000", out["teks_grup"])
        self.assertNotIn("Rina", out["teks_grup"])
        self.assertNotIn("0813", out["teks_grup"])

    def test_blok_multibaris_dan_csv(self):
        teks = ("Nota hari ini:\n\nNota 001\n2 Kopi Susu @18rb\n1 Es Teh @6rb\ntunai\n\n"
                "Nota 002\nAmericano x2 = 30rb\nQRIS\n\nNota 003\n1 Kopi Susu @18rb\ntunai\nBATAL\n\n"
                "Stok: biji kopi 0,4 kg\n")
        _, out = jalankan(teks)
        self.assertEqual(out["nota_sah"], 2)
        self.assertEqual(out["nota_batal"], ["003"])
        self.assertEqual(out["omzet_tercatat"], 36000 + 6000 + 30000)
        self.assertEqual(out["per_metode"]["tunai"]["jumlah"], 42000)
        self.assertTrue(any("Stok" in d["teks"] for d in out["diabaikan"]))
        csvt = ("nota;menu;qty;harga;bayar;status;pelanggan\n001;Kopi Susu;2;18.000;tunai;;\n001;Es Teh;1;6000;tunai;;\n"
                "002;Nasi Goreng Kampung;2;25rb;bon;;Bu Rina\n003;Kopi Susu;1;18000;tunai;BATAL;\n")
        _, out = jalankan(csvt)
        self.assertEqual(out["sumber"], "csv")
        self.assertEqual(out["nota_batal"], ["003"])
        self.assertEqual(out["omzet_tercatat"], 92000)
        self.assertEqual(out["uang_masuk"], 42000)
        self.assertNotIn("Rina", out["teks_grup"])

    def test_input_buruk(self):
        kode, out = jalankan("halo kak")
        self.assertEqual(kode, 0)  # satu baris dianggap nota tanpa item -> perlu dicek
        self.assertTrue(out["perlu_dicek"])
        kode, out = jalankan("")
        self.assertEqual(kode, 1)
        self.assertFalse(out["ok"])
        kode, out = jalankan("Nota 1: 2 Kopi Susu - tunai")
        self.assertFalse(out["rupiah_lengkap"])
        self.assertTrue(any("harga" in p for p in out["perlu_dicek"]))
        kode, out = jalankan("Nota 1: 2 Kopi Susu @18rb", "--kas-fisik", "100rb")
        self.assertEqual(kode, 1)
        kode, out = jalankan("Nota 1: 2 Kopi Susu @18rb - tunai\nNota 2: 1 Kopi Susu 9rb - qris\nNota 2: 1 Es Teh @6rb - qris")
        self.assertTrue(any("berbeda" in p for p in out["perlu_dicek"]))
        self.assertTrue(any("lebih dari sekali" in p for p in out["perlu_dicek"]))
        kode, out = jalankan("Nota 1: 2 Kopi Susu @18rb - tunai", "--batal", "1")
        self.assertEqual(out["nota_batal"], ["1"])
        self.assertEqual(out["omzet_tercatat"], 0)

    def test_cli_stdin(self):
        p = subprocess.run([sys.executable, SCRIPT, "-", "--json"], input="Nota 1: 2 Es Teh @6rb - tunai\n",
                           capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(json.loads(p.stdout)["omzet_tercatat"], 12000)


if __name__ == "__main__":
    unittest.main(verbosity=1)
