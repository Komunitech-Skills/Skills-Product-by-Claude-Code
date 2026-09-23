#!/usr/bin/env python3
"""
uji_validasi.py — Uji regresi untuk scripts/validasi_html.py.

Menguji bahwa validator:
- MELULUSKAN file HTML presentasi yang benar (termasuk yang padat teks -> peringatan saja).
- MENGGAGALKAN (ERROR, exit 1) setiap pola file rusak yang pernah lolos validator lama,
  ditambah kasus baru. Minimal 13 file rusak diuji, sesuai temuan penguji independen
  di examples/HASIL-UJI.md (lihat juga /tmp/uji-presentasi-instan/rusak/ pada sesi uji).

Jalankan:
    python3 tests/uji_validasi.py
    python3 -m unittest tests.uji_validasi -v

Hanya memakai pustaka standar Python (unittest, tempfile, pathlib). Tidak ada jaringan.
"""

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

FOLDER_SKILL = Path(__file__).resolve().parent.parent
SCRIPT = FOLDER_SKILL / "scripts" / "validasi_html.py"

_spec = importlib.util.spec_from_file_location("validasi_html", SCRIPT)
validasi_html = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(validasi_html)


# Dokumen dasar yang BENAR: satu file HTML mandiri, ada @page dengan size,
# @media print, 3 slide, tanpa rujukan internet, gambar berupa data: URI.
DASAR_BENAR = """<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Uji Presentasi</title>
<style>
  :root { --warna-aksen: #2563eb; }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  .slide { width: 1920px; height: 1080px; }
  @page { size: 1920px 1080px; margin: 0; }
  @media print {
    * { -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; }
    .slide { break-after: page; page-break-after: always; }
    .kontrol { display: none !important; }
  }
</style>
</head>
<body>
<main class="panggung">
  <section class="slide aktif">
    <h1>Judul Presentasi Uji</h1>
    <p>Anak judul singkat untuk uji coba validator.</p>
    <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII=" alt="logo">
  </section>
  <section class="slide">
    <h2>Isi Singkat</h2>
    <p>Beberapa poin singkat yang jelas dan tidak berlebihan panjangnya untuk satu slide.</p>
  </section>
  <section class="slide">
    <h2>Penutup</h2>
    <p>Terima kasih. Hubungi kami untuk info lebih lanjut mengenai penawaran ini.</p>
  </section>
</main>
<div class="kontrol"><button>‹</button><span>1 / 3</span><button>›</button></div>
<script>
  // navigasi lokal saja, tidak ada permintaan jaringan
  document.addEventListener('keydown', function (e) {});
</script>
</body>
</html>
"""


def tulis_dan_validasi(html: str):
    """Tulis `html` ke file sementara lalu jalankan validasi_html.validasi()."""
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html)
        path = Path(f.name)
    try:
        hasil, error_fatal = validasi_html.validasi(path, maks_kata_slide=70)
    finally:
        path.unlink(missing_ok=True)
    return hasil, error_fatal


class UjiFileBenar(unittest.TestCase):
    def test_dokumen_dasar_lulus(self):
        hasil, _ = tulis_dan_validasi(DASAR_BENAR)
        self.assertIsNotNone(hasil)
        self.assertTrue(hasil["valid"], msg=hasil["error"])
        self.assertEqual(hasil["error"], [])

    def test_slide_padat_tetap_lulus_dengan_peringatan(self):
        # Konten sangat panjang -> harus tetap LULUS (hanya peringatan jumlah kata),
        # bukan GAGAL, karena ini bukan pelanggaran keras.
        kata_panjang = " ".join(["kata"] * 200)
        html = DASAR_BENAR.replace(
            "<p>Beberapa poin singkat yang jelas dan tidak berlebihan panjangnya untuk satu slide.</p>",
            f"<p>{kata_panjang}</p>",
        )
        hasil, _ = tulis_dan_validasi(html)
        self.assertTrue(hasil["valid"])
        self.assertTrue(any("kata" in p for p in hasil["peringatan"]))

    def test_tautan_wa_me_lulus_dengan_peringatan(self):
        # Tautan <a href> ke internet (mis. wa.me) HANYA peringatan, bukan error —
        # ini navigasi, bukan pemuatan sumber daya, jadi file tetap LULUS.
        html = DASAR_BENAR.replace(
            "<h2>Isi Singkat</h2>",
            '<h2>Isi Singkat</h2><p><a href="https://wa.me/6281234567890">Hubungi via WhatsApp</a></p>',
        )
        hasil, _ = tulis_dan_validasi(html)
        self.assertTrue(hasil["valid"], msg=hasil["error"])
        self.assertEqual(hasil["error"], [])
        self.assertTrue(any("wa.me" in p for p in hasil["peringatan"]))

    def test_tema_gelap_kontras_cukup_lulus(self):
        # Tema Hitam Emas Premium dengan --warna-teks-lembut yang benar (#cfc8b8) harus LULUS.
        html = DASAR_BENAR.replace(
            "--warna-aksen: #2563eb;",
            "--warna-aksen: #c9a227; --warna-latar-slide: #111111; --warna-teks: #f5f1e6; "
            "--warna-teks-lembut: #cfc8b8;",
        )
        hasil, _ = tulis_dan_validasi(html)
        self.assertTrue(hasil["valid"], msg=hasil["error"])


class UjiFileRusakHarusGagal(unittest.TestCase):
    """Setiap kasus di sini WAJIB membuat validator GAGAL (error tidak kosong)."""

    def _pastikan_gagal(self, html: str, petunjuk_kata_kunci: str = None):
        hasil, error_fatal = tulis_dan_validasi(html)
        if hasil is None:
            self.fail(f"File tidak terbaca sama sekali: {error_fatal}")
        self.assertFalse(hasil["valid"], msg="Seharusnya GAGAL tapi malah LULUS")
        self.assertTrue(len(hasil["error"]) >= 1)
        if petunjuk_kata_kunci:
            gabungan = " ".join(hasil["error"]).lower()
            self.assertIn(petunjuk_kata_kunci.lower(), gabungan)

    # 1. Tanpa @page sama sekali
    def test_01_tanpa_page(self):
        html = DASAR_BENAR.replace("@page { size: 1920px 1080px; margin: 0; }", "")
        self._pastikan_gagal(html, "@page")

    # 2. @page ada tapi tanpa 'size'
    def test_02_page_tanpa_size(self):
        html = DASAR_BENAR.replace("@page { size: 1920px 1080px; margin: 0; }", "@page { margin: 0; }")
        self._pastikan_gagal(html, "@page")

    # 3. Tanpa @media print sama sekali
    def test_03_tanpa_media_print(self):
        import re
        html = re.sub(r"@media print \{.*?\n  \}", "", DASAR_BENAR, flags=re.DOTALL)
        self._pastikan_gagal(html, "@media print")

    # 4. File kosong
    def test_04_file_kosong(self):
        self._pastikan_gagal("")

    # 5. Tanpa class="slide" sama sekali
    def test_05_tanpa_slide(self):
        html = DASAR_BENAR.replace('class="slide aktif"', "").replace('class="slide"', "")
        self._pastikan_gagal(html, "slide")

    # 6. href ke Google Fonts (berkutip)
    def test_06_link_google_fonts(self):
        html = DASAR_BENAR.replace(
            "</head>",
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto"></head>',
        )
        self._pastikan_gagal(html)

    # 7. href TANPA tanda kutip (lolos di validator lama)
    def test_07_href_tanpa_kutip(self):
        html = DASAR_BENAR.replace(
            "</head>", "<link rel=stylesheet href=https://cdn.example.com/x.css></head>"
        )
        self._pastikan_gagal(html)

    # 8. srcset ke internet (lolos di validator lama)
    def test_08_srcset_internet(self):
        html = DASAR_BENAR.replace(
            "<h1>Judul Presentasi Uji</h1>",
            '<h1>Judul Presentasi Uji</h1><img srcset="https://example.com/a.png 2x">',
        )
        self._pastikan_gagal(html)

    # 9. CSS url() protocol-relative (//cdn...) (lolos di validator lama)
    def test_09_css_url_protocol_relative(self):
        html = DASAR_BENAR.replace(
            "</style>", '.x{background:url("//cdn.example.com/bg.png")}</style>'
        )
        self._pastikan_gagal(html)

    # 10. CSS url() http:// langsung tanpa kutip
    def test_10_css_url_http_tanpa_kutip(self):
        html = DASAR_BENAR.replace(
            "</style>", ".y{background:url(http://cdn.example.com/bg.png)}</style>"
        )
        self._pastikan_gagal(html)

    # 11. @import CSS ke internet
    def test_11_css_import(self):
        html = DASAR_BENAR.replace("</style>", '@import url("https://fonts.googleapis.com/x");</style>')
        self._pastikan_gagal(html)

    # 12. fetch() ke internet di JavaScript (lolos di validator lama)
    def test_12_fetch_javascript(self):
        html = DASAR_BENAR.replace("<script>", '<script>fetch("https://example.com/track");')
        self._pastikan_gagal(html)

    # 13. XMLHttpRequest .open() ke internet
    def test_13_xhr_open(self):
        html = DASAR_BENAR.replace(
            "<script>",
            '<script>var x = new XMLHttpRequest(); x.open("GET", "https://example.com/track");',
        )
        self._pastikan_gagal(html)

    # 14. import() dinamis ke internet
    def test_14_import_dinamis(self):
        html = DASAR_BENAR.replace("<script>", '<script>import("https://example.com/modul.js");')
        self._pastikan_gagal(html)

    # 15. <img src> path lokal Windows (lolos di validator lama) — rusak saat dikirim via WA
    def test_15_img_src_path_lokal_windows(self):
        html = DASAR_BENAR.replace(
            'src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="',
            r'src="C:\Users\budi\Desktop\logo.png"',
        )
        self._pastikan_gagal(html, "data:")

    # 16. <img src> path relatif (lolos di validator lama)
    def test_16_img_src_path_relatif(self):
        html = DASAR_BENAR.replace(
            'src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="',
            'src="logo.png"',
        )
        self._pastikan_gagal(html, "data:")

    # 17. File bukan UTF-8 -> tetap harus dilaporkan sebagai gagal terbaca (bukan lolos diam-diam)
    def test_17_bukan_utf8(self):
        with tempfile.NamedTemporaryFile("wb", suffix=".html", delete=False) as f:
            f.write(b"\xff\xfe" + "Judul".encode("utf-16-le"))
            path = Path(f.name)
        try:
            hasil, error_fatal = validasi_html.validasi(path, maks_kata_slide=70)
        finally:
            path.unlink(missing_ok=True)
        self.assertIsNone(hasil)
        self.assertTrue(len(error_fatal) >= 1)

    # 18. File tidak ada
    def test_18_file_tidak_ada(self):
        path = Path("/tidak/ada/file/ini.html")
        hasil, error_fatal = validasi_html.validasi(path, maks_kata_slide=70)
        self.assertIsNone(hasil)
        self.assertTrue(len(error_fatal) >= 1)

    # 19. Tema gelap tapi --warna-teks-lembut masih memakai default terang-lemah
    # (#475569 di atas latar #111111 -> kontras cuma ~2,5:1, di bawah 4,5:1 WCAG)
    def test_19_kontras_tema_gelap_kurang(self):
        html = DASAR_BENAR.replace(
            "--warna-aksen: #2563eb;",
            "--warna-aksen: #c9a227; --warna-latar-slide: #111111; --warna-teks: #f5f1e6; "
            "--warna-teks-lembut: #475569;",
        )
        self._pastikan_gagal(html, "kontras")

    # 20. CSS url() menunjuk file lokal (mis. foto-toko.jpg) — rusak saat dikirim
    def test_20_css_url_lokal(self):
        html = DASAR_BENAR.replace(
            "</style>", '.z{background:url("foto-toko.jpg")}</style>'
        )
        self._pastikan_gagal(html, "url")

    # 21. <video src="promo.mp4"> lokal — rusak saat dikirim ke perangkat lain
    def test_21_video_src_lokal(self):
        html = DASAR_BENAR.replace(
            "<h2>Isi Singkat</h2>",
            '<h2>Isi Singkat</h2><video src="promo.mp4" controls></video>',
        )
        self._pastikan_gagal(html, "video")

    # 22. <source src="..."> lokal di dalam <video>/<audio> — rusak saat dikirim
    def test_22_source_src_lokal(self):
        html = DASAR_BENAR.replace(
            "<h2>Isi Singkat</h2>",
            '<h2>Isi Singkat</h2><video controls><source src="promo.mp4" type="video/mp4"></video>',
        )
        self._pastikan_gagal(html, "source")


if __name__ == "__main__":
    unittest.main(verbosity=2)
