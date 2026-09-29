#!/usr/bin/env python3
"""Hitung fee & PPh final aset kripto (Decimal) -- rekap dari bot/transaksi.csv atau satu transaksi.

Dasar: PMK 50/2025 (berlaku 1 Agustus 2025) -- PPh Pasal 22 final atas penjualan aset kripto:
  0,21% dari nilai transaksi lewat PAKD/PPMSE dalam negeri (dipungut otomatis oleh bursa),
  1%    lewat platform luar negeri (bila platform tidak ditunjuk DJP, penjual menyetor sendiri).
Penyerahan aset kripto tidak dikenai PPN (Pasal 2 ayat (1) PMK 50/2025). Pembeli tidak dikenai PPh ini.
Sumber: https://www.pajak.go.id/index.php/en/node/118105 & https://www.pajak.go.id/en/node/117774 (dibaca 2026-09-29).
Pembulatan: PPh dibulatkan ke BAWAH ke rupiah; fee ke rupiah terdekat. BELUM dicocokkan dengan Coretax.

  python3 hitung_pajak_biaya.py --nilai-jual 15000000 --pajak domestik --fee-persen 0.2
  python3 hitung_pajak_biaya.py --transaksi bot/transaksi.csv [--kurs-idr 16500]   (rekap per bulan)
"""

import argparse
import csv
import json
import sys
from collections import OrderedDict
from decimal import Decimal, InvalidOperation, ROUND_DOWN, ROUND_HALF_UP

TARIF = {"domestik": Decimal("0.0021"), "luar_negeri": Decimal("0.01")}
CATATAN = ("Dasar: PMK 50/2025 (berlaku 1 Agustus 2025), dicek 2026-09-29 di pajak.go.id. Pembulatan belum "
           "dicocokkan dengan Coretax. Ini alat bantu hitung, bukan nasihat pajak -- konfirmasi ke konsultan pajak/DJP.")


def dec(s, nama):
    try:
        x = Decimal(str(s).strip())
    except InvalidOperation:
        raise ValueError(f"{nama} '{s}' bukan angka")
    if not x.is_finite() or x < 0:
        raise ValueError(f"{nama} harus angka >= 0")
    return x


def rp(x):
    return int(x.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def satu(nilai_jual, pajak, fee_persen):
    pph = (nilai_jual * TARIF[pajak]).quantize(Decimal("1"), rounding=ROUND_DOWN)
    fee = (nilai_jual * fee_persen / 100).quantize(Decimal("1"), rounding=ROUND_HALF_UP)
    return {"nilai_jual": rp(nilai_jual), "tarif_pph_persen": str(TARIF[pajak] * 100), "pph": int(pph),
            "fee": int(fee), "diterima_bersih": rp(nilai_jual - pph - fee), "catatan": CATATAN}


def rekap(path, kurs):
    per_bulan = OrderedDict()
    rusak = []
    with open(path, encoding="utf-8-sig") as f:
        for no, b in enumerate(csv.DictReader(f), start=2):
            try:
                bulan = b["waktu"][:7]
                k = kurs if b["pasangan"].upper().endswith("USDT") else Decimal("1")
                if k is None:
                    raise ValueError("pasangan non-IDR butuh --kurs-idr")
                r = per_bulan.setdefault(bulan, {"jumlah_jual": 0, "nilai_jual_idr": Decimal(0),
                                                 "pph_idr": Decimal(0), "fee_idr": Decimal(0), "nilai_beli_idr": Decimal(0)})
                r["fee_idr"] += dec(b["fee"], "fee") * k
                if b["sisi"] == "jual":
                    r["jumlah_jual"] += 1
                    r["nilai_jual_idr"] += dec(b["bruto"], "bruto") * k
                    r["pph_idr"] += dec(b["pajak_pph"] or "0", "pajak_pph") * k
                else:
                    r["nilai_beli_idr"] += dec(b["bruto"], "bruto") * k
            except (KeyError, ValueError) as e:
                rusak.append({"baris": no, "alasan": str(e)})
    hasil = {m: {k: (rp(v) if isinstance(v, Decimal) else v) for k, v in r.items()} for m, r in per_bulan.items()}
    return {"per_bulan": hasil, "baris_bermasalah": rusak, "catatan": CATATAN}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Hitung fee & PPh final kripto (PMK 50/2025)")
    ap.add_argument("--nilai-jual")
    ap.add_argument("--pajak", choices=tuple(TARIF), default="domestik")
    ap.add_argument("--fee-persen", default="0")
    ap.add_argument("--transaksi")
    ap.add_argument("--kurs-idr")
    a = ap.parse_args(argv)
    try:
        if a.transaksi:
            out = rekap(a.transaksi, dec(a.kurs_idr, "kurs") if a.kurs_idr else None)
        elif a.nilai_jual:
            out = satu(dec(a.nilai_jual, "nilai jual"), a.pajak, dec(a.fee_persen, "fee"))
        else:
            print("Isi --nilai-jual atau --transaksi.")
            return 1
    except (ValueError, FileNotFoundError) as e:
        print(json.dumps({"status": "error", "pesan": str(e)}, ensure_ascii=False))
        return 1
    print(json.dumps({"status": "ok", **out}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
