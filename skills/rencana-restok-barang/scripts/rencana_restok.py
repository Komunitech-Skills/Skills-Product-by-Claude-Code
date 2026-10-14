#!/usr/bin/env python3
"""Rencana restok barang dari riwayat penjualan (titik pesan ulang / reorder point, stok pengaman / safety stock).

Untuk toko, warung, dan online shop: barang apa yang dipesan sekarang, berapa, dan kapan.
Hanya pustaka standar Python 3.8+. Tanpa akses jaringan. Hanya membaca file yang diberikan
(--file, --barang, --pemasok) atau teks (--data, --barang-data, --pemasok-data); tidak menulis file.

Rumus (Komunitech; dijelaskan dengan bahasa awam di references/rumus-dan-istilah.md):
  Deret harian    : penjualan bersih per hari di rentang data; hari tanpa penjualan = 0.
                    Retur/batal mengurangi penjualan pada tanggal itu, lalu hari-hari sebelumnya.
  Rata-rata (mu)  : total terjual / jumlah hari rentang.
  Simpangan (sd)  : simpangan baku sampel (n-1) deret harian.
                    Data mingguan/bulanan: sd harian = sd laju per periode x akar(panjang periode);
                    < 4 periode penuh -> sd = akar(mu) (asumsi, disebut di catatan).
  Tren            : faktor = rata-rata 28 hari terakhir / mu (data >= 42 hari; mingguan >= 6 minggu;
                    bulanan >= 3 bulan, bulan terakhir). >= 1,2 naik; <= 0,8 turun; selain itu stabil.
                    Naik/turun: mu dan sd dikali faktor yang dibatasi 0,5..1,5 (--tanpa-tren mematikan).
  Faktor musim    : dari pengguna (--faktor-musim, default 1), dikalikan ke mu dan sd.
  Stok pengaman   : SS  = z x sd x akar(lead time)     z: 90% = 1,28 | 95% = 1,65 | 99% = 2,33
  Titik pesan     : ROP = mu x lead time + SS                (dibulatkan ke atas)
  Stok target     : T   = mu x (lead time + horizon) + SS    (dibulatkan ke atas)
  Posisi stok     : stok sekarang + barang dalam pesanan
  PESAN SEKARANG  : posisi <= ROP, atau ROP tercapai < 1 hari lagi; jumlah = T - posisi
  MINGGU DEPAN    : ROP tercapai dalam 1..7 hari; jumlah = T - perkiraan posisi pada tanggal pesan
  Pembulatan qty  : ke atas ke bilangan bulat -> naik ke minimal order -> ke atas ke kelipatan kemasan
  Habis dalam     : floor(stok / mu) hari
  Barang mati     : tidak terjual >= 60 hari dan stok > 0 (atau stok belum diketahui)
  Data belum cukup: rentang data barang < 14 hari, atau barang baru tercatat < 14 hari terakhir
Rupiah: jumlah x harga beli, dibulatkan ke rupiah terdekat (0,5 ke atas).
"""
import argparse
import csv
import io
import json
import re
import sys
from calendar import monthrange
from datetime import date, timedelta
from decimal import ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_UP, Decimal, InvalidOperation, getcontext

getcontext().prec = 40
VERSI = "1.0.0"
LABEL_AGENT = ("[UNTUK AGENT SAJA - jangan disalin apa adanya; sampaikan dengan bahasa awam, tanpa menyebut "
               "script/file/proses. Semua angka disalin persis dari sini.]")
DISCLAIMER = ("Rencana ini perkiraan dari pola penjualan sebelumnya, bukan jaminan. Cocokkan dulu dengan stok fisik, "
              "harga, dan kesanggupan pemasok sebelum memesan; promo, musim, dan libur bisa mengubah permintaan.")

Z_LAYANAN = {80: Decimal("0.84"), 85: Decimal("1.04"), 90: Decimal("1.28"), 95: Decimal("1.65"),
             97: Decimal("1.88"), 98: Decimal("2.05"), 99: Decimal("2.33")}
MIN_HARI_DATA = 14
HARI_TREN = 28
MIN_HARI_TREN = 42
TREN_NAIK, TREN_TURUN = Decimal("1.2"), Decimal("0.8")
FAKTOR_MIN, FAKTOR_MAKS = Decimal("0.5"), Decimal("1.5")
JENDELA_MINGGU_DEPAN = 7
HARI_STOK_BERLEBIH = 90
BLN = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]

URUTAN_KELOMPOK = ["PESAN_SEKARANG", "PESAN_MINGGU_DEPAN", "AMAN", "STOK_BELUM_DIKETAHUI",
                   "DATA_BELUM_CUKUP", "BARANG_MATI", "TIDAK_ADA_PENJUALAN"]
LABEL_KELOMPOK = {"PESAN_SEKARANG": "PESAN SEKARANG", "PESAN_MINGGU_DEPAN": "PESAN MINGGU DEPAN", "AMAN": "AMAN",
                  "STOK_BELUM_DIKETAHUI": "STOK BELUM DIKETAHUI", "DATA_BELUM_CUKUP": "DATA BELUM CUKUP",
                  "BARANG_MATI": "BARANG MATI", "TIDAK_ADA_PENJUALAN": "TIDAK ADA PENJUALAN"}


class Galat(Exception):
    def __init__(self, pesan, saran=""):
        super().__init__(pesan)
        self.pesan, self.saran = pesan, saran


# ------------------------------------------------------------------ angka, hari, tanggal
PENGALI = {"rb": 10**3, "ribu": 10**3, "k": 10**3, "jt": 10**6, "juta": 10**6}
SATUAN = ("pcs|pc|unit|buah|bh|biji|bks|bungkus|botol|btl|dus|box|pack|pak|kg|gr|gram|liter|ltr|cup|porsi|lembar|lbr|"
          "meter|roll|sachet|renteng|karung|sak|ikat|potong|pasang|psg|set|x")


def ke_angka(teks, nama="angka"):
    """'Rp 35.000' | '35rb' | '1,5' | '1.200' | '12 pcs' | '2 lusin' | '(2)' | '-3' -> Decimal; kosong -> None."""
    if teks is None:
        return None
    asli = str(teks)
    s = asli.strip().lower()
    if s in ("", "-", "—", "n/a", "na", "null", "none", "?", "nan"):
        return None
    kali = Decimal(1)
    m = re.search(r"\s*(lusin|kodi)$", s)
    if m:
        kali = Decimal(12 if m.group(1) == "lusin" else 20)
        s = s[:m.start()]
    s = re.sub(r"^(rp|idr)\.?\s*", "", s)
    s = re.sub(r",-$", "", s).strip()
    s = re.sub(r"\s*(" + SATUAN + r")\.?$", "", s).strip()
    neg = False
    if s.startswith("(") and s.endswith(")"):
        neg, s = True, s[1:-1].strip()
    if s[:1] in ("-", "−"):
        neg, s = True, s[1:].strip()
    s = re.sub(r"^(rp|idr)\.?\s*", "", s).replace(" ", "")
    m = re.fullmatch(r"([0-9][0-9.,]*)(rb|ribu|k|jt|juta)?", s)
    if not m:
        raise Galat(f"{nama}: '{asli}' tidak terbaca sebagai angka", "Tulis angka seperti 12, 1.200, 1,5, atau 35rb.")
    num, suf = m.group(1).strip(".,"), m.group(2)
    if "," in num and "." in num:
        num = num.replace(".", "").replace(",", ".") if num.rfind(",") > num.rfind(".") else num.replace(",", "")
    elif "," in num:
        b = num.split(",")
        if len(b) > 2 or (len(b[1]) == 3 and not suf):
            num = num.replace(",", "")
        else:
            num = num.replace(",", ".")
    elif "." in num:
        b = num.split(".")
        if len(b) > 2 or len(b[1]) == 3:
            num = num.replace(".", "")
    try:
        v = Decimal(num) * Decimal(PENGALI[suf] if suf else 1) * kali
    except InvalidOperation:
        raise Galat(f"{nama}: '{asli}' tidak terbaca sebagai angka", "Tulis angka seperti 12 atau 1.200.")
    return -v if neg else v


def ke_hari(teks, nama="lead time"):
    """'7' | '7 hari' | '2-3 hari' (ambil terlama) | '1 minggu' | '2 pekan' | '1 bulan' -> Decimal hari; kosong -> None."""
    if teks is None:
        return None
    s = str(teks).strip().lower()
    if s in ("", "-", "?", "n/a"):
        return None
    kali = Decimal(1)
    if re.search(r"(minggu|mgg|pekan|week|wk)", s):
        kali = Decimal(7)
    elif re.search(r"(bulan|bln|month)", s):
        kali = Decimal(30)
    angka = re.findall(r"\d+(?:[.,]\d+)?", re.sub(r"[a-z/]+", " ", s))
    if not angka:
        raise Galat(f"{nama}: '{teks}' tidak terbaca", "Tulis jumlah hari, mis. 7 atau '2-3 hari' atau '1 minggu'.")
    return max(Decimal(a.replace(",", ".")) for a in angka) * kali


BULAN = {"jan": 1, "januari": 1, "january": 1, "feb": 2, "februari": 2, "pebruari": 2, "february": 2,
         "mar": 3, "maret": 3, "march": 3, "apr": 4, "april": 4, "mei": 5, "may": 5, "jun": 6, "juni": 6,
         "june": 6, "jul": 7, "juli": 7, "july": 7, "agu": 8, "agt": 8, "ags": 8, "agus": 8, "agustus": 8,
         "aug": 8, "august": 8, "sep": 9, "sept": 9, "september": 9, "okt": 10, "oktober": 10, "oct": 10,
         "october": 10, "nov": 11, "nop": 11, "nopember": 11, "november": 11, "des": 12, "desember": 12,
         "dec": 12, "december": 12}
POLA_HARI = r"^(senin|selasa|rabu|kamis|jumat|jum'at|sabtu|minggu|ahad|mon|tue|wed|thu|fri|sat|sun)[a-z]*,?\s+"


def _buat(y, m, d):
    if not 2000 <= y <= 2100:
        return None
    try:
        return date(y, m, d)
    except ValueError:
        return None


def ke_tanggal(teks, bulan_dulu=False):
    """-> (date|None, catatan). catatan: None | 'bulan-dulu' | 'ambigu' | 'bulan-saja'.
    bulan_dulu=True: tanggal yang bisa dibaca dua arah (mis. 02/09/2026) dibaca bulan/tanggal (gaya AS)."""
    if teks is None:
        return None, None
    s = str(teks).strip().lower()
    if not s:
        return None, None
    s = re.sub(POLA_HARI, "", s)
    s = re.sub(r"(t|\s+)\d{1,2}[:.]\d{2}([:.]\d{2})?(\.\d+)?\s*(wib|wita|wit|am|pm|z|[+-]\d{2}:?\d{2})?$", "", s).strip()
    m = re.fullmatch(r"(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})", s)
    if m:
        return _buat(int(m.group(1)), int(m.group(2)), int(m.group(3))), None
    m = re.fullmatch(r"(\d{1,2})[-/.](\d{1,2})[-/.](\d{4}|\d{2})", s)
    if m:
        a, b, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        y = y + 2000 if y < 100 else y
        if a > 12 and b <= 12:
            return _buat(y, b, a), None
        if b > 12 and a <= 12:
            return _buat(y, a, b), "bulan-dulu"
        if a <= 12 and b <= 12:
            if bulan_dulu:
                return _buat(y, a, b), None
            return _buat(y, b, a), ("ambigu" if a != b else None)
        return None, None
    m = re.fullmatch(r"(\d{1,2})[\s\-/.]*([a-z]+)\.?[\s\-/.,]*(\d{4}|\d{2})", s)
    if m and m.group(2) in BULAN:
        y = int(m.group(3))
        return _buat(y + 2000 if y < 100 else y, BULAN[m.group(2)], int(m.group(1))), None
    m = re.fullmatch(r"([a-z]+)\.?\s*(\d{1,2}),?\s*(\d{4})", s)
    if m and m.group(1) in BULAN:
        return _buat(int(m.group(3)), BULAN[m.group(1)], int(m.group(2))), None
    m = re.fullmatch(r"(\d{4})[-/.](\d{1,2})", s)
    if m:
        return _buat(int(m.group(1)), int(m.group(2)), 1), "bulan-saja"
    m = re.fullmatch(r"(\d{1,2})[-/.](\d{4})", s)
    if m:
        return _buat(int(m.group(2)), int(m.group(1)), 1), "bulan-saja"
    m = re.fullmatch(r"([a-z]+)\.?[\s\-/]*(\d{4}|\d{2})", s)
    if m and m.group(1) in BULAN:
        y = int(m.group(2))
        return _buat(y + 2000 if y < 100 else y, BULAN[m.group(1)], 1), "bulan-saja"
    m = re.fullmatch(r"(\d{5})(\.\d+)?", s)  # nomor seri tanggal Excel
    if m and 30000 <= int(m.group(1)) <= 80000:
        return date(1899, 12, 30) + timedelta(days=int(m.group(1))), None
    return None, None


# ------------------------------------------------------------------ format tampilan
def bulat(x):
    return int(Decimal(x).quantize(Decimal(1), rounding=ROUND_HALF_UP))


def atas(x):
    return int(Decimal(x).to_integral_value(rounding=ROUND_CEILING))


def bawah(x):
    return int(Decimal(x).to_integral_value(rounding=ROUND_FLOOR))


def rp(n):
    n = int(n)
    return ("-" if n < 0 else "") + "Rp" + f"{abs(n):,}".replace(",", ".")


def des(x, d=2):
    """Decimal -> '1,43' (koma desimal, titik ribuan, nol di belakang dibuang)."""
    if x is None:
        return "-"
    x = Decimal(x).quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP)
    s = f"{x:,.{d}f}".replace(",", "_").replace(".", ",").replace("_", ".")
    if "," in s:
        s = s.rstrip("0").rstrip(",")
    return s


def angka_json(x, d=2):
    if x is None:
        return None
    x = Decimal(x)
    if x == x.to_integral_value():
        return int(x)
    return float(x.quantize(Decimal(1).scaleb(-d), rounding=ROUND_HALF_UP))


def tgl_id(t):
    return f"{t.day} {BLN[t.month - 1]} {t.year}" if t else "-"


# ------------------------------------------------------------------ baca tabel
def kunci_kolom(h):
    n = re.sub(r"\s+", " ", re.sub(r"[_\-/().:#'*]+", " ", str(h).strip().lower())).strip()
    tok = n.split(" ")
    while len(tok) > 1 and tok[-1] in ("pcs", "rp", "idr", "buah", "hari", "harian"):
        tok.pop()
    return " ".join(tok)


A_SKU = ["sku", "nomor referensi sku", "sku penjual", "seller sku", "kode barang", "kode produk", "kode item", "kode sku",
         "nomor sku", "kode", "item code", "product code", "barcode", "sku induk", "sku id"]
A_NAMA = ["nama barang", "nama produk", "nama item", "nama", "produk", "barang", "item", "product name", "product",
          "menu", "nama menu", "item name", "judul produk"]
A_VARIAN = ["varian", "nama variasi", "variasi", "variation", "variant", "variation name"]
A_MASTER = {
    "stok": ["stok sekarang", "stok", "stock", "sisa stok", "stok akhir", "stok saat ini", "qty stok", "persediaan",
             "on hand", "stok tersedia", "sisa"],
    "lead_time": ["lead time", "leadtime", "lead time pemasok", "waktu kirim", "lama kirim", "waktu tunggu",
                  "lama pengiriman", "lama datang", "estimasi datang"],
    "harga_beli": ["harga beli", "harga modal", "modal", "hpp", "hpp rata2", "hpp rata rata", "harga pokok", "harga kulak",
                   "harga kulakan", "cost", "buy price", "harga beli satuan", "harga beli terakhir"],
    "pemasok": ["pemasok", "supplier", "vendor", "distributor", "suplier", "nama pemasok", "nama supplier"],
    "dalam_pesanan": ["dalam pesanan", "sedang dipesan", "on order", "dipesan", "dalam perjalanan",
                      "barang dalam perjalanan", "sudah dipesan", "po berjalan"],
    "kelipatan": ["kelipatan", "isi per dus", "isi dus", "isi kemasan", "kemasan", "per dus", "isi per pack", "pack size",
                  "isi karton", "isi per karton", "kelipatan pesan"],
    "moq": ["moq", "minimal order", "min order", "minimum order", "minimal pesan", "min pesan", "minimal beli", "min beli"],
    "mulai_jual": ["mulai jual", "mulai dijual", "tanggal mulai jual", "tgl mulai jual", "barang baru sejak", "tanggal rilis"],
    "satuan": ["satuan", "uom", "unit"],
}
KOLOM_JUAL = {
    "tanggal": ["tanggal", "tgl", "date", "tanggal transaksi", "tanggal penjualan", "tanggal pesanan", "tgl transaksi",
                "tgl penjualan", "tanggal order", "waktu pesanan dibuat", "waktu transaksi", "waktu", "created time",
                "order created time", "order date", "tanggal pembayaran", "waktu pembayaran dilakukan", "paid time",
                "hari", "periode", "minggu", "minggu mulai", "bulan"],
    "sku": A_SKU, "nama": A_NAMA, "varian": A_VARIAN,
    "qty": ["qty", "kuantitas", "quantity", "jumlah terjual", "qty terjual", "terjual", "jumlah", "jml", "jumlah barang",
            "jumlah produk", "jumlah produk dibeli", "jumlah produk di pesan", "banyak", "pcs", "sold", "qty sold",
            "unit terjual", "laku"],
    "status": ["status pesanan", "status", "order status", "status transaksi", "status order", "status terakhir"],
    "no_pesanan": ["no pesanan", "nomor pesanan", "id pesanan", "order id", "no invoice", "nomor invoice", "invoice",
                   "no transaksi", "nomor transaksi", "no nota", "nomor nota", "order no", "order number"],
    "arah": ["arah"],
    "jenis": ["jenis", "jenis transaksi", "tipe transaksi"],
    "stok_sesudah": ["stok sesudah"],
}
KOLOM_JUAL.update(A_MASTER)
KOLOM_BARANG = {"sku": A_SKU, "nama": A_NAMA, "varian": A_VARIAN}
KOLOM_BARANG.update(A_MASTER)
KOLOM_PEMASOK = {
    "pemasok": A_MASTER["pemasok"],
    "lead_time": A_MASTER["lead_time"],
    "min_belanja": ["minimal belanja", "min belanja", "minimum belanja", "minimal transaksi", "min transaksi",
                    "minimal order rp", "min order rp"],
}
KATA_BATAL = ("batal", "cancel", "dibatalkan", "belum bayar", "belum dibayar", "unpaid", "gagal", "failed",
              "pengembalian", "retur", "return", "refund", "ditolak", "rejected")
JENIS_JUAL = {"jual", "jual-mp", "penjualan", "sale", "sales", "terjual"}
JENIS_KURANG = {"batal-pesanan", "retur-pembeli"}
JENIS_DIKENAL = JENIS_JUAL | JENIS_KURANG | {"beli", "masuk", "opname", "saldo-awal", "saldo awal", "rusak", "hilang",
                                            "retur-supplier", "pakai-sendiri", "lainnya", "retur", "refund", "pembelian",
                                            "batal", "keluar"}


def petakan(header, alias):
    hn = [kunci_kolom(h) for h in header]
    peta, dipakai = {}, set()
    for field, daftar in alias.items():
        for a in daftar:
            for i, h in enumerate(hn):
                if i not in dipakai and h == a:
                    peta[field] = i
                    dipakai.add(i)
                    break
            if field in peta:
                break
    return peta


def cari_header(rows, alias, maks=15):
    terbaik, peta_terbaik = None, {}
    for i, r in enumerate(rows[:maks]):
        p = petakan(r, alias)
        if len(p) > len(peta_terbaik):
            terbaik, peta_terbaik = i, p
    return terbaik, peta_terbaik


def baris_dari_json(obj):
    if isinstance(obj, list) and obj and all(isinstance(x, dict) for x in obj):
        kunci = []
        for x in obj:
            for k in x:
                if k not in kunci:
                    kunci.append(k)
        return [kunci] + [["" if x.get(k) is None else str(x.get(k)) for k in kunci] for x in obj]
    if isinstance(obj, list) and all(isinstance(x, list) for x in obj):
        return [["" if c is None else str(c) for c in x] for x in obj]
    raise Galat("format JSON tidak dikenali", "Pakai daftar objek, mis. [{\"tanggal\": \"2026-09-01\", \"sku\": \"A\", \"qty\": 3}].")


def baca_teks_tabel(teks):
    teks = (teks or "").lstrip("﻿")
    s = teks.strip()
    if not s:
        raise Galat("data kosong", "Tempel tabel penjualan dengan kolom tanggal, nama barang/SKU, dan jumlah terjual.")
    if s[0] in "[{":
        try:
            obj = json.loads(s)
        except ValueError:
            obj = None
        if obj is not None:
            if isinstance(obj, dict):
                raise Galat("JSON gabungan harus dipisah", "Pakai kunci 'penjualan' (dan opsional 'barang', 'pemasok') lewat --file.")
            return baris_dari_json(obj)
    baris = [b for b in teks.replace("\r\n", "\n").replace("\r", "\n").split("\n") if b.strip()]
    if sum(1 for b in baris if b.strip().startswith("|")) >= 2:
        rows = []
        for b in baris:
            b = b.strip()
            if not b.startswith("|"):
                continue
            sel = [c.strip() for c in b.strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in sel if c):
                continue
            rows.append(sel)
        return rows
    contoh = baris[:10]
    delim = ","
    for d in ("\t", ";", "|"):
        if sum(1 for b in contoh if d in b) * 2 > len(contoh):
            delim = d
            break
    return [r for r in csv.reader(io.StringIO("\n".join(baris)), delimiter=delim)]


def kolom_ref(ref):
    n = 0
    for ch in re.match(r"[A-Z]*", ref).group(0):
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def baca_xlsx(path):
    import zipfile
    import xml.etree.ElementTree as ET
    ns = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    try:
        z = zipfile.ZipFile(path)
    except (zipfile.BadZipFile, OSError) as e:
        raise Galat(f"file Excel tidak bisa dibuka: {e}", "Simpan ulang sebagai CSV, atau tempel isinya.")
    with z:
        nama = z.namelist()
        shared = []
        if "xl/sharedStrings.xml" in nama:
            for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall(ns + "si"):
                shared.append("".join(t.text or "" for t in si.iter(ns + "t")))
        lembar = sorted(n for n in nama if n.startswith("xl/worksheets/sheet") and n.endswith(".xml"))
        if not lembar:
            raise Galat("file Excel tidak berisi lembar kerja", "Simpan ulang sebagai CSV.")
        pilih = "xl/worksheets/sheet1.xml" if "xl/worksheets/sheet1.xml" in nama else lembar[0]
        rows = []
        for r in ET.fromstring(z.read(pilih)).iter(ns + "row"):
            sel = {}
            for c in r.findall(ns + "c"):
                t, v = c.get("t"), c.find(ns + "v")
                if t == "s":
                    val = shared[int(v.text)] if v is not None and v.text else ""
                elif t == "inlineStr":
                    val = "".join(x.text or "" for x in c.iter(ns + "t"))
                else:
                    val = v.text if v is not None and v.text is not None else ""
                sel[kolom_ref(c.get("r", "A"))] = val
            if sel:
                rows.append([sel.get(i, "") for i in range(max(sel) + 1)])
    return rows


def baca_sumber(path=None, teks=None):
    if path:
        p = str(path)
        if p.lower().endswith(".xls"):
            raise Galat("file .xls lama belum didukung", "Simpan sebagai .xlsx atau CSV dari Excel, lalu kirim ulang.")
        if p.lower().endswith(".xlsx"):
            return baca_xlsx(p), None
        try:
            with open(p, "rb") as f:
                mentah = f.read()
        except OSError as e:
            raise Galat(f"file tidak bisa dibuka: {e}", "Periksa nama file, atau tempel isinya.")
        try:
            isi = mentah.decode("utf-8-sig")
        except UnicodeDecodeError:
            isi = mentah.decode("cp1252", errors="replace")
        s = isi.strip()
        if s.startswith("{"):
            try:
                obj = json.loads(s)
            except ValueError:
                obj = None
            if isinstance(obj, dict):
                return None, obj
        return baca_teks_tabel(isi), None
    return baca_teks_tabel(teks.replace("\\n", "\n").replace("\\t", "\t")), None


# ------------------------------------------------------------------ olah data
def kunci_sku(s):
    return re.sub(r"\s+", " ", str(s).strip()).upper()


def kunci_nama(s):
    return re.sub(r"\s+", " ", str(s).strip()).lower()


class Konteks:
    def __init__(self, args):
        self.args = args
        self.barang = {}
        self.idx_sku, self.idx_nama = {}, {}
        self.tanggal = []
        self.dilewati = []
        self.catatan = []
        self.status_lewat = {}
        self.dobel = 0
        self.bulan_dulu = self.ambigu = self.bulan_saja = 0
        self.di_luar = 0
        self.pemetaan = {}
        self.pemasok = {}
        self.galat_master = set()
        self.gaya_as = False

    def lewati(self, no, alasan, nilai=""):
        self.dilewati.append({"baris": no, "alasan": alasan, "nilai": str(nilai)[:40]})

    def item(self, sku, nama, varian="", buat=True):
        sku, nama, varian = (sku or "").strip(), (nama or "").strip(), (varian or "").strip()
        label = (nama + (" " + varian if varian else "")).strip()
        it = None
        if sku and kunci_sku(sku) in self.idx_sku:
            it = self.idx_sku[kunci_sku(sku)]
        elif label and kunci_nama(label) in self.idx_nama:
            it = self.idx_nama[kunci_nama(label)]
        if it is None:
            if not buat:
                return None
            kunci = kunci_sku(sku) if sku else "N:" + kunci_nama(label)
            it = {"kunci": kunci, "sku": sku, "nama": label or sku, "jual": {}, "kurang": [], "pertama": None,
                  "saldo_awal": None, "master": {}, "ada_baris": False}
            self.barang[kunci] = it
        if sku and not it["sku"]:
            it["sku"] = sku
        if label and (it["nama"] == it["sku"] or not it["nama"]):
            it["nama"] = label
        if sku:
            self.idx_sku[kunci_sku(sku)] = it
        if label:
            self.idx_nama[kunci_nama(label)] = it
        return it


PARSER_MASTER = {"stok": ke_angka, "dalam_pesanan": ke_angka, "kelipatan": ke_angka, "moq": ke_angka,
                 "harga_beli": ke_angka, "lead_time": ke_hari}


def isi_master(ctx, it, field, teks, urutan, sumber):
    teks = (teks or "").strip()
    if not teks:
        return
    try:
        if field in PARSER_MASTER:
            v = PARSER_MASTER[field](teks, field)
            if v is None:
                return
            if v < 0 and field != "stok":
                raise Galat("negatif")
        elif field == "mulai_jual":
            v = ke_tanggal(teks)[0]
            if v is None:
                raise Galat("tanggal")
        else:
            v = teks
    except Galat:
        ctx.galat_master.add(f"{field} '{teks[:20]}' ({it['nama']})")
        return
    lama = it["master"].get(field)
    if lama is None or urutan >= lama[0]:
        it["master"][field] = (urutan, v, sumber)


def nilai_master(it, field):
    x = it["master"].get(field)
    return x[1] if x else None


def format_bulan_dulu(nilai):
    """True bila kolom tanggal tampak gaya AS (bulan/tanggal): >= 2 baris pasti bulan/tanggal, >= 20% baris
    bergaris miring, dan tidak ada satu pun baris yang pasti tanggal/bulan."""
    pasti_hb = pasti_bh = jumlah = 0
    for v in nilai:
        m = re.match(r"^\s*(?:[a-z']+,?\s+)?(\d{1,2})[-/.](\d{1,2})[-/.](\d{2}|\d{4})\b", str(v).lower())
        if not m:
            continue
        jumlah += 1
        a, b = int(m.group(1)), int(m.group(2))
        if a > 12 and b <= 12:
            pasti_hb += 1
        elif b > 12 and a <= 12:
            pasti_bh += 1
    return pasti_hb == 0 and pasti_bh >= 2 and pasti_bh * 5 >= jumlah


def ubah_lebar(rows):
    """Tabel lebar (baris = barang, kolom = tanggal) -> tabel panjang tanggal;sku;nama;varian;qty."""
    for hi, r in enumerate(rows[:15]):
        tgl = [(i, ke_tanggal(c)[0]) for i, c in enumerate(r)]
        tgl = [(i, t) for i, t in tgl if t]
        if len(tgl) < 2:
            continue
        kol_tgl = {i for i, _ in tgl}
        peta = petakan([c if i not in kol_tgl else "" for i, c in enumerate(r)],
                       {"sku": A_SKU, "nama": A_NAMA, "varian": A_VARIAN})
        if not peta:
            bebas = [i for i in range(len(r)) if i not in kol_tgl]
            if not bebas:
                return None
            peta = {"nama": bebas[0]}
        out = [["tanggal", "sku", "nama", "varian", "qty"]]
        for b in rows[hi + 1:]:
            ambil = lambda f: (b[peta[f]] if f in peta and peta[f] < len(b) else "")  # noqa: E731
            for i, t in tgl:
                q = b[i] if i < len(b) else ""
                if str(q).strip():
                    out.append([t.isoformat(), ambil("sku"), ambil("nama"), ambil("varian"), q])
        return out
    return None


def olah_penjualan(ctx, rows, lebar_dicoba=False):
    a = ctx.args
    if not rows:
        raise Galat("data penjualan kosong", "Tempel tabel penjualan: tanggal, nama barang/SKU, jumlah terjual.")
    hi, peta = cari_header(rows, KOLOM_JUAL)
    if hi is None or "tanggal" not in peta or "qty" not in peta or not ({"sku", "nama"} & set(peta)):
        if not lebar_dicoba:
            lebar = ubah_lebar(rows)
            if lebar:
                ctx.catatan.append("Tabel berbentuk lebar (kolom = tanggal) dibaca sebagai penjualan per tanggal.")
                return olah_penjualan(ctx, lebar, lebar_dicoba=True)
        kurang = [k for k, lab in (("tanggal", "tanggal"), ("qty", "jumlah terjual")) if k not in peta]
        if not ({"sku", "nama"} & set(peta)):
            kurang.append("nama barang/SKU")
        judul = rows[hi] if hi is not None else rows[0]
        raise Galat("kolom penjualan tidak lengkap: " + ", ".join(kurang) + f". Judul kolom yang terbaca: {judul[:12]}",
                    "Minimal perlu kolom tanggal, nama barang (atau SKU), dan jumlah terjual (qty). "
                    "Ganti judul kolom bila namanya lain, mis. 'Tgl Nota' -> 'tanggal'.")
    header = rows[hi]
    ctx.pemetaan["penjualan"] = {f: header[i] for f, i in sorted(peta.items(), key=lambda x: x[1])}
    buku_stok = "arah" in peta and "jenis" in peta
    pakai_jenis = False
    if "jenis" in peta:
        nilai = [str(r[peta["jenis"]]).strip().lower() for r in rows[hi + 1:] if peta["jenis"] < len(r) and str(r[peta["jenis"]]).strip()]
        cocok = sum(1 for v in nilai if v in JENIS_DIKENAL or any(k in v for k in ("retur", "jual", "beli", "batal")))
        pakai_jenis = buku_stok or (nilai and cocok * 2 >= len(nilai))
        if not pakai_jenis:
            ctx.catatan.append("Kolom jenis tidak dipakai sebagai jenis transaksi (isinya tampak seperti kategori barang).")
    if buku_stok:
        ctx.catatan.append("Data dikenali sebagai ekspor mutasi buku stok: penjualan = jenis jual/jual-mp; batal pesanan "
                           "dan retur pembeli mengurangi penjualan; stok sekarang diambil dari stok sesudah transaksi terakhir.")
    kol_t = peta["tanggal"]
    ctx.gaya_as = format_bulan_dulu(r[kol_t] for r in rows[hi + 1:] if kol_t < len(r))
    if ctx.gaya_as:
        ctx.catatan.append("Tanggal dibaca bergaya bulan/tanggal (gaya Amerika) untuk seluruh tabel, karena beberapa "
                           "tanggal hanya masuk akal dibaca begitu (mis. 09/13/2026). Pastikan formatnya.")
    terlihat = set()
    for no, r in enumerate(rows[hi + 1:], start=hi + 2):
        if not any(str(c).strip() for c in r):
            continue

        def ambil(f, r=r):
            return str(r[peta[f]]).strip() if f in peta and peta[f] < len(r) and r[peta[f]] is not None else ""
        sku, nama, varian = ambil("sku"), ambil("nama"), ambil("varian")
        if not sku and not nama:
            ctx.lewati(no, "nama barang/SKU kosong")
            continue
        if not sku and kunci_nama(nama) in ("total", "jumlah", "grand total", "subtotal", "total penjualan"):
            ctx.lewati(no, "baris total")
            continue
        tgl, ket = ke_tanggal(ambil("tanggal"), bulan_dulu=ctx.gaya_as)
        if tgl is None:
            ctx.lewati(no, "tanggal tidak terbaca", ambil("tanggal"))
            continue
        if (a.dari and tgl < a.dari) or (a.sampai and tgl > a.sampai):
            ctx.di_luar += 1
            continue
        if ket == "bulan-dulu":
            ctx.bulan_dulu += 1
        elif ket == "ambigu":
            ctx.ambigu += 1
        elif ket == "bulan-saja":
            ctx.bulan_saja += 1
        try:
            q = ke_angka(ambil("qty"), "jumlah")
        except Galat:
            ctx.lewati(no, "jumlah tidak terbaca", ambil("qty"))
            continue
        if q is None:
            ctx.lewati(no, "jumlah kosong")
            continue
        status = ambil("status").lower()
        if status and any(k in status for k in KATA_BATAL):
            ctx.status_lewat[status] = ctx.status_lewat.get(status, 0) + 1
            continue
        it = ctx.item(sku, nama, varian)
        order = ambil("no_pesanan")
        if order:
            kk = (order, it["kunci"], tgl, q)
            if kk in terlihat:
                ctx.dobel += 1
                continue
            terlihat.add(kk)
        jenis = ambil("jenis").lower() if pakai_jenis else ""
        if jenis:
            if jenis in JENIS_JUAL:
                macam = "jual"
            elif jenis in JENIS_KURANG:
                macam = "kurang"
            elif "supplier" in jenis or "pemasok" in jenis:
                macam = "info"
            elif any(k in jenis for k in ("retur", "refund", "batal", "return", "cancel")):
                macam = "kurang"
            elif any(k in jenis for k in ("jual", "sale")):
                macam = "jual"
            else:
                macam = "info"
        else:
            macam = "jual" if q > 0 else ("kurang" if q < 0 else "info")
        ctx.tanggal.append(tgl)
        it["ada_baris"] = True
        it["pertama"] = tgl if it["pertama"] is None else min(it["pertama"], tgl)
        if macam == "jual":
            it["jual"][tgl] = it["jual"].get(tgl, Decimal(0)) + abs(q)
        elif macam == "kurang":
            it["kurang"].append((tgl, abs(q)))
        elif jenis in ("saldo-awal", "saldo awal"):
            it["saldo_awal"] = tgl if it["saldo_awal"] is None else min(it["saldo_awal"], tgl)
        urutan = (tgl.toordinal(), no)
        if "stok_sesudah" in peta:
            isi_master(ctx, it, "stok", ambil("stok_sesudah"), urutan, "buku stok (stok sesudah transaksi terakhir)")
        for f in A_MASTER:
            if f in peta:
                isi_master(ctx, it, f, ambil(f), urutan, "tabel penjualan")


def olah_barang(ctx, rows):
    hi, peta = cari_header(rows, KOLOM_BARANG)
    if hi is None or not ({"sku", "nama"} & set(peta)) or len(peta) < 2:
        raise Galat("tabel data barang tidak dikenali", "Minimal kolom sku atau nama barang + salah satu: stok, lead_time, "
                    "harga_beli, pemasok, kelipatan, moq, dalam_pesanan.")
    header = rows[hi]
    ctx.pemetaan["barang"] = {f: header[i] for f, i in sorted(peta.items(), key=lambda x: x[1])}
    for no, r in enumerate(rows[hi + 1:], start=hi + 2):
        if not any(str(c).strip() for c in r):
            continue

        def ambil(f, r=r):
            return str(r[peta[f]]).strip() if f in peta and peta[f] < len(r) and r[peta[f]] is not None else ""
        if not ambil("sku") and not ambil("nama"):
            continue
        it = ctx.item(ambil("sku"), ambil("nama"), ambil("varian"))
        label = (ambil("nama") + (" " + ambil("varian") if ambil("varian") else "")).strip()
        if label:
            it["nama"] = label  # nama di daftar barang lebih diutamakan daripada judul produk di ekspor penjualan
            ctx.idx_nama[kunci_nama(label)] = it
        for f in A_MASTER:
            if f in peta:
                isi_master(ctx, it, f, ambil(f), (10**9, no), "data barang")


def olah_pemasok(ctx, rows):
    hi, peta = cari_header(rows, KOLOM_PEMASOK)
    if hi is None or "pemasok" not in peta or len(peta) < 2:
        raise Galat("tabel pemasok tidak dikenali", "Pakai kolom pemasok;lead_time_hari (opsional minimal_belanja).")
    ctx.pemetaan["pemasok"] = {f: rows[hi][i] for f, i in sorted(peta.items(), key=lambda x: x[1])}
    for r in rows[hi + 1:]:
        nama = str(r[peta["pemasok"]]).strip() if peta["pemasok"] < len(r) else ""
        if not nama:
            continue
        d = {"nama": nama}
        for f, fn in (("lead_time", ke_hari), ("min_belanja", ke_angka)):
            if f in peta and peta[f] < len(r) and str(r[peta[f]]).strip():
                try:
                    d[f] = fn(r[peta[f]], f)
                except Galat:
                    ctx.galat_master.add(f"{f} pemasok {nama}")
        ctx.pemasok[kunci_nama(nama)] = d


# ------------------------------------------------------------------ hitung
def rata(xs):
    return sum(xs, Decimal(0)) / len(xs) if xs else Decimal(0)


def simpangan(xs):
    n = len(xs)
    if n < 2:
        return Decimal(0)
    m = rata(xs)
    return (sum(((x - m) ** 2 for x in xs), Decimal(0)) / (n - 1)).sqrt()


def median(xs):
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2


def ember(harian, mulai, mode):
    """-> daftar (total, panjang_hari, penuh?)"""
    out = []
    if mode == "minggu":
        for i in range(0, len(harian), 7):
            seg = harian[i:i + 7]
            out.append((sum(seg, Decimal(0)), len(seg), len(seg) == 7))
    else:
        kini = None
        for i, x in enumerate(harian):
            t = mulai + timedelta(days=i)
            k = (t.year, t.month)
            if k != kini:
                out.append([Decimal(0), 0, monthrange(t.year, t.month)[1]])
                kini = k
            out[-1][0] += x
            out[-1][1] += 1
        out = [(tot, n, n == penuh) for tot, n, penuh in out]
    return out


def bulatkan_pesan(q, kelipatan, moq):
    """q (Decimal > 0) -> (jumlah, keterangan): ke atas -> minimal order -> kelipatan kemasan."""
    n = Decimal(atas(q))
    ket = []
    if moq and moq > 0 and n < moq:
        n = Decimal(atas(moq))
        ket.append(f"naik ke minimal order {des(moq)}")
    if kelipatan and kelipatan > 0:
        n2 = (n / kelipatan).to_integral_value(rounding=ROUND_CEILING) * kelipatan
        if n2 != n:
            ket.append(f"dibulatkan ke kelipatan {des(kelipatan)}")
        n = n2
    return n, ket


def hitung_barang(it, ctx):
    a = ctx.args
    akhir, awal = ctx.akhir, ctx.awal
    h = {"sku": it["sku"], "nama": it["nama"], "catatan": []}
    satuan = nilai_master(it, "satuan") or "pcs"
    h["satuan"] = satuan
    pemasok = nilai_master(it, "pemasok")
    h["pemasok"] = pemasok
    harga = nilai_master(it, "harga_beli")
    h["harga_beli"] = bulat(harga) if harga is not None else None
    stok = nilai_master(it, "stok")
    dp = nilai_master(it, "dalam_pesanan") or Decimal(0)
    kel, moq = nilai_master(it, "kelipatan"), nilai_master(it, "moq")
    if stok is not None and it["master"]["stok"][2].startswith("buku stok"):
        h["catatan"].append("stok sekarang diambil dari catatan buku stok terakhir")
    h.update({"stok_sekarang": angka_json(stok), "dalam_pesanan": angka_json(dp),
              "kelipatan": angka_json(kel), "minimal_order": angka_json(moq)})

    # lead time
    L, sumber_L = nilai_master(it, "lead_time"), "data barang"
    if L is None and pemasok and kunci_nama(pemasok) in ctx.pemasok and "lead_time" in ctx.pemasok[kunci_nama(pemasok)]:
        L, sumber_L = ctx.pemasok[kunci_nama(pemasok)]["lead_time"], "data pemasok"
    if L is None:
        L, sumber_L = ctx.lead_default, "default"
    if L < 1:
        h["catatan"].append(f"lead time {des(L)} hari dinaikkan ke 1 hari")
        L = Decimal(1)
    h["lead_time_hari"], h["sumber_lead_time"] = angka_json(L), sumber_L

    # rentang barang ini
    mulai, sumber_mulai = awal, "awal data"
    mj = nilai_master(it, "mulai_jual")
    if mj is not None and mj > awal:
        mulai, sumber_mulai = mj, "tanggal mulai dijual"
    elif mj is None and it["saldo_awal"] and it["saldo_awal"] > awal:
        mulai, sumber_mulai = it["saldo_awal"], "saldo awal buku stok"
    N = (akhir - mulai).days + 1

    jual = dict(it["jual"])
    sisa_kurang = Decimal(0)
    for tgl, q in sorted(it["kurang"]):
        t, sisa = min(tgl, akhir), q
        while sisa > 0 and t >= awal:
            ada = jual.get(t, Decimal(0))
            if ada > 0:
                ambil = min(ada, sisa)
                jual[t] = ada - ambil
                sisa -= ambil
            t -= timedelta(days=1)
        sisa_kurang += sisa
    if sisa_kurang > 0:
        h["catatan"].append(f"retur/batal {des(sisa_kurang)} {satuan} tidak ada penjualan pasangannya di rentang data (diabaikan)")
    if it["kurang"]:
        h["retur_batal_dikurangkan"] = angka_json(sum((q for _, q in it["kurang"]), Decimal(0)) - sisa_kurang)

    harian = [jual.get(mulai + timedelta(days=i), Decimal(0)) for i in range(max(N, 0))]
    total = sum(harian, Decimal(0))
    tgl_jual = sorted(t for t, q in jual.items() if q > 0 and mulai <= t <= akhir)
    pertama_jual = tgl_jual[0] if tgl_jual else None
    terakhir_jual = tgl_jual[-1] if tgl_jual else None
    if terakhir_jual and ctx.mode == "minggu":
        terakhir_jual = min(terakhir_jual + timedelta(days=6), akhir)
    elif terakhir_jual and ctx.mode == "bulan":
        terakhir_jual = min(terakhir_jual.replace(day=monthrange(terakhir_jual.year, terakhir_jual.month)[1]), akhir)
    tanpa_jual = (akhir - terakhir_jual).days if terakhir_jual else max(N, 0)
    h["data"] = {"mulai": mulai.isoformat(), "sampai": akhir.isoformat(), "jumlah_hari": max(N, 0),
                 "sumber_mulai": sumber_mulai, "total_terjual": angka_json(total),
                 "hari_ada_penjualan": sum(1 for x in harian if x > 0) if ctx.mode == "hari" else None,
                 "penjualan_terakhir": terakhir_jual.isoformat() if terakhir_jual else None,
                 "hari_tanpa_penjualan": tanpa_jual, "belum_pernah_terjual": terakhir_jual is None}
    sebelum = sum((q for t, q in jual.items() if t < mulai), Decimal(0))
    if sebelum > 0:
        h["catatan"].append(f"{des(sebelum)} {satuan} terjual sebelum tanggal mulai dijual tidak dihitung")

    nilai_stok = bulat(stok * harga) if (stok is not None and harga is not None and stok > 0) else None
    kosong = {"rata_rata_harian": None, "simpangan_harian": None, "tren": "tidak dihitung", "faktor_tren": None,
              "rata_rata_dipakai": None, "stok_pengaman": None, "titik_pesan_ulang": None, "stok_target": None,
              "habis_dalam_hari": None, "perkiraan_tanggal_habis": None, "tanggal_pesan": None,
              "jumlah_pesan": None, "nilai_pesanan": None, "posisi_stok": None, "lonjakan": []}
    h.update(kosong)

    # 1. data belum cukup
    baru = (mj is None and it["pertama"] is not None and sumber_mulai == "awal data"
            and (akhir - it["pertama"]).days + 1 < MIN_HARI_DATA and N >= MIN_HARI_DATA)
    if N < MIN_HARI_DATA or baru:
        hari_amat = (akhir - max(mulai, it["pertama"] or mulai)).days + 1
        h["kelompok"] = "DATA_BELUM_CUKUP"
        rentang = (akhir - awal).days + 1
        if rentang < MIN_HARI_DATA:
            h["alasan"] = f"data penjualan baru {rentang} hari (perlu minimal {MIN_HARI_DATA} hari)"
        elif N < MIN_HARI_DATA:
            h["alasan"] = (f"mulai dijual {tgl_id(mulai)}, data baru {max(N, 0)} hari (perlu minimal {MIN_HARI_DATA} hari)"
                           if N > 0 else f"tanggal mulai dijual ({tgl_id(mulai)}) sesudah akhir data")
        else:
            h["alasan"] = f"barang ini baru tercatat sejak {tgl_id(it['pertama'])} ({hari_amat} hari); barang baru atau jarang laku"
        h["data_pendek"] = rentang < MIN_HARI_DATA
        tot_amat = sum((q for t, q in jual.items() if t >= max(mulai, it["pertama"] or mulai) and t <= akhir), Decimal(0))
        laju = (tot_amat / hari_amat) if hari_amat > 0 else None
        h["pengamatan"] = {"hari": max(hari_amat, 0), "terjual": angka_json(tot_amat),
                           "laju_sementara_per_hari": angka_json(laju) if laju is not None else None,
                           "habis_dalam_hari_laju_sementara": (0 if stok <= 0 else bawah(stok / laju))
                           if (stok is not None and laju) else None}
        h["nilai_stok"] = nilai_stok
        return h

    # lonjakan (hanya data harian)
    if ctx.mode == "hari":
        isi = [x for x in harian if x > 0]
        if len(isi) >= 5:
            med = median(isi)
            for i, x in enumerate(harian):
                if x >= 4 * med and x >= med + 10:
                    t = mulai + timedelta(days=i)
                    h["lonjakan"].append({"tanggal": t.isoformat(), "terjual": angka_json(x), "biasanya": angka_json(med)})
                    if a.abaikan_lonjakan:
                        harian[i] = med
            if h["lonjakan"] and a.abaikan_lonjakan:
                total = sum(harian, Decimal(0))
                h["catatan"].append("lonjakan diganti nilai biasanya (median hari laku) sebelum dihitung")

    mu = total / N
    emb = ember(harian, mulai, ctx.mode) if ctx.mode != "hari" else None
    asumsi_sd = False
    if ctx.mode == "hari":
        sd = simpangan(harian)
    else:
        penuh = [(t, n) for t, n, p in emb if p]
        if len(penuh) >= 4:
            laju = [t / n for t, n in penuh]
            sd = simpangan(laju) * (Decimal(sum(n for _, n in penuh)) / len(penuh)).sqrt()
        else:
            sd = mu.sqrt()
            asumsi_sd = True
            h["catatan"].append("simpangan diasumsikan = akar rata-rata (periode data < 4)")
    h["asumsi_simpangan"] = asumsi_sd

    mu_baru = None
    if ctx.mode == "hari" and N >= MIN_HARI_TREN:
        mu_baru = sum(harian[-HARI_TREN:], Decimal(0)) / HARI_TREN
    elif ctx.mode == "minggu" and len(emb) >= 6:
        mu_baru = sum((t for t, _, _ in emb[-4:]), Decimal(0)) / sum(n for _, n, _ in emb[-4:])
    elif ctx.mode == "bulan" and len(emb) >= 3:
        mu_baru = emb[-1][0] / emb[-1][1]
    faktor = (mu_baru / mu) if (mu_baru is not None and mu > 0) else None
    tren = "tidak dihitung" if faktor is None else ("naik" if faktor >= TREN_NAIK else "turun" if faktor <= TREN_TURUN else "stabil")
    f_pakai = Decimal(1)
    if tren in ("naik", "turun") and not a.tanpa_tren:
        f_pakai = min(max(faktor, FAKTOR_MIN), FAKTOR_MAKS)
    mu_p = mu * f_pakai * ctx.faktor_musim
    sd_p = sd * f_pakai * ctx.faktor_musim
    h.update({"rata_rata_harian": angka_json(mu), "simpangan_harian": angka_json(sd),
              "rata_rata_terbaru": angka_json(mu_baru), "tren": tren,
              "faktor_tren": angka_json(faktor, 2) if faktor is not None else None,
              "faktor_tren_dipakai": angka_json(f_pakai), "faktor_musim": angka_json(ctx.faktor_musim),
              "rata_rata_dipakai": angka_json(mu_p), "simpangan_dipakai": angka_json(sd_p)})
    h["nilai_stok"] = nilai_stok

    # 2. barang mati / tanpa penjualan
    if tanpa_jual >= a.batas_mati:
        if stok is None or stok > 0:
            h["kelompok"] = "BARANG_MATI"
            h["alasan"] = (f"belum pernah terjual selama {tanpa_jual} hari data" if terakhir_jual is None else
                           f"tidak terjual {tanpa_jual} hari (terakhir {tgl_id(terakhir_jual)})")
            if stok is None:
                h["alasan"] += "; stok belum diketahui (bila masih ada stok, ini barang mati)"
            h["nilai_tertahan"] = nilai_stok
        else:
            h["kelompok"] = "TIDAK_ADA_PENJUALAN"
            h["alasan"] = f"tidak terjual {tanpa_jual} hari dan stok sudah habis: tidak perlu dipesan ulang dulu"
        return h
    if mu_p <= 0:
        h["kelompok"] = "TIDAK_ADA_PENJUALAN"
        h["alasan"] = (f"belum ada penjualan bersih selama {N} hari data (belum {a.batas_mati} hari, jadi belum disebut barang mati)")
        return h

    ss = ctx.z * sd_p * L.sqrt()
    rop_x = mu_p * L + ss
    tgt_x = mu_p * (L + ctx.horizon) + ss
    SS, ROP, TGT = atas(ss), atas(rop_x), atas(tgt_x)
    h.update({"stok_pengaman": SS, "titik_pesan_ulang": ROP, "stok_target": TGT})

    if stok is None:
        h["kelompok"] = "STOK_BELUM_DIKETAHUI"
        h["alasan"] = (f"pesan bila stok tinggal {ROP} atau kurang; jumlah pesan = {TGT} - stok sekarang"
                       + (f" - {des(dp)} dalam pesanan" if dp else ""))
        return h

    posisi = stok + dp
    h["posisi_stok"] = angka_json(posisi)
    if stok < 0:
        h["catatan"].append(f"stok minus ({des(stok)}): kemungkinan terlanjur terjual melebihi stok atau salah catat; "
                            "jumlah pesan ikut menutup kekurangan itu, cocokkan dengan stok fisik")
    habis = 0 if stok <= 0 else bawah(stok / mu_p)
    h["habis_dalam_hari"] = habis
    h["perkiraan_tanggal_habis"] = (ctx.acuan + timedelta(days=habis)).isoformat()
    if posisi <= ROP:
        hari_ke_rop = 0
    else:
        hari_ke_rop = bawah((posisi - ROP) / mu_p)
    if hari_ke_rop < 1:
        h["kelompok"] = "PESAN_SEKARANG"
        kurang = TGT - posisi
        if kurang <= 0:
            kurang = Decimal(1)
        h["tanggal_pesan"] = ctx.acuan.isoformat()
        h["kosong_sebelum_barang_datang"] = Decimal(habis) < L
        if h["kosong_sebelum_barang_datang"]:
            h["catatan"].append(f"stok diperkirakan habis ±{habis} hari lagi, sebelum barang datang ({des(L)} hari)"
                                + ("; kecuali barang yang sedang dipesan datang lebih dulu" if dp else ""))
    elif hari_ke_rop <= JENDELA_MINGGU_DEPAN:
        h["kelompok"] = "PESAN_MINGGU_DEPAN"
        kurang = TGT - (posisi - mu_p * hari_ke_rop)
        h["tanggal_pesan"] = (ctx.acuan + timedelta(days=hari_ke_rop)).isoformat()
    else:
        h["kelompok"] = "AMAN"
        h["tanggal_pesan_berikutnya"] = (ctx.acuan + timedelta(days=hari_ke_rop)).isoformat() if hari_ke_rop <= 365 else None
        if habis > HARI_STOK_BERLEBIH:
            lebih = stok - TGT
            h["stok_berlebih"] = True
            h["kelebihan_stok"] = angka_json(lebih) if lebih > 0 else 0
            h["nilai_kelebihan"] = bulat(lebih * harga) if (harga is not None and lebih > 0) else None
            h["catatan"].append(f"stok cukup untuk ±{habis} hari: jangan ditambah dulu")
        return h
    jumlah, ket = bulatkan_pesan(kurang, kel, moq)
    h["jumlah_pesan_hitungan"] = atas(kurang)
    h["jumlah_pesan"] = angka_json(jumlah)
    h["jumlah_kemasan"] = angka_json(jumlah / kel) if kel and kel > 0 else None
    h["penyesuaian_jumlah"] = ket
    h["nilai_pesanan"] = bulat(jumlah * harga) if harga is not None else None
    return h


def urut_kunci(h):
    k = URUTAN_KELOMPOK.index(h["kelompok"])
    if h["kelompok"] == "BARANG_MATI":
        return (k, -(h.get("nilai_tertahan") or 0), h["nama"].lower())
    if h["kelompok"] == "PESAN_MINGGU_DEPAN":
        return (k, h["tanggal_pesan"] or "", h["nama"].lower())
    habis = h.get("habis_dalam_hari")
    return (k, habis if habis is not None else 10**9, -(h.get("nilai_pesanan") or 0), h["nama"].lower())


def susun_pemasok(hasil, ctx):
    out = []
    for kel in ("PESAN_SEKARANG", "PESAN_MINGGU_DEPAN"):
        grup = {}
        for h in hasil:
            if h["kelompok"] != kel or not h.get("jumlah_pesan"):
                continue
            nama = h["pemasok"] or "Pemasok belum diisi"
            grup.setdefault(nama, []).append(h)
        for nama, isi in sorted(grup.items(), key=lambda x: (x[0] == "Pemasok belum diisi", x[0].lower())):
            nilai = [h["nilai_pesanan"] for h in isi if h["nilai_pesanan"] is not None]
            info = ctx.pemasok.get(kunci_nama(nama), {})
            g = {"pemasok": nama, "kelompok": kel, "barang": [], "total_nilai": sum(nilai),
                 "harga_lengkap": len(nilai) == len(isi),
                 "lead_time_hari": sorted({h["lead_time_hari"] for h in isi}),
                 "minimal_belanja": bulat(info["min_belanja"]) if info.get("min_belanja") else None}
            for h in isi:
                g["barang"].append({"nama": h["nama"], "sku": h["sku"], "jumlah": h["jumlah_pesan"], "satuan": h["satuan"],
                                    "jumlah_kemasan": h.get("jumlah_kemasan"), "kelipatan": h.get("kelipatan"),
                                    "harga_beli": h["harga_beli"], "nilai": h["nilai_pesanan"],
                                    "tanggal_pesan": h["tanggal_pesan"]})
            if g["minimal_belanja"] and g["harga_lengkap"] and g["total_nilai"] < g["minimal_belanja"]:
                g["kurang_dari_minimal_belanja"] = g["minimal_belanja"] - g["total_nilai"]
            if kel == "PESAN_SEKARANG":
                g["draf_wa"] = draf_wa(nama, isi)
            out.append(g)
    return out


def draf_wa(pemasok, isi):
    sapa = "[isian: nama pemasok]" if pemasok == "Pemasok belum diisi" else pemasok
    L = [f"Halo {sapa}, saya [isian: nama Anda] dari [isian: nama toko]. Mau pesan barang berikut:"]
    for i, h in enumerate(isi, start=1):
        label = h["nama"] + (f" ({h['sku']})" if h["sku"] and h["sku"].lower() != h["nama"].lower() else "")
        harga = f", harga terakhir {rp(h['harga_beli'])}/{h['satuan']}" if h["harga_beli"] is not None else ""
        L.append(f"{i}. {label}: {des(h['jumlah_pesan'])} {h['satuan']}{harga}")
    L.append("Mohon dikonfirmasi ketersediaan, total harga, dan perkiraan tanggal kirim. "
             "Bila bisa, barang tiba paling lambat [isian: tanggal]. Terima kasih.")
    return "\n".join(L)


def susun_pertanyaan(hasil, ctx):
    q = []
    aktif = [h for h in hasil if h["kelompok"] in ("PESAN_SEKARANG", "PESAN_MINGGU_DEPAN", "AMAN", "STOK_BELUM_DIKETAHUI")]
    tanpa_stok = [h["nama"] for h in hasil if h["kelompok"] == "STOK_BELUM_DIKETAHUI"]
    if tanpa_stok:
        q.append("Berapa stok sekarang untuk: " + ", ".join(tanpa_stok[:6]) + (f" dan {len(tanpa_stok) - 6} lainnya" if len(tanpa_stok) > 6 else "") + "?")
    if any(h["sumber_lead_time"] == "default" for h in aktif):
        q.append(f"Biasanya berapa hari barang datang sejak dipesan, per pemasok? (sementara dipakai {des(ctx.lead_default)} hari)")
    tanpa_harga = [h["nama"] for h in hasil if h.get("jumlah_pesan") and h["harga_beli"] is None]
    if tanpa_harga:
        q.append("Berapa harga beli terakhir untuk: " + ", ".join(tanpa_harga[:6]) + "?")
    lonj = [(h["nama"], x) for h in hasil for x in h.get("lonjakan", [])]
    if lonj:
        n, x = lonj[0]
        q.append(f"Tanggal {tgl_id(date.fromisoformat(x['tanggal']))} {n} terjual {des(x['terjual'])} (biasanya ±{des(x['biasanya'])}). "
                 "Itu pesanan borongan sekali? Bila ya, hitungan bisa diulang tanpa lonjakan itu.")
    if any(h.get("data_pendek") for h in hasil):
        q.insert(0, f"Ada catatan penjualan yang lebih panjang (minimal {MIN_HARI_DATA} hari, idealnya 2-3 bulan)? "
                    "Dengan itu jumlah pesan per barang bisa dihitung.")
    baru = [h["nama"] for h in hasil if h["kelompok"] == "DATA_BELUM_CUKUP" and not h.get("data_pendek")]
    if baru:
        q.append("Apakah " + ", ".join(baru[:4]) + " barang baru? Bila barang lama yang jarang laku, sebutkan agar dihitung dari awal data.")
    if not ctx.ada_dalam_pesanan and any(h["kelompok"] == "PESAN_SEKARANG" for h in hasil):
        q.append("Ada barang yang sudah dipesan tapi belum datang? Jumlahnya akan dikurangkan dari pesanan.")
    tanpa_pemasok = [h["nama"] for h in hasil if h.get("jumlah_pesan") and not h["pemasok"]]
    if tanpa_pemasok:
        q.append("Barang berikut dipesan ke pemasok mana: " + ", ".join(tanpa_pemasok[:6]) + "?")
    return q


def jalankan(args):
    ctx = Konteks(args)
    if args.layanan not in Z_LAYANAN:
        raise Galat(f"tingkat layanan {args.layanan}% tidak tersedia",
                    "Pilih salah satu: " + ", ".join(f"{k}%" for k in Z_LAYANAN) + " (umum: 90, 95, 99).")
    ctx.z = Z_LAYANAN[args.layanan]
    ctx.lead_default = ke_hari(args.lead_time, "lead time default")
    ctx.horizon = ke_hari(args.horizon, "horizon")
    if ctx.lead_default is None or ctx.horizon is None or ctx.horizon < 1:
        raise Galat("lead time/horizon tidak valid", "Contoh: --lead-time 7 --horizon 14")
    ctx.faktor_musim = ke_angka(args.faktor_musim, "faktor musim")
    if ctx.faktor_musim is None or ctx.faktor_musim <= 0:
        raise Galat("faktor musim harus lebih dari 0", "Contoh: 1,5 bila menjelang musim ramai diperkirakan naik 50%.")
    ctx.mode = args.data_per
    for nama in ("dari", "sampai", "hari_ini"):
        v = getattr(args, nama)
        if v:
            t = ke_tanggal(v)[0]
            if t is None:
                raise Galat(f"tanggal --{nama.replace('_', '-')} '{v}' tidak terbaca", "Contoh: 2026-10-14")
            setattr(args, nama, t)
    gabungan = None
    if args.file:
        rows, gabungan = baca_sumber(path=args.file)
    elif args.data is not None:
        rows, _ = baca_sumber(teks=args.data)
    else:
        rows, _ = baca_sumber(teks=sys.stdin.read())
    if gabungan is not None:
        if not isinstance(gabungan.get("penjualan"), list):
            raise Galat("JSON gabungan tanpa kunci 'penjualan'", "Pakai {\"penjualan\": [...], \"barang\": [...], \"pemasok\": [...]}.")
        rows = baris_dari_json(gabungan["penjualan"])
    olah_penjualan(ctx, rows)
    if gabungan and gabungan.get("pemasok"):
        olah_pemasok(ctx, baris_dari_json(gabungan["pemasok"]))
    if args.pemasok or args.pemasok_data:
        olah_pemasok(ctx, baca_sumber(path=args.pemasok)[0] if args.pemasok else baca_sumber(teks=args.pemasok_data)[0])
    if gabungan and gabungan.get("barang"):
        olah_barang(ctx, baris_dari_json(gabungan["barang"]))
    if args.barang or args.barang_data:
        olah_barang(ctx, baca_sumber(path=args.barang)[0] if args.barang else baca_sumber(teks=args.barang_data)[0])
    if not ctx.tanggal:
        contoh = "; ".join(f"baris {d['baris']} {d['alasan']}" + (f" '{d['nilai']}'" if d["nilai"] else "")
                           for d in ctx.dilewati[:4])
        raise Galat("tidak ada baris penjualan yang terbaca (tanggal/jumlah)" + (f". Contoh: {contoh}" if contoh else ""),
                    "Periksa format tanggal (mis. 2026-09-01 atau 01/09/2026; nama hari saja seperti 'Senin' tidak cukup) "
                    "dan kolom jumlah terjual.")

    awal, akhir = min(ctx.tanggal), max(ctx.tanggal)
    if ctx.mode == "minggu":
        akhir = akhir + timedelta(days=6)
    elif ctx.mode == "bulan":
        awal = awal.replace(day=1)
        akhir = akhir.replace(day=monthrange(akhir.year, akhir.month)[1])
    if args.dari:
        awal = args.dari
    if args.sampai:
        akhir = args.sampai
    if akhir < awal:
        raise Galat("rentang tanggal terbalik (sampai lebih awal dari dari)", "Periksa --dari dan --sampai.")
    ctx.awal, ctx.akhir = awal, akhir
    ctx.acuan = args.hari_ini or akhir
    ctx.ada_dalam_pesanan = any("dalam_pesanan" in it["master"] for it in ctx.barang.values())

    hasil = [hitung_barang(it, ctx) for it in ctx.barang.values()]
    hasil.sort(key=urut_kunci)

    # catatan umum
    c = ctx.catatan
    if ctx.mode == "hari" and ctx.bulan_saja:
        c.append(f"{ctx.bulan_saja} baris hanya berisi bulan (tanpa tanggal). Bila datanya total per bulan, hitung ulang dengan data per bulan.")
    if ctx.bulan_dulu:
        c.append(f"{ctx.bulan_dulu} baris tampak berformat bulan/tanggal (gaya Amerika) dan dibaca begitu"
                 + (f"; {ctx.ambigu} baris lain yang bisa dibaca dua arah dibaca tanggal/bulan. Pastikan formatnya." if ctx.ambigu else "."))
    if ctx.status_lewat:
        c.append("Pesanan tidak dihitung karena status: " + ", ".join(f"{k} ({v})" for k, v in sorted(ctx.status_lewat.items())))
    if ctx.dobel:
        c.append(f"{ctx.dobel} baris dobel (nomor pesanan, barang, tanggal, dan jumlah sama) dihitung sekali.")
    if ctx.di_luar:
        c.append(f"{ctx.di_luar} baris di luar rentang tanggal yang diminta tidak dihitung.")
    if ctx.galat_master:
        c.append("Isian berikut tidak terbaca dan diabaikan: " + "; ".join(sorted(ctx.galat_master)[:8]))
    if args.hari_ini and (args.hari_ini - akhir).days > 3:
        c.append(f"Data penjualan berakhir {tgl_id(akhir)}, {(args.hari_ini - akhir).days} hari sebelum hari ini: pastikan angka stok sudah yang terbaru.")
    if args.hari_ini and args.hari_ini < akhir:
        c.append("Tanggal hari ini lebih awal dari akhir data; perkiraan tanggal memakai tanggal hari ini.")
    if ctx.mode != "hari":
        c.append(f"Data dibaca sebagai total per {ctx.mode}; simpangan harian diturunkan dari variasi antar-{ctx.mode}.")
    tanpa_jual = [it["nama"] for it in ctx.barang.values() if not it["ada_baris"]]
    if tanpa_jual:
        c.append(f"{len(tanpa_jual)} barang di daftar barang tidak muncul sama sekali di data penjualan: "
                 + ", ".join(tanpa_jual[:8]) + (" dan lainnya" if len(tanpa_jual) > 8 else "")
                 + ". Bila sebenarnya barang yang sama dengan nama/SKU berbeda di data penjualan, samakan penulisannya lalu hitung ulang.")
    rentang = (akhir - awal).days + 1
    if rentang < 28:
        c.append(f"Rentang data hanya {rentang} hari: hasil kasar. Data 2-3 bulan memberi hasil lebih andal.")

    ringkas = {k: sum(1 for h in hasil if h["kelompok"] == k) for k in URUTAN_KELOMPOK}
    def jumlah_nilai(kel):
        return sum(h["nilai_pesanan"] or 0 for h in hasil if h["kelompok"] == kel)
    ringkas.update({
        "jumlah_barang": len(hasil),
        "nilai_pesan_sekarang": jumlah_nilai("PESAN_SEKARANG"),
        "nilai_pesan_minggu_depan": jumlah_nilai("PESAN_MINGGU_DEPAN"),
        "nilai_barang_mati": sum(h.get("nilai_tertahan") or 0 for h in hasil if h["kelompok"] == "BARANG_MATI"),
        "harga_belum_lengkap": any(h.get("jumlah_pesan") and h["harga_beli"] is None for h in hasil),
    })
    isian = []
    for h in hasil:
        if h["kelompok"] in ("PESAN_SEKARANG", "PESAN_MINGGU_DEPAN"):
            if h["harga_beli"] is None:
                isian.append(f"harga beli {h['nama']}")
            if not h["pemasok"]:
                isian.append(f"pemasok {h['nama']}")
        if h["kelompok"] == "STOK_BELUM_DIKETAHUI":
            isian.append(f"stok sekarang {h['nama']}")
    laris = sorted((h for h in hasil if h.get("rata_rata_dipakai") and h["kelompok"] in
                    ("PESAN_SEKARANG", "PESAN_MINGGU_DEPAN", "AMAN", "STOK_BELUM_DIKETAHUI")),
                   key=lambda h: -h["rata_rata_dipakai"])[:3]
    return {
        "versi": VERSI,
        "parameter": {"tingkat_layanan_persen": args.layanan, "z": str(ctx.z), "lead_time_default_hari": angka_json(ctx.lead_default),
                      "horizon_hari": angka_json(ctx.horizon), "data_per": ctx.mode, "faktor_musim": angka_json(ctx.faktor_musim),
                      "tren_dipakai": not args.tanpa_tren, "batas_barang_mati_hari": args.batas_mati,
                      "jendela_pesan_minggu_depan_hari": JENDELA_MINGGU_DEPAN},
        "rentang_data": {"dari": awal.isoformat(), "sampai": akhir.isoformat(), "jumlah_hari": rentang,
                         "tanggal_acuan": ctx.acuan.isoformat()},
        "pemetaan_kolom": ctx.pemetaan,
        "ringkasan": ringkas,
        "barang": hasil,
        "pesanan_per_pemasok": susun_pemasok(hasil, ctx),
        "barang_laris_untuk_bundling": [h["nama"] for h in laris],
        "pertanyaan_usulan": susun_pertanyaan(hasil, ctx)[:3],
        "isian_kosong": isian,
        "catatan": c,
        "dilewati": {"jumlah": len(ctx.dilewati), "contoh": ctx.dilewati[:8]},
        "disclaimer": DISCLAIMER,
    }


# ------------------------------------------------------------------ keluaran teks
def baris_barang(h):
    s = h["satuan"]
    teks = f"- {h['nama']}" + (f" ({h['sku']})" if h["sku"] and h["sku"].lower() != h["nama"].lower() else "")
    bag = []
    if h.get("stok_sekarang") is not None:
        bag.append(f"stok {des(h['stok_sekarang'])}" + (f" + {des(h['dalam_pesanan'])} dalam pesanan" if h.get("dalam_pesanan") else ""))
    aktif = h["kelompok"] not in ("BARANG_MATI", "TIDAK_ADA_PENJUALAN", "DATA_BELUM_CUKUP")
    if h.get("rata_rata_dipakai") is not None and aktif:
        tr = h["tren"]
        trs = ""
        if tr in ("naik", "turun"):
            trs = f", tren {tr} {des((Decimal(str(h['faktor_tren'])) - 1) * 100, 0)}%" + ("" if h["faktor_tren_dipakai"] != 1 else " (tidak dipakai)")
        bag.append(f"laku ±{des(h['rata_rata_dipakai'])}/hari{trs}")
    if h.get("habis_dalam_hari") is not None:
        bag.append("sudah habis" if h["habis_dalam_hari"] == 0 else
                   f"habis ±{h['habis_dalam_hari']} hari ({tgl_id(date.fromisoformat(h['perkiraan_tanggal_habis']))})")
    if h.get("jumlah_pesan"):
        kem = f" = {des(h['jumlah_kemasan'])} x {des(h['kelipatan'])}" if h.get("jumlah_kemasan") else ""
        bag.append(f"PESAN {des(h['jumlah_pesan'])} {s}{kem}" + (f" ({'; '.join(h['penyesuaian_jumlah'])})" if h.get("penyesuaian_jumlah") else ""))
        bag.append(rp(h["nilai_pesanan"]) if h["nilai_pesanan"] is not None else "nilai: [isian: harga beli]")
        if h["kelompok"] == "PESAN_MINGGU_DEPAN":
            bag.append(f"pesan ±{tgl_id(date.fromisoformat(h['tanggal_pesan']))}")
    if h.get("titik_pesan_ulang") is not None:
        bag.append(f"pesan ulang bila stok ≤ {h['titik_pesan_ulang']}, stok pengaman {h['stok_pengaman']}, stok target {h['stok_target']}")
    if aktif:
        bag.append(f"pemasok {h['pemasok'] or '-'}, lead time {des(h['lead_time_hari'])} hari ({h['sumber_lead_time']})")
    elif h["pemasok"]:
        bag.append(f"pemasok {h['pemasok']}")
    if h.get("alasan"):
        bag.append(h["alasan"])
    if h.get("pengamatan") and h["pengamatan"]["hari"] > 0 and h["pengamatan"]["laju_sementara_per_hari"] is not None:
        p = h["pengamatan"]
        bag.append(f"teramati {des(p['terjual'])} {s} dalam {p['hari']} hari (laju sementara ±{des(p['laju_sementara_per_hari'])}/hari)"
                   + (f"; dengan laju itu stok habis ±{p['habis_dalam_hari_laju_sementara']} hari" if p.get("habis_dalam_hari_laju_sementara") is not None else "")
                   + "; jumlah pesan belum dihitung")
    if h.get("nilai_tertahan") is not None:
        bag.append(f"modal tertahan {rp(h['nilai_tertahan'])}")
    if h.get("stok_berlebih"):
        bag.append(f"STOK BERLEBIH, kelebihan {des(h['kelebihan_stok'])} {s}" + (f" ({rp(h['nilai_kelebihan'])})" if h.get("nilai_kelebihan") else ""))
    for x in h.get("lonjakan", []):
        bag.append(f"LONJAKAN {x['tanggal']}: {des(x['terjual'])} (biasanya {des(x['biasanya'])})")
    bag += h["catatan"]
    return teks + " | " + " | ".join(bag)


def teks(hasil):
    p, r = hasil["parameter"], hasil["rentang_data"]
    L = [LABEL_AGENT,
         f"RENCANA RESTOK per {tgl_id(date.fromisoformat(r['tanggal_acuan']))} | data {tgl_id(date.fromisoformat(r['dari']))} - "
         f"{tgl_id(date.fromisoformat(r['sampai']))} ({r['jumlah_hari']} hari, per {p['data_per']})",
         f"Asumsi: tingkat layanan {p['tingkat_layanan_persen']}% (z {p['z'].replace('.', ',')}), lead time default "
         f"{des(p['lead_time_default_hari'])} hari, stok cukup {des(p['horizon_hari'])} hari setelah barang datang, "
         f"faktor musim {des(p['faktor_musim'])}, barang mati = tidak laku >= {p['batas_barang_mati_hari']} hari", ""]
    ring = hasil["ringkasan"]
    L.append(f"RINGKASAN: {ring['jumlah_barang']} barang | pesan sekarang {ring['PESAN_SEKARANG']} ({rp(ring['nilai_pesan_sekarang'])}"
             f"{', sebagian harga belum ada' if ring['harga_belum_lengkap'] else ''}) | minggu depan {ring['PESAN_MINGGU_DEPAN']} "
             f"({rp(ring['nilai_pesan_minggu_depan'])}) | aman {ring['AMAN']} | barang mati {ring['BARANG_MATI']} "
             f"(modal tertahan {rp(ring['nilai_barang_mati'])})")
    for kel in URUTAN_KELOMPOK:
        isi = [h for h in hasil["barang"] if h["kelompok"] == kel]
        if not isi:
            continue
        L += ["", f"{LABEL_KELOMPOK[kel]} ({len(isi)})"]
        batas = 12 if kel == "AMAN" else len(isi)
        L += [baris_barang(h) for h in isi[:batas]]
        if len(isi) > batas:
            L.append(f"  ... dan {len(isi) - batas} barang aman lainnya")
    if hasil["pesanan_per_pemasok"]:
        L += ["", "PESANAN PER PEMASOK"]
        for g in hasil["pesanan_per_pemasok"]:
            tot = rp(g["total_nilai"]) + ("" if g["harga_lengkap"] else " + [isian: harga yang belum ada]")
            L.append(f"* {g['pemasok']} - {LABEL_KELOMPOK[g['kelompok']]} - total {tot}"
                     + (f" | KURANG {rp(g['kurang_dari_minimal_belanja'])} dari minimal belanja {rp(g['minimal_belanja'])}"
                        if g.get("kurang_dari_minimal_belanja") else ""))
            for b in g["barang"]:
                L.append(f"    {b['nama']}: {des(b['jumlah'])} {b['satuan']} = {rp(b['nilai']) if b['nilai'] is not None else '[isian: harga beli]'}")
            if g.get("draf_wa"):
                L.append("  Draf WA:")
                L += ["    " + x for x in g["draf_wa"].split("\n")]
    if hasil["barang_laris_untuk_bundling"]:
        L += ["", "Barang paling laris (untuk paket bundling barang mati): " + ", ".join(hasil["barang_laris_untuk_bundling"])]
    if hasil["pertanyaan_usulan"]:
        L += ["", "PERTANYAAN USULAN (maks 3):"] + [f"  {i}. {q}" for i, q in enumerate(hasil["pertanyaan_usulan"], 1)]
    if hasil["isian_kosong"]:
        L += ["", "ISIAN KOSONG: " + "; ".join(hasil["isian_kosong"])]
    L += ["", "CATATAN"] + [f"  - {x}" for x in hasil["catatan"]]
    if True:
        if hasil["dilewati"]["jumlah"]:
            cont = "; ".join(f"baris {d['baris']} {d['alasan']}" + (f" '{d['nilai']}'" if d["nilai"] else "")
                             for d in hasil["dilewati"]["contoh"])
            L.append(f"  - {hasil['dilewati']['jumlah']} baris dilewati: {cont}")
    pk = hasil["pemetaan_kolom"]
    if pk.get("penjualan"):
        L.append("  - Kolom penjualan dipakai: " + ", ".join(f"{k}='{v}'" for k, v in pk["penjualan"].items()))
    L += ["", hasil["disclaimer"]]
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Rencana restok dari riwayat penjualan (Decimal, Rupiah).")
    ap.add_argument("--file", help="riwayat penjualan: CSV/TSV/teks tabel/XLSX/JSON (kolom minimal tanggal, sku/nama, qty)")
    ap.add_argument("--data", help="riwayat penjualan sebagai teks (baris dipisah \\n)")
    ap.add_argument("--barang", help="data barang: sku/nama + stok, lead_time, harga_beli, pemasok, dalam_pesanan, kelipatan, moq, mulai_jual")
    ap.add_argument("--barang-data", help="data barang sebagai teks")
    ap.add_argument("--pemasok", help="data pemasok: pemasok, lead_time, minimal_belanja")
    ap.add_argument("--pemasok-data", help="data pemasok sebagai teks")
    ap.add_argument("--lead-time", default="7", help="lead time default (hari) bila tidak ada per barang/pemasok (default 7)")
    ap.add_argument("--layanan", type=int, default=95, help="tingkat layanan persen: 90, 95 (default), 99; juga 80, 85, 97, 98")
    ap.add_argument("--horizon", default="14", help="berapa hari stok harus cukup setelah barang datang (default 14)")
    ap.add_argument("--data-per", choices=["hari", "minggu", "bulan"], default="hari",
                    help="baris data = penjualan per transaksi/hari (default), total per minggu, atau total per bulan")
    ap.add_argument("--faktor-musim", default="1", help="pengali permintaan dari pengguna, mis. 1,5 menjelang musim ramai")
    ap.add_argument("--tanpa-tren", action="store_true", help="jangan pakai tren 4 minggu terakhir")
    ap.add_argument("--abaikan-lonjakan", action="store_true", help="ganti hari lonjakan (borongan sekali) dengan nilai biasanya")
    ap.add_argument("--batas-mati", type=int, default=60, help="hari tanpa penjualan untuk disebut barang mati (default 60)")
    ap.add_argument("--dari", help="hanya pakai data mulai tanggal ini")
    ap.add_argument("--sampai", help="data dianggap mencakup sampai tanggal ini (hari tanpa penjualan dihitung 0)")
    ap.add_argument("--hari-ini", help="tanggal acuan stok sekarang (default: tanggal terakhir data)")
    ap.add_argument("--format", choices=["json", "teks"], default="json")
    args = ap.parse_args(argv)
    try:
        hasil = jalankan(args)
    except Galat as g:
        print(json.dumps({"error": g.pesan, "saran": g.saran}, ensure_ascii=False), file=sys.stderr)
        return 2
    if args.format == "teks":
        print(teks(hasil))
    else:
        print(json.dumps(hasil, ensure_ascii=False, indent=2, default=str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
