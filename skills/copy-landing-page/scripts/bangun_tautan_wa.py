#!/usr/bin/env python3
"""Bantuan teknis untuk skill copy-landing-page: bangun tautan wa.me yang benar
dan hitung panjang meta title/description secara persis.

Hanya memakai pustaka standar Python (3.7+). Tidak ada akses jaringan.
Jalankan dengan `python3` (Windows: `python` atau `py`).

Contoh:
  # Bangun tautan WhatsApp dari nomor + pesan
  python3 bangun_tautan_wa.py wa --nomor "0812-3456-7890" --pesan "Halo, saya mau pesan keripik pedas dari halaman ini"

  # Cek panjang meta title & description
  python3 bangun_tautan_wa.py meta --title "Keripik Pedas Level 5 - Renyah Tahan Lama" --desc "Keripik singkong pedas gurih, tanpa pengawet, siap kirim seluruh Indonesia. Pesan lewat WhatsApp, bayar transfer/QRIS/COD."

Batas meta yang dipakai (batas aman umum, bukan jaminan tampilan Google 100% sama di semua perangkat):
  - Meta title    : maksimal 60 karakter
  - Meta description : maksimal 155 karakter
"""
import argparse
import re
import sys
from urllib.parse import quote

BATAS_TITLE = 60
BATAS_DESC = 155


class InputSalah(Exception):
    pass


def normalisasi_nomor_wa(nomor):
    """Ubah nomor HP Indonesia ke format 62xxxxxxxxxx (tanpa '+', tanpa spasi/strip)."""
    if nomor is None or not str(nomor).strip():
        raise InputSalah("nomor WhatsApp kosong")
    bersih = re.sub(r"[\s\-().]", "", str(nomor).strip())
    if bersih.startswith("+"):
        bersih = bersih[1:]
    if not re.fullmatch(r"\d{8,15}", bersih):
        raise InputSalah(
            f"nomor {nomor!r} tidak terlihat seperti nomor HP yang valid "
            "(harus angka, 8-15 digit setelah tanda dibuang)"
        )
    if bersih.startswith("0"):
        bersih = "62" + bersih[1:]
    elif bersih.startswith("8"):
        bersih = "62" + bersih
    elif not bersih.startswith("62"):
        raise InputSalah(
            f"nomor {nomor!r}: awali dengan 08xx, 8xx, atau 62xx (kode negara Indonesia)"
        )
    return bersih


def bangun_tautan_wa(nomor, pesan=""):
    nomor_bersih = normalisasi_nomor_wa(nomor)
    tautan = f"https://wa.me/{nomor_bersih}"
    if pesan and pesan.strip():
        tautan += f"?text={quote(pesan.strip())}"
    return tautan


def cek_meta(label, teks, batas):
    panjang = len(teks)
    status = "OK" if panjang <= batas else "TERLALU PANJANG"
    return {"label": label, "teks": teks, "panjang": panjang, "batas": batas, "status": status}


def cetak_hasil_meta(hasil):
    tanda = "OK" if hasil["status"] == "OK" else "PERINGATAN"
    print(f"[{tanda}] {hasil['label']}: {hasil['panjang']}/{hasil['batas']} karakter")
    print(f"  Teks: {hasil['teks']}")
    if hasil["status"] != "OK":
        lebih = hasil["panjang"] - hasil["batas"]
        print(f"  Kelebihan {lebih} karakter — pertimbangkan dipersingkat.")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Alat bantu copy-landing-page: tautan WA & cek meta SEO")
    sub = ap.add_subparsers(dest="perintah", required=True)

    p_wa = sub.add_parser("wa", help="Bangun tautan wa.me dari nomor + pesan")
    p_wa.add_argument("--nomor", required=True, help="Nomor WhatsApp, mis. 0812xxxxxxx atau 62812xxxxxxx")
    p_wa.add_argument("--pesan", default="", help="Isi pesan yang otomatis terisi saat tombol WA diklik")

    p_meta = sub.add_parser("meta", help="Cek panjang meta title & meta description")
    p_meta.add_argument("--title", default=None, help="Teks meta title")
    p_meta.add_argument("--desc", default=None, help="Teks meta description")

    args = ap.parse_args(argv)

    try:
        if args.perintah == "wa":
            tautan = bangun_tautan_wa(args.nomor, args.pesan)
            print(tautan)
        elif args.perintah == "meta":
            if not args.title and not args.desc:
                raise InputSalah("isi minimal salah satu dari --title atau --desc")
            if args.title:
                cetak_hasil_meta(cek_meta("Meta title", args.title, BATAS_TITLE))
            if args.desc:
                cetak_hasil_meta(cek_meta("Meta description", args.desc, BATAS_DESC))
    except InputSalah as e:
        print(f"Input tidak valid: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
