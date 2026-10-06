#!/usr/bin/env python3
"""Uji regresi jadwal_rangkaian.py. Jalankan: python3 tests/uji_regresi.py"""
import importlib.util
import json
import subprocess
import sys
import unittest
from datetime import date, timedelta
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent.parent / "scripts" / "jadwal_rangkaian.py"
spec = importlib.util.spec_from_file_location("jadwal_rangkaian", SCRIPT)
jr = importlib.util.module_from_spec(spec)
spec.loader.exec_module(jr)


def jalankan(*args):
    return subprocess.run([sys.executable, "-I", str(SCRIPT), *args], capture_output=True, text=True)


class Uji(unittest.TestCase):
    def test_tanggal_dasar(self):
        h = jr.hitung_jadwal(date(2026, 10, 7), [0, 3, 10, 21])  # Rabu
        self.assertEqual(h["jadwal"][0], [date(2026, 10, 7), date(2026, 10, 10), date(2026, 10, 17), date(2026, 10, 28)])

    def test_minggu_digeser_maju(self):
        h = jr.hitung_jadwal(date(2026, 10, 4), [0])  # Minggu
        self.assertEqual(h["jadwal"][0][0], date(2026, 10, 5))

    def test_minggu_boleh(self):
        h = jr.hitung_jadwal(date(2026, 10, 4), [0], termasuk_minggu=True)
        self.assertEqual(h["jadwal"][0][0], date(2026, 10, 4))

    def test_sebelum_acuan_digeser_mundur(self):
        h = jr.hitung_jadwal(date(2026, 12, 27), [-14], libur=frozenset())  # 13 Des = Minggu
        self.assertEqual(h["jadwal"][0][0], date(2026, 12, 12))

    def test_libur_mundur_berantai(self):
        libur = frozenset({date(2026, 12, 25), date(2026, 12, 24)})
        h = jr.hitung_jadwal(date(2026, 12, 27), [-2], libur=libur)
        self.assertEqual(h["jadwal"][0][0], date(2026, 12, 23))

    def test_batas_per_hari(self):
        h = jr.hitung_jadwal(date(2026, 10, 7), [0, 5], pelanggan=25, per_hari=10)
        self.assertLessEqual(max(h["beban"].values()), 10)
        self.assertEqual(sum(h["beban"].values()), 50)

    def test_satu_pesan_per_pelanggan_per_hari(self):
        h = jr.hitung_jadwal(date(2026, 10, 7), [0, 1, 2, 3], pelanggan=7, per_hari=3)
        for baris in h["jadwal"]:
            self.assertEqual(len(set(baris)), len(baris))
        self.assertLessEqual(max(h["beban"].values()), 3)

    def test_tidak_ada_minggu_di_jadwal(self):
        h = jr.hitung_jadwal(date(2026, 10, 1), list(range(0, 30, 2)), pelanggan=5, per_hari=4)
        for baris in h["jadwal"]:
            for d in baris:
                self.assertNotEqual(d.weekday(), 6)

    def test_banyak_pelanggan_kelompok_rapi(self):
        h = jr.hitung_jadwal(date(2026, 10, 7), [0, 5, 12], pelanggan=120, per_hari=10)
        self.assertLessEqual(max(h["beban"].values()), 10)
        self.assertEqual(sum(h["beban"].values()), 360)
        mulai = sorted({b[0] for b in h["jadwal"]})
        self.assertEqual(len(mulai), 12)
        for b in h["jadwal"]:  # jarak antar pesan tetap sesuai rencana (+geser Minggu)
            self.assertGreaterEqual((b[1] - b[0]).days, 5)

    def test_ringkas_nomor(self):
        self.assertEqual(jr.ringkas_nomor([1, 2, 3, 5, 7, 8]), "1-3, 5, 7-8")

    def test_semua_preset_valid(self):
        for nama, (_, langkah) in jr.SITUASI.items():
            self.assertLessEqual(len(langkah), 5, nama)
            jarak = [j for j, _, _ in langkah]
            self.assertEqual(jarak, sorted(jarak), nama)
            r = jalankan("--situasi", nama, "--mulai", "2026-10-07", "--format", "json")
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(len(json.loads(r.stdout)["langkah"]), len(langkah))

    def test_keranjang_tiga_pesan(self):
        self.assertEqual([j for j, _, _ in jr.SITUASI["keranjang"][1]], [0, 1, 3])

    def test_cli_tanggal_rusak(self):
        r = jalankan("--situasi", "ulasan", "--mulai", "31-02-2026")
        self.assertEqual(r.returncode, 1)
        self.assertIn("tidak dikenali", r.stderr)

    def test_cli_hari_rusak(self):
        r = jalankan("--hari", "0,abc", "--mulai", "2026-10-07")
        self.assertEqual(r.returncode, 1)

    def test_cli_terlalu_banyak_pesan(self):
        r = jalankan("--hari", "0,1,2,3,4,5,6,7,8", "--mulai", "2026-10-07")
        self.assertEqual(r.returncode, 1)
        self.assertIn("maksimal", r.stderr)

    def test_cli_tanpa_situasi(self):
        self.assertEqual(jalankan("--mulai", "2026-10-07").returncode, 1)

    def test_cli_jarak_kembar_dan_per_hari(self):
        self.assertEqual(jalankan("--hari", "1,1", "--mulai", "2026-10-07").returncode, 1)
        self.assertEqual(jalankan("--situasi", "ulasan", "--mulai", "2026-10-07", "--per-hari", "0").returncode, 1)

    def test_cli_sudah_lewat(self):
        r = jalankan("--situasi", "ulasan", "--mulai", "2026-10-07", "--hari-ini", "2026-10-30", "--format", "json")
        self.assertIn("sudah lewat", " ".join(json.loads(r.stdout)["catatan"]).lower())


if __name__ == "__main__":
    unittest.main(verbosity=1)
