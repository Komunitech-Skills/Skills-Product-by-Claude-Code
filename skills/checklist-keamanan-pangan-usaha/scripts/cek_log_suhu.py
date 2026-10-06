#!/usr/bin/env python3
"""Cek log suhu dapur. Pakai: python3 scripts/cek_log_suhu.py log.csv [--json]
(Windows: python atau py). CSV: waktu,alat,suhu. Pustaka standar saja."""
import argparse
import csv
import json
import re
import sys
from datetime import datetime, date, time

SUMBER_BATAS = "acuan ilmiah umum; PERLU REVIEW terhadap acuan Kemenkes/BPOM"
MAKS_ZONA_MENIT = 120
TINDAKAN = {
    "freezer": "cek pintu dan colokan, jangan sering dibuka; bahan yang sudah lunak jangan dibekukan ulang, masak segera atau buang.",
    "masak": "lanjutkan masak/panaskan, ukur ulang di bagian paling tebal sampai mencapai batas.",
}


def jenis_alat(nama):
    n = nama.lower()
    if re.search(r"freezer|beku|frozen", n):
        return "freezer", "maks", -18.0
    if re.search(r"panas ulang|reheat|pemanasan ulang", n):
        return "pemanasan ulang", "min", 74.0
    if re.search(r"penahan|warmer|bain|hot ?hold|pemanas", n):
        return "penahan panas", "min", 60.0
    if re.search(r"masak|matang|ayam|unggas|goreng|bakar", n):
        if re.search(r"giling", n):
            return "masak (giling)", "min", 71.0
        if re.search(r"ikan|telur|utuh|steak", n):
            return "masak (ikan/telur/utuh)", "min", 63.0
        return "masak", "min", 74.0
    if re.search(r"kulkas|chiller|showcase|lemari es|cooler|kulkas|dingin|fridge", n):
        return "kulkas", "maks", 5.0
    return None, None, None


def baca_waktu(teks, dasar):
    t = teks.strip().replace("T", " ")
    for f in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S", "%d/%m/%Y %H:%M", "%d-%m-%Y %H:%M"):
        try:
            return datetime.strptime(t, f)
        except ValueError:
            pass
    for f in ("%H:%M", "%H.%M"):
        try:
            return datetime.combine(dasar, datetime.strptime(t, f).time())
        except ValueError:
            pass
    return None


def baca_suhu(teks):
    t = teks.strip().replace("°", "").replace("º", "")
    t = re.sub(r"\s*[cC]$", "", t).replace(",", ".").strip()
    try:
        v = float(t)
    except ValueError:
        return None
    if v != v or v in (float("inf"), float("-inf")) or v < -80 or v > 400:
        return None
    return v


def analisis(path, dasar=None):
    dasar = dasar or date.today()
    hasil = {"baris_ok": 0, "baris_rusak": [], "alat": {}, "pelanggaran": [], "alat_tak_dikenal": []}
    try:
        with open(path, newline="", encoding="utf-8-sig") as f:
            isi = f.read()
    except (OSError, UnicodeDecodeError) as e:
        raise SystemExit("Tidak bisa membaca berkas: %s" % e)
    baris = list(csv.reader(isi.splitlines()))
    data = []
    for i, r in enumerate(baris, 1):
        if not r or all(not c.strip() for c in r):
            continue
        if i == 1 and r[0].strip().lower() in ("waktu", "tanggal", "jam", "time"):
            continue
        if len(r) < 3:
            hasil["baris_rusak"].append({"baris": i, "alasan": "kolom kurang dari 3"})
            continue
        w, alat, s = baca_waktu(r[0], dasar), r[1].strip(), baca_suhu(r[2])
        if w is None or not alat or s is None:
            alasan = "waktu tak terbaca" if w is None else ("nama alat kosong" if not alat else "suhu bukan angka wajar")
            hasil["baris_rusak"].append({"baris": i, "alasan": alasan})
            continue
        data.append((w, alat, s, i))
    hasil["baris_ok"] = len(data)
    per_alat = {}
    for d in data:
        per_alat.setdefault(d[1], []).append(d)
    for alat, rows in per_alat.items():
        rows.sort(key=lambda x: x[0])
        jenis, arah, batas = jenis_alat(alat)
        suhu = [x[2] for x in rows]
        ringkas = {"jenis": jenis, "batas": batas, "arah": arah, "jumlah": len(rows),
                   "min": min(suhu), "maks": max(suhu), "pembacaan_melanggar": 0, "menit_zona_bahaya": 0}
        if jenis is None:
            hasil["alat_tak_dikenal"].append(alat)
            hasil["alat"][alat] = ringkas
            continue
        def langgar(s):
            return s > batas if arah == "maks" else s < batas
        awal = None
        for idx, (w, _, s, baris_no) in enumerate(rows):
            if langgar(s):
                ringkas["pembacaan_melanggar"] += 1
                if jenis in ("kulkas", "penahan panas"):
                    if awal is None:
                        awal = w
                else:
                    hasil["pelanggaran"].append({"alat": alat, "waktu": w.strftime("%Y-%m-%d %H:%M"), "suhu": s,
                        "batas": batas, "arah": arah, "menit": None, "baris": baris_no})
            else:
                if awal is not None:
                    _tutup(hasil, ringkas, alat, awal, w, rows, batas, arah, True)
                    awal = None
        if awal is not None:
            _tutup(hasil, ringkas, alat, awal, rows[-1][0], rows, batas, arah, False)
        hasil["alat"][alat] = ringkas
    hasil["pelanggaran"].sort(key=lambda p: (p["waktu"], p["alat"]))
    return hasil


def _tutup(hasil, ringkas, alat, awal, akhir, rows, batas, arah, pulih):
    menit = int((akhir - awal).total_seconds() // 60)
    ringkas["menit_zona_bahaya"] += menit
    s_zona = [x[2] for x in rows if awal <= x[0] <= akhir and ((x[2] > batas) if arah == "maks" else (x[2] < batas))]
    ekstrem = max(s_zona) if arah == "maks" else min(s_zona)
    hasil["pelanggaran"].append({"alat": alat, "waktu": awal.strftime("%Y-%m-%d %H:%M"), "suhu": ekstrem,
        "batas": batas, "arah": arah, "menit": menit, "pulih": pulih,
        "lewat_2_jam": menit > MAKS_ZONA_MENIT})


def teks(h):
    o = ["REKAP LOG SUHU (batas: %s)" % SUMBER_BATAS,
         "Baris terbaca: %d; baris bermasalah: %d" % (h["baris_ok"], len(h["baris_rusak"])), ""]
    for a, r in sorted(h["alat"].items()):
        if r["jenis"] is None:
            o.append("- %s: jenis alat tidak dikenal, tidak dinilai (%d pembacaan, %.1f sampai %.1f C)" % (a, r["jumlah"], r["min"], r["maks"]))
        else:
            tanda = ">" if r["arah"] == "maks" else "<"
            o.append("- %s [%s, batas %s%.0f C]: %d pembacaan, %.1f sampai %.1f C, melanggar %d, zona bahaya %d menit" % (
                a, r["jenis"], "<= " if r["arah"] == "maks" else ">= ", r["batas"], r["jumlah"], r["min"], r["maks"],
                r["pembacaan_melanggar"], r["menit_zona_bahaya"]))
    o.append("")
    if h["pelanggaran"]:
        o.append("PELANGGARAN:")
        for p in h["pelanggaran"]:
            if p["menit"] is None:
                o.append("- %s %s: %.1f C (batas %s%.0f C). Tindakan: %s" % (
                    p["waktu"], p["alat"], p["suhu"], "<= " if p["arah"] == "maks" else ">= ", p["batas"],
                    TINDAKAN["freezer" if p["arah"] == "maks" else "masak"]))
            else:
                ket = "sekitar %d menit di luar batas (dari pembacaan pertama sampai pembacaan yang kembali normal)" % p["menit"]
                if not p.get("pulih", True):
                    ket += " (belum terlihat pulih sampai pembacaan terakhir; durasi minimal)"
                if p["lewat_2_jam"]:
                    ket += " - LEBIH DARI 2 JAM: bahan berisiko tinggi sebaiknya dibuang"
                o.append("- %s %s: terburuk %.1f C (batas %s%.0f C), %s" % (
                    p["waktu"], p["alat"], p["suhu"], "<= " if p["arah"] == "maks" else ">= ", p["batas"], ket))
    else:
        o.append("Tidak ada pelanggaran batas pada data yang terbaca.")
    if h["baris_rusak"]:
        o.append("")
        o.append("BARIS BERMASALAH (dilewati):")
        for b in h["baris_rusak"]:
            o.append("- baris %d: %s" % (b["baris"], b["alasan"]))
    return "\n".join(o)


def main(argv=None):
    p = argparse.ArgumentParser(description="Cek log suhu dapur dari CSV waktu,alat,suhu")
    p.add_argument("csv")
    p.add_argument("--json", action="store_true")
    p.add_argument("--tanggal", help="YYYY-MM-DD untuk waktu tanpa tanggal (default hari ini)")
    a = p.parse_args(argv)
    dasar = None
    if a.tanggal:
        try:
            dasar = datetime.strptime(a.tanggal, "%Y-%m-%d").date()
        except ValueError:
            raise SystemExit("--tanggal harus YYYY-MM-DD")
    h = analisis(a.csv, dasar)
    print(json.dumps(h, ensure_ascii=False, indent=2) if a.json else teks(h))
    return 0


if __name__ == "__main__":
    sys.exit(main())
