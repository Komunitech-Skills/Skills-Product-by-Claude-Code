#!/usr/bin/env python3
"""Hitung bantu untuk membingkai ulang harga saat pelanggan bilang "mahal".

Python standar saja, lintas OS (Windows: `python` atau `py`). Semua angka memakai Decimal.
Nominal rupiah dibulatkan ke rupiah terdekat (setengah ke atas); persen hemat dibulatkan ke bawah
agar tidak pernah melebih-lebihkan.

Perintah:
  per-pakai  --harga 129000 --umur 1 --satuan tahun
  bandingkan --harga-kita 420000 --pakai-kita 1000 --harga-lain 400000 --pakai-lain 1000
             [--tambahan-kita 0] [--tambahan-lain 50000]
  cicil      --harga 3600000 --tenor 6 [--dp 600000]     (hanya jika penjual memang menawarkan cicilan)

Input uang boleh: 129000, 129.000, Rp129.000, 129rb, 1,5jt, "1.5 juta".
"""
import argparse
import re
import sys
from decimal import ROUND_FLOOR, ROUND_HALF_UP, Decimal, InvalidOperation

HARI_PER_SATUAN = {"hari": 1, "minggu": 7, "bulan": 30, "tahun": 365}
SUFIKS = (("juta", 10 ** 6), ("jt", 10 ** 6), ("ribu", 1000), ("rb", 1000), ("k", 1000))
BATAS_MAKS = Decimal("1000000000000")  # 1 triliun: di atas ini hampir pasti salah ketik


class MasukanSalah(ValueError):
    """Masukan pengguna tidak bisa dibaca."""


def _angka(teks, nama, boleh_nol=False, boleh_desimal=True):
    """Baca angka gaya Indonesia (titik ribuan, koma desimal) menjadi Decimal."""
    if teks is None:
        raise MasukanSalah(f"{nama} belum diisi.")
    t = str(teks).strip().lower().replace(" ", "")
    t = re.sub(r"^rp\.?", "", t)
    kali = 1
    for sufiks, nilai in SUFIKS:
        if t.endswith(sufiks):
            kali = nilai
            t = t[: -len(sufiks)]
            break
    if not t:
        raise MasukanSalah(f"{nama} tidak terbaca: {teks!r}.")
    if re.fullmatch(r"\d{1,3}(\.\d{3})+(,\d+)?", t):
        t = t.replace(".", "").replace(",", ".")
    elif re.fullmatch(r"\d+,\d+", t):
        t = t.replace(",", ".")
    elif re.fullmatch(r"\d+\.\d{1,2}", t) and kali > 1:
        pass  # "1.5jt" = 1,5 juta
    elif not re.fullmatch(r"\d+", t):
        raise MasukanSalah(f"{nama} tidak terbaca: {teks!r}. Tulis angka saja, mis. 129000 atau 1,5jt.")
    try:
        nilai = Decimal(t) * kali
    except InvalidOperation:
        raise MasukanSalah(f"{nama} tidak terbaca: {teks!r}.")
    if not boleh_desimal and nilai != nilai.to_integral_value():
        raise MasukanSalah(f"{nama} harus bilangan bulat: {teks!r}.")
    if nilai < 0 or (nilai == 0 and not boleh_nol):
        raise MasukanSalah(f"{nama} harus lebih dari 0: {teks!r}.")
    if nilai > BATAS_MAKS:
        raise MasukanSalah(f"{nama} terlalu besar ({teks!r}); cek lagi jumlah nol-nya.")
    return nilai


def bulat(x):
    return int(Decimal(x).quantize(Decimal(1), rounding=ROUND_HALF_UP))


def rp(x):
    n = bulat(x)
    return "Rp" + f"{n:,}".replace(",", ".")


def persen_bawah(x):
    """Persen dibulatkan ke bawah satu desimal, ditulis gaya Indonesia."""
    d = Decimal(x).quantize(Decimal("0.1"), rounding=ROUND_FLOOR)
    return str(d).replace(".", ",") + "%"


def angka_rapi(x):
    d = Decimal(x).normalize()
    teks = format(d, "f")
    return teks.replace(".", ",")


def per_pakai(harga, umur, satuan):
    h = _angka(harga, "Harga")
    u = _angka(umur, "Lama pemakaian")
    baris = [f"Harga {rp(h)}, dipakai {angka_rapi(u)} {satuan}"]
    if satuan == "pakai":
        baris.append(f"Per pemakaian: {rp(h / u)}")
        return baris
    hari = u * HARI_PER_SATUAN[satuan]
    per_hari = h / hari
    baris.append(f"Per hari: {rp(per_hari)}")
    baris.append(f"Per minggu: {rp(per_hari * 7)}")
    baris.append(f"Per bulan (30 hari): {rp(per_hari * 30)}")
    baris.append("Catatan: angka ini hanya berlaku jika benar-benar dipakai selama itu; "
                 "lama pakai harus berasal dari data penjual, bukan dikira.")
    return baris


def bandingkan(hk, pk, hl, pl, tk="0", tl="0"):
    harga_k = _angka(hk, "Harga kita")
    unit_k = _angka(pk, "Jumlah unit/pemakaian kita")
    harga_l = _angka(hl, "Harga pesaing")
    unit_l = _angka(pl, "Jumlah unit/pemakaian pesaing")
    tamb_k = _angka(tk, "Biaya tambahan kita", boleh_nol=True)
    tamb_l = _angka(tl, "Biaya tambahan pesaing", boleh_nol=True)
    total_k, total_l = harga_k + tamb_k, harga_l + tamb_l
    sat_k, sat_l = total_k / unit_k, total_l / unit_l
    baris = [
        f"Kita : {rp(total_k)} untuk {angka_rapi(unit_k)} unit -> {rp(sat_k)} per unit",
        f"Lain : {rp(total_l)} untuk {angka_rapi(unit_l)} unit -> {rp(sat_l)} per unit",
    ]
    if bulat(sat_k) == bulat(sat_l):
        baris.append("Hasil: sama per unit (selisih di bawah Rp1).")
    else:
        murah, mahal = ("kita", "pesaing") if sat_k < sat_l else ("pesaing", "kita")
        selisih = abs(sat_k - sat_l)
        pct = selisih / max(sat_k, sat_l) * 100
        baris.append(f"Hasil: {murah} lebih murah {rp(selisih)} per unit "
                     f"({persen_bawah(pct)} dari harga {mahal}).")
        if murah == "pesaing":
            baris.append("Jujur saja: per unit kita memang lebih mahal. Jawab dengan nilai lain "
                         "yang benar (kualitas, layanan, garansi, ketepatan kirim), bukan dengan angka.")
    return baris


def cicil(harga, tenor, dp="0"):
    h = _angka(harga, "Harga")
    n = _angka(tenor, "Tenor (bulan)", boleh_desimal=False)
    d = _angka(dp, "Uang muka", boleh_nol=True)
    if not (1 <= n <= 60):
        raise MasukanSalah("Tenor harus 1 sampai 60 bulan.")
    h_int, d_int, n = bulat(h), bulat(d), int(n)
    if d_int >= h_int:
        raise MasukanSalah("Uang muka harus lebih kecil dari harga.")
    sisa = h_int - d_int
    dasar = sisa // n
    terakhir = sisa - dasar * (n - 1)
    baris = [f"Harga {rp(h_int)}; uang muka {rp(d_int)}; sisa {rp(sisa)} dibagi {n} bulan, tanpa bunga"]
    if terakhir == dasar:
        baris.append(f"Cicilan: {rp(dasar)} per bulan x {n}")
    else:
        baris.append(f"Cicilan: {rp(dasar)} per bulan x {n - 1}, bulan terakhir {rp(terakhir)}")
    baris.append(f"Total dibayar: {rp(d_int + dasar * (n - 1) + terakhir)}")
    baris.append("Catatan: tawarkan cicilan hanya jika penjual memang menyediakannya dan syaratnya tertulis.")
    return baris


def bangun_parser():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="perintah", required=True)
    a = sub.add_parser("per-pakai", help="harga per hari/minggu/bulan/pemakaian")
    a.add_argument("--harga", required=True)
    a.add_argument("--umur", required=True, help="lama dipakai (angka)")
    a.add_argument("--satuan", choices=sorted(list(HARI_PER_SATUAN) + ["pakai"]), required=True)
    b = sub.add_parser("bandingkan", help="harga per unit kita vs pesaing")
    b.add_argument("--harga-kita", required=True)
    b.add_argument("--pakai-kita", required=True, help="jumlah unit/pemakaian yang didapat")
    b.add_argument("--harga-lain", required=True)
    b.add_argument("--pakai-lain", required=True)
    b.add_argument("--tambahan-kita", default="0", help="ongkir/biaya lain di sisi kita")
    b.add_argument("--tambahan-lain", default="0", help="ongkir/biaya lain di sisi pesaing")
    c = sub.add_parser("cicil", help="cicilan tanpa bunga (hanya jika penjual menawarkan)")
    c.add_argument("--harga", required=True)
    c.add_argument("--tenor", required=True)
    c.add_argument("--dp", default="0")
    return p


def main(argv=None):
    args = bangun_parser().parse_args(argv)
    try:
        if args.perintah == "per-pakai":
            baris = per_pakai(args.harga, args.umur, args.satuan)
        elif args.perintah == "bandingkan":
            baris = bandingkan(args.harga_kita, args.pakai_kita, args.harga_lain, args.pakai_lain,
                               args.tambahan_kita, args.tambahan_lain)
        else:
            baris = cicil(args.harga, args.tenor, args.dp)
    except MasukanSalah as e:
        print(f"Masukan tidak valid: {e}", file=sys.stderr)
        return 2
    print("\n".join(baris))
    return 0


if __name__ == "__main__":
    sys.exit(main())
