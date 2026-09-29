#!/usr/bin/env python3
"""Uji regresi klinis.py (unittest, library standar saja).

Jalankan dari folder skill:  python3 tests/uji_regresi.py      (Windows: python / py)
Setiap angka harapan di bawah dihitung manual (lihat komentar) - bukan disalin dari output script.
Semua data FIKTIF.
"""
import io
import json
import os
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from datetime import date

DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(DIR, "..", "scripts"))
import klinis as k  # noqa: E402


def jalankan(*argv):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        kode = k.main(list(argv))
    return kode, out.getvalue(), err.getvalue()


class TesMAP(unittest.TestCase):
    def test_nilai_umum(self):
        # (120 + 2*80)/3 = 280/3 = 93,33 -> 93,3
        h = k.hitung_map(120, 80)
        self.assertEqual(h["map_mmhg"], "93.3")
        self.assertTrue(h["map_lebih_dari_90"])

    def test_tepat_90_bukan_lebih_dari_90(self):
        # (110 + 160)/3 = 90 tepat -> TIDAK > 90
        h = k.hitung_map(110, 80)
        self.assertEqual(h["map_mmhg"], "90.0")
        self.assertFalse(h["map_lebih_dari_90"])

    def test_sedikit_di_atas_90(self):
        # (111 + 160)/3 = 90,333... -> > 90, tampil 90,3
        h = k.hitung_map(111, 80)
        self.assertEqual(h["map_mmhg"], "90.3")
        self.assertTrue(h["map_lebih_dari_90"])

    def test_pembulatan_setengah_ke_atas(self):
        # (100 + 2*70.25)/3 = 240,5/3 = 80,1666 -> 80,2 ; (101+2*70)/3 = 80,333 -> 80,3
        self.assertEqual(k.hitung_map("100", "70,25")["map_mmhg"], "80.2")

    def test_input_salah(self):
        for s, d in ((80, 120), (120, 120), (400, 80), (120, 10), ("abc", 80), ("", 80)):
            with self.assertRaises(k.InputSalah, msg=(s, d)):
                k.hitung_map(s, d)


class TesPreeklampsia(unittest.TestCase):
    def test_satu_faktor_tinggi(self):
        h = k.skrining_preeklampsia(["hipertensi-kronik"])
        self.assertEqual(h["kategori"], "RISIKO TINGGI")

    def test_dua_sedang(self):
        h = k.skrining_preeklampsia(["nullipara", "riwayat-keluarga"])
        self.assertTrue(h["kategori"].startswith("RISIKO SEDANG"))

    def test_satu_sedang_saja(self):
        h = k.skrining_preeklampsia(["nullipara"])
        self.assertEqual(h["kategori"], "1 FAKTOR RISIKO SEDANG")

    def test_kosong(self):
        h = k.skrining_preeklampsia([""])
        self.assertTrue(h["kategori"].startswith("TIDAK DITEMUKAN"))

    def test_map_dari_angka_menambah_faktor(self):
        # nullipara + MAP 93,3 -> 2 faktor sedang
        h = k.skrining_preeklampsia(["nullipara"], 120, 80)
        self.assertIn("map-90", h["faktor_dari_angka"])
        self.assertTrue(h["kategori"].startswith("RISIKO SEDANG"))

    def test_map_tepat_90_tidak_menambah(self):
        h = k.skrining_preeklampsia(["nullipara"], 110, 80)
        self.assertEqual(h["kategori"], "1 FAKTOR RISIKO SEDANG")

    def test_usia_40_tidak_dihitung_ganda_di_kia(self):
        # usia 41 -> usia-ibu-35 (KIA) ; usia-ibu-40 tidak boleh jadi faktor sedang kedua
        h = k.skrining_preeklampsia([], usia_ibu=41)
        self.assertEqual(h["kategori"], "1 FAKTOR RISIKO SEDANG")

    def test_imt_batas(self):
        # KIA: IMT > 30. 30,0 tidak ; 30,1 ya
        self.assertTrue(k.skrining_preeklampsia([], imt="30.0")["kategori"].startswith("TIDAK"))
        self.assertEqual(k.skrining_preeklampsia([], imt="30,1")["kategori"],
                         "1 FAKTOR RISIKO SEDANG")

    def test_nice_kembar_sedang_usia_35_tidak_dihitung(self):
        # NICE: kembar = sedang, usia 36 tidak termasuk (batas NICE 40)
        h = k.skrining_preeklampsia(["kehamilan-multipel"], usia_ibu=36, pedoman="nice")
        self.assertEqual(h["kategori"], "1 FAKTOR RISIKO SEDANG")
        # Buku KIA: kembar = tinggi
        h2 = k.skrining_preeklampsia(["kehamilan-multipel"], usia_ibu=36, pedoman="kia")
        self.assertEqual(h2["kategori"], "RISIKO TINGGI")

    def test_kode_tidak_dikenal(self):
        with self.assertRaises(k.InputSalah):
            k.skrining_preeklampsia(["darah-tinggi-banget"])

    def test_map_setengah(self):
        with self.assertRaises(k.InputSalah):
            k.skrining_preeklampsia(["nullipara"], 120, None)

    def test_wajib_sumber_dan_penafian(self):
        h = k.skrining_preeklampsia(["nullipara"])
        self.assertIn("2023", h["sumber"][0])
        self.assertIn("bukan pengganti penilaian klinis", h["penafian"])
        self.assertTrue(any("dosis" in c for c in h["catatan"]))


class TesKehamilan(unittest.TestCase):
    def test_umum(self):
        # HPHT 10 Mar 2026: Naegele 17 Mar -> 17 Des 2026.
        # +280: sisa Maret 21 + Apr-Nov 244 = 265 -> 15 Des 2026.
        # Usia 29 Sep: 21 + 30+31+30+31+31 + 29 = 203 hari = 29 mgg 0 hr.
        h = k.kalkulator_kehamilan("2026-03-10", tanggal_periksa="2026-09-29")
        self.assertIn("2026-12-17", h["hpl_naegele"])
        self.assertIn("2026-12-15", h["hpl_280_hari"])
        self.assertEqual(h["usia_kehamilan"], "29 minggu 0 hari")
        self.assertEqual(h["trimester"], "Trimester 3")

    def test_kabisat(self):
        # 22 Feb 2028 +7 = 29 Feb 2028 (kabisat) -> +9 bln = 29 Nov 2028.
        # +280: sisa Feb 7 + Mar-Okt 245 = 252 -> 28 Nov 2028. Usia 1 Mar = 8 hari.
        h = k.kalkulator_kehamilan("2028-02-22", tanggal_periksa="2028-03-01")
        self.assertIn("2028-11-29", h["hpl_naegele"])
        self.assertIn("2028-11-28", h["hpl_280_hari"])
        self.assertEqual(h["usia_kehamilan"], "1 minggu 1 hari")

    def test_bukan_kabisat(self):
        # 22 Feb 2027 +7 = 1 Mar 2027 -> 1 Des 2027. +280: 6 + 245 = 251 -> 29 Nov 2027.
        h = k.kalkulator_kehamilan("22-02-2027", tanggal_periksa="2027-03-01")
        self.assertIn("2027-12-01", h["hpl_naegele"])
        self.assertIn("2027-11-29", h["hpl_280_hari"])

    def test_tanggal_tidak_ada_di_kalender(self):
        # 24 Mei 2027 +7 = 31 Mei -> +9 bln = "31 Feb 2028" -> 29 Feb 2028 (kabisat), ada catatan.
        # +280: sisa Mei 7 + Jun-Jan 245 = 252 -> 28 Feb 2028.
        h = k.kalkulator_kehamilan("2027-05-24", tanggal_periksa="2027-06-01")
        self.assertIn("2028-02-29", h["hpl_naegele"])
        self.assertIn("2028-02-28", h["hpl_280_hari"])
        self.assertTrue(any("akhir bulan" in c for c in h["catatan"]))

    def test_siklus_35(self):
        # HPHT 1 Jan 2027, siklus 35 -> geser +7. 280 hari -> 8 Okt; +7 = 15 Okt 2027.
        # Usia 1 Mar 2027: 59 hari - 7 = 52 = 7 mgg 3 hr.
        h = k.kalkulator_kehamilan("2027-01-01", siklus=35, tanggal_periksa="2027-03-01")
        self.assertIn("2027-10-15", h["hpl_280_hari"])
        self.assertIn("2027-10-15", h["hpl_naegele"])
        self.assertEqual(h["usia_kehamilan"], "7 minggu 3 hari")

    def test_siklus_24(self):
        # geser -4: 280 hari dari 1 Jan 2027 = 8 Okt; -4 = 4 Okt 2027
        h = k.kalkulator_kehamilan("2027-01-01", siklus=24, tanggal_periksa="2027-03-01")
        self.assertIn("2027-10-04", h["hpl_280_hari"])
        self.assertEqual(h["usia_kehamilan"], "9 minggu 0 hari")  # 59 + 4 = 63

    def test_redating_trimester1(self):
        # HPHT 1 Jan 2027; USG 20 Feb 2027 = hari ke-50 (7w1d) menurut HPHT.
        # USG 8w0d (56) -> selisih 6 > 5 -> pakai USG.
        h = k.kalkulator_kehamilan("2027-01-01", tanggal_periksa="2027-03-01",
                                   usg_tanggal="2027-02-20", usg_minggu=8, usg_hari=0)
        self.assertEqual(h["selisih_hpht_vs_usg_hari"], 6)
        self.assertEqual(h["ambang_acog_hari"], 5)
        self.assertEqual(h["penanggalan_dipakai"], "USG")
        # usia 1 Mar dari USG: 56 + 9 = 65 = 9w2d. HPL USG = 20 Feb + 224 = 2 Okt 2027
        self.assertEqual(h["usia_kehamilan"], "9 minggu 2 hari")
        self.assertIn("2027-10-02", h["hpl_usg"])

    def test_redating_batas_7_hari(self):
        # USG 12 Mar 2027 = hari ke-70 (10w0d) menurut HPHT 1 Jan 2027.
        # USG 11w0d -> selisih 7, tidak > 7 -> HPHT; USG 11w1d -> 8 -> USG.
        h = k.kalkulator_kehamilan("2027-01-01", tanggal_periksa="2027-03-12",
                                   usg_tanggal="2027-03-12", usg_minggu=11, usg_hari=0)
        self.assertEqual(h["penanggalan_dipakai"], "HPHT")
        h = k.kalkulator_kehamilan("2027-01-01", tanggal_periksa="2027-03-12",
                                   usg_tanggal="2027-03-12", usg_minggu=11, usg_hari=1)
        self.assertEqual(h["penanggalan_dipakai"], "USG")

    def test_hanya_usg(self):
        h = k.kalkulator_kehamilan(None, tanggal_periksa="2027-03-12",
                                   usg_tanggal="2027-03-12", usg_minggu=12, usg_hari=0)
        self.assertEqual(h["penanggalan_dipakai"], "USG")
        self.assertEqual(h["trimester"], "Trimester 1")

    def test_batas_trimester(self):
        self.assertEqual(k.trimester(13 * 7 + 6), "Trimester 1")
        self.assertEqual(k.trimester(14 * 7), "Trimester 2")
        self.assertEqual(k.trimester(27 * 7 + 6), "Trimester 2")
        self.assertEqual(k.trimester(28 * 7), "Trimester 3")

    def test_input_salah(self):
        salah = [
            dict(hpht="2026-10-10", tanggal_periksa="2026-09-29"),   # HPHT di masa depan
            dict(hpht="2025-01-01", tanggal_periksa="2026-09-29"),   # > 44 minggu
            dict(hpht="2026-02-30", tanggal_periksa="2026-09-29"),   # tanggal tidak ada
            dict(hpht="2026-03-10", siklus=60, tanggal_periksa="2026-09-29"),
            dict(hpht="2026-03-10", siklus="abc", tanggal_periksa="2026-09-29"),
            dict(tanggal_periksa="2026-09-29"),                       # tanpa HPHT/USG
            dict(tanggal_periksa="2026-09-29", usg_tanggal="2026-09-01"),  # USG setengah
            dict(tanggal_periksa="2026-09-29", usg_tanggal="2026-09-01", usg_minggu=8,
                 usg_hari=9),
        ]
        for kw in salah:
            with self.assertRaises(k.InputSalah, msg=kw):
                k.kalkulator_kehamilan(**kw)


class TesIMT(unittest.TestCase):
    def test_umum(self):
        # 72 / 1,65^2 = 72 / 2,7225 = 26,446 -> 26,4
        h = k.imt_dewasa(165, 72)
        self.assertEqual(h["imt"], "26.4")
        self.assertTrue(h["kategori_asia_pasifik"].startswith("Obesitas I"))
        self.assertTrue(h["kategori_kemenkes"].startswith("Gemuk - kelebihan BB tingkat ringan"))

    def test_satuan_meter_dan_koma(self):
        self.assertEqual(k.imt_dewasa("1,65", "72")["imt"], "26.4")

    def test_batas_asia_pasifik_23(self):
        # 58,9 / 2,56 = 23,0078 -> 23,0 -> berisiko (AP), normal (Kemenkes)
        h = k.imt_dewasa(160, "58.9")
        self.assertEqual(h["imt"], "23.0")
        self.assertTrue(h["kategori_asia_pasifik"].startswith("Berat badan lebih"))
        self.assertTrue(h["kategori_kemenkes"].startswith("Normal"))

    def test_pembulatan_ke_18_5(self):
        # 53,4 / 2,89 = 18,477 -> 18,5 -> normal
        self.assertEqual(k.imt_dewasa(170, "53.4")["imt"], "18.5")

    def test_kemenkes_batas_17_dan_27(self):
        self.assertTrue(k.kategori_kemenkes(k.Decimal("16.9")).startswith("Kurus - kekurangan BB tingkat berat"))
        self.assertTrue(k.kategori_kemenkes(k.Decimal("17.0")).startswith("Kurus - kekurangan BB tingkat ringan"))
        self.assertTrue(k.kategori_kemenkes(k.Decimal("25.0")).startswith("Normal"))
        self.assertTrue(k.kategori_kemenkes(k.Decimal("25.1")).startswith("Gemuk - kelebihan BB tingkat ringan"))
        self.assertTrue(k.kategori_kemenkes(k.Decimal("27.1")).startswith("Gemuk - kelebihan BB tingkat berat"))

    def test_lingkar_perut(self):
        self.assertIn("obesitas sentral", k.imt_dewasa(165, 72, 90, "L")["lingkar_perut"])
        self.assertIn("di bawah", k.imt_dewasa(165, 72, "89.9", "L")["lingkar_perut"])
        self.assertIn("obesitas sentral", k.imt_dewasa(155, 55, 80, "p")["lingkar_perut"])
        h = k.imt_dewasa(165, 72, 90, "L")
        self.assertTrue(any("Tepat 90" in c for c in h["catatan"]))
        with self.assertRaises(k.InputSalah):
            k.imt_dewasa(165, 72, 90, None)

    def test_nilai_ekstrem(self):
        for t, b in ((30, 60), (300, 60), (165, 10), (165, 500), ("seratus", 60)):
            with self.assertRaises(k.InputSalah, msg=(t, b)):
                k.imt_dewasa(t, b)
        # batas yang masih diterima
        self.assertEqual(k.imt_dewasa(250, 350)["imt"], "56.0")  # 350/6,25 = 56


class TesBBHamil(unittest.TestCase):
    def test_overweight(self):
        # 62 / 1,55^2 = 62 / 2,4025 = 25,806 -> 25,8 -> overweight: 7-11,5 kg; 0,23-0,33/mgg
        # 24 mgg: 0,5 + 0,23*11 = 3,03 -> 3,0 ; 2 + 0,33*11 = 5,63 -> 5,6 ; naik 6 -> di atas
        h = k.bb_hamil(155, 62, 68, 24)
        self.assertEqual(h["imt_prahamil"], "25.8")
        self.assertEqual(h["rekomendasi_total_kg"], "7-11,5 kg")
        self.assertEqual(h["perkiraan_rentang_saat_ini_kg"], "3.0-5.6")
        self.assertIn("di atas", h["posisi"])

    def test_batas_kategori(self):
        # 18,5 persis -> normal ; 24,9 normal ; 25,0 overweight ; 30,0 obesitas
        # 1,6 m: 47,36/2,56 = 18,5 ; 63,74/2,56 = 24,898 -> 24,9 ; 64/2,56 = 25 ; 76,8/2,56 = 30
        self.assertEqual(k.bb_hamil(160, "47.36")["rekomendasi_total_kg"], "11,5-16 kg")
        self.assertEqual(k.bb_hamil(160, "63.74")["rekomendasi_total_kg"], "11,5-16 kg")
        self.assertEqual(k.bb_hamil(160, "64")["rekomendasi_total_kg"], "7-11,5 kg")
        self.assertEqual(k.bb_hamil(160, "76.8")["rekomendasi_total_kg"], "5-9 kg")
        self.assertEqual(k.bb_hamil(160, "45")["rekomendasi_total_kg"], "12,5-18 kg")

    def test_kembar(self):
        self.assertIn("17-25", k.bb_hamil(160, 55, kembar=True)["rekomendasi_total_kg"])
        self.assertIn("Tidak ada", k.bb_hamil(160, 45, kembar=True)["rekomendasi_total_kg"])

    def test_trimester_1_tanpa_rentang(self):
        h = k.bb_hamil(160, 55, 56, 10)
        self.assertNotIn("perkiraan_rentang_saat_ini_kg", h)
        self.assertEqual(h["kenaikan_sejauh_ini_kg"], "1.0")

    def test_bb_turun_dan_ekstrem(self):
        self.assertEqual(k.bb_hamil(160, 60, "58.5", 20)["kenaikan_sejauh_ini_kg"], "-1.5")
        with self.assertRaises(k.InputSalah):
            k.bb_hamil(160, 60, 60, 50)


class TesKognitif(unittest.TestCase):
    def test_moca_koreksi(self):
        h = k.kognitif("moca", 25, 12)
        self.assertEqual(h["skor_akhir"], 26)
        self.assertIn("normal", h["interpretasi"])
        h = k.kognitif("MoCA-Ina", 25, 13)
        self.assertEqual(h["skor_akhir"], 25)
        self.assertIn("di bawah batas", h["interpretasi"])

    def test_moca_maks_30(self):
        self.assertEqual(k.kognitif("moca", 30, 6)["skor_akhir"], 30)

    def test_moca_wajib_pendidikan(self):
        with self.assertRaises(k.InputSalah):
            k.kognitif("moca", 25, None)

    def test_mmse(self):
        self.assertTrue(k.kognitif("mmse", 24)["interpretasi"].startswith("24-30"))
        self.assertTrue(k.kognitif("mmse", 23)["interpretasi"].startswith("18-23"))
        self.assertTrue(k.kognitif("mmse", 17)["interpretasi"].startswith("0-17"))

    def test_amt(self):
        self.assertTrue(k.kognitif("amt", 8)["interpretasi"].startswith("8-10"))
        self.assertTrue(k.kognitif("amt", 7)["interpretasi"].startswith("4-7"))
        self.assertTrue(k.kognitif("amt", 3)["interpretasi"].startswith("0-3"))

    def test_skor_di_luar_rentang(self):
        for ins, s in (("mmse", 31), ("mmse", -1), ("moca", 31), ("amt", 11), ("mmse", "dua"),
                       ("gds", 5)):
            with self.assertRaises(k.InputSalah, msg=(ins, s)):
                k.kognitif(ins, s, 10)

    def test_tidak_ada_kata_diagnosis_pasti(self):
        for ins, s in (("mmse", 10), ("moca", 10), ("amt", 1)):
            teks = json.dumps(k.kognitif(ins, s, 6), ensure_ascii=False).lower()
            self.assertNotIn("menderita", teks)
            self.assertNotIn("didiagnosis", teks)
            self.assertIn("bukan diagnosis", teks)


class TesCLI(unittest.TestCase):
    def test_teks_memuat_sumber_dan_penafian(self):
        for argv in (["map", "--sistolik", "120", "--diastolik", "80"],
                     ["preeklampsia", "--faktor", "nullipara"],
                     ["kehamilan", "--hpht", "2026-03-10", "--tanggal-periksa", "2026-09-29"],
                     ["bb-hamil", "--tinggi", "155", "--bb-prahamil", "62"],
                     ["imt", "--tinggi", "165", "--berat", "72"],
                     ["kognitif", "--instrumen", "amt", "--skor", "9"],
                     ["faktor-preeklampsia"]):
            kode, out, _ = jalankan(*argv)
            self.assertEqual(kode, 0, argv)
            self.assertIn("Sumber:", out, argv)
            self.assertIn("bukan pengganti penilaian klinis", out, argv)

    def test_json(self):
        kode, out, _ = jalankan("--json", "imt", "--tinggi", "165", "--berat", "72")
        self.assertEqual(kode, 0)
        self.assertEqual(json.loads(out)["imt"], "26.4")

    def test_error_kode_1(self):
        kode, out, err = jalankan("map", "--sistolik", "80", "--diastolik", "120")
        self.assertEqual(kode, 1)
        self.assertIn("Input tidak valid", err)
        kode, _, err = jalankan("kognitif", "--instrumen", "moca", "--skor", "20",
                                "--pendidikan-tahun", "sembilan")
        self.assertEqual(kode, 1)


if __name__ == "__main__":
    unittest.main(verbosity=1)
