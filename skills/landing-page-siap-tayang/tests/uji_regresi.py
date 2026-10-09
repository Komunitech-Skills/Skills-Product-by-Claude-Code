#!/usr/bin/env python3
"""Uji regresi cek_landing.py. Jalankan: python3 tests/uji_regresi.py (Windows: python / py)."""
import os
import sys
import tempfile
import unittest
from pathlib import Path

RAKIT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAKIT / "scripts"))
import cek_landing as c  # noqa: E402

BAIK = """<!DOCTYPE html><html lang="id"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Keripik Pedas Bu Dewi</title><meta name="description" content="Keripik singkong pedas renyah, dikirim ke seluruh Indonesia.">
<style>.wa-melayang{position:fixed;right:10px;bottom:10px}</style></head>
<body><h1>Keripik Pedas Renyah</h1>
<a class="tombol cta" href="https://wa.me/6281234567890?text=Halo%20saya%20mau%20pesan">Pesan</a>
<a class="wa-melayang" href="https://wa.me/6281234567890">Chat</a>
<img src="data:image/gif;base64,R0lGODlhAQABAAAAACw=" alt="foto produk"></body></html>"""


def cek(teks, putih=()):
    return c.periksa(teks, len(teks.encode()), putih)


def gagal(h):
    return [m for ok, m in h if not ok]


class Tes(unittest.TestCase):
    def test_baik_lolos(self):
        self.assertEqual(gagal(cek(BAIK)), [])

    def test_template_gagal_karena_isian(self):
        t = (RAKIT / "templates" / "index-dasar.html").read_text(encoding="utf-8")
        g = gagal(cek(t))
        self.assertTrue(any("[isian" in m for m in g))
        # kerangka sendiri harus punya struktur benar selain isian & format wa
        self.assertFalse(any("viewport" in m.lower() for m in g))
        self.assertFalse(any("sumber luar" in m for m in g))
        self.assertFalse(any("pelacak" in m for m in g))

    def test_template_setelah_isian_lolos(self):
        t = (RAKIT / "templates" / "index-dasar.html").read_text(encoding="utf-8")
        import re
        t = t.replace("62[isian: nomor tanpa 0 di depan]", "6281200001111")
        t = re.sub(r"\[isian:[^\]]*\]", "Contoh", t)
        self.assertEqual(gagal(cek(t)), [])

    def test_buruk(self):
        buruk = ('<html><head><script src="https://www.googletagmanager.com/gtag/js?id=G-1"></script>'
                 '<script>fbq("init","1")</script></head><body><h1>A</h1><h1>B</h1>'
                 '<a class="btn" href="https://wa.me/08123456789">Chat</a>[isian: testimoni]'
                 '<img src="https://cdn.example.com/a.jpg"></body></html>')
        g = " | ".join(gagal(cek(buruk)))
        for k in ("title", "description", "viewport", "lang", "h1", "wa.me", "[isian", "sumber luar", "pelacak", "alt"):
            self.assertIn(k, g, k)

    def test_wa_format(self):
        for url, sah in [("https://wa.me/6281234567890", True), ("https://wa.me/+6281234567890", False),
                         ("https://wa.me/081234567890", False), ("https://wa.me/62812", False),
                         ("http://wa.me/6281234567890", False)]:
            self.assertEqual(bool(c.POLA_WA.match(url)), sah, url)

    def test_putih(self):
        t = BAIK.replace("</head>", '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter"></head>')
        self.assertTrue(any("sumber luar" in m for m in gagal(cek(t))))
        self.assertFalse(any("sumber luar" in m for m in gagal(cek(t, ["fonts.googleapis.com"]))))

    def test_ukuran(self):
        t = BAIK + "<!--" + "x" * (310 * 1024) + "-->"
        self.assertTrue(any("300 KB" in m for m in gagal(cek(t))))

    def test_berkas(self):
        d = tempfile.mkdtemp()
        p = os.path.join(d, "kosong.html")
        open(p, "w").close()
        self.assertEqual(c.main([p]), 1)
        self.assertEqual(c.main([os.path.join(d, "tidak-ada.html")]), 2)
        b = os.path.join(d, "baik.html")
        open(b, "w", encoding="utf-8").write(BAIK)
        self.assertEqual(c.main([b]), 0)
        r = os.path.join(d, "rusak.html")
        open(r, "wb").write(b"\xff\xfe<<<html><a href=\x00")
        self.assertIn(c.main([r]), (0, 1))  # tidak boleh crash


if __name__ == "__main__":
    unittest.main()
