#!/usr/bin/env python3
"""Uji regresi laporan-iklan-mingguan.

Mencakup: 1 CSV contoh per platform (Meta, TikTok Ads Manager, Shopee Ads, TikTok Shop Ads,
Google Ads) dengan nama kolom resmi (lihat references/sumber-kolom.md), angka format
Indonesia & Inggris campur, baris "Total" ganda, file kosong/rusak, mata uang asing, minggu
tanpa data pembanding, dan formula injection saat ekspor CSV hasil.

Jalankan: python3 tests/uji_regresi.py   (Windows: python / py)
"""
import csv
import io
import json
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

SINI = Path(__file__).resolve().parent.parent
SCRIPT = SINI / "scripts" / "laporan_iklan.py"

sys.path.insert(0, str(SINI / "scripts"))
import laporan_iklan as modul  # noqa: E402


def jalankan(*argv, cwd):
    r = subprocess.run([sys.executable, str(SCRIPT), *argv], cwd=cwd,
                        capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


def tulis_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


class UjiPlatform(unittest.TestCase):
    """Satu file contoh per platform, kolom persis seperti dokumentasi resmi
    (lihat references/sumber-kolom.md untuk sumber & tanggal akses)."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_meta_ads(self):
        p = self.dir / "meta.csv"
        tulis_csv(p, ["Campaign name", "Amount spent (IDR)", "Impressions", "Reach", "Link clicks",
                      "Results", "Purchase conversion value"],
                  [["Kaos A", 1500000, 80000, 60000, 900, 45, 4500000],
                   ["Kaos B", 800000, 40000, 35000, 300, 0, 0],
                   ["Total", 2300000, 120000, "", 1200, 45, 4500000]])
        code, out, err = jalankan("analisis", str(p), "--json", cwd=self.dir)
        self.assertEqual(code, 0, err)
        d = json.loads(out)
        self.assertEqual(d["platform_terdeteksi"], "Meta Ads (Facebook/Instagram)")
        self.assertEqual(d["baris_dilewati_baris_total"], 1)
        self.assertEqual(d["total"]["biaya"], 2300000)
        self.assertEqual(d["total"]["hasil"], 45)
        self.assertEqual(d["kolom_dipakai"]["nilai_hasil"], "Purchase conversion value")
        self.assertAlmostEqual(d["total"]["roas"], 4500000 / 2300000)
        # 1 kampanye tanpa hasil -> wajib muncul di saran (biaya >= 50rb)
        self.assertTrue(any("Kaos B" in s for s in d["saran"]))

    def test_tiktok_ads_manager(self):
        p = self.dir / "tiktok.csv"
        tulis_csv(p, ["Campaign name", "Cost", "Impressions", "Clicks (destination)", "Conversion",
                      "Total onsite value"],
                  [["Video A", "1.200.000", 95000, 1200, 30, 2500000],
                   ["Video B", "500000", 40000, 400, 0, 0]])
        code, out, err = jalankan("analisis", str(p), "--json", cwd=self.dir)
        self.assertEqual(code, 0, err)
        d = json.loads(out)
        self.assertEqual(d["platform_terdeteksi"], "TikTok Ads Manager")
        self.assertEqual(d["total"]["biaya"], 1700000)
        self.assertEqual(d["total"]["hasil"], 30)
        self.assertEqual(d["nama_hasil"], "Conversion")

    def test_shopee_ads_kolom_indonesia_dan_rp(self):
        p = self.dir / "shopee.csv"
        tulis_csv(p, ["Nama Iklan", "Dilihat", "Klik", "Konversi (Langsung)",
                      "Rasio Konversi (Langsung)", "Biaya", "Biaya per Konversi (Langsung)",
                      "Omzet Penjualan (Langsung)", "ACOS (Langsung)"],
                  [["Iklan Sepatu", 50000, 800, 20, "2,5%", "Rp600.000", "Rp30.000", "Rp3.000.000", "20%"],
                   ["Iklan Tas", 20000, 150, 0, "0%", "Rp150.000", "-", "Rp0", "-"],
                   ["Total", 70000, 950, 20, "", "Rp750.000", "", "Rp3.000.000", ""]])
        code, out, err = jalankan("analisis", str(p), "--json", cwd=self.dir)
        self.assertEqual(code, 0, err)
        d = json.loads(out)
        self.assertEqual(d["platform_terdeteksi"], "Shopee Ads")
        self.assertEqual(d["baris_dilewati_baris_total"], 1)
        self.assertEqual(d["total"]["biaya"], 750000)
        self.assertEqual(d["total"]["hasil"], 20)
        # kolom "Biaya per Konversi (Langsung)" TIDAK boleh salah kena kolom "biaya"
        self.assertEqual(d["kolom_dipakai"]["biaya"], "Biaya")
        self.assertEqual(d["kolom_dipakai"]["nilai_hasil"], "Omzet Penjualan (Langsung)")

    def test_tiktok_shop_ads(self):
        p = self.dir / "tiktokshop.csv"
        tulis_csv(p, ["Nama Kampanye", "Biaya", "Dilihat", "Klik", "Pesanan", "GMV"],
                  [["GMV Max - Tas", "900.000", 60000, 700, 15, "4.500.000"],
                   ["GMV Max - Dompet", "400.000", 25000, 200, 0, 0]])
        code, out, err = jalankan("analisis", str(p), "--json", cwd=self.dir)
        self.assertEqual(code, 0, err)
        d = json.loads(out)
        self.assertEqual(d["platform_terdeteksi"], "TikTok Shop Ads")
        self.assertEqual(d["total"]["biaya"], 1300000)
        self.assertEqual(d["nama_hasil"], "Pesanan")
        self.assertAlmostEqual(d["total"]["roas"], 4500000 / 1300000)

    def test_google_ads_kolom_singkatan(self):
        p = self.dir / "google.csv"
        tulis_csv(p, ["Campaign", "Cost", "Impr.", "Clicks", "Avg. CPC", "Conversions", "Conv. value"],
                  [["Search - Brand", 750000, 30000, 900, 833, 25, 5000000],
                   ["Display", 350000, 150000, 600, 583, 2, 300000]])
        code, out, err = jalankan("analisis", str(p), "--json", cwd=self.dir)
        self.assertEqual(code, 0, err)
        d = json.loads(out)
        self.assertEqual(d["platform_terdeteksi"], "Google Ads")
        self.assertEqual(d["total"]["tayangan"], 180000)  # "Impr." harus terbaca sbg tayangan
        self.assertEqual(d["total"]["hasil"], 27)


class UjiAngkaDanFormat(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_angka_campur_format_id_dan_en(self):
        p = self.dir / "campur.csv"
        tulis_csv(p, ["Campaign name", "Amount spent (IDR)", "Impressions", "Link clicks", "Results"],
                  [["A", "1.500.000", "80.000", "900", "45"],   # format Indonesia
                   ["B", "800,000", "40,000", "300", "0"]])      # format Inggris (koma ribuan)
        code, out, err = jalankan("analisis", str(p), "--json", cwd=self.dir)
        self.assertEqual(code, 0, err)
        d = json.loads(out)
        self.assertEqual(d["total"]["biaya"], 2300000)
        self.assertEqual(d["total"]["tayangan"], 120000)

    def test_pembulatan_rupiah_dan_persen(self):
        self.assertEqual(modul.bulat_rupiah(100.5), 101)     # 0,5 menjauhi nol
        self.assertEqual(modul.bulat_rupiah(100.49), 100)
        self.assertEqual(modul.bulat_rupiah(-100.5), -101)
        self.assertEqual(modul.bulat_satu_desimal(91.65), 91.7)   # 0,05 menjauhi nol
        self.assertEqual(modul.bulat_satu_desimal(-91.65), -91.7)

    def test_pembagi_nol_jadi_strip(self):
        p = self.dir / "nolklik.csv"
        tulis_csv(p, ["Campaign name", "Amount spent (IDR)", "Impressions", "Link clicks", "Results"],
                  [["A", 100000, 0, 0, 0]])
        code, out, err = jalankan("analisis", str(p), cwd=self.dir)
        self.assertEqual(code, 0, err)
        self.assertIn("CPC: -", out)
        self.assertIn("CPM: -", out)
        self.assertIn("CTR: -", out)


class UjiInputBermasalah(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_file_kosong(self):
        p = self.dir / "kosong.csv"
        p.write_text("", encoding="utf-8")
        code, out, err = jalankan("analisis", str(p), cwd=self.dir)
        self.assertEqual(code, 2)
        self.assertIn("kosong", (out + err).lower())

    def test_file_hanya_header(self):
        p = self.dir / "header.csv"
        p.write_text("Campaign name,Amount spent (IDR),Impressions,Link clicks,Results\n", encoding="utf-8")
        code, out, err = jalankan("analisis", str(p), cwd=self.dir)
        self.assertEqual(code, 2)

    def test_file_rusak_tidak_traceback(self):
        p = self.dir / "rusak.csv"
        p.write_bytes(b"\x00\x01\xff\xfe\"tanpa,penutup\nbaris kedua\n\"\ndata,lagi\n")
        code, out, err = jalankan("analisis", str(p), cwd=self.dir)
        self.assertEqual(code, 2)
        self.assertNotIn("Traceback", err)

    def test_semua_baris_tidak_valid(self):
        p = self.dir / "invalid.csv"
        tulis_csv(p, ["Campaign name", "Amount spent (IDR)", "Impressions", "Link clicks", "Results"],
                  [["A", "abc", "def", "ghi", "jkl"]])
        code, out, err = jalankan("analisis", str(p), cwd=self.dir)
        self.assertEqual(code, 2)

    def test_kolom_wajib_tidak_terdeteksi_perlu_override(self):
        p = self.dir / "aneh.csv"
        tulis_csv(p, ["ID", "Nilai Aneh 1", "Nilai Aneh 2"], [[1, 100, 200]])
        code, out, err = jalankan("analisis", str(p), cwd=self.dir)
        self.assertEqual(code, 2)
        self.assertIn("--kolom-", (out + err))
        code2, out2, err2 = jalankan("analisis", str(p),
                                      "--kolom-biaya", "Nilai Aneh 1", "--kolom-tayangan", "Nilai Aneh 2",
                                      "--kolom-klik", "Nilai Aneh 2", "--kolom-hasil", "Nilai Aneh 1",
                                      "--nama-hasil", "lead", cwd=self.dir)
        self.assertEqual(code2, 0, err2)
        self.assertIn("lead", out2.lower())

    def test_mata_uang_asing_ditolak_tanpa_kurs(self):
        p = self.dir / "usd.csv"
        tulis_csv(p, ["Campaign name", "Amount spent (USD)", "Impressions", "Link clicks", "Results"],
                  [["X", 100, 10000, 200, 10]])
        code, out, err = jalankan("analisis", str(p), cwd=self.dir)
        self.assertEqual(code, 2)
        self.assertIn("USD", out + err)
        code2, out2, err2 = jalankan("analisis", str(p), "--kurs", "15800", cwd=self.dir)
        self.assertEqual(code2, 0, err2)
        self.assertIn("Rp 1.580.000", out2)

    def test_minggu_tanpa_data_pembanding(self):
        p = self.dir / "meta.csv"
        tulis_csv(p, ["Campaign name", "Amount spent (IDR)", "Impressions", "Link clicks", "Results"],
                  [["A", 500000, 20000, 300, 15]])
        code, out, err = jalankan("analisis", str(p), cwd=self.dir)  # tanpa --sebelumnya
        self.assertEqual(code, 0, err)
        self.assertNotIn("VS MINGGU LALU", out)

    def test_platform_berbeda_saat_dibandingkan_diberi_peringatan(self):
        meta = self.dir / "meta.csv"
        google = self.dir / "google.csv"
        tulis_csv(meta, ["Campaign name", "Amount spent (IDR)", "Impressions", "Link clicks", "Results"],
                  [["A", 500000, 20000, 300, 15]])
        tulis_csv(google, ["Campaign", "Cost", "Impr.", "Clicks", "Conversions"],
                  [["B", 400000, 18000, 280, 10]])
        code, out, err = jalankan("analisis", str(meta), "--sebelumnya", str(google), cwd=self.dir)
        self.assertEqual(code, 0, err)
        self.assertIn("berbeda platform/jenis hasil", out)


class UjiFormulaInjectionCsv(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_nama_kampanye_formula_disanitasi_di_csv_keluaran(self):
        p = self.dir / "injeksi.csv"
        keluaran = self.dir / "keluaran.csv"
        tulis_csv(p, ["Campaign name", "Amount spent (IDR)", "Impressions", "Link clicks", "Results"],
                  [["=cmd|'/c calc'!A1", 500000, 20000, 150, 5],
                   ["+SUM(1+1)", 100000, 5000, 50, 2],
                   ["@HYPERLINK(\"http://x\")", 100000, 5000, 50, 2],
                   ["-2+3", 100000, 5000, 50, 2],
                   ["Kampanye Normal", 300000, 15000, 100, 3]])
        code, out, err = jalankan("analisis", str(p), "--csv-keluaran", str(keluaran), cwd=self.dir)
        self.assertEqual(code, 0, err)
        with open(keluaran, encoding="utf-8-sig", newline="") as f:
            baris_csv = list(csv.reader(f))
        sel_nama = {b[0]: b[0] for b in baris_csv[1:]}  # nama kampanye = kolom pertama
        for pemicu in ("=cmd", "+SUM", "@HYPERLINK", "-2+3"):
            cocok = [nama for nama in sel_nama if pemicu in nama]
            self.assertEqual(len(cocok), 1, f"kampanye '{pemicu}' tidak ditemukan di {list(sel_nama)}")
            self.assertTrue(cocok[0].startswith("'"),
                             f"Sel '{cocok[0]}' harus diawali kutip tunggal (anti formula injection)")
        self.assertIn("Kampanye Normal", sel_nama)
        # Nama normal TIDAK boleh diberi kutip tambahan yang tidak perlu
        self.assertFalse(sel_nama["Kampanye Normal"].startswith("'"))


class UjiGabungLintasPlatform(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def test_gabung_dua_platform_dan_omzet(self):
        meta = self.dir / "meta.csv"
        tiktok = self.dir / "tiktok.csv"
        tulis_csv(meta, ["Campaign name", "Amount spent (IDR)", "Impressions", "Link clicks", "Results"],
                  [["A", 1000000, 50000, 500, 25]])
        tulis_csv(tiktok, ["Campaign name", "Cost", "Impressions", "Clicks (destination)", "Conversion"],
                  [["B", 500000, 30000, 300, 10]])
        j1 = self.dir / "j1.json"
        j2 = self.dir / "j2.json"
        for src, dst in ((meta, j1), (tiktok, j2)):
            code, out, err = jalankan("analisis", str(src), "--json", cwd=self.dir)
            self.assertEqual(code, 0, err)
            dst.write_text(out, encoding="utf-8")
        code, out, err = jalankan("gabung", str(j1), str(j2), "--omzet", "10000000", "--json", cwd=self.dir)
        self.assertEqual(code, 0, err)
        g = json.loads(out)
        self.assertEqual(g["total"]["biaya"], 1500000)
        # v1.0.1: nama hasil beda (Results vs Conversion) -> hasil TIDAK dijumlah + peringatan
        self.assertIsNone(g["total"]["hasil"])
        self.assertIsNone(g["total"]["biaya_per_hasil"])
        self.assertAlmostEqual(g["omzet"]["biaya_sebagai_persen_omzet"], 15.0)
        self.assertTrue(any("berbeda" in p for p in g["peringatan"]))

    def test_gabung_file_bukan_json_valid_ditolak_rapi(self):
        bukan_json = self.dir / "bukan.json"
        bukan_json.write_text("ini bukan json", encoding="utf-8")
        code, out, err = jalankan("gabung", str(bukan_json), cwd=self.dir)
        self.assertEqual(code, 2)
        self.assertNotIn("Traceback", err)


# ======================================================================================
# v1.0.1 — regresi untuk cacat uji independen v1.0.0 (examples/HASIL-UJI.md: T1-T4, S1-S4,
# R1-R8, K1). File contoh meniru bentuk ekspor apa adanya (sel kosong, baris judul, baris
# Total/"Total: Account", kolom Currency). Angka acuan dihitung ulang dengan Decimal/Fraction.
# ======================================================================================

META_INI = """Reporting starts,Reporting ends,Ad name,Ad delivery,Attribution setting,Results,Result indicator,Reach,Impressions,Cost per results,Amount spent (IDR),Link clicks,CPC (cost per link click) (IDR),CTR (link click-through rate),Ends
2026-09-14,2026-09-20,Video Testimoni - Paket Harian,active,7-day click or 1-day view,62,actions:onsite_conversion.messaging_conversation_started_7d,41250,68420,20090.32,1245600,1083,1150.14,1.582870,Ongoing
2026-09-14,2026-09-20,Carousel Menu Mingguan,active,7-day click or 1-day view,38,actions:onsite_conversion.messaging_conversation_started_7d,30110,52300,25959.21,986450,702,1405.20,1.342256,Ongoing
2026-09-14,2026-09-20,Promo Gratis Ongkir - Story,active,7-day click or 1-day view,21,actions:onsite_conversion.messaging_conversation_started_7d,25400,47810,38680.95,812300,655,1240.15,1.370006,Ongoing
2026-09-14,2026-09-20,Retargeting Pengunjung IG,active,7-day click or 1-day view,,actions:onsite_conversion.messaging_conversation_started_7d,9800,18760,,356900,212,1683.49,1.130064,Ongoing
2026-09-14,2026-09-20,Foto Produk Nasi Box,active,7-day click or 1-day view,4,actions:onsite_conversion.messaging_conversation_started_7d,15300,22150,124687.50,498750,188,2652.93,0.848758,Ongoing
2026-09-14,2026-09-20,Lookalike Pelanggan,active,7-day click or 1-day view,17,actions:onsite_conversion.messaging_conversation_started_7d,20040,31990,23657.65,402180,377,1066.79,1.178493,Ongoing
"""
META_LALU = """Reporting starts,Reporting ends,Ad name,Results,Impressions,Amount spent (IDR),Link clicks
2026-09-07,2026-09-13,Video Testimoni - Paket Harian,55,61200,1150000,990
2026-09-07,2026-09-13,Carousel Menu Mingguan,40,50100,900000,690
2026-09-07,2026-09-13,Promo Gratis Ongkir - Story,18,45000,790000,600
2026-09-07,2026-09-13,Retargeting Pengunjung IG,2,17000,300000,190
2026-09-07,2026-09-13,Foto Produk Nasi Box,6,21000,450000,170
2026-09-07,2026-09-13,Lookalike Pelanggan,12,29000,380000,330
"""
GOOGLE_MENTAH = """Campaign report
"September 14, 2026 - September 20, 2026"
Campaign status,Campaign,Budget,Budget type,Campaign type,Impr.,Interactions,Interaction rate,Avg. cost,Cost,Clicks,CTR,Avg. CPC,Conversions,Cost / conv.,Conv. value,Currency code
Enabled,Search - Brand Skincare,"150,000.00",Daily,Search,"8,412",913,10.85%,409.64,"374,000.00",913,10.85%,409.64,48.00,"7,791.67","5,280,000.00",IDR
Enabled,Search - Serum Jerawat,"200,000.00",Daily,Search,"21,775","1,204",5.53%,"1,097.87","1,321,835.00","1,204",5.53%,"1,097.87",36.50,"36,214.66","3,869,000.00",IDR
Enabled,PMax - Semua Produk,"250,000.00",Daily,Performance Max,"96,340","1,702",1.77%,958.21,"1,630,880.00","1,702",1.77%,958.21,41.25,"39,536.48","4,950,000.00",IDR
Paused,Display - Remarketing,"100,000.00",Daily,Display,0,0,--,--,0.00,0,--,--,0.00,--,0.00,IDR
Paused,Search - Kompetitor,"100,000.00",Daily,Search,0,0,--,--,0.00,0,--,--,0.00,--,0.00,IDR
Paused,Video - Tutorial,"100,000.00",Daily,Video,0,0,--,--,0.00,0,--,--,0.00,--,0.00,IDR
Total: Account,--,--,--,--,"126,527","3,819",3.02%,873.16,"3,326,715.00","3,819",3.02%,871.09,125.75,"26,454.99","14,099,000.00",IDR
Total: Search,--,--,--,--,"30,187","2,117",7.01%,801.07,"1,695,835.00","2,117",7.01%,801.06,84.50,"20,069.05","9,149,000.00",IDR
Total: Performance Max,--,--,--,--,"96,340","1,702",1.77%,958.21,"1,630,880.00","1,702",1.77%,958.21,41.25,"39,536.48","4,950,000.00",IDR
"""
TIKTOK = """Campaign name,Primary status,Budget,Cost,CPC (destination),CPM,Impressions,Clicks (destination),CTR (destination),Conversions,Cost per conversion,Conversion rate (CVR),Currency
Traffic Video UGC Skincare,Active,300000,1834250,412.19,9860.47,186020,4450,2.39%,57,32179.82,1.28%,IDR
Konversi Serum Vit C,Active,250000,1520700,588.73,14110.61,107770,2583,2.40%,71,21418.31,2.75%,IDR
Live Promo Payday,Inactive,500000,643810,1003.60,23480.12,27420,641,2.34%,0,0,0.00%,IDR
Spark Ads Review Kreator,Active,150000,905440,487.85,10910.53,82988,1856,2.24%,19,47654.74,1.02%,IDR
"""
SHOPEE_HEADER = ["Urutan", "Nama Iklan", "Status", "Jenis Iklan", "Dilihat", "Jumlah Klik", "Persentase Klik",
                 "Konversi", "Biaya per Konversi", "Omzet Penjualan", "Biaya", "ACOS"]
SHOPEE_BARIS = [
    ["1", "Hijab Voal Motif - Pencarian", "Berjalan", "Iklan Produk", "48.215", "1.206", "2,50%", "38", "Rp25.263", "Rp3.895.000", "Rp960.000", "24,65%"],
    ["2", "Gamis Katun Premium", "Berjalan", "Iklan Produk", "22.930", "641", "2,80%", "12", "Rp62.500", "Rp2.868.000", "Rp750.000", "26,15%"],
    ["3", "Toko - Iklan Toko", "Berjalan", "Iklan Toko", "15.404", "2", "0,01%", "0", "-", "Rp0", "Rp100.001", "-"],
    ["4", "Pashmina Ceruty", "Berjalan", "Iklan Produk", "61.772", "1.877", "3,04%", "25", "Rp17.852", "Rp1.620.000", "Rp446.294,5", "27,55%"],
    ["5", "Bundling Mukena Anak", "Dijeda", "Iklan Produk", "3.120", "58", "1,86%", "1", "Rp212.340", "Rp189.000", "Rp212.340", "112,35%"],
]
SHOPEE_ANGKA_TOTAL = ["151.441", "3.784", "2,50%", "76", "Rp32.482", "Rp8.572.000", "Rp2.468.635,5", "28,80%"]


class _Dasar(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def tulis(self, nama, teks, encoding="utf-8"):
        p = self.dir / nama
        p.write_text(teks, encoding=encoding, newline="")
        return p

    def json_ok(self, *argv):
        code, out, err = jalankan(*argv, "--json", cwd=self.dir)
        self.assertEqual(code, 0, err)
        return json.loads(out)


class UjiT1SelKosong(_Dasar):
    def test_meta_results_kosong_tidak_membuang_biaya_dan_arah_benar(self):
        ini = self.tulis("meta_ini.csv", META_INI)
        lalu = self.tulis("meta_lalu.csv", META_LALU)
        d = self.json_ok("analisis", str(ini), "--sebelumnya", str(lalu), "--nama-hasil", "pesan WA")
        self.assertEqual(d["total"]["biaya"], 4302180)
        self.assertEqual(d["total"]["tayangan"], 241430)
        self.assertEqual(d["total"]["klik"], 3217)
        self.assertEqual(d["total"]["hasil"], 142)
        self.assertEqual(modul.bulat_rupiah(d["total"]["biaya_per_hasil"]), 30297)
        pb = d["pembanding_minggu_lalu"]
        self.assertEqual(pb["biaya"]["persen"], 8.4)            # bukan "turun 0,6%"
        self.assertEqual(pb["biaya_per_hasil"]["persen"], 1.5)  # bukan "turun 6,9%"
        self.assertEqual(d["tiga_terburuk"][0]["nama"], "Retargeting Pengunjung IG")
        self.assertIn("Retargeting Pengunjung IG", d["saran"][0])
        self.assertTrue(any("kosong" in c and "Retargeting Pengunjung IG" in c and "Rp 356.900" in c
                            for c in d["catatan"]))
        self.assertEqual(d["periode"]["awal"], "2026-09-14")    # R1: Reporting starts/ends terbaca
        self.assertEqual(d["periode"]["akhir"], "2026-09-20")
        self.assertIn("Pesan WA: 142", d["teks"])              # K1: bukan "Pesan wa"

    def test_sel_konversi_kosong_biaya_tetap_masuk(self):
        p = self.tulis("k.csv", "Campaign name,Cost,Impressions,Clicks (destination),Conversions\n"
                                "A,500000,40000,900,20\nB,120000,9000,150,\n")
        d = self.json_ok("analisis", str(p))
        self.assertEqual(d["total"]["biaya"], 620000)
        self.assertEqual(d["total"]["hasil"], 20)

    def test_biaya_tidak_terbaca_baris_dibuang_dengan_nama_di_peringatan(self):
        p = self.tulis("r.csv", "Campaign name,Cost,Impressions,Clicks,Conversions\n"
                                "Iklan Rusak,lima ratus ribu,1000,10,1\nIklan Baik,300000,2000,20,2\n")
        d = self.json_ok("analisis", str(p))
        self.assertEqual(d["total"]["biaya"], 300000)
        self.assertTrue(any("Iklan Rusak" in x and "lima ratus ribu" in x for x in d["peringatan"]))
        self.assertIn("PERLU DICEK", d["teks"])

    def test_sampah_di_sel_angka_tidak_diterima_diam_diam(self):   # R3
        self.assertEqual(modul.baca_sel("250.000,00;x")[0], "rusak")
        self.assertEqual(modul.baca_sel("")[0], "kosong")
        self.assertEqual(modul.baca_sel("--")[0], "kosong")
        self.assertEqual(modul.baca_sel("—")[0], "kosong")
        self.assertEqual(modul.baca_sel("Rp10.000,-")[1], Decimal(10000))


class UjiT2BarisTotal(_Dasar):
    def _shopee(self, baris_total):
        p = self.dir / "shopee.csv"
        tulis_csv(p, SHOPEE_HEADER, SHOPEE_BARIS + [baris_total])
        return p

    def test_total_di_kolom_pertama_nama_kosong(self):
        d = self.json_ok("analisis", str(self._shopee(["Total", "", "", ""] + SHOPEE_ANGKA_TOTAL)))
        self.assertEqual(d["total"]["biaya"], 2468635.5)
        self.assertEqual(d["total"]["hasil"], 76)
        self.assertEqual(d["baris_dilewati_baris_total"], 1)
        self.assertFalse(any(k["nama"].startswith("(tanpa nama") for k in d["per_kampanye"]))

    def test_variasi_label_total(self):
        for label in ("Total", "TOTAL", "Total:", "Total (5 iklan)", "Total: Account", "Jumlah Total",
                      "Grand Total", "Jumlah", "Subtotal"):
            with self.subTest(label=label):
                d = self.json_ok("analisis", str(self._shopee(["", label, "", ""] + SHOPEE_ANGKA_TOTAL)))
                self.assertEqual(d["total"]["biaya"], 2468635.5, label)
                self.assertEqual(d["baris_dilewati_baris_total"], 1, label)

    def test_total_tanpa_label_dikenali_dari_angka(self):
        d = self.json_ok("analisis", str(self._shopee(["", "", "", ""] + SHOPEE_ANGKA_TOTAL)))
        self.assertEqual(d["total"]["biaya"], 2468635.5)
        self.assertTrue(any("baris TOTAL" in x for x in d["peringatan"]))

    def test_nama_kampanye_berawalan_total_bukan_baris_total(self):
        p = self.tulis("n.csv", "Campaign name,Cost,Impressions,Clicks,Conversions\n"
                                "Total Look Hijab,100000,1000,10,2\nPromo Lain,50000,500,5,1\n")
        d = self.json_ok("analisis", str(p))
        self.assertEqual(d["total"]["biaya"], 150000)
        self.assertEqual(d["baris_dilewati_baris_total"], 0)


class UjiT3KolomGoogle(_Dasar):
    def test_google_ekspor_mentah_judul_status_avg_cost_dan_total(self):
        d = self.json_ok("analisis", str(self.tulis("g.csv", GOOGLE_MENTAH)))
        kd = d["kolom_dipakai"]
        self.assertEqual(kd["nama"], "Campaign")
        self.assertEqual(kd["biaya"], "Cost")
        self.assertEqual(kd["tayangan"], "Impr.")
        self.assertEqual(kd["klik"], "Clicks")
        self.assertEqual(kd["hasil"], "Conversions")
        self.assertEqual(kd["nilai_hasil"], "Conv. value")
        self.assertEqual(d["total"]["biaya"], 3326715)
        self.assertEqual(d["total"]["hasil"], 125.75)
        self.assertEqual(d["baris_dilewati_baris_total"], 3)
        self.assertEqual(float(modul.bulat1(d["total"]["roas"])), 4.2)
        self.assertEqual(d["periode"]["awal"], "2026-09-14")   # dari baris judul
        # S2: kampanye dijeda (Rp 0) tidak mengisi PERLU PERHATIAN
        self.assertTrue(all(k["biaya"] > 0 for k in d["tiga_terburuk"]))
        self.assertIn("PMax - Semua Produk", [k["nama"] for k in d["tiga_terburuk"]])

    def test_google_tanpa_baris_judul(self):
        teks = "\n".join(GOOGLE_MENTAH.splitlines()[2:]) + "\n"
        d = self.json_ok("analisis", str(self.tulis("g2.csv", teks)))
        self.assertEqual(d["kolom_dipakai"]["biaya"], "Cost")
        self.assertEqual(d["total"]["biaya"], 3326715)

    def test_cek_kewajaran_bila_kolom_biaya_salah(self):
        d = self.json_ok("analisis", str(self.tulis("g3.csv", GOOGLE_MENTAH)), "--kolom-biaya", "Avg. cost")
        self.assertTrue(any("tidak wajar" in x for x in d["peringatan"]))

    def test_google_results_dan_results_value(self):   # R8
        p = self.tulis("g4.csv", "Campaign,Cost,Impr.,Clicks,Results,Results value\n"
                                 "A,100000,5000,100,4,500000\n")
        d = self.json_ok("analisis", str(p))
        self.assertEqual(d["kolom_dipakai"]["hasil"], "Results")
        self.assertEqual(d["kolom_dipakai"]["nilai_hasil"], "Results value")
        self.assertEqual(d["total"]["roas"], 5)

    def test_utf16_bertab_dan_xlsx(self):   # S3
        teks = GOOGLE_MENTAH
        rows = list(csv.reader(teks.splitlines()))
        buf = io.StringIO()
        csv.writer(buf, delimiter="\t", lineterminator="\r\n").writerows(rows)
        p = self.dir / "g16.csv"
        p.write_bytes(buf.getvalue().encode("utf-16"))
        d = self.json_ok("analisis", str(p))
        self.assertEqual(d["total"]["biaya"], 3326715)
        x = self.dir / "palsu.csv"
        x.write_bytes(b"PK\x03\x04isi-excel")
        code, out, err = jalankan("analisis", str(x), cwd=self.dir)
        self.assertEqual(code, 2)
        self.assertIn("Excel", err)


class UjiT4MataUang(_Dasar):
    def test_kolom_currency_usd_ditolak(self):
        p = self.tulis("u.csv", "Campaign name,Cost,Impressions,Clicks (destination),Conversions,Currency\n"
                                "A,111.84,186020,4450,57,USD\n")
        code, out, err = jalankan("analisis", str(p), cwd=self.dir)
        self.assertEqual(code, 2)
        self.assertIn("USD", err)
        self.assertNotIn("Rp 112", out)

    def test_simbol_dolar_di_sel_ditolak(self):
        p = self.tulis("d.csv", 'Campaign name,Cost,Impressions,Clicks (destination),Conversions\n'
                                'A,"$1,234.56",100000,1000,10\n')
        code, out, err = jalankan("analisis", str(p), cwd=self.dir)
        self.assertEqual(code, 2)
        self.assertIn("USD", err)

    def test_kurs_dari_kolom_currency_dihitung_decimal(self):
        p = self.tulis("u.csv", "Campaign name,Cost,Impressions,Clicks (destination),Conversions,Currency\n"
                                "A,111.84,186020,4450,57,USD\nB,0.33,100,1,0,USD\n")
        d = self.json_ok("analisis", str(p), "--kurs", "16350.5")
        # (111,84 + 0,33) × 16.350,5 = 1.834.058,09 (Decimal persis)
        self.assertEqual(Decimal(str(d["total"]["biaya"])), Decimal("112.17") * Decimal("16350.5"))
        self.assertTrue(any("USD" in c for c in d["catatan_mata_uang"]))

    def test_campur_mata_uang_ditolak(self):
        p = self.tulis("c.csv", "Campaign name,Cost,Impressions,Clicks,Conversions,Currency\n"
                                "A,100,1000,10,1,USD\nB,200000,1000,10,1,IDR\n")
        code, out, err = jalankan("analisis", str(p), cwd=self.dir)
        self.assertEqual(code, 2)
        self.assertIn("lebih dari satu mata uang", err)

    def test_rupiah_di_sel_dan_currency_idr_tetap_jalan(self):
        d = self.json_ok("analisis", str(self.tulis("t.csv", TIKTOK)))
        self.assertEqual(d["total"]["biaya"], 4904200)
        self.assertEqual(d["mata_uang"], "IDR")

    def test_kurs_nol_atau_negatif_ditolak(self):   # R3
        p = self.tulis("u.csv", "Campaign name,Amount spent (USD),Impressions,Link clicks,Results\nX,100,10000,200,10\n")
        for kurs in ("-16350", "0", "abc"):
            code, out, err = jalankan("analisis", str(p), "--kurs", kurs, cwd=self.dir)
            self.assertEqual(code, 2, kurs)
            self.assertIn("kurs", err)


class UjiS1Gabung(_Dasar):
    def _json(self, nama, teks, *argv):
        src = self.tulis(nama + ".csv", teks)
        code, out, err = jalankan("analisis", str(src), "--json", *argv, cwd=self.dir)
        self.assertEqual(code, 0, err)
        j = self.dir / (nama + ".json")
        j.write_text(out, encoding="utf-8")
        return str(j)

    def test_nama_hasil_sama_beda_platform_diberi_peringatan_dan_roas_hanya_platform_bernilai(self):
        t = self._json("tiktok", TIKTOK)
        g = self._json("google", GOOGLE_MENTAH)
        d = self.json_ok("gabung", t, g, "--omzet", "60 juta")
        self.assertEqual(d["total"]["biaya"], 8230915)
        self.assertEqual(d["total"]["hasil"], 272.75)
        self.assertTrue(any("atribusi" in x for x in d["peringatan"]))
        # ROAS gabungan hanya dari platform yang punya nilai (Google 14.099.000 / 3.326.715)
        self.assertEqual(float(modul.bulat1(d["total"]["roas"])), 4.2)
        self.assertIn("hanya Google Ads", d["total"]["roas_keterangan"])
        self.assertEqual(d["omzet"]["biaya_sebagai_persen_omzet"], 13.7)

    def test_catatan_kurs_ikut_dan_file_ganda_ditolak(self):
        u = self._json("usd", "Campaign name,Amount spent (USD),Impressions,Link clicks,Results\nX,100,10000,200,10\n",
                       "--kurs", "16000")
        code, out, err = jalankan("gabung", u, cwd=self.dir)
        self.assertEqual(code, 0, err)
        self.assertIn("kurs 1 USD", out)
        code, out, err = jalankan("gabung", u, u, cwd=self.dir)
        self.assertEqual(code, 2)
        self.assertIn("lebih dari sekali", err)

    def test_saran_platform_ketiga_tidak_terpotong(self):
        a = self._json("a", "Campaign name,Amount spent (IDR),Impressions,Link clicks,Results\n"
                            "A1,300000,1000,10,0\nA2,200000,1000,10,0\nA3,100000,1000,10,0\nA4,90000,1000,10,0\nA5,80000,1000,10,0\n")
        b = self._json("b", "Campaign,Cost,Impr.,Clicks,Conversions\nB1,70000,1000,10,0\n")
        c = self._json("c", TIKTOK)
        d = self.json_ok("gabung", a, b, c)
        self.assertTrue(any("Live Promo Payday" in s for s in d["saran"]), d["saran"])

    def test_json_bukan_hasil_analisis_pesan_ramah(self):
        x = self.tulis("x.json", '{"a": 1}')
        code, out, err = jalankan("gabung", str(x), cwd=self.dir)
        self.assertEqual(code, 2)
        self.assertIn("bukan hasil 'analisis --json'", err)


class UjiS2S4DanLainnya(_Dasar):
    def test_terbaik_dan_perlu_perhatian_tanpa_irisan(self):
        p = self.dir / "s.csv"
        tulis_csv(p, SHOPEE_HEADER, SHOPEE_BARIS)
        d = self.json_ok("analisis", str(p), "--nama-hasil", "pesanan")
        terbaik = {k["nama"] for k in d["tiga_terbaik"]}
        terburuk = {k["nama"] for k in d["tiga_terburuk"]}
        self.assertFalse(terbaik & terburuk)
        for nama in terbaik:
            self.assertFalse(any(nama in s and "matikan" in s for s in d["saran"]))

    def test_omzet_dengan_satuan(self):   # S4
        for teks, nilai in (("20 juta", 20000000), ("20jt", 20000000), ("Rp20.000.000", 20000000),
                            ("1,5 juta", 1500000), ("750 rb", 750000), ("1,2 miliar", 1200000000)):
            self.assertEqual(modul.parse_omzet(teks), nilai, teks)
        for teks in ("20M", "dua puluh juta", "20 bulan"):
            with self.assertRaises(ValueError):
                modul.parse_omzet(teks)

    def test_persen_tepat_x_x5_dibulatkan_menjauhi_nol(self):   # R2
        self.assertEqual(modul.bandingkan_persen(103000, 80000)[0], Decimal("28.8"))
        self.assertEqual(modul.bandingkan_persen(80000, 103000)[0], Decimal("-22.3"))
        self.assertEqual(modul.bandingkan_persen(5, 0, rupiah=False)[1], "naik dari 0 (persen tidak dihitung)")

    def test_minggu_lalu_file_sama_diberi_peringatan(self):   # R1
        p = self.tulis("m.csv", META_INI)
        d = self.json_ok("analisis", str(p), "--sebelumnya", str(p))
        self.assertTrue(any("SAMA PERSIS" in x for x in d["peringatan"]))

    def test_rentang_lebih_dari_7_hari_diberi_peringatan(self):   # R1
        p = self.tulis("t.csv", "Date,Campaign name,Cost,Impressions,Clicks,Conversions\n"
                                "2026-08-20,A,100000,1000,10,1\n2026-09-18,A,100000,1000,10,1\nkemarin,A,1,1,1,0\n")
        d = self.json_ok("analisis", str(p))
        self.assertTrue(any("30 hari" in x for x in d["peringatan"]))
        self.assertTrue(any("kemarin" in x for x in d["peringatan"]))

    def test_csv_keluaran_tidak_boleh_menimpa_input_dan_angka_konsisten(self):   # R4
        p = self.tulis("m.csv", META_INI)
        asli = p.read_bytes()
        code, out, err = jalankan("analisis", str(p), "--csv-keluaran", str(p), cwd=self.dir)
        self.assertEqual(code, 2)
        self.assertEqual(p.read_bytes(), asli)
        k = self.dir / "rincian.csv"
        code, out, err = jalankan("analisis", str(p), "--nama-hasil", "=1+1", "--csv-keluaran", str(k), cwd=self.dir)
        self.assertEqual(code, 0, err)
        with open(k, encoding="utf-8-sig", newline="") as f:
            baris = list(csv.reader(f))
        self.assertFalse(any(h.startswith("=") for h in baris[0]))
        video = next(b for b in baris if b[0].startswith("Video"))
        self.assertEqual(video[1:4], ["1245600", "68420", "1083"])   # tanpa pemisah ribuan
        self.assertEqual(video[8], "1.6")

    def test_file_tidak_ada_pesan_indonesia(self):   # K1
        code, out, err = jalankan("analisis", "tidak-ada.csv", cwd=self.dir)
        self.assertEqual(code, 2)
        self.assertIn("tidak ditemukan", err)
        self.assertNotIn("Errno", err)


# ======================================================================================
# v1.0.2 — temuan uji ulang v1.0.1 (examples/06-uji-ulang-v1.0.1.md): N1 & N2
# ======================================================================================

META_3LEVEL = ("Campaign name,Ad set name,Ad name,Amount spent (IDR),Impressions,Link clicks,Results\n"
               "Kamp,Set A,Video Testimoni,1850000,70000,1300,32\n"
               "Kamp,Set A,Carousel Produk,1492267,55000,900,17\n"
               "Kamp,Set B,Advantage+ Catalog,1080735,37000,600,\n")
KOLOM_SEDERHANA = "Campaign name,Cost,Impressions,Clicks,Conversions\n"


class UjiN1LevelRincian(_Dasar):
    def test_meta_tiga_level_dirinci_per_iklan_dan_iklan_boros_muncul(self):
        d = self.json_ok("analisis", str(self.tulis("m.csv", META_3LEVEL)))
        self.assertEqual(d["kolom_dipakai"]["nama"], "Ad name")
        self.assertEqual(d["level_rincian"], "iklan")
        self.assertEqual(d["kolom_induk"], ["Ad set name", "Campaign name"])
        self.assertEqual(d["total"]["biaya"], 4423002)          # total tidak berubah
        self.assertEqual(d["jumlah_kampanye"], 3)
        self.assertEqual(d["tiga_terburuk"][0]["nama"], "Advantage+ Catalog")
        self.assertIn("Advantage+ Catalog", d["saran"][0])
        cat = [c for c in d["catatan"] if "kosong" in c]
        self.assertEqual(len(cat), 1)
        self.assertIn("Rp 1.080.735", cat[0])                   # biaya BARIS, bukan kampanye
        self.assertNotIn("Rp 4.423.002", cat[0])
        # v1.0.12: catatan untuk pembeli awam tanpa nama opsi teknis
        self.assertTrue(any("dirinci per iklan" in c and "rinci per kampanye" in c and "--kolom" not in c
                            for c in d["catatan"]), d["catatan"])

    def test_nama_iklan_kembar_dibedakan_dengan_ad_set(self):
        teks = ("Campaign name,Ad set name,Ad name,Amount spent (IDR),Impressions,Link clicks,Results\n"
                "Kamp,Set0,Iklan Hijab,800000,40000,700,30\n"
                "Kamp,Set1,Iklan Hijab,645600,30000,400,25\n"
                "Kamp,Set2,Iklan Mukena,1000000,50000,780,30\n")
        d = self.json_ok("analisis", str(self.tulis("k.csv", teks)))
        nama = {k["nama"]: k["biaya"] for k in d["per_kampanye"]}
        self.assertEqual(nama, {"Iklan Hijab (Set0)": 800000, "Iklan Hijab (Set1)": 645600,
                                "Iklan Mukena": 1000000})
        self.assertEqual(d["total"]["biaya"], 2445600)

    def test_kolom_nama_manual_tetap_dihormati(self):
        d = self.json_ok("analisis", str(self.tulis("m.csv", META_3LEVEL)), "--kolom-nama", "Campaign name")
        self.assertEqual(d["jumlah_kampanye"], 1)
        self.assertEqual(d["level_rincian"], "kampanye")
        self.assertEqual(d["kolom_induk"], [])

    def test_kolom_ad_name_kosong_semua_pakai_ad_set(self):
        teks = ("Campaign name,Ad set name,Ad name,Amount spent (IDR),Impressions,Link clicks,Results\n"
                "Kamp,Set A,,500000,20000,300,10\nKamp,Set B,,300000,15000,100,\n")
        d = self.json_ok("analisis", str(self.tulis("s.csv", teks)))
        self.assertEqual(d["kolom_dipakai"]["nama"], "Ad set name")
        self.assertEqual(d["level_rincian"], "grup iklan")
        self.assertEqual(d["tiga_terburuk"][0]["nama"], "Set B")

    def test_satu_level_saja_perilaku_lama(self):
        d = self.json_ok("analisis", str(self.tulis("s.csv", KOLOM_SEDERHANA + "A,100000,1000,10,2\n")))
        self.assertEqual(d["kolom_dipakai"]["nama"], "Campaign name")
        self.assertEqual(d["level_rincian"], "kampanye")

    def test_sel_kosong_dihitung_per_baris_harian(self):   # R-b
        baris = "".join(f"2026-09-{14 + i},Live,10000,1000,20,-\n2026-09-{14 + i},Katalog,20000,2000,40,3\n"
                        for i in range(7))
        d = self.json_ok("analisis", str(self.tulis("h.csv", "Date,Campaign name,Cost,Impressions,"
                                                             "Clicks,Conversions\n" + baris)))
        cat = next(c for c in d["catatan"] if "kosong" in c)
        self.assertIn("kosong di 7 baris (Live)", cat)
        self.assertIn("Rp 70.000", cat)


class UjiN2BarisTotal(_Dasar):
    def test_jenis_label_total(self):
        f = modul.jenis_label_total
        for s in ("Total", "TOTAL", "Total:", "Total (5 iklan)", "Total: Account", "Total 4 kampanye",
                  "TOTAL - Semua", "Jumlah", "Subtotal", "Grand Total", "Summary", "Totals:"):
            self.assertEqual(f(s), "kuat", s)
        for s in ("Total of 2 campaigns", "Totals", "Total Akun", "Total Keseluruhan", "Jumlah Total",
                  "Grand totals all campaigns", "Total for all ads", "Jumlah Semua Iklan", "Total Account",
                  "Overall results", "Total Keseluruhan Akun"):
            self.assertIn(f(s), ("kuat", "sedang"), s)
        for s in ("Total Look Hijab", "Summary Sale Gamis", "Jumlah Terbatas Promo"):
            self.assertEqual(f(s), "lemah", s)
        for s in ("Totalan Promo", "Promo Total", "Hijab Instan", "", "Subtotalan"):
            self.assertIsNone(f(s), s)

    def test_label_total_tidak_biasa_tidak_dihitung_dua_kali(self):
        for label in ("Total of 2 campaigns", "Totals", "Total Akun", "Total Account", "Total for all ads",
                      "Grand Totals", "Jumlah Semua Iklan", "Overall"):
            with self.subTest(label=label):
                p = self.tulis("t.csv", KOLOM_SEDERHANA + "Promo A,300000,20000,300,10\n"
                               f"Promo B,200000,16000,200,5\n{label},500001,36000,500,15\n")
                d = self.json_ok("analisis", str(p))
                self.assertEqual(d["total"]["biaya"], 500000, label)
                self.assertEqual(d["baris_dilewati_baris_total"], 1, label)
                self.assertNotIn(label, [k["nama"] for k in d["per_kampanye"]])

    def test_total_harian_di_kolom_tanggal_selisih_sen(self):   # K3 varian
        baris = []
        for nama, b, im, kl, kv in (("Live Payday", 150000, 12000, 250, "-"), ("Katalog", 200000, 15000, 330, 5),
                                    ("Video", 107100, 8000, 160, 2)):
            baris += [f"2026-09-{14 + i},{nama},{b},{im},{kl},{kv}" for i in range(7)]
        teks = ("By Day,Campaign name,Cost,Impressions,Clicks (destination),Conversions\n" + "\n".join(baris)
                + "\nTotal of 3 campaigns,,3199700.01,245000,5180,49\n")
        d = self.json_ok("analisis", str(self.tulis("tt.csv", teks)))
        self.assertEqual(d["total"]["biaya"], 3199700)
        self.assertEqual(d["total"]["hasil"], 49)
        self.assertEqual(d["periode"]["label"], "2026-09-14 s.d. 2026-09-20")
        self.assertFalse(any("tidak terbaca" in x for x in d["peringatan"]))

    def test_pengaman_silang_label_asing_semua_angka_hampir_sama(self):
        p = self.tulis("s.csv", KOLOM_SEDERHANA + "Promo A,300000,20000,300,10\nPromo B,200000,16000,200,5\n"
                                "Promo C,150000,9000,120,3\nΣ semua,650001,45000,620,18\n")
        d = self.json_ok("analisis", str(p))
        self.assertEqual(d["total"]["biaya"], 650000)
        self.assertTrue(any("Σ semua" in x and "baris TOTAL" in x for x in d["peringatan"]))
        self.assertIn("PERLU DICEK", d["teks"])

    def test_pengaman_silang_hanya_biaya_sama_diberi_peringatan_tanpa_dibuang(self):
        p = self.tulis("s.csv", KOLOM_SEDERHANA + "Promo A,300000,20000,300,10\nPromo B,200000,16000,200,5\n"
                                "Rekap Mingguan,500000,90000,1400,15\n")
        d = self.json_ok("analisis", str(p))
        self.assertEqual(d["total"]["biaya"], 1000000)          # tidak dibuang diam-diam
        w = [x for x in d["peringatan"] if "terjumlah dua kali" in x]
        self.assertEqual(len(w), 1)
        self.assertIn("Rekap Mingguan", w[0])
        self.assertIn("seharusnya Rp 500.000, bukan Rp 1.000.000", w[0])

    def test_nama_berawalan_total_anggaran_bulat_tidak_dibuang(self):
        p = self.tulis("s.csv", KOLOM_SEDERHANA + "Total Look Hijab,100000,9000,150,4\n"
                                "Promo A,50000,3000,40,1\nPromo B,50000,2500,35,1\n")
        d = self.json_ok("analisis", str(p))
        self.assertEqual(d["total"]["biaya"], 200000)
        self.assertEqual(d["baris_dilewati_baris_total"], 0)
        self.assertTrue(any("Total Look Hijab" in x and "terjumlah dua kali" in x for x in d["peringatan"]))

    def test_label_sedang_angka_tidak_cocok_diberi_peringatan(self):
        p = self.tulis("s.csv", KOLOM_SEDERHANA + "Promo A,300000,20000,300,10\nPromo B,200000,16000,200,5\n"
                                "Total Produk,70000,5000,60,2\n")
        d = self.json_ok("analisis", str(p))
        self.assertEqual(d["total"]["biaya"], 500000)
        self.assertTrue(any("Total Produk" in x and "ganti namanya" in x for x in d["peringatan"]))

    def test_kampanye_dominan_tidak_diberi_peringatan_palsu(self):
        p = self.tulis("s.csv", KOLOM_SEDERHANA + "Utama,900000,60000,900,30\nPromo A,500000,20000,300,10\n"
                                "Promo B,500000,16000,200,5\n")
        d = self.json_ok("analisis", str(p))
        self.assertEqual(d["total"]["biaya"], 1900000)
        self.assertEqual(d["peringatan"], [])


class UjiM1LabelTotalAngkaBukanCakupan(unittest.TestCase):
    """v1.0.3 (M1, examples/07-uji-ulang-v1.0.2.md P5/P7/P7b): nama kampanye ASLI berawalan
    'Total'/'Jumlah' + angka + kata BUKAN cakupan (mis. '12.12 Flash Sale', '2 Pcs Bundling')
    tidak boleh dibuang diam-diam sebagai baris total. Setiap baris yang TETAP dibuang sebagai
    total (label kuat/sedang) sekarang HARUS selalu memberi ⚠️ menyebut nama & biayanya."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def tulis(self, nama, isi):
        p = self.dir / nama
        p.write_text(isi, encoding="utf-8")
        return p

    def json_ok(self, *args):
        kode, keluar, galat = jalankan(*args, "--json", cwd=self.dir)
        self.assertEqual(kode, 0, galat)
        return json.loads(keluar)

    def test_jenis_label_total_angka_diikuti_kata_bukan_cakupan_jadi_lemah(self):
        # Root cause M1: dulu sisa yang DIAWALI ANGKA langsung "kuat" tanpa mengecek kata
        # sesudahnya. "Total 4 kampanye" (angka + kata cakupan) tetap "kuat"; "Total 12.12 Flash
        # Sale" / "Jumlah 2 Pcs Bundling" (angka + kata BUKAN cakupan) sekarang harus "lemah".
        f = modul.jenis_label_total
        self.assertEqual(f("Total 4 kampanye"), "kuat")
        self.assertEqual(f("Total (5 iklan)"), "kuat")
        self.assertEqual(f("Total 12.12 Flash Sale"), "lemah")
        self.assertEqual(f("Jumlah 2 Pcs Bundling"), "lemah")
        self.assertEqual(f("Total Look Hijab"), "lemah")   # regresi: tidak boleh berubah

    def test_p5_dua_kampanye_asli_berawalan_total_jumlah_angka_tidak_dibuang(self):
        # Persis skenario P5 di examples/07-uji-ulang-v1.0.2.md (tanpa baris total sungguhan).
        p = self.tulis("p5.csv", KOLOM_SEDERHANA +
                       "Total 12.12 Flash Sale,600000,40000,600,20\n"
                       "Jumlah 2 Pcs Bundling,250000,15000,250,7\n"
                       "Promo Reguler,150000,9000,150,4\n")
        d = self.json_ok("analisis", str(p))
        self.assertEqual(d["baris_dilewati_baris_total"], 0)
        self.assertEqual(d["total"]["biaya"], 1_000_000)   # BUKAN Rp 150.000 seperti bug v1.0.2
        nama = {k["nama"] for k in d["per_kampanye"]}
        self.assertIn("Total 12.12 Flash Sale", nama)
        self.assertIn("Jumlah 2 Pcs Bundling", nama)
        # Verifikasi independen pakai Decimal, bukan cuma percaya angka skill.
        self.assertEqual(Decimal(600000) + Decimal(250000) + Decimal(150000), Decimal(d["total"]["biaya"]))

    def test_p4_nama_look_hijab_dan_variasi_tidak_dibuang(self):
        # P4: kampanye bernama "Total Look Hijab"/"Jumlah Terbatas - Khimar" dll (kata biasa
        # sesudah Total/Jumlah, TANPA angka) - regresi, harus tetap seperti v1.0.2.
        p = self.tulis("p4.csv", KOLOM_SEDERHANA +
                       "Total Look Hijab,400000,20000,300,10\n"
                       "Jumlah Terbatas Khimar,350000,18000,280,9\n"
                       "Totalitas Gamis,150000,9000,150,4\n"
                       "Total Diskon Bergo,100000,6000,90,3\n")
        d = self.json_ok("analisis", str(p))
        self.assertEqual(d["baris_dilewati_baris_total"], 0)
        self.assertEqual(d["total"]["biaya"], 1_000_000)

    def test_label_kuat_dibuang_selalu_diberi_peringatan_cocok(self):
        # "Total 4 kampanye" TETAP dibuang (label kuat, angka+kata cakupan) - tapi sekarang HARUS
        # selalu ada ⚠️ menyebut namanya & biayanya, walau angkanya COCOK dengan jumlah baris lain
        # (sebelum v1.0.3, label "kuat" yang cocok tidak pernah diberi ⚠️ sama sekali).
        p = self.tulis("kuat_cocok.csv", KOLOM_SEDERHANA +
                       "Promo A,300000,20000,300,10\nPromo B,200000,16000,200,5\n"
                       "Total 4 kampanye,500000,36000,500,15\n")
        d = self.json_ok("analisis", str(p))
        self.assertEqual(d["baris_dilewati_baris_total"], 1)
        self.assertEqual(d["total"]["biaya"], 500000)
        self.assertTrue(any("Total 4 kampanye" in x and "Rp 500.000" in x for x in d["peringatan"]))

    def test_label_kuat_dibuang_selalu_diberi_peringatan_tidak_cocok(self):
        # Label kuat ("Total") yang biayanya JAUH dari jumlah baris lain - sebelum v1.0.3 dibuang
        # 100% diam-diam tanpa ⚠️ sama sekali (celah M1 untuk label kuat, beda dari sedang).
        p = self.tulis("kuat_beda.csv", KOLOM_SEDERHANA +
                       "Promo A,300000,20000,300,10\nPromo B,200000,16000,200,5\n"
                       "Total,999999,80000,900,30\n")
        d = self.json_ok("analisis", str(p))
        self.assertEqual(d["baris_dilewati_baris_total"], 1)
        self.assertEqual(d["total"]["biaya"], 500000)
        w = [x for x in d["peringatan"] if "Total" in x and "tidak sama dengan jumlah baris lain" in x]
        self.assertEqual(len(w), 1)
        self.assertIn("Rp 999.999", w[0])
        self.assertIn("Rp 500.000", w[0])


def _jumlah_biaya(baris_csv, kecuali=()):
    """Hitung ulang total biaya secara independen (Decimal) dari baris CSV sederhana
    'nama,biaya,...' - baris yang namanya ada di `kecuali` tidak dijumlah."""
    tot = Decimal(0)
    for b in baris_csv.strip().splitlines():
        sel = next(csv.reader([b]))
        if sel[0] not in kecuali:
            tot += Decimal(sel[1])
    return tot


class UjiV103KasusM1M2M3(_Dasar):
    """v1.0.3: baris hanya dianggap total bila label ringkasan murni, lolos cek silang ±2%,
    dan/atau kolom nama kosong + cocok dengan tetangganya. Setiap baris yang dikecualikan
    SELALU diberi ⚠️ berisi nama/label + biayanya. Total diverifikasi ulang dengan Decimal."""

    def cek_total(self, d, data, kecuali=()):
        self.assertEqual(Decimal(str(d["total"]["biaya"])), _jumlah_biaya(data, kecuali))

    def test_label_sisa_hanya_angka_jadi_lemah(self):
        f = modul.jenis_label_total
        for s in ("Total 12.12", "Jumlah 2", "Total (3)", "Total: 2026", "Total 12.12 Flash Sale",
                  "Total: Flash Sale Ramadan", "Jumlah 2 Pcs Bundling"):
            self.assertEqual(f(s), "lemah", s)
        for s in ("Total", "Total:", "Total 4 kampanye", "Total (5 iklan)", "Total: Account", "Totals"):
            self.assertIn(f(s), ("kuat", "sedang"), s)

    def test_nama_total_angka_saja_dihitung(self):
        data = ("Total 12.12,400000,30000,400,12\nJumlah 2,100000,5000,90,3\n"
                "Promo Gajian,250000,12000,200,6\n")
        d = self.json_ok("analisis", str(self.tulis("a.csv", KOLOM_SEDERHANA + data)))
        self.assertEqual(d["baris_dilewati_baris_total"], 0)
        self.cek_total(d, data)

    def test_p5_ditambah_baris_total_asli_hanya_total_asli_yang_dibuang(self):
        data = ("Total 12.12 Flash Sale,600000,40000,600,20\nJumlah 2 Pcs Bundling,250000,15000,250,7\n"
                "Promo Reguler,150000,9000,150,4\nTotal,1000000,64000,1000,31\n")
        d = self.json_ok("analisis", str(self.tulis("p5b.csv", KOLOM_SEDERHANA + data)))
        self.assertEqual(d["baris_dilewati_baris_total"], 1)
        self.cek_total(d, data, kecuali=("Total",))
        self.assertEqual(Decimal(d["total"]["biaya"]), Decimal("1000000"))
        self.assertTrue(any("'Total'" in x and "Rp 1.000.000" in x for x in d["peringatan"]))

    def test_nama_total_angka_yang_lolos_cek_silang_dibuang_dengan_peringatan(self):
        # Satu-satunya jalan nama "Total 12.12 ..." dibuang: angkanya ≈ jumlah baris lain (±2%).
        data = ("Promo A,300000,20000,300,10\nPromo B,200000,16000,200,5\n"
                "Total 12.12 Flash Sale,505000,36300,505,15\n")
        d = self.json_ok("analisis", str(self.tulis("c.csv", KOLOM_SEDERHANA + data)))
        self.assertEqual(d["baris_dilewati_baris_total"], 1)
        self.cek_total(d, data, kecuali=("Total 12.12 Flash Sale",))
        self.assertTrue(any("Total 12.12 Flash Sale" in x and "Rp 505.000" in x and "baris TOTAL" in x
                            for x in d["peringatan"]))

    def test_label_total_di_kolom_lain_nama_terisi_tetap_dihitung(self):
        teks = ("Campaign name,Keterangan,Cost,Impressions,Clicks,Conversions\n"
                "Promo Gajian,Total,300000,20000,300,10\nPromo B,,200000,16000,200,5\n"
                "Promo C,,100000,5000,80,2\n")
        d = self.json_ok("analisis", str(self.tulis("k.csv", teks)))
        self.assertEqual(d["baris_dilewati_baris_total"], 0)
        self.assertEqual(Decimal(d["total"]["biaya"]), Decimal(300000) + Decimal(200000) + Decimal(100000))

    def test_setiap_baris_dibuang_selalu_ada_peringatan_nama_dan_biaya(self):
        # P2: 'Totals' +1,5% -> dibuang (label ringkasan murni) tapi tetap ⚠️ nama + biaya.
        data = "Promo A,500000,30000,500,14\nPromo B,300000,20000,300,10\nTotals,812000,50000,800,24\n"
        d = self.json_ok("analisis", str(self.tulis("p2.csv", KOLOM_SEDERHANA + data)))
        self.assertEqual(d["baris_dilewati_baris_total"], 1)
        self.cek_total(d, data, kecuali=("Totals",))
        self.assertTrue(any("'Totals'" in x and "Rp 812.000" in x for x in d["peringatan"]))
        self.assertIn("PERLU DICEK", d["teks"])

    def test_m2_label_asing_selisih_3_persen_diberi_peringatan(self):
        data = ("Promo A,300000,20000,300,10\nPromo B,200000,16000,200,5\n"
                "Akun Toko Berkah,515000,37080,515,15\n")
        d = self.json_ok("analisis", str(self.tulis("p7.csv", KOLOM_SEDERHANA + data)))
        self.cek_total(d, data)                                     # tidak dibuang diam-diam
        w = [x for x in d["peringatan"] if "terjumlah dua kali" in x]
        self.assertEqual(len(w), 1)
        self.assertIn("Akun Toko Berkah", w[0])
        self.assertIn("Rp 515.000", w[0])

    def test_m2_selisih_10_persen_tanpa_peringatan_palsu(self):
        data = "Utama,900000,60000,900,30\nPromo A,500000,20000,300,10\nPromo B,500000,16000,200,5\n"
        d = self.json_ok("analisis", str(self.tulis("u.csv", KOLOM_SEDERHANA + data)))
        self.cek_total(d, data)
        self.assertEqual(d["peringatan"], [])

    P8B = ("Campaign name,Ad name,Cost,Impressions,Clicks,Conversions\n"
           "Grand Total,,550000,30000,500,17\n"
           "Kamp A,Iklan 1,200000,10000,200,6\nKamp A,Iklan 2,100000,6000,100,3\n"
           "Subtotal Kamp A,,300000,16000,300,9\n"
           "Kamp B,Iklan 3,250000,14000,200,8\n"
           "Subtotal Kamp B,,250000,14000,200,8\n")

    def test_m3_subtotal_tanpa_titik_dua_cocok_tetangga_dibuang(self):
        d = self.json_ok("analisis", str(self.tulis("p8b.csv", self.P8B)))
        self.assertEqual(d["baris_dilewati_baris_total"], 3)
        self.assertEqual(Decimal(d["total"]["biaya"]), Decimal(200000) + Decimal(100000) + Decimal(250000))
        self.assertEqual(d["total"]["hasil"], 17)
        self.assertFalse(any(k["nama"].startswith("(tanpa nama") for k in d["per_kampanye"]))
        for lbl, rp in (("Subtotal Kamp A", "Rp 300.000"), ("Subtotal Kamp B", "Rp 250.000")):
            self.assertTrue(any(lbl in x and rp in x and "SUBTOTAL" in x for x in d["peringatan"]), lbl)
        self.assertTrue(any("'Grand Total'" in x and "Rp 550.000" in x for x in d["peringatan"]))

    def test_m3_label_nama_kosong_angka_tidak_cocok_tetap_dihitung_dengan_peringatan(self):
        teks = ("Campaign name,Ad name,Cost,Impressions,Clicks,Conversions\n"
                "Kamp A,Iklan 1,200000,10000,200,6\nKamp A,Iklan 2,100000,6000,100,3\n"
                "Total 12.12 Flash Sale,,90000,4000,70,2\n")
        d = self.json_ok("analisis", str(self.tulis("m3.csv", teks)))
        self.assertEqual(d["baris_dilewati_baris_total"], 0)
        self.assertEqual(Decimal(d["total"]["biaya"]), Decimal(200000) + Decimal(100000) + Decimal(90000))
        self.assertTrue(any("Total 12.12 Flash Sale" in x and "TETAP dihitung" in x and "Rp 90.000" in x
                            for x in d["peringatan"]))


class UjiV104SubtotalDiKolomNama(_Dasar):
    """v1.0.4 (N3, examples/08-uji-ulang-v103-akun-b.md): subtotal buatan admin DI KOLOM NAMA yang
    memuat nama kampanye tidak boleh terhitung dua kali; setiap baris yang dikecualikan diberi ⚠️
    nama + biaya; kampanye sungguhan tidak pernah dibuang diam-diam. Total dicek ulang dengan Decimal."""

    def cek_total(self, d, data, kecuali=()):
        self.assertEqual(Decimal(str(d["total"]["biaya"])), _jumlah_biaya(data, kecuali))

    def test_fungsi_pengenal_subtotal(self):
        f = modul.awalan_subtotal
        self.assertEqual(f("Subtotal: Retarget Video"), "retarget video")
        self.assertEqual(f("Sub total - Retarget Video"), "retarget video")
        self.assertEqual(f("SUB-TOTAL Retarget Video"), "retarget video")
        self.assertEqual(f("Jumlah sementara"), "")
        for s in ("Subtotalan Promo", "Retarget Video", "Total Look Hijab", "Jumlah 2 Pcs Bundling"):
            self.assertIsNone(f(s), s)
        g = modul.nama_subtotal_dari
        self.assertTrue(g("Retarget Video Total", "Retarget Video"))
        self.assertTrue(g("Total: Retarget Video", "Retarget Video"))
        self.assertFalse(g("Retarget Video Baru", "Retarget Video"))
        self.assertFalse(g("Retarget Video", "Retarget Video"))

    def test_repro_kecil_n3_subtotal_nama_kampanye_tidak_dobel(self):
        # Repro kecil di examples/08: dulu Rp 294.240 tanpa ⚠️, seharusnya Rp 202.120.
        data = ("Retarget Video,50000,4000,60,2\nRetarget Video,42120,3500,55,1\n"
                "Subtotal: Retarget Video,92120,7500,115,3\n"
                "Promo A,60000,5000,70,2\nPromo B,50000,4000,50,1\n")
        d = self.json_ok("analisis", str(self.tulis("n3.csv", KOLOM_SEDERHANA + data)))
        self.cek_total(d, data, kecuali=("Subtotal: Retarget Video",))
        self.assertEqual(Decimal(d["total"]["biaya"]), Decimal("202120"))
        self.assertEqual(d["baris_dilewati_baris_total"], 1)
        self.assertNotIn("Subtotal: Retarget Video", [k["nama"] for k in d["per_kampanye"]])
        self.assertTrue(any("'Subtotal: Retarget Video'" in x and "Rp 92.120" in x for x in d["peringatan"]))

    def test_variasi_label_subtotal_dikecualikan_dengan_peringatan(self):
        for lbl in ("Sub total - Retarget Video", "Sub-total Retarget Video", "SUBTOTAL: retarget video",
                    "Jumlah sementara", "Retarget Video Total", "Total: Retarget Video",
                    "Jumlah Retarget Video"):
            with self.subTest(label=lbl):
                data = ("Retarget Video,50000,4000,60,2\nRetarget Video,42120,3500,55,1\n"
                        f"{lbl},92120,7500,115,3\nPromo A,60000,5000,70,2\nPromo B,50000,4000,50,1\n")
                d = self.json_ok("analisis", str(self.tulis("v.csv", KOLOM_SEDERHANA + data)))
                self.cek_total(d, data, kecuali=(lbl,))
                self.assertEqual(d["baris_dilewati_baris_total"], 1)
                self.assertTrue(any(f"'{lbl}'" in x and "Rp 92.120" in x for x in d["peringatan"]))

    def test_file_04_tiktok_harian_subtotal_per_kampanye_dan_total(self):
        # Pola file 04 examples/08: baris harian, "Subtotal: <kampanye>" tanpa tanggal di tengah,
        # "Subtotal" polos, lalu "Total of 3 campaigns" (+Rp 1). Semua subtotal/total dikecualikan.
        baris, kunci = [], Decimal(0)
        for nama, b, im, kl, kv in (("Retarget Video", "25000.25", 3000, 40, 1),
                                    ("Katalog Hijab", "30000", 3500, 50, 2),
                                    ("Live Payday", "30333", 2800, 35, 1)):
            for i in range(7):
                baris.append(f"2026-09-{14 + i},{nama},{b},{im},{kl},{kv}")
                kunci += Decimal(b)
            baris.append(f",Subtotal: {nama},{Decimal(b) * 7},{im * 7},{kl * 7},{kv * 7}")
        baris.append(f",Subtotal,{kunci},64400,875,28")
        baris.append(f"Total of 3 campaigns,,{kunci + 1},64400,875,28")
        teks = "By Day,Campaign name,Cost,Impressions,Clicks (destination),Conversions\n" + "\n".join(baris) + "\n"
        d = self.json_ok("analisis", str(self.tulis("f04.csv", teks)))
        self.assertEqual(Decimal(str(d["total"]["biaya"])), kunci)   # 597.332,75 (Decimal)
        self.assertEqual(d["total"]["hasil"], 28)
        self.assertEqual(d["jumlah_kampanye"], 3)
        self.assertFalse(any(k["nama"].lower().startswith("subtotal") for k in d["per_kampanye"]))
        for nama, rp in (("Retarget Video", "Rp 175.002"), ("Katalog Hijab", "Rp 210.000"),
                         ("Live Payday", "Rp 212.331")):
            self.assertTrue(any(f"'Subtotal: {nama}'" in x and rp in x for x in d["peringatan"]), nama)
        self.assertEqual(d["periode"]["label"], "2026-09-14 s.d. 2026-09-20")

    def test_nama_mirip_subtotal_angka_tidak_cocok_tetap_dihitung(self):
        data = ("Retarget Video,50000,4000,60,2\nRetarget Video,42120,3500,55,1\n"
                "Retarget Video Total,30000,2000,20,1\nPromo A,60000,5000,70,2\n")
        d = self.json_ok("analisis", str(self.tulis("m.csv", KOLOM_SEDERHANA + data)))
        self.cek_total(d, data)                                  # tidak dibuang
        self.assertEqual(d["baris_dilewati_baris_total"], 0)
        self.assertTrue(any("Retarget Video Total" in x and "TETAP dihitung" in x and "Rp 30.000" in x
                            for x in d["peringatan"]))

    def test_awalan_subtotal_angka_tidak_cocok_tetap_ada_peringatan(self):
        data = ("Promo A,60000,5000,70,2\nPromo B,50000,4000,50,1\nSubtotal: Promo Lama,12345,900,10,0\n")
        d = self.json_ok("analisis", str(self.tulis("s.csv", KOLOM_SEDERHANA + data)))
        self.cek_total(d, data, kecuali=("Subtotal: Promo Lama",))
        self.assertTrue(any("'Subtotal: Promo Lama'" in x and "Rp 12.345" in x and "tidak cocok" in x
                            for x in d["peringatan"]))

    def test_baris_harian_asli_yang_kebetulan_sama_dengan_jumlah_tidak_dibuang(self):
        # Hari ke-3 = hari 1 + hari 2 (biaya, tayangan, klik) tetapi BERTANGGAL -> data asli, dihitung.
        teks = ("Date,Campaign name,Cost,Impressions,Clicks,Conversions\n"
                "2026-09-14,Retarget Video,100000,5000,50,2\n2026-09-15,Retarget Video,100000,5000,50,2\n"
                "2026-09-16,Retarget Video,200000,10000,100,4\n2026-09-16,Promo A,80000,4000,30,1\n")
        d = self.json_ok("analisis", str(self.tulis("h.csv", teks)))
        self.assertEqual(Decimal(d["total"]["biaya"]), Decimal(480000))
        self.assertEqual(d["baris_dilewati_baris_total"], 0)
        self.assertFalse(any("subtotal" in x.lower() for x in d["peringatan"]))

    def test_nama_sama_tanpa_tanggal_cocok_semua_metrik_dikecualikan(self):
        teks = ("Date,Campaign name,Cost,Impressions,Clicks,Conversions\n"
                "2026-09-14,Retarget Video,100000,5000,50,2\n2026-09-15,Retarget Video,120000,6000,55,2\n"
                ",Retarget Video,220000,11000,105,4\n2026-09-15,Promo A,80000,4000,30,1\n")
        d = self.json_ok("analisis", str(self.tulis("t.csv", teks)))
        self.assertEqual(Decimal(d["total"]["biaya"]), Decimal(100000) + Decimal(120000) + Decimal(80000))
        self.assertEqual(d["baris_dilewati_baris_total"], 1)
        self.assertTrue(any("'Retarget Video'" in x and "Rp 220.000" in x and "subtotal" in x
                            for x in d["peringatan"]))

    def test_peringatan_m2_bahasa_sopan_tanpa_huruf_kapital_menakutkan(self):
        data = "Promo A,300000,20000,300,10\nPromo B,200000,16000,200,5\nRekap Mingguan,500000,90000,1400,15\n"
        d = self.json_ok("analisis", str(self.tulis("m2.csv", KOLOM_SEDERHANA + data)))
        w = [x for x in d["peringatan"] if "terjumlah dua kali" in x]
        self.assertEqual(len(w), 1)
        self.assertNotIn("TERHITUNG DUA KALI", w[0])
        self.assertIn("Mohon", w[0])


class UjiV106TotalKampanyeTanpaLabel(_Dasar):
    """v1.0.6: baris total kampanye dengan kolom grup iklan kosong (tanpa label) tidak terhitung diam-diam."""

    def test_total_kampanye_cocok_dibuang_dengan_peringatan(self):
        teks = ("Campaign,Ad group,Cost,Impressions,Clicks,Conversions\n"
                "Search Brand,Merek,400000,20000,600,10\n"
                "Search Brand,Umum,300000,10000,300,5\n"
                "Search Brand,,700000,30000,900,15\n"
                "Search Lain,Kata,250000,8000,200,3\n")
        d = self.json_ok("analisis", str(self.tulis("t1.csv", teks)))
        self.assertEqual(Decimal(str(d["total"]["biaya"])), Decimal(950000))
        w = [x for x in d["peringatan"] if "tanpa grup iklan" in x and "Search Brand" in x]
        self.assertEqual(len(w), 1, d["peringatan"])
        self.assertIn("tidak dihitung", w[0])
        self.assertIn("Rp 700.000", w[0])

    def test_baris_kosong_tidak_cocok_tetap_dihitung_dengan_peringatan(self):
        teks = ("Campaign,Ad group,Cost,Impressions,Clicks,Conversions\n"
                "Search Brand,Merek,400000,20000,600,10\n"
                "Search Brand,Umum,300000,10000,300,5\n"
                "Search Brand,,50000,2000,40,1\n")
        d = self.json_ok("analisis", str(self.tulis("t2.csv", teks)))
        self.assertEqual(Decimal(str(d["total"]["biaya"])), Decimal(750000))
        self.assertTrue(any("tetap dihitung" in x and "Search Brand" in x for x in d["peringatan"]), d["peringatan"])

    def test_pmax_tanpa_saudara_tidak_diperingatkan(self):
        teks = ("Campaign,Ad group,Cost,Impressions,Clicks,Conversions\n"
                "Search Brand,Merek,120000,8000,300,6\n"
                "PMax Toko,,250000,96340,1702,41\n")
        d = self.json_ok("analisis", str(self.tulis("t3.csv", teks)))
        self.assertEqual(Decimal(str(d["total"]["biaya"])), Decimal(370000))
        self.assertFalse(any("tanpa grup iklan" in x and "tetap dihitung" in x or "total kampanye" in x
                             for x in d["peringatan"]), d["peringatan"])


class UjiV105NamaPMaxDanTotalAlternatif(_Dasar):
    """v1.0.5 (P-3, P-4 uji ulang v1.0.4): baris Google Performance Max tanpa grup iklan memakai nama
    grup aset/kampanye; ⚠️ subtotal/total yang meragukan menyebut total alternatif (Decimal)."""

    def test_p3_pmax_tanpa_ad_group_pakai_nama_kampanye(self):
        teks = ("Campaign,Ad group,Cost,Impressions,Clicks,Conversions\n"
                "Search Brand,Kata Kunci Merek,120000,8000,300,6\n"
                "Search Brand,Kata Kunci Umum,80000,6000,150,2\n"
                "PMax - Semua Produk,,250000,96340,1702,41\n"
                "PMax - Semua Produk,,50000,20000,300,5\n")
        d = self.json_ok("analisis", str(self.tulis("pmax.csv", teks)))
        nama = [k["nama"] for k in d["per_kampanye"]]
        self.assertFalse(any(n.startswith("(tanpa nama") for n in nama), nama)
        self.assertIn("PMax - Semua Produk (tanpa grup iklan)", nama)
        pm = next(k for k in d["per_kampanye"] if k["nama"].startswith("PMax"))
        self.assertEqual(Decimal(str(pm["biaya"])), Decimal(300000))          # 2 baris digabung
        self.assertEqual(Decimal(str(d["total"]["biaya"])), Decimal(500000))
        self.assertEqual(d["level_rincian"], "grup iklan")

    def test_p3_pakai_kolom_asset_group_bila_ada(self):
        teks = ("Campaign,Ad group,Asset group,Cost,Impressions,Clicks,Conversions\n"
                "Search Brand,Kata Kunci Merek,,120000,8000,300,6\n"
                "PMax Toko,,Grup Aset Hijab,90000,30000,500,9\n"
                "PMax Toko,,Grup Aset Gamis,60000,25000,400,4\n")
        d = self.json_ok("analisis", str(self.tulis("aset.csv", teks)))
        nama = [k["nama"] for k in d["per_kampanye"]]
        self.assertIn("Grup Aset Hijab", nama)
        self.assertIn("Grup Aset Gamis", nama)
        self.assertEqual(Decimal(str(d["total"]["biaya"])), Decimal(270000))

    def test_p4_subtotal_tidak_cocok_sebut_total_alternatif(self):
        # dikecualikan: total 110.000; bila dihitung 110.000 + 12.345 = 122.345
        data = "Promo A,60000,5000,70,2\nPromo B,50000,4000,50,1\nSubtotal: Promo Lama,12345,900,10,0\n"
        d = self.json_ok("analisis", str(self.tulis("s.csv", KOLOM_SEDERHANA + data)))
        w = next(x for x in d["peringatan"] if "'Subtotal: Promo Lama'" in x)
        self.assertIn("sekarang Rp 110.000", w)
        self.assertIn("totalnya menjadi Rp 122.345", w)

    def test_p4_mirip_subtotal_tetap_dihitung_sebut_total_alternatif(self):
        # dihitung: 50.000 + 42.120 + 30.000 + 60.000 = 182.120; tanpa baris itu 152.120
        data = ("Retarget Video,50000,4000,60,2\nRetarget Video,42120,3500,55,1\n"
                "Retarget Video Total,30000,2000,20,1\nPromo A,60000,5000,70,2\n")
        d = self.json_ok("analisis", str(self.tulis("m.csv", KOLOM_SEDERHANA + data)))
        self.assertEqual(Decimal(str(d["total"]["biaya"])), Decimal(182120))
        w = next(x for x in d["peringatan"] if "Retarget Video Total" in x and "TETAP dihitung" in x)
        self.assertIn("sekarang Rp 182.120", w)
        self.assertIn("totalnya menjadi Rp 152.120", w)


class UjiV1010TujuanKampanye(_Dasar):
    """v1.0.10 (uji OpenClaw 2026-10-01): kampanye Traffic/Awareness tanpa pesan WA tidak disarankan
    dimatikan; dinilai dari klik/tayangan. (v1.0.12: baris "Kolom dibaca" tidak lagi ikut teks laporan;
    hanya muncul bila --tampilkan-kolom dipakai, lihat UjiV1012BotTelegram.)"""

    META = ("Reporting starts,Reporting ends,Ad name,Results,Result indicator,Impressions,Amount spent (IDR),Link clicks\n"
            "2026-09-21,2026-09-27,WA - Promo Gamis,64,actions:onsite_conversion.messaging_conversation_started_7d,150000,1250000,2100\n"
            "2026-09-21,2026-09-27,WA - Retarget,38,actions:onsite_conversion.messaging_conversation_started_7d,60000,600000,900\n"
            "2026-09-21,2026-09-27,WA - Hijab Baru,12,actions:onsite_conversion.messaging_conversation_started_7d,80000,1100000,1000\n"
            "2026-09-21,2026-09-27,Katalog IG Oktober,,actions:link_click,145500,850000,2000\n"
            "2026-09-21,2026-09-27,Video Reels Brand,,reach,100000,400000,400\n")

    def test_kolom_tujuan_traffic_reach_tidak_disarankan_matikan(self):
        d = self.json_ok("analisis", str(self.tulis("meta.csv", self.META)), "--nama-hasil", "pesan WA")
        beda = {k["nama"]: k["tujuan_lain"] for k in d["tujuan_berbeda"]}
        self.assertEqual(beda, {"Katalog IG Oktober": "Traffic", "Video Reels Brand": "Reach"})
        terburuk = [k["nama"] for k in d["tiga_terburuk"]]
        self.assertNotIn("Katalog IG Oktober", terburuk)
        self.assertFalse(any("Katalog IG" in x or "Video Reels" in x for x in d["saran"]), d["saran"])
        # total tetap memuat semua belanja; catatan memberi biaya per pesan khusus kampanye pesan
        self.assertEqual(Decimal(str(d["total"]["biaya"])), Decimal(4200000))
        self.assertTrue(any("Rp 25.877" in c for c in d["catatan"]), d["catatan"])   # 2.950.000 / 114
        teks = d["teks"]
        self.assertIn("TUJUAN BERBEDA", teks)
        self.assertIn("CPC Rp 425", teks)                                               # 850.000 / 2.000
        self.assertNotIn("Kolom dibaca", teks)      # v1.0.12: tidak ikut laporan untuk pembeli
        self.assertEqual(d["kolom_dipakai"]["tujuan"], "Result indicator")   # tetap ada di JSON

    def test_nama_kampanye_tanpa_kolom_tujuan(self):
        data = ("WA Promo,500000,40000,600,20\nTraffic - Katalog,300000,50000,900,0\n"
                "Awareness Reels,200000,80000,100,0\nWA Lama Boros,250000,10000,90,0\n")
        d = self.json_ok("analisis", str(self.tulis("n.csv", KOLOM_SEDERHANA + data)))
        self.assertEqual({k["nama"] for k in d["tujuan_berbeda"]}, {"Traffic - Katalog", "Awareness Reels"})
        self.assertTrue(any("WA Lama Boros" in x and "hentikan" in x for x in d["saran"]), d["saran"])
        self.assertFalse(any("Traffic - Katalog" in x for x in d["saran"]), d["saran"])

    def test_kolom_tujuan_pesan_mengalahkan_nama(self):
        teks = ("Campaign name,Objective,Cost,Impressions,Clicks,Conversions\n"
                "Traffic WA Promo,OUTCOME_ENGAGEMENT_MESSAGES,300000,50000,900,0\n"
                "WA Utama,Messages,500000,40000,600,20\n")
        d = self.json_ok("analisis", str(self.tulis("o.csv", teks)))
        # Sel tujuan menyebut pesan (Meta ODAX: Engagement + Messages) -> tetap kampanye pesan,
        # walau namanya memuat "Traffic"; 0 hasil -> tetap disarankan ditinjau.
        self.assertEqual(d["tujuan_berbeda"], [])
        self.assertTrue(any("Traffic WA Promo" in x and "hentikan" in x for x in d["saran"]), d["saran"])

    def test_tujuan_lain_dengan_hasil_tetap_dinilai_dengan_catatan(self):
        data = ("WA A,100000,10000,200,20\nWA B,100000,10000,200,20\nTraffic Katalog,300000,50000,900,2\n")
        d = self.json_ok("analisis", str(self.tulis("h.csv", KOLOM_SEDERHANA + data)))
        self.assertEqual(d["tujuan_berbeda"], [])
        self.assertTrue(any("bertujuan Traffic" in x and "CPC" in x for x in d["saran"]), d["saran"])


class UjiV1012BotTelegram(_Dasar):
    """v1.0.12 (pra-cek bot asli, konteks Telegram, skor 7,0): (1) baris teknis "Kolom dibaca: ..." sempat
    dibacakan ke pembeli, jadi tidak lagi ikut teks laporan (hanya lewat --tampilkan-kolom); kolom yang
    meragukan disebut satu kalimat awam di Catatan; (2) pesan peringatan/catatan tanpa nama opsi atau
    kata proses ("jalankan ulang", "--kolom-nama", "--mata-uang"); (3) istilah CPC/CPM/CTR/ROAS dijelaskan;
    (4) "sampel kecil" diganti bahasa awam. Skenario = uji OpenClaw 2026-10-01 (hasil = chat WA masuk)."""

    KOP = ("Reporting starts,Reporting ends,Campaign name,Result indicator,Amount spent (IDR),"
           "Impressions,Link clicks,Results\n")
    WA = "actions:onsite_conversion.messaging_conversation_started_7d"
    INI = (KOP +
           f"2026-09-21,2026-09-27,WA - Promo Gamis Oktober,{WA},1250000,150000,1900,64\n"
           f"2026-09-21,2026-09-27,WA - Retarget Pengunjung,{WA},600000,60000,900,38\n"
           "2026-09-21,2026-09-27,Traffic - Katalog IG,actions:link_click,850000,200000,2950,\n"
           f"2026-09-21,2026-09-27,WA - Hijab Instan Baru,{WA},1100000,75500,650,12\n"
           "2026-09-21,2026-09-27,Awareness - Video Reels,reach,400000,50000,0,\n")
    LALU = (KOP +
            f"2026-09-14,2026-09-20,WA - Promo Gamis Oktober,{WA},1300000,150000,1900,52\n"
            f"2026-09-14,2026-09-20,WA - Retarget Pengunjung,{WA},550000,60000,900,41\n"
            "2026-09-14,2026-09-20,Traffic - Katalog IG,actions:link_click,700000,200000,2410,\n"
            "2026-09-14,2026-09-20,Awareness - Video Reels,reach,450000,50000,0,\n")
    KATA_TERLARANG = ["kolom dibaca", "nama='", "gateway", "pairing", "script", "skrip", "python",
                      "jalankan ulang", ".py", ".json", "--", "kode keluar", "traceback"]

    def laporan(self, *tambahan):
        ini = self.tulis("ini.csv", self.INI)
        lalu = self.tulis("lalu.csv", self.LALU)
        code, out, err = jalankan("analisis", str(ini), "--sebelumnya", str(lalu), "--omzet", "18500000",
                                  "--nama-hasil", "chat WA masuk", *tambahan, cwd=self.dir)
        self.assertEqual(code, 0, err)
        return out

    def test_angka_skenario_wa_benar_dan_teks_bersih_dari_kata_teknis(self):
        out = self.laporan()
        for angka in ("Rp 4.200.000", "Chat WA masuk: 114", "CPC: Rp 656", "CPM: Rp 7.843", "CTR: 1,2%",
                      "Biaya per chat WA masuk: Rp 36.842", "22,7% dari omzet Rp 18.500.000",
                      "naik 40,0% dari minggu lalu Rp 3.000.000", "naik 22,6% dari minggu lalu 93",
                      "naik 14,2% dari minggu lalu Rp 32.258", "Rp 91.667/chat WA masuk"):
            self.assertIn(angka, out)
        bawah = out.lower()
        for kata in self.KATA_TERLARANG:
            self.assertNotIn(kata, bawah, kata)
        # istilah "chat WA masuk" hanya nama hasil; laporan tidak menawarkan menyambungkan WhatsApp
        self.assertNotIn("sambung", bawah)
        self.assertNotIn("hubungkan", bawah)

    def test_baris_kolom_dibaca_hanya_bila_diminta_teknisi(self):
        self.assertNotIn("Kolom dibaca", self.laporan())
        out = self.laporan("--tampilkan-kolom")
        baris = out.splitlines()
        self.assertTrue(baris[2].startswith("Kolom dibaca (teknis, jangan diteruskan ke pengguna): "), baris[:4])
        self.assertIn("tujuan='Result indicator'", baris[2])
        # JSON: teks mengikuti flag yang sama, pemetaan tetap tersedia sebagai data
        d = self.json_ok("analisis", str(self.tulis("ini.csv", self.INI)))
        self.assertNotIn("Kolom dibaca", d["teks"])
        self.assertEqual(d["kolom_dipakai"]["klik"], "Link clicks")
        self.assertEqual(d["kolom_meragukan"], [])

    def test_kolom_meragukan_satu_kalimat_awam_di_catatan(self):
        teks = ("Campaign name,Amount spent (IDR),Impressions,Link clicks,Clicks (all),Results\n"
                "WA A,500000,40000,600,800,20\nWA B,300000,30000,400,500,10\n")
        d = self.json_ok("analisis", str(self.tulis("m.csv", teks)), "--nama-hasil", "chat WA masuk")
        kalimat = [c for c in d["catatan"] if c.startswith("Saya membaca kolom")]
        self.assertEqual(len(kalimat), 1, d["catatan"])
        self.assertIn("'Link clicks' sebagai jumlah klik", kalimat[0])
        self.assertIn("'Clicks (all)'", kalimat[0])
        self.assertIn("kabari saya", kalimat[0])
        self.assertEqual([m["peran"] for m in d["kolom_meragukan"]], ["klik"])
        self.assertNotIn("Kolom dibaca", d["teks"])
        self.assertIn("- Saya membaca kolom 'Link clicks' sebagai jumlah klik", d["teks"])
        # angka tidak berubah oleh catatan ini: klik tetap dari 'Link clicks' (600 + 400)
        self.assertEqual(Decimal(str(d["total"]["klik"])), Decimal(1000))
        # pengguna sudah menentukan kolomnya sendiri -> tidak ditanya lagi
        d2 = self.json_ok("analisis", str(self.tulis("m.csv", teks)), "--kolom-klik", "Link clicks")
        self.assertFalse(any(c.startswith("Saya membaca kolom") for c in d2["catatan"]), d2["catatan"])

    def test_tanpa_kolom_bersaing_tidak_ada_kalimat_kolom(self):
        d = self.json_ok("analisis", str(self.tulis("ini.csv", self.INI)))
        self.assertFalse(any(c.startswith("Saya membaca kolom") for c in d["catatan"]), d["catatan"])

    def test_istilah_dijelaskan_roas_hanya_bila_ada(self):
        out = self.laporan()
        akhir = out.splitlines()[-1]
        self.assertTrue(akhir.startswith("- Arti istilah: CPC = biaya per klik; CPM = biaya per 1.000 tayangan; "
                                         "CTR = persen tayangan yang diklik"), akhir)
        self.assertNotIn("ROAS", akhir)
        teks = ("Campaign name,Amount spent (IDR),Impressions,Link clicks,Results,Purchase conversion value\n"
                "Kaos A,1000000,50000,500,25,3000000\n")
        code, out2, err = jalankan("analisis", str(self.tulis("r.csv", teks)), cwd=self.dir)
        self.assertEqual(code, 0, err)
        self.assertIn("ROAS = nilai penjualan dari iklan dibagi belanja iklan", out2.splitlines()[-1])

    def test_gabung_juga_menjelaskan_istilah(self):
        meta = self.tulis("meta.csv", "Campaign name,Amount spent (IDR),Impressions,Link clicks,Results\n"
                                      "A,1000000,50000,500,25\n")
        tiktok = self.tulis("tt.csv", "Campaign name,Cost,Impressions,Clicks (destination),Conversion\n"
                                      "B,500000,30000,300,10\n")
        berkas = []
        for src, nama in ((meta, "j1.json"), (tiktok, "j2.json")):
            code, out, err = jalankan("analisis", str(src), "--json", cwd=self.dir)
            self.assertEqual(code, 0, err)
            (self.dir / nama).write_text(out, encoding="utf-8")
            berkas.append(str(self.dir / nama))
        code, out, err = jalankan("gabung", *berkas, cwd=self.dir)
        self.assertEqual(code, 0, err)
        self.assertIn("Arti istilah: CPC = biaya per klik", out)

    def test_gabung_meneruskan_kalimat_kolom_meragukan_per_platform(self):
        meta = self.tulis("meta.csv", "Campaign name,Amount spent (IDR),Impressions,Link clicks,Clicks (all),Results\n"
                                      "A,1000000,50000,500,700,25\n")
        tiktok = self.tulis("tt.csv", "Campaign name,Cost,Impressions,Clicks (destination),Conversion\n"
                                      "B,500000,30000,300,10\n")
        berkas = []
        for src, nama in ((meta, "j1.json"), (tiktok, "j2.json")):
            code, out, err = jalankan("analisis", str(src), "--json", cwd=self.dir)
            self.assertEqual(code, 0, err)
            (self.dir / nama).write_text(out, encoding="utf-8")
            berkas.append(str(self.dir / nama))
        code, out, err = jalankan("gabung", *berkas, cwd=self.dir)
        self.assertEqual(code, 0, err)
        self.assertIn("- [Meta Ads (Facebook/Instagram)] Saya membaca kolom 'Link clicks' sebagai jumlah klik.", out)
        self.assertNotIn("Kolom dibaca", out)

    def test_peringatan_dan_catatan_pembeli_tanpa_opsi_teknis(self):
        # subtotal buatan admin -> peringatan; arahan "kirim ulang", bukan "jalankan ulang"
        data = "Promo A,60000,5000,70,2\nPromo B,50000,4000,50,1\nSubtotal: Promo Lama,12345,900,10,0\n"
        d = self.json_ok("analisis", str(self.tulis("s.csv", KOLOM_SEDERHANA + data)))
        w = next(x for x in d["peringatan"] if "'Subtotal: Promo Lama'" in x)
        self.assertIn("kirim ulang ke saya", w)
        self.assertNotIn("jalankan", w.lower())
        # biaya tak terbaca -> peringatan juga bebas kata proses
        d2 = self.json_ok("analisis", str(self.tulis("b.csv", KOLOM_SEDERHANA + "A,abc,100,10,1\nB,1000,100,10,1\n")))
        for t in d["peringatan"] + d["catatan"] + d2["peringatan"] + d2["catatan"]:
            self.assertNotIn("jalankan", t.lower(), t)
            self.assertNotIn("--", t, t)

    def test_catatan_mata_uang_ditegaskan_rupiah_tanpa_opsi_teknis(self):
        teks = "Campaign name,Amount spent (USD),Impressions,Link clicks,Results\nA,500000,40000,600,20\n"
        d = self.json_ok("analisis", str(self.tulis("u.csv", teks)), "--mata-uang", "IDR")
        self.assertTrue(any("sesuai konfirmasi Anda bahwa angkanya sudah Rupiah" in c
                            for c in d["catatan_mata_uang"]), d["catatan_mata_uang"])
        self.assertFalse(any("--" in c for c in d["catatan_mata_uang"]), d["catatan_mata_uang"])

    def test_saran_data_sedikit_bahasa_awam(self):
        data = "WA A,100000,10000,200,20\nWA B,100000,10000,200,20\nWA C,300000,50000,900,2\n"
        d = self.json_ok("analisis", str(self.tulis("k.csv", KOLOM_SEDERHANA + data)))
        saran = " ".join(d["saran"])
        self.assertIn("datanya masih sedikit", saran)
        self.assertNotIn("sampel kecil", saran)


if __name__ == "__main__":
    unittest.main(verbosity=2)
