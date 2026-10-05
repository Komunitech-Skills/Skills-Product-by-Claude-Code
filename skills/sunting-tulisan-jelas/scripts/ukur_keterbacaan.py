#!/usr/bin/env python3
"""ukur_keterbacaan.py - ukuran keterbacaan sederhana untuk tulisan kerja berbahasa Indonesia.

Hanya library standar Python 3.8+. Lintas OS (Windows: pakai `python` atau `py`).
Tidak membuka jaringan, tidak menulis file, tidak mengubah teks yang diberikan.

Yang diukur: jumlah kata & kalimat, rata-rata kata per kalimat, persen kalimat > 25 kata,
kalimat terpanjang, perkiraan kalimat pasif ("di-"), kata pengisi/bertele/jargon/kabur
(dari references/kata-pengisi-jargon.txt). Mode --sebelum/--sesudah juga membandingkan
angka & tanggal supaya terlihat bila ada fakta yang hilang atau bertambah.

Ukuran ini PENANDA kasar, bukan nilai mutu tulisan. Pembaca (agent) tetap menilai isi.

Contoh:
  python3 ukur_keterbacaan.py --file draf.txt
  python3 ukur_keterbacaan.py --teks "Kami informasikan bahwa toko tutup."
  python3 ukur_keterbacaan.py --sebelum asli.txt --sesudah suntingan.txt
  python3 ukur_keterbacaan.py --file draf.txt --json
"""
import argparse
import io
import json
import re
import sys
from collections import Counter
from pathlib import Path

VERSI = "1.0.0"
BATAS_KALIMAT_PANJANG = 25
MAKS_BYTE = 2_000_000
DAFTAR = Path(__file__).resolve().parent.parent / "references" / "kata-pengisi-jargon.txt"

# Singkatan yang diakhiri titik tetapi bukan akhir kalimat.
SINGKATAN = {
    "jl", "jln", "rp", "no", "nr", "bpk", "sdr", "sdri", "tn", "ny", "nn", "dr", "drs",
    "ir", "prof", "h", "hj", "pt", "cv", "ud", "tbk", "dll", "dsb", "dst", "dkk", "yth", "a.n", "u.p",
    "hlm", "tgl", "pkl", "wib", "wita", "wit", "mis", "dgn", "yg", "spt", "cth", "ttd", "kab",
    "kec", "kel", "ds", "rt", "rw", "st", "mr", "mrs", "ms", "vs", "etc", "e.g", "i.e", "approx", "est",
}
PENANDA_DAFTAR = re.compile(r"^\s*(?:[-*•●▪]|\(?\d{1,3}[.)])\s+")
# Kata berawalan "di" yang BUKAN kata kerja pasif.
BUKAN_PASIF = {
    "dia", "diam", "diri", "dini", "dinas", "dinding", "dingin", "dinamis", "dinamika", "diet", "digital",
    "dimensi", "dimana", "disini", "disana", "disitu", "dikit", "diskon", "diskusi", "disiplin", "distribusi",
    "distributor", "divisi", "direktur", "direksi", "direktorat", "dinar", "dirham", "diagram", "diagnosis",
    "diameter", "dikte", "dilema", "diploma", "diplomat", "disket", "display", "disk", "dibawah", "diatas",
    "didalam", "diluar", "diantara", "didepan", "dibelakang", "disamping", "dimulai",
}
ANGKA = re.compile(r"\d[\d.,:/]*\d|\d")
KATA = re.compile(r"[^\W_][\w'’\-./@:,]*", re.UNICODE)


def baca_teks(path):
    p = Path(path)
    if not p.is_file():
        raise SystemExit("Berkas tidak ditemukan: %s" % path)
    data = p.read_bytes()
    if len(data) > MAKS_BYTE:
        raise SystemExit("Berkas terlalu besar (>2 MB). Pecah per bagian.")
    if b"\x00" in data[:2048]:
        raise SystemExit("Berkas tampaknya bukan teks biasa (mis. Word/PDF). Tempel isinya sebagai teks.")
    return data.decode("utf-8-sig", errors="replace")


def bersihkan_baris(baris):
    return PENANDA_DAFTAR.sub("", baris).strip()


def pecah_kalimat(teks):
    """Pecah teks jadi kalimat. Baris kosong, butir daftar, dan akhir baris judul pendek ikut memisah."""
    kalimat = []
    for blok in re.split(r"\n\s*\n", teks.replace("\r\n", "\n").replace("\r", "\n")):
        for baris in blok.split("\n"):
            isi = bersihkan_baris(baris)
            if not isi:
                continue
            potongan = _pecah_tanda(isi)
            if not potongan:
                continue
            # baris tanpa tanda akhir (judul/butir/sapaan) dihitung satu satuan sendiri
            kalimat.extend(potongan)
    return [k for k in kalimat if KATA.search(k)]


def _pecah_tanda(isi):
    hasil, awal = [], 0
    for m in re.finditer(r"[.!?]+(?=\s|$)", isi):
        akhir = m.end()
        sebelum = isi[awal:m.start()]
        token = sebelum.split()[-1].lower().strip("()\"'") if sebelum.split() else ""
        if m.group().startswith(".") and len(m.group()) == 1 and (token in SINGKATAN or re.fullmatch(r"[a-z]", token)):
            continue
        sisa = isi[akhir:].lstrip()
        if sisa and m.group().startswith(".") and sisa[0].islower():
            continue  # titik lalu huruf kecil: kemungkinan singkatan, bukan akhir kalimat
        bagian = isi[awal:akhir].strip()
        if bagian:
            hasil.append(bagian)
        awal = akhir
    sisa = isi[awal:].strip()
    if sisa:
        hasil.append(sisa)
    return hasil


def hitung_kata(kalimat):
    return len(KATA.findall(kalimat))


def muat_daftar():
    daftar = []
    try:
        for baris in DAFTAR.read_text(encoding="utf-8").splitlines():
            baris = baris.strip()
            if not baris or baris.startswith("#"):
                continue
            bagian = baris.split("|")
            if len(bagian) >= 2:
                daftar.append((bagian[0], bagian[1].strip().lower(), bagian[2].strip() if len(bagian) > 2 else ""))
    except OSError:
        return None
    return daftar


def cari_penanda(teks, daftar):
    """Hitung frasa daftar. Frasa yang berada di dalam frasa lebih panjang yang cocok tidak dihitung dua kali."""
    rendah = teks.lower()
    terpakai = [False] * len(rendah)
    temuan = Counter()
    info = {}
    for jenis, frasa, saran in sorted(daftar, key=lambda d: -len(d[1])):
        pola = re.compile(r"(?<![\w])" + re.escape(frasa) + r"(?![\w])")
        for m in pola.finditer(rendah):
            if any(terpakai[m.start():m.end()]):
                continue
            for i in range(m.start(), m.end()):
                terpakai[i] = True
            temuan[(jenis, frasa)] += 1
            info[(jenis, frasa)] = saran
    return temuan, info


def perkiraan_pasif(kalimat_list):
    jumlah, contoh = 0, []
    for k in kalimat_list:
        for kata in re.findall(r"\b[Dd]i[a-z]{3,}\b", k):
            if kata.lower() in BUKAN_PASIF:
                continue
            jumlah += 1
            if len(contoh) < 5 and kata.lower() not in contoh:
                contoh.append(kata.lower())
    return jumlah, contoh


def angka_dalam(teks):
    hasil = Counter()
    teks = "\n".join(bersihkan_baris(b) for b in teks.splitlines())  # nomor urut daftar bukan angka isi
    for a in ANGKA.findall(teks):
        hasil[a.strip(".,:/")] += 1
    return hasil


def ukur(teks, daftar):
    kalimat = pecah_kalimat(teks)
    panjang = [hitung_kata(k) for k in kalimat]
    n_kata = sum(panjang)
    n_k = len(kalimat)
    panjang_besar = [(p, k) for p, k in zip(panjang, kalimat) if p > BATAS_KALIMAT_PANJANG]
    pasif, contoh_pasif = perkiraan_pasif(kalimat)
    temuan, info = cari_penanda(teks, daftar) if daftar else (Counter(), {})
    per_jenis = Counter()
    for (jenis, _), c in temuan.items():
        per_jenis[jenis] += c
    pecah_paragraf = [p for p in re.split(r"\n\s*\n", teks.strip()) if p.strip()]
    return {
        "kata": n_kata,
        "kalimat": n_k,
        "rata_kata_per_kalimat": round(n_kata / n_k, 1) if n_k else 0.0,
        "kalimat_lebih_25_kata": len(panjang_besar),
        "persen_kalimat_lebih_25_kata": round(100 * len(panjang_besar) / n_k, 1) if n_k else 0.0,
        "kalimat_terpanjang_kata": max(panjang) if panjang else 0,
        "perkiraan_kalimat_pasif": pasif,
        "contoh_pasif": contoh_pasif,
        "penanda_total": sum(temuan.values()),
        "penanda_per_jenis": {j: per_jenis.get(j, 0) for j in ("pengisi", "bertele", "jargon", "kabur")},
        "penanda_rincian": [
            {"jenis": j, "frasa": f, "jumlah": c, "saran": info[(j, f)]}
            for (j, f), c in sorted(temuan.items(), key=lambda x: (-x[1], x[0][1]))
        ],
        "paragraf": len(pecah_paragraf),
        "daftar_ditemukan": daftar is not None,
        "_kalimat_panjang": [(p, k) for p, k in sorted(panjang_besar, key=lambda x: -x[0])[:5]],
    }


def tampil(h, judul="Ukuran keterbacaan"):
    t = []
    t.append(judul)
    t.append("  Kata: %d | Kalimat: %d | Paragraf: %d" % (h["kata"], h["kalimat"], h["paragraf"]))
    t.append("  Rata-rata kata per kalimat: %s (sasaran: 18 atau kurang)" % h["rata_kata_per_kalimat"])
    t.append("  Kalimat > %d kata: %d (%s%%) | terpanjang: %d kata" % (
        BATAS_KALIMAT_PANJANG, h["kalimat_lebih_25_kata"], h["persen_kalimat_lebih_25_kata"], h["kalimat_terpanjang_kata"]))
    t.append("  Perkiraan kalimat pasif (di-): %d%s" % (
        h["perkiraan_kalimat_pasif"], " (" + ", ".join(h["contoh_pasif"]) + ")" if h["contoh_pasif"] else ""))
    if h["daftar_ditemukan"]:
        pj = h["penanda_per_jenis"]
        t.append("  Kata pengisi/bertele/jargon/kabur: %d (pengisi %d, bertele %d, jargon %d, kabur %d)" % (
            h["penanda_total"], pj["pengisi"], pj["bertele"], pj["jargon"], pj["kabur"]))
        for r in h["penanda_rincian"][:12]:
            t.append("    - [%s] \"%s\" x%d -> %s" % (r["jenis"], r["frasa"], r["jumlah"], r["saran"]))
    else:
        t.append("  (daftar kata pengisi tidak ditemukan; bagian ini dilewati)")
    for p, k in h["_kalimat_panjang"]:
        t.append("  Kalimat panjang (%d kata): %s" % (p, k if len(k) <= 140 else k[:137] + "..."))
    return "\n".join(t)


BARIS_BANDING = [
    ("kata", "Jumlah kata"),
    ("kalimat", "Jumlah kalimat"),
    ("rata_kata_per_kalimat", "Rata-rata kata per kalimat"),
    ("persen_kalimat_lebih_25_kata", "Kalimat > 25 kata (%)"),
    ("kalimat_terpanjang_kata", "Kalimat terpanjang (kata)"),
    ("perkiraan_kalimat_pasif", "Perkiraan kalimat pasif"),
    ("penanda_total", "Kata pengisi/jargon/kabur"),
]


def bandingkan(a, b, teks_a, teks_b):
    t = ["Perbandingan sebelum -> sesudah", "  %-30s %9s %9s" % ("Ukuran", "Sebelum", "Sesudah")]
    for kunci, nama in BARIS_BANDING:
        t.append("  %-30s %9s %9s" % (nama, a[kunci], b[kunci]))
    if a["kata"]:
        t.append("  Perubahan panjang: %+.0f%% kata" % (100 * (b["kata"] - a["kata"]) / a["kata"]))
    na, nb = set(angka_dalam(teks_a)), set(angka_dalam(teks_b))
    hilang, baru = sorted(na - nb), sorted(nb - na)
    t.append("  Angka/tanggal yang HILANG dari suntingan: %s" % (", ".join(hilang) if hilang else "tidak ada"))
    t.append("  Angka/tanggal BARU di suntingan: %s" % (", ".join(baru) if baru else "tidak ada"))
    return "\n".join(t)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Ukuran keterbacaan sederhana untuk tulisan kerja (Bahasa Indonesia).")
    ap.add_argument("--file", help="berkas teks (UTF-8)")
    ap.add_argument("--teks", help="teks langsung")
    ap.add_argument("--sebelum", help="berkas teks asli (mode banding)")
    ap.add_argument("--sesudah", help="berkas teks suntingan (mode banding)")
    ap.add_argument("--json", action="store_true", help="keluaran JSON")
    ap.add_argument("--versi", action="version", version=VERSI)
    a = ap.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    daftar = muat_daftar()

    if a.sebelum or a.sesudah:
        if not (a.sebelum and a.sesudah):
            raise SystemExit("Mode banding butuh --sebelum DAN --sesudah.")
        ta, tb = baca_teks(a.sebelum), baca_teks(a.sesudah)
        for nama, t in (("sebelum", ta), (" sesudah", tb)):
            if not t.strip():
                raise SystemExit("Teks %s kosong." % nama.strip())
        ha, hb = ukur(ta, daftar), ukur(tb, daftar)
        if a.json:
            for h in (ha, hb):
                h.pop("_kalimat_panjang", None)
            print(json.dumps({"sebelum": ha, "sesudah": hb}, ensure_ascii=False, indent=2))
        else:
            print(bandingkan(ha, hb, ta, tb))
        return 0

    if a.teks is not None:
        teks = a.teks
    elif a.file:
        teks = baca_teks(a.file)
    elif not sys.stdin.isatty():
        teks = sys.stdin.read()
    else:
        raise SystemExit("Beri --file, --teks, atau tempel lewat stdin.")
    if not teks.strip() or not KATA.search(teks):
        raise SystemExit("Teks kosong atau tidak berisi kata. Minta pengguna menempel tulisannya.")
    h = ukur(teks, daftar)
    if a.json:
        h.pop("_kalimat_panjang", None)
        print(json.dumps(h, ensure_ascii=False, indent=2))
    else:
        print(tampil(h))
        if h["kata"] < 15:
            print("  Catatan: teks sangat pendek; angka rata-rata kurang berarti.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
