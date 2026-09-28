#!/usr/bin/env python3
"""Uji regresi pengingat_pasien.py (unittest, library standar saja).

Jalankan dari folder skill:  python3 tests/uji_regresi.py      (Windows: python / py)
Semua data di sini FIKTIF. File dibuat di folder sementara lalu dihapus otomatis.
"""
import csv
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import date

DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(DIR, "..", "scripts")
SCRIPT = os.path.join(SCRIPTS, "pengingat_pasien.py")
sys.path.insert(0, SCRIPTS)
import pengingat_pasien as pp  # noqa: E402

ACUAN = date(2026, 9, 26)  # Sabtu


class TestTanggal(unittest.TestCase):
    def t(self, teks):
        return pp.parse_tanggal(teks, ACUAN)[0]

    def test_format_lengkap(self):
        for teks in ("2026-10-05", "05-10-2026", "5/10/2026", "5.10.2026", "5/10/26",
                     "5 Oktober 2026", "5 okt 2026", "tgl 5 Okt 2026"):
            self.assertEqual(self.t(teks), date(2026, 10, 5), teks)

    def test_relatif(self):
        self.assertEqual(self.t("hari ini"), ACUAN)
        self.assertEqual(self.t("besok"), date(2026, 9, 27))
        self.assertEqual(self.t("lusa"), date(2026, 9, 28))
        self.assertEqual(self.t("3 hari lagi"), date(2026, 9, 29))
        self.assertEqual(self.t("+10"), date(2026, 10, 6))
        self.assertEqual(self.t("2 minggu lagi"), date(2026, 10, 10))

    def test_bulan_lagi(self):
        self.assertEqual(self.t("1 bulan lagi"), date(2026, 10, 26))
        self.assertEqual(self.t("3 bulan lagi"), date(2026, 12, 26))
        # 31 Jan + 1 bulan -> Februari tidak punya 31, turun ke tanggal terakhir
        d, cat = pp.parse_tanggal("1 bulan lagi", date(2026, 1, 31))
        self.assertEqual(d, date(2026, 2, 28))
        self.assertIsNotNone(cat)

    def test_bulan_lagi_tahun_kabisat(self):
        # 29 Jan 2028 + 1 bulan -> 2028 kabisat, Februari PUNYA tanggal 29 -> tidak boleh turun ke 28.
        d, cat = pp.parse_tanggal("1 bulan lagi", date(2028, 1, 29))
        self.assertEqual(d, date(2028, 2, 29))
        self.assertIsNone(cat)  # tanggal asli tetap terpakai, tidak ada penyesuaian
        # Tahun BUKAN kabisat: tetap turun ke 28 seperti sebelumnya.
        d2, cat2 = pp.parse_tanggal("1 bulan lagi", date(2029, 1, 29))
        self.assertEqual(d2, date(2029, 2, 28))
        self.assertIsNotNone(cat2)
        # 30 Apr + 10 bulan -> Februari 2027 (bukan kabisat): turun ke 28.
        d3, _ = pp.parse_tanggal("10 bulan lagi", date(2026, 4, 30))
        self.assertEqual(d3, date(2027, 2, 28))

    def test_nama_hari(self):
        # ACUAN = Sabtu 26 Sep 2026
        self.assertEqual(self.t("Senin"), date(2026, 9, 28))
        self.assertEqual(self.t("Sabtu"), ACUAN)

    def test_tahun_kabur_ke_depan(self):
        d, cat = pp.parse_tanggal("5/10", ACUAN)
        self.assertEqual(d, date(2026, 10, 5))
        self.assertIn("Tahun tidak disebut", cat)

    def test_tanggal_rusak(self):
        for teks in ("31/2/2026", "32/10", "3/13", "kapan-kapan", "", "2026-02-30"):
            with self.assertRaises(pp.Gagal, msg=teks):
                pp.parse_tanggal(teks, ACUAN)


class TestWa(unittest.TestCase):
    def test_format_umum(self):
        for teks in ("0812-0000-1111", "+62 812 0000 1111", "62812-0000-1111", "0812 0000 1111"):
            wa, _ = pp.normalisasi_wa(teks)
            self.assertEqual(wa, "6281200001111", teks)

    def test_nomor_tidak_wajar(self):
        for teks in ("abc", "", "123", "081200001111222233334444"):
            with self.assertRaises(pp.Gagal, msg=teks):
                pp.normalisasi_wa(teks)

    def test_tampil(self):
        self.assertEqual(pp.tampil_wa("6281200001111"), "0812-0000-1111")


class TestValidasiIsi(unittest.TestCase):
    def test_diagnosis_ditolak(self):
        for kata in ("kontrol kanker", "riwayat diabetes", "cek HIV", "kontrol Covid"):
            with self.assertRaises(pp.Gagal, msg=kata):
                pp.rapikan_jenis(kata)

    def test_jenis_umum_lolos(self):
        for kata in ("kontrol", "vaksin", "cabut jahitan", "cek gigi", "vaksin hewan", "groom", "sunat"):
            self.assertTrue(pp.rapikan_jenis(kata))

    def test_nama_vaksin_lolos_berkonteks_vaksin(self):
        # Temuan TINGGI uji Akun B 2026-09-26: nama vaksin/imunisasi harus tetap boleh dicatat.
        for kata in ("imunisasi campak", "vaksin rabies", "vaksin MR", "imunisasi difteri (DPT)",
                     "vaksinasi tetanus", "booster covid", "suntik rabies", "vaksin hepatitis B",
                     "imunisasi polio"):
            self.assertTrue(pp.rapikan_jenis(kata), kata)

    def test_nama_vaksin_tetap_ditolak_bila_bernada_diagnosis(self):
        for kata in ("riwayat campak", "kena difteri", "positif rabies", "didiagnosis tbc",
                      "hasil lab campak", "menderita hepatitis", "sakit campak"):
            with self.assertRaises(pp.Gagal, msg=kata):
                pp.rapikan_jenis(kata)

    def test_diagnosis_umum_diluar_daftar_lama_ditolak(self):
        # Temuan SEDANG uji Akun B 2026-09-26: celah blocklist untuk penyakit umum sehari-hari.
        for kata in ("kontrol batu ginjal", "cek asma", "kontrol maag", "pasca usus buntu",
                     "kontrol vertigo", "kontrol katarak", "cek amandel", "kontrol wasir",
                     "cek anemia", "kontrol migrain", "kontrol hernia", "cek tiroid"):
            with self.assertRaises(pp.Gagal, msg=kata):
                pp.rapikan_jenis(kata)

    def test_data_pribadi_ditolak(self):
        with self.assertRaises(pp.DataPribadi):
            pp.cek_data_pribadi("nama", "0812-1111-2222")
        with self.assertRaises(pp.DataPribadi):
            pp.cek_data_pribadi("catatan", "email saya budi@contoh.com")
        with self.assertRaises(pp.DataPribadi):
            pp.cek_data_pribadi("catatan", "NIK 3271011234567890")

    def test_samar_nama(self):
        self.assertEqual(pp.samar_nama("Bu Sari"), "Bu S.")
        self.assertEqual(pp.samar_nama("Budi"), "B.")


class TestCLI(unittest.TestCase):
    """Uji end-to-end lewat subprocess, seperti dipakai agent."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="uji-pasien-")
        self.file = os.path.join(self.tmp, "DAFTAR.csv")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def jalan(self, *args, hari_ini="2026-09-26", cek=True):
        cmd = [sys.executable, SCRIPT, "--file", self.file, "--hari-ini", hari_ini, "--json"] + list(args)
        r = subprocess.run(cmd, capture_output=True, text=True)
        if cek and r.returncode != 0:
            self.fail(f"gagal ({r.returncode}): {' '.join(args)}\nstdout={r.stdout}\nstderr={r.stderr}")
        return r

    def baca(self, *args, **kw):
        r = self.jalan(*args, **kw)
        return json.loads(r.stdout), r

    def test_tambah_dan_daftar(self):
        d, _ = self.baca("tambah", "--nama", "Bu Sari", "--wa", "0812-0000-1111",
                          "--jenis", "kontrol", "--tanggal", "besok", "--persetujuan", "ya")
        self.assertTrue(d["ok"])
        self.assertEqual(d["id"], "1")
        d, _ = self.baca("daftar", "--kapan", "besok")
        self.assertEqual(d["kelompok"]["h1"], 1)
        self.assertIn("Bu Sari", d["teks"])
        self.assertIn("0812-0000-1111", d["teks"])

    def test_persetujuan_tidak_tidak_muncul_di_daftar(self):
        self.baca("tambah", "--nama", "Pak Tono", "--wa", "0812-1111-2222",
                  "--jenis", "kontrol", "--tanggal", "besok", "--persetujuan", "tidak")
        d, _ = self.baca("daftar", "--kapan", "besok")
        self.assertNotIn("Pak Tono", d["teks"])
        self.assertEqual(d["kelompok"]["h1"], 0)

    def test_draf_ditolak_tanpa_persetujuan(self):
        self.baca("tambah", "--nama", "Pak Tono", "--wa", "0812-1111-2222",
                  "--jenis", "kontrol", "--tanggal", "besok", "--persetujuan", "tidak")
        r = self.jalan("draf", "--id", "1", cek=False)
        self.assertEqual(r.returncode, 1)

    def test_jenis_diagnosis_ditolak_exit_1(self):
        # v1.0.2: nama uji & docstring script diperbaiki -- diagnosis pakai kode keluar 1
        # (error input biasa via Gagal), BUKAN kode 2 (khusus data pribadi pihak lain/DataPribadi).
        r = self.jalan("tambah", "--nama", "Rina", "--wa", "0812-3333-4444", "--jenis", "kontrol tumor",
                        "--tanggal", "besok", "--persetujuan", "ya", cek=False)
        self.assertEqual(r.returncode, 1)

    def test_jenis_imunisasi_campak_diterima(self):
        # Regresi temuan TINGGI uji Akun B: "imunisasi campak" harus bisa dicatat lewat CLI.
        d, _ = self.baca("tambah", "--nama", "Adik Rara", "--wa", "0812-3333-4444",
                          "--jenis", "imunisasi campak", "--tanggal", "besok", "--persetujuan", "ya")
        self.assertTrue(d["ok"])

    def test_jenis_vaksin_rabies_diterima(self):
        d, _ = self.baca("tambah", "--nama", "Kucing Mimi", "--wa", "0812-3333-4444",
                          "--jenis", "vaksin rabies", "--tanggal", "besok", "--persetujuan", "ya")
        self.assertTrue(d["ok"])

    def test_nomor_hp_di_nama_ditolak_exit_2(self):
        r = self.jalan("tambah", "--nama", "0812-9999-8888", "--wa", "0812-1111-2222", "--jenis", "kontrol",
                        "--tanggal", "besok", "--persetujuan", "ya", cek=False)
        self.assertEqual(r.returncode, 2)

    def test_ubah_status_datang_menjadwalkan_ulang(self):
        self.baca("tambah", "--nama", "Kucing Mimi", "--wa", "0812-5555-6666", "--jenis", "vaksin hewan",
                  "--tanggal", "hari ini", "--persetujuan", "ya")
        d, _ = self.baca("ubah-status", "--id", "1", "--status", "datang", "--berikutnya", "1 bulan lagi")
        self.assertTrue(d["ok"])
        with open(self.file, encoding="utf-8") as f:
            baris = list(csv.DictReader(f))
        self.assertEqual(baris[0]["status"], "dijadwalkan")
        self.assertEqual(baris[0]["tanggal"], "2026-10-26")
        self.assertNotIn(";", baris[0]["catatan"][:1])  # tidak ada '; ' menggantung di awal

    def test_ubah_status_batal(self):
        self.baca("tambah", "--nama", "Bu Rina", "--wa", "0812-7777-8888", "--jenis", "kontrol",
                  "--tanggal", "besok", "--persetujuan", "ya")
        self.baca("ubah-status", "--id", "1", "--status", "batal", "--alasan", "pindah kota")
        d, _ = self.baca("daftar", "--kapan", "semua")
        self.assertNotIn("Bu Rina", d["teks"])

    def test_hapus_perlu_konfirmasi(self):
        self.baca("tambah", "--nama", "Bu Rina", "--wa", "0812-7777-8888", "--jenis", "kontrol",
                  "--tanggal", "besok", "--persetujuan", "ya")
        d, _ = self.baca("hapus", "--id", "1")
        self.assertEqual(d["mode"], "pratinjau")
        with open(self.file, encoding="utf-8") as f:
            self.assertIn("Bu Rina", f.read())
        d, _ = self.baca("hapus", "--id", "1", "--ya")
        self.assertEqual(d["mode"], "tersimpan")
        with open(self.file, encoding="utf-8") as f:
            self.assertNotIn("Bu Rina", f.read())

    def test_hapus_by_wa(self):
        self.baca("tambah", "--nama", "Bu Rina", "--wa", "0812-7777-8888", "--jenis", "kontrol",
                  "--tanggal", "besok", "--persetujuan", "ya")
        self.baca("hapus", "--wa", "0812-7777-8888", "--ya")
        with open(self.file, encoding="utf-8") as f:
            self.assertNotIn("Bu Rina", f.read())

    def test_impor_tanpa_persetujuan_default_ditolak(self):
        src = os.path.join(self.tmp, "impor.csv")
        with open(src, "w", encoding="utf-8", newline="") as f:
            f.write("nama,wa,jenis,tanggal\nBu Wati,0812-1111-0001,kontrol,2026-09-27\n")
        r = self.jalan("impor", src, cek=False)
        self.assertEqual(r.returncode, 1)

    def test_impor_pratinjau_lalu_konfirmasi(self):
        src = os.path.join(self.tmp, "impor.csv")
        with open(src, "w", encoding="utf-8", newline="") as f:
            f.write("nama,wa,jenis,tanggal,persetujuan\n"
                    "Bu Wati,0812-1111-0001,kontrol,2026-09-27,ya\n"
                    "Pak Joko,0812-1111-0002,vaksin,2026-09-29,tidak\n")
        d, _ = self.baca("impor", src)
        self.assertEqual(d["mode"], "pratinjau")
        self.assertEqual(d["akan_ditambah"], 2)
        with open(self.file, encoding="utf-8") if os.path.exists(self.file) else io.StringIO() as f:
            pass  # file belum tertulis pada tahap pratinjau
        self.assertFalse(os.path.exists(self.file))
        d, _ = self.baca("impor", src, "--ya")
        self.assertEqual(d["ditambahkan"], 2)

    def test_csv_formula_injection_aman(self):
        self.baca("tambah", "--nama", "Bu Sari", "--wa", "0812-0000-1111", "--jenis", "kontrol",
                  "--tanggal", "besok", "--persetujuan", "ya", "--catatan", "=cmd|'/c calc'!A1")
        with open(self.file, encoding="utf-8") as f:
            isi = f.read()
        self.assertNotIn("\n=cmd", isi)  # tidak boleh diawali '=' mentah di baris manapun

    def test_baris_rusak_tidak_menghentikan_program(self):
        os.makedirs(os.path.dirname(self.file), exist_ok=True)
        with open(self.file, "w", encoding="utf-8", newline="") as f:
            f.write("id,nama_panggilan,wa,jenis,tanggal,status,persetujuan,dibuat,diingatkan_pada,catatan\n")
            f.write("1,Bu Wati,6281211110001,Kontrol,2026-09-27,dijadwalkan,ya,2026-09-26,,\n")
            f.write("99,A,B,C,D,E,F,G,H,I,J,K\n")  # kolom kelebihan
        d, _ = self.baca("info")
        self.assertIn("baris_ditolak", d)
        d2, _ = self.baca("tambah", "--nama", "Baru", "--wa", "0812-5555-6666", "--jenis", "kontrol",
                           "--tanggal", "besok", "--persetujuan", "ya")
        self.assertEqual(d2["id"], "2")  # id tidak bentrok dengan baris rusak ('99')
        with open(self.file, encoding="utf-8") as f:
            self.assertIn("99,A,B,C,D,E,F,G,H,I,J,K", f.read())  # baris rusak tetap dipertahankan

    def test_ringkasan_tanpa_nomor_wa(self):
        self.baca("tambah", "--nama", "Bu Sari", "--wa", "0812-0000-1111", "--jenis", "kontrol",
                  "--tanggal", "hari ini", "--persetujuan", "ya")
        d, _ = self.baca("ringkasan", "--samarkan")
        self.assertNotIn("0812-0000-1111", d["teks"])
        self.assertIn("S.", d["teks"])
        self.assertNotIn("Sari", d["teks"])

    def test_persetujuan_wajib(self):
        r = self.jalan("tambah", "--nama", "Bu Sari", "--wa", "0812-0000-1111", "--jenis", "kontrol",
                        "--tanggal", "besok", cek=False)
        self.assertNotEqual(r.returncode, 0)  # argparse menolak (--persetujuan wajib)


if __name__ == "__main__":
    unittest.main(verbosity=2)
