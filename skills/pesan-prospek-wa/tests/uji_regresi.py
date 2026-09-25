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


class TesRegresiB1AsalKontak(unittest.TestCase):
    """v1.0.1 — B1: setiap pola di references/pola-pembuka.md harus terdeteksi,
    dan "dari bapak/ibu" sendirian TIDAK boleh salah-positif."""

    def test_pola_1_referral(self):
        teks = ("Selamat siang, Bu Sari. Perkenalkan saya Andi dari Kopi Nusantara. "
                "Saya dapat nomor Ibu dari Pak Joko, yang menyarankan saya menghubungi "
                "langsung karena Ibu sedang cari supplier kopi baru.")
        self.assertTrue(cp.cek_kata_kunci(teks, cp.KATA_KUNCI_ASAL_KONTAK))

    def test_pola_2_pameran(self):
        teks = ("Selamat siang, Pak Budi. Saya Rian dari Katering Berkah, kemarin sempat "
                "bertukar kontak di Jakarta Food & Franchise Expo. Sesuai yang Bapak "
                "ceritakan soal kebutuhan katering kantor, saya mau menindaklanjuti.")
        self.assertTrue(cp.cek_kata_kunci(teks, cp.KATA_KUNCI_ASAL_KONTAK))

    def test_pola_3_google_maps(self):
        teks = ("Selamat pagi, Bu. Saya Sinta dari Kemasan Hijau. Saya melihat Kafe Roma "
                "di Google Maps saat mencari kafe di area Bandung, dan tertarik menawarkan "
                "kopi roastery kami.")
        self.assertTrue(cp.cek_kata_kunci(teks, cp.KATA_KUNCI_ASAL_KONTAK))

    def test_pola_4_instagram(self):
        teks = ("Selamat siang, Kak. Saya Dewi dari Butik Cantik. Saya lihat akun Instagram "
                "@tokobajukamu dan tertarik dengan koleksi terbaru, jadi ingin menawarkan "
                "kerja sama reseller.")
        self.assertTrue(cp.cek_kata_kunci(teks, cp.KATA_KUNCI_ASAL_KONTAK))

    def test_pola_5_grup_komunitas(self):
        teks = ("Selamat siang, Pak. Saya Rudi, sama-sama anggota grup Pengusaha UMKM "
                "Bandung. Melihat Bapak pernah membahas soal kemasan produk di grup, "
                "saya ingin menawarkan jasa desain kemasan.")
        self.assertTrue(cp.cek_kata_kunci(teks, cp.KATA_KUNCI_ASAL_KONTAK))

    def test_pola_website(self):
        teks = ("Selamat siang, Pak. Saya Dodi dari Cetak Cepat. Saya lihat nomor Bapak "
                "di website resmi perusahaan, ingin menawarkan jasa percetakan.")
        self.assertTrue(cp.cek_kata_kunci(teks, cp.KATA_KUNCI_ASAL_KONTAK))

    def test_tidak_salah_positif_dari_ibu_saja(self):
        # "dari ibu"/"dari bapak" sendirian (tanpa konteks asal kontak) tidak boleh
        # dianggap menyebut asal kontak — mis. cerita resep, bukan sumber kontak.
        teks = "Kami masih pakai resep warisan dari ibu saya sejak tahun 1998."
        self.assertFalse(cp.cek_kata_kunci(teks, cp.KATA_KUNCI_ASAL_KONTAK))
        teks2 = "Rumah ini dulu dari bapak saya, sudah 20 tahun."
        self.assertFalse(cp.cek_kata_kunci(teks2, cp.KATA_KUNCI_ASAL_KONTAK))


class TesRegresiB2NormalisasiNomor(unittest.TestCase):
    """v1.0.1 — B2: typo umum dikoreksi, "00" dibuang, panjang tidak wajar ditolak."""

    def test_plus62_0_dikoreksi(self):
        # "+62 0812..." (salah ketik umum: menulis '0' lokal setelah kode negara)
        self.assertEqual(cp.normalisasi_nomor_wa("+6208123456789"), "628123456789")

    def test_awalan_00_dibuang(self):
        self.assertEqual(cp.normalisasi_nomor_wa("0062812345678"), "62812345678")

    def test_14_digit_ditolak_dengan_pesan_jelas(self):
        with self.assertRaises(cp.InputSalah) as ctx:
            cp.normalisasi_nomor_wa("08123456789012")  # 14 digit
        self.assertIn("panjang", str(ctx.exception).lower())

    def test_telepon_rumah_ditolak(self):
        # Bukan pola seluler 08xx (021 = kode area, bukan 08xx)
        with self.assertRaises(cp.InputSalah):
            cp.normalisasi_nomor_wa("021-5551234")

    def test_digit_unicode_fullwidth_ditolak_pesan_benar(self):
        with self.assertRaises(cp.InputSalah) as ctx:
            cp.normalisasi_nomor_wa("０８１２３４５６７８９０")
        self.assertIn("angka biasa 0-9", str(ctx.exception))


class TesRegresiB3SingkatanAman(unittest.TestCase):
    """v1.0.1 — B3: istilah B2B/UMKM Indonesia yang lazim kapital tidak dianggap teriak."""

    def test_singkatan_b2b_tidak_terdeteksi(self):
        teks = ("Kami bantu urus SPT dan PPN bulanan, sudah biasa berhubungan dengan HRD "
                "dan tim BPJS perusahaan Bapak, sesuai standar SOP kami.")
        self.assertEqual(cp.cek_kapital_berlebihan(teks), [])

    def test_masih_deteksi_kata_teriak_asli(self):
        teks = "PROMO GILA khusus hari ini, GRATIS ongkir!"
        hasil = cp.cek_kapital_berlebihan(teks)
        self.assertIn("PROMO", hasil)
        self.assertIn("GRATIS", hasil)


class TesRegresiB4JamKirim(unittest.TestCase):
    """v1.0.1 — B4: format titik & 4-digit diterima; --zona divalidasi lewat periksa_pesan."""

    def test_format_titik_diterima(self):
        jam, wajar = cp.cek_jam_kirim("19.30")
        self.assertEqual(jam, 19)
        self.assertTrue(wajar)

    def test_format_titik_dua_masih_diterima(self):
        jam, wajar = cp.cek_jam_kirim("19:30")
        self.assertEqual(jam, 19)

    def test_format_4_digit_diterima(self):
        jam, wajar = cp.cek_jam_kirim("1930")
        self.assertEqual(jam, 19)
        self.assertTrue(wajar)

    def test_zona_valid_diterima(self):
        hasil = cp.periksa_pesan("Halo Pak, apa kabar?", jam_kirim="19.30", zona="WITA")
        self.assertEqual(hasil["zona"], "WITA")

    def test_zona_tidak_valid_ditolak(self):
        with self.assertRaises(cp.InputSalah):
            cp.periksa_pesan("Halo Pak, apa kabar?", jam_kirim="19.30", zona="GMT")

    def test_format_masih_salah_ditolak(self):
        with self.assertRaises(cp.InputSalah):
            cp.cek_jam_kirim("25:99")


class TesRegresiB7Emoji(unittest.TestCase):
    """v1.0.1 — B7: emoji dihitung, peringatan muncul bila > 3."""

    def test_emoji_wajar_tidak_peringatan(self):
        teks = "Selamat siang Pak, apa kabar? 😊"
        hasil = cp.periksa_pesan(teks)
        self.assertEqual(hasil["jumlah_emoji"], 1)
        self.assertFalse(any("emoji" in p.lower() for p in hasil["peringatan"]))

    def test_emoji_berlebihan_memicu_peringatan(self):
        teks = "Halo Pak 😊🎉🔥💯✅ semoga berkenan ya!"
        hasil = cp.periksa_pesan(teks)
        self.assertGreater(hasil["jumlah_emoji"], 3)
        self.assertTrue(any("emoji" in p.lower() for p in hasil["peringatan"]))


class TesRegresiB8PisahBarisBaru(unittest.TestCase):
    """v1.0.1 — B8: daftar poin bergaya "✅ ...\\n✅ ..." tanpa titik dipisah per baris."""

    def test_baris_tanpa_titik_dipisah(self):
        teks = "✅ tersedia varian pedas\n✅ pengiriman cepat\n✅ bisa retur"
        hasil = cp.pisah_kalimat(teks)
        self.assertEqual(len(hasil), 3)


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
