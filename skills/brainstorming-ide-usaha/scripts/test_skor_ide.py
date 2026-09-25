#!/usr/bin/env python3
"""Tes untuk skor_ide.py. Jalankan: python3 test_skor_ide.py (atau `python -m unittest`)."""
import json
import math
import tempfile
import unittest
from pathlib import Path

import skor_ide as modul


def tulis(path, teks):
    Path(path).write_text(teks, encoding="utf-8")


class TesBacaBobot(unittest.TestCase):
    def test_bobot_valid(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "bobot.json"
            tulis(p, json.dumps({"a": 3, "b": 5}))
            self.assertEqual(modul.baca_bobot(p), {"a": 3.0, "b": 5.0})

    def test_bobot_kosong(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "bobot.json"
            tulis(p, "{}")
            with self.assertRaises(modul.DataTidakValid):
                modul.baca_bobot(p)

    def test_bobot_negatif(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "bobot.json"
            tulis(p, json.dumps({"a": -1}))
            with self.assertRaises(modul.DataTidakValid):
                modul.baca_bobot(p)

    def test_bobot_nol(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "bobot.json"
            tulis(p, json.dumps({"a": 0}))
            with self.assertRaises(modul.DataTidakValid):
                modul.baca_bobot(p)

    def test_bobot_bukan_angka(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "bobot.json"
            tulis(p, json.dumps({"a": "banyak"}))
            with self.assertRaises(modul.DataTidakValid):
                modul.baca_bobot(p)

    def test_bobot_json_rusak(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "bobot.json"
            tulis(p, "{tidak valid")
            with self.assertRaises(modul.DataTidakValid):
                modul.baca_bobot(p)

    def test_bobot_file_tidak_ada(self):
        with self.assertRaises(modul.DataTidakValid):
            modul.baca_bobot("/tidak/ada/file.json")


class TesBacaIde(unittest.TestCase):
    def test_ide_valid(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ide.csv"
            tulis(p, "nama_ide,a,b\nIde 1,3,4\nIde 2,5,2\n")
            hasil = modul.baca_ide(p, ["a", "b"])
            self.assertEqual(len(hasil), 2)
            self.assertEqual(hasil[0]["nama_ide"], "Ide 1")
            self.assertEqual(hasil[0]["skor_kriteria"], {"a": 3.0, "b": 4.0})

    def test_ide_kosong(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ide.csv"
            tulis(p, "nama_ide,a\n")
            with self.assertRaises(modul.DataTidakValid):
                modul.baca_ide(p, ["a"])

    def test_kolom_nama_ide_hilang(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ide.csv"
            tulis(p, "nama,a\nIde 1,3\n")
            with self.assertRaises(modul.DataTidakValid):
                modul.baca_ide(p, ["a"])

    def test_kriteria_tidak_cocok_kurang_di_ide(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ide.csv"
            tulis(p, "nama_ide,a\nIde 1,3\n")
            with self.assertRaises(modul.DataTidakValid):
                modul.baca_ide(p, ["a", "b"])

    def test_kriteria_tidak_cocok_lebih_di_ide(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ide.csv"
            tulis(p, "nama_ide,a,b\nIde 1,3,4\n")
            with self.assertRaises(modul.DataTidakValid):
                modul.baca_ide(p, ["a"])

    def test_nilai_di_luar_rentang(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ide.csv"
            tulis(p, "nama_ide,a\nIde 1,6\n")
            with self.assertRaises(modul.DataTidakValid):
                modul.baca_ide(p, ["a"])

    def test_nilai_nol_di_luar_rentang(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ide.csv"
            tulis(p, "nama_ide,a\nIde 1,0\n")
            with self.assertRaises(modul.DataTidakValid):
                modul.baca_ide(p, ["a"])

    def test_nilai_bukan_angka(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ide.csv"
            tulis(p, "nama_ide,a\nIde 1,tinggi\n")
            with self.assertRaises(modul.DataTidakValid):
                modul.baca_ide(p, ["a"])

    def test_nilai_kosong(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ide.csv"
            tulis(p, "nama_ide,a\nIde 1,\n")
            with self.assertRaises(modul.DataTidakValid):
                modul.baca_ide(p, ["a"])

    def test_nama_ide_kosong(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ide.csv"
            tulis(p, "nama_ide,a\n,3\n")
            with self.assertRaises(modul.DataTidakValid):
                modul.baca_ide(p, ["a"])

    def test_nama_ide_duplikat(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ide.csv"
            tulis(p, "nama_ide,a\nIde 1,3\nIde 1,4\n")
            with self.assertRaises(modul.DataTidakValid):
                modul.baca_ide(p, ["a"])

    def test_file_tidak_ada(self):
        with self.assertRaises(modul.DataTidakValid):
            modul.baca_ide("/tidak/ada/file.csv", ["a"])


class TesHitungSkor(unittest.TestCase):
    def test_peringkat_dan_nilai(self):
        ide = [
            {"nama_ide": "A", "skor_kriteria": {"x": 5, "y": 1}},
            {"nama_ide": "B", "skor_kriteria": {"x": 1, "y": 5}},
        ]
        bobot = {"x": 3, "y": 1}
        hasil = modul.hitung_skor(ide, bobot)
        # A: (5*3 + 1*1) / 4 = 4.0 ; B: (1*3 + 5*1) / 4 = 2.0
        self.assertEqual(hasil[0]["nama_ide"], "A")
        self.assertAlmostEqual(hasil[0]["skor_tertimbang"], 4.0)
        self.assertEqual(hasil[1]["nama_ide"], "B")
        self.assertAlmostEqual(hasil[1]["skor_tertimbang"], 2.0)
        self.assertEqual(hasil[0]["peringkat"], 1)
        self.assertEqual(hasil[1]["peringkat"], 2)

    def test_seri_terdeteksi(self):
        ide = [
            {"nama_ide": "A", "skor_kriteria": {"x": 3}},
            {"nama_ide": "B", "skor_kriteria": {"x": 3}},
            {"nama_ide": "C", "skor_kriteria": {"x": 1}},
        ]
        bobot = {"x": 1}
        hasil = modul.hitung_skor(ide, bobot)
        seri = modul.deteksi_seri(hasil)
        self.assertEqual(len(seri), 1)
        self.assertEqual(set(seri[0]), {"A", "B"})

    def test_tanpa_seri(self):
        ide = [
            {"nama_ide": "A", "skor_kriteria": {"x": 5}},
            {"nama_ide": "B", "skor_kriteria": {"x": 1}},
        ]
        hasil = modul.hitung_skor(ide, {"x": 1})
        self.assertEqual(modul.deteksi_seri(hasil), [])


class TesImpas(unittest.TestCase):
    def test_impas_pas(self):
        self.assertEqual(modul.hitung_impas(1_000_000, 10_000), 100)

    def test_impas_dibulatkan_ke_atas(self):
        self.assertEqual(modul.hitung_impas(1_000_000, 15_000), math.ceil(1_000_000 / 15_000))
        self.assertEqual(modul.hitung_impas(1_000_000, 15_000), 67)

    def test_modal_nol(self):
        with self.assertRaises(modul.DataTidakValid):
            modul.hitung_impas(0, 10_000)

    def test_modal_negatif(self):
        with self.assertRaises(modul.DataTidakValid):
            modul.hitung_impas(-500_000, 10_000)

    def test_margin_nol(self):
        with self.assertRaises(modul.DataTidakValid):
            modul.hitung_impas(1_000_000, 0)

    def test_margin_negatif(self):
        with self.assertRaises(modul.DataTidakValid):
            modul.hitung_impas(1_000_000, -1000)


class TesCliEndToEnd(unittest.TestCase):
    def test_cmd_skor_sukses(self):
        with tempfile.TemporaryDirectory() as d:
            ide_path = Path(d) / "ide.csv"
            bobot_path = Path(d) / "bobot.json"
            tulis(ide_path, "nama_ide,a,b\nIde 1,5,3\nIde 2,2,4\n")
            tulis(bobot_path, json.dumps({"a": 2, "b": 1}))
            kode = modul.main(["skor", "--ide", str(ide_path), "--bobot", str(bobot_path)])
            self.assertEqual(kode, 0)

    def test_cmd_skor_data_rusak(self):
        with tempfile.TemporaryDirectory() as d:
            ide_path = Path(d) / "ide.csv"
            bobot_path = Path(d) / "bobot.json"
            tulis(ide_path, "nama_ide,a\nIde 1,9\n")  # nilai di luar rentang
            tulis(bobot_path, json.dumps({"a": 1}))
            kode = modul.main(["skor", "--ide", str(ide_path), "--bobot", str(bobot_path)])
            self.assertEqual(kode, 1)

    def test_cmd_impas_sukses(self):
        kode = modul.main(["impas", "--modal", "5000000", "--margin", "15000"])
        self.assertEqual(kode, 0)

    def test_cmd_impas_gagal(self):
        kode = modul.main(["impas", "--modal", "0", "--margin", "15000"])
        self.assertEqual(kode, 1)


if __name__ == "__main__":
    unittest.main()
