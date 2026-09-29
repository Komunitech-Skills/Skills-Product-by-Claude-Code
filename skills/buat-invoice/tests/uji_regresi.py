#!/usr/bin/env python3
"""Uji regresi buat-invoice. Jalankan: python3 tests/uji_regresi.py  (Windows: py tests/uji_regresi.py)

Fokus: penomoran (nomor baru = nomor terakhir + 1, aturan ganti bulan/tahun) dan data yang tidak diberikan
(kota, penanda tangan) tidak pernah dikarang -> placeholder [isi ...].
Angka invoice contoh (templates/contoh-invoice.json), dihitung manual:
  100 x 65.000 = 6.500.000; diskon 5% = 325.000 -> 6.175.000; + desain 500.000 = 6.675.000
  + ongkir 75.000 = 6.750.000; DP 3.000.000 -> sisa 3.750.000.
"""
import contextlib
import copy
import datetime
import io
import json
import os
import shutil
import sys
import tempfile
import unittest

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AKAR, "scripts"))
sys.dont_write_bytecode = True
import buat_invoice as B  # noqa: E402

with open(os.path.join(AKAR, "templates", "contoh-invoice.json"), encoding="utf-8") as _f:
    CONTOH = json.load(_f)

D = datetime.date


class UjiNomor(unittest.TestCase):
    def n(self, terakhir, tgl=None, lanjut=False):
        return B.nomor_berikutnya(terakhir, tgl, lanjut)[0]

    def test_bulan_sama_plus_satu(self):
        # kasus uji OpenClaw: terakhir 0012 -> baru 0013 (bukan 0012 dobel)
        self.assertEqual(self.n("INV/2026/09/0012", D(2026, 9, 29)), "INV/2026/09/0013")
        self.assertEqual(self.n("INV/2026/09/0007", D(2026, 9, 1)), "INV/2026/09/0008")

    def test_tanpa_tanggal_plus_satu(self):
        self.assertEqual(self.n("INV/2026/09/0012"), "INV/2026/09/0013")
        self.assertEqual(self.n("INV-0099"), "INV-0100")
        self.assertEqual(self.n("12"), "13")

    def test_nol_depan_dan_melebar(self):
        self.assertEqual(self.n("INV/2026/09/0009", D(2026, 9, 5)), "INV/2026/09/0010")
        self.assertEqual(self.n("INV/2026/09/9999", D(2026, 9, 5)), "INV/2026/09/10000")

    def test_ganti_bulan_mulai_satu(self):
        baru, ket = B.nomor_berikutnya("INV/2026/09/0012", D(2026, 10, 2))
        self.assertEqual(baru, "INV/2026/10/0001")
        self.assertIn("Periode berganti", ket)
        self.assertIn("--urut-lanjut", ket)

    def test_ganti_bulan_urut_lanjut(self):
        self.assertEqual(self.n("INV/2026/09/0012", D(2026, 10, 2), True), "INV/2026/10/0013")

    def test_ganti_tahun(self):
        self.assertEqual(self.n("INV/2026/12/0045", D(2027, 1, 3)), "INV/2027/01/0001")
        self.assertEqual(self.n("INV-2026-0045", D(2027, 1, 3)), "INV-2027-0001")
        self.assertEqual(self.n("INV-2026-0045", D(2026, 11, 3)), "INV-2026-0046")  # nomor tahunan, bulan tak berpengaruh

    def test_format_romawi_urut_di_depan(self):
        # tahun paling kanan TIDAK boleh ikut dinaikkan (bug lama: 2026 -> 2027)
        self.assertEqual(self.n("012/INV/IX/2026", D(2026, 9, 29)), "013/INV/IX/2026")
        self.assertEqual(self.n("012/INV/IX/2026", D(2026, 10, 1)), "001/INV/X/2026")
        self.assertEqual(self.n("012/INV/IX/2026"), "013/INV/IX/2026")

    def test_tanggal_mundur_error(self):
        with self.assertRaises(ValueError):
            B.nomor_berikutnya("INV/2026/09/0012", D(2026, 8, 31))

    def test_tanpa_angka_error(self):
        for s in ("INV/ABC", "", "2026"):
            with self.assertRaises(ValueError):
                B.nomor_berikutnya(s, D(2026, 9, 1))


class UjiCLI(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def jalan(self, data, *argv):
        f = os.path.join(self.dir, "inv.json")
        with open(f, "w", encoding="utf-8") as fh:
            json.dump(data, fh)
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            kode = B.main(["--file", f] + list(argv))
        return kode, out.getvalue(), err.getvalue()

    def test_contoh_angka_dan_nomor(self):
        kode, out, _ = self.jalan(CONTOH, "--nomor-terakhir", "INV/2026/09/0012")
        self.assertEqual(kode, 0)
        self.assertIn("**No.:** INV/2026/09/0013", out)
        self.assertIn("Nomor terakhir dibaca: INV/2026/09/0012 -> nomor baru: INV/2026/09/0013", out)
        self.assertIn("Rp 6.750.000", out)
        self.assertIn("Rp 3.750.000", out)
        self.assertIn("Bandung, 23 September 2026", out)
        self.assertNotIn("[isi", out)

    def test_json_nomor(self):
        kode, out, _ = self.jalan(CONTOH, "--nomor-terakhir", "INV/2026/08/0030", "--format", "json")
        self.assertEqual(kode, 0)
        h = json.loads(out)
        self.assertEqual(h["nomor"], "INV/2026/09/0001")
        self.assertIn("Periode berganti", h["keterangan_nomor"])
        self.assertEqual(h["perlu_diisi"], [])

    def test_nomor_mundur_exit2(self):
        kode, _, err = self.jalan(CONTOH, "--nomor-terakhir", "INV/2026/10/0003")
        self.assertEqual(kode, 2)
        self.assertIn("tidak boleh mundur", err)

    def test_kota_dan_penanda_tangan_tidak_dikarang(self):
        d = copy.deepcopy(CONTOH)
        d["tanda_tangan"] = {}
        html_path = os.path.join(self.dir, "inv.html")
        kode, out, _ = self.jalan(d, "--html", html_path)
        self.assertEqual(kode, 0)
        self.assertIn("[isi kota], 23 September 2026", out)
        self.assertIn("**[isi nama penanda tangan]**", out)
        self.assertIn("PERLU DIISI: kota, nama penanda tangan", out)
        with open(html_path, encoding="utf-8") as fh:
            isi = fh.read()
        self.assertIn("[isi kota], 23 September 2026", isi)
        self.assertIn("[isi nama penanda tangan]", isi)
        for karangan in ("Jakarta, 23", "Rina"):
            self.assertNotIn(karangan, out)

    def test_tanpa_tanda_tangan_sama_sekali(self):
        d = copy.deepcopy(CONTOH)
        del d["tanda_tangan"]
        kode, out, _ = self.jalan(d, "--format", "json")
        self.assertEqual(kode, 0)
        self.assertEqual(json.loads(out)["perlu_diisi"], ["kota", "nama penanda tangan"])

    def test_nomor_manual_menang(self):
        d = copy.deepcopy(CONTOH)
        d["nomor"] = "INV/2026/09/0050"
        kode, out, _ = self.jalan(d, "--nomor-terakhir", "INV/2026/09/0012")
        self.assertEqual(kode, 0)
        self.assertIn("**No.:** INV/2026/09/0050", out)


if __name__ == "__main__":
    unittest.main(verbosity=1)
