#!/usr/bin/env python3
"""Cek konsistensi sitasi pada draf artikel/tulisan (format [n] + Daftar Pustaka).

Hanya library standar Python 3.8+. Tidak ada akses jaringan. Tidak memverifikasi apakah
sebuah sumber BENAR ADA atau ISINYA BENAR — itu tanggung jawab manusia/agent yang menulis
(baca isi sumber sebelum mengutip). Script ini hanya memeriksa KONSISTENSI MEKANIS:

  1. Setiap kutipan [n] di badan teks punya entri bernomor sama di Daftar Pustaka.
  2. Setiap entri di Daftar Pustaka dipakai minimal sekali di badan teks (entri menganggur
     ditandai sebagai peringatan, bukan error keras).
  3. Tidak ada URL yang muncul di dua nomor entri berbeda (duplikat).
  4. HEURISTIK (bukan deteksi pasti): baris yang mengandung angka/persen/Rupiah tapi TIDAK
     punya [n] di baris yang sama ditandai untuk dicek manual — bisa jadi memang opini/tidak
     butuh sumber, bisa juga statistik yang lupa dikutip. Perbaikan tetap keputusan manusia.

Pemakaian:
    python3 cek_sitasi.py draf.md
    python3 cek_sitasi.py draf.md --json
    echo "..." | python3 cek_sitasi.py -

Keluar dengan kode 0 bila tidak ada error keras (poin 1 & 3), kode 1 bila ada error keras
(peringatan poin 2 & 4 tidak menggagalkan exit code -- itu untuk ditinjau manusia).
"""
import argparse
import json
import re
import sys

# [1] atau [1][3] atau [1, 2] di badan teks (bukan di baris Daftar Pustaka)
POLA_KUTIPAN_TEKS = re.compile(r"\[(\d+(?:\s*,\s*\d+)*)\]")
# Baris entri daftar pustaka: "[1] ..." di awal baris (boleh didahului spasi/indentasi)
POLA_ENTRI_PUSTAKA = re.compile(r"^\s*\[(\d+)\]\s+(.*)$")
POLA_JUDUL_PUSTAKA = re.compile(r"^\s{0,3}#{1,6}\s*daftar\s+pustaka\s*$", re.IGNORECASE)
POLA_URL = re.compile(r"https?://[^\s)\]\"']+")
# Heuristik: angka desimal/ribuan, persen, atau Rupiah
POLA_ANGKA_STATISTIK = re.compile(
    r"(Rp\s?[\d.,]+|(?<![\w.])\d{1,3}(?:[.,]\d{3})*(?:[.,]\d+)?\s?%|(?<![\w.,])\d+(?:[.,]\d+)?\s*(?:persen|juta|miliar|milyar|triliun|ribu)\b)",
    re.IGNORECASE,
)


def pisahkan_teks_dan_pustaka(isi):
    """Kembalikan (baris_badan_teks, baris_daftar_pustaka) -- daftar pustaka dimulai dari
    heading '## Daftar Pustaka' (atau variasi level heading) sampai akhir file."""
    baris = isi.splitlines()
    idx_mulai = None
    for i, b in enumerate(baris):
        if POLA_JUDUL_PUSTAKA.match(b):
            idx_mulai = i
            break
    if idx_mulai is None:
        return baris, []
    return baris[:idx_mulai], baris[idx_mulai + 1:]


def ambil_kutipan_teks(baris_badan):
    """dict nomor -> daftar nomor baris (1-based, relatif badan teks) tempat kutipan muncul."""
    pemakaian = {}
    for i, b in enumerate(baris_badan, start=1):
        for m in POLA_KUTIPAN_TEKS.finditer(b):
            for n in re.split(r"\s*,\s*", m.group(1)):
                pemakaian.setdefault(int(n), []).append(i)
    return pemakaian


def ambil_entri_pustaka(baris_pustaka):
    """dict nomor -> {"teks": ..., "url": ... atau None, "baris": nomor baris relatif}.

    Entri boleh melebar ke baris berikutnya (format yang dicontohkan di
    references/gaya-sitasi.md): baris lanjutan adalah baris tidak kosong yang TIDAK diawali
    '[n]' — teks dan pencarian URL-nya digabungkan ke entri [n] terakhir sebelum baris itu."""
    entri = {}
    duplikat_nomor = []
    urutan_nomor = []  # urutan kemunculan nomor, untuk tahu entri "terakhir" saat digabung
    for i, b in enumerate(baris_pustaka, start=1):
        m = POLA_ENTRI_PUSTAKA.match(b)
        if m:
            n = int(m.group(1))
            if n in entri:
                duplikat_nomor.append(n)
            entri[n] = {"teks": m.group(2).strip(), "baris": i}
            urutan_nomor.append(n)
            continue
        if not b.strip():
            continue  # baris kosong tidak dianggap lanjutan
        if urutan_nomor:
            n_terakhir = urutan_nomor[-1]
            entri[n_terakhir]["teks"] += " " + b.strip()

    for e in entri.values():
        url_m = POLA_URL.search(e["teks"])
        e["url"] = url_m.group(0) if url_m else None
    return entri, duplikat_nomor


def cek_url_duplikat(entri):
    per_url = {}
    for n, e in entri.items():
        if e["url"]:
            per_url.setdefault(e["url"], []).append(n)
    return {u: ns for u, ns in per_url.items() if len(ns) > 1}


def cek_statistik_tanpa_kutipan(baris_badan):
    temuan = []
    for i, b in enumerate(baris_badan, start=1):
        for m in POLA_ANGKA_STATISTIK.finditer(b):
            # apakah ada [n] di baris yang sama? (heuristik per baris, bukan per kalimat persis)
            if not POLA_KUTIPAN_TEKS.search(b):
                temuan.append({"baris": i, "cuplikan": b.strip()[:160], "angka": m.group(0)})
                break  # satu temuan cukup per baris
    return temuan


def periksa(isi):
    baris_badan, baris_pustaka = pisahkan_teks_dan_pustaka(isi)
    pemakaian = ambil_kutipan_teks(baris_badan)
    entri, duplikat_nomor = ambil_entri_pustaka(baris_pustaka)

    error = []
    peringatan = []

    if not baris_pustaka:
        error.append("Tidak ditemukan bagian 'Daftar Pustaka' (heading '## Daftar Pustaka' atau serupa).")

    nomor_dipakai = set(pemakaian)
    nomor_ada = set(entri)

    hilang_di_pustaka = sorted(nomor_dipakai - nomor_ada)
    for n in hilang_di_pustaka:
        error.append(f"Kutipan [{n}] dipakai di teks (baris {pemakaian[n]}) tapi tidak ada di Daftar Pustaka.")

    if duplikat_nomor:
        for n in sorted(set(duplikat_nomor)):
            error.append(f"Nomor [{n}] muncul lebih dari sekali di Daftar Pustaka.")

    url_dupe = cek_url_duplikat(entri)
    for url, ns in url_dupe.items():
        error.append(f"URL yang sama dipakai untuk nomor berbeda {sorted(ns)}: {url}")

    entri_tanpa_url = sorted(n for n, e in entri.items() if not e["url"])
    for n in entri_tanpa_url:
        peringatan.append(f"Entri [{n}] di Daftar Pustaka tidak punya URL yang terbaca — pastikan bukan sumber dikarang.")

    tidak_dipakai = sorted(nomor_ada - nomor_dipakai)
    for n in tidak_dipakai:
        peringatan.append(f"Entri [{n}] ada di Daftar Pustaka tapi tidak pernah dikutip [{n}] di badan teks.")

    statistik_tanpa_kutipan = cek_statistik_tanpa_kutipan(baris_badan)
    for t in statistik_tanpa_kutipan:
        peringatan.append(
            f"Baris {t['baris']} punya angka/persen/Rupiah ('{t['angka']}') tanpa [n] di baris sama — "
            f"cek manual: '{t['cuplikan']}'"
        )

    return {
        "jumlah_kutipan_unik_di_teks": len(nomor_dipakai),
        "jumlah_entri_pustaka": len(entri),
        "error": error,
        "peringatan": peringatan,
        "lulus": len(error) == 0,
    }


# Dicoba berurutan sampai berhasil didekode. utf-8-sig menangani BOM UTF-8 (umum dari Word/
# Notepad Windows); utf-16 hanya dicoba bila file punya BOM UTF-16 di awal (0xFF 0xFE / 0xFE 0xFF)
# -- di luar itu 'utf-16' nyaris selalu "berhasil" mendekode byte apa pun jadi teks acak/rusak,
# yang justru menyamarkan file cp1252/latin asli sebagai sukses. cp1252 dicoba PALING TERAKHIR
# sebagai jaring pengaman untuk file lama Windows berkode karakter Eropa Barat -- hampir selalu
# "berhasil" juga (byte apa pun valid di cp1252), jadi urutannya sengaja ditaruh belakang supaya
# encoding yang lebih spesifik/tepat dicoba dulu.
ENCODING_DICOBA = ["utf-8", "utf-8-sig"]
BOM_UTF16 = (b"\xff\xfe", b"\xfe\xff")


def baca_teks_file(path):
    """Baca file draf, mencoba beberapa encoding umum. Kembalikan (isi, encoding_dipakai).
    Raise ValueError dengan pesan ramah Bahasa Indonesia bila semua encoding gagal."""
    with open(path, "rb") as f:
        mentah = f.read()

    urutan = list(ENCODING_DICOBA)
    if mentah.startswith(BOM_UTF16):
        urutan.append("utf-16")
    urutan.append("cp1252")  # jaring terakhir; byte apa pun valid, jadi selalu dicoba paling akhir

    for enc in urutan:
        try:
            return mentah.decode(enc), enc
        except (UnicodeDecodeError, UnicodeError):
            continue
    raise ValueError(
        "Tidak bisa membaca isi file (encoding tidak dikenali; dicoba: "
        + ", ".join(urutan)
        + "). Ini biasa terjadi bila draf ditempel dari aplikasi lain (mis. Word) dan tersimpan "
        "dengan karakter aneh. Perbaikan: buka file di editor teks biasa (Notepad/TextEdit/VS "
        "Code), lalu 'Simpan Sebagai' dengan encoding UTF-8, dan jalankan lagi."
    )


def main():
    ap = argparse.ArgumentParser(description="Cek konsistensi sitasi [n] vs Daftar Pustaka")
    ap.add_argument("file", help="Path file draf (.md/.txt), atau '-' untuk baca dari stdin")
    ap.add_argument("--json", action="store_true", help="Keluaran JSON (default: teks rapi)")
    args = ap.parse_args()

    try:
        if args.file == "-":
            isi = sys.stdin.read()
        else:
            isi, _ = baca_teks_file(args.file)
    except (OSError, ValueError) as e:
        pesan = f"Tidak bisa membaca file: {e}"
        if args.json:
            print(json.dumps({"error": pesan}, ensure_ascii=False, indent=2), file=sys.stderr)
        else:
            print(f"❌ {pesan}", file=sys.stderr)
        sys.exit(2)

    hasil = periksa(isi)

    if args.json:
        print(json.dumps(hasil, ensure_ascii=False, indent=2))
    else:
        print(f"Kutipan unik di teks : {hasil['jumlah_kutipan_unik_di_teks']}")
        print(f"Entri Daftar Pustaka : {hasil['jumlah_entri_pustaka']}")
        if hasil["error"]:
            print("\n❌ ERROR (wajib diperbaiki):")
            for e in hasil["error"]:
                print(f"  - {e}")
        if hasil["peringatan"]:
            print("\n⚠️  PERINGATAN (cek manual, tidak selalu salah):")
            for p in hasil["peringatan"]:
                print(f"  - {p}")
        if not hasil["error"] and not hasil["peringatan"]:
            print("\n✅ Tidak ada masalah terdeteksi.")
        elif not hasil["error"]:
            print("\n✅ Tidak ada error keras. Tinjau peringatan di atas bila ada.")

    sys.exit(0 if hasil["lulus"] else 1)


if __name__ == "__main__":
    main()
