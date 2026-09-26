#!/usr/bin/env python3
"""kas-umkm (Komunitech) - buku kas harian lokal untuk warung, toko, dan UMKM.

Satu file database SQLite di komputer pemilik usaha. Hanya library standar Python 3.8+, lintas OS
(Windows: `python`/`py`), TANPA akses jaringan: script tidak pernah mengirim apa pun ke mana pun.

Lokasi database (urutan prioritas):
  1. --db PATH (ditulis setelah nama perintah)
  2. ENV KOMUNITECH_KAS_DB   (path file lengkap)
  3. ENV KOMUNITECH_DATA     (folder) + /kas/kas.db
  4. ~/KomunitechData/kas/kas.db
Cadangan: folder backup-kas/ di sebelah database (otomatis sekali sehari sebelum perubahan pertama, dan sebelum
impor/restore).

SEMUA perintah tulis hanya PRATINJAU (database tidak berubah) sampai diberi --ya.

Contoh:
  python3 kas.py init --nama-usaha "Warung Bu Sri" --kas-awal 500rb --ya
  python3 kas.py akun tambah --nama BRI --jenis bank --saldo-awal 3jt --terima-qris --ya
  python3 kas.py catat --masuk 1,2jt --kategori penjualan --metode tunai --catatan "jualan hari ini" --ya
  python3 kas.py catat --baris "keluar;25rb;beli-stok;tunai;gas elpiji" --baris "keluar;100rb;prive;tunai;jajan anak"
  python3 kas.py pindah --dari laci --ke BRI --jumlah 1jt --ya
  python3 kas.py opname --fisik 845rb                     # hitung uang fisik di laci
  python3 kas.py rekap --tanggal hari-ini                 # juga --minggu ini|lalu, --bulan ini|lalu|09/2026
  python3 kas.py impor mutasi.csv --akun BRI --jenis-file mutasi-bank
  python3 kas.py impor-kasir rekap-kasir.json             # rekap harian dari skill kasir-lokal
  python3 kas.py ekspor --format emkm|arus-kas|lengkap --csv file.csv

Aturan uang: semua nominal integer rupiah (tanpa sen). Nilai berkoma dari file bank dibulatkan ke rupiah terdekat
(0,5 ke atas). Rata-rata (ekspor arus-kas) dibulatkan ke rupiah terdekat.
Kode keluar: 0 = berhasil (termasuk pratinjau); 1 = gagal (pesan jelas di "error"); 2 = perintah salah tulis.
"""
import argparse
import csv
import hashlib
import io
import json
import os
import re
import sqlite3
import sys
from collections import OrderedDict
from datetime import date, datetime, timedelta, timezone
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from pathlib import Path

APLIKASI = "kas-umkm"
VERSI = "1.0.0"
SKEMA = 1
BATAS_NOMINAL = 10 ** 12            # Rp 1 triliun: di atas ini pasti salah ketik
NOMINAL_BESAR = 50 * 10 ** 6        # di atas ini diberi catatan "pastikan jumlah nolnya benar"
SIMPAN_BACKUP_HARIAN = 30

# kode -> (label, arah yang boleh, kelompok)
KATEGORI = OrderedDict([
    ("penjualan", ("Penjualan", ("masuk", "keluar"), "usaha")),
    ("modal", ("Modal pemilik", ("masuk",), "pemilik")),
    ("beli-stok", ("Beli stok/bahan", ("keluar",), "usaha")),
    ("gaji", ("Gaji/upah", ("keluar",), "usaha")),
    ("listrik-air", ("Listrik/air", ("keluar",), "usaha")),
    ("sewa", ("Sewa tempat", ("keluar",), "usaha")),
    ("prive", ("Prive (ambil pribadi)", ("keluar",), "pemilik")),
    ("pajak", ("Pajak", ("keluar",), "usaha")),
    ("pinjaman", ("Pinjaman/cicilan", ("masuk", "keluar"), "pinjaman")),
    ("lain-lain", ("Lain-lain", ("masuk", "keluar"), "usaha")),
])
KATEGORI_SISTEM = {"selisih-kas": ("Selisih hitung laci", ("masuk", "keluar"), "usaha"),
                   "pindah": ("Pindah dana", ("masuk", "keluar"), "pindah")}
SEMUA_KATEGORI = OrderedDict(list(KATEGORI.items()) + list(KATEGORI_SISTEM.items()))
LABEL_KHUSUS = {("penjualan", "keluar"): "Retur/refund penjualan", ("pinjaman", "masuk"): "Pinjaman diterima",
                ("pinjaman", "keluar"): "Cicilan pinjaman", ("lain-lain", "masuk"): "Pemasukan lain-lain",
                ("lain-lain", "keluar"): "Pengeluaran lain-lain", ("selisih-kas", "masuk"): "Selisih laci lebih",
                ("selisih-kas", "keluar"): "Selisih laci kurang"}
ALIAS_KATEGORI = {
    "penjualan": ["penjualan", "jualan", "jual", "omzet", "omset", "pendapatan", "pendapatan usaha", "sales",
                  "retur", "refund", "retur penjualan"],
    "modal": ["modal", "setor modal", "setoran modal", "tambah modal", "modal pemilik", "suntik dana",
              "suntikan dana", "modal awal"],
    "beli-stok": ["beli stok", "beli stock", "stok", "stock", "belanja stok", "kulakan", "kulak", "belanja bahan",
                  "bahan", "bahan baku", "beli barang", "restock", "restok", "beli bahan", "stok bahan",
                  "beli stok bahan"],
    "gaji": ["gaji", "upah", "gaji karyawan", "bayar karyawan", "honor", "lembur", "thr", "gaji upah"],
    "listrik-air": ["listrik air", "listrik", "air", "pln", "token listrik", "pdam", "utilitas", "listrik dan air"],
    "sewa": ["sewa", "sewa tempat", "kontrakan", "sewa kios", "sewa lapak", "sewa ruko"],
    "prive": ["prive", "privee", "pribadi", "ambil pribadi", "prive ambil pribadi", "keperluan pribadi",
              "ambil pribadi prive"],
    "pajak": ["pajak", "pph", "pph final", "pbjt", "pb1", "ppn", "setor pajak"],
    "pinjaman": ["pinjaman", "cicilan", "angsuran", "kur", "utang bank", "pinjam", "cicilan pinjaman",
                 "pinjaman cicilan"],
    "lain-lain": ["lain lain", "lain", "lainnya", "dll", "lain2", "other"],
}
# Tebakan kategori dari catatan (dipakai bila --kategori kosong); urutan penting.
TEBAK = [
    ("prive", "keluar", r"\b(prive|privee|pribadi|rumah tangga|belanja rumah|keperluan rumah|kebutuhan rumah|spp|"
                        r"uang sekolah|sekolah anak|jajan|uang saku|arisan|kondangan|kirim (ortu|orang tua|ibu|bapak)|"
                        r"liburan|gaji (saya|pemilik|owner|sendiri))\b"),
    ("pajak", "keluar", r"\b(pajak|pph|pbjt|pb1|ppn)\b"),
    ("pinjaman", None, r"\b(cicilan|angsuran|kur|pinjaman|pencairan kredit|pencairan pinjaman)\b"),
    ("gaji", "keluar", r"\b(gaji|upah|honor|lembur|thr|karyawan|pegawai)\b"),
    ("sewa", "keluar", r"\b(sewa|kontrakan)\b"),
    ("listrik-air", "keluar", r"\b(listrik|pln|token listrik|pdam|tagihan air|bayar air|rekening air)\b"),
    ("beli-stok", "keluar", r"\b(kulak|kulakan|stok|stock|restock|restok|bahan|belanja pasar|belanja barang|"
                            r"beli barang|supplier|suplier|grosir|dagangan|air mineral)\b"),
    ("modal", "masuk", r"\b(modal|suntik dana|suntikan dana)\b"),
    ("penjualan", "masuk", r"\b(jual|jualan|penjualan|omzet|omset|laku|terjual|pesanan|orderan|order|pembeli|"
                           r"pelanggan|qris)\b"),
    ("penjualan", "keluar", r"\b(retur|refund|pengembalian uang|kembalikan uang)\b"),
    ("lain-lain", None, r"\b(biaya adm|biaya admin|adm bank|biaya administrasi|biaya transfer|biaya materai|"
                        r"bunga)\b"),
]
POLA_PRIBADI = re.compile(TEBAK[0][2])
POLA_MUNGKIN_PINDAH = re.compile(r"\b(tarik tunai|tarikan atm|tarikan tunai|tarik atm|setor tunai|setoran tunai|"
                                 r"top ?up|pindah buku|pindahbuku|overbooking|pindah dana)\b")
METODE = OrderedDict([
    ("tunai", ("Tunai", ["tunai", "cash", "kontan", "cas", "uang tunai", "laci"])),
    ("transfer", ("Transfer", ["transfer", "tf", "trf", "bank", "m banking", "mbanking", "rekening"])),
    ("qris", ("QRIS", ["qris", "qr"])),
    ("e-wallet", ("E-wallet", ["e wallet", "ewallet", "ovo", "gopay", "dana", "shopeepay", "linkaja",
                               "dompet digital"])),
    ("kartu", ("Kartu debit/kredit", ["kartu", "debit", "edc", "kartu debit", "kartu kredit"])),
    ("pindah", ("Pindah dana", ["pindah"])),
])
JENIS_AKUN = {"tunai": ["tunai", "laci", "kas", "cash", "kas tunai", "brankas"],
              "bank": ["bank", "rekening", "tabungan", "giro"],
              "e-wallet": ["e wallet", "ewallet", "dompet digital", "gopay", "ovo", "dana", "shopeepay", "linkaja"]}
LABEL_JENIS = {"tunai": "tunai", "bank": "rekening bank", "e-wallet": "e-wallet"}
METODE_DEFAULT_AKUN = {"tunai": "tunai", "bank": "transfer", "e-wallet": "e-wallet"}
# kasir-lokal: label metode -> kode metode kas-umkm (None = bukan uang, tidak dicatat)
METODE_KASIR = {"tunai": "tunai", "qris": "qris", "transfer": "transfer", "debit": "kartu", "kartu kredit": "kartu",
                "e-wallet": "e-wallet", "lainnya": None}
# ekspor laporan-keuangan-emkm: (kategori, arah) -> kode kategori emkm ("" = diklasifikasi emkm dari keterangan)
EMKM = {("penjualan", "masuk"): "pendapatan_usaha", ("penjualan", "keluar"): "retur_penjualan",
        ("modal", "masuk"): "setoran_modal", ("beli-stok", "keluar"): "pembelian_bahan",
        ("gaji", "keluar"): "beban_gaji", ("listrik-air", "keluar"): "beban_utilitas",
        ("sewa", "keluar"): "beban_sewa", ("prive", "keluar"): "prive",
        ("pinjaman", "masuk"): "pinjaman_diterima", ("pinjaman", "keluar"): "bayar_pinjaman",
        ("selisih-kas", "masuk"): "pendapatan_lain", ("selisih-kas", "keluar"): "beban_lain"}
ZONA = {"WIB": 7, "WITA": 8, "WIT": 9}
ALIAS_ZONA = {"wib": "WIB", "asia/jakarta": "WIB", "asia/pontianak": "WIB", "wita": "WITA", "asia/makassar": "WITA",
              "wit": "WIT", "asia/jayapura": "WIT"}
HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
HR = ["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"]
BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober",
         "November", "Desember"]
NAMA_BULAN = {}
for _i, _al in enumerate([("jan", "januari", "january"), ("feb", "februari", "pebruari", "february"),
                          ("mar", "maret", "march"), ("apr", "april"), ("mei", "may"), ("jun", "juni", "june"),
                          ("jul", "juli", "july"), ("agu", "agt", "ags", "agus", "agustus", "aug", "august"),
                          ("sep", "sept", "september"), ("okt", "oktober", "oct", "october"),
                          ("nov", "nop", "november", "nopember"), ("des", "desember", "dec", "december")], 1):
    for _a in _al:
        NAMA_BULAN[_a] = _i
SATUAN_NOMINAL = {"rb": 1000, "ribu": 1000, "rbu": 1000, "k": 1000, "jt": 10 ** 6, "juta": 10 ** 6,
                  "jeti": 10 ** 6, "miliar": 10 ** 9, "milyar": 10 ** 9, "M": 10 ** 9}
PECAHAN_SAH = {100000, 75000, 50000, 20000, 10000, 5000, 2000, 1000, 500, 200, 100, 50}


class Gagal(Exception):
    """Error yang pesannya aman ditampilkan ke pengguna."""

    def __init__(self, pesan, **detail):
        super().__init__(pesan)
        self.pesan = pesan
        self.detail = detail


def _timeout():
    try:
        return max(0.1, float(os.environ.get("KOMUNITECH_KAS_TIMEOUT", "15")))
    except ValueError:
        return 15.0


def _detik():
    return ("%.1f" % _timeout()).rstrip("0").rstrip(".").replace(".", ",")


def _terkunci(e):
    s = str(e).lower()
    return "locked" in s or "busy" in s


SARAN_PULIH = ("Pulihkan: kas.py backup --daftar (lihat cadangan), lalu kas.py restore --dari <file cadangan> "
               "(pratinjau, lalu --ya); file rusak otomatis dipindah ke folder backup-kas, tidak dihapus. Belum ada "
               "cadangan? kas.py init --mulai-baru (pratinjau, lalu --ya) untuk database kosong baru.")
PESAN_TERKUNCI = ("Buku kas sedang dipakai program lain (mis. jadwal OpenClaw atau jendela lain) dan tidak selesai "
                  "dalam %s detik. Data aman, tidak rusak. Tunggu sebentar lalu ulangi perintah yang sama. Jangan "
                  "hapus file database.")

# --------------------------------------------------------------------------- waktu & tanggal
_JAM = {"kini": None, "zona": "WIB"}


def kode_zona(teks):
    k = ALIAS_ZONA.get(str(teks or "").strip().lower())
    if not k:
        raise Gagal("Zona waktu '%s' tidak dikenal. Pakai WIB, WITA, atau WIT." % teks)
    return k


def kini():
    if _JAM["kini"]:
        return _JAM["kini"]
    u = datetime.now(timezone.utc)
    return u.astimezone(timezone(timedelta(hours=ZONA[_JAM["zona"]]))).replace(tzinfo=None, microsecond=0)


def hari_ini():
    return kini().date()


def stempel():
    return kini().isoformat(" ", "seconds")


def tgl_id(d):
    if isinstance(d, str):
        d = date.fromisoformat(d[:10])
    return "%02d/%02d/%04d" % (d.day, d.month, d.year)


def tgl_panjang(d):
    return "%s, %s" % (HARI[d.weekday()], tgl_id(d))


def senin(d):
    return d - timedelta(days=d.weekday())


def akhir_bulan(d):
    nb = date(d.year + (d.month == 12), d.month % 12 + 1, 1)
    return nb - timedelta(days=1)


def _buat_tanggal(y, m, d, asli):
    try:
        return date(y, m, d)
    except ValueError:
        raise Gagal("Tanggal '%s' tidak ada di kalender." % asli)


def baca_tanggal(teks, boleh_depan=False):
    """Tanggal format Indonesia (hari/bulan/tahun 4 angka) atau ISO YYYY-MM-DD. Yang ambigu DITOLAK:
    tanpa tahun, tahun 2 angka, urutan bulan/hari (Amerika), nomor seri Excel."""
    if teks is None or not str(teks).strip():
        raise Gagal("Tanggal kosong.")
    asli = str(teks).strip()
    acuan = hari_ini()
    s = re.sub(r"\s+", " ", asli.lower().replace(",", " ")).strip()
    rel = {"hari ini": 0, "hari-ini": 0, "hr ini": 0, "sekarang": 0, "today": 0, "kemarin": -1, "kmrn": -1,
           "kemaren": -1, "yesterday": -1, "kemarin lusa": -2}
    d = None
    if s in rel:
        d = acuan + timedelta(days=rel[s])
    if d is None:
        m = re.fullmatch(r"(\d{1,3}) ?(hari|hr) ?(yang )?lalu", s)
        if m:
            d = acuan - timedelta(days=int(m.group(1)))
    if d is None:
        s2 = re.sub(r"^(hari )?(senin|selasa|rabu|kamis|jumat|jum'at|sabtu|minggu|ahad) ", "", s)
        s2 = re.sub(r"^(tgl\.?|tanggal) ?", "", s2).strip()
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
                    raise Gagal("Tanggal '%s' sepertinya berurutan bulan/hari (format Amerika). Buku kas memakai "
                                "hari/bulan/tahun: tulis %02d/%02d/%s." % (asli, b, a, th))
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
            raise Gagal("Tanggal '%s' tidak dikenali. Contoh: 26/09/2026, 26 Sep 2026, hari ini, kemarin, "
                        "3 hari lalu." % asli)
    if d.year < 2000:
        raise Gagal("Tanggal '%s' terlalu lama (sebelum tahun 2000); periksa lagi." % asli)
    if not boleh_depan and d > acuan:
        raise Gagal("Tanggal %s ada di masa depan (hari ini %s). Buku kas hanya mencatat uang yang sudah masuk/"
                    "keluar." % (tgl_id(d), tgl_id(acuan)))
    return d


def baca_bulan(teks):
    acuan = hari_ini()
    s = re.sub(r"\s+", " ", str(teks or "").strip().lower())
    if s in ("ini", "bulan ini", "bulan-ini"):
        y, m = acuan.year, acuan.month
    elif s in ("lalu", "bulan lalu", "bulan-lalu", "kemarin"):
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
        elif s in NAMA_BULAN:
            raise Gagal("Bulan '%s' tanpa tahun. Tulis mis. '%s %d' atau '%02d/%d'." %
                        (teks, teks, acuan.year, NAMA_BULAN[s], acuan.year))
        else:
            raise Gagal("Bulan '%s' tidak dikenali. Contoh: ini, lalu, 09/2026, September 2026." % teks)
        if not 1 <= m <= 12:
            raise Gagal("Bulan '%s' tidak ada." % teks)
    awal = date(y, m, 1)
    return awal, akhir_bulan(awal)


def ambil_periode(args, default="hari"):
    """(dari, sampai, jenis) dari --tanggal / --minggu / --bulan / --dari --sampai."""
    acuan = hari_ini()
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
    if getattr(args, "minggu", None):
        s = args.minggu.strip().lower()
        if s in ("ini", "minggu ini", "minggu-ini"):
            d = acuan
        elif s in ("lalu", "minggu lalu", "minggu-lalu", "kemarin"):
            d = acuan - timedelta(days=7)
        else:
            d = baca_tanggal(args.minggu, True)
        return senin(d), senin(d) + timedelta(days=6), "minggu"
    if getattr(args, "tanggal", None):
        d = baca_tanggal(args.tanggal, True)
        return d, d, "hari"
    if default == "semua":
        return None, None, "semua"
    return acuan, acuan, "hari"


# --------------------------------------------------------------------------- angka
def rp(n):
    if n is None:
        return "-"
    n = int(n)
    return ("-" if n < 0 else "") + "Rp " + "{:,}".format(abs(n)).replace(",", ".")


def bulat(x):
    """Rupiah terdekat, setengah ke atas."""
    return int(Decimal(x).quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def persen(a, b):
    if not b:
        return "-"
    d = (Decimal(a) * 100 / Decimal(b)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    return ("%s%%" % d).replace(".", ",")


def parse_nominal(teks, boleh_nol=False):
    """'4,5 jt' | '4.500.000' | 'Rp4.500.000' | '750rb' | '4 jt 500 rb' | '25000' -> int rupiah (> 0)."""
    if teks is None or not str(teks).strip():
        raise Gagal("Nominal kosong.")
    asli = str(teks).strip()
    s = re.sub(r"(?i)^\s*(rp\.?|idr)\s*", "", asli).strip()
    s = re.sub(r"(?i)\s*(,-|\.-)$", "", s)
    if s.startswith("-") or s.startswith("("):
        raise Gagal("Nominal '%s' tidak boleh minus. Pakai --masuk atau --keluar untuk arah uangnya." % asli)
    if re.fullmatch(r"(?i)\d+([.,]\d+)?e[+-]?\d+", s):
        raise Gagal("Nominal '%s' berbentuk angka ilmiah Excel. Tulis angka lengkap, mis. 1500000." % asli)
    bagian = re.findall(r"(\d[\d.,]*)\s*([A-Za-z]+)?\s*", s)
    if not bagian or re.sub(r"(\d[\d.,]*)\s*([A-Za-z]+)?\s*", "", s).strip(" dan&+"):
        raise Gagal("Nominal '%s' tidak dikenali. Contoh: 25rb, 1,2 jt, 1.250.000." % asli)
    total = Decimal(0)
    for angka, sat in bagian:
        if sat == "m":
            raise Gagal("Nominal '%s' ambigu: 'm' itu juta atau miliar? Tulis 'jt' atau 'miliar'." % asli)
        if sat and sat not in SATUAN_NOMINAL and sat.lower() not in SATUAN_NOMINAL:
            raise Gagal("Satuan '%s' pada nominal '%s' tidak dikenal. Pakai rb, jt, atau miliar." % (sat, asli))
        kali = SATUAN_NOMINAL.get(sat, SATUAN_NOMINAL.get((sat or "").lower(), 1)) if sat else 1
        if len(bagian) > 1 and not sat:
            raise Gagal("Nominal '%s' ambigu: bagian '%s' tidak bersatuan. Tulis mis. '1 jt 250 rb'." % (asli, angka))
        angka = re.sub(r"[.,]00$", "", angka) if not sat else angka
        if not re.search(r"[.,]", angka):
            nilai = Decimal(angka)
        elif sat:
            m = re.fullmatch(r"(\d+),(\d{1,3})", angka) or re.fullmatch(r"(\d+)\.(\d{1,2})", angka)
            if not m:
                raise Gagal("Nominal '%s' ambigu (mis. '1.500 jt' = 1,5 juta atau 1.500 juta?). Tulis mis. "
                            "'1,5 jt' atau '1500000'." % asli)
            nilai = Decimal(m.group(1) + "." + m.group(2))
        elif re.fullmatch(r"\d{1,3}([.]\d{3})+|\d{1,3}(,\d{3})+", angka):
            nilai = Decimal(re.sub(r"[.,]", "", angka))
        else:
            raise Gagal("Nominal '%s' ambigu atau berisi sen. Tulis rupiah bulat, mis. '25rb', '1,2 jt', "
                        "'1.250.000'." % asli)
        total += nilai * kali
    if total != total.to_integral_value():
        raise Gagal("Nominal '%s' menghasilkan pecahan rupiah; tulis dalam rupiah bulat." % asli)
    n = int(total)
    if n == 0 and not boleh_nol:
        raise Gagal("Nominal harus lebih dari Rp 0.")
    if n >= BATAS_NOMINAL:
        raise Gagal("Nominal %s terlalu besar untuk buku kas UMKM; kemungkinan salah ketik." % rp(n))
    return n


def nominal_file(teks):
    """Nominal dari file (CSV/mutasi bank): format Indonesia (1.500.000,00) maupun Inggris (1,500,000.00),
    tanda minus/kurung, akhiran CR/DB. Kembalikan (nilai bertanda int, dibulatkan: bool, tanda_bank: 'CR'/'DB'/None).
    Nilai kosong -> None. Error -> ValueError(pesan)."""
    s = str(teks or "").strip()
    if not s or s in ("-", "0", "0,00", "0.00"):
        return None
    tanda_bank = None
    m = re.search(r"(?i)\s*\b(CR|DB|K|D)\s*$", s)
    if m:
        tanda_bank = {"cr": "CR", "k": "CR", "db": "DB", "d": "DB"}[m.group(1).lower()]
        s = s[:m.start()].strip()
    s = re.sub(r"(?i)^(rp\.?|idr)\s*", "", s).strip()
    s = re.sub(r"(?i)\s*(,-|\.-)$", "", s).replace(" ", "")
    neg = False
    if s.startswith("(") and s.endswith(")"):
        neg, s = True, s[1:-1]
    if s.startswith("-"):
        neg, s = True, s[1:]
    s = re.sub(r"(?i)^(rp\.?|idr)", "", s)
    if re.fullmatch(r"(?i)\d+([.,]\d+)?e[+-]?\d+", s):
        raise ValueError("angka ilmiah Excel ('%s'); format kolom sebagai angka biasa lalu simpan ulang" % teks)
    if not re.fullmatch(r"[\d.,]+", s) or not re.search(r"\d", s):
        raise ValueError("nominal tidak terbaca ('%s')" % teks)
    if "." in s and "," in s:
        des = "," if s.rfind(",") > s.rfind(".") else "."
        rib = "." if des == "," else ","
        utuh, pecahan = s.rsplit(des, 1)
        if not re.fullmatch(r"\d{1,3}(%s\d{3})*" % re.escape(rib), utuh) or not re.fullmatch(r"\d{1,2}", pecahan):
            raise ValueError("format nominal tidak jelas ('%s')" % teks)
        nilai = Decimal(utuh.replace(rib, "") + "." + pecahan)
    elif "." in s or "," in s:
        sep = "." if "." in s else ","
        if re.fullmatch(r"\d{1,3}(%s\d{3})+" % re.escape(sep), s):
            nilai = Decimal(s.replace(sep, ""))
        elif re.fullmatch(r"\d+%s\d{1,2}" % re.escape(sep), s):
            nilai = Decimal(s.replace(sep, "."))
        else:
            raise ValueError("format nominal tidak jelas ('%s')" % teks)
    else:
        nilai = Decimal(s)
    dibulatkan = nilai != nilai.to_integral_value()
    n = bulat(nilai)
    if neg:
        n = -n
    return n, dibulatkan, tanda_bank


# --------------------------------------------------------------------------- teks
def normal(teks):
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9]+", " ", str(teks or "").lower())).strip()


def bersih(teks, maks=200):
    s = re.sub(r"[\x00-\x08\x0b-\x1f\x7f]", " ", str(teks or ""))
    return re.sub(r"\s+", " ", s).strip()[:maks]


def label_kat(kode, arah=None):
    if arah and (kode, arah) in LABEL_KHUSUS:
        return LABEL_KHUSUS[(kode, arah)]
    return SEMUA_KATEGORI[kode][0]


def kode_kategori(teks):
    n = normal(teks)
    if not n:
        return None
    for kode, alias in ALIAS_KATEGORI.items():
        if n == normal(kode) or n in alias:
            return kode
    return None


def tebak_kategori(teks, arah):
    n = " " + normal(teks) + " "
    for kode, a, pola in TEBAK:
        if a and a != arah:
            continue
        m = re.search(pola, n)
        if m:
            return kode, m.group(0).strip()
    return None, None


def kode_metode(teks):
    n = normal(teks)
    if not n:
        return None
    for kode, (label, alias) in METODE.items():
        if n == normal(kode) or n in alias or n == normal(label):
            return kode
    raise Gagal("Metode '%s' tidak dikenal. Pilih: tunai, transfer, qris, e-wallet, kartu." % teks)


def kode_jenis_akun(teks):
    n = normal(teks)
    for kode, alias in JENIS_AKUN.items():
        if n == normal(kode) or n in alias:
            return kode
    raise Gagal("Jenis akun '%s' tidak dikenal. Pilih: tunai (laci/brankas), bank, e-wallet." % teks)


def slug(teks):
    s = re.sub(r"[^a-z0-9]+", "-", str(teks or "").lower()).strip("-")
    return s[:40]


# --------------------------------------------------------------------------- database
SKEMA_SQL = """
CREATE TABLE meta(kunci TEXT PRIMARY KEY, nilai TEXT);
CREATE TABLE akun(id INTEGER PRIMARY KEY, kode TEXT UNIQUE NOT NULL, nama TEXT NOT NULL, jenis TEXT NOT NULL,
  saldo_awal INTEGER NOT NULL DEFAULT 0, tanggal_awal TEXT NOT NULL, terima_qris INTEGER NOT NULL DEFAULT 0,
  dibuat TEXT NOT NULL);
CREATE TABLE transaksi(id INTEGER PRIMARY KEY, tanggal TEXT NOT NULL,
  arah TEXT NOT NULL CHECK(arah IN ('masuk','keluar')), jumlah INTEGER NOT NULL CHECK(jumlah > 0),
  kategori TEXT NOT NULL, metode TEXT NOT NULL, akun_id INTEGER NOT NULL REFERENCES akun(id),
  catatan TEXT NOT NULL DEFAULT '', jenis TEXT NOT NULL DEFAULT 'biasa', grup TEXT,
  sumber TEXT NOT NULL DEFAULT 'manual', sidik TEXT, status TEXT NOT NULL DEFAULT 'aktif', alasan_batal TEXT,
  dibuat TEXT NOT NULL);
CREATE INDEX ix_trx_tanggal ON transaksi(tanggal);
CREATE INDEX ix_trx_sidik ON transaksi(sidik);
CREATE TABLE opname(id INTEGER PRIMARY KEY, tanggal TEXT NOT NULL, akun_id INTEGER NOT NULL, saldo_buku INTEGER NOT NULL,
  fisik INTEGER NOT NULL, selisih INTEGER NOT NULL, rincian TEXT, disesuaikan INTEGER NOT NULL DEFAULT 0,
  transaksi_id INTEGER, catatan TEXT, dibuat TEXT NOT NULL);
CREATE TABLE log(id INTEGER PRIMARY KEY, waktu TEXT NOT NULL, perintah TEXT NOT NULL, ringkasan TEXT);
"""
PENGATURAN_DEFAULT = {"nama_usaha": "", "zona": "WIB", "batas_prive": ""}


def path_db(args):
    if getattr(args, "db", None):
        p = Path(args.db).expanduser()
    elif os.environ.get("KOMUNITECH_KAS_DB"):
        p = Path(os.environ["KOMUNITECH_KAS_DB"]).expanduser()
    elif os.environ.get("KOMUNITECH_DATA"):
        p = Path(os.environ["KOMUNITECH_DATA"]).expanduser() / "kas" / "kas.db"
    else:
        p = Path.home() / "KomunitechData" / "kas" / "kas.db"
    return p.resolve()


def folder_backup(db):
    return db.parent / "backup-kas"


def buka(db, baca_saja=False):
    if not db.is_file():
        raise Gagal("Buku kas belum ada di %s. Jalankan dulu: kas.py init --nama-usaha \"...\" (pratinjau, lalu --ya "
                    "setelah pengguna setuju)." % db, db=str(db), belum_ada=True)
    if db.stat().st_size == 0:
        raise Gagal("File %s kosong (0 byte), bukan buku kas yang bisa dibaca. %s" % (db, SARAN_PULIH), rusak=True)

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
            conn.execute("SELECT COUNT(*) FROM transaksi").fetchone()
            break
        except sqlite3.OperationalError as e:
            conn.close()
            pesan = str(e).lower()
            if _terkunci(e):
                raise Gagal(PESAN_TERKUNCI % _detik())
            if ro and "readonly" in pesan:
                ro = False      # ada journal sisa: buka biasa sekali agar SQLite memulihkannya
                continue
            if "no such table" in pesan:
                raise Gagal("File %s bukan buku kas kas-umkm (%s). File itu tidak diubah; periksa --db." % (db, e))
            raise Gagal("Database %s tidak bisa dibaca (%s). Jangan hapus file itu. %s" % (db, e, SARAN_PULIH),
                        rusak=True)
        except sqlite3.DatabaseError:
            conn.close()
            raise Gagal("File %s rusak atau bukan buku kas kas-umkm. Jangan hapus file itu. %s" % (db, SARAN_PULIH),
                        rusak=True)
    if not r or r[0] != APLIKASI:
        conn.close()
        raise Gagal("File %s bukan buku kas kas-umkm. File itu tidak diubah; periksa --db." % db)
    if sk and str(sk[0]).isdigit() and int(sk[0]) > SKEMA:
        conn.close()
        raise Gagal("Buku kas dibuat oleh kas-umkm versi lebih baru (skema %s). Perbarui skill kas-umkm dulu." % sk[0])
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
    tujuan = nama_unik(fol, "kas-%s-%s" % (kini().strftime("%Y%m%d-%H%M%S"), label))
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


def backup_harian(db):
    """Cadangan otomatis sekali sehari (sebelum perubahan pertama hari itu). Simpan 30 terakhir."""
    fol = folder_backup(db)
    awalan = "kas-%s-" % kini().strftime("%Y%m%d")
    if fol.is_dir() and any(p.name.startswith(awalan) for p in fol.glob("kas-*.db")):
        return None
    b = buat_backup(db, "harian")
    for lama in sorted(fol.glob("kas-*-harian*.db"))[:-SIMPAN_BACKUP_HARIAN]:
        try:
            lama.unlink()
        except OSError:
            pass
    return b


def singkirkan(db, pola, pindah):
    """Salin (database sehat) atau pindahkan (database rusak) ke backup-kas/. Tidak pernah menghapus apa pun."""
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
    """'tidak_ada' | 'sehat' | 'rusak'."""
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


def jalankan_tulis(args, perintah, kerja, label_backup=None):
    """Jalankan kerja(conn, cfg) dalam satu transaksi. Tanpa --ya: ROLLBACK (pratinjau persis, database tidak
    berubah). Dengan --ya: cadangan dulu, lalu COMMIT. kerja mengembalikan data dict berisi 'teks' dan boleh
    'blokir': [{'opsi': '--izinkan-minus', 'pesan': ...}] = hal yang harus diputuskan pengguna dulu."""
    db = path_db(args)
    conn = buka(db)
    simpan = bool(args.ya)
    backup = None
    try:
        if simpan:
            backup = buat_backup(db, label_backup) if label_backup else backup_harian(db)
        try:
            conn.execute("BEGIN IMMEDIATE")
        except sqlite3.OperationalError as e:
            if _terkunci(e):
                raise Gagal(PESAN_TERKUNCI % _detik())
            raise
        try:
            data = kerja(conn, pengaturan(conn))
            blokir = data.pop("blokir", [])
            if simpan and blokir:
                conn.execute("ROLLBACK")
                raise Gagal("BELUM DISIMPAN. Perlu keputusan pengguna dulu:\n" +
                            "\n".join("- " + b["pesan"] for b in blokir),
                            perlu_izin=[b["opsi"] for b in blokir])
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
    teks = data.pop("teks")
    data.setdefault("ok", True)
    data.setdefault("peringatan", [])
    data["mode"] = "tersimpan" if simpan else "pratinjau"
    data["perlu_konfirmasi"] = not simpan
    data["perlu_izin"] = [b["opsi"] for b in blokir]
    data["db"] = str(db)
    if backup:
        data["backup"] = backup
    if data["peringatan"]:
        teks += "\n" + "\n".join("Catatan: " + p for p in data["peringatan"])
    if simpan:
        teks = "TERSIMPAN.\n" + teks
    else:
        if blokir:
            teks += "\n\nPERLU KEPUTUSAN PENGGUNA sebelum disimpan:\n" + "\n".join("- " + b["pesan"] for b in blokir)
        teks = ("PRATINJAU (belum disimpan):\n" + teks +
                "\n\nSimpan? Jalankan perintah yang sama + --ya setelah pengguna setuju.")
    data["teks"] = teks
    return data, teks


def baca_db(args):
    db = path_db(args)
    return db, buka(db, baca_saja=True)


# --------------------------------------------------------------------------- akun & saldo
def semua_akun(conn):
    return conn.execute("SELECT * FROM akun ORDER BY id").fetchall()


def akun_by_id(conn, aid):
    return conn.execute("SELECT * FROM akun WHERE id=?", (aid,)).fetchone()


def cari_akun(conn, ref):
    n = normal(ref)
    if not n:
        raise Gagal("Nama akun kosong.")
    rows = semua_akun(conn)
    for a in rows:
        if n == normal(a["kode"]) or n == normal(a["nama"]):
            return a
    if n in ("laci", "kas", "tunai", "cash", "kas tunai", "laci kas"):
        tunai = [a for a in rows if a["jenis"] == "tunai"]
        if len(tunai) == 1:
            return tunai[0]
    cocok = [a for a in rows if n in normal(a["nama"]) or n in normal(a["kode"])]
    if len(cocok) == 1:
        return cocok[0]
    raise Gagal("Akun '%s' tidak ditemukan%s. Akun yang ada: %s. Tambah akun: kas.py akun tambah --nama ... "
                "--jenis tunai|bank|e-wallet." % (ref, " (lebih dari satu cocok)" if len(cocok) > 1 else "",
                                                  ", ".join(a["nama"] for a in rows) or "-"))


def akun_untuk_metode(conn, metode):
    """Akun default untuk sebuah metode bayar. Kembalikan (akun, catatan) atau Gagal bila ambigu."""
    rows = semua_akun(conn)
    if metode == "tunai":
        pilih = [a for a in rows if a["jenis"] == "tunai"]
        nama_jenis = "tunai (laci)"
    elif metode == "qris":
        pilih = [a for a in rows if a["terima_qris"]]
        if not pilih:
            pilih = [a for a in rows if a["jenis"] == "bank"]
        nama_jenis = "penampung QRIS (bank/e-wallet)"
    elif metode == "e-wallet":
        pilih = [a for a in rows if a["jenis"] == "e-wallet"]
        nama_jenis = "e-wallet"
    else:
        pilih = [a for a in rows if a["jenis"] == "bank"]
        nama_jenis = "rekening bank"
    if len(pilih) == 1:
        return pilih[0]
    if not pilih:
        raise Gagal("Belum ada akun %s untuk metode %s. Tambah dulu: kas.py akun tambah --nama \"BRI\" --jenis %s "
                    "(pratinjau, lalu --ya), atau sebut akunnya dengan --akun." %
                    (nama_jenis, METODE[metode][0], "e-wallet" if metode == "e-wallet" else "bank"),
                    perlu_akun=True)
    raise Gagal("Ada %d akun %s (%s). Sebut akunnya dengan --akun \"...\"." %
                (len(pilih), nama_jenis, ", ".join(a["nama"] for a in pilih)), perlu_akun=True)


def saldo_awal_hari(conn, a, d):
    """Saldo akun di AWAL hari d (sebelum transaksi tanggal d). 0 bila akun belum dimulai."""
    mulai = date.fromisoformat(a["tanggal_awal"])
    if d < mulai:
        return 0
    r = conn.execute("SELECT COALESCE(SUM(CASE WHEN arah='masuk' THEN jumlah ELSE -jumlah END),0) FROM transaksi "
                     "WHERE akun_id=? AND status='aktif' AND tanggal<?", (a["id"], d.isoformat())).fetchone()[0]
    return a["saldo_awal"] + r


def saldo_akhir_hari(conn, a, d):
    return saldo_awal_hari(conn, a, d + timedelta(days=1))


def saldo_pembuka(conn, a, dari):
    """Saldo pembuka periode: saldo di awal max(dari, tanggal mulai akun)."""
    return saldo_awal_hari(conn, a, max(dari, date.fromisoformat(a["tanggal_awal"])))


def cari_minus(conn, akun_ids, dari):
    """Hari-hari (>= dari) yang saldo AKHIR HARI-nya minus, per akun. Urutan catat dalam satu hari tidak dinilai."""
    hasil = []
    for aid in sorted(set(akun_ids)):
        a = akun_by_id(conn, aid)
        mulai = max(dari, date.fromisoformat(a["tanggal_awal"]))
        saldo = saldo_awal_hari(conn, a, mulai)
        per_hari = conn.execute(
            "SELECT tanggal, SUM(CASE WHEN arah='masuk' THEN jumlah ELSE -jumlah END) AS net FROM transaksi "
            "WHERE akun_id=? AND status='aktif' AND tanggal>=? GROUP BY tanggal ORDER BY tanggal",
            (aid, mulai.isoformat())).fetchall()
        pertama, terendah = None, None
        for r in per_hari:
            saldo += r["net"]
            if saldo < 0:
                if pertama is None:
                    pertama = (r["tanggal"], saldo)
                if terendah is None or saldo < terendah[1]:
                    terendah = (r["tanggal"], saldo)
        if pertama:
            hasil.append({"akun": a["nama"], "akun_id": aid, "tanggal": pertama[0], "saldo": pertama[1],
                          "terendah_tanggal": terendah[0], "terendah": terendah[1]})
    return hasil


def blokir_minus(minus):
    if not minus:
        return []
    bag = []
    for m in minus:
        t = "saldo %s jadi MINUS %s pada akhir %s" % (m["akun"], rp(m["saldo"]), tgl_id(m["tanggal"]))
        if m["terendah"] != m["saldo"]:
            t += " (terendah %s pada %s)" % (rp(m["terendah"]), tgl_id(m["terendah_tanggal"]))
        bag.append(t)
    return [{"opsi": "--izinkan-minus",
             "pesan": "; ".join(bag) + ". Uang di laci/rekening tidak mungkin minus: biasanya ada uang masuk yang "
                      "belum dicatat (penjualan, modal, pindah dana) atau salah pilih akun/nominal. Catat dulu yang "
                      "kurang, atau bila pengguna menegaskan memang benar (mis. rekening cerukan), ulangi dengan "
                      "--izinkan-minus."}]


# --------------------------------------------------------------------------- transaksi
def siapkan_entri(conn, arah, jumlah_teks, kategori_teks, metode_teks, catatan, akun_teks, tanggal_teks):
    """Validasi satu entri. Kembalikan dict entri + daftar catatan (asumsi/tebakan) + peringatan."""
    if arah not in ("masuk", "keluar"):
        raise Gagal("Arah '%s' tidak dikenal. Pakai masuk atau keluar." % arah)
    jumlah = parse_nominal(jumlah_teks)
    tanggal = baca_tanggal(tanggal_teks) if tanggal_teks else hari_ini()
    catatan = bersih(catatan, 200)
    asumsi, peringatan = [], []
    if kategori_teks:
        kat = kode_kategori(kategori_teks)
        if not kat:
            raise Gagal("Kategori '%s' tidak dikenal. Pilih: %s." % (kategori_teks, ", ".join(KATEGORI)))
    else:
        kat, kata = tebak_kategori(catatan, arah)
        if not kat:
            raise Gagal("Kategori untuk '%s' (%s %s) belum jelas. Tanyakan ke pengguna, pilih salah satu: %s." %
                        (catatan or "tanpa catatan", arah, rp(jumlah), ", ".join(KATEGORI)), perlu_kategori=True)
        asumsi.append("kategori '%s' ditebak dari kata '%s'" % (kat, kata))
    if arah not in KATEGORI[kat][1]:
        if kat == "modal":
            raise Gagal("Kategori modal hanya untuk uang MASUK dari pemilik. Uang usaha yang diambil untuk "
                        "keperluan pribadi = prive.")
        if kat == "prive":
            raise Gagal("Prive hanya untuk uang KELUAR (diambil pribadi). Uang pribadi yang dimasukkan ke usaha = "
                        "modal.")
        raise Gagal("Kategori %s hanya untuk uang %s. Untuk uang %s pilih kategori lain (mis. lain-lain)." %
                    (kat, "/".join(KATEGORI[kat][1]).upper(), arah.upper()))
    if kat != "prive" and arah == "keluar":
        m = POLA_PRIBADI.search(" " + normal(catatan) + " ")
        if m:
            peringatan.append("Catatan '%s' menyebut '%s' (keperluan pribadi?). Jika uang usaha dipakai untuk "
                              "keperluan pribadi, kategorinya prive, bukan %s." % (catatan, m.group(0).strip(), kat))
    metode = kode_metode(metode_teks) if metode_teks else None
    if metode == "pindah":
        raise Gagal("Untuk pindah dana antar akun pakai perintah: kas.py pindah --dari ... --ke ... --jumlah ...")
    if akun_teks:
        akun = cari_akun(conn, akun_teks)
        if not metode:
            metode = METODE_DEFAULT_AKUN[akun["jenis"]]
            asumsi.append("metode %s (dari jenis akun %s)" % (METODE[metode][0], akun["nama"]))
        elif metode == "tunai" and akun["jenis"] != "tunai":
            peringatan.append("Metode tunai tetapi akun %s bukan akun tunai; pastikan uangnya memang masuk/keluar "
                              "dari %s." % (akun["nama"], akun["nama"]))
    else:
        if not metode:
            metode = "tunai"
            asumsi.append("dibayar/diterima tunai (metode tidak disebut)")
        akun = akun_untuk_metode(conn, metode)
    if date.fromisoformat(akun["tanggal_awal"]) > tanggal:
        raise Gagal("Tanggal %s lebih awal dari saldo awal akun %s (%s). Ubah dulu tanggal saldo awal akun: kas.py "
                    "akun ubah --akun \"%s\" --tanggal-awal DD/MM/YYYY --saldo-awal ..." %
                    (tgl_id(tanggal), akun["nama"], tgl_id(akun["tanggal_awal"]), akun["nama"]))
    if jumlah >= NOMINAL_BESAR:
        peringatan.append("Nominal %s cukup besar; pastikan jumlah nolnya benar." % rp(jumlah))
    return {"tanggal": tanggal, "arah": arah, "jumlah": jumlah, "kategori": kat, "metode": metode,
            "akun": akun, "catatan": catatan}, asumsi, peringatan


def simpan_entri(conn, e, jenis="biasa", grup=None, sumber="manual", sidik=None):
    cur = conn.execute(
        "INSERT INTO transaksi(tanggal, arah, jumlah, kategori, metode, akun_id, catatan, jenis, grup, sumber, sidik, "
        "status, dibuat) VALUES (?,?,?,?,?,?,?,?,?,?,?, 'aktif', ?)",
        (e["tanggal"].isoformat(), e["arah"], e["jumlah"], e["kategori"], e["metode"], e["akun"]["id"],
         e["catatan"], jenis, grup, sumber, sidik, stempel()))
    return cur.lastrowid


def baris_entri(e, no=None, id_=None):
    arah = "MASUK " if e["arah"] == "masuk" else "KELUAR"
    t = "%s %s | %s | %s | %s -> %s" % (arah, rp(e["jumlah"]), tgl_id(e["tanggal"]), label_kat(e["kategori"], e["arah"]),
                                        METODE[e["metode"]][0], e["akun"]["nama"])
    if e["catatan"]:
        t += " | " + e["catatan"]
    if id_:
        t = "#%d %s" % (id_, t)
    if no:
        t = "%d. %s" % (no, t)
    return t


def urai_baris(teks):
    """'keluar;25rb;beli-stok;tunai;gas elpiji;laci;26/09/2026' -> dict. Kolom setelah jumlah boleh kosong."""
    bag = [b.strip() for b in str(teks).split(";")]
    if len(bag) < 2 or len(bag) > 7:
        raise Gagal("Format --baris salah: '%s'. Pakai: arah;jumlah;kategori;metode;catatan;akun;tanggal (minimal "
                    "arah;jumlah), mis. \"keluar;25rb;beli-stok;tunai;gas elpiji\"." % teks)
    bag += [""] * (7 - len(bag))
    arah = normal(bag[0])
    arah = {"masuk": "masuk", "in": "masuk", "terima": "masuk", "keluar": "keluar", "out": "keluar",
            "bayar": "keluar"}.get(arah, arah)
    return dict(zip(["arah", "jumlah", "kategori", "metode", "catatan", "akun", "tanggal"], [arah] + bag[1:]))


def ringkas_prive(conn, cfg, tanggal):
    """Status prive bulan berjalan s.d. tanggal: (data, [peringatan])."""
    awal = date(tanggal.year, tanggal.month, 1)
    r = hitung_rekap(conn, awal, tanggal)
    return r["prive"], r["hasil_usaha"], cek_prive(r["prive"], r["hasil_usaha"], cfg, "bulan ini (s.d. %s)" %
                                                   tgl_id(tanggal), r)


def cek_prive(prive, hasil, cfg, label, r=None):
    pr = []
    if prive <= 0:
        return pr
    if hasil <= 0:
        t = ("PERINGATAN PRIVE %s: hasil usaha %s, tetapi uang usaha diambil pribadi %s. Uang ini memakan modal/"
             "uang belanja stok." % (label, rp(hasil), rp(prive)))
        if r and r.get("per_kategori", {}).get("beli-stok", {}).get("keluar", 0) > 0:
            t += " (Hasil usaha bisa rendah karena belanja stok besar di awal; lihat rekap bulanan sebelum menyimpulkan.)"
        pr.append(t)
    elif prive > hasil:
        pr.append("PERINGATAN PRIVE %s: diambil pribadi %s, lebih besar dari hasil usaha %s (%s). Kelebihan %s "
                  "diambil dari modal usaha." % (label, rp(prive), rp(hasil), persen(prive, hasil), rp(prive - hasil)))
    batas = cfg.get("batas_prive")
    if batas and str(batas).isdigit() and int(batas) > 0 and prive > int(batas):
        pr.append("PERINGATAN PRIVE %s: %s melewati batas prive bulanan yang Anda tetapkan (%s)." %
                  (label, rp(prive), rp(int(batas))))
    return pr


# --------------------------------------------------------------------------- perintah: init / info / atur
def cmd_init(args):
    db = path_db(args)
    zona = kode_zona(args.zona or "WIB")
    _JAM["zona"] = zona
    rusak = False
    if db.exists():
        try:
            conn = buka(db, baca_saja=True)
            conn.close()
            raise Gagal("Buku kas sudah ada di %s. Tidak dibuat ulang (data aman). Untuk mengubah nama usaha/zona/"
                        "batas prive pakai: kas.py atur." % db, sudah_ada=True)
        except Gagal as e:
            if e.detail.get("sudah_ada") or "sedang dipakai" in e.pesan:
                raise
            if not e.detail.get("rusak"):
                raise Gagal("File %s sudah ada dan bukan buku kas kas-umkm; tidak ditimpa. Pakai --db lain." % db)
            if not args.mulai_baru:
                raise Gagal("Buku kas %s rusak. Pulihkan dari cadangan dulu: kas.py backup --daftar lalu kas.py "
                            "restore --dari <file>. Jika tidak ada cadangan: ulangi dengan --mulai-baru (file rusak "
                            "dipindah ke folder backup-kas, tidak dihapus)." % db, rusak=True)
            rusak = True
    kas_awal = parse_nominal(args.kas_awal, boleh_nol=True) if args.kas_awal else 0
    mulai = baca_tanggal(args.mulai) if args.mulai else hari_ini()
    batas = parse_nominal(args.batas_prive) if args.batas_prive else None
    nama = bersih(args.nama_usaha, 80)
    if not nama:
        raise Gagal("Nama usaha wajib diisi (--nama-usaha), dipakai sebagai judul rekap.")
    ringkas = ("Buku kas baru: %s\nNama usaha: %s | Zona: %s | Mulai: %s\nAkun awal: Laci kas (tunai), saldo awal %s "
               "per %s%s\nCadangan otomatis: %s" %
               (db, nama, zona, tgl_id(mulai), rp(kas_awal), tgl_id(mulai),
                ("\nBatas prive bulanan: %s" % rp(batas)) if batas else "", folder_backup(db)))
    if rusak:
        ringkas += "\nFile rusak yang ada sekarang dipindah (tidak dihapus) ke %s/rusak-kas-<waktu>.db." % folder_backup(db)
    if not args.ya:
        t = ("PRATINJAU (belum dibuat):\n" + ringkas + "\nRekening bank/e-wallet/QRIS ditambah setelah ini dengan "
             "kas.py akun tambah.\n\nBuat? Jalankan perintah yang sama + --ya setelah pengguna setuju.")
        return {"ok": True, "mode": "pratinjau", "perlu_konfirmasi": True, "db": str(db), "teks": t}, t
    db.parent.mkdir(parents=True, exist_ok=True)
    if rusak:
        pindahan = singkirkan(db, "rusak-kas-{}", pindah=True)
        ringkas += "\nFile rusak dipindah ke: %s" % pindahan
    conn = sqlite3.connect(str(db), isolation_level=None)
    try:
        conn.executescript("BEGIN;" + SKEMA_SQL + "COMMIT;")
        meta = {"aplikasi": APLIKASI, "skema": str(SKEMA), "versi_pembuat": VERSI, "dibuat": stempel(),
                "nama_usaha": nama, "zona": zona, "batas_prive": str(batas or ""), "mulai": mulai.isoformat()}
        conn.execute("BEGIN")
        conn.executemany("INSERT INTO meta(kunci, nilai) VALUES (?,?)", list(meta.items()))
        conn.execute("INSERT INTO akun(kode, nama, jenis, saldo_awal, tanggal_awal, terima_qris, dibuat) "
                     "VALUES ('laci', 'Laci kas', 'tunai', ?, ?, 0, ?)", (kas_awal, mulai.isoformat(), stempel()))
        conn.execute("COMMIT")
    finally:
        conn.close()
    t = "TERSIMPAN. Buku kas siap.\n" + ringkas
    return {"ok": True, "mode": "tersimpan", "perlu_konfirmasi": False, "db": str(db), "teks": t}, t


def cmd_info(args):
    db = path_db(args)
    if not db.exists():
        t = ("Buku kas belum ada (lokasi: %s). Mulai dengan: kas.py init --nama-usaha \"...\" --kas-awal ... "
             "(pratinjau, lalu --ya)." % db)
        return {"ok": True, "mode": "baca", "ada": False, "db": str(db), "teks": t}, t
    conn = buka(db, baca_saja=True)
    try:
        cfg = pengaturan(conn)
        hi = hari_ini()
        akun = []
        for a in semua_akun(conn):
            akun.append({"kode": a["kode"], "nama": a["nama"], "jenis": a["jenis"], "terima_qris": bool(a["terima_qris"]),
                         "saldo_awal": a["saldo_awal"], "tanggal_awal": a["tanggal_awal"],
                         "saldo": saldo_akhir_hari(conn, a, hi)})
        n = conn.execute("SELECT COUNT(*) FROM transaksi WHERE status='aktif'").fetchone()[0]
        terakhir = conn.execute("SELECT MAX(tanggal) FROM transaksi WHERE status='aktif'").fetchone()[0]
        op = conn.execute("SELECT MAX(tanggal) FROM opname").fetchone()[0]
    finally:
        conn.close()
    fol = folder_backup(db)
    bks = sorted(fol.glob("kas-*.db")) if fol.is_dir() else []
    t = ["Buku kas: %s" % db, "Usaha: %s | Zona: %s | Hari ini: %s" % (cfg["nama_usaha"] or "-", cfg["zona"],
                                                                       tgl_panjang(hi))]
    if cfg.get("batas_prive"):
        t.append("Batas prive bulanan: %s" % rp(int(cfg["batas_prive"])))
    t.append("Akun:")
    for a in akun:
        t.append("- %s (%s%s): saldo %s" % (a["nama"], LABEL_JENIS[a["jenis"]], ", penampung QRIS" if a["terima_qris"]
                                            else "", rp(a["saldo"])))
    t.append("Transaksi aktif: %d | Catatan terakhir: %s | Hitung laci terakhir: %s" %
             (n, tgl_id(terakhir) if terakhir else "-", tgl_id(op) if op else "belum pernah"))
    t.append("Cadangan: %d file di %s" % (len(bks), fol))
    t = "\n".join(t)
    return {"ok": True, "mode": "baca", "ada": True, "db": str(db), "pengaturan": cfg, "akun": akun,
            "jumlah_transaksi": n, "catatan_terakhir": terakhir, "opname_terakhir": op,
            "backup": [str(b) for b in bks[-5:]], "teks": t}, t


def cmd_atur(args):
    def kerja(conn, cfg):
        ubah = {}
        if args.nama_usaha:
            ubah["nama_usaha"] = bersih(args.nama_usaha, 80)
        if args.zona:
            ubah["zona"] = kode_zona(args.zona)
        if args.batas_prive:
            if normal(args.batas_prive) in ("hapus", "tidak", "tanpa", "0", "none"):
                ubah["batas_prive"] = ""
            else:
                ubah["batas_prive"] = str(parse_nominal(args.batas_prive))
        if not ubah:
            raise Gagal("Tidak ada yang diubah. Pakai --nama-usaha, --zona, atau --batas-prive (mis. 3jt, atau "
                        "'hapus').")
        for k, v in ubah.items():
            conn.execute("INSERT OR REPLACE INTO meta(kunci, nilai) VALUES (?,?)", (k, v))
        bag = []
        for k, v in ubah.items():
            if k == "batas_prive":
                bag.append("Batas prive bulanan: %s" % (rp(int(v)) if v else "tidak ada"))
            else:
                bag.append("%s: %s -> %s" % (k.replace("_", " ").capitalize(), cfg.get(k) or "-", v))
        return {"ringkasan": ubah, "teks": "\n".join(bag)}
    return jalankan_tulis(args, "atur", kerja)


# --------------------------------------------------------------------------- perintah: akun
def cmd_akun(args):
    if args.aksi == "daftar":
        db, conn = baca_db(args)
        try:
            hi = hari_ini()
            rows = [{"kode": a["kode"], "nama": a["nama"], "jenis": a["jenis"], "terima_qris": bool(a["terima_qris"]),
                     "saldo_awal": a["saldo_awal"], "tanggal_awal": a["tanggal_awal"],
                     "saldo": saldo_akhir_hari(conn, a, hi)} for a in semua_akun(conn)]
        finally:
            conn.close()
        t = "Akun (saldo per %s):\n" % tgl_id(hi) + "\n".join(
            "- %s [%s] %s%s: saldo %s (saldo awal %s per %s)" %
            (r["nama"], r["kode"], LABEL_JENIS[r["jenis"]], ", penampung QRIS" if r["terima_qris"] else "",
             rp(r["saldo"]), rp(r["saldo_awal"]), tgl_id(r["tanggal_awal"])) for r in rows)
        t += "\nTotal: %s" % rp(sum(r["saldo"] for r in rows))
        return {"ok": True, "mode": "baca", "akun": rows, "teks": t}, t

    def kerja_tambah(conn, cfg):
        nama = bersih(args.nama, 40)
        if not nama:
            raise Gagal("Nama akun wajib (--nama), mis. \"BRI\", \"GoPay\", \"Brankas\".")
        if not args.jenis:
            raise Gagal("Jenis akun wajib (--jenis tunai|bank|e-wallet).")
        jenis = kode_jenis_akun(args.jenis)
        kode = slug(args.kode or nama)
        if not kode:
            raise Gagal("Nama akun harus mengandung huruf/angka.")
        for a in semua_akun(conn):
            if a["kode"] == kode or normal(a["nama"]) == normal(nama):
                raise Gagal("Akun '%s' sudah ada. Ubah dengan: kas.py akun ubah --akun \"%s\"." % (nama, a["nama"]))
        saldo = parse_nominal(args.saldo_awal, boleh_nol=True) if args.saldo_awal else 0
        mulai = baca_tanggal(args.tanggal_awal) if args.tanggal_awal else hari_ini()
        qris = 1 if args.terima_qris else 0
        if qris and jenis == "tunai":
            raise Gagal("Uang QRIS masuk ke rekening bank/e-wallet, bukan ke laci. --terima-qris hanya untuk akun "
                        "bank/e-wallet.")
        peringatan = []
        if qris:
            lain = [a["nama"] for a in semua_akun(conn) if a["terima_qris"]]
            if lain:
                conn.execute("UPDATE akun SET terima_qris=0")
                peringatan.append("Penampung QRIS dipindah dari %s ke %s." % (", ".join(lain), nama))
        conn.execute("INSERT INTO akun(kode, nama, jenis, saldo_awal, tanggal_awal, terima_qris, dibuat) "
                     "VALUES (?,?,?,?,?,?,?)", (kode, nama, jenis, saldo, mulai.isoformat(), qris, stempel()))
        t = "Akun baru: %s [%s] (%s%s), saldo awal %s per %s." % (
            nama, kode, LABEL_JENIS[jenis], ", penampung QRIS" if qris else "", rp(saldo), tgl_id(mulai))
        return {"ringkasan": {"akun": kode}, "peringatan": peringatan, "teks": t}

    def kerja_ubah(conn, cfg):
        if not args.akun:
            raise Gagal("Sebut akun yang diubah: --akun \"...\".")
        a = cari_akun(conn, args.akun)
        bag, peringatan = [], []
        if args.nama:
            nama = bersih(args.nama, 40)
            for b in semua_akun(conn):
                if b["id"] != a["id"] and normal(b["nama"]) == normal(nama):
                    raise Gagal("Nama akun '%s' sudah dipakai." % nama)
            conn.execute("UPDATE akun SET nama=? WHERE id=?", (nama, a["id"]))
            bag.append("Nama: %s -> %s" % (a["nama"], nama))
        if args.saldo_awal:
            s = parse_nominal(args.saldo_awal, boleh_nol=True)
            conn.execute("UPDATE akun SET saldo_awal=? WHERE id=?", (s, a["id"]))
            bag.append("Saldo awal: %s -> %s" % (rp(a["saldo_awal"]), rp(s)))
        if args.tanggal_awal:
            d = baca_tanggal(args.tanggal_awal)
            pertama = conn.execute("SELECT MIN(tanggal) FROM transaksi WHERE akun_id=? AND status='aktif'",
                                   (a["id"],)).fetchone()[0]
            if pertama and date.fromisoformat(pertama) < d:
                raise Gagal("Sudah ada transaksi akun %s pada %s, sebelum %s. Tanggal saldo awal harus sama atau "
                            "lebih awal dari transaksi pertama." % (a["nama"], tgl_id(pertama), tgl_id(d)))
            conn.execute("UPDATE akun SET tanggal_awal=? WHERE id=?", (d.isoformat(), a["id"]))
            bag.append("Tanggal saldo awal: %s -> %s" % (tgl_id(a["tanggal_awal"]), tgl_id(d)))
        if args.terima_qris:
            if a["jenis"] == "tunai":
                raise Gagal("Akun tunai tidak bisa menjadi penampung QRIS.")
            conn.execute("UPDATE akun SET terima_qris=0")
            conn.execute("UPDATE akun SET terima_qris=1 WHERE id=?", (a["id"],))
            bag.append("%s menjadi penampung QRIS." % a["nama"])
        if not bag:
            raise Gagal("Tidak ada yang diubah. Pakai --nama, --saldo-awal, --tanggal-awal, atau --terima-qris.")
        blokir = blokir_minus(cari_minus(conn, [a["id"]], date(2000, 1, 1)))
        return {"ringkasan": {"akun": a["kode"]}, "peringatan": peringatan, "blokir": blokir,
                "teks": "Ubah akun %s:\n%s" % (a["nama"], "\n".join("- " + b for b in bag))}

    return jalankan_tulis(args, "akun " + args.aksi, kerja_tambah if args.aksi == "tambah" else kerja_ubah)


# --------------------------------------------------------------------------- perintah: catat / pindah / batal
def cmd_catat(args):
    def kerja(conn, cfg):
        mentah = []
        if args.baris:
            if args.masuk or args.keluar:
                raise Gagal("Pakai --baris ATAU --masuk/--keluar, jangan keduanya.")
            mentah = [urai_baris(b) for b in args.baris]
            for m in mentah:
                m["tanggal"] = m["tanggal"] or args.tanggal
        else:
            if bool(args.masuk) == bool(args.keluar):
                raise Gagal("Sebut satu: --masuk NOMINAL atau --keluar NOMINAL (atau beberapa --baris).")
            mentah = [{"arah": "masuk" if args.masuk else "keluar", "jumlah": args.masuk or args.keluar,
                       "kategori": args.kategori, "metode": args.metode, "catatan": args.catatan,
                       "akun": args.akun, "tanggal": args.tanggal}]
        entri, asumsi, peringatan, blokir = [], [], [], []
        for i, m in enumerate(mentah, 1):
            try:
                e, a, p = siapkan_entri(conn, m["arah"], m["jumlah"], m["kategori"], m["metode"], m["catatan"],
                                        m["akun"], m["tanggal"])
            except Gagal as g:
                if len(mentah) > 1:
                    raise Gagal("Baris %d: %s" % (i, g.pesan), **g.detail)
                raise
            entri.append(e)
            asumsi += [("baris %d: " % i if len(mentah) > 1 else "") + x for x in a]
            peringatan += p
        dobel = []
        for i, e in enumerate(entri, 1):
            ada = conn.execute("SELECT id FROM transaksi WHERE status='aktif' AND tanggal=? AND arah=? AND jumlah=? "
                               "AND akun_id=? AND kategori=?", (e["tanggal"].isoformat(), e["arah"], e["jumlah"],
                                                                e["akun"]["id"], e["kategori"])).fetchall()
            sama = [j for j, f in enumerate(entri, 1) if j < i and
                    (f["tanggal"], f["arah"], f["jumlah"], f["akun"]["id"], f["kategori"]) ==
                    (e["tanggal"], e["arah"], e["jumlah"], e["akun"]["id"], e["kategori"])]
            if ada:
                dobel.append("baris %d sama dengan catatan #%s yang sudah ada (%s %s %s)" %
                             (i, ", #".join(str(r[0]) for r in ada), tgl_id(e["tanggal"]), e["arah"], rp(e["jumlah"])))
            if sama:
                dobel.append("baris %d sama dengan baris %s di permintaan ini" % (i, ", ".join(map(str, sama))))
        if dobel:
            blokir.append({"opsi": "--izinkan-duplikat",
                           "pesan": "Kemungkinan tercatat DOBEL: " + "; ".join(dobel) + ". Tanyakan: ini transaksi "
                                    "berbeda atau dobel? Bila berbeda, ulangi dengan --izinkan-duplikat."})
        ids = [simpan_entri(conn, e) for e in entri]
        blokir += blokir_minus(cari_minus(conn, [e["akun"]["id"] for e in entri], min(e["tanggal"] for e in entri)))
        if any(e["kategori"] == "prive" for e in entri):
            tgl = max(e["tanggal"] for e in entri if e["kategori"] == "prive")
            prive, hasil, pr = ringkas_prive(conn, cfg, tgl)
            peringatan += pr
            if not pr:
                peringatan.append("Prive bulan ini s.d. %s: %s (hasil usaha %s)." % (tgl_id(tgl), rp(prive), rp(hasil)))
        hi = hari_ini()
        saldo = OrderedDict()
        for e in entri:
            a = akun_by_id(conn, e["akun"]["id"])
            saldo[a["nama"]] = saldo_akhir_hari(conn, a, hi)
        baris = [baris_entri(e, no=i if len(entri) > 1 else None, id_=ids[i - 1] if args.ya else None)
                 for i, e in enumerate(entri, 1)]
        t = "\n".join(baris)
        if asumsi:
            t += "\nAsumsi: " + "; ".join(asumsi) + "."
        t += "\nSaldo setelah dicatat: " + ", ".join("%s %s" % (k, rp(v)) for k, v in saldo.items())
        data = {"ringkasan": {"jumlah_entri": len(entri), "id": ids},
                "entri": [{"id": ids[i] if args.ya else None, "tanggal": e["tanggal"].isoformat(), "arah": e["arah"],
                           "jumlah": e["jumlah"], "kategori": e["kategori"], "metode": e["metode"],
                           "akun": e["akun"]["nama"], "catatan": e["catatan"]} for i, e in enumerate(entri)],
                "asumsi": asumsi, "saldo": saldo, "peringatan": peringatan, "blokir": blokir, "teks": t}
        return data
    return jalankan_tulis(args, "catat", kerja)


def cmd_pindah(args):
    def kerja(conn, cfg):
        dari, ke = cari_akun(conn, args.dari), cari_akun(conn, args.ke)
        if dari["id"] == ke["id"]:
            raise Gagal("Akun asal dan tujuan sama (%s)." % dari["nama"])
        jumlah = parse_nominal(args.jumlah)
        tanggal = baca_tanggal(args.tanggal) if args.tanggal else hari_ini()
        for a in (dari, ke):
            if date.fromisoformat(a["tanggal_awal"]) > tanggal:
                raise Gagal("Tanggal %s lebih awal dari saldo awal akun %s (%s)." %
                            (tgl_id(tanggal), a["nama"], tgl_id(a["tanggal_awal"])))
        catatan = bersih(args.catatan or "", 150)
        grup = "P%s-%s" % (tanggal.strftime("%y%m%d"), hashlib.sha1(("%s%s%s%s" % (stempel(), dari["id"], ke["id"], jumlah)
                                                                     ).encode()).hexdigest()[:6])
        ket = "Pindah dana %s -> %s%s" % (dari["nama"], ke["nama"], (": " + catatan) if catatan else "")
        base = {"tanggal": tanggal, "jumlah": jumlah, "kategori": "pindah", "metode": "pindah", "catatan": ket}
        id1 = simpan_entri(conn, dict(base, arah="keluar", akun=dari), jenis="pindah", grup=grup)
        id2 = simpan_entri(conn, dict(base, arah="masuk", akun=ke), jenis="pindah", grup=grup)
        t = "%s %s pada %s (tidak mengubah hasil usaha)." % (ket, rp(jumlah), tgl_id(tanggal))
        ids = [id1, id2]
        if args.biaya:
            biaya = parse_nominal(args.biaya)
            e = {"tanggal": tanggal, "arah": "keluar", "jumlah": biaya, "kategori": "lain-lain",
                 "metode": METODE_DEFAULT_AKUN[dari["jenis"]], "akun": dari,
                 "catatan": "biaya admin transfer %s -> %s" % (dari["nama"], ke["nama"])}
            ids.append(simpan_entri(conn, e, grup=grup))
            t += "\nBiaya admin %s dicatat sebagai pengeluaran lain-lain dari %s." % (rp(biaya), dari["nama"])
        hi = hari_ini()
        t += "\nSaldo setelah dicatat: %s %s, %s %s" % (dari["nama"], rp(saldo_akhir_hari(conn, akun_by_id(conn, dari["id"]), hi)),
                                                       ke["nama"], rp(saldo_akhir_hari(conn, akun_by_id(conn, ke["id"]), hi)))
        blokir = blokir_minus(cari_minus(conn, [dari["id"]], tanggal))
        return {"ringkasan": {"grup": grup, "id": ids}, "grup": grup, "id": ids if args.ya else [], "blokir": blokir,
                "teks": t}
    return jalankan_tulis(args, "pindah", kerja)


def cmd_batal(args):
    def kerja(conn, cfg):
        m = re.fullmatch(r"#?\s*(\d+)", str(args.id).strip())
        if not m:
            raise Gagal("ID '%s' tidak valid. Lihat ID di kas.py daftar (mis. #12)." % args.id)
        r = conn.execute("SELECT t.*, a.nama AS akun_nama FROM transaksi t JOIN akun a ON a.id=t.akun_id WHERE t.id=?",
                         (int(m.group(1)),)).fetchone()
        if not r:
            raise Gagal("Catatan #%s tidak ditemukan. Lihat kas.py daftar." % m.group(1))
        if r["status"] != "aktif":
            raise Gagal("Catatan #%d sudah dibatalkan sebelumnya (%s)." % (r["id"], r["alasan_batal"] or "-"))
        alasan = bersih(args.alasan, 150)
        if not alasan:
            raise Gagal("Alasan pembatalan wajib (--alasan), mis. \"salah ketik nominal\".")
        if r["jenis"] == "pindah" and r["grup"]:
            rows = conn.execute("SELECT t.*, a.nama AS akun_nama FROM transaksi t JOIN akun a ON a.id=t.akun_id "
                                "WHERE t.grup=? AND t.status='aktif'", (r["grup"],)).fetchall()
        else:
            rows = [r]
        for x in rows:
            conn.execute("UPDATE transaksi SET status='batal', alasan_batal=? WHERE id=?", (alasan, x["id"]))
        conn.execute("UPDATE opname SET disesuaikan=0 WHERE transaksi_id IN (%s)" % ",".join(str(x["id"]) for x in rows))
        t = "Dibatalkan (tidak dihapus, tetap ada di riwayat):\n" + "\n".join(
            "#%d %s %s | %s | %s | %s | %s" % (x["id"], x["arah"].upper(), rp(x["jumlah"]), tgl_id(x["tanggal"]),
                                               label_kat(x["kategori"], x["arah"]), x["akun_nama"], x["catatan"])
            for x in rows) + "\nAlasan: %s" % alasan
        tmin = min(date.fromisoformat(x["tanggal"]) for x in rows)
        blokir = blokir_minus(cari_minus(conn, [x["akun_id"] for x in rows], tmin))
        return {"ringkasan": {"batal": [x["id"] for x in rows], "alasan": alasan},
                "dibatalkan": [x["id"] for x in rows], "blokir": blokir, "teks": t}
    return jalankan_tulis(args, "batal", kerja)


# --------------------------------------------------------------------------- perintah: opname (hitung laci)
def urai_pecahan(teks):
    """'100rb x5, 50rb x3, 2rb x10, koin 3.500' -> (total, rincian, peringatan)."""
    total, rincian, pr = 0, [], []
    for seg in [s.strip() for s in re.split(r"[,;\n]+(?![0-9]{3}\b)", str(teks)) if s.strip()]:
        s = seg.lower()
        m = (re.fullmatch(r"(.+?)\s*[x\*×]\s*(\d+)\s*(lembar|lbr|keping|kpg|buah)?", s) or
             re.fullmatch(r"(\d+)\s*(lembar|lbr|keping|kpg|buah)?\s*[x\*×]?\s*(.+)", s))
        if re.match(r"^(koin|receh|recehan|uang kecil|lainnya|sisa)\b", s):
            n = parse_nominal(re.sub(r"^(koin|receh|recehan|uang kecil|lainnya|sisa)\s*", "", s) or "0", boleh_nol=True)
            total += n
            rincian.append({"pecahan": "receh/koin", "jumlah": 1, "nilai": n})
            continue
        if not m:
            raise Gagal("Rincian uang '%s' tidak dikenali. Contoh: \"100rb x5, 50rb x3, 2rb x10, koin 3.500\"." % seg)
        if m.re.pattern.startswith("(.+?)"):
            nom, qty = m.group(1), int(m.group(2))
        else:
            qty, nom = int(m.group(1)), m.group(3)
        nilai = parse_nominal(nom)
        if nilai not in PECAHAN_SAH:
            pr.append("Pecahan %s tidak lazim; periksa lagi." % rp(nilai))
        total += nilai * qty
        rincian.append({"pecahan": nilai, "jumlah": qty, "nilai": nilai * qty})
    if not rincian:
        raise Gagal("Rincian uang kosong.")
    return total, rincian, pr


PENYEBAB_KURANG = ["kembalian terlalu banyak", "pengeluaran kecil dari laci belum dicatat (es batu, parkir, dll.)",
                   "uang diambil untuk keperluan pribadi tanpa dicatat (prive)",
                   "pembayaran QRIS/transfer tercatat sebagai tunai", "salah hitung uang"]
PENYEBAB_LEBIH = ["penjualan tunai belum dicatat", "kembalian kurang diberikan ke pembeli",
                  "uang pribadi/modal dimasukkan ke laci tanpa dicatat", "pengeluaran tercatat padahal dibayar dari "
                  "rekening lain", "salah hitung uang"]


def cmd_opname(args):
    if args.daftar:
        db, conn = baca_db(args)
        try:
            rows = conn.execute("SELECT o.*, a.nama AS akun_nama FROM opname o JOIN akun a ON a.id=o.akun_id "
                                "ORDER BY o.tanggal DESC, o.id DESC LIMIT ?", (args.maks,)).fetchall()
        finally:
            conn.close()
        data = [{"id": r["id"], "tanggal": r["tanggal"], "akun": r["akun_nama"], "saldo_buku": r["saldo_buku"],
                 "fisik": r["fisik"], "selisih": r["selisih"], "ditandai": r["selisih"] != 0,
                 "disesuaikan": bool(r["disesuaikan"]), "catatan": r["catatan"]} for r in rows]
        t = "Riwayat hitung uang fisik (terbaru di atas):\n" + ("\n".join(
            "%s %s: buku %s, fisik %s -> %s%s" % (tgl_id(d["tanggal"]), d["akun"], rp(d["saldo_buku"]), rp(d["fisik"]),
                                                   "PAS" if not d["selisih"] else "SELISIH %s %s" %
                                                   ("LEBIH" if d["selisih"] > 0 else "KURANG", rp(abs(d["selisih"]))),
                                                   " (disesuaikan)" if d["disesuaikan"] else "")
            for d in data) or "belum ada")
        return {"ok": True, "mode": "baca", "opname": data, "teks": t}, t

    def kerja(conn, cfg):
        if args.akun:
            a = cari_akun(conn, args.akun)
        else:
            tunai = [x for x in semua_akun(conn) if x["jenis"] == "tunai"]
            if len(tunai) != 1:
                raise Gagal("Sebut akun yang dihitung dengan --akun (ada %d akun tunai)." % len(tunai))
            a = tunai[0]
        if bool(args.fisik) == bool(args.pecahan):
            raise Gagal("Isi salah satu: --fisik (total uang yang dihitung) atau --pecahan (\"100rb x5, 50rb x3, "
                        "koin 3.500\").")
        pr, rincian = [], None
        if args.pecahan:
            fisik, rincian, pr = urai_pecahan(args.pecahan)
        else:
            fisik = parse_nominal(args.fisik, boleh_nol=True)
        tanggal = baca_tanggal(args.tanggal) if args.tanggal else hari_ini()
        if date.fromisoformat(a["tanggal_awal"]) > tanggal:
            raise Gagal("Tanggal %s lebih awal dari saldo awal akun %s." % (tgl_id(tanggal), a["nama"]))
        buku = saldo_akhir_hari(conn, a, tanggal)
        selisih = fisik - buku
        catatan = bersih(args.catatan or "", 150)
        t = ["Hitung uang %s, %s" % (a["nama"], tgl_panjang(tanggal)),
             "Menurut buku : %s" % rp(buku), "Uang dihitung: %s" % rp(fisik)]
        if rincian:
            t.append("Rincian: " + ", ".join(("%s x%d" % (rp(r["pecahan"]), r["jumlah"])) if r["pecahan"] != "receh/koin"
                                              else "receh %s" % rp(r["nilai"]) for r in rincian))
        tid = None
        if selisih == 0:
            t.append("Hasil: PAS, tidak ada selisih.")
        else:
            arah_s = "LEBIH" if selisih > 0 else "KURANG"
            t.append("Hasil: SELISIH %s %s (ditandai)." % (arah_s, rp(abs(selisih))))
            t.append("Kemungkinan penyebab (cek dulu, jangan menuduh siapa pun): " +
                     "; ".join(PENYEBAB_LEBIH if selisih > 0 else PENYEBAB_KURANG) + ".")
            if args.sesuaikan:
                e = {"tanggal": tanggal, "arah": "masuk" if selisih > 0 else "keluar", "jumlah": abs(selisih),
                     "kategori": "selisih-kas", "metode": METODE_DEFAULT_AKUN[a["jenis"]], "akun": a,
                     "catatan": "Penyesuaian hitung uang %s: selisih %s" % (a["nama"], arah_s.lower())}
                tid = simpan_entri(conn, e, jenis="penyesuaian")
                t.append("Buku DISESUAIKAN: dicatat %s %s (kategori selisih hitung laci), saldo buku jadi %s." %
                         ("masuk" if selisih > 0 else "keluar", rp(abs(selisih)), rp(fisik)))
            else:
                t.append("Buku belum disesuaikan. Jika penyebabnya ketemu, catat transaksi yang terlewat. Jika tidak "
                         "ketemu dan pengguna setuju, ulangi dengan --sesuaikan agar saldo buku = uang fisik.")
        if tanggal == hari_ini():
            t.append("Pastikan semua transaksi hari ini sudah dicatat sebelum menghitung.")
        conn.execute("INSERT INTO opname(tanggal, akun_id, saldo_buku, fisik, selisih, rincian, disesuaikan, "
                     "transaksi_id, catatan, dibuat) VALUES (?,?,?,?,?,?,?,?,?,?)",
                     (tanggal.isoformat(), a["id"], buku, fisik, selisih,
                      json.dumps(rincian, ensure_ascii=False) if rincian else None, 1 if tid else 0, tid, catatan,
                      stempel()))
        return {"ringkasan": {"akun": a["kode"], "selisih": selisih}, "akun": a["nama"], "tanggal": tanggal.isoformat(),
                "saldo_buku": buku, "fisik": fisik, "selisih": selisih, "ditandai": selisih != 0,
                "status": "pas" if not selisih else ("lebih" if selisih > 0 else "kurang"),
                "disesuaikan": bool(tid), "rincian": rincian, "peringatan": pr, "teks": "\n".join(t)}
    return jalankan_tulis(args, "opname", kerja)


# --------------------------------------------------------------------------- rekap
def kelompok(kat):
    return SEMUA_KATEGORI[kat][2]


def hitung_rekap(conn, dari, sampai):
    rows = conn.execute("SELECT t.*, a.nama AS akun_nama FROM transaksi t JOIN akun a ON a.id=t.akun_id "
                        "WHERE t.status='aktif' AND t.tanggal BETWEEN ? AND ? ORDER BY t.tanggal, t.id",
                        (dari.isoformat(), sampai.isoformat())).fetchall()
    r = {"masuk": 0, "keluar": 0, "usaha_masuk": 0, "usaha_keluar": 0, "hasil_usaha": 0, "prive": 0, "modal": 0,
         "pinjaman_masuk": 0, "pinjaman_keluar": 0, "per_kategori": OrderedDict(), "per_metode": OrderedDict(),
         "per_hari": OrderedDict(), "pindah": [], "terbesar": [], "jumlah_transaksi": 0}
    grup_pindah = OrderedDict()
    for x in rows:
        if x["kategori"] == "pindah":
            g = grup_pindah.setdefault(x["grup"] or ("#%d" % x["id"]), {"tanggal": x["tanggal"], "jumlah": x["jumlah"],
                                                                          "dari": None, "ke": None})
            g["dari" if x["arah"] == "keluar" else "ke"] = x["akun_nama"]
            continue
        r["jumlah_transaksi"] += 1
        j = x["jumlah"]
        r[x["arah"]] += j
        k = r["per_kategori"].setdefault(x["kategori"], {"masuk": 0, "keluar": 0, "n": 0})
        k[x["arah"]] += j
        k["n"] += 1
        mt = r["per_metode"].setdefault(x["metode"], {"masuk": 0, "keluar": 0})
        mt[x["arah"]] += j
        h = r["per_hari"].setdefault(x["tanggal"], {"masuk": 0, "keluar": 0, "hasil_usaha": 0})
        h[x["arah"]] += j
        kel = kelompok(x["kategori"])
        if kel == "usaha":
            r["usaha_" + x["arah"]] += j
            h["hasil_usaha"] += j if x["arah"] == "masuk" else -j
        elif x["kategori"] == "prive":
            r["prive"] += j
        elif x["kategori"] == "modal":
            r["modal"] += j
        elif x["kategori"] == "pinjaman":
            r["pinjaman_" + x["arah"]] += j
        if x["arah"] == "keluar":
            r["terbesar"].append({"id": x["id"], "tanggal": x["tanggal"], "jumlah": j, "kategori": x["kategori"],
                                  "catatan": x["catatan"], "akun": x["akun_nama"]})
    r["hasil_usaha"] = r["usaha_masuk"] - r["usaha_keluar"]
    r["terbesar"] = sorted(r["terbesar"], key=lambda z: (-z["jumlah"], z["tanggal"], z["id"]))[:5]
    r["pindah"] = list(grup_pindah.values())
    urut = list(SEMUA_KATEGORI)
    r["per_kategori"] = OrderedDict(sorted(r["per_kategori"].items(), key=lambda kv: urut.index(kv[0])))
    return r


def saldo_periode(conn, dari, sampai):
    batas = min(sampai, hari_ini())
    hasil = []
    for a in semua_akun(conn):
        mulai = date.fromisoformat(a["tanggal_awal"])
        if mulai > batas:
            continue
        hasil.append({"akun": a["nama"], "kode": a["kode"], "jenis": a["jenis"], "awal": saldo_pembuka(conn, a, dari),
                      "akhir": saldo_akhir_hari(conn, a, batas), "mulai_di_periode": mulai > dari})
    return hasil, batas


def judul_periode(dari, sampai, jenis):
    if jenis == "hari":
        return "Rekap harian %s" % tgl_panjang(dari)
    if jenis == "minggu":
        return "Rekap mingguan %s - %s" % (tgl_id(dari), tgl_id(sampai))
    if jenis == "bulan":
        return "Rekap bulanan %s %d" % (BULAN[dari.month - 1], dari.year)
    return "Rekap %s - %s" % (tgl_id(dari), tgl_id(sampai))


def cmd_rekap(args):
    db, conn = baca_db(args)
    try:
        cfg = pengaturan(conn)
        dari, sampai, jenis = ambil_periode(args)
        r = hitung_rekap(conn, dari, sampai)
        saldo, batas = saldo_periode(conn, dari, sampai)
        minus = cari_minus(conn, [a["id"] for a in semua_akun(conn)], dari)
        minus = [m for m in minus if date.fromisoformat(m["tanggal"]) <= sampai]
        ops = conn.execute("SELECT o.*, a.nama AS akun_nama FROM opname o JOIN akun a ON a.id=o.akun_id WHERE "
                           "o.tanggal BETWEEN ? AND ? ORDER BY o.tanggal, o.id",
                           (dari.isoformat(), sampai.isoformat())).fetchall()
        op_akhir = conn.execute("SELECT MAX(o.tanggal) FROM opname o JOIN akun a ON a.id=o.akun_id "
                                "WHERE a.jenis='tunai'").fetchone()[0]
        peringatan = []
        if jenis == "bulan" or (jenis == "rentang" and dari.day == 1 and sampai == akhir_bulan(dari)):
            peringatan += cek_prive(r["prive"], r["hasil_usaha"], cfg, "periode ini", r)
        else:
            if r["prive"] and jenis != "hari":
                peringatan += [p for p in cek_prive(r["prive"], r["hasil_usaha"], cfg, "periode ini", r)
                               if "batas prive" not in p]
            if dari <= hari_ini():
                acuan = min(sampai, hari_ini())
                _, _, pr = ringkas_prive(conn, cfg, acuan)
                peringatan += pr
        for m in minus:
            peringatan.append("SALDO MINUS: %s %s pada akhir %s. Ada uang masuk yang belum dicatat atau salah catat." %
                              (m["akun"], rp(m["saldo"]), tgl_id(m["tanggal"])))
        selisih_op = [o for o in ops if o["selisih"]]
        if jenis == "hari" and any(a["jenis"] == "tunai" for a in semua_akun(conn)):
            if not op_akhir or (dari - date.fromisoformat(op_akhir)).days > 7:
                peringatan.append("Saran: uang laci belum dihitung %s. Hitung uang fisik (kas.py opname) minimal "
                                  "seminggu sekali." % ("sejak " + tgl_id(op_akhir) if op_akhir else "sama sekali"))
    finally:
        conn.close()
    total_awal = sum(s["awal"] for s in saldo)
    total_akhir = sum(s["akhir"] for s in saldo)
    t = ["BUKU KAS %s" % (cfg["nama_usaha"] or ""), judul_periode(dari, sampai, jenis)]
    if not r["jumlah_transaksi"] and not r["pindah"]:
        t.append("Belum ada catatan uang masuk/keluar di periode ini.")
    else:
        t.append("")
        t.append("UANG MASUK: %s" % rp(r["masuk"]))
        for k, v in r["per_kategori"].items():
            if v["masuk"]:
                t.append("- %s: %s" % (label_kat(k, "masuk") if k != "penjualan" else "Penjualan", rp(v["masuk"])))
        t.append("UANG KELUAR: %s" % rp(r["keluar"]))
        for k, v in r["per_kategori"].items():
            if v["keluar"]:
                t.append("- %s: %s" % (label_kat(k, "keluar"), rp(v["keluar"])))
        t.append("")
        t.append("HASIL USAHA (masuk usaha - keluar usaha): %s" % rp(r["hasil_usaha"]))
        t.append("  (tidak termasuk modal, pinjaman, prive, dan pindah dana; ini hitungan kas, bukan laba akuntansi)")
        if r["prive"]:
            t.append("Prive (ambil pribadi): %s%s" % (rp(r["prive"]), (" = %s dari hasil usaha" % persen(r["prive"], r["hasil_usaha"]))
                                                     if r["hasil_usaha"] > 0 else ""))
        if r["per_metode"]:
            t.append("Per metode: " + "; ".join("%s masuk %s keluar %s" % (METODE[m][0], rp(v["masuk"]), rp(v["keluar"]))
                                               for m, v in r["per_metode"].items()))
        for p in r["pindah"]:
            t.append("Pindah dana %s: %s -> %s %s" % (tgl_id(p["tanggal"]), p["dari"] or "?", p["ke"] or "?", rp(p["jumlah"])))
        if jenis == "minggu" or (jenis == "rentang" and (sampai - dari).days <= 13):
            t.append("")
            t.append("Per hari:")
            d = dari
            while d <= sampai:
                h = r["per_hari"].get(d.isoformat())
                if h:
                    t.append("%s %s: masuk %s, keluar %s, hasil usaha %s" % (HR[d.weekday()], tgl_id(d)[:5], rp(h["masuk"]),
                                                                            rp(h["keluar"]), rp(h["hasil_usaha"])))
                d += timedelta(days=1)
        if jenis in ("bulan", "rentang") and (sampai - dari).days > 13:
            t.append("")
            t.append("Per minggu:")
            w = senin(dari)
            while w <= sampai:
                a_, b_ = max(w, dari), min(w + timedelta(days=6), sampai)
                ms = sum(v["masuk"] for k, v in r["per_hari"].items() if a_.isoformat() <= k <= b_.isoformat())
                kl = sum(v["keluar"] for k, v in r["per_hari"].items() if a_.isoformat() <= k <= b_.isoformat())
                hu = sum(v["hasil_usaha"] for k, v in r["per_hari"].items() if a_.isoformat() <= k <= b_.isoformat())
                if ms or kl:
                    t.append("%s-%s: masuk %s, keluar %s, hasil usaha %s" % (tgl_id(a_)[:5], tgl_id(b_)[:5], rp(ms),
                                                                             rp(kl), rp(hu)))
                w += timedelta(days=7)
        if jenis != "hari" and r["terbesar"]:
            t.append("")
            t.append("Pengeluaran terbesar:")
            for i, z in enumerate(r["terbesar"], 1):
                t.append("%d. %s %s %s%s" % (i, tgl_id(z["tanggal"])[:5], rp(z["jumlah"]), label_kat(z["kategori"], "keluar"),
                                             (" - " + z["catatan"]) if z["catatan"] else ""))
    t.append("")
    t.append("SALDO per akhir %s:" % tgl_id(batas))
    for s in saldo:
        t.append("- %s: %s" % (s["akun"], rp(s["akhir"])))
    t.append("Total: %s (awal periode %s, %s %s)" % (rp(total_akhir), rp(total_awal),
                                                     "naik" if total_akhir >= total_awal else "turun",
                                                     rp(abs(total_akhir - total_awal))))
    for o in ops:
        t.append("Hitung %s %s: buku %s, fisik %s -> %s" % (o["akun_nama"], tgl_id(o["tanggal"])[:5], rp(o["saldo_buku"]),
                                                            rp(o["fisik"]), "PAS" if not o["selisih"] else "SELISIH %s %s%s" %
                                                            ("LEBIH" if o["selisih"] > 0 else "KURANG", rp(abs(o["selisih"])),
                                                             " (disesuaikan)" if o["disesuaikan"] else "")))
    if peringatan:
        t.append("")
        t += peringatan
    teks = "\n".join(t)
    cek = (total_akhir - total_awal) == sum(v["masuk"] - v["keluar"] for k, v in r["per_hari"].items()
                                             if k <= batas.isoformat())
    data = {"ok": True, "mode": "baca", "periode": {"dari": dari.isoformat(), "sampai": sampai.isoformat(), "jenis": jenis},
            "nama_usaha": cfg["nama_usaha"], "masuk": r["masuk"], "keluar": r["keluar"], "hasil_usaha": r["hasil_usaha"],
            "usaha_masuk": r["usaha_masuk"], "usaha_keluar": r["usaha_keluar"], "prive": r["prive"], "modal": r["modal"],
            "pinjaman_masuk": r["pinjaman_masuk"], "pinjaman_keluar": r["pinjaman_keluar"],
            "per_kategori": r["per_kategori"], "per_metode": r["per_metode"], "per_hari": r["per_hari"],
            "pindah": r["pindah"], "pengeluaran_terbesar": r["terbesar"], "saldo": saldo, "saldo_per": batas.isoformat(),
            "total_saldo_awal": total_awal, "total_saldo_akhir": total_akhir, "cek_saldo_cocok": cek,
            "opname": [{"tanggal": o["tanggal"], "akun": o["akun_nama"], "saldo_buku": o["saldo_buku"], "fisik": o["fisik"],
                        "selisih": o["selisih"], "ditandai": o["selisih"] != 0, "disesuaikan": bool(o["disesuaikan"])}
                       for o in ops],
            "opname_selisih": len(selisih_op), "saldo_minus": minus, "peringatan": peringatan, "teks": teks}
    return data, teks


def cmd_saldo(args):
    db, conn = baca_db(args)
    try:
        d = baca_tanggal(args.tanggal) if args.tanggal else hari_ini()
        rows = []
        for a in semua_akun(conn):
            if date.fromisoformat(a["tanggal_awal"]) > d:
                continue
            rows.append({"akun": a["nama"], "kode": a["kode"], "jenis": a["jenis"], "saldo": saldo_akhir_hari(conn, a, d)})
        minus = [m for m in cari_minus(conn, [a["id"] for a in semua_akun(conn)], date(2000, 1, 1))
                 if date.fromisoformat(m["tanggal"]) <= d]
    finally:
        conn.close()
    t = ["Saldo per akhir %s:" % tgl_panjang(d)] + ["- %s: %s" % (r["akun"], rp(r["saldo"])) for r in rows]
    t.append("Total: %s" % rp(sum(r["saldo"] for r in rows)))
    for m in minus:
        t.append("PERINGATAN: saldo %s pernah minus %s pada %s." % (m["akun"], rp(m["saldo"]), tgl_id(m["tanggal"])))
    t = "\n".join(t)
    return {"ok": True, "mode": "baca", "tanggal": d.isoformat(), "saldo": rows, "total": sum(r["saldo"] for r in rows),
            "saldo_minus": minus, "teks": t}, t


def cmd_daftar(args):
    db, conn = baca_db(args)
    try:
        dari, sampai, jenis = ambil_periode(args)
        q = ("SELECT t.*, a.nama AS akun_nama FROM transaksi t JOIN akun a ON a.id=t.akun_id WHERE t.tanggal BETWEEN ? "
             "AND ?")
        p = [dari.isoformat(), sampai.isoformat()]
        if not args.semua:
            q += " AND t.status='aktif'"
        if args.kategori:
            k = kode_kategori(args.kategori) or ("pindah" if normal(args.kategori) == "pindah" else None)
            if not k:
                raise Gagal("Kategori '%s' tidak dikenal." % args.kategori)
            q += " AND t.kategori=?"
            p.append(k)
        if args.akun:
            q += " AND t.akun_id=?"
            p.append(cari_akun(conn, args.akun)["id"])
        if args.cari:
            q += " AND LOWER(t.catatan) LIKE ?"
            p.append("%" + args.cari.lower() + "%")
        rows = conn.execute(q + " ORDER BY t.tanggal, t.id", p).fetchall()
    finally:
        conn.close()
    lebih = max(0, len(rows) - args.maks)
    tampil = rows[-args.maks:] if lebih else rows
    data = [{"id": r["id"], "tanggal": r["tanggal"], "arah": r["arah"], "jumlah": r["jumlah"], "kategori": r["kategori"],
             "metode": r["metode"], "akun": r["akun_nama"], "catatan": r["catatan"], "jenis": r["jenis"],
             "sumber": r["sumber"], "status": r["status"], "alasan_batal": r["alasan_batal"]} for r in tampil]
    t = ["Catatan kas %s - %s (%d%s):" % (tgl_id(dari), tgl_id(sampai), len(rows),
                                          ", %d terlama tidak ditampilkan" % lebih if lebih else "")]
    for d in data:
        t.append("#%d %s %s %s | %s | %s | %s%s%s" % (
            d["id"], tgl_id(d["tanggal"])[:5], "MASUK " if d["arah"] == "masuk" else "KELUAR", rp(d["jumlah"]),
            label_kat(d["kategori"], d["arah"]), d["akun"], d["catatan"],
            " [%s]" % d["sumber"] if d["sumber"] != "manual" else "",
            " [BATAL: %s]" % d["alasan_batal"] if d["status"] == "batal" else ""))
    if not data:
        t.append("(kosong)")
    t = "\n".join(t)
    return {"ok": True, "mode": "baca", "jumlah": len(rows), "transaksi": data, "teks": t}, t


# --------------------------------------------------------------------------- CSV
def sel_aman(v):
    """Cegah formula injection saat dibuka di Excel/Sheets (teks diawali = + - @ tab CR)."""
    if isinstance(v, (int, Decimal)):
        return v
    s = str(v if v is not None else "")
    if re.fullmatch(r"-?\d+(?:[.,]\d+)?", s):
        return s
    if s and s[0] in "=+-@\t\r":
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
    return str(p.resolve())


def baca_teks_file(path):
    p = Path(path).expanduser()
    if not p.is_file():
        raise Gagal("File %s tidak ditemukan." % path)
    if p.suffix.lower() in (".xlsx", ".xls", ".ods", ".pdf"):
        raise Gagal("File %s belum didukung langsung. Excel: File > Save As > CSV (UTF-8). Mutasi PDF: unduh versi "
                    "CSV/Excel dari internet banking, atau salin tabelnya ke CSV." % p.suffix)
    raw = p.read_bytes()
    if not raw.strip():
        raise Gagal("File %s kosong." % path)
    if b"\x00" in raw[:2000] and not raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        raise Gagal("File %s bukan file teks/CSV (berisi data biner)." % path)
    pr = []
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        teks = raw.decode("utf-16")
    else:
        try:
            teks = raw.decode("utf-8-sig")
        except UnicodeDecodeError:
            teks = raw.decode("cp1252", errors="replace")
            pr.append("File bukan UTF-8; dibaca sebagai Windows-1252 (Excel lama). Cek ejaan keterangan.")
    return teks.lstrip("\ufeff"), pr


def baca_csv(path):
    teks, pr = baca_teks_file(path)
    contoh = [b for b in teks.splitlines() if b.strip()][:20]
    pemisah = max([";", ",", "\t", "|"], key=lambda c: sum(b.count(c) for b in contoh))
    if not any(b.count(pemisah) for b in contoh):
        raise Gagal("File %s tidak berbentuk tabel (tidak ada pemisah kolom ; , tab atau |)." % path)
    rows = list(csv.reader(io.StringIO(teks), delimiter=pemisah))
    return rows, pr


PERAN_KOLOM = OrderedDict([
    ("tanggal", ["tanggal", "tgl", "date", "tanggal transaksi", "tgl transaksi", "waktu", "tanggal waktu",
                 "posting date", "transaction date"]),
    ("keterangan", ["keterangan", "ket", "uraian", "deskripsi", "description", "catatan", "transaksi",
                    "rincian", "detail", "memo", "uraian transaksi", "keterangan transaksi", "remark", "berita"]),
    ("masuk", ["masuk", "uang masuk", "pemasukan", "penerimaan", "kas masuk", "income", "dana masuk", "credit in"]),
    ("keluar", ["keluar", "uang keluar", "pengeluaran", "kas keluar", "expense", "dana keluar", "debit out"]),
    ("debit", ["debit", "debet", "db", "mutasi debet", "mutasi debit"]),
    ("kredit", ["kredit", "credit", "cr", "mutasi kredit"]),
    ("jumlah", ["jumlah", "nominal", "nilai", "amount", "mutasi", "rp", "jumlah rp", "nominal rp"]),
    ("jenis", ["jenis", "arah", "tipe", "type", "db cr", "d k", "cr db", "masuk keluar", "debit kredit"]),
    ("kategori", ["kategori", "category", "pos", "kelompok"]),
    ("metode", ["metode", "metode bayar", "cara bayar", "pembayaran", "metode pembayaran"]),
    ("akun", ["akun", "rekening", "dompet", "sumber dana"]),
])


def peran_header(h):
    n = normal(h)
    for peran, alias in PERAN_KOLOM.items():
        if n in alias:
            return peran
    return None


def cari_header(rows):
    for i, r in enumerate(rows[:15]):
        peran = [peran_header(c) for c in r]
        ada = {p for p in peran if p}
        if "tanggal" in ada and len(ada) >= 2:
            peta = {}
            for j, p in enumerate(peran):
                if p and p not in peta:
                    peta[p] = j
            return i, peta
    raise Gagal("Judul kolom tidak dikenali. Minimal perlu kolom Tanggal dan nominal (Masuk/Keluar, Debit/Kredit, "
                "atau Jumlah + Jenis). Contoh: templates/transaksi-contoh.csv.")


def pecah_tanggal_file(teks):
    """Kembalikan ('iso', date) | ('dm', a, b, tahun|None) | ('teks', date) | ('kosong',) | ('pend',) | ('rusak', alasan)."""
    s = str(teks or "").strip()
    if not s:
        return ("kosong",)
    if s.upper() in ("PEND", "PENDING"):
        return ("pend",)
    s = re.sub(r"[ T]\d{1,2}[:.]\d{2}([:.]\d{2})?$", "", s).strip()
    if re.fullmatch(r"\d{5}(\.0+)?", s):
        return ("rusak", "nomor seri tanggal Excel ('%s'); format kolom tanggal sebagai teks DD/MM/YYYY" % teks)
    m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", s)
    if m:
        try:
            return ("iso", date(int(m.group(1)), int(m.group(2)), int(m.group(3))))
        except ValueError:
            return ("rusak", "tanggal tidak ada di kalender ('%s')" % teks)
    m = re.fullmatch(r"(\d{1,2})[/.-](\d{1,2})(?:[/.-](\d+))?", s)
    if m:
        th = m.group(3)
        if th is not None and len(th) != 4:
            return ("rusak", "tahun 2 angka ambigu ('%s'); simpan ulang dengan tahun 4 angka" % teks)
        return ("dm", int(m.group(1)), int(m.group(2)), int(th) if th else None)
    tok = [x for x in re.split(r"[\s,\-/.]+", s.lower()) if x]
    if len(tok) == 3 and tok[1] in NAMA_BULAN and tok[0].isdigit() and tok[2].isdigit() and len(tok[2]) == 4:
        try:
            return ("teks", date(int(tok[2]), NAMA_BULAN[tok[1]], int(tok[0])))
        except ValueError:
            return ("rusak", "tanggal tidak ada di kalender ('%s')" % teks)
    return ("rusak", "tanggal tidak terbaca ('%s')" % teks)


def cmd_impor(args):
    rows, pr_file = baca_csv(args.file)
    hdr_i, peta = cari_header(rows)
    header = rows[hdr_i]

    def kerja(conn, cfg):
        peringatan = list(pr_file)
        blokir = []
        if "debit" in peta or "kredit" in peta:
            if not args.jenis_file:
                raise Gagal("File memakai kolom Debit/Kredit yang artinya bisa terbalik: di MUTASI BANK debit = uang "
                            "KELUAR dari rekening, di BUKU KAS debit = uang MASUK. Tanyakan ke pengguna, lalu ulangi "
                            "dengan --jenis-file mutasi-bank atau --jenis-file buku-kas.", perlu_jenis_file=True)
        if not any(k in peta for k in ("masuk", "keluar", "debit", "kredit", "jumlah")):
            raise Gagal("Kolom nominal tidak ditemukan (Masuk/Keluar, Debit/Kredit, atau Jumlah). Kolom yang ada: %s."
                        % ", ".join(header))
        akun_default = cari_akun(conn, args.akun) if args.akun else None
        if not akun_default and "akun" not in peta:
            daftar = semua_akun(conn)
            if len(daftar) == 1:
                akun_default = daftar[0]
            elif "metode" not in peta:
                raise Gagal("Sebut akun tujuan impor dengan --akun (mis. --akun BRI untuk mutasi BRI). Akun yang ada: "
                            "%s." % ", ".join(a["nama"] for a in daftar), perlu_akun=True)
        tetap = {}
        for tt in args.tetapkan or []:
            m = re.fullmatch(r"\s*(\d+)\s*=\s*(.+?)\s*", tt)
            if not m:
                raise Gagal("Format --tetapkan salah: '%s'. Contoh: --tetapkan 7=prive, --tetapkan 9=pindah:laci, "
                            "--tetapkan 12=lewati." % tt)
            tetap[int(m.group(1))] = m.group(2)
        # --- baca tanggal (cek urutan hari/bulan untuk seluruh file)
        mentah = []
        bukti_dm, bukti_md = [], []
        for i in range(hdr_i + 1, len(rows)):
            r = rows[i]
            if not any(c.strip() for c in r):
                continue
            ambil = (lambda peran, r=r: r[peta[peran]].strip() if peran in peta and peta[peran] < len(r) else "")
            ket = ambil("keterangan")
            ket_n = normal(ket)
            if re.match(r"^(saldo awal|saldo akhir|saldo sebelumnya|total|jumlah|mutasi debet|mutasi kredit|"
                        r"opening balance|closing balance|ending balance|beginning balance)\b", ket_n) or \
                    normal(ambil("tanggal")) in ("total", "jumlah", "saldo awal", "saldo akhir"):
                mentah.append((i + 1, None, "baris saldo/total dilewati"))
                continue
            if [normal(c) for c in r] == [normal(c) for c in header]:
                continue
            tg = pecah_tanggal_file(ambil("tanggal"))
            if tg[0] == "dm":
                a_, b_ = tg[1], tg[2]
                if a_ > 12 and b_ <= 12:
                    bukti_dm.append(i + 1)
                elif b_ > 12 and a_ <= 12:
                    bukti_md.append(i + 1)
            mentah.append((i + 1, (r, ambil, tg, ket), None))
        fmt = args.format_tanggal
        if bukti_dm and bukti_md:
            raise Gagal("Urutan tanggal di file tidak konsisten: baris %s jelas hari/bulan, baris %s jelas bulan/hari. "
                        "Perbaiki file dulu." % (bukti_dm[0], bukti_md[0]))
        if bukti_md and fmt != "bulan-hari":
            raise Gagal("Tanggal di file ini berurutan BULAN/HARI (format Amerika), mis. baris %d. Jika benar, ulangi "
                        "dengan --format-tanggal bulan-hari." % bukti_md[0])
        if bukti_dm and fmt == "bulan-hari":
            raise Gagal("--format-tanggal bulan-hari bertentangan dengan isi file (baris %d jelas hari/bulan)." % bukti_dm[0])
        ada_dm = any(x[1] and x[1][2][0] == "dm" for x in mentah)
        ambigu = [x[0] for x in mentah if x[1] and x[1][2][0] == "dm" and x[1][2][1] != x[1][2][2]]
        if ada_dm and not bukti_dm and not bukti_md and ambigu and not fmt:
            raise Gagal("Semua tanggal di file ini bisa dibaca dua arah (mis. 01/09 = 1 September atau 9 Januari). "
                        "Tanyakan ke pengguna, lalu ulangi dengan --format-tanggal hari-bulan (Indonesia) atau "
                        "--format-tanggal bulan-hari.", perlu_format_tanggal=True)
        urutan_md = fmt == "bulan-hari" or bool(bukti_md)
        # --- olah baris
        hasil, bermasalah, dilewati, cek = [], [], [], []
        dibulatkan = 0
        hi = hari_ini()
        kemunculan = {}
        for no, isi, alasan in mentah:
            if isi is None:
                dilewati.append({"baris": no, "alasan": alasan})
                continue
            r, ambil, tg, ket = isi
            if no in tetap and normal(tetap[no]) == "lewati":
                dilewati.append({"baris": no, "alasan": "dilewati atas permintaan pengguna"})
                continue
            if tg[0] in ("kosong", "pend"):
                dilewati.append({"baris": no, "alasan": "tanggal kosong/PEND (transaksi belum dibukukan bank)"})
                continue
            if tg[0] == "rusak":
                bermasalah.append({"baris": no, "alasan": tg[1]})
                continue
            if tg[0] == "dm":
                d_, m_ = (tg[2], tg[1]) if urutan_md else (tg[1], tg[2])
                th = tg[3] or args.tahun
                if not th:
                    bermasalah.append({"baris": no, "alasan": "tanggal tanpa tahun ('%s'); ulangi dengan --tahun YYYY" %
                                       ambil("tanggal")})
                    continue
                try:
                    tanggal = date(int(th), m_, d_)
                except ValueError:
                    bermasalah.append({"baris": no, "alasan": "tanggal tidak ada di kalender ('%s')" % ambil("tanggal")})
                    continue
            else:
                tanggal = tg[1]
            if tanggal > hi:
                bermasalah.append({"baris": no, "alasan": "tanggal %s di masa depan" % tgl_id(tanggal)})
                continue
            # nominal & arah
            try:
                arah, jumlah, bul = None, None, False
                if "masuk" in peta or "keluar" in peta:
                    vm = nominal_file(ambil("masuk")) if "masuk" in peta else None
                    vk = nominal_file(ambil("keluar")) if "keluar" in peta else None
                    if vm and vk:
                        raise ValueError("kolom masuk DAN keluar sama-sama terisi")
                    if vm:
                        arah, jumlah, bul = ("masuk" if vm[0] > 0 else "keluar"), abs(vm[0]), vm[1]
                        if vm[0] < 0:
                            raise ValueError("nilai minus di kolom Masuk; pastikan artinya")
                    elif vk:
                        arah, jumlah, bul = "keluar", abs(vk[0]), vk[1]
                if arah is None and ("debit" in peta or "kredit" in peta):
                    vd = nominal_file(ambil("debit")) if "debit" in peta else None
                    vc = nominal_file(ambil("kredit")) if "kredit" in peta else None
                    if vd and vc:
                        raise ValueError("kolom debit DAN kredit sama-sama terisi")
                    bank = args.jenis_file == "mutasi-bank"
                    if vd:
                        arah, jumlah, bul = ("keluar" if bank else "masuk"), abs(vd[0]), vd[1]
                    elif vc:
                        arah, jumlah, bul = ("masuk" if bank else "keluar"), abs(vc[0]), vc[1]
                if arah is None and "jumlah" in peta:
                    vj = nominal_file(ambil("jumlah"))
                    if vj:
                        jenis = normal(ambil("jenis")) if "jenis" in peta else ""
                        tanda = vj[2] or {"cr": "CR", "kredit": "CR", "k": "CR", "masuk": "MASUK", "in": "MASUK",
                                          "db": "DB", "debit": "DB", "debet": "DB", "d": "DB", "keluar": "KELUAR",
                                          "out": "KELUAR"}.get(jenis)
                        if tanda in ("CR", "DB") and not vj[2] and args.jenis_file != "mutasi-bank" and jenis in (
                                "kredit", "debit", "debet", "k", "d"):
                            if not args.jenis_file:
                                raise Gagal("Kolom jenis berisi Debit/Kredit yang artinya bisa terbalik. Ulangi dengan "
                                            "--jenis-file mutasi-bank atau --jenis-file buku-kas.",
                                            perlu_jenis_file=True)
                            tanda = "DB" if tanda == "CR" else "CR"   # buku kas: debit = masuk
                        if tanda in ("CR", "MASUK"):
                            arah = "masuk"
                        elif tanda in ("DB", "KELUAR"):
                            arah = "keluar"
                        elif vj[0] < 0:
                            arah = "keluar"
                        elif "jenis" in peta and jenis:
                            raise ValueError("jenis '%s' tidak dikenal (pakai masuk/keluar, CR/DB)" % ambil("jenis"))
                        else:
                            arah = "masuk"
                            if not any(c["alasan"].startswith("arah") for c in cek):
                                peringatan.append("File tanpa kolom jenis: nominal positif dibaca MASUK, minus dibaca "
                                                  "KELUAR.")
                        jumlah, bul = abs(vj[0]), vj[1]
                if arah is None:
                    raise ValueError("nominal kosong")
                if jumlah < 100:
                    raise ValueError("nominal %s terlalu kecil; kemungkinan format angka salah" % rp(jumlah))
                if jumlah >= BATAS_NOMINAL:
                    raise ValueError("nominal terlalu besar")
            except ValueError as e:
                bermasalah.append({"baris": no, "alasan": str(e)})
                continue
            dibulatkan += 1 if bul else 0
            # akun & metode
            try:
                akun = cari_akun(conn, ambil("akun")) if "akun" in peta and ambil("akun") else None
                metode = kode_metode(ambil("metode")) if "metode" in peta and ambil("metode") else None
                if metode == "pindah":
                    raise Gagal("metode 'pindah' tidak bisa diimpor; catat dengan kas.py pindah")
                if not akun:
                    akun = akun_default or akun_untuk_metode(conn, metode or "tunai")
                if not metode:
                    metode = METODE_DEFAULT_AKUN[akun["jenis"]]
                    if akun["jenis"] != "tunai" and re.search(r"\bqris\b", normal(ket)):
                        metode = "qris"
            except Gagal as g:
                bermasalah.append({"baris": no, "alasan": g.pesan})
                continue
            if date.fromisoformat(akun["tanggal_awal"]) > tanggal:
                bermasalah.append({"baris": no, "alasan": "tanggal %s sebelum saldo awal akun %s (%s)" %
                                   (tgl_id(tanggal), akun["nama"], tgl_id(akun["tanggal_awal"]))})
                continue
            # kategori
            ke_akun = None
            if no in tetap:
                tv = tetap[no].strip()
                if normal(tv).startswith("pindah"):
                    tujuan = tv.split(":", 1)[1] if ":" in tv else ""
                    if not tujuan:
                        raise Gagal("--tetapkan %d=pindah butuh akun pasangan, mis. %d=pindah:laci." % (no, no))
                    ke_akun = cari_akun(conn, tujuan)
                    if ke_akun["id"] == akun["id"]:
                        raise Gagal("--tetapkan %d: akun pasangan sama dengan akun baris itu." % no)
                    kat, sumber_kat = "pindah", "ditetapkan pengguna"
                else:
                    kat = kode_kategori(tv)
                    if not kat:
                        raise Gagal("--tetapkan %d=%s: kategori tidak dikenal. Pilih: %s, pindah:<akun>, lewati." %
                                    (no, tv, ", ".join(KATEGORI)))
                    sumber_kat = "ditetapkan pengguna"
            elif "kategori" in peta and ambil("kategori"):
                kat = kode_kategori(ambil("kategori"))
                sumber_kat = "kolom kategori"
                if not kat:
                    kat, _ = tebak_kategori(ambil("kategori") + " " + ket, arah)
                    sumber_kat = "ditebak dari kolom kategori"
            else:
                kat, _ = tebak_kategori(ket, arah)
                sumber_kat = "ditebak dari keterangan"
            if kat != "pindah":
                if not kat and POLA_MUNGKIN_PINDAH.search(" " + normal(ket) + " "):
                    cek.append({"baris": no, "alasan": "mungkin pindah dana (tarik/setor tunai/top up)", "keterangan": ket,
                                "jumlah": jumlah, "arah": arah, "saran": "--tetapkan %d=pindah:<akun pasangan> atau "
                                                                        "%d=prive / %d=modal" % (no, no, no)})
                    kat, sumber_kat = "lain-lain", "belum jelas"
                elif not kat:
                    kat = kode_kategori(args.kategori_default) if args.kategori_default else None
                    if kat:
                        sumber_kat = "kategori default"
                    else:
                        kat, sumber_kat = "lain-lain", "belum jelas"
                        cek.append({"baris": no, "alasan": "kategori belum jelas", "keterangan": ket, "jumlah": jumlah,
                                    "arah": arah, "saran": "--tetapkan %d=<kategori>" % no})
                if arah not in SEMUA_KATEGORI[kat][1]:
                    bermasalah.append({"baris": no, "alasan": "kategori %s tidak boleh untuk uang %s" % (kat, arah)})
                    continue
            sidik_dasar = "|".join([str(akun["id"]), tanggal.isoformat(), arah, str(jumlah), normal(ket)])
            kemunculan[sidik_dasar] = kemunculan.get(sidik_dasar, 0) + 1
            sidik = hashlib.sha1(("%s|%d" % (sidik_dasar, kemunculan[sidik_dasar])).encode()).hexdigest()[:20]
            hasil.append({"baris": no, "tanggal": tanggal, "arah": arah, "jumlah": jumlah, "kategori": kat,
                          "sumber_kategori": sumber_kat, "metode": metode, "akun": akun, "ke_akun": ke_akun,
                          "catatan": bersih(ket or label_kat(kat, arah) if kat != "pindah" else ket, 200), "sidik": sidik})
        if not hasil and not dilewati:
            raise Gagal("Tidak ada baris yang bisa diimpor. Masalah: %s" % "; ".join(
                "baris %d: %s" % (b["baris"], b["alasan"]) for b in bermasalah[:5]))
        # --- duplikat & mirip
        baru, sudah, mirip = [], [], []
        for h in hasil:
            if conn.execute("SELECT 1 FROM transaksi WHERE sidik=? AND status='aktif'", (h["sidik"],)).fetchone():
                sudah.append(h["baris"])
                continue
            m = conn.execute("SELECT id FROM transaksi WHERE status='aktif' AND sumber='manual' AND akun_id=? AND "
                             "tanggal=? AND arah=? AND jumlah=?", (h["akun"]["id"], h["tanggal"].isoformat(), h["arah"],
                                                                  h["jumlah"])).fetchone()
            if m and not args.sertakan_mirip:
                mirip.append({"baris": h["baris"], "id": m[0], "tanggal": h["tanggal"].isoformat(), "jumlah": h["jumlah"],
                              "arah": h["arah"]})
                continue
            baru.append(h)
        sumber = "impor:" + Path(args.file).name[:60]
        ids = []
        for h in baru:
            if h["kategori"] == "pindah":
                grup = "P-impor-" + h["sidik"][:8]
                e = {"tanggal": h["tanggal"], "jumlah": h["jumlah"], "kategori": "pindah", "metode": "pindah",
                     "catatan": "Pindah dana: " + (h["catatan"] or "")}
                ids.append(simpan_entri(conn, dict(e, arah=h["arah"], akun=h["akun"]), jenis="pindah", grup=grup,
                                        sumber=sumber, sidik=h["sidik"]))
                ids.append(simpan_entri(conn, dict(e, arah="masuk" if h["arah"] == "keluar" else "keluar",
                                                   akun=h["ke_akun"]), jenis="pindah", grup=grup, sumber=sumber))
            else:
                ids.append(simpan_entri(conn, h, sumber=sumber, sidik=h["sidik"]))
        if baru:
            akun_ids = [h["akun"]["id"] for h in baru] + [h["ke_akun"]["id"] for h in baru if h["ke_akun"]]
            blokir += blokir_minus(cari_minus(conn, akun_ids, min(h["tanggal"] for h in baru)))
        if dibulatkan:
            peringatan.append("%d nominal bersen dibulatkan ke rupiah terdekat (0,5 ke atas)." % dibulatkan)
        if any(h["kategori"] == "prive" for h in baru):
            _, _, pr = ringkas_prive(conn, cfg, max(h["tanggal"] for h in baru if h["kategori"] == "prive"))
            peringatan += pr
        masuk = sum(h["jumlah"] for h in baru if h["arah"] == "masuk" and h["kategori"] != "pindah")
        keluar = sum(h["jumlah"] for h in baru if h["arah"] == "keluar" and h["kategori"] != "pindah")
        per_kat = OrderedDict()
        for h in baru:
            k = per_kat.setdefault(label_kat(h["kategori"], h["arah"]), 0)
            per_kat[label_kat(h["kategori"], h["arah"])] = k + h["jumlah"]
        t = ["Impor %s: %d baris akan dicatat (masuk %s, keluar %s)." % (Path(args.file).name, len(baru), rp(masuk),
                                                                         rp(keluar))]
        if baru:
            t.append("Tanggal %s - %s. Per kategori: %s." % (
                tgl_id(min(h["tanggal"] for h in baru)), tgl_id(max(h["tanggal"] for h in baru)),
                ", ".join("%s %s" % (k, rp(v)) for k, v in per_kat.items())))
            for h in baru[:8]:
                t.append("- baris %d: %s %s %s | %s | %s%s" % (h["baris"], tgl_id(h["tanggal"]), h["arah"], rp(h["jumlah"]),
                                                              label_kat(h["kategori"], h["arah"]) if h["kategori"] != "pindah"
                                                              else "Pindah ke/dari " + h["ke_akun"]["nama"],
                                                              h["catatan"][:50],
                                                              " (%s)" % h["sumber_kategori"] if h["sumber_kategori"] not in
                                                              ("kolom kategori",) else ""))
            if len(baru) > 8:
                t.append("- ... dan %d baris lain (lihat field 'baris' di --json)" % (len(baru) - 8))
        if cek:
            t.append("PERLU DICEK KE PENGGUNA (%d baris, sementara dicatat lain-lain):" % len(cek))
            for c in cek[:20]:
                t.append("- baris %d: %s %s '%s' -> %s. Saran: %s" % (c["baris"], c["arah"], rp(c["jumlah"]),
                                                                      c["keterangan"][:50], c["alasan"], c["saran"]))
        if sudah:
            t.append("Dilewati karena sudah pernah diimpor: %d baris." % len(sudah))
        if mirip:
            t.append("Dilewati karena mirip catatan manual (tanggal, akun, arah, nominal sama): %s. Jika memang "
                     "transaksi berbeda, ulangi dengan --sertakan-mirip." % ", ".join(
                         "baris %d ~ #%d" % (m["baris"], m["id"]) for m in mirip[:10]))
        if dilewati:
            t.append("Baris dilewati: %s." % ", ".join("%d (%s)" % (d["baris"], d["alasan"]) for d in dilewati[:10]))
        if bermasalah:
            t.append("Baris BERMASALAH (tidak diimpor): %s." % "; ".join(
                "%d: %s" % (b["baris"], b["alasan"]) for b in bermasalah[:10]))
        return {"ringkasan": {"file": Path(args.file).name, "baris_baru": len(baru)},
                "baris": [{"baris": h["baris"], "tanggal": h["tanggal"].isoformat(), "arah": h["arah"],
                           "jumlah": h["jumlah"], "kategori": h["kategori"], "sumber_kategori": h["sumber_kategori"],
                           "metode": h["metode"], "akun": h["akun"]["nama"],
                           "ke_akun": h["ke_akun"]["nama"] if h["ke_akun"] else None, "catatan": h["catatan"]}
                          for h in baru],
                "jumlah_baru": len(baru), "masuk": masuk, "keluar": keluar, "perlu_dicek": cek,
                "sudah_diimpor": sudah, "mirip_manual": mirip, "dilewati": dilewati, "bermasalah": bermasalah,
                "peringatan": peringatan, "blokir": blokir, "teks": "\n".join(t)}
    return jalankan_tulis(args, "impor", kerja, label_backup="sebelum-impor" if args.ya else None)


def cmd_impor_kasir(args):
    teks, _ = baca_teks_file(args.file)
    try:
        d = json.loads(teks)
    except ValueError:
        raise Gagal("File %s bukan JSON rekap kasir-lokal. Buat dengan: kasir.py rekap --tanggal <tgl> --json > "
                    "rekap-kasir.json" % args.file)
    if not isinstance(d, dict) or "per_metode" not in d or "total_diterima" not in d or "periode" not in d:
        raise Gagal("File %s bukan hasil 'kasir.py rekap --json' dari skill kasir-lokal (field per_metode/"
                    "total_diterima/periode tidak ada)." % args.file)
    if d.get("ok") is False:
        raise Gagal("Rekap kasir berisi error: %s" % d.get("error"))
    per = d["periode"]
    if per.get("dari") != per.get("sampai"):
        raise Gagal("Rekap kasir ini untuk %s s.d. %s. Impor per HARI agar tanggal kas tepat: kasir.py rekap --tanggal "
                    "<tgl> --json > rekap-kasir.json (ulangi untuk tiap hari)." % (per.get("dari"), per.get("sampai")))
    try:
        tanggal = date.fromisoformat(per["dari"])
    except (TypeError, ValueError):
        raise Gagal("Tanggal rekap kasir tidak terbaca (%r)." % per.get("dari"))
    per_metode = d["per_metode"] or {}
    if not isinstance(per_metode, dict) or not all(isinstance(v, int) for v in per_metode.values()):
        raise Gagal("Isi per_metode rekap kasir tidak valid (harus angka rupiah bulat).")

    def kerja(conn, cfg):
        if tanggal > hari_ini():
            raise Gagal("Tanggal rekap kasir %s ada di masa depan." % tgl_id(tanggal))
        peringatan, blokir = [], []
        paksa = {}
        for x in args.akun_untuk or []:
            m = re.fullmatch(r"\s*([^=]+?)\s*=\s*(.+?)\s*", x)
            if not m:
                raise Gagal("Format --akun-untuk salah: '%s'. Contoh: --akun-untuk qris=BRI" % x)
            paksa[kode_metode(m.group(1))] = cari_akun(conn, m.group(2))
        lama = conn.execute("SELECT id, jumlah, arah, metode FROM transaksi WHERE sumber='kasir' AND tanggal=? AND "
                            "status='aktif'", (tanggal.isoformat(),)).fetchall()
        if lama and not args.ganti:
            raise Gagal("Rekap kasir %s sudah pernah diimpor (%s). Jika kasir mendapat transaksi tambahan setelah itu, "
                        "ulangi dengan --ganti (impor lama dibatalkan, bukan dihapus, lalu diganti yang baru)." %
                        (tgl_id(tanggal), ", ".join("#%d" % r["id"] for r in lama)), sudah_diimpor=True)
        for r in lama:
            conn.execute("UPDATE transaksi SET status='batal', alasan_batal=? WHERE id=?",
                         ("diganti impor kasir ulang %s" % stempel(), r["id"]))
        entri = []
        total = 0
        for label, nilai in per_metode.items():
            kunci = normal(label).replace(" ", "-") if normal(label) == "e wallet" else normal(label)
            if kunci not in METODE_KASIR:
                raise Gagal("Metode kasir '%s' tidak dikenal oleh kas-umkm." % label)
            metode = METODE_KASIR[kunci]
            total += nilai
            if not nilai:
                continue
            if metode is None:
                peringatan.append("Metode kasir '%s' %s TIDAK dicatat (voucher/lainnya bukan uang masuk). Catat manual "
                                  "bila memang uang." % (label, rp(nilai)))
                continue
            akun = paksa.get(metode) or akun_untuk_metode(conn, metode)
            if date.fromisoformat(akun["tanggal_awal"]) > tanggal:
                raise Gagal("Tanggal rekap %s lebih awal dari saldo awal akun %s (%s)." %
                            (tgl_id(tanggal), akun["nama"], tgl_id(akun["tanggal_awal"])))
            e = {"tanggal": tanggal, "arah": "masuk" if nilai > 0 else "keluar", "jumlah": abs(nilai),
                 "kategori": "penjualan", "metode": metode, "akun": akun,
                 "catatan": ("Penjualan kasir %s (%s)" if nilai > 0 else "Retur/refund kasir %s (%s)") %
                            (tgl_id(tanggal), label)}
            entri.append(e)
        if total != d["total_diterima"]:
            peringatan.append("Jumlah per metode (%s) berbeda dengan total diterima kasir (%s); periksa rekap kasir." %
                              (rp(total), rp(d["total_diterima"])))
        pajak = int(d.get("pajak") or 0)
        if pajak:
            peringatan.append("Uang diterima termasuk PPN/PBJT %s yang nanti disetor. Saat menyetor, catat keluar "
                              "kategori pajak." % rp(pajak))
        if not entri:
            raise Gagal("Rekap kasir %s tidak berisi uang masuk (belum ada transaksi)." % tgl_id(tanggal))
        ids = [simpan_entri(conn, e, jenis="kasir", sumber="kasir", sidik="kasir:%s:%s" % (tanggal.isoformat(),
                                                                                         e["metode"])) for e in entri]
        blokir += blokir_minus(cari_minus(conn, [e["akun"]["id"] for e in entri], tanggal))
        t = ["Impor rekap kasir-lokal %s (uang diterima %s):" % (tgl_panjang(tanggal), rp(d["total_diterima"]))]
        t += ["- " + baris_entri(e) for e in entri]
        if lama:
            t.append("Impor lama dibatalkan (diganti): %s." % ", ".join("#%d" % r["id"] for r in lama))
        t.append("Pengeluaran laci (kasir.py kas --keluar) TIDAK ikut; catat pengeluaran usaha di buku kas ini.")
        return {"ringkasan": {"tanggal": tanggal.isoformat(), "id": ids}, "tanggal": tanggal.isoformat(),
                "entri": [{"arah": e["arah"], "jumlah": e["jumlah"], "metode": e["metode"], "akun": e["akun"]["nama"]}
                          for e in entri], "diganti": [r["id"] for r in lama], "peringatan": peringatan,
                "blokir": blokir, "teks": "\n".join(t)}
    return jalankan_tulis(args, "impor-kasir", kerja, label_backup="sebelum-impor-kasir" if args.ya else None)


# --------------------------------------------------------------------------- ekspor
def cmd_ekspor(args):
    db, conn = baca_db(args)
    try:
        cfg = pengaturan(conn)
        akun = semua_akun(conn)
        pertama = min(date.fromisoformat(a["tanggal_awal"]) for a in akun) if akun else hari_ini()
        if args.format == "arus-kas":
            return ekspor_arus_kas(conn, cfg, args)
        dari, sampai, jenis = ambil_periode(args, default="semua")
        if jenis == "semua":
            dari, sampai = pertama, hari_ini()
        dari = max(dari, pertama)
        sampai = min(sampai, hari_ini())
        if sampai < dari:
            raise Gagal("Periode ekspor di luar masa pencatatan buku kas (mulai %s)." % tgl_id(pertama))
        q = ("SELECT t.*, a.nama AS akun_nama FROM transaksi t JOIN akun a ON a.id=t.akun_id WHERE t.tanggal BETWEEN ? "
             "AND ?" + ("" if args.semua else " AND t.status='aktif'") + " ORDER BY t.tanggal, t.id")
        rows = conn.execute(q, (dari.isoformat(), sampai.isoformat())).fetchall()
        saldo_awal = sum(saldo_pembuka(conn, a, dari) for a in akun if date.fromisoformat(a["tanggal_awal"]) <= sampai)
        saldo_akhir = sum(saldo_akhir_hari(conn, a, sampai) for a in akun if date.fromisoformat(a["tanggal_awal"]) <= sampai)
        telat = [a["nama"] for a in akun if dari < date.fromisoformat(a["tanggal_awal"]) <= sampai]
    finally:
        conn.close()
    pr = []
    if args.format == "lengkap":
        path = args.csv or str(db.parent / "ekspor" / ("kas-lengkap-%s.csv" % kini().strftime("%Y%m%d-%H%M%S")))
        data = [[r["id"], tgl_id(r["tanggal"]), r["arah"], r["jumlah"], r["kategori"], METODE[r["metode"]][0],
                 r["akun_nama"], r["catatan"], r["jenis"], r["sumber"], r["status"], r["alasan_batal"] or ""]
                for r in rows]
        path = tulis_csv(path, ["ID", "Tanggal", "Arah", "Jumlah", "Kategori", "Metode", "Akun", "Catatan", "Jenis",
                                "Sumber", "Status", "Alasan Batal"], data, args.pemisah)
        t = "Ekspor %d baris %s - %s ke %s (buka di Excel/Google Sheets)." % (len(data), tgl_id(dari), tgl_id(sampai), path)
        return {"ok": True, "mode": "baca", "file": path, "baris": len(data), "teks": t}, t
    # emkm
    path = args.csv or str(db.parent / "ekspor" / ("kas-emkm-%s.csv" % kini().strftime("%Y%m%d-%H%M%S")))
    data = []
    if saldo_awal >= 0:
        data.append([tgl_id(dari), "Saldo awal", saldo_awal, "", ""])
    else:
        pr.append("Saldo awal gabungan minus (%s); tidak ditulis di file. Periksa saldo awal akun." % rp(saldo_awal))
    n_pindah = 0
    for r in rows:
        if r["kategori"] == "pindah":
            n_pindah += 1
            continue
        kode = EMKM.get((r["kategori"], r["arah"]), "")
        ket = r["catatan"] or label_kat(r["kategori"], r["arah"])
        if r["kategori"] == "pajak" and not re.search(r"\b(pajak|pph|pbjt|pb1|ppn)\b", normal(ket)):
            ket = "Pajak: " + ket
        data.append([tgl_id(r["tanggal"]), ket, r["jumlah"] if r["arah"] == "masuk" else "",
                     r["jumlah"] if r["arah"] == "keluar" else "", kode])
    path = tulis_csv(path, ["Tanggal", "Keterangan", "Masuk", "Keluar", "Kategori"], data, args.pemisah)
    if telat:
        pr.append("Akun %s baru dicatat setelah %s; saldo awalnya dianggap sudah ada sejak awal periode." %
                  (", ".join(telat), tgl_id(dari)))
    perintah = ("python3 <folder-laporan-keuangan-emkm>/scripts/laporan_emkm.py \"%s\" --nama-usaha \"%s\" "
                "--periode-awal %s --periode-akhir %s --kas-akhir-aktual %d" %
                (path, cfg["nama_usaha"], dari.isoformat(), sampai.isoformat(), saldo_akhir))
    t = ("Ekspor untuk skill laporan-keuangan-emkm: %d baris %s - %s ke %s\n"
         "Kolom: Tanggal;Keterangan;Masuk;Keluar;Kategori (kode kategori emkm; pajak & lain-lain dikosongkan agar emkm "
         "mengklasifikasi dari keterangan). Pindah dana antar akun (%d baris) tidak ditulis karena kas + rekening "
         "dihitung sebagai satu. Saldo awal gabungan semua akun %s, saldo akhir %s.\n"
         "Jalankan (tanyakan dulu stok awal/akhir, piutang, utang, aset):\n%s" %
         (len(data), tgl_id(dari), tgl_id(sampai), path, n_pindah, rp(saldo_awal), rp(saldo_akhir), perintah))
    t += "".join("\nCatatan: " + p for p in pr)
    return {"ok": True, "mode": "baca", "file": path, "baris": len(data), "saldo_awal": saldo_awal,
            "saldo_akhir": saldo_akhir, "perintah_emkm": perintah, "peringatan": pr, "teks": t}, t


ARUS_LABEL = {("penjualan", "masuk"): "Penjualan (rata-rata riwayat)", ("penjualan", "keluar"): "Retur penjualan",
              ("beli-stok", "keluar"): "Beli stok (bahan/supplier)", ("gaji", "keluar"): "Gaji karyawan",
              ("listrik-air", "keluar"): "Listrik/air", ("sewa", "keluar"): "Sewa tempat",
              ("pajak", "keluar"): "Pajak", ("pinjaman", "keluar"): "Cicilan pinjaman",
              ("prive", "keluar"): "Prive (ambil pribadi)", ("lain-lain", "masuk"): "Pemasukan lain-lain",
              ("lain-lain", "keluar"): "Pengeluaran lain-lain"}
ARUS_BULANAN = {"gaji", "sewa", "listrik-air", "pajak", "pinjaman"}
ARUS_KRITIS = {"gaji": "ya", "sewa": "ya", "listrik-air": "ya", "pajak": "ya", "pinjaman": "ya", "prive": "tidak",
               "lain-lain": "tidak", "penjualan": ""}


def ekspor_arus_kas(conn, cfg, args):
    hi = hari_ini()
    akhir = senin(hi) - timedelta(days=1)            # Minggu terakhir yang sudah lewat penuh
    n_minggu = args.minggu_riwayat
    if not 2 <= n_minggu <= 26:
        raise Gagal("--minggu-riwayat harus 2-26.")
    pertama = conn.execute("SELECT MIN(tanggal) FROM transaksi WHERE status='aktif'").fetchone()[0]
    if not pertama:
        raise Gagal("Belum ada catatan kas untuk dijadikan dasar rencana arus kas.")
    mulai_data = senin(date.fromisoformat(pertama))
    if date.fromisoformat(pertama) != mulai_data:
        mulai_data += timedelta(days=7)               # minggu pertama tidak penuh: dilewati
    tersedia = max(0, ((akhir - mulai_data).days + 1) // 7)
    if tersedia < 2:
        raise Gagal("Riwayat baru %d minggu penuh; butuh minimal 2 minggu penuh (Senin-Minggu) untuk membuat rencana "
                    "dari riwayat. Sementara itu isi rencana arus kas manual di skill arus-kas-13minggu." % tersedia)
    pr = []
    if tersedia < n_minggu:
        pr.append("Riwayat hanya %d minggu penuh (diminta %d); rata-rata memakai %d minggu." % (tersedia, n_minggu,
                                                                                               tersedia))
        n_minggu = tersedia
    dari = akhir - timedelta(days=7 * n_minggu - 1)
    rows = conn.execute("SELECT * FROM transaksi WHERE status='aktif' AND kategori NOT IN ('pindah','selisih-kas') "
                        "AND tanggal BETWEEN ? AND ? ORDER BY tanggal, id", (dari.isoformat(), akhir.isoformat())).fetchall()
    grup = OrderedDict()
    for r in rows:
        grup.setdefault((r["kategori"], r["arah"]), []).append(r)
    data, lewat = [], []
    urut = [k for k in ARUS_LABEL] + [k for k in grup if k not in ARUS_LABEL]
    for kunci in urut:
        if kunci not in grup:
            continue
        kat, arah = kunci
        isi = grup[kunci]
        total = sum(r["jumlah"] for r in isi)
        if kunci in (("modal", "masuk"), ("pinjaman", "masuk")):
            lewat.append("%s %s (sekali waktu, tidak diproyeksikan)" % (label_kat(kat, arah), rp(total)))
            continue
        minggu_ada = {(date.fromisoformat(r["tanggal"]) - dari).days // 7 for r in isi}
        label = ARUS_LABEL.get(kunci, label_kat(kat, arah))
        kritis = ARUS_KRITIS.get(kat, "")
        if kat in ARUS_BULANAN and len(minggu_ada) < max(2, (n_minggu + 1) // 2):
            terakhir = date.fromisoformat(isi[-1]["tanggal"])
            bulan_ini = [r for r in isi if r["tanggal"][:7] == isi[-1]["tanggal"][:7]]
            nominal = sum(r["jumlah"] for r in bulan_ini)
            ket = "riwayat kas-umkm: %dx dalam %d minggu, terakhir %s" % (len(isi), n_minggu, tgl_id(terakhir))
            if len(isi) == 1:
                ket += "; hanya sekali - pastikan memang bulanan"
            data.append(["tgl:%d" % terakhir.day, arah, label, nominal, ket, kritis])
        else:
            nominal = bulat(Decimal(total) / n_minggu)
            data.append(["semua", arah, label, nominal, "rata-rata %d minggu (%s - %s) dari kas-umkm" %
                         (n_minggu, tgl_id(dari), tgl_id(akhir)), kritis])
    if not data:
        raise Gagal("Tidak ada transaksi usaha di %d minggu terakhir (%s - %s)." % (n_minggu, tgl_id(dari), tgl_id(akhir)))
    db = path_db(args)
    path = args.csv or str(db.parent / "ekspor" / ("rencana-kas-%s.csv" % kini().strftime("%Y%m%d-%H%M%S")))
    path = tulis_csv(path, ["minggu", "jenis", "kategori", "nominal", "keterangan", "kritis"], data, ";")
    saldo = sum(saldo_akhir_hari(conn, a, hi) for a in semua_akun(conn))
    mulai = senin(hi) + timedelta(days=7)
    perintah = ("python3 <folder-arus-kas-13minggu>/scripts/proyeksi_kas.py \"%s\" --saldo-awal %d --mulai %s "
                "--output-csv proyeksi-kas-13-minggu.csv" % (path, saldo, mulai.isoformat()))
    t = ("Draf rencana arus kas dari riwayat %d minggu (%s - %s): %s\n%s\n"
         "Saldo semua akun hari ini: %s. Proyeksi mulai Senin %s.\n"
         "SEBELUM menjalankan proyeksi, tanyakan ke pengguna dan tambahkan baris rencana yang tidak terlihat di "
         "riwayat: THR, piutang yang akan dibayar, pembelian besar, kenaikan/penurunan penjualan musiman. Baris "
         "'tgl:' = pos bulanan (tanggal bayar terakhir).\nJalankan:\n%s" %
         (n_minggu, tgl_id(dari), tgl_id(akhir), path, "\n".join("- %s %s %s: %s" % (r[0], r[1], r[2], rp(r[3]))
                                                                 for r in data),
          rp(saldo), tgl_id(mulai), perintah))
    if lewat:
        t += "\nTidak dimasukkan: " + "; ".join(lewat) + "."
    t += "".join("\nCatatan: " + p for p in pr)
    return {"ok": True, "mode": "baca", "file": path, "baris": [dict(zip(["minggu", "jenis", "kategori", "nominal",
                                                                         "keterangan", "kritis"], r)) for r in data],
            "saldo_awal": saldo, "mulai": mulai.isoformat(), "perintah_arus_kas": perintah, "peringatan": pr,
            "teks": t}, t


# --------------------------------------------------------------------------- backup / restore
def cmd_backup(args):
    db = path_db(args)
    fol = folder_backup(db)
    if args.daftar:
        bks = sorted(fol.glob("kas-*.db")) if fol.is_dir() else []
        if bks:
            t = ("Cadangan di %s (terbaru paling bawah):\n%s\nPulihkan: kas.py restore --dari \"%s\" (pratinjau, lalu "
                 "--ya)." % (fol, "\n".join("- " + str(b) for b in bks[-30:]), bks[-1]))
        else:
            t = ("Belum ada cadangan di %s. Jika buku kas rusak dan tidak ada cadangan: kas.py init --mulai-baru "
                 "(pratinjau, lalu --ya) membuat buku kas kosong baru; file rusak dipindah ke %s, tidak dihapus. Data "
                 "bisa diimpor ulang dari ekspor CSV terakhir bila ada." % (fol, fol))
        return {"ok": True, "mode": "baca", "folder": str(fol), "backup": [str(b) for b in bks], "teks": t}, t
    conn = buka(db, baca_saja=True)
    conn.close()
    b = buat_backup(db, re.sub(r"[^\w-]", "", args.label or "manual") or "manual")
    t = "Cadangan dibuat: %s" % b
    return {"ok": True, "mode": "tersimpan", "backup": b, "teks": t}, t


def cmd_restore(args):
    """Pulihkan dari cadangan tanpa membuka database aktif untuk ditulis (bisa saja rusak total)."""
    db = path_db(args)
    src = Path(args.dari).expanduser().resolve()
    if not src.is_file():
        raise Gagal("File cadangan %s tidak ada. Lihat daftar: kas.py backup --daftar" % src)
    if src == db:
        raise Gagal("File cadangan sama dengan buku kas aktif. Pilih file dari kas.py backup --daftar.")
    try:
        c = buka(src, baca_saja=True)
    except Gagal as e:
        raise Gagal("File cadangan %s tidak bisa dipakai (%s). Pilih cadangan lain dari kas.py backup --daftar." %
                    (src.name, e.pesan.split(". ")[0]))
    try:
        n = c.execute("SELECT COUNT(*) FROM transaksi WHERE status='aktif'").fetchone()[0]
        cek = c.execute("PRAGMA quick_check").fetchone()[0]
    finally:
        c.close()
    if cek != "ok":
        raise Gagal("File cadangan %s juga bermasalah (%s). Pilih cadangan lain dari kas.py backup --daftar." %
                    (src.name, cek))
    try:
        st = status_db(db)
    except Gagal as e:
        if "sedang dipakai" in e.pesan:
            raise
        raise Gagal("File %s bukan buku kas kas-umkm; restore dibatalkan agar file itu tidak tertimpa. Periksa --db." % db)
    nasib = {"tidak_ada": "Buku kas belum ada; cadangan akan dipasang di lokasi itu.",
             "sehat": "Buku kas saat ini disalin dulu apa adanya ke folder backup-kas.",
             "rusak": "Buku kas saat ini RUSAK; file itu dipindah (tidak dihapus) ke folder backup-kas dengan nama "
                      "rusak-kas-<waktu>.db."}[st]
    if not args.ya:
        t = ("PRATINJAU (belum disimpan):\nBuku kas %s akan diganti dengan cadangan %s (%d transaksi). %s\n\nLanjut? "
             "Jalankan perintah yang sama + --ya setelah pengguna setuju." % (db, src, n, nasib))
        return {"ok": True, "mode": "pratinjau", "perlu_konfirmasi": True, "status_db": st, "teks": t}, t
    db.parent.mkdir(parents=True, exist_ok=True)
    tmp = nama_unik(db.parent, ".kas-restore-%d" % os.getpid(), ".tmp")
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
        finally:
            c.close()
        if not ok or ok[0] != APLIKASI:
            raise Gagal("Salinan cadangan %s tidak valid; buku kas aktif tidak diubah." % src.name)
        if st == "sehat":
            pastikan_tidak_dipakai(db)
            simpanan = singkirkan(db, "kas-{}-sebelum-restore", pindah=False)
        elif st == "rusak":
            simpanan = singkirkan(db, "rusak-kas-{}", pindah=True)
        os.replace(str(tmp), str(db))
    finally:
        if tmp.exists():
            try:
                tmp.unlink()
            except OSError:
                pass
    t = "TERSIMPAN. Buku kas %s dipulihkan dari %s (%d transaksi)." % (db, src, n)
    if simpanan:
        t += ("\nFile rusak dipindah (tidak dihapus) ke: %s" if st == "rusak" else
              "\nSalinan buku kas sebelumnya: %s") % simpanan
    return {"ok": True, "mode": "tersimpan", "backup": str(simpanan) if simpanan else None, "status_db_lama": st,
            "teks": t}, t


# --------------------------------------------------------------------------- CLI
class ParserID(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        print("GAGAL: perintah tidak lengkap/salah: %s. Lihat --help." % message, file=sys.stderr)
        sys.exit(2)


def parse_hari_ini(teks):
    s = str(teks).strip()
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(s, fmt)
            return dt if fmt != "%Y-%m-%d" else dt.replace(hour=12)
        except ValueError:
            continue
    raise Gagal("--hari-ini harus berformat YYYY-MM-DD.")


def buat_parser():
    umum = argparse.ArgumentParser(add_help=False)
    umum.add_argument("--db", help="File database (default ~/KomunitechData/kas/kas.db; ENV KOMUNITECH_KAS_DB)")
    umum.add_argument("--json", action="store_true", help="Output JSON (untuk agent)")
    umum.add_argument("--hari-ini", help=argparse.SUPPRESS)
    tulis = argparse.ArgumentParser(add_help=False)
    tulis.add_argument("--ya", action="store_true", help="Simpan (tanpa ini hanya pratinjau)")
    periode = argparse.ArgumentParser(add_help=False)
    periode.add_argument("--tanggal", help="Satu hari: hari-ini, kemarin, 26/09/2026")
    periode.add_argument("--minggu", help="Senin-Minggu: ini, lalu, atau tanggal di minggu itu")
    periode.add_argument("--bulan", help="ini, lalu, 09/2026, September 2026")
    periode.add_argument("--dari")
    periode.add_argument("--sampai")

    p = ParserID(prog="kas.py", description="Buku kas harian lokal UMKM (kas-umkm %s)" % VERSI)
    p.add_argument("--versi", action="version", version="kas-umkm " + VERSI)
    sub = p.add_subparsers(dest="perintah", parser_class=ParserID)
    sub.required = True

    s = sub.add_parser("init", parents=[umum, tulis], help="Buat buku kas baru")
    s.add_argument("--nama-usaha")
    s.add_argument("--kas-awal", help="Uang di laci saat mulai (default 0)")
    s.add_argument("--mulai", help="Tanggal mulai pencatatan (default hari ini)")
    s.add_argument("--zona", help="WIB (default), WITA, WIT")
    s.add_argument("--batas-prive", help="Batas ambil pribadi per bulan, mis. 3jt (opsional)")
    s.add_argument("--mulai-baru", action="store_true",
                   help="Buku kas rusak & tidak ada cadangan: pindahkan file rusak ke backup-kas lalu buat baru")
    s.set_defaults(fungsi=cmd_init)

    s = sub.add_parser("info", parents=[umum], help="Lokasi database, akun & saldo, cadangan")
    s.set_defaults(fungsi=cmd_info)

    s = sub.add_parser("atur", parents=[umum, tulis], help="Ubah nama usaha, zona, batas prive")
    s.add_argument("--nama-usaha")
    s.add_argument("--zona")
    s.add_argument("--batas-prive", help="mis. 3jt, atau 'hapus'")
    s.set_defaults(fungsi=cmd_atur)

    s = sub.add_parser("akun", parents=[umum, tulis], help="Akun uang: daftar | tambah | ubah")
    s.add_argument("aksi", choices=["daftar", "tambah", "ubah"])
    s.add_argument("--akun", help="Akun yang diubah (untuk ubah)")
    s.add_argument("--nama")
    s.add_argument("--kode", help="Kode singkat (default dari nama)")
    s.add_argument("--jenis", help="tunai | bank | e-wallet")
    s.add_argument("--saldo-awal")
    s.add_argument("--tanggal-awal", help="Tanggal saldo awal (default hari ini)")
    s.add_argument("--terima-qris", action="store_true", help="Uang QRIS masuk ke akun ini")
    s.add_argument("--izinkan-minus", action="store_true")
    s.set_defaults(fungsi=cmd_akun)

    s = sub.add_parser("catat", parents=[umum, tulis], help="Catat uang masuk/keluar")
    s.add_argument("--masuk", help="Nominal uang masuk")
    s.add_argument("--keluar", help="Nominal uang keluar")
    s.add_argument("--kategori", help=", ".join(KATEGORI))
    s.add_argument("--metode", help="tunai | transfer | qris | e-wallet | kartu")
    s.add_argument("--akun", help="Akun uang (default dari metode)")
    s.add_argument("--catatan")
    s.add_argument("--tanggal", help="Default hari ini; DD/MM/YYYY, kemarin")
    s.add_argument("--baris", action="append",
                   help="Banyak entri sekaligus: 'arah;jumlah;kategori;metode;catatan;akun;tanggal' (bisa diulang)")
    s.add_argument("--izinkan-duplikat", action="store_true")
    s.add_argument("--izinkan-minus", action="store_true")
    s.set_defaults(fungsi=cmd_catat)

    s = sub.add_parser("pindah", parents=[umum, tulis], help="Pindah dana antar akun (tidak mengubah hasil usaha)")
    s.add_argument("--dari", required=True)
    s.add_argument("--ke", required=True)
    s.add_argument("--jumlah", required=True)
    s.add_argument("--biaya", help="Biaya admin transfer (dicatat lain-lain dari akun asal)")
    s.add_argument("--tanggal")
    s.add_argument("--catatan")
    s.add_argument("--izinkan-minus", action="store_true")
    s.set_defaults(fungsi=cmd_pindah)

    s = sub.add_parser("batal", parents=[umum, tulis], help="Batalkan catatan (tidak dihapus)")
    s.add_argument("--id", required=True, help="ID catatan, mis. 12 atau #12")
    s.add_argument("--alasan", required=True)
    s.add_argument("--izinkan-minus", action="store_true")
    s.set_defaults(fungsi=cmd_batal)

    s = sub.add_parser("opname", parents=[umum, tulis], help="Hitung uang fisik laci/brankas vs buku")
    s.add_argument("--akun", help="Default: satu-satunya akun tunai")
    s.add_argument("--fisik", help="Total uang yang dihitung")
    s.add_argument("--pecahan", help="Rincian: '100rb x5, 50rb x3, 2rb x10, koin 3.500'")
    s.add_argument("--tanggal")
    s.add_argument("--sesuaikan", action="store_true", help="Catat selisih agar saldo buku = uang fisik")
    s.add_argument("--catatan")
    s.add_argument("--daftar", action="store_true", help="Riwayat hitung laci")
    s.add_argument("--maks", type=int, default=20)
    s.set_defaults(fungsi=cmd_opname)

    s = sub.add_parser("rekap", parents=[umum, periode], help="Rekap harian/mingguan/bulanan (teks siap Telegram)")
    s.set_defaults(fungsi=cmd_rekap)

    s = sub.add_parser("saldo", parents=[umum], help="Saldo per akun")
    s.add_argument("--tanggal")
    s.set_defaults(fungsi=cmd_saldo)

    s = sub.add_parser("daftar", parents=[umum, periode], help="Daftar catatan (dengan ID)")
    s.add_argument("--kategori")
    s.add_argument("--akun")
    s.add_argument("--cari")
    s.add_argument("--semua", action="store_true", help="Termasuk yang dibatalkan")
    s.add_argument("--maks", type=int, default=50)
    s.set_defaults(fungsi=cmd_daftar)

    s = sub.add_parser("impor", parents=[umum, tulis], help="Impor CSV buku kas / mutasi bank")
    s.add_argument("file")
    s.add_argument("--akun", help="Akun tujuan semua baris (mis. BRI untuk mutasi BRI)")
    s.add_argument("--jenis-file", choices=["mutasi-bank", "buku-kas"], help="Arti kolom Debit/Kredit")
    s.add_argument("--format-tanggal", choices=["hari-bulan", "bulan-hari"])
    s.add_argument("--tahun", type=int, help="Tahun untuk tanggal tanpa tahun (mis. mutasi '26/09')")
    s.add_argument("--kategori-default", help="Kategori untuk baris yang tidak bisa ditebak")
    s.add_argument("--tetapkan", action="append", help="Baris=kategori, mis. 7=prive, 9=pindah:laci, 12=lewati")
    s.add_argument("--sertakan-mirip", action="store_true", help="Tetap impor baris yang mirip catatan manual")
    s.add_argument("--izinkan-minus", action="store_true")
    s.set_defaults(fungsi=cmd_impor)

    s = sub.add_parser("impor-kasir", parents=[umum, tulis], help="Impor rekap harian kasir-lokal (JSON)")
    s.add_argument("file", help="Hasil: kasir.py rekap --tanggal <tgl> --json > rekap-kasir.json")
    s.add_argument("--akun-untuk", action="append", help="Metode=akun, mis. qris=BRI (bisa diulang)")
    s.add_argument("--ganti", action="store_true", help="Ganti impor tanggal yang sama (impor lama dibatalkan)")
    s.add_argument("--izinkan-minus", action="store_true")
    s.set_defaults(fungsi=cmd_impor_kasir)

    s = sub.add_parser("ekspor", parents=[umum, periode], help="Ekspor CSV: lengkap | emkm | arus-kas")
    s.add_argument("--format", choices=["lengkap", "emkm", "arus-kas"], default="lengkap")
    s.add_argument("--csv", help="File tujuan (default folder ekspor/ di sebelah database)")
    s.add_argument("--pemisah", default=";", help="Pemisah CSV (default ';' untuk Excel Indonesia)")
    s.add_argument("--minggu-riwayat", type=int, default=8, help="arus-kas: jumlah minggu riwayat (default 8)")
    s.add_argument("--semua", action="store_true", help="lengkap: termasuk yang dibatalkan")
    s.set_defaults(fungsi=cmd_ekspor)

    s = sub.add_parser("backup", parents=[umum], help="Buat cadangan / --daftar")
    s.add_argument("--daftar", action="store_true")
    s.add_argument("--label")
    s.set_defaults(fungsi=cmd_backup)
    s = sub.add_parser("restore", parents=[umum, tulis], help="Pulihkan dari cadangan")
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
    if not hasattr(args, "ya"):
        args.ya = False
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
    except sqlite3.DatabaseError as e:
        pesan = "Buku kas rusak (%s). Jangan hapus file itu. %s" % (e, SARAN_PULIH)
        return cetak(args, {"ok": False, "error": pesan, "rusak": True}, pesan, 1)
    except OSError as e:
        pesan = "File tidak bisa ditulis/dibaca (%s). Periksa folder dan izin aksesnya." % e
        return cetak(args, {"ok": False, "error": pesan}, pesan, 1)
    return cetak(args, data, teks, 0)


if __name__ == "__main__":
    sys.exit(main())
