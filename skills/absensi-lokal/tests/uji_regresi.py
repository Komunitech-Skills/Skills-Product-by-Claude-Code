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
        self.assertTrue(any(c.startswith("Sudah ada 1 catatan scan dari mesin") for c in out["catatan"]), out["catatan"])



class UjiRekapCepat(unittest.TestCase):
    """rekap-cepat: file mesin + permintaan rekap -> hasil langsung di balasan pertama, tanpa menyimpan apa pun,
    tanpa menyebut lokasi file/nama database/nama skrip. Data fiktif September 2026 (22 hari kerja Senin-Jumat).
    Angka diverifikasi manual (bukan dari keluaran skrip):
      Andi telat (toleransi 10 menit; batas 08.10): 02/09 08.23 (23), 15/09 08.12 (12), 22/09 08.31 (31) = 3x, 66 menit
      Joko telat: 03/09 08.14 (14), 10/09 08.16 (16), 24/09 08.45 (45) = 3x, 75 menit; 17/09 08.08 tidak dihitung
      Sari tidak pernah telat. 14/09 kosong untuk semua; Sari kosong 21-22/09; Andi 25/09 tanpa jam pulang.
      Hari biasa masuk 07.55 pulang 17.05 = 9 jam 10 menit - istirahat 60 = 490 menit; Sari 19 hari x 490 = 9.310.
    """
    TELAT = {("Andi", "02/09"): "08:23", ("Andi", "15/09"): "08:12", ("Andi", "22/09"): "08:31",
             ("Joko", "03/09"): "08:14", ("Joko", "10/09"): "08:16", ("Joko", "17/09"): "08:08",
             ("Joko", "24/09"): "08:45"}
    ORANG = [("1", "Andi"), ("2", "Sari"), ("3", "Joko")]

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.csv = self.buat_csv("absen-sept.csv", 1, 30)

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def buat_csv(self, nama, hari_awal, hari_akhir, sabtu=False):
        import datetime as dt
        baris = ["No.,AC-No.,Nama,Waktu,Status"]
        n = 0
        for tgl in range(hari_awal, hari_akhir + 1):
            d = dt.date(2026, 9, tgl)
            if d.weekday() >= (6 if sabtu else 5) or tgl == 14:
                continue
            kunci = d.strftime("%d/%m")
            for idm, nm in self.ORANG:
                if nm == "Sari" and tgl in (21, 22):
                    continue
                n += 1
                baris.append("%d,%s,%s,%s %s:00,C/In" % (n, idm, nm, d.strftime("%d/%m/%Y"),
                                                        self.TELAT.get((nm, kunci), "07:55")))
                if not (nm == "Andi" and tgl == 25):
                    n += 1
                    baris.append("%d,%s,%s,%s 17:05:00,C/Out" % (n, idm, nm, d.strftime("%d/%m/%Y")))
        p = os.path.join(self.dir, nama)
        with open(p, "w", encoding="utf-8") as f:
            f.write("\n".join(baris) + "\n")
        return p

    def jalan(self, *argv, kode_harapan=0):
        buf = io.StringIO()
        db = os.path.join(self.dir, "tidak-boleh-dibuat", "absensi.db")
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
            kode = A.main(["rekap-cepat"] + list(argv) + ["--db", db, "--json", "--sekarang", "2026-10-01 09:00"])
        self.assertEqual(kode, kode_harapan, buf.getvalue())
        self.assertFalse(os.path.exists(os.path.dirname(db)), "rekap-cepat tidak boleh membuat folder/database")
        return json.loads(buf.getvalue())

    def per_nama(self, out):
        return {k["nama"]: k for k in out["karyawan"]}

    def masalah(self, out, jenis):
        return [m for m in out["masalah"] if m["jenis"] == jenis]

    def test_01_balasan_pertama_langsung_berisi_rekap(self):
        out = self.jalan(self.csv, "--toleransi", "10")
        self.assertTrue(out["ok"])
        self.assertEqual((out["mode"], out["tersimpan"]), ("baca", False))
        k = self.per_nama(out)
        self.assertEqual((k["Andi"]["terlambat_kali"], k["Andi"]["terlambat_menit"]), (3, 66))
        self.assertEqual((k["Joko"]["terlambat_kali"], k["Joko"]["terlambat_menit"]), (3, 75))
        self.assertEqual((k["Sari"]["terlambat_kali"], k["Sari"]["terlambat_menit"]), (0, 0))
        self.assertEqual((k["Andi"]["hari_terjadwal"], k["Andi"]["hadir"], k["Andi"]["tanpa_keterangan"]), (22, 21, 1))
        self.assertEqual((k["Sari"]["hadir"], k["Sari"]["tanpa_keterangan"]), (19, 3))
        self.assertEqual(k["Sari"]["tanggal_tanpa_keterangan"], ["2026-09-14", "2026-09-21", "2026-09-22"])
        self.assertEqual(k["Sari"]["menit_kerja"], 19 * 490)
        self.assertEqual(k["Andi"]["hari_tidak_lengkap"], 1)
        tidak_lengkap = self.masalah(out, "tap_tidak_lengkap")
        self.assertEqual([(m["nama"], m["tanggal"]) for m in tidak_lengkap], [("Andi", "2026-09-25")])
        self.assertEqual(out["tanggal_kosong_semua"], ["2026-09-14"])
        self.assertEqual(out["periode"]["label"], "September 2026")
        self.assertEqual(out["dibaca"]["catatan"], 121)

    def test_02_teks_siap_kirim_tanpa_jargon_dan_tanpa_lokasi(self):
        out = self.jalan(self.csv, "--toleransi", "10")
        teks = out["teks"]
        self.assertTrue(teks.startswith("REKAP ABSENSI SEPTEMBER 2026"))
        self.assertIn("Terlambat 3x (1 jam 6 menit)", teks)
        self.assertIn("Terlambat 3x (1 jam 15 menit)", teks)
        self.assertIn("Yang saya pakai untuk menghitung:", teks)
        self.assertIn("Kelonggaran telat 10 menit", teks)
        self.assertIn("(anggapan saya, bisa diubah)", teks)
        self.assertIn("belum ada data yang disimpan", teks)
        self.assertNotIn("(A01)", teks)                       # kode internal tidak ditampilkan
        for terlarang in (".db", "KomunitechData", "absensi.py", "python", "database", "--", self.dir, "/tmp",
                          "tap ", "json", "pratinjau"):
            self.assertNotIn(terlarang, teks, terlarang)
        for kalimat in out["pertanyaan"] + out["asumsi"] + out["catatan_file"]:
            for terlarang in (".db", "KomunitechData", "absensi.py", "--", self.dir):
                self.assertNotIn(terlarang, kalimat)

    def test_03_pertanyaan_maksimal_tiga_dan_ringkas(self):
        out = self.jalan(self.csv, "--toleransi", "10")
        q = out["pertanyaan"]
        self.assertEqual(len(q), 3)
        self.assertIn("14/09", q[0])                          # libur bersama?
        self.assertIn("Sari 21/09, 22/09", q[1])              # izin/sakit/cuti/alpa?
        self.assertNotIn("14/09", q[1])                       # tanggal libur bersama tidak ditanyakan dua kali
        self.assertIn("simpan", q[2])                         # tawaran simpan selalu terakhir
        self.assertTrue(all(len(x) < 200 for x in q))

    def test_04_daftar_dari_file_sama_dengan_daftar_eksplisit(self):
        otomatis = self.jalan(self.csv, "--toleransi", "10")
        self.assertTrue(otomatis["daftar_dari_file"])
        self.assertEqual(otomatis["daftar_siap_pakai"], "Andi=1; Sari=2; Joko=3")
        eksplisit = self.jalan(self.csv, "--toleransi", "10", "--daftar", "Andi=1; Sari=2; Joko=3")
        self.assertFalse(eksplisit["daftar_dari_file"])
        nama_saja = self.jalan(self.csv, "--toleransi", "10", "--daftar", "Andi, Sari, Joko")
        for out in (eksplisit, nama_saja):
            k = self.per_nama(out)
            self.assertEqual(k["Andi"]["terlambat_menit"], 66)
            self.assertEqual(k["Joko"]["terlambat_menit"], 75)
        self.assertNotIn("Daftar karyawan dibaca dari isi file", eksplisit["teks"])
        self.assertIn("Daftar karyawan dibaca dari isi file", otomatis["teks"])

    def test_05_libur_dari_pengguna_mengubah_hitungan(self):
        out = self.jalan(self.csv, "--toleransi", "10", "--libur", "2026-09-14")
        k = self.per_nama(out)
        self.assertEqual((k["Andi"]["hari_terjadwal"], k["Andi"]["hadir"], k["Andi"]["tanpa_keterangan"]), (21, 21, 0))
        self.assertEqual((k["Sari"]["hari_terjadwal"], k["Sari"]["tanpa_keterangan"]), (21, 2))
        self.assertEqual(out["tanggal_kosong_semua"], [])
        self.assertIn("Libur/tutup: 14/09", out["teks"])
        self.assertNotIn("Tidak ada tanggal merah", out["teks"])
        self.assertFalse(any("tanggal merah" in x for x in out["asumsi"]))
        q = out["pertanyaan"]
        self.assertEqual(len(q), 3)                           # Sari, jam pulang Andi 25/09, tawaran simpan
        self.assertIn("Sari 21/09, 22/09", q[0])
        self.assertIn("Andi 25/09", q[1])
        self.assertIn("simpan", q[2])

    def test_06_default_tanpa_kelonggaran_dan_pola_6_hari(self):
        nol = self.jalan(self.csv)                            # toleransi 0: 17/09 Joko 08.08 ikut dihitung telat
        self.assertEqual(self.per_nama(nol)["Joko"]["terlambat_kali"], 4)
        self.assertEqual(self.per_nama(nol)["Joko"]["terlambat_menit"], 83)
        self.assertIn("Tanpa kelonggaran", nol["teks"])
        enam = self.jalan(self.buat_csv("enam.csv", 1, 30, sabtu=True), "--daftar", "Andi=1", "--hari-kerja", "6")
        a = self.per_nama(enam)["Andi"]
        self.assertEqual(a["hari_terjadwal"], 26)             # 22 hari Senin-Jumat + 4 Sabtu (5/12/19/26 Sep)
        self.assertEqual(a["hari_kerja_per_minggu"], 6)
        self.assertFalse(any("hari kerja seminggu" in x for x in enam["asumsi"]))     # disebut pengguna
        self.assertTrue(any("hari kerja seminggu" in x for x in nol["asumsi"]))       # anggapan bawaan
        self.assertEqual(self.per_nama(self.jalan(self.csv, "--daftar", "Andi=1"))["Andi"]["hari_terjadwal"], 22)

    def test_07_periode_dibaca_dari_isi_file(self):
        sebagian = self.buat_csv("sebagian.csv", 8, 15)
        out = self.jalan(sebagian, "--toleransi", "10")
        self.assertEqual((out["periode"]["dari"], out["periode"]["sampai"]), ("2026-09-08", "2026-09-15"))
        self.assertEqual(self.per_nama(out)["Sari"]["hari_terjadwal"], 6)   # 8-11 dan 14-15 Sep... (14/09 kosong)
        eksplisit = self.jalan(self.csv, "--bulan", "2026-09", "--toleransi", "10")
        self.assertEqual(eksplisit["periode"]["label"], "September 2026")

    def test_08_gagal_dengan_pesan_biasa(self):
        for argv, potongan in (([os.path.join(self.dir, "tidak-ada.csv")], "tidak ditemukan"),
                               ([self.csv, "--daftar", "Zaki=99"], "tidak ada di daftar"),
                               ([self.csv, "--daftar", "Andi=3201234567890001"], "NIK"),
                               ([self.csv, "--toleransi", "500"], "0-120"),
                               ([self.csv, "--libur", "bukan-tanggal"], "tanggal")):
            out = self.jalan(*argv, kode_harapan=1)
            self.assertFalse(out["ok"])
            self.assertIn(potongan, out["error"], argv)
            self.assertNotIn("Traceback", out["error"])
        aneh = os.path.join(self.dir, "aneh.csv")
        with open(aneh, "w", encoding="utf-8") as f:
            f.write("x,y\n1,2\n")
        self.assertIn("tidak dikenali", self.jalan(aneh, kode_harapan=1)["error"])

    def test_09_buku_yang_sudah_ada_tidak_diubah(self):
        """Buku absensi yang sudah ada dibaca (hanya baca) lalu dipakai; ukuran, waktu ubah, dan isi folder tetap."""
        db = os.path.join(self.dir, "absensi.db")
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(A.main(["init", "--ya", "--db", db]), 0)
            self.assertEqual(A.main(["karyawan", "tambah", "--kode", "Z01", "--nama", "Zulkifli", "--id-mesin", "1",
                                     "--ya", "--db", db]), 0)
        sebelum = os.path.getsize(db), os.path.getmtime(db)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.assertEqual(A.main(["rekap-cepat", self.csv, "--db", db, "--json", "--sekarang", "2026-10-01 09:00"]), 0)
        out = json.loads(buf.getvalue())
        self.assertTrue(out["dari_buku"])
        self.assertEqual([k["nama"] for k in out["karyawan"]], ["Zulkifli"])        # karyawan dari buku, bukan dari file
        self.assertTrue(any("tidak ada di buku absensi" in c for c in out["catatan_file"]))
        self.assertEqual((os.path.getsize(db), os.path.getmtime(db)), sebelum)
        self.assertEqual(sorted(os.listdir(self.dir)), sorted(["absen-sept.csv", "absensi.db"]))

    # ---------------------------------------------------------------- perbaikan putaran 2 (1.0.8)
    def jalan_buku(self, db, *argv, kode_harapan=0, sekarang="2026-10-01 09:00"):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
            kode = A.main(["rekap-cepat"] + list(argv) + ["--db", db, "--json", "--sekarang", sekarang])
        self.assertEqual(kode, kode_harapan, buf.getvalue())
        return json.loads(buf.getvalue())

    def cli(self, db, *argv, sekarang="2026-10-01 09:00"):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
            kode = A.main(list(argv) + ["--db", db, "--json", "--sekarang", sekarang])
        self.assertEqual(kode, 0, buf.getvalue())
        return json.loads(buf.getvalue())

    def buat_toko6(self):
        """Toko 4 orang, Agustus 2026, Senin-Sabtu: Senin-Jumat 08.00-16.00, Sabtu pulang 13.00; 17/08 libur.
        Semua masuk 07.55; pulang 16.05 (Senin-Jumat) atau 13.02 (Sabtu)."""
        import datetime as dt
        baris = ["No.,AC-No.,Nama,Waktu,Status"]
        n = 0
        for tgl in range(1, 32):
            d = dt.date(2026, 8, tgl)
            if d.weekday() == 6 or tgl == 17:
                continue
            for idm, nm in (("1", "Andi"), ("2", "Sari"), ("3", "Budi"), ("4", "Dewi")):
                n += 2
                baris.append("%d,%s,%s,%s 07:55:00,C/In" % (n - 1, idm, nm, d.strftime("%d/%m/%Y")))
                baris.append("%d,%s,%s,%s %s,C/Out" % (n, idm, nm, d.strftime("%d/%m/%Y"),
                                                       "13:02:00" if d.weekday() == 5 else "16:05:00"))
        p = os.path.join(self.dir, "toko6.csv")
        with open(p, "w", encoding="utf-8") as f:
            f.write("\n".join(baris) + "\n")
        return p

    def test_11_sabtu_pulang_awal_pola_6_hari(self):
        """Verifikasi manual (Agustus 2026: 25 hari kerja = 20 Senin-Jumat + 5 Sabtu 1/8/15/22/29; 17/08 libur):
        Senin-Jumat 07.55-16.05 = 490 menit - istirahat 60 = 430; Sabtu 07.55-13.02 = 307 menit.
        Dengan jam pulang Sabtu 13.00 (tanpa potongan istirahat): 20 x 430 + 5 x 307 = 10.135 menit.
        Tanpa itu, Sabtu dianggap pulang 16.00: tiap Sabtu 307 - 60 = 247 dan pulang cepat 178 menit
        (13.02 -> 16.00): 20 x 430 + 5 x 247 = 9.835 menit; pulang cepat 5x = 890 menit."""
        csv = self.buat_toko6()
        dasar = [csv, "--hari-kerja", "6", "--masuk", "08.00", "--pulang", "16.00", "--istirahat", "60",
                 "--libur", "2026-08-17"]
        benar = self.jalan(*dasar, "--pulang-hari-pendek", "13.00")
        a = self.per_nama(benar)["Andi"]
        self.assertEqual((a["hari_terjadwal"], a["menit_kerja"], a["pulang_cepat_kali"]), (25, 10135, 0))
        self.assertTrue(any("Sabtu pulang jam 13.00" in x for x in benar["pengaturan_dipakai"]))
        self.assertFalse(any("Sabtu" in x for x in benar["asumsi"]))              # disebut pengguna
        self.assertFalse(any("Sabtu" in x for x in benar["pertanyaan"]))
        # sama dengan alur buku absensi tersimpan (jadwal kerja dengan jam pulang hari pendek)
        db = os.path.join(self.dir, "buku6", "absensi.db")
        self.cli(db, "init", "--ya")
        self.cli(db, "shift", "tambah", "--kode", "REG", "--masuk", "08.00", "--pulang", "16.00", "--istirahat", "60",
                 "--pulang-hari-pendek", "13.00", "--ya")
        for kode, nama, idm in (("A01", "Andi", "1"), ("A02", "Sari", "2"), ("A03", "Budi", "3"), ("A04", "Dewi", "4")):
            self.cli(db, "karyawan", "tambah", "--kode", kode, "--nama", nama, "--id-mesin", idm, "--hari-kerja", "6",
                     "--mulai", "2026-08-01", "--ya")
        self.cli(db, "libur", "tambah", "--tanggal", "2026-08-17", "--nama", "Libur", "--ya")
        self.cli(db, "impor-absen", csv, "--ya")
        rk = {k["nama"]: k for k in self.cli(db, "rekap", "--bulan", "2026-08")["karyawan"]}
        for nama in ("Andi", "Sari", "Budi", "Dewi"):
            self.assertEqual(rk[nama]["menit_kerja"], self.per_nama(benar)[nama]["menit_kerja"], nama)
        # tanpa opsi Sabtu: angka bergeser, ditandai anggapan, dan Sabtu ditanyakan
        salah = self.jalan(*dasar)
        a = self.per_nama(salah)["Andi"]
        self.assertEqual((a["menit_kerja"], a["pulang_cepat_kali"], a["pulang_cepat_menit"]), (9835, 5, 890))
        self.assertTrue(any("Sabtu dihitung hari kerja biasa" in x for x in salah["asumsi"]))
        self.assertIn("Sabtu", salah["pertanyaan"][0])
        self.assertIn("Sabtu dihitung hari kerja biasa", salah["teks"])
        self.assertEqual(len(salah["pertanyaan"]), 2)                             # Sabtu + tawaran simpan

    def test_12_opsi_lengkap_dari_pengguna_hanya_tanggal_merah_jadi_anggapan(self):
        out = self.jalan(self.csv, "--daftar", "Andi=1; Sari=2; Joko=3", "--hari-kerja", "5", "--masuk", "08.00",
                         "--pulang", "17.00", "--istirahat", "60", "--toleransi", "10")
        self.assertEqual(out["asumsi"], ["Tidak ada tanggal merah atau libur khusus"])
        self.assertIn("Jam kerja 08.00-17.00, istirahat 60 menit\n", out["teks"])
        self.assertIn("5 hari kerja seminggu, libur mingguan Sabtu dan Minggu\n", out["teks"])

    def siapkan_buku(self, nama_folder="buku"):
        """Alur simpan A0 langkah 4: kelonggaran 10, 14/09 tutup, Sari izin 21-22/09, file September dimasukkan."""
        db = os.path.join(self.dir, nama_folder, "absensi.db")
        self.cli(db, "init", "--ya")
        self.cli(db, "atur", "--toleransi", "10", "--ya")
        for kode, nama, idm in (("A01", "Andi", "1"), ("A02", "Sari", "2"), ("A03", "Joko", "3")):
            self.cli(db, "karyawan", "tambah", "--kode", kode, "--nama", nama, "--id-mesin", idm,
                     "--mulai", "2026-09-01", "--ya")
        self.cli(db, "libur", "tambah", "--tanggal", "2026-09-14", "--nama", "Tutup", "--ya")
        self.cli(db, "impor-absen", self.csv, "--ya")
        self.cli(db, "keterangan", "--karyawan", "Sari", "--jenis", "izin", "--tanggal", "2026-09-21",
                 "--sampai", "2026-09-22", "--ya")
        return db

    def test_13_pengguna_kembali_memakai_pengaturan_tersimpan(self):
        """Buku sudah ada: kelonggaran telat, libur, izin yang tersimpan dipakai; bukan nilai bawaan."""
        db = self.siapkan_buku()
        dari_buku = {k["nama"]: k for k in self.cli(db, "rekap", "--bulan", "2026-09")["karyawan"]}
        sebelum = os.path.getsize(db), os.path.getmtime(db)
        out = self.jalan_buku(db, self.csv)                                        # tanpa opsi apa pun
        self.assertTrue(out["dari_buku"])
        k = self.per_nama(out)
        for nama in ("Andi", "Sari", "Joko"):
            for f in ("terlambat_kali", "terlambat_menit", "hadir", "hari_terjadwal", "izin", "tanpa_keterangan",
                      "menit_kerja"):
                self.assertEqual(k[nama][f], dari_buku[nama][f], (nama, f))
        self.assertEqual((k["Joko"]["terlambat_kali"], k["Joko"]["terlambat_menit"]), (3, 75))
        self.assertEqual((k["Sari"]["izin"], k["Sari"]["tanpa_keterangan"]), (2, 0))
        self.assertNotIn("Tanpa kelonggaran", out["teks"])
        self.assertIn("Kelonggaran telat 10 menit (dari buku absensi)", out["teks"])
        self.assertIn("Libur/tutup: 14/09", out["teks"])
        self.assertEqual(out["asumsi"], [])                                        # semuanya dari buku
        self.assertNotIn("supaya bulan depan", " ".join(out["pertanyaan"]))        # tawaran simpan tidak muncul lagi
        self.assertFalse(any("14/09" in x for x in out["pertanyaan"]))             # sudah dijawab, tidak ditanya lagi
        self.assertTrue(any("sudah ada di buku absensi" in c for c in out["catatan_file"]))
        for terlarang in (".db", "KomunitechData", "absensi.py", "--", self.dir, "database"):
            self.assertNotIn(terlarang, out["balasan"], terlarang)
        self.assertEqual((os.path.getsize(db), os.path.getmtime(db)), sebelum)     # buku tidak disentuh

    def test_14_bulan_berikutnya_orang_baru_dan_tawaran_masukkan_file(self):
        db = self.siapkan_buku()
        okt = os.path.join(self.dir, "absen-okt.csv")
        with open(self.csv, encoding="utf-8") as f:
            isi = f.read().replace("/09/2026", "/10/2026")
        with open(okt, "w", encoding="utf-8") as f:
            f.write(isi + "999,9,Tamu,05/10/2026 08:00:00,C/In\n")
        out = self.jalan_buku(db, okt, sekarang="2026-11-02 09:00", kode_harapan=0)
        self.assertTrue(out["dari_buku"])
        self.assertEqual(out["periode"]["label"], "Oktober 2026")
        self.assertEqual({k["nama"] for k in out["karyawan"]}, {"Andi", "Sari", "Joko"})
        q = " ".join(out["pertanyaan"])
        self.assertIn("Tamu", q)                                                   # kemungkinan karyawan baru
        self.assertEqual(out["pertanyaan"][-1], "Mau saya masukkan file ini ke buku absensi Anda, supaya tercatat "
                                                "bersama bulan-bulan sebelumnya? Balas \"ya\" bila mau.")
        self.assertLessEqual(len(out["pertanyaan"]), 3)
        self.assertEqual(out["dibaca"]["sudah_ada"], 0)
        self.assertIn("file ini belum dimasukkan ke buku absensi Anda", out["teks"])
        # jadwal yang berbeda dari yang tersimpan tidak diam-diam dipakai
        beda = self.jalan_buku(db, okt, "--masuk", "09.00", sekarang="2026-11-02 09:00")
        self.assertTrue(any("berbeda dari jadwal yang tersimpan" in c for c in beda["catatan_file"]))
        self.assertEqual(self.per_nama(beda)["Andi"]["terlambat_menit"], self.per_nama(out)["Andi"]["terlambat_menit"])

    def test_15_pesan_panjang_dipecah_antar_karyawan(self):
        import datetime as dt
        orang = [(str(i), "Karyawan%02d" % i) for i in range(1, 31)]
        baris = ["No.,AC-No.,Nama,Waktu,Status"]
        n = 0
        for tgl in (1, 2, 3, 4):
            for idm, nm in orang:
                d = dt.date(2026, 9, tgl)
                n += 2
                baris.append("%d,%s,%s,%s 07:55:00,C/In" % (n - 1, idm, nm, d.strftime("%d/%m/%Y")))
                if not (idm == "7" and tgl == 3):
                    baris.append("%d,%s,%s,%s 17:05:00,C/Out" % (n, idm, nm, d.strftime("%d/%m/%Y")))
        besar = os.path.join(self.dir, "besar.csv")
        with open(besar, "w", encoding="utf-8") as f:
            f.write("\n".join(baris) + "\n")
        out = self.jalan(besar)
        self.assertGreater(len(out["balasan"]), A.BATAS_PESAN)
        pesan = out["pesan"]
        self.assertGreaterEqual(len(pesan), 2)
        self.assertTrue(all(len(x) <= A.BATAS_PESAN for x in pesan), [len(x) for x in pesan])
        self.assertEqual("\n\n".join(pesan), out["balasan"])                        # tidak ada yang hilang
        self.assertTrue(pesan[0].startswith("Sudah saya rekap dari file Anda."))
        self.assertIn("1) ", pesan[-1])                                            # pertanyaan di pesan terakhir
        for i, (_, nm) in enumerate(orang, start=1):                               # satu karyawan tidak terbelah
            kepala = "%d. %s\n" % (i, nm)
            ada = [j for j, x in enumerate(pesan) if kepala in x]
            self.assertEqual(len(ada), 1, kepala)
            bagian = pesan[ada[0]].split(kepala)[1].split("\n\n")[0]
            self.assertIn("Jam kerja", bagian)
        # balasan kecil tetap satu pesan
        self.assertEqual(len(self.jalan(self.csv, "--toleransi", "10")["pesan"]), 1)

    def test_16_file_lebih_dari_satu_bulan_diberi_catatan(self):
        import datetime as dt
        baris = ["No.,AC-No.,Nama,Waktu,Status"]
        n = 0
        d = dt.date(2026, 7, 1)
        while d <= dt.date(2026, 9, 30):
            if d.weekday() < 5:
                for idm, nm in (("1", "Andi"), ("2", "Sari")):
                    n += 2
                    baris.append("%d,%s,%s,%s 07:55:00,C/In" % (n - 1, idm, nm, d.strftime("%d/%m/%Y")))
                    baris.append("%d,%s,%s,%s 17:05:00,C/Out" % (n, idm, nm, d.strftime("%d/%m/%Y")))
            d += dt.timedelta(days=1)
        tiga = os.path.join(self.dir, "tiga-bulan.csv")
        with open(tiga, "w", encoding="utf-8") as f:
            f.write("\n".join(baris) + "\n")
        out = self.jalan(tiga)
        self.assertEqual(out["periode"]["label"], "September 2026")
        self.assertEqual((out["dibaca"]["dari"], out["dibaca"]["sampai"]), ("2026-07-01", "2026-09-30"))
        catatan = " ".join(out["catatan_file"])
        self.assertIn("File berisi catatan dari 01/07/2026 sampai 30/09/2026", catatan)
        self.assertIn("yang saya hitung hanya 01/09/2026-30/09/2026", catatan)
        self.assertIn("Catatan dari file:", out["teks"])
        agustus = self.jalan(tiga, "--bulan", "2026-08")                           # bulan dipilih pengguna
        self.assertEqual(agustus["periode"]["label"], "Agustus 2026")
        self.assertIn("yang saya hitung hanya 01/08/2026-31/08/2026", " ".join(agustus["catatan_file"]))
        # file yang pas satu bulan tidak diberi catatan itu
        self.assertFalse(any("File berisi catatan" in c for c in self.jalan(self.csv)["catatan_file"]))

    def test_17_pesan_dipecah_unit(self):
        self.assertEqual(A.bagi_pesan("pendek"), ["pendek"])
        par = ["Paragraf %d\n%s" % (i, "x" * 40) for i in range(10)]
        hasil = A.bagi_pesan("\n\n".join(par), batas=200)
        self.assertGreater(len(hasil), 1)
        self.assertTrue(all(len(x) <= 200 for x in hasil))
        self.assertEqual("\n\n".join(hasil), "\n\n".join(par))
        panjang = "\n".join("baris %d %s" % (i, "y" * 30) for i in range(30))       # satu paragraf besar: dipotong per baris
        pecah = A.bagi_pesan(panjang, batas=300)
        self.assertTrue(all(len(x) <= 300 for x in pecah))
        self.assertEqual("\n".join(pecah).replace("\n\n", "\n"), panjang)
        satu_baris = A.bagi_pesan("z" * 700, batas=300)                             # satu baris melebihi batas
        self.assertEqual([len(x) for x in satu_baris], [300, 300, 100])

    def test_18_buku_kosong_diperlakukan_seperti_belum_ada(self):
        db = os.path.join(self.dir, "kosong", "absensi.db")
        self.cli(db, "init", "--ya")                                              # ada buku, belum ada karyawan
        out = self.jalan_buku(db, self.csv, "--toleransi", "10")
        self.assertFalse(out["dari_buku"])
        self.assertTrue(out["daftar_dari_file"])
        self.assertIn("supaya bulan depan", " ".join(out["pertanyaan"]))
        self.assertEqual(out["asumsi"], ["Jam kerja 08.00-17.00, istirahat 60 menit",
                                         "5 hari kerja seminggu, libur mingguan Sabtu dan Minggu",
                                         "Tidak ada tanggal merah atau libur khusus",
                                         "Daftar karyawan dibaca dari isi file"])

    def test_19_libur_dan_kelonggaran_dari_pengguna_menimpa_buku_hanya_untuk_rekap_ini(self):
        db = self.siapkan_buku()
        sebelum = os.path.getsize(db), os.path.getmtime(db)
        out = self.jalan_buku(db, self.csv, "--toleransi", "20", "--libur", "2026-09-15")
        k = self.per_nama(out)
        self.assertEqual(k["Andi"]["terlambat_kali"], 2)                           # 15/09 08.12 kini libur, 08.23/08.31 tetap
        self.assertEqual(k["Andi"]["terlambat_menit"], 54)                         # 23 + 31
        self.assertEqual(k["Joko"]["terlambat_menit"], 45)                         # hanya 24/09 08.45; 14 dan 16 di bawah 20
        self.assertIn("Kelonggaran telat 20 menit\n", out["teks"])
        self.assertNotIn("(dari buku absensi)", out["teks"].split("Kelonggaran telat 20 menit")[1].split("\n")[0])
        self.assertIn("Libur/tutup: 14/09, 15/09", out["teks"])
        self.assertEqual((os.path.getsize(db), os.path.getmtime(db)), sebelum)
        asli = self.cli(db, "info")["pengaturan"]["toleransi_telat"]
        self.assertEqual(asli, 10)                                                 # pengaturan tersimpan tidak berubah

    def test_10_versi_dan_catatan_revisi_sinkron(self):
        self.assertRegex(A.VERSI, r"^\d+\.\d+\.\d+$")
        import upah_harian as U
        self.assertEqual(U.VERSI, A.VERSI)
        with open(os.path.join(AKAR, "CHANGELOG.md"), encoding="utf-8") as fh:
            self.assertIn("## Catatan revisi %s (" % A.VERSI, fh.read())
        with open(os.path.join(AKAR, "README.md"), encoding="utf-8") as fh:
            self.assertIn("Versi terkini: **%s**" % A.VERSI, fh.read())


class UjiBahasaChat(Dasar):
    """Teks yang bisa sampai ke pemilik usaha tidak boleh memuat istilah teknis, nama opsi, atau nama perintah."""

    def teks(self, *argv):
        argv = list(argv) + ["--db", self.db, "--sekarang", KINI]
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            kode = A.main(argv)
        return kode, out.getvalue(), err.getvalue()

    def test_pesan_masalah_tanpa_jargon(self):
        self.karyawan("A01", "Andi", "--shift", "REG")
        self.ok("catat", "--karyawan", "A01", "--tanggal", "2026-09-03", "--masuk", "08.00", "--pulang", "20.00", "--ya")
        self.ok("keterangan", "--karyawan", "A01", "--jenis", "sakit", "--tanggal", "2026-09-03", "--ya")
        self.ok("catat", "--karyawan", "A01", "--tanggal", "2026-09-02", "--masuk", "08.00", "--pulang", "19.30", "--ya")
        rk, out = self.rekap()
        gabung = " ".join(m["pesan"] for m in out["masalah"])
        self.assertIn("jam masuk/pulang dari absen", gabung)
        self.assertIn("catat sebagai lembur disetujui", gabung)
        self.assertNotIn("perintah lembur", gabung)
        self.assertNotIn("tap absen", gabung)
        self.assertNotIn("--", gabung)

    def test_upah_belum_diisi_dan_catatan_lembur_tanpa_opsi(self):
        self.karyawan("B01", "Budi")
        pratinjau = self.ok("lembur", "--karyawan", "B01", "--tanggal", "2026-09-01", "--jam", "2")
        self.assertTrue(any("Sebaiknya sebutkan siapa" in c for c in pratinjau["catatan"]), pratinjau["catatan"])
        self.assertFalse(any("--" in c for c in pratinjau["catatan"]), pratinjau["catatan"])
        self.ok("lembur", "--karyawan", "B01", "--tanggal", "2026-09-01", "--jam", "2", "--catatan", "x", "--ya")
        _, out = self.rekap()
        pesan = " ".join(m["pesan"] for m in self.masalah(out, "upah_belum_diisi"))
        self.assertIn("gaji pokok + tunjangan tetap", pesan)
        self.assertNotIn("--", pesan)

    def test_teks_rekap_tanpa_data_tidak_menyebut_istilah_tap(self):
        self.karyawan("A01", "Andi")
        _, teks, _ = self.teks("rekap", "--bulan", "2026-09")
        self.assertIn("Belum ada data absen", teks)
        self.assertNotIn("(tap)", teks)
        self.assertNotIn("impor", teks.lower())


    def test_rekap_tanpa_kode_internal_dan_istilah_seragam(self):
        self.karyawan("A01", "Andi")
        self.karyawan("A02", "Sari")
        self.ok("atur", "--toleransi", "10", "--ya")
        self.ok("libur", "tambah", "--tanggal", "2026-09-14", "--nama", "Tutup", "--ya")
        self.ok("libur", "tambah", "--tanggal", "2026-09-17", "--nama", "", "--ya")
        self.ok("catat", "--karyawan", "A01", "--tanggal", "2026-09-02", "--masuk", "08.00", "--pulang", "17.00", "--ya")
        _, out = self.rekap()
        teks = out["teks"]
        self.assertEqual(teks, "\n".join(teks.split("\n")))
        self.assertIn("kelonggaran telat 10 menit", teks)
        self.assertNotIn("toleransi", teks.lower())
        self.assertIn("Libur/tutup: 14/09/2026 Tutup, 17/09/2026", teks)
        self.assertNotIn("Libur resmi", teks)
        self.assertIn("1. Andi\n", teks)
        self.assertNotIn("(A01)", teks)
        self.assertEqual("\n\n".join(out["pesan"]), teks)
        # nama kembar: kode ditampilkan supaya bisa dibedakan
        self.karyawan("A03", "Andi")
        _, out = self.rekap()
        self.assertIn("Andi (A01)", out["teks"])
        self.assertIn("Andi (A03)", out["teks"])
        self.assertNotIn("Sari (A02)", out["teks"])

    def test_catatan_lebih_dari_40_tanpa_istilah_csv_json(self):
        for i in range(1, 42):
            self.karyawan("B%02d" % i, "Orang%02d" % i)
            self.ok("catat", "--karyawan", "B%02d" % i, "--tanggal", "2026-09-01", "--masuk", "08.00", "--ya")
        _, out = self.rekap()
        self.assertIn("dan 1 catatan lainnya", out["teks"])
        self.assertNotIn("CSV", out["teks"])
        self.assertNotIn("JSON", out["teks"])

    def test_teks_buku_baru_dan_info_tanpa_alamat_dan_istilah_teknis(self):
        db2 = os.path.join(self.dir, "baru", "absensi.db")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.assertEqual(A.main(["init", "--db", db2]), 0)
        teks = buf.getvalue()
        for terlarang in (".db", "field", "--", self.dir, "toleransi", "Toleransi", "folder"):
            self.assertNotIn(terlarang, teks, terlarang)
        self.assertIn("Kelonggaran telat", teks)
        self.assertFalse(os.path.exists(db2))                                       # hanya rencana, belum dibuat
        self.karyawan("A01", "Andi")
        _, info, _ = self.teks("info")
        for terlarang in (self.dir, ".db", "Database", "Tap ", "Shift", "Toleransi"):
            self.assertNotIn(terlarang, info, terlarang)
        self.assertIn("Kelonggaran telat", info)
        _, atur, _ = self.teks("atur", "--toleransi", "5")
        self.assertIn("Kelonggaran telat", atur)
        self.assertNotIn("Tap ganda", atur)


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
