"""Tes hitung_hpp.py (v1.0.3: banding harga & porsi biaya). Jalankan dari folder skill:
python3 -m unittest discover -s tests -v"""
import io
import json
import os
import sys
import unittest
from contextlib import redirect_stdout
from decimal import Decimal

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import hitung_hpp as h  # noqa: E402

KOPI = {
    "nama_produk": "Es kopi susu gula aren", "satuan_produk": "gelas", "produksi_per_bulan": 1040,
    "bahan": [
        {"nama": "Kopi", "harga_beli": "180.000", "isi_beli": 1, "satuan_beli": "kg", "pakai": 18,
         "satuan_pakai": "g", "per": "unit"},
        {"nama": "Susu UHT", "harga_beli": "19.500", "isi_beli": 1, "satuan_beli": "liter", "pakai": 120,
         "satuan_pakai": "ml", "per": "unit"},
        {"nama": "Gula aren", "harga_beli": "45.000", "isi_beli": 1, "satuan_beli": "liter", "pakai": 25,
         "satuan_pakai": "ml", "per": "unit"},
        {"nama": "Es batu", "biaya": 500, "per": "unit"}],
    "kemasan": [{"nama": "Gelas+tutup+sedotan", "biaya": 1800}],
    "tenaga_kerja": [{"nama": "Gaji barista", "biaya": "2.400.000", "per": "bulan"}],
    "overhead": [{"nama": "Sewa", "biaya": "1.500.000", "per": "bulan"},
                 {"nama": "Listrik", "biaya": "600.000", "per": "bulan"}],
}


class TesBandingHarga(unittest.TestCase):
    def hitung(self, **tambahan):
        d = dict(KOPI, **tambahan)
        hh = h.hitung(d)
        return hh, h.susun_harga(hh, d)

    def test_bep_harga_18000(self):
        # verifikasi independen: 4.500.000 / (18.000 - 9.005) = 500,28 -> 501 gelas
        _, hg = self.hitung(banding_harga=[18000, "19.500"])
        b18, b195 = hg["banding_harga"]
        self.assertEqual(b18["bep"]["bep_unit"], Decimal(501))
        self.assertEqual(b18["bep"]["bep_unit_tepat"], Decimal("500.28"))
        self.assertEqual(b195["bep"]["bep_unit"], Decimal(429))
        self.assertEqual(b18["laba_per_unit"].quantize(Decimal("0.01")), Decimal("4668.08"))

    def test_banding_dari_teks(self):
        _, hg = self.hitung(banding_harga="Rp 18.000; 19500")
        self.assertEqual([r["harga"] for r in hg["banding_harga"]], [Decimal(18000), Decimal(19500)])
        _, hg = self.hitung(banding_harga="18000 19500")
        self.assertEqual(len(hg["banding_harga"]), 2)

    def test_banding_tidak_valid(self):
        with self.assertRaises(ValueError):
            self.hitung(banding_harga=[0])
        with self.assertRaises(ValueError):
            self.hitung(banding_harga="abc")

    def test_porsi_biaya_bahan_terbesar(self):
        hh, _ = self.hitung()
        p = hh["porsi_biaya"]
        self.assertEqual(p["per_kategori"][0]["kategori"], "Bahan baku")
        self.assertEqual(p["per_kategori"][0]["per_unit"], Decimal(7205))
        self.assertEqual(p["variabel_per_unit"], Decimal(9005))
        self.assertGreater(p["variabel_persen_hpp"], p["tetap_persen_hpp"])
        self.assertEqual(p["komponen_terbesar"]["nama"], "Kopi")

    def test_cli_teks(self):
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as f:
            json.dump(KOPI, f)
        try:
            buf = io.StringIO()
            with redirect_stdout(buf):
                kode = h.main(["--file", f.name, "--banding-harga", "18000"])
        finally:
            os.unlink(f.name)
        self.assertEqual(kode, 0)
        out = buf.getvalue()
        self.assertIn("Banding harga yang dibahas", out)
        self.assertIn("501 gelas (tepatnya 500,28)", out)
        self.assertIn("Porsi biaya dalam HPP", out)


if __name__ == "__main__":
    unittest.main()
