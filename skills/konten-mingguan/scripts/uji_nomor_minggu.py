#!/usr/bin/env python3
"""Tes mandiri untuk nomor_minggu.py (tanpa dependensi luar). Jalankan:
  python3 scripts/uji_nomor_minggu.py
Keluar dengan kode 0 bila semua lolos, 1 bila ada yang gagal.
"""
import json
import subprocess
import sys
from pathlib import Path

SKRIP = Path(__file__).with_name("nomor_minggu.py")
gagal = 0


def jalankan(*args):
    r = subprocess.run([sys.executable, str(SKRIP), *args], capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


def cek(nama, kondisi):
    global gagal
    status = "OK" if kondisi else "GAGAL"
    if not kondisi:
        gagal += 1
    print("[{}] {}".format(status, nama))


# 1. Hari ini Rabu 2026-09-23 -> Senin minggu depan = 2026-09-28 (ISO W40)
kode, out, err = jalankan("--hari-ini", "2026-09-23")
d = json.loads(out)
cek("senin minggu depan dari Rabu 2026-09-23 = 2026-09-28", d["senin"] == "2026-09-28")
cek("label minggu ISO 2026-W40", d["label_minggu"] == "2026-W40")
cek("minggu terakhir (Minggu) = 2026-10-04", d["minggu_terakhir"] == "2026-10-04")
cek("7 hari dihasilkan", len(d["hari"]) == 7)
cek("hari pertama = Senin", d["hari"][0]["hari"] == "Senin")
cek("hari terakhir = Minggu", d["hari"][6]["hari"] == "Minggu")

# 2. Hari ini pas Senin -> tetap loncat ke Senin MINGGU DEPAN (bukan minggu ini)
kode, out, err = jalankan("--hari-ini", "2026-09-28")  # ini sendiri hari Senin
d2 = json.loads(out)
cek("dari hari Senin, tetap lompat ke Senin depannya (2026-10-05)", d2["senin"] == "2026-10-05")

# 3. Momen: tanggal kembar 10.10 dan Harbolnas 12.12 terdeteksi
kode, out, err = jalankan("--mulai", "2026-10-05")
d3 = json.loads(out)
hari_1010 = next(h for h in d3["hari"] if h["tanggal"] == "2026-10-10")
cek("10.10 terdeteksi sebagai tanggal kembar",
    any("kembar" in m["nama"] for m in hari_1010["momen"]))

kode, out, err = jalankan("--mulai", "2026-12-07")
d4 = json.loads(out)
hari_1212 = next(h for h in d4["hari"] if h["tanggal"] == "2026-12-12")
cek("12.12 terdeteksi sebagai Harbolnas", any("Harbolnas" in m["nama"] for m in hari_1212["momen"]))

# 4. Gajian custom tanggal 1 & 15
kode, out, err = jalankan("--mulai", "2026-09-28", "--gajian-tanggal", "1,15")
d5 = json.loads(out)
hari_1okt = next(h for h in d5["hari"] if h["tanggal"] == "2026-10-01")
cek("tanggal 1 dikenali gajian saat --gajian-tanggal 1,15",
    any("gajian" in m["nama"] for m in hari_1okt["momen"]))

# 5. Hari besar tetap: 2026-10-01 (dalam minggu 2026-09-28) juga Hari Kesaktian Pancasila
kode, out, err = jalankan("--mulai", "2026-09-28")
d6 = json.loads(out)
hari_1okt2 = next(h for h in d6["hari"] if h["tanggal"] == "2026-10-01")
cek("1 Okt terdeteksi Hari Kesaktian Pancasila",
    any("Kesaktian Pancasila" in m["nama"] for m in hari_1okt2["momen"]))

# 6. --mulai yang BUKAN hari Senin harus ditolak (exit code != 0)
kode, out, err = jalankan("--mulai", "2026-09-29")  # itu hari Selasa
cek("--mulai bukan Senin ditolak (exit code != 0)", kode != 0)
cek("pesan error menyebut bukan Senin", "bukan hari Senin" in err or "bukan hari Senin" in out)

# 7. Tanggal rusak ditolak
kode, out, err = jalankan("--mulai", "31-13-2026")
cek("tanggal rusak ditolak (exit code != 0)", kode != 0)

# 8. --gajian-tanggal rusak ditolak
kode, out, err = jalankan("--gajian-tanggal", "abc")
cek("--gajian-tanggal bukan angka ditolak", kode != 0)

kode, out, err = jalankan("--gajian-tanggal", "35")
cek("--gajian-tanggal di luar 1-31 ditolak", kode != 0)

# 9. Format text tidak error dan memuat label minggu
kode, out, err = jalankan("--mulai", "2026-09-28", "--format", "text")
cek("format text sukses (exit 0)", kode == 0)
cek("format text memuat label minggu", "2026-W40" in out)

print()
if gagal:
    print("HASIL: {} tes GAGAL".format(gagal))
    sys.exit(1)
print("HASIL: semua tes lolos")
