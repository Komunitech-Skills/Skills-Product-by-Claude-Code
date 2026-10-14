#!/usr/bin/env python3
"""Uji regresi banding_pemasok.py. Jalankan dari folder skill: python3 tests/uji_regresi.py
(Windows: python atau py). Python standar saja.

Angka pembanding dihitung ulang secara independen di file ini (int/float biasa), bukan disalin
dari keluaran script.
"""
import json
import os
import subprocess
import sys
import unittest
from decimal import Decimal

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(AKAR, "scripts", "banding_pemasok.py")
sys.path.insert(0, os.path.join(AKAR, "scripts"))
import banding_pemasok as B  # noqa: E402


def jalan(data, *arg):
    if not isinstance(data, str):
        data = json.dumps(data)
    p = subprocess.run([sys.executable, SCRIPT, "--data", data] + list(arg), capture_output=True, text=True)
    if p.returncode == 0:
        if "--format" in arg and "teks" in arg:
            return 0, p.stdout
        return 0, json.loads(p.stdout)
    return p.returncode, json.loads(p.stderr)


def ppn(dpp):  # 11% dibulatkan ke bawah (12% x 11/12)
    return dpp * 11 // 100


def pem(h, nama):
    return next(x for x in h["pemasok"] if x["nama"] == nama)


NORMAL = {
    "kebutuhan": {"qty": 300, "satuan": "pcs", "butuh_dalam_hari": 14},
    "pemasok": [
        {"nama": "CV Kemasan Prima", "harga_satuan": "Rp4.500/pcs", "tingkat_harga": "250: 4.200; 500: 3.900",
         "moq": 100, "ongkir": "85rb", "pkp": "PKP", "harga_termasuk_ppn": "belum", "lead_time": "5-7 hari",
         "termin": "DP 50%, pelunasan saat barang tiba", "nilai_kualitas": 4},
        {"nama": "UD Sumber Plastik", "harga_satuan": 4300, "moq": 500, "ongkir": "gratis", "pkp": "non-PKP",
         "lead_time": 3, "termin": "tempo 30 hari", "nilai_kualitas": 3},
        {"nama": "Toko Grosir Abadi", "harga_satuan": "4.650", "ongkir": "", "pkp": "", "lead_time": "2 minggu",
         "termin": "COD"},
    ],
}


class TesNormal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.k, cls.h = jalan(NORMAL)

    def test_jalan(self):
        self.assertEqual(self.k, 0)

    def test_total_pkp_belum_termasuk(self):
        sub = 300 * 4200
        tag = sub + 85000
        p = pem(self.h, "CV Kemasan Prima")
        self.assertEqual(p["harga_berlaku"], 4200)
        self.assertEqual(p["subtotal"], sub)
        self.assertEqual(p["dpp"], tag)
        self.assertEqual(p["ppn"], ppn(tag))
        self.assertEqual(p["total_bayar"], tag + ppn(tag))  # 1.492.950

    def test_total_moq_dan_non_pkp(self):
        p = pem(self.h, "UD Sumber Plastik")
        self.assertEqual(p["qty_beli"], 500)
        self.assertEqual(p["kelebihan_unit"], 200)
        self.assertEqual(p["total_bayar"], 500 * 4300)
        self.assertEqual(p["ppn"], 0)
        self.assertEqual(p["nilai_kelebihan"], 200 * 4300)
        self.assertAlmostEqual(p["per_unit"], round(500 * 4300 / 300, 2), places=2)
        self.assertEqual(p["skor"]["moq"], 60.0)
        self.assertIn("moq_tidak_terpenuhi", p["tanda"])

    def test_termurah_dan_selisih(self):
        self.assertEqual(self.h["termurah"], ["Toko Grosir Abadi"])
        p = pem(self.h, "CV Kemasan Prima")
        total = 1260000 + 85000 + ppn(1345000)
        self.assertEqual(p["selisih_vs_termurah_rp"], total - 1395000)
        self.assertEqual(p["selisih_vs_termurah_persen"], round((total - 1395000) * 100 / 1395000, 1))

    def test_skor_independen(self):
        tot = {"CV Kemasan Prima": 1492950, "UD Sumber Plastik": 2150000, "Toko Grosir Abadi": 1395000}
        lead = {"CV Kemasan Prima": 7, "UD Sumber Plastik": 3, "Toko Grosir Abadi": 14}
        hari = {"CV Kemasan Prima": -0.5 * 7, "UD Sumber Plastik": 30, "Toko Grosir Abadi": 0}
        kual = {"CV Kemasan Prima": 80, "UD Sumber Plastik": 60, "Toko Grosir Abadi": 60}
        moq = {"CV Kemasan Prima": 100, "UD Sumber Plastik": 60, "Toko Grosir Abadi": 100}
        for n in tot:
            sb = 100 * 1395000 / tot[n]
            sl = 100 * (3 + 1) / (lead[n] + 1)
            st = max(0, min(100, 50 + hari[n] * 50 / 30))
            total = (40 * sb + 20 * sl + 15 * st + 15 * kual[n] + 10 * moq[n]) / 100
            p = pem(self.h, n)
            self.assertAlmostEqual(p["skor"]["biaya"], round(sb, 1), places=1, msg=n)
            self.assertAlmostEqual(p["skor"]["lead_time"], round(sl, 1), places=1, msg=n)
            self.assertAlmostEqual(p["skor"]["termin"], round(st, 1), places=1, msg=n)
            self.assertAlmostEqual(p["skor_total"], round(total, 1), places=1, msg=n)

    def test_rekomendasi_seri_pilih_murah(self):
        # CV Kemasan Prima & UD Sumber Plastik sama-sama 76,0 -> pilih yang lebih murah
        self.assertEqual(self.h["rekomendasi"]["nama"], "CV Kemasan Prima")
        self.assertEqual(self.h["peringkat"][0], "CV Kemasan Prima")
        self.assertEqual(self.h["rekomendasi"]["hampir_seri_dengan"], "UD Sumber Plastik")

    def test_isian_data_kurang(self):
        isi = [(x["pemasok"], x["data"]) for x in self.h["isian"]]
        self.assertIn(("Toko Grosir Abadi", "ongkir ke alamat Anda"), isi)
        self.assertTrue(any(n == "Toko Grosir Abadi" and "PKP" in d for n, d in isi))
        p = pem(self.h, "Toko Grosir Abadi")
        self.assertEqual(p["potensi_ppn"], ppn(1395000))
        self.assertIn("kualitas_belum_dinilai", p["tanda"])

    def test_sensitivitas_qty2x(self):
        s = self.h["sensitivitas"]["qty_2x"]
        self.assertEqual(s["qty"], 600)
        self.assertEqual(s["termurah"], ["UD Sumber Plastik"])  # 600 x 4.300 = 2.580.000
        self.assertTrue(s["rekomendasi_berubah"])
        cv = next(x for x in s["pemasok"] if x["nama"] == "CV Kemasan Prima")
        tag = 600 * 3900 + 85000
        self.assertEqual(cv["biaya_pembanding"], tag + ppn(tag))

    def test_sensitivitas_telat_dan_bagi(self):
        t = self.h["sensitivitas"]["termurah_telat"]
        self.assertEqual(t["pemasok"], "Toko Grosir Abadi")
        self.assertEqual(t["lead_time_menjadi"], 21)
        self.assertTrue(t["melewati_tenggat"])
        self.assertEqual(t["hemat_vs_termurah_kedua"], 1492950 - 1395000)
        b = self.h["sensitivitas"]["bagi_pesanan"]
        self.assertEqual((b["qty_utama"], b["qty_cadangan"]), (210, 90))
        a = 210 * 4500 + 85000
        self.assertEqual(b["total"], a + ppn(a) + 90 * 4650)
        self.assertEqual(b["cadangan"], "Toko Grosir Abadi")  # bukan UD (MOQ 500 memaksa beli lebih)

    def test_teks(self):
        k, t = jalan(NORMAL, "--format", "teks")
        self.assertEqual(k, 0)
        self.assertIn("UNTUK AGENT SAJA", t)
        self.assertIn("| Pemasok | Total bayar (per pcs) | Selisih vs termurah | Skor (peringkat) |", t)
        self.assertIn("Rp1.492.950", t)
        self.assertIn("[isian:", t)


class TesTingkatHarga(unittest.TestCase):
    def dasar(self, qty, tingkat="100: 11.000; 500: 10.000", harga="12.000"):
        return jalan({"kebutuhan": {"qty": qty}, "pemasok": [
            {"nama": "A", "harga_satuan": harga, "tingkat_harga": tingkat, "ongkir": 0, "pkp": "tidak"}]})[1]

    def test_batas_tingkat(self):
        self.assertEqual(self.dasar(99)["pemasok"][0]["harga_berlaku"], 12000)
        self.assertEqual(self.dasar(100)["pemasok"][0]["harga_berlaku"], 11000)
        self.assertEqual(self.dasar(499)["pemasok"][0]["harga_berlaku"], 11000)
        self.assertEqual(self.dasar(500)["pemasok"][0]["harga_berlaku"], 10000)
        self.assertEqual(self.dasar(500)["pemasok"][0]["total_bayar"], 500 * 10000)

    def test_beli_lebih_justru_lebih_murah(self):
        p = self.dasar(95)["pemasok"][0]
        self.assertEqual(p["total_bayar"], 95 * 12000)
        st = p["saran_tingkat"]
        self.assertEqual(st["qty_beli"], 100)
        self.assertTrue(st["lebih_murah_total"])
        self.assertEqual(st["selisih_total"], 100 * 11000 - 95 * 12000)  # -40.000

    def test_format_rentang_dan_json(self):
        p = self.dasar(150, tingkat="1-99=12rb | 100-499=11,5rb | 500+=10rb", harga="")["pemasok"][0]
        self.assertEqual(p["harga_berlaku"], 11500)
        p = jalan({"kebutuhan": {"qty": 600}, "pemasok": [
            {"nama": "J", "tingkat_harga": [{"min": 1, "harga": 9000}, {"min": 500, "harga": 8000}], "pkp": "tidak"}]})[1]
        self.assertEqual(p["pemasok"][0]["harga_berlaku"], 8000)

    def test_tingkat_persen(self):
        p = self.dasar(200, tingkat=">=200: diskon 5%", harga="10.000")["pemasok"][0]
        self.assertEqual(p["harga_berlaku"], 9500)
        self.assertEqual(p["total_bayar"], 200 * 9500)

    def test_tanpa_harga_dasar_jadi_moq(self):
        p = self.dasar(50, tingkat="100-499: 11.000; 500+: 10.000", harga="")["pemasok"][0]
        self.assertEqual(p["qty_beli"], 100)
        self.assertEqual(p["moq_efektif"], 100)


class TesMoqKemasan(unittest.TestCase):
    def test_kelipatan(self):
        p = jalan({"kebutuhan": {"qty": 130}, "pemasok": [
            {"nama": "A", "harga_satuan": 1000, "kelipatan": 24, "pkp": "tidak", "ongkir": 0}]})[1]["pemasok"][0]
        self.assertEqual(p["qty_beli"], 144)
        self.assertEqual(p["kelebihan_unit"], 14)

    def test_harga_per_dus(self):
        p = jalan({"kebutuhan": {"qty": 100}, "pemasok": [
            {"nama": "Dus", "harga_satuan": "240.000", "isi_kemasan": 24, "moq": 5, "pkp": "tidak", "ongkir": 0}]})[1]["pemasok"][0]
        self.assertEqual(p["qty_beli"], 120)  # MOQ 5 dus x 24
        self.assertEqual(p["harga_berlaku"], 10000)
        self.assertEqual(p["total_bayar"], 5 * 240000)

    def test_min_belanja(self):
        p = jalan({"kebutuhan": {"qty": 50}, "pemasok": [
            {"nama": "A", "harga_satuan": 10000, "min_belanja": "1jt", "pkp": "tidak", "ongkir": 0}]})[1]["pemasok"][0]
        self.assertEqual(p["qty_beli"], 100)

    def test_moq_terpenuhi_tanpa_kelebihan(self):
        p = jalan({"kebutuhan": {"qty": 500}, "pemasok": [
            {"nama": "A", "harga_satuan": 100, "moq": 500, "pkp": "tidak", "ongkir": 0}]})[1]["pemasok"][0]
        self.assertEqual(p["kelebihan_unit"], 0)
        self.assertEqual(p["skor"]["moq"], 100.0)


class TesSatuan(unittest.TestCase):
    def test_lusin_kodi_dan_dus_tanpa_isi(self):
        h = jalan({"kebutuhan": {"qty": 30, "satuan": "pcs"}, "pemasok": [
            {"nama": "Lusin", "harga_satuan": 1000, "moq": "3 lusin", "pkp": "tidak", "ongkir": 0},
            {"nama": "Kodi", "harga_satuan": 1000, "moq": "1 kodi", "pkp": "tidak", "ongkir": 0},
            {"nama": "Dus", "harga_satuan": 1000, "moq": "3 dus"}]})[1]
        self.assertEqual(pem(h, "Lusin")["qty_beli"], 36)
        self.assertEqual(pem(h, "Kodi")["qty_beli"], 30)  # MOQ 20 < 30
        self.assertEqual([d["pemasok"] for d in h["dilewati"]], ["Dus"])  # isi per dus tidak ditebak

    def test_ongkir_per_unit_dan_per_dus(self):
        h = jalan({"kebutuhan": {"qty": 30, "satuan": "pcs"}, "pemasok": [
            {"nama": "PerPcs", "harga_satuan": 1000, "ongkir": "500/pcs", "pkp": "tidak"},
            {"nama": "PerDus", "harga_satuan": "12.000/dus", "isi_kemasan": 12, "ongkir": "15rb/dus", "pkp": "tidak"},
            {"nama": "DusTanpaIsi", "harga_satuan": 1000, "ongkir": "10rb per dus"}]})[1]
        self.assertEqual(pem(h, "PerPcs")["total_bayar"], 30 * 1000 + 30 * 500)
        self.assertEqual(pem(h, "PerDus")["qty_beli"], 36)
        self.assertEqual(pem(h, "PerDus")["total_bayar"], 3 * 12000 + 3 * 15000)
        self.assertEqual([d["pemasok"] for d in h["dilewati"]], ["DusTanpaIsi"])


class TesPPN(unittest.TestCase):
    def satu(self, **kw):
        rec = {"nama": "P", "harga_satuan": 10000, "ongkir": 0}
        rec.update(kw)
        qty = rec.pop("qty", 100)
        pembeli = rec.pop("pembeli_pkp", None)
        keb = {"qty": qty}
        if pembeli:
            keb["pembeli_pkp"] = pembeli
        return jalan({"kebutuhan": keb, "pemasok": [rec]})[1]["pemasok"][0]

    def test_belum_termasuk(self):
        p = self.satu(pkp="ya", harga_termasuk_ppn="tidak")
        self.assertEqual((p["dpp"], p["ppn"], p["total_bayar"]), (1000000, 110000, 1110000))

    def test_termasuk_pas(self):
        p = self.satu(pkp="ya", harga_termasuk_ppn="ya", harga_satuan=11100)
        self.assertEqual((p["dpp"], p["ppn"], p["sisa_pembulatan"], p["total_bayar"]), (1000000, 110000, 0, 1110000))

    def test_termasuk_dpp_terbesar(self):
        gross = 1000000
        d = max(x for x in range(gross - 200000, gross + 1) if x + ppn(x) <= gross)
        p = self.satu(pkp="ya", harga_termasuk_ppn="sudah termasuk PPN")
        self.assertEqual(p["dpp"], d)
        self.assertEqual(p["ppn"], ppn(d))
        self.assertEqual(p["sisa_pembulatan"], gross - d - ppn(d))
        self.assertEqual(p["total_bayar"], gross)

    def test_pembulatan_ke_bawah(self):
        p = self.satu(pkp="ya", harga_termasuk_ppn="tidak", harga_satuan=1234, qty=7)
        self.assertEqual(p["ppn"], 8638 * 11 // 100)  # 950,18 -> 950

    def test_ongkir_ekspedisi_tidak_kena_ppn(self):
        p = self.satu(pkp="ya", harga_termasuk_ppn="tidak", ongkir=50000, ongkir_ditagih_pemasok="tidak")
        self.assertEqual(p["ppn"], 110000)
        self.assertEqual(p["total_bayar"], 1000000 + 110000 + 50000)
        q = self.satu(pkp="ya", harga_termasuk_ppn="tidak", ongkir=50000)
        self.assertEqual(q["ppn"], ppn(1050000))

    def test_pembeli_pkp_membalik_urutan(self):
        data = {"kebutuhan": {"qty": 100}, "pemasok": [
            {"nama": "PKP", "harga_satuan": 10000, "pkp": "ya", "harga_termasuk_ppn": "belum", "ongkir": 0},
            {"nama": "NonPKP", "harga_satuan": 10500, "pkp": "tidak", "ongkir": 0}]}
        self.assertEqual(jalan(data)[1]["termurah"], ["NonPKP"])  # 1.110.000 vs 1.050.000
        data["kebutuhan"]["pembeli_pkp"] = "ya"
        h = jalan(data)[1]
        self.assertEqual(h["termurah"], ["PKP"])  # 1.000.000 (PPN dikreditkan) vs 1.050.000
        p = pem(h, "PKP")
        self.assertEqual(p["total_bayar"], 1110000)
        self.assertEqual(p["ppn_dikreditkan"], 110000)
        self.assertEqual(p["biaya_pembanding"], 1000000)

    def test_non_pkp_menyebut_ppn(self):
        p = self.satu(pkp="non PKP", harga_termasuk_ppn="ya")
        self.assertEqual(p["ppn"], 0)
        self.assertIn("non_pkp_menyebut_ppn", p["tanda"])

    def test_status_tak_jelas(self):
        p = self.satu(pkp="")
        self.assertIsNone(p["pkp"])
        self.assertEqual(p["potensi_ppn"], 110000)
        self.assertEqual(p["total_bayar"], 1000000)
        q = self.satu(harga_termasuk_ppn="belum termasuk")
        self.assertTrue(q["pkp"])  # menyebut PPN -> dianggap PKP
        self.assertEqual(q["ppn"], 110000)


class TesDataRusak(unittest.TestCase):
    def test_satu_pemasok_rusak_dilewati(self):
        k, h = jalan({"kebutuhan": {"qty": 10}, "pemasok": [
            {"nama": "Baik", "harga_satuan": 1000, "pkp": "tidak"},
            {"nama": "Rusak", "harga_satuan": "abc"},
            {"nama": "Kosong", "harga_satuan": ""},
            {"nama": "Minus", "harga_satuan": 1000, "ongkir": -5000},
            {"nama": "DP", "harga_satuan": 1000, "dp_persen": 150}]})
        self.assertEqual(k, 0)
        self.assertEqual([p["nama"] for p in h["pemasok"]], ["Baik"])
        self.assertEqual(sorted(d["pemasok"] for d in h["dilewati"]), ["DP", "Kosong", "Minus", "Rusak"])

    def test_semua_rusak(self):
        k, e = jalan({"kebutuhan": {"qty": 10}, "pemasok": [{"nama": "X", "harga_satuan": "??x"}]})
        self.assertEqual(k, 2)
        self.assertIn("saran", e)

    def test_qty_kosong(self):
        k, e = jalan({"pemasok": [{"nama": "A", "harga_satuan": 1000}]})
        self.assertEqual(k, 2)
        self.assertIn("jumlah", e["error"])

    def test_data_kosong_dan_header_saja(self):
        self.assertEqual(jalan("", "--qty", "10")[0], 2)
        self.assertEqual(jalan("nama;harga", "--qty", "10")[0], 2)
        self.assertEqual(jalan("{rusak", "--qty", "10")[0], 2)
        self.assertEqual(jalan({"kebutuhan": {"qty": 5}, "pemasok": []})[0], 2)

    def test_bobot_rusak(self):
        base = {"kebutuhan": {"qty": 10}, "pemasok": [{"nama": "A", "harga_satuan": 1000}]}
        self.assertEqual(jalan(base, "--bobot", "harga=abc")[0], 2)
        self.assertEqual(jalan(base, "--bobot", "warna=10")[0], 2)
        self.assertEqual(jalan(base, "--bobot", "biaya=0,lead=0,termin=0,kualitas=0,moq=0")[0], 2)

    def test_kolom_kosong_jadi_isian(self):
        k, h = jalan("nama;harga;ongkir;lead time;termin;pkp\nA;5.000;;;;\nB;5.200;20rb;3;cod;tidak", "--qty", "100")
        self.assertEqual(k, 0)
        a = pem(h, "A")
        for t in ("ongkir_belum_ada", "lead_time_belum_ada", "termin_belum_ada", "status_pkp_belum_jelas"):
            self.assertIn(t, a["tanda"])
        self.assertEqual(a["skor"]["lead_time"], 50.0)
        self.assertEqual(a["skor"]["termin"], 50.0)

    def test_kualitas_luar_rentang(self):
        h = jalan({"kebutuhan": {"qty": 10}, "pemasok": [{"nama": "A", "harga_satuan": 1000, "kualitas": 7}]})[1]
        self.assertIsNone(h["pemasok"][0]["nilai_kualitas"])
        self.assertTrue(any("di luar 1-5" in c for c in h["catatan"]))

    def test_nama_ganda(self):
        h = jalan({"kebutuhan": {"qty": 10}, "pemasok": [{"nama": "A", "harga_satuan": 1000},
                                                          {"nama": "A", "harga_satuan": 1100}]})[1]
        self.assertEqual(sorted(p["nama"] for p in h["pemasok"]), ["A", "A (2)"])


class TesBobotTenggat(unittest.TestCase):
    DATA = {"kebutuhan": {"qty": 100}, "pemasok": [
        {"nama": "Murah Lambat", "harga_satuan": 9000, "lead_time": 20, "pkp": "tidak", "termin": "cod", "kualitas": 3},
        {"nama": "Mahal Cepat", "harga_satuan": 10000, "lead_time": 2, "pkp": "tidak", "termin": "cod", "kualitas": 3}]}

    def test_bobot_biaya_saja(self):
        h = jalan(self.DATA, "--bobot", "biaya=100,lead=0,termin=0,kualitas=0,moq=0")[1]
        self.assertEqual(h["peringkat"][0], "Murah Lambat")
        self.assertEqual(h["bobot"]["lead_time"], 0)

    def test_bobot_sebagian_sisanya_default(self):
        h = jalan(self.DATA, "--bobot", "biaya=60")[1]
        self.assertEqual(h["bobot"], {"biaya": 60, "lead_time": 20, "termin": 15, "kualitas": 15, "moq": 10})

    def test_tenggat_dilewati_tidak_direkomendasikan(self):
        h = jalan(self.DATA, "--butuh-hari", "14", "--bobot", "biaya=100,lead=1,termin=0,kualitas=0,moq=0")[1]
        self.assertEqual(h["peringkat"][0], "Murah Lambat")  # skor tertinggi
        self.assertEqual(h["rekomendasi"]["nama"], "Mahal Cepat")  # tapi telat -> bukan rekomendasi
        self.assertEqual(h["melewati_tenggat"], ["Murah Lambat"])
        self.assertEqual(pem(h, "Murah Lambat")["skor"]["lead_time"], 0)

    def test_titik_impas_telat(self):
        h = jalan(self.DATA, "--biaya-telat-per-hari", "20rb", "--telat-hari", "7")[1]
        t = h["sensitivitas"]["termurah_telat"]
        hemat = 1000000 - 900000
        self.assertEqual(t["hemat_vs_termurah_kedua"], hemat)
        self.assertEqual(t["hari_impas"], hemat // 20000)  # 5
        self.assertEqual(t["kerugian_bila_telat"], 7 * 20000)
        self.assertFalse(t["masih_untung_bila_telat"])

    def test_bunga_modal(self):
        h = jalan({"kebutuhan": {"qty": 100}, "pemasok": [
            {"nama": "Tempo", "harga_satuan": 10000, "pkp": "tidak", "termin": "tempo 30 hari", "lead_time": 5},
            {"nama": "Dimuka", "harga_satuan": 10000, "pkp": "tidak", "termin": "bayar di muka", "lead_time": 15}]},
            "--bunga-modal", "2")[1]
        self.assertEqual(pem(h, "Tempo")["manfaat_tempo"], 1000000 * 2 // 100)        # 20.000
        self.assertEqual(pem(h, "Dimuka")["biaya_dana_dp"], 1000000 * 2 // 100 // 2)   # 10.000
        self.assertEqual(pem(h, "Tempo")["biaya_pembanding"], 980000)
        self.assertEqual(h["termurah"], ["Tempo"])


class TesParsing(unittest.TestCase):
    def test_angka(self):
        self.assertEqual(B.parse_angka("Rp12.500/pcs", "x"), 12500)
        self.assertEqual(B.parse_angka("11,5rb", "x"), 11500)
        self.assertEqual(B.parse_angka("Rp 1,2 jt", "x"), 1200000)
        self.assertEqual(B.parse_angka("45,000", "x"), 45000)
        self.assertEqual(B.parse_angka("Rp 4.500,-", "x"), 4500)
        self.assertEqual(B.parse_angka("12,5 kg", "x"), Decimal("12.5"))
        self.assertIsNone(B.parse_angka("", "x"))

    def test_termin(self):
        self.assertEqual(B.parse_termin("DP 50%, sisa tempo 30 hari"), (50, 30))
        self.assertEqual(B.parse_termin("COD"), (0, 0))
        self.assertEqual(B.parse_termin("bayar di muka"), (100, 0))
        self.assertEqual(B.parse_termin("Net 14"), (0, 14))
        self.assertEqual(B.parse_termin("dp 30% pelunasan saat barang tiba"), (30, 0))
        self.assertIsNone(B.parse_termin("konsinyasi"))
        self.assertEqual(B.parse_termin("tempo 2 minggu"), (0, 14))
        self.assertEqual(B.parse_termin("DP 50% sisa H+30"), (50, 30))

    def test_lead_dan_ya(self):
        self.assertEqual(B.parse_lead("2 minggu")[0], 14)
        self.assertEqual(B.parse_lead("3-5 hari")[0], 5)
        self.assertIsNone(B.parse_lead("ready stock")[0])
        self.assertEqual(B.parse_lead("5 hari kerja")[0], 7)
        self.assertIs(B.parse_ya("non-PKP"), False)
        self.assertIs(B.parse_ya("belum termasuk PPN"), False)
        self.assertIs(B.parse_ya("incl. PPN"), True)
        self.assertIsNone(B.parse_ya("?"))

    def test_csv_titik_koma_dan_markdown(self):
        csv_teks = ("nama;harga;tingkat harga;moq;ongkir;pkp;termin\n"
                    "CV A;12.000;100:11.000|500:10.000;50;franco;ya;tempo 14 hari\n"
                    "UD B;11.800;;100;loco;tidak;cod")
        k, h = jalan(csv_teks, "--qty", "200")
        self.assertEqual(k, 0)
        a = pem(h, "CV A")
        self.assertEqual(a["harga_berlaku"], 11000)
        self.assertEqual(a["total_bayar"], 200 * 11000 + ppn(200 * 11000))
        self.assertIn("ambil_sendiri_belum_dihitung", pem(h, "UD B")["tanda"])
        md = "| Pemasok | Harga | Ongkir |\n|---|---|---|\n| X | 5rb | 10rb |\n| Y | 5,2rb | 0 |"
        k, h = jalan(md, "--qty", "10")
        self.assertEqual(pem(h, "X")["total_bayar"], 50000 + 10000)

    def test_diskon(self):
        h = jalan({"kebutuhan": {"qty": 100}, "pemasok": [
            {"nama": "Persen", "harga_satuan": 10000, "diskon": "5%", "pkp": "tidak", "ongkir": 0},
            {"nama": "Rupiah", "harga_satuan": 10000, "diskon": "Rp25.000", "pkp": "tidak", "ongkir": 0}]})[1]
        self.assertEqual(pem(h, "Persen")["diskon"], 50000)
        self.assertEqual(pem(h, "Rupiah")["diskon"], 25000)


if __name__ == "__main__":
    unittest.main(verbosity=1)
