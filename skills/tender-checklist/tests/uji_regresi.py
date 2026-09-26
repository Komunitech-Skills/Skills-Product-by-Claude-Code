#!/usr/bin/env python3
"""Uji regresi tender-checklist. Jalankan: python3 tests/uji_regresi.py  (Windows: py tests/uji_regresi.py)

Angka pembanding dihitung MANUAL di komentar (independen dari script):
  jumlah baris = volume x harga satuan, bulat ke rupiah terdekat
  PPN non-mewah = floor(DPP x 12% x 11/12) = floor(DPP x 11/100)
  PPN mewah     = floor(DPP x 12/100)
  termasuk PPN: DPP = bulat terbesar dengan DPP + floor(DPP x 11/100) <= harga
Kode keluar (v1.0.2): 0 bersih, 1 ada PERINGATAN, 2 input buruk (GALAT), 3 TOTAL BELUM FINAL.
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
        # v1.0.1 (temuan 5): kontrak Rp44 jt <= Rp200 jt -> jaminan pelaksanaan umumnya tidak diberlakukan
        self.assertFalse(any("5% dari nilai HPS" in p for p in h["peringatan"]))
        self.assertTrue(any("s.d. Rp200 juta" in p for p in h["peringatan"]))

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
            self.assertEqual(kode, 2, isi)
            self.assertIn("GALAT", err)
            self.assertNotIn("Traceback", err)
        kode, _, err = self.cli("harga", os.path.join(self.dir, "tidak-ada.csv"))
        self.assertEqual(kode, 2)
        kode, _, err = self.cli("harga", self.tulis(self.CSV, "ok.csv"), "--hps", "abc")
        self.assertEqual(kode, 2)

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


BARIS_S03 = ("1;Kursi kerja staf jaring;120;unit;Rp1.185.000;Rp142.200.000\n"
             "2;Meja kerja 120x60 cm;60;unit;Rp1.640.000;Rp98.400.000\n"
             "3;Lemari arsip besi 4 laci;25;unit;Rp2.975.000;Rp47.375.000\n"
             "4;Rak buku 5 susun;30;unit;Rp1.210.000;Rp36.300.000\n"
             "5;Ongkos kirim & pasang;1;ls;Rp17.500.000;Rp17.500.000\n")
HEADER_S03 = "No;Uraian;Volume;Satuan;Harga Satuan;Jumlah\n"


class UjiPengunci(Dasar):
    """Mengunci hitungan yang sudah benar di v1.0.0 (tidak boleh berubah). Angka dihitung manual."""

    def test_skenario_03_angka_inti(self):
        # 142.200.000 + 98.400.000 + 74.375.000 + 36.300.000 + 17.500.000 = 368.775.000
        # PPN floor(368.775.000 x 11/100) = 40.565.250 ; total 409.340.250
        # 409.340.250 / 538.000.000 = 76,0855% -> 76,09% ; 80% HPS = 430.400.000 ; 5% HPS = 26.900.000
        h = C.hitung(self.tulis(HEADER_S03 + BARIS_S03), "nonmewah", hps=538_000_000)
        self.assertEqual((h["subtotal"], h["ppn"], h["total"]), (368775000, 40565250, 409340250))
        self.assertEqual(h["persen_hps"], Decimal("76.09"))
        self.assertEqual(h["batas_80_hps"], 430400000)
        self.assertEqual(h["terbilang"], "Empat Ratus Sembilan Juta Tiga Ratus Empat Puluh Ribu Dua Ratus Lima Puluh Rupiah")
        self.assertTrue(any("Rp26.900.000" in p and "5% dari nilai HPS" in p for p in h["peringatan"]))

    def test_skenario_01_angka_inti(self):
        # dari uji independen skenario 01: subtotal 163.545.400 -> PPN floor(x0,11)=17.989.994 -> 181.535.394
        # 181.535.394 / 185.000.000 = 98,127% -> 98,13%
        p = self.tulis("Uraian;Volume;Satuan;Harga Satuan\nPaket ATK;1;ls;163.545.400\n")
        h = C.hitung(p, "nonmewah", hps=185_000_000)
        self.assertEqual((h["ppn"], h["total"], h["persen_hps"]), (17989994, 181535394, Decimal("98.13")))
        self.assertFalse(h["peringatan"])
        # kontrak > Rp200 jt? tidak (181 jt) -> tidak ada info jaminan pelaksanaan
        self.assertFalse(any("jaminan pelaksanaan" in x for x in h["info"]))

    def test_termasuk_ppn_brute_force(self):
        # DPP = bulat terbesar dengan DPP + floor(DPP x 11/100) <= harga (cek brute force)
        for bruto in (1, 100, 111, 999, 1000, 12345, 1000000, 11100000, 7777777):
            d = C.dpp_dari_bruto(bruto, C.TARIF["nonmewah"])
            self.assertLessEqual(d + d * 11 // 100, bruto)
            self.assertGreater(d + 1 + (d + 1) * 11 // 100, bruto)
            dm = C.dpp_dari_bruto(bruto, C.TARIF["mewah"])
            self.assertLessEqual(dm + dm * 12 // 100, bruto)
            self.assertGreater(dm + 1 + (dm + 1) * 12 // 100, bruto)

    def test_jadwal_skenario_02(self):
        # batas Jumat 23/10/2026, libur Selasa 20/10, hari ini Kamis 15/10
        j = C.jadwal(datetime(2026, 10, 23, 10, 0), date(2026, 10, 15), pengumuman=datetime(2026, 10, 5),
                     penjelasan=datetime(2026, 10, 12), libur={date(2026, 10, 20)}, konstruksi=True)
        t = {x["kode"]: x["tanggal"] for x in j["tugas"]}
        self.assertEqual([t[k] for k in ("H-1", "H-2", "H-3", "H-5", "H-7", "Penjelasan+1")],
                         [date(2026, 10, 22), date(2026, 10, 21), date(2026, 10, 19), date(2026, 10, 15),
                          date(2026, 10, 13), date(2026, 10, 13)])
        self.assertEqual(j["sisa_hari_kerja"], 5)


class UjiRegresiV101(Dasar):
    """Tes regresi temuan HASIL-UJI v1.0.0 (data repro penguji)."""

    def test_bug1_total_tanpa_ppn_tidak_boleh_cocok(self):
        # PKP, 1 x 5.000.000 -> PPN 550.000 -> total 5.550.000 ; file menulis Total 5.000.000 (lupa PPN)
        p = self.tulis("Uraian;Volume;Satuan;Harga Satuan\nJasa;1;ls;5.000.000\nTotal;;;5.000.000\n")
        h = C.hitung(p, "nonmewah")
        self.assertFalse(any("cocok" in x and "'Total'" in x for x in h["info"]))
        w = [x for x in h["peringatan"] if "'Total'" in x]
        self.assertEqual(len(w), 1)
        self.assertIn("BELUM TERMASUK PPN", w[0])
        self.assertIn("Rp5.550.000", w[0])   # sesudah PPN
        self.assertIn("Rp5.000.000", w[0])   # sebelum PPN
        for label in ("Grand Total", "Total Penawaran", "Jumlah Total"):
            p2 = self.tulis(f"Uraian;Volume;Satuan;Harga Satuan\nJasa;1;ls;5.000.000\n{label};;;5.000.000\n", "g.csv")
            h2 = C.hitung(p2, "nonmewah")
            self.assertTrue(any("BELUM TERMASUK PPN" in x for x in h2["peringatan"]), label)

    def test_bug1_label_dicocokkan_sesuai_basis(self):
        csv_ = "Uraian;Volume;Satuan;Harga Satuan\nJasa;1;ls;5.000.000\n"
        # Total benar (sesudah PPN) -> cocok ; PPN benar -> cocok ; Jumlah = sebelum PPN -> cocok
        h = C.hitung(self.tulis(csv_ + "Jumlah;;;5.000.000\nPPN;;;550.000\nTotal;;;5.550.000\n"), "nonmewah")
        self.assertFalse(h["peringatan"])
        self.assertEqual(sum("cocok" in x for x in h["info"]), 3)
        # PPN diisi angka subtotal -> TIDAK boleh cocok ; Jumlah diisi total sesudah PPN -> diperingatkan
        h = C.hitung(self.tulis(csv_ + "Jumlah;;;5.550.000\nPPN;;;5.000.000\n", "b.csv"), "nonmewah")
        self.assertFalse(any("cocok" in x for x in h["info"]))
        self.assertTrue(any("'PPN'" in x and "Rp550.000" in x for x in h["peringatan"]))
        self.assertTrue(any("'Jumlah'" in x and "SESUDAH PPN" in x for x in h["peringatan"]))
        # bukan PKP: Total = 5.000.000 memang benar
        h = C.hitung(self.tulis(csv_ + "Total;;;5.000.000\n", "c.csv"), "tidak")
        self.assertTrue(any("cocok" in x for x in h["info"]))
        # termasuk PPN: 'Jumlah' 5.000.000 = harga termasuk PPN -> cocok, disebut basisnya
        h = C.hitung(self.tulis(csv_ + "Jumlah;;;5.000.000\n", "d.csv"), "nonmewah", termasuk_ppn=True)
        self.assertTrue(any("SUDAH TERMASUK PPN" in x for x in h["info"]))

    def test_bug2_baris_salah_hitung_ditunjuk(self):
        h = C.hitung(self.tulis(HEADER_S03 + BARIS_S03), "nonmewah", hps=538_000_000)
        self.assertEqual(len(h["selisih_baris"]), 1)
        s = h["selisih_baris"][0]
        self.assertEqual((s["item"], s["baris_file"], s["jumlah_file"], s["jumlah_hitung"], s["selisih"]),
                         (3, 4, 47375000, 74375000, 27000000))
        self.assertEqual(h["subtotal"], 368775000)   # script tetap memakai volume x harga
        out = C.tampil_harga(h)
        self.assertIn("Baris salah hitung", out)
        self.assertIn("file Rp47.375.000 != hitung 25 x Rp2.975.000 = Rp74.375.000 (selisih Rp27.000.000)", out)

    def test_bug2_pembulatan_bukan_salah_hitung_dan_sinonim(self):
        # 3 x 333,33 = 999,99 ; file menulis 1.000 (atau 999,99) -> bukan salah hitung (< Rp1)
        p = self.tulis("Uraian;Qty;Satuan;Harga Satuan;Total Harga\nA;3;m;333,33;1.000\nB;3;m;333,33;999,99\n"
                       "C;2;m;1.000;Rp2.000,-\nD;1;m;1.000;abc\n")
        h = C.hitung(p)
        self.assertEqual(h["selisih_baris"], [])
        self.assertTrue(any("tidak terbaca" in x for x in h["info"]))
        self.assertEqual(h["total"], 1000 + 1000 + 2000 + 1000)

    def test_bug2_judul_jumlah_berarti_banyaknya(self):
        # tanpa kolom Volume, "Jumlah" = banyaknya barang: 10 x 5.000 = 50.000
        p = self.tulis("Uraian;Jumlah;Satuan;Harga Satuan\nPulpen;10;buah;5.000\n")
        h = C.hitung(p)
        self.assertEqual(h["total"], 50000)
        self.assertTrue(any("VOLUME" in x for x in h["catatan"]))

    def test_bug3_total_di_kolom_lain(self):
        # repro varian A: ';;;;TOTAL;Rp341.775.000' -> bukan 'uraian kosong', bukan TOTAL BELUM FINAL
        p = self.tulis(HEADER_S03 + BARIS_S03 + ";;;;TOTAL;Rp341.775.000\n")
        h = C.hitung(p, "nonmewah", hps=538_000_000)
        self.assertFalse(h["baris_bermasalah"])
        self.assertFalse(h["total_belum_final"])
        self.assertFalse(any("BELUM FINAL" in x for x in h["peringatan"]))
        self.assertTrue(any("'TOTAL'" in x for x in h["baris_dilewati"]))
        self.assertTrue(any("'TOTAL'" in x and "Rp409.340.250" in x for x in h["peringatan"]))
        self.assertEqual(h["total"], 409340250)
        kode, out, _ = self.cli("harga", p, "--ppn", "nonmewah", "--hps", "Rp538.000.000")
        self.assertEqual(kode, 1)   # v1.0.2: ada PERINGATAN -> kode 1

    def test_bug3_label_di_kolom_no_dan_ppn_lengkap(self):
        # repro varian C: label di kolom No -> label tidak boleh '' ; varian B: pesan PPN menampilkan PPN script
        p = self.tulis("No;Uraian;Volume;Satuan;Harga Satuan\n1;Kursi;120;unit;Rp1.185.000\n"
                       "Total (dari Excel);;;;Rp379.370.250\n")
        h = C.hitung(p, "nonmewah")
        self.assertTrue(any("'Total (dari Excel)'" in x for x in h["baris_dilewati"]))
        self.assertFalse(any("''" in x for x in h["baris_dilewati"]))
        p2 = self.tulis(HEADER_S03 + BARIS_S03 + ";Jumlah;;;;Rp341.775.000\n;PPN 11%;;;;Rp37.595.250\n"
                        ";Total;;;;Rp379.370.250\n", "b.csv")
        h2 = C.hitung(p2, "nonmewah", hps=538_000_000)
        ppn = [x for x in h2["peringatan"] if "'PPN 11%'" in x][0]
        self.assertIn("Rp40.565.250", ppn)
        self.assertIn("selisih Rp2.970.000", ppn)
        self.assertEqual(len(h2["selisih_baris"]), 1)

    def test_bug4_hps_miliar(self):
        for teks, harap in (("2,4 M", 2_400_000_000), ("Rp2,4 miliar", 2_400_000_000), ("2.4M", 2_400_000_000),
                            ("2,4 milyar", 2_400_000_000), ("Rp 1,25 M", 1_250_000_000), ("185jt", 185_000_000),
                            ("Rp538.000.000", 538_000_000)):
            self.assertEqual(C.parse_angka(teks, "HPS", besar=True), Decimal(harap), teks)
        with self.assertRaises(C.InputSalah):   # 'm' = meter pada volume/harga baris, bukan miliar
            C.parse_angka("2,4 M")
        p = self.tulis("Uraian;Volume;Satuan;Harga Satuan\nGedung;1;ls;2.000.000.000\n")
        kode, out, _ = self.cli("harga", p, "--hps", "2,4 M", "--pagu", "Rp2,5 miliar")
        self.assertEqual(kode, 0)
        self.assertIn("Rp2.400.000.000", out)
        self.assertIn("83,33%", out)   # 2.000.000.000 / 2.400.000.000

    def test_temuan5_jaminan_pelaksanaan_di_atas_200jt(self):
        # total 250 jt, HPS 300 jt -> 83,33% (>= 80%) -> info 5% nilai kontrak = 12.500.000
        p = self.tulis("Uraian;Volume;Satuan;Harga Satuan\nMebel;1;ls;250.000.000\n")
        h = C.hitung(p, hps=300_000_000)
        self.assertTrue(any("Rp12.500.000" in x and "5% dari nilai kontrak" in x for x in h["info"]))

    def test_temuan7_exit_code_belum_final(self):
        p = self.tulis("Uraian;Volume;Satuan;Harga Satuan\nA;1;u;1.000\nB;;u;2.000\n")
        kode, out, _ = self.cli("harga", p)
        self.assertEqual(kode, 3)
        self.assertIn("TOTAL BELUM FINAL", out)

    def test_temuan6_label_acara_lewat(self):
        j = C.jadwal(datetime(2026, 10, 23, 10, 0), date(2026, 10, 15), pengumuman=datetime(2026, 10, 5),
                     penjelasan=datetime(2026, 10, 12))
        st = {x["kode"]: x["status"] for x in j["tugas"]}
        self.assertTrue(st["Pengumuman"].startswith("SUDAH LEWAT"))
        self.assertIn("Berita Acara", st["Penjelasan"])
        self.assertTrue(st["H-7"].startswith("TERLEWAT"))


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
        self.assertEqual(kode, 2)
        self.assertNotIn("Traceback", err)
        kode, _, err = self.cli("jadwal", "--batas", "2026-10-15", "--libur", "32-13-2026")
        self.assertEqual(kode, 2)


# ---------------------------------------------------------------- v1.0.2
# 13 CSV buatan penguji independen uji ulang v1.0.1 (examples/06-uji-ulang-v1.0.1.md, lampiran; TAB asli).
CSV_PENGUJI = {
    "t01": ('No,Uraian Pekerjaan,Vol,Sat,Harga Satuan (Rp),Jumlah Harga (Rp)\n'
        '\n'
        '1,Galian tanah pondasi,"2,5",m3,"Rp 1.250.000,-","Rp 3.125.000,-"\n'
        '2,Pasangan batu kali,"12,75",m3,"Rp 985.500,-","Rp 12.565.125,-"\n'
        '\n'
        '3,Plester dinding,"48,6",m2,"Rp 62.350,-","Rp 3.030.210,-"\n'
        '4,Mobilisasi,1,ls,"Rp 4.500.000,-","Rp 4.500.000,-"\n'
        ',Sub Total,,,,"Rp 23.220.335,-"\n'
        ',PPN 12% (DPP 11/12),,,,"Rp 2.554.236,-"\n'
        ',Grand Total,,,,"Rp 25.774.571,-"\n'),
    "t02": ('No;Nama Barang;Qty;Satuan;Harga Satuan;Jumlah\n'
        '1;Laptop 14 inci i5;4;unit;Rp 12.350.000;Rp 49.400.000\n'
        '2;Printer laser A4;2;unit;Rp 3.275.000;Rp 6.550.000\n'
        '3;Kabel LAN Cat6;305;m;Rp 4.250;Rp 1.296.250\n'
        ';Jumlah Total;;;;Rp 57.246.250\n'),
    "t03": ('Uraian;Volume;Satuan;Harga Satuan;Jumlah\n'
        'Seragam dinas PDH;150;stel;Rp 385.000;Rp 57.750.000\n'
        'Topi lapangan;150;buah;Rp 45.500;Rp 6.825.000\n'
        'Sepatu PDL;150;pasang;Rp 412.000;Rp 61.800.000\n'
        'PPN 12%;;;;Rp 15.169.800\n'
        'TOTAL + PPN 12%;;;;Rp 141.544.800\n'),
    "t04": ('No;Uraian;Volume;Satuan;Harga Satuan;Jumlah\n'
        '1;Cat tembok 25 kg;40;pail;Rp1.150.000;Rp46.000.000\n'
        '2;Kuas 4 inci;60;buah;Rp27.500;Rp1.650.000\n'
        '3;Rol cat;60;buah;Rp48.750;Rp2.295.000\n'
        '4;Amplas;200;lembar;Rp3.200;Rp640.000\n'
        '5;Thinner;35;liter;Rp32.000;Rp1.120.000\n'
        ';;;;Jumlah;Rp51.705.000\n'
        ';;;;PPN 11%;Rp5.687.550\n'
        ';;;;Total;Rp57.392.550\n'),
    "t05": ('Uraian;Volume;Satuan;Harga Satuan;Jumlah\n'
        'Kabel NYM 3x2,5;2,5;roll;1.333;3.333\n'
        'Pipa conduit;0,75;batang;12.345;9.259\n'
        'Besi beton 10 mm;37,5;batang;98.765,50;3.703.706\n'
        'Upah pasang;3,25;OH;175.555;570.554\n'
        'Subtotal;;;;4.286.852\n'),
    "t06": ('Uraian;Volume;Satuan;Harga Satuan\n'
        'Kursi lipat;75;unit;Rp 287.600\n'
        'Meja lipat;25;unit;Rp 1.118.900\n'
        'Tenda 3x3;4;unit;Rp 5.745.000\n'
        'DPP;;;\n'
        'PPN;;;\n'
        'Total (termasuk PPN);;;Rp 72.522.500\n'),
    "t07": ('1;Pekerjaan persiapan;1;ls;45.000.000\n'
        '2;Pekerjaan beton K-250;312,5;m3;1.485.000\n'
        '3;Pekerjaan besi tulangan;28.750;kg;16.450\n'
        '4;Pekerjaan bekisting;1.120;m2;235.000\n'
        'TOTAL;;;;1.713.550.625\n'),
    "t08": ('Uraian;Volume;Satuan;Harga Satuan;Jumlah\n'
        'Beras premium 5 kg;400;karung;Rp 78.500;Rp 31.400.000\n'
        'Minyak goreng 2 L;400;pouch;menyusul;\n'
        'Gula pasir 1 kg;800;kg;Rp 17.250;Rp 13.800.000\n'
        'Total;;;;Rp 45.200.000\n'),
    "t09": ('Uraian;Volume;Satuan;Harga Satuan;Jumlah\n'
        'Kendaraan dinas SUV;3;unit;Rp 612.345.678,-;Rp 1.837.037.034,-\n'
        'Karpet dasar;3;set;Rp 2.750.000,-;Rp 8.250.000,-\n'
        'Grand Total;;;;Rp 2.067.607.401,-\n'),
    "t10": ('No\tUraian\tVolume\tSatuan\tHarga Satuan\tJumlah Harga\n'
        '1\tJasa kebersihan gedung\t12\tbulan\tRp 18.750.000\tRp 225.000.000\n'
        '2\tBahan pembersih\t12\tbulan\tRp 2.125.500\tRp 25.506.000\n'
        '\n'
        '\tSub Total\t\t\t\tRp 250.506.000\n'
        '\tPPN 11%\t\t\t\tRp 27.555.660\n'
        '\tTotal\t\t\t\tRp 278.061.660\n'
        '\tDibulatkan\t\t\t\tRp 278.061.000\n'
        '\tTerbilang: Dua Ratus Tujuh Puluh Delapan Juta Enam Puluh Satu Ribu Rupiah\t\t\t\t\n'),
    "t11": ('Uraian;Volume;Satuan;Harga Satuan;Jumlah\n'
        'Snack rapat;500;kotak;Rp 18.500;Rp 9.250.000\n'
        'Makan siang;500;kotak;Rp 42.000;Rp 21.000.000\n'
        'Total Harga Sebelum PPN;;;;Rp 30.250.000\n'
        'DPP Nilai Lain (11/12);;;;Rp 27.729.167\n'
        'PPN 12%;;;;Rp 3.327.500\n'
        'Total Harga Setelah PPN;;;;Rp 33.577.500\n'),
    "t12": ('No;Nama Barang;Jumlah;Satuan;Harga Satuan;Jumlah Harga\n'
        '1;Map plastik;500;pcs;Rp 3.750;Rp 1.875.000\n'
        '2;Kertas HVS A4 70g;150;rim;Rp 52.500;Rp 7.785.000\n'
        '3;Tinta printer;24;botol;Rp 125.000;Rp 3.000.000\n'
        ';Total;;;;Rp 12.660.000\n'),
    "t13": ('Uraian;Volume;Satuan;Harga Satuan;Jumlah\n'
        'Pagar BRC;42,5;m;Rp 385.000,-;Rp 16.362.500,-\n'
        'Cat pagar;42,5;m;Rp 18.000,-;Rp 765.000,-\n'
        'Harga Total;;;;Rp 17.127.500,-\n'
        'Jumlah Harga Termasuk PPN;;;;Rp 19.011.525,-\n'),
}
# Kunci jawaban dari kunci.py penguji (Decimal/integer, independen dari script) + t13 dihitung manual:
#   42,5 x 385.000 = 16.362.500 ; 42,5 x 18.000 = 765.000 ; DPP 17.127.500 ; PPN floor(x 11/100) = 1.884.025
# (mode ppn, termasuk_ppn, jumlah per baris, subtotal, dpp, ppn, total, sisa)
KUNCI_PENGUJI = {
    "t01": ("nonmewah", False, [3125000, 12565125, 3030210, 4500000], 23220335, 23220335, 2554236, 25774571, 0),
    "t02": ("nonmewah", False, [49400000, 6550000, 1296250], 57246250, 57246250, 6297087, 63543337, 0),
    "t03": ("nonmewah", False, [57750000, 6825000, 61800000], 126375000, 126375000, 13901250, 140276250, 0),
    "t04": ("nonmewah", False, [46000000, 1650000, 2925000, 640000, 1120000], 52335000, 52335000, 5756850,
            58091850, 0),
    "t05": ("tidak", False, [3333, 9259, 3703706, 570554], 4286852, 4286852, 0, 4286852, 0),
    "t06": ("nonmewah", True, [21570000, 27972500, 22980000], 72522500, 65335586, 7186914, 72522500, 0),
    "t07": ("tidak", False, [45000000, 464062500, 472937500, 263200000], 1245200000, 1245200000, 0, 1245200000, 0),
    "t08": ("tidak", False, [31400000, 13800000], 45200000, 45200000, 0, 45200000, 0),
    "t09": ("mewah", False, [1837037034, 8250000], 1845287034, 1845287034, 221434444, 2066721478, 0),
    "t10": ("nonmewah", False, [225000000, 25506000], 250506000, 250506000, 27555660, 278061660, 0),
    "t11": ("nonmewah", False, [9250000, 21000000], 30250000, 30250000, 3327500, 33577500, 0),
    "t12": ("tidak", False, [1875000, 7875000, 3000000], 12750000, 12750000, 0, 12750000, 0),
    "t13": ("nonmewah", False, [16362500, 765000], 17127500, 17127500, 1884025, 19011525, 0),
}


class UjiV102(Dasar):
    """Tes regresi temuan uji ulang v1.0.1 (1-6) + pengunci angka inti 13 CSV penguji."""

    def jalan(self, k, **kw):
        mode, incl = KUNCI_PENGUJI[k][:2]
        return C.hitung(self.tulis(CSV_PENGUJI[k], k + ".csv"), mode, termasuk_ppn=incl, **kw)

    def test_kunci_angka_13_csv_penguji(self):
        for k, (mode, incl, jml, sub, dpp, ppn, tot, sisa) in KUNCI_PENGUJI.items():
            h = self.jalan(k)
            self.assertEqual([i["jumlah"] for i in h["item"]], jml, k)
            self.assertEqual((h["subtotal"], h["dpp"], h["ppn"], h["total"], h["sisa_pembulatan"]),
                             (sub, dpp, ppn, tot, sisa), k)
        # % HPS & jaminan (kunci.py): t07 HPS 2,4 M -> 51,88% ; 1,2 M -> 103,77% ; t09 2,4 M -> 86,11%, 5% kontrak
        h = self.jalan("t07", hps=2_400_000_000)
        self.assertEqual((h["persen_hps"], h["batas_80_hps"]), (Decimal("51.88"), 1_920_000_000))
        self.assertTrue(any("Rp120.000.000" in x for x in h["peringatan"]))
        h = self.jalan("t07", hps=1_200_000_000)
        self.assertEqual(h["persen_hps"], Decimal("103.77"))
        self.assertTrue(any("MELEBIHI HPS" in x and "Rp45.200.000" in x for x in h["peringatan"]))
        h = self.jalan("t09", hps=2_400_000_000)
        self.assertEqual(h["persen_hps"], Decimal("86.11"))
        self.assertTrue(any("Rp103.336.074" in x for x in h["info"]))

    def test_temuan_penguji_tetap_terdeteksi(self):
        # yang sudah benar di v1.0.1 tidak boleh hilang
        self.assertTrue(any("BELUM TERMASUK PPN" in x and "Rp63.543.337" in x for x in self.jalan("t02")["peringatan"]))
        h = self.jalan("t03")
        self.assertEqual(sum("TIDAK cocok" in x or "selisih" in x for x in h["peringatan"]), 2)
        h = self.jalan("t04")
        self.assertEqual([(s["baris_file"], s["selisih"]) for s in h["selisih_baris"]], [(4, 630000)])
        for k in ("t01", "t05", "t06"):
            self.assertFalse(self.jalan(k)["peringatan"], k)
        h = self.jalan("t10")
        self.assertEqual([x for x in h["peringatan"]], [x for x in h["peringatan"] if "'Dibulatkan'" in x])
        self.assertEqual(len(h["peringatan"]), 1)

    def test_temuan1_label_sebelum_ppn_bukan_alarm(self):
        h = self.jalan("t11")
        self.assertFalse(h["peringatan"])
        self.assertEqual(sum("cocok dengan" in x for x in h["info"]), 4)
        base = "Uraian;Volume;Satuan;Harga Satuan;Jumlah\nA;1;u;1.000.000;1.000.000\n"
        for label in ("Total Harga Sebelum PPN", "Total sebelum pajak", "Subtotal (belum PPN)", "Total DPP",
                      "Jumlah (belum termasuk PPN)", "Total excl. PPN"):
            h = C.hitung(self.tulis(base + f"{label};;;;1.000.000\n", "s.csv"), "nonmewah")
            self.assertFalse(h["peringatan"], label)
            self.assertTrue(any("SEBELUM PPN" in x and "cocok" in x for x in h["info"]), label)
            # label 'sebelum PPN' tetapi berisi total sesudah PPN -> diperingatkan
            h = C.hitung(self.tulis(base + f"{label};;;;1.110.000\n", "s2.csv"), "nonmewah")
            self.assertTrue(any("SESUDAH PPN" in x for x in h["peringatan"]), label)
        # label sesudah PPN tetap dicek sebagai total: berisi DPP -> BELUM TERMASUK PPN
        for label in ("Total Harga Setelah PPN", "Total (termasuk PPN)", "Jumlah Harga Termasuk PPN"):
            h = C.hitung(self.tulis(base + f"{label};;;;1.000.000\n", "s3.csv"), "nonmewah")
            self.assertTrue(any("BELUM TERMASUK PPN" in x for x in h["peringatan"]), label)
        # 'Total sebelum PPN' pada mode termasuk PPN -> dibandingkan dengan DPP hasil hitung
        h = C.hitung(self.tulis("Uraian;Volume;Satuan;Harga Satuan\nA;1;u;11.100.000\n"
                                "Total sebelum PPN;;;10.000.000\n", "s4.csv"), "nonmewah", termasuk_ppn=True)
        self.assertFalse(h["peringatan"])

    def test_temuan2_dpp_nilai_lain(self):
        # 11/12 x 30.250.000 = 27.729.166,67 -> 27.729.167 (bulat) atau 27.729.166 (bawah): keduanya diterima
        for nilai in ("27.729.167", "27.729.166"):
            isi = CSV_PENGUJI["t11"].replace("27.729.167", nilai)
            h = C.hitung(self.tulis(isi, "d.csv"), "nonmewah")
            self.assertFalse(h["peringatan"], nilai)
            self.assertTrue(any("DPP nilai lain" in x and "cocok" in x for x in h["info"]))
        # salah: diisi DPP penuh -> diperingatkan dengan acuan 11/12
        isi = CSV_PENGUJI["t11"].replace("Rp 27.729.167", "Rp 30.250.000")
        h = C.hitung(self.tulis(isi, "d2.csv"), "nonmewah")
        w = [x for x in h["peringatan"] if "Nilai Lain" in x]
        self.assertEqual(len(w), 1)
        self.assertIn("Rp27.729.167", w[0])
        self.assertIn("selisih -Rp2.520.833", w[0])
        # 'PPN 12% (DPP 11/12)' tetap baris PPN
        self.assertEqual(C.jenis_total("PPN 12% (DPP 11/12)"), "ppn")

    def test_temuan3_jumlah_dan_jumlah_harga(self):
        h = self.jalan("t12")
        self.assertEqual([(s["baris_file"], s["item"], s["jumlah_file"], s["jumlah_hitung"], s["selisih"])
                          for s in h["selisih_baris"]], [(3, 2, 7785000, 7875000, 90000)])
        self.assertTrue(any("Jumlah Harga" in x for x in h["catatan"]))
        self.assertIn("file Rp7.785.000 != hitung 150 x Rp52.500 = Rp7.875.000 (selisih Rp90.000)",
                      C.tampil_harga(h))
        # 'Jumlah' tunggal tetap = volume (perilaku v1.0.1)
        h = C.hitung(self.tulis("Uraian;Jumlah;Satuan;Harga Satuan\nPulpen;10;buah;5.000\n", "j.csv"))
        self.assertEqual(h["total"], 50000)

    def test_temuan4_label_total_tak_dikenal_dilaporkan(self):
        h = self.jalan("t13")
        x = [i for i in h["info"] if "'Harga Total'" in i]
        self.assertEqual(len(x), 1)
        self.assertIn("TIDAK diperiksa", x[0])
        self.assertIn("SEBELUM PPN", x[0])
        self.assertFalse(any("'Harga Total'" in d and "judul bagian" in d for d in h["baris_dilewati"]))
        # judul bagian tanpa angka tetap judul bagian
        h = C.hitung(self.tulis("Uraian;Volume;Satuan;Harga Satuan;Jumlah\nA. Persiapan;;;;\nA;1;u;1.000;1.000\n",
                                "jb.csv"))
        self.assertTrue(any("judul bagian" in d for d in h["baris_dilewati"]))

    def test_temuan5_tidak_cocok_saat_belum_final(self):
        h = self.jalan("t08")
        self.assertTrue(h["total_belum_final"])
        self.assertFalse(any("cocok dengan" in x for x in h["info"]))
        self.assertTrue(any("'Total'" in x and "SEMENTARA" in x for x in h["info"]))

    def test_temuan6_kode_keluar(self):
        def kode(k, *extra):
            mode, incl = KUNCI_PENGUJI[k][:2]
            arg = ["harga", self.tulis(CSV_PENGUJI[k], k + ".csv"), "--ppn", mode] + (["--termasuk-ppn"] if incl else [])
            return self.cli(*arg, *extra)[0]
        self.assertEqual(kode("t01"), 0)    # bersih
        self.assertEqual(kode("t11"), 0)    # dulu alarm palsu
        self.assertEqual(kode("t12"), 1)    # baris salah hitung
        self.assertEqual(kode("t02"), 1)    # total belum termasuk PPN
        self.assertEqual(kode("t07", "--hps", "Rp1,2 M"), 1)   # melebihi HPS
        self.assertEqual(kode("t08"), 3)    # belum final didahulukan
        self.assertEqual(self.cli("harga", self.tulis("x;y\n", "b.csv"))[0], 2)   # input buruk
        self.assertEqual(self.cli("harga")[0], 2)                                  # argumen kurang
        self.assertEqual(self.cli("jadwal", "--batas", "2026-10-15", "--hari-ini", "2026-10-20")[0], 1)


    def test_v103_header_volume_sinonim(self):
        # uji ulang v1.0.2: kolom banyaknya bernama lain + "Jumlah Harga" -> volume tidak boleh diambil dari kolom uang
        for judul in ("Banyaknya", "Jml", "Qty.", "Volume Pekerjaan"):
            f = self.tulis("No;Uraian;%s;Satuan;Harga Satuan;Jumlah Harga\n1;Kertas A4;10;rim;Rp50.000;Rp500.000\n"
                           "2;Tinta;4;botol;Rp125.000;Rp500.000\n" % judul, "v%s.csv" % len(judul))
            k, out = self.cli("harga", f)[:2]
            self.assertEqual(k, 0, judul + out)
            self.assertIn("1.000.000", out, judul)

    def test_v103_jumlah_harga_bukan_volume(self):
        f = self.tulis("Uraian;Harga Satuan;Jumlah Harga\nKertas;Rp50.000;Rp500.000\n", "vx.csv")
        self.assertEqual(self.cli("harga", f)[0], 2)

    def test_v103_hps_nol_input_buruk(self):
        f = self.tulis("Uraian;Volume;Satuan;Harga Satuan\nKertas;10;rim;Rp50.000\n", "h0.csv")
        self.assertEqual(self.cli("harga", f, "--hps", "0")[0], 2)
        self.assertEqual(self.cli("harga", f, "--hps", "-5")[0], 2)



class UjiV104NaskahResmi(Dasar):
    """v1.0.4: perilaku sesuai naskah konsolidasi resmi Perpres 16/2018 jo. 12/2021 jo. 46/2025."""
    GEDUNG = "Uraian;Volume;Satuan;Harga Satuan\nPaket;1;ls;10.500.000.000\n"

    def info(self, **kw):
        return " | ".join(C.hitung(self.tulis(self.GEDUNG), hps=11_000_000_000, **kw)["info"])

    def test_a_jaminan_penawaran_hanya_konstruksi_terintegrasi(self):
        # 1% x 11 M = 110.000.000 ; 3% = 330.000.000
        for j in ("konstruksi", "terintegrasi"):
            t = self.info(jenis=j)
            self.assertIn("WAJIB JAMINAN PENAWARAN", t)
            self.assertIn("Rp110.000.000 s.d. Rp330.000.000", t)
            self.assertIn("Pasal 30 ayat (2)", t)
        self.assertIn("pagu", self.info(jenis="terintegrasi"))
        for j in ("barang", "jasa-lainnya", "konsultansi"):
            t = self.info(jenis=j)
            self.assertNotIn("WAJIB JAMINAN PENAWARAN", t)
            self.assertIn("TIDAK diperlukan", t)
        t = self.info()
        self.assertIn("ASUMSI", t)
        self.assertIn("KONSTRUKSI", t)
        # angka inti tidak berubah oleh --jenis
        for j in [None] + C.JENIS:
            h = C.hitung(self.tulis(self.GEDUNG), hps=11_000_000_000, jenis=j)
            self.assertEqual((h["total"], h["persen_hps"], h["batas_80_hps"]),
                             (10_500_000_000, Decimal("95.45"), 8_800_000_000))

    def test_a_cli_jenis(self):
        p = self.tulis(self.GEDUNG)
        kode, out, _ = self.cli("harga", p, "--hps", "11 M", "--jenis", "barang")
        self.assertEqual(kode, 0)
        self.assertNotIn("WAJIB JAMINAN PENAWARAN", out)
        kode, out, _ = self.cli("harga", p, "--hps", "11 M", "--jenis", "konstruksi")
        self.assertEqual(kode, 0)
        self.assertIn("WAJIB JAMINAN PENAWARAN", out)
        self.assertEqual(self.cli("harga", p, "--jenis", "sembako")[0], 2)

    def test_b_jaminan_pelaksanaan_tanpa_pengecualian_epurchasing(self):
        p = self.tulis("Uraian;Volume;Satuan;Harga Satuan\nMebel;1;ls;250.000.000\n")
        for j in (None, "barang", "konstruksi"):
            t = " | ".join(C.hitung(p, hps=300_000_000, jenis=j)["info"])
            self.assertIn("Rp12.500.000", t)
            self.assertNotIn("kecuali e-purchasing", t)
            self.assertIn("berlaku juga untuk e-purchasing", t)
        t = " | ".join(C.hitung(p, hps=300_000_000, jenis="konsultansi")["info"])
        self.assertNotIn("Rp12.500.000", t)
        # < 80% HPS: 5% x HPS 400 jt = 20.000.000 (angka lama tetap)
        pr = " | ".join(C.hitung(p, hps=400_000_000, jenis="barang")["peringatan"])
        self.assertIn("Rp20.000.000", pr)
        self.assertIn("Pasal 33 ayat (3) huruf b", pr)

    def test_c_tkdn_dan_pasal65_di_dokumen(self):
        teks = ""
        for f in ("SKILL.md", "README.md", "references/checklist-dokumen.md",
                  "references/kesalahan-gugur.md", "templates/lembar-kerja-tender.md"):
            with open(os.path.join(AKAR, f), encoding="utf-8") as fh:
                teks += fh.read()
        self.assertNotIn("> 25%", teks)
        self.assertNotIn("kecuali e-purchasing", teks)
        self.assertNotIn("bukan e-purchasing", teks)
        self.assertIn("paling sedikit 25%", teks)
        self.assertIn("Pasal 65 ayat (4)", teks)
        with open(os.path.join(AKAR, "scripts", "cek_penawaran.py"), encoding="utf-8") as fh:
            src = fh.read()
        self.assertNotIn("kecuali e-purchasing", src)
        p = self.tulis("Uraian;Volume;Satuan;Harga Satuan\nA;1;u;1.000.000\n")
        t = " | ".join(C.hitung(p, pagu=5_000_000)["info"])
        self.assertIn("Pasal 65 ayat (3)", t)
        self.assertIn("Pasal 65 ayat (4)", t)



class UjiV105Terintegrasi(Dasar):
    """v1.0.5: pekerjaan terintegrasi + --pagu -> jaminan dihitung dari pagu (Pasal 31 ayat (3), Pasal 33 ayat (4))."""
    GEDUNG = "Uraian;Volume;Satuan;Harga Satuan\nPaket;1;ls;10.500.000.000\n"

    def h(self, **kw):
        return C.hitung(self.tulis(self.GEDUNG), hps=11_000_000_000, **kw)

    def test_penawaran_dari_pagu(self):
        h = self.h(jenis="terintegrasi", pagu=14_000_000_000)
        t = " | ".join(h["info"])
        # 1% x 14 M = 140.000.000 ; 3% = 420.000.000
        self.assertIn("WAJIB JAMINAN PENAWARAN 1%-3% dari pagu anggaran Rp14.000.000.000", t)
        self.assertIn("Rp140.000.000 s.d. Rp420.000.000", t)
        self.assertNotIn("Rp110.000.000 s.d. Rp330.000.000", t)
        self.assertEqual(h["dasar_jaminan_penawaran"], "pagu")

    def test_tanpa_pagu_tetap_gambaran_hps(self):
        h = self.h(jenis="terintegrasi")
        t = " | ".join(h["info"])
        self.assertIn("Rp110.000.000 s.d. Rp330.000.000", t)
        self.assertIn("isi --pagu", t)
        self.assertNotIn("di atas dihitung dari HPS", t)
        self.assertEqual(h["dasar_jaminan_penawaran"], "hps")

    def test_pelaksanaan_di_bawah_80_pagu(self):
        # 10,5 M < 80% x 14 M = 11,2 M -> 5% x pagu 14 M = 700.000.000
        h = self.h(jenis="terintegrasi", pagu=14_000_000_000)
        pr = " | ".join(h["peringatan"])
        self.assertIn("di bawah 80% pagu anggaran (< Rp11.200.000.000)", pr)
        self.assertIn("5% dari nilai total pagu = Rp700.000.000", pr)
        self.assertIn("Pasal 33 ayat (4)", pr)
        self.assertNotIn("Rp525.000.000", pr + " | ".join(h["info"]))

    def test_pelaksanaan_80_100_pagu(self):
        # 10,5 M >= 80% x 12 M = 9,6 M -> 5% x kontrak 10,5 M = 525.000.000
        h = self.h(jenis="terintegrasi", pagu=12_000_000_000)
        t = " | ".join(h["info"])
        self.assertIn("5% dari nilai kontrak = Rp525.000.000", t)
        self.assertIn("80%-100% pagu", t)
        self.assertEqual(sum("jaminan pelaksanaan" in x for x in h["info"]), 1)

    def test_klarifikasi_tetap_terhadap_hps(self):
        # 10,5 M < 80% HPS 14 M: klarifikasi kewajaran tetap vs HPS; jaminan pelaksanaan dari pagu 15 M
        h = C.hitung(self.tulis(self.GEDUNG), hps=14_000_000_000, pagu=15_000_000_000, jenis="terintegrasi")
        pr = " | ".join(h["peringatan"])
        self.assertIn("KLARIFIKASI KEWAJARAN HARGA", pr)
        self.assertNotIn("5% dari nilai HPS", pr)
        self.assertIn("Rp750.000.000", pr)

    def test_angka_inti_dan_jenis_lain_tidak_berubah(self):
        for j in [None] + C.JENIS:
            h = self.h(jenis=j, pagu=14_000_000_000)
            self.assertEqual((h["total"], h["persen_hps"], h["batas_80_hps"]),
                             (10_500_000_000, Decimal("95.45"), 8_800_000_000))
        t = " | ".join(self.h(jenis="konstruksi", pagu=14_000_000_000)["info"])
        self.assertIn("Rp110.000.000 s.d. Rp330.000.000", t)
        self.assertIn("Rp525.000.000", t)

    def test_slug_jasa_lainnya_dan_pagu_nol(self):
        t = " | ".join(self.h(jenis="jasa-lainnya")["info"])
        self.assertIn("pengadaan jasa lainnya", t)
        self.assertNotIn("pengadaan jasa-lainnya", t)
        p = self.tulis(self.GEDUNG)
        self.assertEqual(self.cli("harga", p, "--pagu", "0")[0], 2)
        kode, out, _ = self.cli("harga", p, "--hps", "11 M", "--pagu", "14 M", "--jenis", "terintegrasi")
        self.assertIn("Rp140.000.000 s.d. Rp420.000.000", out)

if __name__ == "__main__":
    unittest.main(verbosity=1)
