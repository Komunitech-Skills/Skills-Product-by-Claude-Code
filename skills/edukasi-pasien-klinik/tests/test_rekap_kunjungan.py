#!/usr/bin/env python3
"""Tes mandiri untuk rekap_kunjungan.py — jalankan:
    python3 test_rekap_kunjungan.py
Hanya library standar (unittest).
"""
import io
import json
import sys
import unittest
from contextlib import redirect_stdout, redirect_stderr

import sys as _sys, os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..', 'scripts'))
import rekap_kunjungan as rk


CSV_NORMAL = """Tanggal,Jam,Poli,Penjamin,Status
2026-09-01,08:15,Gigi,BPJS,Selesai
2026-09-01,09:00,Gigi,Umum,Selesai
2026-09-01,09:30,Umum,BPJS,Tidak Datang
2026-09-02,08:00,Gigi,Umum,Selesai
2026-09-02,10:00,KIA,BPJS,Selesai
"""

CSV_DENGAN_KOLOM_SENSITIF = """Tanggal,Nama Pasien,NIK,Poli,Diagnosis
2026-09-01,Budi,3201xxxx,Gigi,K02.1
2026-09-01,Sari,3201yyyy,Umum,J06
"""

CSV_TANGGAL_CAMPUR = """Tanggal,Poli
01/09/2026,Gigi
2026-09-02,Gigi
tanggal-rusak,Gigi
"""

CSV_HANYA_HEADER = """Tanggal,Poli
"""


class TesRekapNormal(unittest.TestCase):
    def test_rekap_lengkap(self):
        header, baris = rk.baca_csv(CSV_NORMAL, is_text=True)
        hasil = rk.rekap(header, baris)
        self.assertEqual(hasil["total_baris"], 5)
        self.assertEqual(hasil["per_hari"]["2026-09-01"], 3)
        self.assertEqual(hasil["per_hari"]["2026-09-02"], 2)
        self.assertEqual(hasil["per_poli"]["Gigi"], 3)
        self.assertEqual(hasil["per_penjamin"]["BPJS"], 3)
        self.assertEqual(hasil["pasien_tidak_datang"], 1)
        self.assertEqual(hasil["kolom_sensitif_diabaikan"], [])
        # jam ramai harus mengandung jam 08 dan 09
        jam_list = [j["jam"] for j in hasil["jam_ramai"]]
        self.assertIn("08:00", jam_list)

    def test_format_teks_tidak_error(self):
        header, baris = rk.baca_csv(CSV_NORMAL, is_text=True)
        hasil = rk.rekap(header, baris)
        teks = rk.format_teks(hasil)
        self.assertIn("REKAP OPERASIONAL", teks)
        self.assertIn("2026-09-01", teks)


class TesPrivasi(unittest.TestCase):
    def test_kolom_sensitif_tidak_muncul_di_output(self):
        header, baris = rk.baca_csv(CSV_DENGAN_KOLOM_SENSITIF, is_text=True)
        hasil = rk.rekap(header, baris)
        teks = rk.format_teks(hasil)
        dump = json.dumps(hasil, ensure_ascii=False)
        for terlarang in ["Budi", "Sari", "3201xxxx", "3201yyyy", "K02.1", "J06"]:
            self.assertNotIn(terlarang, teks)
            self.assertNotIn(terlarang, dump)
        # tapi tetap diberi tahu kolom apa yang diabaikan
        self.assertIn("nama pasien", [c.lower() for c in hasil["kolom_sensitif_diabaikan"]])
        self.assertIn("diagnosis", [c.lower() for c in hasil["kolom_sensitif_diabaikan"]])


class TesDataRusak(unittest.TestCase):
    def test_tanggal_campur_sebagian_gagal(self):
        header, baris = rk.baca_csv(CSV_TANGGAL_CAMPUR, is_text=True)
        hasil = rk.rekap(header, baris)
        self.assertEqual(hasil["total_baris"], 3)
        self.assertEqual(hasil["baris_tanggal_tidak_terbaca"], 1)
        self.assertEqual(sum(hasil["per_hari"].values()), 2)

    def test_hanya_header_raise_error(self):
        header, baris = rk.baca_csv(CSV_HANYA_HEADER, is_text=True)
        with self.assertRaises(rk.DataError):
            rk.rekap(header, baris)

    def test_tanpa_kolom_tanggal_raise_error(self):
        header, baris = rk.baca_csv("Poli\nGigi\n", is_text=True)
        with self.assertRaises(rk.DataError):
            rk.rekap(header, baris)

    def test_file_tidak_ada(self):
        with self.assertRaises(rk.DataError):
            rk.baca_csv("/path/tidak/ada/kunjungan.csv")


class TesCLI(unittest.TestCase):
    def test_main_file_tidak_ada_exit_code_1(self):
        buf_err = io.StringIO()
        with redirect_stderr(buf_err):
            kode = rk.main(["--file", "/path/tidak/ada.csv"])
        self.assertEqual(kode, 1)
        self.assertIn("Error", buf_err.getvalue())

    def test_main_json_output(self):
        import tempfile, os
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".csv", delete=False, encoding="utf-8"
        ) as f:
            f.write(CSV_NORMAL)
            path = f.name
        try:
            buf_out = io.StringIO()
            with redirect_stdout(buf_out):
                kode = rk.main(["--file", path, "--format", "json"])
            self.assertEqual(kode, 0)
            data = json.loads(buf_out.getvalue())
            self.assertEqual(data["total_baris"], 5)
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
