#!/usr/bin/env python3
"""Tes untuk skor_ide.py. Jalankan: python3 test_skor_ide.py (atau `python -m unittest`)."""
import contextlib
import io
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


class TesBugKolomBerlebihTinggi(unittest.TestCase):
    """Regresi temuan TINGGI #1: koma desimal tanpa kutip menggeser kolom diam-diam."""

    def test_baris_kedua_koma_desimal_tanpa_kutip_ditolak(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ide.csv"
            tulis(p, "nama_ide,a,b\nIde X,3,4\nIde Y,3,5,4\n")
            with self.assertRaises(modul.DataTidakValid) as cm:
                modul.baca_ide(p, ["a", "b"])
            pesan = str(cm.exception)
            self.assertIn("baris 3", pesan)
            self.assertIn("kolom", pesan)

    def test_baris_pertama_koma_desimal_tanpa_kutip_ditolak(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ide.csv"
            tulis(p, "nama_ide,a,b\nIde Y,3,5,4\n")
            with self.assertRaises(modul.DataTidakValid) as cm:
                modul.baca_ide(p, ["a", "b"])
            self.assertIn("baris 2", str(cm.exception))

    def test_baris_kolom_kurang_ditolak(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ide.csv"
            tulis(p, "nama_ide,a,b\nIde X,3,4\nIde Y,3\n")
            with self.assertRaises(modul.DataTidakValid) as cm:
                modul.baca_ide(p, ["a", "b"])
            self.assertIn("baris 3", str(cm.exception))

    def test_koma_desimal_berkutip_diterima(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ide.csv"
            tulis(p, 'nama_ide,a,b\nIde 1,"3,5",4\n')
            hasil = modul.baca_ide(p, ["a", "b"])
            self.assertAlmostEqual(hasil[0]["skor_kriteria"]["a"], 3.5)


class TesCsvExcelIndonesia(unittest.TestCase):
    """Regresi temuan SEDANG #2: BOM, pemisah ';', koma desimal."""

    def test_bom_dan_pemisah_titik_koma_diterima(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ide.csv"
            teks = "nama_ide;a;b\nIde 1;3,5;4\n"
            Path(p).write_bytes(b"\xef\xbb\xbf" + teks.encode("utf-8"))
            hasil = modul.baca_ide(p, ["a", "b"])
            self.assertEqual(hasil[0]["nama_ide"], "Ide 1")
            self.assertAlmostEqual(hasil[0]["skor_kriteria"]["a"], 3.5)
            self.assertAlmostEqual(hasil[0]["skor_kriteria"]["b"], 4.0)

    def test_header_dengan_spasi_dirapikan(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ide.csv"
            tulis(p, "nama_ide, a , b \nIde 1,3,4\n")
            hasil = modul.baca_ide(p, ["a", "b"])
            self.assertEqual(hasil[0]["skor_kriteria"], {"a": 3.0, "b": 4.0})


class TesBobotNanInfBool(unittest.TestCase):
    """Regresi temuan SEDANG #3: NaN/Infinity dan boolean di file bobot."""

    def test_bobot_nan_ditolak(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "bobot.json"
            tulis(p, '{"a": NaN}')
            with self.assertRaises(modul.DataTidakValid):
                modul.baca_bobot(p)

    def test_bobot_infinity_ditolak(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "bobot.json"
            tulis(p, '{"a": Infinity}')
            with self.assertRaises(modul.DataTidakValid):
                modul.baca_bobot(p)

    def test_bobot_boolean_ditolak(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "bobot.json"
            tulis(p, '{"a": true}')
            with self.assertRaises(modul.DataTidakValid):
                modul.baca_bobot(p)


class TesNilaiIdeNanInfinity(unittest.TestCase):
    def test_nilai_infinity_ditolak(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ide.csv"
            tulis(p, "nama_ide,a\nIde 1,Infinity\n")
            with self.assertRaises(modul.DataTidakValid):
                modul.baca_ide(p, ["a"])


class TesEncodingDanPath(unittest.TestCase):
    """Regresi temuan RENDAH #8: pesan ramah untuk file bukan UTF-8 dan path folder."""

    def test_encoding_cp1252_fallback(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ide.csv"
            teks = "nama_ide,a\nKafe & Kue Nona,3\n"
            Path(p).write_bytes(teks.encode("cp1252"))
            hasil = modul.baca_ide(p, ["a"])
            self.assertEqual(hasil[0]["nama_ide"], "Kafe & Kue Nona")

    def test_path_folder_pesan_ramah(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(modul.DataTidakValid) as cm:
                modul.baca_ide(d, ["a"])
            self.assertIn("folder", str(cm.exception))


class TesParseRupiah(unittest.TestCase):
    """Regresi temuan RENDAH #8: format rupiah Indonesia untuk --modal/--margin."""

    def test_angka_biasa(self):
        self.assertEqual(modul.parse_rupiah("5000000"), 5_000_000.0)

    def test_format_ribuan_titik(self):
        self.assertEqual(modul.parse_rupiah("5.000.000"), 5_000_000.0)

    def test_prefiks_rp(self):
        self.assertEqual(modul.parse_rupiah("Rp5.000.000"), 5_000_000.0)
        self.assertEqual(modul.parse_rupiah("rp 5.000.000"), 5_000_000.0)

    def test_singkatan_jt_rb(self):
        self.assertEqual(modul.parse_rupiah("5jt"), 5_000_000.0)
        self.assertEqual(modul.parse_rupiah("15rb"), 15_000.0)

    def test_desimal_titik_tetap_desimal(self):
        self.assertAlmostEqual(modul.parse_rupiah("2500.5"), 2500.5)

    def test_nan_infinity_ditolak(self):
        with self.assertRaises(modul.DataTidakValid):
            modul.parse_rupiah("nan")
        with self.assertRaises(modul.DataTidakValid):
            modul.parse_rupiah("inf")

    def test_kosong_ditolak(self):
        with self.assertRaises(modul.DataTidakValid):
            modul.parse_rupiah("   ")

    def test_bukan_angka_ditolak(self):
        with self.assertRaises(modul.DataTidakValid):
            modul.parse_rupiah("banyak sekali")


class TesFormatRupiah(unittest.TestCase):
    def test_bilangan_bulat(self):
        self.assertEqual(modul.format_rupiah(2500), "Rp2.500")

    def test_dengan_desimal(self):
        self.assertEqual(modul.format_rupiah(2500.5), "Rp2.500,50")


class TesMarginModalKurangDariSatuRupiah(unittest.TestCase):
    """Regresi temuan RENDAH #9: margin dibulatkan tampil Rp0 tanpa penjelasan."""

    def test_margin_kurang_dari_satu_ditolak(self):
        with self.assertRaises(modul.DataTidakValid):
            modul.hitung_impas(1_000_000, 0.1)

    def test_modal_kurang_dari_satu_ditolak(self):
        with self.assertRaises(modul.DataTidakValid):
            modul.hitung_impas(0.5, 10_000)

    def test_nan_ditolak(self):
        with self.assertRaises(modul.DataTidakValid):
            modul.hitung_impas(float("nan"), 10_000)
        with self.assertRaises(modul.DataTidakValid):
            modul.hitung_impas(1_000_000, float("inf"))


class TesBobotDefaultDanSamaRata(unittest.TestCase):
    """Regresi temuan SEDANG #6: script bisa jalan tanpa file bobot."""

    def test_tanpa_bobot_kolom_default_dipakai(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ide.csv"
            tulis(
                p,
                "nama_ide,kesesuaian_modal,potensi_permintaan,kemudahan_eksekusi,kecocokan_keahlian,potensi_margin\n"
                "Ide 1,5,4,3,2,4\n"
                "Ide 2,3,3,3,3,3\n",
            )
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                kode = modul.main(["skor", "--ide", str(p)])
            self.assertEqual(kode, 0)
            self.assertIn("default resmi", buf.getvalue())

    def test_tanpa_bobot_kolom_custom_sama_rata(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ide.csv"
            tulis(p, "nama_ide,x,y\nIde 1,5,3\nIde 2,2,4\n")
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                kode = modul.main(["skor", "--ide", str(p)])
            self.assertEqual(kode, 0)
            self.assertIn("sama rata", buf.getvalue())


class TesDuplikatNamaFleksibel(unittest.TestCase):
    """Regresi temuan RENDAH #13: duplikat nama beda huruf/spasi tidak terdeteksi."""

    def test_duplikat_beda_huruf_dan_spasi_terdeteksi(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ide.csv"
            tulis(p, "nama_ide,a\nIde X,3\nide   x ,4\n")
            with self.assertRaises(modul.DataTidakValid) as cm:
                modul.baca_ide(p, ["a"])
            self.assertIn("duplikat", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
