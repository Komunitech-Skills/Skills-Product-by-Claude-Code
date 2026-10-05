#!/usr/bin/env python3
"""Tes mandiri untuk cek_halaman.py. Jalankan: python3 test_cek_halaman.py
Tidak memakai framework eksternal (hanya pustaka standar) supaya bisa jalan
di mana saja. Mencakup HTML normal, rusak, kosong, dan encoding aneh sesuai
Tahap 6 CLAUDE.md.
"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from cek_halaman import (
    InputSalah,
    analisis_canonical,
    analisis_gambar,
    analisis_heading,
    analisis_jsonld,
    analisis_kata_kunci,
    analisis_lengkap,
    analisis_meta_description,
    analisis_og,
    analisis_robots,
    analisis_tautan,
    analisis_title,
    baca_html,
    ekstrak,
    perbaiki_tag_rawtext_tidak_tertutup,
    ukuran_halaman,
)

HTML_NORMAL = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="utf-8">
<title>Keripik Pedas Bandung Level 1-10 | Toko Renyah Jaya</title>
<meta name="description" content="Keripik pedas Bandung asli, level 1 sampai 10, tanpa pengawet, kirim ke seluruh Indonesia lewat JNE/JNT.">
<link rel="canonical" href="https://tokorenyahjaya.com/produk/keripik-pedas-bandung">
<meta property="og:title" content="Keripik Pedas Bandung">
<meta property="og:description" content="Renyah dan pedas mantap">
<meta property="og:image" content="https://tokorenyahjaya.com/gambar/keripik.jpg">
<meta property="og:type" content="product">
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Keripik Pedas Bandung",
  "image": "https://tokorenyahjaya.com/gambar/keripik.jpg",
  "offers": {
    "@type": "Offer",
    "price": "25000",
    "priceCurrency": "IDR",
    "availability": "https://schema.org/InStock"
  }
}
</script>
</head>
<body>
<h1>Keripik Pedas Bandung Asli</h1>
<p>Keripik pedas Bandung buatan rumahan, digoreng segar setiap hari dan dikirim ke seluruh Indonesia.</p>
<h2>Kenapa pilih kami</h2>
<img src="foto1.jpg" alt="Keripik pedas Bandung dalam kemasan">
<img src="foto2.jpg">
<a href="/kontak">Kontak</a>
<a href="#">Klik di sini</a>
<a href="javascript:void(0)">Beli</a>
</body>
</html>
"""

HTML_RUSAK = """<html><head><title>Toko Servis AC Bekasi
<meta name="description" content="Servis AC panggilan area Bekasi, cek freon & cuci AC.">
<h1>Servis AC Bekasi<h2>Kenapa Kami</h1>
<img src="ac.jpg" alt="">
<p>Kami melayani servis AC di seluruh Bekasi.
"""

HTML_TANPA_APAPUN = "<html><body><p>Halaman kosong tanpa SEO apa pun.</p></body></html>"


class TesTitle(unittest.TestCase):
    def test_kosong(self):
        self.assertEqual(analisis_title(None)["status"], "KOSONG")
        self.assertEqual(analisis_title("")["status"], "KOSONG")

    def test_pendek(self):
        self.assertEqual(analisis_title("Toko Saya")["status"], "PENDEK")

    def test_pas(self):
        self.assertEqual(analisis_title("Keripik Pedas Bandung Level 1-10 Renyah")["status"], "PAS")

    def test_panjang(self):
        t = "x" * 61
        self.assertEqual(analisis_title(t)["status"], "PANJANG")

    def test_batas_pas_persis_60(self):
        self.assertEqual(analisis_title("x" * 60)["status"], "PAS")


class TesMetaDescription(unittest.TestCase):
    def test_kosong(self):
        self.assertEqual(analisis_meta_description(None)["status"], "KOSONG")

    def test_pendek(self):
        self.assertEqual(analisis_meta_description("Servis AC Bekasi.")["status"], "PENDEK")

    def test_pas(self):
        teks = "Servis AC panggilan area Bekasi, cek freon, cuci AC, dan perbaikan kompresor. Teknisi berpengalaman, datang hari yang sama."
        self.assertEqual(analisis_meta_description(teks)["status"], "PAS")

    def test_panjang(self):
        self.assertEqual(analisis_meta_description("y" * 156)["status"], "PANJANG")


class TesHeading(unittest.TestCase):
    def test_satu_h1_tanpa_lompatan(self):
        h = analisis_heading([(1, "Judul Utama"), (2, "Sub A"), (2, "Sub B")])
        self.assertEqual(h["jumlah_h1"], 1)
        self.assertEqual(h["lompatan_level"], [])

    def test_tanpa_h1(self):
        h = analisis_heading([(2, "Sub saja")])
        self.assertEqual(h["jumlah_h1"], 0)

    def test_lebih_dari_satu_h1(self):
        h = analisis_heading([(1, "A"), (1, "B")])
        self.assertEqual(h["jumlah_h1"], 2)

    def test_lompatan_level(self):
        h = analisis_heading([(1, "A"), (3, "Lompat ke H3")])
        self.assertEqual(len(h["lompatan_level"]), 1)
        self.assertEqual(h["lompatan_level"][0]["dari"], 1)
        self.assertEqual(h["lompatan_level"][0]["ke"], 3)

    def test_heading_kosong(self):
        h = analisis_heading([(1, "")])
        self.assertIn("H1", h["heading_teks_kosong"])


class TesGambar(unittest.TestCase):
    def test_campuran(self):
        gambar = [
            {"src": "a.jpg", "punya_alt": True, "alt_kosong": False},
            {"src": "b.jpg", "punya_alt": False, "alt_kosong": False},
            {"src": "c.jpg", "punya_alt": True, "alt_kosong": True},
        ]
        g = analisis_gambar(gambar)
        self.assertEqual(g["total"], 3)
        self.assertEqual(g["tanpa_atribut_alt"], ["b.jpg"])
        self.assertEqual(g["alt_kosong"], ["c.jpg"])


class TesTautan(unittest.TestCase):
    def test_format_bermasalah(self):
        links = [
            {"href": "/kontak", "punya_href": True},
            {"href": "#", "punya_href": True},
            {"href": "javascript:void(0)", "punya_href": True},
            {"href": "https://a.com/halaman ini", "punya_href": True},
            {"href": None, "punya_href": False},
        ]
        t = analisis_tautan(links)
        self.assertEqual(t["total"], 5)
        self.assertEqual(len(t["bermasalah"]), 4)


class TesCanonical(unittest.TestCase):
    def test_sama_dengan_url(self):
        c = analisis_canonical("https://a.com/x", "https://a.com/x")
        self.assertTrue(c["sama_dengan_url"])

    def test_beda_dengan_url(self):
        c = analisis_canonical("https://a.com/x", "https://a.com/y")
        self.assertFalse(c["sama_dengan_url"])

    def test_tidak_ada(self):
        c = analisis_canonical(None)
        self.assertFalse(c["ada"])


class TesRobots(unittest.TestCase):
    def test_noindex(self):
        r = analisis_robots("noindex, follow")
        self.assertTrue(r["noindex"])

    def test_tidak_ada(self):
        r = analisis_robots(None)
        self.assertFalse(r["ada"])
        self.assertFalse(r["noindex"])


class TesOpenGraph(unittest.TestCase):
    def test_semua_ada(self):
        og = {"og:title": "a", "og:description": "b", "og:image": "c", "og:type": "product"}
        self.assertEqual(analisis_og(og)["wajib_hilang"], [])

    def test_ada_yang_hilang(self):
        og = {"og:title": "a"}
        hilang = analisis_og(og)["wajib_hilang"]
        self.assertIn("og:image", hilang)


class TesJsonLd(unittest.TestCase):
    def test_valid_product_lengkap(self):
        blok = ['{"@type": "Product", "name": "X", "image": "x.jpg", "offers": {"price": "1000", "priceCurrency": "IDR", "availability": "InStock"}}']
        hasil = analisis_jsonld(blok)
        self.assertTrue(hasil[0]["valid"])
        self.assertEqual(hasil[0]["catatan"], [])

    def test_product_kurang_field(self):
        blok = ['{"@type": "Product", "name": "X"}']
        hasil = analisis_jsonld(blok)
        self.assertTrue(any("image" in c for c in hasil[0]["catatan"]))
        self.assertTrue(any("offers" in c for c in hasil[0]["catatan"]))

    def test_localbusiness_tanpa_alamat(self):
        blok = ['{"@type": "LocalBusiness", "name": "Toko Saya"}']
        hasil = analisis_jsonld(blok)
        self.assertTrue(any("address" in c for c in hasil[0]["catatan"]))

    def test_localbusiness_alamat_lengkap_indonesia(self):
        blok = ['''{
            "@type": "LocalBusiness", "name": "Servis AC Bekasi Jaya",
            "telephone": "+6281234567890",
            "openingHours": "Mo-Sa 08:00-17:00",
            "address": {"streetAddress": "Jl. Mawar No. 1", "addressLocality": "Bekasi",
                         "addressRegion": "Jawa Barat", "postalCode": "17111", "addressCountry": "ID"}
        }''']
        hasil = analisis_jsonld(blok)
        self.assertEqual(hasil[0]["catatan"], [])

    def test_json_tidak_valid(self):
        blok = ["{ini bukan json valid"]
        hasil = analisis_jsonld(blok)
        self.assertFalse(hasil[0]["valid"])
        self.assertIn("error", hasil[0])

    def test_blok_kosong(self):
        hasil = analisis_jsonld([""])
        self.assertFalse(hasil[0]["valid"])

    def test_rating_memicu_peringatan_asli(self):
        blok = ['{"@type": "Product", "name": "X", "image": "x.jpg", "offers": {"price":"1","priceCurrency":"IDR","availability":"InStock"}, "aggregateRating": {"ratingValue": "5"}}']
        hasil = analisis_jsonld(blok)
        self.assertTrue(any("asli" in c for c in hasil[0]["catatan"]))


class TesKataKunci(unittest.TestCase):
    def test_ditemukan_semua(self):
        hasil = analisis_kata_kunci(
            "keripik pedas bandung",
            title="Keripik Pedas Bandung Enak",
            headings=[(1, "Keripik Pedas Bandung Asli")],
            paragraf_awal="Ini adalah keripik pedas Bandung terenak.",
            url="https://a.com/keripik-pedas-bandung",
        )
        self.assertTrue(hasil["di_title"])
        self.assertTrue(hasil["di_h1"])
        self.assertTrue(hasil["di_url"])
        self.assertTrue(hasil["di_paragraf_awal"])

    def test_url_tanda_hubung_dan_variasi_cocok(self):
        for url in ("https://a.com/Keripik-Pedas", "https://a.com/keripik_pedas",
                    "https://a.com/keripik%20pedas", "https://a.com/?q=keripik+pedas"):
            h = analisis_kata_kunci("keripik pedas", "", [], "", url)
            self.assertTrue(h["di_url"], url)
        h = analisis_kata_kunci("keripik pedas", "", [], "", "https://a.com/keripikpedas")
        self.assertFalse(h["di_url"])

    def test_tidak_ditemukan(self):
        hasil = analisis_kata_kunci("servis ac bekasi", title="Toko Kue Enak", headings=[], paragraf_awal="", url=None)
        self.assertFalse(hasil["di_title"])
        self.assertFalse(hasil["di_h1"])
        self.assertFalse(hasil["di_url"])

    def test_tanpa_kata_kunci_hasil_none(self):
        self.assertIsNone(analisis_kata_kunci(None, "judul", [], "", None))


class TesUkuranHalaman(unittest.TestCase):
    def test_kb_dihitung_benar(self):
        u = ukuran_halaman(2048)
        self.assertEqual(u["kb"], 2.0)


class TesBacaFile(unittest.TestCase):
    def _tulis(self, isi_bytes):
        f = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
        f.write(isi_bytes)
        f.close()
        return f.name

    def test_file_tidak_ada(self):
        with self.assertRaises(InputSalah):
            baca_html("/path/tidak/ada/sama/sekali.html")

    def test_file_kosong(self):
        path = self._tulis(b"")
        with self.assertRaises(InputSalah):
            baca_html(path)

    def test_file_normal_utf8(self):
        path = self._tulis(HTML_NORMAL.encode("utf-8"))
        teks, jumlah_bytes, catatan = baca_html(path)
        self.assertIn("Keripik Pedas Bandung", teks)
        self.assertIsNone(catatan)

    def test_encoding_latin1_tanpa_deklarasi_charset(self):
        # Karakter é (bukan UTF-8 valid dalam byte tunggal latin-1: 0xe9)
        isi = "<html><head><title>Kafe R\xe9sto</title></head><body></body></html>".encode("latin-1")
        teks, _, catatan = baca_html(self._tulis(isi))
        self.assertIn("Kafe", teks)
        self.assertIsNotNone(catatan)


class TesPerbaikanRawtextTidakTertutup(unittest.TestCase):
    """Tes langsung untuk perbaiki_tag_rawtext_tidak_tertutup (regresi S1)."""

    def test_title_tertutup_normal_tidak_berubah(self):
        html = "<html><head><title>Judul OK</title></head><body></body></html>"
        hasil, peringatan = perbaiki_tag_rawtext_tidak_tertutup(html)
        self.assertEqual(hasil, html)
        self.assertEqual(peringatan, [])

    def test_title_tidak_tertutup_dipotong_sebelum_tag_berikutnya(self):
        html = "<html><head><title>Judul Tanpa Tutup</head><body><h1>Judul Utama</h1></body></html>"
        hasil, peringatan = perbaiki_tag_rawtext_tidak_tertutup(html)
        self.assertIn("<title>Judul Tanpa Tutup</title>", hasil)
        self.assertIn("<h1>Judul Utama</h1>", hasil)
        self.assertEqual(len(peringatan), 1)
        self.assertIn("<title>", peringatan[0])

    def test_title_tidak_tertutup_sampai_akhir_dokumen(self):
        html = "<html><head><title>Cuma teks polos tanpa tag lain sesudahnya"
        hasil, peringatan = perbaiki_tag_rawtext_tidak_tertutup(html)
        self.assertTrue(hasil.endswith("</title>"))
        self.assertEqual(len(peringatan), 1)

    def test_style_tidak_tertutup_dipotong_sebelum_tag_berikutnya(self):
        html = '<head><style>body{color:red<meta name="x" content="y"></head>'
        hasil, peringatan = perbaiki_tag_rawtext_tidak_tertutup(html)
        self.assertIn("</style>", hasil)
        self.assertIn('<meta name="x" content="y">', hasil)
        self.assertEqual(len(peringatan), 1)
        self.assertIn("<style>", peringatan[0])

    def test_script_tidak_tertutup_dipotong_sebelum_tag_berikutnya(self):
        html = "<head><script>var x=1;<h1>Judul</h1></head>"
        hasil, peringatan = perbaiki_tag_rawtext_tidak_tertutup(html)
        self.assertIn("</script>", hasil)
        self.assertIn("<h1>Judul</h1>", hasil)
        self.assertEqual(len(peringatan), 1)
        self.assertIn("<script>", peringatan[0])

    def test_textarea_tidak_tertutup_dipotong_sebelum_tag_berikutnya(self):
        html = "<body><textarea>Contoh isi<h1>Judul</h1></body>"
        hasil, peringatan = perbaiki_tag_rawtext_tidak_tertutup(html)
        self.assertIn("</textarea>", hasil)
        self.assertIn("<h1>Judul</h1>", hasil)
        self.assertEqual(len(peringatan), 1)

    def test_tanpa_elemen_rawtext_sama_sekali(self):
        html = "<html><body><h1>Judul</h1><p>Teks biasa.</p></body></html>"
        hasil, peringatan = perbaiki_tag_rawtext_tidak_tertutup(html)
        self.assertEqual(hasil, html)
        self.assertEqual(peringatan, [])

    def test_dua_elemen_rawtext_tidak_tertutup_dua_peringatan(self):
        html = (
            "<head><title>Judul Toko"
            '<style>body{color:blue'
            '<meta name="description" content="Deskripsi toko"></head>'
        )
        hasil, peringatan = perbaiki_tag_rawtext_tidak_tertutup(html)
        self.assertEqual(len(peringatan), 2)
        self.assertIn("</title>", hasil)
        self.assertIn("</style>", hasil)
        self.assertIn('<meta name="description" content="Deskripsi toko">', hasil)


class TesAnalisisLengkapIntegrasi(unittest.TestCase):
    def _tulis_dan_analisis(self, isi_teks, **kwargs):
        f = tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False, encoding="utf-8")
        f.write(isi_teks)
        f.close()
        return analisis_lengkap(f.name, **kwargs)

    def test_html_normal_lengkap(self):
        hasil = self._tulis_dan_analisis(HTML_NORMAL, kata_kunci="keripik pedas bandung", url="https://tokorenyahjaya.com/produk/keripik-pedas-bandung")
        self.assertEqual(hasil["title"]["status"], "PAS")
        self.assertEqual(hasil["heading"]["jumlah_h1"], 1)
        self.assertEqual(hasil["gambar"]["total"], 2)
        self.assertEqual(len(hasil["gambar"]["tanpa_atribut_alt"]), 1)
        self.assertTrue(hasil["canonical"]["ada"])
        self.assertTrue(hasil["canonical"]["sama_dengan_url"])
        self.assertEqual(len(hasil["json_ld"]), 1)
        self.assertTrue(hasil["json_ld"][0]["valid"])
        self.assertTrue(hasil["kata_kunci"]["di_title"])
        # 2 tautan bermasalah: "#" dan javascript:void(0)
        self.assertEqual(len(hasil["tautan"]["bermasalah"]), 2)

    def test_html_rusak_tag_title_tidak_ditutup_tetap_diekstrak_dengan_peringatan(self):
        # HTML_RUSAK sengaja punya <title> tanpa </title> (kesalahan umum
        # kalau pengguna menyalin "Lihat Sumber Halaman" secara terpotong).
        # Regresi S1 (temuan uji independen 2026-09-25): sebelum diperbaiki,
        # html.parser stdlib diam-diam menelan SISA SELURUH DOKUMEN sebagai
        # isi <title> tanpa peringatan apa pun, sehingga meta description,
        # H1, gambar, dan JSON-LD ikut hilang total tanpa jejak. Sekarang
        # WAJIB: (1) title/meta/heading/gambar tetap terbaca dengan benar,
        # DAN (2) peringatan eksplisit "HTML rusak" muncul di hasil.
        hasil = self._tulis_dan_analisis(HTML_RUSAK)
        self.assertTrue(hasil["title"]["ada"])
        self.assertEqual(hasil["title"]["teks"], "Toko Servis AC Bekasi")
        self.assertTrue(hasil["meta_description"]["ada"])
        self.assertIn("Servis AC", hasil["meta_description"]["teks"])
        self.assertGreaterEqual(hasil["heading"]["total"], 1)
        self.assertEqual(hasil["gambar"]["total"], 1)
        self.assertTrue(any("title" in p and "tidak ditutup" in p
                             for p in hasil["peringatan_html_rusak"]))

    def test_html_style_tidak_ditutup_tetap_diekstrak_dengan_peringatan(self):
        html = (
            '<html><head><title>Toko OK</title><style>body{color:red\n'
            '<meta name="description" content="Deskripsi toko yang seharusnya tetap terbaca meski style di atasnya rusak, cukup panjang.">'
            "<h1>Judul Utama Toko</h1></body></html>"
        )
        hasil = self._tulis_dan_analisis(html)
        self.assertEqual(hasil["title"]["teks"], "Toko OK")
        self.assertTrue(hasil["meta_description"]["ada"])
        self.assertEqual(hasil["heading"]["jumlah_h1"], 1)
        self.assertTrue(any("style" in p and "tidak ditutup" in p
                             for p in hasil["peringatan_html_rusak"]))

    def test_html_script_tidak_ditutup_tetap_diekstrak_dengan_peringatan(self):
        html = (
            "<html><head><title>Toko Skrip</title>"
            '<script>var x = 1;\n'
            '<h1>Judul Sesudah Skrip Rusak</h1></body></html>'
        )
        hasil = self._tulis_dan_analisis(html)
        self.assertEqual(hasil["title"]["teks"], "Toko Skrip")
        self.assertEqual(hasil["heading"]["jumlah_h1"], 1)
        self.assertTrue(any("script" in p and "tidak ditutup" in p
                             for p in hasil["peringatan_html_rusak"]))

    def test_html_normal_tidak_ada_peringatan_html_rusak(self):
        hasil = self._tulis_dan_analisis(HTML_NORMAL)
        self.assertEqual(hasil["peringatan_html_rusak"], [])

    def test_html_tanpa_seo_apapun(self):
        hasil = self._tulis_dan_analisis(HTML_TANPA_APAPUN)
        self.assertEqual(hasil["title"]["status"], "KOSONG")
        self.assertEqual(hasil["meta_description"]["status"], "KOSONG")
        self.assertEqual(hasil["heading"]["jumlah_h1"], 0)
        self.assertFalse(hasil["canonical"]["ada"])
        self.assertEqual(hasil["json_ld"], [])


if __name__ == "__main__":
    unittest.main()
