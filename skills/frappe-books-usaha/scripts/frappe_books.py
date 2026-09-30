#!/usr/bin/env python3
"""frappe_books.py - asisten Frappe Books untuk UMKM (Komunitech).

Karya orisinal Komunitech. Tidak berafiliasi dengan Frappe Technologies / proyek Frappe Books.
Hanya Python standar. Uang dihitung dengan Decimal.

Perintah:
  cek            periksa file database Frappe Books (read-only)
  akun           daftar akun, satuan (UOM), pajak, dan lokasi yang ada
  penjualan      ringkasan penjualan per periode
  pembelian      ringkasan pembelian per periode
  piutang        invoice penjualan belum lunas + umur
  utang          invoice pembelian belum lunas + umur
  stok           jumlah stok per barang (barang yang dilacak stoknya)
  laba-rugi      laba rugi ringkas per periode (dari buku besar)
  laporan-harian ringkasan satu hari (untuk jadwal Telegram)
  ppn            hitung PPN 12% dengan DPP nilai lain 11/12
  csv-pelanggan  ubah daftar pelanggan/pemasok biasa -> CSV Import Wizard (Party)
  csv-barang     ubah daftar barang biasa -> CSV Import Wizard (Item)
  csv-transaksi  ubah daftar nota biasa -> CSV Import Wizard (SalesInvoice/PurchaseInvoice)

Database SELALU dibuka read-only (sqlite3 URI mode=ro + PRAGMA query_only).
Script ini tidak pernah menulis ke database Frappe Books.

Kode keluar: 0 berhasil, 2 input salah/kurang, 3 file tidak bisa dibuka / bukan Frappe Books,
4 skema tidak sesuai versi yang didukung, 5 data CSV tidak lolos validasi.
"""
import argparse
import csv
import io
import os
import re
import sqlite3
import sys
from datetime import date, datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation, ROUND_FLOOR, ROUND_HALF_UP
from pathlib import Path

VERSI = "1.0.6"
VERSI_DIUJI = "Frappe Books v0.36.0 (skema juga dicocokkan dengan cabang main 0.37.0, 20 Sep 2026)"
ZONA = {"WIB": 7, "WITA": 8, "WIT": 9}
NOL = Decimal(0)
BULAN = ["", "Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
BULAN_PANJANG = {"januari": 1, "februari": 2, "maret": 3, "april": 4, "mei": 5, "juni": 6, "juli": 7,
                 "agustus": 8, "september": 9, "oktober": 10, "november": 11, "desember": 12,
                 "jan": 1, "feb": 2, "mar": 3, "apr": 4, "jun": 6, "jul": 7, "agu": 8, "agt": 8,
                 "ags": 8, "aug": 8, "sep": 9, "sept": 9, "okt": 10, "oct": 10, "nov": 11, "des": 12,
                 "dec": 12, "may": 5}

# Tabel & kolom yang dibaca (diverifikasi dari schemas/ di github.com/frappe/books v0.36.0)
SKEMA_WAJIB = {
    "Account": ["name", "rootType", "accountType", "isGroup"],
    "Party": ["name", "role", "outstandingAmount"],
    "Item": ["name", "trackItem", "unit", "rate"],
    "SalesInvoice": ["name", "party", "date", "netTotal", "grandTotal", "baseGrandTotal",
                     "outstandingAmount", "exchangeRate", "submitted", "cancelled", "returnAgainst"],
    "PurchaseInvoice": ["name", "party", "date", "netTotal", "grandTotal", "baseGrandTotal",
                        "outstandingAmount", "exchangeRate", "submitted", "cancelled", "returnAgainst"],
    "SalesInvoiceItem": ["item", "quantity", "amount", "parent"],
    "TaxSummary": ["account", "rate", "amount", "parent", "parentSchemaName"],
    "AccountingLedgerEntry": ["date", "account", "debit", "credit", "reverted"],
    "StockLedgerEntry": ["date", "item", "location", "quantity"],
    "SingleValue": ["parent", "fieldname", "value"],
}


class Gagal(Exception):
    def __init__(self, pesan, saran="", kode=2):
        super().__init__(pesan)
        self.pesan = pesan
        self.saran = saran
        self.kode = kode


# ---------------------------------------------------------------- uang & angka
def uang(v):
    """Nilai Currency Frappe Books (teks, mis. '85000.00000000000') -> Decimal."""
    if v is None or v == "":
        return NOL
    try:
        return Decimal(str(v).strip())
    except InvalidOperation:
        return NOL


def rupiah_bulat(d):
    return Decimal(d).quantize(Decimal(1), ROUND_HALF_UP)


def rp(d):
    d = rupiah_bulat(d)
    tanda = "-" if d < 0 else ""
    return f"{tanda}Rp {abs(int(d)):,}".replace(",", ".")


def angka(d):
    d = Decimal(d)
    if d == d.to_integral_value():
        return f"{int(d):,}".replace(",", ".")
    s = f"{d.normalize():f}"
    bulat, pecahan = s.split(".")
    return f"{int(bulat):,}".replace(",", ".") + "," + pecahan


def ppn_dari_dpp(dpp):
    """Standar Komunitech: PPN = DPP x 11/12 x 12% dihitung persis, dibulatkan ke bawah sekali."""
    dpp = Decimal(dpp)
    dpp_lain = dpp * Decimal(11) / Decimal(12)
    tepat = dpp * Decimal(11) / Decimal(100)
    return dpp_lain, tepat, tepat.quantize(Decimal(1), ROUND_FLOOR)


def dpp_dari_harga_termasuk(harga):
    """DPP = rupiah bulat terbesar dengan DPP + PPN <= harga (standar pembulatan Komunitech)."""
    harga = Decimal(harga)
    d = (harga * 100 / Decimal(111)).quantize(Decimal(1), ROUND_FLOOR)
    while d > 0 and d + ppn_dari_dpp(d)[2] > harga:
        d -= 1
    while (d + 1) + ppn_dari_dpp(d + 1)[2] <= harga:
        d += 1
    return d


def baca_rupiah(teks, label="nilai"):
    """Terima '85000', 'Rp 85.000', '85.000,50', '85rb', '1,5 jt', '1.5jt'. Tolak yang ambigu."""
    if teks is None:
        raise ValueError(f"{label} kosong")
    s = str(teks).strip().lower().replace("rp", "").replace("idr", "").replace(" ", "")
    s = re.sub(r"[.,]-$", "", s)
    if s == "":
        raise ValueError(f"{label} kosong")
    kali = Decimal(1)
    for akhiran, k in (("juta", 10**6), ("jt", 10**6), ("ribu", 1000), ("rb", 1000), ("k", 1000)):
        if s.endswith(akhiran):
            s = s[: -len(akhiran)]
            kali = Decimal(k)
            break
    negatif = s.startswith("-")
    s = s.lstrip("-")
    if not re.fullmatch(r"[0-9.,]+", s or "x"):
        raise ValueError(f"{label} '{teks}' bukan angka")
    if "." in s and "," in s:
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    elif "," in s:
        bagian = s.split(",")
        if len(bagian) == 2 and len(bagian[1]) == 3 and kali == 1:
            raise ValueError(f"{label} '{teks}' ambigu (koma bisa berarti ribuan atau desimal); "
                             "tulis tanpa pemisah, mis. 85000")
        if len(bagian) > 2:
            raise ValueError(f"{label} '{teks}' tidak jelas")
        s = s.replace(",", ".")
    elif "." in s:
        bagian = s.split(".")
        if len(bagian) > 2 or (len(bagian) == 2 and len(bagian[1]) == 3 and kali == 1):
            if all(len(b) == 3 for b in bagian[1:]) and bagian[0]:
                s = s.replace(".", "")
            else:
                raise ValueError(f"{label} '{teks}' tidak jelas")
    try:
        nilai = Decimal(s) * kali
    except InvalidOperation:
        raise ValueError(f"{label} '{teks}' bukan angka")
    return -nilai if negatif else nilai


def baca_jumlah(teks, label="jumlah"):
    """Jumlah barang: '3', '1,5' (desimal koma), '2.5' (desimal titik), '1.500' / '1.250.000' (titik
    ribuan), '1.500,5'. Bentuk ambigu ('1,500': 1,5 atau 1500?) dan format Inggris ditolak."""
    s = str(teks or "").strip().replace(" ", "").replace("\u00a0", "")
    if s == "":
        raise ValueError(f"{label} kosong")
    v = s.lstrip("-")
    if re.fullmatch(r"\d+", v):
        pass
    elif re.fullmatch(r"[1-9]\d{0,2}(\.\d{3})+(,\d+)?", v):          # 1.500 / 1.250.000 / 1.500,5
        s = s.replace(".", "").replace(",", ".")
    elif re.fullmatch(r"[1-9]\d{0,2},\d{3}", v):                      # 1,500 -> ragu
        raise ValueError(f"{label} '{teks}' ambigu (1,5 atau 1500?); tulis 1500 atau 1,5")
    elif re.fullmatch(r"\d+,\d+", v):                                  # 1,5
        s = s.replace(",", ".")
    elif re.fullmatch(r"\d+\.\d+", v):                                # 2.5 / 0.500 / 1500.5
        pass
    else:
        raise ValueError(f"{label} '{teks}' bukan angka (contoh: 3, 1,5, atau 1.500)")
    try:
        return Decimal(s)
    except InvalidOperation:
        raise ValueError(f"{label} '{teks}' bukan angka")


# ---------------------------------------------------------------- tanggal
def offset_zona(nama):
    nama = (nama or "WIB").upper()
    if nama not in ZONA:
        raise Gagal(f"Zona waktu '{nama}' tidak dikenal.", "Pakai WIB, WITA, atau WIT.")
    return timezone(timedelta(hours=ZONA[nama]))


def tanggal_lokal(nilai, tz):
    """Kolom Datetime Frappe Books disimpan ISO UTC ('2026-08-31T17:00:00.000Z').
    Ubah ke tanggal lokal (WIB/WITA/WIT). Nilai tanpa jam dianggap sudah tanggal lokal."""
    if nilai is None:
        return None
    s = str(nilai).strip()
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})(?:[T ](\d{2}):(\d{2})(?::(\d{2})(?:\.\d+)?)?)?\s*(Z|[+-]\d{2}:?\d{2})?$", s)
    if not m:
        return None
    y, mo, d, hh, mi, ss, zona = m.groups()
    if hh is None:
        return date(int(y), int(mo), int(d))
    dt = datetime(int(y), int(mo), int(d), int(hh), int(mi), int(ss or 0))
    if zona in (None, "Z"):
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        tanda = 1 if zona[0] == "+" else -1
        z = zona[1:].replace(":", "")
        dt = dt.replace(tzinfo=timezone(tanda * timedelta(hours=int(z[:2]), minutes=int(z[2:]))))
    return dt.astimezone(tz).date()


def hari_ini(args, tz):
    if getattr(args, "hari_ini", None):
        return parse_tanggal_tegas(args.hari_ini, "--hari-ini")
    return datetime.now(timezone.utc).astimezone(tz).date()


def parse_tanggal_tegas(s, label="tanggal"):
    try:
        return datetime.strptime(s.strip(), "%Y-%m-%d").date()
    except (ValueError, AttributeError):
        raise Gagal(f"{label} '{s}' tidak dikenali.", "Tulis dengan format TAHUN-BULAN-TANGGAL, mis. 2026-09-01.")


def parse_tanggal_awam(s):
    """Untuk CSV: 2026-09-01, 01/09/2026, 1-9-2026, 1 Sep 2026, 1 September 2026. Hari dulu (gaya Indonesia)."""
    t = str(s or "").strip()
    if not t:
        raise ValueError("tanggal kosong")
    m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", t)
    if m:
        y, mo, d = map(int, m.groups())
    else:
        m = re.fullmatch(r"(\d{1,2})[/\-.](\d{1,2})[/\-.](\d{2,4})", t)
        if m:
            d, mo, y = map(int, m.groups())
            if y < 100:
                y += 2000
        else:
            m = re.fullmatch(r"(\d{1,2})\s+([A-Za-z]+)\.?\s+(\d{4})", t)
            if not m or m.group(2).lower() not in BULAN_PANJANG:
                raise ValueError(f"tanggal '{t}' tidak dikenali (pakai mis. 01/09/2026 atau 2026-09-01)")
            d, mo, y = int(m.group(1)), BULAN_PANJANG[m.group(2).lower()], int(m.group(3))
    try:
        return date(y, mo, d)
    except ValueError:
        raise ValueError(f"tanggal '{t}' tidak ada di kalender")


def tgl_id(d):
    return f"{d.day} {BULAN[d.month]} {d.year}"


def periode(args, tz, bawaan="bulan-ini"):
    """Kembalikan (dari, sampai, label)."""
    kini = hari_ini(args, tz)
    if getattr(args, "tanggal", None):
        t = args.tanggal.lower()
        d = kini if t in ("hari-ini", "hariini", "today") else \
            kini - timedelta(days=1) if t in ("kemarin", "yesterday") else parse_tanggal_tegas(t)
        return d, d, tgl_id(d)
    if getattr(args, "dari", None) or getattr(args, "sampai", None):
        if not (args.dari and args.sampai):
            raise Gagal("--dari dan --sampai harus diisi keduanya.", "Contoh: --dari 2026-09-01 --sampai 2026-09-30")
        a, b = parse_tanggal_tegas(args.dari, "--dari"), parse_tanggal_tegas(args.sampai, "--sampai")
        if a > b:
            raise Gagal("Tanggal --dari lebih besar dari --sampai.", "Tukar urutannya.")
        return a, b, f"{tgl_id(a)} s.d. {tgl_id(b)}"
    bulan = (getattr(args, "bulan", None) or bawaan).lower()
    if bulan in ("ini", "bulan-ini"):
        y, m = kini.year, kini.month
    elif bulan in ("lalu", "bulan-lalu"):
        y, m = (kini.year, kini.month - 1) if kini.month > 1 else (kini.year - 1, 12)
    else:
        mm = re.fullmatch(r"(\d{4})-(\d{1,2})", bulan)
        if not mm or not 1 <= int(mm.group(2)) <= 12:
            raise Gagal(f"--bulan '{bulan}' tidak dikenali.", "Pakai 'ini', 'lalu', atau TAHUN-BULAN mis. 2026-09.")
        y, m = int(mm.group(1)), int(mm.group(2))
    awal = date(y, m, 1)
    akhir = (date(y + (m == 12), m % 12 + 1, 1) - timedelta(days=1))
    return awal, akhir, f"{BULAN[m]} {y} ({tgl_id(awal)} s.d. {tgl_id(akhir)})"


# ---------------------------------------------------------------- database
def lokasi_bawaan():
    """Frappe Books: app.getPath('documents')/Frappe Books. Di Linux tanpa folder Documents (XDG) = folder rumah;
    di Windows Documents sering dipindah ke OneDrive."""
    rumah = Path.home()
    akar = [rumah / "Documents" / "Frappe Books", rumah / "Dokumen" / "Frappe Books", rumah / "Frappe Books",
            rumah / "OneDrive" / "Documents" / "Frappe Books", rumah / "OneDrive" / "Dokumen" / "Frappe Books"]
    od = os.environ.get("OneDrive")
    if od:
        akar += [Path(od) / "Documents" / "Frappe Books", Path(od) / "Dokumen" / "Frappe Books"]
    return akar


def cari_db_bawaan():
    env = os.environ.get("FRAPPE_BOOKS_DB")
    if env:
        return env
    kandidat = []
    for akar in lokasi_bawaan():
        if akar.is_dir():
            for k in sorted(akar.glob("*.books.db")):
                if k.resolve() not in [x.resolve() for x in kandidat]:
                    kandidat.append(k)
    if len(kandidat) == 1:
        return str(kandidat[0])
    if len(kandidat) > 1:
        daftar = "\n".join(f"  - {k}" for k in kandidat)
        raise Gagal("Ada beberapa file Frappe Books:\n" + daftar,
                    "Sebutkan yang mana dengan --db \"<path lengkap>\".")
    raise Gagal("Lokasi file database Frappe Books belum diketahui.",
                "Cari file berakhiran .books.db (bawaan: folder Documents/Frappe Books/, atau ~/Frappe Books/ di Linux, "
                "atau OneDrive/Documents/Frappe Books/ di Windows; juga tampil di layar awal Frappe Books), lalu pakai --db \"<path lengkap>\".")


def buka_db(path):
    if not path:
        path = cari_db_bawaan()
    p = Path(os.path.expanduser(path))
    if not p.is_file():
        raise Gagal(f"File '{path}' tidak ditemukan.",
                    "Periksa lokasi file .books.db (bawaan: folder Documents/Frappe Books; juga tampil di layar awal Frappe Books).",
                    kode=3)
    uri = p.resolve().as_uri() + "?mode=ro"
    try:
        con = sqlite3.connect(uri, uri=True, timeout=5)
        con.execute("PRAGMA query_only = ON")
        con.row_factory = sqlite3.Row
        tabel = {r[0] for r in con.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    except sqlite3.DatabaseError as e:
        raise Gagal(f"'{p.name}' tidak bisa dibuka sebagai database Frappe Books ({pesan_sqlite(e)}).",
                    "Pastikan file-nya benar .books.db dan tidak rusak. Bila Frappe Books sedang menyimpan, "
                    "tunggu sebentar lalu coba lagi.", kode=3)
    if not {"SalesInvoice", "Account", "SingleValue"} <= tabel:
        con.close()
        raise Gagal(f"'{p.name}' bukan database Frappe Books (tabel SalesInvoice/Account tidak ada).",
                    "Pilih file berakhiran .books.db yang dibuat Frappe Books.", kode=3)
    return con, tabel


def pesan_sqlite(e):
    s = str(e).lower()
    if "locked" in s or "busy" in s:
        return "file sedang dikunci program lain"
    if "not a database" in s or "malformed" in s or "encrypted" in s:
        return "isi file bukan database SQLite yang utuh"
    if "unable to open" in s:
        return "file tidak bisa dibuka (izin akses?)"
    return "galat SQLite"


def kolom_tabel(con, tabel):
    return {r[1] for r in con.execute(f'PRAGMA table_info("{tabel}")')}


def cek_skema(con, tabel_ada, perlu):
    kurang = []
    for t in perlu:
        if t not in tabel_ada:
            kurang.append(f"tabel {t}")
            continue
        ada = kolom_tabel(con, t)
        kurang += [f"{t}.{k}" for k in SKEMA_WAJIB.get(t, []) if k not in ada]
    if kurang:
        raise Gagal("Struktur database berbeda dari versi Frappe Books yang didukung (kurang: "
                    + ", ".join(kurang) + ").",
                    f"Skill ini diuji dengan {VERSI_DIUJI}. Laporkan versi Frappe Books Anda ke Komunitech; "
                    "sementara itu pakai laporan bawaan di Frappe Books.", kode=4)


def q(con, sql, par=()):
    try:
        return con.execute(sql, par).fetchall()
    except sqlite3.DatabaseError as e:
        raise Gagal(f"Gagal membaca database ({pesan_sqlite(e)}).",
                    "Tutup dialog yang sedang menyimpan di Frappe Books lalu coba lagi.", kode=3)


def single(con, parent, field):
    r = q(con, "SELECT value FROM SingleValue WHERE parent=? AND fieldname=?", (parent, field))
    return r[0]["value"] if r else None


def centang(v):
    """Nilai Check di SingleValue: file asli v0.36.0 menyimpan '1.0'/'0.0'; terima juga 1, '1', 'true'."""
    if v is None:
        return False
    t = str(v).strip().lower()
    if t in ("true", "yes"):
        return True
    try:
        return Decimal(t) != 0
    except InvalidOperation:
        return False


def info_usaha(con):
    return {
        "nama": single(con, "AccountingSettings", "companyName") or "(nama usaha belum diisi)",
        "mata_uang": single(con, "SystemSettings", "currency") or "?",
        "versi": single(con, "SystemSettings", "version") or "?",
        "inventori": centang(single(con, "AccountingSettings", "enableInventory")),
    }


def cek_mata_uang(info):
    if info["mata_uang"] not in ("IDR", "?"):
        return f"Catatan: mata uang utama usaha ini {info['mata_uang']}, bukan IDR; angka 'Rp' di bawah = {info['mata_uang']}."
    return ""


def samarkan(nama):
    bagian = [re.sub(r"[\W_]+", "", b) for b in re.split(r"[\s(),./&-]+", nama or "")]
    return " ".join(b[0].upper() + "." for b in bagian if b) or "?"


def muat_invoice(con, jenis, tz):
    rows = q(con, f'SELECT name, party, date, netTotal, grandTotal, baseGrandTotal, outstandingAmount, '
                  f'exchangeRate, submitted, cancelled, returnAgainst FROM "{jenis}"')
    hasil = []
    for r in rows:
        kurs = Decimal(str(r["exchangeRate"] or 1)) or Decimal(1)
        hasil.append({
            "no": r["name"], "pihak": r["party"] or "?", "tgl": tanggal_lokal(r["date"], tz),
            "dpp": uang(r["netTotal"]) * kurs, "total": uang(r["baseGrandTotal"]) if r["baseGrandTotal"] not in (None, "") else uang(r["grandTotal"]) * kurs,
            "sisa": uang(r["outstandingAmount"]), "final": bool(r["submitted"]), "batal": bool(r["cancelled"]),
            "retur": bool(r["returnAgainst"]), "retur_atas": r["returnAgainst"] or "", "kurs": kurs,
        })
    return hasil


def pajak_per_invoice(con, jenis):
    hasil = {}
    for r in q(con, "SELECT parent, amount FROM TaxSummary WHERE parentSchemaName=?", (jenis,)):
        hasil[r["parent"]] = hasil.get(r["parent"], NOL) + uang(r["amount"])
    return hasil


# ---------------------------------------------------------------- perintah baca
def cmd_cek(args):
    con, tabel = buka_db(args.db)
    info = info_usaha(con)
    out = [f"FRAPPE BOOKS TERBACA (read-only): {info['nama']}",
           f"Versi data Frappe Books: {info['versi']} | Mata uang: {info['mata_uang']} | "
           f"Fitur stok (Inventory): {'aktif' if info['inventori'] else 'tidak aktif'}"]
    for t, label in (("Party", "pelanggan/pemasok"), ("Item", "barang/jasa"), ("SalesInvoice", "invoice penjualan"),
                     ("PurchaseInvoice", "invoice pembelian"), ("Account", "akun")):
        if t in tabel:
            n = q(con, f'SELECT COUNT(*) AS n FROM "{t}"')[0]["n"]
            out.append(f"- {label}: {n}")
    try:
        cek_skema(con, tabel, list(SKEMA_WAJIB))
        out.append(f"Struktur cocok dengan versi yang diuji ({VERSI_DIUJI}).")
    except Gagal as g:
        out.append("PERINGATAN: " + g.pesan)
    if info["versi"] not in ("?",) and not str(info["versi"]).startswith(("0.36", "0.37")):
        out.append(f"Catatan: versi {info['versi']} belum diuji Komunitech; periksa angka dengan laporan di Frappe Books.")
    catatan = cek_mata_uang(info)
    if catatan:
        out.append(catatan)
    print("\n".join(out))


def cmd_akun(args):
    con, tabel = buka_db(args.db)
    cek_skema(con, tabel, ["Account"])
    out = ["AKUN (bukan grup) - pakai nama PERSIS seperti di bawah untuk CSV:"]
    urut = {"Asset": 1, "Liability": 2, "Equity": 3, "Income": 4, "Expense": 5}
    label = {"Asset": "Aset", "Liability": "Kewajiban", "Equity": "Modal", "Income": "Pendapatan", "Expense": "Beban"}
    rows = q(con, "SELECT name, rootType, accountType FROM Account WHERE isGroup = 0 OR isGroup IS NULL")
    for r in sorted(rows, key=lambda r: (urut.get(r["rootType"], 9), r["name"])):
        jenis = f" [{r['accountType']}]" if r["accountType"] else ""
        out.append(f"- {r['name']} ({label.get(r['rootType'], r['rootType'])}){jenis}")
    for t, judul in (("UOM", "SATUAN (UOM)"), ("Location", "LOKASI GUDANG")):
        if t in tabel:
            nama = [r["name"] for r in q(con, f'SELECT name FROM "{t}" ORDER BY name')]
            out.append(f"{judul}: " + (", ".join(nama) if nama else "(kosong)"))
    if "Tax" in tabel and "TaxDetail" in tabel:
        out.append("PAJAK (template Tax):")
        pajak = q(con, "SELECT t.name AS nama, d.rate AS tarif, d.account AS akun FROM Tax t "
                       "LEFT JOIN TaxDetail d ON d.parent = t.name ORDER BY t.name")
        if not pajak:
            out.append("- (belum ada)")
        for r in pajak:
            out.append(f"- {r['nama']}: {angka(Decimal(str(r['tarif'] or 0)))}% ke akun {r['akun']}")
            if r["tarif"] is not None and Decimal(str(r["tarif"])) == 12:
                out.append("  PERHATIAN: tarif 12% dari harga penuh = PPN terlalu besar untuk barang/jasa non-mewah. "
                           "Umumnya pakai 11% (= 12% x DPP 11/12). Lihat references/ppn-frappe-books.md.")
    print("\n".join(out))


def ringkas_invoice(args, jenis, judul, kata_pihak):
    tz = offset_zona(args.tz)
    con, tabel = buka_db(args.db)
    perlu = [jenis, "TaxSummary", "SingleValue"] + (["SalesInvoiceItem"] if args.per == "barang" and jenis == "SalesInvoice" else [])
    if args.per == "barang" and jenis == "PurchaseInvoice":
        perlu.append("PurchaseInvoiceItem")
    cek_skema(con, tabel, perlu)
    info = info_usaha(con)
    dari, sampai, label = periode(args, tz)
    semua = [i for i in muat_invoice(con, jenis, tz) if i["tgl"] and dari <= i["tgl"] <= sampai]
    final = [i for i in semua if i["final"] and not i["batal"]]
    draf = [i for i in semua if not i["final"] and not i["batal"]]
    batal = [i for i in semua if i["batal"]]
    pajak = pajak_per_invoice(con, jenis)
    dpp = sum((i["dpp"] for i in final), NOL)
    tax = sum((pajak.get(i["no"], NOL) * i["kurs"] for i in final), NOL)
    total = sum((i["total"] for i in final), NOL)
    # Sama dengan 'piutang': retur yang belum dikembalikan tersimpan sebagai sisa NEGATIF (kredit) dan ikut dihitung.
    sisa = sum((i["sisa"] for i in final), NOL)
    kredit_retur = sum((i["sisa"] for i in final if i["sisa"] < 0), NOL)
    selisih = dpp + tax - total
    out = [f"{judul} - {info['nama']}", f"Periode: {label}, zona {args.tz.upper()}",
           f"Invoice final: {len(final)}" + (f" (termasuk {sum(1 for i in final if i['retur'])} retur)" if any(i['retur'] for i in final) else "")
           + f" | draf belum final: {len(draf)} (tidak dihitung) | dibatalkan: {len(batal)} (tidak dihitung)"]
    if not final:
        out.append(f"Belum ada invoice {kata_pihak.lower()} final di periode ini.")
    else:
        out += [f"DPP / sebelum pajak : {rp(dpp)}", f"Pajak               : {rp(tax)}"]
        if rupiah_bulat(selisih) != 0:
            out.append(f"Diskon/penyesuaian  : {rp(-selisih)}")
        out += [f"TOTAL               : {rp(total)}",
                f"Terbayar (bersih)   : {rp(total - sisa)} | Belum dibayar: {rp(sisa)}"
                + (f" (sudah dikurangi kredit retur {rp(kredit_retur)})" if kredit_retur else "")]
        batas = args.batas
        if args.per == "pihak":
            grup = {}
            for i in final:
                g = grup.setdefault(i["pihak"], [0, NOL])
                g[0] += 1
                g[1] += i["total"]
            out.append(f"Per {kata_pihak.lower()} (terbesar dulu):")
            for n, (nama, (jml, tot)) in enumerate(sorted(grup.items(), key=lambda x: -x[1][1])[:batas], 1):
                out.append(f"  {n}. {samarkan(nama) if args.samarkan else nama} - {jml} invoice - {rp(tot)}")
        elif args.per == "hari":
            grup = {}
            for i in final:
                grup[i["tgl"]] = grup.get(i["tgl"], NOL) + i["total"]
            out.append("Per hari:")
            for d in sorted(grup):
                out.append(f"  {tgl_id(d)}: {rp(grup[d])}")
        elif args.per == "barang":
            tabel_item = "SalesInvoiceItem" if jenis == "SalesInvoice" else "PurchaseInvoiceItem"
            kurs = {i["no"]: i["kurs"] for i in final}
            grup = {}
            for r in q(con, f'SELECT parent, item, quantity, amount FROM "{tabel_item}"'):
                if r["parent"] in kurs:
                    g = grup.setdefault(r["item"] or "?", [NOL, NOL])
                    g[0] += Decimal(str(r["quantity"] or 0))
                    g[1] += uang(r["amount"]) * kurs[r["parent"]]
            out.append("Per barang (nilai sebelum pajak & diskon nota, terbesar dulu):")
            for n, (nama, (jml, tot)) in enumerate(sorted(grup.items(), key=lambda x: -x[1][1])[:batas], 1):
                out.append(f"  {n}. {nama} - {angka(jml)} - {rp(tot)}")
    if any(i["retur"] for i in final):
        out.append("Catatan: retur sudah mengurangi angka di atas. 'Belum dibayar' = sisa tagihan dikurangi kredit retur yang "
                   + ("belum dikembalikan (sama dengan PIUTANG BERSIH di perintah 'piutang')." if jenis == "SalesInvoice"
                      else "belum dikembalikan (sama dengan UTANG BERSIH di perintah 'utang')."))
    if draf:
        out.append(f"Catatan: {len(draf)} draf belum di-Submit di Frappe Books; belum masuk angka di atas.")
    catatan = cek_mata_uang(info)
    if catatan:
        out.append(catatan)
    out.append("Sumber: file Frappe Books (dibaca saja). Angka dibulatkan ke rupiah terdekat untuk tampilan.")
    print("\n".join(out))


def cmd_penjualan(args):
    ringkas_invoice(args, "SalesInvoice", "PENJUALAN", "Pelanggan")


def cmd_pembelian(args):
    ringkas_invoice(args, "PurchaseInvoice", "PEMBELIAN", "Pemasok")


def kelompok_umur(telat):
    if telat <= 0:
        return "Belum jatuh tempo"
    if telat <= 30:
        return "Telat 1-30 hari"
    if telat <= 60:
        return "Telat 31-60 hari"
    if telat <= 90:
        return "Telat 61-90 hari"
    return "Telat >90 hari"


def data_umur(con, jenis, tz, kini, tempo):
    hasil = []
    for i in muat_invoice(con, jenis, tz):
        if not i["final"] or i["batal"] or i["retur"] or i["sisa"] <= 0 or not i["tgl"]:
            continue
        jt = i["tgl"] + timedelta(days=tempo)
        i["jatuh_tempo"] = jt
        i["telat"] = (kini - jt).days
        hasil.append(i)
    return sorted(hasil, key=lambda i: (-i["telat"], i["no"]))


def umur(args, jenis, judul, kata):
    tz = offset_zona(args.tz)
    if args.tempo < 0 or args.tempo > 365:
        raise Gagal("--tempo harus 0 sampai 365 hari.", "Contoh: --tempo 30")
    con, tabel = buka_db(args.db)
    cek_skema(con, tabel, [jenis, "SingleValue"])
    info = info_usaha(con)
    kini = hari_ini(args, tz)
    data = data_umur(con, jenis, tz, kini, args.tempo)
    # Frappe Books: saldo pihak = jumlah outstandingAmount semua invoice final (Party._getTotalOutstandingAmount),
    # termasuk invoice retur yang outstanding-nya NEGATIF (kredit/nota retur yang belum dikembalikan/dipotong).
    kredit = sorted((i for i in muat_invoice(con, jenis, tz) if i["final"] and not i["batal"] and i["sisa"] < 0),
                    key=lambda i: (i["pihak"], i["no"]))
    out = [f"{judul} - {info['nama']} (per {tgl_id(kini)})",
           f"Jatuh tempo dihitung = tanggal invoice + {args.tempo} hari (Frappe Books tidak menyimpan tanggal jatuh tempo)."]
    if not data and not kredit:
        out.append(f"Tidak ada invoice {kata} yang belum lunas. Semua beres.")
        print("\n".join(out))
        return
    total = sum((i["sisa"] for i in data), NOL)
    total_kredit = sum((i["sisa"] for i in kredit), NOL)
    out.append(f"Belum lunas: {len(data)} invoice, total {rp(total)}")
    for kel in ("Telat >90 hari", "Telat 61-90 hari", "Telat 31-60 hari", "Telat 1-30 hari", "Belum jatuh tempo"):
        isi = [i for i in data if kelompok_umur(i["telat"]) == kel]
        if not isi:
            continue
        out.append(f"{kel}: {len(isi)} invoice, {rp(sum((i['sisa'] for i in isi), NOL))}")
        for i in isi[: args.batas]:
            nama = samarkan(i["pihak"]) if args.samarkan else i["pihak"]
            ket = f"telat {i['telat']} hari" if i["telat"] > 0 else f"jatuh tempo {tgl_id(i['jatuh_tempo'])}"
            if i["tgl"] > kini:
                ket += " | tanggal invoice setelah hari ini"
            out.append(f"  - {i['no']} | {nama} | tgl {tgl_id(i['tgl'])} | sisa {rp(i['sisa'])} | {ket}")
        if len(isi) > args.batas:
            out.append(f"  ... dan {len(isi) - args.batas} lainnya")
    if kredit:
        out.append(f"Kredit retur belum dikembalikan/dipotong: {len(kredit)} nota retur, total {rp(total_kredit)}")
        for i in kredit[: args.batas]:
            nama = samarkan(i["pihak"]) if args.samarkan else i["pihak"]
            atas = f" atas {i['retur_atas']}" if i["retur_atas"] else ""
            out.append(f"  - {i['no']}{atas} | {nama} | tgl {tgl_id(i['tgl'])} | kredit {rp(i['sisa'])}")
        out.append(f"{'PIUTANG' if jenis == 'SalesInvoice' else 'UTANG'} BERSIH (setelah kredit retur, sama dengan saldo pihak "
                   f"di Frappe Books): {rp(total + total_kredit)}")
        out.append("Catatan: Frappe Books tidak otomatis memotong invoice asli saat retur; kredit ini dipakai saat pembayaran "
                   "berikutnya atau dikembalikan. Tagihan per invoice di atas belum dikurangi kredit.")
    catatan = cek_mata_uang(info)
    if catatan:
        out.append(catatan)
    print("\n".join(out))


def cmd_piutang(args):
    umur(args, "SalesInvoice", "PIUTANG (pelanggan belum bayar)", "penjualan")


def cmd_utang(args):
    umur(args, "PurchaseInvoice", "UTANG (tagihan pemasok belum dibayar)", "pembelian")


def data_stok(con, tabel, lokasi=None):
    cek_skema(con, tabel, ["Item", "StockLedgerEntry"])
    barang = {r["name"]: r["unit"] or "" for r in q(con, "SELECT name, unit FROM Item WHERE trackItem = 1")}
    jumlah = {n: NOL for n in barang}
    sql, par = "SELECT item, SUM(quantity) AS qty FROM StockLedgerEntry", []
    if lokasi:
        sql += " WHERE location = ?"
        par.append(lokasi)
    for r in q(con, sql + " GROUP BY item", par):
        if r["item"] in jumlah:
            jumlah[r["item"]] = Decimal(str(r["qty"] or 0)).quantize(Decimal("0.001"), ROUND_HALF_UP).normalize()
    return barang, jumlah


def cmd_stok(args):
    con, tabel = buka_db(args.db)
    info = info_usaha(con)
    if args.min < 0:
        raise Gagal("--min tidak boleh negatif.", "Contoh: --min 5")
    if args.lokasi and "Location" in tabel and not q(con, "SELECT 1 FROM Location WHERE name=?", (args.lokasi,)):
        nama = ", ".join(r["name"] for r in q(con, "SELECT name FROM Location ORDER BY name")) or "(kosong)"
        raise Gagal(f"Lokasi '{args.lokasi}' tidak ada.", f"Lokasi yang ada: {nama}")
    barang, jumlah = data_stok(con, tabel, args.lokasi)
    out = [f"STOK - {info['nama']}" + (f" (lokasi {args.lokasi})" if args.lokasi else " (semua lokasi)")]
    if not barang:
        out.append("Tidak ada barang yang dilacak stoknya. Di Frappe Books, stok hanya dihitung untuk barang "
                   "dengan 'Track Inventory' dicentang dan fitur Inventory aktif (Setup > Settings > Features > Enable Inventory).")
        print("\n".join(out))
        return
    minus = [(n, q_) for n, q_ in jumlah.items() if q_ < 0]
    habis = [(n, q_) for n, q_ in jumlah.items() if q_ == 0]
    tipis = [(n, q_) for n, q_ in jumlah.items() if 0 < q_ <= args.min]
    aman = [(n, q_) for n, q_ in jumlah.items() if q_ > args.min]
    for judul, isi in (("MINUS (cek pencatatan!)", minus), ("HABIS", habis),
                       (f"MENIPIS (<= {angka(Decimal(args.min))})", tipis)):
        if isi:
            out.append(f"{judul}:")
            out += [f"  - {n}: {angka(q_)} {barang[n]}".rstrip() for n, q_ in sorted(isi, key=lambda x: x[1])]
    if args.semua:
        out.append("AMAN:")
        out += [f"  - {n}: {angka(q_)} {barang[n]}".rstrip() for n, q_ in sorted(aman)] or ["  (tidak ada)"]
    else:
        out.append(f"Aman: {len(aman)} barang (tambahkan --semua untuk melihat daftarnya).")
    print("\n".join(out))


def cmd_laba_rugi(args):
    """Laba rugi ringkas, dihitung PERSIS seperti Reports > Profit And Loss Frappe Books v0.36.0:
    reports/LedgerReport.ts membaca tiap entri AccountingLedgerEntry (reverted = 0) sebagai
    debit = |debit|, credit = |credit| (Math.abs per kolom); AccountReport mengelompokkan per rootType akun.
    Retur (invoice retur & pengiriman/penerimaan retur) ditulis Frappe dengan nilai negatif di sisi yang ditukar;
    nilai mutlak membuat retur MENGURANGI pendapatan dan HPP, sama dengan P&L Frappe."""
    tz = offset_zona(args.tz)
    con, tabel = buka_db(args.db)
    cek_skema(con, tabel, ["Account", "AccountingLedgerEntry", "SingleValue"])
    info = info_usaha(con)
    dari, sampai, label = periode(args, tz)
    akun = {r["name"]: (r["rootType"], r["accountType"] or "") for r in q(con, "SELECT name, rootType, accountType FROM Account")}
    ada_ref = "referenceName" in kolom_tabel(con, "AccountingLedgerEntry")
    sql = "SELECT date, account, debit, credit" + (", referenceName" if ada_ref else "") + \
          " FROM AccountingLedgerEntry WHERE reverted = 0"
    pend, hpp, beban = {}, {}, {}
    ref_negatif = set()
    for r in q(con, sql):
        t = tanggal_lokal(r["date"], tz)
        if not t or not dari <= t <= sampai or r["account"] not in akun:
            continue
        root, tipe = akun[r["account"]]
        d0, c0 = uang(r["debit"]), uang(r["credit"])
        if (d0 < 0 or c0 < 0) and ada_ref and root in ("Income", "Expense"):
            ref_negatif.add(r["referenceName"] or "?")
        d, c = abs(d0), abs(c0)
        if tipe == "Cost of Goods Sold":
            hpp[r["account"]] = hpp.get(r["account"], NOL) + d - c
        elif root == "Income":
            pend[r["account"]] = pend.get(r["account"], NOL) + c - d
        elif root == "Expense":
            beban[r["account"]] = beban.get(r["account"], NOL) + d - c
    tp, th, tb = sum(pend.values(), NOL), sum(hpp.values(), NOL), sum(beban.values(), NOL)
    out = [f"LABA RUGI RINGKAS - {info['nama']}", f"Periode: {label}, zona {args.tz.upper()}", "Pendapatan:"]
    out += [f"  {n}: {rp(v)}" for n, v in sorted(pend.items(), key=lambda x: -x[1]) if rupiah_bulat(v) != 0] or ["  (tidak ada)"]
    out.append(f"Total pendapatan: {rp(tp)}")
    if hpp:
        out.append("Harga pokok penjualan (HPP):")
        out += [f"  {n}: {rp(v)}" for n, v in sorted(hpp.items(), key=lambda x: -x[1]) if rupiah_bulat(v) != 0]
    out.append(f"LABA KOTOR: {rp(tp - th)}")
    out.append("Beban:")
    out += [f"  {n}: {rp(v)}" for n, v in sorted(beban.items(), key=lambda x: -x[1]) if rupiah_bulat(v) != 0] or ["  (tidak ada)"]
    out.append(f"Total beban: {rp(tb)}")
    lb = tp - th - tb
    out.append(f"{'LABA' if lb >= 0 else 'RUGI'} BERSIH: {rp(lb)}")
    if "Item" in tabel and "expenseAccount" in kolom_tabel(con, "Item"):
        salah = [r["name"] for r in q(con, "SELECT name, expenseAccount FROM Item WHERE trackItem = 1")
                 if akun.get(r["expenseAccount"], ("", ""))[1] == "Cost of Goods Sold"]
        if salah:
            out.append(f"PERINGATAN: {len(salah)} barang berstok memakai akun pembelian HPP ({', '.join(salah[:5])}"
                       f"{', ...' if len(salah) > 5 else ''}). Pembelian lalu pengiriman barang itu mencatat HPP dua kali, "
                       "sehingga laba tampak lebih kecil. Perbaiki di Frappe Books: buka barangnya > Purchase Acc. = akun "
                       "'Stock Received But Not Billed' (lihat Inventory Settings), lalu cek ulang invoice pembelian terkait.")
    if ref_negatif:
        out.append(f"Catatan retur: {len(ref_negatif)} dokumen retur di periode ini ({', '.join(sorted(ref_negatif)[:6])}"
                   f"{', ...' if len(ref_negatif) > 6 else ''}) sudah MENGURANGI pendapatan/HPP, sama dengan cara Profit And Loss "
                   "Frappe Books membacanya.")
    out.append("Dihitung dari buku besar Frappe Books (hanya transaksi final) dengan cara yang sama seperti Reports > Profit And "
               "Loss, jadi totalnya semestinya sama. Bukan laporan keuangan resmi.")
    catatan = cek_mata_uang(info)
    if catatan:
        out.append(catatan)
    print("\n".join(out))


def cmd_laporan_harian(args):
    tz = offset_zona(args.tz)
    con, tabel = buka_db(args.db)
    cek_skema(con, tabel, ["SalesInvoice", "SingleValue"])
    info = info_usaha(con)
    kini = hari_ini(args, tz)
    t = (args.tanggal or "hari-ini").lower()
    d = kini if t in ("hari-ini", "hariini") else kini - timedelta(days=1) if t == "kemarin" else parse_tanggal_tegas(t)
    inv = muat_invoice(con, "SalesInvoice", tz)

    def jual(h):
        f = [i for i in inv if i["tgl"] == h and i["final"] and not i["batal"]]
        biasa = [i for i in f if not i["retur"]]
        retur = [i for i in f if i["retur"]]
        return len(biasa), sum((i["total"] for i in f), NOL), len(retur), sum((i["total"] for i in retur), NOL)
    n1, t1, r1, tr1 = jual(d)
    n0, t0, _, _ = jual(d - timedelta(days=1))
    draf = sum(1 for i in inv if i["tgl"] == d and not i["final"] and not i["batal"])
    out = [f"LAPORAN HARIAN {info['nama']} - {tgl_id(d)}",
           f"Penjualan final: {n1} invoice, {rp(t1 - tr1)}" + (f" (draf belum final: {draf})" if draf else "")]
    if r1:
        out.append(f"Retur penjualan: {r1} nota, {rp(tr1)} -> penjualan bersih hari ini {rp(t1)}")
    if t0 > 0 and t1 != t0:
        pers = ((t1 - t0) / t0 * 100).quantize(Decimal("0.1"), ROUND_HALF_UP)
        out.append(f"Dibanding kemarin ({rp(t0)}{' bersih' if r1 else ''}): {'+' if pers >= 0 else ''}{angka(pers)}%")
    elif t0 > 0:
        out.append(f"Sama dengan kemarin ({rp(t0)}).")
    elif t0 < 0:
        out.append(f"Kemarin hanya ada retur ({rp(t0)}).")
    else:
        out.append("Kemarin: belum ada penjualan final.")
    telat = [i for i in data_umur(con, "SalesInvoice", tz, d, args.tempo) if i["telat"] > 0]
    if telat:
        out.append(f"Piutang telat (tempo {args.tempo} hari): {len(telat)} invoice, {rp(sum((i['sisa'] for i in telat), NOL))}")
        for i in telat[:3]:
            out.append(f"  - {i['no']}: {rp(i['sisa'])}, telat {i['telat']} hari")
    else:
        out.append("Piutang telat: tidak ada.")
    if "StockLedgerEntry" in tabel and "Item" in tabel:
        barang, jumlah = data_stok(con, tabel)
        tipis = sorted((n for n, v in jumlah.items() if v <= args.min), key=lambda n: jumlah[n])
        if barang:
            out.append(f"Stok habis/menipis (<= {args.min}): {len(tipis)} barang" + (": " + ", ".join(
                f"{n} ({angka(jumlah[n])})" for n in tipis[:5]) if tipis else ""))
    out.append("(Tanpa nama pelanggan. Detail: minta 'piutang' atau 'penjualan' ke asisten.)")
    print("\n".join(out))


def cmd_ppn(args):
    if (args.dpp is None) == (args.harga_termasuk is None):
        raise Gagal("Isi salah satu: --dpp (harga sebelum PPN) atau --harga-termasuk (harga sudah termasuk PPN).",
                    "Contoh: ppn --dpp 1000000")
    try:
        nilai = baca_rupiah(args.dpp if args.dpp is not None else args.harga_termasuk, "nilai")
    except ValueError as e:
        raise Gagal(str(e) + ".", "Tulis angka rupiah, mis. 1500000 atau 1.500.000.")
    if nilai < 0:
        raise Gagal("Nilai tidak boleh negatif.", "Untuk retur, hitung dari nilai positifnya.")
    if nilai != nilai.to_integral_value():
        raise Gagal("Nilai harus rupiah bulat (tanpa sen).", "Bulatkan dulu ke rupiah.")
    if args.dpp is not None:
        dpp = nilai
    else:
        dpp = dpp_dari_harga_termasuk(nilai)
    dpp_lain, tepat, ppn = ppn_dari_dpp(dpp)
    out = ["HITUNG PPN 12% (DPP nilai lain 11/12)",
           f"Harga jual / penggantian (DPP)  : {rp(dpp)}",
           f"DPP nilai lain (11/12)         : Rp {angka(dpp_lain.quantize(Decimal('0.01'), ROUND_HALF_UP))}",
           f"PPN 12% x DPP nilai lain        : Rp {angka(tepat.quantize(Decimal('0.01'), ROUND_HALF_UP))} -> dibulatkan ke bawah {rp(ppn)}",
           f"TOTAL tagihan                  : {rp(dpp + ppn)}"]
    if args.harga_termasuk is not None:
        sisa = nilai - dpp - ppn
        out.append(f"Dari harga termasuk PPN {rp(nilai)}: sisa pembulatan {rp(sisa)}")
    out += ["Di Frappe Books: buat template Tax bertarif 11% (setara 12% x 11/12). Frappe Books menghitung pajak per "
            "baris tanpa pembulatan ke bawah, jadi bisa beda pecahan rupiah dengan angka di atas.",
            "Pembulatan belum dicocokkan dengan Coretax. Dasar: UU HPP & PMK 131/2024 (tarif 12%, DPP nilai lain "
            "11/12 untuk barang/jasa non-mewah), dicek 26 September 2026. Alat bantu hitung, bukan nasihat pajak; "
            "kasus khusus -> DJP (Kring Pajak 1500200) atau konsultan pajak."]
    print("\n".join(out))


# ---------------------------------------------------------------- CSV Import Wizard
def norm_kepala(s):
    return re.sub(r"[^a-z0-9]+", " ", (s or "").lower().replace("﻿", "")).strip()


ALIAS = {
    "nama": ["nama", "nama pelanggan", "nama pemasok", "nama supplier", "pelanggan", "customer", "supplier",
             "pemasok", "name", "nama barang", "barang", "produk", "nama produk", "item", "nama item"],
    "telepon": ["telepon", "telp", "tlp", "hp", "no hp", "nomor hp", "no telp", "wa", "no wa", "whatsapp",
                "phone", "nomor wa", "kontak"],
    "email": ["email", "e mail", "surel"],
    "npwp": ["npwp", "nitku", "tax id", "nik npwp"],
    "peran": ["peran", "role", "tipe pihak", "jenis pihak", "status"],
    "kode": ["kode", "sku", "kode barang", "item code", "kode produk"],
    "satuan": ["satuan", "unit", "uom"],
    "harga": ["harga", "harga jual", "harga satuan", "rate", "price", "harga beli"],
    "jenis": ["jenis", "tipe", "type", "barang jasa"],
    "lacak": ["lacak stok", "stok", "track inventory", "pakai stok", "hitung stok"],
    "barcode": ["barcode", "kode batang"],
    "keterangan": ["keterangan", "deskripsi", "description", "catatan", "ket"],
    "no": ["no", "no nota", "nota", "nomor", "nomor nota", "invoice", "no invoice", "no faktur"],
    "tanggal": ["tanggal", "tgl", "date", "tanggal nota"],
    "pihak": ["pelanggan", "customer", "pemasok", "supplier", "nama pelanggan", "nama pemasok", "pembeli", "penjual"],
    "barang_trx": ["barang", "produk", "item", "nama barang", "nama produk"],
    "qty": ["qty", "jumlah", "kuantitas", "banyak", "quantity", "jml", "kuantiti"],
    "pajak": ["pajak", "tax", "ppn"],
}


def baca_csv_awam(path):
    p = Path(os.path.expanduser(path or ""))
    if not path or not p.is_file():
        raise Gagal(f"File '{path}' tidak ditemukan.", "Simpan data dari Excel sebagai CSV, lalu sebutkan lokasinya.", kode=2)
    if p.suffix.lower() in (".xlsx", ".xls", ".ods", ".db"):
        raise Gagal(f"'{p.name}' bukan file CSV.", "Di Excel: File > Save As > pilih 'CSV UTF-8 (Comma delimited)'.", kode=5)
    mentah = p.read_bytes()
    teks = None
    for enc in ("utf-8-sig", "cp1252"):
        try:
            teks = mentah.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    if teks is None:
        raise Gagal(f"Huruf di '{p.name}' tidak bisa dibaca (bukan teks UTF-8 maupun Windows).",
                    "Buka di Excel lalu simpan ulang: File > Save As > 'CSV UTF-8 (Comma delimited)'.", kode=5)
    if not teks.strip():
        raise Gagal("File CSV kosong.", "Isi datanya dulu (baris pertama = judul kolom).", kode=5)
    contoh = teks[:4096]
    pemisah = ";" if contoh.count(";") > contoh.count(",") else ("\t" if contoh.count("\t") > contoh.count(",") else ",")
    baris = [b for b in csv.reader(io.StringIO(teks), delimiter=pemisah)]
    baris = [b for b in baris if any(x.strip() for x in b)]
    if len(baris) < 2:
        raise Gagal("CSV hanya berisi judul kolom, belum ada data.", "Tambahkan minimal satu baris data.", kode=5)
    lebar = len(baris[0])
    lebih = [str(i) for i, b in enumerate(baris[1:], start=2) if len(b) > lebar]
    if lebih:
        raise Gagal("Baris " + ", ".join(lebih[:10]) + " punya kolom lebih banyak dari judul (biasanya ada koma di dalam "
                    "angka atau nama, mis. 1,5jt).", "Beri tanda kutip pada nilai itu, tulis angkanya tanpa koma "
                    "(1500000), atau simpan CSV dengan pemisah titik koma (;).", kode=5)
    return [norm_kepala(k) for k in baris[0]], baris[1:]


def peta_kolom(kepala, kunci_list, wajib):
    peta = {}
    for kunci in kunci_list:
        for i, k in enumerate(kepala):
            if k in ALIAS[kunci] and i not in peta.values():
                peta[kunci] = i
                break
    kurang = [k for k in wajib if k not in peta]
    if kurang:
        nama = {"nama": "nama", "no": "no nota", "tanggal": "tanggal", "pihak": "pelanggan/pemasok",
                "barang_trx": "barang", "qty": "jumlah", "harga": "harga"}
        raise Gagal("Kolom wajib tidak ditemukan: " + ", ".join(nama.get(k, k) for k in kurang)
                    + ". Judul kolom yang terbaca: " + ", ".join(k or "(kosong)" for k in kepala) + ".",
                    "Ganti judul kolom di baris pertama, mis. " + ", ".join(nama.get(k, k) for k in wajib) + ".", kode=5)
    return peta


def ambil(baris, peta, kunci):
    i = peta.get(kunci)
    if i is None or i >= len(baris):
        return ""
    return bersih_teks(baris[i])


def bersih_teks(s):
    # Parser CSV Frappe Books salah membaca tanda kutip ganda di dalam nilai -> ganti dengan kutip tunggal
    return re.sub(r"\s+", " ", str(s or "").replace('"', "'")).strip()


DB_DIPAKAI = []


def periksa_keluar(path, db=None):
    """Tolak --keluar yang bisa menimpa database (Frappe Books atau SQLite apa pun). Hanya boleh file .csv baru/CSV lama."""
    p = Path(os.path.expanduser(path or ""))
    saran = "Pakai nama file baru berakhiran .csv, mis. impor-pelanggan.csv, di folder lain dari file .books.db."
    if not path:
        raise Gagal("--keluar belum diisi.", saran)
    if p.exists() and p.is_dir():
        raise Gagal(f"'{path}' adalah folder.", saran)
    if p.suffix.lower() != ".csv":
        raise Gagal(f"--keluar '{p.name}' harus berakhiran .csv (file ini TIDAK ditulis).", saran)
    lawan = [d for d in ([db] if db else []) + DB_DIPAKAI if d]
    for d in lawan:
        try:
            if p.resolve() == Path(os.path.expanduser(d)).resolve():
                raise Gagal("--keluar sama dengan file database Frappe Books. Ditolak agar database tidak tertimpa.", saran)
        except OSError:
            pass
    if p.is_file():
        try:
            with p.open("rb") as f:
                kepala = f.read(16)
        except OSError:
            kepala = b""
        if kepala.startswith(b"SQLite format 3"):
            raise Gagal(f"'{p.name}' adalah file database, bukan CSV. Ditolak agar tidak tertimpa.", saran)
    return p


def tulis_template(path, kolom, baris):
    """Format template resmi Import Wizard: 3 baris judul (nama skema, label, fieldKey), lalu data. CRLF, koma."""
    p = periksa_keluar(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow([k[0] for k in kolom])
        w.writerow([k[1] for k in kolom])
        w.writerow([k[2] for k in kolom])
        for b in baris:
            w.writerow(["" if v is None else v for v in b])
    return p


def angka_csv(d):
    d = Decimal(d)
    return str(int(d)) if d == d.to_integral_value() else format(d.normalize(), "f")


def laporan_validasi(judul, galat, peringatan, ok_teks):
    out = [judul]
    if galat:
        out.append(f"TIDAK LOLOS: {len(galat)} masalah harus diperbaiki dulu (file CSV TIDAK dibuat):")
        out += [f"  - {g}" for g in galat[:30]]
        if len(galat) > 30:
            out.append(f"  ... dan {len(galat) - 30} lainnya")
    if peringatan:
        out.append("Perlu dicek (tidak menghalangi):")
        out += [f"  - {p}" for p in peringatan[:30]]
    if not galat:
        out += ok_teks
    print("\n".join(out))
    if galat:
        raise SystemExit(5)


def db_opsional(path):
    """CSV bisa dibuat tanpa database, tapi dengan database nama-nama bisa dicek. Cari otomatis bila --db kosong."""
    if not path:
        try:
            path = cari_db_bawaan()
        except Gagal as g:
            if "beberapa" in g.pesan:
                raise
            return None, set()
        print(f"(Memakai database Frappe Books: {path})")
    DB_DIPAKAI.append(path)
    return buka_db(path)


def nama_ada(con, tabel_ada, tabel):
    if not con or tabel not in tabel_ada:
        return None
    return {r["name"].lower(): r["name"] for r in q(con, f'SELECT name FROM "{tabel}"')}


LANGKAH_IMPOR = [
    "Langkah di Frappe Books: menu Import Wizard (Setup/Pengaturan) > pilih jenis '{skema}' > Select File > pilih file ini >",
    "periksa pratinjau (kolom merah = salah) > Import Data. Saat ditanya 'submit after syncing', jawab TIDAK untuk transaksi",
    "agar masuk sebagai draf dan bisa dicek dulu. Backup file .books.db sebelum impor pertama.",
]


def cmd_csv_pelanggan(args):
    periksa_keluar(args.keluar, args.db)
    kepala, data = baca_csv_awam(args.masuk)
    peta = peta_kolom(kepala, ["nama", "telepon", "email", "npwp", "peran"], ["nama"])
    con, tabel = db_opsional(args.db)
    sudah = nama_ada(con, tabel, "Party") or {}
    punya_taxid = ("taxId" in kolom_tabel(con, "Party")) if con is not None and "Party" in tabel else None
    peran_bawaan = {"pelanggan": "Customer", "pemasok": "Supplier", "keduanya": "Both"}[args.peran]
    galat, peringatan, hasil, lihat = [], [], [], {}
    for no, b in enumerate(data, start=2):
        nama = ambil(b, peta, "nama")
        if not nama:
            galat.append(f"baris {no}: nama kosong")
            continue
        kunci = nama.lower()
        if kunci in lihat:
            galat.append(f"baris {no}: '{nama}' dobel dengan baris {lihat[kunci]} (nama harus unik di Frappe Books)")
            continue
        lihat[kunci] = no
        if kunci in sudah:
            peringatan.append(f"baris {no}: '{nama}' sudah ada di Frappe Books -> dilewati")
            continue
        peran_teks = ambil(b, peta, "peran").lower()
        peran = peran_bawaan
        if peran_teks:
            if any(k in peran_teks for k in ("keduanya", "both", "dua")):
                peran = "Both"
            elif any(k in peran_teks for k in ("pemasok", "supplier", "vendor", "pemasok")):
                peran = "Supplier"
            elif any(k in peran_teks for k in ("pelanggan", "customer", "pembeli")):
                peran = "Customer"
            else:
                peringatan.append(f"baris {no}: peran '{peran_teks}' tidak dikenal -> dipakai '{peran_bawaan}'")
        tel = ambil(b, peta, "telepon")
        tel_bersih = re.sub(r"[^\d+]", "", tel)
        if tel and not re.fullmatch(r"(\+62|62|0)\d{7,13}", tel_bersih):
            peringatan.append(f"baris {no}: nomor '{tel}' tampak tidak lazim, tetap disalin apa adanya")
            tel_bersih = tel
        elif tel_bersih.startswith("0"):
            tel_bersih = "+62" + tel_bersih[1:]
        elif tel_bersih.startswith("62"):
            tel_bersih = "+" + tel_bersih
        email = ambil(b, peta, "email")
        if email and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
            peringatan.append(f"baris {no}: email '{email}' tampak salah, dikosongkan")
            email = ""
        hasil.append([nama, peran, email, tel_bersih, ambil(b, peta, "npwp")])
    kolom = [("Party", "Name", "Party.name"), ("Party", "Role", "Party.role"), ("Party", "Email", "Party.email"),
             ("Party", "Phone", "Party.phone"), ("Party", "Tax ID", "Party.taxId")]
    ada_npwp = [(h[0], h[4]) for h in hasil if h[4]]
    if punya_taxid is False:
        kolom = kolom[:4]
        hasil = [h[:4] for h in hasil]
        for nama, npwp in ada_npwp:
            peringatan.append(f"NPWP '{npwp}' milik '{nama}' TIDAK ikut diimpor: file Frappe Books ini tidak punya kolom "
                              "Tax ID. Catat manual setelah impor (mis. di data pelanggan atau alamat).")
    elif punya_taxid is None and ada_npwp:
        peringatan.append(f"{len(ada_npwp)} NPWP ditaruh di kolom Tax ID. Tanpa --db belum dicek apakah Frappe Books Anda "
                          "punya kolom itu; bila tidak ada, Import Wizard mengabaikannya diam-diam. Cek setelah impor.")
    if not galat and not hasil:
        galat.append("tidak ada baris baru untuk diimpor (semua sudah ada / kosong)")
    ok = []
    if not galat:
        p = tulis_template(args.keluar, kolom, hasil)
        ok = [f"LOLOS: {len(hasil)} pihak siap diimpor -> {p}"] + [s.format(skema="Party") for s in LANGKAH_IMPOR]
    laporan_validasi("VALIDASI CSV PELANGGAN/PEMASOK (Frappe Books: Party)", galat, peringatan, ok)


def nama_dasar(nama):
    """Bagan akun Indonesia bawaan memberi nama '<nama> - <nomor>' (createCOA.ts), mis. 'Penjualan - 4110.000'."""
    return re.sub(r"\s+-\s+[0-9][0-9.]*$", "", nama or "").strip().lower()


def pilih_akun(con, tabel, diminta, aturan, label, opsi):
    """Pilih akun dengan aturan eksplisit; bila tidak pasti -> Gagal berisi daftar pilihan (agent wajib bertanya).

    aturan: tipe (accountType), root (rootType), nama (nama dasar yang diterima), kecuali (accountType yang dilarang),
    satu_tipe (boleh ambil otomatis bila hanya ada SATU akun bertipe itu)."""
    if con is None:
        if not diminta:
            raise Gagal(f"Akun {label} belum ditentukan.",
                        f"Tambahkan --db \"<file .books.db>\" agar dicocokkan dengan bagan akun, atau {opsi} \"<nama akun persis>\" "
                        "(lihat perintah 'akun').")
        return diminta
    rows = q(con, "SELECT name, rootType, accountType, isGroup FROM Account")
    ada = {r["name"]: r for r in rows}
    if diminta:
        if diminta in ada:
            nama = diminta
        else:
            cocok = [n for n in ada if nama_dasar(n) == nama_dasar(diminta) and not ada[n]["isGroup"]]
            if len(cocok) != 1:
                mirip = cocok or [n for n in ada if diminta.lower() in n.lower()][:8]
                raise Gagal(f"Akun '{diminta}' tidak ada (atau tidak tunggal) di Frappe Books.",
                            "Nama harus persis. " + (f"Pilihan: {'; '.join(mirip)}." if mirip else "Jalankan perintah 'akun'."))
            nama = cocok[0]
        if ada[nama]["isGroup"]:
            raise Gagal(f"Akun '{nama}' adalah akun grup (tidak bisa dipakai transaksi).", "Pilih akun di bawahnya (perintah 'akun').")
        return nama
    calon = sorted(n for n, r in ada.items() if not r["isGroup"]
                   and (not aturan.get("tipe") or r["accountType"] == aturan["tipe"])
                   and (not aturan.get("root") or r["rootType"] == aturan["root"])
                   and (r["accountType"] or "") not in aturan.get("kecuali", ()))
    lewat_nama = [n for n in calon if nama_dasar(n) in aturan.get("nama", ())]
    if len(lewat_nama) == 1:
        return lewat_nama[0]
    if not lewat_nama and aturan.get("satu_tipe") and len(calon) == 1:
        return calon[0]
    pilihan = lewat_nama or calon
    raise Gagal(f"Akun {label} tidak bisa dipastikan otomatis"
                + (f" (ada {len(lewat_nama)} yang cocok)" if len(lewat_nama) > 1 else "") + ". Pilihan: "
                + ("; ".join(pilihan[:12]) if pilihan else "(tidak ada akun yang sesuai)") + ".",
                f"Tanyakan ke pengguna akun mana yang benar, lalu jalankan ulang dengan {opsi} \"<nama akun persis>\".")


ATURAN_AKUN = {
    "penjualan": {"root": "Income", "kecuali": ("Cost of Goods Sold",), "nama": ("penjualan", "sales")},
    "jasa": {"root": "Income", "kecuali": ("Cost of Goods Sold",),
             "nama": ("pendapatan service", "pendapatan jasa", "service", "services")},
    "hpp": {"tipe": "Cost of Goods Sold", "nama": ("hpp pembelian", "cost of goods sold", "harga pokok penjualan"),
            "satu_tipe": True},
    "piutang": {"tipe": "Receivable", "nama": ("piutang dagang", "piutang usaha", "debtors"), "satu_tipe": True},
    "utang": {"tipe": "Payable", "nama": ("hutang dagang dalam negeri", "utang dagang dalam negeri", "hutang usaha",
                                         "utang usaha", "creditors"), "satu_tipe": True},
}
ATURAN_AKUN["srbnb"] = {"tipe": "Stock Received But Not Billed", "satu_tipe": True,
                        "nama": ("stock received but not billed", "stock diterima tapi tidak ditagih")}
SERI_BAWAAN = {"SalesInvoice": "SINV-", "PurchaseInvoice": "PINV-"}


def pilih_seri(con, tabel, skema, diminta):
    """Kolom Number Series WAJIB di Import Wizard v0.36.0 (requiredNotSelected)."""
    bawaan = SERI_BAWAAN[skema]
    if con is None or "NumberSeries" not in tabel:
        return diminta or bawaan
    ada = [r["name"] for r in q(con, "SELECT name FROM NumberSeries WHERE referenceType = ?", (skema,))]
    if diminta:
        if ada and diminta not in ada:
            raise Gagal(f"Number Series '{diminta}' tidak ada untuk {skema}.", "Pilihan: " + ", ".join(ada))
        return diminta
    if not ada or bawaan in ada:
        return bawaan
    if len(ada) == 1:
        return ada[0]
    raise Gagal(f"Ada beberapa Number Series untuk {skema}: {', '.join(ada)}.",
                "Tanyakan ke pengguna seri mana yang dipakai, lalu jalankan ulang dengan --seri \"<nama seri>\".")


def pilih_akun_stok(con, tabel, diminta, peringatan):
    if diminta:
        return pilih_akun(con, tabel, diminta, ATURAN_AKUN["srbnb"], "pembelian barang berstok", "--akun-pembelian-stok")
    if con is None:
        raise Gagal("Akun pembelian untuk barang yang dilacak stoknya belum ditentukan.",
                    "Tambahkan --db \"<file .books.db>\" (diambil dari Inventory Settings > Stock Received But Not Billed), "
                    "atau --akun-pembelian-stok \"<nama akun persis>\". Jangan pakai akun HPP: HPP akan terhitung dua kali.")
    akun = {r["name"]: r for r in q(con, "SELECT name, accountType, isGroup FROM Account")}
    v = single(con, "InventorySettings", "stockReceivedButNotBilled")
    for f, label in (("stockInHand", "Stock In Hand"), ("costOfGoodsSold", "Cost Of Goods Sold")):
        if not single(con, "InventorySettings", f):
            peringatan.append(f"Inventory Settings '{label}' belum diisi di Frappe Books; isi dulu (Setup > Settings > "
                              "Inventory) sebelum menerima/mengirim barang berstok")
    if v and v in akun and not akun[v]["isGroup"]:
        return v
    hasil = pilih_akun(con, tabel, None, ATURAN_AKUN["srbnb"], "pembelian barang berstok (Stock Received But Not Billed)",
                       "--akun-pembelian-stok")
    peringatan.append(f"Inventory Settings 'Stock Received But Not Billed' belum diisi; dipakai akun bertipe itu: {hasil}")
    return hasil


def cmd_csv_barang(args):
    periksa_keluar(args.keluar, args.db)
    kepala, data = baca_csv_awam(args.masuk)
    peta = peta_kolom(kepala, ["nama", "kode", "satuan", "harga", "jenis", "lacak", "barcode", "keterangan"], ["nama"])
    con, tabel = db_opsional(args.db)
    akun_jual = pilih_akun(con, tabel, args.akun_penjualan, ATURAN_AKUN["penjualan"], "penjualan", "--akun-penjualan")
    akun_jasa, jasa_cadangan = akun_jual, False
    if args.akun_jasa:
        akun_jasa = pilih_akun(con, tabel, args.akun_jasa, ATURAN_AKUN["jasa"], "jasa", "--akun-jasa")
    elif con is not None:
        try:
            akun_jasa = pilih_akun(con, tabel, None, ATURAN_AKUN["jasa"], "jasa", "--akun-jasa")
        except Gagal:
            jasa_cadangan = True
    else:
        jasa_cadangan = True
    sudah = nama_ada(con, tabel, "Item") or {}
    satuan_ada = nama_ada(con, tabel, "UOM")
    galat, peringatan, hasil, lihat = [], [], [], {}
    for no, b in enumerate(data, start=2):
        nama = ambil(b, peta, "nama")
        if not nama:
            galat.append(f"baris {no}: nama barang kosong")
            continue
        if nama.lower() in lihat:
            galat.append(f"baris {no}: '{nama}' dobel dengan baris {lihat[nama.lower()]}")
            continue
        lihat[nama.lower()] = no
        if nama.lower() in sudah:
            peringatan.append(f"baris {no}: '{nama}' sudah ada di Frappe Books -> dilewati")
            continue
        harga = ""
        if ambil(b, peta, "harga"):
            try:
                h = baca_rupiah(ambil(b, peta, "harga"), "harga")
                if h < 0:
                    raise ValueError("harga negatif")
                harga = angka_csv(h)
            except ValueError as e:
                galat.append(f"baris {no}: {e}")
                continue
        jenis_teks = ambil(b, peta, "jenis").lower()
        jenis = "Service" if any(k in jenis_teks for k in ("jasa", "service", "layanan")) else "Product"
        satuan = ambil(b, peta, "satuan")
        if not satuan:
            satuan = "Unit"
            if jenis == "Service" and satuan_ada:
                satuan = next((satuan_ada[k] for k in ("hour", "jam") if k in satuan_ada), "Unit")
        if satuan_ada is not None:
            if satuan.lower() in satuan_ada:
                satuan = satuan_ada[satuan.lower()]
            else:
                galat.append(f"baris {no}: satuan '{satuan}' belum ada di Frappe Books (yang ada: "
                             + ", ".join(sorted(satuan_ada.values())) + "). Tambahkan dulu satuan itu atau ganti.")
                continue
        lacak_teks = ambil(b, peta, "lacak").lower()
        lacak = "1" if lacak_teks in ("ya", "y", "yes", "1", "true", "iya") or (not lacak_teks and args.lacak_stok and jenis == "Product") else "0"
        if lacak == "1" and jenis == "Service":
            peringatan.append(f"baris {no}: jasa tidak bisa dilacak stoknya -> lacak stok dimatikan")
            lacak = "0"
        hasil.append([nama, ambil(b, peta, "kode"), "Both", jenis, satuan, harga, ambil(b, peta, "keterangan"),
                      akun_jasa if jenis == "Service" else akun_jual, None, ambil(b, peta, "barcode"), lacak])
    # Akun pembelian mengikuti formula bawaan Frappe Books v0.36.0 (models/baseModels/Item/Item.ts, expenseAccount):
    # barang dilacak stok -> InventorySettings.stockReceivedButNotBilled; lainnya -> akun bertipe Cost of Goods Sold.
    # Barang berstok dengan akun HPP membuat HPP terhitung dua kali (saat pembelian dan saat pengiriman/Shipment).
    akun_beli = akun_stok = None
    if any(h[10] == "0" for h in hasil):
        akun_beli = pilih_akun(con, tabel, args.akun_pembelian, ATURAN_AKUN["hpp"], "pembelian/HPP (barang tanpa stok & jasa)",
                               "--akun-pembelian")
    if any(h[10] == "1" for h in hasil):
        akun_stok = pilih_akun_stok(con, tabel, args.akun_pembelian_stok, peringatan)
    for h in hasil:
        h[8] = akun_stok if h[10] == "1" else akun_beli
    if jasa_cadangan and any(h[3] == "Service" for h in hasil):
        peringatan.append(f"jasa memakai akun penjualan '{akun_jual}' (akun pendapatan jasa tidak ditemukan pasti); "
                          "bila salah, jalankan ulang dengan --akun-jasa \"<nama akun>\"")
    if satuan_ada is None:
        peringatan.append("tanpa --db: nama satuan belum dicek. Satuan bawaan Frappe Books: Unit, Kg, Gram, Meter, Hour, Day "
                          "(Jam/Hari bila usaha dibuat dalam bahasa Indonesia). Satuan lain harus dibuat dulu.")
    if any(h[-1] == "1" for h in hasil) and con is not None and not info_usaha(con)["inventori"]:
        peringatan.append("fitur Inventory belum aktif; aktifkan di Setup > Settings > Features (Enable Inventory) agar 'Track Inventory' dipakai")
    kolom = [("Item", "Item Name", "Item.name"), ("Item", "Item Code", "Item.itemCode"), ("Item", "Purpose", "Item.for"),
             ("Item", "Type", "Item.itemType"), ("Item", "Unit Type", "Item.unit"), ("Item", "Rate", "Item.rate"),
             ("Item", "Description", "Item.description"), ("Item", "Sales Acc.", "Item.incomeAccount"),
             ("Item", "Purchase Acc.", "Item.expenseAccount"), ("Item", "Barcode", "Item.barcode"),
             ("Item", "Track Inventory", "Item.trackItem")]
    if not galat and not hasil:
        galat.append("tidak ada barang baru untuk diimpor")
    ok = []
    if not galat:
        p = tulis_template(args.keluar, kolom, hasil)
        ok = [f"LOLOS: {len(hasil)} barang/jasa siap diimpor -> {p}",
              f"Akun penjualan: {akun_jual}" + (f" (jasa: {akun_jasa})" if akun_jasa != akun_jual else "")
              + (f" | akun pembelian (tanpa stok/jasa): {akun_beli}" if akun_beli else "")
              + (f" | akun pembelian barang berstok: {akun_stok} (bawaan Frappe: Stock Received But Not Billed)"
                 if akun_stok else "")] + [s.format(skema="Item") for s in LANGKAH_IMPOR]
        if con is None:
            ok.append("Nama akun belum dicek ke database (tanpa --db); pastikan persis sama dengan di Frappe Books.")
    laporan_validasi("VALIDASI CSV BARANG (Frappe Books: Item)", galat, peringatan, ok)


def cmd_csv_transaksi(args):
    jual = args.jenis == "penjualan"
    skema = "SalesInvoice" if jual else "PurchaseInvoice"
    skema_item = skema + "Item"
    label_skema = "Sales Invoice" if jual else "Purchase Invoice"
    periksa_keluar(args.keluar, args.db)
    kepala, data = baca_csv_awam(args.masuk)
    peta = peta_kolom(kepala, ["no", "tanggal", "pihak", "barang_trx", "qty", "harga", "pajak", "keterangan"],
                      ["no", "tanggal", "pihak", "barang_trx", "qty", "harga"])
    con, tabel = db_opsional(args.db)
    akun_pihak = pilih_akun(con, tabel, args.akun_piutang if jual else args.akun_utang,
                            ATURAN_AKUN["piutang" if jual else "utang"],
                            "piutang" if jual else "utang", "--akun-piutang" if jual else "--akun-utang")
    seri = pilih_seri(con, tabel, skema, args.seri)
    pihak_ada = nama_ada(con, tabel, "Party")
    peran_pihak = {r["name"]: r["role"] for r in q(con, "SELECT name, role FROM Party")} if pihak_ada is not None else {}
    peran_salah = set()
    barang_db = {}
    if con is not None and "Item" in tabel:
        for r in q(con, "SELECT name, incomeAccount, expenseAccount, unit FROM Item"):
            barang_db[r["name"].lower()] = r
    pajak_db = {}
    if con is not None and "Tax" in tabel and "TaxDetail" in tabel:
        for r in q(con, "SELECT t.name AS nama, d.rate AS tarif FROM Tax t LEFT JOIN TaxDetail d ON d.parent=t.name"):
            pajak_db.setdefault(r["nama"].lower(), (r["nama"], []))[1].append(Decimal(str(r["tarif"] or 0)))
    galat, peringatan, hasil = [], [], []
    nota = {}
    for no, b in enumerate(data, start=2):
        kode = ambil(b, peta, "no")
        if not kode:
            galat.append(f"baris {no}: no nota kosong")
            continue
        try:
            tgl = parse_tanggal_awam(ambil(b, peta, "tanggal"))
            qty = baca_jumlah(ambil(b, peta, "qty"), "jumlah")
            harga = baca_rupiah(ambil(b, peta, "harga"), "harga")
        except ValueError as e:
            galat.append(f"baris {no}: {e}")
            continue
        if qty <= 0:
            galat.append(f"baris {no}: jumlah harus lebih dari 0 (retur dibuat di Frappe Books lewat tombol Return)")
            continue
        if harga < 0:
            galat.append(f"baris {no}: harga tidak boleh negatif")
            continue
        pihak = ambil(b, peta, "pihak")
        barang = ambil(b, peta, "barang_trx")
        if not pihak or not barang:
            galat.append(f"baris {no}: {'pelanggan/pemasok' if not pihak else 'barang'} kosong")
            continue
        if pihak_ada is not None:
            if pihak.lower() not in pihak_ada:
                galat.append(f"baris {no}: '{pihak}' belum ada di Frappe Books -> impor dulu lewat csv-pelanggan")
                continue
            pihak = pihak_ada[pihak.lower()]
            if peran_pihak.get(pihak) == ("Supplier" if jual else "Customer") and pihak not in peran_salah:
                peran_salah.add(pihak)
                peringatan.append(f"baris {no}: '{pihak}' terdaftar sebagai {'pemasok' if jual else 'pelanggan'} saja; "
                                  f"ubah perannya ke Both di Frappe Books bila memang juga {'pelanggan' if jual else 'pemasok'}")
        if con is not None:
            if barang.lower() not in barang_db:
                galat.append(f"baris {no}: barang '{barang}' belum ada di Frappe Books -> impor dulu lewat csv-barang")
                continue
            r = barang_db[barang.lower()]
            barang = r["name"]
            akun_baris = r["incomeAccount"] if jual else r["expenseAccount"]
            if not akun_baris:
                galat.append(f"baris {no}: barang '{barang}' belum punya akun {'penjualan' if jual else 'pembelian'} di Frappe Books")
                continue
        else:
            akun_baris = args.akun_barang
            if not akun_baris:
                raise Gagal("Tanpa --db, akun barang tidak bisa diambil dari data barang.",
                            "Tambahkan --db \"<file .books.db>\" (disarankan) atau --akun-barang \"<nama akun>\".")
        pajak = ambil(b, peta, "pajak") or (args.pajak or "")
        tarif = None
        if pajak and pajak_db:
            if pajak.lower() not in pajak_db:
                awal = [k for k in pajak_db if k.startswith(pajak.lower())]
                if len(awal) == 1:
                    peringatan.append(f"baris {no}: pajak '{pajak}' dianggap '{pajak_db[awal[0]][0]}' (satu-satunya yang cocok)")
                    pajak = pajak_db[awal[0]][0]
            if pajak.lower() not in pajak_db:
                galat.append(f"baris {no}: pajak '{pajak}' belum ada di Frappe Books (yang ada: "
                             + ", ".join(v[0] for v in pajak_db.values()) + ")")
                continue
            pajak, tarif_list = pajak_db[pajak.lower()]
            tarif = sum(tarif_list, NOL)
            if tarif == 12:
                peringatan.append(f"baris {no}: pajak '{pajak}' bertarif 12% dari harga penuh; untuk PPN DPP 11/12 "
                                  "biasanya 11% (lihat perintah ppn)")
        elif pajak and con is None:
            peringatan.append(f"baris {no}: nama pajak '{pajak}' belum dicek (tanpa --db)")
        n = nota.setdefault(kode, {"tgl": tgl, "pihak": pihak, "baris": no, "dpp": NOL, "tarif": set(), "ada_pajak": False})
        if n["tgl"] != tgl or n["pihak"].lower() != pihak.lower():
            galat.append(f"baris {no}: nota '{kode}' berbeda tanggal/pihak dengan baris {n['baris']} (satu nota = satu tanggal & pihak)")
            continue
        jumlah_baris = rupiah_bulat(qty * harga)
        n["dpp"] += jumlah_baris
        if pajak:
            n["ada_pajak"] = True
            n["tarif"].add(tarif)
        kode_impor = f"{args.awalan}{kode}"
        ket = ambil(b, peta, "keterangan") if not n.get("ket_ditulis") else ""
        n["ket_ditulis"] = True
        hasil.append([kode_impor, seri, pihak, akun_pihak, tgl.isoformat(), ket,
                      barang, angka_csv(harga), angka_csv(qty), akun_baris, pajak])
    kolom = [(label_skema, "Invoice No", f"{skema}.name"), (label_skema, "Number Series", f"{skema}.numberSeries"),
             (label_skema, "Customer" if jual else "Supplier", f"{skema}.party"),
             (label_skema, "Account", f"{skema}.account"), (label_skema, "Date", f"{skema}.date"),
             (label_skema, "Notes", f"{skema}.terms"),
             (label_skema + " Item", "Item", f"{skema_item}.item"), (label_skema + " Item", "Rate", f"{skema_item}.rate"),
             (label_skema + " Item", "Quantity", f"{skema_item}.quantity"),
             (label_skema + " Item", "Account", f"{skema_item}.account"), (label_skema + " Item", "Tax", f"{skema_item}.tax")]
    if not galat and not hasil:
        galat.append("tidak ada baris transaksi")
    ok = []
    if not galat:
        p = tulis_template(args.keluar, kolom, hasil)
        ok = [f"LOLOS: {len(nota)} nota ({len(hasil)} baris barang) siap diimpor -> {p}", "Pratinjau per nota (hitungan Komunitech):"]
        tot_dpp = NOL
        for kode, n in sorted(nota.items(), key=lambda x: (x[1]["tgl"], x[0])):
            tot_dpp += n["dpp"]
            baris = f"  - {kode} | {tgl_id(n['tgl'])} | {n['pihak']} | DPP {rp(n['dpp'])}"
            if n["ada_pajak"]:
                if n["tarif"] == {Decimal(11)}:
                    _, tepat, ppn = ppn_dari_dpp(n["dpp"])
                    baris += f" | PPN (standar Komunitech) {rp(ppn)} | total {rp(n['dpp'] + ppn)}"
                else:
                    baris += " | ada pajak (lihat hitungan Frappe Books)"
            ok.append(baris)
        ok.append(f"Total DPP semua nota: {rp(tot_dpp)}")
        ok.append(f"Akun {'piutang' if jual else 'utang'}: {akun_pihak} | Number Series: {seri}")
        ok.append(f"Kolom 'Invoice No' ({args.awalan}...) hanya pengelompok baris; nomor final diberi otomatis oleh "
                  f"Number Series {seri}.")
        ok += [s.format(skema=label_skema) for s in LANGKAH_IMPOR]
        ok.append("Setelah impor, cocokkan total tiap invoice di Frappe Books dengan pratinjau di atas. Pajak di Frappe Books "
                  "dihitung per baris tanpa pembulatan ke bawah, jadi bisa beda pecahan rupiah.")
        if con is None:
            ok.append("Tanpa --db: nama pelanggan/barang/akun/pajak belum dicek; Import Wizard akan menolak nama yang belum ada.")
    laporan_validasi(f"VALIDASI CSV {'PENJUALAN' if jual else 'PEMBELIAN'} (Frappe Books: {skema})", galat, peringatan, ok)


# ---------------------------------------------------------------- CLI
class Parser(argparse.ArgumentParser):
    def error(self, message):
        raise Gagal(f"Perintah kurang/salah: {message}.", "Lihat bantuan: python3 frappe_books.py -h")


def buat_parser():
    ap = Parser(prog="frappe_books.py", description="Asisten Frappe Books untuk UMKM (Komunitech). Database dibaca saja.")
    ap.add_argument("--versi", action="version", version=f"frappe_books.py {VERSI}")
    sub = ap.add_subparsers(dest="perintah")

    def dasar(p, periode_=False, tz=True):
        p.add_argument("--db", help="path file .books.db (atau ENV FRAPPE_BOOKS_DB)")
        if tz:
            p.add_argument("--tz", default="WIB", help="WIB (bawaan), WITA, WIT")
            p.add_argument("--hari-ini", help=argparse.SUPPRESS)
        if periode_:
            p.add_argument("--bulan", help="ini (bawaan), lalu, atau TAHUN-BULAN")
            p.add_argument("--dari")
            p.add_argument("--sampai")
            p.add_argument("--tanggal", help="hari-ini, kemarin, atau TAHUN-BULAN-TANGGAL")

    p = sub.add_parser("cek"); dasar(p, tz=False); p.set_defaults(fungsi=cmd_cek)
    p = sub.add_parser("akun"); dasar(p, tz=False); p.set_defaults(fungsi=cmd_akun)
    for nama, fungsi in (("penjualan", cmd_penjualan), ("pembelian", cmd_pembelian)):
        p = sub.add_parser(nama); dasar(p, periode_=True)
        p.add_argument("--per", choices=["pihak", "hari", "barang", "tidak"], default="pihak")
        p.add_argument("--batas", type=int, default=10)
        p.add_argument("--samarkan", action="store_true", help="nama pihak jadi inisial")
        p.set_defaults(fungsi=fungsi)
    for nama, fungsi in (("piutang", cmd_piutang), ("utang", cmd_utang)):
        p = sub.add_parser(nama); dasar(p)
        p.add_argument("--tempo", type=int, default=30, help="hari tempo pembayaran (bawaan 30)")
        p.add_argument("--batas", type=int, default=10)
        p.add_argument("--samarkan", action="store_true")
        p.set_defaults(fungsi=fungsi)
    p = sub.add_parser("stok"); dasar(p, tz=False)
    p.add_argument("--min", type=int, default=5, help="batas stok menipis (bawaan 5)")
    p.add_argument("--lokasi")
    p.add_argument("--semua", action="store_true")
    p.set_defaults(fungsi=cmd_stok)
    p = sub.add_parser("laba-rugi"); dasar(p, periode_=True); p.set_defaults(fungsi=cmd_laba_rugi)
    p = sub.add_parser("laporan-harian"); dasar(p)
    p.add_argument("--tanggal", help="hari-ini (bawaan), kemarin, atau TAHUN-BULAN-TANGGAL")
    p.add_argument("--tempo", type=int, default=30)
    p.add_argument("--min", type=int, default=5)
    p.set_defaults(fungsi=cmd_laporan_harian)
    p = sub.add_parser("ppn")
    p.add_argument("--dpp")
    p.add_argument("--harga-termasuk")
    p.set_defaults(fungsi=cmd_ppn)
    p = sub.add_parser("csv-pelanggan"); p.add_argument("--db")
    p.add_argument("--masuk", required=True); p.add_argument("--keluar", required=True)
    p.add_argument("--peran", choices=["pelanggan", "pemasok", "keduanya"], default="pelanggan")
    p.set_defaults(fungsi=cmd_csv_pelanggan)
    p = sub.add_parser("csv-barang"); p.add_argument("--db")
    p.add_argument("--masuk", required=True); p.add_argument("--keluar", required=True)
    p.add_argument("--akun-penjualan"); p.add_argument("--akun-pembelian"); p.add_argument("--akun-jasa")
    p.add_argument("--akun-pembelian-stok", help="akun pembelian barang berstok (bawaan: Inventory Settings)")
    p.add_argument("--lacak-stok", action="store_true", help="barang (bukan jasa) tanpa kolom lacak stok -> dilacak")
    p.set_defaults(fungsi=cmd_csv_barang)
    p = sub.add_parser("csv-transaksi"); p.add_argument("--db")
    p.add_argument("--jenis", choices=["penjualan", "pembelian"], default="penjualan")
    p.add_argument("--masuk", required=True); p.add_argument("--keluar", required=True)
    p.add_argument("--akun-piutang"); p.add_argument("--akun-utang"); p.add_argument("--akun-barang")
    p.add_argument("--pajak", help="nama template Tax untuk semua baris tanpa kolom pajak")
    p.add_argument("--awalan", default="IMPOR-", help="awalan nomor pengelompok nota")
    p.add_argument("--seri", help="Number Series, bawaan SINV- (penjualan) / PINV- (pembelian)")
    p.set_defaults(fungsi=cmd_csv_transaksi)
    return ap


def main(argv=None):
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass
    try:
        args = buat_parser().parse_args(argv)
        if not getattr(args, "perintah", None):
            raise Gagal("Perintah belum disebut.", "Contoh: python3 frappe_books.py penjualan --db \"<file .books.db>\"")
        if getattr(args, "batas", 1) < 1:
            raise Gagal("--batas minimal 1.", "Contoh: --batas 10")
        args.fungsi(args)
        return 0
    except Gagal as g:
        print(f"GAGAL: {g.pesan}", file=sys.stderr)
        if g.saran:
            print(f"Saran: {g.saran}", file=sys.stderr)
        return g.kode
    except SystemExit as e:
        return e.code if isinstance(e.code, int) else 0
    except KeyboardInterrupt:
        print("GAGAL: dibatalkan.", file=sys.stderr)
        return 130
    except Exception as e:  # jangan pernah tampilkan traceback ke pengguna awam
        print(f"GAGAL: terjadi galat tak terduga ({type(e).__name__}). Data Anda tidak diubah.", file=sys.stderr)
        print("Saran: jalankan 'cek' untuk memeriksa file, lalu laporkan pesan ini ke Komunitech.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
