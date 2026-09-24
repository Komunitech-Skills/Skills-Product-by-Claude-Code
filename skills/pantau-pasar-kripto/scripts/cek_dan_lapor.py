#!/usr/bin/env python3
"""Wrapper untuk automation OpenClaw (`--command`): jalankan `cek_ambang.py`, dan HANYA
cetak sesuatu ke stdout kalau ada yang perlu dilaporkan (ambang baru terlewati ATAU ada
koin gagal total). Kalau tidak, cetak `NO_REPLY` -- OpenClaw tidak mem-posting apa pun ke
kanal kalau keluaran job persis `NO_REPLY` (lihat `references/openclaw-jadwal.md`).

SELALU keluar dengan kode 0 (exit 0), apa pun hasil `cek_ambang.py` -- Gateway OpenClaw
mencatat job `--command` yang keluar dengan kode bukan-0 sebagai job GAGAL (bisa memicu
notifikasi kegagalan terpisah), padahal exit 2/3 dari `cek_ambang.py` adalah kondisi NORMAL
(ambang terlewati / sebagian koin gagal), bukan bug. Wrapper inilah yang menerjemahkan kode
keluar `cek_ambang.py` (0/2/3) menjadi "ada pesan" vs "NO_REPLY", supaya Gateway sendiri
selalu melihat job ini sebagai sukses.

Ini murni Python standar (tanpa dependensi luar) supaya sama-sama jalan di
Windows/macOS/Linux -- tidak butuh `sh`/shell script terpisah seperti versi awal
(lihat catatan status di `references/openclaw-jadwal.md`).

Pakai:
  python3 cek_dan_lapor.py --konfigurasi kripto/konfigurasi.json --state kripto/state.json
  (opsi lain diteruskan apa adanya ke cek_ambang.py, mis. --jeda-ulang-jam, --harga-file
  untuk uji offline, --usia-basi-jam, --timeout, --percobaan)
"""

import json
import os
import subprocess
import sys

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
CEK_AMBANG = os.path.join(SCRIPTS_DIR, "cek_ambang.py")


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    cmd = [sys.executable, CEK_AMBANG] + argv
    proses = subprocess.run(cmd, capture_output=True, text=True)

    if proses.returncode in (2, 3):
        pesan = None
        try:
            data = json.loads(proses.stdout)
            pesan = data.get("pesan_singkat")
        except (json.JSONDecodeError, AttributeError):
            pesan = None
        if pesan:
            print(pesan)
        else:
            # cek_ambang.py tidak mengembalikan JSON yang bisa dibaca (seharusnya tidak
            # terjadi) -- tetap laporkan sesuatu daripada diam, sertakan info mentah.
            print(
                "Pantau kripto: ada yang perlu dilaporkan, tapi wrapper gagal membaca "
                "pesan_singkat dari cek_ambang.py. Keluaran mentah (stdout, dipotong):\n"
                + (proses.stdout or "(kosong)")[:1500]
            )
    elif proses.returncode == 1:
        # error konfigurasi/input -- ini PERLU diketahui pemilik, bukan didiamkan, tapi
        # juga bukan exit != 0 (lihat alasan di docstring) supaya job tidak ditandai gagal.
        print(f"Pantau kripto: cek_ambang.py gagal karena error input/konfigurasi:\n{proses.stdout}")
    else:
        print("NO_REPLY")

    return 0


if __name__ == "__main__":
    sys.exit(main())
