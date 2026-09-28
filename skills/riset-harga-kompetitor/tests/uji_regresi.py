#!/usr/bin/env python3
"""Uji regresi riset-harga-kompetitor. Jalankan: python3 tests/uji_regresi.py  (Windows: py tests/uji_regresi.py)

Angka acuan dihitung manual (di komentar), bukan disalin dari keluaran script:
  harga minimum = ceil((HPP + biaya tetap) / (1 - biaya% - margin%))
  laba          = P - P x biaya% - HPP - biaya tetap ; margin = laba / P
  persentil     = interpolasi linear, posisi = (n - 1) x p   (PERCENTILE.INC)
"""
import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from datetime import date
from decimal import Decimal as D

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AKAR, "scripts"))
import banding_harga as B  # noqa: E402

HARI = date(2026, 9, 28)


def baris(harga, ukuran="250 gr", **lain):
    d = {"toko": lain.pop("toko", "Toko " + str(harga)), "nama": "Kopi", "ukuran": ukuran, "harga": harga}
    d.update(lain)
    return d


class Parsing(unittest.TestCase):
    def test_rupiah_berbagai_format(self):
        kasus = {"Rp49.900": 49900, "Rp 49.900": 49900, "49900": 49900, "49,9rb": 49900, "49.9rb": 49900,
                 "Rp 1,2 jt": 1200000, "1.2jt": 1200000, "1.250.000": 1250000, "Rp49.900,-": 49900,
                 "49.900,00": 49900, "49,900": 49900, "10RB": 10000, "59k": 59000, "IDR 75.000": 75000,
                 "1.250rb": 1250000, 49900: 49900, 49900.0: 49900}
        for teks, harap in kasus.items():
            with self.subTest(teks=teks):
                self.assertEqual(B.parse_rupiah(teks), D(harap))

    def test_rupiah_ditolak(self):
        for teks in ("49,9", "abc", "0", "", None, "Rp", "1.2.3", "49.90.0"):
            with self.subTest(teks=teks):
                with self.assertRaises(B.InputError):
                    B.parse_rupiah(teks)

    def test_rentang(self):
        kasus = {"49.900-59.900": (49900, 59900), "Rp49.900 - Rp59.900": (49900, 59900),
                 "49-59rb": (49000, 59000), "49.900 s/d 59.900": (49900, 59900),
                 "45rb–55rb": (45000, 55000), "Rp59.900 - Rp49.900": (49900, 59900),
                 "Rp49.900,- - Rp59.900,-": (49900, 59900), "Rp62.000": (62000, 62000),
                 "49.900 sampai 59.900": (49900, 59900)}
        for teks, (lo, hi) in kasus.items():
            with self.subTest(teks=teks):
                self.assertEqual(B.parse_rentang(teks), (D(lo), D(hi)))
        for teks in ("-5", "1-2-3", "", "gratis"):
            with self.subTest(teks=teks):
                with self.assertRaises(B.InputError):
                    B.parse_rentang(teks)

    def test_terjual_rating(self):
        self.assertEqual(B.parse_terjual("1rb+ terjual"), 1000)
        self.assertEqual(B.parse_terjual("2,3RB"), 2300)
        self.assertEqual(B.parse_terjual("Terjual 250+"), 250)
        self.assertEqual(B.parse_terjual("10 rb+"), 10000)
        self.assertIsNone(B.parse_terjual(""))
        self.assertEqual(B.parse_rating("4,9"), D("4.9"))
        self.assertEqual(B.parse_rating("★4.8/5"), D("4.8"))
        with self.assertRaises(B.InputError):
            B.parse_rating("9")

    def test_ukuran(self):
        kasus = {"250 gr": ("g", 250), "250g": ("g", 250), "0,5 kg": ("g", 500), "1.5 kg": ("g", 1500),
                 "1 ons": ("g", 100), "1 L": ("ml", 1000), "1.000 ml": ("ml", 1000), "500ML": ("ml", 500),
                 "12 x 25 g": ("g", 300), "2x250gr": ("g", 500), "3 × 1 kg": ("g", 3000),
                 "isi 12": ("pcs", 12), "isi 10 sachet": ("pcs", 10), "1 lusin": ("pcs", 12),
                 "1 kodi": ("pcs", 20), "Kopi Arabika Gayo 1kg": ("g", 1000)}
        for teks, (dim, qty) in kasus.items():
            with self.subTest(teks=teks):
                self.assertEqual(B.parse_ukuran(teks), (dim, D(qty)))
        for teks in ("", "Medium roast", "1 pack", None):
            with self.subTest(teks=teks):
                self.assertIsNone(B.parse_ukuran(teks))


class Hitungan(unittest.TestCase):
    def test_persentil_seperti_excel(self):
        data = [D(x) for x in (10, 20, 30, 40)]
        # posisi P25 = 0,75 -> 10 + 0,75 x 10 = 17,5 ; median = 25 ; P75 posisi 2,25 -> 32,5
        self.assertEqual(B.persentil(data, "0.25"), D("17.5"))
        self.assertEqual(B.persentil(data, "0.5"), D("25"))
        self.assertEqual(B.persentil(data, "0.75"), D("32.5"))
        self.assertEqual(B.persentil([D(7)], "0.5"), D(7))

    def test_harga_minimum_dan_laba(self):
        # (32.000 + 1.250) / (1 - 0,125 - 0,20) = 33.250 / 0,675 = 49.259,26 -> ceil 49.260
        # balik modal: 33.250 / 0,875 = 38.000
        h = B.olah([baris(60000), baris(55000), baris(50000)],
                   {"hpp": "32.000", "biaya_tetap": "1.250", "biaya_persen": ["8", "4", "0,5"],
                    "margin": "20", "ukuran": "250 gr"}, hari_ini=HARI)
        self.assertEqual(h["produk"]["minimum"], D(49260))
        self.assertEqual(h["produk"]["balik_modal"], D(38000))
        rk = h["rekomendasi"]
        # tengah: P25 = 52.500, median 55.000, P75 57.500
        self.assertEqual((rk["rentang_bawah"], rk["titik"], rk["rentang_atas"]), (D(52500), D(55000), D(57500)))
        # laba di 55.000 = 55.000 x 0,875 - 33.250 = 14.875 ; margin 27,045...%
        self.assertEqual(rk["laba_titik"], D(14875))
        self.assertEqual(B.bulat_ke(rk["margin_titik"] * 100, "0.01"), D("27.05"))
        self.assertEqual(rk["harga_cantik"], D(54900))
        self.assertEqual(rk["tanda"], [])

    def test_margin_default_20(self):
        # 40.000 / 0,8 = 50.000
        h = B.olah([baris(60000)], {"hpp": 40000}, hari_ini=HARI)
        self.assertEqual(h["produk"]["minimum"], D(50000))
        self.assertTrue(h["produk"]["margin_default"])

    def test_penyetaraan_ukuran(self):
        # 500 gr Rp115.000 -> setara 250 gr = 57.500 ; 1 kg 210.000 -> 52.500 ; 200 gr 45.000 -> 56.250
        h = B.olah([baris("Rp115.000", "500 gr"), baris("210rb", "1 kg"), baris("45.000", "200 gr"),
                    baris("25.000", "isi 10 sachet")],
                   {"hpp": 30000, "ukuran": "250 gr"}, hari_ini=HARI)
        setara = [p["setara"] for p in h["pesaing"]]
        self.assertEqual(setara[:3], [D(57500), D(52500), D(56250)])
        self.assertIsNone(setara[3])                    # pcs tidak bisa disetarakan ke gram
        self.assertEqual(h["stat"]["n"], 3)
        self.assertEqual(h["stat"]["median"], D(56250))
        self.assertEqual(h["pesaing"][0]["per_satuan"], D(23000))   # per 100 g

    def test_rentang_mode(self):
        rows = [baris("49.900-59.900")]
        for mode, harap in (("min", 49900), ("tengah", 54900), ("maks", 59900)):
            h = B.olah(rows, {"hpp": 20000}, mode_rentang=mode, hari_ini=HARI)
            self.assertEqual(h["pesaing"][0]["harga"], D(harap))

    def test_duplikat_url_dan_isi(self):
        rows = [baris(50000, sumber="https://www.tokopedia.com/a/kopi-250?utm=x"),
                baris(51000, sumber="https://tokopedia.com/a/kopi-250/"),
                baris(52000, toko="Sama"), baris(52000, toko="Sama"), baris(53000)]
        h = B.olah(rows, {"hpp": 20000}, hari_ini=HARI)
        self.assertEqual(len(h["duplikat"]), 2)
        self.assertEqual(h["stat"]["n"], 3)

    def test_baris_rusak_dilewati(self):
        rows = [baris("hubungi penjual"), baris(""), baris(50000), {"toko": "", "harga": ""}]
        h = B.olah(rows, {"hpp": 20000}, hari_ini=HARI)
        self.assertEqual(h["stat"]["n"], 1)
        self.assertEqual(len(h["dilewati"]), 2)
        self.assertTrue(any("Hanya 1 pesaing" in x for x in h["peringatan"]))

    def test_tanda_pasar_di_bawah_minimum(self):
        # minimum = 45.000 / 0,675 = 66.666,67 -> 66.667 ; semua pesaing <= 62.000
        h = B.olah([baris(50000), baris(55000), baris(62000)],
                   {"hpp": 45000, "biaya_persen": "12,5", "harga_kita": "60.000"}, hari_ini=HARI)
        rk = h["rekomendasi"]
        self.assertIn("PASAR_DI_BAWAH_MINIMUM", rk["tanda"])
        self.assertIn("HARGA_KITA_DI_BAWAH_MINIMUM", rk["tanda"])
        self.assertEqual((rk["rentang_bawah"], rk["titik"], rk["rentang_atas"]), (D(66667), D(66667), D(66667)))

    def test_tanda_median_di_bawah_minimum(self):
        # minimum 40.000 / 0,8 = 50.000 ; median 45.000 < 50.000 <= P75 55.000
        h = B.olah([baris(40000), baris(45000), baris(55000), baris(60000), baris(35000)],
                   {"hpp": 40000}, hari_ini=HARI)
        self.assertEqual(h["rekomendasi"]["tanda"], ["MEDIAN_DI_BAWAH_MINIMUM"])
        self.assertEqual(h["rekomendasi"]["titik"], D(50000))

    def test_posisi_harga_kita(self):
        h = B.olah([baris(50000), baris(55000), baris(60000), baris(65000)],
                   {"hpp": 30000, "harga_kita": "Rp55.000"}, hari_ini=HARI)
        ps = h["posisi"]
        self.assertEqual((ps["lebih_murah_dari"], ps["sama_dengan"], ps["lebih_mahal_dari"]), (2, 1, 1))
        self.assertEqual(ps["persentil"], D("37.5"))        # (1 + 0,5) / 4
        self.assertEqual(ps["laba"], D(25000))

    def test_strategi(self):
        rows = [baris(x) for x in (40000, 50000, 60000, 70000, 80000)]
        prod = {"hpp": 10000}
        murah = B.olah(rows, prod, "murah", hari_ini=HARI)["rekomendasi"]
        premium = B.olah(rows, prod, "premium", hari_ini=HARI)["rekomendasi"]
        self.assertEqual((murah["rentang_bawah"], murah["rentang_atas"], murah["titik"]), (D(40000), D(50000), D(50000)))
        # v1.0.1 (temuan T4): premium dulu [median..P75] = subset strategi tengah, bukan premium.
        # Sekarang premium = [P75..P90], titik P75. P75 = 70.000 ; P90 posisi 4 x 0,9 = 3,6 -> 70.000 + 0,6 x 10.000 = 76.000
        self.assertEqual((premium["rentang_bawah"], premium["rentang_atas"], premium["titik"]), (D(70000), D(76000), D(70000)))

    def test_promo_bundling_data_lama(self):
        rows = [baris(50000, harga_coret="Rp62.500", promo="Gratis ongkir"),
                baris(60000, nama="Paket hemat beli 2"), baris(55000, tanggal="2026-07-01"),
                baris(58000, harga_coret="50.000")]
        h = B.olah(rows, {"hpp": 20000}, hari_ini=HARI)
        self.assertEqual(h["promo"]["harga_coret"], 1)
        self.assertEqual(h["promo"]["rata_diskon"], D("0.2"))        # 12.500 / 62.500
        self.assertEqual(h["promo"]["promo_ongkir"], 1)
        self.assertEqual(len(h["promo"]["bundling"]), 1)
        self.assertTrue(any("data lama" in c for c in h["pesaing"][2]["catatan"]))
        self.assertTrue(any("diabaikan" in c for c in h["pesaing"][3]["catatan"]))

    def test_error_input(self):
        # v1.0.1 (temuan T5): HPP kosong tidak lagi error -> mode pasar saja (diuji di UjiRevisi101.test_t5_*)
        salah = [({"hpp": "0"}, "lebih dari 0"), ({"hpp": 1000, "margin": "100"}, "margin"),
                 ({"hpp": 1000, "biaya_persen": ["50"], "margin": "50"}, "mustahil"),
                 ({"hpp": 1000, "ukuran": "sebungkus"}, "tidak dikenali")]
        for prod, pesan in salah:
            with self.subTest(prod=prod):
                with self.assertRaises(B.InputError) as cm:
                    B.olah([baris(50000)], prod, hari_ini=HARI)
                self.assertIn(pesan, str(cm.exception))
        with self.assertRaises(B.InputError):
            B.olah([baris("abc")], {"hpp": 1000}, hari_ini=HARI)
        with self.assertRaises(B.InputError):          # satuan tidak cocok semua
            B.olah([baris(50000, "500 ml")], {"hpp": 1000, "ukuran": "250 gr"}, hari_ini=HARI)


class CLI(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def jalankan(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            kode = B.main(list(argv))
        return kode, out.getvalue(), err.getvalue()

    def tulis(self, nama, isi):
        p = os.path.join(self.dir, nama)
        with open(p, "w", encoding="utf-8") as f:
            f.write(isi)
        return p

    def test_csv_titik_koma_dan_header_alias(self):
        p = self.tulis("a.csv", "Penjual;Produk;Berat;Harga Jual;Link\n"
                                "A;Kopi;250 gr;Rp50.000;\nB;Kopi;250 gr;49,9rb;\nC;Kopi;500 gr;Rp 110.000;\n")
        kode, out, _ = self.jalankan(p, "--hpp", "30.000", "--ukuran", "250 gr", "--tanggal", "2026-09-28")
        self.assertEqual(kode, 0)
        self.assertIn("Median (tengah)", out)
        self.assertIn("**Rp 50.000**", out)          # median dari 49.900 / 50.000 / 55.000
        self.assertIn("Harga minimum sesuai target margin", out)

    def test_json_dengan_produk_kita(self):
        data = {"produk_kita": {"nama": "Sambal", "hpp": 18000, "ukuran": "200 ml", "margin": 25},
                "pesaing": [{"nama": "S1", "ukuran": "150 ml", "harga": "Rp30.000"},
                            {"nama": "S2", "ukuran": "250 ml", "harga": 45000}]}
        p = self.tulis("a.json", json.dumps(data))
        kode, out, _ = self.jalankan(p, "--format", "json", "--tanggal", "2026-09-28")
        self.assertEqual(kode, 0)
        h = json.loads(out)
        # setara 200 ml: 30.000/150x200 = 40.000 ; 45.000/250x200 = 36.000 ; minimum 18.000/0,75 = 24.000
        self.assertEqual([p["setara"] for p in h["pesaing"]], ["40000.00", "36000.00"])
        self.assertEqual(h["produk"]["minimum"], "24000.00")

    def test_error_keluar_kode_2(self):
        # v1.0.1 (temuan T5): tanpa --hpp tidak lagi keluar kode 2, tetapi mode pasar saja (kode 0)
        p = self.tulis("a.csv", "toko,harga\nA,50000\n")
        kode, out, err = self.jalankan(p)
        self.assertEqual(kode, 0)
        self.assertIn("HPP", out)
        kode, _, err = self.jalankan(p, "--hpp", "0")
        self.assertEqual(kode, 2)
        self.assertIn("HPP", err)
        kode, _, err = self.jalankan(os.path.join(self.dir, "tidak-ada.csv"), "--hpp", "1000")
        self.assertEqual(kode, 2)
        kode, _, err = self.jalankan(self.tulis("k.csv", ""), "--hpp", "1000")
        self.assertEqual(kode, 2)
        kode, _, err = self.jalankan(self.tulis("j.json", "{rusak"), "--hpp", "1000")
        self.assertEqual(kode, 2)

    def test_contoh_bawaan(self):
        p = os.path.join(AKAR, "examples", "contoh-pesaing-kopi.csv")
        kode, out, _ = self.jalankan(p, "--hpp", "32.000", "--ukuran", "250 gr", "--biaya-persen", "8",
                                     "--biaya-persen", "4", "--biaya-persen", "0,5", "--biaya-tetap", "1.250",
                                     "--harga-kita", "65.000", "--tanggal", "2026-09-28")
        self.assertEqual(kode, 0)
        # setara 250 g: 62.000, 57.500, 49.900, 52.500, 49.950, 56.250 -> median (52.500+56.250)/2 = 54.375
        self.assertIn("**Rp 54.375**", out)
        self.assertIn("**Rp 49.260**", out)          # 33.250 / 0,675
        self.assertIn("1 duplikat", out)


class UjiRevisi101(unittest.TestCase):
    """Regresi temuan uji independen v1.0.0 (examples/HASIL-UJI.md, T1-T11)."""

    def tulis(self, isi, nama="a.csv", biner=False):
        d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, d, True)
        p = os.path.join(d, nama)
        with open(p, "wb" if biner else "w", **({} if biner else {"encoding": "utf-8"})) as f:
            f.write(isi)
        return p

    def jalankan(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            kode = B.main(list(argv))
        return kode, out.getvalue(), err.getvalue()

    # ---- T1 pecahan
    def test_t1_pecahan(self):
        kasus = {"1/2 kg": ("g", 500), "1/4 kg": ("g", 250), "1/2kg": ("g", 500), "setengah kilo": ("g", 500),
                 "Setengah kg": ("g", 500), "seperempat kg": ("g", 250), "1 1/2 kg": ("g", 1500),
                 "1½ kg": ("g", 1500), "1/2 liter": ("ml", 500), "3/4 kg": ("g", 750),
                 "Kopi Gayo 1/2 kg": ("g", 500), "12 x 1/2 kg": ("g", 6000)}
        for teks, (dim, qty) in kasus.items():
            with self.subTest(teks=teks):
                self.assertEqual(B.parse_ukuran(teks), (dim, D(qty)))
        for teks in ("1/3 kg", "1/0 kg"):
            with self.subTest(teks=teks):
                with self.assertRaises(B.InputError):
                    B.parse_ukuran(teks)

    def test_t1_pecahan_di_analisis(self):
        # 1/2 kg Rp100.000 -> setara 250 g = 100.000 / 500 x 250 = 50.000 (dulu salah: /2.000 g -> 12.500)
        h = B.olah([baris(100000, "1/2 kg"), baris(52000), baris(54000), baris(26000, "1/3 kg")],
                   {"hpp": 20000, "ukuran": "250 gr"}, hari_ini=HARI)
        self.assertEqual(h["pesaing"][0]["setara"], D(50000))
        self.assertIsNone(h["pesaing"][3]["setara"])            # pecahan aneh -> ditolak + alasan
        self.assertTrue(any("pecahan" in c for c in h["pesaing"][3]["catatan"]))

    # ---- T2 pengali di belakang / paket
    def test_t2_pengali(self):
        for teks in ("250 g x 2", "250gr x 2 pcs", "isi 2 @250gr", "250 g + 250 g", "Paket 2 pcs @ 250 gr",
                     "2 x 250 gr", "250 gr x2", "2 bungkus @ 250 gr", "250 g * 2"):
            with self.subTest(teks=teks):
                self.assertEqual(B.parse_ukuran(teks), ("g", D(500)))
        with self.assertRaises(B.InputError):
            B.parse_ukuran("250 g + 250 ml")
        # produk kita dalam pcs: paket dibaca sebagai jumlah kemasan
        self.assertEqual(B.parse_ukuran("Paket 2 pcs @ 250 gr", "pcs"), ("pcs", D(2)))

    def test_t2_setara_uji03(self):
        # dimsum 88.000 untuk 'Paket 2 pcs @ 250 gr' -> setara 250 g = 44.000 (dulu 88.000)
        h = B.olah([baris(88000, "Paket 2 pcs @ 250 gr"), baris(45000), baris(43000)],
                   {"hpp": 20000, "ukuran": "250 gr"}, hari_ini=HARI)
        self.assertEqual(h["pesaing"][0]["setara"], D(44000))
        self.assertEqual(h["pencilan"], [])

    # ---- T3 pencilan keluar statistik
    def test_t3_pencilan_keluar_statistik(self):
        rows = [baris(x) for x in (50000, 52000, 54000, 56000)] + [baris(12500, toko="Salah baca")]
        h = B.olah(rows, {"hpp": 20000, "ukuran": "250 gr"}, hari_ini=HARI)
        # median awal 52.000 -> batas 26.000..104.000 ; 12.500 keluar. Statistik dari 50/52/54/56 ribu:
        # terendah 50.000, P25 = 50.000 + 0,75 x 2.000 = 51.500, median 53.000
        self.assertEqual(h["pencilan"], [5])
        self.assertEqual(h["stat"]["n"], 4)
        self.assertEqual((h["stat"]["terendah"], h["stat"]["p25"], h["stat"]["median"]), (D(50000), D(51500), D(53000)))
        self.assertFalse(h["pesaing"][4]["dihitung"])
        self.assertTrue(any("TIDAK ikut statistik" in c for c in h["pesaing"][4]["catatan"]))
        self.assertTrue(any("--pakai-semua" in x for x in h["peringatan"]))
        semua = B.olah(rows, {"hpp": 20000, "ukuran": "250 gr"}, hari_ini=HARI, pakai_semua=True)
        self.assertEqual((semua["stat"]["n"], semua["stat"]["terendah"]), (5, D(12500)))
        md = B.ke_markdown(h)
        self.assertIn("Salah baca", md)                          # tetap tampil di tabel
        self.assertIn("1 jauh dari median tidak dihitung", md)

    def test_t3_dua_pesaing_tidak_dibuang(self):
        h = B.olah([baris(10000), baris(50000)], {"hpp": 5000}, hari_ini=HARI)
        self.assertEqual(h["stat"]["n"], 2)

    # ---- T4 premium
    def test_t4_premium_di_atas_tengah(self):
        rows = [baris(x) for x in (38000, 40000, 42000, 44000, 45000, 46000, 48000, 55000)]
        prod = {"hpp": 10000}
        tengah = B.olah(rows, prod, "tengah", hari_ini=HARI)["rekomendasi"]
        premium = B.olah(rows, prod, "premium", hari_ini=HARI)["rekomendasi"]
        # P75 posisi 5,25 -> 46.000 + 0,25 x 2.000 = 46.500 ; P90 posisi 6,3 -> 48.000 + 0,3 x 7.000 = 50.100
        self.assertEqual((premium["rentang_bawah"], premium["rentang_atas"], premium["titik"]),
                         (D(46500), D(50100), D(46500)))
        self.assertEqual(premium["rentang_bawah"], tengah["rentang_atas"])   # bersinggungan, bukan subset
        self.assertGreater(premium["rentang_atas"], tengah["rentang_atas"])

    # ---- T5 mode pasar saja
    def test_t5_pasar_saja(self):
        h = B.olah([baris(50000), baris(55000), baris(60000)], {"ukuran": "250 gr", "harga_kita": "58.000"},
                   hari_ini=HARI)
        self.assertEqual(h["mode"], "pasar_saja")
        self.assertIsNone(h["rekomendasi"])
        self.assertIsNone(h["produk"]["minimum"])
        self.assertEqual(h["stat"]["median"], D(55000))
        self.assertEqual(h["posisi"]["lebih_mahal_dari"], 2)
        self.assertIsNone(h["posisi"]["laba"])
        md = B.ke_markdown(h)
        self.assertIn("Mode harga pasar saja", md)
        self.assertIn("Belum dihitung: HPP", md)
        self.assertNotIn("Harga minimum sesuai", md)

    def test_t5_pasar_saja_json(self):
        p = self.tulis("toko,ukuran,harga\nA,250 gr,50.000\nB,250 gr,60.000\n")
        kode, out, _ = self.jalankan(p, "--format", "json", "--tanggal", "2026-09-28")
        self.assertEqual(kode, 0)
        h = json.loads(out)
        self.assertEqual((h["mode"], h["rekomendasi"], h["stat"]["median"]), ("pasar_saja", None, "55000.00"))

    # ---- T6 encoding
    def test_t6_csv_ansi(self):
        isi = "toko,ukuran,harga\nCafé Kopi,250 gr,Rp50.000\nB,250 gr,Rp52.000\n".encode("cp1252")
        kode, out, _ = self.jalankan(self.tulis(isi, biner=True), "--hpp", "20.000", "--tanggal", "2026-09-28")
        self.assertEqual(kode, 0)
        self.assertIn("Café Kopi", out)
        self.assertIn("Windows-1252", out)

    def test_t6_csv_utf16_dan_biner(self):
        isi = "toko\tukuran\tharga\nA\t250 gr\tRp50.000\n".encode("utf-16")
        kode, out, _ = self.jalankan(self.tulis(isi, biner=True), "--hpp", "20.000")
        self.assertEqual(kode, 0)
        for data, pesan in ((b"PK\x03\x04\x00\x00rusak", "Excel"), (b"\x00\x01\x02\xff\xfe", "biner"),
                            (b"toko,harga\nA,\x81\x8d\x8f\n", "encoding")):
            with self.subTest(pesan=pesan):
                kode, _, err = self.jalankan(self.tulis(data, biner=True), "--hpp", "20.000")
                self.assertEqual(kode, 2)
                self.assertTrue(err.startswith("ERROR:"))
                self.assertIn(pesan, err)
                self.assertNotIn("Traceback", err)

    # ---- T7 jumlah kolom
    def test_t7_kolom_bergeser(self):
        p = self.tulis("toko,ukuran,harga,terjual,lokasi\nA,250 gr,50.000,1,2RB terjual,Medan\n"
                       "B,250 gr,52.000,\"1,2RB\",Bandung\nC,250 gr,54.000\n")
        kode, out, _ = self.jalankan(p, "--hpp", "20.000", "--tanggal", "2026-09-28")
        self.assertEqual(kode, 0)
        self.assertIn("baris 1 (A): jumlah kolom 6 padahal judul kolom 5", out)
        self.assertIn("Baris 3 (C): jumlah kolom lebih sedikit", out)
        self.assertIn("Pesaing dibandingkan: **2**", out)

    # ---- T8 harga < 100
    def test_t8_harga_kecil_ditolak(self):
        for nilai in (49.9, 50, "50", "Rp 99", D("49.9")):
            with self.subTest(nilai=nilai):
                with self.assertRaises(B.InputError) as cm:
                    B.parse_rentang(nilai)
                self.assertIn("terlalu kecil", str(cm.exception))
        self.assertEqual(B.parse_rentang(100), (D(100), D(100)))
        h = B.olah([baris(49.9), baris(50000)], {"hpp": 20000}, hari_ini=HARI)
        self.assertEqual(h["stat"]["n"], 1)
        with self.assertRaises(B.InputError):
            B.olah([baris(50000)], {"hpp": 20000, "harga_kita": 49.9}, hari_ini=HARI)

    # ---- T9 beberapa dimensi
    def test_t9_pilih_dimensi_produk_kita(self):
        self.assertEqual(B.parse_ukuran("isi 10 pcs 250 gr", "g"), ("g", D(250)))
        self.assertEqual(B.parse_ukuran("isi 10 pcs 250 gr", "pcs"), ("pcs", D(10)))
        h = B.olah([baris(50000, "isi 10 pcs 250 gr"), baris(100000, "10 pcs", nama="Kopi 500 gr")],
                   {"hpp": 20000, "ukuran": "250 gr"}, hari_ini=HARI)
        self.assertEqual([p["setara"] for p in h["pesaing"]], [D(50000), D(50000)])
        self.assertTrue(any("beberapa ukuran" in c for c in h["pesaing"][0]["catatan"]))
        self.assertTrue(any("dibaca dari nama" in c for c in h["pesaing"][1]["catatan"]))

    # ---- T10 pesan
    def test_t10_pesan(self):
        with self.assertRaises(B.InputError) as cm:
            B.parse_rentang("Rp -49.900")
        self.assertIn("negatif", str(cm.exception))
        with self.assertRaises(B.InputError) as cm:
            B.olah([baris(50000)], {"hpp": 20000, "margin": "-5"}, hari_ini=HARI)
        self.assertIn("negatif", str(cm.exception))
        with self.assertRaises(B.InputError) as cm:
            B.olah([{"toko": "A", "price_idr": "50.000"}], {"hpp": 20000}, hari_ini=HARI)
        self.assertIn("kolom harga tidak ditemukan", str(cm.exception))
        self.assertIn("price_idr", str(cm.exception))
        with self.assertRaises(B.InputError) as cm:
            B.olah([], {"hpp": 20000}, hari_ini=HARI)
        self.assertIn("hanya judul kolom", str(cm.exception))
        rows = [baris(50000, sumber="https://tokopedia.com/a/x"), baris(51000, sumber="https://www.tokopedia.com/a/x")]
        h = B.olah(rows, {"hpp": 20000}, hari_ini=HARI)
        self.assertIn("harga beda (50000 vs 51000)", h["duplikat"][0])
        md = B.ke_markdown(B.olah([baris(50000, harga_coret="60.000"), baris(50000, "500 ml")],
                                  {"hpp": 20000, "ukuran": "250 gr"}, hari_ini=HARI))
        self.assertIn("1 dari 2 pesaing di tabel memasang harga coret", md)

    # ---- T11 sebagian punya ukuran
    def test_t11_ukuran_campur(self):
        h = B.olah([baris(40000, ""), baris(42000, ""), baris(80000, "2 pcs")], {"hpp": 20000}, hari_ini=HARI)
        self.assertTrue(any("1 pesaing mencantumkan ukuran/isi (2 pcs) dan 2 tidak" in x and "'1 pcs'" in x
                            for x in h["peringatan"]))
        h = B.olah([baris(40000, ""), baris(80000, "2 pcs"), baris(41000, "1 pcs")],
                   {"hpp": 20000, "ukuran": "1 pcs"}, hari_ini=HARI)
        self.assertEqual([p["setara"] for p in h["pesaing"]], [None, D(40000), D(41000)])
        self.assertTrue(any("tulis 1 pcs" in c for c in h["pesaing"][0]["catatan"]))


if __name__ == "__main__":
    unittest.main(verbosity=1)
