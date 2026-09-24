#!/usr/bin/env python3
"""Tes mandiri untuk cek_sitasi.py — jalankan:
    python3 test_cek_sitasi.py
Hanya library standar (unittest).
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
import cek_sitasi as cs


DRAF_NORMAL = """# Judul Artikel

Transaksi e-commerce Indonesia tumbuh 12% pada 2025 [1]. Menurut OJK, literasi keuangan
digital juga naik [2].

## Daftar Pustaka
[1] Statistik E-Commerce 2025. BPS. 2025. https://www.bps.go.id/statistik . Diakses 24 September 2026.
[2] Survei Literasi Keuangan. OJK. 2025. https://www.ojk.go.id/survei . Diakses 24 September 2026.
"""

DRAF_KUTIPAN_HILANG = """# Judul

Angka ini penting [1] dan juga ini [3].

## Daftar Pustaka
[1] Sumber Satu. Lembaga A. 2025. https://a.go.id . Diakses 24 September 2026.
"""

DRAF_TANPA_PUSTAKA = """# Judul

Ada klaim [1] tapi tidak ada daftar pustaka.
"""

DRAF_URL_DUPLIKAT = """# Judul

Klaim satu [1]. Klaim dua [2].

## Daftar Pustaka
[1] Sumber A. Lembaga A. 2025. https://sama.go.id/halaman . Diakses 24 September 2026.
[2] Sumber B (judul beda). Lembaga B. 2025. https://sama.go.id/halaman . Diakses 24 September 2026.
"""

DRAF_ENTRI_TAK_DIPAKAI = """# Judul

Hanya klaim [1] yang dipakai di sini.

## Daftar Pustaka
[1] Sumber Satu. Lembaga A. 2025. https://a.go.id . Diakses 24 September 2026.
[2] Sumber Dua tidak pernah dikutip. Lembaga B. 2025. https://b.go.id . Diakses 24 September 2026.
"""

DRAF_NOMOR_DUPLIKAT = """# Judul

Klaim [1].

## Daftar Pustaka
[1] Sumber Pertama. Lembaga A. 2025. https://a.go.id . Diakses 24 September 2026.
[1] Sumber Kedua Memakai Nomor Sama. Lembaga B. 2025. https://b.go.id . Diakses 24 September 2026.
"""

DRAF_STATISTIK_TANPA_KUTIPAN = """# Judul

Pertumbuhan mencapai 25% tahun ini tanpa disebut sumbernya.
Pendapatan sebesar Rp 5.000.000 juga tidak berkutipan.
Ini opini saya saja tanpa angka apa pun.

## Daftar Pustaka
[1] Sumber Satu. Lembaga A. 2025. https://a.go.id . Diakses 24 September 2026.
"""

DRAF_ENTRI_TANPA_URL = """# Judul

Klaim dari wawancara langsung [1].

## Daftar Pustaka
[1] Wawancara langsung dengan pemilik usaha. 2026. Diakses 24 September 2026.
"""

DRAF_KUTIPAN_GABUNGAN = """# Judul

Dua sumber sekaligus mendukung klaim ini [1][2].

## Daftar Pustaka
[1] Sumber Satu. Lembaga A. 2025. https://a.go.id . Diakses 24 September 2026.
[2] Sumber Dua. Lembaga B. 2025. https://b.go.id . Diakses 24 September 2026.
"""

DRAF_KUTIPAN_KOMA = """# Judul

Sumber gabungan gaya koma [1, 2].

## Daftar Pustaka
[1] Sumber Satu. Lembaga A. 2025. https://a.go.id . Diakses 24 September 2026.
[2] Sumber Dua. Lembaga B. 2025. https://b.go.id . Diakses 24 September 2026.
"""

DRAF_KOSONG = ""


class TesDrafNormal(unittest.TestCase):
    def test_lulus_tanpa_error(self):
        hasil = cs.periksa(DRAF_NORMAL)
        self.assertTrue(hasil["lulus"])
        self.assertEqual(hasil["error"], [])

    def test_jumlah_kutipan_dan_entri(self):
        hasil = cs.periksa(DRAF_NORMAL)
        self.assertEqual(hasil["jumlah_kutipan_unik_di_teks"], 2)
        self.assertEqual(hasil["jumlah_entri_pustaka"], 2)


class TesKutipanHilang(unittest.TestCase):
    def test_gagal_karena_nomor_tidak_ada_di_pustaka(self):
        hasil = cs.periksa(DRAF_KUTIPAN_HILANG)
        self.assertFalse(hasil["lulus"])
        self.assertTrue(any("[3]" in e for e in hasil["error"]))


class TesTanpaDaftarPustaka(unittest.TestCase):
    def test_gagal_tanpa_bagian_pustaka(self):
        hasil = cs.periksa(DRAF_TANPA_PUSTAKA)
        self.assertFalse(hasil["lulus"])
        self.assertTrue(any("Daftar Pustaka" in e for e in hasil["error"]))


class TesUrlDuplikat(unittest.TestCase):
    def test_gagal_karena_url_sama_nomor_beda(self):
        hasil = cs.periksa(DRAF_URL_DUPLIKAT)
        self.assertFalse(hasil["lulus"])
        self.assertTrue(any("URL yang sama" in e for e in hasil["error"]))


class TesEntriTidakDipakai(unittest.TestCase):
    def test_peringatan_bukan_error(self):
        hasil = cs.periksa(DRAF_ENTRI_TAK_DIPAKAI)
        self.assertTrue(hasil["lulus"])  # hanya peringatan, bukan error keras
        self.assertTrue(any("tidak pernah dikutip" in p for p in hasil["peringatan"]))


class TesNomorDuplikat(unittest.TestCase):
    def test_gagal_karena_nomor_dobel_di_pustaka(self):
        hasil = cs.periksa(DRAF_NOMOR_DUPLIKAT)
        self.assertFalse(hasil["lulus"])
        self.assertTrue(any("lebih dari sekali" in e for e in hasil["error"]))


class TesStatistikTanpaKutipan(unittest.TestCase):
    def test_terdeteksi_sebagai_peringatan(self):
        hasil = cs.periksa(DRAF_STATISTIK_TANPA_KUTIPAN)
        self.assertTrue(hasil["lulus"])  # heuristik = peringatan saja
        gabungan = " ".join(hasil["peringatan"])
        self.assertIn("25%", gabungan)
        self.assertIn("Rp", gabungan)

    def test_opini_tanpa_angka_tidak_ditandai(self):
        hasil = cs.periksa(DRAF_STATISTIK_TANPA_KUTIPAN)
        gabungan = " ".join(hasil["peringatan"])
        self.assertNotIn("opini saya saja", gabungan)


class TesEntriTanpaUrl(unittest.TestCase):
    def test_peringatan_entri_tanpa_url(self):
        hasil = cs.periksa(DRAF_ENTRI_TANPA_URL)
        self.assertTrue(hasil["lulus"])
        self.assertTrue(any("tidak punya URL" in p for p in hasil["peringatan"]))


class TesKutipanGabungan(unittest.TestCase):
    def test_kutipan_gaya_kurung_ganda(self):
        hasil = cs.periksa(DRAF_KUTIPAN_GABUNGAN)
        self.assertTrue(hasil["lulus"])
        self.assertEqual(hasil["jumlah_kutipan_unik_di_teks"], 2)

    def test_kutipan_gaya_koma(self):
        hasil = cs.periksa(DRAF_KUTIPAN_KOMA)
        self.assertTrue(hasil["lulus"])
        self.assertEqual(hasil["jumlah_kutipan_unik_di_teks"], 2)


class TesInputKosong(unittest.TestCase):
    def test_draf_kosong_tidak_meledak(self):
        hasil = cs.periksa(DRAF_KOSONG)
        self.assertFalse(hasil["lulus"])
        self.assertEqual(hasil["jumlah_kutipan_unik_di_teks"], 0)
        self.assertEqual(hasil["jumlah_entri_pustaka"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
