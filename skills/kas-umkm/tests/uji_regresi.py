#!/usr/bin/env python3
"""Uji regresi kas-umkm. Jalankan: python3 tests/uji_regresi.py  (Windows: py tests/uji_regresi.py)

Hanya library standar. Semua data fiktif, dibuat di folder sementara yang dihapus setelah tes.
Angka diverifikasi dengan rumus manual di komentar tiap tes:
  saldo akun      = saldo awal + masuk - keluar (transaksi aktif s.d. akhir hari itu)
  hasil usaha     = masuk kelompok usaha - keluar kelompok usaha
                    (usaha = penjualan, beli-stok, gaji, listrik-air, sewa, pajak, lain-lain, selisih-kas;
                     BUKAN modal, pinjaman, prive, pindah dana)
  selisih laci    = uang fisik - saldo buku
  rata-rata       = total / jumlah minggu, dibulatkan ke rupiah terdekat (0,5 ke atas)
"""
import contextlib
import csv
import hashlib
import io
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from datetime import date

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AKAR, "scripts"))
import kas as K  # noqa: E402

SKILLS = os.path.dirname(AKAR)
HARI = "2026-09-26"   # Sabtu


def jalan(*argv, db, hari=HARI):
    argv = list(argv) + ["--db", db, "--json", "--hari-ini", hari]
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
        kode = K.main(argv)
    return kode, json.loads(buf.getvalue())


class Dasar(unittest.TestCase):
    """Buku kas fiktif: Laci kas 500rb, BRI 3jt (penampung QRIS), GoPay 150rb; semua mulai 01/09/2026."""

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.db = os.path.join(self.dir, "kas.db")
        self.ok("init", "--nama-usaha", "Warung Contoh", "--kas-awal", "500rb", "--mulai", "01/09/2026", "--ya")
        self.ok("akun", "tambah", "--nama", "BRI", "--jenis", "bank", "--saldo-awal", "3jt", "--tanggal-awal",
                "01/09/2026", "--terima-qris", "--ya")
        self.ok("akun", "tambah", "--nama", "GoPay", "--jenis", "e-wallet", "--saldo-awal", "150rb",
                "--tanggal-awal", "01/09/2026", "--ya")

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def run_cli(self, *argv, hari=HARI, db=None):
        return jalan(*argv, db=db or self.db, hari=hari)

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

    def saldo(self, tanggal=None):
        a = ["saldo"] + (["--tanggal", tanggal] if tanggal else [])
        return {r["akun"]: r["saldo"] for r in self.ok(*a)["saldo"]}

    def sha(self, p=None):
        with open(p or self.db, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()

    def file(self, nama, isi, encoding="utf-8"):
        p = os.path.join(self.dir, nama)
        with open(p, "w", encoding=encoding, newline="") as f:
            f.write(isi)
        return p


# --------------------------------------------------------------------------- angka & tanggal
class UjiNominal(unittest.TestCase):
    def test_nominal_ketik(self):
        kasus = {"25rb": 25000, "1,2 jt": 1200000, "1.250.000": 1250000, "Rp1.250.000": 1250000,
                 "Rp 1.250.000,-": 1250000, "1 jt 250 rb": 1250000, "750 ribu": 750000, "25000": 25000,
                 "2.5jt": 2500000, "1.250.000,00": 1250000, "4,275 jt": 4275000, "100k": 100000}
        for teks, harap in kasus.items():
            self.assertEqual(K.parse_nominal(teks), harap, teks)

    def test_nominal_ditolak(self):
        for teks in ("5m", "1.500 jt", "4,5", "-100rb", "(100rb)", "abc", "1,5 ekor", "0", "", "1.5E+06",
                     "12,50", "2 jt 500", "2000 miliar"):
            with self.assertRaises(K.Gagal, msg=teks):
                K.parse_nominal(teks)
        self.assertEqual(K.parse_nominal("0", boleh_nol=True), 0)

    def test_nominal_file_indonesia_inggris_bank(self):
        kasus = {"1.500.000": (1500000, False, None), "1,500,000.00": (1500000, False, None),
                 "1.500.000,00": (1500000, False, None), "750,000.00 CR": (750000, False, "CR"),
                 "12.500 DB": (12500, False, "DB"), "(200.000)": (-200000, False, None),
                 "-200000": (-200000, False, None), "1,234.56 CR": (1235, True, "CR"),
                 "1.234,50": (1235, True, None), "1.234,49": (1234, True, None), "Rp 25.000": (25000, False, None),
                 "25000": (25000, False, None)}
        for teks, harap in kasus.items():
            self.assertEqual(K.nominal_file(teks), harap, teks)
        self.assertIsNone(K.nominal_file(""))
        self.assertIsNone(K.nominal_file("0,00"))
        for rusak in ("1.5E+06", "12.34.5", "abc", "1,50,000", "Rp"):
            with self.assertRaises(ValueError, msg=rusak):
                K.nominal_file(rusak)


class UjiTanggal(unittest.TestCase):
    def setUp(self):
        K._JAM["kini"] = K.parse_hari_ini(HARI)

    def tearDown(self):
        K._JAM["kini"] = None

    def test_diterima(self):
        kasus = {"26/09/2026": date(2026, 9, 26), "1-9-2026": date(2026, 9, 1), "01.09.2026": date(2026, 9, 1),
                 "2026-09-01": date(2026, 9, 1), "hari ini": date(2026, 9, 26), "hari-ini": date(2026, 9, 26),
                 "kemarin": date(2026, 9, 25), "3 hari lalu": date(2026, 9, 23), "5 Sep 2026": date(2026, 9, 5),
                 "5 september 2026": date(2026, 9, 5), "Senin 21/09/2026": date(2026, 9, 21),
                 "tgl 21/09/2026": date(2026, 9, 21)}
        for teks, harap in kasus.items():
            self.assertEqual(K.baca_tanggal(teks), harap, teks)

    def test_ambigu_ditolak(self):
        pesan = {"26/09": "tahun", "26/09/26": "4 angka", "09/26/2026": "bulan/hari", "5 Sep": "tahun",
                 "31/02/2026": "kalender", "27/09/2026": "masa depan", "46000": "tidak dikenali",
                 "Jumat": "tidak dikenali", "01/01/1999": "sebelum tahun 2000", "": "kosong"}
        for teks, kata in pesan.items():
            with self.assertRaises(K.Gagal, msg=teks) as c:
                K.baca_tanggal(teks)
            self.assertIn(kata, c.exception.pesan, teks)

    def test_periode(self):
        a, b = K.baca_bulan("09/2026")
        self.assertEqual((a, b), (date(2026, 9, 1), date(2026, 9, 30)))
        self.assertEqual(K.baca_bulan("lalu"), (date(2026, 8, 1), date(2026, 8, 31)))
        self.assertEqual(K.baca_bulan("Februari 2028"), (date(2028, 2, 1), date(2028, 2, 29)))
        with self.assertRaises(K.Gagal):
            K.baca_bulan("september")
        with self.assertRaises(K.Gagal):
            K.baca_bulan("13/2026")

    def test_pecahan(self):
        # 100rb x5 + 50rb x3 + 2rb x10 + receh 3.500 = 500.000 + 150.000 + 20.000 + 3.500 = 673.500
        total, rinci, pr = K.urai_pecahan("100rb x5, 50rb x3, 2rb x10, koin 3.500")
        self.assertEqual(total, 673500)
        self.assertEqual(len(rinci), 4)
        self.assertEqual(pr, [])
        self.assertEqual(K.urai_pecahan("5x100rb; 3 lembar 50rb")[0], 650000)
        self.assertTrue(K.urai_pecahan("30rb x2")[2])        # pecahan tidak lazim -> peringatan
        with self.assertRaises(K.Gagal):
            K.urai_pecahan("banyak uang")


# --------------------------------------------------------------------------- pencatatan
class UjiCatat(Dasar):
    def test_pratinjau_tidak_mengubah_database(self):
        h = self.sha()
        out = self.ok("catat", "--masuk", "1,2jt", "--kategori", "penjualan", "--catatan", "jualan")
        self.assertEqual(out["mode"], "pratinjau")
        self.assertTrue(out["perlu_konfirmasi"])
        self.assertEqual(h, self.sha())
        self.assertEqual(self.saldo()["Laci kas"], 500000)

    def test_catat_dan_saldo_per_akun(self):
        self.ok("catat", "--masuk", "1,2jt", "--kategori", "penjualan", "--ya")                 # laci +1.200.000
        out = self.ok("catat", "--masuk", "350rb", "--kategori", "penjualan", "--metode", "qris", "--ya")
        self.assertEqual(out["entri"][0]["akun"], "BRI")                                          # penampung QRIS
        self.ok("catat", "--keluar", "200rb", "--kategori", "listrik-air", "--metode", "transfer", "--ya")
        self.ok("catat", "--masuk", "75rb", "--kategori", "penjualan", "--metode", "gopay", "--ya")
        s = self.saldo()
        self.assertEqual(s["Laci kas"], 500000 + 1200000)
        self.assertEqual(s["BRI"], 3000000 + 350000 - 200000)
        self.assertEqual(s["GoPay"], 150000 + 75000)

    def test_banyak_baris_dan_tebakan_kategori(self):
        out = self.ok("catat", "--baris", "masuk;1.150.000;penjualan;tunai;jualan", "--baris",
                      "keluar;600rb;;tunai;kulakan ke agen", "--baris", "keluar;100rb;;;jajan anak", "--ya")
        kat = [e["kategori"] for e in out["entri"]]
        self.assertEqual(kat, ["penjualan", "beli-stok", "prive"])
        self.assertTrue(any("ditebak" in a for a in out["asumsi"]))
        self.assertEqual(self.saldo()["Laci kas"], 500000 + 1150000 - 600000 - 100000)

    def test_kategori_tidak_jelas_ditanyakan(self):
        out = self.gagal("catat", "--keluar", "25rb", "--catatan", "gas elpiji")
        self.assertTrue(out.get("perlu_kategori"))
        self.gagal("catat", "--keluar", "25rb", "--kategori", "sedekah")

    def test_arah_kategori_salah_ditolak(self):
        self.assertIn("prive", self.gagal("catat", "--keluar", "1jt", "--kategori", "modal")["error"])
        self.assertIn("modal", self.gagal("catat", "--masuk", "1jt", "--kategori", "prive")["error"])
        self.gagal("catat", "--masuk", "1jt", "--kategori", "gaji")

    def test_peringatan_keperluan_pribadi(self):
        out = self.ok("catat", "--keluar", "250rb", "--kategori", "lain-lain", "--catatan", "bayar SPP anak")
        self.assertTrue(any("prive" in p for p in out["peringatan"]))

    def test_duplikat_perlu_izin(self):
        self.ok("catat", "--keluar", "50rb", "--kategori", "beli-stok", "--catatan", "es batu", "--ya")
        out = self.ok("catat", "--keluar", "50rb", "--kategori", "beli-stok", "--catatan", "es batu")
        self.assertIn("--izinkan-duplikat", out["perlu_izin"])
        h = self.sha()
        g = self.gagal("catat", "--keluar", "50rb", "--kategori", "beli-stok", "--catatan", "es batu", "--ya")
        self.assertIn("BELUM DISIMPAN", g["error"])
        self.assertEqual(h, self.sha())
        self.ok("catat", "--keluar", "50rb", "--kategori", "beli-stok", "--izinkan-duplikat", "--ya")
        self.assertEqual(self.saldo()["Laci kas"], 400000)

    def test_saldo_minus_tidak_diterima_diam_diam(self):
        out = self.ok("catat", "--keluar", "600rb", "--kategori", "beli-stok")       # 500rb - 600rb = -100rb
        self.assertIn("--izinkan-minus", out["perlu_izin"])
        self.assertIn("MINUS", out["teks"])
        self.gagal("catat", "--keluar", "600rb", "--kategori", "beli-stok", "--ya")
        self.assertEqual(self.saldo()["Laci kas"], 500000)
        self.ok("catat", "--keluar", "600rb", "--kategori", "beli-stok", "--izinkan-minus", "--ya")
        self.assertEqual(self.saldo()["Laci kas"], -100000)
        rek = self.ok("rekap", "--tanggal", "hari-ini")
        self.assertTrue(rek["saldo_minus"])
        self.assertIn("SALDO MINUS", rek["teks"])

    def test_catatan_mundur_yang_membuat_hari_berikutnya_minus(self):
        # 20/09: keluar 400rb (saldo 100rb). Lalu catat mundur 10/09 keluar 300rb -> 20/09 jadi -200rb.
        self.ok("catat", "--keluar", "400rb", "--kategori", "sewa", "--tanggal", "20/09/2026", "--ya")
        out = self.ok("catat", "--keluar", "300rb", "--kategori", "beli-stok", "--tanggal", "10/09/2026")
        self.assertIn("--izinkan-minus", out["perlu_izin"])
        self.assertIn("20/09/2026", out["teks"])

    def test_akun_ambigu_dan_tanggal_sebelum_saldo_awal(self):
        self.ok("akun", "tambah", "--nama", "BCA", "--jenis", "bank", "--ya")
        self.assertTrue(self.gagal("catat", "--keluar", "50rb", "--kategori", "sewa", "--metode", "transfer")
                        .get("perlu_akun"))
        self.ok("catat", "--keluar", "50rb", "--kategori", "sewa", "--akun", "BRI", "--ya")
        e = self.gagal("catat", "--keluar", "50rb", "--kategori", "sewa", "--akun", "BCA", "--tanggal", "20/09/2026")
        self.assertIn("lebih awal dari saldo awal", e["error"])

    def test_tanggal_masa_depan_ditolak(self):
        self.assertIn("masa depan", self.gagal("catat", "--masuk", "1jt", "--kategori", "penjualan",
                                                "--tanggal", "27/09/2026")["error"])

    def test_pindah_dana_tidak_mengubah_hasil_usaha(self):
        self.ok("catat", "--masuk", "2jt", "--kategori", "penjualan", "--ya")
        sebelum = self.ok("rekap", "--tanggal", "hari-ini")["hasil_usaha"]
        out = self.ok("pindah", "--dari", "laci", "--ke", "BRI", "--jumlah", "1,5jt", "--ya")
        s = self.saldo()
        self.assertEqual(s["Laci kas"], 500000 + 2000000 - 1500000)
        self.assertEqual(s["BRI"], 3000000 + 1500000)
        rek = self.ok("rekap", "--tanggal", "hari-ini")
        self.assertEqual(rek["hasil_usaha"], sebelum)
        self.assertEqual(rek["masuk"], 2000000)
        self.assertEqual(len(rek["pindah"]), 1)
        # batal satu sisi -> kedua sisi batal
        self.ok("batal", "--id", str(out["id"][0]), "--alasan", "salah akun", "--ya")
        self.assertEqual(self.saldo()["BRI"], 3000000)

    def test_pindah_dengan_biaya_admin(self):
        self.ok("pindah", "--dari", "BRI", "--ke", "GoPay", "--jumlah", "100rb", "--biaya", "1.000", "--ya")
        s = self.saldo()
        self.assertEqual(s["BRI"], 3000000 - 100000 - 1000)
        self.assertEqual(s["GoPay"], 250000)
        self.assertEqual(self.ok("rekap", "--tanggal", "hari-ini")["hasil_usaha"], -1000)

    def test_pindah_ke_akun_sama_dan_minus(self):
        self.gagal("pindah", "--dari", "laci", "--ke", "laci", "--jumlah", "1rb")
        self.assertIn("--izinkan-minus", self.ok("pindah", "--dari", "laci", "--ke", "BRI", "--jumlah", "1jt")
                      ["perlu_izin"])

    def test_batal_wajib_alasan_dan_tidak_dihapus(self):
        out = self.ok("catat", "--masuk", "300rb", "--kategori", "penjualan", "--ya")
        i = out["entri"][0]["id"]
        self.gagal("batal", "--id", "#%d" % i, "--alasan", " ")
        self.ok("batal", "--id", "#%d" % i, "--alasan", "salah ketik", "--ya")
        self.gagal("batal", "--id", str(i), "--alasan", "lagi", "--ya")
        self.assertEqual(self.saldo()["Laci kas"], 500000)
        semua = self.ok("daftar", "--semua")["transaksi"]
        self.assertEqual(semua[0]["status"], "batal")
        self.assertEqual(self.ok("daftar")["jumlah"], 0)
        self.gagal("batal", "--id", "999", "--alasan", "x")


class UjiOpname(Dasar):
    def test_pas_kurang_lebih_dan_sesuaikan(self):
        self.ok("catat", "--masuk", "845rb", "--kategori", "penjualan", "--ya")            # buku 1.345.000
        self.assertEqual(self.ok("opname", "--fisik", "1.345.000")["status"], "pas")
        out = self.ok("opname", "--fisik", "1.340.000", "--ya")                            # kurang 5.000
        self.assertEqual((out["saldo_buku"], out["selisih"], out["status"], out["ditandai"]),
                         (1345000, -5000, "kurang", True))
        self.assertEqual(self.saldo()["Laci kas"], 1345000)                                 # tidak disesuaikan
        out = self.ok("opname", "--fisik", "1.340.000", "--sesuaikan", "--ya")
        self.assertTrue(out["disesuaikan"])
        self.assertEqual(self.saldo()["Laci kas"], 1340000)
        rek = self.ok("rekap", "--tanggal", "hari-ini")
        self.assertEqual(rek["per_kategori"]["selisih-kas"]["keluar"], 5000)
        self.assertEqual(rek["hasil_usaha"], 845000 - 5000)
        out = self.ok("opname", "--fisik", "1.350.000")
        self.assertEqual((out["selisih"], out["status"]), (10000, "lebih"))
        self.assertIn("penjualan tunai belum dicatat", out["teks"])
        riwayat = self.ok("opname", "--daftar")["opname"]
        self.assertEqual([r["ditandai"] for r in riwayat], [True, True])

    def test_pecahan_dan_input_salah(self):
        # 100rb x3 + 50rb x4 = 500.000 = saldo laci
        self.assertEqual(self.ok("opname", "--pecahan", "100rb x3, 50rb x4")["status"], "pas")
        self.gagal("opname")
        self.gagal("opname", "--fisik", "1jt", "--pecahan", "100rb x1")
        self.gagal("opname", "--fisik=-5rb")
        self.ok("akun", "tambah", "--nama", "Brankas", "--jenis", "tunai", "--ya")
        self.gagal("opname", "--fisik", "1jt")                                              # 2 akun tunai
        self.ok("opname", "--akun", "brankas", "--fisik", "0")


class UjiRekap(Dasar):
    def isi_minggu(self):
        # Minggu 14-20/09/2026 (Senin-Minggu), semua fiktif.
        b = [("14/09/2026", "masuk;1jt;penjualan;tunai;jualan"), ("14/09/2026", "keluar;1,3jt;beli-stok;tunai;kulakan"),
             ("15/09/2026", "masuk;800rb;penjualan;qris;jualan qris"), ("16/09/2026", "masuk;2jt;modal;tunai;tambah modal"),
             ("17/09/2026", "keluar;500rb;gaji;tunai;gaji Andi"), ("18/09/2026", "keluar;300rb;prive;tunai;belanja rumah"),
             ("19/09/2026", "keluar;1,5jt;sewa;transfer;sewa kios"), ("20/09/2026", "masuk;1jt;pinjaman;transfer;KUR cair"),
             ("20/09/2026", "keluar;200rb;pajak;transfer;PPh final Agustus")]
        for tgl, baris in b:
            self.ok("catat", "--baris", baris, "--tanggal", tgl, "--izinkan-minus", "--ya")

    def test_rekap_mingguan_angka_manual(self):
        self.isi_minggu()
        r = self.ok("rekap", "--minggu", "14/09/2026")
        # masuk = 1.000.000 + 800.000 + 2.000.000 + 1.000.000 = 4.800.000
        # keluar = 1.300.000 + 500.000 + 300.000 + 1.500.000 + 200.000 = 3.800.000
        # hasil usaha = (1.000.000 + 800.000) - (1.300.000 + 500.000 + 1.500.000 + 200.000) = -1.700.000
        self.assertEqual((r["masuk"], r["keluar"], r["hasil_usaha"]), (4800000, 3800000, -1700000))
        self.assertEqual((r["prive"], r["modal"], r["pinjaman_masuk"]), (300000, 2000000, 1000000))
        # saldo awal 14/09 = 3.650.000; akhir = 3.650.000 + 4.800.000 - 3.800.000 = 4.650.000
        self.assertEqual((r["total_saldo_awal"], r["total_saldo_akhir"]), (3650000, 4650000))
        self.assertTrue(r["cek_saldo_cocok"])
        self.assertIn("Per hari:", r["teks"])
        self.assertTrue(any("PERINGATAN PRIVE" in p for p in r["peringatan"]))    # hasil usaha minus, ada prive

    def test_rekap_bulanan_dan_harian(self):
        self.isi_minggu()
        self.ok("catat", "--masuk", "3jt", "--kategori", "penjualan", "--ya")
        r = self.ok("rekap", "--bulan", "09/2026")
        # hasil usaha = -1.700.000 + 3.000.000 = 1.300.000 ; prive 300.000 < hasil -> tidak ada peringatan prive
        self.assertEqual(r["hasil_usaha"], 1300000)
        self.assertFalse(any("PRIVE" in p for p in r["peringatan"]))
        self.assertIn("Per minggu:", r["teks"])
        self.assertIn("Pengeluaran terbesar:", r["teks"])
        self.assertEqual(r["pengeluaran_terbesar"][0]["jumlah"], 1500000)
        h = self.ok("rekap", "--tanggal", "15/09/2026")
        self.assertEqual((h["masuk"], h["per_metode"]["qris"]["masuk"]), (800000, 800000))
        self.assertEqual(self.ok("rekap", "--bulan", "08/2026")["teks"].count("Belum ada catatan"), 1)

    def test_peringatan_prive_melebihi_hasil_dan_batas(self):
        self.ok("atur", "--batas-prive", "500rb", "--ya")
        self.ok("catat", "--baris", "masuk;1jt;penjualan", "--baris", "keluar;400rb;beli-stok",
                "--baris", "keluar;800rb;prive;;ambil pribadi", "--izinkan-minus", "--ya")
        r = self.ok("rekap", "--bulan", "ini")
        # hasil usaha 600.000; prive 800.000 > hasil -> kelebihan 200.000; 800.000 > batas 500.000
        teks = "\n".join(r["peringatan"])
        self.assertIn("Kelebihan Rp 200.000", teks)
        self.assertIn("batas prive", teks)
        self.assertIn("133,3%", teks)                   # 800.000 / 600.000 = 133,33% -> 133,3%
        c = self.ok("catat", "--keluar", "50rb", "--kategori", "prive")
        self.assertTrue(any("PERINGATAN PRIVE" in p for p in c["peringatan"]))
        self.ok("atur", "--batas-prive", "hapus", "--ya")
        self.assertFalse(any("batas prive" in p for p in self.ok("rekap", "--bulan", "ini")["peringatan"]))

    def test_saran_hitung_laci(self):
        self.assertTrue(any("belum dihitung" in p for p in self.ok("rekap")["peringatan"]))
        self.ok("opname", "--fisik", "500rb", "--ya")
        self.assertFalse(any("belum dihitung" in p for p in self.ok("rekap")["peringatan"]))

    def test_teks_siap_telegram(self):
        self.isi_minggu()
        t = self.ok("rekap", "--minggu", "14/09/2026")["teks"]
        self.assertIn("BUKU KAS Warung Contoh", t)
        self.assertIn("HASIL USAHA", t)
        self.assertIn("Rp 4.650.000", t)


# --------------------------------------------------------------------------- impor
class UjiImpor(Dasar):
    def test_impor_buku_kas_dan_tidak_dobel(self):
        f = self.file("kas.csv", "Tanggal;Keterangan;Masuk;Keluar;Kategori;Metode\n"
                                 "14/09/2026;Jualan tunai;765.000;;penjualan;tunai\n"
                                 "14/09/2026;Jualan QRIS;177.000;;;qris\n"
                                 "15/09/2026;Kulakan ke agen;;1.500.000;;tunai\n"
                                 "15/09/2026;Sumbangan 17an;;50.000;;tunai\n"
                                 "16/09/2026;TOTAL;942.000;1.550.000;;\n")
        h = self.sha()
        out = self.ok("impor", f)
        self.assertEqual(h, self.sha())
        self.assertEqual(out["jumlah_baru"], 4)
        # v1.0.1: baris belum jelas disimpan sebagai 'perlu-dicek' (bukan lain-lain) sampai digolongkan
        self.assertEqual([b["kategori"] for b in out["baris"]], ["penjualan", "penjualan", "beli-stok", "perlu-dicek"])
        self.assertEqual(len(out["perlu_dicek"]), 1)                 # 'Sumbangan 17an' belum jelas
        self.assertIn("--izinkan-minus", out["perlu_izin"])          # laci 500rb + 765rb - 1,55jt < 0
        self.ok("impor", f, "--tetapkan", "5=lain-lain", "--izinkan-minus", "--ya")
        self.assertEqual(self.saldo()["BRI"], 3177000)
        ulang = self.ok("impor", f)
        self.assertEqual(ulang["jumlah_baru"], 0)                    # impor ulang dilewati
        self.assertEqual(len(ulang["sudah_diimpor"]), 4)
        self.assertEqual(ulang["perlu_dicek"], [])                   # yang sudah diimpor tidak ditanyakan lagi

    def test_mutasi_bank_cr_db_tanpa_tahun_pend(self):
        f = self.file("mutasi.csv", "Mutasi Rekening (fiktif)\nNo. rekening : 0000\n"
                                    "Tanggal Transaksi,Keterangan,Cabang,Jumlah,Saldo\n"
                                    "21/09,TRSF CR PESANAN BU RINA,0998,\"750,000.00 CR\",\"3,750,000.00\"\n"
                                    "22/09,TARIKAN ATM 22/09,0998,\"500,000.00 DB\",\"3,250,000.00\"\n"
                                    "23/09,BIAYA ADM,0000,\"12,500.00 DB\",\"3,237,500.00\"\n"
                                    "25/09,BUNGA,0000,\"1,234.56 CR\",\"3,238,735.00\"\n"
                                    "PEND,TRSF MASUK,0000,\"100,000.00 CR\",\n")
        out = self.ok("impor", f, "--akun", "BRI")
        self.assertEqual(out["jumlah_baru"], 0)
        self.assertEqual(len(out["bermasalah"]), 4)                  # tanpa tahun
        out = self.ok("impor", f, "--akun", "BRI", "--tahun", "2026")
        self.assertEqual(out["jumlah_baru"], 4)
        # v1.0.1: tarikan ATM dikenali otomatis sebagai pindah dana ke satu-satunya akun tunai (bukan beban)
        self.assertEqual(out["perlu_dicek"], [])
        self.assertEqual([(c["baris"], c["pasangan"]) for c in out["pindah_dikenali"]], [(5, "Laci kas")])
        self.assertEqual(out["baris"][1]["kategori"], "pindah")
        self.assertEqual([b["jumlah"] for b in out["baris"]], [750000, 500000, 12500, 1235])   # 1.234,56 -> 1.235
        self.assertTrue(any("dibulatkan" in p for p in out["peringatan"]))
        self.assertEqual(len(out["dilewati"]), 1)                    # PEND
        self.ok("impor", f, "--akun", "BRI", "--tahun", "2026", "--tetapkan", "5=pindah:laci", "--ya")
        s = self.saldo()
        # BRI = 3.000.000 + 750.000 - 500.000 - 12.500 + 1.235 = 3.238.735 (sama dengan kolom saldo bank)
        self.assertEqual(s["BRI"], 3238735)
        self.assertEqual(s["Laci kas"], 1000000)                     # tarik tunai masuk laci
        self.assertEqual(self.ok("rekap", "--tanggal", "22/09/2026")["hasil_usaha"], 0)

    def test_debit_kredit_wajib_jenis_file(self):
        f = self.file("dk.csv", "Tanggal,Keterangan,Debit,Kredit\n21/09/2026,Transfer pelanggan,,250000\n"
                                "22/09/2026,Bayar listrik PLN,200000,\n")
        self.assertTrue(self.gagal("impor", f, "--akun", "BRI").get("perlu_jenis_file"))
        bank = self.ok("impor", f, "--akun", "BRI", "--jenis-file", "mutasi-bank")["baris"]
        self.assertEqual([b["arah"] for b in bank], ["masuk", "keluar"])
        kas = self.ok("impor", f, "--akun", "BRI", "--jenis-file", "buku-kas", "--izinkan-minus")["baris"]
        self.assertEqual([b["arah"] for b in kas], ["keluar", "masuk"])

    def test_jumlah_plus_jenis(self):
        f = self.file("j.csv", "tanggal,uraian,jumlah,jenis\n21/09/2026,jualan,300000,masuk\n"
                               "21/09/2026,beli bahan,-100000,\n21/09/2026,sewa,100000,DB\n21/09/2026,x,5000,entah\n")
        out = self.ok("impor", f, "--akun", "laci")
        self.assertEqual([(b["arah"], b["jumlah"]) for b in out["baris"]],
                         [("masuk", 300000), ("keluar", 100000), ("keluar", 100000)])
        self.assertEqual(out["bermasalah"][0]["baris"], 5)

    def test_urutan_tanggal(self):
        amb = self.file("amb.csv", "Tanggal;Keterangan;Masuk;Keluar\n01/09/2026;jualan;100000;\n02/09/2026;jualan;"
                                   "100000;\n")
        self.assertTrue(self.gagal("impor", amb, "--akun", "laci").get("perlu_format_tanggal"))
        out = self.ok("impor", amb, "--akun", "laci", "--format-tanggal", "hari-bulan")
        self.assertEqual(out["baris"][1]["tanggal"], "2026-09-02")
        us = self.file("us.csv", "Tanggal;Keterangan;Masuk;Keluar\n09/15/2026;jualan;100000;\n09/02/2026;jualan;"
                                 "100000;\n")
        self.assertIn("bulan-hari", self.gagal("impor", us, "--akun", "laci")["error"])
        out = self.ok("impor", us, "--akun", "laci", "--format-tanggal", "bulan-hari")
        self.assertEqual([b["tanggal"] for b in out["baris"]], ["2026-09-15", "2026-09-02"])
        campur = self.file("c.csv", "Tanggal;Keterangan;Masuk;Keluar\n15/09/2026;a;1000;\n09/16/2026;b;1000;\n")
        self.assertIn("tidak konsisten", self.gagal("impor", campur, "--akun", "laci")["error"])

    def test_data_rusak(self):
        f = self.file("rusak.csv", "Tanggal;Keterangan;Masuk;Keluar\n"
                                   "15/09/2026;angka ilmiah;1,5E+06;\n"
                                   "16/09/26;tahun dua angka;100000;\n"
                                   "17/09/2026;dua kolom;100000;50000\n"
                                   "18/09/2026;kosong;;\n"
                                   "31/09/2026;tanggal mustahil;1000;\n"
                                   "46000;serial excel;1000;\n"
                                   "20/09/2026;masuk minus;-5000;\n"
                                   "21/09/2026;terlalu kecil;1,5;\n"
                                   "30/09/2026;masa depan;1000;\n"
                                   "19/09/2026;jualan;150.000;\n")
        out = self.ok("impor", f, "--akun", "laci")
        self.assertEqual(out["jumlah_baru"], 1)
        self.assertEqual(len(out["bermasalah"]), 9)
        alasan = " ".join(b["alasan"] for b in out["bermasalah"])
        for kata in ("ilmiah", "tahun 2 angka", "sama-sama terisi", "nominal kosong", "kalender", "seri",
                     "minus", "terlalu kecil", "masa depan"):
            self.assertIn(kata, alasan)
        semua_rusak = self.file("sr.csv", "Tanggal;Keterangan;Masuk\n15/09/2026;x;abc\n")
        self.assertIn("Tidak ada baris", self.gagal("impor", semua_rusak, "--akun", "laci")["error"])

    def test_file_tidak_didukung(self):
        self.assertIn("tidak ditemukan", self.gagal("impor", os.path.join(self.dir, "tidakada.csv"))["error"])
        x = self.file("a.xlsx", "x")
        self.assertIn("Save As", self.gagal("impor", x)["error"])
        kosong = self.file("kosong.csv", "  \n")
        self.assertIn("kosong", self.gagal("impor", kosong)["error"])
        biner = os.path.join(self.dir, "b.csv")
        with open(biner, "wb") as fh:
            fh.write(b"\x00\x01\x02SQLite\x00" * 50)
        self.assertIn("biner", self.gagal("impor", biner)["error"])
        tanpa_judul = self.file("tj.csv", "a;b;c\n1;2;3\n")
        self.assertIn("Judul kolom", self.gagal("impor", tanpa_judul)["error"])

    def test_cp1252_utf16_dan_akun_wajib(self):
        f = self.file("w.csv", "Tanggal;Keterangan;Masuk;Keluar\n19/09/2026;Jualan café;150.000;\n",
                      encoding="cp1252")
        out = self.ok("impor", f, "--akun", "laci")
        self.assertTrue(any("Windows-1252" in p for p in out["peringatan"]))
        f16 = self.file("u16.csv", "Tanggal;Keterangan;Masuk;Keluar\n19/09/2026;Jualan;150.000;\n", encoding="utf-16")
        self.assertEqual(self.ok("impor", f16, "--akun", "laci")["jumlah_baru"], 1)
        self.assertTrue(self.gagal("impor", f16).get("perlu_akun"))

    def test_mirip_catatan_manual_dilewati(self):
        self.ok("catat", "--masuk", "750rb", "--kategori", "penjualan", "--akun", "BRI", "--tanggal", "21/09/2026",
                "--ya")
        f = self.file("m.csv", "Tanggal;Keterangan;Masuk;Keluar\n21/09/2026;TRSF CR PESANAN;750.000;\n")
        out = self.ok("impor", f, "--akun", "BRI")
        self.assertEqual((out["jumlah_baru"], len(out["mirip_manual"])), (0, 1))
        self.assertEqual(self.ok("impor", f, "--akun", "BRI", "--sertakan-mirip")["jumlah_baru"], 1)

    def test_tetapkan_salah(self):
        f = self.file("t.csv", "Tanggal;Keterangan;Masuk;Keluar\n21/09/2026;x;;1000\n")
        self.gagal("impor", f, "--akun", "laci", "--tetapkan", "2")
        self.gagal("impor", f, "--akun", "laci", "--tetapkan", "2=sedekah")
        self.gagal("impor", f, "--akun", "laci", "--tetapkan", "2=pindah")
        self.gagal("impor", f, "--akun", "laci", "--tetapkan", "2=pindah:laci")
        self.assertEqual(self.ok("impor", f, "--akun", "laci", "--tetapkan", "2=lewati")["jumlah_baru"], 0)


class UjiImporKasir(Dasar):
    def rekap_kasir(self, nama="rk.json", per_metode=None, total=None, dari="2026-09-25", sampai=None, pajak=0,
                    encoding="utf-8"):
        per_metode = per_metode if per_metode is not None else {"Tunai": 24000, "QRIS": 15000}
        d = {"ok": True, "mode": "baca", "periode": {"dari": dari, "sampai": sampai or dari, "jenis": "hari"},
             "total_diterima": sum(per_metode.values()) if total is None else total, "pajak": pajak,
             "per_metode": per_metode, "teks": "REKAP KASIR"}
        return self.file(nama, json.dumps(d), encoding=encoding)

    def test_impor_per_metode_ke_akun(self):
        f = self.rekap_kasir()
        out = self.ok("impor-kasir", f, "--ya")
        self.assertEqual([(e["akun"], e["jumlah"]) for e in out["entri"]], [("Laci kas", 24000), ("BRI", 15000)])
        s = self.saldo()
        self.assertEqual((s["Laci kas"], s["BRI"]), (524000, 3015000))
        self.assertTrue(self.gagal("impor-kasir", f).get("sudah_diimpor"))
        f2 = self.rekap_kasir("rk2.json", {"Tunai": 30000, "QRIS": 15000})
        out = self.ok("impor-kasir", f2, "--ganti", "--ya")
        self.assertEqual(len(out["diganti"]), 2)
        self.assertEqual(self.saldo()["Laci kas"], 530000)
        self.assertEqual(self.ok("rekap", "--tanggal", "25/09/2026")["masuk"], 45000)

    def test_penjualan_manual_tanggal_sama_perlu_izin(self):
        self.ok("catat", "--masuk", "900rb", "--kategori", "penjualan", "--tanggal", "25/09/2026", "--ya")
        f = self.rekap_kasir()
        out = self.ok("impor-kasir", f)
        self.assertIn("--izinkan-duplikat", out["perlu_izin"])
        self.assertIn("DOBEL", out["teks"])
        self.gagal("impor-kasir", f, "--ya")
        self.ok("impor-kasir", f, "--izinkan-duplikat", "--ya")
        self.assertEqual(self.saldo()["Laci kas"], 500000 + 900000 + 24000)

    def test_metode_lain_refund_pajak_dan_selisih(self):
        f = self.rekap_kasir(per_metode={"Tunai": -10000, "Lainnya": 5000, "E-wallet": 20000, "Debit": 50000},
                             total=70000, pajak=6000)
        out = self.ok("impor-kasir", f, "--akun-untuk", "kartu=BRI")
        self.assertEqual([(e["arah"], e["metode"], e["akun"]) for e in out["entri"]],
                         [("keluar", "tunai", "Laci kas"), ("masuk", "e-wallet", "GoPay"), ("masuk", "kartu", "BRI")])
        teks = " ".join(out["peringatan"])
        self.assertIn("Lainnya", teks)
        self.assertIn("PPN/PBJT Rp 6.000", teks)
        self.assertIn("berbeda", teks)                               # 65.000 per metode vs total 70.000

    def test_rekap_kasir_tidak_valid(self):
        self.assertIn("per HARI", self.gagal("impor-kasir", self.rekap_kasir(dari="2026-09-01", sampai="2026-09-25"))
                      ["error"])
        self.assertIn("masa depan", self.gagal("impor-kasir", self.rekap_kasir(dari="2026-09-30"))["error"])
        self.assertIn("bukan hasil", self.gagal("impor-kasir", self.file("x.json", '{"ok": true}'))["error"])
        self.assertIn("bukan JSON", self.gagal("impor-kasir", self.file("y.json", "REKAP KASIR"))["error"])
        self.assertIn("tidak dikenal", self.gagal("impor-kasir", self.rekap_kasir(per_metode={"Emas": 1000}))["error"])
        self.gagal("impor-kasir", self.rekap_kasir(per_metode={"Tunai": "24rb"}, total=24000))
        self.assertIn("tidak berisi", self.gagal("impor-kasir", self.rekap_kasir(per_metode={}))["error"])
        self.ok("impor-kasir", self.rekap_kasir("u16.json", encoding="utf-16"))     # PowerShell: > file = UTF-16

    def test_file_asli_kasir_lokal(self):
        kasir = os.path.join(SKILLS, "kasir-lokal", "scripts", "kasir.py")
        if not os.path.isfile(kasir):
            self.skipTest("skill kasir-lokal tidak ada di sebelah skill ini")
        kdb = os.path.join(self.dir, "kasir.db")
        env = dict(os.environ, KOMUNITECH_KASIR_DB=kdb)

        def k(*a):
            r = subprocess.run([sys.executable, kasir] + list(a), capture_output=True, text=True, env=env)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            return r.stdout
        k("init", "--nama-toko", "Warung Uji", "--ya")
        k("produk", "tambah", "--kode", "KH", "--nama", "Kopi Hitam", "--harga", "12000", "--satuan", "cup", "--ya")
        k("jual", "--pesan", "2 kopi hitam, bayar tunai 50rb", "--ya")
        k("jual", "--pesan", "1 kopi hitam, bayar qris", "--ya")
        f = self.file("asli.json", k("rekap", "--tanggal", "hari-ini", "--json"))
        with open(f, encoding="utf-8") as fh:
            tgl = json.load(fh)["periode"]["dari"]
        out = self.ok("impor-kasir", f, hari=tgl)
        self.assertEqual(sorted((e["metode"], e["jumlah"]) for e in out["entri"]), [("qris", 12000), ("tunai", 24000)])


# --------------------------------------------------------------------------- ekspor
class UjiEkspor(Dasar):
    def isi(self):
        self.ok("catat", "--baris", "masuk;1jt;penjualan;tunai;jualan", "--baris", "keluar;400rb;beli-stok;tunai;kulakan",
                "--baris", "keluar;100rb;prive;tunai;jajan anak", "--baris", "masuk;2jt;modal;transfer;tambah modal",
                "--baris", "keluar;150rb;pajak;transfer;setor bulanan", "--baris", "keluar;50rb;lain-lain;tunai;=SUM(A1)",
                "--tanggal", "15/09/2026", "--ya")
        self.ok("pindah", "--dari", "BRI", "--ke", "laci", "--jumlah", "500rb", "--tanggal", "16/09/2026", "--ya")

    def baca(self, path):
        with open(path, encoding="utf-8-sig", newline="") as f:
            return list(csv.reader(f, delimiter=";"))

    def test_emkm(self):
        self.isi()
        out = self.ok("ekspor", "--format", "emkm", "--bulan", "09/2026", "--csv", os.path.join(self.dir, "e.csv"))
        rows = self.baca(out["file"])
        self.assertEqual(rows[0], ["Tanggal", "Keterangan", "Masuk", "Keluar", "Kategori"])
        self.assertEqual(rows[1], ["01/09/2026", "Saldo awal", "3650000", "", ""])
        kat = [r[4] for r in rows[2:]]
        self.assertEqual(kat, ["pendapatan_usaha", "pembelian_bahan", "prive", "setoran_modal", "", ""])
        self.assertEqual(rows[6][1], "Pajak: setor bulanan")
        self.assertEqual(rows[7][1], "'=SUM(A1)")                     # anti formula injection
        self.assertEqual(len(rows), 8)                               # pindah dana tidak ditulis
        # saldo akhir = 3.650.000 + 1.000.000 + 2.000.000 - 400.000 - 100.000 - 150.000 - 50.000 = 5.950.000
        self.assertEqual(out["saldo_akhir"], 5950000)
        emkm = os.path.join(SKILLS, "laporan-keuangan-emkm", "scripts", "laporan_emkm.py")
        if os.path.isfile(emkm):
            r = subprocess.run([sys.executable, emkm, out["file"], "--format", "json", "--periode-awal", "2026-09-01",
                                "--periode-akhir", "2026-09-26", "--kas-akhir-aktual", str(out["saldo_akhir"])],
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            d = json.loads(r.stdout)
            # hasil usaha kas-umkm = 1.000.000 - 400.000 - 150.000 - 50.000 = 400.000 = laba emkm (tanpa stok akhir)
            self.assertEqual(self.ok("rekap", "--bulan", "09/2026")["hasil_usaha"], 400000)
            self.assertEqual(d["laba_rugi"]["laba_bersih"], 400000)

    def test_arus_kas(self):
        # 3 minggu penuh 31/08-20/09 tidak mungkin (mulai 01/09); data 07/09-20/09 = 2 minggu penuh
        for tgl in ("07/09/2026", "10/09/2026", "14/09/2026", "17/09/2026"):
            self.ok("catat", "--baris", "masuk;1jt;penjualan;tunai;jualan", "--baris", "keluar;301rb;beli-stok;tunai;"
                    "kulakan", "--tanggal", tgl, "--ya")
        self.ok("catat", "--keluar", "1,5jt", "--kategori", "sewa", "--metode", "transfer", "--tanggal", "01/09/2026",
                "--ya")
        self.ok("catat", "--masuk", "2jt", "--kategori", "modal", "--tanggal", "08/09/2026", "--ya")
        out = self.ok("ekspor", "--format", "arus-kas", "--csv", os.path.join(self.dir, "r.csv"))
        b = {r["kategori"]: r for r in out["baris"]}
        # penjualan: 4.000.000 / 2 minggu = 2.000.000 ; stok: 1.204.000 / 2 = 602.000
        self.assertEqual(b["Penjualan (rata-rata riwayat)"]["nominal"], 2000000)
        self.assertEqual(b["Beli stok (bahan/supplier)"]["nominal"], 602000)
        self.assertEqual((b["Sewa tempat"]["minggu"], b["Sewa tempat"]["nominal"], b["Sewa tempat"]["kritis"]),
                         ("tgl:1", 1500000, "ya"))
        self.assertNotIn("Modal pemilik", b)
        self.assertEqual(out["mulai"], "2026-09-28")
        rows = self.baca(out["file"])
        self.assertEqual(rows[0], ["minggu", "jenis", "kategori", "nominal", "keterangan", "kritis"])
        proyeksi = os.path.join(SKILLS, "arus-kas-13minggu", "scripts", "proyeksi_kas.py")
        if os.path.isfile(proyeksi):
            r = subprocess.run([sys.executable, proyeksi, out["file"], "--saldo-awal", str(out["saldo_awal"]),
                                "--mulai", out["mulai"]], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("minggu", r.stdout.lower())

    def test_arus_kas_riwayat_kurang(self):
        self.ok("catat", "--masuk", "1jt", "--kategori", "penjualan", "--ya")
        self.assertIn("minimal 2 minggu", self.gagal("ekspor", "--format", "arus-kas")["error"])

    def test_lengkap_dengan_batal(self):
        self.isi()
        self.ok("batal", "--id", "1", "--alasan", "uji", "--izinkan-minus", "--ya")
        p = os.path.join(self.dir, "l.csv")
        self.assertEqual(self.ok("ekspor", "--csv", p)["baris"], 7)
        self.assertEqual(self.ok("ekspor", "--csv", p, "--semua")["baris"], 8)
        self.assertEqual(self.baca(p)[1][10], "batal")


# --------------------------------------------------------------------------- database: rusak, restore, kunci
class UjiDatabase(Dasar):
    def test_init_ulang_ditolak_dan_nama_wajib(self):
        self.assertIn("sudah ada", self.gagal("init", "--nama-usaha", "X", "--ya")["error"])
        db2 = os.path.join(self.dir, "baru", "kas.db")
        self.gagal("init", db=db2)
        self.ok("init", "--nama-usaha", "Y", db=db2)
        self.assertFalse(os.path.exists(db2))                        # pratinjau tidak membuat file

    def test_backup_harian_dan_restore(self):
        self.ok("catat", "--masuk", "1jt", "--kategori", "penjualan", "--ya")
        daftar = self.ok("backup", "--daftar")["backup"]
        self.assertTrue(daftar)                                      # cadangan harian otomatis
        manual = self.ok("backup", "--label", "sebelum uji")["backup"]
        self.ok("catat", "--masuk", "2jt", "--kategori", "penjualan", "--ya")
        self.assertEqual(self.saldo()["Laci kas"], 3500000)
        pr = self.ok("restore", "--dari", manual)
        self.assertEqual(pr["mode"], "pratinjau")
        self.assertEqual(self.saldo()["Laci kas"], 3500000)
        self.ok("restore", "--dari", manual, "--ya")
        self.assertEqual(self.saldo()["Laci kas"], 1500000)
        self.gagal("restore", "--dari", self.db)
        self.gagal("restore", "--dari", os.path.join(self.dir, "tidakada.db"))

    def test_database_rusak_dipulihkan(self):
        self.ok("catat", "--masuk", "1jt", "--kategori", "penjualan", "--ya")
        cadangan = self.ok("backup")["backup"]
        with open(self.db, "wb") as f:
            f.write(b"ini bukan database" * 100)
        e = self.gagal("rekap")
        self.assertTrue(e.get("rusak"))
        self.assertIn("restore", e["error"])
        self.assertEqual(self.ok("restore", "--dari", cadangan)["status_db"], "rusak")
        out = self.ok("restore", "--dari", cadangan, "--ya")
        self.assertIn("rusak-kas-", out["backup"])
        self.assertTrue(os.path.exists(out["backup"]))               # file rusak dipindah, tidak dihapus
        self.assertEqual(self.saldo()["Laci kas"], 1500000)

    def test_database_kosong_dan_mulai_baru(self):
        open(self.db, "wb").close()
        self.assertTrue(self.gagal("info").get("rusak"))
        self.assertTrue(self.gagal("rekap").get("rusak"))
        self.assertIn("--mulai-baru", self.gagal("init", "--nama-usaha", "Z", "--ya")["error"])
        self.ok("init", "--nama-usaha", "Z", "--mulai-baru", "--ya")
        self.assertEqual(self.saldo(), {"Laci kas": 0})
        self.assertTrue([p for p in os.listdir(os.path.join(self.dir, "backup-kas")) if p.startswith("rusak-kas-")])

    def test_cadangan_rusak_ditolak(self):
        buruk = self.file("buruk.db", "bukan db")
        self.assertIn("tidak bisa dipakai", self.gagal("restore", "--dari", buruk)["error"])

    def test_bukan_database_kas(self):
        lain = os.path.join(self.dir, "lain.db")
        c = sqlite3.connect(lain)
        c.execute("CREATE TABLE meta(kunci TEXT, nilai TEXT)")
        c.execute("INSERT INTO meta VALUES ('aplikasi','crm-wa')")
        c.commit()
        c.close()
        h = self.sha(lain)
        self.assertIn("bukan buku kas", self.gagal("rekap", db=lain)["error"])
        self.assertIn("tidak ditimpa", self.gagal("init", "--nama-usaha", "X", "--ya", db=lain)["error"])
        self.assertEqual(h, self.sha(lain))

    def test_database_terkunci(self):
        os.environ["KOMUNITECH_KAS_TIMEOUT"] = "0.2"
        c = sqlite3.connect(self.db, isolation_level=None)
        try:
            c.execute("BEGIN EXCLUSIVE")
            e = self.gagal("catat", "--masuk", "1jt", "--kategori", "penjualan", "--ya")
            self.assertIn("sedang dipakai", e["error"])
        finally:
            c.execute("ROLLBACK")
            c.close()
            del os.environ["KOMUNITECH_KAS_TIMEOUT"]
        self.ok("catat", "--masuk", "1jt", "--kategori", "penjualan", "--ya")

    def test_info_akun_atur(self):
        i = self.ok("info")
        self.assertEqual([a["nama"] for a in i["akun"]], ["Laci kas", "BRI", "GoPay"])
        self.assertIn("penampung QRIS", i["teks"])
        self.gagal("akun", "tambah", "--nama", "bri", "--jenis", "bank")
        self.gagal("akun", "tambah", "--nama", "Laci 2", "--jenis", "tunai", "--terima-qris")
        self.gagal("akun", "tambah", "--nama", "X", "--jenis", "emas")
        self.ok("akun", "tambah", "--nama", "BCA", "--jenis", "bank", "--terima-qris", "--ya")
        self.assertEqual([a["nama"] for a in self.ok("info")["akun"] if a["terima_qris"]], ["BCA"])
        self.ok("catat", "--keluar", "100rb", "--kategori", "sewa", "--akun", "GoPay", "--tanggal", "05/09/2026", "--ya")
        self.assertIn("transaksi akun GoPay", self.gagal("akun", "ubah", "--akun", "GoPay", "--tanggal-awal",
                                                         "10/09/2026")["error"])
        self.assertIn("--izinkan-minus", self.ok("akun", "ubah", "--akun", "GoPay", "--saldo-awal", "50rb")["perlu_izin"])
        self.ok("atur", "--zona", "WITA", "--nama-usaha", "Warung Baru", "--ya")
        self.assertEqual(self.ok("info")["pengaturan"]["zona"], "WITA")
        self.gagal("atur", "--zona", "GMT")
        self.gagal("atur")

    def test_perintah_salah_kode_2(self):
        buf = io.StringIO()
        with contextlib.redirect_stderr(buf), self.assertRaises(SystemExit) as c:
            K.main(["catat", "--tidak-ada"])
        self.assertEqual(c.exception.code, 2)


class UjiPlatform(unittest.TestCase):
    def test_tanpa_modul_luar_dan_jaringan(self):
        with open(os.path.join(AKAR, "scripts", "kas.py"), encoding="utf-8") as f:
            isi = f.read()
        for terlarang in ("import requests", "urllib.request", "import socket", "http.client", "subprocess"):
            self.assertNotIn(terlarang, isi)

    def test_frontmatter_hanya_name_description(self):
        with open(os.path.join(AKAR, "SKILL.md"), encoding="utf-8") as f:
            teks = f.read()
        fm = teks.split("---")[1].strip().splitlines()
        self.assertEqual([b.split(":")[0] for b in fm], ["name", "description"])


# --------------------------------------------------------------------------- v1.0.1: temuan penguji Akun B
class UjiV101(Dasar):
    MUTASI = ("Tanggal,Keterangan,Jumlah\n"
              "21/09/2026,TRSF CR PESANAN BU RINA,\"750,000.00 CR\"\n"
              "22/09/2026,TARIK TUNAI ATM 22/09,\"500,000.00 DB\"\n"
              "23/09/2026,SETOR TUNAI CRM,\"300,000.00 CR\"\n"
              "23/09/2026,TOPUP GOPAY 0812xxxx,\"100,000.00 DB\"\n"
              "24/09/2026,PINDAH BUKU KE REK SENDIRI,\"200,000.00 DB\"\n"
              "24/09/2026,TRSF DB SUMBANGAN MASJID,\"50,000.00 DB\"\n"
              "25/09/2026,BIAYA TARIK TUNAI ATM BERSAMA,\"7,500.00 DB\"\n")

    def test_impor_tarik_setor_topup_jadi_pindah_dana(self):
        f = self.file("mutasi.csv", self.MUTASI)
        out = self.ok("impor", f, "--akun", "BRI")
        kat = {b["baris"]: b["kategori"] for b in out["baris"]}
        self.assertEqual(kat, {2: "penjualan", 3: "pindah", 4: "pindah", 5: "pindah", 6: "perlu-dicek",
                               7: "perlu-dicek", 8: "lain-lain"})
        pasangan = {c["baris"]: (c["pola"], c["pasangan"]) for c in out["pindah_dikenali"]}
        self.assertEqual(pasangan, {3: ("tarik tunai", "Laci kas"), 4: ("setor tunai", "Laci kas"),
                                    5: ("antar rekening sendiri", "GoPay")})
        self.assertEqual(sorted(c["baris"] for c in out["perlu_dicek"]), [6, 7])   # pindah buku tanpa nama akun; sumbangan
        self.assertIn("DIKENALI SEBAGAI PINDAH DANA", out["teks"])
        self.ok("impor", f, "--akun", "BRI", "--ya")
        s = self.saldo()
        self.assertEqual(s["BRI"], 3000000 + 750000 - 500000 + 300000 - 100000 - 200000 - 50000 - 7500)
        self.assertEqual(s["Laci kas"], 500000 + 500000 - 300000)
        self.assertEqual(s["GoPay"], 150000 + 100000)
        r = self.ok("rekap", "--bulan", "09/2026")
        # hasil usaha hanya penjualan 750rb - biaya 7,5rb; tarik/setor/top up/perlu dicek TIDAK ikut
        self.assertEqual(r["hasil_usaha"], 742500)
        self.assertEqual(r["perlu_dicek"]["keluar"], 250000)
        self.assertTrue(any("BELUM DIGOLONGKAN" in p for p in r["peringatan"]))
        # ekspor emkm ditolak sampai digolongkan
        e = self.gagal("ekspor", "--format", "emkm", "--bulan", "09/2026")
        self.assertEqual(len(e["perlu_dicek"]), 2)
        ids = e["perlu_dicek"]
        # golongkan: pindah buku ke GoPay, sumbangan = lain-lain
        self.ok("golongkan", "--id", str(ids[0]), "--kategori", "pindah:GoPay", "--ya")
        self.ok("golongkan", "--id", "#%d" % ids[1], "--kategori", "lain-lain", "--ya")
        s = self.saldo()
        self.assertEqual(s["GoPay"], 150000 + 100000 + 200000)
        r = self.ok("rekap", "--bulan", "09/2026")
        self.assertEqual(r["hasil_usaha"], 742500 - 50000)
        self.assertEqual(r["perlu_dicek"]["id"], [])
        self.ok("ekspor", "--format", "emkm", "--bulan", "09/2026", "--csv", os.path.join(self.dir, "e.csv"))
        # catatan yang sudah pindah tidak bisa digolongkan ulang
        self.gagal("golongkan", "--id", str(ids[0]), "--kategori", "prive", "--ya")

    def test_tetapkan_mengalahkan_aturan_pindah(self):
        f = self.file("mutasi.csv", self.MUTASI)
        out = self.ok("impor", f, "--akun", "BRI", "--tetapkan", "3=prive", "--tetapkan", "6=pindah:GoPay")
        kat = {b["baris"]: b["kategori"] for b in out["baris"]}
        self.assertEqual((kat[3], kat[6]), ("prive", "pindah"))

    def test_tarik_tunai_akun_tunai_ganda_perlu_dicek(self):
        self.ok("akun", "tambah", "--nama", "Brankas", "--jenis", "tunai", "--saldo-awal", "0", "--tanggal-awal",
                "01/09/2026", "--ya")
        f = self.file("m.csv", "Tanggal,Keterangan,Jumlah\n22/09/2026,TARIK TUNAI ATM,\"500,000.00 DB\"\n"
                               "23/09/2026,TARIK TUNAI ATM KE BRANKAS,\"400,000.00 DB\"\n")
        out = self.ok("impor", f, "--akun", "BRI")
        self.assertEqual([b["kategori"] for b in out["baris"]], ["perlu-dicek", "pindah"])
        self.assertEqual(out["pindah_dikenali"][0]["pasangan"], "Brankas")

    def test_tanpa_kategori_default_tidak_masuk_laba_rugi(self):
        f = self.file("kas.csv", "Tanggal;Keterangan;Masuk;Keluar\n20/09/2026;Jualan tunai;500.000;\n"
                                 "21/09/2026;Titipan Pak RT;;100.000\n")
        self.ok("impor", f, "--akun", "laci", "--ya")
        r = self.ok("rekap", "--bulan", "09/2026")
        self.assertEqual(r["hasil_usaha"], 500000)                   # titipan belum jelas tidak jadi beban
        self.assertEqual(self.saldo()["Laci kas"], 900000)           # tapi saldo laci tetap benar
        # --kategori-default = pilihan eksplisit pengguna
        f2 = self.file("kas2.csv", "Tanggal;Keterangan;Masuk;Keluar\n22/09/2026;Titipan Bu RW;;40.000\n")
        self.ok("impor", f2, "--akun", "laci", "--kategori-default", "lain-lain", "--ya")
        self.assertEqual(self.ok("rekap", "--bulan", "09/2026")["hasil_usaha"], 460000)
        self.assertEqual(len(self.ok("daftar", "--bulan", "09/2026", "--kategori", "perlu dicek")["transaksi"]), 1)

    def test_catat_manual_tarik_tunai_diarahkan_ke_pindah(self):
        out = self.gagal("catat", "--keluar", "500rb", "--catatan", "tarik tunai ATM BRI", "--akun", "BRI")
        self.assertTrue(out.get("mungkin_pindah"))
        self.assertIn("kas.py pindah", out["error"])
        out = self.ok("catat", "--keluar", "500rb", "--kategori", "lain-lain", "--catatan", "setor tunai ke BRI")
        self.assertTrue(any("pindah dana" in p for p in out["peringatan"]))

    def test_skill_md_menolak_pembukuan_ganda(self):
        with open(os.path.join(AKAR, "SKILL.md"), encoding="utf-8") as f:
            isi = f.read()
        self.assertIn("pembukuan ganda", isi.lower())
        self.assertIn("UU KUP", isi)


# --------------------------------------------------------------------------- v1.0.2: temuan uji ulang v1.0.1 (Akun B)
class UjiV102(Dasar):
    """Data uji ulang Akun B: Laci 1.000.000, BRI 5.000.000, GoPay 100.000; mutasi BRI 9 baris (saldo akhir 9.042.500)."""
    MUTASI = ("Tanggal,Keterangan,Debet,Kredit\n"
              "02/09/2026,TRSF QRIS SETTLEMENT MERCHANT,,1250000\n"
              "03/09/2026,TARIK TUNAI ATM BRI JL MERDEKA,500000,\n"
              "03/09/2026,BIAYA TARIK TUNAI ATM BERSAMA,7500,\n"
              "04/09/2026,SETOR TUNAI CRM,,2000000\n"
              "05/09/2026,TOPUP GOPAY 0812XXXX,300000,\n"
              "06/09/2026,PINDAH BUKU KE REK 0987654,1000000,\n"
              "07/09/2026,SUMBANGAN 17AN RT 05,150000,\n"
              "08/09/2026,TRSF DR BUDI SANTOSO FIKTIF,,3000000\n"
              "09/09/2026,PEMBAYARAN PLN PRABAYAR,250000,\n")

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.db = os.path.join(self.dir, "kas.db")
        self.ok("init", "--nama-usaha", "Warung Uji Fiktif", "--kas-awal", "1jt", "--mulai", "01/09/2026", "--ya")
        self.ok("akun", "tambah", "--nama", "BRI", "--jenis", "bank", "--saldo-awal", "5jt", "--tanggal-awal",
                "01/09/2026", "--terima-qris", "--ya")
        self.ok("akun", "tambah", "--nama", "GoPay", "--jenis", "e-wallet", "--saldo-awal", "100rb",
                "--tanggal-awal", "01/09/2026", "--ya")
        self.ok("catat", "--keluar", "400rb", "--kategori", "beli-stok", "--metode", "tunai", "--catatan", "kulakan",
                "--tanggal", "02/09/2026", "--ya")
        self.ok("catat", "--masuk", "1,5jt", "--kategori", "penjualan", "--metode", "tunai", "--catatan", "jualan",
                "--tanggal", "03/09/2026", "--ya")
        f = self.file("mutasi-bri.csv", self.MUTASI)
        self.ok("impor", f, "--akun", "BRI", "--jenis-file", "mutasi-bank", "--format-tanggal", "hari-bulan", "--ya")

    def golongkan_semua(self):
        ids = self.ok("rekap", "--bulan", "09/2026")["perlu_dicek"]["id"]
        self.assertEqual(len(ids), 3)                                # pindah buku, sumbangan, trsf Budi
        for i, kat in zip(ids, ("prive", "lain-lain", "penjualan")):
            self.ok("golongkan", "--id", str(i), "--kategori", kat, "--ya")

    def test_biaya_tarik_tunai_jadi_beban_bank_dan_laba_emkm_sama(self):
        from decimal import Decimal as D
        self.golongkan_semua()
        s = self.saldo()
        # verifikasi Decimal independen dari data input
        laci = D(1000000) - D(400000) + D(1500000) + D(500000) - D(2000000)
        bri = D(5000000) + D(1250000) + D(2000000) + D(3000000) - (D(500000) + D(7500) + D(300000) + D(1000000) +
                                                                     D(150000) + D(250000))
        gopay = D(100000) + D(300000)
        self.assertEqual((D(s["Laci kas"]), D(s["BRI"]), D(s["GoPay"])), (laci, bri, gopay))
        self.assertEqual((laci, bri, gopay), (D(600000), D(9042500), D(400000)))
        hasil = (D(1500000) + D(1250000) + D(3000000)) - (D(400000) + D(7500) + D(150000) + D(250000))
        self.assertEqual(hasil, D(4942500))
        self.assertEqual(D(self.ok("rekap", "--bulan", "09/2026")["hasil_usaha"]), hasil)
        out = self.ok("ekspor", "--format", "emkm", "--bulan", "09/2026", "--csv", os.path.join(self.dir, "e.csv"))
        with open(out["file"], encoding="utf-8-sig", newline="") as fh:
            rows = list(csv.reader(fh, delimiter=";"))
        kode = {r[1]: r[4] for r in rows[1:]}
        self.assertEqual(kode["BIAYA TARIK TUNAI ATM BERSAMA"], "beban_keuangan")   # beban bank, bukan pindah dana
        self.assertEqual(D(out["saldo_akhir"]), laci + bri + gopay)
        emkm = os.path.join(SKILLS, "laporan-keuangan-emkm", "scripts", "laporan_emkm.py")
        if not os.path.isfile(emkm):
            self.skipTest("laporan-keuangan-emkm tidak ada di sebelah skill ini")
        r = subprocess.run([sys.executable, emkm, out["file"], "--format", "json", "--periode-awal", "2026-09-01",
                            "--periode-akhir", "2026-09-26", "--kas-akhir-aktual", str(out["saldo_akhir"])],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        d = json.loads(r.stdout)
        self.assertEqual(D(str(d["laba_rugi"]["laba_bersih"])), hasil)            # dulu 4.950.000 (selisih 7.500)
        self.assertEqual(D(str(d["laba_rugi"]["beban_keuangan"])), D(7500))
        neraca = d["posisi_keuangan"]
        self.assertTrue(neraca["seimbang"], neraca)
        self.assertEqual(D(str(neraca["selisih"])), D(0))

    def test_kode_emkm_lain_lain(self):
        k = K.kode_emkm
        for ket in ("BIAYA TARIK TUNAI ATM BERSAMA", "BIAYA ADM", "BIAYA TRANSFER BI FAST", "Biaya adm bank"):
            self.assertEqual(k("lain-lain", "keluar", ket, "bank"), "beban_keuangan", ket)
            self.assertEqual(k("lain-lain", "keluar", ket, "tunai"), "beban_keuangan", ket)
        self.assertEqual(k("lain-lain", "keluar", "BIAYA ADMIN", "bank"), "beban_keuangan")
        self.assertEqual(k("lain-lain", "keluar", "biaya admin shopee", "bank"), "")   # biarkan emkm (admin marketplace)
        self.assertEqual(k("lain-lain", "keluar", "PINDAH BUKU KE REK 0987654", "bank"), "beban_lain")
        self.assertEqual(k("lain-lain", "keluar", "fotokopi", "tunai"), "")
        self.assertEqual(k("lain-lain", "masuk", "BUNGA", "bank"), "pendapatan_lain")
        self.assertEqual(k("penjualan", "masuk", "qris", "bank"), "pendapatan_usaha")
        self.assertEqual(k("pajak", "keluar", "Pajak: setor", "bank"), "")

    def test_per_minggu_menandai_perlu_dicek(self):
        r = self.ok("rekap", "--bulan", "09/2026")
        baris = [b for b in r["teks"].splitlines() if b.startswith("07/09-13/09")]
        self.assertEqual(len(baris), 1, r["teks"])
        # 07/09-13/09: masuk 3.000.000 (Perlu dicek), keluar 150.000 (Perlu dicek) + 250.000 PLN; hasil usaha -250.000
        self.assertIn("masuk Rp 3.000.000, keluar Rp 400.000, hasil usaha -Rp 250.000", baris[0])
        self.assertIn("[termasuk 'Perlu dicek' masuk Rp 3.000.000, keluar Rp 150.000 - belum dihitung di hasil usaha]",
                      baris[0])
        self.golongkan_semua()
        r = self.ok("rekap", "--bulan", "09/2026")
        self.assertNotIn("termasuk 'Perlu dicek'", r["teks"])


class UjiV103(Dasar):
    """Sisa rendah H9: lain-lain 'utang/cicilan', 'uang muka karyawan/kasbon', 'belanja rumah' bukan biaya usaha."""
    # v1.0.4: utang pemasok = belanja (lain-lain, ekspor bayar_utang_usaha), bukan pinjaman
    LAIN = (("150rb", "bayar utang toko Pak Joko", "lain-lain"), ("100rb", "belanja rumah", "prive"),
            ("60rb", "beli kursi plastik", "lain-lain"), ("80rb", "uang muka karyawan Andi", "kasbon"),
            ("80rb", "cicilan etalase", "pinjaman"), ("5rb", "bunga cicilan etalase", "lain-lain"))

    def kategori_db(self):
        con = sqlite3.connect(self.db)
        try:
            return {c: k for c, k in con.execute("SELECT catatan, kategori FROM transaksi WHERE status='aktif'")}
        finally:
            con.close()

    def isi_data(self):
        self.ok("catat", "--masuk", "2jt", "--kategori", "penjualan", "--metode", "tunai", "--catatan", "jualan",
                "--tanggal", "02/09/2026", "--ya")
        self.ok("catat", "--keluar", "700rb", "--kategori", "beli-stok", "--metode", "tunai", "--catatan", "kulakan",
                "--tanggal", "03/09/2026", "--ya")
        for jml, cat, harap in self.LAIN:
            out = self.ok("catat", "--keluar", jml, "--kategori", "lain-lain", "--metode", "tunai", "--catatan", cat,
                          "--tanggal", "05/09/2026", "--ya")
            if harap != "lain-lain":
                self.assertTrue(any("diubah dari lain-lain ke %s" % harap in p for p in out["peringatan"]), out)
        out = self.ok("catat", "--masuk", "30rb", "--kategori", "lain-lain", "--metode", "tunai", "--catatan",
                      "Andi kembalikan kasbon", "--tanggal", "10/09/2026", "--ya")
        self.assertTrue(any("kasbon" in p for p in out["peringatan"]))

    def test_lain_lain_digolongkan_benar_dan_laba_emkm_sama(self):
        from decimal import Decimal as D
        self.isi_data()
        kat = self.kategori_db()
        for _, cat, harap in self.LAIN:
            self.assertEqual(kat[cat], harap, cat)
        self.assertEqual(kat["Andi kembalikan kasbon"], "kasbon")
        # verifikasi Decimal independen: hasil usaha hanya penjualan - stok - kursi - bunga
        hasil = D(2000000) - D(700000) - D(150000) - D(60000) - D(5000)
        r = self.ok("rekap", "--bulan", "09/2026")
        self.assertEqual(D(r["hasil_usaha"]), hasil)
        self.assertIn("kasbon karyawan", r["teks"])
        laci = D(500000) + D(2000000) - D(700000) - sum(D(K.parse_nominal(j)) for j, _, _ in self.LAIN) + D(30000)
        self.assertEqual(D(self.saldo()["Laci kas"]), laci)
        out = self.ok("ekspor", "--format", "emkm", "--bulan", "09/2026", "--csv", os.path.join(self.dir, "e.csv"))
        with open(out["file"], encoding="utf-8-sig", newline="") as fh:
            kode = {r[1]: r[4] for r in list(csv.reader(fh, delimiter=";"))[1:]}
        self.assertEqual(kode["bayar utang toko Pak Joko"], "bayar_utang_usaha")
        self.assertEqual(kode["cicilan etalase"], "bayar_pinjaman")
        self.assertEqual(kode["belanja rumah"], "prive")
        self.assertEqual(kode["uang muka karyawan Andi"], "piutang_lain")
        self.assertEqual(kode["Andi kembalikan kasbon"], "piutang_lain")
        self.assertTrue(any("--utang-bank-awal" in p and "Rp 80.000" in p for p in out["peringatan"]), out)
        emkm = os.path.join(SKILLS, "laporan-keuangan-emkm", "scripts", "laporan_emkm.py")
        if not os.path.isfile(emkm):
            self.skipTest("laporan-keuangan-emkm tidak ada di sebelah skill ini")
        r = subprocess.run([sys.executable, emkm, out["file"], "--format", "json", "--periode-awal", "2026-09-01",
                            "--periode-akhir", "2026-09-26", "--kas-akhir-aktual", str(out["saldo_akhir"]),
                            "--utang-bank-awal", "80000"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        d = json.loads(r.stdout)
        self.assertEqual(D(str(d["laba_rugi"]["laba_bersih"])), hasil)            # dulu bergeser 410.000
        neraca = d["posisi_keuangan"]
        self.assertTrue(neraca["seimbang"], neraca)
        self.assertEqual(D(str(neraca["selisih"])), D(0))

    def test_tebakan_tanpa_kategori(self):
        for n, (cat, harap) in enumerate((("uang muka karyawan Budi", "kasbon"), ("kasbon Siti", "kasbon"),
                                          ("bayar hutang ke Bu Rini", "pinjaman"), ("bunga cicilan motor", "lain-lain"),
                                          ("gaji karyawan", "gaji")), 1):
            out = self.ok("catat", "--keluar", str(50000 + n), "--metode", "tunai", "--catatan", cat, "--tanggal",
                          "05/09/2026", "--ya")
            self.assertEqual(self.kategori_db()[cat], harap, (cat, out))

    def test_koreksi_lain_lain_unit(self):
        k = K.koreksi_lain_lain
        self.assertEqual(k("lain-lain", "keluar", "biaya admin cicilan")[0], "lain-lain")   # biaya, bukan pokok
        self.assertEqual(k("lain-lain", "keluar", "denda angsuran")[0], "lain-lain")
        self.assertEqual(k("lain-lain", "masuk", "pinjaman dari saudara")[0], "pinjaman")
        self.assertEqual(k("lain-lain", "keluar", "beli kurir box")[0], "lain-lain")        # 'kur' kata utuh
        self.assertEqual(k("lain-lain", "keluar", "bayar piutang")[0], "lain-lain")         # 'utang' kata utuh
        self.assertEqual(k("beli-stok", "keluar", "belanja rumah"), ("beli-stok", None))    # hanya lain-lain

    def test_catatan_lama_dan_golongkan_impor(self):
        # catatan lama (sebelum v1.0.3) yang tersimpan sebagai lain-lain: tetap beban_lain + saran golongkan
        self.ok("catat", "--masuk", "1jt", "--kategori", "penjualan", "--metode", "tunai", "--catatan", "jualan",
                "--tanggal", "02/09/2026", "--ya")
        self.ok("catat", "--keluar", "40rb", "--kategori", "lain-lain", "--metode", "tunai", "--catatan", "fotokopi",
                "--tanggal", "03/09/2026", "--ya")
        con = sqlite3.connect(self.db)
        con.execute("UPDATE transaksi SET catatan='cicilan etalase' WHERE catatan='fotokopi'")
        con.commit()
        (i,) = con.execute("SELECT id FROM transaksi WHERE catatan='cicilan etalase'").fetchone()
        con.close()
        out = self.ok("ekspor", "--format", "emkm", "--bulan", "09/2026", "--csv", os.path.join(self.dir, "e.csv"))
        with open(out["file"], encoding="utf-8-sig", newline="") as fh:
            kode = {r[1]: r[4] for r in list(csv.reader(fh, delimiter=";"))[1:]}
        self.assertEqual(kode["cicilan etalase"], "beban_lain")
        self.assertTrue(any("golongkan --id %d --kategori pinjaman" % i in p for p in out["peringatan"]), out)
        self.ok("golongkan", "--id", str(i), "--kategori", "pinjaman", "--ya")
        self.assertEqual(self.ok("rekap", "--bulan", "09/2026")["hasil_usaha"], 1000000)
        # impor: --tetapkan N=lain-lain dan golongkan lain-lain ikut dikoreksi
        f = self.file("m.csv", "Tanggal,Keterangan,Debet,Kredit\n"
                               "04/09/2026,TRSF KASBON KARYAWAN DEDI,200000,\n"
                               "05/09/2026,SUMBANGAN MASJID,50000,\n"
                               "06/09/2026,TRSF BELANJA RUMAH TANGGA,300000,\n")
        self.ok("impor", f, "--akun", "BRI", "--jenis-file", "mutasi-bank", "--format-tanggal", "hari-bulan",
                "--tetapkan", "2=lain-lain", "--tetapkan", "3=lain-lain", "--ya")    # baris 1 = judul kolom
        kat = self.kategori_db()
        self.assertEqual(kat["TRSF KASBON KARYAWAN DEDI"], "kasbon")
        self.assertEqual(kat["SUMBANGAN MASJID"], "lain-lain")
        con = sqlite3.connect(self.db)
        (j,) = con.execute("SELECT id FROM transaksi WHERE catatan='TRSF BELANJA RUMAH TANGGA'").fetchone()
        con.close()
        self.ok("golongkan", "--id", str(j), "--kategori", "lain-lain", "--ya")
        self.assertEqual(self.kategori_db()["TRSF BELANJA RUMAH TANGGA"], "prive")
        self.assertEqual(self.ok("rekap", "--bulan", "09/2026")["hasil_usaha"], 1000000 - 50000)


class UjiV104(Dasar):
    """Uji ulang v1.0.3 (6,5/10): denda/biaya cicilan, utang pemasok, pelanggan bayar bon, 'X pinjam uang', denda pajak."""
    LAIN_KELUAR = (("25rb", "denda telat cicilan", "lain-lain", "beban_keuangan"),
                   ("30rb", "denda keterlambatan angsuran", "lain-lain", "beban_keuangan"),
                   ("5rb", "biaya admin cicilan", "lain-lain", "beban_keuangan"),
                   ("10rb", "bunga cicilan KUR", "lain-lain", "beban_keuangan"),
                   ("750rb", "bayar utang toko bangunan", "lain-lain", "bayar_utang_usaha"),
                   ("200rb", "Rudi pinjam uang", "kasbon", "piutang_lain"),
                   ("500rb", "angsuran pokok KUR", "pinjaman", "bayar_pinjaman"),
                   ("40rb", "ongkos pinjam troli", "lain-lain", "beban_lain"))

    def kategori_db(self):
        con = sqlite3.connect(self.db)
        try:
            return {c: k for c, k in con.execute("SELECT catatan, kategori FROM transaksi WHERE status='aktif'")}
        finally:
            con.close()

    def test_jebakan_penguji_laba_emkm_sama_neraca_seimbang(self):
        from decimal import Decimal as D
        self.ok("catat", "--masuk", "3jt", "--kategori", "penjualan", "--metode", "tunai", "--catatan", "jualan",
                "--tanggal", "02/09/2026", "--ya")
        self.ok("catat", "--keluar", "1jt", "--kategori", "beli-stok", "--metode", "tunai", "--catatan", "kulakan",
                "--tanggal", "03/09/2026", "--ya")
        for jml, cat, _, _ in self.LAIN_KELUAR:
            self.ok("catat", "--keluar", jml, "--kategori", "lain-lain", "--metode", "tunai", "--catatan", cat,
                    "--tanggal", "05/09/2026", "--ya")
        out = self.ok("catat", "--masuk", "150rb", "--kategori", "lain-lain", "--metode", "tunai", "--catatan",
                      "Bu Ani bayar hutang belanja", "--tanggal", "06/09/2026", "--ya")
        self.assertTrue(any("ke penjualan" in p for p in out["peringatan"]), out)
        out = self.ok("catat", "--keluar", "100rb", "--kategori", "pajak", "--metode", "tunai", "--catatan",
                      "denda pajak telat lapor", "--tanggal", "07/09/2026", "--ya")
        self.assertTrue(any("Pasal 9 ayat (1) huruf k" in p for p in out["peringatan"]), out)
        kat = self.kategori_db()
        for _, cat, harap, _ in self.LAIN_KELUAR:
            self.assertEqual(kat[cat], harap, cat)
        self.assertEqual(kat["Bu Ani bayar hutang belanja"], "penjualan")
        # verifikasi Decimal independen
        biaya = D(1000000) + D(25000) + D(30000) + D(5000) + D(10000) + D(750000) + D(40000) + D(100000)
        hasil = D(3000000) + D(150000) - biaya
        self.assertEqual(hasil, D(1190000))
        self.assertEqual(D(self.ok("rekap", "--bulan", "09/2026")["hasil_usaha"]), hasil)
        out = self.ok("ekspor", "--format", "emkm", "--bulan", "09/2026", "--csv", os.path.join(self.dir, "e.csv"))
        with open(out["file"], encoding="utf-8-sig", newline="") as fh:
            kode = {r[1]: r[4] for r in list(csv.reader(fh, delimiter=";"))[1:]}
        for _, cat, _, harap in self.LAIN_KELUAR:
            self.assertEqual(kode[cat], harap, cat)
        self.assertEqual(kode["denda pajak telat lapor"], "beban_lain")          # bukan beban PPh
        self.assertEqual(kode["Bu Ani bayar hutang belanja"], "pendapatan_usaha")
        emkm = os.path.join(SKILLS, "laporan-keuangan-emkm", "scripts", "laporan_emkm.py")
        if not os.path.isfile(emkm):
            self.skipTest("laporan-keuangan-emkm tidak ada di sebelah skill ini")
        r = subprocess.run([sys.executable, emkm, out["file"], "--format", "json", "--periode-awal", "2026-09-01",
                            "--periode-akhir", "2026-09-26", "--kas-akhir-aktual", str(out["saldo_akhir"]),
                            "--utang-bank-awal", "500000"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        d = json.loads(r.stdout)
        self.assertEqual(D(str(d["laba_rugi"]["laba_bersih"])), hasil)            # dulu selisih 25.000
        neraca = d["posisi_keuangan"]
        self.assertTrue(neraca["seimbang"], neraca)
        self.assertEqual(D(str(neraca["selisih"])), D(0))

    def test_tebakan_tanpa_kategori(self):
        kasus = (("keluar", "denda telat cicilan", "lain-lain"), ("keluar", "biaya admin angsuran", "lain-lain"),
                 ("keluar", "Rudi pinjam uang", "kasbon"), ("masuk", "Bu Ani bayar hutang belanja", "penjualan"),
                 ("masuk", "pinjaman dari saudara", "pinjaman"), ("keluar", "cicilan KUR", "pinjaman"))
        for n, (arah, cat, harap) in enumerate(kasus, 1):
            self.ok("catat", "--" + arah, str(10000 + n), "--metode", "tunai", "--catatan", cat, "--tanggal",
                    "05/09/2026", "--ya")
            self.assertEqual(self.kategori_db()[cat], harap, cat)
        # utang pemasok tanpa kategori: ditanyakan dengan pilihan jelas, bukan ditebak pinjaman
        for cat in ("bayar utang toko bangunan", "bayar hutang supplier", "lunasi bon grosir"):
            g = self.gagal("catat", "--keluar", "750rb", "--metode", "tunai", "--catatan", cat)
            self.assertTrue(g.get("perlu_kategori") and g.get("utang_pemasok"), g)
            self.assertIn("beli-stok", g["error"])
        # kategori pinjaman dipilih eksplisit untuk utang pemasok / pelanggan bayar bon -> diperingatkan
        o = self.ok("catat", "--keluar", "750rb", "--kategori", "pinjaman", "--metode", "tunai", "--catatan",
                    "bayar utang toko bangunan")
        self.assertTrue(any("PEMASOK" in p for p in o["peringatan"]), o)
        o = self.ok("catat", "--masuk", "150rb", "--kategori", "pinjaman", "--metode", "tunai", "--catatan",
                    "Bu Ani bayar hutang belanja")
        self.assertTrue(any("penjualan" in p for p in o["peringatan"]), o)

    def test_impor_dan_golongkan(self):
        f = self.file("m.csv", "Tanggal,Keterangan,Debet,Kredit\n"
                               "04/09/2026,BAYAR HUTANG TOKO BANGUNAN,750000,\n"
                               "05/09/2026,DENDA TELAT CICILAN,25000,\n"
                               "06/09/2026,BU ANI BAYAR HUTANG BELANJA,,150000\n")
        out = self.ok("impor", f, "--akun", "BRI", "--jenis-file", "mutasi-bank", "--format-tanggal", "hari-bulan",
                      "--ya")
        kat = self.kategori_db()
        self.assertEqual(kat["BAYAR HUTANG TOKO BANGUNAN"], "perlu-dicek")
        self.assertIn("pemasok", json.dumps(out, ensure_ascii=False))
        self.assertEqual(kat["DENDA TELAT CICILAN"], "lain-lain")
        self.assertEqual(kat["BU ANI BAYAR HUTANG BELANJA"], "penjualan")
        con = sqlite3.connect(self.db)
        (i,) = con.execute("SELECT id FROM transaksi WHERE catatan='BAYAR HUTANG TOKO BANGUNAN'").fetchone()
        con.close()
        o = self.ok("golongkan", "--id", str(i), "--kategori", "pinjaman")
        self.assertTrue(any("PEMASOK" in p for p in o["peringatan"]), o)
        self.ok("golongkan", "--id", str(i), "--kategori", "lain-lain", "--ya")
        self.assertEqual(self.kategori_db()["BAYAR HUTANG TOKO BANGUNAN"], "lain-lain")
        self.assertEqual(self.ok("rekap", "--bulan", "09/2026")["hasil_usaha"], 150000 - 750000 - 25000)

    def test_kode_emkm_unit(self):
        k = K.kode_emkm
        self.assertEqual(k("lain-lain", "keluar", "denda keterlambatan angsuran", "tunai"), "beban_keuangan")
        self.assertEqual(k("lain-lain", "keluar", "utang supplier", "bank"), "bayar_utang_usaha")
        self.assertEqual(k("lain-lain", "keluar", "denda pajak", "tunai"), "beban_lain")
        self.assertEqual(k("pajak", "keluar", "sanksi STP PPh", "tunai"), "beban_lain")
        self.assertEqual(k("pajak", "keluar", "PPh final Agustus", "tunai"), "")


if __name__ == "__main__":
    unittest.main(verbosity=1)
