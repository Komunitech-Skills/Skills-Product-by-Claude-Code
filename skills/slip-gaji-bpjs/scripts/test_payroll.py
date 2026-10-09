#!/usr/bin/env python3
"""Uji otomatis payroll.py. Jalankan: python3 test_payroll.py"""
import csv
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal as D

FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, FOLDER)
import ter_core as tc  # noqa: E402
import payroll  # noqa: E402

SHA256_TABEL = "26edfe89bda74169a5280317da194cec3194e8c48c661a8e6860ff8b48d5da72"
SUMBER_REPO = os.path.normpath(os.path.join(FOLDER, "..", "..", "..", "research", "sources", "pph21-ter-tabel.json"))
CORE_SKILL1 = os.path.normpath(os.path.join(FOLDER, "..", "..", "pph21-ter", "scripts", "ter_core.py"))


def cfg(periode="2026-09", umk=None, jkk="0.24", hari_kerja="5", batas=None):
    tahun, bulan = map(int, periode.split("-"))
    return {"tahun": tahun, "bulan": bulan, "perusahaan": "PT Uji", "umk": tc.parse_angka(umk) if umk else None,
            "jkk": tc.parse_angka(jkk), "hari_kerja": hari_kerja, "batas_jp": payroll.batas_jp(periode, batas),
            "pemisah_csv": ";", "peringatan": []}


def orang(**kw):
    r = {"nama": "Uji", "ptkp": "TK/0", "gaji_pokok": "5jt"}
    r.update(kw)
    return r


class TestTabel(unittest.TestCase):
    def test_hash(self):
        with open(tc.FILE_TABEL, "rb") as f:
            self.assertEqual(hashlib.sha256(f.read()).hexdigest(), SHA256_TABEL)

    def test_sama_dengan_sumber(self):
        if not os.path.exists(SUMBER_REPO):
            self.skipTest("sumber riset tidak ada (paket pembeli)")
        with open(SUMBER_REPO, encoding="utf-8") as a, open(tc.FILE_TABEL, encoding="utf-8") as b:
            self.assertEqual(json.load(a), json.load(b))

    def test_core_identik_dengan_pph21_ter(self):
        if not os.path.exists(CORE_SKILL1):
            self.skipTest("skill pph21-ter tidak terpasang berdampingan")
        with open(CORE_SKILL1, "rb") as a, open(os.path.join(FOLDER, "ter_core.py"), "rb") as b:
            self.assertEqual(a.read(), b.read())

    def test_contoh_resmi_ter(self):
        self.assertEqual(tc.pph_ter_bulanan(D(10000000), "A")[0], 200000)   # PP 58/2023, K/0 -> 2%
        self.assertEqual(tc.pph_ter_bulanan(D(15500000), "A")[0], 1085000)  # PMK 168/2023 -> 7%


class TestHitung(unittest.TestCase):
    def test_kasus_normal_lembur(self):
        r = orang(nama="Budi", ptkp="K/1", gaji_pokok="Rp 5.000.000", tunjangan_tetap="500.000",
                  tunjangan_tidak_tetap="600.000", lembur_hari_kerja="2+3", lembur_hari_libur="8",
                  potongan_lain="100.000")
        h = payroll.hitung_karyawan(r, cfg(umk="5.396.761", jkk="0,54"))
        # upah sejam 5.500.000/173; jam setara 3,5 + 5,5 + 16 = 25
        self.assertEqual(h["pendapatan"]["Lembur"], tc.bulat_terdekat(D(5500000) / 173 * 25))
        self.assertEqual(h["pendapatan"]["Lembur"], 794798)
        self.assertEqual(h["iuran"]["kes_karyawan"], 55000)
        self.assertEqual(h["iuran"]["jht_karyawan"], 110000)
        self.assertEqual(h["iuran"]["jp_karyawan"], 55000)
        self.assertEqual(h["iuran"]["jkk"], 29700)
        self.assertEqual(h["pph_info"]["bruto"], 7160998)       # + JKK 29.700 + JKM 16.500 + BPJS Kes 4% 220.000
        self.assertEqual(h["pph_info"]["kategori"], "B")
        self.assertEqual(h["pph"], 53707)                        # 0,75% x 7.160.998
        self.assertEqual(h["take_home_pay"], 6521091)
        self.assertEqual(h["biaya_perusahaan"], 6894798 + 220000 + 203500 + 29700 + 16500 + 110000)

    def test_batas_bpjs_dan_jp(self):
        h = payroll.hitung_karyawan(orang(ptkp="K/3", gaji_pokok="15jt", tunjangan_tetap="3jt"), cfg())
        self.assertEqual(h["iuran"]["kes_karyawan"], 120000)     # batas Rp12 jt
        self.assertEqual(h["iuran"]["kes_perusahaan"], 480000)
        self.assertEqual(h["iuran"]["jht_karyawan"], 360000)     # JHT tanpa batas
        self.assertEqual(h["iuran"]["jp_karyawan"], 110863)      # 1% x 11.086.300
        self.assertEqual(h["iuran"]["jp_perusahaan"], 221726)
        self.assertEqual(h["pph_info"]["kategori"], "C")
        h = payroll.hitung_karyawan(orang(gaji_pokok="15jt"), cfg(periode="2026-02"))
        self.assertEqual(h["iuran"]["jp_karyawan"], 105474)      # 1% x 10.547.400 (s.d. Feb 2026)

    def test_tepat_batas_jp(self):
        h = payroll.hitung_karyawan(orang(gaji_pokok="11.086.300"), cfg())
        self.assertEqual(h["iuran"]["jp_karyawan"], 110863)
        h = payroll.hitung_karyawan(orang(gaji_pokok="12.000.000"), cfg())
        self.assertEqual(h["iuran"]["kes_karyawan"], 120000)

    def test_umk(self):
        h = payroll.hitung_karyawan(orang(gaji_pokok="4,8jt"), cfg(umk="5396761"))
        self.assertEqual(h["iuran"]["kes_karyawan"], 53968)      # dasar minimal UMK
        self.assertTrue(any("di bawah UMK" in p for p in h["peringatan"]))
        h = payroll.hitung_karyawan(orang(gaji_pokok="6jt"), cfg(umk="5396761"))
        self.assertFalse(any("UMK" in p for p in h["peringatan"]))

    def test_lembur_libur_6_hari(self):
        c = cfg(hari_kerja="6")
        h = payroll.hitung_karyawan(orang(gaji_pokok="1.730.000", lembur_hari_libur="11"), c)
        self.assertEqual(h["pendapatan"]["Lembur"], 10000 * 29)   # 7x2 + 3 + 3x4
        h = payroll.hitung_karyawan(orang(gaji_pokok="1.730.000", lembur_hari_libur="9p"), c)
        self.assertEqual(h["pendapatan"]["Lembur"], 10000 * 25)   # 5x2 + 3 + 3x4
        with self.assertRaises(payroll.InputError):
            payroll.hitung_karyawan(orang(gaji_pokok="1.730.000", lembur_hari_libur="12"), c)

    def test_lembur_libur_5_hari_dan_desimal(self):
        h = payroll.hitung_karyawan(orang(gaji_pokok="1.730.000", lembur_hari_libur="12"), cfg())
        self.assertEqual(h["pendapatan"]["Lembur"], 10000 * 31)   # 8x2 + 3 + 3x4
        h = payroll.hitung_karyawan(orang(gaji_pokok="1.730.000", lembur_hari_kerja="1,5"), cfg())
        self.assertEqual(h["pendapatan"]["Lembur"], 10000 * D("2.5"))
        h = payroll.hitung_karyawan(orang(gaji_pokok="1.730.000", lembur_hari_kerja="5"), cfg())
        self.assertTrue(any("4 jam" in p for p in h["peringatan"]))

    def test_lembur_aturan_75_persen(self):
        h = payroll.hitung_karyawan(orang(gaji_pokok="3jt", tunjangan_tidak_tetap="2jt", lembur_hari_kerja="1"), cfg())
        self.assertEqual(h["lembur"]["dasar_upah"], D("3750000"))

    def test_desember_wajib_data_ytd(self):
        with self.assertRaises(payroll.InputError):
            payroll.hitung_karyawan(orang(gaji_pokok="10jt"), cfg(periode="2026-12"))

    def test_desember_hitung_ulang(self):
        # K/0 gaji 10 jt, BPJS TK saja (JKK 0,24% = 24.000, JKM 30.000) -> bruto pajak 10.054.000 -> TER A 2,25%
        c = cfg()
        h = payroll.hitung_karyawan(orang(ptkp="K/0", gaji_pokok="10jt", ikut_bpjs_kesehatan="tidak"), c)
        self.assertEqual(h["pph_info"]["bruto"], 10054000)
        self.assertEqual(h["pph"], 226215)
        r = orang(ptkp="K/0", gaji_pokok="10jt", ikut_bpjs_kesehatan="tidak", bruto_sd_bulan_lalu=str(11 * 10054000),
                  pph21_sd_bulan_lalu=str(11 * 226215), iuran_sd_bulan_lalu=str(11 * 300000), bulan_mulai="1")
        h = payroll.hitung_karyawan(r, cfg(periode="2026-12"))
        d = h["pph_info"]["detail"]
        self.assertEqual(d["neto"], 120648000 - 6000000 - 3600000)
        self.assertEqual(d["pkp"], 52548000)
        self.assertEqual(d["pph_terutang"], 2627400)
        self.assertEqual(h["pph"], 2627400 - 11 * 226215)

    def test_desember_wajib_jumlah_bulan(self):
        r = orang(gaji_pokok="20jt", bruto_sd_bulan_lalu="62jt", pph21_sd_bulan_lalu="3jt", iuran_sd_bulan_lalu="900rb")
        with self.assertRaises(payroll.InputError):
            payroll.hitung_karyawan(r, cfg(periode="2026-12"))

    def test_desember_masuk_september(self):
        # regresi uji independen: masuk September -> 4 bulan -> biaya jabatan maks 4 x Rp500.000
        base = dict(gaji_pokok="20jt", ikut_bpjs_kesehatan="tidak", ikut_bpjs_tk="tidak",
                    bruto_sd_bulan_lalu="60jt", pph21_sd_bulan_lalu="0")
        h1 = payroll.hitung_karyawan(orang(bulan_mulai="9", **base), cfg(periode="2026-12"))
        h2 = payroll.hitung_karyawan(orang(jumlah_bulan_kerja="4", **base), cfg(periode="2026-12"))
        d = h1["pph_info"]["detail"]
        self.assertEqual(d["biaya_jabatan"], 2000000)
        self.assertEqual(h1["pph"], h2["pph"])
        # 80 jt - 2 jt = 78 jt; PKP 24 jt; 5% = 1.200.000
        self.assertEqual(d["pkp"], 24000000)
        self.assertEqual(h1["pph"], 1200000)
        with self.assertRaises(payroll.InputError):
            payroll.hitung_karyawan(orang(bulan_mulai="13", **base), cfg(periode="2026-12"))

    def test_dtp_ditolak_gaji_di_atas_10jt(self):
        # regresi uji independen: gaji 15 jt + dtp=ya -> bukan DTP
        h = payroll.hitung_karyawan(orang(gaji_pokok="15jt", dtp="ya"), cfg())
        self.assertFalse(h["dtp"])
        self.assertEqual(h["pendapatan"]["PPh 21 DTP dibayar tunai"], 0)
        self.assertEqual(h["pph_disetor"], h["pph"])
        self.assertTrue(any("TIDAK memenuhi syarat" in p for p in h["peringatan"]))

    def test_dtp_dipotong_lalu_dibayar_tunai(self):
        # PMK 105/2025 Pasal 2 ayat 1, Pasal 5, Lampiran B (penilai gelombang 7, 2026-10-05): PPh dipotong, DTP tunai
        # dengan nilai sama -> take home pay sama dengan tanpa pajak; setoran ke negara Rp 0 (bukan gaji + DTP)
        dtp = payroll.hitung_karyawan(orang(gaji_pokok="6jt", dtp="ya", ikut_jp="tidak"), cfg())
        biasa = payroll.hitung_karyawan(orang(gaji_pokok="6jt", ikut_jp="tidak"), cfg())
        self.assertTrue(dtp["dtp"])
        pph = dtp["pph"]
        self.assertGreater(pph, 0)
        self.assertEqual(dtp["potongan"]["PPh 21"], pph)
        self.assertEqual(dtp["pendapatan"]["PPh 21 DTP dibayar tunai"], pph)
        self.assertEqual(dtp["pph_disetor"], 0)
        self.assertEqual(dtp["take_home_pay"], biasa["take_home_pay"] + pph)
        iuran_karyawan = dtp["iuran"]["kes_karyawan"] + dtp["iuran"]["jht_karyawan"] + dtp["iuran"]["jp_karyawan"]
        self.assertEqual(dtp["take_home_pay"], 6000000 - iuran_karyawan)
        teks = payroll.slip_md(dtp, cfg()) + payroll.slip_html(dtp, cfg())
        self.assertIn("tetap dipotong", teks)
        self.assertIn("Setoran PPh 21 ke negara untuk karyawan ini: Rp 0", teks)

    def test_dtp_pakai_bruto_januari(self):
        h = payroll.hitung_karyawan(orang(gaji_pokok="12jt", dtp="ya", bruto_tetap_januari="9jt"), cfg())
        self.assertTrue(h["dtp"])
        h = payroll.hitung_karyawan(orang(gaji_pokok="8jt", dtp="ya", bruto_tetap_januari="10.000.001"), cfg())
        self.assertFalse(h["dtp"])
        h = payroll.hitung_karyawan(orang(gaji_pokok="8jt", dtp="ya", bruto_tetap_januari="10jt"), cfg())
        self.assertTrue(h["dtp"])                                  # tepat Rp10 jt masih memenuhi

    def test_dtp_ditolak_bukan_2026(self):
        h = payroll.hitung_karyawan(orang(gaji_pokok="8jt", dtp="ya"), cfg(periode="2027-01"))
        self.assertFalse(h["dtp"])

    def test_lebih_potong_dikembalikan(self):
        r = orang(gaji_pokok="5jt", berhenti="ya", bruto_sd_bulan_lalu="20jt", pph21_sd_bulan_lalu="500rb",
                  jumlah_bulan_kerja="4", iuran_sd_bulan_lalu="450rb")
        h = payroll.hitung_karyawan(r, cfg())
        self.assertLess(h["pph"], 0)
        self.assertEqual(h["pendapatan"]["Pengembalian kelebihan PPh 21"], -h["pph"])
        self.assertEqual(h["potongan"]["PPh 21"], 0)

    def test_dtp(self):
        h = payroll.hitung_karyawan(orang(gaji_pokok="8jt", ikut_bpjs_kesehatan="tidak", ikut_bpjs_tk="tidak",
                                          dtp="ya"), cfg())
        self.assertEqual(h["pph"], 120000)                        # PMK 105/2025 contoh: 1,5% x 8 jt
        self.assertEqual(h["pendapatan"]["PPh 21 DTP dibayar tunai"], 120000)
        self.assertEqual(h["take_home_pay"], 8000000)
        self.assertEqual(h["pph_disetor"], 0)


class TestInputRusak(unittest.TestCase):
    def cek(self, r, c=None):
        with self.assertRaises((payroll.InputError, ValueError)):
            payroll.hitung_karyawan(r, c or cfg())

    def test_rusak(self):
        self.cek(orang(ptkp="K/5"))
        self.cek(orang(gaji_pokok="lima juta"))
        self.cek(orang(gaji_pokok="0"))
        self.cek(orang(lembur_hari_kerja="dua"))
        self.cek(orang(lembur_hari_kerja="2", lembur_rp="100rb"))
        self.cek(orang(dtp="mungkin"))
        self.cek(orang(nama=""))
        self.cek(orang(lembur_hari_libur="5p"))                   # 'p' hanya pola 6 hari

    def test_batas_jp_tidak_diketahui(self):
        with self.assertRaises(payroll.InputError):
            payroll.batas_jp("2027-06", None)
        self.assertEqual(payroll.batas_jp("2027-06", "11.600.000"), 11600000)

    def test_cli(self):
        tmp = tempfile.mkdtemp()
        try:
            path = os.path.join(tmp, "k.csv")
            with open(path, "w", newline="", encoding="utf-8") as f:
                w = csv.writer(f, delimiter=";")
                w.writerow(["Nama", "PTKP", "Gaji Pokok", "Jabatan"])
                w.writerow(["<script>Ani</script>", "TK/0", "Rp 6.000.000", "Kasir"])
            out = os.path.join(tmp, "out")
            r = subprocess.run([sys.executable, os.path.join(FOLDER, "payroll.py"), "--data", path, "--periode",
                                "2026-09", "--out", out, "--format", "json"], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            data = json.loads(r.stdout)
            self.assertEqual(len(data["karyawan"]), 1)
            with open(os.path.join(out, "slip-gaji-2026-09.html"), encoding="utf-8") as f:
                isi = f.read()
            self.assertNotIn("<script>Ani", isi)
            self.assertIn("&lt;script&gt;Ani", isi)
            self.assertTrue(os.path.exists(os.path.join(out, "rekap-payroll-2026-09.csv")))
            # input rusak: exit 2, tidak ada file dibuat
            with open(path, "a", newline="", encoding="utf-8") as f:
                csv.writer(f, delimiter=";").writerow(["Budi", "K/9", "5jt", ""])
            out2 = os.path.join(tmp, "out2")
            r = subprocess.run([sys.executable, os.path.join(FOLDER, "payroll.py"), "--data", path, "--periode",
                                "2026-09", "--out", out2], capture_output=True, text=True)
            self.assertEqual(r.returncode, 2)
            self.assertIn("Budi", r.stderr)
            self.assertFalse(os.path.exists(out2))
            r = subprocess.run([sys.executable, os.path.join(FOLDER, "payroll.py"), "--data", path, "--periode",
                                "2026-13"], capture_output=True, text=True)
            self.assertEqual(r.returncode, 2)
        finally:
            shutil.rmtree(tmp)


def _tulis_data(tmp):
    path = os.path.join(tmp, "k.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["Nama", "PTKP", "Gaji Pokok", "Jabatan"])
        w.writerow(["Ani", "TK/0", "Rp 6.000.000", "Kasir"])
    return path


class TestPeringatanTemp(unittest.TestCase):
    def test_fungsi(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertTrue(payroll.peringatan_folder_sementara(os.path.join(tmp, "x")))
        self.assertFalse(payroll.peringatan_folder_sementara(os.path.expanduser("~")))

    def test_cli_tetap_menulis_dan_memperingatkan(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = subprocess.run([sys.executable, os.path.join(FOLDER, "payroll.py"), "--data", _tulis_data(tmp), "--periode", "2026-09", "--out", os.path.join(tmp, "o")], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertIn("PERINGATAN", r.stderr)
            self.assertIn("folder sementara", r.stderr)
            self.assertTrue(os.path.exists(os.path.join(tmp, "o", "rekap-payroll-2026-09.csv")))


class TestTotalBiayaPerusahaan(unittest.TestCase):
    """Pembanding independen (aritmetika bulat sendiri, tanpa fungsi payroll) untuk kasus uji gabungan 2026-10-03:
    4 karyawan Oktober 2026, JKK 0,24%. Jawaban salah yang pernah muncul: Rp27.798.120 (iuran karyawan dikurangkan)."""
    DATA = [  # nama, ptkp, pokok, tunjangan tetap, tunjangan tidak tetap
        ("Yohanes", "TK/0", 4500000, 500000, 0), ("Maria", "K/1", 6000000, 750000, 525000),
        ("Daniel", "TK/0", 3800000, 0, 660000), ("Ester", "K/2", 8500000, 1000000, 0)]

    def pembanding(self):
        kotor = iuran = 0
        for _, _, pokok, tetap, tidak_tetap in self.DATA:
            dasar = pokok + tetap  # semua di bawah batas BPJS Kes (12 jt) & JP
            kotor += pokok + tetap + tidak_tetap
            # persen dalam basis 10.000 (4% = 400; 3,7% = 370; 2% = 200; 0,24% = 24; 0,3% = 30), bulat terdekat
            iuran += sum((dasar * b + 5000) // 10000 for b in (400, 370, 200, 24, 30))
        return kotor, iuran, kotor + iuran

    def test_angka(self):
        kotor, iuran, biaya = self.pembanding()
        self.assertEqual((kotor, iuran, biaya), (26235000, 2565120, 28800120))
        c = cfg("2026-10")
        hasil = [payroll.hitung_karyawan({"nama": n, "ptkp": p, "gaji_pokok": str(a), "tunjangan_tetap": str(b),
                                          "tunjangan_tidak_tetap": str(t)}, c) for n, p, a, b, t in self.DATA]
        total = payroll.total_rekap(hasil)
        self.assertEqual(total["penghasilan"], D(kotor))
        self.assertEqual(total["iuran_perusahaan"], D(iuran))
        self.assertEqual(total["biaya_perusahaan"], D(biaya))
        baris = payroll.baris_biaya_perusahaan(total)
        self.assertIn("Total biaya gaji perusahaan", baris)
        self.assertIn("Rp 26.235.000", baris)
        self.assertIn("Rp 2.565.120", baris)
        self.assertIn("Rp 28.800.120", baris)
        self.assertNotIn("27.798.120", baris)
        teks = payroll.ringkasan_teks(hasil, c, {"csv": "x.csv"}, total)
        self.assertIn(baris, teks)


if __name__ == "__main__":
    unittest.main(verbosity=1)
