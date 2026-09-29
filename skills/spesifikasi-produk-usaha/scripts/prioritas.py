#!/usr/bin/env python3
"""Skor prioritas RICE / ICE untuk ide produk atau fitur (Python standar, Decimal).

Pakai:
  python3 scripts/prioritas.py --metode rice --csv ide.csv [--kapasitas 20] [--json]
  python3 scripts/prioritas.py --metode ice  --csv ide.csv
(Windows: python atau py.)  CSV boleh dipisah , ; atau tab. Angka desimal boleh 0,5 atau 0.5.

RICE  kolom: nama, jangkauan, dampak, keyakinan, usaha
  jangkauan = perkiraan orang/pelanggan tersentuh per periode (>= 0)
  dampak    = 0,25 / 0,5 / 1 / 2 / 3 (minimal sampai masif); boleh angka > 0 lain
  keyakinan = 0-100 (persen; boleh ditulis 80%)  -> dipakai sebagai keyakinan/100
  usaha     = orang-hari kerja (> 0)
  skor = jangkauan x dampak x (keyakinan/100) / usaha
ICE   kolom: nama, dampak, keyakinan, kemudahan  (masing-masing 1-10)
  skor = dampak x keyakinan x kemudahan
Baris yang salah tidak dihitung diam-diam: dilaporkan jelas, baris lain tetap diproses.
Bagian roadmap: urutan skor teratas -> Sekarang, lalu Berikutnya, Nanti.
Tanpa --kapasitas (RICE): sepertiga teratas = Sekarang. Dengan --kapasitas (total orang-hari
tersedia): item berurutan masuk Sekarang selama muat; item berikutnya yang muat -> Berikutnya
setelah kapasitas yang sama terisi lagi; sisanya Nanti.
"""
import argparse
import csv
import io
import json
import re
import sys
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

DUA = Decimal("0.01")


class GalatBaris(ValueError):
    pass


def angka(teks, kolom):
    t = (teks or "").strip().replace("%", "").replace(" ", "")
    if t == "":
        raise GalatBaris(f"kolom '{kolom}' kosong")
    # 1.500 (titik ribuan) vs 0,5 (koma desimal) vs 0.5
    if "," in t and "." in t:
        t = t.replace(".", "").replace(",", ".")
    elif "," in t:
        t = t.replace(",", ".")
    elif t.count(".") > 1:
        t = t.replace(".", "")
    elif re.fullmatch(r"[1-9]\d{0,2}\.\d{3}", t):
        t = t.replace(".", "")  # 1.500 = seribu lima ratus (titik ribuan gaya Indonesia)
    try:
        v = Decimal(t)
    except InvalidOperation:
        raise GalatBaris(f"kolom '{kolom}' bukan angka: {teks!r}")
    if not v.is_finite():
        raise GalatBaris(f"kolom '{kolom}' bukan angka: {teks!r}")
    return v


def hitung_rice(baris):
    j = angka(baris.get("jangkauan"), "jangkauan")
    d = angka(baris.get("dampak"), "dampak")
    k = angka(baris.get("keyakinan"), "keyakinan")
    u = angka(baris.get("usaha"), "usaha")
    if j < 0:
        raise GalatBaris("jangkauan tidak boleh negatif")
    if d <= 0:
        raise GalatBaris("dampak harus > 0")
    if not (0 <= k <= 100):
        raise GalatBaris("keyakinan harus 0-100 (persen)")
    if u <= 0:
        raise GalatBaris("usaha harus > 0 orang-hari (tidak boleh dibagi nol)")
    return j * d * (k / Decimal(100)) / u, u


def hitung_ice(baris):
    v = []
    for kol in ("dampak", "keyakinan", "kemudahan"):
        x = angka(baris.get(kol), kol)
        if not (1 <= x <= 10):
            raise GalatBaris(f"{kol} harus 1-10")
        v.append(x)
    return v[0] * v[1] * v[2], None


def baca_csv(teks):
    teks = teks.lstrip("﻿")
    baris_awal = teks.splitlines()[0] if teks.strip() else ""
    delim = max([",", ";", "\t"], key=baris_awal.count)
    r = csv.DictReader(io.StringIO(teks), delimiter=delim)
    if not r.fieldnames:
        raise ValueError("file kosong")
    r.fieldnames = [f.strip().lower() for f in r.fieldnames]
    return list(r)


def proses(baris_list, metode):
    fn = hitung_rice if metode == "rice" else hitung_ice
    hasil, galat = [], []
    for no, b in enumerate(baris_list, start=2):
        b = {(k or "").strip().lower(): v for k, v in b.items() if k}
        nama = (b.get("nama") or "").strip()
        if not nama:
            if any((v or "").strip() for v in b.values() if isinstance(v, str)):
                galat.append((no, "(tanpa nama)", "kolom 'nama' kosong"))
            continue
        try:
            skor, usaha = fn(b)
        except GalatBaris as e:
            galat.append((no, nama, str(e)))
            continue
        hasil.append({"nama": nama, "skor": skor, "usaha": usaha})
    hasil.sort(key=lambda h: (-h["skor"], h["usaha"] if h["usaha"] is not None else Decimal(0), h["nama"].lower()))
    return hasil, galat


def beri_tahap(hasil, metode, kapasitas=None):
    n = len(hasil)
    if metode == "rice" and kapasitas is not None:
        terpakai, tahap = Decimal(0), "Sekarang"
        for h in hasil:
            if tahap == "Sekarang" and terpakai + h["usaha"] <= kapasitas:
                terpakai += h["usaha"]
                h["tahap"] = "Sekarang"
                continue
            if tahap == "Sekarang":
                tahap, terpakai = "Berikutnya", Decimal(0)
            if tahap == "Berikutnya" and terpakai + h["usaha"] <= kapasitas:
                terpakai += h["usaha"]
                h["tahap"] = "Berikutnya"
                continue
            tahap = "Nanti"
            h["tahap"] = "Nanti"
        return
    a = -(-n // 3)  # ceil(n/3)
    for i, h in enumerate(hasil):
        h["tahap"] = "Sekarang" if i < a else ("Berikutnya" if i < 2 * a else "Nanti")


def fmt(d):
    return f"{d.quantize(DUA, rounding=ROUND_HALF_UP):,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Skor prioritas RICE/ICE")
    ap.add_argument("--metode", choices=["rice", "ice"], required=True)
    ap.add_argument("--csv", required=True, help="file CSV ide")
    ap.add_argument("--kapasitas", help="total orang-hari tersedia (hanya RICE)")
    ap.add_argument("--json", action="store_true", help="keluaran JSON")
    a = ap.parse_args(argv)
    try:
        with open(a.csv, encoding="utf-8-sig") as f:
            baris = baca_csv(f.read())
    except (OSError, UnicodeDecodeError, ValueError, csv.Error) as e:
        print(f"GAGAL membaca file: {e}", file=sys.stderr)
        return 2
    kap = None
    if a.kapasitas is not None:
        try:
            kap = angka(a.kapasitas, "kapasitas")
            if kap <= 0:
                raise GalatBaris("kapasitas harus > 0")
        except GalatBaris as e:
            print(f"GAGAL: {e}", file=sys.stderr)
            return 2
    hasil, galat = proses(baris, a.metode)
    beri_tahap(hasil, a.metode, kap)
    if a.json:
        print(json.dumps({
            "metode": a.metode,
            "hasil": [{"urutan": i, "nama": h["nama"], "skor": str(h["skor"].quantize(DUA, rounding=ROUND_HALF_UP)),
                       "tahap": h["tahap"]} for i, h in enumerate(hasil, 1)],
            "galat": [{"baris": n, "nama": nm, "alasan": al} for n, nm, al in galat]},
            ensure_ascii=False, indent=2))
    else:
        print(f"Metode {a.metode.upper()} - {len(hasil)} ide dihitung, {len(galat)} bermasalah\n")
        if hasil:
            print("| # | Ide | Skor | Tahap |\n|---|---|---|---|")
            for i, h in enumerate(hasil, 1):
                print(f"| {i} | {h['nama']} | {fmt(h['skor'])} | {h['tahap']} |")
        for n, nm, al in galat:
            print(f"\nTIDAK DIHITUNG baris {n} ({nm}): {al}")
    if not hasil:
        return 1
    return 1 if galat else 0


if __name__ == "__main__":
    sys.exit(main())
