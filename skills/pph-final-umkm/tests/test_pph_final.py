"""Tes pph_final.py (v1.0.3: geser hari libur & jangka waktu tarif 0,5%). Jalankan dari folder skill:
python3 -m unittest discover -s tests -v"""
import datetime
import io
import json
import os
import sys
import unittest
from contextlib import redirect_stdout
from decimal import Decimal

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import pph_final as p  # noqa: E402

WARUNG = ["48jt", "45jt", "52jt", "70jt", "55jt", "50jt", "53jt", "58jt", "61jt", "60jt"]


def jalankan(*argv):
    buf = io.StringIO()
    with redirect_stdout(buf):
        kode = p.main(list(argv) + ["--format", "json"])
    return kode, json.loads(buf.getvalue()) if kode == 0 else None


class TesRevisi103(unittest.TestCase):
    def test_skenario_warung(self):
        kode, h = jalankan("--jenis", "op", "--tahun", "2026", "--tahun-terdaftar", "2021",
                           "--hari-ini", "2026-10-01", "--omzet", *WARUNG)
        self.assertEqual(kode, 0)
        okt = h["bulan"][9]
        self.assertEqual(okt["pph_final"], 260000)
        self.assertEqual(okt["setor_paling_lambat"], "2026-11-15")
        self.assertEqual(okt["setor_hari_kerja"], "2026-11-16")
        semua = " ".join(h["catatan"])
        self.assertIn("Senin 16 November 2026", semua)
        self.assertIn("PMK 81/2024 Pasal 100", semua)
        self.assertIn("s.d. tahun pajak 2027", semua)
        self.assertIn("PP 55/2022 Pasal 59", semua)
        self.assertFalse(any(b["batas_setor_sudah_lewat"] for b in h["bulan"]))

    def test_geser_libur_nasional_dan_cuti(self):
        # 15 Feb 2026 Minggu, 16 Feb cuti bersama Imlek, 17 Feb Imlek -> 18 Feb
        self.assertEqual(p.geser_hari_kerja(datetime.date(2026, 2, 15))[0], datetime.date(2026, 2, 18))
        # 15 Agu 2026 Sabtu, 17 Agu libur kemerdekaan -> 18 Agu
        self.assertEqual(p.geser_hari_kerja(datetime.date(2026, 8, 15))[0], datetime.date(2026, 8, 18))
        # hari kerja biasa tidak bergeser
        self.assertEqual(p.geser_hari_kerja(datetime.date(2026, 10, 15))[0], datetime.date(2026, 10, 15))
        # tahun tanpa data libur: hanya Sabtu/Minggu, ditandai tidak lengkap
        t, _, lengkap = p.geser_hari_kerja(datetime.date(2028, 1, 15))
        self.assertEqual(t, datetime.date(2028, 1, 17))
        self.assertFalse(lengkap)

    def test_jangka_waktu(self):
        self.assertIn("s.d. tahun pajak 2027", p.catatan_jangka_waktu("op", None, 2026, 2021))
        self.assertIn("TERAKHIR", p.catatan_jangka_waktu("op", None, 2027, 2021))
        self.assertIn("MELEWATI", p.catatan_jangka_waktu("op", None, 2028, 2021))
        self.assertIn("sejak 2018", p.catatan_jangka_waktu("op", None, 2024, 2015))
        self.assertIn("s.d. tahun pajak 2024", p.catatan_jangka_waktu("op", None, 2024, 2015))
        self.assertIn("3 tahun pajak", p.catatan_jangka_waktu("badan", "pt", 2026, 2025))
        self.assertIn("--tahun-terdaftar", p.catatan_jangka_waktu("op", None, 2026, None))

    def test_tahun_terdaftar_tidak_masuk_akal(self):
        kode, _ = jalankan("--tahun", "2026", "--tahun-terdaftar", "2030", "--omzet", "10jt")
        self.assertEqual(kode, 2)

    def test_hitungan_lama_tetap(self):
        kode, h = jalankan("--jenis", "op", "--tahun", "2026", "--hari-ini", "2026-09-23", "--omzet",
                           "45jt", "60jt", "80jt", "120jt", "150jt", "90jt", "70jt")
        self.assertEqual([b["pph_final"] for b in h["bulan"]][-2:], [225000, 350000])
        self.assertEqual(h["ringkasan"]["total_pph_final"], 575000)


if __name__ == "__main__":
    unittest.main()
