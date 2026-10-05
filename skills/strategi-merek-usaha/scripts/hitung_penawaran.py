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
Nominal boleh format Indonesia: 38000, 38.000, Rp38.000, 38rb, 1,5jt, 38.000,50. Yang ambigu (38.5) -> GAGAL.
Persen: 10, 10%, 7,5. Keluar kode 0 bila sukses, 2 bila input salah.
"""
import argparse
import json
import math
import re
import sys


class InputSalah(Exception):
    pass


def bulat(x):
    return int(math.floor(x + 0.5))


_SUFIKS = {"rb": 1_000, "ribu": 1_000, "k": 1_000, "jt": 1_000_000, "juta": 1_000_000}


def baca_rupiah(teks, nama="nilai"):
    """Baca nominal format Indonesia. Terima: 38000, 38.000, 1.500.000, Rp38.000, Rp 38.000,-,
    38.000,50 (koma = desimal), 38,5, 38rb, 38 ribu, 1,5jt, 1.5jt, 2 juta.
    Ambigu (mis. 38.5, 38,000, 1.500rb, 1,500.50) -> InputSalah, bukan ditebak."""
    t = str(teks).strip().lower()
    asli = str(teks).strip()
    t = re.sub(r"^rp\.?\s*", "", t)
    t = re.sub(r",-$", "", t).replace(" ", "")
    if t.startswith("-"):
        raise InputSalah(f"{nama} tidak boleh negatif: '{asli}'")
    m = re.match(r"^([0-9.,]+?)(rb|ribu|k|jt|juta)?$", t)
    if not m or not re.search(r"\d", m.group(1)):
        raise InputSalah(f"{nama} '{asli}' bukan nominal yang dikenal (contoh: 38000, 38.000, Rp38.000, 38rb, 1,5jt)")
    angka_t, suf = m.group(1), m.group(2)
    ambigu = InputSalah(f"{nama} '{asli}' ambigu (titik/koma bisa ribuan atau desimal). "
                        "Tulis tanpa pemisah (38000), titik ribuan (38.000), atau koma desimal (38,5)")
    if suf:
        if re.fullmatch(r"\d+", angka_t):
            nilai = float(angka_t)
        elif re.fullmatch(r"\d+,\d{1,2}", angka_t) or re.fullmatch(r"\d+\.\d{1,2}", angka_t):
            nilai = float(angka_t.replace(",", "."))
        else:
            raise ambigu
        return nilai * _SUFIKS[suf]
    if re.fullmatch(r"\d+", angka_t):
        return float(angka_t)
    if re.fullmatch(r"[1-9]\d{0,2}(\.\d{3})+(,\d+)?", angka_t):
        return float(angka_t.replace(".", "").replace(",", "."))
    if re.fullmatch(r"\d+,\d{1,2}", angka_t):
        return float(angka_t.replace(",", "."))
    raise ambigu


def baca_persen(teks, nama="nilai"):
    t = str(teks).strip().replace(" ", "")
    if t.endswith("%"):
        t = t[:-1]
    if re.fullmatch(r"\d+([.,]\d+)?", t):
        return float(t.replace(",", "."))
    raise InputSalah(f"--{nama} '{teks}' bukan persen yang dikenal (contoh: 10, 7,5, 10%)")


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
        biaya = baca_rupiah(b, f"biaya bonus '{n.strip()}'")
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
    p.add_argument("--harga", type=str, required=True, help="harga normal per unit, mis. 38000, 38.000, Rp38.000, 38rb")
    p.add_argument("--hpp", type=str, required=True, help="modal per unit (Rp)")
    p.add_argument("--diskon", type=str, default="0", help="diskon persen")
    p.add_argument("--platform", type=str, default="0", help="total potongan marketplace/payment persen")
    p.add_argument("--bonus", default="", help='"Nama=biaya modal;Nama2=biaya"')
    p.add_argument("--refund", type=str, default="0", help="perkiraan persen pembeli minta uang kembali")
    p.add_argument("--margin-minimal", type=str, default=None, help="target margin minimal persen")
    p.add_argument("--format", choices=["teks", "json"], default="teks")
    try:
        a = p.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0
    try:
        harga = angka("harga", baca_rupiah(a.harga, "--harga"), 0.0)
        if harga <= 0:
            raise InputSalah("--harga harus lebih dari 0")
        hpp = angka("hpp", baca_rupiah(a.hpp, "--hpp"), 0.0)
        diskon = angka("diskon", baca_persen(a.diskon, "diskon"), 0.0, 100.0)
        platform = angka("platform", baca_persen(a.platform, "platform"), 0.0, 100.0)
        refund = angka("refund", baca_persen(a.refund, "refund"), 0.0, 100.0)
        mm = None if a.margin_minimal is None else angka("margin-minimal", baca_persen(a.margin_minimal, "margin-minimal"), 0.0, 99.0)
        bonus = baca_bonus(a.bonus)
        if diskon >= 100:
            raise InputSalah("--diskon 100 berarti gratis; pakai angka di bawah 100")
        r = hitung(harga, bulat(hpp), diskon, platform, bonus, refund, mm)
    except InputSalah as e:
        print(f"GAGAL: {e}", file=sys.stderr)
        return 2
    peringatan = []
    if harga < 1000:
        peringatan.append(f"PERINGATAN: harga {rp(bulat(harga))} sangat kecil. Bila maksud Anda ribuan, tulis 38000 atau 38rb.")
    if 0 < hpp < 100:
        peringatan.append(f"PERINGATAN: HPP {rp(bulat(hpp))} sangat kecil. Bila maksud Anda ribuan, tulis 17000 atau 17rb.")
    r["peringatan"] = peringatan
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
    for w in peringatan:
        print(w)
    if diskon > 50:
        print("Catatan: diskon > 50% -- pastikan harga normal pernah benar-benar berlaku (lihat SKILL.md, kelangkaan jujur).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
