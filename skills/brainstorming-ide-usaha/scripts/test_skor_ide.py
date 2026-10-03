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


class TesHeaderKolomKembar(unittest.TestCase):
    """Regresi temuan uji ulang v1.0.1 B-5: header kolom kembar diterima
    diam-diam (nilai kolom terakhir menimpa) -> harus ditolak dengan galat
    jelas."""

    def test_header_kolom_kembar_ditolak(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ide.csv"
            tulis(p, "nama_ide,a,a\nIde X,1,5\n")
            with self.assertRaises(modul.DataTidakValid) as cm:
                modul.baca_ide(p, ["a"])
            pesan = str(cm.exception)
            self.assertIn("kembar", pesan)
            self.assertIn("baris 1", pesan)

    def test_header_kolom_kembar_beda_huruf_besar_ditolak(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ide.csv"
            tulis(p, "nama_ide,Skor_A,skor a\nIde X,1,5\n")
            with self.assertRaises(modul.DataTidakValid) as cm:
                modul.baca_ide(p, ["a"])
            self.assertIn("kembar", str(cm.exception))


class TesCocokkanBobotDefaultFleksibel(unittest.TestCase):
    """Regresi temuan uji ulang v1.0.1 B-2: nama kolom default salah huruf
    besar/spasi/garis bawah harus tetap dikenali sebagai bobot default (tanpa
    diam-diam jatuh ke sama rata), dan kalau memang tidak cocok sama sekali
    harus muncul PERINGATAN eksplisit, bukan diam-diam."""

    def test_kolom_default_beda_huruf_besar_dan_spasi_tetap_dipakai(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ide.csv"
            tulis(
                p,
                "nama_ide,Kesesuaian_Modal,Potensi Permintaan,kemudahan_eksekusi,"
                "kecocokan_keahlian,potensi_margin\n"
                "Ide 1,5,4,3,2,4\n"
                "Ide 2,3,3,3,3,3\n",
            )
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                kode = modul.main(["skor", "--ide", str(p)])
            keluaran = buf.getvalue()
            self.assertEqual(kode, 0)
            self.assertIn("default resmi", keluaran)
            self.assertNotIn("PERINGATAN", keluaran)
            # Skor harus sama persis dengan bobot default asli: nilai Ide 1
            # (5,4,3,2,4) x bobot (5,4,3,2,4) / 18 = (25+16+9+4+16)/18 = 3,889
            self.assertIn("3.889", keluaran)

    def test_kolom_tidak_cocok_bobot_default_dapat_peringatan_eksplisit(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ide.csv"
            tulis(p, "nama_ide,x,y\nIde 1,5,3\nIde 2,2,4\n")
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                kode = modul.main(["skor", "--ide", str(p)])
            keluaran = buf.getvalue()
            self.assertEqual(kode, 0)
            self.assertTrue(keluaran.startswith("PERINGATAN"))
            self.assertIn("SAMA RATA", keluaran)


class TesNomorBarisFisik(unittest.TestCase):
    """Regresi temuan uji ulang v1.0.1 B-1: nomor baris di pesan error salah
    setelah ada baris kosong di tengah file (baris kosong dibuang sebelum
    penomoran)."""

    def test_nomor_baris_benar_setelah_baris_kosong(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ide.csv"
            tulis(p, "nama_ide,a,b\n\n\nIde Y,3,9\n")  # baris data di baris fisik ke-4
            with self.assertRaises(modul.DataTidakValid) as cm:
                modul.baca_ide(p, ["a", "b"])
            self.assertIn("baris 4", str(cm.exception))


class TesHeaderNamaIdeHurufBesar(unittest.TestCase):
    """Regresi temuan uji ulang v1.0.1 B-3: header 'Nama_Ide'/'NAMA IDE'
    ditolak padahal maksudnya sama dengan 'nama_ide'."""

    def test_header_nama_ide_huruf_besar_diterima(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ide.csv"
            tulis(p, "Nama_Ide,a\nIde 1,3\n")
            hasil = modul.baca_ide(p, ["a"])
            self.assertEqual(hasil[0]["nama_ide"], "Ide 1")

    def test_header_nama_ide_spasi_diterima(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ide.csv"
            tulis(p, "NAMA IDE,a\nIde 1,3\n")
            hasil = modul.baca_ide(p, ["a"])
            self.assertEqual(hasil[0]["nama_ide"], "Ide 1")


class TesKolomTanpaNamaDiUjung(unittest.TestCase):
    """Regresi temuan uji ulang v1.0.1 B-4: koma di ujung tiap baris (kolom
    kosong ekor ala Excel) memberi pesan membingungkan ("tidak ada di file
    bobot: ['']")."""

    def test_koma_ekor_kosong_dibuang_otomatis(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ide.csv"
            tulis(p, "nama_ide,a,b,\nIde 1,3,4,\nIde 2,1,2,\n")
            hasil = modul.baca_ide(p, ["a", "b"])
            self.assertEqual(len(hasil), 2)
            self.assertEqual(hasil[0]["skor_kriteria"], {"a": 3.0, "b": 4.0})

    def test_koma_ekor_berisi_data_ditolak_jelas(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "ide.csv"
            tulis(p, "nama_ide,a,b,\nIde 1,3,4,oops\n")
            with self.assertRaises(modul.DataTidakValid) as cm:
                modul.baca_ide(p, ["a", "b"])
            pesan = str(cm.exception)
            self.assertIn("tidak punya nama", pesan)
            self.assertIn("baris 1", pesan)


class TesModalMarginNegatifCli(unittest.TestCase):
    """Regresi temuan uji ulang v1.0.1 B-6: '--modal -5jt' menampilkan pesan
    argparse bawaan Bahasa Inggris ("expected one argument"), bukan pesan
    Bahasa Indonesia yang jelas."""

    def test_modal_negatif_singkatan_pesan_indonesia(self):
        kode_keluar = modul.main(["impas", "--modal", "-5jt", "--margin", "5000"])
        self.assertEqual(kode_keluar, 1)

    def test_margin_negatif_singkatan_pesan_indonesia(self):
        kode_keluar = modul.main(["impas", "--modal", "5jt", "--margin", "-1000"])
        self.assertEqual(kode_keluar, 1)

    def test_modal_negatif_dengan_sama_dengan_tetap_jalan(self):
        kode_keluar = modul.main(["impas", "--modal=-5jt", "--margin", "5000"])
        self.assertEqual(kode_keluar, 1)


class TesRencanaUji7Hari(unittest.TestCase):
    """v1.0.5: hitungan rupiah rencana uji 7 hari (angka diverifikasi manual)."""

    def test_angka_dasar(self):
        r = modul.hitung_rencana(25000, 14000, 20, 300000, 30, 1500000)
        self.assertEqual(r["potongan_rp"], 5000)          # 25.000 x 20%
        self.assertEqual(r["margin_unit"], 6000)          # 25.000 - 5.000 - 14.000
        self.assertEqual(r["margin_persen"], 24.0)
        self.assertEqual(r["laba_uji"], -120000)          # 30 x 6.000 - 300.000
        self.assertEqual(r["unit_tutup_biaya"], 50)       # ceil(300.000 / 6.000)
        self.assertEqual(r["unit_impas_modal"], 250)      # ceil(1.500.000 / 6.000)
        self.assertEqual(r["target_kumulatif"], {3: 9, 5: 18, 7: 30})
        self.assertEqual(r["ambang_perbaiki"], 9)

    def test_potongan_dibulatkan_rupiah_terdekat(self):
        r = modul.hitung_rencana(9999, 5000, 20)
        self.assertEqual(r["potongan_rp"], 2000)          # 1.999,8 -> 2.000
        self.assertEqual(r["margin_unit"], 2999)

    def test_rugi_per_unit_ditandai(self):
        r = modul.hitung_rencana(10000, 9000, 20)
        self.assertTrue(r["rugi_per_unit"])
        self.assertIsNone(r["unit_tutup_biaya"])

    def test_input_buruk(self):
        for argumen in [(0, 1000), (10000, -1), (10000, 1000, 100), (10000, 1000, -5),
                        (10000, 1000, 0, -1), (10000, 1000, 0, 0, 0), (float("nan"), 1000)]:
            with self.assertRaises(modul.DataTidakValid, msg=str(argumen)):
                modul.hitung_rencana(*argumen)

    def test_cli_format_indonesia(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = modul.main(["rencana", "--harga", "Rp25.000", "--modal-unit", "14rb",
                             "--potongan-persen", "20,5%", "--biaya-uji", "300rb", "--target", "30"])
        out = buf.getvalue()
        self.assertEqual(rc, 0)
        self.assertIn("20,5% = Rp5.125", out)
        self.assertIn("Rp5.875 (23,5% dari harga)", out)
        self.assertIn("-Rp123.750", out)                  # 30 x 5.875 - 300.000
        self.assertIn("Hari 3 >= 9, Hari 5 >= 18, Hari 7 >= 30", out)
        self.assertIn("PERINGATAN: target 7 hari belum menutup biaya uji", out)

    def test_cli_rugi(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            modul.main(["rencana", "--harga", "10rb", "--modal-unit", "9rb", "--potongan-persen", "20"])
        self.assertIn("RUGI", buf.getvalue())


class TesIdeDariStdin(unittest.TestCase):
    """v1.0.5: skor tanpa menulis file (--ide -), supaya tidak ada CSV nyasar di folder skill."""

    def test_stdin(self):
        import sys as _sys
        data = ("nama_ide,kesesuaian_modal,potensi_permintaan,kemudahan_eksekusi,kecocokan_keahlian,potensi_margin\n"
                "Kilat,5,4,4,4,4\nAntar,4,4,4,4,4\n").encode("utf-8")

        class _Stdin:
            buffer = io.BytesIO(data)

        lama_stdin, modul._STDIN_CACHE = _sys.stdin, None
        _sys.stdin = _Stdin()
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                rc = modul.main(["skor", "--ide", "-"])
        finally:
            _sys.stdin, modul._STDIN_CACHE = lama_stdin, None
        self.assertEqual(rc, 0)
        self.assertIn("4.278", buf.getvalue())            # (5*5+4*4+4*3+4*2+4*4)/18 = 77/18


class TesKewajaranHarga(unittest.TestCase):
    """v1.0.6: saran harga wajib dicek kewajarannya (uji OpenClaw 2026-10-01: paket Rp8-9rb/kg
    padahal harga sendiri Rp6rb/kg dan pesaing Rp5rb/kg)."""

    def test_paket_laundry_terlalu_mahal_ditandai(self):
        r = modul.hitung_rencana(120000, 48000, 0, 200000, 10, isi_per_unit=15, satuan="kg",
                                 harga_lama=6000, harga_pesaing=5000)
        self.assertEqual(r["harga_per_satuan"], 8000)       # 120.000 / 15
        self.assertEqual(r["modal_per_satuan"], 3200)       # 48.000 / 15
        self.assertEqual(r["selisih_vs_lama_persen"], 33.3)  # (8.000-6.000)/6.000
        self.assertEqual(r["selisih_vs_pesaing_persen"], 60.0)
        self.assertEqual(r["kewajaran"], "CEK")
        self.assertEqual(len(r["catatan_kewajaran"]), 2)

    def test_harga_dari_biaya_plus_margin(self):
        r = modul.hitung_rencana(None, 48000, 0, 200000, 10, margin_target=30, isi_per_unit=15,
                                 satuan="kg", harga_lama=6000, harga_pesaing=5000)
        self.assertEqual(r["harga"], 68572)                 # ceil(48.000 / 0,7) = ceil(68.571,43)
        self.assertEqual(r["harga_saran"], 68572)
        self.assertEqual(r["harga_per_satuan"], 4571)       # 68.572 / 15 = 4.571,47
        self.assertEqual(r["kewajaran"], "WAJAR")
        self.assertEqual(r["margin_unit"], 20572)

    def test_harga_saran_dengan_potongan(self):
        r = modul.hitung_rencana(None, 14000, 20, margin_target=25)
        self.assertEqual(r["harga"], 25455)                 # ceil(14.000 / 0,55) = ceil(25.454,5)
        self.assertEqual(r["potongan_rp"], 5091)            # 25.455 x 20% = 5.091
        self.assertEqual(r["kewajaran"], "BELUM DICEK")

    def test_harga_di_bawah_margin_target(self):
        r = modul.hitung_rencana(60000, 48000, 0, margin_target=30)
        self.assertTrue(any("di bawah harga minimal" in c for c in r["catatan_kewajaran"]))

    def test_berhenti_dini(self):
        r = modul.hitung_rencana(25000, 14000, 0, 0, 30)
        self.assertEqual(r["berhenti_dini"], {3: 0, 5: 9})

    def test_input_buruk(self):
        for kw in [dict(margin_target=-1), dict(margin_target=100), dict(isi_per_unit=0),
                   dict(harga_pesaing=-5000), dict(harga_lama=0)]:
            with self.assertRaises(modul.DataTidakValid, msg=str(kw)):
                modul.hitung_rencana(10000, 1000, **kw)
        with self.assertRaises(modul.DataTidakValid):
            modul.hitung_rencana(None, 1000)                # tanpa harga & tanpa margin target
        with self.assertRaises(modul.DataTidakValid):
            modul.hitung_rencana(None, 1000, 60, margin_target=40)

    def test_cli(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = modul.main(["rencana", "--harga", "120rb", "--modal-unit", "48rb", "--isi-per-unit", "15",
                             "--satuan", "kg", "--harga-lama", "Rp6.000", "--harga-pesaing", "5rb"])
        out = buf.getvalue()
        self.assertEqual(rc, 0)
        self.assertIn("Harga per kg                  : Rp8.000", out)
        self.assertIn("Rp6.000 (selisih +33,3%)", out)
        self.assertIn("PERINGATAN HARGA", out)
        self.assertIn("Hari 5 < 3 -> hentikan uji", out)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            modul.main(["rencana", "--harga", "25rb", "--modal-unit", "14rb"])
        self.assertIn("BELUM DICEK - isi [isi: harga pesaing per unit]", buf.getvalue())
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(modul.main(["rencana", "--modal-unit", "14rb"]), 1)


class TesKonsistensiV107(unittest.TestCase):
    """v1.0.7: saran harga <= harga lama = efektif turun harga (jangan "bukan turun harga"); target uji
    dikaitkan ke gap omzet; SKILL.md memuat ATURAN WAJIB & larangan /tmp."""

    def test_paket_sama_dengan_pesaing_ditandai_turun_harga(self):
        r = modul.hitung_rencana(75000, 52000, 0, 300000, 14, isi_per_unit=15, satuan="kg",
                                 harga_lama=6000, harga_pesaing=5000)
        self.assertEqual(r["harga_per_satuan"], 5000)
        self.assertEqual(len(r["catatan_konsistensi"]), 1)
        self.assertIn("TURUN HARGA", r["catatan_konsistensi"][0])
        self.assertIn("kanibalisasi", r["catatan_konsistensi"][0])

    def test_harga_di_atas_acuan_tidak_ada_catatan_turun_harga(self):
        r = modul.hitung_rencana(30000, 15000, 0, 0, 10, isi_per_unit=1, harga_lama=25000)
        self.assertEqual(r["catatan_konsistensi"], [])

    def test_gap_omzet(self):
        r = modul.hitung_rencana(75000, 52000, 0, 300000, 14, gap_omzet=2700000)
        self.assertEqual(r["omzet_bulan_proyeksi"], 4500000)   # 14 x 75.000 = 1.050.000; x 30/7
        self.assertEqual(r["tutup_gap_persen"], 166.7)         # 4.500.000 / 2.700.000
        self.assertIn("gap omzet", r["catatan_konsistensi"][0])
        with self.assertRaises(modul.DataTidakValid):
            modul.hitung_rencana(75000, 52000, gap_omzet=0)

    def test_cli_konsistensi(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = modul.main(["rencana", "--harga", "75rb", "--modal-unit", "52rb", "--biaya-uji", "300rb",
                             "--target", "14", "--isi-per-unit", "15", "--satuan", "kg", "--harga-lama", "6rb",
                             "--harga-pesaing", "5rb", "--gap-omzet", "2,7jt"])
        self.assertEqual(rc, 0)
        self.assertIn("KONSISTENSI:", buf.getvalue())
        self.assertIn("TURUN HARGA", buf.getvalue())

    def test_skill_md_aturan_wajib(self):
        folder = Path(__file__).resolve().parent.parent
        sk = (folder / "SKILL.md").read_text(encoding="utf-8")
        awal = sk.split("## Tujuan")[0]
        self.assertIn("ATURAN WAJIB", awal)
        for frasa in ("/tmp", "[isi:", "KONSISTENSI", "--gap-omzet"):
            self.assertIn(frasa, awal)


class TesSkillTanpaPasalPidanaUsang(unittest.TestCase):
    """v1.0.6: SKILL.md tidak mengutip pasal KUHP lama dan melarang pasal pidana tanpa diminta."""

    def test_skill_md(self):
        folder = Path(__file__).resolve().parent.parent
        sk = (folder / "SKILL.md").read_text(encoding="utf-8")
        self.assertNotIn("378", sk)
        self.assertNotIn("372", sk)
        self.assertIn("references/rujukan-kasus-terlarang.md", sk)
        ref = (folder / "references" / "rujukan-kasus-terlarang.md").read_text(encoding="utf-8")
        self.assertIn("Pasal 492", ref)
        self.assertIn("Pasal 486", ref)


if __name__ == "__main__":
    unittest.main()
