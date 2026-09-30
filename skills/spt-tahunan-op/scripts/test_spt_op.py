#!/usr/bin/env python3
"""Tes regresi spt_op.py. Jalankan: python3 test_spt_op.py

Semua angka pembanding DIHITUNG MANUAL (lihat komentar tiap kasus), bukan disalin dari output script.
Lapisan Pasal 17 (UU HPP): 5% s.d. 60 jt (maks Rp3.000.000) · 15% 60–250 jt (maks Rp28.500.000) ·
25% 250–500 jt (maks Rp62.500.000) · 30% 500 jt–5 M (maks Rp1.350.000.000) · 35% di atasnya.
PTKP: TK/0 54 jt · TK/1 58,5 jt · K/0 58,5 jt · K/1 63 jt · K/2 67,5 jt · K/I/3 126 jt.
"""
import datetime
import io
import json
import os
import subprocess
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from decimal import Decimal as D

FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, FOLDER)
import spt_op  # noqa: E402

HARI = datetime.date(2026, 2, 1)   # sebelum batas lapor, agar tidak ada peringatan telat


def hitung(*argv, hari=HARI):
    args = spt_op.buat_parser().parse_args(list(argv))
    return spt_op.hitung(args, hari)


def gagal(*argv):
    """Jalankan main(); kembalikan (kode keluar, stderr)."""
    err, out = io.StringIO(), io.StringIO()
    with redirect_stderr(err), redirect_stdout(out):
        try:
            kode = spt_op.main(list(argv))
        except SystemExit as e:   # error argparse
            kode = e.code
    return kode, err.getvalue()


class TestKasus(unittest.TestCase):
    def test_01_karyawan_satu_pemberi_kerja_nihil(self):
        # TK/0, neto A1 114.000.000, PPh 21 dipotong 3.000.000
        # PKP = 114.000.000 − 54.000.000 = 60.000.000 → 5% = 3.000.000 → kredit 3.000.000 → NIHIL
        h = hitung("--status", "TK/0", "--tahun", "2025", "--a1", "114jt", "3jt")
        self.assertEqual(h["ptkp"], D(54000000))
        self.assertEqual(h["pkp"], D(60000000))
        self.assertEqual(h["pph_terutang"], D(3000000))
        self.assertEqual(h["selisih"], 0)
        self.assertEqual(h["status_spt"], "NIHIL")
        self.assertIsNone(h["perkiraan_pph25_per_bulan_tahun_berikut"])

    def test_02_karyawan_dua_pemberi_kerja_kurang_bayar(self):
        # K/1 → PTKP 63.000.000. A1 #1 neto 90 jt (dipotong 1.350.000 = 5% × 27 jt); A1 #2 neto 60 jt (dipotong 0)
        # Neto 150.000.000 − 63.000.000 = PKP 87.000.000
        # PPh = 5% × 60 jt (3.000.000) + 15% × 27 jt (4.050.000) = 7.050.000
        # Kredit 1.350.000 → KURANG BAYAR 5.700.000
        h = hitung("--status", "K/1", "--tahun", "2025", "--a1", "90jt", "1.350.000", "--a1", "60jt", "0")
        self.assertEqual(h["penghasilan_neto"], D(150000000))
        self.assertEqual(h["pkp"], D(87000000))
        self.assertEqual(h["pph_terutang"], D(7050000))
        self.assertEqual(h["total_kredit"], D(1350000))
        self.assertEqual(h["selisih"], D(5700000))
        self.assertEqual(h["status_spt"], "KURANG BAYAR")
        self.assertTrue(any("2 bukti potong" in c for c in h["catatan"]))

    def test_03_freelancer_nppn_kurang_bayar(self):
        # TK/1 → PTKP 58.500.000. NPPN bruto 240 jt × 50% = neto 120.000.000
        # PKP 61.500.000 → 3.000.000 + 15% × 1.500.000 (225.000) = 3.225.000
        # Kredit PPh 21 bukan pegawai 2.400.000 → KB 825.000; PPh 25 depan = (3.225.000 − 2.400.000)/12 = 68.750
        h = hitung("--status", "TK/1", "--tahun", "2025", "--nppn", "240jt", "50%", "--nppn-diberitahukan", "ya",
                   "--pph21-lain", "2,4jt")
        self.assertEqual(h["penghasilan_neto"], D(120000000))
        self.assertEqual(h["pkp"], D(61500000))
        self.assertEqual(h["pph_terutang"], D(3225000))
        self.assertEqual(h["selisih"], D(825000))
        self.assertEqual(h["perkiraan_pph25_per_bulan_tahun_berikut"], D(68750))

    def test_04_karyawan_plus_nppn_zakat_pph25(self):
        # K/2 → PTKP 67.500.000. A1 neto 120 jt (PPh 21 2.625.000); NPPN 300 jt × 32% = 96.000.000
        # Jumlah 216.000.000 − zakat 5.000.000 = 211.000.000 → PKP 143.500.000
        # PPh = 3.000.000 + 15% × 83.500.000 (12.525.000) = 15.525.000
        # Kredit 2.625.000 + PPh 25 6.000.000 = 8.625.000 → KB 6.900.000
        # PPh 25 depan = (15.525.000 − 2.625.000)/12 = 12.900.000/12 = 1.075.000
        h = hitung("--status", "K/2", "--tahun", "2025", "--a1", "120jt", "2.625.000", "--nppn", "300jt", "32",
                   "--nppn-diberitahukan", "ya", "--zakat", "5jt", "--pph25", "6jt")
        self.assertEqual(h["zakat_dikurangkan"], D(5000000))
        self.assertEqual(h["pkp"], D(143500000))
        self.assertEqual(h["pph_terutang"], D(15525000))
        self.assertEqual(h["selisih"], D(6900000))
        self.assertEqual(h["perkiraan_pph25_per_bulan_tahun_berikut"], D(1075000))

    def test_05_zakat_membuat_lebih_bayar(self):
        # TK/0, A1 neto 150 jt; PPh 21 dipotong kantor = PKP 96 jt → 3.000.000 + 15% × 36 jt = 8.400.000
        # Zakat mandiri ke BAZNAS 3.750.000 → neto 146.250.000 → PKP 92.250.000
        # PPh = 3.000.000 + 15% × 32.250.000 (4.837.500) = 7.837.500 → LEBIH BAYAR 562.500
        h = hitung("--status", "TK/0", "--tahun", "2025", "--a1", "150jt", "8,4jt", "--zakat", "3.750.000")
        self.assertEqual(h["pkp"], D(92250000))
        self.assertEqual(h["pph_terutang"], D(7837500))
        self.assertEqual(h["selisih"], D(-562500))
        self.assertEqual(h["status_spt"], "LEBIH BAYAR")

    def test_06_freelancer_lebih_bayar_pkp_nol(self):
        # TK/0, NPPN 100 jt × 50% = 50.000.000 < PTKP 54 jt → PKP 0 → PPh 0
        # PPh 21 bukan pegawai dipotong 2.500.000 → LEBIH BAYAR 2.500.000
        h = hitung("--status", "TK/0", "--tahun", "2025", "--nppn", "100jt", "50", "--nppn-diberitahukan", "ya",
                   "--pph21-lain", "2.500.000")
        self.assertEqual(h["pkp"], 0)
        self.assertEqual(h["pph_terutang"], 0)
        self.assertEqual(h["selisih"], D(-2500000))
        self.assertEqual(h["perkiraan_pph25_per_bulan_tahun_berikut"], 0)

    def test_07_suami_istri_digabung(self):
        # K/I/3 → PTKP 54 + 54 + 4,5 + 13,5 = 126.000.000
        # Suami A1 neto 200 jt (PPh 21 13.200.000); istri pembukuan neto 150 jt → 350.000.000
        # PKP 224.000.000 → 3.000.000 + 15% × 164.000.000 (24.600.000) = 27.600.000
        # Kredit 13.200.000 + PPh 23 1.000.000 = 14.200.000 → KB 13.400.000
        h = hitung("--status", "K/I/3", "--tahun", "2025", "--a1", "200jt", "13,2jt", "--pembukuan-neto", "150jt",
                   "--pph23", "1jt")
        self.assertEqual(h["ptkp"], D(126000000))
        self.assertEqual(h["pph_terutang"], D(27600000))
        self.assertEqual(h["selisih"], D(13400000))

    def test_08_lapisan_35_persen_dan_pembulatan_pkp(self):
        # TK/0, neto 5.055.500.999 → PKP mentah 5.001.500.999 → dibulatkan 5.001.500.000
        # PPh = 3.000.000 + 28.500.000 + 62.500.000 + 1.350.000.000 + 35% × 1.500.000 (525.000) = 1.444.525.000
        h = hitung("--status", "TK/0", "--tahun", "2025", "--a1", "5.055.500.999", "1.444.525.000")
        self.assertEqual(h["pkp_sebelum_bulat"], D(5001500999))
        self.assertEqual(h["pkp"], D(5001500000))
        self.assertEqual(h["pph_terutang"], D(1444525000))
        self.assertEqual(len(h["lapisan_pasal17"]), 5)
        self.assertEqual(h["status_spt"], "NIHIL")

    def test_09_a1_dari_bruto_setengah_tahun(self):
        # TK/0, bruto 60 jt selama 6 bulan, iuran pegawai 1.200.000, PPh 21 0
        # Biaya jabatan = min(5% × 60 jt = 3.000.000; 6 × 500.000 = 3.000.000) = 3.000.000
        # Neto 60.000.000 − 3.000.000 − 1.200.000 = 55.800.000 → PKP 1.800.000 → 5% = 90.000 → KB 90.000
        h = hitung("--status", "TK/0", "--tahun", "2025", "--a1-bruto", "60jt", "0", "6", "1,2jt")
        self.assertEqual(h["penghasilan_neto"], D(55800000))
        self.assertEqual(h["pph_terutang"], D(90000))
        self.assertEqual(h["selisih"], D(90000))

    def test_10_omzet_final_tidak_mengubah_pasal17(self):
        # Sama dengan kasus 01 + omzet PP 55 600 jt (PPh final disetor 500.000) → PPh terutang tetap 3.000.000
        h = hitung("--status", "TK/0", "--tahun", "2025", "--a1", "114jt", "3jt", "--omzet-final", "600jt",
                   "--pph-final", "500rb")
        self.assertEqual(h["pph_terutang"], D(3000000))
        self.assertEqual(h["status_spt"], "NIHIL")
        self.assertEqual(h["omzet_final_pp55"], D(600000000))

    def test_11_zakat_melebihi_neto_dibatasi(self):
        # TK/0, pembukuan neto 10 jt, zakat 12 jt → yang dikurangkan hanya 10 jt → neto 0
        h = hitung("--status", "TK/0", "--tahun", "2025", "--pembukuan-neto", "10jt", "--zakat", "12jt")
        self.assertEqual(h["zakat_dikurangkan"], D(10000000))
        self.assertEqual(h["penghasilan_neto"], 0)
        self.assertTrue(h["peringatan"])


class TestBatasWaktu(unittest.TestCase):
    def test_tp2025_jatuh_tempo_tetap_31_maret_kep55_hapus_sanksi(self):
        # v1.0.1: KEP-55/PJ/2026 BUKAN perpanjangan — jatuh tempo tetap 31 Maret 2026; sanksi dihapus s.d. 30 April
        h = hitung("--status", "TK/0", "--tahun", "2025", "--a1", "114jt", "3jt", hari=datetime.date(2026, 4, 15))
        self.assertEqual(h["batas_lapor"], "2026-03-31")
        self.assertEqual(h["batas_bebas_sanksi_kep55"], "2026-04-30")
        self.assertTrue(h["batas_sudah_lewat"])
        self.assertNotIn("diperpanjang", h["keterangan_batas"])
        self.assertIn("jatuh tempo formal tetap", h["keterangan_batas"])
        self.assertTrue(any("masa penghapusan sanksi" in p for p in h["peringatan"]))
        self.assertFalse(any("Rp100.000" in p for p in h["peringatan"]))

    def test_tp2025_setelah_30_april_kena_denda(self):
        h = hitung("--status", "TK/0", "--tahun", "2025", "--a1", "114jt", "3jt", hari=datetime.date(2026, 5, 1))
        self.assertTrue(any("Rp100.000" in p and "berakhir" in p for p in h["peringatan"]))

    def test_tp2025_sebelum_31_maret(self):
        h = hitung("--status", "TK/0", "--tahun", "2025", "--a1", "114jt", "3jt", hari=datetime.date(2026, 3, 31))
        self.assertFalse(h["batas_sudah_lewat"])
        self.assertEqual(h["peringatan"], [])

    def test_teks_tanpa_kata_diperpanjang(self):
        out = subprocess.run([sys.executable, os.path.join(FOLDER, "spt_op.py"), "--status", "TK/0", "--tahun",
                              "2025", "--a1", "114jt", "3jt", "--hari-ini", "2026-09-30"],
                             capture_output=True, text=True, check=True).stdout
        self.assertNotIn("diperpanjang", out)
        self.assertIn("31 Maret 2026", out)
        self.assertIn("KEP-55/PJ/2026", out)

    def test_tahun_lain_hari_libur_cek_djp(self):
        h = hitung("--status", "TK/0", "--tahun", "2026", "--a1", "114jt", "3jt", hari=datetime.date(2027, 2, 1))
        self.assertEqual(h["batas_lapor"], "2027-03-31")
        self.assertIsNone(h["batas_bebas_sanksi_kep55"])
        self.assertIn("hari libur", h["keterangan_batas"])

    def test_tp2026_lewat(self):
        h = hitung("--status", "TK/0", "--tahun", "2026", "--a1", "114jt", "3jt", hari=datetime.date(2027, 4, 1))
        self.assertEqual(h["batas_lapor"], "2027-03-31")
        self.assertTrue(h["batas_sudah_lewat"])
        self.assertTrue(any("Rp100.000" in p for p in h["peringatan"]))

    def test_tahun_berjalan_perkiraan(self):
        h = hitung("--status", "TK/0", "--tahun", "2026", "--a1", "114jt", "3jt", hari=datetime.date(2026, 9, 30))
        self.assertTrue(any("PERKIRAAN" in p for p in h["peringatan"]))

    def test_default_tahun_lalu(self):
        h = hitung("--status", "TK/0", "--a1", "114jt", "3jt", hari=datetime.date(2026, 9, 30))
        self.assertEqual(h["tahun_pajak"], 2025)


class TestCekA1Tunggal(unittest.TestCase):
    def test_satu_pemberi_kerja_kurang_bayar_disarankan_cek_hrd(self):
        # Skenario 06 penguji: K/2, neto 180 jt, PPh 21 10,5 jt → KB 375.000 → sarankan cek A1 ke HRD
        h = hitung("--status", "K/2", "--tahun", "2025", "--a1", "180jt", "10,5jt")
        self.assertEqual(h["selisih"], D(375000))
        self.assertTrue(h["cek_ulang_a1_ke_hrd"])
        self.assertTrue(any("HRD" in p and "PTKP" in p for p in h["peringatan"]))

    def test_satu_pemberi_kerja_lebih_bayar_juga_dicek(self):
        h = hitung("--status", "TK/0", "--tahun", "2025", "--a1", "114jt", "4jt")
        self.assertEqual(h["status_spt"], "LEBIH BAYAR")
        self.assertTrue(h["cek_ulang_a1_ke_hrd"])

    def test_nihil_atau_dua_pemberi_kerja_tidak_dicek(self):
        self.assertFalse(hitung("--status", "TK/0", "--tahun", "2025", "--a1", "114jt", "3jt")["cek_ulang_a1_ke_hrd"])
        h = hitung("--status", "K/1", "--tahun", "2025", "--a1", "90jt", "1.350.000", "--a1", "60jt", "0")
        self.assertFalse(h["cek_ulang_a1_ke_hrd"])
        self.assertFalse(any("HRD" in p for p in h["peringatan"]))

    def test_zakat_mandiri_tidak_dicek(self):
        # LB karena zakat mandiri itu wajar (kasus 05) → tidak memicu saran cek HRD
        h = hitung("--status", "TK/0", "--tahun", "2025", "--a1", "150jt", "8,4jt", "--zakat", "3.750.000")
        self.assertFalse(h["cek_ulang_a1_ke_hrd"])

    def test_a1_dari_bruto_diberi_catatan_neto(self):
        h = hitung("--status", "TK/0", "--tahun", "2025", "--a1-bruto", "60jt", "0", "6", "1,2jt")
        self.assertTrue(any("dihitung dari bruto" in p for p in h["peringatan"]))


class TestPPhFinal(unittest.TestCase):
    def test_pekerjaan_bebas_disebut(self):
        h = hitung("--status", "TK/0", "--tahun", "2025", "--a1", "114jt", "3jt", "--omzet-final", "600jt",
                   "--pph-final", "500rb")
        self.assertTrue(any("PEKERJAAN BEBAS" in c and "PP 20/2026" in c for c in h["catatan"]))
        # 0,5% × (600 jt − 500 jt) = 500.000 → cocok, tidak ada catatan kewajaran
        self.assertFalse(any("Cek kewajaran PPh final" in c for c in h["catatan"]))

    def test_pph_final_tidak_wajar_dicatat(self):
        # 0,5% × (900 jt − 500 jt) = 2.000.000; diisi 4.500.000 → dicatat
        h = hitung("--status", "TK/0", "--tahun", "2025", "--a1", "114jt", "3jt", "--omzet-final", "900jt",
                   "--pph-final", "4,5jt")
        self.assertTrue(any("Cek kewajaran PPh final" in c and "Rp 2.000.000" in c for c in h["catatan"]))


class TestAngka(unittest.TestCase):
    def test_diterima(self):
        p = spt_op.parse_angka
        self.assertEqual(p("15000"), D(15000))
        self.assertEqual(p("Rp 1.250.000,50"), D("1250000.50"))
        self.assertEqual(p("2,5jt"), D(2500000))
        self.assertEqual(p("500rb"), D(500000))
        self.assertEqual(p("1,2 miliar"), D(1200000000))
        self.assertEqual(p("3.000.000,-"), D(3000000))
        self.assertEqual(p("1.500jt"), D(1500000000))

    def test_ambigu_ditolak(self):
        for s in ["1,500", "2.5jt", "2.5", "1,250,000", "1,250.50", "1.25.000", "5m", "5M", "0.500", "abc", "",
                  "1,500jt"]:
            with self.assertRaises(spt_op.InputError, msg=s):
                spt_op.parse_angka(s)

    def test_negatif_ditolak(self):
        with self.assertRaises(spt_op.InputError):
            spt_op.parse_angka("-5jt")

    def test_koma_tiga_digit_miliar_diterima(self):
        p = spt_op.parse_angka
        self.assertEqual(p("5,054miliar"), D(5054000000))
        self.assertEqual(p("5,054 miliar"), D(5054000000))
        self.assertEqual(p("Rp 1,250 milyar"), D(1250000000))

    def test_m_ditolak_dengan_contoh(self):
        for s in ["5,054 M", "5,054M", "5M"]:
            with self.assertRaises(spt_op.InputError) as cm:
                spt_op.parse_angka(s)
            self.assertIn("5,054 miliar", str(cm.exception))

    def test_koma_tiga_digit_jt_tetap_ditolak_dengan_contoh(self):
        with self.assertRaises(spt_op.InputError) as cm:
            spt_op.parse_angka("1,500jt")
        self.assertIn("1,5jt", str(cm.exception))


class TestError(unittest.TestCase):
    def test_status_salah(self):
        for s in ["K/4", "X/1", "kawin"]:
            kode, err = gagal("--status", s, "--a1", "100jt", "0")
            self.assertEqual(kode, 2, s)
            self.assertIn("ERROR", err)

    def test_nppn_di_atas_4_8_miliar(self):
        kode, err = gagal("--status", "TK/0", "--nppn", "4,5 miliar", "30", "--omzet-final", "400jt")
        self.assertEqual(kode, 2)
        self.assertIn("4,8 miliar", err)

    def test_persen_nppn_salah(self):
        kode, _ = gagal("--status", "TK/0", "--nppn", "100jt", "150")
        self.assertEqual(kode, 2)

    def test_tanpa_penghasilan(self):
        kode, err = gagal("--status", "TK/0")
        self.assertEqual(kode, 2)
        self.assertIn("Tidak ada penghasilan", err)

    def test_singkatan_opsi_ditolak(self):
        kode, _ = gagal("--stat", "TK/0", "--a1", "100jt", "0")
        self.assertEqual(kode, 2)

    def test_angka_ambigu_lewat_cli(self):
        kode, err = gagal("--status", "TK/0", "--a1", "114,000,000", "3jt")
        self.assertEqual(kode, 2)
        self.assertIn("Inggris", err)

    def test_negatif_lewat_cli_pesan_ramah(self):
        for argv in (["--a1", "-10jt", "0"], ["--a1", "100jt", "0", "--zakat", "-5jt"],
                     ["--a1", "100jt", "0", "--pph23", "-Rp1.000.000"]):
            kode, err = gagal("--status", "TK/0", *argv)
            self.assertEqual(kode, 2, argv)
            self.assertIn("tidak boleh negatif", err)
            self.assertNotIn("expected", err)
        kode, err = gagal("--status", "TK/0", "--a1", "100jt", "0", "--zakat", "-5jt")
        self.assertIn("--zakat", err)
        self.assertNotIn("rugi usaha", err)

    def test_negatif_bentuk_sama_dengan(self):
        kode, err = gagal("--status", "TK/0", "--a1", "100jt", "0", "--zakat=-5jt")
        self.assertEqual(kode, 2)
        self.assertIn("tidak boleh negatif", err)
        self.assertNotIn("rugi usaha", err)
        kode, err = gagal("--status", "TK/0", "--pembukuan-neto=-5jt")
        self.assertIn("rugi usaha", err)

    def test_nppn_tanpa_pemberitahuan_diberi_peringatan(self):
        h = hitung("--status", "TK/0", "--tahun", "2025", "--nppn", "200jt", "50", "--nppn-diberitahukan", "tidak")
        self.assertTrue(any("PEMBUKUAN" in p for p in h["peringatan"]))


class TestCLI(unittest.TestCase):
    def test_json_subprocess(self):
        out = subprocess.run([sys.executable, os.path.join(FOLDER, "spt_op.py"), "--status", "K/1", "--tahun", "2025",
                              "--a1", "90jt", "1.350.000", "--a1", "60jt", "0", "--format", "json"],
                             capture_output=True, text=True, check=True).stdout
        d = json.loads(out)
        self.assertEqual(d["selisih"], 5700000)
        self.assertEqual(d["status_spt"], "KURANG BAYAR")

    def test_teks_memuat_disclaimer(self):
        out = subprocess.run([sys.executable, os.path.join(FOLDER, "spt_op.py"), "--status", "TK/0", "--tahun",
                              "2025", "--a1", "114jt", "3jt", "--hari-ini", "2026-02-01"],
                             capture_output=True, text=True, check=True).stdout
        self.assertIn("bukan konsultan pajak", out)
        self.assertIn("Coretax", out)
        self.assertIn("NIHIL", out)


if __name__ == "__main__":
    unittest.main(verbosity=1)
