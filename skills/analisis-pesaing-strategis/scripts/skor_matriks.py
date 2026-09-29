#!/usr/bin/env python3
"""Skor matriks pesaing berbobot + peta posisi teks. Python standar saja.

CSV: kriteria,bobot,<nama kita>,<pesaing 1>,<pesaing 2>,...
Nilai 1-5, makin tinggi = makin baik di mata pelanggan (harga murah = nilai tinggi). Boleh desimal. Sel kosong = belum diketahui (tidak ikut dihitung,
bobot dinormalkan ulang per toko dan cakupan data ditampilkan).
Pakai: python3 skor_matriks.py matriks.csv [--sumbu-x KRITERIA --sumbu-y KRITERIA]
       [--format json]   (Windows: python atau py)
"""
import argparse
import csv
import io
import json
import math
import sys


class MatriksError(Exception):
    pass


def angka(teks, nama, baris):
    t = (teks or "").strip().replace(",", ".")
    if t == "":
        return None
    try:
        v = float(t)
    except ValueError:
        raise MatriksError(f"Baris {baris}: nilai '{teks}' pada '{nama}' bukan angka.")
    if v != v or v in (float("inf"), float("-inf")):
        raise MatriksError(f"Baris {baris}: nilai '{teks}' pada '{nama}' bukan angka yang wajar.")
    return v


def baca(path):
    for enc in ("utf-8-sig", "cp1252"):
        try:
            with open(path, encoding=enc, newline="") as f:
                isi = f.read()
            break
        except UnicodeDecodeError:
            continue
        except OSError as e:
            raise MatriksError(f"File tidak bisa dibuka: {e}")
    else:
        raise MatriksError("Encoding file tidak dikenali; simpan sebagai CSV UTF-8.")
    return parse(isi)


def parse(isi):
    try:
        dialek = csv.Sniffer().sniff(isi.split("\n")[0], delimiters=",;\t")
        delim = dialek.delimiter
    except csv.Error:
        delim = ","
    rows = list(csv.reader(io.StringIO(isi), delimiter=delim))
    rows = [r for r in rows if any(c.strip() for c in r)]
    if len(rows) < 2:
        raise MatriksError("CSV kosong atau tanpa baris kriteria.")
    head = [h.strip() for h in rows[0]]
    if len(head) < 4 or head[0].lower() != "kriteria" or head[1].lower() != "bobot":
        raise MatriksError("Header harus: kriteria,bobot,<nama kita>,<pesaing 1>,... (min. 1 pesaing).")
    toko = head[2:]
    if len(set(t.lower() for t in toko)) != len(toko) or any(not t for t in toko):
        raise MatriksError("Nama toko di header harus unik dan tidak kosong.")
    krit = []
    for i, r in enumerate(rows[1:], start=2):
        r = r + [""] * (len(head) - len(r))
        nama = r[0].strip()
        if not nama:
            raise MatriksError(f"Baris {i}: nama kriteria kosong.")
        b = angka(r[1], "bobot", i)
        if b is None or b <= 0:
            raise MatriksError(f"Baris {i}: bobot '{nama}' harus angka > 0.")
        nilai = {}
        for t, c in zip(toko, r[2:len(head)]):
            v = angka(c, t, i)
            if v is not None and not 1 <= v <= 5:
                raise MatriksError(f"Baris {i}: nilai {t} pada '{nama}' = {v}, harus 1-5.")
            nilai[t] = v
        krit.append({"nama": nama, "bobot": b, "nilai": nilai})
    return toko, krit


def hitung(toko, krit):
    total_bobot = sum(k["bobot"] for k in krit)
    hasil = {}
    for t in toko:
        ada = [k for k in krit if k["nilai"][t] is not None]
        bobot_ada = sum(k["bobot"] for k in ada)
        skor = (sum(k["bobot"] * k["nilai"][t] for k in ada) / bobot_ada) if bobot_ada else None
        hasil[t] = {"skor": None if skor is None else round(skor, 2),
                    "cakupan_persen": round(100 * bobot_ada / total_bobot),
                    "kosong": [k["nama"] for k in krit if k["nilai"][t] is None]}
    kita = toko[0]
    unggul, tertinggal = [], []
    for k in krit:
        if k["nilai"][kita] is None:
            continue
        lain = [k["nilai"][t] for t in toko[1:] if k["nilai"][t] is not None]
        if not lain:
            continue
        rata = sum(lain) / len(lain)
        selisih = round(k["nilai"][kita] - rata, 2)
        (unggul if selisih > 0 else tertinggal if selisih < 0 else []).append(
            {"kriteria": k["nama"], "bobot": k["bobot"], "selisih_vs_rata_pesaing": selisih,
             "prioritas": round(abs(selisih) * k["bobot"] / total_bobot * 100, 1)})
    unggul.sort(key=lambda x: -x["prioritas"])
    tertinggal.sort(key=lambda x: -x["prioritas"])
    return hasil, unggul, tertinggal


def peta(toko, krit, sx, sy):
    def cari(n):
        for k in krit:
            if k["nama"].lower() == n.lower():
                return k
        raise MatriksError(f"Kriteria sumbu '{n}' tidak ada di CSV.")
    kx, ky = cari(sx), cari(sy)
    grid = {}
    for i, t in enumerate(toko):
        x, y = kx["nilai"][t], ky["nilai"][t]
        if x is None or y is None:
            continue
        grid.setdefault((int(math.floor(x + 0.5)), int(math.floor(y + 0.5))), []).append(f"{i}")
    out = [f"Peta posisi (atas = {ky['nama']} tinggi, kanan = {kx['nama']} tinggi)"]
    for y in range(5, 0, -1):
        sel = ["/".join(grid.get((x, y), [])) or "." for x in range(1, 6)]
        out.append(f"{y} | " + " ".join(f"{s:>6}" for s in sel))
    out.append("  +" + "-" * 38)
    out.append("    " + " ".join(f"{x:>6}" for x in range(1, 6)) + f"   -> {kx['nama']}")
    out.append("Kode: " + ", ".join(f"{i}={t}" for i, t in enumerate(toko)) + " (0 = kita)")
    out.append("Nilai dibulatkan ke 1-5 untuk peta; petak kosong = celah posisi yang belum diisi siapa pun.")
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--sumbu-x")
    ap.add_argument("--sumbu-y")
    ap.add_argument("--format", choices=["teks", "json"], default="teks")
    a = ap.parse_args(argv)
    try:
        toko, krit = baca(a.csv)
        hasil, unggul, tertinggal = hitung(toko, krit)
        pt = peta(toko, krit, a.sumbu_x, a.sumbu_y) if a.sumbu_x and a.sumbu_y else None
    except MatriksError as e:
        print(f"GAGAL: {e}", file=sys.stderr)
        return 2
    if a.format == "json":
        print(json.dumps({"skor": hasil, "unggul": unggul, "tertinggal": tertinggal, "peta": pt},
                         ensure_ascii=False, indent=2))
        return 0
    print("## Skor berbobot (skala 1-5)")
    print("| Peringkat | Toko | Skor | Data terisi | Belum diketahui |")
    print("|---|---|---|---|---|")
    urut = sorted(hasil.items(), key=lambda kv: -(kv[1]["skor"] or 0))
    for n, (t, h) in enumerate(urut, 1):
        skor = "-" if h["skor"] is None else f"{h['skor']:.2f}".replace(".", ",")
        print(f"| {n} | {t}{' (kita)' if t == toko[0] and t.lower() != 'kita' else ''} | {skor} | {h['cakupan_persen']}% | {', '.join(h['kosong']) or '-'} |")
    if any(h["cakupan_persen"] < 70 for h in hasil.values()):
        print("\nPERHATIAN: ada toko dengan data < 70% bobot; skor kurang dapat diandalkan, lengkapi dulu.")
    print("\n## Unggul dibanding rata-rata pesaing (urut prioritas = selisih x bobot)")
    for x in unggul or [{"kriteria": "(tidak ada)", "selisih_vs_rata_pesaing": 0, "prioritas": 0}]:
        print(f"- {x['kriteria']}: +{x['selisih_vs_rata_pesaing']:g}".replace(".", ","))
    print("\n## Tertinggal dibanding rata-rata pesaing")
    for x in tertinggal or [{"kriteria": "(tidak ada)", "selisih_vs_rata_pesaing": 0, "prioritas": 0}]:
        print(f"- {x['kriteria']}: {x['selisih_vs_rata_pesaing']:g}".replace(".", ","))
    if pt:
        print("\n" + pt)
    print("\nCatatan: skor hanya secerdas nilai yang kamu isi; nilai 1-5 adalah penilaian subjektif berdasarkan bukti yang dicatat.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
