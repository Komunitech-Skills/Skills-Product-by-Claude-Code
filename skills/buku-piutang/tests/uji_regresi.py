#!/usr/bin/env python3
"""Uji regresi buku-piutang. Jalankan: python3 tests/uji_regresi.py  (Windows: py tests/uji_regresi.py)

Hanya library standar. Semua data fiktif (nomor dummy 0812-0000-xxxx), dibuat di folder sementara.
Angka diverifikasi dengan rumus manual di komentar tiap tes:
  sisa nota  = nominal - pembayaran dialokasikan - potongan
  deposit    = pembayaran - alokasi ke nota aktif - pengembalian
  umur       = tanggal posisi - jatuh tempo (hari); <=0 belum JT, 1-30, 31-60, 61-90, >90
  PPN        = floor(DPP x tarif) sekali; tarif 11 = 12% x 11/12
"""
import contextlib
import hashlib
import io
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from urllib.parse import unquote

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AKAR, "scripts"))
import piutang as P  # noqa: E402

HARI = "2026-09-26"   # Sabtu


class Dasar(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.db = os.path.join(self.dir, "piutang.db")
        self.ok("init", "--nama-usaha", "Toko Contoh", "--pengirim", "Sari", "--rekening",
                "BCA 0000000000 a.n. Contoh", "--ya")

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def run_cli(self, *argv, hari=HARI, db=None):
        argv = list(argv) + ["--db", db or self.db, "--json", "--hari-ini", hari]
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
            kode = P.main(argv)
        return kode, json.loads(buf.getvalue())

    def ok(self, *argv, **kw):
        kode, out = self.run_cli(*argv, **kw)
        self.assertEqual(kode, 0, out)
        self.assertTrue(out["ok"], out)
        return out

    def gagal(self, *argv, **kw):
        kode, out = self.run_cli(*argv, **kw)
        self.assertEqual(kode, 1, out)
        self.assertFalse(out["ok"])
        return out

    def sha(self, p=None):
        with open(p or self.db, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()

    def file(self, nama, isi, encoding="utf-8"):
        p = os.path.join(self.dir, nama)
        with open(p, "w", encoding=encoding, newline="") as f:
            f.write(isi)
        return p

    def hitung(self, sql):
        c = sqlite3.connect(self.db)
        try:
            return c.execute(sql).fetchone()[0]
        finally:
            c.close()

    def catat(self, pel, nota, tgl, nominal, jt=None, termin=None, **kw):
        a = ["catat", "--pelanggan", pel, "--nota", nota, "--tanggal", tgl, "--nominal", nominal]
        if jt:
            a += ["--jatuh-tempo", jt]
        if termin is not None:
            a += ["--termin", str(termin)]
        for k, v in kw.items():
            a += ["--" + k.replace("_", "-"), v]
        return self.ok(*a)


# --------------------------------------------------------------------------- fungsi murni
class UjiUang(unittest.TestCase):
    def test_format_rupiah_diterima(self):
        kasus = {"2,5 jt": 2500000, "2.500.000": 2500000, "Rp2.500.000,-": 2500000, "750rb": 750000,
                 "2 jt 500 rb": 2500000, "1,2 M": 1200000000, "Rp 1.250.000": 1250000, "150000": 150000,
                 "1,234,567": 1234567, "150000.00": 150000, "1.500.000,00": 1500000, "4,275 jt": 4275000}
        for teks, harap in kasus.items():
            self.assertEqual(P.parse_rupiah(teks)[0], harap, teks)

    def test_pecahan_sen_dibulatkan_terdekat(self):
        # 1.234.567,50 -> 1.234.568 (0,5 ke atas); 150000.49 -> 150000
        n, cat = P.parse_rupiah("1.234.567,50")
        self.assertEqual(n, 1234568)
        self.assertTrue(cat)
        self.assertEqual(P.parse_rupiah("150000.49")[0], 150000)

    def test_nominal_ambigu_atau_ngawur_ditolak(self):
        for teks in ("4,5", "12.50", "1.500 jt", "5m", "-50.000", "(50.000)", "0", "abc", "", "2 jt 500",
                     "9999999999999", "Rp", "1.2.3"):
            with self.assertRaises(P.Gagal, msg=teks):
                P.parse_rupiah(teks)

    def test_ppn_dibulatkan_ke_bawah_sekali(self):
        # 999.999 x 11% = 109.999,89 -> 109.999 ; 1.234.567 x 12% = 148.148,04 -> 148.148
        self.assertEqual(P.hitung_ppn(999999, "11")[0], 109999)
        self.assertEqual(P.hitung_ppn(1234567, "12")[0], 148148)
        self.assertEqual(P.hitung_ppn(10000000, "11%")[0], 1100000)
        for dpp in range(1, 3000, 7):
            for t, tarif in (("11", 11), ("12", 12)):
                ppn = P.hitung_ppn(dpp, t)[0]
                self.assertLessEqual(ppn * 100, dpp * tarif)          # tidak pernah melebihi tarif
                self.assertGreater((ppn + 1) * 100, dpp * tarif)      # dan tidak kurang dari satu rupiah
        with self.assertRaises(P.Gagal):
            P.hitung_ppn(1000, "10")


class UjiTanggal(unittest.TestCase):
    H = date(2026, 9, 26)

    def baca(self, t, arah="bebas", **kw):
        return P.baca_tgl(t, self.H, arah, hari=self.H, **kw)[0]

    def test_format_indonesia_diterima(self):
        kasus = {"26/09/2026": date(2026, 9, 26), "1/8/2026": date(2026, 8, 1), "01-08-2026": date(2026, 8, 1),
                 "01.08.2026": date(2026, 8, 1), "2026-08-01": date(2026, 8, 1), "1 Agu 2026": date(2026, 8, 1),
                 "1 agustus 2026": date(2026, 8, 1), "01-Aug-26": date(2026, 8, 1),
                 "2026-08-01 13:45:00": date(2026, 8, 1), "01/08/2026 13.45": date(2026, 8, 1),
                 "2026-08-01T13:45": date(2026, 8, 1), "kemarin": date(2026, 9, 25), "hari ini": self.H,
                 "Senin 28/09/2026": date(2026, 9, 28), "3 hari lalu": date(2026, 9, 23)}
        for t, harap in kasus.items():
            self.assertEqual(self.baca(t), harap, t)

    def test_tanggal_ngawur_ditolak(self):
        for t in ("10/25/2026", "31/02/2026", "31/09/2026", "2026-13-01", "46291", "1/1/1926", "1/1/2126",
                  "25-12", "kapan-kapan", "", "20260926", "13/13/2026", "0/5/2026", "tgl 5"):
            with self.assertRaises(P.Gagal, msg=t):
                self.baca(t, "lalu")

    def test_petunjuk_format_amerika(self):
        with self.assertRaises(P.Gagal) as c:
            self.baca("10/25/2026")
        self.assertIn("25/10/2026", c.exception.pesan)

    def test_tanpa_tahun(self):
        self.assertEqual(self.baca("3/9", "lalu"), date(2026, 9, 3))
        self.assertEqual(self.baca("5/10", "depan"), date(2026, 10, 5))
        self.assertEqual(self.baca("5 Jan", "depan"), date(2027, 1, 5))     # 101 hari lagi
        with self.assertRaises(P.Gagal):
            self.baca("28/12", "lalu")          # 272 hari lalu: terlalu jauh, minta tahun
        with self.assertRaises(P.Gagal):
            self.baca("1/6", "depan")           # 248 hari lagi: minta tahun

    def test_tahun_dua_angka_diberi_catatan(self):
        d, cat = P.baca_tgl("26/09/26", self.H, "lalu", hari=self.H)
        self.assertEqual(d, date(2026, 9, 26))
        self.assertTrue(cat)

    def test_urutan_bulan_hari_eksplisit(self):
        self.assertEqual(self.baca("09/25/2026", urutan="bulan-hari"), date(2026, 9, 25))
        with self.assertRaises(P.Gagal):
            self.baca("25/09/2026", urutan="bulan-hari")

    def test_termin(self):
        self.assertEqual(P.baca_termin("30"), 30)
        self.assertEqual(P.baca_termin("30 hari"), 30)
        self.assertEqual(P.baca_termin("net 14"), 14)
        self.assertIsNone(P.baca_termin("26/10/2026"))

    def test_umur_batas(self):
        # telat 0 = belum JT; 1 & 30 -> 1_30; 31 & 60 -> 31_60; 61 & 90 -> 61_90; 91 -> lebih_90
        harap = {-5: "belum_jatuh_tempo", 0: "belum_jatuh_tempo", 1: "1_30", 30: "1_30", 31: "31_60",
                 60: "31_60", 61: "61_90", 90: "61_90", 91: "lebih_90", 400: "lebih_90"}
        for t, k in harap.items():
            self.assertEqual(P.kelompok_umur(t), k, t)


class UjiNamaNomor(unittest.TestCase):
    def test_wa(self):
        self.assertEqual(P.normalisasi_wa("0812-0000-1001")[0], "6281200001001")
        self.assertEqual(P.normalisasi_wa("+62 812 0000 1001")[0], "6281200001001")
        for bad in ("6.28E+12", "0812 atau 0813-0000-1111 / 081200002222", "abc", "0812"):
            with self.assertRaises(P.Gagal):
                P.normalisasi_wa(bad)

    def test_samar_dan_panggilan(self):
        self.assertEqual(P.samar_nama("Warung Bu Tini"), "Warung Bu T.")
        self.assertEqual(P.samar_nama("Budi Santoso"), "B. S.")
        self.assertEqual(P.samar_wa("6281200001001"), "0812-****-1001")
        self.assertEqual(P.panggilan({"nama": "Warung Bu Tini", "sapaan": None}, {}), "Bu Tini")
        self.assertEqual(P.panggilan({"nama": "CV Maju", "sapaan": None}, {}), "Bapak/Ibu di CV Maju")
        self.assertEqual(P.panggilan({"nama": "Pak Joko", "sapaan": None}, {}), "Pak Joko")
        self.assertEqual(P.panggilan({"nama": "Rina", "sapaan": "Kak"}, {}), "Kak Rina")


# --------------------------------------------------------------------------- catat & bayar
class UjiCatat(Dasar):
    def test_catat_dasar_dan_jatuh_tempo_default(self):
        o = self.ok("catat", "--pelanggan", "Toko Maju", "--wa", "0812-0000-1001", "--nota", "INV-1", "--tanggal",
                    "01/09/2026", "--nominal", "2,5jt")
        self.assertEqual(o["nota"]["jatuh_tempo"], "2026-10-01")     # termin default 30 hari
        self.assertTrue(o["pelanggan_baru"])
        self.assertTrue(any("termin 30" in p for p in o["peringatan"]))
        o = self.catat("Toko Maju", "INV-2", "10/09/2026", "1jt", termin=14)
        self.assertEqual(o["nota"]["jatuh_tempo"], "2026-09-24")
        self.assertEqual(o["saldo_pelanggan"], 3500000)
        o = self.catat("P0001", "INV-3", "10/09/2026", "1jt", jt="45 hari")
        self.assertEqual(o["nota"]["jatuh_tempo"], "2026-10-25")

    def test_nomor_dobel_dan_nomor_otomatis(self):
        self.catat("Toko Maju", "INV-1", "01/09/2026", "100rb")
        o = self.gagal("catat", "--pelanggan", "Toko Maju", "--nota", "inv 1", "--nominal", "5rb")
        self.assertTrue(o.get("duplikat"))
        a = self.ok("catat", "--pelanggan", "Toko Maju", "--nominal", "5rb")
        b = self.ok("catat", "--pelanggan", "Toko Maju", "--nominal", "6rb")
        self.assertEqual((a["nota"]["no_nota"], b["nota"]["no_nota"]), ("PB-0001", "PB-0002"))

    def test_nama_mirip_ditanyakan_bukan_ditebak(self):
        self.catat("Pak Joko Susilo", "N1", "20/09/2026", "100rb")
        o = self.gagal("catat", "--pelanggan", "Pak Joko Susila", "--nota", "N2", "--nominal", "5rb")
        self.assertTrue(o.get("mirip"))
        o = self.gagal("catat", "--pelanggan", "Joko", "--nota", "N2", "--nominal", "5rb")
        self.assertTrue(o.get("ambigu"))
        self.ok("catat", "--pelanggan", "Pak Joko Susila", "--nota", "N2", "--nominal", "5rb", "--pelanggan-baru")
        self.assertEqual(self.hitung("SELECT COUNT(*) FROM pelanggan"), 2)

    def test_tanggal_dan_jatuh_tempo_ngawur(self):
        s = self.sha()
        self.gagal("catat", "--pelanggan", "A", "--tanggal", "27/09/2026", "--nominal", "1rb")        # masa depan
        self.gagal("catat", "--pelanggan", "A", "--tanggal", "10/25/2026", "--nominal", "1rb")
        self.gagal("catat", "--pelanggan", "A", "--tanggal", "20/09/2026", "--jatuh-tempo", "10/09/2026",
                   "--nominal", "1rb")
        self.gagal("catat", "--pelanggan", "A", "--tanggal", "20/09/2026", "--jatuh-tempo", "30", "--nominal",
                   "1rb")                                                                           # 30 apa?
        self.gagal("catat", "--pelanggan", "A", "--termin", "500", "--nominal", "1rb")
        self.gagal("catat", "--pelanggan", "A", "--termin", "7", "--jatuh-tempo", "1/10/2026", "--nominal", "1rb")
        self.gagal("catat", "--pelanggan", "=cmd()", "--nominal", "1rb")
        self.assertEqual(self.hitung("SELECT COUNT(*) FROM nota"), 0)
        self.assertEqual(s, self.sha())

    def test_ppn_lewat_dpp(self):
        o = self.ok("catat", "--pelanggan", "CV Maju", "--nota", "F1", "--dpp", "999.999", "--ppn", "11")
        self.assertEqual((o["dpp"], o["ppn"], o["nota"]["nominal"]), (999999, 109999, 1109998))
        self.assertTrue(any("Coretax" in p for p in o["peringatan"]))
        self.gagal("catat", "--pelanggan", "CV Maju", "--nominal", "1jt", "--ppn", "11")
        self.gagal("catat", "--pelanggan", "CV Maju", "--dpp", "1jt")


class UjiBayar(Dasar):
    def siapkan(self):
        # N1 jt 1 Sep (lewat), N2 jt 20 Sep (lewat), N3 jt 10 Okt
        self.catat("Toko Maju", "N2", "01/09/2026", "800rb", jt="20/09/2026")
        self.catat("Toko Maju", "N1", "01/08/2026", "500rb", jt="01/09/2026")
        self.catat("Toko Maju", "N3", "20/09/2026", "1jt", jt="10/10/2026")

    def test_alokasi_jatuh_tempo_tertua_dulu(self):
        self.siapkan()
        o = self.ok("bayar", "--pelanggan", "Toko Maju", "--jumlah", "1jt")
        # 1.000.000 -> N1 500.000 (lunas) + N2 500.000 (sisa 300.000)
        self.assertEqual([(a["no_nota"], a["jumlah"], a["sisa_nota"]) for a in o["alokasi"]],
                         [("N1", 500000, 0), ("N2", 500000, 300000)])
        self.assertEqual(o["saldo_pelanggan"], 1300000)          # 2.300.000 - 1.000.000

    def test_bayar_nota_tertentu_dan_lunas(self):
        self.siapkan()
        o = self.ok("bayar", "--nota", "N3", "--jumlah", "lunas")
        self.assertEqual(o["jumlah"], 1000000)
        self.assertEqual(o["alokasi"][0]["sisa_nota"], 0)
        self.gagal("bayar", "--nota", "N3", "--jumlah", "1rb")          # sudah lunas
        self.ok("bayar", "--pelanggan", "Toko Maju", "--jumlah", "lunas", "--tanggal", "kemarin")
        self.assertEqual(self.ok("saldo", "--pelanggan", "P0001")["piutang"], 0)

    def test_kelebihan_bayar_tidak_pernah_diam_diam(self):
        self.siapkan()
        s = self.sha()
        o = self.gagal("bayar", "--pelanggan", "Toko Maju", "--jumlah", "2,5jt")
        self.assertEqual(o["kelebihan"], 200000)                  # 2.500.000 - 2.300.000
        o = self.gagal("bayar", "--nota", "N1", "--jumlah", "600rb")
        self.assertEqual(o["kelebihan"], 100000)
        self.assertIn("nota-lain", o["error"])
        self.assertEqual(s, self.sha())                           # tidak ada yang tersimpan
        o = self.ok("bayar", "--nota", "N1", "--jumlah", "600rb", "--kelebihan", "nota-lain")
        self.assertEqual([(a["no_nota"], a["jumlah"]) for a in o["alokasi"]], [("N1", 500000), ("N2", 100000)])
        o = self.ok("bayar", "--pelanggan", "Toko Maju", "--jumlah", "2jt", "--kelebihan", "kredit",
                    "--tanggal", "25/09/2026")
        # sisa sebelum: 2.300.000 - 600.000 = 1.700.000 -> kelebihan 300.000 jadi deposit
        self.assertEqual((o["kelebihan_disimpan"], o["kredit_pelanggan"], o["saldo_pelanggan"]), (300000, 300000, 0))
        s = self.ok("saldo", "--pelanggan", "P0001")
        self.assertEqual((s["piutang"], s["kredit"], s["saldo_bersih"]), (0, 300000, -300000))
        self.assertIn("DEPOSIT", self.ok("bayar", "--pelanggan", "P0001", "--jumlah", "1rb", "--kelebihan",
                                         "kredit")["teks"])

    def test_kelebihan_dikembalikan(self):
        self.catat("Bu Rina", "R1", "20/09/2026", "450rb")
        o = self.ok("bayar", "--pelanggan", "Bu Rina", "--jumlah", "500rb", "--kelebihan", "kembalikan")
        self.assertEqual((o["kelebihan_dikembalikan"], o["kredit_pelanggan"]), (50000, 0))

    def test_deposit_dipakai_dan_dikembalikan(self):
        self.catat("Bu Rina", "R1", "20/09/2026", "450rb")
        self.ok("bayar", "--pelanggan", "Bu Rina", "--jumlah", "1jt", "--kelebihan", "kredit")   # deposit 550.000
        self.catat("Bu Rina", "R2", "25/09/2026", "300rb")
        o = self.ok("pakai-kredit", "--pelanggan", "Bu Rina")
        self.assertEqual((o["dipakai"], o["kredit_pelanggan"], o["saldo_pelanggan"]), (300000, 250000, 0))
        self.gagal("kembalikan", "--pelanggan", "Bu Rina", "--jumlah", "300rb")      # > deposit 250.000
        o = self.ok("kembalikan", "--pelanggan", "Bu Rina", "--jumlah", "semua")
        self.assertEqual((o["jumlah"], o["kredit_pelanggan"]), (250000, 0))
        self.gagal("pakai-kredit", "--pelanggan", "Bu Rina")

    def test_pembayaran_dobel_ditolak(self):
        self.siapkan()
        self.ok("bayar", "--pelanggan", "Toko Maju", "--jumlah", "100rb")
        self.gagal("bayar", "--pelanggan", "Toko Maju", "--jumlah", "100rb")
        self.ok("bayar", "--pelanggan", "Toko Maju", "--jumlah", "100rb", "--izinkan-dobel")
        self.gagal("bayar", "--pelanggan", "Toko Maju", "--jumlah", "100rb", "--tanggal", "besok")
        self.gagal("bayar", "--pelanggan", "Tidak Ada", "--jumlah", "100rb")
        self.gagal("bayar", "--nota", "N1", "--pelanggan", "Orang Lain", "--jumlah", "1rb")

    def test_invarian_nominal_tidak_boleh_di_bawah_dibayar(self):
        self.siapkan()
        self.ok("bayar", "--nota", "N3", "--jumlah", "700rb")
        s = self.sha()
        o = self.gagal("ubah-nota", "--nota", "N3", "--nominal", "500rb")
        self.assertTrue(o.get("invarian"))
        self.assertEqual(s, self.sha())
        o = self.ok("ubah-nota", "--nota", "N3", "--nominal", "900rb")
        self.assertEqual(o["nota"]["sisa"], 200000)

    def test_batal_bayar_dan_batal_nota(self):
        self.siapkan()
        b = self.ok("bayar", "--pelanggan", "Toko Maju", "--jumlah", "600rb")["kode"]
        s = self.sha()
        self.ok("batal-bayar", "--bayar", b, "--alasan", "salah catat")          # pratinjau
        self.assertEqual(s, self.sha())
        o = self.ok("batal-bayar", "--bayar", b, "--alasan", "salah catat", "--ya")
        self.assertEqual(o["saldo_pelanggan"], 2300000)
        self.assertTrue(os.path.isfile(o["backup"]))
        self.gagal("batal-bayar", "--bayar", b, "--alasan", "lagi", "--ya")
        self.ok("bayar", "--nota", "N3", "--jumlah", "400rb")
        o = self.ok("batal-nota", "--nota", "N3", "--alasan", "dobel", "--ya")
        self.assertEqual(o["dibayar_jadi_deposit"], 400000)
        s = self.ok("saldo", "--pelanggan", "P0001")
        self.assertEqual((s["piutang"], s["kredit"]), (1300000, 400000))
        self.gagal("bayar", "--nota", "N3", "--jumlah", "1rb")                      # nota batal

    def test_batal_bayar_yang_sudah_dikembalikan_ditolak(self):
        self.catat("Bu Rina", "R1", "20/09/2026", "100rb")
        b = self.ok("bayar", "--pelanggan", "Bu Rina", "--jumlah", "300rb", "--kelebihan", "kredit")["kode"]
        self.ok("kembalikan", "--pelanggan", "Bu Rina", "--jumlah", "200rb")
        o = self.gagal("batal-bayar", "--bayar", b, "--alasan", "x", "--ya")
        self.assertTrue(o.get("invarian"))

    def test_potong_pratinjau_lalu_simpan(self):
        self.siapkan()
        s = self.sha()
        o = self.ok("potong", "--nota", "N2", "--jumlah", "50rb", "--alasan", "retur 1 dus")
        self.assertTrue(o["perlu_konfirmasi"])
        self.assertEqual(s, self.sha())
        o = self.ok("potong", "--nota", "N2", "--jumlah", "50rb", "--alasan", "retur 1 dus", "--ya")
        self.assertEqual(o["sisa_nota"], 750000)
        self.gagal("potong", "--nota", "N2", "--jumlah", "800rb", "--alasan", "x", "--ya")
        self.ok("potong", "--nota", "N2", "--jumlah", "sisa", "--alasan", "diikhlaskan", "--ya")
        self.assertEqual(self.ok("saldo", "--pelanggan", "P0001")["piutang"], 1500000)


# --------------------------------------------------------------------------- laporan
class UjiLaporan(Dasar):
    def setUp(self):
        super().setUp()
        # jatuh tempo relatif thd 26 Sep 2026
        self.catat("Warung Bu Tini", "A", "01/05/2026", "100rb", jt="27/06/2026", wa="0812-0000-2001")  # 91 hari
        self.catat("Warung Bu Tini", "B", "01/06/2026", "200rb", jt="28/06/2026")    # 90 hari -> 61_90
        self.catat("CV Maju", "C", "01/07/2026", "300rb", jt="28/07/2026")           # 60 -> 31_60
        self.catat("CV Maju", "D", "01/08/2026", "400rb", jt="27/08/2026")           # 30 -> 1_30
        self.catat("Pak Joko", "E", "01/09/2026", "500rb", jt="26/09/2026")          # 0 -> hari ini
        self.catat("Pak Joko", "F", "20/09/2026", "600rb", jt="03/10/2026")          # -7 -> minggu ini
        self.catat("Pak Joko", "G", "20/09/2026", "700rb", jt="04/10/2026")          # -8 -> belum, bukan minggu ini

    def test_umur_dan_persen(self):
        u = self.ok("umur")
        um = u["umur"]
        self.assertEqual(u["total_piutang"], 2800000)
        self.assertEqual(um["lebih_90"]["nominal"], 100000)
        self.assertEqual(um["61_90"]["nominal"], 200000)
        self.assertEqual(um["31_60"]["nominal"], 300000)
        self.assertEqual(um["1_30"]["nominal"], 400000)
        self.assertEqual(um["belum_jatuh_tempo"]["nominal"], 1800000)       # 500+600+700 rb
        self.assertIn("64,3%", u["teks"])                                   # 1.800.000/2.800.000 = 64,2857 -> 64,3

    def test_jatuh_tempo_kelompok(self):
        j = self.ok("jatuh-tempo")
        self.assertEqual([n["no_nota"] for n in j["terlewat"]], ["A", "B", "C", "D"])
        self.assertEqual([n["no_nota"] for n in j["hari_ini"]], ["E"])
        self.assertEqual([n["no_nota"] for n in j["minggu_ini"]], ["F"])
        self.assertEqual(j["ringkasan"]["terlewat"]["nominal"], 1000000)

    def test_posisi_per_tanggal(self):
        self.ok("bayar", "--nota", "A", "--jumlah", "lunas", "--tanggal", "25/09/2026")
        s = self.ok("saldo", "--per", "24/09/2026")
        self.assertEqual(s["total_piutang"], 2800000)               # pembayaran 25/9 belum ada per 24/9
        self.assertEqual(self.ok("saldo")["total_piutang"], 2700000)
        u = self.ok("umur", "--per", "31/07/2026")                  # hanya A, B, C yang sudah terbit
        self.assertEqual(u["total_piutang"], 600000)
        # A: 31/7 - 27/6 = 34 hari, B: 31/7 - 28/6 = 33 hari -> 31_60 ; C: 31/7 - 28/7 = 3 hari -> 1_30
        self.assertEqual(u["umur"]["31_60"]["nominal"], 300000)
        self.assertEqual(u["umur"]["1_30"]["nominal"], 300000)

    def test_rekap_json_kontrak(self):
        self.ok("bayar", "--nota", "E", "--jumlah", "200rb")
        self.ok("potong", "--nota", "F", "--jumlah", "100rb", "--alasan", "retur", "--ya")
        r = self.ok("rekap", "--periode", "bulan-ini")
        for k in ("skema_json", "periode", "arus_periode", "posisi", "jatuh_tempo", "teratas_terlewat", "rumus"):
            self.assertIn(k, r)
        self.assertEqual(r["skema_json"], 1)
        self.assertEqual(r["arus_periode"]["nota_baru"], {"jumlah": 3, "nominal": 1800000})   # E, F, G
        self.assertEqual(r["arus_periode"]["pembayaran_masuk"], {"jumlah": 1, "nominal": 200000})
        self.assertEqual(r["arus_periode"]["potongan"]["nominal"], 100000)
        self.assertEqual(r["posisi"]["per"], HARI)
        self.assertEqual(r["posisi"]["total_piutang"], 2500000)     # 2.800.000 - 200.000 - 100.000
        self.assertEqual(r["teratas_terlewat"][0]["kode"], "P0002")  # CV Maju 700.000 terlewat
        rl = self.ok("rekap", "--periode", "bulan-lalu")
        self.assertEqual(rl["posisi"]["per"], "2026-08-31")
        self.assertEqual(rl["posisi"]["total_piutang"], 1000000)     # A+B+C+D

    def test_samarkan_tanpa_nama_dan_nomor(self):
        for cmd in (["ringkasan", "--samarkan"], ["jatuh-tempo", "--samarkan"], ["saldo", "--samarkan"],
                    ["umur", "--samarkan"], ["rekap", "--samarkan"], ["saldo", "--pelanggan", "P0001", "--samarkan"]):
            o = self.ok(*cmd)
            dump = json.dumps(o, ensure_ascii=False)
            for rahasia in ("Tini", "Joko", "Maju", "0000-2001", "6281200002001"):
                self.assertNotIn(rahasia, dump, cmd)
            self.assertFalse(o["data_sensitif"])

    def test_laporan_tidak_mengubah_database(self):
        s = self.sha()
        for cmd in (["ringkasan"], ["jatuh-tempo"], ["saldo"], ["umur"], ["rekap", "--rumus"], ["info"],
                    ["draf", "--pelanggan", "P0001"], ["saldo", "--pelanggan", "Joko"]):
            self.ok(*cmd)
        self.assertEqual(s, self.sha())

    def test_draf_nada_dan_tautan(self):
        d = self.ok("draf", "--pelanggan", "Warung Bu Tini")
        self.assertEqual(d["jenis"], "terlewat-lama")
        self.assertTrue(d["draf"].startswith("Halo Bu Tini"))
        self.assertIn("BCA 0000000000", d["draf"])
        self.assertIn("bertahap", d["draf"])
        self.assertEqual(unquote(d["tautan_wa"].split("text=", 1)[1]), d["draf"])
        self.assertTrue(d["saran"])                                # > 14 hari -> saran tagih-piutang
        for kasar in ("polisi", "pidana", "viral", "sebar", "denda"):
            self.assertNotIn(kasar, d["draf"].lower())
        d = self.ok("draf", "--pelanggan", "Pak Joko")
        self.assertEqual(d["jenis"], "hari-jatuh-tempo")          # E hari ini, F dalam 7 hari; G tidak ikut
        self.assertEqual([n["no_nota"] for n in d["nota"]], ["E", "F"])
        self.assertIsNone(d["tautan_wa"])
        d = self.ok("draf", "--nota", "G")
        self.assertEqual(d["jenis"], "pengingat-awal")
        self.ok("bayar", "--nota", "G", "--jumlah", "lunas")
        self.gagal("draf", "--nota", "G")

    def test_terkirim_dihitung_sekali_per_hari(self):
        o = self.ok("terkirim", "--pelanggan", "Pak Joko")
        self.assertEqual(o["nota"], ["E", "F"])
        self.gagal("terkirim", "--pelanggan", "Pak Joko")
        self.ok("terkirim", "--pelanggan", "Pak Joko", hari="2026-09-28")
        d = self.ok("jatuh-tempo", hari="2026-09-28")
        self.assertEqual([n["diingatkan"] for n in d["terlewat"] if n["no_nota"] == "E"], [2])


# --------------------------------------------------------------------------- impor & ekspor
CSV_NOTA = """No Invoice;Nama Pelanggan;Tanggal;Jatuh Tempo;Total;Dibayar;No HP;Status
INV-101;Toko Makmur;05/09/2026;19/09/2026;Rp 2.400.000;500.000;0813-0000-3001;Belum Lunas
INV-102;Toko Makmur;15/09/2026;;1.750.000;;;Tempo
INV-103;Bu Rina;20/09/2026;30 hari;650.000;;081200003002;belum lunas
INV-104;Kafe Senja;21/09/2026;05/10/2026;1.200.000;1.200.000;;Lunas
INV-105;Kafe Senja;22/09/2026;06/10/2026;480.000;;;Void
INV-106;=HYPERLINK("x");23/09/2026;07/10/2026;100.000;;;belum lunas
INV-107;Toko Makmur;31/09/2026;07/10/2026;100.000;;;belum lunas
INV-108;Pak Budi;24/09/2026;01/10/2026;-50.000;;;belum lunas
INV-109;Pak Budi;24/09/2026;01/10/2026;2.500.000;3.000.000;;belum lunas
INV-110;Pak Budi;24/09/2026;01/10/2026;300.000;;;kartu kredit
INV-111;Pak Budi;24/09/2026;01/10/2026;300.000;;;entah
INV-112;Pak Budi;27/09/2026;01/10/2026;300.000;;;belum lunas
"""


class UjiImpor(Dasar):
    def test_pratinjau_lalu_simpan(self):
        f = self.file("nota.csv", CSV_NOTA)
        s = self.sha()
        o = self.ok("impor", f)
        self.assertTrue(o["perlu_konfirmasi"])
        self.assertEqual(s, self.sha())
        # dicatat: 101 (2.400.000, dibayar 500.000), 102 (1.750.000), 103 (650.000)
        self.assertEqual((o["jumlah_nota"], o["total"], o["sisa"]), (3, 4800000, 4300000))
        self.assertEqual(o["dilewati"], {"sudah_ada": 0, "lunas": 2, "batal": 1})       # 104, 110 lunas; 105 void
        self.assertEqual(sorted(m["baris"] for m in o["masalah"]), [7, 8, 9, 10, 12, 13])
        o = self.ok("impor", f, "--ya")
        self.assertTrue(os.path.isfile(o["backup"]))
        s2 = self.ok("saldo")
        self.assertEqual(s2["total_piutang"], 4300000)
        n = {x["no_nota"]: x for x in self.ok("saldo", "--pelanggan", "Toko Makmur")["nota_terbuka"]}
        self.assertEqual(n["INV-102"]["jatuh_tempo"], "2026-10-15")        # termin default 30 hari
        self.assertEqual(n["INV-101"]["sisa"], 1900000)
        # impor ulang file yang sama: tidak dobel
        o = self.ok("impor", f, "--ya")
        self.assertEqual((o["jumlah_nota"], o["dilewati"]["sudah_ada"]), (0, 3))
        self.assertEqual(self.ok("saldo")["total_piutang"], 4300000)

    def test_format_amerika_dan_campur_ditolak_seluruhnya(self):
        us = self.file("us.csv", "invoice,customer,date,due date,amount\nA1,Joe,09/25/2026,10/25/2026,100000\n"
                                 "A2,Ann,03/09/2026,04/08/2026,200000\n")
        o = self.gagal("impor", us)
        self.assertEqual(o["format_tanggal"], "bulan-hari")
        o = self.ok("impor", us, "--format-tanggal", "bulan-hari", "--ya")
        self.assertEqual(o["jumlah_nota"], 2)
        self.assertEqual(self.ok("saldo", "--pelanggan", "Ann")["nota_terbuka"][0]["tanggal"], "2026-03-09")
        campur = self.file("c.csv", "nota,pelanggan,tanggal,total\nX1,A,25/09/2026,1000\nX2,B,09/25/2026,1000\n")
        self.assertEqual(self.gagal("impor", campur)["format_tanggal"], "campur")
        self.gagal("impor", campur, "--format-tanggal", "bulan-hari")

    def test_file_per_barang_digabung(self):
        f = self.file("kasir.csv", "No Transaksi,Tanggal,Pelanggan,Produk,Total,Status\n"
                                   "T1,2026-09-20 10:00:00,Bu Ani,Beras,150000,Tempo\n"
                                   "T1,2026-09-20 10:00:00,Bu Ani,Minyak,45000,Tempo\n"
                                   "T2,2026-09-20 11:00:00,Pak Edi,Gula,30000,Tunai\n")
        o = self.ok("impor", f)
        self.assertEqual(o["jumlah_nota"], 1)
        self.assertIn("gabung-baris", o["masalah"][0]["alasan"])
        o = self.ok("impor", f, "--gabung-baris", "--ya")
        self.assertEqual((o["jumlah_nota"], o["total"], o["dilewati"]["lunas"]), (1, 195000, 1))

    def test_tanpa_nomor_nota_tidak_dobel(self):
        f = self.file("bon.csv", "pelanggan,tanggal,nominal\nBu Ani,20/09/2026,50rb\nBu Ani,20/09/2026,50rb\n"
                                 "Bu Ani,21/09/2026,70rb\n")
        o = self.ok("impor", f, "--ya")
        self.assertEqual(o["jumlah_nota"], 2)
        self.assertEqual(len(o["masalah"]), 1)
        o = self.ok("impor", f, "--ya")
        self.assertEqual(o["jumlah_nota"], 0)

    def test_file_rusak(self):
        self.gagal("impor", os.path.join(self.dir, "tidak-ada.csv"))
        self.gagal("impor", self.file("x.xlsx", "PK"))
        p = os.path.join(self.dir, "bin.csv")
        with open(p, "wb") as f:
            f.write(b"\x00\x01\x02nota")
        self.gagal("impor", p)
        self.gagal("impor", self.file("kosong.csv", ""))
        self.gagal("impor", self.file("judul.csv", "pelanggan;tanggal;nominal\n"))
        o = self.gagal("impor", self.file("kolom.csv", "a;b;c\n1;2;3\n"))
        self.assertIn("Kolom wajib", o["error"])
        o = self.ok("impor", self.file("ansi.csv", "pelanggan;tanggal;nominal\nJos\xe9;20/09/2026;10000\n",
                                       encoding="cp1252"))
        self.assertTrue(any("Windows-1252" in p for p in o["peringatan"]))
        o = self.ok("impor", self.file("kutip.csv", 'pelanggan,tanggal,nominal\n"Bu Ani,20/09/2026,1000\n'
                                                     'Pak B,20/09/2026,2000\n'))
        self.assertTrue(any("tanda kutip" in p for p in o["peringatan"]))
        o = self.ok("impor", self.file("excel.csv", "pelanggan;tanggal;nominal\nBu A;46291;1000\nBu B;20/09/2026;"
                                                    "6.28E+12\n"))
        self.assertEqual(len(o["masalah"]), 2)

    def test_ekspor_aman_dan_cocok_tagih_piutang(self):
        self.catat("Toko Makmur", "INV-1", "01/09/2026", "2,4jt", jt="19/09/2026")
        self.catat("Bu Rina", "INV-2", "20/09/2026", "650rb")
        self.ok("bayar", "--nota", "INV-1", "--jumlah", "500rb")
        self.ok("potong", "--nota", "INV-1", "--jumlah", "100rb", "--alasan", "retur", "--ya")
        self.ok("ubah-pelanggan", "--pelanggan", "Bu Rina", "--nama", "-Rina @rumah")
        tuju = os.path.join(self.dir, "lengkap.csv")
        o = self.ok("ekspor", "--ke", tuju)
        with open(tuju, encoding="utf-8-sig") as f:
            isi = f.read()
        self.assertIn("'-Rina", isi)                              # dilindungi dari formula injection
        self.gagal("ekspor", "--ke", tuju)                         # tidak menimpa tanpa --timpa
        self.gagal("ekspor", "--ke", os.path.join(self.dir, "x.db"))
        tp = os.path.join(self.dir, "tagih.csv")
        self.ok("ekspor", "--format", "tagih-piutang", "--ke", tp)
        skrip = os.path.join(os.path.dirname(AKAR), "tagih-piutang", "scripts", "hitung_telat.py")
        if not os.path.isfile(skrip):
            self.skipTest("skill tagih-piutang tidak ada di sebelah buku-piutang")
        r = subprocess.run([sys.executable, skrip, "--file", tp, "--tanggal", HARI], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        # sisa INV-1 = 2.400.000 - 500.000 - 100.000 = 1.800.000 ; INV-2 650.000 -> total 2.450.000
        self.assertIn("Rp 2.450.000", r.stdout)
        self.assertIn("Rp 1.800.000", r.stdout)
        o = self.ok("ekspor", "--samarkan", "--ke", os.path.join(self.dir, "samar.csv"))
        with open(o["file"], encoding="utf-8-sig") as f:
            self.assertNotIn("Makmur", f.read())


# --------------------------------------------------------------------------- keamanan data
class UjiKeamananData(Dasar):
    def test_init_tidak_menimpa(self):
        self.gagal("init", "--ya")
        lain = self.file("bukan.db", "halo")
        self.gagal("init", "--ya", db=lain)
        with open(lain, encoding="utf-8") as f:
            self.assertEqual(f.read(), "halo")

    def test_database_rusak_restore_aman(self):
        self.catat("Toko Maju", "N1", "20/09/2026", "1jt")
        cad = self.ok("backup")["backup"]
        self.catat("Toko Maju", "N2", "21/09/2026", "2jt")
        with open(self.db, "r+b") as f:
            f.write(b"RUSAK" * 40)
        o = self.gagal("saldo")
        self.assertTrue(o.get("rusak"))
        self.gagal("catat", "--pelanggan", "X", "--nominal", "1rb")
        self.gagal("restore", "--dari", self.file("palsu.db", "bukan database"))
        o = self.ok("restore", "--dari", cad)
        self.assertEqual(o["status_db"], "rusak")
        o = self.ok("restore", "--dari", cad, "--ya")
        self.assertTrue(os.path.basename(o["backup"]).startswith("rusak-piutang-"))
        self.assertTrue(os.path.isfile(o["backup"]))              # file rusak dipindah, tidak dihapus
        self.assertEqual(self.ok("saldo")["total_piutang"], 1000000)

    def test_rusak_tanpa_cadangan_mulai_baru(self):
        with open(self.db, "wb") as f:
            f.write(b"x" * 100)
        self.gagal("init", "--ya")
        o = self.ok("init", "--mulai-baru", "--ya")
        self.assertIn("rusak-piutang", o["teks"])
        self.assertEqual(self.ok("saldo")["total_piutang"], 0)

    def test_database_kosong_nol_byte(self):
        open(self.db, "wb").close()
        self.assertTrue(self.gagal("saldo").get("rusak"))

    def test_bukan_database_buku_piutang(self):
        lain = os.path.join(self.dir, "lain.db")
        c = sqlite3.connect(lain)
        c.execute("CREATE TABLE meta(kunci TEXT, nilai TEXT)")
        c.execute("INSERT INTO meta VALUES ('aplikasi','crm-wa')")
        c.commit()
        c.close()
        s = self.sha(lain)
        self.gagal("saldo", db=lain)
        self.gagal("restore", "--dari", self.db, "--ya", db=lain)
        self.assertEqual(s, self.sha(lain))

    def test_database_terkunci(self):
        c = sqlite3.connect(self.db, isolation_level=None)
        c.execute("BEGIN EXCLUSIVE")
        os.environ["KOMUNITECH_PIUTANG_TIMEOUT"] = "0.2"
        try:
            o = self.gagal("catat", "--pelanggan", "A", "--nominal", "1rb")
            self.assertIn("sedang dipakai", o["error"])
        finally:
            os.environ.pop("KOMUNITECH_PIUTANG_TIMEOUT", None)
            c.execute("ROLLBACK")
            c.close()

    def test_cadangan_harian_otomatis(self):
        self.catat("A", "N1", "20/09/2026", "1rb")
        fol = os.path.join(self.dir, "backup-piutang")
        self.assertEqual(len([f for f in os.listdir(fol) if "harian" in f]), 1)
        self.catat("A", "N2", "20/09/2026", "2rb")
        self.assertEqual(len([f for f in os.listdir(fol) if "harian" in f]), 1)      # sekali sehari
        self.ok("catat", "--pelanggan", "A", "--nota", "N4", "--nominal", "4rb", hari="2026-09-27")
        self.assertEqual(len([f for f in os.listdir(fol) if "harian" in f]), 2)

    def test_perintah_salah_tulis(self):
        with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit) as c:
            P.main(["bayar", "--db", self.db])
        self.assertEqual(c.exception.code, 2)


class UjiScript(unittest.TestCase):
    def test_tanpa_akses_jaringan_dan_perintah_sistem(self):
        with open(os.path.join(AKAR, "scripts", "piutang.py"), encoding="utf-8") as f:
            src = f.read()
        for terlarang in ("import socket", "urllib.request", "http.client", "import requests", "subprocess",
                          "smtplib", "webbrowser", "os.system", "eval(", "exec("):
            self.assertNotIn(terlarang, src)



class UjiSingkatanFlag(unittest.TestCase):
    """Regresi keamanan: argparse tidak boleh menerima singkatan flag konfirmasi (mis. --y untuk --ya)."""

    def test_singkatan_flag_konfirmasi_ditolak(self):
        import subprocess
        import tempfile
        skrip = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scripts", "piutang.py")
        with tempfile.TemporaryDirectory() as t:
            argv = ["init", "--db", os.path.join(t, "a.db"), "--y"]
            p = subprocess.run([sys.executable, skrip] + argv, capture_output=True, text=True, timeout=60)
            self.assertNotEqual(p.returncode, 0, p.stdout + p.stderr)
            self.assertIn("unrecognized arguments", p.stdout + p.stderr)
            self.assertFalse(os.path.exists(os.path.join(t, "a.db")), "singkatan flag tidak boleh menulis apa pun")


if __name__ == "__main__":
    unittest.main(verbosity=1)
