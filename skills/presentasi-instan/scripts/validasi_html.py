#!/usr/bin/env python3
"""
validasi_html.py — Memeriksa file presentasi HTML hasil skill `presentasi-instan`.

Skill ini menghasilkan SATU file HTML mandiri (tanpa internet, tanpa instalasi).
Script ini memverifikasi itu secara otomatis:
  1. Tidak ada rujukan ke internet (CDN, Google Fonts, http(s)://, dsb.) — wajib
     supaya file benar-benar bisa dibuka tanpa koneksi internet.
  2. Jumlah slide terdeteksi (class="slide").
  3. Slide dengan teks terlalu panjang (berpotensi tidak terbaca di HP / saat
     dipresentasikan) ditandai sebagai peringatan.
  4. Kelengkapan dasar (DOCTYPE, viewport meta, CSS cetak untuk PDF).

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

# Pola yang menandakan file mencoba mengambil sesuatu dari internet.
POLA_EKSTERNAL = [
    (r'(?:href|src)\s*=\s*["\']https?://', "atribut href/src menunjuk ke URL internet (http/https)"),
    (r'(?:href|src)\s*=\s*["\']//', "atribut href/src memakai protocol-relative URL (//...), ini tetap memanggil internet"),
    (r'@import\s+(?:url\()?["\']?https?://', "@import CSS memanggil URL internet"),
    (r'url\(\s*["\']?https?://', "CSS url() memanggil gambar/font dari internet"),
    (r'fonts\.googleapis\.com|fonts\.gstatic\.com|api\.fontshare\.com|cdn\.jsdelivr\.net|cdnjs\.cloudflare\.com|unpkg\.com',
     "menyebut layanan CDN/font online (Google Fonts, Fontshare, jsdelivr, cdnjs, unpkg)"),
]

POLA_SLIDE = re.compile(r'<[a-zA-Z0-9]+[^>]*\bclass\s*=\s*"[^"]*\bslide\b[^"]*"[^>]*>', re.IGNORECASE)
POLA_TAG = re.compile(r'<[^>]+>')
POLA_SCRIPT_STYLE = re.compile(r'<(script|style)\b[^>]*>.*?</\1>', re.IGNORECASE | re.DOTALL)


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

    # 2. Kelengkapan dasar
    if "<!doctype html>" not in html.lower():
        peringatan.append("Tidak ada <!DOCTYPE html> di awal file — tambahkan agar browser merender dengan benar.")
    if 'name="viewport"' not in html and "name='viewport'" not in html:
        peringatan.append("Tidak ada meta viewport — tampilan di HP bisa tidak pas.")
    if "@media print" not in html:
        error.append("Tidak ada blok CSS @media print — 'Print ke PDF' tidak akan rapi satu slide per halaman.")

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
