"""Tes harga_marketplace.py (v1.0.3). Jalankan dari folder skill: python3 -m unittest discover -s tests -v

Skenario uji OpenClaw 2026-10-01 (Shopee, modal 39.250, admin 8%, layanan 4% maks 10.000, target margin 25%):
  balik modal = 39.250 / (1 - 0,08 - 0,04 - 0,005) = 44.857,14 -> Rp 44.858
  target      = 39.250 / (1 - 0,125 - 0,25) = 62.800 -> rekomendasi kelipatan 500 = Rp 63.000
  di 63.000   : admin 5.040, layanan 2.520, PPh 22 315 -> diterima 55.125, laba 15.875"""
import io
import json
import os
import subprocess
import sys
import unittest
from contextlib import redirect_stdout

SKRIP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts", "harga_marketplace.py")
sys.path.insert(0, os.path.dirname(SKRIP))
import harga_marketplace as hm  # noqa: E402

ARGV = ["--platform", "Shopee", "--modal", "39.250", "--admin", "8", "--layanan", "4", "--maks-layanan", "10.000",
        "--target-margin", "25"]


def jalan(*argv):
    buf = io.StringIO()
    with redirect_stdout(buf):
        kode = hm.main(list(argv))
    return kode, buf.getvalue()


class TesRevisi103(unittest.TestCase):
    def test_help_tidak_crash(self):
        p = subprocess.run([sys.executable, SKRIP, "--help"], capture_output=True, text=True, timeout=60)
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertNotIn("Traceback", p.stderr)

    def test_angka_skenario_shopee(self):
        kode, out = jalan(*ARGV)
        self.assertEqual(kode, 0)
        self.assertIn("Harga minimal agar tidak rugi: **Rp 44.858**", out)
        self.assertIn("Rp 63.000", out)
        self.assertIn("-Rp 315", out)
        self.assertIn("**Rp 15.875**", out)

    def test_blok_catatan_memuat_dasar_aturan_tanggal_disclaimer(self):
        kode, out = jalan(*ARGV)
        blok = out.split("**Catatan & asumsi**", 1)[1]
        self.assertIn("PMK 37/2025, berlaku 1 Agustus 2026", blok)
        self.assertIn("Berlaku per 2026-09-23", blok)
        self.assertIn("bukan nasihat pajak", blok)
        kode, out = jalan(*(ARGV + ["--format", "json"]))
        catatan = " ".join(json.loads(out)["catatan"])
        self.assertIn("PMK 37/2025", catatan)


if __name__ == "__main__":
    unittest.main()
