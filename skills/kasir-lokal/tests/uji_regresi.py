#!/usr/bin/env python3
"""Uji regresi kasir-lokal. Jalankan: python3 tests/uji_regresi.py  (Windows: py tests/uji_regresi.py)

Semua angka diverifikasi dengan rumus manual di komentar:
  total baris      = qty x harga, dibulatkan ke rupiah terdekat (0,5 ke atas)
  diskon bertingkat= tiap langkah dari sisa sebelumnya, dibulatkan ke rupiah terdekat
  diskon nota      = dari subtotal (setelah diskon item), dibagi ke baris proporsional (sisa terbesar)
  PPN (belum)      = floor(11% x DPP)             [12% x 11/12 x DPP, dibulatkan ke bawah sekali]
  PPN (termasuk)   = DPP rupiah bulat terbesar dengan DPP + floor(11% x DPP) <= harga; sisa ditampilkan
  retur            = nilai sisa sebelum - nilai sisa sesudah; pajak retur = pajak(sisa sebelum) - pajak(sisa sesudah)
  kas seharusnya   = kas awal + tunai bersih (tunai diterima - kembalian - refund tunai) + kas masuk - kas keluar
Produk contoh (templates/produk-contoh.csv): KSGA 18.000/cup, KH 12.000/cup, ETM 6.000/gelas,
RB Roti Bakar Coklat 15.000/porsi, RBK 17.000/porsi, AM600 4.000/botol (stok 48), GP1 Gula Pasir 16.500/kg (stok 20).
"""
import contextlib
import csv
import importlib.util
import io
import json
import os
import re
import shutil
import sqlite3
import sys
import tempfile
import unittest

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AKAR, "scripts"))
import kasir as K  # noqa: E402

KINI = "2026-09-24 21:00"
PRODUK_CSV = os.path.join(AKAR, "templates", "produk-contoh.csv")


def isi_file(path, encoding="utf-8"):
    with open(path, encoding=encoding) as f:
        return f.read()


class Dasar(unittest.TestCase):
    pajak = "tanpa"

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.db = os.path.join(self.dir, "kasir.db")
        argv = ["init", "--nama-toko", "Kedai Uji", "--ya"]
        if self.pajak != "tanpa":
            argv += ["--pajak", self.pajak, "--pkp", "ya"]
        self.ok(*argv)
        self.ok("produk", "impor", PRODUK_CSV, "--ya")

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def run_cli(self, *argv):
        argv = list(argv) + ["--db", self.db, "--json", "--hari-ini", KINI]
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
            kode = K.main(argv)
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

    def jual(self, pesan, waktu="2026-09-24 10:00", *extra):
        return self.ok("jual", "--pesan", pesan, "--waktu", waktu, "--ya", *extra)

    def file(self, nama, isi, encoding="utf-8"):
        p = os.path.join(self.dir, nama)
        with open(p, "w", encoding=encoding, newline="") as f:
            f.write(isi)
        return p


class UjiInti(unittest.TestCase):
    """Fungsi murni: pembulatan, diskon, alokasi, pajak."""

    def test_01_parse_angka_format_indonesia(self):
        self.assertEqual(K.parse_angka("Rp 15.000"), 15000)
        self.assertEqual(K.parse_angka("100rb"), 100000)
        self.assertEqual(K.parse_angka("1,5jt"), 1500000)
        self.assertEqual(str(K.parse_angka("1,5")), "1.5")
        self.assertEqual(K.parse_angka("15.000,-"), 15000)
        for rusak in ("1,250,000.50", "1.5E+04", "abc", "15.000.00"):
            with self.assertRaises(K.Gagal):
                K.parse_angka(rusak, "Harga")

    def test_02_diskon_bertingkat(self):
        # 18.000: 10% = 1.800 -> sisa 16.200; 5% x 16.200 = 810 -> total 2.610 (bukan 15% = 2.700)
        d, langkah = K.terapkan_diskon(18000, K.parse_diskon("10%+5%"), "x")
        self.assertEqual(d, 2610)
        self.assertEqual([x["potongan"] for x in langkah], [1800, 810])
        # campur persen + nominal: 50.000 - 10% (5.000) = 45.000 - 2.000 = 43.000 -> diskon 7.000
        self.assertEqual(K.terapkan_diskon(50000, K.parse_diskon("10%+2rb"), "x")[0], 7000)

    def test_03_pembulatan_diskon_terdekat(self):
        # 12,5% x 12.345 = 1.543,125 -> 1.543 ; 50% x 12.345 = 6.172,5 -> 6.173 (0,5 ke atas)
        self.assertEqual(K.terapkan_diskon(12345, K.parse_diskon("12,5%"), "x")[0], 1543)
        self.assertEqual(K.terapkan_diskon(12345, K.parse_diskon("50%"), "x")[0], 6173)

    def test_04_diskon_tidak_masuk_akal(self):
        for d in ("0%", "150%", "-5%"):
            with self.assertRaises(K.Gagal):
                K.parse_diskon(d)
        with self.assertRaises(K.Gagal):
            K.terapkan_diskon(5000, K.parse_diskon("6rb"), "x")   # diskon > harga

    def test_05_alokasi_sisa_terbesar(self):
        # 100 dibagi bobot 1:1:1 -> 33,33 masing-masing; sisa 1 ke baris pertama -> 34,33,33
        self.assertEqual(K.alokasi(100, [1, 1, 1]), [34, 33, 33])
        # 5.100 ke 36.000 : 15.000 -> 3.600 : 1.500 persis
        self.assertEqual(K.alokasi(5100, [36000, 15000]), [3600, 1500])
        self.assertEqual(sum(K.alokasi(7, [3, 5, 11])), 7)

    def test_06_ppn_belum_termasuk(self):
        # DPP 12.000 -> PPN = floor(11% x 12.000) = 1.320 -> total 13.320
        self.assertEqual(K.hitung_pajak(12000, "ppn-belum"), {"dpp": 12000, "ppn": 1320, "total": 13320, "sisa": 0})
        # DPP 12.345 -> 11% = 1.357,95 -> dibulatkan KE BAWAH 1.357 (bukan 1.358)
        self.assertEqual(K.hitung_pajak(12345, "ppn-belum")["ppn"], 1357)

    def test_07_ppn_termasuk(self):
        # 53.000: DPP = 47.748 (47.748 + floor(5.252,28)=5.252 = 53.000); 47.749 + 5.252 = 53.001 > 53.000
        self.assertEqual(K.hitung_pajak(53000, "ppn-termasuk"), {"dpp": 47748, "ppn": 5252, "total": 53000, "sisa": 0})
        # 1.110.000 -> DPP 1.000.000, PPN 110.000 (contoh hitung-ppn)
        self.assertEqual(K.hitung_pajak(1110000, "ppn-termasuk")["dpp"], 1000000)
        # 7.500.000 -> DPP 6.756.757, PPN floor(743.243,27) = 743.243, sisa 0 (contoh SKILL hitung-ppn)
        h = K.hitung_pajak(7500000, "ppn-termasuk")
        self.assertEqual((h["dpp"], h["ppn"], h["sisa"]), (6756757, 743243, 0))
        # 100: DPP 90 -> 90 + floor(9,9)=9 = 99 <= 100; DPP 91 -> 91 + 10 = 101 > 100 -> sisa Rp 1
        self.assertEqual(K.hitung_pajak(100, "ppn-termasuk"), {"dpp": 90, "ppn": 9, "total": 100, "sisa": 1})

    def test_08_konsisten_dengan_skill_hitung_ppn(self):
        path = os.path.join(AKAR, "..", "hitung-ppn", "scripts", "hitung_ppn.py")
        if not os.path.isfile(path):
            self.skipTest("skill hitung-ppn tidak ada di sebelah folder ini")
        spec = importlib.util.spec_from_file_location("hitung_ppn", path)
        H = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(H)
        for harga in list(range(1, 2000, 7)) + [53000, 99999, 1234567, 7500000, 45900, 118165]:
            a = K.hitung_pajak(harga, "ppn-termasuk")
            b = H.hitung_ppn_dari_total(harga, "umum")
            self.assertEqual((a["dpp"], a["ppn"]), (int(b["dpp"]), int(b["ppn"])), harga)
            c = K.hitung_pajak(harga, "ppn-belum")
            d = H.hitung_ppn_dari_dpp(harga, "umum")
            self.assertEqual(c["ppn"], int(d["ppn"]), harga)

    def test_09_dpp_nilai_lain(self):
        # 47.748 x 11/12 = 43.769 persis
        self.assertEqual(str(K.dpp_nilai_lain(47748)), "43769.00")

    def test_10_formula_injection(self):
        self.assertEqual(K.sel_aman("=HYPERLINK(\"x\")"), "'=HYPERLINK(\"x\")")
        self.assertEqual(K.sel_aman("+62812"), "'+62812")
        self.assertEqual(K.sel_aman("@SUM(A1)"), "'@SUM(A1)")
        # v1.1.1: teks diawali minus+angka tetap diamankan (payload DDE), angka murni tetap angka
        self.assertEqual(K.sel_aman("-1+1+cmd|' /C calc'!A0"), "'-1+1+cmd|' /C calc'!A0")
        self.assertEqual(K.sel_aman("-5 Diskon Palsu"), "'-5 Diskon Palsu")
        self.assertEqual(K.sel_aman("-2,5"), "-2,5")
        self.assertEqual(K.sel_aman("-2.5"), "-2.5")
        self.assertEqual(K.sel_aman(-5000), -5000)          # angka minus tetap angka
        self.assertEqual(K.sel_aman("Kopi"), "Kopi")


class UjiJual(Dasar):
    def test_11_contoh_utama(self):
        # 2 x 18.000 = 36.000 ; 1 x 15.000 = 15.000 ; subtotal 51.000 ; diskon 10% = 5.100 ; total 45.900
        # bayar 100.000 -> kembalian 54.100
        o = self.jual("2 kopi susu, 1 roti bakar, diskon 10%, bayar tunai 100rb")
        self.assertEqual((o["subtotal"], o["diskon_nota"], o["total"], o["kembalian"]), (51000, 5100, 45900, 54100))
        self.assertEqual([b["diskon_nota"] for b in o["baris"]], [3600, 1500])
        self.assertEqual(o["no"], "N-260924-0001")
        self.assertTrue(any("Kopi Susu Gula Aren" in p for p in o["peringatan"]))   # cocok sebagian disebut

    def test_12_pratinjau_tidak_menyimpan(self):
        o = self.ok("jual", "--pesan", "1 kopi hitam, bayar pas")
        self.assertEqual(o["mode"], "pratinjau")
        self.assertEqual(self.ok("nota", "--tanggal", "2026-09-24")["nota"], [])

    def test_13_diskon_item_bertingkat_dan_nota(self):
        # ETM 3 x 6.000 = 18.000, diskon 10%+5% = 2.610 -> 15.390 ; KH 2 x 12.000 = 24.000
        # subtotal 39.390 ; diskon nota 5rb -> 34.390 ; alokasi 5.000 x 15.390/39.390 = 1.953,5 ; x 24.000/39.390 = 3.046,4
        #   dasar 1.953 + 3.046 = 4.999 ; sisa 1 ke pecahan terbesar (0,5 > 0,4) -> 1.954 / 3.046
        o = self.jual("3 es teh manis diskon 10%+5%, kopi hitam x2, diskon 5rb, bayar pas")
        self.assertEqual(o["baris"][0]["diskon_item"], 2610)
        self.assertEqual(o["subtotal"], 39390)
        self.assertEqual(o["total"], 34390)
        self.assertEqual([b["diskon_nota"] for b in o["baris"]], [1954, 3046])
        self.assertEqual(sum(b["netto"] for b in o["baris"]), o["netto"])

    def test_14_qty_pecahan_kg_dan_pembulatan(self):
        # 0,33 kg x 16.500 = 5.445 persis ; 1,255 kg x 16.500 = 20.707,5 -> 20.708 (0,5 ke atas)
        o = self.jual("0,33 kg gula pasir, gula pasir 1,255 kg, bayar pas")
        self.assertEqual([b["bruto"] for b in o["baris"]], [5445, 20708])
        self.assertEqual(o["total"], 26153)

    def test_15_qty_pecahan_satuan_non_kg_ditolak(self):
        o = self.gagal("jual", "--pesan", "1,5 kopi hitam")
        self.assertIn("pecahan", o["error"])

    def test_16_produk_tak_dikenal_disarankan(self):
        o = self.gagal("jual", "--pesan", "2 kopi susuu, 1 bakso")
        self.assertIn("Kopi Susu Gula Aren", o["error"])
        self.assertEqual(o["masalah"][1]["masalah"], "tidak dikenal")
        self.assertEqual(self.ok("nota", "--tanggal", "2026-09-24")["nota"], [])   # tidak ada yang tersimpan

    def test_17_produk_ambigu_tidak_ditebak(self):
        # 'roti' cocok dengan RB (Roti Bakar Coklat) dan RBK -> wajib memilih
        o = self.gagal("jual", "--pesan", "1 roti")
        self.assertEqual(o["masalah"][0]["masalah"], "cocok dengan beberapa produk")

    def test_18_pembayaran_kurang_dan_bon(self):
        o = self.gagal("jual", "--pesan", "1 roti bakar keju, bayar tunai 10rb")
        self.assertEqual(o["kurang"], 7000)      # 17.000 - 10.000
        self.assertIn("bon", self.gagal("jual", "--pesan", "1 kopi hitam, bayar nanti")["error"])

    def test_19_bayar_campuran_dan_non_tunai_lebih(self):
        # total 12.000 x 2 = 24.000 ; qris 10rb + tunai 20rb = 30.000 -> kembalian 6.000 (dari tunai)
        o = self.jual("2 kopi hitam, bayar qris 10rb, tunai 20rb")
        self.assertEqual(o["bayar"], {"QRIS": 10000, "Tunai": 20000})
        self.assertEqual(o["kembalian"], 6000)
        # qris tanpa jumlah + tunai 5rb -> qris = 24.000 - 5.000 = 19.000
        o = self.jual("2 kopi hitam, bayar tunai 5rb, qris", "2026-09-24 11:00")
        self.assertEqual(o["bayar"]["QRIS"], 19000)
        self.assertIn("non-tunai", self.gagal("jual", "--pesan", "1 kopi hitam, bayar qris 20rb")["error"])

    def test_20_nota_duplikat_ditahan(self):
        self.jual("1 kopi hitam, bayar pas", "2026-09-24 10:00")
        o = self.gagal("jual", "--pesan", "1 kopi hitam, bayar pas", "--waktu", "2026-09-24 10:03", "--ya")
        self.assertIn("dobel", o["error"])
        o = self.jual("1 kopi hitam, bayar pas", "2026-09-24 10:03", "--izinkan-duplikat")
        self.assertEqual(o["no"], "N-260924-0002")
        self.jual("1 kopi hitam, bayar pas", "2026-09-24 10:30")   # > 10 menit: bukan dobel

    def test_21_nomor_nota_berurutan_per_hari(self):
        nos = [self.jual("1 es teh manis, bayar pas", "2026-09-24 1%d:00" % i)["no"] for i in range(3)]
        self.assertEqual(nos, ["N-260924-0001", "N-260924-0002", "N-260924-0003"])
        self.assertEqual(self.jual("1 es teh manis, bayar pas", "2026-09-25 08:00")["no"], "N-260925-0001")

    def test_22_stok_mode_kasir(self):
        self.ok("atur", "--stok", "kasir", "--ya")
        self.jual("2 air mineral, bayar pas")                     # 48 - 2 = 46
        o = self.ok("produk", "cari", "AM600")
        self.assertEqual(o["produk"][0]["stok"], 46)
        self.assertIn("tidak cukup", self.gagal("jual", "--pesan", "21 gula pasir", "--ya")["error"])  # stok 20


class UjiPajak(Dasar):
    pajak = "ppn-termasuk"

    def test_23_nota_ppn_termasuk(self):
        # 2 x 18.000 + 17.000 = 53.000 -> DPP 47.748, PPN 5.252, total 53.000
        o = self.jual("2 kopi susu gula aren, 1 roti bakar keju, bayar qris")
        self.assertEqual((o["dpp"], o["ppn"], o["total"], o["selisih_pembulatan"]), (47748, 5252, 53000, 0))

    def test_24_retur_ppn_termasuk(self):
        # sisa 35.000 -> DPP 31.532 (31.532 + 3.468 = 35.000) ; koreksi DPP = 31.532 - 47.748 = -16.216 ;
        # koreksi PPN = 3.468 - 5.252 = -1.784 ; uang kembali 18.000
        o = self.jual("2 kopi susu gula aren, 1 roti bakar keju, bayar qris")
        r = self.ok("retur", "--nota", o["no"], "--item", "1 kopi susu", "--alasan", "salah rasa", "--refund", "qris",
                    "--waktu", "2026-09-24 10:10", "--ya")
        self.assertEqual((r["dpp"], r["ppn"], r["total"]), (-16216, -1784, -18000))
        self.assertEqual(r["refund"], {"QRIS": 18000})

    def test_25_ppn_wajib_pkp(self):
        self.assertIn("PKP", self.gagal("atur", "--pkp", "tidak", "--ya")["error"])

    def test_26_ppn_belum_dan_rekap_omzet(self):
        self.ok("atur", "--pajak", "ppn-belum", "--ya")
        # KH 12.000 x 3 = 36.000 -> PPN = floor(11% x 36.000) = 3.960 -> total 39.960
        o = self.jual("3 kopi hitam, bayar transfer")
        self.assertEqual((o["ppn"], o["total"]), (3960, 39960))
        r = self.ok("rekap", "--bulan", "2026-09")
        self.assertEqual((r["ppn"], r["total_diterima"], r["omzet_tanpa_ppn"]), (3960, 39960, 36000))
        self.assertIn("pph-final-umkm", r["teks"])


class UjiReturVoidKas(Dasar):
    def test_27_retur_sebagian_diskon_bertingkat(self):
        # ETM 3 x 6.000 - (10%+5%) = 15.390 ; retur 1 -> sisa 15.390 - round(5.130) = 10.260 -> nilai retur 5.130
        o = self.jual("3 es teh manis diskon 10%+5%, bayar pas")
        r = self.ok("retur", "--nota", o["no"], "--item", "1 es teh", "--alasan", "tumpah", "--waktu",
                    "2026-09-24 10:05", "--ya")
        self.assertEqual(r["total"], -5130)
        self.assertEqual(r["no"], "R-260924-0001")
        # retur 2 sisanya -> 10.260 ; lebih dari itu ditolak
        r2 = self.ok("retur", "--nota", o["no"], "--item", "2 es teh", "--alasan", "tumpah", "--waktu",
                     "2026-09-24 10:06", "--ya")
        self.assertEqual(r2["total"], -10260)
        self.assertIn("melebihi", self.gagal("retur", "--nota", o["no"], "--item", "1 es teh", "--alasan", "x")["error"])

    def test_28_void_membalik_semua_metode(self):
        o = self.jual("2 kopi hitam, bayar qris 10rb, tunai 20rb")
        v = self.ok("void", "--nota", o["no"], "--alasan", "salah input", "--waktu", "2026-09-24 10:01", "--ya")
        # QRIS dibalik 10.000; tunai dibalik 20.000 - kembalian 6.000 = 14.000
        self.assertEqual(v["refund"], {"QRIS": 10000, "Tunai": 14000})
        self.assertIn("sudah pernah", self.gagal("void", "--nota", o["no"], "--alasan", "lagi")["error"])
        n = self.ok("nota", "--no", o["no"])
        self.assertEqual(n["status"], "void")                   # nota asal tetap ada, tidak dihapus
        r = self.ok("rekap", "--tanggal", "2026-09-24")
        self.assertEqual((r["penjualan_bersih"], r["total_diterima"]), (0, 0))

    def test_29_retur_wajib_alasan_dan_nota_ada(self):
        o = self.jual("1 kopi hitam, bayar pas")
        self.gagal("retur", "--nota", o["no"], "--item", "1 kopi hitam", "--alasan", "  ")
        self.assertIn("tidak ditemukan", self.gagal("void", "--nota", "N-000000-0009", "--alasan", "x")["error"])

    def test_30_tutup_kasir_selisih(self):
        self.ok("buka-kasir", "--kas-awal", "200rb", "--waktu", "2026-09-24 07:00", "--ya")
        self.jual("2 kopi susu, 1 roti bakar, diskon 10%, bayar tunai 100rb", "2026-09-24 08:15")   # tunai +45.900
        o = self.jual("2 kopi hitam, bayar qris 10rb, tunai 20rb", "2026-09-24 09:00")              # tunai +14.000
        self.ok("void", "--nota", o["no"], "--alasan", "batal", "--waktu", "2026-09-24 09:05", "--ya")  # tunai -14.000
        self.ok("kas", "--keluar", "20rb", "--catatan", "beli es batu", "--waktu", "2026-09-24 10:00", "--ya")
        # seharusnya = 200.000 + 45.900 + 14.000 - 14.000 - 20.000 = 225.900 ; fisik 225.000 -> KURANG 900
        t = self.ok("tutup-kasir", "--kas-fisik", "225.000", "--setoran", "125rb", "--waktu", "2026-09-24 21:00", "--ya")
        self.assertEqual((t["kas_seharusnya"], t["selisih"], t["sisa_laci"]), (225900, -900, 100000))
        self.assertIn("KURANG Rp 900", t["teks"])
        self.assertEqual(t["per_metode"].get("QRIS"), 0)
        self.assertIn("backup", t)
        self.assertIn("Kasir belum dibuka", self.gagal("tutup-kasir", "--kas-fisik", "0", "--ya")["error"])

    def test_31_buka_kasir_mundur_mengikutkan_nota(self):
        self.jual("1 kopi hitam, bayar pas", "2026-09-24 08:00")
        o = self.ok("buka-kasir", "--kas-awal", "100rb", "--waktu", "2026-09-24 07:00", "--ya")
        self.assertEqual(o["nota_disertakan"], 1)
        t = self.ok("tutup-kasir", "--kas-fisik", "112rb", "--waktu", "2026-09-24 21:00")   # 100.000 + 12.000 -> PAS
        self.assertEqual(t["selisih"], 0)


class UjiRekapStrukEkspor(Dasar):
    def isi(self):
        self.jual("2 kopi susu, 1 roti bakar, diskon 10%, bayar tunai 100rb", "2026-09-24 08:15")   # 45.900
        o = self.jual("3 es teh manis diskon 10%+5%, 1,5 kg gula pasir, kopi hitam x2, bayar qris 40rb, tunai 50rb",
                      "2026-09-24 09:05")                                                          # 64.140
        self.ok("retur", "--nota", o["no"], "--item", "1 es teh", "--alasan", "tumpah", "--waktu", "2026-09-24 09:30",
                "--ya")                                                                            # -5.130
        self.ok("void", "--nota", "N-260924-0001", "--alasan", "salah", "--waktu", "2026-09-24 09:40", "--ya")  # -45.900
        self.jual("gula pasir 0,25 kg dan 1 air mineral, bayar pas", "2026-09-24 12:10")          # 8.125
        return o

    def test_32_rekap_harian(self):
        self.isi()
        r = self.ok("rekap", "--tanggal", "2026-09-24")
        # kotor = 51.000 + 66.750 + 8.125 = 125.875 ; diskon = 5.100 + 2.610 = 7.710
        # retur/void = -(5.130 + 45.900) = -51.030 ; bersih = 125.875 - 7.710 - 51.030 = 67.135
        self.assertEqual((r["penjualan_kotor"], r["diskon"], r["retur_void"], r["penjualan_bersih"]),
                         (125875, 7710, -51030, 67135))
        # tunai: 45.900 - 45.900 + 24.140 - 5.130 + 8.125 = 27.135 ; QRIS 40.000 ; jumlah = uang diterima
        self.assertEqual(r["per_metode"], {"Tunai": 27135, "QRIS": 40000})
        self.assertEqual(sum(r["per_metode"].values()), r["total_diterima"])
        # v1.1.0: nota yang di-void (N-0001) tidak ikut rata-rata: (64.140 + 8.125) / 2 = 36.132,5 -> 36.133
        self.assertEqual(r["rata_rata_per_nota"], 36133)
        self.assertNotIn("08", r["per_jam"])                       # jam 08 hanya berisi nota yang di-void
        self.assertEqual(r["per_jam"]["09"], {"nota": 1, "total": 64140})
        gp = [p for p in r["per_produk"] if p["kode"] == "GP1"][0]
        self.assertEqual((gp["qty"], gp["netto"]), (1.75, 28875))     # 24.750 + 4.125
        self.assertNotIn("KSGA", [p["kode"] for p in r["per_produk"] if p["netto"]])   # di-void -> 0
        self.assertIn("REKAP KASIR Kamis, 24/09/2026", r["teks"])

    def test_33_rekap_kosong_dan_tahunan(self):
        self.assertIn("Belum ada transaksi", self.ok("rekap", "--tanggal", "2026-09-20")["teks"])
        self.isi()
        r = self.ok("rekap", "--tahun", "2026")
        self.assertEqual(r["per_bulan"], {"2026-09": 67135})
        self.assertIn("--bulan-awal 9 --omzet 67135", r["perintah_pph_final"])

    def test_34_struk_58_dan_80(self):
        o = self.isi()
        s58 = self.ok("struk", "--nota", o["no"], "--kertas", "58", "--keluar", os.path.join(self.dir, "s58.html"))
        self.assertTrue(all(len(b) <= 32 for b in s58["baris"]))
        html58 = isi_file(s58["file"])
        self.assertIn("size: 58mm", html58)
        self.assertIn("monospace", html58)
        self.assertNotIn("http", html58.replace("http-equiv", ""))     # tanpa sumber daya internet
        s80 = self.ok("struk", "--nota", o["no"], "--kertas", "80", "--keluar", os.path.join(self.dir, "s80.html"))
        self.assertTrue(all(len(b) <= 48 for b in s80["baris"]))
        self.assertIn("size: 80mm", isi_file(s80["file"]))
        self.assertIn("SALINAN - cetak ke-2", s80["baris"][0])          # cetak ulang ditandai
        self.assertTrue(any("64.140" in b and "TOTAL" in b for b in s58["baris"]))
        r = self.ok("struk", "--nota", "R-260924-0001", "--teks")
        self.assertIn("RETUR", r["teks"])

    def test_35_struk_escape_html(self):
        self.ok("produk", "tambah", "--kode", "X1", "--nama", "<script>alert(1)</script>", "--harga", "1000", "--ya")
        self.ok("jual", "--item", "1 X1", "--ya")
        s = self.ok("struk", "--keluar", os.path.join(self.dir, "x.html"))
        self.assertNotIn("<script>", isi_file(s["file"]))

    def test_36_ekspor_penjualan_kompatibel_rekap_penjualan_csv(self):
        self.isi()
        out = os.path.join(self.dir, "jual.csv")
        self.ok("ekspor", "--format", "penjualan", "--tanggal", "2026-09-24", "--csv", out)
        with open(out, encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f, delimiter=";"))
        self.assertEqual(sum(int(r["Total"]) for r in rows), 67135)     # = penjualan bersih rekap
        self.assertIn("1,5", [r["Qty"] for r in rows])                  # desimal koma untuk Excel Indonesia
        path = os.path.join(AKAR, "..", "rekap-penjualan-csv", "scripts", "rekap.py")
        if os.path.isfile(path):
            import subprocess
            p = subprocess.run([sys.executable, path, out, "--kolom-tanggal", "Tanggal", "--kolom-produk", "Produk",
                                "--kolom-qty", "Qty", "--kolom-total", "Total", "--kolom-status", "Status"],
                               capture_output=True, text=True)
            self.assertEqual(json.loads(p.stdout)["total_omzet"], 67135)

    def test_37_ekspor_buku_stok(self):
        self.isi()
        out = os.path.join(self.dir, "bs.csv")
        o = self.ok("ekspor", "--format", "buku-stok", "--tanggal", "2026-09-24", "--csv", out)
        with open(out, encoding="utf-8-sig") as f:
            rows = list(csv.DictReader(f, delimiter=";"))
        self.assertEqual({r["Status"] for r in rows if r["Nomor Pesanan"] == "N-260924-0001"}, {"Dibatalkan"})
        self.assertTrue(all(float(r["Jumlah"].replace(",", ".")) > 0 for r in rows))   # tanpa qty minus
        self.assertTrue(any("retur pembeli" in p for p in o["peringatan"]))
        stok = os.path.join(AKAR, "..", "buku-stok", "scripts", "stok.py")
        if os.path.isfile(stok):
            import subprocess
            sdb = os.path.join(self.dir, "stok.db")
            run = lambda *a: subprocess.run([sys.executable, stok] + list(a) + ["--db", sdb, "--json"],
                                            capture_output=True, text=True)
            run("init", "--ya")
            for sku in ("KSGA", "RB", "ETM", "GP1", "KH", "AM600"):
                run("produk", "tambah", "--sku", sku, "--nama", sku, "--satuan", "kg" if sku == "GP1" else "pcs",
                    "--stok-awal", "20", "--harga-beli", "1000", "--ya")
            run("impor-pesanan", out, "--platform", "lainnya", "--ya")
            d = json.loads(run("laporan", "stok").stdout)
            stok_akhir = {p["sku"]: p["stok"] for p in d["produk"]}
            # ETM 20-3 = 17 ; GP1 20-1,5-0,25 = 18,25 ; KSGA & RB tidak dipotong (nota di-void = Dibatalkan)
            self.assertEqual((stok_akhir["ETM"], stok_akhir["GP1"], stok_akhir["KSGA"]), (17, 18.25, 20))
            ulang = json.loads(run("impor-pesanan", out, "--platform", "lainnya").stdout)
            self.assertEqual(ulang["ringkasan"]["pesanan_baru"], 0)       # impor ulang tidak dobel potong

    def test_38_ekspor_formula_injection(self):
        self.ok("produk", "tambah", "--kode", "INJ", "--nama", "=HYPERLINK(\"http://x\")", "--harga", "1000", "--ya")
        self.ok("jual", "--item", "1 INJ", "--ya")
        out = os.path.join(self.dir, "j.csv")
        self.ok("ekspor", "--tanggal", "2026-09-24", "--csv", out)
        isi = isi_file(out, "utf-8-sig")
        self.assertIn("'=HYPERLINK", isi)


class UjiDataRusak(Dasar):
    def test_39_impor_csv_excel_bom_cp1252_dan_baris_rusak(self):
        # cp1252 (Excel Windows lama), pemisah ';', harga 0, harga negatif, kode ganda, kode kosong
        isi = ("Kode;Nama Produk;Harga;Satuan\r\nC1;Caf\xe9 Latte;22.000;cup\r\nC2;Teh Gratis;0;cup\r\n"
               "C3;Minus;-5000;cup\r\nC1;Dobel;1000;cup\r\n;Tanpa Kode;7.500;pcs\r\nC4;Ilmiah;1,5E+04;pcs\r\n")
        p = self.file("excel.csv", isi, encoding="cp1252")
        o = self.ok("produk", "impor", p, "--ya")
        self.assertEqual([b["kode"] for b in o["baru"]], ["C1", "P008"])
        self.assertEqual(len(o["baris_rusak"]), 4)
        self.assertTrue(any("Windows-1252" in x for x in o["peringatan"]))
        self.assertEqual(self.ok("produk", "cari", "latte")["produk"][0]["nama"], "Caf\xe9 Latte")
        # BOM UTF-8 + pemisah koma
        p2 = self.file("bom.csv", "﻿kode,nama,harga jual\nD1,Donat,5000\n")
        self.assertEqual(self.ok("produk", "impor", p2, "--ya")["baru"][0]["kode"], "D1")

    def test_40_produk_harga_nol_negatif_ditolak(self):
        self.gagal("produk", "tambah", "--kode", "Z", "--nama", "Gratis", "--harga", "0", "--ya")
        self.gagal("produk", "tambah", "--kode", "Z", "--nama", "Minus", "--harga", "-1000", "--ya")
        self.gagal("produk", "tambah", "--kode", "Z", "--nama", "Sen", "--harga", "1.000,50", "--ya")
        self.gagal("produk", "tambah", "--kode", "KSGA", "--nama", "Kembar", "--harga", "1000", "--ya")

    def test_41_db_terkunci_pesan_jelas(self):
        kunci = sqlite3.connect(self.db, isolation_level=None)
        kunci.execute("BEGIN EXCLUSIVE")
        lama = os.environ.get("KOMUNITECH_KASIR_TIMEOUT")
        os.environ["KOMUNITECH_KASIR_TIMEOUT"] = "0.3"
        try:
            o = self.gagal("jual", "--pesan", "1 kopi hitam, bayar pas", "--ya")
            self.assertIn("sedang dipakai", o["error"])
        finally:
            kunci.execute("ROLLBACK")
            kunci.close()
            if lama is None:
                os.environ.pop("KOMUNITECH_KASIR_TIMEOUT", None)
            else:
                os.environ["KOMUNITECH_KASIR_TIMEOUT"] = lama
        self.jual("1 kopi hitam, bayar pas")

    def test_42_bukan_database_kasir_dan_belum_ada(self):
        p = self.file("bukan.db", "ini bukan database")
        kode, o = self.run_cli("info")
        self.assertEqual(kode, 0)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.assertEqual(K.main(["info", "--db", p, "--json"]), 1)
        self.assertIn("bukan buku kasir", json.loads(buf.getvalue())["error"])
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.assertEqual(K.main(["info", "--db", os.path.join(self.dir, "tidak-ada.db"), "--json"]), 1)
        self.assertIn("belum dibuat", json.loads(buf.getvalue())["error"])

    def test_43_lokasi_db_env(self):
        lama = {k: os.environ.pop(k, None) for k in ("KOMUNITECH_KASIR_DB", "KOMUNITECH_DATA")}
        try:
            os.environ["KOMUNITECH_DATA"] = self.dir
            ns = K.buat_parser().parse_args(["info"])
            self.assertEqual(str(K.path_db(ns)), os.path.join(self.dir, "kasir", "kasir.db"))
            os.environ["KOMUNITECH_KASIR_DB"] = self.db
            self.assertEqual(str(K.path_db(ns)), self.db)
        finally:
            for k, v in lama.items():
                os.environ.pop(k, None)
                if v is not None:
                    os.environ[k] = v

    def test_44_backup_restore(self):
        self.jual("1 kopi hitam, bayar pas")
        b = self.ok("backup", "--label", "uji")["backup"]
        self.jual("1 es teh manis, bayar pas", "2026-09-24 11:00")
        self.assertEqual(self.ok("restore", "--dari", b)["mode"], "pratinjau")
        self.ok("restore", "--dari", b, "--ya")
        self.assertEqual(len(self.ok("nota", "--tanggal", "2026-09-24")["nota"]), 1)


class UjiPBJT(Dasar):
    """PBJT makanan/minuman (UU 1/2022): dasar = jumlah dibayar setelah diskon (Ps 57(1)), pokok = dasar x tarif
    Perda (Ps 59), dibulatkan ke bawah sekali; tanpa DPP 11/12."""

    def atur(self, *extra):
        return self.ok("atur", *extra, "--ya")

    def test_45_pbjt_belum(self):
        self.atur("--pajak", "pbjt-belum", "--tarif-pbjt", "10")
        # 51.000 - diskon 10% (5.100) = 45.900 ; PBJT = floor(10% x 45.900) = 4.590 ; total 50.490
        o = self.jual("2 kopi susu, 1 roti bakar, diskon 10%, bayar tunai 100rb")
        self.assertEqual((o["dpp"], o["pbjt"], o["ppn"], o["total"], o["kembalian"]), (45900, 4590, 0, 50490, 49510))
        self.assertEqual(o["jenis_pajak"], "PBJT")

    def test_46_pbjt_pembulatan_ke_bawah_tarif_pecahan(self):
        self.atur("--pajak", "pbjt-belum", "--tarif-pbjt", "2,5")
        # ETM 6.000 x 3 = 18.000 - 10%+5% (2.610) = 15.390 ; 2,5% x 15.390 = 384,75 -> 384 (ke bawah, bukan 385)
        o = self.jual("3 es teh manis diskon 10%+5%, bayar pas")
        self.assertEqual((o["pbjt"], o["total"]), (384, 15774))

    def test_47_pbjt_termasuk(self):
        self.atur("--pajak", "pbjt-termasuk", "--tarif-pbjt", "10")
        # 53.000: dasar = 48.182 (48.182 + floor(4.818,2)=4.818 = 53.000; 48.183 + 4.818 = 53.001 > 53.000)
        o = self.jual("2 kopi susu gula aren, 1 roti bakar keju, bayar qris")
        self.assertEqual((o["dpp"], o["pbjt"], o["total"], o["selisih_pembulatan"]), (48182, 4818, 53000, 0))
        # 100 termasuk 10%: dasar 91 -> 91 + 9 = 100 persis ; dasar 92 -> 92 + 9 = 101 > 100
        self.assertEqual(K.hitung_pajak(100, "pbjt-termasuk", "10"), {"dpp": 91, "ppn": 9, "total": 100, "sisa": 0})
        # 105 termasuk 10%: dasar 95 -> 95 + 9 = 104 ; dasar 96 -> 96 + 9 = 105 -> dasar 96, sisa 0
        self.assertEqual(K.hitung_pajak(105, "pbjt-termasuk", "10")["dpp"], 96)
        # retur 1 kopi: sisa 35.000 -> dasar 31.819 (31.819 + 3.181 = 35.000) ; koreksi = 3.181 - 4.818 = -1.637
        r = self.ok("retur", "--nota", o["no"], "--item", "1 kopi susu", "--alasan", "x", "--waktu", "2026-09-24 10:05",
                    "--ya")
        self.assertEqual((r["pbjt"], r["dpp"], r["total"]), (-1637, -16363, -18000))

    def test_48_pbjt_validasi(self):
        self.assertIn("tarif", self.gagal("atur", "--pajak", "pbjt-belum", "--ya")["error"])
        self.assertIn("10%", self.gagal("atur", "--pajak", "pbjt-belum", "--tarif-pbjt", "11", "--ya")["error"])
        self.gagal("atur", "--pajak", "pbjt-belum", "--tarif-pbjt", "0", "--ya")
        o = self.gagal("atur", "--pajak", "ppn-belum", "--pkp", "ya", "--tarif-pbjt", "10", "--ya")
        self.assertIn("4A", o["error"])                              # PPN + PBJT ditolak

    def test_49_service_charge(self):
        self.gagal("atur", "--pajak", "pbjt-belum", "--tarif-pbjt", "10", "--service-charge", "5", "--ya")  # kena? wajib
        self.atur("--pajak", "pbjt-belum", "--tarif-pbjt", "10", "--service-charge", "5", "--sc-kena-pajak", "ya")
        # 36.000 ; SC 5% = 1.800 ; dasar 37.800 ; PBJT 3.780 ; total 41.580
        o = self.jual("3 kopi hitam, bayar qris")
        self.assertEqual((o["service"], o["dpp"], o["pbjt"], o["total"]), (1800, 37800, 3780, 41580))
        self.atur("--sc-kena-pajak", "tidak")
        # SC tidak kena: dasar 36.000 ; PBJT 3.600 ; total 36.000 + 1.800 + 3.600 = 41.400
        o = self.jual("3 kopi hitam, bayar qris", "2026-09-24 11:00")
        self.assertEqual((o["dpp"], o["pbjt"], o["total"]), (36000, 3600, 41400))
        # retur 1 dari 3: sisa 24.000 ; SC 1.200 ; PBJT 2.400 ; total 27.600 -> koreksi 27.600 - 41.400 = -13.800
        r = self.ok("retur", "--nota", o["no"], "--item", "1 kopi hitam", "--alasan", "x", "--waktu",
                    "2026-09-24 11:05", "--ya")
        self.assertEqual((r["service"], r["pbjt"], r["total"]), (-600, -1200, -13800))
        self.assertIn("termasuk", self.gagal("atur", "--pajak", "pbjt-termasuk", "--ya")["error"])  # SC + termasuk

    def test_50_rekap_dan_struk_pbjt(self):
        self.atur("--pajak", "pbjt-belum", "--tarif-pbjt", "10")
        o = self.jual("2 kopi susu, 1 roti bakar, diskon 10%, bayar tunai 100rb")    # total 50.490, PBJT 4.590
        r = self.ok("rekap", "--bulan", "2026-09")
        # omzet tanpa PBJT = 50.490 - 4.590 = 45.900 (bahan pph-final-umkm)
        self.assertEqual((r["pbjt"], r["ppn"], r["total_diterima"], r["omzet_tanpa_pajak"]), (4590, 0, 50490, 45900))
        self.assertIn("PBJT dipungut", r["teks"])
        self.assertIn("Bapenda", r["teks"])
        s = self.ok("struk", "--nota", o["no"], "--teks")
        self.assertIn("PBJT 10%", s["teks"])
        self.assertIn("bukan faktur pajak", s["teks"])


class UjiSatuan(Dasar):
    def setUp(self):
        super().setUp()
        isi = ("Kode;Nama;Harga;Satuan\nSMN;Semen Tiga Roda 50 kg;65.000;sak\nCAT;Cat Tembok Putih;450.000;pail\n"
               "PSR;Pasir Beton;300.000;m3\nKWT;Kawat Bendrat;25.000;kg\nAQ;Aqua Gelas;25.000;dus\n"
               "KK;Kaos Kaki;5.000;pcs\nKRM;Keramik 40x40;60.000;m2\nBSI;Besi Beton;0,5;ton\n")
        self.ok("produk", "impor", self.file("tb.csv", isi.replace("0,5;ton", "12.000.000;ton")), "--ya")

    def test_51_satuan_depan_belakang(self):
        # 2 sak x 65.000 = 130.000 ; 1 pail x 450.000 ; semen 2 sak (belakang) ; 2 dus aqua
        o = self.jual("2 sak semen, 1 pail cat, 2 dus aqua")
        self.assertEqual([b["bruto"] for b in o["baris"]], [130000, 450000, 50000])
        self.assertEqual(self.jual("semen 3 sak", "2026-09-24 11:00")["total"], 195000)

    def test_52_satuan_pecahan_m3_m2_ton(self):
        # 0,5 m3 x 300.000 = 150.000 ; 12,5 m2 x 60.000 = 750.000 ; 0,25 ton x 12.000.000 = 3.000.000
        o = self.jual("0,5 m3 pasir, keramik 12,5 m2, 0,25 ton besi beton")
        self.assertEqual([b["bruto"] for b in o["baris"]], [150000, 750000, 3000000])
        self.assertIn("pecahan", self.gagal("jual", "--pesan", "1,5 sak semen")["error"])

    def test_53_satuan_berbeda_ditolak(self):
        self.assertIn("lusin", self.gagal("jual", "--pesan", "2 lusin kaos kaki")["error"])
        self.assertIn("'sak'", self.gagal("jual", "--pesan", "2 kg semen")["error"])
        self.assertEqual(self.jual("2 buah semen")["total"], 130000)            # satuan hitung generik boleh

    def test_54_retur_dengan_satuan(self):
        o = self.jual("2 sak semen, 0,75 kg kawat bendrat")
        # retur 0,25 kg dari 0,75 kg: nilai 18.750 -> sisa 18.750 - round(18.750 x 0,25/0,75 = 6.250) -> retur 6.250
        r = self.ok("retur", "--nota", o["no"], "--item", "0,25 kg kawat bendrat", "--item", "semen 1 sak",
                    "--alasan", "x", "--waktu", "2026-09-24 10:05", "--ya")
        self.assertEqual(r["total"], -(6250 + 65000))


class UjiV110Lain(Dasar):
    def test_55_zona_waktu(self):
        self.ok("atur", "--zona", "WITA", "--ya")
        self.assertEqual(self.ok("info")["pengaturan"]["zona"], "Asia/Makassar")
        self.gagal("atur", "--zona", "Eropa/Paris", "--ya")
        # waktu 'sekarang' dihitung di zona toko, bukan zona komputer
        waktu = K.sekarang(K.buat_parser().parse_args(["info"]))
        utc = K.datetime.now(K.timezone.utc).replace(tzinfo=None)
        self.assertLess(abs((waktu - utc).total_seconds() - 8 * 3600), 5)
        o = self.jual("1 kopi hitam, bayar pas")
        self.assertIn("WITA", self.ok("struk", "--nota", o["no"], "--teks")["teks"])

    def test_56_zona_fallback_offset_tetap(self):
        import builtins
        asli = builtins.__import__

        def palsu(nama, *a, **k):
            if nama == "zoneinfo":
                raise ImportError("tzdata tidak ada")
            return asli(nama, *a, **k)
        builtins.__import__ = palsu
        try:
            tz = K.tz_zona("Asia/Jayapura")
        finally:
            builtins.__import__ = asli
        self.assertEqual(tz.utcoffset(None), K.timedelta(hours=9))

    def test_57_info_peringatan_zona_komputer(self):
        lama = K.offset_komputer
        K.offset_komputer = lambda: K.timedelta(0)             # komputer/VPS memakai UTC
        try:
            o = self.ok("info")
        finally:
            K.offset_komputer = lama
        self.assertTrue(any("UTC+0" in p and "WIB" in p for p in o["peringatan"]))

    def test_58_csv_qty_minus_pecahan_tetap_angka(self):
        self.assertEqual(K.sel_aman("-2,5"), "-2,5")
        self.assertEqual(K.sel_aman("-5000"), "-5000")
        self.assertEqual(K.sel_aman("-cmd|calc"), "'-cmd|calc")
        o = self.jual("0,75 kg gula pasir, bayar pas")
        self.ok("retur", "--nota", o["no"], "--item", "0,5 kg gula pasir", "--alasan", "x", "--waktu",
                "2026-09-24 10:01", "--ya")
        out = os.path.join(self.dir, "j.csv")
        self.ok("ekspor", "--tanggal", "2026-09-24", "--csv", out)
        self.assertIn(";-0,5;", isi_file(out, "utf-8-sig"))

    def test_59_struk_emoji_dan_lebar(self):
        self.ok("atur", "--nama-toko", "Kafe \U0001F60A Senja — Fiktif", "--ya")
        self.ok("produk", "tambah", "--kode", "EM", "--nama", "Es Kopi \U0001F525\U0001F60A Spesial Panjang Sekali Nian",
                "--harga", "20rb", "--ya")
        self.ok("produk", "tambah", "--kode", "CJ", "--nama", "抹茶拿鐵", "--harga", "30rb", "--ya")
        self.jual("1 EM, 1 CJ, bayar pas")
        for kertas, lebar in (("58", 32), ("80", 48)):
            s = self.ok("struk", "--kertas", kertas, "--keluar", os.path.join(self.dir, "e%s.html" % kertas))
            self.assertTrue(all(K.lebar_tampil(b) <= lebar for b in s["baris"]), s["baris"])
            self.assertFalse(any("\U0001F60A" in b for b in s["baris"]))
        self.assertTrue(any("KAFE SENJA" in b for b in s["baris"]))

    def test_60_struk_teks_tidak_menambah_cetakan(self):
        o = self.jual("1 kopi hitam, bayar pas")
        self.ok("struk", "--nota", o["no"], "--teks")
        self.ok("struk", "--nota", o["no"], "--teks")
        s = self.ok("struk", "--nota", o["no"], "--keluar", os.path.join(self.dir, "a.html"))
        self.assertEqual(s["cetak_ke"], 1)
        self.assertNotIn("SALINAN", s["baris"][0])

    def test_61_pesan_setelah_tutup_kasir_dan_nama_kasir(self):
        self.ok("buka-kasir", "--kas-awal", "100rb", "--kasir", "Rina", "--waktu", "2026-09-24 07:00", "--ya")
        o = self.jual("1 kopi hitam, bayar pas", "2026-09-24 08:00")
        self.assertIn("Rina", "\n".join(self.ok("struk", "--nota", o["no"], "--teks")["baris"]))
        self.ok("tutup-kasir", "--kas-fisik", "112rb", "--waktu", "2026-09-24 20:00", "--ya")
        o = self.ok("jual", "--pesan", "1 kopi hitam, bayar pas", "--waktu", "2026-09-24 20:30")
        self.assertTrue(any("sudah DITUTUP" in p for p in o["peringatan"]))

    def test_62_impor_semua_rusak_alasan_per_baris(self):
        p = self.file("rusak.csv", "Kode;Nama;Harga\nA;Satu;0\nB;Dua;-5\n")
        o = self.gagal("produk", "impor", p)
        self.assertIn("baris 2", o["error"])
        self.assertIn("baris 3", o["error"])

    def test_63_struk_nota_asal_menyebut_retur(self):
        o = self.jual("3 es teh manis, bayar pas")
        self.ok("retur", "--nota", o["no"], "--item", "1 es teh", "--alasan", "x", "--waktu", "2026-09-24 10:01", "--ya")
        s = self.ok("struk", "--nota", o["no"], "--teks")
        self.assertIn("R-260924-0001", s["teks"])

    def test_64_migrasi_database_v100(self):
        con = sqlite3.connect(self.db)
        con.execute("CREATE TABLE nota_lama AS SELECT * FROM nota")
        kolom = [r[1] for r in con.execute("PRAGMA table_info(nota)") if r[1] not in
                 ("tarif_pajak", "service", "service_persen", "service_kena", "zona")]
        con.executescript("DROP TABLE nota; CREATE TABLE nota AS SELECT %s FROM nota_lama; DROP TABLE nota_lama;"
                          % ",".join(kolom))
        con.close()
        o = self.jual("1 kopi hitam, bayar pas")                  # kolom baru ditambahkan otomatis
        self.assertEqual(o["total"], 12000)



PRODUK_BOT_CSV = "Kode;Nama;Varian;Harga Jual;Satuan\nKH;Kopi Hitam;;8.000;cup\nKS;Kopi Susu;;12.000;cup\n" \
                 "ETM;Es Teh Manis;;5.000;gelas\nRB;Roti Bakar;Coklat;15.000;porsi\n"
PESAN_BOT = "2 kopi susu, 1 roti bakar, diskon 10%, bayar tunai 100rb"
KATA_JARGON = ("database", "dipetakan", "sistem kasir", "html", "file lokal", "sqlite", "json")
# Toko perlengkapan kasir/ATK: kata "struk" ADA di nama barang (bukan permintaan struk).
PRODUK_ATK_CSV = ("kode,nama,harga,satuan\nKR,Kertas,500,lembar\nKST,Kertas Struk,6000,roll\n"
                  "PS,Printer Struk,350000,pcs\nPI,Printer Inkjet,900000,pcs\n")


class UjiV118(Dasar):
    """v1.1.8 (temuan uji bot Telegram 17 Okt 2026): struk teks SELALU ikut di balasan setelah nota tersimpan, dan
    pemakaian pertama (produk + pengaturan + penjualan pertama) cukup SATU konfirmasi.
    Angka kunci uji bot (menu bot: Kopi Susu 12.000, Roti Bakar Coklat 15.000): 2 x 12.000 + 1 x 15.000 = 39.000;
    diskon 10% = 3.900; total 35.100; tunai 100.000; kembalian 64.900.
    Angka produk-contoh.csv (Kopi Susu Gula Aren 18.000): 2 x 18.000 + 15.000 = 51.000; diskon 5.100; total 45.900;
    kembalian 54.100."""

    def baru(self):
        """Folder kerja kosong (belum ada buku kasir) + file produk, seperti pembeli yang baru memasang skill."""
        self.dir2 = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.dir2, ignore_errors=True)
        self.db = os.path.join(self.dir2, "data", "kasir.db")
        self.csv = os.path.join(self.dir2, "produk.csv")
        with open(self.csv, "w", encoding="utf-8", newline="") as f:
            f.write(PRODUK_BOT_CSV)

    def mulai(self, *extra, pesan=PESAN_BOT):
        argv = ["mulai", "--produk", self.csv, "--nama-toko", "Warung Kopi Mbak Sri", "--alamat", "Jl. Melati 5, Bekasi"]
        if pesan:
            argv += ["--pesan", pesan]
        return self.ok(*(argv + list(extra)))

    def test_70_version_sama_di_semua_berkas(self):
        self.assertEqual(K.VERSI, "1.1.12")
        spec = importlib.util.spec_from_file_location("rekap_nota", os.path.join(AKAR, "scripts", "rekap_nota.py"))
        rn = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(rn)
        self.assertEqual(rn.VERSI, K.VERSI)
        self.assertIn("## Catatan revisi %s (2026-10-27)" % K.VERSI, isi_file(os.path.join(AKAR, "CHANGELOG.md")))
        self.assertIn("Versi terkini: **%s**" % K.VERSI, isi_file(os.path.join(AKAR, "README.md")))

    def test_71_jual_tersimpan_memuat_struk_teks_58mm(self):
        o = self.jual(PESAN_BOT)
        self.assertEqual((o["total"], o["kembalian"]), (45900, 54100))
        self.assertEqual(o["struk_kertas"], "58")
        self.assertTrue(o["struk_teks"].startswith("```\n") and o["struk_teks"].endswith("\n```"))
        self.assertTrue(all(len(b) <= 32 for b in o["struk_baris"]), o["struk_baris"])        # muat kertas 58 mm
        for kata in (o["no"], "Subtotal                  51.000", "Diskon 10%                -5.100", "Rp 45.900",
                     "Tunai                    100.000", "Kembalian                 54.100"):
            self.assertIn(kata, o["struk_teks"])
        self.assertIn(o["struk_teks"], o["teks"])                      # balasan yang disalin apa adanya sudah memuat struk
        self.assertNotIn("belum disimpan", o["teks"])
        s = self.ok("struk", "--nota", o["no"], "--teks")               # sama persis dengan perintah struk terpisah
        self.assertEqual(s["baris"], o["struk_baris"])

    def test_71b_permintaan_struk_di_kalimat_bukan_barang(self):
        """Kalimat nyata uji bot: '..., terus bikinin struknya ya' dulu ditolak sebagai produk tak dikenal."""
        for tambahan in (", terus bikinin struknya ya", " terus bikinin struknya ya", ", tolong cetak struk",
                         " dan struknya", ", bikinin struk dong", ", struk"):
            o = self.ok("jual", "--pesan", PESAN_BOT + tambahan, "--waktu", "2026-09-24 10:00")
            self.assertEqual((o["total"], o["kembalian"]), (45900, 54100), tambahan)
            self.assertEqual([b["kode"] for b in o["baris"]], ["KSGA", "RB"], tambahan)
        self.gagal("jual", "--pesan", "2 kopi susu, 1 nasi rendang, bikinin struknya")   # produk asing tetap ditolak

    def test_72_jual_struk_80mm_bila_kertas_80(self):
        self.ok("atur", "--kertas", "80", "--ya")
        o = self.jual("3 es teh manis, bayar pas")
        self.assertEqual(o["struk_kertas"], "80")
        self.assertTrue(all(len(b) <= 48 for b in o["struk_baris"]))
        self.assertTrue(any(len(b) > 32 for b in o["struk_baris"]))

    def test_73_pratinjau_jual_tidak_mengubah_buku_dan_tetap_ada_struk_teks(self):
        o = self.ok("jual", "--pesan", PESAN_BOT, "--waktu", "2026-09-24 10:00")
        self.assertEqual(o["mode"], "pratinjau")
        self.assertTrue(o["perlu_konfirmasi"])
        self.assertIn("belum disimpan", o["teks"])
        self.assertIn("struk_teks", o)
        self.assertEqual(self.ok("info")["nota"], 0)
        nyata = self.jual(PESAN_BOT)                                   # nomor & struk pratinjau = yang benar-benar tersimpan
        self.assertEqual((nyata["no"], nyata["struk_baris"]), (o["no"], o["struk_baris"]))

    def test_74_pengingat_kasir_belum_dibuka_singkat_dan_awam(self):
        o = self.jual("1 kopi hitam, bayar pas")
        ingat = [p for p in o["peringatan"] if "dibuka" in p]
        self.assertEqual(len(ingat), 1, o["peringatan"])
        self.assertLess(len(ingat[0]), 190)
        for jargon in ("buka-kasir", "--waktu", "--kas-awal", "sesi"):
            self.assertNotIn(jargon, ingat[0])
        self.assertIn("buka kasir, modal", ingat[0])
        self.ok("buka-kasir", "--kas-awal", "100rb", "--waktu", "2026-09-24 07:00", "--ya")
        self.assertFalse([p for p in self.jual("1 es teh manis, bayar pas")["peringatan"] if "dibuka" in p])

    def test_75_mulai_pratinjau_satu_pesan_tidak_menulis_apa_pun(self):
        self.baru()
        o = self.mulai()
        self.assertEqual((o["mode"], o["perlu_konfirmasi"]), ("pratinjau", True))
        self.assertFalse(os.path.exists(os.path.dirname(self.db)), "pratinjau tidak boleh membuat folder/buku kasir")
        self.assertEqual((o["produk_baru"], o["total"], o["kembalian"], o["no"]), (4, 35100, 64900, "N-260924-0001"))
        t = o["teks"]
        for bagian in ("DAFTAR PRODUK - 4 produk", "Kopi Susu - Rp 12.000/cup", "Roti Bakar Coklat - Rp 15.000/porsi",
                       "Warung Kopi Mbak Sri | Jl. Melati 5, Bekasi", "Saya anggap - koreksi bila beda:",
                       "nota N-260924-0001 (belum disimpan)", "Total Rp 35.100", "Kembalian Rp 64.900",
                       'Balas "ya" kalau sudah sesuai'):
            self.assertIn(bagian, t)
        self.assertIn(o["struk_teks"], t)                               # struk teks ikut di pesan konfirmasi PERTAMA
        self.assertTrue(all(len(b) <= 32 for b in o["struk_baris"]))
        for jargon in KATA_JARGON:
            self.assertNotIn(jargon, t.lower())

    def test_76_mulai_asumsi_ditandai_dan_hilang_bila_disebut(self):
        self.baru()
        o = self.mulai()
        gabung = " | ".join(o["asumsi"])
        for kata in ("tanpa pajak", "kertas 58 mm", "stok barang tidak dihitung", "WIB", "tanpa nomor telepon"):
            self.assertIn(kata, gabung)
        self.assertNotIn("tanpa alamat", gabung)                         # alamat sudah disebut pengguna
        self.assertNotIn("sudah saya buat", o["teks"])                    # asumsi tidak boleh ditulis seperti fakta
        o2 = self.mulai("--pajak", "tanpa", "--kertas", "80", "--telp", "0812", "--stok", "tidak", "--zona", "WIB")
        self.assertEqual(o2["asumsi"], [])
        self.assertNotIn("Saya anggap", o2["teks"])
        self.assertEqual(o2["struk_kertas"], "80")
        self.assertTrue(any(len(b) > 32 for b in o2["struk_baris"]))
        o3 = self.mulai("--kertas", "80")                                 # koreksi pengguna: kertas tidak lagi asumsi
        self.assertFalse([a for a in o3["asumsi"] if "kertas" in a])

    def test_77_mulai_ya_menyimpan_semuanya_dan_sama_dengan_pratinjau(self):
        self.baru()
        pratinjau = self.mulai()
        o = self.mulai("--ya")
        self.assertEqual((o["mode"], o["perlu_konfirmasi"]), ("tersimpan", False))
        for k in ("no", "total", "kembalian", "struk_baris", "produk_baru"):
            self.assertEqual(o[k], pratinjau[k], k)                      # waktu tetap (--hari-ini) -> struk identik
        self.assertTrue(o["teks"].startswith("TERSIMPAN."))
        self.assertIn(o["struk_teks"], o["teks"])
        self.assertIn("Pengaturan yang dipakai: tanpa pajak, struk kertas 58 mm", o["teks"])
        info = self.ok("info")
        self.assertEqual((info["produk_aktif"], info["nota"]), (4, 1))
        self.assertEqual(info["pengaturan"]["nama_toko"], "Warung Kopi Mbak Sri")
        self.assertEqual(self.ok("struk", "--nota", o["no"], "--teks")["baris"], o["struk_baris"])
        kode, out = self.run_cli("mulai", "--produk", self.csv, "--nama-toko", "Lain")     # tidak menimpa buku kasir
        self.assertEqual(kode, 1)
        self.assertIn("sudah ada", out["error"])

    def test_78_mulai_gagal_tidak_menyentuh_buku_kasir(self):
        self.baru()
        for pesan, kata in (("2 kopi susu, 1 nasi rendang, bayar tunai 100rb", "nasi rendang"),
                            ("2 kopi susu, bayar tunai 10rb", "KURANG")):
            for ya in ([], ["--ya"]):
                kode, out = self.run_cli("mulai", "--produk", self.csv, "--nama-toko", "Toko", "--pesan", pesan, *ya)
                self.assertEqual(kode, 1, out)
                self.assertIn(kata, out["error"])
                self.assertFalse(os.path.exists(os.path.dirname(self.db)), "gagal tidak boleh meninggalkan buku kasir setengah jadi")
        kode, out = self.run_cli("mulai", "--produk", os.path.join(self.dir2, "tidak-ada.csv"), "--nama-toko", "Toko", "--ya")
        self.assertEqual(kode, 1, out)
        self.assertFalse(os.path.exists(os.path.dirname(self.db)))

    def test_79_mulai_tanpa_pesan_hanya_produk_dan_toko(self):
        self.baru()
        p = self.mulai(pesan=None)
        self.assertEqual((p["mode"], p["produk_baru"], "struk_teks" in p), ("pratinjau", 4, False))
        self.assertNotIn("Penjualan pertama", p["teks"])
        self.assertFalse(os.path.exists(os.path.dirname(self.db)))
        o = self.mulai("--ya", pesan=None)
        self.assertEqual((o["produk_baru"], "no" in o, "struk_teks" in o), (4, False, False))
        info = self.ok("info")
        self.assertEqual((info["produk_aktif"], info["nota"]), (4, 0))

    def test_80_mulai_catatan_dan_pembayaran_lain(self):
        self.baru()
        o = self.mulai("--ya", "--kasir", "Rina", "--catatan", "meja 4", pesan="2 kopi hitam, bayar qris")
        self.assertEqual((o["total"], o["kembalian"]), (16000, 0))
        self.assertIn("QRIS", o["struk_teks"])
        self.assertIn("Rina", o["struk_teks"])
        self.assertIn("meja 4", o["struk_teks"])

    def test_81_kata_struk_di_dalam_nama_barang_tidak_pernah_dibuang(self):
        """Temuan penguji independen: 'struk' dulu dibuang dari mana saja, jadi '2 kertas struk' tercatat sebagai
        2 x Kertas (Rp 1.000) padahal Kertas Struk (2 x Rp 6.000 = Rp 12.000). Produk tidak boleh berganti diam-diam."""
        self.db = os.path.join(self.dir, "atk.db")
        self.ok("init", "--nama-toko", "Toko ATK", "--ya")
        self.ok("produk", "impor", self.file("atk.csv", PRODUK_ATK_CSV), "--ya")
        for pesan in ("2 kertas struk, bayar pas", "2 kertas struk, bayar pas, terus bikinin struknya ya",
                      "2 kertas struk bikinin struknya, bayar pas", "kertas struk x2, sama struknya, bayar pas"):
            o = self.ok("jual", "--pesan", pesan, "--waktu", "2026-09-24 10:00")
            self.assertEqual([(b["kode"], b["qty"]) for b in o["baris"]], [("KST", 2)], pesan)
            self.assertEqual(o["total"], 12000, pesan)
            self.assertFalse([p for p in o["peringatan"] if "dibaca sebagai" in p], pesan)
        o = self.ok("jual", "--pesan", "1 printer struk, bayar pas", "--waktu", "2026-09-24 10:00")
        self.assertEqual((o["baris"][0]["kode"], o["total"]), ("PS", 350000))
        o = self.ok("jual", "--pesan", "2 kertas, bayar tunai 10rb struknya ya", "--waktu", "2026-09-24 10:00")
        self.assertEqual((o["baris"][0]["kode"], o["total"], o["kembalian"]), ("KR", 1000, 9000))
        # nama yang tidak ada ditolak jelas dengan saran, tidak diam-diam diganti produk lain
        for pesan in ("1 printer struk bluetooth, bayar pas", "2 kertas cetak struk, bayar pas"):
            o = self.gagal("jual", "--pesan", pesan, "--waktu", "2026-09-24 10:00")
            self.assertIn("tidak dikenal", o["error"], pesan)
            self.assertEqual(self.ok("info")["nota"], 0)

    def test_82_variasi_ucapan_penutup_struk_diterima(self):
        for tambahan in (", terus kirim struknya ke sini ya", ", struknya kirim ya", ". Bikinin struknya ya",
                         ". Tolong, bikinin struknya ya", " bikinin struknya ya", ", sama struknya",
                         ", sekalian struknya", ", minta struknya dong", ", trus print struknya", "."):
            o = self.ok("jual", "--pesan", PESAN_BOT + tambahan, "--waktu", "2026-09-24 10:00")
            self.assertEqual((o["total"], o["kembalian"]), (45900, 54100), tambahan)
            self.assertEqual([b["kode"] for b in o["baris"]], ["KSGA", "RB"], tambahan)
        # ukuran kertas bukan bagian pesanan: ditolak jelas (agent membuangnya dan memakai --kertas)
        o = self.gagal("jual", "--pesan", PESAN_BOT + ", bikinin struk 58mm ya", "--waktu", "2026-09-24 10:00")
        self.assertIn("struk 58mm", o["error"])
        self.assertEqual(self.ok("jual", "--pesan", PESAN_BOT, "--waktu", "2026-09-24 10:00")["total"], 45900)

    def test_83_awalan_catat_penjualan_bukan_barang(self):
        """Bentuk pesan uji bot: 'Tolong catat penjualan: 2 kopi susu, ...' dulu ditolak sebagai produk tak dikenal."""
        for awal in ("Tolong catat penjualan: ", "catat penjualan ", "tolong catat penjualan baru ini: ", "Catat: ",
                     "Penjualan: ", "masukin transaksi tadi: ", ""):
            o = self.ok("jual", "--pesan", awal + PESAN_BOT + ", terus bikinin struknya ya", "--waktu",
                        "2026-09-24 10:00")
            self.assertEqual((o["total"], o["kembalian"]), (45900, 54100), awal)
            self.assertEqual([b["kode"] for b in o["baris"]], ["KSGA", "RB"], awal)
        o = self.ok("jual", "--pesan", "catatan: meja 4, 2 kopi hitam, bayar pas", "--waktu", "2026-09-24 10:00")
        self.assertEqual((o["baris"][0]["kode"], o["total"]), ("KH", 24000))      # 'catatan' tetap catatan, bukan awalan
        self.assertIn("meja 4", o["struk_teks"])

    def test_84_buku_belum_ada_menunjuk_ke_mulai_bukan_init(self):
        self.baru()
        for perintah in (["info"], ["jual", "--pesan", PESAN_BOT]):
            kode, out = self.run_cli(*perintah)
            self.assertEqual(kode, 1, out)
            self.assertIn("Buku kasir belum dibuat", out["error"])
            self.assertIn("mulai --produk FILE", out["catatan_agent"])      # petunjuk agent pindah ke field sendiri
            self.assertNotIn("mulai", out["error"])
            self.assertNotIn("Database", out["error"])
        self.assertFalse(os.path.exists(os.path.dirname(self.db)))

    def test_85_pengingat_kasir_satu_kalimat_dan_tidak_bertentangan_dengan_pratinjau(self):
        def kalimat(teks):
            return [x for x in re.split(r"(?<=[.!?])\s+", teks.strip()) if x]
        o = self.jual("1 kopi hitam, bayar pas")
        ingat = [p for p in o["peringatan"] if "dibuka" in p]
        self.assertEqual(len(ingat), 1)
        self.assertEqual(len(kalimat(ingat[0])), 1, ingat[0])                  # SKILL.md: "satu kalimat"
        self.assertNotIn("tersimpan", ingat[0])                                 # pratinjau berkata "belum ada yang disimpan"
        self.ok("buka-kasir", "--kas-awal", "100rb", "--waktu", "2026-09-24 07:00", "--ya")
        self.ok("tutup-kasir", "--kas-fisik", "100rb", "--waktu", "2026-09-24 08:00", "--ya")
        o = self.ok("jual", "--pesan", "1 kopi hitam, bayar pas", "--waktu", "2026-09-24 20:30")
        ditutup = [p for p in o["peringatan"] if "DITUTUP" in p]
        self.assertEqual(len(ditutup), 1)
        self.assertEqual(len(kalimat(ditutup[0])), 1, ditutup[0])
        self.baru()
        t = self.mulai()["teks"]
        self.assertIn("belum ada yang disimpan", t)
        self.assertIn('Kasir belum "dibuka"', t)
        self.assertNotIn("tersimpan", t.lower().replace("belum ada yang disimpan", ""))

    def test_86_jawaban_sama_dengan_asumsi_menghasilkan_catatan_yang_sama(self):
        """SKILL.md A.3: 'tanpa pajak, 58mm, stok tidak dilacak, simpan aja' = setuju. Dua cara agent menjalankannya
        (perintah sama + --ya, atau perintah dengan opsi yang menyebut asumsi itu + --ya) harus identik."""
        self.baru()
        a = self.mulai("--ya")
        self.baru()
        b = self.mulai("--pajak", "tanpa", "--stok", "tidak", "--kertas", "58", "--ya")
        for k in ("no", "total", "kembalian", "struk_baris", "produk_baru"):
            self.assertEqual(a[k], b[k], k)
        self.assertEqual((b["total"], b["kembalian"], b["struk_kertas"]), (35100, 64900, "58"))
        self.assertTrue(all(len(x) <= 32 for x in b["struk_baris"]))

    def test_87_changelog_menyebut_jumlah_uji_v118_dengan_benar(self):
        jumlah = len([n for n in UjiV118.__dict__ if n.startswith("test_")])
        self.assertIn("`UjiV118` (%d uji)" % jumlah, isi_file(os.path.join(AKAR, "CHANGELOG.md")))


POLA_FLAG = re.compile(r"--[a-z]")
KATA_AGEN = ("kasir.py", "perintah yang sama", "produk impor", "produk ubah", ".db", ".html", ".csv", "backup-kasir")


class UjiV119(Dasar):
    """v1.1.9: field yang ditempel agent ke chat bebas dari instruksi agent, nama perintah/opsi, dan jalur berkas;
    awalan 'catat penjualan:' tidak lagi memakan nama produk seperti 'masuk angin' / 'input data'."""

    def bersih(self, teks, msg=""):
        self.assertIsInstance(teks, str)
        self.assertIsNone(POLA_FLAG.search(teks), (msg, teks))
        for kata in KATA_AGEN + (self.dir, tempfile.gettempdir()):
            self.assertNotIn(kata, teks, (msg, teks))

    def baru(self):
        self.dir2 = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.dir2, ignore_errors=True)
        self.db = os.path.join(self.dir2, "data", "kasir.db")
        self.csv = os.path.join(self.dir2, "produk.csv")
        with open(self.csv, "w", encoding="utf-8", newline="") as f:
            f.write(PRODUK_BOT_CSV)

    def mulai(self, *extra):
        return self.ok("mulai", "--produk", self.csv, "--nama-toko", "Warung Kopi", "--pesan", PESAN_BOT, *extra)

    def test_90_pratinjau_berakhir_balas_ya_tanpa_instruksi_agen(self):
        o = self.ok("jual", "--pesan", PESAN_BOT, "--waktu", "2026-09-24 10:00")
        self.assertEqual(o["mode"], "pratinjau")
        self.assertTrue(o["teks"].rstrip().endswith('Simpan? Balas "ya".'), o["teks"])
        self.bersih(o["teks"])
        self.assertIn("--ya", o["catatan_agent"])                      # petunjuk agent ada, tapi di field terpisah
        self.jual("2 kopi hitam, bayar pas")
        o = self.ok("void", "--nota", "N-260924-0001", "--alasan", "salah input", "--waktu", "2026-09-24 11:00")
        self.assertTrue(o["teks"].rstrip().endswith('Simpan? Balas "ya".'), o["teks"])
        self.bersih(o["teks"])

    def test_91_jual_tersimpan_dan_struk_tanpa_jalur_berkas(self):
        o = self.jual(PESAN_BOT, "2026-09-24 10:00", "--struk", "58")
        self.bersih(o["teks"])
        self.bersih(o["struk_teks"])
        self.assertTrue(os.path.isfile(o["berkas_struk"]))              # jalur ada, tapi di field terpisah
        self.assertEqual(o["berkas_struk"], o["struk"])
        self.assertEqual((o["total"], o["kembalian"]), (45900, 54100))   # angka sama dengan 1.1.8
        s = self.ok("struk", "--nota", o["no"], "--kertas", "80")
        self.bersih(s["teks"])
        self.assertTrue(os.path.isfile(s["berkas_struk"]))
        self.assertIn("berkas_struk", s["catatan_agent"])
        t = self.ok("struk", "--nota", o["no"], "--teks")
        self.bersih(t["teks"])

    def test_92_mulai_pratinjau_dan_tersimpan_bersih_jalur_di_field_terpisah(self):
        self.baru()
        o = self.mulai()
        self.assertEqual(o["mode"], "pratinjau")
        for kunci in ("teks", "struk_teks"):
            self.bersih(o[kunci], kunci)
            self.bersih(o[kunci].replace(self.dir2, ""), kunci)
            self.assertNotIn(self.dir2, o[kunci])
        self.assertIn('Balas "ya"', o["teks"])
        self.assertEqual(o["lokasi_buku"], self.db)
        self.assertEqual((o["total"], o["kembalian"]), (35100, 64900))
        o = self.mulai("--ya")
        for kunci in ("teks", "struk_teks"):
            self.assertNotIn(self.dir2, o[kunci])
            self.assertIsNone(POLA_FLAG.search(o[kunci]), o[kunci])
        self.assertNotIn("kasir.db", o["teks"])
        self.assertEqual((o["total"], o["kembalian"]), (35100, 64900))

    def test_93_mulai_buku_sudah_ada_pesan_kata_awam(self):
        self.baru()
        self.mulai("--ya")
        kode, out = self.run_cli("mulai", "--produk", self.csv, "--nama-toko", "Warung Kopi", "--pesan", PESAN_BOT)
        self.assertEqual(kode, 1)
        for kata in ("produk impor", "kasir.py", "--"):
            self.assertNotIn(kata, out["error"])
        self.assertIsNone(re.search(r"\bjual\b", out["error"]))
        self.assertNotIn(self.dir2, out["error"])
        self.assertIn("sudah ada", out["error"])
        self.assertIn("produk impor", out["catatan_agent"])
        self.assertEqual(out["lokasi_buku"], self.db)

    def test_94_pesan_galat_tanpa_opsi_atau_jalur(self):
        """Galat yang bisa sampai ke pemilik: nama opsi dan perintah dipindah ke catatan_agent."""
        kasus = [
            ("void", "--nota", "N-260924-0001"),                         # alasan kosong
            ("kas",),                                                     # masuk/keluar kosong
            ("kas", "--keluar", "5rb"),                                   # catatan kosong
            ("tutup-kasir", "--kas-fisik", "0"),                          # kasir belum dibuka
            ("jual", "--pesan", "bayar tunai 5rb"),                      # tidak ada barang
            ("jual", "--pesan", "2 kopi hitam @9rb"),                    # harga di pesanan
            ("init", "--nama-toko", "X", "--pajak", "pbjt-belum"),       # tarif PBJT kosong
            ("atur",),                                                    # tak ada yang diubah
            ("stok", "--kode", "KH"),                                     # jumlah kosong
        ]
        for argv in kasus:
            try:
                kode, out = self.run_cli(*argv)
            except SystemExit:    # salah tulis opsi oleh agent (bukan galat untuk pemilik)
                continue
            if kode == 0:      # perintah yang butuh buku baru bisa lolos; hanya galat yang diperiksa
                continue
            self.bersih(out["error"], argv)
            self.assertTrue(out.get("catatan_agent") or "--" not in out["error"], argv)
        self.jual("2 kopi hitam, bayar pas")
        kode, out = self.run_cli("jual", "--pesan", "2 kopi hitam, bayar pas", "--waktu", "2026-09-24 10:03", "--ya")
        self.assertEqual(kode, 1)
        self.bersih(out["error"])
        self.assertIn("--izinkan-duplikat", out["catatan_agent"])
        o = self.ok("jual", "--pesan", "2 kopi hitam, bayar pas", "--waktu", "2026-09-24 10:04")
        for p in o["peringatan"]:
            self.bersih(p)

    def test_95_backup_info_ekspor_rekap_tanpa_jalur_di_teks(self):
        self.jual("2 kopi hitam, bayar pas")
        self.bersih(self.ok("info")["teks"])
        b = self.ok("backup")
        self.bersih(b["teks"])
        self.assertTrue(os.path.isfile(b["berkas_backup"]))
        d = self.ok("backup", "--daftar")
        self.bersih(d["teks"])
        self.assertEqual(len(d["berkas_backup"]), len(d["backup"]))
        r = self.ok("restore", "--dari", b["berkas_backup"])
        self.bersih(r["teks"])
        self.assertTrue(r["teks"].rstrip().endswith('Simpan? Balas "ya".'))
        r = self.ok("restore", "--dari", b["berkas_backup"], "--ya")
        self.bersih(r["teks"])
        for fmt in ("penjualan", "buku-stok"):
            e = self.ok("ekspor", "--format", fmt, "--tanggal", "2026-09-24", "--csv", os.path.join(self.dir, "e.csv"))
            self.bersih(e["teks"], fmt)
            self.assertTrue(os.path.isfile(e["berkas_csv"]))
        rk = self.ok("rekap", "--tahun", "2026", "--csv", os.path.join(self.dir, "r.csv"),
                     "--csv-produk", os.path.join(self.dir, "p.csv"))
        self.bersih(rk["teks"])
        self.assertTrue(os.path.isfile(rk["berkas_csv"]) and os.path.isfile(rk["berkas_csv_produk"]))
        self.assertIn("perintah_pph_final", rk)

    def test_96_awalan_hanya_dibuang_bila_jelas_awalan(self):
        pecah = K.pecah_pesan
        for tak_dibuang in ("masuk angin=2", "input data 1", "Masuk Angin 2, bayar pas", "masuk-angin 2",
                            "Rekam Jejak 1", "masukkan angin 2"):
            self.assertEqual(pecah(tak_dibuang)[0].lower(), tak_dibuang.split(",")[0].lower(), tak_dibuang)
        for kalimat, hasil in (("Tolong catat penjualan: 2 kopi", "2 kopi"), ("catat penjualan 2 kopi", "2 kopi"),
                               ("catat: 2 kopi", "2 kopi"), ("input transaksi hari ini: 1 roti", "1 roti"),
                               ("masukkan pesanan baru: 2 teh", "2 teh"), ("rekam nota 2 kopi", "2 kopi"),
                               ("penjualan 2 kopi", "2 kopi"), ("catat - 2 kopi", "2 kopi"),
                               ("coba catatkan penjualan: 2 kopi, bayar pas", "2 kopi"),
                               ("catatan: meja 4, 2 kopi", "catatan: meja 4"),
                               ("catat 2 kopi hitam, bayar pas", "2 kopi hitam"), ("input 3 teh", "3 teh")):
            self.assertEqual(pecah(kalimat)[0], hasil, kalimat)

    def test_97_produk_bernama_mirip_awalan_tetap_terjual(self):
        self.ok("produk", "tambah", "--kode", "MA", "--nama", "Masuk Angin", "--harga", "4000", "--satuan", "sachet", "--ya")
        self.ok("produk", "tambah", "--kode", "ID", "--nama", "Input Data", "--harga", "7000", "--satuan", "pcs", "--ya")
        for pesan, kode, total in (("masuk angin 2, bayar pas", "MA", 8000), ("input data 1, bayar pas", "ID", 7000),
                                   ("Tolong catat penjualan: masuk angin 3, bayar pas", "MA", 12000),
                                   ("catat: input data x2, bayar pas", "ID", 14000), ("MA=2, bayar pas", "MA", 8000),
                                   ("masuk angin x2, bayar pas", "MA", 8000)):
            o = self.ok("jual", "--pesan", pesan, "--waktu", "2026-09-24 10:00")
            self.assertEqual(([b["kode"] for b in o["baris"]], o["total"]), ([kode], total), pesan)

    def test_98_angka_tidak_berubah_dari_118(self):
        o = self.jual("2 kopi susu gula aren, 1 roti bakar, diskon 10%, bayar tunai 100rb")
        self.assertEqual((o["total"], o["kembalian"]), (45900, 54100))
        o = self.jual("1,5 kg gula pasir, 3 es teh manis, bayar tunai 50rb", "2026-09-24 11:00")
        self.assertEqual((o["total"], o["kembalian"]), (42750, 7250))

    def test_98b_skill_md_satu_aturan_berkas_dan_frontmatter(self):
        t = isi_file(os.path.join(AKAR, "SKILL.md"))
        self.assertLess(len(t.splitlines()), 300)
        kepala = t.split("---")[1]
        self.assertEqual(sorted(l.split(":")[0] for l in kepala.strip().splitlines()), ["description", "name"])
        self.assertIn("tersimpan di komputer ini", t)
        self.assertIn("catatan_agent", t)
        self.assertNotIn("jangan menulis file baru tanpa menyebut lokasinya", t)     # bertentangan dengan aturan chat
        self.assertEqual(t.count("Satu aturan untuk semua berkas"), 1)

    def test_99_changelog_menyebut_jumlah_uji_v119_dengan_benar(self):
        jumlah = len([n for n in UjiV119.__dict__ if n.startswith("test_")])
        self.assertIn("`UjiV119` (%d uji)" % jumlah, isi_file(os.path.join(AKAR, "CHANGELOG.md")))


class UjiV1110(Dasar):
    """v1.1.10 (temuan verifikator atas draf 1.1.9): galat `error` tanpa nama perintah/jalur berkas, frasa
    'catat 2 kopi hitam' dipahami lagi, klaim penutup pratinjau jujur, dokumen disamakan."""

    KATA_PERINTAH = ("buka-kasir", "tutup-kasir", "kasir.py", "database", "restore", "produk impor", "mulai --")

    def bersih_error(self, teks, msg=""):
        self.assertIsNone(POLA_FLAG.search(teks), (msg, teks))
        self.assertNotIn(self.dir, teks)
        self.assertNotIn(tempfile.gettempdir(), teks)
        self.assertIsNone(re.search(r"(?i)\bfile\b", teks), (msg, teks))
        for kata in self.KATA_PERINTAH + (".db", ".csv", ".html"):
            self.assertNotIn(kata, teks, (msg, teks))

    def main_json(self, *argv):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
            kode = K.main(list(argv) + ["--json"])
        return kode, json.loads(buf.getvalue())

    def test_100_kas_sebelum_kasir_dibuka_galat_awam(self):
        kode, o = self.run_cli("kas", "--keluar", "20rb", "--catatan", "es batu")
        self.assertEqual(kode, 1)
        self.bersih_error(o["error"])
        self.assertIn("belum dibuka", o["error"])
        self.assertIn("buka-kasir", o["catatan_agent"])

    def test_101_buka_kasir_dua_kali_galat_awam(self):
        self.ok("buka-kasir", "--kas-awal", "100rb", "--ya")
        kode, o = self.run_cli("buka-kasir", "--kas-awal", "100rb", "--ya")
        self.assertEqual(kode, 1)
        self.bersih_error(o["error"])
        self.assertIn("sudah dibuka", o["error"])
        self.assertIn("tutup-kasir", o["catatan_agent"])

    def test_102_galat_berkas_tanpa_jalur_jalur_di_field_terpisah(self):
        hilang = os.path.join(self.dir, "tidakada.csv")
        kode, o = self.run_cli("produk", "impor", hilang, "--ya")
        self.assertEqual(kode, 1)
        self.bersih_error(o["error"], "csv hilang")
        self.assertEqual(o["berkas_csv_produk"], hilang)
        kosong = self.file("kosong.csv", "")
        kode, o = self.run_cli("produk", "impor", kosong, "--ya")
        self.assertEqual(kode, 1)
        self.bersih_error(o["error"], "csv kosong")
        self.assertEqual(o["berkas_csv_produk"], kosong)
        bukan = self.file("lain.db", "ini bukan buku kasir")
        kode, o = self.main_json("info", "--db", bukan)
        self.assertEqual(kode, 1)
        self.bersih_error(o["error"], "bukan buku kasir")
        self.assertIn("bukan buku kasir", o["error"])
        self.assertEqual(o["lokasi_buku"], bukan)
        lain = os.path.join(self.dir, "lain2.db")
        sqlite3.connect(lain).execute("CREATE TABLE meta(kunci TEXT, nilai TEXT)").connection.close()
        kode, o = self.main_json("info", "--db", lain)
        self.assertEqual(kode, 1)
        self.bersih_error(o["error"], "db asing")
        self.assertEqual(o["lokasi_buku"], lain)
        gaib = os.path.join(self.dir, "gaib.db")
        kode, o = self.run_cli("restore", "--dari", gaib)
        self.assertEqual(kode, 1)
        self.bersih_error(o["error"], "restore")
        self.assertEqual(o["berkas_backup"], gaib)

    def test_103_semua_galat_di_kode_tanpa_nama_perintah_dan_jalur(self):
        """Sapuan statis: kalimat pertama setiap `Gagal(...)` tidak boleh memuat nama perintah, opsi, atau 'File %s'."""
        import ast
        src = isi_file(os.path.join(AKAR, "scripts", "kasir.py"))
        diperiksa = 0
        for n in ast.walk(ast.parse(src)):
            if isinstance(n, ast.Call) and getattr(n.func, "id", "") == "Gagal" and n.args:
                seg = ast.get_source_segment(src, n.args[0])
                diperiksa += 1
                for kata in ("-kasir", "--", "database", "kasir.py", "File %s", "File backup", "produk impor", "mulai --"):
                    self.assertNotIn(kata, seg, (n.lineno, seg))
                self.assertIsNone(re.search(r"\b(?:restore|init)\b", seg), (n.lineno, seg))
        self.assertGreater(diperiksa, 80)

    def test_104_catat_kata_kerja_plus_angka_dipahami_seperti_118(self):
        self.ok("produk", "tambah", "--kode", "MA", "--nama", "Masuk Angin", "--harga", "4000", "--satuan", "sachet", "--ya")
        self.ok("produk", "tambah", "--kode", "ID", "--nama", "Input Data", "--harga", "7000", "--satuan", "pcs", "--ya")
        for pesan, kode, total in (("catat 2 kopi hitam, bayar pas", "KH", None), ("input 3 kopi hitam, bayar pas", "KH", None),
                                   ("MA=2, bayar pas", "MA", 8000), ("input data 1, bayar pas", "ID", 7000),
                                   ("masuk angin 2, bayar pas", "MA", 8000)):
            kode_cli, o = self.run_cli("jual", "--pesan", pesan, "--waktu", "2026-09-24 10:00")
            if kode == "KH" and kode_cli == 1:
                self.fail((pesan, o))                          # produk Kopi Hitam ada di katalog contoh bila dikenal
            self.assertEqual(kode_cli, 0, (pesan, o))
            self.assertEqual([b["kode"] for b in o["baris"]], [kode if kode != "KH" else o["baris"][0]["kode"]], pesan)
            if total:
                self.assertEqual(o["total"], total, pesan)
        self.assertEqual(K.pecah_pesan("catat 2 kopi hitam, bayar pas")[0], "2 kopi hitam")

    def test_109_catat_angka_kata_dan_qty_di_belakang(self):
        """Temuan verifikator: 'catat dua kopi hitam' (angka kata) dan 'catat kopi hitam 2' (qty di akhir) harus terbaca;
        nama barang 'masuk angin' / 'input data' tetap utuh; kerusakan sqlite non-kunci memberi catatan_agent."""
        self.ok("produk", "tambah", "--kode", "MA", "--nama", "Masuk Angin", "--harga", "4000", "--satuan", "sachet", "--ya")
        self.ok("produk", "tambah", "--kode", "ID", "--nama", "Input Data", "--harga", "7000", "--satuan", "pcs", "--ya")
        self.assertEqual(K.pecah_pesan("catat dua kopi hitam, bayar pas")[0], "dua kopi hitam")
        self.assertEqual(K.pecah_pesan("masuk angin=2")[0], "masuk angin=2")
        self.assertEqual(K.pecah_pesan("input data 1")[0], "input data 1")
        for pesan in ("catat dua kopi hitam, bayar pas", "catat kopi hitam 2, bayar pas", "input kopi hitam x2, bayar pas"):
            kode_cli, o = self.run_cli("jual", "--pesan", pesan, "--waktu", "2026-09-24 10:00")
            self.assertEqual(kode_cli, 0, (pesan, o))
            self.assertEqual(len(o["baris"]), 1, pesan)
            self.assertEqual(o["baris"][0]["qty"] in (2, "2", 2.0) or str(o["baris"][0]["qty"]).startswith("2"), True, pesan)
        for pesan, kode in (("masuk angin=2, bayar pas", "MA"), ("input data 1, bayar pas", "ID"),
                            ("catat masuk angin 2, bayar pas", "MA")):
            kode_cli, o = self.run_cli("jual", "--pesan", pesan, "--waktu", "2026-09-24 10:00")
            self.assertEqual(kode_cli, 0, (pesan, o))
            self.assertEqual([b["kode"] for b in o["baris"]], [kode], pesan)

    def test_110_galat_sqlite_permanen_tidak_bilang_sementara(self):
        import io, contextlib
        asli = K.buat_parser
        class P:
            def parse_args(self, argv):
                class A:
                    json = True
                    @staticmethod
                    def fungsi(a):
                        raise K.sqlite3.OperationalError("no such table: nota")
                return A()
        K.buat_parser = lambda: P()
        try:
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                self.assertEqual(K.main([]), 1)
        finally:
            K.buat_parser = asli
        o = json.loads(buf.getvalue())
        self.assertNotIn("sementara", o["error"])
        self.assertNotIn("no such table", o["error"])
        self.assertIn("no such table", o["catatan_agent"])

    def test_111_skill_md_tidak_menyebut_aturan_lama(self):
        md = isi_file(os.path.join(AKAR, "SKILL.md"))
        self.assertLess(len(md.splitlines()), 300)
        self.assertNotIn("tidak lagi dipahami", md)

    def test_105_klaim_penutup_pratinjau_sesuai_kenyataan(self):
        jual = self.ok("jual", "--pesan", "2 kopi hitam, bayar pas", "--waktu", "2026-09-24 10:00")
        self.assertTrue(jual["teks"].rstrip().endswith('Simpan? Balas "ya".'))
        d2 = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, d2, ignore_errors=True)
        berkas = os.path.join(d2, "produk.csv")
        with open(berkas, "w", encoding="utf-8", newline="") as f:
            f.write(PRODUK_BOT_CSV)
        kode, o = self.main_json("mulai", "--db", os.path.join(d2, "k.db"), "--produk", berkas, "--nama-toko", "Warung",
                                 "--pesan", PESAN_BOT)
        self.assertEqual(kode, 0, o)
        self.assertTrue(o["teks"].rstrip().endswith('(mis. "sudah PKP", "kertas 80 mm", "bayarnya QRIS").'), o["teks"][-200:])
        self.assertIn('Balas "ya" kalau sudah sesuai.', o["teks"])
        for nama in ("SKILL.md", "README.md", "CHANGELOG.md"):
            t = isi_file(os.path.join(AKAR, nama))
            self.assertNotIn("pratinjau selalu berakhir", t.lower(), nama)
        self.assertIn('berakhir `Balas "ya" kalau sudah sesuai.`', isi_file(os.path.join(AKAR, "SKILL.md")))

    def test_106_ekspor_petunjuk_retur_pembeli_di_catatan_agent(self):
        n = self.jual("3 kopi hitam, bayar tunai 100rb")
        self.ok("retur", "--nota", n["no"], "--item", "1 kopi hitam", "--alasan", "salah rasa", "--refund", "tunai",
                "--waktu", "2026-09-24 12:00", "--ya")
        o = self.ok("ekspor", "--format", "buku-stok", "--tanggal", "2026-09-24", "--csv", os.path.join(self.dir, "bs.csv"))
        self.assertTrue(o["peringatan"])
        for p in o["peringatan"]:
            self.assertNotIn("retur-pembeli", p)
            self.assertIsNone(POLA_FLAG.search(p), p)
        self.assertIn("retur-pembeli", o["catatan_agent"])
        self.assertNotIn("retur-pembeli", o["teks"])

    def test_107_dokumen_disamakan(self):
        self.assertNotIn("Lokasi DB", isi_file(os.path.join(AKAR, "references", "perintah.md")))
        skill = isi_file(os.path.join(AKAR, "SKILL.md"))
        self.assertIn("(kecuali pemilik memintanya atau jelas di komputer yang sama)", skill)
        self.assertLess(len(skill.splitlines()), 300)
        kepala = skill.split("---")[1]
        self.assertEqual(sorted(l.split(":")[0] for l in kepala.strip().splitlines()), ["description", "name"])
        self.assertIn("Buku kasir ada dan terbaca", self.ok("info")["teks"])
        self.assertNotIn(self.dir, self.ok("info")["teks"])
        readme = isi_file(os.path.join(AKAR, "README.md"))
        self.assertEqual(readme.count("## Bukti uji di bot Telegram"), 1)
        self.assertIn("belum diuji ulang di bot asli", readme)

    def test_108_changelog_menyebut_jumlah_uji_dengan_benar(self):
        jumlah = len([n for n in UjiV1110.__dict__ if n.startswith("test_")])
        t = isi_file(os.path.join(AKAR, "CHANGELOG.md"))
        self.assertIn("`UjiV1110` (%d uji)" % jumlah, t)


class UjiV1111(Dasar):
    """v1.1.11 (temuan uji Telegram gelombang 28): setelah "ya", chat hanya berisi hasil untuk pemilik."""

    def skill(self):
        return isi_file(os.path.join(AKAR, "SKILL.md"))

    def test_112_aturan_balasan_setelah_ya_ada(self):
        md = self.skill()
        self.assertIn("Setelah pengguna membalas \"ya\", chat hanya berisi hasil untuk pemilik", md)
        self.assertIn("Kalimat tentang perintah, opsi, persetujuan, proses, atau instruksi kerja tidak pernah ditulis ke chat", md)
        self.assertIn("**Cara bicara**, poin 6", md)

    def test_113_skill_md_tanpa_kalimat_bocor_yang_bisa_disalin(self):
        md = self.skill().lower()
        for frasa in ("user setuju", "jalankan perintah sama persis", "perintah sama persis + --ya",
                      "lalu balas: hasil singkat"):
            self.assertNotIn(frasa, md, frasa)

    def test_114_aturan_baru_tidak_menyebut_opsi_teknis(self):
        md = self.skill()
        a = md.index("6. **Setelah pengguna membalas")
        poin = md[a:md.index("\n", a)]
        self.assertNotIn("--", poin)
        self.assertNotIn("`ya`", poin)

    def test_115_hasil_simpan_tidak_memuat_bahasa_proses(self):
        self.ok("buka-kasir", "--kas-awal", "100rb", "--ya")
        o = self.ok("jual", "--pesan", "2 kopi hitam, bayar pas", "--waktu", "2026-09-24 10:00", "--ya")
        for f in ("teks", "struk_teks"):
            tx = o.get(f, "")
            self.assertIsNone(POLA_FLAG.search(tx), tx)
            for kata in ("user setuju", "setuju", "persis", "perintah", "instruksi"):
                self.assertNotIn(kata, tx.lower(), (f, kata))

    def test_120_skill_md_tanpa_frasa_perintah_salin_varian(self):
        import re
        md = re.sub(r"[`*]", "", self.skill().lower())
        for pola in (r"perintah\s+(yang\s+)?sama(\s+persis)?\s*\+\s*--ya", r"jalankan\s+ulang\s+perintah",
                     r"jalankan\s+perintah\s+sama", r"perintah\s+sama\s*\+"):
            self.assertIsNone(re.search(pola, md), pola)

    def test_121_catatan_agent_bebas_frasa_salin(self):
        import re
        self.ok("init", "--nama-toko", "Warung Uji", "--ya")
        teks = [K.CATATAN_PRATINJAU, K.CATATAN_BERKAS, K.CATATAN_TERKUNCI]
        o = self.ok("jual", "--pesan", "1 kopi hitam, bayar pas", "--waktu", "2026-09-24 10:00")
        teks.append(o.get("catatan_agent", ""))
        for t in teks:
            tl = t.lower()
            self.assertIsNone(re.search(r"jalankan\W+.{0,40}sama\W+persis", tl), t)
            self.assertNotIn("setuju", tl, t)
            self.assertNotIn("sama persis + --ya", tl, t)
        self.assertNotIn("setuju", open(os.path.join(AKAR, "scripts", "kasir.py"), encoding="utf-8").read()
                         .split("CATATAN_PRATINJAU = (")[1].split("CATATAN_BERKAS")[0].lower())

    def test_122_struk_tidak_diminta_dua_kali(self):
        md = self.skill()
        self.assertNotIn("`teks` + `struk_teks`", md)
        self.assertIn("jangan dua kali", md)

    def test_116_versi_dan_dokumen_disamakan(self):
        self.assertEqual(K.VERSI, "1.1.12")
        self.assertIn("**1.1.12**", isi_file(os.path.join(AKAR, "README.md")))
        self.assertIn("## Catatan revisi 1.1.12", isi_file(os.path.join(AKAR, "CHANGELOG.md")))
        self.assertLess(len(self.skill().splitlines()), 300)

    def test_117_changelog_menyebut_jumlah_uji_dengan_benar(self):
        jumlah = len([n for n in UjiV1111.__dict__ if n.startswith("test_")])
        t = isi_file(os.path.join(AKAR, "CHANGELOG.md"))
        self.assertIn("`UjiV1111` (%d uji)" % jumlah, t)
        total = 0
        for nama, kls in list(globals().items()):
            if isinstance(kls, type) and issubclass(kls, unittest.TestCase) and kls.__module__ == __name__:
                total += len([n for n in dir(kls) if n.startswith("test_")]) if kls is not Dasar else 0
        self.assertIn("Total %d uji di `uji_regresi.py`" % total, t)


class UjiSingkatanFlag(unittest.TestCase):
    """Regresi keamanan: argparse tidak boleh menerima singkatan flag konfirmasi (mis. --y untuk --ya)."""

    def test_singkatan_flag_konfirmasi_ditolak(self):
        import subprocess
        import tempfile
        skrip = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts", "kasir.py")
        with tempfile.TemporaryDirectory() as t:
            argv = ["init", "--db", os.path.join(t, "a.db"), "--y"]
            p = subprocess.run([sys.executable, skrip] + argv, capture_output=True, text=True, timeout=60)
            self.assertNotEqual(p.returncode, 0, p.stdout + p.stderr)
            self.assertIn("unrecognized arguments", p.stdout + p.stderr)
            self.assertFalse(os.path.exists(os.path.join(t, "a.db")), "singkatan flag tidak boleh menulis apa pun")


if __name__ == "__main__":
    unittest.main(verbosity=1)
