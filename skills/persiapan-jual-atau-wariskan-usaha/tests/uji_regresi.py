#!/usr/bin/env python3
"""Uji regresi nilai_usaha.py. Jalankan: python3 tests/uji_regresi.py (Windows: python / py)."""
import io
import json
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import nilai_usaha as n  # noqa: E402


def jalan(*arg):
    o, e = io.StringIO(), io.StringIO()
    with redirect_stdout(o), redirect_stderr(e):
        k = n.main(list(arg))
    return k, o.getvalue(), e.getvalue()


class Tes(unittest.TestCase):
    def test_rp(self):
        self.assertEqual(n.rp(1250000), "Rp1.250.000")
        self.assertEqual(n.rp(Decimal("0.5")), "Rp1")
        self.assertEqual(n.rp(-2000), "-Rp2.000")

    def test_kelipatan_manual(self):
        # normalisasi: +60jt -84jt +10jt = -14jt per tahun
        k, o, _ = jalan("--laba", "2023=120000000", "2024=150000000", "2025=180000000",
                        "--kelipatan", "2", "3", "--gaji-diambil", "60000000",
                        "--gaji-pengganti", "84000000", "--biaya-sekali", "10000000", "--json")
        self.assertEqual(k, 0)
        d = json.loads(o)
        # 106, 136, 166 jt -> rata 136jt; terakhir 166 > rata -> basis 136jt
        self.assertEqual(d["basis"], 136000000)
        self.assertEqual(d["rentang_bruto"], [272000000, 408000000])

    def test_terakhir_lebih_rendah(self):
        k, o, _ = jalan("--laba", "2023=200", "2024=200", "2025=100", "--kelipatan", "1", "2", "--json")
        d = json.loads(o)
        self.assertEqual(d["basis"], 100)
        self.assertTrue(any("terakhir" in p for p in d["peringatan"]))

    def test_aset_dan_gabungan(self):
        k, o, _ = jalan("--laba", "2025=100000000", "--kelipatan", "1", "2", "--aset", "300000000",
                        "--utang", "80000000", "--penyesuaian-aset", "20", "--diskon-pemilik", "10",
                        "--biaya-transaksi", "5", "--kebutuhan-bulanan", "10000000", "--bulan", "12", "--json")
        d = json.loads(o)
        self.assertEqual(d["aset_bersih"], 160000000)  # 300*0.8-80
        self.assertEqual(d["metode"][0]["rendah"], 90000000)  # 100jt*1*0.9
        self.assertEqual(d["metode"][0]["tinggi"], 180000000)
        self.assertEqual(d["rentang_bruto"], [90000000, 180000000])
        self.assertEqual(d["rentang_bersih"], [85500000, 171000000])
        self.assertEqual(d["selisih_vs_kebutuhan"], [-34500000, 51000000])

    def test_rugi_dan_utang_besar(self):
        k, o, _ = jalan("--laba", "2025=-5000000", "--kelipatan", "2", "3", "--aset", "10000000", "--utang", "30000000", "--json")
        self.assertEqual(k, 0)
        d = json.loads(o)
        self.assertLess(d["aset_bersih"], 0)
        self.assertTrue(len(d["peringatan"]) >= 2)

    def test_kelipatan_wajib(self):
        k, _, e = jalan("--laba", "2025=100")
        self.assertEqual(k, 2)
        self.assertIn("kelipatan wajib", e)

    def test_ilustrasi_diberi_label(self):
        k, o, e = jalan("--laba", "2025=1000", "--ilustrasi")
        self.assertEqual(k, 0)
        self.assertIn("ILUSTRASI", e)
        self.assertIn("ASUMSI", o)

    def test_input_rusak(self):
        for arg in (["--laba", "abc"], ["--laba", "2025=xx", "--kelipatan", "1"], ["--laba", "2025=1", "2025=2", "--kelipatan", "1"],
                    ["--laba", "2025=1", "--kelipatan", "0"], ["--laba", "2025=1", "--kelipatan", "-2"],
                    ["--aset", "-5"], ["--aset", "5", "--penyesuaian-aset", "150"], [], ["--aset", "nan"],
                    ["--aset", "5", "--bulan", "12"]):
            k, _, e = jalan(*arg)
            self.assertEqual(k, 2, arg)
            self.assertIn("GAGAL", e)

    def test_hanya_aset(self):
        k, o, _ = jalan("--aset", "50000000", "--utang", "10000000")
        self.assertEqual(k, 0)
        self.assertIn("Rp40.000.000", o)


if __name__ == "__main__":
    unittest.main()
