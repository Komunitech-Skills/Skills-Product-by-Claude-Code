#!/usr/bin/env python3
"""Uji kecil untuk scripts/hitung_perubahan.py — fokus kasus nilai lama negatif
(Temuan #1, uji independen v1.0.0) dan pembulatan dasar.

Jalankan: python3 tests/uji_hitung_perubahan.py   (Windows: python / py)
"""
import sys
import unittest
from decimal import Decimal
from pathlib import Path

SINI = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SINI / "scripts"))
import hitung_perubahan as modul  # noqa: E402


class TesFormatAngka(unittest.TestCase):
    def test_bulat_ke_atas_setengah(self):
        self.assertEqual(modul.format_angka(Decimal("2.5")), 3)

    def test_bulat_ke_bawah(self):
        self.assertEqual(modul.format_angka(Decimal("2.4")), 2)


class TesPersen(unittest.TestCase):
    def test_normal(self):
        self.assertEqual(modul.persen(Decimal("32000000"), Decimal("24500000")), -23.4)

    def test_nilai_lama_nol(self):
        self.assertIsNone(modul.persen(Decimal("0"), Decimal("5000000")))


class TesPasanganNilaiLamaNegatif(unittest.TestCase):
    """Temuan #1 uji independen: laba -5jt -> 2jt harus tetap benar secara matematis
    (selisih +7jt, arah 'naik') TAPI wajib menyertakan catatan yang memperingatkan
    persen dari basis negatif tidak intuitif, supaya agent tidak menampilkannya
    mentah-mentah ke pengguna awam."""

    def test_arah_dan_selisih_benar(self):
        hasil = modul.proses_pasangan("Laba:-5000000:2000000")
        self.assertEqual(hasil["selisih"], 7000000)
        self.assertEqual(hasil["arah"], "naik")
        self.assertEqual(hasil["persen_perubahan"], -140.0)

    def test_catatan_basis_negatif_ada_dan_jelas(self):
        hasil = modul.proses_pasangan("Laba:-5000000:2000000")
        self.assertIsNotNone(hasil["catatan"])
        self.assertIn("negatif", hasil["catatan"])

    def test_nilai_lama_positif_tidak_ada_catatan(self):
        hasil = modul.proses_pasangan("Omzet:32000000:24500000")
        self.assertIsNone(hasil["catatan"])

    def test_nilai_lama_nol_catatan_berbeda(self):
        hasil = modul.proses_pasangan("Omzet:0:5000000")
        self.assertIsNone(hasil["persen_perubahan"])
        self.assertIn("tidak didefinisikan", hasil["catatan"])


class TesDaftar(unittest.TestCase):
    def test_total_rata_rata(self):
        hasil = modul.proses_daftar("Stok=18,24,29,33,37,41")
        self.assertEqual(hasil["total"], 182)
        self.assertEqual(hasil["rata_rata"], 30)
        self.assertEqual(hasil["min"], 18)
        self.assertEqual(hasil["max"], 41)


class TesFormatAngkaIndonesia(unittest.TestCase):
    """Audit format angka 2026-09-30: '38.000' dulu terbaca 38 (selisih 7, bukan 7.000)."""

    def test_titik_ribuan_dan_rp(self):
        for teks, harap in (("38.000", 38000), ("1.500", 1500), ("Rp38.000", 38000), ("Rp 38.000", 38000),
                            ("1.250.000", 1250000), ("1.250.000,50", Decimal("1250000.50")), ("2,5", Decimal("2.5")),
                            ("38rb", 38000), ("1,5jt", 1500000), ("-Rp5.000.000", -5000000), ("32000000", 32000000)):
            self.assertEqual(modul.baca_angka(teks), Decimal(harap), teks)

    def test_pasangan_titik_ribuan(self):
        hasil = modul.proses_pasangan("Omzet:38.000:45.000")
        self.assertEqual((hasil["nilai_lama"], hasil["nilai_baru"], hasil["selisih"], hasil["persen_perubahan"]),
                         (38000, 45000, 7000, 18.4))
        self.assertEqual(modul.proses_pasangan("Omzet:Rp38.000:Rp 45.000")["selisih"], 7000)

    def test_bentuk_ragu_ditolak(self):
        for teks in ("38.5", "1,500", "0.5", "abc", "2m"):
            with self.assertRaises(ValueError, msg=teks):
                modul.baca_angka(teks)
        with self.assertRaises(ValueError):
            modul.proses_pasangan("Omzet:38.5:45")

    def test_daftar_titik_ribuan_dan_titik_koma(self):
        hasil = modul.proses_daftar("Jual=1.500,2.000")
        self.assertEqual((hasil["total"], hasil["min"], hasil["max"]), (3500, 1500, 2000))
        hasil = modul.proses_daftar("Omzet=1,5jt;2jt;850rb")
        self.assertEqual(hasil["total"], 4350000)
        with self.assertRaises(ValueError):
            modul.proses_daftar("Omzet=1,5jt,2jt")


if __name__ == "__main__":
    unittest.main()
