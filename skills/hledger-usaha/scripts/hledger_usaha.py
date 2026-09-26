#!/usr/bin/env python3
"""hledger-usaha (Komunitech) - asisten pembukuan teks hledger untuk UMKM Indonesia.

Python standar saja. Bila program hledger terpasang, script memakainya sebagai mesin baca
(`hledger print -O json`) dan pemeriksa (`hledger check`). Bila tidak terpasang, script memakai
pembaca bawaan untuk format jurnal yang ditulis skill ini, jadi tetap bisa mencatat dan membuat
laporan.

Perintah:
  init         buat file jurnal baru berakun Indonesia (+ aturan bank)
  cek          cek hledger, file jurnal, dan hal yang perlu dicek
  catat        catat transaksi (pratinjau; simpan dengan --ya)
  impor-bank   ubah CSV mutasi bank menjadi transaksi (aturan hledger .rules)
  tambah-aturan tambah kata kunci ke aturan bank
  stok-akhir   penyesuaian nilai persediaan akhir bulan (hasil hitung stok)
  saldo        saldo akun per tanggal (+ cocokkan dengan saldo nyata)
  laba-rugi | neraca | arus-kas | bulanan   laporan dalam Rupiah
  ekspor-emkm  buku kas CSV + perintah untuk skill laporan-keuangan-emkm
  backup       salin jurnal & aturan ke folder backup

Windows: pakai `python` atau `py` sebagai ganti `python3`.
"""
import argparse
import csv
import datetime as dt
import difflib
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

VERSI = "1.0.0"
HLEDGER_TERUJI = ("1.52.4",)
SINI = os.path.dirname(os.path.abspath(__file__))
FOLDER_SKILL = os.path.dirname(SINI)
TEMPLATE_JURNAL = os.path.join(FOLDER_SKILL, "templates", "jurnal-awal.journal")
TEMPLATE_ATURAN = os.path.join(FOLDER_SKILL, "templates", "aturan-bank.rules")
JURNAL_DEFAULT = os.path.join(os.path.expanduser("~"), "Pembukuan", "usaha.journal")

K_INPUT, K_FILE, K_JURNAL, K_HLEDGER, K_TULIS, K_GANDA = 2, 3, 4, 5, 6, 7
NOL = Decimal(0)
SEN = Decimal("0.01")
MAKS_NOMINAL = Decimal("1000000000000")  # Rp 1 triliun per baris

BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September",
         "Oktober", "November", "Desember"]
BULAN_KATA = {
    "jan": 1, "januari": 1, "january": 1, "feb": 2, "februari": 2, "february": 2, "peb": 2, "mar": 3,
    "maret": 3, "march": 3, "apr": 4, "april": 4, "mei": 5, "may": 5, "jun": 6, "juni": 6, "june": 6,
    "jul": 7, "juli": 7, "july": 7, "agu": 8, "agt": 8, "ags": 8, "agustus": 8, "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9, "okt": 10, "oktober": 10, "oct": 10, "october": 10,
    "nov": 11, "nop": 11, "november": 11, "des": 12, "desember": 12, "dec": 12, "december": 12,
}


class Gagal(Exception):
    def __init__(self, pesan, kode=K_INPUT):
        super().__init__(pesan)
        self.kode = kode


# ============================================================ angka & tanggal

def rp(x, tanda_plus=False):
    """Decimal -> 'Rp 1.500.000' / '-Rp 1.500.000' / 'Rp 1.250,50' (sen hanya bila ada)."""
    x = Decimal(x).quantize(SEN, ROUND_HALF_UP)
    neg = x < 0
    x = abs(x)
    bulat = int(x)
    sen = int((x - bulat) * 100)
    s = "{:,}".format(bulat).replace(",", ".")
    if sen:
        s += ",{:02d}".format(sen)
    awal = "-" if neg else ("+" if tanda_plus and x > 0 else "")
    return awal + "Rp " + s


def persen(a, b):
    if not b:
        return None
    return (Decimal(a) * 100 / Decimal(b)).quantize(Decimal("0.1"), ROUND_HALF_UP)


def teks_persen(p):
    return str(p).replace(".", ",") + "%"


def parse_nominal(teks, boleh_negatif=False, label="nominal"):
    """Nominal gaya Indonesia: 'Rp 1.500.000', '1.500.000,50', '1500000', '1,5jt', '150rb', '2 miliar'.
    '62,500' ditolak karena ambigu (62,5 atau 62.500?)."""
    if teks is None:
        raise Gagal("{} kosong.".format(label))
    s = str(teks).strip().lower().replace(" ", " ")
    if not s:
        raise Gagal("{} kosong.".format(label))
    neg = False
    if s.startswith("-"):
        neg, s = True, s[1:].strip()
    s = re.sub(r"^(rp\.?|idr)\s*", "", s).strip()
    if s.startswith("-"):
        neg, s = True, s[1:].strip()
    s = re.sub(r"[,.]\s*-$", "", s).strip()
    kali = Decimal(1)
    m = re.match(r"^([\d.,]+)\s*(jt|juta|rb|ribu|k|miliar|milyar|m)?$", s)
    if not m:
        raise Gagal("{} '{}' bukan angka rupiah yang dikenali. Contoh: 150000, 150.000, 150rb, 1,5jt."
                    .format(label, teks))
    angka, akhiran = m.group(1), m.group(2)
    if akhiran == "m":
        raise Gagal("{} '{}': akhiran 'm' ambigu (juta atau miliar?). Tulis 'jt' atau 'miliar'."
                    .format(label, teks))
    if akhiran in ("jt", "juta"):
        kali = Decimal(1000000)
    elif akhiran in ("rb", "ribu", "k"):
        kali = Decimal(1000)
    elif akhiran in ("miliar", "milyar"):
        kali = Decimal(1000000000)
    if akhiran:
        a = angka.replace(",", ".")
        if a.count(".") > 1 or (a.count(".") == 1 and len(a.split(".")[1]) > 3):
            raise Gagal("{} '{}' tidak jelas.".format(label, teks))
        nilai = Decimal(a) * kali
    else:
        if "," in angka and "." in angka:
            if angka.rfind(",") < angka.rfind("."):
                raise Gagal("{} '{}': format Inggris (koma ribuan, titik desimal). Tulis gaya Indonesia, "
                            "mis. 1.500.000,50.".format(label, teks))
            if not re.match(r"^\d{1,3}(\.\d{3})+,\d+$", angka):
                raise Gagal("{} '{}' tidak jelas.".format(label, teks))
            a = angka.replace(".", "").replace(",", ".")
        elif "," in angka:
            bag = angka.split(",")
            if len(bag) == 2 and len(bag[1]) == 3:
                raise Gagal("{} '{}' ambigu: maksudnya {} (desimal) atau {}? Tulis ulang tanpa koma "
                            "atau dengan titik ribuan.".format(label, teks, angka, angka.replace(",", ".")))
            if len(bag) > 2:
                if not re.match(r"^\d{1,3}(,\d{3})+$", angka):
                    raise Gagal("{} '{}' tidak jelas.".format(label, teks))
                a = angka.replace(",", "")
            else:
                a = angka.replace(",", ".")
        elif "." in angka:
            bag = angka.split(".")
            if len(bag) == 2 and len(bag[1]) != 3:
                raise Gagal("{} '{}' tidak jelas: titik dipakai sebagai pemisah ribuan di Indonesia. "
                            "Untuk sen pakai koma (mis. 1.250,50).".format(label, teks))
            if not re.match(r"^\d{1,3}(\.\d{3})+$", angka):
                raise Gagal("{} '{}' tidak jelas.".format(label, teks))
            a = angka.replace(".", "")
        else:
            a = angka
        try:
            nilai = Decimal(a)
        except InvalidOperation:
            raise Gagal("{} '{}' bukan angka.".format(label, teks))
    if nilai != nilai.quantize(SEN):
        raise Gagal("{} '{}' punya lebih dari 2 angka desimal (sen).".format(label, teks))
    nilai = nilai.quantize(SEN) if nilai != nilai.to_integral_value() else nilai.to_integral_value()
    if nilai > MAKS_NOMINAL:
        raise Gagal("{} '{}' terlalu besar (maks. Rp 1 triliun per baris). Periksa angka nolnya.".format(label, teks))
    if neg:
        if not boleh_negatif:
            raise Gagal("{} '{}' negatif. Arah uang ditentukan oleh jenis transaksi; tulis angkanya positif."
                        .format(label, teks))
        nilai = -nilai
    return nilai


def hari_ini():
    return dt.date.today()


def parse_tanggal(teks, tahun_default=None, label="tanggal"):
    t = (teks or "").strip().lower().strip("'\"")
    if t in ("", "hari-ini", "hari ini", "today", "sekarang"):
        return hari_ini()
    if t in ("kemarin", "yesterday"):
        return hari_ini() - dt.timedelta(days=1)
    try:
        m = re.match(r"^(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})$", t)
        if m:
            return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        m = re.match(r"^(\d{1,2})[-/.](\d{1,2})[-/.](\d{2,4})$", t)
        if m:
            y = int(m.group(3))
            return dt.date(y + 2000 if y < 100 else y, int(m.group(2)), int(m.group(1)))
        m = re.match(r"^(\d{1,2})[\s\-/]+([a-z]+)\.?[\s\-/,]+(\d{2,4})$", t)
        if m and m.group(2) in BULAN_KATA:
            y = int(m.group(3))
            return dt.date(y + 2000 if y < 100 else y, BULAN_KATA[m.group(2)], int(m.group(1)))
        m = re.match(r"^(\d{1,2})[-/.](\d{1,2})$", t) or re.match(r"^(\d{1,2})\s+([a-z]+)$", t)
        if m:
            bl = BULAN_KATA.get(m.group(2)) if not m.group(2).isdigit() else int(m.group(2))
            if bl:
                y = tahun_default or hari_ini().year
                return dt.date(y, bl, int(m.group(1)))
    except ValueError:
        raise Gagal("{} '{}' tidak ada di kalender.".format(label, teks))
    raise Gagal("{} '{}' tidak dikenali. Pakai 2026-09-25, 25/09/2026, 25 Sep 2026, 'hari-ini', atau 'kemarin'."
                .format(label, teks))


def teks_tanggal(d):
    return "{} {} {}".format(d.day, BULAN[d.month - 1], d.year)


def akhir_bulan(y, m):
    return dt.date(y + (m == 12), m % 12 + 1, 1) - dt.timedelta(days=1)


def parse_bulan(teks):
    t = (teks or "ini").strip().lower()
    h = hari_ini()
    if t in ("ini", "bulan-ini", "bulan ini"):
        y, m = h.year, h.month
    elif t in ("lalu", "bulan-lalu", "bulan lalu", "kemarin"):
        y, m = (h.year, h.month - 1) if h.month > 1 else (h.year - 1, 12)
    else:
        mm = re.match(r"^(\d{4})-(\d{1,2})$", t) or re.match(r"^(\d{1,2})[/-](\d{4})$", t)
        if mm:
            a, b = int(mm.group(1)), int(mm.group(2))
            y, m = (a, b) if a > 12 else (b, a)
        else:
            mm = re.match(r"^([a-z]+)\s+(\d{4})$", t)
            if not (mm and mm.group(1) in BULAN_KATA):
                raise Gagal("Bulan '{}' tidak dikenali. Pakai 2026-09, 09/2026, 'September 2026', 'ini', "
                            "atau 'lalu'.".format(teks))
            y, m = int(mm.group(2)), BULAN_KATA[mm.group(1)]
        if not 1 <= m <= 12:
            raise Gagal("Bulan '{}' tidak ada.".format(teks))
    return dt.date(y, m, 1), akhir_bulan(y, m)


def periode_dari_arg(a):
    if getattr(a, "dari", None) or getattr(a, "sampai", None):
        if not (a.dari and a.sampai):
            raise Gagal("Isi --dari dan --sampai sekaligus (atau pakai --bulan).")
        d1, d2 = parse_tanggal(a.dari, label="--dari"), parse_tanggal(a.sampai, label="--sampai")
        if d2 < d1:
            raise Gagal("--sampai lebih awal dari --dari.")
        return d1, d2
    return parse_bulan(getattr(a, "bulan", None))


def teks_periode(d1, d2):
    return "{} s.d. {}".format(teks_tanggal(d1), teks_tanggal(d2))


# ============================================================ akun

AKAR_GOL = {
    "aset": "aset", "harta": "aset", "assets": "aset", "asset": "aset",
    "utang": "utang", "hutang": "utang", "liabilitas": "utang", "kewajiban": "utang", "liabilities": "utang",
    "modal": "modal", "ekuitas": "modal", "equity": "modal",
    "pendapatan": "pendapatan", "penghasilan": "pendapatan", "revenue": "pendapatan", "revenues": "pendapatan",
    "income": "pendapatan",
    "hpp": "hpp", "harga pokok penjualan": "hpp",
    "beban": "beban", "biaya": "beban", "expenses": "beban", "expense": "beban",
}
TIPE_GOL = {"A": "aset", "C": "kas", "L": "utang", "E": "modal", "R": "pendapatan", "X": "beban", "V": "modal"}


def bersih_akun(nama, label="akun"):
    n = re.sub(r"\s+", " ", str(nama or "").replace("\t", " ")).strip().strip(":")
    n = re.sub(r"\s*:\s*", ":", n)
    if not n:
        raise Gagal("Nama {} kosong.".format(label))
    if any(c in n for c in ";#=@()[]") or re.search(r"\d{4}-\d{2}-\d{2}", n):
        raise Gagal("Nama {} '{}' berisi karakter terlarang (; # = @ ( ) [ ]).".format(label, nama))
    if len(n) > 120 or any(len(bag) > 50 for bag in n.split(":")):
        raise Gagal("Nama {} '{}' terlalu panjang.".format(label, nama))
    return n


def bersih_segmen(teks, label="nama"):
    s = re.sub(r"\s+", " ", str(teks or "")).strip()
    s = re.sub(r"[:;#=@()\[\],|]", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    if not s:
        raise Gagal("{} kosong.".format(label))
    return s[:40].strip()


def bersih_ket(teks):
    s = re.sub(r"\s+", " ", str(teks or "")).strip()
    s = s.replace(";", ",").replace("|", "/")
    return s[:120].strip()


# ============================================================ jurnal: pembaca bawaan

class Transaksi(object):
    __slots__ = ("tanggal", "ket", "tags", "postings", "baris", "urut")

    def __init__(self, tanggal, ket, tags, postings, baris, urut):
        self.tanggal, self.ket, self.tags, self.postings = tanggal, ket, tags, postings
        self.baris, self.urut = baris, urut


class Jurnal(object):
    def __init__(self):
        self.txns = []
        self.tipe_deklarasi = {}   # akun -> huruf tipe (dari directive account)
        self.tipe_posting = {}     # akun -> huruf tipe (dari hledger, sudah diwariskan)
        self.deklarasi = set()
        self.nama_usaha = None
        self.mesin = "bawaan"
        self.versi_hledger = None
        self.catatan = []
        self.path = None

    def akun_dikenal(self):
        s = set(self.deklarasi)
        for t in self.txns:
            for a, _ in t.postings:
                s.add(a)
        return s

    def tipe(self, akun):
        if akun in self.tipe_posting:
            return self.tipe_posting[akun]
        bag = akun.split(":")
        for i in range(len(bag), 0, -1):
            t = self.tipe_deklarasi.get(":".join(bag[:i]))
            if t:
                return t
        return None

    def gol(self, akun):
        """kas / aset / utang / modal / pendapatan / hpp / beban / None"""
        akar = akun.split(":")[0].strip().lower()
        t = self.tipe(akun)
        if t == "C":
            return "kas"
        if t == "X" and (akar in ("hpp", "harga pokok penjualan") or akar.startswith("hpp")):
            return "hpp"
        if t in TIPE_GOL:
            return TIPE_GOL[t]
        g = AKAR_GOL.get(akar)
        if g == "aset":
            kedua = akun.split(":")[1].strip().lower() if ":" in akun else ""
            if kedua in ("kas", "bank", "cash") or kedua.startswith("kas ") or kedua.startswith("bank "):
                return "kas"
        return g


RE_TXN = re.compile(r"^(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})(?:=\S+)?(?:\s+(.*))?$")
RE_TAG = re.compile(r"([^\s,:]+):([^,]*)")
RE_JUMLAH = re.compile(r"^(-)?\s*(Rp|IDR)\s*(-)?\s*([\d.,]+)$")


def ambil_tag(komentar):
    return {k.strip(): v.strip() for k, v in RE_TAG.findall(komentar or "")}


def angka_jurnal(s, dm, no):
    s = s.strip()
    m = RE_JUMLAH.match(s)
    if not m:
        if re.match(r"^-?[\d.,]+$", s):
            raise Gagal("baris {}: jumlah '{}' tanpa 'Rp'. Tulis seperti 'Rp 150.000'.".format(no, s), K_JURNAL)
        raise Gagal("baris {}: jumlah '{}' belum didukung pembaca bawaan (hanya Rupiah, mis. 'Rp 150.000'). "
                    "Pasang hledger untuk format lain.".format(no, s), K_JURNAL)
    neg = bool(m.group(1)) != bool(m.group(3))
    a = m.group(4)
    if dm == ",":
        a = a.replace(".", "").replace(",", ".")
    elif dm == ".":
        a = a.replace(",", "")
    else:
        raise Gagal("File jurnal belum punya baris 'decimal-mark ,'. Pembaca bawaan butuh baris itu "
                    "(file buatan `init` sudah punya).", K_JURNAL)
    try:
        v = Decimal(a)
    except InvalidOperation:
        raise Gagal("baris {}: angka '{}' rusak.".format(no, s), K_JURNAL)
    return -v if neg else v


def baca_file(path):
    try:
        with open(path, "rb") as f:
            mentah = f.read()
    except FileNotFoundError:
        raise Gagal("File jurnal tidak ditemukan: {}\nBuat dulu dengan perintah `init`, atau sebutkan "
                    "--jurnal <path>.".format(path), K_FILE)
    except OSError as e:
        raise Gagal("File {} tidak bisa dibuka: {}".format(path, e), K_FILE)
    if mentah[:4] == b"PK\x03\x04":
        raise Gagal("File {} adalah Excel (.xlsx). Simpan sebagai CSV dulu.".format(path), K_INPUT)
    if mentah[:5] == b"%PDF-":
        raise Gagal("File {} adalah PDF. Unduh mutasi dalam format CSV dari internet banking.".format(path), K_INPUT)
    for enc in ("utf-8-sig", "cp1252"):
        try:
            return mentah.decode(enc)
        except UnicodeDecodeError:
            continue
    return mentah.decode("latin-1", errors="replace")


def nama_usaha_dari(teks):
    m = re.search(r"^;\s*nama-usaha:\s*(.+?)\s*$", teks, re.M)
    return m.group(1) if m else None


def parse_jurnal(teks):
    j = Jurnal()
    j.nama_usaha = nama_usaha_dari(teks)
    dm = None
    kini = None          # [tanggal, ket, tags, postings(list of [akun, nilai|None, assert, baris]), baris]
    blok_directive = False
    semua = []

    def tutup():
        if kini is None:
            return
        tgl, ket, tags, ps, no = kini
        if len(ps) < 2:
            raise Gagal("baris {}: transaksi '{}' butuh minimal 2 baris akun.".format(no, ket), K_JURNAL)
        kosong = [p for p in ps if p[1] is None]
        total = sum((p[1] for p in ps if p[1] is not None), NOL)
        if len(kosong) > 1:
            raise Gagal("baris {}: lebih dari satu baris akun tanpa jumlah.".format(no), K_JURNAL)
        if kosong:
            kosong[0][1] = -total
        elif total != 0:
            raise Gagal("baris {}: transaksi '{}' tidak seimbang (selisih {}).".format(no, ket, rp(total)), K_JURNAL)
        semua.append((Transaksi(tgl, ket, tags, [(p[0], p[1]) for p in ps], no, len(semua)), ps))

    for no, raw in enumerate(teks.splitlines(), start=1):
        baris = raw.rstrip()
        if not baris.strip():
            tutup()
            kini = None
            blok_directive = False
            continue
        if baris[0] in " \t":
            isi = baris.strip()
            if kini is None:
                if blok_directive or isi.startswith(";"):
                    continue
                raise Gagal("baris {}: baris menjorok di luar transaksi: '{}'".format(no, isi), K_JURNAL)
            if isi.startswith(";") or isi.startswith("#"):
                kini[2].update(ambil_tag(isi[1:]))
                continue
            kom = ""
            if ";" in isi:
                isi, kom = isi.split(";", 1)
                isi = isi.rstrip()
            if isi[:2] in ("* ", "! "):
                isi = isi[2:].lstrip()
            if isi[:1] in "([":
                raise Gagal("baris {}: posting virtual '(..)'/'[..]' belum didukung pembaca bawaan.".format(no),
                            K_JURNAL)
            bag = re.split(r"\t|\s{2,}", isi, maxsplit=1)
            akun = bag[0].strip()
            sisa = bag[1].strip() if len(bag) > 1 else ""
            if "@" in sisa:
                raise Gagal("baris {}: harga/kurs '@' belum didukung pembaca bawaan.".format(no), K_JURNAL)
            nilai, cek = None, None
            if "=" in sisa:
                jml, ass = sisa.split("=", 1)
                inklusif = ass.startswith("*") or ass.startswith("=*")
                ass = ass.lstrip("=*").strip()
                cek = (angka_jurnal(ass, dm, no), inklusif)
                sisa = jml.strip()
            if sisa:
                nilai = angka_jurnal(sisa, dm, no)
            kini[3].append([akun, nilai, cek, no])
            continue
        tutup()
        kini = None
        blok_directive = False
        if baris[0] in ";#*%":
            continue
        m = RE_TXN.match(baris)
        if m:
            try:
                tgl = dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
            except ValueError:
                raise Gagal("baris {}: tanggal '{}' tidak ada di kalender.".format(no, baris.split()[0]), K_JURNAL)
            sisa = m.group(4) or ""
            kom = ""
            if ";" in sisa:
                sisa, kom = sisa.split(";", 1)
            sisa = sisa.strip()
            sisa = re.sub(r"^[*!]\s*", "", sisa)
            sisa = re.sub(r"^\([^)]*\)\s*", "", sisa)
            kini = [tgl, sisa.strip(), ambil_tag(kom), [], no]
            continue
        kata = baris.split()[0]
        if kata == "decimal-mark":
            dm = baris.split()[1] if len(baris.split()) > 1 else None
            if dm not in (",", "."):
                raise Gagal("baris {}: decimal-mark harus ',' atau '.'.".format(no), K_JURNAL)
        elif kata == "commodity":
            if not re.search(r"\b(Rp|IDR)\b", baris):
                raise Gagal("baris {}: mata uang selain Rupiah belum didukung.".format(no), K_JURNAL)
            blok_directive = True
        elif kata == "account":
            isi = baris[len("account"):].strip()
            kom = ""
            m2 = re.search(r"(\s{2,}|\t);", isi)
            if m2:
                kom = isi[m2.end():]
                isi = isi[:m2.start()]
            elif isi.startswith(";"):
                isi = ""
            akun = isi.strip()
            if akun:
                j.deklarasi.add(akun)
                t = ambil_tag(kom).get("type")
                if t:
                    j.tipe_deklarasi[akun] = t.strip()[:1].upper()
            blok_directive = True
        else:
            raise Gagal("baris {}: perintah '{}' belum didukung pembaca bawaan. Pasang hledger (lihat "
                        "docs/panduan-hledger.md) untuk membaca file ini.".format(no, kata), K_JURNAL)
    tutup()

    # saldo (balance assertion), urut tanggal lalu urutan tulis, seperti hledger
    semua.sort(key=lambda x: (x[0].tanggal, x[0].urut))
    saldo = {}
    for t, ps in semua:
        for akun, nilai, cek, no in ps:
            saldo[akun] = saldo.get(akun, NOL) + nilai
            if cek:
                harap, inklusif = cek
                kini_saldo = saldo[akun] if not inklusif else sum(
                    (v for a, v in saldo.items() if a == akun or a.startswith(akun + ":")), NOL)
                if kini_saldo != harap:
                    raise Gagal("baris {}: pengecekan saldo gagal. {} seharusnya {}, menurut catatan {} "
                                "(selisih {}).".format(no, akun, rp(harap), rp(kini_saldo), rp(kini_saldo - harap)),
                                K_JURNAL)
        j.txns.append(t)
    return j


# ============================================================ hledger

def cari_hledger(a):
    p = getattr(a, "hledger", None) or os.environ.get("HLEDGER")
    if p:
        if os.path.isfile(p) or shutil.which(p):
            return shutil.which(p) or p
        raise Gagal("Program hledger di '{}' tidak ditemukan.".format(p), K_HLEDGER)
    return shutil.which("hledger")


def jalankan_hledger(hl, argumen, batas=120):
    try:
        r = subprocess.run([hl, "-n"] + argumen, capture_output=True, timeout=batas)
    except subprocess.TimeoutExpired:
        raise Gagal("hledger tidak selesai dalam {} detik.".format(batas), K_HLEDGER)
    except OSError as e:
        raise Gagal("hledger tidak bisa dijalankan: {}".format(e), K_HLEDGER)
    out = r.stdout.decode("utf-8", errors="replace")
    err = r.stderr.decode("utf-8", errors="replace")
    return r.returncode, out, err


def versi_hledger(hl):
    kode, out, _ = jalankan_hledger(hl, ["--version"], 30)
    m = re.search(r"hledger\s+(\d+(?:\.\d+)+)", out)
    return m.group(1) if m else (out.strip() or "?")


def ringkas_galat(err):
    baris = [b for b in err.strip().splitlines() if b.strip()]
    return "\n".join(baris[:14])


def muat_hledger(hl, path):
    kode, out, err = jalankan_hledger(hl, ["-f", path, "print", "-O", "json"])
    if kode != 0:
        raise Gagal("hledger menolak file jurnal:\n" + ringkas_galat(err), K_JURNAL)
    try:
        data = json.loads(out)
    except ValueError:
        raise Gagal("Keluaran hledger tidak bisa dibaca (JSON rusak).", K_HLEDGER)
    j = Jurnal()
    j.mesin = "hledger"
    for i, t in enumerate(data):
        ps = []
        for p in t.get("tpostings", []):
            if p.get("ptype") != "RegularPosting":
                raise Gagal("Transaksi {} {} memakai posting virtual; belum didukung laporan skill ini."
                            .format(t.get("tdate"), t.get("tdescription")), K_JURNAL)
            jumlah = NOL
            for am in p.get("pamount") or []:
                if am.get("acommodity") not in ("Rp", "IDR", "") or am.get("acost"):
                    raise Gagal("Transaksi {} {} memakai mata uang/harga selain Rupiah; belum didukung."
                                .format(t.get("tdate"), t.get("tdescription")), K_JURNAL)
                q = am["aquantity"]
                jumlah += Decimal(int(q["decimalMantissa"])).scaleb(-int(q["decimalPlaces"]))
            akun = p["paccount"]
            ps.append((akun, jumlah))
            tipe = [v for k, v in (p.get("ptags") or []) if k == "type"]
            if tipe and akun not in j.tipe_posting:
                j.tipe_posting[akun] = tipe[0].strip()[:1].upper()
        tags = {k: v for k, v in (t.get("ttags") or [])}
        pos = t.get("tsourcepos") or [{}]
        baris = pos[0].get("sourceLine") if isinstance(pos, list) and pos and isinstance(pos[0], dict) else None
        j.txns.append(Transaksi(dt.date.fromisoformat(t["tdate"]), t.get("tdescription", ""), tags, ps, baris, i))
    j.txns.sort(key=lambda x: (x.tanggal, x.urut))
    return j


def sidik(j):
    hasil = []
    for t in j.txns:
        agg = {}
        for a, v in t.postings:
            agg[a] = agg.get(a, NOL) + v
        hasil.append((t.tanggal.isoformat(), tuple(sorted((a, str(v.normalize())) for a, v in agg.items() if v))))
    return sorted(hasil)


def muat_jurnal(a, wajib_ada=True):
    path = path_jurnal(a)
    teks = baca_file(path)
    mesin = getattr(a, "mesin", "auto")
    hl = cari_hledger(a) if mesin in ("auto", "hledger") else None
    if mesin == "hledger" and not hl:
        raise Gagal("hledger tidak ditemukan. Pasang dulu (docs/panduan-hledger.md) atau pakai --mesin bawaan.",
                    K_HLEDGER)
    bawaan, galat_bawaan = None, None
    try:
        bawaan = parse_jurnal(teks)
    except Gagal as e:
        galat_bawaan = e
    if hl:
        j = muat_hledger(hl, path)
        j.versi_hledger = versi_hledger(hl)
        j.deklarasi = bawaan.deklarasi if bawaan else set()
        j.tipe_deklarasi = bawaan.tipe_deklarasi if bawaan else {}
        j.nama_usaha = nama_usaha_dari(teks)
        if j.versi_hledger not in HLEDGER_TERUJI:
            j.catatan.append("hledger {} belum diuji Komunitech (teruji: {}). Cocokkan angka penting dengan "
                             "`hledger bal`.".format(j.versi_hledger, ", ".join(HLEDGER_TERUJI)))
        if bawaan is not None:
            j.catatan.append("Uji silang pembaca bawaan: " + ("COCOK" if sidik(bawaan) == sidik(j) else
                             "BEDA (laporan memakai hitungan hledger; laporkan ke dukungan Komunitech)"))
    else:
        if galat_bawaan:
            raise galat_bawaan
        j = bawaan
        j.catatan.append("hledger belum terpasang: dihitung dengan pembaca bawaan skill. Panduan pasang: "
                         "docs/panduan-hledger.md.")
    j.path = path
    return j


def path_jurnal(a):
    p = getattr(a, "jurnal", None) or os.environ.get("LEDGER_FILE") or JURNAL_DEFAULT
    return os.path.abspath(os.path.expanduser(p))


def teks_mesin(j):
    if j.mesin == "hledger":
        return "hledger {}".format(j.versi_hledger)
    return "pembaca bawaan skill (hledger belum terpasang)"


# ============================================================ perhitungan

def saldo_per(j, sampai=None, dari=None):
    s = {}
    for t in j.txns:
        if sampai and t.tanggal > sampai:
            continue
        if dari and t.tanggal < dari:
            continue
        for a, v in t.postings:
            s[a] = s.get(a, NOL) + v
    return s


def label2(akun, buang_akar=True):
    bag = akun.split(":")
    if buang_akar:
        return ":".join(bag[1:2]) if len(bag) > 1 else bag[0]
    return ":".join(bag[:2])


def kelompok(pasangan, fungsi_label):
    hasil = {}
    for akun, v in pasangan:
        k = fungsi_label(akun)
        hasil[k] = hasil.get(k, NOL) + v
    return sorted(((k, v) for k, v in hasil.items() if v), key=lambda x: (-abs(x[1]), x[0]))


def belum_dikelompokkan(j, dari, sampai):
    hasil = []
    for t in j.txns:
        if dari <= t.tanggal <= sampai:
            for a, v in t.postings:
                if "belum dikelompokkan" in a.lower():
                    hasil.append((t, a, v))
    return hasil


def hitung_laba_rugi(j, dari, sampai):
    s = saldo_per(j, sampai, dari)
    pend = [(a, -v) for a, v in s.items() if j.gol(a) == "pendapatan"]
    hpp = [(a, v) for a, v in s.items() if j.gol(a) == "hpp"]
    beban = [(a, v) for a, v in s.items() if j.gol(a) == "beban"]
    tp = sum((v for _, v in pend), NOL)
    th = sum((v for _, v in hpp), NOL)
    tb = sum((v for _, v in beban), NOL)
    kotor = tp - th
    bersih = kotor - tb
    return {
        "dari": dari.isoformat(), "sampai": sampai.isoformat(),
        "pendapatan": kelompok(pend, label2), "total_pendapatan": tp,
        "hpp": kelompok(hpp, label2), "total_hpp": th, "laba_kotor": kotor,
        "beban": kelompok(beban, label2), "total_beban": tb, "laba_bersih": bersih,
        "margin_kotor_persen": persen(kotor, tp), "margin_bersih_persen": persen(bersih, tp),
    }


def hitung_neraca(j, per):
    s = saldo_per(j, per)
    awal_tahun = dt.date(per.year, 1, 1)
    aset, utang, modal, lr_lalu, lr_ini, lain = [], [], [], NOL, NOL, []
    for t in j.txns:
        if t.tanggal > per:
            continue
        for a, v in t.postings:
            g = j.gol(a)
            if g in ("pendapatan", "hpp", "beban"):
                if t.tanggal < awal_tahun:
                    lr_lalu -= v
                else:
                    lr_ini -= v
    for a, v in s.items():
        g = j.gol(a)
        if g in ("aset", "kas"):
            aset.append((a, v))
        elif g == "utang":
            utang.append((a, -v))
        elif g == "modal":
            modal.append((a, -v))
        elif g is None and v:
            lain.append((a, v))
    ta = sum((v for _, v in aset), NOL)
    tu = sum((v for _, v in utang), NOL)
    tm = sum((v for _, v in modal), NOL) + lr_lalu + lr_ini
    return {
        "per": per.isoformat(),
        "aset": kelompok(aset, label2), "total_aset": ta,
        "utang": kelompok(utang, label2), "total_utang": tu,
        "modal": kelompok(modal, label2), "laba_tahun_lalu": lr_lalu, "laba_tahun_ini": lr_ini,
        "total_modal": tm, "selisih": ta - tu - tm,
        "akun_tanpa_golongan": [(a, v) for a, v in lain],
    }


def bagi_proporsional(total, bobot):
    """Bagi `total` sesuai bobot (list Decimal >0), dibulatkan ke sen; sisa ke bobot terbesar."""
    jb = sum(bobot, NOL)
    hasil = [(total * b / jb).quantize(SEN, ROUND_HALF_UP) for b in bobot]
    sisa = total - sum(hasil, NOL)
    if sisa:
        i = max(range(len(bobot)), key=lambda k: bobot[k])
        hasil[i] += sisa
    return hasil


def golongan_arus(j, akun):
    g = j.gol(akun)
    kedua = akun.split(":")[1].lower() if ":" in akun else ""
    if g in ("pendapatan", "hpp", "beban"):
        return "operasi"
    if g == "aset":
        if re.match(r"(piutang|persediaan|stok|uang muka|pajak|kasbon)", kedua):
            return "operasi"
        return "investasi"
    if g == "utang":
        if re.match(r"(usaha|dagang|pemasok|supplier|pajak|gaji)", kedua):
            return "operasi"
        return "pendanaan"
    if g == "modal":
        return "pendanaan"
    return "lainnya"


def alokasi_kas(j, t):
    """Kembalikan (delta_kas, [(akun_lawan, nilai_kas)]) untuk satu transaksi."""
    kas = [(a, v) for a, v in t.postings if j.gol(a) == "kas"]
    delta = sum((v for _, v in kas), NOL)
    if not delta:
        return NOL, []
    lawan = [(a, v) for a, v in t.postings if j.gol(a) != "kas"]
    pemberi = [(a, v) for a, v in lawan if (v < 0) == (delta > 0) and v]
    if not pemberi:
        return delta, [("(tanpa akun lawan)", delta)]
    bagian = bagi_proporsional(delta, [abs(v) for _, v in pemberi])
    return delta, [(a, b) for (a, _), b in zip(pemberi, bagian)]


def hitung_arus_kas(j, dari, sampai):
    kas_awal = sum((v for a, v in saldo_per(j, dari - dt.timedelta(days=1)).items() if j.gol(a) == "kas"), NOL)
    kas_akhir_buku = sum((v for a, v in saldo_per(j, sampai).items() if j.gol(a) == "kas"), NOL)
    grup = {"operasi": {}, "investasi": {}, "pendanaan": {}, "lainnya": {}}
    for t in j.txns:
        if not dari <= t.tanggal <= sampai:
            continue
        _, alok = alokasi_kas(j, t)
        for akun, nilai in alok:
            g = golongan_arus(j, akun) if akun != "(tanpa akun lawan)" else "lainnya"
            lab = label2(akun, buang_akar=False)
            d = grup[g].setdefault(lab, [NOL, NOL])
            if nilai > 0:
                d[0] += nilai
            else:
                d[1] += -nilai
    hasil = {"dari": dari.isoformat(), "sampai": sampai.isoformat(), "kas_awal": kas_awal}
    total = NOL
    for g, isi in grup.items():
        baris = sorted(((k, m, k2) for k, (m, k2) in isi.items()), key=lambda x: -(x[1] + x[2]))
        neto = sum((m - k2 for _, m, k2 in baris), NOL)
        hasil[g] = {"baris": baris, "neto": neto}
        total += neto
    hasil["perubahan_kas"] = total
    hasil["kas_akhir"] = kas_awal + total
    hasil["kas_akhir_buku"] = kas_akhir_buku
    hasil["cocok"] = hasil["kas_akhir"] == kas_akhir_buku
    rinci = {}
    for a, v in saldo_per(j, sampai).items():
        if j.gol(a) == "kas" and v:
            rinci[a] = v
    hasil["rincian_kas_akhir"] = sorted(rinci.items())
    return hasil


# ============================================================ format teks

def kepala(judul, j, periode):
    b = [judul]
    if j.nama_usaha:
        b.append(j.nama_usaha)
    b.append(periode)
    return b


def kaki(j):
    b = ["", "Sumber: {} | Dihitung dengan: {}".format(os.path.basename(j.path), teks_mesin(j))]
    for c in j.catatan:
        if not c.startswith("hledger belum terpasang"):
            b.append(c)
    return b


def perlu_dicek(j, dari, sampai):
    bd = belum_dikelompokkan(j, dari, sampai)
    if not bd:
        return []
    b = ["", "PERLU DICEK ({} transaksi belum dikelompokkan, total {})".format(
        len(bd), rp(sum((abs(v) for _, _, v in bd), NOL)))]
    for t, a, v in bd[:10]:
        b.append("- {} {} ({}) {}".format(t.tanggal.isoformat(), t.ket, "masuk" if v < 0 else "keluar", rp(abs(v))))
    if len(bd) > 10:
        b.append("- ... dan {} lainnya".format(len(bd) - 10))
    b.append("Angka laba masih SEMENTARA sampai transaksi ini dikelompokkan.")
    return b


def teks_laba_rugi(j, lr):
    d1, d2 = dt.date.fromisoformat(lr["dari"]), dt.date.fromisoformat(lr["sampai"])
    b = kepala("LAPORAN LABA RUGI", j, "Periode: " + teks_periode(d1, d2))
    b += ["", "PENDAPATAN"]
    b += ["- {}: {}".format(k, rp(v)) for k, v in lr["pendapatan"]] or ["- (belum ada)"]
    b.append("Total pendapatan: " + rp(lr["total_pendapatan"]))
    b += ["", "HARGA POKOK PENJUALAN (HPP)"]
    b += ["- {}: {}".format(k, rp(v)) for k, v in lr["hpp"]] or ["- (belum ada)"]
    b.append("Total HPP: " + rp(lr["total_hpp"]))
    mk = lr["margin_kotor_persen"]
    b += ["", "LABA KOTOR: {}{}".format(rp(lr["laba_kotor"]),
                                         " ({} dari pendapatan)".format(teks_persen(mk)) if mk is not None else "")]
    b += ["", "BEBAN USAHA"]
    b += ["- {}: {}".format(k, rp(v)) for k, v in lr["beban"]] or ["- (belum ada)"]
    b.append("Total beban: " + rp(lr["total_beban"]))
    lb, mb = lr["laba_bersih"], lr["margin_bersih_persen"]
    b += ["", "{}: {}{}".format("LABA BERSIH" if lb >= 0 else "RUGI BERSIH", rp(abs(lb)),
                                " ({} dari pendapatan)".format(teks_persen(mb)) if mb is not None else "")]
    b += perlu_dicek(j, d1, d2)
    return b


def teks_neraca(j, n):
    per = dt.date.fromisoformat(n["per"])
    b = kepala("NERACA (POSISI KEUANGAN)", j, "Per " + teks_tanggal(per))
    b += ["", "ASET (yang dimiliki)"]
    b += ["- {}: {}".format(k, rp(v)) for k, v in n["aset"]] or ["- (belum ada)"]
    b.append("Total aset: " + rp(n["total_aset"]))
    b += ["", "UTANG (kewajiban)"]
    b += ["- {}: {}".format(k, rp(v)) for k, v in n["utang"]] or ["- (tidak ada)"]
    b.append("Total utang: " + rp(n["total_utang"]))
    b += ["", "MODAL"]
    b += ["- {}: {}".format(k, rp(v)) for k, v in n["modal"]]
    if n["laba_tahun_lalu"]:
        b.append("- Laba (rugi) tahun-tahun lalu: " + rp(n["laba_tahun_lalu"]))
    b.append("- Laba (rugi) tahun {} s.d. tanggal ini: {}".format(per.year, rp(n["laba_tahun_ini"])))
    b.append("Total modal: " + rp(n["total_modal"]))
    b.append("")
    if n["selisih"] == 0:
        b.append("Cek: Aset = Utang + Modal ({}). SEIMBANG.".format(rp(n["total_aset"])))
    else:
        b.append("Cek: TIDAK SEIMBANG, selisih {}.".format(rp(n["selisih"])))
    if n["akun_tanpa_golongan"]:
        b.append("Akun tanpa golongan (beri 'type:' di baris account atau pindahkan ke Aset/Utang/Modal/"
                 "Pendapatan/HPP/Beban): " + ", ".join("{} {}".format(a, rp(v)) for a, v in n["akun_tanpa_golongan"]))
    return b


NAMA_ARUS = {"operasi": "ARUS KAS DARI OPERASI (jualan & biaya sehari-hari)",
             "investasi": "ARUS KAS DARI INVESTASI (beli/jual peralatan)",
             "pendanaan": "ARUS KAS DARI PENDANAAN (modal, prive, pinjaman)",
             "lainnya": "LAINNYA"}


def teks_arus_kas(j, ak):
    d1, d2 = dt.date.fromisoformat(ak["dari"]), dt.date.fromisoformat(ak["sampai"])
    b = kepala("LAPORAN ARUS KAS", j, "Periode: " + teks_periode(d1, d2))
    b += ["", "Kas & bank awal: " + rp(ak["kas_awal"])]
    for g in ("operasi", "investasi", "pendanaan", "lainnya"):
        isi = ak[g]
        if g == "lainnya" and not isi["baris"]:
            continue
        b += ["", NAMA_ARUS[g]]
        for lab, masuk, keluar in isi["baris"]:
            bag = []
            if masuk:
                bag.append("masuk " + rp(masuk))
            if keluar:
                bag.append("keluar " + rp(keluar))
            b.append("- {}: {}".format(lab, ", ".join(bag)))
        if not isi["baris"]:
            b.append("- (tidak ada)")
        b.append("Bersih: " + rp(isi["neto"], tanda_plus=True))
    b += ["", "Kenaikan (penurunan) kas: " + rp(ak["perubahan_kas"], tanda_plus=True),
          "Kas & bank akhir: " + rp(ak["kas_akhir"])]
    for a, v in ak["rincian_kas_akhir"]:
        b.append("- {}: {}".format(a, rp(v)))
    b.append("Cek: kas akhir = saldo akun kas & bank. " + ("COCOK." if ak["cocok"] else
             "BEDA {} (laporkan ke dukungan Komunitech).".format(rp(ak["kas_akhir"] - ak["kas_akhir_buku"]))))
    b.append("Pindah uang antar kas/bank sendiri tidak dihitung sebagai masuk/keluar.")
    return b


def jsonable(x):
    if isinstance(x, Decimal):
        return int(x) if x == x.to_integral_value() else float(x)
    if isinstance(x, dict):
        return {k: jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [jsonable(v) for v in x]
    return x


def cetak(a, teks_baris, data):
    if getattr(a, "json", False):
        print(json.dumps(jsonable(dict(data, teks="\n".join(teks_baris))), ensure_ascii=False, indent=2))
    else:
        print("\n".join(teks_baris))


# ============================================================ perintah laporan

def cmd_laba_rugi(a):
    j = muat_jurnal(a)
    d1, d2 = periode_dari_arg(a)
    lr = hitung_laba_rugi(j, d1, d2)
    cetak(a, teks_laba_rugi(j, lr) + kaki(j) + [PENAFIAN], {"laba_rugi": lr, "catatan": j.catatan})


def tanggal_per(a):
    if getattr(a, "tanggal", None):
        return parse_tanggal(a.tanggal)
    if getattr(a, "bulan", None):
        return parse_bulan(a.bulan)[1]
    return hari_ini()


def cmd_neraca(a):
    j = muat_jurnal(a)
    per = tanggal_per(a)
    n = hitung_neraca(j, per)
    cetak(a, teks_neraca(j, n) + kaki(j) + [PENAFIAN], {"neraca": n, "catatan": j.catatan})
    return 0 if n["selisih"] == 0 else K_JURNAL


def cmd_arus_kas(a):
    j = muat_jurnal(a)
    d1, d2 = periode_dari_arg(a)
    ak = hitung_arus_kas(j, d1, d2)
    cetak(a, teks_arus_kas(j, ak) + kaki(j), {"arus_kas": ak, "catatan": j.catatan})


def cmd_bulanan(a):
    j = muat_jurnal(a)
    d1, d2 = periode_dari_arg(a)
    lr = hitung_laba_rugi(j, d1, d2)
    n = hitung_neraca(j, d2)
    ak = hitung_arus_kas(j, d1, d2)
    garis = ["", "-" * 32, ""]
    ring = ["RINGKASAN {}".format(teks_periode(d1, d2).upper())]
    if j.nama_usaha:
        ring.append(j.nama_usaha)
    ring += ["- Pendapatan: " + rp(lr["total_pendapatan"]),
             "- {}: {}".format("Laba bersih" if lr["laba_bersih"] >= 0 else "Rugi bersih", rp(abs(lr["laba_bersih"]))),
             "- Kas & bank akhir: {} ({} dari awal bulan)".format(rp(ak["kas_akhir"]),
                                                                   rp(ak["perubahan_kas"], tanda_plus=True)),
             "- Piutang (belum dibayar pelanggan): " + rp(sum((v for k, v in n["aset"] if "piutang" in k.lower()), NOL)),
             "- Utang: " + rp(n["total_utang"]),
             "- Neraca: " + ("seimbang" if n["selisih"] == 0 else "TIDAK SEIMBANG " + rp(n["selisih"]))]
    tb = ring + garis + teks_laba_rugi(j, lr) + garis + teks_neraca(j, n) + garis + teks_arus_kas(j, ak) + kaki(j)
    tb.append(PENAFIAN)
    cetak(a, tb, {"laba_rugi": lr, "neraca": n, "arus_kas": ak, "catatan": j.catatan})
    return 0 if n["selisih"] == 0 else K_JURNAL


PENAFIAN = ("Laporan manajemen dari catatan Anda sendiri, bukan laporan audit/pajak. Untuk bank/KUR format "
            "SAK EMKM, pakai perintah ekspor-emkm.")


def cmd_saldo(a):
    j = muat_jurnal(a)
    per = tanggal_per(a)
    s = saldo_per(j, per)
    awalan = [bersih_akun(x) for x in (a.akun or [])]
    nyata = {}
    for item in a.nyata or []:
        if "=" not in item:
            raise Gagal("--nyata harus 'Akun=nominal', mis. --nyata \"Aset:Kas=1.250.000\".")
        ak, nom = item.split("=", 1)
        ak = bersih_akun(ak)
        nyata[ak] = parse_nominal(nom, boleh_negatif=True, label="saldo nyata " + ak)
        if ak not in awalan:
            awalan.append(ak)
    dikenal = j.akun_dikenal()
    for p in awalan:
        if not any(x == p or x.startswith(p + ":") for x in dikenal):
            mirip = difflib.get_close_matches(p, sorted(dikenal), n=3, cutoff=0.5)
            raise Gagal("Akun '{}' tidak ada di jurnal.{}".format(p, " Mungkin maksudnya: " + ", ".join(mirip)
                                                                   if mirip else ""))
    b = kepala("SALDO AKUN", j, "Per " + teks_tanggal(per))
    data = {"per": per.isoformat(), "saldo": {}, "cocok": {}}
    if not awalan:
        awalan = sorted({x.split(":")[0] for x in dikenal})
    for p in awalan:
        anak = sorted((x, v) for x, v in s.items() if (x == p or x.startswith(p + ":")) and v)
        total = sum((v for _, v in anak), NOL)
        g = j.gol(p) or ""
        balik = g in ("utang", "modal", "pendapatan")
        b.append("")
        b.append("{}: {}".format(p, rp(-total if balik else total)))
        if len(anak) > 1 or (anak and anak[0][0] != p):
            for x, v in anak:
                b.append("- {}: {}".format(x, rp(-v if balik else v)))
        data["saldo"][p] = -total if balik else total
        if p in nyata:
            catatan_buku = -total if balik else total
            sel = catatan_buku - nyata[p]
            if sel == 0:
                b.append("Dibanding saldo nyata {}: COCOK.".format(rp(nyata[p])))
            else:
                b.append("Dibanding saldo nyata {}: SELISIH {} (catatan {} dari kenyataan).".format(
                    rp(nyata[p]), rp(abs(sel)), "lebih besar" if sel > 0 else "lebih kecil"))
            data["cocok"][p] = {"nyata": nyata[p], "catatan": catatan_buku, "selisih": sel}
    b += kaki(j)
    cetak(a, b, dict(data, catatan=j.catatan))
    return 0 if all(v["selisih"] == 0 for v in data["cocok"].values()) else 1


# ============================================================ menulis jurnal

def baris_posting(akun, nilai):
    jml = rp(nilai).replace("Rp ", "Rp ")
    return "    {:<40}{:>20}".format(akun + "  ", jml)


def teks_transaksi(tanggal, ket, tags, postings):
    kom = ", ".join("{}:{}".format(k, v) for k, v in tags.items() if v is not None)
    kepala_ = "{} {}".format(tanggal.isoformat(), ket) + ("  ; " + kom if kom else "")
    return "\n".join([kepala_] + [baris_posting(a, v) for a, v in postings])


def tulis_jurnal(a, path, tambahan):
    """Tambahkan teks ke akhir jurnal dengan aman: salin cadangan, tulis, periksa ulang, pulihkan bila gagal."""
    cadangan = path + ".sebelum-ubah"
    with open(path, "rb") as f:
        lama = f.read()
    with open(cadangan, "wb") as f:
        f.write(lama)
    sisip = b"" if (not lama or lama.endswith(b"\n\n")) else (b"\n" if lama.endswith(b"\n") else b"\n\n")
    try:
        with open(path, "ab") as f:
            f.write(sisip + tambahan.encode("utf-8") + b"\n")
        a2 = argparse.Namespace(**vars(a))
        muat_jurnal(a2)
        hl = cari_hledger(a) if getattr(a, "mesin", "auto") != "bawaan" else None
        if hl:
            kode, _, err = jalankan_hledger(hl, ["-f", path, "check"])
            if kode != 0:
                raise Gagal("hledger check gagal:\n" + ringkas_galat(err), K_JURNAL)
    except Exception as e:
        with open(path, "wb") as f:
            f.write(lama)
        raise Gagal("GAGAL MENYIMPAN; file jurnal dikembalikan seperti semula. Sebab: {}".format(e), K_TULIS)
    return cadangan


class Rencana(object):
    """Satu transaksi yang akan dicatat."""

    def __init__(self, tanggal, ket, postings, tags, arti):
        self.tanggal, self.ket, self.postings, self.tags, self.arti = tanggal, ket, postings, tags, arti


def akun_bank(j, a_bank):
    if a_bank:
        return bersih_akun(a_bank if ":" in a_bank else "Aset:Bank:" + a_bank)
    dikenal = sorted(x for x in j.akun_dikenal() if j.gol(x) == "kas" and not x.lower().startswith("aset:kas"))
    daun = [x for x in dikenal if not any(y.startswith(x + ":") for y in dikenal)]
    if len(daun) == 1:
        return daun[0]
    if not daun:
        return "Aset:Bank"
    raise Gagal("Ada beberapa rekening bank ({}). Sebutkan yang mana dengan --bank.".format(", ".join(daun)))


def akun_via(j, via, a_bank, arah_tempo, pihak):
    v = (via or "").strip().lower()
    if v in ("kas", "tunai", "cash", "laci"):
        return "Aset:Kas"
    if v in ("bank", "transfer", "tf", "qris", "rekening", "debit"):
        return akun_bank(j, a_bank)
    if v in ("tempo", "utang", "piutang", "bon", "kredit", "nanti"):
        if not arah_tempo:
            raise Gagal("--via tempo tidak berlaku untuk jenis ini.")
        dasar = "Aset:Piutang Usaha" if arah_tempo == "piutang" else "Utang:Usaha"
        return dasar + (":" + bersih_segmen(pihak, "--pihak") if pihak else "")
    if not v:
        raise Gagal("--via belum diisi: dibayar pakai kas (tunai), bank (transfer/QRIS), atau tempo (belum dibayar)?")
    raise Gagal("--via '{}' tidak dikenal. Pilih: kas, bank, tempo.".format(via))


def rencana_dari(j, e, tahun=None):
    """e: dict dari argumen/batch. Kembalikan Rencana."""
    jenis = (e.get("jenis") or "").strip().lower()
    tgl = parse_tanggal(e.get("tanggal"))
    pihak = e.get("pihak")
    ket = bersih_ket(e.get("ket") or "")
    via = e.get("via")
    bank = e.get("bank")
    akun_arg = bersih_akun(e["akun"]) if e.get("akun") else None
    tags = {}
    if pihak:
        tags["pihak"] = bersih_segmen(pihak, "--pihak")

    def nom(k="nominal"):
        if e.get(k) in (None, ""):
            raise Gagal("--{} belum diisi.".format(k))
        v = parse_nominal(e.get(k), label="--" + k)
        if v <= 0:
            raise Gagal("--{} harus lebih dari 0.".format(k))
        return v

    if jenis in ("jual", "penjualan", "jasa"):
        n = nom()
        ak_p = akun_arg or ("Pendapatan:Jasa" if jenis == "jasa" else "Pendapatan:Penjualan")
        lawan = akun_via(j, via, bank, "piutang", pihak)
        ps = [(lawan, n), (ak_p, -n)]
        arti = "Penjualan {}{}{}.".format(rp(n), " kepada " + tags["pihak"] if pihak else "",
                                         ", belum dibayar (piutang bertambah)" if "Piutang" in lawan else
                                         ", uang masuk ke " + lawan)
        ket = ket or ("Penjualan" + (" - " + tags["pihak"] if pihak else ""))
    elif jenis in ("beli", "pembelian", "belanja-stok", "kulakan"):
        n = nom()
        ak_b = akun_arg or "HPP:Pembelian"
        lawan = akun_via(j, via, bank, "utang", pihak)
        ps = [(ak_b, n), (lawan, -n)]
        arti = "Beli barang dagangan/bahan {}{}{}.".format(rp(n), " dari " + tags["pihak"] if pihak else "",
                                                          ", belum dibayar (utang bertambah)" if "Utang" in lawan
                                                          else ", dibayar dari " + lawan)
        ket = ket or "Pembelian barang/bahan"
    elif jenis in ("beban", "biaya", "bayar-biaya"):
        n = nom()
        if not akun_arg:
            raise Gagal("--akun beban belum diisi, mis. --akun \"Beban:Listrik Air Internet\".")
        if j.gol(akun_arg) not in ("beban", "hpp"):
            raise Gagal("--akun untuk jenis beban harus di bawah Beban atau HPP (bukan '{}').".format(akun_arg))
        ps = [(akun_arg, n), (akun_via(j, via, bank, "utang", pihak), -n)]
        arti = "Biaya {} untuk {}.".format(rp(n), akun_arg)
        ket = ket or akun_arg.split(":")[-1]
    elif jenis in ("terima-piutang", "pelunasan-piutang"):
        n = nom()
        dasar = akun_arg or "Aset:Piutang Usaha" + (":" + tags["pihak"] if pihak else "")
        ps = [(akun_via(j, via, bank, None, None), n), (dasar, -n)]
        arti = "Pelanggan membayar piutang {} (piutang berkurang).".format(rp(n))
        ket = ket or "Terima pelunasan" + (" - " + tags["pihak"] if pihak else "")
    elif jenis in ("bayar-utang", "pelunasan-utang"):
        n = nom()
        dasar = akun_arg or "Utang:Usaha" + (":" + tags["pihak"] if pihak else "")
        ps = [(dasar, n), (akun_via(j, via, bank, None, None), -n)]
        arti = "Membayar utang ke pemasok {} (utang berkurang).".format(rp(n))
        ket = ket or "Bayar utang" + (" - " + tags["pihak"] if pihak else "")
    elif jenis in ("modal", "setor-modal", "tambah-modal"):
        n = nom()
        ps = [(akun_via(j, via, bank, None, None), n), (akun_arg or "Modal:Setoran", -n)]
        arti = "Pemilik menambah modal {} (bukan pendapatan).".format(rp(n))
        ket = ket or "Setoran modal pemilik"
    elif jenis in ("prive", "ambil-pribadi"):
        n = nom()
        ps = [(akun_arg or "Modal:Prive", n), (akun_via(j, via, bank, None, None), -n)]
        arti = "Pemilik mengambil uang usaha untuk pribadi {} (prive, mengurangi modal, BUKAN beban).".format(rp(n))
        ket = ket or "Prive (ambil untuk pribadi)"
    elif jenis in ("pinjaman", "terima-pinjaman"):
        n = nom()
        ps = [(akun_via(j, via, bank, None, None), n), (akun_arg or "Utang:Bank", -n)]
        arti = "Menerima pinjaman {} (utang bertambah, bukan pendapatan).".format(rp(n))
        ket = ket or "Pencairan pinjaman"
    elif jenis in ("angsuran", "cicilan"):
        pokok = nom("pokok")
        bunga = parse_nominal(e.get("bunga") or "0", label="--bunga")
        ps = [(akun_arg or "Utang:Bank", pokok)]
        if bunga:
            ps.append(("Beban:Bunga", bunga))
        ps.append((akun_via(j, via, bank, None, None), -(pokok + bunga)))
        arti = "Bayar angsuran {}: pokok {} (utang berkurang){}.".format(
            rp(pokok + bunga), rp(pokok), ", bunga {} (beban)".format(rp(bunga)) if bunga else ", tanpa bunga")
        ket = ket or "Angsuran pinjaman"
    elif jenis in ("transfer", "pindah", "setor-tunai", "tarik-tunai"):
        n = nom()
        dari = akun_via(j, e.get("dari") or ("kas" if jenis == "setor-tunai" else "bank" if jenis == "tarik-tunai"
                                             else None), bank, None, None)
        ke = akun_via(j, e.get("ke") or ("bank" if jenis == "setor-tunai" else "kas" if jenis == "tarik-tunai"
                                         else None), bank, None, None)
        if dari == ke:
            raise Gagal("--dari dan --ke sama.")
        ps = [(ke, n), (dari, -n)]
        arti = "Pindah uang sendiri {} dari {} ke {} (bukan pendapatan/biaya).".format(rp(n), dari, ke)
        ket = ket or "Pindah dana"
    elif jenis in ("aset", "beli-aset", "peralatan"):
        n = nom()
        ps = [(akun_arg or "Aset:Peralatan", n), (akun_via(j, via, bank, "utang", pihak), -n)]
        arti = "Beli peralatan/aset {} (dicatat sebagai aset, bukan beban bulan ini).".format(rp(n))
        ket = ket or "Beli peralatan"
    elif jenis in ("saldo-awal", "bebas"):
        ps, kosong = [], []
        for item in e.get("posting") or []:
            if "=" in item:
                ak, v = item.split("=", 1)
                ps.append((bersih_akun(ak), parse_nominal(v, boleh_negatif=True, label="posting " + ak.strip())))
            else:
                kosong.append(bersih_akun(item))
        if jenis == "saldo-awal":
            if kosong:
                raise Gagal("Saldo awal: tulis setiap akun dengan nominal, mis. --posting \"Aset:Kas=2.000.000\".")
            kosong = [akun_arg or "Modal:Saldo Awal"]
            for ak, v in ps:
                if j.gol(ak) in ("utang", "modal") and v > 0:
                    raise Gagal("Saldo awal utang/modal ditulis NEGATIF di hledger (mis. "
                                "\"Utang:Bank=-5.000.000\"). Periksa tanda {}.".format(ak))
        if not ps:
            raise Gagal("Isi minimal satu --posting \"Akun=nominal\".")
        if len(kosong) > 1:
            raise Gagal("Hanya satu --posting boleh tanpa nominal (dihitung otomatis).")
        total = sum((v for _, v in ps), NOL)
        if kosong:
            if total == 0:
                raise Gagal("Posting tanpa nominal tidak diperlukan: posting lain sudah seimbang.")
            ps.append((kosong[0], -total))
        elif total != 0:
            raise Gagal("Posting tidak seimbang: jumlahnya {} (harus 0).".format(rp(total)))
        if len(ps) < 2:
            raise Gagal("Transaksi butuh minimal dua akun.")
        arti = ("Saldo awal pembukuan per {}.".format(teks_tanggal(tgl)) if jenis == "saldo-awal"
                else "Transaksi bebas {} baris.".format(len(ps)))
        ket = ket or ("Saldo awal" if jenis == "saldo-awal" else "")
        if not ket:
            raise Gagal("--ket (keterangan) wajib untuk jenis bebas.")
    else:
        raise Gagal("--jenis '{}' tidak dikenal. Pilih: jual, jasa, beli, beban, terima-piutang, bayar-utang, "
                    "modal, prive, pinjaman, angsuran, transfer, setor-tunai, tarik-tunai, aset, saldo-awal, "
                    "bebas.".format(e.get("jenis")))
    return Rencana(tgl, ket, ps, tags, arti)


def periksa_akun(j, rencana, akun_baru_ok):
    """Kembalikan daftar akun baru yang perlu dideklarasikan, atau raise bila salah ketik."""
    dikenal = j.akun_dikenal()
    baru = []
    for r in rencana:
        for ak, _ in r.postings:
            if ak in dikenal or ak in baru:
                continue
            akar = ak.split(":")[0]
            if akar not in {x.split(":")[0] for x in dikenal}:
                raise Gagal("Akun '{}' tidak berada di bawah akun utama yang ada ({}).".format(
                    ak, ", ".join(sorted({x.split(':')[0] for x in dikenal}))))
            induk_otomatis = any(ak.startswith(p + ":") for p in ("Aset:Piutang Usaha", "Utang:Usaha",
                                                                    "Aset:Bank"))
            if not (akun_baru_ok or induk_otomatis):
                mirip = difflib.get_close_matches(ak, sorted(dikenal), n=3, cutoff=0.6)
                raise Gagal("Akun '{}' belum ada di jurnal.{} Bila memang akun baru, ulangi dengan --akun-baru."
                            .format(ak, " Mungkin maksudnya: " + ", ".join(mirip) + "." if mirip else ""))
            baru.append(ak)
    return baru


def cari_ganda(j, r):
    agg = sorted((a, v) for a, v in r.postings)
    for t in j.txns:
        if t.tanggal == r.tanggal and t.ket.strip().lower() == r.ket.strip().lower():
            if sorted((a, v) for a, v in t.postings) == agg:
                return t
    return None


def cmd_catat(a):
    j = muat_jurnal(a)
    entri = []
    if a.batch:
        try:
            with open(a.batch, encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, ValueError) as e:
            raise Gagal("File --batch tidak bisa dibaca sebagai JSON: {}".format(e))
        if not isinstance(data, list) or not data or not all(isinstance(x, dict) for x in data):
            raise Gagal("File --batch harus berisi daftar JSON: [{\"jenis\": \"jual\", ...}, ...].")
        if len(data) > 200:
            raise Gagal("Maksimal 200 transaksi per batch.")
        entri = data
    else:
        entri = [{k: getattr(a, k) for k in ("jenis", "tanggal", "nominal", "via", "bank", "pihak", "ket", "akun",
                                              "dari", "ke", "posting", "pokok", "bunga")}]
    rencana = []
    for i, e in enumerate(entri, start=1):
        try:
            rencana.append(rencana_dari(j, e))
        except Gagal as g:
            raise Gagal(("Transaksi ke-{}: ".format(i) if len(entri) > 1 else "") + str(g), g.kode)
    baru = periksa_akun(j, rencana, a.akun_baru)
    ganda = [(i, t) for i, t in ((i, cari_ganda(j, r)) for i, r in enumerate(rencana, 1)) if t]
    b = ["PRATINJAU CATATAN" + ("" if a.ya else " (BELUM disimpan)"), "File: " + j.path, ""]
    teks_baru = []
    if baru:
        teks_baru.append("\n".join("account " + x for x in baru))
    for i, r in enumerate(rencana, 1):
        tx = teks_transaksi(r.tanggal, r.ket, r.tags, r.postings)
        teks_baru.append(tx)
        b.append(tx)
        b.append("Artinya: " + r.arti)
        if r.tanggal > hari_ini() + dt.timedelta(days=1):
            b.append("PERINGATAN: tanggal {} ada di masa depan.".format(r.tanggal.isoformat()))
        b.append("")
    if baru:
        b.append("Akun baru yang akan dibuat: " + ", ".join(baru))
    if ganda and not a.tetap_catat:
        for i, t in ganda:
            b.append("KEMUNGKINAN DOBEL: transaksi ke-{} sama persis dengan catatan {} '{}'.".format(
                i, t.tanggal.isoformat(), t.ket))
        b.append("TIDAK DISIMPAN. Bila memang transaksi berbeda (mis. dua kali beli barang yang sama), "
                 "ulangi dengan --tetap-catat.")
        print("\n".join(b))
        return K_GANDA
    if not a.ya:
        b.append("Simpan {} transaksi ini? Setelah pengguna menjawab ya, ulangi perintah yang sama dengan --ya."
                 .format(len(rencana)))
        print("\n".join(b))
        return 0
    tulis_jurnal(a, j.path, "\n\n".join(teks_baru))
    b[0] = "TERSIMPAN"
    b.append("Tersimpan {} transaksi ke {}. Cadangan versi sebelumnya: {}".format(
        len(rencana), j.path, os.path.basename(j.path) + ".sebelum-ubah"))
    print("\n".join(b))
    return 0


def cmd_stok_akhir(a):
    j = muat_jurnal(a)
    per = parse_tanggal(a.tanggal) if a.tanggal else hari_ini()
    nilai = parse_nominal(a.nilai, label="--nilai")
    akun = bersih_akun(a.akun or "Aset:Persediaan")
    s = saldo_per(j, per)
    kini = sum((v for x, v in s.items() if x == akun or x.startswith(akun + ":")), NOL)
    beda = nilai - kini
    b = ["PENYESUAIAN PERSEDIAAN per " + teks_tanggal(per),
         "Nilai stok hasil hitung: " + rp(nilai),
         "Nilai {} di catatan: {}".format(akun, rp(kini))]
    if beda == 0:
        b.append("Sudah sama. Tidak ada yang perlu dicatat.")
        print("\n".join(b))
        return 0
    r = Rencana(per, "Penyesuaian persediaan (hitung stok)", [(akun, beda), ("HPP:Penyesuaian Persediaan", -beda)],
                {}, "")
    baru = periksa_akun(j, [r], a.akun_baru)
    tx = teks_transaksi(r.tanggal, r.ket, r.tags, r.postings)
    b += ["", tx, "",
          "Artinya: stok {} {}; HPP bulan ini {} sebesar itu (barang {}).".format(
              "naik" if beda > 0 else "turun", rp(abs(beda)), "berkurang" if beda > 0 else "bertambah",
              "yang dibeli belum terjual" if beda > 0 else "terjual/terpakai/rusak lebih banyak dari stok baru")]
    if not a.ya:
        b.append("Simpan? Setelah pengguna menjawab ya, ulangi dengan --ya.")
        print("\n".join(b))
        return 0
    tulis_jurnal(a, j.path, ("\n".join("account " + x for x in baru) + "\n\n" if baru else "") + tx)
    b.append("TERSIMPAN ke " + j.path)
    print("\n".join(b))
    return 0


# ============================================================ impor mutasi bank

KATA_KOLOM = {
    "tanggal": ["tanggal transaksi", "tgl transaksi", "transaction date", "tanggal", "tgl", "date", "post date",
                "posting date", "tanggal posting", "value date", "trx date"],
    "keterangan": ["keterangan", "deskripsi", "description", "uraian", "remark", "remarks", "narasi", "berita",
                   "detail transaksi", "transaksi", "details", "memo"],
    "masuk": ["kredit", "credit", "mutasi kredit", "uang masuk", "masuk", "setoran", "cr"],
    "keluar": ["debet", "debit", "mutasi debet", "mutasi debit", "uang keluar", "keluar", "penarikan", "db"],
    "nominal": ["jumlah", "nominal", "amount", "mutasi", "nilai", "jumlah (idr)"],
    "dk": ["d/k", "db/cr", "cr/db", "dk", "d/c", "k/d", "jenis", "tipe", "type", "debit/credit"],
    "saldo": ["saldo", "balance", "saldo akhir", "running balance"],
}


def cocok_kolom(sel, daftar):
    s = (sel or "").strip().lower().strip("\"' ")
    if not s:
        return 0
    if s in daftar:
        return 2
    if any(len(k) > 3 and k in s for k in daftar):
        return 1
    return 0


def angka_bank(teks, desimal=None):
    """'1,500,000.00 CR' | '1.500.000,00' | '(25.000)' -> (Decimal|None, 'CR'|'DB'|None)."""
    if teks is None:
        return None, None
    s = str(teks).strip().upper().replace(" ", " ")
    if not s or s in ("-", "0-"):
        return None, None
    dk = None
    m = re.search(r"\s*\b(CR|DB|KR|DR|K|D|C)\b\.?\s*$", s)
    if m:
        dk = "CR" if m.group(1) in ("CR", "KR", "K", "C") else "DB"
        s = s[:m.start()]
    neg = s.strip().startswith("-") or (s.strip().startswith("(") and s.strip().endswith(")"))
    s = re.sub(r"\b(RP|IDR)\b\.?", "", s)
    s = re.sub(r"[,.]\s*-\s*$", "", s)
    s = re.sub(r"[^\d,.]", "", s).strip(".,")
    if not s:
        return None, None
    if desimal == "koma":
        s = s.replace(".", "").replace(",", ".")
    elif desimal == "titik":
        s = s.replace(",", "")
    elif "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".") if s.rfind(",") > s.rfind(".") else s.replace(",", "")
    elif "," in s:
        bag = s.split(",")
        s = s.replace(",", ".") if (len(bag) == 2 and len(bag[1]) != 3) else s.replace(",", "")
    elif "." in s:
        bag = s.split(".")
        if len(bag) > 2 or len(bag[1]) == 3:
            s = s.replace(".", "")
    try:
        v = Decimal(s)
    except InvalidOperation:
        return None, None
    return (-v if neg else v), dk


def baca_mutasi(a, path):
    teks = baca_file(path)
    if not teks.strip():
        raise Gagal("File mutasi {} kosong.".format(path))
    baris = [x for x in teks.splitlines()[:60] if x.strip()]
    skor = {}
    for sep in (",", ";", "\t", "|"):
        hit = [len(next(csv.reader([x], delimiter=sep))) for x in baris]
        skor[sep] = (len([h for h in hit if h >= 3]), max(hit) if hit else 0)
    sep = max(skor, key=lambda k: skor[k])
    semua = list(csv.reader(io.StringIO(teks), delimiter=sep))
    idx = None
    if a.baris_judul:
        idx = a.baris_judul - 1
        if not 0 <= idx < len(semua):
            raise Gagal("--baris-judul di luar isi file.")
    else:
        for i, row in enumerate(semua[:60]):
            ada_tgl = any(cocok_kolom(c, KATA_KOLOM["tanggal"]) for c in row)
            sk = sum(1 for c in row if any(cocok_kolom(c, d) for d in KATA_KOLOM.values()))
            if ada_tgl and sk >= 3:
                idx = i
                break
    if idx is None:
        raise Gagal("Baris judul kolom (Tanggal, Keterangan, ...) tidak ditemukan. Sebutkan --baris-judul <nomor>. "
                    "5 baris pertama: " + " / ".join(",".join(r) for r in semua[:5]))
    judul = [h.strip().strip("'\"") or "kolom_{}".format(i + 1) for i, h in enumerate(semua[idx])]
    peta, terpakai = {}, set()
    paksa = {"tanggal": a.kolom_tanggal, "keterangan": a.kolom_keterangan, "masuk": a.kolom_masuk,
             "keluar": a.kolom_keluar, "nominal": a.kolom_nominal, "dk": a.kolom_dk, "saldo": a.kolom_saldo}
    for k, v in paksa.items():
        if v:
            if v not in judul:
                raise Gagal("Kolom '{}' tidak ada. Kolom yang ada: {}".format(v, ", ".join(judul)))
            peta[k] = judul.index(v)
            terpakai.add(peta[k])
    for k in ("tanggal", "keterangan", "saldo", "masuk", "keluar", "nominal", "dk"):
        if k in peta:
            continue
        terbaik, sk = None, 0
        for i, h in enumerate(judul):
            if i in terpakai:
                continue
            if k in ("masuk", "keluar", "nominal") and re.search(r"saldo|balance", h, re.I):
                continue
            s = cocok_kolom(h, KATA_KOLOM[k])
            if s > sk:
                terbaik, sk = i, s
        if terbaik is not None:
            peta[k] = terbaik
            terpakai.add(terbaik)
    if "tanggal" not in peta or "keterangan" not in peta:
        raise Gagal("Kolom tanggal/keterangan tidak terdeteksi. Kolom: {}. Pakai --kolom-tanggal dan "
                    "--kolom-keterangan.".format(", ".join(judul)))
    if not (("masuk" in peta and "keluar" in peta) or "nominal" in peta):
        raise Gagal("Kolom nominal tidak terdeteksi. Kolom: {}. Pakai --kolom-masuk & --kolom-keluar, atau "
                    "--kolom-nominal (+ --kolom-dk).".format(", ".join(judul)))
    tahun = a.tahun
    hasil, lewati = [], []
    for no, row in enumerate(semua[idx + 1:], start=idx + 2):
        if not any(c.strip() for c in row):
            continue

        def kol(k):
            i = peta.get(k)
            return row[i].strip() if i is not None and i < len(row) else ""

        t_mentah = kol("tanggal").strip("'\" ")
        if not t_mentah or t_mentah.upper().startswith("PEND"):
            lewati.append((no, "tanggal kosong/pending: " + ",".join(row)[:60]))
            continue
        try:
            tgl = parse_tanggal(t_mentah, tahun_default=tahun)
            if re.match(r"^\d{1,2}[-/.]\d{1,2}$", t_mentah) and not tahun:
                raise Gagal("tanpa tahun")
        except Gagal as g:
            if "tanpa tahun" in str(g):
                raise Gagal("Tanggal di mutasi tanpa tahun (mis. '{}'). Sebutkan --tahun 2026.".format(t_mentah))
            lewati.append((no, "tanggal tidak dikenali: " + t_mentah))
            continue
        masuk = keluar = NOL
        if "masuk" in peta and "keluar" in peta:
            m1, _ = angka_bank(kol("masuk"), a.desimal)
            k1, _ = angka_bank(kol("keluar"), a.desimal)
            masuk, keluar = abs(m1 or NOL), abs(k1 or NOL)
        else:
            v, dk = angka_bank(kol("nominal"), a.desimal)
            if v is None:
                lewati.append((no, "nominal kosong/rusak: " + kol("nominal")))
                continue
            penanda = kol("dk").upper() if "dk" in peta else ""
            if penanda in ("CR", "C", "K", "KR", "KREDIT", "CREDIT", "MASUK", "+"):
                dk = "CR"
            elif penanda in ("DB", "D", "DR", "DEBET", "DEBIT", "KELUAR", "-"):
                dk = "DB"
            if dk is None:
                dk = "DB" if v < 0 else None
            if dk is None:
                raise Gagal("Kolom nominal tanpa penanda masuk/keluar (CR/DB) di baris {}. Sebutkan --kolom-dk "
                            "atau --kolom-masuk/--kolom-keluar.".format(no))
            masuk, keluar = (abs(v), NOL) if dk == "CR" else (NOL, abs(v))
        if masuk and keluar:
            lewati.append((no, "masuk dan keluar sekaligus terisi"))
            continue
        if not masuk and not keluar:
            lewati.append((no, "nominal 0/kosong"))
            continue
        for v in (masuk, keluar):
            if v != v.quantize(SEN) or v > MAKS_NOMINAL:
                raise Gagal("Baris {}: nominal {} tidak wajar. Periksa format angka (--desimal koma/titik)."
                            .format(no, v))
        saldo = angka_bank(kol("saldo"), a.desimal)[0] if "saldo" in peta and kol("saldo") else None
        hasil.append({"no": no, "tanggal": tgl, "ket": bersih_ket(kol("keterangan")) or "(tanpa keterangan)",
                      "masuk": masuk, "keluar": keluar, "saldo": saldo})
    if not hasil:
        raise Gagal("Tidak ada baris transaksi yang terbaca dari {}.".format(path))
    return hasil, lewati, [judul[i] for i in sorted(peta.values())]


def cek_urutan_saldo(rows):
    """Cari urutan (file / terbalik) yang membuat kolom saldo konsisten. Kembalikan (saldo_awal, saldo_akhir, ok)."""
    if not rows or any(r["saldo"] is None for r in rows):
        return None
    for urutan in (rows, list(reversed(rows))):
        jalan = NOL
        awal = set()
        for r in urutan:
            jalan += r["masuk"] - r["keluar"]
            awal.add(r["saldo"] - jalan)
        if len(awal) == 1:
            s_awal = awal.pop()
            return s_awal, s_awal + jalan, True
    return None, None, False


# ---- aturan (.rules) : subset yang dibaca pembaca bawaan
def baca_aturan(path):
    """Kembalikan daftar blok: {'syarat': [[(field|None, regex)]...(OR of AND)], 'akun': str}."""
    blok, kini = [], None
    try:
        with open(path, encoding="utf-8") as f:
            isi = f.read().splitlines()
    except OSError as e:
        raise Gagal("File aturan {} tidak bisa dibuka: {}".format(path, e), K_FILE)
    for no, raw in enumerate(isi, 1):
        s = raw.rstrip()
        if not s.strip() or s.lstrip().startswith(("#", ";")):
            if not s.strip():
                kini = None
            continue
        if s.startswith("if"):
            sisa = s[2:].strip()
            kini = {"syarat": [], "akun": None, "baris": no}
            if sisa:
                kini["syarat"].append([matcher(sisa, no)])
            blok.append(kini)
        elif kini is not None and s.startswith("&"):
            if not kini["syarat"]:
                raise Gagal("aturan baris {}: '&' tanpa syarat sebelumnya.".format(no))
            kini["syarat"][-1].append(matcher(s[1:].strip(), no))
        elif kini is not None and s[0] in " \t":
            t = s.strip()
            if t.startswith("account2 "):
                kini["akun"] = bersih_akun(t[len("account2 "):])
            else:
                raise Gagal("aturan baris {}: hanya 'account2 <akun>' yang didukung pembaca bawaan ('{}').".format(
                    no, t))
        elif kini is not None and kini["akun"] is None:
            kini["syarat"].append([matcher(s.strip(), no)])
        else:
            raise Gagal("aturan baris {}: '{}' belum didukung pembaca bawaan. Pasang hledger atau hapus baris itu."
                        .format(no, s.strip()))
    return blok


def matcher(teks, no):
    m = re.match(r"^%(\w+)\s+(.+)$", teks)
    field, pola = (m.group(1), m.group(2)) if m else (None, teks)
    if field and field not in ("keterangan", "masuk", "keluar", "tanggal", "saldo", "ref"):
        raise Gagal("aturan baris {}: kolom %{} tidak dikenal.".format(no, field))
    try:
        rx = re.compile(pola.strip(), re.I)
    except re.error:
        raise Gagal("aturan baris {}: pola '{}' rusak.".format(no, pola))
    return field, rx


def nilai_csv(r):
    return {"tanggal": r["tanggal"].isoformat(), "keterangan": r["ket"],
            "masuk": angka_polos(r["masuk"]) if r["masuk"] else "",
            "keluar": angka_polos(r["keluar"]) if r["keluar"] else "",
            "saldo": angka_polos(r["saldo"]) if r["saldo"] is not None else "", "ref": r["ref"]}


def angka_polos(v):
    v = Decimal(v)
    return str(v.to_integral_value()) if v == v.to_integral_value() else str(v.quantize(SEN))


def kelompokkan(blok, r):
    nilai = nilai_csv(r)
    rekaman = ",".join(nilai[k] for k in ("tanggal", "keterangan", "masuk", "keluar", "saldo", "ref"))
    akun = None
    for b in blok:
        for grup in b["syarat"]:
            if all(rx.search(nilai[f] if f else rekaman) for f, rx in grup):
                akun = b["akun"] or akun
                break
    return akun


def slug(teks):
    return re.sub(r"[^a-z0-9]+", "-", teks.lower()).strip("-")[:40] or "bank"


def aturan_path(a, j):
    return os.path.abspath(os.path.expanduser(a.aturan)) if getattr(a, "aturan", None) else \
        os.path.join(os.path.dirname(j.path), "aturan-bank.rules")


def teks_rules_kepala(akun_bank_, path_kategori):
    return "\n".join([
        "# Dibuat otomatis oleh hledger-usaha untuk file mutasi yang sudah dirapikan.",
        "skip 1",
        "fields tanggal, keterangan, masuk, keluar, saldo, ref",
        "date %tanggal",
        "date-format %Y-%m-%d",
        "description %keterangan",
        "currency Rp",
        "account1 " + akun_bank_,
        "amount-in %masuk",
        "amount-out %keluar",
        "comment ref:%ref",
        "include " + path_kategori.replace("\\", "/"),
        ""])


def cmd_impor_bank(a):
    j = muat_jurnal(a)
    ak_bank = akun_bank(j, a.bank)
    if j.gol(ak_bank) != "kas" and not ak_bank.startswith("Aset:Bank"):
        raise Gagal("--bank harus rekening di bawah Aset:Bank, mis. Aset:Bank:BCA.")
    p_aturan = aturan_path(a, j)
    if not os.path.isfile(p_aturan):
        raise Gagal("File aturan {} tidak ada. Jalankan `init` (membuatnya otomatis) atau salin "
                    "templates/aturan-bank.rules ke folder jurnal.".format(p_aturan), K_FILE)
    rows, lewati, kolom = baca_mutasi(a, a.file)
    # ref stabil: akun|tanggal|ket|masuk|keluar|saldo|kemunculan ke-n
    hitung = {}
    for r in rows:
        kunci = "|".join([ak_bank, r["tanggal"].isoformat(), r["ket"], angka_polos(r["masuk"]),
                          angka_polos(r["keluar"]), angka_polos(r["saldo"]) if r["saldo"] is not None else ""])
        hitung[kunci] = hitung.get(kunci, 0) + 1
        r["ref"] = hashlib.sha1("{}|{}".format(kunci, hitung[kunci]).encode("utf-8")).hexdigest()[:12]
    blok = baca_aturan(p_aturan)
    tetap = {}
    for item in a.tetapkan or []:
        m = re.match(r"^(\d+)=(.+)$", item.strip())
        if not m:
            raise Gagal("--tetapkan harus 'BARIS=Akun', mis. --tetapkan \"12=Beban:Transportasi\".")
        tetap[int(m.group(1))] = bersih_akun(m.group(2))
    nomor_ada = {r["no"] for r in rows}
    for n in tetap:
        if n not in nomor_ada:
            raise Gagal("--tetapkan: baris {} tidak ada di file mutasi.".format(n))
    for r in rows:
        r["akun2"] = tetap.get(r["no"]) or kelompokkan(blok, r) or (
            "Pendapatan:Belum Dikelompokkan" if r["masuk"] else "Beban:Belum Dikelompokkan")
        if r["akun2"] == ak_bank:
            raise Gagal("Baris {}: akun lawan sama dengan rekening bank.".format(r["no"]))
    sudah = set(re.findall(r"\bref:([0-9a-f]{12})\b", baca_file(j.path)))
    baru = [r for r in rows if r["ref"] not in sudah]
    dobel = len(rows) - len(baru)

    # uji silang dengan hledger (aturan yang sama)
    hl = cari_hledger(a) if a.mesin != "bawaan" else None
    silang = None
    with tempfile.TemporaryDirectory() as tmp:
        p_norm = os.path.join(tmp, "mutasi.csv")
        tulis_norm(p_norm, rows)
        if hl:
            p_rules = os.path.join(tmp, "mutasi.csv.rules")
            with open(p_rules, "w", encoding="utf-8") as f:
                f.write(teks_rules_kepala(ak_bank, p_aturan))
            kode, out, err = jalankan_hledger(hl, ["-f", p_norm, "--rules-file", p_rules, "print", "-O", "json"])
            if kode != 0:
                raise Gagal("hledger menolak file aturan:\n" + ringkas_galat(err), K_HLEDGER)
            dari_hl = {}
            for t in json.loads(out):
                ref = dict(t.get("ttags") or []).get("ref")
                for p in t["tpostings"]:
                    if p["paccount"] != ak_bank:
                        dari_hl[ref] = p["paccount"]
            beda = [r for r in rows if r["no"] not in tetap and dari_hl.get(r["ref"]) != r["akun2"]]
            silang = "COCOK ({} baris)".format(len(rows)) if not beda else "BEDA di baris {}".format(
                ", ".join(str(r["no"]) for r in beda[:10]))
        simpan_norm = None
        if a.ya and baru:
            folder = os.path.join(os.path.dirname(j.path), "impor")
            os.makedirs(folder, exist_ok=True)
            simpan_norm = os.path.join(folder, "{}-{}-{}.csv".format(slug(ak_bank.split(":")[-1]),
                                                                      min(r["tanggal"] for r in rows).isoformat(),
                                                                      max(r["tanggal"] for r in rows).isoformat()))
            shutil.copyfile(p_norm, simpan_norm)
    if silang and silang.startswith("BEDA"):
        raise Gagal("Pengelompokan pembaca bawaan BEDA dengan hledger ({}). Tidak ada yang disimpan; laporkan ke "
                    "dukungan Komunitech.".format(silang), K_HLEDGER)

    b = ["IMPOR MUTASI BANK" + ("" if a.ya else " (PRATINJAU, belum disimpan)"),
         "File: {} -> rekening {}".format(os.path.basename(a.file), ak_bank),
         "Kolom terbaca: " + ", ".join(kolom),
         "Terbaca {} transaksi ({} s.d. {}); {} sudah pernah diimpor (dilewati); {} baru.".format(
             len(rows), min(r["tanggal"] for r in rows).isoformat(), max(r["tanggal"] for r in rows).isoformat(),
             dobel, len(baru))]
    tm = sum((r["masuk"] for r in baru), NOL)
    tk = sum((r["keluar"] for r in baru), NOL)
    b.append("Uang masuk {} | uang keluar {}".format(rp(tm), rp(tk)))
    if silang:
        b.append("Uji silang aturan dengan hledger: " + silang)
    if lewati:
        b.append("Baris dilewati: " + "; ".join("baris {} ({})".format(n, s) for n, s in lewati[:8]))
    ringkas = {}
    for r in baru:
        ringkas.setdefault(r["akun2"], [0, NOL])
        ringkas[r["akun2"]][0] += 1
        ringkas[r["akun2"]][1] += r["masuk"] - r["keluar"]
    if ringkas:
        b += ["", "RINGKASAN PER AKUN"]
        for ak, (n, v) in sorted(ringkas.items(), key=lambda x: -abs(x[1][1])):
            b.append("- {}: {} transaksi, {} {}".format(ak, n, "masuk" if v >= 0 else "keluar", rp(abs(v))))
    bd = [r for r in baru if "Belum Dikelompokkan" in r["akun2"]]
    if bd:
        b += ["", "PERLU DITANYAKAN KE PENGGUNA ({} transaksi belum dikelompokkan):".format(len(bd))]
        for r in bd[:25]:
            b.append("- baris {}: {} {} {}".format(r["no"], r["tanggal"].isoformat(), r["ket"],
                                                   ("masuk " + rp(r["masuk"])) if r["masuk"] else
                                                   ("keluar " + rp(r["keluar"]))))
        if len(bd) > 25:
            b.append("- ... dan {} lainnya".format(len(bd) - 25))
        b.append("Tetapkan dengan --tetapkan \"BARIS=Akun\", atau simpan kata kuncinya untuk bulan depan dengan "
                 "perintah tambah-aturan.")
    # cek saldo bank
    cs = cek_urutan_saldo(rows)
    if cs is not None:
        s_awal, s_akhir, ok = cs
        if not ok:
            b.append("PERINGATAN: kolom saldo di file tidak konsisten dengan mutasinya (ada baris hilang/terpotong?).")
        else:
            sebelum = sum((v for x, v in saldo_per(j, min(r["tanggal"] for r in rows) - dt.timedelta(days=1)).items()
                           if x == ak_bank), NOL)
            b.append("")
            b.append("Cek saldo: saldo bank sebelum transaksi pertama {}; saldo {} di catatan sebelum tanggal itu {}."
                     .format(rp(s_awal), ak_bank, rp(sebelum)))
            if sebelum == s_awal:
                b.append("COCOK. Setelah impor, saldo catatan akan sama dengan saldo akhir bank {}.".format(rp(s_akhir)))
            elif sebelum == 0 and not dobel:
                b.append("Saldo awal rekening belum dicatat. Catat dulu: catat --jenis saldo-awal --tanggal {} "
                         "--posting \"{}={}\"".format((min(r["tanggal"] for r in rows) - dt.timedelta(days=1))
                                                      .isoformat(), ak_bank, angka_polos(s_awal)))
            else:
                b.append("SELISIH {}: periksa transaksi bank sebelum periode ini yang belum/dobel dicatat.".format(
                    rp(sebelum - s_awal)))
    if not baru:
        b.append("Tidak ada transaksi baru untuk disimpan.")
        print("\n".join(b))
        return 0
    teks = []
    akun_baru = [x for x in sorted({ak_bank} | {r["akun2"] for r in baru}) if x not in j.akun_dikenal()]
    for x in akun_baru:
        if x.split(":")[0] not in {y.split(":")[0] for y in j.akun_dikenal()}:
            raise Gagal("Akun '{}' (dari aturan/--tetapkan) tidak berada di bawah akun utama yang ada.".format(x))
    if akun_baru:
        teks.append("\n".join("account " + x for x in akun_baru))
        b.append("Akun baru yang akan dibuat: " + ", ".join(akun_baru))
    for r in sorted(baru, key=lambda x: (x["tanggal"], x["no"])):
        v = r["masuk"] - r["keluar"]
        teks.append(teks_transaksi(r["tanggal"], r["ket"], {"ref": r["ref"], "sumber": "mutasi-bank"},
                                   [(ak_bank, v), (r["akun2"], -v)]))
    if not a.ya:
        b += ["", "Contoh 2 transaksi pertama:"] + teks[1 if akun_baru else 0:][:2]
        b.append("")
        b.append("Simpan {} transaksi? Setelah pengguna menjawab ya, ulangi perintah yang sama dengan --ya.".format(
            len(baru)))
        print("\n".join(b))
        return 0
    tulis_jurnal(a, j.path, "\n\n".join(teks))
    b[0] = "IMPOR MUTASI BANK: TERSIMPAN"
    b.append("Tersimpan {} transaksi ke {}. Salinan mutasi rapi: {}".format(len(baru), j.path, simpan_norm))
    print("\n".join(b))
    return 0


def tulis_norm(path, rows):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["tanggal", "keterangan", "masuk", "keluar", "saldo", "ref"])
        for r in rows:
            n = nilai_csv(r)
            w.writerow([n[k] for k in ("tanggal", "keterangan", "masuk", "keluar", "saldo", "ref")])


def escape_regex(teks):
    return re.sub(r"([.^$*+?()\[\]{}|\\])", r"\\\1", teks)


def cmd_tambah_aturan(a):
    j = muat_jurnal(a)
    p = aturan_path(a, j)
    if not os.path.isfile(p):
        raise Gagal("File aturan {} tidak ada.".format(p), K_FILE)
    kata = [k.strip() for k in a.kata if k.strip()]
    if not kata or any(len(k) < 3 for k in kata):
        raise Gagal("--kata minimal 3 huruf (kata terlalu pendek akan cocok ke mana-mana).")
    akun = bersih_akun(a.akun)
    if akun not in j.akun_dikenal():
        mirip = difflib.get_close_matches(akun, sorted(j.akun_dikenal()), n=3, cutoff=0.6)
        raise Gagal("Akun '{}' belum ada di jurnal.{}".format(akun, " Mungkin: " + ", ".join(mirip) if mirip else ""))
    arah = {"masuk": "%masuk [1-9]", "keluar": "%keluar [1-9]"}.get(a.arah)
    blok = "\n# ditambahkan {} lewat tambah-aturan\nif %keterangan {}\n{} account2 {}\n".format(
        hari_ini().isoformat(), "|".join(escape_regex(k) for k in kata), ("& " + arah + "\n") if arah else "", akun)
    print("ATURAN BARU untuk {}:".format(p))
    print(blok)
    if not a.ya:
        print("Simpan? Setelah pengguna menjawab ya, ulangi dengan --ya.")
        return 0
    with open(p, "a", encoding="utf-8") as f:
        f.write(blok)
    baca_aturan(p)
    print("TERSIMPAN. Aturan paling bawah menang bila beberapa aturan cocok.")
    return 0


# ============================================================ ekspor ke laporan-keuangan-emkm

def kode_emkm(j, akun, masuk):
    a = akun.lower()
    g = j.gol(akun)
    if "belum dikelompokkan" in a:
        return ""
    if g == "pendapatan":
        return "pendapatan_lain" if re.search(r"lain|bunga", a) else "pendapatan_usaha"
    if g == "hpp":
        return "pembelian_bahan"
    if g == "beban":
        peta = [("gaji|upah|thr", "beban_gaji"), ("sewa", "beban_sewa"),
                ("listrik|air|internet|telepon|pulsa|gas", "beban_utilitas"),
                ("transport|bensin|ongkir|kirim", "beban_transportasi"), ("pemasaran|iklan|promosi", "beban_pemasaran"),
                ("perlengkapan|kemasan|atk", "beban_perlengkapan"), ("perawatan|servis|perbaikan", "beban_perawatan"),
                ("bunga|admin bank|biaya bank", "beban_keuangan"), ("pajak penghasilan|pph", "beban_pajak_penghasilan"),
                ("pajak", "beban_pajak_lain"), ("komisi|admin marketplace|biaya layanan", "beban_admin_penjualan")]
        for pola, kode in peta:
            if re.search(pola, a.split(":", 1)[-1]):
                return kode
        return "beban_lain"
    if g == "aset":
        if "persediaan" in a or "stok" in a:
            return "pembelian_bahan" if not masuk else ""
        if "piutang" in a:
            return "terima_piutang" if masuk else "piutang_lain"
        if "kasbon" in a:
            return "piutang_lain"
        return "penjualan_aset" if masuk else "aset_tetap"
    if g == "utang":
        if re.search(r"pajak", a):
            return "titipan_pajak"
        if re.search(r"usaha|dagang|pemasok|supplier", a):
            return "bayar_utang_usaha" if not masuk else ""
        return "pinjaman_diterima" if masuk else "bayar_pinjaman"
    if g == "modal":
        if "prive" in a:
            return "prive" if not masuk else "setoran_modal"
        return "setoran_modal" if masuk else "prive"
    return ""


def cmd_ekspor_emkm(a):
    j = muat_jurnal(a)
    d1, d2 = periode_dari_arg(a)
    sebelum = d1 - dt.timedelta(days=1)
    baris = []
    kosong = 0
    for t in j.txns:
        if not d1 <= t.tanggal <= d2:
            continue
        _, alok = alokasi_kas(j, t)
        for akun, nilai in alok:
            masuk = nilai > 0
            kode = kode_emkm(j, akun, masuk) if akun != "(tanpa akun lawan)" else ""
            kosong += not kode
            ket = t.ket + ("" if len(alok) == 1 else " ({})".format(akun.split(":")[-1]))
            baris.append([t.tanggal.strftime("%d/%m/%Y"), ket, angka_polos(nilai) if masuk else "",
                          "" if masuk else angka_polos(-nilai), kode])
    if not baris:
        raise Gagal("Tidak ada transaksi kas/bank pada {}.".format(teks_periode(d1, d2)))
    keluar = a.keluar or os.path.join(os.path.dirname(j.path), "ekspor",
                                      "buku-kas-{}-{}.csv".format(d1.isoformat(), d2.isoformat()))
    keluar = os.path.abspath(os.path.expanduser(keluar))
    if os.path.exists(keluar) and not a.timpa:
        raise Gagal("File {} sudah ada. Pakai --timpa untuk menimpa atau --keluar nama lain.".format(keluar))
    os.makedirs(os.path.dirname(keluar), exist_ok=True)
    with open(keluar, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["Tanggal", "Keterangan", "Masuk", "Keluar", "Kategori"])
        w.writerows(baris)

    def total(pred, per):
        return sum((v for x, v in saldo_per(j, per).items() if pred(x)), NOL)

    kas = lambda x: j.gol(x) == "kas"
    piut = lambda x: j.gol(x) == "aset" and "piutang" in x.lower() and "kasbon" not in x.lower()
    pers = lambda x: j.gol(x) == "aset" and ("persediaan" in x.lower() or "stok" in x.lower())
    tetap = lambda x: j.gol(x) == "aset" and golongan_arus(j, x) == "investasi"
    utu = lambda x: j.gol(x) == "utang" and re.search(r"usaha|dagang|pemasok|supplier", x.lower()) is not None
    utb = lambda x: j.gol(x) == "utang" and golongan_arus(j, x) == "pendanaan"
    nilai = {
        "kas-awal": total(kas, sebelum), "piutang-awal": total(piut, sebelum), "piutang-akhir": total(piut, d2),
        "persediaan-awal": total(pers, sebelum), "persediaan-akhir": total(pers, d2),
        "aset-tetap-awal": total(tetap, sebelum), "utang-usaha-awal": -total(utu, sebelum),
        "utang-usaha-akhir": -total(utu, d2), "utang-bank-awal": -total(utb, sebelum),
    }
    perintah = ["python3 <folder laporan-keuangan-emkm>/scripts/laporan_emkm.py \"{}\"".format(keluar),
                "  --nama-usaha \"{}\"".format(j.nama_usaha or "[Nama Usaha]"),
                "  --periode-awal {} --periode-akhir {}".format(d1.isoformat(), d2.isoformat())]
    perintah += ["  --{} {}".format(k, angka_polos(v)) for k, v in nilai.items()]
    b = ["EKSPOR BUKU KAS UNTUK LAPORAN SAK EMKM", "Periode: " + teks_periode(d1, d2),
         "File: " + keluar, "{} baris (uang masuk/keluar kas & bank; pindah dana sendiri tidak ikut).".format(len(baris))]
    if kosong:
        b.append("{} baris tanpa Kategori (akun 'Belum Dikelompokkan'/tak dikenal): skill laporan-keuangan-emkm akan "
                 "menanyakannya.".format(kosong))
    b += ["", "Saldo dari jurnal untuk dipakai laporan-keuangan-emkm:"]
    b += ["- {}: {}".format(k, rp(v)) for k, v in nilai.items()]
    b += ["", "Perintah (jalankan dengan skill laporan-keuangan-emkm):"] + perintah
    b += ["", "Catatan: penjualan/pembelian tempo tercermin lewat saldo piutang/utang awal-akhir; aset tetap butuh "
          "--umur-aset-tahun bila ingin penyusutan."]
    b += kaki(j)
    cetak(a, b, {"file": keluar, "baris": len(baris), "tanpa_kategori": kosong, "saldo": nilai,
                 "perintah": " \\\n".join(perintah)})
    return 0


# ============================================================ init, cek, backup

def cmd_init(a):
    path = path_jurnal(a)
    if os.path.exists(path):
        raise Gagal("File {} sudah ada. Skill tidak menimpa pembukuan yang sudah ada. Pakai --jurnal lain bila "
                    "ingin membuat buku baru.".format(path))
    nama = bersih_ket(a.nama or "") or "[Nama Usaha]"
    try:
        with open(TEMPLATE_JURNAL, encoding="utf-8") as f:
            isi = f.read()
    except OSError:
        raise Gagal("Template {} tidak ditemukan (folder skill tidak lengkap).".format(TEMPLATE_JURNAL), K_FILE)
    isi = isi.replace("{{NAMA_USAHA}}", nama).replace("{{TANGGAL}}", hari_ini().isoformat())
    bank = [bersih_segmen(x, "--bank") for x in (a.bank or [])]
    if bank:
        isi = isi.rstrip("\n") + "\n\n; Rekening bank usaha\n" + "".join(
            "account Aset:Bank:{}\n".format(x) for x in bank)
    folder = os.path.dirname(path)
    os.makedirs(folder, exist_ok=True)
    for sub in ("impor", "backup", "ekspor"):
        os.makedirs(os.path.join(folder, sub), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(isi)
    p_aturan = os.path.join(folder, "aturan-bank.rules")
    dibuat_aturan = False
    if not os.path.exists(p_aturan):
        shutil.copyfile(TEMPLATE_ATURAN, p_aturan)
        dibuat_aturan = True
    j = muat_jurnal(a)
    print("\n".join([
        "BUKU BARU DIBUAT",
        "File jurnal: " + path,
        "Aturan mutasi bank: " + p_aturan + (" (baru)" if dibuat_aturan else " (sudah ada, tidak diubah)"),
        "Folder: impor/, ekspor/, backup/",
        "Akun siap pakai: Kas, Bank{}, Piutang Usaha, Persediaan, Peralatan, Utang Usaha, Utang Bank, Modal, Prive, "
        "Pendapatan, HPP, Beban.".format(" (" + ", ".join(bank) + ")" if bank else ""),
        "Diperiksa dengan: " + teks_mesin(j),
        "",
        "Langkah berikut: catat saldo awal (uang di laci, saldo rekening, stok, piutang, utang) dengan "
        "`catat --jenis saldo-awal`.",
        "Agar hledger langsung memakai file ini, atur variabel LEDGER_FILE (lihat docs/panduan-hledger.md)."]))
    return 0


def cmd_cek(a):
    hl = None
    b = ["CEK HLEDGER-USAHA (skill v{})".format(VERSI)]
    try:
        hl = cari_hledger(a)
    except Gagal as e:
        b.append(str(e))
    if hl:
        v = versi_hledger(hl)
        b.append("hledger: terpasang, versi {} ({})".format(v, "sudah diuji Komunitech" if v in HLEDGER_TERUJI else
                                                          "belum diuji Komunitech; tetap bisa dipakai"))
    else:
        b.append("hledger: TIDAK ditemukan. Skill tetap bisa mencatat & membuat laporan dengan pembaca bawaan. "
                 "Pasang hledger (gratis) lewat docs/panduan-hledger.md untuk pemeriksaan lengkap & hledger-web.")
    path = path_jurnal(a)
    if not os.path.exists(path):
        b.append("File jurnal: BELUM ADA ({}). Buat dengan: init --nama \"Nama Usaha\"".format(path))
        print("\n".join(b))
        return K_FILE
    j = muat_jurnal(a)
    if j.txns:
        b.append("File jurnal: {} ({} transaksi, {} s.d. {})".format(path, len(j.txns), j.txns[0].tanggal.isoformat(),
                                                                     j.txns[-1].tanggal.isoformat()))
    else:
        b.append("File jurnal: {} (belum ada transaksi)".format(path))
    kode_akhir = 0
    if hl:
        kode, _, err = jalankan_hledger(hl, ["-f", path, "check", "accounts"])
        b.append("Pemeriksaan hledger (seimbang, saldo, akun terdaftar): " + ("LULUS" if kode == 0 else
                 "ADA MASALAH:\n" + ringkas_galat(err)))
        kode_akhir = 0 if kode == 0 else K_JURNAL
    else:
        tanpa = sorted(x for x in j.akun_dikenal() if x not in j.deklarasi)
        b.append("Pemeriksaan bawaan: seimbang & saldo LULUS" + (
            "; akun belum terdaftar: " + ", ".join(tanpa) if tanpa else "; semua akun terdaftar"))
    tanpa_gol = sorted(x for x in j.akun_dikenal() if j.gol(x) is None)
    if tanpa_gol:
        b.append("Akun tanpa golongan (tidak masuk laporan dengan benar): " + ", ".join(tanpa_gol))
        kode_akhir = kode_akhir or K_JURNAL
    if j.txns:
        bd = belum_dikelompokkan(j, j.txns[0].tanggal, j.txns[-1].tanggal)
        if bd:
            b.append("Perlu dicek: {} transaksi masih 'Belum Dikelompokkan'.".format(len(bd)))
    for c in j.catatan:
        if not c.startswith("hledger belum terpasang"):
            b.append(c)
    print("\n".join(b))
    return kode_akhir


def cmd_backup(a):
    path = path_jurnal(a)
    baca_file(path)
    j = muat_jurnal(a)
    folder = os.path.abspath(os.path.expanduser(a.ke)) if a.ke else os.path.join(os.path.dirname(path), "backup")
    os.makedirs(folder, exist_ok=True)
    cap = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    hasil = []
    sumber = [path]
    p_aturan = os.path.join(os.path.dirname(path), "aturan-bank.rules")
    if os.path.isfile(p_aturan):
        sumber.append(p_aturan)
    for s in sumber:
        nama, ext = os.path.splitext(os.path.basename(s))
        tujuan = os.path.join(folder, "{}-{}{}".format(nama, cap, ext))
        shutil.copyfile(s, tujuan)
        with open(s, "rb") as f1, open(tujuan, "rb") as f2:
            if hashlib.sha256(f1.read()).hexdigest() != hashlib.sha256(f2.read()).hexdigest():
                raise Gagal("Salinan {} tidak sama dengan aslinya. Coba lagi / cek ruang disk.".format(tujuan), K_TULIS)
        hasil.append(tujuan)
    print("\n".join(["BACKUP SELESAI ({} transaksi)".format(len(j.txns))] + ["- " + h for h in hasil] + [
        "Simpan juga salinan di tempat lain (flashdisk / penyimpanan cloud pilihan Anda) seminggu sekali."]))
    return 0


# ============================================================ argparse

def buat_parser():
    umum = argparse.ArgumentParser(add_help=False)
    umum.add_argument("--jurnal", help="file jurnal (default: $LEDGER_FILE atau ~/Pembukuan/usaha.journal)")
    umum.add_argument("--hledger", help="path program hledger (default: cari di PATH / $HLEDGER)")
    umum.add_argument("--mesin", choices=["auto", "hledger", "bawaan"], default="auto")
    umum.add_argument("--json", action="store_true", help="keluaran JSON (laporan)")

    p = argparse.ArgumentParser(prog="hledger_usaha.py", description="Asisten pembukuan hledger untuk UMKM "
                                "(Komunitech v{}).".format(VERSI))
    p.add_argument("--versi", action="version", version=VERSI)
    sub = p.add_subparsers(dest="perintah")

    s = sub.add_parser("init", parents=[umum], help="buat buku (file jurnal) baru")
    s.add_argument("--nama", help="nama usaha")
    s.add_argument("--bank", action="append", help="nama rekening bank, mis. BCA (bisa diulang)")
    s.set_defaults(fungsi=cmd_init)

    s = sub.add_parser("cek", parents=[umum], help="cek hledger & file jurnal")
    s.set_defaults(fungsi=cmd_cek)

    s = sub.add_parser("catat", parents=[umum], help="catat transaksi")
    s.add_argument("--jenis")
    s.add_argument("--tanggal")
    s.add_argument("--nominal")
    s.add_argument("--via", help="kas | bank | tempo")
    s.add_argument("--bank", help="rekening, mis. BCA atau Aset:Bank:BCA")
    s.add_argument("--pihak", help="nama pelanggan/pemasok")
    s.add_argument("--ket", help="keterangan singkat")
    s.add_argument("--akun", help="akun khusus, mis. Beban:Listrik Air Internet")
    s.add_argument("--dari")
    s.add_argument("--ke")
    s.add_argument("--posting", action="append", help="Akun=nominal (jenis bebas/saldo-awal)")
    s.add_argument("--pokok")
    s.add_argument("--bunga")
    s.add_argument("--batch", help="file JSON berisi daftar transaksi")
    s.add_argument("--akun-baru", action="store_true", help="izinkan membuat akun baru")
    s.add_argument("--tetap-catat", action="store_true", help="tetap simpan walau mirip catatan lama")
    s.add_argument("--ya", action="store_true", help="simpan (setelah pengguna setuju)")
    s.set_defaults(fungsi=cmd_catat)

    s = sub.add_parser("impor-bank", parents=[umum], help="impor CSV mutasi bank")
    s.add_argument("file")
    s.add_argument("--bank", help="rekening tujuan, mis. BCA atau Aset:Bank:BCA")
    s.add_argument("--aturan", help="file aturan .rules (default: aturan-bank.rules di folder jurnal)")
    s.add_argument("--tahun", type=int, help="tahun untuk tanggal tanpa tahun (mis. BCA '01/09')")
    s.add_argument("--desimal", choices=["koma", "titik"], help="paksa tanda desimal angka di file")
    s.add_argument("--baris-judul", type=int)
    for k in ("tanggal", "keterangan", "masuk", "keluar", "nominal", "dk", "saldo"):
        s.add_argument("--kolom-" + k)
    s.add_argument("--tetapkan", action="append", metavar="BARIS=AKUN")
    s.add_argument("--ya", action="store_true")
    s.set_defaults(fungsi=cmd_impor_bank)

    s = sub.add_parser("tambah-aturan", parents=[umum], help="tambah kata kunci pengelompokan mutasi bank")
    s.add_argument("--kata", action="append", required=True)
    s.add_argument("--akun", required=True)
    s.add_argument("--arah", choices=["masuk", "keluar", "dua"], default="dua")
    s.add_argument("--aturan")
    s.add_argument("--ya", action="store_true")
    s.set_defaults(fungsi=cmd_tambah_aturan)

    s = sub.add_parser("stok-akhir", parents=[umum], help="penyesuaian nilai persediaan dari hitung stok")
    s.add_argument("--nilai", required=True)
    s.add_argument("--tanggal")
    s.add_argument("--akun")
    s.add_argument("--akun-baru", action="store_true")
    s.add_argument("--ya", action="store_true")
    s.set_defaults(fungsi=cmd_stok_akhir)

    s = sub.add_parser("saldo", parents=[umum], help="saldo akun")
    s.add_argument("akun", nargs="*")
    s.add_argument("--tanggal")
    s.add_argument("--bulan")
    s.add_argument("--nyata", action="append", metavar="AKUN=NOMINAL")
    s.set_defaults(fungsi=cmd_saldo)

    for nama, f, per in (("laba-rugi", cmd_laba_rugi, True), ("arus-kas", cmd_arus_kas, True),
                         ("bulanan", cmd_bulanan, True), ("neraca", cmd_neraca, False),
                         ("ekspor-emkm", cmd_ekspor_emkm, True)):
        s = sub.add_parser(nama, parents=[umum])
        s.add_argument("--bulan", help="2026-09 | 09/2026 | 'September 2026' | ini | lalu")
        if per:
            s.add_argument("--dari")
            s.add_argument("--sampai")
        else:
            s.add_argument("--tanggal")
        if nama == "ekspor-emkm":
            s.add_argument("--keluar", help="file CSV hasil")
            s.add_argument("--timpa", action="store_true")
        s.set_defaults(fungsi=f)

    s = sub.add_parser("backup", parents=[umum], help="salin jurnal & aturan")
    s.add_argument("--ke", help="folder tujuan (default: backup/ di folder jurnal)")
    s.set_defaults(fungsi=cmd_backup)
    return p


def main(argv=None):
    for aliran in (sys.stdout, sys.stderr):
        try:
            aliran.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass
    p = buat_parser()
    a = p.parse_args(argv)
    if not getattr(a, "fungsi", None):
        p.print_help()
        return K_INPUT
    try:
        return a.fungsi(a) or 0
    except Gagal as e:
        print("GAGAL: " + str(e), file=sys.stderr)
        return e.kode
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    sys.exit(main())
