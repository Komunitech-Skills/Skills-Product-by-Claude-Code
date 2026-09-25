#!/usr/bin/env python3
"""Skor ide usaha tertimbang + titik impas kasar.

Bagian dari skill `brainstorming-ide-usaha`. Python standar saja (tanpa paket
pihak ketiga), berjalan lintas OS (Linux/macOS: `python3`, Windows: `python`
atau `py`).

Perintah:
  skor   -- hitung skor tertimbang & peringkat dari file ide (CSV) + bobot (JSON)
  impas  -- hitung titik impas kasar (unit) dari modal awal & margin per unit

Contoh:
  python3 skor_ide.py skor --ide ide.csv --bobot bobot.json
  python3 skor_ide.py impas --modal 5000000 --margin 15000

Format file: lihat templates/format-data-skor.md di folder skill.
"""
import argparse
import csv
import json
import math
import sys
from pathlib import Path

NILAI_MIN = 1
NILAI_MAX = 5


class DataTidakValid(Exception):
    """Dilempar saat data ide/bobot/parameter impas tidak valid."""


def baca_bobot(path):
    try:
        mentah = json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise DataTidakValid(f"file bobot tidak ditemukan: {path}")
    except json.JSONDecodeError as e:
        raise DataTidakValid(f"file bobot bukan JSON valid: {e}")
    if not isinstance(mentah, dict) or not mentah:
        raise DataTidakValid("file bobot harus berupa objek JSON tidak kosong, mis. {\"kriteria\": 3}")

    bobot = {}
    for kunci, nilai in mentah.items():
        try:
            angka = float(nilai)
        except (TypeError, ValueError):
            raise DataTidakValid(f"bobot untuk '{kunci}' bukan angka: {nilai!r}")
        if angka <= 0:
            raise DataTidakValid(f"bobot untuk '{kunci}' harus lebih besar dari 0 (nilai: {angka})")
        bobot[kunci] = angka
    return bobot


def baca_ide(path, kriteria):
    try:
        teks = Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        raise DataTidakValid(f"file ide tidak ditemukan: {path}")

    baris_list = list(csv.DictReader(teks.splitlines()))
    if not baris_list:
        raise DataTidakValid("file ide kosong atau tidak punya baris data")

    header = baris_list[0].keys()
    if "nama_ide" not in header:
        raise DataTidakValid("file ide wajib punya kolom 'nama_ide'")

    kolom_kriteria_ada = [k for k in header if k != "nama_ide"]
    hilang_di_ide = set(kriteria) - set(kolom_kriteria_ada)
    hilang_di_bobot = set(kolom_kriteria_ada) - set(kriteria)
    if hilang_di_ide:
        raise DataTidakValid(
            f"kolom kriteria di file bobot tidak ada di file ide: {sorted(hilang_di_ide)}"
        )
    if hilang_di_bobot:
        raise DataTidakValid(
            f"kolom kriteria di file ide tidak ada di file bobot: {sorted(hilang_di_bobot)}"
        )

    ide = []
    nama_terpakai = set()
    for no, baris in enumerate(baris_list, start=2):  # baris 1 = header
        nama = (baris.get("nama_ide") or "").strip()
        if not nama:
            raise DataTidakValid(f"baris {no}: 'nama_ide' kosong")
        if nama in nama_terpakai:
            raise DataTidakValid(f"baris {no}: nama_ide '{nama}' duplikat")
        nama_terpakai.add(nama)

        skor_kriteria = {}
        for k in kriteria:
            mentah = (baris.get(k) or "").strip()
            if not mentah:
                raise DataTidakValid(f"baris {no} ('{nama}'), kolom '{k}': nilai kosong")
            try:
                angka = float(mentah)
            except ValueError:
                raise DataTidakValid(f"baris {no} ('{nama}'), kolom '{k}': bukan angka ({mentah!r})")
            if not (NILAI_MIN <= angka <= NILAI_MAX):
                raise DataTidakValid(
                    f"baris {no} ('{nama}'), kolom '{k}': nilai {angka} di luar rentang {NILAI_MIN}-{NILAI_MAX}"
                )
            skor_kriteria[k] = angka
        ide.append({"nama_ide": nama, "skor_kriteria": skor_kriteria})
    return ide


def hitung_skor(ide, bobot):
    total_bobot = sum(bobot.values())
    hasil = []
    for item in ide:
        jumlah_tertimbang = sum(item["skor_kriteria"][k] * b for k, b in bobot.items())
        skor_akhir = jumlah_tertimbang / total_bobot
        hasil.append({**item, "skor_tertimbang": round(skor_akhir, 3)})
    hasil.sort(key=lambda x: x["skor_tertimbang"], reverse=True)
    for peringkat, item in enumerate(hasil, start=1):
        item["peringkat"] = peringkat
    return hasil


def deteksi_seri(hasil_terurut):
    seri = []
    i = 0
    while i < len(hasil_terurut):
        j = i
        while j + 1 < len(hasil_terurut) and hasil_terurut[j + 1]["skor_tertimbang"] == hasil_terurut[i]["skor_tertimbang"]:
            j += 1
        if j > i:
            seri.append([hasil_terurut[k]["nama_ide"] for k in range(i, j + 1)])
        i = j + 1
    return seri


def cetak_tabel_skor(hasil, bobot):
    lebar_nama = max(8, max(len(h["nama_ide"]) for h in hasil))
    header = f"{'Peringkat':<10}{'Nama Ide':<{lebar_nama + 2}}{'Skor Tertimbang':>16}"
    print(header)
    print("-" * len(header))
    for h in hasil:
        print(f"{h['peringkat']:<10}{h['nama_ide']:<{lebar_nama + 2}}{h['skor_tertimbang']:>16.3f}")

    seri = deteksi_seri(hasil)
    if seri:
        print()
        print("⚠️  Skor seri terdeteksi (putuskan lewat untung-rugi kualitatif, bukan asal pilih):")
        for grup in seri:
            print(f"   - {', '.join(grup)}")

    print()
    print(f"Bobot kriteria dipakai (total bobot = {sum(bobot.values()):g}):")
    for k, v in bobot.items():
        print(f"   - {k}: {v:g}")


def cmd_skor(args):
    try:
        bobot = baca_bobot(args.bobot)
        ide = baca_ide(args.ide, list(bobot.keys()))
    except DataTidakValid as e:
        print(f"❌ Data tidak valid: {e}", file=sys.stderr)
        return 1

    hasil = hitung_skor(ide, bobot)
    cetak_tabel_skor(hasil, bobot)
    return 0


def hitung_impas(modal, margin):
    if modal <= 0:
        raise DataTidakValid(f"modal awal harus lebih besar dari 0 (nilai: {modal:g})")
    if margin <= 0:
        raise DataTidakValid(f"margin per unit harus lebih besar dari 0 (nilai: {margin:g})")
    return math.ceil(modal / margin)


def cmd_impas(args):
    try:
        unit_impas = hitung_impas(args.modal, args.margin)
    except DataTidakValid as e:
        print(f"❌ Data tidak valid: {e}", file=sys.stderr)
        return 1

    print(f"Modal awal        : Rp{args.modal:,.0f}".replace(",", "."))
    print(f"Margin per unit    : Rp{args.margin:,.0f}".replace(",", "."))
    print(f"Titik impas (BEP)  : {unit_impas:,} unit".replace(",", "."))
    print()
    print("Catatan: ini perkiraan KASAR (modal awal ÷ margin per unit, dibulatkan ke atas).")
    print("Tidak memperhitungkan biaya tetap bulanan berulang, pajak, atau penyusutan.")
    print("Untuk modal per unit presisi dari resep/BOM, pakai skill 'hitung-hpp'.")
    return 0


def buat_parser():
    p = argparse.ArgumentParser(description="Skor ide usaha tertimbang + titik impas kasar")
    sub = p.add_subparsers(dest="perintah", required=True)

    p_skor = sub.add_parser("skor", help="Hitung skor tertimbang & peringkat ide")
    p_skor.add_argument("--ide", required=True, help="Path file CSV daftar ide")
    p_skor.add_argument("--bobot", required=True, help="Path file JSON bobot kriteria")
    p_skor.set_defaults(func=cmd_skor)

    p_impas = sub.add_parser("impas", help="Hitung titik impas kasar (unit)")
    p_impas.add_argument("--modal", required=True, type=float, help="Modal awal (Rupiah)")
    p_impas.add_argument("--margin", required=True, type=float, help="Margin/untung per unit (Rupiah)")
    p_impas.set_defaults(func=cmd_impas)

    return p


def main(argv=None):
    parser = buat_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
