#!/usr/bin/env python3
"""Uji regresi strategi-konten-iklan (scripts/alokasi_anggaran.py).
Jalankan: python3 tests/uji_regresi.py   (Windows: python / py)

Semua angka acuan dihitung MANUAL (rumus di komentar), bukan disalin dari keluaran script.
Kasus dasar: anggaran Rp10.000.000, tujuan penjualan, harga rata-rata Rp150.000, margin 40%.
"""
import contextlib
import io
import json
import os
import sys
import unittest

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AKAR, "scripts"))
import alokasi_anggaran as A  # noqa: E402


def jalan(*argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            kode = A.main(list(argv))
        except SystemExit as e:
            kode = e.code
    return kode, out.getvalue(), err.getvalue()


def js(*argv):
    kode, out, err = jalan(*argv, "--json")
    assert kode == 0, err
    return json.loads(out)


class Parsing(unittest.TestCase):
    def test_diterima(self):
        for teks, nilai in [("1.500.000", 1500000), ("1,5jt", 1500000), ("500rb", 500000),
                            ("Rp2 juta", 2000000), ("20jt", 20000000), ("750 ribu", 750000),
                            ("1500000", 1500000), ("1,25jt", 1250000), ("2,5rb", 2500),
                            ("1.500", 1500), ("1,2 miliar", 1200000000), ("10k", 10000)]:
            self.assertEqual(A.parse_rupiah(teks), nilai, teks)

    def test_ambigu_atau_rusak_gagal(self):
        for teks in ["1,500", "1.5", "1.500jt", "1,500rb", "1,500,000", "5M", "abc", "", "-5rb",
                     "0", "1,5", "1,2345rb", "10 dolar", "1..500", "12.34.567"]:
            with self.assertRaises(A.Gagal, msg=teks):
                A.parse_rupiah(teks)

    def test_persen(self):
        from decimal import Decimal as D
        self.assertEqual(A.parse_persen("40%"), D(40))
        self.assertEqual(A.parse_persen("40"), D(40))
        self.assertEqual(A.parse_persen("32,5%"), D("32.5"))
        self.assertEqual(A.parse_persen("0,4%"), D("0.4"))
        for teks in ["0,4", "0", "101", "abc", "-5", "1.500%"]:
            with self.assertRaises(A.Gagal, msg=teks):
                A.parse_persen(teks)


class Pembulatan(unittest.TestCase):
    def test_sisa_positif(self):
        # 100 / 3 = 33,33 -> 33 x3 = 99, sisa +1 ke bagian pertama
        self.assertEqual(A.bagi(100, [1, 1, 1]), ([34, 33, 33], 1))

    def test_sisa_negatif(self):
        # 200 / 3 = 66,67 -> 67 x3 = 201, sisa -1 dikurangkan dari bagian pertama
        self.assertEqual(A.bagi(200, [1, 1, 1]), ([66, 67, 67], -1))

    def test_ke_bobot_terbesar(self):
        # 10 dengan bobot 1:2 -> 3,33->3 ; 6,67->7 = 10, tanpa sisa
        self.assertEqual(A.bagi(10, [1, 2]), ([3, 7], 0))
        # 1 dengan bobot 1:1:1 -> 0,33->0 x3 = 0, sisa +1 ke bagian pertama
        self.assertEqual(A.bagi(1, [1, 1, 1]), ([1, 0, 0], 1))

    def test_total_selalu_sama(self):
        for total in [100001, 333333, 999999, 1234567, 7777777]:
            for bobot in ([35, 20, 20, 15, 10], [55, 15, 30], [1, 1, 1, 2], [3, 7, 11]):
                b, _ = A.bagi(total, bobot)
                self.assertEqual(sum(b), total)


class Alokasi(unittest.TestCase):
    ARG = ["--anggaran", "10jt", "--aov", "150rb", "--margin", "40%"]

    def test_pembagian_kanal(self):
        h = js(*self.ARG)
        # 10.000.000 x (35,20,20,15,10)%
        self.assertEqual([k["anggaran"] for k in h["kanal"]],
                         [3500000, 2000000, 2000000, 1500000, 1000000])
        self.assertEqual(sum(k["anggaran"] for k in h["kanal"]), 10000000)
        self.assertEqual(h["sisa_pembulatan_kanal"], 0)

    def test_mingguan_dan_uji(self):
        h = js(*self.ARG)
        meta = h["kanal"][0]
        self.assertEqual(meta["per_minggu"], [875000] * 4)          # 3.500.000 / 4
        self.assertEqual(meta["uji"], 1050000)                      # 30% x 3.500.000
        self.assertEqual(meta["aman"], 2450000)
        self.assertEqual(h["total_per_minggu"], [2500000] * 4)      # 10.000.000 / 4

    def test_bobot_minggu(self):
        h = js(*self.ARG, "--bobot-minggu", "1", "1", "1", "2")
        # bobot total 5: meta 3.500.000 -> 700.000 x3 dan 1.400.000
        self.assertEqual(h["kanal"][0]["per_minggu"], [700000, 700000, 700000, 1400000])
        self.assertEqual(h["total_per_minggu"], [2000000, 2000000, 2000000, 4000000])

    def test_target_roas_cpa(self):
        t = js(*self.ARG)["target"]
        # laba kotor = 150.000 x 40% = 60.000 ; ROAS impas = 1/0,4 = 2,50
        self.assertEqual(t["laba_kotor_per_pesanan"], 60000)
        self.assertEqual(t["roas_impas"], "2.50")
        self.assertEqual(t["cpa_impas"], 60000)
        # target aman = 70% x 60.000 = 42.000 ; ROAS target = 150.000/42.000 = 3,5714 -> naik ke 3,58
        self.assertEqual(t["cpa_target"], 42000)
        self.assertEqual(t["roas_target"], "3.58")
        # pesanan impas = 10.000.000 / 60.000 = 166,67 -> 167
        self.assertEqual(t["pesanan_minimal_impas"], 167)

    def test_margin_tidak_bulat(self):
        # margin 30% -> ROAS impas 1/0,3 = 3,3333 -> naik ke 3,34 (tidak menyepelekan)
        h = js("--anggaran", "10jt", "--aov", "100rb", "--margin", "30%")
        self.assertEqual(h["target"]["roas_impas"], "3.34")
        self.assertEqual(h["target"]["cpa_target"], 21000)          # 100.000 x 30% x 70%

    def test_batas_uji_iklan_maks(self):
        h = {k["kanal"]: k for k in js(*self.ARG)["kanal"]}
        # minggu terkecil / (7 hari x batas harian): meta 875.000/175.000=5 ; tiktok 500.000/210.000=2
        # shopee 500.000/70.000=7 ; tiktokshop 375.000/140.000=2 ; google 250.000/175.000=1
        self.assertEqual({k: v["iklan_aktif_maks"] for k, v in h.items()},
                         {"meta": 5, "tiktok": 2, "shopee": 7, "tiktokshop": 2, "google": 1})

    def test_leads(self):
        h = js("--anggaran", "10jt", "--tujuan", "leads", "--aov", "1jt", "--margin", "30%",
               "--closing", "20%")
        # bobot 55/15/30 (shopee & tiktokshop bobot 0 -> tidak dipakai)
        self.assertEqual({k["kanal"]: k["anggaran"] for k in h["kanal"]},
                         {"meta": 5500000, "tiktok": 1500000, "google": 3000000})
        # laba = 300.000 ; CPL impas = 300.000 x 20% = 60.000 ; target = 42.000
        self.assertEqual(h["target"]["cpl_impas"], 60000)
        self.assertEqual(h["target"]["cpl_target"], 42000)
        self.assertEqual(set(h["kanal_dikeluarkan"]), {"Shopee Ads", "TikTok Shop Ads"})

    def test_awareness_tanpa_aov(self):
        h = js("--anggaran", "10jt", "--tujuan", "awareness", "--kanal", "meta,tiktok")
        self.assertEqual([k["anggaran"] for k in h["kanal"]], [5000000, 5000000])
        self.assertIsNone(h["target"])

    def test_anggaran_kecil_satu_kanal(self):
        h = js("--anggaran", "500rb", "--aov", "80rb", "--margin", "35%")
        self.assertEqual([k["kanal"] for k in h["kanal"]], ["meta"])
        self.assertEqual(h["kanal"][0]["anggaran"], 500000)
        self.assertEqual(h["kanal"][0]["iklan_aktif_maks"], 0)
        self.assertEqual(h["kanal"][0]["hari_tayang_terbiayai"], 20)   # 500.000 / 25.000
        self.assertEqual(sum(h["total_per_minggu"]), 500000)
        # laba 28.000 ; pesanan impas = 500.000/28.000 = 17,86 -> 18
        self.assertEqual(h["target"]["pesanan_minimal_impas"], 18)

    def test_anggaran_sedang_kanal_dibuang(self):
        # 5 jt: google 10% = 500rb < 700rb (28 hari x 25rb) -> dibuang; sisanya dibagi ulang
        h = js("--anggaran", "5jt", "--aov", "150rb", "--margin", "40%")
        self.assertNotIn("google", [k["kanal"] for k in h["kanal"]])
        self.assertEqual(sum(k["anggaran"] for k in h["kanal"]), 5000000)
        # bobot 35/20/20/15 (sum 90): meta 1.944.444,4->1.944.444 ; tiktok & shopee 1.111.111,1->1.111.111 ;
        # tiktokshop 833.333,3->833.333 ; jumlah 4.999.999 -> sisa +1 ke meta = 1.944.445
        self.assertEqual([k["anggaran"] for k in h["kanal"]], [1944445, 1111111, 1111111, 833333])
        self.assertEqual(h["sisa_pembulatan_kanal"], 1)

    def test_sisa_pembulatan_ditampilkan(self):
        # 3 kanal bobot 35/20/20 (jumlah 75) pada 4.000.000:
        # meta 1.866.666,67->1.866.667 ; tiktok & shopee 1.066.666,67->1.066.667 ; jumlah 4.000.001
        # sisa -1 dikurangkan dari meta -> 1.866.666
        args = ["--anggaran", "4.000.000", "--kanal", "meta,tiktok,shopee", "--aov", "100rb", "--margin", "40%"]
        h = js(*args)
        self.assertEqual([k["anggaran"] for k in h["kanal"]], [1866666, 1066667, 1066667])
        self.assertEqual(h["sisa_pembulatan_kanal"], -1)
        kode, out, _ = jalan(*args)
        self.assertIn("Sisa pembulatan: antar kanal -Rp1", out)

    def test_format_teks(self):
        kode, out, _ = jalan(*self.ARG)
        self.assertEqual(kode, 0)
        self.assertIn("Rp3.500.000", out)
        self.assertIn("2,50x", out)
        self.assertIn("Sisa pembulatan: Rp0", out)


class Penolakan(unittest.TestCase):
    def gagal(self, *argv, kata=""):
        kode, out, err = jalan(*argv)
        self.assertEqual(kode, 2, err)
        self.assertEqual(out, "")
        self.assertIn(kata, err)

    def test_anggaran_ambigu(self):
        self.gagal("--anggaran", "1,500", "--aov", "1", "--margin", "40%", kata="ambigu")

    def test_penjualan_tanpa_aov(self):
        self.gagal("--anggaran", "5jt", kata="--aov")

    def test_margin_ambigu(self):
        self.gagal("--anggaran", "5jt", "--aov", "100rb", "--margin", "0,4", kata="ambigu")

    def test_leads_tanpa_closing(self):
        self.gagal("--anggaran", "5jt", "--tujuan", "leads", "--aov", "1jt", "--margin", "30%", kata="--closing")

    def test_anggaran_terlalu_kecil(self):
        self.gagal("--anggaran", "50rb", "--aov", "100rb", "--margin", "40%", kata="terlalu kecil")

    def test_kanal_salah(self):
        self.gagal("--anggaran", "5jt", "--kanal", "youtube", "--aov", "100rb", "--margin", "40%", kata="tidak dikenal")

    def test_bobot_minggu_salah_jumlah(self):
        self.gagal("--anggaran", "5jt", "--aov", "100rb", "--margin", "40%", "--bobot-minggu", "1", "2", kata="4 angka")

    def test_kategori_dilarang(self):
        self.gagal("--anggaran", "5jt", "--aov", "100rb", "--margin", "40%", "--kategori", "judi online", kata="dilarang")

    def test_singkatan_opsi_ditolak(self):
        # allow_abbrev=False: '--anggar' tidak boleh dianggap '--anggaran'
        self.gagal("--anggar", "5jt", "--aov", "100rb", "--margin", "40%", kata="")

    def test_aov_tanpa_margin(self):
        self.gagal("--anggaran", "5jt", "--tujuan", "awareness", "--aov", "100rb", kata="berpasangan")

    def test_catatan_kategori_terbatas(self):
        for kat in ["kesehatan", "keuangan", "kripto"]:
            h = js("--anggaran", "5jt", "--aov", "100rb", "--margin", "40%", "--kategori", kat)
            self.assertTrue(any("TERBATAS" in c for c in h["catatan"]), kat)


class Perbaikan101(unittest.TestCase):
    """Tes v1.0.1. Angka dihitung manual (rumus di komentar)."""
    DASAR = ["--aov", "150rb", "--margin", "40%"]

    def test_s1_saringan_kanal_pakai_minggu_terkecil(self):
        # 5jt, bobot minggu 1 1 1 4 (total 7): google 500rb -> minggu kecil 71.428 < 175.000 -> keluar.
        # tiktok 1.111.111/7 = 158.730 < 210.000 dan tiktokshop 833.333/7 = 119.047 < 140.000 -> keluar berurutan.
        # tersisa meta:shopee = 35:20 -> 5.000.000 x 35/55 = 3.181.818 ; shopee 1.818.182
        h = js("--anggaran", "5jt", *self.DASAR, "--bobot-minggu", "1", "1", "1", "4")
        self.assertEqual([(k["kanal"], k["anggaran"]) for k in h["kanal"]],
                         [("meta", 3181818), ("shopee", 1818182)])
        # meta minggu: 3.181.818 x 1/7 = 454.545 (x3), 4/7 = 1.818.182 ; jumlah 3.181.817 -> sisa +1 ke minggu 4
        self.assertEqual(h["kanal"][0]["per_minggu"], [454545, 454545, 454545, 1818183])
        self.assertEqual(h["kanal"][0]["iklan_aktif_maks"], 2)     # 454.545 // 175.000
        self.assertEqual(h["kanal"][1]["iklan_aktif_maks"], 3)     # 259.740 // 70.000
        self.assertTrue(all(k["iklan_aktif_maks"] >= 1 for k in h["kanal"]))
        self.assertEqual(sum(k["anggaran"] for k in h["kanal"]), 5000000)
        self.assertTrue(any("minggu terkecil" in v for v in h["kanal_dikeluarkan"].values()))

    def test_s1_di_bawah_batas_selalu_ada_catatan_dan_hari_dibatasi(self):
        h = js("--anggaran", "500rb", "--aov", "80rb", "--margin", "35%")
        self.assertTrue(any("DI BAWAH batas uji" in c for c in h["catatan"]))
        # --minggu 1: 7 hari; 500.000 / 25.000 = 20 hari tetapi dibatasi 7
        h = js("--anggaran", "100rb", "--aov", "80rb", "--margin", "35%", "--minggu", "1", "--kanal", "meta")
        self.assertEqual(h["kanal"][0]["hari_tayang_terbiayai"], 4)   # 100.000 / 25.000
        h = js("--anggaran", "1jt", "--aov", "80rb", "--margin", "35%", "--minggu", "1", "--kanal", "meta",
               "--min-harian", "5rb")
        self.assertGreaterEqual(h["kanal"][0]["iklan_aktif_maks"], 1)

    def test_s2_marketplace_mempertahankan_shopee(self):
        # 500rb: minggu 125.000 ; hanya shopee (70.000/minggu) yang layak
        h = js("--anggaran", "500rb", "--aov", "80rb", "--margin", "35%", "--jenis", "marketplace")
        self.assertEqual([k["kanal"] for k in h["kanal"]], ["shopee"])
        self.assertEqual(h["kanal"][0]["anggaran"], 500000)
        self.assertEqual(h["kanal"][0]["iklan_aktif_maks"], 1)     # 125.000 // 70.000
        self.assertFalse(any("DI BAWAH" in c for c in h["catatan"]))

    def test_s2_jasa_lokal_mempertahankan_google(self):
        # leads 1,5jt: google 1.500.000 -> minggu 375.000 // 175.000 = 2 ; CPL impas 500rb x 40% x 20% = 40.000
        h = js("--anggaran", "1,5jt", "--tujuan", "leads", "--aov", "500rb", "--margin", "40%",
               "--closing", "20%", "--jenis", "jasa-lokal")
        self.assertEqual([(k["kanal"], k["anggaran"]) for k in h["kanal"]], [("google", 1500000)])
        self.assertEqual(h["kanal"][0]["iklan_aktif_maks"], 2)
        self.assertEqual(h["target"]["cpl_impas"], 40000)
        self.assertEqual(h["target"]["cpl_target"], 28000)         # 70%
        self.assertIn("Meta (IG/FB)", h["kanal_dikeluarkan"])
        # tanpa --jenis (umum): tetap perilaku lama, Meta yang dipertahankan
        h = js("--anggaran", "1,5jt", "--tujuan", "leads", "--aov", "500rb", "--margin", "40%", "--closing", "20%")
        self.assertEqual([k["kanal"] for k in h["kanal"]], ["meta"])

    def test_s3_tujuan_campuran(self):
        # bobot = 30% awareness (40,40,5,5,10) + 70% penjualan (35,20,20,15,10)
        # meta 12+24,5=36,5 ; tiktok 12+14=26 ; shopee 1,5+14=15,5 ; tiktokshop 1,5+10,5=12 ; google 3+7=10
        h = js("--anggaran", "10jt", "--tujuan", "awareness:30,penjualan:70", *self.DASAR)
        self.assertEqual([k["anggaran"] for k in h["kanal"]], [3650000, 2600000, 1550000, 1200000, 1000000])
        self.assertEqual(sum(k["anggaran"] for k in h["kanal"]), 10000000)
        self.assertEqual(h["porsi_tujuan"], {"awareness": 30, "penjualan": 70})
        self.assertEqual(h["target"]["roas_impas"], "2.50")
        self.assertEqual([k["iklan_aktif_maks"] for k in h["kanal"]], [5, 3, 5, 2, 1])
        # penjualan:100 sama dengan 'penjualan'
        self.assertEqual(js("--anggaran", "10jt", "--tujuan", "penjualan:100", *self.DASAR)["kanal"],
                         js("--anggaran", "10jt", *self.DASAR)["kanal"])

    def test_s3_tujuan_campuran_validasi(self):
        for tujuan, kata in [("awareness:30,penjualan:60", "harus tepat 100"),
                             ("awareness:50,penjualan:60", "harus tepat 100"),
                             ("awareness:50,awareness:50", "dua kali"),
                             ("awareness:30,promo:70", "tidak dikenal"),
                             ("awareness:30,penjualan", "salah format"),
                             ("awareness:30,penjualan:0", "lebih dari 0"),
                             ("promo", "tidak dikenal")]:
            kode, out, err = jalan("--anggaran", "5jt", "--tujuan", tujuan, *self.DASAR)
            self.assertEqual(kode, 2, tujuan)
            self.assertIn(kata, err, tujuan)

    def test_s3_campuran_leads_wajib_closing_dan_awareness_tanpa_aov(self):
        kode, _, err = jalan("--anggaran", "5jt", "--tujuan", "awareness:50,leads:50", *self.DASAR)
        self.assertEqual(kode, 2)
        self.assertIn("--closing", err)
        h = js("--anggaran", "10jt", "--tujuan", "awareness:100", "--kanal", "meta,tiktok")
        self.assertEqual([k["anggaran"] for k in h["kanal"]], [5000000, 5000000])

    def test_r1_margin_tipis(self):
        # margin 8%: ROAS impas 1/0,08 = 12,50 (>= 10) -> peringatan kuat
        h = js("--anggaran", "8jt", "--aov", "100rb", "--margin", "8%")
        self.assertEqual(h["target"]["roas_impas"], "12.50")
        self.assertTrue(any("PERINGATAN margin sangat tipis" in c for c in h["catatan"]))
        # margin 15%: 1/0,15 = 6,67 (5-10) -> catatan tipis biasa
        h = js("--anggaran", "8jt", "--aov", "100rb", "--margin", "15%")
        self.assertEqual(h["target"]["roas_impas"], "6.67")
        self.assertTrue(any("Margin tipis" in c for c in h["catatan"]))
        self.assertFalse(any("PERINGATAN" in c for c in h["catatan"]))
        # margin 40%: tanpa peringatan
        h = js("--anggaran", "8jt", "--aov", "100rb", "--margin", "40%")
        self.assertFalse(any("tipis" in c for c in h["catatan"]))

    def test_r1_margin_nol_dan_negatif(self):
        for m in ["-10%", "0%", "-5"]:
            kode, out, err = jalan("--anggaran", "8jt", "--aov", "100rb", "--margin", m)
            self.assertEqual(kode, 2, m)
            self.assertIn("SETIAP penjualan rugi", err, m)
        kode, out, err = jalan("--anggaran", "8jt", "--aov", "100rb", "--margin=-10%")
        self.assertIn("SETIAP penjualan rugi", err)

    def test_r2_kata_kunci_kategori(self):
        for kat in ["skincare", "suplemen diet", "klinik gigi", "kosmetik", "obat herbal", "pinjaman online",
                    "asuransi", "investasi saham", "crypto", "aset digital"]:
            h = js("--anggaran", "5jt", "--aov", "100rb", "--margin", "40%", "--kategori", kat)
            self.assertTrue(any("TERBATAS" in c for c in h["catatan"]), kat)
        h = js("--anggaran", "5jt", "--aov", "100rb", "--margin", "40%", "--kategori", "kaos")
        self.assertFalse(any("TERBATAS" in c for c in h["catatan"]))
        self.assertTrue(any("cek dulu" in c for c in h["catatan"]))

    def test_r3_alias_kanal_dan_format_rupiah(self):
        arg = ["--anggaran", "10jt", "--tujuan", "awareness"]
        for teks, harap in [("ig,fb", ["meta"]), ("Instagram, Facebook", ["meta"]),
                            ("tiktok shop", ["tiktokshop"]), ("TikTok-Shop,shopee", ["shopee", "tiktokshop"]),
                            ("Shopee Ads", ["shopee"]), ("google ads; ig", ["meta", "google"]),
                            ("meta tiktok", ["meta", "tiktok"])]:
            h = js(*arg, "--kanal", teks)
            self.assertEqual(sorted(k["kanal"] for k in h["kanal"]), sorted(harap), teks)
        h = js(*arg, "--kanal", "tokopedia,ig")
        self.assertEqual(sorted(k["kanal"] for k in h["kanal"]), ["meta", "tiktokshop"])
        self.assertTrue(any("Tokopedia" in c for c in h["catatan"]))
        self.assertEqual(A.parse_rupiah("Rp 3.000.000,-"), 3000000)
        self.assertEqual(A.parse_rupiah("IDR 3jt"), 3000000)
        self.assertEqual(A.parse_rupiah("Rp. 1.500.000"), 1500000)
        for buruk in ["3.000.000,-,-", "rp -", "IDR"]:
            with self.assertRaises(A.Gagal, msg=buruk):
                A.parse_rupiah(buruk)
        self.gagal_kanal("youtube")

    def gagal_kanal(self, kanal):
        kode, out, err = jalan("--anggaran", "5jt", "--kanal", kanal, "--aov", "100rb", "--margin", "40%")
        self.assertEqual(kode, 2)
        self.assertIn(f"'{kanal}' tidak dikenal", err)

    def test_r4_pesan_margin_dinamis(self):
        for teks, alt in [("0,4", "40%"), ("0,5", "50%"), ("0,25", "25%")]:
            with self.assertRaises(A.Gagal) as c:
                A.parse_persen(teks)
            self.assertIn(f"{teks}% atau {alt}", str(c.exception))

    def test_r5_kanal_penjualan_utama(self):
        # Penjual Shopee + IG, 4jt: bobot meta 35, shopee dinaikkan ke 2 x 35 = 70 -> 1/3 : 2/3
        dasar = ["--anggaran", "4jt", "--aov", "175rb", "--margin", "35%", "--kanal", "meta,shopee"]
        for ekstra in (["--jenis", "marketplace"], ["--kanal-utama", "shopee"]):
            h = js(*dasar, *ekstra)
            ang = {k["kanal"]: k["anggaran"] for k in h["kanal"]}
            self.assertEqual(ang, {"meta": 1333333, "shopee": 2666667})   # 4.000.000/3 dibulatkan; sisa ke terbesar
            self.assertGreater(ang["shopee"], ang["meta"])
            self.assertTrue(any("Kanal penjualan utama: Shopee Ads" in c for c in h["catatan"]))
        # tanpa jenis/kanal-utama: perilaku lama (meta 35 : shopee 20)
        h = js(*dasar)
        self.assertEqual({k["kanal"]: k["anggaran"] for k in h["kanal"]}, {"meta": 2545455, "shopee": 1454545})
        # penjual yang transaksinya lewat DM IG: --kanal-utama meta -> meta 2 x 20 = 70 (tetap 70 karena 35 < 40)
        h = js(*dasar, "--kanal-utama", "ig")
        self.assertEqual({k["kanal"]: k["anggaran"] for k in h["kanal"]}, {"meta": 2666667, "shopee": 1333333})
        # TikTok Shop sebagai utama dengan 3 kanal: tiktokshop = 2 x 35 = 70 ; total 70+35+20 = 125
        h = js("--anggaran", "10jt", "--aov", "100rb", "--margin", "40%", "--kanal", "meta,tiktok,tiktokshop",
               "--kanal-utama", "tiktok shop")
        self.assertEqual({k["kanal"]: k["anggaran"] for k in h["kanal"]},
                         {"meta": 2800000, "tiktok": 1600000, "tiktokshop": 5600000})
        # awareness murni: tidak dinaikkan
        h = js("--anggaran", "4jt", "--tujuan", "awareness", "--kanal", "meta,shopee", "--kanal-utama", "shopee")
        self.assertEqual({k["kanal"]: k["anggaran"] for k in h["kanal"]}, {"meta": 3555556, "shopee": 444444})

    def test_r5_kanal_utama_validasi(self):
        kode, _, err = jalan("--anggaran", "4jt", "--aov", "175rb", "--margin", "35%", "--kanal", "meta",
                             "--kanal-utama", "shopee")
        self.assertEqual(kode, 2)
        self.assertIn("tidak ada di --kanal", err)
        kode, _, err = jalan("--anggaran", "4jt", "--aov", "175rb", "--margin", "35%", "--kanal-utama", "shopee,meta")
        self.assertEqual(kode, 2)
        self.assertIn("hanya satu kanal", err)

    def test_semua_kombinasi_total_sama_dengan_anggaran(self):
        for ang in ["500rb", "1,5jt", "3jt", "7,777jt".replace("7,777jt", "7777777"), "20jt"]:
            for tujuan in ["penjualan", "awareness:30,penjualan:70", "leads:50,awareness:50"]:
                for jenis in ["umum", "marketplace", "jasa-lokal"]:
                    for bm in (["1", "1", "1", "1"], ["1", "1", "1", "3"]):
                        h = js("--anggaran", ang, "--tujuan", tujuan, "--jenis", jenis, "--aov", "200rb",
                               "--margin", "30%", "--closing", "20%", "--bobot-minggu", *bm)
                        self.assertEqual(sum(k["anggaran"] for k in h["kanal"]), h["anggaran"])
                        self.assertEqual(sum(h["total_per_minggu"]), h["anggaran"])
                        if len(h["kanal"]) > 1:
                            self.assertTrue(all(k["iklan_aktif_maks"] >= 1 for k in h["kanal"]))


if __name__ == "__main__":
    unittest.main(verbosity=1)
