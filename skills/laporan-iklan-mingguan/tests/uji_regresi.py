#!/usr/bin/env python3
"""Uji regresi laporan-iklan-mingguan.

Mencakup: 1 CSV contoh per platform (Meta, TikTok Ads Manager, Shopee Ads, TikTok Shop Ads,
Google Ads) dengan nama kolom resmi (lihat references/sumber-kolom.md), angka format
Indonesia & Inggris campur, baris "Total" ganda, file kosong/rusak, mata uang asing, minggu
tanpa data pembanding, dan formula injection saat ekspor CSV hasil.

Jalankan: python3 tests/uji_regresi.py   (Windows: python / py)
"""
import csv
import json
import subprocess
import sys
import tempfile
import unittest
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
        self.assertEqual(g["total"]["hasil"], 35)
        self.assertAlmostEqual(g["omzet"]["biaya_sebagai_persen_omzet"], 15.0)
        # nama hasil beda (Results vs Conversion) -> wajib ada peringatan
        self.assertTrue(any("berbeda" in p for p in g["peringatan"]))

    def test_gabung_file_bukan_json_valid_ditolak_rapi(self):
        bukan_json = self.dir / "bukan.json"
        bukan_json.write_text("ini bukan json", encoding="utf-8")
        code, out, err = jalankan("gabung", str(bukan_json), cwd=self.dir)
        self.assertEqual(code, 2)
        self.assertNotIn("Traceback", err)


if __name__ == "__main__":
    unittest.main(verbosity=2)
