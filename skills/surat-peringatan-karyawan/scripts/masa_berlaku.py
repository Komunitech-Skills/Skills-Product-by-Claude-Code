#!/usr/bin/env python3
"""Hitung masa berlaku Surat Peringatan (SP) dan cek apakah SP sebelumnya masih aktif.

Contoh:
  python3 masa_berlaku.py --terbit "23-09-2026"
  python3 masa_berlaku.py --terbit "2026-03-10" --bulan 6 --cek "23 September 2026"
  python3 masa_berlaku.py --terbit "31/08/2026" --format teks

Aturan hitung (dijelaskan juga di output):
  - SP berlaku sejak tanggal terbit (hari ke-1).
  - Tanggal berakhir = tanggal yang sama N bulan kemudian, dikurangi 1 hari.
    Contoh: terbit 23 September 2026, 6 bulan -> berakhir 22 Maret 2027.
  - Jika tanggal yang sama tidak ada di bulan tujuan (mis. 31 Agustus + 6 bulan
    -> 31 Februari tidak ada), SP berakhir pada hari terakhir bulan tujuan (28/29 Februari).

Hanya library standar Python 3.8+. Tidak ada akses jaringan.
"""
import argparse
import calendar
import json
import re
import sys
from datetime import date, timedelta

BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
         "Agustus", "September", "Oktober", "November", "Desember"]
BULAN_ALIAS = {
    "jan": 1, "januari": 1, "feb": 2, "peb": 2, "februari": 2, "pebruari": 2, "mar": 3, "maret": 3,
    "apr": 4, "april": 4, "mei": 5, "jun": 6, "juni": 6, "jul": 7, "juli": 7,
    "agu": 8, "agt": 8, "agus": 8, "agustus": 8, "sep": 9, "sept": 9, "september": 9,
    "okt": 10, "oktober": 10, "nov": 11, "nop": 11, "nopember": 11, "november": 11,
    "des": 12, "desember": 12,
}
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]


class InputSalah(Exception):
    pass


def parse_tanggal(teks, label):
    """Terima 2026-09-23, 23-09-2026, 23/09/2026, 23.09.2026, '23 September 2026', '23 Sep 2026'."""
    s = (teks or "").strip()
    if not s:
        raise InputSalah(f"{label} kosong. Contoh format: 23-09-2026 atau 23 September 2026.")
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
    raise InputSalah(
        f"{label}: format '{s}' tidak dikenali. Pakai 23-09-2026, 2026-09-23, atau 23 September 2026.")


def tambah_bulan(d, n):
    total = d.month - 1 + n
    tahun = d.year + total // 12
    bulan = total % 12 + 1
    hari = min(d.day, calendar.monthrange(tahun, bulan)[1])
    return date(tahun, bulan, hari)


def fmt(d):
    return f"{HARI[d.weekday()]}, {d.day} {BULAN[d.month - 1]} {d.year}"


def fmt_pendek(d):
    return f"{d.day} {BULAN[d.month - 1]} {d.year}"


def hitung_akhir(terbit, bulan):
    """Hari terakhir berlaku = sehari sebelum 'tanggal yang sama' N bulan kemudian.
    Jika tanggal itu tidak ada di bulan tujuan (mis. 30/31 Februari), SP berakhir
    pada hari terakhir bulan tujuan."""
    target = tambah_bulan(terbit, bulan)
    if target.day < terbit.day:  # terjadi penyesuaian ke akhir bulan
        return target
    return target - timedelta(days=1)


def hitung(terbit, bulan, cek=None):
    akhir = hitung_akhir(terbit, bulan)
    hasil = {
        "tanggal_terbit": terbit.isoformat(),
        "tanggal_terbit_teks": fmt_pendek(terbit),
        "masa_berlaku_bulan": bulan,
        "tanggal_berakhir": akhir.isoformat(),
        "tanggal_berakhir_teks": fmt_pendek(akhir),
        "hari_berakhir": fmt(akhir),
        "kalimat_surat": (f"Surat Peringatan ini berlaku selama {bulan} ({angka_teks(bulan)}) bulan "
                          f"terhitung sejak tanggal {fmt_pendek(terbit)} sampai dengan "
                          f"{fmt_pendek(akhir)}."),
        "aturan_hitung": ("Berlaku sejak tanggal terbit; berakhir pada tanggal yang sama "
                          f"{bulan} bulan kemudian dikurangi 1 hari. Jika tanggal itu tidak ada "
                          "di bulan tujuan (mis. 31 Februari), berakhir di hari terakhir bulan itu."),
    }
    if cek is not None:
        if cek < terbit:
            status = "belum_berlaku"
            ket = f"Tanggal {fmt_pendek(cek)} sebelum SP terbit."
        elif cek <= akhir:
            status = "masih_aktif"
            sisa = (akhir - cek).days
            sisa_teks = ("hari ini adalah hari terakhir SP berlaku" if sisa == 0
                         else f"sisa {sisa} hari")
            ket = (f"Pada {fmt_pendek(cek)} SP ini MASIH AKTIF ({sisa_teks}). Pelanggaran baru "
                   "dalam periode ini umumnya dapat dinaikkan ke tingkat SP berikutnya.")
        else:
            status = "sudah_berakhir"
            ket = (f"Pada {fmt_pendek(cek)} SP ini SUDAH BERAKHIR. Pelanggaran baru umumnya "
                   "dimulai lagi dari SP1 (kecuali PK/PP/PKB mengatur lain).")
        hasil.update({"tanggal_cek": cek.isoformat(), "status_pada_tanggal_cek": status,
                      "keterangan_cek": ket})
    return hasil


def angka_teks(n):
    kata = ["nol", "satu", "dua", "tiga", "empat", "lima", "enam", "tujuh", "delapan",
            "sembilan", "sepuluh", "sebelas", "dua belas"]
    return kata[n] if 0 <= n < len(kata) else str(n)


def main():
    p = argparse.ArgumentParser(description="Hitung masa berlaku Surat Peringatan (SP) karyawan.")
    p.add_argument("--terbit", required=True, help="Tanggal SP diterbitkan, mis. 23-09-2026")
    p.add_argument("--bulan", default="6",
                   help="Lama berlaku dalam bulan (default 6; ikuti PK/PP/PKB bila berbeda)")
    p.add_argument("--cek", help="Opsional: tanggal pelanggaran baru, untuk cek apakah SP masih aktif")
    p.add_argument("--format", choices=["json", "teks"], default="json")
    a = p.parse_args()
    try:
        if not re.fullmatch(r"\s*\d{1,2}\s*", str(a.bulan)):
            raise InputSalah("--bulan harus angka bulat 1 sampai 12, mis. 6.")
        bulan = int(a.bulan)
        if not 1 <= bulan <= 12:
            raise InputSalah("--bulan harus antara 1 dan 12. Masa berlaku SP umumnya 6 bulan.")
        terbit = parse_tanggal(a.terbit, "--terbit")
        cek = parse_tanggal(a.cek, "--cek") if a.cek else None
        hasil = hitung(terbit, bulan, cek)
    except InputSalah as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(2)
    if a.format == "json":
        print(json.dumps(hasil, ensure_ascii=False, indent=2))
    else:
        print(f"Tanggal terbit   : {hasil['tanggal_terbit_teks']}")
        print(f"Masa berlaku     : {bulan} bulan")
        print(f"Berlaku s.d.     : {hasil['hari_berakhir']}")
        print(f"Kalimat untuk SP : {hasil['kalimat_surat']}")
        if cek is not None:
            print(f"Cek tanggal      : {hasil['keterangan_cek']}")
        print(f"Cara hitung      : {hasil['aturan_hitung']}")


if __name__ == "__main__":
    main()
