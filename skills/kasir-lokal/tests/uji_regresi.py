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
        self.assertIn("Tidak ada kasir", self.gagal("tutup-kasir", "--kas-fisik", "0", "--ya")["error"])

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
        # rata-rata = (45.900 + 64.140 + 8.125) / 3 = 39.388,33 -> 39.388
        self.assertEqual(r["rata_rata_per_nota"], 39388)
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
        self.assertTrue(any("retur-pembeli" in p for p in o["peringatan"]))
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
        self.assertIn("bukan database", json.loads(buf.getvalue())["error"])
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.assertEqual(K.main(["info", "--db", os.path.join(self.dir, "tidak-ada.db"), "--json"]), 1)
        self.assertIn("belum ada", json.loads(buf.getvalue())["error"])

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


if __name__ == "__main__":
    unittest.main(verbosity=1)
