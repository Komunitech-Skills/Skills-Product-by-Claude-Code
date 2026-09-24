#!/usr/bin/env python3
"""Uji regresi crm-wa. Jalankan: python3 tests/uji_regresi.py  (Windows: py tests/uji_regresi.py)

Hanya library standar. Semua data fiktif (nomor dummy 0812-0000-xxxx), dibuat di folder sementara.
Angka rekap diverifikasi dengan rumus manual di komentar tiap tes:
  konversi  = lead periode yang kini deal/selesai / lead masuk periode x 100%   (1 desimal, 0,05 ke atas)
  win rate  = deal/selesai / (deal/selesai + batal) dari lead periode
  rata nilai= jumlah nilai deal baru / jumlah deal bernilai, dibulatkan ke rupiah terdekat (0,5 ke atas)
  lama closing = rata-rata (tgl_deal - tgl_masuk) hari, 1 desimal
"""
import contextlib
import csv
import hashlib
import io
import json
import os
import re
import shutil
import sqlite3
import sys
import tempfile
import unittest
from datetime import date, datetime, timezone
from urllib.parse import unquote

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AKAR, "scripts"))
import crm as C  # noqa: E402

HARI = "2026-09-24"   # Kamis


class Dasar(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.db = os.path.join(self.dir, "crm.db")
        self.ok("init", "--nama-usaha", "Dapur Contoh", "--pengirim", "Sari", "--ya")

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def run_cli(self, *argv, hari=HARI, db=None):
        argv = list(argv) + ["--db", db or self.db, "--json", "--hari-ini", hari]
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
            kode = C.main(argv)
        return kode, json.loads(buf.getvalue())

    def ok(self, *argv, **kw):
        kode, out = self.run_cli(*argv, **kw)
        self.assertEqual(kode, 0, out)
        self.assertTrue(out["ok"], out)
        return out

    def gagal(self, *argv, **kw):
        kode, out = self.run_cli(*argv, **kw)
        self.assertEqual(kode, 1, out)
        self.assertFalse(out["ok"])
        return out

    def jumlah(self):
        c = sqlite3.connect(self.db)
        try:
            return c.execute("SELECT COUNT(*) FROM kontak").fetchone()[0]
        finally:
            c.close()

    def sha(self, p):
        with open(p, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()

    def file(self, nama, isi, encoding="utf-8"):
        p = os.path.join(self.dir, nama)
        with open(p, "w", encoding=encoding, newline="") as f:
            f.write(isi)
        return p


class UjiNomor(unittest.TestCase):
    def test_normalisasi_berbagai_format(self):
        for masuk in ("0812-0000-1234", "0812 0000 1234", "+62 812-0000-1234", "62812 0000 1234", "812-0000-1234",
                      "(0812) 0000-1234", "0062 812 0000 1234", "WA: 0812.0000.1234", "+62 (0)812 0000 1234"):
            self.assertEqual(C.normalisasi_wa(masuk)[0], "6281200001234", masuk)

    def test_nomor_ditolak(self):
        for salah in ("0812-000", "08120000123456789", "abc", "6.28120E+12", "0812-0000-1234 / 0813-0000-5678",
                      "12345678", "", "0812 atau 0813 0000 1111 2222 x"):
            with self.assertRaises(C.Gagal, msg=salah):
                C.normalisasi_wa(salah)

    def test_telepon_kantor_dan_luar_negeri_diberi_peringatan(self):
        wa, p = C.normalisasi_wa("021-5550-0000")
        self.assertEqual(wa, "622155500000")
        self.assertTrue(any("bukan nomor HP" in x for x in p))
        wa, p = C.normalisasi_wa("+60 12-000 0000")
        self.assertEqual(wa, "60120000000")
        self.assertTrue(p)

    def test_tampil_dan_samarkan(self):
        self.assertEqual(C.tampil_wa("6281200001234"), "0812-0000-1234")
        self.assertEqual(C.samar_wa("6281200001234"), "0812-****-1234")
        self.assertEqual(C.samar_nama("Bu Rina Wati"), "Bu R.")
        self.assertEqual(C.samar_nama("PT Maju Jaya"), "PT M.")
        self.assertEqual(C.samar_nama("Rina"), "R.")


class UjiNominalTanggal(unittest.TestCase):
    def test_nominal(self):
        kasus = {"450rb": 450000, "4,5 jt": 4500000, "4.500.000": 4500000, "Rp4.500.000": 4500000,
                 "Rp 4.500.000,-": 4500000, "4 jt 500 rb": 4500000, "1,2 M": 1200000000, "750 ribu": 750000,
                 "4500000": 4500000, "2.5jt": 2500000, "1,25 jt": 1250000, "4.500.000,00": 4500000,
                 "12 juta": 12000000, "0": 0, "4,275 jt": 4275000, "1,5 M": 1500000000}
        for teks, harap in kasus.items():
            self.assertEqual(C.parse_nominal(teks), harap, teks)

    def test_nominal_ambigu_ditolak(self):
        for teks in ("5m", "1.500 jt", "4,5", "-100rb", "1,2345 jt", "4 jt 500", "abc", "1,5 ekor", "4,5,6 jt"):
            with self.assertRaises(C.Gagal, msg=teks):
                C.parse_nominal(teks)

    def test_tanggal(self):
        a = date(2026, 9, 24)  # Kamis
        self.assertEqual(C.baca_tanggal("besok", a)[0], date(2026, 9, 25))
        self.assertEqual(C.baca_tanggal("Jumat", a)[0], date(2026, 9, 25))
        self.assertEqual(C.baca_tanggal("Kamis", a)[0], date(2026, 10, 1))      # hari ini Kamis -> Kamis depan
        self.assertEqual(C.baca_tanggal("3 hari lagi", a)[0], date(2026, 9, 27))
        self.assertEqual(C.baca_tanggal("3/10", a)[0], date(2026, 10, 3))
        self.assertEqual(C.baca_tanggal("3 Okt", a)[0], date(2026, 10, 3))
        self.assertEqual(C.baca_tanggal("tgl 5", a)[0], date(2026, 10, 5))
        self.assertEqual(C.baca_tanggal("5/1", a)[0], date(2027, 1, 5))         # Januari -> tahun depan
        self.assertEqual(C.baca_tanggal("bulan depan", a)[0], date(2026, 10, 24))
        self.assertEqual(C.baca_tanggal("20/9", a, "lalu")[0], date(2026, 9, 20))
        with self.assertRaises(C.Gagal):   # follow-up tanpa tahun yang baru lewat -> tanya, jangan tebak
            C.baca_tanggal("20/9", a, "depan")
        with self.assertRaises(C.Gagal):   # tanggal kejadian di masa depan
            C.baca_tanggal("besok", a, "lalu")
        with self.assertRaises(C.Gagal):
            C.baca_tanggal("31/2/2026", a)
        d, cat = C.baca_tanggal("22/9/2026", a, "depan")                      # tahun ditulis -> boleh, terlambat
        self.assertEqual(d, date(2026, 9, 22))
        self.assertTrue(any("TERLAMBAT" in c for c in cat))

    def test_persen_dan_bulat(self):
        self.assertEqual(C.persen(1, 3), (33.3, "33,3%"))
        self.assertEqual(C.persen(2, 3), (66.7, "66,7%"))
        self.assertEqual(C.persen(1, 8), (12.5, "12,5%"))
        self.assertEqual(C.persen(1, 16), (6.3, "6,3%"))    # 6,25 -> 6,3 (setengah ke atas)
        self.assertEqual(C.persen(0, 0), (None, "-"))
        from fractions import Fraction
        self.assertEqual(C.bulat(Fraction(2000001, 2)), 1000001)  # 1.000.000,5 -> 1.000.001


class UjiZonaWaktu(unittest.TestCase):
    def test_wib_wita_wit(self):
        u = datetime(2026, 9, 23, 17, 30, tzinfo=timezone.utc)
        self.assertEqual(C.waktu_lokal("WIB", u), datetime(2026, 9, 24, 0, 30))   # sudah tanggal 24 di WIB
        self.assertEqual(C.waktu_lokal("WITA", u), datetime(2026, 9, 24, 1, 30))
        self.assertEqual(C.waktu_lokal("WIT", u), datetime(2026, 9, 24, 2, 30))
        u2 = datetime(2026, 9, 23, 16, 59, tzinfo=timezone.utc)
        self.assertEqual(C.waktu_lokal("WIB", u2).date(), date(2026, 9, 23))
        self.assertEqual(C.waktu_lokal("WITA", u2).date(), date(2026, 9, 24))

    def test_alias_zona(self):
        self.assertEqual(C.kode_zona("Asia/Makassar"), "WITA")
        with self.assertRaises(C.Gagal):
            C.kode_zona("Europe/London")


class UjiZonaDatabase(Dasar):
    def test_zona_tersimpan_dipakai(self):
        db2 = os.path.join(self.dir, "wita.db")
        self.ok("init", "--zona", "WITA", "--ya", db=db2)
        info = self.ok("info", db=db2)
        self.assertEqual(info["pengaturan"]["zona"], "WITA")
        out = self.ok("hari-ini", db=db2)
        self.assertEqual(out["zona"], "WITA")


class UjiKontakDanDuplikat(Dasar):
    def test_tambah_dan_duplikat_ditolak(self):
        out = self.ok("tambah", "--nama", "Bu Rina", "--wa", "0812-0000-1001", "--sumber", "ig", "--nilai", "450rb")
        self.assertEqual(out["kontak"]["kode"], "K0001")
        self.assertEqual(out["kontak"]["wa"], "6281200001001")
        self.assertEqual(out["kontak"]["sumber"], "Instagram")
        self.assertEqual(out["kontak"]["followup"], HARI)            # lead baru -> hari ini
        g = self.gagal("tambah", "--nama", "Rina", "--wa", "+62 812 0000 1001")
        self.assertEqual(g["duplikat"][0]["kode"], "K0001")
        self.assertEqual(self.jumlah(), 1)
        self.ok("tambah", "--nama", "Suami Bu Rina", "--wa", "6281200001001", "--izinkan-duplikat")
        self.assertEqual(self.jumlah(), 2)
        cek = self.ok("cek-duplikat")
        self.assertEqual(len(cek["nomor_sama"]), 1)

    def test_nama_berisi_nomor_ditolak(self):
        self.gagal("tambah", "--nama", "Rina 081200001001")

    def test_ubah_nomor_ke_nomor_kontak_lain_ditolak(self):
        self.ok("tambah", "--nama", "A", "--wa", "081200001001")
        self.ok("tambah", "--nama", "B", "--wa", "081200001002")
        self.gagal("ubah", "--kontak", "B", "--wa", "0812-0000-1001")

    def test_kontak_ambigu_minta_pilihan(self):
        self.ok("tambah", "--nama", "Bu Rina", "--wa", "081200001001")
        self.ok("tambah", "--nama", "Rina Salon", "--wa", "081200001002")
        self.ok("tambah", "--nama", "Rina Katering", "--wa", "081200001003")
        g = self.gagal("catat", "--kontak", "rin", "--isi", "halo")
        self.assertGreaterEqual(len(g["pilihan"]), 2)
        self.ok("catat", "--kontak", "081200001002", "--isi", "via nomor")
        self.ok("catat", "--kontak", "K3", "--isi", "via kode")

    def test_gabung_perlu_ya_dan_memindah_riwayat(self):
        self.ok("tambah", "--nama", "Bu Rina", "--wa", "081200001001", "--sumber", "ig")
        self.ok("tambah", "--nama", "Rina", "--nilai", "1 jt", "--kebutuhan", "kue", "--label", "vip",
                "--catatan", "catatan penting")
        pra = self.ok("gabung", "--dari", "K0002", "--ke", "K0001")
        self.assertEqual(pra["mode"], "pratinjau")
        self.assertEqual(self.jumlah(), 2)
        out = self.ok("gabung", "--dari", "K0002", "--ke", "K0001", "--ya")
        self.assertTrue(os.path.isfile(out["backup"]))
        self.assertEqual(self.jumlah(), 1)
        k = self.ok("lihat", "--kontak", "K0001")
        self.assertEqual(k["kontak"]["nilai"], 1000000)
        self.assertEqual(k["kontak"]["kebutuhan"], "kue")
        self.assertEqual(k["kontak"]["label"], ["vip"])
        self.assertTrue(any(r["isi"] == "catatan penting" for r in k["riwayat"]))


class UjiTahapDanFollowUp(Dasar):
    def setUp(self):
        super().setUp()
        self.ok("tambah", "--nama", "Bu Rina", "--wa", "081200001001", "--kebutuhan", "kue ulang tahun")

    def test_batal_wajib_alasan_dan_dinormalkan(self):
        self.gagal("catat", "--kontak", "K0001", "--tahap", "batal")
        out = self.ok("catat", "--kontak", "K0001", "--tahap", "gak jadi", "--alasan", "kemahalan")
        self.assertEqual(out["kontak"]["tahap"], "batal")
        self.assertEqual(out["kontak"]["alasan_batal"], "harga terlalu mahal")
        self.assertIsNone(out["kontak"]["followup"])
        self.gagal("terkirim", "--kontak", "K0001")
        self.assertIsNone(self.ok("hari-ini")["draf"] or None)

    def test_irama_terkirim_dan_draf(self):
        d = self.ok("draf", "--kontak", "K0001")
        self.assertEqual(d["jenis"], "sapaan-awal")
        self.assertIn("Bu Rina", d["draf"])
        self.assertEqual(unquote(d["tautan"].split("?text=")[1]), d["draf"])   # tautan = draf persis
        self.assertTrue(d["tautan"].startswith("https://wa.me/6281200001001?text="))
        o = self.ok("terkirim", "--kontak", "K0001")                          # baru -> dihubungi, +2 hari
        self.assertEqual(o["kontak"]["tahap"], "dihubungi")
        self.assertEqual(o["kontak"]["followup"], "2026-09-26")
        self.assertEqual(self.ok("draf", "--kontak", "K0001")["jenis"], "follow-up-1")
        o = self.ok("terkirim", "--kontak", "K0001")                          # ke-1 -> +3 hari
        self.assertEqual(o["kontak"]["followup"], "2026-09-27")
        self.assertEqual(self.ok("draf", "--kontak", "K0001")["jenis"], "pilihan-mudah")
        o = self.ok("terkirim", "--kontak", "K0001")                          # ke-2 -> +4 hari
        self.assertEqual(o["kontak"]["followup"], "2026-09-28")
        self.assertEqual(self.ok("draf", "--kontak", "K0001")["jenis"], "pamit")
        o = self.ok("terkirim", "--kontak", "K0001")                          # ke-3 (pamit) -> stop
        self.assertIsNone(o["kontak"]["followup"])
        self.assertTrue(any("tidak ada respon" in p for p in o["peringatan"]))

    def test_irama_deal_dan_tawaran_ulang(self):
        self.ok("catat", "--kontak", "K0001", "--tahap", "deal", "--nilai", "500rb", "--followup", "besok")
        self.assertEqual(self.ok("draf", "--kontak", "K0001")["jenis"], "konfirmasi-order")
        for _ in range(4):                                                 # deal tidak pernah "pamit"/berhenti
            o = self.ok("terkirim", "--kontak", "K0001")
            self.assertEqual(o["kontak"]["followup"], "2026-09-26")
        self.assertEqual(self.ok("draf", "--kontak", "K0001")["jenis"], "pengingat-order")
        o = self.ok("catat", "--kontak", "K0001", "--tahap", "selesai")
        self.assertIsNone(o["kontak"]["followup"])
        self.assertEqual(self.ok("draf", "--kontak", "K0001")["jenis"], "terima-kasih")
        self.ok("terkirim", "--kontak", "K0001", "--berikutnya", "30 hari lagi")
        self.assertEqual(self.ok("draf", "--kontak", "K0001")["jenis"], "tawaran-ulang")
        out = self.ok("hari-ini", hari="2026-10-24")                       # tawaran ulang muncul di pengingat
        self.assertEqual(out["ringkasan"]["hari_ini"], 1)

    def test_draf_tidak_memuat_catatan_pribadi_atau_nilai(self):
        self.ok("catat", "--kontak", "K0001", "--isi", "RAHASIA pelit", "--tahap", "ditawar", "--nilai", "4,5 jt")
        d = self.ok("draf", "--kontak", "K0001")
        self.assertNotIn("RAHASIA", d["draf"])
        self.assertNotIn("4.500.000", d["draf"])
        self.assertEqual(d["jenis"], "follow-up-penawaran")

    def test_kelompok_hari_ini(self):
        self.ok("tambah", "--nama", "Pak Budi", "--wa", "081200001002", "--tahap", "ditawar", "--nilai", "4 jt",
                "--followup", "22/9/2026")
        self.ok("tambah", "--nama", "Mbak Dewi", "--wa", "081200001003", "--tahap", "dihubungi",
                "--followup", "besok")
        self.ok("tambah", "--nama", "Om Heru", "--wa", "081200001004", "--tahap", "dihubungi")
        self.ok("catat", "--kontak", "Om Heru", "--tanpa-followup")
        out = self.ok("hari-ini")
        r = out["ringkasan"]
        self.assertEqual((r["terlambat"], r["hari_ini"], r["besok"], r["belum_dijadwalkan"]), (1, 1, 1, 1))
        self.assertEqual(r["nilai_perlu_disapa"], 4000000)
        self.assertEqual([d["kode"] for d in out["draf"]], ["K0002", "K0001"])  # terlambat dulu
        self.assertIn("TERLAMBAT", out["teks"])
        s = self.ok("hari-ini", "--samarkan")
        self.assertNotIn("0812-0000-1002", s["teks"])
        self.assertNotIn("wa.me", s["teks"])
        self.assertNotIn("Budi", s["teks"])

    def test_mundur_dari_deal_menghapus_tanggal_deal(self):
        self.ok("catat", "--kontak", "K0001", "--tahap", "deal", "--nilai", "500rb")
        o = self.ok("catat", "--kontak", "K0001", "--tahap", "ditawar")
        self.assertIsNone(o["kontak"]["tgl_deal"])
        self.assertEqual(o["kontak"]["followup"], "2026-09-26")


class UjiRekap(Dasar):
    """Data September 2026 (hari ini 24 Sep):
      K1 Instagram masuk 01/09 -> deal 05/09 nilai 1.000.001   (4 hari)
      K2 Instagram masuk 02/09 -> selesai (deal 10/09) nilai 1.000.000   (8 hari)
      K3 Instagram masuk 03/09 -> batal (harga)          nilai 500.000
      K4 Referensi masuk 04/09 -> deal 06/09 nilai 2.000.001   (2 hari)
      K5 TikTok    masuk 20/09 -> ditawar nilai 3.000.000
      K6 TikTok    masuk 21/09 -> baru (tanpa nilai)
      K7 Walk-in   masuk 15/08 -> deal 02/09 nilai 700.000 (lead Agustus, deal September; 18 hari)
    Periode September:
      lead masuk = 6 (K1-K6); menang di kohort = K1,K2,K4 = 3 -> konversi 3/6 = 50,0%
      batal kohort = 1 -> win rate 3/4 = 75,0%
      deal baru (tgl_deal di Sep) = K1,K2,K4,K7 = 4; nilai = 1.000.001+1.000.000+2.000.001+700.000 = 4.700.002
      rata nilai = 4.700.002/4 = 1.175.000,5 -> 1.175.001; lama closing = (4+8+2+18)/4 = 8,0 hari
      sumber: Referensi nilai 2.000.001 (1 lead) > Instagram 2.000.001? -> Instagram 1.000.001+1.000.000 = 2.000.001
        seri nilai -> konversi Referensi 100% > Instagram 66,7% -> Referensi terbaik
      posisi: baru 1 (0), ditawar 1 (3.000.000), deal 3 (3.700.002), selesai 1 (1.000.000), batal 1
      pipeline terbuka = 2 kontak, 3.000.000
    """
    def setUp(self):
        super().setUp()
        tbh = [("K1", "0812-0000-2001", "ig", "1/9/2026", "1.000.001"),
               ("K2", "0812-0000-2002", "ig", "2/9/2026", "1.000.000"),
               ("K3", "0812-0000-2003", "ig", "3/9/2026", "500rb"),
               ("K4", "0812-0000-2004", "referensi", "4/9/2026", "2.000.001"),
               ("K5", "0812-0000-2005", "tiktok", "20/9/2026", "3 jt"),
               ("K6", "0812-0000-2006", "tiktok", "21/9/2026", None),
               ("K7", "0812-0000-2007", "walk-in", "15/8/2026", "700rb")]
        for nama, wa, sb, masuk, nilai in tbh:
            a = ["tambah", "--nama", "Pelanggan " + nama, "--wa", wa, "--sumber", sb, "--masuk", masuk]
            if nilai:
                a += ["--nilai", nilai]
            self.ok(*a)
        self.ok("catat", "--kontak", "K0001", "--tahap", "deal", "--tanggal", "5/9/2026")
        self.ok("catat", "--kontak", "K0002", "--tahap", "selesai", "--tanggal", "10/9/2026")
        self.ok("catat", "--kontak", "K0003", "--tahap", "batal", "--alasan", "mahal", "--tanggal", "12/9/2026")
        self.ok("catat", "--kontak", "K0004", "--tahap", "deal", "--tanggal", "6/9/2026")
        self.ok("catat", "--kontak", "K0005", "--tahap", "ditawar")
        self.ok("catat", "--kontak", "K0007", "--tahap", "deal", "--tanggal", "2/9/2026")

    def test_rumus_rekap_september(self):
        r = self.ok("rekap", "--bulan", "2026-09")
        self.assertEqual(r["skema_json"], 1)
        self.assertEqual(r["periode"], {"nama": "bulan September 2026", "dari": "2026-09-01", "sampai": "2026-09-30"})
        pi = r["periode_ini"]
        self.assertEqual(pi["lead_masuk"], 6)
        self.assertEqual(pi["kohort"], {"lead": 6, "deal_atau_selesai": 3, "batal": 1, "masih_berjalan": 2})
        self.assertEqual((pi["konversi_persen"], pi["konversi_teks"]), (50.0, "50,0%"))
        self.assertEqual((pi["win_rate_persen"], pi["win_rate_teks"]), (75.0, "75,0%"))
        self.assertEqual(pi["deal_baru"], {"jumlah": 4, "nilai": 4700002, "tanpa_nilai": 0, "rata_nilai": 1175001,
                                           "rata_hari_closing": 8.0})
        self.assertEqual(pi["batal"], 1)
        pos = r["posisi"]
        self.assertEqual(pos["deal"], {"jumlah": 3, "nilai": 3700002})
        self.assertEqual(pos["selesai"], {"jumlah": 1, "nilai": 1000000})
        self.assertEqual(pos["pipeline_terbuka"], {"jumlah": 2, "nilai": 3000000})
        self.assertEqual(pos["total_kontak"], 7)
        self.assertEqual(r["sumber_terbaik"]["sumber"], "Referensi")
        self.assertTrue(r["sumber_terbaik"]["sampel_kecil"])
        ig = [s for s in r["sumber"] if s["sumber"] == "Instagram"][0]
        self.assertEqual((ig["lead"], ig["deal"], ig["batal"], ig["nilai_deal"], ig["konversi_teks"]),
                         (3, 2, 1, 2000001, "66,7%"))
        self.assertEqual(r["alasan_batal"], [{"alasan": "harga terlalu mahal", "jumlah": 1}])
        self.assertIn("50,0%", r["teks"])
        self.assertIn("Rp 4.700.002", r["teks"])

    def test_periode_lain_dan_kontrak_json(self):
        r = self.ok("rekap", "--bulan", "2026-08")
        self.assertEqual(r["periode_ini"]["lead_masuk"], 1)             # K7
        self.assertEqual(r["periode_ini"]["deal_baru"]["jumlah"], 0)    # deal K7 di September
        self.assertEqual(r["periode_ini"]["konversi_persen"], 100.0)
        k = self.ok("rekap", "--tanggal", "2026-09-06")
        self.assertEqual(k["periode_ini"]["deal_baru"]["nilai"], 2000001)
        kosong = self.ok("rekap", "--dari", "2026-01-01", "--sampai", "2026-01-31")
        self.assertIsNone(kosong["periode_ini"]["konversi_persen"])
        self.assertIsNone(kosong["sumber_terbaik"])
        for kunci in ("posisi", "periode_ini", "sumber", "sumber_terbaik", "alasan_batal", "followup", "rumus", "teks",
                      "periode", "hari_ini", "zona"):
            self.assertIn(kunci, r)
        self.assertFalse(r["data_sensitif"])
        self.assertNotRegex(json.dumps(r), r"62812\d{7}")                # rekap tidak memuat nomor HP

    def test_rekap_tidak_mengubah_database(self):
        sebelum = self.sha(self.db)
        self.ok("rekap")
        self.ok("hari-ini")
        self.ok("daftar", "--tahap", "semua")
        self.assertEqual(sebelum, self.sha(self.db))


class UjiCSV(Dasar):
    def test_ekspor_aman_formula_injection_dan_impor_ulang(self):
        self.ok("tambah", "--nama", "=HYPERLINK(\"http://contoh.invalid\",\"klik\")", "--wa", "081200001001",
                "--kebutuhan", "+cmd|' /C calc'!A0", "--label", "@SUM(1)")
        self.ok("tambah", "--nama=-2+3", "--wa", "081200001002", "--nilai", "1 jt")  # nilai diawali "-": pakai --opsi=nilai
        p = os.path.join(self.dir, "ekspor.csv")
        self.ok("ekspor", "--csv", p)
        with open(p, encoding="utf-8-sig", newline="") as f:
            rows = list(csv.reader(f, delimiter=";"))
        for r in rows[1:]:
            for sel in r:
                if sel and not re.fullmatch(r"-?\d+(?:[.,]\d+)?", sel):
                    self.assertNotIn(sel[0], "=+-@\t\r", "sel berbahaya: %r" % sel)
        self.assertEqual(rows[1][1][0], "'")
        self.assertEqual(rows[2][7], "1000000")                          # angka tetap angka
        self.gagal("ekspor", "--csv", p)                                 # tidak menimpa diam-diam
        self.ok("ekspor", "--csv", p, "--timpa")
        db2 = os.path.join(self.dir, "b.db")
        self.ok("init", "--ya", db=db2)
        self.ok("impor", p, "--ya", db=db2)
        k = self.ok("lihat", "--kontak", "K0001", db=db2)
        self.assertEqual(k["kontak"]["nama"], "=HYPERLINK(\"http://contoh.invalid\",\"klik\")")  # tanda ' dibuang

    def test_impor_pratinjau_duplikat_dan_baris_rusak(self):
        self.ok("tambah", "--nama", "Bu Rina", "--wa", "081200001001")
        p = self.file("kontak.csv", "Nama;No HP;Sumber;Tahap;Nilai\n"
                                    "Mbak Dewi;0812-0000-1004;tiktok;baru;350rb\n"
                                    "Kak Sinta;+62 812 0000 1001;ig;;\n"
                                    "Dewi lagi;0812 0000 1004;ig;;\n"
                                    "Toko X;6.28120E+12;shopee;;\n"
                                    ";0812-0000-1007;ig;;\n"
                                    "Bu Lina;0812-0000-1008;pameran;ditawar;5m\n"
                                    "Pak Joko;0812-0000-1009;;tahap aneh;\n")
        pra = self.ok("impor", p)
        self.assertEqual(pra["mode"], "pratinjau")
        self.assertEqual(self.jumlah(), 1)                               # pratinjau tidak menyimpan
        self.assertEqual(len(pra["baru"]), 1)
        self.assertEqual(sorted(d["baris"] for d in pra["duplikat"]), [3, 4])
        self.assertEqual(sorted(d["baris"] for d in pra["rusak"]), [5, 6, 7, 8])
        out = self.ok("impor", p, "--ya")
        self.assertTrue(os.path.isfile(out["backup"]))
        self.assertEqual(self.jumlah(), 2)

    def test_impor_excel_ansi_pemisah_koma(self):
        p = self.file("ansi.csv", "name,phone,source\nJosé Café,081200001010,Google\n", encoding="cp1252")
        out = self.ok("impor", p, "--ya")
        self.assertEqual(len(out["baru"]), 1)
        self.assertTrue(any("Windows-1252" in x for x in out["peringatan"]))

    def test_impor_google_contacts(self):
        p = self.file("google.csv", "First Name,Middle Name,Last Name,Phone 1 - Label,Phone 1 - Value\n"
                                    "Rina,,Wati,Mobile,+62 812-0000-1011\n"
                                    "Budi,,,Mobile,0812 0000 1012\n")
        out = self.ok("impor", p, "--sumber-default", "referensi", "--ya")
        self.assertEqual([x["nama"] for x in out["baru"]], ["Rina Wati", "Budi"])
        self.assertEqual({x["sumber"] for x in out["baru"]}, {"Referensi"})

    def test_ekspor_pengingat_tanpa_nomor(self):
        self.ok("tambah", "--nama", "Bu Rina", "--wa", "081200001001", "--nilai", "450rb", "--kebutuhan", "kue")
        p = os.path.join(self.dir, "p.csv")
        out = self.ok("ekspor", "--csv", p, "--format", "pengingat")
        with open(p, encoding="utf-8-sig") as f:
            isi = f.read()
        self.assertNotIn("0812", isi)
        self.assertNotIn("62812", isi)
        self.assertEqual(out["perintah_pengingat"][0][:5], ["tambah", "--jenis", "prospek", "--nama", "Bu Rina"])


class UjiDatabase(Dasar):
    def test_db_rusak(self):
        p = self.file("rusak.db", "ini bukan database")
        g = self.gagal("hari-ini", db=p)
        self.assertTrue(g.get("rusak"))
        self.assertIn("restore", g["error"])
        with open(p) as f:
            self.assertEqual(f.read(), "ini bukan database")        # tidak ditimpa

    def test_db_milik_aplikasi_lain_tidak_disentuh(self):
        p = os.path.join(self.dir, "kasir.db")
        c = sqlite3.connect(p)
        c.execute("CREATE TABLE meta(kunci TEXT PRIMARY KEY, nilai TEXT)")
        c.execute("INSERT INTO meta VALUES ('aplikasi','kasir-lokal')")
        c.commit()
        c.close()
        h = self.sha(p)
        self.gagal("tambah", "--nama", "X", db=p)
        self.gagal("init", "--ya", db=p)
        self.assertEqual(h, self.sha(p))

    def test_db_belum_ada(self):
        g = self.gagal("hari-ini", db=os.path.join(self.dir, "tidak-ada.db"))
        self.assertTrue(g.get("belum_ada"))
        info = self.ok("info", db=os.path.join(self.dir, "tidak-ada.db"))
        self.assertFalse(info["ada"])

    def test_db_terkunci(self):
        os.environ["KOMUNITECH_CRM_TIMEOUT"] = "0.2"
        c = sqlite3.connect(self.db, isolation_level=None)
        try:
            c.execute("BEGIN EXCLUSIVE")
            for argv in (("hari-ini",), ("tambah", "--nama", "X"), ("rekap",)):
                g = self.gagal(*argv)
                self.assertIn("sedang dipakai", g["error"])
                self.assertIn("0,2 detik", g["error"])
            c.execute("ROLLBACK")
        finally:
            c.close()
            del os.environ["KOMUNITECH_CRM_TIMEOUT"]
        self.ok("tambah", "--nama", "X")

    def test_init_tidak_menimpa(self):
        self.gagal("init", "--ya")

    def test_hapus_perlu_ya_dan_backup_restore(self):
        self.ok("tambah", "--nama", "Bu Rina", "--wa", "081200001001")
        self.ok("hapus", "--kontak", "K0001")
        self.assertEqual(self.jumlah(), 1)
        out = self.ok("hapus", "--kontak", "K0001", "--ya")
        self.assertEqual(self.jumlah(), 0)
        self.ok("restore", "--dari", out["backup"], "--ya")
        self.assertEqual(self.jumlah(), 1)

    def test_backup_harian_otomatis(self):
        self.ok("tambah", "--nama", "A")
        self.ok("tambah", "--nama", "B")
        fol = os.path.join(self.dir, "backup-crm")
        self.assertEqual(len([f for f in os.listdir(fol) if "harian" in f]), 1)   # sekali sehari
        self.ok("tambah", "--nama", "C", hari="2026-09-25")
        self.assertEqual(len([f for f in os.listdir(fol) if "harian" in f]), 2)


class UjiKeamanan(unittest.TestCase):
    def test_script_tanpa_akses_jaringan(self):
        with open(os.path.join(AKAR, "scripts", "crm.py"), encoding="utf-8") as f:
            src = f.read()
        for terlarang in ("import socket", "urllib.request", "http.client", "import requests", "subprocess",
                          "smtplib", "webbrowser"):
            self.assertNotIn(terlarang, src)


if __name__ == "__main__":
    unittest.main(verbosity=1)
