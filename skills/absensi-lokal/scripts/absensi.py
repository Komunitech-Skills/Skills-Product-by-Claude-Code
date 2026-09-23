#!/usr/bin/env python3
"""absensi-lokal (Komunitech) - buku absensi karyawan lokal + rekap bulanan + upah lembur PP 35/2021.

Satu file database SQLite di komputer pemilik usaha. Hanya library standar Python 3.8+,
lintas OS, tanpa akses jaringan. Semua perintah tulis berjalan sebagai PRATINJAU (tidak
menyimpan) sampai diberi flag --ya setelah pengguna menyetujui ringkasannya.

Lokasi database (urutan prioritas):
  1. --db PATH
  2. ENV KOMUNITECH_ABSENSI_DB  (path file lengkap)
  3. ENV KOMUNITECH_DATA        (folder) + /absensi/absensi.db
  4. ~/KomunitechData/absensi/absensi.db

Contoh:
  python3 absensi.py init --ya
  python3 absensi.py karyawan tambah --kode A01 --nama Andi --hari-kerja 5 --gaji-pokok 5000000 --ya
  python3 absensi.py catat --karyawan Andi --masuk 08.12 --ya
  python3 absensi.py impor-absen log-mesin.csv            (pratinjau + pemetaan kolom)
  python3 absensi.py lembur --karyawan Andi --tanggal 2026-09-03 --jam 2 --catatan "perintah Bu Sari" --ya
  python3 absensi.py rekap --bulan 2026-09 --csv-gaji lembur-gaji.csv
"""
import argparse
import csv
import io
import json
import os
import re
import sqlite3
import sys
import zipfile
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import date, datetime, time, timedelta
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

VERSI = "1.0.0"
SKEMA = 1
APLIKASI = "absensi-lokal"
PEMBAGI_UPAH_SEJAM = Decimal(173)          # PP 35/2021 Pasal 32 ayat (2)
MAKS_LEMBUR_HARI_KERJA = Decimal(4)        # PP 35/2021 Pasal 26 ayat (1)
MAKS_LEMBUR_MINGGU = Decimal(18)           # PP 35/2021 Pasal 26 ayat (1)
# Tangga pengali lembur hari istirahat mingguan / hari libur resmi: [(jumlah jam, pengali), ...]
TANGGA_LIBUR = {
    "5": [(8, 2), (1, 3), (3, 4)],   # Pasal 31 ayat (3): jam 1-8 2x, jam 9 3x, jam 10-12 4x
    "6": [(7, 2), (1, 3), (3, 4)],   # Pasal 31 ayat (2) huruf a: jam 1-7 2x, jam 8 3x, jam 9-11 4x
    "6p": [(5, 2), (1, 3), (3, 4)],  # Pasal 31 ayat (2) huruf b: libur resmi di hari kerja terpendek
}
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
BULAN_NAMA = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September",
              "Oktober", "November", "Desember"]
JENIS_KET = ["izin", "sakit", "cuti", "alpa", "dinas"]
DISCLAIMER = ("Upah lembur: PP 35/2021 Pasal 31-32 (upah sejam = 1/173 x upah sebulan), hanya dari lembur yang "
              "disetujui, dibulatkan ke rupiah terdekat. Alat bantu hitung, bukan nasihat hukum; kasus khusus "
              "tanyakan ke Disnaker/konsultan.")


class Gagal(Exception):
    """Error yang pesannya aman ditampilkan ke pengguna."""

    def __init__(self, pesan, **detail):
        super().__init__(pesan)
        self.pesan = pesan
        self.detail = detail


# ---------------------------------------------------------------------------
# Angka, rupiah, tanggal, jam
# ---------------------------------------------------------------------------


def bulat_rp(x):
    """Rupiah terdekat, setengah ke atas (0,5 -> 1)."""
    return int(Decimal(x).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def rp(x):
    if x is None:
        return "-"
    n = bulat_rp(x)
    return ("-Rp " if n < 0 else "Rp ") + "{:,}".format(abs(n)).replace(",", ".")


def fjam(d):
    """Decimal jam -> '2', '1,5'."""
    d = Decimal(d).normalize()
    s = format(d, "f")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s.replace(".", ",")


def fmenit(m):
    """menit -> '7 jam 5 menit'."""
    m = int(m)
    j, s = divmod(abs(m), 60)
    if j and s:
        t = "%d jam %d menit" % (j, s)
    elif j:
        t = "%d jam" % j
    else:
        t = "%d menit" % s
    return ("-" if m < 0 else "") + t


def _grup_ok(bulat, pem):
    g = bulat.split(pem)
    return 1 <= len(g[0]) <= 3 and all(len(x) == 3 for x in g[1:])


def parse_angka(teks):
    """Angka format Indonesia -> Decimal, atau None. '5.000.000', 'Rp 5.000.000', '5jt', '750rb', '1,5'."""
    if teks is None:
        return None
    if isinstance(teks, (int, float, Decimal)):
        return Decimal(str(teks))
    s = str(teks).strip().lower()
    if not s:
        return None
    kali = Decimal(1)
    m = re.search(r"\s*(jt|juta|rb|ribu|k)\s*$", s)
    if m:
        kali = Decimal(1000000) if m.group(1) in ("jt", "juta") else Decimal(1000)
        s = s[:m.start()]
    s = re.sub(r"\b(rp|idr)\b\.?", "", s)
    s = re.sub(r"[,.]\s*-\s*$", "", s)
    s = s.replace(" ", "")
    if not s or not re.fullmatch(r"-?[\d.,]+", s):
        return None
    neg = s.startswith("-")
    s = s.lstrip("-")
    if "," in s and "." in s:
        des = "," if s.rfind(",") > s.rfind(".") else "."
        rib = "." if des == "," else ","
        bulat, _, pec = s.rpartition(des)
        if rib in pec or not _grup_ok(bulat, rib):
            return None
        s = bulat.replace(rib, "") + "." + pec
    elif "," in s or "." in s:
        pem = "," if "," in s else "."
        bag = s.split(pem)
        if len(bag) == 2 and (len(bag[1]) != 3 or kali != 1):
            s = bag[0] + "." + bag[1]
        elif _grup_ok(s, pem):
            s = s.replace(pem, "")
        else:
            return None
    try:
        n = Decimal(s) * kali
    except ArithmeticError:
        return None
    return -n if neg else n


def angka_wajib(teks, nama, boleh_nol=True):
    n = parse_angka(teks)
    if n is None:
        raise Gagal("Angka '%s' untuk %s tidak bisa dibaca. Contoh: 5000000, Rp 5.000.000, 5jt." % (teks, nama))
    if n < 0:
        raise Gagal("%s tidak boleh negatif (%s)." % (nama, teks))
    if n == 0 and not boleh_nol:
        raise Gagal("%s harus lebih dari 0." % nama)
    return n


def parse_durasi_jam(teks):
    """'2', '1,5', '1.5', '1:30', '1 jam 30 menit', '90 menit' -> Decimal jam, atau None."""
    s = str(teks or "").strip().lower()
    if not s:
        return None
    m = re.fullmatch(r"(\d{1,2}):(\d{2})", s)
    if m:
        mn = int(m.group(2))
        return None if mn >= 60 else Decimal(int(m.group(1))) + Decimal(mn) / Decimal(60)
    m = re.fullmatch(r"(?:(\d+(?:[.,]\d+)?)\s*(?:jam|j|h))?\s*(?:(\d+)\s*(?:menit|mnt|m))?", s)
    if m and (m.group(1) or m.group(2)):
        j = Decimal(m.group(1).replace(",", ".")) if m.group(1) else Decimal(0)
        mn = Decimal(m.group(2)) if m.group(2) else Decimal(0)
        return j + mn / Decimal(60)
    m = re.fullmatch(r"(\d+(?:[.,]\d+)?)", s)
    if m:
        return Decimal(m.group(1).replace(",", "."))
    return None


BULAN = {
    "jan": 1, "januari": 1, "january": 1, "feb": 2, "februari": 2, "february": 2, "peb": 2,
    "mar": 3, "maret": 3, "march": 3, "apr": 4, "april": 4, "mei": 5, "may": 5,
    "jun": 6, "juni": 6, "june": 6, "jul": 7, "juli": 7, "july": 7,
    "agu": 8, "agt": 8, "agus": 8, "agustus": 8, "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9, "okt": 10, "oktober": 10, "oct": 10, "october": 10,
    "nov": 11, "nop": 11, "november": 11, "des": 12, "desember": 12, "dec": 12, "december": 12,
}
HARI_KATA = {"senin": 1, "selasa": 2, "rabu": 3, "kamis": 4, "jumat": 5, "jum'at": 5, "sabtu": 6, "minggu": 7,
             "ahad": 7, "mon": 1, "tue": 2, "wed": 3, "thu": 4, "fri": 5, "sat": 6, "sun": 7, "monday": 1,
             "tuesday": 2, "wednesday": 3, "thursday": 4, "friday": 5, "saturday": 6, "sunday": 7}
RE_TGL_ANGKA = re.compile(r"^(\d{1,4})[-/.](\d{1,2})[-/.](\d{1,4})$")
RE_TGL_NAMA = re.compile(r"^(\d{1,2})[\s\-/]+([A-Za-z]+)\.?[\s\-/,]+(\d{2}|\d{4})$")
RE_JAM = re.compile(r"^(\d{1,2})[:.](\d{2})(?:[:.](\d{2}))?\s*(am|pm|a\.m\.|p\.m\.)?$", re.I)


def pisah_tanggal_jam(teks):
    """'Senin, 01/09/2026 08:12:33' -> ('01/09/2026', '08:12:33'). Jam boleh kosong."""
    t = str(teks or "").strip()
    t = re.sub(r"^[A-Za-z']+,?\s+(?=\d)", "", t)       # buang nama hari di depan
    m = re.match(r"^(\d{1,4}[-/.]\d{1,2}[-/.]\d{1,4})(?:[ T]+(.*))?$", t)
    if m:
        return m.group(1), (m.group(2) or "").strip()
    m = re.match(r"^(\d{1,2}[\s\-/]+[A-Za-z]+\.?[\s\-/,]+\d{2,4})(?:[ T,]+(.*))?$", t)
    if m:
        return m.group(1), (m.group(2) or "").strip()
    return t, ""


def parse_tanggal(teks, urutan="dmy"):
    """Tanggal -> date atau None. urutan untuk format angka non-ISO: 'dmy' (Indonesia) atau 'mdy'."""
    t = str(teks or "").strip()
    if not t:
        return None
    try:
        if re.fullmatch(r"\d{5}(\.\d+)?", t):          # nomor seri Excel
            n = float(t)
            return date(1899, 12, 30) + timedelta(days=int(n)) if 20000 < n < 80000 else None
        m = RE_TGL_ANGKA.match(t)
        if m:
            a, b, c = m.group(1), m.group(2), m.group(3)
            if len(a) == 4:
                return date(int(a), int(b), int(c))
            if len(c) not in (2, 4):
                return None
            y = int(c) + (2000 if len(c) == 2 else 0)
            d, mo = (int(a), int(b)) if urutan == "dmy" else (int(b), int(a))
            return date(y, mo, d)
        m = RE_TGL_NAMA.match(t)
        if m and m.group(2).lower() in BULAN:
            y = int(m.group(3)) + (2000 if len(m.group(3)) == 2 else 0)
            return date(y, BULAN[m.group(2).lower()], int(m.group(1)))
    except ValueError:
        return None
    return None


def parse_jam(teks):
    """'08.12', '8:12:33', '08.12.33', '8:12 PM', pecahan Excel '0.3416' -> time, atau None."""
    t = str(teks or "").strip()
    if not t:
        return None
    if re.fullmatch(r"0?\.\d+", t):                    # pecahan hari (sel jam Excel)
        detik = int(round(float(t) * 86400))
        if detik >= 86400:
            return None
        return time(detik // 3600, detik % 3600 // 60, detik % 60)
    m = RE_JAM.match(t)
    if not m:
        return None
    h, mi, s = int(m.group(1)), int(m.group(2)), int(m.group(3) or 0)
    ap = (m.group(4) or "").lower().replace(".", "")
    if ap:
        if not 1 <= h <= 12:
            return None
        h = h % 12 + (12 if ap == "pm" else 0)
    if h > 23 or mi > 59 or s > 59:
        return None
    return time(h, mi, s)


def tanggal_wajib(teks, nama="tanggal"):
    d = parse_tanggal(teks)
    if d is None:
        raise Gagal("%s '%s' tidak dikenali. Pakai format 2026-09-23 atau 23/09/2026." % (nama.capitalize(), teks))
    return d


def jam_wajib(teks, nama):
    j = parse_jam(teks)
    if j is None:
        raise Gagal("Jam %s '%s' tidak valid. Contoh benar: 08.12 atau 17:05 (jam 00-23, menit 00-59)."
                    % (nama, teks))
    return j


def fjm(t):
    """time/datetime -> '08.12'."""
    return "%02d.%02d" % (t.hour, t.minute)


def ftgl(d):
    return "%02d/%02d/%04d" % (d.day, d.month, d.year)


def sekarang(args=None):
    s = getattr(args, "sekarang", None) if args is not None else None
    if s:
        tg, jm = pisah_tanggal_jam(s)
        d = parse_tanggal(tg)
        j = parse_jam(jm) if jm else time(23, 59)
        if d is None or j is None:
            raise Gagal("--sekarang '%s' tidak valid. Contoh: '2026-09-23 09:30'." % s)
        return datetime.combine(d, j)
    return datetime.now().replace(microsecond=0)


def norm(s):
    return re.sub(r"\s+", " ", str(s or "").replace("﻿", "")).strip().lower()


def parse_hari_list(teks, nama):
    """'sabtu,minggu' / '6,7' / '-' -> list int ISO weekday."""
    s = norm(teks)
    if s in ("", "-", "tidak ada", "none"):
        return []
    hasil = []
    for b in re.split(r"[,;/+ ]+", s):
        if not b:
            continue
        if b.isdigit() and 1 <= int(b) <= 7:
            hasil.append(int(b))
        elif b in HARI_KATA:
            hasil.append(HARI_KATA[b])
        else:
            raise Gagal("%s: '%s' bukan nama hari. Contoh: sabtu,minggu" % (nama, b))
    return sorted(set(hasil))


def label_hari_list(lst):
    return ",".join(HARI[i - 1].lower() for i in lst) or "-"


# ---------------------------------------------------------------------------
# Membaca file tabel (CSV / XLSX sederhana)
# ---------------------------------------------------------------------------

BATAS_UKURAN = 100 * 1024 * 1024


def _baca_xlsx(path):
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
          "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
          "pr": "http://schemas.openxmlformats.org/package/2006/relationships"}
    try:
        z = zipfile.ZipFile(str(path))
    except zipfile.BadZipFile:
        raise Gagal("File .xlsx rusak atau bukan file Excel asli. Simpan ulang sebagai CSV.")
    with z:
        nama_file = set(z.namelist())
        if any(i.file_size > BATAS_UKURAN for i in z.infolist()):
            raise Gagal("Isi file Excel terlalu besar untuk dibaca.")
        shared = []
        if "xl/sharedStrings.xml" in nama_file:
            for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", ns):
                shared.append("".join(t.text or "" for t in si.iter("{%s}t" % ns["m"])))
        sheet = "xl/worksheets/sheet1.xml"
        try:
            wb = ET.fromstring(z.read("xl/workbook.xml"))
            pertama = wb.find("m:sheets/m:sheet", ns)
            rid = pertama.get("{%s}id" % ns["r"]) if pertama is not None else None
            for rel in ET.fromstring(z.read("xl/_rels/workbook.xml.rels")).findall("pr:Relationship", ns):
                if rel.get("Id") == rid:
                    tg = rel.get("Target").lstrip("/")
                    sheet = tg if tg.startswith("xl/") else "xl/" + tg
        except (KeyError, ET.ParseError, AttributeError):
            pass
        if sheet not in nama_file:
            raise Gagal("Sheet pertama tidak ditemukan di file Excel. Simpan ulang sebagai CSV.")
        akar = ET.fromstring(z.read(sheet))
    semua = []
    for row in akar.iter("{%s}row" % ns["m"]):
        isi = {}
        for c in row.findall("m:c", ns):
            ref = c.get("r") or ""
            hf = re.match(r"[A-Z]+", ref)
            if hf:
                kol = 0
                for ch in hf.group(0):
                    kol = kol * 26 + (ord(ch) - 64)
                kol -= 1
            else:
                kol = len(isi)
            tipe = c.get("t")
            v = c.find("m:v", ns)
            if tipe == "s" and v is not None:
                nilai = shared[int(v.text)] if v.text and int(v.text) < len(shared) else ""
            elif tipe == "inlineStr":
                nilai = "".join(t.text or "" for t in c.iter("{%s}t" % ns["m"]))
            elif v is not None and v.text is not None:
                nilai = v.text
                if tipe not in ("str", "e", "b") and re.fullmatch(r"-?\d+\.0+", nilai):
                    nilai = nilai.split(".")[0]
            else:
                nilai = ""
            isi[kol] = nilai
        semua.append([isi.get(i, "") for i in range(max(isi) + 1)] if isi else [])
    return semua


def baca_tabel(path):
    p = Path(path).expanduser()
    if not p.is_file():
        raise Gagal("File '%s' tidak ditemukan." % path)
    if p.stat().st_size == 0:
        raise Gagal("File '%s' kosong." % p.name)
    if p.stat().st_size > BATAS_UKURAN:
        raise Gagal("File terlalu besar (> 100 MB).")
    if p.suffix.lower() == ".xls":
        raise Gagal("Format .xls (Excel lama) tidak didukung. Buka di Excel lalu Save As CSV atau .xlsx.")
    mentah = p.read_bytes()
    if p.suffix.lower() in (".xlsx", ".xlsm") or mentah[:2] == b"PK":
        return _baca_xlsx(p)
    if mentah[:2] in (b"\xff\xfe", b"\xfe\xff"):
        teks = mentah.decode("utf-16")
    else:
        if b"\x00" in mentah[:4096]:
            raise Gagal("File '%s' bukan file teks/CSV (berisi data biner). Ekspor ulang dari mesin sebagai CSV/XLSX."
                        % p.name)
        teks = None
        for enc in ("utf-8-sig", "cp1252", "latin-1"):
            try:
                teks = mentah.decode(enc)
                break
            except UnicodeDecodeError:
                continue
    contoh = teks[:8192]
    try:
        dialek = csv.Sniffer().sniff(contoh, delimiters=",;\t|")
    except csv.Error:
        jml = {d: contoh.count(d) for d in ",;\t|"}
        pem = max(jml, key=jml.get)

        class dialek(csv.excel):
            delimiter = pem
    try:
        return [list(r) for r in csv.reader(io.StringIO(teks, newline=""), dialect=dialek)]
    except csv.Error as e:
        raise Gagal("CSV rusak dan tidak bisa dibaca (%s). Simpan ulang sebagai CSV." % e)


def deteksi_kolom(header, sinonim):
    """Cocok persis (sesuai urutan prioritas) menang atas cocok sebagian (kata >= 6 huruf)."""
    hn = [norm(h) for h in header]
    dipakai, hasil = set(), {}
    for field, kata in sinonim.items():
        pilih = None
        for k in kata:
            for i, h in enumerate(hn):
                if i not in dipakai and h == k:
                    pilih = i
                    break
            if pilih is not None:
                break
        if pilih is None:
            for k in kata:
                if len(k) < 6:
                    continue
                for i, h in enumerate(hn):
                    if i not in dipakai and h and k in h:
                        pilih = i
                        break
                if pilih is not None:
                    break
        if pilih is not None:
            hasil[field] = pilih
            dipakai.add(pilih)
    return hasil


def cari_header(baris, sinonim, minimal=2):
    terbaik, skor = None, 0
    for i, r in enumerate(baris[:20]):
        s = len(deteksi_kolom(r, sinonim))
        if s > skor:
            terbaik, skor = i, s
    return terbaik if skor >= minimal else None


def sel(r, idx):
    if idx is None or idx >= len(r):
        return ""
    return (r[idx] or "").strip()


def tulis_csv(path, header, rows, pemisah=";"):
    p = Path(path).expanduser()
    if not p.parent.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
    with open(str(p), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=pemisah)
        w.writerow(header)
        for r in rows:
            w.writerow(r)
    return str(p)


# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

DDL = """
CREATE TABLE IF NOT EXISTS meta (kunci TEXT PRIMARY KEY, nilai TEXT);
CREATE TABLE IF NOT EXISTS shift (
  kode TEXT PRIMARY KEY COLLATE NOCASE,
  masuk TEXT NOT NULL, pulang TEXT NOT NULL,
  istirahat INTEGER NOT NULL DEFAULT 60,
  pulang_pendek TEXT NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS karyawan (
  kode TEXT PRIMARY KEY COLLATE NOCASE,
  nama TEXT NOT NULL COLLATE NOCASE,
  jabatan TEXT NOT NULL DEFAULT '',
  shift TEXT NOT NULL DEFAULT 'REG' COLLATE NOCASE,
  hari_kerja INTEGER NOT NULL DEFAULT 5 CHECK (hari_kerja IN (5,6)),
  libur_mingguan TEXT NOT NULL DEFAULT '6,7',
  hari_pendek INTEGER NOT NULL DEFAULT 0,
  id_mesin TEXT NOT NULL DEFAULT '',
  gaji_pokok TEXT NOT NULL DEFAULT '',
  tunjangan_tetap TEXT NOT NULL DEFAULT '',
  tunjangan_tidak_tetap TEXT NOT NULL DEFAULT '',
  upah_harian TEXT NOT NULL DEFAULT '',
  tanpa_lembur INTEGER NOT NULL DEFAULT 0,
  aktif INTEGER NOT NULL DEFAULT 1,
  dibuat TEXT
);
CREATE TABLE IF NOT EXISTS tap (
  id INTEGER PRIMARY KEY,
  kode TEXT NOT NULL COLLATE NOCASE,
  waktu TEXT NOT NULL,
  jenis TEXT NOT NULL DEFAULT '' CHECK (jenis IN ('masuk','pulang','')),
  tanggal_kerja TEXT,
  sumber TEXT NOT NULL DEFAULT 'manual',
  impor_id INTEGER,
  UNIQUE (kode, waktu, jenis)
);
CREATE INDEX IF NOT EXISTS ix_tap ON tap(kode, waktu);
CREATE TABLE IF NOT EXISTS keterangan (
  kode TEXT NOT NULL COLLATE NOCASE, tanggal TEXT NOT NULL,
  jenis TEXT NOT NULL, catatan TEXT NOT NULL DEFAULT '',
  PRIMARY KEY (kode, tanggal)
);
CREATE TABLE IF NOT EXISTS lembur (
  kode TEXT NOT NULL COLLATE NOCASE, tanggal TEXT NOT NULL,
  jam TEXT NOT NULL, catatan TEXT NOT NULL DEFAULT '', dicatat TEXT,
  PRIMARY KEY (kode, tanggal)
);
CREATE TABLE IF NOT EXISTS libur (tanggal TEXT PRIMARY KEY, nama TEXT NOT NULL DEFAULT '');
CREATE TABLE IF NOT EXISTS impor (id INTEGER PRIMARY KEY, waktu TEXT, file TEXT, baris INTEGER, tap_baru INTEGER,
  pemetaan TEXT);
CREATE TABLE IF NOT EXISTS log (id INTEGER PRIMARY KEY, waktu TEXT, perintah TEXT, ringkasan TEXT);
"""

PENGATURAN_DEFAULT = {"toleransi_telat": "0", "jeda_duplikat": "5", "nama_usaha": ""}


def path_db(args):
    if getattr(args, "db", None):
        return Path(args.db).expanduser()
    env = os.environ.get("KOMUNITECH_ABSENSI_DB")
    if env:
        return Path(env).expanduser()
    folder = os.environ.get("KOMUNITECH_DATA")
    if folder:
        return Path(folder).expanduser() / "absensi" / "absensi.db"
    return Path.home() / "KomunitechData" / "absensi" / "absensi.db"


def buka(db, harus_ada=True):
    if harus_ada and not db.is_file():
        raise Gagal("Database absensi belum ada di %s. Jalankan dulu: absensi.py init (lalu --ya)." % db, db=str(db))
    conn = sqlite3.connect(str(db), isolation_level=None)
    conn.row_factory = sqlite3.Row
    if harus_ada:
        try:
            r = conn.execute("SELECT nilai FROM meta WHERE kunci='aplikasi'").fetchone()
        except sqlite3.DatabaseError:
            conn.close()
            raise Gagal("File %s bukan database absensi-lokal (atau rusak)." % db)
        if not r or r[0] != APLIKASI:
            conn.close()
            raise Gagal("File %s bukan database absensi-lokal." % db)
    return conn


def pengaturan(conn):
    cfg = dict(PENGATURAN_DEFAULT)
    for r in conn.execute("SELECT kunci, nilai FROM meta"):
        cfg[r[0]] = r[1]
    return {"toleransi_telat": int(cfg["toleransi_telat"]), "jeda_duplikat": int(cfg["jeda_duplikat"]),
            "nama_usaha": cfg["nama_usaha"]}


def buat_backup(db, label):
    if not db.is_file():
        return None
    fol = db.parent / "backup-absensi"
    fol.mkdir(parents=True, exist_ok=True)
    cap = datetime.now().strftime("%Y%m%d-%H%M%S")
    tujuan = fol / ("absensi-%s-%s.db" % (cap, label))
    n = 2
    while tujuan.exists():
        tujuan = fol / ("absensi-%s-%s-%d.db" % (cap, label, n))
        n += 1
    src, dst = sqlite3.connect(str(db)), sqlite3.connect(str(tujuan))
    try:
        src.backup(dst)
    finally:
        dst.close()
        src.close()
    return tujuan


def jalankan_tulis(args, perintah, kerja, label_backup=None):
    """Jalankan kerja(conn) dalam transaksi. Tanpa --ya -> ROLLBACK (pratinjau)."""
    db = path_db(args)
    conn = buka(db)
    backup = None
    try:
        if args.ya and label_backup:
            backup = buat_backup(db, label_backup)
        conn.execute("BEGIN IMMEDIATE")
        try:
            data, teks = kerja(conn)
        except BaseException:
            conn.execute("ROLLBACK")
            if backup is not None:
                try:
                    backup.unlink()
                except OSError:
                    pass
            raise
        if args.ya:
            conn.execute("INSERT INTO log(waktu, perintah, ringkasan) VALUES (?,?,?)",
                         (sekarang().isoformat(sep=" "), perintah,
                          json.dumps(data.get("ringkasan", {}), ensure_ascii=False, default=str)[:4000]))
            conn.execute("COMMIT")
        else:
            conn.execute("ROLLBACK")
    finally:
        conn.close()
    data = dict(data)
    data.update(ok=True, perintah=perintah, db=str(db))
    if args.ya:
        data["mode"] = "tersimpan"
        if backup:
            data["backup"] = str(backup)
        kepala = "TERSIMPAN." + (" Backup sebelum perubahan: %s" % backup if backup else "")
    else:
        data["mode"] = "pratinjau"
        data["perlu_konfirmasi"] = True
        data["petunjuk"] = ("BELUM DISIMPAN. Tunjukkan ringkasan ini ke pengguna; jika setuju, jalankan ulang "
                            "perintah yang sama dengan tambahan --ya.")
        kepala = "PRATINJAU (belum disimpan). Jika sudah benar, jalankan ulang perintah yang sama dengan --ya."
    return data, kepala + "\n\n" + teks


# ---------------------------------------------------------------------------
# Model: shift & karyawan
# ---------------------------------------------------------------------------


class Shift(object):
    def __init__(self, r):
        self.kode = r["kode"]
        self.masuk = parse_jam(r["masuk"])
        self.pulang = parse_jam(r["pulang"])
        self.istirahat = int(r["istirahat"])
        self.pulang_pendek = parse_jam(r["pulang_pendek"]) if r["pulang_pendek"] else None

    @property
    def lintas_malam(self):
        return self.pulang <= self.masuk

    def jendela(self, d, pendek):
        """(mulai, selesai, istirahat_menit) jadwal untuk tanggal kerja d."""
        jp = self.pulang_pendek if (pendek and self.pulang_pendek) else self.pulang
        mulai = datetime.combine(d, self.masuk)
        selesai = datetime.combine(d, jp)
        if selesai <= mulai:
            selesai += timedelta(days=1)
        ist = 0 if (pendek and self.pulang_pendek) else self.istirahat
        return mulai, selesai, ist

    def label(self):
        t = "%s %s-%s" % (self.kode, fjm(self.masuk), fjm(self.pulang))
        if self.lintas_malam:
            t += " (lewat tengah malam)"
        if self.pulang_pendek:
            t += ", hari pendek pulang %s" % fjm(self.pulang_pendek)
        return t + ", istirahat %d menit" % self.istirahat


class Karyawan(object):
    def __init__(self, r, shift):
        self.kode = r["kode"]
        self.nama = r["nama"]
        self.jabatan = r["jabatan"]
        self.shift = shift
        self.hari_kerja = int(r["hari_kerja"])
        self.libur_mingguan = [int(x) for x in r["libur_mingguan"].split(",") if x.strip()]
        self.hari_pendek = int(r["hari_pendek"])
        self.id_mesin = r["id_mesin"]
        self.gaji_pokok = parse_angka(r["gaji_pokok"])
        self.tunjangan_tetap = parse_angka(r["tunjangan_tetap"])
        self.tunjangan_tidak_tetap = parse_angka(r["tunjangan_tidak_tetap"])
        self.upah_harian = parse_angka(r["upah_harian"])
        self.tanpa_lembur = bool(r["tanpa_lembur"])
        self.aktif = bool(r["aktif"])

    def pendek(self, d):
        return self.hari_kerja == 6 and self.hari_pendek and d.isoweekday() == self.hari_pendek

    def dasar_lembur(self):
        """(upah sebulan dasar lembur, penjelasan) atau (None, alasan). PP 35/2021 Pasal 32-33."""
        if self.upah_harian:
            kali = 25 if self.hari_kerja == 6 else 21
            return (self.upah_harian * kali,
                    "upah harian %s x %d (Pasal 33 ayat (1) huruf %s)" % (rp(self.upah_harian), kali,
                                                                         "a" if kali == 25 else "b"))
        if not self.gaji_pokok:
            return None, "gaji pokok belum diisi"
        tetap = self.gaji_pokok + (self.tunjangan_tetap or 0)
        tt = self.tunjangan_tidak_tetap or Decimal(0)
        if tt > 0 and tetap < (tetap + tt) * Decimal("0.75"):
            return ((tetap + tt) * Decimal("0.75"),
                    "75%% x seluruh upah %s karena gaji pokok + tunjangan tetap < 75%% (Pasal 32 ayat (4))"
                    % rp(tetap + tt))
        return tetap, "gaji pokok + tunjangan tetap (Pasal 32 ayat (3))"


def muat_shift(conn):
    return {r["kode"].upper(): Shift(r) for r in conn.execute("SELECT * FROM shift")}


def muat_karyawan(conn, hanya_aktif=False):
    sh = muat_shift(conn)
    out = []
    for r in conn.execute("SELECT * FROM karyawan ORDER BY kode"):
        if hanya_aktif and not r["aktif"]:
            continue
        s = sh.get(r["shift"].upper())
        if s is None:
            raise Gagal("Shift '%s' milik karyawan %s tidak ada. Tambahkan dengan: shift tambah" % (r["shift"], r["kode"]))
        out.append(Karyawan(r, s))
    return out


def cari_karyawan(conn, teks):
    """Cari berdasarkan kode, id mesin, lalu nama (persis, lalu awalan). Ambigu -> Gagal."""
    t = (teks or "").strip()
    if not t:
        raise Gagal("Nama/kode karyawan kosong.")
    semua = muat_karyawan(conn)
    for k in semua:
        if k.kode.lower() == t.lower():
            return k
    cocok = [k for k in semua if k.nama.lower() == t.lower()] or \
        [k for k in semua if k.id_mesin and k.id_mesin == t] or \
        [k for k in semua if k.nama.lower().startswith(t.lower())]
    if len(cocok) == 1:
        return cocok[0]
    if not cocok:
        raise Gagal("Karyawan '%s' tidak dikenal. Daftarkan dulu dengan: karyawan tambah" % t,
                    karyawan_terdaftar=[k.kode + " " + k.nama for k in semua][:30])
    raise Gagal("Nama '%s' cocok dengan lebih dari satu karyawan: %s. Pakai kode karyawan."
                % (t, ", ".join("%s (%s)" % (k.nama, k.kode) for k in cocok)))


def libur_set(conn, dari, sampai):
    return {r[0]: r[1] for r in conn.execute("SELECT tanggal, nama FROM libur WHERE tanggal BETWEEN ? AND ?",
                                             (dari.isoformat(), sampai.isoformat()))}


def jenis_hari(k, d, libur):
    if d.isoformat() in libur:
        return "libur-resmi"
    if d.isoweekday() in k.libur_mingguan:
        return "istirahat"
    return "kerja"


# ---------------------------------------------------------------------------
# Lembur (PP 35/2021 Pasal 31)
# ---------------------------------------------------------------------------


def jam_setara_hari_kerja(jam):
    """Pasal 31 ayat (1): jam pertama 1,5x, jam berikutnya 2x."""
    jam = Decimal(jam)
    return Decimal("1.5") * min(jam, Decimal(1)) + Decimal(2) * max(jam - 1, Decimal(0))


def jam_setara_libur(jam, pola):
    """Pasal 31 ayat (2)/(3). pola: '5', '6', '6p'. Kembalikan (jam_setara, None) atau (None, pesan)."""
    tangga = TANGGA_LIBUR[pola]
    maks = sum(n for n, _ in tangga)
    jam = Decimal(jam)
    if jam > maks:
        return None, "melebihi %d jam yang diatur Pasal 31 untuk pola ini" % maks
    sisa, setara = jam, Decimal(0)
    for n, kali in tangga:
        pakai = min(sisa, Decimal(n))
        setara += pakai * kali
        sisa -= pakai
        if sisa <= 0:
            break
    return setara, None


# ---------------------------------------------------------------------------
# Analisis harian
# ---------------------------------------------------------------------------


def _dt(s):
    return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")


def analisa_karyawan(conn, k, dari, sampai, cfg, libur, kini):
    """Kembalikan (daftar_hari, masalah, lembur_rows)."""
    masalah = []
    tambah = lambda tgl, kode, pesan, berat="cek": masalah.append(
        {"kode_karyawan": k.kode, "nama": k.nama, "tanggal": tgl.isoformat() if tgl else "", "jenis": kode,
         "tingkat": berat, "pesan": pesan})
    batas_bawah = datetime.combine(dari - timedelta(days=1), time(0))
    batas_atas = datetime.combine(sampai + timedelta(days=2), time(0))
    rows = conn.execute(
        "SELECT * FROM tap WHERE kode=? AND ((tanggal_kerja BETWEEN ? AND ?) OR "
        "(tanggal_kerja IS NULL AND waktu >= ? AND waktu < ?)) ORDER BY waktu",
        (k.kode, dari.isoformat(), sampai.isoformat(), batas_bawah.isoformat(sep=" "),
         batas_atas.isoformat(sep=" "))).fetchall()
    per_hari = defaultdict(list)
    for r in rows:
        w = _dt(r["waktu"])
        if r["tanggal_kerja"]:
            d = date.fromisoformat(r["tanggal_kerja"])
        else:
            kand = []
            for d0 in (w.date(), w.date() - timedelta(days=1)):
                mulai, selesai, _ = k.shift.jendela(d0, k.pendek(d0))
                if mulai - timedelta(hours=4) <= w <= selesai + timedelta(hours=8):
                    kand.append((min(abs(w - mulai), abs(w - selesai)), d0))
            if not kand:
                if dari <= w.date() <= sampai:
                    tambah(w.date(), "tap_di_luar_shift",
                           "tap %s %s jauh di luar jadwal shift %s, tidak dipakai" % (ftgl(w), fjm(w), k.shift.kode))
                continue
            d = min(kand)[1]
        if dari <= d <= sampai:
            per_hari[d].append((w, r["jenis"], r["sumber"]))
    ket = {r["tanggal"]: r for r in conn.execute(
        "SELECT * FROM keterangan WHERE kode=? AND tanggal BETWEEN ? AND ?",
        (k.kode, dari.isoformat(), sampai.isoformat()))}
    lem = {r["tanggal"]: r for r in conn.execute(
        "SELECT * FROM lembur WHERE kode=? AND tanggal BETWEEN ? AND ?",
        (k.kode, dari.isoformat(), sampai.isoformat()))}
    hari = []
    d = dari
    while d <= sampai:
        if d > kini.date():
            break
        jh = jenis_hari(k, d, libur)
        pendek = bool(k.pendek(d))
        mulai, selesai, ist = k.shift.jendela(d, pendek)
        h = {"tanggal": d.isoformat(), "hari": HARI[d.weekday()], "jenis_hari": jh, "hari_pendek": pendek,
             "jadwal_masuk": fjm(mulai), "jadwal_pulang": fjm(selesai), "masuk": None, "pulang": None,
             "status": None, "terlambat_menit": 0, "pulang_cepat_menit": 0, "menit_kerja": None,
             "keterangan": None, "lembur_jam": None}
        taps = sorted(per_hari.get(d, []))
        # buang tap ganda (jarak <= jeda_duplikat menit, jenis sama/kosong)
        bersih, ganda = [], 0
        for t in taps:
            if bersih and (t[0] - bersih[-1][0]) <= timedelta(minutes=cfg["jeda_duplikat"]) and \
                    (t[1] == bersih[-1][1] or "" in (t[1], bersih[-1][1])):
                ganda += 1
                continue
            bersih.append(t)
        if ganda:
            tambah(d, "tap_ganda", "%d tap ganda (jarak <= %d menit) diabaikan" % (ganda, cfg["jeda_duplikat"]),
                   "info")
        m_list = [t[0] for t in bersih if t[1] == "masuk"]
        p_list = [t[0] for t in bersih if t[1] == "pulang"]
        u_list = [t[0] for t in bersih if t[1] == ""]
        masuk = min(m_list) if m_list else None
        pulang = max(p_list) if p_list else None
        if len(m_list) > 1:
            tambah(d, "masuk_ganda", "ada %d catatan masuk (%s); dipakai yang paling awal"
                   % (len(m_list), ", ".join(fjm(x) for x in m_list)))
        if len(p_list) > 1:
            tambah(d, "pulang_ganda", "ada %d catatan pulang (%s); dipakai yang paling akhir"
                   % (len(p_list), ", ".join(fjm(x) for x in p_list)))
        if u_list:
            if masuk is None and pulang is None:
                if len(u_list) == 1:
                    w = u_list[0]
                    if abs(w - mulai) <= abs(w - selesai):
                        masuk = w
                    else:
                        pulang = w
                else:
                    masuk, pulang = u_list[0], u_list[-1]
            elif masuk is None:
                sisa = [x for x in u_list if x < pulang]
                masuk = sisa[0] if sisa else None
            elif pulang is None:
                sisa = [x for x in u_list if x > masuk]
                pulang = sisa[-1] if sisa else None
        h["masuk"] = masuk.isoformat(sep=" ") if masuk else None
        h["pulang"] = pulang.isoformat(sep=" ") if pulang else None
        kt = ket.get(d.isoformat())
        if kt:
            h["keterangan"] = kt["jenis"]
        ada_tap = bool(bersih)
        valid = True
        if masuk and pulang and pulang <= masuk:
            valid = False
            tambah(d, "pulang_sebelum_masuk", "pulang %s tercatat sebelum masuk %s; jam kerja tidak dihitung"
                   % (fjm(pulang), fjm(masuk)), "salah")
        elif masuk and pulang and (pulang - masuk) > timedelta(hours=18):
            valid = False
            tambah(d, "durasi_tidak_wajar", "masuk %s s.d. pulang %s = %s; tidak dihitung, cek data"
                   % (fjm(masuk), pulang.strftime("%d/%m %H.%M"), fmenit((pulang - masuk).total_seconds() // 60)),
                   "salah")
        if ada_tap and (masuk is None or pulang is None):
            belum = pulang is None and masuk is not None and kini < selesai + timedelta(hours=8)
            if not belum:
                tambah(d, "tap_tidak_lengkap", "hanya ada jam %s (%s); jam %s tidak tercatat"
                       % ("masuk" if masuk else "pulang", fjm(masuk or pulang), "pulang" if masuk else "masuk"),
                       "salah")
        if kt and ada_tap and kt["jenis"] != "dinas":
            tambah(d, "keterangan_dan_tap", "tercatat %s tetapi ada tap absen; pastikan mana yang benar"
                   % kt["jenis"])
        if kt:
            h["status"] = kt["jenis"]
        elif ada_tap:
            h["status"] = "hadir" if jh == "kerja" else "hadir di hari libur"
        elif jh == "kerja":
            h["status"] = "tanpa keterangan"
        else:
            h["status"] = "libur"
        if ada_tap and valid and masuk and pulang:
            durasi = int((pulang - masuk).total_seconds() // 60)
            h["menit_kerja"] = max(durasi - (ist if durasi > 240 else 0), 0)
        if ada_tap and jh == "kerja" and not kt:
            if masuk:
                tl = int((masuk - mulai).total_seconds() // 60)
                if tl > cfg["toleransi_telat"]:
                    h["terlambat_menit"] = tl
            if pulang and valid and pulang < selesai:
                h["pulang_cepat_menit"] = int((selesai - pulang).total_seconds() // 60)
                if h["pulang_cepat_menit"] == 0:
                    h["pulang_cepat_menit"] = 0
        h["_mulai"], h["_selesai"], h["_masuk"], h["_pulang"], h["_valid"] = mulai, selesai, masuk, pulang, valid
        hari.append(h)
        d += timedelta(days=1)
    # lembur yang disetujui untuk tanggal di luar hari yang dianalisis (mis. tanggal masa depan)
    for tgl in sorted(lem):
        if date.fromisoformat(tgl) > kini.date():
            tambah(date.fromisoformat(tgl), "lembur_masa_depan", "lembur tanggal ini belum terjadi; tidak dihitung",
                   "info")
    return hari, masalah, lem


def hitung_lembur(k, hari, lem, libur, masalah):
    """Upah lembur dari daftar lembur DISETUJUI saja. Kembalikan dict ringkasan."""
    tambah = lambda tgl, kode, pesan, berat="cek": masalah.append(
        {"kode_karyawan": k.kode, "nama": k.nama, "tanggal": tgl, "jenis": kode, "tingkat": berat, "pesan": pesan})
    per_tgl = {h["tanggal"]: h for h in hari}
    rincian, setara_total = [], Decimal(0)
    jam_kerja_list, jam_libur_list = [], []
    per_minggu = defaultdict(Decimal)
    for tgl in sorted(lem):
        h = per_tgl.get(tgl)
        if h is None:
            continue
        jam = Decimal(lem[tgl]["jam"])
        d = date.fromisoformat(tgl)
        jh = h["jenis_hari"]
        item = {"tanggal": tgl, "hari": HARI[d.weekday()], "jenis_hari": jh, "jam": jam,
                "catatan": lem[tgl]["catatan"], "jam_setara": None, "dihitung": False, "pola": None}
        h["lembur_jam"] = jam
        if h["keterangan"] in ("izin", "sakit", "cuti", "alpa"):
            tambah(tgl, "lembur_saat_tidak_hadir", "lembur %s jam disetujui, tetapi hari itu tercatat %s; lembur "
                   "TIDAK dihitung sampai diperbaiki" % (fjam(jam), h["keterangan"]), "salah")
            rincian.append(item)
            continue
        if jh == "kerja":
            item["pola"] = "hari kerja"
            item["jam_setara"] = jam_setara_hari_kerja(jam)
            if jam > MAKS_LEMBUR_HARI_KERJA:
                tambah(tgl, "lembur_lebih_4_jam", "lembur hari kerja %s jam melebihi batas 4 jam/hari (PP 35/2021 "
                       "Pasal 26 ayat (1)); tetap dihitung sesuai jam yang disetujui" % fjam(jam))
            iso = d.isocalendar()
            per_minggu[(iso[0], iso[1])] += jam
            jam_kerja_list.append(jam)
            aktual = None
            if h["_pulang"] and h["_valid"] and h["_pulang"] > h["_selesai"]:
                aktual = Decimal(int((h["_pulang"] - h["_selesai"]).total_seconds() // 60)) / 60
            elif h["_pulang"] and h["_valid"]:
                aktual = Decimal(0)
        else:
            pola = str(k.hari_kerja)
            if k.hari_kerja == 6 and jh == "libur-resmi" and k.hari_pendek and d.isoweekday() == k.hari_pendek:
                pola = "6p"
            item["pola"] = {"5": "libur, 5 hari kerja", "6": "libur, 6 hari kerja",
                            "6p": "libur resmi di hari kerja terpendek, 6 hari kerja"}[pola]
            setara, err = jam_setara_libur(jam, pola)
            if err:
                tambah(tgl, "lembur_libur_melebihi_aturan", "lembur hari libur %s jam %s; TIDAK dihitung, perbaiki "
                       "jumlah jamnya" % (fjam(jam), err), "salah")
                rincian.append(item)
                continue
            item["jam_setara"] = setara
            jam_libur_list.append((jam, pola == "6p"))
            aktual = Decimal(h["menit_kerja"]) / 60 if h["menit_kerja"] is not None else None
        if not h["masuk"] and not h["pulang"] and h["keterangan"] != "dinas":
            tambah(tgl, "lembur_tanpa_absen", "lembur %s jam disetujui tetapi tidak ada tap absen hari itu; "
                   "tetap dihitung, pastikan lemburnya benar dilaksanakan" % fjam(jam))
        elif aktual is not None and jam > aktual + Decimal("0.25"):
            tambah(tgl, "lembur_lebih_dari_absen", "lembur disetujui %s jam, tetapi menurut jam absen hanya sekitar "
                   "%s; dihitung sesuai jam yang disetujui, mohon dicek" % (fjam(jam), fmenit(int(aktual * 60))))
        item["dihitung"] = True
        setara_total += item["jam_setara"]
        rincian.append(item)
    for (th, mg), total in sorted(per_minggu.items()):
        if total > MAKS_LEMBUR_MINGGU:
            tambah("", "lembur_lebih_18_jam_seminggu", "lembur hari kerja minggu ke-%d/%d = %s jam, melebihi 18 "
                   "jam/minggu (PP 35/2021 Pasal 26 ayat (1))" % (mg, th, fjam(total)))
    dasar, alasan = k.dasar_lembur()
    hasil = {"rincian": rincian, "jam_hari_kerja": sum(jam_kerja_list, Decimal(0)),
             "jam_hari_libur": sum((j for j, _ in jam_libur_list), Decimal(0)), "jam_setara": setara_total,
             "dasar_upah": dasar, "dasar_keterangan": alasan, "upah_sejam": None, "total": None,
             "tanpa_lembur": k.tanpa_lembur, "list_kerja": jam_kerja_list, "list_libur": jam_libur_list}
    if k.tanpa_lembur:
        if rincian:
            tambah("", "golongan_jabatan_tertentu", "karyawan ditandai golongan jabatan tertentu (tanpa upah "
                   "lembur, PP 35/2021 Pasal 27 ayat (2)-(4)); lembur yang dicatat tidak dibayar", "info")
        hasil["total"] = 0
        return hasil
    if dasar is not None:
        hasil["upah_sejam"] = dasar / PEMBAGI_UPAH_SEJAM
        hasil["total"] = bulat_rp(setara_total * dasar / PEMBAGI_UPAH_SEJAM)
        for it in rincian:
            if it["dihitung"]:
                it["nominal"] = bulat_rp(it["jam_setara"] * dasar / PEMBAGI_UPAH_SEJAM)
    elif setara_total > 0:
        tambah("", "upah_belum_diisi", "ada lembur %s jam setara, tetapi upah belum diisi sehingga rupiahnya belum "
               "dihitung (isi --gaji-pokok/--tunjangan-tetap atau --upah-harian)" % fjam(setara_total), "info")
    return hasil


def ringkas_karyawan(k, hari, lemb):
    r = {"kode": k.kode, "nama": k.nama, "jabatan": k.jabatan, "hari_kerja_per_minggu": k.hari_kerja,
         "shift": k.shift.kode}
    r["hari_terjadwal"] = sum(1 for h in hari if h["jenis_hari"] == "kerja")
    r["hadir"] = sum(1 for h in hari if h["status"] == "hadir")
    r["hadir_di_hari_libur"] = sum(1 for h in hari if h["status"] == "hadir di hari libur")
    for j in JENIS_KET:
        r[j] = sum(1 for h in hari if h["status"] == j)
    r["tanpa_keterangan"] = sum(1 for h in hari if h["status"] == "tanpa keterangan")
    r["tanggal_tanpa_keterangan"] = [h["tanggal"] for h in hari if h["status"] == "tanpa keterangan"]
    r["terlambat_kali"] = sum(1 for h in hari if h["terlambat_menit"] > 0)
    r["terlambat_menit"] = sum(h["terlambat_menit"] for h in hari)
    r["pulang_cepat_kali"] = sum(1 for h in hari if h["pulang_cepat_menit"] > 0)
    r["pulang_cepat_menit"] = sum(h["pulang_cepat_menit"] for h in hari)
    r["menit_kerja"] = sum(h["menit_kerja"] or 0 for h in hari)
    r["hari_tidak_lengkap"] = sum(1 for h in hari if (h["masuk"] or h["pulang"]) and h["menit_kerja"] is None)
    r["lembur_jam_hari_kerja"] = lemb["jam_hari_kerja"]
    r["lembur_jam_hari_libur"] = lemb["jam_hari_libur"]
    r["lembur_jam_setara"] = lemb["jam_setara"]
    r["dasar_upah_lembur"] = bulat_rp(lemb["dasar_upah"]) if lemb["dasar_upah"] is not None else None
    r["dasar_upah_keterangan"] = lemb["dasar_keterangan"]
    r["upah_sejam"] = str(lemb["upah_sejam"].quantize(Decimal("0.01"))) if lemb["upah_sejam"] is not None else None
    r["upah_lembur"] = lemb["total"]
    r["tanpa_lembur"] = lemb["tanpa_lembur"]
    r["lembur_rincian"] = [{kk: (str(v) if isinstance(v, Decimal) else v) for kk, v in it.items()}
                           for it in lemb["rincian"]]
    r["_list_kerja"], r["_list_libur"] = lemb["list_kerja"], lemb["list_libur"]
    return r


def analisa_semua(conn, dari, sampai, kini, kode=None, pola=None):
    cfg = pengaturan(conn)
    libur = libur_set(conn, dari, sampai)
    semua = muat_karyawan(conn)
    if kode:
        k = cari_karyawan(conn, kode)
        semua = [x for x in semua if x.kode == k.kode]
    if pola:
        semua = [x for x in semua if x.hari_kerja == int(pola)]
    hasil, masalah, harian = [], [], {}
    for k in semua:
        punya_data = conn.execute(
            "SELECT 1 FROM tap WHERE kode=? AND waktu BETWEEN ? AND ? UNION SELECT 1 FROM keterangan WHERE kode=? "
            "AND tanggal BETWEEN ? AND ? UNION SELECT 1 FROM lembur WHERE kode=? AND tanggal BETWEEN ? AND ?",
            (k.kode, dari.isoformat(), (sampai + timedelta(days=2)).isoformat(), k.kode, dari.isoformat(),
             sampai.isoformat(), k.kode, dari.isoformat(), sampai.isoformat())).fetchone()
        if not k.aktif and not punya_data:
            continue
        hari, m, lem = analisa_karyawan(conn, k, dari, sampai, cfg, libur, kini)
        lemb = hitung_lembur(k, hari, lem, libur, m)
        hasil.append(ringkas_karyawan(k, hari, lemb))
        harian[k.kode] = hari
        masalah.extend(m)
    return cfg, libur, hasil, masalah, harian


# ---------------------------------------------------------------------------
# Perintah: init, atur, info, backup
# ---------------------------------------------------------------------------


def cmd_init(args):
    db = path_db(args)
    if db.is_file():
        conn = buka(db)
        n = conn.execute("SELECT COUNT(*) FROM karyawan").fetchone()[0]
        conn.close()
        return ({"ok": True, "mode": "baca", "db": str(db), "sudah_ada": True, "jumlah_karyawan": n},
                "Database absensi sudah ada di %s (%d karyawan). Tidak ada yang diubah." % (db, n))
    teks = ("Akan dibuat database absensi baru:\n  %s\nShift bawaan: REG 08.00-17.00, istirahat 60 menit "
            "(bisa diubah). Toleransi terlambat bawaan: 0 menit (atur dengan: atur --toleransi 10)." % db)
    info = {"ok": True, "db": str(db), "perintah": "init"}
    if not args.ya:
        info.update(mode="pratinjau", perlu_konfirmasi=True,
                    petunjuk="BELUM DIBUAT. Konfirmasi lokasi ke pengguna, lalu jalankan ulang dengan --ya.")
        return info, "PRATINJAU. " + teks + "\nJalankan ulang dengan --ya untuk membuat."
    db.parent.mkdir(parents=True, exist_ok=True)
    conn = buka(db, harus_ada=False)
    conn.executescript(DDL)
    for kk, v in (("aplikasi", APLIKASI), ("skema", str(SKEMA)), ("dibuat", sekarang().isoformat(sep=" "))):
        conn.execute("INSERT OR REPLACE INTO meta VALUES (?,?)", (kk, v))
    for kk, v in PENGATURAN_DEFAULT.items():
        conn.execute("INSERT OR IGNORE INTO meta VALUES (?,?)", (kk, v))
    conn.execute("INSERT OR IGNORE INTO shift(kode, masuk, pulang, istirahat) VALUES ('REG','08:00','17:00',60)")
    conn.close()
    info.update(mode="tersimpan")
    return info, "TERSIMPAN. Database absensi dibuat di %s" % db


def cmd_atur(args):
    def kerja(conn):
        ubah = {}
        if args.toleransi is not None:
            if not 0 <= args.toleransi <= 120:
                raise Gagal("Toleransi terlambat harus 0-120 menit.")
            ubah["toleransi_telat"] = str(args.toleransi)
        if args.jeda_duplikat is not None:
            if not 0 <= args.jeda_duplikat <= 60:
                raise Gagal("Jeda tap ganda harus 0-60 menit.")
            ubah["jeda_duplikat"] = str(args.jeda_duplikat)
        if args.nama_usaha is not None:
            ubah["nama_usaha"] = args.nama_usaha.strip()
        lama = pengaturan(conn)
        for kk, v in ubah.items():
            conn.execute("INSERT OR REPLACE INTO meta VALUES (?,?)", (kk, v))
        baru = pengaturan(conn)
        teks = "Pengaturan:\n- Toleransi terlambat: %d menit\n- Tap ganda jika jaraknya <= %d menit\n- Nama usaha: %s" \
            % (baru["toleransi_telat"], baru["jeda_duplikat"], baru["nama_usaha"] or "-")
        return {"sebelum": lama, "sesudah": baru, "ringkasan": ubah}, teks
    return jalankan_tulis(args, "atur", kerja)


def cmd_info(args):
    db = path_db(args)
    conn = buka(db)
    try:
        cfg = pengaturan(conn)
        q = lambda s: conn.execute(s).fetchone()[0]
        data = {"ok": True, "mode": "baca", "db": str(db), "versi_script": VERSI, "pengaturan": cfg,
                "karyawan_aktif": q("SELECT COUNT(*) FROM karyawan WHERE aktif=1"),
                "jumlah_tap": q("SELECT COUNT(*) FROM tap"), "tap_terakhir": q("SELECT MAX(waktu) FROM tap"),
                "shift": [s.label() for s in muat_shift(conn).values()],
                "libur_tercatat": q("SELECT COUNT(*) FROM libur")}
    finally:
        conn.close()
    teks = ("Database: %s\nKaryawan aktif: %d | Tap tercatat: %d (terakhir %s)\nShift: %s\nToleransi terlambat: %d "
            "menit | Libur resmi tercatat: %d" % (db, data["karyawan_aktif"], data["jumlah_tap"],
                                                   data["tap_terakhir"] or "-", "; ".join(data["shift"]),
                                                   cfg["toleransi_telat"], data["libur_tercatat"]))
    return data, teks


def cmd_backup(args):
    db = path_db(args)
    buka(db).close()
    b = buat_backup(db, "manual")
    return {"ok": True, "mode": "tersimpan", "backup": str(b)}, "Backup dibuat: %s" % b


# ---------------------------------------------------------------------------
# Shift & libur
# ---------------------------------------------------------------------------


def cmd_shift_tambah(args):
    def kerja(conn):
        kode = args.kode.strip().upper()
        if not re.fullmatch(r"[A-Z0-9_-]{1,20}", kode):
            raise Gagal("Kode shift hanya huruf/angka tanpa spasi, mis. PAGI, MALAM, REG.")
        ada = conn.execute("SELECT * FROM shift WHERE kode=?", (kode,)).fetchone()
        masuk = jam_wajib(args.masuk, "masuk shift") if args.masuk else (parse_jam(ada["masuk"]) if ada else None)
        pulang = jam_wajib(args.pulang, "pulang shift") if args.pulang else (parse_jam(ada["pulang"]) if ada else None)
        if masuk is None or pulang is None:
            raise Gagal("Shift baru wajib diisi --masuk dan --pulang.")
        if masuk == pulang:
            raise Gagal("Jam masuk dan pulang shift tidak boleh sama.")
        ist = args.istirahat if args.istirahat is not None else (ada["istirahat"] if ada else 60)
        if not 0 <= ist <= 240:
            raise Gagal("Istirahat harus 0-240 menit.")
        pp = ada["pulang_pendek"] if ada else ""
        if args.pulang_hari_pendek is not None:
            pp = "" if args.pulang_hari_pendek.strip() in ("", "-") else \
                jam_wajib(args.pulang_hari_pendek, "pulang hari pendek").strftime("%H:%M")
        conn.execute("INSERT OR REPLACE INTO shift VALUES (?,?,?,?,?)",
                     (kode, masuk.strftime("%H:%M"), pulang.strftime("%H:%M"), ist, pp))
        s = Shift(conn.execute("SELECT * FROM shift WHERE kode=?", (kode,)).fetchone())
        mulai, selesai, _ = s.jendela(date(2026, 1, 5), False)
        menit = int((selesai - mulai).total_seconds() // 60) - (ist if (selesai - mulai).total_seconds() > 14400 else 0)
        teks = "%s shift %s\nJam kerja efektif per hari: %s" % ("Ubah" if ada else "Tambah", s.label(), fmenit(menit))
        return {"shift": s.label(), "menit_kerja_per_hari": menit, "ringkasan": {"shift": kode}}, teks
    return jalankan_tulis(args, "shift tambah", kerja)


def cmd_shift_daftar(args):
    conn = buka(path_db(args))
    try:
        sh = [s.label() for s in muat_shift(conn).values()]
    finally:
        conn.close()
    return {"ok": True, "mode": "baca", "shift": sh}, "Daftar shift:\n" + "\n".join("- " + s for s in sh)


def cmd_libur_tambah(args):
    def kerja(conn):
        baris = []
        if args.file:
            tabel = baca_tabel(args.file)
            sin = {"tanggal": ["tanggal", "tgl", "date"], "nama": ["nama", "keterangan", "libur", "name"]}
            hi = cari_header(tabel, sin, minimal=1)
            if hi is None:
                raise Gagal("File libur wajib punya kolom 'tanggal' (dan 'nama').")
            kol = deteksi_kolom(tabel[hi], sin)
            for i, r in enumerate(tabel[hi + 1:], start=hi + 2):
                if not any(c.strip() for c in r):
                    continue
                d = parse_tanggal(sel(r, kol.get("tanggal")))
                if d is None:
                    raise Gagal("Baris %d: tanggal '%s' tidak valid." % (i, sel(r, kol.get("tanggal"))))
                baris.append((d, sel(r, kol.get("nama"))))
        else:
            if not args.tanggal:
                raise Gagal("Isi --tanggal (dan --nama) atau --file daftar-libur.csv")
            baris.append((tanggal_wajib(args.tanggal), args.nama or ""))
        for d, n in baris:
            conn.execute("INSERT OR REPLACE INTO libur VALUES (?,?)", (d.isoformat(), n))
        teks = "Hari libur resmi yang dicatat (%d):\n" % len(baris) + "\n".join(
            "- %s %s %s" % (HARI[d.weekday()], ftgl(d), n) for d, n in baris)
        return {"libur": [{"tanggal": d.isoformat(), "nama": n} for d, n in baris],
                "ringkasan": {"libur": len(baris)}}, teks
    return jalankan_tulis(args, "libur tambah", kerja)


def cmd_libur_hapus(args):
    def kerja(conn):
        d = tanggal_wajib(args.tanggal)
        n = conn.execute("DELETE FROM libur WHERE tanggal=?", (d.isoformat(),)).rowcount
        if not n:
            raise Gagal("Tidak ada libur tercatat pada %s." % ftgl(d))
        return {"ringkasan": {"hapus_libur": d.isoformat()}}, "Hapus hari libur %s" % ftgl(d)
    return jalankan_tulis(args, "libur hapus", kerja)


def cmd_libur_daftar(args):
    conn = buka(path_db(args))
    try:
        th = args.tahun or str(sekarang(args).year)
        rows = conn.execute("SELECT * FROM libur WHERE tanggal LIKE ? ORDER BY tanggal", (th + "-%",)).fetchall()
    finally:
        conn.close()
    data = [{"tanggal": r["tanggal"], "nama": r["nama"]} for r in rows]
    teks = "Libur resmi tercatat %s (%d):\n" % (th, len(data)) + "\n".join(
        "- %s %s" % (ftgl(date.fromisoformat(x["tanggal"])), x["nama"]) for x in data)
    return {"ok": True, "mode": "baca", "libur": data}, teks


# ---------------------------------------------------------------------------
# Karyawan
# ---------------------------------------------------------------------------

KOLOM_KARYAWAN = ["kode", "nama", "jabatan", "shift", "hari_kerja", "libur_mingguan", "hari_pendek", "id_mesin",
                  "gaji_pokok", "tunjangan_tetap", "tunjangan_tidak_tetap", "upah_harian", "tanpa_lembur"]


def _siapkan_karyawan(conn, d, lama=None):
    """d: dict str mentah (kunci KOLOM_KARYAWAN; None = tidak diubah). Kembalikan dict siap simpan + peringatan."""
    out = dict(lama) if lama else {"jabatan": "", "shift": "REG", "hari_kerja": 5, "libur_mingguan": None,
                                   "hari_pendek": None, "id_mesin": "", "gaji_pokok": "", "tunjangan_tetap": "",
                                   "tunjangan_tidak_tetap": "", "upah_harian": "", "tanpa_lembur": 0, "aktif": 1}
    per = []
    if d.get("kode") is not None:
        kode = d["kode"].strip().upper()
        if not re.fullmatch(r"[A-Z0-9_.-]{1,20}", kode):
            raise Gagal("Kode karyawan '%s' tidak valid (huruf/angka tanpa spasi, mis. A01)." % d["kode"])
        out["kode"] = kode
    if d.get("nama") is not None:
        if not d["nama"].strip():
            raise Gagal("Nama karyawan kosong.")
        out["nama"] = re.sub(r"\s+", " ", d["nama"].strip())
    if d.get("jabatan") is not None:
        out["jabatan"] = d["jabatan"].strip()
    if d.get("shift") is not None and d["shift"].strip():
        s = d["shift"].strip().upper()
        if not conn.execute("SELECT 1 FROM shift WHERE kode=?", (s,)).fetchone():
            raise Gagal("Shift '%s' belum ada. Tambahkan dulu: shift tambah --kode %s --masuk .. --pulang .." % (s, s))
        out["shift"] = s
    pola_berubah = False
    if d.get("hari_kerja") is not None and str(d["hari_kerja"]).strip():
        hk = str(d["hari_kerja"]).strip()
        if hk not in ("5", "6"):
            raise Gagal("Hari kerja per minggu harus 5 atau 6 (PP 35/2021 Pasal 21 ayat (2)).")
        pola_berubah = int(hk) != int(out["hari_kerja"])
        out["hari_kerja"] = int(hk)
    if d.get("libur_mingguan") is not None and str(d["libur_mingguan"]).strip():
        out["libur_mingguan"] = ",".join(str(x) for x in parse_hari_list(d["libur_mingguan"], "libur mingguan"))
    elif out["libur_mingguan"] is None or pola_berubah:
        out["libur_mingguan"] = "6,7" if out["hari_kerja"] == 5 else "7"
    if d.get("hari_pendek") is not None and str(d["hari_pendek"]).strip():
        hp = parse_hari_list(d["hari_pendek"], "hari pendek")
        if len(hp) > 1:
            raise Gagal("Hari kerja terpendek hanya satu hari.")
        out["hari_pendek"] = hp[0] if hp else 0
    elif out["hari_pendek"] is None or pola_berubah:
        out["hari_pendek"] = 6 if out["hari_kerja"] == 6 else 0
    if out["hari_kerja"] == 5:
        out["hari_pendek"] = 0
    lm = [int(x) for x in out["libur_mingguan"].split(",") if x]
    harus = 2 if out["hari_kerja"] == 5 else 1
    if len(lm) != harus:
        per.append("Pola %d hari kerja biasanya punya %d hari istirahat mingguan (PP 35/2021 Pasal 22), tercatat %d "
                   "(%s)." % (out["hari_kerja"], harus, len(lm), label_hari_list(lm)))
    if out["hari_pendek"] and out["hari_pendek"] in lm:
        raise Gagal("Hari kerja terpendek tidak boleh sama dengan hari istirahat mingguan.")
    if d.get("id_mesin") is not None:
        out["id_mesin"] = d["id_mesin"].strip()
        if re.fullmatch(r"\d{16}", out["id_mesin"]):
            raise Gagal("ID mesin 16 digit terlihat seperti NIK. Jangan simpan NIK; pakai nomor ID/PIN di mesin absen.")
    for f in ("gaji_pokok", "tunjangan_tetap", "tunjangan_tidak_tetap", "upah_harian"):
        if d.get(f) is not None:
            v = d[f].strip()
            out[f] = "" if v in ("", "-") else str(angka_wajib(v, f.replace("_", " ")))
    if d.get("tanpa_lembur") is not None and str(d["tanpa_lembur"]).strip():
        out["tanpa_lembur"] = 1 if norm(d["tanpa_lembur"]) in ("ya", "y", "1", "true", "iya") else 0
    if out.get("upah_harian") and out.get("gaji_pokok"):
        per.append("Upah harian dan gaji pokok sama-sama diisi; dasar lembur memakai upah harian x %d."
                   % (25 if out["hari_kerja"] == 6 else 21))
    if "kode" not in out or "nama" not in out:
        raise Gagal("Kode dan nama karyawan wajib diisi.")
    if out["id_mesin"]:
        bentrok = conn.execute("SELECT kode FROM karyawan WHERE id_mesin=? AND kode<>?",
                               (out["id_mesin"], out["kode"])).fetchone()
        if bentrok:
            raise Gagal("ID mesin %s sudah dipakai karyawan %s." % (out["id_mesin"], bentrok[0]))
    return out, per


def _simpan_karyawan(conn, o):
    conn.execute("INSERT OR REPLACE INTO karyawan(kode,nama,jabatan,shift,hari_kerja,libur_mingguan,hari_pendek,"
                 "id_mesin,gaji_pokok,tunjangan_tetap,tunjangan_tidak_tetap,upah_harian,tanpa_lembur,aktif,dibuat) "
                 "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,COALESCE((SELECT dibuat FROM karyawan WHERE kode=?),?))",
                 (o["kode"], o["nama"], o["jabatan"], o["shift"], o["hari_kerja"], o["libur_mingguan"],
                  o["hari_pendek"], o["id_mesin"], o["gaji_pokok"], o["tunjangan_tetap"], o["tunjangan_tidak_tetap"],
                  o["upah_harian"], o["tanpa_lembur"], o.get("aktif", 1), o["kode"], sekarang().isoformat(sep=" ")))


def _label_karyawan(o):
    t = "%s %s%s | %d hari kerja, istirahat mingguan %s" % (
        o["kode"], o["nama"], " (%s)" % o["jabatan"] if o["jabatan"] else "", o["hari_kerja"],
        label_hari_list([int(x) for x in o["libur_mingguan"].split(",") if x]))
    if o["hari_pendek"]:
        t += ", hari terpendek %s" % HARI[o["hari_pendek"] - 1].lower()
    t += " | shift %s" % o["shift"]
    if o["id_mesin"]:
        t += " | ID mesin %s" % o["id_mesin"]
    if o["upah_harian"]:
        t += " | upah harian %s" % rp(Decimal(o["upah_harian"]))
    elif o["gaji_pokok"]:
        t += " | gaji pokok %s" % rp(Decimal(o["gaji_pokok"]))
        if o["tunjangan_tetap"]:
            t += " + tunj. tetap %s" % rp(Decimal(o["tunjangan_tetap"]))
    else:
        t += " | upah belum diisi (lembur hanya dihitung jamnya)"
    if o["tanpa_lembur"]:
        t += " | TANPA upah lembur (golongan jabatan tertentu)"
    return t


def _args_ke_dict(args):
    return {f: getattr(args, f, None) for f in KOLOM_KARYAWAN}


def cmd_karyawan_tambah(args):
    def kerja(conn):
        d = _args_ke_dict(args)
        kode = (d["kode"] or "").strip().upper()
        if conn.execute("SELECT 1 FROM karyawan WHERE kode=?", (kode,)).fetchone():
            raise Gagal("Kode %s sudah terdaftar. Untuk mengubah pakai: karyawan ubah --kode %s ..." % (kode, kode))
        o, per = _siapkan_karyawan(conn, d)
        _simpan_karyawan(conn, o)
        return ({"karyawan": o, "peringatan": per, "ringkasan": {"tambah": o["kode"]}},
                "Tambah karyawan:\n- " + _label_karyawan(o) + "".join("\nCatatan: " + p for p in per))
    return jalankan_tulis(args, "karyawan tambah", kerja)


def cmd_karyawan_ubah(args):
    def kerja(conn):
        k = cari_karyawan(conn, args.kode)
        lama = dict(conn.execute("SELECT * FROM karyawan WHERE kode=?", (k.kode,)).fetchone())
        d = _args_ke_dict(args)
        d["kode"] = None
        o, per = _siapkan_karyawan(conn, d, lama)
        if args.nonaktif:
            o["aktif"] = 0
        if args.aktifkan:
            o["aktif"] = 1
        _simpan_karyawan(conn, o)
        return ({"sebelum": lama, "sesudah": o, "peringatan": per, "ringkasan": {"ubah": o["kode"]}},
                "Sebelum: %s\nSesudah: %s%s%s" % (_label_karyawan(lama), _label_karyawan(o),
                                                 " | NONAKTIF" if not o["aktif"] else "",
                                                 "".join("\nCatatan: " + p for p in per)))
    return jalankan_tulis(args, "karyawan ubah", kerja)


def cmd_karyawan_daftar(args):
    conn = buka(path_db(args))
    try:
        rows = [dict(r) for r in conn.execute("SELECT * FROM karyawan ORDER BY aktif DESC, kode")]
    finally:
        conn.close()
    teks = "Karyawan (%d):\n" % len(rows) + "\n".join(
        "- " + _label_karyawan(r) + ("" if r["aktif"] else " | NONAKTIF") for r in rows)
    for r in rows:
        r.pop("dibuat", None)
    return {"ok": True, "mode": "baca", "karyawan": rows}, teks


SIN_KARYAWAN = {
    "kode": ["kode", "kode karyawan", "no", "no karyawan", "id karyawan"],
    "nama": ["nama", "nama panggilan", "nama karyawan", "name"],
    "jabatan": ["jabatan", "posisi", "bagian"],
    "shift": ["shift", "kode shift"],
    "hari_kerja": ["hari_kerja", "hari kerja", "pola hari kerja", "hari kerja per minggu"],
    "libur_mingguan": ["libur_mingguan", "libur mingguan", "hari libur", "istirahat mingguan"],
    "hari_pendek": ["hari_pendek", "hari pendek", "hari kerja terpendek"],
    "id_mesin": ["id_mesin", "id mesin", "pin", "id fingerprint", "no id", "user id", "ac-no."],
    "gaji_pokok": ["gaji_pokok", "gaji pokok", "upah pokok", "gaji"],
    "tunjangan_tetap": ["tunjangan_tetap", "tunjangan tetap", "tunj tetap"],
    "tunjangan_tidak_tetap": ["tunjangan_tidak_tetap", "tunjangan tidak tetap", "tunj tidak tetap"],
    "upah_harian": ["upah_harian", "upah harian", "gaji harian"],
    "tanpa_lembur": ["tanpa_lembur", "tanpa lembur"],
}


def cmd_karyawan_impor(args):
    def kerja(conn):
        tabel = baca_tabel(args.file)
        hi = cari_header(tabel, SIN_KARYAWAN, minimal=2)
        if hi is None:
            raise Gagal("Judul kolom tidak dikenali. Minimal kolom 'kode' dan 'nama' (contoh: templates/karyawan.csv).")
        kol = deteksi_kolom(tabel[hi], SIN_KARYAWAN)
        if "kode" not in kol or "nama" not in kol:
            raise Gagal("File wajib punya kolom 'kode' dan 'nama'.")
        hasil, galat, per = [], [], []
        for i, r in enumerate(tabel[hi + 1:], start=hi + 2):
            if not any(c.strip() for c in r):
                continue
            d = {f: sel(r, kol[f]) for f in kol}
            try:
                lama = conn.execute("SELECT * FROM karyawan WHERE kode=?", (d["kode"].strip().upper(),)).fetchone()
                o, p = _siapkan_karyawan(conn, d, dict(lama) if lama else None)
                _simpan_karyawan(conn, o)
                hasil.append(("ubah" if lama else "baru", o))
                per.extend("%s: %s" % (o["kode"], x) for x in p)
            except Gagal as e:
                galat.append("Baris %d: %s" % (i, e.pesan))
        if galat:
            raise Gagal("Ada %d baris bermasalah; tidak ada yang disimpan. Perbaiki dulu." % len(galat), baris_rusak=galat)
        teks = "Impor karyawan: %d baru, %d diubah\nPemetaan kolom: %s\n" % (
            sum(1 for s, _ in hasil if s == "baru"), sum(1 for s, _ in hasil if s == "ubah"),
            ", ".join("%s <- '%s'" % (f, tabel[hi][i]) for f, i in kol.items()))
        teks += "\n".join("- [%s] %s" % (s, _label_karyawan(o)) for s, o in hasil)
        teks += "".join("\nCatatan: " + p for p in per)
        return {"karyawan": [o for _, o in hasil], "peringatan": per,
                "pemetaan": {f: tabel[hi][i] for f, i in kol.items()},
                "ringkasan": {"impor_karyawan": len(hasil)}}, teks
    return jalankan_tulis(args, "karyawan impor", kerja, label_backup="impor-karyawan")


# ---------------------------------------------------------------------------
# Catat manual, keterangan, lembur, hapus
# ---------------------------------------------------------------------------


def _jam_arg(teks, nama, kini):
    if norm(teks) in ("sekarang", "now", "skrg"):
        return kini.time().replace(second=0)
    return jam_wajib(teks, nama)


def cmd_catat(args):
    def kerja(conn):
        if not args.masuk and not args.pulang:
            raise Gagal("Isi --masuk dan/atau --pulang (mis. --masuk 08.12).")
        kini = sekarang(args)
        k = cari_karyawan(conn, args.karyawan)
        tgl_eksplisit = bool(args.tanggal)
        d = tanggal_wajib(args.tanggal) if args.tanggal else kini.date()
        jm = _jam_arg(args.masuk, "masuk", kini) if args.masuk else None
        jp = _jam_arg(args.pulang, "pulang", kini) if args.pulang else None
        catatan = []
        # pulang dini hari untuk shift malam kemarin (tanpa --tanggal)
        if jp and not jm and not tgl_eksplisit and k.shift.lintas_malam and jp < k.shift.masuk:
            d = d - timedelta(days=1)
            catatan.append("Dicatat sebagai pulang shift malam yang mulai %s %s." % (HARI[d.weekday()], ftgl(d)))
        elif jp and not jm and not tgl_eksplisit and not k.shift.lintas_malam and jp < k.shift.masuk:
            kemarin = d - timedelta(days=1)
            buka_kemarin = conn.execute("SELECT 1 FROM tap WHERE kode=? AND tanggal_kerja=? AND jenis='masuk'",
                                        (k.kode, kemarin.isoformat())).fetchone()
            if buka_kemarin:
                raise Gagal("Jam pulang %s lebih pagi dari jadwal masuk. Jika ini pulang lembur dari shift kemarin "
                            "(lewat tengah malam), ulangi dengan --tanggal %s --lewat-tengah-malam."
                            % (fjm(jp), kemarin.isoformat()))
        masuk_dt = datetime.combine(d, jm) if jm else None
        pulang_dt = None
        if jp:
            pulang_dt = datetime.combine(d, jp)
            acuan = masuk_dt
            if acuan is None:
                r = conn.execute("SELECT MIN(waktu) FROM tap WHERE kode=? AND tanggal_kerja=? AND jenis='masuk'",
                                 (k.kode, d.isoformat())).fetchone()[0]
                acuan = _dt(r) if r else None
            if args.lewat_tengah_malam:
                pulang_dt += timedelta(days=1)
            elif k.shift.lintas_malam and jp < k.shift.masuk:
                pulang_dt += timedelta(days=1)
            elif acuan and pulang_dt <= acuan:
                raise Gagal("Jam pulang %s lebih awal dari jam masuk %s pada %s. Jika pulangnya lewat tengah malam, "
                            "tambahkan --lewat-tengah-malam; jika salah ketik, perbaiki jamnya."
                            % (fjm(jp), fjm(acuan), ftgl(d)))
        if masuk_dt and masuk_dt > kini + timedelta(minutes=5):
            raise Gagal("Jam masuk %s %s belum terjadi (sekarang %s). Periksa tanggal/jamnya."
                        % (ftgl(d), fjm(masuk_dt), kini.strftime("%d/%m/%Y %H.%M")))
        if pulang_dt and pulang_dt > kini + timedelta(minutes=5):
            raise Gagal("Jam pulang %s belum terjadi (sekarang %s). Periksa tanggal/jamnya."
                        % (pulang_dt.strftime("%d/%m/%Y %H.%M"), kini.strftime("%d/%m/%Y %H.%M")))
        ringkas = []
        for jenis, w in (("masuk", masuk_dt), ("pulang", pulang_dt)):
            if w is None:
                continue
            ada = conn.execute("SELECT waktu, sumber FROM tap WHERE kode=? AND tanggal_kerja=? AND jenis=?",
                               (k.kode, d.isoformat(), jenis)).fetchall()
            ada_mesin = conn.execute("SELECT COUNT(*) FROM tap WHERE kode=? AND tanggal_kerja IS NULL AND waktu "
                                     "BETWEEN ? AND ?", (k.kode, d.isoformat(),
                                                         (d + timedelta(days=2)).isoformat())).fetchone()[0]
            if ada and not args.ganti:
                raise Gagal("%s sudah punya catatan %s %s pada %s. Untuk mengganti, ulangi dengan --ganti."
                            % (k.nama, jenis, ", ".join(fjm(_dt(a["waktu"])) for a in ada), ftgl(d)))
            if ada:
                conn.execute("DELETE FROM tap WHERE kode=? AND tanggal_kerja=? AND jenis=?",
                             (k.kode, d.isoformat(), jenis))
                catatan.append("Menggantikan %s lama %s." % (jenis, ", ".join(fjm(_dt(a["waktu"])) for a in ada)))
            if ada_mesin:
                catatan.append("Sudah ada %d tap dari mesin di sekitar tanggal ini; catatan manual ikut dipakai "
                               "(masuk paling awal / pulang paling akhir)." % ada_mesin)
            conn.execute("INSERT OR IGNORE INTO tap(kode, waktu, jenis, tanggal_kerja, sumber) VALUES (?,?,?,?,?)",
                         (k.kode, w.isoformat(sep=" "), jenis, d.isoformat(), "manual"))
            ringkas.append("%s %s" % (jenis, w.strftime("%H.%M") + ("" if w.date() == d else " (" + ftgl(w) + ")")))
        cfg = pengaturan(conn)
        mulai, selesai, _ = k.shift.jendela(d, k.pendek(d))
        if masuk_dt and jenis_hari(k, d, libur_set(conn, d, d)) == "kerja":
            tl = int((masuk_dt - mulai).total_seconds() // 60)
            if tl > cfg["toleransi_telat"]:
                catatan.append("Terlambat %d menit (jadwal %s, toleransi %d menit)." % (tl, fjm(mulai),
                                                                                    cfg["toleransi_telat"]))
        teks = "%s (%s) - %s %s: %s" % (k.nama, k.kode, HARI[d.weekday()], ftgl(d), ", ".join(ringkas))
        teks += "".join("\nCatatan: " + c for c in catatan)
        return {"karyawan": k.kode, "nama": k.nama, "tanggal_kerja": d.isoformat(), "dicatat": ringkas,
                "catatan": catatan, "ringkasan": {"catat": k.kode, "tanggal": d.isoformat(), "isi": ringkas}}, teks
    return jalankan_tulis(args, "catat", kerja)


def _rentang(args):
    d1 = tanggal_wajib(args.tanggal)
    d2 = tanggal_wajib(args.sampai, "sampai") if getattr(args, "sampai", None) else d1
    if d2 < d1:
        raise Gagal("Tanggal --sampai lebih awal dari --tanggal.")
    if (d2 - d1).days > 366:
        raise Gagal("Rentang terlalu panjang (maks 1 tahun).")
    return d1, d2


def cmd_keterangan(args):
    def kerja(conn):
        k = cari_karyawan(conn, args.karyawan)
        d1, d2 = _rentang(args)
        libur = libur_set(conn, d1, d2)
        dicatat, dilewati, catatan = [], [], []
        d = d1
        while d <= d2:
            if jenis_hari(k, d, libur) != "kerja" and d1 != d2:
                dilewati.append(d)
            else:
                lama = conn.execute("SELECT jenis FROM keterangan WHERE kode=? AND tanggal=?",
                                    (k.kode, d.isoformat())).fetchone()
                if lama and lama[0] != args.jenis:
                    catatan.append("%s sebelumnya tercatat %s, diganti %s." % (ftgl(d), lama[0], args.jenis))
                conn.execute("INSERT OR REPLACE INTO keterangan VALUES (?,?,?,?)",
                             (k.kode, d.isoformat(), args.jenis, args.catatan or ""))
                dicatat.append(d)
            d += timedelta(days=1)
        teks = "%s (%s): %s pada %d hari kerja (%s)" % (
            k.nama, k.kode, args.jenis.upper(), len(dicatat), ", ".join(ftgl(x) for x in dicatat))
        if dilewati:
            teks += "\nDilewati (hari istirahat/libur): " + ", ".join(ftgl(x) for x in dilewati)
        if args.catatan:
            teks += "\nCatatan: " + args.catatan
        teks += "".join("\n" + c for c in catatan)
        return {"karyawan": k.kode, "jenis": args.jenis, "tanggal": [x.isoformat() for x in dicatat],
                "ringkasan": {"keterangan": args.jenis, "kode": k.kode, "hari": len(dicatat)}}, teks
    return jalankan_tulis(args, "keterangan", kerja)


def cmd_lembur(args):
    def kerja(conn):
        k = cari_karyawan(conn, args.karyawan)
        d = tanggal_wajib(args.tanggal)
        jam = parse_durasi_jam(args.jam)
        if jam is None or jam <= 0:
            raise Gagal("Jam lembur '%s' tidak valid. Contoh: 2, 1,5, 1:30, '1 jam 30 menit'." % args.jam)
        if jam > 12:
            raise Gagal("Jam lembur %s dalam sehari tidak wajar (> 12 jam). Periksa lagi." % fjam(jam))
        jam = jam.quantize(Decimal("0.01"))
        catatan = []
        lama = conn.execute("SELECT jam FROM lembur WHERE kode=? AND tanggal=?", (k.kode, d.isoformat())).fetchone()
        if lama and not args.ganti:
            raise Gagal("Lembur %s tanggal %s sudah tercatat %s jam. Untuk mengganti, ulangi dengan --ganti."
                        % (k.nama, ftgl(d), fjam(Decimal(lama[0]))))
        conn.execute("INSERT OR REPLACE INTO lembur VALUES (?,?,?,?,?)",
                     (k.kode, d.isoformat(), str(jam), args.catatan or "", sekarang().isoformat(sep=" ")))
        libur = libur_set(conn, d, d)
        jh = jenis_hari(k, d, libur)
        if jh == "kerja":
            setara = jam_setara_hari_kerja(jam)
            pola = "hari kerja (Pasal 31 ayat (1): jam pertama 1,5x, berikutnya 2x)"
            if jam > MAKS_LEMBUR_HARI_KERJA:
                catatan.append("Melebihi batas 4 jam/hari di hari kerja (Pasal 26 ayat (1)).")
        else:
            p = str(k.hari_kerja)
            if k.hari_kerja == 6 and jh == "libur-resmi" and k.hari_pendek and d.isoweekday() == k.hari_pendek:
                p = "6p"
            setara, err = jam_setara_libur(jam, p)
            pola = {"5": "hari istirahat/libur, pola 5 hari kerja (Pasal 31 ayat (3))",
                    "6": "hari istirahat/libur, pola 6 hari kerja (Pasal 31 ayat (2) huruf a)",
                    "6p": "libur resmi di hari kerja terpendek, pola 6 hari (Pasal 31 ayat (2) huruf b)"}[p]
            if err:
                raise Gagal("Lembur %s jam %s. Periksa jumlah jamnya." % (fjam(jam), err))
        if k.tanpa_lembur:
            catatan.append("Karyawan ini ditandai golongan jabatan tertentu: lembur dicatat tetapi tidak dibayar "
                           "(Pasal 27).")
        if not args.catatan:
            catatan.append("Sebaiknya isi --catatan siapa yang memerintahkan/menyetujui (Pasal 28: perintah dan "
                           "persetujuan tertulis/digital).")
        dasar, _ = k.dasar_lembur()
        nominal = bulat_rp(setara * dasar / PEMBAGI_UPAH_SEJAM) if dasar is not None and not k.tanpa_lembur else None
        teks = "Lembur DISETUJUI - %s (%s), %s %s: %s jam\nJenis: %s\nJam setara: %s x upah sejam%s" % (
            k.nama, k.kode, HARI[d.weekday()], ftgl(d), fjam(jam), pola, fjam(setara),
            " = %s (upah sejam %s)" % (rp(nominal), rp(dasar / PEMBAGI_UPAH_SEJAM)) if nominal is not None else "")
        teks += "".join("\nCatatan: " + c for c in catatan)
        return {"karyawan": k.kode, "tanggal": d.isoformat(), "jam": str(jam), "jenis_hari": jh,
                "jam_setara": str(setara), "perkiraan_upah": nominal, "catatan": catatan,
                "ringkasan": {"lembur": k.kode, "tanggal": d.isoformat(), "jam": str(jam)}}, teks
    return jalankan_tulis(args, "lembur", kerja)


def cmd_hapus(args):
    def kerja(conn):
        k = cari_karyawan(conn, args.karyawan)
        d = tanggal_wajib(args.tanggal)
        n = {"tap": 0, "keterangan": 0, "lembur": 0}
        if args.jenis in ("tap", "semua"):
            n["tap"] += conn.execute("DELETE FROM tap WHERE kode=? AND tanggal_kerja=?", (k.kode, d.isoformat())).rowcount
            # tap mesin tanpa tanggal kerja: hapus yang jatuh di jendela shift tanggal itu
            mulai, selesai, _ = k.shift.jendela(d, k.pendek(d))
            n["tap"] += conn.execute(
                "DELETE FROM tap WHERE kode=? AND tanggal_kerja IS NULL AND waktu BETWEEN ? AND ?",
                (k.kode, (mulai - timedelta(hours=4)).isoformat(sep=" "),
                 (selesai + timedelta(hours=8)).isoformat(sep=" "))).rowcount
        if args.jenis in ("keterangan", "semua"):
            n["keterangan"] = conn.execute("DELETE FROM keterangan WHERE kode=? AND tanggal=?",
                                           (k.kode, d.isoformat())).rowcount
        if args.jenis in ("lembur", "semua"):
            n["lembur"] = conn.execute("DELETE FROM lembur WHERE kode=? AND tanggal=?", (k.kode, d.isoformat())).rowcount
        if not sum(n.values()):
            raise Gagal("Tidak ada data %s untuk %s pada %s." % (args.jenis, k.nama, ftgl(d)))
        teks = "Hapus data %s (%s) %s: %d tap, %d keterangan, %d lembur" % (
            k.nama, k.kode, ftgl(d), n["tap"], n["keterangan"], n["lembur"])
        return {"dihapus": n, "ringkasan": {"hapus": k.kode, "tanggal": d.isoformat(), "jumlah": n}}, teks
    return jalankan_tulis(args, "hapus", kerja, label_backup="hapus")


# ---------------------------------------------------------------------------
# Impor log mesin absen
# ---------------------------------------------------------------------------

SIN_ABSEN = {
    "id": ["id", "no. id", "no id", "no.id", "user id", "userid", "user_id", "pin", "ac-no.", "ac-no", "ac no",
           "enroll id", "enrollid", "emp no.", "emp no", "employee id", "person id", "badge", "id karyawan",
           "no. karyawan", "no karyawan", "kode", "kode karyawan", "id mesin", "no. pegawai"],
    "nama": ["nama", "name", "nama karyawan", "employee name", "nama pegawai", "first name"],
    "waktu": ["waktu", "tanggal & waktu", "tanggal/waktu", "tanggal waktu", "datetime", "date time", "date/time",
              "date & time", "check time", "checktime", "timestamp", "time stamp", "waktu scan", "scan time",
              "log time", "punch time", "tgl/jam", "tanggal jam"],
    "tanggal": ["tanggal", "tgl", "date", "tanggal scan", "hari/tanggal", "tanggal absen"],
    "masuk": ["scan masuk", "masuk", "jam datang", "datang", "clock in", "check in", "checkin", "absen masuk",
              "jam masuk", "in"],
    "pulang": ["scan pulang", "scan keluar", "pulang", "clock out", "check out", "checkout", "absen pulang",
               "jam pulang", "jam keluar", "keluar", "out"],
    "jam": ["jam", "time", "pukul", "jam scan", "waktu absen"],
    "status": ["status", "state", "check type", "checktype", "punch state", "in/out", "tipe", "jenis", "mode absen",
               "type"],
}
STATUS_MASUK = {"c/in", "in", "check in", "checkin", "check-in", "masuk", "datang", "0", "i", "clock in", "duty on",
                "on duty", "absen masuk", "scan masuk"}
STATUS_PULANG = {"c/out", "out", "check out", "checkout", "check-out", "pulang", "keluar", "1", "o", "clock out",
                 "duty off", "off duty", "absen pulang", "scan pulang"}
STATUS_ISTIRAHAT = {"2", "3", "break out", "break in", "istirahat", "kembali", "out back", "istirahat keluar",
                    "istirahat masuk"}
STATUS_LEMBUR = {"4", "5", "ot in", "ot out", "overtime in", "overtime out", "lembur masuk", "lembur keluar",
                 "lembur pulang"}


def _urutan_tanggal(nilai):
    """Tentukan 'dmy' / 'mdy' dari kumpulan teks tanggal angka. Kembalikan (urutan, pasti?)."""
    a_besar = b_besar = False
    for v in nilai:
        tg, _ = pisah_tanggal_jam(v)
        m = RE_TGL_ANGKA.match(tg)
        if not m or len(m.group(1)) == 4:
            continue
        if int(m.group(1)) > 12:
            a_besar = True
        if int(m.group(2)) > 12:
            b_besar = True
    if a_besar and b_besar:
        raise Gagal("Format tanggal di file tidak konsisten (ada yang hari/bulan dan ada yang bulan/hari). "
                    "Periksa file atau ekspor ulang dari mesin.")
    if b_besar:
        return "mdy", True
    return "dmy", a_besar


def cmd_impor_absen(args):
    def kerja(conn):
        tabel = baca_tabel(args.file)
        kini = sekarang(args)
        paksa = {f: getattr(args, "kolom_" + f, None) for f in SIN_ABSEN}
        hi = cari_header(tabel, SIN_ABSEN, minimal=2)
        if hi is None:
            raise Gagal("Judul kolom file absen tidak dikenali. Minimal perlu kolom ID/Nama dan Tanggal/Waktu. "
                        "Sebutkan kolomnya dengan --kolom-id, --kolom-waktu, dst.",
                        baris_awal=[r for r in tabel[:3]])
        header = tabel[hi]
        kol = deteksi_kolom(header, SIN_ABSEN)
        hn = [norm(h) for h in header]
        for f, nama in paksa.items():
            if nama is None:
                continue
            if nama.strip() == "-":
                kol.pop(f, None)
                continue
            if norm(nama) not in hn:
                raise Gagal("Kolom '%s' tidak ada di file. Kolom tersedia: %s" % (nama, ", ".join(header)))
            kol[f] = hn.index(norm(nama))
        if "id" not in kol and "nama" not in kol:
            raise Gagal("Tidak ada kolom ID atau Nama karyawan. Sebutkan dengan --kolom-id atau --kolom-nama.")
        mode_harian = "masuk" in kol or "pulang" in kol
        if mode_harian:
            if "tanggal" not in kol:
                raise Gagal("File berformat per hari (kolom masuk/pulang) tetapi kolom Tanggal tidak ditemukan.")
            kol.pop("jam", None)
            kol.pop("status", None)
        elif "waktu" not in kol and "tanggal" not in kol:
            raise Gagal("Kolom tanggal/waktu tidak ditemukan. Sebutkan dengan --kolom-waktu atau --kolom-tanggal.")
        data = [r for r in tabel[hi + 1:] if any((c or "").strip() for c in r)]
        kol_tgl = kol.get("waktu", kol.get("tanggal"))
        if args.format_tanggal:
            urutan, pasti = args.format_tanggal, True
        else:
            urutan, pasti = _urutan_tanggal([sel(r, kol_tgl) for r in data])
        karyawan = muat_karyawan(conn)
        per_id = {k.id_mesin: k for k in karyawan if k.id_mesin}
        per_kode = {k.kode.lower(): k for k in karyawan}
        per_nama = defaultdict(list)
        for k in karyawan:
            per_nama[k.nama.lower()].append(k)
        dari = tanggal_wajib(args.dari, "dari") if args.dari else None
        sampai = tanggal_wajib(args.sampai, "sampai") if args.sampai else None
        tak_dikenal, rusak, status_asing = defaultdict(int), [], defaultdict(int)
        calon, diabaikan = [], defaultdict(int)
        shift_k = {}

        def karyawan_baris(r):
            idv, nm = sel(r, kol.get("id")), sel(r, kol.get("nama"))
            idv2 = re.sub(r"\.0+$", "", idv)
            k = None
            if idv2:
                k = per_id.get(idv2) or per_id.get(idv2.lstrip("0") or "0") or per_kode.get(idv2.lower())
            if k is None and nm:
                c = per_nama.get(nm.lower(), [])
                if len(c) == 1:
                    k = c[0]
                elif len(c) > 1:
                    return None, "nama '%s' dipakai %d karyawan; isi ID mesin" % (nm, len(c))
            if k is None:
                return None, "ID %s / nama %s" % (idv or "-", nm or "-")
            return k, None

        for i, r in enumerate(data, start=hi + 2):
            k, alasan = karyawan_baris(r)
            if k is None:
                tak_dikenal[alasan] += 1
                continue
            if mode_harian:
                d = parse_tanggal(pisah_tanggal_jam(sel(r, kol["tanggal"]))[0], urutan)
                if d is None:
                    rusak.append("baris %d: tanggal '%s' tidak valid" % (i, sel(r, kol["tanggal"])))
                    continue
                jm_teks, jp_teks = sel(r, kol.get("masuk")), sel(r, kol.get("pulang"))
                jm = parse_jam(jm_teks) if jm_teks else None
                jp = parse_jam(jp_teks) if jp_teks else None
                if jm_teks and jm is None:
                    rusak.append("baris %d (%s %s): jam masuk '%s' tidak valid" % (i, k.nama, ftgl(d), jm_teks))
                if jp_teks and jp is None:
                    rusak.append("baris %d (%s %s): jam pulang '%s' tidak valid" % (i, k.nama, ftgl(d), jp_teks))
                if jm is None and jp is None:
                    if not jm_teks and not jp_teks:
                        diabaikan["baris tanpa jam scan"] += 1
                    continue
                mdt = datetime.combine(d, jm) if jm else None
                pdt = datetime.combine(d, jp) if jp else None
                if pdt and mdt and pdt <= mdt:
                    if k.shift.lintas_malam:
                        pdt += timedelta(days=1)
                    else:
                        rusak.append("baris %d (%s %s): pulang %s sebelum masuk %s - jam pulang tidak diimpor"
                                     % (i, k.nama, ftgl(d), fjm(jp), fjm(jm)))
                        pdt = None
                elif pdt and not mdt and k.shift.lintas_malam and jp < k.shift.masuk:
                    pdt += timedelta(days=1)
                for jenis, w in (("masuk", mdt), ("pulang", pdt)):
                    if w:
                        calon.append((k, w, jenis, d))
            else:
                if "waktu" in kol:
                    tg, jm_teks = pisah_tanggal_jam(sel(r, kol["waktu"]))
                    if not jm_teks and "jam" in kol:
                        jm_teks = sel(r, kol["jam"])
                    if re.fullmatch(r"\d{5}\.\d+", sel(r, kol["waktu"])):      # seri Excel tanggal+jam
                        n = float(sel(r, kol["waktu"]))
                        tg, jm_teks = str(int(n)), str(n - int(n))[1:] if n != int(n) else "0.0"
                else:
                    tg, jm_teks = pisah_tanggal_jam(sel(r, kol["tanggal"]))
                    if "jam" in kol:
                        jm_teks = sel(r, kol["jam"]) or jm_teks
                d = parse_tanggal(tg, urutan)
                j = parse_jam(jm_teks) if jm_teks else None
                if d is None:
                    rusak.append("baris %d (%s): tanggal '%s' tidak valid" % (i, k.nama, tg))
                    continue
                if j is None:
                    rusak.append("baris %d (%s %s): jam '%s' tidak valid" % (i, k.nama, ftgl(d), jm_teks or "(kosong)"))
                    continue
                jenis = ""
                if "status" in kol:
                    st = norm(sel(r, kol["status"]))
                    if st in STATUS_MASUK:
                        jenis = "masuk"
                    elif st in STATUS_PULANG:
                        jenis = "pulang"
                    elif st in STATUS_ISTIRAHAT:
                        diabaikan["tap istirahat (keluar/kembali istirahat)"] += 1
                        continue
                    elif st in STATUS_LEMBUR or st == "":
                        jenis = ""
                    else:
                        status_asing[st] += 1
                calon.append((k, datetime.combine(d, j), jenis, None))
        # filter rentang & masa depan
        baru, sudah, masa_depan, luar = 0, 0, [], 0
        impor_id = conn.execute("INSERT INTO impor(waktu, file, baris, tap_baru, pemetaan) VALUES (?,?,?,?,?)",
                                (kini.isoformat(sep=" "), Path(args.file).name, len(data), 0,
                                 json.dumps({f: header[i] for f, i in kol.items()}, ensure_ascii=False))).lastrowid
        per_karyawan = defaultdict(int)
        rentang = [None, None]
        for k, w, jenis, d in calon:
            acuan = d or w.date()
            if (dari and acuan < dari) or (sampai and acuan > sampai):
                luar += 1
                continue
            if w > kini + timedelta(minutes=5):
                masa_depan.append("%s %s" % (k.nama, w.strftime("%d/%m/%Y %H.%M")))
                continue
            cur = conn.execute("INSERT OR IGNORE INTO tap(kode, waktu, jenis, tanggal_kerja, sumber, impor_id) "
                               "VALUES (?,?,?,?,?,?)", (k.kode, w.isoformat(sep=" "), jenis,
                                                        d.isoformat() if d else None, "impor", impor_id))
            if cur.rowcount:
                baru += 1
                per_karyawan[k.nama] += 1
                rentang[0] = min(rentang[0] or acuan, acuan)
                rentang[1] = max(rentang[1] or acuan, acuan)
            else:
                sudah += 1
        conn.execute("UPDATE impor SET tap_baru=? WHERE id=?", (baru, impor_id))
        peringatan = []
        if not pasti and not mode_harian and not args.format_tanggal:
            peringatan.append("Urutan tanggal tidak bisa dipastikan dari isi file; dibaca sebagai HARI/BULAN/TAHUN "
                              "(format Indonesia). Jika mesin memakai bulan/hari, ulangi dengan --format-tanggal mdy.")
        elif not pasti and mode_harian and not args.format_tanggal:
            peringatan.append("Tanggal dibaca sebagai HARI/BULAN/TAHUN. Jika salah, ulangi dengan --format-tanggal mdy.")
        if urutan == "mdy" and not args.format_tanggal:
            peringatan.append("Tanggal di file terdeteksi berformat BULAN/HARI/TAHUN (gaya Amerika) dan dibaca begitu.")
        if tak_dikenal:
            peringatan.append("Ada %d baris dari karyawan yang tidak dikenal (tidak diimpor). Daftarkan dulu dengan "
                              "karyawan tambah --id-mesin ..., lalu impor ulang file yang sama (data lama tidak "
                              "akan dobel)." % sum(tak_dikenal.values()))
        if status_asing:
            peringatan.append("Status tidak dikenal (dianggap tap biasa, masuk/pulang ditentukan dari jadwal): "
                              + ", ".join("'%s' (%d)" % x for x in status_asing.items()))
        if masa_depan:
            peringatan.append("%d tap bertanggal di masa depan tidak diimpor (cek jam mesin): %s"
                              % (len(masa_depan), "; ".join(masa_depan[:5])))
        if rusak:
            peringatan.append("%d baris rusak tidak diimpor (lihat daftar)." % len(rusak))
        contoh_baca = []
        for k, w, jenis, d in calon[:3]:
            contoh_baca.append("%s: %s %s%s" % (k.nama, HARI[w.weekday()], w.strftime("%d %B %Y %H.%M"),
                                                " (%s)" % jenis if jenis else ""))
        teks = ["Impor absen dari %s (%s)" % (Path(args.file).name, "format per hari: masuk/pulang"
                                              if mode_harian else "format log tap"),
                "Pemetaan kolom: " + ", ".join("%s <- '%s'" % (f, header[i]) for f, i in kol.items()),
                "Contoh cara baca: " + " | ".join(contoh_baca) if contoh_baca else "Tidak ada baris yang terbaca.",
                "Tap baru: %d | sudah ada sebelumnya (dilewati): %d | di luar rentang: %d" % (baru, sudah, luar)]
        if rentang[0]:
            teks.append("Rentang tanggal: %s s.d. %s" % (ftgl(rentang[0]), ftgl(rentang[1])))
        if per_karyawan:
            teks.append("Per karyawan: " + ", ".join("%s %d" % x for x in sorted(per_karyawan.items())))
        for kk, v in diabaikan.items():
            teks.append("Diabaikan: %s %d" % (kk, v))
        if tak_dikenal:
            teks.append("Tidak dikenal: " + "; ".join("%s (%d baris)" % x for x in list(tak_dikenal.items())[:15]))
        if rusak:
            teks.append("Baris rusak:\n" + "\n".join("- " + x for x in rusak[:20]) +
                        ("\n- ... dan %d lainnya" % (len(rusak) - 20) if len(rusak) > 20 else ""))
        teks += ["Peringatan: " + p for p in peringatan]
        return {"format": "harian" if mode_harian else "log", "urutan_tanggal": urutan,
                "pemetaan": {f: header[i] for f, i in kol.items()}, "tap_baru": baru, "sudah_ada": sudah,
                "di_luar_rentang": luar, "per_karyawan": dict(per_karyawan),
                "tak_dikenal": dict(tak_dikenal), "baris_rusak": rusak, "diabaikan": dict(diabaikan),
                "peringatan": peringatan, "contoh_baca": contoh_baca,
                "ringkasan": {"impor": Path(args.file).name, "tap_baru": baru}}, "\n".join(teks)
    return jalankan_tulis(args, "impor-absen", kerja, label_backup="impor-absen")


# ---------------------------------------------------------------------------
# Laporan: rekap bulanan & harian
# ---------------------------------------------------------------------------


def _periode(args, kini):
    if args.bulan:
        m = re.fullmatch(r"(\d{4})-(\d{1,2})", args.bulan.strip()) or re.fullmatch(r"(\d{1,2})[-/](\d{4})",
                                                                                  args.bulan.strip())
        if not m:
            raise Gagal("--bulan harus berformat 2026-09.")
        th, bl = (int(m.group(1)), int(m.group(2))) if len(m.group(1)) == 4 else (int(m.group(2)), int(m.group(1)))
        if not 1 <= bl <= 12:
            raise Gagal("Bulan %d tidak valid." % bl)
        dari = date(th, bl, 1)
        sampai = (date(th + (bl == 12), bl % 12 + 1, 1)) - timedelta(days=1)
        label = "%s %d" % (BULAN_NAMA[bl - 1], th)
    elif args.dari:
        dari = tanggal_wajib(args.dari, "dari")
        sampai = tanggal_wajib(args.sampai, "sampai") if args.sampai else kini.date()
        label = "%s s.d. %s" % (ftgl(dari), ftgl(sampai))
    else:
        dari = kini.date().replace(day=1)
        sampai = kini.date()
        label = "%s %d (s.d. %s)" % (BULAN_NAMA[dari.month - 1], dari.year, ftgl(sampai))
    if sampai < dari:
        raise Gagal("Tanggal akhir lebih awal dari tanggal awal.")
    if (sampai - dari).days > 62:
        raise Gagal("Rekap maksimal 62 hari sekali jalan. Jalankan per bulan.")
    return dari, sampai, label


def _jam_list_str(lst, libur=False):
    if libur:
        return "+".join(fjam(j) + ("p" if p else "") for j, p in lst)
    return "+".join(fjam(j) for j in lst)


def cmd_rekap(args):
    db = path_db(args)
    conn = buka(db)
    kini = sekarang(args)
    try:
        dari, sampai, label = _periode(args, kini)
        cfg, libur, hasil, masalah, harian = analisa_semua(conn, dari, sampai, kini, args.karyawan, args.pola)
    finally:
        conn.close()
    if not hasil:
        raise Gagal("Belum ada karyawan/data untuk periode ini.")
    judul = "REKAP ABSENSI %s" % label.upper()
    if cfg["nama_usaha"]:
        judul += " - " + cfg["nama_usaha"]
    baris = [judul, "Periode %s-%s | toleransi terlambat %d menit" % (ftgl(dari), ftgl(min(sampai, kini.date())),
                                                                     cfg["toleransi_telat"])]
    if libur:
        baris.append("Libur resmi: " + ", ".join("%s %s" % (ftgl(date.fromisoformat(t)), n) for t, n in sorted(libur.items())))
    total_lembur = 0
    for no, r in enumerate(hasil, start=1):
        baris.append("")
        baris.append("%d. %s (%s)%s" % (no, r["nama"], r["kode"], " - " + r["jabatan"] if r["jabatan"] else ""))
        s = "   Hadir %d dari %d hari kerja" % (r["hadir"], r["hari_terjadwal"])
        ket = ["%s %d" % (j.capitalize(), r[j]) for j in JENIS_KET if r[j]]
        if r["tanpa_keterangan"]:
            ket.append("Tanpa keterangan %d" % r["tanpa_keterangan"])
        if ket:
            s += " | " + ", ".join(ket)
        if r["hadir_di_hari_libur"]:
            s += " | masuk di hari libur %d" % r["hadir_di_hari_libur"]
        baris.append(s)
        baris.append("   Terlambat %dx (%s) | Pulang cepat %dx (%s)" % (
            r["terlambat_kali"], fmenit(r["terlambat_menit"]), r["pulang_cepat_kali"], fmenit(r["pulang_cepat_menit"])))
        s = "   Jam kerja %s" % fmenit(r["menit_kerja"])
        if r["hari_tidak_lengkap"]:
            s += " (+%d hari data tidak lengkap, belum dihitung)" % r["hari_tidak_lengkap"]
        baris.append(s)
        if r["lembur_rincian"]:
            s = "   Lembur disetujui: hari kerja %s jam, hari libur %s jam (setara %s jam)" % (
                fjam(r["lembur_jam_hari_kerja"]), fjam(r["lembur_jam_hari_libur"]), fjam(r["lembur_jam_setara"]))
            if r["tanpa_lembur"]:
                s += " -> tidak dibayar (golongan jabatan tertentu)"
            elif r["upah_lembur"] is not None:
                s += " -> %s" % rp(r["upah_lembur"])
                total_lembur += r["upah_lembur"]
            else:
                s += " -> rupiah belum dihitung (upah belum diisi)"
            baris.append(s)
    if total_lembur:
        baris += ["", "Total upah lembur: %s" % rp(total_lembur)]
    serius = [m for m in masalah if m["tingkat"] in ("salah", "cek")]
    if serius:
        baris += ["", "PERLU DICEK (%d):" % len(serius)]
        for m in serius[:40]:
            baris.append("- %s%s: %s" % (m["nama"], " " + ftgl(date.fromisoformat(m["tanggal"])) if m["tanggal"] else "",
                                         m["pesan"]))
        if len(serius) > 40:
            baris.append("- ... dan %d lainnya (lihat CSV/JSON)" % (len(serius) - 40))
    tk = [(r["nama"], r["tanggal_tanpa_keterangan"]) for r in hasil if r["tanggal_tanpa_keterangan"]]
    if tk:
        baris += ["", "Hari kerja tanpa absen & tanpa keterangan (mohon dikonfirmasi: izin/sakit/cuti/alpa?):"]
        for n, t in tk:
            baris.append("- %s: %s" % (n, ", ".join(ftgl(date.fromisoformat(x))[:5] for x in t)))
    if any(r["lembur_rincian"] for r in hasil):
        baris += ["", DISCLAIMER]
    data = {"ok": True, "mode": "baca", "periode": {"dari": dari.isoformat(), "sampai": sampai.isoformat(),
                                                    "label": label},
            "pengaturan": cfg, "libur_resmi": libur, "karyawan": [], "masalah": masalah,
            "total_upah_lembur": total_lembur, "disclaimer": DISCLAIMER}
    for r in hasil:
        rr = {kk: (str(v) if isinstance(v, Decimal) else v) for kk, v in r.items() if not kk.startswith("_")}
        data["karyawan"].append(rr)
    file = {}
    if args.csv:
        hdr = ["kode", "nama", "jabatan", "hari_kerja_per_minggu", "hari_terjadwal", "hadir", "hadir_di_hari_libur",
               "izin", "sakit", "cuti", "alpa", "dinas", "tanpa_keterangan", "terlambat_kali", "terlambat_menit",
               "pulang_cepat_kali", "pulang_cepat_menit", "jam_kerja", "hari_tidak_lengkap", "lembur_jam_hari_kerja",
               "lembur_jam_hari_libur", "lembur_jam_setara", "dasar_upah_lembur", "upah_lembur"]
        rows = []
        for r in hasil:
            rows.append([r["kode"], r["nama"], r["jabatan"], r["hari_kerja_per_minggu"], r["hari_terjadwal"],
                         r["hadir"], r["hadir_di_hari_libur"], r["izin"], r["sakit"], r["cuti"], r["alpa"],
                         r["dinas"], r["tanpa_keterangan"], r["terlambat_kali"], r["terlambat_menit"],
                         r["pulang_cepat_kali"], r["pulang_cepat_menit"],
                         fjam(Decimal(r["menit_kerja"]) / 60 if r["menit_kerja"] else 0).split(",")[0] + ":%02d"
                         % (r["menit_kerja"] % 60), r["hari_tidak_lengkap"], fjam(r["lembur_jam_hari_kerja"]),
                         fjam(r["lembur_jam_hari_libur"]), fjam(r["lembur_jam_setara"]),
                         r["dasar_upah_lembur"] if r["dasar_upah_lembur"] is not None else "",
                         r["upah_lembur"] if r["upah_lembur"] is not None else ""])
        file["csv"] = tulis_csv(args.csv, hdr, rows)
    if args.csv_harian:
        hdr = ["kode", "nama", "tanggal", "hari", "jenis_hari", "status", "jadwal_masuk", "jadwal_pulang", "masuk",
               "pulang", "terlambat_menit", "pulang_cepat_menit", "jam_kerja", "lembur_disetujui_jam"]
        rows = []
        for r in hasil:
            for h in harian[r["kode"]]:
                if h["status"] == "libur" and not h["lembur_jam"]:
                    continue
                mk = h["menit_kerja"]
                rows.append([r["kode"], r["nama"], ftgl(date.fromisoformat(h["tanggal"])), h["hari"], h["jenis_hari"],
                             h["status"], h["jadwal_masuk"], h["jadwal_pulang"],
                             _dt(h["masuk"]).strftime("%H.%M") if h["masuk"] else "",
                             (_dt(h["pulang"]).strftime("%H.%M") + ("" if _dt(h["pulang"]).date().isoformat() ==
                                                                    h["tanggal"] else " (+1)")) if h["pulang"] else "",
                             h["terlambat_menit"] or "", h["pulang_cepat_menit"] or "",
                             "%d:%02d" % divmod(mk, 60) if mk is not None else "",
                             fjam(h["lembur_jam"]) if h["lembur_jam"] else ""])
        file["csv_harian"] = tulis_csv(args.csv_harian, hdr, rows)
    if args.csv_gaji:
        file["csv_gaji"], catat = _ekspor_gaji(args, hasil)
        data["catatan_ekspor_gaji"] = catat
        baris += ["", "File untuk slip-gaji-bpjs: %s" % file["csv_gaji"]] + ["Catatan: " + c for c in catat]
    if file:
        data["file"] = file
        baris += ["", "File: " + ", ".join(file.values())]
    return data, "\n".join(baris)


def _ekspor_gaji(args, hasil):
    """CSV kolom slip-gaji-bpjs: lembur_hari_kerja '2+3', lembur_hari_libur '8+5p'."""
    catat = []
    pola = {r["hari_kerja_per_minggu"] for r in hasil if r["lembur_rincian"] and not r["tanpa_lembur"]}
    if len(pola) > 1:
        catat.append("Ada karyawan pola 5 dan 6 hari kerja. slip-gaji-bpjs memakai satu --hari-kerja per jalan: "
                     "ekspor terpisah dengan --pola 5 dan --pola 6.")
    elif pola:
        catat.append("Jalankan slip-gaji-bpjs dengan --hari-kerja %d." % pola.pop())
    catat.append("slip-gaji-bpjs menghitung ulang rupiah lembur dari gaji pokok + tunjangan tetap di file gajinya; "
                 "bandingkan dengan angka rekap ini.")
    isi = {}
    for r in hasil:
        if r["tanpa_lembur"]:
            lk = ll = ""
        else:
            lk, ll = _jam_list_str(r["_list_kerja"]), _jam_list_str(r["_list_libur"], True)
        isi[r["nama"].lower()] = (r, lk, ll)
        isi[r["kode"].lower()] = (r, lk, ll)
    if args.gabung:
        tabel = baca_tabel(args.gabung)
        if not tabel:
            raise Gagal("File gaji untuk digabung kosong.")
        header = [h.strip() for h in tabel[0]]
        hn = [norm(h).replace(" ", "_") for h in header]
        if "nama" not in hn:
            raise Gagal("File gaji '%s' tidak punya kolom 'nama'." % args.gabung)
        for c in ("lembur_hari_kerja", "lembur_hari_libur"):
            if c not in hn:
                header.append(c)
                hn.append(c)
        i_nama, i_lk, i_ll = hn.index("nama"), hn.index("lembur_hari_kerja"), hn.index("lembur_hari_libur")
        i_rp = hn.index("lembur_rp") if "lembur_rp" in hn else (hn.index("lembur") if "lembur" in hn else None)
        i_nik = hn.index("nik") if "nik" in hn else None
        rows, cocok = [], set()
        for r in tabel[1:]:
            if not any((c or "").strip() for c in r):
                continue
            r = list(r) + [""] * (len(header) - len(r))
            cari = isi.get(r[i_nama].strip().lower()) or (isi.get(r[i_nik].strip().lower()) if i_nik is not None else None)
            if cari is None:
                catat.append("'%s' di file gaji tidak ada di data absensi; kolom lemburnya dibiarkan." % r[i_nama])
            else:
                rr, lk, ll = cari
                cocok.add(rr["kode"])
                if i_rp is not None and (r[i_rp] or "").strip() and (lk or ll):
                    catat.append("%s: file gaji sudah berisi nominal lembur (%s); jam lembur TIDAK diisi agar tidak "
                                 "dobel. Kosongkan salah satunya." % (r[i_nama], r[i_rp]))
                else:
                    r[i_lk], r[i_ll] = lk, ll
            rows.append(r)
        for r in hasil:
            if r["kode"] not in cocok and (r["_list_kerja"] or r["_list_libur"]):
                catat.append("%s punya lembur tetapi tidak ada di file gaji." % r["nama"])
        return tulis_csv(args.csv_gaji, header, rows), catat
    hdr = ["nama", "jabatan", "ptkp", "gaji_pokok", "tunjangan_tetap", "tunjangan_tidak_tetap", "lembur_hari_kerja",
           "lembur_hari_libur", "kode_absensi", "hari_hadir", "hari_alpa", "terlambat_menit"]
    rows = []
    for r in hasil:
        _, lk, ll = isi[r["kode"].lower()]
        rows.append([r["nama"], r["jabatan"], "", "", "", "", lk, ll, r["kode"], r["hadir"], r["alpa"],
                     r["terlambat_menit"]])
    catat.append("Kolom ptkp dan gaji wajib diisi dulu sebelum dipakai slip-gaji-bpjs (atau pakai --gabung "
                 "file-gaji.csv agar kolom lembur langsung dimasukkan ke file gaji yang sudah ada).")
    return tulis_csv(args.csv_gaji, hdr, rows), catat


def cmd_harian(args):
    db = path_db(args)
    conn = buka(db)
    kini = sekarang(args)
    try:
        d = tanggal_wajib(args.tanggal) if args.tanggal else kini.date()
        if d > kini.date():
            raise Gagal("Tanggal %s belum terjadi." % ftgl(d))
        cfg, libur, hasil, masalah, harian = analisa_semua(conn, d, d, kini, args.karyawan)
    finally:
        conn.close()
    judul = "ABSENSI %s, %s" % (HARI[d.weekday()].upper(), ftgl(d))
    if d == kini.date():
        judul += " (per %s)" % fjm(kini)
    if cfg["nama_usaha"]:
        judul += " - " + cfg["nama_usaha"]
    hadir, telat, belum, ket, libur_masuk, lembur, tidak_lengkap, pulang_cepat = [], [], [], [], [], [], [], []
    for r in hasil:
        h = harian[r["kode"]][0] if harian[r["kode"]] else None
        if h is None:
            continue
        if h["status"] == "hadir":
            hadir.append(r["nama"])
            if h["terlambat_menit"]:
                telat.append("%s %s (%d menit)" % (r["nama"], _dt(h["masuk"]).strftime("%H.%M"), h["terlambat_menit"]))
            if h["pulang_cepat_menit"]:
                pulang_cepat.append("%s %s (%d menit)" % (r["nama"], _dt(h["pulang"]).strftime("%H.%M"),
                                                          h["pulang_cepat_menit"]))
        elif h["status"] == "hadir di hari libur":
            libur_masuk.append(r["nama"])
        elif h["status"] == "tanpa keterangan":
            belum.append(r["nama"])
        elif h["status"] in JENIS_KET:
            ket.append("%s (%s)" % (r["nama"], h["status"]))
        if h["lembur_jam"]:
            lembur.append("%s %s jam" % (r["nama"], fjam(h["lembur_jam"])))
    terjadwal = sum(1 for r in hasil if harian[r["kode"]] and harian[r["kode"]][0]["jenis_hari"] == "kerja")
    baris = [judul]
    if d.isoformat() in libur:
        baris.append("Hari libur resmi: %s" % libur[d.isoformat()])
    baris.append("Hadir %d dari %d karyawan terjadwal" % (len(hadir), terjadwal))
    if telat:
        baris.append("Terlambat: " + ", ".join(telat))
    if pulang_cepat:
        baris.append("Pulang cepat: " + ", ".join(pulang_cepat))
    if ket:
        baris.append("Izin/sakit/cuti/alpa/dinas: " + ", ".join(ket))
    if belum:
        baris.append(("Belum ada absen: " if d == kini.date() else "Tidak absen & tanpa keterangan: ") + ", ".join(belum))
    if libur_masuk:
        baris.append("Masuk di hari libur: " + ", ".join(libur_masuk))
    if lembur:
        baris.append("Lembur disetujui: " + ", ".join(lembur))
    serius = [m for m in masalah if m["tingkat"] in ("salah", "cek")]
    if serius:
        baris.append("Perlu dicek: " + "; ".join("%s: %s" % (m["nama"], m["pesan"]) for m in serius[:10]))
    data = {"ok": True, "mode": "baca", "tanggal": d.isoformat(), "terjadwal": terjadwal, "hadir": hadir,
            "terlambat": telat, "pulang_cepat": pulang_cepat, "keterangan": ket, "belum_absen": belum,
            "masuk_hari_libur": libur_masuk, "lembur": lembur, "masalah": masalah}
    return data, "\n".join(baris)


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------


def buat_parser():
    umum = argparse.ArgumentParser(add_help=False)
    umum.add_argument("--db", help="Lokasi file database (default ~/KomunitechData/absensi/absensi.db)")
    umum.add_argument("--json", action="store_true", help="Keluaran JSON")
    umum.add_argument("--sekarang", help=argparse.SUPPRESS)
    tulis = argparse.ArgumentParser(add_help=False)
    tulis.add_argument("--ya", action="store_true", help="Simpan (tanpa ini hanya pratinjau)")

    p = argparse.ArgumentParser(prog="absensi.py", description="Absensi karyawan lokal + rekap + lembur PP 35/2021.")
    p.add_argument("--versi", action="version", version=VERSI)
    sub = p.add_subparsers(dest="perintah")
    sub.required = True

    s = sub.add_parser("init", parents=[umum, tulis], help="Buat database baru")
    s.set_defaults(fungsi=cmd_init)
    s = sub.add_parser("info", parents=[umum], help="Info database & pengaturan")
    s.set_defaults(fungsi=cmd_info)
    s = sub.add_parser("backup", parents=[umum], help="Buat salinan database")
    s.set_defaults(fungsi=cmd_backup)
    s = sub.add_parser("atur", parents=[umum, tulis], help="Toleransi terlambat, jeda tap ganda, nama usaha")
    s.add_argument("--toleransi", type=int, help="Toleransi terlambat (menit)")
    s.add_argument("--jeda-duplikat", type=int, help="Tap berjarak <= menit ini dianggap ganda (default 5)")
    s.add_argument("--nama-usaha")
    s.set_defaults(fungsi=cmd_atur)

    sh = sub.add_parser("shift", help="Kelola shift").add_subparsers(dest="aksi")
    sh.required = True
    s = sh.add_parser("tambah", parents=[umum, tulis], help="Tambah/ubah shift")
    s.add_argument("--kode", required=True)
    s.add_argument("--masuk")
    s.add_argument("--pulang")
    s.add_argument("--istirahat", type=int, help="Menit istirahat (tidak dihitung jam kerja), default 60")
    s.add_argument("--pulang-hari-pendek", help="Jam pulang di hari kerja terpendek (pola 6 hari), '-' untuk hapus")
    s.set_defaults(fungsi=cmd_shift_tambah)
    s = sh.add_parser("daftar", parents=[umum])
    s.set_defaults(fungsi=cmd_shift_daftar)

    lb = sub.add_parser("libur", help="Hari libur resmi").add_subparsers(dest="aksi")
    lb.required = True
    s = lb.add_parser("tambah", parents=[umum, tulis])
    s.add_argument("--tanggal")
    s.add_argument("--nama")
    s.add_argument("--file", help="CSV kolom tanggal;nama")
    s.set_defaults(fungsi=cmd_libur_tambah)
    s = lb.add_parser("hapus", parents=[umum, tulis])
    s.add_argument("--tanggal", required=True)
    s.set_defaults(fungsi=cmd_libur_hapus)
    s = lb.add_parser("daftar", parents=[umum])
    s.add_argument("--tahun")
    s.set_defaults(fungsi=cmd_libur_daftar)

    ky = sub.add_parser("karyawan", help="Data karyawan").add_subparsers(dest="aksi")
    ky.required = True

    def opsi_karyawan(s, wajib):
        s.add_argument("--kode", required=True, help="Kode karyawan, mis. A01")
        s.add_argument("--nama", required=wajib, help="Nama panggilan")
        s.add_argument("--jabatan")
        s.add_argument("--shift", help="Kode shift (default REG)")
        s.add_argument("--hari-kerja", dest="hari_kerja", choices=["5", "6"], help="Pola hari kerja per minggu")
        s.add_argument("--libur-mingguan", dest="libur_mingguan", help="mis. sabtu,minggu (default sesuai pola)")
        s.add_argument("--hari-pendek", dest="hari_pendek", help="Hari kerja terpendek pola 6 hari (default sabtu, '-' = tidak ada)")
        s.add_argument("--id-mesin", dest="id_mesin", help="Nomor ID/PIN di mesin absen (BUKAN NIK)")
        s.add_argument("--gaji-pokok", dest="gaji_pokok")
        s.add_argument("--tunjangan-tetap", dest="tunjangan_tetap")
        s.add_argument("--tunjangan-tidak-tetap", dest="tunjangan_tidak_tetap")
        s.add_argument("--upah-harian", dest="upah_harian", help="Untuk pekerja harian (Pasal 33)")
        s.add_argument("--tanpa-lembur", dest="tanpa_lembur", choices=["ya", "tidak"],
                       help="ya = golongan jabatan tertentu (Pasal 27), tidak dibayar lembur")

    s = ky.add_parser("tambah", parents=[umum, tulis])
    opsi_karyawan(s, True)
    s.set_defaults(fungsi=cmd_karyawan_tambah)
    s = ky.add_parser("ubah", parents=[umum, tulis])
    opsi_karyawan(s, False)
    s.add_argument("--nonaktif", action="store_true")
    s.add_argument("--aktifkan", action="store_true")
    s.set_defaults(fungsi=cmd_karyawan_ubah)
    s = ky.add_parser("daftar", parents=[umum])
    s.set_defaults(fungsi=cmd_karyawan_daftar)
    s = ky.add_parser("impor", parents=[umum, tulis])
    s.add_argument("file")
    s.set_defaults(fungsi=cmd_karyawan_impor)

    s = sub.add_parser("catat", parents=[umum, tulis], help="Catat masuk/pulang manual")
    s.add_argument("--karyawan", required=True, help="Kode atau nama")
    s.add_argument("--masuk", help="Jam masuk, mis. 08.12 atau 'sekarang'")
    s.add_argument("--pulang", help="Jam pulang, mis. 17.05 atau 'sekarang'")
    s.add_argument("--tanggal", help="Tanggal kerja (default hari ini)")
    s.add_argument("--lewat-tengah-malam", action="store_true", help="Jam pulang jatuh besok harinya")
    s.add_argument("--ganti", action="store_true", help="Ganti catatan yang sudah ada")
    s.set_defaults(fungsi=cmd_catat)

    s = sub.add_parser("keterangan", parents=[umum, tulis], help="Izin/sakit/cuti/alpa/dinas")
    s.add_argument("--karyawan", required=True)
    s.add_argument("--jenis", required=True, choices=JENIS_KET)
    s.add_argument("--tanggal", required=True)
    s.add_argument("--sampai", help="Untuk beberapa hari (hari istirahat/libur dilewati)")
    s.add_argument("--catatan")
    s.set_defaults(fungsi=cmd_keterangan)

    s = sub.add_parser("lembur", parents=[umum, tulis], help="Catat lembur yang DISETUJUI")
    s.add_argument("--karyawan", required=True)
    s.add_argument("--tanggal", required=True, help="Tanggal kerja (tanggal mulai shift)")
    s.add_argument("--jam", required=True, help="Jam lembur disetujui, mis. 2 atau 1,5")
    s.add_argument("--catatan", help="Siapa yang memerintahkan/menyetujui")
    s.add_argument("--ganti", action="store_true")
    s.set_defaults(fungsi=cmd_lembur)

    s = sub.add_parser("hapus", parents=[umum, tulis], help="Hapus data satu karyawan pada satu tanggal")
    s.add_argument("--karyawan", required=True)
    s.add_argument("--tanggal", required=True)
    s.add_argument("--jenis", choices=["tap", "keterangan", "lembur", "semua"], default="tap")
    s.set_defaults(fungsi=cmd_hapus)

    s = sub.add_parser("impor-absen", parents=[umum, tulis], help="Impor file dari mesin absen (CSV/XLSX)")
    s.add_argument("file")
    for f in SIN_ABSEN:
        s.add_argument("--kolom-" + f, dest="kolom_" + f, help="Nama kolom untuk %s ('-' = abaikan)" % f)
    s.add_argument("--format-tanggal", choices=["dmy", "mdy"], help="Urutan tanggal angka di file")
    s.add_argument("--dari")
    s.add_argument("--sampai")
    s.set_defaults(fungsi=cmd_impor_absen)

    s = sub.add_parser("rekap", parents=[umum], help="Rekap bulanan + lembur")
    s.add_argument("--bulan", help="YYYY-MM (default bulan ini s.d. hari ini)")
    s.add_argument("--dari")
    s.add_argument("--sampai")
    s.add_argument("--karyawan")
    s.add_argument("--pola", choices=["5", "6"], help="Hanya karyawan pola 5 atau 6 hari kerja")
    s.add_argument("--csv", help="Simpan rekap per karyawan ke CSV")
    s.add_argument("--csv-harian", help="Simpan rincian per hari ke CSV")
    s.add_argument("--csv-gaji", help="Simpan CSV untuk skill slip-gaji-bpjs")
    s.add_argument("--gabung", help="File CSV gaji slip-gaji-bpjs yang kolom lemburnya akan diisi")
    s.set_defaults(fungsi=cmd_rekap)

    s = sub.add_parser("harian", parents=[umum], help="Laporan absensi satu hari")
    s.add_argument("--tanggal")
    s.add_argument("--karyawan")
    s.set_defaults(fungsi=cmd_harian)
    return p


def main(argv=None):
    try:
        sys.stdout.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass
    args = buat_parser().parse_args(argv)
    if not hasattr(args, "ya"):
        args.ya = False
    try:
        data, teks = args.fungsi(args)
    except Gagal as e:
        out = {"ok": False, "error": e.pesan}
        out.update(e.detail)
        if args.json:
            print(json.dumps(out, ensure_ascii=False, indent=2, default=str))
        else:
            print("GAGAL: " + e.pesan, file=sys.stderr)
            for kk, v in e.detail.items():
                print("  %s: %s" % (kk, v), file=sys.stderr)
        return 1
    except sqlite3.OperationalError as e:
        pesan = ("Database sedang dipakai proses lain (%s). Coba lagi sebentar." % e) if "locked" in str(e) \
            else "Kesalahan database: %s" % e
        print(json.dumps({"ok": False, "error": pesan}, ensure_ascii=False) if args.json else "GAGAL: " + pesan,
              file=sys.stdout if args.json else sys.stderr)
        return 1
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2, default=str))
    else:
        print(teks)
    return 0


if __name__ == "__main__":
    sys.exit(main())
