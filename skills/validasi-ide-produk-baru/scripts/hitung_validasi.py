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

ATURAN PENTING (v1.0.4): hanya PESANAN BERKOMITMEN (pre-order yang sudah
transfer/DP/bayar, atau order yang benar-benar masuk) yang boleh diisi ke
--preorder dan ikut hitungan konversi, margin, dan balik modal. SINYAL MINAT
(vote polling, like, komentar "mau", balasan "minat" tanpa bayar) diisi ke
--minat: hanya dilaporkan terpisah, TIDAK PERNAH dihitung sebagai pesanan
atau pendapatan.

Mode banyak kanal (file JSON):
  {"harga": 18000, "hpp": 9500, "biaya_uji": 60000,
   "kanal": [{"nama": "Broadcast WA", "ditawari": 45, "preorder": 4},
             {"nama": "Polling IG", "ditawari": 380, "minat": 52}]}
  Kanal yang hanya punya "minat" tidak ikut klasifikasi maupun hitungan uang.

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
    tanda = "-" if bulat < 0 else ""
    return f"{tanda}Rp{abs(bulat):,.0f}".replace(",", ".")


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
    p.add_argument("--preorder", type=str, help="Jumlah PESANAN BERKOMITMEN (sudah transfer/DP/bayar/order masuk). JANGAN isi vote/like/komentar")
    p.add_argument("--minat", type=str, default=None, help="Sinyal minat tanpa bayar (vote polling, like, komentar 'mau'). Dilaporkan terpisah, TIDAK dihitung sebagai pesanan")
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

    harga = parse_uang(ambil("harga", "harga"), "harga")
    hpp_raw = ambil("hpp", "hpp", wajib=False)
    biaya_uji_raw = ambil("biaya_uji", "biaya_uji", wajib=False)
    ambang_lulus = ke_desimal(ambil("ambang_lulus", "ambang_lulus", wajib=False, default=args.ambang_lulus), "ambang-lulus")
    ambang_bersyarat = ke_desimal(ambil("ambang_bersyarat", "ambang_bersyarat", wajib=False, default=args.ambang_bersyarat), "ambang-bersyarat")
    min_sampel = ke_desimal(ambil("min_sampel", "min_sampel", wajib=False, default=args.min_sampel), "min-sampel")

    # --- kumpulkan kanal ---
    if args.ditawari is None and args.preorder is None and args.minat is None and "kanal" in data:
        if not isinstance(data["kanal"], list) or not data["kanal"]:
            raise SystemExit("Error: 'kanal' di file JSON harus berupa daftar (list) yang tidak kosong.")
        kanal_mentah = data["kanal"]
    else:
        kanal_mentah = [{
            "nama": "Uji",
            "ditawari": ambil("ditawari", "ditawari"),
            "preorder": ambil("preorder", "preorder", wajib=False),
            "minat": ambil("minat", "minat", wajib=False),
        }]
        if kanal_mentah[0]["preorder"] is None and kanal_mentah[0]["minat"] is None:
            raise SystemExit("Error: 'preorder' wajib diisi (jumlah pesanan yang sudah transfer/DP/bayar; isi 0 bila belum ada). Vote/like/komentar diisi ke --minat.")

    kanal = []
    for i, k in enumerate(kanal_mentah, 1):
        if not isinstance(k, dict):
            raise SystemExit(f"Error: kanal ke-{i} harus berupa objek JSON.")
        nama = str(k.get("nama") or f"Kanal {i}")
        if k.get("ditawari") is None:
            raise SystemExit(f"Error: kanal '{nama}' belum punya 'ditawari'.")
        d = ke_desimal(k["ditawari"], f"ditawari ({nama})")
        po = None if k.get("preorder") is None else ke_desimal(k["preorder"], f"preorder ({nama})")
        mn = None if k.get("minat") is None else ke_desimal(k["minat"], f"minat ({nama})")
        if po is None and mn is None:
            raise SystemExit(f"Error: kanal '{nama}' harus punya 'preorder' (pesanan berkomitmen) atau 'minat' (vote/like).")
        if d <= 0:
            raise SystemExit(f"Error: 'ditawari' ({nama}) harus lebih dari 0 (tidak bisa hitung konversi dari 0 orang).")
        for label, v in (("preorder", po), ("minat", mn)):
            if v is not None:
                if v < 0:
                    raise SystemExit(f"Error: '{label}' ({nama}) tidak boleh negatif.")
                if v > d:
                    raise SystemExit(f"Error: '{label}' ({nama}) = {v:g} tidak boleh lebih besar dari 'ditawari' ({d:g}) — periksa kembali data.")
        kanal.append({"nama": nama, "ditawari": d, "preorder": po, "minat": mn})

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

    komit = [k for k in kanal if k["preorder"] is not None]
    hanya_minat = [k for k in kanal if k["preorder"] is None]

    def pct(a, b):
        return (a / b * Decimal(100)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)

    print("=== HASIL VALIDASI IDE ===")
    print("Yang dihitung sebagai pesanan: HANYA pre-order yang sudah transfer/DP/bayar atau order masuk.")
    if len(kanal) > 1:
        print("\nPer kanal:")
        for k in kanal:
            bagian = [f"ditawari {k['ditawari']:g}"]
            if k["preorder"] is not None:
                bagian.append(f"pesanan {k['preorder']:g} ({pct(k['preorder'], k['ditawari'])}%)")
            if k["minat"] is not None:
                bagian.append(f"minat {k['minat']:g} ({pct(k['minat'], k['ditawari'])}%, BUKAN pesanan)")
            print(f"  - {k['nama']}: " + ", ".join(bagian))
        print()

    total_minat = sum((k["minat"] for k in kanal if k["minat"] is not None), Decimal(0))
    if not komit:
        print("Pesanan berkomitmen : 0 (belum ada kanal dengan pre-order/DP/bayar)")
        print(f"Sinyal minat        : {total_minat:g} (vote/like/komentar — TIDAK dihitung sebagai pesanan)")
        print("Klasifikasi         : BELUM BISA DINILAI")
        print("Saran               : Minat belum sama dengan membeli. Ubah minat jadi pesanan dulu: buka pre-order dengan DP/transfer ke yang vote/komentar, lalu hitung ulang.")
        if biaya_uji is not None:
            print(f"\nSelisih biaya uji   : 0 - {rupiah(biaya_uji)} = {rupiah(-biaya_uji)} (BELUM balik modal uji; minat tidak menghasilkan uang)")
        return

    ditawari = sum((k["ditawari"] for k in komit), Decimal(0))
    preorder = sum((k["preorder"] for k in komit), Decimal(0))
    konversi = pct(preorder, ditawari)

    if konversi >= ambang_lulus:
        klasifikasi = "LULUS"
        saran = "Datanya cukup mendukung untuk LANJUT: mulai produksi/investasi bertahap. Lanjutkan ke skill hitung-hpp (HPP & BEP rinci) dan harga-jual-marketplace (harga jual final)."
    elif konversi >= ambang_bersyarat:
        klasifikasi = "LULUS BERSYARAT"
        saran = "Ada minat tapi belum kuat — UBAH satu hal dulu (harga, penawaran/kemasan, atau target pembeli), lalu uji ulang 7 hari dengan hipotesis baru."
    else:
        klasifikasi = "GAGAL"
        saran = "Data belum mendukung ide ini dalam bentuk sekarang — pertimbangkan HENTIKAN atau pivot besar. Kumpulkan alasan penolakan dari form pencatatan sebagai bahan ide berikutnya (brainstorming-ide-usaha)."

    nama_komit = ", ".join(k["nama"] for k in komit) if len(kanal) > 1 else None
    print(f"Ditawari       : {ditawari:g} orang/tampilan" + (f"  (kanal pesanan: {nama_komit})" if nama_komit else ""))
    print(f"Pre-order/beli : {preorder:g}  (pesanan berkomitmen saja)")
    print(f"Konversi       : {konversi}%  (= {preorder:g} / {ditawari:g} x 100)")
    if total_minat > 0 or any(k["minat"] is not None for k in kanal):
        catatan = f" — dari kanal {', '.join(k['nama'] for k in hanya_minat)}" if hanya_minat and len(kanal) > 1 else ""
        print(f"Sinyal minat   : {total_minat:g} (vote/like/komentar{catatan}) — dilaporkan terpisah, TIDAK ikut konversi, margin, atau balik modal")
    if ditawari < min_sampel:
        print(f"PERINGATAN: jumlah ditawari ({ditawari:g}) di bawah ambang sampel minimal ({min_sampel:g}) — anggap ini INDIKASI AWAL, bukan kesimpulan final.")
    if ditawari >= 100 and konversi > 30:
        print("PERINGATAN: konversi > 30% dari >= 100 orang tidak biasa — pastikan angka pre-order adalah pesanan yang sudah bayar/DP, bukan vote/like/komentar.")
    print(f"Ambang         : LULUS >= {ambang_lulus:g}% | LULUS BERSYARAT >= {ambang_bersyarat:g}% | GAGAL < {ambang_bersyarat:g}%")
    print(f"Klasifikasi    : {klasifikasi}")
    print(f"Saran          : {saran}")

    if hpp is not None:
        margin_per_unit = harga - hpp
        total_margin = margin_per_unit * preorder
        print("\n=== MARGIN & BIAYA UJI (hanya dari pesanan berkomitmen) ===")
        print(f"Margin per unit      : {rupiah(margin_per_unit)}  (= {rupiah(harga)} - {rupiah(hpp)})")
        print(f"Total margin preorder: {rupiah(total_margin)}  (= {rupiah(margin_per_unit)} x {preorder:g} unit)")
        if biaya_uji is not None:
            selisih = total_margin - biaya_uji
            status_modal = "SUDAH balik modal uji" if selisih >= 0 else "BELUM balik modal uji"
            print(f"Biaya uji            : {rupiah(biaya_uji)}")
            print(f"Selisih              : {rupiah(selisih)}  (= {rupiah(total_margin)} - {rupiah(biaya_uji)}; {status_modal})")

if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        if e.code and not isinstance(e.code, int):
            print(str(e.code), file=sys.stderr)
            sys.exit(1)
        raise
