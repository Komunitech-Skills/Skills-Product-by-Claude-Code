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
POLA_JEDA = re.compile(r"\[\s*jeda(?:\s+([^\]]*?))?\s*\]", re.IGNORECASE)   # isi kurung diperiksa terpisah
POLA_ANGKA = re.compile(r"\d+(?:[.,]\d+)?")
WPM_WAJAR = (80, 220)      # di luar rentang ini: peringatan
WPM_BATAS = (40, 400)      # di luar rentang ini: ditolak (kode 2)
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


def estimasi(adegan, wpm=WPM_DEFAULT, jeda_adegan=JEDA_ADEGAN, peringatan=None):
    """Kembalikan (rincian, total). Bila `peringatan` (list) diberikan, catatan masalah input ditambahkan ke sana."""
    if wpm <= 0:
        raise ValueError("wpm harus lebih dari 0")
    if peringatan is None:
        peringatan = []
    rincian, total = [], 0.0
    for i, (label, teks) in enumerate(adegan):
        jeda = 0.0
        for m in POLA_JEDA.finditer(teks):
            isi = (m.group(1) or "").strip()
            if not isi:
                jeda += JEDA_DEFAULT
            elif POLA_ANGKA.fullmatch(isi):
                jeda += float(isi.replace(",", "."))
            else:                                   # "[jeda abc]": bukan angka -> pakai jeda bawaan + beri tahu
                jeda += JEDA_DEFAULT
                peringatan.append(f"Adegan '{label}': penanda '{m.group(0)}' bukan angka; dipakai jeda bawaan "
                                  f"{JEDA_DEFAULT:g} dtk. Tulis [jeda 1.5] untuk 1,5 dtk.")
        bersih = POLA_JEDA.sub(" ", teks)
        kata = hitung_kata(bersih)
        if kata == 0 and jeda == 0:
            peringatan.append(f"Adegan '{label}' tidak punya kata yang bisa dihitung (kosong atau hanya emoji/"
                              "simbol) dan dihitung 0 dtk. Bila ada suara di adegan ini, tulis teksnya.")
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
    if not (WPM_BATAS[0] <= a.wpm <= WPM_BATAS[1]):
        print(f"Error: --wpm {a.wpm:g} tidak masuk akal (batas {WPM_BATAS[0]}-{WPM_BATAS[1]} kata/menit; "
              f"wajar {WPM_WAJAR[0]}-{WPM_WAJAR[1]}, bicara santai sekitar {WPM_DEFAULT}).", file=sys.stderr)
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
    peringatan = []
    if not (WPM_WAJAR[0] <= a.wpm <= WPM_WAJAR[1]):
        peringatan.append(f"--wpm {a.wpm:g} di luar kisaran wajar {WPM_WAJAR[0]}-{WPM_WAJAR[1]} kata/menit; "
                          "hasil kurang bisa diandalkan.")
    rincian, total = estimasi(adegan, a.wpm, peringatan=peringatan)
    lebih = round(total - a.target, 1)
    status = "MELEBIHI" if lebih > 0 else ("PAS" if lebih >= -0.1 * a.target else "KEPENDEKAN")  # PAS = di bawah target tidak lebih dari 10%
    if a.json:
        print(json.dumps({"wpm": a.wpm, "target": a.target, "total_dtk": total, "selisih_dtk": lebih,
                          "status": status, "peringatan": peringatan, "adegan": rincian}, ensure_ascii=False, indent=2))
    else:
        # lebar kolom mengikuti isi (angka besar tidak melebur) dan selalu dipisah dua spasi
        wk = max([4] + [len(str(r["kata"])) for r in rincian])
        wj = max([4] + [len(str(r["jeda_dtk"])) for r in rincian])
        wd = max([5] + [len(str(r["detik"])) for r in rincian])
        print(f"{'Adegan':<24}  {'Kata':>{wk}}  {'Jeda':>{wj}}  {'Detik':>{wd}}")
        for r in rincian:
            print(f"{r['label'][:23]:<24}  {r['kata']:>{wk}}  {r['jeda_dtk']:>{wj}}  {r['detik']:>{wd}}")
        print(f"Total {total} dtk (target {a.target:g} dtk, {a.wpm:g} kata/menit) -> {status}")
        if lebih > 0:
            print(f"PERINGATAN: lebih {lebih} dtk (~{int(lebih / 60 * a.wpm) + 1} kata). Ringkas adegan terpanjang.")
        elif status == "KEPENDEKAN":
            print(f"Catatan: suara hanya {total} dtk dari target {a.target:g} dtk (kurang {-lebih} dtk). Ini wajar "
                  "bila ada bagian visual tanpa suara. Bila suara harus mengisi target (selisih lebih dari 10%), "
                  "tambah adegan/kalimat dari fakta pengguna atau ubah target, lalu hitung ulang.")
        for w in peringatan:
            print(f"PERINGATAN: {w}")
        print("Ini perkiraan; ukur ulang dengan rekaman suara asli.")
    return 1 if (a.strict and lebih > 0) else 0


if __name__ == "__main__":
    sys.exit(main())
