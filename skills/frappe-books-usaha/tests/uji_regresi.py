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


def jalan(*arg):
    r = subprocess.run([sys.executable, SKRIP] + list(arg), capture_output=True, text=True, encoding="utf-8")
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
        self.assertEqual(fb.tanggal_lokal("2026-08-31T15:59:00.000Z", fb.offset_zona("WIT")).isoformat(), "2026-08-31")
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
        self.assertIn("HPP Pembelian: Rp 250.000", out)
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
        self.assertIn("PPN 11% (12% x 11/12): 11% ke akun Hutang Pajak", out)
        self.assertIn("SATUAN (UOM): Gram, Hari, Jam, Kg, Meter, Unit", out)
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
        self.assertEqual(rows[2], ["Party.name", "Party.role", "Party.email", "Party.phone", "Party.taxId"])
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
                         ("95000", "Penjualan", "HPP Pembelian", "1"))
        self.assertEqual((b2["Item.itemType"], b2["Item.rate"], b2["Item.unit"], b2["Item.incomeAccount"], b2["Item.trackItem"]),
                         ("Service", "1500000", "Jam", "Pendapatan Service", "0"))
        self.assertEqual(len(rows), 5)  # Kopi Arabika sudah ada
        salah = self.tulis("brg2.csv", "nama,satuan\nSusu,Liter\n")
        k, out, _ = jalan("csv-barang", "--db", self.db, "--masuk", salah, "--keluar", keluar + "2")
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
        self.assertEqual(rows[2][:4], ["SalesInvoice.name", "SalesInvoice.party", "SalesInvoice.account", "SalesInvoice.date"])
        d = [dict(zip(rows[2], r)) for r in rows[3:]]
        self.assertEqual(len(d), 4)
        self.assertEqual(d[0]["SalesInvoice.name"], "IMPOR-N-01")
        self.assertEqual(d[1]["SalesInvoice.party"], "Toko Sinar Abadi")  # huruf disamakan dengan data
        self.assertEqual(d[2]["SalesInvoiceItem.account"], "Pendapatan Service")  # akun dari data barang
        self.assertEqual(d[3]["SalesInvoice.date"], "2026-09-28")
        self.assertEqual(d[3]["SalesInvoiceItem.rate"], "150000")
        self.assertEqual(d[0]["SalesInvoice.account"], "Piutang Dagang")

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
                          "--akun-penjualan", "Pendapatan")
        self.assertEqual(k, 2)
        self.assertIn("akun grup", err)


if __name__ == "__main__":
    unittest.main(verbosity=2)
