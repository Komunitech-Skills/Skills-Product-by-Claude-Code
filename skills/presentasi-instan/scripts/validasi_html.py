#!/usr/bin/env python3
"""
validasi_html.py — Memeriksa file presentasi HTML hasil skill `presentasi-instan`.

Skill ini menghasilkan SATU file HTML mandiri (tanpa internet, tanpa instalasi).
Script ini memverifikasi itu secara otomatis:
  1. Tidak ada rujukan ke internet yang MEMUAT sumber daya (CDN, Google Fonts,
     src/srcset/link href/@import/url()/fetch/XHR/import() http(s)://, dsb.) — wajib
     supaya file benar-benar bisa dibuka tanpa koneksi internet. Tautan navigasi
     <a href="https://..."> (mis. wa.me) HANYA peringatan, bukan error.
  2. Gambar/video/audio/CSS url() dengan path lokal (bukan data: URI) — ERROR, karena
     akan rusak (media hilang) saat file dikirim ke perangkat lain.
  3. Jumlah slide terdeteksi (class="slide").
  4. Slide dengan teks terlalu panjang (berpotensi tidak terbaca di HP / saat
     dipresentasikan) ditandai sebagai peringatan.
  5. Kelengkapan dasar (DOCTYPE, viewport meta, @page dengan size, CSS cetak untuk PDF).
  6. Kontras warna teks (--warna-teks / --warna-teks-lembut) terhadap latar slide,
     dihitung dengan rumus WCAG — ERROR jika di bawah 4,5:1.

Hanya memakai pustaka standar Python (3.8+). Tidak membuka koneksi jaringan apa pun.

Cara pakai:
    python3 validasi_html.py presentasi.html
    python3 validasi_html.py presentasi.html --maks-kata-slide 60 --json

Keluaran: ringkasan teks (default) atau JSON (--json).
Exit code: 0 jika lulus (boleh ada peringatan), 1 jika ada ERROR yang wajib diperbaiki,
2 jika file tidak ditemukan / tidak bisa dibaca.
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Pola yang menandakan file mencoba MEMUAT SUMBER DAYA dari internet (gambar, font,
# CSS, script, data) — ini WAJIB gagal karena file harus tetap bisa dibuka offline.
# src/srcset dicek dengan ATAU tanpa tanda kutip, http(s):// ATAU protocol-relative
# (//...), supaya tidak bisa dilewati hanya dengan menghapus kutip. `href` TIDAK
# dimasukkan di sini — href pada <link> (pemuatan CSS/font) ditangani terpisah agar
# tetap ERROR, sedangkan href pada <a> (tautan navigasi, mis. wa.me) hanya PERINGATAN
# (lihat POLA_TAUTAN_A) karena tidak memuat apa pun saat file dibuka offline.
POLA_EKSTERNAL = [
    (r'(?:src|srcset)\s*=\s*["\']?(?:https?:)?//',
     "atribut src/srcset menunjuk ke URL internet (http(s):// atau //, dengan/tanpa tanda kutip)"),
    (r'<link\b[^>]*\bhref\s*=\s*["\']?(?:https?:)?//',
     "atribut href pada <link> menunjuk ke URL internet (memuat CSS/font dari internet)"),
    (r'@import\s+(?:url\()?["\']?(?:https?:)?//', "@import CSS memanggil URL internet"),
    (r'url\(\s*["\']?(?:https?:)?//', "CSS url() memanggil gambar/font dari internet (http(s):// atau //)"),
    (r'\bfetch\s*\(\s*["\']https?://', "kode JavaScript fetch() memanggil URL internet"),
    (r'\bimport\s*\(\s*["\']https?://', "kode JavaScript import() dinamis memanggil URL internet"),
    (r'\.open\s*\(\s*["\'][A-Za-z]+["\']\s*,\s*["\']https?://',
     "kode JavaScript XMLHttpRequest .open() memanggil URL internet"),
    (r'fonts\.googleapis\.com|fonts\.gstatic\.com|api\.fontshare\.com|cdn\.jsdelivr\.net|cdnjs\.cloudflare\.com|unpkg\.com',
     "menyebut layanan CDN/font online (Google Fonts, Fontshare, jsdelivr, cdnjs, unpkg)"),
]

# Tautan <a href="..."> ke internet (mis. wa.me, situs usaha) — ini NAVIGASI, bukan
# pemuatan sumber daya, jadi hanya peringatan (boleh ada, wajar untuk kontak WA/website).
POLA_TAUTAN_A = re.compile(r'<a\b[^>]*\bhref\s*=\s*["\']?((?:https?:)?//[^"\'\s>]+)', re.IGNORECASE)

# Gambar/video/audio dengan src path lokal (bukan data: URI) rusak saat file dikirim
# ke perangkat lain (mis. lewat WA/email) — folder gambar terpisah biasanya tidak ikut terkirim.
POLA_MEDIA_SRC = re.compile(r'<(img|video|audio|source)\b[^>]*\bsrc\s*=\s*(["\']?)([^"\'\s>]+)\2', re.IGNORECASE)
POLA_CSS_URL = re.compile(r'url\(\s*(["\']?)([^)\'"]+)\1\s*\)', re.IGNORECASE)
POLA_PAGE_SIZE = re.compile(r'@page\s*\{[^}]*\bsize\s*:', re.IGNORECASE | re.DOTALL)

POLA_SLIDE = re.compile(r'<[a-zA-Z0-9]+[^>]*\bclass\s*=\s*"[^"]*\bslide\b[^"]*"[^>]*>', re.IGNORECASE)
POLA_TAG = re.compile(r'<[^>]+>')
POLA_SCRIPT_STYLE = re.compile(r'<(script|style)\b[^>]*>.*?</\1>', re.IGNORECASE | re.DOTALL)
POLA_ROOT = re.compile(r':root\s*\{([^}]*)\}', re.IGNORECASE | re.DOTALL)
POLA_VAR = re.compile(r'(--[a-zA-Z0-9-]+)\s*:\s*([^;]+);')


def _nilai_lokal(nilai: str) -> bool:
    """True jika `nilai` (src/url) adalah path lokal/relatif — bukan data:, bukan http(s)/protocol-relative."""
    n = nilai.strip().lower()
    if not n or n.startswith("data:") or n.startswith("#"):
        return False
    if n.startswith("http://") or n.startswith("https://") or n.startswith("//"):
        return False  # sudah ditangani sebagai rujukan internet di POLA_EKSTERNAL
    return True


# --- Cek kontras warna (WCAG 2.x) untuk --warna-teks / --warna-teks-lembut ---

def _hex_ke_rgb(warna: str):
    """Ubah '#rgb' atau '#rrggbb' jadi (r, g, b) 0-255, atau None jika bukan hex sederhana."""
    w = warna.strip()
    m = re.fullmatch(r'#([0-9a-fA-F]{3})', w)
    if m:
        h = m.group(1)
        return tuple(int(c * 2, 16) for c in h)
    m = re.fullmatch(r'#([0-9a-fA-F]{6})', w)
    if m:
        h = m.group(1)
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    return None


def _luminansi_relatif(rgb):
    def lin(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    return 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)


def rasio_kontras(warna1: str, warna2: str):
    """Rasio kontras WCAG antara dua warna hex, atau None jika salah satu bukan hex sederhana."""
    rgb1, rgb2 = _hex_ke_rgb(warna1), _hex_ke_rgb(warna2)
    if rgb1 is None or rgb2 is None:
        return None
    l1, l2 = _luminansi_relatif(rgb1), _luminansi_relatif(rgb2)
    l1, l2 = max(l1, l2), min(l1, l2)
    return (l1 + 0.05) / (l2 + 0.05)


def hitung_kata(teks_html_slide: str) -> int:
    """Hitung kira-kira jumlah kata yang benar-benar tampil di slide (buang tag & spasi)."""
    tanpa_script = POLA_SCRIPT_STYLE.sub(" ", teks_html_slide)
    tanpa_tag = POLA_TAG.sub(" ", tanpa_script)
    tanpa_tag = re.sub(r'&[a-zA-Z#0-9]+;', ' ', tanpa_tag)  # entitas HTML seperti &nbsp; &amp;
    kata = tanpa_tag.split()
    return len(kata)


def potong_slide(html: str):
    """Pecah dokumen jadi per-slide berdasarkan tag pembuka class="slide" (perkiraan sederhana,
    berbasis kemunculan tag pembuka berikutnya sebagai batas, bukan parser HTML penuh)."""
    batas = [m.start() for m in POLA_SLIDE.finditer(html)]
    if not batas:
        return []
    batas.append(len(html))
    return [html[batas[i]:batas[i + 1]] for i in range(len(batas) - 1)]


def validasi(path: Path, maks_kata_slide: int, maks_baris_kata_kunci: int = 8):
    if not path.exists():
        return None, ["File tidak ditemukan: %s" % path]
    try:
        html = path.read_text(encoding="utf-8", errors="strict")
    except UnicodeDecodeError as e:
        return None, ["File tidak bisa dibaca sebagai UTF-8 (%s). Simpan ulang file dengan encoding UTF-8." % e]
    except OSError as e:
        return None, ["Gagal membaca file: %s" % e]

    error = []
    peringatan = []

    # 1. Cek rujukan eksternal
    for pola, keterangan in POLA_EKSTERNAL:
        for m in re.finditer(pola, html, re.IGNORECASE):
            cuplikan = html[max(0, m.start() - 20):m.start() + 60].replace("\n", " ")
            error.append(f"Ditemukan rujukan internet ({keterangan}): ...{cuplikan}...")

    # 1b. Tautan <a href="..."> ke internet — navigasi, bukan pemuatan sumber daya,
    # jadi hanya PERINGATAN (mis. tautan wa.me/nomor untuk kontak, situs usaha).
    for m in POLA_TAUTAN_A.finditer(html):
        nilai_href = m.group(1)
        cuplikan = html[max(0, m.start()):m.start() + 90].replace("\n", " ")
        peringatan.append(
            f"Tautan <a href=\"...\"> menunjuk ke internet ({nilai_href}) — ini tautan navigasi (boleh ada, "
            f"tidak memuat apa pun saat file dibuka offline), tapi pastikan alamatnya benar sebelum dikirim: ...{cuplikan}..."
        )

    # 1c. Gambar/video/audio dengan src bukan data: URI (path lokal seperti C:\... atau
    # logo.png/promo.mp4) rusak begitu file HTML dikirim ke komputer/HP lain (mis. lewat WA/email).
    for m in POLA_MEDIA_SRC.finditer(html):
        tag, nilai_src = m.group(1).lower(), m.group(3)
        if _nilai_lokal(nilai_src):
            cuplikan = html[max(0, m.start() - 10):m.start() + 80].replace("\n", " ")
            error.append(
                f"<{tag} src=\"...\"> bukan data: URI (base64) — src=\"{nilai_src}\" adalah path lokal/relatif yang "
                f"akan rusak (media hilang) saat file dikirim ke perangkat lain. Ubah jadi base64: ...{cuplikan}..."
            )

    # 1d. CSS url("foto-lokal.jpg") — path lokal juga rusak saat file dikirim ke perangkat lain.
    for m in POLA_CSS_URL.finditer(html):
        nilai_url = m.group(2)
        if _nilai_lokal(nilai_url):
            cuplikan = html[max(0, m.start() - 10):m.start() + 80].replace("\n", " ")
            error.append(
                f"CSS url(\"...\") bukan data: URI — url(\"{nilai_url}\") adalah path lokal/relatif yang akan "
                f"rusak (gambar hilang) saat file dikirim ke perangkat lain. Ubah jadi base64: ...{cuplikan}..."
            )

    # 2. Kelengkapan dasar
    if "<!doctype html>" not in html.lower():
        peringatan.append("Tidak ada <!DOCTYPE html> di awal file — tambahkan agar browser merender dengan benar.")
    if 'name="viewport"' not in html and "name='viewport'" not in html:
        peringatan.append("Tidak ada meta viewport — tampilan di HP bisa tidak pas.")
    if "@media print" not in html:
        error.append("Tidak ada blok CSS @media print — 'Print ke PDF' tidak akan rapi satu slide per halaman.")
    if not POLA_PAGE_SIZE.search(html):
        error.append(
            "Tidak ada blok CSS @page dengan 'size' (mis. @page { size: 1920px 1080px; margin: 0; }) — "
            "tanpa ini, browser memakai ukuran kertas default (A4/Letter) sehingga sisi kanan slide 1920x1080 "
            "TERPOTONG saat dicetak ke PDF."
        )

    # 2b. Kontras warna teks vs latar slide (WCAG 2.x), dari variabel CSS di :root.
    m_root = POLA_ROOT.search(html)
    if m_root:
        variabel = dict(POLA_VAR.findall(m_root.group(1)))
        latar = variabel.get("--warna-latar-slide")
        for nama_var in ("--warna-teks", "--warna-teks-lembut"):
            teks = variabel.get(nama_var)
            if not latar or not teks:
                continue
            rasio = rasio_kontras(teks.strip(), latar.strip())
            if rasio is not None and rasio < 4.5:
                error.append(
                    f"Kontras warna kurang: {nama_var} ({teks.strip()}) terhadap --warna-latar-slide "
                    f"({latar.strip()}) hanya {rasio:.2f}:1 (minimal 4,5:1 menurut WCAG) — teks akan sulit "
                    "dibaca, terutama di latar gelap. Ganti warnanya, lihat aturan-desain.md #5."
                )

    # 3. Jumlah slide & panjang teks per slide
    potongan = potong_slide(html)
    jumlah_slide = len(potongan)
    if jumlah_slide == 0:
        error.append('Tidak ditemukan elemen dengan class="slide" — file ini sepertinya bukan hasil skill presentasi-instan.')
    else:
        if jumlah_slide < 3:
            peringatan.append(f"Hanya {jumlah_slide} slide terdeteksi — presentasi biasanya butuh minimal 3 (pembuka, isi, penutup).")
        if jumlah_slide > 40:
            peringatan.append(f"{jumlah_slide} slide terdeteksi — cukup banyak, pastikan tidak terlalu panjang untuk audiens.")

        slide_terlalu_padat = []
        for i, potong in enumerate(potongan, start=1):
            jumlah_kata = hitung_kata(potong)
            if jumlah_kata > maks_kata_slide:
                slide_terlalu_padat.append({"slide_ke": i, "jumlah_kata": jumlah_kata})
        if slide_terlalu_padat:
            daftar = ", ".join(f"#{s['slide_ke']} ({s['jumlah_kata']} kata)" for s in slide_terlalu_padat)
            peringatan.append(
                f"Slide dengan teks lebih dari {maks_kata_slide} kata (berisiko sulit dibaca di HP / saat presentasi): {daftar}. "
                "Pertimbangkan memecah jadi beberapa slide atau meringkas."
            )

    ukuran_kb = round(len(html.encode("utf-8")) / 1024, 1)
    if ukuran_kb > 5000:
        peringatan.append(f"Ukuran file {ukuran_kb} KB — cukup besar, kemungkinan ada gambar besar tertanam (base64). Pertimbangkan mengecilkan gambar.")

    hasil = {
        "file": str(path),
        "ukuran_kb": ukuran_kb,
        "jumlah_slide": jumlah_slide,
        "valid": len(error) == 0,
        "error": error,
        "peringatan": peringatan,
    }
    return hasil, error


def main():
    ap = argparse.ArgumentParser(description="Validasi file presentasi HTML mandiri dari skill presentasi-instan.")
    ap.add_argument("file_html", help="Path ke file .html hasil presentasi")
    ap.add_argument("--maks-kata-slide", type=int, default=70,
                     help="Ambang jumlah kata per slide sebelum diberi peringatan (default: 70)")
    ap.add_argument("--json", action="store_true", help="Keluarkan hasil sebagai JSON")
    args = ap.parse_args()

    path = Path(args.file_html)
    hasil, error_fatal = validasi(path, args.maks_kata_slide)

    if hasil is None:
        if args.json:
            print(json.dumps({"valid": False, "error": error_fatal}, ensure_ascii=False, indent=2))
        else:
            for e in error_fatal:
                print(f"ERROR: {e}")
        sys.exit(2)

    if args.json:
        print(json.dumps(hasil, ensure_ascii=False, indent=2))
    else:
        print(f"File: {hasil['file']}")
        print(f"Ukuran: {hasil['ukuran_kb']} KB")
        print(f"Jumlah slide: {hasil['jumlah_slide']}")
        print(f"Status: {'LULUS' if hasil['valid'] else 'GAGAL — perlu diperbaiki'}")
        if hasil["error"]:
            print("\nERROR (wajib diperbaiki):")
            for e in hasil["error"]:
                print(f"  - {e}")
        if hasil["peringatan"]:
            print("\nPeringatan (sebaiknya diperbaiki):")
            for p in hasil["peringatan"]:
                print(f"  - {p}")
        if not hasil["error"] and not hasil["peringatan"]:
            print("\nTidak ada masalah ditemukan.")

    sys.exit(0 if hasil["valid"] else 1)


if __name__ == "__main__":
    main()
