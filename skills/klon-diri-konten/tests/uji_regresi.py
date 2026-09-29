#!/usr/bin/env python3
"""Uji regresi rencana_konten_avatar.py. Jalankan: python3 tests/uji_regresi.py"""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AKAR, "scripts"))
import rencana_konten_avatar as r  # noqa: E402

SCRIPT = os.path.join(AKAR, "scripts", "rencana_konten_avatar.py")


def paket(*p):
    return r.muat_paket(list(p))


class Uji(unittest.TestCase):
    def test_kebutuhan_dan_cukup(self):
        # 12 video x 0,75 mnt x 1,25 = 11,25 menit
        mb, h = r.hitung(paket({"nama": "A", "harga_bulanan": 100000, "satuan": "menit", "batas_bulanan": 15}),
                         12, "0.75", 25, 0)
        self.assertEqual(mb, Decimal("11.25"))
        self.assertEqual(h[0]["status"], "cukup")
        self.assertEqual(h[0]["biaya_idr"], 100000)
        self.assertEqual(h[0]["sisa"], Decimal("3.75"))
        self.assertEqual(h[0]["biaya_per_menit_idr"], 8889)  # 100000/11,25 = 8888,9

    def test_kredit_dan_usd(self):
        # 10 mnt x 30 kredit = 300 <= 600; 29 USD x 16500 = 478500
        _, h = r.hitung(paket({"nama": "K", "harga_bulanan": 29, "mata_uang": "USD", "satuan": "kredit",
                               "batas_bulanan": 600, "kredit_per_menit": 30}), 10, 1, 0, 16500)
        self.assertEqual(h[0]["status"], "cukup")
        self.assertEqual(h[0]["butuh"], Decimal(300))
        self.assertEqual(h[0]["biaya_idr"], 478500)

    def test_tambahan_satuan(self):
        # butuh 8 mnt, batas 5, kurang 3 x 60000 = 180000 + 480000
        _, h = r.hitung(paket({"nama": "T", "harga_bulanan": 480000, "satuan": "menit", "batas_bulanan": 5,
                               "biaya_tambahan_per_satuan": 60000}), 8, 1, 0, 0)
        self.assertEqual(h[0]["status"], "tambah-satuan")
        self.assertEqual(h[0]["biaya_idr"], 660000)

    def test_kurang_setara_langganan(self):
        # butuh 25 mnt, batas 10 -> 3 langganan
        _, h = r.hitung(paket({"nama": "L", "harga_bulanan": 100000, "satuan": "menit", "batas_bulanan": 10}),
                        25, 1, 0, 0)
        self.assertEqual(h[0]["status"], "kurang")
        self.assertEqual(h[0]["biaya_idr"], 300000)

    def test_pembulatan_setengah_naik(self):
        self.assertEqual(r.rupiah(Decimal("100.5")), 101)
        self.assertEqual(r.rupiah(Decimal("100.4")), 100)

    def test_data_rusak(self):
        for buruk in ([], {}, [1], [{"nama": ""}], [{"nama": "x", "harga_bulanan": "abc", "batas_bulanan": 5}],
                      [{"nama": "x", "harga_bulanan": -1, "batas_bulanan": 5}],
                      [{"nama": "x", "harga_bulanan": 1, "batas_bulanan": 0}],
                      [{"nama": "x", "harga_bulanan": 1, "batas_bulanan": 5, "satuan": "jam"}],
                      [{"nama": "x", "harga_bulanan": True, "batas_bulanan": 5}],
                      [{"nama": "x", "harga_bulanan": "NaN", "batas_bulanan": 5}]):
            with self.assertRaises(r.DataBuruk, msg=repr(buruk)):
                r.muat_paket(buruk)

    def test_usd_tanpa_kurs(self):
        with self.assertRaises(r.DataBuruk):
            r.hitung(paket({"nama": "U", "harga_bulanan": 5, "mata_uang": "USD", "batas_bulanan": 5}), 1, 1, 0, 0)

    def test_parameter_buruk(self):
        p = paket({"nama": "A", "harga_bulanan": 1, "batas_bulanan": 5})
        for args in ((0, 1, 0, 0), (1, 0, 0, 0), (1, "x", 0, 0), (1, 1, -5, 0)):
            with self.assertRaises(r.DataBuruk):
                r.hitung(p, *args)

    def test_anggaran_dan_termurah(self):
        ps = paket({"nama": "Murah", "harga_bulanan": 100000, "satuan": "menit", "batas_bulanan": 5},
                   {"nama": "Mahal", "harga_bulanan": 900000, "satuan": "menit", "batas_bulanan": 30},
                   {"nama": "Pas", "harga_bulanan": 400000, "satuan": "menit", "batas_bulanan": 30})
        _, h = r.hitung(ps, 8, 1, 0, 0, 500000)
        st = {x["nama"]: x["status"] for x in h}
        self.assertEqual(st, {"Murah": "kurang", "Mahal": "lewat-anggaran", "Pas": "cukup"})

    def test_tidak_ada_yang_muat_anggaran(self):
        ps = paket({"nama": "Mahal", "harga_bulanan": 900000, "satuan": "menit", "batas_bulanan": 30})
        ok = self.cli(json.dumps([{"nama": "Mahal", "harga_bulanan": 900000, "batas_bulanan": 30}]),
                      "--video", "8", "--menit", "1", "--anggaran", "500000")
        self.assertEqual(ok.returncode, 0)
        self.assertIn("PERINGATAN", ok.stdout)
        self.assertNotIn("Termurah", ok.stdout)

    def test_angka_raksasa_galat_rapi(self):
        js = json.dumps([{"nama": "A", "harga_bulanan": 1, "batas_bulanan": 5}])
        for arg in (("--kurs", "1e999"), ("--video", "1e999"), ("--anggaran", "1e999"), ("--revisi", "1e999")):
            base = {"--video": "1", "--menit": "1"}
            base.update(dict([arg]))
            args = [x for kv in base.items() for x in kv]
            if "--kurs" in base or "--anggaran" in base:
                pass
            p = self.cli(js, *args)
            self.assertEqual(p.returncode, 2, (arg, p.stderr))
            self.assertNotIn("Traceback", p.stderr)

    def cli(self, isi, *args):
        with tempfile.TemporaryDirectory() as d:
            f = os.path.join(d, "p.json")
            with open(f, "w", encoding="utf-8") as fh:
                fh.write(isi)
            return subprocess.run([sys.executable, SCRIPT, "--paket", f, *args], capture_output=True, text=True)

    def test_cli_normal_dan_rusak(self):
        ok = self.cli(json.dumps([{"nama": "A", "harga_bulanan": 100000, "batas_bulanan": 15}]),
                      "--video", "12", "--menit", "0.75")
        self.assertEqual(ok.returncode, 0, ok.stderr)
        self.assertIn("Rp100.000", ok.stdout)
        self.assertEqual(self.cli("{bukan json", "--video", "1", "--menit", "1").returncode, 2)
        self.assertEqual(self.cli("[]", "--video", "1", "--menit", "1").returncode, 2)

    def test_contoh_berkas(self):
        f = os.path.join(AKAR, "examples", "contoh-paket.json")
        p = subprocess.run([sys.executable, SCRIPT, "--paket", f, "--video", "12", "--menit", "0.75",
                            "--kurs", "16500"], capture_output=True, text=True)
        self.assertEqual(p.returncode, 0, p.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
