#!/usr/bin/env python3
"""Uji regresi tanggal_relatif.py. Jalankan: python3 uji_tanggal_relatif.py (exit 0 = lulus)."""
import os
import subprocess
import sys
import unittest
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tanggal_relatif import tafsir  # noqa: E402

SENIN = date(2026, 9, 21)
MINGGU = date(2026, 9, 27)


def t(ekspr, rapat):
    return tafsir(ekspr, rapat)


class UjiHariBiasa(unittest.TestCase):
    def test_besok_lusa(self):
        self.assertEqual(t("besok", SENIN)["tanggal"], "2026-09-22")
        self.assertEqual(t("lusa", SENIN)["tanggal"], "2026-09-23")

    def test_jumat_depan_ambigu(self):
        h = t("jumat depan", SENIN)
        self.assertEqual((h["tanggal"], h["status"]), ("2026-10-02", "ambigu"))
        self.assertEqual(h["alternatif"], "Jumat, 25 September 2026")

    def test_hari_minggu_depan_pasti(self):
        h = t("rabu minggu depan", SENIN)
        self.assertEqual((h["tanggal"], h["status"]), ("2026-09-30", "pasti"))

    def test_minggu_depan_perkiraan(self):
        h = t("minggu depan", SENIN)
        self.assertEqual((h["tanggal"], h["status"]), ("2026-09-28", "perkiraan"))

    def test_akhir_bulan_dan_tahun(self):
        self.assertEqual(t("akhir bulan", SENIN)["tanggal"], "2026-09-30")
        self.assertEqual(t("awal bulan depan", date(2026, 12, 25))["tanggal"], "2027-01-01")

    def test_tidak_dikenali(self):
        self.assertEqual(t("secepatnya", SENIN)["status"], "tidak_dikenali")


class UjiRapatHariMinggu(unittest.TestCase):
    """Regresi: rapat hari Minggu 27/9/2026 -> 'depan' selalu ambigu, alternatif +7 hari."""

    def test_senin_minggu_depan(self):
        h = t("senin minggu depan", MINGGU)
        self.assertEqual((h["tanggal"], h["status"]), ("2026-09-28", "ambigu"))
        self.assertEqual(h["alternatif"], "Senin, 5 Oktober 2026")

    def test_jumat_depan(self):
        h = t("jumat depan", MINGGU)
        self.assertEqual((h["tanggal"], h["status"]), ("2026-10-02", "ambigu"))
        self.assertEqual(h["alternatif"], "Jumat, 9 Oktober 2026")

    def test_rabu_depan(self):
        h = t("rabu depan", MINGGU)
        self.assertEqual((h["status"], h["alternatif"]), ("ambigu", "Rabu, 7 Oktober 2026"))

    def test_minggu_depan_tanpa_hari(self):
        h = t("minggu depan", MINGGU)
        self.assertEqual((h["tanggal"], h["status"]), ("2026-09-28", "ambigu"))
        self.assertEqual(h["alternatif"], "Senin, 5 Oktober 2026")

    def test_minggu_depan_hari_minggu(self):
        h = t("minggu minggu depan", MINGGU)
        self.assertEqual((h["tanggal"], h["status"]), ("2026-10-04", "ambigu"))

    def test_bentuk_lain_tidak_terpengaruh(self):
        self.assertEqual(t("besok", MINGGU)["status"], "pasti")
        self.assertEqual(t("senin", MINGGU)["tanggal"], "2026-09-28")
        self.assertEqual(t("senin", MINGGU)["status"], "pasti")


class UjiAwalanBatas(unittest.TestCase):
    """v1.0.3 (uji OpenClaw 2026-10-01): 'sebelum rabu' dulu tidak_dikenali. Rapat Kamis 1/10/2026."""
    KAMIS = date(2026, 10, 1)

    def test_sebelum_rabu(self):
        h = t("sebelum rabu", self.KAMIS)
        self.assertEqual((h["tanggal"], h["status"], h["batas"]), ("2026-10-07", "pasti", "sebelum"))
        self.assertEqual(h["tenggat_teks"], "Sebelum Rabu, 7 Oktober 2026")
        self.assertIn("Selasa, 6 Oktober 2026", h["catatan"])

    def test_sblm_jumat_singkatan(self):
        h = t("sblm jumat", self.KAMIS)
        self.assertEqual((h["tanggal"], h["batas"]), ("2026-10-02", "sebelum"))

    def test_paling_lambat_senin_depan(self):
        h = t("paling lambat senin depan", self.KAMIS)
        self.assertEqual((h["tanggal"], h["status"], h["batas"]), ("2026-10-05", "pasti", "paling_lambat"))
        self.assertEqual(h["tenggat_teks"], "Paling lambat Senin, 5 Oktober 2026")

    def test_awalan_lain_dan_ambigu_tetap_ambigu(self):
        self.assertEqual(t("maks besok", self.KAMIS)["tanggal"], "2026-10-02")
        self.assertEqual(t("s.d. akhir bulan", self.KAMIS)["tanggal"], "2026-10-31")
        h = t("paling lambat jumat depan", self.KAMIS)
        self.assertEqual((h["status"], h["alternatif"]), ("ambigu", "Jumat, 2 Oktober 2026"))

    def test_awalan_tanpa_isi_atau_tak_dikenal(self):
        self.assertEqual(t("sebelum", self.KAMIS)["status"], "tidak_dikenali")
        self.assertEqual(t("sebelum lebaran", self.KAMIS)["status"], "tidak_dikenali")

    def test_tanpa_awalan_tidak_berubah(self):
        h = t("rabu", self.KAMIS)
        self.assertEqual((h["tanggal"], h["batas"], h["tenggat_teks"]), ("2026-10-07", None, "Rabu, 7 Oktober 2026"))


class UjiCli(unittest.TestCase):
    def jalankan(self, *arg):
        skrip = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tanggal_relatif.py")
        return subprocess.run([sys.executable, skrip] + list(arg), capture_output=True, text=True)

    def test_error_tanpa_rapat(self):
        r = self.jalankan("--ekspresi", "besok")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("ERROR", r.stderr)

    def test_tanggal_rusak(self):
        self.assertNotEqual(self.jalankan("--rapat", "31-31-2026", "--ekspresi", "besok").returncode, 0)

    def test_alias_nop(self):
        r = self.jalankan("--cek", "2 Nop 2026", "--format", "teks")
        self.assertEqual(r.returncode, 0)
        self.assertIn("Senin, 2 November 2026", r.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=1)
