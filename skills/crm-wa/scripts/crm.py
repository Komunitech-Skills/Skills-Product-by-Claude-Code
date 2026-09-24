#!/usr/bin/env python3
"""crm-wa (Komunitech) - CRM lokal untuk alur "chat WA -> ditawar -> deal".

Satu file database SQLite di komputer pemilik usaha. Hanya library standar Python 3.8+,
lintas OS (Windows: `python`/`py`), TANPA akses jaringan: script tidak pernah mengirim apa pun.
Pesan ke pelanggan hanya disiapkan sebagai DRAF + tautan wa.me; manusia yang menekan Kirim.

Lokasi database (urutan prioritas):
  1. --db PATH (ditulis setelah nama perintah)
  2. ENV KOMUNITECH_CRM_DB   (path file lengkap)
  3. ENV KOMUNITECH_DATA     (folder) + /crm/crm.db
  4. ~/KomunitechData/crm/crm.db
Cadangan: folder backup-crm/ di sebelah database (otomatis sekali sehari saat ada perubahan,
dan sebelum impor/hapus/gabung/restore).

Perubahan kecil (tambah, catat, tunda, terkirim, ubah, atur) langsung tersimpan.
Perubahan besar (init, impor, hapus, gabung, restore) hanya PRATINJAU sampai diberi --ya.

Contoh:
  python3 crm.py init --nama-usaha "Dapur Bu Sari" --pengirim Sari --ya
  python3 crm.py tambah --nama "Bu Rina" --wa "0812-0000-1001" --sumber ig --kebutuhan "kue ulang tahun" --nilai 450rb
  python3 crm.py catat --kontak "Bu Rina" --isi "minta diskon" --tahap ditawar --followup jumat
  python3 crm.py hari-ini                  # daftar follow-up + draf pesan + tautan wa.me
  python3 crm.py terkirim --kontak K0001   # pemilik sudah mengirim pesannya
  python3 crm.py rekap --periode bulan-ini --json

Kode keluar: 0 = berhasil; 1 = gagal (pesan jelas di "error"/stderr); 2 = perintah salah tulis.
"""
import argparse
import csv
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

APLIKASI = "crm-wa"
VERSI = "1.0.0"
SKEMA = 1
SKEMA_JSON_REKAP = 1

TAHAP = ["baru", "dihubungi", "ditawar", "deal", "selesai", "batal"]
TAHAP_TERBUKA = ("baru", "dihubungi", "ditawar")          # pipeline terbuka (belum diputuskan)
TAHAP_PANTAU = ("baru", "dihubungi", "ditawar", "deal")   # masih perlu follow-up
TAHAP_MENANG = ("deal", "selesai")
ALIAS_TAHAP = {
    "baru": "baru", "lead": "baru", "lead baru": "baru", "new": "baru", "masuk": "baru",
    "dihubungi": "dihubungi", "sudah dihubungi": "dihubungi", "dichat": "dihubungi", "sudah dichat": "dihubungi",
    "kontak": "dihubungi", "contacted": "dihubungi", "follow up": "dihubungi", "followup": "dihubungi",
    "ditawar": "ditawar", "tawar": "ditawar", "nego": "ditawar", "negosiasi": "ditawar", "penawaran": "ditawar",
    "ditawarkan": "ditawar", "sudah ditawari": "ditawar", "quotation": "ditawar", "proposal": "ditawar",
    "deal": "deal", "jadi": "deal", "closing": "deal", "sepakat": "deal", "order": "deal", "won": "deal",
    "selesai": "selesai", "lunas": "selesai", "beres": "selesai", "done": "selesai", "tuntas": "selesai",
    "batal": "batal", "gagal": "batal", "tidak jadi": "batal", "nggak jadi": "batal", "gak jadi": "batal",
    "lost": "batal", "cancel": "batal", "hilang": "batal",
}
LABEL_TAHAP = {"baru": "Baru", "dihubungi": "Dihubungi", "ditawar": "Ditawar", "deal": "Deal",
               "selesai": "Selesai", "batal": "Batal"}
ALIAS_SUMBER = [
    (("ig", "insta", "instagram", "dm ig", "dm instagram"), "Instagram"),
    (("tiktok shop", "tts", "tiktokshop"), "TikTok Shop"),
    (("tiktok", "tik tok", "tt"), "TikTok"),
    (("fb", "facebook", "marketplace fb", "fb marketplace", "facebook marketplace"), "Facebook"),
    (("shopee",), "Shopee"),
    (("tokopedia", "tokped"), "Tokopedia"),
    (("lazada",), "Lazada"),
    (("marketplace", "mp", "e-commerce", "ecommerce"), "Marketplace lain"),
    (("wa", "whatsapp", "chat wa", "wa langsung", "whatsapp langsung"), "WhatsApp langsung"),
    (("referensi", "rekomendasi", "ref", "referral", "teman", "kenalan", "dari teman", "rekomendasi teman",
      "getok tular", "mulut ke mulut"), "Referensi"),
    (("walk-in", "walk in", "walkin", "datang langsung", "datang ke toko", "offline", "toko"), "Walk-in"),
    (("web", "website", "situs", "google", "google maps", "gmaps", "seo"), "Website/Google"),
    (("iklan", "ads", "meta ads", "fb ads", "ig ads", "google ads", "iklan berbayar"), "Iklan"),
    (("pameran", "bazar", "event", "expo"), "Pameran/Event"),
    (("pelanggan lama", "repeat", "repeat order", "langganan"), "Pelanggan lama"),
]
ALIAS_ALASAN = [
    (("mahal", "kemahalan", "harga", "harga mahal", "kemahalan harganya", "budget kurang", "over budget"),
     "harga terlalu mahal"),
    (("tidak ada respon", "tidak respon", "no respon", "no response", "ghosting", "ghosting", "tidak balas",
      "nggak balas", "gak balas", "tidak dibalas", "slow respon"), "tidak ada respon"),
    (("pilih toko lain", "beli di tempat lain", "kompetitor", "pilih penjual lain", "pilih vendor lain",
      "ke toko lain", "sudah beli di tempat lain"), "pilih penjual lain"),
    (("belum butuh", "nanti dulu", "belum perlu", "tidak butuh", "tidak jadi butuh"), "belum butuh"),
    (("belum ada dana", "tidak ada dana", "dana belum ada", "belum gajian", "tidak ada budget", "belum ada budget"),
     "belum ada dana"),
    (("stok habis", "tidak tersedia", "barang habis", "tidak bisa dipenuhi", "jadwal penuh"),
     "stok/layanan tidak tersedia"),
    (("iseng", "cuma tanya", "cuma nanya", "tanya saja", "cuma tanya harga"), "hanya bertanya"),
]
SAPAAN_DIKENAL = {"bu", "ibu", "pak", "bapak", "kak", "ka", "kakak", "mas", "mbak", "mba", "bang", "abang", "om",
                  "tante", "dik", "adik", "cik", "ci", "ko", "koh", "sdr", "sdri", "saudara", "saudari", "dr", "drg",
                  "hj", "haji", "teh", "aa", "uda", "uni", "cak", "bli", "mbok", "opung", "bunda", "ayah", "mama",
                  "papa", "ustadz", "ustazah", "prof", "ir", "kang", "neng", "nona", "tuan", "nyonya", "ny", "tn"}
AWALAN_LEMBAGA = {"pt", "cv", "ud", "toko", "koperasi", "kop", "yayasan", "rs", "klinik", "sekolah", "hotel",
                  "resto", "restoran", "warung", "kafe", "cafe", "kantor", "dinas", "pemkab", "pemkot", "universitas",
                  "smk", "sma", "smp", "sd", "tk", "paud", "bengkel", "apotek", "salon", "katering", "catering"}
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
NAMA_HARI = {"senin": 0, "selasa": 1, "rabu": 2, "kamis": 3, "jumat": 4, "jum'at": 4, "jumaat": 4, "sabtu": 5,
             "minggu": 6, "ahad": 6}
JEDA_SETELAH_KIRIM = {1: 3, 2: 4}      # follow-up ke-1 terkirim -> +3 hari, ke-2 -> +4 hari; ke-3 (pamit) -> stop
MAKS_FU = 3
BATAS_LEWAT = 60                        # hari; lihat baca_tanggal()
SIMPAN_BACKUP_HARIAN = 30
DISCLAIMER_PRIVASI = ("Data pelanggan (nomor HP) adalah data pribadi (UU 27/2022 PDP): simpan di komputer ini, "
                      "jangan dibagikan ke grup, hapus bila pelanggan meminta.")


class Gagal(Exception):
    """Error yang pesannya aman ditampilkan ke pengguna."""

    def __init__(self, pesan, **detail):
        super().__init__(pesan)
        self.pesan = pesan
        self.detail = detail


def _timeout():
    try:
        return max(0.1, float(os.environ.get("KOMUNITECH_CRM_TIMEOUT", "15")))
    except ValueError:
        return 15.0


PESAN_TERKUNCI = ("Database CRM sedang dipakai program lain (mis. jadwal OpenClaw atau jendela lain) dan tidak "
                  "selesai dalam %d detik. Data aman, tidak rusak. Tunggu sebentar lalu ulangi perintah yang sama. "
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
    """Jam lokal (naive) di zona Indonesia. Indonesia tidak memakai jam musim panas, jadi offset tetap persis."""
    u = utc_now or datetime.now(timezone.utc)
    return u.astimezone(timezone(timedelta(hours=ZONA[zona][1]))).replace(tzinfo=None, microsecond=0)


def kini():
    return _JAM["kini"] or waktu_lokal(_JAM["zona"])


def hari_ini():
    return kini().date()


def stempel():
    return kini().isoformat(" ", "seconds")


def tgl_panjang(d):
    return "%s, %d %s %d" % (HARI[d.weekday()], d.day, BULAN[d.month - 1], d.year)


def tgl_pendek(d, tahun=True):
    if isinstance(d, str):
        d = date.fromisoformat(d[:10])
    return ("%d %s %d" % (d.day, BLN[d.month - 1], d.year)) if tahun else ("%d %s" % (d.day, BLN[d.month - 1]))


def _tanggal(y, m, d, asli):
    try:
        return date(y, m, d)
    except ValueError:
        raise Gagal("Tanggal '%s' tidak ada di kalender." % asli)


def _tambah_bulan(d, n):
    m = d.month - 1 + n
    y, m = d.year + m // 12, m % 12 + 1
    hari = min(d.day, [31, 29 if (y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)) else 28, 31, 30, 31, 30, 31, 31,
                       30, 31, 30, 31][m - 1])
    return date(y, m, hari)


def _cek_arah(d, acuan, arah, asli):
    catatan = []
    if arah == "depan" and d < acuan:
        catatan.append("%s sudah lewat %d hari, jadi kontak ini langsung masuk daftar TERLAMBAT." %
                       (tgl_pendek(d), (acuan - d).days))
    if arah == "lalu" and d > acuan:
        raise Gagal("Tanggal '%s' (%s) ada di masa depan; tanggal kejadian harus hari ini atau sebelumnya." %
                    (asli, tgl_pendek(d)))
    if arah == "depan" and (d - acuan).days > 366:
        catatan.append("%s lebih dari setahun lagi; pastikan tanggalnya benar." % tgl_pendek(d))
    return d, catatan


def _tanpa_tahun(hari, bulan, acuan, arah, asli):
    c = _tanggal(acuan.year, bulan, hari, asli) if not (bulan == 2 and hari == 29) else None
    if c is None:  # 29 Feb tanpa tahun: cari tahun kabisat terdekat sesuai arah
        for k in ((0, 1, 2, 3, 4) if arah != "lalu" else (0, -1, -2, -3, -4)):
            try:
                c = date(acuan.year + k, 2, 29)
                break
            except ValueError:
                continue
    if arah == "depan":
        if c >= acuan:
            return c, []
        lewat = (acuan - c).days
        if lewat <= BATAS_LEWAT:
            raise Gagal("Tanggal '%s' (%s) sudah lewat %d hari. Kalau memang tanggal itu, tulis lengkap dengan "
                        "tahunnya (mis. %d/%d/%d); kalau maksudnya tahun depan, tulis tahunnya juga." %
                        (asli, tgl_pendek(c), lewat, c.day, c.month, c.year))
        c2 = _tanggal(acuan.year + 1, bulan, hari, asli)
        return c2, ["Tahun tidak disebut; dipakai %s (tanggal itu tahun ini sudah lewat)." % tgl_pendek(c2)]
    if arah == "lalu":
        if c <= acuan:
            return c, []
        if (c - acuan).days <= BATAS_LEWAT:
            raise Gagal("Tanggal '%s' (%s) ada di masa depan; tanggal kejadian harus hari ini atau sebelumnya." %
                        (asli, tgl_pendek(c)))
        c2 = _tanggal(acuan.year - 1, bulan, hari, asli)
        return c2, ["Tahun tidak disebut; dipakai %s (tahun lalu)." % tgl_pendek(c2)]
    kand = [x for x in (c, _tanggal(acuan.year - 1, bulan, hari, asli), _tanggal(acuan.year + 1, bulan, hari, asli))]
    return min(kand, key=lambda x: abs((x - acuan).days)), []


def baca_tanggal(teks, acuan, arah="depan"):
    """Kembalikan (date, [catatan]). arah: 'depan' (jadwal follow-up), 'lalu' (tanggal kejadian), 'bebas'.

    Urutan selalu hari/bulan (format Indonesia). Contoh: 2026-10-03, 3/10/2026, 3/10, 3 Okt, "tgl 3", besok, lusa,
    "3 hari lagi", +3, "2 minggu lagi", "minggu depan", "bulan depan", Jumat, "Senin depan", kemarin.
    """
    if teks is None or not str(teks).strip():
        raise Gagal("Tanggal kosong.")
    asli = str(teks).strip()
    s = re.sub(r"\s+", " ", asli.lower().replace(",", " ")).strip()
    rel = {"hari ini": 0, "hr ini": 0, "sekarang": 0, "today": 0, "besok": 1, "bsk": 1, "besuk": 1,
           "tomorrow": 1, "lusa": 2, "kemarin": -1, "kmrn": -1, "kemaren": -1, "yesterday": -1, "kemarin lusa": -2}
    if s in rel:
        return _cek_arah(acuan + timedelta(days=rel[s]), acuan, arah, asli)
    m = re.fullmatch(r"\+ ?(\d{1,3})( ?(hari|hr|h))?|(\d{1,3}) ?(hari|hr|h)( lagi)?", s)
    if m:
        return _cek_arah(acuan + timedelta(days=int(m.group(1) or m.group(4))), acuan, arah, asli)
    m = re.fullmatch(r"(\d{1,3}) ?(hari|hr) ?(yang )?lalu", s)
    if m:
        return _cek_arah(acuan - timedelta(days=int(m.group(1))), acuan, arah, asli)
    m = re.fullmatch(r"(\d{1,2}) ?(minggu|mgg|pekan) ?lagi", s)
    if m:
        return _cek_arah(acuan + timedelta(days=7 * int(m.group(1))), acuan, arah, asli)
    m = re.fullmatch(r"(\d{1,2}) ?bulan ?lagi", s)
    if m:
        return _cek_arah(_tambah_bulan(acuan, int(m.group(1))), acuan, arah, asli)
    if s in ("minggu depan", "pekan depan", "next week"):
        d, cat = _cek_arah(acuan + timedelta(days=7), acuan, arah, asli)
        return d, ["\"%s\" diartikan 7 hari dari hari ini (%s)." % (asli, tgl_pendek(d))] + cat
    if s in ("bulan depan", "next month"):
        d, cat = _cek_arah(_tambah_bulan(acuan, 1), acuan, arah, asli)
        return d, ["\"%s\" diartikan tanggal yang sama bulan depan (%s)." % (asli, tgl_pendek(d))] + cat
    m = re.fullmatch(r"(hari )?([a-z']+)( depan| ini| lalu| kemarin| kmrn)?", s)
    if m and m.group(2) in NAMA_HARI:
        target, akhir = NAMA_HARI[m.group(2)], (m.group(3) or "").strip()
        maju = (target - acuan.weekday()) % 7
        mundur = (acuan.weekday() - target) % 7
        if akhir in ("lalu", "kemarin", "kmrn"):
            return _cek_arah(acuan - timedelta(days=mundur or 7), acuan, arah, asli)
        if arah == "lalu":
            if akhir == "depan":
                raise Gagal("'%s' ada di masa depan; tanggal kejadian harus hari ini atau sebelumnya." % asli)
            return acuan - timedelta(days=mundur), []
        if maju == 0 and akhir == "ini":
            return acuan, []
        d = acuan + timedelta(days=maju or 7)
        cat = []
        if maju == 0:
            cat.append("Hari ini juga %s; dipakai %s depan (%s)." % (HARI[target], HARI[target], tgl_pendek(d)))
        elif akhir == "depan":
            cat.append("\"%s\" diartikan %s terdekat (%s). Kalau maksudnya minggu berikutnya, sebut tanggalnya."
                       % (asli, HARI[target], tgl_pendek(d)))
        return d, cat
    s2 = re.sub(r"^(hari )?(senin|selasa|rabu|kamis|jumat|jum'at|sabtu|minggu|ahad) ", "", s)
    s2 = re.sub(r"^(tgl\.?|tanggal) ?", "", s2).strip()
    m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", s2)
    if m:
        return _cek_arah(_tanggal(int(m.group(1)), int(m.group(2)), int(m.group(3)), asli), acuan, arah, asli)
    m = re.fullmatch(r"(\d{1,2})[/.-](\d{1,2})[/.-](\d{2}|\d{4})", s2)
    if m:
        y = int(m.group(3))
        y = y + 2000 if y < 100 else y
        return _cek_arah(_tanggal(y, int(m.group(2)), int(m.group(1)), asli), acuan, arah, asli)
    m = re.fullmatch(r"(\d{1,2})[/-](\d{1,2})", s2)
    if m:
        d, cat = _tanpa_tahun(int(m.group(1)), int(m.group(2)), acuan, arah, asli)
        d, cat2 = _cek_arah(d, acuan, arah, asli)
        return d, cat + cat2
    m = re.fullmatch(r"(\d{1,2}) ?([a-z]+)\.?( (\d{4}))?", s2)
    if m and m.group(2) in NAMA_BULAN:
        if m.group(4):
            return _cek_arah(_tanggal(int(m.group(4)), NAMA_BULAN[m.group(2)], int(m.group(1)), asli), acuan,
                             arah, asli)
        d, cat = _tanpa_tahun(int(m.group(1)), NAMA_BULAN[m.group(2)], acuan, arah, asli)
        d, cat2 = _cek_arah(d, acuan, arah, asli)
        return d, cat + cat2
    m = re.fullmatch(r"(\d{1,2})", s2)
    if m and s2 != s:  # hanya "tgl 3"/"tanggal 3" (angka polos terlalu ambigu)
        h = int(m.group(1))
        if not 1 <= h <= 31:
            raise Gagal("Tanggal '%s' tidak ada di kalender." % asli)
        for k in (range(0, 13) if arah != "lalu" else range(0, -13, -1)):
            b = _tambah_bulan(date(acuan.year, acuan.month, 1), k)
            try:
                c = date(b.year, b.month, h)
            except ValueError:
                continue
            if (arah != "lalu" and c >= acuan) or (arah == "lalu" and c <= acuan):
                return c, ([] if c.month == acuan.month else
                           ["Bulan tidak disebut; dipakai %s (tanggal %d terdekat)." % (tgl_pendek(c), h)])
    raise Gagal("Tanggal '%s' tidak dikenali. Contoh yang bisa: 3/10, 3 Okt, 3/10/2026, besok, lusa, Jumat, "
                "3 hari lagi, minggu depan." % asli)


def parse_hari_ini(teks):
    s = str(teks).strip()
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(s, fmt)
            return dt if fmt != "%Y-%m-%d" else dt.replace(hour=9)
        except ValueError:
            continue
    raise Gagal("--hari-ini harus berformat YYYY-MM-DD atau 'YYYY-MM-DD HH:MM'.")


# --------------------------------------------------------------------------- angka & rupiah
def rp(n):
    if n is None:
        return "-"
    n = int(n)
    return ("-" if n < 0 else "") + "Rp " + "{:,}".format(abs(n)).replace(",", ".")


def bulat(x):
    """Bilangan bulat terdekat, setengah ke atas (0,5 -> 1). Menerima int/Decimal/Fraction."""
    d = Decimal(x.numerator) / Decimal(x.denominator) if isinstance(x, Fraction) else Decimal(x)
    return int(d.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def persen(pembilang, penyebut):
    """(float 1 desimal, teks '33,3%') atau (None, '-') bila penyebut 0. Dihitung pecahan persis, dibulatkan sekali."""
    if not penyebut:
        return None, "-"
    f = Fraction(pembilang * 100, penyebut)
    d = (Decimal(f.numerator) / Decimal(f.denominator)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    return float(d), ("%s%%" % d).replace(".", ",")


SATUAN_NOMINAL = {"rb": 1000, "ribu": 1000, "rbu": 1000, "k": 1000, "jt": 10 ** 6, "juta": 10 ** 6,
                  "jeti": 10 ** 6, "miliar": 10 ** 9, "milyar": 10 ** 9, "M": 10 ** 9}


def parse_nominal(teks):
    """'4,5 jt' | '4.500.000' | 'Rp4.500.000' | '750rb' | '4 jt 500 rb' | '1,2 M' -> int rupiah."""
    if teks is None or not str(teks).strip():
        raise Gagal("Nilai kosong.")
    asli = str(teks).strip()
    s = re.sub(r"(?i)^\s*(rp\.?|idr)\s*", "", asli).strip()
    s = re.sub(r"(?i)\s*(,-|\.-)$", "", s)
    if s.startswith("-"):
        raise Gagal("Nilai '%s' tidak boleh negatif." % asli)
    bagian = re.findall(r"(\d[\d.,]*)\s*([A-Za-z]+)?\s*", s)
    if not bagian or re.sub(r"(\d[\d.,]*)\s*([A-Za-z]+)?\s*", "", s).strip(" dan&+"):
        raise Gagal("Nilai '%s' tidak dikenali. Contoh: 450rb, 4,5 jt, 4.500.000." % asli)
    total = Decimal(0)
    for i, (angka, sat) in enumerate(bagian):
        if sat == "m":
            raise Gagal("Nilai '%s' ambigu: 'm' itu juta atau miliar? Tulis 'jt' atau 'miliar'." % asli)
        if sat and sat not in SATUAN_NOMINAL and sat.lower() not in SATUAN_NOMINAL:
            raise Gagal("Satuan '%s' pada nilai '%s' tidak dikenal. Pakai rb, jt, atau miliar." % (sat, asli))
        kali = SATUAN_NOMINAL.get(sat, SATUAN_NOMINAL.get((sat or "").lower(), 1)) if sat else 1
        if len(bagian) > 1 and not sat:
            raise Gagal("Nilai '%s' ambigu: bagian '%s' tidak bersatuan. Tulis mis. '4 jt 500 rb'." % (asli, angka))
        angka = re.sub(r"[.,]00$", "", angka) if not sat else angka
        pisah = re.findall(r"[.,]", angka)
        if not pisah:
            nilai = Decimal(angka)
        elif sat:
            m = re.fullmatch(r"(\d+)[.,](\d{1,2})", angka)
            if not m:
                raise Gagal("Nilai '%s' ambigu (mis. '1.500 jt' = 1,5 juta atau 1.500 juta?). Tulis mis. '1,5 jt' "
                            "atau '1500000'." % asli)
            nilai = Decimal(m.group(1) + "." + m.group(2))
        else:
            if re.fullmatch(r"\d{1,3}([.]\d{3})+|\d{1,3}(,\d{3})+", angka):
                nilai = Decimal(re.sub(r"[.,]", "", angka))
            else:
                raise Gagal("Nilai '%s' ambigu. Tulis mis. '4,5 jt', '450rb', atau '4.500.000'." % asli)
        total += nilai * kali
    if total != total.to_integral_value():
        raise Gagal("Nilai '%s' menghasilkan pecahan rupiah; tulis dalam rupiah bulat." % asli)
    return int(total)


def nilai_opsional(teks):
    """None bila '-'/'kosong'/'hapus'; selain itu parse_nominal."""
    if teks is None:
        return None
    if str(teks).strip().lower() in ("-", "kosong", "hapus", "tidak ada", "0"):
        return 0 if str(teks).strip() == "0" else None
    return parse_nominal(teks)


# --------------------------------------------------------------------------- nomor WA
def normalisasi_wa(teks):
    """Kembalikan (nomor '62...', [peringatan]). Menolak nomor yang tidak wajar."""
    asli = str(teks or "").strip()
    if not asli:
        raise Gagal("Nomor WA kosong.")
    if re.search(r"\d[.,]\d+\s*e\+?\d+", asli, re.I):
        raise Gagal("Nomor '%s' rusak: Excel mengubahnya menjadi angka ilmiah. Di Excel, format kolom nomor "
                    "sebagai Teks lalu ketik ulang/ekspor ulang." % asli)
    s = re.sub(r"(?i)^(no\.?|nomor|nmr|hp|wa|whatsapp|telp\.?|tel|phone)\s*[:.]?\s*", "", asli)
    s = re.sub(r"(?i)^(hp|wa|whatsapp)\s*[:.]?\s*", "", s)
    potong = [p for p in re.split(r"\s*(?:/|,|;|\batau\b|\bdan\b|&)\s*", s) if re.sub(r"\D", "", p)]
    if len(potong) > 1 and all(len(re.sub(r"\D", "", p)) >= 8 for p in potong):
        raise Gagal("Ada lebih dari satu nomor di '%s'. Simpan satu nomor WA saja per kontak; nomor lain bisa "
                    "ditulis di catatan." % asli)
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
        return d, ["Nomor %s bukan nomor Indonesia (+%s...); pastikan kode negaranya benar." % (asli, d[:2])]
    else:
        raise Gagal("Nomor '%s' tidak dikenali. Nomor Indonesia diawali 08, 62, atau +62." % asli)
    sisa = d[2:]
    if sisa.startswith("0"):
        sisa = sisa.lstrip("0")
        peringatan.append("Nomor '%s' berisi 0 setelah kode negara; angka 0 itu dibuang." % asli)
        d = "62" + sisa
    if not 9 <= len(sisa) <= 12:
        raise Gagal("Nomor '%s' tidak wajar: %d digit setelah 62 (nomor HP Indonesia 9-12 digit, mis. "
                    "0812-0000-1234)." % (asli, len(sisa)))
    if not sisa.startswith("8"):
        peringatan.append("Nomor %s bukan nomor HP (mungkin telepon kantor); pastikan nomor ini memakai "
                          "WhatsApp." % tampil_wa(d))
    return d, peringatan


def tampil_wa(wa):
    if not wa:
        return "-"
    if wa.startswith("62"):
        lok = "0" + wa[2:]
        if len(lok) >= 10:
            return "%s-%s-%s" % (lok[:4], lok[4:-4], lok[-4:])
        return lok
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
    if kata:
        depan.append(kata[0][0].upper() + ".")
    return " ".join(depan)


def link_wa(wa, teks):
    if not wa:
        return None
    return "https://wa.me/%s?text=%s" % (wa, quote(teks, safe=""))


# --------------------------------------------------------------------------- normalisasi teks
def bersih(teks, maks=200):
    s = re.sub(r"[\x00-\x08\x0b-\x1f\x7f]", " ", str(teks or ""))
    s = re.sub(r"[ \t]+", " ", s).strip()
    return s[:maks]


def norm_tahap(teks):
    s = re.sub(r"\s+", " ", str(teks or "").strip().lower())
    if s in ALIAS_TAHAP:
        return ALIAS_TAHAP[s]
    raise Gagal("Tahap '%s' tidak dikenal. Pilihan: baru, dihubungi, ditawar, deal, selesai, batal." % teks)


def norm_sumber(teks):
    s = re.sub(r"\s+", " ", str(teks or "").strip())
    if not s:
        return "Tidak diketahui", False
    k = s.lower()
    for alias, baku in ALIAS_SUMBER:
        if k in alias or k == baku.lower():
            return baku, False
    return bersih(s[:1].upper() + s[1:], 40), True


def norm_alasan(teks):
    s = bersih(teks, 120)
    k = s.lower()
    for alias, baku in ALIAS_ALASAN:
        if k in alias or k == baku:
            return baku
    return k


def norm_label(teks):
    hasil = []
    for x in re.split(r"[,;#]", str(teks or "")):
        x = re.sub(r"\s+", " ", x.strip().lower())
        if x and x not in hasil:
            hasil.append(x[:30])
    return hasil


def kunci_nama(nama):
    kata = [k for k in re.sub(r"[^\w\s]", " ", (nama or "").lower()).split()]
    while kata and kata[0] in SAPAAN_DIKENAL:
        kata.pop(0)
    return " ".join(kata)


# --------------------------------------------------------------------------- database
SKEMA_SQL = """
CREATE TABLE meta(kunci TEXT PRIMARY KEY, nilai TEXT);
CREATE TABLE kontak(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nama TEXT NOT NULL,
  sapaan TEXT,
  wa TEXT,
  sumber TEXT NOT NULL DEFAULT 'Tidak diketahui',
  label TEXT NOT NULL DEFAULT '',
  tahap TEXT NOT NULL DEFAULT 'baru',
  nilai INTEGER,
  kebutuhan TEXT NOT NULL DEFAULT '',
  followup TEXT,
  fu_ke INTEGER NOT NULL DEFAULT 0,
  alasan_batal TEXT,
  tgl_masuk TEXT NOT NULL,
  tgl_tahap TEXT NOT NULL,
  tgl_deal TEXT,
  tgl_batal TEXT,
  kontak_terakhir TEXT,
  dibuat TEXT NOT NULL,
  diubah TEXT NOT NULL
);
CREATE INDEX kontak_wa ON kontak(wa);
CREATE INDEX kontak_followup ON kontak(followup);
CREATE TABLE riwayat(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  kontak_id INTEGER NOT NULL,
  waktu TEXT NOT NULL,
  jenis TEXT NOT NULL,
  isi TEXT NOT NULL DEFAULT ''
);
CREATE INDEX riwayat_kontak ON riwayat(kontak_id);
CREATE TABLE log(id INTEGER PRIMARY KEY AUTOINCREMENT, waktu TEXT, perintah TEXT, ringkasan TEXT);
"""
PENGATURAN_DEFAULT = {"nama_usaha": "", "pengirim": "", "sapaan": "Kak", "zona": "WIB"}


def path_db(args):
    if getattr(args, "db", None):
        return Path(args.db).expanduser()
    env = os.environ.get("KOMUNITECH_CRM_DB")
    if env:
        return Path(env).expanduser()
    folder = os.environ.get("KOMUNITECH_DATA")
    if folder:
        return Path(folder).expanduser() / "crm" / "crm.db"
    return Path.home() / "KomunitechData" / "crm" / "crm.db"


def folder_backup(db):
    return db.parent / "backup-crm"


def buka(db, baca_saja=False):
    if not db.is_file():
        raise Gagal("Database CRM belum ada di %s. Jalankan dulu: crm.py init (lalu --ya setelah pengguna setuju)."
                    % db, db=str(db), belum_ada=True)
    try:
        if baca_saja:
            conn = sqlite3.connect(db.resolve().as_uri() + "?mode=ro", uri=True, timeout=_timeout(),
                                   isolation_level=None)
        else:
            conn = sqlite3.connect(str(db), timeout=_timeout(), isolation_level=None)
    except sqlite3.OperationalError as e:
        raise Gagal("Database %s tidak bisa dibuka (%s). Periksa folder dan izin aksesnya." % (db, e))
    conn.row_factory = sqlite3.Row
    try:
        r = conn.execute("SELECT nilai FROM meta WHERE kunci='aplikasi'").fetchone()
        sk = conn.execute("SELECT nilai FROM meta WHERE kunci='skema'").fetchone()
    except sqlite3.OperationalError as e:
        conn.close()
        if _terkunci(e):
            raise Gagal(PESAN_TERKUNCI % _timeout())
        raise Gagal("File %s bukan database crm-wa (%s). File itu tidak diubah; periksa --db." % (db, e))
    except sqlite3.DatabaseError:
        conn.close()
        raise Gagal("File %s rusak atau bukan database crm-wa. Jangan hapus file itu. Pulihkan dari cadangan: "
                    "crm.py backup --daftar, lalu crm.py restore --dari <file> (pratinjau dulu)." % db, rusak=True)
    if not r or r[0] != APLIKASI:
        conn.close()
        raise Gagal("File %s bukan database crm-wa. File itu tidak diubah; periksa --db." % db)
    if sk and str(sk[0]).isdigit() and int(sk[0]) > SKEMA:
        conn.close()
        raise Gagal("Database dibuat oleh crm-wa versi lebih baru (skema %s). Perbarui skill crm-wa dulu." % sk[0])
    cfg = pengaturan(conn)
    _JAM["zona"] = cfg["zona"] if cfg["zona"] in ZONA else "WIB"
    return conn


def pengaturan(conn):
    cfg = dict(PENGATURAN_DEFAULT)
    for r in conn.execute("SELECT kunci, nilai FROM meta"):
        cfg[r[0]] = r[1]
    return cfg


def buat_backup(db, label):
    if not db.is_file():
        return None
    fol = folder_backup(db)
    fol.mkdir(parents=True, exist_ok=True)
    cap = kini().strftime("%Y%m%d-%H%M%S")
    tujuan = fol / ("crm-%s-%s.db" % (cap, label))
    n = 2
    while tujuan.exists():
        tujuan = fol / ("crm-%s-%s-%d.db" % (cap, label, n))
        n += 1
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
            raise Gagal(PESAN_TERKUNCI % _timeout())
        raise
    finally:
        dst.close()
        src.close()
    return str(tujuan)


def backup_harian(db):
    """Cadangan otomatis sekali sehari (sebelum perubahan pertama hari itu). Simpan 30 terakhir."""
    fol = folder_backup(db)
    awalan = "crm-%s-" % kini().strftime("%Y%m%d")
    if fol.is_dir() and any(p.name.startswith(awalan) for p in fol.glob("crm-*.db")):
        return None
    b = buat_backup(db, "harian")
    harian = sorted(p for p in fol.glob("crm-*-harian*.db"))
    for lama in harian[:-SIMPAN_BACKUP_HARIAN]:
        try:
            lama.unlink()
        except OSError:
            pass
    return b


def jalankan_tulis(args, perintah, kerja, besar=False, label_backup=None):
    """Jalankan kerja(conn) dalam satu transaksi.

    besar=True  -> tanpa --ya: ROLLBACK (pratinjau persis, database tidak berubah); dengan --ya: backup lalu COMMIT.
    besar=False -> langsung tersimpan (perubahan kecil), dengan cadangan harian otomatis.
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
                raise Gagal(PESAN_TERKUNCI % _timeout())
            raise
        try:
            data, teks = kerja(conn, pengaturan(conn))
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
    if simpan:
        if besar:
            teks = "TERSIMPAN.\n" + teks + (("\nCadangan sebelum perubahan: " + backup) if backup else "")
    else:
        teks = ("PRATINJAU (belum disimpan):\n" + teks +
                "\n\nSimpan? Jalankan perintah yang sama + --ya setelah pengguna setuju.")
    if data["peringatan"]:
        teks += "\n" + "\n".join("Catatan: " + p for p in data["peringatan"])
    data["teks"] = teks
    return data, teks


def riwayat(conn, kid, jenis, isi, waktu=None):
    conn.execute("INSERT INTO riwayat(kontak_id, waktu, jenis, isi) VALUES (?,?,?,?)",
                 (kid, waktu or stempel(), jenis, bersih(isi, 1000)))


def kode(kid):
    return "K%04d" % int(kid)


def ambil(conn, kid):
    return conn.execute("SELECT * FROM kontak WHERE id=?", (kid,)).fetchone()


def cari_kontak(conn, ref):
    """Temukan satu kontak dari kode (K0003/3), nomor WA, atau nama. Ambigu -> Gagal berisi pilihan."""
    s = str(ref or "").strip()
    if not s:
        raise Gagal("Kontak belum disebut. Sebut nama, kode (mis. K0003), atau nomor WA.")
    m = re.fullmatch(r"(?i)#?k?0*(\d{1,6})", s)
    if m:
        r = ambil(conn, int(m.group(1)))
        if r:
            return r
        if s.lower().startswith(("k", "#")) or len(m.group(1)) < 6:
            raise Gagal("Kontak %s tidak ada. Cek dengan: crm.py daftar --tahap semua" % s)
    if len(re.sub(r"\D", "", s)) >= 8:
        try:
            wa, _ = normalisasi_wa(s)
        except Gagal:
            wa = None
        if wa:
            rows = conn.execute("SELECT * FROM kontak WHERE wa=? ORDER BY id", (wa,)).fetchall()
            if len(rows) == 1:
                return rows[0]
            if len(rows) > 1:
                raise Gagal("Nomor %s dipakai %d kontak. Sebut kodenya." % (tampil_wa(wa), len(rows)),
                            pilihan=[pilihan_json(r) for r in rows])
            raise Gagal("Tidak ada kontak dengan nomor %s." % tampil_wa(wa))
    k = s.lower()
    semua = conn.execute("SELECT * FROM kontak ORDER BY id").fetchall()
    persis = [r for r in semua if r["nama"].lower() == k]
    if len(persis) == 1:
        return persis[0]
    kn = kunci_nama(s)
    cocok = persis or [r for r in semua if kn and kunci_nama(r["nama"]) == kn]
    if not cocok:
        cocok = [r for r in semua if k in r["nama"].lower() or (kn and kn in kunci_nama(r["nama"]))]
    aktif = [r for r in cocok if r["tahap"] != "batal"]
    if len(cocok) > 1 and len(aktif) == 1:
        return aktif[0]
    if len(cocok) == 1:
        return cocok[0]
    if not cocok:
        raise Gagal("Kontak '%s' tidak ditemukan. Cek ejaan atau lihat: crm.py daftar --tahap semua" % s)
    raise Gagal("Ada %d kontak yang cocok dengan '%s'. Tanyakan yang mana (sebut kodenya)." % (len(cocok), s),
                pilihan=[pilihan_json(r) for r in cocok[:10]])


def pilihan_json(r):
    return {"kode": kode(r["id"]), "nama": r["nama"], "tahap": r["tahap"], "wa": samar_wa(r["wa"]),
            "sumber": r["sumber"], "kebutuhan": r["kebutuhan"]}


def kontak_json(r, samarkan=False):
    return {
        "kode": kode(r["id"]), "nama": samar_nama(r["nama"]) if samarkan else r["nama"],
        "wa": samar_wa(r["wa"]) if samarkan else r["wa"], "wa_tampil": samar_wa(r["wa"]) if samarkan else
        tampil_wa(r["wa"]), "sumber": r["sumber"], "label": norm_label(r["label"]), "tahap": r["tahap"],
        "nilai": r["nilai"], "kebutuhan": r["kebutuhan"], "followup": r["followup"], "fu_ke": r["fu_ke"],
        "alasan_batal": r["alasan_batal"], "tgl_masuk": r["tgl_masuk"], "tgl_deal": r["tgl_deal"],
        "tgl_batal": r["tgl_batal"], "kontak_terakhir": r["kontak_terakhir"],
    }


def cek_duplikat_wa(conn, wa, kecuali=None):
    if not wa:
        return []
    return [r for r in conn.execute("SELECT * FROM kontak WHERE wa=? ORDER BY id", (wa,)).fetchall()
            if r["id"] != kecuali]


def followup_default(tahap, acuan):
    if tahap == "baru":
        return acuan, "Follow-up belum disebut; dijadwalkan hari ini (lead baru sebaiknya dibalas hari yang sama)."
    if tahap in ("dihubungi", "ditawar"):
        d = acuan + timedelta(days=2)
        return d, "Follow-up belum disebut; dijadwalkan %s (2 hari lagi). Ubah bila perlu." % tgl_pendek(d)
    return None, None


# --------------------------------------------------------------------------- draf pesan
def panggilan(k, cfg):
    nama = bersih(k["nama"], 80)
    kata = nama.split()
    awal = kata[0].lower().rstrip(".") if kata else ""
    if awal in SAPAAN_DIKENAL:
        return nama
    if awal in AWALAN_LEMBAGA:
        return "Bapak/Ibu di " + nama
    sap = (k["sapaan"] if "sapaan" in k.keys() and k["sapaan"] else cfg.get("sapaan") or "Kak").strip()
    if sap.lower() in ("-", "tanpa", "none"):
        return nama
    return "%s %s" % (sap, nama)


def susun_draf(k, cfg):
    """Kembalikan (jenis_draf, teks) atau (None, alasan) bila kontak tidak perlu dihubungi."""
    t, n = k["tahap"], int(k["fu_ke"] or 0)
    if t == "batal":
        return None, "Kontak berstatus batal; tidak perlu dihubungi. Pindahkan tahapnya dulu jika ingin menyapa lagi."
    p = panggilan(k, cfg)
    usaha, pengirim = bersih(cfg.get("nama_usaha")), bersih(cfg.get("pengirim"))
    if pengirim and usaha:
        diri = "saya %s dari %s" % (pengirim, usaha)
    elif pengirim:
        diri = "saya %s" % pengirim
    elif usaha:
        diri = "kami dari %s" % usaha
    else:
        diri = ""
    salam = ("Halo %s, %s. " % (p, diri)) if diri else ("Halo %s. " % p)
    hal = bersih(k["kebutuhan"], 120)
    if t == "baru":
        teks = "Halo %s, terima kasih sudah menghubungi %s." % (p, usaha or "kami")
        if pengirim:
            teks += " Saya %s." % pengirim
        teks += (" Soal %s, boleh saya bantu jelaskan pilihan dan harganya?" % hal) if hal else \
            " Ada yang bisa saya bantu?"
        teks += " Kira-kira dibutuhkan untuk kapan ya?"
        return "sapaan-awal", teks
    if t in ("dihubungi", "ditawar") and n >= MAKS_FU - 1:
        return "pamit", (salam + "Saya tidak ingin mengganggu, jadi ini pesan terakhir dari saya soal %s. Kalau suatu "
                         "saat butuh, tinggal chat nomor ini ya. Terima kasih atas waktunya." %
                         (hal or "penawaran kami"))
    if t == "dihubungi":
        if n == 0:
            return "follow-up-1", (salam + "Menyambung obrolan kita %s, apakah masih ada yang ingin ditanyakan? "
                                   "Kalau berkenan, saya kirimkan foto atau detail tambahan supaya lebih mudah "
                                   "memilih." % (("soal " + hal) if hal else "sebelumnya"))
        return "pilihan-mudah", (salam + "Sekadar mengingatkan %s. Supaya mudah, cukup balas angka saja: 1 = mau "
                                 "lanjut, 2 = masih pikir-pikir, 3 = belum perlu dulu. Apa pun jawabannya tidak "
                                 "apa-apa, terima kasih." % (("soal " + hal) if hal else "obrolan kita"))
    if t == "ditawar":
        if n == 0:
            return "follow-up-penawaran", (salam + "Menindaklanjuti penawaran %s, apakah sudah sempat "
                                           "dipertimbangkan? Kalau ada yang kurang pas (harga, jumlah, atau jadwal), "
                                           "kabari saja, kita cari jalan tengahnya." % (hal or "yang kami kirim"))
        return "pilihan-mudah", (salam + "Soal penawaran %s, supaya mudah cukup balas angka saja: 1 = lanjut, "
                                 "2 = perlu penyesuaian, 3 = belum dulu. Apa pun jawabannya tidak apa-apa, terima "
                                 "kasih." % (hal or "kami"))
    if t == "deal":
        if n == 0:
            return "konfirmasi-order", (salam + "Terima kasih sudah memutuskan order %s. Mohon dibantu konfirmasi "
                                        "detail pengiriman/jadwal dan pembayarannya ya. Kalau ada yang ingin diubah, "
                                        "kabari saya." % (hal or "dengan kami"))
        return "pengingat-order", (salam + "Mengingatkan kembali soal order %s: apakah detail pembayaran dan "
                                   "pengirimannya sudah bisa dikonfirmasi? Kalau ada kendala, kabari saja supaya "
                                   "kami bantu." % (hal or "kemarin"))
    return "terima-kasih", (salam + "Terima kasih sudah mempercayakan %s kepada kami. Semoga cocok dan bermanfaat. "
                            "Kalau berkenan, boleh minta sedikit ulasan atau testimoni? Kalau butuh lagi, chat saja "
                            "nomor ini." % (hal or "kebutuhannya"))


def draf_json(k, cfg, samarkan=False, pesan=None):
    if pesan:
        jenis, teks = "pesan-sendiri", bersih(pesan, 2000)
    else:
        jenis, teks = susun_draf(k, cfg)
    if jenis is None:
        return {"kode": kode(k["id"]), "nama": samar_nama(k["nama"]) if samarkan else k["nama"], "draf": None,
                "alasan": teks}
    out = {"kode": kode(k["id"]), "nama": samar_nama(k["nama"]) if samarkan else k["nama"], "jenis": jenis,
           "draf": teks, "tautan": None if samarkan else link_wa(k["wa"], teks),
           "dikirim_oleh": "manusia (klik tautan, periksa, lalu tekan Kirim sendiri)"}
    if samarkan:
        out["draf"] = teks.replace(k["nama"], samar_nama(k["nama"]))
    if not k["wa"]:
        out["catatan"] = "Kontak belum punya nomor WA; salin draf secara manual."
    return out


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
    """Kebalikan sel_aman saat impor ulang: "'=abc" -> "=abc" (disimpan sebagai teks biasa di database)."""
    s = str(s or "")
    return s[1:] if len(s) > 1 and s[0] == "'" and s[1] in "=+-@\t\r" else s


def tulis_csv(path, header, rows, timpa=False):
    p = Path(path).expanduser()
    if p.exists() and not timpa:
        raise Gagal("File %s sudah ada. Pakai nama lain atau tambahkan --timpa bila memang ingin ditimpa." % p)
    if p.suffix.lower() in (".db", ".sqlite"):
        raise Gagal("Nama file ekspor harus berakhiran .csv.")
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(str(p), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(header)
        for r in rows:
            w.writerow([sel_aman(x) for x in r])
    return str(p)


def baca_csv(path):
    p = Path(path).expanduser()
    if not p.is_file():
        raise Gagal("File %s tidak ditemukan." % path)
    if p.suffix.lower() in (".xlsx", ".xls", ".ods", ".numbers", ".vcf"):
        raise Gagal("File %s belum didukung langsung. Di Excel/Sheets: File > Save As/Download > CSV, lalu kirim "
                    "file CSV-nya." % p.name)
    raw = p.read_bytes()
    if len(raw) > 20 * 1024 * 1024:
        raise Gagal("File terlalu besar (> 20 MB). Pecah menjadi beberapa file.")
    peringatan = []
    try:
        teks = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        teks = raw.decode("cp1252", errors="replace")
        peringatan.append("File bukan UTF-8; dibaca sebagai Windows-1252 (ANSI). Periksa huruf khusus di nama.")
    baris1 = teks.split("\n", 1)[0]
    pemisah = max([";", ",", "\t"], key=lambda c: baris1.count(c))
    rows = list(csv.reader(io.StringIO(teks), delimiter=pemisah))
    rows = [r for r in rows if any(x.strip() for x in r)]
    if not rows:
        raise Gagal("File %s kosong." % p.name)
    return rows, peringatan


KOLOM_IMPOR = {
    "nama": ("nama", "name", "nama kontak", "nama pelanggan", "nama customer", "customer", "pelanggan", "kontak",
             "full name", "nama lengkap", "display name"),
    "wa": ("wa", "no wa", "nomor wa", "no whatsapp", "nomor whatsapp", "whatsapp", "hp", "no hp", "nomor hp",
           "handphone", "telepon", "telp", "no telp", "nomor telepon", "phone", "phone number", "mobile",
           "phone 1 value", "phone 1   value", "no wa pelanggan"),
    "sumber": ("sumber", "sumber lead", "source", "asal", "asal lead", "channel", "kanal", "dari"),
    "label": ("label", "labels", "tag", "tags", "kategori"),
    "tahap": ("tahap", "status", "stage", "tahapan", "pipeline"),
    "nilai": ("nilai", "nilai potensi", "potensi", "value", "nominal", "budget", "harga", "nilai deal", "omzet"),
    "kebutuhan": ("kebutuhan", "produk", "minat", "produk diminati", "keperluan", "layanan", "interest", "product"),
    "followup": ("followup", "follow up", "follow-up", "tanggal follow up", "jadwal follow up", "next follow up",
                 "tgl follow up"),
    "catatan": ("catatan", "notes", "note", "keterangan", "ket"),
    "alasan_batal": ("alasan batal", "alasan", "alasan_batal"),
    "tgl_masuk": ("tgl masuk", "tanggal masuk", "tgl_masuk", "masuk", "tanggal", "tgl", "created", "tanggal lead"),
    "sapaan": ("sapaan", "panggilan"),
}
KOLOM_ABAIKAN = {"kode", "link wa", "link_wa", "tautan", "no_wa_tampil", "tgl deal", "tgl_deal", "kontak terakhir",
                 "kontak_terakhir", "fu ke", "fu_ke", "tgl batal", "tgl_batal"}


def _kunci_kolom(h):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", buang_pelindung(h).lower())).strip()


def petakan_kolom(header):
    peta, abaikan = {}, []
    for i, h in enumerate(header):
        k = _kunci_kolom(h)
        if k == "no wa" and "wa" in peta:
            continue
        for nama, alias in KOLOM_IMPOR.items():
            if k in {_kunci_kolom(a) for a in alias} and nama not in peta:
                peta[nama] = i
                break
        else:
            if k and k not in {_kunci_kolom(x) for x in KOLOM_ABAIKAN}:
                abaikan.append(h)
    return peta, abaikan


# --------------------------------------------------------------------------- perintah: init / info / atur
def cmd_init(args):
    db = path_db(args)
    zona = kode_zona(args.zona or "WIB")
    if db.exists():
        try:
            conn = buka(db, baca_saja=True)
            conn.close()
            raise Gagal("Database CRM sudah ada di %s. Tidak dibuat ulang (data aman). Untuk mengubah nama usaha/"
                        "pengirim pakai: crm.py atur." % db, sudah_ada=True)
        except Gagal as e:
            if e.detail.get("sudah_ada"):
                raise
            raise Gagal("File %s sudah ada dan bukan database crm-wa; tidak ditimpa. Pakai --db lain." % db)
    cfg = {"nama_usaha": bersih(args.nama_usaha, 80), "pengirim": bersih(args.pengirim, 40),
           "sapaan": bersih(args.sapaan or "Kak", 20), "zona": zona}
    ringkas = ("Database CRM baru: %s\nNama usaha: %s | Pengirim draf: %s | Sapaan default: %s | Zona: %s\n"
               "Cadangan otomatis: %s" % (db, cfg["nama_usaha"] or "-", cfg["pengirim"] or "-", cfg["sapaan"],
                                          zona, folder_backup(db)))
    if not args.ya:
        t = "PRATINJAU (belum dibuat):\n" + ringkas + "\n\nBuat? Jalankan perintah yang sama + --ya setelah pengguna setuju."
        return {"ok": True, "mode": "pratinjau", "perlu_konfirmasi": True, "db": str(db), "pengaturan": cfg,
                "teks": t}, t
    db.parent.mkdir(parents=True, exist_ok=True)
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
    t = "TERSIMPAN. Database CRM siap.\n" + ringkas
    return {"ok": True, "mode": "tersimpan", "perlu_konfirmasi": False, "db": str(db), "pengaturan": cfg,
            "teks": t}, t


def cmd_info(args):
    db = path_db(args)
    if not db.exists():
        t = ("Database CRM belum ada (lokasi: %s). Mulai dengan: crm.py init --nama-usaha \"...\" --pengirim \"...\" "
             "(pratinjau, lalu --ya)." % db)
        return {"ok": True, "mode": "baca", "ada": False, "db": str(db), "versi": VERSI, "teks": t}, t
    conn = buka(db, baca_saja=True)
    try:
        cfg = pengaturan(conn)
        cek = conn.execute("PRAGMA quick_check").fetchone()[0]
        per = {t: 0 for t in TAHAP}
        for r in conn.execute("SELECT tahap, COUNT(*) FROM kontak GROUP BY tahap"):
            per[r[0]] = r[1]
    finally:
        conn.close()
    bks = sorted(folder_backup(db).glob("crm-*.db")) if folder_backup(db).is_dir() else []
    jam_komp = datetime.now().replace(microsecond=0)
    lokal = waktu_lokal(_JAM["zona"])
    peringatan = []
    if abs((jam_komp - lokal).total_seconds()) > 1800:
        peringatan.append("Jam komputer (%s) berbeda dengan jam %s (%s). CRM tetap memakai jam %s untuk "
                          "'hari ini' dan jadwal follow-up." % (jam_komp.strftime("%H:%M"), _JAM["zona"],
                                                                 lokal.strftime("%H:%M"), _JAM["zona"]))
    if cek != "ok":
        peringatan.append("Pemeriksaan database menemukan masalah (%s). Buat cadangan lalu pulihkan dari cadangan "
                          "terakhir yang sehat." % cek)
    t = ("CRM-WA %s\nDatabase: %s\nUsaha: %s | Pengirim: %s | Sapaan: %s | Zona: %s\nKontak: %s (total %d)\n"
         "Pemeriksaan database: %s\nCadangan: %d file di %s%s" %
         (VERSI, db, cfg["nama_usaha"] or "-", cfg["pengirim"] or "-", cfg["sapaan"], cfg["zona"],
          ", ".join("%s %d" % (t, n) for t, n in per.items()), sum(per.values()), cek, len(bks), folder_backup(db),
          ("\nTerakhir: " + bks[-1].name) if bks else ""))
    if peringatan:
        t += "\n" + "\n".join("Catatan: " + p for p in peringatan)
    return {"ok": True, "mode": "baca", "ada": True, "db": str(db), "versi": VERSI, "pengaturan": cfg,
            "per_tahap": per, "pemeriksaan": cek, "jumlah_backup": len(bks),
            "backup_terakhir": str(bks[-1]) if bks else None, "peringatan": peringatan, "teks": t}, t


def cmd_atur(args):
    ubah = {}
    if args.nama_usaha is not None:
        ubah["nama_usaha"] = bersih(args.nama_usaha, 80)
    if args.pengirim is not None:
        ubah["pengirim"] = bersih(args.pengirim, 40)
    if args.sapaan is not None:
        ubah["sapaan"] = bersih(args.sapaan, 20) or "Kak"
    if args.zona is not None:
        ubah["zona"] = kode_zona(args.zona)
    if not ubah:
        raise Gagal("Tidak ada yang diubah. Pakai --nama-usaha, --pengirim, --sapaan, atau --zona.")

    def kerja(conn, cfg):
        for k, v in ubah.items():
            conn.execute("INSERT OR REPLACE INTO meta(kunci, nilai) VALUES (?,?)", (k, v))
        t = "Pengaturan disimpan: " + ", ".join("%s = %s" % (k, v or "-") for k, v in ubah.items())
        return {"pengaturan": ubah, "ringkasan": ubah}, t
    return jalankan_tulis(args, "atur", kerja)


# --------------------------------------------------------------------------- perintah: tambah / ubah / catat
def cmd_tambah(args):
    acuan = hari_ini()
    nama = bersih(args.nama, 80)
    if not nama:
        raise Gagal("Nama kontak kosong.")
    peringatan = []
    if re.search(r"\d{8,}|\d{3,4}[-\s]\d{3,4}[-\s]\d{3,4}", nama):
        raise Gagal("Kolom nama berisi nomor telepon. Isi nama di --nama dan nomor di --wa.")
    wa = None
    if args.wa:
        wa, p = normalisasi_wa(args.wa)
        peringatan += p
    else:
        peringatan.append("Nomor WA belum ada; draf pesan tidak bisa dibuatkan tautan wa.me. Tambahkan nanti dengan "
                          "crm.py ubah --kontak <kode> --wa <nomor>.")
    sumber, sumber_baru = norm_sumber(args.sumber)
    if sumber_baru:
        peringatan.append("Sumber '%s' belum ada di daftar baku; disimpan apa adanya." % sumber)
    tahap = norm_tahap(args.tahap) if args.tahap else "baru"
    nilai = nilai_opsional(args.nilai) if args.nilai else None
    masuk, cat = baca_tanggal(args.masuk, acuan, "lalu") if args.masuk else (acuan, [])
    peringatan += cat
    alasan = None
    if tahap == "batal":
        if not args.alasan:
            raise Gagal("Tahap batal butuh alasan singkat (mis. harga terlalu mahal, tidak ada respon, pilih penjual "
                        "lain, belum butuh). Tanyakan ke pengguna lalu isi --alasan.")
        alasan = norm_alasan(args.alasan)
    if args.followup:
        fu, cat = baca_tanggal(args.followup, acuan, "depan")
        peringatan += cat
    else:
        fu, cat = followup_default(tahap, acuan)
        if cat:
            peringatan.append(cat)

    def kerja(conn, cfg):
        dup = cek_duplikat_wa(conn, wa)
        if dup and not args.izinkan_duplikat:
            raise Gagal("Nomor %s sudah tersimpan sebagai %s. Tidak ditambah dobel. Untuk mencatat obrolan baru "
                        "pakai: crm.py catat --kontak %s --isi \"...\". Jika memang orang berbeda dengan nomor yang "
                        "sama, ulangi dengan --izinkan-duplikat." %
                        (tampil_wa(wa), ", ".join("%s %s (%s)" % (kode(r["id"]), r["nama"], r["tahap"]) for r in dup),
                         kode(dup[0]["id"])), duplikat=[pilihan_json(r) for r in dup])
        mirip = [r for r in conn.execute("SELECT * FROM kontak").fetchall()
                 if kunci_nama(r["nama"]) == kunci_nama(nama) and kunci_nama(nama)]
        if mirip:
            peringatan.append("Nama mirip kontak lain: %s. Jika orangnya sama, gabungkan dengan crm.py gabung." %
                              ", ".join("%s %s (%s)" % (kode(r["id"]), r["nama"], samar_wa(r["wa"])) for r in mirip))
        now = stempel()
        tgl_deal = masuk.isoformat() if tahap in TAHAP_MENANG else None
        cur = conn.execute(
            "INSERT INTO kontak(nama, sapaan, wa, sumber, label, tahap, nilai, kebutuhan, followup, fu_ke, "
            "alasan_batal, tgl_masuk, tgl_tahap, tgl_deal, tgl_batal, kontak_terakhir, dibuat, diubah) "
            "VALUES (?,?,?,?,?,?,?,?,?,0,?,?,?,?,?,?,?,?)",
            (nama, bersih(args.sapaan, 20) or None, wa, sumber, ", ".join(norm_label(args.label)), tahap, nilai,
             bersih(args.kebutuhan, 120), fu.isoformat() if fu else None, alasan, masuk.isoformat(),
             acuan.isoformat(), tgl_deal, acuan.isoformat() if tahap == "batal" else None, None, now, now))
        kid = cur.lastrowid
        riwayat(conn, kid, "masuk", "Kontak ditambahkan (sumber %s, tahap %s)" % (sumber, tahap))
        if args.catatan:
            riwayat(conn, kid, "catatan", args.catatan)
        k = ambil(conn, kid)
        t = "Tersimpan %s: %s | %s | %s | sumber %s%s%s%s" % (
            kode(kid), nama, tampil_wa(wa), LABEL_TAHAP[tahap], sumber,
            (" | nilai " + rp(nilai)) if nilai is not None else "",
            (" | follow-up " + tgl_panjang(fu)) if fu else "", (" | label: " + k["label"]) if k["label"] else "")
        return {"kontak": kontak_json(k), "peringatan": peringatan,
                "ringkasan": {"kode": kode(kid), "tahap": tahap}}, t
    return jalankan_tulis(args, "tambah", kerja)


def cmd_ubah(args):
    def kerja(conn, cfg):
        k = cari_kontak(conn, args.kontak)
        kid, ubah, peringatan = k["id"], {}, []
        if args.nama is not None:
            n = bersih(args.nama, 80)
            if not n:
                raise Gagal("Nama tidak boleh kosong.")
            ubah["nama"] = n
        if args.wa is not None:
            if args.wa.strip() in ("-", ""):
                ubah["wa"] = None
            else:
                wa, p = normalisasi_wa(args.wa)
                peringatan += p
                dup = cek_duplikat_wa(conn, wa, kecuali=kid)
                if dup and not args.izinkan_duplikat:
                    raise Gagal("Nomor %s sudah dipakai %s. Jika orangnya sama, gabungkan: crm.py gabung --dari %s "
                                "--ke %s. Jika memang berbeda, ulangi dengan --izinkan-duplikat." %
                                (tampil_wa(wa), ", ".join(kode(r["id"]) + " " + r["nama"] for r in dup),
                                 kode(kid), kode(dup[0]["id"])), duplikat=[pilihan_json(r) for r in dup])
                ubah["wa"] = wa
        if args.sumber is not None:
            ubah["sumber"], baru = norm_sumber(args.sumber)
            if baru:
                peringatan.append("Sumber '%s' belum ada di daftar baku; disimpan apa adanya." % ubah["sumber"])
        if args.label is not None:
            ubah["label"] = ", ".join(norm_label(args.label))
        if args.tambah_label or args.hapus_label:
            lab = norm_label(ubah.get("label", k["label"]))
            lab += [x for x in norm_label(args.tambah_label) if x not in lab]
            lab = [x for x in lab if x not in norm_label(args.hapus_label)]
            ubah["label"] = ", ".join(lab)
        if args.nilai is not None:
            ubah["nilai"] = nilai_opsional(args.nilai)
        if args.kebutuhan is not None:
            ubah["kebutuhan"] = bersih(args.kebutuhan, 120)
        if args.sapaan is not None:
            ubah["sapaan"] = bersih(args.sapaan, 20) or None
        if args.masuk is not None:
            d, cat = baca_tanggal(args.masuk, hari_ini(), "lalu")
            ubah["tgl_masuk"] = d.isoformat()
            peringatan += cat
        if not ubah:
            raise Gagal("Tidak ada yang diubah. Pakai --nama, --wa, --sumber, --label, --tambah-label, --hapus-label, "
                        "--nilai, --kebutuhan, --sapaan, atau --masuk. Tahap/catatan/follow-up: pakai crm.py catat.")
        ubah["diubah"] = stempel()
        conn.execute("UPDATE kontak SET %s WHERE id=?" % ", ".join("%s=?" % c for c in ubah),
                     list(ubah.values()) + [kid])
        rinci = ", ".join("%s: %s" % (c, (rp(v) if c == "nilai" and v is not None else
                                          tampil_wa(v) if c == "wa" else (v if v not in (None, "") else "-")))
                          for c, v in ubah.items() if c != "diubah")
        riwayat(conn, kid, "ubah", rinci)
        k2 = ambil(conn, kid)
        return {"kontak": kontak_json(k2), "peringatan": peringatan,
                "ringkasan": {"kode": kode(kid), "ubah": list(ubah)}}, "Diubah %s %s: %s" % (kode(kid), k2["nama"],
                                                                                           rinci)
    return jalankan_tulis(args, "ubah", kerja)


def terapkan_tahap(conn, k, tahap_baru, alasan, tanggal, peringatan):
    """Ubah tahap + tanggal terkait. Kembalikan dict kolom yang berubah."""
    lama = k["tahap"]
    if tahap_baru == lama:
        peringatan.append("Tahap sudah %s; tidak berubah." % tahap_baru)
        return {}
    ubah = {"tahap": tahap_baru, "tgl_tahap": tanggal.isoformat(), "fu_ke": 0}
    if tahap_baru == "batal":
        if not alasan:
            raise Gagal("Tahap batal butuh alasan singkat (mis. harga terlalu mahal, tidak ada respon, pilih penjual "
                        "lain, belum butuh). Tanyakan ke pengguna lalu isi --alasan.")
        ubah.update(alasan_batal=norm_alasan(alasan), tgl_batal=tanggal.isoformat())
    elif lama == "batal":
        ubah.update(alasan_batal=None, tgl_batal=None)
        peringatan.append("Kontak diaktifkan kembali dari batal (alasan lama: %s)." % (k["alasan_batal"] or "-"))
    if tahap_baru in TAHAP_MENANG:
        if not k["tgl_deal"]:
            ubah["tgl_deal"] = tanggal.isoformat()
    elif k["tgl_deal"]:
        ubah["tgl_deal"] = None
        peringatan.append("Kontak mundur dari %s ke %s; tanggal deal dihapus dari rekap." % (lama, tahap_baru))
    if tahap_baru in TAHAP_MENANG and k["nilai"] is None:
        peringatan.append("Nilai deal belum diisi, jadi tidak ikut dijumlahkan di rekap. Tanyakan nilainya lalu "
                          "isi --nilai.")
    return ubah


def cmd_catat(args):
    acuan = hari_ini()
    if not any([args.isi, args.tahap, args.nilai, args.followup, args.tanpa_followup]):
        raise Gagal("Tidak ada yang dicatat. Isi minimal satu: --isi, --tahap, --nilai, --followup.")
    if args.followup and args.tanpa_followup:
        raise Gagal("Pilih salah satu: --followup atau --tanpa-followup.")
    tgl, cat_tgl = baca_tanggal(args.tanggal, acuan, "lalu") if args.tanggal else (acuan, [])

    def kerja(conn, cfg):
        k = cari_kontak(conn, args.kontak)
        kid, peringatan, ubah, bagian = k["id"], list(cat_tgl), {}, []
        tahap = norm_tahap(args.tahap) if args.tahap else k["tahap"]
        if args.tahap:
            ubah.update(terapkan_tahap(conn, k, tahap, args.alasan, tgl, peringatan))
            if "tahap" in ubah:
                bagian.append("tahap %s -> %s%s" % (k["tahap"], tahap,
                                                   (" (alasan: %s)" % ubah["alasan_batal"]) if tahap == "batal" else ""))
        elif args.alasan and k["tahap"] == "batal":
            ubah["alasan_batal"] = norm_alasan(args.alasan)
            bagian.append("alasan batal: %s" % ubah["alasan_batal"])
        if args.nilai is not None:
            ubah["nilai"] = nilai_opsional(args.nilai)
            bagian.append("nilai %s" % rp(ubah["nilai"]))
            if tahap in TAHAP_MENANG and ubah["nilai"] is not None:
                peringatan[:] = [p for p in peringatan if not p.startswith("Nilai deal belum diisi")]
        if args.followup:
            fu, cat = baca_tanggal(args.followup, acuan, "depan")
            peringatan += cat
            ubah["followup"] = fu.isoformat()
            bagian.append("follow-up %s" % tgl_panjang(fu))
        elif args.tanpa_followup or (args.tahap and tahap in ("selesai", "batal")):
            if k["followup"]:
                ubah["followup"] = None
                bagian.append("jadwal follow-up dihapus")
        elif "tahap" in ubah and tahap in TAHAP_TERBUKA:
            fu, cat = followup_default(tahap, acuan)
            ubah["followup"] = fu.isoformat()
            peringatan.append(cat)
            bagian.append("follow-up %s" % tgl_panjang(fu))
        elif "tahap" in ubah and tahap == "deal" and not k["followup"]:
            peringatan.append("Mau dijadwalkan follow-up pembayaran/pengiriman? Isi --followup bila perlu.")
        if args.isi:
            ubah["kontak_terakhir"] = tgl.isoformat()
            riwayat(conn, kid, "catatan", args.isi, waktu=(tgl.isoformat() + " 00:00:00") if args.tanggal else None)
            bagian.insert(0, "catatan \"%s\"" % bersih(args.isi, 80))
        lain = [b for b in bagian if not b.startswith("catatan")]
        if lain:
            riwayat(conn, kid, "tahap" if "tahap" in ubah else "ubah", "; ".join(lain))
        if args.alasan and tahap != "batal":
            peringatan.append("Alasan hanya dipakai untuk tahap batal; diabaikan.")
        if not ubah and not args.isi:
            t = "Tidak ada perubahan untuk %s %s." % (kode(kid), k["nama"])
            return {"kontak": kontak_json(k), "peringatan": peringatan, "ringkasan": {}}, t
        if ubah:
            ubah["diubah"] = stempel()
            conn.execute("UPDATE kontak SET %s WHERE id=?" % ", ".join("%s=?" % c for c in ubah),
                         list(ubah.values()) + [kid])
        k2 = ambil(conn, kid)
        t = "Dicatat %s %s: %s.\nSekarang: %s%s%s" % (
            kode(kid), k2["nama"], "; ".join(bagian) or "-", LABEL_TAHAP[k2["tahap"]],
            (" | nilai " + rp(k2["nilai"])) if k2["nilai"] is not None else "",
            (" | follow-up " + tgl_panjang(date.fromisoformat(k2["followup"]))) if k2["followup"] else
            " | tanpa jadwal follow-up")
        return {"kontak": kontak_json(k2), "peringatan": [p for p in peringatan if p],
                "ringkasan": {"kode": kode(kid), "ubah": list(ubah)}}, t
    return jalankan_tulis(args, "catat", kerja)


def cmd_tunda(args):
    fu, cat = baca_tanggal(args.ke, hari_ini(), "depan")

    def kerja(conn, cfg):
        k = cari_kontak(conn, args.kontak)
        if k["tahap"] in ("selesai", "batal"):
            cat.append("Kontak berstatus %s; jadwal tetap disimpan (mis. untuk tawaran ulang)." % k["tahap"])
        conn.execute("UPDATE kontak SET followup=?, diubah=? WHERE id=?", (fu.isoformat(), stempel(), k["id"]))
        riwayat(conn, k["id"], "tunda", "follow-up dipindah dari %s ke %s" %
                (tgl_pendek(k["followup"]) if k["followup"] else "-", tgl_pendek(fu)))
        t = "Follow-up %s %s dipindah ke %s." % (kode(k["id"]), k["nama"], tgl_panjang(fu))
        return {"kontak": kontak_json(ambil(conn, k["id"])), "peringatan": cat,
                "ringkasan": {"kode": kode(k["id"]), "followup": fu.isoformat()}}, t
    return jalankan_tulis(args, "tunda", kerja)


def cmd_terkirim(args):
    acuan = hari_ini()

    def kerja(conn, cfg):
        k = cari_kontak(conn, args.kontak)
        kid, peringatan, ubah = k["id"], [], {}
        if k["tahap"] == "batal":
            raise Gagal("%s %s berstatus batal. Jika pelanggan dihubungi lagi, pindahkan tahapnya dulu: crm.py catat "
                        "--kontak %s --tahap dihubungi." % (kode(kid), k["nama"], kode(kid)))
        jenis, _ = susun_draf(k, cfg)
        if k["tahap"] == "baru":
            ubah.update(tahap="dihubungi", tgl_tahap=acuan.isoformat(), fu_ke=0)
            ke = 0
            peringatan.append("Tahap otomatis naik dari baru ke dihubungi.")
        else:
            ke = int(k["fu_ke"] or 0) + 1
            ubah["fu_ke"] = ke
        ubah["kontak_terakhir"] = acuan.isoformat()
        if args.berikutnya:
            if args.berikutnya.strip().lower() in ("tidak", "stop", "tidak ada", "-", "berhenti"):
                fu = None
            else:
                fu, cat = baca_tanggal(args.berikutnya, acuan, "depan")
                peringatan += cat
        elif k["tahap"] == "baru":
            fu = acuan + timedelta(days=2)
        elif k["tahap"] == "selesai":
            fu = None
        elif ke >= MAKS_FU:
            fu = None
            peringatan.append("Sudah %d pesan follow-up tanpa kemajuan (terakhir pesan pamit). Jadwal dihentikan. Jika "
                              "tetap tidak ada balasan, tandai batal: crm.py catat --kontak %s --tahap batal "
                              "--alasan \"tidak ada respon\"." % (ke, kode(kid)))
        else:
            fu = acuan + timedelta(days=JEDA_SETELAH_KIRIM.get(ke, 3))
        ubah["followup"] = fu.isoformat() if fu else None
        ubah["diubah"] = stempel()
        conn.execute("UPDATE kontak SET %s WHERE id=?" % ", ".join("%s=?" % c for c in ubah),
                     list(ubah.values()) + [kid])
        riwayat(conn, kid, "kirim", "Pesan %s dikirim pemilik%s" % (jenis or "-", "; follow-up berikutnya %s" %
                                                                     tgl_pendek(fu) if fu else ""))
        t = "Dicatat: pesan ke %s %s sudah dikirim. %s" % (
            kode(kid), k["nama"], ("Follow-up berikutnya: %s." % tgl_panjang(fu)) if fu else
            "Tidak ada jadwal follow-up berikutnya.")
        return {"kontak": kontak_json(ambil(conn, kid)), "peringatan": peringatan,
                "ringkasan": {"kode": kode(kid), "fu_ke": ubah.get("fu_ke", 0)}}, t
    return jalankan_tulis(args, "terkirim", kerja)


# --------------------------------------------------------------------------- perintah baca: daftar / lihat / draf
def _baca(args):
    return buka(path_db(args), baca_saja=True)


def baris_kontak(r, samarkan=False, acuan=None):
    bag = ["%s %s" % (kode(r["id"]), samar_nama(r["nama"]) if samarkan else r["nama"])]
    bag.append(r["sumber"])
    bag.append(LABEL_TAHAP[r["tahap"]] + ((" (%s)" % r["alasan_batal"]) if r["tahap"] == "batal" else ""))
    if r["nilai"] is not None:
        bag.append(rp(r["nilai"]))
    if r["kebutuhan"]:
        bag.append(r["kebutuhan"])
    if r["followup"] and acuan is not None:
        d = date.fromisoformat(r["followup"])
        sel = (d - acuan).days
        bag.append("FU %s%s" % (tgl_pendek(d, False), " (telat %d hari)" % -sel if sel < 0 else
                                 " (hari ini)" if sel == 0 else ""))
    bag.append(samar_wa(r["wa"]) if samarkan else tampil_wa(r["wa"]))
    return " | ".join(bag)


def cmd_daftar(args):
    conn = _baca(args)
    try:
        rows = conn.execute("SELECT * FROM kontak").fetchall()
    finally:
        conn.close()
    acuan = hari_ini()
    t = (args.tahap or "aktif").lower()
    if t == "aktif":
        rows = [r for r in rows if r["tahap"] in TAHAP_PANTAU]
    elif t == "terbuka":
        rows = [r for r in rows if r["tahap"] in TAHAP_TERBUKA]
    elif t != "semua":
        tn = norm_tahap(t)
        rows = [r for r in rows if r["tahap"] == tn]
    if args.label:
        lab = norm_label(args.label)
        rows = [r for r in rows if set(lab) <= set(norm_label(r["label"]))]
    if args.sumber:
        s, _ = norm_sumber(args.sumber)
        rows = [r for r in rows if r["sumber"].lower() == s.lower()]
    if args.cari:
        c = args.cari.lower()
        dig = re.sub(r"\D", "", c)
        rows = [r for r in rows if c in r["nama"].lower() or c in (r["kebutuhan"] or "").lower()
                or c in (r["label"] or "") or (len(dig) >= 4 and dig in (r["wa"] or "") or
                                               (len(dig) >= 4 and dig in ("0" + (r["wa"] or "")[2:])))]
    urut = args.urut or "followup"
    if urut == "followup":
        rows.sort(key=lambda r: (r["followup"] is None, r["followup"] or "", -(r["nilai"] or 0)))
    elif urut == "nilai":
        rows.sort(key=lambda r: -(r["nilai"] or 0))
    elif urut == "nama":
        rows.sort(key=lambda r: r["nama"].lower())
    else:
        rows.sort(key=lambda r: -r["id"])
    total = len(rows)
    rows = rows[:args.maks]
    nilai = sum(r["nilai"] or 0 for r in rows)
    judul = "DAFTAR KONTAK (%s%s%s%s): %d kontak" % (t, (", label " + args.label) if args.label else "",
                                                     (", sumber " + args.sumber) if args.sumber else "",
                                                     (", cari '" + args.cari + "'") if args.cari else "", total)
    isi = ["%d. %s" % (i, baris_kontak(r, args.samarkan, acuan)) for i, r in enumerate(rows, 1)]
    t = judul + "\n" + ("\n".join(isi) if isi else "(kosong)")
    if total > len(rows):
        t += "\n... dan %d lainnya (pakai --maks)." % (total - len(rows))
    if rows:
        t += "\nTotal nilai yang ditampilkan: %s" % rp(nilai)
    return {"ok": True, "mode": "baca", "jumlah": total, "kontak": [kontak_json(r, args.samarkan) for r in rows],
            "data_sensitif": not args.samarkan, "teks": t}, t


def cmd_lihat(args):
    conn = _baca(args)
    try:
        cfg = pengaturan(conn)
        k = cari_kontak(conn, args.kontak)
        riw = conn.execute("SELECT * FROM riwayat WHERE kontak_id=? ORDER BY waktu DESC, id DESC LIMIT ?",
                           (k["id"], args.maks)).fetchall()
    finally:
        conn.close()
    acuan = hari_ini()
    d = draf_json(k, cfg)
    t = ["%s %s" % (kode(k["id"]), k["nama"]),
         "WA: %s | Sumber: %s | Label: %s" % (tampil_wa(k["wa"]), k["sumber"], k["label"] or "-"),
         "Tahap: %s%s | Nilai: %s | Kebutuhan: %s" % (
             LABEL_TAHAP[k["tahap"]], (" (alasan: %s)" % k["alasan_batal"]) if k["alasan_batal"] else "",
             rp(k["nilai"]), k["kebutuhan"] or "-"),
         "Masuk: %s | Deal: %s | Kontak terakhir: %s | Follow-up: %s" % (
             tgl_pendek(k["tgl_masuk"]), tgl_pendek(k["tgl_deal"]) if k["tgl_deal"] else "-",
             tgl_pendek(k["kontak_terakhir"]) if k["kontak_terakhir"] else "-",
             (tgl_panjang(date.fromisoformat(k["followup"])) +
              (" (TERLAMBAT %d hari)" % (acuan - date.fromisoformat(k["followup"])).days
               if date.fromisoformat(k["followup"]) < acuan else "")) if k["followup"] else "-"),
         "Riwayat (terbaru dulu):"]
    t += ["- %s [%s] %s" % (r["waktu"][:16].rstrip(" 0:") if r["waktu"].endswith("00:00:00") else r["waktu"][:16],
                             r["jenis"], r["isi"]) for r in riw] or ["- (belum ada)"]
    if d.get("draf"):
        t += ["", "Draf berikutnya (%s), dikirim sendiri oleh pemilik:" % d["jenis"], d["draf"]]
        if d.get("tautan"):
            t.append(d["tautan"])
    teks = "\n".join(t)
    return {"ok": True, "mode": "baca", "kontak": kontak_json(k), "riwayat": [dict(r) for r in riw], "draf": d,
            "data_sensitif": True, "teks": teks}, teks


def cmd_draf(args):
    conn = _baca(args)
    try:
        cfg = pengaturan(conn)
        k = cari_kontak(conn, args.kontak)
    finally:
        conn.close()
    d = draf_json(k, cfg, pesan=args.pesan)
    if not d.get("draf"):
        raise Gagal(d["alasan"])
    t = "Draf untuk %s %s (%s) - periksa dulu, lalu kirim sendiri:\n%s" % (kode(k["id"]), k["nama"], d["jenis"],
                                                                         d["draf"])
    t += ("\nBuka tautan ini, periksa pesannya, lalu tekan Kirim:\n" + d["tautan"]) if d.get("tautan") else \
        "\n(" + d.get("catatan", "Tanpa tautan.") + ")"
    t += "\nSetelah terkirim, balas: \"terkirim %s\"." % kode(k["id"])
    d.update(ok=True, mode="baca", teks=t)
    return d, t


# --------------------------------------------------------------------------- hari-ini (pengingat harian)
def kelompok_followup(rows, acuan):
    terlambat, hari, besok, tanpa = [], [], [], []
    for r in rows:
        if r["tahap"] not in TAHAP_PANTAU:
            if r["followup"] and r["tahap"] == "selesai" and date.fromisoformat(r["followup"]) <= acuan:
                (hari if date.fromisoformat(r["followup"]) == acuan else terlambat).append(r)
            continue
        if not r["followup"]:
            if r["tahap"] in TAHAP_TERBUKA:
                tanpa.append(r)
            continue
        d = date.fromisoformat(r["followup"])
        if d < acuan:
            terlambat.append(r)
        elif d == acuan:
            hari.append(r)
        elif d == acuan + timedelta(days=1):
            besok.append(r)
    terlambat.sort(key=lambda r: (r["followup"], -(r["nilai"] or 0), r["id"]))
    for x in (hari, besok, tanpa):
        x.sort(key=lambda r: (-(r["nilai"] or 0), r["id"]))
    return terlambat, hari, besok, tanpa


def cmd_hari_ini(args):
    conn = _baca(args)
    try:
        cfg = pengaturan(conn)
        rows = conn.execute("SELECT * FROM kontak").fetchall()
        akhir = {r[0]: r for r in conn.execute(
            "SELECT kontak_id, waktu, isi FROM riwayat WHERE jenis='catatan' ORDER BY waktu, id")}
    finally:
        conn.close()
    acuan = hari_ini()
    terlambat, hari, besok, tanpa = kelompok_followup(rows, acuan)
    sam = args.samarkan
    nilai_perlu = sum(r["nilai"] or 0 for r in terlambat + hari)
    t = ["FOLLOW-UP CRM - %s (%s)" % (tgl_panjang(acuan), _JAM["zona"]),
         "Terlambat: %d | Hari ini: %d | Besok: %d | Belum dijadwalkan: %d" % (len(terlambat), len(hari),
                                                                               len(besok), len(tanpa))]
    if terlambat or hari:
        t.append("Nilai prospek yang perlu disapa: %s" % rp(nilai_perlu))

    def blok(judul, daftar, maks=None):
        if not daftar:
            return
        t.append("")
        t.append("%s (%d)" % (judul, len(daftar)))
        for i, r in enumerate(daftar[:maks] if maks else daftar, 1):
            t.append("%d. %s" % (i, baris_kontak(r, sam, acuan)))
            a = akhir.get(r["id"])
            if a and not sam:
                t.append("   Catatan terakhir %s: \"%s\"" % (tgl_pendek(a["waktu"][:10], False), bersih(a["isi"], 90)))
        if maks and len(daftar) > maks:
            t.append("... dan %d lainnya (crm.py daftar)." % (len(daftar) - maks))
    blok("TERLAMBAT", terlambat)
    blok("HARI INI", hari)
    blok("BESOK", besok, 10)
    blok("BELUM DIJADWALKAN", tanpa, 10)
    draf = []
    if not args.tanpa_draf:
        for r in (terlambat + hari)[:args.maks_draf]:
            d = draf_json(r, cfg, samarkan=sam)
            if d.get("draf"):
                draf.append(d)
        if draf:
            t.append("")
            t.append("DRAF PESAN (periksa, lalu kirim sendiri lewat tautan; bot tidak mengirim apa pun)")
            for d in draf:
                t.append("")
                t.append("%s %s [%s]:" % (d["kode"], d["nama"], d["jenis"]))
                t.append(d["draf"])
                if d.get("tautan"):
                    t.append(d["tautan"])
                elif sam:
                    t.append("(tautan disembunyikan karena mode samarkan)")
            sisa = len([r for r in terlambat + hari]) - len(draf)
            if sisa > 0:
                t.append("")
                t.append("%d draf lain: crm.py draf --kontak <kode>." % sisa)
    if not (terlambat or hari or besok or tanpa):
        t.append("")
        t.append("Tidak ada follow-up hari ini. Mantap!")
    t.append("")
    t.append("Balas misalnya: \"terkirim K0001\", \"Bu Rina deal 4,2 jt\", \"tunda K0002 ke Senin\", "
             "\"K0003 batal, kemahalan\".")
    teks = "\n".join(t)
    kj = lambda xs: [kontak_json(r, sam) for r in xs]  # noqa: E731
    return {"ok": True, "mode": "baca", "hari_ini": acuan.isoformat(), "zona": _JAM["zona"],
            "ringkasan": {"terlambat": len(terlambat), "hari_ini": len(hari), "besok": len(besok),
                          "belum_dijadwalkan": len(tanpa), "nilai_perlu_disapa": nilai_perlu},
            "terlambat": kj(terlambat), "hari_ini_daftar": kj(hari), "besok": kj(besok),
            "belum_dijadwalkan": kj(tanpa), "draf": draf, "data_sensitif": not sam, "teks": teks}, teks


# --------------------------------------------------------------------------- rekap
def periode_dari_args(args, acuan):
    if args.dari or args.sampai:
        if not (args.dari and args.sampai):
            raise Gagal("--dari dan --sampai harus diisi keduanya.")
        a, _ = baca_tanggal(args.dari, acuan, "bebas")
        b, _ = baca_tanggal(args.sampai, acuan, "bebas")
        if b < a:
            raise Gagal("--sampai lebih awal dari --dari.")
        return "rentang", a, b
    if args.tanggal:
        d, _ = baca_tanggal(args.tanggal, acuan, "lalu")
        return "harian", d, d
    if args.bulan:
        b = args.bulan.strip().lower()
        if b in ("ini", "bulan-ini"):
            return periode_nama("bulan-ini", acuan)
        if b in ("lalu", "bulan-lalu"):
            return periode_nama("bulan-lalu", acuan)
        m = re.fullmatch(r"(\d{4})-(\d{1,2})", b)
        if not m or not 1 <= int(m.group(2)) <= 12:
            raise Gagal("--bulan harus berformat YYYY-MM (mis. 2026-09), 'ini', atau 'lalu'.")
        a = date(int(m.group(1)), int(m.group(2)), 1)
        return "bulan %s %d" % (BULAN[a.month - 1], a.year), a, _tambah_bulan(a, 1) - timedelta(days=1)
    return periode_nama(args.periode or "bulan-ini", acuan)


def periode_nama(p, acuan):
    p = p.lower()
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
        return "semua waktu", date(1970, 1, 1), date(2999, 12, 31)
    raise Gagal("Periode '%s' tidak dikenal. Pilihan: hari-ini, kemarin, minggu-ini, minggu-lalu, bulan-ini, "
                "bulan-lalu, tahun-ini, semua (atau --dari/--sampai, --bulan YYYY-MM, --tanggal)." % p)


RUMUS = {
    "posisi": "Posisi saat ini = jumlah kontak & jumlah nilai potensi per tahap untuk SEMUA kontak (bukan hanya "
              "periode). Pipeline terbuka = baru + dihubungi + ditawar.",
    "lead_masuk": "Lead masuk = kontak dengan tanggal masuk di dalam periode.",
    "deal_baru": "Deal baru = kontak yang pertama kali mencapai deal (atau langsung selesai) di dalam periode; nilai "
                 "= jumlah kolom nilai kontak itu (kontak tanpa nilai dihitung jumlahnya, nilainya tidak).",
    "konversi": "Konversi = lead masuk periode yang kini deal/selesai / lead masuk periode x 100%, dihitung pecahan "
                "persis lalu dibulatkan 1 desimal (0,05 ke atas).",
    "win_rate": "Win rate = (deal/selesai) / (deal/selesai + batal) dari lead masuk periode yang sudah diputuskan.",
    "rata_nilai": "Rata-rata nilai deal = jumlah nilai deal baru / jumlah deal baru yang bernilai, dibulatkan ke "
                  "rupiah terdekat.",
    "rata_hari": "Lama closing = rata-rata (tanggal deal - tanggal masuk) dalam hari, deal baru periode ini, 1 desimal.",
    "sumber_terbaik": "Sumber terbaik = sumber dengan nilai deal terbesar dari lead masuk periode; seri -> konversi "
                      "lebih tinggi -> lead lebih banyak.",
}


def hitung_rekap(rows, a, b, acuan):
    def dalam(x):
        return x is not None and a.isoformat() <= x[:10] <= b.isoformat()
    posisi = {t: {"jumlah": 0, "nilai": 0} for t in TAHAP}
    for r in rows:
        posisi[r["tahap"]]["jumlah"] += 1
        posisi[r["tahap"]]["nilai"] += r["nilai"] or 0
    terbuka = {"jumlah": sum(posisi[t]["jumlah"] for t in TAHAP_TERBUKA),
               "nilai": sum(posisi[t]["nilai"] for t in TAHAP_TERBUKA)}
    kohort = [r for r in rows if dalam(r["tgl_masuk"])]
    k_menang = [r for r in kohort if r["tahap"] in TAHAP_MENANG]
    k_batal = [r for r in kohort if r["tahap"] == "batal"]
    k_jalan = [r for r in kohort if r["tahap"] in TAHAP_TERBUKA]
    deal_baru = [r for r in rows if r["tahap"] in TAHAP_MENANG and dalam(r["tgl_deal"])]
    bernilai = [r for r in deal_baru if r["nilai"] is not None]
    nilai_deal = sum(r["nilai"] for r in bernilai)
    rata_nilai = bulat(Fraction(nilai_deal, len(bernilai))) if bernilai else None
    lama = [(date.fromisoformat(r["tgl_deal"]) - date.fromisoformat(r["tgl_masuk"])).days for r in deal_baru]
    rata_hari = None
    if lama:
        f = Fraction(sum(lama), len(lama))
        rata_hari = float((Decimal(f.numerator) / Decimal(f.denominator)).quantize(Decimal("0.1"),
                                                                                   rounding=ROUND_HALF_UP))
    batal_periode = [r for r in rows if r["tahap"] == "batal" and dalam(r["tgl_batal"])]
    konv, konv_t = persen(len(k_menang), len(kohort))
    win, win_t = persen(len(k_menang), len(k_menang) + len(k_batal))
    per_sumber = {}
    for r in kohort:
        s = per_sumber.setdefault(r["sumber"], {"sumber": r["sumber"], "lead": 0, "deal": 0, "batal": 0,
                                                "nilai_deal": 0})
        s["lead"] += 1
        if r["tahap"] in TAHAP_MENANG:
            s["deal"] += 1
            s["nilai_deal"] += r["nilai"] or 0
        elif r["tahap"] == "batal":
            s["batal"] += 1
    sumber = []
    for s in per_sumber.values():
        s["konversi_persen"], s["konversi_teks"] = persen(s["deal"], s["lead"])
        sumber.append(s)
    sumber.sort(key=lambda s: (-s["nilai_deal"], -(Fraction(s["deal"], s["lead"])), -s["lead"], s["sumber"]))
    terbaik = None
    if sumber and sumber[0]["deal"] > 0:
        terbaik = dict(sumber[0], sampel_kecil=sumber[0]["lead"] < 5)
    alasan = {}
    for r in batal_periode:
        alasan[r["alasan_batal"] or "tanpa alasan"] = alasan.get(r["alasan_batal"] or "tanpa alasan", 0) + 1
    alasan_l = [{"alasan": k, "jumlah": v} for k, v in sorted(alasan.items(), key=lambda x: (-x[1], x[0]))]
    terlambat, hari, besok, tanpa = kelompok_followup(rows, acuan)
    return {
        "posisi": dict(posisi, pipeline_terbuka=terbuka, total_kontak=len(rows)),
        "periode_ini": {
            "lead_masuk": len(kohort),
            "deal_baru": {"jumlah": len(deal_baru), "nilai": nilai_deal, "tanpa_nilai": len(deal_baru) - len(bernilai),
                          "rata_nilai": rata_nilai, "rata_hari_closing": rata_hari},
            "batal": len(batal_periode),
            "kohort": {"lead": len(kohort), "deal_atau_selesai": len(k_menang), "batal": len(k_batal),
                       "masih_berjalan": len(k_jalan)},
            "konversi_persen": konv, "konversi_teks": konv_t, "win_rate_persen": win, "win_rate_teks": win_t,
        },
        "sumber": sumber, "sumber_terbaik": terbaik, "alasan_batal": alasan_l,
        "followup": {"terlambat": len(terlambat), "hari_ini": len(hari), "besok": len(besok),
                     "belum_dijadwalkan": len(tanpa),
                     "nilai_terlambat_dan_hari_ini": sum(r["nilai"] or 0 for r in terlambat + hari)},
    }


def cmd_rekap(args):
    conn = _baca(args)
    try:
        rows = conn.execute("SELECT * FROM kontak").fetchall()
        cfg = pengaturan(conn)
    finally:
        conn.close()
    acuan = hari_ini()
    nama_p, a, b = periode_dari_args(args, acuan)
    h = hitung_rekap(rows, a, b, acuan)
    pi, pos = h["periode_ini"], h["posisi"]
    rentang = "semua data" if nama_p == "semua waktu" else (
        tgl_pendek(a) if a == b else "%s - %s" % (tgl_pendek(a), tgl_pendek(b)))
    t = ["REKAP CRM %s%s (%s)" % ((cfg["nama_usaha"] + " - ") if cfg["nama_usaha"] else "", nama_p, rentang),
         "Data per %s %s" % (tgl_panjang(acuan), _JAM["zona"]), "",
         "POSISI SAAT INI (semua kontak)"]
    for tp in TAHAP:
        t.append("- %-10s: %3d kontak%s" % (LABEL_TAHAP[tp], pos[tp]["jumlah"],
                                            (" | " + rp(pos[tp]["nilai"])) if tp != "batal" else ""))
    t.append("Pipeline terbuka (baru+dihubungi+ditawar): %d kontak, %s" % (pos["pipeline_terbuka"]["jumlah"],
                                                                          rp(pos["pipeline_terbuka"]["nilai"])))
    db_ = pi["deal_baru"]
    t += ["", "PERIODE %s" % nama_p.upper(), "Lead masuk: %d" % pi["lead_masuk"],
          "Deal baru: %d senilai %s%s" % (db_["jumlah"], rp(db_["nilai"]),
                                          (" (%d deal belum diisi nilainya)" % db_["tanpa_nilai"])
                                          if db_["tanpa_nilai"] else "")]
    if db_["rata_nilai"] is not None:
        t.append("Rata-rata nilai deal: %s | Rata-rata lama closing: %s hari" %
                 (rp(db_["rata_nilai"]), str(db_["rata_hari_closing"]).replace(".", ",")))
    t.append("Batal: %d" % pi["batal"])
    ko = pi["kohort"]
    t.append("Konversi lead periode ini: %d dari %d = %s (%d masih berjalan, %d batal)" %
             (ko["deal_atau_selesai"], ko["lead"], pi["konversi_teks"], ko["masih_berjalan"], ko["batal"]))
    t.append("Win rate (yang sudah diputuskan): %d dari %d = %s" % (
        ko["deal_atau_selesai"], ko["deal_atau_selesai"] + ko["batal"], pi["win_rate_teks"]))
    if h["sumber"]:
        t += ["", "SUMBER LEAD (lead masuk periode ini)"]
        for i, s in enumerate(h["sumber"], 1):
            t.append("%d. %s: %d lead, %d deal (%s), %s" % (i, s["sumber"], s["lead"], s["deal"], s["konversi_teks"],
                                                            rp(s["nilai_deal"])))
        tb = h["sumber_terbaik"]
        if tb:
            t.append("Sumber terbaik: %s (nilai deal terbesar)%s" % (
                tb["sumber"], ". Sampel kecil (<5 lead), jadikan petunjuk saja." if tb["sampel_kecil"] else "."))
        else:
            t.append("Sumber terbaik: belum bisa ditentukan (belum ada deal dari lead periode ini).")
    if h["alasan_batal"]:
        t += ["", "ALASAN BATAL: " + ", ".join("%s (%d)" % (x["alasan"], x["jumlah"]) for x in h["alasan_batal"])]
    f = h["followup"]
    t += ["", "FOLLOW-UP SAAT INI: terlambat %d, hari ini %d, besok %d, belum dijadwalkan %d" %
          (f["terlambat"], f["hari_ini"], f["besok"], f["belum_dijadwalkan"])]
    if f["terlambat"] or f["hari_ini"]:
        t.append("Ketik \"follow-up hari ini\" untuk daftar & draf pesannya.")
    if pi["lead_masuk"] and ko["masih_berjalan"] and b >= acuan - timedelta(days=14):
        t.append("Catatan: periode ini masih baru; konversi akan naik bila lead yang masih berjalan jadi deal.")
    if args.rumus:
        t += ["", "RUMUS"] + ["- " + v for v in RUMUS.values()]
    else:
        t += ["", "Rumus perhitungan: tambahkan --rumus."]
    teks = "\n".join(t)
    out = {"ok": True, "mode": "baca", "aplikasi": APLIKASI, "versi": VERSI, "skema_json": SKEMA_JSON_REKAP,
           "zona": _JAM["zona"], "hari_ini": acuan.isoformat(),
           "periode": {"nama": nama_p, "dari": a.isoformat(), "sampai": b.isoformat()}}
    out.update(h)
    out.update(rumus=RUMUS, teks=teks, data_sensitif=False)
    return out, teks


# --------------------------------------------------------------------------- duplikat & gabung & hapus
def cmd_cek_duplikat(args):
    conn = _baca(args)
    try:
        rows = conn.execute("SELECT * FROM kontak ORDER BY id").fetchall()
    finally:
        conn.close()
    per_wa, per_nama = {}, {}
    for r in rows:
        if r["wa"]:
            per_wa.setdefault(r["wa"], []).append(r)
        kn = kunci_nama(r["nama"])
        if kn:
            per_nama.setdefault(kn, []).append(r)
    grup_wa = [g for g in per_wa.values() if len(g) > 1]
    sudah = {frozenset(r["id"] for r in g) for g in grup_wa}
    grup_nama = [g for g in per_nama.values() if len(g) > 1 and len({r["wa"] for r in g}) > 1
                 and frozenset(r["id"] for r in g) not in sudah]
    t = ["CEK DUPLIKAT: %d kontak diperiksa" % len(rows)]
    if grup_wa:
        t.append("")
        t.append("NOMOR SAMA (hampir pasti orang yang sama) - %d grup:" % len(grup_wa))
        for g in grup_wa:
            t.append("- %s: %s" % (samar_wa(g[0]["wa"]) if args.samarkan else tampil_wa(g[0]["wa"]),
                                   "; ".join("%s %s (%s)" % (kode(r["id"]), r["nama"], r["tahap"]) for r in g)))
            t.append("  Gabungkan: crm.py gabung --dari %s --ke %s" % (kode(g[-1]["id"]), kode(g[0]["id"])))
    if grup_nama:
        t.append("")
        t.append("NAMA SAMA, NOMOR BERBEDA (periksa dulu, bisa jadi orang berbeda) - %d grup:" % len(grup_nama))
        for g in grup_nama:
            t.append("- " + "; ".join("%s %s %s (%s)" % (kode(r["id"]), r["nama"], samar_wa(r["wa"]), r["tahap"])
                                      for r in g))
    if not grup_wa and not grup_nama:
        t.append("Tidak ada duplikat.")
    teks = "\n".join(t)
    return {"ok": True, "mode": "baca",
            "nomor_sama": [[pilihan_json(r) for r in g] for g in grup_wa],
            "nama_sama": [[pilihan_json(r) for r in g] for g in grup_nama], "teks": teks}, teks


def cmd_gabung(args):
    def kerja(conn, cfg):
        dari = cari_kontak(conn, args.dari)
        ke = cari_kontak(conn, args.ke)
        if dari["id"] == ke["id"]:
            raise Gagal("--dari dan --ke menunjuk kontak yang sama.")
        isi = {}
        for c in ("wa", "sapaan", "nilai", "kebutuhan", "followup", "kontak_terakhir"):
            if (ke[c] is None or ke[c] == "") and dari[c] not in (None, ""):
                isi[c] = dari[c]
        if ke["sumber"] == "Tidak diketahui" and dari["sumber"] != "Tidak diketahui":
            isi["sumber"] = dari["sumber"]
        lab = norm_label(ke["label"]) + [x for x in norm_label(dari["label"]) if x not in norm_label(ke["label"])]
        if ", ".join(lab) != ke["label"]:
            isi["label"] = ", ".join(lab)
        if dari["tgl_masuk"] < ke["tgl_masuk"]:
            isi["tgl_masuk"] = dari["tgl_masuk"]
        n_riw = conn.execute("SELECT COUNT(*) FROM riwayat WHERE kontak_id=?", (dari["id"],)).fetchone()[0]
        peringatan = []
        if dari["tahap"] != ke["tahap"]:
            peringatan.append("Tahap berbeda (%s: %s, %s: %s); tahap %s dipakai. Ubah dengan crm.py catat bila perlu."
                              % (kode(dari["id"]), dari["tahap"], kode(ke["id"]), ke["tahap"], kode(ke["id"])))
        if dari["wa"] and ke["wa"] and dari["wa"] != ke["wa"]:
            peringatan.append("Nomor %s dari %s tidak disimpan (kontak tujuan sudah punya nomor); dicatat di riwayat."
                              % (tampil_wa(dari["wa"]), kode(dari["id"])))
        if isi:
            isi["diubah"] = stempel()
            conn.execute("UPDATE kontak SET %s WHERE id=?" % ", ".join("%s=?" % c for c in isi),
                         list(isi.values()) + [ke["id"]])
        conn.execute("UPDATE riwayat SET kontak_id=? WHERE kontak_id=?", (ke["id"], dari["id"]))
        riwayat(conn, ke["id"], "gabung", "Digabung dari %s %s (%s, tahap %s)" % (
            kode(dari["id"]), dari["nama"], tampil_wa(dari["wa"]), dari["tahap"]))
        conn.execute("DELETE FROM kontak WHERE id=?", (dari["id"],))
        t = ("Gabung %s %s -> %s %s: %d riwayat dipindah; kolom kosong yang diisi: %s. %s dihapus." %
             (kode(dari["id"]), dari["nama"], kode(ke["id"]), ke["nama"], n_riw,
              ", ".join(c for c in isi if c != "diubah") or "-", kode(dari["id"])))
        return {"dari": kode(dari["id"]), "ke": kode(ke["id"]), "peringatan": peringatan,
                "ringkasan": {"dari": kode(dari["id"]), "ke": kode(ke["id"])}}, t
    return jalankan_tulis(args, "gabung", kerja, besar=True, label_backup="gabung")


def cmd_hapus(args):
    def kerja(conn, cfg):
        k = cari_kontak(conn, args.kontak)
        n = conn.execute("SELECT COUNT(*) FROM riwayat WHERE kontak_id=?", (k["id"],)).fetchone()[0]
        conn.execute("DELETE FROM riwayat WHERE kontak_id=?", (k["id"],))
        conn.execute("DELETE FROM kontak WHERE id=?", (k["id"],))
        t = ("Hapus permanen %s %s (%s) beserta %d riwayat.\nCatatan privasi: file cadangan lama di %s masih memuat "
             "data ini; hapus file cadangan lama bila pelanggan meminta datanya dihapus total." %
             (kode(k["id"]), k["nama"], tampil_wa(k["wa"]), n, folder_backup(path_db(args))))
        return {"kode": kode(k["id"]), "ringkasan": {"hapus": kode(k["id"])}}, t
    return jalankan_tulis(args, "hapus", kerja, besar=True, label_backup="hapus")


# --------------------------------------------------------------------------- impor / ekspor
def cmd_impor(args):
    rows, peringatan_file = baca_csv(args.file)
    header, isi = rows[0], rows[1:]
    peta, abaikan = petakan_kolom(header)
    if "nama" not in peta:
        raise Gagal("Kolom nama tidak ditemukan. Header file: %s. Beri judul kolom 'nama' (dan 'no wa', 'sumber', "
                    "'tahap', 'nilai', 'kebutuhan', 'label' bila ada). Contoh: templates/kontak-contoh.csv." %
                    ", ".join(header))
    if len(isi) > 5000:
        raise Gagal("File berisi %d baris; maksimal 5.000 per impor. Pecah menjadi beberapa file." % len(isi))
    acuan = hari_ini()
    sumber_def, _ = norm_sumber(args.sumber_default) if args.sumber_default else ("Tidak diketahui", False)
    tahap_def = norm_tahap(args.tahap_default) if args.tahap_default else "baru"

    def ambil_sel(r, kol):
        i = peta.get(kol)
        return buang_pelindung(r[i]).strip() if i is not None and i < len(r) else ""

    def kerja(conn, cfg):
        ada_wa = {r["wa"]: r for r in conn.execute("SELECT id, nama, wa, tahap FROM kontak WHERE wa IS NOT NULL")}
        di_file, masuk, dup, rusak, peringatan = {}, [], [], [], list(peringatan_file)
        sumber_baru = set()
        for no, r in enumerate(isi, start=2):
            try:
                nama = bersih(ambil_sel(r, "nama"), 80)
                if not nama:
                    raise Gagal("nama kosong")
                if re.fullmatch(r"[\d\s+().-]{8,}", nama):
                    raise Gagal("kolom nama berisi nomor")
                wa, pw = (normalisasi_wa(ambil_sel(r, "wa")) if ambil_sel(r, "wa") else (None, []))
                sumber, baru = norm_sumber(ambil_sel(r, "sumber")) if ambil_sel(r, "sumber") else (sumber_def, False)
                if baru:
                    sumber_baru.add(sumber)
                tahap = norm_tahap(ambil_sel(r, "tahap")) if ambil_sel(r, "tahap") else tahap_def
                nilai = nilai_opsional(ambil_sel(r, "nilai")) if ambil_sel(r, "nilai") else None
                masuk_tgl = baca_tanggal(ambil_sel(r, "tgl_masuk"), acuan, "lalu")[0] if ambil_sel(r, "tgl_masuk") \
                    else acuan
                alasan = ambil_sel(r, "alasan_batal")
                if tahap == "batal" and not alasan:
                    alasan = "tidak dicatat (impor)"
                if ambil_sel(r, "followup"):
                    fu = baca_tanggal(ambil_sel(r, "followup"), acuan, "bebas")[0]
                else:
                    fu = followup_default(tahap, acuan)[0]
            except Gagal as e:
                rusak.append({"baris": no, "alasan": e.pesan.rstrip(".")})
                continue
            if wa and wa in ada_wa:
                x = ada_wa[wa]
                dup.append({"baris": no, "nama": nama, "sudah_ada": "%s %s" % (kode(x["id"]), x["nama"])})
                continue
            if wa and wa in di_file:
                dup.append({"baris": no, "nama": nama, "sudah_ada": "baris %d di file ini" % di_file[wa]})
                continue
            if wa:
                di_file[wa] = no
            now = stempel()
            cur = conn.execute(
                "INSERT INTO kontak(nama, sapaan, wa, sumber, label, tahap, nilai, kebutuhan, followup, fu_ke, "
                "alasan_batal, tgl_masuk, tgl_tahap, tgl_deal, tgl_batal, kontak_terakhir, dibuat, diubah) "
                "VALUES (?,?,?,?,?,?,?,?,?,0,?,?,?,?,?,?,?,?)",
                (nama, bersih(ambil_sel(r, "sapaan"), 20) or None, wa, sumber,
                 ", ".join(norm_label(ambil_sel(r, "label"))), tahap, nilai, bersih(ambil_sel(r, "kebutuhan"), 120),
                 fu.isoformat() if fu and tahap in TAHAP_PANTAU else None,
                 norm_alasan(alasan) if tahap == "batal" else None, masuk_tgl.isoformat(), acuan.isoformat(),
                 masuk_tgl.isoformat() if tahap in TAHAP_MENANG else None,
                 acuan.isoformat() if tahap == "batal" else None, None, now, now))
            riwayat(conn, cur.lastrowid, "masuk", "Diimpor dari %s baris %d" % (Path(args.file).name, no))
            if ambil_sel(r, "catatan"):
                riwayat(conn, cur.lastrowid, "catatan", ambil_sel(r, "catatan"))
            masuk.append({"baris": no, "kode": kode(cur.lastrowid), "nama": nama, "wa": samar_wa(wa),
                          "tahap": tahap, "sumber": sumber})
            for p in pw:
                peringatan.append("Baris %d: %s" % (no, p))
        if sumber_baru:
            peringatan.append("Sumber di luar daftar baku disimpan apa adanya: %s." % ", ".join(sorted(sumber_baru)))
        if abaikan:
            peringatan.append("Kolom diabaikan: %s." % ", ".join(abaikan))
        t = ["Impor %s: %d baris dibaca." % (Path(args.file).name, len(isi)),
             "Kolom dikenali: %s" % ", ".join("%s <- '%s'" % (k, header[i]) for k, i in peta.items()),
             "Kontak baru: %d | Duplikat dilewati: %d | Baris bermasalah dilewati: %d" % (len(masuk), len(dup),
                                                                                        len(rusak))]
        for x in masuk[:10]:
            t.append("+ %s %s | %s | %s | %s" % (x["kode"] if args.ya else "(baru)", x["nama"], x["wa"], x["tahap"],
                                                 x["sumber"]))
        if len(masuk) > 10:
            t.append("+ ... dan %d lainnya" % (len(masuk) - 10))
        for x in dup[:10]:
            t.append("= baris %d %s: sudah ada (%s)" % (x["baris"], x["nama"], x["sudah_ada"]))
        for x in rusak[:20]:
            t.append("! baris %d: %s" % (x["baris"], x["alasan"]))
        if len(rusak) > 20:
            t.append("! ... dan %d baris bermasalah lainnya (lihat JSON)" % (len(rusak) - 20))
        return {"baru": masuk, "duplikat": dup, "rusak": rusak, "peringatan": peringatan,
                "ringkasan": {"file": Path(args.file).name, "baru": len(masuk), "duplikat": len(dup),
                              "rusak": len(rusak)}}, "\n".join(t)
    return jalankan_tulis(args, "impor", kerja, besar=True, label_backup="impor")


def cmd_ekspor(args):
    conn = _baca(args)
    try:
        rows = conn.execute("SELECT * FROM kontak ORDER BY id").fetchall()
    finally:
        conn.close()
    t = (args.tahap or "semua").lower()
    if t == "aktif":
        rows = [r for r in rows if r["tahap"] in TAHAP_PANTAU]
    elif t != "semua":
        tn = norm_tahap(t)
        rows = [r for r in rows if r["tahap"] == tn]
    sam = args.samarkan
    if args.format == "pengingat":
        rows = [r for r in rows if r["tahap"] in TAHAP_PANTAU and r["followup"]]
        data = [["prospek", re.sub(r"\d{6,}", "", r["nama"]).strip() or kode(r["id"]), r["followup"],
                 r["nilai"] if r["nilai"] is not None else "", r["kebutuhan"] or "", kode(r["id"])] for r in rows]
        p = tulis_csv(args.csv, ["jenis", "nama", "tanggal", "nominal", "perihal", "kode_crm"], data, args.timpa)
        perintah = [["tambah", "--jenis", "prospek", "--nama", d[1], "--tanggal", d[2]] +
                    (["--nominal", str(d[3])] if d[3] != "" else []) + (["--perihal", d[4]] if d[4] else [])
                    for d in data]
        teks = ("Ekspor %d prospek aktif ke %s (format pengingat-follow-up, TANPA nomor HP).\nDi skill "
                "pengingat-follow-up, tambahkan per baris dengan perintah 'tambah' (lihat 'perintah_pengingat' di "
                "JSON). Jangan jalankan jadwal kedua skill untuk prospek yang sama, nanti pengingatnya dobel." %
                (len(data), p))
        return {"ok": True, "mode": "baca", "file": p, "jumlah": len(data), "perintah_pengingat": perintah,
                "teks": teks}, teks
    header = ["kode", "nama", "no_wa", "link_wa", "sumber", "label", "tahap", "nilai", "kebutuhan", "followup",
              "alasan_batal", "tgl_masuk", "tgl_deal", "kontak_terakhir"]
    data = []
    for r in rows:
        data.append([kode(r["id"]), samar_nama(r["nama"]) if sam else r["nama"],
                     samar_wa(r["wa"]) if sam else tampil_wa(r["wa"]) if r["wa"] else "",
                     "" if sam or not r["wa"] else "https://wa.me/" + r["wa"], r["sumber"], r["label"], r["tahap"],
                     r["nilai"] if r["nilai"] is not None else "", r["kebutuhan"], r["followup"] or "",
                     r["alasan_batal"] or "", r["tgl_masuk"], r["tgl_deal"] or "", r["kontak_terakhir"] or ""])
    p = tulis_csv(args.csv, header, data, args.timpa)
    teks = "Ekspor %d kontak ke %s (pemisah ';', UTF-8, aman dibuka di Excel)." % (len(data), p)
    if not sam:
        teks += "\nFile ini berisi nomor HP pelanggan (data pribadi). " + DISCLAIMER_PRIVASI
    return {"ok": True, "mode": "baca", "file": p, "jumlah": len(data), "data_sensitif": not sam, "teks": teks}, teks


# --------------------------------------------------------------------------- backup & restore
def cmd_backup(args):
    db = path_db(args)
    if args.daftar:
        fol = folder_backup(db)
        bks = sorted(fol.glob("crm-*.db")) if fol.is_dir() else []
        t = "Cadangan di %s:\n%s" % (fol, "\n".join("- " + b.name for b in bks[-30:]) if bks else "(belum ada)")
        return {"ok": True, "mode": "baca", "backup": [str(b) for b in bks], "teks": t}, t
    conn = buka(db, baca_saja=True)
    conn.close()
    b = buat_backup(db, re.sub(r"[^\w-]", "", args.label or "manual") or "manual")
    t = "Cadangan dibuat: %s" % b
    return {"ok": True, "mode": "tersimpan", "backup": b, "teks": t}, t


def cmd_restore(args):
    db = path_db(args)
    src = Path(args.dari).expanduser()
    if not src.is_file():
        raise Gagal("File cadangan %s tidak ada. Lihat daftar: crm.py backup --daftar" % src)
    c = buka(src, baca_saja=True)
    try:
        n = c.execute("SELECT COUNT(*) FROM kontak").fetchone()[0]
        cek = c.execute("PRAGMA quick_check").fetchone()[0]
    finally:
        c.close()
    if cek != "ok":
        raise Gagal("File cadangan %s juga bermasalah (%s). Pilih cadangan lain." % (src.name, cek))
    if not args.ya:
        t = ("PRATINJAU (belum disimpan):\nDatabase %s akan diganti dengan cadangan %s (%d kontak). Database saat ini "
             "dicadangkan dulu bila masih bisa dibaca.\n\nLanjut? Jalankan perintah yang sama + --ya setelah pengguna "
             "setuju." % (db, src.name, n))
        return {"ok": True, "mode": "pratinjau", "perlu_konfirmasi": True, "teks": t}, t
    bk = None
    if db.is_file():
        fol = folder_backup(db)
        fol.mkdir(parents=True, exist_ok=True)
        bk = fol / ("crm-%s-sebelum-restore.db" % kini().strftime("%Y%m%d-%H%M%S"))
        bk.write_bytes(db.read_bytes())  # salin mentah: tetap bisa walau database rusak
    db.parent.mkdir(parents=True, exist_ok=True)
    s = sqlite3.connect(str(src))
    d = sqlite3.connect(str(db), timeout=_timeout())
    try:
        s.backup(d)
    finally:
        d.close()
        s.close()
    t = "TERSIMPAN. Database dipulihkan dari %s (%d kontak).%s" % (src.name, n, (" Salinan database sebelumnya: %s"
                                                                                % bk) if bk else "")
    return {"ok": True, "mode": "tersimpan", "backup": str(bk) if bk else None, "teks": t}, t


# --------------------------------------------------------------------------- CLI
class ParserID(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        print("GAGAL: perintah tidak lengkap/salah: %s. Lihat --help." % message, file=sys.stderr)
        sys.exit(2)


def buat_parser():
    umum = argparse.ArgumentParser(add_help=False)
    umum.add_argument("--db", help="File database (default ~/KomunitechData/crm/crm.db; ENV KOMUNITECH_CRM_DB)")
    umum.add_argument("--json", action="store_true", help="Output JSON (untuk agent/laporan-harian-usaha)")
    umum.add_argument("--hari-ini", help=argparse.SUPPRESS)
    tulis = argparse.ArgumentParser(add_help=False)
    tulis.add_argument("--ya", action="store_true", help="Simpan perubahan besar (tanpa ini hanya pratinjau)")
    sam = argparse.ArgumentParser(add_help=False)
    sam.add_argument("--samarkan", action="store_true", help="Samarkan nomor & nama, tanpa tautan wa.me")

    p = ParserID(prog="crm.py", description="CRM lokal chat WA -> deal (crm-wa %s)" % VERSI)
    p.add_argument("--versi", action="version", version="crm-wa " + VERSI)
    sub = p.add_subparsers(dest="perintah", parser_class=ParserID)
    sub.required = True

    s = sub.add_parser("init", parents=[umum, tulis], help="Buat database baru")
    s.add_argument("--nama-usaha")
    s.add_argument("--pengirim", help="Nama yang dipakai di draf pesan (mis. Sari)")
    s.add_argument("--sapaan", help="Sapaan default (Kak/Bapak/Ibu/-). Default Kak")
    s.add_argument("--zona", help="WIB (default), WITA, WIT")
    s.set_defaults(fungsi=cmd_init)
    s = sub.add_parser("info", parents=[umum], help="Lokasi database, jumlah kontak, cadangan")
    s.set_defaults(fungsi=cmd_info)
    s = sub.add_parser("atur", parents=[umum, tulis], help="Ubah pengaturan")
    s.add_argument("--nama-usaha")
    s.add_argument("--pengirim")
    s.add_argument("--sapaan")
    s.add_argument("--zona")
    s.set_defaults(fungsi=cmd_atur)

    s = sub.add_parser("tambah", parents=[umum, tulis], help="Tambah kontak/lead")
    s.add_argument("--nama", required=True)
    s.add_argument("--wa", help="Nomor WA (0812..., +62..., 62...)")
    s.add_argument("--sumber", help="ig, tiktok, shopee, referensi, walk-in, ...")
    s.add_argument("--label", help="Dipisah koma, mis. 'reseller, jakarta'")
    s.add_argument("--tahap", help="baru (default), dihubungi, ditawar, deal, selesai, batal")
    s.add_argument("--nilai", help="Nilai potensi, mis. 450rb, 4,5 jt")
    s.add_argument("--kebutuhan", help="Produk/jasa yang diminati")
    s.add_argument("--followup", help="Jadwal follow-up (besok, Jumat, 3/10, ...)")
    s.add_argument("--catatan", help="Catatan pertama (pribadi, tidak masuk draf)")
    s.add_argument("--masuk", help="Tanggal lead masuk (default hari ini)")
    s.add_argument("--sapaan", help="Sapaan khusus kontak ini (Bu/Pak/Kak/-)")
    s.add_argument("--alasan", help="Wajib bila tahap batal")
    s.add_argument("--izinkan-duplikat", action="store_true")
    s.set_defaults(fungsi=cmd_tambah)

    s = sub.add_parser("ubah", parents=[umum, tulis], help="Ubah data kontak")
    s.add_argument("--kontak", required=True, help="Kode (K0003), nama, atau nomor WA")
    for o in ("--nama", "--wa", "--sumber", "--label", "--tambah-label", "--hapus-label", "--nilai", "--kebutuhan",
              "--sapaan", "--masuk"):
        s.add_argument(o)
    s.add_argument("--izinkan-duplikat", action="store_true")
    s.set_defaults(fungsi=cmd_ubah)

    s = sub.add_parser("catat", parents=[umum, tulis], help="Catat interaksi / pindah tahap / nilai / follow-up")
    s.add_argument("--kontak", required=True)
    s.add_argument("--isi", help="Isi catatan interaksi (pribadi, tidak masuk draf)")
    s.add_argument("--tahap")
    s.add_argument("--alasan", help="Alasan batal")
    s.add_argument("--nilai")
    s.add_argument("--followup")
    s.add_argument("--tanpa-followup", action="store_true", help="Hapus jadwal follow-up")
    s.add_argument("--tanggal", help="Tanggal interaksi (default hari ini)")
    s.set_defaults(fungsi=cmd_catat)

    s = sub.add_parser("tunda", parents=[umum, tulis], help="Pindah jadwal follow-up")
    s.add_argument("--kontak", required=True)
    s.add_argument("--ke", required=True)
    s.set_defaults(fungsi=cmd_tunda)

    s = sub.add_parser("terkirim", parents=[umum, tulis], help="Catat bahwa pemilik sudah mengirim pesan")
    s.add_argument("--kontak", required=True)
    s.add_argument("--berikutnya", help="Jadwal follow-up berikutnya (default otomatis; 'stop' = tanpa jadwal)")
    s.set_defaults(fungsi=cmd_terkirim)

    s = sub.add_parser("daftar", parents=[umum, sam], help="Daftar kontak")
    s.add_argument("--tahap", help="aktif (default), terbuka, semua, atau nama tahap")
    s.add_argument("--label")
    s.add_argument("--sumber")
    s.add_argument("--cari")
    s.add_argument("--urut", choices=["followup", "nilai", "nama", "terbaru"])
    s.add_argument("--maks", type=int, default=50)
    s.set_defaults(fungsi=cmd_daftar)

    s = sub.add_parser("lihat", parents=[umum], help="Detail + riwayat satu kontak")
    s.add_argument("--kontak", required=True)
    s.add_argument("--maks", type=int, default=20)
    s.set_defaults(fungsi=cmd_lihat)

    s = sub.add_parser("draf", parents=[umum], help="Draf pesan + tautan wa.me untuk satu kontak")
    s.add_argument("--kontak", required=True)
    s.add_argument("--pesan", help="Pakai teks ini (mis. draf yang sudah diperhalus) untuk tautan wa.me")
    s.set_defaults(fungsi=cmd_draf)

    s = sub.add_parser("hari-ini", parents=[umum, sam], help="Pengingat follow-up harian + draf pesan")
    s.add_argument("--maks-draf", type=int, default=10)
    s.add_argument("--tanpa-draf", action="store_true")
    s.set_defaults(fungsi=cmd_hari_ini)

    s = sub.add_parser("rekap", parents=[umum, sam], help="Rekap pipeline, konversi, sumber lead")
    s.add_argument("--periode", help="hari-ini, kemarin, minggu-ini, minggu-lalu, bulan-ini (default), bulan-lalu, "
                                     "tahun-ini, semua")
    s.add_argument("--bulan", help="YYYY-MM, ini, lalu")
    s.add_argument("--tanggal", help="Satu hari")
    s.add_argument("--dari")
    s.add_argument("--sampai")
    s.add_argument("--rumus", action="store_true", help="Tampilkan rumus perhitungan")
    s.set_defaults(fungsi=cmd_rekap)

    s = sub.add_parser("cek-duplikat", parents=[umum, sam], help="Cari kontak dobel")
    s.set_defaults(fungsi=cmd_cek_duplikat)
    s = sub.add_parser("gabung", parents=[umum, tulis], help="Gabungkan dua kontak (besar: --ya)")
    s.add_argument("--dari", required=True)
    s.add_argument("--ke", required=True)
    s.set_defaults(fungsi=cmd_gabung)
    s = sub.add_parser("hapus", parents=[umum, tulis], help="Hapus kontak permanen (besar: --ya)")
    s.add_argument("--kontak", required=True)
    s.set_defaults(fungsi=cmd_hapus)

    s = sub.add_parser("impor", parents=[umum, tulis], help="Impor kontak dari CSV (besar: --ya)")
    s.add_argument("file")
    s.add_argument("--sumber-default")
    s.add_argument("--tahap-default")
    s.set_defaults(fungsi=cmd_impor)
    s = sub.add_parser("ekspor", parents=[umum, sam], help="Ekspor ke CSV")
    s.add_argument("--csv", required=True)
    s.add_argument("--format", choices=["lengkap", "pengingat"], default="lengkap")
    s.add_argument("--tahap", help="semua (default), aktif, atau nama tahap")
    s.add_argument("--timpa", action="store_true")
    s.set_defaults(fungsi=cmd_ekspor)

    s = sub.add_parser("backup", parents=[umum], help="Buat cadangan / --daftar")
    s.add_argument("--daftar", action="store_true")
    s.add_argument("--label")
    s.set_defaults(fungsi=cmd_backup)
    s = sub.add_parser("restore", parents=[umum, tulis], help="Pulihkan dari cadangan (besar: --ya)")
    s.add_argument("--dari", required=True)
    s.set_defaults(fungsi=cmd_restore)
    return p


def cetak(args, data, teks, kode_keluar):
    if args.json:
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
    if not hasattr(args, "ya"):
        args.ya = False
    if not hasattr(args, "samarkan"):
        args.samarkan = False
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
        pesan = (PESAN_TERKUNCI % _timeout()) if _terkunci(e) else \
            "Kesalahan database: %s. Jangan hapus file database; ulangi, atau pulihkan dari cadangan." % e
        return cetak(args, {"ok": False, "error": pesan}, pesan, 1)
    except sqlite3.DatabaseError as e:
        pesan = ("Database rusak (%s). Jangan hapus file itu. Pulihkan dari cadangan: crm.py backup --daftar, lalu "
                 "crm.py restore --dari <file>." % e)
        return cetak(args, {"ok": False, "error": pesan, "rusak": True}, pesan, 1)
    except OSError as e:
        pesan = "File tidak bisa ditulis/dibaca (%s). Periksa folder dan izin aksesnya." % e
        return cetak(args, {"ok": False, "error": pesan}, pesan, 1)
    return cetak(args, data, teks, 0)


if __name__ == "__main__":
    sys.exit(main())
