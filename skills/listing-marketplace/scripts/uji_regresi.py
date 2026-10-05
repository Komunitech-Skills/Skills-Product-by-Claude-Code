#!/usr/bin/env python3
"""Uji regresi cek_listing.py. Jalankan: python3 uji_regresi.py (hanya library standar)."""
import json
import os
import subprocess
import sys
import unittest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cek_listing.py")


def cek(judul, deskripsi=None, platform="shopee", *arg):
    cmd = [sys.executable, SCRIPT, "--platform", platform, "--judul", judul, "--json"] + list(arg)
    if deskripsi is not None:
        cmd += ["--deskripsi", deskripsi]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    return r, (json.loads(r.stdout)[0] if r.returncode == 0 else None)


def tingkat(h, kata):
    return [t["tingkat"] for t in h["temuan"] if kata.lower() in t["pesan"].lower()]


class Uji(unittest.TestCase):
    def test_barang_tiruan_gagal(self):
        for judul in ("Tas Wanita KW Super Premium", "Sepatu Replika Import", "Jam Tangan Grade Ori",
                      "Dompet Mirip Charles Keith"):
            _, h = cek(judul)
            self.assertFalse(h["lulus"], judul)
            self.assertIn("GAGAL", tingkat(h, "tiruan"), judul)

    def test_klaim_kesehatan_diperluas(self):
        desk = ("Membantu turunkan kolesterol, meningkatkan imun, aman untuk ibu hamil, detoks alami, "
                "menyembuhkan maag.")
        _, h = cek("Teh Celup Jahe Merah 25 Pcs", desk)
        teks = " ".join(t["pesan"].lower() for t in h["temuan"])
        for k in ("turunkan kolesterol", "meningkatkan imun", "aman untuk ibu hamil", "detoks", "menyembuhkan"):
            self.assertIn(k, teks, k)

    def test_kontak_dan_ajakan_wa(self):
        _, h = cek("Kaos Polos Cotton Combed 30s", "Order via WA ya. Hubungi +62 813 1111 2222.")
        self.assertFalse(h["lulus"])
        self.assertEqual(len([t for t in h["temuan"] if t["tingkat"] == "GAGAL"]), 2)

    def test_listing_bersih_lulus_dan_varian_original_tidak_dicek(self):
        _, h = cek("Keripik Tempe Pedas 250 gr Renyah Oleh Oleh Malang", "Varian: Rasa Original / Pedas. " * 20,
                   "tokopedia")
        self.assertTrue(h["lulus"], h["temuan"])
        self.assertEqual(tingkat(h, "keaslian"), [])

    def test_batas_judul_tokopedia(self):
        _, h = cek("A" * 30 + " " + "b" * 45, None, "tokopedia")
        self.assertFalse(h["lulus"])

    def test_input_rusak(self):
        r, _ = cek("Kaos", None, "lazada")
        self.assertEqual(r.returncode, 1)
        r, _ = cek("Kaos", None, "shopee", "--batas-judul", "0")
        self.assertEqual(r.returncode, 1)

    def test_klaim_sifat_di_luar_fakta_gagal(self):
        # Temuan uji OpenClaw 2026-10-01: "ga gampang buyar" ditambah sendiri, script tetap LULUS.
        fakta = ("115x115 voal premium, tepi lasercut, motif bunga dusty pink, sage, mocca, navy. "
                 "adem, ga licin, gampang dibentuk, ga nerawang. isi 1 pcs, cuci tangan aja jgn dipemutih")
        desk = ("Hijab voal premium yang adem, ga licin, gampang dibentuk, dan ga nerawang. "
                "Tepi lasercut ga gampang buyar. Dikirim cepat & packing aman. Awet dipakai.")
        _, h = cek("Hijab Voal Motif Bunga 115x115 Tepi Lasercut", desk, "shopee", "--fakta", fakta)
        self.assertFalse(h["lulus"])
        gagal = " ".join(t["pesan"] for t in h["temuan"] if t["tingkat"] == "GAGAL")
        for frasa in ("ga gampang buyar", "Dikirim cepat", "packing aman", "Awet"):
            self.assertIn(frasa, gagal, frasa)
        for frasa in ("premium", "adem"):
            self.assertNotIn("'" + frasa, gagal.lower(), frasa)

    def test_klaim_sifat_sesuai_fakta_lulus(self):
        fakta = "bahan adem, tepi lasercut ga gampang buyar, voal premium"
        desk = "Bahan voal premium, adem dipakai. Tepi lasercut ga gampang buyar. " * 8
        _, h = cek("Hijab Voal Motif Bunga 115x115 Tepi Lasercut", desk, "shopee", "--fakta", fakta)
        self.assertTrue(h["lulus"], h["temuan"])

    def test_klaim_sifat_tanpa_fakta_cek(self):
        _, h = cek("Tumbler Stainless 500 ml", "Tumbler anti bocor, awet. " * 15)
        self.assertTrue(h["lulus"])
        self.assertIn("CEK", tingkat(h, "anti bocor"))
        # "kering cepat" tidak boleh terbaca sebagai negasi "g cepat ..."
        _, h = cek("Handuk Microfiber 70x140", "Handuk kering cepat kering dipakai. " * 15, "shopee",
                   "--fakta", "handuk microfiber 70x140")
        self.assertTrue(h["lulus"], h["temuan"])

    def test_fakta_ganda_ditolak(self):
        r, _ = cek("Kaos", None, "shopee", "--fakta", "a", "--fakta-file", "x.txt")
        self.assertEqual(r.returncode, 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
