#!/usr/bin/env python3
"""Buat jadwal tanggal follow-up prospek (default H+1, H+3, H+7, H+14 dari kontak terakhir).

Hanya library standar Python (3.8+). Tidak ada akses jaringan.

Contoh:
  python3 jadwal_followup.py --mulai 2026-09-23
  python3 jadwal_followup.py --mulai 2026-09-25 --hari "1,3,7,14,30" --libur "2026-12-25,2026-12-26"
  python3 jadwal_followup.py --mulai 2026-09-23 --termasuk-akhir-pekan   # untuk prospek perorangan/toko online

Aturan: bila tanggal jatuh di Sabtu/Minggu/libur (dan tidak memakai --termasuk-akhir-pekan),
digeser ke hari kerja berikutnya. Bila dua follow-up jatuh di hari yang sama setelah digeser,
yang belakangan digeser lagi ke hari kerja berikutnya.
"""
import argparse
import json
import sys
from datetime import date, datetime, timedelta

HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
         "Agustus", "September", "Oktober", "November", "Desember"]


def gagal(pesan):
    print(f"ERROR: {pesan}", file=sys.stderr)
    sys.exit(1)


def parse_tgl(teks, nama):
    t = teks.strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(t, fmt).date()
        except ValueError:
            pass
    gagal(f"{nama} tidak dikenali: {teks!r}. Pakai format YYYY-MM-DD, mis. 2026-09-23")


def tgl_id(d):
    return f"{HARI[d.weekday()]}, {d.day} {BULAN[d.month - 1]} {d.year}"


def main():
    p = argparse.ArgumentParser(description="Jadwal follow-up prospek")
    p.add_argument("--mulai", required=True, help="Tanggal kontak terakhir/kirim penawaran (H+0), YYYY-MM-DD")
    p.add_argument("--hari", default="1,3,7,14", help="Jarak hari follow-up dari H+0, default '1,3,7,14'")
    p.add_argument("--libur", default="", help="Tanggal libur dipisah koma, mis. '2026-12-25,2026-12-26'")
    p.add_argument("--termasuk-akhir-pekan", action="store_true",
                   help="Boleh follow-up di Sabtu/Minggu (tidak digeser)")
    p.add_argument("--format", choices=["teks", "json"], default="teks")
    a = p.parse_args()

    mulai = parse_tgl(a.mulai, "tanggal mulai")
    try:
        offset = sorted({int(x.strip()) for x in a.hari.split(",") if x.strip()})
    except ValueError:
        gagal(f"--hari harus angka dipisah koma, mis. '1,3,7,14' (diberikan: {a.hari!r})")
    if not offset:
        gagal("--hari kosong")
    if offset[0] < 1 or offset[-1] > 180:
        gagal("jarak hari harus antara 1 dan 180")
    if len(offset) > 8:
        gagal("maksimal 8 follow-up; lebih dari itu terkesan memaksa")
    libur = {parse_tgl(x, "tanggal libur") for x in a.libur.split(",") if x.strip()}

    def hari_kerja(d):
        if d in libur:
            return False
        return a.termasuk_akhir_pekan or d.weekday() < 5

    jadwal, terpakai = [], set()
    for i, n in enumerate(offset, start=1):
        asli = mulai + timedelta(days=n)
        d = asli
        while not hari_kerja(d) or d in terpakai:
            d += timedelta(days=1)
        terpakai.add(d)
        jadwal.append({"ke": i, "rencana": f"H+{n}", "tanggal": d.isoformat(), "tanggal_teks": tgl_id(d),
                       "digeser": d != asli,
                       "alasan_geser": ("akhir pekan/libur/bentrok" if d != asli else "")})
    hasil = {"mulai": mulai.isoformat(), "mulai_teks": tgl_id(mulai), "jadwal": jadwal,
             "catatan": "Jika prospek membalas, hentikan urutan ini dan tanggapi balasannya."}
    if a.format == "json":
        print(json.dumps(hasil, ensure_ascii=False, indent=2))
        return
    print(f"Kontak terakhir (H+0): {hasil['mulai_teks']}")
    print("| Ke | Rencana | Tanggal kirim | Catatan |")
    print("|---|---|---|---|")
    for j in jadwal:
        print(f"| {j['ke']} | {j['rencana']} | {j['tanggal_teks']} | {'digeser (' + j['alasan_geser'] + ')' if j['digeser'] else '-'} |")
    print(f"\n* {hasil['catatan']}")


if __name__ == "__main__":
    main()
