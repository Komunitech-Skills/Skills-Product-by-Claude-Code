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

VERSI = "1.0.0"
BATAS_MB = 50            # file lebih besar ditolak kecuali --paksa
BATAS_BARIS_LAMBAT = 300000
BATAS_XML_MB = 800       # ukuran XML sheet setelah diekstrak (lindungi dari zip bomb)
BATAS_KOLOM_PIVOT = 15

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

POLA_KODE = re.compile(r"^(no|nomor|nomer|id|kode|code|nik|npwp|nip|nis|nim|sku|telp|telepon|tlp|hp|"
                       r"wa|whatsapp|phone|rekening|norek|resi|kodepos|kode pos|zip)\b", re.I)
POLA_UANG = re.compile(r"(\brp\b|\bidr\b|harga|total|omzet|omset|biaya|nilai (transaksi|penjualan|pembelian|kontrak|faktur|invoice)|nominal|pendapatan|"
                       r"penjualan|gaji|bayar|tagihan|amount|price|revenue|sales|cost|diskon|ongkir|"
                       r"laba|modal|saldo|debit|kredit|pengeluaran|pemasukan|belanja|upah|honor)", re.I)
POLA_BUKAN_UANG = re.compile(r"(qty|kuantitas|pcs|unit|jumlah barang|jumlah item|banyak|stok|stock|"
                             r"persen|%|rasio|rating|skor|nilai ujian|berat|kg|gram)", re.I)
POLA_SENSITIF = re.compile(r"(\bnik\b|ktp|npwp|no\.?\s*hp|\bhp\b|telepon|telp|phone|whatsapp|\bwa\b|"
                           r"e-?mail|alamat|address|rekening|norek|gaji|salary|upah|diagnos|penyakit|"
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
    s = str(s).replace("\xa0", " ").replace("\u202f", " ").replace("\u200b", "")
    return " ".join(s.split())


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
            m = re.match(r"(rp\.?|idr)", s)
            if m:
                s, ubah = s[m.end():], True
    s = re.sub(r"(rp|idr)$", "", s)
    s = re.sub(r"[.,]-$", "", s)                    # 15.000,-
    if s.endswith("-") and len(s) > 1:              # 5.000- (format akuntansi)
        neg, s = not neg, s[:-1]
    if not re.fullmatch(r"\d[\d.,]*\d|\d", s):
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


def baca_csv(path, pemisah=None, encoding=None):
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
    m = re.match(r"^\s*sep=(.)\s*$", baris_teks[0], re.I)
    if m:
        pemisah = pemisah or m.group(1)
        teks = "\n".join(baris_teks[1:])
    if pemisah in ("tab", "\\t"):
        pemisah = "\t"
    if not pemisah:
        pemisah = _deteksi_pemisah(teks)
    info["pemisah"] = NAMA_PEMISAH.get(pemisah, pemisah)
    hasil = []
    try:
        for i, row in enumerate(csv.reader(io.StringIO(teks, newline=""), delimiter=pemisah), start=1):
            row = [None if (c is None or not c.strip()) else c for c in row]
            while row and row[-1] is None:
                row.pop()
            if row:
                hasil.append((i, row))
    except csv.Error as e:
        raise InputError("CSV rusak (tanda kutip tidak tertutup?): {}".format(e))
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
                     "peringatan": list(buku.peringatan)})
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
    grid, info_csv = baca_csv(path, pemisah, encoding)
    info["format"] = "csv"
    info["encoding"] = info_csv["encoding"]
    info["pemisah"] = info_csv["pemisah"]
    info["peringatan"] = info.get("peringatan", []) + info_csv["peringatan"]
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


def _adalah_total(row):
    for v in row:
        if adalah_kosong(v):
            continue
        if isinstance(v, str):
            t = rapikan_teks(v).lower().rstrip(":")
            return t in KATA_TOTAL or t.startswith(("total ", "grand total", "jumlah total", "subtotal"))
        return False
    return False


class Data:
    """Tabel siap analisis: kolom bernama, nilai terurai per tipe."""

    def __init__(self, grid, info, baris_header=None, pertahankan_total=False, urutan=None, tipe_paksa=None):
        self.info = info
        self.peringatan = list(info.get("peringatan", []))
        self.catatan = []
        if not grid:
            raise InputError("Tidak ada data di {}.".format(
                "sheet '{}'".format(info["sheet"]) if info.get("sheet") else "file"))
        if baris_header:
            idx = next((i for i, (r, _row) in enumerate(grid) if r >= baris_header), None)
            if idx is None or grid[idx][0] != baris_header:
                raise InputError("Baris header {} kosong atau di luar data.".format(baris_header))
        else:
            idx = deteksi_header(grid)
        r_header, header = grid[idx]
        self.baris_header = r_header
        if r_header != 1:
            self.catatan.append("Judul kolom (header) terdeteksi di baris {} (baris di atasnya dianggap "
                                "judul/keterangan). Bila salah, pakai --baris-header N.".format(r_header))
        data_rows = grid[idx + 1:]
        lebar = max([len(header)] + [len(row) for _r, row in data_rows]) if data_rows else len(header)
        nama = []
        for i in range(lebar):
            v = header[i] if i < len(header) else None
            if isinstance(v, date):
                n = fmt_tanggal(v)
            elif isinstance(v, Decimal):
                n = fmt_angka(v)
            else:
                n = rapikan_teks(v)
            nama.append(n or "Kolom {}".format(huruf_kolom(i)))
        seen = Counter()
        for i, n in enumerate(nama):
            seen[n.casefold()] += 1
            if seen[n.casefold()] > 1:
                nama[i] = "{} ({})".format(n, seen[n.casefold()])
        kunci_header = [x.casefold() for x in nama]
        self.baris_no, self.mentah = [], []
        self.baris_total, self.header_ulang = [], []
        for r, row in data_rows:
            row = list(row) + [None] * (lebar - len(row))
            if all(adalah_kosong(v) for v in row):
                continue
            if [rapikan_teks(v).casefold() if isinstance(v, str) else "" for v in row] == kunci_header:
                self.header_ulang.append(r)
                continue
            if not pertahankan_total and _adalah_total(row):
                self.baris_total.append(r)
                continue
            self.baris_no.append(r)
            self.mentah.append(row)
        # buang kolom tanpa nama & tanpa isi
        pakai = [i for i in range(lebar)
                 if not nama[i].startswith("Kolom ") or any(not adalah_kosong(row[i]) for row in self.mentah)]
        self.kolom = [nama[i] for i in pakai]
        self.mentah = [[row[i] for i in pakai] for row in self.mentah]
        if self.baris_total:
            self.peringatan.append("{} baris Total/Jumlah dilewati agar tidak terhitung dua kali (baris {}). "
                                   "Pakai --pertahankan-total bila itu data asli.".format(
                                       len(self.baris_total), ", ".join(map(str, self.baris_total[:8]))))
        if self.header_ulang:
            self.catatan.append("{} baris yang mengulang judul kolom dilewati (baris {}).".format(
                len(self.header_ulang), ", ".join(map(str, self.header_ulang[:8]))))
        if not self.mentah:
            raise InputError("Judul kolom ditemukan di baris {} tetapi tidak ada baris data di bawahnya."
                             .format(r_header))
        if len(self.mentah) > BATAS_BARIS_LAMBAT:
            self.peringatan.append("Data {} baris — melebihi {} baris; hasil tetap dihitung tetapi bisa lambat."
                                   .format(fmt_angka(Decimal(len(self.mentah))), fmt_angka(Decimal(BATAS_BARIS_LAMBAT))))
        self.urutan_paksa = urutan
        self.tipe_paksa = tipe_paksa or {}
        self.kol = OrderedDict()
        for i, n in enumerate(self.kolom):
            self.kol[n] = self._ketik(n, [row[i] for row in self.mentah])
        sens = [n for n, k in self.kol.items() if k["sensitif"]]
        if sens:
            self.peringatan.append(
                "Kolom yang tampak berisi DATA PRIBADI/SENSITIF: {}. Contoh isinya tidak ditampilkan; "
                "jangan bagikan file/hasil mentah ke pihak lain tanpa izin (UU PDP No. 27/2022)."
                .format(", ".join(sens)))

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
            if email > len(teks_str) / 2 or nik > len(teks_str) / 2:
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
                and not (POLA_KODE.search(nama) and angka_bulat):
            tipe = "angka"
        elif n_angka >= 0.7 * n:
            tipe = "kode"
        else:
            tipe = "teks"
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
                kunci = t.casefold()
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
            raise InputError("Kolom {} '{}' {}. Kolom yang tersedia: {}.".format(
                peran, nama, alasan, ", ".join(self.kolom)))
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
                idx = [i for i in idx if k["nilai"][i] is not None and k["nilai"][i].casefold() in daftar]
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
                out.append("Kolom '{}': penulisan beda huruf besar-kecil/spasi digabung ({}).".format(n, contoh))
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
    sumber = info["file"] + (" — sheet '{}'".format(info["sheet"]) if info.get("sheet") else "")
    return {"perintah": perintah, "judul": judul, "sumber": sumber,
            "jumlah_baris_data": len(data.mentah), "baris_header": data.baris_header,
            "tabel": [], "temuan": [], "saran_grafik": "", "peringatan": list(data.peringatan),
            "catatan": list(data.catatan)}


def tabel(judul, kolom, jenis, baris):
    return {"judul": judul, "kolom": kolom, "jenis": jenis, "baris": baris}


def cmd_daftar(args):
    grid, info = baca_grid(args.file, args.sheet, args.pemisah, args.encoding, args.paksa)
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
        d = Data(grid, info, args.baris_header, args.pertahankan_total, args.urutan_tanggal, parse_tipe(args.tipe))
        h["temuan"].append("Judul kolom di baris {}: {}.".format(d.baris_header, ", ".join(d.kolom)))
        h["catatan"] += d.catatan
    except InputError as e:
        h["peringatan"].append(str(e))
    return h


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
    t = h["temuan"]
    t.append("{} baris data × {} kolom (judul kolom di baris {}).".format(
        fmt_angka(Decimal(len(data.mentah))), len(data.kolom), data.baris_header))
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
    h["saran_grafik"] = ("Histogram untuk melihat sebaran kolom angka; box plot untuk menandai outlier. "
                         "Untuk laporan, lanjutkan dengan 'ringkas', 'pivot', atau 'tren'.")
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
    h["peringatan"] += data.peringatan_kolom(daftar)
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
    return str(key)


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
    judul_nilai = "{} {}".format(NAMA_FUNGSI[fungsi], nilai) if nilai else NAMA_FUNGSI[fungsi]
    h = hasil_dasar(data, "pivot", "{} per {}".format(judul_nilai, grup +
                                                     (" ({})".format(per) if data.kol[grup]["tipe"] == "tanggal" else "")))
    h["catatan"] = list(data.catatan)
    kelompok = OrderedDict()
    for i in idx:
        kelompok.setdefault(_kunci_grup(data, grup, i, per), []).append(i)
    if data.kol[grup]["tipe"] == "tanggal" or data.kol[grup]["tipe"] == "angka":
        urut_nama = sorted(kelompok, key=lambda x: (x is None, x if x is not None else 0))
    else:
        urut_nama = sorted(kelompok, key=lambda x: (x is None, str(x).casefold()))
    semua_vals = _vals(data, nilai, idx)
    total = agregasi(semua_vals, fungsi)
    bisa_persen = fungsi in ("jumlah", "hitung") and all(v >= 0 for v in semua_vals) and total and total > 0
    if kolom2:
        sub = OrderedDict()
        for i in idx:
            sub.setdefault(_kunci_grup(data, kolom2, i, per), None)
        subkeys = sorted(sub, key=lambda x: (x is None, str(x).casefold() if not isinstance(x, (date, Decimal)) else x))
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
        rows = []
        for g in urut_nama:
            ig = kelompok[g]
            v = agregasi(_vals(data, nilai, ig), fungsi)
            row = [_label_grup(data, grup, g, per), Decimal(len(ig)), v]
            if bisa_persen:
                row.append(v / total * SERATUS if v is not None else None)
            rows.append(row)
        if args.urut == "nilai" or (args.urut is None and data.kol[grup]["tipe"] not in ("tanggal", "angka")):
            rows.sort(key=lambda r: (r[2] is None, -(r[2] or 0)))
        header = [grup, "Baris", judul_nilai] + (["% dari total"] if bisa_persen else [])
        jenis_k = ["teks", "bulat", jenis] + (["persen"] if bisa_persen else [])
        if args.n:
            rows = rows[:args.n]
        tot = ["TOTAL", Decimal(len(idx)), total] + ([SERATUS] if bisa_persen else [])
        h["tabel"].append(tabel(h["judul"], header, jenis_k, rows + [tot]))
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
    return h


def cmd_tren(args, data):
    idx = data.terapkan_filter(args.filter, args.tanggal, args.dari, args.sampai)
    kt = data.kolom_tanggal_otomatis(args.tanggal)
    nilai, fungsi = _siapkan_nilai(data, args)
    per = args.per or "bulan"
    jenis = _jenis_hasil(data, nilai, fungsi)
    judul_nilai = "{} {}".format(NAMA_FUNGSI[fungsi], nilai) if nilai else NAMA_FUNGSI[fungsi]
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
        ubah = persen_ubah(sebelumnya, v) if sebelumnya is not None and v is not None else None
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
            naik = [(rows[j][0], rows[j][3]) for j in range(1, len(rows)) if rows[j][3] is not None]
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
        judul_nilai = "{} {}".format(NAMA_FUNGSI[fungsi], nilai) if nilai else NAMA_FUNGSI[fungsi]
        h = hasil_dasar(data, "top", "{} {} {} menurut {}".format(n, arah.lower(), grup, judul_nilai))
        h["catatan"] = list(data.catatan)
        kel = OrderedDict()
        per = args.per or "bulan"
        for i in idx:
            kel.setdefault(_kunci_grup(data, grup, i, per), []).append(i)
        daftar = [(g, agregasi(_vals(data, nilai, ig), fungsi), len(ig)) for g, ig in kel.items()]
        daftar = [x for x in daftar if x[1] is not None]
        daftar.sort(key=lambda x: x[1], reverse=not args.terbawah)
        total = agregasi(_vals(data, nilai, idx), fungsi)
        bisa_persen = fungsi in ("jumlah", "hitung") and total and total > 0 and all(x[1] >= 0 for x in daftar)
        rows, kum = [], NOL
        for no, (g, v, c) in enumerate(daftar[:n], 1):
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
        h["tabel"].append(tabel(h["judul"], header, ["bulat", "teks", "bulat", jenis] +
                                (["persen", "persen"] if bisa_persen else []), rows))
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
                 and not data.kol[c]["sensitif"]][:3]
    rows = []
    for no, (v, i) in enumerate(pasangan[:n], 1):
        rows.append([Decimal(no), Decimal(data.baris_no[i])] +
                    [data.kol[c]["nilai"][i] for c in label_kol] + [v])
    h["tabel"].append(tabel(h["judul"], ["#", "Baris Excel"] + label_kol + [nilai],
                            ["bulat", "bulat"] + ["teks"] * len(label_kol) + [data.jenis_nilai(nilai)], rows))
    if rows:
        h["temuan"].append("Nilai {} '{}': {} di baris {}.".format(
            "terkecil" if args.terbawah else "terbesar", nilai, fmt_sel(rows[0][-1], data.jenis_nilai(nilai)),
            rows[0][1]))
    h["peringatan"] += data.peringatan_kolom([nilai])
    h["saran_grafik"] = "Tabel saja sudah cukup; bila perlu grafik, batang horizontal."
    return h


def _data_banding(args):
    """Kembalikan (data_a, idx_a, label_a, data_b, idx_b, label_b, hari_a, hari_b)."""
    data = muat(args, args.file, args.sheet)
    if args.file_b:
        data_b = muat(args, args.file_b, args.sheet_b or args.sheet)
        ia = data.terapkan_filter(args.filter, args.tanggal, args.dari, args.sampai)
        ib = data_b.terapkan_filter(args.filter, args.tanggal, args.dari, args.sampai)
        la = args.label_a or data.info["file"]
        lb = args.label_b or data_b.info["file"]
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
    judul_nilai = "{} {}".format(NAMA_FUNGSI[fungsi], nilai_a) if nilai_a else NAMA_FUNGSI[fungsi]
    h = hasil_dasar(da, "banding", "Perbandingan {}: {} vs {}".format(judul_nilai, la, lb))
    h["catatan"] = list(da.catatan) + ([c for c in db.catatan if c not in da.catatan] if db is not da else [])
    if db is not da:
        h["peringatan"] += [p for p in db.peringatan if p not in h["peringatan"]]
        h["sumber"] += " vs " + db.info["file"]
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
            kel_a.setdefault(v.casefold() if isinstance(v, str) else v, (v, []))[1].append(i)
        for i in ib:
            v = db.kol[gb]["nilai"][i]
            kel_b.setdefault(v.casefold() if isinstance(v, str) else v, (v, []))[1].append(i)
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
    h["peringatan"] += da.peringatan_kolom([nilai_a])
    if db is not da:
        h["peringatan"] += db.peringatan_kolom([nilai_b])
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
                ubah.append([n, k["tipe"], "{} kategori diseragamkan huruf besar-kecil: {}".format(
                    len(k["gabung_kategori"]), "; ".join("{} ← {}".format(t, "/".join(v))
                                                         for t, v in k["gabung_kategori"][:3]))])
        if k["tidak_valid"]:
            ubah.append([n, k["tipe"], "{} nilai tidak valid DIBIARKAN apa adanya (cek manual: baris {})".format(
                len(k["tidak_valid"]), ", ".join(str(r) for r, _v in k["tidak_valid"][:6]))])
    h["tabel"].append(tabel("Perubahan", ["Kolom", "Tipe", "Perubahan"], ["teks", "teks", "teks"], ubah))
    h["temuan"].append("File bersih ditulis: {} ({} baris data, {} kolom).".format(keluar, len(tulis), len(data.kolom)))
    if data.baris_total:
        h["temuan"].append("{} baris Total/Jumlah tidak disalin.".format(len(data.baris_total)))
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
    if h["peringatan"]:
        out += ["### Perlu diperhatikan", ""] + ["- \u26a0\ufe0f " + p for p in h["peringatan"]] + [""]
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


def muat(args, path, sheet):
    grid, info = baca_grid(path, sheet, args.pemisah, args.encoding, args.paksa)
    return Data(grid, info, args.baris_header, args.pertahankan_total, args.urutan_tanggal, parse_tipe(args.tipe))


def buat_parser():
    umum = argparse.ArgumentParser(add_help=False)
    umum.add_argument("file", help="File .csv / .xlsx")
    umum.add_argument("--sheet", help="Nama atau nomor sheet (XLSX). Default: sheet pertama yang terlihat")
    umum.add_argument("--baris-header", type=int, help="Nomor baris judul kolom (default: deteksi otomatis)")
    umum.add_argument("--pemisah", help="Pemisah CSV: , ; tab | (default: deteksi otomatis)")
    umum.add_argument("--encoding", help="Encoding CSV (default: deteksi UTF-8/BOM/cp1252)")
    umum.add_argument("--urutan-tanggal", choices=["dmy", "mdy"], help="Paksa urutan tanggal angka")
    umum.add_argument("--tipe", action="append", help="Paksa tipe kolom, mis. \"No HP=kode\" (bisa diulang)")
    umum.add_argument("--filter", action="append", help="Saring baris, mis. \"Cabang=Bandung|Bogor\"")
    umum.add_argument("--tanggal", help="Kolom tanggal (default: kolom tanggal pertama)")
    umum.add_argument("--dari", help="Tanggal/periode awal, mis. 2026-07 atau 01/07/2026")
    umum.add_argument("--sampai", help="Tanggal/periode akhir")
    umum.add_argument("--pertahankan-total", action="store_true", help="Jangan lewati baris Total/Jumlah")
    umum.add_argument("--json", action="store_true", help="Keluaran JSON (untuk agent)")
    umum.add_argument("--keluar", help="Simpan tabel hasil utama ke file CSV ini")
    umum.add_argument("--excel-id", action="store_true",
                      help="CSV keluaran untuk Excel berbahasa Indonesia (pemisah ; dan koma desimal)")
    umum.add_argument("--paksa", action="store_true", help="Tetap proses file > {} MB".format(BATAS_MB))

    nilai = argparse.ArgumentParser(add_help=False)
    nilai.add_argument("--nilai", help="Kolom angka yang dihitung (kosong = hitung banyak baris)")
    nilai.add_argument("--fungsi", choices=["jumlah", "rata", "median", "hitung", "min", "max"],
                       help="Default: jumlah (atau hitung bila tanpa --nilai)")
    nilai.add_argument("--per", choices=["hari", "minggu", "bulan", "kuartal", "tahun"],
                       help="Pengelompokan tanggal (default: bulan)")

    ap = argparse.ArgumentParser(description="Analisis spreadsheet CSV/XLSX untuk pengguna awam (Komunitech).")
    ap.add_argument("--versi", action="version", version=VERSI)
    sub = ap.add_subparsers(dest="perintah")
    sub.add_parser("daftar", parents=[umum], help="Daftar sheet & info pembacaan")
    sub.add_parser("profil", parents=[umum], help="Profil data")
    p = sub.add_parser("ringkas", parents=[umum], help="Ringkasan statistik")
    p.add_argument("--kolom", action="append", help="Batasi ke kolom ini (bisa diulang)")
    p = sub.add_parser("pivot", parents=[umum, nilai], help="Group-by / pivot")
    p.add_argument("--grup", required=True, help="Kolom pengelompokan (kategori atau tanggal)")
    p.add_argument("--kolom-pivot", help="Kolom kedua untuk tabel silang (opsional)")
    p.add_argument("--urut", choices=["nilai", "nama"], help="Urutan baris (default: nilai; tanggal: waktu)")
    p.add_argument("--n", type=int, help="Tampilkan N baris pertama saja")
    sub.add_parser("tren", parents=[umum, nilai], help="Tren per periode")
    p = sub.add_parser("top", parents=[umum, nilai], help="Top-N / bottom-N")
    p.add_argument("--grup", help="Kolom kategori (kosong = per baris)")
    p.add_argument("--n", type=int, help="Jumlah (default 10)")
    p.add_argument("--terbawah", action="store_true", help="Urutkan dari terkecil")
    p = sub.add_parser("banding", parents=[umum, nilai], help="Bandingkan dua periode / dua file")
    p.add_argument("--periode-a", help="Periode pembanding (lama), mis. 2026-08")
    p.add_argument("--periode-b", help="Periode yang dinilai (baru), mis. 2026-09")
    p.add_argument("--file-b", help="File kedua (bandingkan file A vs file B)")
    p.add_argument("--sheet-b", help="Sheet untuk file kedua")
    p.add_argument("--grup", help="Rinci perbandingan per kategori")
    p.add_argument("--label-a", help="Label periode/file A")
    p.add_argument("--label-b", help="Label periode/file B")
    p = sub.add_parser("bersihkan", parents=[umum], help="Tulis CSV bersih")
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
