#!/usr/bin/env python3
"""Uji regresi hitung_skema.py. Jalankan: python3 test_hitung_skema.py (hanya library standar)."""
import os
import random
import subprocess
import sys
import unittest
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hitung_skema as h  # noqa: E402

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hitung_skema.py")


def jalan(*args):
    return subprocess.run([sys.executable, SCRIPT, *args, "--format", "json"], capture_output=True, text=True)


class UjiSkenario(unittest.TestCase):
    def cek(self, teks, harapan, bulat=True):
        self.assertEqual([int(x) if bulat else x for x in h.parse_skenario(teks, "skenario", bulat)], harapan)

    def test_koma_banyak_dipisah(self):
        self.cek("10,20,30", [10, 20, 30])          # bug lama: terbaca 102030
        self.cek("5,10,15", [5, 10, 15])
        self.cek("50,100,200", [50, 100, 200])
        self.cek("10,25,50", [10, 25, 50], bulat=False)

    def test_titik_koma_dan_lainnya(self):
        self.cek("10;20;30", [10, 20, 30])
        self.cek("50 / 100", [50, 100])
        self.cek("10, 20", [10, 20])
        self.cek("10jt;25jt;50jt", [10**7, 25 * 10**6, 5 * 10**7], bulat=False)
        self.cek("10jt,25jt", [10**7, 25 * 10**6], bulat=False)
        self.cek("1,5jt;2,5jt", [1500000, 2500000], bulat=False)
        self.cek("Rp 7.777.777,50", [Decimal("7777777.50")], bulat=False)

    def test_ambigu_ditolak(self):
        for t in ("30,60", "2,5", "1,500"):
            with self.assertRaises(h.InputSalah):
                h.parse_skenario(t, "skenario", True)

    def test_cli_koma_tidak_diam_diam(self):
        r = jalan("konsinyasi", "--harga-jual", "25000", "--porsi-toko", "20%", "--skenario", "10,20,30")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('"unit_terjual": 30', r.stdout)
        self.assertNotIn("102030", r.stdout)
        r = jalan("konsinyasi", "--harga-jual", "25000", "--porsi-toko", "20%", "--skenario", "30,60")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("ambigu", r.stderr)


class UjiKonsinyasiPembulatan(unittest.TestCase):
    def test_toko_plus_pemilik_sama_dengan_omzet(self):
        acak = random.Random(7)
        for _ in range(500):
            hj = acak.randint(1000, 250000) + acak.choice([0, 0.5, 0.33])
            porsi = f"{acak.randint(1, 49)},{acak.randint(0, 9)}%"
            q = acak.randint(1, 999)

            class A:
                pass
            a = A()
            a.harga_jual, a.porsi_toko, a.harga_titip, a.modal = str(hj).replace(".", ","), porsi, None, None
            a.periode, a.skenario_v = "per bulan", [Decimal(q)]
            s = h.konsinyasi(a)["skenario"][0]
            self.assertEqual(s["bagian_toko"] + s["bagian_pemilik_barang"], s["omzet"])

    def test_contoh_penguji(self):
        r = jalan("konsinyasi", "--harga-jual", "12.345", "--porsi-toko", "15%", "--skenario", "2")
        self.assertIn('"omzet": 24690', r.stdout)
        self.assertIn('"bagian_toko": 3704', r.stdout)
        self.assertIn('"bagian_pemilik_barang": 20986', r.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
