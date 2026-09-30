#!/usr/bin/env python3
"""Uji regresi scripts/susun_pesan.py (format Rupiah dari teks gaya Indonesia).

Jalankan: python3 tests/uji_regresi.py   (Windows: python / py)
"""
import json
import os
import subprocess
import sys
import unittest

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(AKAR, "scripts", "susun_pesan.py")
sys.path.insert(0, os.path.join(AKAR, "scripts"))
import susun_pesan as sp  # noqa: E402


def jalan(data):
    p = subprocess.run([sys.executable, SCRIPT], input=json.dumps(data), capture_output=True, text=True,
                       encoding="utf-8")
    return p.returncode, p.stdout, p.stderr


class FormatRupiah(unittest.TestCase):
    """Audit format angka 2026-09-30: "38.000" dulu tercetak "Rp 38" dan "1.500" tercetak "Rp 2"."""

    def test_angka_json_tetap(self):
        self.assertEqual(sp.format_rupiah(4500000), "Rp 4.500.000")
        self.assertEqual(sp.format_rupiah(-150000), "-Rp 150.000")
        self.assertEqual(sp.format_rupiah(1250000.4), "Rp 1.250.000")

    def test_teks_format_indonesia(self):
        for teks, harap in (("38.000", "Rp 38.000"), ("1.500", "Rp 1.500"), ("Rp38.000", "Rp 38.000"),
                            ("Rp 38.000", "Rp 38.000"), ("Rp 1.250.000", "Rp 1.250.000"),
                            ("1.250.000,50", "Rp 1.250.001"), ("38000", "Rp 38.000"), ("38rb", "Rp 38.000"),
                            ("1,5jt", "Rp 1.500.000"), ("-Rp5.000", "-Rp 5.000"), ("38000.5", "Rp 38.001")):
            self.assertEqual(sp.format_rupiah(teks), harap, teks)

    def test_teks_ragu_ditolak(self):
        for teks in ("38.5", "1,5", "1,500", "abc", "", None, True):
            with self.assertRaises(ValueError, msg=repr(teks)):
                sp.format_rupiah(teks)

    def test_nan_inf_ditolak_rapi(self):
        for x in (float("nan"), float("inf")):
            with self.assertRaises(ValueError):
                sp.format_rupiah(x)


class Cli(unittest.TestCase):
    def test_teks_bertitik_tercetak_benar(self):
        kode, out, err = jalan({"judul": "T", "baris": [{"label": "Omzet", "nilai": "38.000", "rupiah": True},
                                                        {"label": "Biaya", "nilai": "Rp 1.250.000", "rupiah": True},
                                                        {"label": "Transaksi", "nilai": 32}]})
        self.assertEqual(kode, 0, err)
        self.assertIn("Omzet: Rp 38.000", out)
        self.assertIn("Biaya: Rp 1.250.000", out)
        self.assertIn("Transaksi: 32", out)

    def test_teks_ragu_gagal_tanpa_pesan(self):
        kode, out, err = jalan({"judul": "T", "baris": [{"label": "Omzet", "nilai": "38.5", "rupiah": True}]})
        self.assertEqual(kode, 1)
        self.assertEqual(out, "")
        self.assertIn("meragukan", err)
        self.assertIn("Omzet", err)


if __name__ == "__main__":
    unittest.main(verbosity=2)
