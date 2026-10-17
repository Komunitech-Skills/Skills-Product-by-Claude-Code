#!/usr/bin/env python3
"""Uji regresi buku-stok. Jalankan: python3 scripts/uji_regresi.py  (Windows: py scripts\\uji_regresi.py)

Semua uji memakai database sementara (tempfile), tidak menyentuh ~/KomunitechData.
"""
import contextlib
import io
import json
import os
import re
import shutil
import sqlite3
import sys
import tempfile
import time
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import stok  # noqa: E402


class Dasar(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="bukustok-uji-"))
        self.db = self.tmp / "data" / "stok.db"
        self._env = os.environ.pop("KOMUNITECH_STOK_DB", None)
        self.run_ok("init", "--ya")

    def tearDown(self):
        if self._env is not None:
            os.environ["KOMUNITECH_STOK_DB"] = self._env
        shutil.rmtree(self.tmp, ignore_errors=True)

    def cli(self, *argv):
        out = io.StringIO()
        err = io.StringIO()
        argv = list(argv) + ["--db", str(self.db), "--json"]
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            kode = stok.main(argv)
        teks = out.getvalue()
        data = json.loads(teks) if teks.strip().startswith("{") else {"_teks": teks}
        return kode, data

    def run_ok(self, *argv):
        kode, data = self.cli(*argv)
        self.assertEqual(kode, 0, "perintah gagal: %s -> %s" % (argv, data))
        return data

    def run_gagal(self, *argv):
        kode, data = self.cli(*argv)
        self.assertEqual(kode, 1, "seharusnya gagal: %s -> %s" % (argv, data))
        self.assertFalse(data.get("ok"))
        return data

    def tulis(self, nama, isi, enc="utf-8"):
        p = self.tmp / nama
        p.write_text(isi, encoding=enc)
        return str(p)

    def produk(self, sku):
        c = sqlite3.connect(str(self.db))
        c.row_factory = sqlite3.Row
        r = c.execute("SELECT * FROM produk WHERE sku=?", (sku,)).fetchone()
        c.close()
        return r

    def konsisten(self):
        """Stok di tabel produk harus sama dengan jumlah semua mutasi."""
        c = sqlite3.connect(str(self.db))
        beda = c.execute("SELECT p.sku, p.stok, COALESCE(SUM(m.qty),0) FROM produk p LEFT JOIN mutasi m "
                         "ON m.produk_id=p.id GROUP BY p.id HAVING ABS(p.stok - COALESCE(SUM(m.qty),0)) > 0.0001").fetchall()
        c.close()
        self.assertEqual(beda, [], "stok tidak konsisten dengan mutasi")

    def tambah(self, sku, stok_awal="0", beli="10000", jual="15000", smin="0", lokasi="", nama=None, varian=""):
        self.run_ok("produk", "tambah", "--sku", sku, "--nama", nama or ("Produk " + sku), "--varian", varian,
                    "--harga-beli", beli, "--harga-jual", jual, "--stok-min", smin, "--lokasi", lokasi,
                    "--stok-awal", stok_awal, "--ya")


class UjiHPP(Dasar):
    def test_hpp_rata_rata_tertimbang_manual(self):
        # Hitungan manual:
        #  masuk 10 @ 10.000 -> HPP 10.000
        #  masuk  5 @ 13.000 -> (100.000 + 65.000) / 15 = 11.000
        #  keluar 6          -> stok 9, HPP tetap 11.000 (nilai 99.000)
        #  masuk  3 @ 12.500 -> (99.000 + 37.500) / 12 = 11.375 ; nilai 136.500
        self.tambah("A", beli="10000")
        self.run_ok("masuk", "--sku", "A", "--qty", "10", "--harga", "10.000", "--ya")
        d = self.run_ok("masuk", "--sku", "A", "--qty", "5", "--harga", "Rp 13.000", "--ya")
        self.assertEqual(d["item"][0]["hpp_sesudah"], 11000)
        self.run_ok("keluar", "--sku", "A", "--qty", "6", "--ya")
        self.assertAlmostEqual(self.produk("A")["hpp"], 11000)
        d = self.run_ok("masuk", "--sku", "A", "--qty", "3", "--harga", "12500", "--ya")
        self.assertAlmostEqual(d["item"][0]["hpp_sesudah"], 11375)
        lap = self.run_ok("laporan", "stok")
        self.assertEqual(lap["nilai_persediaan_total"], 136500)
        self.assertEqual(lap["produk"][0]["stok"], 12)
        self.konsisten()

    def test_hpp_pecahan_dan_pembulatan(self):
        # 3 @ 10.000 + 4 @ 10.001 -> 70.004 / 7 = 10.000,571428... disimpan 10000,5714; nilai 70.004
        self.tambah("B")
        self.run_ok("masuk", "--sku", "B", "--qty", "3", "--harga", "10000", "--ya")
        self.run_ok("masuk", "--sku", "B", "--qty", "4", "--harga", "10001", "--ya")
        self.assertAlmostEqual(self.produk("B")["hpp"], 10000.5714, places=4)
        self.assertEqual(self.run_ok("laporan", "stok")["nilai_persediaan_total"], 70004)

    def test_biaya_tambahan_dibagi_sesuai_nilai(self):
        # Barang X 10 @ 20.000 (200.000) dan Y 20 @ 5.000 (100.000), ongkir 30.000
        # porsi X = 30.000 x 200/300 = 20.000 -> +2.000/pcs -> HPP 22.000
        # porsi Y = 10.000 -> +500/pcs -> HPP 5.500
        self.tambah("X")
        self.tambah("Y")
        f = self.tulis("nota.csv", "SKU;Qty;Harga\nX;10;20.000\nY;20;5.000\n")
        d = self.run_ok("masuk", "--file", f, "--biaya-tambahan", "Rp 30.000", "--ref", "NOTA-01", "--ya")
        self.assertEqual(d["total_nilai"], 330000)
        self.assertAlmostEqual(self.produk("X")["hpp"], 22000)
        self.assertAlmostEqual(self.produk("Y")["hpp"], 5500)

    def test_masuk_setelah_stok_minus_pakai_harga_baru(self):
        self.tambah("C", stok_awal="2", beli="9000")
        self.run_ok("keluar", "--sku", "C", "--qty", "5", "--izinkan-minus", "--ya")
        self.run_ok("masuk", "--sku", "C", "--qty", "10", "--harga", "12000", "--ya")
        self.assertAlmostEqual(self.produk("C")["hpp"], 12000)
        self.assertAlmostEqual(self.produk("C")["stok"], 7)


class UjiKeamanan(Dasar):
    def test_pratinjau_tidak_menyimpan(self):
        self.tambah("A", stok_awal="10")
        d = self.run_ok("keluar", "--sku", "A", "--qty", "3")
        self.assertEqual(d["mode"], "pratinjau")
        self.assertTrue(d["perlu_konfirmasi"])
        self.assertEqual(d["item"][0]["stok_sesudah"], 7)
        self.assertAlmostEqual(self.produk("A")["stok"], 10)
        d = self.run_ok("produk", "tambah", "--sku", "Z", "--nama", "Z")
        self.assertIsNone(self.produk("Z"))

    def test_stok_negatif_ditolak_lalu_diperingatkan(self):
        self.tambah("A", stok_awal="3")
        e = self.run_gagal("keluar", "--sku", "A", "--qty", "5", "--ya")
        self.assertIn("tidak cukup", e["error"])
        self.assertAlmostEqual(self.produk("A")["stok"], 3)
        d = self.run_ok("keluar", "--sku", "A", "--qty", "5", "--izinkan-minus", "--ya")
        self.assertTrue(d["peringatan"])
        self.assertAlmostEqual(self.produk("A")["stok"], -2)
        lap = self.run_ok("laporan", "menipis")
        self.assertEqual(lap["produk"][0]["status"], "MINUS")
        self.assertEqual(self.run_ok("laporan", "stok")["nilai_persediaan_total"], 0)

    def test_sku_tidak_ada_dan_input_buruk(self):
        self.tambah("KAOS-M")
        e = self.run_gagal("keluar", "--sku", "KAOS", "--qty", "1", "--ya")
        self.assertIn("KAOS-M", e["saran"])
        self.run_gagal("masuk", "--sku", "KAOS-M", "--qty", "abc", "--ya")
        self.run_gagal("masuk", "--sku", "KAOS-M", "--qty", "0", "--ya")
        self.run_gagal("masuk", "--sku", "KAOS-M", "--qty", "-5", "--ya")
        self.run_gagal("masuk", "--sku", "KAOS-M", "--qty", "2", "--harga", "15.000.00", "--ya")
        self.run_gagal("masuk", "--sku", "KAOS-M", "--qty", "2", "--tanggal", "31/02/2026", "--ya")
        self.run_gagal("produk", "tambah", "--sku", "KAOS-M", "--nama", "dobel", "--ya")
        self.run_gagal("keluar", "--sku", "KAOS-M", "--qty", "1", "--jenis", "rusak", "--ya")  # tanpa alasan

    def test_database_belum_ada_dan_bukan_database(self):
        kode, d = 0, None
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            kode = stok.main(["laporan", "stok", "--db", str(self.tmp / "tidak-ada.db"), "--json"])
        self.assertEqual(kode, 1)
        e = json.loads(out.getvalue())
        self.assertIn("belum disiapkan", e["error"])          # bahasa awam, tanpa path/perintah (v1.1.7)
        self.assertIn("init", e["langkah_agen"])                # petunjuk teknis hanya untuk agent
        palsu = self.tmp / "palsu.db"
        palsu.write_text("bukan sqlite")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            kode = stok.main(["info", "--db", str(palsu), "--json"])
        self.assertEqual(kode, 1)

    def test_path_dari_env(self):
        lain = self.tmp / "folder lain" / "toko.db"
        os.environ["KOMUNITECH_STOK_DB"] = str(lain)
        try:
            out = io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(stok.main(["init", "--ya", "--json"]), 0)
            self.assertTrue(lain.is_file())
        finally:
            del os.environ["KOMUNITECH_STOK_DB"]
        os.environ["KOMUNITECH_DATA"] = str(self.tmp / "datafolder")
        try:
            import argparse
            self.assertEqual(stok.path_db(argparse.Namespace(db=None)), self.tmp / "datafolder" / "stok.db")
        finally:
            del os.environ["KOMUNITECH_DATA"]


class UjiOpname(Dasar):
    def test_opname_selisih_alasan_backup(self):
        self.tambah("A", stok_awal="20", beli="10000")
        self.tambah("B", stok_awal="5", beli="4000")
        d = self.run_ok("opname", "--hitung", "A=18", "--hitung", "B=6")
        self.assertEqual(d["mode"], "pratinjau")
        self.assertEqual(sorted(d["sku_tanpa_alasan"]), ["A", "B"])
        e = self.run_gagal("opname", "--hitung", "A=18", "--hitung", "B=6", "--ya")
        self.assertIn("tanpa alasan", e["error"])
        self.assertAlmostEqual(self.produk("A")["stok"], 20)
        d = self.run_ok("opname", "--hitung", "A=18", "--hitung", "B=6", "--alasan", "hilang / salah catat", "--ya")
        self.assertEqual(d["nilai_kurang"], -20000)
        self.assertEqual(d["nilai_lebih"], 4000)
        self.assertEqual(d["nilai_bersih"], -16000)
        self.assertTrue(Path(d["backup"]).is_file())
        self.assertAlmostEqual(self.produk("A")["stok"], 18)
        self.assertAlmostEqual(self.produk("B")["stok"], 6)
        self.assertAlmostEqual(self.produk("A")["hpp"], 10000)  # opname tidak mengubah HPP
        m = self.run_ok("laporan", "mutasi", "--sku", "A")
        self.assertEqual(m["per_produk"][0]["opname"], -2)
        self.konsisten()

    def test_opname_dari_file_dan_sku_ganda(self):
        self.tambah("A", stok_awal="10")
        f = self.tulis("hitung.csv", "Kode Barang,Stok Fisik,Keterangan\nA,\"9\",pecah\n")
        d = self.run_ok("opname", "--file", f, "--ya")
        self.assertEqual(d["hasil"][0]["selisih"], -1)
        self.run_gagal("opname", "--hitung", "A=1", "--hitung", "a=2")
        f2 = self.tulis("rusak.csv", "Kode,Fisik\nA,sepuluh\n")
        self.run_gagal("opname", "--file", f2)

    def test_opname_memperhitungkan_pesanan_belum_dikemas(self):
        self.tambah("A", stok_awal="10")
        f = self.tulis("p.csv", "No. Pesanan,Status Pesanan,Nomor Referensi SKU,Jumlah\nX1,Perlu Dikirim,A,3\n")
        self.run_ok("impor-pesanan", f, "--ya")
        self.assertAlmostEqual(self.produk("A")["stok"], 7)
        # Barang untuk X1 masih di rak: hitungan fisik 10 = cocok
        d = self.run_ok("opname", "--hitung", "A=10")
        self.assertEqual(d["hasil"][0]["selisih"], 0)
        self.assertEqual(d["hasil"][0]["termasuk_pesanan_belum_dikemas"], 3)


SHOPEE = ("No. Pesanan,Status Pesanan,No. Resi,Opsi Pengiriman,Waktu Pesanan Dibuat,Nomor Referensi SKU,"
          "Nama Produk,Nama Variasi,Harga Setelah Diskon,Jumlah\n")


class UjiImpor(Dasar):
    def setUp(self):
        super().setUp()
        self.tambah("KAOS-M", stok_awal="20", beli="35000", lokasi="A1")
        self.tambah("TOTE", stok_awal="10", beli="18500", lokasi="B1")

    def test_impor_ganda_dicegah(self):
        f = self.tulis("s1.csv", SHOPEE +
                       "P1,Perlu Dikirim,R1,SPX,2026-09-20 10:00,KAOS-M,Kaos,M,\"59.000\",2\n"
                       "P1,Perlu Dikirim,R1,SPX,2026-09-20 10:00,TOTE,Tote,,\"35.000\",1\n"
                       "P2,Selesai,R2,J&T,2026-09-19 10:00,KAOS-M,Kaos,M,\"59.000\",1\n")
        d = self.run_ok("impor-pesanan", f)
        self.assertEqual(d["platform"], "shopee")
        self.assertEqual(d["pemetaan_kolom"]["SKU"], "Nomor Referensi SKU")
        self.assertAlmostEqual(self.produk("KAOS-M")["stok"], 20)  # pratinjau
        d = self.run_ok("impor-pesanan", f, "--ya")
        self.assertEqual(d["pesanan_baru"], 2)
        self.assertTrue(Path(d["backup"]).is_file())
        self.assertAlmostEqual(self.produk("KAOS-M")["stok"], 17)
        d = self.run_ok("impor-pesanan", f, "--ya")
        self.assertEqual(d["pesanan_baru"], 0)
        self.assertEqual(d["pesanan_sudah_pernah_diimpor"], 2)
        self.assertTrue(any("Tidak ada pesanan baru" in p for p in d["peringatan"]))
        self.assertAlmostEqual(self.produk("KAOS-M")["stok"], 17)
        # file lain yang tumpang tindih: hanya P3 yang baru; nomor dengan apostrof Excel tetap dikenali
        f2 = self.tulis("s2.csv", SHOPEE +
                        "'P2,Selesai,R2,J&T,2026-09-19,KAOS-M,Kaos,M,59000,1\n"
                        "P3,Perlu Dikirim,R3,SPX,2026-09-21,KAOS-M,Kaos,M,59000,4\n")
        d = self.run_ok("impor-pesanan", f2, "--ya")
        self.assertEqual(d["pesanan_baru"], 1)
        self.assertAlmostEqual(self.produk("KAOS-M")["stok"], 13)
        self.konsisten()

    def test_batal_retur_belum_bayar_diabaikan(self):
        f = self.tulis("s.csv", SHOPEE +
                       "B1,Batal,,SPX,2026-09-20,KAOS-M,Kaos,M,59000,5\n"
                       "B2,Pembatalan: Dibatalkan oleh pembeli,,SPX,2026-09-20,KAOS-M,Kaos,M,59000,1\n"
                       "B3,Pengembalian Barang/Dana,,SPX,2026-09-20,KAOS-M,Kaos,M,59000,1\n"
                       "B4,Belum Bayar,,SPX,2026-09-20,KAOS-M,Kaos,M,59000,1\n"
                       "B5,Cancelled,,SPX,2026-09-20,TOTE,Tote,,35000,2\n"
                       "B6,Perlu Dikirim,R6,SPX,2026-09-20,TOTE,Tote,,35000,1\n")
        d = self.run_ok("impor-pesanan", f, "--ya")
        self.assertEqual(d["pesanan_baru"], 1)
        self.assertEqual(d["diabaikan_batal"], 3)
        self.assertEqual(d["diabaikan_retur"], 1)
        self.assertEqual(d["diabaikan_belum_bayar"], 1)
        self.assertAlmostEqual(self.produk("KAOS-M")["stok"], 20)
        self.assertAlmostEqual(self.produk("TOTE")["stok"], 9)
        # Pesanan belum bayar tidak dicatat, jadi setelah dibayar tetap bisa diimpor
        f2 = self.tulis("s2.csv", SHOPEE + "B4,Perlu Dikirim,R4,SPX,2026-09-21,KAOS-M,Kaos,M,59000,1\n")
        self.assertEqual(self.run_ok("impor-pesanan", f2, "--ya")["pesanan_baru"], 1)

    def test_pesanan_batal_setelah_diimpor_stok_kembali(self):
        self.run_ok("masuk", "--sku", "KAOS-M", "--qty", "10", "--harga", "38000", "--ya")  # HPP 36.000
        f = self.tulis("s.csv", SHOPEE + "C1,Perlu Dikirim,R1,SPX,2026-09-20,KAOS-M,Kaos,M,59000,3\n")
        self.run_ok("impor-pesanan", f, "--ya")
        self.assertAlmostEqual(self.produk("KAOS-M")["stok"], 27)
        f2 = self.tulis("s2.csv", SHOPEE + "C1,Batal,R1,SPX,2026-09-20,KAOS-M,Kaos,M,59000,3\n")
        d = self.run_ok("impor-pesanan", f2, "--ya")
        self.assertEqual(d["pesanan_lama_kini_batal_stok_dikembalikan"], ["C1"])
        self.assertAlmostEqual(self.produk("KAOS-M")["stok"], 30)
        self.assertAlmostEqual(self.produk("KAOS-M")["hpp"], 36000)
        # impor ulang file batal tidak mengembalikan stok dua kali
        self.run_ok("impor-pesanan", f2, "--ya")
        self.assertAlmostEqual(self.produk("KAOS-M")["stok"], 30)
        self.assertEqual(self.run_ok("picking")["jumlah_pesanan"], 0)
        self.konsisten()

    def test_sku_tak_dikenal_dan_cocok_nama(self):
        f = self.tulis("s.csv", SHOPEE +
                       "D1,Perlu Dikirim,R1,SPX,2026-09-20,SKU-ASING,Topi Baru,,50000,2\n"
                       "D2,Perlu Dikirim,R2,SPX,2026-09-20,,Produk TOTE,,35000,1\n")
        d = self.run_ok("impor-pesanan", f)
        self.assertEqual(d["sku_tak_dikenal"][0]["sku_marketplace"], "SKU-ASING")
        self.assertEqual(d["barang_keluar"][0]["sku"], "TOTE")  # cocok lewat nama produk
        e = self.run_gagal("impor-pesanan", f, "--ya")
        self.assertIn("belum terdaftar", e["error"])
        self.assertAlmostEqual(self.produk("TOTE")["stok"], 10)
        self.run_ok("impor-pesanan", f, "--ya", "--lewati-tak-dikenal")
        self.assertAlmostEqual(self.produk("TOTE")["stok"], 9)
        pk = self.run_ok("picking")
        self.assertTrue(any(not a["terdaftar"] for a in pk["daftar_ambil"]))

    def test_tiktok_baris_keterangan_dan_pemetaan_manual(self):
        f = self.tulis("tt.csv",
                       "Order ID,Order Status,Seller SKU,Product Name,Variation,Quantity,Sku Quantity of return,Tracking ID,Shipping Provider Name,Created Time\n"
                       "Platform unique order ID.,Order status,Seller SKU,Product name,Variation,Quantity,Return qty,Tracking,Provider,Created\n"
                       "5770001,AWAITING_SHIPMENT,KAOS-M,Kaos,M,2,0,JX1,J&T,20/09/2026 10:11:00\n"
                       "5770002,Shipped,TOTE,Tote,,1,0,JX2,J&T,20/09/2026 11:00:00\n"
                       "5770003,Unpaid,TOTE,Tote,,1,0,,J&T,20/09/2026 12:00:00\n")
        d = self.run_ok("impor-pesanan", f)
        self.assertEqual(d["platform"], "tiktok")
        self.assertEqual(d["pemetaan_kolom"]["Jumlah"], "Quantity")
        self.assertEqual(d["baris_dilewati"]["qty_tidak_valid"], 1)
        self.assertEqual(d["pesanan_baru"], 2)
        # pemetaan manual mengganti deteksi (kolom retur berisi 0 semua -> tidak ada baris sah -> ditolak)
        e = self.run_gagal("impor-pesanan", f, "--kolom-qty", "Sku Quantity of return")
        self.assertEqual(e["pemetaan"]["qty"], "Sku Quantity of return")
        d = self.run_ok("impor-pesanan", f, "--kolom-resi", "-")
        self.assertNotIn("No. resi", d["pemetaan_kolom"])
        self.run_gagal("impor-pesanan", f, "--kolom-qty", "Kolom Tidak Ada")
        self.run_ok("impor-pesanan", f, "--ya")
        pk = self.run_ok("picking")
        self.assertEqual(pk["jumlah_pesanan"], 1)  # hanya AWAITING_SHIPMENT
        self.assertEqual(pk["urutan_pesanan"][0]["resi"], "JX1")

    def test_xlsx_langsung_dibaca(self):
        baris = [["No. Pesanan", "Status Pesanan", "Nomor Referensi SKU", "Jumlah"],
                 ["X1", "Perlu Dikirim", "KAOS-M", 2], ["X2", "Perlu Dikirim", "TOTE", 1]]
        shared = []
        sel = []
        for ri, r in enumerate(baris, start=1):
            cells = []
            for ci, v in enumerate(r):
                ref = "%s%d" % ("ABCD"[ci], ri)
                if isinstance(v, str):
                    shared.append(v)
                    cells.append('<c r="%s" t="s"><v>%d</v></c>' % (ref, len(shared) - 1))
                else:
                    cells.append('<c r="%s"><v>%s</v></c>' % (ref, float(v)))
            sel.append('<row r="%d">%s</row>' % (ri, "".join(cells)))
        ns = 'xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"'
        p = self.tmp / "pesanan.xlsx"
        with zipfile.ZipFile(p, "w") as z:
            z.writestr("xl/workbook.xml", '<workbook %s xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
                       '<sheets><sheet name="orders" sheetId="1" r:id="rId1"/></sheets></workbook>' % ns)
            z.writestr("xl/_rels/workbook.xml.rels", '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                       '<Relationship Id="rId1" Target="worksheets/sheet1.xml" Type="x"/></Relationships>')
            z.writestr("xl/sharedStrings.xml", '<sst %s>%s</sst>' % (ns, "".join("<si><t>%s</t></si>" % s for s in shared)))
            z.writestr("xl/worksheets/sheet1.xml", '<worksheet %s><sheetData>%s</sheetData></worksheet>' % (ns, "".join(sel)))
        d = self.run_ok("impor-pesanan", str(p), "--ya")
        self.assertEqual(d["jenis_file"], "xlsx")
        self.assertEqual(d["pesanan_baru"], 2)
        self.assertAlmostEqual(self.produk("KAOS-M")["stok"], 18)

    def test_picking_urutan_dan_tandai_dikemas(self):
        f = self.tulis("s.csv", SHOPEE +
                       "E1,Perlu Dikirim,SPX2,SPX,2026-09-20,KAOS-M,Kaos,M,59000,2\n"
                       "E2,Perlu Dikirim,JNT1,J&T,2026-09-20,TOTE,Tote,,35000,1\n"
                       "E3,Perlu Dikirim,SPX1,SPX,2026-09-20,KAOS-M,Kaos,M,59000,1\n"
                       "E3,Perlu Dikirim,SPX1,SPX,2026-09-20,TOTE,Tote,,35000,1\n"
                       "E4,Sedang Dikirim,SPX9,SPX,2026-09-19,TOTE,Tote,,35000,1\n")
        self.run_ok("impor-pesanan", f, "--ya")
        csv1, csv2 = str(self.tmp / "ambil.csv"), str(self.tmp / "urutan.csv")
        pk = self.run_ok("picking", "--csv", csv1, "--csv-pesanan", csv2)
        self.assertEqual(pk["jumlah_pesanan"], 3)
        ambil = {a["sku"]: a for a in pk["daftar_ambil"]}
        self.assertEqual(ambil["KAOS-M"]["qty"], 3)
        self.assertEqual(ambil["KAOS-M"]["jumlah_pesanan"], 2)
        self.assertEqual([a["lokasi"] for a in pk["daftar_ambil"]], ["A1", "B1"])
        self.assertEqual([u["no_pesanan"] for u in pk["urutan_pesanan"]], ["E2", "E3", "E1"])  # J&T dulu, lalu resi SPX1, SPX2
        isi = Path(csv1).read_text(encoding="utf-8-sig")
        self.assertIn("lokasi;sku;nama;qty", isi)
        d = self.run_ok("picking", "--tandai-dikemas")
        self.assertEqual(d["mode"], "pratinjau")
        self.assertEqual(self.run_ok("picking")["jumlah_pesanan"], 3)
        self.run_ok("picking", "--tandai-dikemas", "--ya")
        self.assertEqual(self.run_ok("picking")["jumlah_pesanan"], 0)


class UjiFileRusak(Dasar):
    def setUp(self):
        super().setUp()
        self.tambah("A", stok_awal="10")

    def test_file_rusak_ditolak_dengan_pesan_jelas(self):
        kosong = self.tulis("kosong.csv", "")
        self.assertIn("kosong", self.run_gagal("impor-pesanan", kosong)["error"])
        biner = self.tmp / "gambar.csv"
        biner.write_bytes(b"\x89PNG\r\n\x1a\n\x00\x00\x00IHDR" + bytes(range(256)))
        self.assertIn("biner", self.run_gagal("impor-pesanan", str(biner))["error"])
        lain = self.tulis("lain.csv", "Tanggal,Keterangan,Debit,Kredit\n2026-09-01,Setoran,100000,0\n")
        self.assertIn("tidak dikenali", self.run_gagal("impor-pesanan", lain)["error"])
        xls = self.tmp / "lama.xls"
        xls.write_bytes(b"\xd0\xcf\x11\xe0 bukan xlsx")
        self.assertIn(".xls", self.run_gagal("impor-pesanan", str(xls))["error"])
        xlsx = self.tmp / "rusak.xlsx"
        xlsx.write_bytes(b"PK\x03\x04 terpotong")
        self.assertIn("rusak", self.run_gagal("impor-pesanan", str(xlsx))["error"])
        self.run_gagal("impor-pesanan", str(self.tmp / "tidak-ada.csv"))
        self.assertAlmostEqual(self.produk("A")["stok"], 10)

    def test_baris_rusak_dilewati_dan_dilaporkan(self):
        f = self.tulis("s.csv", SHOPEE +
                       "F1,Perlu Dikirim,R1,SPX,2026-09-20,A,Produk A,,10000,dua\n"
                       "2.40920E+17,Perlu Dikirim,R2,SPX,2026-09-20,A,Produk A,,10000,1\n"
                       "F3,Perlu Dikirim,R3,SPX,2026-09-20,A,Produk A,,10000,1\n"
                       "F3,Perlu Dikirim,R3,SPX,2026-09-20,A,Produk A,,10000,1\n"
                       ",,,,,,,,,\n"
                       "F4,Perlu Dikirim,R4,SPX,2026-09-20,A,Produk A\n"
                       "F5,Status Aneh,R5,SPX,2026-09-20,A,Produk A,,10000,1\n")
        d = self.run_ok("impor-pesanan", f, "--ya")
        self.assertEqual(d["pesanan_baru"], 2)
        self.assertEqual(d["baris_dilewati"]["qty_tidak_valid"], 2)
        self.assertEqual(d["baris_dilewati"]["nomor_pesanan_rusak"], 1)
        self.assertEqual(d["baris_dilewati"]["baris_kembar"], 1)
        self.assertTrue(any("Status Aneh" in p for p in d["peringatan"]))
        self.assertAlmostEqual(self.produk("A")["stok"], 8)

    def test_csv_titik_koma_ansi_dan_judul_bukan_baris_pertama(self):
        isi = ("Laporan Pesanan Toko Maju\nPeriode: September 2026\n\n"
               "Nomor Invoice;Status Terakhir;Nomor SKU;Nama Produk;Jumlah Produk Dibeli;Harga Jual\n"
               "INV/2026/1;Pesanan Selesai;A;Produk A café;3;Rp 15.000,50\n")
        f = self.tmp / "toped.csv"
        f.write_bytes(isi.encode("cp1252"))
        d = self.run_ok("impor-pesanan", str(f), "--ya")
        self.assertEqual(d["platform"], "tokopedia")
        self.assertEqual(d["baris_judul"], 4)
        self.assertEqual(d["pesanan_baru"], 1)
        c = sqlite3.connect(str(self.db))
        harga = c.execute("SELECT harga FROM mutasi WHERE jenis='jual-mp'").fetchone()[0]
        c.close()
        self.assertAlmostEqual(harga, 15000.5)


class UjiAngka(unittest.TestCase):
    def test_format_angka_indonesia(self):
        kasus = {"15000": 15000, "Rp 15.000": 15000, "Rp. 25000": 25000, "IDR 25.000": 25000, "Rp 15.000,-": 15000,
                 "15.000,50": 15000.5, "15,000.50": 15000.5, "1.250.000": 1250000, "12,5": 12.5, "2 pcs": 2,
                 "(15.000)": -15000, "1.000": 1000, "0": 0}
        for teks, harap in kasus.items():
            self.assertAlmostEqual(stok.parse_angka(teks), harap, msg=teks)
        for buruk in ("15.000.00", "15000.500", "1.5E+06", "abc", "", "1-2"):
            self.assertIsNone(stok.parse_angka(buruk), buruk)

    def test_format_rupiah_dan_pembulatan(self):
        self.assertEqual(stok.rp(1250000), "Rp 1.250.000")
        self.assertEqual(stok.rp(-70000), "-Rp 70.000")
        self.assertEqual(stok.bulat_rp(10000.5), 10001)
        self.assertEqual(stok.bulat_rp(10000.49), 10000)
        self.assertEqual(stok.bulat_rp(2.5), 3)
        self.assertEqual(stok.fq(1.5), "1,5")
        self.assertEqual(stok.fq(3.0), "3")

    def test_tanggal(self):
        from datetime import date
        self.assertEqual(stok.parse_tanggal("23/09/2026"), date(2026, 9, 23))
        self.assertEqual(stok.parse_tanggal("2026-09-23 10:11"), date(2026, 9, 23))
        self.assertEqual(stok.parse_tanggal("1 Agustus 2026"), date(2026, 8, 1))
        self.assertEqual(stok.parse_tanggal("46288"), date(2026, 9, 23))
        self.assertIsNone(stok.parse_tanggal("31/02/2026"))

    def test_kategori_status(self):
        k = stok.kategori_status
        self.assertEqual(k("Perlu Dikirim"), "perlu_kirim")
        self.assertEqual(k("Sedang Dikirim"), "dikirim")
        self.assertEqual(k("Selesai"), "selesai")
        self.assertEqual(k("Batal"), "batal")
        self.assertEqual(k("Pengembalian Barang/Dana"), "retur")
        self.assertEqual(k("Pengembalian Ditolak"), "lainnya")
        self.assertEqual(k("Belum Bayar"), "belum_bayar")
        self.assertEqual(k("AWAITING_SHIPMENT".replace("_", " ")), "perlu_kirim")
        self.assertEqual(k(""), "tanpa_status")


class UjiBackup(Dasar):
    def test_backup_restore(self):
        self.tambah("A", stok_awal="10")
        b = self.run_ok("backup", "--label", "Sebelum Lebaran!")
        self.assertTrue(Path(b["backup"]).is_file())
        self.assertIn("sebelum-lebaran", b["backup"])
        self.run_ok("keluar", "--sku", "A", "--qty", "4", "--ya")
        self.tambah("B", stok_awal="1")
        d = self.run_ok("restore", "--dari", b["backup"])
        self.assertEqual(d["mode"], "pratinjau")
        self.assertAlmostEqual(self.produk("A")["stok"], 6)
        d = self.run_ok("restore", "--dari", b["backup"], "--ya")
        self.assertAlmostEqual(self.produk("A")["stok"], 10)
        self.assertIsNone(self.produk("B"))
        self.assertIn("sebelum-restore", d["backup"])
        # Batalkan restore: kembali ke kondisi sebelum restore
        self.run_ok("restore", "--dari", d["backup"], "--ya")
        self.assertAlmostEqual(self.produk("A")["stok"], 6)
        daftar = self.run_ok("backup", "--daftar")
        self.assertGreaterEqual(len(daftar["backup"]), 3)

    def test_restore_file_asing_ditolak(self):
        asing = self.tmp / "asing.db"
        c = sqlite3.connect(str(asing))
        c.execute("CREATE TABLE x(a)")
        c.close()
        self.run_gagal("restore", "--dari", str(asing), "--ya")
        teks = self.tmp / "teks.db"
        teks.write_text("halo")
        self.run_gagal("restore", "--dari", str(teks), "--ya")
        self.run_gagal("restore", "--dari", str(self.tmp / "tidak-ada.db"), "--ya")


class UjiLaporan(Dasar):
    def test_laporan_tidak_laku_menipis_mutasi_csv(self):
        self.run_ok("produk", "tambah", "--sku", "LAKU", "--nama", "Laku", "--harga-beli", "1000", "--harga-jual", "2000",
                    "--stok-min", "25", "--stok-awal", "50", "--tanggal", "2026-07-01", "--ya")
        self.run_ok("produk", "tambah", "--sku", "MATI", "--nama", "Mati", "--harga-beli", "5000", "--stok-awal", "8",
                    "--tanggal", "2026-07-01", "--ya")
        for i in range(1, 31):
            self.run_ok("keluar", "--sku", "LAKU", "--qty", "1", "--tanggal", "2026-09-%02d" % i, "--ya")
        self.run_ok("keluar", "--sku", "MATI", "--qty", "1", "--tanggal", "2026-07-15", "--ya")
        tl = self.run_ok("laporan", "tidak-laku", "--hari", "30", "--hari-ini", "2026-09-30")
        self.assertEqual([p["sku"] for p in tl["produk"]], ["MATI"])
        self.assertEqual(tl["nilai_tertahan_total"], 35000)
        mn = self.run_ok("laporan", "menipis", "--hari-ini", "2026-09-30")
        self.assertEqual(mn["produk"][0]["sku"], "LAKU")
        self.assertEqual(mn["produk"][0]["rata2_terjual_per_hari_30h"], 1)
        self.assertEqual(mn["produk"][0]["perkiraan_habis_hari"], 20)
        f = str(self.tmp / "mutasi.csv")
        mt = self.run_ok("laporan", "mutasi", "--dari", "2026-09-01", "--sampai", "2026-09-15", "--csv", f)
        per = {p["sku"]: p for p in mt["per_produk"]}
        self.assertEqual((per["LAKU"]["awal"], per["LAKU"]["keluar"], per["LAKU"]["akhir"]), (50, 15, 35))
        self.assertEqual(mt["nilai_penjualan_tercatat"], 30000)
        self.assertEqual(mt["hpp_barang_terjual"], 15000)
        self.assertTrue(Path(f).read_text(encoding="utf-8-sig").startswith("tanggal;sku;arah"))
        rk = self.run_ok("laporan", "ringkas", "--tanggal", "2026-09-30", "--hari-ini", "2026-09-30")
        self.assertEqual(rk["terjual_qty"], 1)
        self.assertEqual(rk["omzet_tercatat"], 2000)
        self.assertEqual(rk["laba_kotor_perkiraan"], 1000)
        self.assertEqual(rk["nilai_persediaan"], 20 * 1000 + 7 * 5000)
        self.run_gagal("laporan", "mutasi", "--dari", "2026-09-10", "--sampai", "2026-09-01")


class UjiPerforma(Dasar):
    def test_1000_lebih_transaksi(self):
        n_produk = 50
        baris = ["SKU;Nama;Harga Beli;Harga Jual;Stok;Stok Minimum;Lokasi"]
        for i in range(n_produk):
            baris.append("P%03d;Produk %d;%d;%d;1000;20;R%d" % (i, i, 10000 + i, 15000 + i, i % 5))
        f = self.tulis("produk.csv", "\n".join(baris) + "\n")
        t0 = time.time()
        self.run_ok("produk", "impor", f, "--ya")
        # 1.200 transaksi manual (masuk & keluar bergantian)
        for i in range(1200):
            sku = "P%03d" % (i % n_produk)
            if i % 4 == 0:
                self.run_ok("masuk", "--sku", sku, "--qty", "5", "--harga", str(9000 + i), "--ya")
            else:
                self.run_ok("keluar", "--sku", sku, "--qty", "2", "--ya")
        t_manual = time.time() - t0
        # 1.500 baris pesanan marketplace dalam satu file
        rows = [SHOPEE.strip()]
        for i in range(1500):
            rows.append("Q%05d,Perlu Dikirim,R%05d,SPX,2026-09-20,P%03d,Produk,,15000,1" % (i // 2, i // 2, i % n_produk))
        f2 = self.tulis("besar.csv", "\n".join(rows) + "\n")
        t1 = time.time()
        d = self.run_ok("impor-pesanan", f2, "--ya")
        t_impor = time.time() - t1
        self.assertEqual(d["pesanan_baru"], 750)
        t2 = time.time()
        self.run_ok("laporan", "stok")
        self.run_ok("laporan", "mutasi", "--dari", "2026-01-01", "--sampai", "2026-12-31")
        self.run_ok("laporan", "ringkas")
        pk = self.run_ok("picking")
        t_lap = time.time() - t2
        self.assertEqual(pk["jumlah_pesanan"], 750)
        self.konsisten()
        c = sqlite3.connect(str(self.db))
        jml = c.execute("SELECT COUNT(*) FROM mutasi").fetchone()[0]
        c.close()
        self.assertGreaterEqual(jml, 2700)
        print("\n  [performa] %d mutasi | 1.200 transaksi manual %.1f dtk | impor 1.500 baris %.2f dtk | 4 laporan %.2f dtk"
              % (jml, t_manual, t_impor, t_lap), file=sys.stderr)
        self.assertLess(t_impor, 30)
        self.assertLess(t_lap, 30)


TEMPLATES = Path(__file__).resolve().parent.parent / "templates"
SHOPEE_H = ("No. Pesanan,Status Pesanan,No. Resi,Opsi Pengiriman,Waktu Pesanan Dibuat,Nomor Referensi SKU,"
            "Nama Produk,Nama Variasi,Harga Setelah Diskon,Jumlah\n")


class UjiRevisi(Dasar):
    """Kasus dari uji independen (HASIL-UJI.md: B-1, S-1..S-4, R-1..R-4)."""

    def setUp(self):
        super().setUp()
        self.run_ok("produk", "impor", str(TEMPLATES / "daftar-produk.csv"), "--tanggal", "2026-09-01", "--ya")

    def test_b1_batal_setelah_impor_tidak_masuk_laporan(self):
        f1 = self.tulis("h1.csv", SHOPEE_H +
                        "P1,Perlu Dikirim,R1,SPX,2026-09-23 08:00,KAOS-HT-M,Kaos,Hitam M,59.000,2\n"
                        "P1,Perlu Dikirim,R1,SPX,2026-09-23 08:00,TOTE-NAT,Tote,Natural,35.000,1\n"
                        "P2,Perlu Dikirim,R2,J&T,2026-09-23 09:00,KAOS-PT-M,Kaos,Putih M,57.000,3\n"
                        "P3,Perlu Dikirim,R3,SPX,2026-09-23 10:00,MUG-KRM,Mug,Putih,45.000,2\n")
        self.run_ok("impor-pesanan", f1, "--ya")
        rk = self.run_ok("laporan", "ringkas", "--tanggal", "2026-09-23", "--hari-ini", "2026-09-23")
        self.assertEqual(rk["omzet_tercatat"], 414000)
        f2 = self.tulis("h2.csv", SHOPEE_H + "P2,Batal,R2,J&T,2026-09-23 09:00,KAOS-PT-M,Kaos,Putih M,57.000,3\n")
        self.run_ok("impor-pesanan", f2, "--ya")
        rk = self.run_ok("laporan", "ringkas", "--tanggal", "2026-09-23", "--hari-ini", "2026-09-23")
        self.assertEqual(rk["omzet_tercatat"], 243000)       # bukan 414.000
        self.assertEqual(rk["hpp_terjual"], 132500)           # 2x35.000 + 18.500 + 2x22.000
        self.assertEqual(rk["laba_kotor_perkiraan"], 110500)
        self.assertEqual(rk["terjual_qty"], 5)
        self.assertEqual(rk["pesanan_marketplace_hari_ini"], 2)
        self.assertNotIn("KAOS-PT-M", [t["sku"] for t in rk["top_terjual"]])
        mt = self.run_ok("laporan", "mutasi", "--dari", "2026-09-01", "--sampai", "2026-09-30")
        self.assertEqual(mt["nilai_penjualan_tercatat"], 243000)
        self.assertEqual(mt["hpp_barang_terjual"], 132500)
        per = {p["sku"]: p for p in mt["per_produk"]}
        self.assertEqual(per["KAOS-PT-M"]["akhir"], 30)       # stok kembali utuh
        mn = self.run_ok("laporan", "menipis", "--hari-ini", "2026-09-23")
        self.assertTrue(all(p["sku"] != "KAOS-PT-M" for p in mn["produk"]))
        self.konsisten()

    def test_migrasi_database_lama(self):
        f1 = self.tulis("h1.csv", SHOPEE_H + "P2,Perlu Dikirim,R2,J&T,2026-09-23,KAOS-PT-M,Kaos,Putih M,57000,3\n")
        self.run_ok("impor-pesanan", f1, "--ya")
        self.run_ok("impor-pesanan", self.tulis("h2.csv", SHOPEE_H + "P2,Batal,R2,J&T,2026-09-23,KAOS-PT-M,K,,57000,3\n"), "--ya")
        c = sqlite3.connect(str(self.db))
        try:
            c.execute("ALTER TABLE mutasi DROP COLUMN dibatalkan")   # tiru database versi 1.0.0
        except sqlite3.OperationalError:
            c.close()
            self.skipTest("SQLite terlalu lama untuk DROP COLUMN")
        c.commit()
        c.close()
        rk = self.run_ok("laporan", "ringkas", "--tanggal", "2026-09-23", "--hari-ini", "2026-09-23")
        self.assertEqual(rk["omzet_tercatat"], 0)

    def test_s1_item_dilewati_dipotong_setelah_sku_didaftarkan(self):
        f = self.tulis("s.csv", SHOPEE_H +
                       "X1,Perlu Dikirim,R1,SPX,2026-09-23,KAOS-HT-XL,Kaos,Hitam XL,59000,2\n"
                       "X1,Perlu Dikirim,R1,SPX,2026-09-23,TOTE-NAT,Tote,Natural,35000,1\n")
        self.run_ok("impor-pesanan", f, "--ya", "--lewati-tak-dikenal")
        self.assertAlmostEqual(self.produk("TOTE-NAT")["stok"], 39)
        self.run_ok("produk", "tambah", "--sku", "KAOS-HT-XL", "--nama", "Kaos", "--varian", "Hitam XL",
                    "--harga-beli", "36000", "--stok-awal", "10", "--lokasi", "A3", "--ya")
        d = self.run_ok("impor-pesanan", f, "--ya")
        self.assertEqual(d["pesanan_baru"], 0)
        self.assertEqual(len(d["item_lama_kini_terpotong"]), 1)
        self.assertAlmostEqual(self.produk("KAOS-HT-XL")["stok"], 8)
        self.assertAlmostEqual(self.produk("TOTE-NAT")["stok"], 39)   # tidak terpotong dua kali
        pk = self.run_ok("picking")
        self.assertTrue(all(a["terdaftar"] for a in pk["daftar_ambil"]))
        self.assertEqual(self.run_ok("impor-pesanan", f, "--ya")["item_lama_kini_terpotong"], [])
        self.konsisten()

    def test_b2_impor_ulang_sku_saja_tidak_salah_potong(self):
        f = self.tulis("wa.csv", "No. Pesanan;SKU;Qty;Status\n"
                       "WA-001;MUG-KRM;1;Perlu Dikirim\nWA-001;GELAS-01;2;Perlu Dikirim\n")
        self.run_ok("impor-pesanan", f, "--ya", "--lewati-tak-dikenal", "--tanggal-default", "2026-09-23") \
            if "--tanggal-default" in stok.__doc__ else self.run_ok("impor-pesanan", f, "--ya", "--lewati-tak-dikenal")
        awal = self.produk("MUG-KRM")["stok"]
        d = self.run_ok("impor-pesanan", f, "--ya", "--lewati-tak-dikenal")     # GELAS-01 masih belum terdaftar
        self.assertEqual(d["item_lama_kini_terpotong"], [])
        self.assertAlmostEqual(self.produk("MUG-KRM")["stok"], awal)          # MUG tidak terpotong lagi
        self.konsisten()

    def test_s2_pembatalan_diajukan_lalu_aktif_lagi(self):
        def impor(status):
            return self.run_ok("impor-pesanan", self.tulis("m.csv", SHOPEE_H +
                               "M1,%s,R1,SPX,2026-09-23,MUG-KRM,Mug,Putih,45000,2\n" % status), "--ya")
        impor("Perlu Dikirim")
        self.assertAlmostEqual(self.produk("MUG-KRM")["stok"], 10)
        d = impor("Pembatalan Diajukan")
        self.assertEqual(d["pembatalan_diajukan"], ["M1"])
        self.assertAlmostEqual(self.produk("MUG-KRM")["stok"], 10)          # stok tidak berubah
        self.assertEqual(self.run_ok("picking")["jumlah_pesanan"], 0)        # jangan dikemas dulu
        impor("Perlu Dikirim")                                               # pembatalan ditolak
        self.assertAlmostEqual(self.produk("MUG-KRM")["stok"], 10)
        self.assertEqual(self.run_ok("picking")["jumlah_pesanan"], 1)
        impor("Batal")
        self.assertAlmostEqual(self.produk("MUG-KRM")["stok"], 12)
        d = impor("Perlu Dikirim")                                           # aktif lagi -> potong ulang
        self.assertEqual(d["pesanan_batal_kini_aktif_lagi"], ["M1"])
        self.assertAlmostEqual(self.produk("MUG-KRM")["stok"], 10)
        rk = self.run_ok("laporan", "ringkas", "--tanggal", "2026-09-23", "--hari-ini", "2026-09-23")
        self.assertEqual((rk["terjual_qty"], rk["omzet_tercatat"]), (2, 90000))   # dihitung sekali
        self.assertEqual(stok.kategori_status("Cancellation requested"), "batal_diajukan")
        self.assertEqual(stok.kategori_status("Menunggu Konfirmasi Pembatalan"), "batal_diajukan")
        self.assertEqual(stok.kategori_status("Pembatalan: Dibatalkan oleh pembeli"), "batal")
        # pesanan baru yang langsung "pembatalan diajukan": stok dipotong, tidak masuk picking, diberi peringatan
        d = self.run_ok("impor-pesanan", self.tulis("m2.csv", SHOPEE_H +
                        "M2,Cancellation requested,R2,SPX,2026-09-23,TOTE-NAT,Tote,Natural,35000,1\n"), "--ya")
        self.assertEqual(d["pembatalan_diajukan"], ["M2"])
        self.assertEqual(self.run_ok("picking")["jumlah_pesanan"], 1)
        self.konsisten()

    def test_s3_s4_tiktok_harga_dan_versi_indonesia(self):
        en = self.tulis("en.csv",
                        "Order ID,Order Status,Cancelation/Return Type,Seller SKU,Product Name,Variation,Quantity,"
                        "Sku Quantity of return,SKU Unit Original Price,SKU Subtotal After Discount,Created Time,Tracking ID,"
                        "Shipping Provider Name\n"
                        "T1,AWAITING_SHIPMENT,,KAOS-HT-M,Kaos,Hitam M,2,0,65.000,110.000,23/09/2026 10:00:00,JX1,J&T\n"
                        "T2,Completed,Return/Refund,TOTE-NAT,Tote,Natural,1,1,40.000,35.000,23/09/2026 11:00:00,JX2,J&T\n")
        d = self.run_ok("impor-pesanan", en, "--ya")
        self.assertEqual(d["pemetaan_kolom"]["Subtotal baris"], "SKU Subtotal After Discount")
        self.assertNotIn("Harga satuan", d["pemetaan_kolom"])               # harga asli (sebelum diskon) tidak dipakai
        self.assertEqual(d["pesanan_bertanda_retur"], ["T2"])
        rk = self.run_ok("laporan", "ringkas", "--tanggal", "2026-09-23", "--hari-ini", "2026-09-23")
        self.assertEqual(rk["omzet_tercatat"], 145000)                        # 110.000 + 35.000
        self.assertEqual(rk["baris_jual_tanpa_harga"], 0)
        idn = self.tulis("id.csv",
                         "ID Pesanan,Status Pesanan,Jenis Pembatalan/Pengembalian,SKU Penjual,Nama Produk,Variasi,Kuantitas,"
                         "Jumlah Pengembalian SKU,Harga Satuan Asli SKU,Subtotal SKU Setelah Diskon,Waktu Dibuat,ID Pelacakan,"
                         "Nama Penyedia Pengiriman\n"
                         "5769001,Akan dikirim,,MUG-KRM,Mug,Putih,1,0,50.000,45.000,23/09/2026 12:00,JP9,J&T Express\n"
                         "5769002,Dikirim,,MUG-KRM,Mug,Putih,1,0,50.000,45.000,23/09/2026 12:30,JP8,J&T Express\n")
        d = self.run_ok("impor-pesanan", idn, "--ya")
        self.assertEqual(d["platform"], "tiktok")
        for label, kolom in (("No. resi", "ID Pelacakan"), ("Kurir", "Nama Penyedia Pengiriman"),
                             ("Tanggal", "Waktu Dibuat"), ("Subtotal baris", "Subtotal SKU Setelah Diskon")):
            self.assertEqual(d["pemetaan_kolom"][label], kolom)
        pk = self.run_ok("picking")
        nomor = [u["no_pesanan"] for u in pk["urutan_pesanan"]]
        self.assertIn("5769001", nomor)                                       # "Akan dikirim" masuk picking
        self.assertNotIn("5769002", nomor)
        self.assertEqual([u["resi"] for u in pk["urutan_pesanan"] if u["no_pesanan"] == "5769001"], ["JP9"])
        self.assertEqual(stok.kategori_status("Menunggu Konfirmasi Penjual"), "perlu_kirim")

    def test_r1_ringkas_pisah_toko_marketplace(self):
        self.run_ok("impor-pesanan", self.tulis("h.csv", SHOPEE_H +
                    "P1,Perlu Dikirim,R1,SPX,2026-09-23,KAOS-HT-M,Kaos,Hitam M,59000,2\n"), "--ya")
        self.run_ok("keluar", "--sku", "MUG-KRM", "--qty", "3", "--tanggal", "2026-09-23", "--ya")
        self.run_ok("masuk", "--sku", "TOTE-NAT", "--qty", "10", "--harga", "18000", "--biaya-tambahan", "5000",
                    "--tanggal", "2026-09-23", "--ya")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            stok.main(["laporan", "ringkas", "--tanggal", "2026-09-23", "--db", str(self.db)])
        teks = out.getvalue()
        self.assertIn("marketplace 2 dari 1 pesanan, toko/offline 3", teks)
        self.assertIn("Rp 185.000, termasuk ongkir/biaya tambahan", teks)

    def test_r4_backup_dihapus_bila_operasi_gagal(self):
        folder = self.db.parent / "backup-stok"
        sebelum = len(list(folder.glob("*.db"))) if folder.is_dir() else 0
        self.run_gagal("opname", "--hitung", "KAOS-HT-M=1", "--ya")          # tanpa alasan -> gagal
        self.assertEqual(len(list(folder.glob("*.db"))) if folder.is_dir() else 0, sebelum)



SKILL_MD = Path(__file__).resolve().parent.parent / "SKILL.md"


class UjiBahasaPengguna(Dasar):
    """v1.1.7: keluaran yang disalin agent ke chat tidak boleh memuat path/folder/perintah,
    dan istilah teknis (HPP, SKU) harus dijelaskan saat muncul (temuan pra-cek bot Telegram asli)."""

    LARANGAN_TEKS = ("backup-stok", "stok.py", "KomunitechData", "sqlite", "SQLite", ".db")

    def setUp(self):
        super().setUp()
        self.run_ok("produk", "impor", str(TEMPLATES / "daftar-produk.csv"), "--tanggal", "2026-09-01", "--ya")

    def teks(self, *argv, kode_harap=0):
        """Jalankan TANPA --json (teks siap kirim), kembalikan stdout+stderr."""
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            kode = stok.main(list(argv) + ["--db", str(self.db)])
        self.assertEqual(kode, kode_harap, out.getvalue() + err.getvalue())
        return out.getvalue() + err.getvalue()

    def cek_teks_bersih(self, t, nama):
        self.assertNotIn(str(self.tmp), t, "%s memuat path lengkap" % nama)
        for kata in self.LARANGAN_TEKS:
            if kata == ".db" and nama.startswith("backup"):
                continue  # nama berkas cadangan (tanpa folder) boleh tampil di perintah cadangan/pulihkan
            self.assertNotIn(kata, t, "%s memuat '%s'" % (nama, kata))
        # HPP hanya boleh muncul bersama penjelasan: "... (HPP)"
        self.assertEqual(len(re.findall(r"HPP", t)), len(re.findall(r"\(HPP\)", t)), "%s: HPP tanpa penjelasan\n%s" % (nama, t))
        # SKU hanya boleh muncul sebagai "kode barang (SKU)"
        tanpa_header = re.sub(r"<- [^\n]*", "<- ...", t)      # nama kolom di berkas pengguna (mis. "SKU") bukan istilah kita
        for m in re.finditer(r"SKU", tanpa_header):
            self.assertIn("barang (", tanpa_header[max(0, m.start() - 8):m.start()].lower(), "%s: SKU tanpa penjelasan\n%s" % (nama, t))

    def test_versi_dan_dokumen_sinkron(self):
        self.assertEqual(stok.VERSI, "1.1.7")
        akar = Path(__file__).resolve().parent.parent
        self.assertIn("1.1.7", (akar / "CHANGELOG.md").read_text(encoding="utf-8"))
        self.assertIn("Versi terkini: **1.1.7**", (akar / "README.md").read_text(encoding="utf-8"))
        self.assertEqual(self.run_ok("info")["versi_alat"], "1.1.7")

    def test_hasil_json_perintah_tulis_tanpa_lokasi(self):
        db2 = self.tmp / "toko2" / "stok.db"
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(stok.main(["init", "--db", str(db2), "--json"]), 0)
            self.assertEqual(stok.main(["init", "--db", str(db2), "--ya", "--json"]), 0)
        for potong in out.getvalue().replace("}\n{", "}\x00{").split("\x00"):
            d = json.loads(potong)
            self.assertNotIn(str(self.tmp), json.dumps(d), "init membocorkan path")
            self.assertNotIn("db", d)
            self.assertNotIn("folder_backup", d)
        d = self.run_ok("masuk", "--sku", "KAOS-HT-M", "--qty", "5", "--harga", "30000")
        self.assertNotIn(str(self.tmp), json.dumps(d))
        self.assertNotIn("db", d)
        self.assertNotIn("Konfirmasi lokasi", d["petunjuk"])
        d = self.run_ok("masuk", "--sku", "KAOS-HT-M", "--qty", "5", "--harga", "30000", "--ya")
        self.assertNotIn(str(self.tmp), json.dumps(d))
        d = self.run_ok("init")      # database sudah ada
        self.assertTrue(d["sudah_ada"])
        self.assertNotIn(str(self.tmp), json.dumps(d))

    def test_pratinjau_init_tidak_menyuruh_tanya_lokasi(self):
        baru = self.tmp / "baru" / "stok.db"
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            self.assertEqual(stok.main(["init", "--db", str(baru), "--json"]), 0)
        d = json.loads(out.getvalue())
        self.assertEqual(d["mode"], "pratinjau")
        self.assertIn("Jangan tanyakan lokasi", d["petunjuk"])
        self.assertNotIn("konfirmasi lokasi", d["petunjuk"].lower())
        self.assertFalse(baru.exists())

    def test_catatan_agen_bila_hasil_memuat_lokasi(self):
        b = self.run_ok("backup", "--label", "Sebelum Lebaran!")
        self.assertIn("Jangan menyebut path", b["catatan_agen"])
        daftar = self.run_ok("backup", "--daftar")
        self.assertIn("catatan_agen", daftar)
        item = [x for x in daftar["backup"] if x["nama"].endswith("-sebelum-lebaran.db")][0]
        self.assertTrue(item["nama"].startswith("stok-") and item["nama"].endswith(".db"))
        self.assertRegex(item["dibuat"], r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$")
        self.assertEqual(item["keterangan"], "sebelum lebaran")
        self.assertTrue(all(x["keterangan"] and x["dibuat"] for x in daftar["backup"]))
        self.assertIn("catatan_agen", self.run_ok("info"))
        d = self.run_ok("opname", "--hitung", "KAOS-HT-M=20", "--alasan", "salah catat", "--ya")
        self.assertIn("backup", d)
        self.assertIn("catatan_agen", d)
        self.assertNotIn("db", d)
        d = self.run_ok("restore", "--dari", b["backup"])
        self.assertIn("catatan_agen", d)
        self.assertNotIn("db", d)
        # hasil tanpa lokasi tidak perlu catatan
        self.assertNotIn("catatan_agen", self.run_ok("laporan", "stok"))

    def test_teks_siap_kirim_tanpa_path_dan_jargon(self):
        f1 = self.tulis("h1.csv", SHOPEE_H +
                        "P1,Perlu Dikirim,R1,SPX,2026-09-23 08:00,KAOS-HT-M,Kaos,Hitam M,59.000,2\n"
                        "P2,Perlu Dikirim,R2,J&T,2026-09-23 09:00,ABC-BARU,Topi,Merah,40.000,1\n")
        semua = {
            "laporan ringkas": self.teks("laporan", "ringkas", "--tanggal", "2026-09-23"),
            "laporan stok": self.teks("laporan", "stok"),
            "laporan menipis": self.teks("laporan", "menipis"),
            "laporan tidak-laku": self.teks("laporan", "tidak-laku", "--hari", "1"),
            "laporan mutasi": self.teks("laporan", "mutasi"),
            "masuk": self.teks("masuk", "--sku", "KAOS-HT-M", "--qty", "5", "--harga", "30000"),
            "keluar": self.teks("keluar", "--sku", "KAOS-HT-M", "--qty", "5"),
            "opname": self.teks("opname", "--hitung", "KAOS-HT-M=20", "--alasan", "salah catat"),
            "produk impor": self.teks("produk", "impor", str(TEMPLATES / "daftar-produk.csv")),
            "pesanan (kode belum terdaftar)": self.teks("impor-pesanan", f1, "--lewati-tak-dikenal"),
            "ubah produk": self.teks("produk", "ubah", "--sku", "KAOS-HT-M", "--koreksi-hpp", "34000"),
        }
        self.run_ok("impor-pesanan", f1, "--lewati-tak-dikenal", "--ya")
        semua["picking"] = self.teks("picking", "--csv", str(self.tmp / "ambil.csv"))
        semua["tulis ya (tersimpan)"] = self.teks("masuk", "--sku", "KAOS-HT-M", "--qty", "5", "--harga", "30000", "--ya")
        for nama, t in semua.items():
            self.cek_teks_bersih(t, nama)
        self.assertIn("Modal barang terjual (HPP)", semua["laporan ringkas"])
        self.assertIn("modal rata-rata per barang (HPP)", semua["masuk"])
        self.assertIn("KODE BARANG (SKU) BELUM TERDAFTAR", semua["pesanan (kode belum terdaftar)"])
        self.assertIn("ambil.csv", semua["picking"])
        self.assertNotIn("Backup sebelum perubahan", semua["tulis ya (tersimpan)"])
        self.assertIn("Cadangan otomatis", self.teks("opname", "--hitung", "KAOS-HT-M=21", "--alasan", "salah catat", "--ya"))

    def test_peringatan_dan_galat_tanpa_opsi_perintah(self):
        # peringatan impor pesanan: tanpa opsi/perintah
        f = self.tulis("h.csv", SHOPEE_H +
                       "P1,Status Aneh,R1,SPX,2026-09-23 08:00,KAOS-HT-M,Kaos,Hitam M,59.000,2\n"
                       "P2,Perlu Dikirim,R2,J&T,2026-09-23 09:00,MUG-KRM,Mug,Putih,45.000,200\n")
        d = self.run_ok("impor-pesanan", f)
        isi = " ".join(d["peringatan"])
        self.assertTrue(d["peringatan"])
        self.assertNotIn("--", isi)
        self.assertNotIn("opname untuk", isi)
        # galat: kalimat awam di `error`, petunjuk teknis di `langkah_agen`
        kasus = [
            ("masuk", "--ya"),
            ("keluar", "--sku", "KAOS-HT-M", "--qty", "1", "--jenis", "rusak", "--ya"),
            ("keluar", "--sku", "KAOS-HT-M", "--qty", "9999", "--ya"),
            ("keluar", "--sku", "ZZZ", "--qty", "1", "--ya"),
            ("produk", "tambah", "--sku", "KAOS-HT-M", "--nama", "dobel", "--ya"),
            ("produk", "ubah", "--sku", "KAOS-HT-M", "--ya"),
            ("opname", "--hitung", "KAOS-HT-M=1", "--ya"),
            ("opname", "--hitung", "KAOS-HT-M", "--ya"),
            ("opname", "--ya"),
            ("restore", "--dari", str(self.tmp / "tidak-ada.db")),
        ]
        for argv in kasus:
            e = self.run_gagal(*argv)
            self.assertNotIn("--", e["error"], "opsi bocor di error: %s" % e["error"])
            self.assertNotIn(str(self.tmp), json.dumps(e), "path bocor di error: %s" % (argv,))
            self.assertNotIn("stok.py", e["error"])
        e = self.run_gagal("keluar", "--sku", "ZZZ", "--qty", "1", "--ya")
        self.assertIn("Kode barang 'ZZZ' belum terdaftar", e["error"])
        self.assertIn("produk tambah", e["langkah_agen"])
        e = self.run_gagal("keluar", "--sku", "KAOS-HT-M", "--qty", "9999", "--ya")
        self.assertIn("--izinkan-minus", e["langkah_agen"])
        # pesanan dengan kode barang belum terdaftar
        g = self.tulis("g.csv", SHOPEE_H + "P9,Perlu Dikirim,R9,SPX,2026-09-23,TIDAK-ADA,Topi,Merah,40.000,1\n")
        e = self.run_gagal("impor-pesanan", g, "--ya")
        self.assertNotIn("--", e["error"])
        self.assertIn("--lewati-tak-dikenal", e["langkah_agen"])

    def test_skill_md_bagian_pengguna_bersih_dari_lokasi_dan_perintah(self):
        isi = SKILL_MD.read_text(encoding="utf-8")
        self.assertLess(isi.count("\n"), 300)
        self.assertIn("## Bahasa ke pengguna", isi)
        self.assertNotIn("Backup: <path>", isi)
        self.assertNotIn("boleh disimpan di", isi)           # tidak lagi menanyakan lokasi simpan
        # teks balasan ke pengguna = isi bagian "Format output ke pengguna" + kutipan (">") di bagian "Contoh"
        def bagian(judul):
            a = isi.index(judul)
            z = isi.find("\n## ", a + 5)
            return isi[a:z if z != -1 else None]
        contoh = bagian("## Contoh")
        balasan = re.findall(r"```\n(.*?)```", bagian("## Format output ke pengguna"), re.S)   # hanya blok contoh balasan
        balasan += [b[1:].strip() for b in contoh.splitlines() if b.startswith(">")]
        teks = "\n".join(balasan)
        self.assertIn("modal rata-rata per barang (HPP)", teks)
        self.assertIn("kode barang (SKU)", teks)
        for kata in ("KomunitechData", "backup-stok", ".db", "stok.py", "~/", "--ya", "--json", "database", "SQLite", "Backup:"):
            self.assertNotIn(kata, teks, "'%s' ada di teks balasan contoh SKILL.md" % kata)
        # setiap contoh balasan memuat paling banyak satu permintaan persetujuan
        grup, cur = [], []
        for b in contoh.splitlines():
            if b.startswith(">"):
                cur.append(b)
            elif cur:
                grup.append("\n".join(cur))
                cur = []
        if cur:
            grup.append("\n".join(cur))
        self.assertGreaterEqual(len(grup), 4)
        for blok in grup:
            self.assertLessEqual(blok.count("Simpan?"), 1)
        self.assertGreaterEqual(contoh.count("Simpan?"), 2)


class UjiBahasaPenggunaLanjutan(Dasar):
    """v1.1.7 (putaran 2): cadangan tidak boleh diklaim bila tidak dibuat, galat teks tanpa petunjuk teknis,
    lokasi tidak bocor di teks init/info, pratinjau impor sebelum buku stok ada, CSV dilampirkan (bukan disebut letaknya)."""

    def teks(self, *argv, db=None, kode_harap=0):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            kode = stok.main(list(argv) + ["--db", str(db or self.db)])
        self.assertEqual(kode, kode_harap, out.getvalue() + err.getvalue())
        return out.getvalue() + err.getvalue()

    def json_di(self, db, *argv, kode_harap=0):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            kode = stok.main(list(argv) + ["--db", str(db), "--json"])
        self.assertEqual(kode, kode_harap, out.getvalue())
        return json.loads(out.getvalue())

    # --- cadangan hanya disebut bila memang dibuat ---------------------------------------------------------
    def test_perintah_biasa_tidak_membuat_cadangan_dan_tidak_menyebutnya(self):
        self.run_ok("produk", "tambah", "--sku", "AA-1", "--nama", "Topi", "--harga-beli", "10000",
                    "--harga-jual", "20000", "--stok-awal", "10", "--ya")
        hasil = [
            self.run_ok("produk", "ubah", "--sku", "AA-1", "--harga-jual", "21000", "--ya"),
            self.run_ok("masuk", "--sku", "AA-1", "--qty", "50", "--harga", "9000", "--biaya-tambahan", "25000", "--ya"),
            self.run_ok("keluar", "--sku", "AA-1", "--qty", "2", "--ya"),
        ]
        for d in hasil:
            self.assertEqual(d["mode"], "tersimpan")
            self.assertNotIn("backup", d, "perintah ini tidak membuat cadangan")
            self.assertNotIn("catatan_agen", d)
        self.assertEqual(self.run_ok("info")["jumlah_backup"], 0)
        self.assertFalse((self.db.parent / "backup-stok").exists())
        t = self.teks("masuk", "--sku", "AA-1", "--qty", "1", "--harga", "9000", "--ya")
        self.assertNotIn("adangan", t)

    def test_cadangan_otomatis_hanya_untuk_impor_opname_restore(self):
        d = self.run_ok("produk", "impor", str(TEMPLATES / "daftar-produk.csv"), "--ya")
        self.assertIn("backup", d)
        d = self.run_ok("opname", "--hitung", "KAOS-HT-M=20", "--alasan", "salah catat", "--ya")
        self.assertIn("backup", d)
        self.assertEqual(self.run_ok("info")["jumlah_backup"], 2)

    def test_skill_md_cadangan_bersyarat(self):
        isi = SKILL_MD.read_text(encoding="utf-8")
        self.assertIn("hanya bila hasil script memuat `backup`", isi)
        self.assertIn("TIDAK", isi.split("## Bahasa ke pengguna")[0])        # aturan keamanan 3 menyebut yang tidak membuat cadangan
        setelah = isi[isi.index("**Setelah tersimpan:**"):isi.index("**Laporan harian**")]
        blok = re.search(r"```\n(.*?)```", setelah, re.S).group(1)
        self.assertNotIn("adangan", blok, "templat 'Setelah tersimpan' tidak boleh selalu menyebut cadangan")
        self.assertIn("hanya bila hasil script memuat `backup`", setelah)
        contoh = isi[isi.index("## Contoh"):isi.index("## Checklist")]
        grup, cur = [], []
        for baris in contoh.splitlines():
            if baris.startswith(">"):
                cur.append(baris)
            elif cur:
                grup.append("\n".join(cur))
                cur = []
        if cur:
            grup.append("\n".join(cur))
        sebut = [g for g in grup if "adangan" in g]
        self.assertEqual(len(sebut), 1, "hanya contoh hitung fisik (opname) yang boleh menyebut cadangan")
        self.assertIn("sekarang 72", sebut[0])                  # balasan setelah hitung fisik (opname)
        for g in grup:
            if "Kaos Hitam M sekarang 74" in g:
                self.assertNotIn("adangan", g)          # barang datang biasa
        self.assertIn('- [ ] "Cadangan otomatis sudah dibuat" hanya bila', isi)

    # --- kunci lokasi: "dari" di laporan mutasi bukan path -------------------------------------------------
    def test_laporan_mutasi_tanpa_catatan_agen_restore_tetap(self):
        self.run_ok("produk", "tambah", "--sku", "AA-1", "--nama", "Topi", "--harga-beli", "10000",
                    "--harga-jual", "20000", "--stok-awal", "10", "--ya")
        d = self.run_ok("laporan", "mutasi", "--dari", "2020-01-01", "--sampai", "2099-12-31")
        self.assertIn("dari", d)
        self.assertNotIn("catatan_agen", d)
        b = self.run_ok("backup")
        r = self.run_ok("restore", "--dari", b["backup"])
        self.assertIn("catatan_agen", r)
        self.assertNotIn("dari", r)
        self.assertIn("berkas_cadangan", r)

    # --- galat dalam mode teks (laporan terjadwal) ---------------------------------------------------------
    def test_galat_teks_hanya_kalimat_awam(self):
        hilang = self.tmp / "tidak-ada" / "stok.db"
        t = self.teks("laporan", "ringkas", db=hilang, kode_harap=1)
        self.assertEqual(t.strip(), "GAGAL: Buku stok belum disiapkan di komputer ini.")
        for kata in ("langkah_agen", "init", "--ya", str(self.tmp)):
            self.assertNotIn(kata, t)
        e = self.json_di(hilang, "laporan", "ringkas", kode_harap=1)       # JSON tetap memuat petunjuk teknis
        self.assertIn("init", e["langkah_agen"])
        self.assertFalse(hilang.parent.exists())

    def test_galat_sqlite_tidak_membocorkan_pesan_mentah(self):
        from unittest import mock
        kasus = [("database is locked", "sedang dipakai proses lain"),
                 ("disk I/O error", "gangguan teknis"),
                 ("unable to open database file", "gangguan teknis")]
        for mentah, awam in kasus:
            with mock.patch.object(stok, "buka", side_effect=sqlite3.OperationalError(mentah)):
                t = self.teks("laporan", "ringkas", kode_harap=1)
                self.assertIn(awam, t)
                self.assertNotIn(mentah, t)
                self.assertNotIn(str(self.tmp), t)
                self.assertNotIn("Kesalahan database", t)
                self.assertNotIn("langkah_agen", t)
                e = self.json_di(self.db, "laporan", "ringkas", kode_harap=1)
                self.assertIn(awam, e["error"])
                self.assertIn(mentah, e["detail_teknis"])
                self.assertNotIn(mentah, e["error"])
                self.assertIn("Jangan kutip detail_teknis", e["langkah_agen"])

    def test_galat_berkas_os_tanpa_path(self):
        from unittest import mock
        with mock.patch.object(stok, "buka", side_effect=PermissionError(13, "Permission denied", str(self.db))):
            t = self.teks("laporan", "ringkas", kode_harap=1)
            self.assertNotIn(str(self.tmp), t)
            self.assertIn("izin akses", t)
            self.assertNotIn("Traceback", t)

    # --- teks init/info tanpa lokasi -----------------------------------------------------------------------
    def test_teks_init_dan_info_tanpa_lokasi(self):
        baru = self.tmp / "toko-baru" / "stok.db"
        semua = [self.teks("init", db=baru)]
        self.assertFalse(baru.exists())
        semua.append(self.teks("init", "--ya", db=baru))
        semua.append(self.teks("init", db=baru))                          # sudah ada
        self.run_ok("produk", "impor", str(TEMPLATES / "daftar-produk.csv"), "--ya")
        semua.append(self.teks("info"))
        for t in semua:
            self.assertNotIn(str(self.tmp), t)
            for kata in ("backup-stok", ".db", "KomunitechData", "database", "Database"):
                self.assertNotIn(kata, t, t)
        self.assertIn("jumlah_backup: 1", semua[-1])
        self.assertIn("backup_terakhir_dibuat", semua[-1])
        self.assertIn("backup_terakhir", self.run_ok("info"))               # JSON tetap memuat lokasi untuk agent

    def test_teks_pratinjau_tanpa_nama_opsi(self):
        self.run_ok("produk", "tambah", "--sku", "AA-1", "--nama", "Topi", "--harga-beli", "10000",
                    "--harga-jual", "20000", "--stok-awal", "10", "--ya")
        for argv in (("masuk", "--sku", "AA-1", "--qty", "5", "--harga", "9000"),
                     ("keluar", "--sku", "AA-1", "--qty", "1"),
                     ("opname", "--hitung", "AA-1=9", "--alasan", "salah catat")):
            t = self.teks(*argv)
            self.assertTrue(t.startswith("PRATINJAU (belum disimpan)"), t)
            self.assertNotIn("--", t.splitlines()[0])

    # --- pratinjau impor sebelum buku stok ada -------------------------------------------------------------
    def test_pratinjau_impor_produk_sebelum_buku_stok_ada(self):
        baru = self.tmp / "belum" / "stok.db"
        f = str(TEMPLATES / "daftar-produk.csv")
        d = self.json_di(baru, "produk", "impor", f)
        self.assertEqual(d["mode"], "pratinjau")
        self.assertTrue(d["buku_belum_ada"])
        self.assertEqual(d["produk_baru"], 5)
        self.assertEqual(d["nilai_stok_awal"], 3494000)
        self.assertIn("init --ya", d["petunjuk"])
        self.assertNotIn(str(self.tmp), json.dumps(d))
        self.assertFalse(baru.parent.exists(), "pratinjau tidak boleh membuat berkas atau folder")
        # menyimpan tanpa menyiapkan buku tetap ditolak (tidak membuat buku diam-diam)
        e = self.json_di(baru, "produk", "impor", f, "--ya", kode_harap=1)
        self.assertIn("belum disiapkan", e["error"])
        self.assertFalse(baru.parent.exists())
        # alur sesungguhnya: init --ya, lalu impor --ya; angkanya sama dengan pratinjau
        self.json_di(baru, "init", "--ya")
        h = self.json_di(baru, "produk", "impor", f, "--ya")
        self.assertEqual(h["produk_baru"], d["produk_baru"])
        self.assertEqual(h["nilai_stok_awal"], d["nilai_stok_awal"])
        self.assertIn("backup", h)
        self.assertNotIn("buku_belum_ada", self.json_di(baru, "produk", "impor", f))

    def test_baris_rusak_dan_kolom_wajib_pakai_kode_barang_sku(self):
        f = self.tulis("rusak.csv", "SKU;Nama Produk;Harga Beli;Harga Jual;Stok\n;Topi;1000;2000;3\nB-1;Kaos;1000;2000;3\n")
        d = self.run_ok("produk", "impor", f)
        self.assertEqual(d["produk_baru"], 1)
        self.assertEqual(d["baris_rusak"][0]["alasan"], "kode barang (SKU) atau nama kosong")
        g = self.tulis("tanpa-sku.csv", "Harga Beli;Harga Jual;Stok\n1000;2000;3\n")
        e = self.run_gagal("produk", "impor", g)
        self.assertIn("kode barang (SKU)", e["error"])
        h = self.tulis("pes.csv", "No. Pesanan;Jumlah;Status\nP1;1;Selesai\n")
        e = self.run_gagal("impor-pesanan", h)
        self.assertIn("Kode barang (SKU) atau Nama produk", e["error"])

    # --- berkas yang diminta dilampirkan; pesan panjang -----------------------------------------------------
    def test_skill_md_lampiran_dan_pesan_panjang(self):
        isi = SKILL_MD.read_text(encoding="utf-8")
        self.assertNotIn("tersimpan di folder kerja", isi)
        bagian = isi[isi.index("## Bahasa ke pengguna"):isi.index("## Cara menjalankan script")]
        self.assertIn("lampirkan berkasnya ke chat", bagian)
        self.assertIn("balas 'kirim file'", bagian)
        self.assertIn("jangan menyebut nama folder atau jalur", bagian)
        self.assertIn("±3.500 karakter", bagian)
        self.assertIn("--ringkas-saja", bagian)
        self.assertIn("lalu lampirkan ke chat", isi)                          # D.2 picking
        self.assertIn("Bila gagal, kirim satu kalimat", isi)                   # pesan jadwal laporan
        self.assertIn("buku_belum_ada", isi)
        self.assertLess(isi.count("\n"), 300)

    def test_catatan_agen_menyebut_lampiran_dan_syarat_cadangan(self):
        self.assertIn("lampirkan berkasnya ke chat", stok.CATATAN_AGEN_LOKASI)
        self.assertIn("kunci backup", stok.CATATAN_AGEN_LOKASI)
        self.assertNotIn("dari", stok.KUNCI_LOKASI)


class UjiSingkatanFlag(unittest.TestCase):
    """Regresi keamanan: argparse tidak boleh menerima singkatan flag konfirmasi (mis. --y untuk --ya)."""

    def test_singkatan_flag_konfirmasi_ditolak(self):
        import subprocess
        import tempfile
        skrip = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts", "stok.py")
        with tempfile.TemporaryDirectory() as t:
            argv = ["init", "--db", os.path.join(t, "a.db"), "--y"]
            p = subprocess.run([sys.executable, skrip] + argv, capture_output=True, text=True, timeout=60)
            self.assertNotEqual(p.returncode, 0, p.stdout + p.stderr)
            self.assertIn("unrecognized arguments", p.stdout + p.stderr)
            self.assertFalse(os.path.exists(os.path.join(t, "a.db")), "singkatan flag tidak boleh menulis apa pun")


if __name__ == "__main__":
    unittest.main(verbosity=2)
