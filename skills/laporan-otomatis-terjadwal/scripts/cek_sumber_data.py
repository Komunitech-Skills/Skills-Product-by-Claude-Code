#!/usr/bin/env python3
"""Cek folder sumber data sebelum laporan disusun.

Tujuan: mencegah laporan berisi angka nol/karangan saat file sumber belum ada,
kosong, atau sudah lama tidak diperbarui. HANYA membaca metadata & isi file
di dalam folder yang diberikan pengguna. Tidak ada panggilan jaringan.

Hanya library standar Python (3.8+). Output JSON ke stdout (sukses maupun
"tidak siap" -- keduanya JSON valid; exit code membedakan).
Exit code 0  : ada file cocok, tidak kosong -> boleh lanjut menyusun laporan.
Exit code 1  : tidak siap (folder tidak ada / tidak ada file cocok / file
               kosong / file terlalu lama) -> pesan siap dipakai apa adanya,
               JANGAN membuat laporan dengan angka nol.
Exit code 2  : argumen salah.

PENTING soal "file terbaru" vs periode laporan: script ini hanya memeriksa
KESIAPAN file (ada/tidak kosong/tidak basi), BUKAN apakah isinya benar-benar
mencakup periode yang diminta (mis. seluruh minggu untuk laporan mingguan).
Setelah file dihitung oleh script skill sumber (rekap.py, dll.), WAJIB
bandingkan periode hasil hitung dengan periode yang seharusnya -- lihat
SKILL.md langkah "Cek periode". Pasang `--maks-umur-hari` LEBIH KETAT dari
irama jadwal (harian: 1, mingguan: 6, bulanan: ~27) supaya file basi/tertinggal
tidak lolos tanpa peringatan.

Kalau folder berisi BANYAK file yang masing-masing hanya mencakup sebagian
periode (mis. satu file per hari untuk laporan mingguan), memakai "file
terbaru" saja TIDAK CUKUP -- pakai `--daftar-semua` untuk melihat semua file
yang cocok (dengan tanggalnya), lalu gabungkan (concat, satu header saja) file
yang tanggalnya masuk periode target sebelum dijalankan ke script rekap.
"""
import argparse
import csv
import fnmatch
import json
import os
import sys
from datetime import datetime, timezone


def hitung_baris_data(path):
    """Hitung baris data CSV (tidak termasuk header). None bila gagal dibaca sbg CSV."""
    try:
        mentah = open(path, "rb").read()
    except OSError:
        return None
    if not mentah.strip():
        return 0
    for enc in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            teks = mentah.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        return None
    try:
        dialek = csv.Sniffer().sniff(teks[:4096], delimiters=",;\t|")
    except csv.Error:
        dialek = csv.excel
    try:
        baris = list(csv.reader(teks.splitlines(), dialect=dialek))
    except csv.Error:
        return None
    baris = [b for b in baris if any(sel.strip() for sel in b)]
    return max(0, len(baris) - 1)  # kurangi 1 baris header


def main():
    p = argparse.ArgumentParser(description="Cek kesiapan folder sumber data laporan")
    p.add_argument("--folder", required=True, help="Folder yang berisi file sumber (CSV)")
    p.add_argument("--pola", default="*.csv",
                    help="Pola nama file, pisahkan koma bila lebih dari satu. Default: *.csv")
    p.add_argument("--maks-umur-hari", type=int,
                    help="Peringatan bila file terbaru lebih tua dari N hari (opsional)")
    p.add_argument("--label", default="data",
                    help="Nama data untuk pesan (mis. 'penjualan', 'buku kas', 'stok')")
    p.add_argument("--daftar-semua", action="store_true",
                    help="Sertakan daftar SEMUA file yang cocok (path, tanggal ubah, ukuran) "
                         "di field 'file_cocok' -- dipakai untuk menggabungkan beberapa file "
                         "harian saat laporan mingguan/bulanan butuh lebih dari satu file")
    a = p.parse_args()

    if not os.path.isdir(a.folder):
        hasil = {
            "status": "folder_tidak_ada",
            "siap": False,
            "pesan": (f"Folder sumber {a.label} tidak ditemukan: {a.folder}. "
                      "Buat folder itu dan taruh file ekspor CSV di dalamnya, lalu coba lagi. "
                      "Laporan TIDAK dibuat (tidak ada angka nol palsu)."),
        }
        print(json.dumps(hasil, ensure_ascii=False, indent=2))
        sys.exit(1)

    pola_list = [x.strip() for x in a.pola.split(",") if x.strip()]
    kandidat = []
    for nama in os.listdir(a.folder):
        path = os.path.join(a.folder, nama)
        if not os.path.isfile(path):
            continue
        if any(fnmatch.fnmatch(nama.lower(), pol.lower()) for pol in pola_list):
            kandidat.append(path)

    if not kandidat:
        hasil = {
            "status": "tidak_ada_file",
            "siap": False,
            "folder": a.folder,
            "pola_dicari": pola_list,
            "pesan": (f"Belum ada file {a.label} (pola {', '.join(pola_list)}) di folder {a.folder}. "
                      f"Ekspor data {a.label} dari sumbernya (kasir/marketplace/bank/aplikasi stok) "
                      "sebagai CSV, taruh di folder itu, lalu jalankan lagi. "
                      "Laporan TIDAK dibuat (tidak ada angka nol palsu)."),
        }
        print(json.dumps(hasil, ensure_ascii=False, indent=2))
        sys.exit(1)

    kandidat.sort(key=lambda pth: os.path.getmtime(pth), reverse=True)
    terbaru = kandidat[0]
    ukuran = os.path.getsize(terbaru)
    mtime = datetime.fromtimestamp(os.path.getmtime(terbaru), tz=timezone.utc)
    umur_hari = (datetime.now(tz=timezone.utc) - mtime).days

    if ukuran == 0:
        hasil = {
            "status": "file_kosong",
            "siap": False,
            "file_terbaru": terbaru,
            "pesan": (f"File {a.label} terbaru ({os.path.basename(terbaru)}) kosong (0 byte). "
                      "Ekspor ulang datanya, lalu jalankan lagi. "
                      "Laporan TIDAK dibuat (tidak ada angka nol palsu)."),
        }
        print(json.dumps(hasil, ensure_ascii=False, indent=2))
        sys.exit(1)

    baris = hitung_baris_data(terbaru)
    if baris == 0:
        hasil = {
            "status": "tidak_ada_baris_data",
            "siap": False,
            "file_terbaru": terbaru,
            "pesan": (f"File {a.label} terbaru ({os.path.basename(terbaru)}) hanya berisi judul kolom, "
                      "tidak ada baris data. Cek lagi ekspornya, lalu jalankan ulang. "
                      "Laporan TIDAK dibuat (tidak ada angka nol palsu)."),
        }
        print(json.dumps(hasil, ensure_ascii=False, indent=2))
        sys.exit(1)

    peringatan = []
    if a.maks_umur_hari is not None and umur_hari > a.maks_umur_hari:
        peringatan.append(
            f"File {a.label} terbaru berumur {umur_hari} hari (lebih dari {a.maks_umur_hari} hari). "
            "Data mungkin sudah tidak mencerminkan periode laporan ini -- sebutkan ini di laporan."
        )

    if a.daftar_semua and len(kandidat) > 1:
        peringatan.append(
            f"Ada {len(kandidat) - 1} file lain yang juga cocok pola di folder ini. Kalau file "
            f"terbaru saja tidak mencakup seluruh periode laporan (mis. laporan mingguan tapi "
            "file diekspor harian), gabungkan file-file yang tanggalnya masuk periode target "
            "(lihat field 'file_cocok') menjadi satu file sebelum dihitung -- jangan hanya "
            "memakai file terbaru begitu saja."
        )

    hasil = {
        "status": "siap",
        "siap": True,
        "folder": a.folder,
        "file_terbaru": terbaru,
        "file_lain_cocok": len(kandidat) - 1,
        "ukuran_bytes": ukuran,
        "umur_hari": umur_hari,
        "perkiraan_baris_data": baris,
        "peringatan": peringatan,
        "pesan": f"Data {a.label} siap: {os.path.basename(terbaru)} ({baris} baris data, umur {umur_hari} hari).",
    }
    if a.daftar_semua:
        hasil["file_cocok"] = [
            {
                "path": pth,
                "diubah_pada": datetime.fromtimestamp(os.path.getmtime(pth), tz=timezone.utc)
                .isoformat(timespec="seconds"),
                "ukuran_bytes": os.path.getsize(pth),
            }
            for pth in kandidat
        ]
    print(json.dumps(hasil, ensure_ascii=False, indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()
