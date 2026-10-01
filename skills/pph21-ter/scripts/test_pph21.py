#!/usr/bin/env python3
"""Uji otomatis kalkulator PPh 21 TER. Jalankan: python3 test_pph21.py

Semua angka pembanding diambil dari contoh RESMI:
- Penjelasan PP 58/2023 Pasal 2 (K/0 Rp10 jt, iuran Rp100 rb -> Desember Rp515.000)
- Lampiran PMK 168/2023 Bagian Kedua (Tuan A, B, C, D, E, K, L, M, Z, N)
- Lampiran B PMK 105/2025 (contoh PPh 21 DTP 2026: Tuan A, B, C)
"""
import csv
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal as D

FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, FOLDER)
import ter_core as tc  # noqa: E402
import pph21  # noqa: E402

# SHA-256 ter_tabel.json = research/sources/pph21-ter-tabel.json (terverifikasi dari Lampiran PP 58/2023)
SHA256_TABEL = "26edfe89bda74169a5280317da194cec3194e8c48c661a8e6860ff8b48d5da72"
SUMBER_REPO = os.path.normpath(os.path.join(FOLDER, "..", "..", "..", "research", "sources", "pph21-ter-tabel.json"))


def jalankan(*argv):
    """Jalankan subperintah lewat main() dan kembalikan hasil dict (via cmd_*)."""
    args = pph21.buat_parser().parse_args(list(argv))
    fn = {"bulan": pph21.cmd_bulan, "setahun": pph21.cmd_setahun, "harian": pph21.cmd_harian,
          "tabel": pph21.cmd_tabel}[args.perintah]
    return fn(args)


def tulis_csv(baris, kolom):
    f = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, newline="", encoding="utf-8")
    w = csv.writer(f)
    w.writerow(kolom)
    for b in baris:
        w.writerow(b)
    f.close()
    return f.name


class TestTabel(unittest.TestCase):
    def test_hash_salinan(self):
        with open(tc.FILE_TABEL, "rb") as f:
            self.assertEqual(hashlib.sha256(f.read()).hexdigest(), SHA256_TABEL,
                             "ter_tabel.json berubah dari salinan resmi yang terverifikasi")

    def test_sama_dengan_sumber_repo(self):
        if not os.path.exists(SUMBER_REPO):
            self.skipTest("sumber riset tidak ada (paket pembeli) — dicek lewat hash")
        with open(SUMBER_REPO, encoding="utf-8") as a, open(tc.FILE_TABEL, encoding="utf-8") as b:
            self.assertEqual(json.load(a), json.load(b))

    def test_struktur(self):
        t = tc.muat_tabel()
        self.assertEqual([len(t[k]) for k in ("A", "B", "C", "harian")], [44, 40, 41, 2])
        for k in ("A", "B", "C"):
            tarif = [r[2] for r in t[k]]
            self.assertEqual(tarif, sorted(tarif))
            self.assertEqual(tarif[0], 0)
            self.assertEqual(tarif[-1], 34)
            self.assertIsNone(t[k][-1][1])

    def test_kategori(self):
        for p, k in [("TK/0", "A"), ("TK/1", "A"), ("K/0", "A"), ("TK/2", "B"), ("TK/3", "B"), ("K/1", "B"),
                     ("K/2", "B"), ("K/3", "C"), ("k3", "C"), ("tk 0", "A"), ("K-2", "B")]:
            self.assertEqual(tc.kategori_ter(p), k, p)

    def test_ptkp(self):
        self.assertEqual(tc.ptkp_setahun("TK/0"), 54000000)
        self.assertEqual(tc.ptkp_setahun("K/0"), 58500000)
        self.assertEqual(tc.ptkp_setahun("TK/1"), 58500000)
        self.assertEqual(tc.ptkp_setahun("K/1"), 63000000)
        self.assertEqual(tc.ptkp_setahun("K/3"), 72000000)

    def test_tabel_referensi_dibuat_dari_json(self):
        ref = os.path.join(FOLDER, "..", "references", "tabel-ter.md")
        if not os.path.exists(ref):
            self.skipTest("references/tabel-ter.md belum dibuat")
        with open(ref, encoding="utf-8") as f:
            isi = f.read()
        self.assertIn(pph21.teks_tabel(jalankan("tabel")), isi)


class TestBatas(unittest.TestCase):
    def tarif(self, bruto, kat):
        return tc.tarif_ter_bulanan(D(bruto), kat)[0]

    def test_batas_pertama(self):
        self.assertEqual(self.tarif(5400000, "A"), 0)
        self.assertEqual(self.tarif(5400001, "A"), D("0.25"))
        self.assertEqual(self.tarif(6200000, "B"), 0)
        self.assertEqual(self.tarif(6200001, "B"), D("0.25"))
        self.assertEqual(self.tarif(6600000, "C"), 0)
        self.assertEqual(self.tarif(6600001, "C"), D("0.25"))
        self.assertEqual(self.tarif(0, "A"), 0)

    def test_batas_tengah_inklusif_atas(self):
        self.assertEqual(self.tarif(10050000, "A"), 2)
        self.assertEqual(self.tarif(10050001, "A"), D("2.25"))
        self.assertEqual(self.tarif(D("10050000.5"), "A"), D("2.25"))

    def test_baris_terakhir(self):
        self.assertEqual(self.tarif(1400000000, "A"), 33)
        self.assertEqual(self.tarif(1400000001, "A"), 34)
        self.assertEqual(self.tarif(1419000001, "C"), 34)

    def test_k3_kategori_c(self):
        h = jalankan("bulan", "--ptkp", "K/3", "--bruto", "6.600.000")
        self.assertEqual((h["kategori"], h["pph21"]), ("C", 0))
        h = jalankan("bulan", "--ptkp", "K/3", "--bruto", "10jt")
        self.assertEqual(h["tarif_ter_persen"], D("1.5"))  # C: 9,8 jt s.d. 10,95 jt = 1,5%

    def test_harian(self):
        self.assertEqual(tc.pph_harian(450000)["pph"], 0)
        self.assertEqual(tc.pph_harian(450001)["tarif"], D("0.5"))
        self.assertEqual(tc.pph_harian(2500000)["pph"], 12500)          # tepat batas: masih TER harian
        h = tc.pph_harian(2500001)
        self.assertEqual(h["metode"], "Pasal 17 x 50% bruto")
        self.assertEqual(h["pph"], 62500)                               # 5% x 1.250.000,5 -> dibulatkan ke bawah

    def test_pasal17(self):
        self.assertEqual(tc.pasal17(60000000)[0], 3000000)
        self.assertEqual(tc.pasal17(250000000)[0], 31500000)
        self.assertEqual(tc.pasal17(500000000)[0], 94000000)
        self.assertEqual(tc.pasal17(5000000000)[0], 1444000000)
        self.assertEqual(tc.pasal17(6000000000)[0], 1794000000)
        self.assertEqual(tc.pasal17(0)[0], 0)

    def test_pkp_dibulatkan_ribuan(self):
        self.assertEqual(tc.bulat_ribuan_bawah(D("54300999.99")), 54300000)
        self.assertEqual(tc.bulat_ribuan_bawah(D("-5")), 0)


class TestContohResmi(unittest.TestCase):
    def test_pp58_penjelasan(self):
        h = jalankan("bulan", "--ptkp", "K/0", "--bruto", "Rp 10.000.000")
        self.assertEqual((h["tarif_ter_persen"], h["pph21"]), (2, 200000))
        h = jalankan("setahun", "--ptkp", "K/0", "--gaji", "10jt", "--iuran", "100rb")
        self.assertEqual(h["masa_terakhir"]["pkp"], 54300000)
        self.assertEqual(h["masa_terakhir"]["pph_terutang"], 2715000)
        self.assertEqual(h["masa_terakhir"]["pph_masa_terakhir"], 515000)

    def test_pmk168_tarif(self):
        self.assertEqual(jalankan("bulan", "--ptkp", "TK/0", "--bruto", "15,5jt")["tarif_ter_persen"], 7)
        self.assertEqual(jalankan("bulan", "--ptkp", "TK/0", "--bruto", "15,5jt")["pph21"], 1085000)
        self.assertEqual(jalankan("bulan", "--ptkp", "TK/0", "--bruto", "17.500.000")["pph21"], 1400000)
        self.assertEqual(jalankan("bulan", "--ptkp", "TK/0", "--bruto", "22.500.000")["pph21"], 2025000)

    def test_pmk168_tuan_a_setahun(self):
        bruto = [30080000, 35080000, 30080000, 30080000, 35080000, 30080000, 50080000, 30080000, 30080000,
                 30080000, 30080000, 90080000]
        pph_resmi = [3910400, 4911200, 3910400, 3910400, 4911200, 3910400, 9014400, 3910400, 3910400, 3910400,
                     3910400]
        path = tulis_csv([[i + 1, b, 100000, 200000] for i, b in enumerate(bruto)],
                         ["bulan", "bruto", "iuran_pensiun", "zakat"])
        try:
            h = jalankan("setahun", "--ptkp", "K/0", "--data", path)
        finally:
            os.unlink(path)
        self.assertEqual([r["pph21"] for r in h["bulan"][:11]], pph_resmi)
        mt = h["masa_terakhir"]
        self.assertEqual(mt["neto"], 441360000)
        self.assertEqual(mt["pkp"], 382860000)
        self.assertEqual(mt["pph_terutang"], 64715000)
        self.assertEqual(mt["pph_sudah_dipotong"], 50120000)
        self.assertEqual(mt["pph_masa_terakhir"], 14595000)

    def test_pmk168_tuan_b_mulai_september(self):
        h = jalankan("setahun", "--ptkp", "TK/0", "--gaji", "15,5jt", "--iuran", "100rb", "--mulai", "9")
        mt = h["masa_terakhir"]
        self.assertEqual(mt["biaya_jabatan"], 2000000)
        self.assertEqual(mt["pph_terutang"], 280000)
        self.assertEqual(mt["pph_masa_terakhir"], -2975000)
        self.assertEqual(h["ringkasan"]["kelebihan_dikembalikan"], 2975000)

    def test_pmk168_tuan_c_disetahunkan(self):
        h = jalankan("setahun", "--ptkp", "TK/0", "--gaji", "15,5jt", "--zakat", "775rb", "--mulai", "9",
                     "--disetahunkan")
        mt = h["masa_terakhir"]
        self.assertEqual(mt["neto_disetahunkan"], 170700000)
        self.assertEqual(mt["pph_setahun_penuh"], 11505000)
        self.assertEqual(mt["pph_terutang"], 3835000)
        self.assertEqual(mt["pph_masa_terakhir"], 580000)

    def test_pmk168_tuan_d_berhenti(self):
        h = jalankan("setahun", "--ptkp", "TK/0", "--gaji", "17,5jt", "--iuran", "100rb", "--akhir", "8",
                     "--status", "berhenti")
        mt = h["masa_terakhir"]
        self.assertEqual(mt["biaya_jabatan"], 4000000)
        self.assertEqual(mt["pkp"], 81200000)
        self.assertEqual(mt["pph_terutang"], 6180000)
        self.assertEqual(mt["pph_masa_terakhir"], -3620000)

    def test_pmk168_tuan_d_pemberi_kerja_baru(self):
        h = jalankan("setahun", "--ptkp", "TK/0", "--gaji", "22,5jt", "--iuran", "100rb", "--mulai", "9")
        self.assertEqual(h["masa_terakhir"]["pph_terutang"], 1680000)
        self.assertEqual(h["masa_terakhir"]["pph_masa_terakhir"], -4395000)

    def test_pmk168_tuan_e_disetahunkan_berhenti(self):
        h = jalankan("setahun", "--ptkp", "TK/0", "--gaji", "17,5jt", "--akhir", "8", "--status", "berhenti",
                     "--disetahunkan")
        mt = h["masa_terakhir"]
        self.assertEqual(mt["pkp"], 150000000)
        self.assertEqual(mt["pph_setahun_penuh"], 16500000)
        self.assertEqual(mt["pph_terutang"], 11000000)
        self.assertEqual(mt["pph_masa_terakhir"], 1200000)

    def test_pmk168_pegawai_tidak_tetap(self):
        self.assertEqual(jalankan("harian", "--upah", "500rb", "--hari", "20")["pph_sehari"], 2500)   # Tuan K
        self.assertEqual(jalankan("harian", "--total", "4,5jt", "--hari", "10")["pph_total"], 0)     # Tuan L
        self.assertEqual(jalankan("harian", "--upah", "3jt", "--hari", "1")["pph_total"], 75000)     # Tuan M
        h = jalankan("harian", "--total", "15jt", "--hari", "5")                                   # Tuan Z
        self.assertEqual((h["pph_sehari"], h["pph_total"]), (75000, 375000))

    def test_pmk168_tuan_n_ptt_bulanan(self):
        bruto = [4, 7, 1, 7, 8, 6, 7, 8, 6, 9, 2, 8]
        resmi = [0, 87500, 0, 87500, 120000, 45000, 87500, 120000, 45000, 157500, 0, 120000]
        hasil = [jalankan("bulan", "--ptkp", "TK/0", "--bruto", "{}jt".format(b))["pph21"] for b in bruto]
        self.assertEqual(hasil, resmi)
        self.assertEqual(sum(hasil), 870000)

    def test_pmk105_dtp_tuan_a(self):
        h = jalankan("bulan", "--ptkp", "TK/0", "--bruto", "8jt")
        self.assertEqual((h["tarif_ter_persen"], h["pph21"]), (D("1.5"), 120000))

    def test_pmk105_dtp_tuan_b_k1(self):
        bruto = [15, 10, 15, 10, 10, 10, 10, 10, 10, 12, 12, 12]
        path = tulis_csv([[i + 1, "{}jt".format(b), "10jt" if i < 9 else "12jt"] for i, b in enumerate(bruto)],
                         ["bulan", "bruto", "bruto_tetap"])
        try:
            h = jalankan("setahun", "--ptkp", "K/1", "--data", path, "--dtp")
        finally:
            os.unlink(path)
        self.assertTrue(h["dtp"])
        self.assertEqual([r["pph21"] for r in h["bulan"][:11]],
                         [900000, 150000, 900000, 150000, 150000, 150000, 150000, 150000, 150000, 360000, 360000])
        self.assertEqual(h["masa_terakhir"]["pph_terutang"], 4050000)
        self.assertEqual(h["masa_terakhir"]["pph_masa_terakhir"], 480000)
        self.assertEqual(h["ringkasan"]["total_dtp_dibayar_tunai"], 4050000)

    def test_pmk105_dtp_tuan_c_lebih_tidak_dikembalikan(self):
        h = jalankan("setahun", "--ptkp", "TK/0", "--gaji", "9jt", "--mulai", "3", "--tambahan", "10=5jt", "--dtp")
        self.assertEqual(h["bulan"][0]["pph21"], 157500)
        self.assertEqual(h["bulan"][7]["pph21"], 840000)
        mt = h["masa_terakhir"]
        self.assertEqual(mt["biaya_jabatan"], 4750000)
        self.assertEqual(mt["pph_terutang"], 1812500)
        self.assertEqual(mt["pph_masa_terakhir"], -287500)
        self.assertEqual(h["ringkasan"]["kelebihan_dikembalikan"], 0)
        self.assertEqual(h["ringkasan"]["total_dtp_dibayar_tunai"], 2100000)

    def test_teks_catatan_premi_dan_ringkasan_dtp(self):
        # regresi uji independen (ringan): catatan premi JKK/JKM/BPJS Kes & dua angka DTP
        h = jalankan("setahun", "--ptkp", "TK/0", "--gaji", "9jt", "--mulai", "3", "--tambahan", "10=5jt", "--dtp")
        teks = pph21.teks_setahun(h)
        self.assertIn("premi JKK, JKM", teks)
        self.assertIn("ditanggung pemerintah", teks)
        self.assertIn("Rp 1.812.500", teks)      # terutang setahun (Lampiran B PMK 105 Tuan C)
        self.assertIn("Rp 2.100.000", teks)      # dibayar tunai
        self.assertIn("Rp 287.500", teks)        # selisih tidak dikembalikan

    def test_bulan_dtp_dibayar_tunai(self):
        # regresi uji OpenClaw 2026-10-01: konveksi TK/0 Rp6 jt, DTP -> diterima Rp6.045.000 (PMK 105/2025 Pasal 5)
        h = jalankan("bulan", "--ptkp", "TK/0", "--bruto", "6jt", "--dtp")
        self.assertTrue(h["dtp"])
        self.assertEqual(h["pph21"], 45000)
        self.assertEqual(h["pph21_dipotong_dari_gaji"], 0)
        self.assertEqual(h["pph21_dtp_dibayar_tunai"], 45000)
        self.assertEqual(h["diterima_pegawai"], 6045000)
        teks = pph21.teks_bulan(h)
        self.assertIn("Rp 6.045.000", teks)
        self.assertIn("WAJIB dibayar tunai", teks)

    def test_bulan_dtp_potongan_premi(self):
        h = jalankan("bulan", "--ptkp", "TK/0", "--bruto", "8jt", "--dtp", "--bruto-tetap", "7,8jt",
                     "--premi-perusahaan", "200rb", "--potongan-lain", "240rb")
        self.assertEqual(h["pph21_dtp_dibayar_tunai"], 120000)   # Lampiran B PMK 105 Tuan A: 1,5% x 8 jt
        self.assertEqual(h["diterima_pegawai"], 8000000 - 200000 - 240000 + 120000)
        self.assertEqual(h["peringatan"], [])

    def test_bulan_dtp_tidak_memenuhi(self):
        h = jalankan("bulan", "--ptkp", "TK/0", "--bruto", "11jt", "--dtp")
        self.assertFalse(h["dtp"])
        self.assertEqual(h["pph21_dipotong_dari_gaji"], 330000)
        self.assertEqual(h["diterima_pegawai"], 10670000)
        h = jalankan("bulan", "--ptkp", "TK/0", "--bruto", "6jt", "--dtp", "--tahun", "2027")
        self.assertFalse(h["dtp"])
        self.assertEqual(h["pph21_dipotong_dari_gaji"], 45000)
        h = jalankan("bulan", "--ptkp", "TK/0", "--bruto", "12jt", "--dtp", "--bruto-tetap", "9jt")
        self.assertTrue(h["dtp"])   # bonus bulan ini tidak menggugurkan syarat (dinilai dari bruto tetap Januari)

    def test_bulan_tanpa_dtp_tidak_berubah(self):
        h = jalankan("bulan", "--ptkp", "K/0", "--bruto", "10jt")
        self.assertFalse(h["dtp"])
        self.assertEqual((h["pph21"], h["pph21_dipotong_dari_gaji"], h["diterima_pegawai"]), (200000, 200000, 9800000))

    def test_bulan_premi_lebih_besar_ditolak(self):
        with self.assertRaises(pph21.InputError):
            jalankan("bulan", "--ptkp", "K/0", "--bruto", "1jt", "--premi-perusahaan", "2jt")

    def test_syarat_dtp_core(self):
        self.assertTrue(tc.cek_syarat_dtp(2026, D(10000000))[0])
        self.assertFalse(tc.cek_syarat_dtp(2026, D(10000001))[0])
        self.assertFalse(tc.cek_syarat_dtp(2027, D(5000000))[0])
        self.assertFalse(tc.cek_syarat_dtp(2026, None)[0])

    def test_dtp_tidak_memenuhi(self):
        h = jalankan("setahun", "--ptkp", "TK/0", "--gaji", "10.000.001", "--dtp")
        self.assertFalse(h["dtp"])
        self.assertTrue(any("Tidak memenuhi" in p for p in h["peringatan"]))


class TestInputRusak(unittest.TestCase):
    def cek_error(self, *argv):
        with self.assertRaises((pph21.InputError, ValueError)):
            jalankan(*argv)

    def test_ptkp_salah(self):
        self.cek_error("bulan", "--ptkp", "K/4", "--bruto", "10jt")
        self.cek_error("bulan", "--ptkp", "X/1", "--bruto", "10jt")

    def test_angka_salah(self):
        self.cek_error("bulan", "--ptkp", "K/0", "--bruto", "sepuluh juta")
        self.cek_error("bulan", "--ptkp", "K/0", "--bruto=-5jt")
        self.cek_error("bulan", "--ptkp", "K/0", "--bruto", "1,250,000.50")
        self.cek_error("bulan", "--ptkp", "K/0", "--bruto", "15.00.000")

    def test_rentang_bulan(self):
        self.cek_error("setahun", "--ptkp", "K/0", "--gaji", "5jt", "--mulai", "10", "--akhir", "3")
        self.cek_error("setahun", "--ptkp", "K/0", "--gaji", "5jt", "--tambahan", "13=1jt")
        self.cek_error("setahun", "--ptkp", "K/0", "--gaji", "5jt", "--akhir", "6", "--tambahan", "Des=1jt")

    def test_csv_bulan_ganda(self):
        path = tulis_csv([[1, "5jt"], [1, "6jt"]], ["bulan", "bruto"])
        try:
            self.cek_error("setahun", "--ptkp", "K/0", "--data", path)
        finally:
            os.unlink(path)

    def test_csv_tanpa_kolom_bulan(self):
        path = tulis_csv([["5jt"]], ["gaji"])
        try:
            self.cek_error("setahun", "--ptkp", "K/0", "--data", path)
        finally:
            os.unlink(path)

    def test_harian_argumen(self):
        self.cek_error("harian", "--upah", "100rb")
        self.cek_error("harian", "--upah", "100rb", "--total", "1jt", "--hari", "2")

    def test_exit_code_cli(self):
        r = subprocess.run([sys.executable, os.path.join(FOLDER, "pph21.py"), "bulan", "--ptkp", "K/9",
                            "--bruto", "1jt"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)
        self.assertIn("ERROR", r.stderr)
        r = subprocess.run([sys.executable, os.path.join(FOLDER, "pph21.py"), "bulan", "--ptkp", "K/0",
                            "--bruto", "10jt", "--format", "json"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)
        self.assertEqual(json.loads(r.stdout)["pph21"], 200000)


if __name__ == "__main__":
    unittest.main(verbosity=1)
