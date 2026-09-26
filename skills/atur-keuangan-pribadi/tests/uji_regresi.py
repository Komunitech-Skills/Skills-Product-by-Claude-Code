#!/usr/bin/env python3
"""Uji regresi scripts/keuangan.py — jalankan dengan:
    python3 tests/uji_regresi.py
(Windows: python atau py). Hanya pustaka standar (unittest).

Angka diverifikasi INDEPENDEN memakai fractions.Fraction (aritmetika pecahan persis),
ditulis terpisah dari logika Decimal di script — bukan memanggil fungsi yang sama.
"""
import math
import random
import subprocess
import sys
import unittest
from decimal import Decimal
from fractions import Fraction as F
from pathlib import Path

FOLDER = Path(__file__).resolve().parent.parent
SCRIPT = FOLDER / "scripts" / "keuangan.py"
sys.path.insert(0, str(FOLDER / "scripts"))

import keuangan as k  # noqa: E402


# ---------------------------------------------------------------------------
# Implementasi pembanding independen (Fraction)
# ---------------------------------------------------------------------------

def f_bulat(x):
    """Rupiah terdekat, setengah ke atas (x >= 0)."""
    return F(math.floor(x + F(1, 2)))


def f_ceil(x):
    return F(math.ceil(x))


def f_simulasi(utang, anggaran, metode):
    """utang: list (nama, saldo F, bunga_bulanan F, minimum F). Kembalikan (bulan, total_bunga, lunas)."""
    saldo = [u[1] for u in utang]
    n = len(utang)
    if metode == "avalanche":
        urut = sorted(range(n), key=lambda i: (-utang[i][2], utang[i][1], i))
    else:
        urut = sorted(range(n), key=lambda i: (utang[i][1], -utang[i][2], i))
    total_bunga = F(0)
    lunas = [None] * n
    bulan = 0
    while any(s > 0 for s in saldo):
        bulan += 1
        if bulan > 600:
            return None, total_bunga, lunas
        awal = sum(saldo)
        for i in range(n):
            if saldo[i] > 0:
                b = f_bulat(saldo[i] * utang[i][2])
                saldo[i] += b
                total_bunga += b
        sisa = anggaran
        for i in urut:
            if saldo[i] > 0:
                x = min(utang[i][3], saldo[i], sisa)
                saldo[i] -= x
                sisa -= x
        for i in urut:
            if saldo[i] > 0 and sisa > 0:
                x = min(sisa, saldo[i])
                saldo[i] -= x
                sisa -= x
        for i in range(n):
            if saldo[i] == 0 and lunas[i] is None:
                lunas[i] = bulan
        if any(s > 0 for s in saldo) and sum(saldo) >= awal:
            return None, total_bunga, lunas
    return bulan, total_bunga, lunas


def f_target(biaya, bulan, inflasi_pct, imbal_pct, terkumpul):
    i = F(inflasi_pct) / 1200
    r = F(imbal_pct) / 1200
    nanti = f_bulat(biaya * (1 + i) ** bulan)
    tumbuh = terkumpul * (1 + r) ** bulan
    kurang = nanti - tumbuh
    if kurang <= 0:
        return nanti, 0
    pmt = kurang / bulan if r == 0 else kurang * r / ((1 + r) ** bulan - 1)
    return nanti, f_ceil(pmt)


def jalankan(*argumen):
    return subprocess.run([sys.executable, str(SCRIPT)] + list(argumen),
                          capture_output=True, text=True, encoding="utf-8")


def utang_script(spesifikasi):
    return [k.parse_utang(s) for s in spesifikasi]


# ---------------------------------------------------------------------------
# Tes parsing
# ---------------------------------------------------------------------------

class TesParseRupiah(unittest.TestCase):
    KASUS = {
        "Rp1.500.000": 1500000, "Rp 1.500.000": 1500000, "1500000": 1500000, "1,5jt": 1500000,
        "1.5jt": 1500000, "1,5 juta": 1500000, "750rb": 750000, "750 ribu": 750000, "750k": 750000,
        "2 juta": 2000000, "Rp1.500.000,-": 1500000, "IDR 2.000.000": 2000000, "1.250.000,50": Decimal("1250000.50"),
        "1,500,000": 1500000, "2,25jt": 2250000, "1,2 miliar": 1200000000, "0": 0, "Rp.500.000": 500000,
        "12.5rb": 12500,
    }

    def test_format_benar(self):
        for teks, harap in self.KASUS.items():
            with self.subTest(teks=teks):
                self.assertEqual(k.parse_rupiah(teks), Decimal(harap))

    def test_format_salah(self):
        for teks in ["abc", "", "-5jt", "Rp-100", "1.5", "1,5M", "10M", "1..5jt", "jt", "1,5,5jt", None]:
            with self.subTest(teks=teks):
                with self.assertRaises(k.InputSalah):
                    k.parse_rupiah(teks)

    def test_nol_ditolak_bila_diminta(self):
        with self.assertRaises(k.InputSalah):
            k.parse_rupiah("0", boleh_nol=False)


class TesParseBunga(unittest.TestCase):
    def test_periode(self):
        self.assertEqual(k.parse_bunga("24%").per_bulan_persen(), Decimal(2))
        self.assertEqual(k.parse_bunga("24%/th").per_bulan_persen(), Decimal(2))
        self.assertEqual(k.parse_bunga("1,75%/bln").per_bulan_persen(), Decimal("1.75"))
        self.assertEqual(k.parse_bunga("0,1%/hari").per_bulan_persen(), Decimal(3))
        self.assertEqual(k.parse_bunga("12 per tahun").per_bulan_persen(), Decimal(1))
        self.assertEqual(k.parse_bunga("0%").per_bulan_persen(), Decimal(0))

    def test_bunga_dari_saldo_dibulatkan_setengah_ke_atas(self):
        # 13%/th x 1.000.000 / 12 = 10.833,33.. -> 10.833 ; 6%/th x 100.100 /12 = 500,5 -> 501
        self.assertEqual(k.parse_bunga("13%").bunga_dari(Decimal(1000000)), Decimal(10833))
        self.assertEqual(k.parse_bunga("6%").bunga_dari(Decimal(100100)), Decimal(501))

    def test_salah(self):
        for teks in ["-2%", "abc", "", "2%%x", "60%/bln", "5%/hari"]:
            with self.subTest(teks=teks):
                with self.assertRaises(k.InputSalah):
                    k.parse_bunga(teks)


# ---------------------------------------------------------------------------
# Tes utang (avalanche/snowball) diverifikasi dengan Fraction
# ---------------------------------------------------------------------------

def ke_fraction(u):
    return (u.nama, F(str(u.saldo)), F(str(u.bunga.per_bulan_persen())) / 100, F(str(u.minimum)))


class TesUtang(unittest.TestCase):
    SPEK = ["Kartu kredit;12jt;1,75%/bln;600rb;kk", "Pinjol;1,5jt;0,1%/hari;400rb;pinjol",
            "KTA;20jt;11%/th;700rb;kta", "Paylater;3jt;2,5%/bln;200rb;paylater"]

    def banding_fraction(self, spek, anggaran):
        daftar = utang_script(spek)
        for metode in ("avalanche", "snowball"):
            h = k.simulasi(daftar, anggaran, metode)
            fb, fbunga, flunas = f_simulasi([ke_fraction(u) for u in daftar], F(str(anggaran)), metode)
            with self.subTest(metode=metode, spek=spek):
                self.assertEqual(h["bulan"], fb)
                self.assertEqual(F(str(h["total_bunga"])), fbunga)
                self.assertEqual(h["lunas"], flunas)

    def test_kasus_utama(self):
        daftar = utang_script(self.SPEK)
        anggaran = sum(u.minimum for u in daftar) + Decimal(1000000)
        self.banding_fraction(self.SPEK, anggaran)

    def test_avalanche_tidak_lebih_mahal_acak(self):
        rnd = random.Random(20260926)
        for _ in range(40):
            spek = []
            for j in range(rnd.randint(1, 4)):
                saldo = rnd.randint(5, 400) * 100000
                bunga = rnd.choice(["0%", "1%/bln", "1,75%/bln", "2,5%/bln", "12%", "18%", "0,1%/hari"])
                minimum = rnd.randint(1, 20) * 50000
                spek.append("U{};{};{};{}".format(j, saldo, bunga, minimum))
            daftar = utang_script(spek)
            anggaran = sum(u.minimum for u in daftar) + rnd.randint(0, 30) * 100000
            self.banding_fraction(spek, anggaran)
            a = k.simulasi(daftar, anggaran, "avalanche")
            s = k.simulasi(daftar, anggaran, "snowball")
            if a["bulan"] is not None and s["bulan"] is not None:
                # toleransi Rp jumlah bulan x jumlah utang karena pembulatan bunga per bulan
                self.assertLessEqual(a["total_bunga"], s["total_bunga"] + a["bulan"] * len(daftar))

    def test_satu_utang_hitungan_manual(self):
        # 1.000.000, 2%/bln, bayar 300.000: bunga 20.000, 14.400, 8.688, 2.862 -> lunas bulan 4
        daftar = utang_script(["A;1jt;2%/bln;300rb"])
        h = k.simulasi(daftar, Decimal(300000), "avalanche")
        self.assertEqual(h["bulan"], 4)
        self.assertEqual(h["total_bunga"], Decimal(20000 + 14400 + 8688 + 2862))

    def test_bunga_nol(self):
        daftar = utang_script(["Utang ke kakak;2jt;0%;500rb;keluarga"])
        h = k.simulasi(daftar, Decimal(500000), "snowball")
        self.assertEqual((h["bulan"], h["total_bunga"]), (4, Decimal(0)))

    def test_minimum_di_bawah_bunga_diberi_peringatan_dan_macet(self):
        daftar = utang_script(["KK;5jt;3%/bln;150rb"])
        per = " ".join(k.peringatan_utang(daftar, Decimal(150000)))
        self.assertIn("tidak akan pernah lunas", per)
        h = k.simulasi(daftar, Decimal(150000), "avalanche")
        self.assertIsNone(h["bulan"])
        self.assertTrue(h["macet"])

    def test_peringatan_pinjol_ilegal_dan_kk(self):
        per = " ".join(k.peringatan_utang(utang_script(["X;3jt;0,4%/hari;1,5jt;pinjol", "KK;5jt;2,5%/bln;1jt;kk"]),
                                          Decimal(2500000)))
        self.assertIn("PINJOL ILEGAL", per)
        self.assertIn("157", per)
        self.assertIn("1,75%/bulan", per)

    def test_cli_anggaran_kurang_dari_minimum(self):
        r = jalankan("utang", "--utang", "KK;5jt;2%/bln;300rb", "--anggaran", "100rb")
        self.assertEqual(r.returncode, 2)
        self.assertIn("lebih kecil dari total cicilan minimum", r.stderr)


# ---------------------------------------------------------------------------
# Konversi flat -> efektif
# ---------------------------------------------------------------------------

class TesKonversiFlat(unittest.TestCase):
    def test_nilai_dikenal(self):
        # Rp10 jt, flat 10%/th, 12 bulan -> efektif ~17,97%/th (angka umum di literatur)
        r = k.cari_bunga_efektif_bulanan(Decimal(10000000), Decimal(916667), 12)
        self.assertEqual((r * 1200).quantize(Decimal("0.01")), Decimal("17.97"))

    def test_verifikasi_fraction(self):
        for pokok, flat, n in [(18000000, 12, 24), (25000000, 8, 36), (5000000, 20, 6), (150000000, 5, 60)]:
            cicilan = f_bulat(F(pokok) / n + F(pokok) * flat / 1200)
            r = k.cari_bunga_efektif_bulanan(Decimal(pokok), Decimal(int(cicilan)), n)
            rf = F(str(r))
            pv = cicilan * (1 - (1 + rf) ** (-n)) / rf
            with self.subTest(pokok=pokok):
                self.assertLess(abs(pv - pokok), F(1, 100))

    def test_cli_cicilan_flat(self):
        r = jalankan("konversi-flat", "--pokok", "18jt", "--bunga-flat", "12", "--tenor", "24")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("Rp930.000", r.stdout)   # 750.000 + 180.000

    def test_cli_input_buruk(self):
        for argumen in (["--pokok", "0", "--tenor", "12", "--bunga-flat", "5"],
                        ["--pokok", "10jt", "--tenor", "0", "--bunga-flat", "5"],
                        ["--pokok", "10jt", "--tenor", "12"],
                        ["--pokok", "10jt", "--tenor", "12", "--cicilan", "500rb"],
                        ["--pokok", "10jt", "--tenor", "12", "--bunga-flat", "5", "--sudah-bayar", "12"]):
            r = jalankan("konversi-flat", *argumen)
            with self.subTest(argumen=argumen):
                self.assertEqual(r.returncode, 2)
                self.assertNotIn("Traceback", r.stderr)


# ---------------------------------------------------------------------------
# Target keuangan
# ---------------------------------------------------------------------------

class TesTarget(unittest.TestCase):
    def test_banding_fraction(self):
        kasus = [(60000000, 60, 4, 5, 10000000), (1440000000, 300, 4, 6, 0), (35000000, 36, 3, 0, 0),
                 (120000000, 144, 10, 4, 5000000), (5000000, 12, 0, 0, 5000000), (20000000, 1, 4, 5, 0)]
        for biaya, bulan, inf, imb, tk in kasus:
            nanti, _, pmt = k.hitung_target(Decimal(biaya), bulan, Decimal(inf), Decimal(imb), Decimal(tk))
            fn, fp = f_target(F(biaya), bulan, inf, imb, F(tk))
            with self.subTest(biaya=biaya, bulan=bulan):
                self.assertEqual(F(str(nanti)), fn)
                self.assertEqual(F(str(pmt)), fp)

    def test_tanpa_inflasi_tanpa_imbal(self):
        _, _, pmt = k.hitung_target(Decimal(12000000), 12, Decimal(0), Decimal(0), Decimal(0))
        self.assertEqual(pmt, Decimal(1000000))

    def test_cli_kemampuan_kurang(self):
        r = jalankan("target", "--nama", "DP rumah", "--biaya-sekarang", "60jt", "--tahun", "5",
                     "--inflasi", "4", "--imbal", "5", "--terkumpul", "10jt", "--kemampuan", "700rb")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("Kurang", r.stdout)
        self.assertIn("Bukan nasihat keuangan", r.stdout)

    def test_cli_pensiun(self):
        r = jalankan("target", "--jenis", "pensiun", "--pengeluaran-bulanan", "6jt", "--tahun", "25")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("Rp1.440.000.000", r.stdout)


# ---------------------------------------------------------------------------
# Anggaran & dana darurat
# ---------------------------------------------------------------------------

class TesAnggaran(unittest.TestCase):
    def test_musiman_dibagi_12_dibulatkan_ke_bawah(self):
        h = k.hitung_anggaran([("Gaji", Decimal(7500000))], [("THR", Decimal(7500000)), ("Bonus", Decimal(5000000))],
                              [], [Decimal(50), Decimal(30), Decimal(20)])
        self.assertEqual(h["musiman_per_bulan"], Decimal(1041666))   # 12.500.000/12 = 1.041.666,67
        self.assertEqual(h["total_masuk"], Decimal(8541666))

    def test_zero_based_dan_kelompok(self):
        pos = [k.parse_pos(p) for p in ["Kontrakan=2jt", "Kiriman ortu=1jt", "Zakat=200rb", "Cicilan motor=900rb",
                                        "Nongkrong=500rb", "Dana darurat=1,4jt", "Arisan=0"]]
        h = k.hitung_anggaran([("Gaji", Decimal(6000000))], [], pos, [Decimal(50), Decimal(30), Decimal(20)])
        self.assertEqual(h["sisa"], Decimal(0))
        self.assertEqual(h["kebutuhan"], Decimal(4100000))
        self.assertEqual(h["keinginan"], Decimal(500000))
        self.assertEqual(h["tabungan"], Decimal(1400000))
        self.assertEqual(h["cicilan"], Decimal(900000))
        self.assertEqual(h["target_pola"], [Decimal(3000000), Decimal(1800000), Decimal(1200000)])

    def test_tebak_kelompok(self):
        self.assertEqual(k.tebak_kelompok("Kiriman orang tua"), "sosial")
        self.assertEqual(k.tebak_kelompok("Perpuluhan gereja"), "sosial")
        self.assertEqual(k.tebak_kelompok("Dana darurat"), "tabungan")
        self.assertEqual(k.tebak_kelompok("Listrik token"), "wajib")
        self.assertEqual(k.tebak_kelompok("Netflix"), "keinginan")
        self.assertEqual(k.tebak_kelompok("Hadiah ulang tahun"), "lain")

    def test_label_eksplisit_menang(self):
        self.assertEqual(k.parse_pos("Kopi kantor=300rb:wajib")[2], "wajib")

    def test_cli_defisit_dan_ewallet(self):
        r = jalankan("anggaran", "--pemasukan", "Gaji=4jt", "--pos", "Kos=2,5jt", "--pos", "Makan=2jt",
                     "--pos", "Top up OVO=300rb")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("DEFISIT", r.stdout)
        self.assertIn("gali lubang", r.stdout)
        self.assertIn("TOP-UP e-wallet", r.stdout)

    def test_cli_rasio_cicilan_tinggi(self):
        r = jalankan("anggaran", "--pemasukan", "Gaji=5jt", "--pos", "Cicilan KPR=1,8jt", "--pos", "Paylater=500rb")
        self.assertIn("DI ATAS patokan umum 30%", r.stdout)


class TesDanaDarurat(unittest.TestCase):
    def test_hitung(self):
        ket, h = k.hitung_dana_darurat(Decimal(4500000), "anak", Decimal(6000000), Decimal(750000))
        self.assertEqual([x["bulan"] for x in h], [9, 12])
        self.assertEqual(h[0]["target"], Decimal(40500000))
        self.assertEqual(h[0]["lama"], math.ceil(F(34500000, 750000)))   # 46
        self.assertEqual(h[1]["lama"], 64)

    def test_lepas_12_bulan_dan_sudah_tercapai(self):
        _, h = k.hitung_dana_darurat(Decimal(3000000), "lepas", Decimal(40000000), Decimal(0))
        self.assertEqual(len(h), 1)
        self.assertEqual(h[0]["lama"], 0)

    def test_setoran_nol(self):
        _, h = k.hitung_dana_darurat(Decimal(3000000), "lajang", Decimal(0), Decimal(0))
        self.assertIsNone(h[0]["lama"])


# ---------------------------------------------------------------------------
# Input buruk: tidak boleh ada traceback
# ---------------------------------------------------------------------------

class TesInputBuruk(unittest.TestCase):
    KASUS = [
        ["utang", "--utang", "KK;5jt;-2%;300rb"],
        ["utang", "--utang", "KK;5jt;2%/bln"],
        ["utang", "--utang", "KK;abc;2%/bln;300rb"],
        ["utang", "--utang", "KK;5jt;2%/bln;0"],
        ["utang", "--utang", "KK;5jt;2%/bln;300rb;rentenir"],
        ["utang", "--utang", "KK;5jt;2%/bln;300rb", "--ekstra", "-100rb"],
        ["utang", "--utang", "KK;5jt;2%/bln;300rb", "--ekstra", "1jt", "--anggaran", "2jt"],
        ["utang"],
        ["anggaran"],
        ["anggaran", "--pemasukan", "Gaji=lima juta"],
        ["anggaran", "--pemasukan", "5jt", "--pos", "Kontrakan 1jt"],
        ["anggaran", "--pemasukan", "5jt", "--pola", "50/30/30"],
        ["anggaran", "--pemasukan", "5M"],
        ["dana-darurat", "--pengeluaran-pokok", "0", "--status", "lajang"],
        ["dana-darurat", "--pengeluaran-pokok", "3jt", "--status", "bujang"],
        ["dana-darurat", "--pengeluaran-pokok", "3jt"],
        ["target", "--biaya-sekarang", "10jt"],
        ["target", "--biaya-sekarang", "10jt", "--tahun", "3", "--inflasi", "-2"],
        ["target", "--biaya-sekarang", "10jt", "--tahun", "tiga"],
        ["target", "--biaya-sekarang", "10jt", "--tahun", "3", "--bulan", "36"],
        ["target", "--jenis", "pensiun", "--tahun", "20"],
        ["target", "--biaya-sekarang", "10jt", "--tahun", "3", "--imbal", "80"],
        [],
        ["hitung-semua"],
    ]

    def test_tanpa_traceback(self):
        for argumen in self.KASUS:
            r = jalankan(*argumen)
            with self.subTest(argumen=argumen):
                self.assertNotEqual(r.returncode, 0)
                self.assertNotIn("Traceback", r.stderr + r.stdout)
                self.assertIn("Input belum benar", r.stderr)


class TesStrukturSkill(unittest.TestCase):
    def test_frontmatter_dua_field(self):
        teks = (FOLDER / "SKILL.md").read_text(encoding="utf-8")
        fm = teks.split("---")[1].strip().splitlines()
        self.assertEqual([b.split(":")[0] for b in fm], ["name", "description"])
        self.assertLess(len(teks.splitlines()), 300)

    def test_rujukan_ojk_konsisten(self):
        ref = (FOLDER / "references" / "utang-dan-pinjol.md").read_text(encoding="utf-8")
        self.assertIn("157", ref)
        self.assertIn("081-157-157-157", ref)


if __name__ == "__main__":
    unittest.main(verbosity=1)
