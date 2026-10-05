#!/usr/bin/env python3
"""Uji regresi untuk scripts/cek_pola.py — jalankan dengan:
    python3 tests/uji_regresi.py
(Windows: python atau py). Tidak butuh pustaka luar (unittest bawaan Python).
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

import cek_pola as cp  # noqa: E402


def id_terdeteksi(teks):
    return {t["id"] for t in cp.deteksi(teks)}


class TesPolaTerdeteksi(unittest.TestCase):
    def test_pembuka_basa_basi(self):
        self.assertIn("pembuka-basa-basi", id_terdeteksi(
            "Di era digital ini, siapa pun bisa jualan online."))

    def test_pembuka_basa_basi_variasi(self):
        self.assertIn("pembuka-basa-basi", id_terdeteksi(
            "Seiring perkembangan zaman, kebutuhan pelanggan makin beragam."))

    def test_kontras_biner(self):
        self.assertIn("kontras-biner", id_terdeteksi(
            "Produk ini tidak hanya enak, tetapi juga bergizi tinggi untuk keluarga."))

    def test_ajakan_generik(self):
        self.assertIn("ajakan-generik", id_terdeteksi(
            "Yuk simak tips memilih sepatu yang tepat berikut ini!"))

    def test_menjadi_kunci(self):
        self.assertIn("menjadi-kunci", id_terdeteksi(
            "Kualitas bahan baku menjadi kunci kesuksesan usaha kuliner kami."))

    def test_tak_dipungkiri(self):
        self.assertIn("tak-dipungkiri", id_terdeteksi(
            "Tak bisa dipungkiri, foto produk sangat penting untuk penjualan online."))

    def test_tiga_serangkai(self):
        self.assertIn("tiga-serangkai", id_terdeteksi(
            "Layanan kami cepat, mudah, dan terpercaya untuk semua pelanggan."))

    def test_emdash_berlebihan(self):
        self.assertIn("emdash-berlebihan", id_terdeteksi(
            "Kopi ini — dibuat dari biji pilihan — akan membuatmu — jatuh cinta."))

    def test_emdash_wajar_tidak_terdeteksi(self):
        # 1 em-dash dalam kalimat panjang dianggap wajar, tidak boleh kena pola ini
        self.assertNotIn("emdash-berlebihan", id_terdeteksi(
            "Promo ini berlaku sampai akhir bulan — jangan sampai kelewatan."))

    def test_emoji_berderet(self):
        self.assertIn("emoji-berderet", id_terdeteksi(
            "Promo gila-gilaan hari ini! \U0001F525\U0001F525✨\U0001F4AF"))

    def test_emoji_wajar_tidak_terdeteksi(self):
        self.assertNotIn("emoji-berderet", id_terdeteksi(
            "Promo hari ini aja \U0001F525 order sebelum jam 8 malam."))

    def test_penutup_klise(self):
        self.assertIn("penutup-klise", id_terdeteksi(
            "Itu dia tips hari ini. Semoga bermanfaat!"))

    def test_klaim_superlatif(self):
        self.assertIn("klaim-superlatif", id_terdeteksi(
            "Skincare terbaik nomor satu, dijamin puas dalam 3 hari!"))

    def test_insight_palsu(self):
        self.assertIn("insight-palsu", id_terdeteksi(
            "Yang menarik adalah, hal ini menunjukkan bahwa konsumen makin sadar kualitas."))

    def test_dramatis_terpotong(self):
        self.assertIn("dramatis-terpotong", id_terdeteksi(
            "Bayangkan jika kamu tidak perlu lagi ribet packing setiap hari."))

    def test_sok_tahu(self):
        self.assertIn("sok-tahu", id_terdeteksi(
            "Ini rahasia yang jarang dibagikan: rajin follow-up bikin closing naik."))

    def test_kesimpulan_berlebihan(self):
        self.assertIn("kesimpulan-berlebihan", id_terdeteksi(
            "Kesimpulannya, media sosial memang penting untuk bisnis kuliner."))

    def test_weasel_attribution(self):
        self.assertIn("weasel-attribution", id_terdeteksi(
            "Banyak orang percaya produk herbal lebih aman dikonsumsi."))

    def test_teks_bersih_tidak_ada_temuan(self):
        temuan = cp.deteksi(
            "Kopi susu gula aren kami dibuat dari biji lokal Garut, harga Rp18.000. "
            "Order lewat WA atau GoFood ya."
        )
        self.assertEqual(temuan, [])


class TesSkor(unittest.TestCase):
    def test_skor_teks_bersih_100(self):
        temuan = cp.deteksi("Kopi susu gula aren, harga Rp18.000, order lewat WA.")
        self.assertEqual(cp.hitung_skor(temuan), 100)

    def test_skor_turun_sesuai_bobot(self):
        temuan = cp.deteksi("Solusi terbaik nomor satu, dijamin puas!")
        skor = cp.hitung_skor(temuan)
        self.assertLess(skor, 100)

    def test_skor_tidak_pernah_negatif(self):
        # draf dengan sangat banyak pola sekaligus
        teks = (
            "Di era digital ini, tidak hanya cepat tetapi juga mudah. "
            "Yuk simak, ini menjadi kunci sukses. Tak bisa dipungkiri, "
            "cepat, mudah, dan terpercaya. Solusi terbaik nomor satu, "
            "dijamin puas, terbukti ampuh, revolusioner! "
            "Banyak orang percaya penelitian menunjukkan ini. "
            "Kesimpulannya, semoga bermanfaat!"
        )
        temuan = cp.deteksi(teks)
        self.assertGreaterEqual(cp.hitung_skor(temuan), 0)


class TesInputRusak(unittest.TestCase):
    def test_teks_kosong_deteksi_tidak_error(self):
        self.assertEqual(cp.deteksi(""), [])

    def test_teks_hanya_spasi(self):
        self.assertEqual(cp.deteksi("   \n  "), [])

    def test_teks_hanya_emoji_tanpa_kalimat(self):
        temuan = cp.deteksi("\U0001F525\U0001F525\U0001F525")
        # tetap terdeteksi sebagai emoji berderet meski tanpa kalimat bermakna
        ids = {t["id"] for t in temuan}
        self.assertIn("emoji-berderet", ids)


if __name__ == "__main__":
    unittest.main()
