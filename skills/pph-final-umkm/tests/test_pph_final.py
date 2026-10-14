"""Tes pph_final.py (v1.0.4: kredit PPh 22 marketplace, PP 20/2026 tanpa batas waktu OP & PT perorangan,
hari ini/besok, subtotal proyeksi, mode data belum lengkap). Jalankan dari folder skill:
python3 -m unittest discover -s tests -v      (atau: python3 tests/test_pph_final.py)"""
import datetime
import io
import json
import os
import random
import sys
import unittest
from contextlib import redirect_stdout
from decimal import Decimal, ROUND_FLOOR

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import pph_final as p  # noqa: E402

WARUNG = ["48jt", "45jt", "52jt", "70jt", "55jt", "50jt", "53jt", "58jt", "61jt", "60jt"]
OLSHOP = ["52jt", "48,5jt", "95jt", "61jt", "58jt", "64jt", "70jt", "73jt", "66jt"]


def jalankan(*argv):
    buf = io.StringIO()
    with redirect_stdout(buf):
        kode = p.main(list(argv) + ["--format", "json"])
    return kode, json.loads(buf.getvalue()) if kode == 0 else None


def teks(*argv):
    buf = io.StringIO()
    with redirect_stdout(buf):
        kode = p.main(list(argv))
    return kode, buf.getvalue()


class TesHitunganDasar(unittest.TestCase):
    def test_hitungan_lama_tetap(self):
        kode, h = jalankan("--jenis", "op", "--tahun", "2026", "--hari-ini", "2026-09-23", "--omzet",
                           "45jt", "60jt", "80jt", "120jt", "150jt", "90jt", "70jt")
        self.assertEqual(kode, 0)
        self.assertEqual([b["pph_final"] for b in h["bulan"]][-2:], [225000, 350000])
        self.assertEqual(h["ringkasan"]["total_pph_final"], 575000)
        self.assertEqual(h["versi"], "1.0.4")

    def test_skenario_warung_batas_libur(self):
        kode, h = jalankan("--jenis", "op", "--tahun", "2026", "--tahun-terdaftar", "2021",
                           "--hari-ini", "2026-10-01", "--omzet", *WARUNG)
        self.assertEqual(kode, 0)
        okt = h["bulan"][9]
        self.assertEqual(okt["pph_final"], 260000)
        self.assertEqual(okt["setor_paling_lambat"], "2026-11-15")
        self.assertEqual(okt["setor_hari_kerja"], "2026-11-16")
        semua = " ".join(h["catatan"])
        self.assertIn("Senin 16 November 2026", semua)
        self.assertIn("PMK 81/2024 Pasal 100", semua)
        self.assertIn("tidak ada lagi batas tahun", semua)
        self.assertNotIn("TERAKHIR", semua)
        self.assertFalse(any(b["batas_setor_sudah_lewat"] for b in h["bulan"]))

    def test_geser_libur_nasional_dan_cuti(self):
        self.assertEqual(p.geser_hari_kerja(datetime.date(2026, 2, 15))[0], datetime.date(2026, 2, 18))
        self.assertEqual(p.geser_hari_kerja(datetime.date(2026, 8, 15))[0], datetime.date(2026, 8, 18))
        self.assertEqual(p.geser_hari_kerja(datetime.date(2026, 10, 15))[0], datetime.date(2026, 10, 15))
        t, _, lengkap = p.geser_hari_kerja(datetime.date(2028, 1, 15))
        self.assertEqual(t, datetime.date(2028, 1, 17))
        self.assertFalse(lengkap)

    def test_input_rusak(self):
        self.assertEqual(jalankan("--tahun", "2026", "--tahun-terdaftar", "2030", "--omzet", "10jt")[0], 2)
        self.assertEqual(jalankan("--omzet", "abc")[0], 2)
        self.assertEqual(jalankan("--omzet", "10jt", "--pph22", "1rb", "2rb")[0], 2)
        self.assertEqual(jalankan("--omzet", "10jt", "--proyeksi-mulai", "5")[0], 2)
        self.assertEqual(jalankan("--kemungkinan", "--omzet", "10jt", "20jt")[0], 2)


class TesKreditPPh22(unittest.TestCase):
    """FAQ DJP PMK 37/2025 no. 14-15: PPh 22 marketplace = bagian pelunasan PPh final masa yang sama."""

    def setUp(self):
        kode, self.h = jalankan("--jenis", "op", "--tahun", "2026", "--hari-ini", "2026-10-14",
                                "--omzet", *OLSHOP, "--pph22", *(["0"] * 7 + ["180rb", "165rb"]))
        self.assertEqual(kode, 0)
        self.agu, self.sep = self.h["bulan"][7], self.h["bulan"][8]

    def test_lebih_bayar(self):
        self.assertEqual(self.agu["pph_final"], 107500)
        self.assertEqual(self.agu["setor_sendiri"], 0)
        self.assertEqual(self.agu["lebih_dipungut"], 72500)
        # sudah lunas lewat PPh 22 -> tidak ditandai telat walau 15 Sep sudah lewat
        self.assertFalse(self.agu["batas_setor_sudah_lewat"])
        self.assertEqual(self.agu["status_batas"], "")

    def test_kurang_bayar(self):
        self.assertEqual(self.sep["pph_final"], 330000)
        self.assertEqual(self.sep["setor_sendiri"], 165000)
        self.assertEqual(self.sep["lebih_dipungut"], 0)
        self.assertEqual(self.sep["status_batas"], "besok")
        r = self.h["ringkasan"]
        self.assertEqual(r["total_pph_final"], 437500)
        self.assertEqual(r["total_setor_sendiri_data_nyata"], 165000)
        self.assertEqual(r["total_lebih_dipungut"], 72500)
        self.assertEqual(r["batas_setor_terdekat"]["tanggal_teks"], "Kamis 15 Oktober 2026")
        self.assertEqual(r["batas_setor_terdekat"]["jarak"], "besok")
        self.assertEqual(r["bulan_batas_setor_sudah_lewat"], [])

    def test_teks_tabel_dan_catatan(self):
        _, out = teks("--jenis", "op", "--tahun", "2026", "--hari-ini", "2026-10-14", "--marketplace",
                      "--omzet", *OLSHOP, "--pph22", *(["0"] * 7 + ["180rb", "165rb"]))
        self.assertIn("Hari ini (tanggal acuan hitungan): Rabu 14 Oktober 2026", out)
        self.assertIn("| lebih Rp72.500 |", out)
        self.assertIn("kurang Rp165.000 (setor sendiri)", out)
        self.assertIn("Kamis 15 Okt 2026 - BESOK", out)
        self.assertIn("FAQ DJP PMK 37/2025", out)
        self.assertIn("paling lambat Senin 31 Agustus 2026", out)
        self.assertNotIn("BELUM dikurangi", out)
        self.assertNotIn("Rp 1", out)  # format standar tanpa spasi

    def test_tanpa_pph22(self):
        kode, h = jalankan("--jenis", "badan", "--jenis-badan", "pt-perorangan", "--tahun", "2026",
                           "--hari-ini", "2026-10-14", "--omzet", "35jt", "42jt", "38jt", "50jt", "47jt", "44jt",
                           "51jt", "49jt", "53jt")
        self.assertEqual(kode, 0)
        self.assertFalse(h["mode_pph22"])
        for b in h["bulan"]:
            self.assertEqual(b["setor_sendiri"], b["pph_final"])
            self.assertEqual(b["lebih_dipungut"], 0)
        self.assertEqual(h["ringkasan"]["total_pph_final"], 2045000)
        self.assertEqual(len(h["ringkasan"]["bulan_batas_setor_sudah_lewat"]), 8)
        self.assertEqual(h["bulan"][8]["status_batas"], "besok")
        _, out = teks("--jenis", "badan", "--tahun", "2026", "--hari-ini", "2026-10-14", "--omzet", "35jt")
        self.assertNotIn("PPh 22 dipungut", out)

    def test_bebas_tapi_dipungut(self):
        kode, h = jalankan("--jenis", "op", "--tahun", "2026", "--hari-ini", "2026-10-14", "--bulan-awal", "8",
                           "--omzet", "40jt", "--pph22", "200rb")
        self.assertEqual(h["bulan"][0]["pph_final"], 0)
        self.assertEqual(h["bulan"][0]["lebih_dipungut"], 200000)
        self.assertIn("surat pernyataan bermeterai omzet s.d. Rp500 juta", " ".join(h["catatan"]))

    def test_pembulatan_selisih_ke_bawah(self):
        self.assertEqual(p.kredit_pph22(Decimal(107500), Decimal("100000.50")), (Decimal(7499), Decimal(0)))
        self.assertEqual(p.kredit_pph22(Decimal(107500), Decimal("107500.75")), (Decimal(0), Decimal(0)))
        self.assertEqual(p.kredit_pph22(Decimal(0), Decimal(0)), (Decimal(0), Decimal(0)))

    def test_cocok_hitungan_independen_acak(self):
        rnd = random.Random(20261014)
        for _ in range(300):
            jenis = rnd.choice(["op", "badan"])
            awal = rnd.randint(1, 12)
            n = rnd.randint(1, 13 - awal)
            sebelum = rnd.choice([0, rnd.randint(0, 700) * 1000000])
            omzet = [rnd.randint(0, 250000000) for _ in range(n)]
            pph22 = [rnd.choice([0, rnd.randint(0, 900000)]) for _ in range(n)]
            argv = ["--jenis", jenis, "--tahun", "2026", "--hari-ini", "2026-10-14", "--bulan-awal", str(awal),
                    "--omzet-sebelumnya", str(sebelum), "--omzet"] + [str(o) for o in omzet] + \
                   ["--pph22"] + [str(x) for x in pph22]
            kode, h = jalankan(*argv)
            self.assertEqual(kode, 0)
            kum = sebelum
            for i, b in enumerate(h["bulan"]):
                lama, kum = kum, kum + omzet[i]
                kena = max(0, kum - max(lama, 500000000)) if jenis == "op" else omzet[i]
                pph = kena * 5 // 1000
                self.assertEqual(b["pph_final"], pph)
                self.assertEqual(b["setor_sendiri"], max(0, pph - pph22[i]))
                self.assertEqual(b["lebih_dipungut"], max(0, pph22[i] - pph))


class TesHariIniDanProyeksi(unittest.TestCase):
    def test_subtotal_proyeksi(self):
        kode, h = jalankan("--tahun", "2026", "--hari-ini", "2026-10-14", "--bulan-awal", "7",
                           "--omzet-sebelumnya", "410jt", "--omzet", "95jt", "88jt", "102jt", "100jt", "100jt", "100jt",
                           "--proyeksi-mulai", "10")
        self.assertEqual(kode, 0)
        r = h["ringkasan"]
        self.assertEqual(r["total_pph_final_data_nyata"], 975000)
        self.assertEqual(r["total_pph_final"], 2475000)
        self.assertEqual(r["rentang_data_nyata"], "Juli–September")
        self.assertEqual(r["bulan_batas_setor_sudah_lewat"], ["Juli", "Agustus"])
        self.assertTrue(h["bulan"][3]["proyeksi"])
        self.assertEqual(h["bulan"][3]["status_batas"], "")
        self.assertEqual(h["bulan"][3]["setor_hari_kerja"], "2026-11-16")
        _, out = teks("--tahun", "2026", "--hari-ini", "2026-10-14", "--bulan-awal", "7",
                      "--omzet-sebelumnya", "410jt", "--omzet", "95jt", "88jt", "102jt", "100jt", "100jt", "100jt",
                      "--proyeksi-mulai", "10")
        self.assertIn("**Subtotal data nyata (Juli–September)**", out)
        self.assertIn("**Rp975.000**", out)
        self.assertIn("Oktober (proyeksi)", out)

    def test_status_relatif(self):
        hi = datetime.date(2026, 10, 14)
        self.assertEqual(p.status_relatif(datetime.date(2026, 10, 15), hi), "besok")
        self.assertEqual(p.status_relatif(datetime.date(2026, 10, 14), hi), "hari ini")
        self.assertEqual(p.status_relatif(datetime.date(2026, 9, 15), hi), "sudah lewat")
        self.assertEqual(p.keterangan_jarak(datetime.date(2026, 11, 16), hi), "33 hari lagi")
        self.assertEqual(p.format_tgl(hi), "Rabu 14 Oktober 2026")


class TesJangkaWaktuPP20(unittest.TestCase):
    def test_op_dan_pt_perorangan_tanpa_batas(self):
        for jb, terdaftar in ((None, 2020), (None, 2015), ("pt-perorangan", 2024)):
            jenis = "op" if jb is None else "badan"
            for tahun in (2026, 2027, 2030):
                t = p.catatan_jangka_waktu(jenis, jb, tahun, terdaftar)
                self.assertIn("tidak ada lagi batas tahun", t)
                self.assertIn("Pasal 59", t)
                self.assertNotIn("TERAKHIR", t)
                self.assertNotIn("MELEWATI", t)
        self.assertIn("Pasal II angka 1 huruf a", p.catatan_jangka_waktu("op", None, 2026, 2018))
        self.assertIn("pastikan ke DJP", p.catatan_jangka_waktu("badan", "pt-perorangan", 2026, 2021))

    def test_koperasi(self):
        self.assertIn("s.d. tahun pajak 2029", p.catatan_jangka_waktu("badan", "koperasi", 2026, 2021))
        self.assertIn("s.d. tahun pajak 2029", p.catatan_jangka_waktu("badan", "koperasi", 2026, 2023))
        self.assertIn("MELEWATI", p.catatan_jangka_waktu("badan", "koperasi", 2026, 2020))
        self.assertIn("s.d. tahun pajak 2030", p.catatan_jangka_waktu("badan", "koperasi", 2028, 2027))

    def test_cv_firma_pt(self):
        self.assertIn("TERAKHIR", p.catatan_jangka_waktu("badan", "cv", 2026, 2023))
        self.assertIn("MELEWATI", p.catatan_jangka_waktu("badan", "cv", 2027, 2023))
        self.assertIn("s.d. tahun pajak 2026", p.catatan_jangka_waktu("badan", "pt", 2026, 2024))
        self.assertIn("tidak bisa memakai 0,5%", p.catatan_jangka_waktu("badan", "firma", 2027, 2027))
        self.assertNotIn("--tahun-terdaftar", p.catatan_jangka_waktu("badan", "cv", 2026, None))


class TesKemungkinan(unittest.TestCase):
    def test_satu_bulan_data_kurang(self):
        kode, h = jalankan("--kemungkinan", "--tahun", "2026", "--hari-ini", "2026-10-14", "--bulan-awal", "10",
                           "--omzet", "85jt")
        self.assertEqual(kode, 0)
        nilai = [(k["pph_min"], k["pph_max"]) for k in h["kemungkinan"]]
        self.assertEqual(nilai, [(0, 0), (0, 425000), (425000, 425000), (425000, 425000)])
        self.assertIn("Rp415.000.000", h["kemungkinan"][0]["kondisi"])
        self.assertEqual(h["setor_hari_kerja_teks"], "Senin 16 November 2026")
        self.assertEqual(h["jarak_batas_setor"], "33 hari lagi")

    def test_kemungkinan_dengan_pph22(self):
        kode, h = jalankan("--kemungkinan", "--tahun", "2026", "--hari-ini", "2026-10-14", "--bulan-awal", "2",
                           "--omzet", "50jt", "--pph22", "100rb")
        self.assertEqual(h["kemungkinan"][0]["lebih_dipungut"], 100000)
        self.assertEqual(h["kemungkinan"][-1]["setor_sendiri"], 150000)


if __name__ == "__main__":
    unittest.main()
