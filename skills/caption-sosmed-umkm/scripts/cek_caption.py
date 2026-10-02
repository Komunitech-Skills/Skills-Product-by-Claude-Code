#!/usr/bin/env python3
"""Cek format & fakta caption sebelum dikirim ke pengguna.

Memeriksa tiap variasi (baris yang diawali "**Variasi ..."):
  - jumlah kata (hashtag tidak dihitung) sesuai platform,
  - jumlah hashtag sesuai platform,
  - fakta/klaim lewat cek_fakta.py (klaim kesehatan, label BPOM/halal, jam, asal, ukuran, urgensi, testimoni karangan).

Platform: ig (80-150 kata, 3-8 hashtag), tiktok (8-60 kata, 3-5 hashtag), fb (50-120 kata, 0-3 hashtag),
wa (<=30 kata, 0 hashtag).
Kode keluar: 0 = LULUS, 2 = ada GAGAL, 1 = input salah. Hanya Python standar. Contoh:
  python3 cek_caption.py --platform ig --teks-file caption.md --fakta "keripik singkong 200 gram Rp15.000"
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cek_fakta  # noqa: E402

ATURAN = {"ig": (80, 150, 3, 8), "tiktok": (8, 60, 3, 5), "fb": (50, 120, 0, 3), "wa": (1, 30, 0, 0)}
POLA_HASHTAG = re.compile(r"(?<!\w)#\w+")


def pecah_variasi(teks):
    bagian, nama, buf = [], None, []
    for baris in teks.splitlines():
        if re.match(r"\s*\**\s*Variasi\b", baris, re.IGNORECASE):
            if nama is not None:
                bagian.append((nama, "\n".join(buf)))
            nama, buf = baris.strip().strip("*").strip(), []
        elif re.match(r"\s*(?:💡|tips\s+posting|asumsi)", baris, re.IGNORECASE):
            if nama is not None:
                bagian.append((nama, "\n".join(buf)))
            nama, buf = None, []
        elif nama is not None:
            buf.append(baris)
    if nama is not None:
        bagian.append((nama, "\n".join(buf)))
    return bagian


def hitung(caption):
    tag = POLA_HASHTAG.findall(caption)
    isi = POLA_HASHTAG.sub(" ", caption)
    isi = re.sub(r"\[[^\]\n]*\]", lambda m: " x " if m.group(0).lower().startswith("[isi") else " ", isi)
    kata = [k for k in re.findall(r"[^\W_]+(?:[-'][^\W_]+)*", isi)]
    return len(kata), len(tag)


def periksa_caption(teks, fakta, platform):
    kmin, kmaks, hmin, hmaks = ATURAN[platform]
    variasi = pecah_variasi(teks)
    temuan = []
    if not variasi:
        temuan.append(("GAGAL", "format", "Tidak ada baris '**Variasi A – ...**'. Ikuti format output SKILL.md."))
    for nama, isi in variasi:
        kata, tag = hitung(isi)
        if kata < kmin or kata > kmaks:
            temuan.append(("GAGAL", nama, "{} kata (hashtag tidak dihitung); {} wajib {}-{} kata. Tulis ulang."
                           .format(kata, platform, kmin, kmaks)))
        if tag < hmin or tag > hmaks:
            temuan.append(("GAGAL", nama, "{} hashtag; {} wajib {}-{} hashtag.".format(tag, platform, hmin, hmaks)))
        for t in cek_fakta.periksa(isi, fakta):
            temuan.append((t["level"], nama, t["pesan"]))
    return temuan, variasi


def main():
    p = argparse.ArgumentParser(description="Cek panjang, hashtag, dan fakta caption.")
    p.add_argument("--platform", required=True, choices=sorted(ATURAN))
    p.add_argument("--teks-file")
    p.add_argument("--teks")
    p.add_argument("--fakta")
    p.add_argument("--fakta-file")
    a = p.parse_args()
    if (a.teks is None) == (a.teks_file is None):
        cek_fakta.galat("Isi salah satu: --teks atau --teks-file.")
    if (a.fakta is None) == (a.fakta_file is None):
        cek_fakta.galat("Isi salah satu: --fakta atau --fakta-file (kata-kata pengguna).")
    teks = a.teks if a.teks is not None else cek_fakta.baca_file(a.teks_file)
    fakta = a.fakta if a.fakta is not None else cek_fakta.baca_file(a.fakta_file)
    if not teks.strip() or not fakta.strip():
        cek_fakta.galat("Teks atau fakta kosong.")
    temuan, variasi = periksa_caption(teks, fakta, a.platform)
    for nama, isi in variasi:
        k, h = hitung(isi)
        print("{}: {} kata, {} hashtag".format(nama, k, h))
    for lv, nama, pesan in temuan:
        print("{}: [{}] {}".format(lv, nama, pesan))
    gagal = sum(1 for t in temuan if t[0] == "GAGAL")
    print("HASIL: {} ({} GAGAL, {} CEK)".format("GAGAL" if gagal else "LULUS", gagal, len(temuan) - gagal))
    sys.exit(2 if gagal else 0)


if __name__ == "__main__":
    main()
