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
              nilai 0 < k <= 1 tanpa tanda % (mis. 0,8) ditolak: "0,8 maksudnya 80%?"
  usaha     = orang-hari kerja (> 0)
  skor = jangkauan x dampak x (keyakinan/100) / usaha
ICE   kolom: nama, dampak, keyakinan, kemudahan  (masing-masing 1-10)
  skor = dampak x keyakinan x kemudahan
Judul kolom Inggris juga diterima (name, reach, impact, confidence, effort, ease).
Angka "10,000" (satu koma + 3 angka) ambigu (sepuluh ribu gaya Inggris atau 10 gaya Indonesia)
-> baris ditolak dengan pesan; tulis 10000 atau 10.000 atau 10.
Baris yang salah tidak dihitung diam-diam: dilaporkan jelas, baris lain tetap diproses.
Bagian roadmap: urutan skor teratas -> Sekarang, lalu Berikutnya, Nanti.
Tanpa --kapasitas: dibagi tiga (n >= 3 -> tiap tahap minimal 1 ide; mis. 4 ide = 2/1/1,
5 = 2/2/1, 6 = 2/2/2); ide dengan skor sama persis ikut tahap ide di atasnya.
Dengan --kapasitas (RICE, total orang-hari per tahap): ide diisi ke Sekarang menurut urutan skor
selama muat (ide yang tidak muat dilewati, bukan mengunci tahap), lalu sisanya ke Berikutnya
dengan cara yang sama; sisanya Nanti. Ide yang usahanya > kapasitas -> Nanti + catatan.
--kapasitas pada ICE diabaikan dan diberi PERINGATAN (ICE tidak punya kolom usaha).
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


ALIAS_KOLOM = {"name": "nama", "reach": "jangkauan", "impact": "dampak", "confidence": "keyakinan",
               "effort": "usaha", "ease": "kemudahan"}
KOLOM_WAJIB = {"rice": ["nama", "jangkauan", "dampak", "keyakinan", "usaha"],
               "ice": ["nama", "dampak", "keyakinan", "kemudahan"]}


def angka(teks, kolom):
    t = (teks or "").strip().replace("%", "").replace(" ", "")
    if t == "":
        raise GalatBaris(f"kolom '{kolom}' kosong")
    # 1.500 (titik ribuan) vs 0,5 (koma desimal) vs 0.5
    if "," in t and "." in t:
        t = t.replace(".", "").replace(",", ".")
    elif re.fullmatch(r"-?[1-9]\d{0,2}(,\d{3}){2,}", t):
        t = t.replace(",", "")  # 10,000,000 = pasti koma ribuan gaya Inggris
    elif re.fullmatch(r"-?[1-9]\d{0,2},\d{3}", t):
        bulat = t.replace(",", "")
        raise GalatBaris(f"kolom '{kolom}' ambigu: {teks.strip()!r} maksudnya {bulat} atau "
                         f"{t.replace(',', '.').rstrip('0').rstrip('.').replace('.', ',')}? Tulis {bulat} (atau {bulat[:-3]}.{bulat[-3:]}) "
                         f"bila maksudnya ribuan, atau {t.replace(',', '.').rstrip('0').rstrip('.').replace('.', ',')} "
                         f"bila maksudnya desimal")
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
    if 0 < k <= 1 and "%" not in (baris.get("keyakinan") or ""):
        persen = (k * 100).normalize()
        raise GalatBaris(f"keyakinan ditulis persen 0-100; {baris.get('keyakinan').strip()} maksudnya "
                         f"{persen:f}%? Tulis {persen:f} (atau tulis {baris.get('keyakinan').strip()}% bila memang "
                         f"kurang dari 1 persen)")
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
    r.fieldnames = [normal_kolom(f) for f in r.fieldnames]
    return list(r)


def normal_kolom(f):
    f = (f or "").strip().lower()
    return ALIAS_KOLOM.get(f, f)


def kolom_hilang(teks, metode):
    """Kolom wajib yang tidak ada di baris judul (setelah alias Inggris)."""
    teks = teks.lstrip("\ufeff")
    baris_awal = teks.splitlines()[0] if teks.strip() else ""
    delim = max([",", ";", "\t"], key=baris_awal.count)
    ada = [normal_kolom(k) for k in next(csv.reader([baris_awal], delimiter=delim), [])]
    return [k for k in KOLOM_WAJIB[metode] if k not in ada], [k for k in ada if k]


def proses(baris_list, metode):
    fn = hitung_rice if metode == "rice" else hitung_ice
    hasil, galat = [], []
    for no, b in enumerate(baris_list, start=2):
        lebih = b.get(None)
        b = {normal_kolom(k): v for k, v in b.items() if k}
        nama = (b.get("nama") or "").strip()
        if lebih:
            galat.append((no, nama or "(tanpa nama)",
                          "jumlah nilai lebih banyak dari judul kolom; kemungkinan ada koma di nama "
                          "atau angka desimal (mis. 0,9) - beri tanda kutip atau pakai titik/titik koma"))
            continue
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
    """Isi h["tahap"] (dan h["catatan"] bila perlu). Urutan `hasil` tidak diubah."""
    for h in hasil:
        h["catatan"] = ""
    if metode == "rice" and kapasitas is not None:
        sisa = list(hasil)
        for tahap in ("Sekarang", "Berikutnya"):
            terpakai, belum = Decimal(0), []
            for h in sisa:
                if terpakai + h["usaha"] <= kapasitas:
                    terpakai += h["usaha"]
                    h["tahap"] = tahap
                else:
                    belum.append(h)  # tidak muat: lewati, lanjut ke ide berikutnya
            sisa = belum
        for h in sisa:
            h["tahap"] = "Nanti"
            if h["usaha"] > kapasitas:
                h["catatan"] = "usaha lebih besar dari kapasitas per tahap; pecah jadi langkah kecil"
            else:
                h["catatan"] = "tidak muat di kapasitas Sekarang/Berikutnya"
        return
    n = len(hasil)
    a = -(-n // 3)             # Sekarang = ceil(n/3)
    b = -(-(n - a) // 2)       # Berikutnya = separuh sisa (dibulatkan ke atas)
    for i, h in enumerate(hasil):
        h["tahap"] = "Sekarang" if i < a else ("Berikutnya" if i < a + b else "Nanti")
        if i > 0 and h["skor"] == hasil[i - 1]["skor"] and h["tahap"] != hasil[i - 1]["tahap"]:
            h["tahap"] = hasil[i - 1]["tahap"]
            h["catatan"] = "skor sama dengan ide di atasnya, ikut tahapnya"


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
            teks = f.read()
        baris = baca_csv(teks)
    except (OSError, UnicodeDecodeError, ValueError, csv.Error) as e:
        print(f"GAGAL membaca file: {e}", file=sys.stderr)
        return 2
    hilang, ada = kolom_hilang(teks, a.metode)
    if hilang:
        print(f"GAGAL: kolom wajib tidak ditemukan: {', '.join(hilang)}. Baris pertama (judul) untuk "
              f"{a.metode.upper()} harus: {','.join(KOLOM_WAJIB[a.metode])}. "
              f"Judul yang terbaca: {', '.join(ada) or '(kosong)'}", file=sys.stderr)
        return 2
    peringatan = []
    kap = None
    if a.kapasitas is not None:
        try:
            kap = angka(a.kapasitas, "kapasitas")
            if kap <= 0:
                raise GalatBaris("kapasitas harus > 0")
        except GalatBaris as e:
            print(f"GAGAL: {e}", file=sys.stderr)
            return 2
    if kap is not None and a.metode == "ice":
        peringatan.append("--kapasitas hanya berlaku untuk RICE (ICE tidak punya kolom usaha); "
                          "diabaikan, tahap memakai pembagian tiga")
        kap = None
    hasil, galat = proses(baris, a.metode)
    beri_tahap(hasil, a.metode, kap)
    for w in peringatan:
        print(f"PERINGATAN: {w}", file=sys.stderr)
    if a.json:
        print(json.dumps({
            "metode": a.metode,
            "hasil": [{"urutan": i, "nama": h["nama"], "skor": str(h["skor"].quantize(DUA, rounding=ROUND_HALF_UP)),
                       "tahap": h["tahap"], "catatan": h["catatan"]} for i, h in enumerate(hasil, 1)],
            "peringatan": peringatan,
            "galat": [{"baris": n, "nama": nm, "alasan": al} for n, nm, al in galat]},
            ensure_ascii=False, indent=2))
    else:
        print(f"Metode {a.metode.upper()} - {len(hasil)} ide dihitung, {len(galat)} bermasalah\n")
        for w in peringatan:
            print(f"PERINGATAN: {w}\n")
        if hasil:
            print("| # | Ide | Skor | Tahap |\n|---|---|---|---|")
            for i, h in enumerate(hasil, 1):
                print(f"| {i} | {h['nama']} | {fmt(h['skor'])} | {h['tahap']} |")
            for i, h in enumerate(hasil, 1):
                if h["catatan"]:
                    print(f"\nCatatan #{i} ({h['nama']}): {h['catatan']}")
        for n, nm, al in galat:
            print(f"\nTIDAK DIHITUNG baris {n} ({nm}): {al}")
    if not hasil:
        return 1
    return 1 if galat else 0


if __name__ == "__main__":
    sys.exit(main())
