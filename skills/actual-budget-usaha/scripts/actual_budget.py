#!/usr/bin/env python3
"""actual_budget.py - asisten Actual Budget (lokal) untuk freelancer & usaha kecil.

Karya orisinal Komunitech. Python standar saja (tanpa paket tambahan).
Tidak berafiliasi dengan proyek Actual Budget.

Perintah:
  konversi MUTASI.csv   ubah mutasi bank Indonesia (BCA/BRI/Mandiri/BNI, CSV) jadi CSV impor Actual
  cari                  cari file budget Actual (db.sqlite) di folder data bawaan
  cek      --db PATH    periksa file budget (read-only): nama, jenis anggaran, rekening, kategori
  kategori --db PATH    daftar kategori (untuk menyamakan nama saat konversi)
  ringkasan --db PATH   ringkasan bulanan: sisa anggaran per kategori, kategori jebol, pengeluaran terbesar

File budget Actual SELALU dibuka read-only (mode=ro) dan disalin ke memori dulu; script ini
tidak pernah menulis ke db.sqlite. Jumlah uang di db.sqlite disimpan sebagai bilangan bulat
dalam SEN (Rp 1.500.000 = 150000000); semua hitungan memakai Decimal.

Kode keluar: 0 = berhasil, 2 = input pengguna tidak jelas/kurang, 3 = file tidak ditemukan/
tidak bisa dibaca, 4 = file budget tidak dikenali / sedang terkunci.
"""
import argparse
import csv
import datetime as dt
import difflib
import io
import json
import os
import re
import sqlite3
import sys
from collections import OrderedDict, defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path

VERSI = "1.0.8"
ACTUAL_DIUJI = "26.9.0"
NOL = Decimal(0)
SERATUS = Decimal(100)
MAKS_NOMINAL = Decimal("1000000000000")  # Rp 1 triliun per baris: di atas ini hampir pasti salah format

K_OK, K_INPUT, K_FILE, K_DB = 0, 2, 3, 4


class Gagal(Exception):
    def __init__(self, pesan, kode=K_INPUT):
        super().__init__(pesan)
        self.kode = kode


# ------------------------------------------------------------------ format Rupiah
def rp(nilai, tanda=True):
    """Decimal -> 'Rp 1.500.000' (sen hanya bila ada). Negatif -> '-Rp 1.500.000'."""
    v = Decimal(nilai)
    neg = v < 0
    v = abs(v).quantize(Decimal("0.01"))
    bulat, sen = divmod(v, 1)
    teks = "{:,}".format(int(bulat)).replace(",", ".")
    if sen:
        teks += "," + "{:02d}".format(int(sen * 100))
    teks = "Rp " + teks
    return ("-" + teks) if (neg and tanda) else teks


def rp_kata(nilai):
    """Seperti rp(), tetapi negatif ditulis 'minus Rp ...' (lebih mudah dibaca awam)."""
    v = Decimal(nilai)
    return ("minus " + rp(-v)) if v < 0 else rp(v)


def dari_sen(n):
    return Decimal(int(n or 0)) / SERATUS


# ------------------------------------------------------------------ angka mutasi bank
POLA_ID = re.compile(r"^\d{1,3}(\.\d{3})+(,\d{1,2})?$|^\d+(,\d{1,2})?$")
POLA_EN = re.compile(r"^\d{1,3}(,\d{3})+(\.\d{1,2})?$|^\d+(\.\d{1,2})?$")


def bersihkan_angka(teks):
    """Buang Rp/IDR/spasi/penanda CR-DB. Kembalikan (inti, negatif, penanda 'CR'|'DB'|None) atau None."""
    if teks is None:
        return None
    s = str(teks).strip().upper().replace(" ", " ").replace("−", "-")
    if not s or s in ("-", "--", "0-"):
        return None
    dk = None
    m = re.search(r"\s*\b(CR|DB|KR|DR|K|D|C)\b\.?\s*$", s)
    if m:
        dk = "CR" if m.group(1) in ("CR", "KR", "K", "C") else "DB"
        s = s[:m.start()]
    s = s.strip()
    neg = s.startswith("-") or s.endswith("-") and not re.search(r"[,.]\s*-$", s) or (s.startswith("(") and s.endswith(")"))
    s = re.sub(r"\b(RP|IDR)\b\.?", "", s)
    s = re.sub(r"[,.]\s*-\s*$", "", s)          # "1.500.000,-"
    s = re.sub(r"[\s()+-]", "", s)
    if not s:
        return None
    if not re.fullmatch(r"[\d.,]+", s):
        raise ValueError("bukan angka")
    return s.strip(".,") if s[-1] in ".," else s, neg, dk


def suara_desimal(inti):
    """Tebak pemisah desimal dari satu angka: 'koma', 'titik', atau None (tidak bisa ditebak)."""
    if "," in inti and "." in inti:
        return "koma" if inti.rfind(",") > inti.rfind(".") else "titik"
    for tanda, nama in ((",", "koma"), (".", "titik")):
        if tanda in inti:
            bag = inti.split(tanda)
            if len(bag) == 2 and len(bag[1]) in (1, 2):
                return nama
            if len(bag) > 2:  # "1.500.000" -> titik = ribuan -> desimalnya koma
                return "titik" if tanda == "," else "koma"
    return None


def ke_decimal(inti, desimal):
    """inti angka tanpa tanda -> Decimal, sesuai mode desimal ('koma' = format Indonesia)."""
    if desimal == "koma":
        if not POLA_ID.match(inti):
            raise ValueError("format angka tidak cocok dengan gaya Indonesia (1.500.000,00)")
        return Decimal(inti.replace(".", "").replace(",", "."))
    if desimal == "titik":
        if not POLA_EN.match(inti):
            raise ValueError("format angka tidak cocok dengan gaya Inggris (1,500,000.00)")
        return Decimal(inti.replace(",", ""))
    # mode belum diketahui: hanya terima yang tidak ambigu
    if re.fullmatch(r"\d+", inti):
        return Decimal(inti)
    for tanda in (".", ","):
        if tanda in inti and re.fullmatch(r"\d{1,3}(\%s\d{3})+" % tanda, inti):
            return Decimal(inti.replace(tanda, ""))  # 1.500 / 1,500 -> ribuan (Rupiah tanpa sen)
    raise ValueError("angka ambigu")


def parse_nominal(teks, desimal):
    """-> (Decimal|None, penanda). Raise ValueError bila rusak."""
    hasil = bersihkan_angka(teks)
    if hasil is None:
        return None, None
    inti, neg, dk = hasil
    v = ke_decimal(inti, desimal)
    if v != v.quantize(Decimal("0.01")):
        raise ValueError("lebih dari 2 angka di belakang koma")
    return (-v if neg else v), dk


# ------------------------------------------------------------------ tanggal
BULAN = {
    "jan": 1, "januari": 1, "january": 1, "feb": 2, "februari": 2, "february": 2, "peb": 2,
    "mar": 3, "maret": 3, "march": 3, "apr": 4, "april": 4, "mei": 5, "may": 5,
    "jun": 6, "juni": 6, "june": 6, "jul": 7, "juli": 7, "july": 7,
    "agu": 8, "ags": 8, "agt": 8, "agus": 8, "agustus": 8, "aug": 8, "august": 8,
    "sep": 9, "sept": 9, "september": 9, "okt": 10, "oktober": 10, "oct": 10, "october": 10,
    "nov": 11, "nop": 11, "november": 11, "nopember": 11,
    "des": 12, "desember": 12, "dec": 12, "december": 12,
}


def pecah_tanggal(teks):
    """Teks tanggal -> (a, b, c|None, jenis) tanpa memutuskan urutan hari/bulan.
    jenis: 'ymd' | 'dm?' (angka, urutan belum pasti) | 'dmy-nama' (bulan berupa nama)."""
    s = str(teks).strip().strip("'\"").strip()
    s = re.split(r"[ T]\d{1,2}:\d{2}", s)[0].strip()        # buang jam
    m = re.fullmatch(r"(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})", s)
    if m:
        return int(m.group(1)), int(m.group(2)), int(m.group(3)), "ymd"
    m = re.fullmatch(r"(\d{1,2})[-/.](\d{1,2})(?:[-/.](\d{2}|\d{4}))?", s)
    if m:
        c = m.group(3)
        return int(m.group(1)), int(m.group(2)), (int(c) if c else None), "dm?"
    m = re.fullmatch(r"(\d{1,2})[\s\-/.]+([A-Za-z]+)\.?(?:[\s\-/.,]+(\d{2}|\d{4}))?", s)
    if m and m.group(2).lower() in BULAN:
        c = m.group(3)
        return int(m.group(1)), BULAN[m.group(2).lower()], (int(c) if c else None), "dmy-nama"
    raise ValueError("tanggal tidak dikenali")


def rakit_tanggal(bagian, urutan, tahun_default):
    a, b, c, jenis = bagian
    if jenis == "ymd":
        y, mo, d = a, b, c
    else:
        d, mo = (a, b) if (jenis == "dmy-nama" or urutan == "dm") else (b, a)
        if c is None:
            if not tahun_default:
                raise Gagal("TANPA_TAHUN")
            y = tahun_default
        else:
            y = c + 2000 if c < 100 else c
    return dt.date(y, mo, d)


# ------------------------------------------------------------------ baca CSV mutasi
KATA_KOLOM = {
    "tanggal": ["tanggal transaksi", "tgl transaksi", "transaction date", "post date", "posting date",
                "tanggal", "tgl_tran", "tgl", "date"],
    "keterangan": ["keterangan", "uraian transaksi", "uraian", "deskripsi", "description", "desk_tran",
                   "transaction details", "remark", "berita", "narasi"],
    "keluar": ["mutasi_debet", "mutasi debet", "debet", "debit", "keluar", "pengeluaran", "withdrawal", "dana keluar"],
    "masuk": ["mutasi_kredit", "mutasi kredit", "kredit", "credit", "masuk", "pemasukan", "deposit", "dana masuk"],
    "nominal": ["jumlah", "nominal", "amount", "mutasi"],
    "dk": ["db/cr", "d/k", "cr/db", "dk", "d/c", "tipe", "type", "jenis"],
    "saldo": ["saldo_akhir_mutasi", "saldo akhir", "saldo", "balance"],
}
KOLOM_BUKAN_TANGGAL = re.compile(r"val(ue|\.)?\s*date|tgl\s*valuta|jam|time", re.I)


def norm_judul(h):
    return re.sub(r"\s+", " ", str(h).strip().strip("'\"").lower())


def skor_kolom(judul, jenis):
    h = norm_judul(judul)
    if not h:
        return 0
    if jenis == "tanggal" and KOLOM_BUKAN_TANGGAL.search(h):
        return 0
    if jenis in ("masuk", "keluar", "nominal") and re.search(r"saldo|balance", h):
        return 0
    daftar = KATA_KOLOM[jenis]
    if h in daftar:
        return 3
    if jenis in ("keluar", "masuk", "dk") and len(h) <= 3:
        return 0
    if any(len(k) > 3 and k in h for k in daftar):
        return 1
    return 0


def baca_teks(path):
    p = Path(path)
    if not p.is_file():
        raise Gagal("File '{}' tidak ditemukan. Periksa nama & lokasinya.".format(path), K_FILE)
    data = p.read_bytes()
    if data[:4] == b"PK\x03\x04" or data[:8] == b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1":
        raise Gagal("File '{}' adalah file Excel, bukan CSV. Buka di Excel lalu 'Simpan Sebagai' -> CSV, "
                    "kemudian coba lagi.".format(p.name), K_INPUT)
    if data[:5] == b"%PDF-":
        raise Gagal("File '{}' adalah PDF. Mutasi PDF tidak bisa dibaca; unduh versi CSV/Excel dari "
                    "internet banking.".format(p.name), K_INPUT)
    for enc in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue
    raise Gagal("File tidak bisa dibaca sebagai teks.", K_FILE)


def baca_mutasi(path, opsi):
    teks = baca_teks(path)
    if not teks.strip():
        raise Gagal("File mutasi '{}' kosong.".format(path))
    contoh = [x for x in teks.splitlines()[:40] if x.strip()]
    skor = {}
    for sep in (",", ";", "\t", "|"):
        hit = [len(next(csv.reader([x], delimiter=sep))) for x in contoh]
        skor[sep] = (sum(1 for h in hit if h >= 3), max(hit) if hit else 0)
    sep = max(skor, key=lambda k: skor[k])
    semua = list(csv.reader(io.StringIO(teks), delimiter=sep))

    idx = None
    for i, row in enumerate(semua[:40]):
        ada_tgl = any(skor_kolom(c, "tanggal") for c in row)
        n = sum(1 for c in row if any(skor_kolom(c, j) for j in KATA_KOLOM))
        if ada_tgl and n >= 3:
            idx = i
            break
    if idx is None:
        raise Gagal("Baris judul kolom (Tanggal, Keterangan, Debet/Kredit/Jumlah) tidak ditemukan di 40 baris "
                    "pertama. 3 baris pertama file: " + " / ".join(",".join(r) for r in semua[:3]))
    judul = [h.strip().strip("'\"") for h in semua[idx]]
    peta, terpakai = {}, set()
    for jenis in ("tanggal", "saldo", "keluar", "masuk", "nominal", "dk"):
        best, sk = None, 0
        for i, h in enumerate(judul):
            if i in terpakai:
                continue
            s = skor_kolom(h, jenis)
            if s > sk:
                best, sk = i, s
        if best is not None:
            peta[jenis] = best
            terpakai.add(best)
    ket_idx = [i for i, h in enumerate(judul) if i not in terpakai and skor_kolom(h, "keterangan")]
    if not ket_idx:
        raise Gagal("Kolom keterangan/uraian tidak ditemukan. Kolom yang ada: {}".format(", ".join(judul)))
    data_rows = semua[idx + 1:]
    # kolom tanpa judul berisi CR/DB (mis. BCA: "Jumlah,,Saldo")
    if "nominal" in peta and "dk" not in peta and not ("masuk" in peta and "keluar" in peta):
        lebar = max((len(r) for r in data_rows), default=0)
        for i in range(lebar):
            if i in terpakai:
                continue
            isi = [r[i].strip().upper() for r in data_rows if i < len(r) and r[i].strip()]
            if isi and sum(v in ("CR", "DB", "D", "K", "C", "DR", "KR") for v in isi) >= 0.8 * len(isi):
                peta["dk"] = i
                break
    if not (("masuk" in peta and "keluar" in peta) or "nominal" in peta):
        raise Gagal("Kolom jumlah (Debet/Kredit atau Jumlah) tidak ditemukan. Kolom yang ada: {}".format(", ".join(judul)))
    if "masuk" in peta and "keluar" in peta:
        peta.pop("nominal", None)

    def ambil(row, k):
        i = peta.get(k)
        return row[i].strip() if i is not None and i < len(row) else ""

    # --- tentukan gaya angka satu file
    desimal = opsi.desimal
    if not desimal:
        suara = defaultdict(int)
        for row in data_rows:
            for k in ("masuk", "keluar", "nominal", "saldo"):
                try:
                    h = bersihkan_angka(ambil(row, k))
                except ValueError:
                    continue
                if h:
                    v = suara_desimal(h[0])
                    if v:
                        suara[v] += 1
        if suara.get("koma") and suara.get("titik"):
            raise Gagal("Format angka di file campur (ada 1.500.000,00 dan 1,500,000.00). Sebutkan "
                        "--desimal koma (gaya Indonesia) atau --desimal titik (gaya Inggris).")
        desimal = "koma" if suara.get("koma") else ("titik" if suara.get("titik") else None)
        if not desimal and opsi.bank == "BCA":
            desimal = "titik"

    # --- tentukan urutan tanggal satu file
    urutan = "dm"
    pertama_besar = kedua_besar = False
    tanpa_tahun = False
    for row in data_rows:
        try:
            b = pecah_tanggal(ambil(row, "tanggal"))
        except ValueError:
            continue
        if b[3] == "dm?":
            pertama_besar |= b[0] > 12
            kedua_besar |= b[1] > 12
            tanpa_tahun |= b[2] is None
    if kedua_besar and not pertama_besar:
        urutan = "md"
    elif kedua_besar and pertama_besar:
        raise Gagal("Tanggal di file tidak konsisten (campur hari/bulan dan bulan/hari). Periksa kolom tanggal.")
    if tanpa_tahun and not opsi.tahun:
        raise Gagal("Tanggal di mutasi tanpa tahun (mis. '01/09', khas BCA). Sebutkan tahunnya: --tahun 2026.")

    hasil, lewati = [], []
    for no, row in enumerate(data_rows, start=idx + 2):
        if not any(c.strip() for c in row):
            continue
        t = ambil(row, "tanggal").strip("'\" ")
        ket = " ".join(row[i].strip().strip("'\"").strip() for i in ket_idx if i < len(row) and row[i].strip())
        ket = re.sub(r"^[=+@]+", "", ket)  # cegah teks dibaca sebagai rumus di spreadsheet
        ket = re.sub(r"\s+", " ", ket).strip()
        if not t or re.match(r"(?i)(saldo|mutasi|total|jumlah|opening|closing|ending|beginning)\b", t):
            lewati.append((no, "baris ringkasan (saldo/total), bukan transaksi", ",".join(row)[:70]))
            continue
        if t.upper().startswith("PEND"):
            lewati.append((no, "transaksi PENDING (belum final) - impor setelah muncul tanggalnya", ket[:70]))
            continue
        try:
            tgl = rakit_tanggal(pecah_tanggal(t), urutan, opsi.tahun)
        except (ValueError, Gagal):
            lewati.append((no, "tanggal tidak dikenali: '{}'".format(t), ket[:70]))
            continue
        try:
            if "masuk" in peta:
                m1, _ = parse_nominal(ambil(row, "masuk"), desimal)
                k1, _ = parse_nominal(ambil(row, "keluar"), desimal)
                masuk, keluar = abs(m1 or NOL), abs(k1 or NOL)
            else:
                v, dk = parse_nominal(ambil(row, "nominal"), desimal)
                if v is None:
                    lewati.append((no, "jumlah kosong", ket[:70]))
                    continue
                penanda = ambil(row, "dk").upper().strip(". ")
                if penanda in ("CR", "C", "K", "KR", "KREDIT", "CREDIT", "MASUK", "+"):
                    dk = "CR"
                elif penanda in ("DB", "D", "DR", "DEBET", "DEBIT", "KELUAR", "-"):
                    dk = "DB"
                if dk is None:
                    dk = "DB" if v < 0 else ("CR" if opsi.tanpa_tanda_masuk else None)
                if dk is None:
                    raise Gagal("Kolom jumlah tidak punya penanda masuk/keluar (CR/DB atau minus) di baris {}. "
                                "Periksa file, atau bila semua angka positif = uang masuk, pakai --tanpa-tanda-masuk."
                                .format(no))
                masuk, keluar = (abs(v), NOL) if dk == "CR" else (NOL, abs(v))
        except ValueError as e:
            lewati.append((no, "angka tidak jelas ({})".format(e), ket[:70]))
            continue
        if masuk and keluar:
            lewati.append((no, "kolom masuk dan keluar sama-sama terisi", ket[:70]))
            continue
        if not masuk and not keluar:
            lewati.append((no, "jumlah 0/kosong", ket[:70]))
            continue
        if max(masuk, keluar) > MAKS_NOMINAL:
            lewati.append((no, "jumlah tidak wajar (> Rp 1 triliun) - cek format angka", ket[:70]))
            continue
        saldo = None
        if "saldo" in peta and ambil(row, "saldo"):
            try:
                saldo = parse_nominal(ambil(row, "saldo"), desimal)[0]
            except ValueError:
                saldo = None
        hasil.append({"no": no, "tanggal": tgl, "ket": ket or "(tanpa keterangan)",
                      "jumlah": masuk - keluar, "saldo": saldo})
    # lintas tahun (Des -> Jan) untuk tanggal tanpa tahun
    catatan = []
    if tanpa_tahun and opsi.tahun:
        bulan = {r["tanggal"].month for r in hasil}
        if 12 in bulan and 1 in bulan:
            for r in hasil:
                if r["tanggal"].month == 12:
                    r["tanggal"] = r["tanggal"].replace(year=opsi.tahun - 1)
            catatan.append("Mutasi melewati pergantian tahun: baris Desember dianggap tahun {}.".format(opsi.tahun - 1))
    info = {"pemisah": {",": "koma", ";": "titik koma", "\t": "tab", "|": "garis tegak"}[sep],
            "baris_judul": idx + 1, "desimal": desimal or "tidak perlu (angka bulat)",
            "urutan_tanggal": "hari/bulan" if urutan == "dm" else "bulan/hari",
            "kolom": {k: judul[v] if v < len(judul) else "(tanpa judul)" for k, v in peta.items()},
            "kolom_keterangan": [judul[i] for i in ket_idx], "catatan": catatan}
    if urutan == "md":
        info["catatan"].append("Tanggal terbaca sebagai BULAN/HARI (ada angka kedua > 12). Pastikan benar.")
    return hasil, lewati, info


def cek_saldo(rows):
    """Cek kolom saldo konsisten (urutan file atau terbalik). -> dict atau None."""
    if not rows or any(r["saldo"] is None for r in rows):
        return None
    for urutan, nama in ((rows, "urut"), (list(reversed(rows)), "terbalik")):
        jalan, awal = NOL, set()
        for r in urutan:
            jalan += r["jumlah"]
            awal.add(r["saldo"] - jalan)
        if len(awal) == 1:
            a = awal.pop()
            return {"cocok": True, "saldo_awal": a, "saldo_akhir": a + jalan}
    return {"cocok": False}


# ------------------------------------------------------------------ kategori usulan
# (pola regex, arah 'masuk'|'keluar'|None, kategori|None, alasan ragu|None)
PINDAH = ("Sepertinya PINDAH DANA milik sendiri (tarik/setor tunai, top up e-wallet, bayar kartu kredit, "
          "antar rekening). Di Actual catat sebagai TRANSFER: pilih Payee = nama akun tujuan, tanpa kategori.")
SETOR = ("Setor tunai: bila ini uang HASIL JUALAN tunai yang belum pernah dicatat, pilih kategori pemasukan "
         "(mis. Pendapatan Usaha). Bila uang dari laci/dompet yang sudah tercatat di akun Actual lain, catat sebagai "
         "TRANSFER dari akun itu (tanpa kategori) agar tidak terhitung dua kali.")
ATURAN_BAWAAN = [
    (r"TARIK TUNAI|TARIKAN ATM|\bATM\b.*TARIK|PENARIKAN TUNAI|CASH WITHDRAWAL", "keluar", None, PINDAH),
    (r"SETOR(AN)? (PENJUALAN|HASIL|OMZET|JUALAN|DAGANGAN)|SETTLEMENT|MERCHANT|\bEDC\b|QRIS", "masuk",
     "Pendapatan Usaha", None),
    (r"SETOR(AN)? TUNAI|CASH DEPOSIT|SETOR TUNAI", "masuk", None, SETOR),
    (r"TOP ?UP|GOPAY|\bOVO\b|\bDANA\b|SHOPEEPAY|LINKAJA|FLAZZ|E-?MONEY|BRIZZI|TAPCASH", None, None, PINDAH),
    (r"KARTU KREDIT|CREDIT CARD|\bKK\b|PEMBAYARAN CC", "keluar", None, PINDAH),
    (r"PAJAK|\bDJP\b|\bMPN\b|BILLING ?PAJAK|\bPBB\b|SAMSAT|\bPKB\b", "keluar", "Pajak", None),
    (r"BIAYA ADM|BIAYA ADMIN|ADM(IN)? BULANAN|BIAYA TXN|BIAYA TRANSFER|BIAYA KARTU|\bFEE\b|MATERAI|BIAYA PROVISI",
     "keluar", "Biaya Bank", None),
    (r"\bBUNGA\b|INTEREST|JASA GIRO", "masuk", "Pendapatan Lain", None),
    (r"GAJI|PAYROLL|HONOR|UPAH|THR\b", "keluar", "Gaji & Honor", None),
    (r"BPJS", "keluar", "BPJS", None),
    (r"\bPLN\b|LISTRIK|TOKEN|PDAM|\bAIR\b", "keluar", "Listrik & Air", None),
    (r"TELKOMSEL|INDOSAT|\bXL\b|AXIS|SMARTFREN|\bTRI\b|PULSA|PAKET DATA|INDIHOME|TELKOM|BIZNET|FIRST ?MEDIA|MYREPUBLIC|ICONNET|WIFI|INTERNET",
     "keluar", "Internet & Pulsa", None),
    (r"SEWA|KONTRAKAN|KOST?\b|COWORKING|RUKO", "keluar", "Sewa", None),
    (r"FACEBOOK|\bMETA\b|FB ?ADS|GOOGLE ?ADS|GOOGLE ?\*?ADS|TIKTOK ?ADS|IKLAN|ADS\b", "keluar", "Iklan & Promosi", None),
    (r"ADOBE|CANVA|FIGMA|MICROSOFT|OFFICE ?365|GOOGLE ?(WORKSPACE|STORAGE|ONE)|NOTION|ZOOM|CHATGPT|OPENAI|ANTHROPIC|CLAUDE|NETFLIX|SPOTIFY|DOMAIN|HOSTING|NIAGAHOSTER|RUMAHWEB|CLOUD",
     "keluar", "Software & Langganan", None),
    (r"PERTAMINA|SPBU|SHELL|\bBBM\b|\bTOL\b|E-?TOLL|GOJEK|GRAB|MAXIM|PARKIR|KAI\b|TRAVELOKA|TIKET",
     "keluar", "Transportasi", None),
    (r"JNE|J&T|JNT|SICEPAT|ANTERAJA|POS INDONESIA|ONGKIR|PAXEL|LION PARCEL|NINJA", "keluar", "Ongkir & Kurir", None),
    (r"ANGSURAN|CICILAN|KREDIT USAHA|\bKUR\b|LEASING|ADIRA|\bFIF\b|\bBAF\b|PINJAMAN", "keluar", "Cicilan & Pinjaman", None),
    (r"TOKOPEDIA|SHOPEE|LAZADA|BLIBLI|BUKALAPAK|TIKTOK ?SHOP", "keluar", None,
     "Belanja marketplace: bisa bahan usaha, peralatan, atau keperluan pribadi. Pilih kategorinya."),
    (r"INDOMARET|ALFAMART|SUPERINDO|HYPERMART|TRANSMART|GIANT|LOTTE|HERO", "keluar", None,
     "Belanja minimarket/supermarket: keperluan usaha atau rumah tangga? Pilih kategorinya."),
    (r"REFUND|RETUR|PENGEMBALIAN|REVERSAL|KOREKSI", None, None,
     "Pengembalian dana/koreksi: masukkan ke kategori pengeluaran asalnya (bukan pendapatan)."),
    (r"PENCAIRAN|PINJAMAN|KREDIT MASUK|LOAN", "masuk", None,
     "Sepertinya pencairan pinjaman: ini BUKAN pendapatan. Di Actual catat ke akun pinjaman (transfer) atau tanya pemilik."),
]
KATEGORI_MASUK_DEFAULT = "Pendapatan Usaha"


def muat_peta(path):
    """CSV pengguna: kata_kunci,kategori[,arah]. Kata kunci = teks biasa (bukan regex)."""
    aturan = []
    teks = baca_teks(path)
    for i, row in enumerate(csv.reader(io.StringIO(teks)), 1):
        if not row or not row[0].strip() or row[0].strip().startswith("#"):
            continue
        if i == 1 and norm_judul(row[0]) in ("kata_kunci", "kata kunci", "keyword"):
            continue
        if len(row) < 2 or not row[1].strip():
            raise Gagal("File peta baris {}: format 'kata_kunci,kategori[,masuk|keluar]'.".format(i))
        arah = row[2].strip().lower() if len(row) > 2 and row[2].strip() else None
        if arah not in (None, "masuk", "keluar"):
            raise Gagal("File peta baris {}: arah harus 'masuk' atau 'keluar' (atau kosong).".format(i))
        aturan.append((re.escape(row[0].strip().upper()), arah, row[1].strip(), None))
    return aturan


def usul_kategori(ket, jumlah, aturan):
    teks = ket.upper()
    arah = "masuk" if jumlah > 0 else "keluar"
    for pola, a, kat, ragu in aturan:
        if a and a != arah:
            continue
        if re.search(pola, teks):
            return kat, ragu, pola
    if arah == "masuk":
        return KATEGORI_MASUK_DEFAULT, None, "(bawaan uang masuk)"
    return None, "Belum ada kata kunci yang cocok. Pilih kategori pengeluarannya.", None


BUANG_PAYEE = re.compile(
    r"\b(TRSF|TRF|TRANSFER|E-?BANKING|M-?BANKING|MBANKING|IBANK|INTERNET BANKING|SWITCHING|BI-?FAST|"
    r"ONLINE|OTOMATIS|KR|DB|CR|DR|DARI|KE|KPD|BYR|BAYAR|VIA|PEMBAYARAN|PEMBELIAN|QRIS|QR|DEBIT|KREDIT|"
    r"FTSCY|FTFVA|WS\w*|NBMB|MCM|INHOUSE|SKN|RTGS|LLG|ATM|EDC|POS|PURCHASE|PAYMENT|TO|FROM|IDR|RP|"
    r"KARTU|MASUK|KELUAR|TARIKAN|BRIVA|VA|VIRTUAL|ACCOUNT|BCA|BRI|BNI|MANDIRI)\b", re.I)


POTONG_REF = re.compile(r"\b(NO\.?\s?REF|REF(ERENSI)?|KODE|KD|TRX\s?ID|ID\s?TRX|NO\.?\s?TRX|NOMOR)\b.*$", re.I)


def nama_payee(ket):
    """Nama penerima yang rapi dari keterangan mutasi: buang kode transaksi, nomor, kata bank, dan ekor referensi."""
    ket = POTONG_REF.sub(" ", ket)
    ket_kasar = " ".join(w for w in ket.split() if not re.search(r"\w\.\w{2,}", w))   # FB.ME/ADS, WWW.XXX = bukan nama
    s = re.sub(r"[^\w&.\- ]", " ", ket_kasar)
    kata = [w for w in s.split()
            if not re.search(r"\d", w) and not BUANG_PAYEE.fullmatch(w) and len(w) > 1]
    nama = " ".join(kata[:5]).strip(" .-")
    if not nama:
        nama = re.sub(r"\s+", " ", ket).strip()[:40]
    return nama[:60]


# ------------------------------------------------------------------ mencocokkan usulan ke kategori budget
KATA_SEPADAN = {  # kategori usulan baku -> kata kunci yang lazim dipakai di nama kategori buatan pengguna
    "iklan & promosi": ("iklan", "promosi", "ads", "marketing", "pemasaran"),
    "software & langganan": ("software", "langganan", "subscription", "aplikasi", "tools", "digital"),
    "internet & pulsa": ("internet", "pulsa", "telepon", "komunikasi", "telekomunikasi", "wifi"),
    "listrik & air": ("listrik", "air", "utilitas", "pln", "pdam"),
    "biaya bank": ("bank", "admin", "administrasi"),
    "sewa": ("sewa", "kontrakan", "kost", "coworking", "ruko"),
    "transportasi": ("transport", "transportasi", "bbm", "bensin", "kendaraan", "perjalanan"),
    "ongkir & kurir": ("ongkir", "kurir", "pengiriman", "ekspedisi", "logistik"),
    "gaji & honor": ("gaji", "honor", "upah", "karyawan", "payroll"),
    "cicilan & pinjaman": ("cicilan", "pinjaman", "angsuran", "utang", "kredit"),
    "pajak": ("pajak", "tax"),
    "bpjs": ("bpjs", "asuransi", "jaminan"),
    "pendapatan usaha": ("pendapatan", "penjualan", "omzet", "income", "usaha", "proyek", "jasa"),
    "pendapatan lain": ("pendapatan", "lain", "bunga", "income"),
}
KATA_SEPADAN_NORM = {}
KATA_UMUM = {"dan", "biaya", "untuk", "lain", "lainnya", "usaha", "di", "ke", "the"}


def _norm_kat(teks):
    t = re.sub(r"[^a-z0-9 ]+", " ", (teks or "").lower().replace("&", " dan "))
    return re.sub(r"\s+", " ", t).strip()


def _isi_sepadan():
    for k, v in KATA_SEPADAN.items():
        KATA_SEPADAN_NORM[_norm_kat(k)] = v


def _kata_kat(teks):
    return [w for w in _norm_kat(teks).split() if w not in KATA_UMUM and len(w) > 1]


_isi_sepadan()


def cocokkan_kategori(usul, kategori_db, income):
    """Cocokkan nama kategori usulan ke daftar kategori yang ADA di budget.
    kategori_db: {nama: info}. income: True bila usulan untuk uang masuk.
    -> (nama_db atau None, cara, pilihan) ; pilihan = daftar nama bila ambigu."""
    kandidat = [n for n, v in kategori_db.items() if bool(v["is_income"]) == bool(income)]
    if not kandidat:
        return None, None, []
    nu = _norm_kat(usul)
    for n in kandidat:                                    # 1. sama persis setelah normalisasi
        if _norm_kat(n) == nu:
            return n, "nama sama (normalisasi)", []
    skor = {}
    kata_u = set(_kata_kat(usul))
    sepadan = set(KATA_SEPADAN_NORM.get(nu, ()))
    for n in kandidat:
        kata_n = set(_kata_kat(n))
        sk = 0.0
        if kata_u and kata_u & kata_n:                    # 2. kata inti sama ("Sewa" ~ "Sewa Coworking")
            sk = max(sk, 0.9)
        if sepadan and (sepadan & kata_n):                # 3. kata kunci sepadan ("Iklan & Promosi" ~ "Iklan")
            sk = max(sk, 0.8)
        r = difflib.SequenceMatcher(None, nu, _norm_kat(n)).ratio()   # 4. kemiripan tulisan
        if r >= 0.75:
            sk = max(sk, r)
        if sk:
            skor[n] = sk
    if not skor:
        return None, None, []
    terbaik = max(skor.values())
    puncak = sorted(n for n, v in skor.items() if v >= terbaik - 1e-9)
    if len(puncak) == 1:
        return puncak[0], "mirip", []
    return None, "ambigu", puncak


def _kunci_payee(nama):
    return re.sub(r"[^A-Z0-9]", "", (nama or "").upper())


def riwayat_payee(con):
    """Riwayat transaksi lama: {kunci payee: Counter(nama kategori)}. Hanya transaksi berkategori, bukan transfer."""
    kat = {r["id"]: r["nama"] for r in daftar_kategori(con) if not r["tombstone"]}
    _, _, trx = muat_data(con)
    peta = defaultdict(lambda: defaultdict(int))
    for t in trx:
        if t["transfer"] or not t["kategori"] or t["kategori"] not in kat or not t.get("nama_payee"):
            continue
        k = _kunci_payee(nama_payee(t["nama_payee"]))
        if len(k) >= 4:
            peta[k][kat[t["kategori"]]] += 1
    return peta


def cari_riwayat(payee, peta):
    """Kategori paling sering dipakai untuk penerima yang sama (persis, mengandung, atau sangat mirip)."""
    k = _kunci_payee(payee)
    if len(k) < 4 or not peta:
        return None
    cocok = peta.get(k)
    if not cocok:
        for kk, v in peta.items():
            if (len(k) >= 5 and len(kk) >= 5 and (k in kk or kk in k)) or \
               difflib.SequenceMatcher(None, k, kk).ratio() >= 0.85:
                cocok = v
                break
    if not cocok:
        return None
    return max(sorted(cocok), key=lambda n: cocok[n])


def format_angka_csv(v):
    """Decimal -> '-150000' atau '1500000.50' (titik desimal, tanpa pemisah ribuan).
    Dibaca benar oleh looselyParseAmount di Actual (diuji terhadap kode sumber v26.9.0)."""
    v = Decimal(v).quantize(Decimal("0.01"))
    if v == v.to_integral_value():
        return str(int(v))
    return "{:.2f}".format(v)


def susun_pertanyaan(ragu, kategori_db):
    """Kelompokkan baris 'perlu dicek' jadi maksimal 5 pertanyaan (satu per jenis masalah)."""
    judul = OrderedDict([
        ("kategori", "Pilih kategori untuk baris berikut (usulan otomatis tidak ketemu/ambigu di budget Anda)"),
        ("pindah", "Apakah baris berikut pindah dana milik sendiri (dicatat sebagai TRANSFER ke akun tujuan, tanpa kategori)? "
                   "Sebutkan nama akun tujuannya di Actual"),
        ("setor", "Setor tunai berikut: hasil jualan tunai yang belum tercatat (pemasukan) atau uang dari kas yang sudah "
                  "tercatat (transfer)"),
        ("lain", "Belanja/pengembalian/pinjaman berikut: pilih kategori atau bilang kalau bukan transaksi usaha"),
        ("cek", "Cek data: nominal sangat kecil atau baris kembar berikut, apakah sudah benar"),
    ])
    hasil = []
    for g, teks in judul.items():
        baris = [x for x in ragu if x[6] == g]
        if not baris:
            continue
        if g == "kategori" and kategori_db:
            pilihan = [n for n, v in kategori_db.items() if not v["is_income"]][:15]
            teks += " (kategori yang ada: {})".format(", ".join(pilihan))
        hasil.append({"kelompok": g, "pertanyaan": teks, "baris": [x[0] for x in baris]})
    return hasil


def cmd_konversi(a):
    if a.desimal and a.desimal not in ("koma", "titik"):
        raise Gagal("--desimal harus 'koma' (1.500.000,00) atau 'titik' (1,500,000.00).")
    a.bank = (a.bank or "").upper() or None
    if a.bank and a.bank not in ("BCA", "BRI", "MANDIRI", "BNI", "LAIN"):
        raise Gagal("--bank: BCA, BRI, MANDIRI, BNI, atau LAIN.")
    rows, lewati, info = baca_mutasi(a.mutasi, a)
    if not rows:
        raise Gagal("Tidak ada baris transaksi yang terbaca. Baris yang dilewati: " +
                    "; ".join("baris {}: {}".format(n, r) for n, r, _ in lewati[:5]))
    aturan = (muat_peta(a.peta) if a.peta else []) + ATURAN_BAWAAN
    kategori_db = None
    riwayat = {}
    if a.db:
        con, _ = buka_db(a.db)
        kategori_db = {r["nama"]: r for r in daftar_kategori(con) if not r["tombstone"]}
        try:
            riwayat = riwayat_payee(con)
        except sqlite3.Error:
            riwayat = {}
        con.close()
    else:
        riwayat = {}

    keluar_path = Path(a.keluaran) if a.keluaran else Path(a.mutasi).with_name(Path(a.mutasi).stem + "-actual.csv")
    ragu_path = keluar_path.with_name(keluar_path.stem + "-ragu.csv")
    if keluar_path.resolve() == Path(a.mutasi).resolve():
        raise Gagal("File hasil tidak boleh sama dengan file mutasi asli.")
    for p in (keluar_path, ragu_path):
        if p.exists() and not a.timpa:
            raise Gagal("File '{}' sudah ada. Pakai --keluaran nama-lain.csv atau --timpa.".format(p))

    kembar = defaultdict(int)
    for r in rows:
        kembar[(r["tanggal"], r["jumlah"], r["ket"])] += 1

    hasil, ragu = [], []
    per_kat = defaultdict(lambda: [0, NOL])
    masuk_default = 0
    dipetakan = OrderedDict()      # usulan baku -> nama kategori di budget
    dari_riwayat = 0
    for r in rows:
        kat, alasan, pola = usul_kategori(r["ket"], r["jumlah"], aturan)
        grup = None
        if alasan:
            grup = ("pindah" if alasan == PINDAH else "setor" if alasan == SETOR else
                    "kategori" if pola is None else "lain")
        payee = nama_payee(r["ket"])
        # riwayat transaksi lama untuk penerima yang sama (hanya bila aturan tidak menandai transfer/setor/dll.)
        if kategori_db is not None and not alasan:
            lama = cari_riwayat(payee, riwayat)
            if lama and lama in kategori_db and bool(kategori_db[lama]["is_income"]) == (r["jumlah"] > 0):
                if lama != kat:
                    dari_riwayat += 1
                kat, pola = lama, "(riwayat)"
        if kat and kategori_db is not None and pola != "(riwayat)":
            if kat in kategori_db:
                pass
            else:
                nama_db, cara, pilihan = cocokkan_kategori(kat, kategori_db, r["jumlah"] > 0)
                if nama_db:
                    dipetakan[kat] = nama_db
                    kat = nama_db
                else:
                    if pilihan:
                        alasan = ("Kategori usulan '{}' cocok dengan beberapa kategori di budget Anda: {}. "
                                  "Pilih salah satu.".format(kat, " / ".join(pilihan)))
                    else:
                        alasan = ("Kategori usulan '{}' belum ada di budget Actual Anda. Buat kategorinya di Actual, "
                                  "atau pilih kategori lain yang sudah ada.".format(kat))
                    grup = "kategori"
                    kat = None
        if kat and kategori_db is not None:
            # uang masuk wajib ke kategori pemasukan, uang keluar ke kategori pengeluaran
            if r["jumlah"] < 0 and kategori_db[kat]["is_income"] and not alasan:
                alasan = "Uang keluar diberi kategori PEMASUKAN '{}'. Periksa.".format(kat)
                grup = "lain"
        if pola == "(bawaan uang masuk)" and kat:
            masuk_default += 1
        if abs(r["jumlah"]) < 100:
            kecil = ("Nominal sangat kecil ({}): pastikan format angka terbaca benar (mis. '12,5' dibaca "
                     "Rp 12,50).".format(rp(abs(r["jumlah"]))))
            alasan = (alasan + " " + kecil) if alasan else kecil
            grup = grup or "cek"
        if kembar[(r["tanggal"], r["jumlah"], r["ket"])] > 1:
            tambahan = "Baris sama persis muncul {}x di file: pastikan bukan dobel.".format(
                kembar[(r["tanggal"], r["jumlah"], r["ket"])])
            alasan = (alasan + " " + tambahan) if alasan else tambahan
            grup = grup or "cek"
        hasil.append([r["tanggal"].isoformat(), payee, r["ket"], kat or "", format_angka_csv(r["jumlah"])])
        per_kat[kat or "(kosong - perlu dipilih)"][0] += 1
        per_kat[kat or "(kosong - perlu dipilih)"][1] += r["jumlah"]
        if alasan:
            ragu.append([r["no"], r["tanggal"].isoformat(), r["ket"], format_angka_csv(r["jumlah"]), kat or "", alasan,
                         grup or "lain"])

    keluar_path.parent.mkdir(parents=True, exist_ok=True)
    with open(keluar_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Date", "Payee", "Notes", "Category", "Amount"])
        w.writerows(hasil)
    with open(ragu_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Baris", "Tanggal", "Keterangan", "Jumlah", "Kategori", "Alasan"])
        w.writerows([x[:6] for x in ragu])

    total_masuk = sum((r["jumlah"] for r in rows if r["jumlah"] > 0), NOL)
    total_keluar = -sum((r["jumlah"] for r in rows if r["jumlah"] < 0), NOL)
    saldo = cek_saldo(rows)
    ringkas = {
        "file_mutasi": str(a.mutasi), "file_hasil": str(keluar_path), "file_ragu": str(ragu_path),
        "baris_terbaca": len(rows), "baris_dilewati": len(lewati), "baris_ragu": len(ragu),
        "total_masuk": str(total_masuk), "total_keluar": str(total_keluar),
        "periode": [min(r["tanggal"] for r in rows).isoformat(), max(r["tanggal"] for r in rows).isoformat()],
        "deteksi": info, "cek_saldo": ({k: str(v) if isinstance(v, Decimal) else v for k, v in saldo.items()}
                                       if saldo else None),
        "per_kategori": {k: {"baris": v[0], "jumlah": str(v[1])} for k, v in per_kat.items()},
        "ragu": [{"baris": x[0], "tanggal": x[1], "keterangan": x[2], "jumlah": x[3], "kategori": x[4],
                  "alasan": x[5], "kelompok": x[6]} for x in ragu],
        "pertanyaan": susun_pertanyaan(ragu, kategori_db),
        "kategori_dipetakan": dict(dipetakan), "dari_riwayat": dari_riwayat,
        "dilewati": [{"baris": n, "alasan": al, "isi": isi} for n, al, isi in lewati],
        "kategori_dicek_ke_budget": kategori_db is not None,
    }
    if a.json:
        print(json.dumps(ringkas, ensure_ascii=False, indent=2))
        return K_OK
    out = []
    out.append("KONVERSI MUTASI -> CSV IMPOR ACTUAL")
    out.append("File mutasi: {}".format(a.mutasi))
    out.append("Periode: {} s.d. {}".format(tgl_id(min(r["tanggal"] for r in rows)), tgl_id(max(r["tanggal"] for r in rows))))
    out.append("Terbaca: {} transaksi | Dilewati: {} | Perlu dicek: {}".format(len(rows), len(lewati), len(ragu)))
    out.append("Total masuk: {} | Total keluar: {}".format(rp(total_masuk), rp(total_keluar)))
    if saldo:
        if saldo["cocok"]:
            out.append("Cek saldo bank: COCOK (saldo awal {} -> saldo akhir {})".format(
                rp(saldo["saldo_awal"]), rp(saldo["saldo_akhir"])))
        else:
            out.append("Cek saldo bank: TIDAK COCOK - ada baris yang hilang/terbaca salah. Jangan impor dulu; "
                       "periksa baris yang dilewati.")
    for c in info["catatan"]:
        out.append("Catatan: " + c)
    out.append("")
    out.append("RINGKASAN PER KATEGORI USULAN")
    for k, v in sorted(per_kat.items(), key=lambda x: x[1][1]):
        out.append("- {}: {} baris, {}".format(k, v[0], rp(v[1])))
    if masuk_default:
        out.append("Catatan: {} uang masuk otomatis diusulkan '{}'. Ganti bila itu pinjaman, uang pribadi, "
                   "atau pindahan dari rekening sendiri.".format(masuk_default, KATEGORI_MASUK_DEFAULT))
    for u, n in dipetakan.items():
        out.append("Catatan: usulan '{}' dipetakan ke kategori Anda '{}'.".format(u, n))
    if dari_riwayat:
        out.append("Catatan: {} baris memakai kategori dari riwayat transaksi lama (penerima yang sama).".format(dari_riwayat))
    if kategori_db is None:
        out.append("Catatan: nama kategori BELUM dicocokkan dengan budget Anda. Actual hanya mengisi kategori bila "
                   "namanya SAMA PERSIS (huruf besar/kecil juga). Jalankan ulang dengan --db agar dicek.")
    if ragu:
        out.append("")
        out.append("PERLU DICEK ({} baris, juga di {}):".format(len(ragu), ragu_path.name))
        for x in ragu[:20]:
            out.append("- Baris {} | {} | {} | {}: {}".format(x[0], x[1], x[2][:45], rp(Decimal(x[3])), x[5]))
        if len(ragu) > 20:
            out.append("- ... {} baris lain di file ragu".format(len(ragu) - 20))
        out.append("")
        out.append("PERTANYAAN UNTUK PENGGUNA (kelompok, tanyakan sekaligus dalam satu pesan):")
        for i, q in enumerate(susun_pertanyaan(ragu, kategori_db), 1):
            out.append("{}. {}: baris {}".format(i, q["pertanyaan"], ", ".join(str(n) for n in q["baris"])))
    if lewati:
        out.append("")
        out.append("DILEWATI ({} baris, tidak masuk file hasil):".format(len(lewati)))
        for n, al, isi in lewati[:15]:
            out.append("- Baris {}: {} | {}".format(n, al, isi))
    out.append("")
    out.append("File hasil: {}".format(keluar_path))
    out.append("Cara impor di Actual: buka akun bank -> Import -> pilih file hasil -> pastikan kolom Date/Payee/"
               "Notes/Category/Amount terpasang, format tanggal 'YYYY MM DD', pemisah koma, opsi 'Split amount' "
               "dan 'Flip amount' MATI -> cek pratinjau -> Import.")
    print("\n".join(out))
    return K_OK


# ------------------------------------------------------------------ baca db.sqlite (READ-ONLY)
TABEL_WAJIB = {
    "transactions": {"id", "isParent", "isChild", "acct", "category", "amount", "description", "date",
                     "tombstone", "parent_id", "starting_balance_flag"},
    "categories": {"id", "name", "is_income", "cat_group", "tombstone"},
    "category_groups": {"id", "name", "is_income", "tombstone"},
    "category_mapping": {"id", "transferId"},
    "payees": {"id", "name", "transfer_acct", "tombstone"},
    "payee_mapping": {"id", "targetId"},
    "accounts": {"id", "name", "offbudget", "closed", "tombstone"},
    "zero_budgets": {"month", "category", "amount", "carryover"},
}


def cari_db(path):
    p = Path(os.path.expanduser(str(path)))
    if p.is_dir():
        kandidat = p / "db.sqlite"
        if kandidat.is_file():
            return kandidat
        sub = sorted(p.glob("*/db.sqlite"))
        if len(sub) == 1:
            return sub[0]
        if sub:
            raise Gagal("Folder berisi lebih dari satu budget. Pilih salah satu:\n" +
                        "\n".join("- {} ({})".format(x.parent, nama_budget(x.parent)) for x in sub), K_INPUT)
        raise Gagal("Tidak ada db.sqlite di folder '{}'. Jalankan perintah 'cari' untuk menemukan budget Anda."
                    .format(p), K_FILE)
    if not p.is_file():
        raise Gagal("File budget '{}' tidak ditemukan. Jalankan perintah 'cari'.".format(p), K_FILE)
    if p.suffix.lower() == ".zip":
        raise Gagal("Ini file ekspor/backup Actual (.zip). Ekstrak dulu, lalu pakai db.sqlite di dalamnya "
                    "(atau pakai folder budget asli di folder data Actual).", K_INPUT)
    return p


def nama_budget(folder):
    try:
        with open(Path(folder) / "metadata.json", encoding="utf-8") as f:
            return json.load(f).get("budgetName") or "(tanpa nama)"
    except (OSError, ValueError):
        return "(metadata.json tidak terbaca)"


def buka_db(path):
    """Buka db.sqlite READ-ONLY (mode=ro), salin ke memori, tutup file asli. -> (koneksi memori, path)."""
    p = cari_db(path).resolve()
    with open(p, "rb") as f:
        if f.read(16) != b"SQLite format 3\x00":
            raise Gagal("File '{}' bukan database SQLite (bukan file budget Actual).".format(p), K_DB)
    uri = p.as_uri() + "?mode=ro"
    try:
        src = sqlite3.connect(uri, uri=True, timeout=5, isolation_level=None)
        mem = sqlite3.connect(":memory:")
        try:
            # Ambil kunci baca (SHARED) dulu: bila Actual sedang menulis, ini gagal dengan 'locked'
            # setelah 5 detik (backup() bawaan Python akan menunggu tanpa batas).
            src.execute("BEGIN")
            src.execute("SELECT count(*) FROM sqlite_master").fetchone()
            src.backup(mem)
            src.execute("COMMIT")
        finally:
            src.close()
    except sqlite3.OperationalError as e:
        pesan = str(e).lower()
        if "locked" in pesan or "busy" in pesan:
            raise Gagal("File budget sedang dipakai/ditulis Actual. Tunggu sebentar (atau tutup Actual) lalu coba "
                        "lagi.", K_DB)
        raise Gagal("File budget tidak bisa dibuka read-only ({}). Tutup aplikasi Actual lalu coba lagi. Jika "
                    "tetap gagal, pakai salinan (Actual: Export) yang diekstrak.".format(e), K_DB)
    except sqlite3.DatabaseError as e:
        raise Gagal("File budget rusak atau bukan SQLite ({}).".format(e), K_DB)
    mem.row_factory = sqlite3.Row
    kolom = {}
    for (nama,) in mem.execute("SELECT name FROM sqlite_master WHERE type='table'"):
        kolom[nama] = {r[1] for r in mem.execute('PRAGMA table_info("{}")'.format(nama.replace('"', '""')))}
    kurang = []
    for t, cols in TABEL_WAJIB.items():
        if t not in kolom:
            kurang.append(t)
        elif not cols <= kolom[t]:
            kurang.append("{} ({})".format(t, ", ".join(sorted(cols - kolom[t]))))
    if kurang:
        raise Gagal("File ini tidak dikenali sebagai budget Actual (versi {} diuji). Bagian yang tidak ada: {}. "
                    "Pastikan memilih db.sqlite dari folder budget Actual.".format(ACTUAL_DIUJI, "; ".join(kurang)), K_DB)
    return mem, p


def ada_kolom(con, tabel, kolom):
    return any(r[1] == kolom for r in con.execute('PRAGMA table_info("{}")'.format(tabel)))


def pref(con, kunci):
    if not con.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='preferences'").fetchone():
        return None
    r = con.execute("SELECT value FROM preferences WHERE id = ?", (kunci,)).fetchone()
    return r[0] if r else None


def daftar_kategori(con):
    hid_c = "c.hidden" if ada_kolom(con, "categories", "hidden") else "0"
    hid_g = "g.hidden" if ada_kolom(con, "category_groups", "hidden") else "0"
    so_c = "c.sort_order" if ada_kolom(con, "categories", "sort_order") else "0"
    so_g = "g.sort_order" if ada_kolom(con, "category_groups", "sort_order") else "0"
    q = ("SELECT c.id, c.name AS nama, c.is_income, c.cat_group, IFNULL(c.tombstone,0) AS tombstone, "
         "{} AS hidden, g.name AS grup, IFNULL(g.tombstone,1) AS g_tomb, {} AS g_hidden, "
         "IFNULL({},0) AS so_g, IFNULL({},0) AS so_c "
         "FROM categories c LEFT JOIN category_groups g ON g.id = c.cat_group "
         "ORDER BY c.is_income, so_g, g.name, so_c, c.name").format(hid_c, hid_g, so_g, so_c)
    hasil = []
    for r in con.execute(q):
        d = dict(r)
        d["tombstone"] = bool(d["tombstone"]) or bool(d["g_tomb"])
        d["hidden"] = bool(d["hidden"]) or bool(d["g_hidden"])
        d["is_income"] = bool(d["is_income"])
        hasil.append(d)
    return hasil


SQL_TRANSAKSI = """
SELECT t.id, t.isParent AS is_parent, t.isChild AS is_child, t.acct AS akun,
       CASE WHEN t.isParent = 1 THEN NULL ELSE cm.transferId END AS kategori,
       IFNULL(t.amount, 0) AS jumlah, pm.targetId AS payee, t.notes AS catatan, t.date AS tanggal,
       IFNULL(t.starting_balance_flag, 0) AS saldo_awal, t.parent_id
FROM transactions t
LEFT JOIN category_mapping cm ON cm.id = t.category
LEFT JOIN payee_mapping pm ON pm.id = t.description
LEFT JOIN transactions p ON (t.isChild = 1 AND p.id = t.parent_id)
WHERE t.date IS NOT NULL AND t.acct IS NOT NULL
  AND (t.isChild = 0 OR t.parent_id IS NOT NULL)
  AND IFNULL(t.tombstone, 0) = 0
  AND (t.isChild = 0 OR p.tombstone = 0)
"""
# Setara dengan view v_transactions_internal_alive di Actual 26.9.0
# (packages/loot-core/src/server/aql/schema/index.ts).


def muat_data(con):
    akun = {r["id"]: dict(r) for r in con.execute(
        "SELECT id, name, IFNULL(offbudget,0) AS offbudget, IFNULL(closed,0) AS closed, "
        "IFNULL(tombstone,0) AS tombstone FROM accounts")}
    payee = {r["id"]: dict(r) for r in con.execute(
        "SELECT id, name, transfer_acct, IFNULL(tombstone,0) AS tombstone FROM payees")}
    trx = [dict(r) for r in con.execute(SQL_TRANSAKSI)]
    for t in trx:
        a = akun.get(t["akun"])
        t["on_budget"] = bool(a) and not a["offbudget"]
        p = payee.get(t["payee"]) if t["payee"] else None
        t["nama_payee"] = p["name"] if p else None
        tujuan = akun.get(p["transfer_acct"]) if p and p["transfer_acct"] else None
        t["transfer_on_budget"] = bool(tujuan) and not tujuan["offbudget"]
        t["transfer"] = bool(p and p["transfer_acct"])
        if p and p["transfer_acct"] and not (p["name"] or "").strip():
            nama_akun = akun[p["transfer_acct"]]["name"] if p["transfer_acct"] in akun else "akun lain"
            t["nama_payee"] = ("Transfer ke " if int(t["jumlah"] or 0) < 0 else "Transfer dari ") + nama_akun
        if not (t["nama_payee"] or "").strip() and (t["catatan"] or "").strip():
            t["nama_payee"] = nama_payee(t["catatan"])
        t["bulan"] = int(t["tanggal"]) // 100
    return akun, payee, trx


def muat_anggaran(con, tabel):
    ang = {}
    if not con.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (tabel,)).fetchone():
        return ang
    for r in con.execute("SELECT month, category, IFNULL(amount,0) AS amount, IFNULL(carryover,0) AS carryover "
                         "FROM {}".format(tabel)):
        ang[(int(r["month"]), r["category"])] = (int(r["amount"]), bool(r["carryover"]))
    return ang


def geser_bulan(ym, n):
    y, m = divmod(ym, 100)
    total = y * 12 + (m - 1) + n
    return (total // 12) * 100 + total % 12 + 1


NAMA_BULAN = ["", "Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September",
              "Oktober", "November", "Desember"]


def tgl_id(d):
    return "{} {} {}".format(d.day, NAMA_BULAN[d.month], d.year)


def parse_bulan(teks, hari_ini=None):
    hari_ini = hari_ini or dt.date.today()
    ini = hari_ini.year * 100 + hari_ini.month
    s = (teks or "ini").strip().lower()
    if s in ("ini", "bulan ini", "sekarang"):
        return ini
    if s in ("lalu", "bulan lalu", "kemarin"):
        return geser_bulan(ini, -1)
    m = re.fullmatch(r"(\d{4})[-/](\d{1,2})", s) or None
    if m:
        y, mo = int(m.group(1)), int(m.group(2))
    else:
        m = re.fullmatch(r"(\d{1,2})[-/](\d{4})", s)
        if m:
            y, mo = int(m.group(2)), int(m.group(1))
        else:
            m = re.fullmatch(r"([a-z]+)\.?\s+(\d{4})", s)
            if not m or m.group(1) not in BULAN:
                raise Gagal("Bulan '{}' tidak dikenali. Contoh: 2026-09, 09/2026, 'September 2026', ini, lalu."
                            .format(teks))
            y, mo = int(m.group(2)), BULAN[m.group(1)]
    if not 1 <= mo <= 12:
        raise Gagal("Bulan '{}' tidak valid.".format(teks))
    return y * 100 + mo


def hitung_bulan(con, target):
    """Hitung anggaran s.d. bulan target, meniru rumus spreadsheet Actual 26.9.0
    (packages/loot-core/src/server/budget/envelope.ts, tracking.ts, base.ts)."""
    jenis = pref(con, "budgetType") or "envelope"
    if jenis == "report":
        jenis = "tracking"
    tabel = "reflect_budgets" if jenis == "tracking" else "zero_budgets"
    kategori = [k for k in daftar_kategori(con) if not k["tombstone"]]
    kat_id = {k["id"]: k for k in kategori}
    akun, payee, trx = muat_data(con)
    ang = muat_anggaran(con, tabel)

    pakai = defaultdict(int)  # (bulan, kategori) -> sen (on-budget)
    for t in trx:
        if t["on_budget"] and t["kategori"]:
            pakai[(t["bulan"], t["kategori"])] += int(t["jumlah"])
    bulan_trx = [t["bulan"] for t in trx if t["on_budget"]]
    mulai = geser_bulan(min(bulan_trx + [target]), -3)  # Actual membuat lembar mulai 3 bulan sebelum transaksi tertua

    beban = [k for k in kategori if not k["is_income"]]
    pemasukan = [k for k in kategori if k["is_income"]]
    budget_months = {}
    if con.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='zero_budget_months'").fetchone():
        for r in con.execute("SELECT id, IFNULL(buffered,0) AS b FROM zero_budget_months"):
            try:
                y, m = str(r["id"]).split("-")
                budget_months[int(y) * 100 + int(m)] = int(r["b"])
            except ValueError:
                continue

    sisa_lalu = {k["id"]: 0 for k in beban}
    bawa_lalu = {k["id"]: False for k in beban}
    sisa_lalu_inc = {k["id"]: 0 for k in pemasukan}
    bawa_lalu_inc = {k["id"]: False for k in pemasukan}
    to_budget_lalu, buffer_lalu = 0, 0
    m = mulai
    hasil = None
    while m <= target:
        baris = []
        overspent_lalu = sum(min(0, sisa_lalu[c]) for c in sisa_lalu if not bawa_lalu[c])
        total_ang = 0
        for k in beban:
            b, bawa = ang.get((m, k["id"]), (0, False))
            s = pakai.get((m, k["id"]), 0)
            if jenis == "envelope":
                sisa = b + s + (sisa_lalu[k["id"]] if bawa_lalu[k["id"]] else max(sisa_lalu[k["id"]], 0))
                dari_lalu = sisa - b - s
            else:
                dari_lalu = sisa_lalu[k["id"]] if bawa_lalu[k["id"]] else 0
                sisa = b + s + dari_lalu
            baris.append({"id": k["id"], "kategori": k["nama"], "grup": k["grup"], "tersembunyi": k["hidden"],
                          "anggaran": b, "terpakai": -s, "bawaan": dari_lalu, "sisa": sisa, "bawa_minus": bawa})
            sisa_lalu[k["id"]], bawa_lalu[k["id"]] = sisa, bawa
            total_ang += b
        masuk_bulan = 0
        buffer_auto = 0
        masuk_rinci = []
        for k in pemasukan:
            b, bawa = ang.get((m, k["id"]), (0, False))
            s = pakai.get((m, k["id"]), 0)
            masuk_bulan += s
            if bawa:
                buffer_auto += s
            masuk_rinci.append({"kategori": k["nama"], "diterima": s})
        buffer_manual = budget_months.get(m, 0)
        buffer_sel = buffer_manual if buffer_manual != 0 else buffer_auto
        to_budget = masuk_bulan + to_budget_lalu + buffer_lalu + overspent_lalu - total_ang - buffer_sel
        if m == target:
            hasil = {"jenis": jenis, "bulan": m, "kategori": baris, "pemasukan": masuk_rinci,
                     "total_pemasukan": masuk_bulan, "total_anggaran": total_ang,
                     "total_terpakai": sum(x["terpakai"] for x in baris),
                     "overspent_lalu": overspent_lalu, "siap_dianggarkan": to_budget if jenis == "envelope" else None,
                     "ditahan": buffer_sel, "ditahan_lalu": buffer_lalu}
        to_budget_lalu, buffer_lalu = to_budget, buffer_sel
        m = geser_bulan(m, 1)

    # transaksi bulan target
    tb = [t for t in trx if t["bulan"] == target and t["on_budget"]]
    tanpa_kat = [t for t in tb if not t["kategori"] and not t["is_parent"] and not t["transfer_on_budget"]
                 and not t["saldo_awal"]]
    anak = defaultdict(list)
    for t in tb:
        if t["is_child"]:
            anak[t["parent_id"]].append(t)
    besar = []
    for t in tb:
        if t["is_child"] or t["transfer_on_budget"] or int(t["jumlah"]) >= 0:
            continue
        if t["is_parent"]:
            kats = sorted({kat_id[c["kategori"]]["nama"] for c in anak[t["id"]] if c["kategori"] in kat_id})
            label = "dipecah: " + ", ".join(kats) if kats else "dipecah"
        else:
            label = kat_id[t["kategori"]]["nama"] if t["kategori"] in kat_id else "tanpa kategori"
        besar.append({"tanggal": t["tanggal"], "payee": t["nama_payee"] or "(tanpa payee)",
                      "jumlah": -int(t["jumlah"]), "kategori": label, "akun": akun[t["akun"]]["name"]})
    besar.sort(key=lambda x: (-x["jumlah"], x["tanggal"]))
    hasil["tanpa_kategori"] = {"jumlah_baris": len(tanpa_kat), "total": sum(int(t["jumlah"]) for t in tanpa_kat)}
    hasil["terbesar"] = besar
    hasil["ada_transaksi"] = bool(tb)
    hasil["mata_uang"] = pref(con, "defaultCurrencyCode")
    return hasil


def cmd_ringkasan(a):
    con, p = buka_db(a.db)
    target = parse_bulan(a.bulan)
    h = hitung_bulan(con, target)
    con.close()
    y, mo = divmod(target, 100)
    jebol = [x for x in h["kategori"] if x["sisa"] < 0]
    aktif = [x for x in h["kategori"] if x["anggaran"] or x["terpakai"] or x["sisa"]]
    if a.json:
        def s(v):
            return str(dari_sen(v)) if isinstance(v, int) and not isinstance(v, bool) else v
        out = {k: v for k, v in h.items() if k not in ("kategori", "terbesar", "pemasukan", "tanpa_kategori")}
        out = {k: s(v) if k not in ("bulan", "jenis", "mata_uang", "ada_transaksi") else v for k, v in out.items()}
        out["budget"] = nama_budget(p.parent)
        out["file"] = str(p)
        out["kategori"] = [{k: s(v) for k, v in x.items() if k != "id"} for x in aktif]
        out["jebol"] = [x["kategori"] for x in jebol]
        out["pemasukan"] = [{"kategori": x["kategori"], "diterima": s(x["diterima"])} for x in h["pemasukan"] if x["diterima"]]
        out["terbesar"] = [{**x, "jumlah": s(x["jumlah"]), "tanggal": "{}-{}-{}".format(
            str(x["tanggal"])[:4], str(x["tanggal"])[4:6], str(x["tanggal"])[6:])} for x in h["terbesar"][:a.top]]
        out["tanpa_kategori"] = {"jumlah_baris": h["tanpa_kategori"]["jumlah_baris"],
                                 "total": s(h["tanpa_kategori"]["total"])}
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return K_OK
    L = []
    L.append("RINGKASAN ANGGARAN {} {}".format(NAMA_BULAN[mo].upper(), y))
    L.append("Budget: {} (dibaca read-only)".format(nama_budget(p.parent)))
    L.append("Jenis anggaran: {}".format("amplop (envelope)" if h["jenis"] == "envelope" else "pelacakan (tracking)"))
    if h["mata_uang"] and h["mata_uang"].upper() != "IDR":
        L.append("PERHATIAN: mata uang budget tercatat {}; angka ditampilkan dengan format Rupiah.".format(h["mata_uang"]))
    if not h["ada_transaksi"]:
        L.append("Catatan: belum ada transaksi di bulan ini (mutasi belum diimpor?).")
    L.append("")
    L.append("- Pemasukan bulan ini: {}".format(rp(dari_sen(h["total_pemasukan"]))))
    L.append("- Total dianggarkan: {}".format(rp(dari_sen(h["total_anggaran"]))))
    L.append("- Total terpakai: {}".format(rp(dari_sen(h["total_terpakai"]))))
    if h["siap_dianggarkan"] is not None:
        v = h["siap_dianggarkan"]
        if v >= 0:
            L.append("- Siap dianggarkan (To Budget): {}".format(rp(dari_sen(v))))
        else:
            L.append("- Siap dianggarkan (To Budget): MINUS {} (anggaran melebihi uang yang ada)".format(rp(dari_sen(-v))))
    if h["ditahan"] and h["jenis"] == "envelope":
        L.append("- Ditahan untuk bulan depan (Hold): {} (sudah dikurangkan dari To Budget di atas)".format(
            rp(dari_sen(h["ditahan"]))))
    if h.get("ditahan_lalu") and h["jenis"] == "envelope":
        L.append("- Dana yang ditahan bulan lalu dan masuk ke bulan ini: {}".format(rp(dari_sen(h["ditahan_lalu"]))))
    if h["overspent_lalu"] and h["jenis"] == "envelope":
        L.append("- Kelebihan belanja bulan lalu yang memotong bulan ini: {}".format(rp(dari_sen(-h["overspent_lalu"]))))
    L.append("")
    if jebol:
        L.append("KATEGORI JEBOL ({}):".format(len(jebol)))
        for x in sorted(jebol, key=lambda x: x["sisa"]):
            L.append("- {}: minus {} (anggaran {}, terpakai {}{})".format(
                x["kategori"], rp(dari_sen(-x["sisa"])), rp(dari_sen(x["anggaran"])), rp(dari_sen(x["terpakai"])),
                ", bawaan bulan lalu " + rp_kata(dari_sen(x["bawaan"])) if x["bawaan"] else ""))
        if h["jenis"] == "envelope":
            L.append("  Saran: tutup dari kategori yang masih bersisa, atau kurangi anggaran bulan depan.")
    else:
        L.append("KATEGORI JEBOL: tidak ada.")
    L.append("")
    L.append("SISA ANGGARAN PER KATEGORI:")
    grup = OrderedDict()
    for x in aktif:
        grup.setdefault(x["grup"] or "(tanpa grup)", []).append(x)
    for g, isi in grup.items():
        L.append("[{}]".format(g))
        for x in isi:
            tanda = " (JEBOL)" if x["sisa"] < 0 else ""
            sembunyi = " (disembunyikan)" if x["tersembunyi"] else ""
            L.append("- {}{}: sisa {}{} | anggaran {}, terpakai {}".format(
                x["kategori"], sembunyi, rp_kata(dari_sen(x["sisa"])), tanda, rp(dari_sen(x["anggaran"])),
                rp(dari_sen(x["terpakai"]))))
    if not aktif:
        L.append("- (belum ada anggaran atau pengeluaran bulan ini)")
    L.append("")
    L.append("PENGELUARAN TERBESAR:")
    for i, x in enumerate(h["terbesar"][:a.top], 1):
        tg = str(x["tanggal"])
        L.append("{}. {} {} - {} - {} ({})".format(i, int(tg[6:]), NAMA_BULAN[int(tg[4:6])][:3], x["payee"],
                                                  rp(dari_sen(x["jumlah"])), x["kategori"]))
    if not h["terbesar"]:
        L.append("- (tidak ada)")
    tk = h["tanpa_kategori"]
    if tk["jumlah_baris"]:
        L.append("")
        L.append("PERLU DICEK: {} transaksi belum berkategori (bersih {} {}). Beri kategori di Actual agar sisa "
                 "anggaran akurat.".format(tk["jumlah_baris"], rp(dari_sen(abs(tk["total"]))),
                                           "keluar" if tk["total"] < 0 else "masuk"))
    L.append("")
    L.append("Sumber: {} | Dihitung ulang dari db.sqlite dengan rumus Actual {}; bila beda dengan layar Actual, "
             "yang benar adalah layar Actual.".format(p.name, ACTUAL_DIUJI))
    if h["jenis"] == "tracking":
        L.append("Catatan: mode pelacakan (tracking) - sisa tidak dibawa ke bulan berikutnya kecuali opsi "
                 "'rollover' kategori itu dinyalakan di Actual.")
    print("\n".join(L))
    return K_OK


def cmd_kategori(a):
    con, p = buka_db(a.db)
    kat = [k for k in daftar_kategori(con) if not k["tombstone"]]
    con.close()
    if a.json:
        print(json.dumps([{"grup": k["grup"], "kategori": k["nama"], "pemasukan": k["is_income"],
                           "disembunyikan": k["hidden"]} for k in kat], ensure_ascii=False, indent=2))
        return K_OK
    print("KATEGORI DI BUDGET: {}".format(nama_budget(p.parent)))
    grup = OrderedDict()
    for k in kat:
        grup.setdefault((k["is_income"], k["grup"]), []).append(k)
    for (inc, g), isi in grup.items():
        print("[{}]{}".format(g, " (pemasukan)" if inc else ""))
        for k in isi:
            print("- {}{}".format(k["nama"], " (disembunyikan)" if k["hidden"] else ""))
    print("Nama harus ditulis SAMA PERSIS saat impor CSV (huruf besar/kecil diperhatikan).")
    return K_OK


def cmd_cek(a):
    con, p = buka_db(a.db)
    akun, payee, trx = muat_data(con)
    kat = [k for k in daftar_kategori(con) if not k["tombstone"]]
    jenis = pref(con, "budgetType") or "envelope"
    mu = pref(con, "defaultCurrencyCode")
    con.close()
    hidup = [x for x in akun.values() if not x["tombstone"]]
    L = ["CEK FILE BUDGET ACTUAL (read-only)", "File: {}".format(p), "Nama budget: {}".format(nama_budget(p.parent)),
         "Jenis anggaran: {}".format("amplop (envelope)" if jenis != "tracking" and jenis != "report" else "pelacakan (tracking)"),
         "Mata uang: {}".format(mu or "(tidak diatur; dianggap Rupiah)"),
         "Rekening: {}".format(", ".join("{}{}{}".format(x["name"], " [di luar anggaran]" if x["offbudget"] else "",
                                                          " [ditutup]" if x["closed"] else "") for x in hidup) or "-"),
         "Kategori aktif: {} ({} pemasukan)".format(len(kat), sum(1 for k in kat if k["is_income"])),
         "Transaksi: {}".format(len(trx))]
    if trx:
        tg = sorted(int(t["tanggal"]) for t in trx)
        f = lambda n: "{}-{:02d}-{:02d}".format(n // 10000, n // 100 % 100, n % 100)
        L.append("Rentang tanggal: {} s.d. {}".format(f(tg[0]), f(tg[-1])))
    L.append("Status: OK - struktur cocok dengan Actual {} (jumlah uang disimpan dalam sen).".format(ACTUAL_DIUJI))
    print("\n".join(L))
    return K_OK


def folder_data_bawaan():
    home = Path.home()
    calon = [home / "Documents" / "Actual", home / "Dokumen" / "Actual", home / "My Documents" / "Actual"]
    up = os.environ.get("USERPROFILE")
    if up:
        calon.append(Path(up) / "Documents" / "Actual")
    one = os.environ.get("OneDrive")
    if one:
        calon.append(Path(one) / "Documents" / "Actual")
    return calon


def cmd_cari(a):
    folder = [Path(os.path.expanduser(a.folder))] if a.folder else folder_data_bawaan()
    temu = []
    for f in folder:
        if f.is_dir():
            for db in sorted(f.glob("*/db.sqlite")):
                temu.append((db, nama_budget(db.parent)))
    if not temu:
        print("Tidak ada budget Actual di: " + "; ".join(str(f) for f in folder))
        print("Cek lokasi di Actual: Settings (dari daftar budget) -> 'Actual's data directory', lalu jalankan "
              "'cari --folder <lokasi>'. Versi web/server menyimpan data di browser/server, bukan file lokal.")
        return K_FILE
    print("BUDGET ACTUAL DITEMUKAN:")
    for db, nama in temu:
        print("- {} -> {}".format(nama, db))
    return K_OK


def main(argv=None):
    ap = argparse.ArgumentParser(description="Asisten Actual Budget lokal (Komunitech, v{})".format(VERSI), allow_abbrev=False)
    sub = ap.add_subparsers(dest="cmd")
    s = sub.add_parser("konversi", help="mutasi bank CSV -> CSV impor Actual", allow_abbrev=False)
    s.add_argument("mutasi")
    s.add_argument("--bank", help="BCA, BRI, MANDIRI, BNI, LAIN (opsional; kolom dideteksi otomatis)")
    s.add_argument("--tahun", type=int, help="tahun untuk tanggal tanpa tahun (mis. BCA '01/09')")
    s.add_argument("--desimal", help="koma (1.500.000,00) | titik (1,500,000.00)")
    s.add_argument("--db", help="db.sqlite / folder budget: cocokkan nama kategori (read-only)")
    s.add_argument("--peta", help="CSV aturan sendiri: kata_kunci,kategori[,masuk|keluar]")
    s.add_argument("--keluaran", help="nama file hasil (default: <mutasi>-actual.csv)")
    s.add_argument("--timpa", action="store_true", help="boleh menimpa file hasil yang sudah ada")
    s.add_argument("--tanpa-tanda-masuk", action="store_true", help="angka positif tanpa CR/DB = uang masuk")
    s.add_argument("--json", action="store_true")
    for nama, bantu in (("cek", "periksa file budget"), ("kategori", "daftar kategori"),
                        ("ringkasan", "ringkasan bulanan")):
        s = sub.add_parser(nama, help=bantu, allow_abbrev=False)
        s.add_argument("--db", required=True, help="path db.sqlite atau folder budget Actual")
        s.add_argument("--json", action="store_true")
        if nama == "ringkasan":
            s.add_argument("--bulan", default="ini", help="2026-09 | 09/2026 | 'September 2026' | ini | lalu")
            s.add_argument("--top", type=int, default=5, help="jumlah pengeluaran terbesar (default 5)")
    s = sub.add_parser("cari", help="cari budget Actual di folder data", allow_abbrev=False)
    s.add_argument("--folder")
    a = ap.parse_args(argv)
    if not a.cmd:
        ap.print_help()
        return K_INPUT
    try:
        return {"konversi": cmd_konversi, "cek": cmd_cek, "kategori": cmd_kategori,
                "ringkasan": cmd_ringkasan, "cari": cmd_cari}[a.cmd](a)
    except Gagal as g:
        print("GAGAL: {}".format(g), file=sys.stderr)
        return g.kode


if __name__ == "__main__":
    sys.exit(main())
