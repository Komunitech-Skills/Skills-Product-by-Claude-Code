#!/usr/bin/env python3
"""Uji regresi segmentasi.py. Jalankan: python3 tests/uji_regresi.py (Python standar)."""
import os
import sys
import tempfile
import unittest
from datetime import date
from decimal import Decimal

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AKAR, "scripts"))
import segmentasi as S  # noqa: E402

DATA = os.path.join(AKAR, "examples", "data-contoh.csv")
HARI = date(2026, 10, 5)


def tulis(isi, enc="utf-8"):
    f = tempfile.NamedTemporaryFile("wb", suffix=".csv", delete=False)
    f.write(isi.encode(enc))
    f.close()
    return f.name


class TesParse(unittest.TestCase):
    def test_tanggal(self):
        self.assertEqual(S.parse_tanggal("05/10/2026")[0], date(2026, 10, 5))
        self.assertEqual(S.parse_tanggal("5-10-2026")[0], date(2026, 10, 5))
        self.assertEqual(S.parse_tanggal("2026-10-05")[0], date(2026, 10, 5))
        self.assertEqual(S.parse_tanggal("5 Oktober 2026")[0], date(2026, 10, 5))
        self.assertEqual(S.parse_tanggal("17 Agu 2026")[0], date(2026, 8, 17))
        self.assertEqual(S.parse_tanggal("03/11/25")[0], date(2025, 11, 3))
        self.assertEqual(S.parse_tanggal("05/10/2026 14:30")[0], date(2026, 10, 5))

    def test_tanggal_dd_mm_bukan_mm_dd(self):
        # 03/11 = 3 November (bukan 11 Maret)
        self.assertEqual(S.parse_tanggal("03/11/2025")[0], date(2025, 11, 3))
        self.assertIsNone(S.parse_tanggal("11/25/2026")[0])  # bulan 25 tidak ada

    def test_tanggal_rusak(self):
        for t in ["", "kemarin", "31/02/2026", "00/01/2026", "2026/13/01", "abc 12"]:
            self.assertIsNone(S.parse_tanggal(t)[0], t)

    def test_rupiah(self):
        kasus = {"Rp 1.250.000": 1250000, "1250000": 1250000, "1,250,000": 1250000,
                 "Rp1.250.000,50": 1250001, "IDR 500.000": 500000, "0": 0, "1250000,5": 1250001}
        for t, v in kasus.items():
            self.assertEqual(S.parse_rupiah(t)[0], Decimal(v), t)
        for t in ["", "tidak ada", "-5000", "Rp", "1.2.3"]:
            self.assertIsNone(S.parse_rupiah(t)[0], t)

    def test_hp(self):
        for t in ["0812-3456-7801", "+62 812 3456 7801", "6281234567801", "81234567801",
                  "0062 812 3456 7801", "+62 0812 3456 7801"]:
            self.assertEqual(S.normalisasi_hp(t)[0], "6281234567801", t)
        for t in ["", "abc", "08123", "8.12346E+11", "021-5551234", "62812345678012345"]:
            self.assertIsNone(S.normalisasi_hp(t)[0], t)


class TesSegmen(unittest.TestCase):
    def test_batas(self):
        self.assertIsNone(S.segmen_untuk(44, 45))
        self.assertEqual(S.segmen_untuk(45, 45)[0], "A")
        self.assertEqual(S.segmen_untuk(90, 45)[0], "A")
        self.assertEqual(S.segmen_untuk(91, 45)[0], "B")
        self.assertEqual(S.segmen_untuk(180, 45)[0], "B")
        self.assertEqual(S.segmen_untuk(181, 45)[0], "C")
        self.assertEqual(S.segmen_untuk(365, 45)[0], "C")
        self.assertEqual(S.segmen_untuk(366, 45)[0], "D")


class TesProses(unittest.TestCase):
    def jalankan(self, **kw):
        a = dict(path=DATA, hari_ini=HARI, ambang=45, per_hari=10, mulai=HARI,
                 kecuali_nomor=set(), kecuali_nama=set(), target_balik=Decimal(10))
        a.update(kw)
        return S.proses(**a)

    def test_angka_data_contoh_diverifikasi_independen(self):
        h = self.jalankan()
        # Hitung ulang manual (tanpa memakai fungsi script) dari data-contoh.csv
        # (hari sejak 2026-10-05, total): segmen A 45-90, B 91-180, C 181-365, D >=366
        harapan = {"A": (3, 3230000), "B": (7, 7340000), "C": (6, 3975000), "D": (2, 1580000)}
        for r in h["ringkas"]:
            self.assertEqual((r["jumlah"], int(r["potensi"])), harapan[r["kode"]], r["kode"])
        self.assertEqual(sum(int(r["potensi"]) for r in h["ringkas"]), 16125000)
        self.assertEqual(int(h["ringkas"][1]["rata_rata"]), 1048571)  # 7.340.000 / 7
        self.assertEqual(int(h["ringkas"][0]["skenario_omzet"]), 323000)  # 10% dari 3.230.000
        self.assertEqual(len(h["ditolak"]), 5)
        self.assertEqual(h["aktif"], 5)

    def test_jadwal_aturan(self):
        h = self.jalankan()
        per_hari = {}
        for p in h["sasaran"]:
            d1, d2, d3 = p["jadwal"]
            self.assertGreaterEqual((d2 - d1).days, S.JEDA_PESAN2)
            self.assertGreaterEqual((d3 - d2).days, S.JEDA_PESAN3)
            self.assertLessEqual((d3 - d1).days, 28)
            for d in p["jadwal"]:
                self.assertNotEqual(d.weekday(), 6)  # tidak ada hari Minggu
                per_hari[d] = per_hari.get(d, 0) + 1
        self.assertLessEqual(max(per_hari.values()), 10)
        # nilai tertinggi diutamakan
        self.assertEqual(h["sasaran"][0]["nama"], "Bu Maryam")

    def test_duplikat_digabung(self):
        h = self.jalankan()
        self.assertTrue(any("digabung" in w for w in h["peringatan"]))

    def test_pengecualian(self):
        h = self.jalankan(kecuali_nomor={"6281234567805"}, kecuali_nama={"pak agus"})
        nama = [p["nama"] for p in h["sasaran"]]
        self.assertNotIn("Bu Wati", nama)
        self.assertNotIn("Pak Agus", nama)
        self.assertEqual(len(h["dikecualikan"]), 2)

    def test_semicolon_cp1252_dan_alias(self):
        isi = "Nama;WA;Terakhir Beli;Total\nBu Sri;0812 3456 7801;1 Januari 2026;Rp 1.000.000\n"
        h = self.jalankan(path=tulis(isi, "cp1252"))
        self.assertEqual(h["dipakai"], 1)
        self.assertEqual(h["sasaran"][0]["kode"], "C")  # 277 hari

    def test_kolom_produk_terakhir(self):
        isi = ("nama,no_hp,tanggal_beli_terakhir,total_belanja,produk\n"
               "Bu Sari,081234567801,01/03/2026,2000000,Kue lapis\n"
               "Bu Sari,081234567801,01/06/2026,2500000,Brownies\n"
               "Pak Eko,081234567802,01/06/2026,500000,\n")
        h = self.jalankan(path=tulis(isi))
        per_nama = {p["nama"]: p for p in h["sasaran"]}
        self.assertEqual(per_nama["Bu Sari"]["produk"], "Brownies")  # pembelian terbaru
        self.assertEqual(int(per_nama["Bu Sari"]["total"]), 4500000)
        self.assertEqual(per_nama["Pak Eko"]["produk"], "")
        self.assertIn("Brownies", S.cetak(h))
        # tanpa kolom produk tetap jalan
        self.assertEqual(self.jalankan()["sasaran"][0]["produk"], "")

    def test_kolom_wajib_hilang(self):
        with self.assertRaises(ValueError) as cm:
            self.jalankan(path=tulis("nama,telepon\nA,0812\n"))
        self.assertIn("tanggal", str(cm.exception))

    def test_file_kosong_dan_biner(self):
        with self.assertRaises(ValueError):
            self.jalankan(path=tulis(""))
        f = tempfile.NamedTemporaryFile("wb", suffix=".csv", delete=False)
        f.write(b"PK\x03\x04\x00\x00xlsx"); f.close()
        with self.assertRaises(ValueError):
            self.jalankan(path=f.name)

    def test_semua_aktif(self):
        isi = "nama,no_hp,tanggal_beli_terakhir,total_belanja\nA,081234567890,01/10/2026,1000\n"
        h = self.jalankan(path=tulis(isi))
        self.assertEqual(h["sasaran"], [])
        self.assertIn("tidak ada pelanggan pasif", S.cetak(h))

    def test_main_kode_keluar(self):
        self.assertEqual(S.main(["tidak-ada.csv"]), 2)
        self.assertEqual(S.main([DATA, "--hari-ini", "bukan-tanggal"]), 2)
        self.assertEqual(S.main([DATA, "--hari-ini", "2026-10-05", "--target-balik", "150"]), 2)


if __name__ == "__main__":
    unittest.main(verbosity=1)
