#!/usr/bin/env python3
"""Regresi rapikan_draf.py & buat_docx.py. python3 tests/uji_regresi.py"""
import os
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import buat_docx  # noqa: E402
import rapikan_draf as rd  # noqa: E402


class Rapikan(unittest.TestCase):
    def test_bersihkan_meta(self):
        t = "Tentu!\n\n- poin satu\n\n\n\n- poin dua"
        out = rd.bersihkan(t)
        self.assertNotIn("Tentu", out)
        self.assertIn("poin satu", out)

    def test_deteksi_notulen(self):
        self.assertEqual(rd.deteksi_jenis("Agenda rapat dan tindak lanjut"), "notulen")

    def test_deteksi_umum(self):
        self.assertEqual(rd.deteksi_jenis("halo dunia"), "umum")


class Docx(unittest.TestCase):
    def test_buat_docx_zip(self):
        md = "# Judul\n\nParagraf **tebal**.\n\n| A | B |\n|---|---|\n| 1 | 2 |\n"
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "t.docx")
            buat_docx.buat_docx(md, path)
            self.assertTrue(os.path.isfile(path))
            with zipfile.ZipFile(path) as z:
                self.assertIn("word/document.xml", z.namelist())
                xml = z.read("word/document.xml").decode("utf-8")
            self.assertIn("Judul", xml)
            self.assertIn("Paragraf", xml)


if __name__ == "__main__":
    unittest.main()
