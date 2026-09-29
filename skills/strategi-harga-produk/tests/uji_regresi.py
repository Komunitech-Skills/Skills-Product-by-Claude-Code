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


# ================================================================ revisi 1.0.1 (permintaan HASIL-UJI.md)

class Revisi101Pkp(unittest.TestCase):
    """Cacat 1: jalur PKP harus bisa dihitung penuh oleh script (kasus S3 nugget, CV fiktif)."""
    TERMASUK = S.Pajak("termasuk")

    def test_lantai_paket_176675(self):
        # HPP paket 93.000 + 2.500 = 95.500 ; margin 40% dari DPP -> DPP 95.500/0,6 = 159.166,67 -> 159.167
        # PPN floor(159.167 x 0,11 = 17.508,37) = 17.508 -> harga tayang 176.675 (BUKAN 176.700)
        h = S.hitung_margin(D(95500), margin=D("0.4"), pajak=self.TERMASUK)
        self.assertEqual((h["harga"], h["dpp"], h["ppn"]), (D(176675), D(159167), D(17508)))
        # 176.674 -> DPP 159.166 (159.167 + 17.508 = 176.675 > 176.674) -> margin < 40%
        self.assertLess(S.hitung_margin(D(95500), harga=D(176674), pajak=self.TERMASUK)["margin"], D("0.4"))

    def test_169900_margin_3761(self):
        # 169.900/1,11 = 153.063,06 ; DPP 153.063 + PPN floor(16.836,93)=16.836 = 169.899 -> sisa 1
        # 153.064 + 16.837 = 169.901 > 169.900 ; laba 153.063 - 95.500 = 57.563 ; margin 57.563/153.063 = 37,607%
        h = S.hitung_margin(D(95500), harga=D(169900), pajak=self.TERMASUK, margin_min=D("0.4"))
        self.assertEqual((h["dpp"], h["laba"]), (D(153063), D(57563)))
        self.assertEqual(S.pct(h["margin"]), "37,61%")
        self.assertFalse(h["aman"])
        self.assertEqual(h["batas"], D(176675))
        _, out, _ = jalan("margin", "--hpp", "95.500", "--harga", "169.900", "--ppn", "termasuk", "--margin-min", "40")
        self.assertIn("sisa pembulatan Rp1", out)
        self.assertIn("DI BAWAH MIN", out)

    def test_164900(self):
        # 164.900/1,11 = 148.558,56 ; 148.559 + floor(16.341,49)=16.341 = 164.900 pas ; laba 53.059 -> 35,72%
        h = S.hitung_margin(D(95500), harga=D(164900), pajak=self.TERMASUK)
        self.assertEqual(h["dpp"], D(148559))
        self.assertEqual(S.pct(h["margin"]), "35,72%")

    def test_bundel_termasuk_ppn(self):
        # 3 x 59.900 = 179.700 ; paket 150.000 -> DPP 135.136 (135.136 + 14.864 = 150.000)
        # laba paket 135.136 - 95.500 = 39.636 ; margin 29,33% ; satuan: DPP 59.900 = 53.964 -> 3 x 53.964 - 93.000 = 68.892
        # hemat tayang 29.700 (16,53%) ; lantai 40% = 176.675
        item = [S.parse_item("Nugget:59.900:31rb:3")]
        h = S.hitung_bundel(item, D(150000), D(2500), margin_min=D("0.4"), pajak=self.TERMASUK)
        self.assertEqual((h["dpp_bundel"], h["laba_bundel"], h["laba_terpisah"]), (D(135136), D(39636), D(68892)))
        self.assertEqual(S.pct(h["margin_bundel"]), "29,33%")
        self.assertEqual(S.pct(h["margin_terpisah"]), "42,55%")
        self.assertEqual((h["hemat"], S.pct(h["hemat_persen"])), (D(29700), "16,53%"))
        self.assertEqual(h["batas"], D(176675))
        self.assertFalse(h["aman"])

    def test_bep_dan_elastisitas_termasuk_ppn(self):
        # 59.900 -> DPP 53.964 ; laba 22.964 ; BEP 12.000.000/22.964 = 522,56 -> 523
        h = S.hitung_bep(D(12000000), D(59900), D(31000), pajak=self.TERMASUK)
        self.assertEqual(h["unit"], D(523))
        # 54.900 -> DPP 49.460 (49.461 + 5.440 = 54.901 > 54.900) ; laba 18.460 ; impas 800 x 18.460/22.964 = 643,09 -> 644
        e = S.hitung_elastisitas(D(54900), D(800), D(31000), harga_baru=[D(59900)], pajak=self.TERMASUK)
        self.assertEqual(e["laba_unit"], D(18460))
        self.assertEqual(e["skenario"][0]["volume_impas"], D(644))

    def test_mode_belum_dan_potongan_dari_harga_tayang(self):
        # DPP 50.000 -> PPN 5.500 -> tayang 55.500 ; potongan 10% dari 55.500 = 5.550 ; laba 50.000 - 5.550 - 30.000 = 14.450
        h = S.hitung_margin(D(30000), harga=D(50000), biaya=D("0.1"), pajak=S.Pajak("belum"))
        self.assertEqual((h["tayang"], h["potongan"], h["laba"]), (D(55500), D(5550), D(14450)))
        self.assertEqual(S.pct(h["margin"]), "28,9%")

    def test_cantik_dan_tangga_termasuk_ppn(self):
        h = S.hitung_cantik(D(176675), D(95500), D("0.4"), pajak=self.TERMASUK)
        st = {b["harga"]: b["aman"] for b in h["baris"]}
        self.assertFalse(st[D(169900)])
        self.assertFalse(st[D(175900)])   # DPP 158.469 -> 39,74%
        self.assertTrue(st[D(176900)])    # DPP 159.370 -> 40,08%
        t = S.hitung_tangga(D(59900), D(31000), [S.parse_level("Kafe:3:=50000")], D("0.4"), pajak=self.TERMASUK)
        # 50.000 -> DPP 45.045 (45.045 + 4.954 = 49.999, sisa 1) ; laba 14.045 ; margin 31,18% < 40%
        self.assertEqual(t["baris"][0]["dpp"], D(45045))
        self.assertFalse(t["baris"][0]["aman"])

    def test_markup_dengan_potongan_tidak_berubah(self):
        # 11.500 x 1,5 / 0,9 = 19.166,67 -> 19.167 (rumus lama tetap berlaku tanpa PPN)
        self.assertEqual(S.hitung_margin(D(11500), markup=D("0.5"), biaya=D("0.1"))["harga"], D(19167))

    def test_cli_ppn_semua_perintah(self):
        perintah = [
            ["margin", "--hpp", "95500", "--margin", "40", "--ppn", "termasuk"],
            ["bep", "--biaya-tetap", "12jt", "--harga", "59900", "--hpp", "31000", "--ppn", "termasuk"],
            ["tangga", "--harga-ecer", "59900", "--hpp", "31000", "--margin-min", "30", "--level", "R:10:10", "--ppn", "termasuk"],
            ["diskon", "--harga", "59900", "--hpp", "31000", "--diskon", "10", "--ppn", "termasuk"],
            ["bundel", "--item", "N:59900:31000:3", "--harga-bundel", "165000", "--ppn", "termasuk"],
            ["elastisitas", "--harga", "54900", "--volume", "800", "--hpp", "31000", "--harga-baru", "59900", "--ppn", "termasuk"],
            ["cantik", "--harga", "176675", "--hpp", "95500", "--margin-min", "40", "--ppn", "belum", "--mewah"],
        ]
        for p in perintah:
            with self.subTest(p=p[0]):
                kode, out, err = jalan(*p)
                self.assertEqual(kode, 0, err)
                self.assertIn("DPP", out)
                self.assertIn("Coretax", out)


class Revisi101Reseller(unittest.TestCase):
    """Cacat 3: harga reseller konsisten dengan harga toko; reseller tetap untung."""

    def test_anjuran_lebih_mahal_dari_toko(self):
        # kasus S1: toko Rp47.900 tetapi reseller disuruh jual Rp49.900 -> peringatan
        h = S.hitung_tangga(D(47900), D(22000), [S.parse_level("Reseller:10:15")], D("0.4"), harga_anjuran=D(49900))
        self.assertTrue(any("LEBIH MAHAL" in p and "toko" in p for p in h["peringatan"]))

    def test_untung_reseller_default_harga_toko(self):
        # anjuran = eceran 47.900 ; reseller 15% -> 40.715 ; untung 7.185 (15%)
        h = S.hitung_tangga(D(47900), D(22000), [S.parse_level("Reseller:10:15")], D("0.4"))
        r = h["baris"][0]
        self.assertEqual((r["harga"], r["untung_reseller"]), (D(40715), D(7185)))
        self.assertEqual(S.pct(r["margin_reseller"]), "15%")
        self.assertEqual(h["peringatan"], [])

    def test_reseller_tidak_untung_dan_tipis(self):
        lv = [S.parse_level("Reseller:10:5"), S.parse_level("Agen:50:=48000")]
        h = S.hitung_tangga(D(47900), D(22000), lv, D("0.4"))
        self.assertTrue(any("Reseller" in p and "kurang tertarik" in p for p in h["peringatan"]))   # 5% < 10%
        self.assertTrue(any("Agen" in p and "TIDAK UNTUNG" in p for p in h["peringatan"]))
        self.assertTrue(any("terbalik" in p for p in h["peringatan"]))

    def test_eceran_sendiri_tidak_dicek_sebagai_reseller(self):
        h = S.hitung_tangga(D(28000), D(11500), [S.parse_level("Eceran:1:0")], D("0.35"))
        self.assertFalse(h["baris"][0]["reseller"])
        self.assertEqual(h["peringatan"], [])


class Revisi101Ringan(unittest.TestCase):
    """Cacat ringan 4-9."""

    def test_4_harga_di_bawah_modal(self):
        h = S.hitung_margin(D(30000), harga=D(25000))
        self.assertTrue(any("RUGI Rp5.000" in p for p in h["peringatan"]))
        kode, out, _ = jalan("margin", "--hpp", "30000", "--harga", "30000")
        self.assertEqual(kode, 0)
        self.assertIn("PERHATIAN: harga di bawah modal", out)

    def test_5_batas_aman_tidak_negatif(self):
        # kontribusi 10.000 ; BEP 1.200 ; jual 800 -> kurang 400 unit (400/1.200 = 33,33%)
        h = S.hitung_bep(D(12000000), D(30000), D(20000), volume=D(800))
        self.assertNotIn("batas_aman", h)
        self.assertEqual((h["kurang"], S.pct(h["kurang_persen"])), (D(400), "33,33%"))
        _, out, _ = jalan("bep", "--biaya-tetap", "12jt", "--harga", "30000", "--hpp", "20000", "--volume", "800")
        self.assertIn("kurang 400 unit (33,33%)", out)
        self.assertNotIn("-33", out)
        _, out, _ = jalan("bep", "--biaya-tetap", "12jt", "--harga", "30000", "--hpp", "20000", "--volume", "0")
        self.assertIn("kurang 1.200 unit (100%)", out)

    def test_6_hari_jual_harus_positif(self):
        for hari in ("-5", "0", "dua"):
            with self.subTest(hari=hari):
                kode, _, err = jalan("bep", "--biaya-tetap", "1jt", "--harga", "30000", "--hpp", "20000", "--hari-jual", hari)
                self.assertEqual(kode, 2)
                self.assertIn("hari jual", err)
        with self.assertRaises(S.InputError):
            S.hitung_bep(D(1000000), D(30000), D(20000), hari_jual=0)

    def test_7_tanpa_pembagian_nol(self):
        rusak = [
            ["tangga", "--harga-ecer", "300", "--hpp", "100", "--margin-min", "10", "--level", "R:10:50", "--kelipatan", "500"],
            ["diskon", "--harga", "1", "--hpp", "0,5", "--diskon", "60"],
            ["elastisitas", "--harga", "1", "--volume", "10", "--hpp", "0,5", "--ubah", "-60"],
        ]
        for p in rusak:
            with self.subTest(p=p):
                kode, _, err = jalan(*p)
                self.assertEqual(kode, 2)
                self.assertIn("Rp0", err)
                self.assertNotIn("Traceback", err)

    def test_8_angka_ambigu_ditolak(self):
        for teks in ("12.5", "1.25", "28.50"):
            with self.subTest(teks=teks):
                with self.assertRaises(S.InputError):
                    S.parse_rupiah(teks)
        self.assertEqual(S.parse_rupiah("12.500"), D(12500))
        self.assertEqual(S.parse_rupiah("1.5jt"), D(1500000))
        self.assertEqual(S.parse_rupiah("12,5rb"), D(12500))
        h = S.hitung_margin(D(100), harga=D(28000))
        self.assertTrue(any("kurang dari 1%" in p for p in h["peringatan"]))

    def test_9_laba_promo_dibulatkan_di_tampilan(self):
        # beli 2 gratis 1: laba efektif 7.166,67 -> tampil Rp7.167 (hitungan tetap presisi)
        _, out, _ = jalan("diskon", "--harga", "28000", "--hpp", "11500", "--beli-gratis", "2:1")
        self.assertIn("laba Rp7.167/unit", out)
        self.assertNotIn("Rp7.166,67", out)

    def test_status_margin_min_pada_margin_dan_diskon(self):
        h = S.hitung_margin(D(11500), harga=D(17000), margin_min=D("0.35"))
        self.assertFalse(h["aman"])
        self.assertEqual(h["batas"], D(17693))
        _, out, _ = jalan("diskon", "--harga", "28000", "--hpp", "11500", "--diskon", "40", "--margin-min", "35")
        self.assertIn("DI BAWAH minimum", out)   # 16.800 -> margin 31,55% < 35%


class Revisi101Dokumen(unittest.TestCase):
    """Cacat 2, 3, 10, 11: aturan di SKILL.md."""

    def setUp(self):
        with open(os.path.join(AKAR, "SKILL.md"), encoding="utf-8") as f:
            self.teks = f.read()

    def test_wajib_script_untuk_setiap_harga(self):
        self.assertIn("WAJIB", self.teks)
        for kata in ("reseller", "harga cantik", "--ppn termasuk", "--harga-anjuran", "bundel"):
            self.assertIn(kata, self.teks)

    def test_kartel_tanpa_klaim_sanksi(self):
        self.assertIn("UU 5/1999", self.teks)
        self.assertIn("tanpa klaim sanksi", self.teks)


if __name__ == "__main__":
    unittest.main(verbosity=1)
