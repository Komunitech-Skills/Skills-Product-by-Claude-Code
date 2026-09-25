#!/usr/bin/env python3
"""Uji regresi tender-checklist. Jalankan: python3 tests/uji_regresi.py  (Windows: py tests/uji_regresi.py)

Angka pembanding dihitung MANUAL di komentar (independen dari script):
  jumlah baris = volume x harga satuan, bulat ke rupiah terdekat
  PPN non-mewah = floor(DPP x 12% x 11/12) = floor(DPP x 11/100)
  PPN mewah     = floor(DPP x 12/100)
  termasuk PPN: DPP = bulat terbesar dengan DPP + floor(DPP x 11/100) <= harga
Kalender Oktober 2026: 1 = Kamis; 3/10/17 = Sabtu; 4/11/18 = Minggu. 25 Sep 2026 = Jumat.
"""
import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from datetime import date, datetime
from decimal import Decimal

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(AKAR, "scripts"))
import cek_penawaran as C  # noqa: E402


class Dasar(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.dir, ignore_errors=True)

    def tulis(self, isi, nama="r.csv", enc="utf-8"):
        p = os.path.join(self.dir, nama)
        with open(p, "w", encoding=enc, newline="") as f:
            f.write(isi)
        return p

    def cli(self, *argv):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            kode = C.main(list(argv))
        return kode, out.getvalue(), err.getvalue()


class UjiAngka(unittest.TestCase):
    def test_parse(self):
        kasus = {"Rp1.250.000,00": 1250000, "Rp 25.000,-": 25000, "1,5": Decimal("1.5"), "1.500": 1500,
                 "2.5": Decimal("2.5"), "15,000.50": Decimal("15000.50"), "1,250,000": 1250000,
                 "250rb": 250000, "1,5jt": 1500000, "30jt": 30000000, "Rp. 7.875.000": 7875000}
        for teks, harap in kasus.items():
            self.assertEqual(C.parse_angka(teks), Decimal(harap), teks)
        for buruk in ("", "abc", "Rp", "-", None):
            with self.assertRaises(C.InputSalah):
                C.parse_angka(buruk)

    def test_terbilang(self):
        self.assertEqual(C.terbilang(0), "Nol Rupiah")
        self.assertEqual(C.terbilang(1000), "Seribu Rupiah")
        self.assertEqual(C.terbilang(111), "Seratus Sebelas Rupiah")
        self.assertEqual(C.terbilang(44142480),
                         "Empat Puluh Empat Juta Seratus Empat Puluh Dua Ribu Empat Ratus Delapan Puluh Rupiah")
        self.assertEqual(C.terbilang(1_015_000_000), "Satu Miliar Lima Belas Juta Rupiah")
        self.assertEqual(C.terbilang(2_001_019), "Dua Juta Seribu Sembilan Belas Rupiah")

    def test_ppn_bawah_dan_dpp(self):
        # 1.234.567 x 11/100 = 135.802,37 -> 135.802
        self.assertEqual(C.ppn_bawah(1234567, C.TARIF["nonmewah"]), 135802)
        # 1.234.567 x 12/100 = 148.148,04 -> 148.148
        self.assertEqual(C.ppn_bawah(1234567, C.TARIF["mewah"]), 148148)
        # 11.100.000 / 1,11 = 10.000.000 ; PPN 1.100.000 ; sisa 0
        self.assertEqual(C.dpp_dari_bruto(11100000, C.TARIF["nonmewah"]), 10000000)
        # 1.000.000: DPP 900.901 -> PPN floor(99.099,11)=99.099 -> 999.999+... cek: 900.901+99.099=1.000.000
        self.assertEqual(C.dpp_dari_bruto(1000000, C.TARIF["nonmewah"]), 900901)
        # 100: DPP 90 -> PPN 9 (99); DPP 91 -> PPN 10 (101 > 100) -> 90, sisa 1
        self.assertEqual(C.dpp_dari_bruto(100, C.TARIF["nonmewah"]), 90)


class UjiHarga(Dasar):
    CSV = ("No;Uraian;Volume;Satuan;Harga Satuan\n"
           "1;Kertas HVS A4 70 gsm;150;rim;Rp52.500\n"
           "2;Tinta printer original hitam;24;botol;Rp1.250.000,00\n"
           "3;Map snelhecter plastik;500;buah;Rp3.750\n"
           "4;Paper clip no.3;1,5;lusin;12.000\n")

    def test_normal_ppn_nonmewah(self):
        # 150x52.500=7.875.000 ; 24x1.250.000=30.000.000 ; 500x3.750=1.875.000 ; 1,5x12.000=18.000
        # subtotal 39.768.000 ; PPN floor(39.768.000x0,11)=4.374.480 ; total 44.142.480
        # HPS 50.000.000 -> 88,28% (44.142.480/50.000.000 = 0,8828496)
        h = C.hitung(self.tulis(self.CSV), "nonmewah", hps=50_000_000)
        self.assertEqual([i["jumlah"] for i in h["item"]], [7875000, 30000000, 1875000, 18000])
        self.assertEqual(h["subtotal"], 39768000)
        self.assertEqual(h["ppn"], 4374480)
        self.assertEqual(h["total"], 44142480)
        self.assertEqual(h["persen_hps"], Decimal("88.28"))
        self.assertEqual(h["batas_80_hps"], 40_000_000)
        self.assertFalse(h["peringatan"])

    def test_di_bawah_80_persen(self):
        # 44.142.480 / 60.000.000 = 73,57% (< 80%) ; batas 80% = 48.000.000
        h = C.hitung(self.tulis(self.CSV), "nonmewah", hps=60_000_000)
        self.assertEqual(h["persen_hps"], Decimal("73.57"))
        self.assertTrue(any("KEWAJARAN HARGA" in p for p in h["peringatan"]))
        self.assertTrue(any("5% dari nilai HPS" in p for p in h["peringatan"]))

    def test_tepat_80_persen_tidak_diperingatkan(self):
        # total 40.000.000 tanpa PPN, HPS 50.000.000 -> tepat 80,00%
        p = self.tulis("Uraian;Volume;Satuan;Harga Satuan\nJasa kebersihan;4;bulan;10.000.000\n")
        h = C.hitung(p, "tidak", hps=50_000_000)
        self.assertEqual(h["persen_hps"], Decimal("80.00"))
        self.assertFalse(any("KEWAJARAN" in x for x in h["peringatan"]))

    def test_melebihi_hps(self):
        h = C.hitung(self.tulis(self.CSV), "nonmewah", hps=44_000_000)
        self.assertTrue(any("MELEBIHI HPS" in p for p in h["peringatan"]))
        self.assertEqual(h["selisih_hps"], 44_000_000 - 44_142_480)

    def test_termasuk_ppn(self):
        # 3 x 3.700.000 = 11.100.000 -> DPP 10.000.000, PPN 1.100.000, sisa 0
        p = self.tulis("Uraian;Volume;Satuan;Harga Satuan\nLaptop;3;unit;3.700.000\n")
        h = C.hitung(p, "nonmewah", termasuk_ppn=True)
        self.assertEqual((h["dpp"], h["ppn"], h["total"], h["sisa_pembulatan"]), (10000000, 1100000, 11100000, 0))
        # 1 x 1.000.000 -> DPP 900.901, PPN 99.099, sisa 0
        p2 = self.tulis("Uraian;Volume;Satuan;Harga Satuan\nPrinter;1;unit;1.000.000\n", "b.csv")
        h2 = C.hitung(p2, "nonmewah", termasuk_ppn=True)
        self.assertEqual((h2["dpp"], h2["ppn"], h2["sisa_pembulatan"]), (900901, 99099, 0))

    def test_mewah(self):
        # 2 x 617.283,50 = 1.234.567 ; PPN floor(1.234.567 x 0,12) = 148.148 ; total 1.382.715
        p = self.tulis("Uraian;Volume;Satuan;Harga Satuan\nBarang X;2;unit;617.283,50\n")
        h = C.hitung(p, "mewah")
        self.assertEqual((h["subtotal"], h["ppn"], h["total"]), (1234567, 148148, 1382715))

    def test_pembulatan_baris(self):
        # 3 x 333,33 = 999,99 -> 1.000 ; 0,5 x 1.001 = 500,5 -> 501 (0,5 naik)
        p = self.tulis("Uraian;Volume;Satuan;Harga Satuan\nA;3;m;333,33\nB;0,5;m;1.001\n")
        h = C.hitung(p)
        self.assertEqual([i["jumlah"] for i in h["item"]], [1000, 501])
        self.assertEqual(h["total"], 1501)

    def test_koma_tanpa_kutip_diperbaiki(self):
        # "Rp450.000,00" tanpa kutip di CSV koma -> terpecah; harus digabung kembali
        # 40 x 450.000 = 18.000.000 ; 2 x 1.250.000 = 2.500.000 ; total 20.500.000
        p = self.tulis('Uraian,Volume,Satuan,Harga Satuan\nKursi lipat,40,unit,Rp450.000,00\n'
                       'Meja,2,unit,"Rp1.250.000,00"\n')
        h = C.hitung(p)
        self.assertEqual(h["subtotal"], 20500000)
        self.assertFalse(h["baris_bermasalah"])

    def test_sel_kosong_dan_baris_total(self):
        p = self.tulis("Uraian;Volume;Satuan;Harga Satuan\n"
                       "A. PEKERJAAN PERSIAPAN;;;\n"
                       "Papan nama proyek;1;ls;750.000\n"
                       "Lemari arsip;;unit;2.000.000\n"
                       ";;;\n"
                       "Jumlah;;;750.000\n"
                       "PPN 11%;;;82.500\n"
                       "Total;;;999.999\n")
        h = C.hitung(p, "nonmewah")
        self.assertEqual(h["subtotal"], 750000)          # hanya papan nama
        self.assertEqual(h["ppn"], 82500)                 # 750.000 x 0,11
        self.assertEqual(len(h["baris_bermasalah"]), 1)   # lemari tanpa volume
        self.assertTrue(any("BELUM FINAL" in x for x in h["peringatan"]))
        self.assertTrue(any("'Jumlah'" in x and "cocok" in x for x in h["info"]))
        self.assertTrue(any("'Total'" in x and "TIDAK cocok" in x for x in h["peringatan"]))
        self.assertTrue(any("judul bagian" in x for x in h["baris_dilewati"]))

    def test_tanpa_header_dan_tab(self):
        p = self.tulis("1\tSemen 50 kg\t100\tsak\t65.000\n2\tPasir\t2,5\tm3\t350.000\n")
        h = C.hitung(p)
        # 100 x 65.000 = 6.500.000 ; 2,5 x 350.000 = 875.000 ; total 7.375.000
        self.assertEqual(h["total"], 7375000)
        self.assertTrue(h["catatan"])

    def test_hps_per_baris(self):
        p = self.tulis("Uraian;Volume;Satuan;Harga Satuan;Harga Satuan HPS\nA;1;u;110.000;100.000\n")
        h = C.hitung(p)
        self.assertEqual(h["item"][0]["persen_hps"], Decimal("110.00"))
        self.assertTrue(h["info"])

    def test_input_buruk_tanpa_traceback(self):
        kasus = ["", "Uraian;Volume;Satuan;Harga Satuan\n", "Uraian;Volume;Satuan;Harga Satuan\nA;dua;u;x\n",
                 "Uraian;Volume;Satuan;Harga Satuan\nA;-1;u;1000\n", "foo\nbar\n"]
        for i, isi in enumerate(kasus):
            kode, out, err = self.cli("harga", self.tulis(isi, f"b{i}.csv"))
            self.assertEqual(kode, 1, isi)
            self.assertIn("GALAT", err)
            self.assertNotIn("Traceback", err)
        kode, _, err = self.cli("harga", os.path.join(self.dir, "tidak-ada.csv"))
        self.assertEqual(kode, 1)
        kode, _, err = self.cli("harga", self.tulis(self.CSV, "ok.csv"), "--hps", "abc")
        self.assertEqual(kode, 1)

    def test_encoding_cp1252_dan_bom(self):
        p = self.tulis("Uraian;Volume;Satuan;Harga Satuan\nKabel 2,5 mm²;10;roll;500.000\n", enc="cp1252")
        self.assertEqual(C.hitung(p)["total"], 5000000)
        p2 = self.tulis("﻿Uraian;Volume;Satuan;Harga Satuan\nA;1;u;1.000\n", "bom.csv")
        self.assertEqual(C.hitung(p2)["total"], 1000)

    def test_cli_teks_dan_json(self):
        p = self.tulis(self.CSV)
        kode, out, _ = self.cli(p, "--ppn", "nonmewah", "--hps", "Rp 50.000.000", "--pagu", "50jt")
        self.assertEqual(kode, 0)
        self.assertIn("Rp44.142.480", out)
        self.assertIn("88,28%", out)
        self.assertIn("Coretax", out)
        self.assertIn("Pasal 65", out)
        kode, out, _ = self.cli("harga", p, "--ppn", "nonmewah", "--json")
        d = json.loads(out)
        self.assertEqual(d["total"], 44142480)

    def test_jaminan_penawaran_info(self):
        p = self.tulis("Uraian;Volume;Satuan;Harga Satuan\nGedung;1;ls;10.500.000.000\n")
        h = C.hitung(p, hps=11_000_000_000)
        self.assertTrue(any("JAMINAN PENAWARAN" in x for x in h["info"]))


class UjiJadwal(Dasar):
    def test_hari_kerja_dan_libur(self):
        # batas Kamis 15-10-2026, libur Senin 12-10.
        # mundur hari kerja: H-1 Rabu 14, H-2 Selasa 13, (12 libur), H-3 Jumat 9, H-4 Kamis 8, H-5 Rabu 7,
        # H-6 Selasa 6, H-7 Senin 5.
        j = C.jadwal(datetime(2026, 10, 15, 14, 0), date(2026, 9, 25), libur={date(2026, 10, 12)})
        t = {x["kode"]: x["tanggal"] for x in j["tugas"]}
        self.assertEqual(t["H-1"], date(2026, 10, 14))
        self.assertEqual(t["H-2"], date(2026, 10, 13))
        self.assertEqual(t["H-3"], date(2026, 10, 9))
        self.assertEqual(t["H-5"], date(2026, 10, 7))
        self.assertEqual(t["H-7"], date(2026, 10, 5))
        # sisa hari kerja 25/9 s.d. 14/10: Sep 25,28,29,30 (4) + Okt 1,2,5-9 (7) + 13,14 (2) = 13
        self.assertEqual(j["sisa_hari_kerja"], 13)
        self.assertFalse(j["peringatan"])

    def test_tanpa_libur_dan_sabtu_kerja(self):
        j = C.jadwal(datetime(2026, 10, 15), date(2026, 9, 25))
        t = {x["kode"]: x["tanggal"] for x in j["tugas"]}
        self.assertEqual(t["H-3"], date(2026, 10, 12))   # Senin (tanpa libur)
        self.assertEqual(t["H-7"], date(2026, 10, 6))
        j2 = C.jadwal(datetime(2026, 10, 15), date(2026, 9, 25), sabtu=True)
        t2 = {x["kode"]: x["tanggal"] for x in j2["tugas"]}
        self.assertEqual(t2["H-3"], date(2026, 10, 12))  # 14,13,12
        self.assertEqual(t2["H-5"], date(2026, 10, 9))   # 14,13,12,10(Sabtu),9
        self.assertEqual(t2["H-7"], date(2026, 10, 7))

    def test_terlewat_dan_mepet(self):
        j = C.jadwal(datetime(2026, 10, 15), date(2026, 10, 13))
        st = {x["kode"]: x["status"] for x in j["tugas"]}
        self.assertTrue(st["H-3"].startswith("TERLEWAT"))
        self.assertEqual(st["H-2"], "HARI INI")
        self.assertEqual(j["sisa_hari_kerja"], 2)
        self.assertTrue(any("Sisa hanya 2" in p for p in j["peringatan"]))

    def test_batas_di_akhir_pekan_dan_penjelasan(self):
        j = C.jadwal(datetime(2026, 10, 17), date(2026, 9, 25), penjelasan=datetime(2026, 10, 2))
        self.assertTrue(any("hari libur/akhir pekan" in p for p in j["peringatan"]))
        t = {x["kode"]: x["tanggal"] for x in j["tugas"]}
        self.assertEqual(t["Penjelasan+1"], date(2026, 10, 5))  # Jumat 2 -> Senin 5

    def test_cli_jadwal(self):
        f = self.tulis("2026-10-12\n2026-10-13\n", "libur.txt")
        kode, out, _ = self.cli("jadwal", "--batas", "15/10/2026 14.00", "--hari-ini", "2026-09-25",
                                "--libur", f, "--konstruksi", "--jaminan")
        self.assertEqual(kode, 0)
        self.assertIn("pukul 14:00", out)
        self.assertIn("SBU", out)
        self.assertIn("JAMINAN PENAWARAN", out)
        # libur 12 & 13 -> H-1 14, H-2 9
        self.assertIn("H-2          Jumat, 9 Oktober 2026", out)
        kode, _, err = self.cli("jadwal", "--batas", "kapan-kapan")
        self.assertEqual(kode, 1)
        self.assertNotIn("Traceback", err)
        kode, _, err = self.cli("jadwal", "--batas", "2026-10-15", "--libur", "32-13-2026")
        self.assertEqual(kode, 1)


if __name__ == "__main__":
    unittest.main(verbosity=1)
