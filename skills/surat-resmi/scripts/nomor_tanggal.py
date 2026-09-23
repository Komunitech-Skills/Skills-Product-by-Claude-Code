#!/usr/bin/env python3
"""Bantu penulisan tanggal surat (EYD V) dan nomor surat dengan bulan Romawi.

Contoh:
  python3 nomor_tanggal.py --tanggal 23-09-2026
  python3 nomor_tanggal.py --tanggal "23 Sep 2026" --urut 7 --kode UND --instansi "CV-MJ"
  python3 nomor_tanggal.py --tanggal 2026-10-05 --urut 12 --pola "{urut}/{kode}/{romawi}/{tahun}" --kode SK
  python3 nomor_tanggal.py --tanggal 23-09-2026 --acara 03-10-2026 --format teks

Keluaran:
  - tanggal_surat   : "23 September 2026" (bulan ditulis lengkap, tanpa angka nol di depan)
  - baris_tanggal   : "Surabaya, 23 September 2026" bila --kota diisi
  - nomor_surat     : sesuai --pola. Placeholder: {urut} {kode} {instansi} {romawi} {bulan} {tahun}
                      {urut} diisi 3 digit (007) kecuali --digit diubah.
  - acara           : hari & tanggal kegiatan untuk surat undangan, mis. "Sabtu, 3 Oktober 2026"

Hanya library standar Python 3.8+. Tidak ada akses jaringan.
"""
import argparse
import json
import re
import sys
from datetime import date

BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
         "Agustus", "September", "Oktober", "November", "Desember"]
BULAN_ALIAS = {
    "jan": 1, "januari": 1, "feb": 2, "februari": 2, "pebruari": 2, "mar": 3, "maret": 3,
    "apr": 4, "april": 4, "mei": 5, "jun": 6, "juni": 6, "jul": 7, "juli": 7,
    "agu": 8, "agt": 8, "agus": 8, "agustus": 8, "sep": 9, "sept": 9, "september": 9,
    "okt": 10, "oktober": 10, "nov": 11, "nopember": 11, "november": 11,
    "des": 12, "desember": 12,
}
ROMAWI = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
POLA_DEFAULT = "{urut}/{kode}/{instansi}/{romawi}/{tahun}"
PLACEHOLDER = {"urut", "kode", "instansi", "romawi", "bulan", "tahun"}


class InputSalah(Exception):
    pass


def parse_tanggal(teks, label):
    s = (teks or "").strip()
    if not s:
        raise InputSalah(f"{label} kosong. Contoh: 23-09-2026 atau 23 September 2026.")
    try:
        m = re.fullmatch(r"(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})", s)
        if m:
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        m = re.fullmatch(r"(\d{1,2})[-/.](\d{1,2})[-/.](\d{4})", s)
        if m:
            return date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        m = re.fullmatch(r"(\d{1,2})\s+([A-Za-z]+)\.?\s+(\d{4})", s)
        if m:
            b = BULAN_ALIAS.get(m.group(2).lower())
            if b is None:
                raise InputSalah(f"{label}: nama bulan '{m.group(2)}' tidak dikenali.")
            return date(int(m.group(3)), b, int(m.group(1)))
    except ValueError:
        raise InputSalah(f"{label}: tanggal '{s}' tidak ada di kalender (cek hari/bulan).")
    raise InputSalah(f"{label}: format '{s}' tidak dikenali. Pakai 23-09-2026, 2026-09-23, "
                     "atau 23 September 2026.")


def teks_tanggal(d):
    return f"{d.day} {BULAN[d.month - 1]} {d.year}"


def buat_nomor(pola, urut, digit, kode, instansi, d):
    kunci = set(re.findall(r"\{(\w+)\}", pola))
    tak_dikenal = kunci - PLACEHOLDER
    if tak_dikenal:
        raise InputSalah(f"--pola memakai placeholder tak dikenal: {', '.join(sorted(tak_dikenal))}. "
                         f"Yang tersedia: {', '.join(sorted(PLACEHOLDER))}.")
    if "kode" in kunci and not kode:
        raise InputSalah("--pola memakai {kode} tapi --kode belum diisi (mis. UND, SK, SKU).")
    if "instansi" in kunci and not instansi:
        raise InputSalah("--pola memakai {instansi} tapi --instansi belum diisi (mis. CV-MJ).")
    nilai = {
        "urut": str(urut).zfill(digit),
        "kode": (kode or "").strip(),
        "instansi": (instansi or "").strip(),
        "romawi": ROMAWI[d.month - 1],
        "bulan": str(d.month).zfill(2),
        "tahun": str(d.year),
    }
    return re.sub(r"\{(\w+)\}", lambda m: nilai[m.group(1)], pola)


def main():
    p = argparse.ArgumentParser(description="Tanggal surat (EYD V) dan nomor surat bulan Romawi.")
    p.add_argument("--tanggal", required=True, help="Tanggal surat, mis. 23-09-2026")
    p.add_argument("--kota", help="Kota tempat surat dibuat, mis. Surabaya")
    p.add_argument("--urut", help="Nomor urut surat keluar (angka), mis. 7")
    p.add_argument("--digit", default="3", help="Jumlah digit nomor urut (default 3 -> 007)")
    p.add_argument("--kode", help="Kode jenis surat, mis. UND / SK / SKU / SPm")
    p.add_argument("--instansi", help="Singkatan instansi/usaha, mis. CV-MJ")
    p.add_argument("--pola", default=POLA_DEFAULT, help=f"Pola nomor (default {POLA_DEFAULT})")
    p.add_argument("--acara", help="Opsional: tanggal kegiatan (untuk undangan)")
    p.add_argument("--format", choices=["json", "teks"], default="json")
    a = p.parse_args()
    try:
        d = parse_tanggal(a.tanggal, "--tanggal")
        hasil = {
            "tanggal_iso": d.isoformat(),
            "tanggal_surat": teks_tanggal(d),
            "hari": HARI[d.weekday()],
            "bulan_romawi": ROMAWI[d.month - 1],
            "tahun": d.year,
        }
        if a.kota:
            hasil["baris_tanggal"] = f"{a.kota.strip()}, {teks_tanggal(d)}"
        if a.urut is not None:
            u = a.urut.strip()
            if not u.isdigit() or int(u) < 1:
                raise InputSalah("--urut harus angka bulat mulai 1, mis. 7.")
            if not a.digit.strip().isdigit() or not 1 <= int(a.digit) <= 6:
                raise InputSalah("--digit harus angka 1 sampai 6.")
            hasil["nomor_surat"] = buat_nomor(a.pola, int(u), int(a.digit), a.kode, a.instansi, d)
        if a.acara:
            e = parse_tanggal(a.acara, "--acara")
            hasil["acara"] = f"{HARI[e.weekday()]}, {teks_tanggal(e)}"
            if e < d:
                hasil["peringatan"] = "Tanggal acara lebih awal dari tanggal surat. Mohon dicek."
    except InputSalah as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(2)
    if a.format == "json":
        print(json.dumps(hasil, ensure_ascii=False, indent=2))
    else:
        label = {"tanggal_surat": "Tanggal surat", "hari": "Hari", "bulan_romawi": "Bulan Romawi",
                 "baris_tanggal": "Baris tanggal", "nomor_surat": "Nomor surat",
                 "acara": "Hari/tanggal acara", "peringatan": "PERINGATAN"}
        for k, v in label.items():
            if k in hasil:
                print(f"{v:<18}: {hasil[k]}")


if __name__ == "__main__":
    main()
