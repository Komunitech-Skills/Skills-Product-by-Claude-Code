#!/usr/bin/env python3
"""Uji otomatis thr.py. Jalankan: python3 test_thr.py"""
import datetime
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal as D

FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, FOLDER)
import ter_core as tc  # noqa: E402
import thr  # noqa: E402

SHA256_TABEL = "26edfe89bda74169a5280317da194cec3194e8c48c661a8e6860ff8b48d5da72"
SUMBER_REPO = os.path.normpath(os.path.join(FOLDER, "..", "..", "..", "research", "sources", "pph21-ter-tabel.json"))
CORE_SKILL1 = os.path.normpath(os.path.join(FOLDER, "..", "..", "pph21-ter", "scripts", "ter_core.py"))


def cfg(hari_raya="2027-03-10", bayar=None):
    hr = datetime.date.fromisoformat(hari_raya)
    batas = hr - datetime.timedelta(days=7)
    b = datetime.date.fromisoformat(bayar) if bayar else batas
    return {"hari_raya": hr, "batas_bayar": batas, "tanggal_bayar": b, "bulan_bayar": b.month,
            "nama_hari_raya": "Idul Fitri", "perusahaan": "PT Uji", "peringatan": []}


def orang(**kw):
    r = {"nama": "Uji", "jenis": "tetap", "gaji_pokok": "5jt", "tanggal_mulai": "2020-01-01"}
    r.update(kw)
    return r


class TestTabel(unittest.TestCase):
    def test_hash(self):
        with open(tc.FILE_TABEL, "rb") as f:
            self.assertEqual(hashlib.sha256(f.read()).hexdigest(), SHA256_TABEL)

    def test_sama_dengan_sumber(self):
        if not os.path.exists(SUMBER_REPO):
            self.skipTest("sumber riset tidak ada (paket pembeli)")
        with open(SUMBER_REPO, encoding="utf-8") as a, open(tc.FILE_TABEL, encoding="utf-8") as b:
            self.assertEqual(json.load(a), json.load(b))

    def test_core_identik(self):
        if not os.path.exists(CORE_SKILL1):
            self.skipTest("skill pph21-ter tidak berdampingan")
        with open(CORE_SKILL1, "rb") as a, open(os.path.join(FOLDER, "ter_core.py"), "rb") as b:
            self.assertEqual(a.read(), b.read())

    def test_contoh_resmi_ter(self):
        self.assertEqual(tc.pph_ter_bulanan(D(10000000), "A")[0], 200000)   # PP 58/2023 K/0
        self.assertEqual(tc.pph_ter_bulanan(D(15500000), "A")[0], 1085000)  # PMK 168/2023


class TestMasaKerja(unittest.TestCase):
    def test_bulan_penuh(self):
        f = datetime.date.fromisoformat
        self.assertEqual(thr.bulan_penuh(f("2026-03-10"), f("2027-03-10")), 12)
        self.assertEqual(thr.bulan_penuh(f("2026-03-11"), f("2027-03-10")), 11)
        self.assertEqual(thr.bulan_penuh(f("2027-02-10"), f("2027-03-10")), 1)
        self.assertEqual(thr.bulan_penuh(f("2027-02-11"), f("2027-03-10")), 0)

    def test_11_vs_12_bulan(self):
        h11 = thr.hitung_karyawan(orang(gaji_pokok="6jt", tanggal_mulai="2026-03-11"), cfg())
        h12 = thr.hitung_karyawan(orang(gaji_pokok="6jt", tanggal_mulai="2026-03-10"), cfg())
        self.assertEqual((h11["masa_kerja_bulan"], h11["thr"]), (11, 5500000))
        self.assertEqual((h12["masa_kerja_bulan"], h12["thr"]), (12, 6000000))

    def test_kurang_1_bulan(self):
        h = thr.hitung_karyawan(orang(tanggal_mulai="2027-02-20"), cfg())
        self.assertFalse(h["berhak"])
        self.assertEqual(h["thr"], 0)

    def test_proporsional_dan_pembulatan(self):
        h = thr.hitung_karyawan(orang(gaji_pokok="5.000.000", tunjangan_tetap="555.555", masa_kerja_bulan="7"),
                                cfg())
        self.assertEqual(h["thr"], tc.bulat_terdekat(D(7) / 12 * D(5555555)))
        self.assertEqual(h["thr"], 3240740)

    def test_komponen_upah(self):
        h = thr.hitung_karyawan(orang(gaji_pokok="5jt", tunjangan_tetap="750rb"), cfg())
        self.assertEqual(h["thr"], 5750000)


class TestJenis(unittest.TestCase):
    def test_harian_12_bulan_rata2(self):
        upah = "+".join(["3jt"] * 11 + ["4,2jt"] + ["9jt"])     # 13 data: yang dipakai 12 terakhir
        h = thr.hitung_karyawan(orang(jenis="harian", gaji_pokok="", upah_bulanan=upah, tanggal_mulai="2025-01-01"),
                                cfg())
        self.assertEqual(h["upah_sebulan"], (D(3000000) * 10 + D(4200000) + D(9000000)) / 12)
        self.assertEqual(h["thr"], 3600000)

    def test_harian_kurang_12(self):
        h = thr.hitung_karyawan(orang(jenis="harian", gaji_pokok="", upah_bulanan="3jt+2jt+4jt",
                                      tanggal_mulai="2026-12-01"), cfg())
        self.assertEqual(h["masa_kerja_bulan"], 3)
        self.assertEqual(h["thr"], 750000)                          # 3/12 x rata-rata 3 jt

    def test_pkwt_berakhir_sebelum_hari_raya(self):
        h = thr.hitung_karyawan(orang(jenis="kontrak", tanggal_berhenti="2027-03-01"), cfg())
        self.assertFalse(h["berhak"])

    def test_pkwtt_phk_30_hari(self):
        h = thr.hitung_karyawan(orang(tanggal_berhenti="2027-02-08"), cfg())   # 30 hari sebelum
        self.assertTrue(h["berhak"])
        h = thr.hitung_karyawan(orang(tanggal_berhenti="2027-02-07"), cfg())   # 31 hari
        self.assertFalse(h["berhak"])

    def test_kebijakan_lebih_besar(self):
        h = thr.hitung_karyawan(orang(thr_kebijakan="7,5jt"), cfg())
        self.assertEqual(h["thr"], 7500000)
        h = thr.hitung_karyawan(orang(thr_kebijakan="1jt"), cfg())
        self.assertEqual(h["thr"], 5000000)
        self.assertTrue(h["peringatan"])


class TestPPh(unittest.TestCase):
    def test_pph_thr_ter(self):
        # K/0 gaji 10 jt: tanpa THR 2% = 200.000; dengan THR 10 jt -> bruto 20 jt -> TER A 9% = 1.800.000
        h = thr.hitung_karyawan(orang(ptkp="K/0", gaji_pokok="10jt", bruto_bulan_bayar="10jt"), cfg())
        p = h["pph21"]
        self.assertEqual(p["pph_tanpa_thr"], 200000)
        self.assertEqual(p["tarif_dengan_thr"], 9)
        self.assertEqual(p["pph_dengan_thr"], 1800000)
        self.assertEqual(p["tambahan_pph_thr"], 1600000)
        self.assertEqual(h["thr_setelah_pph"], 8400000)

    def test_pph_k3_kategori_c(self):
        h = thr.hitung_karyawan(orang(ptkp="K/3", gaji_pokok="5jt", bruto_bulan_bayar="5jt"), cfg())
        self.assertEqual(h["pph21"]["kategori"], "C")
        self.assertEqual(h["pph21"]["pph_tanpa_thr"], 0)

    def test_desember_tidak_pakai_ter(self):
        h = thr.hitung_karyawan(orang(ptkp="TK/0"), cfg("2026-12-25"))
        self.assertFalse(h["pph21"]["dihitung"])
        self.assertTrue(any("Masa Pajak Terakhir" in x for x in h["peringatan"]))

    def test_dtp(self):
        h = thr.hitung_karyawan(orang(ptkp="TK/0", gaji_pokok="8jt", bruto_bulan_bayar="8jt", dtp="ya"), cfg())
        self.assertTrue(h["pph21"]["dtp"])
        self.assertEqual(h["thr_setelah_pph"], h["thr"])


class TestRusak(unittest.TestCase):
    def cek(self, r):
        with self.assertRaises((thr.InputError, ValueError)):
            thr.hitung_karyawan(r, cfg())

    def test_rusak(self):
        self.cek(orang(gaji_pokok="abc"))
        self.cek(orang(tanggal_mulai="31-31-2026"))
        self.cek(orang(tanggal_mulai="2028-01-01"))
        self.cek(orang(tanggal_mulai="", masa_kerja_bulan=""))
        self.cek(orang(jenis="magang"))
        self.cek(orang(jenis="harian", upah_bulanan=""))
        self.cek(orang(ptkp="K/7"))
        self.cek(orang(nama=""))

    def test_cli(self):
        r = subprocess.run([sys.executable, os.path.join(FOLDER, "thr.py"), "--hari-raya", "2027-03-10",
                            "--nama", "Budi", "--gaji-pokok", "6jt", "--mulai", "2026-06-10", "--format", "json"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        d = json.loads(r.stdout)
        self.assertEqual(d["batas_bayar"], "2027-03-03")
        self.assertEqual(d["karyawan"][0]["thr"], 4500000)          # 9/12 x 6 jt
        r = subprocess.run([sys.executable, os.path.join(FOLDER, "thr.py"), "--hari-raya", "10 Maret",
                            "--nama", "Budi", "--gaji-pokok", "6jt", "--mulai", "2026-06-10"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)
        self.assertIn("ERROR", r.stderr)
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "thr.csv")
            r = subprocess.run([sys.executable, os.path.join(FOLDER, "thr.py"), "--hari-raya", "2027-03-10",
                                "--nama", "Budi", "--gaji-pokok", "6jt", "--mulai", "2026-06-10", "--tanggal-bayar",
                                "2027-03-05", "--csv", out], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0)
            self.assertIn("denda 5%", r.stdout)
            self.assertTrue(os.path.exists(out))


if __name__ == "__main__":
    unittest.main(verbosity=1)
