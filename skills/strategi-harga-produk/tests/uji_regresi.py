#!/usr/bin/env python3
"""Uji regresi strategi-harga-produk. Jalankan: python3 tests/uji_regresi.py  (Windows: py tests/uji_regresi.py)

Semua angka acuan dihitung MANUAL (rumus di komentar), bukan disalin dari keluaran script.
Contoh dasar: Roti Sobek Toko "Roti Bu Ratna" (fiktif), HPP Rp11.500, harga Rp28.000.
"""
import contextlib
import io
import os
import sys
import unittest
from decimal import Decimal as D

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AKAR, "scripts"))
import strategi_harga as S  # noqa: E402


def jalan(*argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        kode = S.main(list(argv))
    return kode, out.getvalue(), err.getvalue()


class Parsing(unittest.TestCase):
    def test_rupiah(self):
        kasus = {"Rp28.000": 28000, "28000": 28000, "28rb": 28000, "28,5rb": 28500, "1,2jt": 1200000,
                 "Rp 1.250.000": 1250000, "28.000,-": 28000, "11.500,50": D("11500.50"), "28,000": 28000,
                 "IDR 45.000": 45000, "45k": 45000, "1.250rb": 1250000, 28000: 28000}
        for teks, harap in kasus.items():
            with self.subTest(teks=teks):
                self.assertEqual(S.parse_rupiah(teks), D(harap))

    def test_rupiah_ditolak(self):
        for teks in ("abc", "0", "", "-5000", "1.2.3", "Rp"):
            with self.subTest(teks=teks):
                with self.assertRaises(S.InputError):
                    S.parse_rupiah(teks)

    def test_persen(self):
        self.assertEqual(S.parse_persen("15"), D("0.15"))
        self.assertEqual(S.parse_persen("12,5%"), D("0.125"))
        self.assertEqual(S.parse_persen("-10", boleh_negatif=True), D("-0.10"))
        with self.assertRaises(S.InputError):
            S.parse_persen("-10")
        with self.assertRaises(S.InputError):
            S.parse_persen("150")

    def test_format(self):
        self.assertEqual(S.rp(D(1250000)), "Rp1.250.000")
        self.assertEqual(S.rp(D("18666.666")), "Rp18.666,67")
        self.assertEqual(S.rp(D(-636000)), "-Rp636.000")
        self.assertEqual(S.pct(D("0.258064")), "25,81%")
        self.assertEqual(S.pct(D("0.2")), "20%")
        self.assertEqual(S.pct(D("0.125")), "12,5%")


class Margin(unittest.TestCase):
    def test_dari_harga(self):
        # laba = 28.000 - 11.500 = 16.500 ; margin = 16.500/28.000 = 0,589285 ; markup = 16.500/11.500 = 1,434782
        h = S.hitung_margin(D(11500), harga=D(28000))
        self.assertEqual(h["laba"], D(16500))
        self.assertEqual(S.pct(h["margin"]), "58,93%")
        self.assertEqual(S.pct(h["markup"]), "143,48%")

    def test_markup_50_bukan_margin_50(self):
        # harga = 11.500 x 1,5 = 17.250 ; margin = 5.750/17.250 = 33,33%
        h = S.hitung_margin(D(11500), markup=D("0.5"))
        self.assertEqual(h["harga"], D(17250))
        self.assertEqual(S.pct(h["margin"]), "33,33%")

    def test_target_margin_dengan_potongan(self):
        # 11.500 / (1 - 0,12 - 0,55) = 11.500 / 0,33 = 34.848,48 -> ke atas 34.849
        h = S.hitung_margin(D(11500), margin=D("0.55"), biaya=D("0.12"))
        self.assertEqual(h["harga"], D(34849))
        self.assertGreaterEqual(h["margin"], D("0.55"))

    def test_target_tidak_mungkin(self):
        with self.assertRaises(S.InputError):
            S.hitung_margin(D(11500), margin=D("0.9"), biaya=D("0.15"))

    def test_konversi(self):
        self.assertEqual(S.margin_ke_markup(D("0.4")), D("0.4") / D("0.6"))   # 66,67%
        self.assertEqual(S.pct(S.margin_ke_markup(D("0.4"))), "66,67%")
        self.assertEqual(S.pct(S.markup_ke_margin(D("1"))), "50%")          # markup 100% = margin 50%


class Bep(unittest.TestCase):
    def test_bep_roti(self):
        # kontribusi = 28.000 - 11.500 = 16.500 ; 6.500.000 / 16.500 = 393,94 -> 394 unit ; omzet 394 x 28.000 = 11.032.000
        # per hari 394/26 = 15,15 -> 16 ; laba di 600 unit = 600 x 16.500 - 6.500.000 = 3.400.000
        # batas aman = (600 - 394)/600 = 34,33%
        h = S.hitung_bep(D(6500000), D(28000), D(11500), hari_jual=26, volume=D(600))
        self.assertEqual(h["unit"], D(394))
        self.assertEqual(h["omzet"], D(11032000))
        self.assertEqual(h["per_hari"], D(16))
        self.assertEqual(h["laba_sekarang"], D(3400000))
        self.assertEqual(S.pct(h["batas_aman"]), "34,33%")

    def test_bep_dengan_target_laba_dan_potongan(self):
        # kontribusi = 28.000 x 0,9 - 11.500 = 13.700 ; (6.500.000 + 3.000.000)/13.700 = 693,43 -> 694
        h = S.hitung_bep(D(6500000), D(28000), D(11500), biaya=D("0.1"), target_laba=D(3000000))
        self.assertEqual(h["unit"], D(694))

    def test_bep_rugi_per_unit(self):
        with self.assertRaises(S.InputError):
            S.hitung_bep(D(1000000), D(10000), D(12000))


class Tangga(unittest.TestCase):
    def test_tangga_roti(self):
        # batas = 11.500/0,65 = 17.692,31 -> 17.693 ; diskon maks = 1 - 17.693/28.000 = 36,81%
        # Reseller 15%: 23.800 -> kelipatan 500 terdekat = 24.000 ; laba 12.500 ; margin 52,08%
        # Grosir 25%: 21.000 ; laba 9.500 ; margin 45,24%
        # Agen =17.000 ; laba 5.500 ; margin 32,35% < 35% -> DI BAWAH MIN ; laba di 200 pcs = 1.100.000
        lv = [S.parse_level(x) for x in ("Agen:200:=17000", "Eceran:1:0", "Reseller:10:15", "Grosir:50:25")]
        h = S.hitung_tangga(D(28000), D(11500), lv, D("0.35"), kelipatan_rp=D(500))
        self.assertEqual(h["batas"], D(17693))
        self.assertEqual(S.pct(h["diskon_maks"]), "36,81%")
        nama = [b["nama"] for b in h["baris"]]
        self.assertEqual(nama, ["Eceran", "Reseller", "Grosir", "Agen"])   # diurutkan min beli
        r = {b["nama"]: b for b in h["baris"]}
        self.assertEqual(r["Reseller"]["harga"], D(24000))
        self.assertEqual(r["Reseller"]["laba"], D(12500))
        self.assertEqual(r["Grosir"]["harga"], D(21000))
        self.assertEqual(S.pct(r["Grosir"]["margin"]), "45,24%")
        self.assertFalse(r["Agen"]["aman"])
        self.assertEqual(r["Agen"]["laba_min_beli"], D(1100000))
        self.assertEqual(len(h["peringatan"]), 1)

    def test_tangga_terbalik_dan_format_salah(self):
        lv = [S.parse_level("A:1:20"), S.parse_level("B:10:10")]
        h = S.hitung_tangga(D(28000), D(11500), lv, D("0.3"))
        self.assertTrue(any("terbalik" in p for p in h["peringatan"]))
        for salah in ("Reseller:10", "Reseller:x:10", ":10:10", "R:0:10"):
            with self.subTest(salah=salah):
                with self.assertRaises(S.InputError):
                    S.parse_level(salah)


class Diskon(unittest.TestCase):
    def test_diskon_20(self):
        # promo 28.000 x 0,8 = 22.400 ; laba 10.900 ; faktor 16.500/10.900 = 1,513761 -> naik 51,38%
        # volume 600 x 1,513761 = 908,26 -> 909
        h = S.hitung_diskon(D(28000), D(11500), diskon=D("0.2"), volume=D(600), margin_min=D("0.35"))
        self.assertEqual(h["harga_promo"], D(22400))
        self.assertEqual(h["laba_promo"], D(10900))
        self.assertEqual(S.pct(h["tambahan"]), "51,38%")
        self.assertEqual(h["volume_perlu"], D(909))
        self.assertEqual(h["batas"], D(17693))

    def test_klasik_margin_40_diskon_20_butuh_2x(self):
        # harga 100.000, HPP 60.000: laba 40.000 -> 20.000 ; volume harus 2x (naik 100%)
        h = S.hitung_diskon(D(100000), D(60000), diskon=D("0.2"), volume=D(50))
        self.assertEqual(h["tambahan"], D(1))
        self.assertEqual(h["volume_perlu"], D(100))

    def test_beli2_gratis1(self):
        # harga efektif 2 x 28.000 / 3 = 18.666,67 ; laba 7.166,67 ; faktor 16.500 / 7.166,67 = 2,302326
        # 600 x 2,302326 = 1.381,40 -> 1.382
        h = S.hitung_diskon(D(28000), D(11500), bxgy=(2, 1), volume=D(600))
        self.assertEqual(S.rp(h["harga_promo"]), "Rp18.666,67")
        self.assertEqual(S.pct(h["diskon_efektif"]), "33,33%")
        self.assertEqual(h["volume_perlu"], D(1382))

    def test_potongan_rupiah_dengan_biaya_marketplace(self):
        # laba normal 28.000 x 0,9 - 11.500 = 13.700 ; promo 23.000 x 0,9 - 11.500 = 9.200
        # faktor 13.700/9.200 = 1,489130 ; 200 x = 297,83 -> 298
        h = S.hitung_diskon(D(28000), D(11500), potongan=D(5000), volume=D(200), biaya=D("0.1"))
        self.assertEqual(h["laba_promo"], D(9200))
        self.assertEqual(h["volume_perlu"], D(298))

    def test_promo_rugi(self):
        h = S.hitung_diskon(D(28000), D(11500), diskon=D("0.6"))   # 11.200 < HPP
        self.assertTrue(h["rugi"])
        self.assertNotIn("volume_perlu", h)
        with self.assertRaises(S.InputError):
            S.hitung_diskon(D(10000), D(12000), diskon=D("0.1"))
        with self.assertRaises(S.InputError):
            S.parse_bxgy("2")


class Bundel(unittest.TestCase):
    ITEM = ["Roti Sobek:28000:11500", "Bolu Pandan:45.000:19rb", "Cookies Coklat:35000:14000"]

    def test_paket_hampers(self):
        # total 108.000 ; HPP isi 44.500 ; + kemasan 6.000 = 50.500 ; hemat 13.000 (12,04%)
        # laba paket 95.000 - 50.500 = 44.500 (46,84%) ; satuan 108.000 - 44.500 = 63.500 (58,80%)
        # faktor 63.500/44.500 = 1,426966 ; batas margin 40% = 50.500/0,6 = 84.166,67 -> 84.167
        item = [S.parse_item(x) for x in self.ITEM]
        h = S.hitung_bundel(item, D(95000), D(6000), margin_min=D("0.4"))
        self.assertEqual(h["total_normal"], D(108000))
        self.assertEqual(h["hpp_bundel"], D(50500))
        self.assertEqual(S.pct(h["hemat_persen"]), "12,04%")
        self.assertEqual(h["laba_bundel"], D(44500))
        self.assertEqual(S.pct(h["margin_terpisah"]), "58,8%")
        self.assertEqual(S.pct(h["faktor"] - 1), "42,7%")
        self.assertEqual(h["batas"], D(84167))
        self.assertEqual(h["peringatan"], [])

    def test_paket_tidak_hemat_dan_rugi(self):
        item = [S.parse_item(x) for x in self.ITEM]
        self.assertTrue(any("tidak lebih murah" in p for p in S.hitung_bundel(item, D(110000))["peringatan"]))
        self.assertTrue(any("RUGI" in p for p in S.hitung_bundel(item, D(44000))["peringatan"]))

    def test_item_qty(self):
        i = S.parse_item("Donat:6000:2500:6")
        self.assertEqual(i["qty"], 6)
        h = S.hitung_bundel([i], D(30000))      # 36.000 vs 30.000 ; HPP 15.000 ; laba 15.000
        self.assertEqual(h["laba_bundel"], D(15000))


class Elastisitas(unittest.TestCase):
    def test_naik_turun_10(self):
        # naik 10%: 30.800, laba/unit 19.300 ; volume impas 600 x 16.500/19.300 = 512,95 -> 513
        #   elastisitas impas (512,95/600 - 1)/0,1 = -1,4508 ; e=-1 -> 540 unit, laba 540 x 19.300 = 10.422.000
        #   e=-2 -> 480 unit, laba 9.264.000, selisih 9.264.000 - 9.900.000 = -636.000
        # turun 10%: 25.200, laba/unit 13.700 ; impas 600 x 16.500/13.700 = 722,63 -> 723
        h = S.hitung_elastisitas(D(28000), D(600), D(11500), [D("0.1"), D("-0.1")])
        naik, turun = h["skenario"]
        self.assertEqual(h["dasar"], D(9900000))
        self.assertEqual(naik["harga_baru"], D(30800))
        self.assertEqual(naik["volume_impas"], D(513))
        self.assertEqual(str(naik["elastisitas_impas"].quantize(D("0.01"))), "-1.45")
        e1 = [r for r in naik["hasil"] if r["e"] == D(-1)][0]
        self.assertEqual((e1["volume"], e1["laba"]), (D(540), D(10422000)))
        e2 = [r for r in naik["hasil"] if r["e"] == D(-2)][0]
        self.assertEqual(e2["selisih"], D(-636000))
        self.assertEqual(turun["volume_impas"], D(723))
        self.assertFalse(h["peringatan_besar"])

    def test_harga_baru_langsung_dengan_biaya_tetap(self):
        # HPP naik ke 13.200; harga 28.000 -> 29.900 (naik 1.900/28.000 = 6,7857%), biaya tetap 6.500.000
        # dasar = 600 x 14.800 - 6.500.000 = 2.380.000 ; impas 600 x 14.800/16.700 = 531,74 -> 532
        # e=-1: 600 x (1 - 0,067857) = 559,29 -> 559 ; laba 559 x 16.700 - 6.500.000 = 2.835.300
        h = S.hitung_elastisitas(D(28000), D(600), D(13200), elastisitas=[D(-1)], biaya_tetap=D(6500000),
                                 harga_baru=[D(29900)])
        s = h["skenario"][0]
        self.assertEqual(h["dasar"], D(2380000))
        self.assertEqual(s["harga_baru"], D(29900))
        self.assertEqual(s["volume_impas"], D(532))
        self.assertEqual((s["hasil"][0]["volume"], s["hasil"][0]["laba"]), (D(559), D(2835300)))
        with self.assertRaises(S.InputError):
            S.hitung_elastisitas(D(28000), D(600), D(13200))

    def test_perubahan_besar_dan_volume_tidak_negatif(self):
        h = S.hitung_elastisitas(D(28000), D(600), D(11500), [D("0.6")], [D(-2)])
        self.assertTrue(h["peringatan_besar"])
        self.assertEqual(h["skenario"][0]["hasil"][0]["volume"], D(0))   # 1 - 2 x 0,6 < 0 -> 0


class Cantik(unittest.TestCase):
    def test_kandidat_52300(self):
        harga = [k for k, _ in S.kandidat_cantik(D(52300))]
        self.assertEqual(harga, [D(x) for x in (49000, 49900, 51900, 52900, 53000, 59000, 59900)])

    def test_kandidat_kecil_dan_batas(self):
        harga = [k for k, _ in S.kandidat_cantik(D(3700))]
        self.assertEqual(harga, [D(x) for x in (2900, 3500, 3900, 4000)])
        # batas = 30.000/0,6 = 50.000 -> 49.900 tidak aman, 51.900 aman
        h = S.hitung_cantik(D(52300), D(30000), D("0.4"))
        st = {b["harga"]: b["aman"] for b in h["baris"]}
        self.assertFalse(st[D(49900)])
        self.assertTrue(st[D(51900)])


class Ppn(unittest.TestCase):
    def test_belum_termasuk(self):
        # 28.000 x 11% = 3.080 ; total 31.080
        h = S.hitung_ppn(D(28000))
        self.assertEqual((h["ppn"], h["total"]), (D(3080), D(31080)))

    def test_pembulatan_ke_bawah(self):
        # 28.555 x 11% = 3.141,05 -> 3.141
        self.assertEqual(S.hitung_ppn(D(28555))["ppn"], D(3141))

    def test_termasuk_49900(self):
        # 49.900/1,11 = 44.954,95 ; DPP 44.955 -> PPN floor(4.945,05)=4.945 -> 49.900 (pas) ; 44.956 -> 49.901 (lebih)
        h = S.hitung_ppn(D(49900), "termasuk")
        self.assertEqual((h["dpp"], h["ppn"], h["sisa"]), (D(44955), D(4945), D(0)))

    def test_termasuk_sisa(self):
        # 100.000: DPP 90.090 -> PPN 9.909 (9.909,9) = 99.999 ; 90.091 -> 9.910 = 100.001 (lebih) -> sisa 1
        h = S.hitung_ppn(D(100000), "termasuk")
        self.assertEqual((h["dpp"], h["ppn"], h["sisa"]), (D(90090), D(9909), D(1)))

    def test_mewah(self):
        self.assertEqual(S.hitung_ppn(D(1000000), mewah=True)["ppn"], D(120000))


class Cli(unittest.TestCase):
    def test_semua_perintah_jalan(self):
        perintah = [
            ["margin", "--hpp", "11.500", "--harga", "28rb"],
            ["bep", "--biaya-tetap", "6,5jt", "--harga", "28000", "--hpp", "11500", "--volume", "600"],
            ["tangga", "--harga-ecer", "28000", "--hpp", "11500", "--margin-min", "35", "--level", "Reseller:10:15"],
            ["diskon", "--harga", "28000", "--hpp", "11500", "--beli-gratis", "2:1"],
            ["bundel", "--item", "A:28000:11500", "--item", "B:45000:19000", "--harga-bundel", "65000"],
            ["elastisitas", "--harga", "28000", "--volume", "600", "--hpp", "11500", "--ubah", "5", "--elastisitas", "-1,5"],
            ["cantik", "--harga", "52300"],
            ["ppn", "--harga", "49900", "--mode", "termasuk", "--status-pkp", "non-pkp"],
        ]
        for p in perintah:
            with self.subTest(p=p[0]):
                kode, out, err = jalan(*p)
                self.assertEqual(kode, 0, err)
                self.assertTrue(out.strip())

    def test_label_estimasi_dan_simulasi(self):
        _, out, _ = jalan("elastisitas", "--harga", "28000", "--volume", "600", "--hpp", "11500", "--ubah", "10")
        self.assertIn("ESTIMASI", out)
        _, out, _ = jalan("ppn", "--harga", "28000", "--status-pkp", "non-pkp")
        self.assertIn("SIMULASI", out)
        self.assertIn("Coretax", out)

    def test_input_rusak_pesan_ramah(self):
        rusak = [
            ["margin", "--hpp", "abc", "--harga", "28000"],
            ["margin", "--hpp", "11500", "--margin", "120"],
            ["bep", "--biaya-tetap", "1jt", "--harga", "10000", "--hpp", "12000"],
            ["diskon", "--harga", "28000", "--hpp", "11500", "--beli-gratis", "dua"],
            ["bundel", "--item", "A:28000", "--harga-bundel", "20000"],
            ["bundel", "--item", "A:28000:11500", "--harga-bundel", "20000"],
            ["elastisitas", "--harga", "28000", "--volume", "600", "--hpp", "11500", "--ubah", "10", "--elastisitas", "1"],
            ["tangga", "--harga-ecer", "28000", "--hpp", "11500", "--margin-min", "35", "--level", "Reseller"],
        ]
        for p in rusak:
            with self.subTest(p=p):
                kode, out, err = jalan(*p)
                self.assertEqual(kode, 2)
                self.assertIn("GAGAL:", err)
                self.assertNotIn("Traceback", err)


if __name__ == "__main__":
    unittest.main(verbosity=1)
