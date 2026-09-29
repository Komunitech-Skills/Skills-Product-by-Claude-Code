#!/usr/bin/env python3
"""Uji regresi riset-saham-berita. Jalankan: python3 tests/uji_regresi.py  (Windows: py tests/uji_regresi.py)

Angka acuan dihitung manual di komentar (bukan disalin dari keluaran script).
"""
import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
from datetime import date
from decimal import Decimal as D

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AKAR, "scripts"))
import rasio_saham as R  # noqa: E402

HARI = date(2026, 9, 29)
KATA_TERLARANG = ("rekomendasi", "target harga", "sinyal beli", "sinyal jual", "layak beli", "saatnya beli",
                  "buy", "sell", "hold", "undervalued", "overvalued", "murah sekali")


def rasio(hasil, kode):
    return next(r for r in hasil["rasio"] if r["kode"] == kode)


def jalankan(argv):
    keluar, galat = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(keluar), contextlib.redirect_stderr(galat):
        kode = R.main(argv)
    return kode, keluar.getvalue(), galat.getvalue()


class Parsing(unittest.TestCase):
    def test_format_indonesia_dan_akhiran(self):
        kasus = {
            "Rp1,2 T": "1200000000000", "Rp 1,2 triliun": "1200000000000", "1.234,5 miliar": "1234500000000",
            "5 milyar": "5000000000", "2,5 bn": "2500000000", "3B": "3000000000",
            "12.5jt": "12500000", "12,5 juta": "12500000", "750 mn": "750000000", "10rb": "10000", "59k": "59000",
            "1.250": "1250", "Rp1.250": "1250", "Rp 49.900,-": "49900", "1.234.567": "1234567",
            "1,234,567": "1234567", "1.234.567,89": "1234567.89", "1,234,567.89": "1234567.89",
            "4,5 miliar lembar": "4500000000", "IDR 685": "685", "12.5": "12.5", "0,25": "0.25",
            "1.2 T": "1200000000000", 1250: "1250", 12.5: "12.5",
        }
        for teks, harap in kasus.items():
            with self.subTest(teks=teks):
                self.assertEqual(R.parse_angka(teks), D(harap))

    def test_negatif(self):
        self.assertEqual(R.parse_angka("(12.000)"), D(-12000))
        self.assertEqual(R.parse_angka("-Rp3,4 T"), D("-3400000000000"))
        self.assertEqual(R.parse_angka("Rp-1.000"), D(-1000))
        self.assertEqual(R.parse_angka("−1.500"), D(-1500))
        self.assertEqual(R.parse_angka("(Rp 2,5 M)", arti_m="miliar"), D("-2500000000"))  # v1.0.1: M butuh arti_m

    def test_satuan_laporan_hanya_untuk_angka_tanpa_akhiran(self):
        self.assertEqual(R.parse_angka("1.234.567", 6), D("1234567000000"))   # dalam jutaan
        self.assertEqual(R.parse_angka("Rp1,1 T", 6), D("1100000000000"))     # akhiran menang
        self.assertEqual(R.satuan_ke_pangkat("jutaan"), 6)
        with self.assertRaises(R.InputError):
            R.satuan_ke_pangkat("lusin")

    def test_koma_tiga_digit_diberi_catatan(self):
        cat = []
        self.assertEqual(R.parse_angka("1,234", 0, cat), D("1.234"))
        self.assertTrue(cat and "desimal" in cat[0])

    def test_kosong_dan_ditolak(self):
        for teks in (None, "", "-", "n/a", "  "):
            with self.subTest(teks=teks):
                self.assertIsNone(R.parse_angka(teks))
        for teks in ("abc", "1.2.3", "12,34,5", ",5", "5,", "1..2", "Rp", "1.234,5,6", True, float("nan"), "5 lusin"):
            with self.subTest(teks=teks):
                with self.assertRaises(R.InputError):
                    R.parse_angka(teks)

    def test_tanggal(self):
        self.assertEqual(R.parse_tanggal("31/12/2025", "x"), date(2025, 12, 31))
        with self.assertRaises(R.InputError):
            R.parse_tanggal("Des 2025", "x")


LENGKAP = {
    "emiten": "UJI", "periode_bulan": 12, "tanggal_laporan": "2025-12-31", "satuan_laporan": "miliar",
    "sumber_laporan": "uji", "pendapatan": "1.200", "pendapatan_lalu": "1.000", "laba_bersih": "150",
    "laba_bersih_lalu": "120", "total_ekuitas": "1.000", "total_ekuitas_lalu": "800",
    "total_liabilitas": "500", "total_aset": "1.500", "saham_beredar": "1 miliar",
    "harga_saham": "1.500", "tanggal_harga": "2026-09-28", "dividen_per_saham": "60",
}


class Rasio(unittest.TestCase):
    def test_rasio_lengkap(self):
        h = R.proses_rasio(dict(LENGKAP), HARI)
        # pertumbuhan: (1200-1000)/1000 = 20% ; laba (150-120)/120 = 25% ; margin 150/1200 = 12,5%
        self.assertEqual(rasio(h, "pertumbuhan_pendapatan")["nilai"], D(20))
        self.assertEqual(rasio(h, "pertumbuhan_laba")["nilai"], D(25))
        self.assertEqual(rasio(h, "margin_bersih")["nilai"], D("12.5"))
        # ROE rata-rata ekuitas: 150 / ((1000+800)/2 = 900) = 16,666..%
        self.assertEqual(round(rasio(h, "roe")["nilai"], 4), D("16.6667"))
        # DER 500/1000 = 0,5 ; EPS 150 M / 1 M lembar = 150 ; BVPS 1000 ; PER 1500/150 = 10 ; PBV 1,5
        self.assertEqual(rasio(h, "der")["nilai"], D("0.5"))
        self.assertEqual(rasio(h, "eps")["nilai"], D(150))
        self.assertEqual(rasio(h, "bvps")["nilai"], D(1000))
        self.assertEqual(rasio(h, "per")["nilai"], D(10))
        self.assertEqual(rasio(h, "pbv")["nilai"], D("1.5"))
        # kapitalisasi 1500 x 1 miliar = 1,5 T ; imbal dividen 60/1500 = 4% ; pembayaran 60/150 = 40%
        self.assertEqual(rasio(h, "kapitalisasi")["nilai"], D("1500000000000"))
        self.assertEqual(rasio(h, "imbal_dividen")["nilai"], D(4))
        self.assertEqual(rasio(h, "rasio_pembayaran")["nilai"], D(40))
        # laporan 272 hari (> 200, < 460): hanya saran cek laporan kuartal; harga 1 hari = segar
        self.assertEqual(len(h["kesegaran"]), 1)
        self.assertIn("kuartal", h["kesegaran"][0])
        h = R.proses_rasio(dict(LENGKAP, tanggal_laporan="2026-06-30"), HARI)
        self.assertEqual(h["kesegaran"], [])

    def test_ekuitas_negatif(self):
        d = dict(LENGKAP, total_ekuitas="(200)", total_ekuitas_lalu="100", total_liabilitas="1.700",
                 laba_bersih="(50)")
        h = R.proses_rasio(d, HARI)
        for kode in ("roe", "der", "pbv", "per"):
            with self.subTest(kode=kode):
                self.assertEqual(rasio(h, kode)["status"], "tidak_bermakna")
                self.assertIsNone(rasio(h, kode)["nilai"])
        self.assertTrue(any("EKUITAS NEGATIF" in f for f in h["fakta"]))
        self.assertTrue(any("RUGI" in f for f in h["fakta"]))
        # pertumbuhan laba 120 -> -50 = (-50-120)/120 = -141,666..%
        self.assertEqual(round(rasio(h, "pertumbuhan_laba")["nilai"], 2), D("-141.67"))
        md = R.md_rasio(h)
        self.assertIn("tidak bermakna", md)

    def test_ekuitas_awal_negatif_pakai_akhir(self):
        h = R.proses_rasio(dict(LENGKAP, total_ekuitas_lalu="-100"), HARI)
        self.assertEqual(rasio(h, "roe")["nilai"], D(15))  # 150/1000

    def test_rugi_ke_laba(self):
        h = R.proses_rasio(dict(LENGKAP, laba_bersih_lalu="(30)"), HARI)
        self.assertEqual(rasio(h, "pertumbuhan_laba")["status"], "tidak_bermakna")
        self.assertTrue(any("berbalik" in f for f in h["fakta"]))

    def test_kolom_kosong(self):
        h = R.proses_rasio({"emiten": "KOSONG", "pendapatan": "Rp1 T"}, HARI)
        for r in h["rasio"]:
            with self.subTest(kode=r["kode"]):
                self.assertIn(r["status"], ("tidak_dihitung",))
                self.assertIsNone(r["nilai"])
                self.assertTrue(r["alasan"].startswith("butuh"))
        self.assertTrue(any("Tanggal laporan tidak diisi" in k for k in h["kesegaran"]))
        md = R.md_rasio(h)
        self.assertIn("TIDAK DICANTUMKAN", md)

    def test_tanpa_harga(self):
        d = dict(LENGKAP)
        for k in ("harga_saham", "tanggal_harga"):
            d.pop(k)
        h = R.proses_rasio(d, HARI)
        for kode in ("per", "pbv", "kapitalisasi", "imbal_dividen"):
            self.assertEqual(rasio(h, kode)["status"], "tidak_dihitung")

    def test_interim_disetahunkan(self):
        # 6 bulan laba 150 -> setahun 300 ; ekuitas induk 1200 (tanpa rata-rata) -> ROE 25% ; EPS 300
        d = dict(LENGKAP, periode_bulan=6, ekuitas_entitas_induk="1.200")
        h = R.proses_rasio(d, HARI)
        self.assertEqual(rasio(h, "roe")["nilai"], D(25))
        self.assertEqual(rasio(h, "eps")["nilai"], D(300))
        self.assertEqual(rasio(h, "per")["nilai"], D(5))
        self.assertFalse(any(r["kode"] == "rasio_pembayaran" for r in h["rasio"]))
        self.assertTrue(any("interim" in f for f in h["fakta"]))
        # TTM diberikan -> dipakai apa adanya: 200/900 ; EPS 200
        h = R.proses_rasio(dict(LENGKAP, periode_bulan=6, laba_bersih_ttm="200"), HARI)
        self.assertEqual(rasio(h, "eps")["nilai"], D(200))

    def test_entitas_induk_diutamakan(self):
        h = R.proses_rasio(dict(LENGKAP, laba_bersih_entitas_induk="100"), HARI)
        self.assertEqual(rasio(h, "eps")["nilai"], D(100))
        self.assertEqual(rasio(h, "margin_bersih")["nilai"], D("12.5"))  # margin tetap laba total

    def test_total_dividen(self):
        d = dict(LENGKAP)
        d.pop("dividen_per_saham")
        d["total_dividen"] = "30"  # 30 miliar / 1 miliar lembar = Rp30 -> 2%
        h = R.proses_rasio(d, HARI)
        self.assertEqual(rasio(h, "imbal_dividen")["nilai"], D(2))

    def test_data_basi_dan_harga_lama(self):
        h = R.proses_rasio(dict(LENGKAP, tanggal_laporan="2024-12-31", tanggal_harga="2026-08-01"), HARI)
        teks = " ".join(h["kesegaran"])
        self.assertIn("DATA BASI", teks)
        self.assertIn("HARGA LAMA", teks)
        h = R.proses_rasio(dict(LENGKAP, tanggal_laporan="2026-01-31"), HARI)
        self.assertIn("kuartal", " ".join(h["kesegaran"]))

    def test_cek_neraca_tidak_seimbang(self):
        h = R.proses_rasio(dict(LENGKAP, total_aset="2.000"), HARI)
        self.assertTrue(any("CEK ANGKA" in f for f in h["fakta"]))

    def test_sektor_bank(self):
        h = R.proses_rasio(dict(LENGKAP, sektor="Perbankan"), HARI)
        self.assertTrue(any("Sektor keuangan" in f for f in h["fakta"]))

    def test_input_salah(self):
        for d in ({"saham_beredar": "0"}, {"harga_saham": "-5"}, {"periode_bulan": 7},
                  {"satuan_laporan": "lusin"}, {"pendapatan": "seribu"}, {"total_liabilitas": "(5)"}, []):
            with self.subTest(d=d):
                with self.assertRaises(R.InputError):
                    R.proses_rasio(d, HARI)

    def test_kolom_asing_dicatat(self):
        h = R.proses_rasio(dict(LENGKAP, target_harga="2000"), HARI)
        self.assertTrue(any("target_harga" in c for c in h["catatan_baca"]))

    def test_keluaran_tanpa_kata_rekomendasi(self):
        md = R.md_rasio(R.proses_rasio(dict(LENGKAP), HARI)).lower()
        for kata in KATA_TERLARANG:
            with self.subTest(kata=kata):
                self.assertNotIn(kata, md)
        self.assertIn("bukan nasihat investasi", md)
        self.assertIn("ojk", md)


class Level(unittest.TestCase):
    def test_level(self):
        baris = [
            {"kode": "aaaa", "harga_sekarang": "1.050", "tanggal_harga": "2026-09-28", "sumber_harga": "idx",
             "level_atas": "1.000", "level_bawah": "800"},
            {"kode": "BBBB", "harga_sekarang": "Rp 750", "tanggal_harga": "2026-09-01", "sumber_harga": "",
             "level_atas": "", "level_bawah": "760"},
            {"kode": "CCCC", "harga_sekarang": "900", "tanggal_harga": "2026-09-28", "sumber_harga": "x",
             "level_atas": "1.000", "level_bawah": "800"},
            {"kode": "DDDD", "harga_sekarang": "", "level_atas": "1.000"},
            {"kode": "EEEE", "harga_sekarang": "900", "level_atas": "800", "level_bawah": "1.000"},
            {"kode": "FFFF", "harga_sekarang": "900"},
            {"kode": "", "harga_sekarang": ""},
        ]
        h = R.proses_level(baris, HARI)
        hasil = {x["kode"]: x for x in h["hasil"]}
        self.assertTrue(hasil["AAAA"]["tersentuh"])
        self.assertTrue(hasil["BBBB"]["tersentuh"])
        self.assertIn("harga lama (28 hari)", hasil["BBBB"]["peringatan"])
        self.assertIn("sumber harga tidak dicantumkan", hasil["BBBB"]["peringatan"])
        self.assertFalse(hasil["CCCC"]["tersentuh"])
        # jarak CCCC: (1000-900)/900 = 11,11% ; (900-800)/900 = 11,11%
        self.assertEqual(hasil["CCCC"]["jarak"], ["11,11% ke level atas", "11,11% ke level bawah"])
        self.assertEqual(len(h["masalah"]), 3)  # DDDD, EEEE, FFFF
        self.assertTrue(h["ada_tersentuh"])
        md = R.md_level(h).lower()
        for kata in KATA_TERLARANG:
            self.assertNotIn(kata, md)


class CLI(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tulis(self, nama, isi):
        p = os.path.join(self.tmp, nama)
        with open(p, "w", encoding="utf-8") as f:
            f.write(isi)
        return p

    def test_rasio_md_dan_json(self):
        p = self.tulis("d.json", json.dumps(LENGKAP))
        kode, out, _ = jalankan(["rasio", p, "--hari-ini", "2026-09-29"])
        self.assertEqual(kode, 0)
        self.assertIn("| PER | 10,00x |", out)
        self.assertIn("Rp1,50 T", out)
        kode, out, _ = jalankan(["rasio", p, "--format", "json", "--hari-ini", "2026-09-29"])
        data = json.loads(out)
        per = next(r for r in data["rasio"] if r["kode"] == "per")
        self.assertEqual(per["nilai"], "10")

    def test_json_rusak(self):
        p = self.tulis("r.json", '{"emiten": "X",')
        kode, _, err = jalankan(["rasio", p])
        self.assertEqual(kode, 1)
        self.assertIn("JSON rusak", err)

    def test_file_tidak_ada(self):
        kode, _, err = jalankan(["rasio", os.path.join(self.tmp, "tidak-ada.json")])
        self.assertEqual(kode, 1)

    def test_level_csv_titik_koma_exit_code(self):
        p = self.tulis("w.csv", "kode;harga_sekarang;tanggal_harga;sumber_harga;level_atas;level_bawah;catatan\n"
                                "AAAA;1.050;2026-09-28;idx;1.000;800;cek RUPS\n")
        kode, out, _ = jalankan(["level", p, "--hari-ini", "2026-09-29"])
        self.assertEqual(kode, 2)
        self.assertIn("DI ATAS/SAMA DENGAN level atas Anda (Rp1.000)", out)
        p = self.tulis("w2.csv", "kode,harga_sekarang,level_atas\nAAAA,900,1000\n")
        kode, _, _ = jalankan(["level", p])
        self.assertEqual(kode, 0)
        p = self.tulis("w3.csv", "saham,harga\nAAAA,900\n")
        kode, _, err = jalankan(["level", p])
        self.assertEqual(kode, 1)

    def test_angka(self):
        kode, out, _ = jalankan(["angka", "1.234,5 miliar"])
        self.assertEqual(kode, 0)
        self.assertTrue(out.startswith("1.234.500.000.000"))

    def test_contoh_bawaan_jalan(self):
        p = os.path.join(AKAR, "examples", "contoh-data-emiten.json")
        kode, out, _ = jalankan(["rasio", p, "--hari-ini", "2026-09-29"])
        self.assertEqual(kode, 0)
        # EPS = 355.480 jt x 2 / 5,2 M lembar = 136,72 ; PER = 685 / 136,7231 = 5,01
        self.assertIn("Rp136,72", out)
        self.assertIn("| PER | 5,01x |", out)


class RevisiV101(unittest.TestCase):
    """Regresi untuk temuan uji independen v1.0.0 (S1-S3, R1-R5)."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def tulis(self, nama, isi):
        p = os.path.join(self.tmp, nama)
        with open(p, "w", encoding="utf-8") as f:
            f.write(isi)
        return p

    # S2 - akhiran "M"
    def test_m_ditolak_tanpa_arti_m(self):
        for teks in ("Rp5 M", "61,9 M", "5.2M", "(Rp 2,5 M)"):
            with self.subTest(teks=teks):
                with self.assertRaises(R.InputError) as ctx:
                    R.parse_angka(teks)
                self.assertIn("miliar", str(ctx.exception))
                self.assertIn("million", str(ctx.exception))

    def test_m_dengan_arti_m(self):
        cat = []
        self.assertEqual(R.parse_angka("Rp5 M", 0, cat, "miliar"), D("5000000000"))
        self.assertTrue(any("MILIAR" in c for c in cat))
        self.assertEqual(R.parse_angka("5.2M", arti_m="juta"), D("5200000"))
        with self.assertRaises(R.InputError):
            R.parse_angka("5 M", arti_m="lusin")

    def test_satuan_inggris_jelas(self):
        kasus = {"750 mn": "750000000", "1.5 million": "1500000", "2,5 bn": "2500000000", "3 billion": "3000000000",
                 "1.2 trillion": "1200000000000", "4 tn": "4000000000000", "10 thousand": "10000", "5 mio": "5000000"}
        for teks, harap in kasus.items():
            with self.subTest(teks=teks):
                self.assertEqual(R.parse_angka(teks), D(harap))

    def test_m_di_json_dan_cli(self):
        d = dict(LENGKAP, satuan_laporan="", pendapatan="1.200 M", pendapatan_lalu="1.000 M")
        with self.assertRaises(R.InputError):
            R.proses_rasio(d, HARI)
        h = R.proses_rasio(dict(d, arti_m="miliar"), HARI)
        self.assertEqual(h["angka"]["pendapatan"], D("1200000000000"))
        p = self.tulis("m.json", json.dumps(d))
        kode, _, err = jalankan(["rasio", p, "--hari-ini", "2026-09-29"])
        self.assertEqual(kode, 1)
        self.assertIn("ambigu", err)
        kode, out, _ = jalankan(["rasio", p, "--hari-ini", "2026-09-29", "--arti-m", "miliar"])
        self.assertEqual(kode, 0)
        kode, out, _ = jalankan(["angka", "61,9 M", "--arti-m", "juta"])
        self.assertTrue(out.startswith("61.900.000"))

    # S1 - exit code level
    def test_level_gagal_exit_3(self):
        p = self.tulis("g.csv", "kode,harga_sekarang,level_atas,level_bawah\nAAAA,abc,1000,800\nBBBB,900,,\n")
        kode, out, _ = jalankan(["level", p, "--hari-ini", "2026-09-29"])
        self.assertEqual(kode, 3)
        self.assertIn("0 saham dicek, 0 menyentuh level Anda, 2 baris GAGAL dicek", out)
        self.assertIn("TIDAK berarti aman", out)

    def test_level_campuran_tersentuh_dan_gagal_exit_3(self):
        p = self.tulis("c.csv", "kode,harga_sekarang,level_atas\nAAAA,1100,1000\nBBBB,,1000\n")
        kode, out, _ = jalankan(["level", p, "--format", "json", "--hari-ini", "2026-09-29"])
        self.assertEqual(kode, 3)
        data = json.loads(out)
        self.assertEqual(data["ringkasan"], {"dicek": 1, "tersentuh": 1, "gagal_dicek": 1})

    def test_level_file_tanpa_baris_exit_3(self):
        p = self.tulis("k.csv", "kode,harga_sekarang,level_atas\n")
        kode, out, _ = jalankan(["level", p])
        self.assertEqual(kode, 3)
        self.assertIn("tidak ada baris saham", out)

    def test_level_tampil_desimal(self):  # R5
        h = R.proses_level([{"kode": "X", "harga_sekarang": "1,5", "level_atas": "2", "level_bawah": "1"}], HARI)
        md = R.md_level(h)
        self.assertIn("Rp1,50", md)
        self.assertIn("| Rp1 | Rp2 |", md)

    # S3 - bank
    def test_bank_pendapatan_dari_komponen(self):
        d = dict(LENGKAP, sektor="Perbankan")
        for k in ("pendapatan", "pendapatan_lalu"):
            d.pop(k)
        # (1.500 - 500) + 200 = 1.200 ; lalu (1.300 - 400) + 100 = 1.000 -> +20% ; margin 150/1200 = 12,5%
        d.update(pendapatan_bunga="1.500", beban_bunga="500", pendapatan_operasional_lain="200",
                 pendapatan_bunga_lalu="1.300", beban_bunga_lalu="400", pendapatan_operasional_lain_lalu="100")
        h = R.proses_rasio(d, HARI)
        self.assertEqual(rasio(h, "pertumbuhan_pendapatan")["nilai"], D(20))
        m = rasio(h, "margin_bersih")
        self.assertEqual(m["nilai"], D("12.5"))
        self.assertIn("tidak sebanding lintas sektor", m["nama"])
        self.assertIn("pendapatan bunga bersih", m["rumus"])
        self.assertTrue(any("dihitung = pendapatan bunga - beban bunga" in f for f in h["fakta"]))
        self.assertTrue(any("ROE hitungan ini bisa berbeda" in f for f in h["fakta"]))

    def test_bank_isi_total_pendapatan_bunga_diperingatkan(self):
        h = R.proses_rasio(dict(LENGKAP, sektor="Bank", pendapatan_bunga="1.200"), HARI)
        self.assertTrue(any(f.startswith("PERINGATAN") and "bruto" in f for f in h["fakta"]))
        h = R.proses_rasio(dict(LENGKAP, sektor="bank", jenis_pendapatan="total pendapatan bunga"), HARI)
        self.assertTrue(any(f.startswith("PERINGATAN") for f in h["fakta"]))
        h = R.proses_rasio(dict(LENGKAP, sektor="bank"), HARI)
        self.assertTrue(any("pastikan 'pendapatan'" in f for f in h["fakta"]))
        h = R.proses_rasio(dict(LENGKAP, sektor="bank", jenis_pendapatan="pendapatan bunga bersih + operasional lain"), HARI)
        self.assertFalse(any(f.startswith("PERINGATAN") for f in h["fakta"]))

    def test_non_bank_tanpa_catatan_bank(self):
        h = R.proses_rasio(dict(LENGKAP, sektor="Konsumer"), HARI)
        self.assertEqual(rasio(h, "margin_bersih")["nama"], "Margin laba bersih")
        self.assertFalse(any("Bank" in f or "Sektor keuangan" in f for f in h["fakta"]))

    # R1-R4
    def test_nol_koma_desimal(self):
        self.assertEqual(R.parse_angka("0.125"), D("0.125"))
        self.assertEqual(R.parse_angka("0,125"), D("0.125"))

    def test_satuan_frasa_laporan(self):
        for teks, harap in (("dalam jutaan Rupiah", 6), ("(dalam jutaan rupiah)", 6), ("in millions of Rupiah", 6),
                            ("Rp juta", 6), ("dalam miliaran", 9), ("in thousands", 3)):
            with self.subTest(teks=teks):
                self.assertEqual(R.satuan_ke_pangkat(teks), harap)

    def test_laba_ke_rugi_simetris(self):
        h = R.proses_rasio(dict(LENGKAP, laba_bersih="(50)"), HARI)
        self.assertTrue(any("Berbalik dari LABA" in f for f in h["fakta"]))
        self.assertFalse(any("Laba bersih turun" in f for f in h["fakta"]))

    def test_roe_basis_campuran_dan_rata_rata_induk(self):
        h = R.proses_rasio(dict(LENGKAP, laba_bersih_entitas_induk="140"), HARI)
        self.assertTrue(any("mencampur basis" in f for f in h["fakta"]))
        # induk: 140 / ((1.200 + 800) / 2 = 1.000) = 14%
        h = R.proses_rasio(dict(LENGKAP, laba_bersih_entitas_induk="140", ekuitas_entitas_induk="1.200",
                                ekuitas_entitas_induk_lalu="800"), HARI)
        self.assertEqual(rasio(h, "roe")["nilai"], D(14))
        self.assertFalse(any("mencampur basis" in f for f in h["fakta"]))


if __name__ == "__main__":
    unittest.main(verbosity=1)
