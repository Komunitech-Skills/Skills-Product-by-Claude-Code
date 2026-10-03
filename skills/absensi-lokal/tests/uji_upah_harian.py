#!/usr/bin/env python3
"""Uji upah_harian.py. Jalankan: python3 tests/uji_upah_harian.py  (Windows: py tests/uji_upah_harian.py)

Pembanding independen memakai pecahan (fractions.Fraction) dan tangga pengali PP 35/2021 yang
ditulis ulang di sini (bukan diimpor dari script):
  upah sebulan = harian x 25 (pola 6) / x 21 (pola 5); upah sejam = /173
  hari kerja: jam ke-1 x1,5, berikutnya x2 (per hari)
  libur pola 6: jam 1-7 x2, jam 8 x3, jam 9-11 x4 | pola 5: jam 1-8 x2, jam 9 x3, jam 10-12 x4
  lembur minimum = jam setara x upah sebulan / 173, dibulatkan sekali (0,5 ke atas)
Kasus nyata uji gabungan 2026-10-03 (bengkel Sidoarjo): Agus 750.000 (minimum 780.694), Budi 350.000,
Cici 550.000, total 1.650.000 (minimum 1.680.694).
"""
import io
import json
import os
import random
import sys
import unittest
from contextlib import redirect_stdout
from fractions import Fraction as F

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AKAR, "scripts"))
import upah_harian as U  # noqa: E402


def bulat(fr):
    fr = F(fr)
    return int((fr * 2 + 1) // 2) if fr >= 0 else -int((-fr * 2 + 1) // 2)


def setara_kerja(j):
    j = F(j)
    return F(3, 2) * min(j, 1) + 2 * max(j - 1, 0)


def setara_libur(j, pola):
    j = F(j)
    batas = [(7, 2), (1, 3), (3, 4)] if pola == 6 else [(8, 2), (1, 3), (3, 4)]
    s, sisa = F(0), j
    for n, k in batas:
        pakai = min(sisa, n)
        s += pakai * k
        sisa -= pakai
    return s


def harapan(tarif, hari, setengah, lembur, libur, pola, tarif_lembur, tambahan, potongan):
    hadir = bulat(F(tarif) * F(hari) + F(tarif) * F(setengah) / 2)
    sebulan = tarif * (25 if pola == 6 else 21)
    st = sum((setara_kerja(j) for j in lembur), F(0)) + sum((setara_libur(j, pola) for j in libur), F(0))
    minimum = bulat(st * sebulan / 173) if st else 0
    jam = sum((F(j) for j in lembur + libur), F(0))
    bayar = bulat(jam * tarif_lembur) if (tarif_lembur is not None and jam) else minimum
    total = hadir + bayar + tambahan - potongan
    total_min = hadir + max(bayar, minimum) + tambahan - potongan
    return hadir, minimum, bayar, total, total_min


def jalankan(*argv):
    buf = io.StringIO()
    with redirect_stdout(buf):
        kode = U.main(list(argv) + ["--json"])
    return kode, json.loads(buf.getvalue())


class UjiUpahHarian(unittest.TestCase):
    def test_kasus_bengkel(self):
        kode, out = jalankan("--pola", "6", "--pekerja", "Agus; tarif=120rb; hari=6; lembur=2; tarif-lembur=15rb",
                             "--pekerja", "Budi; tarif=110rb; hari=5; kasbon=200rb",
                             "--pekerja", "Cici; tarif=100.000; hari=5; setengah=1")
        self.assertEqual(kode, 0)
        a, b, c = out["pekerja"]
        self.assertEqual((a["upah_hadir"], a["lembur_minimum_pp35"], a["lembur_dibayar"], a["total_dibayar"],
                          a["total_versi_minimum_pp35"]), (720000, 60694, 30000, 750000, 780694))
        self.assertEqual(b["total_dibayar"], 350000)
        self.assertEqual(c["total_dibayar"], 550000)
        self.assertEqual(out["total_dibayar"], 1650000)
        self.assertEqual(out["total_versi_minimum_pp35"], 1680694)
        self.assertTrue(any("DI BAWAH minimum" in p and "30.694" in p for p in out["peringatan"]))
        self.assertIn("173", out["teks"])

    def test_acak_vs_pembanding(self):
        rnd = random.Random(2026)
        for _ in range(400):
            pola = rnd.choice([5, 6])
            tarif = rnd.choice([75000, 100000, 110000, 120000, 135500, 150000, 200000])
            hari = rnd.randint(0, 6)
            setengah = rnd.randint(0, 1)
            lembur = [rnd.choice([F(1, 2), 1, F(3, 2), 2, 3, 4]) for _ in range(rnd.randint(0, 3))]
            libur = [rnd.choice([1, 3, 7, 8, 9]) for _ in range(rnd.randint(0, 1))]
            tl = rnd.choice([None, 10000, 15000, 25000, 40000])
            tambahan = rnd.choice([0, 20000])
            potongan = rnd.choice([0, 50000, 200000])

            def fj(x):
                x = F(x)
                return str(x.numerator) if x.denominator == 1 else str(float(x)).replace(".", ",")
            spek = "P; tarif=%d; hari=%d; setengah=%d; pola=%d; tambahan=%d; potongan=%d" % (
                tarif, hari, setengah, pola, tambahan, potongan)
            if lembur:
                spek += "; lembur=" + "+".join(fj(j) for j in lembur)
            if libur:
                spek += "; lembur-libur=" + "+".join(fj(j) for j in libur)
            if tl is not None:
                spek += "; tarif-lembur=%d" % tl
            kode, out = jalankan("--pekerja", spek)
            self.assertEqual(kode, 0, out)
            h = out["pekerja"][0]
            exp = harapan(tarif, hari, setengah, lembur, libur, pola, tl, tambahan, potongan)
            with self.subTest(spek=spek):
                self.assertEqual((h["upah_hadir"], h["lembur_minimum_pp35"], h["lembur_dibayar"], h["total_dibayar"],
                                  h["total_versi_minimum_pp35"]), exp)

    def test_lembur_libur_pola5_dan_batas(self):
        # pola 5, libur 10 jam: 8x2 + 1x3 + 1x4 = 23 jam setara; 200.000 x 21 = 4.200.000; 23 x 4.200.000 / 173
        kode, out = jalankan("--pola", "5", "--pekerja", "Joko; tarif=200rb; hari=0; lembur-libur=10")
        self.assertEqual(out["pekerja"][0]["lembur_minimum_pp35"], bulat(F(23 * 4200000, 173)))
        kode, out = jalankan("--pola", "6", "--pekerja", "Joko; tarif=200rb; lembur-libur=12")
        self.assertEqual(kode, 1)
        self.assertIn("melebihi", out["error"])
        kode, out = jalankan("--pekerja", "Andi; tarif=100rb; hari=6; lembur=5")
        self.assertTrue(any("4 jam/hari" in p for p in out["peringatan"]))

    def test_input_buruk_dan_csv(self):
        self.assertEqual(jalankan("--pekerja", "Andi; hari=5")[0], 1)
        self.assertEqual(jalankan("--pekerja", "Andi; tarif=abc; hari=5")[0], 1)
        self.assertEqual(jalankan("--pekerja", "Andi; gaji=100rb")[0], 1)
        self.assertEqual(jalankan("--pekerja", "Andi; tarif=100rb; pola=7")[0], 1)
        self.assertEqual(jalankan()[0], 1)
        kode, out = jalankan("--pekerja", "Andi; tarif=100rb; hari=1; potongan=300rb")
        self.assertEqual(out["total_dibayar"], -200000)
        self.assertTrue(any("lebih besar" in p for p in out["peringatan"]))
        kode, out = jalankan("--pekerja", "Andi; tarif=500rb; hari=1")
        self.assertTrue(any("PPh 21" in p for p in out["peringatan"]))
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "p.csv")
            with open(p, "w", encoding="utf-8") as f:
                f.write("nama;upah harian;hari;setengah;lembur;tarif lembur;kasbon\n"
                        "Agus;120.000;6;0;2;15.000;0\nBudi;110000;5;;;;200rb\n")
            kode, out = jalankan("--file", p)
            self.assertEqual(kode, 0, out)
            self.assertEqual(out["total_dibayar"], 750000 + 350000)


if __name__ == "__main__":
    unittest.main(verbosity=1)
