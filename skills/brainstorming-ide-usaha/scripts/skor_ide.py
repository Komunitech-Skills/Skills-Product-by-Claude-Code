#!/usr/bin/env python3
"""Skor ide usaha tertimbang + titik impas kasar.

Bagian dari skill `brainstorming-ide-usaha`. Python standar saja (tanpa paket
pihak ketiga), berjalan lintas OS (Linux/macOS: `python3`, Windows: `python`
atau `py`).

Perintah:
  skor   -- hitung skor tertimbang & peringkat dari file ide (CSV) + bobot (JSON, opsional)
  impas  -- hitung titik impas kasar (unit) dari modal awal & margin per unit

Contoh:
  python3 skor_ide.py skor --ide ide.csv --bobot bobot.json
  python3 skor_ide.py skor --ide ide.csv               # tanpa bobot -> pakai default/sama rata
  python3 skor_ide.py impas --modal 5000000 --margin 15000
  python3 skor_ide.py impas --modal Rp5.000.000 --margin 15rb

Format file: lihat templates/format-data-skor.md di folder skill.
"""
import argparse
import csv
import json
import math
import re
import sys
from pathlib import Path

NILAI_MIN = 1
NILAI_MAX = 5

# Bobot default resmi skill ini (dipakai otomatis kalau --bobot tidak
# diberikan DAN nama kolom kriteria di file ide sama persis dengan ini).
# Lihat SKILL.md Langkah C.5 dan templates/format-data-skor.md.
BOBOT_DEFAULT = {
    "kesesuaian_modal": 5,
    "potensi_permintaan": 4,
    "kemudahan_eksekusi": 3,
    "kecocokan_keahlian": 2,
    "potensi_margin": 4,
}

# Cegah UnicodeEncodeError kalau output di-redirect ke konsol non-UTF-8
# (mis. Command Prompt Windows lama) dan skrip mencetak emoji/simbol.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="replace")
    except Exception:
        pass


class DataTidakValid(Exception):
    """Dilempar saat data ide/bobot/parameter impas tidak valid."""


# ---------------------------------------------------------------------------
# Pembacaan file (encoding & pemisah CSV gaya Excel Indonesia)
# ---------------------------------------------------------------------------

def _baca_file_teks(path, label):
    p = Path(path)
    try:
        data = p.read_bytes()
    except FileNotFoundError:
        raise DataTidakValid(f"file {label} tidak ditemukan: {path}")
    except IsADirectoryError:
        raise DataTidakValid(f"path {label} yang diberikan adalah folder, bukan file: {path}")
    except OSError as e:
        raise DataTidakValid(f"tidak bisa membaca file {label} ({path}): {e}")

    # utf-8-sig juga membuang BOM yang ditambahkan Excel ("CSV UTF-8").
    for enc in ("utf-8-sig", "cp1252"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue
    raise DataTidakValid(
        f"file {label} ({path}) tidak bisa dibaca sebagai teks — encoding tidak dikenali. "
        "Simpan ulang sebagai CSV UTF-8."
    )


def _deteksi_pemisah(baris_pertama):
    try:
        dialect = csv.Sniffer().sniff(baris_pertama, delimiters=",;")
        return dialect.delimiter
    except csv.Error:
        # Excel Indonesia sering memakai ';' karena ',' dipakai sebagai desimal.
        return ";" if baris_pertama.count(";") > baris_pertama.count(",") else ","


def _parse_csv_ide(path):
    teks = _baca_file_teks(path, "ide")
    baris_teks = [b for b in teks.splitlines()]
    if not baris_teks:
        raise DataTidakValid("file ide kosong")
    pemisah = _deteksi_pemisah(baris_teks[0])
    baris_mentah = list(csv.reader(baris_teks, delimiter=pemisah))
    baris_mentah = [b for b in baris_mentah if b]  # buang baris benar-benar kosong
    if not baris_mentah:
        raise DataTidakValid("file ide kosong")

    header = [h.strip() for h in baris_mentah[0]]
    if not header or header == [""]:
        raise DataTidakValid("file ide tidak punya baris header")
    if "nama_ide" not in header:
        raise DataTidakValid(
            "file ide wajib punya kolom 'nama_ide' "
            f"(header terbaca: {header}; pemisah kolom terdeteksi: {pemisah!r})"
        )

    data_rows = baris_mentah[1:]
    if not data_rows:
        raise DataTidakValid("file ide kosong atau tidak punya baris data")
    return header, data_rows, pemisah


def kolom_kriteria_dari_file(path):
    """Nama kolom kriteria (semua kolom selain nama_ide) di file ide."""
    header, _, _ = _parse_csv_ide(path)
    return [k for k in header if k != "nama_ide"]


def _parse_angka_nilai(mentah):
    s = mentah.strip()
    # Terima koma sebagai desimal (format Indonesia) selama tidak ada titik,
    # supaya "3.5" (format internasional) tidak salah diubah jadi "3.5.5".
    if "," in s and "." not in s:
        s = s.replace(",", ".")
    return float(s)


def baca_bobot(path):
    teks = _baca_file_teks(path, "bobot")
    try:
        mentah = json.loads(teks)
    except json.JSONDecodeError as e:
        raise DataTidakValid(f"file bobot bukan JSON valid: {e}")
    if not isinstance(mentah, dict) or not mentah:
        raise DataTidakValid("file bobot harus berupa objek JSON tidak kosong, mis. {\"kriteria\": 3}")

    bobot = {}
    for kunci, nilai in mentah.items():
        if isinstance(nilai, bool):
            raise DataTidakValid(f"bobot untuk '{kunci}' harus berupa angka, bukan true/false")
        try:
            angka = float(nilai)
        except (TypeError, ValueError):
            raise DataTidakValid(f"bobot untuk '{kunci}' bukan angka: {nilai!r}")
        if not math.isfinite(angka):
            raise DataTidakValid(
                f"bobot untuk '{kunci}' bukan angka wajar (nan/infinity tidak diterima): {nilai!r}"
            )
        if angka <= 0:
            raise DataTidakValid(f"bobot untuk '{kunci}' harus lebih besar dari 0 (nilai: {angka})")
        bobot[kunci] = angka
    return bobot


def baca_ide(path, kriteria):
    header, data_rows, pemisah = _parse_csv_ide(path)

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
    nama_terpakai = {}  # bentuk dinormalisasi (huruf kecil, spasi dirapikan) -> nomor baris
    for offset, baris in enumerate(data_rows, start=1):
        no = offset + 1  # baris 1 = header

        # Bug utama yang diperbaiki di v1.0.1: baris dengan koma desimal tanpa
        # kutip (mis. "Ide Y,3,5,4" dengan pemisah ',') menghasilkan jumlah
        # kolom yang tidak sama dengan header. Sebelumnya csv.DictReader
        # membuang/menggeser kolom itu diam-diam (skor jadi salah tanpa
        # peringatan). Sekarang baris seperti ini DITOLAK secara eksplisit,
        # di baris mana pun (bukan cuma baris data pertama).
        if len(baris) != len(header):
            raise DataTidakValid(
                f"baris {no}: jumlah kolom ({len(baris)}) tidak sama dengan jumlah kolom header "
                f"({len(header)}, pemisah kolom yang dipakai: {pemisah!r}). Kalau ini karena koma "
                "desimal tanpa kutip (mis. 3,5), tulis pakai titik (3.5) atau beri tanda kutip "
                '("3,5").'
            )

        row_map = dict(zip(header, [c.strip() for c in baris]))
        nama = (row_map.get("nama_ide") or "").strip()
        if not nama:
            raise DataTidakValid(f"baris {no}: 'nama_ide' kosong")

        kunci_dup = " ".join(nama.split()).casefold()
        if kunci_dup in nama_terpakai:
            raise DataTidakValid(
                f"baris {no}: nama_ide '{nama}' duplikat dengan baris {nama_terpakai[kunci_dup]} "
                "(besar/kecil huruf dan spasi ganda diabaikan saat membandingkan)"
            )
        nama_terpakai[kunci_dup] = no

        skor_kriteria = {}
        for k in kriteria:
            mentah = row_map.get(k, "")
            if not mentah:
                raise DataTidakValid(f"baris {no} ('{nama}'), kolom '{k}': nilai kosong")
            try:
                angka = _parse_angka_nilai(mentah)
            except ValueError:
                raise DataTidakValid(f"baris {no} ('{nama}'), kolom '{k}': bukan angka ({mentah!r})")
            if not math.isfinite(angka):
                raise DataTidakValid(
                    f"baris {no} ('{nama}'), kolom '{k}': nilai bukan angka wajar (nan/infinity tidak diterima): {mentah!r}"
                )
            if not (NILAI_MIN <= angka <= NILAI_MAX):
                raise DataTidakValid(
                    f"baris {no} ('{nama}'), kolom '{k}': nilai {angka:g} di luar rentang {NILAI_MIN}-{NILAI_MAX}"
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


def cetak_tabel_skor(hasil, bobot, sumber_bobot):
    lebar_nama = max(8, max(len(h["nama_ide"]) for h in hasil))
    header = f"{'Peringkat':<10}{'Nama Ide':<{lebar_nama + 2}}{'Skor Tertimbang':>16}"
    print(header)
    print("-" * len(header))
    for h in hasil:
        print(f"{h['peringkat']:<10}{h['nama_ide']:<{lebar_nama + 2}}{h['skor_tertimbang']:>16.3f}")

    seri = deteksi_seri(hasil)
    if seri:
        print()
        print("PERINGATAN: skor seri terdeteksi (putuskan lewat untung-rugi kualitatif, bukan asal pilih):")
        for grup in seri:
            print(f"   - {', '.join(grup)}")

    print()
    print(f"Bobot kriteria dipakai (total bobot = {sum(bobot.values()):g}; sumber: {sumber_bobot}):")
    for k, v in bobot.items():
        print(f"   - {k}: {v:g}")


def cmd_skor(args):
    try:
        if args.bobot:
            bobot = baca_bobot(args.bobot)
            sumber_bobot = f"file '{args.bobot}'"
        else:
            kolom = kolom_kriteria_dari_file(args.ide)
            if not kolom:
                raise DataTidakValid("file ide tidak punya kolom kriteria selain 'nama_ide'")
            if set(kolom) == set(BOBOT_DEFAULT):
                bobot = dict(BOBOT_DEFAULT)
                sumber_bobot = "default resmi skill (--bobot tidak diberikan; lihat templates/format-data-skor.md)"
            else:
                bobot = {k: 1.0 for k in kolom}
                sumber_bobot = (
                    "sama rata/semua kriteria bobot 1 (--bobot tidak diberikan dan nama kolom "
                    "tidak cocok persis dengan bobot default resmi)"
                )
        ide = baca_ide(args.ide, list(bobot.keys()))
    except DataTidakValid as e:
        print(f"Data tidak valid: {e}", file=sys.stderr)
        return 1

    hasil = hitung_skor(ide, bobot)
    cetak_tabel_skor(hasil, bobot, sumber_bobot)
    return 0


# ---------------------------------------------------------------------------
# Titik impas kasar
# ---------------------------------------------------------------------------

_AKHIRAN_PENGALI = (
    ("miliar", 1_000_000_000),
    ("m", 1_000_000_000),
    ("juta", 1_000_000),
    ("jt", 1_000_000),
    ("ribu", 1_000),
    ("rb", 1_000),
)

_POLA_RIBUAN_INDONESIA = re.compile(r"-?\d{1,3}(\.\d{3})+(,\d+)?$")


def parse_rupiah(mentah):
    """Terima angka biasa (5000000), format ribuan Indonesia (5.000.000),
    dengan/tanpa 'Rp' di depan (Rp5.000.000), dan singkatan (5jt, 15rb)."""
    asli = mentah
    s = mentah.strip()
    if not s:
        raise DataTidakValid("nilai rupiah kosong")
    s = s.replace(" ", "")
    if s[:2].lower() == "rp":
        s = s[2:]
    if not s:
        raise DataTidakValid(f"nilai rupiah tidak valid: {asli!r}")

    pengali = 1
    lower = s.lower()
    for akhiran, kali in _AKHIRAN_PENGALI:
        if lower.endswith(akhiran) and len(s) > len(akhiran):
            s = s[: -len(akhiran)]
            pengali = kali
            break

    if not s:
        raise DataTidakValid(f"nilai rupiah tidak valid: {asli!r}")

    if _POLA_RIBUAN_INDONESIA.match(s):
        # format "5.000.000" atau "5.000.000,50" -> titik ribuan, koma desimal
        s = s.replace(".", "").replace(",", ".")
    elif "," in s and "." not in s:
        # format "15000,5" -> koma desimal saja
        s = s.replace(",", ".")

    try:
        angka = float(s) * pengali
    except ValueError:
        raise DataTidakValid(
            f"nilai rupiah tidak valid: {asli!r} — pakai angka biasa (5000000), format ribuan "
            "(5.000.000), 'Rp5.000.000', atau singkatan (5jt, 15rb)"
        )
    if not math.isfinite(angka):
        raise DataTidakValid(f"nilai rupiah bukan angka wajar (nan/infinity tidak diterima): {asli!r}")
    return angka


def _tipe_rupiah_cli(mentah):
    try:
        return parse_rupiah(mentah)
    except DataTidakValid as e:
        raise argparse.ArgumentTypeError(str(e))


def format_rupiah(nilai):
    dibulatkan = round(nilai, 2)
    if dibulatkan == int(dibulatkan):
        angka = f"{int(dibulatkan):,}".replace(",", ".")
    else:
        mentah = f"{dibulatkan:,.2f}"
        bagian_bulat, bagian_desimal = mentah.split(".")
        bagian_bulat = bagian_bulat.replace(",", ".")
        angka = f"{bagian_bulat},{bagian_desimal}"
    return f"Rp{angka}"


def hitung_impas(modal, margin):
    if not math.isfinite(modal):
        raise DataTidakValid(f"modal awal bukan angka wajar (nan/infinity tidak diterima): {modal!r}")
    if not math.isfinite(margin):
        raise DataTidakValid(f"margin per unit bukan angka wajar (nan/infinity tidak diterima): {margin!r}")
    if modal <= 0:
        raise DataTidakValid(f"modal awal harus lebih besar dari 0 (nilai: {modal:g})")
    if margin <= 0:
        raise DataTidakValid(f"margin per unit harus lebih besar dari 0 (nilai: {margin:g})")
    if modal < 1:
        raise DataTidakValid(f"modal awal kurang dari Rp1 — masukkan dalam rupiah bulat (nilai: {modal:g})")
    if margin < 1:
        raise DataTidakValid(
            f"margin per unit kurang dari Rp1 — masukkan dalam rupiah bulat, atau pakai skill "
            f"'hitung-hpp' untuk perhitungan presisi (nilai: {margin:g})"
        )
    return math.ceil(modal / margin)


def cmd_impas(args):
    try:
        unit_impas = hitung_impas(args.modal, args.margin)
    except DataTidakValid as e:
        print(f"Data tidak valid: {e}", file=sys.stderr)
        return 1

    print(f"{'Modal awal':<19}: {format_rupiah(args.modal)}")
    print(f"{'Margin per unit':<19}: {format_rupiah(args.margin)}")
    print(f"{'Titik impas (BEP)':<19}: {unit_impas:,} unit".replace(",", "."))
    print()
    print("Catatan: ini perkiraan KASAR (modal awal / margin per unit, dibulatkan ke atas).")
    print("Tidak memperhitungkan biaya tetap bulanan berulang, pajak, atau penyusutan.")
    print("Untuk modal per unit presisi dari resep/BOM, pakai skill 'hitung-hpp'.")
    print("Catatan istilah: 'unit' di sini bisa berarti transaksi, pelanggan, atau siklus langganan — sesuaikan dengan jenis usahamu.")
    return 0


def buat_parser():
    p = argparse.ArgumentParser(description="Skor ide usaha tertimbang + titik impas kasar")
    sub = p.add_subparsers(dest="perintah", required=True)

    p_skor = sub.add_parser("skor", help="Hitung skor tertimbang & peringkat ide")
    p_skor.add_argument("--ide", required=True, help="Path file CSV daftar ide")
    p_skor.add_argument(
        "--bobot",
        required=False,
        default=None,
        help=(
            "Path file JSON bobot kriteria (opsional). Kalau tidak diberikan, "
            "dipakai bobot default resmi (bila nama kolom kriteria cocok) atau bobot sama rata."
        ),
    )
    p_skor.set_defaults(func=cmd_skor)

    p_impas = sub.add_parser("impas", help="Hitung titik impas kasar (unit)")
    p_impas.add_argument(
        "--modal", required=True, type=_tipe_rupiah_cli,
        help="Modal awal (Rupiah). Terima 5000000, 5.000.000, Rp5.000.000, atau 5jt",
    )
    p_impas.add_argument(
        "--margin", required=True, type=_tipe_rupiah_cli,
        help="Margin/untung per unit (Rupiah). Terima format yang sama dengan --modal",
    )
    p_impas.set_defaults(func=cmd_impas)

    return p


def main(argv=None):
    parser = buat_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
