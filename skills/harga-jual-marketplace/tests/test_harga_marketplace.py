"""Tes harga_marketplace.py (v1.0.3-1.0.4). Jalankan dari folder skill: python3 -m unittest discover -s tests -v

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


class TesRevisi104(unittest.TestCase):
    """Uji ulang OpenClaw 2026-10-01: model menyebut Rp62.900 'di bawah target' padahal margin 25,1% (>= 25%)."""

    def test_status_rekomendasi_dan_banding(self):
        kode, out = jalan(*(ARGV + ["--banding-harga", "62.900;59.900"]))
        self.assertEqual(kode, 0)
        self.assertIn("Status target pada harga rekomendasi: **MEMENUHI target margin 25%", out)
        baris = {l.split("|")[1].strip(): l for l in out.splitlines() if l.startswith("| Rp 6") or l.startswith("| Rp 5")}
        self.assertIn("MEMENUHI target", baris["Rp 62.900"])
        self.assertIn("25,1%", baris["Rp 62.900"])
        self.assertIn("DI BAWAH target", baris["Rp 59.900"])
        self.assertIn("laba kurang Rp 1.813", baris["Rp 59.900"])

    def test_harga_tepat_target_memenuhi_satu_rupiah_dibawah_tidak(self):
        kode, out = jalan(*(ARGV + ["--banding-harga", "62.800;62.799", "--format", "json"]))
        b = json.loads(out)["hasil"][0]["banding"]
        self.assertEqual([x["memenuhi_target"] for x in b], [True, False])

    def test_cek_harga_dengan_target(self):
        kode, out = jalan("--platform", "Shopee", "--modal", "39.250", "--admin", "8", "--layanan", "4",
                          "--harga-jual", "62.900", "--target-margin", "25")
        self.assertEqual(kode, 0)
        self.assertIn("Status target: **MEMENUHI target margin 25%", out)
        kode, out = jalan("--modal", "39.250", "--admin", "8", "--harga-jual", "50.000")
        self.assertNotIn("Status target", out)   # tanpa target: tidak ada status

    def test_target_laba_dan_banding_rusak(self):
        kode, out = jalan("--modal", "39.250", "--admin", "8", "--target-laba", "10.000", "--banding-harga", "50.000")
        self.assertIn("MEMENUHI target laba Rp 10.000", out)
        self.assertIn("| Rp 50.000 | Rp 45.750 | Rp 6.500 | 13% | DI BAWAH target laba Rp 10.000 per barang", out)
        p = subprocess.run([sys.executable, SKRIP, "--modal", "39.250", "--target-margin", "25", "--banding-harga",
                            "abc"], capture_output=True, text=True, timeout=60)
        self.assertEqual(p.returncode, 2)
        self.assertIn("ERROR", p.stderr)
        self.assertNotIn("Traceback", p.stderr)


if __name__ == "__main__":
    unittest.main()
