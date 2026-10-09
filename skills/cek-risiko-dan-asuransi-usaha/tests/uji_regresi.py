#!/usr/bin/env python3
"""Uji regresi cek_risiko.py. Jalankan: python3 tests/uji_regresi.py (Windows: python / py)."""
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import cek_risiko as c  # noqa: E402


def jalan(*arg):
    o, e = io.StringIO(), io.StringIO()
    with redirect_stdout(o), redirect_stderr(e):
        k = c.main(list(arg))
    return k, o.getvalue(), e.getvalue()


def tmp_json(obj, mentah=None):
    p = os.path.join(tempfile.mkdtemp(), "r.json")
    with open(p, "w", encoding="utf-8") as f:
        f.write(mentah if mentah is not None else json.dumps(obj))
    return p


class Tes(unittest.TestCase):
    def test_skor_dan_tingkat(self):
        h = c.hitung_risiko([{"nama": "A", "kemungkinan": 2, "dampak": 5},
                             {"nama": "B", "kemungkinan": 5, "dampak": 3},
                             {"nama": "C", "kemungkinan": 1, "dampak": 2}])
        self.assertEqual([(x["nama"], x["skor"], x["tingkat"]) for x in h],
                         [("B", 15, "KRITIS"), ("A", 10, "TINGGI"), ("C", 2, "RENDAH")])

    def test_batas_tingkat(self):
        self.assertEqual([c.tingkat(s) for s in (1, 4, 5, 9, 10, 14, 15, 25)],
                         ["RENDAH", "RENDAH", "SEDANG", "SEDANG", "TINGGI", "TINGGI", "KRITIS", "KRITIS"])

    def test_respons(self):
        self.assertEqual(c.respons(2, 2, 4)[1], "Tidak")
        self.assertEqual(c.respons(2, 5, 10)[1], "Ya, pertimbangkan")
        self.assertEqual(c.respons(4, 5, 20)[1], "Ya, setelah dikurangi")
        self.assertEqual(c.respons(4, 3, 12)[1], "Tidak perlu")
        # kerugian melebihi dana darurat -> dianggap besar
        self.assertEqual(c.respons(2, 3, 6, 50_000_000, 20_000_000)[1], "Ya, pertimbangkan")
        self.assertEqual(c.respons(2, 3, 6, 10_000_000, 20_000_000)[1], "Tidak perlu")

    def test_dana(self):
        o = c.hitung_dana({"sewa": 3_000_000, "gaji": 8_500_000, "listrik": 750_000}, 3, 10_000_000)
        self.assertEqual(o["biaya_tetap_bulanan"], 12_250_000)
        self.assertEqual(o["target"], 36_750_000)
        self.assertEqual(o["kekurangan"], 26_750_000)
        self.assertEqual(o["tercukupi_bulan"], 0.8)
        self.assertEqual(c.hitung_dana({"a": 1}, 6, 99)["kekurangan"], 0)

    def test_parse_biaya(self):
        self.assertEqual(c.parse_biaya("Sewa=3.000.000, Gaji=8500000"), {"Sewa": 3000000, "Gaji": 8500000})
        with self.assertRaises(ValueError):
            c.parse_biaya("Sewa=abc")
        with self.assertRaises(ValueError):
            c.parse_biaya("Sewa")

    def test_rp(self):
        self.assertEqual(c.rp(1250000), "Rp1.250.000")
        self.assertEqual(c.rp(0), "Rp0")

    def test_data_rusak(self):
        for bad in ([{"nama": "A", "kemungkinan": 0, "dampak": 3}],
                    [{"nama": "A", "kemungkinan": 6, "dampak": 3}],
                    [{"nama": "A", "kemungkinan": "tinggi", "dampak": 3}],
                    [{"nama": "", "kemungkinan": 1, "dampak": 1}],
                    [{"nama": "A", "kemungkinan": True, "dampak": 1}],
                    [{"nama": "A", "kemungkinan": 1, "dampak": 1, "kerugian_rp": -5}],
                    [], "bukan list"):
            with self.assertRaises(ValueError):
                c.hitung_risiko(bad)
        with self.assertRaises(ValueError):
            c.hitung_dana({"a": -1}, 3)
        with self.assertRaises(ValueError):
            c.hitung_dana({}, 3)
        with self.assertRaises(ValueError):
            c.hitung_dana({"a": 1}, 0)

    def test_cli(self):
        k, o, _ = jalan("risiko", tmp_json([{"nama": "Kebakaran", "kemungkinan": 2, "dampak": 5}]))
        self.assertEqual(k, 0)
        self.assertIn("| 1 | Kebakaran | 2 | 5 | 10 | TINGGI |", o)
        k, o, _ = jalan("dana", "--biaya", "Sewa=2000000,Gaji=4000000", "--bulan", "6", "--kas", "10000000")
        self.assertEqual(k, 0)
        self.assertIn("Rp6.000.000", o)
        self.assertIn("Rp36.000.000", o)
        self.assertIn("Kekurangan: Rp26.000.000", o)

    def test_cli_berkas_rusak(self):
        k, _, e = jalan("risiko", tmp_json(None, "{rusak"))
        self.assertEqual(k, 2)
        self.assertIn("tidak valid", e)
        k, _, e = jalan("risiko", "/tidak/ada.json")
        self.assertEqual(k, 2)


if __name__ == "__main__":
    unittest.main()
