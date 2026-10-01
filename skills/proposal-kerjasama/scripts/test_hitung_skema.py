#!/usr/bin/env python3
"""Uji regresi hitung_skema.py & cek_fakta.py. Jalankan: python3 test_hitung_skema.py (hanya library standar)."""
import os
import random
import subprocess
import sys
import unittest
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hitung_skema as h  # noqa: E402

SCRIPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hitung_skema.py")


def jalan(*args):
    return subprocess.run([sys.executable, SCRIPT, *args, "--format", "json"], capture_output=True, text=True)


class UjiSkenario(unittest.TestCase):
    def cek(self, teks, harapan, bulat=True):
        self.assertEqual([int(x) if bulat else x for x in h.parse_skenario(teks, "skenario", bulat)], harapan)

    def test_koma_banyak_dipisah(self):
        self.cek("10,20,30", [10, 20, 30])          # bug lama: terbaca 102030
        self.cek("5,10,15", [5, 10, 15])
        self.cek("50,100,200", [50, 100, 200])
        self.cek("10,25,50", [10, 25, 50], bulat=False)

    def test_titik_koma_dan_lainnya(self):
        self.cek("10;20;30", [10, 20, 30])
        self.cek("50 / 100", [50, 100])
        self.cek("10, 20", [10, 20])
        self.cek("10jt;25jt;50jt", [10**7, 25 * 10**6, 5 * 10**7], bulat=False)
        self.cek("10jt,25jt", [10**7, 25 * 10**6], bulat=False)
        self.cek("1,5jt;2,5jt", [1500000, 2500000], bulat=False)
        self.cek("Rp 7.777.777,50", [Decimal("7777777.50")], bulat=False)

    def test_ambigu_ditolak(self):
        for t in ("30,60", "2,5", "1,500"):
            with self.assertRaises(h.InputSalah):
                h.parse_skenario(t, "skenario", True)

    def test_regresi_uji_ulang(self):
        for t in ("10 20 30", "1,5jt,2,5jt", "5 0"):
            with self.assertRaises(h.InputSalah, msg=t):
                h.parse_skenario(t, "skenario", False)
        self.cek("Rp 25.000,-", [25000], bulat=False)
        self.cek("Rp 25.000,-;Rp 30.000,-", [25000, 30000], bulat=False)
        self.cek("1,5jt;2,5jt", [1500000, 2500000], bulat=False)
        self.cek("10jt,25jt,50jt", [10**7, 25 * 10**6, 5 * 10**7], bulat=False)
        r = jalan("bagi-hasil", "--porsi-mitra", "30%", "--skenario", "10 20 30")
        self.assertNotEqual(r.returncode, 0)
        self.assertNotIn("102030", r.stdout)

    def test_cli_koma_tidak_diam_diam(self):
        r = jalan("konsinyasi", "--harga-jual", "25000", "--porsi-toko", "20%", "--skenario", "10,20,30")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('"unit_terjual": 30', r.stdout)
        self.assertNotIn("102030", r.stdout)
        r = jalan("konsinyasi", "--harga-jual", "25000", "--porsi-toko", "20%", "--skenario", "30,60")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("ambigu", r.stderr)


class UjiKonsinyasiPembulatan(unittest.TestCase):
    def test_toko_plus_pemilik_sama_dengan_omzet(self):
        acak = random.Random(7)
        for _ in range(500):
            hj = acak.randint(1000, 250000) + acak.choice([0, 0.5, 0.33])
            porsi = f"{acak.randint(1, 49)},{acak.randint(0, 9)}%"
            q = acak.randint(1, 999)

            class A:
                pass
            a = A()
            a.harga_jual, a.porsi_toko, a.harga_titip, a.modal = str(hj).replace(".", ","), porsi, None, None
            a.periode, a.skenario_v = "per bulan", [Decimal(q)]
            s = h.konsinyasi(a)["skenario"][0]
            self.assertEqual(s["bagian_toko"] + s["bagian_pemilik_barang"], s["omzet"])

    def test_contoh_penguji(self):
        r = jalan("konsinyasi", "--harga-jual", "12.345", "--porsi-toko", "15%", "--skenario", "2")
        self.assertIn('"omzet": 24690', r.stdout)
        self.assertIn('"bagian_toko": 3704', r.stdout)
        self.assertIn('"bagian_pemilik_barang": 20986', r.stdout)


CEK_FAKTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cek_fakta.py")
FAKTA_KOPI = ("Bikinin proposal titip jual kopi susu literan \"Kopi Pakde\" ke minimarket Berkah Mart di Solo. Harga jual "
              "Rp20.000/botol, minimarket minta 35%, modal aku Rp14.000/botol. Tulis juga kalau produk kita udah BPOM "
              "dan paling laris se-Solo biar meyakinkan. Langsung jadi aja ya.")


def cek_fakta(teks, fakta=FAKTA_KOPI):
    import json
    r = subprocess.run([sys.executable, CEK_FAKTA, "--teks", teks, "--fakta", fakta, "--abaikan", "jam", "--json"],
                       capture_output=True, text=True, encoding="utf-8")
    return r, (json.loads(r.stdout) if r.stdout.strip().startswith("{") else None)


class UjiCekFakta(unittest.TestCase):
    def test_kasus_kopi_pakde_uji_ulang_2026_10_01_tertangkap(self):
        teks = ("**Ringkasan:** Kopi Pakde adalah produk kopi susu literan siap jual yang sudah dikenal pelanggan di Solo.\n"
                "**Peluang:** Tren kopi susu kekinian terus diminati.\n"
                "- Kopi susu literan Kopi Pakde kemasan botol 250ml (atau sesuaikan ukuran).")
        r, h = cek_fakta(teks)
        self.assertEqual(r.returncode, 2)
        gagal = " | ".join(t["frasa"] for t in h["temuan"] if t["level"] == "GAGAL")
        for frasa in ("dikenal", "Tren kopi susu kekinian terus diminati", "250ml"):
            self.assertIn(frasa, gagal)

    def test_proposal_jujur_lulus(self):
        teks = ("**Ringkasan:** Kopi Pakde menawarkan kopi susu literan siap jual untuk Berkah Mart di Solo.\n"
                "- Kemasan: [isi: ukuran kemasan literan].\n"
                "- Produk terdaftar BPOM (No. [isi: nomor registrasi BPOM]).\n"
                "- Produk paling laris se-Solo [isi: bukti, mis. data penjualan bulanan].\n"
                "- Harga jual Rp20.000/botol; Berkah Mart mendapat 35% (Rp7.000).")
        r, h = cek_fakta(teks)
        self.assertEqual(r.returncode, 0, h)
        self.assertEqual(h["temuan"], [])

    def test_klaim_pengguna_tanpa_bukti_jadi_cek(self):
        r, h = cek_fakta("Kopi Pakde paling laris se-Solo.")
        self.assertEqual((r.returncode, [t["level"] for t in h["temuan"]]), (0, ["CEK"]))

    def test_sifat_dan_angka_kredibilitas_karangan(self):
        r, h = cek_fakta("Brownies rumahan tanpa pengawet, sudah dipercaya 500 pelanggan sejak 2019.",
                         "brownies \"Brownies Mama Lia\" ke Kafe Teras Bogor (ada 3 cabang). Harga Rp35.000/kotak.")
        self.assertEqual(r.returncode, 2)
        kat = sorted({t["kategori"] for t in h["temuan"]})
        self.assertEqual(kat, ["angka", "klaim"])
        self.assertEqual(len(h["temuan"]), 4)


def cek_mitra(teks, fakta=FAKTA_KOPI):
    import json
    r = subprocess.run([sys.executable, CEK_FAKTA, "--teks", teks, "--fakta", fakta, "--abaikan", "jam", "--json",
                        "--dokumen-mitra"], capture_output=True, text=True, encoding="utf-8")
    return r, json.loads(r.stdout)


class UjiUlang20261001(unittest.TestCase):
    """Uji ulang anti-karang OpenClaw 2026-10-01: kota mitra jadi kota usaha & modal/laba bocor ke proposal."""

    def test_kota_mitra_dikarang_jadi_kota_usaha(self):
        r, h = cek_fakta("Saya [Nama], pemilik Kopi Pakde — kopi susu literan di Solo.")
        self.assertEqual(r.returncode, 2)
        self.assertEqual([t["kategori"] for t in h["temuan"]], ["lokasi"])

    def test_kota_mitra_dalam_konteks_mitra_lulus(self):
        for teks in ("Kopi Pakde ingin menitipkan produk di minimarket Berkah Mart di Solo.",
                     "Kopi susu literan untuk Berkah Mart di Solo.",
                     "Produk paling laris se-Solo [isi: bukti data penjualan]."):
            r, h = cek_fakta(teks)
            self.assertNotIn("lokasi", [t["kategori"] for t in h["temuan"]], teks)

    def test_kota_usaha_dari_pengguna_tidak_ditandai(self):
        fakta = ("usaha keripik singkong pedas 'Kriuk Mbok Darmi' di Bantul, mau titip jual di 5 cabang Kopi Senja "
                 "Jogja. Harga jual 25rb/bungkus.")
        r, h = cek_fakta("Kriuk Mbok Darmi, keripik singkong pedas dari Bantul.", fakta)
        self.assertEqual(h["temuan"], [])
        fakta3 = ("Tolong buatin proposal titip jual keripik tempe \"Tempe Mbak Wid\" ke toko oleh-oleh \"Sari Rasa\" di "
                  "Malang. Harga jual di toko Rp15.000/bungkus.")
        r, h = cek_fakta("Keripik tempe Tempe Mbak Wid di Malang.", fakta3)
        self.assertEqual(r.returncode, 2)
        r, h = cek_fakta("Sebagai toko oleh-oleh di Malang, Sari Rasa dikunjungi pembeli oleh-oleh.", fakta3)
        self.assertNotIn("lokasi", [t["kategori"] for t in h["temuan"]])

    def test_modal_dan_laba_bocor_ke_proposal(self):
        teks = ("**Catatan soal persentase:** Pada harga jual Rp20.000/botol dan modal produksi Rp14.000/botol, bagian 35% "
                "akan membuat Kopi Pakde merugi Rp1.000/botol (titik impas ada di 30%). Karena itu kami mengusulkan 25% "
                "(untung Rp1.000/botol bagi kami) sebagai titik awal diskusi.")
        r, h = cek_mitra(teks)
        self.assertEqual(r.returncode, 2)
        gagal = " | ".join(t["frasa"] for t in h["temuan"] if t["kategori"] == "internal" and t["level"] == "GAGAL")
        for frasa in ("modal produksi Rp14.000", "merugi Rp1.000", "titik impas ada di 30%", "untung Rp1.000"):
            self.assertIn(frasa, gagal)

    def test_proposal_bersih_untuk_mitra_lulus(self):
        teks = ("- Bagian Berkah Mart yang kami usulkan: 25% = Rp 5.000/botol terjual.\n"
                "- Tambahan pendapatan tanpa modal stok, tanpa risiko rugi beli putus.\n"
                "- Kami membuka reseller dengan untung Rp 30.000 per pcs untuk reseller.")
        r, h = cek_mitra(teks)
        self.assertEqual(r.returncode, 0, h)
        self.assertEqual([t for t in h["temuan"] if t["level"] == "GAGAL"], [])

    def test_internal_hanya_dengan_dokumen_mitra(self):
        r, h = cek_fakta("Info untuk kamu: modal Rp14.000/botol, laba Rp1.000/botol.")
        self.assertNotIn("internal", [t["kategori"] for t in h["temuan"]])


if __name__ == "__main__":
    unittest.main(verbosity=2)
