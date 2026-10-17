#!/usr/bin/env python3
"""kasir-lokal - kasir UMKM satu outlet di komputer sendiri (SQLite, tanpa internet, Python standar).

Dioperasikan oleh AI agent lewat chat. Setiap perintah tulis hanya PRATINJAU sampai diberi --ya.

Contoh:
  python3 kasir.py init --nama-toko "Kedai Contoh" --ya
  python3 kasir.py produk impor produk.csv --ya
  python3 kasir.py jual --pesan "2 kopi susu, 1 roti bakar, diskon 10%, bayar tunai 100rb" --json
  python3 kasir.py struk --nota N-260924-0001 --kertas 58
  python3 kasir.py rekap --tanggal hari-ini
Windows: ganti python3 dengan python atau py.

Lokasi database (urutan prioritas):
  1. --db PATH
  2. ENV KOMUNITECH_KASIR_DB (path file lengkap)
  3. ENV KOMUNITECH_DATA (folder) + /kasir/kasir.db
  4. ~/KomunitechData/kasir/kasir.db

Pembulatan (standar library Komunitech):
  - Total baris & diskon: dibulatkan ke rupiah terdekat (0,5 ke atas).
  - PPN 12% dengan DPP nilai lain 11/12 = 11% x DPP, dihitung per nota dari DPP persis lalu
    dibulatkan KE BAWAH sekali. Mode harga termasuk PPN: DPP = rupiah bulat terbesar dengan
    DPP + PPN <= harga; sisanya ditampilkan sebagai selisih pembulatan.
  - Belum dicocokkan dengan Coretax.
"""
import argparse
import csv
import difflib
import hashlib
import html
import io
import json
import os
import re
import math
import shutil
import sqlite3
import sys
import tempfile
import unicodedata
from datetime import date, datetime, timedelta, timezone
from fractions import Fraction
from decimal import Decimal, InvalidOperation, ROUND_FLOOR, ROUND_HALF_UP
from pathlib import Path

APLIKASI = "kasir-lokal"
VERSI = "1.1.8"


def _timeout():
    try:
        return max(0.1, float(os.environ.get("KOMUNITECH_KASIR_TIMEOUT", "15")))
    except ValueError:
        return 15.0


PESAN_TERKUNCI = ("Database kasir sedang dipakai program lain (mis. jadwal OpenClaw atau jendela lain) dan "
                  "tidak selesai dalam %d detik. Data aman, tidak rusak. Tunggu sebentar lalu ulangi perintah yang "
                  "sama. Jangan hapus file database.")
SATUAN_PECAHAN = {"kg", "kilo", "kilogram", "gram", "gr", "g", "ons", "liter", "ltr", "l", "ml", "cc", "meter", "m",
                  "cm", "m2", "meter2", "m3", "meter3", "kubik", "ton", "kwintal"}
# Kata satuan umum (selain satuan yang ada di tabel produk). Dipakai hanya untuk MEMBUANG kata satuan dari pesanan.
SATUAN_UMUM = {"pcs", "buah", "bh", "biji", "unit", "porsi", "cup", "gelas", "bungkus", "bks", "botol", "btl", "sak",
               "zak", "dus", "dos", "karton", "pak", "pack", "box", "lembar", "lbr", "batang", "btg", "rol", "roll",
               "pail", "ikat", "lusin", "kodi", "set", "pasang", "psg", "kaleng", "sachet", "renteng", "tray", "rim",
               "galon", "tabung", "piring", "mangkok", "potong", "ekor", "sisir", "papan", "keping"}
# Satuan hitung generik: boleh dipakai untuk produk bersatuan hitung apa pun (1 buah = 1 pcs = 1 porsi dst.)
SATUAN_GENERIK = {"pcs", "buah", "bh", "biji", "unit"}
ALIAS_SATUAN = {"kilo": "kg", "kilogram": "kg", "gr": "gram", "g": "gram", "ltr": "liter", "l": "liter",
                "meter": "m", "meter2": "m2", "meter3": "m3", "kubik": "m3", "zak": "sak", "dos": "dus",
                "pack": "pak", "roll": "rol", "lbr": "lembar", "btg": "batang", "btl": "botol", "bks": "bungkus",
                "psg": "pasang", "bh": "buah"}
MODE_PAJAK = ("tanpa", "ppn-belum", "ppn-termasuk", "pbjt-belum", "pbjt-termasuk")
# Zona waktu Indonesia (tanpa musim panas -> offset tetap selalu benar; dipakai bila tzdata tidak ada, mis. Windows)
ZONA = {"Asia/Jakarta": (7, "WIB"), "Asia/Pontianak": (7, "WIB"), "Asia/Makassar": (8, "WITA"),
        "Asia/Jayapura": (9, "WIT")}
ALIAS_ZONA = {"wib": "Asia/Jakarta", "wita": "Asia/Makassar", "wit": "Asia/Jayapura"}
MODE_STOK = ("tidak", "kasir", "buku-stok")
LABEL_PAJAK = {"tanpa": "tanpa pajak", "ppn-belum": "PPN 12% (harga produk belum termasuk PPN)",
               "ppn-termasuk": "PPN 12% (harga produk sudah termasuk PPN)",
               "pbjt-belum": "PBJT makanan/minuman %s%% (harga menu belum termasuk PBJT)",
               "pbjt-termasuk": "PBJT makanan/minuman %s%% (harga menu sudah termasuk PBJT)"}
METODE = [  # (label, kata kunci)
    ("Tunai", ["tunai", "cash", "kontan", "cas"]),
    ("QRIS", ["qris", "qr"]),
    ("Transfer", ["transfer", "tf", "trf", "bank"]),
    ("Debit", ["debit", "edc"]),
    ("Kartu kredit", ["kartu kredit", "kredit", "cc"]),
    ("E-wallet", ["e-wallet", "ewallet", "ovo", "gopay", "dana", "shopeepay", "linkaja"]),
    ("Lainnya", ["lainnya", "voucher"]),
]
KATA_BON = re.compile(r"\b(bon|ngebon|utang|hutang|kasbon|nanti\s+bayar|bayar\s+nanti|tempo)\b")
ANGKA_KATA = {"satu": 1, "se": 1, "dua": 2, "tiga": 3, "empat": 4, "lima": 5, "enam": 6, "tujuh": 7,
              "delapan": 8, "sembilan": 9, "sepuluh": 10, "setengah": Decimal("0.5")}
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
BULAN = ["", "JANUARI", "FEBRUARI", "MARET", "APRIL", "MEI", "JUNI", "JULI", "AGUSTUS", "SEPTEMBER",
         "OKTOBER", "NOVEMBER", "DESEMBER"]
DISCLAIMER_PBJT = ("Dasar: UU 1/2022 (HKPD) Pasal 50 huruf a, 51, 56, 57 ayat (1), 58 ayat (1) & (4); tarif sesuai Perda "
                   "daerah Anda (paling tinggi 10%); berlaku per 24 September 2026. Pembulatan belum dicocokkan dengan "
                   "sistem pajak daerah/Bapenda. Alat bantu catat, bukan nasihat pajak; tanyakan Bapenda setempat.")
DISCLAIMER_PAJAK = ("Dasar: UU HPP & PMK 131/2024 (PPN 12%, DPP nilai lain 11/12); PP 55/2022 jo. PP 20/2026 "
                    "(PPh final 0,5%); berlaku per 24 September 2026. Pembulatan belum dicocokkan dengan Coretax. "
                    "Alat bantu catat, bukan nasihat pajak; hubungi DJP (Kring Pajak 1500200) atau konsultan pajak.")


class Gagal(Exception):
    def __init__(self, pesan, **detail):
        super().__init__(pesan)
        self.pesan = pesan
        self.detail = detail


# --------------------------------------------------------------------------- angka & format
def _cek_ribuan(bagian, asli, nama):
    if not (1 <= len(bagian[0]) <= 3) or any(len(b) != 3 for b in bagian[1:]):
        raise Gagal("%s: '%s' tidak dikenali. Tulis dengan titik untuk ribuan dan koma untuk desimal, "
                    "mis. 15.000 atau 1,5." % (nama, asli))


def parse_angka(nilai, nama="angka"):
    """'Rp 15.000' / '15.000,50' / '100rb' / '1,5jt' / '1,5' -> Decimal. Format ragu ditolak (Gagal)."""
    if nilai is None:
        raise Gagal("%s kosong." % nama)
    if isinstance(nilai, (int, Decimal)):
        return Decimal(nilai)
    asli = str(nilai)
    s = asli.strip().lower().replace("\u00a0", "").replace(" ", "")
    if re.search(r"\de[+-]?\d", s):
        raise Gagal("%s: '%s' berformat ilmiah (dari Excel). Ubah kolomnya ke format Angka/Teks lalu simpan ulang."
                    % (nama, asli))
    s = re.sub(r"^(rp|idr)\.?", "", s)
    s = re.sub(r"[,.]-+$", "", s)
    pengali = 1
    for akhiran, kali in (("ribu", 1000), ("rb", 1000), ("k", 1000), ("juta", 10 ** 6), ("jt", 10 ** 6)):
        if s.endswith(akhiran):
            s, pengali = s[: -len(akhiran)], kali
            break
    negatif = s.startswith("-")
    if negatif:
        s = s[1:]
    if not s or not re.fullmatch(r"[\d.,]+", s) or not re.search(r"\d", s):
        raise Gagal("%s: '%s' bukan angka yang valid." % (nama, asli))
    if "," in s and "." in s:
        if s.rfind(",") < s.rfind("."):
            raise Gagal("%s: '%s' memakai format Inggris. Tulis 1.250.000,50 (titik ribuan, koma desimal)."
                        % (nama, asli))
        utuh, _, pecahan = s.rpartition(",")
        _cek_ribuan(utuh.split("."), asli, nama)
        s = utuh.replace(".", "") + "." + pecahan
    elif "," in s:
        bagian = s.split(",")
        if len(bagian) == 2:
            s = (bagian[0] or "0") + "." + bagian[1]
        else:
            _cek_ribuan(bagian, asli, nama)
            s = s.replace(",", "")
    elif "." in s:
        bagian = s.split(".")
        if len(bagian) == 2 and (len(bagian[1]) != 3 or bagian[0] in ("", "0")):
            if pengali == 1 and len(bagian[1]) == 2 and nama.lower().startswith(("harga", "bayar", "kas", "setor")):
                raise Gagal("%s: '%s' meragukan (titik diikuti 2 angka). Tulis 15.000 atau 15000." % (nama, asli))
            s = (bagian[0] or "0") + "." + bagian[1]
        else:
            _cek_ribuan(bagian, asli, nama)
            s = s.replace(".", "")
    try:
        d = Decimal(s) * pengali
    except InvalidOperation:
        raise Gagal("%s: '%s' bukan angka yang valid." % (nama, asli))
    return -d if negatif else d


def rupiah_bulat(nilai, nama):
    """Nominal uang -> int rupiah. Pecahan sen ditolak (kecuali ,00)."""
    d = parse_angka(nilai, nama)
    if d != d.to_integral_value():
        raise Gagal("%s: '%s' punya pecahan sen. Kasir mencatat rupiah bulat; tulis tanpa sen." % (nama, nilai))
    return int(d)


def rhu(d):
    """Pembulatan ke rupiah terdekat (0,5 ke atas)."""
    return int(Decimal(d).quantize(Decimal(1), ROUND_HALF_UP))


def fmt_angka(n):
    n = int(n)
    return ("-" if n < 0 else "") + "{:,}".format(abs(n)).replace(",", ".")


def fmt_rp(n):
    n = int(n)
    return ("-" if n < 0 else "") + "Rp " + fmt_angka(abs(n))


def fmt_qty(q):
    q = Decimal(str(q)).normalize()
    t = "{:f}".format(q)
    if "." in t:
        t = t.rstrip("0").rstrip(".")
    return t.replace(".", ",")


def angka_json(q):
    q = Decimal(str(q))
    return int(q) if q == q.to_integral_value() else float(q)


def norm(t):
    t = str(t or "").casefold().replace("\u00a0", " ")
    t = re.sub(r"[^\w%]+", " ", t)
    return " ".join(t.split())


# --------------------------------------------------------------------------- pajak (inti)
def jenis_pajak(mode):
    return "PPN" if mode.startswith("ppn") else ("PBJT" if mode.startswith("pbjt") else "")


def tarif_efektif(mode, tarif=None):
    """Fraction. PPN: 11/100 (= 12% x 11/12). PBJT: tarif Perda / 100 (dasar = jumlah dibayar, tanpa 11/12)."""
    if mode.startswith("ppn"):
        return Fraction(11, 100)
    if mode.startswith("pbjt"):
        if tarif in (None, ""):
            raise Gagal("Tarif PBJT belum diatur (atur --tarif-pbjt N sesuai Perda daerah Anda).")
        return Fraction(Decimal(str(tarif))) / 100
    return Fraction(0)


def hitung_pajak(netto, mode, tarif=None):
    """netto = total harga setelah semua diskon (int rupiah). Kembalikan dict dpp, ppn, total, sisa.
    Kunci 'ppn' = jumlah pajak (PPN atau PBJT sesuai mode); 'dpp' = dasar pengenaan.

    *-belum   : dasar = netto; pajak = floor(r x dasar); total = dasar + pajak.
    *-termasuk: dasar = rupiah bulat terbesar dengan dasar + floor(r x dasar) <= netto; total = netto;
                sisa = netto - dasar - pajak (selisih pembulatan, biasanya Rp 0-1).
    PPN: r = 11% (identik 12% x 11/12, satu kali pembulatan). PBJT: r = tarif Perda (Pasal 57-59 UU 1/2022).
    Pajak selalu dibulatkan KE BAWAH sekali (tidak pernah memungut melebihi tarif).
    """
    netto = int(netto)
    if mode == "tanpa" or netto == 0:
        return {"dpp": netto, "ppn": 0, "total": netto, "sisa": 0}
    if netto < 0:
        h = hitung_pajak(-netto, mode, tarif)
        return {k: -v for k, v in h.items()}
    r = tarif_efektif(mode, tarif)
    if mode.endswith("-belum"):
        pj = math.floor(netto * r)
        return {"dpp": netto, "ppn": pj, "total": netto + pj, "sisa": 0}
    if mode.endswith("-termasuk"):
        dpp = math.floor(netto / (1 + r)) + 2
        while dpp > 0 and dpp + math.floor(dpp * r) > netto:
            dpp -= 1
        pj = math.floor(dpp * r)
        return {"dpp": dpp, "ppn": pj, "total": netto, "sisa": netto - dpp - pj}
    raise Gagal("Mode pajak tidak dikenal: %s" % mode)


def hitung_total(netto, mode, tarif=None, sc_persen=None, sc_kena=None):
    """Tambah service charge (opsional) lalu pajak.
    service = rupiah terdekat dari sc% x netto (setelah diskon). Hanya mode tanpa/*-belum.
    Dasar pajak = netto + service bila sc_kena (ditentukan pemilik sesuai Perda/aturan), selain itu netto saja.
    """
    netto = int(netto)
    sc = rhu(Decimal(netto) * Decimal(str(sc_persen)) / 100) if sc_persen not in (None, "", "0") else 0
    if sc and mode.endswith("-termasuk"):
        raise Gagal("Service charge tidak bisa dipakai dengan harga termasuk pajak. Pakai mode *-belum.")
    kena = sc if (sc and sc_kena) else 0
    h = hitung_pajak(netto + kena, mode, tarif)
    h["total"] += sc - kena
    h["service"] = sc
    return h


def dpp_nilai_lain(dpp):
    return (Decimal(int(dpp)) * 11 / 12).quantize(Decimal("0.01"), ROUND_HALF_UP)


# --------------------------------------------------------------------------- diskon
def parse_diskon(teks, nama="diskon"):
    """'10%' / '5rb' / '10%+5%' -> list of ('persen'|'nominal', Decimal)."""
    t = str(teks or "").strip().lower()
    if not t:
        return []
    hasil = []
    for bag in re.split(r"\s*\+\s*", t):
        bag = bag.strip()
        if not bag:
            continue
        if bag.endswith("%"):
            p = parse_angka(bag[:-1], nama)
            if p <= 0 or p > 100:
                raise Gagal("%s %s%% tidak masuk akal (harus lebih dari 0 dan paling besar 100%%)." % (nama, fmt_qty(p)))
            hasil.append(("persen", p))
        else:
            n = parse_angka(bag, nama)
            if n <= 0 or n != n.to_integral_value():
                raise Gagal("%s '%s' harus rupiah bulat lebih dari 0." % (nama, bag))
            hasil.append(("nominal", n))
    return hasil


def terapkan_diskon(jumlah, spek, nama):
    """Diskon bertingkat: tiap langkah dihitung dari sisa sebelumnya, dibulatkan ke rupiah terdekat."""
    sisa = int(jumlah)
    langkah = []
    for jenis, v in spek:
        d = rhu(Decimal(sisa) * v / 100) if jenis == "persen" else int(v)
        if d > sisa:
            raise Gagal("%s %s lebih besar dari harga yang didiskon (%s)." % (nama, fmt_rp(d), fmt_rp(sisa)))
        langkah.append({"jenis": jenis, "nilai": angka_json(v), "potongan": d,
                        "label": (fmt_qty(v) + "%") if jenis == "persen" else fmt_rp(int(v))})
        sisa -= d
    return int(jumlah) - sisa, langkah


def alokasi(total, bobot):
    """Bagi 'total' ke baris sesuai bobot (sisa terbesar); jumlah hasil == total persis."""
    s = sum(bobot)
    if total == 0 or s == 0:
        return [0] * len(bobot)
    dasar = [total * b // s for b in bobot]
    sisa = total - sum(dasar)
    urut = sorted(range(len(bobot)), key=lambda i: (-((total * bobot[i]) % s), i))
    for i in urut[:sisa]:
        dasar[i] += 1
    return dasar


def label_diskon(langkah):
    return "+".join(x["label"] for x in langkah)


# --------------------------------------------------------------------------- waktu
_ZONA_AKTIF = {"nama": "Asia/Jakarta"}


def normal_zona(teks):
    t = str(teks or "").strip()
    z = ALIAS_ZONA.get(t.lower(), None)
    if not z:
        z = next((k for k in ZONA if k.lower() == t.lower()), None)
    if not z:
        raise Gagal("Zona waktu '%s' tidak dikenal. Pilihan: WIB (Asia/Jakarta), WITA (Asia/Makassar), WIT "
                    "(Asia/Jayapura), Asia/Pontianak." % teks)
    return z


def tz_zona(nama):
    """ZoneInfo bila tersedia; bila tzdata tidak ada (mis. Windows tanpa paket tzdata) pakai offset tetap."""
    try:
        from zoneinfo import ZoneInfo
        return ZoneInfo(nama)
    except Exception:
        jam, label = ZONA[nama]
        return timezone(timedelta(hours=jam), label)


def offset_zona(nama):
    jam = ZONA[nama][0]
    return "+%02d:00" % jam


def label_zona(offset):
    return {"+07:00": "WIB", "+08:00": "WITA", "+09:00": "WIT"}.get(offset or "", "")


def offset_komputer():
    """Selisih jam komputer terhadap UTC (untuk peringatan bila berbeda dengan zona toko)."""
    return datetime.now().astimezone().utcoffset() or timedelta(0)


def sekarang(args):
    """Waktu SEKARANG menurut zona toko (bukan zona komputer), tanpa info zona (disimpan terpisah)."""
    s = getattr(args, "hari_ini", None)
    if s:
        return parse_waktu(s)
    return datetime.now(tz_zona(_ZONA_AKTIF["nama"])).replace(tzinfo=None, microsecond=0)


def parse_waktu(teks):
    t = str(teks).strip().replace("T", " ")
    m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})(?:\s+(\d{1,2})[:.](\d{2})(?:[:.](\d{2}))?)?", t)
    if not m:
        m2 = re.fullmatch(r"(\d{1,2})[/-](\d{1,2})[/-](\d{4})(?:\s+(\d{1,2})[:.](\d{2})(?:[:.](\d{2}))?)?", t)
        if not m2:
            raise Gagal("Waktu '%s' tidak dikenali. Contoh: 2026-09-24 10:15 atau 24/09/2026 10.15" % teks)
        g = m2.groups()
        parts = (g[2], g[1], g[0], g[3], g[4], g[5])
    else:
        parts = m.groups()
    try:
        return datetime(int(parts[0]), int(parts[1]), int(parts[2]), int(parts[3] or 0), int(parts[4] or 0),
                        int(parts[5] or 0))
    except ValueError:
        raise Gagal("Waktu '%s' tidak valid." % teks)


def parse_tanggal(teks, args):
    t = str(teks or "").strip().lower()
    kini = sekarang(args).date()
    if t in ("", "hari-ini", "hari ini", "hariini", "today"):
        return kini
    if t in ("kemarin", "yesterday"):
        return kini - timedelta(days=1)
    return parse_waktu(t).date()


def parse_bulan(teks, args):
    t = str(teks or "").strip().lower()
    kini = sekarang(args).date()
    if t in ("", "ini", "bulan-ini", "bulan ini"):
        return kini.year, kini.month
    if t in ("lalu", "bulan-lalu", "bulan lalu"):
        d = kini.replace(day=1) - timedelta(days=1)
        return d.year, d.month
    m = re.fullmatch(r"(\d{4})-(\d{1,2})", t) or None
    if m:
        y, b = int(m.group(1)), int(m.group(2))
    else:
        m = re.fullmatch(r"(\d{1,2})[/-](\d{4})", t)
        if not m:
            raise Gagal("Bulan '%s' tidak dikenali. Contoh: 2026-09, 09/2026, ini, lalu." % teks)
        y, b = int(m.group(2)), int(m.group(1))
    if not 1 <= b <= 12:
        raise Gagal("Bulan '%s' tidak valid." % teks)
    return y, b


def tgl_id(d):
    return d.strftime("%d/%m/%Y")


# --------------------------------------------------------------------------- database
SKEMA = """
CREATE TABLE IF NOT EXISTS meta (kunci TEXT PRIMARY KEY, nilai TEXT);
CREATE TABLE IF NOT EXISTS produk (
  id INTEGER PRIMARY KEY, kode TEXT NOT NULL UNIQUE COLLATE NOCASE, nama TEXT NOT NULL,
  varian TEXT NOT NULL DEFAULT '', harga INTEGER NOT NULL, satuan TEXT NOT NULL DEFAULT 'pcs',
  stok REAL, aktif INTEGER NOT NULL DEFAULT 1, dibuat TEXT, diubah TEXT);
CREATE TABLE IF NOT EXISTS sesi (
  id INTEGER PRIMARY KEY, buka TEXT NOT NULL, kas_awal INTEGER NOT NULL, kasir TEXT NOT NULL DEFAULT '',
  tutup TEXT, kas_seharusnya INTEGER, kas_fisik INTEGER, selisih INTEGER, setoran INTEGER, catatan TEXT);
CREATE TABLE IF NOT EXISTS nota (
  id INTEGER PRIMARY KEY, no TEXT NOT NULL UNIQUE, jenis TEXT NOT NULL, waktu TEXT NOT NULL,
  ref_nota_id INTEGER, pajak_mode TEXT NOT NULL, bruto INTEGER NOT NULL, diskon_item INTEGER NOT NULL,
  diskon_nota INTEGER NOT NULL, diskon_nota_label TEXT NOT NULL DEFAULT '', netto INTEGER NOT NULL,
  dpp INTEGER NOT NULL, ppn INTEGER NOT NULL, sisa INTEGER NOT NULL, total INTEGER NOT NULL,
  bayar INTEGER NOT NULL, kembalian INTEGER NOT NULL, kasir TEXT NOT NULL DEFAULT '', catatan TEXT NOT NULL DEFAULT '',
  alasan TEXT NOT NULL DEFAULT '', sidik TEXT, sesi_id INTEGER, dicetak INTEGER NOT NULL DEFAULT 0, dibuat TEXT,
  tarif_pajak TEXT, service INTEGER NOT NULL DEFAULT 0, service_persen TEXT, service_kena INTEGER, zona TEXT);
CREATE TABLE IF NOT EXISTS nota_item (
  id INTEGER PRIMARY KEY, nota_id INTEGER NOT NULL, urut INTEGER NOT NULL, produk_id INTEGER, kode TEXT, nama TEXT,
  varian TEXT, satuan TEXT, qty REAL NOT NULL, harga INTEGER NOT NULL, bruto INTEGER NOT NULL,
  diskon_item INTEGER NOT NULL, diskon_item_label TEXT NOT NULL DEFAULT '', diskon_nota INTEGER NOT NULL,
  netto INTEGER NOT NULL, ref_item_id INTEGER);
CREATE TABLE IF NOT EXISTS bayar (id INTEGER PRIMARY KEY, nota_id INTEGER NOT NULL, metode TEXT NOT NULL,
  jumlah INTEGER NOT NULL);
CREATE TABLE IF NOT EXISTS kas (id INTEGER PRIMARY KEY, sesi_id INTEGER NOT NULL, waktu TEXT, jumlah INTEGER NOT NULL,
  catatan TEXT);
CREATE TABLE IF NOT EXISTS stok_mutasi (id INTEGER PRIMARY KEY, waktu TEXT, produk_id INTEGER, perubahan REAL,
  stok_sesudah REAL, sebab TEXT, nota_id INTEGER, catatan TEXT);
CREATE TABLE IF NOT EXISTS log (id INTEGER PRIMARY KEY, waktu TEXT, perintah TEXT, ringkasan TEXT);
CREATE INDEX IF NOT EXISTS i_nota_waktu ON nota(waktu);
CREATE INDEX IF NOT EXISTS i_item_nota ON nota_item(nota_id);
"""
PENGATURAN_DEFAULT = {"nama_toko": "", "alamat": "", "telp": "", "footer": "Terima kasih", "pajak": "tanpa",
                      "pkp": "tidak", "stok": "tidak", "kertas": "58", "npwp": "", "tarif_pbjt": "",
                      "service_persen": "0", "service_kena_pajak": "", "zona": "Asia/Jakarta"}
KOLOM_BARU_NOTA = [("tarif_pajak", "TEXT"), ("service", "INTEGER NOT NULL DEFAULT 0"), ("service_persen", "TEXT"),
                   ("service_kena", "INTEGER"), ("zona", "TEXT")]


def path_db(args):
    if getattr(args, "db", None):
        return Path(args.db).expanduser()
    env = os.environ.get("KOMUNITECH_KASIR_DB")
    if env:
        return Path(env).expanduser()
    folder = os.environ.get("KOMUNITECH_DATA")
    if folder:
        return Path(folder).expanduser() / "kasir" / "kasir.db"
    return Path.home() / "KomunitechData" / "kasir" / "kasir.db"


def _terkunci(e):
    s = str(e).lower()
    return "locked" in s or "busy" in s


def buka(db, harus_ada=True):
    if harus_ada and not db.is_file():
        raise Gagal("Buku kasir belum ada di %s. Pemakaian pertama: bila pengguna sudah mengirim file produk, jalankan "
                    "kasir.py mulai --produk FILE --nama-toko \"...\" [--pesan \"<kalimat penjualan>\"] (pratinjau dulu, "
                    "ulangi sama persis + --ya setelah pengguna setuju). Tanpa file produk: kasir.py init --nama-toko "
                    "\"...\" lalu --ya." % db, db=str(db))
    try:
        conn = sqlite3.connect(str(db), isolation_level=None, timeout=_timeout())
    except sqlite3.OperationalError as e:
        raise Gagal("Database %s tidak bisa dibuka (%s). Periksa folder/izin aksesnya." % (db, e))
    conn.row_factory = sqlite3.Row
    if harus_ada:
        try:
            r = conn.execute("SELECT nilai FROM meta WHERE kunci='aplikasi'").fetchone()
        except sqlite3.OperationalError as e:
            conn.close()
            if _terkunci(e):
                raise Gagal(PESAN_TERKUNCI % _timeout())
            raise Gagal("File %s bukan database kasir-lokal (%s). Jangan timpa file ini." % (db, e))
        except sqlite3.DatabaseError:
            conn.close()
            raise Gagal("File %s bukan database kasir-lokal atau rusak. Pulihkan dari folder backup-kasir." % db)
        if not r or r[0] != APLIKASI:
            conn.close()
            raise Gagal("File %s bukan database kasir-lokal." % db)
        try:
            ada = {x[1] for x in conn.execute("PRAGMA table_info(nota)")}
            for k, tipe in KOLOM_BARU_NOTA:      # pembaruan otomatis database v1.0.0 (angka lama tidak berubah)
                if k not in ada:
                    conn.execute("ALTER TABLE nota ADD COLUMN %s %s" % (k, tipe))
            z = conn.execute("SELECT nilai FROM meta WHERE kunci='zona'").fetchone()
            _ZONA_AKTIF["nama"] = z[0] if z and z[0] in ZONA else "Asia/Jakarta"
        except sqlite3.OperationalError as e:
            conn.close()
            if _terkunci(e):
                raise Gagal(PESAN_TERKUNCI % _timeout())
            raise
    return conn


def pengaturan(conn):
    cfg = dict(PENGATURAN_DEFAULT)
    for r in conn.execute("SELECT kunci, nilai FROM meta"):
        cfg[r[0]] = r[1]
    return cfg


def buat_backup(db, label):
    if not db.is_file():
        return None
    fol = db.parent / "backup-kasir"
    fol.mkdir(parents=True, exist_ok=True)
    cap = datetime.now().strftime("%Y%m%d-%H%M%S")
    tujuan = fol / ("kasir-%s-%s.db" % (cap, label))
    n = 2
    while tujuan.exists():
        tujuan = fol / ("kasir-%s-%s-%d.db" % (cap, label, n))
        n += 1
    src = sqlite3.connect(str(db), timeout=_timeout())
    dst = sqlite3.connect(str(tujuan))
    try:
        src.backup(dst)
    finally:
        dst.close()
        src.close()
    return str(tujuan)


def jalankan_tulis(args, db, perintah, kerja, backup_label=None):
    """Jalankan 'kerja(conn)' dalam transaksi. Tanpa --ya: ROLLBACK (pratinjau persis). Dengan --ya: COMMIT."""
    conn = buka(db)
    backup = None
    try:
        if args.ya and backup_label:
            backup = buat_backup(db, backup_label)
        try:
            conn.execute("BEGIN IMMEDIATE")
        except sqlite3.OperationalError as e:
            if _terkunci(e):
                raise Gagal(PESAN_TERKUNCI % _timeout())
            raise
        try:
            data, teks = kerja(conn)
            if args.ya:
                conn.execute("INSERT INTO log(waktu,perintah,ringkasan) VALUES (?,?,?)",
                             (datetime.now().isoformat(" ", "seconds"), perintah,
                              json.dumps(data.get("ringkasan", {}), ensure_ascii=False, default=str)))
                conn.execute("COMMIT")
            else:
                conn.execute("ROLLBACK")
        except BaseException:
            if conn.in_transaction:
                conn.execute("ROLLBACK")
            raise
    finally:
        conn.close()
    data.setdefault("ok", True)
    data["mode"] = "tersimpan" if args.ya else "pratinjau"
    data["perlu_konfirmasi"] = not args.ya
    data["db"] = str(db)
    if backup:
        data["backup"] = backup
    if args.ya:
        teks = "TERSIMPAN.\n" + teks + (("\nBackup: " + backup) if backup else "")
    else:
        teks = "PRATINJAU (belum disimpan):\n" + teks + "\n\nSimpan? Jalankan perintah yang sama + --ya setelah pengguna setuju."
    data.setdefault("peringatan", [])
    data["teks"] = teks
    return data, teks


def baca(args):
    db = path_db(args)
    return db, buka(db)


# --------------------------------------------------------------------------- CSV aman
def sel_aman(v):
    """Cegah formula injection saat file dibuka di Excel/Sheets (teks diawali = + - @ tab CR)."""
    if isinstance(v, (int, float, Decimal)):
        return v
    s = str(v if v is not None else "")
    if re.fullmatch(r"-?\d+(?:[.,]\d+)?", s):          # angka biasa (termasuk minus pecahan '-2,5') tetap angka
        return s
    if s and s[0] in "=+-@\t\r":                    # teks diawali '-' juga bisa dijalankan Excel sebagai rumus
        return "'" + s
    return s


def tulis_csv(path, header, rows, pemisah=";"):
    p = Path(path).expanduser()
    if p.parent and not p.parent.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
    with open(str(p), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=pemisah)
        w.writerow(header)
        for r in rows:
            w.writerow([sel_aman(x) for x in r])
    return str(p)


def baca_csv(path):
    p = Path(path).expanduser()
    if not p.is_file():
        raise Gagal("File %s tidak ditemukan." % path)
    if p.suffix.lower() in (".xlsx", ".xls", ".ods"):
        raise Gagal("File Excel belum didukung langsung. Di Excel: File > Save As > CSV (UTF-8) lalu kirim file CSV-nya.")
    raw = p.read_bytes()
    peringatan = []
    try:
        teks = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        teks = raw.decode("cp1252", errors="replace")
        peringatan.append("File bukan UTF-8; dibaca sebagai Windows-1252 (Excel lama). Cek ejaan nama produk.")
    teks = teks.lstrip("\ufeff")
    baris_awal = next((b for b in teks.splitlines() if b.strip()), "")
    if not baris_awal:
        raise Gagal("File %s kosong." % path)
    pemisah = max([";", ",", "\t", "|"], key=lambda c: baris_awal.count(c))
    if baris_awal.count(pemisah) == 0:
        pemisah = ","
    rows = [r for r in csv.reader(io.StringIO(teks), delimiter=pemisah)]
    return rows, pemisah, peringatan


SINONIM_PRODUK = {
    "kode": ["kode", "sku", "kode produk", "kode barang", "plu", "barcode", "kode item"],
    "nama": ["nama", "nama produk", "produk", "nama barang", "item", "nama item", "menu"],
    "varian": ["varian", "variasi", "ukuran", "variant"],
    "harga": ["harga jual", "harga", "harga satuan", "price", "harga (rp)"],
    "satuan": ["satuan", "unit", "uom"],
    "stok": ["stok", "stock", "jumlah stok", "stok awal", "qty stok"],
}


# --------------------------------------------------------------------------- produk
def cek_qty(q, satuan, konteks):
    if q <= 0:
        raise Gagal("%s: jumlah harus lebih dari 0." % konteks)
    if q != q.to_integral_value():
        if not satuan_boleh_pecahan(satuan):
            raise Gagal("%s: jumlah %s pecahan, padahal satuannya '%s'. Pecahan hanya untuk satuan timbang/ukur "
                        "(kg, gram, liter, meter, m2, m3, ton). Periksa lagi jumlahnya." % (konteks, fmt_qty(q), satuan))
        if q != q.quantize(Decimal("0.001")):
            raise Gagal("%s: jumlah maksimal 3 angka di belakang koma." % konteks)


def label_produk(p):
    return p["nama"] + ((" " + p["varian"]) if p["varian"] else "")


def validasi_produk(kode, nama, harga, satuan, stok):
    if not kode or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._/-]{0,39}", kode):
        raise Gagal("Kode produk '%s' tidak valid: pakai huruf/angka/tanda - _ . / tanpa spasi, maks 40 karakter."
                    % kode)
    if not nama.strip():
        raise Gagal("Nama produk wajib diisi (kode %s)." % kode)
    if harga <= 0:
        raise Gagal("Harga %s (%s) harus lebih dari Rp 0. Untuk barang gratis/bonus, catat harga normal lalu beri "
                    "diskon 100%%." % (kode, fmt_rp(harga)))
    if stok is not None and stok < 0:
        raise Gagal("Stok %s tidak boleh negatif." % kode)
    if stok is not None and stok != stok.to_integral_value() and not satuan_boleh_pecahan(satuan):
        raise Gagal("Stok %s pecahan, padahal satuannya '%s'." % (kode, satuan))


def cari_produk(conn, teks, semua_produk=None):
    """Cocokkan teks bebas ke produk. Kembalikan (produk, cara) atau raise Gagal dengan saran.

    Urutan: kode persis -> nama+varian persis -> nama persis (satu produk) -> semua kata ada di satu produk.
    Tidak pernah menebak dari kemiripan ejaan; kemiripan hanya jadi SARAN.
    """
    rows = semua_produk if semua_produk is not None else conn.execute("SELECT * FROM produk WHERE aktif=1").fetchall()
    q = norm(teks)
    if not q:
        raise Gagal("Nama produk kosong.")
    for p in rows:
        if norm(p["kode"]) == q:
            return p, "kode"
    persis = [p for p in rows if norm(label_produk(p)) == q]
    if len(persis) == 1:
        return persis[0], "nama"
    nama_persis = [p for p in rows if norm(p["nama"]) == q]
    if len(nama_persis) == 1:
        return nama_persis[0], "nama"
    if len(nama_persis) > 1:
        return None, {"teks": teks, "masalah": "ada beberapa varian",
                      "pilihan": ["%s (%s) %s" % (label_produk(p), p["kode"], fmt_rp(p["harga"])) for p in nama_persis]}
    kata = q.split()
    cocok = [p for p in rows if all(k in norm(label_produk(p) + " " + p["kode"]).split() for k in kata)]
    if len(cocok) == 1:
        return cocok[0], "sebagian"
    if len(cocok) > 1:
        return None, {"teks": teks, "masalah": "cocok dengan beberapa produk",
                      "pilihan": ["%s (%s) %s" % (label_produk(p), p["kode"], fmt_rp(p["harga"])) for p in cocok[:6]]}
    label = {norm(label_produk(p)): p for p in rows}
    mirip = difflib.get_close_matches(q, list(label), n=3, cutoff=0.6)
    if not mirip:
        mirip = [k for k in label if any(difflib.get_close_matches(w, k.split(), n=1, cutoff=0.8) for w in kata)][:3]
    return None, {"teks": teks, "masalah": "tidak dikenal",
                  "saran": ["%s (%s)" % (label_produk(label[m]), label[m]["kode"]) for m in mirip]}


def cmd_produk_tambah(args):
    db = path_db(args)
    harga = rupiah_bulat(args.harga, "Harga")
    stok = parse_angka(args.stok, "Stok") if args.stok not in (None, "") else None
    satuan = (args.satuan or "pcs").strip()
    validasi_produk(args.kode.strip(), args.nama, harga, satuan, stok)

    def kerja(conn):
        cfg = pengaturan(conn)
        if conn.execute("SELECT 1 FROM produk WHERE kode=?", (args.kode.strip(),)).fetchone():
            raise Gagal("Kode %s sudah dipakai. Pakai 'produk ubah' untuk mengubahnya." % args.kode)
        peringatan = []
        lama = [p for p in conn.execute("SELECT * FROM produk") if norm(label_produk(p)) == norm(
            args.nama + " " + (args.varian or ""))]
        if lama:
            peringatan.append("Nama sama dengan produk %s. Pastikan bukan produk dobel." % lama[0]["kode"])
        if stok is not None and cfg["stok"] != "kasir":
            peringatan.append("Stok dicatat, tetapi pengaturan stok toko = '%s' (stok hanya dipotong kasir bila "
                              "mode stok = kasir)." % cfg["stok"])
        w = datetime.now().isoformat(" ", "seconds")
        conn.execute("INSERT INTO produk(kode,nama,varian,harga,satuan,stok,dibuat,diubah) VALUES (?,?,?,?,?,?,?,?)",
                     (args.kode.strip(), args.nama.strip(), (args.varian or "").strip(), harga, satuan,
                      float(stok) if stok is not None else None, w, w))
        teks = "Produk baru: %s | %s %s | %s/%s%s" % (
            args.kode, args.nama, args.varian or "", fmt_rp(harga), satuan,
            (" | stok %s" % fmt_qty(stok)) if stok is not None else "")
        return {"produk": {"kode": args.kode, "nama": args.nama, "varian": args.varian or "", "harga": harga,
                           "satuan": satuan, "stok": angka_json(stok) if stok is not None else None},
                "peringatan": peringatan, "ringkasan": {"kode": args.kode}}, teks
    return jalankan_tulis(args, db, "produk tambah", kerja)


def cmd_produk_ubah(args):
    db = path_db(args)

    def kerja(conn):
        p = conn.execute("SELECT * FROM produk WHERE kode=?", (args.kode,)).fetchone()
        if not p:
            raise Gagal("Kode %s tidak ada. Cek dengan 'produk cari'." % args.kode)
        baru = dict(p)
        perubahan = []
        if args.nama:
            baru["nama"] = args.nama.strip()
        if args.varian is not None:
            baru["varian"] = args.varian.strip()
        if args.satuan:
            baru["satuan"] = args.satuan.strip()
        if args.harga:
            baru["harga"] = rupiah_bulat(args.harga, "Harga")
        if args.stok not in (None, ""):
            baru["stok"] = float(parse_angka(args.stok, "Stok"))
        if args.tanpa_stok:
            baru["stok"] = None
        if args.kode_baru:
            baru["kode"] = args.kode_baru.strip()
            if conn.execute("SELECT 1 FROM produk WHERE kode=? AND id<>?", (baru["kode"], p["id"])).fetchone():
                raise Gagal("Kode %s sudah dipakai produk lain." % baru["kode"])
        if args.nonaktif:
            baru["aktif"] = 0
        if args.aktif:
            baru["aktif"] = 1
        validasi_produk(baru["kode"], baru["nama"], baru["harga"], baru["satuan"],
                        Decimal(str(baru["stok"])) if baru["stok"] is not None else None)
        for k in ("kode", "nama", "varian", "harga", "satuan", "stok", "aktif"):
            if baru[k] != p[k]:
                a, b = p[k], baru[k]
                if k == "harga":
                    a, b = fmt_rp(a), fmt_rp(b)
                perubahan.append("%s: %s -> %s" % (k, a, b))
        if not perubahan:
            raise Gagal("Tidak ada yang diubah.")
        conn.execute("UPDATE produk SET kode=?,nama=?,varian=?,harga=?,satuan=?,stok=?,aktif=?,diubah=? WHERE id=?",
                     (baru["kode"], baru["nama"], baru["varian"], baru["harga"], baru["satuan"], baru["stok"],
                      baru["aktif"], datetime.now().isoformat(" ", "seconds"), p["id"]))
        if baru["stok"] != p["stok"] and baru["stok"] is not None:
            conn.execute("INSERT INTO stok_mutasi(waktu,produk_id,perubahan,stok_sesudah,sebab,catatan) "
                         "VALUES (?,?,?,?,?,?)", (datetime.now().isoformat(" ", "seconds"), p["id"],
                                                  baru["stok"] - (p["stok"] or 0), baru["stok"], "ubah-produk", ""))
        teks = "Ubah produk %s:\n- %s" % (args.kode, "\n- ".join(perubahan))
        pr = ["Harga baru hanya berlaku untuk nota berikutnya; nota lama tidak berubah."] if args.harga else []
        return {"perubahan": perubahan, "peringatan": pr, "ringkasan": {"kode": args.kode}}, teks
    return jalankan_tulis(args, db, "produk ubah", kerja)


def cmd_produk_cari(args):
    db, conn = baca(args)
    try:
        sql = "SELECT * FROM produk" + ("" if args.semua else " WHERE aktif=1") + " ORDER BY nama, varian"
        rows = conn.execute(sql).fetchall()
    finally:
        conn.close()
    q = norm(args.kata)
    if q:
        rows = [p for p in rows if all(k in norm(label_produk(p) + " " + p["kode"]) for k in q.split())]
    daftar = [{"kode": p["kode"], "nama": p["nama"], "varian": p["varian"], "harga": p["harga"], "satuan": p["satuan"],
               "stok": angka_json(p["stok"]) if p["stok"] is not None else None, "aktif": bool(p["aktif"])} for p in rows]
    t = ["Produk (%d):" % len(daftar)]
    for d in daftar:
        t.append("- %s | %s%s | %s/%s%s%s" % (d["kode"], d["nama"], (" " + d["varian"]) if d["varian"] else "",
                                             fmt_rp(d["harga"]), d["satuan"],
                                             (" | stok " + fmt_qty(d["stok"])) if d["stok"] is not None else "",
                                             "" if d["aktif"] else " | NONAKTIF"))
    if not daftar:
        t.append("(tidak ada)")
    return {"ok": True, "mode": "baca", "produk": daftar, "teks": "\n".join(t)}, "\n".join(t)


def cmd_produk_impor(args):
    db = path_db(args)
    rows, pemisah, peringatan = baca_csv(args.file)
    hi = None
    kol = {}
    for i, r in enumerate(rows[:10]):
        hn = [norm(x) for x in r]
        cand = {}
        for f, sin in SINONIM_PRODUK.items():
            for s in sin:
                if s in hn:
                    cand[f] = hn.index(s)
                    break
        if "nama" in cand and "harga" in cand:
            hi, kol = i, cand
            break
    if hi is None:
        raise Gagal("Kolom wajib tidak ketemu. File harus punya kolom Nama dan Harga (opsional Kode, Varian, Satuan, "
                    "Stok). Contoh: templates/produk-contoh.csv", kolom_ada=rows[0] if rows else [])
    header = rows[hi]
    pemetaan = {f: header[i] for f, i in kol.items()}

    def sel(r, f):
        i = kol.get(f)
        return (r[i].strip() if i is not None and i < len(r) else "")

    def kerja(conn):
        ada = {norm(p["kode"]) for p in conn.execute("SELECT kode FROM produk")}
        baru, dilewati, rusak, diperbarui = [], [], [], []
        kode_file = set()
        nomor_otomatis = conn.execute("SELECT COUNT(*) FROM produk").fetchone()[0]
        w = datetime.now().isoformat(" ", "seconds")
        for no, r in enumerate(rows[hi + 1:], start=hi + 2):
            if not any(c.strip() for c in r):
                continue
            nama, varian, kode = sel(r, "nama"), sel(r, "varian"), sel(r, "kode")
            satuan = sel(r, "satuan") or "pcs"
            try:
                harga = rupiah_bulat(sel(r, "harga"), "Harga")
                stok = parse_angka(sel(r, "stok"), "Stok") if sel(r, "stok") else None
                if not kode:
                    nomor_otomatis += 1
                    kode = "P%03d" % nomor_otomatis
                    while norm(kode) in ada or norm(kode) in kode_file:
                        nomor_otomatis += 1
                        kode = "P%03d" % nomor_otomatis
                    peringatan.append("Baris %d (%s): kode kosong, diberi kode otomatis %s." % (no, nama, kode))
                validasi_produk(kode, nama, harga, satuan, stok)
            except Gagal as e:
                rusak.append({"baris": no, "alasan": e.pesan})
                continue
            if norm(kode) in kode_file:
                rusak.append({"baris": no, "alasan": "Kode %s muncul dua kali di file." % kode})
                continue
            kode_file.add(norm(kode))
            if norm(kode) in ada:
                if args.perbarui:
                    conn.execute("UPDATE produk SET nama=?,varian=?,harga=?,satuan=?,diubah=? WHERE kode=?",
                                 (nama, varian, harga, satuan, w, kode))
                    diperbarui.append(kode)
                else:
                    dilewati.append(kode)
                continue
            conn.execute("INSERT INTO produk(kode,nama,varian,harga,satuan,stok,dibuat,diubah) VALUES (?,?,?,?,?,?,?,?)",
                         (kode, nama, varian, harga, satuan, float(stok) if stok is not None else None, w, w))
            baru.append({"kode": kode, "nama": nama, "varian": varian, "harga": harga, "satuan": satuan,
                         "stok": angka_json(stok) if stok is not None else None})
        t = ["Impor produk dari %s (pemisah '%s')" % (Path(args.file).name, "tab" if pemisah == "\t" else pemisah),
             "Pemetaan kolom: " + ", ".join("%s <- '%s'" % (k, v) for k, v in pemetaan.items()),
             "Produk baru: %d | sudah ada (dilewati): %d | diperbarui: %d | baris rusak: %d"
             % (len(baru), len(dilewati), len(diperbarui), len(rusak))]
        for b in baru[:15]:
            t.append("- %s | %s | %s/%s" % (b["kode"], label_produk(b), fmt_rp(b["harga"]), b["satuan"]))
        if len(baru) > 15:
            t.append("  ... dan %d produk lain" % (len(baru) - 15))
        for x in rusak:
            t.append("BARIS RUSAK %d: %s" % (x["baris"], x["alasan"]))
        if dilewati and not args.perbarui:
            t.append("Kode sudah ada (tidak diubah): %s. Pakai --perbarui untuk memperbarui nama/harga."
                     % ", ".join(dilewati[:10]))
        if not baru and not diperbarui:
            raise Gagal("Tidak ada produk yang bisa diimpor.%s%s" % (
                "".join("\n- baris %d: %s" % (x["baris"], x["alasan"]) for x in rusak[:20]),
                ("\n(kode sudah ada: %s; pakai --perbarui untuk memperbarui)" % ", ".join(dilewati[:10])) if dilewati else ""),
                baris_rusak=rusak, dilewati=dilewati, pemetaan=pemetaan)
        return {"pemetaan": pemetaan, "baru": baru, "dilewati": dilewati, "diperbarui": diperbarui,
                "baris_rusak": rusak, "peringatan": peringatan,
                "ringkasan": {"baru": len(baru), "diperbarui": len(diperbarui)}}, "\n".join(t)
    return jalankan_tulis(args, db, "produk impor", kerja, backup_label="impor-produk")


def cmd_stok(args):
    db = path_db(args)

    def kerja(conn):
        cfg = pengaturan(conn)
        p, info = cari_produk(conn, args.kode)
        if not p:
            raise Gagal("Produk '%s' tidak dikenal." % args.kode, detail=info)
        lama = Decimal(str(p["stok"])) if p["stok"] is not None else Decimal(0)
        if args.tambah is not None:
            d = parse_angka(args.tambah, "Stok")
            if d == 0:
                raise Gagal("Jumlah stok masuk tidak boleh 0.")
            baru = lama + d
        elif args.jadi is not None:
            baru = parse_angka(args.jadi, "Stok")
        else:
            raise Gagal("Isi --tambah N (barang datang) atau --jadi N (hasil hitung fisik).")
        if baru < 0:
            raise Gagal("Stok %s tidak boleh menjadi negatif (%s)." % (p["kode"], fmt_qty(baru)))
        validasi_produk(p["kode"], p["nama"], p["harga"], p["satuan"], baru)
        conn.execute("UPDATE produk SET stok=?, diubah=? WHERE id=?", (float(baru), datetime.now().isoformat(" ", "seconds"), p["id"]))
        conn.execute("INSERT INTO stok_mutasi(waktu,produk_id,perubahan,stok_sesudah,sebab,catatan) VALUES (?,?,?,?,?,?)",
                     (sekarang(args).isoformat(" "), p["id"], float(baru - lama), float(baru),
                      "tambah" if args.tambah is not None else "hitung-fisik", args.catatan or ""))
        pr = []
        if cfg["stok"] == "buku-stok":
            pr.append("Toko memakai buku-stok untuk stok. Catat barang datang di buku-stok saja agar tidak dobel.")
        elif cfg["stok"] == "tidak":
            pr.append("Mode stok toko = 'tidak': stok ini tidak dipotong otomatis saat jual. Ubah dengan atur --stok kasir.")
        teks = "Stok %s (%s): %s -> %s %s" % (p["kode"], label_produk(p), fmt_qty(lama), fmt_qty(baru), p["satuan"])
        return {"kode": p["kode"], "stok_lama": angka_json(lama), "stok_baru": angka_json(baru), "peringatan": pr,
                "ringkasan": {"kode": p["kode"], "stok": angka_json(baru)}}, teks
    return jalankan_tulis(args, db, "stok", kerja)


# --------------------------------------------------------------------------- init / atur / info
def _terapkan_atur(conn, args, cfg, wajib_nama=False):
    ubah = {}
    for k in ("nama_toko", "alamat", "telp", "footer", "npwp"):
        v = getattr(args, k, None)
        if v is not None:
            ubah[k] = v.strip()
    for k in ("pajak", "pkp", "stok", "kertas", "service_kena_pajak"):
        v = getattr(args, k, None)
        if v is not None:
            ubah[k] = str(v)
    if getattr(args, "zona", None):
        ubah["zona"] = normal_zona(args.zona)
    if getattr(args, "tarif_pbjt", None) not in (None, ""):
        t = parse_angka(args.tarif_pbjt.rstrip("% "), "Tarif PBJT")
        if t <= 0 or t > 10:
            raise Gagal("Tarif PBJT %s%% tidak sah: UU 1/2022 Pasal 58 ayat (1) membatasi paling tinggi 10%%. Isi "
                        "sesuai Perda daerah Anda (lihat SKPD/surat Bapenda)." % fmt_qty(t))
        ubah["tarif_pbjt"] = fmt_qty(t).replace(",", ".")
    if getattr(args, "service_charge", None) not in (None, ""):
        sc = parse_angka(args.service_charge.rstrip("% "), "Service charge")
        if sc < 0 or sc > 100:
            raise Gagal("Service charge harus 0-100%.")
        ubah["service_persen"] = fmt_qty(sc).replace(",", ".")
    baru = dict(cfg)
    baru.update(ubah)
    if wajib_nama and not baru["nama_toko"]:
        raise Gagal("Nama toko wajib diisi (--nama-toko), untuk kepala struk.")
    if baru["pajak"].startswith("ppn") and getattr(args, "tarif_pbjt", None) not in (None, ""):
        raise Gagal("PPN dan PBJT tidak digabung: makanan/minuman yang menjadi objek PBJT (pajak daerah) bukan objek "
                    "PPN (Pasal 4A ayat (2) huruf c UU PPN s.t.d.t.d. UU HPP). Pilih salah satu: --pajak pbjt-belum/"
                    "pbjt-termasuk untuk restoran/kafe/warung makan, atau PPN untuk toko PKP non-kuliner.")
    if baru["pajak"].startswith("pbjt") and not baru.get("tarif_pbjt"):
        raise Gagal("Mode PBJT butuh tarif dari Perda daerah Anda: tambahkan --tarif-pbjt N (paling tinggi 10). "
                    "Tarif tidak diisi otomatis karena berbeda per kabupaten/kota; lihat SKPD atau tanya Bapenda.")
    sc_on = baru.get("service_persen") not in ("", "0", None)
    if sc_on and baru["pajak"].endswith("-termasuk"):
        raise Gagal("Service charge tidak bisa dipakai dengan harga termasuk pajak. Pakai --pajak pbjt-belum/"
                    "ppn-belum, atau masukkan service charge ke harga menu.")
    if sc_on and baru["pajak"] != "tanpa" and baru.get("service_kena_pajak") not in ("ya", "tidak"):
        raise Gagal("Apakah service charge ikut dikenai pajak? Perlakuannya mengikuti Perda/aturan pajak yang berlaku "
                    "untuk usaha Anda; skill ini tidak menentukannya. Tanyakan ke Bapenda/konsultan, lalu isi "
                    "--sc-kena-pajak ya atau --sc-kena-pajak tidak.")
    if baru["pajak"].startswith("ppn") and baru["pkp"] != "ya":
        raise Gagal("PPN hanya boleh dipungut oleh Pengusaha Kena Pajak (PKP). Jika toko sudah PKP, tambahkan "
                    "--pkp ya. Jika belum PKP, pakai --pajak tanpa (jangan cantumkan PPN di struk). "
                    "PPh final 0,5% tidak dicantumkan di struk; kasir hanya menyiapkan omzet.")
    for k, v in ubah.items():
        conn.execute("INSERT OR REPLACE INTO meta(kunci,nilai) VALUES (?,?)", (k, v))
    return baru, ubah


def label_pajak(mode, tarif):
    lb = LABEL_PAJAK[mode]
    return lb % (tarif or "?").replace(".", ",") if "%s" in lb else lb


def ringkas_cfg(cfg):
    sc = cfg.get("service_persen") not in ("", "0", None)
    return ("Toko: %s | Pajak: %s%s | Stok: %s | Kertas struk: %s mm | Zona: %s (%s)"
            % (cfg["nama_toko"] or "-", label_pajak(cfg["pajak"], cfg.get("tarif_pbjt")),
               (" | Service charge %s%%%s" % (cfg["service_persen"].replace(".", ","),
                                             {"ya": " (kena pajak)", "tidak": " (tidak kena pajak)"}.get(
                                                 cfg.get("service_kena_pajak"), ""))) if sc else "",
               {"tidak": "tidak dilacak", "kasir": "dipotong kasir", "buku-stok": "dikelola skill buku-stok"}[cfg["stok"]],
               cfg["kertas"], cfg.get("zona", "Asia/Jakarta"), ZONA[cfg.get("zona", "Asia/Jakarta")][1]))


def cmd_init(args):
    db = path_db(args)
    if db.is_file():
        conn = buka(db)
        conn.close()
        d = {"ok": True, "mode": "baca", "db": str(db), "sudah_ada": True,
             "teks": "Database kasir sudah ada di %s. Tidak ada yang diubah. Pakai 'atur' untuk mengubah pengaturan." % db}
        return d, d["teks"]
    cfg = dict(PENGATURAN_DEFAULT)
    if not args.ya:
        # pratinjau tanpa membuat file
        mem = sqlite3.connect(":memory:")
        mem.executescript(SKEMA)
        baru, _ = _terapkan_atur(mem, args, cfg, wajib_nama=True)
        mem.close()
        t = "PRATINJAU (belum disimpan):\nBuat database kasir baru di %s\n%s\n\nSimpan? Jalankan ulang + --ya." % (
            db, ringkas_cfg(baru))
        return {"ok": True, "mode": "pratinjau", "perlu_konfirmasi": True, "db": str(db), "pengaturan": baru,
                "peringatan": [], "teks": t}, t
    db.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db), isolation_level=None, timeout=_timeout())
    try:
        conn.execute("BEGIN")
        for stmt in [s for s in SKEMA.split(";") if s.strip()]:
            conn.execute(stmt)
        conn.execute("INSERT OR REPLACE INTO meta VALUES ('aplikasi', ?)", (APLIKASI,))
        conn.execute("INSERT OR REPLACE INTO meta VALUES ('versi', ?)", (VERSI,))
        for k, v in PENGATURAN_DEFAULT.items():
            conn.execute("INSERT OR IGNORE INTO meta VALUES (?,?)", (k, v))
        conn.row_factory = sqlite3.Row
        baru, _ = _terapkan_atur(conn, args, cfg, wajib_nama=True)
        conn.execute("COMMIT")
    except BaseException:
        if conn.in_transaction:
            conn.execute("ROLLBACK")
        conn.close()
        try:
            db.unlink()
        except OSError:
            pass
        raise
    conn.close()
    t = "TERSIMPAN.\nDatabase kasir dibuat di %s\n%s" % (db, ringkas_cfg(baru))
    return {"ok": True, "mode": "tersimpan", "perlu_konfirmasi": False, "db": str(db), "pengaturan": baru,
            "peringatan": [], "teks": t}, t


def cmd_atur(args):
    db = path_db(args)

    def kerja(conn):
        cfg = pengaturan(conn)
        baru, ubah = _terapkan_atur(conn, args, cfg)
        if not ubah:
            raise Gagal("Tidak ada pengaturan yang diubah. Opsi: --nama-toko --alamat --telp --footer --npwp "
                        "--pajak --pkp --stok --kertas")
        pr = []
        if "pajak" in ubah and ubah["pajak"] != cfg["pajak"]:
            pr.append("Mode pajak baru hanya berlaku untuk nota berikutnya; nota lama tetap dengan mode lamanya.")
            if ubah["pajak"] == "ppn-belum":
                pr.append("Mode 'ppn-belum': harga produk di daftar dianggap BELUM termasuk PPN, jadi pembeli membayar "
                          "harga + PPN 11% efektif. Pastikan harga di menu/etalase sudah dikomunikasikan.")
        if "stok" in ubah and ubah["stok"] == "buku-stok":
            pr.append("Kasir tidak lagi memotong stok. Setiap hari ekspor penjualan (ekspor --format buku-stok) lalu "
                      "impor ke buku-stok agar stok tidak dobel terpotong.")
        t = "Ubah pengaturan: " + ", ".join("%s = %s" % (k, v) for k, v in ubah.items()) + "\n" + ringkas_cfg(baru)
        return {"pengaturan": baru, "diubah": ubah, "peringatan": pr, "ringkasan": ubah}, t
    return jalankan_tulis(args, db, "atur", kerja)


def cmd_info(args):
    db, conn = baca(args)
    try:
        cfg = pengaturan(conn)
        n_produk = conn.execute("SELECT COUNT(*) FROM produk WHERE aktif=1").fetchone()[0]
        n_nota = conn.execute("SELECT COUNT(*) FROM nota").fetchone()[0]
        akhir = conn.execute("SELECT no, waktu FROM nota ORDER BY id DESC LIMIT 1").fetchone()
        sesi = conn.execute("SELECT * FROM sesi WHERE tutup IS NULL ORDER BY id DESC LIMIT 1").fetchone()
    finally:
        conn.close()
    fol = db.parent / "backup-kasir"
    bks = sorted(fol.glob("*.db")) if fol.is_dir() else []
    peringatan = []
    zona = cfg.get("zona") or "Asia/Jakarta"
    kom = offset_komputer()
    toko = timedelta(hours=ZONA[zona][0])
    if kom != toko:
        jam = kom.total_seconds() / 3600
        peringatan.append("Jam komputer memakai zona UTC%+g, sedangkan toko %s (UTC+%d). Waktu nota tetap dicatat dalam "
                          "%s; jadwal OpenClaw sebaiknya memakai --tz %s." % (jam, ZONA[zona][1], ZONA[zona][0],
                                                                             ZONA[zona][1], zona))
    t = ["Database: %s" % db, ringkas_cfg(cfg), "Produk aktif: %d | Nota: %d%s" % (
        n_produk, n_nota, (" | nota terakhir %s (%s)" % (akhir["no"], akhir["waktu"])) if akhir else ""),
        ("Kasir DIBUKA sejak %s, kas awal %s" % (sesi["buka"], fmt_rp(sesi["kas_awal"]))) if sesi else "Kasir: belum dibuka",
        "Backup terakhir: %s" % (bks[-1].name if bks else "-")] + ["Catatan: " + x for x in peringatan]
    return {"ok": True, "mode": "baca", "db": str(db), "pengaturan": cfg, "produk_aktif": n_produk, "nota": n_nota,
            "sesi_terbuka": dict(sesi) if sesi else None, "peringatan": peringatan,
            "teks": "\n".join(t)}, "\n".join(t)


# --------------------------------------------------------------------------- parse pesanan chat
# Permintaan struk di kalimat ("..., terus bikinin struknya ya") bukan barang. Struk teks memang otomatis ikut setelah
# nota tersimpan, jadi permintaannya dibuang sebelum pesanan dibaca. ATURAN KERAS: kata "struk" TIDAK PERNAH dibuang dari
# dalam nama barang ("kertas struk", "printer struk", "kertas cetak struk"): produk tidak boleh berganti diam-diam.
# Yang dibuang hanya (a) kalimat penutup yang seluruhnya permintaan struk, (b) segmen yang seluruhnya permintaan struk,
# (c) ekor permintaan di akhir segmen bayar/diskon (tidak mungkin berisi nama barang), dan (d) ekor dengan kata kerja
# berimbuhan -in/-kan ("bikinin struknya") di segmen barang. "cetak struk" tanpa imbuhan di ekor segmen barang TIDAK
# dibuang: ditolak jelas oleh pencocokan produk, bukan ditebak.
_RM_AWAL = r"(?:(?:terus|trus|lalu|habis itu|abis itu|setelah itu|dan|sama|plus|sekalian)[,\s]+)*"
_RM_MINTA = r"(?:(?:tolong|mau|minta|bisa|boleh|coba)[,\s]+)*"
_RM_KERJA_BEBAS = r"(?:(?:bikin|buat|cetak|kirim|kasih|print|tampilkan|munculkan)(?:in|kan)?\s+)?"
_RM_KERJA_IMBUHAN = r"(?:bikin|buat|cetak|kirim|kasih|print)(?:in|kan)\s+"
_RM_STRUK = r"(?:sekalian\s+)?\bstruk(?:nya)?\b(?!\s*\d)"
_RM_AKHIR = (r"(?:\s+(?:ke|di)\s+(?:sini|chat|telegram|wa|whatsapp))?(?:\s+(?:bikin|buat|cetak|kirim|kasih|print)(?:in|kan)?)?"
             r"(?:\s+(?:ya|yah|dong|juga|aja|saja|deh|kak|mas|mbak|bu|pak|dulu|sekalian|please|plis|tolong))*[\s.!?]*$")
POLA_SEGMEN_STRUK = re.compile(r"^\s*" + _RM_AWAL + _RM_MINTA + _RM_KERJA_BEBAS + _RM_STRUK + _RM_AKHIR, re.I)
POLA_EKOR_STRUK_BEBAS = re.compile(r"(?<!\w)" + _RM_AWAL + _RM_MINTA + _RM_KERJA_BEBAS + _RM_STRUK + _RM_AKHIR, re.I)
POLA_EKOR_STRUK_IMBUHAN = re.compile(r"(?<!\w)" + _RM_AWAL + _RM_MINTA + _RM_KERJA_IMBUHAN + _RM_STRUK + _RM_AKHIR, re.I)
POLA_BAYAR_ATAU_DISKON = re.compile(r"^\s*(?:bayar|dibayar|pembayaran|uang pas|diskon|disc|disk|potongan|pot)\b", re.I)
POLA_BATAS_KALIMAT = re.compile(r"[.!?]+\s+|\n+")
# Awalan yang bukan barang: "Tolong catat penjualan: 2 kopi susu, ..." -> yang dibaca hanya "2 kopi susu, ...".
POLA_AWALAN = re.compile(
    r"^\s*(?:(?:tolong|coba|mohon|minta)[,\s]+)*"
    r"(?:(?:catat|input|rekam|masuk)(?:kan|in)?\b\s*(?:(?:penjualan|transaksi|pesanan|order|jualan|nota)"
    r"(?:\s+(?:baru|ini|tadi|berikut|hari\s+ini))*)?\s*[:\-]?\s*"
    r"|(?:penjualan|transaksi|pesanan|order|jualan)(?:\s+(?:baru|ini|tadi|berikut|hari\s+ini))*(?:\s*:\s*|\s+(?=\d)))",
    re.I)
POLA_POTONG = re.compile(r"\s*(?:;|\n|,(?!\d)|\bdan\b|\bsama\b|\btambah\b(?!\s*\d))\s*")


def metode_dari(teks):
    t = norm(teks)
    for label, kata in METODE:
        for k in sorted(kata, key=len, reverse=True):
            if re.search(r"(?<![\w])" + re.escape(norm(k)) + r"(?![\w])", t):
                return label, k
    return None, None


def parse_bayar_segmen(seg):
    """'tunai 100rb' / 'qris' / 'pas' / 'qris 50rb tunai 50rb' -> list[(metode, jumlah|None)]."""
    t = seg.strip().lower()
    t = re.sub(r"^(bayar(nya)?|dibayar|pembayaran|pakai|via|lewat)\b\s*", "", t)
    if re.fullmatch(r"(uang\s+)?pas|tunai\s+pas|cash\s+pas|pas\s+tunai", t):
        return [("Tunai", "PAS")]
    hasil = []
    pola = re.compile(r"([a-z][a-z\s-]*?)\s*[:=]?\s*((?:rp\.?\s*)?\d[\d.,]*\s*(?:rb|ribu|k|jt|juta)?)?(?=\s+[a-z]|$)")
    sisa = t
    while sisa.strip():
        m = pola.match(sisa.strip())
        if not m or not m.group(1).strip():
            raise Gagal("Pembayaran '%s' tidak dimengerti. Contoh: 'bayar tunai 100rb', 'bayar qris', "
                        "'bayar qris 50rb, tunai 50rb'." % seg)
        label, _ = metode_dari(m.group(1))
        if not label:
            raise Gagal("Metode bayar '%s' tidak dikenal. Pilihan: tunai, QRIS, transfer, debit, kartu kredit, "
                        "e-wallet." % m.group(1).strip())
        jumlah = m.group(2)
        if jumlah and re.search(r"\bpas\b", m.group(1)):
            jumlah = None
        hasil.append((label, jumlah.strip() if jumlah else ("PAS" if re.search(r"\bpas\b", m.group(1)) else None)))
        sisa = sisa.strip()[m.end():]
    return hasil


def satuan_kanonik(u):
    u = norm(u).replace("²", "2").replace("³", "3")
    return ALIAS_SATUAN.get(u, u)


def satuan_boleh_pecahan(u):
    return norm(u) in SATUAN_PECAHAN or satuan_kanonik(u) in SATUAN_PECAHAN


SATUAN_BAWAAN = SATUAN_UMUM | SATUAN_PECAHAN | set(ALIAS_SATUAN)
POLA_QTY = r"(\d+(?:[.,]\d+)?)"


def parse_item_segmen(seg, satuan_dikenal=None):
    """'2 sak semen diskon 10%' -> dict(teks, utuh, nama, qty, satuan, diskon, qty_eksplisit).
    Satuan (kata setelah angka, atau di akhir: 'semen 2 sak') dipisahkan dan nanti dicek terhadap satuan produk."""
    unit = set(SATUAN_BAWAAN) | set(satuan_dikenal or ())
    s = " ".join(seg.strip().split())
    diskon = ""
    m = re.search(r"\s*\(?\s*\b(?:diskon|disc|disk|potongan|pot)\b\.?\s*([\d.,%+\srbkjtribu]+)\)?\s*$", s, re.I)
    if m:
        diskon = m.group(1).strip()
        s = s[:m.start()].strip()
    m = re.search(r"\s*@\s*[\d.,]+\s*(rb|k)?\s*$", s, re.I)
    if m:
        raise Gagal("'%s': harga di pesanan (@...) tidak dipakai. Kasir memakai harga dari daftar produk; ubah "
                    "harga lewat 'produk ubah' atau beri diskon." % seg)
    qty, satuan = None, None
    low = s.lower()
    m_kode = re.match(r"^([a-z0-9][a-z0-9._/-]*)\s*=\s*" + POLA_QTY + "$", low)
    m_lekat = re.match(r"^" + POLA_QTY + r"([a-z][a-z0-9²³]*)\s+(.+)$", low)      # '2kg gula', '0,5m3 pasir'
    m = re.match(r"^" + POLA_QTY + r"\s*(?:x\s+|x(?=[a-z])|\s)(.+)$", low)
    if m_kode:
        nama, qty = m_kode.group(1), m_kode.group(2)
    elif m_lekat and norm(m_lekat.group(2)) in unit:
        qty, satuan, nama = m_lekat.group(1), m_lekat.group(2), m_lekat.group(3)
    elif m:
        qty, nama = m.group(1), m.group(2)
        kata = nama.split()
        if len(kata) > 1 and norm(kata[0]) in unit:
            satuan, nama = kata[0], " ".join(kata[1:])
    else:
        m = re.match(r"^(" + "|".join(ANGKA_KATA) + r")\s+(.+)$", low)
        if m and m.group(1) != "se":
            qty, nama = ANGKA_KATA[m.group(1)], m.group(2)
            kata = nama.split()
            if len(kata) > 1 and norm(kata[0]) in unit:
                satuan, nama = kata[0], " ".join(kata[1:])
        else:
            m = re.match(r"^(.+?)\s*(?:x\s*|\s)" + POLA_QTY + r"\s*([a-z][a-z0-9²³]*)?$", low)
            if m and (m.group(3) is None or norm(m.group(3)) in unit):
                nama, qty, satuan = m.group(1), m.group(2), m.group(3)
            else:
                nama, qty = low, None
    nama = nama.strip()
    qty_d = parse_angka(qty, "Jumlah") if qty is not None and not isinstance(qty, Decimal) else (
        Decimal(qty) if qty is not None else Decimal(1))
    return {"teks": seg.strip(), "utuh": low, "nama": nama, "qty": qty_d, "satuan": satuan, "diskon": diskon,
            "qty_eksplisit": qty is not None}


def buang_satuan(nama, unit):
    """Buang kata satuan di awal/akhir nama. Kembalikan (nama_bersih, satuan_dibuang|None)."""
    kata = nama.split()
    dibuang = None
    if len(kata) > 1 and norm(kata[0]) in unit:
        dibuang, kata = kata[0], kata[1:]
    elif len(kata) > 1 and norm(kata[-1]) in unit:
        dibuang, kata = kata[-1], kata[:-1]
    return " ".join(kata), dibuang


def cocokkan_item(conn, it, rows, unit):
    """Cocokkan satu item pesanan ke produk (atau baris nota). Kembalikan (produk, info_cocok, qty) atau
    (None, info_masalah, None). Tidak pernah menebak; satuan yang berbeda dengan satuan produk ditolak."""
    p, cara = cari_produk(conn, it["utuh"], rows)                  # nama produk berisi angka, mis. 'Air 600 ml'
    if p is not None and cara in ("kode", "nama") and it["utuh"] != it["nama"]:
        return p, cara, Decimal(1)
    satuan = it["satuan"]
    p, info = cari_produk(conn, it["nama"], rows)
    if p is None and satuan and info.get("pilihan"):
        # beberapa produk cocok -> satuan yang disebut boleh mempersempit ('0,5 m3 pasir' = Pasir Beton, bukan Gula Pasir)
        sama = [r for r in rows if satuan_kanonik(r["satuan"]) == satuan_kanonik(satuan)]
        p2, info2 = cari_produk(conn, it["nama"], sama) if sama else (None, None)
        if p2 is not None:
            p, info = p2, "sebagian"
    if p is None and satuan:
        p2, info2 = cari_produk(conn, satuan + " " + it["nama"], rows)   # produk yang namanya diawali kata satuan
        if p2 is not None:
            p, info, satuan = p2, info2, None
    if p is None:
        bersih, dibuang = buang_satuan(it["nama"], unit)
        if dibuang:
            p2, info2 = cari_produk(conn, bersih, rows)
            if p2 is not None:
                p, info, satuan = p2, info2, satuan or dibuang
            else:
                info = info2
    if p is None:
        info = dict(info)
        info["teks"] = it["teks"]
        return None, info, None
    if satuan:
        a, b = satuan_kanonik(satuan), satuan_kanonik(p["satuan"])
        if a != b and not (a in SATUAN_GENERIK and not satuan_boleh_pecahan(p["satuan"])):
            contoh = {"lusin": " (1 lusin = 12)", "kodi": " (1 kodi = 20)"}.get(a, "")
            return None, {"teks": it["teks"], "masalah": "satuan '%s' berbeda dengan satuan produk %s ('%s'). Sebutkan "
                          "jumlah dalam %s%s, atau daftarkan produk dengan satuan itu"
                          % (satuan, label_produk(p), p["satuan"], p["satuan"], contoh)}, None
    return p, info, it["qty"]


def pecah_pesan(pesan):
    """Pecah kalimat penjualan jadi segmen (barang / diskon / bayar / catatan) tanpa awalan "catat penjualan:" dan
    tanpa permintaan struk. Kata "struk" di dalam nama barang tidak pernah dibuang (lihat POLA_SEGMEN_STRUK)."""
    p = POLA_AWALAN.sub("", pesan, count=1).strip()
    batas = list(POLA_BATAS_KALIMAT.finditer(p))
    if batas and POLA_SEGMEN_STRUK.match(p[batas[-1].end():]):        # ". Bikinin struknya ya" di ujung pesan
        p = p[:batas[-1].start()]
    p = p.rstrip(" \t\n.!?")
    hasil = []
    for seg in POLA_POTONG.split(p):
        if not seg or not seg.strip():
            continue
        seg = seg.strip()
        if POLA_SEGMEN_STRUK.match(seg):
            continue
        pola_ekor = POLA_EKOR_STRUK_BEBAS if POLA_BAYAR_ATAU_DISKON.match(seg) else POLA_EKOR_STRUK_IMBUHAN
        if not re.match(r"^(catatan|atas nama|an\.?|a/n|meja)\b", seg.lower()):
            seg = pola_ekor.sub("", seg).rstrip(" \t,;.!?")
        if seg:
            hasil.append(seg)
    return hasil


def parse_pesan(pesan):
    items, diskon_nota, bayar, catatan = [], "", [], []
    if KATA_BON.search(pesan.lower()):
        raise Gagal("Transaksi bon/utang/tempo tidak dicatat di kasir (kasir mencatat yang sudah dibayar). Catat "
                    "sebagai piutang dengan skill tagih-piutang atau buat-invoice, lalu catat di kasir saat dibayar.")
    segmen = pecah_pesan(pesan)
    mode_bayar = False
    for seg in segmen:
        low = seg.strip().lower()
        if re.match(r"^(catatan|atas nama|an\.?|a/n|meja)\b", low):
            catatan.append(re.sub(r"^catatan\s*:?\s*", "", seg.strip(), flags=re.I))
            continue
        if re.match(r"^(diskon|disc|disk|potongan|pot)\b", low) and not mode_bayar:
            diskon_nota = (diskon_nota + "+" if diskon_nota else "") + re.sub(
                r"^(diskon|disc|disk|potongan|pot)\.?\s*(nota|semua|total)?\s*", "", low).strip()
            continue
        if re.match(r"^(bayar|dibayar|pembayaran|uang pas)\b", low):
            mode_bayar = True
            bayar.extend(parse_bayar_segmen(low))
            continue
        if mode_bayar:
            label, _ = metode_dari(low)
            if label:
                bayar.extend(parse_bayar_segmen(low))
                continue
        items.append(parse_item_segmen(seg))
    return items, diskon_nota, bayar, catatan


# --------------------------------------------------------------------------- nota: hitung
def nomor_nota(conn, jenis, waktu):
    pref = "N" if jenis == "jual" else "R"
    kunci = "%s-%s-" % (pref, waktu.strftime("%y%m%d"))
    r = conn.execute("SELECT no FROM nota WHERE no LIKE ? ORDER BY no DESC LIMIT 1", (kunci + "%",)).fetchone()
    n = int(r["no"].rsplit("-", 1)[1]) + 1 if r else 1
    return "%s%04d" % (kunci, n)


def susun_bayar(bayar_spek, total):
    peringatan = []
    if not bayar_spek:
        bayar_spek = [("Tunai", "PAS")]
        peringatan.append("Cara bayar tidak disebut: dianggap TUNAI uang pas. Koreksi bila salah.")
    kosong = [b for b in bayar_spek if b[1] is None]
    if len(kosong) > 1:
        raise Gagal("Lebih dari satu metode bayar tanpa jumlah. Sebutkan jumlah per metode, mis. 'qris 50rb, tunai 50rb'.")
    tetap = {}
    for m, j in bayar_spek:
        if j is None:
            continue
        v = total if j == "PAS" else rupiah_bulat(j, "Bayar " + m)
        if v <= 0:
            raise Gagal("Jumlah bayar %s harus lebih dari 0." % m)
        tetap[m] = tetap.get(m, 0) + v
    if kosong:
        m = kosong[0][0]
        sisa = total - sum(tetap.values())
        if sisa <= 0:
            raise Gagal("Pembayaran %s tidak diperlukan: metode lain sudah menutup total." % m)
        tetap[m] = tetap.get(m, 0) + sisa
    non_tunai = sum(v for m, v in tetap.items() if m != "Tunai")
    jumlah = sum(tetap.values())
    if jumlah < total:
        raise Gagal("Pembayaran KURANG %s (total %s, dibayar %s). Minta kekurangannya atau ubah metode bayar. "
                    "Transaksi bon tidak dicatat di kasir." % (fmt_rp(total - jumlah), fmt_rp(total), fmt_rp(jumlah)),
                    kurang=total - jumlah)
    if non_tunai > total:
        raise Gagal("Pembayaran non-tunai (%s) melebihi total (%s). Kembalian hanya bisa dari uang tunai; cek lagi "
                    "nominal QRIS/transfer." % (fmt_rp(non_tunai), fmt_rp(total)))
    kembalian = jumlah - total
    return tetap, jumlah, kembalian, peringatan


def param_pajak_cfg(cfg):
    """Parameter pajak toko saat ini -> disimpan di nota agar nota lama tidak berubah bila pengaturan diubah."""
    mode = cfg["pajak"]
    sc = cfg.get("service_persen") if cfg.get("service_persen") not in ("", "0", None) else None
    return {"mode": mode, "tarif": cfg.get("tarif_pbjt") if mode.startswith("pbjt") else (
                "11/12x12" if mode.startswith("ppn") else None),
            "sc_persen": sc, "sc_kena": (cfg.get("service_kena_pajak") == "ya") if sc else None}


def param_pajak_nota(n):
    return {"mode": n["pajak_mode"], "tarif": n["tarif_pajak"], "sc_persen": n["service_persen"],
            "sc_kena": bool(n["service_kena"]) if n["service_kena"] is not None else None}


def total_dari_param(netto, pp):
    tarif = pp["tarif"] if pp["mode"].startswith("pbjt") else None
    return hitung_total(netto, pp["mode"], tarif, pp["sc_persen"], pp["sc_kena"])


def hitung_nota(item_siap, diskon_nota_spek, pp):
    """item_siap: list dict(produk, qty, diskon_spek). Kembalikan baris & total (int rupiah)."""
    baris = []
    for it in item_siap:
        p = it["produk"]
        bruto = rhu(it["qty"] * p["harga"])
        d_item, langkah = terapkan_diskon(bruto, it["diskon_spek"], "Diskon %s" % label_produk(p))
        baris.append({"produk_id": p["id"], "kode": p["kode"], "nama": p["nama"], "varian": p["varian"],
                      "satuan": p["satuan"], "qty": it["qty"], "harga": p["harga"], "bruto": bruto,
                      "diskon_item": d_item, "diskon_item_label": label_diskon(langkah), "setelah_item": bruto - d_item})
    subtotal = sum(b["setelah_item"] for b in baris)
    d_nota, langkah_nota = terapkan_diskon(subtotal, diskon_nota_spek, "Diskon nota")
    alok = alokasi(d_nota, [b["setelah_item"] for b in baris])
    for b, a in zip(baris, alok):
        b["diskon_nota"] = a
        b["netto"] = b["setelah_item"] - a
    netto = subtotal - d_nota
    pj = total_dari_param(netto, pp)
    return {"baris": baris, "bruto": sum(b["bruto"] for b in baris), "diskon_item": sum(b["diskon_item"] for b in baris),
            "subtotal": subtotal, "diskon_nota": d_nota, "diskon_nota_label": label_diskon(langkah_nota),
            "netto": netto, "service": pj["service"], "dpp": pj["dpp"], "ppn": pj["ppn"], "sisa": pj["sisa"],
            "total": pj["total"], "pp": pp}


def sidik_nota(h, bayar):
    isi = json.dumps([[b["produk_id"], str(b["qty"]), b["diskon_item"]] for b in h["baris"]] +
                     [h["diskon_nota"], sorted(bayar.items())], sort_keys=True)
    return hashlib.sha1(isi.encode()).hexdigest()


def teks_rincian(h, cfg_pajak):
    t = []
    for i, b in enumerate(h["baris"], 1):
        t.append("%d. %s (%s) %s x %s = %s" % (i, label_produk(b), b["kode"], fmt_qty(b["qty"]),
                                                  fmt_rp(b["harga"]), fmt_rp(b["bruto"])))
        if b["diskon_item"]:
            t.append("   diskon %s: -%s" % (b["diskon_item_label"], fmt_rp(b["diskon_item"])))
    t.append("Subtotal: %s" % fmt_rp(h["subtotal"]))
    if h["diskon_nota"]:
        t.append("Diskon nota %s: -%s" % (h["diskon_nota_label"], fmt_rp(h["diskon_nota"])))
    t += teks_pajak(h, h["pp"])
    return t


def label_tarif(pp):
    return (pp["tarif"] or "?").replace(".", ",")


def teks_pajak(h, pp):
    mode = pp["mode"]
    t = []
    if h.get("service"):
        t.append("Service charge %s%%: %s%s" % (pp["sc_persen"].replace(".", ","), fmt_rp(h["service"]),
                                              "" if mode == "tanpa" else (" (ikut dasar pajak)" if pp["sc_kena"]
                                                                          else " (tidak dikenai pajak)")))
    if mode == "pbjt-belum":
        return t + ["Dasar PBJT: %s | PBJT %s%%: %s" % (fmt_rp(h["dpp"]), label_tarif(pp), fmt_rp(h["ppn"])),
                    "TOTAL: %s" % fmt_rp(h["total"])]
    if mode == "pbjt-termasuk":
        return t + ["TOTAL: %s (sudah termasuk PBJT %s%%)" % (fmt_rp(h["total"]), label_tarif(pp)),
                    "  Dasar PBJT %s | PBJT %s%s" % (fmt_rp(h["dpp"]), fmt_rp(h["ppn"]),
                                                    (" | selisih pembulatan %s" % fmt_rp(h["sisa"])) if h["sisa"] else "")]
    if mode == "ppn-belum":
        return t + ["DPP: %s | DPP nilai lain 11/12: Rp %s | PPN 12%%: %s" % (
                    fmt_rp(h["dpp"]), fmt_desimal(dpp_nilai_lain(h["dpp"])), fmt_rp(h["ppn"])),
                "TOTAL: %s" % fmt_rp(h["total"])]
    if mode == "ppn-termasuk":
        return t + ["TOTAL: %s (sudah termasuk PPN)" % fmt_rp(h["total"]),
                "  DPP %s | DPP nilai lain 11/12 Rp %s | PPN 12%% %s%s" % (
                    fmt_rp(h["dpp"]), fmt_desimal(dpp_nilai_lain(h["dpp"])), fmt_rp(h["ppn"]),
                    (" | selisih pembulatan %s" % fmt_rp(h["sisa"])) if h["sisa"] else "")]
    return t + ["TOTAL: %s" % fmt_rp(h["total"])]


def fmt_desimal(d):
    d = Decimal(d).quantize(Decimal("0.01"), ROUND_HALF_UP)
    utuh, _, pec = "{:f}".format(abs(d)).partition(".")
    return ("-" if d < 0 else "") + fmt_angka(int(utuh)) + ("," + pec if pec and pec != "00" else "")


def potong_stok(conn, cfg, baris, arah, nota_id, waktu, izinkan_minus, peringatan):
    """arah -1 = jual, +1 = retur/void. Hanya bila mode stok = kasir dan produk punya stok."""
    if cfg["stok"] != "kasir":
        return
    for b in baris:
        p = conn.execute("SELECT * FROM produk WHERE id=?", (b["produk_id"],)).fetchone()
        if not p or p["stok"] is None:
            continue
        q = Decimal(str(abs(b["qty"])))
        lama = Decimal(str(p["stok"]))
        baru = lama + q * arah
        if baru < 0 and arah < 0:
            if not izinkan_minus:
                raise Gagal("Stok %s (%s) tidak cukup: tersisa %s, diminta %s. Cek fisik barangnya; bila memang ada, "
                            "perbarui stok dulu (stok --kode %s --jadi N) atau ulangi dengan --izinkan-minus."
                            % (p["kode"], label_produk(p), fmt_qty(lama), fmt_qty(q), p["kode"]))
            peringatan.append("Stok %s menjadi minus (%s). Hitung ulang fisiknya." % (p["kode"], fmt_qty(baru)))
        conn.execute("UPDATE produk SET stok=? WHERE id=?", (float(baru), p["id"]))
        conn.execute("INSERT INTO stok_mutasi(waktu,produk_id,perubahan,stok_sesudah,sebab,nota_id) VALUES (?,?,?,?,?,?)",
                     (waktu, p["id"], float(q * arah), float(baru), "jual" if arah < 0 else "retur", nota_id))


def simpan_nota(conn, jenis, no, waktu, ref_id, mode, h, bayar, jumlah_bayar, kembalian, args, alasan, sidik, sesi_id,
                baris_ref=None):
    nid = conn.execute(
        "INSERT INTO nota(no,jenis,waktu,ref_nota_id,pajak_mode,bruto,diskon_item,diskon_nota,diskon_nota_label,netto,"
        "dpp,ppn,sisa,total,bayar,kembalian,kasir,catatan,alasan,sidik,sesi_id,dibuat,tarif_pajak,service,"
        "service_persen,service_kena,zona) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (no, jenis, waktu, ref_id, mode, h["bruto"], h["diskon_item"], h["diskon_nota"], h.get("diskon_nota_label", ""),
         h["netto"], h["dpp"], h["ppn"], h["sisa"], h["total"], jumlah_bayar, kembalian, getattr(args, "kasir", "") or "",
         getattr(args, "catatan_nota", "") or "", alasan or "", sidik, sesi_id,
         datetime.now().isoformat(" ", "seconds"), h["pp"]["tarif"], h.get("service", 0), h["pp"]["sc_persen"],
         None if h["pp"]["sc_kena"] is None else int(h["pp"]["sc_kena"]),
         offset_zona(_ZONA_AKTIF["nama"]))).lastrowid
    for i, b in enumerate(h["baris"], 1):
        conn.execute("INSERT INTO nota_item(nota_id,urut,produk_id,kode,nama,varian,satuan,qty,harga,bruto,diskon_item,"
                     "diskon_item_label,diskon_nota,netto,ref_item_id) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                     (nid, i, b["produk_id"], b["kode"], b["nama"], b["varian"], b["satuan"], float(b["qty"]), b["harga"],
                      b["bruto"], b["diskon_item"], b.get("diskon_item_label", ""), b["diskon_nota"], b["netto"],
                      b.get("ref_item_id")))
    for m, v in bayar.items():
        conn.execute("INSERT INTO bayar(nota_id,metode,jumlah) VALUES (?,?,?)", (nid, m, v))
    return nid


def pesan_tanpa_sesi(conn, waktu):
    akhir = conn.execute("SELECT * FROM sesi WHERE tutup IS NOT NULL ORDER BY tutup DESC LIMIT 1").fetchone()
    if akhir and waktu.isoformat(" ") >= akhir["tutup"]:
        return ("Kasir sudah DITUTUP pukul %s, jadi nota ini belum ikut hitungan uang laci tadi; kalau toko masih "
                "buka, bilang \"buka kasir, modal ...\" lagi." % akhir["tutup"][:16])
    return ("Kasir belum \"dibuka\", jadi nota ini belum ikut hitungan uang laci; bilang \"buka kasir, modal 200 ribu\" "
            "bila mau dicocokkan.")


def sesi_aktif(conn):
    return conn.execute("SELECT * FROM sesi WHERE tutup IS NULL ORDER BY id DESC LIMIT 1").fetchone()


def cmd_jual(args):
    db = path_db(args)
    items, diskon_nota, bayar_spek, catatan = [], args.diskon or "", [], []
    if args.pesan:
        items, dn, bayar_spek, catatan = parse_pesan(args.pesan)
        if dn:
            diskon_nota = (diskon_nota + "+" if diskon_nota else "") + dn
    for it in args.item or []:
        if KATA_BON.search(it.lower()):
            raise Gagal("Transaksi bon/utang tidak dicatat di kasir; pakai skill tagih-piutang.")
        items.append(parse_item_segmen(it))
    for b in args.bayar or []:
        bayar_spek.extend(parse_bayar_segmen(b.replace("=", " ")))
    if not items:
        raise Gagal("Tidak ada barang di pesanan. Contoh: --pesan \"2 kopi susu, 1 roti bakar, bayar tunai 50rb\"")
    diskon_spek = parse_diskon(diskon_nota, "Diskon nota")
    args.catatan_nota = "; ".join(filter(None, [args.catatan or ""] + catatan))

    def kerja(conn):
        cfg = pengaturan(conn)
        waktu = parse_waktu(args.waktu) if args.waktu else sekarang(args)
        semua = conn.execute("SELECT * FROM produk WHERE aktif=1").fetchall()
        unit = SATUAN_BAWAAN | {norm(x["satuan"]) for x in semua}
        masalah, siap, info_cocok = [], [], []
        for it in items:
            p, info, qty = cocokkan_item(conn, it, semua, unit)
            if p is None:
                masalah.append(info)
                continue
            try:
                cek_qty(qty, p["satuan"], label_produk(p))
                siap.append({"produk": p, "qty": qty, "diskon_spek": parse_diskon(it["diskon"], "Diskon item")})
            except Gagal as e:
                masalah.append({"teks": it["teks"], "masalah": e.pesan})
            if info == "sebagian":
                info_cocok.append("'%s' dibaca sebagai %s (%s)" % (it["nama"], label_produk(p), p["kode"]))
        if masalah:
            t = ["Pesanan belum bisa dicatat:"]
            for m in masalah:
                baris = "- '%s': %s" % (m["teks"], m["masalah"])
                if m.get("saran"):
                    baris += ". Mungkin maksudnya: " + "; ".join(m["saran"])
                elif not m.get("pilihan") and m["masalah"] == "tidak dikenal":
                    baris += ". Tidak ada produk yang mirip; daftarkan dulu dengan 'produk tambah'"
                if m.get("pilihan"):
                    baris += ". Pilih salah satu: " + "; ".join(m["pilihan"])
                t.append(baris)
            raise Gagal("\n".join(t), masalah=masalah)
        h = hitung_nota(siap, diskon_spek, param_pajak_cfg(cfg))
        bayar, jumlah_bayar, kembalian, peringatan = susun_bayar(bayar_spek, h["total"])
        peringatan = info_cocok + peringatan
        sesi = sesi_aktif(conn)
        if not sesi:
            peringatan.append(pesan_tanpa_sesi(conn, waktu))
        elif not args.kasir and sesi["kasir"]:
            args.kasir = sesi["kasir"]
        sidik = sidik_nota(h, bayar)
        batas = (waktu - timedelta(minutes=10)).isoformat(" ")
        kembar = conn.execute("SELECT no, waktu FROM nota WHERE sidik=? AND jenis='jual' AND waktu>=? AND waktu<=? "
                              "ORDER BY id DESC LIMIT 1", (sidik, batas, waktu.isoformat(" "))).fetchone()
        perlu_izin = False
        if kembar:
            pesan = ("Isi nota SAMA PERSIS dengan %s (%s), kurang dari 10 menit lalu. Kemungkinan tercatat dobel."
                     % (kembar["no"], kembar["waktu"]))
            if args.ya and not args.izinkan_duplikat:
                raise Gagal(pesan + " Tidak disimpan. Jika memang pembeli berbeda, ulangi dengan --izinkan-duplikat "
                            "setelah pengguna menegaskan.", nota_mirip=kembar["no"])
            if not args.izinkan_duplikat:
                perlu_izin = True
                peringatan.append(pesan + " Tanyakan ke pengguna; jika pembeli berbeda tambahkan --izinkan-duplikat.")
        no = nomor_nota(conn, "jual", waktu)
        nid = simpan_nota(conn, "jual", no, waktu.isoformat(" "), None, cfg["pajak"], h, bayar, jumlah_bayar, kembalian,
                          args, "", sidik, sesi["id"] if sesi else None)
        potong_stok(conn, cfg, h["baris"], -1, nid, waktu.isoformat(" "), args.izinkan_minus, peringatan)
        nota_baru = dict(conn.execute("SELECT * FROM nota WHERE rowid=?", (nid,)).fetchone())
        nota_baru["id"] = nid                      # database lama tanpa kunci utama tetap aman
        kertas = cfg["kertas"] if cfg["kertas"] in ("58", "80") else "58"
        struk_baris = baris_struk(conn, nota_baru, lebar_kertas(kertas), cfg)
        t = ["Nota %s | %s %s" % (no, waktu.strftime("%d/%m/%Y %H:%M"), ZONA[_ZONA_AKTIF["nama"]][1])] + teks_rincian(h, None)
        t.append("Bayar: %s | Kembalian: %s" % (", ".join("%s %s" % (m, fmt_rp(v)) for m, v in bayar.items()),
                                                fmt_rp(kembalian)))
        if args.catatan_nota:
            t.append("Catatan: " + args.catatan_nota)
        for p in peringatan:
            t.append("Catatan: " + p)
        data = {"no": no, "waktu": waktu.isoformat(" "), "pajak_mode": cfg["pajak"],
                "baris": [{"kode": b["kode"], "nama": b["nama"], "varian": b["varian"], "qty": angka_json(b["qty"]),
                           "harga": b["harga"], "bruto": b["bruto"], "diskon_item": b["diskon_item"],
                           "diskon_nota": b["diskon_nota"], "netto": b["netto"]} for b in h["baris"]],
                "bruto": h["bruto"], "diskon_item": h["diskon_item"], "subtotal": h["subtotal"],
                "diskon_nota": h["diskon_nota"], "netto": h["netto"], "service": h["service"], "dpp": h["dpp"],
                "jenis_pajak": jenis_pajak(cfg["pajak"]), "pajak": h["ppn"],
                "ppn": h["ppn"] if cfg["pajak"].startswith("ppn") else 0,
                "pbjt": h["ppn"] if cfg["pajak"].startswith("pbjt") else 0,
                "tarif_pbjt": h["pp"]["tarif"] if cfg["pajak"].startswith("pbjt") else None, "zona": _ZONA_AKTIF["nama"],
                "selisih_pembulatan": h["sisa"], "total": h["total"], "bayar": bayar, "jumlah_bayar": jumlah_bayar,
                "kembalian": kembalian, "peringatan": peringatan, "perlu_izin_duplikat": perlu_izin,
                "struk_kertas": kertas, "struk_baris": struk_baris, "struk_teks": blok_kode(struk_baris),
                "ringkasan": {"no": no, "total": h["total"]}}
        return data, "\n".join(t)
    data, teks = jalankan_tulis(args, db, "jual", kerja)
    if args.ya:
        # Setelah tersimpan, struk teks SELALU ikut di hasil: di kanal chat pengguna tidak bisa membuka file di komputer.
        data["teks"] = teks = "\n".join(
            ["TERSIMPAN.", "Nota %s | Total %s | Kembalian %s" % (data["no"], fmt_rp(data["total"]), fmt_rp(data["kembalian"]))]
            + ["Catatan: " + p for p in data["peringatan"]] + ["", "Struk:", data["struk_teks"]])
    if args.ya and args.struk:
        s, _ = cmd_struk(argparse.Namespace(db=args.db, json=True, hari_ini=args.hari_ini, nota=data["no"],
                                            kertas=args.struk, keluar=None, teks=False))
        data["struk"] = s["file"]
        data["teks"] += "\nFile struk siap cetak: " + s["file"]
        teks = data["teks"]
    return data, teks


# --------------------------------------------------------------------------- mulai: pertama kali, satu konfirmasi
FLAG_TOKO = (("nama_toko", "--nama-toko"), ("alamat", "--alamat"), ("telp", "--telp"), ("footer", "--footer"),
             ("npwp", "--npwp"), ("pajak", "--pajak"), ("pkp", "--pkp"), ("stok", "--stok"), ("kertas", "--kertas"),
             ("tarif_pbjt", "--tarif-pbjt"), ("service_charge", "--service-charge"),
             ("service_kena_pajak", "--sc-kena-pajak"), ("zona", "--zona"))


def _langkah(argv):
    """Jalankan satu perintah lewat parser aslinya, supaya aturan & pesan error sama persis dengan perintah terpisah."""
    a = buat_parser().parse_args(argv)
    if not hasattr(a, "ya"):
        a.ya = False
    return a.fungsi(a)[0]


def _rantai_mulai(args, db):
    """Buat buku kasir, masukkan produk, lalu (bila ada pesanan) catat penjualan pertama: semuanya dengan --ya."""
    umum = ["--db=" + str(db), "--json", "--ya"] + (["--hari-ini=" + args.hari_ini] if args.hari_ini else [])
    toko = ["%s=%s" % (flag, getattr(args, attr)) for attr, flag in FLAG_TOKO if getattr(args, attr, None) is not None]
    hasil = {"init": _langkah(["init"] + toko + umum)}
    hasil["impor"] = _langkah(["produk", "impor"] + umum + ["--", args.produk])
    if args.pesan:
        jual = ["jual", "--pesan=" + args.pesan] + umum
        for attr, flag in (("kasir", "--kasir"), ("catatan", "--catatan")):
            if getattr(args, attr, None):
                jual.append("%s=%s" % (flag, getattr(args, attr)))
        hasil["jual"] = _langkah(jual)
    return hasil


def _asumsi_mulai(args):
    """Pengaturan yang BELUM disebut pengguna -> ditandai asumsi (bukan fakta)."""
    a = []
    if args.pajak is None:
        a.append("tanpa pajak (belum PKP dan belum terdaftar pajak restoran)")
    if args.kertas is None:
        a.append("struk untuk printer kertas 58 mm")
    if args.stok is None:
        a.append("stok barang tidak dihitung otomatis")
    if args.zona is None:
        a.append("jam toko WIB")
    if args.alamat is None and args.telp is None:
        a.append("struk tanpa alamat dan nomor telepon")
    elif args.alamat is None:
        a.append("struk tanpa alamat")
    elif args.telp is None:
        a.append("struk tanpa nomor telepon")
    return a


def ringkas_awam(cfg):
    zona = cfg.get("zona") if cfg.get("zona") in ZONA else "Asia/Jakarta"
    stok = {"tidak": "stok tidak dihitung otomatis", "kasir": "stok dipotong kasir",
            "buku-stok": "stok dikelola skill buku-stok"}[cfg["stok"]]
    return ", ".join([label_pajak(cfg["pajak"], cfg.get("tarif_pbjt")), "struk kertas %s mm" % cfg["kertas"], stok,
                      "jam " + ZONA[zona][1]])


def cmd_mulai(args):
    db = path_db(args)
    if db.exists():
        raise Gagal("Buku kasir sudah ada, jadi tidak dibuat ulang. Tambah produk dengan 'produk impor', catat "
                    "penjualan dengan 'jual'.", db=str(db))
    # Selalu dicoba dulu di salinan sementara: bila ada yang gagal, buku kasir asli tidak tersentuh sama sekali.
    tmp = tempfile.mkdtemp(prefix="kasir-pratinjau-")
    try:
        hasil = _rantai_mulai(args, Path(tmp) / "kasir.db")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    if args.ya:
        hasil = _rantai_mulai(args, db)
    cfg, impor, jual = hasil["init"]["pengaturan"], hasil["impor"], hasil.get("jual")
    asumsi = _asumsi_mulai(args)
    peringatan = list(impor.get("peringatan", [])) + (list(jual["peringatan"]) if jual else [])
    baru = impor["baru"]
    identitas = " | ".join(x for x in (cfg["nama_toko"], cfg["alamat"], cfg["telp"]) if x)

    t = ["TERSIMPAN." if args.ya else 'PRATINJAU - belum ada yang disimpan. Cukup balas "ya" sekali untuk menyimpan semuanya.']
    if args.ya:
        t.append('Buku kasir "%s" sudah siap, %d produk masuk.' % (cfg["nama_toko"], len(baru)))
    else:
        t += ["", "1) DAFTAR PRODUK - %d produk akan dimasukkan:" % len(baru)]
        t += ["- %s - %s/%s" % (label_produk(b), fmt_rp(b["harga"]), b["satuan"]) for b in baru[:8]]
        if len(baru) > 8:
            t.append("  ... dan %d produk lain" % (len(baru) - 8))
        t += ["- Baris %d dilewati: %s" % (x["baris"], x["alasan"]) for x in impor["baris_rusak"][:5]]
        t += ["", "2) TOKO", identitas]
        if asumsi:
            t += ["Saya anggap - koreksi bila beda:"] + ["- " + x for x in asumsi]
    if jual:
        t += ["", "%sPenjualan pertama: nota %s%s | Total %s | Kembalian %s" % (
            "" if args.ya else "3) ", jual["no"], "" if args.ya else " (belum disimpan)", fmt_rp(jual["total"]),
            fmt_rp(jual["kembalian"])), "Struk:", jual["struk_teks"]]
    t += ["Catatan: " + p for p in peringatan]
    if args.ya:
        t += ["", "Pengaturan yang dipakai: %s. Mau diubah? Bilang saja." % ringkas_awam(cfg)]
    else:
        t += ["", 'Balas "ya" kalau sudah sesuai. Ada yang beda? Sebutkan saja (mis. "sudah PKP", "kertas 80 mm", '
                  '"bayarnya QRIS").']
    teks = "\n".join(t)
    data = {"ok": True, "mode": "tersimpan" if args.ya else "pratinjau", "perlu_konfirmasi": not args.ya, "db": str(db),
            "toko": {k: cfg[k] for k in ("nama_toko", "alamat", "telp", "pajak", "kertas", "stok", "zona")},
            "asumsi": asumsi, "produk_baru": len(baru), "produk": baru[:15], "baris_rusak": impor["baris_rusak"],
            "peringatan": peringatan, "teks": teks}
    if jual:
        data.update({"no": jual["no"], "total": jual["total"], "kembalian": jual["kembalian"],
                     "struk_kertas": jual["struk_kertas"], "struk_baris": jual["struk_baris"],
                     "struk_teks": jual["struk_teks"],
                     "nota": {k: v for k, v in jual.items() if k not in ("teks", "struk_teks", "struk_baris")}})
    return data, teks


# --------------------------------------------------------------------------- retur & void
def ambil_nota(conn, no):
    if not no:
        raise Gagal("Sebutkan nomor nota (--nota).")
    n = conn.execute("SELECT * FROM nota WHERE no=? COLLATE NOCASE", (no.strip(),)).fetchone()
    if not n:
        mirip = [r["no"] for r in conn.execute("SELECT no FROM nota WHERE no LIKE ? ORDER BY id DESC LIMIT 5",
                                                ("%" + no.strip()[-4:] + "%",))]
        raise Gagal("Nota %s tidak ditemukan.%s" % (no, (" Mungkin: " + ", ".join(mirip)) if mirip else ""))
    return n


def posisi_nota(conn, n):
    """Kembalikan daftar baris asli + qty sudah diretur."""
    rows = []
    for it in conn.execute("SELECT * FROM nota_item WHERE nota_id=? ORDER BY urut", (n["id"],)):
        ret = conn.execute("SELECT COALESCE(SUM(-qty),0) FROM nota_item WHERE ref_item_id=?", (it["id"],)).fetchone()[0]
        rows.append({"item": it, "diretur": Decimal(str(round(ret, 3)))})
    return rows


def sisa_nilai(nilai, q_total, q_diretur):
    """Nilai baris yang tersisa setelah q_diretur dari q_total diretur (proporsional, dibulatkan terdekat).
    Saat semua diretur hasilnya 0 persis."""
    q_total = Decimal(str(q_total))
    return int(nilai) - rhu(Decimal(int(nilai)) * q_diretur / q_total)


def proses_retur(conn, args, n, pilihan, alasan, jenis, refund_metode):
    cfg = pengaturan(conn)
    waktu = parse_waktu(args.waktu) if getattr(args, "waktu", None) else sekarang(args)
    if waktu.isoformat(" ") < n["waktu"]:
        raise Gagal("Waktu retur tidak boleh sebelum waktu nota asal (%s)." % n["waktu"])
    pos = posisi_nota(conn, n)
    sebelum = [(r, r["diretur"]) for r in pos]
    tambahan = {r["item"]["id"]: Decimal(0) for r in pos}
    for r_id, q in pilihan:
        tambahan[r_id] += q
    baris_retur = []
    net_sebelum = net_sesudah = 0
    for r, dr in sebelum:
        it = r["item"]
        Q = Decimal(str(it["qty"]))
        da = dr + tambahan[it["id"]]
        if da > Q:
            raise Gagal("Retur %s melebihi jumlah di nota: dibeli %s, sudah diretur %s, diminta %s."
                        % (it["nama"], fmt_qty(Q), fmt_qty(dr), fmt_qty(tambahan[it["id"]])))
        nb, na = sisa_nilai(it["netto"], Q, dr), sisa_nilai(it["netto"], Q, da)
        net_sebelum += nb
        net_sesudah += na
        if tambahan[it["id"]] > 0:
            bb, ba = sisa_nilai(it["bruto"], Q, dr), sisa_nilai(it["bruto"], Q, da)
            dib = sisa_nilai(it["diskon_item"], Q, dr) - sisa_nilai(it["diskon_item"], Q, da)
            baris_retur.append({"produk_id": it["produk_id"], "kode": it["kode"], "nama": it["nama"], "varian": it["varian"],
                                "satuan": it["satuan"], "qty": -tambahan[it["id"]], "harga": it["harga"],
                                "bruto": -(bb - ba), "diskon_item": -dib, "diskon_nota": -((bb - ba) - dib - (nb - na)),
                                "netto": -(nb - na), "ref_item_id": it["id"], "diskon_item_label": ""})
    if not baris_retur:
        raise Gagal("Tidak ada barang yang diretur.")
    pp = param_pajak_nota(n)
    pb, pa = total_dari_param(net_sebelum, pp), total_dari_param(net_sesudah, pp)
    h = {"baris": baris_retur, "bruto": sum(b["bruto"] for b in baris_retur),
         "diskon_item": sum(b["diskon_item"] for b in baris_retur),
         "diskon_nota": sum(b["diskon_nota"] for b in baris_retur), "netto": net_sesudah - net_sebelum,
         "service": pa["service"] - pb["service"],
         "dpp": pa["dpp"] - pb["dpp"], "ppn": pa["ppn"] - pb["ppn"], "sisa": pa["sisa"] - pb["sisa"],
         "total": pa["total"] - pb["total"], "diskon_nota_label": "", "pp": pp}
    refund = -h["total"]
    ada_retur_lama = any(dr > 0 for _, dr in sebelum)
    if jenis == "void" and not ada_retur_lama and not refund_metode:
        bayar = {}
        for b in conn.execute("SELECT metode, jumlah FROM bayar WHERE nota_id=?", (n["id"],)):
            bayar[b["metode"]] = bayar.get(b["metode"], 0) - b["jumlah"]
        if n["kembalian"]:
            bayar["Tunai"] = bayar.get("Tunai", 0) + n["kembalian"]
        bayar = {m: v for m, v in bayar.items() if v}
    else:
        m = refund_metode or "Tunai"
        bayar = {m: -refund} if refund else {}
    if sum(bayar.values()) != h["total"]:
        raise Gagal("Kesalahan internal: pengembalian dana tidak seimbang.")
    sesi = sesi_aktif(conn)
    if sesi and not getattr(args, "kasir", None) and sesi["kasir"]:
        args.kasir = sesi["kasir"]
    no = nomor_nota(conn, jenis, waktu)
    nid = simpan_nota(conn, jenis, no, waktu.isoformat(" "), n["id"], n["pajak_mode"], h, bayar, sum(bayar.values()), 0,
                      args, alasan, None, sesi["id"] if sesi else None)
    peringatan = []
    if args.stok_kembali == "ya":
        potong_stok(conn, cfg, baris_retur, +1, nid, waktu.isoformat(" "), True, peringatan)
    elif cfg["stok"] == "kasir":
        peringatan.append("Barang retur TIDAK dikembalikan ke stok (rusak/tidak layak jual).")
    if cfg["stok"] == "buku-stok":
        peringatan.append("Stok dikelola buku-stok: " + (
            "setelah ekspor ulang, nota %s berstatus Dibatalkan dan buku-stok mengembalikan stoknya otomatis saat file "
            "diimpor ulang." % n["no"] if jenis == "void" else
            "catat barang yang kembali di buku-stok (masuk --jenis retur-pembeli) setelah dicek fisik. Retur sebagian "
            "tidak ikut file ekspor buku-stok."))
    if not sesi:
        peringatan.append(pesan_tanpa_sesi(conn, waktu) + " (pengembalian uang ini)")
    judul = "VOID" if jenis == "void" else "RETUR"
    t = ["%s %s atas nota %s | %s" % (judul, no, n["no"], waktu.strftime("%d/%m/%Y %H:%M")), "Alasan: " + alasan]
    for b in baris_retur:
        t.append("- %s (%s) %s x | nilai -%s" % (label_produk(b), b["kode"], fmt_qty(-b["qty"]),
                                                   fmt_rp(-b["netto"])))
    if h["ppn"]:
        jp = jenis_pajak(n["pajak_mode"])
        t.append("Koreksi %s: %s | koreksi %s: %s" % (jp, fmt_rp(h["ppn"]), "DPP" if jp == "PPN" else "dasar PBJT",
                                                      fmt_rp(h["dpp"])))
    if h["service"]:
        t.append("Koreksi service charge: %s" % fmt_rp(h["service"]))
    t.append("Uang dikembalikan: %s" % (", ".join("%s %s" % (m, fmt_rp(-v)) for m, v in bayar.items()) or "Rp 0"))
    t.append("Nota asal tidak dihapus; entri ini membalik nilainya.")
    t += ["Catatan: " + p for p in peringatan]
    data = {"no": no, "jenis": jenis, "nota_asal": n["no"], "alasan": alasan, "total": h["total"], "netto": h["netto"],
            "dpp": h["dpp"], "pajak": h["ppn"], "ppn": h["ppn"] if n["pajak_mode"].startswith("ppn") else 0,
            "pbjt": h["ppn"] if n["pajak_mode"].startswith("pbjt") else 0, "service": h["service"],
            "refund": {m: -v for m, v in bayar.items()},
            "baris": [{"kode": b["kode"], "qty": angka_json(b["qty"]), "netto": b["netto"]} for b in baris_retur],
            "peringatan": peringatan, "ringkasan": {"no": no, "nota_asal": n["no"], "total": h["total"]}}
    return data, "\n".join(t)


def cmd_retur(args):
    db = path_db(args)
    if not (args.alasan or "").strip():
        raise Gagal("Alasan retur wajib diisi (--alasan), mis. 'kopi tumpah', 'salah pesanan'.")
    refund = None
    if args.refund:
        refund, _ = metode_dari(args.refund)
        if not refund:
            raise Gagal("Metode pengembalian '%s' tidak dikenal." % args.refund)

    def kerja(conn):
        n = ambil_nota(conn, args.nota)
        if n["jenis"] != "jual":
            raise Gagal("%s adalah entri %s, bukan nota penjualan." % (n["no"], n["jenis"]))
        pos = posisi_nota(conn, n)
        rows = [r["item"] for r in pos]
        unik = {}
        for r in rows:
            unik.setdefault(r["kode"], dict(r))
        sisa = {r["item"]["id"]: Decimal(str(r["item"]["qty"])) - r["diretur"] for r in pos}
        pilihan = []
        unit = SATUAN_BAWAAN | {norm(r["satuan"]) for r in rows}
        for teks in args.item:
            it = parse_item_segmen(teks, unit)
            p, info, qty = cocokkan_item(conn, it, list(unik.values()), unit)
            if p is None:
                raise Gagal("Barang '%s' tidak ada di nota %s atau kurang jelas (%s). Isi nota: %s" % (
                    teks, n["no"], info.get("masalah", ""),
                    "; ".join("%s (%s) x%s %s" % (r["nama"], r["kode"], fmt_qty(r["qty"]), r["satuan"]) for r in rows)))
            cek_qty(qty, p["satuan"], p["nama"])
            butuh = qty
            baris_sama = [r for r in rows if r["kode"] == p["kode"]]
            for r in baris_sama:
                ambil = min(butuh, sisa[r["id"]])
                if ambil > 0:
                    pilihan.append((r["id"], ambil))
                    sisa[r["id"]] -= ambil
                    butuh -= ambil
            if butuh > 0:
                pilihan.append((baris_sama[-1]["id"], butuh))   # memicu pesan 'melebihi jumlah di nota'
        return proses_retur(conn, args, n, pilihan, args.alasan.strip(), "retur", refund)
    return jalankan_tulis(args, db, "retur", kerja)


def cmd_void(args):
    db = path_db(args)
    if not (args.alasan or "").strip():
        raise Gagal("Alasan void wajib diisi (--alasan), mis. 'salah input', 'pembeli batal'.")

    def kerja(conn):
        n = ambil_nota(conn, args.nota)
        if n["jenis"] != "jual":
            raise Gagal("%s adalah entri %s, bukan nota penjualan." % (n["no"], n["jenis"]))
        if conn.execute("SELECT no FROM nota WHERE ref_nota_id=? AND jenis='void'", (n["id"],)).fetchone():
            raise Gagal("Nota %s sudah pernah di-void." % n["no"])
        pos = posisi_nota(conn, n)
        pilihan = [(r["item"]["id"], Decimal(str(r["item"]["qty"])) - r["diretur"]) for r in pos
                   if Decimal(str(r["item"]["qty"])) - r["diretur"] > 0]
        if not pilihan:
            raise Gagal("Semua barang di nota %s sudah diretur; tidak ada yang bisa di-void." % n["no"])
        return proses_retur(conn, args, n, pilihan, args.alasan.strip(), "void", None)
    return jalankan_tulis(args, db, "void", kerja)


# --------------------------------------------------------------------------- nota & struk
def status_nota(conn, n):
    if n["jenis"] != "jual":
        return n["jenis"]
    r = conn.execute("SELECT jenis FROM nota WHERE ref_nota_id=?", (n["id"],)).fetchall()
    if any(x["jenis"] == "void" for x in r):
        return "void"
    if r:
        pos = posisi_nota(conn, n)
        if all(Decimal(str(p["item"]["qty"])) == p["diretur"] for p in pos):
            return "retur penuh"
        return "retur sebagian"
    return "normal"


def cmd_nota(args):
    db, conn = baca(args)
    try:
        if args.no:
            n = ambil_nota(conn, args.no)
            items = [dict(x) for x in conn.execute("SELECT * FROM nota_item WHERE nota_id=? ORDER BY urut", (n["id"],))]
            bayar = {b["metode"]: b["jumlah"] for b in conn.execute("SELECT * FROM bayar WHERE nota_id=?", (n["id"],))}
            st = status_nota(conn, n)
            ref = conn.execute("SELECT no FROM nota WHERE id=?", (n["ref_nota_id"],)).fetchone() if n["ref_nota_id"] else None
            t = ["Nota %s (%s, status: %s) %s" % (n["no"], n["jenis"], st, n["waktu"])]
            if ref:
                t.append("Atas nota: %s | alasan: %s" % (ref["no"], n["alasan"]))
            for x in items:
                t.append("- %s %s (%s) %s x %s = %s%s | bersih %s" % (
                    x["nama"], x["varian"], x["kode"], fmt_qty(x["qty"]), fmt_rp(x["harga"]), fmt_rp(x["bruto"]),
                    (" diskon -%s" % fmt_rp(x["diskon_item"])) if x["diskon_item"] else "", fmt_rp(x["netto"])))
            t.append("Total %s | bayar %s | kembalian %s" % (fmt_rp(n["total"]), ", ".join(
                "%s %s" % (m, fmt_rp(v)) for m, v in bayar.items()), fmt_rp(n["kembalian"])))
            d = {"ok": True, "mode": "baca", "nota": dict(n), "status": st, "item": items, "bayar": bayar}
        else:
            tg = parse_tanggal(args.tanggal, args)
            rows = conn.execute("SELECT * FROM nota WHERE substr(waktu,1,10)=? ORDER BY waktu, id", (tg.isoformat(),)).fetchall()
            daftar = [{"no": r["no"], "jenis": r["jenis"], "waktu": r["waktu"], "total": r["total"],
                       "status": status_nota(conn, r)} for r in rows]
            t = ["Nota %s (%d):" % (tgl_id(tg), len(daftar))]
            for x in daftar:
                tanda = " [%s]" % x["status"] if x["jenis"] == "jual" and x["status"] != "normal" else ""
                t.append("- %s %s %s %s%s" % (x["waktu"][11:16], x["no"], x["jenis"], fmt_rp(x["total"]), tanda))
            d = {"ok": True, "mode": "baca", "tanggal": tg.isoformat(), "nota": daftar}
    finally:
        conn.close()
    d["teks"] = "\n".join(t)
    return d, d["teks"]


def bersih_struk(teks):
    """Buang emoji & simbol gambar (printer thermal umumnya tidak bisa mencetaknya dan lebarnya 2 kolom)."""
    teks = str(teks)
    hasil = []
    for i, ch in enumerate(teks):
        kat = unicodedata.category(ch)
        if ord(ch) > 0xFFFF or kat in ("So", "Cs", "Co") or ch in "\u200d\ufe0f\ufe0e":
            continue
        if ch == " " and hasil and hasil[-1] == " " and i > 0 and teks[i - 1] != " ":
            continue                        # spasi ganda yang tersisa setelah emoji dibuang
        hasil.append(ch)
    return "".join(hasil)


def lebar_tampil(teks):
    """Lebar di font monospace: huruf lebar (CJK, W/F) = 2 kolom, tanda gabung = 0."""
    n = 0
    for ch in teks:
        if unicodedata.combining(ch):
            continue
        n += 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1
    return n


def _potong(k, lebar):
    """Potong kata terlalu panjang menjadi potongan dengan lebar tampil <= lebar."""
    hasil, cur = [], ""
    for ch in k:
        if lebar_tampil(cur + ch) > lebar:
            hasil.append(cur)
            cur = ""
        cur += ch
    return hasil + ([cur] if cur else [])


def _tengah(teks, lebar):
    sisa = max(0, lebar - lebar_tampil(teks))
    return (" " * (sisa // 2) + teks).rstrip()


def _kiri_kanan(kiri, kanan, lebar):
    kiri, kanan = bersih_struk(kiri), bersih_struk(kanan)
    if lebar_tampil(kiri) + lebar_tampil(kanan) + 1 > lebar:
        return _bungkus(kiri, lebar) + [" " * (lebar - lebar_tampil(kanan)) + kanan]
    return [kiri + " " * (lebar - lebar_tampil(kiri) - lebar_tampil(kanan)) + kanan]


def _bungkus(teks, lebar, tengah=False):
    kata, baris, cur = bersih_struk(teks).split(), [], ""
    for k in kata:
        potongan = _potong(k, lebar) if lebar_tampil(k) > lebar else [k]
        for k2 in potongan[:-1]:
            if cur:
                baris.append(cur)
                cur = ""
            baris.append(k2)
        k = potongan[-1]
        if not cur:
            cur = k
        elif lebar_tampil(cur) + 1 + lebar_tampil(k) <= lebar:
            cur += " " + k
        else:
            baris.append(cur)
            cur = k
    if cur:
        baris.append(cur)
    return [_tengah(b, lebar) if tengah else b for b in baris] or [""]


def baris_struk(conn, n, lebar, cfg):
    garis = "-" * lebar
    L = []
    for teks, tengah in ((cfg["nama_toko"].upper(), True), (cfg["alamat"], True), (cfg["telp"], True)):
        if teks:
            L += _bungkus(teks, lebar, tengah=True)
    if n["pajak_mode"] != "tanpa" and cfg.get("npwp"):
        L += _bungkus("NPWP " + cfg["npwp"], lebar, tengah=True)
    L.append(garis)
    judul = {"jual": "", "retur": "RETUR", "void": "VOID / PEMBATALAN"}[n["jenis"]]
    if judul:
        L += _bungkus("*** %s ***" % judul, lebar, tengah=True)
    w = datetime.fromisoformat(n["waktu"])
    L += _kiri_kanan("No", n["no"], lebar)
    zl = label_zona(n["zona"])
    L += _kiri_kanan("Tgl", w.strftime("%d/%m/%Y %H:%M") + ((" " + zl) if zl else ""), lebar)
    if n["kasir"]:
        L += _kiri_kanan("Kasir", n["kasir"], lebar)
    if n["ref_nota_id"]:
        ref = conn.execute("SELECT no FROM nota WHERE id=?", (n["ref_nota_id"],)).fetchone()
        L += _kiri_kanan("Nota asal", ref["no"], lebar)
    L.append(garis)
    for x in conn.execute("SELECT * FROM nota_item WHERE nota_id=? ORDER BY urut", (n["id"],)):
        L += _bungkus(x["nama"] + ((" " + x["varian"]) if x["varian"] else ""), lebar)
        L += _kiri_kanan("  %s %s x %s" % (fmt_qty(x["qty"]), x["satuan"], fmt_angka(x["harga"])), fmt_angka(x["bruto"]), lebar)
        if x["diskon_item"]:
            L += _kiri_kanan("  Diskon %s" % (x["diskon_item_label"] or ""), "-" + fmt_angka(x["diskon_item"])
                             if x["diskon_item"] > 0 else fmt_angka(-x["diskon_item"]), lebar)
    L.append(garis)
    sub = n["bruto"] - n["diskon_item"]
    L += _kiri_kanan("Subtotal", fmt_angka(sub), lebar)
    if n["diskon_nota"]:
        L += _kiri_kanan("Diskon %s" % n["diskon_nota_label"],
                         ("-" + fmt_angka(n["diskon_nota"])) if n["diskon_nota"] > 0 else fmt_angka(-n["diskon_nota"]), lebar)
    tarif = (n["tarif_pajak"] or "?").replace(".", ",")
    if n["service"]:
        L += _kiri_kanan("Service %s%%" % (n["service_persen"] or "").replace(".", ","), fmt_angka(n["service"]), lebar)
    if n["pajak_mode"] == "ppn-belum":
        L += _kiri_kanan("DPP", fmt_angka(n["dpp"]), lebar)
        L += _kiri_kanan("PPN 12% x DPP 11/12", fmt_angka(n["ppn"]), lebar)
    if n["pajak_mode"] == "pbjt-belum":
        L += _kiri_kanan("Dasar PBJT", fmt_angka(n["dpp"]), lebar)
        L += _kiri_kanan("PBJT %s%%" % tarif, fmt_angka(n["ppn"]), lebar)
    L += _kiri_kanan("TOTAL", "Rp " + fmt_angka(n["total"]) if n["total"] >= 0 else "-Rp " + fmt_angka(-n["total"]), lebar)
    for b in conn.execute("SELECT * FROM bayar WHERE nota_id=?", (n["id"],)):
        L += _kiri_kanan(b["metode"] if b["jumlah"] >= 0 else "Dikembalikan (%s)" % b["metode"], fmt_angka(abs(b["jumlah"])), lebar)
    if n["kembalian"]:
        L += _kiri_kanan("Kembalian", fmt_angka(n["kembalian"]), lebar)
    if n["pajak_mode"] == "ppn-termasuk":
        L.append(garis)
        L += _bungkus("Harga sudah termasuk PPN", lebar)
        L += _kiri_kanan("DPP", fmt_angka(n["dpp"]), lebar)
        L += _kiri_kanan("DPP nilai lain 11/12", fmt_desimal(dpp_nilai_lain(n["dpp"])), lebar)
        L += _kiri_kanan("PPN 12%", fmt_angka(n["ppn"]), lebar)
    if n["pajak_mode"] == "pbjt-termasuk":
        L.append(garis)
        L += _bungkus("Harga sudah termasuk PBJT %s%%" % tarif, lebar)
        L += _kiri_kanan("Dasar PBJT", fmt_angka(n["dpp"]), lebar)
        L += _kiri_kanan("PBJT %s%%" % tarif, fmt_angka(n["ppn"]), lebar)
    if n["jenis"] == "jual":
        koreksi = conn.execute("SELECT no, jenis FROM nota WHERE ref_nota_id=? ORDER BY id", (n["id"],)).fetchall()
        if koreksi:
            L += _bungkus("Ada %s: %s" % ("/".join(sorted({k["jenis"] for k in koreksi})),
                                          ", ".join(k["no"] for k in koreksi)), lebar)
    if n["alasan"]:
        L += _bungkus("Alasan: " + n["alasan"], lebar)
    if n["catatan"]:
        L += _bungkus("Catatan: " + n["catatan"], lebar)
    L.append(garis)
    if n["pajak_mode"] != "tanpa":
        L += _bungkus("Struk ini bukan faktur pajak.", lebar, tengah=True)
    if n["jenis"] == "jual" and cfg["footer"]:
        L += _bungkus(cfg["footer"], lebar, tengah=True)
    return L


def lebar_kertas(kertas):
    return 32 if str(kertas) == "58" else 48


def blok_kode(baris):
    """Struk teks dalam blok kode (huruf lebar sama) agar rapi di Telegram/WhatsApp."""
    return "```\n" + "\n".join(baris) + "\n```"


def html_struk(baris, kertas, judul):
    lebar_mm = 58 if kertas == "58" else 80
    cetak_mm = 48 if kertas == "58" else 72
    tinggi = int(len(baris) * 3.4 + 16)
    isi = html.escape("\n".join(baris))
    return """<!DOCTYPE html>
<html lang="id"><head><meta charset="utf-8">
<title>{judul}</title>
<style>
@page {{ size: {lebar}mm {tinggi}mm; margin: 0; }}
html, body {{ margin: 0; padding: 0; background: #fff; color: #000; }}
body {{ width: {lebar}mm; }}
pre {{ width: {cetak}mm; margin: 3mm auto 6mm auto; font-family: "Courier New", Courier, "Liberation Mono", monospace;
      font-size: 2.5mm; line-height: 1.3; white-space: pre; overflow: hidden; }}
.petunjuk {{ font: 12px sans-serif; margin: 8px; padding: 8px; border: 1px dashed #999; max-width: 320px; }}
@media print {{ .petunjuk {{ display: none; }} }}
</style></head>
<body>
<div class="petunjuk">Cetak: tekan Ctrl+P (Mac: Cmd+P) &rarr; pilih printer thermal &rarr; ukuran kertas {lebar} mm &rarr;
margin: Tidak ada/None &rarr; skala 100% &rarr; matikan "Header dan footer". Kotak ini tidak ikut tercetak.</div>
<pre>{isi}</pre>
</body></html>
""".format(judul=html.escape(judul), lebar=lebar_mm, cetak=cetak_mm, tinggi=tinggi, isi=isi)


def cmd_struk(args):
    db = path_db(args)
    conn = buka(db)
    try:
        cfg = pengaturan(conn)
        if args.nota:
            n = ambil_nota(conn, args.nota)
        else:
            n = conn.execute("SELECT * FROM nota ORDER BY id DESC LIMIT 1").fetchone()
            if not n:
                raise Gagal("Belum ada nota.")
        kertas = str(args.kertas or cfg["kertas"])
        if kertas not in ("58", "80"):
            raise Gagal("Kertas harus 58 atau 80 (mm).")
        lebar = lebar_kertas(kertas)
        baris = baris_struk(conn, n, lebar, cfg)
        ke = n["dicetak"] + (0 if args.teks else 1)     # teks untuk chat tidak dihitung sebagai cetakan
        if ke > 1:
            baris.insert(0, _tengah("SALINAN - cetak ke-%d" % ke, lebar))
        if not args.teks:
            conn.execute("UPDATE nota SET dicetak=? WHERE id=?", (ke, n["id"]))
    finally:
        conn.close()
    d = {"ok": True, "mode": "baca", "no": n["no"], "kertas": kertas, "baris": baris, "cetak_ke": ke}
    if args.teks:
        d["teks"] = blok_kode(baris)
        return d, d["teks"]
    keluar = Path(args.keluar).expanduser() if args.keluar else db.parent / "struk" / ("%s-%smm.html" % (n["no"], kertas))
    keluar.parent.mkdir(parents=True, exist_ok=True)
    keluar.write_text(html_struk(baris, kertas, "Struk " + n["no"]), encoding="utf-8")
    d["file"] = str(keluar)
    d["teks"] = ("Struk %s (%s mm) siap cetak: %s\nBuka file di browser lalu Ctrl+P (Mac: Cmd+P), pilih printer thermal, "
                 "margin None, skala 100%%." % (n["no"], kertas, keluar))
    return d, d["teks"]


# --------------------------------------------------------------------------- kas & tutup kasir
def cmd_buka_kasir(args):
    db = path_db(args)
    kas_awal = rupiah_bulat(args.kas_awal, "Kas awal")
    if kas_awal < 0:
        raise Gagal("Kas awal tidak boleh negatif.")

    def kerja(conn):
        s = sesi_aktif(conn)
        if s:
            raise Gagal("Kasir sudah dibuka sejak %s (kas awal %s). Tutup dulu dengan tutup-kasir." % (
                s["buka"], fmt_rp(s["kas_awal"])))
        w = parse_waktu(args.waktu) if args.waktu else sekarang(args)
        akhir = conn.execute("SELECT MAX(tutup) FROM sesi").fetchone()[0]
        if akhir and w.isoformat(" ") < akhir:
            raise Gagal("Waktu buka (%s) sebelum kasir terakhir ditutup (%s)." % (w, akhir))
        sid = conn.execute("INSERT INTO sesi(buka,kas_awal,kasir) VALUES (?,?,?)",
                           (w.isoformat(" "), kas_awal, args.kasir or "")).lastrowid
        n = conn.execute("UPDATE nota SET sesi_id=? WHERE sesi_id IS NULL AND waktu>=?", (sid, w.isoformat(" "))).rowcount
        t = "Buka kasir %s | kas awal (modal kembalian) %s%s%s" % (
            w.strftime("%d/%m/%Y %H:%M"), fmt_rp(kas_awal), (" | kasir " + args.kasir) if args.kasir else "",
            ("\n%d nota sejak jam itu ikut dimasukkan ke sesi ini." % n) if n else "")
        return {"sesi_id": sid, "kas_awal": kas_awal, "nota_disertakan": n, "peringatan": [],
                "ringkasan": {"kas_awal": kas_awal}}, t
    return jalankan_tulis(args, db, "buka-kasir", kerja)


def cmd_kas(args):
    db = path_db(args)
    if bool(args.masuk) == bool(args.keluar):
        raise Gagal("Isi salah satu: --masuk N (tambah uang ke laci) atau --keluar N (ambil uang dari laci).")
    if not (args.catatan or "").strip():
        raise Gagal("Catatan wajib diisi (--catatan), mis. 'beli es batu', 'tambah uang kecil'.")
    j = rupiah_bulat(args.masuk or args.keluar, "Kas")
    if j <= 0:
        raise Gagal("Jumlah kas harus lebih dari 0.")
    j = j if args.masuk else -j

    def kerja(conn):
        s = sesi_aktif(conn)
        if not s:
            raise Gagal("Kasir belum dibuka. Jalankan buka-kasir dulu.")
        w = parse_waktu(args.waktu) if args.waktu else sekarang(args)
        conn.execute("INSERT INTO kas(sesi_id,waktu,jumlah,catatan) VALUES (?,?,?,?)", (s["id"], w.isoformat(" "), j,
                                                                                      args.catatan.strip()))
        t = "Kas %s %s dari laci: %s" % ("masuk" if j > 0 else "keluar", fmt_rp(abs(j)), args.catatan.strip())
        return {"jumlah": j, "peringatan": [], "ringkasan": {"kas": j}}, t
    return jalankan_tulis(args, db, "kas", kerja)


def hitung_sesi(conn, s):
    notas = conn.execute("SELECT * FROM nota WHERE sesi_id=?", (s["id"],)).fetchall()
    per_metode = {}
    kembalian = 0
    for n in notas:
        kembalian += n["kembalian"]
        for b in conn.execute("SELECT metode, jumlah FROM bayar WHERE nota_id=?", (n["id"],)):
            per_metode[b["metode"]] = per_metode.get(b["metode"], 0) + b["jumlah"]
    per_metode["Tunai"] = per_metode.get("Tunai", 0) - kembalian
    kas = conn.execute("SELECT * FROM kas WHERE sesi_id=? ORDER BY waktu", (s["id"],)).fetchall()
    kas_masuk = sum(k["jumlah"] for k in kas if k["jumlah"] > 0)
    kas_keluar = -sum(k["jumlah"] for k in kas if k["jumlah"] < 0)
    seharusnya = s["kas_awal"] + per_metode["Tunai"] + kas_masuk - kas_keluar
    return {"nota_jual": sum(1 for n in notas if n["jenis"] == "jual"),
            "nota_koreksi": sum(1 for n in notas if n["jenis"] != "jual"),
            "total": sum(n["total"] for n in notas), "per_metode": per_metode, "kas_masuk": kas_masuk,
            "kas_keluar": kas_keluar, "rincian_kas": [dict(k) for k in kas], "kas_seharusnya": seharusnya}


def cmd_tutup_kasir(args):
    db = path_db(args)
    fisik = rupiah_bulat(args.kas_fisik, "Kas fisik")
    setoran = rupiah_bulat(args.setoran, "Setoran") if args.setoran not in (None, "") else 0
    if fisik < 0 or setoran < 0:
        raise Gagal("Kas fisik dan setoran tidak boleh negatif.")
    if setoran > fisik:
        raise Gagal("Setoran (%s) lebih besar dari uang di laci (%s)." % (fmt_rp(setoran), fmt_rp(fisik)))

    def kerja(conn):
        s = sesi_aktif(conn)
        if not s:
            raise Gagal("Tidak ada kasir yang sedang dibuka. Jika lupa membuka, jalankan dulu "
                        "buka-kasir --kas-awal N --waktu \"YYYY-MM-DD HH:MM\" (jam mulai jualan), lalu tutup-kasir.")
        w = parse_waktu(args.waktu) if args.waktu else sekarang(args)
        h = hitung_sesi(conn, s)
        selisih = fisik - h["kas_seharusnya"]
        conn.execute("UPDATE sesi SET tutup=?, kas_seharusnya=?, kas_fisik=?, selisih=?, setoran=?, catatan=? WHERE id=?",
                     (w.isoformat(" "), h["kas_seharusnya"], fisik, selisih, setoran, args.catatan or "", s["id"]))
        cfg = pengaturan(conn)
        label = "PAS" if selisih == 0 else ("LEBIH %s" % fmt_rp(selisih) if selisih > 0 else "KURANG %s" % fmt_rp(-selisih))
        t = ["TUTUP KASIR - %s" % (cfg["nama_toko"] or "Toko"),
             "Sesi %s s/d %s%s" % (s["buka"][:16], w.strftime("%Y-%m-%d %H:%M"), (" | kasir " + s["kasir"]) if s["kasir"] else ""),
             "Nota jual: %d | retur/void: %d | total transaksi %s" % (h["nota_jual"], h["nota_koreksi"], fmt_rp(h["total"])),
             "", "Uang tunai di laci:",
             "  Kas awal            %s" % fmt_rp(s["kas_awal"]),
             "  + Tunai bersih      %s" % fmt_rp(h["per_metode"]["Tunai"])]
        if h["kas_masuk"]:
            t.append("  + Kas masuk         %s" % fmt_rp(h["kas_masuk"]))
        if h["kas_keluar"]:
            t.append("  - Kas keluar        %s" % fmt_rp(h["kas_keluar"]))
        t += ["  = Seharusnya        %s" % fmt_rp(h["kas_seharusnya"]),
              "  Dihitung (fisik)    %s" % fmt_rp(fisik),
              "  SELISIH             %s" % label]
        non = {m: v for m, v in h["per_metode"].items() if m != "Tunai" and v}
        if non:
            t.append("")
            t.append("Non-tunai (cocokkan dengan mutasi bank/aplikasi QRIS):")
            for m, v in sorted(non.items()):
                t.append("  %-18s %s" % (m, fmt_rp(v)))
        t += ["", "Disetor ke pemilik: %s | sisa di laci: %s" % (fmt_rp(setoran), fmt_rp(fisik - setoran))]
        pr = []
        if selisih:
            pr.append("Ada selisih kas %s. Cek ulang hitungan uang, nota yang belum dicatat, kembalian salah, atau "
                      "pengeluaran laci yang belum dicatat (perintah kas --keluar)." % label)
        t += ["Catatan: " + p for p in pr]
        return {"sesi_id": s["id"], "kas_awal": s["kas_awal"], "tunai_bersih": h["per_metode"]["Tunai"],
                "kas_masuk": h["kas_masuk"], "kas_keluar": h["kas_keluar"], "kas_seharusnya": h["kas_seharusnya"],
                "kas_fisik": fisik, "selisih": selisih, "setoran": setoran, "sisa_laci": fisik - setoran,
                "per_metode": h["per_metode"], "nota_jual": h["nota_jual"], "peringatan": pr,
                "ringkasan": {"selisih": selisih, "setoran": setoran}}, "\n".join(t)
    return jalankan_tulis(args, db, "tutup-kasir", kerja, backup_label="tutup-kasir")


# --------------------------------------------------------------------------- rekap
def ambil_periode(args):
    if getattr(args, "tahun", None):
        y = int(args.tahun)
        return date(y, 1, 1), date(y, 12, 31), "tahun"
    if getattr(args, "bulan", None):
        y, b = parse_bulan(args.bulan, args)
        akhir = (date(y + (b == 12), b % 12 + 1, 1) - timedelta(days=1))
        return date(y, b, 1), akhir, "bulan"
    if getattr(args, "dari", None) or getattr(args, "sampai", None):
        dari = parse_tanggal(args.dari, args) if args.dari else parse_tanggal("", args).replace(day=1)
        sampai = parse_tanggal(args.sampai, args) if args.sampai else parse_tanggal("", args)
        if sampai < dari:
            raise Gagal("Tanggal --sampai sebelum --dari.")
        return dari, sampai, "rentang"
    t = parse_tanggal(getattr(args, "tanggal", None), args)
    return t, t, "hari"


def data_periode(conn, dari, sampai):
    notas = conn.execute("SELECT * FROM nota WHERE waktu>=? AND waktu<? ORDER BY waktu, id",
                         (dari.isoformat(), (sampai + timedelta(days=1)).isoformat())).fetchall()
    return notas


def hitung_rekap(conn, dari, sampai):
    notas = data_periode(conn, dari, sampai)
    r = {"nota_jual": 0, "nota_retur": 0, "nota_void": 0, "penjualan_kotor": 0, "diskon": 0, "retur_void": 0,
         "penjualan_bersih": 0, "service": 0, "ppn": 0, "pbjt": 0, "pajak": 0, "total_diterima": 0,
         "omzet_tanpa_pajak": 0, "per_metode": {}, "per_produk": {}, "per_jam": {}, "per_bulan": {}, "per_hari": {}}
    di_void = {x[0] for x in conn.execute("SELECT ref_nota_id FROM nota WHERE jenis='void'")}
    nota_sah, total_sah = 0, 0
    for n in notas:
        if n["jenis"] == "jual":
            r["nota_jual"] += 1
            r["penjualan_kotor"] += n["bruto"]
            r["diskon"] += n["diskon_item"] + n["diskon_nota"]
            if n["id"] not in di_void:          # nota yang di-void tidak dihitung di rata-rata & per jam
                nota_sah += 1
                total_sah += n["total"]
                jam = n["waktu"][11:13]
                pj = r["per_jam"].setdefault(jam, {"nota": 0, "total": 0})
                pj["nota"] += 1
                pj["total"] += n["total"]
        else:
            r["nota_" + n["jenis"]] += 1
            r["retur_void"] += n["netto"]
        r["penjualan_bersih"] += n["netto"]
        r["service"] += n["service"] or 0
        r["pajak"] += n["ppn"]
        if n["pajak_mode"].startswith("ppn"):
            r["ppn"] += n["ppn"]
        elif n["pajak_mode"].startswith("pbjt"):
            r["pbjt"] += n["ppn"]
        r["total_diterima"] += n["total"]
        bl = n["waktu"][:7]
        r["per_bulan"][bl] = r["per_bulan"].get(bl, 0) + n["total"] - n["ppn"]
        hr = n["waktu"][:10]
        r["per_hari"][hr] = r["per_hari"].get(hr, 0) + n["total"]
        for b in conn.execute("SELECT metode, jumlah FROM bayar WHERE nota_id=?", (n["id"],)):
            r["per_metode"][b["metode"]] = r["per_metode"].get(b["metode"], 0) + b["jumlah"]
        if n["kembalian"]:
            r["per_metode"]["Tunai"] = r["per_metode"].get("Tunai", 0) - n["kembalian"]
        for it in conn.execute("SELECT * FROM nota_item WHERE nota_id=?", (n["id"],)):
            k = it["kode"]
            p = r["per_produk"].setdefault(k, {"kode": k, "nama": it["nama"] + ((" " + it["varian"]) if it["varian"] else ""),
                                              "satuan": it["satuan"], "qty": Decimal(0), "netto": 0})
            p["qty"] += Decimal(str(it["qty"]))
            p["netto"] += it["netto"]
    r["omzet_tanpa_pajak"] = r["total_diterima"] - r["pajak"]
    r["omzet_tanpa_ppn"] = r["omzet_tanpa_pajak"]          # nama lama (v1.0.0), nilainya sama
    r["nota_dihitung_rata_rata"] = nota_sah
    r["rata_rata_per_nota"] = rhu(Decimal(total_sah) / nota_sah) if nota_sah else 0
    r["per_metode"] = {m: v for m, v in r["per_metode"].items() if v}
    return r, notas


def teks_rekap(r, dari, sampai, jenis, cfg, top=10):
    if jenis == "hari":
        judul = "REKAP KASIR %s, %s" % (HARI[dari.weekday()], tgl_id(dari))
    elif jenis == "bulan":
        judul = "REKAP KASIR %s %d" % (BULAN[dari.month], dari.year)
    elif jenis == "tahun":
        judul = "REKAP OMZET TAHUN %d" % dari.year
    else:
        judul = "REKAP KASIR %s - %s" % (tgl_id(dari), tgl_id(sampai))
    t = [judul]
    if cfg["nama_toko"]:
        t.append(cfg["nama_toko"])
    if not r["nota_jual"] and not r["nota_retur"] and not r["nota_void"]:
        t.append("Belum ada transaksi di periode ini.")
        return "\n".join(t)
    t += ["Nota jual: %d%s" % (r["nota_jual"], (" | retur %d | void %d" % (r["nota_retur"], r["nota_void"]))
                                if r["nota_retur"] or r["nota_void"] else ""),
          "Penjualan kotor : %s" % fmt_rp(r["penjualan_kotor"]),
          "Diskon          : -%s" % fmt_rp(r["diskon"])]
    if r["retur_void"]:
        t.append("Retur/void      : -%s" % fmt_rp(-r["retur_void"]))
    t.append("Penjualan bersih: %s" % fmt_rp(r["penjualan_bersih"]))
    if r["service"]:
        t.append("Service charge  : %s" % fmt_rp(r["service"]))
    if r["ppn"]:
        t.append("PPN terpungut   : %s" % fmt_rp(r["ppn"]))
    if r["pbjt"]:
        t.append("PBJT dipungut   : %s" % fmt_rp(r["pbjt"]))
    t.append("Uang diterima   : %s" % fmt_rp(r["total_diterima"]))
    if r["pajak"]:
        t.append("Omzet tanpa %s: %s" % ("pajak" if r["ppn"] and r["pbjt"] else ("PPN " if r["ppn"] else "PBJT"),
                                         fmt_rp(r["omzet_tanpa_pajak"])))
    if r["nota_dihitung_rata_rata"]:
        t.append("Rata-rata/nota  : %s%s" % (fmt_rp(r["rata_rata_per_nota"]),
                                            " (tanpa nota void)" if r["nota_void"] else ""))
    if r["per_metode"]:
        t += ["", "Per metode bayar:"]
        for m, v in sorted(r["per_metode"].items(), key=lambda x: -x[1]):
            t.append("- %-13s %s" % (m, fmt_rp(v)))
    if jenis == "tahun":
        t += ["", "Omzet per bulan (tanpa PPN/PBJT):"]
        for bl, v in sorted(r["per_bulan"].items()):
            t.append("- %s %s" % (BULAN[int(bl[5:7])].capitalize()[:3], fmt_rp(v)))
    prod = sorted(r["per_produk"].values(), key=lambda p: (-p["netto"], p["kode"]))
    prod = [p for p in prod if p["qty"] != 0 or p["netto"] != 0]
    if prod and jenis != "tahun":
        t += ["", "Produk terlaris (penjualan bersih):"]
        for i, p in enumerate(prod[:top], 1):
            t.append("%d. %s - %s %s - %s" % (i, p["nama"], fmt_qty(p["qty"]), p["satuan"], fmt_rp(p["netto"])))
        if len(prod) > top:
            t.append("(+%d produk lain)" % (len(prod) - top))
    if r["per_jam"] and jenis == "hari":
        t += ["", "Per jam:"]
        for jam, v in sorted(r["per_jam"].items()):
            t.append("%s.00-%s.59  %d nota  %s" % (jam, jam, v["nota"], fmt_rp(v["total"])))
    elif r["per_jam"] and jenis in ("bulan", "rentang"):
        ramai = sorted(r["per_jam"].items(), key=lambda x: (-x[1]["nota"], x[0]))[:3]
        t += ["", "Jam paling ramai: " + ", ".join("%s.00 (%d nota)" % (j, v["nota"]) for j, v in ramai)]
    if r["pbjt"] and jenis in ("bulan", "rentang", "tahun"):
        t += ["", "PBJT yang dipungut dari pembeli periode ini %s: setor & laporkan ke Bapenda sesuai jadwal dan cara "
              "yang diatur Perda daerah Anda (kasir tidak menyetor)." % fmt_rp(r["pbjt"])]
    if jenis in ("bulan", "tahun"):
        t += ["", "Catatan PPh final UMKM: omzet (peredaran bruto, tanpa PPN/PBJT) periode ini %s. Hitung PPh final "
              "0,5%% dengan skill pph-final-umkm (bergantung omzet kumulatif setahun dari SEMUA usaha dan status wajib "
              "pajak; orang pribadi: Rp500 juta pertama setahun tidak kena)." % fmt_rp(r["omzet_tanpa_pajak"])]
    if r["pbjt"]:
        t += ["", "_" + DISCLAIMER_PBJT + "_"]
    if r["ppn"] or jenis in ("bulan", "tahun"):
        t += ["", "_" + DISCLAIMER_PAJAK + "_"]
    return "\n".join(t)


def qty_csv(q, pemisah):
    """Qty pecahan ditulis 1,5 bila pemisah ';' (Excel Indonesia), 1.5 bila pemisah lain."""
    v = angka_json(round(q, 3))
    if isinstance(v, int):
        return v
    t = fmt_qty(v)
    return t if pemisah == ";" else t.replace(",", ".")


def baris_csv_penjualan(conn, notas, pemisah=";"):
    rows = []
    for n in notas:
        bayar = conn.execute("SELECT metode FROM bayar WHERE nota_id=?", (n["id"],)).fetchall()
        metode = "+".join(sorted({b["metode"] for b in bayar}))
        for it in conn.execute("SELECT * FROM nota_item WHERE nota_id=? ORDER BY urut", (n["id"],)):
            rows.append([n["waktu"][:10], n["waktu"][11:16], n["no"], {"jual": "Jual", "retur": "Retur", "void": "Void"}[n["jenis"]],
                         it["kode"], it["nama"], it["varian"], qty_csv(it["qty"], pemisah), it["satuan"], it["harga"],
                         it["diskon_item"] + it["diskon_nota"], it["netto"], "Selesai", metode])
    return rows


HEADER_PENJUALAN = ["Tanggal", "Jam", "No. Nota", "Jenis", "Kode", "Produk", "Varian", "Qty", "Satuan", "Harga Satuan",
                    "Diskon", "Total", "Status", "Metode Bayar"]


def cmd_rekap(args):
    db, conn = baca(args)
    try:
        cfg = pengaturan(conn)
        dari, sampai, jenis = ambil_periode(args)
        r, notas = hitung_rekap(conn, dari, sampai)
        teks = teks_rekap(r, dari, sampai, jenis, cfg)
        d = {"ok": True, "mode": "baca", "periode": {"dari": dari.isoformat(), "sampai": sampai.isoformat(), "jenis": jenis}}
        for k, v in r.items():
            if k == "per_produk":
                d[k] = [{"kode": p["kode"], "nama": p["nama"], "qty": angka_json(p["qty"]), "netto": p["netto"]}
                        for p in sorted(v.values(), key=lambda p: (-p["netto"], p["kode"]))]
            else:
                d[k] = v
        if args.csv:
            d["csv"] = tulis_csv(args.csv, HEADER_PENJUALAN, baris_csv_penjualan(conn, notas, args.pemisah), args.pemisah)
            teks += "\n\nCSV per baris nota: %s" % d["csv"]
        if args.csv_produk:
            d["csv_produk"] = tulis_csv(args.csv_produk, ["Kode", "Produk", "Qty", "Penjualan Bersih"],
                                        [[p["kode"], p["nama"], qty_csv(p["qty"], args.pemisah), p["netto"]] for p in d["per_produk"]], args.pemisah)
            teks += "\nCSV per produk: %s" % d["csv_produk"]
        if jenis in ("tahun",) and r["per_bulan"]:
            y = dari.year
            omzet = [r["per_bulan"].get("%d-%02d" % (y, b), 0) for b in range(1, 13)]
            akhir = max(i for i, v in enumerate(omzet) if v) + 1 if any(omzet) else 0
            awal = min(i for i, v in enumerate(omzet) if v) + 1 if any(omzet) else 1
            d["perintah_pph_final"] = ("python3 <folder-pph-final-umkm>/scripts/pph_final.py --jenis op --tahun %d "
                                       "--bulan-awal %d --omzet %s" % (y, awal, " ".join(str(v) for v in omzet[awal - 1:akhir])))
            teks += ("\n\nBahan skill pph-final-umkm (cek jenis wajib pajak & omzet usaha lain dulu):\n"
                     + d["perintah_pph_final"])
    finally:
        conn.close()
    d["teks"] = teks
    return d, teks


def cmd_ekspor(args):
    db, conn = baca(args)
    try:
        cfg = pengaturan(conn)
        dari, sampai, _ = ambil_periode(args)
        notas = data_periode(conn, dari, sampai)
        pr = []
        if args.format == "penjualan":
            rows = baris_csv_penjualan(conn, notas, args.pemisah)
            path = tulis_csv(args.csv, HEADER_PENJUALAN, rows, args.pemisah)
            t = ("Ekspor %d baris penjualan %s - %s ke %s\nUntuk skill rekap-penjualan-csv: --kolom-tanggal \"Tanggal\" "
                 "--kolom-produk \"Produk\" --kolom-qty \"Qty\" --kolom-total \"Total\" --kolom-status \"Status\" "
                 "(retur/void tercatat sebagai baris minus)." % (len(rows), tgl_id(dari), tgl_id(sampai), path))
        else:
            if cfg["stok"] == "kasir":
                pr.append("PERHATIAN: mode stok toko = kasir (kasir sudah memotong stok). Jika file ini juga diimpor ke "
                          "buku-stok, stok terpotong DOBEL. Pilih satu: atur --stok buku-stok, atau jangan impor file ini.")
            rows, retur = [], []
            for n in notas:
                if n["jenis"] != "jual":
                    if n["jenis"] == "retur":
                        for it in conn.execute("SELECT * FROM nota_item WHERE nota_id=?", (n["id"],)):
                            retur.append("%s %s x%s (%s)" % (n["no"], it["kode"], fmt_qty(-it["qty"]), n["waktu"][:10]))
                    continue
                st = "Dibatalkan" if status_nota(conn, n) == "void" else "Selesai"
                for it in conn.execute("SELECT * FROM nota_item WHERE nota_id=? ORDER BY urut", (n["id"],)):
                    harga_bersih = rhu(Decimal(it["netto"]) / Decimal(str(it["qty"])))
                    rows.append([n["no"], n["waktu"][:16], it["kode"], it["nama"], it["varian"],
                                 qty_csv(it["qty"], args.pemisah), harga_bersih, st])
            path = tulis_csv(args.csv, ["Nomor Pesanan", "Tanggal", "SKU", "Nama Produk", "Varian", "Jumlah",
                                        "Harga Satuan", "Status"], rows, args.pemisah)
            if retur:
                pr.append("Retur sebagian TIDAK ada di file ini (buku-stok tidak menerima jumlah minus). Setelah barang dicek, "
                          "catat di buku-stok: masuk --jenis retur-pembeli. Daftar: " + "; ".join(retur))
            t = ("Ekspor %d baris (%d nota) %s - %s untuk buku-stok: %s\nImpor di buku-stok: stok.py impor-pesanan \"%s\" "
                 "--platform lainnya (pratinjau dulu). Nomor nota yang sudah pernah diimpor dilewati otomatis; nota yang "
                 "di-void berstatus Dibatalkan sehingga stoknya dikembalikan. Kode produk kasir harus sama dengan SKU di "
                 "buku-stok." % (len(rows), len({r[0] for r in rows}), tgl_id(dari), tgl_id(sampai), path, path))
        t += "".join("\nCatatan: " + p for p in pr)
    finally:
        conn.close()
    d = {"ok": True, "mode": "baca", "file": path, "baris": len(rows), "peringatan": pr, "teks": t}
    return d, t


# --------------------------------------------------------------------------- backup & restore
def cmd_backup(args):
    db = path_db(args)
    buka(db).close()
    fol = db.parent / "backup-kasir"
    if args.daftar:
        bks = sorted(fol.glob("*.db")) if fol.is_dir() else []
        t = "Backup (%d):\n%s" % (len(bks), "\n".join("- " + str(b) for b in bks) or "(belum ada)")
        return {"ok": True, "mode": "baca", "backup": [str(b) for b in bks], "teks": t}, t
    p = buat_backup(db, re.sub(r"[^\w-]", "", args.label or "manual") or "manual")
    t = "Backup dibuat: %s" % p
    return {"ok": True, "mode": "tersimpan", "backup": p, "teks": t}, t


def cmd_restore(args):
    db = path_db(args)
    src = Path(args.dari).expanduser()
    if not src.is_file():
        raise Gagal("File backup %s tidak ada." % src)
    c = buka(src)
    n = c.execute("SELECT COUNT(*) FROM nota").fetchone()[0]
    c.close()
    if not args.ya:
        t = ("PRATINJAU (belum disimpan):\nDatabase aktif %s akan diganti dengan %s (%d nota). Database aktif dibackup "
             "dulu.\n\nSimpan? Jalankan ulang + --ya." % (db, src, n))
        return {"ok": True, "mode": "pratinjau", "perlu_konfirmasi": True, "teks": t, "peringatan": []}, t
    bk = buat_backup(db, "sebelum-restore") if db.is_file() else None
    s = sqlite3.connect(str(src))
    d = sqlite3.connect(str(db), timeout=_timeout())
    try:
        s.backup(d)
    finally:
        d.close()
        s.close()
    t = "TERSIMPAN.\nDatabase dipulihkan dari %s (%d nota).%s" % (src, n, ("\nBackup sebelum restore: " + bk) if bk else "")
    return {"ok": True, "mode": "tersimpan", "backup": bk, "teks": t, "peringatan": []}, t


# --------------------------------------------------------------------------- CLI
class ParserID(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        print("GAGAL: perintah tidak lengkap/salah: %s. Lihat --help." % message, file=sys.stderr)
        sys.exit(2)


def buat_parser():
    umum = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
    umum.add_argument("--db", help="File database (default ~/KomunitechData/kasir/kasir.db, ENV KOMUNITECH_KASIR_DB)")
    umum.add_argument("--json", action="store_true", help="Output JSON (untuk agent)")
    umum.add_argument("--hari-ini", help=argparse.SUPPRESS)
    tulis = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
    tulis.add_argument("--ya", action="store_true", help="Simpan (tanpa ini hanya pratinjau)")

    p = ParserID(prog="kasir.py", description="Kasir UMKM lokal (kasir-lokal %s)" % VERSI, allow_abbrev=False)
    p.add_argument("--versi", action="version", version="kasir-lokal " + VERSI)
    sub = p.add_subparsers(dest="perintah", parser_class=ParserID)
    sub.required = True

    def opsi_toko(s):
        s.add_argument("--nama-toko")
        s.add_argument("--alamat")
        s.add_argument("--telp")
        s.add_argument("--footer", help="Teks penutup struk")
        s.add_argument("--npwp", help="NPWP toko (hanya dicetak bila mode PPN)")
        s.add_argument("--pajak", choices=MODE_PAJAK)
        s.add_argument("--pkp", choices=["ya", "tidak"], help="Status Pengusaha Kena Pajak (wajib 'ya' untuk mode PPN)")
        s.add_argument("--stok", choices=MODE_STOK, help="tidak | kasir (kasir memotong stok) | buku-stok")
        s.add_argument("--kertas", choices=["58", "80"])
        s.add_argument("--tarif-pbjt", help="Tarif PBJT makanan/minuman (persen) sesuai Perda daerah, maks 10")
        s.add_argument("--service-charge", help="Service charge persen (0 = tidak ada)")
        s.add_argument("--sc-kena-pajak", dest="service_kena_pajak", choices=["ya", "tidak"],
                       help="Apakah service charge ikut dasar pajak (ikuti Perda/aturan; tanya Bapenda/konsultan)")
        s.add_argument("--zona", help="Zona waktu toko: WIB (default), WITA, WIT, atau Asia/Jakarta dst.")

    s = sub.add_parser("init", parents=[umum, tulis], help="Buat database kasir baru", allow_abbrev=False)
    opsi_toko(s)
    s.set_defaults(fungsi=cmd_init)
    s = sub.add_parser("atur", parents=[umum, tulis], help="Ubah pengaturan toko/pajak/stok/struk", allow_abbrev=False)
    opsi_toko(s)
    s.set_defaults(fungsi=cmd_atur)
    s = sub.add_parser("info", parents=[umum], help="Info database & pengaturan", allow_abbrev=False)
    s.set_defaults(fungsi=cmd_info)
    s = sub.add_parser("mulai", parents=[umum, tulis], allow_abbrev=False,
                       help="Pertama kali: daftar produk + pengaturan toko + penjualan pertama, SATU konfirmasi")
    opsi_toko(s)
    s.add_argument("--produk", required=True, help="File CSV daftar produk")
    s.add_argument("--pesan", help="Penjualan pertama (bahasa bebas, sama seperti 'jual --pesan'); boleh dikosongkan")
    s.add_argument("--kasir")
    s.add_argument("--catatan")
    s.set_defaults(fungsi=cmd_mulai)

    s = sub.add_parser("produk", help="Daftar produk", allow_abbrev=False)
    ps = s.add_subparsers(dest="aksi", parser_class=ParserID)
    ps.required = True
    a = ps.add_parser("tambah", parents=[umum, tulis], allow_abbrev=False)
    a.add_argument("--kode", required=True)
    a.add_argument("--nama", required=True)
    a.add_argument("--varian", default="")
    a.add_argument("--harga", required=True, help="Harga jual (rupiah)")
    a.add_argument("--satuan", default="pcs")
    a.add_argument("--stok", help="Stok awal (opsional)")
    a.set_defaults(fungsi=cmd_produk_tambah)
    a = ps.add_parser("ubah", parents=[umum, tulis], allow_abbrev=False)
    a.add_argument("--kode", required=True)
    for f in ("nama", "harga", "satuan", "stok", "kode-baru"):
        a.add_argument("--" + f)
    a.add_argument("--varian")
    a.add_argument("--tanpa-stok", action="store_true", help="Berhenti melacak stok produk ini")
    a.add_argument("--nonaktif", action="store_true")
    a.add_argument("--aktif", action="store_true")
    a.set_defaults(fungsi=cmd_produk_ubah)
    a = ps.add_parser("cari", parents=[umum], allow_abbrev=False)
    a.add_argument("kata", nargs="?", default="")
    a.add_argument("--semua", action="store_true")
    a.set_defaults(fungsi=cmd_produk_cari)
    a = ps.add_parser("impor", parents=[umum, tulis], allow_abbrev=False)
    a.add_argument("file")
    a.add_argument("--perbarui", action="store_true", help="Perbarui nama/harga produk yang kodenya sudah ada")
    a.set_defaults(fungsi=cmd_produk_impor)

    s = sub.add_parser("stok", parents=[umum, tulis], help="Tambah stok / set hasil hitung fisik (mode stok kasir)", allow_abbrev=False)
    s.add_argument("--kode", required=True)
    s.add_argument("--tambah")
    s.add_argument("--jadi")
    s.add_argument("--catatan")
    s.set_defaults(fungsi=cmd_stok)

    s = sub.add_parser("jual", parents=[umum, tulis], help="Catat penjualan (nota)", allow_abbrev=False)
    s.add_argument("--pesan", help="Pesanan bahasa bebas: '2 kopi susu, 1 roti bakar, diskon 10%%, bayar tunai 100rb'")
    s.add_argument("--item", action="append", help="Satu barang: '2 kopi susu diskon 10%%' (boleh berulang)")
    s.add_argument("--diskon", help="Diskon nota: 10%%, 5rb, 10%%+5%%")
    s.add_argument("--bayar", action="append", help="tunai=100rb | qris | transfer=50rb (boleh berulang)")
    s.add_argument("--kasir")
    s.add_argument("--catatan")
    s.add_argument("--waktu", help="Catat transaksi yang terlewat: 'YYYY-MM-DD HH:MM'")
    s.add_argument("--izinkan-duplikat", action="store_true")
    s.add_argument("--izinkan-minus", action="store_true")
    s.add_argument("--struk", choices=["58", "80"], help="Langsung buat file struk setelah tersimpan")
    s.set_defaults(fungsi=cmd_jual)

    s = sub.add_parser("retur", parents=[umum, tulis], help="Retur sebagian barang dari nota (entri balik)", allow_abbrev=False)
    s.add_argument("--nota", required=True)
    s.add_argument("--item", action="append", required=True, help="'1 kopi susu' (boleh berulang)")
    s.add_argument("--alasan", required=True)
    s.add_argument("--refund", help="Metode uang kembali (default tunai)")
    s.add_argument("--stok-kembali", choices=["ya", "tidak"], default="ya")
    s.add_argument("--waktu")
    s.set_defaults(fungsi=cmd_retur)
    s = sub.add_parser("void", parents=[umum, tulis], help="Batalkan seluruh nota (entri balik)", allow_abbrev=False)
    s.add_argument("--nota", required=True)
    s.add_argument("--alasan", required=True)
    s.add_argument("--stok-kembali", choices=["ya", "tidak"], default="ya")
    s.add_argument("--waktu")
    s.set_defaults(fungsi=cmd_void)

    s = sub.add_parser("nota", parents=[umum], help="Lihat satu nota atau daftar nota per tanggal", allow_abbrev=False)
    s.add_argument("--no")
    s.add_argument("--tanggal")
    s.set_defaults(fungsi=cmd_nota)
    s = sub.add_parser("struk", parents=[umum], help="Buat struk HTML siap cetak 58/80 mm", allow_abbrev=False)
    s.add_argument("--nota", help="Nomor nota (default nota terakhir)")
    s.add_argument("--kertas", choices=["58", "80"])
    s.add_argument("--keluar", help="Path file HTML")
    s.add_argument("--teks", action="store_true", help="Tampilkan struk sebagai teks (untuk chat)")
    s.set_defaults(fungsi=cmd_struk)

    s = sub.add_parser("buka-kasir", parents=[umum, tulis], help="Mulai sesi kasir dengan kas awal", allow_abbrev=False)
    s.add_argument("--kas-awal", required=True)
    s.add_argument("--kasir")
    s.add_argument("--waktu")
    s.set_defaults(fungsi=cmd_buka_kasir)
    s = sub.add_parser("kas", parents=[umum, tulis], help="Uang masuk/keluar laci di luar penjualan", allow_abbrev=False)
    s.add_argument("--masuk")
    s.add_argument("--keluar")
    s.add_argument("--catatan")
    s.add_argument("--waktu")
    s.set_defaults(fungsi=cmd_kas)
    s = sub.add_parser("tutup-kasir", parents=[umum, tulis], help="Tutup sesi: hitung selisih kas & setoran", allow_abbrev=False)
    s.add_argument("--kas-fisik", required=True, help="Uang tunai yang benar-benar ada di laci")
    s.add_argument("--setoran", help="Uang yang diambil/disetor ke pemilik")
    s.add_argument("--catatan")
    s.add_argument("--waktu")
    s.set_defaults(fungsi=cmd_tutup_kasir)

    def opsi_periode(s):
        s.add_argument("--tanggal", help="hari-ini | kemarin | YYYY-MM-DD")
        s.add_argument("--bulan", help="ini | lalu | YYYY-MM")
        s.add_argument("--tahun")
        s.add_argument("--dari")
        s.add_argument("--sampai")
        s.add_argument("--pemisah", default=";", help="Pemisah CSV (default ';' untuk Excel Indonesia)")

    s = sub.add_parser("rekap", parents=[umum], help="Rekap harian/bulanan/tahunan", allow_abbrev=False)
    opsi_periode(s)
    s.add_argument("--csv", help="CSV per baris nota (kompatibel rekap-penjualan-csv)")
    s.add_argument("--csv-produk", help="CSV ringkasan per produk")
    s.set_defaults(fungsi=cmd_rekap)
    s = sub.add_parser("ekspor", parents=[umum], help="Ekspor CSV penjualan / untuk buku-stok", allow_abbrev=False)
    opsi_periode(s)
    s.add_argument("--format", choices=["penjualan", "buku-stok"], default="penjualan")
    s.add_argument("--csv", required=True)
    s.set_defaults(fungsi=cmd_ekspor)

    s = sub.add_parser("backup", parents=[umum], help="Salinan database bertanggal", allow_abbrev=False)
    s.add_argument("--label")
    s.add_argument("--daftar", action="store_true")
    s.set_defaults(fungsi=cmd_backup)
    s = sub.add_parser("restore", parents=[umum, tulis], help="Pulihkan dari backup", allow_abbrev=False)
    s.add_argument("--dari", required=True)
    s.set_defaults(fungsi=cmd_restore)
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
        return 1
    except sqlite3.OperationalError as e:
        pesan = (PESAN_TERKUNCI % _timeout()) if _terkunci(e) else \
            "Kesalahan database: %s. Jangan hapus file database; coba lagi atau pulihkan dari backup." % e
        print(json.dumps({"ok": False, "error": pesan}, ensure_ascii=False) if args.json else "GAGAL: " + pesan,
              file=sys.stdout if args.json else sys.stderr)
        return 1
    except OSError as e:
        pesan = "File tidak bisa ditulis/dibaca (%s). Periksa folder dan izin aksesnya." % e
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
