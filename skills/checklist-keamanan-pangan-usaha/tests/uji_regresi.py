#!/usr/bin/env python3
"""Uji regresi cek_log_suhu.py. Jalankan: python3 tests/uji_regresi.py (Windows: python / py)."""
import os
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import cek_log_suhu as c  # noqa: E402

D = date(2026, 10, 6)


def tulis(isi):
    d = tempfile.mkdtemp()
    p = os.path.join(d, "log.csv")
    with open(p, "w", encoding="utf-8") as f:
        f.write(isi)
    return p


class Uji(unittest.TestCase):
    def test_kulkas_zona_bahaya(self):
        h = c.analisis(tulis("2026-10-06 08:00,kulkas 1,4\n2026-10-06 10:00,kulkas 1,8\n2026-10-06 13:00,kulkas 1,9\n2026-10-06 14:00,kulkas 1,4\n"), D)
        p = h["pelanggaran"][0]
        self.assertEqual(p["menit"], 240)
        self.assertTrue(p["lewat_2_jam"])
        self.assertEqual(p["suhu"], 9.0)

    def test_batas_tepat_lolos(self):
        h = c.analisis(tulis("2026-10-06 08:00,kulkas,5\n2026-10-06 09:00,freezer,-18\n2026-10-06 10:00,penahan panas,60\n2026-10-06 11:00,pemanasan ulang,74\n"), D)
        self.assertEqual(h["pelanggaran"], [])

    def test_freezer_dan_masak(self):
        h = c.analisis(tulis("2026-10-06 08:00,freezer,-15\n2026-10-06 09:00,masak ayam,70\n2026-10-06 09:30,masak ayam,72\n2026-10-06 10:00,masak ikan,64\n"), D)
        alat = {(p["alat"], p["suhu"]) for p in h["pelanggaran"]}
        self.assertIn(("freezer", -15.0), alat)
        self.assertEqual(sum(1 for p in h["pelanggaran"] if p["alat"] == "freezer"), 1)
        self.assertIn(("masak ayam", 72.0), alat)
        self.assertNotIn(("masak ikan", 64.0), alat)

    def test_koma_desimal_dan_derajat(self):
        h = c.analisis(tulis('2026-10-06 08:00,kulkas,"4,5 C"\n2026-10-06 09:00,kulkas,6.2°\n'), D)
        self.assertEqual(h["alat"]["kulkas"]["pembacaan_melanggar"], 1)

    def test_data_rusak(self):
        h = c.analisis(tulis("waktu,alat,suhu\nkemarin,kulkas,4\n2026-10-06 08:00,kulkas,abc\n2026-10-06 08:00,,4\nx\n2026-10-06 08:00,kulkas,nan\n2026-10-06 08:00,kulkas,9999\n\n"), D)
        self.assertEqual(h["baris_ok"], 0)
        self.assertEqual(len(h["baris_rusak"]), 6)
        self.assertIn("Tidak ada pelanggaran", c.teks(h))

    def test_alat_tak_dikenal_dan_jam_saja(self):
        h = c.analisis(tulis("08:00,mesin es,3\n09:00,kulkas,7\n"), D)
        self.assertEqual(h["alat_tak_dikenal"], ["mesin es"])
        self.assertEqual(len(h["pelanggaran"]), 1)

    def test_belum_pulih(self):
        h = c.analisis(tulis("2026-10-06 08:00,kulkas,4\n2026-10-06 09:00,kulkas,7\n2026-10-06 09:45,kulkas,8\n"), D)
        p = h["pelanggaran"][0]
        self.assertEqual(p["menit"], 45)
        self.assertFalse(p["pulih"])
        self.assertIn("belum terlihat pulih", c.teks(h))

    def test_berkas_hilang(self):
        with self.assertRaises(SystemExit):
            c.analisis("/tidak/ada.csv", D)


if __name__ == "__main__":
    unittest.main()
