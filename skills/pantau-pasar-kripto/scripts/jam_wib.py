#!/usr/bin/env python3
"""Ubah waktu data (mis. `last_updated` CoinGecko, timestamp Indodax) ke jam WIB (UTC+7).

Dipakai agar jam data di riset/ringkasan DIHITUNG, bukan ditebak (uji ulang OpenClaw
2026-10-01 skenario 04: `last_updated` 07:10 UTC ditulis "07:10 WIB", padahal 14:10 WIB).

Pemakaian (python3; Windows: python atau py):
  python3 scripts/jam_wib.py 2026-10-01T07:14:00.123Z      # ISO 8601 dengan Z / +00:00 / +07:00
  python3 scripts/jam_wib.py 1790838840                    # Unix detik (Indodax server_time)
  python3 scripts/jam_wib.py 1790838840000                 # Unix milidetik
  python3 scripts/jam_wib.py                               # waktu sekarang (jam ambil)

Waktu ISO TANPA zona (mis. "2026-10-01 07:14") ditolak: zonanya tidak boleh ditebak.
Hanya pustaka standar; tidak memakai internet. Keluaran: satu baris teks siap kutip,
mis. "1 Okt 2026 14:14 WIB (dari 2026-10-01 07:14 UTC)". Kode keluar 2 bila input salah.
"""
import re
import sys
from datetime import datetime, timedelta, timezone

WIB = timezone(timedelta(hours=7))
BULAN = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]


class InputSalah(Exception):
    pass


def parse_waktu(teks):
    s = teks.strip()
    if not s:
        raise InputSalah("Waktu kosong.")
    if s.isdigit():
        n = int(s)
        if n > 10 ** 11:          # milidetik
            n = n / 1000.0
        return datetime.fromtimestamp(n, tz=timezone.utc)
    iso = s.replace(" ", "T", 1)
    if iso.endswith("Z") or iso.endswith("z"):
        iso = iso[:-1] + "+00:00"
    try:
        t = datetime.fromisoformat(iso)
    except ValueError:
        # Python < 3.11 tidak menerima pecahan detik selain 3/6 digit; buang pecahan detik.
        iso2 = re.sub(r"\.\d+", "", iso)
        try:
            t = datetime.fromisoformat(iso2)
        except ValueError:
            raise InputSalah("Waktu '{}' tidak terbaca. Contoh: 2026-10-01T07:14:00Z atau 1790838840.".format(teks))
    if t.tzinfo is None:
        raise InputSalah("Waktu '{}' tidak punya zona waktu. Jangan ditebak: tambahkan Z bila UTC "
                         "(mis. {}Z) atau +07:00 bila memang WIB.".format(teks, s))
    return t


def format_wib(t):
    w = t.astimezone(WIB)
    return "{} {} {} {:02d}:{:02d} WIB".format(w.day, BULAN[w.month - 1], w.year, w.hour, w.minute)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    try:
        if not argv:
            print(format_wib(datetime.now(timezone.utc)) + " (waktu sekarang)")
            return 0
        teks = " ".join(argv)
        t = parse_waktu(teks)
        asal = t.astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        print("{} (dari {})".format(format_wib(t), asal))
        return 0
    except InputSalah as e:
        sys.stderr.write(str(e) + "\n")
        return 2


if __name__ == "__main__":
    sys.exit(main())
