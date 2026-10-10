#!/usr/bin/env python3
"""Uji regresi nilai_usaha.py. Jalankan: python3 tests/uji_regresi.py (Windows: python / py)."""
import io
import json
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
import nilai_usaha as n  # noqa: E402


def jalan(*arg):
    o, e = io.StringIO(), io.StringIO()
    with redirect_stdout(o), redirect_stderr(e):
        k = n.main(list(arg))
    return k, o.getvalue(), e.getvalue()


class Tes(unittest.TestCase):
    def test_rp(self):
        self.assertEqual(n.rp(1250000), "Rp1.250.000")
        self.assertEqual(n.rp(Decimal("0.5")), "Rp1")
        self.assertEqual(n.rp(-2000), "-Rp2.000")

    def test_kelipatan_manual(self):
        # normalisasi: +60jt -84jt +10jt = -14jt per tahun
        k, o, _ = jalan("--laba", "2023=120000000", "2024=150000000", "2025=180000000",
                        "--kelipatan", "2", "3", "--gaji-diambil", "60000000",
                        "--gaji-pengganti", "84000000",
                        # v1.0.1: biaya sekali jalan wajib bertahun; di sini sengaja dipasang ke 3 tahun
                        "--biaya-sekali", "2023=10000000", "2024=10000000", "2025=10000000", "--json")
        self.assertEqual(k, 0)
        d = json.loads(o)
        # 106, 136, 166 jt -> rata 136jt; terakhir 166 > rata -> basis 136jt
        self.assertEqual(d["basis"], 136000000)
        self.assertEqual(d["rentang_bruto"], [272000000, 408000000])

    def test_terakhir_lebih_rendah(self):
        k, o, _ = jalan("--laba", "2023=200", "2024=200", "2025=100", "--kelipatan", "1", "2", "--json")
        d = json.loads(o)
        self.assertEqual(d["basis"], 100)
        self.assertTrue(any("terakhir" in p for p in d["peringatan"]))

    def test_aset_dan_gabungan(self):
        k, o, _ = jalan("--laba", "2025=100000000", "--kelipatan", "1", "2", "--aset", "300000000",
                        "--utang", "80000000", "--penyesuaian-aset", "20", "--diskon-pemilik", "10",
                        "--biaya-transaksi", "5", "--kebutuhan-bulanan", "10000000", "--bulan", "12", "--json")
        d = json.loads(o)
        self.assertEqual(d["aset_bersih"], 160000000)  # 300*0.8-80
        self.assertEqual(d["metode"][0]["rendah"], 90000000)  # 100jt*1*0.9
        self.assertEqual(d["metode"][0]["tinggi"], 180000000)
        self.assertEqual(d["rentang_bruto"], [90000000, 180000000])
        self.assertEqual(d["rentang_bersih"], [85500000, 171000000])
        # v1.0.1 (S1): utang 80jt dilunasi pemilik dari hasil jual -> hasil bersih 5,5jt-91jt
        self.assertEqual(d["hasil_bersih_pemilik"], [5500000, 91000000])
        self.assertEqual(d["selisih_vs_kebutuhan"], [-114500000, -29000000])

    def test_rugi_dan_utang_besar(self):
        k, o, _ = jalan("--laba", "2025=-5000000", "--kelipatan", "2", "3", "--aset", "10000000", "--utang", "30000000", "--json")
        self.assertEqual(k, 0)
        d = json.loads(o)
        self.assertLess(d["aset_bersih"], 0)
        self.assertTrue(len(d["peringatan"]) >= 2)

    def test_kelipatan_wajib(self):
        k, _, e = jalan("--laba", "2025=100")
        self.assertEqual(k, 2)
        self.assertIn("kelipatan wajib", e)

    def test_ilustrasi_diberi_label(self):
        k, o, e = jalan("--laba", "2025=1000", "--ilustrasi")
        self.assertEqual(k, 0)
        self.assertIn("ILUSTRASI", e)
        self.assertIn("ASUMSI", o)

    def test_input_rusak(self):
        for arg in (["--laba", "abc"], ["--laba", "2025=xx", "--kelipatan", "1"], ["--laba", "2025=1", "2025=2", "--kelipatan", "1"],
                    ["--laba", "2025=1", "--kelipatan", "0"], ["--laba", "2025=1", "--kelipatan", "-2"],
                    ["--aset", "-5"], ["--aset", "5", "--penyesuaian-aset", "150"], [], ["--aset", "nan"],
                    ["--aset", "5", "--bulan", "12"]):
            k, _, e = jalan(*arg)
            self.assertEqual(k, 2, arg)
            self.assertIn("GAGAL", e)

    def test_hanya_aset(self):
        k, o, _ = jalan("--aset", "50000000", "--utang", "10000000")
        self.assertEqual(k, 0)
        self.assertIn("Rp40.000.000", o)

    # ---- v1.0.1 ----
    WARUNG = ("--laba", "2023=84000000", "2024=97000000", "2025=91000000", "--kelipatan", "2", "3",
              "--aset", "65000000", "--utang", "18000000", "--penyesuaian-aset", "25",
              "--gaji-diambil", "36000000", "--gaji-pengganti", "42000000", "--diskon-pemilik", "20",
              "--biaya-transaksi", "4", "--kebutuhan-bulanan", "6000000", "--bulan", "18", "--json")

    def test_t1_biaya_sekali_hanya_tahunnya(self):
        k, o, _ = jalan(*self.WARUNG, "--biaya-sekali", "2024=12000000")
        self.assertEqual(k, 0)
        d = json.loads(o)
        # hitung ulang independen dengan Decimal
        D = Decimal
        norm = [D(84000000) - 6000000, D(97000000) - 6000000 + 12000000, D(91000000) - 6000000]
        basis = min(sum(norm) / 3, norm[-1])
        lo, hi = basis * 2 * D("0.8"), basis * 3 * D("0.8")
        bersih = [lo * D("0.96") - 18000000, hi * D("0.96") - 18000000]
        self.assertEqual(list(d["laba_normalisasi"].values()), [int(x) for x in norm])  # 78/103/85 jt
        self.assertEqual(d["basis"], int(basis))  # 85 jt (tahun terakhir lebih rendah)
        self.assertEqual(d["rentang_bruto"], [int(lo), int(hi)])  # 136-204 jt (dulu s/d 232 jt)
        self.assertEqual(d["hasil_bersih_pemilik"], [int(x) for x in bersih])  # 112,56-177,84 jt
        self.assertEqual(d["selisih_vs_kebutuhan"], [int(x - 108000000) for x in bersih])
        self.assertTrue(any("terakhir" in p for p in d["peringatan"]))
        self.assertEqual(d["biaya_sekali"], {"2024": 12000000})

    def test_biaya_sekali_aturan_input(self):
        # angka tanpa tahun + beberapa tahun laba -> ditolak jelas
        k, _, e = jalan("--laba", "2024=100", "2025=100", "--kelipatan", "1", "--biaya-sekali", "50")
        self.assertEqual(k, 2)
        self.assertIn("tahun", e)
        # angka tanpa tahun + tepat satu tahun laba -> dipasang ke tahun itu
        k, o, _ = jalan("--laba", "2025=100", "--kelipatan", "1", "--biaya-sekali", "50", "--json")
        self.assertEqual(json.loads(o)["laba_normalisasi"], {"2025": 150})
        # tahun tidak ada di --laba -> ditolak
        k, _, e = jalan("--laba", "2025=100", "--kelipatan", "1", "--biaya-sekali", "2023=50")
        self.assertEqual(k, 2)
        # diulang & tahun sama dijumlahkan; tahun lama di luar 3 tahun -> peringatan
        k, o, _ = jalan("--laba", "2021=100", "2023=100", "2024=100", "2025=100", "--kelipatan", "1",
                        "--biaya-sekali", "2024=10", "--biaya-sekali", "2024=5", "2021=7", "--json")
        d = json.loads(o)
        self.assertEqual(d["laba_normalisasi"], {"2023": 100, "2024": 115, "2025": 100})
        self.assertTrue(any("2021" in p for p in d["peringatan"]))
        # tanpa --laba -> ditolak
        k, _, e = jalan("--aset", "100", "--biaya-sekali", "2025=5")
        self.assertEqual(k, 2)

    def test_s1_utang_sekali_di_kedua_metode(self):
        # hanya aset: nilai sebelum utang 100, utang 30 dilunasi -> hasil bersih 70 (bukan 70 lalu dikurangi lagi)
        k, o, _ = jalan("--aset", "100", "--utang", "30", "--json")
        d = json.loads(o)
        self.assertEqual(d["rentang_bruto"], [100, 100])
        self.assertEqual(d["hasil_bersih_pemilik"], [70, 70])
        # utang ikut pembeli: harga turun, pemilik tidak melunasi lagi
        k, o, _ = jalan("--laba", "2025=100", "--kelipatan", "2", "3", "--utang", "50", "--utang-ikut", "--json")
        d = json.loads(o)
        self.assertEqual(d["harga"], [150, 250])
        self.assertEqual(d["hasil_bersih_pemilik"], [150, 250])
        # default: utang dilunasi dari hasil jual -> harga tetap, hasil bersih berkurang
        k, o, _ = jalan("--laba", "2025=100", "--kelipatan", "2", "3", "--utang", "50", "--json")
        d = json.loads(o)
        self.assertEqual(d["harga"], [200, 300])
        self.assertEqual(d["hasil_bersih_pemilik"], [150, 250])

    def test_s4_porsi_sekutu(self):
        k, o, _ = jalan("--laba", "2024=240000000", "2025=270000000", "--kelipatan", "2", "2.5",
                        "--aset", "180000000", "--utang", "60000000", "--penyesuaian-aset", "20",
                        "--gaji-diambil", "84000000", "--gaji-pengganti", "72000000",
                        "--biaya-transaksi", "3", "--porsi", "40", "--json")
        self.assertEqual(k, 0)
        d = json.loads(o)
        D = Decimal
        basis = (D(252000000) + D(282000000)) / 2  # 267 jt; terakhir 282 jt lebih tinggi
        harga = [(basis * D(x) - 60000000) * D("0.4") for x in ("2", "2.5")]
        self.assertTrue(d["utang_ikut"])  # sebagian -> utang tetap di badan usaha
        self.assertEqual(d["harga"], [int(h) for h in harga])  # 189,6-243 jt
        self.assertEqual(d["rentang_bersih"], [int(h * D("0.97")) for h in harga])
        for arg in (["--porsi", "0"], ["--porsi", "150"]):
            k, _, e = jalan("--aset", "100", *arg)
            self.assertEqual(k, 2, arg)

    def test_r1_biaya_tidak_dari_negatif(self):
        k, o, _ = jalan("--aset", "10000000", "--utang", "30000000", "--biaya-transaksi", "10", "--utang-ikut", "--json")
        d = json.loads(o)
        self.assertEqual(d["rentang_bersih"], [-20000000, -20000000])  # dulu -18 jt
        self.assertTrue(any("negatif" in p for p in d["peringatan"]))

    def test_r2_r3_r6_pesan_jelas(self):
        k, _, e = jalan("--laba", "2025=1000000", "--kelipatan", "2", "--gaji-pengganti", "5000000")
        self.assertEqual(k, 2)
        self.assertIn("nol/negatif", e)
        for arg in (["--aset", "1e400"], ["--laba", "0000=5", "--kelipatan", "1"], ["--laba", "2025=1e20", "--kelipatan", "1"]):
            k, _, e = jalan(*arg)
            self.assertEqual(k, 2, arg)
            self.assertIn("GAGAL", e)


if __name__ == "__main__":
    unittest.main()
