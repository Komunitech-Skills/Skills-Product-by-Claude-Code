#!/usr/bin/env python3
"""Analisis umum file spreadsheet (CSV / XLSX) untuk pengguna awam.

Hanya memakai library standar Python (3.8+). XLSX dibaca langsung lewat zipfile + xml.etree
(tanpa openpyxl/pandas). Semua angka uang dihitung dengan Decimal.

Subperintah:
  daftar     daftar sheet (XLSX) / info pembacaan file
  profil     profil data: kolom, tipe, kosong, duplikat, nilai tidak valid, outlier
  ringkas    ringkasan statistik: jumlah, rata-rata, median, min, max
  pivot      group-by / pivot: jumlah/rata-rata/hitung per kategori atau per bulan
  tren       tren per bulan (atau hari/minggu/kuartal/tahun) + perubahan %
  top        top-N / bottom-N (per kategori atau per baris) + kumulatif % (Pareto)
  banding    bandingkan dua periode (atau dua file): selisih & persen perubahan
  bersihkan  tulis CSV bersih (angka, tanggal, spasi, huruf besar-kecil kategori dirapikan)

Contoh:
  python3 analisis.py profil data.xlsx
  python3 analisis.py pivot data.xlsx --grup "Cabang" --nilai "Total" --fungsi jumlah
  python3 analisis.py tren data.csv --tanggal "Tanggal" --nilai "Total"
  python3 analisis.py banding data.csv --tanggal Tanggal --nilai Total --periode-a 2026-08 --periode-b 2026-09
(Windows: ganti python3 dengan python atau py)

Kode keluar: 0 = berhasil, 2 = masalah input (pesan jelas di stderr), 3 = kesalahan tak terduga.
"""
import argparse
import bisect
import csv
import io
import json
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from collections import Counter, OrderedDict
from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP, getcontext

getcontext().prec = 40

VERSI = "1.0.11"
BATAS_MB = 50            # file lebih besar ditolak kecuali --paksa
BATAS_BARIS_LAMBAT = 300000
BATAS_XML_MB = 800       # ukuran XML sheet setelah diekstrak (lindungi dari zip bomb)
BATAS_KOLOM_PIVOT = 15
MAKS_KANDIDAT_TAMPIL = 20   # v1.0.7: batas rincian per kandidat di pesan/JSON agar tetap terbaca

NOL = Decimal(0)
SERATUS = Decimal(100)


class InputError(Exception):
    """Masalah input yang dijelaskan ke pengguna tanpa traceback."""


# ---------------------------------------------------------------------------
# Utilitas teks, angka, tanggal
# ---------------------------------------------------------------------------

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
NAMA_BULAN = ["", "Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]

KOSONG = {"", "-", "--", "\u2014", "\u2013", "n/a", "na", "null", "none", "nil"}
GALAT_EXCEL = {"#n/a", "#div/0!", "#value!", "#ref!", "#name?", "#num!", "#null!", "#spill!",
               "#calc!", "#getting_data", "#n/a!"}

KATA_TOTAL = {"total", "grand total", "jumlah", "jumlah total", "subtotal", "sub total", "sub-total",
              "total keseluruhan", "total akhir", "ttl", "grandtotal", "totals"}

# Label baris ringkasan/catatan (v1.0.5). KUAT: dikenali di kolom mana pun (isi sel persis). LEMAH: hanya bila
# satu-satunya teks di baris tanpa tanggal (mis. "Min", "Maks" di bawah tabel).
LABEL_RINGKASAN = KATA_TOTAL | {"rata-rata", "rata rata", "rata2", "rerata", "average", "avg", "mean",
                                "saldo akhir", "saldo awal", "opening balance", "closing balance",
                                "beginning balance", "ending balance", "mutasi kredit", "mutasi debet",
                                "mutasi debit", "total kredit", "total debet", "total debit", "grand-total"}
LABEL_LEMAH = {"min", "maks", "max", "minimum", "maksimum", "maximum", "median", "terkecil", "terbesar"}
AWALAN_RINGKASAN = ("total ", "grand total", "jumlah total", "subtotal", "sub total", "rata-rata ",
                    "saldo akhir", "saldo awal")
AWALAN_LABEL_TITIK2 = ("total", "jumlah", "subtotal", "grand total", "saldo", "mutasi", "rata-rata", "rerata")
POLA_CATATAN = re.compile(r"^(dicetak|dibuat|diunduh|diekspor|dihasilkan|catatan|keterangan|sumber|note|notes|"
                          r"printed|generated|exported|downloaded|source|laporan|periode|halaman|page)\b|:", re.I)

POLA_KODE = re.compile(r"^(no|nomor|nomer|id|kode|code|nik|npwp|nip|nis|nim|sku|telp|telepon|tlp|hp|"
                       r"wa|whatsapp|phone|rekening|norek|resi|kodepos|kode pos|zip)\b", re.I)
# v1.0.8: kolom periode berisi bilangan bulat (Tahun 2026, Masa Pajak 9, Bulan 1..12) = kode/periode, tidak dijumlah
POLA_KOLOM_PERIODE = re.compile(r"^(tahun|tahun pajak|masa|masa pajak|bulan|periode|year|month|tax period|"
                                r"triwulan|kuartal|quarter|semester)$", re.I)
POLA_KODE_AKHIR = re.compile(r"\b(code|kode|id|no|nomor|number|ref)\.?$", re.I)   # "Transaction Code", "Reference No."
POLA_UANG = re.compile(r"(\brp\b|\bidr\b|harga|total|omzet|omset|biaya|nilai (transaksi|penjualan|pembelian|kontrak|faktur|invoice)|nominal|pendapatan|"
                       r"penjualan|gaji|bayar|tagihan|amount|price|revenue|sales|cost|diskon|ongkir|"
                       r"laba|modal|saldo|debit|debet|kredit|credit|pengeluaran|pemasukan|belanja|upah|honor|"
                       r"\buang\b|simpanan|iuran|setoran|tunjangan|\bthr\b|bonus|insentif|komisi)", re.I)
POLA_BUKAN_UANG = re.compile(r"(qty|kuantitas|pcs|unit|jumlah barang|jumlah item|banyak|stok|stock|"
                             r"persen|%|rasio|rating|skor|nilai ujian|berat|kg|gram)", re.I)
POLA_SENSITIF = re.compile(r"(\bnik\b|ktp|npwp|no\.?\s*hp|\bhp\b|telepon|telp|phone|whatsapp|\bwa\b|"
                           r"e-?mail|alamat|address|rekening|norek|gaji|salary|upah|uang lembur|tunjangan|\bthr\b|"
                           r"bonus|insentif|komisi|diagnos|penyakit|"
                           r"rekam medis|agama|tanggal lahir|tgl lahir|tempat lahir|password|sandi|"
                           r"\bpin\b|ibu kandung|kartu kredit|no\.?\s*kartu)", re.I)
POLA_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[a-z]{2,}$", re.I)

POLA_ILMIAH = re.compile(r"\d\s*e\s*[+-]?\s*\d", re.I)
POLA_HARI = re.compile(r"^(senin|selasa|rabu|kamis|jumat|jum'at|sabtu|minggu|ahad|monday|tuesday|"
                       r"wednesday|thursday|friday|saturday|sunday|sen|sel|rab|kam|jum|sab|min|mon|"
                       r"tue|wed|thu|fri|sat|sun)\.?,?\s+", re.I)
POLA_ISO = re.compile(r"^(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})(?:[ T].*)?$")
POLA_DMY = re.compile(r"^(\d{1,2})[-/.](\d{1,2})[-/.](\d{4}|\d{2})(?:[ T].*)?$")
POLA_D_NAMA = re.compile(r"^(\d{1,2})[\s\-/.]*([a-z]+)\.?[\s\-/.,]*(\d{4}|\d{2})(?:[ T,].*)?$", re.I)
POLA_NAMA_D = re.compile(r"^([a-z]+)\.?\s+(\d{1,2}),?\s+(\d{4})(?:[ T,].*)?$", re.I)


def rapikan_teks(s):
    """Buang spasi berlebih (termasuk non-breaking space) di awal, akhir, dan tengah."""
    if s is None:
        return ""
    if type(s) is str and s.isprintable() and "  " not in s and s[:1] != " " and s[-1:] != " ":
        return s        # jalur cepat (hasil identik): tanpa spasi ganda/tepi, tab, baris baru, NBSP, zero-width
    s = str(s).replace("\xa0", " ").replace("\u202f", " ").replace("\u200b", "")
    return " ".join(s.split())


def kunci_kategori(s):
    """Kunci pembanding kategori: tanpa beda huruf besar-kecil dan tanpa spasi ("4 A" = "4a" = "4A")."""
    return "".join(rapikan_teks(s).split()).casefold()


POLA_HP = re.compile(r"^(\+62|62|0)8\d{7,11}$")


def samarkan(v):
    """Samarkan isi data pribadi untuk tampilan: 3201005625752408 -> 3201•••••••••408."""
    if v is None:
        return v
    t = rapikan_teks(v)
    if "@" in t:
        nama, _, dom = t.partition("@")
        if not nama:
            return "•••@" + dom
        # 2 karakter akhir ikut tampil bila bagian nama cukup panjang, agar anggota01 & anggota04 tidak kembar
        return nama[:1] + "•••" + (nama[-2:] if len(nama) >= 6 else "") + "@" + dom
    rapat = re.sub(r"[\s.\-]", "", t)
    if rapat.lstrip("+").isdigit() and len(rapat) >= 7:
        return rapat[:4] + "•" * max(3, len(rapat) - 7) + rapat[-3:]
    if len(t) <= 3:
        return t[:1] + "•••"
    return t[:3] + "•••"


def adalah_kosong(v):
    if v is None:
        return True
    if isinstance(v, str):
        t = rapikan_teks(v).lower()
        return t in KOSONG or t in GALAT_EXCEL
    return False


def adalah_galat_excel(v):
    return isinstance(v, str) and rapikan_teks(v).lower() in GALAT_EXCEL


def _rapikan_desimal(d):
    """Buang nol di belakang koma tanpa menghasilkan notasi 1E+3."""
    if d == d.to_integral_value():
        return d.quantize(Decimal(1))
    return d.normalize()


def dec_dari_xlsx(v):
    """Nilai angka tersimpan XLSX -> Decimal, dibulatkan ke 15 digit signifikan (seperti tampilan Excel)."""
    d = Decimal(v.strip())
    if d != 0 and len(d.as_tuple().digits) > 15:
        d = d.quantize(Decimal(1).scaleb(d.adjusted() - 14), rounding=ROUND_HALF_UP)
    return _rapikan_desimal(d)


_RE_RP_AWAL = re.compile(r"(rp\.?|idr)")
_RE_RP_AKHIR = re.compile(r"(rp|idr)$")
_RE_STRIP_AKHIR = re.compile(r"[.,]-$")
_RE_INTI = re.compile(r"\d[\d.,]*\d|\d")


def _inti_angka(teks):
    """Pisahkan tanda, 'Rp', persen, spasi. Kembalikan (inti_digit, negatif, persen) atau None."""
    s = str(teks).strip().lower()
    for ch in ("\xa0", "\u202f", "\u2009", " "):
        s = s.replace(ch, "")
    if not s or POLA_ILMIAH.search(s):
        return None
    persen = s.endswith("%")
    if persen:
        s = s[:-1]
    neg = False
    ubah = True
    while ubah and s:
        ubah = False
        if s[0] in "-\u2212":
            neg, s, ubah = not neg, s[1:], True
        elif s.startswith("(") and s.endswith(")"):
            neg, s, ubah = not neg, s[1:-1], True
        else:
            m = _RE_RP_AWAL.match(s)
            if m:
                s, ubah = s[m.end():], True
    s = _RE_RP_AKHIR.sub("", s)
    s = _RE_STRIP_AKHIR.sub("", s)                  # 15.000,-
    if s.endswith("-") and len(s) > 1:              # 5.000- (format akuntansi)
        neg, s = not neg, s[:-1]
    if not _RE_INTI.fullmatch(s):
        return None
    return s, neg, persen


def _grup_ok(bulat, sep):
    g = bulat.split(sep)
    return 1 <= len(g[0]) <= 3 and all(len(x) == 3 for x in g[1:])


def bukti_gaya(teks):
    """'id' bila teks jelas memakai koma desimal (1.234,5), 'en' bila titik desimal, None bila tak jelas."""
    inti = _inti_angka(teks)
    if not inti:
        return None
    s = inti[0]
    koma, titik = s.count(","), s.count(".")
    if koma and titik:
        return "id" if s.rfind(",") > s.rfind(".") else "en"
    if koma == 1:
        depan, belakang = s.split(",")
        return "id" if (len(belakang) != 3 or depan == "0") else None
    if titik == 1:
        depan, belakang = s.split(".")
        return "en" if (len(belakang) != 3 or depan == "0") else None
    if koma > 1:
        return "en"
    if titik > 1:
        return "id"
    return None


def parse_angka(teks, gaya=None):
    """Teks angka Indonesia/Inggris -> Decimal, atau None bila bukan angka / meragukan.

    gaya: 'id' (titik ribuan, koma desimal), 'en' (koma ribuan, titik desimal), None (tebak aman:
    satu pemisah + tepat 3 digit = ribuan; selain itu desimal; pola ganjil ditolak).
    """
    if isinstance(teks, Decimal):
        return teks
    if teks is None:
        return None
    inti = _inti_angka(teks)
    if not inti:
        return None
    s, neg, _persen = inti
    koma, titik = s.count(","), s.count(".")
    if koma and titik:
        dec = "," if s.rfind(",") > s.rfind(".") else "."
        if (gaya == "id" and dec != ",") or (gaya == "en" and dec != "."):
            return None
        rib = "." if dec == "," else ","
        bulat, _, pec = s.rpartition(dec)
        if dec in bulat or not _grup_ok(bulat, rib):
            return None
        angka = bulat.replace(rib, "") + "." + pec
    elif koma or titik:
        sep = "," if koma else "."
        jumlah_sep = koma or titik
        sep_desimal = {"id": ",", "en": "."}.get(gaya)
        if jumlah_sep > 1:
            if sep == sep_desimal or not _grup_ok(s, sep):
                return None
            angka = s.replace(sep, "")
        else:
            depan, belakang = s.split(sep)
            if sep_desimal is None:
                if depan == "0" or len(belakang) != 3:
                    angka = depan + "." + belakang
                elif _grup_ok(s, sep):
                    angka = depan + belakang
                else:
                    return None                     # 15000.500 -> meragukan
            elif sep == sep_desimal:
                angka = depan + "." + belakang
            else:
                if not _grup_ok(s, sep):
                    return None
                angka = depan + belakang
    else:
        angka = s
    try:
        d = Decimal(angka)
    except InvalidOperation:
        return None
    return -d if neg else d


def _tahun(t):
    t = int(t)
    return t + 2000 if t < 100 else t


def _buat_tanggal(y, m, d):
    try:
        return date(y, m, d)
    except ValueError:
        return None


def parse_tanggal(teks, urutan="dmy"):
    """Teks tanggal -> date, atau None. Mendukung 2026-09-25, 25/09/2026, 25-09-26, 25 Sep 2026,
    25 September 2026, Kamis, 25 September 2026, Sep 25, 2026 (jam di belakang diabaikan)."""
    if isinstance(teks, datetime):
        return teks.date()
    if isinstance(teks, date):
        return teks
    if teks is None or isinstance(teks, Decimal):
        return None
    s = rapikan_teks(teks)
    if not s:
        return None
    s = POLA_HARI.sub("", s)
    m = POLA_ISO.match(s)
    if m:
        return _buat_tanggal(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = POLA_DMY.match(s)
    if m:
        a, b, y = int(m.group(1)), int(m.group(2)), _tahun(m.group(3))
        d, bl = (a, b) if urutan == "dmy" else (b, a)
        return _buat_tanggal(y, bl, d)
    m = POLA_D_NAMA.match(s)
    if m:
        bl = BULAN.get(m.group(2).lower())
        if bl:
            return _buat_tanggal(_tahun(m.group(3)), bl, int(m.group(1)))
    m = POLA_NAMA_D.match(s)
    if m:
        bl = BULAN.get(m.group(1).lower())
        if bl:
            return _buat_tanggal(int(m.group(3)), bl, int(m.group(2)))
    return None


def deteksi_urutan(teks_list):
    """Kembalikan (urutan, ambigu) untuk tanggal angka a/b/tahun."""
    dmy = mdy = False
    for t in teks_list:
        m = POLA_DMY.match(POLA_HARI.sub("", rapikan_teks(t)))
        if not m:
            continue
        a, b = int(m.group(1)), int(m.group(2))
        dmy = dmy or a > 12
        mdy = mdy or b > 12
    if mdy and not dmy:
        return "mdy", False
    ada_angka = any(POLA_DMY.match(POLA_HARI.sub("", rapikan_teks(t))) for t in teks_list)
    return "dmy", (ada_angka and not dmy)


def serial_ke_tanggal(x, date1904=False):
    """Serial tanggal Excel -> date. Sistem 1900 meniru bug Lotus: serial 60 = 29-Feb-1900 (tidak ada)."""
    if x is None or x < 0:
        return None
    hari = int(x)
    if date1904:
        return date(1904, 1, 1) + timedelta(days=hari)
    if hari == 60:
        return None
    if hari == 0:
        return None
    if hari < 60:
        return date(1899, 12, 31) + timedelta(days=hari)
    return date(1899, 12, 30) + timedelta(days=hari)


def huruf_kolom(i):
    """0 -> A, 25 -> Z, 26 -> AA."""
    s = ""
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


def indeks_kolom(ref):
    """'AB12' -> (27, 12)."""
    m = re.match(r"^\$?([A-Za-z]{1,3})\$?(\d+)$", ref or "")
    if not m:
        return None
    col = 0
    for ch in m.group(1).upper():
        col = col * 26 + (ord(ch) - 64)
    return col - 1, int(m.group(2))


# ---------------------------------------------------------------------------
# Format tampilan (gaya Indonesia)
# ---------------------------------------------------------------------------

def bulatkan(d, desimal=0):
    return d.quantize(Decimal(1).scaleb(-desimal), rounding=ROUND_HALF_UP)


def fmt_angka(d, desimal=None):
    if d is None:
        return "-"
    if desimal is None:
        desimal = 0 if d == d.to_integral_value() else 2
    d = bulatkan(d, desimal)
    neg = d < 0
    teks = "{:f}".format(abs(d))
    bulat, _, pec = teks.partition(".")
    grup = []
    while len(bulat) > 3:
        grup.insert(0, bulat[-3:])
        bulat = bulat[:-3]
    grup.insert(0, bulat)
    hasil = ".".join(grup) + ("," + pec if pec else "")
    return ("-" if neg else "") + hasil


def fmt_uang(d):
    if d is None:
        return "-"
    teks = fmt_angka(abs(bulatkan(d, 0)), 0)
    return ("-Rp " if d < 0 and bulatkan(d, 0) != 0 else "Rp ") + teks


def fmt_persen(d):
    return "-" if d is None else fmt_angka(bulatkan(d, 1), 1) + "%"


def fmt_sel(v, jenis):
    if v is None:
        return "-"
    if jenis == "uang":
        return fmt_uang(v)
    if jenis == "persen":
        return fmt_persen(v)
    if jenis == "angka":
        return fmt_angka(v)
    if jenis == "bulat":
        return fmt_angka(v, 0)
    if isinstance(v, date):
        return fmt_tanggal(v)
    return str(v)


def fmt_tanggal(d):
    return "{} {} {}".format(d.day, NAMA_BULAN[d.month], d.year)


def persen_ubah(lama, baru):
    """(baru - lama) / lama x 100; None bila lama = 0."""
    if lama is None or baru is None or lama == 0:
        return None
    return (baru - lama) / abs(lama) * SERATUS


def kalimat_ubah(lama, baru, fmt):
    if lama is None or baru is None:
        return "tidak bisa dibandingkan (data kosong)"
    if lama == 0 and baru == 0:
        return "sama-sama 0"
    if lama == 0:
        return "naik dari 0 menjadi {} (persen tidak dihitung)".format(fmt(baru))
    p = persen_ubah(lama, baru)
    if bulatkan(p, 1) == 0:
        return "tetap ({} \u2192 {})".format(fmt(lama), fmt(baru))
    arah = "naik" if p > 0 else "turun"
    return "{} {} ({} \u2192 {})".format(arah, fmt_persen(abs(p)), fmt(lama), fmt(baru))


# ---------------------------------------------------------------------------
# Pembacaan file
# ---------------------------------------------------------------------------

def _lokal(tag):
    return tag.rsplit("}", 1)[-1]


def _attr(el, nama):
    for k, v in el.attrib.items():
        if _lokal(k) == nama:
            return v
    return None


def _anak(el, nama):
    for c in el:
        if _lokal(c.tag) == nama:
            return c
    return None


def _teks_si(el):
    """Teks sel shared/inline string: <t> langsung atau run <r><t>; abaikan <rPh> (fonetik)."""
    bagian = []
    for c in el:
        n = _lokal(c.tag)
        if n == "t":
            bagian.append(c.text or "")
        elif n == "r":
            t = _anak(c, "t")
            if t is not None:
                bagian.append(t.text or "")
    return "".join(bagian)


# v1.0.6: sel XLSX berisi RUMUS AGREGAT atas rentang baris lain (=SUM(C2:C6), =SUBTOTAL(9,C2:C9), =AVERAGE(...))
# = bukti tidak ambigu bahwa barisnya baris ringkasan. Rumus per baris (=SUM(B5:D5)) dan saldo berjalan
# (=SUM($C$2:C5), rentangnya memuat baris itu sendiri) BUKAN ringkasan.
POLA_FUNGSI_AGREGAT = re.compile(r"(?<![A-Z0-9_.])(?:_xlfn\.)?(SUM|SUBTOTAL|AVERAGE|AVERAGEA|COUNT|COUNTA|MIN|MAX|"
                                 r"AGGREGATE)\s*\(", re.I)
POLA_RENTANG = re.compile(r"\$?([A-Z]{1,3})\$?(\d+)\s*:\s*\$?([A-Z]{1,3})\$?(\d+)", re.I)
POLA_REF_RELATIF = re.compile(r"(?<![A-Z0-9_$])(\$?)([A-Z]{1,3})(\$?)(\d+)(?![0-9(])", re.I)


def _teks_rumus(f_el, r, bersama):
    """Teks rumus sebuah sel; rumus bersama (t="shared") anak digeser dari rumus induknya."""
    teks = (f_el.text or "").strip()
    if f_el.get("t") != "shared":
        return teks
    si = f_el.get("si")
    if teks:
        bersama[si] = (teks, r)
        return teks
    if si not in bersama:
        return ""
    induk, r0 = bersama[si]
    geser = r - r0

    def ganti(m):
        if m.group(3) == "$":
            return m.group(0)
        return "{}{}{}{}".format(m.group(1), m.group(2), m.group(3), int(m.group(4)) + geser)
    return POLA_REF_RELATIF.sub(ganti, induk)


POLA_REF_SEL = re.compile(r"(?<![A-Z0-9_$!])\$?([A-Z]{1,3})\$?(\d+)(?![0-9(!])", re.I)
POLA_PLUS_SAJA = re.compile(r"^\s*\+?\s*\$?[A-Z]{1,3}\$?\d+(\s*\+\s*\$?[A-Z]{1,3}\$?\d+)+\s*$", re.I)


def _rumus_agregat_luar(teks, r):
    """True bila rumus menjumlah/merangkum baris LAIN: fungsi agregat atas rentang yang TIDAK memuat baris r,
    (v1.0.7, B22) fungsi agregat atas daftar sel tunggal baris lain (=SUM(C5,C9,C12)), atau penjumlahan sel
    saja dari >= 2 baris lain (=C5+C9+C12). Rumus yang menyebut baris r sendiri (=B2*C2, =SUM(B2:D2)) = data."""
    if POLA_PLUS_SAJA.match(teks):
        baris = [int(m.group(2)) for m in POLA_REF_SEL.finditer(teks)]
        return len(baris) >= 2 and r not in baris
    if not POLA_FUNGSI_AGREGAT.search(teks):
        return False
    for m in POLA_RENTANG.finditer(teks):
        a, b = sorted((int(m.group(2)), int(m.group(4))))
        if not (a <= r <= b):
            return True
    if POLA_RENTANG.search(teks):
        return False
    baris = [int(m.group(2)) for m in POLA_REF_SEL.finditer(teks)]
    return len(baris) >= 2 and r not in baris


BUILTIN_TANGGAL = set(range(14, 23)) | set(range(27, 37)) | {45, 46, 47} | set(range(50, 59))


def _format_tanggal(kode):
    s = re.sub(r'"[^"]*"', "", kode)
    s = re.sub(r"\\.", "", s)
    s = re.sub(r"_.", "", s)
    s = re.sub(r"\*.", "", s)
    s = re.sub(r"\[(?!h\]|hh\]|m\]|mm\]|s\]|ss\])[^\]]*\]", "", s, flags=re.I)
    s = s.split(";")[0]
    return bool(re.search(r"[dmyhs]", s, re.I)) and "general" not in s.lower()


class BukuXlsx:
    def __init__(self, path):
        self.peringatan = []
        try:
            self.z = zipfile.ZipFile(path)
        except (zipfile.BadZipFile, OSError) as e:
            raise InputError("File XLSX rusak atau bukan file Excel yang valid ({}). Coba buka di "
                             "Excel/LibreOffice lalu Simpan Ulang (Save As) sebagai .xlsx atau .csv.".format(e))
        nama = set(self.z.namelist())
        if "xl/workbook.xml" not in nama:
            if "content.xml" in nama:
                raise InputError("Ini file OpenDocument (.ods), bukan .xlsx. Buka di LibreOffice/Excel lalu "
                                 "Save As .xlsx atau .csv.")
            raise InputError("File ZIP ini bukan workbook Excel (.xlsx) — xl/workbook.xml tidak ditemukan.")
        wb = self._xml("xl/workbook.xml")
        self.date1904 = any(_lokal(e.tag) == "workbookPr" and (_attr(e, "date1904") or "").lower()
                            in ("1", "true") for e in wb.iter())
        rels = {}
        if "xl/_rels/workbook.xml.rels" in nama:
            for e in self._xml("xl/_rels/workbook.xml.rels").iter():
                if _lokal(e.tag) == "Relationship":
                    rels[e.get("Id")] = e.get("Target", "")
        self.sheets = []
        for e in wb.iter():
            if _lokal(e.tag) != "sheet":
                continue
            target = rels.get(_attr(e, "id"), "")
            if target.startswith("/"):
                path_xml = target.lstrip("/")
            else:
                path_xml = "xl/" + target
            path_xml = os.path.normpath(path_xml).replace("\\", "/")
            self.sheets.append({"nama": e.get("name", "?"), "path": path_xml,
                                "status": e.get("state", "visible")})
        if not self.sheets:
            raise InputError("Workbook tidak berisi sheet apa pun.")
        self.shared = []
        if "xl/sharedStrings.xml" in nama:
            for e in self._xml("xl/sharedStrings.xml"):
                if _lokal(e.tag) == "si":
                    self.shared.append(_teks_si(e))
        self.gaya_tanggal = set()
        if "xl/styles.xml" in nama:
            st = self._xml("xl/styles.xml")
            fmt_custom = {}
            for e in st.iter():
                if _lokal(e.tag) == "numFmt":
                    try:
                        fmt_custom[int(e.get("numFmtId"))] = e.get("formatCode", "")
                    except (TypeError, ValueError):
                        pass
            xfs = None
            for e in st.iter():
                if _lokal(e.tag) == "cellXfs":
                    xfs = e
                    break
            if xfs is not None:
                for i, xf in enumerate(c for c in xfs if _lokal(c.tag) == "xf"):
                    try:
                        fid = int(xf.get("numFmtId", "0"))
                    except ValueError:
                        continue
                    if fid in BUILTIN_TANGGAL or (fid in fmt_custom and _format_tanggal(fmt_custom[fid])):
                        self.gaya_tanggal.add(i)

    def _xml(self, nama):
        try:
            return ET.fromstring(self.z.read(nama))
        except KeyError:
            raise InputError("Bagian '{}' tidak ada di file XLSX (file tidak lengkap/rusak).".format(nama))
        except ET.ParseError as e:
            raise InputError("Bagian '{}' di file XLSX rusak ({}). Buka lalu simpan ulang di Excel.".format(nama, e))

    def pilih_sheet(self, pilihan):
        if pilihan is None:
            terlihat = [s for s in self.sheets if s["status"] == "visible"] or self.sheets
            return terlihat[0]
        p = str(pilihan).strip()
        for s in self.sheets:
            if s["nama"] == p:
                return s
        for s in self.sheets:
            if s["nama"].strip().casefold() == p.casefold():
                return s
        if p.isdigit() and 1 <= int(p) <= len(self.sheets):
            return self.sheets[int(p) - 1]
        raise InputError("Sheet '{}' tidak ada. Sheet yang tersedia: {}.".format(
            p, ", ".join("{}. {}".format(i + 1, s["nama"]) for i, s in enumerate(self.sheets))))

    def baca_sheet(self, sheet):
        """Kembalikan list (nomor_baris_excel, [nilai...]). Nilai: str / Decimal / date / None."""
        try:
            info = self.z.getinfo(sheet["path"])
        except KeyError:
            raise InputError("Isi sheet '{}' tidak ditemukan di file (file rusak).".format(sheet["nama"]))
        if info.file_size > BATAS_XML_MB * 1024 * 1024:
            raise InputError("Sheet '{}' terlalu besar untuk dibaca aman (> {} MB setelah diekstrak).".format(
                sheet["nama"], BATAS_XML_MB))
        baris = {}
        gabungan = []
        rumus_kosong, galat, bug1900 = [], [], []
        rumus_agregat, rumus_bersama = {}, {}
        no_baris_seq = 0
        try:
            with self.z.open(sheet["path"]) as f:
                for _ev, el in ET.iterparse(f, events=("end",)):
                    tag = _lokal(el.tag)
                    if tag == "mergeCell":
                        gabungan.append(el.get("ref", ""))
                    elif tag == "row":
                        try:
                            r = int(el.get("r"))
                        except (TypeError, ValueError):
                            r = no_baris_seq + 1
                        no_baris_seq = r
                        sel = {}
                        kol_seq = -1
                        for c in el:
                            if _lokal(c.tag) != "c":
                                continue
                            pos = indeks_kolom(c.get("r"))
                            kol = pos[0] if pos else kol_seq + 1
                            kol_seq = kol
                            ref = "{}{}".format(huruf_kolom(kol), r)
                            nilai = self._nilai_sel(c, ref, rumus_kosong, galat, bug1900)
                            if nilai is not None:
                                sel[kol] = nilai
                            f_el = _anak(c, "f")
                            if f_el is not None and r not in rumus_agregat:
                                teks_f = _teks_rumus(f_el, r, rumus_bersama)
                                if teks_f and _rumus_agregat_luar(teks_f, r):
                                    rumus_agregat[r] = "{}: ={}".format(ref, teks_f)
                        if sel:
                            n = max(sel) + 1
                            baris[r] = [sel.get(i) for i in range(n)]
                        el.clear()
        except ET.ParseError as e:
            raise InputError("Isi sheet '{}' rusak ({}). Buka lalu simpan ulang di Excel.".format(sheet["nama"], e))
        if rumus_kosong:
            self.peringatan.append(
                "{} sel berisi rumus tanpa nilai tersimpan (mis. {}) sehingga dianggap kosong. Biasanya "
                "file dibuat aplikasi lain/belum dihitung: buka di Excel/LibreOffice, tekan Simpan sekali, "
                "lalu kirim ulang.".format(len(rumus_kosong), ", ".join(rumus_kosong[:5])))
        if galat:
            self.peringatan.append("{} sel berisi galat Excel (#N/A, #DIV/0!, dll., mis. {}) dianggap kosong."
                                   .format(len(galat), ", ".join(galat[:5])))
        if bug1900:
            self.peringatan.append(
                "Sel {} berisi serial tanggal 60 = 29-Feb-1900, tanggal yang sebenarnya TIDAK ADA (bug "
                "warisan Excel). Dianggap tidak valid; periksa isinya.".format(", ".join(bug1900[:5])))
        self._isi_gabungan(baris, gabungan)
        sheet["rumus_agregat"] = {r: t for r, t in rumus_agregat.items() if r in baris}
        return [(r, baris[r]) for r in sorted(baris)]

    def _nilai_sel(self, c, ref, rumus_kosong, galat, bug1900):
        t = c.get("t", "n")
        v_el, f_el, is_el = _anak(c, "v"), _anak(c, "f"), _anak(c, "is")
        v = v_el.text if v_el is not None else None
        if t == "inlineStr":
            return _teks_si(is_el) if is_el is not None else None
        if v is None or v == "":
            if f_el is not None:
                rumus_kosong.append(ref)
            return None
        if t == "s":
            try:
                return self.shared[int(v)]
            except (ValueError, IndexError):
                self.peringatan.append("Sel {} merujuk teks bersama yang tidak ada (file rusak).".format(ref))
                return None
        if t == "str":
            return v
        if t == "b":
            return "TRUE" if v.strip() == "1" else "FALSE"
        if t == "e":
            galat.append(ref)
            return None
        if t == "d":
            return parse_tanggal(v[:10]) or v
        try:
            d = dec_dari_xlsx(v)
        except InvalidOperation:
            return v
        try:
            gaya = int(c.get("s", "0"))
        except ValueError:
            gaya = 0
        if gaya in self.gaya_tanggal:
            if d < 1 and d >= 0 and not self.date1904:
                detik = int(bulatkan(d * 86400, 0))
                return "{:02d}:{:02d}".format(detik // 3600, (detik % 3600) // 60)
            if not self.date1904 and int(d) == 60:
                bug1900.append(ref)
                return None
            tgl = serial_ke_tanggal(d, self.date1904)
            return tgl if tgl else None
        return d

    def _isi_gabungan(self, baris, gabungan):
        """Sel gabungan (merge): teks kiri-atas disalin ke sel lain di rentangnya; angka TIDAK disalin."""
        diisi, angka, datar = [], [], []
        for ref in gabungan:
            if ":" not in ref:
                continue
            a, b = ref.split(":", 1)
            pa, pb = indeks_kolom(a), indeks_kolom(b)
            if not pa or not pb:
                continue
            (c1, r1), (c2, r2) = pa, pb
            baris_a = baris.get(r1, [])
            nilai = baris_a[c1] if c1 < len(baris_a) else None
            if nilai is None:
                continue
            if not isinstance(nilai, str):
                angka.append(ref)
                continue
            if r1 == r2:
                datar.append(ref)       # gabungan mendatar (judul/label): tidak disalin
                continue
            if r2 - r1 > 100000:
                continue
            for r in range(r1, r2 + 1):
                row = baris.setdefault(r, [])
                if len(row) <= c2:
                    row.extend([None] * (c2 + 1 - len(row)))
                for c in range(c1, c2 + 1):
                    if row[c] is None:
                        row[c] = nilai
            diisi.append(ref)
        if diisi:
            self.peringatan.append(
                "{} rentang sel gabungan (merge) ditemukan: {}. Teksnya disalin ke setiap baris di "
                "rentang itu agar bisa dikelompokkan — pastikan ini sesuai maksud tabel.".format(
                    len(diisi), ", ".join(diisi[:6]) + (" ..." if len(diisi) > 6 else "")))
        if angka:
            self.peringatan.append(
                "Sel gabungan berisi angka ({}) TIDAK disalin (agar tidak terhitung ganda); hanya sel "
                "kiri-atasnya yang dihitung.".format(", ".join(angka[:6])))


def _decode(data):
    if data.startswith(b"\xef\xbb\xbf"):
        return data[3:].decode("utf-8", errors="replace"), "utf-8 (BOM)", None
    if data.startswith(b"\xff\xfe") or data.startswith(b"\xfe\xff"):
        try:
            return data.decode("utf-16"), "utf-16", None
        except UnicodeDecodeError:
            raise InputError("File berpenanda UTF-16 tapi isinya rusak. Simpan ulang sebagai 'CSV UTF-8'.")
    try:
        return data.decode("utf-8"), "utf-8", None
    except UnicodeDecodeError:
        return (data.decode("cp1252", errors="replace"), "cp1252 (Windows/Excel lama)",
                "File bukan UTF-8; dibaca sebagai cp1252 (ANSI Excel Windows). Bila ada huruf aneh, "
                "simpan ulang dari Excel sebagai 'CSV UTF-8'.")


def _deteksi_pemisah(teks):
    baris = [b for b in teks.splitlines() if b.strip()][:60]
    if not baris:
        return ","
    terbaik, skor_terbaik = ",", (-1, -1)
    for cand in [",", ";", "\t", "|"]:
        jumlah = [len(r) for r in csv.reader(baris, delimiter=cand)]
        mode, frek = Counter(jumlah).most_common(1)[0]
        if mode < 2:
            continue
        skor = (frek, mode)
        if skor > skor_terbaik:
            terbaik, skor_terbaik = cand, skor
    return terbaik


NAMA_PEMISAH = {",": "koma", ";": "titik koma", "\t": "tab", "|": "garis tegak"}


def _jenis_kolom_csv(rekaman, ncol, pemisah):
    """Kolom bertipe tetap {indeks: "angka"|"tanggal"} dari rekaman normal (tanpa sel multi-baris)."""
    hit = [[0, 0, 0] for _ in range(ncol)]   # angka, tanggal, terisi
    for _no, _a, _b, row in rekaman[1:]:
        if len(row) != ncol or any("\n" in c or "\r" in c for c in row):
            continue
        for j, c in enumerate(row):
            if c.strip():
                hit[j][2] += 1
                if parse_angka(c) is not None:
                    hit[j][0] += 1
                elif parse_tanggal(c.strip()) is not None:
                    hit[j][1] += 1
    jenis = {}
    for j, (na, nt, n) in enumerate(hit):
        if n >= 2 and na >= 0.8 * n:
            jenis[j] = "angka"
        elif n >= 2 and nt >= 0.8 * n:
            jenis[j] = "tanggal"
    return jenis


def _baris_fisik_mirip_data(teks_baris, pemisah, ncol, jenis):
    """True bila SATU baris fisik (dibaca sendirian) tampak seperti baris data utuh: jumlah field ≈ jumlah kolom
    header dan setiap kolom angka/tanggal di posisinya berisi angka/tanggal (minimal 2 kolom bertipe cocok)."""
    if ncol < 2 or not teks_baris.strip():
        return False
    bagian = next(csv.reader([teks_baris], delimiter=pemisah), [])
    if not (ncol - 1 <= len(bagian) <= ncol):
        return False
    cocok = 0
    for j, jn in jenis.items():
        if j >= len(bagian):
            continue
        v = bagian[j].strip().strip('"').strip()
        if not v:
            continue
        ok = parse_angka(v) is not None if jn == "angka" else parse_tanggal(v) is not None
        if not ok:
            return False
        cocok += 1
    return cocok >= min(2, len(jenis)) and cocok >= 1


def _rentang(a, b):
    return "baris {}".format(a) if a == b else "baris {} s.d. {}".format(a, b)


def baca_csv(path, pemisah=None, encoding=None, paksa=False):
    try:
        with open(path, "rb") as f:
            data = f.read()
    except OSError as e:
        raise InputError("File tidak bisa dibuka: {}".format(e))
    if b"\x00" in data[:4096] and not data.startswith((b"\xff\xfe", b"\xfe\xff")):
        raise InputError("File berisi data biner, bukan CSV/teks. Pastikan file yang dikirim benar.")
    info = {"peringatan": []}
    if encoding:
        try:
            teks = data.decode(encoding)
        except (LookupError, UnicodeDecodeError) as e:
            raise InputError("Encoding '{}' gagal dipakai: {}".format(encoding, e))
        if teks.startswith("\ufeff"):
            teks = teks[1:]
        info["encoding"] = encoding
    else:
        teks, info["encoding"], pesan = _decode(data)
        if pesan:
            info["peringatan"].append(pesan)
    if not teks.strip():
        raise InputError("File kosong (tidak ada baris data).")
    baris_teks = teks.splitlines()
    geser = 0   # selisih nomor baris fisik (baris sep= dibuang)
    m = re.match(r"^\s*sep=(.)\s*$", baris_teks[0], re.I)
    if m:
        pemisah = pemisah or m.group(1)
        teks = "\n".join(baris_teks[1:])
        geser = 1
    if pemisah in ("tab", "\\t"):
        pemisah = "\t"
    if not pemisah:
        pemisah = _deteksi_pemisah(teks)
    info["pemisah"] = NAMA_PEMISAH.get(pemisah, pemisah)
    # Parser csv = sumber kebenaran. rekaman: (nomor_rekaman, baris_fisik_awal, baris_fisik_akhir, sel mentah)
    rekaman = []
    awal = 1
    try:
        rd = csv.reader(io.StringIO(teks, newline=""), delimiter=pemisah)
        for i, row in enumerate(rd, start=1):
            akhir = rd.line_num
            rekaman.append((i, awal + geser, akhir + geser, row))
            awal = akhir + 1
    except csv.Error as e:
        raise InputError("CSV rusak di sekitar baris {}: {}. Buka file di Excel/Notepad, perbaiki baris itu, "
                         "lalu simpan ulang.".format(awal + geser, e))
    # 1) Tanda kutip tak tertutup sampai akhir file: parser biasa diam-diam menelan sisa file ke satu sel.
    #    Ini PASTI rusak -> selalu GAGAL (juga dengan --paksa).
    try:
        for _row in csv.reader(io.StringIO(teks, newline=""), delimiter=pemisah, strict=True):
            pass
    except csv.Error as e:
        if "unexpected end of data" in str(e):
            _no, a, b, _r = rekaman[-1] if rekaman else (0, 1 + geser, 1 + geser, [])
            b = max(b, len(teks.splitlines()) + geser)
            ekor = ("baris {} (baris terakhir file)".format(a) if a == b
                    else "baris {} s.d. {} (akhir file)".format(a, b))
            raise InputError(
                "CSV rusak: tanda kutip (\") di baris {} tidak ditutup, sehingga {} terbaca "
                "sebagai SATU sel dan angkanya akan salah. Buka file di Notepad/Excel, perbaiki tanda kutip "
                "di baris {} (hapus, atau tutup dengan \" di akhir teksnya), lalu simpan ulang.".format(a, ekor, a))
    # 2) Sel multi-baris (mis. alamat "Jl. ..., No. ..⏎Kel. .., Kec. .."): SAH. Aturan utama pengaman angka
    #    adalah INVARIAN JUMLAH KOLOM (diperiksa di _potong_tabel setelah judul kolom diketahui): tanda kutip
    #    nyasar hampir selalu membuat rekaman gabungan punya jumlah sel berbeda. Satu-satunya pola yang lolos
    #    invarian itu: kutip nyasar yang "tertutup" beberapa baris kemudian dengan jumlah sel kebetulan tetap
    #    sama. Pola itu dicek di sini, HANYA pada kolom yang biasanya satu baris (kolom yang memang berisi
    #    alamat/catatan berbaris-baris tidak dicurigai -> tidak ada penolakan palsu).
    ncol = Counter(len(r) for _n, _a, _b, r in rekaman if r).most_common(1)[0][0] if rekaman else 0
    jenis_kol = _jenis_kolom_csv(rekaman, ncol, pemisah)
    fisik = io.StringIO(teks, newline="").readlines()     # sama dengan penghitungan baris parser csv
    multi, curiga, n_sel_multi = [], [], 0
    sel_per_kolom = Counter()
    for no, a, b, row in rekaman:
        kol_multi = [j for j, c in enumerate(row) if c and ("\n" in c or "\r" in c)]
        if kol_multi:
            multi.append((no, a, b, kol_multi))
            n_sel_multi += len(kol_multi)
            sel_per_kolom.update(kol_multi)
    batas_jarang = max(2, len(rekaman) // 10)
    for no, a, b, kol_multi in multi:
        if not all(sel_per_kolom[j] <= batas_jarang for j in kol_multi):
            continue
        # Baris fisik lanjutan yang, dibaca sendirian, tampak seperti baris data utuh = baris data yang
        # tertelan tanda kutip nyasar.
        tertelan = [n for n in range(a + 1, b + 1)
                    if 0 < n - geser <= len(fisik)
                    and _baris_fisik_mirip_data(fisik[n - geser - 1].rstrip("\r\n"), pemisah, ncol, jenis_kol)]
        if tertelan:
            curiga.append((no, a, b, "baris {} di Notepad tampak seperti baris data utuh ({} kolom, angka/tanggal "
                           "di posisi yang sama) — kemungkinan tertelan tanda kutip nyasar".format(
                               ", ".join(str(x) for x in tertelan), ncol), len(tertelan)))
    if curiga:
        rincian = "; ".join("{}: {}".format(_rentang(a, b), al) for _n, a, b, al, _h in curiga[:3])
        if len(curiga) > 3:
            rincian += "; dan {} lainnya".format(len(curiga) - 3)
        total_hilang = sum(h for *_x, h in curiga)
        n_fisik = sum(1 for x in fisik if x.strip())
        n_rekaman = sum(1 for _n, _a, _b, r in rekaman if any(c.strip() for c in r))
        n_lanjutan = sum(b - a for _n, a, b, _k in multi)
        hitungan = ("File berisi {} baris (tanpa baris kosong) di Notepad; terbaca {} baris data (termasuk judul) "
                    "+ {} baris lanjutan sel multi-baris — kemungkinan {} baris data HILANG dari hitungan.".format(
                        n_fisik, n_rekaman, n_lanjutan, total_hilang))
        if not paksa:
            no, a, b, _al, _h = curiga[0]
            raise InputError(
                "CSV kemungkinan rusak: {} terbaca sebagai SATU sel, padahal kolom itu biasanya hanya satu baris. "
                "Rincian: {}. {} Biasanya karena tanda kutip (\") tidak tertutup di baris {}. Perbaiki tanda kutip "
                "itu lalu simpan ulang. Bila Anda yakin file benar (sel itu memang berisi teks berbaris-baris), "
                "ulangi dengan --paksa untuk membaca apa adanya.".format(_rentang(a, b), rincian, hitungan, a))
        info["peringatan"].append(
            "PERINGATAN TEGAS (--paksa): CSV dibaca apa adanya walau {} tampak janggal — {}. {} Angka di hasil ini "
            "bisa KURANG bila memang ada tanda kutip nyasar — cek baris itu di Notepad sebelum memakai "
            "angkanya.".format("sel" if len(curiga) == 1 else "{} sel".format(len(curiga)), rincian, hitungan))
    if multi:
        contoh = ", ".join("{} di Notepad = baris {} di Excel".format(_rentang(a, b).capitalize(), no)
                           for no, a, b, _k in multi[:3])
        info["catatan_csv"] = [
            "Info: {} baris berisi sel multi-baris ({} sel, mis. alamat/catatan panjang); tiap sel tetap terbaca "
            "sebagai satu sel dan jumlah kolomnya sudah dicek cocok. Nomor baris di hasil ini = nomor baris di "
            "Excel; di Notepad bergeser: {}{}.".format(len(multi), n_sel_multi, contoh,
                                                       ", dll" if len(multi) > 3 else "")]
        # Kolom yang biasanya satu baris tapi punya 1-2 sel multi-baris: kadang tanda kutip nyasar.
        curiga_no = {no for no, *_x in curiga}
        if len(rekaman) >= 10:
            for j, n in sorted(sel_per_kolom.items()):
                if n > 2:
                    continue
                lok = [(no, a, b) for no, a, b, km in multi if no not in curiga_no and j in km]
                if lok:
                    nama_kol = rekaman[0][3][j].strip() if j < len(rekaman[0][3]) else huruf_kolom(j)
                    info["peringatan"].append(
                        "Kolom '{}' biasanya satu baris, tetapi {} berisi sel multi-baris — cek {} di Notepad, "
                        "mungkin ada tanda kutip (\") nyasar; bila isinya memang catatan berbaris-baris, abaikan "
                        "pesan ini (jumlah kolomnya sudah dicek cocok).".format(
                            nama_kol, "baris " + ", ".join(str(no) for no, _a, _b in lok) + " (Excel)",
                            ", ".join(_rentang(a, b) for _no, a, b in lok)))
    # Untuk invarian jumlah kolom: jumlah sel mentah (sebelum sel kosong di ujung kanan dibuang) & baris Notepad.
    info["n_sel"] = {no: len(row) for no, _a, _b, row in rekaman}
    info["fisik"] = {no: (a, b) for no, a, b, _r in rekaman}
    hasil = []
    for no, _a, _b, row in rekaman:
        row = [None if (c is None or not c.strip()) else c for c in row]
        while row and row[-1] is None:
            row.pop()
        if row:
            hasil.append((no, row))
    return hasil, info


def baca_grid(path, sheet=None, pemisah=None, encoding=None, paksa=False):
    """Kembalikan (grid, info). grid = list (nomor_baris, [nilai])."""
    if not os.path.isfile(path):
        raise InputError("File '{}' tidak ditemukan.".format(path))
    ukuran = os.path.getsize(path)
    if ukuran == 0:
        raise InputError("File kosong (0 byte).")
    if ukuran > BATAS_MB * 1024 * 1024 and not paksa:
        raise InputError("File {:.0f} MB melebihi batas {} MB skill ini. Pecah per bulan/sheet, atau "
                         "tambahkan --paksa bila tetap ingin mencoba (bisa lambat).".format(
                             ukuran / 1048576, BATAS_MB))
    with open(path, "rb") as f:
        kepala = f.read(8)
    info = {"file": os.path.basename(path)}
    if kepala.startswith(b"\xd0\xcf\x11\xe0"):
        raise InputError("Ini file Excel lama (.xls) atau file yang dikunci kata sandi. Buka di Excel, "
                         "hapus kata sandi bila ada, lalu Save As '.xlsx' atau 'CSV UTF-8'.")
    if kepala.startswith(b"PK"):
        buku = BukuXlsx(path)
        sh = buku.pilih_sheet(sheet)
        grid = buku.baca_sheet(sh)
        info.update({"format": "xlsx", "sheet": sh["nama"],
                     "semua_sheet": [s["nama"] for s in buku.sheets],
                     "rumus_agregat": sh.get("rumus_agregat", {}),
                     "peringatan": list(buku.peringatan), "paksa": paksa})
        if sheet is None and len(buku.sheets) > 1:
            info["peringatan"].insert(0, "Workbook punya {} sheet ({}); yang dianalisis: '{}'. Pakai --sheet "
                                      "untuk sheet lain.".format(len(buku.sheets),
                                                                 ", ".join(s["nama"] for s in buku.sheets),
                                                                 sh["nama"]))
        if sh["status"] != "visible":
            info["peringatan"].append("Sheet '{}' tersembunyi (hidden) di Excel.".format(sh["nama"]))
        if buku.date1904:
            info["peringatan"].append("Workbook memakai sistem tanggal 1904 (Mac lama); sudah diperhitungkan.")
        return grid, info
    if path.lower().endswith((".xlsx", ".xlsm")):
        raise InputError("File berakhiran .xlsx tapi isinya bukan Excel (mungkin rusak atau salah ganti "
                         "nama). Buka di Excel lalu simpan ulang.")
    if sheet is not None:
        info.setdefault("peringatan", []).append("--sheet diabaikan karena file ini CSV (hanya 1 tabel).")
    grid, info_csv = baca_csv(path, pemisah, encoding, paksa)
    info["format"] = "csv"
    info["encoding"] = info_csv["encoding"]
    info["pemisah"] = info_csv["pemisah"]
    info["peringatan"] = info.get("peringatan", []) + info_csv["peringatan"]
    info["catatan_csv"] = info_csv.get("catatan_csv", [])
    info["n_sel"], info["fisik"], info["paksa"] = info_csv["n_sel"], info_csv["fisik"], paksa
    return grid, info


# ---------------------------------------------------------------------------
# Tabel: header, baris total, tipe kolom
# ---------------------------------------------------------------------------

def _sel_teks(v):
    return (isinstance(v, str) and not adalah_kosong(v) and parse_angka(v) is None
            and parse_tanggal(v) is None)


def deteksi_header(grid):
    """Indeks (dalam grid) baris header: baris pertama yang cukup lebar & dominan teks."""
    contoh = grid[:30]
    if not contoh:
        return 0
    isi = [sum(1 for v in row if not adalah_kosong(v)) for _r, row in contoh]
    maks = max(isi)
    batas = max(2, -(-maks * 6 // 10)) if maks >= 2 else 1
    for i, (_r, row) in enumerate(contoh):
        n = isi[i]
        if n < batas:
            continue
        teks = sum(1 for v in row if _sel_teks(v))
        unik = len(set(rapikan_teks(v).casefold() for v in row if not adalah_kosong(v)))
        if n > 1 and unik == 1:
            continue
        if teks >= max(1, -(-n * 6 // 10)):
            return i
    for i, n in enumerate(isi):
        if n >= batas:
            return i
    return 0


def _norm_label(v):
    return rapikan_teks(v).lower().strip().rstrip(":").strip()


def _label_ringkasan(row):
    """Label ringkasan (teks sel) bila baris berlabel Total/Jumlah/Subtotal/Grand Total/Rata-rata/Saldo…; None bila bukan.

    v1.0.6: label hanya dikenali pada sel TEKS PERTAMA baris (sel sebelumnya kosong/angka/tanggal), sehingga
    kategori di kolom kedua dst. ("Pegawai 02 | Rata-rata", "KLM-002 | Total") bukan label. Awalan
    ("Total Penjualan", "Rata-rata per pesanan") hanya bila sel itu sel berisi pertama. Min/Maks/Median hanya bila
    satu-satunya teks di baris tanpa tanggal. Label saja belum cukup untuk MEMBUANG baris: lihat _klasifikasi_baris.
    """
    norm = [(v, _norm_label(v)) for v in row if isinstance(v, str) and not adalah_kosong(v)]
    if not norm:
        return None
    if not any(t in LABEL_RINGKASAN or t in LABEL_LEMAH or rapikan_teks(v).strip().endswith(":")
               for v, t in norm) and not norm[0][1].startswith(AWALAN_RINGKASAN):
        return None
    pertama_isi = True
    teks = []
    ada_tanggal = False
    label = None
    for v in row:
        if adalah_kosong(v):
            continue
        if isinstance(v, date):
            ada_tanggal = True
            pertama_isi = False
            continue
        if not isinstance(v, str) or parse_angka(v) is not None:
            pertama_isi = False
            continue
        mentah = rapikan_teks(v).strip()
        if parse_tanggal(mentah) is not None:
            ada_tanggal = True
            pertama_isi = False
            continue
        t = _norm_label(v)
        if not teks:
            if t in LABEL_RINGKASAN or (pertama_isi and t.startswith(AWALAN_RINGKASAN)) or \
                    (mentah.endswith(":") and t.startswith(AWALAN_LABEL_TITIK2) and len(t) <= 40):
                label = mentah
        teks.append(t)
        pertama_isi = False
    if label:
        return label
    if len(teks) == 1 and teks[0] in LABEL_LEMAH and not ada_tanggal:
        return teks[0]
    return None


def _label_jumlah(label):
    """v1.0.9: label ringkasan yang berarti JUMLAH (Total/Grand Total/Jumlah/Subtotal), bukan rata-rata/saldo."""
    t = _norm_label(label)
    return bool(re.search(r"(?<![\w-])(total|totals|jumlah|grand|grandtotal|subtotal|sub total|keseluruhan|ttl)(?![\w-])",
                          t)) and not re.search(r"rata|saldo|average|avg|mean|mutasi|balance|min|maks|max", t)


def _adalah_total(row):
    return _label_ringkasan(row) is not None


def _label_saldo_awal(label):
    t = _norm_label(label)
    return t.startswith(("saldo awal", "saldo sebelumnya", "saldo lalu", "opening balance", "beginning balance"))


POLA_LABEL_TEGAS_AKHIR = re.compile(r"(?<![\w-])(total|jumlah|subtotal|sub total|grand total)$")
POLA_LABEL_TEGAS_AWAL = re.compile(r"(grand total|sub[\s-]?total|jumlah total|total keseluruhan|total semua)(?![\w-])")


def _bentuk_data(mr, prof, modus):
    """Baris berpola SAMA dengan baris data lain: banyak sel terisi >= modus tabel, tidak ada kolom yang biasanya
    terisi dibiarkan kosong, dan jenis tiap sel terisi (angka/tanggal/teks) = jenis mayoritas kolomnya."""
    isi = [(j, jn) for j, (jn, _x) in enumerate(mr) if jn is not None]
    if len(isi) < modus or _ada_kolom_sering_kosong(mr, prof):
        return False
    return all(prof[j]["tipe"] in (jn, "campur") for j, jn in isi)


def _baris_ringkasan(label, mr, prof, modus, blok=None, atas=None, pivot=False):
    """v1.0.11 (B35): SATU-SATUNYA penentu apakah baris berlabel ringkasan (hasil _label_ringkasan) memang baris
    RINGKASAN. Dipakai semua jalur: klasifikasi utama, blok EKOR, blok KEPALA, dan pengaman silang.

    Ringkasan bila: label TEGAS (persis kata ringkasan, berakhiran ':', '<X> Total', 'Grand Total/Subtotal/Jumlah
    Total/Total Keseluruhan …'), atau PivotTable, atau baris TIDAK berpola data (_bentuk_data), atau ada kolom angka
    = jumlah >= 2 baris di atasnya (blok sejak batas terakhir / semua baris data di atasnya), atau SEMUA kolom
    angkanya > nilai terbesar baris di atasnya DAN >= separuh jumlahnya (pola Total yang angkanya salah). Selain itu label hanya
    AWALAN nama ('Total Care Body Lotion', 'Jumlah Besar Deterjen') pada baris data biasa = DATA, di posisi mana pun
    (atas, tengah, baris terakhir, sesudah baris kosong)."""
    if not label:
        return False
    t = _norm_label(label)
    if pivot or t in LABEL_RINGKASAN or t in LABEL_LEMAH or rapikan_teks(label).strip().endswith(":") or \
            POLA_LABEL_TEGAS_AKHIR.search(t) or POLA_LABEL_TEGAS_AWAL.match(t):
        return True
    if not _bentuk_data(mr, prof, modus):
        return True
    angka = [(j, x) for j, (jn, x) in enumerate(mr) if jn == "angka" and prof[j]["tipe"] == "angka"]
    for j, x in angka:
        if not x:
            continue
        for agr in (blok, atas):
            a = agr.get(j) if agr else None
            if a is not None and a.n >= 2 and abs(x - a.s) <= _toleransi(a.s):
                return True
    atas = atas or {}
    return bool(angka) and all(atas.get(j) is not None and atas[j].n >= 2 and x > atas[j].hi and 2 * x >= atas[j].s
                               for j, x in angka)


def _jenis_sel(v, gaya=None):
    """('angka', Decimal) / ('tanggal', date) / ('teks', str) / (None, None) untuk sel kosong/galat."""
    if adalah_kosong(v) or adalah_galat_excel(v):
        return None, None
    if isinstance(v, bool):
        return "teks", str(v)
    if isinstance(v, Decimal):
        return "angka", v
    if isinstance(v, (int, float)):
        return "angka", Decimal(str(v))
    if isinstance(v, date):
        return "tanggal", v
    t = str(v).strip()
    a = parse_angka(t, gaya)
    if a is not None:
        return "angka", a
    d = parse_tanggal(t)
    return ("tanggal", d) if d is not None else ("teks", t)


def _matriks_jenis(rows, lebar):
    """Urai setiap sel SEKALI: (gaya desimal per kolom, matriks [(jenis, nilai)] per baris)."""
    gaya = []
    for j in range(lebar):
        contoh = [row[j] for row in rows if j < len(row) and isinstance(row[j], str)]
        if len(contoh) > 3000:     # cukup sampel merata untuk menebak gaya desimal (file besar tetap cepat)
            contoh = contoh[::len(contoh) // 3000 + 1]
        bukti = Counter(bukti_gaya(v) for v in contoh)
        bukti.pop(None, None)
        gaya.append(bukti.most_common(1)[0][0] if bukti else None)
    kosong = (None, None)
    M = [[_jenis_sel(row[j], gaya[j]) if j < len(row) else kosong for j in range(lebar)] for row in rows]
    return gaya, M


def _profil_dari(M, gaya, lebar):
    """Per kolom: tipe mayoritas ('angka'|'tanggal'|'teks'|'campur'|'kosong'), porsi terisi, gaya desimal.

    "Porsi terisi" = maksimum dari porsi di semua baris dan porsi di baris yang punya teks/tanggal (baris data
    berlabel), agar banyaknya baris jumlah tanpa label di tabel kecil tidak menurunkan porsinya."""
    n = max(1, len(M))
    berlabel = [mr for mr in M if any(jn in ("teks", "tanggal") for jn, _x in mr)] or M
    nb = max(1, len(berlabel))
    prof = []
    for j in range(lebar):
        c = Counter(mr[j][0] for mr in M)
        c.pop(None, None)
        isi = sum(c.values())
        if not isi:
            tipe = "kosong"
        elif c["angka"] >= 0.8 * isi:
            tipe = "angka"
        elif c["tanggal"] >= 0.8 * isi:
            tipe = "tanggal"
        elif c["angka"] <= 0.1 * isi and c["tanggal"] <= 0.1 * isi:
            tipe = "teks"
        else:
            tipe = "campur"
        isi_b = sum(1 for mr in berlabel if mr[j][0] is not None)
        prof.append({"tipe": tipe, "isi": max(isi / n, isi_b / nb), "gaya": gaya[j]})
    return prof


def _profil_kolom(rows, lebar):
    gaya, M = _matriks_jenis(rows, lebar)
    return _profil_dari(M, gaya, lebar)


def _toleransi(x):
    return Decimal(1) if abs(x) >= 100 else Decimal("0.01")


def _ada_kolom_sering_kosong(mr, prof):
    return any(p["isi"] >= 0.8 and mr[j][0] is None for j, p in enumerate(prof))


def _baris_catatan(row, mr, prof):
    """Baris catatan kaki: tanpa angka sama sekali, ada kolom yang biasanya terisi tetapi kosong, dan berisi
    teks bergaya catatan ('Dicetak oleh…', 'Sumber: …', 'Laporan dibuat…', '…:') ATAU hanya satu sel teks
    panjang (>= 25 huruf) pada tabel yang punya >= 3 kolom yang biasanya terisi."""
    if any(jn == "angka" for jn, _x in mr):
        return False
    isi = [row[j] for j, (jn, _x) in enumerate(mr) if jn is not None]
    if not isi or not _ada_kolom_sering_kosong(mr, prof):
        return False
    if any(jn == "teks" and POLA_CATATAN.search(rapikan_teks(row[j]).strip()) for j, (jn, _x) in enumerate(mr)):
        return True
    sering = sum(1 for p in prof if p["isi"] >= 0.8)
    return len(isi) == 1 and isinstance(isi[0], str) and len(rapikan_teks(isi[0])) >= 25 and sering >= 3


POLA_CATATAN_AWAL = re.compile(r"^(\*|(catatan|keterangan|ket|note|notes|nb|n\.b|sumber|source|dicetak|dibuat|"
                               r"diunduh|diekspor|dihasilkan|printed|generated|exported|downloaded)\b)", re.I)


def _hanya_teks(mr):
    return any(jn for jn, _x in mr) and all(jn in (None, "teks") for jn, _x in mr)


def _catatan_berawalan(row, mr):
    """Sel berisi pertama berupa teks berawalan Catatan/Keterangan/Note/NB/*/Sumber… (walau baris berisi angka)."""
    for j, (jn, _x) in enumerate(mr):
        if jn is None:
            continue
        return jn == "teks" and bool(POLA_CATATAN_AWAL.match(rapikan_teks(row[j]).strip()))
    return False


class _Agr:
    """Agregat berjalan satu kolom: jumlah, banyak, min, maks."""
    __slots__ = ("s", "n", "lo", "hi")

    def __init__(self, s=NOL, n=0, lo=None, hi=None):
        self.s, self.n, self.lo, self.hi = s, n, lo, hi

    def tambah(self, x):
        self.s += x
        self.n += 1
        self.lo = x if self.lo is None or x < self.lo else self.lo
        self.hi = x if self.hi is None or x > self.hi else self.hi

    def salin(self):
        return _Agr(self.s, self.n, self.lo, self.hi)


def _tambah_agr(dct, mr, kol_angka):
    for j in kol_angka:
        if mr[j][0] == "angka":
            dct.setdefault(j, _Agr()).tambah(mr[j][1])


def _calon_agregat(a, min_jumlah, ekor):
    """[(nama, nilai)] agregat pembanding dari _Agr."""
    if a is None or a.n == 0:
        return []
    c = []
    if a.n >= min_jumlah:
        c.append(("jumlah", a.s))
    if a.n >= 3:
        c.append(("rata-rata", a.s / a.n))
    if ekor and a.n >= 3:
        c += [("min", a.lo), ("maks", a.hi)]
    return c


def _kolom_nomor_urut(M, j):
    """Kolom angka berisi nomor urut (1, 2, 3, …): >= 80% pasangan berurutan naik tepat 1."""
    v = [mr[j][1] for mr in M if mr[j][0] == "angka"]
    if len(v) < 3:
        return False
    naik = sum(1 for a, b in zip(v, v[1:]) if b - a == 1)
    return naik >= 0.8 * (len(v) - 1)


def _judul_kelompok(M, mentah, keluar, label, lebar, pivot=False):
    """v1.0.8 (B28): baris JUDUL KELOMPOK = tepat satu sel teks (mis. 'SEMEN', 'Jawa') di tengah tabel >= 3 kolom,
    langsung diikuti baris berangka. Hanya bila ada >= 2 baris seperti itu di kolom yang sama dan teksnya unik
    (bukan nilai yang juga muncul di baris data); tabel 2 kolom hanya bila judul kolomnya khas PivotTable.
    Kembalikan {indeks: teks}."""
    if lebar < (2 if pivot else 3):
        return {}
    calon = {}
    n = len(M)
    for i, mr in enumerate(M):
        if i in keluar or i in label:
            continue
        isi = [(j, jn) for j, (jn, _x) in enumerate(mr) if jn is not None]
        if len(isi) != 1 or isi[0][1] != "teks":
            continue
        t = rapikan_teks(mentah[i][isi[0][0]]).strip()
        if not t or POLA_CATATAN_AWAL.match(t) or POLA_CATATAN.search(t) or len(t) > 40:
            continue
        k = i + 1
        while k < n and k in keluar:
            k += 1
        if k >= n or not any(jn == "angka" for jn, _x in M[k]):
            continue
        calon[i] = (isi[0][0], t)
    if len(calon) < 2 or len({j for j, _t in calon.values()}) != 1:
        return {}
    j0 = next(iter(calon.values()))[0]
    teks_c = Counter(_norm_label(t) for _j, t in calon.values())
    if any(v > 1 for v in teks_c.values()):
        return {}
    lain = {_norm_label(mentah[i][j0]) for i in range(n) if i not in calon and M[i][j0][0] == "teks"}
    if any(t in lain for t in teks_c):
        return {}
    return {i: t for i, (_j, t) in calon.items()}


POLA_PIVOT = re.compile(r"^(row labels|column labels|label baris|label kolom|sum of |count of |average of |"
                        r"jumlah dari |hitungan dari |rata-rata dari |grand total$|total keseluruhan$)", re.I)


def _subtotal_di_atas(urut, sudah, M, utama, kol_sum, pivot):
    """v1.0.8 (B26): pivot bentuk ringkas — baris kelompok berisi subtotal DI ATAS anak-anaknya ('Jawa 5.000.000',
    lalu 'Kopi 3.000.000', 'Teh 2.000.000'). Kandidat hanya bila SELURUH tabel terbagi habis menjadi kelompok
    [baris kelompok, >= 2 anak] dengan angka kelompok = jumlah anak-anaknya (kolom utama & kolom angka lain yang
    terisi), minimal 2 kelompok (atau 1 bila judul kolom khas PivotTable)."""
    L = [i for i in urut if i not in sudah]
    if utama is None or len(L) < 3:
        return []
    for i in L:
        if M[i][utama][0] != "angka":
            return []
    grup, p = [], 0
    while p < len(L):
        v = {j: M[L[p]][j][1] for j in kol_sum if M[L[p]][j][0] == "angka"}
        if not v.get(utama):
            return []
        s = {j: NOL for j in v}
        ok = None
        for q in range(p + 1, len(L)):
            for j in v:
                if M[L[q]][j][0] == "angka":
                    s[j] += M[L[q]][j][1]
            # v1.0.9 (B29): kelompok beranak TUNGGAL (baris kelompok = baris tepat di bawahnya, mis. 'Bogor 9' lalu
            # 'Kopi 9') sah sebagai satu kelompok — tidak lagi membatalkan deteksi kelompok lain di file itu.
            if all(abs(s[j] - v[j]) <= _toleransi(v[j]) for j in v):
                ok = q
                break
        if ok is None:
            return []
        grup.append((L[p], ok - p))
        p = ok + 1
    # minimal kelompok beranak >= 2 (bukti kuat): 1 bila judul kolom khas PivotTable, 2 bila bukan
    if sum(1 for _i, k in grup if k >= 2) < (1 if pivot else 2) or len(grup) < 2 and not pivot:
        return []
    return [(i, "angka baris = jumlah {} baris TEPAT DI BAWAHNYA (subtotal kelompok di atas anak-anaknya, gaya "
                "PivotTable ringkas) — bisa terhitung dobel".format(k)) for i, k in grup]


def _klasifikasi_baris(baris_no, mentah, lebar, rumus=None, pertahankan_total=False, buang=None, pertahankan=None,
                       nama=None, pivot=False):
    """v1.0.6 — PRINSIP: baris hanya DIKELUARKAN otomatis bila statusnya TIDAK AMBIGU; kasus lain yang MUNGKIN
    ringkasan tetap DIHITUNG dan dilaporkan sebagai kandidat (peringatan tegas + total alternatif).

    Dikeluarkan otomatis:
      (a) XLSX: baris dengan sel berisi RUMUS AGREGAT (SUM/SUBTOTAL/AVERAGE/COUNT/MIN/MAX/AGGREGATE) atas baris lain;
      (b) blok EKOR (dari baris terakhir ke atas, berturut-turut): baris berlabel ringkasan (Total/Jumlah/Grand
          Total/Rata-rata/Saldo Akhir…), baris catatan (teks saja: bergaya catatan atau dipisah baris kosong), dan
          baris berawalan Catatan/Keterangan/NB/* walau berisi angka;
      (c) blok KEPALA: baris berlabel Saldo Awal/Opening balance tepat di bawah judul kolom;
      (d) baris yang diminta pengguna (--buang-baris).
    Kandidat (tetap dihitung): baris berlabel ringkasan di tengah/atas tabel; baris angka TANPA label (ada kolom
    yang biasanya terisi tetapi kosong) yang nilainya = jumlah/rata-rata baris di atasnya (di ekor juga min/maks).
    --pertahankan-baris melindungi baris dari keduanya; --pertahankan-total = tidak ada yang dikeluarkan/dicurigai.

    Kembalikan (indeks_dipakai, dikeluarkan[(i, alasan)], kandidat[(i, alasan)], profil kolom baris dipakai)."""
    rumus = rumus or {}
    buang = buang or set()
    pertahankan = pertahankan or set()
    gaya, M = _matriks_jenis(mentah, lebar)
    prof = _profil_dari(M, gaya, lebar)
    kol_angka = [j for j, p in enumerate(prof) if p["tipe"] == "angka"]
    n = len(M)
    keluar = {}
    for i, r in enumerate(baris_no):
        if r in buang:
            keluar[i] = "diminta --buang-baris"
    lindung = {i for i, r in enumerate(baris_no) if r in pertahankan and i not in keluar}
    label = {}
    label_putusan = {}      # i -> label ringkasan, atau None bila label ternyata awalan NAMA data
    if not pertahankan_total:
        for i, row in enumerate(mentah):
            if i in keluar or i in lindung:
                continue
            if baris_no[i] in rumus:
                keluar[i] = "rumus agregat ({})".format(rumus[baris_no[i]])
                continue
            lb = _label_ringkasan(row)
            if lb:
                label[i] = lb
        # v1.0.11 (B35): SATU keputusan per baris berlabel, dari _baris_ringkasan, dipakai SEMUA jalur di bawah
        # (ekor, kepala, klasifikasi utama) dan dikembalikan untuk pengaman silang. Agregat pembanding dihitung
        # dari atas ke bawah; baris dikeluarkan/ringkasan = batas blok dan tidak ikut dijumlah.
        n_isi0 = [sum(1 for jn, _x in mr if jn is not None) for mr in M]
        sisa = [n_isi0[i] for i in range(n) if i not in keluar]
        modus0 = Counter(sisa).most_common(1)[0][0] if sisa else 0
        blok, atas = {}, {}
        for i in range(n):
            if i in keluar:
                blok = {}
                continue
            if i in label:
                if _baris_ringkasan(label[i], M[i], prof, modus0, blok, atas, pivot):
                    label_putusan[i] = label[i]
                    blok = {}
                    continue
                label_putusan[i] = None
                del label[i]
            _tambah_agr(blok, M[i], kol_angka)
            _tambah_agr(atas, M[i], kol_angka)
        # blok EKOR: akhiran tabel yang tiap barisnya berlabel ringkasan, berawalan Catatan/NB/*, atau teks saja.
        # Baris teks saja hanya ikut bila bergaya catatan atau blok itu dipisah baris kosong dari data.
        def celah(k):
            j = k - 1
            while j >= 0 and j in keluar:
                j -= 1
            return j >= 0 and isinstance(baris_no[k], int) and isinstance(baris_no[j], int) \
                and baris_no[k] - baris_no[j] > 1

        def jenis_ekor(k, ada_celah):
            if k in label:
                return "label"
            if _catatan_berawalan(mentah[k], M[k]) or \
                    (_hanya_teks(M[k]) and (ada_celah or _baris_catatan(mentah[k], M[k], prof))):
                return "catatan"
            return None
        s0 = n
        while s0 > 0 and (s0 - 1 in keluar or (s0 - 1 not in lindung and (
                s0 - 1 in label or _catatan_berawalan(mentah[s0 - 1], M[s0 - 1]) or _hanya_teks(M[s0 - 1])))):
            s0 -= 1
        while s0 < n:
            ada, buruk = False, None
            for k in range(s0, n):
                if k in keluar:
                    continue
                ada = ada or celah(k)
                if not jenis_ekor(k, ada):
                    buruk = k
            if buruk is None:
                break
            s0 = buruk + 1
        ada = False
        for k in range(s0, n):
            if k in keluar:
                continue
            ada = ada or celah(k)
            if jenis_ekor(k, ada) == "label":
                keluar[k] = "baris ringkasan berlabel '{}' di bawah tabel".format(label.pop(k))
            else:
                keluar[k] = "catatan di bawah tabel"
        # blok KEPALA: Saldo Awal tepat di bawah judul kolom
        for i in range(n):
            if i in keluar:
                continue
            if i in label and _label_saldo_awal(label[i]):
                keluar[i] = "baris '{}' di atas tabel (bukan transaksi)".format(label.pop(i))
                continue
            break
    # v1.0.8 (B28): baris judul kelompok satu sel ('SEMEN', 'Jawa') = bukan data; dilewati + disebut
    judul = {}
    if not pertahankan_total:
        for i, t in _judul_kelompok(M, mentah, keluar, label, lebar, pivot).items():
            if i not in lindung:
                keluar[i] = "judul kelompok '{}' (satu sel teks, bukan data)".format(t)
                judul[i] = _norm_label(t)
    kandidat = []
    urut = [i for i in range(n) if i not in keluar]
    if not pertahankan_total:
        # Wilayah ekor untuk baris tanpa label: sesudah baris terakhir yang punya teks/tanggal (maks. 20 baris).
        t0 = len(urut)
        while t0 > 0 and not any(jn in ("teks", "tanggal") for jn, _x in M[urut[t0 - 1]]):
            t0 -= 1
        t0 = max(t0, len(urut) - 20)
        seg, nonc, semua = {}, {}, {}
        batas_calon = False
        potret = []
        # v1.0.7 — PENGAMAN UMUM (hanya kandidat/peringatan, tidak membuang). Kolom angka utama = kolom angka
        # paling sering terisi (seri: paling kanan). Baris "jarang" = sel terisinya lebih sedikit daripada
        # kebanyakan baris (ringkasan/rincian biasanya tidak punya ID/tanggal/qty).
        utama = max(kol_angka, key=lambda j: (prof[j]["isi"], j)) if kol_angka else None
        n_isi = [sum(1 for jn, _x in mr if jn is not None) for mr in M]
        modus = Counter(n_isi[i] for i in urut).most_common(1)[0][0] if urut else 0
        jarang = {i for i in urut if n_isi[i] < modus}

        def _cek_umum(i, row, mr, seg):
            """Hanya baris JARANG (baris lengkap seperti baris data lain = transaksi; kebetulan x + y = z di baris
            lengkap sangat sering terjadi). (i) kata ringkasan sebagai kata utuh di sel teks mana pun (mis.
            'Jakarta Total' hasil Data > Subtotal); (ii) angka kolom utama = jumlah >= 2 baris berurutan tepat di
            atasnya (sejak kandidat/baris dikeluarkan sebelumnya), dan kolom angka lain yang terisi juga = jumlahnya."""
            x = mr[utama][1] if mr[utama][0] == "angka" else None
            if x is None:
                return None
            if i in jarang:
                for j, (jn, _v) in enumerate(mr):
                    if jn == "teks" and POLA_KATA_RINGKASAN.search(rapikan_teks(row[j])):
                        return "memuat kata ringkasan '{}' dan kolom lain kosong".format(rapikan_teks(row[j]).strip())
            a = seg.get(utama)
            if i not in jarang or a is None or a.n < 2 or not x or abs(x - a.s) > _toleransi(a.s):
                return None
            for j in kol_angka:
                if j != utama and mr[j][0] == "angka":
                    b = seg.get(j)
                    if b is None or abs(mr[j][1] - b.s) > _toleransi(b.s):
                        return None
            return "angka = jumlah {} baris tepat di atasnya".format(a.n)

        # v1.0.8 (B24) — baris ringkasan TERISI LENGKAP (tidak jarang). Kolom penjumlah = kolom angka selain kode/
        # nomor urut. Kolom "bertipe" = kolom yang >= 60% isinya angka/tanggal (teks ringkasan di situ = janggal).
        kol_sum = [j for j in kol_angka
                   if not (nama and j < len(nama) and (POLA_KODE.match(nama[j]) or POLA_KODE_AKHIR.search(nama[j])))
                   and not _kolom_nomor_urut(M, j)]
        kol_bertipe = set()
        for j in range(lebar):
            c = Counter(mr[j][0] for mr in M)
            isi_j = c["angka"] + c["tanggal"] + c["teks"]
            if isi_j and c["angka"] + c["tanggal"] >= 0.6 * isi_j and c["teks"]:
                kol_bertipe.add(j)
        judul_sebelum, judul_kata = {}, {}
        # kolom angka KEMBAR (isi identik di semua baris, mis. 'Harga Awal' = 'Total Pembayaran') = satu bukti saja
        wakil, sidik = {}, {}
        for j in kol_sum:
            wakil[j] = sidik.setdefault(tuple(mr[j][1] for mr in M), j)
        hitung_teks = {}

        def _kata_unik(row, mr):
            for j, (jn, _v) in enumerate(mr):
                if jn != "teks" or not POLA_KATA_RINGKASAN.search(rapikan_teks(row[j])):
                    continue
                if j not in hitung_teks:
                    hitung_teks[j] = Counter(_norm_label(r[j]) for r, m in zip(mentah, M) if m[j][0] == "teks")
                if hitung_teks[j][_norm_label(row[j])] == 1:
                    return True
            return False

        def _cek_lengkap(i, row, mr, blok):  # blok = agregat sejak batas kelompok/kandidat terakhir
            """(1) kata ringkasan ('Jumlah Hadir', 'Total') di sel teks pada kolom yang biasanya angka/tanggal;
            (2) label kelompok: sel teks = judul kelompok sebelumnya ('SEMEN'), atau memuatnya + kata ringkasan
            ('Subtotal Semen', 'Jawa Total'), pada baris berangka; (3) angka baris = jumlah blok >= 2 baris
            berurutan tepat di atasnya (sejak batas kelompok/kandidat sebelumnya) — atau jumlah SEMUA baris data
            di atasnya (grand total) — pada kolom utama DAN >= 1 kolom angka lain sekaligus (kebetulan x + y = z
            pada dua kolom sekaligus sangat jarang)."""
            ada_angka = any(jn == "angka" for jn, _x in mr)
            if not ada_angka:
                return None
            for j in kol_bertipe:
                if mr[j][0] == "teks" and POLA_KATA_RINGKASAN.search(rapikan_teks(row[j])):
                    return "memuat '{}' di kolom yang biasanya angka/tanggal".format(rapikan_teks(row[j]).strip())
            if judul_sebelum:
                for j, (jn, _v) in enumerate(mr):
                    if jn != "teks":
                        continue
                    t = _norm_label(row[j])
                    if t in judul_sebelum:
                        return "label '{}' = judul kelompok di baris {} (kemungkinan subtotal kelompok)".format(
                            rapikan_teks(row[j]).strip(), judul_sebelum[t])
                    if POLA_KATA_RINGKASAN.search(t):
                        kata = re.findall(r"[^\W_]+", t)       # cari judul sebagai rangkaian kata utuh (n-gram)
                        for a in range(len(kata)):
                            for b in range(a + 1, min(len(kata), a + 6) + 1):
                                jt = " ".join(kata[a:b])
                                if jt in judul_kata:
                                    return "label '{}' memuat judul kelompok '{}' (baris {}) + kata ringkasan".format(
                                        rapikan_teks(row[j]).strip(), judul_kata[jt][0], judul_kata[jt][1])
            if utama is None or utama not in kol_sum or mr[utama][0] != "angka" or not mr[utama][1]:
                return None
            cols = [j for j in kol_sum if mr[j][0] == "angka" and wakil[j] == j]
            if len(cols) < 2:
                return None
            for jenis, agr in (("{} baris tepat di atasnya", blok), ("SEMUA {} baris data di atasnya", nonc)):
                a = agr.get(utama)
                if a is None or a.n < 2 or abs(mr[utama][1] - a.s) > _toleransi(a.s):
                    continue
                cocok = [j for j in cols if mr[j][1] and agr.get(j) is not None and agr[j].n >= 2
                         and abs(mr[j][1] - agr[j].s) <= _toleransi(agr[j].s)]
                # blok 2 baris di awal tabel (belum ada batas kelompok) = paling rawan kebetulan: semua kolom wajib cocok
                lemah = a.n < 3 and not batas_calon
                if len(cocok) < 2 or 2 * len(cocok) < len(cols) or (lemah and len(cocok) < len(cols)):
                    continue
                # bukti tambahan: kata ringkasan di sel teks yang UNIK di kolomnya ('Subtotal Cabang Bekasi', bukan
                # nama produk berulang 'Jumlah Besar Hemat'), ATAU >= 2 kolom cocok yang bukan bilangan kecil
                # (qty 1 + 2 = 3 terlalu mudah kebetulan)
                besar = [j for j in cocok if abs(mr[j][1]) > 100 or mr[j][1] != mr[j][1].to_integral_value()]
                if len(besar) >= 2 or _kata_unik(row, mr):
                    return "angka di {} kolom = jumlah {}".format(len(cocok), jenis.format(a.n))
            return None

        def tambah(dct, mr):
            _tambah_agr(dct, mr, kol_angka)
        for pos, i in enumerate(urut):
            mr = M[i]
            alasan = None
            if i > 0 and i - 1 in keluar:      # baris yang dikeluarkan (rumus/--buang-baris) = batas kelompok
                seg = {}
                batas_calon = True
                k = i - 1
                while k >= 0 and k in keluar:
                    if k in judul:
                        judul_sebelum.setdefault(judul[k], baris_no[k])
                        judul_kata.setdefault(" ".join(re.findall(r"[^\W_]+", judul[k])), (judul[k], baris_no[k]))
                    k -= 1
            if i in label:
                alasan = "berlabel '{}' di {} tabel".format(label[i], "tengah" if pos else "atas")
            elif i not in lindung:
                isi = [(j, x) for j, (jn, x) in enumerate(mr) if jn is not None]
                if isi and all(mr[j][0] == "angka" and prof[j]["tipe"] == "angka" for j, _x in isi) \
                        and _ada_kolom_sering_kosong(mr, prof):
                    ekor = pos >= t0
                    nama_cocok = None
                    for j, x in isi:
                        calon = _calon_agregat(seg.get(j), 1 if batas_calon else 2, False)
                        a = nonc.get(j)
                        if a is not None and a.n != (seg[j].n if j in seg else 0):
                            calon += _calon_agregat(a, 2, ekor)
                        elif ekor:
                            calon += [c for c in _calon_agregat(a, 2, True) if c[0] in ("min", "maks")]
                        if ekor:
                            for p in potret:
                                calon += _calon_agregat(p.get(j), 2, True)
                        cocok = next((nm for nm, v in calon if abs(x - v) <= _toleransi(v)), None)
                        if not cocok:
                            nama_cocok = None
                            break
                        nama_cocok = nama_cocok or cocok
                    if nama_cocok:
                        alasan = "angka tanpa label = {} baris di atasnya".format(nama_cocok)
            if not alasan and i not in lindung and utama is not None:
                alasan = _cek_umum(i, mentah[i], mr, seg)
            if not alasan and i not in lindung:
                alasan = _cek_lengkap(i, mentah[i], mr, seg)
            if alasan:
                kandidat.append((i, alasan))
                seg = {}
                batas_calon = True
                tambah(semua, mr)
            else:
                tambah(seg, mr)
                tambah(nonc, mr)
                tambah(semua, mr)
            if pos >= t0 - 1:
                potret.append({j: a.salin() for j, a in semua.items()})
        kandidat += _cari_rincian(urut, kandidat, keluar, M, utama, jarang, lindung, buang, baris_no)
        if not lindung:
            kandidat += _subtotal_di_atas(urut, {i for i, _a in kandidat}, M, utama, kol_sum, pivot)
        kandidat.sort()
    dikeluarkan = sorted(keluar.items())
    dipakai = urut
    return dipakai, dikeluarkan, kandidat, _profil_dari([M[i] for i in dipakai], gaya, lebar), label_putusan


POLA_KATA_RINGKASAN = re.compile(r"(?<![\w-])(total|sub[\s-]?total|jumlah|grand|rekap|rata-rata|rata2|rerata|"
                                 r"saldo)(?![\w-])", re.I)


def _cari_rincian(urut, kandidat, keluar, M, utama, jarang, lindung, buang, baris_no):
    """v1.0.7 (iii): sekelompok >= 2 baris JARANG berurutan tepat di bawah (atau di atas) sebuah baris ringkasan
    (kandidat atau baris yang dikeluarkan) yang jumlahnya = angka baris itu, mis. rincian pembayaran Tunai/QRIS/
    Transfer di bawah 'Total Penjualan' -> kandidat juga (total bisa terhitung dobel)."""
    if utama is None:
        return []
    sudah = {i for i, _a in kandidat}
    pos = {i: p for p, i in enumerate(urut)}
    jangkar = sorted(sudah | {i for i in keluar if baris_no[i] not in buang})
    hasil = []

    def nilai(i):
        jn, x = M[i][utama]
        return x if jn == "angka" else None

    for c in jangkar:
        v = nilai(c)
        if not v:
            continue
        # posisi awal di urutan baris dipakai: sesudah / sebelum c
        if c in keluar:     # urut terurut naik: posisi baris dipakai pertama sesudah c (bisect, bukan pindai O(n))
            p_sesudah = bisect.bisect_right(urut, c)
            p_sesudah = p_sesudah if p_sesudah < len(urut) else None
        else:
            p_sesudah = pos[c] + 1
        p_sebelum = (p_sesudah - 1 if p_sesudah is not None else len(urut) - 1) if c in keluar else pos[c] - 1
        for arah, p in ((1, p_sesudah), (-1, p_sebelum)):
            if p is None:
                continue
            ambil, jml = [], NOL
            while 0 <= p < len(urut) and len(ambil) < 12:
                i = urut[p]
                x = nilai(i)
                if i in sudah or i in lindung or i not in jarang or x is None:
                    break
                ambil.append(i)
                jml += x
                if len(ambil) >= 2 and abs(jml - v) <= _toleransi(v):
                    for k in ambil:
                        sudah.add(k)
                        hasil.append((k, "rincian baris {}: {} baris jarang di {}nya berjumlah sama dengan baris "
                                         "itu (mis. rincian pembayaran) — bisa terhitung dobel".format(
                                             baris_no[c], len(ambil), "bawah" if arah > 0 else "atas")))
                    break
                p += arah
            else:
                continue
    return hasil


def _ringkas_sel(row, maks=60):
    def teks(v):
        if adalah_kosong(v):
            return ""
        if isinstance(v, Decimal):
            return fmt_angka(v)
        if isinstance(v, date):
            return fmt_tanggal(v)
        return rapikan_teks(v).replace("\n", " ")
    t = " | ".join(teks(v) for v in row).rstrip(" |")
    return t if len(t) <= maks else t[:maks - 1] + "…"


def _isi_bernama(row, nama, maks=90):
    """Isi baris untuk pesan: 'Kolom=nilai, …' (sel kosong dilewati; kolom lain kosong)."""
    def teks(v):
        if isinstance(v, Decimal):
            return fmt_angka(v)
        if isinstance(v, date):
            return fmt_tanggal(v)
        return rapikan_teks(v).replace("\n", " ")
    isi = ["{}={}".format(nama[j] if j < len(nama) else "Kolom {}".format(huruf_kolom(j)), teks(v))
           for j, v in enumerate(row) if not adalah_kosong(v)]
    t = ", ".join(isi) + ("; kolom lain kosong" if len(isi) < len([v for v in nama if v]) else "")
    return t if len(t) <= maks else t[:maks - 1] + "…"


def _cek_geser(row, k, prof, nama):
    """Untuk baris yang kekurangan sel: kembalikan uraian sel yang tipenya tidak cocok dengan kolomnya
    (tanda isi bergeser), atau None bila semua sel yang ada cocok tipe kolomnya."""
    for j in range(min(k, len(row))):
        v = row[j]
        if j >= len(prof):
            break
        jn, _x = _jenis_sel(v, prof[j]["gaya"])
        tp = prof[j]["tipe"]
        if jn is None or tp in ("campur", "kosong"):
            continue
        if tp == "angka" and jn != "angka":
            return "'{}' masuk kolom '{}' yang biasanya angka".format(rapikan_teks(v), nama[j])
        if tp == "tanggal" and jn != "tanggal":
            return "'{}' masuk kolom '{}' yang biasanya tanggal".format(rapikan_teks(v), nama[j])
        if tp == "teks" and jn in ("angka", "tanggal"):
            return "{} '{}' masuk kolom '{}' yang biasanya teks".format(
                "angka" if jn == "angka" else "tanggal", rapikan_teks(v), nama[j])
    return None


def _cek_jumlah_kolom(info, r_header, header, baris_no, data_rows, peringatan, prof=None, nama=None,
                      catatan=None):
    """INVARIAN CSV: setiap baris data wajib punya jumlah sel = jumlah judul kolom.

    Toleransi (tidak ada angka yang bergeser):
    - sel KOSONG berlebih di ujung kanan (padding Excel);
    - (v1.0.5) baris yang kekurangan sel HANYA di kolom paling kanan, bila kolom-kolom yang hilang itu kosong di
      >= 50% baris data (kolom opsional, mis. Catatan) DAN setiap sel yang ada cocok tipe kolomnya (angka di
      kolom angka, tanggal di kolom tanggal, teks di kolom teks) -> sel yang hilang dianggap kosong + info.
    Baris lain yang kekurangan sel, atau yang punya sel berisi di luar judul kolom -> GAGAL (kecuali --paksa).
    """
    n_sel, fisik = info["n_sel"], info.get("fisik", {})
    m = len(header)                                   # judul kolom sampai judul terakhir yang berisi
    batas_lebih = max(m, n_sel.get(r_header, m))      # judul boleh diikuti sel kosong (padding)
    dipakai = set(baris_no)
    prof = prof or []
    nama = nama or [rapikan_teks(v) for v in header]
    rows_dipakai = [(r, row) for r, row in data_rows if r in dipakai]
    # Tipe kolom untuk baris yang punya k sel diukur dari baris yang LEBIH panjang (> k sel), agar baris pendek
    # yang bergeser tidak ikut "mengajari" tipe kolom. Terlalu sedikit pembanding -> profil semua baris.
    prof_per_k = {}

    def prof_untuk(k):
        if k not in prof_per_k:
            lebih = [list(row) for r, row in rows_dipakai if n_sel.get(r, len(row)) > k]
            prof_per_k[k] = _profil_kolom(lebih, len(prof)) if prof and len(lebih) >= 3 else prof
        return prof_per_k[k]
    n_data = max(1, len(rows_dipakai))
    kosong_kol = Counter()
    for r, row in rows_dipakai:
        for j in range(m):
            if j >= len(row) or adalah_kosong(row[j]) or j >= n_sel.get(r, m):
                kosong_kol[j] += 1
    salah, opsional = [], []
    for r, row in rows_dipakai:
        k = n_sel.get(r, len(row))
        if k < m:
            hilang = list(range(k, m))
            geser = _cek_geser(row, k, prof_untuk(k), nama) if prof else "tipe kolom tidak diketahui"
            wajib = [j for j in hilang if (kosong_kol[j] - 1) < 0.5 * (n_data - 1)]
            if not geser and not wajib:
                opsional.append((r, hilang))
                continue
            alasan = "hanya {} dari {} kolom".format(k, m)
            if geser:
                alasan += " ({})".format(geser)
            elif wajib:
                alasan += " (kolom '{}' tidak ada, padahal biasanya terisi)".format(
                    "', '".join(nama[j] for j in wajib[:3]))
            salah.append((r, alasan, row))
        elif len(row) > batas_lebih:
            salah.append((r, "{} kolom terisi, padahal judul kolom hanya {}".format(len(row), m), row))
    if opsional and catatan is not None:
        kol = sorted({j for _r, h in opsional for j in h})
        catatan.append("Info: {} baris tidak punya sel untuk kolom paling kanan ({}) — kolom itu memang sering "
                       "kosong, jadi dianggap kosong; angka tidak bergeser (mis. baris {}).".format(
                           len(opsional), ", ".join("'{}'".format(nama[j]) for j in kol),
                           ", ".join(str(r) for r, _h in opsional[:5])))
    if not salah:
        return

    def lokasi(r):
        a, b = fisik.get(r, (r, r))
        return "baris {}".format(r) if (a, b) == (r, r) else "baris {} (Notepad: {})".format(r, _rentang(a, b))
    rincian = "; ".join("{}: {} → {}".format(lokasi(r), al, _ringkas_sel(row)) for r, al, row in salah[:5])
    if len(salah) > 5:
        rincian += "; dan {} baris lainnya".format(len(salah) - 5)
    n = len(salah)
    if not info.get("paksa"):
        raise InputError(
            "Jumlah kolom tidak cocok di {} baris data, jadi file ini BELUM dihitung (kalau dipaksa, angka bisa "
            "masuk ke kolom yang salah dan total/rata-rata jadi SALAH). Aturannya: setiap baris harus punya {} "
            "kolom, sama dengan judul kolom ({}). Baris bermasalah: {}. Kemungkinan penyebab: (1) sel kosong/"
            "terlewat di tengah baris sehingga isi sesudahnya bergeser ke kiri; (2) teks berisi koma atau titik "
            "koma tanpa diapit tanda kutip; (3) tanda kutip (\") nyasar yang menggabungkan beberapa baris; "
            "(4) catatan di tengah tabel. Cara memperbaiki: buka file di Excel, lihat baris di atas, isi sel yang "
            "terlewat atau pindahkan isinya ke kolom yang benar (baris catatan boleh dihapus), simpan ulang, lalu "
            "analisis lagi. Bila Anda yakin angkanya tidak bergeser, ulangi dengan --paksa (hasil diberi "
            "peringatan).".format(n, m, ", ".join(rapikan_teks(v) or "(kosong)" for v in header), rincian))
    peringatan.insert(0,
        "PERINGATAN TEGAS (--paksa): {} baris data jumlah kolomnya tidak sama dengan judul kolom ({} kolom): {}. "
        "Angka di baris itu bisa bergeser ke kolom lain atau tidak terhitung — total/rata-rata di hasil ini "
        "MUNGKIN SALAH. Perbaiki baris itu sebelum memakai angkanya.".format(n, m, rincian))


POLA_HALAMAN = re.compile(r"^(halaman|hal\.?|page|hlm\.?)\s*:?\s*\d+\s*((dari|of|/)\s*\d+)?$", re.I)


def _header_berulang(row, teks_row, nama_asli):
    """v1.0.7: baris yang >= 50% judul kolomnya muncul lagi DI POSISI YANG SAMA (min. 2) dan tanpa angka/tanggal
    = judul kolom berulang (mis. tiap halaman mutasi bank), bukan data."""
    if len(nama_asli) < 2:
        return False
    cocok = sum(1 for j, t in nama_asli.items() if j < len(teks_row) and teks_row[j] == t)
    if cocok < 2 or cocok * 2 < len(nama_asli):
        return False
    return all(_sel_teks(v) for v in row if not adalah_kosong(v))


def _cari_tabel_kedua(baris_no, mentah, lebar, set_header, n_header):
    """v1.0.7 (B21): baris judul kolom BERBEDA di tengah data = awal tabel kedua. Syarat: semua sel teks
    (bukan angka/tanggal), >= 2 sel dan >= separuh jumlah judul kolom, ada baris berangka sebelum & sesudahnya,
    dan (memuat nama judul kolom tabel pertama ATAU teksnya berada di >= 2 kolom yang biasanya angka/tanggal, atau
    di 1 kolom angka/tanggal bila didahului baris kosong/baris judul satu sel). Kembalikan (baris awal tabel kedua, baris judulnya, isi judul) atau None."""
    calon = []
    for i, row in enumerate(mentah):
        isi = [(j, v) for j, v in enumerate(row) if not adalah_kosong(v)]
        if len(isi) < 2 or len(isi) * 2 < n_header:
            continue
        # saring cepat (file besar): sel bukan teks / berawalan angka -> bukan baris judul kolom
        if any(not isinstance(v, str) or v.lstrip()[:1].isdigit() for _j, v in isi):
            continue
        if all(_sel_teks(v) for _j, v in isi):
            calon.append(i)
    if not calon:
        return None
    ada_angka = [any(isinstance(v, (Decimal, int, float)) or (isinstance(v, str) and parse_angka(v) is not None)
                     for v in row if not adalah_kosong(v)) for row in mentah]
    prof = None
    for i in calon:
        if not any(ada_angka[:i]) or not any(ada_angka[i + 1:]):
            continue
        teks = [(j, rapikan_teks(v).casefold()) for j, v in enumerate(mentah[i]) if not adalah_kosong(v)]
        tanda = any(t in set_header for _j, t in teks)
        if not tanda:
            if prof is None:
                contoh = [r for k, r in enumerate(mentah) if k not in calon]
                contoh = contoh[::len(contoh) // 2000 + 1] if contoh else contoh
                prof = _profil_kolom(contoh, lebar)
            bertipe = sum(1 for j, _t in teks if j < len(prof) and prof[j]["tipe"] in ("angka", "tanggal"))
            # teks di kolom angka/tanggal: >= 2 sel, atau 1 sel bila didahului baris kosong / baris judul 1 sel
            sebelum = mentah[i - 1] if i else []
            jeda = (isinstance(baris_no[i], int) and isinstance(baris_no[i - 1], int)
                    and baris_no[i] - baris_no[i - 1] > 1) or \
                (not ada_angka[i - 1] and sum(1 for v in sebelum if not adalah_kosong(v)) == 1)
            tanda = bertipe >= 2 or (bertipe >= 1 and jeda)
        if not tanda:
            continue
        awal = i
        while awal > 0 and not ada_angka[awal - 1] and \
                sum(1 for v in mentah[awal - 1] if not adalah_kosong(v)) == 1 and \
                isinstance(baris_no[awal - 1], int) and isinstance(baris_no[awal], int) and \
                baris_no[awal] - baris_no[awal - 1] == 1:
            awal -= 1
        return baris_no[awal], baris_no[i], ", ".join(rapikan_teks(v) for _j, v in
                                                        ((j, mentah[i][j]) for j, _t in teks))
    return None


def _header_tampak_data(grid, idx):
    """v1.0.8 (B25): baris 'judul kolom' yang sebenarnya DATA — ada sel angka/tanggal yang jenisnya sama dengan isi
    kolom di bawahnya. Angka yang lazim jadi judul kolom (tahun 1900–2100, nomor urut 1, 2, 3 …) diabaikan.
    Kembalikan uraian bukti (teks) atau None."""
    _r, header = grid[idx]
    bawah = [row for _r2, row in grid[idx + 1: idx + 301]]
    if len(bawah) < 2:
        return None
    lebar = max([len(header)] + [len(row) for row in bawah])
    prof = _profil_kolom(bawah, lebar)
    angka_h = []
    bukti = []
    for j, v in enumerate(header):
        jn, x = _jenis_sel(v, prof[j]["gaya"])
        if jn == "angka":
            angka_h.append((j, x))
        elif jn == "tanggal" and prof[j]["tipe"] == "tanggal":
            bukti.append((j, v))
    bulat = [x for _j, x in angka_h if x == x.to_integral_value()]
    urut = len(bulat) >= 2 and len(bulat) == len(angka_h) and \
        sorted(bulat) == [min(bulat) + k for k in range(len(bulat))] and max(bulat) <= 100
    for j, x in angka_h:
        if urut or prof[j]["tipe"] != "angka" or (x == x.to_integral_value() and 1900 <= x <= 2100):
            continue
        bukti.append((j, header[j]))
    if not bukti:
        return None
    return ", ".join("'{}'".format(rapikan_teks(v) if isinstance(v, str) else
                                   (fmt_tanggal(v) if isinstance(v, date) else fmt_angka(v))) for _j, v in bukti[:4])


def _potong_tabel(grid, info, baris_header=None, pertahankan_total=False, buang=None, pertahankan=None):
    """Pisahkan header, baris Total, dan baris data dari grid satu sheet/CSV."""
    catatan, peringatan = [], []
    mulai, sampai = info.get("mulai_baris"), info.get("sampai_baris")
    if grid and (mulai or sampai):
        grid = [(r, row) for r, row in grid if isinstance(r, int) and (not mulai or r >= mulai)
                and (not sampai or r <= sampai)]
        catatan.append("Hanya baris {} s.d. {} yang dibaca (--mulai-baris/--sampai-baris).".format(
            mulai or 1, sampai or "akhir"))
    if not grid:
        raise InputError("Tidak ada data di {}.".format(
            "sheet '{}'".format(info["sheet"]) if info.get("sheet") else "file"))
    if baris_header is not None and baris_header < 0:
        raise InputError("--baris-header harus 0 (tanpa judul kolom) atau nomor baris >= 1.")
    tanpa_header = baris_header == 0
    if baris_header:
        idx = next((i for i, (r, _row) in enumerate(grid) if r >= baris_header), None)
        if idx is None or grid[idx][0] != baris_header:
            raise InputError("Baris header {} kosong atau di luar data.".format(baris_header))
    else:
        idx = deteksi_header(grid)
        if not tanpa_header:
            bukti = _header_tampak_data(grid, idx)
            if bukti:
                tanpa_header = True
                peringatan.append(
                    "PERINGATAN TEGAS — Tabel ini tampaknya TIDAK punya baris judul kolom: baris {} berisi data "
                    "({}), jenisnya sama dengan isi kolom di bawahnya. Baris {} DIHITUNG sebagai data dan kolom "
                    "diberi nama Kolom1, Kolom2, …. Sebutkan ke pengguna nama kolom sebenarnya; bila baris {} "
                    "ternyata memang judul kolom, ulangi dengan --baris-header {}.".format(
                        grid[idx][0], bukti, grid[idx][0], grid[idx][0], grid[idx][0]))
    if tanpa_header:
        r_header = None
        lebar0 = max(len(row) for _r, row in grid[idx:])
        header = ["Kolom{}".format(j + 1) for j in range(lebar0)]
        data_rows = grid[idx:]
        if baris_header == 0:
            catatan.append("Dibaca TANPA judul kolom (--tanpa-header): semua baris mulai baris {} = data; kolom "
                           "dinamai Kolom1..Kolom{}.".format(grid[idx][0], lebar0))
    else:
        r_header, header = grid[idx]
        data_rows = grid[idx + 1:]
    if r_header is not None and r_header != 1:
        catatan.append("Judul kolom (header) terdeteksi di baris {} (baris di atasnya dianggap "
                       "judul/keterangan). Bila salah, pakai --baris-header N.".format(r_header))
    lebar = max([len(header)] + [len(row) for _r, row in data_rows]) if data_rows else len(header)
    nama = []
    for i in range(lebar):
        v = header[i] if i < len(header) else None
        if isinstance(v, date):
            n = fmt_tanggal(v)
        elif isinstance(v, Decimal):   # v1.0.9 (B30): judul angka bulat (tahun 2023) tampil apa adanya
            n = str(int(v)) if v == v.to_integral_value() else fmt_angka(v)
        else:
            n = rapikan_teks(v)
        nama.append(n or "Kolom {}".format(huruf_kolom(i)))
    seen = Counter()
    for i, n in enumerate(nama):
        seen[n.casefold()] += 1
        if seen[n.casefold()] > 1:
            nama[i] = "{} ({})".format(n, seen[n.casefold()])
    kunci_header = [x.casefold() for x in nama]
    nama_asli = {} if tanpa_header else {j: rapikan_teks(header[j]).casefold() for j in range(min(len(header), lebar))
                                         if isinstance(header[j], str) and not adalah_kosong(header[j])}
    set_header = set(nama_asli.values())
    # v1.0.7 (B23): baris judul di atas header yang berulang di tengah (mis. "MUTASI REKENING" tiap halaman)
    judul_atas = set()
    for _r, row in grid[:idx]:
        isi = tuple(rapikan_teks(v).casefold() for v in row if not adalah_kosong(v))
        if isi and all(isinstance(v, str) for v in row if not adalah_kosong(v)):
            judul_atas.add(isi)
    baris_no, mentah, baris_total, header_ulang, halaman = [], [], [], [], []
    for r, row in data_rows:
        row = list(row) + [None] * (lebar - len(row))
        if all(adalah_kosong(v) for v in row):
            continue
        teks_row = [rapikan_teks(v).casefold() if isinstance(v, str) else "" for v in row]
        if teks_row == kunci_header or _header_berulang(row, teks_row, nama_asli):
            header_ulang.append(r)
            continue
        isi = [v for v in row if not adalah_kosong(v)]
        if all(isinstance(v, str) for v in isi) and (
                (len(isi) == 1 and POLA_HALAMAN.match(rapikan_teks(isi[0]).strip()))
                or tuple(rapikan_teks(v).casefold() for v in isi) in judul_atas):
            halaman.append(r)
            continue
        baris_no.append(r)
        mentah.append(row)
    kedua = _cari_tabel_kedua(baris_no, mentah, lebar, set_header, len(nama_asli))
    if kedua:
        n_awal, n_header, isi_header = kedua
        pesan = ("File ini berisi LEBIH DARI SATU TABEL: tabel kedua mulai baris {} (judul kolom berbeda di baris "
                 "{}: {}). Kalau digabung, angka tabel kedua masuk ke kolom tabel pertama dan total jadi SALAH. "
                 "Pisahkan tabelnya di Excel, atau analisis per tabel: tabel pertama dengan --sampai-baris {}, "
                 "tabel kedua dengan --mulai-baris {}.".format(n_awal, n_header, isi_header, n_awal - 1, n_header))
        if not info.get("paksa"):
            raise InputError(pesan)
        peringatan.insert(0, "PERINGATAN TEGAS (--paksa): " + pesan)
    # v1.0.6: keluarkan otomatis HANYA yang tidak ambigu; yang mungkin ringkasan = kandidat (tetap dihitung)
    pivot = any(POLA_PIVOT.match(rapikan_teks(v).strip()) for _r, row in grid[:idx + 1] for v in row
                if isinstance(v, str))
    if pivot:
        catatan.append("Tabel ini tampaknya PivotTable yang disalin sebagai nilai (judul 'Row Labels'/'Label Baris'/"
                       "'Sum of'/'Jumlah dari'). Hanya baris paling rinci yang boleh dijumlah; baris kelompok, "
                       "'Total …' dan 'Grand Total' adalah ringkasan.")
    dipakai, keluar, calon, prof, putusan = _klasifikasi_baris(baris_no, mentah, lebar, info.get("rumus_agregat"),
                                                      pertahankan_total, buang, pertahankan, nama, pivot)
    dikeluarkan = [(baris_no[i], al, _isi_bernama(mentah[i], nama)) for i, al in keluar]
    kandidat = [(baris_no[i], al, _isi_bernama(mentah[i], nama)) for i, al in calon]
    semua_no = set(baris_no)
    tidak_ada = sorted(r for r in (buang or set()) | (pertahankan or set()) if r not in semua_no)
    baris_total = [r for r, _a, _i in dikeluarkan]
    # v1.0.9 (B31): baris Total/Grand Total/Jumlah di EKOR (dikeluarkan, atau kandidat yang jadi baris terakhir)
    # disimpan sebagai ACUAN pengaman silang: angkanya dibandingkan dengan total hasil hitungan script.
    acuan = []
    akhir = max(dipakai) if dipakai else -1
    for i, al in keluar:
        if i <= akhir:
            continue
        # v1.0.11 (B35): acuan = baris yang DIPUTUSKAN ringkasan oleh _baris_ringkasan (bukan tebakan dari teks)
        if putusan.get(i) and _label_jumlah(putusan[i]):
            acuan.append((baris_no[i], rapikan_teks(putusan[i]).strip(), i, False))
        elif al.startswith("rumus agregat") and not re.search(r"(AVERAGE|COUNT|MIN|MAX|MEDIAN)", al, re.I):
            lb = next((rapikan_teks(v).strip() for v in mentah[i] if isinstance(v, str) and not adalah_kosong(v)
                       and parse_angka(v) is None), None)
            if lb is None or _label_jumlah(lb):
                acuan.append((baris_no[i], lb or "baris rumus jumlah", i, False))
    if dipakai and any(i == dipakai[-1] for i, _a in calon) and putusan.get(dipakai[-1], "") is not None:
        lb = next((rapikan_teks(v).strip() for v in mentah[dipakai[-1]] if isinstance(v, str)
                   and not adalah_kosong(v) and parse_angka(v) is None and _label_jumlah(v)), None)
        if lb:      # kandidat (sudah diperingatkan): hanya penguat, bukan dasar peringatan beda
            acuan.append((baris_no[dipakai[-1]], lb, dipakai[-1], True))
    baris_no_asli, mentah_asli = baris_no, mentah
    baris_no = [baris_no[i] for i in dipakai]
    mentah = [mentah[i] for i in dipakai]
    # buang kolom tanpa nama & tanpa isi
    pakai = [i for i in range(lebar)
             if not nama[i].startswith("Kolom ") or any(not adalah_kosong(row[i]) for row in mentah)]
    kolom = [nama[i] for i in pakai]
    acuan = [(baris_no_asli[i], lb, [mentah_asli[i][j] for j in pakai], pn) for _r, lb, i, pn in acuan]
    mentah = [[row[i] for i in pakai] for row in mentah]
    if tidak_ada:
        peringatan.append("Nomor baris {} di --buang-baris/--pertahankan-baris bukan baris data tabel ini (judul, "
                          "kosong, atau di luar tabel) — diabaikan.".format(", ".join(map(str, tidak_ada))))
    if info.get("n_sel") is not None and not info.get("paksa") and not tanpa_header and \
            rapikan_teks(header[0] if header else "").strip().upper() == "FK" and \
            {rapikan_teks(row[0]).strip().upper() for _r, row in data_rows if row} <= {"FK", "LT", "OF"}:
        raise InputError(
            "File ini tampaknya CSV e-Faktur format lama (baris FK = faktur, LT = lawan transaksi, OF = objek/"
            "barang faktur). Ketiga jenis baris punya kolom berbeda, jadi TIDAK bisa dijumlah sebagai satu tabel "
            "(DPP faktur dan DPP barang akan terhitung dobel). Untuk total per faktur, hitung baris FK saja: "
            "ulangi dengan --paksa --filter \"FK=FK\" (kolom JUMLAH_DPP / JUMLAH_PPN). Untuk rincian barang, "
            "salin baris OF ke sheet terpisah dengan judul kolom OF.")
    if info.get("n_sel") is not None:
        _cek_jumlah_kolom(info, r_header, header, baris_no, data_rows, peringatan, prof, nama, catatan)
        lebih = []
    else:
        lebih = [r for r, row in zip(baris_no, mentah)
                 if any(not adalah_kosong(v) for v in row[len(header):])] if lebar > len(header) else []
    if lebih:
        peringatan.append("{} baris berisi lebih banyak sel daripada judul kolom (mis. baris {}); isinya masuk "
                          "kolom tanpa nama ({}). Pada CSV biasanya karena koma/pemisah di dalam teks yang tidak "
                          "diapit tanda kutip — cek baris itu.".format(
                              len(lebih), ", ".join(map(str, lebih[:5])),
                              ", ".join("Kolom {}".format(huruf_kolom(i)) for i in range(len(header), lebar))))
    catatan += info.get("catatan_csv", [])
    if header_ulang:
        catatan.append("{} baris yang mengulang judul kolom dilewati (baris {}).".format(
            len(header_ulang), ", ".join(map(str, header_ulang[:8]))))
    if halaman:
        catatan.append("{} baris judul/nomor halaman yang berulang di tengah data dilewati (baris {}).".format(
            len(halaman), ", ".join(map(str, halaman[:8]))))
    if not mentah:
        raise InputError("Judul kolom ditemukan di baris {} tetapi tidak ada baris data di bawahnya."
                         .format(r_header))
    return {"baris_header": r_header if r_header is not None else 0, "kolom": kolom, "baris_no": baris_no,
            "mentah": mentah,
            "baris_total": baris_total, "header_ulang": header_ulang + halaman, "catatan": catatan,
            "peringatan": peringatan, "dikeluarkan": dikeluarkan, "kandidat": kandidat, "acuan_total": acuan}


class Data:
    """Tabel siap analisis: kolom bernama, nilai terurai per tipe."""

    def __init__(self, grid, info, baris_header=None, pertahankan_total=False, urutan=None, tipe_paksa=None,
                 potongan=None, tampilkan_pribadi=False, buang=None, pertahankan=None):
        self.info = info
        self.peringatan = list(info.get("peringatan", []))
        self.catatan = []
        self.tampilkan_pribadi = tampilkan_pribadi
        self.disamarkan = []
        self._dup = None
        self._buang_pengguna = bool(buang)
        p = potongan or _potong_tabel(grid, info, baris_header, pertahankan_total, buang, pertahankan)
        self.dikeluarkan = p.get("dikeluarkan", [])
        self.kandidat = p.get("kandidat", [])
        self.baris_header = p["baris_header"]
        self.kolom, self.baris_no, self.mentah = p["kolom"], p["baris_no"], p["mentah"]
        self.baris_total, self.header_ulang = p["baris_total"], p["header_ulang"]
        self.peringatan += p["peringatan"]
        self.catatan += p["catatan"]
        if len(self.mentah) > BATAS_BARIS_LAMBAT:
            self.peringatan.append("Data {} baris — melebihi {} baris; hasil tetap dihitung tetapi bisa lambat."
                                   .format(fmt_angka(Decimal(len(self.mentah))), fmt_angka(Decimal(BATAS_BARIS_LAMBAT))))
        self.urutan_paksa = urutan
        self.tipe_paksa = tipe_paksa or {}
        self.kol = OrderedDict()
        for i, n in enumerate(self.kolom):
            self.kol[n] = self._ketik(n, [row[i] for row in self.mentah])
        self.total_alternatif = self._total_alternatif()
        self.cek_silang = self._cek_silang(p.get("acuan_total", []))
        self._pesan_ringkasan()
        sens = [n for n, k in self.kol.items() if k["sensitif"]]
        if sens:
            self.peringatan.append(
                "Kolom yang tampak berisi DATA PRIBADI/SENSITIF: {}. Contoh isinya tidak ditampilkan; "
                "jangan bagikan file/hasil mentah ke pihak lain tanpa izin (UU PDP No. 27/2022)."
                .format(", ".join(sens)))

    # -- baris dikeluarkan & kandidat ringkasan (v1.0.6) -------------------
    def _total_alternatif(self):
        """Per kolom angka yang tersentuh kandidat: total DENGAN (default) & TANPA baris kandidat."""
        if not self.kandidat:
            return []
        posisi = {r: i for i, r in enumerate(self.baris_no)}
        hasil = []
        for nama, k in self.kol.items():
            if k["tipe"] != "angka":
                continue
            vals = k["nilai"]
            per = [(r, vals[posisi[r]]) for r, _a, _i in self.kandidat
                   if r in posisi and vals[posisi[r]] is not None]
            if not per:
                continue
            dengan = sum((v for v in vals if v is not None), NOL)
            hasil.append({"kolom": nama, "uang": k["uang"], "dengan": dengan,
                          "tanpa": dengan - sum((v for _r, v in per), NOL),
                          "tanpa_per_baris": [{"baris": r, "total": dengan - v} for r, v in per[:MAKS_KANDIDAT_TAMPIL]]})
        hasil.sort(key=lambda a: not a["uang"])
        return hasil

    def _cek_silang(self, acuan):
        """v1.0.9 (B31) — PENGAMAN SILANG: angka baris Total/Grand Total di file (acuan) dibandingkan dengan total
        hasil hitungan script per kolom angka. Status per kolom: 'cocok' (= total hitungan), 'cocok_tanpa'
        (= total TANPA baris kandidat), 'beda' (+ rasio 2x/3x bila bulat). Kolom yang angkanya di baris itu =
        rata-rata/min/maks (bukan jumlah) dilewati."""
        alt = {a["kolom"]: a for a in self.total_alternatif}
        hasil = []
        # subtotal kelompok terakhir ('Subtotal', 'Subtotal Cabang C') boleh menguatkan (cocok) tetapi tidak dipakai
        # untuk peringatan beda — angkanya memang hanya sebagian tabel.
        for r, label, row, penguat in acuan:
            kol = []
            for j, n in enumerate(self.kolom):
                k = self.kol[n]
                if k["tipe"] != "angka" or k.get("persen") or j >= len(row) or adalah_kosong(row[j]):
                    continue
                v = row[j]
                x = v if isinstance(v, Decimal) else (parse_angka(v, k["gaya"]) if isinstance(v, str) else None)
                vals = [a for a in k["nilai"] if a is not None]
                if not x or not vals:
                    continue
                total = sum(vals, NOL)
                tanpa = alt[n]["tanpa"] if n in alt else None
                rasio = None
                if abs(x - total) <= _toleransi(x):
                    st = "cocok"
                elif tanpa is not None and abs(x - tanpa) <= _toleransi(x):
                    st = "cocok_tanpa"
                else:
                    st = "beda"
                    rasio = next((m for m in (2, 3) if abs(total - m * x) <= _toleransi(total)), None)
                    # angka baris itu = rata-rata/min/maks kolom (bukan jumlah) -> bukan pembanding, kecuali rasio bulat
                    if not rasio and any(abs(x - y) <= _toleransi(x)
                                         for y in (total / len(vals), min(vals), max(vals))):
                        continue
                kol.append({"kolom": n, "di_file": x, "hitungan": total, "tanpa_kandidat": tanpa, "status": st,
                            "rasio": rasio, "uang": k["uang"]})
            if kol:
                kol.sort(key=lambda c: not c["uang"])
                hasil.append({"baris": r, "label": label, "kolom": kol,
                              "subtotal": penguat or bool(re.search(r"\bsub[\s-]?total", label, re.I))})
        return hasil

    def _pesan_silang(self):
        """(jenis, teks): jenis 'cocok' -> catatan; 'tanpa' -> ditambahkan ke peringatan kandidat; 'tegas'/'lunak'
        -> peringatan tersendiri."""
        if not self.cek_silang:
            return None, None

        def ringkas(c, kunci="di_file"):
            return "kolom '{}' {}".format(c["kolom"], fmt_angka(c[kunci]))
        for a in self.cek_silang:
            if all(c["status"] == "cocok" for c in a["kolom"]):
                return "cocok", ("Pengaman silang: total hasil hitungan COCOK dengan baris '{}' di file (baris {}): "
                                 "{}.{} Keyakinan hasil lebih tinggi.".format(
                                     a["label"], a["baris"], "; ".join(ringkas(c) for c in a["kolom"][:4]),
                                     " Cocok DENGAN baris kandidat ikut dihitung — kemungkinan baris kandidat "
                                     "memang data." if self.kandidat else ""))
        for a in self.cek_silang:
            if all(c["status"] in ("cocok", "cocok_tanpa") for c in a["kolom"]):
                return "tanpa", ("PENGAMAN SILANG: baris '{}' di file (baris {}) = total TANPA baris kandidat ({}) — "
                                 "kemungkinan besar total yang benar adalah total TANPA baris kandidat.".format(
                                     a["label"], a["baris"], "; ".join(ringkas(c) for c in a["kolom"][:4])))
        utama = [x for x in self.cek_silang if not x["subtotal"]]
        if not utama:
            return None, None
        a = utama[-1]      # baris Total terakhir (Grand Total)
        beda = [c for c in a["kolom"] if c["status"] == "beda"]
        ganda = [c for c in beda if c["rasio"]]
        lain = [c for c in beda if not c["rasio"]]
        bagian = []
        for c in beda[:4]:
            t = "kolom '{}': total hitungan {} ≠ {} di file {}".format(
                c["kolom"], fmt_angka(c["hitungan"]), a["label"], fmt_angka(c["di_file"]))
            if c["rasio"]:
                t += " (tepat {}× — kemungkinan subtotal/baris kelompok ikut terhitung)".format(c["rasio"])
            bagian.append(t)
        # v1.0.10 (B33): hanya situasi DOBEL HITUNG (tepat k×) yang boleh menawarkan angka file sebagai alternatif.
        # Selisih lain = Total di FILE yang patut dicek; cari penjelasannya (sel angka bertipe teks / baris tepi).
        for c in lain:
            c["penjelasan"] = self._jelaskan_selisih(c["kolom"], c["hitungan"] - c["di_file"])
        jelas = bool(lain) and all(c["penjelasan"] and c["penjelasan"]["jenis"] in ("sel_teks", "baris_tepi")
                                   for c in lain)
        # pengguna sudah memutuskan baris mana yang dibuang (--buang-baris) -> peringatan biasa, kecuali rasio bulat
        tegas = bool(ganda) or (all(c["status"] == "beda" for c in a["kolom"]) and not self._buang_pengguna
                                and not jelas)
        teks = "{} — PENGAMAN SILANG: Total hitungan ≠ '{}' di file (baris {}): {}.".format(
            "PERINGATAN TEGAS" if tegas else "PERINGATAN", a["label"], a["baris"], "; ".join(bagian))
        if ganda:
            teks += (" Kemungkinan DOBEL HITUNG (subtotal/baris kelompok ikut terhitung): total tanpa subtotal "
                     "kemungkinan = {}. Total alternatif = angka '{}' di file ({}). Tampilkan kedua angka ke "
                     "pengguna dan periksa tata letak tabel (profil) sebelum menyimpulkan.").format(
                         "; ".join("kolom '{}' {}".format(c["kolom"], fmt_angka(c["hitungan"] / c["rasio"]))
                                   for c in ganda[:4]),
                         a["label"], "; ".join(ringkas(c) for c in ganda[:4]))
        for c in lain[:4]:
            teks += (" Kolom '{}': Total di file ({}) tidak sama dengan jumlah baris data ({}); selisih {} tidak "
                     "dijelaskan oleh subtotal. Periksa rumus Total di file Anda (mis. angka yang tersimpan "
                     "sebagai teks tidak ikut dijumlah Excel, atau rentang rumus tidak mencakup semua baris).").format(
                         c["kolom"], fmt_angka(c["di_file"]), fmt_angka(c["hitungan"]),
                         fmt_angka(abs(c["hitungan"] - c["di_file"])))
            if c["tanpa_kandidat"] is not None:
                teks += " (Total TANPA baris kandidat ringkasan = {} juga tidak sama.)".format(
                    fmt_angka(c["tanpa_kandidat"]))
            if c["penjelasan"]:
                teks += " " + c["penjelasan"]["teks"]
        if lain:
            teks += (" Angka Total di file BUKAN jawaban alternatif — jangan dipakai sebagai total; {}").format(
                "hitungan script sudah memasukkan semua baris data; sebutkan ke pengguna bahwa Total di file "
                "kemungkinan salah." if jelas else
                "tampilkan total hitungan, jelaskan bahwa Total di file berbeda, dan minta pengguna memeriksa "
                "rumus/baris datanya sebelum menyimpulkan.")
        return ("tegas" if tegas else "lunak"), teks

    def _jelaskan_selisih(self, nama, selisih):
        """v1.0.10 (B33): cari penyebab selisih total hitungan − Total di file: (1) sel angka bertipe TEKS di
        kolom yang selain itu berisi angka asli (SUM Excel melewatkannya); (2) 1–3 baris data di awal/akhir tabel
        (rentang rumus kurang); (3) tepat satu baris data mana pun. None bila tidak ditemukan."""
        if not selisih:
            return None
        k = self.kol[nama]
        j = self.kolom.index(nama)
        vals = k["nilai"]
        tol = _toleransi(abs(selisih))
        ada_asli = any(isinstance(row[j], Decimal) for row in self.mentah)
        if selisih > 0 and ada_asli:
            teks_i = [i for i, row in enumerate(self.mentah)
                      if isinstance(row[j], str) and not adalah_kosong(row[j]) and vals[i] is not None]
            if teks_i and abs(sum((vals[i] for i in teks_i), NOL) - selisih) <= tol:
                no = [self.baris_no[i] for i in teks_i]
                return {"jenis": "sel_teks", "baris": no, "teks":
                        "Penyebab yang cocok: sel {} di baris {} berisi angka yang TERSIMPAN SEBAGAI TEKS (jumlahnya "
                        "{} = tepat selisihnya) — rumus SUM Excel tidak menjumlahkannya, sedangkan hitungan script "
                        "sudah memasukkannya. Total di file kemungkinan SALAH; perbaiki dengan mengubah sel itu "
                        "menjadi angka.".format(nama, ", ".join(map(str, no[:10])), fmt_angka(selisih))}
        isi = [i for i, v in enumerate(vals) if v is not None]
        if selisih > 0 and len(isi) >= 3:
            for m in (1, 2, 3):
                for ujung, pilih in (("akhir", isi[-m:]), ("awal", isi[:m])):
                    if m < len(isi) and abs(sum((vals[i] for i in pilih), NOL) - selisih) <= tol:
                        no = [self.baris_no[i] for i in pilih]
                        return {"jenis": "baris_tepi", "baris": no, "teks":
                                "Penyebab yang cocok: selisihnya = tepat angka baris {} (di {} tabel) — kemungkinan "
                                "rentang rumus Total di file tidak mencakup baris itu. Hitungan script sudah "
                                "memasukkannya; Total di file kemungkinan SALAH.".format(
                                    ", ".join(map(str, no)), ujung)}
            satu = [i for i in isi if abs(vals[i] - selisih) <= tol]
            if len(satu) == 1:
                no = [self.baris_no[satu[0]]]
                return {"jenis": "satu_baris", "baris": no, "teks":
                        "Kemungkinan penyebab: selisihnya = tepat angka baris {} — cek apakah baris itu ikut "
                        "dijumlah rumus Total di file.".format(no[0])}
        return None

    def _pesan_ringkasan(self):
        def daftar(no):
            return ",".join(str(r) for r in no)
        if self.dikeluarkan:
            isi = "; ".join("baris {} ({}): '{}'".format(r, al, t) for r, al, t in self.dikeluarkan[:8])
            if len(self.dikeluarkan) > 8:
                isi += "; dan {} baris lainnya".format(len(self.dikeluarkan) - 8)
            self.peringatan.insert(0,
                "BARIS DIKELUARKAN dari perhitungan ({} baris, bukan data): {}. Bila ada yang ternyata data asli, "
                "ulangi dengan --pertahankan-baris {}.".format(
                    len(self.dikeluarkan), isi, daftar(r for r, _a, _t in self.dikeluarkan)))
        if self.kandidat:
            # v1.0.7: dibatasi agar tetap terbaca; daftar lengkap ada di JSON (kemungkinan_ringkasan)
            n_k = len(self.kandidat)
            isi = "; ".join("baris {} ({} — {})".format(r, t, al) for r, al, t in self.kandidat[:8])
            if n_k > 8:
                isi += "; dan {} baris lainnya".format(n_k - 8)
            alt = []
            for a in self.total_alternatif[:3]:
                teks = "kolom '{}': DENGAN baris itu {} / TANPA SEMUA baris itu {}".format(
                    a["kolom"], fmt_angka(a["dengan"]), fmt_angka(a["tanpa"])) if n_k > 1 else \
                    "kolom '{}': DENGAN baris itu {} / TANPA baris itu {}".format(
                    a["kolom"], fmt_angka(a["dengan"]), fmt_angka(a["tanpa"]))
                per = a["tanpa_per_baris"]
                if len(per) > 1:
                    teks += " (per kandidat — tanpa baris {}{})".format("; tanpa baris ".join(
                        "{} saja: {}".format(x["baris"], fmt_angka(x["total"])) for x in per[:5]),
                        "; …" if len(per) > 5 else "")
                alt.append(teks)
            no = [r for r, _a, _t in self.kandidat]
            saran = daftar(no) if n_k <= 30 else daftar(no[:30]) + ",… (daftar lengkap di keluaran --json)"
            self.peringatan.insert(0,
                "PERINGATAN TEGAS — Kemungkinan baris ringkasan ikut terhitung ({} baris): {}. Baris itu TETAP "
                "DIHITUNG di hasil ini. Bila benar ringkasan, ulangi dengan --buang-baris {}. Total alternatif: {}. "
                "Tanyakan ke pengguna (atau tampilkan kedua total) sebelum menyimpulkan.".format(
                    n_k, isi, saran, "; ".join(alt) if alt else "(baris itu tidak berisi angka di kolom angka)"))
        jenis, teks = self._pesan_silang()
        if jenis == "cocok":
            self.catatan.insert(0, teks)
        elif jenis == "tanpa" and self.kandidat:
            self.peringatan[0] += " " + teks
        elif jenis:
            self.peringatan.insert(1 if self.kandidat else 0, teks)

    # -- tipe kolom --------------------------------------------------------
    def _ketik(self, nama, mentah):
        isi = [(i, v) for i, v in enumerate(mentah) if not adalah_kosong(v)]
        galat = sum(1 for v in mentah if adalah_galat_excel(v))
        n = len(isi)
        teks_str = [v for _i, v in isi if isinstance(v, str)]
        paksa = self.tipe_paksa.get(nama.casefold())
        k = {"nama": nama, "terisi": n, "kosong": len(mentah) - n, "galat": galat, "tidak_valid": [],
             "uang": False, "gaya": None, "urutan": None, "urutan_ambigu": False,
             "sensitif": bool(POLA_SENSITIF.search(nama)), "gabung_kategori": []}
        if teks_str and not k["sensitif"]:
            email = sum(1 for v in teks_str if POLA_EMAIL.match(rapikan_teks(v)))
            nik = sum(1 for v in teks_str if re.fullmatch(r"\d{16}", rapikan_teks(v)))
            hp = sum(1 for v in teks_str if POLA_HP.match(re.sub(r"[\s.\-]", "", rapikan_teks(v))))
            if email > len(teks_str) / 2 or nik > len(teks_str) / 2 or hp > len(teks_str) / 2:
                k["sensitif"] = True
        if n == 0:
            k["tipe"] = "kosong"
            k["nilai"] = [None] * len(mentah)
            return k
        # gaya desimal & urutan tanggal dari bukti di seluruh kolom
        bukti = Counter(bukti_gaya(v) for v in teks_str)
        bukti.pop(None, None)
        if bukti:
            k["gaya"] = bukti.most_common(1)[0][0]
            if len(bukti) > 1:
                k["gaya_campur"] = True
        urutan, ambigu = deteksi_urutan(teks_str)
        if self.urutan_paksa:
            urutan, ambigu = self.urutan_paksa, False
        k["urutan"], k["urutan_ambigu"] = urutan, ambigu
        angka = [parse_angka(v, k["gaya"]) if isinstance(v, str) else (v if isinstance(v, Decimal) else None)
                 for _i, v in isi]
        tgl = [parse_tanggal(v, urutan) if isinstance(v, (str, date)) else None for _i, v in isi]
        n_angka = sum(1 for a in angka if a is not None)
        n_tgl = sum(1 for t in tgl if t is not None)
        nol_depan = sum(1 for v in teks_str if re.fullmatch(r"\s*0\d+\s*", v))
        digit_panjang = sum(1 for v in teks_str if re.fullmatch(r"\s*\+?\d{11,}\s*", v))
        angka_bulat = all(a == a.to_integral_value() for a in angka if a is not None)
        if paksa:
            tipe = paksa
        elif n_tgl >= 0.7 * n:
            tipe = "tanggal"
        elif n_angka >= 0.7 * n and (nol_depan + digit_panjang) < 0.3 * max(1, len(teks_str)) \
                and not ((POLA_KODE.search(nama) or POLA_KODE_AKHIR.search(nama.strip())
                          or POLA_KOLOM_PERIODE.match(rapikan_teks(nama).strip())) and angka_bulat):
            tipe = "angka"
        elif n_angka >= 0.7 * n:
            tipe = "kode"
        else:
            tipe = "teks"
        # v1.0.9 (B32): kolom NOMOR URUT berisi 1, 2, 3, … n berurutan dengan judul '#'/'No urut'/'Urutan', atau
        # kolom paling kiri tabel TANPA judul (Kolom1) = nomor baris, bukan besaran -> tidak dijumlah. (Judul
        # No/No./Nomor sudah dianggap kode oleh POLA_KODE.)
        if tipe == "angka" and not paksa and angka_bulat and n_angka == n >= 3:
            urut_ok = all(a is not None and a == angka[0] + t for t, a in enumerate(angka)) and angka[0] in (0, 1)
            if urut_ok and (rapikan_teks(nama).strip() in ("#", "No", "No.") or
                            re.match(r"^(no\.?\s*urut|urutan|nomor urut)$", rapikan_teks(nama).strip(), re.I)
                            or (self.kolom.index(nama) == 0 and len(self.kolom) >= 3
                                and re.match(r"^Kolom ?(\d+|[A-Z]{1,3})$", nama))):
                tipe = "kode"
                k["nomor_urut"] = True
        k["tipe"] = tipe
        nilai = [None] * len(mentah)
        if tipe == "tanggal":
            for (i, v), t in zip(isi, tgl):
                if t is None:
                    k["tidak_valid"].append((self.baris_no[i], v))
                nilai[i] = t
        elif tipe == "angka":
            for (i, v), a in zip(isi, angka):
                if a is None:
                    k["tidak_valid"].append((self.baris_no[i], v))
                nilai[i] = a
            raw_rp = sum(1 for v in teks_str if re.search(r"\b(rp|idr)", v, re.I))
            k["uang"] = bool((POLA_UANG.search(nama) and not POLA_BUKAN_UANG.search(nama))
                             or raw_rp >= 0.3 * max(1, len(teks_str)) and raw_rp > 0)
            k["persen"] = sum(1 for v in teks_str if rapikan_teks(v).endswith("%")) > len(teks_str) / 2 \
                if teks_str else False
        else:
            varian = {}
            for i, v in isi:
                if isinstance(v, date):
                    t = v.isoformat()
                elif isinstance(v, Decimal):
                    t = "{:f}".format(v)
                else:
                    t = rapikan_teks(v)
                kunci = kunci_kategori(t)
                varian.setdefault(kunci, Counter())[t] += 1
                nilai[i] = kunci
            tampil = {}
            for kunci, cnt in varian.items():
                tampil[kunci] = cnt.most_common(1)[0][0]
                if len(cnt) > 1:
                    k["gabung_kategori"].append((tampil[kunci], sorted(cnt)))
            nilai = [tampil[x] if x is not None else None for x in nilai]
        k["nilai"] = nilai
        return k

    # -- pencarian kolom ---------------------------------------------------
    def cari(self, nama, tipe=None, peran="kolom"):
        if nama is None:
            return None
        cf = rapikan_teks(nama).casefold()
        cocok = [n for n in self.kolom if n.casefold() == cf]
        if not cocok:
            cocok = [n for n in self.kolom if cf in n.casefold()]
        if len(cocok) != 1:
            alasan = "tidak ada" if not cocok else "cocok dengan lebih dari satu ({})".format(", ".join(cocok))
            label = peran[:1].upper() + peran[1:] if peran.startswith("kolom") else "Kolom {}".format(peran)
            raise InputError("{} '{}' {}. Kolom yang tersedia: {}.".format(
                label, nama, alasan, ", ".join(self.kolom)))
        n = cocok[0]
        if tipe and self.kol[n]["tipe"] not in tipe:
            raise InputError("Kolom '{}' bertipe {}, bukan {}. Bila isinya sebenarnya {}, tambahkan "
                             "--tipe \"{}={}\".".format(n, self.kol[n]["tipe"], "/".join(tipe),
                                                        tipe[0], n, tipe[0]))
        return n

    def kolom_tanggal_otomatis(self, nama=None):
        if nama:
            return self.cari(nama, ("tanggal",), "tanggal")
        tgl = [n for n, k in self.kol.items() if k["tipe"] == "tanggal"]
        if not tgl:
            raise InputError("Tidak ada kolom bertipe tanggal. Sebutkan dengan --tanggal \"Nama Kolom\". "
                             "Kolom yang tersedia: {}.".format(", ".join(self.kolom)))
        if len(tgl) > 1:
            self.catatan.append("Ada beberapa kolom tanggal ({}); dipakai '{}'. Pakai --tanggal untuk "
                                "memilih yang lain.".format(", ".join(tgl), tgl[0]))
        return tgl[0]

    def jenis_nilai(self, nama):
        if nama is None:
            return "bulat"
        k = self.kol[nama]
        if k.get("persen"):
            return "angka"
        return "uang" if k["uang"] else "angka"

    def terapkan_filter(self, filters, kol_tgl=None, dari=None, sampai=None):
        idx = list(range(len(self.mentah)))
        for f in filters or []:
            if "=" not in f:
                raise InputError("Format --filter harus \"Kolom=nilai\" (boleh beberapa nilai dipisah |).")
            kol, nilai = f.split("=", 1)
            n = self.cari(kol, peran="filter")
            k = self.kol[n]
            daftar = [rapikan_teks(x).casefold() for x in nilai.split("|")]
            if k["tipe"] in ("teks", "kode"):
                daftar_k = [kunci_kategori(x) for x in daftar]
                idx = [i for i in idx if k["nilai"][i] is not None and kunci_kategori(k["nilai"][i]) in daftar_k]
            elif k["tipe"] == "angka":
                target = [parse_angka(x) for x in daftar]
                idx = [i for i in idx if k["nilai"][i] is not None and k["nilai"][i] in target]
            else:
                target = [parse_tanggal(x) for x in daftar]
                idx = [i for i in idx if k["nilai"][i] in target]
            self.catatan.append("Filter: {} = {} ({} baris cocok).".format(n, nilai, len(idx)))
        if dari or sampai:
            kt = self.kolom_tanggal_otomatis(kol_tgl)
            a = parse_periode(dari)[0] if dari else date.min
            b = parse_periode(sampai)[1] if sampai else date.max
            nilai = self.kol[kt]["nilai"]
            idx = [i for i in idx if nilai[i] is not None and a <= nilai[i] <= b]
            self.catatan.append("Rentang tanggal ({}): {} s.d. {} ({} baris).".format(
                kt, fmt_tanggal(a) if dari else "awal", fmt_tanggal(b) if sampai else "akhir", len(idx)))
        if not idx:
            raise InputError("Tidak ada baris yang cocok dengan filter/rentang yang diminta.")
        return idx

    def peringatan_kolom(self, nama_list):
        """Peringatan untuk kolom yang dipakai dalam perhitungan."""
        out = []
        for n in nama_list:
            if not n:
                continue
            k = self.kol[n]
            if k["tidak_valid"]:
                contoh = "; ".join("baris {}: '{}'".format(r, v) for r, v in k["tidak_valid"][:4])
                if len(k["tidak_valid"]) > 4:
                    contoh += "; dll."
                out.append("Kolom '{}': {} nilai tidak bisa dibaca sebagai {} dan TIDAK dihitung ({}).".format(
                    n, len(k["tidak_valid"]), k["tipe"], contoh))
            if k.get("gaya_campur"):
                out.append("Kolom '{}' mencampur format angka Indonesia (1.234,5) dan Inggris (1,234.5); "
                           "dipakai format {}. Nilai yang bertentangan ditandai tidak valid.".format(
                               n, "Indonesia" if k["gaya"] == "id" else "Inggris"))
            if k["tipe"] == "tanggal" and k["urutan_ambigu"]:
                out.append("Tanggal di kolom '{}' ambigu (semua hari ≤ 12): dibaca hari/bulan/tahun "
                           "(format Indonesia). Bila file dari sistem AS (bulan/hari), jalankan ulang dengan "
                           "--urutan-tanggal mdy.".format(n))
            if k["tipe"] == "tanggal" and k["urutan"] == "mdy" and not self.urutan_paksa:
                out.append("Tanggal di kolom '{}' terdeteksi berformat bulan/hari/tahun (AS).".format(n))
            if k["gabung_kategori"]:
                contoh = "; ".join("{} ← {}".format(t, " / ".join(repr(x) for x in v))
                                   for t, v in k["gabung_kategori"][:4])
                if len(k["gabung_kategori"]) > 4:
                    contoh += "; dll."
                out.append("Kolom '{}': {} kategori yang penulisannya beda huruf besar-kecil/spasi digabung ({})."
                           .format(n, len(k["gabung_kategori"]), contoh))
        return out

    # -- peringatan tambahan untuk subperintah yang menghitung -----------
    def duplikat(self, idx=None):
        """Daftar (baris, baris_pertama) untuk baris yang persis sama dengan baris sebelumnya."""
        if idx is None:
            if self._dup is None:
                self._dup = self.duplikat(range(len(self.mentah)))
            return self._dup
        pertama, dup = {}, []
        for i in idx:
            key = tuple(rapikan_teks(v).casefold() if isinstance(v, str) else v for v in self.mentah[i])
            if key in pertama:
                dup.append((self.baris_no[i], pertama[key]))
            else:
                pertama[key] = self.baris_no[i]
        return dup

    def peringatan_duplikat(self, idx):
        dup = self.duplikat(idx)
        if not dup:
            return []
        return ["{} baris persis sama dengan baris lain (mis. baris {} = baris {}) dan TETAP ikut dihitung. "
                "Bila itu salah input ganda, jalankan 'bersihkan --buang-duplikat' lalu analisis file "
                "bersihnya.".format(len(dup), dup[0][0], dup[0][1])]

    def peringatan_nilai_kosong(self, nilai, idx):
        """Sel kosong di kolom nilai (baris tetap ada, tapi nilainya tidak dihitung)."""
        if not nilai:
            return [], 0
        k = self.kol[nilai]
        j = self.kolom.index(nilai)
        kosong = [self.baris_no[i] for i in idx if k["nilai"][i] is None and adalah_kosong(self.mentah[i][j])]
        tak_terhitung = sum(1 for i in idx if k["nilai"][i] is None)
        if not kosong:
            return [], tak_terhitung
        return ["Kolom '{}': {} baris tanpa nilai (sel kosong / rumus tanpa nilai / galat) TIDAK ikut dihitung "
                "(baris {}{}). Kolom 'Baris' = semua baris di kelompok; 'Nilai terisi' = baris yang angkanya "
                "dihitung (pembagi rata-rata).".format(nilai, len(kosong), ", ".join(map(str, kosong[:8])),
                                                       ", dll." if len(kosong) > 8 else "")], tak_terhitung

    def label_pribadi(self, n, teks):
        """Samarkan label dari kolom data pribadi (NIK, HP, email, rekening) kecuali --tampilkan-pribadi."""
        k = self.kol[n]
        if not k["sensitif"] or k["tipe"] not in ("teks", "kode") or teks is None or self.tampilkan_pribadi:
            return teks
        if n not in self.disamarkan:
            self.disamarkan.append(n)
        return samarkan(teks)

    def peringatan_privasi(self, nilai=None, per=None):
        out = []
        if self.disamarkan:
            out.append("Isi kolom {} DISAMARKAN (mis. 3201•••••••••408) karena data pribadi (UU PDP No. 27/2022). "
                       "Pengelompokan tetap memakai nilai lengkap. Pemilik data yang berhak boleh menambah "
                       "--tampilkan-pribadi; jangan bagikan hasilnya.".format(
                           ", ".join("'{}'".format(x) for x in self.disamarkan)))
        if self.tampilkan_pribadi and any(k["sensitif"] for k in self.kol.values()):
            out.append("--tampilkan-pribadi aktif: data pribadi ditampilkan LENGKAP. Hanya untuk pemilik data "
                       "yang berhak; jangan tempel/bagikan ke grup atau pihak lain (UU PDP No. 27/2022).")
        if nilai and self.kol[nilai]["sensitif"]:
            out.append("Kolom '{}' adalah data SENSITIF dan tabel ini menampilkannya per {}. Tunjukkan hanya ke "
                       "yang berhak; untuk laporan bersama pakai agregat (mis. per divisi/jabatan), bukan per "
                       "orang (UU PDP No. 27/2022).".format(nilai, per or "baris"))
        return out


# ---------------------------------------------------------------------------
# Statistik (Decimal)
# ---------------------------------------------------------------------------

def median(vals):
    s = sorted(vals)
    n = len(s)
    if n == 0:
        return None
    m = n // 2
    return s[m] if n % 2 else (s[m - 1] + s[m]) / 2


def kuartil_inc(vals, p):
    """Persentil inklusif, sama dengan Excel QUARTILE.INC / PERCENTILE.INC."""
    s = sorted(vals)
    if not s:
        return None
    h = (len(s) - 1) * p
    lo = int(h)
    frac = h - lo
    if lo + 1 >= len(s):
        return s[lo]
    return s[lo] + (s[lo + 1] - s[lo]) * frac


def agregasi(vals, fungsi):
    if fungsi == "hitung":
        return Decimal(len(vals))
    if not vals:
        return None
    if fungsi == "jumlah":
        return sum(vals, NOL)
    if fungsi == "rata":
        return sum(vals, NOL) / len(vals)
    if fungsi == "median":
        return median(vals)
    if fungsi == "min":
        return min(vals)
    if fungsi == "max":
        return max(vals)
    raise InputError("Fungsi '{}' tidak dikenal.".format(fungsi))


NAMA_FUNGSI = {"jumlah": "Jumlah", "rata": "Rata-rata", "median": "Median", "hitung": "Banyak baris",
               "min": "Minimum", "max": "Maksimum"}


def buat_judul_nilai(fungsi, nilai):
    """"Jumlah Total"; bila nama kolom = nama fungsi, hindari "Jumlah Jumlah" -> "Total kolom Jumlah"."""
    if not nilai:
        return NAMA_FUNGSI[fungsi]
    if kunci_kategori(nilai) == kunci_kategori(NAMA_FUNGSI[fungsi]):
        return "{} kolom {}".format("Total" if fungsi == "jumlah" else NAMA_FUNGSI[fungsi], nilai)
    return "{} {}".format(NAMA_FUNGSI[fungsi], nilai)


def outlier(vals_baris):
    """vals_baris: list (nilai, nomor_baris). Metode IQR 1,5x (QUARTILE.INC)."""
    vals = [v for v, _r in vals_baris]
    if len(vals) < 5:
        return None
    q1, q3 = kuartil_inc(vals, Decimal("0.25")), kuartil_inc(vals, Decimal("0.75"))
    iqr = q3 - q1
    bawah, atas = q1 - Decimal("1.5") * iqr, q3 + Decimal("1.5") * iqr
    luar = [(v, r) for v, r in vals_baris if v < bawah or v > atas]
    return {"q1": q1, "q3": q3, "batas_bawah": bawah, "batas_atas": atas, "jumlah": len(luar),
            "contoh": sorted(luar, key=lambda x: -abs(x[0] - (q1 + q3) / 2))[:5]}


# ---------------------------------------------------------------------------
# Periode
# ---------------------------------------------------------------------------

def akhir_bulan(y, m):
    return (date(y + (m == 12), m % 12 + 1, 1) - timedelta(days=1))


def parse_periode(teks):
    """'2026-09', '2026', 'Sep 2026', 'Q3 2026', '2026-09-01..2026-09-15', '25/09/2026' -> (awal, akhir)."""
    if teks is None:
        raise InputError("Periode kosong.")
    t = rapikan_teks(teks).lower()
    if ".." in t:
        a, b = t.split("..", 1)
        da, db = parse_tanggal(a.strip()), parse_tanggal(b.strip())
        if not da or not db or da > db:
            raise InputError("Rentang '{}' tidak valid. Contoh: 2026-09-01..2026-09-15".format(teks))
        return da, db
    m = re.fullmatch(r"(\d{4})-(\d{1,2})", t) or re.fullmatch(r"(\d{1,2})/(\d{4})", t)
    if m:
        g = m.groups()
        y, bl = (int(g[0]), int(g[1])) if len(g[0]) == 4 else (int(g[1]), int(g[0]))
        if 1 <= bl <= 12:
            return date(y, bl, 1), akhir_bulan(y, bl)
    m = re.fullmatch(r"(\d{4})", t)
    if m:
        y = int(t)
        return date(y, 1, 1), date(y, 12, 31)
    m = re.fullmatch(r"([a-z]+)\.?\s*(\d{4})", t)
    if m and BULAN.get(m.group(1)):
        y, bl = int(m.group(2)), BULAN[m.group(1)]
        return date(y, bl, 1), akhir_bulan(y, bl)
    m = re.fullmatch(r"q([1-4])[\s\-/]*(\d{4})", t) or re.fullmatch(r"(\d{4})[\s\-/]*q([1-4])", t)
    if m:
        a, b = m.groups()
        q, y = (int(a), int(b)) if len(a) == 1 else (int(b), int(a))
        return date(y, 3 * q - 2, 1), akhir_bulan(y, 3 * q)
    d = parse_tanggal(t)
    if d:
        return d, d
    raise InputError("Periode '{}' tidak dikenali. Contoh: 2026-09, Sep 2026, 2026, Q3 2026, "
                     "2026-09-01..2026-09-15.".format(teks))


def kunci_periode(d, per):
    if per == "hari":
        return d
    if per == "minggu":
        return d - timedelta(days=d.weekday())
    if per == "bulan":
        return date(d.year, d.month, 1)
    if per == "kuartal":
        return date(d.year, 3 * ((d.month - 1) // 3) + 1, 1)
    return date(d.year, 1, 1)


def langkah_periode(d, per):
    if per == "hari":
        return d + timedelta(days=1)
    if per == "minggu":
        return d + timedelta(days=7)
    bulan = {"bulan": 1, "kuartal": 3, "tahun": 12}[per]
    m = d.month - 1 + bulan
    return date(d.year + m // 12, m % 12 + 1, 1)


def label_periode(d, per):
    if per == "hari":
        return fmt_tanggal(d)
    if per == "minggu":
        return "Minggu {}".format(fmt_tanggal(d))
    if per == "bulan":
        return "{} {}".format(NAMA_BULAN[d.month], d.year)
    if per == "kuartal":
        return "Q{} {}".format((d.month - 1) // 3 + 1, d.year)
    return str(d.year)


def akhir_periode(d, per):
    return langkah_periode(d, per) - timedelta(days=1)


# ---------------------------------------------------------------------------
# Subperintah
# ---------------------------------------------------------------------------

def hasil_dasar(data, perintah, judul):
    info = data.info
    if info.get("gabungan"):
        sumber = info["file"] + " — gabungan sheet " + info["sheet"]
    else:
        sumber = info["file"] + (" — sheet '{}'".format(info["sheet"]) if info.get("sheet") else "")
    return {"perintah": perintah, "judul": judul, "sumber": sumber,
            "jumlah_baris_data": len(data.mentah), "baris_header": data.baris_header,
            "tabel": [], "temuan": [], "saran_grafik": "", "peringatan": list(data.peringatan),
            "catatan": list(data.catatan),
            "baris_dikeluarkan": [{"baris": r, "alasan": a, "isi": t} for r, a, t in data.dikeluarkan],
            "kemungkinan_ringkasan": [{"baris": r, "alasan": a, "isi": t} for r, a, t in data.kandidat],
            "total_alternatif": data.total_alternatif, "cek_silang_total": data.cek_silang}


def tabel(judul, kolom, jenis, baris):
    return {"judul": judul, "kolom": kolom, "jenis": jenis, "baris": baris}


def cmd_daftar(args):
    sheet = None if _minta_banyak_sheet(args.file, args.sheet) else args.sheet
    grid, info = baca_grid(args.file, sheet, args.pemisah, args.encoding, args.paksa)
    h = {"perintah": "daftar", "judul": "Isi file " + info["file"], "sumber": info["file"], "tabel": [],
         "temuan": [], "saran_grafik": "", "peringatan": info.get("peringatan", []), "catatan": []}
    if info["format"] == "xlsx":
        buku = BukuXlsx(args.file)
        rows = []
        for i, s in enumerate(buku.sheets, 1):
            try:
                g = buku.baca_sheet(s)
                jml = len(g)
            except InputError:
                jml = None
            rows.append([Decimal(i), s["nama"], "tersembunyi" if s["status"] != "visible" else "terlihat",
                         Decimal(jml) if jml is not None else None])
        h["tabel"].append(tabel("Sheet di workbook", ["No", "Sheet", "Status", "Baris berisi"],
                                ["bulat", "teks", "teks", "bulat"], rows))
        h["temuan"].append("Workbook berisi {} sheet. Tanpa --sheet, yang dianalisis: '{}'.".format(
            len(buku.sheets), info["sheet"]))
    else:
        h["temuan"].append("CSV dibaca dengan encoding {} dan pemisah {}; {} baris berisi.".format(
            info["encoding"], info["pemisah"], len(grid)))
    try:
        d = Data(grid, info, args.baris_header, args.pertahankan_total, args.urutan_tanggal, parse_tipe(args.tipe),
                 buang=_baris_untuk_sheet(parse_daftar_baris(args.buang_baris, "--buang-baris"), None, False),
                 pertahankan=_baris_untuk_sheet(parse_daftar_baris(args.pertahankan_baris, "--pertahankan-baris"),
                                                None, False))
        h["temuan"].append("Judul kolom di baris {}: {}.".format(d.baris_header, ", ".join(d.kolom)) if d.baris_header
                           else "Tanpa baris judul kolom; nama kolom: {}.".format(", ".join(d.kolom)))
        h["catatan"] += d.catatan
    except InputError as e:
        h["peringatan"].append(str(e))
    return h


def _tabel_cek_baris(data, n=5, maks_kolom=8, maks_sel=24):
    kolom = data.kolom[:maks_kolom]
    tersembunyi = {k for k in kolom if data.kol[k]["sensitif"] and not data.tampilkan_pribadi}

    def sel(v, k):
        if adalah_kosong(v):
            return ""
        if k in tersembunyi:
            return "(disembunyikan)"
        if isinstance(v, Decimal):
            t = fmt_angka(v)
        elif isinstance(v, date):
            t = fmt_tanggal(v)
        else:
            t = rapikan_teks(v).replace("\n", " ")
        return t if len(t) <= maks_sel else t[:maks_sel - 1] + "…"
    m = len(data.mentah)
    posisi = list(range(m)) if m <= 2 * n else list(range(n)) + [None] + list(range(m - n, m))
    rows = []
    for p in posisi:
        if p is None:
            rows.append(["…"] + ["({} baris lain)".format(fmt_angka(Decimal(m - 2 * n)))] + [""] * (len(kolom) - 1))
            continue
        rows.append([str(data.baris_no[p])] + [sel(data.mentah[p][j], k) for j, k in enumerate(kolom)])
    judul = ("Cek sekilas: baris data yang DIPAKAI ({}{}) — ada baris total/rekap/tabel lain yang ikut?".format(
        "semua {} baris".format(m) if m <= 2 * n else "{} pertama & {} terakhir".format(n, n),
        "; kolom ke-{} dst. tidak ditampilkan".format(len(kolom) + 1) if len(data.kolom) > maks_kolom else ""))
    hasil = [tabel(judul, ["Baris"] + kolom, ["teks"] * (len(kolom) + 1), rows)]
    for judul, daftar in (("Baris DIKELUARKAN dari perhitungan (bukan data)", data.dikeluarkan),
                          ("Kemungkinan baris ringkasan (TETAP dihitung — konfirmasi ke pengguna)", data.kandidat)):
        b = [[str(r), al, isi] for r, al, isi in daftar[:20]]
        if len(daftar) > 20:
            b.append(["…", "dan {} baris lainnya".format(len(daftar) - 20), ""])
        hasil.append(tabel(judul, ["Baris", "Alasan", "Isi"], ["teks"] * 3, b))
    return hasil


def cmd_profil(args, data):
    h = hasil_dasar(data, "profil", "Profil data")
    rows = []
    for n, k in data.kol.items():
        total = k["terisi"] + k["kosong"]
        unik = len(set(v for v in k["nilai"] if v is not None))
        if k["sensitif"]:
            contoh = "(disembunyikan: data pribadi)"
        else:
            contoh_v = []
            for v in k["nilai"]:
                if v is not None and v not in contoh_v:
                    contoh_v.append(v)
                if len(contoh_v) == 3:
                    break
            jenis = data.jenis_nilai(n) if k["tipe"] == "angka" else None
            contoh = ", ".join(fmt_sel(v, jenis) if jenis else (fmt_tanggal(v) if isinstance(v, date) else str(v))
                               for v in contoh_v)
        rows.append([n, k["tipe"] + (" (uang)" if k["uang"] else ""), Decimal(k["terisi"]), Decimal(k["kosong"]),
                     Decimal(k["kosong"]) / total * SERATUS if total else None, Decimal(unik),
                     Decimal(len(k["tidak_valid"])), contoh[:80]])
    h["tabel"].append(tabel("Kolom", ["Kolom", "Tipe", "Terisi", "Kosong", "% kosong", "Nilai unik",
                                      "Tidak valid", "Contoh"],
                            ["teks", "teks", "bulat", "bulat", "persen", "bulat", "bulat", "teks"], rows))
    # duplikat
    kunci = Counter()
    pertama = {}
    dup_baris = []
    for r, row in zip(data.baris_no, data.mentah):
        key = tuple(rapikan_teks(v).casefold() if isinstance(v, str) else v for v in row)
        kunci[key] += 1
        if kunci[key] > 1:
            dup_baris.append((r, pertama[key]))
        else:
            pertama[key] = r
    h["duplikat"] = len(dup_baris)
    # outlier
    out_rows = []
    for n, k in data.kol.items():
        if k["tipe"] != "angka":
            continue
        o = outlier([(v, r) for v, r in zip(k["nilai"], data.baris_no) if v is not None])
        if not o:
            continue
        jenis = data.jenis_nilai(n)
        out_rows.append([n, fmt_sel(o["batas_bawah"], jenis) + " s.d. " + fmt_sel(o["batas_atas"], jenis),
                         Decimal(o["jumlah"]),
                         "; ".join("baris {}: {}".format(r, fmt_sel(v, jenis)) for v, r in o["contoh"]) or "-"])
    if out_rows:
        h["tabel"].append(tabel("Nilai ekstrem (outlier, metode IQR 1,5×)",
                                ["Kolom", "Rentang wajar", "Jumlah outlier", "Contoh (terjauh)"],
                                ["teks", "teks", "bulat", "teks"], out_rows))
    # v1.0.7 — PENGAMAN AGENT: tampilkan baris yang DIPAKAI (5 pertama & 5 terakhir), baris yang dikeluarkan,
    # dan kandidat ringkasan, agar baris total/rekap/tabel lain yang terlewat deteksi terlihat sekilas.
    h["tabel"] += _tabel_cek_baris(data)
    t = h["temuan"]
    t.append("{} baris data × {} kolom ({}).".format(
        fmt_angka(Decimal(len(data.mentah))), len(data.kolom), "judul kolom di baris {}".format(data.baris_header)
        if data.baris_header else "TANPA baris judul kolom — nama kolom Kolom1, Kolom2, … dibuat script"))
    tipe = Counter(k["tipe"] for k in data.kol.values())
    t.append("Tipe kolom: " + ", ".join("{} {}".format(v, k) for k, v in tipe.most_common()) + ".")
    if dup_baris:
        t.append("{} baris persis sama dengan baris lain (mis. baris {} = baris {}). Periksa apakah data "
                 "terinput dua kali.".format(len(dup_baris), dup_baris[0][0], dup_baris[0][1]))
    else:
        t.append("Tidak ada baris yang persis sama (duplikat).")
    banyak_kosong = [n for n, k in data.kol.items() if k["terisi"] + k["kosong"] and
                     k["kosong"] / (k["terisi"] + k["kosong"]) >= 0.2]
    if banyak_kosong:
        t.append("Kolom dengan ≥ 20% sel kosong: {}.".format(", ".join(banyak_kosong)))
    for r in out_rows:
        if not r[2]:
            continue
        t.append("Kolom '{}' punya {} nilai di luar rentang wajar {} — cek salah ketik atau transaksi "
                 "khusus.".format(r[0], r[2], r[1]))
    h["peringatan"] += data.peringatan_kolom(data.kolom)
    if any(k["tipe"] == "angka" for k in data.kol.values()):
        h["saran_grafik"] = ("Histogram untuk melihat sebaran kolom angka; box plot untuk menandai outlier. "
                             "Untuk laporan, lanjutkan dengan 'ringkas', 'pivot', atau 'tren'.")
    else:
        h["saran_grafik"] = ("Tidak ada kolom angka; untuk kolom kategori pakai 'pivot --grup <kolom>' (hitung "
                             "banyak baris) lalu grafik batang.")
    return h


def cmd_ringkas(args, data):
    h = hasil_dasar(data, "ringkas", "Ringkasan statistik")
    idx = data.terapkan_filter(args.filter, args.tanggal, args.dari, args.sampai)
    h["catatan"] = list(data.catatan)
    if args.kolom:
        daftar = [data.cari(x) for x in args.kolom]
    else:
        daftar = list(data.kolom)
    rows, catatan_median = [], []
    for n in daftar:
        k = data.kol[n]
        if k["tipe"] != "angka":
            continue
        vals = [k["nilai"][i] for i in idx if k["nilai"][i] is not None]
        j = data.jenis_nilai(n)
        rows.append([n, Decimal(len(vals)), agregasi(vals, "jumlah"), agregasi(vals, "rata"),
                     agregasi(vals, "median"), agregasi(vals, "min"), agregasi(vals, "max"), j])
        if vals:
            rata, med = agregasi(vals, "rata"), agregasi(vals, "median")
            if len(vals) >= 8 and med and med > 0 and abs(rata - med) / med > Decimal("0.2"):
                catatan_median.append(
                    "'{}': rata-rata {} jauh dari median {} — ada beberapa nilai sangat besar/kecil; "
                    "median lebih mewakili nilai 'biasa'.".format(n, fmt_sel(rata, j), fmt_sel(med, j)))
            h["temuan"].append("'{}': total {} dari {} baris, rata-rata {} per baris (terkecil {}, "
                                  "terbesar {}).".format(n, fmt_sel(agregasi(vals, "jumlah"), j),
                                                         fmt_angka(Decimal(len(vals))), fmt_sel(rata, j),
                                                         fmt_sel(min(vals), j), fmt_sel(max(vals), j)))
    h["temuan"] += catatan_median
    if rows:
        # format per baris berbeda (uang/angka): tabel memakai jenis per baris
        h["tabel"].append({"judul": "Kolom angka", "kolom": ["Kolom", "Terisi", "Jumlah", "Rata-rata",
                                                             "Median", "Min", "Max"],
                           "jenis": ["teks", "bulat", "*", "*", "*", "*", "*"],
                           "baris": [r[:7] for r in rows], "jenis_baris": [r[7] for r in rows]})
    trows = []
    for n in daftar:
        k = data.kol[n]
        if k["tipe"] == "tanggal":
            vals = [k["nilai"][i] for i in idx if k["nilai"][i] is not None]
            if vals:
                a, b = min(vals), max(vals)
                trows.append([n, fmt_tanggal(a), fmt_tanggal(b), Decimal((b - a).days + 1),
                              Decimal(len(set(vals)))])
    if trows:
        h["tabel"].append(tabel("Kolom tanggal", ["Kolom", "Awal", "Akhir", "Rentang (hari)", "Hari berisi data"],
                                ["teks", "teks", "teks", "bulat", "bulat"], trows))
        h["temuan"].append("Data mencakup {} s.d. {}.".format(trows[0][1], trows[0][2]))
    krows = []
    for n in daftar:
        k = data.kol[n]
        if k["tipe"] in ("teks", "kode") and not k["sensitif"]:
            vals = [k["nilai"][i] for i in idx if k["nilai"][i] is not None]
            if not vals:
                continue
            c = Counter(vals)
            krows.append([n, Decimal(len(c)), ", ".join("{} ({})".format(x, y) for x, y in c.most_common(3))])
    if krows:
        h["tabel"].append(tabel("Kolom teks/kategori", ["Kolom", "Nilai unik", "3 terbanyak (jumlah baris)"],
                                ["teks", "bulat", "teks"], krows))
    if not rows and not trows and not krows:
        raise InputError("Tidak ada kolom yang bisa diringkas.")
    h["peringatan"] += data.peringatan_kolom(daftar) + data.peringatan_duplikat(idx)
    h["saran_grafik"] = ("Kartu angka (KPI) untuk total & rata-rata; bila ingin melihat pembagian per "
                         "kategori, lanjutkan dengan 'pivot'.")
    return h


def _kunci_grup(data, n, i, per):
    k = data.kol[n]
    v = k["nilai"][i]
    if k["tipe"] == "tanggal":
        return kunci_periode(v, per) if v is not None else None
    if k["tipe"] == "angka":
        return v
    return v


def _label_grup(data, n, key, per):
    if key is None:
        return "(kosong)"
    if data.kol[n]["tipe"] == "tanggal":
        return label_periode(key, per)
    if isinstance(key, Decimal):
        return fmt_angka(key)
    return data.label_pribadi(n, str(key))


def _kunci_urut_teks(keys):
    """Fungsi urut untuk kunci teks: nama bulan (Juli, Agustus, ...) diurut kronologis, lainnya abjad."""
    isi = [k for k in keys if k is not None]
    if isi and all(isinstance(k, str) and rapikan_teks(k).casefold().rstrip(".") in BULAN for k in isi):
        return lambda x: (x is None, BULAN[rapikan_teks(x).casefold().rstrip(".")] if x is not None else 0, "")
    if isi and all(isinstance(k, str) and rapikan_teks(k).isdigit() for k in isi):   # kode/periode 1, 2, …, 10
        return lambda x: (x is None, int(rapikan_teks(x)) if x is not None else 0, "")
    return lambda x: (x is None, 0, str(x).casefold() if not isinstance(x, (date, Decimal)) else x)


def _sisip_terisi(rows, header, jenis_k, pos, terisi):
    """Sisipkan kolom 'Nilai terisi' (list terisi sejajar rows) di posisi pos (di akhir agar indeks kolom
    lain tetap sama untuk pembaca JSON/CSV)."""
    header.insert(pos, "Nilai terisi")
    jenis_k.insert(pos, "bulat")
    for row, t in zip(rows, terisi):
        row.insert(pos, t)


def _siapkan_nilai(data, args):
    nilai = data.cari(args.nilai, ("angka",), "nilai") if args.nilai else None
    fungsi = args.fungsi or ("jumlah" if nilai else "hitung")
    if fungsi != "hitung" and not nilai:
        raise InputError("Fungsi '{}' butuh --nilai \"Kolom Angka\".".format(fungsi))
    return nilai, fungsi


def _jenis_hasil(data, nilai, fungsi):
    if fungsi == "hitung":
        return "bulat"
    return data.jenis_nilai(nilai)


def _vals(data, nilai, idx_list):
    if not nilai:
        return [Decimal(1)] * len(idx_list)
    k = data.kol[nilai]
    return [k["nilai"][i] for i in idx_list if k["nilai"][i] is not None]


def cmd_pivot(args, data):
    idx = data.terapkan_filter(args.filter, args.tanggal, args.dari, args.sampai)
    grup = data.cari(args.grup, peran="grup")
    nilai, fungsi = _siapkan_nilai(data, args)
    per = args.per or "bulan"
    kolom2 = data.cari(args.kolom_pivot, peran="kolom pivot") if args.kolom_pivot else None
    jenis = _jenis_hasil(data, nilai, fungsi)
    judul_nilai = buat_judul_nilai(fungsi, nilai)
    h = hasil_dasar(data, "pivot", "{} per {}".format(judul_nilai, grup +
                                                     (" ({})".format(per) if data.kol[grup]["tipe"] == "tanggal" else "")))
    h["catatan"] = list(data.catatan)
    kelompok = OrderedDict()
    for i in idx:
        kelompok.setdefault(_kunci_grup(data, grup, i, per), []).append(i)
    if data.kol[grup]["tipe"] == "tanggal" or data.kol[grup]["tipe"] == "angka":
        urut_nama = sorted(kelompok, key=lambda x: (x is None, x if x is not None else 0))
    else:
        urut_nama = sorted(kelompok, key=_kunci_urut_teks(kelompok))
    semua_vals = _vals(data, nilai, idx)
    total = agregasi(semua_vals, fungsi)
    bisa_persen = fungsi in ("jumlah", "hitung") and all(v >= 0 for v in semua_vals) and total and total > 0
    pesan_kosong, tak_terhitung = data.peringatan_nilai_kosong(nilai, idx)
    if kolom2:
        sub = OrderedDict()
        for i in idx:
            sub.setdefault(_kunci_grup(data, kolom2, i, per), None)
        if data.kol[kolom2]["tipe"] in ("tanggal", "angka"):
            subkeys = sorted(sub, key=lambda x: (x is None, x if x is not None else 0))
        else:
            subkeys = sorted(sub, key=_kunci_urut_teks(sub))
        if len(subkeys) > BATAS_KOLOM_PIVOT:
            raise InputError("Kolom pivot '{}' punya {} nilai berbeda (maks. {}). Pilih kolom lain atau "
                             "saring dengan --filter.".format(kolom2, len(subkeys), BATAS_KOLOM_PIVOT))
        header = [grup] + [_label_grup(data, kolom2, s, per) for s in subkeys] + ["Total"]
        rows = []
        for g in urut_nama:
            ig = kelompok[g]
            row = [_label_grup(data, grup, g, per)]
            for s in subkeys:
                isub = [i for i in ig if _kunci_grup(data, kolom2, i, per) == s]
                row.append(agregasi(_vals(data, nilai, isub), fungsi) if isub else None)
            row.append(agregasi(_vals(data, nilai, ig), fungsi))
            rows.append(row)
        tot = ["TOTAL"] + [agregasi(_vals(data, nilai, [i for i in idx if _kunci_grup(data, kolom2, i, per) == s]),
                                    fungsi) for s in subkeys] + [total]
        rows.append(tot)
        h["tabel"].append(tabel(h["judul"] + " × " + kolom2, header, ["teks"] + [jenis] * (len(header) - 1), rows))
        h["saran_grafik"] = ("Grafik batang berkelompok (clustered bar): sumbu = {}, warna = {}. Alternatif: "
                             "tabel dengan pewarnaan bersyarat (heatmap) di Excel.".format(grup, kolom2))
    else:
        rows, terisi = [], []
        for g in urut_nama:
            ig = kelompok[g]
            vs = _vals(data, nilai, ig)
            v = agregasi(vs, fungsi)
            row = [_label_grup(data, grup, g, per), Decimal(len(ig)), v]
            if bisa_persen:
                row.append(v / total * SERATUS if v is not None else None)
            rows.append(row)
            terisi.append(Decimal(len(vs)))
        if args.urut == "nilai" or (args.urut is None and data.kol[grup]["tipe"] not in ("tanggal", "angka")):
            urutan = sorted(range(len(rows)), key=lambda j: (rows[j][2] is None, -(rows[j][2] or 0)))
            rows, terisi = [rows[j] for j in urutan], [terisi[j] for j in urutan]
        header = [grup, "Baris", judul_nilai] + (["% dari total"] if bisa_persen else [])
        jenis_k = ["teks", "bulat", jenis] + (["persen"] if bisa_persen else [])
        if args.n:
            rows, terisi = rows[:args.n], terisi[:args.n]
        tot = ["TOTAL", Decimal(len(idx)), total] + ([SERATUS] if bisa_persen else [])
        if nilai and tak_terhitung:
            tabel_rows = [list(r) for r in rows] + [list(tot)]
            _sisip_terisi(tabel_rows, header, jenis_k, len(header), terisi + [Decimal(len(semua_vals))])
        else:
            tabel_rows = rows + [tot]
        h["tabel"].append(tabel(h["judul"], header, jenis_k, tabel_rows))
        if fungsi in ("jumlah", "hitung") and not bisa_persen and any(v < 0 for v in semua_vals):
            h["catatan"].append("Kolom '% dari total' tidak ditampilkan karena ada nilai negatif (mis. retur/"
                                "koreksi), sehingga persen bagian tidak bermakna.")
        valid = [r for r in rows if r[2] is not None]
        if valid:
            atas = max(valid, key=lambda r: r[2])
            bawah = min(valid, key=lambda r: r[2])
            teks = "Tertinggi: {} ({}{}).".format(atas[0], fmt_sel(atas[2], jenis),
                                                  ", " + fmt_persen(atas[3]) + " dari total" if bisa_persen else "")
            h["temuan"].append(teks)
            if len(valid) > 1:
                h["temuan"].append("Terendah: {} ({}{}).".format(
                    bawah[0], fmt_sel(bawah[2], jenis),
                    ", " + fmt_persen(bawah[3]) + " dari total" if bisa_persen else ""))
            h["temuan"].append("{} kelompok; {} keseluruhan: {}.".format(
                len(kelompok), judul_nilai.lower(), fmt_sel(total, jenis)))
        n = len(rows)
        if data.kol[grup]["tipe"] == "tanggal":
            h["saran_grafik"] = "Grafik garis (line chart) atau batang vertikal, urut waktu dari kiri ke kanan."
        elif bisa_persen and n <= 5:
            h["saran_grafik"] = ("Grafik batang horizontal urut terbesar. Pie/donat boleh karena ≤ 5 bagian "
                                 "dari satu total, tapi batang tetap lebih mudah dibandingkan.")
        elif n <= 15:
            h["saran_grafik"] = "Grafik batang horizontal, urut dari terbesar ke terkecil."
        else:
            h["saran_grafik"] = ("Grafik batang horizontal untuk 10 teratas saja; sisanya digabung 'Lainnya' "
                                 "(pakai subperintah 'top').")
    h["peringatan"] += data.peringatan_kolom([grup, nilai, kolom2])
    h["peringatan"] += pesan_kosong + data.peringatan_duplikat(idx) + data.peringatan_privasi(nilai, grup)
    return h


def cmd_tren(args, data):
    idx = data.terapkan_filter(args.filter, args.tanggal, args.dari, args.sampai)
    kt = data.kolom_tanggal_otomatis(args.tanggal)
    nilai, fungsi = _siapkan_nilai(data, args)
    per = args.per or "bulan"
    jenis = _jenis_hasil(data, nilai, fungsi)
    judul_nilai = buat_judul_nilai(fungsi, nilai)
    h = hasil_dasar(data, "tren", "Tren {} per {}".format(judul_nilai, per))
    h["catatan"] = list(data.catatan)
    tg = data.kol[kt]["nilai"]
    idx_t = [i for i in idx if tg[i] is not None]
    tanpa_tgl = len(idx) - len(idx_t)
    if not idx_t:
        raise InputError("Kolom '{}' tidak berisi tanggal yang terbaca.".format(kt))
    kelompok = {}
    for i in idx_t:
        kelompok.setdefault(kunci_periode(tg[i], per), []).append(i)
    awal, akhir = min(kelompok), max(kelompok)
    if per == "hari" and (akhir - awal).days > 400:
        raise InputError("Rentang lebih dari 400 hari; pakai --per minggu/bulan.")
    rows, seri = [], []
    p = awal
    sebelumnya = None
    while p <= akhir:
        ig = kelompok.get(p, [])
        v = agregasi(_vals(data, nilai, ig), fungsi) if ig else (NOL if fungsi in ("jumlah", "hitung") else None)
        ubah = (persen_ubah(sebelumnya, v) if sebelumnya is not None and v is not None and ig
                and seri and seri[-1][2] > 0 else None)
        rows.append([label_periode(p, per), Decimal(len(ig)), v, ubah])
        seri.append((p, v, len(ig)))
        sebelumnya = v
        p = langkah_periode(p, per)
    h["tabel"].append(tabel(h["judul"], ["Periode", "Baris", judul_nilai, "Perubahan vs periode sebelumnya"],
                            ["teks", "bulat", jenis, "persen"], rows))
    kosong = [label_periode(p, per) for p, _v, c in seri if c == 0]
    if kosong:
        h["catatan"].append("Periode tanpa data (ditulis {}): {}.".format(
            "0" if fungsi in ("jumlah", "hitung") else "-", ", ".join(kosong[:10])))
    valid = [(p, v) for p, v, c in seri if v is not None and c > 0]
    t = h["temuan"]
    if valid:
        atas = max(valid, key=lambda x: x[1])
        bawah = min(valid, key=lambda x: x[1])
        t.append("Tertinggi: {} ({}). Terendah: {} ({}).".format(
            label_periode(atas[0], per), fmt_sel(atas[1], jenis), label_periode(bawah[0], per),
            fmt_sel(bawah[1], jenis)))
        if len(valid) >= 2:
            t.append("Dari {} ke {}: {}.".format(label_periode(valid[0][0], per), label_periode(valid[-1][0], per),
                                                 kalimat_ubah(valid[0][1], valid[-1][1], lambda x: fmt_sel(x, jenis))))
            # periode tanpa data (mis. sheet bulan kosong) bukan "penurunan -100%": abaikan di kenaikan/penurunan
            naik = [(rows[j][0], rows[j][3]) for j in range(1, len(rows))
                    if rows[j][3] is not None and seri[j][2] > 0 and seri[j - 1][2] > 0]
            if naik:
                mx = max(naik, key=lambda x: x[1])
                mn = min(naik, key=lambda x: x[1])
                if mx[1] > 0:
                    t.append("Kenaikan terbesar: {} ({}).".format(mx[0], "+" + fmt_persen(mx[1])))
                if mn[1] < 0:
                    t.append("Penurunan terbesar: {} ({}).".format(mn[0], fmt_persen(mn[1])))
        if fungsi in ("jumlah", "hitung") and per != "hari":
            t.append("Rata-rata per {}: {}.".format(per, fmt_sel(
                sum((v for _p, v, _c in seri), NOL) / len(seri), jenis)))
    # periode tidak penuh
    tmin = min(tg[i] for i in idx_t)
    tmax = max(tg[i] for i in idx_t)
    if per != "hari":
        if tmin != kunci_periode(tmin, per):
            h["peringatan"].append("{} tidak penuh: data baru mulai {}. Jangan dibandingkan langsung dengan "
                                   "periode penuh.".format(label_periode(kunci_periode(tmin, per), per), fmt_tanggal(tmin)))
        if tmax != akhir_periode(kunci_periode(tmax, per), per):
            h["peringatan"].append("{} tidak penuh: data terakhir {}. Jangan dibandingkan langsung dengan "
                                   "periode penuh.".format(label_periode(kunci_periode(tmax, per), per), fmt_tanggal(tmax)))
    if tanpa_tgl:
        h["peringatan"].append("{} baris tanpa tanggal terbaca tidak masuk tren.".format(tanpa_tgl))
    h["peringatan"] += data.peringatan_kolom([kt, nilai])
    h["peringatan"] += data.peringatan_nilai_kosong(nilai, idx_t)[0] + data.peringatan_duplikat(idx)
    h["saran_grafik"] = ("Grafik garis (line chart): sumbu X = {}, sumbu Y = {}. Di Excel: blok tabel → "
                         "Insert → Line.".format(per, judul_nilai))
    return h


def cmd_top(args, data):
    idx = data.terapkan_filter(args.filter, args.tanggal, args.dari, args.sampai)
    nilai, fungsi = _siapkan_nilai(data, args)
    n = args.n or 10
    jenis = _jenis_hasil(data, nilai, fungsi)
    arah = "Terbawah" if args.terbawah else "Teratas"
    if args.grup:
        grup = data.cari(args.grup, peran="grup")
        judul_nilai = buat_judul_nilai(fungsi, nilai)
        h = hasil_dasar(data, "top", "{} {} {} menurut {}".format(n, arah.lower(), grup, judul_nilai))
        h["catatan"] = list(data.catatan)
        kel = OrderedDict()
        per = args.per or "bulan"
        for i in idx:
            kel.setdefault(_kunci_grup(data, grup, i, per), []).append(i)
        daftar = [(g, agregasi(_vals(data, nilai, ig), fungsi), len(ig), len(_vals(data, nilai, ig)))
                  for g, ig in kel.items()]
        daftar = [x for x in daftar if x[1] is not None]
        daftar.sort(key=lambda x: x[1], reverse=not args.terbawah)
        total = agregasi(_vals(data, nilai, idx), fungsi)
        bisa_persen = fungsi in ("jumlah", "hitung") and total and total > 0 and all(x[1] >= 0 for x in daftar)
        rows, kum = [], NOL
        for no, (g, v, c, _t) in enumerate(daftar[:n], 1):
            kum += v
            row = [Decimal(no), _label_grup(data, grup, g, per), Decimal(c), v]
            if bisa_persen:
                row += [v / total * SERATUS, kum / total * SERATUS]
            rows.append(row)
        if bisa_persen and len(daftar) > n:
            sisa = sum((x[1] for x in daftar[n:]), NOL)
            rows.append([None, "Lainnya ({} {})".format(len(daftar) - n, grup), Decimal(sum(x[2] for x in daftar[n:])),
                         sisa, sisa / total * SERATUS, None])
        header = ["#", grup, "Baris", judul_nilai] + (["% dari total", "% kumulatif"] if bisa_persen else [])
        jenis_k = ["bulat", "teks", "bulat", jenis] + (["persen", "persen"] if bisa_persen else [])
        pesan_kosong, tak_terhitung = data.peringatan_nilai_kosong(nilai, idx)
        if nilai and tak_terhitung:
            terisi = [Decimal(x[3]) for x in daftar[:n]]
            if len(rows) > len(terisi):
                terisi.append(Decimal(sum(x[3] for x in daftar[n:])))
            tabel_rows = [list(r) for r in rows]
            _sisip_terisi(tabel_rows, header, jenis_k, len(header), terisi)
        else:
            tabel_rows = rows
        h["tabel"].append(tabel(h["judul"], header, jenis_k, tabel_rows))
        if rows and bisa_persen and not args.terbawah:
            k80 = next((r for r in rows if r[5] is not None and r[5] >= 80), None)
            h["temuan"].append("{} teratas ({}) menyumbang {} dari total {}.".format(
                min(n, len(daftar)), ", ".join(r[1] for r in rows[:3]) + ("..." if len(rows) > 3 else ""),
                fmt_persen(rows[min(n, len(daftar)) - 1][5]), fmt_sel(total, jenis)))
            if k80:
                h["temuan"].append("{} dari {} {} sudah mencakup ≥ 80% total (pola Pareto).".format(
                    int(k80[0]), len(daftar), grup))
        elif rows:
            h["temuan"].append("{} {}: {} ({}).".format(arah, grup, rows[0][1], fmt_sel(rows[0][3], jenis)))
        h["peringatan"] += data.peringatan_kolom([grup, nilai])
        h["peringatan"] += pesan_kosong + data.peringatan_duplikat(idx) + data.peringatan_privasi(nilai, grup)
        h["saran_grafik"] = "Grafik batang horizontal urut nilai + garis % kumulatif (diagram Pareto)."
        return h
    if not nilai:
        raise InputError("Subperintah 'top' butuh --nilai (dan opsional --grup).")
    k = data.kol[nilai]
    h = hasil_dasar(data, "top", "{} {} baris menurut {}".format(n, arah.lower(), nilai))
    h["catatan"] = list(data.catatan)
    pasangan = [(k["nilai"][i], i) for i in idx if k["nilai"][i] is not None]
    pasangan.sort(key=lambda x: x[0], reverse=not args.terbawah)
    label_kol = [c for c in data.kolom if c != nilai and data.kol[c]["tipe"] in ("teks", "tanggal", "kode")
                 and (not data.kol[c]["sensitif"] or data.tampilkan_pribadi)][:3]
    rows = []
    no_teks = any(not isinstance(r, int) for r in data.baris_no)
    for no, (v, i) in enumerate(pasangan[:n], 1):
        rows.append([Decimal(no), str(data.baris_no[i]) if no_teks else Decimal(data.baris_no[i])] +
                    [data.kol[c]["nilai"][i] for c in label_kol] + [v])
    h["tabel"].append(tabel(h["judul"], ["#", "Baris Excel"] + label_kol + [nilai],
                            ["bulat", "teks" if no_teks else "bulat"] + ["teks"] * len(label_kol) +
                            [data.jenis_nilai(nilai)], rows))
    if rows:
        h["temuan"].append("Nilai {} '{}': {} di baris {}.".format(
            "terkecil" if args.terbawah else "terbesar", nilai, fmt_sel(rows[0][-1], data.jenis_nilai(nilai)),
            rows[0][1]))
    h["peringatan"] += data.peringatan_kolom([nilai])
    h["peringatan"] += data.peringatan_duplikat(idx) + data.peringatan_privasi(nilai, "baris")
    h["saran_grafik"] = "Tabel saja sudah cukup; bila perlu grafik, batang horizontal."
    return h


def _data_banding(args):
    """Kembalikan (data_a, idx_a, label_a, data_b, idx_b, label_b, hari_a, hari_b)."""
    data = muat(args, args.file, args.sheet)
    if args.file_b:
        data_b = muat(args, args.file_b, args.sheet_b or args.sheet, pakai_opsi_baris=False)
        ia = data.terapkan_filter(args.filter, args.tanggal, args.dari, args.sampai)
        ib = data_b.terapkan_filter(args.filter, args.tanggal, args.dari, args.sampai)
        la = args.label_a or data.info["file"]
        lb = args.label_b or data_b.info["file"]
        if la == lb and data.info.get("sheet") and data_b.info.get("sheet") \
                and data.info["sheet"] != data_b.info["sheet"] and not (args.label_a or args.label_b):
            la, lb = data.info["sheet"], data_b.info["sheet"]
        if la == lb:
            la, lb = "A: " + la, "B: " + lb
        return data, ia, la, data_b, ib, lb, None, None
    if not (args.periode_a and args.periode_b):
        raise InputError("Subperintah 'banding' butuh --periode-a dan --periode-b (mis. 2026-08 dan 2026-09), "
                         "atau --file-b untuk membandingkan dua file.")
    kt = data.kolom_tanggal_otomatis(args.tanggal)
    base = data.terapkan_filter(args.filter, None, None, None)
    tg = data.kol[kt]["nilai"]
    a1, a2 = parse_periode(args.periode_a)
    b1, b2 = parse_periode(args.periode_b)
    ia = [i for i in base if tg[i] is not None and a1 <= tg[i] <= a2]
    ib = [i for i in base if tg[i] is not None and b1 <= tg[i] <= b2]
    if not ia and not ib:
        raise InputError("Tidak ada data di kedua periode. Data tersedia {} s.d. {}.".format(
            fmt_tanggal(min(v for v in tg if v)), fmt_tanggal(max(v for v in tg if v))))

    def label(a, b):
        if a.day == 1 and b == akhir_bulan(b.year, b.month) and a.year == b.year and a.month == b.month:
            return "{} {}".format(NAMA_BULAN[a.month], a.year)
        return "{} s.d. {}".format(fmt_tanggal(a), fmt_tanggal(b))
    ada = [v for v in tg if v]
    for (p1, p2) in ((a1, a2), (b1, b2)):
        if ada and (p1 < min(ada) or p2 > max(ada)):
            data.peringatan.append("Periode {} tidak sepenuhnya tercakup data (data {} s.d. {}); angkanya "
                                   "bisa belum lengkap.".format(label(p1, p2), fmt_tanggal(min(ada)),
                                                                fmt_tanggal(max(ada))))
    return (data, ia, args.label_a or label(a1, a2), data, ib, args.label_b or label(b1, b2),
            (a2 - a1).days + 1, (b2 - b1).days + 1)


def cmd_banding(args, _data=None):
    da, ia, la, db, ib, lb, hari_a, hari_b = _data_banding(args)
    nilai_a, fungsi = _siapkan_nilai(da, args)
    nilai_b = db.cari(args.nilai, ("angka",), "nilai (file B)") if (args.nilai and db is not da) else nilai_a
    jenis = _jenis_hasil(da, nilai_a, fungsi)
    judul_nilai = buat_judul_nilai(fungsi, nilai_a)
    h = hasil_dasar(da, "banding", "Perbandingan {}: {} vs {}".format(judul_nilai, la, lb))
    h["catatan"] = list(da.catatan) + ([c for c in db.catatan if c not in da.catatan] if db is not da else [])
    if db is not da:
        h["peringatan"] += [p for p in db.peringatan if p not in h["peringatan"]]
        h["sumber"] += " vs " + db.info["file"] + (" — sheet '{}'".format(db.info["sheet"])
                                                  if db.info.get("sheet") else "")
    else:
        h["peringatan"] = list(da.peringatan)
    tot_a = agregasi(_vals(da, nilai_a, ia), fungsi) if ia else (NOL if fungsi in ("jumlah", "hitung") else None)
    tot_b = agregasi(_vals(db, nilai_b, ib), fungsi) if ib else (NOL if fungsi in ("jumlah", "hitung") else None)
    fmt = lambda x: fmt_sel(x, jenis)  # noqa: E731
    rows = []
    if args.grup:
        ga = da.cari(args.grup, peran="grup")
        gb = db.cari(args.grup, peran="grup (file B)") if db is not da else ga
        kel_a, kel_b = {}, {}
        for i in ia:
            v = da.kol[ga]["nilai"][i]
            kel_a.setdefault(kunci_kategori(v) if isinstance(v, str) else v, (v, []))[1].append(i)
        for i in ib:
            v = db.kol[gb]["nilai"][i]
            kel_b.setdefault(kunci_kategori(v) if isinstance(v, str) else v, (v, []))[1].append(i)
        kunci = list(OrderedDict.fromkeys(list(kel_a) + list(kel_b)))
        baru, hilang = [], []
        for kk in kunci:
            lab = (kel_a.get(kk) or kel_b.get(kk))[0]
            va = agregasi(_vals(da, nilai_a, kel_a[kk][1]), fungsi) if kk in kel_a else NOL
            vb = agregasi(_vals(db, nilai_b, kel_b[kk][1]), fungsi) if kk in kel_b else NOL
            if fungsi not in ("jumlah", "hitung"):
                va = va if kk in kel_a else None
                vb = vb if kk in kel_b else None
            sel = (vb - va) if (va is not None and vb is not None) else None
            label_g = _label_grup(da, ga, lab, "bulan") if kk is not None else "(kosong)"
            rows.append([label_g, va, vb, sel, persen_ubah(va, vb)])
            if kk in kel_a and kk not in kel_b:
                hilang.append(label_g)
            elif kk in kel_b and kk not in kel_a:
                baru.append(label_g)
            for lab_p, kel, dd, nn in ((la, kel_a, da, nilai_a), (lb, kel_b, db, nilai_b)):
                if nn and kk in kel and not _vals(dd, nn, kel[kk][1]):
                    h["peringatan"].append("'{}' ada di {} tetapi semua nilainya kosong/tidak terbaca "
                                           "(ditulis '-').".format(label_g, lab_p))
        rows.sort(key=lambda r: (r[3] is None, -abs(r[3] or 0)))
        judul_kol = ga
        h["peringatan"] += da.peringatan_kolom([ga])
    else:
        judul_kol = "Keterangan"
    sel_tot = (tot_b - tot_a) if (tot_a is not None and tot_b is not None) else None
    rows.append(["TOTAL" if args.grup else judul_nilai, tot_a, tot_b, sel_tot, persen_ubah(tot_a, tot_b)])
    h["tabel"].append(tabel(h["judul"], [judul_kol, la, lb, "Selisih", "Perubahan %"],
                            ["teks", jenis, jenis, jenis, "persen"], rows))
    h["temuan"].append("{}: {}.".format(judul_nilai, kalimat_ubah(tot_a, tot_b, fmt)))
    h["temuan"].append("Jumlah baris: {} vs {}.".format(fmt_angka(Decimal(len(ia))), fmt_angka(Decimal(len(ib)))))
    if args.grup and len(rows) > 1:
        naik = [r for r in rows[:-1] if r[3] is not None and r[3] > 0]
        turun = [r for r in rows[:-1] if r[3] is not None and r[3] < 0]
        if naik:
            r = max(naik, key=lambda x: x[3])
            h["temuan"].append("Naik paling besar: {} — {}.".format(r[0], kalimat_ubah(r[1], r[2], fmt)))
        if turun:
            r = min(turun, key=lambda x: x[3])
            h["temuan"].append("Turun paling besar: {} — {}.".format(r[0], kalimat_ubah(r[1], r[2], fmt)))
        if baru:
            h["temuan"].append("Hanya ada di {}: {}.".format(lb, ", ".join(map(str, baru[:8]))))
        if hilang:
            h["temuan"].append("Tidak muncul lagi di {}: {}.".format(lb, ", ".join(map(str, hilang[:8]))))
    if hari_a and hari_b and hari_a != hari_b and fungsi in ("jumlah", "hitung"):
        ra, rb = tot_a / hari_a, tot_b / hari_b
        h["temuan"].append("Panjang periode beda ({} vs {} hari). Rata-rata per hari: {} vs {} — {}.".format(
            hari_a, hari_b, fmt(ra), fmt(rb), kalimat_ubah(ra, rb, fmt)))
    h["peringatan"] += da.peringatan_kolom([nilai_a]) + da.peringatan_duplikat(ia)
    if db is not da:
        h["peringatan"] += db.peringatan_kolom([nilai_b]) + db.peringatan_duplikat(ib)
    else:
        h["peringatan"] += da.peringatan_duplikat(ib)
    h["peringatan"] += da.peringatan_privasi() + (db.peringatan_privasi() if db is not da else [])
    h["saran_grafik"] = ("Grafik batang berdampingan (clustered column): {} vs {}{}.".format(
        la, lb, " per " + args.grup if args.grup else ""))
    return h


def aman_csv(v):
    """Cegah formula injection saat CSV dibuka di Excel/Sheets."""
    if isinstance(v, str) and v and v[0] in "=+-@\t\r":
        return "'" + v
    return v


def _nilai_csv(v, jenis, excel_id):
    if v is None:
        return ""
    if isinstance(v, date):
        return v.strftime("%d/%m/%Y") if excel_id else v.isoformat()
    if isinstance(v, Decimal):
        if jenis == "persen":
            v = bulatkan(v, 1)
        elif jenis in ("uang", "angka", "*"):
            v = _rapikan_desimal(bulatkan(v, 2))
        elif jenis == "bulat":
            v = bulatkan(v, 0)
        s = "{:f}".format(v)
        return s.replace(".", ",") if excel_id else s
    return aman_csv(str(v))


def cmd_bersihkan(args, data):
    h = hasil_dasar(data, "bersihkan", "Data dibersihkan")
    keluar = args.keluar or os.path.splitext(args.file)[0] + "-bersih.csv"
    if os.path.abspath(keluar) == os.path.abspath(args.file):
        raise InputError("File keluaran tidak boleh menimpa file asli.")
    buang_dup = args.buang_duplikat
    seen = set()
    dup = 0
    tulis = []
    for i, r in enumerate(data.baris_no):
        row = []
        for n in data.kolom:
            k = data.kol[n]
            v = k["nilai"][i]
            if v is None and not adalah_kosong(data.mentah[i][data.kolom.index(n)]) \
                    and not adalah_galat_excel(data.mentah[i][data.kolom.index(n)]):
                m = data.mentah[i][data.kolom.index(n)]
                v = rapikan_teks(m) if isinstance(m, str) else m    # nilai tidak valid: biarkan apa adanya
            row.append(v)
        key = tuple(x.casefold() if isinstance(x, str) else x for x in row)
        if buang_dup and key in seen:
            dup += 1
            continue
        seen.add(key)
        tulis.append(row)
    try:
        with open(keluar, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f, delimiter=";" if args.excel_id else ",")
            w.writerow([aman_csv(n) for n in data.kolom])
            for row in tulis:
                w.writerow([_nilai_csv(v, "angka" if isinstance(v, Decimal) else "teks", args.excel_id) for v in row])
    except OSError as e:
        raise InputError("Gagal menulis '{}': {}".format(keluar, e))
    ubah = []
    for n, k in data.kol.items():
        mentah = [row[data.kolom.index(n)] for row in data.mentah]
        if k["tipe"] == "angka":
            c = sum(1 for m in mentah if isinstance(m, str) and not adalah_kosong(m)
                    and parse_angka(m, k["gaya"]) is not None and rapikan_teks(m) != "{:f}".format(parse_angka(m, k["gaya"])))
            if c:
                ubah.append([n, "angka", "{} teks angka (Rp/titik ribuan/koma desimal) diubah ke angka murni".format(c)])
        elif k["tipe"] == "tanggal":
            c = sum(1 for m in mentah if not adalah_kosong(m))
            ubah.append([n, "tanggal", "{} tanggal diseragamkan ke {}".format(
                c, "DD/MM/YYYY" if args.excel_id else "YYYY-MM-DD")])
        else:
            c = sum(1 for m in mentah if isinstance(m, str) and m != rapikan_teks(m))
            if c:
                ubah.append([n, k["tipe"], "{} sel dirapikan spasinya".format(c)])
            if k["gabung_kategori"]:
                ubah.append([n, k["tipe"], "{} kategori diseragamkan (huruf besar-kecil/spasi): {}".format(
                    len(k["gabung_kategori"]), "; ".join("{} ← {}".format(t, "/".join(v))
                                                         for t, v in k["gabung_kategori"][:3]))])
        if k["tidak_valid"]:
            ubah.append([n, k["tipe"], "{} nilai tidak valid DIBIARKAN apa adanya (cek manual: baris {})".format(
                len(k["tidak_valid"]), ", ".join(str(r) for r, _v in k["tidak_valid"][:6]))])
    h["tabel"].append(tabel("Perubahan", ["Kolom", "Tipe", "Perubahan"], ["teks", "teks", "teks"], ubah))
    h["temuan"].append("File bersih ditulis: {} ({} baris data, {} kolom).".format(keluar, len(tulis), len(data.kolom)))
    if data.baris_total:
        h["temuan"].append("{} baris dikeluarkan (ringkasan/catatan) tidak disalin.".format(len(data.baris_total)))
    if dup:
        h["temuan"].append("{} baris duplikat dibuang (--buang-duplikat).".format(dup))
    h["temuan"].append("File asli TIDAK diubah. Format: UTF-8, pemisah {}, angka tanpa titik ribuan{}.".format(
        "titik koma" if args.excel_id else "koma",
        " dan koma desimal (untuk Excel berbahasa Indonesia)" if args.excel_id else " dengan titik desimal"))
    h["peringatan"] += data.peringatan_kolom(data.kolom)
    h["file_keluar"] = keluar
    h["saran_grafik"] = "Lanjutkan dengan 'profil' atau 'pivot' pada file bersih ini."
    return h


# ---------------------------------------------------------------------------
# Keluaran
# ---------------------------------------------------------------------------

def _md_esc(s):
    return str(s).replace("|", "\\|").replace("\n", " ")


def render_md(h):
    out = ["## " + h["judul"], "", "_Sumber: {}{}_".format(
        h["sumber"], "; {} baris data".format(fmt_angka(Decimal(h["jumlah_baris_data"])))
        if h.get("jumlah_baris_data") else ""), ""]
    atas = [p for p in h["peringatan"] if p.startswith(("PERINGATAN TEGAS", "BARIS DIKELUARKAN"))]
    for p in atas:
        out += ["> **\u26a0\ufe0f {}**".format(_md_esc(p)) if p.startswith("PERINGATAN TEGAS")
                else "> {}".format(_md_esc(p)), ""]
    for t in h["tabel"]:
        if len(h["tabel"]) > 1 or t["judul"] != h["judul"]:
            out += ["### " + t["judul"], ""]
        if not t["baris"]:
            out += ["(tidak ada)", ""]
            continue
        out.append("| " + " | ".join(_md_esc(k) for k in t["kolom"]) + " |")
        out.append("|" + "|".join("---:" if j not in ("teks",) else "---" for j in t["jenis"]) + "|")
        for bi, row in enumerate(t["baris"]):
            sel = []
            for j, v in enumerate(row):
                jenis = t["jenis"][j]
                if jenis == "*":
                    jenis = t["jenis_baris"][bi]
                s = fmt_sel(v, jenis) if v is not None else ("" if t["jenis"][j] == "teks" else "-")
                sel.append(_md_esc(s))
            if row and row[0] == "TOTAL":
                sel = ["**{}**".format(s) if s else s for s in sel]
            out.append("| " + " | ".join(sel) + " |")
        out.append("")
    if h["temuan"]:
        out += ["### Temuan (dihitung script)", ""] + ["- " + t for t in h["temuan"]] + [""]
    if h.get("saran_grafik"):
        out += ["### Saran grafik", "", h["saran_grafik"], ""]
    lain = [p for p in h["peringatan"] if p not in atas]
    if lain:
        out += ["### Perlu diperhatikan", ""] + ["- \u26a0\ufe0f " + p for p in lain] + [""]
    if h["catatan"]:
        out += ["### Catatan", ""] + ["- " + c for c in h["catatan"]] + [""]
    return "\n".join(out)


def _json_default(o):
    if isinstance(o, Decimal):
        return "{:f}".format(o)
    if isinstance(o, date):
        return o.isoformat()
    return str(o)


def tulis_csv_hasil(h, path, excel_id):
    if not h["tabel"]:
        return
    t = h["tabel"][0]
    try:
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f, delimiter=";" if excel_id else ",")
            w.writerow([aman_csv(k) for k in t["kolom"]])
            for bi, row in enumerate(t["baris"]):
                w.writerow([_nilai_csv(v, t["jenis_baris"][bi] if t["jenis"][j] == "*" else t["jenis"][j], excel_id)
                            for j, v in enumerate(row)])
    except OSError as e:
        raise InputError("Gagal menulis '{}': {}".format(path, e))
    h["file_keluar"] = path
    h["catatan"].append("Tabel hasil disimpan ke {}.".format(path))


def parse_tipe(daftar):
    hasil = {}
    for x in daftar or []:
        if "=" not in x:
            raise InputError("Format --tipe harus \"Kolom=angka|tanggal|teks|kode\".")
        k, v = x.rsplit("=", 1)
        v = v.strip().lower()
        if v not in ("angka", "tanggal", "teks", "kode"):
            raise InputError("Tipe '{}' tidak dikenal (pilih angka, tanggal, teks, kode).".format(v))
        hasil[rapikan_teks(k).casefold()] = v
    return hasil


SEMUA_SHEET = {"semua", "all", "*", "semua sheet"}


def _minta_banyak_sheet(path, sheet):
    """True bila --sheet meminta beberapa sheet ("semua" atau "Q1,Q2,Q3") pada file XLSX."""
    if sheet is None:
        return False
    t = str(sheet).strip()
    if t.casefold() not in SEMUA_SHEET and "," not in t:
        return False
    try:
        with open(path, "rb") as f:
            if not f.read(2).startswith(b"PK"):
                return False
    except OSError:
        return False
    buku = BukuXlsx(path)
    return not any(s["nama"] == t for s in buku.sheets)   # nama sheet yang memang mengandung koma


def _cocok_struktur(ref_cf, cf):
    """Sheet berkolom cf boleh digabung ke acuan ref_cf bila minimal separuh kolom acuan ada."""
    sama = [k for k in ref_cf if k in cf]
    return bool(sama) and len(sama) * 2 >= len(ref_cf)


def _pilih_sheet_daftar(buku, nama):
    try:
        return buku.pilih_sheet(nama)
    except InputError as e:
        berkoma = [s["nama"] for s in buku.sheets if "," in s["nama"]]
        if berkoma:
            nomor = ", ".join("'{}' = nomor {}".format(n, [s["nama"] for s in buku.sheets].index(n) + 1)
                              for n in berkoma)
            raise InputError("{} Catatan: nama sheet {} mengandung koma, jadi tidak bisa ditulis di daftar "
                             "--sheet. Pakai nomor sheet, mis. --sheet \"1,{}\".".format(
                                 e, nomor, [s["nama"] for s in buku.sheets].index(berkoma[0]) + 1))
        raise


POLA_NAMA_REKAP = re.compile(r"\b(ringkas\w*|rangkum\w*|rekap\w*|recap|total|summary|ikhtisar|resume|pivot|"
                             r"dashboard)\b", re.I)
POLA_LABEL_PERIODE = re.compile(r"^(tw|triwulan|kuartal|q|semester|smt|caturwulan|cawu)\s*[-.]?\s*([1-4]|i{1,3}|iv)$",
                                re.I)


def _label_periode(v):
    """True bila sel adalah label bulan/triwulan (Jan, Februari, TW1, Q2, Triwulan III, Jan 2026 ...)."""
    if not isinstance(v, str):
        return False
    t = rapikan_teks(v).lower().rstrip(".")
    if POLA_LABEL_PERIODE.match(t):
        return True
    kata = re.split(r"[\s\-/']+", t)
    return bool(kata) and kata[0].rstrip(".") in BULAN and len(kata) <= 2 and \
        (len(kata) == 1 or re.fullmatch(r"\d{2}|\d{4}", kata[1]) is not None)


def _nilai_dec(v):
    if isinstance(v, bool):
        return None
    if isinstance(v, Decimal):
        return v
    if isinstance(v, str):
        return parse_angka(v)
    return None


def _jumlah_kolom(p):
    """{kolom (casefold): jumlah} untuk kolom angka sebuah potongan tabel (kolom kode/nomor dilewati)."""
    hasil = {}
    for j, nama in enumerate(p["kolom"]):
        if POLA_KODE.search(nama.casefold()):
            continue
        isi = [row[j] for row in p["mentah"] if j < len(row) and not adalah_kosong(row[j])]
        angka = [x for x in (_nilai_dec(v) for v in isi) if x is not None]
        if isi and len(angka) >= 0.6 * len(isi):
            hasil[nama.casefold()] = sum(angka, NOL)
    return hasil


def _hampir(a, b):
    return b != 0 and abs(a - b) <= abs(b) * Decimal("0.005")


def _deteksi_rekap(bagian):
    """{nama sheet: alasan} untuk sheet yang tampak rekap/ringkasan dari sheet lain (menggabungkannya = DOBEL)."""
    rekap = {}
    for nama, _p in bagian:
        m = POLA_NAMA_REKAP.search(nama)
        if m:
            rekap[nama] = "namanya mengandung '{}'".format(m.group(1))
    sisa = [(n, p) for n, p in bagian if n not in rekap]
    info = {n: (_jumlah_kolom(p), len(p["mentah"])) for n, p in sisa}
    for nama, p in sisa:
        lain = [(n, info[n]) for n, _q in sisa if n != nama]
        if not lain:
            continue
        jml, n_baris = info[nama]
        baris_lain = sum(b for _n, (_j, b) in lain)
        # (a) isinya menduplikasi total sheet lain: jumlah satu kolom angka (atau semua kolom angkanya)
        #     = jumlah gabungan sheet lain di satu kolom angka (atau semua kolom angkanya).
        if len(lain) >= 2 and jml and n_baris < baris_lain:
            acuan_lain = {}
            for _n, (jl, _b) in lain:
                for k, v in jl.items():
                    acuan_lain[k] = acuan_lain.get(k, NOL) + v
            calon = list(jml.items()) + [("semua kolom angka", sum(jml.values(), NOL))]
            target = list(acuan_lain.items()) + [("semua kolom angka", sum(acuan_lain.values(), NOL))]
            hit = next(((k1, v1, k2, v2) for k1, v1 in calon for k2, v2 in target
                        if v1 > 0 and _hampir(v1, v2)), None)
            if hit:
                selisih = abs(hit[1] - hit[3])
                rekap[nama] = "jumlah {} = {} {} jumlah gabungan sheet lain di {} ({}){}".format(
                    "kolom '{}'".format(p["kolom"][[k.casefold() for k in p["kolom"]].index(hit[0])])
                    if hit[0] != "semua kolom angka" else "semua kolom angkanya", fmt_angka(hit[1]),
                    "=" if not selisih else "≈",
                    "kolom '{}'".format(hit[2]) if hit[2] != "semua kolom angka" else "semua kolom angka",
                    fmt_angka(hit[3]), "" if not selisih else ", selisih {}".format(fmt_angka(selisih)))
                continue
        # (b) sedikit baris, tiap baris berlabel bulan/triwulan berbeda, sementara sheet lain jauh lebih panjang
        baris_lain_urut = sorted(b for _n, (_j, b) in lain)
        median_lain = baris_lain_urut[len(baris_lain_urut) // 2]
        if 2 <= n_baris <= 16 and median_lain >= 2 * n_baris:
            for j in range(len(p["kolom"])):
                isi = [row[j] for row in p["mentah"] if j < len(row) and not adalah_kosong(row[j])]
                lab = [rapikan_teks(v).casefold() for v in isi if _label_periode(v)]
                if len(lab) >= 2 and len(lab) >= 0.8 * n_baris and len(set(lab)) >= 0.8 * len(lab):
                    rekap[nama] = "hanya {} baris, masing-masing berlabel periode ({}), sedangkan sheet lain " \
                                  "puluhan baris".format(n_baris, ", ".join(str(v) for v in isi[:3]))
                    break
    return rekap


def gabung_sheet(path, spec, baris_header=None, pertahankan_total=False, acuan=None, sertakan=None, buang=None,
                 pertahankan=None, rentang=(None, None, False)):
    """Baca beberapa sheet berstruktur sama lalu gabungkan. Kembalikan (potongan, info).
    rentang = (--mulai-baris, --sampai-baris, --paksa) yang berlaku untuk setiap sheet."""
    buku = BukuXlsx(path)
    catatan, peringatan = [], []
    if str(spec).strip().casefold() in SEMUA_SHEET:
        pilih = [s for s in buku.sheets if s["status"] == "visible"]
        sembunyi = [s["nama"] for s in buku.sheets if s["status"] != "visible"]
        if sembunyi:
            catatan.append("Sheet tersembunyi tidak ikut digabung: {}. Sebutkan namanya di --sheet bila perlu."
                           .format(", ".join(sembunyi)))
    else:
        pilih = []
        for nama in [x.strip() for x in str(spec).split(",") if x.strip()]:
            sh = _pilih_sheet_daftar(buku, nama)
            if sh not in pilih:
                pilih.append(sh)
    semua = str(spec).strip().casefold() in SEMUA_SHEET
    dipaksa = set()   # sheet yang pengguna minta tetap digabung (--sertakan / --acuan)
    for nama in ([x.strip() for x in str(sertakan).split(",") if x.strip()] if sertakan else []) + \
            ([acuan] if acuan else []):
        sh = _pilih_sheet_daftar(buku, nama)
        dipaksa.add(sh["nama"])
        if sertakan and sh not in pilih and nama != acuan:
            pilih.append(sh)
    if not pilih:
        raise InputError("Tidak ada sheet yang bisa digabung.")
    bagian = []
    for sh in pilih:
        awal = len(buku.peringatan)
        try:
            grid = buku.baca_sheet(sh)
            p = _potong_tabel(grid, {"sheet": sh["nama"], "rumus_agregat": sh.get("rumus_agregat", {}),
                                     "mulai_baris": rentang[0], "sampai_baris": rentang[1], "paksa": rentang[2]},
                              baris_header, pertahankan_total, _baris_untuk_sheet(buang or [], sh["nama"], True),
                              _baris_untuk_sheet(pertahankan or [], sh["nama"], True))
        except InputError as e:
            peringatan.append("Sheet '{}' TIDAK digabung: {}".format(sh["nama"], e))
            continue
        pesan = buku.peringatan[awal:] + p["peringatan"]
        if sh["status"] != "visible":
            pesan.append("Sheet ini tersembunyi (hidden) di Excel.")
        p["pesan"] = (["Sheet '{}': {}".format(sh["nama"], x) for x in pesan],
                      ["Sheet '{}': {}".format(sh["nama"], x) for x in p["catatan"]])
        bagian.append((sh["nama"], p))
    if not bagian:
        raise InputError("Tidak ada sheet berisi tabel yang bisa digabung. " + " ".join(peringatan))
    # Sheet rekap/ringkasan (menjumlahkan sheet lain) jangan ikut digabung: total jadi DOBEL.
    if len(bagian) > 1:
        dilewati = []
        for nama, alasan in _deteksi_rekap(bagian).items():
            if nama in dipaksa:
                peringatan.append("Sheet '{}' tampak sheet REKAP/RINGKASAN ({}) tetapi tetap digabung karena "
                                  "diminta (--sertakan/--acuan). Cek totalnya — bisa DOBEL.".format(nama, alasan))
            elif semua:
                dilewati.append(nama)
                peringatan.append("Sheet '{}' TIDAK digabung: tampak sheet REKAP/RINGKASAN ({}); menggabungkannya "
                                  "akan menghitung total DOBEL. Bila sheet itu memang berisi data, ulangi dengan "
                                  "--sertakan \"{}\".".format(nama, alasan, nama))
            else:
                peringatan.append("Sheet '{}' yang Anda pilih tampak sheet REKAP/RINGKASAN ({}). Bila isinya "
                                  "menjumlahkan sheet lain, total gabungan DOBEL — keluarkan dari --sheet.".format(
                                      nama, alasan))
        bagian = [(n, p) for n, p in bagian if n not in dilewati]
        if not bagian:
            raise InputError("Semua sheet tampak sheet rekap/ringkasan. Pilih sheet data dengan --sheet \"<nama>\".")
    # Acuan struktur = sheet yang paling banyak cocok dengan sheet lain (bukan otomatis sheet pertama,
    # karena sheet pertama sering "Ringkasan"/"Rekap"/"Cover" berstruktur beda).
    if acuan:
        sh_acuan = buku.pilih_sheet(acuan)
        cocok_nama = [i for i, (n, _p) in enumerate(bagian) if n == sh_acuan["nama"]]
        if not cocok_nama:
            raise InputError("--acuan '{}' harus salah satu sheet yang digabung dan berisi tabel ({}).".format(
                acuan, ", ".join(n for n, _p in bagian)))
        i_ref = cocok_nama[0]
    else:
        skor = []
        for i, (_n, p) in enumerate(bagian):
            rcf = [k.casefold() for k in p["kolom"]]
            n_cocok = sum(1 for _m, q in bagian if _cocok_struktur(rcf, [k.casefold() for k in q["kolom"]]))
            skor.append((n_cocok, -i))
        i_ref = -max(skor)[1]
        if i_ref != 0:
            catatan.append("Acuan struktur kolom: sheet '{}' (cocok dengan {} sheet), bukan sheet pertama '{}'. "
                           "Ganti dengan --acuan \"<nama sheet>\" bila perlu.".format(
                               bagian[i_ref][0], max(skor)[0], bagian[0][0]))
    ref_nama, ref = bagian[i_ref]
    ref_kol = ref["kolom"]
    ref_cf = [k.casefold() for k in ref_kol]
    kol_sheet = "Sheet"
    while kol_sheet.casefold() in ref_cf:
        kol_sheet = "Asal " + kol_sheet
    baris_no, mentah, baris_total, header_ulang, dipakai = [], [], [], [], []
    dikeluarkan, kandidat = [], []
    for nama, p in bagian:
        cf = [k.casefold() for k in p["kolom"]]
        sama = [k for k in ref_cf if k in cf]
        kurang = [ref_kol[j] for j, k in enumerate(ref_cf) if k not in cf]
        lebih = [p["kolom"][j] for j, k in enumerate(cf) if k not in ref_cf]
        if not _cocok_struktur(ref_cf, cf):
            peringatan.append("Sheet '{}' TIDAK digabung karena judul kolomnya berbeda dari sheet '{}' "
                              "(kolom sheet ini: {}; mungkin sheet ringkasan/rekap). Analisis sheet itu terpisah "
                              "dengan --sheet \"{}\".".format(nama, ref_nama, ", ".join(p["kolom"]), nama))
            continue
        if kurang or lebih:
            peringatan.append("Sheet '{}' judul kolomnya TIDAK persis sama dengan sheet '{}': {}{}. Kolom yang "
                              "sama tetap digabung; cek hasilnya.".format(
                                  nama, ref_nama,
                                  "tidak ada kolom {} (dianggap kosong)".format(", ".join(kurang)) if kurang else "",
                                  ("; " if kurang else "") + "kolom tambahan {} diabaikan".format(", ".join(lebih))
                                  if lebih else ""))
        peringatan += p["pesan"][0]
        catatan += p["pesan"][1]
        posisi = [cf.index(k) if k in cf else None for k in ref_cf]
        for r, row in zip(p["baris_no"], p["mentah"]):
            baris_no.append("{}:{}".format(nama, r))
            mentah.append([nama] + [row[j] if j is not None else None for j in posisi])
        baris_total += ["{}:{}".format(nama, r) for r in p["baris_total"]]
        header_ulang += ["{}:{}".format(nama, r) for r in p["header_ulang"]]
        dikeluarkan += [("{}:{}".format(nama, r), a, t) for r, a, t in p["dikeluarkan"]]
        kandidat += [("{}:{}".format(nama, r), a, t) for r, a, t in p["kandidat"]]
        dipakai.append((nama, len(p["baris_no"]), p["baris_header"]))
    # Pemeriksaan umum dobel hitung: total gabungan ≈ 2 × total tanpa satu sheet (sheet itu = jumlah sheet lain).
    if len(dipakai) >= 3:
        idx_sheet = {}
        for b, row in zip(baris_no, mentah):
            idx_sheet.setdefault(b.split(":", 1)[0], []).append(row)
        sudah = False
        for j, nama_k in enumerate(ref_kol, start=1):
            if POLA_KODE.search(nama_k.casefold()) or sudah:
                continue
            jml = {n: sum((x for x in (_nilai_dec(r[j]) for r in rows) if x is not None), NOL)
                   for n, rows in idx_sheet.items()}
            total = sum(jml.values(), NOL)
            if total <= 0:
                continue
            for n, v in jml.items():
                if v > 0 and _hampir(total, 2 * (total - v)):
                    peringatan.append(
                        "PERINGATAN kemungkinan DOBEL HITUNG: di kolom '{}' total gabungan {} ≈ 2 × total tanpa "
                        "sheet '{}' ({}). Sheet itu tampaknya menjumlahkan sheet lain; bila benar, keluarkan dari "
                        "--sheet dan pakai total {}.".format(nama_k, fmt_angka(total), n, fmt_angka(total - v),
                                                            fmt_angka(total - v)))
                    sudah = True
                    break
    if len(dipakai) < 2 and len(pilih) > 1:
        peringatan.append("Hanya 1 sheet yang bisa dipakai; hasil BUKAN gabungan beberapa sheet. Bila sheet "
                          "yang Anda maksud dilewati, sebutkan daftarnya, mis. --sheet \"TW1,TW2,TW3\", atau "
                          "pilih acuan dengan --acuan \"<nama sheet>\".")
    hdr = {h for _n, _c, h in dipakai}
    potongan = {"baris_header": dipakai[0][2] if len(hdr) == 1 else "beragam per sheet",
                "kolom": [kol_sheet] + list(ref_kol), "baris_no": baris_no, "mentah": mentah,
                "baris_total": baris_total, "header_ulang": header_ulang, "peringatan": peringatan,
                "dikeluarkan": dikeluarkan, "kandidat": kandidat,
                "catatan": ["Gabungan {} sheet: {}. Kolom '{}' berisi asal sheet; nomor baris ditulis "
                            "'Sheet:baris' (mis. {}).".format(
                                len(dipakai), ", ".join("{} ({} baris)".format(n, c) for n, c, _h in dipakai),
                                kol_sheet, baris_no[0] if baris_no else dipakai[0][0] + ":1")] + catatan}
    info = {"file": os.path.basename(path), "format": "xlsx", "gabungan": True,
            "sheet": " + ".join(n for n, _c, _h in dipakai), "semua_sheet": [s["nama"] for s in buku.sheets],
            "peringatan": ["Workbook memakai sistem tanggal 1904 (Mac lama); sudah diperhitungkan."]
            if buku.date1904 else []}
    return potongan, info


def parse_daftar_baris(daftar, opsi):
    """'5,9' / '5 9' / 'Kas:7' (bisa diulang) -> list (sheet_atau_None, nomor_baris)."""
    hasil = []
    for teks in daftar or []:
        for tok in re.split(r"[,;\s]+", str(teks).strip()):
            if not tok:
                continue
            sh, _, no = tok.rpartition(":")
            no = no.strip()
            if not no.isdigit() or int(no) < 1:
                raise InputError("{} berisi '{}' — tulis nomor baris seperti di pesan script, mis. "
                                 "{} 5,9 (gabungan sheet: {} \"Kas:7\").".format(opsi, tok, opsi, opsi))
            hasil.append((sh.strip() or None, int(no)))
    return hasil


def _baris_untuk_sheet(daftar, nama_sheet, gabungan):
    hasil = set()
    for sh, no in daftar:
        if sh is None:
            if gabungan:
                raise InputError("Untuk gabungan sheet, tulis nomor baris beserta sheetnya seperti di pesan "
                                 "script, mis. \"TW1:7\".")
            hasil.add(no)
        elif not gabungan or nama_sheet is None or sh.casefold() == str(nama_sheet).casefold():
            hasil.add(no)
    return hasil


def muat(args, path, sheet, pakai_opsi_baris=True):
    pribadi = getattr(args, "tampilkan_pribadi", False)
    buang = parse_daftar_baris(getattr(args, "buang_baris", None), "--buang-baris") if pakai_opsi_baris else []
    jaga = parse_daftar_baris(getattr(args, "pertahankan_baris", None), "--pertahankan-baris") \
        if pakai_opsi_baris else []
    mulai = getattr(args, "mulai_baris", None) if pakai_opsi_baris else None
    sampai = getattr(args, "sampai_baris", None) if pakai_opsi_baris else None
    for nm, v in (("--mulai-baris", mulai), ("--sampai-baris", sampai)):
        if v is not None and v < 1:
            raise InputError("{} harus nomor baris >= 1.".format(nm))
    if mulai and sampai and mulai > sampai:
        raise InputError("--mulai-baris ({}) lebih besar dari --sampai-baris ({}).".format(mulai, sampai))
    if _minta_banyak_sheet(path, sheet):
        potongan, info = gabung_sheet(path, sheet, args.baris_header, args.pertahankan_total,
                                      getattr(args, "acuan", None), getattr(args, "sertakan", None),
                                      buang=buang, pertahankan=jaga, rentang=(mulai, sampai, args.paksa))
        return Data(None, info, urutan=args.urutan_tanggal, tipe_paksa=parse_tipe(args.tipe),
                    potongan=potongan, tampilkan_pribadi=pribadi)
    grid, info = baca_grid(path, sheet, args.pemisah, args.encoding, args.paksa)
    info["mulai_baris"], info["sampai_baris"] = mulai, sampai
    return Data(grid, info, args.baris_header, args.pertahankan_total, args.urutan_tanggal, parse_tipe(args.tipe),
                tampilkan_pribadi=pribadi, buang=_baris_untuk_sheet(buang, None, False),
                pertahankan=_baris_untuk_sheet(jaga, None, False))


def buat_parser():
    umum = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
    umum.add_argument("file", help="File .csv / .xlsx")
    umum.add_argument("--sheet", help="Nama atau nomor sheet (XLSX). \"semua\" = gabung semua sheet terlihat "
                      "berstruktur sama; \"Q1,Q2,Q3\" = gabung sheet tertentu. Default: sheet pertama yang terlihat")
    umum.add_argument("--acuan", help="Dengan --sheet semua/daftar: sheet acuan struktur kolom (default: sheet "
                      "yang paling banyak cocok dengan sheet lain)")
    umum.add_argument("--sertakan", help="Dengan --sheet semua: tetap gabungkan sheet ini walau tampak sheet "
                      "rekap/ringkasan (default dilewati agar total tidak dobel). Beberapa: \"Rekap,Total\"")
    umum.add_argument("--baris-header", "--header-baris", dest="baris_header", type=int,
                      help="Nomor baris judul kolom (default: deteksi otomatis). 0 = tabel tanpa judul kolom")
    umum.add_argument("--tanpa-header", action="store_const", const=0, dest="baris_header",
                      help="Tabel TANPA baris judul kolom: baris pertama ikut dihitung, kolom dinamai Kolom1..N")
    umum.add_argument("--mulai-baris", type=int,
                      help="Abaikan baris sebelum nomor ini (mis. untuk tabel kedua di file yang sama)")
    umum.add_argument("--sampai-baris", type=int,
                      help="Abaikan baris sesudah nomor ini (mis. hanya tabel pertama)")
    umum.add_argument("--pemisah", help="Pemisah CSV: , ; tab | (default: deteksi otomatis)")
    umum.add_argument("--encoding", help="Encoding CSV (default: deteksi UTF-8/BOM/cp1252)")
    umum.add_argument("--urutan-tanggal", choices=["dmy", "mdy"], help="Paksa urutan tanggal angka")
    umum.add_argument("--tipe", action="append", help="Paksa tipe kolom, mis. \"No HP=kode\" (bisa diulang)")
    umum.add_argument("--filter", action="append", help="Saring baris, mis. \"Cabang=Bandung|Bogor\"")
    umum.add_argument("--tanggal", help="Kolom tanggal (default: kolom tanggal pertama)")
    umum.add_argument("--dari", help="Tanggal/periode awal, mis. 2026-07 atau 01/07/2026")
    umum.add_argument("--sampai", help="Tanggal/periode akhir")
    umum.add_argument("--pertahankan-total", action="store_true",
                      help="Jangan keluarkan/curigai baris ringkasan sama sekali (semua baris dihitung apa adanya)")
    umum.add_argument("--buang-baris", action="append",
                      help="Keluarkan baris ini dari perhitungan (nomor seperti di pesan script), mis. \"5,9\"; "
                      "gabungan sheet: \"TW1:7\". Dengan --file-b hanya berlaku untuk file pertama")
    umum.add_argument("--pertahankan-baris", action="append",
                      help="Tetap hitung baris ini sebagai data walau tampak ringkasan/catatan, mis. \"12\"")
    umum.add_argument("--json", action="store_true", help="Keluaran JSON (untuk agent)")
    umum.add_argument("--keluar", help="Simpan tabel hasil utama ke file CSV ini")
    umum.add_argument("--excel-id", action="store_true",
                      help="CSV keluaran untuk Excel berbahasa Indonesia (pemisah ; dan koma desimal)")
    umum.add_argument("--paksa", action="store_true",
                      help="Tetap proses file > {} MB, dan baca CSV yang jumlah kolomnya tidak cocok / tampak "
                      "janggal apa adanya dengan PERINGATAN TEGAS (angka mungkin salah)".format(BATAS_MB))
    umum.add_argument("--tampilkan-pribadi", action="store_true",
                      help="Tampilkan NIK/HP/email/rekening lengkap (default disamarkan; UU PDP)")

    nilai = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
    nilai.add_argument("--nilai", help="Kolom angka yang dihitung (kosong = hitung banyak baris)")
    nilai.add_argument("--fungsi", choices=["jumlah", "rata", "median", "hitung", "min", "max"],
                       help="Default: jumlah (atau hitung bila tanpa --nilai)")
    nilai.add_argument("--per", choices=["hari", "minggu", "bulan", "kuartal", "tahun"],
                       help="Pengelompokan tanggal (default: bulan)")

    ap = argparse.ArgumentParser(description="Analisis spreadsheet CSV/XLSX untuk pengguna awam (Komunitech).", allow_abbrev=False)
    ap.add_argument("--versi", action="version", version=VERSI)
    sub = ap.add_subparsers(dest="perintah")
    sub.add_parser("daftar", parents=[umum], help="Daftar sheet & info pembacaan", allow_abbrev=False)
    sub.add_parser("profil", parents=[umum], help="Profil data", allow_abbrev=False)
    p = sub.add_parser("ringkas", parents=[umum], help="Ringkasan statistik", allow_abbrev=False)
    p.add_argument("--kolom", action="append", help="Batasi ke kolom ini (bisa diulang)")
    p = sub.add_parser("pivot", parents=[umum, nilai], help="Group-by / pivot", allow_abbrev=False)
    p.add_argument("--grup", required=True, help="Kolom pengelompokan (kategori atau tanggal)")
    p.add_argument("--kolom-pivot", help="Kolom kedua untuk tabel silang (opsional)")
    p.add_argument("--urut", choices=["nilai", "nama"], help="Urutan baris (default: nilai; tanggal: waktu)")
    p.add_argument("--n", type=int, help="Tampilkan N baris pertama saja")
    sub.add_parser("tren", parents=[umum, nilai], help="Tren per periode", allow_abbrev=False)
    p = sub.add_parser("top", parents=[umum, nilai], help="Top-N / bottom-N", allow_abbrev=False)
    p.add_argument("--grup", help="Kolom kategori (kosong = per baris)")
    p.add_argument("--n", type=int, help="Jumlah (default 10)")
    p.add_argument("--terbawah", action="store_true", help="Urutkan dari terkecil")
    p = sub.add_parser("banding", parents=[umum, nilai], help="Bandingkan dua periode / dua file", allow_abbrev=False)
    p.add_argument("--periode-a", help="Periode pembanding (lama), mis. 2026-08")
    p.add_argument("--periode-b", help="Periode yang dinilai (baru), mis. 2026-09")
    p.add_argument("--file-b", help="File kedua (bandingkan file A vs file B)")
    p.add_argument("--sheet-b", help="Sheet untuk file kedua")
    p.add_argument("--grup", help="Rinci perbandingan per kategori")
    p.add_argument("--label-a", help="Label periode/file A")
    p.add_argument("--label-b", help="Label periode/file B")
    p = sub.add_parser("bersihkan", parents=[umum], help="Tulis CSV bersih", allow_abbrev=False)
    p.add_argument("--buang-duplikat", action="store_true", help="Buang baris yang persis sama")
    return ap


PERINTAH = {"profil": cmd_profil, "ringkas": cmd_ringkas, "pivot": cmd_pivot, "tren": cmd_tren,
            "top": cmd_top, "banding": cmd_banding, "bersihkan": cmd_bersihkan}


def jalankan(argv=None):
    ap = buat_parser()
    args = ap.parse_args(argv)
    if not args.perintah:
        ap.print_help()
        return 2
    if getattr(args, "n", None) is not None and args.n < 1:
        raise InputError("--n harus ≥ 1.")
    if args.perintah == "daftar":
        h = cmd_daftar(args)
    elif args.perintah == "banding":
        h = cmd_banding(args)
    else:
        data = muat(args, args.file, args.sheet)
        h = PERINTAH[args.perintah](args, data)
    if args.keluar and args.perintah != "bersihkan":
        tulis_csv_hasil(h, args.keluar, args.excel_id)
    # buang duplikat peringatan, pertahankan urutan
    h["peringatan"] = list(OrderedDict.fromkeys(h["peringatan"]))
    h["catatan"] = list(OrderedDict.fromkeys(h["catatan"]))
    if args.json:
        print(json.dumps(h, ensure_ascii=False, indent=1, default=_json_default))
    else:
        print(render_md(h))
    return 0


def main(argv=None):
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    try:
        return jalankan(argv)
    except InputError as e:
        print("GAGAL: {}".format(e), file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        return 130
    except MemoryError:
        print("GAGAL: memori tidak cukup — file terlalu besar. Pecah file per bulan/sheet.", file=sys.stderr)
        return 2
    except Exception as e:  # jangan pernah tampilkan traceback mentah ke pengguna awam
        print("GAGAL: kesalahan tak terduga ({}: {}). Coba simpan ulang file sebagai CSV UTF-8 lalu ulangi; "
              "bila tetap gagal, laporkan pesan ini ke Komunitech.".format(type(e).__name__, e), file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
