#!/usr/bin/env python3
"""Uji regresi hitung_sph.py. Jalankan: python3 test_hitung_sph.py (hanya library standar)."""
import json
import os
import random
import subprocess
import sys
import unittest
from decimal import Decimal, ROUND_FLOOR

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hitung_sph.py")


def jalan(*args):
    r = subprocess.run([sys.executable, SCRIPT, *args, "--format", "json", "--tanggal", "2026-09-23"],
                       capture_output=True, text=True)
    return r.returncode, (json.loads(r.stdout) if r.returncode == 0 else r.stderr)


class UjiPPN(unittest.TestCase):
    def test_ppn_dibulatkan_ke_bawah(self):
        kode, h = jalan("--item", "A|1|pcs|Rp 1.000.005", "--ppn", "pkp")
        self.assertEqual(kode, 0)
        self.assertEqual(h["ppn"], 110000)          # 110.000,55 -> ke bawah (bukan 110.001)
        self.assertEqual(h["total"], 1110005)

    def test_ppn_acak_sesuai_rumus(self):
        acak = random.Random(11)
        for _ in range(60):
            harga = acak.randint(1000, 50_000_000)
            kode, h = jalan("--item", f"A|1|pcs|{harga}", "--ppn", "pkp")
            harap = int((Decimal(harga) * Decimal(11) / 100).quantize(Decimal(1), ROUND_FLOOR))
            self.assertEqual(h["ppn"], harap, harga)

    def test_contoh_skill(self):
        kode, h = jalan("--item", "Kursi kantor ergonomis|10|unit|Rp 1.250.000|5%", "--item", "Meja kerja 120x60|10|unit|Rp 950.000",
                        "--diskon-total", "Rp 250.000", "--ongkir", "Rp 300.000", "--ppn", "pkp")
        self.assertEqual((h["dpp"], h["ppn"], h["total"]), (21425000, 2356750, 23781750))
        self.assertTrue(h["asumsi_wajib_disebut"])     # ongkir ikut DPP wajib disebut

    def test_termasuk_ppn_ongkir_tidak_dipotong(self):
        kode, h = jalan("--item", "Jasa|1|paket|Rp 11.100.000", "--ongkir", "100000", "--ppn", "pkp", "--harga-termasuk-ppn")
        self.assertEqual((h["dpp"], h["ppn"], h["total"]), (10100000, 1111000, 11211000))

    def test_termasuk_ppn_dpp_terbesar(self):
        acak = random.Random(5)
        for _ in range(60):
            harga = acak.randint(1000, 20_000_000)
            kode, h = jalan("--item", f"A|1|pcs|{harga}", "--ppn", "pkp", "--harga-termasuk-ppn")
            dpp, ppn = h["dpp"], h["ppn"]
            self.assertLessEqual(dpp + ppn, harga)
            lebih = dpp + 1
            self.assertGreater(lebih + int((Decimal(lebih) * Decimal("0.11")).quantize(Decimal(1), ROUND_FLOOR)), harga)


class UjiRedaksiNonPKP(unittest.TestCase):
    def test_catatan_non_pkp_tidak_menyesatkan(self):
        r = subprocess.run([sys.executable, SCRIPT, "--item", "Jasa|1|paket|Rp 7.500.000", "--tanggal", "2026-10-01"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)
        low = r.stdout.lower()
        self.assertIn("bukan pkp", low)
        self.assertNotIn("belum kena", low)
        self.assertNotIn("belum termasuk ppn", low)


class UjiInput(unittest.TestCase):
    def test_angka_format_indonesia(self):
        kode, h = jalan("--item", "Kaos|12|pcs|Rp 85.000,-")
        self.assertEqual(h["total"], 1020000)

    def test_ambigu_dan_rusak(self):
        for item in ("A|1|pcs|1.500rb", "A|0|pcs|1000", "A|1|pcs|abc", "A|2"):
            kode, _ = jalan("--item", item)
            self.assertNotEqual(kode, 0, item)


if __name__ == "__main__":
    unittest.main(verbosity=2)
