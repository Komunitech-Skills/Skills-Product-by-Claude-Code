#!/usr/bin/env python3
"""Perkiraan durasi ucapan naskah video pendek per adegan. Python standar saja.

Pakai:  python3 scripts/durasi_naskah.py naskah.txt --target 30
        (Windows: python atau py)   Bisa juga:  ... - < naskah.txt   atau   --teks "adegan 1 | kalimat"
Format naskah: satu adegan per baris, "Label | teks sulih suara" (label boleh dihilangkan).
Baris kosong dan baris berawalan # diabaikan. Penanda jeda: [jeda] = 0,5 dtk, [jeda 1.5] = 1,5 dtk.
Ini PERKIRAAN (kecepatan bicara tiap orang berbeda); ukur ulang dengan rekaman asli.
"""
import argparse
import json
import re
import sys

WPM_DEFAULT = 150      # kata per menit, bicara santai Bahasa Indonesia
JEDA_ADEGAN = 0.3      # detik jeda napas antar adegan
JEDA_DEFAULT = 0.5     # detik untuk [jeda] tanpa angka
POLA_JEDA = re.compile(r"\[\s*jeda(?:\s+(\d+(?:[.,]\d+)?))?\s*\]", re.IGNORECASE)
POLA_KATA = re.compile(r"[0-9A-Za-zÀ-ÿ]+(?:[-'’.,][0-9A-Za-zÀ-ÿ]+)*")


def hitung_kata(teks):
    return len(POLA_KATA.findall(teks))


def urai(baris_list):
    """Kembalikan daftar (label, teks). Baris kosong/komentar dilewati."""
    hasil = []
    for baris in baris_list:
        b = baris.strip()
        if not b or b.startswith("#"):
            continue
        label, teks = (b.split("|", 1) + [""])[:2] if "|" in b else (f"Adegan {len(hasil) + 1}", b)
        hasil.append((label.strip() or f"Adegan {len(hasil) + 1}", teks.strip()))
    return hasil


def estimasi(adegan, wpm=WPM_DEFAULT, jeda_adegan=JEDA_ADEGAN):
    if wpm <= 0:
        raise ValueError("wpm harus lebih dari 0")
    rincian, total = [], 0.0
    for i, (label, teks) in enumerate(adegan):
        jeda = 0.0
        for m in POLA_JEDA.finditer(teks):
            jeda += float(m.group(1).replace(",", ".")) if m.group(1) else JEDA_DEFAULT
        bersih = POLA_JEDA.sub(" ", teks)
        kata = hitung_kata(bersih)
        detik = kata / wpm * 60 + jeda + (jeda_adegan if i < len(adegan) - 1 else 0)
        rincian.append({"label": label, "kata": kata, "jeda_dtk": round(jeda, 1), "detik": round(detik, 1)})
        total += detik
    return rincian, round(total, 1)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Perkiraan durasi sulih suara per adegan")
    ap.add_argument("berkas", nargs="?", help="berkas naskah, atau '-' untuk stdin")
    ap.add_argument("--teks", help="naskah langsung; pisahkan adegan dengan ';;'")
    ap.add_argument("--target", type=float, default=30, help="durasi target (detik), default 30")
    ap.add_argument("--wpm", type=float, default=WPM_DEFAULT, help=f"kata per menit, default {WPM_DEFAULT}")
    ap.add_argument("--json", action="store_true", help="keluaran JSON")
    ap.add_argument("--strict", action="store_true", help="kode keluar 1 bila melebihi target")
    a = ap.parse_args(argv)

    if a.wpm <= 0 or a.target <= 0:
        print("Error: --wpm dan --target harus lebih dari 0.", file=sys.stderr)
        return 2
    try:
        if a.teks:
            baris = a.teks.split(";;")
        elif a.berkas == "-":
            baris = sys.stdin.read().splitlines()
        elif a.berkas:
            with open(a.berkas, encoding="utf-8") as f:
                baris = f.read().splitlines()
        else:
            ap.print_usage(sys.stderr)
            print("Error: beri berkas naskah, '-' atau --teks.", file=sys.stderr)
            return 2
    except (OSError, UnicodeDecodeError) as e:
        print(f"Error: tidak bisa membaca naskah ({e}).", file=sys.stderr)
        return 2

    adegan = urai(baris)
    if not adegan or all(not t for _, t in adegan):
        print("Error: naskah kosong. Tulis minimal satu adegan.", file=sys.stderr)
        return 2
    rincian, total = estimasi(adegan, a.wpm)
    lebih = round(total - a.target, 1)
    status = "MELEBIHI" if lebih > 0 else ("PAS" if lebih >= -5 else "KEPENDEKAN")
    if a.json:
        print(json.dumps({"wpm": a.wpm, "target": a.target, "total_dtk": total, "selisih_dtk": lebih,
                          "status": status, "adegan": rincian}, ensure_ascii=False, indent=2))
    else:
        print(f"{'Adegan':<24}{'Kata':>5}{'Jeda':>6}{'Detik':>7}")
        for r in rincian:
            print(f"{r['label'][:23]:<24}{r['kata']:>5}{r['jeda_dtk']:>6}{r['detik']:>7}")
        print(f"Total {total} dtk (target {a.target:g} dtk, {a.wpm:g} kata/menit) -> {status}")
        if lebih > 0:
            print(f"PERINGATAN: lebih {lebih} dtk (~{int(lebih / 60 * a.wpm) + 1} kata). Ringkas adegan terpanjang.")
        elif status == "KEPENDEKAN":
            print(f"Catatan: kurang {-lebih} dtk dari target; boleh tambah isi atau biarkan lebih singkat.")
        print("Ini perkiraan; ukur ulang dengan rekaman suara asli.")
    return 1 if (a.strict and lebih > 0) else 0


if __name__ == "__main__":
    sys.exit(main())
