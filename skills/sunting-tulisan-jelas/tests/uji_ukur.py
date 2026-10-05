#!/usr/bin/env python3
"""Uji sederhana ukur_keterbacaan.py. Jalankan: python3 tests/uji_ukur.py"""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKRIP = Path(__file__).resolve().parent.parent / "scripts" / "ukur_keterbacaan.py"
sys.path.insert(0, str(SKRIP.parent))
import ukur_keterbacaan as u  # noqa: E402

DAFTAR = u.muat_daftar()


def jalan(*args, stdin=None):
    return subprocess.run([sys.executable, str(SKRIP), *args], input=stdin, capture_output=True, text=True, encoding="utf-8")


class Uji(unittest.TestCase):
    def test_kalimat_sederhana(self):
        h = u.ukur("Toko tutup besok. Kami buka lagi Senin. Terima kasih!", DAFTAR)
        self.assertEqual(h["kalimat"], 3)
        self.assertEqual(h["kata"], 9)
        self.assertEqual(h["rata_kata_per_kalimat"], 3.0)

    def test_singkatan_dan_angka_tidak_memecah(self):
        h = u.ukur("Bpk. Budi membayar Rp1.500.000 pada pukul 10.30 di Jl. Melati No. 5 hari ini.", DAFTAR)
        self.assertEqual(h["kalimat"], 1)

    def test_kalimat_panjang(self):
        teks = " ".join(["kata"] * 30) + ". Pendek saja."
        h = u.ukur(teks, DAFTAR)
        self.assertEqual(h["kalimat_lebih_25_kata"], 1)
        self.assertEqual(h["persen_kalimat_lebih_25_kata"], 50.0)

    def test_butir_daftar_satu_satuan(self):
        h = u.ukur("Bawa:\n- KTP\n- Fotokopi KK\n1. Isi formulir", DAFTAR)
        self.assertEqual(h["kalimat"], 4)

    def test_penanda_tidak_dihitung_ganda(self):
        h = u.ukur("Kami lakukan dalam rangka evaluasi.", DAFTAR)
        frasa = [r["frasa"] for r in h["penanda_rincian"]]
        self.assertIn("dalam rangka", frasa)

    def test_pasif_bukan_kata_biasa(self):
        h = u.ukur("Dia diam di dinas. Barang dikirim kemarin.", DAFTAR)
        self.assertEqual(h["perkiraan_kalimat_pasif"], 1)

    def test_banding_angka_hilang(self):
        with tempfile.TemporaryDirectory() as d:
            a, b = Path(d, "a.txt"), Path(d, "b.txt")
            a.write_text("Bayar Rp1.500.000 sebelum 10 Oktober.", encoding="utf-8")
            b.write_text("Bayar sebelum 12 Oktober.", encoding="utf-8")
            r = jalan("--sebelum", str(a), "--sesudah", str(b))
            self.assertEqual(r.returncode, 0)
            self.assertIn("1.500.000", r.stdout.split("HILANG")[1].splitlines()[0])
            self.assertIn("12", r.stdout.split("BARU")[1])

    def test_kosong_dan_rusak(self):
        self.assertNotEqual(jalan("--teks", "   ").returncode, 0)
        self.assertNotEqual(jalan("--file", "tidak-ada.txt").returncode, 0)
        with tempfile.TemporaryDirectory() as d:
            bin_ = Path(d, "x.docx")
            bin_.write_bytes(b"PK\x03\x04\x00\x00binary")
            r = jalan("--file", str(bin_))
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("bukan teks", r.stderr)
        r = jalan("--teks", "😀😀 123 !!!")
        self.assertEqual(r.returncode, 0)  # angka dihitung sebagai kata; tidak crash

    def test_stdin_dan_json(self):
        r = jalan("--json", stdin="Halo Bu. Pesanan sudah dikirim.")
        self.assertEqual(r.returncode, 0)
        self.assertIn('"kalimat": 2', r.stdout)


if __name__ == "__main__":
    unittest.main()
