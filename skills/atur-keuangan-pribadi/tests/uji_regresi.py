#!/usr/bin/env python3
"""Uji regresi scripts/keuangan.py — jalankan dengan:
    python3 tests/uji_regresi.py
(Windows: python atau py). Hanya pustaka standar (unittest).

Angka diverifikasi INDEPENDEN memakai fractions.Fraction (aritmetika pecahan persis),
ditulis terpisah dari logika Decimal di script — bukan memanggil fungsi yang sama.
"""
import math
import random
import re
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


class TesCicilanMasukPokok(unittest.TestCase):
    """v1.0.5 (uji OpenClaw 2026-10-01 skenario 02): cicilan PayLater/KK/KPR/pinjol wajib masuk
    pengeluaran pokok untuk dasar dana darurat (dulu PayLater Rp650rb terlewat -> target kurang +-Rp5,85 jt)."""

    POS = ["Kontrakan=2jt", "Cicilan motor=1,15jt", "Shopee PayLater=650rb", "Belanja dapur=1.787.500",
           "Token listrik=350rb", "SPP PAUD=350rb", "Pulsa=150rb", "Bensin=120rb", "Kiriman ibu=1jt",
           "Arisan RT=500rb", "Dana darurat=750rb", "Jajan=692.500:keinginan"]

    def test_anggaran_pokok_termasuk_semua_cicilan(self):
        pos = [k.parse_pos(p) for p in self.POS]
        h = k.hitung_anggaran([("Gaji", Decimal(9500000))], [], pos, [Decimal(50), Decimal(30), Decimal(20)])
        # independen: wajib 2.000.000+1.150.000+650.000+1.787.500+350.000+350.000+150.000+120.000
        # + v1.0.6 kewajiban rutin keluarga (Kiriman ibu 1.000.000)
        self.assertEqual(h["pokok_dana_darurat"], Decimal(sum([2000000, 1150000, 650000, 1787500, 350000,
                                                                350000, 150000, 120000, 1000000])))
        self.assertIn("Shopee PayLater", [n for n, _, _ in h["pokok_rinci"]])

    def test_cicilan_berlabel_lain_tetap_pokok_tapi_ekstra_tidak(self):
        pos = [k.parse_pos(p) for p in ["Kos=1jt", "Paylater=300rb:keinginan", "Kartu kredit=400rb:tabungan",
                                        "Ekstra utang KK=500rb", "KPR=2jt", "Pinjol=250rb"]]
        h = k.hitung_anggaran([("Gaji", Decimal(8000000))], [], pos, [Decimal(50), Decimal(30), Decimal(20)])
        self.assertEqual(h["pokok_dana_darurat"], Decimal(1000000 + 300000 + 400000 + 2000000 + 250000))

    def test_cli_anggaran_menampilkan_dasar_dana_darurat(self):
        argumen = ["anggaran", "--pemasukan", "Gaji=9,5jt"]
        for p in self.POS:
            argumen += ["--pos", p]
        r = jalankan(*argumen)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("Dasar dana darurat", r.stdout)
        self.assertIn("| Shopee PayLater | cicilan/utang minimum |", r.stdout)
        self.assertIn("--pengeluaran-pokok 7557500 ", r.stdout)

    def test_cli_dana_darurat_dengan_cicilan(self):
        r = jalankan("dana-darurat", "--pengeluaran-pokok", "6.907.500", "--cicilan", "PayLater=650rb",
                     "--status", "anak", "--saldo", "4jt", "--setoran", "750rb")
        self.assertEqual(r.returncode, 0, r.stderr)
        pokok = 6907500 + 650000
        self.assertIn(k.rp(Decimal(pokok)), r.stdout)
        self.assertIn(k.rp(Decimal(pokok * 9)), r.stdout)          # Rp68.017.500
        self.assertIn("{} bulan".format(math.ceil(F(pokok * 9 - 4000000, 750000))), r.stdout)
        self.assertNotIn("CEK CICILAN", r.stdout)

    def test_cli_dana_darurat_tanpa_cicilan_diingatkan(self):
        r = jalankan("dana-darurat", "--pengeluaran-pokok", "5jt", "--status", "lajang")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("CEK CICILAN", r.stdout)

    def test_cli_dana_darurat_hanya_rincian(self):
        r = jalankan("dana-darurat", "--pos", "Kontrakan=2jt", "--cicilan", "KPR=3jt", "--status", "lajang")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("Rp15.000.000", r.stdout)   # 5 jt x 3 bulan



class TesUji02KirimanKeluargaMasukPokok(unittest.TestCase):
    """v1.0.6 (uji ulang OpenClaw 2026-10-01 skenario 02, data mutasi-september.csv): kiriman ortu Rp1 jt
    dulu keluar dari pokok diam-diam -> dasar Rp6.282.500, target 9 bln Rp56.542.500 (kekecilan Rp9 jt).
    Angka benar dihitung ulang dengan python (Fraction) terpisah dari script:
      pokok = 2.000.000 + 1.150.000 + 650.000 + 500.000 + 350.000 + 1.500.000 + 132.500 + 1.000.000 = 7.282.500
      9 bln = 65.542.500 ; 12 bln = 87.390.000 ; saldo 4 jt, setor 717.500 -> ceil(61.542.500/717.500) = 86 bln
    """

    POS = ["Kontrakan=2jt", "Cicilan motor Adira=1,15jt", "Shopee PayLater=650rb", "Token PLN + Pulsa=500rb",
           "SPP PAUD=350rb", "Belanja bulanan & dapur=1,5jt", "Bensin + admin bank=132.500:wajib",
           "Kiriman ortu=1jt", "Arisan RT=500rb", "Jajan e-wallet QRIS=2.185.500:keinginan",
           "Top-up Indodax=2,5jt"]
    POKOK = F(2000000 + 1150000 + 650000 + 500000 + 350000 + 1500000 + 132500 + 1000000)

    def argumen(self, *tambahan):
        a = ["anggaran", "--pemasukan", "Gaji=9,5jt"]
        for p in self.POS:
            a += ["--pos", p]
        return a + list(tambahan)

    def test_pokok_uji02(self):
        self.assertEqual(self.POKOK, 7282500)
        r = jalankan(*self.argumen())
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("| Kiriman ortu | kewajiban rutin keluarga | Rp1.000.000 |", r.stdout)
        self.assertIn("| Shopee PayLater | cicilan/utang minimum | Rp650.000 |", r.stdout)
        self.assertIn("**Total pengeluaran pokok** | | **Rp7.282.500**", r.stdout)
        self.assertIn("--pengeluaran-pokok 7282500 ", r.stdout)
        # pos yang dikeluarkan WAJIB tercetak beserta alasannya
        bagian = r.stdout.split("Pos DIKELUARKAN dari pokok", 1)[1]
        for nama in ("Arisan RT", "Jajan e-wallet QRIS", "Top-up Indodax"):
            self.assertRegex(bagian, r"\| {} \| Rp[0-9.]+ \| [a-z]".format(re.escape(nama)))
        self.assertNotIn("Kiriman ortu", bagian.split("- Pokok =")[0])

    def test_target_dana_darurat_uji02(self):
        r = jalankan("dana-darurat", "--pos", "Kontrakan=2jt", "--pos", "Token PLN + Pulsa=500rb",
                     "--pos", "SPP PAUD=350rb", "--pos", "Belanja bulanan & dapur=1,5jt",
                     "--pos", "Bensin + admin bank=132.500", "--cicilan", "Motor=1,15jt",
                     "--cicilan", "PayLater=650rb", "--keluarga", "Kiriman ortu=1jt",
                     "--dikeluarkan", "Top-up Indodax=2,5jt;top-up investasi, bisa dihentikan",
                     "--status", "anak", "--saldo", "4jt", "--setoran", "717500")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("Rp7.282.500", r.stdout)
        self.assertIn(k.rp(Decimal(int(self.POKOK * 9))), r.stdout)      # Rp65.542.500
        self.assertIn(k.rp(Decimal(int(self.POKOK * 12))), r.stdout)     # Rp87.390.000
        self.assertIn("Rp65.542.500", r.stdout)
        self.assertIn("Rp87.390.000", r.stdout)
        self.assertIn("{} bulan".format(math.ceil((self.POKOK * 9 - 4000000) / 717500)), r.stdout)  # 86
        self.assertIn("Kiriman ortu (kewajiban keluarga)", r.stdout)
        self.assertIn("| Top-up Indodax | Rp2.500.000 | top-up investasi, bisa dihentikan |", r.stdout)
        self.assertNotIn("CEK KIRIMAN KELUARGA", r.stdout)
        self.assertNotIn("CEK CICILAN", r.stdout)
        # angka lama yang salah tidak boleh muncul
        self.assertNotIn("Rp56.542.500", r.stdout)

    def test_bukan_pokok_atas_keputusan_pengguna(self):
        r = jalankan(*self.argumen("--bukan-pokok", "Kiriman ortu"))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("**Rp6.282.500**", r.stdout)
        self.assertIn("| Kiriman ortu | Rp1.000.000 | dikeluarkan atas keputusan pengguna |", r.stdout)
        r = jalankan(*self.argumen("--pokok-juga", "Arisan RT"))
        self.assertIn("**Rp7.782.500**", r.stdout)
        r = jalankan(*self.argumen("--bukan-pokok", "Kiriman orang tua"))
        self.assertEqual(r.returncode, 2)
        self.assertIn("tidak cocok dengan nama pos", r.stderr)

    def test_dana_darurat_tanpa_keluarga_diingatkan(self):
        r = jalankan("dana-darurat", "--pengeluaran-pokok", "6.282.500", "--cicilan", "PayLater=650rb",
                     "--status", "anak")
        self.assertIn("CEK KIRIMAN KELUARGA", r.stdout)
        r = jalankan("dana-darurat", "--pengeluaran-pokok", "6.282.500", "--status", "anak",
                     "--dikeluarkan", "Kiriman ortu=1jt;ortu sudah mandiri, kiriman bisa dihentikan")
        self.assertNotIn("CEK KIRIMAN KELUARGA", r.stdout)
        self.assertIn("Rp6.282.500", r.stdout)
        self.assertIn("ortu sudah mandiri", r.stdout)


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
        ["dana-darurat", "--status", "lajang"],
        ["dana-darurat", "--cicilan", "PayLater=abc", "--status", "lajang"],
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


# ---------------------------------------------------------------------------
# v1.0.1 — regresi per temuan HASIL-UJI (T-1 satuan bunga, T-2 nominal kecil, T-5, T-6)
# ---------------------------------------------------------------------------

def f_efektif_tahunan(pokok, cicilan, n):
    """Bisection Fraction independen: r bulanan dgn PV anuitas = pokok; kembalikan persen/tahun (float)."""
    lo, hi = F(0), F(1)
    for _ in range(80):
        mid = (lo + hi) / 2
        pv = cicilan * (1 - (1 + mid) ** (-n)) / mid
        if pv > pokok:
            lo = mid
        else:
            hi = mid
    return float((lo + hi) / 2 * 1200)


class TesT1SatuanBungaFlat(unittest.TestCase):
    def efektif(self, stdout):
        import re
        m = re.findall(r"= ([0-9]+,[0-9]{2})%/tahun\*\*", stdout)
        return [x.replace(",", ".") for x in m]

    def test_per_bulan_dengan_satuan(self):
        # 30 jt flat 0,9%/bln 24 bln -> cicilan 1.520.000 -> efektif 19,53%/th (bukan 1,72%)
        for bunga in ("0,9%/bln", "0,9%/bulan", "0,9% per bulan", "0.9%/bln"):
            r = jalankan("konversi-flat", "--pokok", "30jt", "--bunga-flat", bunga, "--tenor", "24")
            with self.subTest(bunga=bunga):
                self.assertEqual(r.returncode, 0, r.stderr)
                self.assertIn("Rp1.520.000", r.stdout)
                self.assertEqual(self.efektif(r.stdout), ["19.53"])
                self.assertNotIn("PERINGATAN", r.stdout)
        self.assertAlmostEqual(f_efektif_tahunan(F(30000000), F(1520000), 24), 19.53, places=2)

    def test_opsi_per(self):
        r = jalankan("konversi-flat", "--pokok", "30jt", "--bunga-flat", "0,9", "--per", "bulan", "--tenor", "24")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.efektif(r.stdout), ["19.53"])
        r = jalankan("konversi-flat", "--pokok", "30jt", "--bunga-flat", "10,8%/thn", "--tenor", "24")
        self.assertEqual(self.efektif(r.stdout), ["19.53"])

    def test_tanpa_satuan_kecil_tampilkan_dua_tafsiran(self):
        r = jalankan("konversi-flat", "--pokok", "30jt", "--bunga-flat", "0,9", "--tenor", "24")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("PERINGATAN", r.stdout)
        self.assertIn("per BULAN", r.stdout)
        # tafsiran per bulan tampil PERTAMA, lalu per tahun
        self.assertEqual(self.efektif(r.stdout), ["19.53", "1.72"])

    def test_tanpa_satuan_besar_dianggap_tahunan_dan_diberi_catatan(self):
        r = jalankan("konversi-flat", "--pokok", "18jt", "--bunga-flat", "12", "--tenor", "24")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("Rp930.000", r.stdout)
        self.assertEqual(self.efektif(r.stdout), ["21.57"])
        self.assertIn("DIANGGAP 12%/tahun", r.stdout)

    def test_satuan_bertentangan_ditolak(self):
        r = jalankan("konversi-flat", "--pokok", "30jt", "--bunga-flat", "10,8%/th", "--per", "bulan",
                     "--tenor", "24")
        self.assertEqual(r.returncode, 2)
        self.assertIn("Pilih salah satu", r.stderr)

    def test_presisi_4_desimal_untuk_utang(self):
        r = jalankan("konversi-flat", "--pokok", "30jt", "--bunga-flat", "0,9%/bln", "--tenor", "24")
        self.assertIn("1,6275%/bln", r.stdout)


class TesT1SatuanBungaUtang(unittest.TestCase):
    def test_tanpa_satuan_kecil_ditanya(self):
        for bunga in ("1,75", "2%", "0,5"):
            r = jalankan("utang", "--utang", "KK;12jt;{};600rb;kk".format(bunga))
            with self.subTest(bunga=bunga):
                self.assertEqual(r.returncode, 2)
                self.assertIn("per BULAN atau per TAHUN", r.stderr)
                self.assertNotIn("Traceback", r.stderr)

    def test_opsi_per_sama_dengan_satuan_eksplisit(self):
        a = jalankan("utang", "--utang", "KK;12jt;1,75;600rb;kk", "--per", "bulan", "--ekstra", "300rb")
        b = jalankan("utang", "--utang", "KK;12jt;1,75%/bln;600rb;kk", "--ekstra", "300rb")
        self.assertEqual(a.returncode, 0, a.stderr)
        self.assertEqual(a.stdout, b.stdout)
        u = k.parse_utang("KK;12jt;1,75;600rb;kk", "bulan")
        self.assertEqual(u.bunga.per_bulan_persen(), Decimal("1.75"))

    def test_tanpa_satuan_besar_diberi_peringatan(self):
        r = jalankan("utang", "--utang", "KTA;20jt;11;700rb;kta")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("DIANGGAP 11%/tahun", r.stdout)
        r = jalankan("utang", "--utang", "KTA;20jt;11%/th;700rb;kta")
        self.assertNotIn("DIANGGAP", r.stdout)

    def test_nol_tanpa_satuan_boleh(self):
        r = jalankan("utang", "--utang", "Kakak;2jt;0;500rb;keluarga")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotIn("DIANGGAP", r.stdout)

    def test_skenario_02_tidak_berubah(self):
        r = jalankan("utang", "--utang", "Kartu kredit;12jt;1,75%/bln;600rb;kk",
                     "--utang", "KTA;30jt;1,628%/bln;1.520.000;kta", "--utang", "Paylater;3jt;2,5%/bln;300rb;paylater",
                     "--utang", "Pinjol legal;2jt;0,1%/hari;500rb;pinjol", "--ekstra", "2,5jt", "--metode", "banding")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stdout.count("Semua lunas dalam 10 bulan (~0 th 10 bln). Total bunga Rp4.226.895."), 2)


class TesT2NominalKecil(unittest.TestCase):
    def test_peringatan_ribuan(self):
        r = jalankan("anggaran", "--pemasukan", "Gaji=1.500", "--pos", "Makan=1jt")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("PERINGATAN INPUT", r.stdout)
        self.assertIn("Rp1.500.000", r.stdout)
        for argumen in (["dana-darurat", "--pengeluaran-pokok", "4.500", "--status", "lajang"],
                        ["utang", "--utang", "KK;5.000;1,75%/bln;500;kk"],
                        ["target", "--biaya-sekarang", "60", "--tahun", "5"]):
            r = jalankan(*argumen)
            with self.subTest(argumen=argumen):
                self.assertEqual(r.returncode, 0, r.stderr)
                self.assertIn("PERINGATAN INPUT", r.stdout)

    def test_tanpa_peringatan_bila_wajar(self):
        r = jalankan("anggaran", "--pemasukan", "Gaji=1,5jt", "--pos", "Sampah=5rb")
        self.assertNotIn("PERINGATAN INPUT", r.stdout)
        r = jalankan("dana-darurat", "--pengeluaran-pokok", "4,5jt", "--status", "lajang", "--saldo", "0")
        self.assertNotIn("PERINGATAN INPUT", r.stdout)


def f_bulan_sampai(biaya, inf, imb, terkumpul, setor, batas=720):
    """Independen (Fraction): bulan pertama tabungan >= biaya ikut inflasi (setor akhir bulan)."""
    i, r = F(inf) / 1200, F(imb) / 1200
    if terkumpul >= biaya:
        return 0
    tab = terkumpul
    for m in range(1, batas + 1):
        tab = tab * (1 + r) + setor
        if tab >= f_bulat(biaya * (1 + i) ** m):
            return m
    return None


class TesT5BulanSampaiTarget(unittest.TestCase):
    def test_banding_fraction_acak(self):
        rnd = random.Random(101)
        for _ in range(25):
            biaya = rnd.randint(5, 300) * 1000000
            inf, imb = rnd.choice([0, 3, 4, 6]), rnd.choice([0, 3, 5])
            tk = rnd.randint(0, 20) * 1000000
            setor = rnd.randint(1, 40) * 100000
            m, _ = k.bulan_sampai_target(Decimal(biaya), Decimal(inf), Decimal(imb), Decimal(tk), Decimal(setor))
            with self.subTest(biaya=biaya, inf=inf, imb=imb, tk=tk, setor=setor):
                self.assertEqual(m, f_bulan_sampai(F(biaya), inf, imb, F(tk), F(setor)))

    def test_konsisten_dengan_tabungan_per_bulan(self):
        # menabung tepat sebesar kebutuhan/bulan untuk N bulan -> tercapai paling lambat bulan ke-N
        for biaya, n, inf, imb, tk in [(60000000, 60, 4, 5, 10000000), (150000000, 48, 4, 0, 20000000),
                                       (35000000, 36, 3, 0, 0)]:
            _, _, pmt = k.hitung_target(Decimal(biaya), n, Decimal(inf), Decimal(imb), Decimal(tk))
            m, _ = k.bulan_sampai_target(Decimal(biaya), Decimal(inf), Decimal(imb), Decimal(tk), pmt)
            with self.subTest(biaya=biaya):
                self.assertLessEqual(m, n)
                self.assertGreaterEqual(m, n - 1)

    def test_cli(self):
        r = jalankan("target", "--nama", "DP rumah", "--biaya-sekarang", "60jt", "--tahun", "5", "--inflasi", "4",
                     "--imbal", "5", "--terkumpul", "10jt", "--kemampuan", "700rb")
        self.assertIn("tercapai di bulan ke-78", r.stdout)
        self.assertIn("Rp888.542", r.stdout)   # angka lama tidak berubah
        r = jalankan("target", "--biaya-sekarang", "150jt", "--tahun", "4", "--terkumpul", "20jt",
                     "--inflasi", "5", "--kemampuan", "100rb")
        self.assertIn("TIDAK tercapai", r.stdout)


class TesT6TakeOver(unittest.TestCase):
    def test_catatan_take_over_tanpa_produk(self):
        r = jalankan("utang", "--utang", "KK;5jt;1,75%/bln;500rb;kk")
        for kata in ("take over", "provisi", "penalti", "Tenor lebih panjang"):
            self.assertIn(kata, r.stdout)
        ref = (FOLDER / "references" / "utang-dan-pinjol.md").read_text(encoding="utf-8")
        self.assertIn("Take over", ref)



class TesV102PerbaikanKecil(unittest.TestCase):
    """v1.0.2: N-1, N-2, N-3, T-4, T-7 (pesan), angka tidak berubah."""

    def efektif(self, stdout):
        import re
        return [x.replace(",", ".") for x in re.findall(r"= ([0-9]+,[0-9]{2})%/tahun\*\*", stdout)]

    def test_n1_satuan_sehari_hari(self):
        for bunga, ef in (("18% setahun", "31.46"), ("18 persen per tahun", "31.46"), ("1,5% sebulan", "31.46"),
                          ("1,5 persen per bulan", "31.46"), ("1,5 persen perbulan", "31.46"),
                          ("0,9%/bln flat", "19.53"), ("0,9% sebulan flat", "19.53")):
            r = jalankan("konversi-flat", "--pokok", "30jt", "--bunga-flat", bunga, "--tenor", "24")
            with self.subTest(bunga=bunga):
                self.assertEqual(r.returncode, 0, r.stderr)
                self.assertEqual(self.efektif(r.stdout), [ef])
                self.assertNotIn("PERINGATAN", r.stdout)
        # 'persen' TANPA satuan waktu tetap dianggap ambigu (dua tafsiran), tidak ditafsir diam-diam
        r = jalankan("konversi-flat", "--pokok", "30jt", "--bunga-flat", "0,9 persen", "--tenor", "24")
        self.assertEqual(self.efektif(r.stdout), ["19.53", "1.72"])
        self.assertIn("PERINGATAN", r.stdout)
        # utang: kata sehari-hari = satuan eksplisit; angka sama dengan %/bln
        a = jalankan("utang", "--utang", "KK;12jt;1,75% sebulan;600rb;kk", "--ekstra", "300rb")
        b = jalankan("utang", "--utang", "KK;12jt;1,75%/bln;600rb;kk", "--ekstra", "300rb")
        self.assertEqual(a.returncode, 0, a.stderr)
        self.assertEqual(a.stdout, b.stdout)
        self.assertEqual(k.parse_bunga("24 persen setahun").per_bulan_persen(), Decimal(2))
        self.assertEqual(k.parse_bunga("0,1 persen sehari").per_bulan_persen(), Decimal(3))
        # inflasi 'per tahun' / 'persen'
        a = jalankan("target", "--biaya-sekarang", "60jt", "--tahun", "5", "--inflasi", "4% per tahun")
        b = jalankan("target", "--biaya-sekarang", "60jt", "--tahun", "5", "--inflasi", "4")
        self.assertEqual(a.returncode, 0, a.stderr)
        self.assertEqual(a.stdout, b.stdout)

    def test_n1_flat_efektif(self):
        r = jalankan("utang", "--utang", "KTA;30jt;0,9%/bln flat;1,52jt;kta")
        self.assertEqual(r.returncode, 2)
        self.assertIn("konversi-flat", r.stderr)
        r = jalankan("konversi-flat", "--pokok", "30jt", "--bunga-flat", "1,6%/bln efektif", "--tenor", "24")
        self.assertEqual(r.returncode, 2)
        self.assertIn("EFEKTIF", r.stderr)
        r = jalankan("konversi-flat", "--pokok", "30jt", "--bunga-flat", "0,9%/bln flat efektif", "--tenor", "24")
        self.assertEqual(r.returncode, 2)

    def test_t4_catatan_flat_hilang_bila_efektif(self):
        r = jalankan("utang", "--utang", "KTA;30jt;1,6275%/bln efektif;1,52jt;kta")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotIn("bila bunganya FLAT", r.stdout)
        r2 = jalankan("utang", "--utang", "KTA;30jt;1,6275%/bln;1,52jt;kta")
        self.assertIn("bila bunganya FLAT", r2.stdout)
        # angka simulasi identik
        import re
        self.assertEqual(re.findall(r"Total bunga Rp[0-9.]+", r.stdout), re.findall(r"Total bunga Rp[0-9.]+", r2.stdout))

    def test_n2_pos_kecil(self):
        r = jalankan("anggaran", "--pemasukan", "Gaji=7jt", "--pos", "Makan=1.500")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("PERINGATAN INPUT", r.stdout)
        self.assertIn("Pos 'Makan'", r.stdout)
        self.assertIn("Rp1.500.000", r.stdout)
        for pos in ("Sampah=5rb", "Makan=1,5jt", "Parkir=10.000", "Iuran=0",
                    "Parkir=5000", "Parkir=5.000", "Jajan anak=8.000", "Sewa=Rp5.000"):  # v1.0.3: tidak berisik
            r = jalankan("anggaran", "--pemasukan", "Gaji=7jt", "--pos", pos)
            with self.subTest(pos=pos):
                self.assertNotIn("PERINGATAN INPUT", r.stdout)

    def test_v103_pos_wajar_kecil_tetap_diperingatkan_bila_sangat_kecil(self):
        r = jalankan("anggaran", "--pemasukan", "Gaji=7jt", "--pos", "Parkir=500")
        self.assertIn("PERINGATAN INPUT", r.stdout)
        r = jalankan("anggaran", "--pemasukan", "Gaji=7jt", "--pos", "Sewa kos=1.200")
        self.assertIn("PERINGATAN INPUT", r.stdout)

    def test_n3_target_cukup_harga_sekarang(self):
        r = jalankan("target", "--biaya-sekarang", "50jt", "--bulan", "24", "--terkumpul", "51jt", "--kemampuan", "0")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("sudah cukup untuk harga sekarang Rp50.000.000", r.stdout)
        self.assertIn("Rp54.157.148", r.stdout)     # biaya setelah inflasi (angka lama)
        self.assertIn("Rp131.548", r.stdout)        # tambahan per bulan (angka lama)
        self.assertNotIn("**Kurang", r.stdout)
        self.assertLess(r.stdout.index("sudah cukup untuk harga sekarang"), r.stdout.index("Bila menunggu 24 bulan, biaya diperkirakan naik menjadi Rp54.157.148"))
        r = jalankan("target", "--biaya-sekarang", "50jt", "--bulan", "24", "--terkumpul", "51jt", "--kemampuan", "200rb")
        self.assertIn("cukup (sisa Rp68.452)", r.stdout)
        r = jalankan("target", "--biaya-sekarang", "50jt", "--bulan", "12", "--terkumpul", "60jt")
        self.assertIn("tetap cukup", r.stdout)
        # kasus biasa tidak berubah
        r = jalankan("target", "--nama", "DP rumah", "--biaya-sekarang", "60jt", "--tahun", "5", "--inflasi", "4",
                     "--imbal", "5", "--terkumpul", "10jt", "--kemampuan", "700rb")
        self.assertIn("tercapai di bulan ke-78", r.stdout)
        self.assertNotIn("harga sekarang", r.stdout)

    def test_t7_pesan(self):
        r = jalankan("anggaran", "--pemasukan", "Gaji=7jt", "--pos", "Nongkrong=1jt:hiburan")
        self.assertEqual(r.returncode, 2)
        self.assertIn("label kelompok 'hiburan' tidak dikenal", r.stderr)
        r = jalankan("dana-darurat", "--pengeluaran-pokok", "-500rb", "--status", "lajang")
        self.assertEqual(r.returncode, 2)
        self.assertIn("tidak boleh negatif", r.stderr)
        self.assertNotIn("expected one argument", r.stderr)

class TesTHRMusimanTidakDihitungDuaKali(unittest.TestCase):
    """v1.0.7 (uji tampilan Telegram 2026-10-02): keluarga Bekasi, gaji 8,5 jt + 4 jt, THR 1x gaji, pos
    Rp11.670.000. Dulu: sisa Rp1.871.666 (termasuk THR/12) disuruh dipindah tiap bulan dari 'sisa gaji'
    DAN THR disimpan lagi saat cair -> THR terhitung dua kali. Angka benar (dihitung manual, Fraction):
      sisa rutin = 12.500.000 - 11.670.000 = 830.000 ; THR/12 = floor(12.500.000/12) = 1.041.666
      rasio cicilan rutin = 4.300.000/12.500.000 = 34,4% ; dengan THR/12 = 4.300.000/13.541.666 = 31,8%"""

    POS = ["Kontrakan=2,5jt", "Cicilan motor=1,3jt", "KPR=3jt", "Dapur=3jt", "Listrik air=500rb", "SPP=800rb",
           "Bensin=570rb"]
    ARG = ["anggaran", "--pemasukan", "Gaji suami=8,5jt", "--pemasukan", "Gaji istri=4jt",
           "--musiman", "THR suami=8,5jt", "--musiman", "THR istri=4jt"]

    def hitung(self, pos):
        return k.hitung_anggaran([("Gaji suami", Decimal(8500000)), ("Gaji istri", Decimal(4000000))],
                                 [("THR suami", Decimal(8500000)), ("THR istri", Decimal(4000000))],
                                 [k.parse_pos(p) for p in pos], [Decimal(50), Decimal(30), Decimal(20)])

    def test_sisa_rutin_dipisah_dari_thr(self):
        h = self.hitung(self.POS)
        self.assertEqual(h["sisa"], Decimal(1871666))
        self.assertEqual(h["sisa_rutin"], Decimal(830000))
        self.assertEqual(h["musiman_per_bulan"], Decimal(math.floor(F(12500000, 12))))
        self.assertEqual(h["tambal_musiman_per_bulan"], Decimal(0))

    def test_rasio_cicilan_basis_rutin(self):
        h = self.hitung(self.POS)
        self.assertEqual(h["basis_cicilan"], Decimal(12500000))
        r = jalankan(*(self.ARG + sum([["--pos", p] for p in self.POS], [])))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("34,4% dari pemasukan RUTIN", r.stdout)
        self.assertIn("31,8%", r.stdout)
        self.assertIn("paling banyak **Rp830.000/bulan**", r.stdout)
        self.assertIn("SEKALI saat cair: Rp12.500.000", r.stdout)
        self.assertIn("(Rp830.000 dari gaji tiap bulan + Rp1.041.666 bagian THR", r.stdout)

    def test_setoran_melebihi_gaji_ditambal_thr(self):
        h = self.hitung(self.POS + ["Setoran dana darurat=1,5jt"])
        self.assertEqual(h["sisa_rutin"], Decimal(-670000))
        self.assertEqual(h["tambal_musiman_per_bulan"], Decimal(670000))
        self.assertEqual(h["tambal_musiman_setahun"], Decimal(8040000))
        self.assertEqual(h["musiman_bebas_setahun"], Decimal(12500000 - 8040000))
        self.assertEqual(h["bulan_ditambal_musiman"], math.floor(F(12500000, 670000)))   # 18
        r = jalankan(*(self.ARG + sum([["--pos", p] for p in self.POS + ["Setoran dana darurat=1,5jt"]], [])))
        self.assertIn("kurang **Rp670.000/bulan** dari gaji", r.stdout)
        self.assertIn("maks. Rp830.000 (sisa gaji)", r.stdout)

    def test_tanpa_musiman_tidak_ada_bagian_arus(self):
        r = jalankan("anggaran", "--pemasukan", "Gaji=5jt", "--pos", "Kos=2jt")
        self.assertNotIn("Arus kas rutin vs musiman", r.stdout)

    def test_dana_darurat_dengan_thr_sekaligus(self):
        self.assertEqual(k.lama_dengan_musiman(Decimal(95500000), Decimal(830000), Decimal(12500000), 6), 54)
        # independen: cari m terkecil dengan 830.000*m + 12.500.000*jumlah_cair(m) >= kurang
        def f_lama(kurang, setor, thr, cair):
            m = 0
            while True:
                m += 1
                n_cair = 0 if m < cair else (m - cair) // 12 + 1
                if setor * m + thr * n_cair >= kurang:
                    return m
        for kurang, cair in [(95500000, 6), (130000000, 1), (5000000, 12), (12500000, 3)]:
            self.assertEqual(k.lama_dengan_musiman(Decimal(kurang), Decimal(830000), Decimal(12500000), cair),
                             f_lama(kurang, 830000, 12500000, cair))
        r = jalankan("dana-darurat", "--pengeluaran-pokok", "11,67jt", "--cicilan", "KPR=0", "--status", "anak",
                     "--saldo", "8jt", "--setoran", "830rb", "--setoran-tahunan", "12,5jt")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("cair bulan ke-12 dari sekarang (asumsi bawaan", r.stdout)
        self.assertIn("Lama tercapai (+ THR/bonus)", r.stdout)
        r = jalankan("dana-darurat", "--pengeluaran-pokok", "5jt", "--status", "lajang", "--bulan-cair", "13")
        self.assertEqual(r.returncode, 2)


if __name__ == "__main__":
    unittest.main(verbosity=1)
