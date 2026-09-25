#!/usr/bin/env python3
"""Uji regresi untuk scripts/cek_pesan.py — jalankan dengan:
    python3 tests/uji_regresi.py
(Windows: python atau py). Tidak butuh pustaka luar (unittest bawaan Python).
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import cek_pesan as cp  # noqa: E402


class TesNormalisasiNomor(unittest.TestCase):
    def test_awalan_nol(self):
        self.assertEqual(cp.normalisasi_nomor_wa("0812-3456-7890"), "6281234567890")

    def test_awalan_delapan(self):
        self.assertEqual(cp.normalisasi_nomor_wa("81234567890"), "6281234567890")

    def test_awalan_62(self):
        self.assertEqual(cp.normalisasi_nomor_wa("6281234567890"), "6281234567890")

    def test_awalan_plus62(self):
        self.assertEqual(cp.normalisasi_nomor_wa("+62 812 3456 7890"), "6281234567890")

    def test_nomor_kosong(self):
        with self.assertRaises(cp.InputSalah):
            cp.normalisasi_nomor_wa("")

    def test_nomor_none(self):
        with self.assertRaises(cp.InputSalah):
            cp.normalisasi_nomor_wa(None)

    def test_nomor_bukan_angka(self):
        with self.assertRaises(cp.InputSalah):
            cp.normalisasi_nomor_wa("08abc34567")

    def test_kode_negara_asing(self):
        with self.assertRaises(cp.InputSalah):
            cp.normalisasi_nomor_wa("15551234567")  # awalan '1' AS, bukan 0/8/62

    def test_terlalu_pendek(self):
        with self.assertRaises(cp.InputSalah):
            cp.normalisasi_nomor_wa("0812345")

    def test_terlalu_panjang(self):
        with self.assertRaises(cp.InputSalah):
            cp.normalisasi_nomor_wa("081234567890123456")


class TesBangunTautan(unittest.TestCase):
    def test_tanpa_pesan(self):
        self.assertEqual(cp.bangun_tautan_wa("0812-3456-7890"), "https://wa.me/6281234567890")

    def test_dengan_pesan(self):
        tautan = cp.bangun_tautan_wa("0812-3456-7890", "Halo, apa kabar?")
        self.assertTrue(tautan.startswith("https://wa.me/6281234567890?text="))
        self.assertIn("Halo%2C", tautan)

    def test_pesan_kosong_string(self):
        self.assertEqual(cp.bangun_tautan_wa("0812-3456-7890", "   "), "https://wa.me/6281234567890")


class TesKalimatPanjang(unittest.TestCase):
    def test_kalimat_pendek_lolos(self):
        teks = "Halo Pak Budi. Saya Rian dari Toko Berkah. Ada waktu sebentar?"
        self.assertEqual(cp.cek_kalimat_panjang(teks), [])

    def test_kalimat_panjang_terdeteksi(self):
        kalimat = "Saya " + "sangat sangat sangat " * 10 + "senang bisa menghubungi Bapak hari ini."
        hasil = cp.cek_kalimat_panjang(kalimat)
        self.assertEqual(len(hasil), 1)


class TesKapitalBerlebihan(unittest.TestCase):
    def test_singkatan_aman_dilewati(self):
        teks = "Silakan hubungi CS kami via WA atau kunjungi PT Maju Jaya."
        self.assertEqual(cp.cek_kapital_berlebihan(teks), [])

    def test_kata_teriak_terdeteksi(self):
        teks = "PROMO GILA khusus hari ini, GRATIS ongkir!"
        hasil = cp.cek_kapital_berlebihan(teks)
        self.assertIn("PROMO", hasil)
        self.assertIn("GILA", hasil)
        self.assertIn("GRATIS", hasil)


class TesPemicuSpam(unittest.TestCase):
    def test_bersih(self):
        teks = "Selamat siang Pak Andi, perkenalkan saya Rian dari Toko Berkah."
        self.assertEqual(cp.cek_kata_pemicu_spam(teks), [])

    def test_frasa_spam_terdeteksi(self):
        teks = "GRATIS!!! ongkir hari ini, 100% dijamin puas!!!"
        hasil = cp.cek_kata_pemicu_spam(teks)
        self.assertTrue(any("gratis" in h for h in hasil))
        self.assertTrue(any("dijamin" in h for h in hasil))

    def test_tanda_seru_berulang(self):
        teks = "Buruan order sekarang!!!"
        hasil = cp.cek_kata_pemicu_spam(teks)
        self.assertTrue(any("tanda seru" in h for h in hasil))


class TesLinkDanKataKunci(unittest.TestCase):
    def test_hitung_link(self):
        teks = "Info produk di https://tokosaya.id dan lihat juga www.instagram.com/tokosaya"
        self.assertEqual(cp.hitung_link(teks), 2)

    def test_tanpa_link(self):
        self.assertEqual(cp.hitung_link("Halo Pak, apa kabar?"), 0)

    def test_asal_kontak_terdeteksi(self):
        teks = "Perkenalkan, saya dapat nomor Bapak dari rekan di Google Maps."
        self.assertTrue(cp.cek_kata_kunci(teks, cp.KATA_KUNCI_ASAL_KONTAK))

    def test_asal_kontak_tidak_ada(self):
        teks = "Selamat siang Pak, kami menjual jasa cleaning service."
        self.assertFalse(cp.cek_kata_kunci(teks, cp.KATA_KUNCI_ASAL_KONTAK))

    def test_opsi_keluar_terdeteksi(self):
        teks = "Boleh diabaikan bila tidak relevan ya, Pak. Terima kasih."
        self.assertTrue(cp.cek_kata_kunci(teks, cp.KATA_KUNCI_OPSI_KELUAR))


class TesJamKirim(unittest.TestCase):
    def test_tidak_diisi(self):
        self.assertIsNone(cp.cek_jam_kirim(None))
        self.assertIsNone(cp.cek_jam_kirim(""))

    def test_jam_wajar(self):
        jam, wajar = cp.cek_jam_kirim("10:30")
        self.assertEqual(jam, 10)
        self.assertTrue(wajar)

    def test_jam_batas_awal_wajar(self):
        jam, wajar = cp.cek_jam_kirim("08:00")
        self.assertTrue(wajar)

    def test_jam_batas_akhir_tidak_wajar(self):
        jam, wajar = cp.cek_jam_kirim("20:00")
        self.assertFalse(wajar)  # 20:00 dianggap sudah di batas, bukan wajar lagi

    def test_jam_malam_tidak_wajar(self):
        jam, wajar = cp.cek_jam_kirim("22:15")
        self.assertFalse(wajar)

    def test_jam_subuh_tidak_wajar(self):
        jam, wajar = cp.cek_jam_kirim("05:00")
        self.assertFalse(wajar)

    def test_format_salah(self):
        with self.assertRaises(cp.InputSalah):
            cp.cek_jam_kirim("25:99")

    def test_format_bukan_jam(self):
        with self.assertRaises(cp.InputSalah):
            cp.cek_jam_kirim("malam")


class TesPeriksaPesanLengkap(unittest.TestCase):
    def test_pesan_baik_tidak_ada_peringatan_utama(self):
        teks = (
            "Selamat siang, Pak Dedi. Perkenalkan saya Sinta dari Toko Kemasan Hijau. "
            "Saya dapat nomor Bapak dari rekan di pameran UMKM kemarin. "
            "Kami menyediakan kemasan makanan ramah lingkungan untuk usaha katering. "
            "Boleh saya kirim katalog singkat? Boleh diabaikan bila belum relevan, Pak."
        )
        hasil = cp.periksa_pesan(teks, jam_kirim="10:00")
        self.assertTrue(hasil["sebut_asal_kontak"])
        self.assertTrue(hasil["ada_opsi_keluar"])
        self.assertTrue(hasil["jam_kirim_wajar"])
        self.assertEqual(cp.cek_kata_pemicu_spam(teks), [])

    def test_pesan_kosong_ditolak(self):
        with self.assertRaises(cp.InputSalah):
            cp.periksa_pesan("")
        with self.assertRaises(cp.InputSalah):
            cp.periksa_pesan("    ")

    def test_pesan_spam_banyak_peringatan(self):
        teks = "GRATIS!!! PROMO GILA hari ini, 100% dijamin murah!!! Cek http://a.co www.b.co www.c.co"
        hasil = cp.periksa_pesan(teks, jam_kirim="23:00")
        self.assertGreaterEqual(len(hasil["peringatan"]), 4)
        self.assertFalse(hasil["sebut_asal_kontak"])
        self.assertFalse(hasil["ada_opsi_keluar"])
        self.assertFalse(hasil["jam_kirim_wajar"])

    def test_pesan_kepanjangan_memicu_peringatan_karakter(self):
        teks = "Halo Pak. " * 90  # jauh di atas batas karakter
        hasil = cp.periksa_pesan(teks)
        self.assertTrue(any("karakter" in p for p in hasil["peringatan"]))

    def test_data_rusak_file_tidak_ada(self):
        # dipakai lewat CLI, bukan fungsi ini langsung — diuji di TesCLI
        pass


class TesCLI(unittest.TestCase):
    def test_wa_lewat_cli(self):
        kode = cp.main(["wa", "--nomor", "0812-3456-7890", "--pesan", "Halo"])
        self.assertEqual(kode, 0)

    def test_wa_nomor_rusak_lewat_cli(self):
        kode = cp.main(["wa", "--nomor", "abc"])
        self.assertEqual(kode, 1)

    def test_cek_pesan_lewat_cli(self):
        kode = cp.main(["cek", "--pesan", "Halo Pak, apa kabar hari ini?"])
        self.assertEqual(kode, 0)

    def test_cek_file_tidak_ada(self):
        kode = cp.main(["cek", "--file", "/path/tidak/ada/sama/sekali.txt"])
        self.assertEqual(kode, 1)

    def test_cek_jam_format_salah_lewat_cli(self):
        kode = cp.main(["cek", "--pesan", "Halo", "--jam-kirim", "bukan-jam"])
        self.assertEqual(kode, 1)


if __name__ == "__main__":
    unittest.main()
