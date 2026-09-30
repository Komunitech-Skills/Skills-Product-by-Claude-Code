#!/usr/bin/env python3
"""Hitung laba per unit untuk sebuah penawaran (harga, diskon, bonus, garansi). Python standar saja.

Pakai:
  python3 scripts/hitung_penawaran.py --harga 45000 --hpp 22000 --diskon 10 --platform 8 \
      --bonus "Stiker=500;Kartu resep=800" --refund 3 --margin-minimal 20
(Windows: ganti python3 dengan python atau py.)

Rumus (rupiah dibulatkan ke rupiah terdekat, .5 ke atas):
  harga_tayang = harga x (1 - diskon/100)
  biaya_platform = harga_tayang x platform/100
  biaya_bonus = jumlah biaya MODAL tiap bonus per unit (bukan harga jual bonus)
  biaya_refund = harga_tayang x refund/100   (perkiraan pengembalian dana; barang kembali tidak dihitung)
  laba = harga_tayang - biaya_platform - hpp - biaya_bonus - biaya_refund
  margin = laba / harga_tayang
Dengan --margin-minimal M: dihitung batas biaya bonus per unit agar margin >= M%.
Keluar kode 0 bila sukses, 2 bila input salah.
"""
import argparse
import json
import math
import sys


class InputSalah(Exception):
    pass


def bulat(x):
    return int(math.floor(x + 0.5))


def angka(nama, v, minimum=0.0, maksimum=None):
    if v is None or v != v or v in (float("inf"), float("-inf")):
        raise InputSalah(f"--{nama} harus angka biasa")
    if v < minimum or (maksimum is not None and v > maksimum):
        rentang = f"{minimum:g} sampai {maksimum:g}" if maksimum is not None else f"{minimum:g} atau lebih"
        raise InputSalah(f"--{nama} harus {rentang}")
    return v


def baca_bonus(teks):
    hasil = []
    for bag in [x for x in teks.split(";") if x.strip()]:
        if "=" not in bag:
            raise InputSalah(f"bonus '{bag.strip()}' harus berbentuk Nama=biaya")
        n, b = bag.rsplit("=", 1)
        try:
            biaya = float(b.strip().replace("_", ""))
        except ValueError:
            raise InputSalah(f"biaya bonus '{n.strip()}' bukan angka: '{b.strip()}' (rupiah tanpa titik ribuan)")
        if biaya != biaya or biaya < 0 or biaya == float("inf"):
            raise InputSalah(f"biaya bonus '{n.strip()}' harus 0 atau lebih")
        if not n.strip():
            raise InputSalah("nama bonus kosong")
        hasil.append((n.strip(), bulat(biaya)))
    return hasil


def hitung(harga, hpp, diskon=0.0, platform=0.0, bonus=(), refund=0.0, margin_min=None):
    tayang = bulat(harga * (1 - diskon / 100))
    fee = bulat(tayang * platform / 100)
    b = sum(x[1] for x in bonus)
    rf = bulat(tayang * refund / 100)
    laba = tayang - fee - hpp - b - rf
    margin = (laba / tayang * 100) if tayang > 0 else float("nan")
    hasil = {"harga_tayang": tayang, "biaya_platform": fee, "hpp": hpp, "biaya_bonus": b,
             "biaya_refund": rf, "laba_per_unit": laba,
             "margin_persen": None if margin != margin else round(margin, 1), "bonus": bonus}
    if margin_min is not None:
        # laba minimal = tayang x M/100 ; ruang bonus = laba tanpa bonus - laba minimal (dibulatkan ke bawah)
        tanpa_bonus = tayang - fee - hpp - rf
        ruang = math.floor(tanpa_bonus - tayang * margin_min / 100)
        hasil["ruang_bonus_maks"] = max(ruang, 0)
        hasil["memenuhi_margin_minimal"] = laba >= tayang * margin_min / 100 - 1e-9
    return hasil


def rp(n):
    s = f"{abs(n):,}".replace(",", ".")
    return ("-" if n < 0 else "") + "Rp" + s


def main(argv=None):
    p = argparse.ArgumentParser(description="Laba per unit penawaran", allow_abbrev=False)
    p.add_argument("--harga", type=float, required=True, help="harga normal per unit (Rp)")
    p.add_argument("--hpp", type=float, required=True, help="modal per unit (Rp)")
    p.add_argument("--diskon", type=float, default=0.0, help="diskon persen")
    p.add_argument("--platform", type=float, default=0.0, help="total potongan marketplace/payment persen")
    p.add_argument("--bonus", default="", help='"Nama=biaya modal;Nama2=biaya"')
    p.add_argument("--refund", type=float, default=0.0, help="perkiraan persen pembeli minta uang kembali")
    p.add_argument("--margin-minimal", type=float, default=None, help="target margin minimal persen")
    p.add_argument("--format", choices=["teks", "json"], default="teks")
    try:
        a = p.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0
    try:
        harga = angka("harga", a.harga, 0.0)
        if harga <= 0:
            raise InputSalah("--harga harus lebih dari 0")
        hpp = angka("hpp", a.hpp, 0.0)
        diskon = angka("diskon", a.diskon, 0.0, 100.0)
        platform = angka("platform", a.platform, 0.0, 100.0)
        refund = angka("refund", a.refund, 0.0, 100.0)
        mm = None if a.margin_minimal is None else angka("margin-minimal", a.margin_minimal, 0.0, 99.0)
        bonus = baca_bonus(a.bonus)
        if diskon >= 100:
            raise InputSalah("--diskon 100 berarti gratis; pakai angka di bawah 100")
        r = hitung(harga, bulat(hpp), diskon, platform, bonus, refund, mm)
    except InputSalah as e:
        print(f"GAGAL: {e}", file=sys.stderr)
        return 2
    if a.format == "json":
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0
    print(f"Harga tayang        : {rp(r['harga_tayang'])}" + (f" (diskon {diskon:g}%)" if diskon else ""))
    print(f"Potongan platform   : -{rp(r['biaya_platform'])}")
    print(f"HPP                 : -{rp(r['hpp'])}")
    for n, b in bonus:
        print(f"Bonus {n:<14}: -{rp(b)} (biaya modal)")
    if refund:
        print(f"Perkiraan refund {refund:g}% : -{rp(r['biaya_refund'])}")
    print(f"LABA per unit       : {rp(r['laba_per_unit'])}" +
          (f" (margin {r['margin_persen']:.1f}%)" if r["margin_persen"] is not None else ""))
    if r["laba_per_unit"] < 0:
        print("PERINGATAN: RUGI per unit. Kurangi diskon/bonus atau naikkan harga.")
    if mm is not None:
        print(f"Ruang biaya bonus maksimum agar margin >= {mm:g}%: {rp(r['ruang_bonus_maks'])} per unit; "
              + ("memenuhi." if r["memenuhi_margin_minimal"] else "BELUM memenuhi."))
    if diskon > 50:
        print("Catatan: diskon > 50% -- pastikan harga normal pernah benar-benar berlaku (lihat SKILL.md, kelangkaan jujur).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
