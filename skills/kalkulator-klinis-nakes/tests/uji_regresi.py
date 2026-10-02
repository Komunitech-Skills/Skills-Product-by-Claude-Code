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
        self.assertTrue(h["map_90_atau_lebih"])

    def test_tepat_90_memenuhi_ambang_kia_2025(self):
        # (110 + 160)/3 = 90 tepat -> Buku KIA cetakan 2025: MAP >= 90 -> YA
        h = k.hitung_map(110, 80)
        self.assertEqual(h["map_mmhg"], "90.0")
        self.assertTrue(h["map_90_atau_lebih"])

    def test_sedikit_di_bawah_90(self):
        # (109 + 160)/3 = 89,666... -> < 90, tampil 89,7 (tidak dibulatkan dulu ke 90)
        h = k.hitung_map(109, 80)
        self.assertEqual(h["map_mmhg"], "89.7")
        self.assertFalse(h["map_90_atau_lebih"])

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
        self.assertTrue(h["kategori"].startswith("RISIKO TINGGI"))
        self.assertIn("rujukan terencana", h["arti"])
        self.assertIn("Rumah Sakit", h["arti"])

    def test_belum_ditanyakan_memuat_hipertensi_kronik(self):
        h = k.skrining_preeklampsia(["nullipara"])
        t = " ".join(h["catatan"])
        self.assertIn("Belum ditanyakan", t)
        for x in ("hipertensi kronik", "diabetes", "penyakit ginjal", "autoimun/APS"):
            self.assertIn(x, t)
        h2 = k.skrining_preeklampsia(["hipertensi-kronik", "diabetes"])
        t2 = " ".join(h2["catatan"])
        self.assertNotIn("hipertensi kronik,", t2.split("Belum ditanyakan")[-1])

    def test_dua_sedang(self):
        h = k.skrining_preeklampsia(["nullipara", "riwayat-keluarga"])
        self.assertTrue(h["kategori"].startswith("BERISIKO PREEKLAMPSIA - perlu rujukan terencana"))

    def test_label_berisiko_bukan_risiko_sedang(self):
        # v1.0.x openclaw: label lama "RISIKO SEDANG" terbaca seperti risiko menengah.
        for ped in ("kia", "nice"):
            h = k.skrining_preeklampsia(["nullipara", "riwayat-keluarga"], pedoman=ped)
            self.assertTrue(h["kategori"].startswith("BERISIKO PREEKLAMPSIA"))
            self.assertNotIn("RISIKO SEDANG (", h["kategori"])
        h = k.skrining_preeklampsia(["nullipara", "riwayat-keluarga"])
        self.assertIn("rujukan terencana", h["kategori"])

    def test_satu_sedang_saja(self):
        h = k.skrining_preeklampsia(["nullipara"])
        self.assertTrue(h["kategori"].startswith("1 FAKTOR RISIKO SEDANG"))

    def test_kosong(self):
        h = k.skrining_preeklampsia([""])
        self.assertTrue(h["kategori"].startswith("TIDAK DITEMUKAN"))

    def test_map_dari_angka_menambah_faktor(self):
        # nullipara + MAP 93,3 -> 2 faktor sedang
        h = k.skrining_preeklampsia(["nullipara"], 120, 80)
        self.assertIn("map-90", h["faktor_dari_angka"])
        self.assertTrue(h["kategori"].startswith("BERISIKO PREEKLAMPSIA - perlu rujukan terencana"))

    def test_map_tepat_90_menambah_faktor(self):
        # Buku KIA cetakan 2025: MAP >= 90 -> nullipara + MAP 90,0 = 2 sedang
        h = k.skrining_preeklampsia(["nullipara"], 110, 80)
        self.assertIn("map-90", h["faktor_dari_angka"])
        self.assertTrue(h["kategori"].startswith("BERISIKO PREEKLAMPSIA - perlu rujukan terencana"))
        h = k.skrining_preeklampsia(["nullipara"], 109, 80)  # 89,67
        self.assertTrue(h["kategori"].startswith("1 FAKTOR RISIKO SEDANG"))

    def test_usia_40_tidak_dihitung_ganda_di_kia(self):
        # usia 41 -> usia-ibu-35 (KIA) ; usia-ibu-40 tidak boleh jadi faktor sedang kedua
        h = k.skrining_preeklampsia([], usia_ibu=41)
        self.assertTrue(h["kategori"].startswith("1 FAKTOR RISIKO SEDANG"))

    def test_imt_batas(self):
        # KIA: IMT > 30. 30,0 tidak ; 30,1 ya
        self.assertTrue(k.skrining_preeklampsia([], imt="30.0")["kategori"].startswith("TIDAK"))
        self.assertTrue(k.skrining_preeklampsia([], imt="30,1")["kategori"].startswith(
            "1 FAKTOR RISIKO SEDANG"))

    def test_nice_kembar_sedang_usia_35_tidak_dihitung(self):
        # NICE: kembar = sedang, usia 36 tidak termasuk (batas NICE 40)
        h = k.skrining_preeklampsia(["kehamilan-multipel"], usia_ibu=36, pedoman="nice")
        self.assertTrue(h["kategori"].startswith("1 FAKTOR RISIKO SEDANG"))
        # Buku KIA: kembar = tinggi
        h2 = k.skrining_preeklampsia(["kehamilan-multipel"], usia_ibu=36, pedoman="kia")
        self.assertTrue(h2["kategori"].startswith("RISIKO TINGGI"))

    def test_kode_tidak_dikenal(self):
        # v1.0.2: tidak lagi dilempar; dilaporkan di field kode_tidak_dikenal (CLI exit 1)
        h = k.skrining_preeklampsia(["darah-tinggi-banget"])
        self.assertEqual(h["kode_tidak_dikenal"], ["faktor: darah-tinggi-banget"])

    def test_map_setengah(self):
        # v1.0.2: TD parsial tidak ditolak; MAP tidak dihitung, ada peringatan
        h = k.skrining_preeklampsia(["nullipara"], 120, None)
        self.assertIsNone(h["map"])
        self.assertIn("Diastolik TIDAK diisi", h["peringatan"])

    def test_wajib_sumber_dan_penafian(self):
        h = k.skrining_preeklampsia(["nullipara"])
        self.assertIn("2025", h["sumber"][0])
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
        # R3: tanpa jenis kelamin -> IMT tetap keluar, LP tidak dinilai
        h = k.imt_dewasa(165, 72, 90, None)
        self.assertEqual(h["imt"], "26.4")
        self.assertIn("tidak dinilai", h["lingkar_perut"])

    def test_catatan_beda_kategori(self):
        # R5: IMT 25,0 -> Obesitas I (AP) vs Normal (Kemenkes) -> ada catatan
        self.assertTrue(any("berbeda" in c for c in k.imt_dewasa(200, 100)["catatan"]))
        # 60/1,65^2 = 22,0 normal di keduanya; 40/1,7^2 = 13,8 kurang di keduanya -> tanpa catatan
        self.assertFalse(any("berbeda" in c for c in k.imt_dewasa(165, 60)["catatan"]))
        self.assertFalse(any("berbeda" in c for c in k.imt_dewasa(170, 40)["catatan"]))

    def test_batch(self):
        # R7: 72/1,65^2 = 26,4 ; 55/1,55^2 = 22,89 -> 22,9 ; baris rusak tidak menghentikan
        h = k.imt_batch("id,tinggi,berat,lingkar_perut,jk\nA1,165,72,92,L\n"
                        "A2,155,55,,\nA3,abc,60,,\n")
        self.assertIn("A1 | IMT 26.4", h["hasil_per_pasien"][0])
        self.assertIn("obesitas sentral", h["hasil_per_pasien"][0])
        self.assertIn("A2 | IMT 22.9", h["hasil_per_pasien"][1])
        self.assertIn("TIDAK DIHITUNG", h["hasil_per_pasien"][2])
        self.assertEqual(h["ringkasan"], "2 dihitung, 1 tidak dihitung (cek data)")
        with self.assertRaises(k.InputSalah):
            k.imt_batch("nama,umur\nX,5\n")

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
        # R2: posisi terhadap asumsi IOM trimester 1 (0,5-2 kg)
        self.assertEqual(h["perkiraan_trimester_1_kg"], "0.5-2.0")
        self.assertIn("di dalam", h["posisi"])
        self.assertIn("di bawah", k.bb_hamil(160, 55, "54.5", 10)["posisi"])

    def test_posisi_konsisten_dengan_tampilan(self):
        # R1: normal, 16 mgg: bawah 0,5+0,35*3 = 1,55 -> 1,6 ; atas 2+0,5*3 = 3,5.
        # naik 3,54 -> tampil 3,5 -> harus "di dalam" (bukan "di atas 3,5")
        h = k.bb_hamil(160, 55, "58.54", 16)
        self.assertEqual(h["perkiraan_rentang_saat_ini_kg"], "1.6-3.5")
        self.assertIn("Kenaikan 3.5 kg di dalam", h["posisi"])

    def test_catatan_keterbatasan_iom(self):
        self.assertTrue(any("lebih pendek" in c for c in k.bb_hamil(155, 50)["catatan"]))

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


class TesRevisi101(unittest.TestCase):
    """Temuan HASIL-UJI v1.0.0 (T1-T3, S1-S3, S6, R4, R6)."""

    def json_teks(self, h):
        return json.dumps(h, ensure_ascii=False)

    def test_T2_proteinuria_tunggal_sedang_bukan_tinggi(self):
        h = k.skrining_preeklampsia(["proteinuria"])
        self.assertTrue(h["kategori"].startswith("1 FAKTOR RISIKO SEDANG"))
        self.assertEqual(h["faktor_tinggi"], [])
        h = k.skrining_preeklampsia(["proteinuria", "nullipara"])
        self.assertTrue(h["kategori"].startswith("BERISIKO PREEKLAMPSIA - perlu rujukan terencana"))

    def test_T3_td_berat_tidak_pernah_anc_rutin(self):
        for s, d in ((170, 115), (160, 80), (150, 110), (200, 120)):
            for f in ([], ["nullipara"], ["hipertensi-kronik"]):
                for ped in ("kia", "nice"):
                    h = k.skrining_preeklampsia(f, s, d, pedoman=ped)
                    self.assertTrue(h["kategori"].startswith("TANDA BAHAYA"), (s, d, f, ped))
                    self.assertNotIn("ANC rutin", self.json_teks(h))
                    self.assertNotIn("Lanjutkan ANC rutin", h["arti"])
                    self.assertIn("SEGERA", h["arti"])
                    self.assertIn("protokol", h["arti"])
                    self.assertTrue(any("160/110" in x for x in h["sumber"]))

    def test_T3_td_hipertensi_150_95_evaluasi_hari_ini(self):
        for s, d in ((150, 95), (140, 80), (130, 90), (159, 109)):
            h = k.skrining_preeklampsia([], s, d)
            self.assertTrue(h["kategori"].startswith("TD RENTANG HIPERTENSI"), (s, d))
            self.assertNotIn("ANC rutin", self.json_teks(h))
            self.assertIn("rujuk", h["arti"])

    def test_T3_td_normal_tidak_ada_tanda_bahaya(self):
        for s, d in ((139, 89), (120, 80)):
            h = k.skrining_preeklampsia([], s, d)
            self.assertIsNone(h["tanda_bahaya"])

    def test_T3_gejala_bahaya(self):
        for g in k.GEJALA_BAHAYA:
            h = k.skrining_preeklampsia([], gejala=[g])
            self.assertTrue(h["kategori"].startswith("TANDA BAHAYA"), g)
            self.assertNotIn("ANC rutin", self.json_teks(h))
        h = k.skrining_preeklampsia([], gejala=["pusing-dikit"])  # v1.0.2: dilaporkan
        self.assertEqual(h["kode_tidak_dikenal"], ["gejala: pusing-dikit"])

    def test_T3_perintah_map_juga_menandai(self):
        self.assertIn("SEGERA", k.hitung_map(170, 115)["tanda_bahaya"])
        self.assertIn("HARI INI", k.hitung_map(150, 95)["tanda_bahaya"])
        self.assertIsNone(k.hitung_map(120, 80)["tanda_bahaya"])

    def test_T3_cli_170_115(self):
        kode, out, _ = jalankan("preeklampsia", "--sistolik", "170", "--diastolik", "115")
        self.assertEqual(kode, 0)
        self.assertIn("!! TANDA BAHAYA", out)
        self.assertNotIn("Lanjutkan ANC rutin", out)
        kode, out, _ = jalankan("preeklampsia", "--faktor", "nullipara", "--gejala", "kejang")
        self.assertIn("SEGERA", out)

    def test_S1_nice_hanya_dm_tipe_1_2(self):
        h = k.skrining_preeklampsia(["diabetes-gestasional"], pedoman="nice")
        self.assertTrue(h["kategori"].startswith("TIDAK DITEMUKAN"))
        self.assertTrue(any("tidak tercantum di NICE" in c for c in h["catatan"]))
        h = k.skrining_preeklampsia(["diabetes-pregestasional"], pedoman="nice")
        self.assertTrue(h["kategori"].startswith("RISIKO TINGGI"))
        h = k.skrining_preeklampsia(["diabetes"], pedoman="nice")  # v1.0.2: dilaporkan, bukan dilempar
        self.assertTrue(any("diabetes" in x for x in h["kode_tidak_dikenal"]))
        # Buku KIA: diabetes dalam kehamilan = tinggi (semua kode diabetes)
        for f in ("diabetes", "diabetes-gestasional", "diabetes-pregestasional"):
            self.assertTrue(k.skrining_preeklampsia([f])["kategori"].startswith("RISIKO TINGGI"))

    def test_S2_riwayat_hipertensi_tanpa_pe(self):
        h = k.skrining_preeklampsia(["riwayat-hipertensi-kehamilan"], pedoman="kia")
        self.assertTrue(h["kategori"].startswith("TIDAK DITEMUKAN"))
        self.assertTrue(any("NICE NG133 = faktor tinggi" in c for c in h["catatan"]))
        h = k.skrining_preeklampsia(["riwayat-hipertensi-kehamilan"], pedoman="nice")
        self.assertTrue(h["kategori"].startswith("RISIKO TINGGI"))

    def test_sumber_aturan_disebut(self):
        self.assertTrue(any("Buku KIA" in c for c in
                            k.skrining_preeklampsia(["nullipara"])["catatan"]))
        self.assertTrue(any("NICE NG133 (rek. 1.1.2)" in c for c in
                            k.skrining_preeklampsia(["nullipara"], pedoman="nice")["catatan"]))

    def test_S6_siklus_di_luar_rentang_tetap_pakai_usg(self):
        # USG 2 Mei 2026 usia 7w3d (52 hr) + 150 hari ke 29 Sep = 202 = 28w6d
        h = k.kalkulator_kehamilan("2026-03-10", siklus=60, tanggal_periksa="2026-09-29",
                                   usg_tanggal="2026-05-02", usg_minggu=7, usg_hari=3)
        self.assertEqual(h["penanggalan_dipakai"], "USG")
        self.assertEqual(h["usia_kehamilan"], "28 minggu 6 hari")
        self.assertNotIn("hpl_naegele", h)
        self.assertTrue(any("TIDAK ANDAL" in c for c in h["catatan"]))
        # HPHT > 44 minggu tapi ada USG -> tetap jalan dengan USG
        h = k.kalkulator_kehamilan("2025-01-01", tanggal_periksa="2026-09-29",
                                   usg_tanggal="2026-05-02", usg_minggu=7, usg_hari=3)
        self.assertEqual(h["penanggalan_dipakai"], "USG")

    def test_R4_sumber_acog(self):
        h = k.kalkulator_kehamilan("2026-03-10", tanggal_periksa="2026-09-29")
        self.assertFalse(any("ACOG" in x for x in h["sumber"]))
        h = k.kalkulator_kehamilan(None, tanggal_periksa="2027-03-12", usg_tanggal="2027-03-12",
                                   usg_minggu=12, usg_hari=0)
        self.assertTrue(any("reaffirmed 2025" in x for x in h["sumber"]))

    def test_R6_catatan_kognitif_dan_lisensi(self):
        for ins in ("mmse", "moca", "amt"):
            teks = self.json_teks(k.kognitif(ins, 5, 6))
            self.assertIn("delirium", teks)
        for ins in ("mmse", "moca"):
            teks = self.json_teks(k.kognitif(ins, 20, 6))
            self.assertIn("HANYA menafsirkan skor total", teks)
            self.assertIn("lisensi/izin", teks)



class TesRevisi102(unittest.TestCase):
    """Temuan HASIL-UJI-ULANG v1.0.1 (S-baru-1 s.d. S-baru-4)."""

    def json_teks(self, h):
        return json.dumps(h, ensure_ascii=False)

    # 1) TD parsial
    def test_hanya_sistolik_170_tanda_bahaya(self):
        h = k.skrining_preeklampsia([], 170, None)
        self.assertTrue(h["kategori"].startswith("TANDA BAHAYA"))
        self.assertIn("170/?", h["tanda_bahaya"])
        self.assertIn("Diastolik TIDAK diisi", h["peringatan"])
        self.assertNotIn("ANC rutin", self.json_teks(h))
        self.assertIsNone(h["map"])

    def test_hanya_diastolik(self):
        h = k.skrining_preeklampsia([], None, 112)
        self.assertTrue(h["kategori"].startswith("TANDA BAHAYA"))
        self.assertIn("Sistolik TIDAK diisi", h["peringatan"])
        h = k.skrining_preeklampsia([], None, 95)
        self.assertTrue(h["kategori"].startswith("TD RENTANG HIPERTENSI"))
        # parsial normal: tidak ada tanda bahaya, tapi tidak boleh "Lanjutkan ANC rutin" polos
        h = k.skrining_preeklampsia([], 120, None)
        self.assertIsNone(h["tanda_bahaya"])
        self.assertNotIn("Lanjutkan ANC rutin", h["arti"])
        self.assertIn("Diastolik TIDAK diisi", h["peringatan"])

    def test_parsial_di_luar_rentang_tetap_ditolak(self):
        for s, d in ((400, None), (None, 5), ("abc", None)):
            with self.assertRaises(k.InputSalah, msg=(s, d)):
                k.skrining_preeklampsia([], s, d)

    def test_cli_hanya_sistolik(self):
        kode, out, _ = jalankan("preeklampsia", "--sistolik", "170")
        self.assertEqual(kode, 0)
        self.assertIn("!! TANDA BAHAYA", out)
        self.assertIn("Diastolik TIDAK diisi", out)
        kode, out, _ = jalankan("map", "--diastolik", "112")
        self.assertEqual(kode, 0)
        self.assertIn("SEGERA", out)
        self.assertIn("Sistolik TIDAK diisi", out)
        kode, _, err = jalankan("map")
        self.assertEqual(kode, 1)

    # 2) Kode tak dikenal tidak menekan tanda bahaya
    def test_cli_kode_tidak_dikenal_tanda_bahaya_dulu(self):
        kode, out, err = jalankan("preeklampsia", "--faktor", "preeklampsia-dulu",
                                  "--sistolik", "170", "--diastolik", "115", "--gejala", "pusing")
        self.assertEqual(kode, 1)
        self.assertIn("!! TANDA BAHAYA", out)
        self.assertIn("SEGERA", out)
        self.assertIn("preeklampsia-dulu", err)
        self.assertIn("pusing", err)
        self.assertIn("nyeri-kepala-hebat", err)   # daftar kode gejala valid
        self.assertIn("riwayat-preeklampsia", err)  # daftar kode faktor valid

    def test_cli_gejala_tak_dikenal_bersama_gejala_valid(self):
        kode, out, err = jalankan("preeklampsia", "--gejala", "pusing,kejang")
        self.assertEqual(kode, 1)
        self.assertIn("SEGERA", out)
        self.assertIn("pusing", err)

    def test_cli_map_gejala_tak_dikenal(self):
        kode, out, err = jalankan("map", "--sistolik", "165", "--diastolik", "100",
                                  "--gejala", "pandangan kabur")
        self.assertEqual(kode, 1)
        self.assertIn("SEGERA", out)
        self.assertIn("pandangan kabur", err)

    def test_json_kode_tidak_dikenal(self):
        kode, out, err = jalankan("--json", "preeklampsia", "--sistolik", "170",
                                  "--diastolik", "115", "--gejala", "pusing")
        self.assertEqual(kode, 1)
        h = json.loads(out)
        self.assertTrue(h["kategori"].startswith("TANDA BAHAYA"))
        self.assertEqual(h["kode_tidak_dikenal"], ["gejala: pusing"])

    def test_kode_tak_dikenal_tanpa_bahaya_tidak_anc_polos(self):
        h = k.skrining_preeklampsia(["darah-tinggi-dulu"], 120, 80)
        self.assertNotIn("Lanjutkan ANC rutin", h["arti"])
        self.assertIn("kode tidak dikenal", h["peringatan"])

    # 3) Tanpa TD
    def test_tanpa_td_tidak_anc_polos(self):
        for f in ([], ["nullipara"]):
            h = k.skrining_preeklampsia(f)
            self.assertNotIn("Lanjutkan ANC rutin", h["arti"])
            self.assertIn("Tanda bahaya (TD/gejala) belum diperiksa", h["peringatan"])
        kode, out, _ = jalankan("preeklampsia")
        self.assertEqual(kode, 0)
        self.assertIn("Tanda bahaya (TD/gejala) belum diperiksa", out)
        self.assertNotIn("Lanjutkan ANC rutin", out)
        # TD lengkap & normal -> saran rutin boleh, tanpa peringatan
        h = k.skrining_preeklampsia([], 120, 80)
        self.assertIsNone(h["peringatan"])

    # 4) Hipotensi
    def test_td_rendah(self):
        for s, d in ((75, 45), (89, 70), (100, 59), (89.9, 60)):
            h = k.skrining_preeklampsia([], s, d)
            self.assertTrue(h["kategori"].startswith("TD RENDAH"), (s, d))
            self.assertIn("TD rendah", h["arti"])
            self.assertNotIn("ANC rutin", self.json_teks(h))
            self.assertTrue(any("NHLBI" in x and "PERLU REVIEW" in x for x in h["sumber"]))
        for s, d in ((90, 60), (110, 70)):
            self.assertIsNone(k.skrining_preeklampsia([], s, d)["tanda_bahaya"], (s, d))
        self.assertIn("TD RENDAH", k.hitung_map(85, 50)["tanda_bahaya"])
        self.assertIn("TD RENDAH", k.skrining_preeklampsia([], 85, None)["kategori"])

    def test_td_tinggi_plus_diastolik_rendah(self):
        # 150/55: hipertensi (kategori lebih tinggi) + komponen TD rendah disebut
        h = k.skrining_preeklampsia([], 150, 55)
        self.assertTrue(h["kategori"].startswith("TD RENTANG HIPERTENSI"))
        self.assertIn("RENDAH", h["tanda_bahaya"])
        self.assertIn("TD rendah", h["arti"])

    # 5) imt-batch
    def test_batch_koma_desimal_tanpa_kutip(self):
        h = k.imt_batch("id,tinggi,berat,lingkar_perut,jk\nA1,165,72,92,L\nA2,1,65,70,82,P\n")
        self.assertIn("A1 | IMT 26.4", h["hasil_per_pasien"][0])
        self.assertIn("GAGAL", h["hasil_per_pasien"][1])
        self.assertIn("koma desimal", h["hasil_per_pasien"][1])
        self.assertEqual(h["ringkasan"], "1 dihitung, 1 tidak dihitung (cek data)")

    def test_batch_titik_koma(self):
        # 70,5 / 1,65^2 = 70,5 / 2,7225 = 25,895 -> 25,9 ; 55/1,55^2 = 22,89 -> 22,9
        h = k.imt_batch("id;tinggi;berat\nB1;1,65;70,5\nB2;155;55\n")
        self.assertIn("B1 | IMT 25.9", h["hasil_per_pasien"][0])
        self.assertIn("B2 | IMT 22.9", h["hasil_per_pasien"][1])
        self.assertTrue(any("titik koma" in c for c in h["catatan"]))

    def test_batch_pesan_pemisah(self):
        with self.assertRaises(k.InputSalah) as e:
            k.imt_batch("id|tinggi|berat\nX|160|60\n")
        self.assertIn("Pemisah", str(e.exception))

    def test_cli_batch_tidak_crash(self):
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False,
                                         encoding="utf-8") as f:
            f.write("id,tinggi,berat\nA1,1,65,70\nA2,160,60\n")
            nama = f.name
        try:
            kode, out, _ = jalankan("imt-batch", "--file", nama)
        finally:
            os.unlink(nama)
        self.assertEqual(kode, 0)
        self.assertIn("GAGAL", out)
        self.assertIn("A2 | IMT 23.4", out)  # 60/2,56 = 23,4375 -> 23,4


if __name__ == "__main__":
    unittest.main(verbosity=1)
