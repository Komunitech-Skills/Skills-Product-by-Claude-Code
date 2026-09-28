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
        self.assertEqual((premium["rentang_bawah"], premium["rentang_atas"], premium["titik"]), (D(60000), D(70000), D(70000)))

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
        salah = [({}, "HPP"), ({"hpp": "0"}, "lebih dari 0"), ({"hpp": 1000, "margin": "100"}, "margin"),
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
        p = self.tulis("a.csv", "toko,harga\nA,50000\n")
        kode, _, err = self.jalankan(p)
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


if __name__ == "__main__":
    unittest.main(verbosity=1)
