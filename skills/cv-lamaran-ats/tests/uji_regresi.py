#!/usr/bin/env python3
"""Uji regresi ringan untuk skor_kecocokan.py (cv-lamaran-ats).

Jalankan: python3 tests/uji_regresi.py
Hanya memakai library standar Python.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import skor_kecocokan as sk  # noqa: E402


class TesStopwordsFiller(unittest.TestCase):
    def test_stopword_baru_v1_1_1_tidak_muncul(self):
        teks = ("Kandidat yang jujur dan dipersilakan melamar untuk posisi ini. "
                "Silakan kirim CV jika berminat.")
        kk = sk.ekstrak_kata_kunci(teks)
        for kata in ("jujur", "dipersilakan", "melamar", "silakan"):
            self.assertNotIn(kata, kk, f"'{kata}' seharusnya jadi stopword, malah lolos jadi kata kunci")

    def test_kata_bermakna_tetap_lolos(self):
        teks = "Dibutuhkan kandidat menguasai Python dan SQL untuk analisis data penjualan."
        kk = sk.ekstrak_kata_kunci(teks)
        self.assertIn("python", kk)
        self.assertIn("sql", kk)
        self.assertIn("penjualan", kk)


if __name__ == "__main__":
    unittest.main()
