#!/usr/bin/env python3
"""Rekap penjualan dari file CSV. Output: JSON ke stdout.

Hanya memakai library standar Python.
"""
import argparse
import csv
import json
import re
import sys
from collections import defaultdict
from datetime import datetime

FORMAT_TANGGAL = [
    "%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M",
    "%d/%m/%Y", "%d/%m/%Y %H:%M:%S", "%d/%m/%Y %H:%M",
    "%d-%m-%Y", "%d-%m-%Y %H:%M:%S", "%d-%m-%Y %H:%M",
    "%d/%m/%y", "%Y/%m/%d",
]


def parse_tanggal(teks):
    teks = teks.strip()
    for fmt in FORMAT_TANGGAL:
        try:
            return datetime.strptime(teks, fmt).date()
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(teks).date()
    except ValueError:
        return None


def parse_angka(teks):
    """Mendukung '15000', 'Rp 15.000', '15.000,50', '15,000.50', '1.5'."""
    if teks is None:
        return None
    s = re.sub(r"[^\d,.\-]", "", str(teks))
    if not s or s in "-.,":
        return None
    if "," in s and "." in s:
        # Pemisah desimal adalah yang muncul terakhir
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    elif "," in s:
        # '15,50' -> desimal; '15,000' -> ribuan
        bagian = s.split(",")
        if len(bagian) == 2 and len(bagian[1]) != 3:
            s = s.replace(",", ".")
        else:
            s = s.replace(",", "")
    elif s.count(".") > 1 or (s.count(".") == 1 and len(s.split(".")[1]) == 3):
        # '15.000' atau '1.250.000' -> ribuan
        s = s.replace(".", "")
    try:
        return float(s)
    except ValueError:
        return None


def baca_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        contoh = f.read(4096)
        f.seek(0)
        try:
            dialek = csv.Sniffer().sniff(contoh, delimiters=",;\t|")
        except csv.Error:
            dialek = csv.excel
        return list(csv.DictReader(f, dialect=dialek))


def main():
    p = argparse.ArgumentParser(description="Rekap penjualan dari CSV")
    p.add_argument("file")
    p.add_argument("--kolom-tanggal", required=True)
    p.add_argument("--kolom-produk", required=True)
    p.add_argument("--kolom-qty")
    grup = p.add_mutually_exclusive_group(required=True)
    grup.add_argument("--kolom-total", help="Total harga per baris")
    grup.add_argument("--kolom-harga", help="Harga satuan (dikali qty)")
    p.add_argument("--top", type=int, default=5)
    a = p.parse_args()

    try:
        baris = baca_csv(a.file)
    except (OSError, UnicodeDecodeError) as e:
        print(json.dumps({"error": f"Gagal membaca file: {e}"}), file=sys.stderr)
        sys.exit(1)

    if not baris:
        print(json.dumps({"error": "File kosong"}), file=sys.stderr)
        sys.exit(1)

    kolom = list(baris[0].keys())
    wajib = [a.kolom_tanggal, a.kolom_produk, a.kolom_total or a.kolom_harga]
    if a.kolom_qty:
        wajib.append(a.kolom_qty)
    hilang = [k for k in wajib if k not in kolom]
    if hilang:
        print(json.dumps({"error": "Kolom tidak ditemukan", "hilang": hilang,
                          "kolom_tersedia": kolom}, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    per_produk = defaultdict(lambda: {"qty": 0.0, "omzet": 0.0})
    per_hari = defaultdict(float)
    dilewati = defaultdict(int)
    total, n = 0.0, 0

    for r in baris:
        tgl = parse_tanggal(r.get(a.kolom_tanggal) or "")
        if tgl is None:
            dilewati["tanggal tidak valid"] += 1
            continue
        qty = parse_angka(r.get(a.kolom_qty)) if a.kolom_qty else 1.0
        if qty is None:
            dilewati["qty tidak valid"] += 1
            continue
        if a.kolom_total:
            nilai = parse_angka(r.get(a.kolom_total))
        else:
            harga = parse_angka(r.get(a.kolom_harga))
            nilai = harga * qty if harga is not None else None
        if nilai is None:
            dilewati["harga/total tidak valid"] += 1
            continue
        produk = (r.get(a.kolom_produk) or "").strip() or "(tanpa nama)"
        per_produk[produk]["qty"] += qty
        per_produk[produk]["omzet"] += nilai
        per_hari[tgl.isoformat()] += nilai
        total += nilai
        n += 1

    if n == 0:
        print(json.dumps({"error": "Tidak ada baris valid", "alasan": dict(dilewati)},
                         ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    urut = sorted(per_produk.items(), key=lambda x: x[1]["omzet"], reverse=True)
    hari = sorted(per_hari.items())
    terbaik = max(hari, key=lambda x: x[1])
    terendah = min(hari, key=lambda x: x[1])

    hasil = {
        "periode": {"awal": hari[0][0], "akhir": hari[-1][0], "jumlah_hari_ada_penjualan": len(hari)},
        "total_omzet": round(total, 2),
        "jumlah_baris_valid": n,
        "rata_rata_omzet_per_hari": round(total / len(hari), 2),
        "produk_terlaris": [
            {"produk": k, "qty": round(v["qty"], 2), "omzet": round(v["omzet"], 2),
             "persen_omzet": round(v["omzet"] / total * 100, 1) if total else 0}
            for k, v in urut[: a.top]
        ],
        "jumlah_produk_unik": len(per_produk),
        "hari_terbaik": {"tanggal": terbaik[0], "omzet": round(terbaik[1], 2)},
        "hari_terendah": {"tanggal": terendah[0], "omzet": round(terendah[1], 2)},
        "omzet_harian": {k: round(v, 2) for k, v in hari},
        "baris_dilewati": sum(dilewati.values()),
        "alasan_dilewati": dict(dilewati),
    }
    print(json.dumps(hasil, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
