#!/usr/bin/env python3
"""Uji regresi rekap.py. Jalankan: python3 uji_regresi.py (hanya library standar)."""
import json
import os
import subprocess
import sys
import tempfile
import unittest

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rekap.py")


def rekap(isi_csv, *arg):
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, "jual.csv")
        with open(path, "w", encoding="utf-8") as f:
            f.write(isi_csv)
        r = subprocess.run([sys.executable, SCRIPT, path, "--kolom-tanggal", "Tanggal", "--kolom-produk", "Produk",
                            "--kolom-total", "Total"] + list(arg), capture_output=True, text=True, encoding="utf-8")
    return r, (json.loads(r.stdout) if r.returncode == 0 else None)


# 01/09: 1 pesanan besar (omzet tertinggi); 02/09: 3 pesanan kecil (transaksi terbanyak, 4 baris)
CSV = """No. Pesanan,Tanggal,Produk,Total
A1,01/09/2026,Serum,500.000
B1,02/09/2026,Masker,20.000
B1,02/09/2026,Sabun,10.000
B2,02/09/2026,Masker,20.000
B3,02/09/2026,Sabun,10.000
C1,03/09/2026,Masker,20.000
"""


class Uji(unittest.TestCase):
    def test_hari_omzet_vs_transaksi_terbanyak(self):
        # Temuan uji OpenClaw 2026-10-01: "hari paling rame" hanya dijawab dari omzet.
        _, h = rekap(CSV)
        self.assertEqual(h["hari_terbaik"]["tanggal"], "2026-09-01")
        self.assertEqual(h["hari_transaksi_terbanyak"]["tanggal"], "2026-09-02")
        self.assertEqual(h["hari_transaksi_terbanyak"]["jumlah"], 4)
        self.assertEqual(h["hari_transaksi_terbanyak"]["satuan"], "baris transaksi")
        self.assertEqual(h["jumlah_transaksi_harian"], {"2026-09-01": 1, "2026-09-02": 4, "2026-09-03": 1})

    def test_pesanan_unik(self):
        _, h = rekap(CSV, "--kolom-pesanan", "No. Pesanan")
        self.assertEqual(h["hari_transaksi_terbanyak"]["jumlah"], 3)
        self.assertIn("pesanan unik", h["hari_transaksi_terbanyak"]["satuan"])
        self.assertEqual(h["total_omzet"], 580000)

    def test_seri(self):
        _, h = rekap(CSV.replace("C1,03/09/2026,Masker,20.000\n", "") + "C1,03/09/2026,Masker,20.000\n" * 4)
        self.assertEqual(h["hari_transaksi_terbanyak"]["semua_tanggal_seri"], ["2026-09-02", "2026-09-03"])

    def test_kolom_pesanan_tidak_ada(self):
        r, _ = rekap(CSV, "--kolom-pesanan", "Order ID")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("Order ID", r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
