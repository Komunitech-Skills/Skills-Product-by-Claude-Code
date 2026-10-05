#!/usr/bin/env python3
"""Uji rapikan.py. Jalankan: python3 tests/uji_rapikan.py  (hanya library standar)."""
import csv
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest

AKAR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(AKAR, "scripts", "rapikan.py")
CONTOH = os.path.join(AKAR, "examples", "data-contoh.csv")

spec = importlib.util.spec_from_file_location("rapikan", SCRIPT)
R = importlib.util.module_from_spec(spec)
spec.loader.exec_module(R)


def jalankan(isi, *arg, nama="data.csv", biner=False, enc="utf-8"):
    """Tulis isi ke berkas sementara, jalankan script, kembalikan (proses, laporan, baris-bersih)."""
    with tempfile.TemporaryDirectory() as d:
        path = os.path.join(d, nama)
        with open(path, "wb") as f:
            f.write(isi if biner else isi.encode(enc))
        keluar = os.path.join(d, "out")
        p = subprocess.run([sys.executable, SCRIPT, path, "--keluar", keluar] + list(arg),
                           capture_output=True, text=True, encoding="utf-8")
        lap = baris = None
        if p.returncode == 0:
            with open(os.path.join(keluar, "laporan.json"), encoding="utf-8") as f:
                lap = json.load(f)
            with open(os.path.join(keluar, lap["file_bersih"]), encoding="utf-8-sig", newline="") as f:
                baris = list(csv.DictReader(f))
        return p, lap, baris


class UjiHP(unittest.TestCase):
    def test_variasi_format(self):
        sama = ["0812-3456-7890", "+62 812 3456 7890", "6281234567890", "81234567890", "0812 3456 7890.0",
                "+62 (0) 812-3456-7890", "0062 812 3456 7890", "(0812) 3456 7890", "wa 0812 3456 7890"]
        for v in sama:
            self.assertEqual(R.normalisasi_hp(v)[0], "6281234567890", v)

    def test_gagal_dengan_alasan(self):
        for v, kata in [("6.28123E+11", "ilmiah"), ("0812-ABC-5555", "huruf"), ("0812345", "panjang"),
                        ("+1 202 555 0143", "luar negeri"), ("0812345678901234", "panjang"), ("---", "angka")]:
            hasil, _, alasan = R.normalisasi_hp(v)
            self.assertIsNone(hasil, v)
            self.assertIn(kata, alasan, v)

    def test_banyak_nomor_dan_telepon_tetap(self):
        h, cat, _ = R.normalisasi_hp("081234567890 / 085611112222")
        self.assertEqual(h, "6281234567890")
        self.assertIn("banyak_nomor", cat)
        h, cat, _ = R.normalisasi_hp("(021) 555-0123")
        self.assertEqual(h, "62215550123")
        self.assertIn("telepon_tetap", cat)


class UjiTanggal(unittest.TestCase):
    def iso(self, v, urutan="dmy"):
        return R.normalisasi_tanggal(v, urutan)[0]

    def test_format_campur(self):
        for v in ["5 Okt 2026", "05/10/2026", "2026-10-05", "2026-10-05 14:30:10", "5-Okt-26", "Okt 5, 2026",
                  "Senin, 5 Oktober 2026", "05.10.2026", "20261005", "46300", "5-10-26", "2026/10/05",
                  "Senin, 5 Okt 2026 pukul 14.30"]:
            self.assertEqual(self.iso(v), "2026-10-05", v)

    def test_ambigu_dan_urutan(self):
        iso, info = R.normalisasi_tanggal("03/04/2026", "dmy")
        self.assertEqual((iso, info["ambigu"]), ("2026-04-03", True))
        iso, info = R.normalisasi_tanggal("03/04/2026", "mdy")
        self.assertEqual((iso, info["ambigu"]), ("2026-03-04", True))
        iso, info = R.normalisasi_tanggal("05/05/2026")
        self.assertFalse(info["ambigu"])   # hari = bulan, tidak ambigu
        iso, info = R.normalisasi_tanggal("10/13/2026")
        self.assertEqual(iso, "2026-10-13")
        self.assertTrue(info["dibalik"])

    def test_tidak_valid(self):
        for v in ["31/02/2026", "abc", "32 Okt 2026", "0/0/2026", "5 Foo 2026", "2026-02-30"]:
            iso, info = R.normalisasi_tanggal(v)
            self.assertIsNone(iso, v)
            self.assertTrue(info["alasan"], v)

    def test_tentukan_urutan(self):
        self.assertEqual(R.tentukan_urutan(["10/13/2026", "01/02/2026"])[0], "mdy")
        self.assertEqual(R.tentukan_urutan(["13/10/2026", "01/02/2026"])[0], "dmy")
        urutan, warn = R.tentukan_urutan(["13/10/2026", "10/13/2026"])
        self.assertEqual(urutan, "dmy")
        self.assertTrue(warn)
        self.assertEqual(R.tentukan_urutan(["10/13/2026"], paksa="dmy")[0], "dmy")


class UjiRupiah(unittest.TestCase):
    def test_nilai(self):
        cocok = {"Rp 150.000": 150000, "150000": 150000, "150rb": 150000, "250 ribu": 250000, "1,5jt": 1500000,
                 "1.5jt": 1500000, "2jt": 2000000, "3 juta": 3000000, "Rp1.250.000,-": 1250000,
                 "Rp. 75.000": 75000, "68.500,00": 68500, "1,500,000": 1500000, "1.234.567,89": 1234568,
                 "(50.000)": -50000, "-50.000": -50000, "gratis": 0, "Rp 0": 0, "100k": 100000,
                 "1,234.50": 1235, "1.500": 1500}
        for v, e in cocok.items():
            self.assertEqual(R.normalisasi_rupiah(v)[0], e, v)

    def test_pembulatan_setengah_naik(self):
        n, info = R.normalisasi_rupiah("Rp 1.500,50")
        self.assertEqual(n, 1501)
        self.assertTrue(info["pembulatan"])
        self.assertEqual(R.normalisasi_rupiah("100,49")[0], 100)

    def test_ambigu_koma_tiga_digit(self):
        n, info = R.normalisasi_rupiah("1,500")
        self.assertEqual(n, 1500)
        self.assertTrue(info["ambigu"])

    def test_gagal(self):
        for v in ["abc", "12,34,56", "1.50.000", "Rp", "1..000", "12ab"]:
            n, info = R.normalisasi_rupiah(v)
            self.assertIsNone(n, v)
            self.assertTrue(info["alasan"])


class UjiNama(unittest.TestCase):
    def test_kapitalisasi(self):
        self.assertEqual(R.rapikan_nama("  BUDI   santoso "), "Budi Santoso")
        self.assertEqual(R.rapikan_nama("iPhone 15 pro"), "iPhone 15 Pro")   # huruf campur dibiarkan
        self.assertEqual(R.rapikan_nama("pt maju jaya"), "PT Maju Jaya")
        self.assertEqual(R.rapikan_nama("Beras 5kg"), "Beras 5kg")
        self.assertEqual(R.rapikan_nama("rizal bin ahmad"), "Rizal bin Ahmad")

    def test_kelompok(self):
        hitung = R.Counter({"Budi Santoso": 3, "Santoso Budi": 1, "Bpk. Budi Santoso": 1, "Budi Santosa": 1,
                            "Siti Aminah": 2, "Kopi 250ml": 1, "Kopi 500ml": 1, "Ani": 1, "Anis": 1,
                            "Muh. Rizal": 1, "Muhammad Rizal": 1})
        grup = R.kelompok_mirip(hitung, 0.86)
        himpunan = [frozenset(g[1]) for g in grup]
        self.assertIn(frozenset({"Budi Santoso", "Santoso Budi", "Bpk. Budi Santoso", "Budi Santosa"}), himpunan)
        self.assertIn(frozenset({"Muh. Rizal", "Muhammad Rizal"}), himpunan)
        semua = set().union(*himpunan)
        self.assertNotIn("Kopi 250ml", semua)   # beda angka = produk beda
        self.assertNotIn("Ani", semua)          # terlalu pendek untuk ditebak
        self.assertNotIn("Siti Aminah", semua)

    def test_usulan_nama_baku(self):
        hitung = R.Counter({"Budi Santoso": 3, "Bpk. Budi Santoso": 3, "Budi Santosa": 1})
        self.assertEqual(R.usulan_kanonik(list(hitung), hitung), "Budi Santoso")


class UjiDataContoh(unittest.TestCase):
    """Angka diverifikasi independen: dihitung tangan dari data-contoh.csv."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        p = subprocess.run([sys.executable, SCRIPT, CONTOH, "--keluar", cls.tmp.name],
                           capture_output=True, text=True, encoding="utf-8")
        assert p.returncode == 0, p.stderr
        cls.out = p.stdout
        with open(os.path.join(cls.tmp.name, "laporan.json"), encoding="utf-8") as f:
            cls.lap = json.load(f)
        with open(os.path.join(cls.tmp.name, "data-contoh-bersih.csv"), encoding="utf-8-sig", newline="") as f:
            cls.baris = list(csv.DictReader(f))

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_jumlah_baris_tidak_hilang(self):
        self.assertEqual(self.lap["jumlah_baris_data_isi"], 40)
        self.assertEqual(len(self.baris), 40)
        self.assertEqual(self.lap["jumlah_baris_keluar"], 40)

    def test_kolom_terdeteksi(self):
        d = self.lap["deteksi_kolom"]
        self.assertEqual(d["hp"]["kolom"], ["No HP"])
        self.assertEqual(d["tanggal"]["kolom"], ["Tanggal Order"])
        self.assertEqual(d["rupiah"]["kolom"], ["Total Bayar"])
        self.assertEqual(d["nama"]["kolom"], ["Nama Pelanggan", "Produk", "Kota"])

    def test_hp_budi_semua_sama(self):
        for no in ("1", "2", "3", "4", "5"):
            b = next(r for r in self.baris if r["No"] == no)
            self.assertEqual(b["No HP"], "6281234500101", no)

    def test_total_dihitung_tangan(self):
        harapan = {"1": "150000", "2": "150000", "3": "150000", "4": "1250000", "5": "75000", "6": "1200000",
                   "7": "1200000", "8": "2500000", "9": "2500000", "10": "45000", "11": "45000",
                   "14": "68500", "15": "68500", "16": "0", "23": "1501", "24": "", "27": "", "36": "3500000"}
        for no, e in harapan.items():
            b = next(r for r in self.baris if r["No"] == no)
            self.assertEqual(b["Total Bayar"], e, no)

    def test_tanggal(self):
        harapan = {"1": "2026-10-05", "3": "2026-10-07", "4": "2026-10-08", "7": "2026-10-05", "9": "2026-10-07",
                   "10": "2026-05-10", "39": "2026-11-01"}
        for no, e in harapan.items():
            b = next(r for r in self.baris if r["No"] == no)
            self.assertEqual(b["Tanggal Order"], e, no)

    def test_baris_rusak_dibiarkan_asli_dan_dicatat(self):
        b = next(r for r in self.baris if r["No"] == "16")
        self.assertEqual(b["Tanggal Order"], "31/02/2026")
        self.assertIn("kalender", b["_catatan"])
        b = next(r for r in self.baris if r["No"] == "18")
        self.assertEqual(b["No HP"], "6.28123E+11")
        gagal = {(g["baris"], g["kolom"]) for g in self.lap["tidak_bisa_diperbaiki"]}
        for pasangan in [(17, "Tanggal Order"), (18, "No HP"), (19, "No HP"), (20, "No HP"), (21, "No HP"),
                         (21, "Total Bayar"), (31, "(struktur)"), (32, "(struktur)"), (33, "(struktur)")]:
            self.assertIn(pasangan, gagal)
        self.assertEqual(len(self.lap["tidak_bisa_diperbaiki"]), 9)

    def test_duplikat_ditandai_bukan_dibuang(self):
        grup = [g["baris"] for g in self.lap["duplikat"]["persis"]]
        self.assertEqual(sorted(grup), [[13, 14], [15, 16]])
        self.assertTrue(next(r for r in self.baris if r["No"] == "12")["_grup_duplikat"].startswith("P"))

    def test_kelompok_nama(self):
        peta = {k["usulan_nama_baku"]: {i["nilai"] for i in k["isi"]} for k in self.lap["kelompok_nama_mirip"]}
        self.assertEqual(peta["Budi Santoso"], {"Budi Santoso", "Bpk. Budi Santoso", "Budi Santosa", "Santoso Budi"})
        self.assertEqual(peta["Muhammad Rizal Pratama"], {"Muh. Rizal Pratama", "Muhammad Rizal Pratama"})
        self.assertEqual(peta["Dewi Lestari"], {"Dewi Lestari", "Dewi Lestary"})
        self.assertEqual(peta["Yogyakarta"], {"Yogyakarta", "Jogja"})
        # tidak digabung tanpa izin
        self.assertEqual(next(r for r in self.baris if r["No"] == "5")["Nama Pelanggan"], "Santoso Budi")
        self.assertEqual(self.lap["perbaikan"]["nama_digabung_otomatis"], 0)

    def test_tanggal_ambigu_dilaporkan(self):
        self.assertEqual(len(self.lap["tanggal_ambigu"]), 8)

    def test_ringkasan_untuk_agent(self):
        self.assertIn("UNTUK AGENT SAJA", self.out)

    def test_idempoten(self):
        """Menjalankan ulang pada hasil bersih tidak mengubah apa pun."""
        with tempfile.TemporaryDirectory() as d:
            salinan = os.path.join(d, "bersih.csv")
            with open(os.path.join(self.tmp.name, "data-contoh-bersih.csv"), encoding="utf-8-sig", newline="") as f:
                baris = list(csv.reader(f))
            with open(salinan, "w", encoding="utf-8", newline="") as f:
                csv.writer(f).writerows([r[:7] for r in baris])
            p = subprocess.run([sys.executable, SCRIPT, salinan, "--keluar", os.path.join(d, "o"),
                                "--kolom-nama", "Nama Pelanggan|Produk|Kota", "--kolom-hp", "No HP",
                                "--kolom-tanggal", "Tanggal Order", "--kolom-rupiah", "Total Bayar"],
                               capture_output=True, text=True, encoding="utf-8")
            self.assertEqual(p.returncode, 0, p.stderr)
            with open(os.path.join(d, "o", "laporan.json"), encoding="utf-8") as f:
                lap = json.load(f)
            for k in ("hp_format", "tanggal_format", "rupiah_format", "nama_dirapikan"):
                self.assertEqual(lap["perbaikan"][k], 0, k)


class UjiDataRusak(unittest.TestCase):
    def test_gabung_dan_buang_duplikat(self):
        isi = "Nama,HP\nBudi Santoso,0812 1111 2222\nBudi Santosa,0812 1111 2222\nBudi Santoso,0812 1111 2222\n"
        _, lap, baris = jalankan(isi, "--buang-duplikat-persis")
        self.assertEqual(len(baris), 2)
        self.assertEqual(lap["file_dibuang_duplikat"], "dibuang-duplikat.csv")
        self.assertEqual(lap["baris_dibuang"][0]["baris"], 4)
        _, lap, baris = jalankan(isi, "--gabungkan-otomatis")
        self.assertEqual({r["Nama"] for r in baris}, {"Budi Santoso"})
        self.assertEqual(lap["perbaikan"]["nama_digabung_otomatis"], 1)

    def test_gabung_pilihan_dan_nama_baku(self):
        isi = ("Nama,HP\nBudi Santoso,0812 1111 2222\nBudi Santosa,0812 1111 2222\n"
               "Dewi Lestari,0812 3333 4444\nDewi Lestary,0812 3333 4444\n")
        _, lap, baris = jalankan(isi, "--gabung-kelompok", "1")
        nama = [r["Nama"] for r in baris]
        self.assertEqual(nama[0], nama[1])            # kelompok 1 digabung
        self.assertEqual(nama[2:], ["Dewi Lestari", "Dewi Lestary"])   # kelompok 2 dibiarkan
        _, lap, baris = jalankan(isi, "--nama-baku", "2=dewi lestary putri")
        self.assertEqual([r["Nama"] for r in baris][2:], ["Dewi Lestary Putri", "Dewi Lestary Putri"])
        self.assertEqual([r["Nama"] for r in baris][:2], ["Budi Santoso", "Budi Santosa"])
        p, _, _ = jalankan(isi, "--nama-baku", "ngawur")
        self.assertNotEqual(p.returncode, 0)

    def test_bom_titik_koma_cp1252(self):
        isi = "Nama;No HP;Total\nJosé Müller;0812 3333 4444;Rp 10.000\n"
        for enc in ("utf-8-sig", "cp1252"):
            p, lap, baris = jalankan(isi, enc=enc)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertEqual(lap["pemisah"], "titik koma")
            self.assertEqual(baris[0]["Nama"], "José Müller")
            self.assertEqual(baris[0]["No HP"], "6281233334444")
            self.assertEqual(baris[0]["Total"], "10000")

    def test_tab(self):
        _, lap, baris = jalankan("Nama\tHP\nAni Lestari\t081211112222\n")
        self.assertEqual(lap["pemisah"], "tab")
        self.assertEqual(baris[0]["HP"], "6281211112222")

    def test_berkas_kosong_biner_dan_tidak_ada(self):
        for isi in (b"", b"\n\n  \n"):
            p, _, _ = jalankan(isi, biner=True)
            self.assertEqual(p.returncode, 2)
            self.assertIn("GAGAL", p.stderr)
        p, _, _ = jalankan(b"PK\x03\x04\x00\x00binary\x00\x00", biner=True, nama="x.xlsx")
        self.assertEqual(p.returncode, 2)
        self.assertIn("CSV", p.stderr)
        q = subprocess.run([sys.executable, SCRIPT, "/tidak/ada.csv"], capture_output=True, text=True)
        self.assertEqual(q.returncode, 2)

    def test_hanya_judul(self):
        p, lap, baris = jalankan("Nama,HP,Tanggal\n")
        self.assertEqual(p.returncode, 0, p.stderr)
        self.assertEqual(lap["jumlah_baris_keluar"], 0)

    def test_baris_kosong_dan_judul_berulang_dicatat(self):
        isi = "Nama,HP\nAni,0812 1111 0000\n\nNama,HP\nBudi,0812 2222 0000\n"
        _, lap, baris = jalankan(isi)
        self.assertEqual(len(baris), 2)
        alasan = sorted(d["alasan"] for d in lap["baris_dibuang"])
        self.assertEqual(len(alasan), 2)
        self.assertTrue(any("kosong" in a for a in alasan))
        self.assertTrue(any("judul" in a for a in alasan))

    def test_kolom_tidak_ada(self):
        p, _, _ = jalankan("Nama,HP\nAni,0812 1111 0000\n", "--kolom-hp", "Telepon")
        self.assertEqual(p.returncode, 2)
        self.assertIn("tidak ditemukan", p.stderr)

    def test_urutan_tanggal_paksa_dan_bukti(self):
        isi = "Nama,Tanggal\nA,03/04/2026\nB,10/13/2026\n"
        _, lap, baris = jalankan(isi)
        self.assertEqual(baris[0]["Tanggal"], "2026-03-04")   # bukti 10/13 -> bulan/hari
        _, lap, baris = jalankan("Nama,Tanggal\nA,03/04/2026\n", "--urutan-tanggal", "mdy")
        self.assertEqual(baris[0]["Tanggal"], "2026-03-04")
        _, lap, baris = jalankan("Nama,Tanggal\nA,03/04/2026\n")
        self.assertEqual(baris[0]["Tanggal"], "2026-04-03")
        self.assertEqual(len(lap["tanggal_ambigu"]), 1)

    def test_daftar_hp_sama_ditandai(self):
        isi = "Nama,HP\nAni,0812 1111 0000\nAnita,0812-1111-0000\nBudi,0812 2222 0000\n"
        _, lap, baris = jalankan(isi, "--jenis", "daftar")
        self.assertEqual(len(lap["duplikat"]["nomor_hp_sama"]), 1)
        self.assertEqual(lap["duplikat"]["nomor_hp_sama"][0]["baris"], [2, 3])
        self.assertEqual(len(baris), 3)

    def test_transaksi_pelanggan_berulang_bukan_duplikat(self):
        isi = "Nama,HP,Tanggal,Total\nAni,0812 1111 0000,01/10/2026,10.000\nAni,0812 1111 0000,02/10/2026,20.000\n"
        _, lap, baris = jalankan(isi)
        self.assertEqual(lap["jenis_tabel"], "transaksi")
        self.assertEqual(lap["duplikat"]["persis"], [])
        self.assertEqual(lap["duplikat"]["nomor_hp_sama"], [])

    def test_hp_untuk_excel_dan_kolom_kosong(self):
        isi = "Nama,HP,Catatan\nAni,0812 1111 0000,\nBudi,0812 2222 0000,\n"
        _, lap, baris = jalankan(isi, "--hp-untuk-excel", "--buang-kolom-kosong")
        self.assertEqual(baris[0]["HP"], '="6281211110000"')
        self.assertNotIn("Catatan", baris[0])
        self.assertEqual(lap["kolom_kosong_semua"], ["Catatan"])

    def test_sel_berisi_koma_dengan_kutip_aman(self):
        isi = 'Nama,Alamat\n"Siti, S.Pd",Jl. Mawar 1\n'
        _, lap, baris = jalankan(isi)
        self.assertEqual(baris[0]["Nama"], "Siti, S.Pd")
        self.assertEqual(lap["tidak_bisa_diperbaiki"], [])

    def test_judul_kembar(self):
        _, lap, baris = jalankan("Nama,Nama\nAni,Budi\n")
        self.assertEqual(lap["kolom"], ["Nama", "Nama_2"])

    def test_data_asli_tidak_diubah(self):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "a.csv")
            isi = "Nama,HP\nANI,081211112222\n"
            with open(path, "w", encoding="utf-8") as f:
                f.write(isi)
            subprocess.run([sys.executable, SCRIPT, path], capture_output=True)
            with open(path, encoding="utf-8") as f:
                self.assertEqual(f.read(), isi)
            self.assertTrue(os.path.isfile(os.path.join(d, "hasil-rapikan", "a-bersih.csv")))


if __name__ == "__main__":
    unittest.main(verbosity=1)
