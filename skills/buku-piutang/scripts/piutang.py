#!/usr/bin/env python3
"""buku-piutang (Komunitech) - buku piutang pelanggan yang jalan lokal.

Satu file database SQLite di komputer pemilik usaha. Hanya library standar Python 3.8+, lintas OS
(Windows: `python`/`py`), TANPA akses jaringan: script tidak pernah mengirim apa pun. Pesan tagihan hanya
disiapkan sebagai DRAF (+ tautan wa.me bila nomor ada); manusia yang memeriksa dan menekan Kirim.

Lokasi database (urutan prioritas):
  1. --db PATH (ditulis setelah nama perintah)
  2. ENV KOMUNITECH_PIUTANG_DB  (path file lengkap)
  3. ENV KOMUNITECH_DATA        (folder) + /piutang/piutang.db
  4. ~/KomunitechData/piutang/piutang.db
Cadangan: folder backup-piutang/ di sebelah database (otomatis sekali sehari saat ada perubahan, dan sebelum
setiap perubahan besar).

Uang selalu integer rupiah. Setiap perubahan diperiksa: sisa nota dan kelebihan bayar pelanggan tidak pernah
boleh negatif (jika terjadi, transaksi dibatalkan seluruhnya).

Perubahan kecil (tambah-pelanggan, ubah-pelanggan, catat, bayar, pakai-kredit, kembalikan, ubah-nota, terkirim,
atur) langsung tersimpan. Perubahan besar (init, impor, potong, batal-nota, batal-bayar, hapus-pelanggan, restore)
hanya PRATINJAU sampai diberi --ya.

Contoh:
  python3 piutang.py init --nama-usaha "Toko Berkah" --pengirim Sari --rekening "BCA 1234567890 a.n. Sari" --ya
  python3 piutang.py catat --pelanggan "Toko Maju" --nota INV-001 --tanggal 01/09/2026 --termin 14 --nominal 2,5jt
  python3 piutang.py bayar --pelanggan "Toko Maju" --jumlah 1jt --metode transfer
  python3 piutang.py jatuh-tempo
  python3 piutang.py umur
  python3 piutang.py draf --pelanggan "Toko Maju"
  python3 piutang.py rekap --periode bulan-ini --json

Kode keluar: 0 = berhasil; 1 = gagal (pesan jelas di "error"/stderr); 2 = perintah salah tulis.
"""
import argparse
import csv
import difflib
import io
import json
import os
import re
import sqlite3
import sys
from datetime import date, datetime, timedelta, timezone
from decimal import ROUND_HALF_UP, Decimal
from fractions import Fraction
from pathlib import Path
from urllib.parse import quote

APLIKASI = "buku-piutang"
VERSI = "1.0.0"
SKEMA = 1
SKEMA_JSON_REKAP = 1
SIMPAN_BACKUP_HARIAN = 30
TERMIN_DEFAULT = 30
MAKS_TERMIN = 366
BATAS_TANPA_TAHUN = 180        # hari; tanggal tanpa tahun yang lebih jauh dari ini ditolak (minta tahun)
MAKS_BARIS = 20
MAKS_NOMINAL = 10 ** 12        # Rp 1 triliun: di atas ini hampir pasti salah ketik
UMUR = [("belum_jatuh_tempo", "Belum jatuh tempo"), ("1_30", "1-30 hari"), ("31_60", "31-60 hari"),
        ("61_90", "61-90 hari"), ("lebih_90", ">90 hari")]
LABEL_UMUR = dict(UMUR)
ZONA = {"WIB": ("Asia/Jakarta", 7), "WITA": ("Asia/Makassar", 8), "WIT": ("Asia/Jayapura", 9)}
ALIAS_ZONA = {"wib": "WIB", "asia/jakarta": "WIB", "asia/pontianak": "WIB", "wita": "WITA",
              "asia/makassar": "WITA", "wit": "WIT", "asia/jayapura": "WIT"}
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober",
         "November", "Desember"]
BLN = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
NAMA_BULAN = {}
for _i, _al in enumerate([("jan", "januari", "january"), ("feb", "februari", "pebruari", "february"),
                          ("mar", "maret", "march"), ("apr", "april"), ("mei", "may"), ("jun", "juni", "june"),
                          ("jul", "juli", "july"), ("agu", "agt", "ags", "agus", "agustus", "aug", "august"),
                          ("sep", "sept", "september"), ("okt", "oktober", "oct", "october"),
                          ("nov", "nop", "november", "nopember"), ("des", "desember", "dec", "december")], 1):
    for _a in _al:
        NAMA_BULAN[_a] = _i
SAPAAN_DIKENAL = {"bu", "ibu", "pak", "bapak", "kak", "ka", "kakak", "mas", "mbak", "mba", "bang", "abang", "om",
                  "tante", "cik", "ci", "ko", "koh", "sdr", "sdri", "dr", "drg", "hj", "haji", "teh", "aa", "uda",
                  "uni", "cak", "bli", "mbok", "bunda", "ustadz", "kang", "neng", "ny", "tn"}
AWALAN_LEMBAGA = {"pt", "cv", "ud", "toko", "tk", "koperasi", "kop", "yayasan", "rs", "klinik", "sekolah", "hotel",
                  "resto", "restoran", "warung", "kafe", "cafe", "kantor", "dinas", "universitas", "smk", "sma",
                  "smp", "sd", "tk", "paud", "bengkel", "apotek", "salon", "katering", "catering", "kios", "agen"}
DISCLAIMER_PRIVASI = ("Nama, nomor HP, dan utang pelanggan adalah data pribadi (UU 27/2022 PDP): simpan di komputer "
                      "ini, jangan dibagikan ke grup atau media sosial.")
CATATAN_PAJAK = ("PPN dihitung dari DPP persis lalu dibulatkan ke bawah sekali (tidak pernah melebihi tarif). "
                 "Pembulatan ini belum dicocokkan dengan Coretax; faktur pajak resmi tetap mengikuti Coretax.")


class Gagal(Exception):
    """Error yang pesannya aman ditampilkan ke pengguna."""

    def __init__(self, pesan, **detail):
        super().__init__(pesan)
        self.pesan = pesan
        self.detail = detail


def _timeout():
    try:
        return max(0.1, float(os.environ.get("KOMUNITECH_PIUTANG_TIMEOUT", "15")))
    except ValueError:
        return 15.0


def _detik():
    return ("%.1f" % _timeout()).rstrip("0").rstrip(".").replace(".", ",")


SARAN_PULIH = ("Pulihkan: piutang.py backup --daftar (lihat cadangan), lalu piutang.py restore --dari <file cadangan> "
               "(pratinjau, lalu --ya); file rusak otomatis dipindah ke folder backup-piutang, tidak dihapus. Belum ada "
               "cadangan? piutang.py init --mulai-baru (pratinjau, lalu --ya) untuk database kosong baru.")
PESAN_TERKUNCI = ("Database piutang sedang dipakai program lain (mis. jadwal OpenClaw atau jendela lain) dan tidak "
                  "selesai dalam %s detik. Data aman, tidak rusak. Tunggu sebentar lalu ulangi perintah yang sama. "
                  "Jangan hapus file database.")


def _terkunci(e):
    s = str(e).lower()
    return "locked" in s or "busy" in s


# --------------------------------------------------------------------------- waktu
_JAM = {"kini": None, "zona": "WIB"}


def kode_zona(teks):
    k = ALIAS_ZONA.get(str(teks or "").strip().lower())
    if not k:
        raise Gagal("Zona waktu '%s' tidak dikenal. Pakai WIB, WITA, atau WIT." % teks)
    return k


def waktu_lokal(zona="WIB", utc_now=None):
    """Jam lokal (naive) di zona Indonesia (tanpa jam musim panas, offset tetap)."""
    u = utc_now or datetime.now(timezone.utc)
    return u.astimezone(timezone(timedelta(hours=ZONA[zona][1]))).replace(tzinfo=None, microsecond=0)


def kini():
    return _JAM["kini"] or waktu_lokal(_JAM["zona"])


def hari_ini():
    return kini().date()


def stempel():
    return kini().isoformat(" ", "seconds")


def tgl_panjang(d):
    if isinstance(d, str):
        d = date.fromisoformat(d[:10])
    return "%s, %d %s %d" % (HARI[d.weekday()], d.day, BULAN[d.month - 1], d.year)


def tgl_pendek(d, tahun=True):
    if isinstance(d, str):
        d = date.fromisoformat(d[:10])
    return ("%d %s %d" % (d.day, BLN[d.month - 1], d.year)) if tahun else ("%d %s" % (d.day, BLN[d.month - 1]))


def _tambah_bulan(d, n):
    m = d.month - 1 + n
    y, m = d.year + m // 12, m % 12 + 1
    kabisat = y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)
    hari = min(d.day, [31, 29 if kabisat else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1])
    return date(y, m, hari)


def _buat_tgl(y, m, d, asli, urutan="hari-bulan"):
    if not 2000 <= y <= 2100:
        raise Gagal("Tahun %d pada tanggal '%s' tidak wajar. Tulis tanggal lengkap hari/bulan/tahun, mis. "
                    "26/09/2026." % (y, asli), tanggal_salah=True)
    try:
        return date(y, m, d)
    except ValueError:
        pesan = "Tanggal '%s' tidak ada di kalender." % asli
        if urutan == "hari-bulan" and m > 12 and d <= 12:
            try:
                date(y, d, m)
                pesan += (" Sepertinya ditulis bulan/hari (gaya Amerika). Buku ini memakai hari/bulan/tahun: "
                          "maksudnya %02d/%02d/%d?" % (m, d, y))
            except ValueError:
                pass
        raise Gagal(pesan, tanggal_salah=True, mungkin_bulan_hari=(m > 12 and d <= 12))


def _tanpa_tahun(h, b, acuan, arah, asli):
    tahun = [acuan.year]
    if arah == "lalu":
        tahun.append(acuan.year - 1)
    elif arah == "depan":
        tahun.append(acuan.year + 1)
    else:
        tahun += [acuan.year - 1, acuan.year + 1]
    kand = []
    for y in tahun:
        try:
            kand.append(date(y, b, h))
        except ValueError:
            continue
    if not kand:
        raise Gagal("Tanggal '%s' tidak ada di kalender." % asli, tanggal_salah=True)
    if arah == "lalu":
        kand = [c for c in kand if c <= acuan]
    elif arah == "depan":
        kand = [c for c in kand if c >= acuan]
    c = min(kand, key=lambda x: abs((x - acuan).days)) if kand else None
    if c is None or abs((c - acuan).days) > BATAS_TANPA_TAHUN:
        raise Gagal("Tanggal '%s' tanpa tahun tidak jelas (bisa tahun ini atau tahun lain). Tulis lengkap, mis. "
                    "%d/%d/%d." % (asli, h, b, acuan.year), tanggal_salah=True)
    return c, ["'%s' dibaca %s (tahun tidak disebut)." % (asli, tgl_pendek(c))]


POLA_JAM = r"(?:[ tT]+\d{1,2}[:.]\d{2}(?:[:.]\d{2})?(?:\.\d+)?(?: ?[ap]m)?)?"


def baca_tgl(teks, acuan, arah="bebas", urutan="hari-bulan", hari=None):
    """Kembalikan (date, [catatan]).

    Format Indonesia hari/bulan/tahun: 26/09/2026, 26-09-2026, 26.09.2026, 26/9/26, 26 Sep 2026, 26-Sep-2026,
    ISO 2026-09-26 (juga dengan jam). Kata: hari ini, kemarin, besok, lusa, "3 hari lalu".
    Tanpa tahun (26/9, 26 Sep) hanya bila jelas (<= 180 hari dari acuan sesuai arah).
    urutan='bulan-hari' hanya untuk file impor yang dipastikan berformat Amerika.
    Ditolak: tanggal yang tidak ada, tahun < 2000 / > 2100, angka seri Excel, format lain.
    """
    hari = hari or hari_ini()
    if teks is None or not str(teks).strip():
        raise Gagal("Tanggal kosong.", tanggal_salah=True)
    asli = str(teks).strip()
    s = re.sub(r"\s+", " ", asli.lower().replace(",", " ")).strip()
    rel = {"hari ini": 0, "hr ini": 0, "sekarang": 0, "today": 0, "besok": 1, "bsk": 1, "lusa": 2,
           "kemarin": -1, "kmrn": -1, "kemaren": -1, "yesterday": -1, "kemarin lusa": -2}
    if s in rel:
        return hari + timedelta(days=rel[s]), []
    m = re.fullmatch(r"(\d{1,3}) ?(hari|hr) ?(yang )?lalu", s)
    if m:
        return hari - timedelta(days=int(m.group(1))), []
    m = re.fullmatch(r"(\d{1,3}) ?(hari|hr) ?lagi", s)
    if m:
        return hari + timedelta(days=int(m.group(1))), []
    s = re.sub(r"^(hari )?(senin|selasa|rabu|kamis|jumat|jum'at|sabtu|minggu|ahad) ", "", s)
    s = re.sub(r"^(tgl\.?|tanggal) ?", "", s).strip()
    if re.fullmatch(r"\d{5}(\.0+)?", s):
        raise Gagal("Tanggal '%s' berupa angka seri Excel, bukan tanggal. Di Excel, format kolom tanggal sebagai "
                    "Tanggal (dd/mm/yyyy) lalu simpan ulang." % asli, tanggal_salah=True)
    m = re.fullmatch(r"(\d{4})[-/](\d{1,2})[-/](\d{1,2})" + POLA_JAM, s)
    if m:
        return _buat_tgl(int(m.group(1)), int(m.group(2)), int(m.group(3)), asli, "iso"), []
    m = re.fullmatch(r"(\d{1,2})[/.-](\d{1,2})[/.-](\d{4}|\d{2})" + POLA_JAM, s)
    if m:
        a, b, y = int(m.group(1)), int(m.group(2)), m.group(3)
        catatan = []
        if len(y) == 2:
            y = 2000 + int(y)
            catatan.append("Tahun '%s' ditulis 2 angka; dibaca %d." % (asli, y))
        else:
            y = int(y)
        if urutan == "bulan-hari":
            a, b = b, a
        return _buat_tgl(y, b, a, asli, urutan), catatan
    m = re.fullmatch(r"(\d{1,2})[/-](\d{1,2})", s)
    if m:
        a, b = int(m.group(1)), int(m.group(2))
        if urutan == "bulan-hari":
            a, b = b, a
        if b > 12:
            _buat_tgl(hari.year, b, a, asli, urutan)   # memberi pesan "tidak ada di kalender" + petunjuk
        return _tanpa_tahun(a, b, acuan, arah, asli)
    m = re.fullmatch(r"(\d{1,2})[ .-]?([a-z]+)\.?(?:[ .-](\d{4}|\d{2}))?" + POLA_JAM, s)
    if m and m.group(2) in NAMA_BULAN:
        h, b = int(m.group(1)), NAMA_BULAN[m.group(2)]
        if m.group(3):
            y = int(m.group(3))
            catatan = []
            if y < 100:
                y += 2000
                catatan.append("Tahun '%s' ditulis 2 angka; dibaca %d." % (asli, y))
            return _buat_tgl(y, b, h, asli), catatan
        return _tanpa_tahun(h, b, acuan, arah, asli)
    raise Gagal("Tanggal '%s' tidak dikenali. Pakai format hari/bulan/tahun, mis. 26/09/2026, 26 Sep 2026, atau "
                "2026-09-26; kata 'hari ini', 'kemarin', 'besok' juga bisa." % asli, tanggal_salah=True)


def tgl_nota(teks, hari):
    """Tanggal nota/transaksi: hari ini atau sebelumnya."""
    if not teks:
        return hari, []
    d, cat = baca_tgl(teks, hari, "lalu", hari=hari)
    if d > hari:
        raise Gagal("Tanggal '%s' (%s) ada di masa depan. Tanggal nota/pembayaran harus hari ini atau sebelumnya."
                    % (teks, tgl_pendek(d)), tanggal_salah=True)
    if (hari - d).days > 3 * 366:
        cat.append("Tanggal %s lebih dari 3 tahun lalu; pastikan benar." % tgl_pendek(d))
    return d, cat


def baca_termin(teks):
    """'30', '30 hari', '+30', 'net 30' -> 30. None bila bukan termin."""
    m = re.fullmatch(r"(?i)\s*(?:\+|net\s*|n/)?\s*(\d{1,3})\s*(hari|hr|h|days?)?\s*", str(teks or ""))
    return int(m.group(1)) if m else None


def tentukan_jatuh_tempo(args_jt, args_termin, tanggal, cfg, hari):
    """Kembalikan (date jatuh tempo, termin_hari, [catatan])."""
    catatan = []
    if args_jt and args_termin is not None:
        raise Gagal("Isi salah satu saja: --jatuh-tempo atau --termin.")
    termin = None
    if args_termin is not None:
        termin = baca_termin(args_termin)
        if termin is None:
            raise Gagal("--termin harus jumlah hari, mis. 30.")
    elif args_jt:
        termin = baca_termin(args_jt)
        if termin is not None and not re.fullmatch(r"\s*\d{1,3}\s*", str(args_jt)):
            catatan.append("Jatuh tempo '%s' dibaca %d hari dari tanggal nota." % (args_jt, termin))
        elif termin is not None:
            raise Gagal("Jatuh tempo '%s' tidak jelas: tanggal atau jumlah hari? Tulis mis. '30 hari' atau "
                        "tanggal lengkap 26/10/2026." % args_jt, tanggal_salah=True)
    if termin is None and args_jt:
        jt, cat = baca_tgl(args_jt, tanggal, "depan", hari=hari)
        catatan += cat
    else:
        if termin is None:
            try:
                termin = int(cfg.get("termin") or TERMIN_DEFAULT)
            except ValueError:
                termin = TERMIN_DEFAULT
            catatan.append("Jatuh tempo belum disebut; dipakai termin %d hari dari tanggal nota." % termin)
        if termin > MAKS_TERMIN:
            raise Gagal("Termin %d hari tidak wajar (maks. %d)." % (termin, MAKS_TERMIN))
        jt = tanggal + timedelta(days=termin)
    if jt < tanggal:
        raise Gagal("Jatuh tempo %s lebih awal dari tanggal nota %s. Periksa lagi." % (tgl_pendek(jt),
                                                                                     tgl_pendek(tanggal)),
                    tanggal_salah=True)
    if (jt - tanggal).days > MAKS_TERMIN:
        catatan.append("Jatuh tempo %s lebih dari setahun setelah tanggal nota; pastikan benar." % tgl_pendek(jt))
    return jt, (jt - tanggal).days, catatan


def parse_hari_ini(teks):
    s = str(teks).strip()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(s, fmt)
            return dt if fmt != "%Y-%m-%d" else dt.replace(hour=9)
        except ValueError:
            continue
    raise Gagal("--hari-ini harus berformat YYYY-MM-DD atau 'YYYY-MM-DD HH:MM'.")


# --------------------------------------------------------------------------- rupiah
def rp(n):
    if n is None:
        return "-"
    n = int(n)
    return ("-" if n < 0 else "") + "Rp " + "{:,}".format(abs(n)).replace(",", ".")


def bulat(x):
    """Rupiah terdekat, setengah ke atas (0,5 -> 1). Menerima int/Decimal/Fraction."""
    d = Decimal(x.numerator) / Decimal(x.denominator) if isinstance(x, Fraction) else Decimal(x)
    return int(d.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def persen(pembilang, penyebut):
    if not penyebut:
        return None, "-"
    f = Fraction(pembilang * 100, penyebut)
    d = (Decimal(f.numerator) / Decimal(f.denominator)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    return float(d), ("%s%%" % d).replace(".", ",")


SATUAN = {"rb": 1000, "ribu": 1000, "rbu": 1000, "k": 1000, "jt": 10 ** 6, "juta": 10 ** 6, "jeti": 10 ** 6,
          "miliar": 10 ** 9, "milyar": 10 ** 9, "M": 10 ** 9}


def parse_rupiah(teks, nama="Nominal"):
    """'2,5 jt' | '2.500.000' | 'Rp2.500.000,-' | '750rb' | '2 jt 500 rb' | '1.234.567,50' -> (int, [catatan]).

    Pecahan sen dibulatkan ke rupiah terdekat (0,5 ke atas) dan disebut di catatan. Nilai ambigu ditolak.
    """
    if teks is None or not str(teks).strip():
        raise Gagal("%s kosong." % nama)
    asli = str(teks).strip()
    s = re.sub(r"(?i)^\s*(rp\.?|idr)\s*", "", asli).strip()
    s = re.sub(r"(?i)\s*(,-|\.-)$", "", s).strip()
    if s.startswith("-") or s.startswith("("):
        raise Gagal("%s '%s' tidak boleh negatif. Pembayaran dicatat dengan perintah bayar; pengurangan tagihan "
                    "(retur/diskon) dengan perintah potong." % (nama, asli))
    bagian = re.findall(r"(\d[\d.,]*)\s*([A-Za-z]+)?\s*", s)
    if not bagian or re.sub(r"(\d[\d.,]*)\s*([A-Za-z]+)?\s*", "", s).strip(" dan&+"):
        raise Gagal("%s '%s' tidak dikenali. Contoh: 750rb, 2,5 jt, 2.500.000." % (nama, asli))
    total = Decimal(0)
    for angka, sat in bagian:
        if sat == "m":
            raise Gagal("%s '%s' ambigu: 'm' itu juta atau miliar? Tulis 'jt' atau 'miliar'." % (nama, asli))
        if sat and sat not in SATUAN and sat.lower() not in SATUAN:
            raise Gagal("Satuan '%s' pada '%s' tidak dikenal. Pakai rb, jt, atau miliar." % (sat, asli))
        kali = SATUAN.get(sat, SATUAN.get((sat or "").lower(), 1)) if sat else 1
        if len(bagian) > 1 and not sat:
            raise Gagal("%s '%s' ambigu: bagian '%s' tidak bersatuan. Tulis mis. '2 jt 500 rb'." % (nama, asli, angka))
        if not sat:
            angka = re.sub(r"(?<=\d{4})[.,]0{1,2}$|(?<=\d{3}[.,]\d{3})[.,]0{1,2}$", "", angka)
        if not re.search(r"[.,]", angka):
            nilai = Decimal(angka)
        elif sat:
            m = re.fullmatch(r"(\d+),(\d{1,3})", angka) or re.fullmatch(r"(\d+)\.(\d{1,2})", angka)
            if not m:
                raise Gagal("%s '%s' ambigu (mis. '1.500 jt' = 1,5 juta atau 1.500 juta?). Tulis mis. '1,5 jt' atau "
                            "'1500000'." % (nama, asli))
            nilai = Decimal(m.group(1) + "." + m.group(2))
        elif re.fullmatch(r"\d{1,3}(\.\d{3})+|\d{1,3}(,\d{3})+", angka):
            nilai = Decimal(re.sub(r"[.,]", "", angka))
        elif re.fullmatch(r"\d{1,3}(\.\d{3})+,\d{1,2}|\d{4,},\d{1,2}", angka):          # 1.234.567,50
            nilai = Decimal(angka.replace(".", "").replace(",", "."))
        elif re.fullmatch(r"\d{1,3}(,\d{3})+\.\d{1,2}|\d{4,}\.\d{1,2}", angka):         # 1,234,567.50
            nilai = Decimal(angka.replace(",", ""))
        else:
            raise Gagal("%s '%s' ambigu. Tulis mis. '2,5 jt', '750rb', atau '2.500.000'." % (nama, asli))
        total += nilai * kali
    catatan = []
    if total != total.to_integral_value():
        b = bulat(total)
        catatan.append("%s '%s' berisi pecahan sen; dibulatkan ke rupiah terdekat: %s." % (nama, asli, rp(b)))
        total = Decimal(b)
    if total <= 0:
        raise Gagal("%s '%s' harus lebih dari nol." % (nama, asli))
    if total >= MAKS_NOMINAL:
        raise Gagal("%s '%s' (%s) tidak wajar; kemungkinan salah ketik." % (nama, asli, rp(int(total))))
    return int(total), catatan


def hitung_ppn(dpp, tarif_teks):
    """PPN atas DPP (belum termasuk PPN), dibulatkan ke BAWAH sekali. '11' = 12% x DPP nilai lain 11/12
    (barang/jasa umum, efektif 11%); '12' = 12% penuh (barang mewah)."""
    t = str(tarif_teks or "").strip().replace("%", "").replace(",", ".")
    if t not in ("11", "12"):
        raise Gagal("--ppn hanya 11 (12%% x DPP nilai lain 11/12, barang/jasa umum) atau 12 (barang mewah). "
                    "Isian: '%s'." % tarif_teks)
    tarif = Fraction(11, 100) if t == "11" else Fraction(12, 100)
    ppn = int((Fraction(dpp) * tarif) // 1)      # floor, pecahan persis
    ket = ("PPN 12%% x DPP nilai lain 11/12 = %s (efektif 11%%, dibulatkan ke bawah)" % rp(ppn) if t == "11" else
           "PPN 12%% = %s (dibulatkan ke bawah)" % rp(ppn))
    return ppn, ket


# --------------------------------------------------------------------------- nomor WA & nama
def normalisasi_wa(teks):
    """Kembalikan (nomor '62...', [peringatan]). Menolak nomor yang tidak wajar."""
    asli = str(teks or "").strip()
    if not asli:
        raise Gagal("Nomor WA kosong.")
    if re.search(r"\d[.,]\d+\s*e\+?\d+", asli, re.I):
        raise Gagal("Nomor '%s' rusak: Excel mengubahnya menjadi angka ilmiah. Format kolom nomor sebagai Teks lalu "
                    "ekspor ulang." % asli)
    s = re.sub(r"(?i)^(no\.?|nomor|hp|wa|whatsapp|telp\.?|tel|phone)\s*[:.]?\s*", "", asli)
    potong = [p for p in re.split(r"\s*(?:/|,|;|\batau\b|\bdan\b|&)\s*", s) if re.sub(r"\D", "", p)]
    if len(potong) > 1 and all(len(re.sub(r"\D", "", p)) >= 8 for p in potong):
        raise Gagal("Ada lebih dari satu nomor di '%s'. Simpan satu nomor WA saja per pelanggan." % asli)
    if re.search(r"[A-Za-z]", s):
        raise Gagal("Nomor '%s' berisi huruf. Tulis angkanya saja, mis. 0812-0000-1234." % asli)
    plus = s.startswith("+")
    d = re.sub(r"\D", "", s)
    peringatan = []
    if d.startswith("00"):
        d, plus = d[2:], True
    if d.startswith("62"):
        pass
    elif d.startswith("0"):
        d = "62" + d[1:]
    elif d.startswith("8") and not plus:
        d = "62" + d
    elif plus:
        if not 8 <= len(d) <= 15:
            raise Gagal("Nomor luar negeri '%s' tidak wajar (%d digit)." % (asli, len(d)))
        return d, ["Nomor %s bukan nomor Indonesia; pastikan kode negaranya benar." % asli]
    else:
        raise Gagal("Nomor '%s' tidak dikenali. Nomor Indonesia diawali 08, 62, atau +62." % asli)
    sisa = d[2:].lstrip("0")
    d = "62" + sisa
    if not 9 <= len(sisa) <= 12:
        raise Gagal("Nomor '%s' tidak wajar: %d digit setelah 62 (nomor HP Indonesia 9-12 digit)." % (asli, len(sisa)))
    if not sisa.startswith("8"):
        peringatan.append("Nomor %s bukan nomor HP (mungkin telepon kantor); pastikan memakai WhatsApp." % tampil_wa(d))
    return d, peringatan


def tampil_wa(wa):
    if not wa:
        return "-"
    if wa.startswith("628"):
        lok = "0" + wa[2:]
        return "%s-%s-%s" % (lok[:4], lok[4:-4], lok[-4:]) if len(lok) >= 10 else lok
    if wa.startswith("62"):
        return "0" + wa[2:]
    return "+" + wa


def samar_wa(wa):
    if not wa:
        return "-"
    lok = ("0" + wa[2:]) if wa.startswith("62") else ("+" + wa)
    return lok[:4] + "-****-" + lok[-4:] if len(lok) >= 9 else "****"


def samar_nama(nama):
    kata = (nama or "").split()
    if not kata:
        return "-"
    depan = []
    while kata and kata[0].lower().rstrip(".") in (SAPAAN_DIKENAL | AWALAN_LEMBAGA) and len(depan) < 2:
        depan.append(kata.pop(0))
    depan += [k[0].upper() + "." for k in kata[:2]]
    return " ".join(depan)


def link_wa(wa, teks):
    if not wa:
        return None
    return "https://wa.me/%s?text=%s" % (wa, quote(teks, safe=""))


def bersih(teks, maks=200):
    s = re.sub(r"[\x00-\x08\x0b-\x1f\x7f]", " ", str(teks or ""))
    s = re.sub(r"[ \t]+", " ", s).strip()
    return s[:maks]


def kunci_nama(nama):
    kata = re.sub(r"[^\w\s]", " ", (nama or "").lower()).split()
    while len(kata) > 1 and kata[0] in SAPAAN_DIKENAL:
        kata.pop(0)
    return " ".join(kata)


def kunci_nota(no):
    """'INV-001', 'inv 001', 'INV/001' -> 'INV001' (tanda baca & spasi diabaikan agar nota yang sama tidak dobel)."""
    return re.sub(r"[\W_]+", "", str(no or "").upper())


def panggilan(p, cfg):
    nama = bersih(p["nama"], 80)
    kata = nama.split()
    awal = kata[0].lower().rstrip(".") if kata else ""
    if p.get("sapaan"):
        s = p["sapaan"].strip()
        return nama if s.lower() in ("-", "tanpa") else "%s %s" % (s, nama)
    if awal in SAPAAN_DIKENAL:
        return nama
    if awal in AWALAN_LEMBAGA:
        # "Warung Bu Tini" -> "Bu Tini"; "Toko Maju" -> "Bapak/Ibu di Toko Maju"
        for i, k in enumerate(kata[1:3], 1):
            if k.lower().rstrip(".") in SAPAAN_DIKENAL and len(kata) > i + 1:
                return " ".join(kata[i:])
        return "Bapak/Ibu di " + nama
    return "Bapak/Ibu " + nama


# --------------------------------------------------------------------------- database
SKEMA_SQL = """
CREATE TABLE meta(kunci TEXT PRIMARY KEY, nilai TEXT);
CREATE TABLE pelanggan(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nama TEXT NOT NULL,
  sapaan TEXT,
  wa TEXT,
  catatan TEXT NOT NULL DEFAULT '',
  dibuat TEXT NOT NULL,
  diubah TEXT NOT NULL
);
CREATE INDEX pelanggan_wa ON pelanggan(wa);
CREATE TABLE nota(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pelanggan_id INTEGER NOT NULL REFERENCES pelanggan(id),
  no_nota TEXT NOT NULL,
  kunci TEXT NOT NULL UNIQUE,
  tanggal TEXT NOT NULL,
  jatuh_tempo TEXT NOT NULL,
  nominal INTEGER NOT NULL CHECK (nominal > 0),
  dpp INTEGER,
  ppn INTEGER,
  keterangan TEXT NOT NULL DEFAULT '',
  status TEXT NOT NULL DEFAULT 'aktif' CHECK (status IN ('aktif','batal')),
  alasan_batal TEXT,
  tgl_batal TEXT,
  sumber TEXT NOT NULL DEFAULT 'manual',
  diingatkan INTEGER NOT NULL DEFAULT 0,
  terakhir_diingatkan TEXT,
  dibuat TEXT NOT NULL,
  diubah TEXT NOT NULL
);
CREATE INDEX nota_pelanggan ON nota(pelanggan_id);
CREATE TABLE pembayaran(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pelanggan_id INTEGER NOT NULL REFERENCES pelanggan(id),
  tanggal TEXT NOT NULL,
  jumlah INTEGER NOT NULL CHECK (jumlah > 0),
  metode TEXT NOT NULL DEFAULT '',
  catatan TEXT NOT NULL DEFAULT '',
  status TEXT NOT NULL DEFAULT 'aktif' CHECK (status IN ('aktif','batal')),
  alasan_batal TEXT,
  tgl_batal TEXT,
  dibuat TEXT NOT NULL
);
CREATE INDEX bayar_pelanggan ON pembayaran(pelanggan_id);
CREATE TABLE alokasi(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pembayaran_id INTEGER NOT NULL REFERENCES pembayaran(id),
  nota_id INTEGER NOT NULL REFERENCES nota(id),
  tanggal TEXT NOT NULL,
  jumlah INTEGER NOT NULL CHECK (jumlah > 0),
  dibuat TEXT NOT NULL
);
CREATE INDEX alokasi_nota ON alokasi(nota_id);
CREATE TABLE potongan(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nota_id INTEGER NOT NULL REFERENCES nota(id),
  tanggal TEXT NOT NULL,
  jumlah INTEGER NOT NULL CHECK (jumlah > 0),
  alasan TEXT NOT NULL,
  dibuat TEXT NOT NULL
);
CREATE TABLE pengembalian(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pelanggan_id INTEGER NOT NULL REFERENCES pelanggan(id),
  tanggal TEXT NOT NULL,
  jumlah INTEGER NOT NULL CHECK (jumlah > 0),
  catatan TEXT NOT NULL DEFAULT '',
  dibuat TEXT NOT NULL
);
CREATE TABLE log(id INTEGER PRIMARY KEY AUTOINCREMENT, waktu TEXT, perintah TEXT, ringkasan TEXT);
"""
PENGATURAN_DEFAULT = {"nama_usaha": "", "pengirim": "", "rekening": "", "termin": str(TERMIN_DEFAULT), "zona": "WIB"}
TABEL_WAJIB = ("meta", "pelanggan", "nota", "pembayaran", "alokasi", "potongan", "pengembalian")


def path_db(args):
    if getattr(args, "db", None):
        p = Path(args.db).expanduser()
    elif os.environ.get("KOMUNITECH_PIUTANG_DB"):
        p = Path(os.environ["KOMUNITECH_PIUTANG_DB"]).expanduser()
    elif os.environ.get("KOMUNITECH_DATA"):
        p = Path(os.environ["KOMUNITECH_DATA"]).expanduser() / "piutang" / "piutang.db"
    else:
        p = Path.home() / "KomunitechData" / "piutang" / "piutang.db"
    return p.resolve()


def folder_backup(db):
    return db.parent / "backup-piutang"


def buka(db, baca_saja=False):
    if not db.is_file():
        raise Gagal("Database piutang belum ada di %s. Jalankan dulu: piutang.py init (lalu --ya setelah pengguna "
                    "setuju)." % db, db=str(db), belum_ada=True)
    if db.stat().st_size == 0:
        raise Gagal("File %s kosong (0 byte), bukan database yang bisa dibaca. %s" % (db, SARAN_PULIH), rusak=True)

    def sambung(ro):
        try:
            if ro:
                c = sqlite3.connect(db.resolve().as_uri() + "?mode=ro", uri=True, timeout=_timeout(),
                                    isolation_level=None)
            else:
                c = sqlite3.connect(str(db), timeout=_timeout(), isolation_level=None)
        except sqlite3.OperationalError as e:
            raise Gagal("Database %s tidak bisa dibuka (%s). Periksa folder dan izin aksesnya." % (db, e))
        c.row_factory = sqlite3.Row
        return c

    ro = baca_saja
    while True:
        conn = sambung(ro)
        try:
            r = conn.execute("SELECT nilai FROM meta WHERE kunci='aplikasi'").fetchone()
            sk = conn.execute("SELECT nilai FROM meta WHERE kunci='skema'").fetchone()
            break
        except sqlite3.OperationalError as e:
            conn.close()
            pesan = str(e).lower()
            if _terkunci(e):
                raise Gagal(PESAN_TERKUNCI % _detik())
            if ro and "readonly" in pesan:
                ro = False        # journal sisa program terhenti: buka biasa sekali agar SQLite memulihkannya
                continue
            if "no such table" in pesan:
                raise Gagal("File %s bukan database buku-piutang (%s). File itu tidak diubah; periksa --db." % (db, e))
            raise Gagal("Database %s tidak bisa dibaca (%s). Jangan hapus file itu. %s" % (db, e, SARAN_PULIH),
                        rusak=True)
        except sqlite3.DatabaseError:
            conn.close()
            raise Gagal("File %s rusak atau bukan database buku-piutang. Jangan hapus file itu. %s" % (db, SARAN_PULIH),
                        rusak=True)
    if not r or r[0] != APLIKASI:
        conn.close()
        raise Gagal("File %s bukan database buku-piutang. File itu tidak diubah; periksa --db." % db)
    if sk and str(sk[0]).isdigit() and int(sk[0]) > SKEMA:
        conn.close()
        raise Gagal("Database dibuat oleh buku-piutang versi lebih baru (skema %s). Perbarui skill dulu." % sk[0])
    cfg = pengaturan(conn)
    _JAM["zona"] = cfg["zona"] if cfg["zona"] in ZONA else "WIB"
    return conn


def pengaturan(conn):
    cfg = dict(PENGATURAN_DEFAULT)
    for r in conn.execute("SELECT kunci, nilai FROM meta"):
        cfg[r[0]] = r[1]
    return cfg


def nama_unik(folder, dasar, akhiran=".db"):
    tujuan = folder / (dasar + akhiran)
    n = 2
    while tujuan.exists():
        tujuan = folder / ("%s-%d%s" % (dasar, n, akhiran))
        n += 1
    return tujuan


def buat_backup(db, label):
    if not db.is_file():
        return None
    fol = folder_backup(db)
    fol.mkdir(parents=True, exist_ok=True)
    tujuan = nama_unik(fol, "piutang-%s-%s" % (kini().strftime("%Y%m%d-%H%M%S"), label))
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


def singkirkan(db, pola, pindah):
    """Salin (database sehat) atau pindahkan (database rusak, + journal) ke backup-piutang/. Tidak menghapus."""
    fol = folder_backup(db)
    fol.mkdir(parents=True, exist_ok=True)
    tujuan = nama_unik(fol, pola.format(kini().strftime("%Y%m%d-%H%M%S")))
    if not pindah:
        tujuan.write_bytes(db.read_bytes())
        return tujuan
    os.replace(str(db), str(tujuan))
    for ek in ("-journal", "-wal", "-shm"):
        j = Path(str(db) + ek)
        if j.exists():
            os.replace(str(j), str(tujuan) + ek)
    return tujuan


def pastikan_tidak_dipakai(db):
    c = sqlite3.connect(str(db), timeout=_timeout(), isolation_level=None)
    try:
        c.execute("BEGIN IMMEDIATE")
        c.execute("ROLLBACK")
    except sqlite3.OperationalError as e:
        if _terkunci(e):
            raise Gagal(PESAN_TERKUNCI % _detik())
        raise
    finally:
        c.close()


def status_db(db):
    """'tidak_ada' | 'sehat' | 'rusak'. Database terkunci / milik aplikasi lain -> Gagal."""
    if not db.exists():
        return "tidak_ada"
    try:
        c = buka(db, baca_saja=True)
    except Gagal as e:
        if e.detail.get("rusak"):
            return "rusak"
        raise
    try:
        cek = c.execute("PRAGMA quick_check").fetchone()[0]
    except sqlite3.DatabaseError:
        cek = "rusak"
    finally:
        c.close()
    return "sehat" if cek == "ok" else "rusak"


def backup_harian(db):
    fol = folder_backup(db)
    awalan = "piutang-%s-" % kini().strftime("%Y%m%d")
    if fol.is_dir() and any(p.name.startswith(awalan) for p in fol.glob("piutang-*.db")):
        return None
    b = buat_backup(db, "harian")
    harian = sorted(fol.glob("piutang-*-harian*.db"))
    for lama in harian[:-SIMPAN_BACKUP_HARIAN]:
        try:
            lama.unlink()
        except OSError:
            pass
    return b


def jalankan_tulis(args, perintah, kerja, besar=False, label_backup=None):
    """Jalankan kerja(conn, cfg) dalam satu transaksi, lalu periksa invarian (tidak ada sisa/kredit minus).

    besar=True  -> tanpa --ya: ROLLBACK (pratinjau persis); dengan --ya: cadangan lalu COMMIT.
    besar=False -> langsung tersimpan, dengan cadangan harian otomatis.
    """
    db = path_db(args)
    conn = buka(db)
    simpan = args.ya or not besar
    backup = None
    try:
        if simpan:
            backup = buat_backup(db, label_backup) if (besar and label_backup) else backup_harian(db)
        try:
            conn.execute("BEGIN IMMEDIATE")
        except sqlite3.OperationalError as e:
            if _terkunci(e):
                raise Gagal(PESAN_TERKUNCI % _detik())
            raise
        try:
            data, teks = kerja(conn, pengaturan(conn))
            cek_invarian(conn)
            if simpan:
                conn.execute("INSERT INTO log(waktu, perintah, ringkasan) VALUES (?,?,?)",
                             (stempel(), perintah, json.dumps(data.get("ringkasan", {}), ensure_ascii=False,
                                                              default=str)[:2000]))
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
    data.setdefault("peringatan", [])
    data["mode"] = "tersimpan" if simpan else "pratinjau"
    data["perlu_konfirmasi"] = not simpan
    data["db"] = str(db)
    if backup:
        data["backup"] = backup
    if data["peringatan"]:
        teks += "\n" + "\n".join("Catatan: " + p for p in data["peringatan"])
    if simpan:
        if besar:
            teks = "TERSIMPAN.\n" + teks + (("\nCadangan sebelum perubahan: " + backup) if backup else "")
    else:
        teks = ("PRATINJAU (belum disimpan):\n" + teks +
                "\n\nSimpan? Jalankan perintah yang sama + --ya setelah pengguna setuju.")
    data["teks"] = teks
    return data, teks


def _baca(args):
    return buka(path_db(args), baca_saja=True)


# --------------------------------------------------------------------------- posisi piutang
def kode_p(i):
    return "P%04d" % int(i)


def kode_b(i):
    return "B%04d" % int(i)


def kelompok_umur(telat):
    if telat <= 0:
        return "belum_jatuh_tempo"
    if telat <= 30:
        return "1_30"
    if telat <= 60:
        return "31_60"
    if telat <= 90:
        return "61_90"
    return "lebih_90"


class Buku:
    """Posisi piutang DIHITUNG dari transaksi (tidak disimpan), jadi selalu konsisten.

    per=None -> semua transaksi, umur dihitung terhadap hari ini.
    per=date -> hanya transaksi bertanggal <= per (posisi per tanggal itu).
    sisa nota = nominal - pembayaran yang dialokasikan - potongan.
    kredit pelanggan (kelebihan bayar/deposit) = pembayaran - alokasi ke nota aktif - pengembalian.
    """

    def __init__(self, conn, per=None):
        self.acuan = per or hari_ini()
        ps = per.isoformat() if per else None

        def ok(t):
            return ps is None or str(t)[:10] <= ps

        self.pel = {r["id"]: dict(r) for r in conn.execute("SELECT * FROM pelanggan ORDER BY id")}
        self.nota = [dict(r) for r in conn.execute(
            "SELECT * FROM nota WHERE status='aktif' ORDER BY jatuh_tempo, tanggal, id") if ok(r["tanggal"])]
        idn = {n["id"]: n for n in self.nota}
        bayar = {r["id"]: dict(r) for r in conn.execute("SELECT * FROM pembayaran WHERE status='aktif'")}
        self.kredit = {}
        for n in self.nota:
            n["dibayar"], n["dipotong"] = 0, 0
        for b in bayar.values():
            if ok(b["tanggal"]):
                self.kredit[b["pelanggan_id"]] = self.kredit.get(b["pelanggan_id"], 0) + b["jumlah"]
        for a in conn.execute("SELECT * FROM alokasi"):
            b, n = bayar.get(a["pembayaran_id"]), idn.get(a["nota_id"])
            if not b or not n or not ok(a["tanggal"]):
                continue
            n["dibayar"] += a["jumlah"]
            self.kredit[b["pelanggan_id"]] = self.kredit.get(b["pelanggan_id"], 0) - a["jumlah"]
        for p in conn.execute("SELECT * FROM potongan"):
            n = idn.get(p["nota_id"])
            if n and ok(p["tanggal"]):
                n["dipotong"] += p["jumlah"]
        for k in conn.execute("SELECT * FROM pengembalian"):
            if ok(k["tanggal"]):
                self.kredit[k["pelanggan_id"]] = self.kredit.get(k["pelanggan_id"], 0) - k["jumlah"]
        for n in self.nota:
            n["sisa"] = n["nominal"] - n["dibayar"] - n["dipotong"]
            n["telat"] = (self.acuan - date.fromisoformat(n["jatuh_tempo"])).days
            n["umur"] = kelompok_umur(n["telat"])
            n["pelanggan"] = self.pel.get(n["pelanggan_id"], {}).get("nama", "?")
        self.terbuka = [n for n in self.nota if n["sisa"] > 0]

    def terbuka_pel(self, pid):
        return [n for n in self.terbuka if n["pelanggan_id"] == pid]

    def piutang_pel(self, pid):
        return sum(n["sisa"] for n in self.terbuka_pel(pid))

    def kredit_pel(self, pid):
        return self.kredit.get(pid, 0)

    def total(self):
        return sum(n["sisa"] for n in self.terbuka)

    def umur(self, pid=None):
        hasil = {k: {"jumlah_nota": 0, "nominal": 0} for k, _ in UMUR}
        for n in self.terbuka:
            if pid is None or n["pelanggan_id"] == pid:
                hasil[n["umur"]]["jumlah_nota"] += 1
                hasil[n["umur"]]["nominal"] += n["sisa"]
        return hasil


def cek_invarian(conn):
    b = Buku(conn)
    for n in b.nota:
        if n["sisa"] < 0:
            raise Gagal("Ditolak: sisa nota %s (%s) akan menjadi minus %s. Tidak ada yang disimpan. Periksa nominal/"
                        "pembayaran/potongan nota itu." % (n["no_nota"], n["pelanggan"], rp(-n["sisa"])),
                        invarian=True)
    for pid, k in b.kredit.items():
        if k < 0:
            nama = b.pel.get(pid, {}).get("nama", "?")
            raise Gagal("Ditolak: kelebihan bayar (deposit) %s (%s) akan menjadi minus %s -- uang itu sudah dipakai "
                        "untuk nota lain atau sudah dicatat dikembalikan. Tidak ada yang disimpan. Lihat riwayatnya: "
                        "piutang.py saldo --pelanggan %s" % (nama, kode_p(pid), rp(-k), kode_p(pid)), invarian=True)


# --------------------------------------------------------------------------- pelanggan & nota
def pilihan_json(r):
    return {"kode": kode_p(r["id"]), "nama": r["nama"], "akhir_wa": r["wa"][-4:] if r["wa"] else "-"}


def mirip(nama, semua, kecuali=None):
    kn = kunci_nama(nama)
    hasil = []
    for r in semua:
        if kecuali and r["id"] == kecuali:
            continue
        k2 = kunci_nama(r["nama"])
        if not kn or not k2:
            continue
        if kn == k2 or kn in k2 or k2 in kn or difflib.SequenceMatcher(None, kn, k2).ratio() >= 0.8:
            hasil.append(r)
    return hasil


def cari_pelanggan(conn, ref, ketat=False):
    """Satu pelanggan dari kode (P0003), nomor WA, atau nama. Ambigu -> Gagal berisi pilihan.
    ketat=True (saat mencatat utang baru): hanya nama sama persis/kode/nomor; nama mirip -> ditanyakan."""
    s = bersih(ref, 100)
    if not s:
        raise Gagal("Pelanggan belum disebut. Sebut nama, kode (mis. P0003), atau nomor WA.")
    m = re.fullmatch(r"(?i)p0*(\d{1,6})", s)
    if m:
        r = conn.execute("SELECT * FROM pelanggan WHERE id=?", (int(m.group(1)),)).fetchone()
        if r:
            return r
        raise Gagal("Pelanggan %s tidak ada. Lihat daftar: piutang.py saldo --semua" % s.upper(), tidak_ada=True)
    if len(re.sub(r"\D", "", s)) >= 8 and not re.search(r"[A-Za-z]{3,}", s):
        try:
            wa, _ = normalisasi_wa(s)
        except Gagal:
            wa = None
        if wa:
            rows = conn.execute("SELECT * FROM pelanggan WHERE wa=? ORDER BY id", (wa,)).fetchall()
            if len(rows) == 1:
                return rows[0]
            if len(rows) > 1:
                raise Gagal("Nomor %s dipakai %d pelanggan. Sebut kodenya." % (tampil_wa(wa), len(rows)),
                            pilihan=[pilihan_json(r) for r in rows], ambigu=True)
            raise Gagal("Tidak ada pelanggan dengan nomor %s." % tampil_wa(wa), tidak_ada=True)
    semua = conn.execute("SELECT * FROM pelanggan ORDER BY id").fetchall()
    k, kn = s.lower(), kunci_nama(s)
    cocok = [r for r in semua if r["nama"].lower() == k or (kn and kunci_nama(r["nama"]) == kn)]
    if not cocok and not ketat:
        cocok = [r for r in semua if kn and kn in kunci_nama(r["nama"])]
    if len(cocok) == 1:
        return cocok[0]
    if len(cocok) > 1:
        daftar = "; ".join("%s %s (WA akhiran %s)" % (kode_p(r["id"]), r["nama"], r["wa"][-4:] if r["wa"] else "-")
                           for r in cocok[:10])
        raise Gagal("Ada %d pelanggan yang cocok dengan '%s': %s. Tanyakan ke pengguna yang mana, lalu ulangi "
                    "dengan kodenya (mis. --pelanggan %s)." % (len(cocok), s, daftar, kode_p(cocok[0]["id"])),
                    pilihan=[pilihan_json(r) for r in cocok[:10]], ambigu=True)
    mr = mirip(s, semua)
    if mr:
        daftar = "; ".join("%s %s" % (kode_p(r["id"]), r["nama"]) for r in mr[:10])
        raise Gagal("Pelanggan '%s' tidak ada yang persis sama, tapi ada yang mirip: %s. Tanyakan ke pengguna: "
                    "pelanggan yang sama (ulangi dengan kodenya) atau pelanggan baru (tambahkan --pelanggan-baru)?"
                    % (s, daftar), pilihan=[pilihan_json(r) for r in mr[:10]], ambigu=True, mirip=True)
    raise Gagal("Pelanggan '%s' belum ada di buku. Cek ejaan atau lihat: piutang.py saldo --semua" % s,
                tidak_ada=True)


def buat_pelanggan(conn, nama, wa=None, sapaan=None, catatan="", izinkan_dup=False):
    nama = bersih(nama, 80)
    if not nama or not re.search(r"[^\W\d_]", nama):
        raise Gagal("Nama pelanggan '%s' tidak valid (harus ada huruf)." % nama)
    if nama[0] in "=+@":
        raise Gagal("Nama pelanggan '%s' diawali tanda rumus Excel (= + @); tulis nama biasa." % nama)
    if re.fullmatch(r"(?i)p\d{1,6}|b\d{1,6}", nama):
        raise Gagal("Nama pelanggan tidak boleh berupa kode (%s)." % nama)
    peringatan, w = [], None
    if wa:
        w, p = normalisasi_wa(wa)
        peringatan += p
        dup = conn.execute("SELECT * FROM pelanggan WHERE wa=?", (w,)).fetchone()
        if dup and not izinkan_dup:
            raise Gagal("Nomor %s sudah dipakai pelanggan %s %s. Pakai pelanggan itu (--pelanggan %s), atau "
                        "tambahkan --izinkan-duplikat bila memang orang berbeda." %
                        (tampil_wa(w), kode_p(dup["id"]), dup["nama"], kode_p(dup["id"])), pilihan=[pilihan_json(dup)])
    sama = [r for r in conn.execute("SELECT * FROM pelanggan") if kunci_nama(r["nama"]) == kunci_nama(nama)]
    if sama and not izinkan_dup:
        raise Gagal("Pelanggan bernama '%s' sudah ada (%s). Pakai kodenya, atau tambahkan --izinkan-duplikat bila "
                    "memang orang berbeda (beri nama pembeda, mis. 'Bu Rina Bekasi')." %
                    (nama, ", ".join(kode_p(r["id"]) for r in sama)), pilihan=[pilihan_json(r) for r in sama])
    sap = bersih(sapaan, 20) or None
    cur = conn.execute("INSERT INTO pelanggan(nama, sapaan, wa, catatan, dibuat, diubah) VALUES (?,?,?,?,?,?)",
                       (nama, sap, w, bersih(catatan, 500), stempel(), stempel()))
    return cur.lastrowid, peringatan


def cari_nota(conn, ref, aktif=True):
    k = kunci_nota(ref)
    if not k:
        raise Gagal("Nomor nota belum disebut.")
    r = conn.execute("SELECT * FROM nota WHERE kunci=?", (k,)).fetchone()
    if not r:
        mr = [x["no_nota"] for x in conn.execute("SELECT no_nota, kunci FROM nota")
              if k in x["kunci"] or difflib.SequenceMatcher(None, k, x["kunci"]).ratio() >= 0.85][:5]
        raise Gagal("Nota '%s' tidak ada di buku.%s" % (ref, (" Mungkin maksudnya: " + ", ".join(mr) + "?") if mr
                                                           else " Lihat daftar: piutang.py saldo --pelanggan <nama>"),
                    tidak_ada=True)
    if aktif and r["status"] != "aktif":
        raise Gagal("Nota %s sudah dibatalkan (%s)." % (r["no_nota"], r["alasan_batal"] or "-"))
    return r


def nomor_otomatis(conn, awalan="PB"):
    n = 0
    for r in conn.execute("SELECT kunci FROM nota WHERE kunci LIKE ?", (awalan + "%",)):
        m = re.fullmatch(awalan + r"(\d+)", r["kunci"])
        if m:
            n = max(n, int(m.group(1)))
    return "%s-%04d" % (awalan, n + 1)


def telat_teks(telat, jt):
    if telat > 0:
        return "JT %s (lewat %d hari)" % (tgl_pendek(jt), telat)
    if telat == 0:
        return "JT %s (hari ini)" % tgl_pendek(jt)
    return "JT %s (%d hari lagi)" % (tgl_pendek(jt), -telat)


def nama_tampil(p, samarkan=False):
    return samar_nama(p["nama"]) if samarkan else p["nama"]


def saldo_teks(buku, pid):
    p = buku.piutang_pel(pid)
    n = len(buku.terbuka_pel(pid))
    k = buku.kredit_pel(pid)
    t = "Saldo piutang %s: %s (%d nota terbuka)" % (buku.pel[pid]["nama"], rp(p), n)
    if k:
        t += " | kelebihan bayar/deposit: %s" % rp(k)
        t += (" | saldo bersih: %s" % rp(p - k)) if p >= k else \
            (" | saldo bersih: DEPOSIT milik pelanggan %s (bukan utang pelanggan)" % rp(k - p))
    return t + "."


def nota_json(n, samarkan=False, pel=None):
    d = {"no_nota": n["no_nota"], "kode_pelanggan": kode_p(n["pelanggan_id"]),
         "pelanggan": samar_nama(n["pelanggan"]) if samarkan else n["pelanggan"], "tanggal": n["tanggal"],
         "jatuh_tempo": n["jatuh_tempo"], "nominal": n["nominal"], "dibayar": n.get("dibayar"),
         "dipotong": n.get("dipotong"), "sisa": n.get("sisa"), "hari_lewat": max(0, n.get("telat", 0)),
         "hari_menuju_jatuh_tempo": max(0, -n.get("telat", 0)), "umur": n.get("umur"),
         "diingatkan": n["diingatkan"], "terakhir_diingatkan": n["terakhir_diingatkan"]}
    if not samarkan:
        d["keterangan"] = n["keterangan"]
    return d


# --------------------------------------------------------------------------- perintah: pengaturan
def cmd_init(args):
    db = path_db(args)
    zona = kode_zona(args.zona or "WIB")
    termin = TERMIN_DEFAULT if args.termin is None else baca_termin(args.termin)
    if termin is None or termin > MAKS_TERMIN:
        raise Gagal("--termin harus jumlah hari 0-%d, mis. 30." % MAKS_TERMIN)
    rusak = False
    if db.exists():
        try:
            conn = buka(db, baca_saja=True)
            conn.close()
            raise Gagal("Database piutang sudah ada di %s. Tidak dibuat ulang (data aman). Untuk mengubah pengaturan "
                        "pakai: piutang.py atur." % db, sudah_ada=True)
        except Gagal as e:
            if e.detail.get("sudah_ada") or "sedang dipakai" in e.pesan:
                raise
            if not e.detail.get("rusak"):
                raise Gagal("File %s sudah ada dan bukan database buku-piutang; tidak ditimpa. Pakai --db lain." % db)
            if not args.mulai_baru:
                raise Gagal("Database %s rusak. Pulihkan dari cadangan dulu: piutang.py backup --daftar lalu "
                            "piutang.py restore --dari <file>. Jika tidak ada cadangan: ulangi dengan --mulai-baru "
                            "(file rusak dipindah ke folder backup-piutang, tidak dihapus)." % db, rusak=True)
            rusak = True
    cfg = {"nama_usaha": bersih(args.nama_usaha, 80), "pengirim": bersih(args.pengirim, 40),
           "rekening": bersih(args.rekening, 120), "termin": str(termin), "zona": zona}
    ringkas = ("Database piutang baru: %s\nNama usaha: %s | Pengirim draf: %s | Rekening di draf: %s\n"
               "Termin default: %d hari | Zona: %s\nCadangan otomatis: %s" %
               (db, cfg["nama_usaha"] or "-", cfg["pengirim"] or "-", cfg["rekening"] or "-", termin, zona,
                folder_backup(db)))
    if rusak:
        ringkas += "\nFile rusak yang ada sekarang dipindah (tidak dihapus) ke %s." % folder_backup(db)
    if not args.ya:
        t = ("PRATINJAU (belum dibuat):\n" + ringkas +
             "\n\nBuat? Jalankan perintah yang sama + --ya setelah pengguna setuju.")
        return {"ok": True, "mode": "pratinjau", "perlu_konfirmasi": True, "db": str(db), "pengaturan": cfg,
                "teks": t}, t
    db.parent.mkdir(parents=True, exist_ok=True)
    if rusak:
        pindahan = singkirkan(db, "rusak-piutang-{}", pindah=True)
        ringkas += "\nFile rusak dipindah ke: %s" % pindahan
    conn = sqlite3.connect(str(db), isolation_level=None)
    try:
        conn.executescript("BEGIN;" + SKEMA_SQL + "COMMIT;")
        _JAM["zona"] = zona
        meta = dict(cfg, aplikasi=APLIKASI, skema=str(SKEMA), versi_pembuat=VERSI, dibuat=stempel())
        conn.execute("BEGIN")
        conn.executemany("INSERT INTO meta(kunci, nilai) VALUES (?,?)", list(meta.items()))
        conn.execute("COMMIT")
    finally:
        conn.close()
    t = "TERSIMPAN. Buku piutang siap.\n" + ringkas
    return {"ok": True, "mode": "tersimpan", "perlu_konfirmasi": False, "db": str(db), "pengaturan": cfg,
            "teks": t}, t


def cmd_info(args):
    db = path_db(args)
    if not db.exists():
        t = ("Buku piutang belum ada (lokasi: %s). Mulai dengan: piutang.py init --nama-usaha \"...\" --pengirim "
             "\"...\" --rekening \"...\" (pratinjau, lalu --ya)." % db)
        return {"ok": True, "mode": "baca", "ada": False, "db": str(db), "versi": VERSI, "teks": t}, t
    conn = buka(db, baca_saja=True)
    try:
        cfg = pengaturan(conn)
        cek = conn.execute("PRAGMA quick_check").fetchone()[0]
        buku = Buku(conn)
        n_pel = len(buku.pel)
        n_nota = conn.execute("SELECT COUNT(*) FROM nota").fetchone()[0]
    finally:
        conn.close()
    fol = folder_backup(db)
    bks = sorted(fol.glob("piutang-*.db")) if fol.is_dir() else []
    peringatan = []
    jam_komp = datetime.now().replace(microsecond=0)
    lokal = waktu_lokal(_JAM["zona"])
    if abs((jam_komp - lokal).total_seconds()) > 1800:
        peringatan.append("Jam komputer (%s) berbeda dengan jam %s (%s). Buku piutang tetap memakai jam %s untuk "
                          "'hari ini'." % (jam_komp.strftime("%H:%M"), _JAM["zona"], lokal.strftime("%H:%M"),
                                           _JAM["zona"]))
    if cek != "ok":
        peringatan.append("Pemeriksaan database menemukan masalah (%s). Pulihkan dari cadangan terakhir yang sehat."
                          % cek)
    t = ("BUKU PIUTANG %s\nDatabase: %s\nUsaha: %s | Pengirim: %s | Rekening: %s | Termin default: %s hari | Zona: %s\n"
         "Pelanggan: %d | Nota: %d | Piutang terbuka: %s (%d nota)\nPemeriksaan database: %s\n"
         "Cadangan: %d file di %s%s" %
         (VERSI, db, cfg["nama_usaha"] or "-", cfg["pengirim"] or "-", cfg["rekening"] or "-", cfg["termin"],
          cfg["zona"], n_pel, n_nota, rp(buku.total()), len(buku.terbuka), cek, len(bks), fol,
          ("\nTerakhir: " + bks[-1].name) if bks else ""))
    if peringatan:
        t += "\n" + "\n".join("Catatan: " + p for p in peringatan)
    return {"ok": True, "mode": "baca", "ada": True, "db": str(db), "versi": VERSI, "pengaturan": cfg,
            "jumlah_pelanggan": n_pel, "jumlah_nota": n_nota, "total_piutang": buku.total(), "pemeriksaan": cek,
            "jumlah_backup": len(bks), "backup_terakhir": str(bks[-1]) if bks else None, "peringatan": peringatan,
            "teks": t}, t


def cmd_atur(args):
    def kerja(conn, cfg):
        ubah = {}
        for k in ("nama_usaha", "pengirim", "rekening"):
            v = getattr(args, k)
            if v is not None:
                ubah[k] = bersih(v, 120)
        if args.termin is not None:
            t = baca_termin(args.termin)
            if t is None or t > MAKS_TERMIN:
                raise Gagal("--termin harus jumlah hari 0-%d." % MAKS_TERMIN)
            ubah["termin"] = str(t)
        if args.zona is not None:
            ubah["zona"] = kode_zona(args.zona)
        if not ubah:
            raise Gagal("Tidak ada yang diubah. Pilihan: --nama-usaha, --pengirim, --rekening, --termin, --zona.")
        for k, v in ubah.items():
            conn.execute("INSERT OR REPLACE INTO meta(kunci, nilai) VALUES (?,?)", (k, v))
        t = "Pengaturan diperbarui: " + ", ".join("%s = %s" % (k, v or "-") for k, v in ubah.items())
        return {"pengaturan": ubah, "ringkasan": ubah}, t
    return jalankan_tulis(args, "atur", kerja)


# --------------------------------------------------------------------------- perintah: pelanggan
def cmd_tambah_pelanggan(args):
    def kerja(conn, cfg):
        pid, per = buat_pelanggan(conn, args.nama, args.wa, args.sapaan, args.catatan or "", args.izinkan_duplikat)
        r = conn.execute("SELECT * FROM pelanggan WHERE id=?", (pid,)).fetchone()
        t = "Pelanggan %s dicatat: %s | WA %s" % (kode_p(pid), r["nama"], tampil_wa(r["wa"]))
        return {"pelanggan": pilihan_json(r), "kode": kode_p(pid), "peringatan": per,
                "ringkasan": {"kode": kode_p(pid)}}, t
    return jalankan_tulis(args, "tambah-pelanggan", kerja)


def cmd_ubah_pelanggan(args):
    def kerja(conn, cfg):
        p = cari_pelanggan(conn, args.pelanggan)
        ubah, per = {}, []
        if args.nama:
            nama = bersih(args.nama, 80)
            if not re.search(r"[^\W\d_]", nama):
                raise Gagal("Nama pelanggan harus berisi huruf.")
            ubah["nama"] = nama
        if args.wa is not None:
            if args.wa.strip().lower() in ("-", "hapus", "kosong"):
                ubah["wa"] = None
            else:
                w, pr = normalisasi_wa(args.wa)
                per += pr
                dup = conn.execute("SELECT * FROM pelanggan WHERE wa=? AND id<>?", (w, p["id"])).fetchone()
                if dup and not args.izinkan_duplikat:
                    raise Gagal("Nomor %s sudah dipakai %s %s." % (tampil_wa(w), kode_p(dup["id"]), dup["nama"]))
                ubah["wa"] = w
        if args.sapaan is not None:
            ubah["sapaan"] = bersih(args.sapaan, 20) or None
        if args.catatan is not None:
            ubah["catatan"] = bersih(args.catatan, 500)
        if not ubah:
            raise Gagal("Tidak ada yang diubah. Pilihan: --nama, --wa, --sapaan, --catatan.")
        for k, v in ubah.items():
            conn.execute("UPDATE pelanggan SET %s=?, diubah=? WHERE id=?" % k, (v, stempel(), p["id"]))
        r = conn.execute("SELECT * FROM pelanggan WHERE id=?", (p["id"],)).fetchone()
        t = "Pelanggan %s diperbarui: %s | WA %s" % (kode_p(r["id"]), r["nama"], tampil_wa(r["wa"]))
        return {"pelanggan": pilihan_json(r), "peringatan": per, "ringkasan": {"kode": kode_p(r["id"]),
                                                                                "ubah": list(ubah)}}, t
    return jalankan_tulis(args, "ubah-pelanggan", kerja)


def cmd_hapus_pelanggan(args):
    def kerja(conn, cfg):
        p = cari_pelanggan(conn, args.pelanggan)
        buku = Buku(conn)
        sisa, kredit = buku.piutang_pel(p["id"]), buku.kredit_pel(p["id"])
        if sisa or kredit:
            raise Gagal("%s masih punya piutang %s / kelebihan bayar %s. Selesaikan dulu (bayar/potong/kembalikan) "
                        "sebelum datanya dihapus." % (p["nama"], rp(sisa), rp(kredit)))
        ids = [r[0] for r in conn.execute("SELECT id FROM nota WHERE pelanggan_id=?", (p["id"],))]
        bids = [r[0] for r in conn.execute("SELECT id FROM pembayaran WHERE pelanggan_id=?", (p["id"],))]
        for i in ids:
            conn.execute("DELETE FROM alokasi WHERE nota_id=?", (i,))
            conn.execute("DELETE FROM potongan WHERE nota_id=?", (i,))
        for i in bids:
            conn.execute("DELETE FROM alokasi WHERE pembayaran_id=?", (i,))
        conn.execute("DELETE FROM nota WHERE pelanggan_id=?", (p["id"],))
        conn.execute("DELETE FROM pembayaran WHERE pelanggan_id=?", (p["id"],))
        conn.execute("DELETE FROM pengembalian WHERE pelanggan_id=?", (p["id"],))
        conn.execute("DELETE FROM pelanggan WHERE id=?", (p["id"],))
        t = ("Hapus permanen %s %s beserta %d nota dan %d pembayaran (semuanya sudah lunas/selesai).\n"
             "Cadangan lama di folder backup-piutang masih memuat data ini." % (kode_p(p["id"]), p["nama"], len(ids),
                                                                                  len(bids)))
        return {"kode": kode_p(p["id"]), "jumlah_nota": len(ids), "jumlah_pembayaran": len(bids),
                "ringkasan": {"hapus": kode_p(p["id"])}}, t
    return jalankan_tulis(args, "hapus-pelanggan", kerja, besar=True, label_backup="sebelum-hapus")


# --------------------------------------------------------------------------- perintah: catat nota
def nominal_dari_args(args):
    """Kembalikan (nominal, dpp, ppn, [catatan])."""
    catatan = []
    if args.dpp is not None or args.ppn is not None:
        if args.nominal is not None:
            raise Gagal("Isi --nominal (total tagihan) ATAU --dpp + --ppn, bukan keduanya. Bila total di nota sudah "
                        "termasuk PPN, cukup --nominal.")
        if args.dpp is None or args.ppn is None:
            raise Gagal("--dpp dan --ppn harus diisi bersama (mis. --dpp 10jt --ppn 11).")
        dpp, c = parse_rupiah(args.dpp, "DPP")
        catatan += c
        ppn, ket = hitung_ppn(dpp, args.ppn)
        catatan.append("Rincian: DPP %s + %s = %s. %s" % (rp(dpp), ket, rp(dpp + ppn), CATATAN_PAJAK))
        return dpp + ppn, dpp, ppn, catatan
    if args.nominal is None:
        raise Gagal("Nominal tagihan belum disebut (--nominal, mis. 2,5jt).")
    n, c = parse_rupiah(args.nominal)
    return n, None, None, c


def cmd_catat(args):
    def kerja(conn, cfg):
        hari = hari_ini()
        per = []
        nominal, dpp, ppn, c = nominal_dari_args(args)
        per += c
        tanggal, c = tgl_nota(args.tanggal, hari)
        per += c
        if not args.tanggal:
            per.append("Tanggal nota belum disebut; dipakai hari ini (%s)." % tgl_pendek(tanggal))
        jt, termin, c = tentukan_jatuh_tempo(args.jatuh_tempo, args.termin, tanggal, cfg, hari)
        per += c
        baru = False
        try:
            p = cari_pelanggan(conn, args.pelanggan, ketat=True)
            if args.pelanggan_baru:
                raise Gagal("--pelanggan-baru dipakai, tapi pelanggan '%s' sudah ada (%s). Jika memang orang berbeda, "
                            "beri nama pembeda." % (args.pelanggan, kode_p(p["id"])))
            if args.wa:
                per.append("--wa diabaikan karena pelanggan sudah ada; ubah nomor dengan ubah-pelanggan.")
        except Gagal as e:
            if not (e.detail.get("tidak_ada") or (e.detail.get("mirip") and args.pelanggan_baru)):
                raise
            if re.fullmatch(r"(?i)p\d{1,6}", bersih(args.pelanggan)):
                raise
            pid, c = buat_pelanggan(conn, args.pelanggan, args.wa, args.sapaan, izinkan_dup=args.pelanggan_baru)
            per += c
            p = conn.execute("SELECT * FROM pelanggan WHERE id=?", (pid,)).fetchone()
            baru = True
        no = bersih(args.nota, 40) if args.nota else nomor_otomatis(conn)
        if not kunci_nota(no):
            raise Gagal("Nomor nota kosong.")
        ada = conn.execute("SELECT n.*, p.nama FROM nota n JOIN pelanggan p ON p.id=n.pelanggan_id WHERE kunci=?",
                           (kunci_nota(no),)).fetchone()
        if ada:
            raise Gagal("Nota %s sudah tercatat untuk %s (%s, %s, status %s). Tidak dicatat dobel. Kalau ini nota "
                        "lain, pakai nomor berbeda." % (ada["no_nota"], ada["nama"], rp(ada["nominal"]),
                                                        tgl_pendek(ada["tanggal"]), ada["status"]), duplikat=True)
        mirip_dobel = conn.execute("SELECT no_nota FROM nota WHERE pelanggan_id=? AND tanggal=? AND nominal=? AND "
                                   "status='aktif'", (p["id"], tanggal.isoformat(), nominal)).fetchall()
        if mirip_dobel:
            per.append("Sudah ada nota %s untuk %s dengan tanggal dan nominal sama. Pastikan ini bukan catatan dobel "
                       "(batalkan dengan batal-nota bila dobel)." % (", ".join(r[0] for r in mirip_dobel), p["nama"]))
        if not args.nota:
            per.append("Nomor nota tidak disebut; diberi nomor otomatis %s." % no)
        cur = conn.execute(
            "INSERT INTO nota(pelanggan_id, no_nota, kunci, tanggal, jatuh_tempo, nominal, dpp, ppn, keterangan, "
            "sumber, dibuat, diubah) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], no, kunci_nota(no), tanggal.isoformat(), jt.isoformat(), nominal, dpp, ppn,
             bersih(args.keterangan, 200), "manual", stempel(), stempel()))
        telat = (hari - jt).days
        if telat > 0:
            per.append("Nota ini sudah lewat jatuh tempo %d hari; langsung masuk daftar terlewat." % telat)
        buku = Buku(conn)
        if buku.kredit_pel(p["id"]) > 0:
            per.append("%s punya deposit/kelebihan bayar %s. Tawarkan ke pengguna: pakai untuk nota ini "
                       "(pakai-kredit --pelanggan %s)?" % (p["nama"], rp(buku.kredit_pel(p["id"])), kode_p(p["id"])))
        t = ("Tercatat nota %s untuk %s (%s%s): %s | tanggal %s | jatuh tempo %s (%d hari)\n%s" %
             (no, p["nama"], kode_p(p["id"]), ", pelanggan baru" if baru else "", rp(nominal), tgl_pendek(tanggal),
              tgl_panjang(jt), termin, saldo_teks(buku, p["id"])))
        n = [x for x in buku.nota if x["id"] == cur.lastrowid][0]
        return {"nota": nota_json(n), "pelanggan_baru": baru, "kode_pelanggan": kode_p(p["id"]), "dpp": dpp,
                "ppn": ppn, "saldo_pelanggan": buku.piutang_pel(p["id"]), "peringatan": per,
                "ringkasan": {"nota": no, "nominal": nominal}}, t
    return jalankan_tulis(args, "catat", kerja)


def cmd_ubah_nota(args):
    def kerja(conn, cfg):
        hari = hari_ini()
        n = cari_nota(conn, args.nota)
        per, ubah = [], {}
        tanggal = date.fromisoformat(n["tanggal"])
        if args.tanggal:
            tanggal, c = tgl_nota(args.tanggal, hari)
            per += c
            ubah["tanggal"] = tanggal.isoformat()
        if args.jatuh_tempo or args.termin is not None:
            jt, _, c = tentukan_jatuh_tempo(args.jatuh_tempo, args.termin, tanggal, cfg, hari)
            per += c
            ubah["jatuh_tempo"] = jt.isoformat()
        elif args.tanggal and n["jatuh_tempo"] < tanggal.isoformat():
            raise Gagal("Tanggal nota baru %s melewati jatuh tempo %s. Ubah juga --jatuh-tempo." %
                        (tgl_pendek(tanggal), tgl_pendek(n["jatuh_tempo"])))
        if args.nominal:
            v, c = parse_rupiah(args.nominal)
            per += c
            ubah["nominal"] = v
            ubah["dpp"], ubah["ppn"] = None, None
            if n["dpp"] is not None:
                per.append("Rincian DPP/PPN lama dihapus karena nominal diubah langsung.")
        if args.keterangan is not None:
            ubah["keterangan"] = bersih(args.keterangan, 200)
        if args.no_baru:
            k = kunci_nota(args.no_baru)
            if not k:
                raise Gagal("Nomor nota baru kosong.")
            if k != n["kunci"] and conn.execute("SELECT 1 FROM nota WHERE kunci=?", (k,)).fetchone():
                raise Gagal("Nomor nota %s sudah dipakai." % args.no_baru)
            ubah["no_nota"], ubah["kunci"] = bersih(args.no_baru, 40), k
        if args.pelanggan:
            p = cari_pelanggan(conn, args.pelanggan)
            if p["id"] != n["pelanggan_id"]:
                ada_bayar = conn.execute("SELECT COUNT(*) FROM alokasi a JOIN pembayaran b ON b.id=a.pembayaran_id "
                                         "WHERE a.nota_id=? AND b.status='aktif'", (n["id"],)).fetchone()[0]
                if ada_bayar:
                    raise Gagal("Nota %s sudah ada pembayarannya; tidak bisa dipindah ke pelanggan lain. Batalkan "
                                "pembayarannya dulu (batal-bayar)." % n["no_nota"])
                ubah["pelanggan_id"] = p["id"]
        if not ubah:
            raise Gagal("Tidak ada yang diubah. Pilihan: --tanggal, --jatuh-tempo/--termin, --nominal, --keterangan, "
                        "--no-baru, --pelanggan.")
        for k, v in ubah.items():
            conn.execute("UPDATE nota SET %s=?, diubah=? WHERE id=?" % k, (v, stempel(), n["id"]))
        buku = Buku(conn)
        x = [y for y in buku.nota if y["id"] == n["id"]][0]
        t = ("Nota %s diperbarui: %s | %s | nominal %s | sisa %s | %s" %
             (x["no_nota"], x["pelanggan"], tgl_pendek(x["tanggal"]), rp(x["nominal"]), rp(x["sisa"]),
              telat_teks(x["telat"], x["jatuh_tempo"])))
        return {"nota": nota_json(x), "peringatan": per,
                "ringkasan": {"nota": x["no_nota"], "ubah": sorted(ubah)}}, t
    return jalankan_tulis(args, "ubah-nota", kerja)


# --------------------------------------------------------------------------- perintah: pembayaran
def alokasikan(conn, bid, target, uang, tgl_bayar):
    """Alokasikan uang ke nota target (urut), kembalikan (daftar (nota, jumlah), sisa uang)."""
    hasil = []
    for n in target:
        if uang <= 0:
            break
        if n["sisa"] <= 0:
            continue
        j = min(uang, n["sisa"])
        tgl = max(tgl_bayar.isoformat(), n["tanggal"])
        conn.execute("INSERT INTO alokasi(pembayaran_id, nota_id, tanggal, jumlah, dibuat) VALUES (?,?,?,?,?)",
                     (bid, n["id"], tgl, j, stempel()))
        n["sisa"] -= j
        uang -= j
        hasil.append((n, j))
    return hasil, uang


def teks_alokasi(hasil):
    return ", ".join("%s %s (%s)" % (n["no_nota"], rp(j), "LUNAS" if n["sisa"] == 0 else "sisa " + rp(n["sisa"]))
                     for n, j in hasil)


def cmd_bayar(args):
    def kerja(conn, cfg):
        hari = hari_ini()
        per = []
        nota = cari_nota(conn, args.nota) if args.nota else None
        if nota:
            p = conn.execute("SELECT * FROM pelanggan WHERE id=?", (nota["pelanggan_id"],)).fetchone()
            if args.pelanggan:
                p2 = cari_pelanggan(conn, args.pelanggan)
                if p2["id"] != p["id"]:
                    raise Gagal("Nota %s milik %s (%s), bukan %s. Periksa lagi." %
                                (nota["no_nota"], p["nama"], kode_p(p["id"]), p2["nama"]))
        else:
            if not args.pelanggan:
                raise Gagal("Sebut pelanggan (--pelanggan) atau nomor nota (--nota).")
            p = cari_pelanggan(conn, args.pelanggan)
        tgl, c = tgl_nota(args.tanggal, hari)
        per += c
        buku = Buku(conn)
        terbuka = buku.terbuka_pel(p["id"])
        if nota:
            n0 = [n for n in buku.nota if n["id"] == nota["id"]][0]
            if n0["sisa"] <= 0:
                raise Gagal("Nota %s sudah lunas. Kalau pelanggan membayar nota lain, sebut nomornya atau hilangkan "
                            "--nota (pembayaran dialokasikan ke nota tertua)." % nota["no_nota"], lunas=True)
            target = [n0] + ([n for n in terbuka if n["id"] != n0["id"]] if args.kelebihan == "nota-lain" else [])
        else:
            target = terbuka
        total_target = sum(n["sisa"] for n in target)
        if str(args.jumlah).strip().lower() in ("lunas", "semua", "sisa", "pelunasan"):
            if total_target <= 0:
                raise Gagal("Tidak ada tagihan terbuka untuk %s; tidak ada yang perlu dilunasi." % p["nama"])
            jumlah = sum(n["sisa"] for n in ([target[0]] if nota else target))
        else:
            jumlah, c = parse_rupiah(args.jumlah, "Jumlah bayar")
            per += c
        if not args.izinkan_dobel:
            dobel = conn.execute("SELECT id FROM pembayaran WHERE pelanggan_id=? AND tanggal=? AND jumlah=? AND "
                                 "status='aktif'", (p["id"], tgl.isoformat(), jumlah)).fetchall()
            if dobel:
                raise Gagal("Pembayaran %s dari %s tanggal %s sudah tercatat (%s). Tidak dicatat dobel. Jika memang ada "
                            "dua pembayaran terpisah dengan jumlah sama, ulangi dengan --izinkan-dobel." %
                            (rp(jumlah), p["nama"], tgl_pendek(tgl), ", ".join(kode_b(r[0]) for r in dobel)),
                            duplikat=True)
        lebih = jumlah - total_target
        if total_target == 0 and args.kelebihan not in ("kredit", "kembalikan"):
            raise Gagal("%s tidak punya tagihan terbuka, jadi pembayaran %s TIDAK dicatat. Kalau ini uang muka/deposit "
                        "untuk pesanan berikutnya, ulangi dengan --kelebihan kredit. Kalau untuk pelanggan lain, periksa "
                        "namanya." % (p["nama"], rp(jumlah)), kelebihan=jumlah, total_tagihan=0)
        if lebih > 0 and args.kelebihan not in ("kredit", "kembalikan"):
            opsi = ["--kelebihan kredit (disimpan sebagai deposit/kelebihan bayar pelanggan, bisa dipakai untuk nota "
                    "berikutnya)", "--kelebihan kembalikan (uang lebihnya sudah dikembalikan ke pelanggan)"]
            lain = [n for n in terbuka if not nota or n["id"] != nota["id"]]
            if nota and lain and args.kelebihan != "nota-lain":
                opsi.insert(0, "--kelebihan nota-lain (sisanya untuk nota lain pelanggan ini: %s)" %
                            ", ".join(n["no_nota"] for n in lain[:5]))
            raise Gagal("Pembayaran %s melebihi %s %s (kelebihan %s). TIDAK dicatat, supaya saldo tidak minus "
                        "diam-diam. Tanyakan ke pengguna, lalu ulangi perintah yang sama dengan salah satu: %s. Atau "
                        "periksa lagi jumlahnya (salah ketik?)." %
                        (rp(jumlah), "sisa nota " + nota["no_nota"] if nota and args.kelebihan != "nota-lain" else
                         "seluruh tagihan terbuka " + p["nama"], rp(total_target), rp(lebih), "; ".join(opsi)),
                        kelebihan=lebih, total_tagihan=total_target)
        if lebih <= 0 and args.kelebihan in ("kredit", "kembalikan"):
            per.append("Tidak ada kelebihan bayar; opsi --kelebihan %s tidak dipakai." % args.kelebihan)
        cur = conn.execute("INSERT INTO pembayaran(pelanggan_id, tanggal, jumlah, metode, catatan, dibuat) "
                           "VALUES (?,?,?,?,?,?)", (p["id"], tgl.isoformat(), jumlah, bersih(args.metode, 40),
                                                    bersih(args.catatan, 200), stempel()))
        bid = cur.lastrowid
        hasil, sisa_uang = alokasikan(conn, bid, target, jumlah, tgl)
        for n, _ in hasil:
            if n["tanggal"] > tgl.isoformat():
                per.append("Tanggal bayar %s lebih awal dari tanggal nota %s (%s); dicatat berlaku sejak tanggal nota."
                           % (tgl_pendek(tgl), n["no_nota"], tgl_pendek(n["tanggal"])))
        kembali = 0
        if sisa_uang > 0 and args.kelebihan == "kembalikan":
            conn.execute("INSERT INTO pengembalian(pelanggan_id, tanggal, jumlah, catatan, dibuat) VALUES (?,?,?,?,?)",
                         (p["id"], tgl.isoformat(), sisa_uang, "kelebihan bayar %s dikembalikan" % kode_b(bid),
                          stempel()))
            kembali = sisa_uang
        buku = Buku(conn)
        t = "Pembayaran %s dicatat: %s dari %s (%s), %s%s." % (
            kode_b(bid), rp(jumlah), p["nama"], kode_p(p["id"]), tgl_pendek(tgl),
            (", " + bersih(args.metode, 40)) if args.metode else "")
        if hasil:
            t += "\nDipakai untuk: " + teks_alokasi(hasil) + "."
        if sisa_uang > 0:
            t += ("\nKelebihan %s dicatat sudah DIKEMBALIKAN ke pelanggan." % rp(sisa_uang) if kembali else
                  "\nKelebihan %s disimpan sebagai DEPOSIT/kelebihan bayar %s (dipakai untuk nota berikutnya dengan "
                  "perintah pakai-kredit)." % (rp(sisa_uang), p["nama"]))
        t += "\n" + saldo_teks(buku, p["id"])
        return {"kode": kode_b(bid), "kode_pelanggan": kode_p(p["id"]), "jumlah": jumlah, "tanggal": tgl.isoformat(),
                "alokasi": [{"no_nota": n["no_nota"], "jumlah": j, "sisa_nota": n["sisa"]} for n, j in hasil],
                "kelebihan_disimpan": sisa_uang - kembali, "kelebihan_dikembalikan": kembali,
                "saldo_pelanggan": buku.piutang_pel(p["id"]), "kredit_pelanggan": buku.kredit_pel(p["id"]),
                "peringatan": per, "ringkasan": {"bayar": kode_b(bid), "jumlah": jumlah}}, t
    return jalankan_tulis(args, "bayar", kerja)


def cmd_pakai_kredit(args):
    def kerja(conn, cfg):
        hari = hari_ini()
        p = cari_pelanggan(conn, args.pelanggan)
        tgl, per = tgl_nota(args.tanggal, hari)
        buku = Buku(conn)
        kredit = buku.kredit_pel(p["id"])
        if kredit <= 0:
            raise Gagal("%s tidak punya kelebihan bayar/deposit yang bisa dipakai." % p["nama"])
        if args.nota:
            nota = cari_nota(conn, args.nota)
            if nota["pelanggan_id"] != p["id"]:
                raise Gagal("Nota %s bukan milik %s." % (nota["no_nota"], p["nama"]))
            target = [n for n in buku.terbuka if n["id"] == nota["id"]]
            if not target:
                raise Gagal("Nota %s sudah lunas." % nota["no_nota"])
        else:
            target = buku.terbuka_pel(p["id"])
        if not target:
            raise Gagal("%s tidak punya nota terbuka; deposit %s tetap tersimpan." % (p["nama"], rp(kredit)))
        pakai = min(kredit, sum(n["sisa"] for n in target))
        # sumber uang: pembayaran aktif yang masih punya sisa belum teralokasi (tertua dulu)
        sumber = []
        for b in conn.execute("SELECT * FROM pembayaran WHERE pelanggan_id=? AND status='aktif' ORDER BY tanggal, id",
                              (p["id"],)):
            dipakai = conn.execute("SELECT IFNULL(SUM(a.jumlah),0) FROM alokasi a JOIN nota n ON n.id=a.nota_id "
                                   "WHERE a.pembayaran_id=? AND n.status='aktif'", (b["id"],)).fetchone()[0]
            if b["jumlah"] - dipakai > 0:
                sumber.append((b, b["jumlah"] - dipakai))
        hasil_total, sisa_pakai = [], pakai
        for b, bebas in sumber:
            if sisa_pakai <= 0:
                break
            ambil = min(bebas, sisa_pakai)
            tgl_a = max(tgl, date.fromisoformat(b["tanggal"]))
            hasil, lebih = alokasikan(conn, b["id"], target, ambil, tgl_a)
            hasil_total += hasil
            sisa_pakai -= ambil - lebih
        buku2 = Buku(conn)
        t = ("Deposit %s dipakai %s untuk: %s.\nSisa deposit: %s. %s" %
             (p["nama"], rp(pakai), teks_alokasi(hasil_total), rp(buku2.kredit_pel(p["id"])),
              saldo_teks(buku2, p["id"])))
        return {"kode_pelanggan": kode_p(p["id"]), "dipakai": pakai,
                "alokasi": [{"no_nota": n["no_nota"], "jumlah": j, "sisa_nota": n["sisa"]} for n, j in hasil_total],
                "kredit_pelanggan": buku2.kredit_pel(p["id"]), "saldo_pelanggan": buku2.piutang_pel(p["id"]),
                "peringatan": per, "ringkasan": {"pakai_kredit": pakai}}, t
    return jalankan_tulis(args, "pakai-kredit", kerja)


def cmd_kembalikan(args):
    def kerja(conn, cfg):
        hari = hari_ini()
        p = cari_pelanggan(conn, args.pelanggan)
        tgl, per = tgl_nota(args.tanggal, hari)
        kredit = Buku(conn).kredit_pel(p["id"])
        if kredit <= 0:
            raise Gagal("%s tidak punya kelebihan bayar/deposit untuk dikembalikan." % p["nama"])
        if str(args.jumlah).strip().lower() in ("semua", "seluruh", "sisa"):
            jumlah = kredit
        else:
            jumlah, c = parse_rupiah(args.jumlah, "Jumlah dikembalikan")
            per += c
        if jumlah > kredit:
            raise Gagal("Jumlah dikembalikan %s melebihi deposit %s (%s). Tidak dicatat." %
                        (rp(jumlah), p["nama"], rp(kredit)))
        conn.execute("INSERT INTO pengembalian(pelanggan_id, tanggal, jumlah, catatan, dibuat) VALUES (?,?,?,?,?)",
                     (p["id"], tgl.isoformat(), jumlah, bersih(args.catatan, 200), stempel()))
        sisa = kredit - jumlah
        t = "Pengembalian %s ke %s dicatat (%s). Sisa deposit: %s." % (rp(jumlah), p["nama"], tgl_pendek(tgl), rp(sisa))
        return {"kode_pelanggan": kode_p(p["id"]), "jumlah": jumlah, "kredit_pelanggan": sisa, "peringatan": per,
                "ringkasan": {"kembalikan": jumlah}}, t
    return jalankan_tulis(args, "kembalikan", kerja)


def cmd_potong(args):
    def kerja(conn, cfg):
        hari = hari_ini()
        nota = cari_nota(conn, args.nota)
        if not bersih(args.alasan):
            raise Gagal("Alasan potongan wajib diisi (mis. 'retur 2 dus', 'diskon pelunasan', 'dihapus/diikhlaskan').")
        tgl, per = tgl_nota(args.tanggal, hari)
        buku = Buku(conn)
        n = [x for x in buku.nota if x["id"] == nota["id"]][0]
        if n["sisa"] <= 0:
            raise Gagal("Nota %s sudah lunas; tidak ada yang bisa dipotong." % n["no_nota"])
        if str(args.jumlah).strip().lower() in ("sisa", "semua"):
            jumlah = n["sisa"]
        else:
            jumlah, c = parse_rupiah(args.jumlah, "Jumlah potongan")
            per += c
        if jumlah > n["sisa"]:
            raise Gagal("Potongan %s melebihi sisa nota %s (%s). Tidak dicatat." % (rp(jumlah), n["no_nota"],
                                                                                  rp(n["sisa"])))
        tgl_p = max(tgl.isoformat(), n["tanggal"])
        conn.execute("INSERT INTO potongan(nota_id, tanggal, jumlah, alasan, dibuat) VALUES (?,?,?,?,?)",
                     (n["id"], tgl_p, jumlah, bersih(args.alasan, 200), stempel()))
        sisa = n["sisa"] - jumlah
        t = ("Potongan %s pada nota %s (%s), alasan: %s.\nSisa nota: %s -> %s%s" %
             (rp(jumlah), n["no_nota"], n["pelanggan"], bersih(args.alasan, 200), rp(n["sisa"]), rp(sisa),
              " (LUNAS)" if sisa == 0 else ""))
        return {"no_nota": n["no_nota"], "jumlah": jumlah, "sisa_nota": sisa, "peringatan": per,
                "ringkasan": {"potong": n["no_nota"], "jumlah": jumlah}}, t
    return jalankan_tulis(args, "potong", kerja, besar=True, label_backup="sebelum-potong")


def cmd_batal_nota(args):
    def kerja(conn, cfg):
        nota = cari_nota(conn, args.nota)
        if not bersih(args.alasan):
            raise Gagal("Alasan pembatalan wajib diisi (mis. 'salah catat', 'dobel', 'pesanan batal').")
        buku = Buku(conn)
        n = [x for x in buku.nota if x["id"] == nota["id"]][0]
        conn.execute("UPDATE nota SET status='batal', alasan_batal=?, tgl_batal=?, diubah=? WHERE id=?",
                     (bersih(args.alasan, 200), hari_ini().isoformat(), stempel(), n["id"]))
        t = "Nota %s (%s, %s) DIBATALKAN, alasan: %s." % (n["no_nota"], n["pelanggan"], rp(n["nominal"]),
                                                         bersih(args.alasan, 200))
        if n["dibayar"]:
            t += ("\nPembayaran %s yang sudah masuk ke nota ini menjadi deposit/kelebihan bayar %s (bisa dipakai untuk "
                  "nota lain dengan pakai-kredit, atau dicatat dikembalikan dengan kembalikan)." %
                  (rp(n["dibayar"]), n["pelanggan"]))
        buku2 = Buku(conn)
        t += "\n" + saldo_teks(buku2, n["pelanggan_id"])
        return {"no_nota": n["no_nota"], "dibayar_jadi_deposit": n["dibayar"],
                "ringkasan": {"batal_nota": n["no_nota"]}}, t
    return jalankan_tulis(args, "batal-nota", kerja, besar=True, label_backup="sebelum-batal-nota")


def cmd_batal_bayar(args):
    def kerja(conn, cfg):
        m = re.fullmatch(r"(?i)b0*(\d{1,6})", str(args.bayar or "").strip())
        if not m:
            raise Gagal("Kode pembayaran harus seperti B0003 (lihat: piutang.py saldo --pelanggan <nama>).")
        b = conn.execute("SELECT * FROM pembayaran WHERE id=?", (int(m.group(1)),)).fetchone()
        if not b:
            raise Gagal("Pembayaran %s tidak ada." % args.bayar.upper())
        if b["status"] != "aktif":
            raise Gagal("Pembayaran %s sudah dibatalkan sebelumnya." % kode_b(b["id"]))
        if not bersih(args.alasan):
            raise Gagal("Alasan pembatalan wajib diisi (mis. 'salah catat', 'transfer ditolak bank').")
        p = conn.execute("SELECT * FROM pelanggan WHERE id=?", (b["pelanggan_id"],)).fetchone()
        alok = conn.execute("SELECT a.jumlah, n.no_nota FROM alokasi a JOIN nota n ON n.id=a.nota_id WHERE "
                            "a.pembayaran_id=? AND n.status='aktif'", (b["id"],)).fetchall()
        conn.execute("UPDATE pembayaran SET status='batal', alasan_batal=?, tgl_batal=? WHERE id=?",
                     (bersih(args.alasan, 200), hari_ini().isoformat(), b["id"]))
        buku = Buku(conn)
        t = ("Pembayaran %s (%s dari %s, %s) DIBATALKAN, alasan: %s.\nNota yang kembali terbuka: %s\n%s" %
             (kode_b(b["id"]), rp(b["jumlah"]), p["nama"], tgl_pendek(b["tanggal"]), bersih(args.alasan, 200),
              ", ".join("%s +%s" % (a["no_nota"], rp(a["jumlah"])) for a in alok) or "-", saldo_teks(buku, p["id"])))
        return {"kode": kode_b(b["id"]), "jumlah": b["jumlah"], "saldo_pelanggan": buku.piutang_pel(p["id"]),
                "ringkasan": {"batal_bayar": kode_b(b["id"])}}, t
    return jalankan_tulis(args, "batal-bayar", kerja, besar=True, label_backup="sebelum-batal-bayar")


# --------------------------------------------------------------------------- perintah: laporan (hanya baca)
def per_dari_args(args, hari):
    if not getattr(args, "per", None):
        return None
    d, _ = baca_tgl(args.per, hari, "bebas", hari=hari)
    return d


def baris_nota(n, samarkan=False, dengan_nama=True):
    s = "%s | %s" % (n["no_nota"], ("%s (%s) | " % (samar_nama(n["pelanggan"]) if samarkan else n["pelanggan"],
                                                   kode_p(n["pelanggan_id"]))) if dengan_nama else "")
    s = s.rstrip(" |") + " | "
    s += "sisa %s" % rp(n["sisa"])
    if n["dibayar"] or n["dipotong"]:
        s += " dari %s" % rp(n["nominal"])
    s += " | " + telat_teks(n["telat"], n["jatuh_tempo"])
    if n["diingatkan"]:
        s += " | diingatkan %dx%s" % (n["diingatkan"], (" (terakhir %s)" % tgl_pendek(n["terakhir_diingatkan"], False))
                                      if n["terakhir_diingatkan"] else "")
    return s


def potong_daftar(daftar, semua, maks=MAKS_BARIS):
    if semua or len(daftar) <= maks:
        return daftar, 0
    return daftar[:maks], len(daftar) - maks


def cmd_saldo(args):
    conn = _baca(args)
    try:
        hari = hari_ini()
        per = per_dari_args(args, hari)
        buku = Buku(conn, per)
        sam = args.samarkan
        judul_per = tgl_panjang(per or hari)
        if args.pelanggan:
            p = cari_pelanggan(conn, args.pelanggan)
            pid = p["id"]
            semua_nota = [n for n in buku.nota if n["pelanggan_id"] == pid]
            terbuka = [n for n in semua_nota if n["sisa"] > 0]
            lunas = [n for n in semua_nota if n["sisa"] == 0][-5:]
            bayar = conn.execute("SELECT * FROM pembayaran WHERE pelanggan_id=? ORDER BY tanggal DESC, id DESC LIMIT 10",
                                 (pid,)).fetchall()
            kemb = conn.execute("SELECT * FROM pengembalian WHERE pelanggan_id=? ORDER BY tanggal DESC, id DESC "
                                "LIMIT 5", (pid,)).fetchall()
            piut, kred = buku.piutang_pel(pid), buku.kredit_pel(pid)
            t = ["SALDO %s (%s) | WA %s | per %s" % (nama_tampil(p, sam), kode_p(pid),
                                                     samar_wa(p["wa"]) if sam else tampil_wa(p["wa"]), judul_per),
                 "Piutang: %s (%d nota terbuka) | Kelebihan bayar/deposit: %s | Saldo bersih: %s" %
                 (rp(piut), len(terbuka), rp(kred), rp(piut - kred))]
            t.append("\nNOTA TERBUKA (%d)" % len(terbuka))
            for i, n in enumerate(terbuka, 1):
                t.append("%d. %s | tgl %s | nominal %s | dibayar %s%s | sisa %s | %s%s" % (
                    i, n["no_nota"], tgl_pendek(n["tanggal"]), rp(n["nominal"]), rp(n["dibayar"]),
                    (" | potongan %s" % rp(n["dipotong"])) if n["dipotong"] else "", rp(n["sisa"]),
                    telat_teks(n["telat"], n["jatuh_tempo"]),
                    (" | diingatkan %dx" % n["diingatkan"]) if n["diingatkan"] else ""))
            if lunas:
                t.append("\nNOTA LUNAS (maks. 5 terakhir)")
                t += ["- %s | tgl %s | %s" % (n["no_nota"], tgl_pendek(n["tanggal"]), rp(n["nominal"])) for n in lunas]
            if bayar:
                t.append("\nPEMBAYARAN (maks. 10 terakhir)")
                for b in bayar:
                    al = conn.execute("SELECT a.jumlah, n.no_nota, n.status FROM alokasi a JOIN nota n ON "
                                      "n.id=a.nota_id WHERE a.pembayaran_id=?", (b["id"],)).fetchall()
                    t.append("- %s | %s | %s%s%s -> %s" % (
                        kode_b(b["id"]), tgl_pendek(b["tanggal"]), rp(b["jumlah"]),
                        (" | " + b["metode"]) if b["metode"] else "",
                        " | DIBATALKAN (%s)" % b["alasan_batal"] if b["status"] != "aktif" else "",
                        ", ".join("%s %s%s" % (a["no_nota"], rp(a["jumlah"]), " (nota batal)" if a["status"] != "aktif"
                                               else "") for a in al) or "deposit"))
            if kemb:
                t.append("\nPENGEMBALIAN KELEBIHAN BAYAR")
                t += ["- %s | %s | %s" % (tgl_pendek(k["tanggal"]), rp(k["jumlah"]), k["catatan"] or "-") for k in kemb]
            teks = "\n".join(t)
            return {"ok": True, "mode": "baca", "per": (per or hari).isoformat(), "kode_pelanggan": kode_p(pid),
                    "pelanggan": nama_tampil(p, sam), "piutang": piut, "kredit": kred, "saldo_bersih": piut - kred,
                    "umur": buku.umur(pid), "nota_terbuka": [nota_json(n, sam) for n in terbuka],
                    "data_sensitif": not sam, "teks": teks}, teks
        rows = []
        for pid, p in buku.pel.items():
            piut, kred = buku.piutang_pel(pid), buku.kredit_pel(pid)
            if not (piut or kred or args.semua):
                continue
            tb = buku.terbuka_pel(pid)
            terlewat = sum(n["sisa"] for n in tb if n["telat"] > 0)
            rows.append({"kode": kode_p(pid), "pelanggan": nama_tampil(p, sam), "piutang": piut, "kredit": kred,
                         "saldo_bersih": piut - kred, "jumlah_nota": len(tb), "terlewat": terlewat,
                         "telat_maks_hari": max([n["telat"] for n in tb] + [0])})
        rows.sort(key=lambda r: (-r["piutang"], r["kode"]))
        tampil, lebih = potong_daftar(rows, args.semua, 50)
        t = ["SALDO PIUTANG PER PELANGGAN - per %s" % judul_per,
             "Total piutang: %s (%d nota, %d pelanggan) | Kelebihan bayar pelanggan: %s" %
             (rp(buku.total()), len(buku.terbuka), len([r for r in rows if r["piutang"]]),
              rp(sum(r["kredit"] for r in rows)))]
        if not rows:
            t.append("Tidak ada piutang terbuka.")
        for i, r in enumerate(tampil, 1):
            s = "%d. %s (%s) | piutang %s (%d nota)" % (i, r["pelanggan"], r["kode"], rp(r["piutang"]),
                                                       r["jumlah_nota"])
            if r["terlewat"]:
                s += " | terlewat %s, paling lama %d hari" % (rp(r["terlewat"]), r["telat_maks_hari"])
            if r["kredit"]:
                s += " | deposit %s | saldo bersih %s" % (rp(r["kredit"]), rp(r["saldo_bersih"]))
            t.append(s)
        if lebih:
            t.append("... dan %d pelanggan lainnya (--semua untuk semuanya)." % lebih)
        teks = "\n".join(t)
        return {"ok": True, "mode": "baca", "per": (per or hari).isoformat(), "total_piutang": buku.total(),
                "total_kredit": sum(r["kredit"] for r in rows), "pelanggan": rows, "data_sensitif": not sam,
                "teks": teks}, teks
    finally:
        conn.close()


def teks_umur(um, total):
    return " | ".join("%s %s (%s)" % (LABEL_UMUR[k], rp(um[k]["nominal"]), persen(um[k]["nominal"], total)[1])
                      for k, _ in UMUR)


def cmd_umur(args):
    conn = _baca(args)
    try:
        hari = hari_ini()
        per = per_dari_args(args, hari)
        buku = Buku(conn, per)
        sam = args.samarkan
        total = buku.total()
        um = buku.umur()
        rows = []
        for pid, p in buku.pel.items():
            if not buku.piutang_pel(pid):
                continue
            u = buku.umur(pid)
            rows.append({"kode": kode_p(pid), "pelanggan": nama_tampil(p, sam), "total": buku.piutang_pel(pid),
                         "umur": {k: u[k]["nominal"] for k, _ in UMUR}})
        rows.sort(key=lambda r: (-sum(r["umur"][k] for k in ("lebih_90", "61_90", "31_60")), -r["total"]))
        tampil, lebih = potong_daftar(rows, args.semua)
        t = ["UMUR PIUTANG - per %s" % tgl_panjang(per or hari),
             "Total piutang: %s (%d nota)" % (rp(total), len(buku.terbuka))]
        if total:
            t.append(teks_umur(um, total))
            t.append("")
            for i, r in enumerate(tampil, 1):
                bag = " + ".join("%s %s" % (LABEL_UMUR[k], rp(r["umur"][k])) for k, _ in UMUR if r["umur"][k])
                t.append("%d. %s (%s): %s = %s" % (i, r["pelanggan"], r["kode"], rp(r["total"]), bag))
            if lebih:
                t.append("... dan %d pelanggan lainnya (--semua)." % lebih)
        else:
            t.append("Tidak ada piutang terbuka.")
        teks = "\n".join(t)
        return {"ok": True, "mode": "baca", "per": (per or hari).isoformat(), "total_piutang": total,
                "umur": um, "pelanggan": rows, "data_sensitif": not sam, "teks": teks}, teks
    finally:
        conn.close()


def kelompok_jatuh_tempo(buku):
    terlewat = sorted([n for n in buku.terbuka if n["telat"] > 0], key=lambda n: (-n["telat"], -n["sisa"]))
    hari_ini_ = [n for n in buku.terbuka if n["telat"] == 0]
    minggu = sorted([n for n in buku.terbuka if -7 <= n["telat"] < 0], key=lambda n: -n["telat"])
    return terlewat, hari_ini_, minggu


def ringkas_kelompok(daftar):
    return {"jumlah_nota": len(daftar), "nominal": sum(n["sisa"] for n in daftar),
            "jumlah_pelanggan": len({n["pelanggan_id"] for n in daftar})}


def teks_kelompok(judul, daftar, sam, semua, maks=MAKS_BARIS):
    if not daftar:
        return []
    tampil, lebih = potong_daftar(daftar, semua, maks)
    t = ["", "%s (%d nota, %s)" % (judul, len(daftar), rp(sum(n["sisa"] for n in daftar)))]
    t += ["%d. %s" % (i, baris_nota(n, sam)) for i, n in enumerate(tampil, 1)]
    if lebih:
        t.append("... dan %d nota lainnya (--semua)." % lebih)
    return t


def cmd_jatuh_tempo(args):
    conn = _baca(args)
    try:
        hari = hari_ini()
        buku = Buku(conn)
        sam = args.samarkan
        a, b, c = kelompok_jatuh_tempo(buku)
        t = ["JATUH TEMPO PIUTANG - %s (%s)" % (tgl_panjang(hari), _JAM["zona"]),
             "Terlewat: %s (%d nota) | Hari ini: %s (%d) | 7 hari ke depan: %s (%d)" %
             (rp(sum(n["sisa"] for n in a)), len(a), rp(sum(n["sisa"] for n in b)), len(b),
              rp(sum(n["sisa"] for n in c)), len(c))]
        t += teks_kelompok("TERLEWAT", a, sam, args.semua)
        t += teks_kelompok("JATUH TEMPO HARI INI", b, sam, args.semua)
        t += teks_kelompok("MINGGU INI (besok s.d. %s)" % tgl_pendek(hari + timedelta(days=7)), c, sam, args.semua)
        if not (a or b or c):
            t.append("Tidak ada tagihan yang terlewat atau jatuh tempo dalam 7 hari.")
        else:
            t.append("\nDraf pesan tagihan: minta \"bikinin pesan tagihan untuk <pelanggan>\". Pesan dikirim sendiri, "
                     "satu per satu.")
        teks = "\n".join(t)
        return {"ok": True, "mode": "baca", "tanggal": hari.isoformat(),
                "terlewat": [nota_json(n, sam) for n in a], "hari_ini": [nota_json(n, sam) for n in b],
                "minggu_ini": [nota_json(n, sam) for n in c],
                "ringkasan": {"terlewat": ringkas_kelompok(a), "hari_ini": ringkas_kelompok(b),
                              "minggu_ini": ringkas_kelompok(c)}, "data_sensitif": not sam, "teks": teks}, teks
    finally:
        conn.close()


def masuk_tanggal(conn, d):
    r = conn.execute("SELECT COUNT(*), IFNULL(SUM(jumlah),0) FROM pembayaran WHERE status='aktif' AND tanggal=?",
                     (d.isoformat(),)).fetchone()
    return r[0], r[1]


def cmd_ringkasan(args):
    """Ringkasan harian untuk pemilik (jadwal OpenClaw -> Telegram). Hanya membaca."""
    conn = _baca(args)
    try:
        hari = hari_ini()
        cfg = pengaturan(conn)
        buku = Buku(conn)
        sam = args.samarkan
        a, b, c = kelompok_jatuh_tempo(buku)
        total = buku.total()
        n_kem, j_kem = masuk_tanggal(conn, hari - timedelta(days=1))
        n_hi, j_hi = masuk_tanggal(conn, hari)
        kredit = sum(v for v in buku.kredit.values() if v > 0)
        t = ["RINGKASAN PIUTANG%s - %s (%s)" % ((" " + cfg["nama_usaha"]) if cfg["nama_usaha"] else "",
                                                tgl_panjang(hari), _JAM["zona"]),
             "Total piutang: %s (%d nota, %d pelanggan)" % (rp(total), len(buku.terbuka),
                                                           len({n["pelanggan_id"] for n in buku.terbuka})),
             "Terlewat: %s (%d nota) | Hari ini: %s (%d) | 7 hari ke depan: %s (%d)" %
             (rp(sum(n["sisa"] for n in a)), len(a), rp(sum(n["sisa"] for n in b)), len(b),
              rp(sum(n["sisa"] for n in c)), len(c)),
             "Pembayaran masuk kemarin: %s (%d) | hari ini: %s (%d)" % (rp(j_kem), n_kem, rp(j_hi), n_hi)]
        if total:
            t.append("Umur: " + teks_umur(buku.umur(), total))
        if kredit:
            t.append("Kelebihan bayar pelanggan (deposit) belum dipakai: %s" % rp(kredit))
        maks = 10
        t += teks_kelompok("TERLEWAT", a, sam, args.semua, maks)
        t += teks_kelompok("JATUH TEMPO HARI INI", b, sam, args.semua, maks)
        t += teks_kelompok("MINGGU INI", c, sam, args.semua, maks)
        if a or b:
            t.append("\nMinta draf pesan tagihan ke agent di komputer Anda (mis. \"pesan tagihan untuk %s\"). Pesan "
                     "dikirim sendiri, satu per satu." % kode_p((a or b)[0]["pelanggan_id"]))
        teks = "\n".join(t)
        return {"ok": True, "mode": "baca", "tanggal": hari.isoformat(), "total_piutang": total,
                "terlewat": ringkas_kelompok(a), "hari_ini": ringkas_kelompok(b), "minggu_ini": ringkas_kelompok(c),
                "pembayaran_kemarin": {"jumlah": n_kem, "nominal": j_kem},
                "pembayaran_hari_ini": {"jumlah": n_hi, "nominal": j_hi}, "kredit_pelanggan": kredit,
                "umur": buku.umur(), "data_sensitif": not sam, "teks": teks}, teks
    finally:
        conn.close()


def periode_nama(p, acuan):
    p = (p or "bulan-ini").lower()
    if p in ("hari-ini", "harian"):
        return "hari ini", acuan, acuan
    if p == "kemarin":
        d = acuan - timedelta(days=1)
        return "kemarin", d, d
    if p == "minggu-ini":
        a = acuan - timedelta(days=acuan.weekday())
        return "minggu ini", a, a + timedelta(days=6)
    if p == "minggu-lalu":
        a = acuan - timedelta(days=acuan.weekday() + 7)
        return "minggu lalu", a, a + timedelta(days=6)
    if p == "bulan-ini":
        a = acuan.replace(day=1)
        return "bulan %s %d" % (BULAN[a.month - 1], a.year), a, _tambah_bulan(a, 1) - timedelta(days=1)
    if p == "bulan-lalu":
        a = _tambah_bulan(acuan.replace(day=1), -1)
        return "bulan %s %d" % (BULAN[a.month - 1], a.year), a, acuan.replace(day=1) - timedelta(days=1)
    if p == "tahun-ini":
        return "tahun %d" % acuan.year, date(acuan.year, 1, 1), date(acuan.year, 12, 31)
    if p == "semua":
        return "semua waktu", date(2000, 1, 1), date(2100, 12, 31)
    raise Gagal("Periode '%s' tidak dikenal. Pilihan: hari-ini, kemarin, minggu-ini, minggu-lalu, bulan-ini, "
                "bulan-lalu, tahun-ini, semua (atau --dari/--sampai)." % p)


def periode_dari_args(args, acuan):
    if args.dari or args.sampai:
        if not (args.dari and args.sampai):
            raise Gagal("--dari dan --sampai harus diisi keduanya.")
        a, _ = baca_tgl(args.dari, acuan, "lalu", hari=acuan)
        b, _ = baca_tgl(args.sampai, acuan, "bebas", hari=acuan)
        if b < a:
            raise Gagal("--sampai lebih awal dari --dari.")
        return "%s - %s" % (tgl_pendek(a), tgl_pendek(b)), a, b
    return periode_nama(args.periode, acuan)


RUMUS = {
    "sisa_nota": "Sisa nota = nominal - pembayaran yang dialokasikan ke nota itu - potongan (retur/diskon/hapus).",
    "total_piutang": "Total piutang = jumlah sisa semua nota aktif yang belum lunas (nota batal tidak dihitung).",
    "kredit": "Kelebihan bayar/deposit pelanggan = pembayaran - bagian yang sudah dipakai untuk nota - pengembalian.",
    "umur": "Umur = tanggal posisi - jatuh tempo (hari kalender). 0 atau minus = belum jatuh tempo; 1-30, 31-60, "
            "61-90, >90 hari. Persen = nominal kelompok / total piutang, 1 desimal (0,05 ke atas).",
    "alokasi": "Pembayaran tanpa nomor nota dipakai untuk nota dengan jatuh tempo paling awal lebih dulu.",
    "periode": "Nota baru = nota bertanggal di periode; pembayaran = pembayaran aktif bertanggal di periode; posisi "
               "dihitung per akhir periode (atau hari ini bila periode belum selesai).",
}


def cmd_rekap(args):
    conn = _baca(args)
    try:
        hari = hari_ini()
        nama, a, b = periode_dari_args(args, hari)
        per = min(b, hari)
        sam = args.samarkan
        buku_per = Buku(conn, per)
        buku_kini = Buku(conn)
        rng = (a.isoformat(), b.isoformat())

        def satu(sql):
            r = conn.execute(sql, rng).fetchone()
            return {"jumlah": r[0], "nominal": r[1]}

        nota_baru = satu("SELECT COUNT(*), IFNULL(SUM(nominal),0) FROM nota WHERE status='aktif' AND tanggal BETWEEN ? "
                         "AND ?")
        bayar = satu("SELECT COUNT(*), IFNULL(SUM(jumlah),0) FROM pembayaran WHERE status='aktif' AND tanggal BETWEEN "
                     "? AND ?")
        potong = satu("SELECT COUNT(*), IFNULL(SUM(p.jumlah),0) FROM potongan p JOIN nota n ON n.id=p.nota_id WHERE "
                      "n.status='aktif' AND p.tanggal BETWEEN ? AND ?")
        kembali = satu("SELECT COUNT(*), IFNULL(SUM(jumlah),0) FROM pengembalian WHERE tanggal BETWEEN ? AND ?")
        batal = satu("SELECT COUNT(*), IFNULL(SUM(nominal),0) FROM nota WHERE status='batal' AND tgl_batal BETWEEN ? "
                     "AND ?")
        total_per = buku_per.total()
        um = buku_per.umur()
        ja, jb, jc = kelompok_jatuh_tempo(buku_kini)
        per_pel = {}
        for n in ja:
            d = per_pel.setdefault(n["pelanggan_id"], {"sisa_terlewat": 0, "telat_maks_hari": 0})
            d["sisa_terlewat"] += n["sisa"]
            d["telat_maks_hari"] = max(d["telat_maks_hari"], n["telat"])
        teratas = sorted(per_pel.items(), key=lambda kv: -kv[1]["sisa_terlewat"])[:5]
        teratas = [dict(v, kode=kode_p(pid), pelanggan=nama_tampil(buku_kini.pel[pid], sam)) for pid, v in teratas]
        kredit = sum(v for v in buku_per.kredit.values() if v > 0)
        posisi = {"per": per.isoformat(), "total_piutang": total_per, "jumlah_nota_terbuka": len(buku_per.terbuka),
                  "jumlah_pelanggan_berpiutang": len({n["pelanggan_id"] for n in buku_per.terbuka}),
                  "kredit_pelanggan": kredit, "umur": um,
                  "persen_terlewat": persen(total_per - um["belum_jatuh_tempo"]["nominal"], total_per)[0]}
        t = ["REKAP PIUTANG - %s (%s s.d. %s)" % (nama, tgl_pendek(a), tgl_pendek(b)),
             "Nota piutang baru: %d nota, %s" % (nota_baru["jumlah"], rp(nota_baru["nominal"])),
             "Pembayaran diterima: %d kali, %s" % (bayar["jumlah"], rp(bayar["nominal"])),
             "Potongan (retur/diskon/hapus): %s | Nota dibatalkan: %d (%s) | Kelebihan bayar dikembalikan: %s" %
             (rp(potong["nominal"]), batal["jumlah"], rp(batal["nominal"]), rp(kembali["nominal"])),
             "Posisi per %s: piutang %s (%d nota, %d pelanggan)%s" %
             (tgl_pendek(per), rp(total_per), posisi["jumlah_nota_terbuka"], posisi["jumlah_pelanggan_berpiutang"],
              (" | deposit pelanggan %s" % rp(kredit)) if kredit else "")]
        if total_per:
            t.append("Umur: " + teks_umur(um, total_per))
        t.append("Status hari ini (%s): terlewat %s (%d nota) | jatuh tempo hari ini %s (%d) | 7 hari ke depan %s (%d)"
                 % (tgl_pendek(hari), rp(sum(n["sisa"] for n in ja)), len(ja), rp(sum(n["sisa"] for n in jb)),
                    len(jb), rp(sum(n["sisa"] for n in jc)), len(jc)))
        if teratas:
            t.append("Terlewat terbesar: " + "; ".join("%d. %s (%s) %s, paling lama %d hari" % (
                i, r["pelanggan"], r["kode"], rp(r["sisa_terlewat"]), r["telat_maks_hari"])
                for i, r in enumerate(teratas, 1)))
        if args.rumus:
            t.append("\nRUMUS")
            t += ["- " + v for v in RUMUS.values()]
        teks = "\n".join(t)
        return {"ok": True, "mode": "baca", "skema_json": SKEMA_JSON_REKAP, "aplikasi": APLIKASI, "versi": VERSI,
                "hari_ini": hari.isoformat(), "zona": _JAM["zona"],
                "periode": {"nama": nama, "dari": a.isoformat(), "sampai": b.isoformat()},
                "arus_periode": {"nota_baru": nota_baru, "pembayaran_masuk": bayar, "potongan": potong,
                                 "nota_dibatalkan": batal, "kelebihan_dikembalikan": kembali},
                "posisi": posisi,
                "jatuh_tempo": {"terlewat": ringkas_kelompok(ja), "hari_ini": ringkas_kelompok(jb),
                                "tujuh_hari": ringkas_kelompok(jc)},
                "teratas_terlewat": teratas, "data_sensitif": not sam, "rumus": RUMUS, "teks": teks}, teks
    finally:
        conn.close()


# --------------------------------------------------------------------------- draf pesan tagihan
def pilih_nota_tagih(buku, pid, nota=None):
    terbuka = buku.terbuka_pel(pid)
    if nota is not None:
        sel = [n for n in terbuka if n["id"] == nota["id"]]
        if not sel:
            raise Gagal("Nota %s sudah lunas; tidak perlu ditagih." % nota["no_nota"])
        return sel, None
    if not terbuka:
        raise Gagal("%s tidak punya tagihan terbuka; tidak perlu ditagih." % buku.pel[pid]["nama"], lunas=True)
    sel = [n for n in terbuka if n["telat"] >= -7]
    if not sel:
        return terbuka, "Belum ada nota %s yang jatuh tempo dalam 7 hari; draf berupa pengingat awal." % \
            buku.pel[pid]["nama"]
    return sel, None


def susun_draf(p, notas, cfg):
    sapa = panggilan(p, cfg)
    usaha, pengirim, rek = bersih(cfg.get("nama_usaha")), bersih(cfg.get("pengirim")), bersih(cfg.get("rekening"))
    if pengirim and usaha:
        diri = " Saya %s dari %s." % (pengirim, usaha)
    elif pengirim:
        diri = " Saya %s." % pengirim
    elif usaha:
        diri = " Kami dari %s." % usaha
    else:
        diri = ""
    maks = max(n["telat"] for n in notas)
    if maks < 0:
        jenis, buka_ = "pengingat-awal", "Izin mengingatkan tagihan yang akan jatuh tempo:"
    elif maks == 0:
        jenis, buka_ = "hari-jatuh-tempo", "Izin mengingatkan, tagihan berikut jatuh tempo hari ini:"
    elif maks <= 6:
        jenis, buka_ = "terlewat-ringan", ("Sepertinya tagihan berikut terlewat, karena pembayarannya belum kami "
                                           "terima:")
    elif maks <= 29:
        jenis, buka_ = "terlewat", "Kami ingin menanyakan tagihan berikut yang sudah melewati jatuh tempo:"
    else:
        jenis, buka_ = "terlewat-lama", ("Kami ingin menanyakan kembali tagihan berikut yang sudah cukup lama melewati "
                                         "jatuh tempo:")
    baris = []
    for n in notas:
        s = "- Nota %s (%s): %s%s, jatuh tempo %s" % (n["no_nota"], tgl_pendek(n["tanggal"]),
                                                      "sisa " if (n["dibayar"] or n["dipotong"]) else "",
                                                      rp(n["sisa"]), tgl_pendek(n["jatuh_tempo"]))
        if n["telat"] == 0:
            s += " (hari ini)"
        baris.append(s)
    t = ["Halo %s, semoga sehat selalu.%s" % (sapa, diri), "", buka_] + baris
    if len(notas) > 1:
        t.append("Total: %s" % rp(sum(n["sisa"] for n in notas)))
    t.append("")
    t.append(("Pembayaran bisa ditransfer ke %s." % rek) if rek else "Pembayaran bisa melalui cara yang biasa.")
    if jenis in ("pengingat-awal", "hari-jatuh-tempo", "terlewat-ringan"):
        t.append("Kalau sudah membayar, mohon kirimkan bukti transfernya dan abaikan pesan ini ya.")
    else:
        t.append("Mohon dibantu informasikan kapan rencana pembayarannya, supaya bisa kami catat. Kalau sudah "
                 "membayar, mohon kirimkan bukti transfernya.")
    if jenis == "terlewat-lama":
        t.append("Kalau ada kendala, kami terbuka membicarakan jadwal pembayaran bertahap.")
    t.append("Terima kasih atas perhatiannya.")
    return jenis, "\n".join(t)


def cmd_draf(args):
    conn = _baca(args)
    try:
        cfg = pengaturan(conn)
        buku = Buku(conn)
        nota = cari_nota(conn, args.nota) if args.nota else None
        if nota and args.pelanggan:
            p = cari_pelanggan(conn, args.pelanggan)
            if p["id"] != nota["pelanggan_id"]:
                raise Gagal("Nota %s bukan milik %s." % (nota["no_nota"], p["nama"]))
        elif nota:
            p = conn.execute("SELECT * FROM pelanggan WHERE id=?", (nota["pelanggan_id"],)).fetchone()
        else:
            p = cari_pelanggan(conn, args.pelanggan)
        p = dict(p)
        notas, cat = pilih_nota_tagih(buku, p["id"], nota)
        per = [cat] if cat else []
        jenis, draf = susun_draf(p, notas, cfg)
        if args.pesan:
            draf = str(args.pesan).strip()
            jenis = "pesan-sendiri"
        kredit = buku.kredit_pel(p["id"])
        if kredit > 0:
            per.append("%s punya kelebihan bayar/deposit %s yang belum dipakai. Sebaiknya jalankan pakai-kredit dulu "
                       "sebelum menagih." % (p["nama"], rp(kredit)))
        if not cfg.get("rekening"):
            per.append("Rekening belum diatur; draf menulis 'cara yang biasa'. Atur: piutang.py atur --rekening "
                       "\"BCA 123... a.n. ...\".")
        maks = max(n["telat"] for n in notas)
        ingat = max(n["diingatkan"] for n in notas)
        saran = []
        if maks >= 14 or ingat >= 2:
            saran.append("Tagihan ini sudah lewat %d hari / diingatkan %dx. Untuk pemberitahuan resmi bertahap atau "
                         "surat teguran, pakai skill tagih-piutang (data: piutang.py ekspor --format tagih-piutang)."
                         % (maks, ingat))
        tautan = link_wa(p["wa"], draf)
        t = "DRAF PESAN TAGIHAN untuk %s (%s) [%s] - periksa dulu, lalu kirim sendiri:\n\n%s" % (
            p["nama"], kode_p(p["id"]), jenis, draf)
        if tautan:
            t += "\n\nBuka di WhatsApp (teks sudah terisi, tekan Kirim sendiri):\n" + tautan
        else:
            t += "\n\n(Nomor WA pelanggan belum ada; salin teks di atas. Tambah nomor: ubah-pelanggan --wa ...)"
        t += "\nSetelah terkirim: piutang.py terkirim --pelanggan %s" % kode_p(p["id"])
        if saran:
            t += "\n" + "\n".join("Saran: " + s for s in saran)
        if per:
            t += "\n" + "\n".join("Catatan: " + x for x in per)
        return {"ok": True, "mode": "baca", "kode_pelanggan": kode_p(p["id"]), "pelanggan": p["nama"],
                "jenis": jenis, "draf": draf, "tautan_wa": tautan, "nota": [nota_json(n) for n in notas],
                "total": sum(n["sisa"] for n in notas), "saran": saran, "peringatan": per, "teks": t}, t
    finally:
        conn.close()


def cmd_terkirim(args):
    def kerja(conn, cfg):
        hari = hari_ini()
        buku = Buku(conn)
        nota = cari_nota(conn, args.nota) if args.nota else None
        if nota:
            pid = nota["pelanggan_id"]
        else:
            pid = cari_pelanggan(conn, args.pelanggan)["id"]
        notas, _ = pilih_nota_tagih(buku, pid, nota)
        sudah = [n for n in notas if n["terakhir_diingatkan"] == hari.isoformat()]
        baru = [n for n in notas if n not in sudah]
        if not baru:
            raise Gagal("Pengingat untuk nota %s sudah dicatat hari ini; tidak dihitung dobel." %
                        ", ".join(n["no_nota"] for n in sudah))
        for n in baru:
            conn.execute("UPDATE nota SET diingatkan=diingatkan+1, terakhir_diingatkan=?, diubah=? WHERE id=?",
                         (hari.isoformat(), stempel(), n["id"]))
        t = "Dicatat: pengingat sudah dikirim untuk %s (%s): %s." % (
            buku.pel[pid]["nama"], kode_p(pid), ", ".join("%s (ke-%d)" % (n["no_nota"], n["diingatkan"] + 1)
                                                          for n in baru))
        per = ["Nota %s sudah dicatat hari ini; dilewati." % ", ".join(n["no_nota"] for n in sudah)] if sudah else []
        return {"kode_pelanggan": kode_p(pid), "nota": [n["no_nota"] for n in baru], "peringatan": per,
                "ringkasan": {"terkirim": [n["no_nota"] for n in baru]}}, t
    return jalankan_tulis(args, "terkirim", kerja)


# --------------------------------------------------------------------------- CSV
def sel_aman(v):
    """Cegah formula injection saat CSV dibuka di Excel/Sheets (teks diawali = + - @ tab CR diberi ')."""
    if v is None:
        return ""
    if isinstance(v, (int, float)):
        return v
    s = str(v)
    if re.fullmatch(r"-?\d+(?:[.,]\d+)?", s):
        return s
    if s and s[0] in "=+-@\t\r":
        return "'" + s
    return s


def buang_pelindung(s):
    s = str(s or "")
    return s[1:] if len(s) > 1 and s[0] == "'" and s[1] in "=+-@\t\r" else s


def tulis_csv(path, header, rows, timpa=False, pemisah=";"):
    p = Path(path).expanduser().resolve()
    if p.exists() and not timpa:
        raise Gagal("File %s sudah ada. Pakai nama lain atau tambahkan --timpa bila memang ingin ditimpa." % p)
    if p.suffix.lower() != ".csv":
        raise Gagal("Nama file ekspor harus berakhiran .csv.")
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
    if p.suffix.lower() in (".xlsx", ".xls", ".ods", ".numbers", ".pdf"):
        raise Gagal("File %s belum didukung langsung. Di Excel/Sheets: File > Save As/Download > CSV, lalu kirim file "
                    "CSV-nya." % p.name)
    raw = p.read_bytes()
    if len(raw) > 20 * 1024 * 1024:
        raise Gagal("File terlalu besar (> 20 MB). Pecah menjadi beberapa file.")
    if b"\x00" in raw[:4096]:
        raise Gagal("File %s bukan file teks CSV (isinya biner). Simpan ulang dari Excel/Sheets sebagai CSV." % p.name)
    peringatan = []
    try:
        teks = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        teks = raw.decode("cp1252", errors="replace")
        peringatan.append("File bukan UTF-8; dibaca sebagai Windows-1252 (ANSI). Periksa huruf khusus di nama.")
    baris1 = teks.split("\n", 1)[0]
    pemisah = max([";", ",", "\t", "|"], key=lambda c: baris1.count(c))
    rows, pembaca, akhir, ganjil = [], csv.reader(io.StringIO(teks), delimiter=pemisah), 0, []
    for r in pembaca:
        awal, akhir = akhir + 1, pembaca.line_num
        if any(x.strip() for x in r):
            rows.append((awal, r))
            if akhir > awal:
                ganjil.append((awal, akhir))
    if not rows:
        raise Gagal("File %s kosong." % p.name)
    if ganjil:
        peringatan.append("%d baris dibaca menyatu dengan baris sesudahnya (%s): kemungkinan ada tanda kutip (\") yang "
                          "tidak tertutup. Periksa baris itu di file aslinya." %
                          (len(ganjil), ", ".join("%d-%d" % g for g in ganjil[:5])))
    return rows, peringatan


KOLOM_IMPOR = {
    "pelanggan": ("pelanggan", "nama pelanggan", "nama", "customer", "customer name", "nama customer", "pembeli",
                  "nama pembeli", "konsumen", "client", "klien", "nama klien", "nama toko", "debitur", "bill to"),
    "nota": ("no nota", "nomor nota", "nota", "no invoice", "nomor invoice", "invoice", "invoice no", "invoice number",
             "no faktur", "nomor faktur", "faktur", "no transaksi", "nomor transaksi", "receipt number", "receipt no",
             "order id", "no pesanan", "nomor pesanan", "id transaksi", "kode transaksi", "bill no", "no bon",
             "nomor bon", "no struk", "nomor struk"),
    "tanggal": ("tanggal", "tgl", "date", "tanggal nota", "tgl nota", "tanggal transaksi", "tgl transaksi",
                "tanggal invoice", "invoice date", "tanggal faktur", "waktu", "created at", "transaction date",
                "tanggal order", "tanggal pesanan", "tanggal bon"),
    "jatuh_tempo": ("jatuh tempo", "tgl jatuh tempo", "tanggal jatuh tempo", "jt", "due date", "due", "tempo",
                    "batas bayar", "batas pembayaran"),
    "nominal": ("nominal", "total", "jumlah", "grand total", "total tagihan", "amount", "nilai", "total harga",
                "tagihan", "total invoice", "total nota", "total bon", "nilai tagihan", "total belanja", "invoice total"),
    "dibayar": ("dibayar", "terbayar", "sudah dibayar", "paid", "amount paid", "bayar", "dp", "uang muka",
                "jumlah dibayar"),
    "sisa": ("sisa", "sisa tagihan", "outstanding", "balance", "balance due", "kurang bayar", "sisa piutang",
             "sisa bayar", "amount due"),
    "wa": ("no wa", "wa", "whatsapp", "no hp", "hp", "telepon", "telp", "phone", "no telp", "nomor wa", "nomor hp",
           "mobile", "no telepon", "phone number"),
    "keterangan": ("keterangan", "catatan", "note", "notes", "deskripsi", "description", "item", "produk", "barang",
                   "memo"),
    "status": ("status", "status bayar", "payment status", "status pembayaran", "metode bayar", "payment method",
               "metode pembayaran", "cara bayar", "payment type", "tipe pembayaran"),
    "termin": ("termin", "term", "terms", "top", "lama tempo", "payment terms"),
}
STATUS_KARTU = ("kartu kredit", "credit card", "kartu debit", "debit card", "cc")
STATUS_PIUTANG = ("belum lunas", "belum bayar", "belum dibayar", "unpaid", "tempo", "piutang", "bon", "hutang",
                  "utang", "kasbon", "kredit", "credit", "partial", "partially paid", "sebagian", "dp", "open",
                  "outstanding", "pending", "jatuh tempo", "overdue", "invoice", "nanti bayar", "bayar nanti")
STATUS_BATAL = ("batal", "dibatalkan", "void", "voided", "cancel", "cancelled", "canceled", "refund", "refunded",
                "retur", "returned")
STATUS_LUNAS = ("lunas", "paid", "sudah bayar", "sudah dibayar", "selesai", "completed", "complete", "settled",
                "tunai", "cash", "qris", "debit", "transfer", "e-wallet", "ewallet", "gopay", "ovo", "dana",
                "shopeepay", "edc", "success", "sukses", "berhasil")


def _norm_kolom(h):
    h = str(h or "").replace("﻿", "").strip().lower()
    h = re.sub(r"[_\s]+", " ", h).strip(" .:*#")
    return h


def petakan_kolom(header):
    peta, dipakai = {}, set()
    norm = [_norm_kolom(h) for h in header]
    for kunci, alias in KOLOM_IMPOR.items():
        for i, h in enumerate(norm):
            if i not in dipakai and h in alias:
                peta[kunci] = i
                dipakai.add(i)
                break
    abaikan = [header[i] for i in range(len(header)) if i not in dipakai and str(header[i]).strip()]
    return peta, abaikan


def jenis_status(teks):
    s = " %s " % re.sub(r"[^a-z0-9-]+", " ", str(teks or "").lower())
    if not s.strip():
        return None
    for daftar, jenis in ((STATUS_KARTU, "lunas"), (STATUS_PIUTANG, "piutang"), (STATUS_BATAL, "batal"),
                          (STATUS_LUNAS, "lunas")):
        if any((" %s " % x) in s for x in daftar):
            return jenis
    return "tidak_dikenal"


def deteksi_urutan(nilai):
    """Hitung bukti format: hari/bulan (angka pertama > 12) vs bulan/hari (angka kedua > 12)."""
    hb, bh = [], []
    for no, v in nilai:
        m = re.match(r"\s*(\d{1,2})[/.-](\d{1,2})[/.-]\d{2,4}", str(v or ""))
        if m:
            a, b = int(m.group(1)), int(m.group(2))
            if a > 12 >= b:
                hb.append((no, v))
            elif b > 12 >= a:
                bh.append((no, v))
    return hb, bh


def cmd_impor(args):
    rows, per_file = baca_csv(args.file)
    header_no, header = rows[0]
    data = rows[1:]
    peta, abaikan = petakan_kolom(header)
    if "pelanggan" not in peta or not ("nominal" in peta or "sisa" in peta) or "tanggal" not in peta:
        kurang = [k for k, ada in (("nama pelanggan", "pelanggan" in peta), ("tanggal", "tanggal" in peta),
                                   ("nominal/total", "nominal" in peta or "sisa" in peta)) if not ada]
        raise Gagal("Kolom wajib tidak ditemukan: %s. Judul kolom di file: %s. Ganti judul kolom (mis. 'pelanggan', "
                    "'no nota', 'tanggal', 'jatuh tempo', 'nominal', 'dibayar', 'no wa') lalu ulangi. Contoh: "
                    "templates/piutang-contoh.csv" % (", ".join(kurang), ", ".join(h for h in header if h) or "-"),
                    kolom=header)
    if not data:
        raise Gagal("File hanya berisi judul kolom, belum ada data.")

    def ambil(r, k):
        i = peta.get(k)
        return buang_pelindung(bersih(r[i], 200)) if i is not None and i < len(r) else ""

    nilai_tgl = [(no, ambil(r, "tanggal")) for no, r in data] + [(no, ambil(r, "jatuh_tempo")) for no, r in data]
    hb, bh = deteksi_urutan(nilai_tgl)
    urutan = args.format_tanggal or "hari-bulan"
    if not args.format_tanggal:
        if bh and hb:
            raise Gagal("Format tanggal di file ini CAMPUR: ada yang hari/bulan (baris %d '%s') dan bulan/hari (baris "
                        "%d '%s'). Tanggal seperti 03/10/2026 tidak bisa dipastikan. Rapikan kolom tanggal dulu di "
                        "Excel (format dd/mm/yyyy), lalu ulangi. Tidak ada yang diimpor." %
                        (hb[0][0], hb[0][1], bh[0][0], bh[0][1]), format_tanggal="campur")
        if bh:
            raise Gagal("Kolom tanggal tampaknya berformat bulan/hari (gaya Amerika), mis. baris %d '%s'. Akibatnya "
                        "tanggal seperti 03/10/2026 ambigu (3 Okt atau 10 Mar?). Pastikan di aplikasi asal file, lalu "
                        "ulangi dengan --format-tanggal bulan-hari (atau ubah ke hari/bulan/tahun). Tidak ada yang "
                        "diimpor." % bh[0], format_tanggal="bulan-hari")
    elif urutan == "bulan-hari" and hb:
        raise Gagal("--format-tanggal bulan-hari dipilih, tapi baris %d '%s' jelas hari/bulan. Periksa file. Tidak ada "
                    "yang diimpor." % hb[0], format_tanggal="campur")
    termin_arg = None
    if args.termin is not None:
        termin_arg = baca_termin(args.termin)
        if termin_arg is None or termin_arg > MAKS_TERMIN:
            raise Gagal("--termin harus jumlah hari 0-%d." % MAKS_TERMIN)

    def kerja(conn, cfg):
        hari = hari_ini()
        termin_def = termin_arg if termin_arg is not None else int(cfg.get("termin") or TERMIN_DEFAULT)
        masalah, lewati = [], {"sudah_ada": 0, "lunas": 0, "batal": 0}
        catatan_baris = []
        siap = []           # dict per nota
        per_kunci = {}
        for no, r in data:
            try:
                st = jenis_status(ambil(r, "status")) if "status" in peta else None
                if st == "batal":
                    lewati["batal"] += 1
                    continue
                if st == "lunas":
                    lewati["lunas"] += 1
                    continue
                if st == "tidak_dikenal":
                    raise Gagal("status '%s' tidak dikenal (lunas/belum lunas/batal?)" % ambil(r, "status"))
                nama = ambil(r, "pelanggan")
                if not nama or not re.search(r"[^\W\d_]", nama):
                    raise Gagal("nama pelanggan kosong/tidak valid")
                if nama[0] in "=+@":
                    raise Gagal("nama pelanggan '%s' berisi rumus Excel" % nama[:40])
                tgl, c = baca_tgl(ambil(r, "tanggal"), hari, "lalu", urutan=urutan, hari=hari)
                catatan_baris += ["baris %d: %s" % (no, x) for x in c]
                if tgl > hari:
                    raise Gagal("tanggal %s di masa depan" % tgl_pendek(tgl))
                if "nominal" in peta and ambil(r, "nominal"):
                    nominal, c = parse_rupiah(ambil(r, "nominal"))
                    catatan_baris += ["baris %d: %s" % (no, x) for x in c]
                elif "sisa" in peta:
                    nominal, c = parse_rupiah(ambil(r, "sisa"), "Sisa")
                    catatan_baris += ["baris %d: %s" % (no, x) for x in c]
                else:
                    raise Gagal("nominal kosong")
                dibayar = 0
                if "dibayar" in peta and ambil(r, "dibayar") and re.sub(r"[\s0.,rpRP-]", "", ambil(r, "dibayar")):
                    dibayar, c = parse_rupiah(ambil(r, "dibayar"), "Dibayar")
                    catatan_baris += ["baris %d: %s" % (no, x) for x in c]
                elif "sisa" in peta and "nominal" in peta and ambil(r, "sisa") != "":
                    s_txt = ambil(r, "sisa")
                    sisa_v = 0 if not re.sub(r"[\s0.,rpRP-]", "", s_txt) else parse_rupiah(s_txt, "Sisa")[0]
                    dibayar = nominal - sisa_v
                    if dibayar < 0:
                        raise Gagal("sisa lebih besar dari nominal")
                if dibayar > nominal:
                    raise Gagal("dibayar %s melebihi nominal %s" % (rp(dibayar), rp(nominal)))
                if dibayar == nominal:
                    lewati["lunas"] += 1
                    continue
                jt_txt = ambil(r, "jatuh_tempo")
                if jt_txt:
                    t_hari = baca_termin(jt_txt)
                    if t_hari is not None and not re.fullmatch(r"\d{1,3}", jt_txt):
                        jt = tgl + timedelta(days=t_hari)
                    else:
                        jt, c = baca_tgl(jt_txt, tgl, "depan", urutan=urutan, hari=hari)
                        catatan_baris += ["baris %d: %s" % (no, x) for x in c]
                    asal_jt = "kolom"
                elif "termin" in peta and baca_termin(ambil(r, "termin")) is not None:
                    jt, asal_jt = tgl + timedelta(days=baca_termin(ambil(r, "termin"))), "kolom termin"
                else:
                    jt, asal_jt = tgl + timedelta(days=termin_def), "termin"
                if jt < tgl:
                    raise Gagal("jatuh tempo %s sebelum tanggal nota %s" % (tgl_pendek(jt), tgl_pendek(tgl)))
                wa = None
                if "wa" in peta and ambil(r, "wa"):
                    try:
                        wa, _ = normalisasi_wa(ambil(r, "wa"))
                    except Gagal as e:
                        catatan_baris.append("baris %d: nomor WA diabaikan (%s)" % (no, e.pesan))
                no_nota = ambil(r, "nota")
                item = {"baris": no, "nama": bersih(nama, 80), "tanggal": tgl, "jt": jt, "asal_jt": asal_jt,
                        "nominal": nominal, "dibayar": dibayar, "wa": wa, "no_nota": bersih(no_nota, 40),
                        "keterangan": ambil(r, "keterangan")}
                k = kunci_nota(no_nota)
                if k and k in per_kunci:
                    lama = per_kunci[k]
                    if not args.gabung_baris:
                        raise Gagal("nomor nota %s sudah muncul di baris %d. Jika file ini per barang (satu nota "
                                    "beberapa baris), ulangi dengan --gabung-baris" % (no_nota, lama["baris"]))
                    if kunci_nama(lama["nama"]) != kunci_nama(item["nama"]) or lama["tanggal"] != tgl:
                        raise Gagal("nota %s di baris %d berbeda pelanggan/tanggal; tidak bisa digabung" %
                                    (no_nota, lama["baris"]))
                    lama["nominal"] += nominal
                    lama["dibayar"] += dibayar
                    lama.setdefault("gabungan", [lama["baris"]]).append(no)
                    continue
                if k:
                    per_kunci[k] = item
                siap.append(item)
            except Gagal as e:
                masalah.append({"baris": no, "alasan": e.pesan})
        # cocokkan dengan database & pelanggan
        semua_pel = conn.execute("SELECT * FROM pelanggan").fetchall()
        pel_baru, hasil, mungkin_sama = {}, [], []
        tanda_file = {}
        for it in siap:
            if it["dibayar"] >= it["nominal"]:
                lewati["lunas"] += 1
                continue
            k = kunci_nota(it["no_nota"])
            if k:
                ada = conn.execute("SELECT n.*, p.nama AS pnama FROM nota n JOIN pelanggan p ON p.id=n.pelanggan_id "
                                   "WHERE n.kunci=?", (k,)).fetchone()
                if ada:
                    if kunci_nama(ada["pnama"]) == kunci_nama(it["nama"]) and ada["nominal"] == it["nominal"]:
                        lewati["sudah_ada"] += 1
                    else:
                        masalah.append({"baris": it["baris"], "alasan": "nomor nota %s sudah dipakai di buku untuk %s "
                                        "(%s); isi file berbeda" % (it["no_nota"], ada["pnama"], rp(ada["nominal"]))})
                    continue
            cocok = [p for p in semua_pel if kunci_nama(p["nama"]) == kunci_nama(it["nama"])]
            if len(cocok) > 1:
                masalah.append({"baris": it["baris"], "alasan": "nama '%s' cocok dengan %d pelanggan (%s); pakai nama "
                                "yang lebih jelas" % (it["nama"], len(cocok), ", ".join(kode_p(p["id"])
                                                                                         for p in cocok))})
                continue
            if not k:
                tanda = (kunci_nama(it["nama"]), it["tanggal"].isoformat(), it["nominal"])
                if cocok and conn.execute("SELECT 1 FROM nota WHERE pelanggan_id=? AND tanggal=? AND nominal=? AND "
                                          "status='aktif'", (cocok[0]["id"], tanda[1], tanda[2])).fetchone():
                    lewati["sudah_ada"] += 1
                    continue
                if tanda in tanda_file:
                    masalah.append({"baris": it["baris"], "alasan": "sama persis dengan baris %d (pelanggan, tanggal, "
                                    "nominal) dan tanpa nomor nota; kemungkinan dobel. Tambahkan kolom no nota bila "
                                    "memang dua bon berbeda" % tanda_file[tanda]})
                    continue
                tanda_file[tanda] = it["baris"]
            if cocok:
                it["pid"] = cocok[0]["id"]
            else:
                kn = kunci_nama(it["nama"])
                if kn not in pel_baru:
                    pid, _ = buat_pelanggan(conn, it["nama"], it["wa"], izinkan_dup=True)
                    pel_baru[kn] = pid
                    mr = mirip(it["nama"], semua_pel)
                    if mr:
                        mungkin_sama.append("'%s' (baru, %s) mirip %s" % (it["nama"], kode_p(pid), ", ".join(
                            "%s %s" % (kode_p(p["id"]), p["nama"]) for p in mr[:3])))
                it["pid"] = pel_baru[kn]
            hasil.append(it)
        # tulis
        for it in hasil:
            no = it["no_nota"] or nomor_otomatis(conn, "IMP")
            cur = conn.execute(
                "INSERT INTO nota(pelanggan_id, no_nota, kunci, tanggal, jatuh_tempo, nominal, keterangan, sumber, "
                "dibuat, diubah) VALUES (?,?,?,?,?,?,?,?,?,?)",
                (it["pid"], no, kunci_nota(no), it["tanggal"].isoformat(), it["jt"].isoformat(), it["nominal"],
                 bersih(it["keterangan"], 200), "impor:" + Path(args.file).name[:60], stempel(), stempel()))
            it["no_final"] = no
            if it["dibayar"]:
                b = conn.execute("INSERT INTO pembayaran(pelanggan_id, tanggal, jumlah, metode, catatan, dibuat) VALUES "
                                 "(?,?,?,?,?,?)", (it["pid"], it["tanggal"].isoformat(), it["dibayar"], "sebelum impor",
                                                   "pembayaran tercatat di file impor", stempel()))
                conn.execute("INSERT INTO alokasi(pembayaran_id, nota_id, tanggal, jumlah, dibuat) VALUES (?,?,?,?,?)",
                             (b.lastrowid, cur.lastrowid, it["tanggal"].isoformat(), it["dibayar"], stempel()))
        total = sum(it["nominal"] for it in hasil)
        sisa = sum(it["nominal"] - it["dibayar"] for it in hasil)
        pakai_termin = sum(1 for it in hasil if it["asal_jt"] == "termin")
        t = ["IMPOR PIUTANG dari %s (format tanggal: %s)" % (Path(args.file).name,
                                                            "hari/bulan/tahun" if urutan == "hari-bulan" else
                                                            "bulan/hari/tahun (sesuai --format-tanggal)"),
             "Kolom dikenali: " + ", ".join("%s='%s'" % (k, header[i]) for k, i in peta.items()),
             "Kolom diabaikan: " + (", ".join(abaikan) or "-"),
             "Akan dicatat: %d nota, total %s, sisa piutang %s, untuk %d pelanggan (%d pelanggan baru)" %
             (len(hasil), rp(total), rp(sisa), len({it["pid"] for it in hasil}), len(pel_baru)),
             "Dilewati: %d sudah ada di buku, %d sudah lunas, %d batal/void" %
             (lewati["sudah_ada"], lewati["lunas"], lewati["batal"])]
        if pakai_termin:
            t.append("Jatuh tempo: %d nota tanpa kolom jatuh tempo diberi termin %d hari dari tanggal nota (asumsi; "
                     "ubah dengan --termin)." % (pakai_termin, termin_def))
        if hasil:
            t.append("Contoh (maks. 10):")
            t += ["- baris %s: %s | %s | %s | JT %s | %s%s" % (
                it["baris"] if "gabungan" not in it else ",".join(map(str, it["gabungan"])), it["nama"],
                it["no_nota"] or "(nomor otomatis)", tgl_pendek(it["tanggal"]), tgl_pendek(it["jt"]),
                rp(it["nominal"]), (" (dibayar %s)" % rp(it["dibayar"])) if it["dibayar"] else "") for it in hasil[:10]]
        if masalah:
            t.append("BARIS BERMASALAH, TIDAK DIIMPOR (%d):" % len(masalah))
            t += ["- baris %d: %s" % (m["baris"], m["alasan"]) for m in sorted(masalah, key=lambda m: m["baris"])[:30]]
            if len(masalah) > 30:
                t.append("... dan %d lainnya (lihat JSON 'masalah')." % (len(masalah) - 30))
        per = list(per_file)
        if mungkin_sama:
            per.append("Nama pelanggan baru yang mirip pelanggan lama (periksa, mungkin orang yang sama): " +
                       "; ".join(mungkin_sama[:10]))
        per += catatan_baris[:20]
        if len(catatan_baris) > 20:
            per.append("... dan %d catatan baris lainnya." % (len(catatan_baris) - 20))
        if masalah and len(masalah) * 2 > len(data):
            per.append("Lebih dari separuh baris bermasalah; periksa dulu file dan judul kolomnya sebelum --ya.")
        return {"jumlah_nota": len(hasil), "total": total, "sisa": sisa, "pelanggan_baru": len(pel_baru),
                "dilewati": lewati, "masalah": sorted(masalah, key=lambda m: m["baris"]), "kolom": {
                    k: header[i] for k, i in peta.items()}, "format_tanggal": urutan, "peringatan": per,
                "ringkasan": {"impor": len(hasil), "total": total}}, "\n".join(t)
    return jalankan_tulis(args, "impor", kerja, besar=True, label_backup="sebelum-impor")


def di_repo_git(p):
    for d in [p.parent] + list(p.parent.parents):
        if (d / ".git").exists():
            return d
    return None


def cmd_ekspor(args):
    db = path_db(args)
    conn = _baca(args)
    try:
        buku = Buku(conn)
        sam = args.samarkan
        if args.ke:
            tujuan = Path(args.ke).expanduser().resolve()
        else:
            fol = db.parent / "ekspor"
            fol.mkdir(parents=True, exist_ok=True)
            tujuan = nama_unik(fol, "piutang-%s-%s" % (args.format, kini().strftime("%Y%m%d-%H%M%S")), ".csv")
        per = []
        repo = di_repo_git(tujuan)
        if repo and not sam:
            per.append("Folder tujuan berada di dalam repositori git (%s). File berisi data pelanggan: jangan di-commit/"
                       "diunggah." % repo)
        if args.format == "tagih-piutang":
            rows = [[n["pelanggan"], n["no_nota"], n["nominal"] - n["dipotong"], n["jatuh_tempo"], n["dibayar"],
                     n["diingatkan"]] for n in buku.terbuka]
            p = tulis_csv(tujuan, ["pelanggan", "no_invoice", "nominal", "jatuh_tempo", "dibayar", "sudah_diingatkan"],
                          rows, args.timpa, pemisah=",")
            teks = ("Ekspor %d nota terbuka ke %s\nFormat skill tagih-piutang: python3 <folder-tagih-piutang>/scripts/"
                    "hitung_telat.py --file \"%s\" (rekap umur + urutan prioritas penagihan). Kolom nominal = nominal "
                    "nota dikurangi potongan." % (len(rows), p, p))
            if any(v > 0 for v in buku.kredit.values()):
                per.append("Ada pelanggan dengan kelebihan bayar/deposit yang belum dipakai; jalankan pakai-kredit dulu "
                           "agar tagihan tidak terlalu besar.")
        elif args.format == "pembayaran":
            rows = []
            for b in conn.execute("SELECT b.*, p.nama FROM pembayaran b JOIN pelanggan p ON p.id=b.pelanggan_id "
                                  "ORDER BY b.tanggal, b.id"):
                al = conn.execute("SELECT a.jumlah, n.no_nota FROM alokasi a JOIN nota n ON n.id=a.nota_id WHERE "
                                  "a.pembayaran_id=?", (b["id"],)).fetchall()
                rows.append([kode_b(b["id"]), b["tanggal"], kode_p(b["pelanggan_id"]),
                             samar_nama(b["nama"]) if sam else b["nama"], b["jumlah"], b["metode"], b["status"],
                             "; ".join("%s=%d" % (a["no_nota"], a["jumlah"]) for a in al)])
            p = tulis_csv(tujuan, ["kode", "tanggal", "kode_pelanggan", "pelanggan", "jumlah", "metode", "status",
                                   "alokasi"], rows, args.timpa)
            teks = "Ekspor %d pembayaran ke %s (pemisah ';', UTF-8, aman dibuka di Excel)." % (len(rows), p)
        else:
            daftar = buku.nota if args.status == "semua" else buku.terbuka
            rows = [[kode_p(n["pelanggan_id"]), samar_nama(n["pelanggan"]) if sam else n["pelanggan"],
                     samar_wa(buku.pel[n["pelanggan_id"]]["wa"]) if sam else tampil_wa(buku.pel[n["pelanggan_id"]]["wa"]),
                     n["no_nota"], n["tanggal"], n["jatuh_tempo"], n["nominal"], n["dibayar"], n["dipotong"], n["sisa"],
                     max(0, n["telat"]), LABEL_UMUR[n["umur"]] if n["sisa"] else "lunas", n["diingatkan"],
                     "" if sam else n["keterangan"]] for n in daftar]
            p = tulis_csv(tujuan, ["kode_pelanggan", "pelanggan", "no_wa", "no_nota", "tanggal", "jatuh_tempo",
                                   "nominal", "dibayar", "potongan", "sisa", "hari_lewat", "umur", "diingatkan",
                                   "keterangan"], rows, args.timpa)
            teks = "Ekspor %d nota ke %s (pemisah ';', UTF-8, aman dibuka di Excel)." % (len(rows), p)
        if not sam:
            teks += "\n" + DISCLAIMER_PRIVASI
        if per:
            teks += "\n" + "\n".join("Catatan: " + x for x in per)
        return {"ok": True, "mode": "tersimpan", "file": p, "jumlah": len(rows), "format": args.format,
                "data_sensitif": not sam, "peringatan": per, "teks": teks}, teks
    finally:
        conn.close()


# --------------------------------------------------------------------------- backup & restore
def cmd_backup(args):
    db = path_db(args)
    fol = folder_backup(db)
    if args.daftar:
        bks = sorted(fol.glob("piutang-*.db")) if fol.is_dir() else []
        if bks:
            t = ("Cadangan di %s (terbaru paling bawah):\n%s\nPulihkan: piutang.py restore --dari \"%s\" (pratinjau, "
                 "lalu --ya)." % (fol, "\n".join("- " + str(b) for b in bks[-30:]), bks[-1]))
        else:
            t = ("Belum ada cadangan di %s. Jika database rusak dan tidak ada cadangan: piutang.py init --mulai-baru "
                 "(pratinjau, lalu --ya); file rusak dipindah ke %s, tidak dihapus. Data bisa diimpor ulang dari "
                 "ekspor CSV terakhir bila ada." % (fol, fol))
        return {"ok": True, "mode": "baca", "folder": str(fol), "backup": [str(b) for b in bks], "teks": t}, t
    conn = buka(db, baca_saja=True)
    conn.close()
    b = buat_backup(db, re.sub(r"[^\w-]", "", args.label or "manual") or "manual")
    t = "Cadangan dibuat: %s" % b
    return {"ok": True, "mode": "tersimpan", "backup": b, "teks": t}, t


def cmd_restore(args):
    """Pulihkan TANPA menulis ke database aktif lewat SQLite (bisa saja rusak total): periksa cadangan -> salin/
    pindahkan database aktif (+journal) ke backup-piutang -> tulis cadangan ke file sementara -> periksa ->
    os.replace (atomik)."""
    db = path_db(args)
    src = Path(args.dari).expanduser().resolve()
    if not src.is_file():
        raise Gagal("File cadangan %s tidak ada. Lihat daftar: piutang.py backup --daftar" % src)
    if src == db:
        raise Gagal("File cadangan sama dengan database aktif. Pilih file dari piutang.py backup --daftar.")
    try:
        c = buka(src, baca_saja=True)
    except Gagal as e:
        raise Gagal("File cadangan %s tidak bisa dipakai (%s). Pilih cadangan lain dari piutang.py backup --daftar." %
                    (src.name, e.pesan.split(". ")[0]))
    try:
        n = c.execute("SELECT COUNT(*) FROM nota").fetchone()[0]
        cek = c.execute("PRAGMA quick_check").fetchone()[0]
        tabel = {r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    finally:
        c.close()
    if cek != "ok" or not set(TABEL_WAJIB) <= tabel:
        raise Gagal("File cadangan %s juga bermasalah (%s). Pilih cadangan lain dari piutang.py backup --daftar." %
                    (src.name, cek if cek != "ok" else "tabel tidak lengkap"))
    try:
        st = status_db(db)
    except Gagal as e:
        if "sedang dipakai" in e.pesan:
            raise
        raise Gagal("File %s bukan database buku-piutang; restore dibatalkan agar file itu tidak tertimpa. Periksa --db."
                    % db)
    nasib = {"tidak_ada": "Database belum ada; cadangan akan dipasang di lokasi itu.",
             "sehat": "Database saat ini disalin dulu apa adanya ke folder backup-piutang.",
             "rusak": "Database saat ini RUSAK; file itu dipindah (tidak dihapus) ke folder backup-piutang dengan nama "
                      "rusak-piutang-<waktu>.db."}[st]
    if not args.ya:
        t = ("PRATINJAU (belum disimpan):\nDatabase %s akan diganti dengan cadangan %s (%d nota). %s\n\nLanjut? "
             "Jalankan perintah yang sama + --ya setelah pengguna setuju." % (db, src, n, nasib))
        return {"ok": True, "mode": "pratinjau", "perlu_konfirmasi": True, "status_db": st, "teks": t}, t
    db.parent.mkdir(parents=True, exist_ok=True)
    tmp = nama_unik(db.parent, ".piutang-restore-%d" % os.getpid(), ".tmp")
    simpanan = None
    try:
        s_ = sqlite3.connect(str(src))
        d_ = sqlite3.connect(str(tmp))
        try:
            s_.backup(d_)
        finally:
            d_.close()
            s_.close()
        c = sqlite3.connect(str(tmp))
        try:
            ok = c.execute("SELECT nilai FROM meta WHERE kunci='aplikasi'").fetchone()
            cek2 = c.execute("PRAGMA quick_check").fetchone()[0]
        finally:
            c.close()
        if not ok or ok[0] != APLIKASI or cek2 != "ok":
            raise Gagal("Salinan cadangan %s tidak valid; database aktif tidak diubah." % src.name)
        if st == "sehat":
            pastikan_tidak_dipakai(db)
            simpanan = singkirkan(db, "piutang-{}-sebelum-restore", pindah=False)
        elif st == "rusak":
            simpanan = singkirkan(db, "rusak-piutang-{}", pindah=True)
        os.replace(str(tmp), str(db))
    finally:
        if tmp.exists():
            try:
                tmp.unlink()
            except OSError:
                pass
    t = "TERSIMPAN. Database %s dipulihkan dari %s (%d nota)." % (db, src, n)
    if simpanan:
        t += ("\nFile rusak dipindah (tidak dihapus) ke: %s" if st == "rusak" else
              "\nSalinan database sebelumnya: %s") % simpanan
    return {"ok": True, "mode": "tersimpan", "backup": str(simpanan) if simpanan else None, "status_db_lama": st,
            "teks": t}, t


# --------------------------------------------------------------------------- CLI
class ParserID(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        print("GAGAL: perintah tidak lengkap/salah: %s. Lihat --help." % message, file=sys.stderr)
        sys.exit(2)


def buat_parser():
    umum = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
    umum.add_argument("--db", help="File database (default ~/KomunitechData/piutang/piutang.db)")
    umum.add_argument("--json", action="store_true", help="Output JSON (untuk agent/laporan)")
    umum.add_argument("--hari-ini", help=argparse.SUPPRESS)
    tulis = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
    tulis.add_argument("--ya", action="store_true", help="Simpan perubahan besar (tanpa ini hanya pratinjau)")
    sam = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
    sam.add_argument("--samarkan", action="store_true", help="Nama jadi inisial, nomor WA disamarkan")

    p = ParserID(prog="piutang.py", description="Buku piutang pelanggan lokal (buku-piutang %s)" % VERSI, allow_abbrev=False)
    p.add_argument("--versi", action="version", version="buku-piutang " + VERSI)
    sub = p.add_subparsers(dest="perintah", parser_class=ParserID)
    sub.required = True

    s = sub.add_parser("init", parents=[umum, tulis], help="Buat buku piutang baru (besar: --ya)", allow_abbrev=False)
    s.add_argument("--nama-usaha")
    s.add_argument("--pengirim", help="Nama yang dipakai di draf pesan")
    s.add_argument("--rekening", help="Rekening pembayaran untuk draf, mis. 'BCA 1234567890 a.n. Sari'")
    s.add_argument("--termin", help="Termin default (hari), default 30")
    s.add_argument("--zona", help="WIB (default), WITA, WIT")
    s.add_argument("--mulai-baru", action="store_true", help="Database rusak & tanpa cadangan: buat baru")
    s.set_defaults(fungsi=cmd_init)
    s = sub.add_parser("info", parents=[umum], help="Lokasi database, jumlah data, cadangan", allow_abbrev=False)
    s.set_defaults(fungsi=cmd_info)
    s = sub.add_parser("atur", parents=[umum, tulis], help="Ubah pengaturan", allow_abbrev=False)
    for o in ("--nama-usaha", "--pengirim", "--rekening", "--termin", "--zona"):
        s.add_argument(o)
    s.set_defaults(fungsi=cmd_atur)

    s = sub.add_parser("tambah-pelanggan", parents=[umum, tulis], help="Tambah pelanggan", allow_abbrev=False)
    s.add_argument("--nama", required=True)
    s.add_argument("--wa")
    s.add_argument("--sapaan", help="Bu/Pak/Kak/- (default: dari nama, atau 'Bapak/Ibu')")
    s.add_argument("--catatan")
    s.add_argument("--izinkan-duplikat", action="store_true")
    s.set_defaults(fungsi=cmd_tambah_pelanggan)
    s = sub.add_parser("ubah-pelanggan", parents=[umum, tulis], help="Ubah data pelanggan", allow_abbrev=False)
    s.add_argument("--pelanggan", required=True)
    for o in ("--nama", "--wa", "--sapaan", "--catatan"):
        s.add_argument(o)
    s.add_argument("--izinkan-duplikat", action="store_true")
    s.set_defaults(fungsi=cmd_ubah_pelanggan)
    s = sub.add_parser("hapus-pelanggan", parents=[umum, tulis], help="Hapus data pelanggan yang sudah lunas (besar)", allow_abbrev=False)
    s.add_argument("--pelanggan", required=True)
    s.set_defaults(fungsi=cmd_hapus_pelanggan)

    s = sub.add_parser("catat", parents=[umum, tulis], help="Catat piutang (nota belum dibayar)", allow_abbrev=False)
    s.add_argument("--pelanggan", required=True, help="Nama, kode (P0001), atau nomor WA")
    s.add_argument("--nota", help="Nomor nota/invoice (kosong = nomor otomatis PB-0001)")
    s.add_argument("--tanggal", help="Tanggal nota, hari/bulan/tahun (default hari ini)")
    s.add_argument("--jatuh-tempo", help="Tanggal jatuh tempo, atau '30 hari'")
    s.add_argument("--termin", help="Jumlah hari dari tanggal nota (default pengaturan, 30)")
    s.add_argument("--nominal", help="Total tagihan, mis. 2,5jt / 2.500.000")
    s.add_argument("--dpp", help="DPP (belum termasuk PPN); pakai bersama --ppn")
    s.add_argument("--ppn", help="11 (12%% x DPP nilai lain 11/12) atau 12 (barang mewah)")
    s.add_argument("--keterangan")
    s.add_argument("--wa", help="Nomor WA (untuk pelanggan baru)")
    s.add_argument("--sapaan")
    s.add_argument("--pelanggan-baru", action="store_true", help="Buat pelanggan baru walau ada nama mirip")
    s.set_defaults(fungsi=cmd_catat)
    s = sub.add_parser("ubah-nota", parents=[umum, tulis], help="Koreksi nota", allow_abbrev=False)
    s.add_argument("--nota", required=True)
    for o in ("--tanggal", "--jatuh-tempo", "--termin", "--nominal", "--keterangan", "--no-baru", "--pelanggan"):
        s.add_argument(o)
    s.set_defaults(fungsi=cmd_ubah_nota)

    s = sub.add_parser("bayar", parents=[umum, tulis], help="Catat pembayaran (sebagian/lunas)", allow_abbrev=False)
    s.add_argument("--pelanggan")
    s.add_argument("--nota", help="Nomor nota (kosong = nota jatuh tempo paling awal dulu)")
    s.add_argument("--jumlah", required=True, help="Nominal, atau 'lunas'")
    s.add_argument("--tanggal", help="Tanggal bayar (default hari ini)")
    s.add_argument("--metode", help="transfer/tunai/QRIS/...")
    s.add_argument("--catatan")
    s.add_argument("--kelebihan", choices=["kredit", "kembalikan", "nota-lain"],
                   help="Jika bayar melebihi tagihan: simpan sebagai deposit, sudah dikembalikan, atau ke nota lain")
    s.add_argument("--izinkan-dobel", action="store_true", help="Izinkan pembayaran dengan tanggal & jumlah sama")
    s.set_defaults(fungsi=cmd_bayar)
    s = sub.add_parser("pakai-kredit", parents=[umum, tulis], help="Pakai deposit/kelebihan bayar untuk nota terbuka", allow_abbrev=False)
    s.add_argument("--pelanggan", required=True)
    s.add_argument("--nota")
    s.add_argument("--tanggal")
    s.set_defaults(fungsi=cmd_pakai_kredit)
    s = sub.add_parser("kembalikan", parents=[umum, tulis], help="Catat deposit/kelebihan bayar yang dikembalikan", allow_abbrev=False)
    s.add_argument("--pelanggan", required=True)
    s.add_argument("--jumlah", required=True, help="Nominal, atau 'semua'")
    s.add_argument("--tanggal")
    s.add_argument("--catatan")
    s.set_defaults(fungsi=cmd_kembalikan)
    s = sub.add_parser("potong", parents=[umum, tulis], help="Kurangi tagihan: retur/diskon/hapus (besar)", allow_abbrev=False)
    s.add_argument("--nota", required=True)
    s.add_argument("--jumlah", required=True, help="Nominal, atau 'sisa'")
    s.add_argument("--alasan", required=True)
    s.add_argument("--tanggal")
    s.set_defaults(fungsi=cmd_potong)
    s = sub.add_parser("batal-nota", parents=[umum, tulis], help="Batalkan nota salah catat/dobel (besar)", allow_abbrev=False)
    s.add_argument("--nota", required=True)
    s.add_argument("--alasan", required=True)
    s.set_defaults(fungsi=cmd_batal_nota)
    s = sub.add_parser("batal-bayar", parents=[umum, tulis], help="Batalkan pembayaran salah catat (besar)", allow_abbrev=False)
    s.add_argument("--bayar", required=True, help="Kode pembayaran, mis. B0003")
    s.add_argument("--alasan", required=True)
    s.set_defaults(fungsi=cmd_batal_bayar)

    s = sub.add_parser("saldo", parents=[umum, sam], help="Saldo per pelanggan / detail satu pelanggan", allow_abbrev=False)
    s.add_argument("--pelanggan")
    s.add_argument("--per", help="Posisi per tanggal (default hari ini)")
    s.add_argument("--semua", action="store_true")
    s.set_defaults(fungsi=cmd_saldo)
    s = sub.add_parser("umur", parents=[umum, sam], help="Umur piutang (aging)", allow_abbrev=False)
    s.add_argument("--per")
    s.add_argument("--semua", action="store_true")
    s.set_defaults(fungsi=cmd_umur)
    s = sub.add_parser("jatuh-tempo", parents=[umum, sam], help="Terlewat, hari ini, 7 hari ke depan", allow_abbrev=False)
    s.add_argument("--semua", action="store_true")
    s.set_defaults(fungsi=cmd_jatuh_tempo)
    s = sub.add_parser("ringkasan", parents=[umum, sam], help="Ringkasan harian (untuk Telegram pemilik)", allow_abbrev=False)
    s.add_argument("--semua", action="store_true")
    s.set_defaults(fungsi=cmd_ringkasan)
    s = sub.add_parser("rekap", parents=[umum, sam], help="Rekap periode + JSON untuk laporan", allow_abbrev=False)
    s.add_argument("--periode", help="hari-ini, kemarin, minggu-ini, minggu-lalu, bulan-ini (default), bulan-lalu, "
                                     "tahun-ini, semua")
    s.add_argument("--dari")
    s.add_argument("--sampai")
    s.add_argument("--rumus", action="store_true")
    s.set_defaults(fungsi=cmd_rekap)
    s = sub.add_parser("draf", parents=[umum], help="Draf pesan tagihan sopan (+ tautan wa.me)", allow_abbrev=False)
    s.add_argument("--pelanggan")
    s.add_argument("--nota")
    s.add_argument("--pesan", help="Pakai teks ini (draf yang sudah diperhalus) untuk tautan wa.me")
    s.set_defaults(fungsi=cmd_draf)
    s = sub.add_parser("terkirim", parents=[umum, tulis], help="Catat bahwa pengingat sudah dikirim pemilik", allow_abbrev=False)
    s.add_argument("--pelanggan")
    s.add_argument("--nota")
    s.set_defaults(fungsi=cmd_terkirim)

    s = sub.add_parser("impor", parents=[umum, tulis], help="Impor piutang dari CSV nota/kasir (besar: --ya)", allow_abbrev=False)
    s.add_argument("file")
    s.add_argument("--format-tanggal", choices=["hari-bulan", "bulan-hari"])
    s.add_argument("--termin", help="Termin (hari) untuk baris tanpa jatuh tempo")
    s.add_argument("--gabung-baris", action="store_true", help="File per barang: jumlahkan baris dengan nomor nota sama")
    s.set_defaults(fungsi=cmd_impor)
    s = sub.add_parser("ekspor", parents=[umum, sam], help="Ekspor ke CSV", allow_abbrev=False)
    s.add_argument("--format", choices=["lengkap", "tagih-piutang", "pembayaran"], default="lengkap")
    s.add_argument("--status", choices=["terbuka", "semua"], default="terbuka")
    s.add_argument("--ke", "--csv", dest="ke", help="File tujuan (default: <folder database>/ekspor/...)")
    s.add_argument("--timpa", action="store_true")
    s.set_defaults(fungsi=cmd_ekspor)

    s = sub.add_parser("backup", parents=[umum], help="Buat cadangan / --daftar", allow_abbrev=False)
    s.add_argument("--daftar", action="store_true")
    s.add_argument("--label")
    s.set_defaults(fungsi=cmd_backup)
    s = sub.add_parser("restore", parents=[umum, tulis], help="Pulihkan dari cadangan (besar: --ya)", allow_abbrev=False)
    s.add_argument("--dari", required=True)
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
    args = buat_parser().parse_args(argv)
    for k, v in (("ya", False), ("samarkan", False)):
        if not hasattr(args, k):
            setattr(args, k, v)
    _JAM["kini"] = None
    _JAM["zona"] = "WIB"
    try:
        if args.hari_ini:
            _JAM["kini"] = parse_hari_ini(args.hari_ini)
        data, teks = args.fungsi(args)
    except Gagal as e:
        out = {"ok": False, "error": e.pesan}
        out.update(e.detail)
        return cetak(args, out, e.pesan, 1)
    except sqlite3.OperationalError as e:
        pesan = (PESAN_TERKUNCI % _detik()) if _terkunci(e) else \
            "Kesalahan database: %s. Jangan hapus file database; ulangi, atau pulihkan dari cadangan." % e
        return cetak(args, {"ok": False, "error": pesan}, pesan, 1)
    except sqlite3.IntegrityError as e:
        pesan = ("Data bentrok dengan catatan yang sudah ada (%s). Tidak ada yang disimpan; database aman. Periksa "
                 "nomor nota/pembayaran lalu ulangi." % e)
        return cetak(args, {"ok": False, "error": pesan, "bentrok": True}, pesan, 1)
    except sqlite3.DatabaseError as e:
        pesan = "Database rusak (%s). Jangan hapus file itu. %s" % (e, SARAN_PULIH)
        return cetak(args, {"ok": False, "error": pesan, "rusak": True}, pesan, 1)
    except OSError as e:
        pesan = "File tidak bisa ditulis/dibaca (%s). Periksa folder dan izin aksesnya." % e
        return cetak(args, {"ok": False, "error": pesan}, pesan, 1)
    return cetak(args, data, teks, 0)


if __name__ == "__main__":
    sys.exit(main())
