#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""arsip-nota - rapikan foto/PDF nota & faktur UMKM: ganti nama file baku, pindahkan ke folder
per tahun/bulan, catat di indeks SQLite lokal. Python standar saja (sqlite3, hashlib, shutil, csv).
Script ini TIDAK membaca isi nota (OCR) - datanya diisi dari hasil skill ekstrak-nota-faktur atau
diketik pengguna.

Pakai --json di semua perintah. Field penting: ok, mode (pratinjau/tersimpan/baca), perlu_konfirmasi,
perlu_izin, peringatan, error, teks (siap tempel). Kode keluar: 0 = berhasil (termasuk pratinjau),
1 = gagal (pesan di error), 2 = perintah salah tulis.
"""
import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import sqlite3
import sys
from collections import OrderedDict
from datetime import date, datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from pathlib import Path

APLIKASI = "komunitech-arsip-nota"
SKEMA = 1

KATEGORI = OrderedDict([
    ("bahan-baku", ("Bahan baku", ["bahan", "baku", "sembako", "grosir", "supplier", "pemasok"])),
    ("operasional", ("Operasional", ["operasional", "atk", "kebersihan", "kantor"])),
    ("peralatan", ("Peralatan", ["peralatan", "alat", "mesin", "elektronik", "komputer", "printer"])),
    ("jasa", ("Jasa", ["jasa", "service", "servis", "konsultan", "desain", "iklan"])),
    ("transportasi", ("Transportasi", ["ongkir", "kirim", "bensin", "bbm", "tol", "parkir", "grab", "gojek", "gocar"])),
    ("listrik-air", ("Listrik/air/internet", ["listrik", "pln", "air", "pdam", "internet", "wifi", "pulsa", "telepon"])),
    ("sewa", ("Sewa", ["sewa", "kontrak", "rental"])),
    ("pajak", ("Pajak/retribusi", ["pajak", "pbb", "retribusi", "pph", "ppn"])),
    ("lain-lain", ("Lain-lain", [])),
])
JENIS_DOKUMEN = {"nota", "struk", "kuitansi", "invoice", "faktur", "bukti-transfer"}
EKSTENSI_DIKENAL = {".jpg", ".jpeg", ".png", ".heic", ".heif", ".webp", ".gif", ".tif", ".tiff", ".pdf", ".bmp"}
# Kode kategori kas-umkm yang cocok untuk pengeluaran (lihat CLAUDE.md & references/kas-umkm)
PETA_KATEGORI_KAS_UMKM = {
    "bahan-baku": "beli-stok", "peralatan": "beli-stok", "operasional": "lain-lain",
    "jasa": "lain-lain", "transportasi": "lain-lain", "listrik-air": "listrik-air",
    "sewa": "sewa", "pajak": "pajak", "lain-lain": "lain-lain",
}
KARAKTER_TERLARANG_WINDOWS = re.compile(r'[\x00-\x1f<>:"/\\|?*]')
NAMA_TERLARANG_WINDOWS = {"con", "prn", "aux", "nul"} | {"com%d" % i for i in range(1, 10)} | \
                          {"lpt%d" % i for i in range(1, 10)}
NAMA_BULAN = {}
for _i, _al in enumerate([("jan", "januari", "january"), ("feb", "februari", "february"),
                          ("mar", "maret", "march"), ("apr", "april"),
                          ("mei", "may"), ("jun", "juni", "june"),
                          ("jul", "juli", "july"), ("agu", "agt", "agustus", "aug", "august"),
                          ("sep", "sept", "september"), ("okt", "oktober", "oct", "october"),
                          ("nov", "nop", "november", "nopember"), ("des", "desember", "dec", "december")], 1):
    for _a in _al:
        NAMA_BULAN[_a] = _i
SATUAN_NOMINAL = {"rb": 1000, "ribu": 1000, "rbu": 1000, "k": 1000, "jt": 10 ** 6, "juta": 10 ** 6,
                  "jeti": 10 ** 6, "miliar": 10 ** 9, "milyar": 10 ** 9}


class Gagal(Exception):
    """Error yang pesannya aman ditampilkan ke pengguna."""

    def __init__(self, pesan, **detail):
        super().__init__(pesan)
        self.pesan = pesan
        self.detail = detail


def _timeout():
    try:
        return max(0.1, float(os.environ.get("KOMUNITECH_ARSIP_TIMEOUT", "15")))
    except ValueError:
        return 15.0


def _detik():
    return ("%.1f" % _timeout()).rstrip("0").rstrip(".").replace(".", ",")


def _terkunci(e):
    s = str(e).lower()
    return "locked" in s or "busy" in s


SARAN_PULIH = ("Pulihkan: arsip.py backup --daftar (lihat cadangan), lalu arsip.py restore --dari <file cadangan> "
               "(pratinjau, lalu --ya). File rusak otomatis dipindah ke folder backup-arsip, tidak dihapus. File "
               "asli/foto nota tidak pernah dihapus oleh script ini, hanya indeksnya.")
PESAN_TERKUNCI = ("Indeks arsip sedang dipakai program lain (mis. jadwal OpenClaw atau jendela lain) dan tidak "
                  "selesai dalam %s detik. Data aman. Tunggu sebentar lalu ulangi perintah yang sama.")


# --------------------------------------------------------------------------- waktu & tanggal
def hari_ini():
    return datetime.now().date()


def stempel():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def tgl_id(d):
    return d.strftime("%d/%m/%Y")


def _buat_tanggal(y, m, d, asli):
    try:
        return date(y, m, d)
    except ValueError:
        raise Gagal("Tanggal '%s' tidak ada di kalender." % asli)


def baca_tanggal(teks, boleh_depan=False):
    """Tanggal format Indonesia (hari/bulan/tahun 4 angka) atau ISO YYYY-MM-DD. Ambigu DITOLAK:
    tanpa tahun, tahun 2 angka, urutan bulan/hari (format Amerika)."""
    if teks is None or not str(teks).strip():
        raise Gagal("Tanggal kosong.")
    asli = str(teks).strip()
    acuan = hari_ini()
    s = re.sub(r"\s+", " ", asli.lower().replace(",", " ")).strip()
    rel = {"hari ini": 0, "hari-ini": 0, "sekarang": 0, "today": 0, "kemarin": -1, "kmrn": -1,
           "kemaren": -1, "yesterday": -1}
    d = None
    if s in rel:
        d = acuan + timedelta(days=rel[s])
    if d is None:
        m = re.fullmatch(r"(\d{1,3}) ?(hari|hr) ?(yang )?lalu", s)
        if m:
            d = acuan - timedelta(days=int(m.group(1)))
    if d is None:
        s2 = re.sub(r"^(tgl\.?|tanggal) ?", "", s).strip()
        m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", s2)
        if m:
            d = _buat_tanggal(int(m.group(1)), int(m.group(2)), int(m.group(3)), asli)
        if d is None:
            m = re.fullmatch(r"(\d{1,2})[/.-](\d{1,2})[/.-](\d+)", s2)
            if m:
                a, b, th = int(m.group(1)), int(m.group(2)), m.group(3)
                if len(th) != 4:
                    raise Gagal("Tanggal '%s' ambigu: tahun harus 4 angka. Tulis mis. %02d/%02d/20%s." %
                                (asli, a, b, th[-2:].zfill(2)))
                if b > 12 and a <= 12:
                    raise Gagal("Tanggal '%s' sepertinya berurutan bulan/hari (format Amerika). Tulis "
                                "hari/bulan/tahun: %02d/%02d/%s." % (asli, b, a, th))
                d = _buat_tanggal(int(th), b, a, asli)
        if d is None:
            m = re.fullmatch(r"(\d{1,2}) ?([a-z]+)\.?( (\d{4}))?", s2)
            if m and m.group(2) in NAMA_BULAN:
                if not m.group(4):
                    raise Gagal("Tanggal '%s' tidak menyebut tahun. Tulis lengkap, mis. %s %s %d." %
                                (asli, m.group(1), m.group(2), acuan.year))
                d = _buat_tanggal(int(m.group(4)), NAMA_BULAN[m.group(2)], int(m.group(1)), asli)
        if d is None:
            if re.fullmatch(r"\d{1,2}[/.-]\d{1,2}", s2):
                raise Gagal("Tanggal '%s' tidak menyebut tahun. Tulis lengkap hari/bulan/tahun, mis. %s/%d." %
                            (asli, s2.replace("-", "/").replace(".", "/"), acuan.year))
            raise Gagal("Tanggal '%s' tidak dikenali. Contoh: 26/09/2026, 26 Sep 2026, hari ini, kemarin." % asli)
    if d.year < 2000:
        raise Gagal("Tanggal '%s' terlalu lama (sebelum tahun 2000); periksa lagi." % asli)
    if not boleh_depan and d > acuan:
        raise Gagal("Tanggal %s ada di masa depan (hari ini %s). Nota tidak mungkin bertanggal masa depan." %
                    (tgl_id(d), tgl_id(acuan)))
    return d


def baca_bulan(teks):
    acuan = hari_ini()
    s = re.sub(r"\s+", " ", str(teks or "").strip().lower())
    if s in ("ini", "bulan ini", "bulan-ini"):
        y, m = acuan.year, acuan.month
    elif s in ("lalu", "bulan lalu", "bulan-lalu"):
        y, m = (acuan.year, acuan.month - 1) if acuan.month > 1 else (acuan.year - 1, 12)
    else:
        mt = re.fullmatch(r"(\d{1,2})[/.-](\d{4})", s)
        mi = re.fullmatch(r"(\d{4})-(\d{1,2})", s)
        mn = re.fullmatch(r"([a-z]+) (\d{4})", s)
        if mt:
            m, y = int(mt.group(1)), int(mt.group(2))
        elif mi:
            y, m = int(mi.group(1)), int(mi.group(2))
        elif mn and mn.group(1) in NAMA_BULAN:
            y, m = int(mn.group(2)), NAMA_BULAN[mn.group(1)]
        else:
            raise Gagal("Bulan '%s' tidak dikenali. Contoh: ini, lalu, 09/2026, September 2026." % teks)
        if not 1 <= m <= 12:
            raise Gagal("Bulan '%s' tidak ada." % teks)
    awal = date(y, m, 1)
    akhir = date(y + 1, 1, 1) - timedelta(days=1) if m == 12 else date(y, m + 1, 1) - timedelta(days=1)
    return awal, akhir


def ambil_periode(args):
    """(dari, sampai, jenis) dari --bulan / --tahun / --dari --sampai. None,None jika tidak diisi."""
    if getattr(args, "dari", None) or getattr(args, "sampai", None):
        if not (args.dari and args.sampai):
            raise Gagal("Isi --dari dan --sampai sekaligus (format 01/09/2026).")
        a, b = baca_tanggal(args.dari, True), baca_tanggal(args.sampai, True)
        if b < a:
            raise Gagal("--sampai (%s) lebih awal dari --dari (%s)." % (tgl_id(b), tgl_id(a)))
        return a, b, "rentang"
    if getattr(args, "bulan", None):
        a, b = baca_bulan(args.bulan)
        return a, b, "bulan"
    if getattr(args, "tahun", None):
        try:
            y = int(str(args.tahun).strip())
        except ValueError:
            raise Gagal("Tahun '%s' tidak valid." % args.tahun)
        if not 2000 <= y <= 2100:
            raise Gagal("Tahun '%s' tidak valid." % args.tahun)
        return date(y, 1, 1), date(y, 12, 31), "tahun"
    return None, None, "semua"


# --------------------------------------------------------------------------- angka
def rp(n):
    if n is None:
        return "-"
    n = int(n)
    return ("-" if n < 0 else "") + "Rp " + "{:,}".format(abs(n)).replace(",", ".")


def bulat(x):
    """Rupiah terdekat, setengah ke atas."""
    return int(Decimal(x).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def parse_nominal(teks):
    """'4,5 jt' | '4.500.000' | 'Rp4.500.000' | '150rb' | '25000' | '25000.50' -> (Decimal bulat, dibulatkan?)."""
    if teks is None or not str(teks).strip():
        raise Gagal("Nominal kosong.")
    asli = str(teks).strip()
    s = re.sub(r"(?i)^\s*(rp\.?|idr)\s*", "", asli).strip()
    s = re.sub(r"(?i)\s*(,-|\.-)$", "", s)
    if s.startswith("-") or s.startswith("("):
        raise Gagal("Nominal '%s' tidak boleh minus." % asli)
    total = Decimal(0)
    sisa = s
    cocok_satuan = False
    for kata, kali in sorted(SATUAN_NOMINAL.items(), key=lambda kv: -len(kv[0])):
        for m in re.finditer(r"(\d+(?:[.,]\d+)?) ?%s\b" % kata, sisa, re.I):
            angka = m.group(1).replace(",", ".")
            try:
                total += Decimal(angka) * kali
            except InvalidOperation:
                raise Gagal("Nominal '%s' tidak dikenali." % asli)
            cocok_satuan = True
        sisa = re.sub(r"(\d+(?:[.,]\d+)?) ?%s\b" % kata, " ", sisa, flags=re.I)
    sisa = sisa.strip()
    if sisa:
        s2 = sisa.replace(" ", "")
        if re.fullmatch(r"\d{1,3}(\.\d{3})+(,\d+)?", s2):
            s2 = s2.replace(".", "").replace(",", ".")
        elif re.fullmatch(r"\d+,\d{1,2}", s2) and cocok_satuan:
            s2 = s2.replace(",", ".")
        else:
            s2 = s2.replace(",", "")
        try:
            total += Decimal(s2)
        except InvalidOperation:
            raise Gagal("Nominal '%s' tidak dikenali. Contoh: 150000, 150rb, Rp1.250.000, 4,5jt." % asli)
    elif not cocok_satuan:
        raise Gagal("Nominal '%s' tidak dikenali." % asli)
    if total <= 0:
        raise Gagal("Nominal '%s' harus lebih dari nol." % asli)
    dibulatkan = (total != total.to_integral_value())
    return bulat(total), dibulatkan


def tebak_kategori(*teks_list):
    gabungan = " ".join(str(t or "") for t in teks_list).lower()
    for kode, (_label, kata_kunci) in KATEGORI.items():
        for kk in kata_kunci:
            if kk in gabungan:
                return kode, True
    return "lain-lain", False


def label_kategori(kode):
    return KATEGORI.get(kode, ("(tidak dikenal)", []))[0]


def kode_kategori(teks):
    if not teks:
        return None
    k = str(teks).strip().lower().replace(" ", "-").replace("_", "-")
    if k not in KATEGORI:
        raise Gagal("Kategori '%s' tidak dikenal. Pilihan: %s." % (teks, ", ".join(KATEGORI)))
    return k


def kode_jenis(teks):
    if not teks:
        return "nota"
    k = str(teks).strip().lower().replace(" ", "-")
    if k not in JENIS_DOKUMEN:
        raise Gagal("Jenis dokumen '%s' tidak dikenal. Pilihan: %s." % (teks, ", ".join(sorted(JENIS_DOKUMEN))))
    return k


# --------------------------------------------------------------------------- nama file aman
def nama_bagian_aman(teks, maks=40):
    s = str(teks or "").strip()
    s = KARAKTER_TERLARANG_WINDOWS.sub("", s)
    s = re.sub(r"\s+", "-", s)
    s = re.sub(r"[^A-Za-z0-9._-]", "", s)
    s = re.sub(r"-{2,}", "-", s).strip("-. ")
    if not s:
        s = "tanpa-nama"
    if s.lower() in NAMA_TERLARANG_WINDOWS:
        s = "_" + s
    s = s[:maks].strip("-. ")
    return s or "tanpa-nama"


def nama_arsip(tanggal_iso, vendor, nominal, ekstensi):
    return "%s_%s_%s%s" % (tanggal_iso, nama_bagian_aman(vendor), int(nominal), ekstensi)


def path_unik(target):
    if not target.exists():
        return target
    n = 2
    stem, suf = target.stem, target.suffix
    while True:
        kandidat = target.with_name("%s-%d%s" % (stem, n, suf))
        if not kandidat.exists():
            return kandidat
        n += 1


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for blok in iter(lambda: f.read(1024 * 1024), b""):
            h.update(blok)
    return h.hexdigest()


# --------------------------------------------------------------------------- database
SKEMA_SQL = """
CREATE TABLE meta(kunci TEXT PRIMARY KEY, nilai TEXT);
CREATE TABLE nota(id INTEGER PRIMARY KEY, tanggal TEXT NOT NULL, vendor TEXT NOT NULL,
  nominal INTEGER NOT NULL CHECK(nominal > 0), kategori TEXT NOT NULL, jenis_dokumen TEXT NOT NULL DEFAULT 'nota',
  nama_file TEXT NOT NULL, path_file TEXT NOT NULL, hash_sha256 TEXT NOT NULL, ukuran_byte INTEGER NOT NULL,
  catatan TEXT NOT NULL DEFAULT '', sumber_asli TEXT, status TEXT NOT NULL DEFAULT 'aktif', dibuat TEXT NOT NULL);
CREATE INDEX ix_nota_tanggal ON nota(tanggal);
CREATE INDEX ix_nota_hash ON nota(hash_sha256);
CREATE INDEX ix_nota_vendor ON nota(vendor);
CREATE TABLE log(id INTEGER PRIMARY KEY, waktu TEXT NOT NULL, perintah TEXT NOT NULL, ringkasan TEXT);
"""


def path_db(args):
    if getattr(args, "db", None):
        p = Path(args.db).expanduser()
    elif os.environ.get("KOMUNITECH_ARSIP_DB"):
        p = Path(os.environ["KOMUNITECH_ARSIP_DB"]).expanduser()
    elif os.environ.get("KOMUNITECH_DATA"):
        p = Path(os.environ["KOMUNITECH_DATA"]).expanduser() / "arsip-nota" / "arsip.db"
    else:
        p = Path.home() / "KomunitechData" / "arsip-nota" / "arsip.db"
    return p.resolve()


def folder_arsip_default(db):
    return db.parent / "arsip"


def folder_backup(db):
    return db.parent / "backup-arsip"


def buka(db, baca_saja=False):
    if not db.is_file():
        raise Gagal("Indeks arsip belum ada di %s. Jalankan dulu: arsip.py init (pratinjau, lalu --ya setelah "
                    "pengguna setuju)." % db, db=str(db), belum_ada=True)
    if db.stat().st_size == 0:
        raise Gagal("File %s kosong (0 byte), bukan indeks arsip yang bisa dibaca. %s" % (db, SARAN_PULIH), rusak=True)

    def sambung(ro):
        try:
            if ro:
                c = sqlite3.connect(db.resolve().as_uri() + "?mode=ro", uri=True, timeout=_timeout(),
                                    isolation_level=None)
            else:
                c = sqlite3.connect(str(db), timeout=_timeout(), isolation_level=None)
        except sqlite3.OperationalError as e:
            raise Gagal("Indeks %s tidak bisa dibuka (%s). Periksa folder dan izin aksesnya." % (db, e))
        c.row_factory = sqlite3.Row
        return c

    ro = baca_saja
    while True:
        conn = sambung(ro)
        try:
            r = conn.execute("SELECT nilai FROM meta WHERE kunci='aplikasi'").fetchone()
            sk = conn.execute("SELECT nilai FROM meta WHERE kunci='skema'").fetchone()
            conn.execute("SELECT COUNT(*) FROM nota").fetchone()
            break
        except sqlite3.OperationalError as e:
            conn.close()
            pesan = str(e).lower()
            if _terkunci(e):
                raise Gagal(PESAN_TERKUNCI % _detik())
            if ro and "readonly" in pesan:
                ro = False
                continue
            if "no such table" in pesan:
                raise Gagal("File %s bukan indeks arsip-nota (%s). File itu tidak diubah; periksa --db." % (db, e))
            raise Gagal("Indeks %s tidak bisa dibaca (%s). Jangan hapus file itu. %s" % (db, e, SARAN_PULIH), rusak=True)
        except sqlite3.DatabaseError:
            conn.close()
            raise Gagal("File %s rusak atau bukan indeks arsip-nota. Jangan hapus file itu. %s" % (db, SARAN_PULIH),
                        rusak=True)
    if not r or r[0] != APLIKASI:
        conn.close()
        raise Gagal("File %s bukan indeks arsip-nota. File itu tidak diubah; periksa --db." % db)
    if sk and str(sk[0]).isdigit() and int(sk[0]) > SKEMA:
        conn.close()
        raise Gagal("Indeks dibuat oleh arsip-nota versi lebih baru (skema %s). Perbarui skill arsip-nota dulu." % sk[0])
    return conn


def nama_backup_unik(folder, dasar):
    tujuan = folder / (dasar + ".db")
    n = 2
    while tujuan.exists():
        tujuan = folder / ("%s-%d.db" % (dasar, n))
        n += 1
    return tujuan


def buat_backup(db, label):
    if not db.is_file():
        return None
    fol = folder_backup(db)
    fol.mkdir(parents=True, exist_ok=True)
    tujuan = nama_backup_unik(fol, "arsip-%s-%s" % (datetime.now().strftime("%Y%m%d-%H%M%S"), label))
    src = sqlite3.connect(str(db), timeout=_timeout())
    dst = sqlite3.connect(str(tujuan))
    try:
        src.backup(dst)
    except sqlite3.OperationalError as e:
        dst.close()
        try:
            tujuan.unlink()
        except OSError:
            pass
        if _terkunci(e):
            raise Gagal(PESAN_TERKUNCI % _detik())
        raise
    finally:
        dst.close()
        src.close()
    return str(tujuan)


def backup_sebelum_tulis(db):
    """Cadangan sekali sehari sebelum perubahan pertama hari itu. Simpan 30 terakhir."""
    if not db.is_file():
        return None
    tanda = folder_backup(db) / ".terakhir"
    hari = hari_ini().isoformat()
    if tanda.is_file():
        try:
            if tanda.read_text(encoding="utf-8").strip() == hari:
                return None
        except OSError:
            pass
    path_bk = buat_backup(db, "harian")
    try:
        tanda.parent.mkdir(parents=True, exist_ok=True)
        tanda.write_text(hari, encoding="utf-8")
    except OSError:
        pass
    fol = folder_backup(db)
    cadangan = sorted([p for p in fol.glob("arsip-*.db")], key=lambda p: p.stat().st_mtime)
    for lama in cadangan[:-30]:
        try:
            lama.unlink()
        except OSError:
            pass
    return path_bk


def catat_log(conn, perintah, ringkasan):
    conn.execute("INSERT INTO log(waktu, perintah, ringkasan) VALUES (?,?,?)", (stempel(), perintah, ringkasan))


def jalankan_tulis(args, perintah, kerja):
    db = path_db(args)
    if not getattr(args, "ya", False):
        return kerja(None, db, pratinjau=True)
    backup = None
    if db.is_file():
        backup = backup_sebelum_tulis(db)
    conn = buka(db)
    try:
        conn.execute("BEGIN IMMEDIATE")
        hasil = kerja(conn, db, pratinjau=False)
        conn.execute("COMMIT")
    except sqlite3.OperationalError as e:
        conn.execute("ROLLBACK") if conn.in_transaction else None
        conn.close()
        if _terkunci(e):
            raise Gagal(PESAN_TERKUNCI % _detik())
        raise
    except Exception:
        if conn.in_transaction:
            conn.execute("ROLLBACK")
        conn.close()
        raise
    conn.close()
    if backup:
        hasil[0]["backup"] = backup
    return hasil


# --------------------------------------------------------------------------- perintah
def cmd_init(args):
    db = path_db(args)
    folder_arsip = Path(args.folder_arsip).expanduser().resolve() if args.folder_arsip else folder_arsip_default(db)
    if db.is_file() and not args.mulai_baru:
        raise Gagal("Indeks arsip sudah ada di %s. Pakai perintah lain (mis. 'tambah', 'info'), atau tambahkan "
                    "--mulai-baru untuk membuat indeks kosong baru (file lama dipindah, tidak dihapus)." % db)
    if not args.ya:
        data = {"ok": True, "mode": "pratinjau", "db": str(db), "folder_arsip": str(folder_arsip),
                "perlu_konfirmasi": True}
        teks = ("Akan dibuat indeks arsip baru di:\n  %s\nFolder arsip (file nota dipindah/disalin ke sini, per "
                "tahun/bulan):\n  %s\nSimpan? Balas \"ya\", lalu jalankan ulang perintah ini dengan --ya." %
                (db, folder_arsip))
        return data, teks
    db.parent.mkdir(parents=True, exist_ok=True)
    if db.is_file() and args.mulai_baru:
        lama = path_unik(db.with_name(db.stem + "-lama.db"))
        shutil.move(str(db), str(lama))
    conn = sqlite3.connect(str(db), timeout=_timeout())
    conn.executescript(SKEMA_SQL)
    conn.execute("INSERT INTO meta VALUES ('aplikasi', ?)", (APLIKASI,))
    conn.execute("INSERT INTO meta VALUES ('skema', ?)", (str(SKEMA),))
    conn.execute("INSERT INTO meta VALUES ('folder_arsip', ?)", (str(folder_arsip),))
    conn.execute("INSERT INTO meta VALUES ('dibuat', ?)", (stempel(),))
    catat_log(conn, "init", "Indeks arsip dibuat.")
    conn.commit()
    conn.close()
    folder_arsip.mkdir(parents=True, exist_ok=True)
    data = {"ok": True, "mode": "tersimpan", "db": str(db), "folder_arsip": str(folder_arsip)}
    teks = "Indeks arsip siap di %s. Folder arsip: %s. Kirim foto/PDF nota untuk mulai mengarsipkan." % \
           (db, folder_arsip)
    return data, teks


def cmd_info(args):
    db = path_db(args)
    if not db.is_file():
        data = {"ok": True, "mode": "baca", "db": str(db), "ada": False}
        return data, "Belum ada indeks arsip di %s. Jalankan 'init' dulu." % db
    conn = buka(db, baca_saja=True)
    folder_arsip = conn.execute("SELECT nilai FROM meta WHERE kunci='folder_arsip'").fetchone()
    folder_arsip = folder_arsip[0] if folder_arsip else str(folder_arsip_default(db))
    jml = conn.execute("SELECT COUNT(*) FROM nota").fetchone()[0]
    total = conn.execute("SELECT COALESCE(SUM(nominal),0) FROM nota").fetchone()[0]
    per_kat = conn.execute("SELECT kategori, COUNT(*), SUM(nominal) FROM nota GROUP BY kategori "
                            "ORDER BY SUM(nominal) DESC").fetchall()
    conn.close()
    data = {"ok": True, "mode": "baca", "db": str(db), "ada": True, "folder_arsip": folder_arsip,
            "jumlah_nota": jml, "total_nominal": total,
            "per_kategori": [{"kategori": r[0], "jumlah": r[1], "total": r[2]} for r in per_kat]}
    teks = "Indeks arsip: %s\nFolder arsip: %s\nJumlah nota: %d | Total nominal: %s" % \
           (db, folder_arsip, jml, rp(total))
    return data, teks


def _validasi_file_sumber(path_teks):
    if not path_teks:
        raise Gagal("--file wajib diisi (path foto/PDF nota).")
    p = Path(path_teks).expanduser()
    if not p.exists():
        raise Gagal("File '%s' tidak ditemukan. Periksa lagi lokasinya." % path_teks)
    if p.is_dir():
        raise Gagal("'%s' adalah folder, bukan file. Sebutkan file foto/PDF-nya." % path_teks)
    if p.stat().st_size == 0:
        raise Gagal("File '%s' kosong (0 byte), sepertinya rusak/gagal diunduh." % path_teks)
    return p.resolve()


def cmd_tambah(args):
    sumber = _validasi_file_sumber(args.file)
    tanggal = baca_tanggal(args.tanggal)
    nominal, dibulatkan = parse_nominal(args.nominal)
    peringatan = []
    asumsi = []
    if dibulatkan:
        peringatan.append("Nominal '%s' bukan bilangan bulat, dibulatkan ke rupiah terdekat: %s." %
                          (args.nominal, rp(nominal)))
    jenis = kode_jenis(args.jenis)
    if args.kategori:
        kategori = kode_kategori(args.kategori)
    else:
        kategori, ditebak = tebak_kategori(args.vendor, args.catatan)
        if ditebak:
            asumsi.append("Kategori '%s' ditebak dari nama vendor/catatan." % label_kategori(kategori))
        else:
            asumsi.append("Kategori tidak disebut, dipakai 'Lain-lain'.")
    ekstensi = sumber.suffix.lower()
    if ekstensi not in EKSTENSI_DIKENAL:
        peringatan.append("Jenis file '%s' tidak umum untuk nota/faktur (biasanya .jpg/.png/.pdf). File tetap "
                          "diarsipkan apa adanya." % (ekstensi or "(tanpa akhiran)"))
    hash_sumber = sha256_file(sumber)
    ukuran = sumber.stat().st_size

    db = path_db(args)
    ada_db = db.is_file()
    folder_arsip_teks = None
    duplikat_persis = None
    if ada_db:
        conn = buka(db, baca_saja=True)
        r = conn.execute("SELECT nilai FROM meta WHERE kunci='folder_arsip'").fetchone()
        folder_arsip_teks = r[0] if r else None
        dup = conn.execute("SELECT id, tanggal, vendor, nominal, path_file FROM nota WHERE hash_sha256=? "
                            "AND status='aktif'", (hash_sumber,)).fetchone()
        if dup:
            duplikat_persis = dict(dup)
        conn.close()
    folder_arsip = Path(args.folder_arsip).expanduser().resolve() if args.folder_arsip else \
        (Path(folder_arsip_teks) if folder_arsip_teks else folder_arsip_default(db))

    if duplikat_persis and not args.izinkan_duplikat:
        data = {"ok": True, "mode": "pratinjau" if not args.ya else "tersimpan", "perlu_izin": ["izinkan_duplikat"],
                "duplikat": duplikat_persis, "hash_sha256": hash_sumber}
        teks = ("File ini isinya SAMA PERSIS dengan nota yang sudah diarsipkan (ID %s, %s, %s, %s).\n"
                "Kalau ini memang dokumen berbeda (mis. difoto ulang), tambahkan --izinkan-duplikat. Kalau memang "
                "sama, tidak perlu diarsipkan lagi." %
                (duplikat_persis["id"], tgl_id(datetime.strptime(duplikat_persis["tanggal"], "%Y-%m-%d").date()),
                 duplikat_persis["vendor"], rp(duplikat_persis["nominal"])))
        return data, teks

    nama_baru = nama_arsip(tanggal.isoformat(), args.vendor, nominal, ekstensi)
    target_folder = folder_arsip / ("%04d" % tanggal.year) / ("%02d" % tanggal.month)
    target = path_unik(target_folder / nama_baru)
    aksi = "dipindah" if args.pindah else "disalin"

    if not args.ya:
        data = {"ok": True, "mode": "pratinjau", "perlu_konfirmasi": True, "tanggal": tanggal.isoformat(),
                "vendor": args.vendor, "nominal": nominal, "kategori": kategori, "jenis_dokumen": jenis,
                "file_sumber": str(sumber), "file_tujuan": str(target), "aksi": aksi,
                "hash_sha256": hash_sumber, "peringatan": peringatan, "asumsi": asumsi}
        teks = ("Akan diarsipkan (belum disimpan, file asli belum %s):\n"
                "  Dari : %s\n  Ke   : %s (%s)\n  Tanggal: %s | Vendor: %s | Nominal: %s | Kategori: %s | Jenis: %s\n"
                "%s%sLanjutkan? Balas \"ya\", lalu jalankan ulang perintah ini dengan --ya." %
                (aksi, sumber, target, aksi, tgl_id(tanggal), args.vendor, rp(nominal), label_kategori(kategori),
                 jenis, ("Asumsi: " + " ".join(asumsi) + "\n" if asumsi else ""),
                 ("Peringatan: " + " ".join(peringatan) + "\n" if peringatan else "")))
        return data, teks

    if not ada_db:
        raise Gagal("Indeks arsip belum ada di %s. Jalankan dulu: arsip.py init --ya." % db, belum_ada=True)

    def kerja(conn, db2, pratinjau):
        target_folder.mkdir(parents=True, exist_ok=True)
        target2 = path_unik(target_folder / nama_baru)
        if args.pindah:
            shutil.move(str(sumber), str(target2))
        else:
            shutil.copy2(str(sumber), str(target2))
        cur = conn.execute(
            "INSERT INTO nota(tanggal, vendor, nominal, kategori, jenis_dokumen, nama_file, path_file, "
            "hash_sha256, ukuran_byte, catatan, sumber_asli, dibuat) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (tanggal.isoformat(), args.vendor.strip(), nominal, kategori, jenis, target2.name, str(target2),
             hash_sumber, ukuran, (args.catatan or "").strip(), str(sumber), stempel()))
        nota_id = cur.lastrowid
        catat_log(conn, "tambah", "Nota #%d %s %s diarsipkan ke %s." % (nota_id, args.vendor, rp(nominal), target2))
        data = {"ok": True, "mode": "tersimpan", "id": nota_id, "tanggal": tanggal.isoformat(),
                "vendor": args.vendor, "nominal": nominal, "kategori": kategori, "jenis_dokumen": jenis,
                "file_tujuan": str(target2), "aksi": aksi, "hash_sha256": hash_sumber, "peringatan": peringatan,
                "asumsi": asumsi}
        teks = "Tersimpan (ID %d). File %s ke %s. %s" % (nota_id, aksi, target2,
                                                          " ".join(peringatan) if peringatan else "")
        return data, teks.strip()

    return jalankan_tulis(args, "tambah", kerja)


def cmd_cari(args):
    db = path_db(args)
    conn = buka(db, baca_saja=True)
    klausa, param = ["status='aktif'"], []
    if args.vendor:
        klausa.append("vendor LIKE ? COLLATE NOCASE")
        param.append("%%%s%%" % args.vendor)
    if args.kategori:
        klausa.append("kategori=?")
        param.append(kode_kategori(args.kategori))
    if args.dari or args.sampai:
        if not (args.dari and args.sampai):
            conn.close()
            raise Gagal("Isi --dari dan --sampai sekaligus.")
        a, b = baca_tanggal(args.dari, True), baca_tanggal(args.sampai, True)
        klausa.append("tanggal BETWEEN ? AND ?")
        param += [a.isoformat(), b.isoformat()]
    if args.nominal_min:
        klausa.append("nominal >= ?")
        param.append(parse_nominal(args.nominal_min)[0])
    if args.nominal_max:
        klausa.append("nominal <= ?")
        param.append(parse_nominal(args.nominal_max)[0])
    if args.cari:
        klausa.append("(vendor LIKE ? COLLATE NOCASE OR catatan LIKE ? COLLATE NOCASE)")
        param += ["%%%s%%" % args.cari, "%%%s%%" % args.cari]
    sql = "SELECT * FROM nota WHERE %s ORDER BY tanggal DESC, id DESC" % " AND ".join(klausa)
    baris = [dict(r) for r in conn.execute(sql, param).fetchall()]
    conn.close()
    total = sum(b["nominal"] for b in baris)
    data = {"ok": True, "mode": "baca", "jumlah": len(baris), "total_nominal": total, "nota": baris}
    if not baris:
        teks = "Tidak ada nota yang cocok."
    else:
        garis = ["%-4s %-10s %-22s %14s  %-16s %s" % ("ID", "Tanggal", "Vendor", "Nominal", "Kategori", "Catatan")]
        for b in baris:
            garis.append("%-4d %-10s %-22s %14s  %-16s %s" %
                         (b["id"], tgl_id(datetime.strptime(b["tanggal"], "%Y-%m-%d").date()), b["vendor"][:22],
                          rp(b["nominal"]), label_kategori(b["kategori"]), (b["catatan"] or "")[:40]))
        garis.append("Ditemukan %d nota, total %s." % (len(baris), rp(total)))
        teks = "\n".join(garis)
    return data, teks


def cmd_rekap(args):
    db = path_db(args)
    conn = buka(db, baca_saja=True)
    dari, sampai, jenis_periode = ambil_periode(args)
    klausa, param = ["status='aktif'"], []
    if dari:
        klausa.append("tanggal BETWEEN ? AND ?")
        param += [dari.isoformat(), sampai.isoformat()]
    if args.kategori:
        klausa.append("kategori=?")
        param.append(kode_kategori(args.kategori))
    sql_where = " AND ".join(klausa)
    total = conn.execute("SELECT COALESCE(SUM(nominal),0), COUNT(*) FROM nota WHERE %s" % sql_where, param).fetchone()
    per_kat = conn.execute("SELECT kategori, COUNT(*), SUM(nominal) FROM nota WHERE %s GROUP BY kategori "
                            "ORDER BY SUM(nominal) DESC" % sql_where, param).fetchall()
    per_vendor = conn.execute("SELECT vendor, COUNT(*), SUM(nominal) FROM nota WHERE %s GROUP BY vendor "
                              "ORDER BY SUM(nominal) DESC LIMIT 10" % sql_where, param).fetchall()
    conn.close()
    data = {"ok": True, "mode": "baca", "periode": jenis_periode,
            "dari": dari.isoformat() if dari else None, "sampai": sampai.isoformat() if sampai else None,
            "jumlah_nota": total[1], "total_nominal": total[0],
            "per_kategori": [{"kategori": r[0], "jumlah": r[1], "total": r[2]} for r in per_kat],
            "per_vendor_teratas": [{"vendor": r[0], "jumlah": r[1], "total": r[2]} for r in per_vendor]}
    if args.csv:
        _tulis_csv_rekap(args.csv, data)
        data["file_csv"] = args.csv
    label_periode = ("%s - %s" % (tgl_id(dari), tgl_id(sampai))) if dari else "semua waktu"
    garis = ["REKAP NOTA (%s)" % label_periode, "Jumlah nota: %d | Total: %s" % (total[1], rp(total[0])),
             "", "Per kategori:"]
    for r in per_kat:
        garis.append("- %s: %d nota, %s" % (label_kategori(r[0]), r[1], rp(r[2])))
    if per_vendor:
        garis.append("")
        garis.append("Vendor teratas:")
        for r in per_vendor:
            garis.append("- %s: %d nota, %s" % (r[0], r[1], rp(r[2])))
    if args.csv:
        garis.append("")
        garis.append("CSV: %s" % args.csv)
    return data, "\n".join(garis)


def _tulis_csv_rekap(path, data):
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["Kategori", "Jumlah Nota", "Total Nominal"])
        for r in data["per_kategori"]:
            w.writerow([label_kategori(r["kategori"]), r["jumlah"], r["total"]])
        w.writerow([])
        w.writerow(["Total", data["jumlah_nota"], data["total_nominal"]])


def cmd_duplikat(args):
    db = path_db(args)
    conn = buka(db, baca_saja=True)
    persis = conn.execute(
        "SELECT hash_sha256, COUNT(*) n, GROUP_CONCAT(id) ids FROM nota WHERE status='aktif' "
        "GROUP BY hash_sha256 HAVING n > 1").fetchall()
    mirip = conn.execute(
        "SELECT tanggal, vendor, nominal, COUNT(*) n, GROUP_CONCAT(id) ids FROM nota WHERE status='aktif' "
        "GROUP BY tanggal, vendor, nominal HAVING n > 1").fetchall()
    persis_ids = set()
    for r in persis:
        persis_ids.update(int(x) for x in r["ids"].split(","))
    mirip_bersih = [r for r in mirip if not set(int(x) for x in r["ids"].split(",")).issubset(persis_ids)]
    conn.close()
    data = {"ok": True, "mode": "baca",
            "file_sama_persis": [{"hash_sha256": r["hash_sha256"], "id_nota": [int(x) for x in r["ids"].split(",")]}
                                  for r in persis],
            "kemungkinan_dobel": [{"tanggal": r["tanggal"], "vendor": r["vendor"], "nominal": r["nominal"],
                                   "id_nota": [int(x) for x in r["ids"].split(",")]} for r in mirip_bersih]}
    if not persis and not mirip_bersih:
        teks = "Tidak ada nota yang tampak dobel."
    else:
        garis = []
        if persis:
            garis.append("File SAMA PERSIS (isi file identik):")
            for r in persis:
                garis.append("- ID %s" % ", ".join(str(x) for x in sorted(int(i) for i in r["ids"].split(","))))
        if mirip_bersih:
            garis.append("Kemungkinan dobel (tanggal, vendor, nominal sama, file berbeda - cek manual):")
            for r in mirip_bersih:
                garis.append("- %s | %s | %s -> ID %s" %
                             (tgl_id(datetime.strptime(r["tanggal"], "%Y-%m-%d").date()), r["vendor"],
                              rp(r["nominal"]), ", ".join(str(x) for x in sorted(int(i) for i in r["ids"].split(",")))))
        teks = "\n".join(garis)
    return data, teks


def cmd_ekspor(args):
    db = path_db(args)
    conn = buka(db, baca_saja=True)
    dari, sampai, jenis_periode = ambil_periode(args)
    if not dari:
        conn.close()
        raise Gagal("Isi --bulan, --tahun, atau --dari/--sampai untuk ekspor.")
    baris = conn.execute("SELECT * FROM nota WHERE status='aktif' AND tanggal BETWEEN ? AND ? "
                         "ORDER BY tanggal, id", (dari.isoformat(), sampai.isoformat())).fetchall()
    conn.close()
    if not baris:
        return {"ok": True, "mode": "baca", "jumlah": 0}, \
            "Tidak ada nota pada %s - %s untuk diekspor." % (tgl_id(dari), tgl_id(sampai))
    if not args.csv:
        raise Gagal("Isi --csv <file> untuk menyimpan hasil ekspor.")
    with open(args.csv, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["Tanggal", "Keterangan", "Masuk", "Keluar", "Kategori"])
        for b in baris:
            ket = b["vendor"] + (" - " + b["catatan"] if b["catatan"] else "")
            kat_kas = PETA_KATEGORI_KAS_UMKM.get(b["kategori"], "lain-lain")
            w.writerow([tgl_id(datetime.strptime(b["tanggal"], "%Y-%m-%d").date()), ket, "", b["nominal"], kat_kas])
    total = sum(b["nominal"] for b in baris)
    data = {"ok": True, "mode": "baca", "jumlah": len(baris), "total_nominal": total, "file_csv": args.csv,
            "dari": dari.isoformat(), "sampai": sampai.isoformat()}
    teks = ("Diekspor %d nota (%s) ke %s, total %s.\nUntuk masuk ke buku kas, jalankan (dari folder skill "
            "kas-umkm): python3 scripts/kas.py impor \"%s\" --jenis-file buku-kas" %
            (len(baris), tgl_id(dari) + " - " + tgl_id(sampai), args.csv, rp(total), args.csv))
    return data, teks


def cmd_backup(args):
    db = path_db(args)
    if args.daftar:
        fol = folder_backup(db)
        if not fol.is_dir():
            return {"ok": True, "mode": "baca", "cadangan": []}, "Belum ada cadangan."
        arsip = sorted(fol.glob("arsip-*.db"), key=lambda p: p.stat().st_mtime, reverse=True)
        data = {"ok": True, "mode": "baca", "cadangan": [str(p) for p in arsip]}
        teks = "\n".join(str(p) for p in arsip) if arsip else "Belum ada cadangan."
        return data, teks
    if not db.is_file():
        raise Gagal("Indeks arsip belum ada di %s." % db)
    path_bk = buat_backup(db, "manual")
    return {"ok": True, "mode": "tersimpan", "backup": path_bk}, "Cadangan dibuat: %s" % path_bk


def cmd_restore(args):
    sumber = Path(args.dari).expanduser()
    if not sumber.is_file():
        raise Gagal("File cadangan '%s' tidak ditemukan." % args.dari)
    try:
        cek = sqlite3.connect(str(sumber), timeout=_timeout())
        r = cek.execute("SELECT nilai FROM meta WHERE kunci='aplikasi'").fetchone()
        cek.close()
    except sqlite3.DatabaseError:
        raise Gagal("File '%s' bukan cadangan indeks arsip-nota yang valid." % args.dari)
    if not r or r[0] != APLIKASI:
        raise Gagal("File '%s' bukan cadangan indeks arsip-nota." % args.dari)
    db = path_db(args)
    if not args.ya:
        data = {"ok": True, "mode": "pratinjau", "perlu_konfirmasi": True, "dari": str(sumber), "ke": str(db)}
        teks = ("Akan memulihkan indeks di %s dari cadangan %s. Indeks saat ini (bila ada) dicadangkan dulu, tidak "
                "dihapus. File nota (foto/PDF) di folder arsip tidak terpengaruh. Lanjutkan? Balas \"ya\", lalu "
                "jalankan ulang dengan --ya." % (db, sumber))
        return data, teks
    if db.is_file():
        buat_backup(db, "sebelum-restore")
    db.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(str(sumber), str(db))
    data = {"ok": True, "mode": "tersimpan", "dari": str(sumber), "ke": str(db)}
    return data, "Indeks dipulihkan dari %s." % sumber


# --------------------------------------------------------------------------- argparse
def buat_parser():
    p = argparse.ArgumentParser(prog="arsip.py", description="Arsip nota & faktur UMKM (indeks SQLite lokal).")
    umum = argparse.ArgumentParser(add_help=False)
    umum.add_argument("--json", action="store_true", help="Keluaran JSON (disarankan untuk agent).")
    umum.add_argument("--db", help="Lokasi file indeks (default ~/KomunitechData/arsip-nota/arsip.db).")
    sub = p.add_subparsers(dest="perintah")
    sub.required = True

    s = sub.add_parser("init", parents=[umum], help="Buat indeks arsip baru.")
    s.add_argument("--folder-arsip", help="Folder tujuan file nota (default: folder 'arsip' di sebelah indeks).")
    s.add_argument("--mulai-baru", action="store_true", help="Buat indeks kosong baru (indeks lama dipindah).")
    s.add_argument("--ya", action="store_true")
    s.set_defaults(fungsi=cmd_init)

    s = sub.add_parser("info", parents=[umum], help="Ringkasan indeks arsip.")
    s.set_defaults(fungsi=cmd_info)

    s = sub.add_parser("tambah", parents=[umum], help="Arsipkan satu file nota/faktur ke indeks.")
    s.add_argument("--file", required=True, help="Path foto/PDF nota yang akan diarsipkan.")
    s.add_argument("--tanggal", required=True, help="Tanggal nota, format DD/MM/YYYY.")
    s.add_argument("--vendor", required=True, help="Nama penjual/vendor di nota.")
    s.add_argument("--nominal", required=True, help="Nominal total nota, mis. 150000 atau 150rb.")
    s.add_argument("--kategori", help="Kategori pengeluaran (lihat references/perintah.md).")
    s.add_argument("--jenis", help="nota|struk|kuitansi|invoice|faktur|bukti-transfer (default nota).")
    s.add_argument("--catatan", default="", help="Catatan bebas.")
    s.add_argument("--folder-arsip", help="Override folder arsip untuk file ini.")
    s.add_argument("--pindah", action="store_true", help="Pindahkan file asli (default: salin, file asli tetap ada).")
    s.add_argument("--izinkan-duplikat", action="store_true",
                   help="Tetap arsipkan walau isi file sama persis dengan nota yang sudah ada.")
    s.add_argument("--ya", action="store_true")
    s.set_defaults(fungsi=cmd_tambah)

    s = sub.add_parser("cari", parents=[umum], help="Cari nota di indeks.")
    s.add_argument("--vendor")
    s.add_argument("--kategori")
    s.add_argument("--dari")
    s.add_argument("--sampai")
    s.add_argument("--nominal-min")
    s.add_argument("--nominal-max")
    s.add_argument("--cari", help="Cari kata di vendor/catatan.")
    s.set_defaults(fungsi=cmd_cari)

    s = sub.add_parser("rekap", parents=[umum], help="Rekap per kategori/vendor untuk suatu periode.")
    s.add_argument("--bulan")
    s.add_argument("--tahun")
    s.add_argument("--dari")
    s.add_argument("--sampai")
    s.add_argument("--kategori")
    s.add_argument("--csv")
    s.set_defaults(fungsi=cmd_rekap)

    s = sub.add_parser("duplikat", parents=[umum], help="Cari nota yang kemungkinan sudah diarsipkan dua kali.")
    s.set_defaults(fungsi=cmd_duplikat)

    s = sub.add_parser("ekspor", parents=[umum], help="Ekspor CSV pengeluaran (siap diimpor kas-umkm).")
    s.add_argument("--bulan")
    s.add_argument("--tahun")
    s.add_argument("--dari")
    s.add_argument("--sampai")
    s.add_argument("--csv", required=True)
    s.set_defaults(fungsi=cmd_ekspor)

    s = sub.add_parser("backup", parents=[umum], help="Cadangkan/lihat cadangan indeks.")
    s.add_argument("--daftar", action="store_true")
    s.set_defaults(fungsi=cmd_backup)

    s = sub.add_parser("restore", parents=[umum], help="Pulihkan indeks dari cadangan.")
    s.add_argument("--dari", required=True)
    s.add_argument("--ya", action="store_true")
    s.set_defaults(fungsi=cmd_restore)

    return p


def cetak(args, data, teks, kode_keluar):
    if getattr(args, "json", False):
        print(json.dumps(data, ensure_ascii=False, indent=2, default=str))
    elif kode_keluar:
        print("GAGAL: " + teks, file=sys.stderr)
    else:
        print(teks)
    return kode_keluar


def main(argv=None):
    try:
        sys.stdout.reconfigure(errors="replace")
        sys.stderr.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass
    try:
        args = buat_parser().parse_args(argv)
    except SystemExit as e:
        return e.code if e.code is not None else 2
    if not hasattr(args, "ya"):
        args.ya = False
    try:
        data, teks = args.fungsi(args)
    except Gagal as e:
        out = {"ok": False, "error": e.pesan}
        out.update(e.detail)
        return cetak(args, out, e.pesan, 1)
    except sqlite3.OperationalError as e:
        pesan = (PESAN_TERKUNCI % _detik()) if _terkunci(e) else \
            "Kesalahan indeks: %s. Jangan hapus file indeks; ulangi, atau pulihkan dari cadangan." % e
        return cetak(args, {"ok": False, "error": pesan}, pesan, 1)
    except sqlite3.DatabaseError as e:
        pesan = "Indeks arsip rusak (%s). Jangan hapus file itu. %s" % (e, SARAN_PULIH)
        return cetak(args, {"ok": False, "error": pesan, "rusak": True}, pesan, 1)
    except OSError as e:
        pesan = "File tidak bisa ditulis/dibaca (%s). Periksa folder dan izin aksesnya." % e
        return cetak(args, {"ok": False, "error": pesan}, pesan, 1)
    return cetak(args, data, teks, 0)


if __name__ == "__main__":
    sys.exit(main())
