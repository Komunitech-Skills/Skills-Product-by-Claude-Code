#!/usr/bin/env python3
"""Uji regresi buat_kalender.py. Jalankan: python3 uji_regresi.py (hanya library standar)."""
import json
import os
import subprocess
import sys
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "buat_kalender.py")


def jalan(*arg):
    r = subprocess.run([sys.executable, SCRIPT] + list(arg), capture_output=True, text=True, encoding="utf-8")
    return r


def kerangka(*arg):
    r = jalan(*(list(arg) + ["--format", "json"]))
    assert r.returncode == 0, r.stderr
    return json.loads(r.stdout)


class Uji(unittest.TestCase):
    def test_hari_dan_tanggal(self):
        d = kerangka("--mulai", "2026-10-01", "--hari", "31")
        self.assertEqual(len(d["baris"]), 31)
        self.assertEqual(d["baris"][0]["Hari"], "Kamis")
        self.assertEqual(d["baris"][-1]["Tanggal"], "2026-10-31")

    def test_tidak_ada_promo_di_peringatan_dan_tanggal_tua(self):
        for m in ("2026-09-01", "2026-10-01", "2026-11-01", "2026-12-01"):
            for b in kerangka("--mulai", m)["baris"]:
                if "peringatan" in b["Momen"] or "Tanggal tua" in b["Momen"]:
                    self.assertNotIn("promo", b["Pilar"].lower(), (b["Tanggal"], b["Momen"]))

    def test_promo_pengguna_di_hari_peringatan_diberitahu(self):
        d = kerangka("--mulai", "2026-11-01", "--momen", "2026-11-10:Diskon 10.11:promo")
        self.assertTrue(any("Diskon 10.11" in p for p in d["ringkasan"]["peringatan"]))

    def test_isi_memeriksa_promo_di_hari_peringatan(self):
        d = kerangka("--mulai", "2026-10-01", "--hari", "7")
        d["baris"][0]["Pilar"] = "Edukasi"
        d["baris"][0]["Ide Konten"] = "Diskon 50% semua menu"
        d["baris"][0]["Momen"] = ""
        f = os.path.join(tempfile.mkdtemp(), "isi.json")
        with open(f, "w", encoding="utf-8") as h:
            json.dump(d, h)
        r = jalan("--isi", f, "--format", "json")
        hasil = json.loads(r.stdout)
        self.assertTrue(any("hari peringatan" in p for p in hasil["ringkasan"]["peringatan"]))
        self.assertIn("Kesaktian Pancasila", hasil["baris"][0]["Momen"])

    def test_input_rusak(self):
        for arg in (["--mulai", "2026-13-01"], ["--hari", "3"], ["--pilar", "Promo"], ["--momen", "2026-10-10"],
                    ["--isi", "tidak-ada.json"]):
            self.assertEqual(jalan(*arg).returncode, 1, arg)


if __name__ == "__main__":
    unittest.main(verbosity=2)
