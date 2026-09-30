#!/usr/bin/env python3
"""Uji regresi program-referral-loyalitas. Jalankan: python3 tests/uji_regresi.py  (Windows: py tests/uji_regresi.py)

Semua angka acuan dihitung MANUAL (rumus di komentar), bukan disalin dari keluaran script.
Contoh dasar: "Kopi Senja" (fiktif), nilai pesanan Rp60.000, margin kotor 55% -> laba kotor Rp33.000.
"""
import contextlib
import io
import os
import sys
import unittest
from decimal import Decimal as D

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AKAR, "scripts"))
import hitung_referral as H  # noqa: E402


def jalan(*argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        try:
            kode = H.main(list(argv))
        except SystemExit as e:      # argparse keluar dengan kode 2
            kode = e.code
    return kode, out.getvalue(), err.getvalue()


class Parsing(unittest.TestCase):
    def test_rupiah(self):
        for teks, harap in {"Rp28.000": 28000, "28rb": 28000, "1,2jt": 1200000, "45k": 45000, "60000": 60000}.items():
            self.assertEqual(H.parse_rupiah(teks), D(harap))

    def test_rupiah_ditolak(self):
        for teks in ("abc", "0", "-5000", "12.5", ""):
            with self.assertRaises(H.InputError):
                H.parse_rupiah(teks)

    def test_hadiah_persen_dan_rupiah(self):
        self.assertEqual(H.parse_hadiah("10%", D(60000)), D(6000))        # 60000 x 10%
        self.assertEqual(H.parse_hadiah("12,5%", D(45000)), D(5625))      # 45000 x 0,125
        self.assertEqual(H.parse_hadiah("15rb", D(60000)), D(15000))
        self.assertEqual(H.parse_hadiah("0", D(60000)), D(0))

    def test_margin_batas(self):
        for teks in ("0", "100", "-5", "abc"):
            with self.assertRaises(H.InputError):
                H.parse_margin(teks)
        self.assertEqual(H.parse_margin("55"), D("0.55"))

    def test_format(self):
        self.assertEqual(H.rp(D(1250000)), "Rp1.250.000")
        self.assertEqual(H.rp(D(-18000)), "-Rp18.000")
        self.assertEqual(H.pct(D("0.545454")), "54,55%")
        self.assertEqual(H.pct(D("0.3")), "30%")


class Biaya(unittest.TestCase):
    def test_dasar(self):
        # laba kotor = 60000 x 0,55 = 33000 ; biaya = 10000 + (10% x 60000 = 6000) + 2000 = 18000
        h = H.biaya_referral(D(60000), D("0.55"), D(10000), D(6000), D(2000))
        self.assertEqual(h["lpo"], D(33000))
        self.assertEqual(h["biaya"], D(18000))
        self.assertEqual(h["laba_setelah"], D(15000))                    # 33000 - 18000
        self.assertEqual(h["persen_aov"], D("0.3"))                      # 18000 / 60000
        self.assertEqual(H.pct(h["persen_laba"]), "54,55%")              # 18000 / 33000
        self.assertEqual(h["pesanan_tambahan"], D(0))

    def test_rugi_pesanan_pertama(self):
        # laba kotor 33000 ; biaya 30000 + 6000 + 2000 = 38000 ; setelah = -5000 ; pesanan tambahan = ceil(5000/33000) = 1
        h = H.biaya_referral(D(60000), D("0.55"), D(30000), D(6000), D(2000))
        self.assertEqual(h["laba_setelah"], D(-5000))
        self.assertEqual(h["pesanan_tambahan"], D(1))

    def test_cli_total_dan_anggaran(self):
        kode, out, _ = jalan("biaya", "--aov", "60rb", "--margin", "55", "--hadiah-pemberi", "10rb",
                             "--hadiah-teman", "10%", "--biaya-lain", "2rb", "--jumlah-referral", "20",
                             "--anggaran", "300rb", "--cac-iklan", "25rb")
        self.assertEqual(kode, 0)
        self.assertIn("BIAYA PER REFERRAL              : Rp18.000", out)
        self.assertIn("total biaya Rp360.000", out)                      # 20 x 18000
        self.assertIn("laba setelah hadiah Rp300.000", out)              # 20 x 15000
        self.assertIn("TIDAK CUKUP (kurang Rp60.000)", out)              # 300000 - 360000
        self.assertIn("LEBIH MURAH (selisih Rp7.000)", out)              # 25000 - 18000

    def test_cli_anggaran_saja(self):
        # 300000 / 18000 = 16,67 -> maksimal 16
        kode, out, _ = jalan("biaya", "--aov", "60rb", "--margin", "55", "--hadiah-pemberi", "10rb",
                             "--hadiah-teman", "10%", "--biaya-lain", "2rb", "--anggaran", "300rb")
        self.assertIn("maksimal 16 referral", out)

    def test_cli_peringatan_rugi(self):
        kode, out, _ = jalan("biaya", "--aov", "60rb", "--margin", "55", "--hadiah-pemberi", "30rb",
                             "--hadiah-teman", "10%", "--biaya-lain", "2rb")
        self.assertIn("PERHATIAN: hadiah lebih besar dari laba kotor pesanan pertama (rugi Rp5.000", out)
        self.assertIn("minimal 1 pesanan ulang", out)


class Impas(unittest.TestCase):
    def test_aman(self):
        # biaya 18000 ; lpo 33000 ; impas di pesanan ke-1 ; LTV = 33000 x (2 x 6 = 12) = 396000 ; aman 30% = 118800
        h = H.titik_impas(D(60000), D("0.55"), D(10000), D(6000), D(2000), D(2), D(6), D("0.3"))
        self.assertEqual(h["pesanan_impas"], D(1))
        self.assertEqual(h["ltv"], D(396000))
        self.assertEqual(h["batas_aman"], D(118800))
        self.assertEqual(h["pemberi_maks"], D(110800))                   # 118800 - 6000 - 2000
        self.assertEqual(h["status"], "AMAN")

    def test_impas_pesanan_kedua(self):
        # biaya 40000 + 6000 + 2000 = 48000 ; ceil(48000/33000) = 2 ; bulan = ceil((2-1)/2) = 1
        h = H.titik_impas(D(60000), D("0.55"), D(40000), D(6000), D(2000), D(2), D(6), D("0.3"))
        self.assertEqual(h["pesanan_impas"], D(2))
        self.assertEqual(h["bulan_impas"], D(1))
        self.assertEqual(h["status"], "AMAN")                            # 48000 <= 118800

    def test_status_perhatian_dan_tidak_disarankan(self):
        # frekuensi 1 x 6 bln -> LTV = 33000 x 6 = 198000 ; aman 30% = 59400
        h = H.titik_impas(D(60000), D("0.55"), D(60000), D(0), D(0), D(1), D(6), D("0.3"))
        self.assertEqual(h["batas_aman"], D(59400))
        self.assertEqual(h["status"], "PERHATIAN")                       # 60000 > 59400 tetapi <= 198000
        h = H.titik_impas(D(60000), D("0.55"), D(200000), D(0), D(0), D(1), D(6), D("0.3"))
        self.assertEqual(h["status"], "TIDAK DISARANKAN")                # 200000 > 198000
        self.assertEqual(h["pesanan_impas"], D(7))                       # ceil(200000/33000) = ceil(6,06)

    def test_batas_aman_dibulatkan_ke_bawah(self):
        # aov 1000, margin 33% -> lpo 330 ; LTV = 330 x 1 x 1 = 330 ; 33% x 330 = 108,9 -> 108 (ke bawah)
        h = H.titik_impas(D(1000), D("0.33"), D(0), D(0), D(0), D(1), D(1), D("0.33"))
        self.assertEqual(h["batas_aman"], D(108))

    def test_cli(self):
        kode, out, _ = jalan("impas", "--aov", "60rb", "--margin", "55", "--hadiah-pemberi", "40rb",
                             "--hadiah-teman", "10%", "--biaya-lain", "2rb", "--frekuensi-bulan", "2", "--umur-bulan", "6")
        self.assertEqual(kode, 0)
        self.assertIn("pesanan ke-2 milik teman, sekitar bulan ke-1", out)
        self.assertIn("Rp118.800 total per referral", out)
        self.assertIn("STATUS: AMAN", out)


class Poin(unittest.TestCase):
    def test_dasar(self):
        # rate = 250/10000 = 2,5% ; porsi margin = 2,5%/40% = 6,25% ; aov 85000 -> floor(8,5) = 8 poin = 2000
        # lpo = 85000 x 0,4 = 34000 ; setelah tukar 32000 ; rate nyata = 2000/85000 = 2,35%
        # omzet 80jt x 2,5% = 2.000.000 ; breakage 20% -> 1.600.000 ; beredar 40000 x 250 = 10.000.000 ; -> 8.000.000
        h = H.nilai_poin(D(10000), D(250), D("0.4"), aov=D(85000), omzet=D(80000000), breakage=D("0.2"),
                         beredar=D(40000), min_tukar=D(40))
        self.assertEqual(h["rate"], D("0.025"))
        self.assertEqual(h["porsi_margin"], D("0.0625"))
        self.assertEqual(h["status"], "OK")
        self.assertEqual(h["poin_per_pesanan"], D(8))
        self.assertEqual(h["nilai_per_pesanan"], D(2000))
        self.assertEqual(H.pct(h["rate_nyata"]), "2,35%")
        self.assertEqual(h["laba_setelah_tukar"], D(32000))
        self.assertEqual(h["biaya_maks"], D(2000000))
        self.assertEqual(h["biaya_perkiraan"], D(1600000))
        self.assertEqual(h["liab_maks"], D(10000000))
        self.assertEqual(h["liab_perkiraan"], D(8000000))
        self.assertEqual(h["belanja_min"], D(400000))                    # 40 x 10000
        self.assertEqual(h["hadiah_min"], D(10000))                      # 40 x 250

    def test_status(self):
        # margin 30% : rate 20% -> 66,7% margin = PERHATIAN ; rate 40% -> RUGI ; rate 15% -> tepat 50% = OK
        self.assertEqual(H.nilai_poin(D(10000), D(2000), D("0.3"))["status"], "PERHATIAN")
        self.assertEqual(H.nilai_poin(D(10000), D(4000), D("0.3"))["status"], "RUGI")
        self.assertEqual(H.nilai_poin(D(10000), D(1500), D("0.3"))["status"], "OK")
        self.assertEqual(H.nilai_poin(D(10000), D(3000), D("0.3"))["status"], "RUGI")   # sama dengan margin

    def test_poin_dibulatkan_ke_bawah(self):
        h = H.nilai_poin(D(10000), D(100), D("0.4"), aov=D(9999))
        self.assertEqual(h["poin_per_pesanan"], D(0))                    # 9999 < 10000 -> 0 poin

    def test_cli_rugi(self):
        kode, out, _ = jalan("poin", "--belanja-per-poin", "10rb", "--nilai-poin", "4rb", "--margin", "30")
        self.assertEqual(kode, 0)
        self.assertIn("STATUS: RUGI", out)
        self.assertIn("133,33% dari margin", out)                        # 40% / 30%


class Simulasi(unittest.TestCase):
    def test_skenario_bawaan(self):
        # 400 pelanggan ; realistis 10%:2:25% -> 40 perujuk, 80 teman, 20 pembeli ; biaya 20 x 18000 = 360000
        # laba kotor (1 pesanan) = 20 x 33000 = 660000 ; setelah hadiah 300000 ; ROI = 300000/360000 = 83,33%
        per, hasil = H.simulasi(D(400), D(60000), D("0.55"), D(10000), D(6000), D(2000),
                                [H.parse_skenario(x) for x in H.SKENARIO_BAWAAN], D(0), None, None)
        r = {x["nama"]: x for x in hasil}
        self.assertEqual((r["konservatif"]["perujuk"], r["konservatif"]["diajak"], r["konservatif"]["pembeli"]),
                         (D(20), D(20), D(4)))
        self.assertEqual((r["realistis"]["perujuk"], r["realistis"]["diajak"], r["realistis"]["pembeli"]),
                         (D(40), D(80), D(20)))
        self.assertEqual((r["optimis"]["perujuk"], r["optimis"]["diajak"], r["optimis"]["pembeli"]),
                         (D(60), D(120), D(36)))
        self.assertEqual(r["realistis"]["biaya"], D(360000))
        self.assertEqual(r["realistis"]["laba_kotor"], D(660000))
        self.assertEqual(r["realistis"]["bersih"], D(300000))
        self.assertEqual(H.pct(r["realistis"]["roi"]), "83,33%")
        self.assertEqual(r["realistis"]["omzet"], D(1200000))            # 20 x 60000

    def test_pesanan_ulang(self):
        # 1 pesanan ulang tanpa hadiah: laba kotor = 20 x 33000 x 2 = 1.320.000 ; bersih = 960000 ; ROI 266,67%
        _, hasil = H.simulasi(D(400), D(60000), D("0.55"), D(10000), D(6000), D(2000),
                              [H.parse_skenario("realistis:10:2:25")], D(1), None, None)
        self.assertEqual(hasil[0]["laba_kotor"], D(1320000))
        self.assertEqual(hasil[0]["bersih"], D(960000))
        self.assertEqual(H.pct(hasil[0]["roi"]), "266,67%")

    def test_pembulatan_orang(self):
        # 30 pelanggan x 5% = 1,5 -> 2 (setengah ke atas) ; 2 x 1 = 2 ; 2 x 25% = 0,5 -> 1
        _, hasil = H.simulasi(D(30), D(60000), D("0.55"), D(0), D(0), D(0),
                              [H.parse_skenario("x:5:1:25")], D(0), None, None)
        self.assertEqual((hasil[0]["perujuk"], hasil[0]["diajak"], hasil[0]["pembeli"]), (D(2), D(2), D(1)))

    def test_cli_anggaran_dan_rugi(self):
        kode, out, _ = jalan("simulasi", "--pelanggan-aktif", "400", "--aov", "60rb", "--margin", "55",
                             "--hadiah-pemberi", "30rb", "--hadiah-teman", "10%", "--biaya-lain", "2rb",
                             "--skenario", "a:10:2:25", "--anggaran", "500rb")
        # biaya per referral 38000 ; 20 pembeli -> 760000 > 500000 ; laba setelah = 20 x (33000 - 38000) = -100000
        self.assertEqual(kode, 0)
        self.assertIn("biaya hadiah Rp760.000", out)
        self.assertIn("laba setelah hadiah -Rp100.000", out)
        self.assertIn("melebihi anggaran Rp500.000", out)
        self.assertIn("tiap referral rugi Rp5.000", out)


class InputBuruk(unittest.TestCase):
    def cek_gagal(self, *argv, kata=None):
        kode, out, err = jalan(*argv)
        self.assertEqual(kode, 2, (out, err))
        if kata:
            self.assertIn(kata, err + out)
        self.assertNotIn("Traceback", err)

    def test_gagal(self):
        self.cek_gagal("biaya", "--aov", "12.5", "--margin", "50", kata="GAGAL")
        self.cek_gagal("biaya", "--aov", "abc", "--margin", "50", kata="GAGAL")
        self.cek_gagal("biaya", "--aov", "50rb", "--margin", "0", kata="GAGAL")
        self.cek_gagal("biaya", "--aov", "50rb", "--margin", "100", kata="GAGAL")
        self.cek_gagal("biaya", "--aov", "50rb", "--margin", "50", "--hadiah-pemberi=-5rb", kata="GAGAL")
        self.cek_gagal("biaya", "--aov", "50rb", "--margin", "50", "--hadiah-teman", "150%", kata="GAGAL")
        self.cek_gagal("biaya", "--aov", "50rb", "--margin", "50", "--jumlah-referral", "2,5", kata="GAGAL")
        self.cek_gagal("impas", "--aov", "50rb", "--margin", "50", "--umur-bulan", "0", kata="GAGAL")
        self.cek_gagal("impas", "--aov", "50rb", "--margin", "50", "--porsi-ltv", "0", kata="GAGAL")
        self.cek_gagal("poin", "--belanja-per-poin", "0", "--nilai-poin", "100", "--margin", "40", kata="GAGAL")
        self.cek_gagal("poin", "--belanja-per-poin", "10rb", "--nilai-poin", "100", "--margin", "40",
                       "--breakage", "100", kata="GAGAL")
        self.cek_gagal("simulasi", "--pelanggan-aktif", "100", "--aov", "50rb", "--margin", "50",
                       "--skenario", "salah-format", kata="GAGAL")
        self.cek_gagal("simulasi", "--pelanggan-aktif", "0", "--aov", "50rb", "--margin", "50", kata="GAGAL")

    def test_singkatan_opsi_ditolak(self):
        kode, _, _ = jalan("biaya", "--aov", "50rb", "--marg", "50")
        self.assertEqual(kode, 2)
        kode, _, _ = jalan("biaya", "--aov", "50rb", "--margin", "50", "--jumlah", "5")
        self.assertEqual(kode, 2)

    def test_tanpa_perintah(self):
        kode, _, _ = jalan()
        self.assertEqual(kode, 2)


if __name__ == "__main__":
    unittest.main(verbosity=1)
