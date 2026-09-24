#!/usr/bin/env python3
"""Rekap operasional kunjungan klinik dari file CSV — AGREGAT SAJA.

Tujuan: menghasilkan angka kunjungan per hari/poli/penjamin, jam ramai, dan
perkiraan pasien tidak datang, TANPA pernah menampilkan data per-pasien
(nama, NIK, tanggal lahir, diagnosis, dll.) di output. Ini BUKAN alat rekam
medis dan BUKAN alat skrining/diagnosis — hanya rekap jumlah untuk laporan
operasional (lihat CLAUDE.md Komunitech & keputusan pemilik jalur 3, bidang
kesehatan: tanpa skrining/diagnosis/kalkulator medis).

Hanya memakai library standar Python (3.8+). Lintas OS (Windows/macOS/Linux).

Contoh pakai:
    python3 rekap_kunjungan.py --file kunjungan.csv
    python3 rekap_kunjungan.py --file kunjungan.csv --format json

Windows: ganti "python3" dengan "python" atau "py".
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime

# Nama kolom yang berisi data pribadi/klinis spesifik — kalau ada di file,
# kolom ini SENGAJA tidak pernah dibaca isinya untuk ditampilkan (hanya
# diberi tahu ke pengguna bahwa kolom itu diabaikan demi privasi pasien).
KOLOM_SENSITIF = [
    "nama", "nama pasien", "nama lengkap", "nik", "no ktp", "no. ktp",
    "tanggal lahir", "no rm", "no. rm", "rekam medis", "no bpjs",
    "no. bpjs", "diagnosis", "diagnosa", "keluhan", "alamat", "no hp",
    "no. hp", "no telepon", "no. telepon", "telepon", "hp",
]

# Alias nama kolom yang diterima (huruf kecil, tanpa spasi berlebih) untuk
# setiap kolom agregat yang DIPAKAI.
ALIAS_TANGGAL = ["tanggal", "tgl", "date", "tanggal kunjungan"]
ALIAS_JAM = ["jam", "waktu", "jam kunjungan", "time"]
ALIAS_POLI = ["poli", "layanan", "unit", "poliklinik", "jenis layanan"]
ALIAS_PENJAMIN = ["penjamin", "pembayaran", "cara bayar", "jenis pasien", "kelas"]
ALIAS_STATUS = ["status", "status kunjungan", "keterangan"]

KATA_TIDAK_DATANG = [
    "tidak datang", "tdk datang", "no show", "no-show", "noshow",
    "batal", "dibatalkan", "cancel", "absen",
]

FORMAT_TANGGAL_DICOBA = [
    "%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d/%m/%y", "%d-%m-%y",
    "%Y/%m/%d", "%m/%d/%Y",
]


class DataError(Exception):
    pass


def _normalisasi_header(h: str) -> str:
    return " ".join(h.strip().lower().split())


def _cari_kolom(header_asli: list, alias: list) -> str | None:
    norm = {_normalisasi_header(h): h for h in header_asli}
    for a in alias:
        if a in norm:
            return norm[a]
    return None


def _parse_tanggal(teks: str):
    teks = (teks or "").strip()
    if not teks:
        return None
    for fmt in FORMAT_TANGGAL_DICOBA:
        try:
            return datetime.strptime(teks, fmt).date()
        except ValueError:
            continue
    return None


def _parse_jam(teks: str):
    teks = (teks or "").strip()
    if not teks:
        return None
    for fmt in ("%H:%M", "%H:%M:%S", "%H.%M"):
        try:
            return datetime.strptime(teks, fmt).hour
        except ValueError:
            continue
    # tanggal+jam sekaligus, mis. "2026-09-24 08:15"
    for fmt in ("%Y-%m-%d %H:%M", "%d/%m/%Y %H:%M"):
        try:
            return datetime.strptime(teks, fmt).hour
        except ValueError:
            continue
    return None


def baca_csv(path_or_text: str, is_text: bool = False):
    if is_text:
        f = io.StringIO(path_or_text)
    else:
        try:
            f = open(path_or_text, "r", encoding="utf-8-sig", newline="")
        except FileNotFoundError:
            raise DataError(f"File tidak ditemukan: {path_or_text}")
        except OSError as e:
            raise DataError(f"Gagal membuka file: {e}")
    try:
        contoh = f.read(4096)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(contoh, delimiters=",;\t")
        except csv.Error:
            dialect = csv.excel
        reader = csv.DictReader(f, dialect=dialect)
        baris = [row for row in reader]
        header = reader.fieldnames or []
    finally:
        f.close()
    if not header:
        raise DataError("File CSV kosong atau tidak punya baris header.")
    return header, baris


def rekap(header: list, baris: list) -> dict:
    if not baris:
        raise DataError(
            "File tidak berisi baris data (hanya header). "
            "Cek apakah file ekspor sudah benar."
        )

    kolom_tanggal = _cari_kolom(header, ALIAS_TANGGAL)
    kolom_jam = _cari_kolom(header, ALIAS_JAM)
    kolom_poli = _cari_kolom(header, ALIAS_POLI)
    kolom_penjamin = _cari_kolom(header, ALIAS_PENJAMIN)
    kolom_status = _cari_kolom(header, ALIAS_STATUS)

    if not kolom_tanggal:
        raise DataError(
            "Tidak menemukan kolom tanggal (dicoba: "
            + ", ".join(ALIAS_TANGGAL)
            + "). Beri nama kolom tanggal kunjungan, mis. 'Tanggal'."
        )

    kolom_sensitif_terpakai = sorted(
        {h for h in header if _normalisasi_header(h) in KOLOM_SENSITIF}
    )

    per_hari = Counter()
    per_poli = Counter()
    per_penjamin = Counter()
    per_jam = Counter()
    tidak_datang = 0
    baris_tanggal_gagal = 0
    total = 0

    for row in baris:
        total += 1
        t = _parse_tanggal(row.get(kolom_tanggal, ""))
        if t is None:
            baris_tanggal_gagal += 1
        else:
            per_hari[t.isoformat()] += 1

        if kolom_poli:
            nilai = (row.get(kolom_poli) or "").strip() or "(tidak diisi)"
            per_poli[nilai] += 1
        if kolom_penjamin:
            nilai = (row.get(kolom_penjamin) or "").strip() or "(tidak diisi)"
            per_penjamin[nilai] += 1
        if kolom_jam:
            jam = _parse_jam(row.get(kolom_jam, ""))
            if jam is not None:
                per_jam[jam] += 1
        if kolom_status:
            status_l = (row.get(kolom_status) or "").strip().lower()
            if any(k in status_l for k in KATA_TIDAK_DATANG):
                tidak_datang += 1

    jam_ramai = per_jam.most_common(3)

    return {
        "total_baris": total,
        "total_kunjungan_tanggal_terbaca": total - baris_tanggal_gagal,
        "baris_tanggal_tidak_terbaca": baris_tanggal_gagal,
        "per_hari": dict(sorted(per_hari.items())),
        "per_poli": dict(per_poli.most_common()) if kolom_poli else None,
        "per_penjamin": dict(per_penjamin.most_common()) if kolom_penjamin else None,
        "jam_ramai": [{"jam": f"{j:02d}:00", "jumlah": n} for j, n in jam_ramai] if kolom_jam else None,
        "pasien_tidak_datang": tidak_datang if kolom_status else None,
        "kolom_sensitif_diabaikan": kolom_sensitif_terpakai,
    }


def format_teks(hasil: dict) -> str:
    baris = []
    baris.append("REKAP OPERASIONAL KUNJUNGAN (agregat, tanpa nama/diagnosis)")
    baris.append(f"Total baris data: {hasil['total_baris']}")
    if hasil["baris_tanggal_tidak_terbaca"]:
        baris.append(
            f"⚠️  {hasil['baris_tanggal_tidak_terbaca']} baris tanggalnya tidak terbaca "
            "dan tidak dihitung di rekap per hari."
        )
    baris.append("")
    baris.append("Kunjungan per hari:")
    if hasil["per_hari"]:
        for tgl, n in hasil["per_hari"].items():
            baris.append(f"  {tgl}: {n}")
    else:
        baris.append("  (tidak ada)")

    if hasil["per_poli"] is not None:
        baris.append("")
        baris.append("Kunjungan per poli/layanan:")
        for nama, n in hasil["per_poli"].items():
            baris.append(f"  {nama}: {n}")

    if hasil["per_penjamin"] is not None:
        baris.append("")
        baris.append("Kunjungan per penjamin/cara bayar:")
        for nama, n in hasil["per_penjamin"].items():
            baris.append(f"  {nama}: {n}")

    if hasil["jam_ramai"] is not None:
        baris.append("")
        baris.append("Jam paling ramai (top 3):")
        if hasil["jam_ramai"]:
            for j in hasil["jam_ramai"]:
                baris.append(f"  {j['jam']}: {j['jumlah']} kunjungan")
        else:
            baris.append("  (kolom jam ada tapi tidak ada nilai yang terbaca)")

    if hasil["pasien_tidak_datang"] is not None:
        baris.append("")
        baris.append(f"Perkiraan pasien tidak datang/batal: {hasil['pasien_tidak_datang']}")

    if hasil["kolom_sensitif_diabaikan"]:
        baris.append("")
        baris.append(
            "Catatan privasi: kolom berikut TIDAK dibaca isinya dan diabaikan demi "
            "kerahasiaan data pasien (UU PDP 27/2022): "
            + ", ".join(hasil["kolom_sensitif_diabaikan"])
        )

    baris.append("")
    baris.append(
        "Catatan: ini rekap operasional (jumlah), bukan rekam medis, "
        "bukan alat skrining/diagnosis, dan tidak menampilkan data per-pasien."
    )
    return "\n".join(baris)


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Rekap agregat kunjungan klinik dari CSV (tanpa nama/diagnosis di output)."
    )
    ap.add_argument("--file", required=True, help="Path file CSV ekspor kunjungan klinik.")
    ap.add_argument(
        "--format", choices=["teks", "json"], default="teks",
        help="Format output (default: teks).",
    )
    args = ap.parse_args(argv)

    try:
        header, baris = baca_csv(args.file)
        hasil = rekap(header, baris)
    except DataError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps(hasil, ensure_ascii=False, indent=2))
    else:
        print(format_teks(hasil))
    return 0


if __name__ == "__main__":
    sys.exit(main())
