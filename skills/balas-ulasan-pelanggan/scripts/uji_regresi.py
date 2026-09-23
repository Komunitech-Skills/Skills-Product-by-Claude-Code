#!/usr/bin/env python3
"""Uji regresi cek_balasan.py. Jalankan: python3 uji_regresi.py (hanya library standar)."""
import json
import os
import subprocess
import sys
import unittest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cek_balasan.py")


def cek(teks, platform="shopee", jenis="negatif"):
    r = subprocess.run([sys.executable, SCRIPT, "--platform", platform, "--jenis", jenis, "--teks", teks, "--json"],
                       capture_output=True, text=True, encoding="utf-8")
    return r, (json.loads(r.stdout) if r.returncode == 0 else None)


def pesan(h):
    return " ".join(t["pesan"] for t in h["temuan"])


class Uji(unittest.TestCase):
    def test_nama_lengkap_dan_kutipan_chat(self):
        _, h = cek("Kak Rina Wulandari, mohon maaf ya. Kakak sendiri bilang 'gpp kak telat dikit'. "
                   "Kami bantu lewat chat toko, terima kasih.")
        self.assertTrue(h["perlu_dicek_privasi"])
        self.assertIn("NAMA LENGKAP", pesan(h))
        self.assertIn("KUTIPAN CHAT", pesan(h))

    def test_data_pesanan_dan_wa_gagal(self):
        _, h = cek("Mohon maaf Kak, pesanan INV/20260920/MPL/123456 ke Jl. Melati No. 5 RT 03/RW 07. "
                   "Hubungi WA 0812-3333-4444 ya, terima kasih.")
        self.assertFalse(h["lulus"])
        for k in ("invoice", "alamat", "nomor HP", "luar platform"):
            self.assertIn(k, pesan(h))

    def test_imbalan_ubah_rating_gagal(self):
        _, h = cek("Terima kasih Kak, mohon maaf. Nanti kami kasih voucher kalau ubah bintang 5 ya, chat kami.")
        self.assertFalse(h["lulus"])

    def test_false_positive_berkurang(self):
        _, h = cek("Terima kasih Kak Dodi! Semoga jalan-jalan ke Bekasi mampir lagi. Line produksi kami baru. "
                   "Pengalaman yang seharusnya Kakak dapat memang begitu.", "google", "positif")
        self.assertTrue(h["lulus"])
        self.assertFalse(h["perlu_dicek_privasi"], h["temuan"])
        self.assertNotIn("defensif", pesan(h))

    def test_balasan_baik_lulus(self):
        _, h = cek("Kak, terima kasih sudah memberi tahu, dan mohon maaf botol sambalnya bocor. Kami sudah "
                   "menghubungi Kakak lewat chat toko untuk membantu penggantian. — Dapur Bu Ratmi")
        self.assertTrue(h["lulus"])
        self.assertFalse(h["perlu_dicek_privasi"])

    def test_input_rusak(self):
        self.assertEqual(cek("x", "lazada")[0].returncode, 1)
        self.assertEqual(cek("   ")[0].returncode, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
