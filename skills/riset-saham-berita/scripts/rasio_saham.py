#!/usr/bin/env python3
"""Hitung rasio dasar saham BEI dari angka yang ditempel pengguna, dan cek level harga pantauan.

TIDAK ada akses jaringan. Script ini hanya menghitung angka yang sudah diberikan; ia tidak
mengambil harga, tidak memberi rekomendasi beli/jual/tahan, dan tidak menghitung target harga.

Perintah:
  python3 rasio_saham.py rasio data.json [--format md|json] [--hari-ini YYYY-MM-DD]
  python3 rasio_saham.py level watchlist.csv [--format md|json] [--hari-ini YYYY-MM-DD]
  python3 rasio_saham.py angka "Rp1,2 T" [--satuan juta]      (cek cara sebuah angka dibaca)
Windows: ganti python3 dengan python atau py.

--- Perintah `rasio`: file JSON (semua angka boleh teks format Indonesia) ---
{
  "emiten": "ABCD", "nama": "PT Contoh Tbk", "sektor": "Konsumer",
  "periode": "FY2025", "periode_lalu": "FY2024", "periode_bulan": 12,
  "tanggal_laporan": "2025-12-31",          # tanggal akhir periode laporan
  "sumber_laporan": "idx.co.id, LK tahunan audit, diakses 2026-09-28",
  "satuan_laporan": "juta",                 # angka laporan TANPA akhiran dikali satuan ini
  "pendapatan": "1.234.567", "pendapatan_lalu": "Rp1,1 T",
  "laba_bersih": "98.765", "laba_bersih_lalu": "(12.000)",
  "laba_bersih_entitas_induk": "...",       # opsional, diutamakan untuk ROE/EPS
  "laba_bersih_ttm": "...",                 # opsional, laba 12 bulan terakhir (untuk interim)
  "total_ekuitas": "...", "total_ekuitas_lalu": "...", "ekuitas_entitas_induk": "...",
  "total_liabilitas": "...", "utang_berbunga": "...", "total_aset": "...",
  "saham_beredar": "4,5 miliar",             # lembar
  "harga_saham": "Rp1.250", "tanggal_harga": "2026-09-26", "sumber_harga": "idx.co.id",
  "dividen_per_saham": "Rp50" | "total_dividen": "225 miliar", "tahun_buku_dividen": "2024"
}
Semua kolom opsional; rasio yang datanya kurang ditulis "tidak dihitung" beserta kolom yang kurang.

Cara baca angka (format Indonesia diutamakan):
- "1.234.567" = 1234567 ; "1.250" = 1250 ; "1.234,5" = 1234,5 ; "1,2" = 1,2 ; "1.2" = 1,2
- "1,234" dibaca 1,234 (koma = desimal) dan diberi catatan; "1,234,567" = 1234567 (format Inggris)
- Akhiran: rb/ribu/k = 10^3 ; jt/juta/mn/million = 10^6 ; M/miliar/milyar/B/bn/billion = 10^9 ;
  T/triliun/tn/trillion = 10^12.  "M" dibaca MILIAR (kebiasaan berita Indonesia, mis. "Rp5 M").
- Negatif: "-1.000", "−1.000", atau "(1.000)" (gaya laporan keuangan).
- "Rp", "IDR", "lembar", "saham" diabaikan.

Rumus (semua Decimal, tanpa pembulatan di tengah; tampilan: 2 desimal, rupiah dibulatkan terdekat):
  pertumbuhan  = (sekarang - lalu) / abs(lalu) x 100%   (tidak bermakna bila lalu <= 0)
  margin laba bersih = laba bersih / pendapatan x 100%
  laba setahun = laba_bersih_ttm, atau laba (induk bila ada) x 12 / periode_bulan (disetahunkan sederhana)
  ROE          = laba setahun / ekuitas (induk bila ada; rata-rata awal-akhir bila ekuitas lalu ada) x 100%
  DER          = total liabilitas / total ekuitas (x) ; DER utang berbunga = utang berbunga / total ekuitas
  EPS          = laba setahun / saham beredar ; BVPS = ekuitas (induk bila ada) / saham beredar
  PER          = harga / EPS (tidak bermakna bila EPS <= 0) ; PBV = harga / BVPS (tidak bermakna bila BVPS <= 0)
  kapitalisasi = harga x saham beredar
  imbal dividen = DPS / harga x 100% ; rasio pembayaran = DPS / EPS x 100%

--- Perintah `level`: CSV dengan kolom ---
  kode,harga_sekarang,tanggal_harga,sumber_harga,level_atas,level_bawah,catatan
level_atas / level_bawah = angka yang DITETAPKAN PENGGUNA SENDIRI (boleh salah satu kosong).
Keluaran hanya menyatakan fakta "harga di atas/di bawah level Anda". Exit code: 0 = tidak ada
level tersentuh, 2 = ada level tersentuh, 1 = input salah.

Hanya library standar Python 3.8+.
"""
import argparse
import csv
import json
import re
import sys
from datetime import date, datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

HARI_LAPORAN_PERLU_CEK = 200   # > ~6,5 bulan sejak akhir periode: mungkin ada laporan kuartal lebih baru
HARI_LAPORAN_BASI = 460        # > ~15 bulan: laporan tahunan berikutnya seharusnya sudah terbit
HARI_HARGA_LAMA = 7
BATAS_ANGKA = Decimal(10) ** 18
DISCLAIMER = ("Bukan nasihat investasi. Keputusan & risiko sepenuhnya di tangan Anda. "
              "Cek prospektus/laporan resmi di idx.co.id & situs emiten; info izin & pengaduan: OJK (kontak 157).")


class InputError(ValueError):
    """Kesalahan input yang harus dijelaskan ke pengguna."""


# ----------------------------------------------------------------------------- baca angka
_AKHIRAN = [
    ("triliun", 12), ("trilyun", 12), ("trillion", 12), ("tn", 12), ("t", 12),
    ("miliar", 9), ("milyar", 9), ("billion", 9), ("bn", 9), ("b", 9), ("m", 9),
    ("million", 6), ("juta", 6), ("mio", 6), ("jt", 6), ("mn", 6),
    ("ribu", 3), ("rb", 3), ("thousand", 3), ("k", 3),
]
_SATUAN = {"": 0, "satuan": 0, "rupiah": 0, "ribu": 3, "ribuan": 3, "juta": 6, "jutaan": 6,
           "miliar": 9, "miliaran": 9, "milyar": 9, "triliun": 12}
_BUANG = re.compile(r"(rp\.?|idr|rupiah|lembar|saham)")
_POLA = re.compile(r"^([0-9][0-9.,]*)(" + "|".join(a for a, _ in _AKHIRAN) + r")?$")


def satuan_ke_pangkat(satuan):
    s = (satuan or "").strip().lower()
    if s not in _SATUAN:
        raise InputError(f"satuan_laporan '{satuan}' tidak dikenal (pakai: satuan, ribu, juta, miliar, triliun)")
    return _SATUAN[s]


def _grup_ok(grup):
    return 1 <= len(grup[0]) <= 3 and all(len(g) == 3 for g in grup[1:])


def _normal(num, catatan, asli):
    titik, koma = num.count("."), num.count(",")
    if titik and koma:
        des, rib = (",", ".") if num.rfind(",") > num.rfind(".") else (".", ",")
        bulat, _, pecahan = num.rpartition(des)
        if bulat.count(des) or not _grup_ok(bulat.split(rib)) or not pecahan:
            raise InputError(f"'{asli}': susunan titik/koma tidak wajar")
        return bulat.replace(rib, "") + "." + pecahan
    if koma:
        grup = num.split(",")
        if koma > 1:
            if not _grup_ok(grup):
                raise InputError(f"'{asli}': susunan koma tidak wajar")
            return "".join(grup)
        if not grup[0] or not grup[1]:
            raise InputError(f"'{asli}': koma di awal/akhir angka")
        if len(grup[1]) == 3:
            catatan.append(f"'{asli}' dibaca {grup[0]},{grup[1]} (koma = desimal, format Indonesia); "
                           f"kalau maksudnya ribuan, tulis {grup[0]}.{grup[1]}")
        return grup[0] + "." + grup[1]
    if titik:
        grup = num.split(".")
        if titik > 1:
            if not _grup_ok(grup):
                raise InputError(f"'{asli}': susunan titik tidak wajar")
            return "".join(grup)
        if not grup[0] or not grup[1]:
            raise InputError(f"'{asli}': titik di awal/akhir angka")
        if len(grup[1]) == 3 and len(grup[0]) <= 3:
            return grup[0] + grup[1]          # 1.250 = seribu dua ratus lima puluh
        return grup[0] + "." + grup[1]        # 1.2 T / 12.5 = desimal
    return num


def parse_angka(nilai, pangkat_default=0, catatan=None):
    """Kembalikan Decimal, atau None bila kosong. Raise InputError bila tidak bisa dibaca."""
    catatan = catatan if catatan is not None else []
    if nilai is None:
        return None
    if isinstance(nilai, bool):
        raise InputError(f"'{nilai}' bukan angka")
    if isinstance(nilai, (int, float, Decimal)):
        d = Decimal(str(nilai))
        if not d.is_finite() or abs(d) >= BATAS_ANGKA:
            raise InputError(f"'{nilai}' bukan angka yang wajar")
        return d * (Decimal(10) ** pangkat_default)
    asli = str(nilai).strip()
    s = asli.lower().replace("−", "-").replace("–", "-")
    if s in ("", "-", "n/a", "na", "tidak ada", "kosong"):
        return None
    negatif = False
    if s.startswith("(") and s.endswith(")"):
        negatif, s = True, s[1:-1].strip()
    if s.startswith("-"):
        negatif, s = (not negatif), s[1:].strip()
    s = _BUANG.sub("", s)
    s = s.replace(",-", "").replace(" ", "").replace(" ", "")
    if s.startswith("-"):  # "Rp-1.000"
        negatif, s = (not negatif), s[1:]
    m = _POLA.match(s)
    if not m:
        raise InputError(f"'{asli}' tidak bisa dibaca sebagai angka")
    num, akhiran = m.group(1), m.group(2)
    try:
        d = Decimal(_normal(num, catatan, asli))
    except InvalidOperation:
        raise InputError(f"'{asli}' tidak bisa dibaca sebagai angka")
    pangkat = dict(_AKHIRAN)[akhiran] if akhiran else pangkat_default
    d = d * (Decimal(10) ** pangkat)
    if abs(d) >= BATAS_ANGKA:
        raise InputError(f"'{asli}' terlalu besar, cek kembali satuannya")
    return -d if negatif else d


def parse_tanggal(teks, label):
    if teks in (None, ""):
        return None
    t = str(teks).strip()
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(t, fmt).date()
        except ValueError:
            pass
    raise InputError(f"{label} '{t}' tidak dikenali (pakai YYYY-MM-DD, mis. 2025-12-31)")


# ----------------------------------------------------------------------------- tampilan
def _ribuan(d, desimal):
    q = Decimal(1) if desimal == 0 else Decimal(1).scaleb(-desimal)
    d = d.quantize(q, rounding=ROUND_HALF_UP)
    tanda = "-" if d < 0 else ""
    bulat, _, pecahan = f"{abs(d):f}".partition(".")
    bulat = f"{int(bulat):,}".replace(",", ".")
    return tanda + bulat + ("," + pecahan if pecahan else "")


def fmt_rp(d, desimal=0):
    if d is None:
        return "-"
    teks = _ribuan(d, desimal)
    return ("-Rp" + teks[1:]) if teks.startswith("-") else "Rp" + teks


def fmt_ringkas(d):
    """Rp1,23 T / Rp456,70 M / Rp12,00 jt untuk angka besar."""
    if d is None:
        return "-"
    for pangkat, akhiran in ((12, " T"), (9, " M"), (6, " jt")):
        if abs(d) >= Decimal(10) ** pangkat:
            return fmt_rp(d / Decimal(10) ** pangkat, 2) + akhiran
    return fmt_rp(d)


def fmt_nilai(r):
    v = r["nilai"]
    if v is None:
        return "-"
    if r["satuan"] == "%":
        return _ribuan(v, 2) + "%"
    if r["satuan"] == "x":
        return _ribuan(v, 2) + "x"
    if r["satuan"] == "Rp/saham":
        return fmt_rp(v, 2)
    return fmt_ringkas(v)


# ----------------------------------------------------------------------------- rasio
KOLOM_LAPORAN = ["pendapatan", "pendapatan_lalu", "laba_bersih", "laba_bersih_lalu",
                 "laba_bersih_entitas_induk", "laba_bersih_ttm", "total_ekuitas", "total_ekuitas_lalu",
                 "ekuitas_entitas_induk", "total_liabilitas", "utang_berbunga", "total_aset", "total_dividen"]
KOLOM_LAIN = ["saham_beredar", "harga_saham", "dividen_per_saham"]
LABEL = {
    "pendapatan": "Pendapatan", "pendapatan_lalu": "Pendapatan periode lalu",
    "laba_bersih": "Laba bersih", "laba_bersih_lalu": "Laba bersih periode lalu",
    "laba_bersih_entitas_induk": "Laba bersih entitas induk", "laba_bersih_ttm": "Laba bersih 12 bln terakhir",
    "total_ekuitas": "Total ekuitas", "total_ekuitas_lalu": "Total ekuitas periode lalu",
    "ekuitas_entitas_induk": "Ekuitas entitas induk", "total_liabilitas": "Total liabilitas",
    "utang_berbunga": "Utang berbunga", "total_aset": "Total aset", "total_dividen": "Total dividen",
    "saham_beredar": "Saham beredar (lembar)", "harga_saham": "Harga saham",
    "dividen_per_saham": "Dividen per saham",
}
KOLOM_DIKENAL = set(KOLOM_LAPORAN + KOLOM_LAIN) | {
    "emiten", "nama", "sektor", "periode", "periode_lalu", "periode_bulan", "tanggal_laporan",
    "sumber_laporan", "satuan_laporan", "tanggal_harga", "sumber_harga", "tahun_buku_dividen", "catatan"}


def baca_data(mentah):
    if not isinstance(mentah, dict):
        raise InputError("isi file harus objek JSON {...}")
    catatan = []
    asing = sorted(set(mentah) - KOLOM_DIKENAL)
    if asing:
        catatan.append("kolom tidak dikenal diabaikan: " + ", ".join(asing))
    pangkat = satuan_ke_pangkat(mentah.get("satuan_laporan"))
    angka = {}
    for k in KOLOM_LAPORAN:
        angka[k] = parse_angka(mentah.get(k), pangkat, catatan)
    for k in KOLOM_LAIN:
        angka[k] = parse_angka(mentah.get(k), 0, catatan)
    try:
        bulan = int(str(mentah.get("periode_bulan", 12)).strip() or 12)
    except ValueError:
        raise InputError("periode_bulan harus 3, 6, 9, atau 12")
    if bulan not in (3, 6, 9, 12):
        raise InputError("periode_bulan harus 3, 6, 9, atau 12")
    if angka["saham_beredar"] is not None and angka["saham_beredar"] <= 0:
        raise InputError("saham_beredar harus lebih dari 0")
    if angka["harga_saham"] is not None and angka["harga_saham"] <= 0:
        raise InputError("harga_saham harus lebih dari 0")
    for k in ("dividen_per_saham", "total_dividen", "total_liabilitas", "utang_berbunga", "total_aset"):
        if angka[k] is not None and angka[k] < 0:
            raise InputError(f"{LABEL[k]} tidak boleh negatif")
    info = {k: (str(mentah[k]).strip() if mentah.get(k) not in (None, "") else None)
            for k in ("emiten", "nama", "sektor", "periode", "periode_lalu", "sumber_laporan",
                      "sumber_harga", "tahun_buku_dividen", "catatan")}
    info["periode_bulan"] = bulan
    info["tanggal_laporan"] = parse_tanggal(mentah.get("tanggal_laporan"), "tanggal_laporan")
    info["tanggal_harga"] = parse_tanggal(mentah.get("tanggal_harga"), "tanggal_harga")
    info["satuan_laporan"] = mentah.get("satuan_laporan") or "satuan (rupiah penuh)"
    return info, angka, catatan


def _hasil(kode, nama, satuan, rumus, nilai=None, status="ok", alasan=""):
    return {"kode": kode, "nama": nama, "satuan": satuan, "rumus": rumus,
            "nilai": nilai, "status": status, "alasan": alasan}


def _kurang(kode, nama, satuan, rumus, kolom):
    return _hasil(kode, nama, satuan, rumus, None, "tidak_dihitung", "butuh: " + ", ".join(kolom))


def _tumbuh(kode, nama, now, lalu, kolom):
    rumus = "(sekarang - lalu) / abs(lalu) x 100%"
    kurang = [LABEL[k] for k, v in zip(kolom, (now, lalu)) if v is None]
    if kurang:
        return _kurang(kode, nama, "%", rumus, kurang)
    if lalu == 0:
        return _hasil(kode, nama, "%", rumus, None, "tidak_bermakna", "periode lalu = 0")
    if lalu < 0 and now >= 0:
        return _hasil(kode, nama, "%", rumus, None, "tidak_bermakna",
                      "berbalik dari negatif (rugi) ke positif; persen tidak bermakna")
    if lalu < 0:
        return _hasil(kode, nama, "%", rumus, None, "tidak_bermakna",
                      "periode lalu negatif (rugi); bandingkan nominalnya saja")
    return _hasil(kode, nama, "%", rumus, (now - lalu) / abs(lalu) * 100)


def hitung(info, a):
    r, fakta = [], []
    bulan = info["periode_bulan"]
    r.append(_tumbuh("pertumbuhan_pendapatan", "Pertumbuhan pendapatan", a["pendapatan"], a["pendapatan_lalu"],
                     ["pendapatan", "pendapatan_lalu"]))
    r.append(_tumbuh("pertumbuhan_laba", "Pertumbuhan laba bersih", a["laba_bersih"], a["laba_bersih_lalu"],
                     ["laba_bersih", "laba_bersih_lalu"]))

    rumus = "laba bersih / pendapatan x 100%"
    if a["laba_bersih"] is None or a["pendapatan"] is None:
        r.append(_kurang("margin_bersih", "Margin laba bersih", "%", rumus,
                         [LABEL[k] for k in ("laba_bersih", "pendapatan") if a[k] is None]))
    elif a["pendapatan"] <= 0:
        r.append(_hasil("margin_bersih", "Margin laba bersih", "%", rumus, None, "tidak_bermakna", "pendapatan <= 0"))
    else:
        r.append(_hasil("margin_bersih", "Margin laba bersih", "%", rumus, a["laba_bersih"] / a["pendapatan"] * 100))

    # laba & ekuitas dasar
    laba_induk = a["laba_bersih_entitas_induk"] if a["laba_bersih_entitas_induk"] is not None else a["laba_bersih"]
    dasar_laba = "entitas induk" if a["laba_bersih_entitas_induk"] is not None else "laba bersih total"
    if a["laba_bersih_ttm"] is not None:
        laba_th, ket_laba = a["laba_bersih_ttm"], "laba 12 bulan terakhir (TTM) dari pengguna"
    elif laba_induk is not None and bulan < 12:
        laba_th = laba_induk * 12 / bulan
        ket_laba = f"{dasar_laba} {bulan} bulan x 12/{bulan} (disetahunkan sederhana, abaikan musim)"
        fakta.append(f"Laporan interim {bulan} bulan: ROE, EPS, PER, dan rasio pembayaran memakai laba "
                     f"yang disetahunkan sederhana (x12/{bulan}). Hasil bisa meleset bila usaha musiman.")
    else:
        laba_th, ket_laba = laba_induk, dasar_laba
    ekuitas = a["ekuitas_entitas_induk"] if a["ekuitas_entitas_induk"] is not None else a["total_ekuitas"]
    dasar_ek = "ekuitas entitas induk" if a["ekuitas_entitas_induk"] is not None else "total ekuitas"

    rumus = f"laba setahun / {dasar_ek} x 100%"
    if laba_th is None or ekuitas is None:
        r.append(_kurang("roe", "ROE", "%", rumus,
                         [x for x, v in (("Laba bersih", laba_th), ("Total ekuitas", ekuitas)) if v is None]))
    else:
        penyebut, ket = ekuitas, "akhir periode"
        if a["total_ekuitas_lalu"] is not None and a["ekuitas_entitas_induk"] is None:
            if a["total_ekuitas_lalu"] > 0:
                penyebut, ket = (ekuitas + a["total_ekuitas_lalu"]) / 2, "rata-rata awal & akhir"
            else:
                ket = "akhir periode; ekuitas awal negatif/nol sehingga rata-rata tidak dipakai"
        if ekuitas <= 0 or penyebut <= 0:
            r.append(_hasil("roe", "ROE", "%", rumus, None, "tidak_bermakna", "ekuitas negatif/nol (defisiensi modal)"))
        else:
            r.append(_hasil("roe", "ROE", "%", f"{ket_laba} / {dasar_ek} ({ket}) x 100%", laba_th / penyebut * 100))

    rumus = "total liabilitas / total ekuitas"
    if a["total_liabilitas"] is None or a["total_ekuitas"] is None:
        r.append(_kurang("der", "DER (liabilitas/ekuitas)", "x", rumus,
                         [LABEL[k] for k in ("total_liabilitas", "total_ekuitas") if a[k] is None]))
    elif a["total_ekuitas"] <= 0:
        r.append(_hasil("der", "DER (liabilitas/ekuitas)", "x", rumus, None, "tidak_bermakna",
                        "ekuitas negatif/nol: liabilitas melebihi aset"))
    else:
        r.append(_hasil("der", "DER (liabilitas/ekuitas)", "x", rumus, a["total_liabilitas"] / a["total_ekuitas"]))
    if a["utang_berbunga"] is not None:
        rumus = "utang berbunga / total ekuitas"
        if a["total_ekuitas"] is None:
            r.append(_kurang("der_berbunga", "DER utang berbunga", "x", rumus, ["Total ekuitas"]))
        elif a["total_ekuitas"] <= 0:
            r.append(_hasil("der_berbunga", "DER utang berbunga", "x", rumus, None, "tidak_bermakna", "ekuitas negatif/nol"))
        else:
            r.append(_hasil("der_berbunga", "DER utang berbunga", "x", rumus, a["utang_berbunga"] / a["total_ekuitas"]))

    saham, harga = a["saham_beredar"], a["harga_saham"]
    eps = laba_th / saham if (laba_th is not None and saham) else None
    bvps = ekuitas / saham if (ekuitas is not None and saham) else None
    if eps is None:
        r.append(_kurang("eps", "Laba per saham (EPS, setahun)", "Rp/saham", "laba setahun / saham beredar",
                         [x for x, v in (("Laba bersih", laba_th), ("Saham beredar", saham)) if v is None]))
    else:
        r.append(_hasil("eps", "Laba per saham (EPS, setahun)", "Rp/saham", f"{ket_laba} / saham beredar", eps))
    if bvps is None:
        r.append(_kurang("bvps", "Nilai buku per saham (BVPS)", "Rp/saham", f"{dasar_ek} / saham beredar",
                         [x for x, v in (("Total ekuitas", ekuitas), ("Saham beredar", saham)) if v is None]))
    else:
        r.append(_hasil("bvps", "Nilai buku per saham (BVPS)", "Rp/saham", f"{dasar_ek} / saham beredar", bvps))

    if harga is None:
        for kode, nama, sat in (("per", "PER", "x"), ("pbv", "PBV", "x"), ("kapitalisasi", "Kapitalisasi pasar", "Rp")):
            r.append(_kurang(kode, nama, sat, "butuh harga", ["Harga saham"]))
    else:
        if eps is None:
            r.append(_kurang("per", "PER", "x", "harga / EPS", ["EPS (laba & saham beredar)"]))
        elif eps <= 0:
            r.append(_hasil("per", "PER", "x", "harga / EPS", None, "tidak_bermakna", "EPS <= 0 (rugi)"))
        else:
            r.append(_hasil("per", "PER", "x", "harga / EPS", harga / eps))
        if bvps is None:
            r.append(_kurang("pbv", "PBV", "x", "harga / BVPS", ["BVPS (ekuitas & saham beredar)"]))
        elif bvps <= 0:
            r.append(_hasil("pbv", "PBV", "x", "harga / BVPS", None, "tidak_bermakna", "nilai buku negatif/nol"))
        else:
            r.append(_hasil("pbv", "PBV", "x", "harga / BVPS", harga / bvps))
        if saham is None:
            r.append(_kurang("kapitalisasi", "Kapitalisasi pasar", "Rp", "harga x saham beredar", ["Saham beredar"]))
        else:
            r.append(_hasil("kapitalisasi", "Kapitalisasi pasar", "Rp", "harga x saham beredar", harga * saham))

    dps = a["dividen_per_saham"]
    if dps is None and a["total_dividen"] is not None and saham:
        dps = a["total_dividen"] / saham
    if dps is not None:
        tb = f" (tahun buku {info['tahun_buku_dividen']})" if info.get("tahun_buku_dividen") else ""
        if harga is None:
            r.append(_kurang("imbal_dividen", "Imbal hasil dividen" + tb, "%", "DPS / harga x 100%", ["Harga saham"]))
        else:
            r.append(_hasil("imbal_dividen", "Imbal hasil dividen" + tb, "%", "DPS / harga x 100%", dps / harga * 100))
        if eps is not None and eps > 0:
            r.append(_hasil("rasio_pembayaran", "Rasio pembayaran dividen", "%", "DPS / EPS x 100%", dps / eps * 100))
        fakta.append("Imbal hasil dividen memakai dividen yang SUDAH diumumkan/dibayar; dividen tahun "
                     "berikutnya belum tentu sama.")
    elif a["total_dividen"] is not None:
        r.append(_kurang("imbal_dividen", "Imbal hasil dividen", "%", "DPS / harga x 100%", ["Saham beredar"]))

    # fakta yang perlu diketahui (bukan penilaian)
    if a["total_ekuitas"] is not None and a["total_ekuitas"] < 0:
        fakta.append("EKUITAS NEGATIF (defisiensi modal): total liabilitas melebihi total aset. "
                     "Cek di idx.co.id apakah saham ini diberi notasi khusus.")
    if a["laba_bersih"] is not None and a["laba_bersih"] < 0:
        fakta.append("Periode ini RUGI bersih.")
    if a["laba_bersih_lalu"] is not None and a["laba_bersih_lalu"] < 0 and a["laba_bersih"] is not None \
            and a["laba_bersih"] >= 0:
        fakta.append("Laba berbalik dari rugi (periode lalu) menjadi laba; cek apakah ada pos satu kali "
                     "(penjualan aset, selisih kurs, dll.) di catatan laporan keuangan.")
    for kode, teks in (("pertumbuhan_pendapatan", "Pendapatan turun"), ("pertumbuhan_laba", "Laba bersih turun")):
        h = next(x for x in r if x["kode"] == kode)
        if h["nilai"] is not None and h["nilai"] < 0:
            fakta.append(f"{teks} {_ribuan(-h['nilai'], 2)}% dibanding periode lalu.")
    if a["laba_bersih_entitas_induk"] is None and a["laba_bersih"] is not None:
        fakta.append("Laba entitas induk tidak diisi: ROE/EPS memakai laba bersih total (termasuk "
                     "kepentingan nonpengendali bila ada).")
    sektor = (info.get("sektor") or "").lower()
    if any(k in sektor for k in ("bank", "asuransi", "pembiayaan", "multifinance", "keuangan")):
        fakta.append("Sektor keuangan: DER lazim tinggi karena dana nasabah tercatat sebagai liabilitas; "
                     "jangan dibandingkan dengan DER perusahaan non-keuangan.")
    if a["total_aset"] is not None and a["total_liabilitas"] is not None and a["total_ekuitas"] is not None \
            and a["total_aset"] > 0:
        selisih = abs(a["total_aset"] - a["total_liabilitas"] - a["total_ekuitas"])
        if selisih > a["total_aset"] / 100:
            fakta.append(f"CEK ANGKA: total aset ({fmt_ringkas(a['total_aset'])}) tidak sama dengan liabilitas + "
                         f"ekuitas ({fmt_ringkas(a['total_liabilitas'] + a['total_ekuitas'])}). Mungkin salah "
                         "salin atau beda satuan.")
    return r, fakta


def cek_kesegaran(info, hari_ini, ada_harga):
    out = []
    tl = info["tanggal_laporan"]
    if tl is None:
        out.append("Tanggal laporan tidak diisi: kesegaran data tidak bisa dicek.")
    else:
        umur = (hari_ini - tl).days
        if umur < 0:
            out.append(f"Tanggal laporan {tl} ada di masa depan; cek kembali.")
        elif umur > HARI_LAPORAN_BASI:
            out.append(f"DATA BASI: laporan per {tl} ({umur} hari lalu). Laporan yang lebih baru seharusnya "
                       "sudah terbit; cari di idx.co.id sebelum memakai angka ini.")
        elif umur > HARI_LAPORAN_PERLU_CEK:
            out.append(f"Laporan per {tl} ({umur} hari lalu): cek apakah laporan kuartal yang lebih baru sudah terbit.")
    if ada_harga:
        th = info["tanggal_harga"]
        if th is None:
            out.append("Tanggal harga tidak diisi: PER, PBV, kapitalisasi & imbal dividen memakai harga tanpa tanggal.")
        elif (hari_ini - th).days > HARI_HARGA_LAMA:
            out.append(f"HARGA LAMA: harga per {th} ({(hari_ini - th).days} hari lalu). PER/PBV/imbal dividen "
                       "berubah setiap hari bursa.")
        elif th > hari_ini:
            out.append(f"Tanggal harga {th} ada di masa depan; cek kembali.")
    return out


def proses_rasio(mentah, hari_ini):
    info, angka, catatan = baca_data(mentah)
    rasio, fakta = hitung(info, angka)
    kesegaran = cek_kesegaran(info, hari_ini, angka["harga_saham"] is not None)
    return {"info": info, "angka": angka, "rasio": rasio, "fakta": fakta,
            "kesegaran": kesegaran, "catatan_baca": catatan, "hari_ini": hari_ini}


def _jsonable(o):
    if isinstance(o, Decimal):
        return str(o.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP).normalize()) if o == o else None
    if isinstance(o, date):
        return o.isoformat()
    if isinstance(o, dict):
        return {k: _jsonable(v) for k, v in o.items()}
    if isinstance(o, list):
        return [_jsonable(v) for v in o]
    return o


def md_rasio(h):
    i = h["info"]
    judul = " - ".join(x for x in (i.get("emiten"), i.get("nama")) if x) or "Emiten"
    b = [f"## Hitungan Rasio: {judul}", ""]
    b.append(f"Periode: {i.get('periode') or '-'} ({i['periode_bulan']} bulan)"
             f" | Pembanding: {i.get('periode_lalu') or '-'} | Tanggal laporan: {i['tanggal_laporan'] or '-'}")
    b.append(f"Sumber laporan: {i.get('sumber_laporan') or 'TIDAK DICANTUMKAN'}"
             f" | Harga: {i.get('sumber_harga') or '-'}, per {i['tanggal_harga'] or '-'}"
             f" | Dihitung: {h['hari_ini']}")
    b += ["", "### Angka yang dibaca script (cocokkan dengan sumber)", "",
          f"Satuan laporan: {i['satuan_laporan']}", "", "| Pos | Nilai terbaca |", "|---|---|"]
    for k in KOLOM_LAPORAN + KOLOM_LAIN:
        v = h["angka"][k]
        if v is None:
            continue
        if k == "saham_beredar":
            teks = _ribuan(v, 0) + " lembar"
        elif k in ("harga_saham", "dividen_per_saham"):
            teks = fmt_rp(v, 2 if v != v.to_integral_value() else 0)
        else:
            teks = f"{fmt_rp(v)} ({fmt_ringkas(v)})"
        b.append(f"| {LABEL[k]} | {teks} |")
    b += ["", "### Rasio", "", "| Rasio | Nilai | Keterangan |", "|---|---|---|"]
    for r in h["rasio"]:
        ket = r["rumus"] if r["status"] == "ok" else (
            ("tidak dihitung, " if r["status"] == "tidak_dihitung" else "tidak bermakna: ") + r["alasan"])
        b.append(f"| {_sel(r['nama'])} | {fmt_nilai(r)} | {_sel(ket)} |")
    if h["kesegaran"]:
        b += ["", "### Kesegaran data"] + [f"- {x}" for x in h["kesegaran"]]
    if h["fakta"]:
        b += ["", "### Fakta yang perlu diketahui"] + [f"- {x}" for x in h["fakta"]]
    if h["catatan_baca"]:
        b += ["", "### Catatan cara baca angka"] + [f"- {x}" for x in h["catatan_baca"]]
    b += ["", "Rasio hanyalah hasil hitung dari angka di atas, bukan penilaian murah/mahal atau layak/tidak.",
          "", f"_{DISCLAIMER}_"]
    return "\n".join(b)


# ----------------------------------------------------------------------------- level harga
KOLOM_LEVEL = ["kode", "harga_sekarang", "tanggal_harga", "sumber_harga", "level_atas", "level_bawah", "catatan"]


def proses_level(baris_csv, hari_ini):
    hasil, masalah = [], []
    for no, b in enumerate(baris_csv, start=2):
        b = {(k or "").strip().lower(): (v or "").strip() for k, v in b.items() if k is not None}
        kode = b.get("kode", "").upper()
        if not kode:
            if any(b.values()):
                masalah.append(f"baris {no}: kode saham kosong")
            continue
        try:
            harga = parse_angka(b.get("harga_sekarang"))
            atas = parse_angka(b.get("level_atas"))
            bawah = parse_angka(b.get("level_bawah"))
            tgl = parse_tanggal(b.get("tanggal_harga"), "tanggal_harga")
        except InputError as e:
            masalah.append(f"baris {no} ({kode}): {e}")
            continue
        if atas is None and bawah is None:
            masalah.append(f"baris {no} ({kode}): level_atas dan level_bawah kosong, tidak ada yang dicek")
            continue
        if harga is None:
            masalah.append(f"baris {no} ({kode}): harga_sekarang kosong; ambil dulu dari sumber publik")
            continue
        if harga <= 0 or (atas is not None and atas <= 0) or (bawah is not None and bawah <= 0):
            masalah.append(f"baris {no} ({kode}): harga/level harus lebih dari 0")
            continue
        if atas is not None and bawah is not None and bawah >= atas:
            masalah.append(f"baris {no} ({kode}): level_bawah harus lebih kecil dari level_atas")
            continue
        status, jarak = [], []
        if atas is not None:
            if harga >= atas:
                status.append(f"DI ATAS/SAMA DENGAN level atas Anda ({fmt_rp(atas)})")
            jarak.append(f"{_ribuan((atas - harga) / harga * 100, 2)}% ke level atas")
        if bawah is not None:
            if harga <= bawah:
                status.append(f"DI BAWAH/SAMA DENGAN level bawah Anda ({fmt_rp(bawah)})")
            jarak.append(f"{_ribuan((harga - bawah) / harga * 100, 2)}% ke level bawah")
        peringatan = []
        if tgl is None:
            peringatan.append("tanggal harga tidak diisi")
        elif (hari_ini - tgl).days > HARI_HARGA_LAMA:
            peringatan.append(f"harga lama ({(hari_ini - tgl).days} hari)")
        if not b.get("sumber_harga"):
            peringatan.append("sumber harga tidak dicantumkan")
        hasil.append({"kode": kode, "harga": harga, "tanggal_harga": tgl, "sumber": b.get("sumber_harga") or None,
                      "level_atas": atas, "level_bawah": bawah, "tersentuh": bool(status),
                      "status": status, "jarak": jarak, "peringatan": peringatan, "catatan": b.get("catatan") or None})
    return {"hasil": hasil, "masalah": masalah, "hari_ini": hari_ini,
            "ada_tersentuh": any(x["tersentuh"] for x in hasil)}


def _sel(teks):
    return str(teks).replace("|", "/").replace("\n", " ")


def md_level(h):
    b = [f"## Cek Level Harga Pantauan ({h['hari_ini']})", "",
         "| Kode | Harga | Per tanggal | Level bawah | Level atas | Status | Catatan data |", "|---|---|---|---|---|---|---|"]
    for x in h["hasil"]:
        st = "; ".join(x["status"]) if x["status"] else "di antara level Anda (" + ", ".join(x["jarak"]) + ")"
        b.append(f"| {_sel(x['kode'])} | {fmt_rp(x['harga'])} | {x['tanggal_harga'] or '-'} | {fmt_rp(x['level_bawah'])} | "
                 f"{fmt_rp(x['level_atas'])} | {st} | {_sel(', '.join(x['peringatan']) or (x['sumber'] or '-'))} |")
    if h["masalah"]:
        b += ["", "### Baris yang tidak dicek"] + [f"- {m}" for m in h["masalah"]]
    b += ["", "Level di atas ditetapkan sendiri oleh Anda; notifikasi ini hanya fakta posisi harga, bukan sinyal.",
          "", f"_{DISCLAIMER}_"]
    return "\n".join(b)


# ----------------------------------------------------------------------------- CLI
def main(argv=None):
    ap = argparse.ArgumentParser(description="Rasio dasar saham BEI & cek level harga (tanpa jaringan).")
    sub = ap.add_subparsers(dest="perintah", required=True)
    for nama in ("rasio", "level"):
        p = sub.add_parser(nama)
        p.add_argument("file")
        p.add_argument("--format", choices=("md", "json"), default="md")
        p.add_argument("--hari-ini", help="YYYY-MM-DD (default: tanggal komputer)")
    p = sub.add_parser("angka")
    p.add_argument("teks")
    p.add_argument("--satuan", default="")
    args = ap.parse_args(argv)
    try:
        if args.perintah == "angka":
            cat = []
            v = parse_angka(args.teks, satuan_ke_pangkat(args.satuan), cat)
            print("kosong" if v is None else f"{_ribuan(v, 4).rstrip('0').rstrip(',')}  ({fmt_ringkas(v)})")
            for c in cat:
                print("catatan:", c)
            return 0
        hari_ini = parse_tanggal(args.hari_ini, "--hari-ini") if args.hari_ini else date.today()
        if args.perintah == "rasio":
            with open(args.file, encoding="utf-8-sig") as f:
                try:
                    mentah = json.load(f)
                except json.JSONDecodeError as e:
                    raise InputError(f"file JSON rusak (baris {e.lineno}): {e.msg}")
            h = proses_rasio(mentah, hari_ini)
            print(json.dumps(_jsonable(h), ensure_ascii=False, indent=2) if args.format == "json" else md_rasio(h))
            return 0
        with open(args.file, encoding="utf-8-sig", newline="") as f:
            teks = f.read()
        pemisah = ";" if teks.splitlines() and teks.splitlines()[0].count(";") > teks.splitlines()[0].count(",") else ","
        pembaca = csv.DictReader(teks.splitlines(), delimiter=pemisah)
        kolom = [(k or "").strip().lower() for k in (pembaca.fieldnames or [])]
        if "kode" not in kolom or "harga_sekarang" not in kolom:
            raise InputError("CSV level wajib punya kolom: " + ",".join(KOLOM_LEVEL))
        h = proses_level(list(pembaca), hari_ini)
        print(json.dumps(_jsonable(h), ensure_ascii=False, indent=2) if args.format == "json" else md_level(h))
        return 2 if h["ada_tersentuh"] else 0
    except InputError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    except OSError as e:
        print(f"ERROR: file tidak bisa dibuka: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
