#!/usr/bin/env python3
"""Analisis ekspor iklan mingguan (Meta/TikTok Ads/Shopee Ads/TikTok Shop Ads/Google Ads)
dan gabungan lintas-platform. Output JSON ke stdout (mode --json) atau teks siap kirim.

Hanya memakai library standar Python (3.8+). Lintas OS (Windows: pakai `python`/`py`).
Semua perhitungan uang & persen memakai `decimal.Decimal` (tanpa float).

Sumber nama kolom per platform & status verifikasinya: references/sumber-kolom.md.

v1.0.1: sel kosong = 0 (dengan catatan), baris total dikenali di kolom teks mana pun + cek
angka, pemilihan kolom berprioritas (Google Ads), deteksi mata uang dari kolom Currency &
simbol di sel, baris judul sebelum header, UTF-16, omzet "20 juta", mode gabung lebih jujur.

v1.0.2: ekspor bertingkat (Campaign + Ad set + Ad) dirinci ke level PALING RINCI (iklan), nama
kembar dibedakan dengan induknya, dan catatan sel kosong memakai biaya BARIS itu sendiri (N1).
Baris total dikenali dari kata kepala + kata cakupan ("Total of 2 campaigns", "Totals",
"Total Akun"), dan ada pengaman silang angka: baris yang biayanya ≈ jumlah baris lain diberi ⚠️
atau dibuang bila tayangan & kliknya juga cocok (N2).

v1.0.3 (M1, examples/07-uji-ulang-v1.0.2.md): nama kampanye ASLI berawalan "Total"/"Jumlah" +
angka + kata lain ("Total 12.12 Flash Sale", "Jumlah 2 Pcs Bundling") tidak lagi salah dibuang
sebagai baris total (dulu dianggap "kuat" hanya karena diawali angka, walau kata sesudahnya
bukan kata cakupan seperti "kampanye"/"iklan") - sekarang dihitung sebagai kampanye biasa kecuali
pengaman silang N2 bilang lain. SETIAP baris yang tetap dibuang sebagai baris total (label
"kuat" ATAU "sedang", bukan cuma yang angkanya tidak cocok) sekarang SELALU dapat ⚠️ menyebut
nama & biayanya, supaya pengguna bisa memverifikasi sendiri. Label yang sisanya HANYA angka
("Total 12.12", "Jumlah 2") juga dianggap nama, dan label total di kolom LAIN sementara kolom nama
berisi nama biasa tidak lagi membuang baris: keduanya hanya dianggap total bila lolos cek silang
±2%. M2: biaya ≈ jumlah baris lain dalam ±5% (bukan ±2%) sudah memberi ⚠️ "TERHITUNG DUA KALI".
M3: kolom nama kosong + label mirip total di kolom lain → dibuang HANYA bila biaya, tayangan &
klik ≈ (±2%) jumlah baris-baris tepat di atas/bawahnya (subtotal); selain itu dihitung + ⚠️.

v1.0.4 (N3, examples/08-uji-ulang-v103-akun-b.md): subtotal buatan admin DI KOLOM NAMA yang
memuat nama kampanye ("Subtotal: Retarget Video", "Retarget Video Total", "Jumlah sementara")
tidak lagi terhitung dua kali. Dikenali dari (a) awalan Subtotal/Sub total/Sub-total/Jumlah
sementara -> selalu dikecualikan, atau (b) nama = nama kampanye di atasnya + kata total, atau
(c) nama sama persis tetapi baris tanpa tanggal, dengan biaya ≈ (±2%) jumlah baris-baris kampanye
itu tepat di atasnya. Setiap baris yang dikecualikan diberi ⚠️ nama + biaya; nama yang hanya
MIRIP subtotal tetapi angkanya tidak cocok tetap dihitung + ⚠️. Kalimat ⚠️ M2 dilunakkan.
"""
import argparse
import csv
import hashlib
import io
import json
import os
import re
import sys
from collections import defaultdict
from datetime import date
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation, getcontext

getcontext().prec = 40

NOL = Decimal(0)
SERATUS = Decimal(100)
SERIBU = Decimal(1000)

# --------------------------------------------------------------------------------------
# Tanggal
# --------------------------------------------------------------------------------------

BULAN = {
    "jan": 1, "januari": 1, "january": 1,
    "feb": 2, "februari": 2, "february": 2, "peb": 2, "pebruari": 2,
    "mar": 3, "maret": 3, "march": 3,
    "apr": 4, "april": 4,
    "mei": 5, "may": 5,
    "jun": 6, "juni": 6, "june": 6,
    "jul": 7, "juli": 7, "july": 7,
    "agu": 8, "agt": 8, "agus": 8, "agustus": 8, "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9,
    "okt": 10, "oktober": 10, "oct": 10, "october": 10,
    "nov": 11, "nop": 11, "november": 11, "nopember": 11,
    "des": 12, "desember": 12, "dec": 12, "december": 12,
}
POLA_ISO = re.compile(r"^(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})(?:[ T].*)?$")
POLA_ANGKA_3 = re.compile(r"^(\d{1,2})[-/.](\d{1,2})[-/.](\d{2}|\d{4})(?:[ T].*)?$")
POLA_NAMA_BULAN = re.compile(r"^(\d{1,2})[\s\-/]+([A-Za-z]+)\.?[\s\-/,]+(\d{2}|\d{4})(?:[ T].*)?$")
# "September 14, 2026" (judul laporan Google Ads) dan "14 Sep 2026" di baris judul
POLA_TGL_EN_DI_TEKS = re.compile(r"\b([A-Za-z]{3,9})\.?\s+(\d{1,2}),\s*(\d{4})\b")
POLA_TGL_ID_DI_TEKS = re.compile(r"\b(\d{1,2})\s+([A-Za-z]{3,9})\.?\s+(\d{4})\b")
POLA_ISO_DI_TEKS = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")


def _tahun(t):
    t = int(t)
    return t + 2000 if t < 100 else t


def _buat_tanggal(y, m, d):
    try:
        return date(y, m, d)
    except ValueError:
        return None


def deteksi_urutan(teks_tanggal):
    dmy_pasti = mdy_pasti = False
    for t in teks_tanggal:
        m = POLA_ANGKA_3.match((t or "").strip())
        if not m:
            continue
        a, b = int(m.group(1)), int(m.group(2))
        if a > 12:
            dmy_pasti = True
        if b > 12:
            mdy_pasti = True
    if mdy_pasti and not dmy_pasti:
        return "mdy"
    return "dmy"


def parse_tanggal(teks, urutan="dmy"):
    teks = (teks or "").strip()
    if not teks:
        return None
    m = POLA_ISO.match(teks)
    if m:
        return _buat_tanggal(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = POLA_ANGKA_3.match(teks)
    if m:
        a, b, y = int(m.group(1)), int(m.group(2)), _tahun(m.group(3))
        d, bl = (a, b) if urutan == "dmy" else (b, a)
        return _buat_tanggal(y, bl, d)
    m = POLA_NAMA_BULAN.match(teks)
    if m:
        bl = BULAN.get(m.group(2).lower())
        if bl:
            return _buat_tanggal(_tahun(m.group(3)), bl, int(m.group(1)))
    return None


def tanggal_dalam_teks(teks):
    """Semua tanggal yang bisa dikenali di sebuah teks bebas (baris judul ekspor)."""
    hasil = []
    for m in POLA_TGL_EN_DI_TEKS.finditer(teks):
        bl = BULAN.get(m.group(1).lower())
        if bl:
            t = _buat_tanggal(int(m.group(3)), bl, int(m.group(2)))
            if t:
                hasil.append(t)
    for m in POLA_TGL_ID_DI_TEKS.finditer(teks):
        bl = BULAN.get(m.group(2).lower())
        if bl:
            t = _buat_tanggal(int(m.group(3)), bl, int(m.group(1)))
            if t:
                hasil.append(t)
    for m in POLA_ISO_DI_TEKS.finditer(teks):
        t = _buat_tanggal(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        if t:
            hasil.append(t)
    return hasil


# --------------------------------------------------------------------------------------
# Angka & mata uang di sel
# --------------------------------------------------------------------------------------

# Isi sel yang berarti "tidak ada nilai" (Ads Manager menampilkan "—" untuk metrik kosong).
SEL_KOSONG = {"", "-", "--", "---", "—", "–", "n/a", "na", "null", "none", "(not set)"}

# Simbol/kode mata uang di dalam sel -> kode ISO. Urutan penting (US$/S$ sebelum $).
SIMBOL_MATA_UANG = [
    (re.compile(r"us\$"), "USD"), (re.compile(r"s\$"), "SGD"), (re.compile(r"a\$"), "AUD"),
    (re.compile(r"\$"), "USD"), (re.compile(r"€"), "EUR"), (re.compile(r"£"), "GBP"),
    (re.compile(r"¥"), "JPY/CNY"), (re.compile(r"₱"), "PHP"), (re.compile(r"฿"), "THB"),
    (re.compile(r"₫"), "VND"), (re.compile(r"(?<![a-z])rm(?![a-z])"), "MYR"),
    (re.compile(r"(?<![a-z])rp(?![a-z])\.?"), "IDR"),
]
KODE_MATA_UANG = {"IDR", "USD", "SGD", "MYR", "PHP", "THB", "VND", "EUR", "GBP", "AUD", "JPY",
                  "CNY", "HKD", "TWD", "KRW", "INR", "SAR", "AED"}
POLA_KODE_DI_SEL = re.compile(r"(?<![a-z])(" + "|".join(k.lower() for k in KODE_MATA_UANG) + r")(?![a-z])")
POLA_MATA_UANG_HEADER = re.compile(r"\(([A-Za-z]{3})\)")


def _grup_ribuan_valid(bagian_bulat, pemisah):
    grup = bagian_bulat.split(pemisah)
    return 1 <= len(grup[0]) <= 3 and all(len(g) == 3 for g in grup[1:])


def _angka_bersih(s):
    """String angka tanpa simbol -> Decimal, atau None bila meragukan."""
    if not s:
        return None
    negatif = s.startswith("-")
    s = s.lstrip("-")
    if not s or "-" in s:
        return None
    digit = sum(c.isdigit() for c in s)
    if digit == 0:
        return None
    if s[0] in ".,":            # ",5" / ".5" -> 0,5
        s = "0" + s
    if s[-1] in ".,":
        return None
    if "," in s and "." in s:
        desimal = "," if s.rfind(",") > s.rfind(".") else "."
        ribuan = "." if desimal == "," else ","
        bulat, _, pecahan = s.rpartition(desimal)
        if ribuan in pecahan or not _grup_ribuan_valid(bulat, ribuan):
            return None
        s = bulat.replace(ribuan, "") + "." + pecahan
    elif "," in s or "." in s:
        pemisah = "," if "," in s else "."
        bagian = s.split(pemisah)
        if len(bagian) == 2 and len(bagian[1]) != 3:
            s = bagian[0] + "." + bagian[1]
        elif _grup_ribuan_valid(s, pemisah):
            s = s.replace(pemisah, "")
        else:
            return None
    try:
        nilai = Decimal(s)
    except InvalidOperation:
        return None
    if digit >= 4 and NOL < nilai < 1:
        return None
    return -nilai if negatif else nilai


def baca_sel(teks):
    """Baca satu sel angka. Kembalikan (status, Decimal|None, kode_mata_uang|None).

    status: "kosong" (sel kosong/"-"/"--"/"—"), "ok", atau "rusak" (ada teks yang bukan
    angka, mis. "lima ratus ribu" atau "250.000,00;x"). Simbol/kode mata uang di sel
    (Rp, $, US$, RM, USD, ...) dikenali dan DILAPORKAN, tidak dibuang diam-diam.
    """
    if teks is None:
        return "kosong", None, None
    s = str(teks).replace(" ", " ").strip().lower()
    if s in SEL_KOSONG:
        return "kosong", None, None
    mata_uang = None
    if re.fullmatch(r"\(.*\)", s):
        s = "-" + s[1:-1].strip()
    for pola, kode in SIMBOL_MATA_UANG:
        if pola.search(s):
            mata_uang = mata_uang or kode
            s = pola.sub(" ", s)
    m = POLA_KODE_DI_SEL.search(s)
    if m:
        mata_uang = mata_uang or m.group(1).upper()
        s = POLA_KODE_DI_SEL.sub(" ", s)
    s = re.sub(r"[,.]\s*-\s*$", "", s.strip())       # "10.000,-"
    s = s.replace(" ", "")
    if re.search(r"[^\d,.\-]", s):
        return "rusak", None, mata_uang
    nilai = _angka_bersih(s)
    if nilai is None:
        return "rusak", None, mata_uang
    return "ok", nilai, mata_uang


def parse_angka(teks):
    """Kompatibilitas: angka format Indonesia/Inggris -> Decimal, atau None bila kosong/rusak."""
    status, nilai, _ = baca_sel(teks)
    return nilai if status == "ok" else None


PENGALI_OMZET = {"rb": 10 ** 3, "ribu": 10 ** 3, "k": 10 ** 3, "jt": 10 ** 6, "juta": 10 ** 6,
                 "miliar": 10 ** 9, "milyar": 10 ** 9, "m": None}


def parse_omzet(teks):
    """'20000000', 'Rp20.000.000', '20 juta', '20jt', '1,5 juta', '750 rb', '1,2 miliar'."""
    s = str(teks or "").replace(" ", " ").strip().lower()
    m = re.fullmatch(r"(?:rp\.?\s*)?([\d.,]+)\s*([a-z]+)?\.?", s)
    if not m:
        raise ValueError(f"Nilai --omzet '{teks}' tidak terbaca. Tulis angka penuh (mis. 20000000) "
                         "atau dengan satuan: '20 juta', '20jt', '750 ribu', '1,2 miliar'.")
    angka, satuan = m.group(1), m.group(2)
    if satuan and satuan not in PENGALI_OMZET:
        raise ValueError(f"Satuan '{satuan}' pada --omzet '{teks}' tidak dikenal. Pakai 'ribu'/'rb', "
                         "'juta'/'jt', atau 'miliar'.")
    if satuan and PENGALI_OMZET[satuan] is None:
        raise ValueError(f"'{teks}': huruf 'M' bisa berarti juta (Inggris) atau miliar (Indonesia). "
                         "Tulis 'juta' atau 'miliar', atau angka penuh.")
    nilai = parse_angka(angka)
    if nilai is None:
        raise ValueError(f"Nilai --omzet '{teks}' tidak terbaca sebagai angka rupiah.")
    if satuan:
        nilai = nilai * PENGALI_OMZET[satuan]
    return nilai


# --------------------------------------------------------------------------------------
# Pembulatan & format (aturan eksplisit, sama untuk seluruh library — lihat SKILL.md § Rumus)
# --------------------------------------------------------------------------------------

def D(x):
    if x is None or isinstance(x, Decimal):
        return x
    if isinstance(x, float):
        return Decimal(repr(x))
    return Decimal(x)


def bulat_rupiah(x):
    """Ke rupiah bulat terdekat, 0,5 menjauhi nol."""
    if x is None:
        return None
    return int(D(x).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def bulat1(x):
    """Decimal 1 desimal, 0,05 menjauhi nol (persen & ROAS)."""
    if x is None:
        return None
    return D(x).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


def bulat_satu_desimal(x):
    """Sama dengan bulat1, dikembalikan sebagai float (untuk JSON/kompatibilitas)."""
    if x is None:
        return None
    return float(bulat1(x))


def _ribuan(n):
    return f"{n:,}".replace(",", ".")


def fmt_rp(x):
    if x is None:
        return "-"
    n = bulat_rupiah(x)
    return ("Rp -" if n < 0 else "Rp ") + _ribuan(abs(n))


def fmt_rp_desimal(x, desimal=2):
    """Format Rupiah dengan desimal (mis. untuk kurs): ribuan '.', desimal ','."""
    q = D(x).quantize(Decimal(1).scaleb(-desimal), rounding=ROUND_HALF_UP)
    bulat, _, pecahan = f"{q:f}".partition(".")
    return "Rp " + _ribuan(int(bulat)) + ("," + pecahan if pecahan else "")


def fmt_persen(x):
    if x is None:
        return "-"
    return f"{bulat1(x):f}".replace(".", ",") + "%"


def fmt_x(x):
    return f"{bulat1(x):f}".replace(".", ",") + "x"


fmt_satu_desimal_x = fmt_x


def fmt_angka(x):
    if x is None:
        return "-"
    x = D(x)
    if x == x.to_integral_value():
        n = int(x)
        return ("-" if n < 0 else "") + _ribuan(abs(n))
    q = x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    bulat, _, pecahan = f"{abs(q):f}".partition(".")
    return ("-" if q < 0 else "") + _ribuan(int(bulat)) + "," + pecahan


def bagi(a, b):
    if a is None or b is None or b == 0:
        return None
    return D(a) / D(b)


def kapital(s):
    s = str(s or "")
    return s[:1].upper() + s[1:]


def daftar_nama(nama, maks=4):
    nama = list(nama)
    if len(nama) <= maks:
        return ", ".join(nama)
    return ", ".join(nama[:maks]) + f", dan {len(nama) - maks} lainnya"


# --------------------------------------------------------------------------------------
# Deteksi platform & pemetaan kolom
# --------------------------------------------------------------------------------------

# peran -> (kata kunci BERURUTAN menurut prioritas, kata yang membuat kolom DITOLAK).
# Pencocokan per kata utuh (bukan potongan kata). Lintasan 1: judul kolom PERSIS sama dengan
# kata kunci (setelah label mata uang "(IDR)" dibuang). Lintasan 2: judul kolom MENGANDUNG kata
# kunci. Di tiap lintasan kata kunci dicoba sesuai urutan prioritas, bukan urutan kolom di file.
PERAN_UTAMA = [
    ("biaya", (["amount spent", "jumlah yang dibelanjakan", "biaya bersih", "net cost", "cost", "biaya", "spend", "spent",
                "biaya iklan", "pengeluaran"],
               ["per", "/", "avg", "avg.", "average", "rata", "rata-rata", "roas", "acos", "value",
                "nilai", "%", "budget", "anggaran", "cpc", "cpm", "cpa", "cpv", "bid", "max",
                "maks", "target", "tawaran"])),
    ("nama", (["campaign name", "nama kampanye", "nama iklan", "ad set name", "ad name",
               "campaign", "kampanye", "ad group", "iklan"],
              ["status", "id", "type", "jenis", "tipe", "budget", "anggaran", "objective",
               "tujuan", "bid", "bidding", "delivery", "strategy", "strategi", "start", "end",
               "urutan", "no", "nomor"])),
    ("nilai_hasil", (["purchase conversion value", "results value", "conv. value", "conversion value",
                      "conversions value", "total onsite value", "omzet penjualan", "gmv",
                      "pendapatan kotor", "gross revenue", "nilai konversi", "penjualan langsung",
                      "total purchase value"],
                     ["per", "/", "rate", "persen", "persentase", "rasio", "%", "roas", "acos",
                      "cost", "biaya"])),
    ("hasil", (["results", "conversions", "conversion", "konversi", "pesanan", "orders",
                "purchases", "leads", "messaging conversations started", "messages",
                "hasil"],
               ["cost", "biaya", "per", "/", "value", "nilai", "rate", "ratio", "rasio", "roas",
                "%", "persentase", "tingkat", "indicator", "type", "jenis", "action", "name"])),
    ("klik", (["link clicks", "klik tautan", "clicks (destination)", "clicks", "klik", "jumlah klik"],
              ["cost", "biaya", "cpc", "rate", "ctr", "tingkat", "persentase", "per", "%", "/",
               "through", "unique", "unik", "outbound"])),
    ("tayangan", (["impressions", "impr.", "impresi", "tayangan", "dilihat"],
                  ["cost", "biaya", "cpm", "per", "%", "/", "share", "frequency", "frekuensi",
                   "rate", "top", "abs.", "lost", "persentase"])),
    ("tanggal", (["date", "day", "tanggal", "tgl", "hari"],
                 ["update", "updated", "created", "dibuat", "mulai", "selesai", "start", "starts",
                  "end", "ends", "reporting", "of week", "berakhir"])),
]
PERAN_TAYANGAN_CADANGAN = (["reach", "jangkauan"], ["cost", "biaya", "per", "%", "/"])
KOLOM_PERIODE_AWAL = {"reporting starts", "start date", "tanggal mulai", "reporting start"}
KOLOM_PERIODE_AKHIR = {"reporting ends", "end date", "tanggal selesai", "tanggal berakhir", "reporting end"}
KOLOM_MATA_UANG = {"currency", "currency code", "mata uang", "kode mata uang", "account currency",
                   "account currency code"}

# v1.0.10: tujuan (objective) kampanye. Kampanye bertujuan Traffic/Awareness/Reach/Video views/
# Engagement memang tidak dirancang menghasilkan pesan/pembelian, jadi tidak dinilai dari "hasil".
KOLOM_TUJUAN = {"objective", "campaign objective", "tujuan", "tujuan kampanye", "tujuan iklan",
                "result indicator", "indikator hasil", "result type", "jenis hasil", "optimization goal",
                "tujuan optimasi", "campaign type", "jenis kampanye", "tipe kampanye"}
# (label, kata kunci di sel kolom tujuan, kata kunci di NAMA kampanye/iklan - lebih ketat)
TUJUAN_LAIN = [
    ("Traffic", ["traffic", "outcome traffic", "link click", "link clicks", "landing page view",
                 "landing page views", "lalu lintas", "klik tautan", "kunjungan profil", "profile visit"],
     ["traffic", "lalu lintas"]),
    ("Awareness", ["awareness", "outcome awareness", "brand awareness", "kesadaran", "kesadaran merek"],
     ["awareness", "brand awareness", "kesadaran merek"]),
    ("Reach", ["reach", "jangkauan"], ["reach", "jangkauan"]),
    ("Video views", ["video views", "video view", "thruplay", "tayangan video", "video"],
     ["video views", "thruplay", "tayangan video"]),
    ("Engagement", ["engagement", "outcome engagement", "post engagement", "interaksi", "keterlibatan"],
     ["engagement", "keterlibatan"]),
]


KATA_TUJUAN_HASIL = ["message", "messages", "messaging", "pesan", "whatsapp", "conversation", "conversations",
                     "percakapan", "lead", "leads", "prospek", "purchase", "purchases", "pembelian",
                     "conversion", "conversions", "konversi", "sales", "penjualan", "app install", "app installs"]


def _norm_tujuan(teks):
    return " ".join(re.sub(r"[_:.\-/|]+", " ", str(teks or "").lower()).split())


def deteksi_tujuan_lain(isi_kolom_tujuan, nama_nama):
    """Label tujuan non-konversi ('Traffic', ...) atau None. Sel kolom tujuan diutamakan;
    bila kolom itu ada dan berisi tujuan konversi/pesan, nama kampanye TIDAK dipakai."""
    sel = _norm_tujuan(isi_kolom_tujuan)
    if sel and any(_ada_kata(k, sel) for k in KATA_TUJUAN_HASIL):
        return None        # mis. Meta "OUTCOME_ENGAGEMENT" + pesan WA = tetap kampanye pesan
    if sel:
        for label, kunci_sel, _ in TUJUAN_LAIN:
            if any(_ada_kata(k, sel) for k in kunci_sel):
                return label
        return None
    for nama in nama_nama:
        n = _norm_tujuan(nama)
        for label, _, kunci_nama in TUJUAN_LAIN:
            if any(_ada_kata(k, n) for k in kunci_nama):
                return label
    return None


AMBANG_FINGERPRINT = 2
FINGERPRINT_PLATFORM = [
    ("Meta Ads (Facebook/Instagram)", [("ad set name", 2), ("reach", 1), ("link clicks", 1),
                                        ("amount spent", 1), ("result indicator", 2),
                                        ("reporting starts", 1)]),
    ("TikTok Shop Ads", [("gmv", 2), ("pendapatan kotor", 2), ("pesanan", 1)]),
    ("Shopee Ads", [("dilihat", 1), ("konversi (langsung)", 1), ("acos", 2), ("rasio konversi", 1),
                    ("konversi langsung", 1)]),
    ("TikTok Ads Manager", [("clicks (destination)", 2), ("cpc (destination)", 2),
                            ("cost per conversion", 1)]),
    ("Google Ads", [("impr.", 2), ("avg. cpc", 1), ("cost / conv.", 1), ("conv. value", 1)]),
]


def _norm(h):
    return re.sub(r"\s+", " ", str(h or "").replace("﻿", "").strip().lower())


def _tanpa_label_uang(n):
    return re.sub(r"\s*\(([a-z]{3})\)\s*$", "", n)


def _ada_kata(kata, teks):
    return re.search(r"(?<![a-z0-9])" + re.escape(kata) + r"(?![a-z0-9])", teks) is not None


def _cocok(n, wajib, dilarang, persis):
    if any(_ada_kata(k, n) for k in dilarang):
        return False
    if persis:
        return _tanpa_label_uang(n) == wajib
    return _ada_kata(wajib, n)


def deteksi_kolom(header, override):
    """Kembalikan (dict peran->nama_kolom_asli atau None, daftar_peringatan)."""
    norm = {h: _norm(h) for h in header}
    dipakai = set()
    hasil = {}
    peringatan = []

    for peran, kolom in override.items():
        if kolom:
            if kolom not in header:
                raise ValueError(f"Kolom '{kolom}' (untuk --kolom-{peran.replace('_', '-')}) "
                                  f"tidak ada di file. Kolom tersedia: {', '.join(header)}")
            hasil[peran] = kolom
            dipakai.add(kolom)

    for peran, (wajib_ada, dilarang) in PERAN_UTAMA:
        if peran in hasil:
            continue
        hasil[peran] = None
        for persis in (True, False):
            for kata in wajib_ada:
                for h in header:
                    if h in dipakai or not h:
                        continue
                    if _cocok(norm[h], kata, dilarang, persis):
                        hasil[peran] = h
                        break
                if hasil[peran]:
                    break
            if hasil[peran]:
                break
        if hasil[peran]:
            dipakai.add(hasil[peran])

    if not hasil.get("tayangan"):
        wajib_ada, dilarang = PERAN_TAYANGAN_CADANGAN
        for h in header:
            if h in dipakai:
                continue
            if any(_cocok(norm[h], k, dilarang, False) for k in wajib_ada):
                hasil["tayangan"] = h
                dipakai.add(h)
                peringatan.append(
                    f"Kolom tayangan/impresi tidak ditemukan; memakai '{h}' (jangkauan/reach) "
                    "sebagai gantinya. CPM & CTR jadi perkiraan berbasis jangkauan, bukan tayangan asli.")
                break
    return hasil, peringatan


def deteksi_platform(header):
    norm = " | ".join(_norm(h) for h in header)
    cocok = []
    for nama, penanda in FINGERPRINT_PLATFORM:
        skor = sum(bobot for substr, bobot in penanda if substr in norm)
        if skor >= AMBANG_FINGERPRINT:
            cocok.append((skor, nama))
    if not cocok:
        return None
    cocok.sort(reverse=True)
    return cocok[0][1]


def deteksi_mata_uang(header):
    for h in header:
        m = POLA_MATA_UANG_HEADER.search(h or "")
        if m and m.group(1).upper() in KODE_MATA_UANG:
            return m.group(1).upper(), h
    return None, None


# --------------------------------------------------------------------------------------
# Baca file CSV (encoding, baris judul sebelum header)
# --------------------------------------------------------------------------------------

MAKS_BARIS_JUDUL = 15


def _dekode(mentah):
    if mentah[:2] in (b"\xff\xfe", b"\xfe\xff"):
        return mentah.decode("utf-16"), "utf-16"
    if mentah[:3] == b"\xef\xbb\xbf":
        return mentah.decode("utf-8-sig"), "utf-8-sig"
    awal = mentah[:400]
    if awal.count(b"\x00") > len(awal) // 4:
        for enc in ("utf-16-le", "utf-16-be"):
            try:
                return mentah.decode(enc), enc
            except UnicodeDecodeError:
                continue
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            return mentah.decode(enc), enc
        except UnicodeDecodeError:
            continue
    return mentah.decode("latin-1", errors="replace"), "latin-1"


def _pisah_baris(baris_teks):
    """Pilih pemisah (, ; tab |) yang menghasilkan kolom terbanyak untuk satu baris."""
    terbaik = (1, ",")
    for pemisah in (",", ";", "\t", "|"):
        try:
            sel = next(csv.reader([baris_teks], delimiter=pemisah))
        except (csv.Error, StopIteration):
            continue
        if len(sel) > terbaik[0]:
            terbaik = (len(sel), pemisah)
    return terbaik[1]


def _header_layak(sel, override):
    header = [s.strip() for s in sel]
    if sum(1 for h in header if h) < 3:
        return False
    wajib_override = [k for k in override.values() if k]
    if wajib_override:
        return all(k in header for k in wajib_override)
    try:
        kolom, _ = deteksi_kolom(header, {})
    except ValueError:
        return False
    return bool(kolom.get("biaya")) and bool(kolom.get("tayangan") or kolom.get("klik") or kolom.get("hasil"))


def baca_csv(path, override=None):
    """Kembalikan (header, daftar_baris_dict, info). Info: encoding, baris judul yang dilewati."""
    override = override or {}
    with open(path, "rb") as f:
        mentah = f.read()
    if not mentah.strip():
        raise ValueError("File kosong (0 byte). Ekspor ulang dari Ads Manager.")
    if mentah[:4] == b"PK\x03\x04" or mentah[:4] == b"\xd0\xcf\x11\xe0":
        raise ValueError("File ini adalah file Excel (.xlsx/.xls), bukan CSV, walaupun namanya "
                         "mungkin .csv. Buka di Excel/Google Sheets lalu File > Save As / Download > "
                         "CSV, kemudian kirim ulang.")
    teks, enc = _dekode(mentah)
    teks = teks.lstrip("﻿")
    baris_teks = teks.splitlines()
    if not any(b.strip() for b in baris_teks):
        raise ValueError("File kosong. Ekspor ulang dari Ads Manager.")

    idx_header = None
    for i, b in enumerate(baris_teks[:MAKS_BARIS_JUDUL]):
        if not b.strip():
            continue
        pemisah = _pisah_baris(b)
        try:
            sel = next(csv.reader([b], delimiter=pemisah))
        except (csv.Error, StopIteration):
            continue
        if _header_layak(sel, override):
            idx_header = i
            break
    if idx_header is None:
        idx_header = next(i for i, b in enumerate(baris_teks) if b.strip())
    pemisah = _pisah_baris(baris_teks[idx_header])
    judul = [b.strip() for b in baris_teks[:idx_header] if b.strip()]
    try:
        semua = list(csv.reader(io.StringIO("\n".join(baris_teks[idx_header:])), delimiter=pemisah))
    except csv.Error as e:
        raise ValueError(f"File tidak bisa dibaca sebagai CSV ({e}). Pastikan file benar-benar hasil "
                          "ekspor CSV, bukan file rusak/format lain.")
    header = [h.replace("﻿", "").strip() for h in semua[0]]
    baris = []
    for no, sel in enumerate(semua[1:], start=idx_header + 2):
        d = {}
        for j, h in enumerate(header):
            if h and h not in d:
                d[h] = sel[j] if j < len(sel) else ""
        d["__no_baris__"] = no
        d["__sel__"] = sel
        baris.append(d)
    return header, baris, {"encoding": enc, "baris_judul": judul, "pemisah": pemisah}


# --------------------------------------------------------------------------------------
# Baris total
# --------------------------------------------------------------------------------------

# Kata kepala baris total/ringkasan (di AWAL sel). Setelah kata kepala, sisa teks menentukan
# kekuatan label:
#   "kuat"   : tidak ada sisa, atau sisa diawali tanda baca/angka ("Total", "Total:", "Total (5 iklan)",
#              "Total: Account", "Total 4 kampanye", "TOTAL - Semua").
#   "sedang" : sisa HANYA berisi kata cakupan/angka ("Total of 2 campaigns", "Totals", "Total Akun",
#              "Jumlah Keseluruhan", "Grand total all campaigns").
#   "lemah"  : sisa berisi kata lain ("Total Look Hijab", "Total 12.12 Flash Sale") ATAU hanya angka
#              ("Total 12.12", "Jumlah 2") -> tetap dihitung sebagai kampanye, kecuali angkanya
#              ≈ jumlah baris lain (pengaman silang di analisis_file). (v1.0.3)
KEPALA_TOTAL = r"(?:grand[\s-]*totals?|sub[\s-]*totals?|totals?|jumlah|summary|ringkasan|keseluruhan|" \
               r"overall|semua\s+kampanye|all\s+campaigns)"
POLA_KEPALA_TOTAL = re.compile(r"^[^\w]*" + KEPALA_TOTAL + r"(?![a-z0-9])(.*)$", re.IGNORECASE | re.DOTALL)
POLA_KATA_KEPALA = re.compile(r"^" + KEPALA_TOTAL + r"$", re.IGNORECASE)
KATA_CAKUPAN = {
    "of", "for", "the", "all", "per", "in", "and", "dan", "dari", "untuk", "semua", "seluruh",
    "seluruhnya", "keseluruhan", "overall", "total", "totals", "jumlah", "grand", "sub", "summary",
    "ringkasan", "akun", "account", "accounts", "campaign", "campaigns", "kampanye", "iklan", "ad",
    "ads", "adset", "adsets", "set", "sets", "group", "groups", "grup", "adgroup", "adgroups",
    "result", "results", "hasil", "report", "laporan", "periode", "period", "minggu", "week",
    "weekly", "mingguan", "harian", "daily", "day", "days", "hari", "row", "rows", "baris", "data",
    "filtered", "terfilter", "search", "display", "video", "shopping", "performance", "max", "pmax",
    "demand", "gen", "app", "apps", "toko", "shop", "store", "produk", "product", "products",
    "keyword", "keywords", "kata", "kunci", "item", "items", "idr", "rp", "value", "values",
}
TANDA_BACA_TOTAL = set(":(-–—=|/,.[#*;")
TOLERANSI_TOTAL = Decimal("0.02")   # ±2%: batas "hampir sama" untuk cek angka baris total
TOLERANSI_CURIGA = Decimal("0.05")  # ±5%: biaya saja ≈ jumlah baris lain -> hanya ⚠️ (M2), tidak dibuang

# v1.0.4 (N3): awalan subtotal di KOLOM NAMA. "Subtotal"/"Sub total"/"Sub-total"/"Jumlah sementara"
# hampir tidak pernah dipakai sebagai nama kampanye -> baris ini selalu dikecualikan (+ ⚠️).
POLA_AWALAN_SUBTOTAL = re.compile(r"^[^\w]*(?:sub[\s-]*totals?|jumlah\s+sementara)(?![a-z0-9])(.*)$",
                                  re.IGNORECASE | re.DOTALL)
# Kata yang boleh menempel pada nama kampanye untuk membentuk label subtotal ("Retarget Video Total",
# "Total: Retarget Video", "Jumlah Retarget Video").
KATA_SUBTOTAL = {"total", "totals", "subtotal", "subtotals", "sub", "jumlah", "sementara", "sum", "jml",
                 "grand"}


def _norm_nama(teks):
    return " ".join(str(teks or "").split()).lower()


def awalan_subtotal(nama):
    """Sisa nama (tanpa tanda baca pinggir) bila `nama` diawali kata subtotal, else None."""
    m = POLA_AWALAN_SUBTOTAL.match(_norm_nama(nama))
    if not m:
        return None
    return re.sub(r"^[\W_]+|[\W_]+$", "", m.group(1))


def nama_subtotal_dari(nama, induk):
    """True bila `nama` = `induk` + HANYA kata total/subtotal/tanda baca, mis. 'Retarget Video Total'
    atau 'Total: Retarget Video' untuk induk 'Retarget Video'."""
    n, k = _norm_nama(nama), _norm_nama(induk)
    if not k or n == k or k not in n:
        return False
    token = re.findall(r"[^\W_]+", n.replace(k, " ", 1))
    return bool(token) and all(t in KATA_SUBTOTAL for t in token)


def jenis_label_total(teks):
    """'kuat' | 'sedang' | 'lemah' | None untuk satu isi sel teks.

    v1.0.3 (M1, examples/07-uji-ulang-v1.0.2.md): sebelumnya, sisa teks yang DIAWALI ANGKA
    langsung dianggap "kuat" tanpa mengecek kata sesudahnya - jadi "Total 12.12 Flash Sale" atau
    "Jumlah 2 Pcs Bundling" (nama kampanye ASLI yang kebetulan diawali angka setelah kata
    "Total"/"Jumlah") ikut dibuang sebagai baris total, padahal "Flash Sale"/"Pcs Bundling" bukan
    kata cakupan ringkasan. Sekarang, sisa yang diawali angka/tanda baca HANYA "kuat" kalau
    SEMUA token sesudahnya kata cakupan/angka juga (mis. "Total 4 kampanye", "Total (5 iklan)") -
    kalau ada kata lain yang bukan cakupan, turun jadi "lemah" (tetap dihitung sebagai kampanye,
    kecuali pengaman silang angka di analisis_file bilang lain)."""
    s = " ".join(str(teks or "").split()).lower()
    m = POLA_KEPALA_TOTAL.match(s)
    if not m:
        return None
    sisa = m.group(1).strip()
    if not sisa:
        return "kuat"
    token = re.findall(r"[^\W\d_]+|\d+", sisa)
    semua_cakupan = bool(token) and all(t.isdigit() or t in KATA_CAKUPAN or POLA_KATA_KEPALA.match(t) for t in token)
    if token and all(t.isdigit() for t in token):
        # "Total 12.12", "Jumlah 2", "Total (3)": sisa hanya angka -> bisa nama kampanye
        # (tanggal promo/jumlah pcs). Dianggap total hanya lewat cek silang angka.
        return "lemah"
    if sisa[0] in TANDA_BACA_TOTAL or sisa[0].isdigit():
        return "kuat" if (semua_cakupan or not token) else "lemah"
    return "sedang" if semua_cakupan else "lemah"


def teks_total(r, header):
    """Kembalikan (isi sel, jenis) untuk sel TEKS yang berbunyi total/jumlah, else None.
    Label kuat/sedang didahulukan daripada label lemah bila ada di beberapa sel."""
    lemah = None
    for h in header:
        v = (r.get(h) or "").strip()
        if not v or baca_sel(v)[0] == "ok":
            continue
        jenis = jenis_label_total(v)
        if jenis in ("kuat", "sedang"):
            return v, jenis
        if jenis == "lemah" and lemah is None:
            lemah = (v, jenis)
    return lemah


# Level rincian untuk ekspor bertingkat (mis. Meta: Campaign name + Ad set name + Ad name).
# Urutan = paling rinci dulu. Judul kolom dicocokkan PERSIS (setelah label "(IDR)" dibuang).
LEVEL_NAMA = [
    ("iklan", {"ad name", "nama iklan"}),
    ("grup iklan", {"ad set name", "nama set iklan", "ad group name", "nama grup iklan", "ad group",
                    "grup iklan", "ad set"}),
    ("kampanye", {"campaign name", "nama kampanye", "campaign", "kampanye"}),
]


def pilih_level_nama(header, data):
    """Bila file memuat >= 2 level nama yang terisi, kembalikan (level, kolom_rinci, [kolom_induk...]),
    else None. Kolom induk diurutkan dari yang terdekat (ad set) ke terjauh (kampanye)."""
    tersedia = []
    for level, kata in LEVEL_NAMA:
        for h in header:
            if h and _tanpa_label_uang(_norm(h)) in kata and any((r.get(h) or "").strip() for r in data):
                tersedia.append((level, h))
                break
    if len(tersedia) < 2:
        return None
    return tersedia[0][0], tersedia[0][1], [h for _, h in tersedia[1:]]


# --------------------------------------------------------------------------------------
# Analisis satu file (satu platform, satu minggu)
# --------------------------------------------------------------------------------------

def sidik_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def _rentang(tgl):
    return (min(tgl), max(tgl)) if tgl else (None, None)


def analisis_file(path, override, args):
    header, data, info = baca_csv(path, override)
    if not data:
        raise ValueError("File hanya berisi judul kolom, tanpa baris data. Ekspor ulang dengan "
                         "rentang tanggal yang benar.")

    kolom, peringatan_kolom = deteksi_kolom(header, override)
    wajib = ["biaya", "tayangan", "klik", "hasil"]
    hilang = [k for k in wajib if not kolom.get(k)]
    if hilang:
        petunjuk = ""
        if len([h for h in header if h]) <= 2:
            petunjuk = (" Baris pertama file tampaknya judul/keterangan, bukan nama kolom, dan "
                        f"tabel tidak ditemukan dalam {MAKS_BARIS_JUDUL} baris pertama. Pastikan "
                        "file berisi tabel kampanye.")
        raise ValueError(
            "Kolom wajib tidak terdeteksi otomatis: " + ", ".join(hilang) + ". "
            "Beri tahu nama kolomnya lewat opsi --kolom-" +
            "/--kolom-".join(x.replace("_", "-") for x in hilang) +
            f". Kolom yang ada di file: {', '.join(h for h in header if h)}." + petunjuk)

    platform_terdeteksi = args.platform or deteksi_platform(header) or "Tidak diketahui"
    catatan = []
    peringatan = list(peringatan_kolom)

    # --- N1: ekspor bertingkat -> rinci ke level paling rinci (iklan > grup iklan > kampanye) ---
    kolom_induk = []
    level_rincian = None
    if not override.get("nama"):
        lv = pilih_level_nama(header, data)
        if lv:
            level_rincian, kolom["nama"], kolom_induk = lv
            catatan.append(
                f"File memuat beberapa level nama ({', '.join([kolom['nama']] + kolom_induk)}). Laporan "
                f"dirinci per {level_rincian} (kolom '{kolom['nama']}', paling rinci) agar {level_rincian} "
                f"yang boros tidak tersembunyi di dalam total induknya. Untuk rincian per "
                f"{'kampanye' if level_rincian != 'kampanye' else level_rincian}, jalankan ulang dengan "
                f"--kolom-nama \"{kolom_induk[-1]}\".")
    # v1.0.5 (P-3): kolom grup aset (Google Performance Max) sebagai nama cadangan bila kolom nama kosong
    kolom_aset = next((h for h in header if h and h != kolom.get("nama") and _tanpa_label_uang(_norm(h)) in
                       {"asset group", "asset group name", "grup aset", "nama grup aset"}), None)
    if info["baris_judul"]:
        catatan.append(f"{len(info['baris_judul'])} baris judul/keterangan di atas tabel dilewati "
                       f"(mis. '{info['baris_judul'][0][:60]}').")
    if info["encoding"].startswith("utf-16"):
        catatan.append("File berformat UTF-16 (CSV ala Excel) dan sudah dibaca otomatis.")

    kolom_uang = next((h for h in header if _norm(h) in KOLOM_MATA_UANG), None)
    kolom_tujuan = next((h for h in header if h and _tanpa_label_uang(_norm(h)) in KOLOM_TUJUAN), None)
    kolom_awal = next((h for h in header if _norm(h) in KOLOM_PERIODE_AWAL), None)
    kolom_akhir = next((h for h in header if _norm(h) in KOLOM_PERIODE_AKHIR), None)

    urutan = "dmy"
    kolom_tgl_semua = [k for k in (kolom.get("tanggal"), kolom_awal, kolom_akhir) if k]
    if kolom_tgl_semua:
        urutan = deteksi_urutan([r.get(k) for r in data for k in kolom_tgl_semua])

    peran_angka = ["biaya", "tayangan", "klik", "hasil"] + (["nilai_hasil"] if kolom.get("nilai_hasil") else [])
    rekaman = []
    baris_total = []
    kosong_per_kolom = defaultdict(list)     # peran -> [rekaman baris yang selnya kosong]
    rusak_metrik = []                        # (nama, kolom, isi)
    biaya_rusak = []                         # (nama, isi)
    biaya_negatif = []
    kode_sel = set()
    kode_kolom = set()
    baris_tanpa_angka = 0
    # (label, biaya_atau_None) untuk SETIAP baris yang dibuang sebagai total berlabel "kuat"/
    # "sedang" - dipakai supaya SETIAP baris yang dibuang selalu dapat ⚠️ menyebut nama & biayanya
    # (temuan M1), bukan cuma label "sedang" yang angkanya tidak cocok seperti versi sebelumnya.
    baris_total_info = []
    # v1.0.5 (P-4): (indeks peringatan, biaya baris, dihitung?) -> setelah total dihitung, ⚠️ subtotal/total
    # yang meragukan ditambah kalimat "bila baris itu (tidak) dihitung, total belanja menjadi ...".
    alt_total = []

    for r in data:
        sel = [s for s in r["__sel__"] if (s or "").strip()]
        if not sel:
            continue
        label_total = teks_total(r, header)
        # v1.0.3 (M1): label total di kolom LAIN, sementara kolom nama berisi nama biasa (bukan label
        # total) -> baris itu kampanye bernama; hanya dianggap total lewat cek silang angka.
        if label_total and label_total[1] in ("kuat", "sedang") and kolom.get("nama"):
            isi_nama = " ".join((r.get(kolom["nama"]) or "").split())
            # "--"/"-" (placeholder Google Ads di baris total) bukan nama.
            if any(c.isalnum() for c in isi_nama) and jenis_label_total(isi_nama) not in ("kuat", "sedang"):
                label_total = (label_total[0], "lemah")
        if label_total and label_total[1] in ("kuat", "sedang"):
            baris_total.append(label_total[0])
            st_b, v_b, _ = baca_sel(r.get(kolom["biaya"]))
            baris_total_info.append((label_total[0], v_b if st_b == "ok" else None))
            continue

        nama = " ".join((r.get(kolom["nama"]) or "").split()) if kolom.get("nama") else ""
        nama_asli_kosong = not nama
        if not nama and not label_total:
            # v1.0.5 (P-3): baris tanpa grup iklan/iklan (mis. Google Performance Max) memakai nama
            # grup aset, lalu nama induknya (kampanye), bukan "(tanpa nama, baris N)".
            for h in [kolom_aset] + kolom_induk:
                isi = " ".join((r.get(h) or "").split()) if h else ""
                if any(c.isalnum() for c in isi) and jenis_label_total(isi) not in ("kuat", "sedang"):
                    nama = isi if h == kolom_aset else f"{isi} (tanpa {level_rincian or 'nama'})"
                    break
        if not nama:
            nama = f"(tanpa nama, baris {r['__no_baris__']})"

        dibaca = {}
        for peran in peran_angka:
            status, nilai, kode = baca_sel(r.get(kolom[peran]))
            if kode and peran in ("biaya", "nilai_hasil"):
                kode_sel.add(kode)
            dibaca[peran] = (status, nilai, r.get(kolom[peran]))

        if all(dibaca[p][0] == "kosong" for p in ("biaya", "tayangan", "klik", "hasil")):
            baris_tanpa_angka += 1
            continue

        st_biaya, biaya, isi_biaya = dibaca["biaya"]
        if st_biaya == "rusak":
            biaya_rusak.append((nama, isi_biaya))
            continue
        if st_biaya == "kosong":
            biaya = NOL
        if biaya < 0:
            biaya_negatif.append((nama, biaya))

        nilai = {"nama": nama, "biaya": biaya, "no_baris": r["__no_baris__"],
                 "nama_asli": "" if nama_asli_kosong else nama, "n3": False,
                 # M3: kolom nama kosong + label mirip total di kolom lain -> kandidat subtotal,
                 # dicek silang dengan baris-baris tetangganya setelah loop.
                 "kandidat_subtotal": label_total[0] if (nama_asli_kosong and label_total) else None,
                 "induk": tuple(" ".join((r.get(h) or "").split()) for h in kolom_induk),
                 "label_lemah": label_total[0] if label_total else None,
                 "tgl_ok": [], "tgl_rusak": []}
        nilai["tujuan_lain"] = deteksi_tujuan_lain(r.get(kolom_tujuan) if kolom_tujuan else "",
                                                   [nama] + [x for x in nilai["induk"] if x])
        if st_biaya == "kosong":
            kosong_per_kolom["biaya"].append(nilai)
        for peran in peran_angka[1:]:
            st, v, isi = dibaca[peran]
            if st == "kosong":
                kosong_per_kolom[peran].append(nilai)
                v = NOL
            elif st == "rusak":
                rusak_metrik.append((nama, kolom[peran], isi))
                v = NOL
            nilai[peran] = v
        nilai.setdefault("nilai_hasil", NOL)

        if kolom_uang:
            v = (r.get(kolom_uang) or "").strip().upper()
            if v:
                kode_kolom.add(v)

        for k in kolom_tgl_semua:
            teks_tgl = (r.get(k) or "").strip()
            if not teks_tgl:
                continue
            t = parse_tanggal(teks_tgl, urutan)
            if t:
                nilai["tgl_ok"].append(t)
            else:
                nilai["tgl_rusak"].append(teks_tgl)

        rekaman.append(nilai)

    # --- N1: nama iklan kembar di induk berbeda -> dibedakan dengan nama induknya ---
    if kolom_induk:
        jalur_per_nama = defaultdict(set)
        for x in rekaman:
            jalur_per_nama[x["nama"]].add(x["induk"])
        kembar = sorted(n for n, j in jalur_per_nama.items() if len(j) > 1)
        for x in rekaman:
            if x["nama"] in kembar:
                jalur = jalur_per_nama[x["nama"]]
                if len({j[0] for j in jalur}) == len(jalur):
                    tambahan = x["induk"][0] or "-"
                else:
                    tambahan = " / ".join(i or "-" for i in reversed(x["induk"]))
                x["nama"] = f"{x['nama']} ({tambahan})"
        if kembar:
            catatan.append(f"{len(kembar)} nama {level_rincian} dipakai di lebih dari satu "
                           f"'{kolom_induk[0]}' ({daftar_nama(kembar)}); dibedakan dengan nama induknya "
                           "dalam kurung.")

    # --- mata uang: label kolom (IDR), kolom Currency, simbol di sel ---
    kode_label, kolom_label = deteksi_mata_uang(
        [kolom["biaya"]] + ([kolom["nilai_hasil"]] if kolom.get("nilai_hasil") else []))
    kode_semua = set(kode_sel) | set(kode_kolom) | ({kode_label} if kode_label else set())
    asing = sorted(kode_semua - {"IDR"})
    sumber = []
    if kode_label:
        sumber.append(f"label kolom '{kolom_label}'")
    if kode_kolom:
        sumber.append(f"kolom '{kolom_uang}' = {', '.join(sorted(kode_kolom))}")
    if kode_sel:
        sumber.append(f"simbol di sel biaya/nilai ({', '.join(sorted(kode_sel))})")
    catatan_mata_uang = []
    kurs = Decimal(1)
    mata_uang_final = "IDR"
    if len(asing) > 1 or (asing and "IDR" in kode_semua):
        raise ValueError(
            "File ini mencampur lebih dari satu mata uang (" + "; ".join(sumber) + "). Skill ini "
            "tidak menjumlah mata uang berbeda. Pisahkan ekspor per akun/mata uang, atau pakai "
            "--mata-uang IDR bila Anda yakin semua angka sudah Rupiah.")
    if asing:
        kode = asing[0]
        if args.mata_uang == "IDR":
            catatan_mata_uang.append(
                f"File tampak ber-mata uang {kode} ({'; '.join(sumber)}), tetapi dianggap IDR "
                "sesuai perintah eksplisit --mata-uang IDR.")
        elif args.kurs is not None:
            kurs = args.kurs
            sumber_kurs = f", sumber: {args.kurs_sumber}" if args.kurs_sumber else ""
            tanggal_kurs = f" per {args.kurs_tanggal}" if args.kurs_tanggal else ""
            mata_uang_final = f"IDR (dikonversi dari {kode})"
            catatan_mata_uang.append(
                f"Nilai dikonversi dari {kode} ke IDR dengan kurs 1 {kode} = {fmt_rp_desimal(kurs)}"
                f"{tanggal_kurs}{sumber_kurs} (kurs diberikan pengguna, bukan realtime). "
                f"Terdeteksi dari: {'; '.join(sumber)}.")
        else:
            raise ValueError(
                f"File ini memakai mata uang {kode}, bukan Rupiah (terdeteksi dari: {'; '.join(sumber)}). "
                "Skill ini menghitung dalam Rupiah dan TIDAK mengonversi diam-diam. Jalankan ulang "
                f"dengan --kurs <angka> (nilai tukar 1 {kode} ke Rupiah, boleh tambah --kurs-sumber/"
                "--kurs-tanggal) atau --mata-uang IDR bila angkanya memang sudah Rupiah.")
    elif not kode_semua:
        catatan_mata_uang.append("Tidak ada label mata uang di file; diasumsikan IDR (Rupiah).")

    def _dekat(a, b, batas=TOLERANSI_TOTAL):
        return abs(a - b) <= b * batas

    metrik_silang = ("biaya", "tayangan", "klik")

    def _cocok_jumlah(x, grup, semua_metrik):
        """Biaya x ≈ (±2%) jumlah biaya grup; tayangan & klik ikut dicek bila semua_metrik, atau bila
        baris x memang punya angkanya (subtotal yang hanya mengisi biaya tetap dikenali)."""
        if x["biaya"] <= 0 or not grup:
            return False
        for k in metrik_silang:
            acc = sum((g[k] for g in grup), NOL)
            if k == "biaya" or semua_metrik or x[k] != 0:
                if not _dekat(x[k], acc):
                    return False
        return True

    def _jalan(i, arah, x):
        """Cari n baris beruntun tepat di atas (arah -1) / bawah (+1) yang jumlahnya ≈ baris x."""
        grup, j = [], i + arah
        while 0 <= j < len(rekaman) and not rekaman[j]["kandidat_subtotal"] and not rekaman[j]["n3"]:
            grup.append(rekaman[j])
            if _cocok_jumlah(x, grup, False):
                return grup
            if sum((g["biaya"] for g in grup), NOL) > x["biaya"] * (1 + TOLERANSI_TOTAL):
                return None
            j += arah
        return None

    # --- N3 (v1.0.4): subtotal buatan admin DI KOLOM NAMA ("Subtotal: Retarget Video") ---
    for i, x in enumerate(rekaman):
        if x["kandidat_subtotal"] or not x["nama_asli"]:
            continue
        # baris-baris beruntun tepat di atasnya yang namanya sama (mis. 3 baris harian "Retarget Video")
        run, j = [], i - 1
        while j >= 0 and not rekaman[j]["kandidat_subtotal"] and not rekaman[j]["n3"] and (
                not run or _norm_nama(rekaman[j]["nama_asli"]) == _norm_nama(run[0]["nama_asli"])):
            if not rekaman[j]["nama_asli"]:
                break
            run.append(rekaman[j])
            j -= 1
        induk = run[0]["nama_asli"] if run else ""
        b_x = fmt_rp(x["biaya"] * kurs)
        sisa = awalan_subtotal(x["nama_asli"])
        if sisa is not None:
            alasan = None
            if run and _norm_nama(sisa) == _norm_nama(induk) and _cocok_jumlah(x, run, False):
                alasan = (f"sama dengan jumlah {len(run)} baris '{induk}' tepat di atasnya "
                          f"({fmt_rp(sum((g['biaya'] for g in run), NOL) * kurs)})")
            else:
                for arah, kata_arah in ((-1, "di atasnya"), (1, "di bawahnya")):
                    grup = _jalan(i, arah, x)
                    if grup:
                        alasan = (f"sama dengan jumlah {len(grup)} baris tepat {kata_arah} "
                                  f"({fmt_rp(sum((g['biaya'] for g in grup), NOL) * kurs)})")
                        break
            if alasan is None and sisa:
                grup = [y for y in rekaman if y is not x and not y["n3"]
                        and _norm_nama(y["nama_asli"]) == _norm_nama(sisa)]
                if _cocok_jumlah(x, grup, False):
                    alasan = (f"sama dengan jumlah semua baris '{grup[0]['nama_asli']}' "
                              f"({fmt_rp(sum((g['biaya'] for g in grup), NOL) * kurs)})")
            x["n3"] = True
            if alasan:
                peringatan.append(
                    f"Baris '{x['nama_asli']}' (baris {x['no_baris']}, biaya {b_x}) tampaknya subtotal "
                    f"buatan lembar kerja: biayanya {alasan}. Baris ini tidak dihitung supaya biayanya "
                    "tidak terjumlah dua kali. Bila itu kampanye sungguhan, mohon ganti namanya di file "
                    "lalu jalankan ulang.")
            else:
                alt_total.append((len(peringatan), x["biaya"], False))
                peringatan.append(
                    f"Baris '{x['nama_asli']}' (baris {x['no_baris']}, biaya {b_x}) diawali kata "
                    "'Subtotal'/'Jumlah sementara', jadi dianggap subtotal dan tidak dihitung, walaupun "
                    "angkanya tidak cocok dengan jumlah baris di sekitarnya. Mohon cek file; bila itu "
                    "kampanye sungguhan, ganti namanya lalu jalankan ulang.")
            continue
        if not run:
            continue
        b_run = fmt_rp(sum((g["biaya"] for g in run), NOL) * kurs)
        if nama_subtotal_dari(x["nama_asli"], induk):
            if _cocok_jumlah(x, run, False):
                x["n3"] = True
                peringatan.append(
                    f"Baris '{x['nama_asli']}' (baris {x['no_baris']}, biaya {b_x}) tampaknya subtotal "
                    f"buatan lembar kerja: biayanya sama dengan jumlah {len(run)} baris '{induk}' tepat "
                    f"di atasnya ({b_run}). Baris ini tidak dihitung supaya biayanya tidak terjumlah dua "
                    "kali. Bila itu kampanye sungguhan, mohon ganti namanya di file lalu jalankan ulang.")
            else:
                alt_total.append((len(peringatan), x["biaya"], True))
                peringatan.append(
                    f"Nama baris '{x['nama_asli']}' (biaya {b_x}) mirip subtotal dari '{induk}', tetapi "
                    f"angkanya tidak sama dengan jumlah baris '{induk}' di atasnya ({b_run}), jadi TETAP "
                    "dihitung sebagai kampanye. Bila itu sebenarnya subtotal, mohon hapus baris itu dari "
                    "file lalu jalankan ulang.")
        elif (_norm_nama(x["nama_asli"]) == _norm_nama(induk) and len(run) >= 2
              and (not kolom_tgl_semua or (not x["tgl_ok"] and not x["tgl_rusak"]
                                           and all(g["tgl_ok"] or g["tgl_rusak"] for g in run)))
              and _cocok_jumlah(x, run, True)):
            # Nama sama persis: hanya bila biaya, tayangan & klik semuanya cocok DAN baris ini tidak
            # bertanggal sementara baris-baris di atasnya bertanggal (baris harian asli tidak kena).
            x["n3"] = True
            peringatan.append(
                f"Baris '{x['nama_asli']}' (baris {x['no_baris']}, biaya {b_x}) tampaknya subtotal: "
                f"{'tanpa tanggal, dan ' if kolom_tgl_semua else ''}biaya, tayangan & kliknya sama "
                f"dengan jumlah {len(run)} baris '{induk}' tepat di atasnya ({b_run}). Baris ini tidak "
                "dihitung supaya biayanya tidak terjumlah dua kali. Bila itu data sungguhan, mohon "
                "beri tahu agar dihitung ulang.")
    for x in [y for y in rekaman if y["n3"]]:
        baris_total.append(x["nama_asli"])
        rekaman.remove(x)

    # --- v1.0.6: baris total kampanye TANPA label (kolom grup iklan/iklan kosong) di file bertingkat ---
    # Bila kampanye yang sama punya baris rincian bernama, baris berkolom-rinci-kosong itu bisa berupa total
    # kampanye (mis. "Search Brand,,700000,..." di bawah dua grup iklan). Biaya, tayangan & klik ≈ (±2%)
    # jumlah baris rincian -> dibuang dengan ⚠️ (tidak dihitung dua kali); selain itu tetap dihitung + ⚠️.
    if kolom_induk:
        for x in list(rekaman):
            if x["nama_asli"] or x["kandidat_subtotal"] or not any(x["induk"]):
                continue
            saudara = [y for y in rekaman if y is not x and y["nama_asli"] and y["induk"] == x["induk"]]
            if not saudara:
                continue
            b_x = fmt_rp(x["biaya"] * kurs)
            b_s = fmt_rp(sum((g["biaya"] for g in saudara), NOL) * kurs)
            kamp = x["induk"][-1] or x["induk"][0]
            if _cocok_jumlah(x, saudara, True):
                x["n3"] = True
                peringatan.append(
                    f"Baris kampanye '{kamp}' tanpa {level_rincian} (baris {x['no_baris']}, biaya {b_x}) "
                    f"tampaknya total kampanye: biaya, tayangan & kliknya sama dengan jumlah {len(saudara)} "
                    f"baris {level_rincian} kampanye itu ({b_s}). Baris ini tidak dihitung supaya biayanya "
                    "tidak terjumlah dua kali. Bila itu data sungguhan (mis. Performance Max), mohon "
                    "beri tahu agar dihitung ulang.")
            else:
                peringatan.append(
                    f"Baris kampanye '{kamp}' tanpa {level_rincian} (baris {x['no_baris']}, biaya {b_x}) "
                    f"tetap dihitung, tetapi kampanye itu juga punya {len(saudara)} baris {level_rincian} "
                    f"bernama (jumlah {b_s}). Mohon cek: bila baris ini sebenarnya total kampanye, hapus "
                    "dari file lalu jalankan ulang agar tidak terjumlah dua kali.")
        for x in [y for y in rekaman if y["n3"] and not y["nama_asli"]]:
            baris_total.append(f"total {x['induk'][-1] or x['induk'][0]}")
            rekaman.remove(x)

    # --- M3: kolom nama kosong + label mirip total di kolom lain (mis. "Subtotal Kamp A") ---
    # Dibuang HANYA bila biaya, tayangan & klik ≈ (±2%) jumlah beberapa baris data tepat di atas
    # ATAU tepat di bawahnya (pola subtotal). Selain itu tetap dihitung + ⚠️.
    subtotal_dibuang = []
    for i, x in enumerate(rekaman):
        if not x["kandidat_subtotal"]:
            continue
        cocok = None
        if x["biaya"] > 0:
            for arah, kata_arah in ((-1, "di atasnya"), (1, "di bawahnya")):
                acc = {k: NOL for k in metrik_silang}
                j, n = i + arah, 0
                while 0 <= j < len(rekaman) and not rekaman[j]["kandidat_subtotal"]:
                    for k in metrik_silang:
                        acc[k] += rekaman[j][k]
                    n += 1
                    if all(_dekat(x[k], acc[k]) for k in metrik_silang):
                        cocok = (n, kata_arah, acc["biaya"])
                        break
                    if acc["biaya"] > x["biaya"] * (1 + TOLERANSI_TOTAL):
                        break
                    j += arah
                if cocok:
                    break
        if cocok:
            n, kata_arah, b_grup = cocok
            subtotal_dibuang.append(x)
            baris_total.append(x["kandidat_subtotal"])
            peringatan.append(
                f"Baris {x['no_baris']} (kolom {level_rincian or 'kampanye'} kosong, berlabel "
                f"'{x['kandidat_subtotal']}', biaya {fmt_rp(x['biaya'] * kurs)}) sama dengan jumlah {n} baris "
                f"tepat {kata_arah} (biaya {fmt_rp(b_grup * kurs)}), jadi dianggap SUBTOTAL dan tidak "
                "dihitung. Bila itu iklan sungguhan, beri nama di file lalu jalankan ulang.")
        else:
            alt_total.append((len(peringatan), x["biaya"], True))
            peringatan.append(
                f"Baris {x['no_baris']} tidak ada nama di kolom {level_rincian or 'kampanye'}, tapi kolom lain "
                f"berbunyi '{x['kandidat_subtotal']}' (mirip label total/ringkasan). Angkanya tidak cocok "
                "dengan jumlah baris di sekitarnya, jadi baris ini TETAP dihitung sebagai kampanye biasa "
                f"(biaya {fmt_rp(x['biaya'] * kurs)}) - kalau ini sebenarnya baris subtotal, hapus baris itu "
                "dari file lalu jalankan ulang, atau beri nama yang jelas.")
    for x in subtotal_dibuang:
        rekaman.remove(x)

    # --- N2: pengaman silang angka baris total ---
    # Hanya baris berbiaya TERBESAR yang mungkin = jumlah semua baris lain (biaya >= 0).

    if len(rekaman) >= 3:
        jml = {k: sum((x[k] for x in rekaman), NOL) for k in ("biaya", "tayangan", "klik")}
        x = max(rekaman, key=lambda y: y["biaya"])
        lain = {k: jml[k] - x[k] for k in jml}
        lain_positif = sum(1 for y in rekaman if y is not x and y["biaya"] > 0)
        if x["biaya"] > 0 and lain_positif >= 2 and lain["biaya"] > 0:
            b_x, b_lain = fmt_rp(x["biaya"] * kurs), fmt_rp(lain["biaya"] * kurs)
            if all(x[k] == lain[k] for k in jml):
                alasan_total = f"angkanya ({b_x}) persis sama dengan jumlah semua baris lain"
            elif all(_dekat(x[k], lain[k]) for k in jml):
                alasan_total = (f"punya biaya ({b_x}), tayangan, dan klik yang hampir sama (selisih ≤ 2%) "
                                f"dengan jumlah semua baris lain (biaya {b_lain})")
            else:
                alasan_total = None
            if alasan_total:
                rekaman.remove(x)
                baris_total.append(x["nama"])
                peringatan.append(
                    f"Baris '{x['nama']}' {alasan_total}, jadi dianggap baris TOTAL dan tidak dihitung "
                    "lagi. Bila itu memang iklan sungguhan, beri tahu agar dihitung ulang.")
            elif _dekat(x["biaya"], lain["biaya"], TOLERANSI_CURIGA):   # M2: ±5%, hanya ⚠️
                berlabel = (f" (berlabel '{x['label_lemah']}')"
                            if x["label_lemah"] and x["label_lemah"] != x["nama"] else "")
                peringatan.append(
                    f"Biaya baris '{x['nama']}'{berlabel} ({b_x}) hampir sama dengan jumlah semua baris lain "
                    f"({b_lain}). Baris ini tetap dihitung. Mohon dicek sebentar: kalau ternyata itu baris "
                    "total/ringkasan, biayanya mungkin terjumlah dua kali, dan total belanja minggu ini "
                    f"seharusnya {b_lain}, bukan {fmt_rp((x['biaya'] + lain['biaya']) * kurs)}. Bila benar, "
                    "hapus baris itu dari file lalu jalankan ulang. Bila itu kampanye sungguhan, abaikan "
                    "catatan ini.")

    # v1.0.3 (M1): SETIAP baris berlabel total "kuat"/"sedang" yang dibuang selalu dapat ⚠️
    # menyebut nama & biayanya, supaya pengguna bisa cek sendiri - sebelumnya hanya label
    # "sedang" yang angkanya tidak cocok yang diberi tahu; label "kuat" dibuang tanpa ⚠️ sama
    # sekali walau biayanya jauh dari jumlah baris lain.
    if baris_total_info:
        jml_biaya = sum((x["biaya"] for x in rekaman), NOL) if rekaman else NOL
        for lbl, b in baris_total_info:
            if b is None:
                peringatan.append(
                    f"Baris '{lbl}' dianggap baris total/ringkasan dan tidak dihitung sebagai kampanye "
                    "(biayanya tidak terbaca sebagai angka, jadi tidak bisa dicek silang). Cek dulu file "
                    "asli kalau itu ternyata kampanye sungguhan.")
            elif jml_biaya > 0 and not _dekat(b, jml_biaya):
                alt_total.append((len(peringatan), b, False))
                peringatan.append(
                    f"Baris '{lbl}' dianggap baris total/ringkasan dan tidak dihitung, tetapi biayanya "
                    f"({fmt_rp(b * kurs)}) tidak sama dengan jumlah baris lain ({fmt_rp(jml_biaya * kurs)}). "
                    "Bila itu kampanye sungguhan, ganti namanya di file lalu jalankan ulang.")
            else:
                peringatan.append(
                    f"Baris '{lbl}' dianggap baris total/ringkasan (biaya {fmt_rp(b * kurs)}) dan tidak "
                    "dihitung sebagai kampanye. Cek dulu file asli kalau itu ternyata kampanye sungguhan.")

    tanggal_terlihat = [t for x in rekaman for t in x["tgl_ok"]]
    tanggal_tak_terbaca = [t for x in rekaman for t in x["tgl_rusak"]]

    if not rekaman:
        alasan = []
        if baris_total:
            alasan.append(f"{len(baris_total)} baris total")
        if biaya_rusak:
            alasan.append(f"{len(biaya_rusak)} baris biayanya tidak terbaca (mis. '{biaya_rusak[0][1]}')")
        if baris_tanpa_angka:
            alasan.append(f"{baris_tanpa_angka} baris tanpa angka")
        raise ValueError("Tidak ada baris data yang valid di file ini"
                          + (" (" + "; ".join(alasan) + ")" if alasan else "") +
                          ". Cek ulang hasil ekspor.")

    # --- agregasi per nama kampanye ---
    per_kampanye = defaultdict(lambda: {"biaya": NOL, "tayangan": NOL, "klik": NOL,
                                        "hasil": NOL, "nilai_hasil": NOL})
    tujuan_per_kampanye = {}
    for x in rekaman:
        if x.get("tujuan_lain") and x["nama"] not in tujuan_per_kampanye:
            tujuan_per_kampanye[x["nama"]] = x["tujuan_lain"]
        k = per_kampanye[x["nama"]]
        k["biaya"] += x["biaya"] * kurs
        k["nilai_hasil"] += x["nilai_hasil"] * kurs
        for m in ("tayangan", "klik", "hasil"):
            k[m] += x[m]

    ada_nilai = bool(kolom.get("nilai_hasil"))
    total = {"biaya": NOL, "tayangan": NOL, "klik": NOL, "hasil": NOL, "nilai_hasil": NOL}
    daftar_kampanye = []
    for nama, v in per_kampanye.items():
        for kk in total:
            total[kk] += v[kk]
        daftar_kampanye.append({"nama": nama, **metrik(v, ada_nilai),
                                "tujuan_lain": tujuan_per_kampanye.get(nama)})
    t = metrik(total, ada_nilai)
    for idx, b_baris, dihitung in alt_total:                     # v1.0.5 (P-4)
        b_rp = b_baris * kurs
        if dihitung:
            peringatan[idx] += (f" Total belanja file ini sekarang {fmt_rp(total['biaya'])} (baris itu ikut "
                                f"dihitung); bila baris itu ternyata subtotal, totalnya menjadi "
                                f"{fmt_rp(total['biaya'] - b_rp)}.")
        else:
            peringatan[idx] += (f" Total belanja file ini sekarang {fmt_rp(total['biaya'])} (baris itu tidak "
                                f"dihitung); bila baris itu ternyata kampanye sungguhan, totalnya menjadi "
                                f"{fmt_rp(total['biaya'] + b_rp)}.")

    # --- periode ---
    tgl_judul = []
    for b in info["baris_judul"]:
        tgl_judul.extend(tanggal_dalam_teks(b))
    awal, akhir = _rentang(tanggal_terlihat)
    sumber_periode = "kolom tanggal"
    if not awal and tgl_judul:
        awal, akhir = _rentang(tgl_judul)
        sumber_periode = "baris judul file"
    periode = {"awal": awal.isoformat() if awal else None, "akhir": akhir.isoformat() if akhir else None,
               "label": args.periode or "(tidak ada kolom tanggal di file; sebutkan periodenya)"}
    if awal and not args.periode:
        periode["label"] = f"{awal.isoformat()} s.d. {akhir.isoformat()}"
        if sumber_periode != "kolom tanggal":
            catatan.append(f"Periode dibaca dari {sumber_periode}.")
    if awal:
        hari = (akhir - awal).days + 1
        periode["jumlah_hari"] = hari
        if hari > 7:
            peringatan.append(f"Data di file mencakup {hari} hari ({awal.isoformat()} s.d. "
                              f"{akhir.isoformat()}), bukan satu minggu. Angka di laporan ini untuk "
                              "seluruh rentang itu. Ekspor ulang 7 hari saja bila perlu laporan mingguan.")
    if tanggal_tak_terbaca:
        contoh = ", ".join(f"'{x}'" for x in list(dict.fromkeys(tanggal_tak_terbaca))[:3])
        peringatan.append(f"{len(tanggal_tak_terbaca)} isi kolom tanggal tidak terbaca ({contoh}) dan "
                          "tidak dipakai untuk menentukan periode (angkanya tetap dihitung).")

    # --- catatan/peringatan sel ---
    label_peran = {"biaya": kolom["biaya"], "tayangan": kolom["tayangan"], "klik": kolom["klik"],
                   "hasil": kolom["hasil"], "nilai_hasil": kolom.get("nilai_hasil")}
    nama_hasil = args.nama_hasil or (kolom["hasil"] if kolom.get("hasil") else "hasil")
    for peran in ("hasil", "klik", "tayangan", "nilai_hasil", "biaya"):
        rec_kosong = [x for x in kosong_per_kolom.get(peran, []) if any(x is y for y in rekaman)]
        if not rec_kosong:
            continue
        nama_kosong = list(dict.fromkeys(x["nama"] for x in rec_kosong))
        # biaya BARIS yang selnya kosong (bukan biaya seluruh kampanye/induknya) — N1
        biaya_mereka = sum((x["biaya"] for x in rec_kosong), NOL) * kurs
        teks = (f"Sel '{label_peran[peran]}' kosong di {len(rec_kosong)} baris "
                f"({daftar_nama(nama_kosong)}) dan dihitung 0")
        if peran == "hasil":
            teks += (f"; biayanya ({fmt_rp(biaya_mereka)}) tetap masuk total. Ads Manager biasanya "
                     "mengosongkan sel ini bila iklan belum menghasilkan apa pun")
        catatan.append(teks + ".")
    if biaya_rusak:
        peringatan.append(
            f"{len(biaya_rusak)} baris TIDAK dihitung karena biayanya tidak terbaca: "
            + "; ".join(f"{n} ('{i}')" for n, i in biaya_rusak[:4])
            + ". Total belanja di laporan ini bisa LEBIH KECIL dari sebenarnya. Perbaiki sel itu lalu jalankan ulang.")
    if rusak_metrik:
        peringatan.append(
            "Isi sel berikut bukan angka dan dihitung 0: "
            + "; ".join(f"{n} kolom '{k}' ('{i}')" for n, k, i in rusak_metrik[:4])
            + (f", dan {len(rusak_metrik) - 4} lainnya" if len(rusak_metrik) > 4 else "") + ".")
    if biaya_negatif:
        peringatan.append("Ada biaya bernilai negatif (mis. kredit/refund): "
                          + "; ".join(f"{n} {fmt_rp(b * kurs)}" for n, b in biaya_negatif[:4])
                          + ". Ikut dihitung apa adanya; pastikan memang benar.")
    tanpa_nama = sum(1 for x in rekaman if x["nama"].startswith("(tanpa nama"))
    if tanpa_nama:
        catatan.append(f"{tanpa_nama} baris tidak punya nama kampanye/iklan dan diberi label nomor baris.")
    if baris_tanpa_angka:
        catatan.append(f"{baris_tanpa_angka} baris tanpa angka dilewati.")

    # --- cek kewajaran (mencegah kolom/mata uang salah pilih tanpa ketahuan) ---
    if t["cpc"] is not None and t["klik"] > 0 and t["cpc"] < 10:
        peringatan.append(f"CPC {fmt_rp(t['cpc'])} tidak wajar untuk Rupiah. Kemungkinan kolom biaya "
                          f"salah ('{kolom['biaya']}') atau angkanya mata uang asing. Periksa sebelum dikirim.")
    if t["roas"] is not None and t["roas"] > 50:
        peringatan.append(f"ROAS {fmt_x(t['roas'])} tidak wajar. Kemungkinan kolom biaya ('{kolom['biaya']}') "
                          f"atau nilai ('{kolom.get('nilai_hasil')}') salah pilih. Periksa sebelum dikirim.")

    # v1.0.10: kampanye bertujuan lain (Traffic/Awareness/...) TANPA hasil tidak dinilai dari hasil
    tujuan_berbeda = sorted((k for k in daftar_kampanye if k.get("tujuan_lain") and k["hasil"] <= 0
                             and k["biaya"] > 0), key=lambda k: (-k["biaya"], k["nama"]))
    id_beda = {id(k) for k in tujuan_berbeda}
    dinilai = [k for k in daftar_kampanye if id(k) not in id_beda]
    terbaik, terburuk, dijeda = pilih_terbaik_terburuk(dinilai, args.top)
    if dijeda:
        catatan.append(f"{len(dijeda)} kampanye tanpa biaya minggu ini (mis. dijeda) tidak dinilai: "
                       f"{daftar_nama([k['nama'] for k in dijeda])}.")
    saran = susun_saran(dinilai, t, nama_hasil, terbaik)
    if tujuan_berbeda:
        biaya_beda = sum((k["biaya"] for k in tujuan_berbeda), NOL)
        sisa_biaya = t["biaya"] - biaya_beda
        teks_beda = (f"{len(tujuan_berbeda)} kampanye bertujuan lain ({daftar_nama([k['nama'] for k in tujuan_berbeda])}; "
                     f"belanja {fmt_rp(biaya_beda)}) dinilai dari klik/tayangan, bukan {nama_hasil}")
        if t["hasil"] > 0 and sisa_biaya > 0:
            teks_beda += (f". Biaya per {nama_hasil} di atas ikut menghitung belanja itu; khusus kampanye "
                          f"bertujuan {nama_hasil}: {fmt_rp(bagi(sisa_biaya, t['hasil']))}")
        catatan.append(teks_beda + ".")

    kolom_dipakai = dict(kolom)
    kolom_dipakai["mata_uang"] = kolom_uang
    kolom_dipakai["tujuan"] = kolom_tujuan
    return {
        "platform_terdeteksi": platform_terdeteksi,
        "mata_uang": mata_uang_final,
        "catatan_mata_uang": catatan_mata_uang,
        "periode": periode,
        "sidik_file": sidik_file(path),
        "jumlah_kampanye": len(daftar_kampanye),
        "jumlah_baris_data_valid": len(rekaman),
        "level_rincian": level_rincian or "kampanye",
        "kolom_induk": kolom_induk,
        "baris_dilewati_baris_total": len(baris_total),
        "label_baris_total": baris_total,
        "baris_dilewati_lainnya": {"biaya_tidak_terbaca": len(biaya_rusak),
                                   "tanpa_angka": baris_tanpa_angka},
        "kolom_dipakai": kolom_dipakai,
        "ada_nilai_hasil": ada_nilai,
        "nama_hasil": nama_hasil,
        "total": t,
        "per_kampanye": sorted(daftar_kampanye, key=lambda k: -k["biaya"]),
        "tiga_terbaik": terbaik,
        "tiga_terburuk": terburuk,
        "tujuan_berbeda": tujuan_berbeda,
        "saran": saran,
        "catatan": catatan,
        "peringatan": peringatan,
    }


def metrik(v, ada_nilai):
    cpm = bagi(v["biaya"], v["tayangan"])
    ctr = bagi(v["klik"], v["tayangan"])
    return {
        "biaya": v["biaya"], "tayangan": v["tayangan"], "klik": v["klik"], "hasil": v["hasil"],
        "nilai_hasil": v["nilai_hasil"] if ada_nilai else None,
        "cpc": bagi(v["biaya"], v["klik"]),
        "cpm": cpm * SERIBU if cpm is not None else None,
        "ctr_persen": ctr * SERATUS if ctr is not None else None,
        "biaya_per_hasil": bagi(v["biaya"], v["hasil"]),
        "roas": bagi(v["nilai_hasil"], v["biaya"]) if ada_nilai else None,
    }


def pilih_terbaik_terburuk(daftar, top):
    """Terbaik & perlu perhatian TANPA irisan; kampanye berbiaya 0 (dijeda) tidak dinilai."""
    dijeda = [k for k in daftar if k["biaya"] <= 0]
    aktif = [k for k in daftar if k["biaya"] > 0]
    ada_hasil = sorted((k for k in aktif if k["hasil"] > 0), key=lambda k: (k["biaya_per_hasil"], k["nama"]))
    tanpa_hasil = sorted((k for k in aktif if k["hasil"] <= 0), key=lambda k: (-k["biaya"], k["nama"]))
    n_terbaik = top if len(ada_hasil) >= 2 * top else min(top, (len(ada_hasil) + 1) // 2)
    terbaik = ada_hasil[:n_terbaik]
    sisa = [k for k in reversed(ada_hasil) if k not in terbaik]
    terburuk = (tanpa_hasil + sisa)[:top]
    return terbaik, terburuk, dijeda


AMBANG_SAMPEL_KECIL = 5


def susun_saran(daftar, t, nama_hasil, terbaik):
    saran = []
    rata = t["biaya_per_hasil"]           # = total biaya ÷ total hasil (angka yang sama di atas)
    aktif = [k for k in daftar if k["biaya"] > 0]
    for k in sorted((k for k in aktif if k["hasil"] <= 0), key=lambda x: -x["biaya"]):
        if k["biaya"] >= 50000:
            saran.append(f"Tinjau/hentikan iklan '{k['nama']}': sudah menghabiskan {fmt_rp(k['biaya'])} "
                         f"tanpa {nama_hasil} sama sekali.")
    if rata:
        nama_terbaik = {k["nama"] for k in terbaik}
        ada_hasil = [k for k in aktif if k["hasil"] > 0]
        for k in sorted(ada_hasil, key=lambda x: -x["biaya_per_hasil"]):
            if k["nama"] in nama_terbaik:
                continue
            if k["biaya_per_hasil"] > 2 * rata:
                kalimat = (f"Tinjau/matikan iklan '{k['nama']}': biaya per {nama_hasil} "
                           f"{fmt_rp(k['biaya_per_hasil'])}, {fmt_x(k['biaya_per_hasil'] / rata)} rata-rata "
                           f"semua iklan ({fmt_rp(rata)}).")
                if k.get("tujuan_lain"):
                    kalimat = (f"Iklan '{k['nama']}' bertujuan {k['tujuan_lain']}, jadi wajar lebih mahal per "
                               f"{nama_hasil} ({fmt_rp(k['biaya_per_hasil'])}, {fmt_x(k['biaya_per_hasil'] / rata)} "
                               f"rata-rata {fmt_rp(rata)}); nilai juga dari CPC {fmt_rp(k['cpc'])} & CTR "
                               f"{fmt_persen(k['ctr_persen'])} sebelum memutuskan.")
                if k["hasil"] < AMBANG_SAMPEL_KECIL:
                    kalimat += (f" Baru {fmt_angka(k['hasil'])} {nama_hasil}, sampel kecil: pantau 1 minggu "
                                "lagi sebelum memutuskan.")
                saran.append(kalimat)
        if len(ada_hasil) > 1:
            k = min(ada_hasil, key=lambda x: x["biaya_per_hasil"])
            if k["biaya_per_hasil"] <= rata / 2:
                kalimat = (f"Pertimbangkan naikkan anggaran iklan '{k['nama']}': biaya per {nama_hasil} "
                           f"{fmt_rp(k['biaya_per_hasil'])}, jauh di bawah rata-rata semua iklan ({fmt_rp(rata)}).")
                if k["hasil"] < AMBANG_SAMPEL_KECIL:
                    kalimat += f" Baru {fmt_angka(k['hasil'])} {nama_hasil}, sampel kecil: naikkan bertahap."
                saran.append(kalimat)
    if t["roas"] is not None and t["roas"] < 1:
        saran.append(f"ROAS keseluruhan {fmt_x(t['roas'])} (di bawah 1x): biaya iklan minggu ini "
                     f"lebih besar dari nilai {nama_hasil}/penjualan yang tercatat dari iklan.")
    if not saran:
        saran.append("Belum ada kampanye yang menonjol biaya-per-hasilnya minggu ini; performa relatif merata.")
    return saran[:5]


# --------------------------------------------------------------------------------------
# Perbandingan minggu ini vs minggu lalu
# --------------------------------------------------------------------------------------

def bandingkan_persen(sekarang, lalu, rupiah=True):
    """Persen perubahan dengan Decimal; dibulatkan 1 desimal, 0,05 menjauhi nol."""
    s, l = D(sekarang), D(lalu)
    nol = "Rp 0" if rupiah else "0"
    if l == 0:
        if s == 0:
            return None, f"sama-sama {nol}"
        return None, f"naik dari {nol} (persen tidak dihitung)"
    p = bulat1((s - l) / l * SERATUS)
    if s == l:
        return p, "sama dengan"
    if p == 0:
        return p, "hampir sama dengan"
    arah = "naik" if p > 0 else "turun"
    return p, f"{arah} {fmt_persen(abs(p))} dari"


def bandingkan(hasil_sekarang, hasil_lalu):
    keluar = {}
    for metrik_, label, rupiah in [("biaya", "Biaya iklan", True), ("hasil", "Hasil", False),
                                   ("biaya_per_hasil", "Biaya per hasil", True), ("klik", "Klik", False),
                                   ("tayangan", "Tayangan", False)]:
        s = hasil_sekarang["total"].get(metrik_)
        l = hasil_lalu["total"].get(metrik_)
        if s is None or l is None:
            keluar[metrik_] = {"sekarang": s, "lalu": l, "persen": None, "label": label,
                               "keterangan": "tidak dapat dibandingkan (- pada salah satu minggu)"}
            continue
        p, ket = bandingkan_persen(s, l, rupiah)
        keluar[metrik_] = {"sekarang": s, "lalu": l, "persen": p, "keterangan": ket, "label": label}
    return keluar


# --------------------------------------------------------------------------------------
# Susun teks laporan siap kirim
# --------------------------------------------------------------------------------------

def _blok_peringatan(L, peringatan):
    if peringatan:
        L.append("")
        L.append("⚠️ PERLU DICEK SEBELUM DIPAKAI:")
        for p in peringatan:
            L.append(f"- {p}")


def susun_teks(h, pembanding=None, omzet=None):
    L = [f"LAPORAN IKLAN MINGGUAN — {h['platform_terdeteksi']}", f"Periode: {h['periode']['label']}"]
    kd = h["kolom_dipakai"]
    # v1.0.10: "Kolom dibaca" di bagian atas (bukan ekor Catatan) supaya selalu ikut terkirim.
    L.append("Kolom dibaca: " + ", ".join(
        f"{lbl}='{kd[p]}'" for p, lbl in (("nama", "nama"), ("biaya", "biaya"), ("tayangan", "tayangan"),
                                           ("klik", "klik"), ("hasil", "hasil"), ("nilai_hasil", "nilai"),
                                           ("tujuan", "tujuan"))
        if kd.get(p)) + ".")
    _blok_peringatan(L, h.get("peringatan", []))
    L.append("")
    t = h["total"]
    nh = h["nama_hasil"]
    L.append(f"Total belanja iklan: {fmt_rp(t['biaya'])}")
    L.append(f"Tayangan: {fmt_angka(t['tayangan'])} | Klik: {fmt_angka(t['klik'])} "
             f"| {kapital(nh)}: {fmt_angka(t['hasil'])}")
    L.append(f"CPC: {fmt_rp(t['cpc'])} | CPM: {fmt_rp(t['cpm'])} | CTR: {fmt_persen(t['ctr_persen'])}")
    L.append(f"Biaya per {nh}: {fmt_rp(t['biaya_per_hasil'])}")
    if t.get("roas") is not None:
        L.append(f"ROAS: {fmt_x(t['roas'])}")
    if omzet:
        L.append(f"Biaya iklan vs omzet: {fmt_persen(omzet['biaya_sebagai_persen_omzet'])} dari omzet "
                 f"{fmt_rp(omzet['omzet'])}")

    if pembanding:
        L.append("")
        L.append("VS MINGGU LALU")
        for m in ("biaya", "hasil", "biaya_per_hasil"):
            b = pembanding[m]
            rupiah = m != "hasil"
            f = fmt_rp if rupiah else fmt_angka
            if b["persen"] is None:
                L.append(f"{b['label']}: {f(b['sekarang'])} ({b['keterangan']})")
            else:
                L.append(f"{b['label']}: {f(b['sekarang'])} ({b['keterangan']} minggu lalu {f(b['lalu'])})")

    if h["tiga_terbaik"]:
        L.append("")
        L.append(f"TERBAIK (biaya per {nh} termurah)")
        for i, k in enumerate(h["tiga_terbaik"], 1):
            L.append(f"{i}. {k['nama']}: {fmt_rp(k['biaya_per_hasil'])}/{nh} "
                     f"({fmt_angka(k['hasil'])} {nh}, {fmt_rp(k['biaya'])})")
    if h["tiga_terburuk"]:
        L.append("")
        L.append("PERLU PERHATIAN (tanpa hasil / biaya per hasil termahal)")
        for i, k in enumerate(h["tiga_terburuk"], 1):
            if k["hasil"] <= 0:
                L.append(f"{i}. {k['nama']}: {fmt_rp(k['biaya'])} terpakai, 0 {nh}")
            else:
                L.append(f"{i}. {k['nama']}: {fmt_rp(k['biaya_per_hasil'])}/{nh} "
                         f"({fmt_angka(k['hasil'])} {nh}, {fmt_rp(k['biaya'])})")

    if h.get("tujuan_berbeda"):
        L.append("")
        L.append(f"TUJUAN BERBEDA (Traffic/Awareness dll. — tidak dinilai dari {nh}, jangan dimatikan hanya karena 0 {nh})")
        for i, k in enumerate(h["tujuan_berbeda"], 1):
            L.append(f"{i}. {k['nama']} [{k['tujuan_lain']}]: {fmt_rp(k['biaya'])} | Klik {fmt_angka(k['klik'])} "
                     f"| CPC {fmt_rp(k['cpc'])} | CTR {fmt_persen(k['ctr_persen'])} | CPM {fmt_rp(k['cpm'])}")
        L.append(f"   Bandingkan dengan CPC rata-rata akun {fmt_rp(t['cpc'])}. Matikan hanya bila tujuan itu "
                 "memang tidak dibutuhkan; untuk mendatangkan pesan, pakai kampanye bertujuan pesan/konversi.")

    L.append("")
    L.append("SARAN")
    for i, s in enumerate(h["saran"], 1):
        L.append(f"{i}. {s}")
    L.append("(Saran berdasarkan angka minggu ini, bukan jaminan hasil. Keputusan tetap di tangan Anda.)")

    catatan = list(h.get("catatan_mata_uang", [])) + list(h.get("catatan", []))
    if h["baris_dilewati_baris_total"]:
        label = ", ".join(f"'{x}'" for x in h.get("label_baris_total", [])[:3])
        catatan.append(f"{h['baris_dilewati_baris_total']} baris total/ringkasan ({label}) diabaikan agar "
                       "tidak dihitung dua kali.")
    if omzet:
        catatan.append(omzet["catatan"])
    L.append("")
    L.append("Catatan:")
    for c in catatan:
        L.append(f"- {c}")
    return "\n".join(L)


# --------------------------------------------------------------------------------------
# Mode gabung (lintas platform)
# --------------------------------------------------------------------------------------

KUNCI_JSON_WAJIB = ("platform_terdeteksi", "total", "nama_hasil", "saran")


def _ke_decimal(o):
    if isinstance(o, dict):
        return {k: _ke_decimal(v) for k, v in o.items()}
    if isinstance(o, list):
        return [_ke_decimal(v) for v in o]
    if isinstance(o, bool) or o is None:
        return o
    if isinstance(o, int):
        return Decimal(o)
    return o


def gabung(daftar_json, omzet=None):
    peringatan = []
    sidik = [h.get("sidik_file") for h in daftar_json if h.get("sidik_file")]
    if len(sidik) != len(set(sidik)):
        raise ValueError("File ekspor yang sama dimasukkan lebih dari sekali ke 'gabung' (biaya akan "
                         "terhitung dua kali). Pakai satu JSON per platform.")
    total = {"biaya": NOL, "tayangan": NOL, "klik": NOL}
    per_platform = []
    catatan_mu = []
    for h in daftar_json:
        t = h["total"]
        for k in total:
            total[k] += D(t.get(k) or 0)
        per_platform.append({"platform": h["platform_terdeteksi"], "biaya": D(t["biaya"]),
                             "hasil": D(t["hasil"]), "biaya_per_hasil": t.get("biaya_per_hasil"),
                             "nama_hasil": h["nama_hasil"],
                             "ada_nilai_hasil": bool(h.get("ada_nilai_hasil", t.get("nilai_hasil") is not None)),
                             "nilai_hasil": D(t.get("nilai_hasil") or 0), "roas": t.get("roas")})
        for c in h.get("catatan_mata_uang", []):
            if not c.startswith("Tidak ada label"):
                catatan_mu.append(f"[{h['platform_terdeteksi']}] {c}")
        peringatan.extend(f"[{h['platform_terdeteksi']}] {p}" for p in h.get("peringatan", []))

    biaya_total = total["biaya"]
    for p in per_platform:
        p["persen_biaya"] = bulat1(p["biaya"] / biaya_total * SERATUS) if biaya_total else None

    platform_unik = {p["platform"] for p in per_platform}
    nama_unik = {p["nama_hasil"].strip().lower() for p in per_platform}
    hasil_total = None
    bph = None
    nama_hasil = per_platform[0]["nama_hasil"] if per_platform else "hasil"
    if len(nama_unik) > 1:
        peringatan.append(
            "Jenis hasil tiap platform berbeda (" + ", ".join(sorted({p['nama_hasil'] for p in per_platform}))
            + "), jadi jumlah hasil dan biaya per hasil TIDAK digabung. Lihat angka per platform.")
    else:
        hasil_total = sum((p["hasil"] for p in per_platform), NOL)
        bph = bagi(biaya_total, hasil_total)
        if len(platform_unik) > 1:
            peringatan.append(
                f"'{nama_hasil}' dihitung dengan aturan masing-masing platform (atribusi berbeda), "
                "jadi total dan biaya per hasil gabungan hanya perkiraan kasar. Angka per platform lebih akurat.")

    punya_nilai = [p for p in per_platform if p["ada_nilai_hasil"]]
    roas = None
    roas_label = None
    if punya_nilai:
        b = sum((p["biaya"] for p in punya_nilai), NOL)
        roas = bagi(sum((p["nilai_hasil"] for p in punya_nilai), NOL), b)
        if len(punya_nilai) < len(per_platform):
            roas_label = ("hanya " + ", ".join(p["platform"] for p in punya_nilai)
                          + "; platform lain tidak punya data nilai penjualan")

    periode = {(h.get("periode") or {}).get("label") for h in daftar_json}
    periode = {x for x in periode if x and not x.startswith("(")}
    if len(periode) > 1:
        peringatan.append("Periode file berbeda-beda: " + "; ".join(sorted(periode)) + ".")

    # saran bergiliran per platform supaya platform terakhir tidak terpotong
    antrian = [[f"[{h['platform_terdeteksi']}] {s}" for s in h["saran"]
                if not s.startswith("Belum ada kampanye")] for h in daftar_json]
    saran = []
    while any(antrian) and len(saran) < 6:
        for a in antrian:
            if a and len(saran) < 6:
                saran.append(a.pop(0))

    cpm = bagi(total["biaya"], total["tayangan"])
    ctr = bagi(total["klik"], total["tayangan"])
    return {
        "platform_terdeteksi": " + ".join(sorted(platform_unik)),
        "mata_uang": "IDR",
        "total": {**total, "hasil": hasil_total, "nilai_hasil": None,
                  "cpc": bagi(total["biaya"], total["klik"]),
                  "cpm": cpm * SERIBU if cpm is not None else None,
                  "ctr_persen": ctr * SERATUS if ctr is not None else None,
                  "biaya_per_hasil": bph, "roas": roas, "roas_keterangan": roas_label},
        "per_platform": per_platform,
        "nama_hasil": nama_hasil if hasil_total is not None else None,
        "saran": saran or ["Belum ada kampanye yang menonjol biaya-per-hasilnya minggu ini."],
        "catatan_mata_uang": catatan_mu,
        "peringatan": list(dict.fromkeys(peringatan)),
    }


def susun_teks_gabung(g, omzet=None):
    L = ["LAPORAN IKLAN MINGGUAN — GABUNGAN SEMUA PLATFORM"]
    _blok_peringatan(L, g["peringatan"])
    L.append("")
    t = g["total"]
    L.append(f"Total belanja iklan (semua platform): {fmt_rp(t['biaya'])}")
    for p in g["per_platform"]:
        baris = (f"- {p['platform']}: {fmt_rp(p['biaya'])} ({fmt_persen(p['persen_biaya'])} dari total), "
                 f"{fmt_angka(p['hasil'])} {p['nama_hasil']}, biaya per {p['nama_hasil']}: "
                 f"{fmt_rp(p['biaya_per_hasil'])}")
        if p.get("roas") is not None:
            baris += f", ROAS {fmt_x(p['roas'])}"
        L.append(baris)
    L.append(f"Tayangan: {fmt_angka(t['tayangan'])} | Klik: {fmt_angka(t['klik'])}")
    L.append(f"CPC: {fmt_rp(t['cpc'])} | CPM: {fmt_rp(t['cpm'])} | CTR: {fmt_persen(t['ctr_persen'])}")
    if t["hasil"] is not None:
        L.append(f"Total {g['nama_hasil']} (perkiraan): {fmt_angka(t['hasil'])} | Biaya per "
                 f"{g['nama_hasil']} (gabungan): {fmt_rp(t['biaya_per_hasil'])}")
    else:
        L.append("Total hasil: tidak dijumlah (jenis hasil tiap platform berbeda)")
    if t.get("roas") is not None:
        L.append(f"ROAS gabungan: {fmt_x(t['roas'])}"
                 + (f" ({t['roas_keterangan']})" if t.get("roas_keterangan") else ""))
    if omzet:
        L.append(f"Biaya iklan vs omzet: {fmt_persen(omzet['biaya_sebagai_persen_omzet'])} dari omzet "
                 f"{fmt_rp(omzet['omzet'])}")
    L.append("")
    L.append("SARAN")
    for i, s in enumerate(g["saran"], 1):
        L.append(f"{i}. {s}")
    L.append("(Saran berdasarkan angka minggu ini, bukan jaminan hasil. Keputusan tetap di tangan Anda.)")
    catatan = list(g.get("catatan_mata_uang", []))
    if omzet:
        catatan.append(omzet["catatan"])
    if catatan:
        L.append("")
        L.append("Catatan:")
        for c in catatan:
            L.append(f"- {c}")
    return "\n".join(L)


# --------------------------------------------------------------------------------------
# Keluaran CSV & omzet
# --------------------------------------------------------------------------------------

def sanitasi_sel_csv(nilai):
    """Cegah formula injection (CSV/Excel): sel diawali '=', '+', '-', '@', tab, CR diberi
    awalan kutip tunggal agar dibaca sebagai teks, bukan dieksekusi sebagai formula."""
    s = str(nilai)
    if s and s[0] in ("=", "+", "-", "@", "\t", "\r"):
        return "'" + s
    return s


def _mentah(x, desimal=None):
    """Angka mesin untuk CSV: tanpa pemisah ribuan, desimal titik (konsisten semua kolom)."""
    if x is None:
        return ""
    x = D(x)
    if desimal is None:
        return str(bulat_rupiah(x))
    q = x.quantize(Decimal(1).scaleb(-desimal), rounding=ROUND_HALF_UP)
    return f"{q:f}"


def _mentah_hitung(x):
    x = D(x)
    return str(int(x)) if x == x.to_integral_value() else f"{x.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):f}"


def tulis_csv_kampanye(path, daftar_kampanye, nama_hasil):
    nh = re.sub(r"[^\w]+", "_", str(nama_hasil)).strip("_") or "hasil"
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow([sanitasi_sel_csv(x) for x in
                    ["nama_kampanye", "biaya_rp", "tayangan", "klik", nh, "nilai_hasil_rp",
                     "cpc_rp", "cpm_rp", "ctr_persen", "biaya_per_" + nh + "_rp", "roas_x"]])
        for k in daftar_kampanye:
            w.writerow([
                sanitasi_sel_csv(k["nama"]), _mentah(k["biaya"]), _mentah_hitung(k["tayangan"]),
                _mentah_hitung(k["klik"]), _mentah_hitung(k["hasil"]),
                _mentah(k["nilai_hasil"]) if k.get("nilai_hasil") is not None else "",
                _mentah(k["cpc"]), _mentah(k["cpm"]), _mentah(k["ctr_persen"], 1),
                _mentah(k["biaya_per_hasil"]), _mentah(k.get("roas"), 1),
            ])


def hitung_omzet(total_biaya, omzet_teks):
    omzet = parse_omzet(omzet_teks)
    if omzet <= 0:
        raise ValueError("--omzet harus lebih besar dari 0.")
    return {"omzet": omzet, "biaya_sebagai_persen_omzet": bulat1(D(total_biaya) / omzet * SERATUS),
            "catatan": ("Biaya iklan diambil dari file ekspor. Tagihan platform ke akun Indonesia bisa "
                        "ditambah PPN (cek invoice/faktur platform), jadi persentase terhadap omzet "
                        "bisa sedikit lebih tinggi.")}


# --------------------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------------------

def baca_kurs(teks):
    if teks is None:
        return None
    nilai = parse_angka(teks)
    if nilai is None or nilai <= 0:
        raise ValueError(f"--kurs '{teks}' harus angka lebih besar dari 0 (nilai 1 mata uang asing "
                         "dalam Rupiah, mis. 16350).")
    return nilai


def buat_parser():
    p = argparse.ArgumentParser(description="Laporan iklan mingguan (Meta/TikTok/Shopee/Google Ads)")
    sub = p.add_subparsers(dest="mode", required=True)

    a = sub.add_parser("analisis", help="Analisis satu file ekspor iklan (satu platform, satu minggu)")
    a.add_argument("file")
    a.add_argument("--sebelumnya", help="File ekspor minggu sebelumnya (platform sama) untuk perbandingan")
    a.add_argument("--platform", help="Label platform manual bila deteksi otomatis meleset/kosong")
    a.add_argument("--kolom-nama")
    a.add_argument("--kolom-biaya")
    a.add_argument("--kolom-tayangan")
    a.add_argument("--kolom-klik")
    a.add_argument("--kolom-hasil")
    a.add_argument("--kolom-nilai-hasil")
    a.add_argument("--nama-hasil", help="Label hasil di laporan, mis. 'pesan WA', 'pembelian', 'leads'")
    a.add_argument("--mata-uang", choices=["IDR"], help="Paksa anggap file ber-mata uang asing sebagai IDR")
    a.add_argument("--kurs", help="Nilai tukar 1 satuan mata uang asing ke Rupiah (> 0)")
    a.add_argument("--kurs-sumber")
    a.add_argument("--kurs-tanggal")
    a.add_argument("--periode", help="Label periode bila file tidak punya kolom tanggal")
    a.add_argument("--omzet", help="Omzet periode ini: 20000000, 'Rp20.000.000', '20 juta', '20jt'")
    a.add_argument("--top", type=int, default=3)
    a.add_argument("--json", action="store_true")
    a.add_argument("--csv-keluaran", help="Simpan rincian per kampanye sebagai file CSV (aman dibuka di Excel)")

    g = sub.add_parser("gabung", help="Gabungkan beberapa hasil --json 'analisis' (lintas platform)")
    g.add_argument("files", nargs="+", help="File JSON hasil 'analisis --json'")
    g.add_argument("--omzet")
    g.add_argument("--json", action="store_true")
    return p


def keluar_error(pesan):
    print(json.dumps({"error": pesan}, ensure_ascii=False), file=sys.stderr)
    sys.exit(2)


def pesan_os(e, path):
    if isinstance(e, FileNotFoundError):
        return f"File '{path}' tidak ditemukan. Periksa nama dan lokasi filenya."
    if isinstance(e, IsADirectoryError):
        return f"'{path}' adalah folder, bukan file."
    if isinstance(e, PermissionError):
        return f"Tidak punya izin membuka '{path}'."
    return f"File '{path}' tidak bisa dibuka ({e.strerror or e})."


def ke_json(o):
    if isinstance(o, Decimal):
        return int(o) if o == o.to_integral_value() else float(o)
    return str(o)


def _sama_path(a, b):
    try:
        return os.path.exists(a) and os.path.exists(b) and os.path.samefile(a, b)
    except OSError:
        return os.path.abspath(a) == os.path.abspath(b)


def jalankan_analisis(args):
    override = {"nama": args.kolom_nama, "biaya": args.kolom_biaya, "tayangan": args.kolom_tayangan,
                "klik": args.kolom_klik, "hasil": args.kolom_hasil, "nilai_hasil": args.kolom_nilai_hasil}
    try:
        args.kurs = baca_kurs(args.kurs)
    except ValueError as e:
        keluar_error(str(e))
    if args.csv_keluaran and any(x and _sama_path(args.csv_keluaran, x) for x in (args.file, args.sebelumnya)):
        keluar_error("--csv-keluaran menunjuk ke file ekspor asli; file itu akan tertimpa. Pakai nama "
                     "file lain, mis. rincian-kampanye.csv.")
    try:
        hasil = analisis_file(args.file, override, args)
    except OSError as e:
        keluar_error(pesan_os(e, args.file))
    except ValueError as e:
        keluar_error(str(e))

    pembanding = None
    if args.sebelumnya:
        try:
            hasil_lalu = analisis_file(args.sebelumnya, override, args)
        except OSError as e:
            keluar_error("Gagal membaca file minggu sebelumnya: " + pesan_os(e, args.sebelumnya))
        except ValueError as e:
            keluar_error(f"Gagal membaca file minggu sebelumnya: {e}")
        pembanding = bandingkan(hasil, hasil_lalu)
        if hasil["sidik_file"] == hasil_lalu["sidik_file"]:
            hasil["peringatan"].append("File minggu lalu SAMA PERSIS dengan file minggu ini, jadi "
                                       "perbandingan tidak bermakna. Kirim ekspor minggu lalu yang benar.")
        elif hasil["periode"]["awal"] and hasil["periode"]["awal"] == hasil_lalu["periode"]["awal"] \
                and hasil["periode"]["akhir"] == hasil_lalu["periode"]["akhir"]:
            hasil["peringatan"].append("File minggu ini dan minggu lalu punya periode yang sama "
                                       f"({hasil['periode']['label']}). Pastikan file minggu lalu benar.")
        if hasil["nama_hasil"] != hasil_lalu["nama_hasil"] or \
                hasil["platform_terdeteksi"] != hasil_lalu["platform_terdeteksi"]:
            hasil["peringatan"].append(
                f"File minggu ini ('{hasil['platform_terdeteksi']}', hasil='{hasil['nama_hasil']}') dan "
                f"minggu lalu ('{hasil_lalu['platform_terdeteksi']}', hasil='{hasil_lalu['nama_hasil']}') "
                "tampak berbeda platform/jenis hasil, jadi perbandingan % mungkin tidak "
                "membandingkan hal yang sama. Pastikan kedua file dari platform yang sama.")
        for c in hasil_lalu.get("catatan_mata_uang", []):
            if not c.startswith("Tidak ada label") and c not in hasil["catatan_mata_uang"]:
                hasil["catatan_mata_uang"].append("Minggu lalu: " + c)

    omzet = None
    if args.omzet:
        try:
            omzet = hitung_omzet(hasil["total"]["biaya"], args.omzet)
        except ValueError as e:
            keluar_error(str(e))

    hasil["pembanding_minggu_lalu"] = pembanding
    hasil["omzet"] = omzet
    hasil["teks"] = susun_teks(hasil, pembanding, omzet)

    if args.csv_keluaran:
        try:
            tulis_csv_kampanye(args.csv_keluaran, hasil["per_kampanye"], hasil["nama_hasil"])
        except OSError as e:
            keluar_error(pesan_os(e, args.csv_keluaran))

    if args.json:
        print(json.dumps(hasil, ensure_ascii=False, indent=2, default=ke_json))
    else:
        print(hasil["teks"])


def jalankan_gabung(args):
    daftar = []
    for f in args.files:
        try:
            with open(f, encoding="utf-8") as fh:
                d = json.load(fh, parse_float=Decimal)
        except OSError as e:
            keluar_error(pesan_os(e, f))
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            keluar_error(f"Gagal membaca '{f}': jalankan dulu 'analisis --json' untuk tiap platform. ({e})")
        if not isinstance(d, dict) or any(k not in d for k in KUNCI_JSON_WAJIB):
            keluar_error(f"'{f}' bukan hasil 'analisis --json' dari skill ini. Jalankan dulu "
                         "'analisis <file.csv> --json > nama.json' untuk tiap platform.")
        daftar.append(_ke_decimal(d))
    try:
        g = gabung(daftar)
        omzet = hitung_omzet(g["total"]["biaya"], args.omzet) if args.omzet else None
    except ValueError as e:
        keluar_error(str(e))
    g["omzet"] = omzet
    g["teks"] = susun_teks_gabung(g, omzet)
    if args.json:
        print(json.dumps(g, ensure_ascii=False, indent=2, default=ke_json))
    else:
        print(g["teks"])


def main():
    args = buat_parser().parse_args()
    try:
        if args.mode == "analisis":
            jalankan_analisis(args)
        elif args.mode == "gabung":
            jalankan_gabung(args)
    except SystemExit:
        raise
    except Exception as e:  # noqa: BLE001 - skill ini dipakai pengguna awam, jangan pernah traceback mentah
        keluar_error(f"Terjadi kesalahan tak terduga ({type(e).__name__}: {e}). Kirim pesan ini ke "
                     "penjual skill bila berulang.")


if __name__ == "__main__":
    main()
