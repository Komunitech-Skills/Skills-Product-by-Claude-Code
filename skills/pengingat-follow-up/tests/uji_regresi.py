#!/usr/bin/env python3
"""Uji regresi cek_jatuh_tempo.py (unittest, library standar saja).

Jalankan dari folder skill:  python3 tests/uji_regresi.py      (Windows: python / py)
Semua data di sini FIKTIF. File dibuat di folder sementara lalu dihapus.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from datetime import date

DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(DIR, "..", "scripts")
SCRIPT = os.path.join(SCRIPTS, "cek_jatuh_tempo.py")
sys.path.insert(0, SCRIPTS)
import cek_jatuh_tempo as cj  # noqa: E402

ACUAN = date(2026, 10, 1)  # Kamis


class TestTanggal(unittest.TestCase):
    def t(self, teks, arah="depan"):
        return cj.parse_tanggal(teks, ACUAN, arah)[0]

    def test_format_lengkap(self):
        for teks in ("2026-10-03", "03-10-2026", "3/10/2026", "3.10.2026", "3/10/26", "3 Oktober 2026",
                     "3 okt 2026", "Sabtu, 3 Oktober 2026", "tgl 3 Okt 2026"):
            self.assertEqual(self.t(teks), date(2026, 10, 3), teks)

    def test_relatif(self):
        self.assertEqual(self.t("besok"), date(2026, 10, 2))
        self.assertEqual(self.t("lusa"), date(2026, 10, 3))
        self.assertEqual(self.t("hari ini"), ACUAN)
        self.assertEqual(self.t("3 hari lagi"), date(2026, 10, 4))
        self.assertEqual(self.t("+10"), date(2026, 10, 11))
        self.assertEqual(self.t("Jumat"), date(2026, 10, 2))
        self.assertEqual(self.t("Senin"), date(2026, 10, 5))

    def test_hari_sama_dianggap_minggu_depan_dengan_catatan(self):
        d, cat = cj.parse_tanggal("Kamis", ACUAN)
        self.assertEqual(d, date(2026, 10, 8))
        self.assertIn("Kamis depan", cat)

    def test_tahun_kabur_ke_depan_dengan_catatan(self):
        d, cat = cj.parse_tanggal("3/10", ACUAN)
        self.assertEqual(d, date(2026, 10, 3))
        self.assertIn("Tahun tidak disebut", cat)
        # Januari tanpa tahun saat Oktober -> tahun depan
        self.assertEqual(self.t("5 Jan"), date(2027, 1, 5))

    def test_tahun_kabur_baru_lewat_dianggap_terlambat(self):
        d, cat = cj.parse_tanggal("20 Sep", ACUAN)
        self.assertEqual(d, date(2026, 9, 20))
        self.assertIn("TERLAMBAT", cat)
        # lewat > 60 hari -> tahun depan
        self.assertEqual(self.t("1/7"), date(2027, 7, 1))

    def test_hari_saja(self):
        self.assertEqual(self.t("tgl 3"), date(2026, 10, 3))
        self.assertEqual(self.t("tanggal 1"), date(2026, 10, 1))
        # 31 saat Oktober ada; 31 dari 1 Nov -> 31 Des (Nov tidak punya 31)
        self.assertEqual(cj.parse_tanggal("31", date(2026, 11, 1))[0], date(2026, 12, 31))

    def test_29_februari(self):
        self.assertEqual(cj.parse_tanggal("29/2", date(2027, 3, 10))[0], date(2028, 2, 29))
        with self.assertRaises(cj.InputSalah):
            cj.parse_tanggal("29/2/2027", ACUAN)

    def test_tanggal_rusak(self):
        for teks in ("31/2/2026", "32/10", "3/13", "kapan-kapan", "", "2026-02-30"):
            with self.assertRaises(cj.InputSalah, msg=teks):
                cj.parse_tanggal(teks, ACUAN)


class TestAngka(unittest.TestCase):
    def test_nominal_format_indonesia(self):
        kasus = {"4,5 jt": 4500000, "4.500.000": 4500000, "Rp4.500.000": 4500000, "Rp 4.500.000,-": 4500000,
                 "750rb": 750000, "750 ribu": 750000, "1,2 M": 1200000000, "4 jt 500 rb": 4500000,
                 "4.5jt": 4500000, "12500000": 12500000, "Rp 1.250.000,50": 1250001, "150k": 150000}
        for teks, harap in kasus.items():
            self.assertEqual(cj.parse_nominal(teks)[0], harap, teks)
        self.assertEqual(cj.parse_nominal("")[0], None)

    def test_nominal_rusak(self):
        for teks in ("abc", "-500rb", "0", "1.500rb", "Rp"):
            with self.assertRaises(cj.InputSalah, msg=teks):
                cj.parse_nominal(teks)

    def test_jam(self):
        kasus = {"1:30": 90, "1,5": 90, "1.5": 90, "90m": 90, "90 menit": 90, "2 jam": 120, "1j30m": 90,
                 "1 jam 30 menit": 90, "2": 120, "0:45": 45, "1,25": 75}
        for teks, harap in kasus.items():
            self.assertEqual(cj.parse_jam(teks)[0], harap, teks)
        menit, cat = cj.parse_jam("1,33")
        self.assertEqual(menit, 80)
        self.assertIn("dibulatkan ke 80 menit", cat)

    def test_jam_rusak(self):
        for teks in ("abc", "1:75", "0", "25 jam", "-1", ""):
            with self.assertRaises(cj.InputSalah, msg=teks):
                cj.parse_jam(teks)

    def test_bulat_fraction_setengah_ke_atas(self):
        from fractions import Fraction
        self.assertEqual(cj.bulat(Fraction(5, 2)), 3)
        self.assertEqual(cj.bulat(Fraction(7, 3)), 2)
        self.assertEqual(cj.rupiah(1250000), "Rp 1.250.000")


class BasisCLI(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="uji-pengingat-")
        self.file = os.path.join(self.tmp, "pengingat", "DAFTAR.csv")
        self.ts = os.path.join(self.tmp, "pengingat", "timesheet.csv")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_cli(self, *arg, hari="2026-10-01"):
        p = subprocess.run([sys.executable, SCRIPT, "--file", self.file, "--timesheet-file", self.ts,
                            "--hari-ini", hari] + list(arg), capture_output=True, text=True, encoding="utf-8")
        data = json.loads(p.stdout) if p.returncode == 0 and p.stdout.strip().startswith("{") else None
        return p.returncode, data, p.stderr

    def tambah(self, jenis, nama, tgl, nominal=None, perihal=""):
        arg = ["tambah", "--jenis", jenis, "--nama", nama, "--tanggal", tgl, "--perihal", perihal]
        if nominal:
            arg += ["--nominal", nominal]
        kode, data, err = self.run_cli(*arg)
        self.assertEqual(kode, 0, err)
        return data


class TestCLI(BasisCLI):
    def test_rekap_kelompok_dan_total_bulat(self):
        self.tambah("piutang", "Bu Rina", "3/10", "4,5 jt", "INV-012")          # 2 hari lagi
        self.tambah("piutang", "CV Maju", "2026-09-21", "Rp12.500.000")         # lewat 10 hari
        self.tambah("piutang", "Toko Sinar", "hari ini", "750rb")               # hari ini
        self.tambah("prospek", "Pak Budi", "besok", perihal="penawaran katering")  # H-1
        self.tambah("piutang", "Bu Sari", "besok", "1.250.000")                 # H-1 piutang
        kode, r, err = self.run_cli("rekap")
        self.assertEqual(kode, 0, err)
        self.assertEqual([i["nama"] for i in r["terlambat"]], ["CV Maju"])
        self.assertEqual(r["terlambat"][0]["hari_terlambat"], 10)
        self.assertEqual([i["nama"] for i in r["jatuh_tempo_hari_ini"]], ["Toko Sinar"])
        self.assertEqual(sorted(i["nama"] for i in r["besok_h_1"]), ["Bu Sari", "Pak Budi"])
        self.assertEqual(r["ringkasan"]["total_tertunggak"], 13250000)
        self.assertIsInstance(r["ringkasan"]["total_tertunggak"], int)
        self.assertEqual(r["ringkasan"]["piutang_besok"], 1250000)
        self.assertEqual(r["ringkasan"]["total_tertunggak_teks"], "Rp 13.250.000")
        self.assertIn("Rp 12.500.000", r["terlambat"][0]["draf"])
        self.assertIn("DRAF PESAN", r["teks"])
        self.assertEqual(len(r["tujuh_hari_ke_depan"]), 1)

    def test_baris_rusak_tidak_crash(self):
        self.tambah("piutang", "Bu Rina", "hari ini", "4,5 jt")
        with open(self.file, "a", encoding="utf-8") as f:
            f.write("2,piutang,Rusak,31/2/2026,1jt,,aktif,,\n")
            f.write("3,piutang,Nominal Aneh,1/10/2026,abc,,aktif,,\n")
            f.write("4,,,,,,,,\n")
            f.write("5,piutang,Kebanyakan,1/10/2026,1,000,000,,aktif,,,,\n")
            f.write("6,piutang,Status Aneh,1/10/2026,1jt,,entahlah,,\n")
        kode, r, err = self.run_cli("rekap")
        self.assertEqual(kode, 0, err)
        self.assertEqual(len(r["jatuh_tempo_hari_ini"]), 1)
        self.assertEqual(sorted(x["baris"] for x in r["baris_ditolak"]), [3, 4, 5, 6, 7])
        self.assertIn("PERHATIAN", r["teks"])

    def test_file_belum_ada_dan_header_salah(self):
        kode, r, _ = self.run_cli("rekap")
        self.assertEqual(kode, 0)
        self.assertFalse(r["file_ada"])
        os.makedirs(os.path.dirname(self.file), exist_ok=True)
        with open(self.file, "w", encoding="utf-8") as f:
            f.write("a,b,c\n1,2,3\n")
        kode, r, err = self.run_cli("rekap")
        self.assertEqual(kode, 1)
        self.assertIn("kolom wajib", err)

    def test_csv_titik_koma_dan_bom_excel(self):
        os.makedirs(os.path.dirname(self.file), exist_ok=True)
        with open(self.file, "w", encoding="utf-8-sig") as f:
            f.write("id;jenis;nama;tanggal;nominal;perihal;status;catatan;dibuat\n"
                    "1;piutang;Bu Rina;01/10/2026;4.500.000;INV-1;aktif;;\n")
        kode, r, err = self.run_cli("rekap")
        self.assertEqual(kode, 0, err)
        self.assertEqual(r["ringkasan"]["total_tertunggak"], 4500000)

    def test_selesai_tunda_hapus(self):
        self.tambah("piutang", "Bu Rina", "hari ini", "4,5 jt")
        self.tambah("prospek", "Pak Budi", "hari ini")
        self.tambah("janji", "Bu Dewi", "hari ini")
        self.assertEqual(self.run_cli("selesai", "--id", "1")[0], 0)
        kode, d, err = self.run_cli("tunda", "--id", "2", "--ke", "Senin")
        self.assertEqual(kode, 0, err)
        self.assertEqual(self.run_cli("hapus", "--id", "3")[0], 0)
        kode, r, _ = self.run_cli("rekap")
        self.assertTrue(r["kosong"])
        kode, dft, _ = self.run_cli("daftar", "--semua")
        status = {i["id"]: (i["status"], i["tanggal"]) for i in dft["items"]}
        self.assertEqual(status, {"1": ("selesai", "2026-10-01"), "2": ("aktif", "2026-10-05")})
        kode, _, err = self.run_cli("hapus", "--id", "99")
        self.assertEqual(kode, 1)
        self.assertIn("tidak ada", err)

    def test_tolak_kontak_pribadi(self):
        kode, _, err = self.run_cli("tambah", "--jenis", "prospek", "--nama", "Pak Andi",
                                    "--catatan", "wa 0812-3456-7890", "--tanggal", "besok")
        self.assertEqual(kode, 2)
        self.assertIn("nomor HP", err)
        self.assertFalse(os.path.exists(self.file))
        kode, _, _ = self.run_cli("tambah", "--jenis", "prospek", "--nama", "x@contoh.com", "--tanggal", "besok")
        self.assertEqual(kode, 2)

    def test_jenis_dan_input_salah(self):
        kode, _, err = self.run_cli("tambah", "--jenis", "arisan", "--nama", "A", "--tanggal", "besok")
        self.assertEqual(kode, 1)
        self.assertIn("jenis", err)
        kode, _, err = self.run_cli("tambah", "--jenis", "piutang", "--nama", "A", "--tanggal", "31/2/2026")
        self.assertEqual(kode, 1)
        kode, _, err = self.run_cli("rekap", hari="bukan tanggal")
        self.assertEqual(kode, 1)

    def test_injeksi_rumus_excel_dinetralkan(self):
        self.tambah("lainnya", "=HYPERLINK(\"x\")", "besok")
        with open(self.file, encoding="utf-8") as f:
            isi = f.read()
        self.assertIn("'=HYPERLINK", isi)

    def test_draf_piutang_nada_bertahap(self):
        self.tambah("piutang", "A", "2026-09-28", "1jt")   # lewat 3 hari -> ramah
        self.tambah("piutang", "B", "2026-09-21", "1jt")   # lewat 10 hari -> minta tanggal pasti
        self.tambah("piutang", "C", "2026-08-20", "1jt")   # lewat 42 hari -> pemberitahuan tertulis
        kode, r, _ = self.run_cli("rekap")
        draf = {i["nama"]: i["draf"] for i in r["terlambat"]}
        self.assertIn("Mungkin terlewat", draf["A"])
        self.assertIn("tanggal pasti", draf["B"])
        self.assertIn("secara tertulis", draf["C"])
        for teks in draf.values():
            for kata in ("polisi", "pidana", "viral", "sebar"):
                self.assertNotIn(kata, teks.lower())

    def test_maks_draf_dan_draf_satu_item(self):
        for n in range(4):
            self.tambah("piutang", f"Pelanggan {chr(65 + n)}", "hari ini", "100rb")
        kode, r, _ = self.run_cli("rekap", "--maks-draf", "2")
        self.assertEqual(sum(1 for i in r["jatuh_tempo_hari_ini"] if i["draf"]), 2)
        self.assertIn("belum ditampilkan", r["teks"])
        kode, d, _ = self.run_cli("draf", "--id", "4")
        self.assertIn("Rp 100.000", d["draf"])

    def test_timesheet_total_dan_pembulatan(self):
        for klien, jam, tgl in (("PT Kreatif", "1:30", "2026-09-28"), ("PT Kreatif", "2,5", "2026-09-29"),
                                ("PT Kreatif", "20m", "2026-10-01"), ("CV Lestari", "1j10m", "2026-09-30"),
                                ("CV Lestari", "0:07", "2026-10-01"), ("CV Lestari", "2 jam", "2026-09-15")):
            tarif = "150rb" if klien == "PT Kreatif" else "Rp 175.000"
            kode, _, err = self.run_cli("catat-jam", "--klien", klien, "--jam", jam, "--tanggal", tgl, "--tarif", tarif)
            self.assertEqual(kode, 0, err)
        kode, r, err = self.run_cli("timesheet", "--periode", "minggu-ini")
        self.assertEqual(kode, 0, err)
        per = {d["klien"]: d for d in r["per_klien"]}
        self.assertEqual(per["PT Kreatif"]["total_menit"], 260)
        self.assertEqual(per["PT Kreatif"]["nilai"], 650000)
        # 77 menit x 175.000 / 60 = 224.583,33 -> Rp 224.583 (baris 15 Sep di luar periode)
        self.assertEqual(per["CV Lestari"]["total_menit"], 77)
        self.assertEqual(per["CV Lestari"]["nilai"], 224583)
        self.assertEqual(r["total_nilai"], 874583)
        kode, r, _ = self.run_cli("timesheet", "--periode", "bulan-lalu", "--klien", "cv lestari")
        # September: 70 + 120 = 190 menit x 175.000 / 60 = 554.166,67 -> Rp 554.167
        self.assertEqual(r["per_klien"][0]["nilai"], 554167)
        self.assertIn("DRAF PESAN KE KLIEN", r["teks"])

    def test_timesheet_baris_rusak_dan_tanpa_tarif(self):
        os.makedirs(os.path.dirname(self.ts), exist_ok=True)
        with open(self.ts, "w", encoding="utf-8") as f:
            f.write("tanggal,klien,jam,tarif_per_jam,keterangan\n"
                    "2026-10-01,PT A,1:00,,rapat\n"
                    "2026-10-01,PT A,abc,100000,\n"
                    "2026-09-31,PT A,1,100000,\n"
                    "2026-10-01,,1,100000,\n"
                    "2026-10-01,PT B,1:75,100000,\n")
        kode, r, err = self.run_cli("timesheet", "--periode", "bulan-ini")
        self.assertEqual(kode, 0, err)
        self.assertEqual([x["baris"] for x in r["baris_ditolak"]], [3, 4, 5, 6])
        self.assertIsNone(r["per_klien"][0]["nilai"])
        kode, r, _ = self.run_cli("timesheet", "--periode", "bulan-ini", "--tarif", "120rb")
        self.assertEqual(r["per_klien"][0]["nilai"], 120000)

    def test_timesheet_file_tidak_ada(self):
        kode, _, err = self.run_cli("timesheet")
        self.assertEqual(kode, 1)
        self.assertIn("belum ada", err)

    def test_output_teks(self):
        self.tambah("piutang", "Bu Rina", "hari ini", "4,5 jt")
        p = subprocess.run([sys.executable, SCRIPT, "--file", self.file, "--hari-ini", "2026-10-01", "rekap",
                            "--teks"], capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(p.returncode, 0)
        self.assertTrue(p.stdout.startswith("PENGINGAT FOLLOW-UP - Kamis, 1 Oktober 2026"))
        self.assertIn("Rp 4.500.000", p.stdout)


class TestRevisi101(unittest.TestCase):
    """Kasus dari uji independen v1.0.0 (examples/HASIL-UJI.md) -- regresi v1.0.1."""

    # BERAT 1
    def test_nominal_koma_ganjil_ditolak(self):
        for teks in ("4,5,6 jt", "1,500 jt", "1.500 jt", "1,250 rb", "4,5,6", "1.5.0", "1,2.3 jt"):
            with self.assertRaises(cj.InputSalah, msg=teks):
                cj.parse_nominal(teks)

    def test_nominal_besar_diberi_peringatan(self):
        n, cat = cj.parse_nominal("1,2 M")
        self.assertEqual(n, 1200000000)
        self.assertIn("1 miliar", cat)
        self.assertEqual(cj.parse_nominal("1 Miliar")[0], 10**9)
        self.assertIsNone(cj.parse_nominal("4,5 JT")[1])

    # SEDANG 6
    def test_m_kecil_ambigu_M_besar_miliar(self):
        for teks in ("750m", "5m", "5 m"):
            with self.assertRaises(cj.InputSalah, msg=teks):
                cj.parse_nominal(teks)
        self.assertEqual(cj.parse_nominal("2M")[0], 2 * 10**9)
        self.assertEqual(cj.parse_jam("90m")[0], 90)  # di jam, m = menit

    # BERAT 3
    def test_nama_hari_timesheet_ke_belakang(self):
        jumat = date(2026, 10, 2)
        self.assertEqual(cj.parse_tanggal("Senin", jumat, "lalu")[0], date(2026, 9, 28))
        self.assertEqual(cj.parse_tanggal("Kamis", jumat, "lalu")[0], date(2026, 10, 1))
        self.assertEqual(cj.parse_tanggal("Jumat", jumat, "lalu")[0], jumat)
        self.assertEqual(cj.parse_tanggal("Jumat lalu", jumat, "lalu")[0], date(2026, 9, 25))
        self.assertEqual(cj.parse_tanggal("Senin kemarin", jumat, "depan")[0], date(2026, 9, 28))
        self.assertEqual(cj.parse_tanggal("28/9", jumat, "lalu"), (date(2026, 9, 28), None))  # tanpa catatan tahun

    # SEDANG 5
    def test_jam_titik_dua_digit_ambigu(self):
        for teks in ("1.30", "2.15", "2.15 jam"):
            with self.assertRaises(cj.InputSalah, msg=teks):
                cj.parse_jam(teks)
        menit, cat = cj.parse_jam("1,30")
        self.assertEqual(menit, 78)
        self.assertIn("1:30", cat)

    # SEDANG 8
    def test_kontak_berbagai_format(self):
        for teks in ("+62 812 0000 1234", "+62-812-0000-1234", "0812.0000.1234", "62 812 0000 1234",
                     "0812 0000 1234", "081200001234"):
            self.assertIsNotNone(cj.cek_kontak({"perihal": teks}), teks)
        self.assertIsNone(cj.cek_kontak({"perihal": "INV-2026-0012 Rp 4.500.000"}))

    def test_status_dan_jenis_alias(self):
        self.assertEqual(cj.normal_status("LUNAS"), "selesai")
        self.assertEqual(cj.normal_status("sudah bayar"), "selesai")
        for j in ("hutang", "bon", "kasbon", "nota"):
            self.assertEqual(cj.normal_jenis(j), "piutang")

    def test_tahap_piutang_ikut_riwayat(self):
        self.assertEqual(cj.tahap_piutang(20, 0), 4)
        self.assertEqual(cj.tahap_piutang(20, 1), 5)
        self.assertEqual(cj.tahap_piutang(35, 0), 5)
        self.assertEqual(cj.tahap_piutang(35, 2), 6)
        self.assertEqual(cj.tahap_piutang(-1, 0), 1)


class TestRevisi101CLI(BasisCLI):
    def test_baris_rusak_tetap_tersimpan_setelah_tulis_ulang(self):
        self.tambah("piutang", "Bu Rina", "hari ini", "4,5 jt")
        with open(self.file, "a", encoding="utf-8") as f:
            f.write("2,piutang,Toko E,1/10/2026,1jt,kolom,ekstra,x,y,z,w\n")
            f.write("3,piutang,Toko F,31/2/2026,1jt,,aktif,,\n")
        with open(self.file, encoding="utf-8") as f:
            sebelum = f.read().splitlines()
        kode, d, err = self.run_cli("selesai", "--id", "1", "--teks")
        self.assertEqual(kode, 0, err)
        p = subprocess.run([sys.executable, SCRIPT, "--file", self.file, "--hari-ini", "2026-10-01", "selesai",
                            "--id", "1", "--teks"], capture_output=True, text=True, encoding="utf-8")
        self.assertIn("tetap disimpan", p.stdout)
        with open(self.file, encoding="utf-8") as f:
            sesudah = f.read().splitlines()
        self.assertEqual(len(sesudah), len(sebelum))
        self.assertEqual(sesudah[2], sebelum[2])  # posisi & isi baris rusak terjaga
        self.assertTrue(sesudah[3].startswith(sebelum[3]))  # baris sah: isi sama (+ kolom baru 'diingatkan')
        # tambah/ubah/hapus juga tidak menghilangkan baris rusak
        self.tambah("prospek", "Pak Budi", "besok")
        self.assertEqual(self.run_cli("ubah", "--id", "1", "--catatan", "cek")[0], 0)
        self.assertEqual(self.run_cli("hapus", "--id", "4")[0], 0)
        with open(self.file, encoding="utf-8") as f:
            isi = f.read()
        self.assertIn("Toko E", isi)
        self.assertIn("Toko F", isi)

    def test_catat_jam_nama_hari_dan_masa_depan(self):
        kode, d, err = self.run_cli("catat-jam", "--klien", "Batik Laras", "--jam", "4:30", "--tanggal", "Senin",
                                    "--tarif", "150rb", hari="2026-10-02")
        self.assertEqual(kode, 0, err)
        self.assertEqual(d["baris"]["tanggal"], "2026-09-28")
        for tgl in ("besok", "Senin depan", "3 Okt", "2026-10-05"):
            kode, _, err = self.run_cli("catat-jam", "--klien", "X", "--jam", "1", "--tanggal", tgl, hari="2026-10-02")
            self.assertEqual(kode, 1, tgl)
            self.assertIn("masa depan", err)
        kode, r, _ = self.run_cli("timesheet", "--periode", "minggu-ini", hari="2026-10-02")
        self.assertEqual(r["per_klien"][0]["nilai"], 675000)

    def test_draf_tidak_bilang_besok_untuk_item_jauh(self):
        self.tambah("piutang", "Bu Rina", "2026-10-10", "4,5 jt")
        self.tambah("janji", "Bu Dewi", "2026-10-03", perihal="meeting")
        self.tambah("piutang", "Pak Joko", "besok", "1jt")
        _, d1, _ = self.run_cli("draf", "--id", "1")
        self.assertNotIn("besok", d1["draf"])
        self.assertIn("pada 10 Okt 2026", d1["draf"])
        _, d2, _ = self.run_cli("draf", "--id", "2")
        self.assertIn("lusa", d2["draf"])
        self.assertNotIn("besok", d2["draf"])
        _, d3, _ = self.run_cli("draf", "--id", "3")
        self.assertIn("besok", d3["draf"])

    def test_csv_ansi_cp1252(self):
        os.makedirs(os.path.dirname(self.file), exist_ok=True)
        with open(self.file, "w", encoding="cp1252") as f:
            f.write("id,jenis,nama,tanggal,nominal,perihal,status,catatan,dibuat\n"
                    "1,piutang,Café Senja,2026-10-01,1500000,INV-1,aktif,,\n")
        kode, r, err = self.run_cli("rekap")
        self.assertEqual(kode, 0, err)
        self.assertEqual(r["jatuh_tempo_hari_ini"][0]["nama"], "Café Senja")
        self.assertTrue(any("ANSI" in p for p in r["peringatan"]))
        self.assertEqual(self.run_cli("selesai", "--id", "1")[0], 0)
        with open(self.file, encoding="utf-8") as f:
            self.assertIn("Café Senja", f.read())

    def test_kontak_spasi_ditolak_saat_tambah_dan_diperingatkan_saat_rekap(self):
        kode, _, err = self.run_cli("tambah", "--jenis", "piutang", "--nama", "Bu Rina", "--tanggal", "besok",
                                    "--perihal", "+62 812 0000 1234")
        self.assertEqual(kode, 2)
        os.makedirs(os.path.dirname(self.file), exist_ok=True)
        with open(self.file, "w", encoding="utf-8") as f:
            f.write("id,jenis,nama,tanggal,nominal,perihal,status,catatan,dibuat\n"
                    "1,piutang,Bu Rina,2026-10-01,1jt,,aktif,wa +62 812 0000 1234,\n")
        _, r, _ = self.run_cli("rekap")
        self.assertTrue(any("nomor HP" in p for p in r["peringatan"]))

    def test_rekap_ringan(self):
        self.tambah("prospek", "Pak Budi", "hari ini")
        self.tambah("janji", "Bu Dewi", "2026-10-05")
        _, r, _ = self.run_cli("rekap")
        self.assertNotIn("Total piutang", r["teks"])          # tanpa piutang -> baris total disembunyikan
        self.assertIn("#2 Bu Dewi", r["teks"])                  # nama item 7 hari ke depan
        self.tambah("piutang", "A", "2026-09-20", "1jt")       # 11 hari
        self.tambah("piutang", "B", "2026-08-10", "2jt")       # 52 hari
        self.tambah("piutang", "C", "2026-07-01", "3jt")       # 92 hari
        _, r, _ = self.run_cli("rekap")
        u = r["ringkasan"]["umur_piutang_terlambat"]
        self.assertEqual((u["1-30"]["nominal"], u["31-60"]["nominal"], u[">60"]["nominal"]), (1000000, 2000000, 3000000))
        self.assertIn("Umur piutang terlambat", r["teks"])

    def test_ubah_catatan_menambah_dan_status_lunas(self):
        self.tambah("piutang", "Bu Rina", "hari ini", "4,5 jt")
        self.run_cli("ubah", "--id", "1", "--catatan", "janji bayar Jumat")
        self.run_cli("ubah", "--id", "1", "--catatan", "transfer sebagian")
        _, d, _ = self.run_cli("daftar")
        self.assertEqual(d["items"][0]["catatan"], "janji bayar Jumat | transfer sebagian")
        kode, _, err = self.run_cli("ubah", "--id", "1", "--status", "lunas")
        self.assertEqual(kode, 0, err)
        _, d, _ = self.run_cli("daftar", "--semua")
        self.assertEqual(d["items"][0]["status"], "selesai")

    def test_terkirim_menaikkan_nada_dan_menjadwalkan_ulang(self):
        self.tambah("piutang", "CV Maju", "2026-09-11", "5jt")   # 20 hari
        _, d, _ = self.run_cli("draf", "--id", "1")
        self.assertIn("tanggal pasti", d["draf"])
        kode, t, err = self.run_cli("terkirim", "--id", "1")
        self.assertEqual(kode, 0, err)
        _, d, _ = self.run_cli("draf", "--id", "1")
        self.assertIn("secara tertulis", d["draf"])
        self.tambah("prospek", "Pak Budi", "hari ini", perihal="penawaran")
        draf = []
        for _ in range(4):
            draf.append(self.run_cli("draf", "--id", "2")[1]["draf"])
            kode, t, err = self.run_cli("terkirim", "--id", "2", "--berikutnya", "3 hari lagi")
            self.assertEqual(kode, 0, err)
        self.assertEqual(len(set(draf)), 4)                     # draf prospek berbeda tiap tahap
        self.assertIn("pesan terakhir", draf[3])
        _, dft, _ = self.run_cli("daftar")
        self.assertEqual([i["tanggal"] for i in dft["items"] if i["id"] == "2"], ["2026-10-04"])

    def test_rumus_excel_di_csv_lama_diamankan_saat_tulis_ulang(self):
        os.makedirs(os.path.dirname(self.file), exist_ok=True)
        with open(self.file, "w", encoding="utf-8") as f:
            f.write("id,jenis,nama,tanggal,nominal,perihal,status,catatan,dibuat\n"
                    "1,piutang,Bu Rina,2026-10-01,1jt,=HYPERLINK(1),aktif,@x,\n")
        self.assertEqual(self.run_cli("selesai", "--id", "1")[0], 0)
        with open(self.file, encoding="utf-8") as f:
            isi = f.read()
        self.assertIn("'=HYPERLINK", isi)
        self.assertIn("'@x", isi)


class TestRevisi102(BasisCLI):
    """Cacat ringan uji ulang v1.0.1 (R1-R4) -- regresi v1.0.2."""

    HEADER_LAMA = "id,jenis,nama,tanggal,nominal,perihal,status,catatan,dibuat\n"

    def tulis(self, isi):
        os.makedirs(os.path.dirname(self.file), exist_ok=True)
        with open(self.file, "w", encoding="utf-8") as f:
            f.write(isi)

    def test_r1_baris_berlebih_tidak_jatuh_ke_kolom_baru(self):
        self.tulis(self.HEADER_LAMA + "1,piutang,Bu Rina,2026-10-01,1jt,,aktif,,\n"
                   "2,piutang,Toko E,2026-10-01,1jt,,aktif,,,2\n")      # kelebihan berupa angka
        for _ in range(3):                                           # tulis ulang berkali-kali
            kode, d, err = self.run_cli("selesai", "--id", "1")
            self.assertEqual(kode, 0, err)
            kode, r, _ = self.run_cli("rekap")
            self.assertEqual([x["baris"] for x in r["baris_ditolak"]], [3])
            self.assertEqual(r["jatuh_tempo_hari_ini"], [])
            self.assertTrue(any("format lama" in p for p in r["peringatan"]))
        with open(self.file, encoding="utf-8") as f:
            self.assertEqual(f.readline(), self.HEADER_LAMA)        # header lama dipertahankan
        kode, _, err = self.run_cli("terkirim", "--id", "1")
        self.assertEqual(kode, 1)
        self.assertIn("format lama", err)

    def test_r1_migrasi_eksplisit_tanpa_baris_rusak(self):
        self.tulis(self.HEADER_LAMA + "1,piutang,Bu Rina,2026-10-01,1jt,INV-1,aktif,,\n")
        kode, d, err = self.run_cli("terkirim", "--id", "1")
        self.assertEqual(kode, 0, err)
        with open(self.file, encoding="utf-8") as f:
            baris = f.read().splitlines()
        self.assertEqual(baris[0], self.HEADER_LAMA.strip() + ",diingatkan")
        self.assertTrue(baris[1].endswith(",1"))
        p = subprocess.run([sys.executable, SCRIPT, "--file", self.file, "--hari-ini", "2026-10-01", "--teks",
                            "rekap"], capture_output=True, text=True, encoding="utf-8")
        self.assertIn("sudah diingatkan 1x", p.stdout)

    def test_r2_pesan_pamit_disarankan_selesai(self):
        self.tambah("prospek", "Pak Budi", "hari ini", perihal="penawaran")
        for _ in range(3):
            self.run_cli("terkirim", "--id", "1")
        _, d, _ = self.run_cli("draf", "--id", "1")
        self.assertIn("pesan terakhir", d["draf"])
        self.assertIn("selesai 1", d["saran"])
        self.assertNotIn("lanjut", d["saran"])

    def test_r3_kurung_dan_sensor_di_rekap(self):
        for teks in ("(0812) 0000-1234", "+62 (812) 0000 1234", "wa (0812)0000 1234"):
            self.assertIsNotNone(cj.cek_kontak({"perihal": teks}), teks)
        kode, _, _ = self.run_cli("tambah", "--jenis", "piutang", "--nama", "Bu Rina", "--tanggal", "besok",
                                  "--catatan", "(0812) 0000-1234")
        self.assertEqual(kode, 2)
        self.tulis("id,jenis,nama,tanggal,nominal,perihal,status,catatan,dibuat,diingatkan\n"
                   "1,piutang,Bu Rina,2026-10-01,1jt,INV-1 (0812) 0000-1234,aktif,email rina@contoh.com,,\n")
        _, r, _ = self.run_cli("rekap")
        self.assertNotIn("0000-1234", r["teks"])
        self.assertNotIn("rina@contoh.com", r["teks"])
        self.assertIn("0812-****-1234", r["teks"])
        self.assertNotIn("0000", r["jatuh_tempo_hari_ini"][0]["draf"])
        self.assertTrue(any("disamarkan" in p for p in r["peringatan"]))

    def test_r4_saran_jam_valid(self):
        for teks in ("1.60", "1:60", "1:75", "2.75"):
            with self.assertRaises(cj.InputSalah) as ctx:
                cj.parse_jam(teks)
            pesan = str(ctx.exception)
            self.assertNotIn("tulis 1:60", pesan)
            self.assertNotIn("tulis 1:75", pesan)
            self.assertNotIn("tulis 2:75", pesan)
        with self.assertRaises(cj.InputSalah) as ctx:
            cj.parse_jam("1.60")
        self.assertIn("2:00", str(ctx.exception))


if __name__ == "__main__":
    unittest.main(verbosity=1)
