#!/usr/bin/env python3
"""Uji regresi hitung_harga.py. Jalankan: python3 tests/uji_regresi.py (Windows: python / py)."""
import io
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import hitung_harga as h  # noqa: E402


def jalan(*argv):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        kode = h.main(list(argv))
    return kode, out.getvalue(), err.getvalue()


class TesBacaAngka(unittest.TestCase):
    def test_format_indonesia(self):
        kasus = {"129000": 129000, "129.000": 129000, "Rp129.000": 129000, "Rp. 129.000": 129000,
                 "129rb": 129000, "1,5jt": 1500000, "1.5 juta": 1500000, "1.500.000,50": Decimal("1500000.50"),
                 "75k": 75000, "0,5": Decimal("0.5")}
        for teks, harapan in kasus.items():
            with self.subTest(teks=teks):
                self.assertEqual(h._angka(teks, "x"), Decimal(str(harapan)))

    def test_masukan_rusak(self):
        for teks in ["", "abc", "-5000", "0", "1.2.3", "Rp", "1e9", "99999999999999"]:
            with self.subTest(teks=teks):
                with self.assertRaises(h.MasukanSalah):
                    h._angka(teks, "x")

    def test_tenor_harus_bulat(self):
        with self.assertRaises(h.MasukanSalah):
            h._angka("2,5", "t", boleh_desimal=False)


class TesPerPakai(unittest.TestCase):
    def test_setahun(self):
        kode, out, _ = jalan("per-pakai", "--harga", "129000", "--umur", "1", "--satuan", "tahun")
        self.assertEqual(kode, 0)
        self.assertIn("Per hari: Rp353", out)
        self.assertIn("Per bulan (30 hari): Rp10.603", out)

    def test_per_pemakaian(self):
        _, out, _ = jalan("per-pakai", "--harga", "300rb", "--umur", "20", "--satuan", "pakai")
        self.assertIn("Per pemakaian: Rp15.000", out)

    def test_pembulatan_setengah_ke_atas(self):
        self.assertEqual(h.rp(Decimal("2.5")), "Rp3")
        self.assertEqual(h.rp(Decimal("2.4999")), "Rp2")


class TesBandingkan(unittest.TestCase):
    def test_kita_lebih_murah_setelah_ongkir(self):
        _, out, _ = jalan("bandingkan", "--harga-kita", "420000", "--pakai-kita", "1000",
                          "--harga-lain", "400000", "--pakai-lain", "1000", "--tambahan-lain", "50000")
        self.assertIn("kita lebih murah Rp30 per unit (6,6%", out)
        self.assertNotIn("Jujur saja", out)

    def test_pesaing_lebih_murah_jujur(self):
        _, out, _ = jalan("bandingkan", "--harga-kita", "2100000", "--pakai-kita", "5000",
                          "--harga-lain", "2000000", "--pakai-lain", "5000", "--tambahan-lain", "50000")
        self.assertIn("pesaing lebih murah Rp10 per unit (2,3%", out)
        self.assertIn("Jujur saja", out)

    def test_sama(self):
        _, out, _ = jalan("bandingkan", "--harga-kita", "1000", "--pakai-kita", "1",
                          "--harga-lain", "1000", "--pakai-lain", "1")
        self.assertIn("sama per unit", out)

    def test_persen_dibulatkan_ke_bawah(self):
        self.assertEqual(h.persen_bawah(Decimal("6.67")), "6,6%")
        self.assertEqual(h.persen_bawah(Decimal("22.99")), "22,9%")


class TesCicil(unittest.TestCase):
    def test_sisa_masuk_cicilan_terakhir(self):
        _, out, _ = jalan("cicil", "--harga", "3600000", "--tenor", "7", "--dp", "600000")
        self.assertIn("Rp428.571 per bulan x 6, bulan terakhir Rp428.574", out)
        self.assertIn("Total dibayar: Rp3.600.000", out)

    def test_pas(self):
        _, out, _ = jalan("cicil", "--harga", "1,2jt", "--tenor", "6")
        self.assertIn("Rp200.000 per bulan x 6", out)

    def test_tenor_dan_dp_salah(self):
        for argv in (["cicil", "--harga", "1000000", "--tenor", "0"],
                     ["cicil", "--harga", "1000000", "--tenor", "61"],
                     ["cicil", "--harga", "1000000", "--tenor", "3", "--dp", "1000000"],
                     ["cicil", "--harga", "1000000", "--tenor", "3,5"]):
            with self.subTest(argv=argv):
                kode, _, err = jalan(*argv)
                self.assertEqual(kode, 2)
                self.assertIn("Masukan tidak valid", err)


class TesDataRusak(unittest.TestCase):
    def test_pesan_ramah_bukan_traceback(self):
        for argv in (["per-pakai", "--harga", "abc", "--umur", "1", "--satuan", "hari"],
                     ["per-pakai", "--harga", "1000", "--umur", "0", "--satuan", "hari"],
                     ["bandingkan", "--harga-kita", "-1", "--pakai-kita", "1", "--harga-lain", "1", "--pakai-lain", "1"]):
            with self.subTest(argv=argv):
                kode, _, err = jalan(*argv)
                self.assertEqual(kode, 2)
                self.assertTrue(err.startswith("Masukan tidak valid"))


if __name__ == "__main__":
    unittest.main(verbosity=1)
