#!/usr/bin/env python3
"""Hitung hasil uji murah validasi ide produk baru: konversi, klasifikasi
LULUS/LULUS BERSYARAT/GAGAL, dan (opsional) margin & balik modal biaya uji.

Rumus:
  konversi (%) = (preorder / ditawari) * 100   -> dibulatkan 1 desimal

  Klasifikasi (ambang default, bisa dioverride):
    konversi >= ambang_lulus (default 15%)               -> LULUS
    ambang_bersyarat <= konversi < ambang_lulus (def. 8%) -> LULUS BERSYARAT
    konversi < ambang_bersyarat                            -> GAGAL

  Jika --hpp diisi:
    margin_per_unit   = harga - hpp
    total_margin      = margin_per_unit * preorder
    Jika --biaya-uji diisi:
      selisih_modal   = total_margin - biaya_uji   (positif = sudah balik modal uji)

Rupiah dibulatkan ke rupiah terdekat. Hanya library standar Python 3.8+.

Field UANG (--harga, --hpp, --biaya-uji) menerima format Indonesia:
  angka polos      : 25000
  "Rp" + titik ribuan: Rp25.000, 150.000, 1.234.567
  singkatan        : 25rb, 25ribu, 1jt, 1juta
  desimal + singkatan: 1,5jt (artinya 1.500.000), 2,5rb (artinya 2500)
Format yang TIDAK JELAS (mis. "25.5" atau "1.234,56" atau titik+koma campur
tanpa pola baku) DITOLAK dengan pesan error, bukan ditebak — tulis ulang
sebagai angka polos atau salah satu format di atas.

Contoh:
  python3 hitung_validasi.py --ditawari 20 --preorder 4 --harga 25.000 --hpp 12rb --biaya-uji 50000
  python3 hitung_validasi.py --file data-uji.json
"""
import argparse
import json
import re
import sys
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation


def rupiah(nilai: Decimal) -> str:
    bulat = nilai.quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    return f"Rp{bulat:,.0f}".replace(",", ".")


def ke_desimal(nilai, nama):
    try:
        return Decimal(str(nilai))
    except (InvalidOperation, TypeError, ValueError):
        raise SystemExit(f"Error: '{nama}' harus berupa angka, dapat: {nilai!r}")


_SARAN_FORMAT_UANG = (
    "tulis angka polos (mis. 25000), format Rupiah bertitik ribuan (mis. 25.000 "
    "atau Rp25.000), atau singkatan (mis. 25rb, 1jt, 1,5jt) — jangan campur titik "
    "& koma dan jangan tulis desimal ganjil seperti 25.5."
)


def parse_uang(nilai, nama):
    """Parse field uang (harga/hpp/biaya-uji) dengan format Indonesia.

    Angka int/float dari JSON diterima apa adanya (tidak ambigu). String
    (dari CLI atau JSON) diparse: dukung prefiks 'Rp', titik sebagai
    pemisah ribuan (kelompok 3 digit), koma sebagai desimal, dan singkatan
    'rb'/'ribu' (x1.000) / 'jt'/'juta' (x1.000.000). Pola yang tidak jelas
    ditolak dengan pesan error eksplisit, tidak pernah ditebak.
    """
    if isinstance(nilai, (int, float)) and not isinstance(nilai, bool):
        return Decimal(str(nilai))
    if not isinstance(nilai, str):
        raise SystemExit(f"Error: '{nama}' harus berupa angka, dapat: {nilai!r}")

    asli = nilai
    s = nilai.strip()
    if s == "":
        raise SystemExit(f"Error: '{nama}' kosong. {_SARAN_FORMAT_UANG}")

    # Prefiks "Rp"/"rp."/"IDR" (opsional, boleh diikuti spasi)
    s = re.sub(r"(?i)^\s*(rp\.?|idr)\s*", "", s).strip()
    if s == "":
        raise SystemExit(f"Error: '{nama}' ({asli!r}) tidak berisi angka. {_SARAN_FORMAT_UANG}")

    # Singkatan ribu/juta di akhir
    pengali = Decimal(1)
    m = re.search(r"(?i)\s*(ribu|rb|juta|jt)\s*$", s)
    if m:
        satuan = m.group(1).lower()
        pengali = Decimal(1000) if satuan in ("ribu", "rb") else Decimal(1000000)
        s = s[: m.start()].strip()
    if s == "":
        raise SystemExit(f"Error: '{nama}' ({asli!r}) tidak ada angka sebelum singkatan. {_SARAN_FORMAT_UANG}")

    if "." in s and "," in s:
        raise SystemExit(
            f"Error: '{nama}' ({asli!r}) tidak jelas — mengandung titik DAN koma sekaligus. {_SARAN_FORMAT_UANG}"
        )

    if "," in s:
        # Koma = pemisah desimal (dipakai bersama singkatan rb/jt, mis. "1,5jt")
        if not re.fullmatch(r"\d+,\d{1,2}", s):
            raise SystemExit(
                f"Error: '{nama}' ({asli!r}) format koma tidak dikenali. {_SARAN_FORMAT_UANG}"
            )
        if pengali == Decimal(1):
            raise SystemExit(
                f"Error: '{nama}' ({asli!r}) memakai koma tanpa singkatan rb/jt — tidak jelas maksudnya "
                f"desimal atau ribuan yang salah tulis. {_SARAN_FORMAT_UANG}"
            )
        angka = Decimal(s.replace(",", "."))
    elif "." in s:
        kelompok = s.split(".")
        ribuan_valid = (
            len(kelompok) >= 2
            and kelompok[0].isdigit()
            and 1 <= len(kelompok[0]) <= 3
            and all(bagian.isdigit() and len(bagian) == 3 for bagian in kelompok[1:])
        )
        if ribuan_valid:
            angka = Decimal("".join(kelompok))
        else:
            raise SystemExit(
                f"Error: '{nama}' ({asli!r}) tidak jelas apakah titik ini pemisah ribuan atau desimal "
                f"(mis. '25.5' bisa berarti 25,5 atau salah tulis format ribuan). {_SARAN_FORMAT_UANG}"
            )
    else:
        if not s.isdigit():
            raise SystemExit(f"Error: '{nama}' ({asli!r}) bukan angka yang dikenali. {_SARAN_FORMAT_UANG}")
        angka = Decimal(s)

    return angka * pengali


def parse_args():
    p = argparse.ArgumentParser(description="Hitung hasil uji validasi ide produk baru.")
    p.add_argument("--file", help="File JSON berisi field: ditawari, preorder, harga, hpp (opsional), biaya_uji (opsional)")
    p.add_argument("--ditawari", type=str, help="Jumlah orang/tampilan yang ditawari")
    p.add_argument("--preorder", type=str, help="Jumlah pre-order/pembeli yang benar-benar memesan")
    p.add_argument("--harga", type=str, help="Harga jual rencana per unit (Rupiah)")
    p.add_argument("--hpp", type=str, default=None, help="Modal/HPP per unit (Rupiah), opsional")
    p.add_argument("--biaya-uji", type=str, default=None, help="Total biaya untuk menjalankan uji (bahan sampel, ongkir, pulsa), opsional")
    p.add_argument("--ambang-lulus", type=str, default="15", help="Persen konversi minimal untuk LULUS (default 15)")
    p.add_argument("--ambang-bersyarat", type=str, default="8", help="Persen konversi minimal untuk LULUS BERSYARAT (default 8)")
    p.add_argument("--min-sampel", type=str, default="20", help="Jumlah ditawari minimal agar hasil dianggap cukup andal (default 20)")
    return p.parse_args()


def main():
    args = parse_args()
    data = {}
    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            raise SystemExit(f"Error: file '{args.file}' tidak ditemukan.")
        except json.JSONDecodeError as e:
            raise SystemExit(f"Error: file JSON '{args.file}' tidak valid ({e}).")

    def ambil(nama_cli, nama_json, wajib=True, default=None):
        nilai_cli = getattr(args, nama_cli, None)
        if nilai_cli is not None:
            return nilai_cli
        if nama_json in data:
            return data[nama_json]
        if wajib:
            raise SystemExit(f"Error: '{nama_json}' wajib diisi (lewat --{nama_cli.replace('_','-')} atau field '{nama_json}' di file JSON).")
        return default

    ditawari = ke_desimal(ambil("ditawari", "ditawari"), "ditawari")
    preorder = ke_desimal(ambil("preorder", "preorder"), "preorder")
    harga = parse_uang(ambil("harga", "harga"), "harga")
    hpp_raw = ambil("hpp", "hpp", wajib=False)
    biaya_uji_raw = ambil("biaya_uji", "biaya_uji", wajib=False)
    ambang_lulus = ke_desimal(ambil("ambang_lulus", "ambang_lulus", wajib=False, default=args.ambang_lulus), "ambang-lulus")
    ambang_bersyarat = ke_desimal(ambil("ambang_bersyarat", "ambang_bersyarat", wajib=False, default=args.ambang_bersyarat), "ambang-bersyarat")
    min_sampel = ke_desimal(ambil("min_sampel", "min_sampel", wajib=False, default=args.min_sampel), "min-sampel")

    # --- validasi ---
    if ditawari <= 0:
        raise SystemExit("Error: 'ditawari' harus lebih dari 0 (tidak bisa hitung konversi dari 0 orang).")
    if preorder < 0:
        raise SystemExit("Error: 'preorder' tidak boleh negatif.")
    if preorder > ditawari:
        raise SystemExit(f"Error: 'preorder' ({preorder}) tidak boleh lebih besar dari 'ditawari' ({ditawari}) — periksa kembali data.")
    if harga <= 0:
        raise SystemExit("Error: 'harga' harus lebih dari 0.")
    if ambang_bersyarat > ambang_lulus:
        raise SystemExit("Error: 'ambang-bersyarat' tidak boleh lebih besar dari 'ambang-lulus'.")

    hpp = None
    if hpp_raw is not None:
        hpp = parse_uang(hpp_raw, "hpp")
        if hpp < 0:
            raise SystemExit("Error: 'hpp' tidak boleh negatif.")
        if hpp >= harga:
            print(f"PERINGATAN: hpp ({rupiah(hpp)}) >= harga jual ({rupiah(harga)}) — margin per unit nol atau negatif, periksa kembali harga/HPP.\n")

    biaya_uji = None
    if biaya_uji_raw is not None:
        biaya_uji = parse_uang(biaya_uji_raw, "biaya-uji")
        if biaya_uji < 0:
            raise SystemExit("Error: 'biaya-uji' tidak boleh negatif.")

    # --- hitung konversi ---
    konversi = (preorder / ditawari * Decimal(100)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)

    if konversi >= ambang_lulus:
        klasifikasi = "LULUS"
        saran = "Datanya cukup mendukung untuk LANJUT: mulai produksi/investasi bertahap. Lanjutkan ke skill hitung-hpp (HPP & BEP rinci) dan harga-jual-marketplace (harga jual final)."
    elif konversi >= ambang_bersyarat:
        klasifikasi = "LULUS BERSYARAT"
        saran = "Ada minat tapi belum kuat — UBAH satu hal dulu (harga, penawaran/kemasan, atau target pembeli), lalu uji ulang 7 hari dengan hipotesis baru."
    else:
        klasifikasi = "GAGAL"
        saran = "Data belum mendukung ide ini dalam bentuk sekarang — pertimbangkan HENTIKAN atau pivot besar. Kumpulkan alasan penolakan dari form pencatatan sebagai bahan ide berikutnya (brainstorming-ide-usaha)."

    print("=== HASIL VALIDASI IDE ===")
    print(f"Ditawari       : {ditawari:g} orang/tampilan")
    print(f"Pre-order/beli : {preorder:g}")
    print(f"Konversi       : {konversi}%")
    if ditawari < min_sampel:
        print(f"PERINGATAN: jumlah ditawari ({ditawari:g}) di bawah ambang sampel minimal ({min_sampel:g}) — anggap ini INDIKASI AWAL, bukan kesimpulan final.")
    print(f"Ambang         : LULUS >= {ambang_lulus:g}% | LULUS BERSYARAT >= {ambang_bersyarat:g}% | GAGAL < {ambang_bersyarat:g}%")
    print(f"Klasifikasi    : {klasifikasi}")
    print(f"Saran          : {saran}")

    if hpp is not None:
        margin_per_unit = harga - hpp
        total_margin = margin_per_unit * preorder
        print("\n=== MARGIN & BIAYA UJI ===")
        print(f"Margin per unit      : {rupiah(margin_per_unit)}  ({rupiah(harga)} - {rupiah(hpp)})")
        print(f"Total margin preorder: {rupiah(total_margin)}  ({margin_per_unit:g} x {preorder:g} unit)")
        if biaya_uji is not None:
            selisih = total_margin - biaya_uji
            status_modal = "SUDAH balik modal uji" if selisih >= 0 else "BELUM balik modal uji"
            print(f"Biaya uji            : {rupiah(biaya_uji)}")
            print(f"Selisih              : {rupiah(selisih)}  ({status_modal})")


if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        if e.code and not isinstance(e.code, int):
            print(str(e.code), file=sys.stderr)
            sys.exit(1)
        raise
