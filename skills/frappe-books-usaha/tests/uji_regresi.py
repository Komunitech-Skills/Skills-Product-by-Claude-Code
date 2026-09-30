#!/usr/bin/env python3
"""Uji regresi frappe_books.py (Komunitech).

Jalankan:  python3 tests/uji_regresi.py      (Windows: python / py)

Memakai database Frappe Books TIRUAN (data fiktif) yang dibangun dari skema resmi v0.36.0
(tests/data/skema-frappe-books-v0.36.0.sql + tests/data/buat_db_contoh.py).
Angka pembanding dihitung independen dari data mentah di buat_db_contoh.py, bukan dari script.
"""
import csv
import hashlib
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal

SINI = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(SINI)
SKRIP = os.path.join(SKILL, "scripts", "frappe_books.py")
sys.path.insert(0, os.path.join(SINI, "data"))
sys.path.insert(0, os.path.join(SKILL, "scripts"))
import buat_db_contoh  # noqa: E402
import frappe_books as fb  # noqa: E402


RUMAH_KOSONG = tempfile.mkdtemp(prefix="uji-rumah-")  # HOME tanpa Documents/Frappe Books


def jalan(*arg, rumah=None):
    env = dict(os.environ)
    env.pop("FRAPPE_BOOKS_DB", None)
    env["HOME"] = env["USERPROFILE"] = rumah or RUMAH_KOSONG
    r = subprocess.run([sys.executable, SKRIP] + list(arg), capture_output=True, text=True, encoding="utf-8", env=env)
    return r.returncode, r.stdout, r.stderr


def sha(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


class Dasar(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="uji frappe books ")  # spasi di path sengaja
        cls.db = os.path.join(cls.tmp, "Toko Kopi #1.books.db")  # '#' sengaja: uji URI read-only
        buat_db_contoh.buat(cls.db)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def tulis(self, nama, isi):
        p = os.path.join(self.tmp, nama)
        with open(p, "w", encoding="utf-8", newline="") as f:
            f.write(isi)
        return p

    def baca_csv(self, p):
        with open(p, encoding="utf-8", newline="") as f:
            return list(csv.reader(f))


class UjiBaca(Dasar):
    def test_01_cek_dan_skema(self):
        k, out, err = jalan("cek", "--db", self.db)
        self.assertEqual(k, 0, err)
        self.assertIn("Toko Kopi Nusantara (fiktif)", out)
        self.assertIn("Struktur cocok", out)
        self.assertIn("invoice penjualan: 8", out)

    def test_02_database_tidak_berubah(self):
        sebelum = sha(self.db)
        for perintah in (["cek"], ["akun"], ["penjualan", "--bulan", "2026-09"], ["piutang"], ["stok"],
                         ["laba-rugi", "--bulan", "2026-09"], ["laporan-harian"]):
            jalan(*perintah, "--db", self.db)
        self.assertEqual(sebelum, sha(self.db))
        sisa = [f for f in os.listdir(self.tmp) if f.endswith(("-journal", "-wal", "-shm"))]
        self.assertEqual(sisa, [])

    def test_03_koneksi_benar_benar_read_only(self):
        con, _ = fb.buka_db(self.db)
        with self.assertRaises(sqlite3.DatabaseError):
            con.execute("DELETE FROM Party")
        con.close()

    def test_04_penjualan_september_angka_independen(self):
        # Independen: final & tidak batal di Sep (WIB): 1002 (300.000), 1003 (585.000 + 9.350),
        # 1004 (170.000 + 18.700), 1008 retur (-150.000). Draf 1005 & batal 1006 tidak dihitung.
        k, out, err = jalan("penjualan", "--db", self.db, "--bulan", "2026-09")
        self.assertEqual(k, 0, err)
        self.assertIn("DPP / sebelum pajak : Rp 905.000", out)
        self.assertIn("Pajak               : Rp 28.050", out)
        self.assertIn("TOTAL               : Rp 933.050", out)
        self.assertIn("Belum dibayar: Rp 483.050", out)
        self.assertIn("draf belum final: 1", out)
        self.assertIn("dibatalkan: 1", out)
        self.assertIn("termasuk 1 retur", out)

    def test_05_zona_waktu_tengah_malam_wib(self):
        # SINV-1002 disimpan 2026-08-31T17:00:00.000Z = 1 Sep 00:00 WIB -> masuk 1 Sep, bukan 31 Agu.
        k, out, _ = jalan("penjualan", "--db", self.db, "--tanggal", "2026-09-01")
        self.assertIn("TOTAL               : Rp 300.000", out)
        k, out, _ = jalan("penjualan", "--db", self.db, "--tanggal", "2026-08-31")
        self.assertIn("Belum ada invoice", out)
        self.assertEqual(fb.tanggal_lokal("2026-08-31T17:00:00.000Z", fb.offset_zona("WIB")).isoformat(), "2026-09-01")
        self.assertEqual(fb.tanggal_lokal("2026-08-31T14:59:00.000Z", fb.offset_zona("WIT")).isoformat(), "2026-08-31")
        self.assertEqual(fb.tanggal_lokal("2026-09-01", fb.offset_zona("WIB")).isoformat(), "2026-09-01")

    def test_06_penjualan_per_barang_dan_samarkan(self):
        k, out, _ = jalan("penjualan", "--db", self.db, "--bulan", "2026-09", "--per", "barang")
        self.assertIn("Kopi Arabika 250g - 3 - Rp 255.000", out)
        self.assertIn("Kopi Robusta 1kg - 1 - Rp 150.000", out)
        k, out, _ = jalan("penjualan", "--db", self.db, "--bulan", "2026-09", "--samarkan")
        self.assertNotIn("Warung Bu Sari", out)
        self.assertIn("W. B. S.", out)

    def test_07_pembelian(self):
        k, out, _ = jalan("pembelian", "--db", self.db, "--bulan", "2026-09")
        self.assertEqual(k, 0)
        self.assertIn("TOTAL               : Rp 1.110.000", out)
        self.assertIn("Pajak               : Rp 110.000", out)

    def test_08_piutang_umur(self):
        k, out, _ = jalan("piutang", "--db", self.db, "--hari-ini", "2026-09-26")
        self.assertEqual(k, 0)
        self.assertIn("Belum lunas: 4 invoice, total Rp 988.250", out)
        self.assertIn("SINV-1007 | Warung Bu Sari | tgl 1 Jun 2026 | sisa Rp 150.000 | telat 87 hari", out)
        self.assertIn("telat 48 hari", out)  # 10 Jul + 30 = 9 Agu -> 26 Sep = 48 hari
        self.assertNotIn("SINV-1005", out)  # draf
        self.assertNotIn("SINV-1006", out)  # batal

    def test_09_piutang_tempo_lain(self):
        k, out, _ = jalan("piutang", "--db", self.db, "--hari-ini", "2026-09-26", "--tempo", "0")
        self.assertIn("SINV-1004 | Toko Sinar Abadi | tgl 26 Sep 2026 | sisa Rp 188.700 | jatuh tempo 26 Sep 2026", out)
        self.assertIn("telat 1 hari", out)  # SINV-1003 25 Sep, tempo 0

    def test_10_utang(self):
        k, out, _ = jalan("utang", "--db", self.db, "--hari-ini", "2026-09-26")
        self.assertIn("Belum lunas: 2 invoice, total Rp 1.310.000", out)
        self.assertIn("PINV-2002 | UD Gula Manis | tgl 1 Agu 2026 | sisa Rp 200.000 | telat 26 hari", out)

    def test_11_stok(self):
        k, out, _ = jalan("stok", "--db", self.db)
        self.assertIn("Filter Kertas: -1 Unit", out)
        self.assertIn("Paper Cup 8oz: 0 Unit", out)
        self.assertIn("Gula Aren 1kg: 2 Kg", out)
        self.assertIn("Kopi Robusta 1kg: 1 Unit", out)
        self.assertNotIn("Jasa Seduh", out)  # jasa tidak dilacak
        k, out, _ = jalan("stok", "--db", self.db, "--semua")
        self.assertIn("Kopi Arabika 250g: 24 Unit", out)  # 10-3+20-1-2
        k, out, _ = jalan("stok", "--db", self.db, "--lokasi", "Gudang", "--semua")
        self.assertIn("Kopi Arabika 250g: 20 Unit", out)

    def test_12_laba_rugi(self):
        # Pendapatan: 300.000 - 150.000 + 85.000 + 170.000 (Penjualan) + 500.000 (Service) = 905.000
        # HPP: 200.000 - 100.000 + 50.000 + 100.000 = 250.000 ; Beban Sep: 1.000.000 + 250.000
        # Entri 1 Okt 00:30 WIB & Agustus & entri reverted TIDAK dihitung.
        k, out, _ = jalan("laba-rugi", "--db", self.db, "--bulan", "2026-09")
        self.assertEqual(k, 0)
        self.assertIn("Total pendapatan: Rp 905.000", out)
        self.assertIn("HPP Pembelian - 4210.000: Rp 250.000", out)
        self.assertIn("LABA KOTOR: Rp 655.000", out)
        self.assertIn("Total beban: Rp 1.250.000", out)
        self.assertIn("RUGI BERSIH: -Rp 595.000", out)

    def test_13_laporan_harian_tanpa_nama(self):
        k, out, _ = jalan("laporan-harian", "--db", self.db, "--hari-ini", "2026-09-26")
        self.assertEqual(k, 0)
        self.assertIn("Penjualan final: 1 invoice, Rp 188.700", out)
        self.assertIn("-68,3%", out)  # (188.700-594.350)/594.350
        self.assertIn("Piutang telat (tempo 30 hari): 2 invoice, Rp 505.200", out)
        for nama in ("Toko Sinar Abadi", "Warung Bu Sari", "CV Maju Jaya"):
            self.assertNotIn(nama, out)

    def test_14_akun_dan_peringatan_pajak_12(self):
        k, out, _ = jalan("akun", "--db", self.db)
        self.assertIn("PPN 11% (12% x 11/12): 11% ke akun Hutang Pajak - 2141.000", out)
        self.assertIn("SATUAN (UOM): Day, Gram, Hour, Kg, Meter, Unit", out)
        salin = os.path.join(self.tmp, "pajak12.books.db")
        shutil.copy(self.db, salin)
        c = sqlite3.connect(salin)
        c.execute("UPDATE TaxDetail SET rate = 12")
        c.commit()
        c.close()
        k, out, _ = jalan("akun", "--db", salin)
        self.assertIn("PERHATIAN: tarif 12%", out)


class UjiGalat(Dasar):
    def test_15_file_tidak_ada_rusak_bukan_frappe(self):
        k, _, err = jalan("penjualan", "--db", os.path.join(self.tmp, "tidak-ada.books.db"))
        self.assertEqual(k, 3)
        self.assertIn("tidak ditemukan", err)
        rusak = self.tulis("rusak.books.db", "ini bukan sqlite")
        k, _, err = jalan("stok", "--db", rusak)
        self.assertEqual(k, 3)
        self.assertNotIn("Traceback", err)
        lain = os.path.join(self.tmp, "lain.db")
        c = sqlite3.connect(lain)
        c.execute("CREATE TABLE x(a)")
        c.commit()
        c.close()
        k, _, err = jalan("penjualan", "--db", lain)
        self.assertEqual(k, 3)
        self.assertIn("bukan database Frappe Books", err)

    def test_16_skema_versi_lain(self):
        salin = os.path.join(self.tmp, "versi-lain.books.db")
        shutil.copy(self.db, salin)
        c = sqlite3.connect(salin)
        c.execute("ALTER TABLE SalesInvoice RENAME COLUMN outstandingAmount TO sisaTagihan")
        c.commit()
        c.close()
        k, _, err = jalan("piutang", "--db", salin)
        self.assertEqual(k, 4)
        self.assertIn("SalesInvoice.outstandingAmount", err)
        self.assertNotIn("Traceback", err)

    def test_17_argumen_salah(self):
        for arg, kata in ((["penjualan", "--db", self.db, "--bulan", "2026-13"], "--bulan"),
                          (["penjualan", "--db", self.db, "--dari", "2026-09-01"], "--dari dan --sampai"),
                          (["piutang", "--db", self.db, "--tz", "GMT"], "Zona waktu"),
                          (["piutang", "--db", self.db, "--tempo", "-3"], "--tempo"),
                          (["stok", "--db", self.db, "--lokasi", "Dapur"], "Lokasi 'Dapur'"),
                          (["tidak-ada"], "Perintah kurang/salah"), ([], "Perintah belum disebut")):
            k, _, err = jalan(*arg)
            self.assertEqual(k, 2, arg)
            self.assertIn(kata, err)
            self.assertNotIn("Traceback", err)

    def test_18_nilai_currency_aneh_tidak_crash(self):
        salin = os.path.join(self.tmp, "aneh.books.db")
        shutil.copy(self.db, salin)
        c = sqlite3.connect(salin)
        c.execute("UPDATE SalesInvoice SET netTotal = NULL, outstandingAmount = 'abc' WHERE name='SINV-1003'")
        c.execute("UPDATE SalesInvoice SET date = 'bukan tanggal' WHERE name='SINV-1004'")
        c.commit()
        c.close()
        k, out, err = jalan("penjualan", "--db", salin, "--bulan", "2026-09")
        self.assertEqual(k, 0, err)
        self.assertIn("TOTAL", out)


class UjiCariOtomatis(Dasar):
    def test_29_cari_db_otomatis_di_documents(self):
        rumah = os.path.join(self.tmp, "rumah")
        folder = os.path.join(rumah, "Documents", "Frappe Books")
        os.makedirs(folder)
        shutil.copy(self.db, os.path.join(folder, "Toko Kopi.books.db"))
        k, out, err = jalan("cek", rumah=rumah)
        self.assertEqual(k, 0, err)
        self.assertIn("Toko Kopi Nusantara", out)
        masuk = self.tulis("auto.csv", "nama,hp\nPelanggan Baru,0811111111\n")
        k, out, _ = jalan("csv-pelanggan", "--masuk", masuk, "--keluar", os.path.join(self.tmp, "auto-out.csv"), rumah=rumah)
        self.assertEqual(k, 0)
        self.assertIn("Memakai database Frappe Books", out)
        shutil.copy(self.db, os.path.join(folder, "Usaha Kedua.books.db"))
        k, _, err = jalan("stok", rumah=rumah)
        self.assertEqual(k, 2)
        self.assertIn("beberapa file", err)
        k, _, err = jalan("stok")
        self.assertEqual(k, 2)
        self.assertIn("belum diketahui", err)


class UjiPpn(unittest.TestCase):
    def test_19_ppn_standar_komunitech(self):
        self.assertEqual(fb.ppn_dari_dpp(Decimal(332345))[2], Decimal(36557))   # 36.557,95 -> ke bawah
        self.assertEqual(fb.ppn_dari_dpp(Decimal(1000000))[2], Decimal(110000))
        self.assertEqual(fb.ppn_dari_dpp(Decimal(1))[2], Decimal(0))
        k, out, _ = jalan("ppn", "--dpp", "332.345")
        self.assertIn("dibulatkan ke bawah Rp 36.557", out)
        self.assertIn("TOTAL tagihan                  : Rp 368.902", out)
        self.assertIn("belum dicocokkan dengan Coretax", out)

    def test_20_ppn_harga_termasuk(self):
        for harga in (1110000, 368902, 100000, 999, 1, 0, 12345678):
            h = Decimal(harga)
            d = fb.dpp_dari_harga_termasuk(h)
            self.assertLessEqual(d + fb.ppn_dari_dpp(d)[2], h)
            self.assertGreater((d + 1) + fb.ppn_dari_dpp(d + 1)[2], h)
        self.assertEqual(fb.dpp_dari_harga_termasuk(Decimal(1110000)), Decimal(1000000))
        k, out, _ = jalan("ppn", "--harga-termasuk", "100000")
        self.assertIn("Harga jual / penggantian (DPP)  : Rp 90.090", out)  # 90.090 + 9.909 = 99.999
        self.assertIn("sisa pembulatan Rp 1", out)
        k, _, err = jalan("ppn")
        self.assertEqual(k, 2)
        k, _, err = jalan("ppn", "--dpp", "12.5")
        self.assertEqual(k, 2)

    def test_21_baca_rupiah(self):
        ok = {"85000": 85000, "Rp 85.000": 85000, "85.000,50": Decimal("85000.50"), "85rb": 85000,
              "1,5jt": 1500000, "1.5 juta": 1500000, "Rp1.250.000,-": 1250000, "12.5": Decimal("12.5"),
              "1,000.50": Decimal("1000.50")}
        for teks, harap in ok.items():
            self.assertEqual(fb.baca_rupiah(teks), Decimal(harap), teks)
        for teks in ("85,000", "abc", "", "1.2.3"):
            with self.assertRaises(ValueError):
                fb.baca_rupiah(teks)

    def test_21b_baca_jumlah_format_indonesia(self):
        # audit format angka 2026-09-30: '1.500' dulu terbaca 1,5 dan '38.000' terbaca 38 (diam-diam)
        ok = {"3": 3, "1.500": 1500, "38.000": 38000, "1.250.000": 1250000, "1.500,5": Decimal("1500.5"),
              "1,5": Decimal("1.5"), "2.5": Decimal("2.5"), "0.500": Decimal("0.5"), "0,25": Decimal("0.25")}
        for teks, harap in ok.items():
            self.assertEqual(fb.baca_jumlah(teks), Decimal(harap), teks)
        for teks in ("1,500", "1,250,000", "abc", "", "1.5.0"):
            with self.assertRaises(ValueError, msg=teks):
                fb.baca_jumlah(teks)


class UjiCsv(Dasar):
    def test_22_csv_pelanggan_template_resmi(self):
        masuk = self.tulis("pel.csv", "Nama Pelanggan;No HP;Email\nKedai Kopi Senja;0812-3456-7890;senja@contoh.id\n"
                                      "Toko Sinar Abadi;081234567001;\nCV Berkah, Solo;62811222333;\nBu \"Rina\";;rina@contoh\n")
        keluar = os.path.join(self.tmp, "hasil", "pel-impor.csv")
        k, out, err = jalan("csv-pelanggan", "--db", self.db, "--masuk", masuk, "--keluar", keluar)
        self.assertEqual(k, 0, out + err)
        with open(keluar, "rb") as f:
            self.assertIn(b"\r\n", f.read())  # CRLF seperti generateCSV Frappe Books
        rows = self.baca_csv(keluar)
        self.assertEqual(rows[2], ["Party.name", "Party.role", "Party.email", "Party.phone"])  # file asli: tanpa taxId
        self.assertEqual(rows[3][:4], ["Kedai Kopi Senja", "Customer", "senja@contoh.id", "+6281234567890"])
        self.assertEqual(rows[4][0], "CV Berkah, Solo")
        self.assertEqual(rows[5][0], "Bu 'Rina'")  # kutip ganda diganti (parser Frappe Books)
        self.assertEqual(len(rows), 6)  # Toko Sinar Abadi sudah ada -> dilewati
        self.assertIn("sudah ada di Frappe Books", out)
        self.assertIn("email 'rina@contoh' tampak salah", out)

    def test_23_csv_pelanggan_dobel_ditolak(self):
        masuk = self.tulis("dobel.csv", "nama,hp\nA Jaya,0811\na jaya,0812\n,0813\n")
        keluar = os.path.join(self.tmp, "dobel-out.csv")
        k, out, _ = jalan("csv-pelanggan", "--masuk", masuk, "--keluar", keluar)
        self.assertEqual(k, 5)
        self.assertIn("dobel dengan baris 2", out)
        self.assertIn("baris 4: nama kosong", out)
        self.assertFalse(os.path.exists(keluar))

    def test_24_csv_barang_akun_dan_satuan(self):
        masuk = self.tulis("brg.csv", 'nama barang,sku,satuan,harga jual,jenis,stok\nKopi Liberika,KPL,Unit,"Rp 95.000",barang,ya\n'
                                      'Kelas Barista,,,"1,5jt",jasa,ya\nKopi Arabika 250g,KPA,Unit,85000,barang,ya\n')
        keluar = os.path.join(self.tmp, "brg-out.csv")
        k, out, err = jalan("csv-barang", "--db", self.db, "--masuk", masuk, "--keluar", keluar)
        self.assertEqual(k, 0, out + err)
        rows = self.baca_csv(keluar)
        self.assertEqual(rows[2][0], "Item.name")
        kol = rows[2]
        b1 = dict(zip(kol, rows[3]))
        b2 = dict(zip(kol, rows[4]))
        self.assertEqual((b1["Item.rate"], b1["Item.incomeAccount"], b1["Item.expenseAccount"], b1["Item.trackItem"]),
                         ("95000", "Penjualan - 4110.000", "Stock Diterima Tapi Tidak Ditagih - 2115.000", "1"))  # v1.0.2: bawaan Frappe
        self.assertEqual((b2["Item.itemType"], b2["Item.rate"], b2["Item.unit"], b2["Item.incomeAccount"], b2["Item.trackItem"]),
                         ("Service", "1500000", "Hour", "Pendapatan Service - 4310.000", "0"))
        self.assertEqual(len(rows), 5)  # Kopi Arabika sudah ada
        salah = self.tulis("brg2.csv", "nama,satuan\nSusu,Liter\n")
        k, out, _ = jalan("csv-barang", "--db", self.db, "--masuk", salah, "--keluar", os.path.join(self.tmp, "brg-out2.csv"))
        self.assertEqual(k, 5)
        self.assertIn("satuan 'Liter' belum ada", out)

    def test_25_csv_transaksi_valid(self):
        masuk = self.tulis("jual.csv", "No Nota;Tanggal;Pelanggan;Barang;Jumlah;Harga;Pajak\n"
                                       "N-01;27/09/2026;Toko Sinar Abadi;Kopi Arabika 250g;3;85.000;PPN 11% (12% x 11/12)\n"
                                       "N-01;27/09/2026;toko sinar abadi;Gula Aren 1kg;2;32.500;PPN 11% (12% x 11/12)\n"
                                       "N-01;27/09/2026;Toko Sinar Abadi;Jasa Seduh Event;1;12345;PPN 11% (12% x 11/12)\n"
                                       "N-02;28 Sep 2026;Warung Bu Sari;Kopi Robusta 1kg;1;150rb;\n")
        keluar = os.path.join(self.tmp, "jual-out.csv")
        k, out, err = jalan("csv-transaksi", "--db", self.db, "--masuk", masuk, "--keluar", keluar)
        self.assertEqual(k, 0, out + err)
        self.assertIn("N-01 | 27 Sep 2026 | Toko Sinar Abadi | DPP Rp 332.345 | PPN (standar Komunitech) Rp 36.557 | total Rp 368.902", out)
        rows = self.baca_csv(keluar)
        self.assertEqual(rows[2][:5], ["SalesInvoice.name", "SalesInvoice.numberSeries", "SalesInvoice.party", "SalesInvoice.account", "SalesInvoice.date"])
        d = [dict(zip(rows[2], r)) for r in rows[3:]]
        self.assertEqual(len(d), 4)
        self.assertEqual(d[0]["SalesInvoice.name"], "IMPOR-N-01")
        self.assertEqual(d[1]["SalesInvoice.party"], "Toko Sinar Abadi")  # huruf disamakan dengan data
        self.assertEqual(d[2]["SalesInvoiceItem.account"], "Pendapatan Service - 4310.000")  # akun dari data barang
        self.assertEqual(d[3]["SalesInvoice.date"], "2026-09-28")
        self.assertEqual(d[3]["SalesInvoiceItem.rate"], "150000")
        self.assertEqual(d[0]["SalesInvoice.account"], "Piutang Dagang - 1131.0010")
        self.assertEqual(d[0]["SalesInvoice.numberSeries"], "SINV-")

    def test_26_csv_transaksi_buruk(self):
        masuk = self.tulis("buruk.csv", "No Nota;Tanggal;Pelanggan;Barang;Jumlah;Harga\n"
                                        "N-01;31/09/2026;CV Maju Jaya;Kopi Arabika 250g;3;85000\n"
                                        "N-02;27/09/2026;CV Maju Jaya;Teh Hijau;1;10000\n"
                                        "N-03;27/09/2026;CV Maju Jaya;Kopi Robusta 1kg;0;150000\n"
                                        "N-04;27/09/2026;CV Maju Jaya;Kopi Robusta 1kg;1;85,000\n"
                                        "N-05;27/09/2026;Toko Baru;Kopi Robusta 1kg;1;1000\n"
                                        "N-06;27/09/2026;CV Maju Jaya;Kopi Robusta 1kg;1;1000\n"
                                        "N-06;28/09/2026;CV Maju Jaya;Kopi Robusta 1kg;1;1000\n")
        keluar = os.path.join(self.tmp, "buruk-out.csv")
        k, out, _ = jalan("csv-transaksi", "--db", self.db, "--masuk", masuk, "--keluar", keluar)
        self.assertEqual(k, 5)
        for kata in ("tidak ada di kalender", "'Teh Hijau' belum ada", "jumlah harus lebih dari 0", "ambigu",
                     "'Toko Baru' belum ada", "nota 'N-06' berbeda tanggal"):
            self.assertIn(kata, out)
        self.assertFalse(os.path.exists(keluar))

    def test_27_csv_kolom_kurang_dan_koma_liar(self):
        masuk = self.tulis("kurang.csv", "tanggal,barang\n2026-09-01,Kopi\n")
        k, _, err = jalan("csv-transaksi", "--db", self.db, "--masuk", masuk, "--keluar", os.path.join(self.tmp, "k.csv"))
        self.assertEqual(k, 5)
        self.assertIn("Kolom wajib tidak ditemukan", err)
        liar = self.tulis("liar.csv", "nama,harga\nKelas Barista,1,5jt\n")
        k, _, err = jalan("csv-barang", "--db", self.db, "--masuk", liar, "--keluar", os.path.join(self.tmp, "l.csv"))
        self.assertEqual(k, 5)
        self.assertIn("kolom lebih banyak", err)
        k, _, err = jalan("csv-barang", "--masuk", os.path.join(self.tmp, "tak-ada.csv"), "--keluar", "x.csv")
        self.assertEqual(k, 2)

    def test_28_csv_tanpa_db_butuh_akun(self):
        masuk = self.tulis("brg-nodb.csv", "nama,harga\nKopi,10000\n")
        k, _, err = jalan("csv-barang", "--masuk", masuk, "--keluar", os.path.join(self.tmp, "n.csv"))
        self.assertEqual(k, 2)
        self.assertIn("Akun penjualan belum ditentukan", err)
        k, out, _ = jalan("csv-barang", "--masuk", masuk, "--keluar", os.path.join(self.tmp, "n.csv"),
                          "--akun-penjualan", "Sales", "--akun-pembelian", "Cost of Goods Sold")
        self.assertEqual(k, 0)
        self.assertIn("belum dicek", out)
        k, _, err = jalan("csv-barang", "--db", self.db, "--masuk", masuk, "--keluar", os.path.join(self.tmp, "n2.csv"),
                          "--akun-penjualan", "Penjualan - 4000.000")
        self.assertEqual(k, 2)
        self.assertIn("akun grup", err)


class UjiRevisi101(Dasar):
    """Regresi temuan uji independen v1.0.0 (file .books.db ASLI Frappe Books v0.36.0)."""

    def nota(self, nama, pihak="Toko Sinar Abadi"):
        return self.tulis(nama, "No Nota;Tanggal;Pelanggan;Barang;Jumlah;Harga\n"
                                f"N-01;27/09/2026;{pihak};Kopi Arabika 250g;1;50000\n")

    def salin_db(self, nama, *sql):
        p = os.path.join(self.tmp, nama)
        shutil.copy(self.db, p)
        c = sqlite3.connect(p)
        for x in sql:
            c.execute(x)
        c.commit()
        c.close()
        return p

    def test_30_number_series_wajib_di_csv_invoice(self):
        for jenis, skema, seri, pihak in (("penjualan", "SalesInvoice", "SINV-", "Toko Sinar Abadi"),
                                         ("pembelian", "PurchaseInvoice", "PINV-", "PT Biji Kopi Gayo")):
            keluar = os.path.join(self.tmp, f"seri-{jenis}.csv")
            k, out, err = jalan("csv-transaksi", "--db", self.db, "--jenis", jenis, "--masuk", self.nota(f"n-{jenis}.csv", pihak),
                                "--keluar", keluar)
            self.assertEqual(k, 0, out + err)
            rows = self.baca_csv(keluar)
            self.assertEqual(rows[2][1], f"{skema}.numberSeries")
            self.assertEqual(rows[1][1], "Number Series")
            self.assertEqual(rows[3][1], seri)
        k, _, err = jalan("csv-transaksi", "--db", self.db, "--masuk", self.nota("n-seri.csv"), "--keluar",
                          os.path.join(self.tmp, "seri-x.csv"), "--seri", "INV-LAIN-")
        self.assertEqual(k, 2)
        self.assertIn("Number Series 'INV-LAIN-' tidak ada", err)
        dua = self.salin_db("dua-seri.books.db", "DELETE FROM NumberSeries WHERE name='SINV-'",
                            "INSERT INTO NumberSeries VALUES ('JUAL-',1001,4,'SalesInvoice',1001,'a','a','x','x')",
                            "INSERT INTO NumberSeries VALUES ('POS-',1001,4,'SalesInvoice',1001,'a','a','x','x')")
        k, _, err = jalan("csv-transaksi", "--db", dua, "--masuk", self.nota("n-dua.csv"), "--keluar", os.path.join(self.tmp, "s2.csv"))
        self.assertEqual(k, 2)
        self.assertIn("beberapa Number Series", err)

    def test_31_akun_bernomor_tidak_menebak(self):
        brg = self.tulis("akun-brg.csv", "nama,jenis\nKopi X,barang\nKursus Y,jasa\n")
        keluar = os.path.join(self.tmp, "akun-brg-out.csv")
        k, out, err = jalan("csv-barang", "--db", self.db, "--masuk", brg, "--keluar", keluar)
        self.assertEqual(k, 0, out + err)
        self.assertNotIn("Bunga Bank", out + open(keluar, encoding="utf-8").read())
        d = [dict(zip(self.baca_csv(keluar)[2], r)) for r in self.baca_csv(keluar)[3:]]
        self.assertEqual(d[0]["Item.incomeAccount"], "Penjualan - 4110.000")
        self.assertEqual(d[1]["Item.incomeAccount"], "Pendapatan Service - 4310.000")
        keluar = os.path.join(self.tmp, "akun-beli.csv")
        k, out, err = jalan("csv-transaksi", "--db", self.db, "--jenis", "pembelian",
                            "--masuk", self.nota("n-beli.csv", "PT Biji Kopi Gayo"), "--keluar", keluar)
        self.assertEqual(k, 0, out + err)
        self.assertEqual(dict(zip(self.baca_csv(keluar)[2], self.baca_csv(keluar)[3]))["PurchaseInvoice.account"],
                         "Hutang Dagang Dalam Negeri - 2111.001")
        # Akun utang dagang tidak ada -> jangan menebak (HUtang Dagang Biaya Kirim...), tanya pengguna
        tanpa = self.salin_db("tanpa-utang.books.db",
                              "DELETE FROM Account WHERE name='Hutang Dagang Dalam Negeri - 2111.001'")
        k, _, err = jalan("csv-transaksi", "--db", tanpa, "--jenis", "pembelian",
                          "--masuk", self.nota("n-beli2.csv", "PT Biji Kopi Gayo"), "--keluar", os.path.join(self.tmp, "u.csv"))
        self.assertEqual(k, 2)
        self.assertIn("tidak bisa dipastikan otomatis", err)
        self.assertIn("HUtang Dagang Biaya Kirim Luar Negeri - 2111.004", err)
        self.assertIn("Tanyakan ke pengguna", err)
        tanpa2 = self.salin_db("tanpa-jual.books.db", "DELETE FROM Account WHERE name='Penjualan - 4110.000'")
        k, _, err = jalan("csv-barang", "--db", tanpa2, "--masuk", brg, "--keluar", os.path.join(self.tmp, "j.csv"))
        self.assertEqual(k, 2)
        self.assertIn("Akun penjualan tidak bisa dipastikan", err)
        # nama tanpa nomor dari pengguna dicocokkan ke nama bernomor yang tunggal
        k, out, _ = jalan("csv-barang", "--db", self.db, "--masuk", brg, "--keluar", os.path.join(self.tmp, "j2.csv"),
                          "--akun-penjualan", "Penjualan", "--akun-pembelian", "HPP Pembelian")
        self.assertEqual(k, 0)
        self.assertIn("Akun penjualan: Penjualan - 4110.000", out)

    def test_32_keluar_tidak_boleh_menimpa_database(self):
        brg = self.tulis("aman.csv", "nama\nKopi Z\n")
        sebelum = sha(self.db)
        salin = self.salin_db("korban.books.db")
        sqlite_csv = os.path.join(self.tmp, "menyamar.csv")
        shutil.copy(self.db, sqlite_csv)
        for keluar in (self.db, salin, os.path.join(self.tmp, "apa.db"), sqlite_csv, os.path.join(self.tmp, "x.txt")):
            for perintah in (["csv-barang"], ["csv-pelanggan"], ["csv-transaksi"]):
                k, _, err = jalan(*perintah, "--db", self.db, "--masuk", brg, "--keluar", keluar)
                self.assertEqual(k, 2, (perintah, keluar, err))
                self.assertNotIn("Traceback", err)
        self.assertEqual(sha(self.db), sebelum)
        with open(sqlite_csv, "rb") as f:
            self.assertTrue(f.read(16).startswith(b"SQLite format 3"))
        # nama .csv tetapi sama dengan database yang dipakai (db ber-akhiran .csv)
        db_csv = self.salin_db("db-bernama.csv")
        k, _, err = jalan("csv-pelanggan", "--db", db_csv, "--masuk", brg, "--keluar", db_csv)
        self.assertEqual(k, 2)

    def test_33_centang_inventory_format_asli(self):
        self.assertTrue(fb.centang("1.0"))
        self.assertFalse(fb.centang("0.0"))
        self.assertTrue(fb.centang("1"))
        self.assertFalse(fb.centang(None))
        k, out, _ = jalan("cek", "--db", self.db)  # fixture menyimpan '1.0' seperti file asli
        self.assertIn("Fitur stok (Inventory): aktif", out)
        mati = self.salin_db("inv-mati.books.db", "UPDATE SingleValue SET value='0.0' WHERE fieldname='enableInventory'")
        k, out, _ = jalan("cek", "--db", mati)
        self.assertIn("Fitur stok (Inventory): tidak aktif", out)
        brg = self.tulis("lacak.csv", "nama,stok\nKopi Lacak,ya\n")
        k, out, _ = jalan("csv-barang", "--db", self.db, "--masuk", brg, "--keluar", os.path.join(self.tmp, "lacak-out.csv"))
        self.assertNotIn("fitur Inventory belum aktif", out)

    def test_34_retur_laba_rugi_sejalan_dengan_penjualan(self):
        # Retur SINV-1008 diposting bertanda terbalik (seperti v0.36.0). Pendapatan koreksi = DPP penjualan (905.000).
        k, out, _ = jalan("laba-rugi", "--db", self.db, "--bulan", "2026-09")
        self.assertIn("Total pendapatan: Rp 905.000", out)
        # v1.0.3: P&L Frappe sendiri memakai nilai mutlak per kolom (LedgerReport.ts) -> retur mengurangi; tidak ada
        # lagi "angka buku besar apa adanya" yang berbeda (klaim v1.0.1-1.0.2 keliru, dibuktikan di aplikasi asli).
        self.assertIn("Catatan retur: 2 dokumen retur", out)
        self.assertIn("SHPM-R1008, SINV-1008", out)
        self.assertIn("HPP Pembelian - 4210.000: Rp 250.000", out)
        self.assertNotIn("1.205.000", out)
        k, out2, _ = jalan("penjualan", "--db", self.db, "--bulan", "2026-09")
        self.assertIn("DPP / sebelum pajak : Rp 905.000", out2)
        self.assertIn("Terbayar (bersih)", out2)
        k, out3, _ = jalan("laba-rugi", "--db", self.db, "--bulan", "2026-08")
        self.assertNotIn("Catatan retur", out3)

    def test_35_npwp_tidak_hilang_diam_diam(self):
        pel = self.tulis("npwp.csv", "nama,npwp\nPT Pajak Taat,01.234.567.8-901.000\n")
        keluar = os.path.join(self.tmp, "npwp-out.csv")
        k, out, _ = jalan("csv-pelanggan", "--db", self.db, "--masuk", pel, "--keluar", keluar)
        self.assertEqual(k, 0)
        self.assertNotIn("Party.taxId", self.baca_csv(keluar)[2])
        self.assertIn("NPWP '01.234.567.8-901.000' milik 'PT Pajak Taat' TIDAK ikut diimpor", out)
        db_tax = os.path.join(self.tmp, "taxid.books.db")
        buat_db_contoh.buat(db_tax, taxid=True)
        k, out, _ = jalan("csv-pelanggan", "--db", db_tax, "--masuk", pel, "--keluar", keluar)
        rows = self.baca_csv(keluar)
        self.assertEqual(dict(zip(rows[2], rows[3]))["Party.taxId"], "01.234.567.8-901.000")
        k, out, _ = jalan("csv-pelanggan", "--masuk", pel, "--keluar", keluar)
        self.assertIn("belum dicek apakah Frappe Books Anda punya kolom itu", out)

    def test_36_csv_byte_tidak_valid(self):
        p = os.path.join(self.tmp, "rusak-byte.csv")
        with open(p, "wb") as f:
            f.write(b"nama\n\x81abc\n")
        k, _, err = jalan("csv-pelanggan", "--masuk", p, "--keluar", os.path.join(self.tmp, "rb.csv"))
        self.assertEqual(k, 5)
        self.assertIn("simpan ulang", err)
        self.assertNotIn("tak terduga", err)

    def test_37_lokasi_rumah_linux_dan_onedrive(self):
        for sub in (("Frappe Books",), ("OneDrive", "Documents", "Frappe Books")):
            rumah = tempfile.mkdtemp(prefix="rumah-", dir=self.tmp)
            folder = os.path.join(rumah, *sub)
            os.makedirs(folder)
            shutil.copy(self.db, os.path.join(folder, "Usaha.books.db"))
            k, out, err = jalan("cek", rumah=rumah)
            self.assertEqual(k, 0, (sub, err))

    def test_38_samarkan_nama_berkurung(self):
        self.assertEqual(fb.samarkan("Warung Pak Budi (Pasar Baru)"), "W. P. B. P. B.")
        self.assertEqual(fb.samarkan("CV. Maju-Jaya"), "C. M. J.")
        self.assertEqual(fb.samarkan("((  ))"), "?")

    def test_39_peran_pihak_tidak_cocok(self):
        k, out, _ = jalan("csv-transaksi", "--db", self.db, "--jenis", "pembelian",
                          "--masuk", self.nota("n-peran.csv", "Toko Sinar Abadi"), "--keluar", os.path.join(self.tmp, "peran.csv"))
        self.assertEqual(k, 0)
        self.assertIn("terdaftar sebagai pelanggan saja", out)


class UjiRevisi102(Dasar):
    """Regresi uji ulang v1.0.1 di Frappe Books v0.36.0 asli: akun pembelian barang berstok & kredit retur di piutang."""

    def salin_db(self, nama, *sql):
        p = os.path.join(self.tmp, nama)
        shutil.copy(self.db, p)
        c = sqlite3.connect(p)
        for x in sql:
            c.execute(x)
        c.commit()
        c.close()
        return p

    def test_40_akun_pembelian_barang_berstok_dari_inventory_settings(self):
        brg = self.tulis("stok102.csv", "nama,jenis,stok\nKopi Stok,barang,ya\nKopi Titip,barang,tidak\nKursus,jasa,\n")
        keluar = os.path.join(self.tmp, "stok102-out.csv")
        k, out, err = jalan("csv-barang", "--db", self.db, "--masuk", brg, "--keluar", keluar)
        self.assertEqual(k, 0, out + err)
        d = {r[0]: dict(zip(self.baca_csv(keluar)[2], r)) for r in self.baca_csv(keluar)[3:]}
        self.assertEqual(d["Kopi Stok"]["Item.expenseAccount"], "Stock Diterima Tapi Tidak Ditagih - 2115.000")
        self.assertEqual(d["Kopi Titip"]["Item.expenseAccount"], "HPP Pembelian - 4210.000")
        self.assertEqual(d["Kursus"]["Item.expenseAccount"], "HPP Pembelian - 4210.000")
        # nilai benar-benar dibaca dari InventorySettings (bukan tebakan nama)
        lain = self.salin_db("srbnb-lain.books.db",
                             "INSERT INTO Account (name, rootType, accountType, isGroup, lft, rgt, createdBy, modifiedBy, created, modified) "
                             "VALUES ('Barang Diterima Belum Ditagih - 2116.000','Liability','Stock Received But Not Billed',0,90,91,'a','a','x','x')",
                             "UPDATE SingleValue SET value='Barang Diterima Belum Ditagih - 2116.000' WHERE fieldname='stockReceivedButNotBilled'")
        k, out, _ = jalan("csv-barang", "--db", lain, "--masuk", brg, "--keluar", keluar)
        self.assertEqual(k, 0)
        self.assertIn("akun pembelian barang berstok: Barang Diterima Belum Ditagih - 2116.000", out)
        # Inventory Settings kosong & ada 2 akun bertipe SRBNB -> jangan menebak
        dua = self.salin_db("srbnb-dua.books.db",
                            "INSERT INTO Account (name, rootType, accountType, isGroup, lft, rgt, createdBy, modifiedBy, created, modified) "
                            "VALUES ('Barang Diterima Belum Ditagih - 2116.000','Liability','Stock Received But Not Billed',0,90,91,'a','a','x','x')",
                            "INSERT INTO Account (name, rootType, accountType, isGroup, lft, rgt, createdBy, modifiedBy, created, modified) "
                            "VALUES ('Titipan Barang Masuk - 2117.000','Liability','Stock Received But Not Billed',0,92,93,'a','a','x','x')",
                            "DELETE FROM Account WHERE name='Stock Diterima Tapi Tidak Ditagih - 2115.000'",
                            "DELETE FROM SingleValue WHERE parent='InventorySettings'")
        k, _, err = jalan("csv-barang", "--db", dua, "--masuk", brg, "--keluar", keluar)
        self.assertEqual(k, 2)
        self.assertIn("tidak bisa dipastikan", err)
        self.assertIn("Titipan Barang Masuk - 2117.000", err)
        # Inventory Settings kosong tapi akun bernama baku ada -> dipakai + diberi peringatan
        kosong = self.salin_db("srbnb-kosong.books.db", "DELETE FROM SingleValue WHERE parent='InventorySettings'")
        k, out, _ = jalan("csv-barang", "--db", kosong, "--masuk", brg, "--keluar", keluar)
        self.assertEqual(k, 0)
        self.assertIn("'Stock Received But Not Billed' belum diisi", out)
        self.assertIn("'Stock In Hand' belum diisi", out)
        # tanpa --db: wajib disebut, tidak diam-diam memakai HPP
        k, _, err = jalan("csv-barang", "--masuk", brg, "--keluar", keluar, "--akun-penjualan", "Sales",
                          "--akun-pembelian", "Cost of Goods Sold")
        self.assertEqual(k, 2)
        self.assertIn("--akun-pembelian-stok", err)

    def laba_setelah_beli_jual(self, akun_beli_item, nama_db):
        """Tiru posting Frappe v0.36.0 untuk 1 barang berstok: beli 10 x 50.000, terima barang, jual 4 x 85.000, kirim."""
        p = os.path.join(self.tmp, nama_db)
        buat_db_contoh.buat(p)
        c = sqlite3.connect(p)
        c.execute("DELETE FROM AccountingLedgerEntry")
        c.execute("UPDATE Item SET expenseAccount=? WHERE name='Kopi Arabika 250g'", (akun_beli_item,))
        n = [0]

        def ale(tgl, akun, d, k, ref):
            n[0] += 1
            c.execute("INSERT INTO AccountingLedgerEntry (name, date, account, debit, credit, referenceType, referenceName, "
                      "reverted, createdBy, modifiedBy, created, modified) VALUES (?,?,?,?,?,?,?,0,'a','a','x','x')",
                      (f"T{n[0]}", tgl + "T00:00:00.000Z", akun, f"{d:.11f}", f"{k:.11f}", "X", ref))
        inv = "Persediaan Barang - 1141.000"
        srbnb = "Stock Diterima Tapi Tidak Ditagih - 2115.000"
        hpp = "HPP Pembelian - 4210.000"
        # PurchaseInvoice.getPosting: debit(item.account = expenseAccount barang), credit(akun utang)
        ale("2026-09-02", akun_beli_item, 500000, 0, "PINV-9")
        ale("2026-09-02", "Hutang Dagang Dalam Negeri - 2111.001", 0, 500000, "PINV-9")
        # PurchaseReceipt (StockTransfer.getPosting): debit stockInHand, credit stockReceivedButNotBilled
        ale("2026-09-02", inv, 500000, 0, "PREC-9")
        ale("2026-09-02", srbnb, 0, 500000, "PREC-9")
        # SalesInvoice: debit piutang, credit penjualan
        ale("2026-09-10", "Piutang Dagang - 1131.0010", 340000, 0, "SINV-9")
        ale("2026-09-10", "Penjualan - 4110.000", 0, 340000, "SINV-9")
        # Shipment: debit costOfGoodsSold, credit stockInHand (4 x 50.000)
        ale("2026-09-10", hpp, 200000, 0, "SHPM-9")
        ale("2026-09-10", inv, 0, 200000, "SHPM-9")
        c.commit()
        c.close()
        return jalan("laba-rugi", "--db", p, "--bulan", "2026-09")

    def test_41_laba_rugi_barang_berstok_tidak_hpp_ganda(self):
        # Akun dari csv-barang (v1.0.2) -> laba = 340.000 - 200.000 = 140.000
        brg = self.tulis("stok41.csv", "nama,stok\nKopi Baru,ya\n")
        keluar = os.path.join(self.tmp, "stok41-out.csv")
        jalan("csv-barang", "--db", self.db, "--masuk", brg, "--keluar", keluar)
        akun = dict(zip(self.baca_csv(keluar)[2], self.baca_csv(keluar)[3]))["Item.expenseAccount"]
        k, out, _ = self.laba_setelah_beli_jual(akun, "beli-jual-benar.books.db")
        self.assertEqual(k, 0)
        self.assertIn("HPP Pembelian - 4210.000: Rp 200.000", out)
        self.assertIn("LABA BERSIH: Rp 140.000", out)
        self.assertNotIn("PERINGATAN", out)
        # Perilaku v1.0.1 (akun HPP untuk barang berstok) -> HPP ganda 700.000, rugi; skill kini memperingatkan
        k, out, _ = self.laba_setelah_beli_jual("HPP Pembelian - 4210.000", "beli-jual-salah.books.db")
        self.assertIn("HPP Pembelian - 4210.000: Rp 700.000", out)
        self.assertIn("RUGI BERSIH: -Rp 360.000", out)
        self.assertIn("PERINGATAN: 1 barang berstok memakai akun pembelian HPP (Kopi Arabika 250g)", out)

    def test_42_piutang_memperhitungkan_kredit_retur(self):
        # Retur SINV-1009 atas SINV-1003 (1 x 85.000 + PPN 9.350) dengan outstanding -94.350 seperti file asli
        p = self.salin_db("kredit.books.db",
                          "INSERT INTO SalesInvoice (name, numberSeries, party, account, date, netTotal, grandTotal, baseGrandTotal, "
                          "outstandingAmount, exchangeRate, submitted, cancelled, returnAgainst, createdBy, modifiedBy, created, modified) "
                          "VALUES ('SINV-1009','SINV-','Warung Bu Sari','Piutang Dagang - 1131.0010','2026-09-26T03:00:00.000Z',"
                          "'-85000.00000000000','-94350.00000000000','-94350.00000000000','-94350.00000000000',1,1,0,'SINV-1003',"
                          "'a','a','x','x')",
                          "INSERT INTO SalesInvoice (name, numberSeries, party, account, date, netTotal, grandTotal, baseGrandTotal, "
                          "outstandingAmount, exchangeRate, submitted, cancelled, createdBy, modifiedBy, created, modified) "
                          "VALUES ('SINV-1010','SINV-','CV Maju Jaya','Piutang Dagang - 1131.0010','2026-09-29T03:00:00.000Z',"
                          "'10000.00000000000','10000.00000000000','10000.00000000000','10000.00000000000',1,1,0,'a','a','x','x')")
        k, out, _ = jalan("piutang", "--db", p, "--hari-ini", "2026-09-26")
        self.assertEqual(k, 0)
        self.assertIn("Belum lunas: 5 invoice, total Rp 998.250", out)
        self.assertIn("Kredit retur belum dikembalikan/dipotong: 1 nota retur, total -Rp 94.350", out)
        self.assertIn("SINV-1009 atas SINV-1003 | Warung Bu Sari", out)
        # sama dengan Party.outstandingAmount Frappe: jumlah outstanding semua invoice final
        self.assertIn("PIUTANG BERSIH (setelah kredit retur, sama dengan saldo pihak di Frappe Books): Rp 903.900", out)
        self.assertIn("SINV-1010 | CV Maju Jaya | tgl 29 Sep 2026 | sisa Rp 10.000 | jatuh tempo 29 Okt 2026 | tanggal invoice setelah hari ini", out)
        c = sqlite3.connect(p)
        frappe = sum(Decimal(r[0]) for r in c.execute("SELECT outstandingAmount FROM SalesInvoice WHERE submitted=1 AND cancelled=0"))
        c.close()
        self.assertEqual(frappe, Decimal("903900"))
        k, out, _ = jalan("piutang", "--db", self.db, "--hari-ini", "2026-09-26")
        self.assertNotIn("Kredit retur", out)  # retur lama (outstanding 0) tidak memunculkan kredit


class UjiRevisi103(Dasar):
    """Regresi uji ulang v1.0.2 (Frappe v0.36.0 asli): laba-rugi = P&L Frappe termasuk pengiriman retur."""

    def db_kosong_ledger(self, nama):
        p = os.path.join(self.tmp, nama)
        buat_db_contoh.buat(p)
        c = sqlite3.connect(p)
        c.execute("DELETE FROM AccountingLedgerEntry")
        c.commit()
        return p, c

    def test_43_laba_rugi_sama_dengan_pl_frappe_skenario_grosir(self):
        # Buku besar skenario penguji 09 (Grosir Uji v102). P&L Frappe asli: Penjualan 985.000, Service 25.000,
        # HPP -850.000, beban 100.000, Total Profit 60.000.
        p, c = self.db_kosong_ledger("grosir.books.db")
        c.execute("INSERT INTO Account (name, rootType, accountType, isGroup, lft, rgt, createdBy, modifiedBy, created, modified) "
                  "VALUES ('Biaya Sewa Gudang - 5110.015','Expense',NULL,0,95,96,'a','a','x','x')")
        pj, sv, hpp, inv = ("Penjualan - 4110.000", "Pendapatan Service - 4310.000", "HPP Pembelian - 4210.000",
                            "Persediaan Barang - 1141.000")
        baris = [("2026-09-03", "PINV-1002", hpp, 50000, 0),
                 ("2026-09-05", "SINV-1001", pj, 0, 591000), ("2026-09-10", "SINV-1002", pj, 0, 220000),
                 ("2026-09-10", "SINV-1002", sv, 0, 25000), ("2026-09-15", "SINV-1003", pj, 0, 246000),
                 ("2026-09-05", "SHPM-1001", hpp, 492000, 0), ("2026-09-15", "SHPM-1002", hpp, 200000, 0),
                 ("2026-09-10", "SHPM-1004", hpp, 180000, 0),
                 ("2026-09-30", "SINV-1005", pj, -72000, 0),                                  # retur invoice
                 ("2026-09-30", "SHPM-1005", inv, -72000, 0), ("2026-09-30", "SHPM-1005", hpp, 0, -72000),  # retur kirim
                 ("2026-09-25", "JV-1001", "Biaya Sewa Gudang - 5110.015", 100000, 0),
                 ("2026-10-01", "SHPM-1003", hpp, 64000, 0), ("2026-10-01", "SINV-1004", pj, 0, 77000)]
        for i, (tg, ref, ak, d, k) in enumerate(baris):
            c.execute("INSERT INTO AccountingLedgerEntry (name, date, account, debit, credit, referenceType, referenceName, "
                      "reverted, createdBy, modifiedBy, created, modified) VALUES (?,?,?,?,?,?,?,0,'a','a','x','x')",
                      (f"G{i}", tg + "T00:00:00.000Z", ak, f"{d:.11f}", f"{k:.11f}", "X", ref))
        c.commit()
        c.close()
        k, out, _ = jalan("laba-rugi", "--db", p, "--bulan", "2026-09")
        self.assertEqual(k, 0)
        self.assertIn("Penjualan - 4110.000: Rp 985.000", out)
        self.assertIn("Pendapatan Service - 4310.000: Rp 25.000", out)
        self.assertIn("HPP Pembelian - 4210.000: Rp 850.000", out)
        self.assertIn("LABA BERSIH: Rp 60.000", out)
        self.assertIn("SHPM-1005, SINV-1005", out)
        k, out, _ = jalan("laba-rugi", "--db", p, "--dari", "2026-09-01", "--sampai", "2026-10-01")
        self.assertIn("HPP Pembelian - 4210.000: Rp 914.000", out)
        self.assertIn("LABA BERSIH: Rp 73.000", out)  # 985.000+77.000+25.000-914.000-100.000 (tanpa jasa SINV-1006)

    def test_44_penjualan_belum_dibayar_memakai_kredit_retur(self):
        p = os.path.join(self.tmp, "kredit44.books.db")
        shutil.copy(self.db, p)
        c = sqlite3.connect(p)
        c.execute("UPDATE SalesInvoice SET outstandingAmount='-150000.00000000000' WHERE name='SINV-1008'")
        c.commit()
        c.close()
        k, out, _ = jalan("penjualan", "--db", p, "--bulan", "2026-09")
        self.assertIn("TOTAL               : Rp 933.050", out)
        self.assertIn("Belum dibayar: Rp 333.050 (sudah dikurangi kredit retur -Rp 150.000)", out)
        self.assertIn("Terbayar (bersih)   : Rp 600.000", out)  # = kas masuk 300.000 (SINV-1002) + 300.000 (SINV-1003)
        k, out2, _ = jalan("penjualan", "--db", self.db, "--bulan", "2026-09")
        self.assertIn("Belum dibayar: Rp 483.050", out2)
        self.assertNotIn("kredit retur -Rp", out2)

    def test_45_laporan_harian_hari_retur(self):
        k, out, _ = jalan("laporan-harian", "--db", self.db, "--tanggal", "2026-09-05", "--hari-ini", "2026-09-26")
        self.assertEqual(k, 0)
        self.assertIn("Penjualan final: 0 invoice, Rp 0", out)
        self.assertIn("Retur penjualan: 1 nota, -Rp 150.000 -> penjualan bersih hari ini -Rp 150.000", out)
        k, out, _ = jalan("laporan-harian", "--db", self.db, "--tanggal", "2026-09-06", "--hari-ini", "2026-09-26")
        self.assertIn("Kemarin hanya ada retur (-Rp 150.000).", out)

    def test_46_pajak_awalan_tunggal(self):
        masuk = self.tulis("pajak46.csv", "No Nota;Tanggal;Pelanggan;Barang;Jumlah;Harga;Pajak\n"
                                          "N-1;27/09/2026;Toko Sinar Abadi;Kopi Arabika 250g;1;85000;PPN\n")
        keluar = os.path.join(self.tmp, "pajak46-out.csv")
        k, out, _ = jalan("csv-transaksi", "--db", self.db, "--masuk", masuk, "--keluar", keluar)
        self.assertEqual(k, 0, out)
        self.assertIn("pajak 'PPN' dianggap 'PPN 11% (12% x 11/12)'", out)
        self.assertEqual(dict(zip(self.baca_csv(keluar)[2], self.baca_csv(keluar)[3]))["SalesInvoiceItem.tax"],
                         "PPN 11% (12% x 11/12)")


if __name__ == "__main__":
    try:
        unittest.main(verbosity=2)
    finally:
        shutil.rmtree(RUMAH_KOSONG, ignore_errors=True)
