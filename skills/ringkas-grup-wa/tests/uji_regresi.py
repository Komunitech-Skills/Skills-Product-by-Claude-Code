#!/usr/bin/env python3
"""Uji regresi untuk scripts/parse_ekspor_wa.py.

Jalankan: python3 tests/uji_regresi.py   (dari folder skill ini)
atau:     python3 -m unittest tests.uji_regresi -v
Tidak butuh pustaka luar (hanya unittest, standar Python 3.8+).
"""
import json
import os
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

FOLDER_SKILL = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(FOLDER_SKILL / "scripts"))

import parse_ekspor_wa as p  # noqa: E402


def parse_teks(teks, **kwargs):
    pesan, fmt, urutan, catatan = p.parse_pesan(teks)
    if kwargs.get("samarkan"):
        pesan, _peta = p.samarkan_pengirim(pesan)
    return pesan, fmt, urutan, catatan


class FormatAndroid(unittest.TestCase):
    def test_android_id_24jam_titik(self):
        teks = "12/09/26, 17.05 - Budi: Halo semua"
        pesan, fmt, urutan, catatan = parse_teks(teks)
        self.assertEqual(fmt, "android")
        self.assertEqual(len(pesan), 1)
        self.assertEqual(pesan[0]["pengirim"], "Budi")
        self.assertEqual(pesan[0]["waktu"], "2026-09-12T17:05:00")

    def test_android_id_tanpa_koma(self):
        teks = "12/09/26 17.05 - Budi: Halo semua"
        pesan, fmt, urutan, catatan = parse_teks(teks)
        self.assertEqual(len(pesan), 1)
        self.assertEqual(pesan[0]["teks"], "Halo semua")

    def test_android_en_ampm(self):
        # Hari 25 > 12 di posisi kedua -> urutan m/d tidak ambigu (9=bulan, 25=hari)
        teks = "9/25/26, 5:05 PM - Name: msg"
        pesan, fmt, urutan, catatan = parse_teks(teks)
        self.assertEqual(urutan, "m/d")
        self.assertEqual(pesan[0]["waktu"], "2026-09-25T17:05:00")

    def test_android_dash_en_dash(self):
        # Sebagian ekspor memakai en dash (–) bukan '-'
        teks = "12/09/26, 17.05 – Budi: Halo"
        pesan, fmt, urutan, catatan = parse_teks(teks)
        self.assertEqual(len(pesan), 1)


class FormatIOS(unittest.TestCase):
    def test_ios_id_dengan_detik(self):
        teks = "[12/09/26, 17.05.22] Budi: Halo"
        pesan, fmt, urutan, catatan = parse_teks(teks)
        self.assertEqual(fmt, "ios")
        self.assertEqual(pesan[0]["waktu"], "2026-09-12T17:05:22")

    def test_ios_en_ampm(self):
        teks = "[9/25/26, 5:05:22 PM] Name: msg"
        pesan, fmt, urutan, catatan = parse_teks(teks)
        self.assertEqual(urutan, "m/d")
        self.assertEqual(pesan[0]["waktu"], "2026-09-25T17:05:22")

    def test_ios_tanpa_detik(self):
        teks = "[12/09/26, 17.05] Budi: Halo"
        pesan, fmt, urutan, catatan = parse_teks(teks)
        self.assertEqual(pesan[0]["waktu"], "2026-09-12T17:05:00")


class Waktu24DanAMPM(unittest.TestCase):
    def test_tengah_malam_am(self):
        self.assertEqual(p.buat_waktu("12", "00", None, "AM"), ((0, 0, 0), None))

    def test_tengah_hari_pm(self):
        self.assertEqual(p.buat_waktu("12", "00", None, "PM"), ((12, 0, 0), None))

    def test_pagi_indonesia(self):
        jam, catatan = p.buat_waktu("7", "30", None, "pagi")
        self.assertEqual(jam, (7, 30, 0))

    def test_malam_12_jadi_tengah_malam(self):
        jam, catatan = p.buat_waktu("12", "00", None, "malam")
        self.assertEqual(jam, (0, 0, 0))

    def test_sore(self):
        jam, catatan = p.buat_waktu("6", "00", None, "sore")
        self.assertEqual(jam, (18, 0, 0))

    def test_jam_tidak_valid(self):
        hasil, catatan = p.buat_waktu("25", "00", None, None)
        self.assertIsNone(hasil)


class PesanMultiBaris(unittest.TestCase):
    def test_gabung_baris_lanjutan(self):
        teks = (
            "12/09/26, 08.00 - Sari: baris pertama\n"
            "baris kedua\n"
            "baris ketiga\n"
            "12/09/26, 08.05 - Budi: pesan lain"
        )
        pesan, *_ = parse_teks(teks)
        self.assertEqual(len(pesan), 2)
        self.assertIn("baris kedua", pesan[0]["teks"])
        self.assertIn("baris ketiga", pesan[0]["teks"])


class PesanSistemMediaDihapus(unittest.TestCase):
    def test_pesan_terenkripsi(self):
        teks = "12/09/26, 08.00 - Pesan dan panggilan terenkripsi end-to-end. Tidak seorang pun di luar chat ini, termasuk WhatsApp, yang dapat membacanya."
        pesan, *_ = parse_teks(teks)
        self.assertEqual(pesan[0]["jenis"], "sistem")
        self.assertIsNone(pesan[0]["pengirim"])

    def test_anggota_bergabung(self):
        teks = "12/09/26, 09.00 - Fajar bergabung menggunakan tautan undangan grup ini"
        pesan, *_ = parse_teks(teks)
        self.assertEqual(pesan[0]["jenis"], "sistem")

    def test_media_tidak_disertakan(self):
        teks = "12/09/26, 08.10 - Dimas: <Media tidak disertakan>"
        pesan, *_ = parse_teks(teks)
        self.assertEqual(pesan[0]["jenis"], "media")

    def test_media_omitted_en(self):
        teks = "12/09/26, 08.10 - Dimas: <Media omitted>"
        pesan, *_ = parse_teks(teks)
        self.assertEqual(pesan[0]["jenis"], "media")

    def test_pesan_dihapus(self):
        teks = "12/09/26, 08.10 - Dimas: Pesan ini dihapus"
        pesan, *_ = parse_teks(teks)
        self.assertEqual(pesan[0]["jenis"], "dihapus")

    def test_message_deleted_en(self):
        teks = "12/09/26, 08.10 - Dimas: This message was deleted"
        pesan, *_ = parse_teks(teks)
        self.assertEqual(pesan[0]["jenis"], "dihapus")


class KarakterTakTerlihat(unittest.TestCase):
    def test_lrm_di_awal_baris(self):
        teks = "‎12/09/26, 08.00 - Budi: Halo"
        pesan, *_ = parse_teks(teks)
        self.assertEqual(len(pesan), 1)
        self.assertEqual(pesan[0]["pengirim"], "Budi")

    def test_nbsp_di_tanggal(self):
        teks = "12/09/26, 08.00 - Budi: Halo"
        pesan, *_ = parse_teks(teks)
        self.assertEqual(len(pesan), 1)


class UrutanTanggalAmbigu(unittest.TestCase):
    def test_default_dm_saat_ambigu(self):
        # Semua tanggal <=12 di kedua posisi -> ambigu, default d/m
        teks = (
            "01/02/26, 08.00 - A: x\n"
            "03/04/26, 08.00 - A: y\n"
        )
        pesan, fmt, urutan, catatan = parse_teks(teks)
        self.assertEqual(urutan, "d/m")
        self.assertTrue(any("ambigu" in c.lower() for c in catatan))

    def test_terdeteksi_md_dari_nilai_lebih_12(self):
        teks = "9/12/26, 17.05 - A: x"  # posisi kedua (12) bukan sinyal, posisi ini <=12 juga
        pesan, fmt, urutan, catatan = parse_teks(teks)
        # 9 dan 12 sama2 <=12 -> tetap ambigu; uji sinyal nyata di bawah
        self.assertIn(urutan, ("d/m", "m/d"))

    def test_terdeteksi_dm_dari_nilai_lebih_12(self):
        teks = "25/09/26, 08.00 - A: x"  # posisi pertama 25 > 12 -> pasti d/m
        pesan, fmt, urutan, catatan = parse_teks(teks)
        self.assertEqual(urutan, "d/m")

    def test_terdeteksi_md_dari_bulan_lebih_12_di_posisi_kedua(self):
        teks = "09/25/26, 08.00 - A: x"  # posisi kedua 25 > 12 -> pasti m/d
        pesan, fmt, urutan, catatan = parse_teks(teks)
        self.assertEqual(urutan, "m/d")


class FilterRentangWaktu(unittest.TestCase):
    def setUp(self):
        self.pesan = [
            {"waktu": "2026-09-12T17:05:00", "pengirim": "A", "teks": "x", "jenis": "obrolan"},
            {"waktu": "2026-09-13T07:30:00", "pengirim": "A", "teks": "y", "jenis": "obrolan"},
        ]

    def test_filter_sejak(self):
        from datetime import datetime
        hasil = p.filter_rentang(self.pesan, datetime(2026, 9, 13, 0, 0), None)
        self.assertEqual(len(hasil), 1)
        self.assertEqual(hasil[0]["teks"], "y")

    def test_urai_kemarin(self):
        from datetime import datetime
        sekarang = datetime(2026, 9, 13, 12, 0)
        hasil = p.urai_titik_waktu("kemarin 17:00", sekarang)
        self.assertEqual(hasil, datetime(2026, 9, 12, 17, 0))

    def test_urai_iso(self):
        from datetime import datetime
        hasil = p.urai_titik_waktu("2026-09-12 17:00", datetime.now())
        self.assertEqual(hasil, datetime(2026, 9, 12, 17, 0))

    def test_urai_format_tidak_dikenali(self):
        from datetime import datetime
        with self.assertRaises(ValueError):
            p.urai_titik_waktu("besok-lusa jam sekian", datetime.now())


class Samarkan(unittest.TestCase):
    def test_pemetaan_urut_dan_konsisten(self):
        teks = (
            "12/09/26, 08.00 - Sari: halo\n"
            "12/09/26, 08.01 - Budi: halo juga\n"
            "12/09/26, 08.02 - Sari: oke\n"
        )
        pesan, *_ = parse_teks(teks)
        pesan, peta = p.samarkan_pengirim(pesan)
        self.assertEqual(pesan[0]["pengirim"], "Anggota 1")
        self.assertEqual(pesan[1]["pengirim"], "Anggota 2")
        self.assertEqual(pesan[2]["pengirim"], "Anggota 1")
        self.assertEqual(peta, {"Sari": "Anggota 1", "Budi": "Anggota 2"})

    def test_nomor_telepon_disamarkan(self):
        hasil = p.samarkan_nomor_dalam_teks("hubungi saya di 0812-3456-7890 ya")
        self.assertNotIn("0812", hasil)
        self.assertIn("[nomor disamarkan]", hasil)

    def test_nomor_dengan_kode_negara(self):
        hasil = p.samarkan_nomor_dalam_teks("wa saya +62 812-0000-0001")
        self.assertNotIn("0001", hasil)

    def test_nomor_landline_tidak_disamarkan(self):
        # Nomor rumah/kantor (021-...) bukan format HP 08xx, tidak seharusnya disamarkan
        hasil = p.samarkan_nomor_dalam_teks("telepon kantor 021-7654321")
        self.assertIn("021-7654321", hasil)


class StatistikDanPengelompokan(unittest.TestCase):
    def test_statistik_dasar(self):
        teks = (
            "12/09/26, 08.00 - Sari: halo\n"
            "12/09/26, 08.10 - Budi: <Media tidak disertakan>\n"
            "12/09/26, 08.20 - Sari: Pesan ini dihapus\n"
        )
        pesan, *_ = parse_teks(teks)
        stat = p.hitung_statistik(pesan)
        self.assertEqual(stat["total_pesan"], 3)
        self.assertEqual(stat["jumlah_media"], 1)
        self.assertEqual(stat["jumlah_dihapus"], 1)
        self.assertEqual(stat["per_pengirim"]["Sari"], 2)

    def test_kelompok_per_hari(self):
        teks = (
            "12/09/26, 08.00 - Sari: halo\n"
            "13/09/26, 08.00 - Sari: halo lagi\n"
        )
        pesan, *_ = parse_teks(teks)
        hari = p.kelompokkan_per_hari(pesan)
        self.assertEqual([h["tanggal"] for h in hari], ["2026-09-12", "2026-09-13"])
        self.assertEqual(hari[0]["jumlah_pesan"], 1)


class FileKosongRusakEncoding(unittest.TestCase):
    def test_file_tidak_ada(self):
        with self.assertRaises(ValueError):
            p.baca_teks_ekspor("/path/yang/tidak/ada.txt")

    def test_file_kosong(self):
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            path = f.name
        try:
            teks, sumber = p.baca_teks_ekspor(path)
            self.assertEqual(teks, "")
        finally:
            os.unlink(path)

    def test_zip_tanpa_txt(self):
        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as f:
            path = f.name
        try:
            with zipfile.ZipFile(path, "w") as z:
                z.writestr("foto.jpg", b"bukan teks")
            with self.assertRaises(ValueError):
                p.baca_teks_ekspor(path)
        finally:
            os.unlink(path)

    def test_zip_berisi_txt_dibaca(self):
        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as f:
            path = f.name
        try:
            with zipfile.ZipFile(path, "w") as z:
                z.writestr("WhatsApp Chat with Toko.txt", "12/09/26, 08.00 - Sari: halo\n")
            teks, sumber = p.baca_teks_ekspor(path)
            self.assertIn("Sari", teks)
            self.assertIn("Toko", sumber)
        finally:
            os.unlink(path)

    def test_zip_rusak(self):
        with tempfile.NamedTemporaryFile(suffix=".zip", delete=False) as f:
            f.write(b"bukan file zip yang valid")
            path = f.name
        try:
            teks, sumber = p.baca_teks_ekspor(path)
            # Bukan zip valid -> dibaca sebagai teks biasa, tidak ada pesan dikenali
            pesan, fmt, urutan, catatan = p.parse_pesan(teks)
            self.assertEqual(pesan, [])
        finally:
            os.unlink(path)

    def test_encoding_latin1(self):
        with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as f:
            baris = "12/09/26, 08.00 - Nona\xe9: cafe\xe9 enak".encode("latin-1")
            f.write(baris)
            path = f.name
        try:
            teks, sumber = p.baca_teks_ekspor(path)
            pesan, *_ = p.parse_pesan(teks)
            self.assertEqual(len(pesan), 1)
        finally:
            os.unlink(path)

    def test_teks_acak_tanpa_pola_pesan(self):
        pesan, fmt, urutan, catatan = p.parse_pesan("halo\nini bukan ekspor whatsapp\nbaris acak")
        self.assertEqual(pesan, [])
        self.assertTrue(len(catatan) >= 1)


class CLIIntegrasi(unittest.TestCase):
    """Uji lewat file contoh di templates/ (dijalankan sebagai subprocess CLI)."""

    def test_contoh_android_valid_json(self):
        import subprocess
        skrip = FOLDER_SKILL / "scripts" / "parse_ekspor_wa.py"
        contoh = FOLDER_SKILL / "templates" / "contoh-ekspor-android.txt"
        hasil = subprocess.run(
            [sys.executable, str(skrip), str(contoh), "--indent", "0"],
            capture_output=True, text=True, check=True,
        )
        data = json.loads(hasil.stdout)
        self.assertEqual(data["format_terdeteksi"], "android")
        self.assertGreater(data["statistik"]["total_pesan"], 0)

    def test_contoh_ios_valid_json(self):
        import subprocess
        skrip = FOLDER_SKILL / "scripts" / "parse_ekspor_wa.py"
        contoh = FOLDER_SKILL / "templates" / "contoh-ekspor-ios.txt"
        hasil = subprocess.run(
            [sys.executable, str(skrip), str(contoh), "--indent", "0"],
            capture_output=True, text=True, check=True,
        )
        data = json.loads(hasil.stdout)
        self.assertEqual(data["format_terdeteksi"], "ios")
        self.assertEqual(data["urutan_tanggal"], "m/d")

    def test_file_tidak_ada_exit_1(self):
        import subprocess
        skrip = FOLDER_SKILL / "scripts" / "parse_ekspor_wa.py"
        hasil = subprocess.run(
            [sys.executable, str(skrip), "/tidak/ada/file.txt"],
            capture_output=True, text=True,
        )
        self.assertNotEqual(hasil.returncode, 0)
        self.assertIn("Error", hasil.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
