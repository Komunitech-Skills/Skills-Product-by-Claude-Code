#!/usr/bin/env python3
"""Tes mandiri untuk bangun_tautan_wa.py. Jalankan: python3 test_bangun_tautan_wa.py
Tidak memakai framework eksternal (hanya pustaka standar) supaya bisa jalan di mana saja.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from bangun_tautan_wa import (
    InputSalah,
    bangun_tautan_wa,
    cek_meta,
    normalisasi_nomor_wa,
)


class TesNormalisasiNomor(unittest.TestCase):
    def test_awalan_nol(self):
        self.assertEqual(normalisasi_nomor_wa("0812-3456-7890"), "6281234567890")

    def test_awalan_delapan(self):
        self.assertEqual(normalisasi_nomor_wa("81234567890"), "6281234567890")

    def test_awalan_62(self):
        self.assertEqual(normalisasi_nomor_wa("6281234567890"), "6281234567890")

    def test_awalan_plus62(self):
        self.assertEqual(normalisasi_nomor_wa("+62 812 3456 7890"), "6281234567890")

    def test_kosong_gagal(self):
        with self.assertRaises(InputSalah):
            normalisasi_nomor_wa("")

    def test_bukan_angka_gagal(self):
        with self.assertRaises(InputSalah):
            normalisasi_nomor_wa("08abc23456")

    def test_kode_negara_asing_gagal(self):
        with self.assertRaises(InputSalah):
            normalisasi_nomor_wa("14155552671")  # nomor AS, bukan 08xx/8xx/62xx


class TesBangunTautan(unittest.TestCase):
    def test_tautan_tanpa_pesan(self):
        self.assertEqual(bangun_tautan_wa("081234567890"), "https://wa.me/6281234567890")

    def test_tautan_dengan_pesan_ter_encode(self):
        tautan = bangun_tautan_wa("081234567890", "Halo, saya mau pesan keripik pedas")
        self.assertTrue(tautan.startswith("https://wa.me/6281234567890?text="))
        self.assertIn("Halo%2C%20saya%20mau%20pesan%20keripik%20pedas", tautan)
        self.assertNotIn(" ", tautan)

    def test_nomor_tidak_valid_raise(self):
        with self.assertRaises(InputSalah):
            bangun_tautan_wa("bukan-nomor")


class TesCekMeta(unittest.TestCase):
    def test_title_pas_batas(self):
        teks = "x" * 60
        hasil = cek_meta("Meta title", teks, 60)
        self.assertEqual(hasil["status"], "OK")
        self.assertEqual(hasil["panjang"], 60)

    def test_title_lewat_batas(self):
        teks = "x" * 61
        hasil = cek_meta("Meta title", teks, 60)
        self.assertEqual(hasil["status"], "TERLALU PANJANG")

    def test_desc_lewat_batas(self):
        teks = "y" * 156
        hasil = cek_meta("Meta description", teks, 155)
        self.assertEqual(hasil["status"], "TERLALU PANJANG")
        self.assertEqual(hasil["panjang"], 156)

    def test_desc_dalam_batas(self):
        teks = "Keripik singkong pedas gurih, tanpa pengawet, siap kirim seluruh Indonesia. Pesan via WhatsApp."
        hasil = cek_meta("Meta description", teks, 155)
        self.assertEqual(hasil["status"], "OK")


class TesDataRusak(unittest.TestCase):
    """Skenario input rusak/aneh yang wajib ditangani dengan pesan error jelas, bukan crash mentah."""

    def test_nomor_none(self):
        with self.assertRaises(InputSalah):
            normalisasi_nomor_wa(None)

    def test_nomor_terlalu_pendek(self):
        with self.assertRaises(InputSalah):
            normalisasi_nomor_wa("0812")

    def test_nomor_terlalu_panjang(self):
        with self.assertRaises(InputSalah):
            normalisasi_nomor_wa("0" + "8" * 20)

    def test_pesan_kosong_tidak_menambah_query(self):
        tautan = bangun_tautan_wa("081234567890", "   ")
        self.assertEqual(tautan, "https://wa.me/6281234567890")


if __name__ == "__main__":
    unittest.main()
