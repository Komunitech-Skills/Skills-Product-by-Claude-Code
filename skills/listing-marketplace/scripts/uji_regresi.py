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


if __name__ == "__main__":
    unittest.main(verbosity=2)
