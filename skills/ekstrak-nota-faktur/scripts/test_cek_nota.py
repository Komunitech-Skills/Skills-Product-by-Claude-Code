#!/usr/bin/env python3
"""Uji regresi cek_nota.py. Jalankan: python3 test_cek_nota.py  (hanya library standar)."""
import csv
import datetime as dt
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal

SINI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SINI)
import cek_nota as cn  # noqa: E402

HARI_INI = dt.date(2026, 9, 23)
SCRIPT = os.path.join(SINI, "cek_nota.py")
CONTOH = os.path.join(SINI, "..", "templates", "contoh-input.json")


def cek(dok):
    return cn.cek_aman(dok, 1, HARI_INI)


def pesan(d):
    return " | ".join(h["pesan"] for h in d["hasil_cek"])


def jalan(*arg, stdin=None):
    p = subprocess.run([sys.executable, SCRIPT] + list(arg), input=stdin, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


class UjiAngka(unittest.TestCase):
    def test_parse(self):
        self.assertEqual(cn.parse_angka("Rp 1.250.000"), 1250000)
        self.assertEqual(cn.parse_angka("15.000,50"), Decimal("15000.50"))
        self.assertEqual(cn.parse_angka("25.000,-"), 25000)
        self.assertEqual(cn.parse_angka("1,5jt"), 1500000)
        with self.assertRaises(cn.GalatInput):
            cn.parse_angka("1,250,000.00")

    def test_terbilang_bolak_balik(self):
        for n in (0, 11, 100, 1000, 1011, 1001000, 8800000, 999999999999):
            self.assertEqual(cn.baca_terbilang(cn.terbilang(n)), n)
        self.assertEqual(cn.baca_terbilang("# Satu Juta Seratus Sepuluh Ribu Rupiah saja #"), 1110000)


class UjiPPN(unittest.TestCase):
    def test_non_mewah_2026_benar(self):
        d = cek({"jenis": "faktur_pajak", "tanggal": "2026-09-10", "dpp": "4.500.000", "ppn": "495.000",
                 "nsfp": "04.00.26.00001234567", "penjual": {"npwp": "0012345678012345"}})
        self.assertEqual(d["status_cek"], "COCOK")
        self.assertEqual(d["ppn_seharusnya"], 495000)

    def test_12_penuh_diberi_ppn_dan_total_seharusnya(self):
        d = cek({"jenis": "invoice", "tanggal": "2026-09-12", "subtotal": "8.000.000", "dpp": "8.000.000",
                 "ppn": "960.000", "pph": "160.000", "total": "8.800.000"})
        self.assertEqual(d["status_cek"], "PERLU DICEK")
        self.assertEqual(d["ppn_seharusnya"], 880000)
        self.assertEqual(d["total_seharusnya"], 8720000)
        self.assertIn("Rp 8.720.000", pesan(d))

    def test_tarif_menurut_tanggal(self):
        self.assertEqual(cek({"tanggal": "2024-12-01", "dpp": "1.000.000", "ppn": "110.000", "total": "1.110.000"})
                         ["status_cek"], "COCOK")
        self.assertEqual(cek({"tanggal": "2021-06-01", "dpp": "1.000.000", "ppn": "100.000", "total": "1.100.000"})
                         ["status_cek"], "COCOK")

    def test_selisih_rp1_pakai_angka_dokumen(self):
        d = cek({"jenis": "struk", "tanggal": "2026-09-05", "harga_termasuk_ppn": True, "subtotal": "127.900",
                 "dpp": "115.225", "ppn": "12.675", "total": "127.900"})
        self.assertEqual(d["status_cek"], "COCOK")
        self.assertEqual(d["ppn_seharusnya"], 12675)


class UjiRegresiHasilUji(unittest.TestCase):
    def test_angka_hitungan_tidak_masuk_kolom_dokumen(self):
        d = cek({"tanggal": "2026-09-01", "item": [{"nama": "A", "qty": 2, "harga_satuan": "10.000", "jumlah": "20.000"}],
                 "ppn": "2.200", "total": "22.200"})
        self.assertIsNone(d["subtotal"])
        self.assertEqual(d["subtotal_dihitung"], 20000)
        self.assertIsNone(d["dpp"])
        self.assertEqual(d["dpp_dihitung"], 20000)
        teks = cn.ke_csv([d], "dokumen", ";", "koma", False)
        baris = list(csv.DictReader(io.StringIO(teks), delimiter=";"))[0]
        self.assertEqual(baris["Subtotal"], "")
        self.assertEqual(baris["DPP"], "")
        self.assertEqual(baris["Subtotal Dihitung Script"], "20000")
        self.assertEqual(baris["DPP Dihitung Script"], "20000")

    def test_npwp_15_digit_faktur_2024_bukan_peringatan(self):
        d = cek({"jenis": "faktur_pajak", "tanggal": "2024-12-10", "nsfp": "010.000-24.12345678",
                 "penjual": {"npwp": "01.234.567.8-901.234"}, "dpp": "1.000.000", "ppn": "110.000"})
        self.assertEqual(d["status_cek"], "COCOK", pesan(d))
        d2 = cek({"jenis": "faktur_pajak", "tanggal": "2026-01-10", "nsfp": "04.00.26.00001234567",
                  "penjual": {"npwp": "01.234.567.8-901.234"}, "dpp": "1.000.000", "ppn": "110.000"})
        self.assertEqual(d2["status_cek"], "PERLU DICEK")

    def test_penanda_tidak_terbaca_konsisten(self):
        d = cek({"tanggal": "TIDAK_TERBACA", "nomor": "?", "penjual": {"nama": "X", "npwp": "buram"},
                 "total": "tidak terbaca"})
        teks = cn.ke_csv([d], "dokumen", ";", "koma", False)
        baris = list(csv.DictReader(io.StringIO(teks), delimiter=";"))[0]
        for kol in ("Tanggal", "Nomor Dokumen", "NPWP Penjual", "Total"):
            self.assertEqual(baris[kol], cn.TIDAK_TERBACA, kol)
        self.assertNotIn("TIDAK TERBACA", baris.values())
        self.assertIsNone(d["total_rekap"])

    def test_satu_dokumen_rusak_tidak_gagalkan_batch(self):
        data = {"dokumen": [
            {"id": "OK1", "tanggal": "2026-09-01", "total": "10.000"},
            {"id": "RUSAK", "tanggal": "31/02/2026", "total": "10.000"},
            {"id": "RUSAK2", "total": "1,250,000.00"},
            "bukan objek",
            {"id": "OK2", "tanggal": "2026-09-02", "total": "5.000"}]}
        kode, out, err = jalan("-", "--format", "json", stdin=json.dumps(data))
        self.assertEqual(kode, 1, err)
        hasil = json.loads(out)
        status = {d["id"]: d["status_cek"] for d in hasil["dokumen"]}
        self.assertEqual(status["RUSAK"], cn.STATUS_INVALID)
        self.assertEqual(status["RUSAK2"], cn.STATUS_INVALID)
        self.assertEqual(status["D4"], cn.STATUS_INVALID)
        self.assertEqual(hasil["rekap"]["total_pengeluaran"], 15000)
        self.assertEqual(sorted(hasil["rekap"]["tidak_valid"]), ["D4", "RUSAK", "RUSAK2"])
        self.assertIn("tidak valid", err)

    def test_petunjuk_terbilang_bila_total_tidak_terbaca(self):
        d = cek({"jenis": "kuitansi", "tanggal": "2026-09-01", "total": "TIDAK_TERBACA",
                 "terbilang": "Tiga juta seratus ribu rupiah"})
        self.assertIn("Rp 3.100.000", pesan(d))
        self.assertEqual(d["total"], cn.TIDAK_TERBACA)
        self.assertIsNone(d["total_rekap"])

    def test_faktur_tanpa_total_ditandai_dihitung(self):
        kode, out, _ = jalan(CONTOH, "--hari-ini", "2026-09-23")
        self.assertEqual(kode, 0)
        self.assertIn("Rp 4.995.000 (dihitung)", out)

    def test_jatuh_tempo_rekening(self):
        d = cek({"jenis": "invoice", "tanggal": "2026-09-01", "total": "1.000", "jatuh_tempo": "2026-10-01",
                 "rekening_tujuan": "1234567890"})
        teks = cn.ke_csv([d], "dokumen", ";", "koma", False)
        baris = list(csv.DictReader(io.StringIO(teks), delimiter=";"))[0]
        self.assertEqual(baris["Jatuh Tempo"], "2026-10-01")
        self.assertEqual(baris["Rekening Tujuan"], '="1234567890"')


class UjiCLI(unittest.TestCase):
    def test_contoh_semua_format(self):
        for arg in ([], ["--format", "json"], ["--format", "csv"], ["--format", "csv", "--csv", "item", "--pemisah", "tab"],
                    ["--format", "csv", "--pemisah", ","]):
            kode, out, err = jalan(CONTOH, "--hari-ini", "2026-09-23", *arg)
            self.assertEqual(kode, 0, err)
            self.assertTrue(out.strip())

    def test_error_fatal(self):
        with tempfile.TemporaryDirectory() as tmp:
            rusak = os.path.join(tmp, "r.json")
            with open(rusak, "w") as fh:
                fh.write("{bad")
            self.assertEqual(jalan(rusak)[0], 2)
        self.assertEqual(jalan("tidak-ada.json")[0], 2)
        self.assertEqual(jalan()[0], 2)
        self.assertEqual(jalan("-", stdin="[]")[0], 2)
        self.assertEqual(jalan(CONTOH, "--pemisah", "x")[0], 2)


if __name__ == "__main__":
    unittest.main(verbosity=1)
