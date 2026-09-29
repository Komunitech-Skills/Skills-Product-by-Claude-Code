#!/usr/bin/env python3
"""Uji regresi absensi-lokal. Jalankan: python3 tests/uji_regresi.py  (Windows: py tests/uji_regresi.py)

Semua angka lembur diverifikasi dengan rumus manual di komentar:
  upah sejam = upah sebulan / 173                        (PP 35/2021 Pasal 32 ayat (2))
  hari kerja: jam ke-1 x1,5, jam berikutnya x2          (Pasal 31 ayat (1))
  libur, 6 hari kerja: jam 1-7 x2, jam 8 x3, jam 9-11 x4 (Pasal 31 ayat (2) huruf a)
  libur resmi di hari kerja terpendek (6 hari): jam 1-5 x2, jam 6 x3, jam 7-9 x4 (Pasal 31 ayat (2) huruf b)
  libur, 5 hari kerja: jam 1-8 x2, jam 9 x3, jam 10-12 x4 (Pasal 31 ayat (3))
  total rupiah = jam setara x upah sebulan / 173, dibulatkan SEKALI ke rupiah terdekat.
Kalender September 2026: 1 = Selasa, 5/12/19/26 = Sabtu, 6/13/20/27 = Minggu.
"""
import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from datetime import time
from decimal import Decimal

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AKAR, "scripts"))
import absensi as A  # noqa: E402

KINI = "2026-09-30 23:00"


class Dasar(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.db = os.path.join(self.dir, "absensi.db")
        self.ok("init", "--ya")

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def run_cli(self, *argv):
        argv = list(argv) + ["--db", self.db, "--json", "--sekarang", KINI]
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
            kode = A.main(argv)
        return kode, json.loads(buf.getvalue())

    def ok(self, *argv):
        kode, out = self.run_cli(*argv)
        self.assertEqual(kode, 0, out)
        self.assertTrue(out["ok"], out)
        return out

    def gagal(self, *argv):
        kode, out = self.run_cli(*argv)
        self.assertEqual(kode, 1, out)
        self.assertFalse(out["ok"])
        return out

    def file(self, nama, isi):
        p = os.path.join(self.dir, nama)
        with open(p, "w", encoding="utf-8") as f:
            f.write(isi)
        return p

    def karyawan(self, kode, nama, *opsi):
        return self.ok("karyawan", "tambah", "--kode", kode, "--nama", nama, *opsi, "--ya")

    def rekap(self, *opsi):
        out = self.ok("rekap", "--bulan", "2026-09", *opsi)
        return {k["kode"]: k for k in out["karyawan"]}, out

    def masalah(self, out, jenis):
        return [m for m in out["masalah"] if m["jenis"] == jenis]


# ---------------------------------------------------------------- fungsi dasar
class UjiParser(unittest.TestCase):
    def test_01_parse_jam(self):
        self.assertEqual(A.parse_jam("08.12"), time(8, 12))
        self.assertEqual(A.parse_jam("8:12:33"), time(8, 12, 33))
        self.assertEqual(A.parse_jam("8:12 PM"), time(20, 12))
        self.assertEqual(A.parse_jam("0.5"), time(12, 0))          # pecahan hari Excel
        for salah in ("25.10", "08.75", "24:00", "jam 8", "", "13:00 PM"):
            self.assertIsNone(A.parse_jam(salah), salah)

    def test_02_parse_tanggal(self):
        self.assertEqual(A.parse_tanggal("03/09/2026").isoformat(), "2026-09-03")         # hari/bulan
        self.assertEqual(A.parse_tanggal("09/03/2026", "mdy").isoformat(), "2026-09-03")  # bulan/hari
        self.assertEqual(A.parse_tanggal("3 Sep 2026").isoformat(), "2026-09-03")
        self.assertEqual(A.parse_tanggal("2026-09-03").isoformat(), "2026-09-03")
        self.assertIsNone(A.parse_tanggal("31/02/2026"))
        self.assertEqual(A.pisah_tanggal_jam("Kamis, 03/09/2026 08:12:33"), ("03/09/2026", "08:12:33"))

    def test_03_parse_angka_dan_durasi(self):
        self.assertEqual(A.parse_angka("Rp 5.000.000"), Decimal(5000000))
        self.assertEqual(A.parse_angka("5jt"), Decimal(5000000))
        self.assertEqual(A.parse_angka("750rb"), Decimal(750000))
        self.assertEqual(A.parse_angka("4,5 jt"), Decimal(4500000))
        self.assertIsNone(A.parse_angka("lima juta"))
        self.assertEqual(A.parse_durasi_jam("1,5"), Decimal("1.5"))
        self.assertEqual(A.parse_durasi_jam("1:30"), Decimal("1.5"))
        self.assertEqual(A.parse_durasi_jam("1 jam 30 menit"), Decimal("1.5"))
        self.assertIsNone(A.parse_durasi_jam("dua jam"))

    def test_04_pengali_hari_kerja(self):
        # Pasal 31 (1): 1 jam = 1x1,5 = 1,5 ; 2 jam = 1,5 + 1x2 = 3,5 ; 4 jam = 1,5 + 3x2 = 7,5 ; 0,5 jam = 0,75
        self.assertEqual(A.jam_setara_hari_kerja(Decimal(1)), Decimal("1.5"))
        self.assertEqual(A.jam_setara_hari_kerja(Decimal(2)), Decimal("3.5"))
        self.assertEqual(A.jam_setara_hari_kerja(Decimal(4)), Decimal("7.5"))
        self.assertEqual(A.jam_setara_hari_kerja(Decimal("0.5")), Decimal("0.75"))

    def test_05_pengali_libur_5_hari(self):
        # Pasal 31 (3): 8 jam = 8x2 = 16 ; 9 jam = 16 + 3 = 19 ; 12 jam = 16 + 3 + 3x4 = 31 ; 13 jam = di luar aturan
        self.assertEqual(A.jam_setara_libur(Decimal(8), "5")[0], Decimal(16))
        self.assertEqual(A.jam_setara_libur(Decimal(9), "5")[0], Decimal(19))
        self.assertEqual(A.jam_setara_libur(Decimal(12), "5")[0], Decimal(31))
        self.assertIsNone(A.jam_setara_libur(Decimal(13), "5")[0])

    def test_06_pengali_libur_6_hari_dan_hari_pendek(self):
        # Pasal 31 (2) a: 7 jam = 14 ; 8 jam = 14 + 3 = 17 ; 11 jam = 17 + 3x4 = 29 ; 12 jam = di luar aturan
        self.assertEqual(A.jam_setara_libur(Decimal(7), "6")[0], Decimal(14))
        self.assertEqual(A.jam_setara_libur(Decimal(8), "6")[0], Decimal(17))
        self.assertEqual(A.jam_setara_libur(Decimal(11), "6")[0], Decimal(29))
        self.assertIsNone(A.jam_setara_libur(Decimal(12), "6")[0])
        # Pasal 31 (2) b: 5 jam = 10 ; 6 jam = 10 + 3 = 13 ; 9 jam = 13 + 3x4 = 25 ; 10 jam = di luar aturan
        self.assertEqual(A.jam_setara_libur(Decimal(5), "6p")[0], Decimal(10))
        self.assertEqual(A.jam_setara_libur(Decimal(6), "6p")[0], Decimal(13))
        self.assertEqual(A.jam_setara_libur(Decimal(9), "6p")[0], Decimal(25))
        self.assertIsNone(A.jam_setara_libur(Decimal(10), "6p")[0])


# ---------------------------------------------------------------- lembur end-to-end
class UjiLembur(Dasar):
    def test_07_lembur_hari_kerja_rupiah(self):
        # Gaji 5.000.000 + tunj. tetap 500.000 = 5.500.000 ; upah sejam = 5.500.000/173 = 31.791,907
        # Selasa 1/9 lembur 2 jam = 1,5 + 2 = 3,5 jam setara -> 3,5 x 5.500.000 / 173 = 111.271,68 -> Rp 111.272
        self.karyawan("A01", "Andi", "--gaji-pokok", "5.000.000", "--tunjangan-tetap", "500rb")
        self.ok("catat", "--karyawan", "Andi", "--tanggal", "2026-09-01", "--masuk", "07.58", "--pulang", "19.05", "--ya")
        self.ok("lembur", "--karyawan", "A01", "--tanggal", "2026-09-01", "--jam", "2", "--catatan", "Bu Rina", "--ya")
        r, out = self.rekap()
        self.assertEqual(r["A01"]["upah_lembur"], 111272)
        self.assertEqual(r["A01"]["lembur_jam_setara"], "3.5")
        self.assertEqual(self.masalah(out, "lembur_lebih_dari_absen"), [])

    def test_08_lembur_libur_pola_5_hari(self):
        # Pola 5 hari, gaji 4.000.000. Minggu 6/9 lembur 10 jam: 8x2 + 1x3 + 1x4 = 23 jam setara
        # 23 x 4.000.000 / 173 = 531.791,91 -> Rp 531.792
        self.karyawan("B01", "Budi", "--gaji-pokok", "4000000")
        self.ok("catat", "--karyawan", "Budi", "--tanggal", "2026-09-06", "--masuk", "08.00", "--pulang", "19.00", "--ya")
        self.ok("lembur", "--karyawan", "Budi", "--tanggal", "2026-09-06", "--jam", "10", "--catatan", "x", "--ya")
        r, _ = self.rekap()
        self.assertEqual(r["B01"]["upah_lembur"], 531792)
        self.assertEqual(r["B01"]["hadir_di_hari_libur"], 1)

    def test_09_lembur_libur_pola_6_hari_minggu(self):
        # Pola 6 hari, gaji 3.460.000 -> upah sejam 3.460.000/173 = 20.000 tepat.
        # Minggu 6/9 (istirahat mingguan) 8 jam: 7x2 + 1x3 = 17 -> 17 x 20.000 = Rp 340.000
        self.karyawan("C01", "Citra", "--hari-kerja", "6", "--gaji-pokok", "3460000")
        self.ok("lembur", "--karyawan", "Citra", "--tanggal", "2026-09-06", "--jam", "8", "--catatan", "x", "--ya")
        r, out = self.rekap()
        self.assertEqual(r["C01"]["upah_lembur"], 340000)
        self.assertEqual(len(self.masalah(out, "lembur_tanpa_absen")), 1)   # tidak ada tap -> diperingatkan

    def test_10_libur_resmi_di_hari_kerja_terpendek(self):
        # Pola 6 hari, hari terpendek Sabtu. Sabtu 12/9 dicatat libur resmi. Lembur 6 jam:
        # Pasal 31 (2) b: 5x2 + 1x3 = 13 -> 13 x 20.000 = Rp 260.000
        # Rabu 16/9 libur resmi (bukan hari terpendek) 8 jam: tangga biasa 7x2 + 1x3 = 17 -> Rp 340.000
        # Total 260.000 + 340.000 = Rp 600.000 ; kolom slip-gaji: lembur_hari_libur '6p+8'
        self.karyawan("C01", "Citra", "--hari-kerja", "6", "--gaji-pokok", "3460000")
        self.ok("libur", "tambah", "--tanggal", "2026-09-12", "--nama", "Libur uji", "--ya")
        self.ok("libur", "tambah", "--tanggal", "2026-09-16", "--nama", "Libur uji 2", "--ya")
        self.ok("lembur", "--karyawan", "Citra", "--tanggal", "2026-09-12", "--jam", "6", "--catatan", "x", "--ya")
        self.ok("lembur", "--karyawan", "Citra", "--tanggal", "2026-09-16", "--jam", "8", "--catatan", "x", "--ya")
        gaji = os.path.join(self.dir, "gaji.csv")
        r, _ = self.rekap("--csv-gaji", gaji)
        self.assertEqual(r["C01"]["upah_lembur"], 600000)
        with open(gaji, encoding="utf-8-sig") as f:
            baris = f.read().splitlines()
        self.assertIn(";6p+8;", baris[1])

    def test_11_tanpa_persetujuan_tidak_ada_lembur(self):
        # Pulang 21.00 (4 jam setelah jadwal 17.00) tetapi TIDAK ada catatan lembur disetujui -> upah lembur 0
        self.karyawan("A01", "Andi", "--gaji-pokok", "5000000")
        self.ok("catat", "--karyawan", "Andi", "--tanggal", "2026-09-02", "--masuk", "08.00", "--pulang", "21.00", "--ya")
        r, _ = self.rekap()
        self.assertEqual(r["A01"]["upah_lembur"], 0)
        self.assertEqual(r["A01"]["lembur_jam_setara"], "0")
        self.assertEqual(r["A01"]["menit_kerja"], 12 * 60)     # 08.00-21.00 = 13 jam - istirahat 60 menit

    def test_12_dasar_75_persen_dan_upah_harian(self):
        # Pasal 32 (4): pokok 3.000.000 + tidak tetap 2.000.000 -> 3 jt < 75% x 5 jt (3,75 jt) -> dasar 3.750.000
        #   1 jam hari kerja = 1,5 x 3.750.000 / 173 = 32.514,45 -> Rp 32.514
        # Pasal 33 (1) a: upah harian 150.000 pola 6 hari -> 150.000 x 25 = 3.750.000
        #   2 jam hari kerja = 3,5 x 3.750.000 / 173 = 75.867,05 -> Rp 75.867
        self.karyawan("D01", "Dewi", "--gaji-pokok", "3000000", "--tunjangan-tidak-tetap", "2000000")
        self.karyawan("E01", "Eko", "--hari-kerja", "6", "--upah-harian", "150000")
        self.ok("lembur", "--karyawan", "D01", "--tanggal", "2026-09-01", "--jam", "1", "--catatan", "x", "--ya")
        self.ok("lembur", "--karyawan", "E01", "--tanggal", "2026-09-01", "--jam", "2", "--catatan", "x", "--ya")
        r, _ = self.rekap()
        self.assertEqual(r["D01"]["dasar_upah_lembur"], 3750000)
        self.assertEqual(r["D01"]["upah_lembur"], 32514)
        self.assertEqual(r["E01"]["dasar_upah_lembur"], 3750000)
        self.assertEqual(r["E01"]["upah_lembur"], 75867)

    def test_13_golongan_jabatan_tertentu(self):
        self.karyawan("M01", "Maya", "--gaji-pokok", "12000000", "--tanpa-lembur", "ya")
        self.ok("lembur", "--karyawan", "Maya", "--tanggal", "2026-09-01", "--jam", "3", "--catatan", "x", "--ya")
        r, out = self.rekap()
        self.assertEqual(r["M01"]["upah_lembur"], 0)
        self.assertEqual(len(self.masalah(out, "golongan_jabatan_tertentu")), 1)

    def test_14_batas_4_jam_dan_18_jam_seminggu(self):
        # Senin-Jumat 7-11/9 masing-masing 4 jam = 20 jam > 18 jam/minggu ; Senin 14/9 5 jam > 4 jam/hari
        # Tetap dihitung: 5 hari x 7,5 + (1,5 + 4x2 = 9,5) = 47 jam setara x 3.460.000/173 = 47 x 20.000 = Rp 940.000
        self.karyawan("A01", "Andi", "--gaji-pokok", "3460000")
        for tgl in ("07", "08", "09", "10", "11"):
            self.ok("lembur", "--karyawan", "A01", "--tanggal", "2026-09-" + tgl, "--jam", "4", "--catatan", "x", "--ya")
        self.ok("lembur", "--karyawan", "A01", "--tanggal", "2026-09-14", "--jam", "5", "--catatan", "x", "--ya")
        r, out = self.rekap()
        self.assertEqual(len(self.masalah(out, "lembur_lebih_18_jam_seminggu")), 1)
        self.assertEqual(len(self.masalah(out, "lembur_lebih_4_jam")), 1)
        self.assertEqual(r["A01"]["upah_lembur"], 940000)

    def test_15_lembur_libur_melebihi_aturan_ditolak(self):
        # pola 6 hari: lembur hari istirahat maks 11 jam (Pasal 31 (2) a) -> 11,5 jam ditolak
        self.karyawan("A01", "Andi", "--hari-kerja", "6", "--gaji-pokok", "5000000")
        out = self.gagal("lembur", "--karyawan", "A01", "--tanggal", "2026-09-06", "--jam", "11,5")
        self.assertIn("melebihi 11 jam", out["error"])
        self.assertIn("tidak wajar", self.gagal("lembur", "--karyawan", "A01", "--tanggal", "2026-09-01",
                                                "--jam", "13")["error"])
        f = self.file("lembur.csv", "tanggal;kode;jam;disetujui_oleh\n2026-09-01;A01;2;Bu Rina\n2026-09-06;A01;11,5;x\n")
        out = self.gagal("lembur", "--file", f, "--ya")
        self.assertEqual(len(out["baris_rusak"]), 1)
        r, _ = self.rekap()
        self.assertEqual(r["A01"]["lembur_rincian"], [])     # satu baris rusak -> tidak ada yang disimpan

    def test_16_lembur_saat_sakit_tidak_dihitung(self):
        self.karyawan("A01", "Andi", "--gaji-pokok", "5000000")
        self.ok("keterangan", "--karyawan", "A01", "--jenis", "sakit", "--tanggal", "2026-09-03", "--ya")
        self.ok("lembur", "--karyawan", "A01", "--tanggal", "2026-09-03", "--jam", "2", "--catatan", "x", "--ya")
        r, out = self.rekap()
        self.assertEqual(r["A01"]["upah_lembur"], 0)
        self.assertEqual(r["A01"]["sakit"], 1)
        self.assertEqual(len(self.masalah(out, "lembur_saat_tidak_hadir")), 1)


# ---------------------------------------------------------------- absensi & data rusak
class UjiAbsensi(Dasar):
    def test_17_shift_malam_impor_dan_manual(self):
        # Shift 22.00-06.00. Tap 1/9 21.58 & 2/9 06.03 -> satu hari kerja 1/9: 8 jam 5 menit - 60 = 425 menit
        self.ok("shift", "tambah", "--kode", "MALAM", "--masuk", "22.00", "--pulang", "06.00", "--ya")
        self.karyawan("J01", "Joko", "--shift", "MALAM", "--id-mesin", "7")
        f = self.file("log.csv", "AC-No.,Nama,Waktu,Status\n7,Joko,01/09/2026 21:58:00,C/In\n"
                                 "7,Joko,02/09/2026 06:03:00,C/Out\n")
        self.ok("impor-absen", f, "--ya")
        # manual: masuk 2/9 22.05, lalu pulang dicatat "besok pagi" tanpa --tanggal -> otomatis tanggal kerja 2/9
        self.ok("catat", "--karyawan", "Joko", "--tanggal", "2026-09-02", "--masuk", "22.05", "--ya")
        self.ok("catat", "--karyawan", "Joko", "--tanggal", "2026-09-02", "--pulang", "06.00", "--ya")
        _, rk = self.rekap("--csv-harian", os.path.join(self.dir, "h.csv"))
        with open(os.path.join(self.dir, "h.csv"), encoding="utf-8-sig") as fh:
            baris = [b.split(";") for b in fh.read().splitlines()[1:]]
        hari = {b[2]: b for b in baris}
        self.assertEqual(hari["01/09/2026"][12], "7:05")
        self.assertEqual(hari["02/09/2026"][9], "06.00 (+1)")
        self.assertEqual(hari["02/09/2026"][10], "5")                  # terlambat 5 menit
        self.assertEqual(self.masalah(rk, "tap_di_luar_shift"), [])

    def test_18_pulang_malam_dicatat_pagi_berikutnya(self):
        # Shift malam, 'pulang 06.05' tanpa --tanggal pada pagi 30/9 -> tanggal kerja 29/9
        self.ok("shift", "tambah", "--kode", "MALAM", "--masuk", "22.00", "--pulang", "06.00", "--ya")
        self.karyawan("J01", "Joko", "--shift", "MALAM")
        self.ok("catat", "--karyawan", "J01", "--tanggal", "2026-09-29", "--masuk", "21.55", "--ya")
        kode, out = self.run_cli("catat", "--karyawan", "J01", "--pulang", "06.05", "--ya")
        self.assertEqual(kode, 0, out)
        self.assertEqual(out["tanggal_kerja"], "2026-09-29")

    def test_19_pulang_sebelum_masuk(self):
        self.karyawan("A01", "Andi", "--id-mesin", "1")
        self.ok("catat", "--karyawan", "Andi", "--tanggal", "2026-09-01", "--masuk", "08.00", "--ya")
        out = self.gagal("catat", "--karyawan", "Andi", "--tanggal", "2026-09-01", "--pulang", "07.30", "--ya")
        self.assertIn("lebih awal dari jam masuk", out["error"])
        # dari mesin: C/Out 07.50 dan C/In 17.00 di hari yang sama -> dilaporkan, jam kerja tidak dihitung
        f = self.file("log.csv", "ID;Nama;Tanggal;Jam;Status\n1;Andi;02/09/2026;07:50;C/Out\n1;Andi;02/09/2026;17:00;C/In\n")
        self.ok("impor-absen", f, "--ya")
        r, out = self.rekap()
        self.assertEqual(len(self.masalah(out, "pulang_sebelum_masuk")), 1)
        self.assertEqual(r["A01"]["hari_tidak_lengkap"], 2)   # 1/9 hanya masuk, 2/9 data terbalik

    def test_20_tap_ganda_dan_impor_ulang(self):
        self.karyawan("A01", "Andi", "--id-mesin", "1")
        isi = ("No.,AC-No.,Nama,Waktu\n1,1,Andi,01/09/2026 07:55:12\n2,1,Andi,01/09/2026 07:57:40\n"
               "3,1,Andi,01/09/2026 17:03:00\n")
        f = self.file("log.csv", isi)
        out = self.ok("impor-absen", f, "--ya")
        self.assertEqual(out["tap_baru"], 3)
        out = self.ok("impor-absen", f, "--ya")
        self.assertEqual((out["tap_baru"], out["sudah_ada"]), (0, 3))
        r, rk = self.rekap()
        self.assertEqual(len(self.masalah(rk, "tap_ganda")), 1)
        # tap ganda 07.57 diabaikan; 07.55.12-17.03.00 = 9 jam 7 menit 48 detik -> 547 menit (detik dibuang) - 60
        self.assertEqual(r["A01"]["menit_kerja"], 487)

    def test_21_jam_tidak_valid_dan_karyawan_tak_dikenal(self):
        self.karyawan("A01", "Andi", "--id-mesin", "1")
        f = self.file("log.csv", "ID,Nama,Tanggal,Jam\n1,Andi,01/09/2026,25:61\n1,Andi,01/09/2026,08:00\n"
                                 "99,Tamu,01/09/2026,08:00\n1,Andi,32/09/2026,08:00\n")
        out = self.ok("impor-absen", f)          # pratinjau
        self.assertEqual(out["mode"], "pratinjau")
        self.assertEqual(out["tap_baru"], 1)
        self.assertEqual(len(out["baris_rusak"]), 2)
        self.assertEqual(sum(out["tak_dikenal"].values()), 1)
        r, _ = self.rekap()
        self.assertEqual(r["A01"]["hadir"], 0)    # pratinjau tidak menyimpan apa pun

    def test_22_deteksi_urutan_tanggal(self):
        self.karyawan("A01", "Andi", "--id-mesin", "1")
        f = self.file("us.csv", "User ID,Date,Time\n1,09/13/2026,08:00\n1,09/01/2026,08:00\n")
        out = self.ok("impor-absen", f)
        self.assertEqual(out["urutan_tanggal"], "mdy")
        self.assertTrue(any("BULAN/HARI" in p for p in out["peringatan"]))
        f = self.file("campur.csv", "User ID,Date,Time\n1,13/09/2026,08:00\n1,09/13/2026,08:00\n")
        self.assertIn("tidak konsisten", self.gagal("impor-absen", f)["error"])

    def test_23_toleransi_terlambat(self):
        self.karyawan("A01", "Andi")
        self.ok("atur", "--toleransi", "10", "--ya")
        self.ok("catat", "--karyawan", "A01", "--tanggal", "2026-09-01", "--masuk", "08.10", "--pulang", "17.00", "--ya")
        self.ok("catat", "--karyawan", "A01", "--tanggal", "2026-09-02", "--masuk", "08.11", "--pulang", "16.45", "--ya")
        r, _ = self.rekap()
        self.assertEqual((r["A01"]["terlambat_kali"], r["A01"]["terlambat_menit"]), (1, 11))
        self.assertEqual((r["A01"]["pulang_cepat_kali"], r["A01"]["pulang_cepat_menit"]), (1, 15))

    def test_24_format_harian_scan_masuk_diutamakan(self):
        # Kolom 'Jam Masuk' = jadwal, 'Scan Masuk' = jam asli -> yang dipakai Scan Masuk
        self.karyawan("A01", "Andi", "--id-mesin", "1")
        f = self.file("harian.csv", "No. ID;Nama;Tanggal;Jam Masuk;Jam Pulang;Scan Masuk;Scan Pulang\n"
                                    "1;Andi;03-09-2026;08.00;17.00;08.20;17.30\n")
        out = self.ok("impor-absen", f, "--ya")
        self.assertEqual(out["pemetaan"]["masuk"], "Scan Masuk")
        r, _ = self.rekap()
        self.assertEqual(r["A01"]["terlambat_menit"], 20)

    def test_25_keterangan_rentang_dan_tanpa_keterangan(self):
        # Cuti Kamis 3/9 s.d. Senin 7/9: Sabtu-Minggu dilewati -> 3 hari (3, 4, 7)
        self.karyawan("A01", "Andi")
        out = self.ok("keterangan", "--karyawan", "Andi", "--jenis", "cuti", "--tanggal", "2026-09-03",
                      "--sampai", "2026-09-07", "--ya")
        self.assertEqual(out["tanggal"], ["2026-09-03", "2026-09-04", "2026-09-07"])
        r, _ = self.rekap()
        self.assertEqual(r["A01"]["cuti"], 3)
        self.assertEqual(r["A01"]["hari_terjadwal"], 22)           # hari kerja Senin-Jumat September 2026
        self.assertEqual(r["A01"]["tanpa_keterangan"], 19)

    def test_26_validasi_input_karyawan(self):
        self.gagal("karyawan", "tambah", "--kode", "X1", "--nama", "Xena", "--id-mesin", "3201234567890001", "--ya")
        self.gagal("karyawan", "tambah", "--kode", "X1", "--nama", "Xena", "--shift", "TIDAKADA", "--ya")
        self.gagal("karyawan", "tambah", "--kode", "X1", "--nama", "Xena", "--gaji-pokok", "lima juta", "--ya")
        self.karyawan("A01", "Andi")
        self.karyawan("A02", "Andika")
        self.assertIn("lebih dari satu", self.gagal("catat", "--karyawan", "and", "--masuk", "08.00", "--ya")["error"])
        self.assertIn("tidak dikenal", self.gagal("catat", "--karyawan", "Zaki", "--masuk", "08.00", "--ya")["error"])
        self.assertIn("tidak valid", self.gagal("catat", "--karyawan", "A01", "--masuk", "8.75", "--ya")["error"])

    def test_27_gabung_ke_file_slip_gaji(self):
        self.karyawan("A01", "Andi", "--gaji-pokok", "5000000")
        self.karyawan("S01", "Sari", "--gaji-pokok", "4000000")
        self.ok("lembur", "--karyawan", "A01", "--tanggal", "2026-09-01", "--jam", "1,5", "--catatan", "x", "--ya")
        self.ok("lembur", "--karyawan", "A01", "--tanggal", "2026-09-02", "--jam", "2", "--catatan", "x", "--ya")
        self.ok("lembur", "--karyawan", "S01", "--tanggal", "2026-09-02", "--jam", "1", "--catatan", "x", "--ya")
        gaji = self.file("gaji.csv", "nama;ptkp;gaji_pokok;lembur_rp\nAndi;K/1;5.000.000;\nSari;TK/0;4.000.000;50.000\n")
        keluar = os.path.join(self.dir, "gabung.csv")
        _, out = self.rekap("--csv-gaji", keluar, "--gabung", gaji)
        with open(keluar, encoding="utf-8-sig") as f:
            baris = f.read().splitlines()
        self.assertEqual(baris[1], "Andi;K/1;5.000.000;;1,5+2;")
        self.assertEqual(baris[2], "Sari;TK/0;4.000.000;50.000;;")   # sudah ada nominal -> jam tidak diisi
        self.assertTrue(any("agar tidak dobel" in c for c in out["catatan_ekspor_gaji"]))

    def test_28_harian_dan_tap_tidak_lengkap(self):
        self.karyawan("A01", "Andi")
        self.karyawan("B01", "Budi")
        self.ok("catat", "--karyawan", "A01", "--tanggal", "2026-09-01", "--masuk", "08.30", "--ya")
        out = self.ok("harian", "--tanggal", "2026-09-01")
        self.assertEqual(out["hadir"], ["Andi"])
        self.assertEqual(out["belum_absen"], ["Budi"])
        self.assertEqual(len(out["terlambat"]), 1)
        self.assertEqual(len([m for m in out["masalah"] if m["jenis"] == "tap_tidak_lengkap"]), 1)

    def test_29_tanggal_mulai_dan_bulan_lalu(self):
        # Karyawan didaftarkan 30/9 (mulai default 1/9): rekap Agustus tidak boleh berisi 21 hari "tanpa keterangan".
        self.karyawan("A01", "Andi")
        self.assertIn("Belum ada", self.gagal("rekap", "--bulan", "2026-08")["error"])
        # Data mesin lama (Agustus) yang diimpor tetap direkap mulai tanggal data pertama (Senin 24/8).
        self.ok("catat", "--karyawan", "A01", "--tanggal", "2026-08-24", "--masuk", "08.00", "--pulang", "17.00", "--ya")
        out = self.ok("rekap", "--bulan", "2026-08")
        r = out["karyawan"][0]
        self.assertEqual((r["hari_terjadwal"], r["hadir"], r["tanpa_keterangan"]), (6, 1, 5))   # 24-28 & 31 Agustus
        # --bulan lalu dengan --sekarang 30/9 = Agustus 2026
        self.assertEqual(self.ok("rekap", "--bulan", "lalu")["periode"]["dari"], "2026-08-01")


# ---------------------------------------------------------------- perbaikan v1.0.1 (temuan uji independen)
class UjiPerbaikan101(Dasar):
    def teks(self, *argv):
        """Jalankan tanpa --json, kembalikan (kode, stdout, stderr)."""
        argv = list(argv) + ["--db", self.db, "--sekarang", KINI]
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            kode = A.main(argv)
        return kode, out.getvalue(), err.getvalue()

    def test_30_csv_tidak_bisa_ditulis_dan_init_gagal(self):
        self.karyawan("A01", "Andi")
        out = self.gagal("rekap", "--bulan", "2026-09", "--csv", self.dir)          # tujuan = folder
        self.assertIn("tidak bisa ditulis", out["error"])
        self.assertIn("Excel", out["error"])
        berkas = self.file("bukan-folder.txt", "x")
        kode, out = self.run_cli("rekap", "--bulan", "2026-09", "--csv-harian", os.path.join(berkas, "r.csv"))
        self.assertEqual(kode, 1)
        argv = ["init", "--ya", "--json", "--db", os.path.join(berkas, "sub", "a.db")]
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.assertEqual(A.main(argv), 1)
        self.assertIn("tidak bisa dibuat", json.loads(buf.getvalue())["error"])

    def test_31_database_terkunci_bukan_rusak(self):
        import sqlite3
        self.karyawan("A01", "Andi")
        kunci = sqlite3.connect(self.db, isolation_level=None)
        kunci.execute("BEGIN EXCLUSIVE")
        lama, A.TIMEOUT_DB = A.TIMEOUT_DB, 0.2
        try:
            for argv in (("rekap", "--bulan", "2026-09"),
                         ("catat", "--karyawan", "A01", "--tanggal", "2026-09-01", "--masuk", "08.00", "--ya")):
                out = self.gagal(*argv)
                self.assertIn("sedang dipakai program lain", out["error"])
                self.assertNotIn("bukan database", out["error"])
                self.assertIn("Jangan hapus", out["error"])
        finally:
            A.TIMEOUT_DB = lama
            kunci.execute("ROLLBACK")
            kunci.close()

    def test_32_batas_18_jam_minggu_lintas_bulan(self):
        # Minggu ISO 31/8 (Senin) - 6/9: 31/8 4 jam + 1-4/9 4 jam = 20 jam > 18 (Pasal 26 ayat (1))
        self.karyawan("A01", "Andi", "--gaji-pokok", "3460000", "--mulai", "2026-08-01")
        for tgl in ("2026-08-31", "2026-09-01", "2026-09-02", "2026-09-03"):
            self.ok("lembur", "--karyawan", "A01", "--tanggal", tgl, "--jam", "4", "--catatan", "x", "--ya")
        pratinjau = self.ok("lembur", "--karyawan", "A01", "--tanggal", "2026-09-04", "--jam", "4", "--catatan", "x")
        self.assertTrue(any("18 jam/minggu" in c for c in pratinjau["catatan"]))
        self.ok("lembur", "--karyawan", "A01", "--tanggal", "2026-09-04", "--jam", "4", "--catatan", "x", "--ya")
        for bulan in ("2026-08", "2026-09"):
            _, out = self.rekap() if bulan == "2026-09" else (None, self.ok("rekap", "--bulan", bulan))
            m = self.masalah(out, "lembur_lebih_18_jam_seminggu")
            self.assertEqual(len(m), 1, bulan)
            self.assertIn("20 jam", m[0]["pesan"])
        # upah tetap hanya dari lembur dalam periode: September 4 hari x 7,5 x 20.000 = Rp 600.000
        r, _ = self.rekap()
        self.assertEqual(r["A01"]["upah_lembur"], 600000)

    def test_33_rekap_tanpa_data_tidak_mendaftar_alpa(self):
        self.karyawan("A01", "Andi")
        kode, teks, _ = self.teks("rekap", "--bulan", "2026-09")
        self.assertEqual(kode, 0)
        self.assertIn("Belum ada data absen", teks)
        self.assertNotIn("mohon dikonfirmasi", teks)
        self.assertFalse(self.ok("rekap", "--bulan", "2026-09")["ada_data_absen"])

    def test_34_pengingat_pasal_29_dan_dasar_75_persen(self):
        # Dasar 75%: 3.000.000 + tidak tetap 2.000.000 -> 3.750.000 tampil di teks
        self.karyawan("D01", "Dewi", "--gaji-pokok", "3000000", "--tunjangan-tidak-tetap", "2000000")
        self.ok("lembur", "--karyawan", "D01", "--tanggal", "2026-09-01", "--jam", "4", "--catatan", "x", "--ya")
        self.ok("lembur", "--karyawan", "D01", "--tanggal", "2026-09-02", "--jam", "3", "--catatan", "x", "--ya")
        _, teks, _ = self.teks("rekap", "--bulan", "2026-09")
        self.assertIn("Dasar upah lembur Rp 3.750.000", teks)
        self.assertIn("Pasal 32 ayat (4)", teks)
        self.assertEqual(teks.count("1.400 kkal"), 1)            # hanya lembur 4 jam, bukan 3 jam
        out = self.ok("lembur", "--karyawan", "D01", "--tanggal", "2026-09-03", "--jam", "4", "--catatan", "x")
        self.assertTrue(any("Pasal 29" in c for c in out["catatan"]))

    def test_35_csv_gaji_terisi_dari_database(self):
        # Upah harian 150.000 pola 6 -> gaji_pokok 150.000 x 25 = 3.750.000 (Pasal 33 ayat (1) huruf a)
        self.karyawan("E01", "Eko", "--hari-kerja", "6", "--upah-harian", "150000")
        self.karyawan("A01", "Andi", "--gaji-pokok", "5000000", "--tunjangan-tetap", "500000")
        keluar = os.path.join(self.dir, "gaji.csv")
        _, out = self.rekap("--csv-gaji", keluar)
        with open(keluar, encoding="utf-8-sig") as f:
            baris = {b.split(";")[0]: b.split(";") for b in f.read().splitlines()[1:]}
        self.assertEqual(baris["Eko"][3], "3750000")
        self.assertEqual(baris["Andi"][3:5], ["5000000", "500000"])
        self.assertTrue(any("upah harian" in c and "Pasal 33" in c for c in out["catatan_ekspor_gaji"]))

    def test_36_pulang_lewat_jadwal_tanpa_lembur_hanya_info(self):
        self.karyawan("J01", "Joko", "--gaji-pokok", "4000000")
        self.ok("catat", "--karyawan", "J01", "--tanggal", "2026-08-25", "--masuk", "08.00", "--pulang", "19.10", "--ya")
        self.ok("catat", "--karyawan", "J01", "--tanggal", "2026-09-06", "--masuk", "08.00", "--pulang", "12.00", "--ya")
        _, teks, _ = self.teks("rekap", "--bulan", "2026-08")
        self.assertIn("2 jam 10 menit setelah jadwal", teks)
        self.assertIn("TIDAK dihitung lembur", teks)
        r, out = self.rekap()
        self.assertEqual(r["J01"]["upah_lembur"], 0)
        self.assertEqual(len(self.masalah(out, "masuk_libur_tanpa_lembur")), 1)

    def test_37_utf16_tanpa_bom_dan_file_hanya_judul(self):
        self.karyawan("A01", "Andi", "--id-mesin", "1")
        p = os.path.join(self.dir, "u16.csv")
        with open(p, "wb") as f:
            f.write("User ID\tDate\tTime\n1\t2026-09-01\t08:00\n1\t2026-09-01\t17:00\n".encode("utf-16-le"))
        self.assertEqual(self.ok("impor-absen", p)["tap_baru"], 2)
        kosong = self.file("judul.csv", "User ID,Date,Time\n")
        self.assertIn("tidak ada baris data", self.gagal("impor-absen", kosong)["error"])

    def test_38_catatan_tap_mesin_hanya_jadwal_hari_itu(self):
        self.karyawan("A01", "Andi", "--id-mesin", "1")
        f = self.file("log.csv", "ID,Tanggal,Jam\n1,01/09/2026,08:00\n1,02/09/2026,08:00\n1,02/09/2026,17:00\n")
        self.ok("impor-absen", f, "--ya")
        out = self.ok("catat", "--karyawan", "A01", "--tanggal", "2026-09-01", "--pulang", "17.00")
        self.assertTrue(any(c.startswith("Sudah ada 1 tap dari mesin") for c in out["catatan"]), out["catatan"])



class UjiSingkatanFlag(unittest.TestCase):
    """Regresi keamanan: argparse tidak boleh menerima singkatan flag konfirmasi (mis. --y untuk --ya)."""

    def test_singkatan_flag_konfirmasi_ditolak(self):
        import subprocess
        import tempfile
        skrip = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts", "absensi.py")
        with tempfile.TemporaryDirectory() as t:
            argv = ["init", "--db", os.path.join(t, "a.db"), "--y"]
            p = subprocess.run([sys.executable, skrip] + argv, capture_output=True, text=True, timeout=60)
            self.assertNotEqual(p.returncode, 0, p.stdout + p.stderr)
            self.assertIn("unrecognized arguments", p.stdout + p.stderr)
            self.assertFalse(os.path.exists(os.path.join(t, "a.db")), "singkatan flag tidak boleh menulis apa pun")


if __name__ == "__main__":
    unittest.main(verbosity=2)
