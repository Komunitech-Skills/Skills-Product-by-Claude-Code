#!/usr/bin/env python3
"""buku-stok (Komunitech) - buku stok/inventori lokal untuk toko & seller marketplace.

Satu file database SQLite di komputer pengguna. Hanya library standar Python 3.8+.
Tidak ada akses jaringan. Semua perintah tulis berjalan sebagai PRATINJAU (tidak menyimpan)
sampai diberi flag --ya setelah pengguna menyetujui ringkasannya.

Lokasi database (urutan prioritas):
  1. --db PATH
  2. ENV KOMUNITECH_STOK_DB  (path file lengkap)
  3. ENV KOMUNITECH_DATA     (folder) + /stok.db
  4. ~/KomunitechData/stok.db

Contoh:
  python3 stok.py init --ya
  python3 stok.py produk tambah --sku KAOS-HT-M --nama "Kaos Polos" --varian "Hitam M" \
      --harga-beli 35000 --harga-jual 59000 --stok-min 10 --lokasi A1 --stok-awal 24 --ya
  python3 stok.py masuk --sku KAOS-HT-M --qty 50 --harga "Rp 34.000" --ya
  python3 stok.py impor-pesanan pesanan-shopee.csv          (pratinjau + pemetaan kolom)
  python3 stok.py picking
  python3 stok.py laporan ringkas --json
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
from datetime import date, datetime, timedelta
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

VERSI = "1.1.1"
SKEMA = 1
APLIKASI = "buku-stok"
EPS = 1e-9

# ---------------------------------------------------------------------------
# Error & util umum
# ---------------------------------------------------------------------------


class Gagal(Exception):
    """Error yang pesannya aman ditampilkan ke pengguna."""

    def __init__(self, pesan, **detail):
        super().__init__(pesan)
        self.pesan = pesan
        self.detail = detail


def sekarang():
    return datetime.now().replace(microsecond=0).isoformat(sep=" ")


def bulat_rp(x):
    """Pembulatan rupiah: ke rupiah terdekat, setengah ke atas (0,5 -> 1)."""
    if x is None:
        return None
    return int(Decimal(repr(float(x))).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def rp(x):
    if x is None:
        return "-"
    n = bulat_rp(x)
    s = "{:,}".format(abs(n)).replace(",", ".")
    return ("-Rp " if n < 0 else "Rp ") + s


def rapikan_qty(q):
    return round(float(q) + 0.0, 3)


def fq(q):
    """Format qty: 12 / 1,5 / -3 (desimal pakai koma)."""
    if q is None:
        return "-"
    q = rapikan_qty(q)
    if abs(q - round(q)) < 1e-9:
        return str(int(round(q)))
    return ("%.3f" % q).rstrip("0").rstrip(".").replace(".", ",")


def angka_json(q):
    q = rapikan_qty(q)
    return int(round(q)) if abs(q - round(q)) < 1e-9 else q


def _grup_ribuan_valid(bagian_bulat, pemisah):
    grup = bagian_bulat.split(pemisah)
    return 1 <= len(grup[0]) <= 3 and all(len(g) == 3 for g in grup[1:])


def parse_angka(teks):
    """Angka format Indonesia/Inggris -> float, atau None bila kosong/tidak valid/meragukan.

    Diterima: '15000', 'Rp 15.000', 'Rp. 25000', 'IDR 25.000', 'Rp 15.000,-', '15.000,50',
    '15,000.50', '1.250.000', '12,5', '2 pcs'. Ditolak (None): '15.000.00', '15000.500', '1.5E+06'.
    """
    if teks is None:
        return None
    if isinstance(teks, (int, float)):
        return float(teks)
    s = str(teks).strip().lower()
    if not s:
        return None
    if re.fullmatch(r"\(.*\)", s):
        s = "-" + s[1:-1].strip()
    if re.search(r"\d\s*e\s*[+-]?\s*\d", s):
        return None
    s = re.sub(r"\b(rp|idr)\b\.?", "", s)
    s = re.sub(r"[,.]\s*-\s*$", "", s)
    s = re.sub(r"[^\d,.\-]", "", s).strip(".,")
    if not s or s == "-":
        return None
    negatif = s.startswith("-")
    s = s.lstrip("-")
    if "-" in s:
        return None
    digit = sum(c.isdigit() for c in s)
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
        nilai = float(s)
    except ValueError:
        return None
    if digit >= 4 and 0 < nilai < 1:
        return None
    return -nilai if negatif else nilai


def angka_wajib(teks, nama, boleh_nol=True, boleh_negatif=False):
    n = parse_angka(teks)
    if n is None:
        raise Gagal("Angka '%s' untuk %s tidak bisa dibaca. Contoh format benar: 15000, Rp 15.000, 15.000,50."
                    % (teks, nama))
    if n < 0 and not boleh_negatif:
        raise Gagal("%s tidak boleh negatif (%s)." % (nama, teks))
    if n == 0 and not boleh_nol:
        raise Gagal("%s harus lebih dari 0." % nama)
    return n


BULAN = {
    "jan": 1, "januari": 1, "january": 1, "feb": 2, "februari": 2, "february": 2, "peb": 2,
    "mar": 3, "maret": 3, "march": 3, "apr": 4, "april": 4, "mei": 5, "may": 5,
    "jun": 6, "juni": 6, "june": 6, "jul": 7, "juli": 7, "july": 7,
    "agu": 8, "agt": 8, "agus": 8, "agustus": 8, "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9, "okt": 10, "oktober": 10, "oct": 10, "october": 10,
    "nov": 11, "nop": 11, "november": 11, "des": 12, "desember": 12, "dec": 12, "december": 12,
}
POLA_ISO = re.compile(r"^(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})(?:[ T].*)?$")
POLA_DMY = re.compile(r"^(\d{1,2})[-/.](\d{1,2})[-/.](\d{4}|\d{2})(?:[ T].*)?$")
POLA_NAMA_BULAN = re.compile(r"^(\d{1,2})[\s\-/]+([A-Za-z]+)\.?[\s\-/,]+(\d{2}|\d{4})(?:[ T].*)?$")


def parse_tanggal(teks):
    """Tanggal -> date atau None. Angka hari/bulan/tahun dibaca gaya Indonesia (hari dulu)."""
    t = (str(teks) if teks is not None else "").strip()
    if not t:
        return None
    try:
        if re.fullmatch(r"\d{5}(\.\d+)?", t):   # nomor seri tanggal Excel
            n = float(t)
            if 20000 < n < 80000:
                return date(1899, 12, 30) + timedelta(days=int(n))
        m = POLA_ISO.match(t)
        if m:
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        m = POLA_DMY.match(t)
        if m:
            y = int(m.group(3))
            y = y + 2000 if y < 100 else y
            return date(y, int(m.group(2)), int(m.group(1)))
        m = POLA_NAMA_BULAN.match(t)
        if m and m.group(2).lower() in BULAN:
            y = int(m.group(3))
            y = y + 2000 if y < 100 else y
            return date(y, BULAN[m.group(2).lower()], int(m.group(1)))
    except ValueError:
        return None
    return None


def tanggal_wajib(teks, nama="tanggal"):
    d = parse_tanggal(teks)
    if d is None:
        raise Gagal("%s '%s' tidak dikenali. Pakai format 2026-09-23 atau 23/09/2026." % (nama.capitalize(), teks))
    return d


def hari_ini(args):
    h = getattr(args, "hari_ini", None)
    return tanggal_wajib(h, "hari-ini") if h else date.today()


def norm(s):
    return re.sub(r"\s+", " ", str(s or "").replace("\ufeff", "")).strip().lower()


# ---------------------------------------------------------------------------
# Membaca file tabel (CSV / XLSX sederhana)
# ---------------------------------------------------------------------------

BATAS_UKURAN = 200 * 1024 * 1024


def _baca_xlsx(path):
    """Membaca sheet pertama file .xlsx dengan zipfile + XML (tanpa library luar)."""
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
          "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
          "pr": "http://schemas.openxmlformats.org/package/2006/relationships"}
    try:
        z = zipfile.ZipFile(path)
    except zipfile.BadZipFile:
        raise Gagal("File .xlsx rusak atau bukan file Excel asli. Buka di Excel lalu simpan ulang sebagai CSV.")
    with z:
        nama_file = set(z.namelist())
        for info in z.infolist():
            if info.file_size > BATAS_UKURAN:
                raise Gagal("Isi file Excel terlalu besar untuk dibaca (> 200 MB).")
        shared = []
        if "xl/sharedStrings.xml" in nama_file:
            akar = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in akar.findall("m:si", ns):
                shared.append("".join(t.text or "" for t in si.iter("{%s}t" % ns["m"])))
        sheet = "xl/worksheets/sheet1.xml"
        try:
            wb = ET.fromstring(z.read("xl/workbook.xml"))
            pertama = wb.find("m:sheets/m:sheet", ns)
            rid = pertama.get("{%s}id" % ns["r"]) if pertama is not None else None
            rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
            for rel in rels.findall("pr:Relationship", ns):
                if rel.get("Id") == rid:
                    target = rel.get("Target").lstrip("/")
                    sheet = target if target.startswith("xl/") else "xl/" + target
        except (KeyError, ET.ParseError, AttributeError):
            pass
        if sheet not in nama_file:
            raise Gagal("Sheet pertama tidak ditemukan di file Excel. Simpan ulang sebagai CSV.")
        akar = ET.fromstring(z.read(sheet))
    baris_semua = []
    for row in akar.iter("{%s}row" % ns["m"]):
        isi = {}
        for c in row.findall("m:c", ns):
            ref = c.get("r") or ""
            huruf = re.match(r"[A-Z]+", ref)
            if huruf:
                kol = 0
                for ch in huruf.group(0):
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
        if isi:
            lebar = max(isi) + 1
            baris_semua.append([isi.get(i, "") for i in range(lebar)])
        else:
            baris_semua.append([])
    return baris_semua, "xlsx"


def baca_tabel(path):
    """Kembalikan (daftar baris [list str], info). Mendukung CSV (, ; tab |) dan XLSX sederhana."""
    p = Path(path).expanduser()
    if not p.is_file():
        raise Gagal("File '%s' tidak ditemukan." % path)
    if p.stat().st_size > BATAS_UKURAN:
        raise Gagal("File terlalu besar (> 200 MB).")
    if p.stat().st_size == 0:
        raise Gagal("File '%s' kosong." % p.name)
    if p.suffix.lower() in (".xlsx", ".xlsm"):
        return _baca_xlsx(p)
    if p.suffix.lower() == ".xls":
        raise Gagal("Format .xls (Excel lama) tidak didukung. Buka di Excel, lalu File > Save As > CSV atau .xlsx.")
    mentah = p.read_bytes()
    if mentah[:2] == b"PK":
        return _baca_xlsx(p)
    if b"\x00" in mentah[:4096]:
        raise Gagal("File '%s' tampaknya bukan file teks/CSV (berisi data biner). Simpan ulang sebagai CSV." % p.name)
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
        baris = [list(r) for r in csv.reader(io.StringIO(teks, newline=""), dialect=dialek)]
    except csv.Error as e:
        raise Gagal("CSV rusak dan tidak bisa dibaca (%s). Buka di Excel lalu simpan ulang sebagai CSV." % e)
    return baris, "csv"


def cari_header(baris, sinonim, minimal=2, maks_scan=15):
    """Cari baris judul kolom: baris (dari 15 pertama) dengan paling banyak kolom dikenali."""
    terbaik, skor_terbaik = None, 0
    for i, r in enumerate(baris[:maks_scan]):
        skor = len(deteksi_kolom([c for c in r], sinonim))
        if skor > skor_terbaik:
            terbaik, skor_terbaik = i, skor
    if terbaik is None or skor_terbaik < minimal:
        return None
    return terbaik


KECUALI = {
    # kolom harga "asli/awal/original" = harga SEBELUM diskon -> jangan dipakai sebagai harga jual
    "harga": ["asli", "awal", "original", "sebelum diskon", "coret"],
    "harga_total": ["asli", "awal", "original", "sebelum diskon"],
}


def deteksi_kolom(header, sinonim):
    """header: list nama kolom. sinonim: {field: [kata...]} (urutan = prioritas).

    Cocok persis selalu menang atas cocok sebagian; cocok sebagian hanya untuk kata >= 8 huruf.
    Satu kolom hanya dipakai untuk satu field (field diproses sesuai urutan dict).
    """
    hn = [norm(h) for h in header]
    dipakai, hasil = set(), {}
    for field, kata in sinonim.items():
        pilih = None
        larang = KECUALI.get(field, []) if sinonim is SINONIM_PESANAN else []
        boleh = lambda h: h and not any(x in h for x in larang)
        for k in kata:
            for i, h in enumerate(hn):
                if i not in dipakai and boleh(h) and h == k:
                    pilih = i
                    break
            if pilih is not None:
                break
        if pilih is None:
            for k in kata:
                if len(k) < 8:
                    continue
                for i, h in enumerate(hn):
                    if i not in dipakai and boleh(h) and k in h:
                        pilih = i
                        break
                if pilih is not None:
                    break
        if pilih is not None:
            hasil[field] = pilih
            dipakai.add(pilih)
    return hasil


def sel(r, idx):
    if idx is None or idx >= len(r):
        return ""
    return (r[idx] or "").strip()


# ---------------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------------

DDL = """
CREATE TABLE IF NOT EXISTS meta (kunci TEXT PRIMARY KEY, nilai TEXT);
CREATE TABLE IF NOT EXISTS produk (
  id INTEGER PRIMARY KEY,
  sku TEXT NOT NULL UNIQUE COLLATE NOCASE,
  nama TEXT NOT NULL,
  varian TEXT NOT NULL DEFAULT '',
  satuan TEXT NOT NULL DEFAULT 'pcs',
  harga_beli REAL NOT NULL DEFAULT 0,
  harga_jual REAL NOT NULL DEFAULT 0,
  hpp REAL NOT NULL DEFAULT 0,
  stok REAL NOT NULL DEFAULT 0,
  stok_min REAL NOT NULL DEFAULT 0,
  lokasi TEXT NOT NULL DEFAULT '',
  aktif INTEGER NOT NULL DEFAULT 1,
  dibuat TEXT, diubah TEXT
);
CREATE TABLE IF NOT EXISTS mutasi (
  id INTEGER PRIMARY KEY,
  waktu TEXT NOT NULL,
  tanggal TEXT NOT NULL,
  produk_id INTEGER NOT NULL REFERENCES produk(id),
  arah TEXT NOT NULL CHECK (arah IN ('masuk','keluar','opname')),
  jenis TEXT NOT NULL,
  qty REAL NOT NULL,
  harga REAL,
  hpp REAL NOT NULL,
  stok_sesudah REAL NOT NULL,
  ref TEXT NOT NULL DEFAULT '',
  catatan TEXT NOT NULL DEFAULT '',
  impor_id INTEGER,
  dibatalkan INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS ix_mutasi_produk ON mutasi(produk_id, tanggal);
CREATE INDEX IF NOT EXISTS ix_mutasi_tanggal ON mutasi(tanggal);
CREATE TABLE IF NOT EXISTS impor (
  id INTEGER PRIMARY KEY, waktu TEXT, file TEXT, platform TEXT, baris INTEGER,
  pesanan_baru INTEGER, pemetaan TEXT
);
CREATE TABLE IF NOT EXISTS pesanan (
  id INTEGER PRIMARY KEY,
  no_pesanan TEXT NOT NULL UNIQUE,
  platform TEXT NOT NULL DEFAULT '',
  tanggal TEXT, status TEXT NOT NULL DEFAULT '', kategori TEXT NOT NULL DEFAULT '',
  resi TEXT NOT NULL DEFAULT '', kurir TEXT NOT NULL DEFAULT '', batas_kirim TEXT NOT NULL DEFAULT '',
  dikemas INTEGER NOT NULL DEFAULT 0, dibatalkan INTEGER NOT NULL DEFAULT 0,
  impor_id INTEGER, diubah TEXT
);
CREATE TABLE IF NOT EXISTS pesanan_item (
  id INTEGER PRIMARY KEY,
  pesanan_id INTEGER NOT NULL REFERENCES pesanan(id),
  produk_id INTEGER REFERENCES produk(id),
  sku_mp TEXT NOT NULL DEFAULT '', nama_mp TEXT NOT NULL DEFAULT '',
  qty REAL NOT NULL, harga REAL, mutasi_id INTEGER
);
CREATE INDEX IF NOT EXISTS ix_item_pesanan ON pesanan_item(pesanan_id);
CREATE TABLE IF NOT EXISTS log (id INTEGER PRIMARY KEY, waktu TEXT, perintah TEXT, ringkasan TEXT);
"""


def path_db(args):
    if getattr(args, "db", None):
        return Path(args.db).expanduser()
    env = os.environ.get("KOMUNITECH_STOK_DB")
    if env:
        return Path(env).expanduser()
    folder = os.environ.get("KOMUNITECH_DATA")
    if folder:
        return Path(folder).expanduser() / "stok.db"
    return Path.home() / "KomunitechData" / "stok.db"


def folder_backup(db):
    return db.parent / "backup-stok"


def buka(db, harus_ada=True):
    if harus_ada and not db.is_file():
        raise Gagal("Database stok belum ada di %s. Jalankan dulu: stok.py init (lalu --ya)." % db,
                    db=str(db))
    conn = sqlite3.connect(str(db), isolation_level=None)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    if harus_ada:
        try:
            r = conn.execute("SELECT nilai FROM meta WHERE kunci='aplikasi'").fetchone()
        except sqlite3.DatabaseError:
            conn.close()
            raise Gagal("File %s bukan database buku-stok (atau rusak)." % db)
        if not r or r[0] != APLIKASI:
            conn.close()
            raise Gagal("File %s bukan database buku-stok." % db)
        migrasi(conn)
    return conn


def migrasi(conn):
    """Perbarui struktur database versi lama (aman diulang, tidak mengubah angka stok)."""
    kolom = [r[1] for r in conn.execute("PRAGMA table_info(mutasi)")]
    if "dibatalkan" not in kolom:
        conn.execute("BEGIN IMMEDIATE")
        conn.execute("ALTER TABLE mutasi ADD COLUMN dibatalkan INTEGER NOT NULL DEFAULT 0")
        # Penjualan marketplace milik pesanan yang sudah batal tidak dihitung sebagai penjualan.
        conn.execute("UPDATE mutasi SET dibatalkan=1 WHERE id IN (SELECT i.mutasi_id FROM pesanan_item i "
                     "JOIN pesanan s ON s.id=i.pesanan_id WHERE s.dibatalkan=1 AND i.mutasi_id IS NOT NULL)")
        conn.execute("COMMIT")


def buat_backup(db, label):
    """Salin database (aman, lewat sqlite backup API) ke backup-stok/stok-YYYYmmdd-HHMMSS-label.db."""
    if not db.is_file():
        return None
    fol = folder_backup(db)
    fol.mkdir(parents=True, exist_ok=True)
    cap = datetime.now().strftime("%Y%m%d-%H%M%S")
    label = re.sub(r"[^a-z0-9-]+", "-", label.lower()).strip("-") or "manual"
    tujuan = fol / ("stok-%s-%s.db" % (cap, label))
    n = 2
    while tujuan.exists():
        tujuan = fol / ("stok-%s-%s-%d.db" % (cap, label, n))
        n += 1
    src = sqlite3.connect(str(db))
    dst = sqlite3.connect(str(tujuan))
    try:
        src.backup(dst)
    finally:
        dst.close()
        src.close()
    return tujuan


def jalankan_tulis(args, db, perintah, kerja, label_backup=None, conn=None):
    """Jalankan `kerja(conn)` dalam transaksi. Tanpa --ya -> rollback (pratinjau)."""
    tutup = conn is None
    if conn is None:
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
                    backup.unlink()  # operasi gagal -> backup tidak diperlukan
                except OSError:
                    pass
            raise
        if args.ya:
            conn.execute("INSERT INTO log(waktu, perintah, ringkasan) VALUES (?,?,?)",
                         (sekarang(), perintah, json.dumps(data.get("ringkasan", {}), ensure_ascii=False)[:4000]))
            conn.execute("COMMIT")
        else:
            conn.execute("ROLLBACK")
    finally:
        if tutup:
            conn.close()
    data = dict(data)
    data["perintah"] = perintah
    data["db"] = str(db)
    if args.ya:
        data["mode"] = "tersimpan"
        if backup:
            data["backup"] = str(backup)
        kepala = "TERSIMPAN." + (" Backup sebelum perubahan: %s" % backup if backup else "")
    else:
        data["mode"] = "pratinjau"
        data["perlu_konfirmasi"] = True
        data["petunjuk"] = ("BELUM DISIMPAN. Tunjukkan ringkasan ini ke pengguna; jika pengguna setuju, "
                            "jalankan ulang perintah yang sama dengan tambahan --ya.")
        kepala = "PRATINJAU (belum disimpan). Jika sudah benar, jalankan ulang perintah yang sama dengan --ya."
    return data, kepala + "\n\n" + teks


def ambil_produk(conn, sku, wajib=True):
    r = conn.execute("SELECT * FROM produk WHERE sku=?", (sku.strip(),)).fetchone()
    if r is None and wajib:
        mirip = conn.execute("SELECT sku, nama, varian FROM produk WHERE sku LIKE ? OR nama LIKE ? LIMIT 5",
                             ("%" + sku.strip() + "%", "%" + sku.strip() + "%")).fetchall()
        saran = ", ".join("%s (%s %s)" % (m["sku"], m["nama"], m["varian"]) for m in mirip)
        raise Gagal("SKU '%s' belum terdaftar.%s Tambahkan dulu dengan: produk tambah --sku %s --nama ..."
                    % (sku, (" Mungkin maksudnya: " + saran + ".") if saran else "", sku),
                    sku=sku, saran=[m["sku"] for m in mirip])
    return r


def catat_mutasi(conn, p, arah, jenis, qty, harga, tanggal, ref="", catatan="", impor_id=None,
                 izinkan_minus=False):
    """Tambah satu mutasi & perbarui stok + HPP rata-rata tertimbang (moving average).

    qty bertanda: + masuk, - keluar. Untuk masuk, `harga` = harga beli per satuan (sudah termasuk
    bagian biaya tambahan). HPP baru = (stok_lama x HPP_lama + qty x harga) / (stok_lama + qty).
    Bila stok lama <= 0, HPP baru = harga masuk. Keluar tidak mengubah HPP.
    """
    p = conn.execute("SELECT * FROM produk WHERE id=?", (p["id"],)).fetchone()
    stok_lama, hpp_lama = float(p["stok"]), float(p["hpp"])
    qty = rapikan_qty(qty)
    if abs(qty) < EPS:
        raise Gagal("Jumlah untuk %s tidak boleh 0." % p["sku"])
    stok_baru = rapikan_qty(stok_lama + qty)
    if qty > 0:
        h = float(harga) if harga is not None else (hpp_lama if hpp_lama > 0 else float(p["harga_beli"]))
        if stok_lama <= EPS:
            hpp_baru = h
        else:
            hpp_baru = (stok_lama * hpp_lama + qty * h) / (stok_lama + qty)
        hpp_baru = round(hpp_baru, 4)
        hpp_catat = hpp_baru
        harga_catat = h
    else:
        if stok_baru < -EPS and not izinkan_minus:
            raise Gagal("Stok %s (%s %s) tidak cukup: tersedia %s, diminta keluar %s. Transaksi ditolak. "
                        "Cek stok fisik (opname) atau pakai --izinkan-minus bila memang sudah terjual."
                        % (p["sku"], p["nama"], p["varian"], fq(stok_lama), fq(-qty)),
                        sku=p["sku"], stok=angka_json(stok_lama), diminta=angka_json(-qty))
        hpp_baru = hpp_lama
        hpp_catat = hpp_lama
        harga_catat = float(harga) if harga is not None else None
    w = sekarang()
    conn.execute("UPDATE produk SET stok=?, hpp=?, diubah=? WHERE id=?", (stok_baru, hpp_baru, w, p["id"]))
    cur = conn.execute(
        "INSERT INTO mutasi(waktu,tanggal,produk_id,arah,jenis,qty,harga,hpp,stok_sesudah,ref,catatan,impor_id)"
        " VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
        (w, tanggal.isoformat(), p["id"], arah, jenis, qty, harga_catat, hpp_catat, stok_baru,
         ref or "", catatan or "", impor_id))
    return {"mutasi_id": cur.lastrowid, "sku": p["sku"], "nama": p["nama"], "varian": p["varian"],
            "qty": angka_json(qty), "stok_sebelum": angka_json(stok_lama), "stok_sesudah": angka_json(stok_baru),
            "hpp_sebelum": round(hpp_lama, 2), "hpp_sesudah": round(hpp_baru, 2),
            "harga": harga_catat, "minus": stok_baru < -EPS}


def label_produk(r):
    v = (r["varian"] or "").strip()
    return "%s%s" % (r["nama"], (" - " + v) if v else "")


def baris_produk_json(r):
    return {"sku": r["sku"], "nama": r["nama"], "varian": r["varian"], "satuan": r["satuan"],
            "lokasi": r["lokasi"], "stok": angka_json(r["stok"]), "stok_min": angka_json(r["stok_min"]),
            "harga_beli": bulat_rp(r["harga_beli"]), "harga_jual": bulat_rp(r["harga_jual"]),
            "hpp_rata2": round(float(r["hpp"]), 2), "nilai_persediaan": bulat_rp(max(r["stok"], 0) * r["hpp"]),
            "aktif": bool(r["aktif"])}


def tulis_csv(path, header, rows, pemisah=";"):
    p = Path(path).expanduser()
    if p.parent and not p.parent.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=pemisah)
        w.writerow(header)
        for r in rows:
            out = []
            for v in r:
                if isinstance(v, float) and pemisah == ";":
                    v = fq(v)
                out.append(v)
            w.writerow(out)
    return str(p)


# ---------------------------------------------------------------------------
# Perintah: init, info, backup, restore
# ---------------------------------------------------------------------------


def cmd_init(args):
    db = path_db(args)
    if db.is_file():
        conn = buka(db)
        n = conn.execute("SELECT COUNT(*) FROM produk").fetchone()[0]
        conn.close()
        return ({"ok": True, "mode": "baca", "db": str(db), "sudah_ada": True, "jumlah_produk": n},
                "Database stok sudah ada di %s (%d produk). Tidak ada yang diubah." % (db, n))
    info = {"ok": True, "db": str(db), "folder_backup": str(folder_backup(db)),
            "ringkasan": {"buat_database": str(db)}}
    teks = ("Akan dibuat database stok baru:\n  %s\nBackup otomatis disimpan di:\n  %s"
            % (db, folder_backup(db)))
    if not args.ya:
        info.update(mode="pratinjau", perlu_konfirmasi=True, perintah="init",
                    petunjuk="BELUM DIBUAT. Konfirmasi lokasi ke pengguna, lalu jalankan ulang dengan --ya.")
        return info, "PRATINJAU. " + teks + "\nJalankan ulang dengan --ya untuk membuat."
    db.parent.mkdir(parents=True, exist_ok=True)
    conn = buka(db, harus_ada=False)
    conn.executescript(DDL)
    conn.execute("INSERT OR REPLACE INTO meta VALUES ('aplikasi', ?)", (APLIKASI,))
    conn.execute("INSERT OR REPLACE INTO meta VALUES ('skema', ?)", (str(SKEMA),))
    conn.execute("INSERT OR REPLACE INTO meta VALUES ('dibuat', ?)", (sekarang(),))
    conn.close()
    info.update(mode="tersimpan", perintah="init")
    return info, "TERSIMPAN. Database stok dibuat di %s" % db


def cmd_info(args):
    db = path_db(args)
    conn = buka(db)
    q = lambda s: conn.execute(s).fetchone()[0]
    fol = folder_backup(db)
    backups = sorted(fol.glob("stok-*.db")) if fol.is_dir() else []
    data = {"ok": True, "mode": "baca", "db": str(db), "ukuran_kb": round(db.stat().st_size / 1024, 1),
            "versi_alat": VERSI, "produk_aktif": q("SELECT COUNT(*) FROM produk WHERE aktif=1"),
            "mutasi": q("SELECT COUNT(*) FROM mutasi"), "pesanan": q("SELECT COUNT(*) FROM pesanan"),
            "mutasi_terakhir": q("SELECT MAX(waktu) FROM mutasi"),
            "jumlah_backup": len(backups), "backup_terakhir": str(backups[-1]) if backups else None,
            "folder_backup": str(fol)}
    conn.close()
    teks = "\n".join("%s: %s" % (k, v) for k, v in data.items() if k not in ("ok", "mode"))
    return data, teks


def cmd_backup(args):
    db = path_db(args)
    buka(db).close()
    fol = folder_backup(db)
    if args.daftar:
        daftar = sorted(fol.glob("stok-*.db")) if fol.is_dir() else []
        data = {"ok": True, "mode": "baca", "folder": str(fol),
                "backup": [{"file": str(f), "ukuran_kb": round(f.stat().st_size / 1024, 1)} for f in daftar]}
        teks = "Backup di %s:\n" % fol + ("\n".join("  %s" % f.name for f in daftar) or "  (belum ada)")
        return data, teks
    # Membuat salinan tidak mengubah data, jadi tidak perlu --ya.
    tujuan = buat_backup(db, args.label or "manual")
    return ({"ok": True, "mode": "tersimpan", "perintah": "backup", "backup": str(tujuan)},
            "Backup dibuat: %s" % tujuan)


def _ringkas_db(path):
    c = sqlite3.connect(str(path))
    try:
        c.row_factory = sqlite3.Row
        cek = c.execute("PRAGMA integrity_check").fetchone()[0]
        app = c.execute("SELECT nilai FROM meta WHERE kunci='aplikasi'").fetchone()
        if not app or app[0] != APLIKASI:
            raise Gagal("File %s bukan backup buku-stok." % path)
        return {"integritas": cek, "produk": c.execute("SELECT COUNT(*) FROM produk").fetchone()[0],
                "mutasi": c.execute("SELECT COUNT(*) FROM mutasi").fetchone()[0],
                "mutasi_terakhir": c.execute("SELECT MAX(waktu) FROM mutasi").fetchone()[0]}
    except sqlite3.DatabaseError:
        raise Gagal("File %s rusak atau bukan database SQLite." % path)
    finally:
        c.close()


def cmd_restore(args):
    db = path_db(args)
    sumber = Path(args.dari).expanduser()
    if not sumber.is_file():
        raise Gagal("File backup '%s' tidak ditemukan. Lihat daftar: backup --daftar" % args.dari)
    if sumber.resolve() == db.resolve():
        raise Gagal("File backup sama dengan database aktif.")
    info_sumber = _ringkas_db(sumber)
    if info_sumber["integritas"] != "ok":
        raise Gagal("File backup gagal cek integritas (%s). Pilih backup lain." % info_sumber["integritas"])
    info_skrg = _ringkas_db(db) if db.is_file() else None
    data = {"ok": True, "perintah": "restore", "db": str(db), "dari": str(sumber),
            "isi_backup": info_sumber, "isi_sekarang": info_skrg,
            "ringkasan": {"restore_dari": str(sumber)}}
    teks = ("Database aktif akan DIGANTI dengan isi backup:\n  %s\n"
            "Isi backup   : %s produk, %s mutasi (terakhir %s)\n"
            "Isi sekarang : %s produk, %s mutasi (terakhir %s)\n"
            "Transaksi setelah tanggal backup akan hilang dari database aktif "
            "(tetap tersimpan di backup 'sebelum-restore')."
            % (sumber, info_sumber["produk"], info_sumber["mutasi"], info_sumber["mutasi_terakhir"],
               (info_skrg or {}).get("produk"), (info_skrg or {}).get("mutasi"),
               (info_skrg or {}).get("mutasi_terakhir")))
    if not args.ya:
        data.update(mode="pratinjau", perlu_konfirmasi=True,
                    petunjuk="BELUM DIPULIHKAN. Minta persetujuan pengguna lalu jalankan ulang dengan --ya.")
        return data, "PRATINJAU. " + teks
    cadangan = buat_backup(db, "sebelum-restore") if db.is_file() else None
    db.parent.mkdir(parents=True, exist_ok=True)
    src = sqlite3.connect(str(sumber))
    dst = sqlite3.connect(str(db))
    try:
        src.backup(dst)
    finally:
        src.close()
        dst.close()
    data.update(mode="tersimpan", backup=str(cadangan) if cadangan else None)
    return data, "TERSIMPAN. Database dipulihkan dari %s.\nBackup kondisi sebelum restore: %s" % (sumber, cadangan)


# ---------------------------------------------------------------------------
# Perintah: produk
# ---------------------------------------------------------------------------


def _nilai_opsional(v, nama):
    return None if v is None else angka_wajib(v, nama)


def cmd_produk_tambah(args):
    db = path_db(args)
    sku = (args.sku or "").strip()
    if not sku or re.search(r"\s{2,}|[\t\n]", sku):
        raise Gagal("SKU wajib diisi dan tidak boleh berisi tab/enter.")
    hb = _nilai_opsional(args.harga_beli, "harga beli") or 0
    hj = _nilai_opsional(args.harga_jual, "harga jual") or 0
    smin = _nilai_opsional(args.stok_min, "stok minimum") or 0
    awal = _nilai_opsional(args.stok_awal, "stok awal") or 0
    tgl = tanggal_wajib(args.tanggal) if args.tanggal else hari_ini(args)

    def kerja(conn):
        if conn.execute("SELECT 1 FROM produk WHERE sku=?", (sku,)).fetchone():
            raise Gagal("SKU '%s' sudah ada. Pakai 'produk ubah' untuk mengubahnya." % sku)
        w = sekarang()
        cur = conn.execute(
            "INSERT INTO produk(sku,nama,varian,satuan,harga_beli,harga_jual,hpp,stok,stok_min,lokasi,dibuat,diubah)"
            " VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (sku, args.nama.strip(), (args.varian or "").strip(), (args.satuan or "pcs").strip(), hb, hj, hb, 0,
             smin, (args.lokasi or "").strip(), w, w))
        p = conn.execute("SELECT * FROM produk WHERE id=?", (cur.lastrowid,)).fetchone()
        m = None
        if awal > 0:
            m = catat_mutasi(conn, p, "masuk", "saldo-awal", awal, hb, tgl, catatan="stok awal")
        p = conn.execute("SELECT * FROM produk WHERE id=?", (cur.lastrowid,)).fetchone()
        d = baris_produk_json(p)
        teks = ("Produk baru: %s | %s | satuan %s | lokasi %s\nHarga beli %s, harga jual %s, stok minimum %s\n"
                "Stok awal: %s (nilai %s)"
                % (sku, label_produk(p), p["satuan"], p["lokasi"] or "-", rp(hb), rp(hj), fq(smin), fq(awal),
                   rp(awal * hb)))
        if hj and hb and hj < hb:
            teks += "\nPERINGATAN: harga jual lebih rendah dari harga beli."
        return {"ok": True, "produk": d, "mutasi_awal": m, "ringkasan": {"tambah_produk": sku, "stok_awal": awal}}, teks

    return jalankan_tulis(args, db, "produk tambah", kerja)


def cmd_produk_ubah(args):
    db = path_db(args)

    def kerja(conn):
        p = ambil_produk(conn, args.sku)
        ubah = {}
        if args.nama is not None:
            ubah["nama"] = args.nama.strip()
        if args.varian is not None:
            ubah["varian"] = args.varian.strip()
        if args.satuan is not None:
            ubah["satuan"] = args.satuan.strip()
        if args.lokasi is not None:
            ubah["lokasi"] = args.lokasi.strip()
        if args.harga_beli is not None:
            ubah["harga_beli"] = angka_wajib(args.harga_beli, "harga beli")
        if args.harga_jual is not None:
            ubah["harga_jual"] = angka_wajib(args.harga_jual, "harga jual")
        if args.stok_min is not None:
            ubah["stok_min"] = angka_wajib(args.stok_min, "stok minimum")
        if args.koreksi_hpp is not None:
            ubah["hpp"] = angka_wajib(args.koreksi_hpp, "koreksi HPP")
        if args.sku_baru:
            if conn.execute("SELECT 1 FROM produk WHERE sku=? AND id<>?", (args.sku_baru.strip(), p["id"])).fetchone():
                raise Gagal("SKU baru '%s' sudah dipakai produk lain." % args.sku_baru)
            ubah["sku"] = args.sku_baru.strip()
        if args.nonaktif:
            ubah["aktif"] = 0
        if args.aktif:
            ubah["aktif"] = 1
        if not ubah:
            raise Gagal("Tidak ada yang diubah. Sebutkan field, mis. --harga-jual 65000.")
        perubahan = {k: {"lama": p[k], "baru": v} for k, v in ubah.items() if p[k] != v}
        sets = ", ".join("%s=?" % k for k in ubah) + ", diubah=?"
        conn.execute("UPDATE produk SET %s WHERE id=?" % sets, list(ubah.values()) + [sekarang(), p["id"]])
        baru = conn.execute("SELECT * FROM produk WHERE id=?", (p["id"],)).fetchone()
        teks = "Ubah produk %s (%s):\n" % (p["sku"], label_produk(p)) + "\n".join(
            "  %s: %s -> %s" % (k, v["lama"], v["baru"]) for k, v in perubahan.items())
        if "hpp" in ubah:
            teks += "\nCatatan: koreksi HPP mengubah nilai persediaan dan tercatat di log."
        return {"ok": True, "produk": baris_produk_json(baru), "perubahan": perubahan,
                "ringkasan": {"ubah_produk": p["sku"], "perubahan": perubahan}}, teks

    return jalankan_tulis(args, db, "produk ubah", kerja)


def cmd_produk_cari(args):
    db = path_db(args)
    conn = buka(db)
    kata = (args.kata or "").strip()
    sql = "SELECT * FROM produk WHERE 1=1"
    par = []
    if not args.semua:
        sql += " AND aktif=1"
    for k in kata.split():
        sql += " AND (sku LIKE ? OR nama LIKE ? OR varian LIKE ? OR lokasi LIKE ?)"
        par += ["%" + k + "%"] * 4
    rows = conn.execute(sql + " ORDER BY sku", par).fetchall()
    conn.close()
    data = {"ok": True, "mode": "baca", "kata": kata, "jumlah": len(rows), "produk": [baris_produk_json(r) for r in rows]}
    if not rows:
        return data, "Tidak ada produk yang cocok dengan '%s'." % kata
    teks = "%d produk:\n" % len(rows) + "\n".join(
        "- %s | %s | stok %s %s | lokasi %s | HPP %s | jual %s"
        % (r["sku"], label_produk(r), fq(r["stok"]), r["satuan"], r["lokasi"] or "-", rp(r["hpp"]), rp(r["harga_jual"]))
        for r in rows)
    return data, teks


SINONIM_PRODUK = {
    "sku": ["sku", "kode sku", "kode", "kode barang", "kode produk", "nomor referensi sku", "seller sku"],
    "varian": ["varian", "variasi", "nama variasi", "variation"],
    "nama": ["nama", "nama produk", "nama barang", "produk", "barang", "product name"],
    "satuan": ["satuan", "unit"],
    "harga_beli": ["harga beli", "harga modal", "modal", "hpp", "harga pokok", "cost"],
    "harga_jual": ["harga jual", "harga", "price", "harga satuan"],
    "stok_min": ["stok minimum", "stok min", "minimum", "min stok", "stok minimal"],
    "stok": ["stok", "stok awal", "qty", "jumlah", "stock", "kuantitas"],
    "lokasi": ["lokasi", "rak", "lokasi rak", "gudang"],
}


def cmd_produk_impor(args):
    db = path_db(args)
    baris, jenis = baca_tabel(args.file)
    hi = cari_header(baris, SINONIM_PRODUK)
    if hi is None:
        raise Gagal("Judul kolom tidak dikenali. Minimal perlu kolom SKU dan Nama.",
                    kolom_ada=baris[0] if baris else [])
    header = baris[hi]
    kol = deteksi_kolom(header, SINONIM_PRODUK)
    if "sku" not in kol or "nama" not in kol:
        raise Gagal("Kolom SKU dan Nama wajib ada.", kolom_ada=header)
    tgl = tanggal_wajib(args.tanggal) if args.tanggal else hari_ini(args)
    pemetaan = {k: header[i] for k, i in kol.items()}

    def kerja(conn):
        baru, lewat, rusak = [], [], []
        nilai_awal = 0.0
        for no, r in enumerate(baris[hi + 1:], start=hi + 2):
            if not any((c or "").strip() for c in r):
                continue
            sku, nama = sel(r, kol["sku"]), sel(r, kol["nama"])
            if not sku or not nama:
                rusak.append({"baris": no, "alasan": "SKU/nama kosong"})
                continue
            nilai = {}
            for f in ("harga_beli", "harga_jual", "stok_min", "stok"):
                t = sel(r, kol.get(f))
                n = parse_angka(t) if t else 0.0
                if n is None or n < 0:
                    nilai = None
                    rusak.append({"baris": no, "sku": sku, "alasan": "angka %s tidak valid: %r" % (f, t)})
                    break
                nilai[f] = n
            if nilai is None:
                continue
            if conn.execute("SELECT 1 FROM produk WHERE sku=?", (sku,)).fetchone():
                lewat.append(sku)
                continue
            w = sekarang()
            cur = conn.execute(
                "INSERT INTO produk(sku,nama,varian,satuan,harga_beli,harga_jual,hpp,stok,stok_min,lokasi,dibuat,diubah)"
                " VALUES (?,?,?,?,?,?,?,0,?,?,?,?)",
                (sku, nama, sel(r, kol.get("varian")), sel(r, kol.get("satuan")) or "pcs", nilai["harga_beli"],
                 nilai["harga_jual"], nilai["harga_beli"], nilai["stok_min"], sel(r, kol.get("lokasi")), w, w))
            if nilai["stok"] > 0:
                p = conn.execute("SELECT * FROM produk WHERE id=?", (cur.lastrowid,)).fetchone()
                catat_mutasi(conn, p, "masuk", "saldo-awal", nilai["stok"], nilai["harga_beli"], tgl,
                             catatan="impor produk")
                nilai_awal += nilai["stok"] * nilai["harga_beli"]
            baru.append({"sku": sku, "nama": nama, "stok_awal": angka_json(nilai["stok"])})
        data = {"ok": True, "file": str(args.file), "pemetaan_kolom": pemetaan, "produk_baru": len(baru),
                "contoh": baru[:10], "sku_sudah_ada_dilewati": lewat, "baris_rusak": rusak,
                "nilai_stok_awal": bulat_rp(nilai_awal),
                "ringkasan": {"produk_baru": len(baru), "dilewati": len(lewat), "rusak": len(rusak)}}
        teks = ("Pemetaan kolom: %s\nProduk baru: %d (nilai stok awal %s)\nSKU sudah ada (dilewati): %d%s\n"
                "Baris rusak (dilewati): %d%s"
                % (", ".join("%s=%s" % kv for kv in pemetaan.items()), len(baru), rp(nilai_awal), len(lewat),
                   (" -> " + ", ".join(lewat[:10])) if lewat else "", len(rusak),
                   "".join("\n  baris %s: %s" % (x["baris"], x["alasan"]) for x in rusak[:10])))
        return data, teks

    return jalankan_tulis(args, db, "produk impor", kerja, label_backup="sebelum-impor-produk")


# ---------------------------------------------------------------------------
# Perintah: masuk & keluar
# ---------------------------------------------------------------------------

SINONIM_ITEM = {
    "sku": ["sku", "kode", "kode barang", "kode produk"],
    "qty": ["qty", "jumlah", "kuantitas", "quantity", "banyak"],
    "harga": ["harga", "harga beli", "harga satuan", "harga jual", "price"],
}


def _daftar_item(args):
    if args.file:
        baris, _ = baca_tabel(args.file)
        hi = cari_header(baris, SINONIM_ITEM)
        if hi is None:
            raise Gagal("File item perlu kolom SKU dan Qty.")
        kol = deteksi_kolom(baris[hi], SINONIM_ITEM)
        if "sku" not in kol or "qty" not in kol:
            raise Gagal("File item perlu kolom SKU dan Qty.", kolom_ada=baris[hi])
        items = []
        for no, r in enumerate(baris[hi + 1:], start=hi + 2):
            if not any((c or "").strip() for c in r):
                continue
            q = parse_angka(sel(r, kol["qty"]))
            if q is None or q <= 0:
                raise Gagal("Baris %d: qty '%s' tidak valid." % (no, sel(r, kol["qty"])))
            h = sel(r, kol.get("harga"))
            items.append((sel(r, kol["sku"]), q, angka_wajib(h, "harga baris %d" % no) if h else None))
        if not items:
            raise Gagal("File item tidak berisi baris data.")
        return items
    if not args.sku or args.qty is None:
        raise Gagal("Sebutkan --sku dan --qty (atau --file daftar.csv).")
    q = angka_wajib(args.qty, "qty", boleh_nol=False)
    h = angka_wajib(args.harga, "harga") if args.harga is not None else None
    return [(args.sku, q, h)]


def cmd_masuk(args):
    db = path_db(args)
    items = _daftar_item(args)
    tgl = tanggal_wajib(args.tanggal) if args.tanggal else hari_ini(args)
    biaya = angka_wajib(args.biaya_tambahan, "biaya tambahan") if args.biaya_tambahan else 0.0

    def kerja(conn):
        prods, total_barang = [], 0.0
        for sku, q, h in items:
            p = ambil_produk(conn, sku)
            if h is None:
                if args.jenis == "beli":
                    if p["harga_beli"] <= 0:
                        raise Gagal("Harga beli %s belum diketahui. Sebutkan --harga." % p["sku"])
                    h = float(p["harga_beli"])
                else:
                    h = float(p["hpp"]) if p["hpp"] > 0 else float(p["harga_beli"])
            prods.append((p, q, h))
            total_barang += q * h
        hasil = []
        for p, q, h in prods:
            porsi = (biaya * (q * h) / total_barang) if (biaya and total_barang > 0) else \
                (biaya / len(prods) if biaya else 0.0)
            h_efektif = h + porsi / q
            m = catat_mutasi(conn, p, "masuk", args.jenis, q, h_efektif, tgl, ref=args.ref, catatan=args.catatan)
            if args.jenis == "beli" and args.perbarui_harga_beli:
                conn.execute("UPDATE produk SET harga_beli=? WHERE id=?", (h, p["id"]))
            m["harga_beli"] = h
            m["biaya_tambahan_per_satuan"] = round(porsi / q, 2)
            hasil.append(m)
        total = sum(m["qty"] * (m["harga_beli"] + m["biaya_tambahan_per_satuan"]) for m in hasil)
        teks = "Barang MASUK (%s) tanggal %s%s:\n" % (args.jenis, tgl.isoformat(), (" ref " + args.ref) if args.ref else "")
        for m in hasil:
            teks += ("- %s %s: +%s @ %s%s | stok %s -> %s | HPP rata-rata %s -> %s\n"
                     % (m["sku"], m["nama"] + (" " + m["varian"] if m["varian"] else ""), fq(m["qty"]),
                        rp(m["harga_beli"]),
                        (" + biaya %s" % rp(m["biaya_tambahan_per_satuan"])) if m["biaya_tambahan_per_satuan"] else "",
                        fq(m["stok_sebelum"]), fq(m["stok_sesudah"]), rp(m["hpp_sebelum"]), rp(m["hpp_sesudah"])))
        teks += "Total nilai masuk: %s" % rp(total)
        return {"ok": True, "tanggal": tgl.isoformat(), "jenis": args.jenis, "item": hasil,
                "total_nilai": bulat_rp(total), "biaya_tambahan": bulat_rp(biaya),
                "ringkasan": {"masuk": [(m["sku"], m["qty"]) for m in hasil], "total": bulat_rp(total)}}, teks

    return jalankan_tulis(args, db, "masuk", kerja)


def cmd_keluar(args):
    db = path_db(args)
    items = _daftar_item(args)
    tgl = tanggal_wajib(args.tanggal) if args.tanggal else hari_ini(args)
    if args.jenis != "jual" and not (args.catatan or "").strip() and args.jenis in ("rusak", "hilang", "lainnya"):
        raise Gagal("Untuk barang keluar karena %s, isi --catatan (alasan singkat)." % args.jenis)

    def kerja(conn):
        hasil = []
        for sku, q, h in items:
            p = ambil_produk(conn, sku)
            if args.jenis == "jual" and h is None:
                h = float(p["harga_jual"]) if p["harga_jual"] > 0 else None
            m = catat_mutasi(conn, p, "keluar", args.jenis, -q, h, tgl, ref=args.ref, catatan=args.catatan,
                             izinkan_minus=args.izinkan_minus)
            m["nilai_hpp"] = bulat_rp(q * m["hpp_sebelum"])
            m["nilai_jual"] = bulat_rp(q * h) if (args.jenis == "jual" and h is not None) else None
            hasil.append(m)
        teks = "Barang KELUAR (%s) tanggal %s%s:\n" % (args.jenis, tgl.isoformat(), (" ref " + args.ref) if args.ref else "")
        peringatan = []
        for m in hasil:
            teks += ("- %s %s: %s | stok %s -> %s | nilai HPP %s%s\n"
                     % (m["sku"], m["nama"] + (" " + m["varian"] if m["varian"] else ""), fq(m["qty"]),
                        fq(m["stok_sebelum"]), fq(m["stok_sesudah"]), rp(m["nilai_hpp"]),
                        (" | nilai jual %s" % rp(m["nilai_jual"])) if m["nilai_jual"] is not None else ""))
            if m["minus"]:
                peringatan.append("Stok %s menjadi MINUS (%s). Segera cek fisik / opname." % (m["sku"], fq(m["stok_sesudah"])))
        if peringatan:
            teks += "PERINGATAN:\n" + "\n".join("- " + x for x in peringatan)
        return {"ok": True, "tanggal": tgl.isoformat(), "jenis": args.jenis, "item": hasil, "peringatan": peringatan,
                "ringkasan": {"keluar": [(m["sku"], m["qty"]) for m in hasil]}}, teks

    return jalankan_tulis(args, db, "keluar", kerja)


# ---------------------------------------------------------------------------
# Perintah: opname
# ---------------------------------------------------------------------------

SINONIM_OPNAME = {
    "sku": ["sku", "kode", "kode barang", "kode produk"],
    "fisik": ["fisik", "stok fisik", "hitung", "hitungan", "hasil hitung", "jumlah fisik", "qty fisik", "qty", "jumlah"],
    "alasan": ["alasan", "keterangan", "catatan"],
}


def cmd_opname(args):
    db = path_db(args)
    tgl = tanggal_wajib(args.tanggal) if args.tanggal else hari_ini(args)
    hitungan = []  # (sku, fisik, alasan)
    if args.file:
        baris, _ = baca_tabel(args.file)
        hi = cari_header(baris, SINONIM_OPNAME)
        kol = deteksi_kolom(baris[hi], SINONIM_OPNAME) if hi is not None else {}
        if "sku" not in kol or "fisik" not in kol:
            raise Gagal("File hitungan perlu kolom SKU dan Fisik (hasil hitung).",
                        kolom_ada=baris[hi] if hi is not None else (baris[0] if baris else []))
        for no, r in enumerate(baris[hi + 1:], start=hi + 2):
            if not any((c or "").strip() for c in r):
                continue
            t = sel(r, kol["fisik"])
            n = parse_angka(t)
            if n is None or n < 0:
                raise Gagal("Baris %d: hitungan fisik '%s' tidak valid." % (no, t))
            hitungan.append((sel(r, kol["sku"]), n, sel(r, kol.get("alasan"))))
    for h in args.hitung or []:
        if "=" not in h:
            raise Gagal("Format --hitung harus SKU=jumlah, mis. --hitung KAOS-HT-M=18")
        sku, _, n = h.rpartition("=")
        hitungan.append((sku.strip(), angka_wajib(n, "hitungan %s" % sku), ""))
    if not hitungan:
        raise Gagal("Belum ada hasil hitung. Pakai --hitung SKU=jumlah (boleh berulang) atau --file hitungan.csv")
    skus = [s.lower() for s, _, _ in hitungan]
    ganda = sorted({s for s in skus if skus.count(s) > 1})
    if ganda:
        raise Gagal("SKU dihitung lebih dari sekali: %s. Jumlahkan dulu hasil hitungnya." % ", ".join(ganda))

    def kerja(conn):
        hasil, kurang_alasan = [], []
        tot_plus = tot_minus = 0.0
        for sku, fisik, alasan in hitungan:
            p = ambil_produk(conn, sku)
            # Barang pesanan yang sudah dipotong dari stok tetapi BELUM dikemas masih ada di rak.
            tertahan = conn.execute(
                "SELECT COALESCE(SUM(i.qty),0) FROM pesanan_item i JOIN pesanan s ON s.id=i.pesanan_id "
                "WHERE i.produk_id=? AND i.mutasi_id IS NOT NULL AND s.kategori IN ('perlu_kirim','tanpa_status') "
                "AND s.dikemas=0 AND s.dibatalkan=0", (p["id"],)).fetchone()[0]
            sistem = rapikan_qty(float(p["stok"]) + tertahan)
            selisih = rapikan_qty(fisik - sistem)
            al = (alasan or args.alasan or "").strip()
            baris = {"sku": p["sku"], "nama": label_produk(p), "stok_sistem": angka_json(sistem),
                     "termasuk_pesanan_belum_dikemas": angka_json(tertahan),
                     "stok_fisik": angka_json(fisik), "selisih": angka_json(selisih),
                     "nilai_selisih": bulat_rp(selisih * (p["hpp"] or p["harga_beli"])), "alasan": al}
            if abs(selisih) > EPS:
                if not al:
                    kurang_alasan.append(p["sku"])
                else:
                    catat_mutasi(conn, p, "opname", "opname", selisih, None, tgl, ref=args.ref or "opname",
                                 catatan=al, izinkan_minus=True)
                if selisih > 0:
                    tot_plus += baris["nilai_selisih"]
                else:
                    tot_minus += baris["nilai_selisih"]
            hasil.append(baris)
        if kurang_alasan and args.ya:
            raise Gagal("Ada selisih tanpa alasan: %s. Isi --alasan \"...\" atau kolom Alasan di file."
                        % ", ".join(kurang_alasan), sku_tanpa_alasan=kurang_alasan)
        tidak_dihitung = conn.execute(
            "SELECT COUNT(*) FROM produk WHERE aktif=1 AND sku NOT IN (%s)" % ",".join("?" * len(hasil)),
            [h["sku"] for h in hasil]).fetchone()[0]
        beda = [h for h in hasil if h["selisih"] != 0]
        teks = "STOCK OPNAME tanggal %s - %d SKU dihitung, %d ada selisih\n" % (tgl.isoformat(), len(hasil), len(beda))
        for h in hasil:
            tanda = "cocok" if h["selisih"] == 0 else ("%+g" % h["selisih"]).replace(".", ",")
            teks += "- %s %s: sistem %s%s, fisik %s -> %s%s%s\n" % (
                h["sku"], h["nama"], fq(h["stok_sistem"]),
                (" (termasuk %s milik pesanan belum dikemas)" % fq(h["termasuk_pesanan_belum_dikemas"]))
                if h["termasuk_pesanan_belum_dikemas"] else "", fq(h["stok_fisik"]), tanda,
                (" (%s)" % rp(h["nilai_selisih"])) if h["selisih"] else "", (" alasan: " + h["alasan"]) if h["alasan"] and h["selisih"] else "")
        teks += "Nilai lebih: %s | Nilai kurang: %s | Bersih: %s" % (rp(tot_plus), rp(tot_minus), rp(tot_plus + tot_minus))
        if tidak_dihitung:
            teks += "\nCatatan: %d produk aktif lain tidak ikut dihitung (stoknya tidak diubah)." % tidak_dihitung
        if kurang_alasan:
            teks += "\nPERLU ALASAN untuk: %s (mis. rusak, hilang, salah catat, bonus supplier)." % ", ".join(kurang_alasan)
        return {"ok": True, "tanggal": tgl.isoformat(), "hasil": hasil, "jumlah_selisih": len(beda),
                "nilai_lebih": bulat_rp(tot_plus), "nilai_kurang": bulat_rp(tot_minus),
                "nilai_bersih": bulat_rp(tot_plus + tot_minus), "produk_tidak_dihitung": tidak_dihitung,
                "sku_tanpa_alasan": kurang_alasan,
                "ringkasan": {"opname_sku": len(hasil), "selisih": len(beda), "nilai_bersih": bulat_rp(tot_plus + tot_minus)}}, teks

    return jalankan_tulis(args, db, "opname", kerja, label_backup="sebelum-opname")


# ---------------------------------------------------------------------------
# Perintah: impor-pesanan (Shopee / TikTok Shop / Tokopedia / lainnya)
# ---------------------------------------------------------------------------

# Nama kolom umum di file ekspor pesanan. Urutan = prioritas. Selalu minta pengguna
# mengonfirmasi pemetaan karena nama kolom marketplace bisa berubah sewaktu-waktu.
SINONIM_PESANAN = {
    "no_pesanan": ["no. pesanan", "no pesanan", "nomor pesanan", "order id", "order no", "order number",
                   "nomor invoice", "no. invoice", "no invoice", "invoice", "id pesanan", "no. order"],
    "resi": ["no. resi", "nomor resi", "no resi", "tracking id", "tracking number", "no resi / kode booking",
             "id pelacakan", "nomor pelacakan", "kode booking", "awb", "resi"],
    "batas_kirim": ["pesanan harus dikirimkan sebelum", "harus dikirimkan sebelum", "ship by date", "ship by",
                    "batas kirim", "batas pengiriman"],
    "tanggal": ["waktu pesanan dibuat", "created time", "waktu dibuat", "waktu pembuatan", "tanggal pesanan",
                "tanggal pembayaran", "waktu pembayaran dilakukan", "paid time", "waktu dibayar", "order date",
                "tanggal", "waktu"],
    "status": ["status pesanan", "order status", "status terakhir", "status"],
    "sku": ["nomor referensi sku", "seller sku", "sku penjual", "nomor sku", "sku", "kode sku", "sku induk",
            "kode produk", "kode barang"],
    "varian": ["nama variasi", "variation", "variasi", "varian", "tipe produk"],
    "nama": ["nama produk", "product name", "nama barang", "produk"],
    "tipe_retur": ["cancelation/return type", "cancellation/return type", "tipe pembatalan/pengembalian",
                   "jenis pembatalan/pengembalian"],
    "qty_retur": ["returned quantity", "sku quantity of return", "jumlah dikembalikan", "jumlah produk dikembalikan",
                  "jumlah sku yang dikembalikan", "jumlah pengembalian sku", "jumlah pengembalian"],
    "qty": ["jumlah", "quantity", "qty", "jumlah produk dibeli", "kuantitas", "jumlah barang"],
    "kurir": ["opsi pengiriman", "shipping provider name", "nama penyedia pengiriman", "penyedia pengiriman",
              "shipping provider", "kurir", "jasa kirim", "ekspedisi", "delivery option", "jasa pengiriman"],
    "harga": ["harga setelah diskon", "harga satuan setelah diskon", "harga satuan", "harga jual", "unit price",
              "harga"],
    "harga_total": ["sku subtotal after discount", "subtotal sku setelah diskon", "subtotal setelah diskon",
                    "total harga produk", "subtotal produk", "subtotal"],
}
LABEL_FIELD = {
    "no_pesanan": "No. pesanan", "sku": "SKU", "nama": "Nama produk", "varian": "Varian", "qty": "Jumlah",
    "status": "Status", "resi": "No. resi", "kurir": "Kurir", "tanggal": "Tanggal", "batas_kirim": "Batas kirim",
    "harga": "Harga satuan", "harga_total": "Subtotal baris", "tipe_retur": "Tipe batal/retur",
    "qty_retur": "Jumlah diretur",
}

KATA_BATAL = ["batal", "dibatalkan", "cancel", "canceled", "cancelled", "gagal", "failed", "expired", "kedaluwarsa"]
KATA_RETUR = ["retur", "return", "refund", "pengembalian", "dikembalikan"]
KATA_BELUM_BAYAR = ["belum bayar", "belum dibayar", "unpaid", "menunggu pembayaran", "awaiting payment"]
KATA_BATAL_DIAJUKAN = ["diajukan", "requested", "request", "permintaan", "pengajuan", "menunggu"]
KATA_PERLU_KIRIM = ["akan dikirim", "menunggu pengiriman", "menunggu dikirim", "menunggu konfirmasi", "perlu dikirim", "siap dikirim", "sedang dikemas", "dikemas", "to ship", "awaiting shipment",
                    "awaiting collection", "ready to ship", "diproses", "pesanan baru", "belum dikirim",
                    "menunggu pickup", "menunggu penjemputan", "processing", "packed", "perlu diproses"]
KATA_DIKIRIM = ["sedang dikirim", "dalam pengiriman", "telah dikirim", "dikirim", "shipped", "in transit",
                "shipping"]
KATA_SELESAI = ["selesai", "completed", "delivered", "diterima", "terkirim", "pesanan tiba"]
PENGECUALIAN = ["ditolak", "rejected", "pembatalan ditolak", "dibatalkan pembatalannya"]


def kategori_status(teks, abaikan=None):
    s = norm(str(teks or "").replace("_", " "))
    if not s:
        return "tanpa_status"
    if abaikan is not None:
        if any(k in s for k in abaikan):
            return "batal"
    else:
        dikecualikan = any(k in s for k in PENGECUALIAN)
        if not dikecualikan:
            if any(k in s for k in KATA_BATAL):
                if any(k in s for k in KATA_BATAL_DIAJUKAN):
                    return "batal_diajukan"   # belum pasti batal: stok tidak diubah
                return "batal"
            if any(k in s for k in KATA_RETUR):
                return "retur"
    if any(k in s for k in KATA_BELUM_BAYAR):
        return "belum_bayar"
    if any(k in s for k in KATA_PERLU_KIRIM):
        return "perlu_kirim"
    if any(k in s for k in KATA_DIKIRIM):
        return "dikirim"
    if any(k in s for k in KATA_SELESAI):
        return "selesai"
    return "lainnya"


def norm_no_pesanan(t):
    t = (t or "").strip().lstrip("'").strip()
    if re.fullmatch(r"\d+\.0+", t):
        t = t.split(".")[0]
    return t


def tebak_platform(header):
    h = {norm(x) for x in header}
    if "nomor referensi sku" in h or "no. pesanan" in h or any("dikirimkan sebelum" in x for x in h):
        return "shopee"
    if ("seller sku" in h or ("order id" in h and "tracking id" in h) or "id pelacakan" in h
            or "sku penjual" in h or "nama penyedia pengiriman" in h):
        return "tiktok"
    if "nomor invoice" in h:
        return "tokopedia"
    return "lainnya"


def _cocokkan_produk(conn, sku, nama, varian, cache):
    kunci = (sku.lower(), nama.lower(), varian.lower())
    if kunci in cache:
        return cache[kunci]
    p = None
    if sku:
        p = conn.execute("SELECT * FROM produk WHERE sku=?", (sku,)).fetchone()
    if p is None and nama:
        # Cocokkan nama (+ varian) persis, hanya bila hasilnya tunggal.
        kandidat = conn.execute("SELECT * FROM produk WHERE lower(nama)=?", (nama.lower().strip(),)).fetchall()
        if varian:
            kandidat = [k for k in kandidat if norm(k["varian"]) == norm(varian)]
        if len(kandidat) == 1:
            p = kandidat[0]
    cache[kunci] = p
    return p


def cmd_impor_pesanan(args):
    db = path_db(args)
    baris, jenis_file = baca_tabel(args.file)
    hi = cari_header(baris, SINONIM_PESANAN, minimal=2)
    if hi is None:
        raise Gagal("Judul kolom pesanan tidak dikenali. Pastikan ini file ekspor pesanan (bukan laporan lain).",
                    kolom_ada=[c for c in (baris[0] if baris else [])][:40])
    header = baris[hi]
    kol = deteksi_kolom(header, SINONIM_PESANAN)
    header_norm = [norm(h) for h in header]
    # Pemetaan manual dari pengguna/agent mengalahkan deteksi otomatis.
    for field in SINONIM_PESANAN:
        nilai = getattr(args, "kolom_" + field, None)
        if nilai is None:
            continue
        if nilai.strip() == "-":
            kol.pop(field, None)
            continue
        if norm(nilai) not in header_norm:
            raise Gagal("Kolom '%s' (untuk %s) tidak ada di file." % (nilai, LABEL_FIELD[field]), kolom_ada=header)
        idx = header_norm.index(norm(nilai))
        for f2, i2 in list(kol.items()):
            if i2 == idx and f2 != field:
                kol.pop(f2)
        kol[field] = idx
    pemetaan = {f: header[i] for f, i in sorted(kol.items(), key=lambda x: x[1])}
    hilang = [LABEL_FIELD[f] for f in ("no_pesanan", "qty") if f not in kol]
    if "sku" not in kol and "nama" not in kol:
        hilang.append("SKU atau Nama produk")
    if hilang:
        raise Gagal("Kolom wajib tidak ketemu: %s. Sebutkan manual, mis. --kolom-no-pesanan \"Nama Kolom\"."
                    % ", ".join(hilang), kolom_ada=header, pemetaan_terdeteksi=pemetaan)
    platform = args.platform or tebak_platform(header)
    abaikan = [norm(x) for x in args.abaikan_status.split(",") if x.strip()] if args.abaikan_status else None
    tgl_default = hari_ini(args)

    # 1) Parse baris -> pesanan
    urut, pesanan = [], {}
    lewat = {"qty_tidak_valid": [], "nomor_rusak": [], "baris_kembar": 0}
    no_sebelum, isi_ikut = "", 0
    for no, r in enumerate(baris[hi + 1:], start=hi + 2):
        if not any((c or "").strip() for c in r):
            continue
        nop = norm_no_pesanan(sel(r, kol["no_pesanan"]))
        if re.search(r"\d[.,]\d+e\+?\d+", nop.lower()):
            lewat["nomor_rusak"].append(no)
            continue
        if not nop:
            if no_sebelum:
                nop = no_sebelum
                isi_ikut += 1
            else:
                lewat["qty_tidak_valid"].append(no)
                continue
        q = parse_angka(sel(r, kol["qty"]))
        if q is None or q <= 0 or abs(q - round(q, 3)) > 1e-9:
            lewat["qty_tidak_valid"].append(no)
            continue
        no_sebelum = nop
        harga = parse_angka(sel(r, kol.get("harga"))) if "harga" in kol else None
        if harga is None and "harga_total" in kol:
            tot = parse_angka(sel(r, kol["harga_total"]))
            harga = (tot / q) if tot is not None else None
        tanda_retur = False
        if "tipe_retur" in kol and re.search(r"retur|return|refund|pengembalian", sel(r, kol["tipe_retur"]).lower()):
            tanda_retur = True
        if "qty_retur" in kol and (parse_angka(sel(r, kol["qty_retur"])) or 0) > 0:
            tanda_retur = True
        item = {"baris": no, "sku": sel(r, kol.get("sku")), "nama": sel(r, kol.get("nama")),
                "varian": sel(r, kol.get("varian")), "qty": q, "harga": harga, "tanda_retur": tanda_retur}
        if nop not in pesanan:
            st = sel(r, kol.get("status"))
            tgl = parse_tanggal(sel(r, kol.get("tanggal"))) if "tanggal" in kol else None
            pesanan[nop] = {"no": nop, "status": st, "kategori": kategori_status(st, abaikan) if "status" in kol else "tanpa_status",
                            "tanggal": tgl, "resi": sel(r, kol.get("resi")).lstrip("'"), "kurir": sel(r, kol.get("kurir")),
                            "batas_kirim": sel(r, kol.get("batas_kirim")), "item": []}
            urut.append(nop)
        ps = pesanan[nop]
        if any(i["sku"] == item["sku"] and i["nama"] == item["nama"] and i["varian"] == item["varian"]
               and i["qty"] == item["qty"] for i in ps["item"]):
            lewat["baris_kembar"] += 1
            continue
        ps["item"].append(item)
    if not pesanan:
        raise Gagal("Tidak ada baris pesanan yang bisa dibaca dari file. Cek kolom Jumlah/No. pesanan.",
                    pemetaan=pemetaan, baris_dilewati=lewat)

    def kerja(conn):
        imp = conn.execute("INSERT INTO impor(waktu,file,platform,baris,pesanan_baru,pemetaan) VALUES (?,?,?,?,?,?)",
                           (sekarang(), Path(args.file).name, platform, len(baris) - hi - 1, 0,
                            json.dumps(pemetaan, ensure_ascii=False))).lastrowid
        cache = {}
        hit = {"baru": 0, "sudah_ada": 0, "batal": 0, "retur": 0, "belum_bayar": 0}
        per_sku, tak_dikenal, minus, dibatalkan_ulang, cek_retur, status_asing = {}, {}, {}, [], [], {}
        contoh_ganda, aktif_lagi, diajukan, item_lama_terpotong, tanda_retur = [], [], [], [], []

        def potong(p, qty, harga, tanggal, nop):
            m = catat_mutasi(conn, p, "keluar", "jual-mp", -qty, harga, tanggal, ref=nop, catatan=platform,
                             impor_id=imp, izinkan_minus=True)
            s = per_sku.setdefault(p["sku"], {"sku": p["sku"], "nama": label_produk(p), "qty": 0,
                                              "stok_sebelum": m["stok_sebelum"], "stok_sesudah": 0})
            s["qty"] = angka_json(s["qty"] + qty)
            s["stok_sesudah"] = m["stok_sesudah"]
            if m["minus"]:
                minus[p["sku"]] = m["stok_sesudah"]
            return m
        for nop in urut:
            ps = pesanan[nop]
            kat = ps["kategori"]
            if kat == "lainnya":
                status_asing[ps["status"]] = status_asing.get(ps["status"], 0) + 1
            if kat not in ("batal", "retur", "belum_bayar") and any(i["tanda_retur"] for i in ps["item"]):
                tanda_retur.append(nop)
            tgl_ps = ps["tanggal"] or tgl_default
            lama = conn.execute("SELECT * FROM pesanan WHERE no_pesanan=?", (nop,)).fetchone()
            if lama is not None:
                hit["sudah_ada"] += 1
                if len(contoh_ganda) < 10:
                    contoh_ganda.append(nop)
                if kat == "batal" and not lama["dibatalkan"]:
                    # Pesanan yang dulu diimpor kini batal -> kembalikan stok sesuai HPP saat keluar.
                    for it in conn.execute("SELECT i.*, m.hpp AS hpp_keluar FROM pesanan_item i "
                                           "LEFT JOIN mutasi m ON m.id=i.mutasi_id WHERE i.pesanan_id=?",
                                           (lama["id"],)).fetchall():
                        if it["produk_id"] is None or it["mutasi_id"] is None:
                            continue
                        p = conn.execute("SELECT * FROM produk WHERE id=?", (it["produk_id"],)).fetchone()
                        catat_mutasi(conn, p, "masuk", "batal-pesanan", it["qty"], it["hpp_keluar"],
                                     tgl_ps, ref=nop, catatan="pesanan batal setelah diimpor", impor_id=imp)
                        # penjualan asalnya tidak lagi dihitung di laporan penjualan
                        conn.execute("UPDATE mutasi SET dibatalkan=1 WHERE id=?", (it["mutasi_id"],))
                    conn.execute("UPDATE pesanan SET dibatalkan=1, status=?, kategori=?, diubah=? WHERE id=?",
                                 (ps["status"], kat, sekarang(), lama["id"]))
                    dibatalkan_ulang.append(nop)
                elif lama["dibatalkan"] and kat not in ("batal", "retur", "belum_bayar"):
                    # Dulu batal, kini aktif lagi (mis. pembatalan ditolak) -> potong stok ulang.
                    for it in conn.execute("SELECT * FROM pesanan_item WHERE pesanan_id=? AND produk_id IS NOT NULL",
                                           (lama["id"],)).fetchall():
                        p = conn.execute("SELECT * FROM produk WHERE id=?", (it["produk_id"],)).fetchone()
                        m = potong(p, it["qty"], it["harga"], tgl_ps, nop)
                        conn.execute("UPDATE pesanan_item SET mutasi_id=? WHERE id=?", (m["mutasi_id"], it["id"]))
                    conn.execute("UPDATE pesanan SET dibatalkan=0, dikemas=0, status=?, kategori=?, diubah=? WHERE id=?",
                                 (ps["status"], kat, sekarang(), lama["id"]))
                    aktif_lagi.append(nop)
                elif kat == "retur" and lama["kategori"] != "retur":
                    conn.execute("UPDATE pesanan SET status=?, kategori=?, diubah=? WHERE id=?",
                                 (ps["status"], kat, sekarang(), lama["id"]))
                    cek_retur.append(nop)
                elif not lama["dibatalkan"]:
                    conn.execute("UPDATE pesanan SET status=?, kategori=?, resi=CASE WHEN ?<>'' THEN ? ELSE resi END,"
                                 " kurir=CASE WHEN ?<>'' THEN ? ELSE kurir END, diubah=? WHERE id=?",
                                 (ps["status"] or lama["status"], kat if ps["status"] else lama["kategori"],
                                  ps["resi"], ps["resi"], ps["kurir"], ps["kurir"], sekarang(), lama["id"]))
                    if kat == "batal_diajukan" and lama["kategori"] != "batal_diajukan":
                        diajukan.append(nop)
                # Item yang dulu dilewati (SKU belum terdaftar): coba cocokkan lagi & potong stoknya.
                sekarang_aktif = conn.execute("SELECT dibatalkan, kategori FROM pesanan WHERE id=?", (lama["id"],)).fetchone()
                if not sekarang_aktif["dibatalkan"] and sekarang_aktif["kategori"] not in ("batal", "retur", "belum_bayar"):
                    for it in conn.execute("SELECT * FROM pesanan_item WHERE pesanan_id=? AND produk_id IS NULL",
                                           (lama["id"],)).fetchall():
                        # Cocokkan lewat SKU bila item punya SKU; lewat nama hanya bila SKU kosong DAN nama
                        # tidak kosong (mencegah "" == "" mencocokkan item pertama pada file SKU-saja).
                        if it["sku_mp"]:
                            sumber = next((f for f in ps["item"] if f["sku"] == it["sku_mp"]), None)
                        elif (it["nama_mp"] or "").strip():
                            sumber = next((f for f in ps["item"] if not f["sku"] and
                                           ("%s %s" % (f["nama"], f["varian"])).strip() == it["nama_mp"].strip()), None)
                        else:
                            sumber = None
                        if sumber is None:
                            continue
                        p = _cocokkan_produk(conn, sumber["sku"], sumber["nama"], sumber["varian"], cache)
                        if p is None:
                            k = it["sku_mp"] or it["nama_mp"]
                            d = tak_dikenal.setdefault(k, {"sku_marketplace": it["sku_mp"], "nama": sumber["nama"],
                                                           "varian": sumber["varian"], "qty": 0, "pesanan": 0})
                            d["qty"] = angka_json(d["qty"] + it["qty"])
                            d["pesanan"] += 1
                            continue
                        m = potong(p, it["qty"], it["harga"], tgl_ps, nop)
                        conn.execute("UPDATE pesanan_item SET produk_id=?, mutasi_id=? WHERE id=?",
                                     (p["id"], m["mutasi_id"], it["id"]))
                        item_lama_terpotong.append("%s (%s x%s)" % (nop, p["sku"], fq(it["qty"])))
                continue
            if kat in ("batal", "retur", "belum_bayar"):
                hit[kat] += 1
                continue
            if kat == "batal_diajukan":
                diajukan.append(nop)
            hit["baru"] += 1
            pid = conn.execute(
                "INSERT INTO pesanan(no_pesanan,platform,tanggal,status,kategori,resi,kurir,batas_kirim,impor_id,diubah)"
                " VALUES (?,?,?,?,?,?,?,?,?,?)",
                (nop, platform, (ps["tanggal"] or tgl_default).isoformat(), ps["status"], kat, ps["resi"],
                 ps["kurir"], ps["batas_kirim"], imp, sekarang())).lastrowid
            for it in ps["item"]:
                p = _cocokkan_produk(conn, it["sku"], it["nama"], it["varian"], cache)
                mid = None
                if p is None:
                    k = it["sku"] or ("%s %s" % (it["nama"], it["varian"])).strip()
                    d = tak_dikenal.setdefault(k, {"sku_marketplace": it["sku"], "nama": it["nama"],
                                                   "varian": it["varian"], "qty": 0, "pesanan": 0})
                    d["qty"] = angka_json(d["qty"] + it["qty"])
                    d["pesanan"] += 1
                else:
                    mid = potong(p, it["qty"], it["harga"], tgl_ps, nop)["mutasi_id"]
                conn.execute("INSERT INTO pesanan_item(pesanan_id,produk_id,sku_mp,nama_mp,qty,harga,mutasi_id)"
                             " VALUES (?,?,?,?,?,?,?)",
                             (pid, p["id"] if p else None, it["sku"], ("%s %s" % (it["nama"], it["varian"])).strip(),
                              it["qty"], it["harga"], mid))
        conn.execute("UPDATE impor SET pesanan_baru=? WHERE id=?", (hit["baru"], imp))
        if tak_dikenal and args.ya and not args.lewati_tak_dikenal:
            raise Gagal("Ada %d SKU dari file yang belum terdaftar di buku stok: %s. Tambahkan produknya dulu "
                        "(produk tambah) atau jalankan dengan --lewati-tak-dikenal (stok barang itu tidak dikurangi)."
                        % (len(tak_dikenal), ", ".join(list(tak_dikenal)[:10])), sku_tak_dikenal=list(tak_dikenal.values()))
        peringatan = []
        if hit["baru"] == 0 and not (aktif_lagi or item_lama_terpotong):
            peringatan.append("Tidak ada pesanan baru di file ini (semua sudah pernah diimpor atau dilewati).")
        if item_lama_terpotong:
            peringatan.append("%d item pesanan lama yang dulu dilewati (SKU belum terdaftar) kini dicocokkan & "
                              "stoknya dipotong: %s" % (len(item_lama_terpotong), ", ".join(item_lama_terpotong[:20])))
        if aktif_lagi:
            peringatan.append("Pesanan yang sebelumnya batal kini AKTIF lagi, stok dipotong ulang: %s"
                              % ", ".join(aktif_lagi[:20]))
        if diajukan:
            peringatan.append("Pembatalan DIAJUKAN (belum pasti batal; tidak masuk daftar ambil sampai statusnya "
                              "jelas). Pesanan yang sudah pernah diimpor: stok tidak diubah. Pesanan baru: stok "
                              "tetap dipotong karena pesanan masih sah; bila akhirnya batal, stok dikembalikan saat "
                              "impor berikutnya: %s" % ", ".join(diajukan[:20]))
        if tanda_retur:
            peringatan.append("Pesanan sah tetapi ada tanda retur/refund di kolom retur (stok TIDAK otomatis ditambah; "
                              "cek barangnya): %s" % ", ".join(tanda_retur[:20]))
        if minus:
            peringatan.append("Stok menjadi MINUS setelah impor: %s. Kemungkinan stok belum dicatat/terlewat restock; "
                              "lakukan opname untuk SKU ini." % ", ".join("%s (%s)" % (k, fq(v)) for k, v in minus.items()))
        if status_asing:
            peringatan.append("Status tidak dikenal (tetap dihitung terjual): %s. Jika ini pesanan batal, jalankan "
                              "ulang dengan --abaikan-status." % ", ".join("%s (%d)" % kv for kv in status_asing.items()))
        if "status" not in kol:
            peringatan.append("File tidak punya kolom status: semua pesanan dianggap sah & belum dikirim.")
        if lewat["nomor_rusak"]:
            peringatan.append("%d baris nomor pesanannya rusak (tampil seperti 2,4E+17 karena dibuka di Excel). "
                              "Ekspor ulang dari Seller Center tanpa membuka di Excel." % len(lewat["nomor_rusak"]))
        if isi_ikut:
            peringatan.append("%d baris tanpa nomor pesanan dianggap lanjutan pesanan di atasnya." % isi_ikut)
        if cek_retur:
            peringatan.append("Pesanan yang kini berstatus retur/refund (stok TIDAK otomatis ditambah; cek fisik "
                              "barangnya lalu catat 'masuk --jenis retur-pembeli' bila layak jual): %s" % ", ".join(cek_retur[:20]))
        tq = sum(v["qty"] for v in per_sku.values())
        data = {
            "ok": True, "file": str(args.file), "jenis_file": jenis_file, "platform": platform,
            "baris_judul": hi + 1, "pemetaan_kolom": {LABEL_FIELD[k]: v for k, v in pemetaan.items()},
            "pesanan_baru": hit["baru"], "pesanan_sudah_pernah_diimpor": hit["sudah_ada"],
            "contoh_pesanan_ganda": contoh_ganda, "diabaikan_batal": hit["batal"], "diabaikan_retur": hit["retur"],
            "diabaikan_belum_bayar": hit["belum_bayar"], "pesanan_lama_kini_batal_stok_dikembalikan": dibatalkan_ulang,
            "pesanan_lama_kini_retur": cek_retur, "pesanan_batal_kini_aktif_lagi": aktif_lagi,
            "pembatalan_diajukan": diajukan, "item_lama_kini_terpotong": item_lama_terpotong,
            "pesanan_bertanda_retur": tanda_retur, "barang_keluar": list(per_sku.values()), "total_qty_keluar": angka_json(tq),
            "sku_tak_dikenal": list(tak_dikenal.values()), "stok_minus": {k: angka_json(v) for k, v in minus.items()},
            "baris_dilewati": {"qty_tidak_valid": len(lewat["qty_tidak_valid"]), "contoh_baris": lewat["qty_tidak_valid"][:10],
                               "nomor_pesanan_rusak": len(lewat["nomor_rusak"]), "baris_kembar": lewat["baris_kembar"]},
            "peringatan": peringatan,
            "ringkasan": {"file": Path(args.file).name, "pesanan_baru": hit["baru"], "qty_keluar": angka_json(tq)},
        }
        t = ["IMPOR PESANAN %s (%s) - file %s" % (platform.upper(), jenis_file.upper(), Path(args.file).name),
             "Pemetaan kolom (mohon dicek):"]
        t += ["  %-16s <- %s" % (LABEL_FIELD[k], v) for k, v in pemetaan.items()]
        t.append("Pesanan baru: %d | sudah pernah diimpor (dilewati): %d" % (hit["baru"], hit["sudah_ada"]))
        t.append("Diabaikan: batal %d, retur/refund %d, belum bayar %d" % (hit["batal"], hit["retur"], hit["belum_bayar"]))
        if dibatalkan_ulang:
            t.append("Pesanan lama yang kini BATAL (stok dikembalikan): %s" % ", ".join(dibatalkan_ulang))
        if per_sku:
            t.append("Stok berkurang (total %s):" % fq(tq))
            for v in sorted(per_sku.values(), key=lambda x: -x["qty"]):
                t.append("  - %s %s: -%s (stok %s -> %s)" % (v["sku"], v["nama"], fq(v["qty"]), fq(v["stok_sebelum"]), fq(v["stok_sesudah"])))
        if tak_dikenal:
            t.append("SKU BELUM TERDAFTAR (stok tidak dikurangi):")
            for v in tak_dikenal.values():
                t.append("  - %s %s %s: %s pcs di %d pesanan" % (v["sku_marketplace"] or "(tanpa SKU)", v["nama"], v["varian"], fq(v["qty"]), v["pesanan"]))
        dl = data["baris_dilewati"]
        if dl["qty_tidak_valid"] or dl["baris_kembar"]:
            t.append("Baris dilewati: %d (jumlah tidak valid/baris keterangan), %d baris kembar"
                     % (dl["qty_tidak_valid"], dl["baris_kembar"]))
        if peringatan:
            t.append("PERINGATAN:")
            t += ["  - " + x for x in peringatan]
        return data, "\n".join(t)

    return jalankan_tulis(args, db, "impor-pesanan", kerja, label_backup="sebelum-impor-pesanan")


# ---------------------------------------------------------------------------
# Perintah: picking
# ---------------------------------------------------------------------------


def _pesanan_belum_kirim(conn, platform=None):
    sql = ("SELECT * FROM pesanan WHERE kategori IN ('perlu_kirim','tanpa_status') AND dikemas=0 AND dibatalkan=0")
    par = []
    if platform:
        sql += " AND platform=?"
        par.append(platform)
    return conn.execute(sql, par).fetchall()


def cmd_picking(args):
    db = path_db(args)
    conn = buka(db)
    ps = _pesanan_belum_kirim(conn, args.platform)
    ids = [p["id"] for p in ps]
    items = []
    if ids:
        items = conn.execute(
            "SELECT i.*, p.sku, p.nama, p.varian, p.satuan, p.lokasi, p.stok FROM pesanan_item i "
            "LEFT JOIN produk p ON p.id=i.produk_id WHERE i.pesanan_id IN (%s) ORDER BY i.id" % ",".join("?" * len(ids)),
            ids).fetchall()
    per_pesanan = {}
    for it in items:
        per_pesanan.setdefault(it["pesanan_id"], []).append(it)
    ambil = {}
    for it in items:
        k = it["sku"] or ("?" + (it["sku_mp"] or it["nama_mp"]))
        a = ambil.setdefault(k, {"lokasi": it["lokasi"] if it["sku"] else "(belum terdaftar)",
                                 "sku": it["sku"] or it["sku_mp"], "nama": ("%s%s" % (it["nama"], (" - " + it["varian"]) if it["varian"] else "")) if it["sku"] else it["nama_mp"],
                                 "satuan": it["satuan"] or "pcs", "qty": 0, "jumlah_pesanan": 0,
                                 "stok_sisa": angka_json(it["stok"]) if it["sku"] else None, "terdaftar": bool(it["sku"])})
        a["qty"] = angka_json(a["qty"] + it["qty"])
        a["jumlah_pesanan"] += 1
    daftar_ambil = sorted(ambil.values(), key=lambda a: (not a["terdaftar"], a["lokasi"] == "", a["lokasi"] or "", a["sku"] or ""))

    def kunci(p):
        if args.urut == "batas":
            return (p["batas_kirim"] or "9999", p["kurir"], p["resi"], p["no_pesanan"])
        if args.urut == "resi":
            return (p["resi"] or "~", p["no_pesanan"])
        if args.urut == "pesanan":
            return (p["id"],)
        return (p["kurir"] or "~", p["resi"] or "~", p["no_pesanan"])

    urutan = []
    for n, p in enumerate(sorted(ps, key=kunci), start=1):
        urutan.append({"urut": n, "no_pesanan": p["no_pesanan"], "platform": p["platform"], "kurir": p["kurir"],
                       "resi": p["resi"], "batas_kirim": p["batas_kirim"],
                       "item": [{"sku": it["sku"] or it["sku_mp"], "nama": it["nama_mp"] if not it["sku"] else
                                 ("%s%s" % (it["nama"], (" - " + it["varian"]) if it["varian"] else "")),
                                 "qty": angka_json(it["qty"]), "lokasi": it["lokasi"] or ""} for it in per_pesanan.get(p["id"], [])]})
    peringatan = [ "Barang %s belum terdaftar di buku stok." % a["sku"] for a in daftar_ambil if not a["terdaftar"]]
    peringatan += ["Stok %s tercatat minus (%s): cek fisik sebelum mengemas." % (a["sku"], fq(a["stok_sisa"]))
                   for a in daftar_ambil if a["terdaftar"] and a["stok_sisa"] is not None and a["stok_sisa"] < 0]
    data = {"ok": True, "mode": "baca", "jumlah_pesanan": len(ps), "total_barang": angka_json(sum(a["qty"] for a in daftar_ambil)),
            "daftar_ambil": daftar_ambil, "urutan_pesanan": urutan, "urut_berdasarkan": args.urut, "peringatan": peringatan}
    t = ["DAFTAR AMBIL BARANG (picking) - %d pesanan, %s barang" % (len(ps), fq(data["total_barang"]))]
    if not ps:
        t = ["Tidak ada pesanan yang menunggu dikemas. Impor dulu file pesanan 'Perlu Dikirim' dari Seller Center."]
    else:
        t.append("")
        t.append("A. AMBIL DI RAK (urut lokasi)")
        lok = None
        for a in daftar_ambil:
            if a["lokasi"] != lok:
                lok = a["lokasi"]
                t.append("[Rak %s]" % (lok or "tanpa lokasi"))
            t.append("  [ ] %-14s %-32s x %s %s (%d pesanan)" % (a["sku"], a["nama"][:32], fq(a["qty"]), a["satuan"], a["jumlah_pesanan"]))
        t.append("")
        t.append("B. URUTAN KEMAS / TEMPEL RESI (urut %s)" % args.urut)
        for u in urutan:
            isi = "; ".join("%s x%s" % (i["sku"], fq(i["qty"])) for i in u["item"])
            t.append("  %3d. [ ] %s | %s | resi %s | %s" % (u["urut"], u["no_pesanan"], u["kurir"] or "-", u["resi"] or "-", isi))
        if peringatan:
            t.append("")
            t.append("PERINGATAN:")
            t += ["  - " + x for x in peringatan]
    if args.csv:
        data["csv"] = tulis_csv(args.csv, ["lokasi", "sku", "nama", "qty", "satuan", "jumlah_pesanan"],
                                [[a["lokasi"], a["sku"], a["nama"], a["qty"], a["satuan"], a["jumlah_pesanan"]] for a in daftar_ambil],
                                args.pemisah)
        t.append("CSV daftar ambil: %s" % data["csv"])
    if args.csv_pesanan:
        rows = []
        for u in urutan:
            for i in u["item"]:
                rows.append([u["urut"], u["no_pesanan"], u["kurir"], u["resi"], u["batas_kirim"], i["sku"], i["nama"], i["qty"], i["lokasi"]])
        data["csv_pesanan"] = tulis_csv(args.csv_pesanan, ["urut", "no_pesanan", "kurir", "resi", "batas_kirim", "sku", "nama", "qty", "lokasi"],
                                        rows, args.pemisah)
        t.append("CSV urutan pesanan: %s" % data["csv_pesanan"])
    conn.close()
    if args.tandai_dikemas:
        if not ps:
            return data, "\n".join(t)

        def kerja(c2):
            c2.executemany("UPDATE pesanan SET dikemas=1, diubah=? WHERE id=?", [(sekarang(), i) for i in ids])
            d = dict(data)
            d["mode"] = None
            d["ditandai_dikemas"] = len(ids)
            d["ringkasan"] = {"tandai_dikemas": len(ids)}
            return d, "\n".join(t) + "\n\n%d pesanan akan ditandai SUDAH DIKEMAS (tidak muncul lagi di picking berikutnya)." % len(ids)

        return jalankan_tulis(args, db, "picking --tandai-dikemas", kerja)
    return data, "\n".join(t)


# ---------------------------------------------------------------------------
# Perintah: laporan
# ---------------------------------------------------------------------------

JENIS_JUAL = ("jual", "jual-mp")


def _status_stok(r):
    if r["stok"] < -EPS:
        return "MINUS"
    if r["stok"] <= EPS:
        return "HABIS"
    if r["stok_min"] > 0 and r["stok"] <= r["stok_min"] + EPS:
        return "MENIPIS"
    return "aman"


def _rata2_jual(conn, pid, acuan, hari=30):
    dari = (acuan - timedelta(days=hari - 1)).isoformat()
    q = conn.execute("SELECT COALESCE(SUM(-qty),0) FROM mutasi WHERE produk_id=? AND jenis IN ('jual','jual-mp') "
                     "AND dibatalkan=0 AND tanggal BETWEEN ? AND ?", (pid, dari, acuan.isoformat())).fetchone()[0]
    return max(q, 0) / hari


def lap_stok(conn, args):
    sql = "SELECT * FROM produk WHERE aktif=1"
    par = []
    if args.cari:
        sql += " AND (sku LIKE ? OR nama LIKE ? OR varian LIKE ? OR lokasi LIKE ?)"
        par = ["%" + args.cari + "%"] * 4
    rows = conn.execute(sql + " ORDER BY lokasi, sku", par).fetchall()
    out = []
    for r in rows:
        d = baris_produk_json(r)
        d["status"] = _status_stok(r)
        out.append(d)
    total = sum(d["nilai_persediaan"] for d in out)
    data = {"jumlah_produk": len(out), "total_qty": angka_json(sum(max(d["stok"], 0) for d in out)),
            "nilai_persediaan_total": total, "produk": out,
            "catatan": "Nilai persediaan = stok x HPP rata-rata tertimbang, dibulatkan ke rupiah terdekat. Stok minus dihitung 0."}
    t = ["STOK SAAT INI - %d produk, nilai persediaan %s" % (len(out), rp(total))]
    for d in out:
        t.append("- %s | %s%s | %s %s | HPP %s | nilai %s%s" % (
            d["lokasi"] or "-", d["sku"], (" " + d["nama"] + (" " + d["varian"] if d["varian"] else "")), fq(d["stok"]), d["satuan"],
            rp(d["hpp_rata2"]), rp(d["nilai_persediaan"]), "" if d["status"] == "aman" else "  <- " + d["status"]))
    head = ["lokasi", "sku", "nama", "varian", "satuan", "stok", "stok_min", "hpp_rata2", "nilai_persediaan", "harga_jual", "status"]
    rows_csv = [[d["lokasi"], d["sku"], d["nama"], d["varian"], d["satuan"], d["stok"], d["stok_min"], bulat_rp(d["hpp_rata2"]),
                 d["nilai_persediaan"], d["harga_jual"], d["status"]] for d in out]
    return data, t, head, rows_csv


def lap_menipis(conn, args):
    acuan = hari_ini(args)
    rows = conn.execute("SELECT * FROM produk WHERE aktif=1 AND (stok <= 0 OR (stok_min > 0 AND stok <= stok_min)) "
                        "ORDER BY stok - stok_min, sku").fetchall()
    out = []
    for r in rows:
        rata = _rata2_jual(conn, r["id"], acuan)
        d = {"sku": r["sku"], "nama": label_produk(r), "lokasi": r["lokasi"], "stok": angka_json(r["stok"]),
             "stok_min": angka_json(r["stok_min"]), "status": _status_stok(r),
             "kurang_dari_minimum": angka_json(max(r["stok_min"] - r["stok"], 0)),
             "rata2_terjual_per_hari_30h": round(rata, 2),
             "perkiraan_habis_hari": (int(max(r["stok"], 0) / rata) if rata > 0 else None),
             "harga_beli_terakhir": bulat_rp(r["harga_beli"])}
        out.append(d)
    data = {"jumlah": len(out), "produk": out, "tanggal_acuan": acuan.isoformat(),
            "catatan": "Menipis = stok <= stok minimum. Rata-rata terjual dihitung dari 30 hari terakhir."}
    t = ["STOK MENIPIS / HABIS - %d produk (acuan %s)" % (len(out), acuan.isoformat())]
    if not out:
        t.append("Semua stok di atas batas minimum.")
    for d in out:
        t.append("- %s %s: stok %s (min %s) %s%s" % (
            d["sku"], d["nama"], fq(d["stok"]), fq(d["stok_min"]), d["status"],
            (" | laku +-%s/hari, habis dalam +-%s hari" % (fq(d["rata2_terjual_per_hari_30h"]), d["perkiraan_habis_hari"]))
            if d["perkiraan_habis_hari"] is not None else ""))
    head = ["sku", "nama", "lokasi", "stok", "stok_min", "status", "kurang_dari_minimum", "rata2_per_hari", "perkiraan_habis_hari"]
    rows_csv = [[d["sku"], d["nama"], d["lokasi"], d["stok"], d["stok_min"], d["status"], d["kurang_dari_minimum"],
                 d["rata2_terjual_per_hari_30h"], d["perkiraan_habis_hari"] if d["perkiraan_habis_hari"] is not None else ""] for d in out]
    return data, t, head, rows_csv


def lap_tidak_laku(conn, args):
    acuan = hari_ini(args)
    batas = (acuan - timedelta(days=args.hari)).isoformat()
    rows = conn.execute(
        "SELECT p.*, (SELECT MAX(tanggal) FROM mutasi m WHERE m.produk_id=p.id AND m.jenis IN ('jual','jual-mp') AND m.dibatalkan=0) AS jual_terakhir, "
        "(SELECT MIN(tanggal) FROM mutasi m WHERE m.produk_id=p.id) AS pertama FROM produk p WHERE p.aktif=1 AND p.stok > 0").fetchall()
    out = []
    for r in rows:
        acuan_awal = r["jual_terakhir"] or r["pertama"]
        if acuan_awal is None or acuan_awal <= batas:
            umur = (acuan - date.fromisoformat(acuan_awal)).days if acuan_awal else None
            out.append({"sku": r["sku"], "nama": label_produk(r), "lokasi": r["lokasi"], "stok": angka_json(r["stok"]),
                        "jual_terakhir": r["jual_terakhir"], "hari_tanpa_penjualan": umur,
                        "nilai_tertahan": bulat_rp(r["stok"] * r["hpp"])})
    out.sort(key=lambda d: -d["nilai_tertahan"])
    total = sum(d["nilai_tertahan"] for d in out)
    data = {"hari": args.hari, "tanggal_acuan": acuan.isoformat(), "jumlah": len(out), "nilai_tertahan_total": total, "produk": out,
            "catatan": "Tidak laku = masih ada stok tetapi tidak ada penjualan selama N hari (produk baru dihitung sejak stok pertama masuk)."}
    t = ["BARANG TIDAK LAKU >= %d HARI - %d produk, modal tertahan %s" % (args.hari, len(out), rp(total))]
    for d in out:
        t.append("- %s %s: stok %s, terakhir laku %s, modal tertahan %s" % (
            d["sku"], d["nama"], fq(d["stok"]), d["jual_terakhir"] or "belum pernah", rp(d["nilai_tertahan"])))
    head = ["sku", "nama", "lokasi", "stok", "jual_terakhir", "hari_tanpa_penjualan", "nilai_tertahan"]
    rows_csv = [[d["sku"], d["nama"], d["lokasi"], d["stok"], d["jual_terakhir"] or "", d["hari_tanpa_penjualan"] or "", d["nilai_tertahan"]] for d in out]
    return data, t, head, rows_csv


def _periode(args):
    acuan = hari_ini(args)
    dari = tanggal_wajib(args.dari, "dari") if args.dari else acuan.replace(day=1)
    sampai = tanggal_wajib(args.sampai, "sampai") if args.sampai else acuan
    if sampai < dari:
        raise Gagal("Tanggal 'sampai' lebih awal dari 'dari'.")
    return dari, sampai


def lap_mutasi(conn, args):
    dari, sampai = _periode(args)
    par = [dari.isoformat(), sampai.isoformat()]
    filt = ""
    if args.sku:
        p = ambil_produk(conn, args.sku)
        filt = " AND m.produk_id=%d" % p["id"]
    rows = conn.execute("SELECT m.*, p.sku, p.nama, p.varian FROM mutasi m JOIN produk p ON p.id=m.produk_id "
                        "WHERE m.tanggal BETWEEN ? AND ?%s ORDER BY m.tanggal, m.id" % filt, par).fetchall()
    ringkas = {}
    prods = conn.execute("SELECT * FROM produk p WHERE 1=1%s" % filt.replace("m.produk_id", "p.id")).fetchall()
    for p in prods:
        sesudah = conn.execute("SELECT COALESCE(SUM(qty),0) FROM mutasi WHERE produk_id=? AND tanggal > ?", (p["id"], sampai.isoformat())).fetchone()[0]
        dalam = conn.execute("SELECT arah, COALESCE(SUM(qty),0) FROM mutasi WHERE produk_id=? AND tanggal BETWEEN ? AND ? GROUP BY arah",
                             (p["id"], par[0], par[1])).fetchall()
        d = {a: q for a, q in dalam}
        akhir = rapikan_qty(p["stok"] - sesudah)
        net = sum(d.values())
        if not dalam and not args.sku:
            continue
        ringkas[p["sku"]] = {"sku": p["sku"], "nama": label_produk(p), "awal": angka_json(akhir - net),
                             "masuk": angka_json(d.get("masuk", 0)), "keluar": angka_json(-d.get("keluar", 0)),
                             "opname": angka_json(d.get("opname", 0)), "akhir": angka_json(akhir)}
    detail = [{"tanggal": r["tanggal"], "sku": r["sku"], "arah": r["arah"], "jenis": r["jenis"], "qty": angka_json(r["qty"]),
               "harga": bulat_rp(r["harga"]) if r["harga"] is not None else None, "hpp": round(r["hpp"], 2),
               "stok_sesudah": angka_json(r["stok_sesudah"]), "ref": r["ref"], "catatan": r["catatan"]} for r in rows]
    # Penjualan milik pesanan yang kemudian batal (dibatalkan=1) tidak dihitung sebagai penjualan.
    jual = [r for r in rows if r["jenis"] in JENIS_JUAL and not r["dibatalkan"]]
    nilai_jual = sum(-r["qty"] * r["harga"] for r in jual if r["harga"] is not None)
    hpp_jual = sum(-r["qty"] * r["hpp"] for r in jual)
    hpp_batal = 0
    nilai_beli = sum(r["qty"] * r["harga"] for r in rows if r["arah"] == "masuk" and r["jenis"] == "beli")
    data = {"dari": dari.isoformat(), "sampai": sampai.isoformat(), "jumlah_mutasi": len(detail),
            "per_produk": list(ringkas.values()), "detail": detail if not args.ringkas_saja else [],
            "nilai_pembelian": bulat_rp(nilai_beli), "hpp_barang_terjual": bulat_rp(hpp_jual - hpp_batal),
            "nilai_penjualan_tercatat": bulat_rp(nilai_jual)}
    t = ["MUTASI STOK %s s/d %s - %d transaksi" % (dari.isoformat(), sampai.isoformat(), len(detail)),
         "Pembelian: %s | HPP barang terjual: %s | Penjualan tercatat (yang ada harganya): %s"
         % (rp(nilai_beli), rp(hpp_jual - hpp_batal), rp(nilai_jual)), "", "Per produk (awal + masuk - keluar +/- opname = akhir):"]
    for v in ringkas.values():
        t.append("- %s %s: %s + %s - %s %s = %s" % (v["sku"], v["nama"], fq(v["awal"]), fq(v["masuk"]), fq(v["keluar"]),
                                                  ("%+g" % v["opname"]).replace(".", ",") if v["opname"] else "+0", fq(v["akhir"])))
    if not args.ringkas_saja and detail:
        t.append("")
        t.append("Rincian:")
        for d in detail[:200]:
            t.append("  %s %-12s %-14s %6s  stok %s  %s %s" % (d["tanggal"], d["sku"], d["jenis"], fq(d["qty"]), fq(d["stok_sesudah"]), d["ref"], d["catatan"]))
        if len(detail) > 200:
            t.append("  ... %d baris lagi (pakai --csv untuk semua)" % (len(detail) - 200))
    head = ["tanggal", "sku", "arah", "jenis", "qty", "harga", "hpp", "stok_sesudah", "ref", "catatan"]
    rows_csv = [[d["tanggal"], d["sku"], d["arah"], d["jenis"], d["qty"], d["harga"] if d["harga"] is not None else "",
                 bulat_rp(d["hpp"]), d["stok_sesudah"], d["ref"], d["catatan"]] for d in detail]
    return data, t, head, rows_csv


def lap_ringkas(conn, args):
    acuan = tanggal_wajib(args.tanggal) if args.tanggal else hari_ini(args)
    a = acuan.isoformat()
    jual = conn.execute("SELECT m.*, p.sku FROM mutasi m JOIN produk p ON p.id=m.produk_id "
                        "WHERE m.tanggal=? AND m.jenis IN ('jual','jual-mp') AND m.dibatalkan=0", (a,)).fetchall()
    qty = sum(-r["qty"] for r in jual)
    qty_mp = sum(-r["qty"] for r in jual if r["jenis"] == "jual-mp")
    qty_toko = qty - qty_mp
    omzet = sum(-r["qty"] * r["harga"] for r in jual if r["harga"] is not None)
    hpp = sum(-r["qty"] * r["hpp"] for r in jual)
    tanpa_harga = sum(1 for r in jual if r["harga"] is None)
    top = {}
    for r in jual:
        top[r["sku"]] = top.get(r["sku"], 0) + (-r["qty"])
    top = sorted(top.items(), key=lambda x: -x[1])[:5]
    n_pesanan = conn.execute("SELECT COUNT(*) FROM pesanan WHERE tanggal=? AND dibatalkan=0", (a,)).fetchone()[0]
    belum = _pesanan_belum_kirim(conn)
    menipis, _, _, _ = lap_menipis(conn, argparse.Namespace(hari_ini=a))
    nilai = conn.execute("SELECT COALESCE(SUM(CASE WHEN stok>0 THEN stok*hpp ELSE 0 END),0) FROM produk WHERE aktif=1").fetchone()[0]
    masuk = conn.execute("SELECT COALESCE(SUM(qty),0), COALESCE(SUM(qty*harga),0) FROM mutasi WHERE tanggal=? AND jenis='beli'", (a,)).fetchone()
    opn = conn.execute("SELECT COUNT(*) FROM mutasi WHERE tanggal=? AND arah='opname'", (a,)).fetchone()[0]
    tl, _, _, _ = lap_tidak_laku(conn, argparse.Namespace(hari_ini=a, hari=args.hari))
    data = {"tanggal": a, "terjual_qty": angka_json(qty), "terjual_marketplace_qty": angka_json(qty_mp),
            "terjual_toko_qty": angka_json(qty_toko), "pesanan_marketplace_hari_ini": n_pesanan,
            "omzet_tercatat": bulat_rp(omzet), "hpp_terjual": bulat_rp(hpp),
            "laba_kotor_perkiraan": bulat_rp(omzet - sum(-r["qty"] * r["hpp"] for r in jual if r["harga"] is not None)),
            "baris_jual_tanpa_harga": tanpa_harga, "top_terjual": [{"sku": s, "qty": angka_json(q)} for s, q in top],
            "pesanan_belum_dikemas": len(belum), "restock_qty": angka_json(masuk[0]), "restock_nilai": bulat_rp(masuk[1]),
            "opname_selisih_hari_ini": opn, "stok_menipis": menipis["produk"], "nilai_persediaan": bulat_rp(nilai),
            "tidak_laku": {"hari": args.hari, "jumlah": tl["jumlah"], "nilai_tertahan": tl["nilai_tertahan_total"]},
            "catatan": "Pesanan yang batal setelah diimpor tidak dihitung. Omzet hanya dari transaksi yang punya harga jual; laba kotor = omzet - HPP rata-rata (sebelum biaya admin marketplace, ongkir, iklan)."}
    t = ["Laporan Stok Harian - %s" % acuan.strftime("%d/%m/%Y"),
         "Terjual: %s barang (marketplace %s dari %d pesanan, toko/offline %s)"
         % (fq(qty), fq(qty_mp), n_pesanan, fq(qty_toko)),
         "Omzet tercatat: %s | HPP: %s | Laba kotor (perkiraan): %s" % (rp(omzet), rp(hpp), rp(data["laba_kotor_perkiraan"]))]
    if tanpa_harga:
        t.append("(%d transaksi jual tanpa harga, tidak masuk omzet)" % tanpa_harga)
    if top:
        t.append("Terlaris: " + ", ".join("%s (%s)" % (s, fq(q)) for s, q in top))
    t.append("Pesanan belum dikemas: %d" % len(belum))
    if masuk[0]:
        t.append("Restock hari ini: %s barang (%s, termasuk ongkir/biaya tambahan)" % (fq(masuk[0]), rp(masuk[1])))
    t.append("Stok menipis/habis: %d produk" % len(menipis["produk"]))
    for d in menipis["produk"][:10]:
        t.append("  - %s %s: sisa %s (min %s)%s" % (d["sku"], d["nama"], fq(d["stok"]), fq(d["stok_min"]),
                                                  (", habis +-%s hari lagi" % d["perkiraan_habis_hari"]) if d["perkiraan_habis_hari"] is not None else ""))
    if len(menipis["produk"]) > 10:
        t.append("  ... dan %d lainnya" % (len(menipis["produk"]) - 10))
    t.append("Barang tidak laku >= %d hari: %d produk (modal tertahan %s)" % (args.hari, tl["jumlah"], rp(tl["nilai_tertahan_total"])))
    t.append("Nilai persediaan: %s" % rp(nilai))
    head = ["kunci", "nilai"]
    rows_csv = [[k, v] for k, v in data.items() if not isinstance(v, (list, dict))]
    return data, t, head, rows_csv


LAPORAN = {"stok": lap_stok, "menipis": lap_menipis, "tidak-laku": lap_tidak_laku, "mutasi": lap_mutasi, "ringkas": lap_ringkas}


def cmd_laporan(args):
    db = path_db(args)
    conn = buka(db)
    try:
        data, t, head, rows_csv = LAPORAN[args.jenis_laporan](conn, args)
    finally:
        conn.close()
    data = dict(ok=True, mode="baca", laporan=args.jenis_laporan, **data)
    if args.csv:
        data["csv"] = tulis_csv(args.csv, head, rows_csv, args.pemisah)
        t.append("File CSV (buka di Excel): %s" % data["csv"])
    return data, "\n".join(t)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def buat_parser():
    umum = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
    umum.add_argument("--db", help="Path file database (default ~/KomunitechData/stok.db atau ENV KOMUNITECH_STOK_DB)")
    umum.add_argument("--json", action="store_true", help="Output JSON (untuk dibaca agent)")
    umum.add_argument("--hari-ini", help=argparse.SUPPRESS)
    tulis = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
    tulis.add_argument("--ya", action="store_true", help="Simpan perubahan (tanpa ini hanya pratinjau)")

    p = argparse.ArgumentParser(prog="stok.py", description="buku-stok Komunitech - stok/inventori lokal (SQLite).", allow_abbrev=False)
    p.add_argument("--versi", action="version", version="buku-stok " + VERSI)
    sub = p.add_subparsers(dest="perintah", metavar="PERINTAH")
    sub.required = True

    s = sub.add_parser("init", parents=[umum, tulis], help="Buat database stok baru", allow_abbrev=False)
    s.set_defaults(fungsi=cmd_init)
    s = sub.add_parser("info", parents=[umum], help="Info database & backup", allow_abbrev=False)
    s.set_defaults(fungsi=cmd_info)

    s = sub.add_parser("produk", help="Tambah/ubah/cari/impor produk", allow_abbrev=False)
    ps = s.add_subparsers(dest="aksi", metavar="AKSI")
    ps.required = True
    a = ps.add_parser("tambah", parents=[umum, tulis], help="Tambah produk (SKU per varian)", allow_abbrev=False)
    a.add_argument("--sku", required=True)
    a.add_argument("--nama", required=True)
    a.add_argument("--varian", default="")
    a.add_argument("--satuan", default="pcs")
    a.add_argument("--harga-beli")
    a.add_argument("--harga-jual")
    a.add_argument("--stok-min")
    a.add_argument("--lokasi", default="", help="Lokasi rak, mis. A1")
    a.add_argument("--stok-awal", help="Stok awal (dicatat sebagai saldo awal dengan harga beli)")
    a.add_argument("--tanggal")
    a.set_defaults(fungsi=cmd_produk_tambah)
    a = ps.add_parser("ubah", parents=[umum, tulis], help="Ubah data produk", allow_abbrev=False)
    a.add_argument("--sku", required=True)
    for f in ("nama", "varian", "satuan", "lokasi", "harga-beli", "harga-jual", "stok-min", "sku-baru", "koreksi-hpp"):
        a.add_argument("--" + f)
    a.add_argument("--nonaktif", action="store_true")
    a.add_argument("--aktif", action="store_true")
    a.set_defaults(fungsi=cmd_produk_ubah)
    a = ps.add_parser("cari", parents=[umum], help="Cari produk (kosong = semua)", allow_abbrev=False)
    a.add_argument("kata", nargs="?", default="")
    a.add_argument("--semua", action="store_true", help="Termasuk produk nonaktif")
    a.set_defaults(fungsi=cmd_produk_cari)
    a = ps.add_parser("impor", parents=[umum, tulis], help="Impor daftar produk dari CSV/XLSX", allow_abbrev=False)
    a.add_argument("file")
    a.add_argument("--tanggal")
    a.set_defaults(fungsi=cmd_produk_impor)

    for nama, fungsi, pilihan, bantuan in (
            ("masuk", cmd_masuk, ["beli", "retur-pembeli", "saldo-awal", "lainnya"], "Barang masuk (pembelian/restock)"),
            ("keluar", cmd_keluar, ["jual", "retur-supplier", "rusak", "hilang", "pakai-sendiri", "lainnya"], "Barang keluar")):
        s = sub.add_parser(nama, parents=[umum, tulis], help=bantuan, allow_abbrev=False)
        s.add_argument("--sku")
        s.add_argument("--qty")
        s.add_argument("--harga", help="Harga per satuan (masuk: harga beli; keluar jual: harga jual)")
        s.add_argument("--file", help="CSV berisi banyak item: kolom SKU, Qty, Harga (opsional)")
        s.add_argument("--jenis", choices=pilihan, default=pilihan[0])
        s.add_argument("--tanggal")
        s.add_argument("--ref", default="", help="No. nota/faktur/pesanan")
        s.add_argument("--catatan", default="")
        if nama == "masuk":
            s.add_argument("--biaya-tambahan", help="Ongkir/biaya kulakan total, dibagi ke item sesuai nilai")
            s.add_argument("--perbarui-harga-beli", action="store_true", default=True, help=argparse.SUPPRESS)
        else:
            s.add_argument("--izinkan-minus", action="store_true", help="Izinkan stok menjadi minus (tetap diberi peringatan)")
        s.set_defaults(fungsi=fungsi)

    s = sub.add_parser("opname", parents=[umum, tulis], help="Stock opname: hitung fisik -> selisih -> penyesuaian", allow_abbrev=False)
    s.add_argument("--hitung", action="append", help="SKU=jumlah fisik (boleh berulang)")
    s.add_argument("--file", help="CSV hasil hitung: kolom SKU, Fisik, Alasan (opsional)")
    s.add_argument("--alasan", help="Alasan selisih untuk semua baris yang tidak punya alasan sendiri")
    s.add_argument("--tanggal")
    s.add_argument("--ref", default="")
    s.set_defaults(fungsi=cmd_opname)

    s = sub.add_parser("impor-pesanan", parents=[umum, tulis], help="Impor file pesanan Shopee/TikTok Shop/Tokopedia", allow_abbrev=False)
    s.add_argument("file")
    s.add_argument("--platform", choices=["shopee", "tiktok", "tokopedia", "lainnya"])
    for f in SINONIM_PESANAN:
        s.add_argument("--kolom-" + f.replace("_", "-"), dest="kolom_" + f,
                       help="Nama kolom untuk %s ('-' = abaikan)" % LABEL_FIELD[f])
    s.add_argument("--abaikan-status", help="Kata status yang dianggap batal (mengganti daftar bawaan), pisahkan koma")
    s.add_argument("--lewati-tak-dikenal", action="store_true", help="Tetap impor walau ada SKU belum terdaftar")
    s.set_defaults(fungsi=cmd_impor_pesanan)

    s = sub.add_parser("picking", parents=[umum, tulis], help="Daftar ambil barang & urutan resi dari pesanan belum dikirim", allow_abbrev=False)
    s.add_argument("--platform")
    s.add_argument("--urut", choices=["kurir", "resi", "batas", "pesanan"], default="kurir")
    s.add_argument("--csv")
    s.add_argument("--csv-pesanan")
    s.add_argument("--pemisah", default=";")
    s.add_argument("--tandai-dikemas", action="store_true", help="Tandai semua pesanan di daftar sebagai sudah dikemas")
    s.set_defaults(fungsi=cmd_picking)

    s = sub.add_parser("laporan", parents=[umum], help="Laporan stok", allow_abbrev=False)
    s.add_argument("jenis_laporan", choices=list(LAPORAN))
    s.add_argument("--cari")
    s.add_argument("--hari", type=int, default=30, help="Batas hari untuk laporan tidak-laku (default 30)")
    s.add_argument("--dari")
    s.add_argument("--sampai")
    s.add_argument("--sku")
    s.add_argument("--tanggal")
    s.add_argument("--ringkas-saja", action="store_true")
    s.add_argument("--csv", help="Simpan juga sebagai CSV (untuk Excel)")
    s.add_argument("--pemisah", default=";", help="Pemisah CSV: ';' (Excel Indonesia, default) atau ','")
    s.set_defaults(fungsi=cmd_laporan)

    s = sub.add_parser("backup", parents=[umum], help="Buat salinan database bertanggal", allow_abbrev=False)
    s.add_argument("--label")
    s.add_argument("--daftar", action="store_true", help="Tampilkan daftar backup")
    s.set_defaults(fungsi=cmd_backup)
    s = sub.add_parser("restore", parents=[umum, tulis], help="Pulihkan database dari file backup", allow_abbrev=False)
    s.add_argument("--dari", required=True)
    s.set_defaults(fungsi=cmd_restore)
    return p


def main(argv=None):
    try:
        sys.stdout.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass
    parser = buat_parser()
    args = parser.parse_args(argv)
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
            for k, v in e.detail.items():
                print("  %s: %s" % (k, v), file=sys.stderr)
        return 1
    except sqlite3.OperationalError as e:
        pesan = "Database sedang dipakai proses lain atau terkunci (%s). Coba lagi sebentar." % e \
            if "locked" in str(e) else "Kesalahan database: %s" % e
        if args.json:
            print(json.dumps({"ok": False, "error": pesan}, ensure_ascii=False))
        else:
            print("GAGAL: " + pesan, file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(data, ensure_ascii=False, indent=2, default=str))
    else:
        print(teks)
    return 0


if __name__ == "__main__":
    sys.exit(main())
