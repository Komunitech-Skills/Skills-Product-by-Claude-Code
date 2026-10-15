#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Laporan keuangan sederhana ala SAK EMKM dari buku kas / daftar transaksi.

Menghasilkan: Laporan Laba Rugi, Laporan Posisi Keuangan (neraca sederhana),
Catatan atas Laporan Keuangan ringkas, ringkasan bahasa awam, tren per periode,
daftar transaksi yang belum terklasifikasi, dan cek keseimbangan neraca.

Hanya memakai library standar Python (3.8+). Tidak ada akses jaringan.
Semua nominal dibulatkan ke rupiah terdekat (setengah ke atas) saat dibaca,
sehingga semua penjumlahan memakai angka bulat dan totalnya pasti cocok.

Contoh:
  python3 laporan_emkm.py buku-kas.csv --nama-usaha "Warung Bu Sri" --kas-awal "Rp 2.000.000"
  python3 laporan_emkm.py buku-kas.csv --format json
  python3 laporan_emkm.py --daftar-kategori
"""
import argparse
import csv
import html
import io
import json
import os
import re
import sys
import unicodedata
from collections import OrderedDict, defaultdict
from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

VERSI = "1.3.5"

# ---------------------------------------------------------------------------
# Kategori & peran akuntansinya
# jenis:
#   pend_usaha, retur, pend_lain, jual_aset, hpp, beban_usaha, beban_keuangan,
#   beban_pph, prive, modal, pinjaman_masuk, bayar_pinjaman, bayar_utang_usaha,
#   terima_piutang, aset_tetap, transfer
# arah: masuk | keluar | dua
# ---------------------------------------------------------------------------
KATEGORI = OrderedDict([
    ("pendapatan_usaha", {"label": "Penjualan / pendapatan usaha", "jenis": "pend_usaha", "arah": "masuk"}),
    ("retur_penjualan", {"label": "Retur & pengembalian dana ke pembeli", "jenis": "retur", "arah": "keluar"}),
    ("pendapatan_lain", {"label": "Pendapatan lain-lain", "jenis": "pend_lain", "arah": "masuk"}),
    ("penjualan_aset", {"label": "Hasil penjualan aset/barang bekas usaha", "jenis": "jual_aset", "arah": "masuk"}),
    ("pembelian_bahan", {"label": "Pembelian bahan/barang dagangan", "jenis": "hpp", "arah": "keluar"}),
    ("beban_gaji", {"label": "Beban gaji & upah", "jenis": "beban_usaha", "arah": "keluar"}),
    ("beban_sewa", {"label": "Beban sewa tempat", "jenis": "beban_usaha", "arah": "keluar"}),
    ("beban_utilitas", {"label": "Beban listrik, air, gas & internet", "jenis": "beban_usaha", "arah": "keluar"}),
    ("beban_transportasi", {"label": "Beban transportasi & pengiriman", "jenis": "beban_usaha", "arah": "keluar"}),
    ("beban_pemasaran", {"label": "Beban iklan & promosi", "jenis": "beban_usaha", "arah": "keluar"}),
    ("beban_admin_penjualan", {"label": "Beban admin & komisi penjualan (marketplace, QRIS)", "jenis": "beban_usaha", "arah": "keluar"}),
    ("beban_perlengkapan", {"label": "Beban kemasan & perlengkapan", "jenis": "beban_usaha", "arah": "keluar"}),
    ("beban_perawatan", {"label": "Beban perawatan & perbaikan", "jenis": "beban_usaha", "arah": "keluar"}),
    ("beban_pajak_lain", {"label": "Beban pajak daerah, retribusi & meterai", "jenis": "beban_usaha", "arah": "keluar"}),
    ("beban_lain", {"label": "Beban lain-lain", "jenis": "beban_usaha", "arah": "keluar"}),
    ("beban_keuangan", {"label": "Beban bunga & biaya bank", "jenis": "beban_keuangan", "arah": "keluar"}),
    ("beban_pajak_penghasilan", {"label": "Beban pajak penghasilan (PPh)", "jenis": "beban_pph", "arah": "keluar"}),
    ("prive", {"label": "Prive (pengambilan pribadi pemilik)", "jenis": "prive", "arah": "keluar"}),
    ("setoran_modal", {"label": "Setoran/tambahan modal pemilik", "jenis": "modal", "arah": "masuk"}),
    ("pinjaman_diterima", {"label": "Pinjaman diterima", "jenis": "pinjaman_masuk", "arah": "masuk"}),
    ("bayar_pinjaman", {"label": "Pembayaran pokok pinjaman", "jenis": "bayar_pinjaman", "arah": "keluar"}),
    ("bayar_utang_usaha", {"label": "Pembayaran utang ke pemasok", "jenis": "bayar_utang_usaha", "arah": "keluar"}),
    ("terima_piutang", {"label": "Penerimaan piutang dari pelanggan", "jenis": "terima_piutang", "arah": "masuk"}),
    ("aset_tetap", {"label": "Pembelian aset tetap (peralatan, mesin, kendaraan)", "jenis": "aset_tetap", "arah": "keluar"}),
    ("transfer_internal", {"label": "Pindah dana antar kas/rekening sendiri", "jenis": "transfer", "arah": "dua"}),
    ("piutang_lain", {"label": "Kasbon/piutang karyawan & piutang lain-lain", "jenis": "piutang_lain", "arah": "dua"}),
    ("titipan_pajak", {"label": "Titipan pajak daerah (PB1/PBJT dipungut dari pembeli & disetor)", "jenis": "titipan",
                       "arah": "dua"}),
])

# Urutan penting: aturan pertama yang cocok (dan arahnya sesuai) yang dipakai.
# Kata kunci <= 3 huruf dicocokkan sebagai kata utuh; yang lebih panjang
# dicocokkan di awal kata (mis. "gaji" cocok dengan "gajian").
ATURAN_BAWAAN = [
    ("transfer_internal", ["setor tunai", "tarik tunai", "pindah buku", "pindahbuku", "antar rekening",
                           "pindah dana", "mutasi internal", "setor ke bank", "setoran ke bank",
                           "ambil dari bank", "tarik dari bank", "transfer ke rekening usaha",
                           "top up saldo usaha"]),
    ("piutang_lain", ["kasbon", "pinjaman karyawan", "pinjam karyawan", "uang muka karyawan",
                      "potong kasbon", "potongan kasbon", "piutang karyawan", "piutang lain"]),
    ("prive", ["prive", "privee", "pribadi", "rumah tangga", "keperluan rumah", "belanja rumah",
               "gaji pemilik", "gaji owner", "gaji sendiri", "gaji saya", "uang saku", "jajan",
               "uang sekolah", "spp", "biaya sekolah", "keluarga", "ambil uang", "ambil kas",
               "tarik modal", "kirim ortu", "kirim orang tua", "liburan"]),
    ("beban_keuangan", ["bunga pinjaman", "bunga bank", "bunga kur", "bunga kredit", "bunga cicilan",
                        "bunga utang", "bunga hutang", "admin bank", "biaya admin bank", "biaya bank",
                        "administrasi bank", "biaya transfer", "biaya tarik", "provisi"]),
    ("terima_piutang", ["piutang", "pelunasan bon", "bayar bon", "bon pelanggan", "bayar tempo",
                        "pelunasan tempo", "tagihan pelanggan", "cicilan pelanggan", "utang pelanggan",
                        "hutang pelanggan", "utang customer", "hutang customer"]),
    ("bayar_utang_usaha", ["bayar supplier", "pelunasan supplier", "utang supplier", "hutang supplier",
                           "utang dagang", "hutang dagang", "utang usaha", "hutang usaha", "bayar tempo",
                           "bon supplier", "bayar bon", "pelunasan bon", "tagihan supplier",
                           "utang toko", "hutang toko", "utang pemasok", "hutang pemasok"]),
    ("pinjaman_diterima", ["pinjaman", "pinjam", "kur", "kredit usaha", "pencairan kredit",
                           "pencairan pinjaman", "utang", "hutang", "dana talangan"]),
    ("bayar_pinjaman", ["cicilan", "angsuran", "cicil", "bayar pinjaman", "pelunasan pinjaman",
                        "bayar utang", "bayar hutang", "pelunasan utang", "pelunasan hutang", "kur",
                        "pinjaman", "kredit", "utang", "hutang"]),
    ("setoran_modal", ["modal", "setoran pemilik", "setor pemilik", "tambahan dana pemilik",
                       "suntikan dana", "dana pemilik", "investasi pemilik", "uang pribadi",
                       "dari pribadi", "tabungan pribadi"]),
    ("penjualan_aset", ["jual aset", "penjualan aset", "jual peralatan", "jual mesin", "jual motor",
                        "jual barang bekas", "rongsok", "jual rongsok"]),
    ("pendapatan_lain", ["bunga bank", "bunga tabungan", "bunga deposito", "jasa giro", "cashback",
                         "hadiah", "hibah", "bantuan", "subsidi", "bonus", "insentif", "terima sewa",
                         "pendapatan sewa", "pendapatan lain", "lain lain", "lainnya"]),
    ("pendapatan_usaha", ["penjualan", "jual", "jualan", "omzet", "omset", "pendapatan", "pemasukan",
                          "order", "orderan", "pesanan", "pembeli", "pelanggan", "customer", "konsumen",
                          "shopee", "tokopedia", "tokped", "tiktok", "lazada", "blibli", "bukalapak",
                          "gofood", "grabfood", "shopeefood", "qris", "dp", "uang muka", "pelunasan",
                          "jasa", "fee", "honor", "katering", "catering", "laku", "terjual", "setoran",
                          "transfer masuk", "kas masuk", "tunai", "cash", "hasil", "sales", "invoice",
                          "tagihan", "reseller", "grosir"]),
    ("retur_penjualan", ["retur", "refund", "pengembalian dana", "pengembalian uang", "kembalikan uang",
                         "ganti rugi pembeli"]),
    ("beban_pajak_lain", ["pajak restoran", "pb1", "pbjt", "pajak hotel", "pajak hiburan", "pajak parkir",
                          "pbb", "retribusi", "pajak kendaraan", "stnk", "samsat", "pajak reklame",
                          "bea meterai", "meterai", "materai", "perizinan", "izin usaha"]),
    ("beban_pajak_penghasilan", ["pph", "pajak penghasilan", "pajak umkm", "pajak final", "pajak omzet",
                                 "pajak omset", "pajak"]),
    ("beban_gaji", ["bpjs", "iuran bpjs"]),
    ("beban_lain", ["iuran", "keamanan", "kebersihan", "sampah"]),
    ("pembelian_bahan", ["kulakan", "kulak", "restock", "restok", "untuk dijual", "stok", "stock",
                         "barang dagangan", "dagangan", "air mineral", "air minum kemasan"]),
    ("beban_admin_penjualan", ["admin shopee", "admin tokopedia", "admin marketplace", "biaya admin",
                               "biaya layanan", "fee marketplace", "potongan marketplace", "komisi",
                               "potongan admin", "biaya platform", "mdr", "biaya qris", "potongan"]),
    ("beban_pemasaran", ["iklan", "ads", "promosi", "promo", "endorse", "brosur", "spanduk", "banner",
                         "baliho", "sponsor", "boost", "kol", "affiliate", "afiliasi", "giveaway",
                         "kartu nama", "pemasaran", "marketing"]),
    ("beban_gaji", ["gaji", "upah", "honor", "lembur", "thr", "bonus karyawan", "insentif karyawan",
                    "makan karyawan", "bpjs", "karyawan", "pegawai", "tukang", "kuli", "buruh",
                    "pekerja", "freelancer", "helper", "asisten"]),
    ("beban_sewa", ["sewa", "kontrakan", "kontrak tempat", "kontrak ruko", "ruko", "kios", "lapak",
                    "los pasar", "tempat usaha", "biaya tempat"]),
    ("beban_utilitas", ["listrik", "pln", "token", "air", "pdam", "gas", "elpiji", "lpg", "internet",
                        "wifi", "indihome", "biznet", "pulsa", "kuota", "paket data", "telepon",
                        "telpon", "galon"]),
    ("beban_transportasi", ["bensin", "bbm", "pertalite", "pertamax", "solar", "ongkir", "ongkos kirim",
                            "ongkos", "ekspedisi", "jne", "jnt", "j t", "sicepat", "anteraja",
                            "pos indonesia", "kurir", "gosend", "grabexpress", "grab", "gojek", "ojek",
                            "ojol", "maxim", "parkir", "tol", "transport", "angkut", "kirim paket",
                            "pengiriman", "tiket"]),
    ("beban_perlengkapan", ["kemasan", "packaging", "plastik", "kresek", "kardus", "dus", "box", "lakban",
                            "selotip", "isolasi", "bubble", "stiker", "label", "atk", "alat tulis",
                            "kertas", "tinta", "nota", "struk", "sabun", "pembersih", "tisu", "tissue",
                            "sedotan", "cup", "mika", "botol", "jerigen", "jeriken", "pouch", "toples", "thinwall", "styrofoam", "perlengkapan",
                            "sarung tangan", "masker"]),
    ("beban_perawatan", ["servis", "service", "perbaikan", "reparasi", "ganti oli", "oli", "tambal",
                         "ban", "sparepart", "suku cadang", "maintenance", "perawatan", "betulin",
                         "benerin", "cat ulang"]),
    ("aset_tetap", ["mesin", "etalase", "showcase", "rak", "lemari", "kulkas", "freezer", "chiller",
                    "oven", "mixer", "blender", "kompor", "dispenser", "laptop", "komputer", "printer",
                    "hp baru", "handphone", "kamera", "motor", "mobil", "gerobak", "booth", "peralatan",
                    "perabot", "meja", "kursi", "renovasi", "bangunan", "timbangan", "ac", "aset",
                    "inventaris", "cctv", "tenda", "genset", "pompa", "alat"]),
    ("pembelian_bahan", ["bahan", "belanja pasar", "pasar", "kulakan", "kulak", "stok", "stock",
                         "restock", "restok", "barang dagangan", "dagangan", "beli barang", "pembelian",
                         "supplier", "suplier", "pemasok", "grosir", "agen", "distributor", "hpp",
                         "beban pokok", "cogs", "tepung", "terigu", "gula", "telur", "telor", "minyak",
                         "mentega", "margarin", "butter", "keju", "coklat", "cokelat", "susu", "kopi",
                         "teh", "daging", "ayam", "ikan", "sayur", "buah", "beras", "bumbu", "cabe",
                         "cabai", "bawang", "santan", "kelapa", "es batu", "kain", "benang", "kancing",
                         "resleting", "sablon", "bibit", "pupuk", "pakan", "benih"]),
    ("beban_lain", ["lain lain", "lainnya", "sumbangan", "donasi", "iuran", "keamanan", "kebersihan",
                    "sampah", "konsumsi", "rapat", "fotokopi", "fotocopy", "print", "langganan",
                    "software", "aplikasi", "canva", "domain", "hosting", "pelatihan", "kursus",
                    "seminar", "asuransi", "sedekah", "zakat usaha", "denda", "biaya lain",
                    "operasional"]),
]

NAMA_BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus",
              "September", "Oktober", "November", "Desember"]
BULAN_TEKS = {
    "jan": 1, "januari": 1, "january": 1, "feb": 2, "februari": 2, "pebruari": 2, "february": 2,
    "mar": 3, "maret": 3, "march": 3, "apr": 4, "april": 4, "mei": 5, "may": 5, "jun": 6, "juni": 6,
    "june": 6, "jul": 7, "juli": 7, "july": 7, "agu": 8, "agt": 8, "ags": 8, "agus": 8, "agustus": 8,
    "aug": 8, "august": 8, "sep": 9, "sept": 9, "september": 9, "okt": 10, "oktober": 10, "oct": 10,
    "october": 10, "nov": 11, "nopember": 11, "november": 11, "des": 12, "desember": 12, "dec": 12,
    "december": 12,
}


class GalatInput(Exception):
    """Kesalahan input yang pesannya ditampilkan ke pengguna."""


# ---------------------------------------------------------------------------
# Utilitas angka & teks
# ---------------------------------------------------------------------------
def normal_teks(teks):
    t = unicodedata.normalize("NFKD", str(teks)).encode("ascii", "ignore").decode("ascii").lower()
    t = re.sub(r"[^a-z0-9]+", " ", t).strip()
    return " " + t + " "


def pola_kata(kata):
    k = normal_teks(kata).strip()
    if not k:
        return None
    if len(k.replace(" ", "")) <= 3:
        return re.compile(r"(?<![a-z0-9])" + re.escape(k) + r"(?![a-z0-9])")
    return re.compile(r"(?<![a-z0-9])" + re.escape(k))


def parse_rupiah(teks, boleh_kosong=True):
    """Ubah teks nominal gaya Indonesia menjadi Decimal (belum dibulatkan).

    Diterima: 15000, "Rp 15.000", "15.000,50", "1,250,000.50", "(15.000)", "-15.000",
    "15rb", "15 ribu", "1,5jt", "2 juta", "15k". Kosong/"-" dianggap 0.
    Mengembalikan None jika tidak bisa dibaca.
    """
    if teks is None:
        return Decimal(0) if boleh_kosong else None
    s = str(teks).strip().lower()
    if s in ("", "-", "--", "–", "—", "nihil", "0"):
        return Decimal(0) if (boleh_kosong or s == "0") else None
    negatif = False
    if s.startswith("(") and s.endswith(")"):
        negatif, s = True, s[1:-1].strip()
    s = s.replace("idr", "").replace("rp.", "").replace("rp", "").strip()
    s = re.sub(r"[.,]\s*-+$", "", s).strip()  # "15.000,-" = tanpa sen, bukan negatif
    if s.startswith("-") or s.startswith("−"):
        negatif, s = True, s[1:].strip()
    elif s.endswith("-") and len(s) > 1:
        negatif, s = True, s[:-1].strip()
    kali = Decimal(1)
    m = re.search(r"(rb|ribu|k|jt|juta)\.?$", s)
    if m:
        kali = Decimal(1000) if m.group(1) in ("rb", "ribu", "k") else Decimal(1000000)
        s = s[:m.start()].strip()
    s = s.replace(" ", "").replace(" ", "")
    if not s or not re.fullmatch(r"[\d.,]+", s) or not re.search(r"\d", s):
        return None
    if "," in s and "." in s:
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    elif "," in s:
        bagian = s.split(",")
        if len(bagian) == 2 and (len(bagian[1]) != 3 or kali != 1):
            s = s.replace(",", ".")
        elif all(len(b) == 3 for b in bagian[1:]):
            s = s.replace(",", "")
        else:
            return None
    elif "." in s:
        bagian = s.split(".")
        if len(bagian) == 2 and (len(bagian[1]) != 3 or kali != 1):
            pass  # desimal, mis. "1.5jt" atau "12.50"
        elif all(len(b) == 3 for b in bagian[1:]):
            s = s.replace(".", "")
        else:
            return None
    try:
        nilai = Decimal(s) * kali
    except InvalidOperation:
        return None
    return -nilai if negatif else nilai


def bulat(d):
    return int(Decimal(d).quantize(Decimal(1), rounding=ROUND_HALF_UP))


def rp(n):
    n = int(n)
    teks = "{:,}".format(abs(n)).replace(",", ".")
    return ("-Rp " if n < 0 else "Rp ") + teks


def rp_kurang(n):
    """Tampilkan pengurang dalam kurung, gaya laporan keuangan."""
    n = int(n)
    if n == 0:
        return "Rp 0"
    return "(" + rp(abs(n)) + ")" if n > 0 else rp(-n)


def tgl_indo(d):
    return "{} {} {}".format(d.day, NAMA_BULAN[d.month - 1], d.year)


def akhir_bulan(d):
    nxt = date(d.year + (d.month // 12), d.month % 12 + 1, 1)
    return nxt - timedelta(days=1)


def parse_tanggal(teks):
    """Kembalikan (date, dibaca_sebagai_bulan_hari) atau (None, False)."""
    if teks is None:
        return None, False
    s = str(teks).strip()
    if not s:
        return None, False
    # nomor seri tanggal Excel
    if re.fullmatch(r"\d{5}(\.0+)?", s):
        n = int(float(s))
        if 20000 < n < 80000:
            return date(1899, 12, 30) + timedelta(days=n), False
    s2 = s.split("T")[0]
    s2 = re.sub(r"\s+\d{1,2}[:.]\d{2}([:.]\d{2})?\s*$", "", s2).strip()
    m = re.fullmatch(r"(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})", s2)
    if m:
        try:
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3))), False
        except ValueError:
            return None, False
    m = re.fullmatch(r"(\d{1,2})[-/.](\d{1,2})[-/.](\d{2,4})", s2)
    if m:
        a, b, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if y < 100:
            y += 2000
        try:
            return date(y, b, a), False
        except ValueError:
            try:
                return date(y, a, b), True
            except ValueError:
                return None, False
    # nama bulan: "5 Jan 2026", "05-Januari-2026", "Jan 5, 2026", "Senin, 5 Januari 2026"
    t = re.sub(r"^[a-zA-Z]+,\s*", "", s2)
    token = [x for x in re.split(r"[\s,\-/.]+", t.lower()) if x]
    if len(token) == 3:
        angka = [x for x in token if x.isdigit()]
        huruf = [x for x in token if not x.isdigit()]
        if len(angka) == 2 and len(huruf) == 1 and huruf[0] in BULAN_TEKS:
            bln = BULAN_TEKS[huruf[0]]
            besar = [int(x) for x in angka]
            y = max(besar) if max(besar) > 31 else None
            if y is None:
                return None, False
            d = [x for x in besar if x != y] or [y]
            try:
                return date(y, bln, d[0]), False
            except ValueError:
                return None, False
    return None, False


# ---------------------------------------------------------------------------
# Pembacaan tabel
# ---------------------------------------------------------------------------
NAMA_KOLOM = {
    "tanggal": ["tanggal", "tgl", "date", "waktu", "hari tanggal", "tanggal transaksi"],
    "keterangan": ["keterangan", "ket", "uraian", "deskripsi", "description", "catatan", "transaksi",
                   "nama transaksi", "memo", "rincian", "item", "detail", "perihal"],
    "masuk": ["masuk", "uang masuk", "pemasukan", "penerimaan", "kas masuk", "income", "in",
              "pendapatan", "dana masuk"],
    "keluar": ["keluar", "uang keluar", "pengeluaran", "kas keluar", "expense", "expenses", "out",
               "biaya", "dana keluar"],
    "kategori": ["kategori", "category", "akun", "pos", "kelompok", "jenis biaya", "kategori transaksi"],
    "jumlah": ["jumlah", "nominal", "nilai", "amount", "total", "rp", "jumlah rp", "nominal rp"],
    "jenis": ["jenis", "tipe", "type", "arah", "masuk keluar", "m k", "d k", "db cr", "status"],
    "saldo": ["saldo", "balance", "saldo akhir"],
}
KOLOM_AMBIGU = ["debit", "debet", "kredit", "credit", "db", "cr"]


def cari_kolom(header, peran, paksa=None):
    norm = [normal_teks(h).strip() for h in header]
    if paksa:
        target = normal_teks(paksa).strip()
        for i, h in enumerate(norm):
            if h == target:
                return i
        raise GalatInput("Kolom '{}' tidak ditemukan. Kolom yang ada: {}".format(
            paksa, ", ".join(header)))
    for nama in NAMA_KOLOM[peran]:
        for i, h in enumerate(norm):
            if h == nama:
                return i
    # cocok sebagian (mis. "Uang Masuk (Rp)")
    for nama in NAMA_KOLOM[peran]:
        if len(nama) < 4:
            continue
        for i, h in enumerate(norm):
            if h.startswith(nama + " ") or h.endswith(" " + nama):
                return i
    return None


def baca_teks(path):
    if path == "-":
        data = sys.stdin.buffer.read()
        nama = "(input tempel)"
    else:
        if not os.path.exists(path):
            raise GalatInput("File '{}' tidak ditemukan. Periksa nama dan lokasi file.".format(path))
        if os.path.isdir(path):
            raise GalatInput("'{}' adalah folder, bukan file.".format(path))
        with open(path, "rb") as f:
            data = f.read()
        nama = os.path.basename(path)
    if not data.strip():
        raise GalatInput("File kosong. Isi minimal: baris judul kolom + 1 baris transaksi.")
    if data[:2] == b"PK":
        raise GalatInput("File ini tampaknya Excel (.xlsx) atau ZIP. Buka di Excel/Google Sheets, lalu "
                         "simpan/unduh sebagai CSV (File > Download > CSV), kemudian coba lagi.")
    if data[:4] == b"%PDF":
        raise GalatInput("File ini PDF. Script hanya membaca CSV/teks tabel. Salin tabelnya ke CSV dulu.")
    if b"\x00" in data[:4096] and not data.startswith((b"\xff\xfe", b"\xfe\xff")):
        raise GalatInput("File tidak bisa dibaca sebagai teks (kemungkinan rusak atau bukan CSV).")
    for enc in ("utf-8-sig", "utf-16", "cp1252", "latin-1"):
        try:
            teks = data.decode(enc)
            if enc == "utf-16" and not data.startswith((b"\xff\xfe", b"\xfe\xff")):
                continue
            return teks, nama
        except UnicodeDecodeError:
            continue
    raise GalatInput("File tidak bisa dibaca sebagai teks.")


def pecah_baris(teks):
    """Kembalikan list baris (list sel) beserta nomor baris aslinya."""
    baris_mentah = teks.splitlines()
    isi = [b for b in baris_mentah if b.strip()]
    if not isi:
        raise GalatInput("File tidak berisi data.")
    # Tabel Markdown (hasil tempel dari chat)
    if sum(1 for b in isi if b.strip().startswith("|")) >= max(2, len(isi) // 2):
        hasil = []
        for no, b in enumerate(baris_mentah, start=1):
            s = b.strip()
            if not s.startswith("|"):
                continue
            sel = [c.strip() for c in s.strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c or "--") for c in sel):
                continue
            hasil.append((no, sel))
        return hasil
    contoh = isi[:15]
    kandidat = ["\t", ";", "|", ","]
    skor = {}
    for d in kandidat:
        jumlah = [len(next(csv.reader([b], delimiter=d))) for b in contoh]
        umum = max(set(jumlah), key=jumlah.count)
        skor[d] = (umum if umum > 1 else 0, jumlah.count(umum))
    delim = max(kandidat, key=lambda d: skor[d])
    if skor[delim][0] == 0:
        # mungkin dipisah 2+ spasi (tempel dari tabel)
        hasil = []
        for no, b in enumerate(baris_mentah, start=1):
            if b.strip():
                hasil.append((no, [c.strip() for c in re.split(r"\s{2,}", b.strip())]))
        if max(len(r) for _, r in hasil) > 1:
            return hasil
        raise GalatInput("Tidak menemukan pemisah kolom (koma, titik koma, tab, atau '|'). "
                         "Pastikan data berbentuk tabel dengan judul kolom.")
    hasil = []
    pembaca = csv.reader(io.StringIO(teks), delimiter=delim)
    for sel in pembaca:
        no = pembaca.line_num
        if any(c.strip() for c in sel):
            hasil.append((no, [c.strip() for c in sel]))
    return hasil


def temukan_header(baris, a):
    for idx, (_, sel) in enumerate(baris[:15]):
        n_kenal = 0
        for peran in ("tanggal", "keterangan", "masuk", "keluar", "jumlah", "kategori"):
            try:
                if cari_kolom(sel, peran) is not None:
                    n_kenal += 1
            except GalatInput:
                pass
        if n_kenal >= 2:
            return idx
    if any(getattr(a, "kolom_" + k) for k in ("tanggal", "keterangan", "masuk", "keluar", "jumlah")):
        return 0
    raise GalatInput("Judul kolom tidak dikenali. Minimal perlu kolom Tanggal, Keterangan, dan "
                     "Masuk/Keluar (atau Jumlah). Contoh judul: Tanggal,Keterangan,Masuk,Keluar,Kategori")


def ke_arah(teks, debit_artinya):
    t = normal_teks(teks).strip()
    if t in ("masuk", "in", "pemasukan", "penerimaan", "income", "m", "plus", "kas masuk", "uang masuk"):
        return "masuk"
    if t in ("keluar", "out", "pengeluaran", "biaya", "expense", "k", "minus", "kas keluar", "uang keluar"):
        return "keluar"
    if t in ("debit", "debet", "db", "d", "dr"):
        if not debit_artinya:
            raise GalatInput("Kolom jenis berisi 'Debit/Kredit' yang artinya bisa terbalik (buku kas vs "
                             "mutasi bank). Jalankan ulang dengan --debit-artinya masuk atau "
                             "--debit-artinya keluar.")
        return debit_artinya
    if t in ("kredit", "credit", "cr", "c"):
        if not debit_artinya:
            raise GalatInput("Kolom jenis berisi 'Debit/Kredit'. Jalankan ulang dengan "
                             "--debit-artinya masuk atau --debit-artinya keluar.")
        return "keluar" if debit_artinya == "masuk" else "masuk"
    return None


# ---------------------------------------------------------------------------
# Klasifikasi
# ---------------------------------------------------------------------------
def siapkan_aturan(path_pemetaan):
    kategori = OrderedDict((k, dict(v)) for k, v in KATEGORI.items())
    aturan_kustom = []
    if path_pemetaan:
        if not os.path.isfile(path_pemetaan):
            raise GalatInput("File pemetaan '{}' tidak ditemukan.".format(path_pemetaan))
        try:
            with open(path_pemetaan, encoding="utf-8-sig") as f:
                data = json.load(f)
        except (ValueError, UnicodeDecodeError) as e:
            raise GalatInput("File pemetaan bukan JSON yang valid: {}".format(e))
        if not isinstance(data, dict):
            raise GalatInput('File pemetaan harus berbentuk {"kode_kategori": ["kata kunci", ...]}.')
        for kode, isi in data.items():
            if str(kode).startswith("_"):
                continue  # komentar
            label = None
            if isinstance(isi, dict):
                label = isi.get("label")
                kata = isi.get("kata", isi.get("kata_kunci", []))
            else:
                kata = isi
            if isinstance(kata, str):
                kata = [kata]
            if not isinstance(kata, list) or not all(isinstance(x, str) for x in kata):
                raise GalatInput("Isi pemetaan untuk '{}' harus daftar kata kunci (teks).".format(kode))
            if kode not in kategori:
                if re.fullmatch(r"beban_[a-z0-9_]+", kode):
                    kategori[kode] = {"label": label or kode.replace("_", " ").capitalize(),
                                      "jenis": "beban_usaha", "arah": "keluar"}
                elif re.fullmatch(r"pendapatan_[a-z0-9_]+", kode):
                    kategori[kode] = {"label": label or kode.replace("_", " ").capitalize(),
                                      "jenis": "pend_usaha", "arah": "masuk"}
                else:
                    raise GalatInput("Kode kategori '{}' tidak dikenal. Pakai kode yang ada (lihat "
                                     "--daftar-kategori) atau kode baru berawalan 'beban_' / "
                                     "'pendapatan_'.".format(kode))
            elif label:
                kategori[kode]["label"] = label
            aturan_kustom.append((kode, kata))
    aturan = []
    for kode, kata in aturan_kustom + ATURAN_BAWAAN:
        pola = [p for p in (pola_kata(k) for k in kata) if p]
        aturan.append((kode, pola, kode in dict(aturan_kustom)))
    return kategori, aturan


POLA_PB1 = re.compile(r"(?<![a-z0-9])(pb1|pbjt|pajak (restoran|hotel|hiburan|parkir))")
POLA_TANPA_PB1 = re.compile(r"(belum|tidak|tanpa|exclude|excl|di ?luar) (termasuk )?(pb1|pbjt|pajak)")


def sebut_pb1(teks):
    """Baris yang benar-benar tentang PB1/PBJT (bukan sekadar 'belum termasuk PB1')."""
    t = normal_teks(teks)
    return bool(POLA_PB1.search(t)) and not POLA_TANPA_PB1.search(t)


def klasifikasi(teks, arah, kategori, aturan):
    t = normal_teks(teks)
    pb1_masuk = arah == "masuk" and sebut_pb1(teks)
    for kode, pola, kustom in aturan:
        if pb1_masuk and not kustom:
            return None  # PB1 dari pembeli bukan penjualan: ditanyakan (titipan)
        info = kategori[kode]
        if info["arah"] not in (arah, "dua"):
            continue
        for p in pola:
            if p.search(t):
                return kode
    return None


def kode_dari_kolom_kategori(nilai, arah, kategori, aturan):
    if not nilai or not str(nilai).strip():
        return None
    n = normal_teks(nilai).strip()
    for kode, info in kategori.items():
        if info["arah"] not in (arah, "dua"):
            continue
        if n == normal_teks(kode).strip() or n == normal_teks(info["label"]).strip():
            return kode
    return klasifikasi(nilai, arah, kategori, aturan)


# ---------------------------------------------------------------------------
# Proses utama
# ---------------------------------------------------------------------------
def muat_transaksi(a, kategori, aturan):
    teks, nama_file = baca_teks(a.file)
    baris = pecah_baris(teks)
    ih = temukan_header(baris, a)
    header = baris[ih][1]
    k = {}
    for peran in ("tanggal", "keterangan", "masuk", "keluar", "kategori", "jumlah", "jenis", "saldo"):
        k[peran] = cari_kolom(header, peran, getattr(a, "kolom_" + peran, None))
    if k["tanggal"] is None:
        raise GalatInput("Kolom tanggal tidak ditemukan. Kolom yang ada: {}. Pakai --kolom-tanggal "
                         "\"<nama kolom>\".".format(", ".join(header)))
    if k["keterangan"] is None:
        raise GalatInput("Kolom keterangan tidak ditemukan. Kolom yang ada: {}. Pakai "
                         "--kolom-keterangan \"<nama kolom>\".".format(", ".join(header)))
    mode_jumlah = k["masuk"] is None and k["keluar"] is None
    if mode_jumlah and k["jumlah"] is None:
        ambigu = [h for h in header if normal_teks(h).strip() in KOLOM_AMBIGU]
        if ambigu:
            raise GalatInput("Kolom {} bisa berarti uang masuk ATAU keluar (buku kas vs mutasi bank "
                             "terbalik). Tentukan dengan --kolom-masuk dan --kolom-keluar.".format(
                                 " / ".join(ambigu)))
        raise GalatInput("Kolom nominal tidak ditemukan. Perlu kolom Masuk dan/atau Keluar, atau "
                         "kolom Jumlah. Kolom yang ada: {}".format(", ".join(header)))

    transaksi, bermasalah, dilewati = [], [], defaultdict(int)
    saldo_awal_baris, saldo_kolom_terakhir = None, None
    n_bulan_hari = 0
    n_kurung_keluar = 0
    tgl_saldo_awal = None
    for no, sel in baris[ih + 1:]:
        def ambil(peran):
            i = k[peran]
            return sel[i] if (i is not None and i < len(sel)) else ""
        ket = ambil("keterangan").strip()
        ket_n = normal_teks(ket).strip()
        mentah_tgl = ambil("tanggal")
        if normal_teks(sel[k["tanggal"]] if k["tanggal"] < len(sel) else "").strip() == \
                normal_teks(header[k["tanggal"]]).strip():
            continue  # judul kolom berulang
        # baris saldo / total
        if re.match(r"^(saldo awal|saldo sebelumnya|saldo bulan lalu|sisa saldo)", ket_n):
            nilai = parse_rupiah(ambil("masuk")) if k["masuk"] is not None else None
            if not nilai:
                nilai = parse_rupiah(ambil("saldo")) if k["saldo"] is not None else None
            if not nilai and k["jumlah"] is not None:
                nilai = parse_rupiah(ambil("jumlah"))
            if nilai is not None:
                saldo_awal_baris = bulat(nilai)
                tgl_saldo_awal = parse_tanggal(mentah_tgl)[0]
            dilewati["baris saldo awal (dipakai sebagai kas awal bila --kas-awal tidak diisi)"] += 1
            continue
        tgl_n = normal_teks(mentah_tgl).strip()
        if re.match(r"^(total|jumlah|sub ?total|grand total|saldo akhir|saldo)$", ket_n) or \
                (not mentah_tgl.strip() and re.match(r"^(total|jumlah|saldo)", ket_n)) or \
                re.match(r"^(total|jumlah|sub ?total|grand total|saldo)\b", tgl_n):
            dilewati["baris total/saldo (bukan transaksi)"] += 1
            continue
        if k["saldo"] is not None:
            sv = parse_rupiah(ambil("saldo"), boleh_kosong=False)
            if sv is not None:
                saldo_kolom_terakhir = bulat(sv)
        tgl, bh = parse_tanggal(mentah_tgl)
        if tgl is None:
            bermasalah.append({"baris": no, "alasan": "tanggal tidak terbaca: '{}'".format(mentah_tgl),
                               "keterangan": ket})
            continue
        n_bulan_hari += 1 if bh else 0
        # nominal
        masuk = keluar = Decimal(0)
        if not mode_jumlah:
            vm = parse_rupiah(ambil("masuk")) if k["masuk"] is not None else Decimal(0)
            vk = parse_rupiah(ambil("keluar")) if k["keluar"] is not None else Decimal(0)
            if vm is None or vk is None:
                bermasalah.append({"baris": no, "alasan": "nominal tidak terbaca: masuk='{}' keluar='{}'".format(
                    ambil("masuk"), ambil("keluar")), "keterangan": ket})
                continue
            if vm < 0:
                bermasalah.append({"baris": no, "alasan": "nilai minus/dalam kurung di kolom Masuk ('{}'); "
                                   "apakah ini koreksi, retur, atau uang keluar?".format(ambil("masuk")),
                                   "keterangan": ket})
                continue
            if vk < 0:
                vk = -vk  # "(200.000)" di kolom Keluar = uang keluar, bukan dibalik jadi masuk
                n_kurung_keluar += 1
            masuk, keluar = vm, vk
        else:
            v = parse_rupiah(ambil("jumlah"), boleh_kosong=False)
            if v is None:
                bermasalah.append({"baris": no, "alasan": "nominal tidak terbaca: '{}'".format(ambil("jumlah")),
                                   "keterangan": ket})
                continue
            arah = ke_arah(ambil("jenis"), a.debit_artinya) if k["jenis"] is not None else None
            if arah is None and k["jenis"] is not None and ambil("jenis").strip():
                bermasalah.append({"baris": no, "alasan": "jenis transaksi tidak dikenal: '{}'".format(
                    ambil("jenis")), "keterangan": ket})
                continue
            if arah is None:
                arah = "keluar" if v < 0 else "masuk"
            if arah == "masuk":
                masuk = abs(v)
            else:
                keluar = abs(v)
        masuk, keluar = bulat(masuk), bulat(keluar)
        if masuk and keluar:
            bermasalah.append({"baris": no, "alasan": "kolom masuk DAN keluar sama-sama terisi; pisahkan "
                               "menjadi dua baris", "keterangan": ket})
            continue
        if not masuk and not keluar:
            dilewati["nominal kosong/nol"] += 1
            continue
        arah = "masuk" if masuk else "keluar"
        nilai = masuk or keluar
        transaksi.append({"baris": no, "tanggal": tgl, "keterangan": ket, "arah": arah, "nilai": nilai,
                          "kategori_asli": ambil("kategori").strip()})
    return {
        "nama_file": nama_file, "header": header, "transaksi": transaksi, "bermasalah": bermasalah,
        "dilewati": dict(dilewati), "saldo_awal_baris": saldo_awal_baris,
        "saldo_kolom_terakhir": saldo_kolom_terakhir, "n_bulan_hari": n_bulan_hari,
        "n_kurung_keluar": n_kurung_keluar, "tgl_saldo_awal": tgl_saldo_awal,
    }


def daftar_bulan(awal, akhir):
    hasil, y, m = [], awal.year, awal.month
    while (y, m) <= (akhir.year, akhir.month):
        hasil.append((y, m))
        m += 1
        if m > 12:
            y, m = y + 1, 1
    return hasil


def kunci_periode(d, mode):
    if mode == "bulan":
        return "{}-{:02d}".format(d.year, d.month), "{} {}".format(NAMA_BULAN[d.month - 1][:3], d.year)
    if mode == "kuartal":
        q = (d.month - 1) // 3 + 1
        return "{}-Q{}".format(d.year, q), "Kuartal {} {}".format(q, d.year)
    return str(d.year), "Tahun {}".format(d.year)


def hitung(a):
    kategori, aturan = siapkan_aturan(a.pemetaan)
    data = muat_transaksi(a, kategori, aturan)
    trx_semua = data["transaksi"]
    if not trx_semua:
        alasan = "; ".join("baris {}: {}".format(b["baris"], b["alasan"]) for b in data["bermasalah"][:5])
        lewat = "; ".join("{}: {} baris".format(k, v) for k, v in data["dilewati"].items())
        raise GalatInput("Tidak ada transaksi valid yang bisa diproses." +
                         (" Contoh masalah: " + alasan + "." if alasan else "") +
                         (" Baris dilewati: " + lewat + "." if lewat else ""))
    tetapkan = {}
    for t in a.tetapkan or []:
        m = re.fullmatch(r"\s*(\d+)\s*=\s*([a-z0-9_]+)\s*", t)
        if not m:
            raise GalatInput("Format --tetapkan salah: '{}'. Contoh benar: --tetapkan 12=prive".format(t))
        if m.group(2) not in kategori:
            raise GalatInput("Kode kategori '{}' pada --tetapkan tidak dikenal. Lihat --daftar-kategori.".format(
                m.group(2)))
        tetapkan[int(m.group(1))] = m.group(2)

    peringatan, asumsi = [], []
    # periode
    tgl_min = min(t["tanggal"] for t in trx_semua)
    tgl_max = max(t["tanggal"] for t in trx_semua)
    p_awal = parse_tanggal(a.periode_awal)[0] if a.periode_awal else date(tgl_min.year, tgl_min.month, 1)
    p_akhir = parse_tanggal(a.periode_akhir)[0] if a.periode_akhir else akhir_bulan(tgl_max)
    if (a.periode_awal and p_awal is None) or (a.periode_akhir and p_akhir is None):
        raise GalatInput("Format --periode-awal/--periode-akhir tidak terbaca. Contoh: 2026-01-01")
    if p_awal > p_akhir:
        raise GalatInput("Periode awal lebih besar dari periode akhir.")
    if not a.periode_awal:
        asumsi.append("Periode laporan dianggap {} s.d. {} (bulan penuh dari transaksi pertama sampai "
                      "terakhir).".format(tgl_indo(p_awal), tgl_indo(p_akhir)))
    if data["n_bulan_hari"]:
        peringatan.append("{} tanggal hanya bisa dibaca sebagai bulan/hari (format Amerika). Cek apakah "
                          "tanggalnya benar.".format(data["n_bulan_hari"]))

    # klasifikasi
    for t in trx_semua:
        kode, sumber = None, None
        if t["baris"] in tetapkan:
            kode, sumber = tetapkan[t["baris"]], "ditetapkan pengguna"
            if kategori[kode]["arah"] not in (t["arah"], "dua"):
                raise GalatInput("Baris {} adalah uang {} tetapi ditetapkan ke '{}' yang khusus uang {}.".format(
                    t["baris"], t["arah"], kode, kategori[kode]["arah"]))
        if kode is None and t["kategori_asli"]:
            kode = kode_dari_kolom_kategori(t["kategori_asli"], t["arah"], kategori, aturan)
            sumber = "kolom kategori" if kode else None
        if kode is None:
            kode = klasifikasi(t["keterangan"], t["arah"], kategori, aturan)
            sumber = "kata kunci" if kode else None
        t["kode"], t["sumber"] = kode, sumber

    # pemisahan bunga dari angsuran (--bunga BARIS=NOMINAL)
    tambahan = []
    for isi in a.bunga or []:
        m = re.fullmatch(r"\s*(\d+)\s*=\s*(.+?)\s*", isi)
        if not m:
            raise GalatInput("Format --bunga salah: '{}'. Contoh benar: --bunga 25=208.334".format(isi))
        no_baris = int(m.group(1))
        v = parse_rupiah(m.group(2), boleh_kosong=False)
        if v is None or v < 0:
            raise GalatInput("Nominal bunga '{}' tidak terbaca.".format(m.group(2)))
        v = bulat(v)
        cocok = [t for t in trx_semua if t["baris"] == no_baris]
        if not cocok:
            raise GalatInput("Baris {} pada --bunga tidak ditemukan sebagai transaksi.".format(no_baris))
        t = cocok[0]
        if t["arah"] != "keluar":
            raise GalatInput("Baris {} adalah uang masuk; --bunga hanya untuk angsuran (uang keluar).".format(no_baris))
        if v > t["nilai"]:
            raise GalatInput("Bunga baris {} ({}) lebih besar dari nominal angsurannya ({}).".format(
                no_baris, rp(v), rp(t["nilai"])))
        t["bunga_dikonfirmasi"] = True
        if t["kode"] in (None, "beban_keuangan"):
            t["kode"], t["sumber"] = "bayar_pinjaman", "angsuran (dipisah --bunga)"
        if v == 0:
            continue
        if v == t["nilai"]:
            t["kode"], t["sumber"] = "beban_keuangan", "bunga (--bunga)"
            continue
        t["nilai"] -= v
        b = dict(t)
        b.update({"nilai": v, "kode": "beban_keuangan", "sumber": "bunga dipisah dari angsuran (--bunga)",
                  "keterangan": t["keterangan"] + " [bagian bunga]"})
        tambahan.append(b)
        t["keterangan"] = t["keterangan"] + " [bagian pokok]"
    trx_semua.extend(tambahan)
    trx_semua.sort(key=lambda t: (t["tanggal"], t["baris"], t["kode"] == "beban_keuangan"))

    trx = [t for t in trx_semua if p_awal <= t["tanggal"] <= p_akhir]
    sebelum = [t for t in trx_semua if t["tanggal"] < p_awal]
    sesudah = [t for t in trx_semua if t["tanggal"] > p_akhir]
    if sesudah:
        peringatan.append("{} transaksi setelah {} tidak dihitung.".format(len(sesudah), tgl_indo(p_akhir)))
    if not trx:
        raise GalatInput("Tidak ada transaksi di dalam periode {} s.d. {}.".format(p_awal, p_akhir))
    tak_terklasifikasi = [t for t in trx if t["kode"] is None]

    def uang(x, default=0):
        if x is None:
            return default
        v = parse_rupiah(x, boleh_kosong=False)
        if v is None:
            raise GalatInput("Nominal '{}' tidak terbaca. Tulis angka, mis. 'Rp 1.500.000', '1500000', "
                             "atau '1,5jt'.".format(x))
        return bulat(v)

    # saldo awal
    kas_awal = uang(a.kas_awal, None)
    if kas_awal is None:
        if data["saldo_awal_baris"] is not None:
            kas_awal = data["saldo_awal_baris"]
            asumsi.append("Kas awal diambil dari baris 'saldo awal' di file: {}.".format(rp(kas_awal)))
        else:
            kas_awal = 0
            asumsi.append("Kas awal tidak diberikan, dianggap Rp 0.")
    piutang_awal = uang(a.piutang_awal)
    persediaan_awal = uang(a.persediaan_awal)
    aset_tetap_awal = uang(a.aset_tetap_awal)
    utang_usaha_awal = uang(a.utang_usaha_awal)
    utang_bank_awal = uang(a.utang_bank_awal)
    for nama, nilai in (("piutang", a.piutang_awal), ("persediaan (stok)", a.persediaan_awal),
                        ("aset tetap", a.aset_tetap_awal), ("utang ke pemasok", a.utang_usaha_awal),
                        ("utang bank/pinjaman", a.utang_bank_awal)):
        if nilai is None:
            asumsi.append("Saldo awal {} tidak diberikan, dianggap Rp 0 (per awal data).".format(nama))
    pertanyaan_awal = []
    piutang_lain_awal = uang(a.piutang_lain_awal)
    titipan_pajak_awal = uang(a.titipan_pajak_awal)
    modal_input = uang(a.modal_awal, None)
    kas_dari_baris = a.kas_awal is None and data["saldo_awal_baris"] is not None
    mode_saldo = a.saldo_awal_per or "awal-file"
    tgl_file = min([t["tanggal"] for t in trx_semua] + [p_awal])
    if data.get("tgl_saldo_awal") and data["tgl_saldo_awal"] < tgl_file:
        tgl_file = data["tgl_saldo_awal"]
    # daftar aset untuk penyusutan per bulan dari HARGA PEROLEHAN: (biaya, bulan mulai disusutkan)
    daftar_aset = []
    if aset_tetap_awal:
        mulai_aset = (p_awal.year, p_awal.month) if (sebelum and mode_saldo == "awal-periode"
                                                     and a.aset_tetap_awal is not None) \
            else (tgl_file.year, tgl_file.month)
        daftar_aset.append((aset_tetap_awal, mulai_aset))
    for t in trx_semua:
        if t["kode"] == "aset_tetap" and not (sebelum and mode_saldo == "awal-periode" and a.aset_tetap_awal
                                              is not None and t["tanggal"] < p_awal):
            ym = (t["tanggal"].year + (t["tanggal"].month // 12), t["tanggal"].month % 12 + 1)
            daftar_aset.append((t["nilai"], ym))

    def penyusutan_bulan(ym):
        if a.umur_aset_tahun is None or a.umur_aset_tahun <= 0:
            return 0
        bu = Decimal(str(a.umur_aset_tahun)) * 12
        d = Decimal(0)
        for biaya, mulai in daftar_aset:
            ke = (ym[0] - mulai[0]) * 12 + ym[1] - mulai[1]
            if 0 <= ke < bu:
                d += Decimal(biaya) / bu
        return bulat(d)

    dep_sebelum = 0
    dana_lain_awal = 0
    if sebelum:
        def js(jenis, arah=None):
            return sum(t["nilai"] for t in sebelum if t["kode"] and kategori[t["kode"]]["jenis"] == jenis
                       and (arah is None or t["arah"] == arah))
        m_seb = sum(t["nilai"] for t in sebelum if t["arah"] == "masuk")
        k_seb = sum(t["nilai"] for t in sebelum if t["arah"] == "keluar")
        # dana yang dipindah ke rekening lain tetap termasuk kas & setara kas
        geser_kas = m_seb - k_seb + js("transfer", "keluar") - js("transfer", "masuk")
        # pos yang diberikan pengguna pada mode awal-periode TIDAK digulir; sisanya digulir dari awal data
        diberi = {"kas": a.kas_awal is not None, "piutang": a.piutang_awal is not None,
                  "aset": a.aset_tetap_awal is not None, "uu": a.utang_usaha_awal is not None,
                  "ub": a.utang_bank_awal is not None, "pl": a.piutang_lain_awal is not None,
                  "tp": a.titipan_pajak_awal is not None,
                  "modal": a.modal_awal is not None}

        def gulir(pos):
            return mode_saldo == "awal-file" or not diberi[pos]
        aset0 = kas_awal + piutang_awal + persediaan_awal + aset_tetap_awal + piutang_lain_awal
        liab0 = utang_usaha_awal + utang_bank_awal + titipan_pajak_awal
        if gulir("kas"):
            kas_awal += geser_kas
            dana_lain_awal = js("transfer", "keluar") - js("transfer", "masuk")
        if gulir("piutang"):
            piutang_awal = max(0, piutang_awal - js("terima_piutang"))
        if gulir("uu"):
            utang_usaha_awal = max(0, utang_usaha_awal - js("bayar_utang_usaha"))
        if gulir("ub"):
            utang_bank_awal += js("pinjaman_masuk") - js("bayar_pinjaman")
        if gulir("pl"):
            piutang_lain_awal += js("piutang_lain", "keluar") - js("piutang_lain", "masuk")
        if gulir("tp"):
            titipan_pajak_awal += js("titipan", "masuk") - js("titipan", "keluar")
        if gulir("aset"):
            bln_seb = daftar_bulan(date(tgl_file.year, tgl_file.month, 1), p_awal - timedelta(days=1))
            dep_sebelum = sum(penyusutan_bulan(ym) for ym in bln_seb)
            aset_tetap_awal = max(0, aset_tetap_awal + js("aset_tetap") - dep_sebelum)
        # piutang & utang pemasok per awal periode (penjualan/pembelian tempo sebelum periode tidak tercatat di kas)
        if a.piutang_awal_periode is not None:
            piutang_awal = uang(a.piutang_awal_periode)
        if a.utang_usaha_awal_periode is not None:
            utang_usaha_awal = uang(a.utang_usaha_awal_periode)
        aset1 = kas_awal + piutang_awal + persediaan_awal + aset_tetap_awal + piutang_lain_awal
        liab1 = utang_usaha_awal + utang_bank_awal + titipan_pajak_awal
        if modal_input is not None and gulir("modal"):
            modal_input += (aset1 - liab1) - (aset0 - liab0)
        if mode_saldo == "awal-file":
            asumsi.append("Saldo awal yang Anda berikan/dibaca dari file dianggap per awal data ({}), lalu "
                          "digulirkan dengan {} transaksi sebelum {}. Kas awal periode = {}; modal awal periode "
                          "sudah termasuk laba/prive sebelum periode. Stok awal (--persediaan-awal) dipakai sebagai "
                          "stok per {}.".format(tgl_indo(tgl_file), len(sebelum), tgl_indo(p_awal), rp(kas_awal),
                                                tgl_indo(p_awal)))
        else:
            tetap = [n for n, k in (("kas", "kas"), ("piutang", "piutang"), ("aset tetap", "aset"),
                                    ("utang pemasok", "uu"), ("utang bank", "ub"), ("kasbon", "pl")) if diberi[k]]
            asumsi.append("Saldo awal yang Anda isi ({}) dianggap sudah per {}; pos lain digulirkan dari {} "
                          "transaksi sebelumnya.".format(", ".join(tetap) or "-", tgl_indo(p_awal), len(sebelum)))
        if dep_sebelum:
            asumsi.append("Penyusutan sebelum periode ({}) sudah dikurangkan dari aset tetap awal.".format(
                rp(dep_sebelum)))
        if a.persediaan_awal is None:
            peringatan.append("Stok awal per {} tidak diberikan, dianggap Rp 0. Isi --persediaan-awal dengan hasil "
                              "hitung stok per tanggal itu.".format(tgl_indo(p_awal)))
        ada_piutang = bool(uang(a.piutang_awal) or any(t["kode"] == "terima_piutang" for t in trx_semua) or
                           (a.piutang_akhir is not None and uang(a.piutang_akhir)))
        ada_utang = bool(uang(a.utang_usaha_awal) or any(t["kode"] == "bayar_utang_usaha" for t in trx_semua) or
                         (a.utang_usaha_akhir is not None and uang(a.utang_usaha_akhir)))
        if ada_piutang and a.piutang_awal_periode is None and gulir("piutang"):
            pertanyaan_awal.append("Berapa piutang pelanggan (penjualan tempo yang belum dibayar) per {}? "
                                   "Jawab lalu jalankan ulang dengan --piutang-awal-periode <nominal> (0 bila tidak "
                                   "ada).".format(tgl_indo(p_awal)))
        if ada_utang and a.utang_usaha_awal_periode is None and gulir("uu"):
            pertanyaan_awal.append("Berapa utang ke pemasok (bon/tempo yang belum dibayar) per {}? Jawab lalu "
                                   "jalankan ulang dengan --utang-usaha-awal-periode <nominal> (0 bila tidak "
                                   "ada).".format(tgl_indo(p_awal)))
        n_tak_seb = sum(1 for t in sebelum if t["kode"] is None)
        if n_tak_seb:
            peringatan.append("{} transaksi sebelum periode belum terklasifikasi; kas awal tetap benar, tetapi "
                              "utang/piutang awal bisa kurang tepat.".format(n_tak_seb))
    else:
        if a.piutang_awal_periode is not None:
            piutang_awal = uang(a.piutang_awal_periode)
        if a.utang_usaha_awal_periode is not None:
            utang_usaha_awal = uang(a.utang_usaha_awal_periode)
        if a.periode_awal:
            asumsi.append("Saldo awal (kas, piutang, stok, utang, aset) harus per {}.".format(tgl_indo(p_awal)))

    # agregasi per kode
    total = defaultdict(int)
    masuk_tak, keluar_tak = 0, 0
    for t in trx:
        if t["kode"]:
            total[t["kode"]] += t["nilai"]
        elif t["arah"] == "masuk":
            masuk_tak += t["nilai"]
        else:
            keluar_tak += t["nilai"]

    def jumlah_jenis(jenis):
        return sum(v for kd, v in total.items() if kategori[kd]["jenis"] == jenis)

    def jumlah_jenis_arah(jenis, arah):
        return sum(t["nilai"] for t in trx if t["kode"] and kategori[t["kode"]]["jenis"] == jenis and t["arah"] == arah)

    total_masuk = sum(t["nilai"] for t in trx if t["arah"] == "masuk")
    total_keluar = sum(t["nilai"] for t in trx if t["arah"] == "keluar")
    transfer_masuk = sum(t["nilai"] for t in trx if t["kode"] == "transfer_internal" and t["arah"] == "masuk")
    transfer_keluar = sum(t["nilai"] for t in trx if t["kode"] == "transfer_internal" and t["arah"] == "keluar")
    dana_di_rekening_lain = transfer_keluar - transfer_masuk

    # --- Pendapatan (dengan penyesuaian piutang)
    pend_usaha_tunai = jumlah_jenis("pend_usaha")
    terima_piutang = jumlah_jenis("terima_piutang")
    if a.piutang_akhir is not None:
        piutang_akhir = uang(a.piutang_akhir)
    else:
        piutang_akhir = max(0, piutang_awal - terima_piutang)
        if terima_piutang or piutang_awal:
            asumsi.append("Piutang akhir tidak diberikan: dianggap tidak ada penjualan tempo baru yang "
                          "belum dibayar, sehingga piutang akhir = {}.".format(rp(piutang_akhir)))
    penjualan_kredit_raw = piutang_akhir - piutang_awal + terima_piutang
    penjualan_kredit = max(0, penjualan_kredit_raw)
    piutang_tak_tertagih = max(0, -penjualan_kredit_raw)
    if piutang_tak_tertagih:
        peringatan.append("Piutang akhir lebih kecil dari yang seharusnya; selisih {} dicatat sebagai beban "
                          "piutang tak tertagih. Pastikan memang ada piutang yang tidak akan dibayar.".format(
                              rp(piutang_tak_tertagih)))
    pendapatan_usaha = pend_usaha_tunai + penjualan_kredit
    retur = jumlah_jenis("retur")
    pendapatan_bersih = pendapatan_usaha - retur

    # --- HPP (dengan penyesuaian utang usaha & persediaan)
    pembelian_tunai = jumlah_jenis("hpp")
    bayar_utang_usaha = jumlah_jenis("bayar_utang_usaha")
    if a.utang_usaha_akhir is not None:
        utang_usaha_akhir = uang(a.utang_usaha_akhir)
    else:
        utang_usaha_akhir = max(0, utang_usaha_awal - bayar_utang_usaha)
        if bayar_utang_usaha or utang_usaha_awal:
            asumsi.append("Utang ke pemasok di akhir periode tidak diberikan: dianggap tidak ada pembelian "
                          "tempo baru yang belum dibayar, sehingga utang usaha akhir = {}.".format(
                              rp(utang_usaha_akhir)))
    pembelian_kredit_raw = utang_usaha_akhir - utang_usaha_awal + bayar_utang_usaha
    pembelian_kredit = max(0, pembelian_kredit_raw)
    keuntungan_utang = max(0, -pembelian_kredit_raw)
    if keuntungan_utang:
        peringatan.append("Utang usaha turun {} tanpa ada pembayaran tercatat; dicatat sebagai pendapatan "
                          "lain-lain. Pastikan angka utang akhir benar.".format(rp(keuntungan_utang)))
    total_pembelian = pembelian_tunai + pembelian_kredit
    if a.persediaan_akhir is not None:
        persediaan_akhir = uang(a.persediaan_akhir)
    else:
        persediaan_akhir = persediaan_awal
        asumsi.append("Stok akhir tidak diberikan: dianggap sama dengan stok awal ({}), sehingga beban "
                      "pokok penjualan = total pembelian bahan/barang. Isi --persediaan-akhir dari hasil "
                      "hitung stok agar laba lebih akurat.".format(rp(persediaan_awal)))
    hpp = persediaan_awal + total_pembelian - persediaan_akhir
    if hpp < 0:
        peringatan.append("Beban pokok penjualan negatif ({}): stok akhir lebih besar dari stok awal + "
                          "pembelian. Cek angka stok akhir.".format(rp(hpp)))
    laba_kotor = pendapatan_bersih - hpp

    # --- Penyusutan
    bulan_periode = daftar_bulan(p_awal, p_akhir)
    n_bulan = len(bulan_periode)
    beli_aset = [t for t in trx if t["kode"] == "aset_tetap"]
    total_beli_aset = sum(t["nilai"] for t in beli_aset)
    penyusutan = 0
    if a.penyusutan is not None and a.umur_aset_tahun is not None:
        raise GalatInput("Pilih salah satu: --penyusutan (nominal) atau --umur-aset-tahun, jangan keduanya.")
    if a.penyusutan is not None:
        penyusutan = uang(a.penyusutan)
        asumsi.append("Penyusutan aset tetap periode ini {} (angka dari pengguna).".format(rp(penyusutan)))
    elif a.umur_aset_tahun is not None:
        if a.umur_aset_tahun <= 0:
            raise GalatInput("--umur-aset-tahun harus lebih dari 0.")
        penyusutan = sum(penyusutan_bulan(ym) for ym in bulan_periode)
        asumsi.append("Penyusutan garis lurus, umur manfaat {} tahun, tanpa nilai sisa; aset yang dibeli "
                      "mulai disusutkan bulan berikutnya; dihitung per bulan dari harga perolehan (dibulatkan ke "
                      "rupiah per bulan). Nilai aset tetap awal yang Anda berikan diperlakukan sebagai harga "
                      "perolehan per awal data.".format(("%g" % a.umur_aset_tahun).replace(".", ",")))
    elif aset_tetap_awal or total_beli_aset:
        asumsi.append("Penyusutan aset tetap BELUM dihitung (tidak ada --penyusutan / --umur-aset-tahun). "
                      "Laba bisa sedikit lebih tinggi dari seharusnya.")
    penyusutan = min(penyusutan, aset_tetap_awal + total_beli_aset)

    jadwal_penyusutan = []
    if a.umur_aset_tahun is not None and a.umur_aset_tahun > 0:
        bu = Decimal(str(a.umur_aset_tahun)) * 12
        for biaya, mulai in daftar_aset:
            n_aktif = sum(1 for ym in bulan_periode if 0 <= (ym[0] - mulai[0]) * 12 + ym[1] - mulai[1] < bu)
            jadwal_penyusutan.append({"harga_perolehan": biaya, "mulai_disusutkan": "{} {}".format(
                NAMA_BULAN[mulai[1] - 1], mulai[0]), "per_bulan": bulat(Decimal(biaya) / bu),
                "bulan_dalam_periode": n_aktif})

    # --- Beban usaha
    beban_rinci = OrderedDict()
    for kd, info in kategori.items():
        if info["jenis"] == "beban_usaha" and total.get(kd):
            beban_rinci[kd] = total[kd]
    if penyusutan:
        beban_rinci["beban_penyusutan"] = penyusutan
    if piutang_tak_tertagih:
        beban_rinci["beban_piutang_tak_tertagih"] = piutang_tak_tertagih
    if keluar_tak:
        beban_rinci["belum_terklasifikasi_keluar"] = keluar_tak
    label_ekstra = {"beban_penyusutan": "Beban penyusutan aset tetap",
                    "beban_piutang_tak_tertagih": "Beban piutang tak tertagih",
                    "belum_terklasifikasi_keluar": "Pengeluaran BELUM TERKLASIFIKASI (perlu dicek)"}
    kas_buku_akhir = kas_awal + total_masuk - total_keluar
    kas_hitung = kas_buku_akhir + dana_di_rekening_lain
    kas_aktual = uang(a.kas_akhir_aktual, None)
    selisih_kas_dicatat = 0
    if a.catat_selisih_kas:
        if kas_aktual is None:
            raise GalatInput("--catat-selisih-kas butuh --kas-akhir-aktual (saldo kas nyata).")
        selisih_kas_dicatat = kas_aktual - kas_hitung
        if selisih_kas_dicatat < 0:
            beban_rinci["selisih_kas_kurang"] = -selisih_kas_dicatat
        if selisih_kas_dicatat:
            asumsi.append("Selisih kas {} dicatat sebagai {} atas konfirmasi pemilik.".format(
                rp(abs(selisih_kas_dicatat)),
                "beban selisih kas (kas kurang)" if selisih_kas_dicatat < 0 else "pendapatan selisih kas (kas lebih)"))
    label_ekstra["selisih_kas_kurang"] = "Selisih kas (kurang), dikonfirmasi pemilik"
    total_beban_usaha = sum(beban_rinci.values())
    laba_usaha = laba_kotor - total_beban_usaha

    pend_lain_rinci = OrderedDict()
    if total.get("pendapatan_lain"):
        pend_lain_rinci["pendapatan_lain"] = total["pendapatan_lain"]
    if total.get("penjualan_aset"):
        pend_lain_rinci["penjualan_aset"] = total["penjualan_aset"]
        peringatan.append("Ada penjualan aset/barang bekas {}. Seluruh hasilnya dicatat sebagai pendapatan "
                          "lain-lain; nilai buku aset yang dijual belum dikurangkan dari aset tetap. Beri tahu "
                          "nilai bukunya bila ingin lebih akurat.".format(rp(total["penjualan_aset"])))
    if keuntungan_utang:
        pend_lain_rinci["pengurangan_utang"] = keuntungan_utang
    if selisih_kas_dicatat > 0:
        pend_lain_rinci["selisih_kas_lebih"] = selisih_kas_dicatat
    if masuk_tak:
        pend_lain_rinci["belum_terklasifikasi_masuk"] = masuk_tak
    label_ekstra.update({"selisih_kas_lebih": "Selisih kas (lebih), dikonfirmasi pemilik",
                         "pengurangan_utang": "Pengurangan utang usaha tanpa pembayaran",
                         "belum_terklasifikasi_masuk": "Pemasukan BELUM TERKLASIFIKASI (perlu dicek)"})
    total_pend_lain = sum(pend_lain_rinci.values())
    beban_keuangan = jumlah_jenis("beban_keuangan")
    laba_sebelum_pajak = laba_usaha + total_pend_lain - beban_keuangan
    beban_pph = jumlah_jenis("beban_pph")
    laba_bersih = laba_sebelum_pajak - beban_pph

    # --- Neraca
    setoran_modal = jumlah_jenis("modal")
    prive = jumlah_jenis("prive")
    pinjaman_masuk = jumlah_jenis("pinjaman_masuk")
    bayar_pinjaman = jumlah_jenis("bayar_pinjaman")
    kas_neraca = kas_aktual if kas_aktual is not None else kas_hitung
    selisih_kas = (kas_aktual - kas_hitung - selisih_kas_dicatat) if kas_aktual is not None else None
    aset_tetap_akhir = aset_tetap_awal + total_beli_aset - penyusutan
    utang_bank_akhir = utang_bank_awal + pinjaman_masuk - bayar_pinjaman
    aset_awal = kas_awal + piutang_awal + persediaan_awal + aset_tetap_awal + piutang_lain_awal
    liab_awal = utang_usaha_awal + utang_bank_awal + titipan_pajak_awal
    modal_awal_hitung = aset_awal - liab_awal
    if modal_input is not None:
        modal_awal = modal_input
    else:
        modal_awal = modal_awal_hitung
        asumsi.append("Modal awal dihitung dari (aset awal - utang awal) = {}.".format(rp(modal_awal)))
    modal_akhir = modal_awal + setoran_modal - prive + laba_bersih
    piutang_lain_akhir = piutang_lain_awal + sum(t["nilai"] for t in trx if t["kode"] == "piutang_lain" and t["arah"] == "keluar") \
        - sum(t["nilai"] for t in trx if t["kode"] == "piutang_lain" and t["arah"] == "masuk")
    total_aset = kas_neraca + piutang_akhir + piutang_lain_akhir + persediaan_akhir + aset_tetap_akhir
    titipan_pajak_akhir = titipan_pajak_awal + jumlah_jenis_arah("titipan", "masuk") - jumlah_jenis_arah("titipan", "keluar")
    total_liab = utang_usaha_akhir + utang_bank_akhir + titipan_pajak_akhir
    selisih_neraca = total_aset - (total_liab + modal_akhir)
    penyebab = []
    if modal_input is not None and modal_awal != modal_awal_hitung:
        penyebab.append("Modal awal yang diberikan ({}) tidak sama dengan aset awal - utang awal ({}); "
                        "selisih {}.".format(rp(modal_awal), rp(modal_awal_hitung),
                                             rp(modal_awal_hitung - modal_awal)))
    if selisih_kas:
        penyebab.append("Saldo kas nyata ({}) berbeda {} dari hasil hitung buku kas ({}). Kemungkinan ada "
                        "transaksi yang belum dicatat, salah ketik nominal, atau kas awal kurang tepat. Jika "
                        "pemilik yakin selisih ini memang kas hilang/lebih, jalankan ulang dengan "
                        "--catat-selisih-kas.".format(rp(kas_aktual), rp(selisih_kas), rp(kas_hitung)))
    if selisih_neraca and not penyebab:
        penyebab.append("Selisih tidak terduga; periksa angka saldo awal yang dimasukkan.")

    # kas berjalan
    saldo, kas_min, tgl_kas_min = kas_awal, kas_awal, None
    for t in trx:
        saldo += t["nilai"] if t["arah"] == "masuk" else -t["nilai"]
        if t["kode"] == "transfer_internal":
            saldo += t["nilai"] if t["arah"] == "keluar" else -t["nilai"]
        if saldo < kas_min:
            kas_min, tgl_kas_min = saldo, t["tanggal"]
    if data["saldo_kolom_terakhir"] is not None and kas_aktual is None and \
            data["saldo_kolom_terakhir"] != kas_buku_akhir:
        peringatan.append("Kolom Saldo di file berakhir di {}, sedangkan hasil hitung {}. Cek kas awal atau "
                          "baris yang terlewat.".format(rp(data["saldo_kolom_terakhir"]), rp(kas_buku_akhir)))
    # Modal (ekuitas) negatif BUKAN otomatis "wajar": paling sering karena aset lama tidak dicatat.
    modal_negatif = None
    if modal_awal < 0 or modal_akhir < 0:
        cek = []
        if aset_tetap_awal == 0:
            cek.append("ASET YANG BELUM DICATAT: aset tetap awal tercatat Rp 0. Peralatan/kendaraan lama yang masih "
                       "dipakai usaha (kompor, gerobak, etalase, motor, mesin) belum masuk neraca. Isi "
                       "--aset-tetap-awal <nilai wajar sekarang> + --umur-aset-tahun <sisa umur>, atau lampirkan "
                       "daftar aset bila laporan untuk bank")
        cek.append("UTANG: pastikan utang awal ({}) memang utang usaha yang masih tersisa, bukan utang pribadi "
                   "atau angka plafon awal".format(rp(liab_awal)))
        cek.append("SALDO AWAL LAIN: kas, saldo rekening usaha, stok, dan piutang awal sudah lengkap")
        modal_negatif = ("Modal (ekuitas) NEGATIF (modal awal {}, modal akhir {}): utang tercatat lebih besar dari "
                         "aset tercatat. Ini BUKAN otomatis 'wajar untuk usaha baru' — bank membacanya sebagai "
                         "kewajiban melebihi harta. Periksa dulu: {}. Bila setelah dicek tetap negatif, sampaikan "
                         "apa adanya beserta penyebabnya.".format(rp(modal_awal), rp(modal_akhir),
                                                                 "; ".join("({}) {}".format(i, x) for i, x in
                                                                           enumerate(cek, 1))))
        peringatan.append(modal_negatif)
    if prive > 0 and laba_bersih > 0 and prive > laba_bersih:
        peringatan.append("Pengambilan pribadi (prive) {} lebih besar dari laba {}: modal usaha berkurang.".format(
            rp(prive), rp(laba_bersih)))

    # --- Kondisi mustahil & pertanyaan untuk pemilik
    anomali, pertanyaan = [], list(pertanyaan_awal)
    for nama, nilai in (("Utang bank/pinjaman akhir", utang_bank_akhir), ("Utang usaha akhir", utang_usaha_akhir),
                        ("Piutang usaha akhir", piutang_akhir), ("Kasbon/piutang lain akhir", piutang_lain_akhir),
                        ("Persediaan akhir", persediaan_akhir), ("Beban pokok penjualan", hpp),
                        ("Aset tetap akhir", aset_tetap_akhir), ("Titipan pajak daerah akhir", titipan_pajak_akhir)):
        if nilai < 0:
            anomali.append("{} negatif ({}).".format(nama, rp(nilai)))
    if kas_min < 0 and a.abaikan_kas_minus:
        asumsi.append("Saldo kas sempat minus ({} pada {}) dan pemilik mengonfirmasi ini karena urutan pencatatan "
                      "(mis. penjualan dicatat mingguan), bukan transaksi yang terlewat.".format(
                          rp(kas_min), tgl_indo(tgl_kas_min)))
    elif kas_min < 0:
        anomali.append("Saldo kas sempat minus ({} pada {}).".format(rp(kas_min), tgl_indo(tgl_kas_min)))
    saran = {"Utang bank": "Isi --utang-bank-awal, atau cicilan itu sebenarnya untuk barang pribadi (prive)?",
             "Saldo kas": "Berapa kas + saldo rekening di awal periode? Atau ada pemasukan yang belum dicatat?",
             "Beban pokok": "Cek angka stok akhir; stok akhir tidak mungkin melebihi stok awal + pembelian.",
             "Persediaan": "Cek angka stok akhir.", "Piutang usaha": "Cek angka piutang awal/akhir.",
             "Utang usaha": "Cek angka utang pemasok awal/akhir.",
             "Kasbon": "Ada pelunasan kasbon yang kasbonnya tidak tercatat? Isi saldo kasbon awal.",
             "Aset tetap": "Cek nilai aset tetap awal dan penyusutan.",
             "Titipan": "Apakah ada PB1/PBJT bulan lalu yang belum disetor per {}? Isi --titipan-pajak-awal "
                        "<nominal>.".format(tgl_indo(p_awal))}
    for x in anomali:
        tambah = next((v for k, v in saran.items() if x.startswith(k)), "Mohon cek saldo awal atau transaksi.")
        pertanyaan.append("Angka mustahil: " + x + " " + tambah)
    bulan_bunga = set((t["tanggal"].year, t["tanggal"].month) for t in trx if t["kode"] == "beban_keuangan"
                      and "bunga" in normal_teks(t["keterangan"]))
    for t in trx:
        if t["kode"] == "bayar_pinjaman" and not t.get("bunga_dikonfirmasi") and \
                (t["tanggal"].year, t["tanggal"].month) not in bulan_bunga:
            pertanyaan.append("Baris {} \"{}\" {}: berapa bagian BUNGA dari angsuran ini? (Bunga = beban, pokok = "
                              "pengurang utang.) Jawab lalu jalankan ulang dengan --bunga {}=<nominal bunga>; "
                              "jika memang pokok saja, --bunga {}=0.".format(
                                  t["baris"], t["keterangan"], rp(t["nilai"]), t["baris"], t["baris"]))
    pb1_baris = [t for t in trx if t["sumber"] != "ditetapkan pengguna" and t["kode"] != "titipan_pajak"
                 and sebut_pb1(t["keterangan"])]
    if pb1_baris:
        masuk_b = [t["baris"] for t in pb1_baris if t["arah"] == "masuk"]
        keluar_b = [t["baris"] for t in pb1_baris if t["arah"] == "keluar"]
        cmd_a = " ".join("--tetapkan {}=titipan_pajak".format(b) for b in masuk_b + keluar_b)
        cmd_b = " ".join(["--tetapkan {}=pendapatan_usaha".format(b) for b in masuk_b] +
                         ["--tetapkan {}=beban_pajak_lain".format(b) for b in keluar_b])
        pertanyaan.append("Baris {} menyebut PB1/PBJT (pajak restoran/hotel). Apakah PB1 dipungut terpisah dari "
                          "pembeli? (a) Ya, dicatat terpisah lalu disetor: pemungutan & penyetorannya adalah TITIPAN "
                          "(utang pajak daerah, bukan pendapatan/beban): {}. Bila ada PB1 bulan lalu yang belum disetor "
                          "per {}, isi juga --titipan-pajak-awal <nominal>. (b) PB1 sudah termasuk harga jual/penjualan: "
                          "{}.".format(", ".join(str(t["baris"]) for t in pb1_baris), cmd_a, tgl_indo(p_awal), cmd_b))
    # setoran PB1 melebihi pemungutan yang tercatat, tetapi saldo titipan awal tidak diketahui
    if a.titipan_pajak_awal is None and not titipan_pajak_awal and not any(x.startswith("Titipan") for x in anomali):
        setor, jalan_tp = [], 0
        for t in trx:
            if t["kode"] == "titipan_pajak":
                jalan_tp += t["nilai"] if t["arah"] == "masuk" else -t["nilai"]
                if jalan_tp < 0:
                    setor = [t]  # setoran melebihi PB1 yang sudah dipungut di periode ini
                    break
        if setor:
            pertanyaan.append("Baris {} \"{}\" menyetor PB1/PBJT. Apakah ada PB1 bulan lalu yang belum disetor per "
                              "{}? Isi --titipan-pajak-awal <nominal> (0 bila tidak ada).".format(
                                  setor[0]["baris"], setor[0]["keterangan"], tgl_indo(p_awal)))
    if data.get("n_kurung_keluar"):
        peringatan.append("{} nominal minus/dalam kurung di kolom Keluar dibaca sebagai uang keluar.".format(
            data["n_kurung_keluar"]))

    # --- Tren per periode (basis kas, sebelum penyesuaian)
    tren = OrderedDict()
    for t in trx:
        kunci, label = kunci_periode(t["tanggal"], a.rekap)
        r = tren.setdefault(kunci, {"periode": label, "pendapatan": 0, "pengeluaran_usaha": 0, "prive": 0})
        jenis = kategori[t["kode"]]["jenis"] if t["kode"] else ("tak_masuk" if t["arah"] == "masuk" else "tak_keluar")
        if jenis in ("pend_usaha", "pend_lain", "jual_aset", "tak_masuk"):
            r["pendapatan"] += t["nilai"]
        elif jenis == "retur":
            r["pendapatan"] -= t["nilai"]
        elif jenis in ("hpp", "beban_usaha", "beban_keuangan", "beban_pph", "tak_keluar"):
            r["pengeluaran_usaha"] += t["nilai"]
        elif jenis == "prive":
            r["prive"] += t["nilai"]
    for r in tren.values():
        r["selisih"] = r["pendapatan"] - r["pengeluaran_usaha"]

    # --- Pengeluaran terbesar (biaya usaha)
    biaya = OrderedDict()
    if total_pembelian:
        biaya["pembelian_bahan"] = total_pembelian
    for kd, v in beban_rinci.items():
        if kd != "belum_terklasifikasi_keluar":
            biaya[kd] = v
    if beban_keuangan:
        biaya["beban_keuangan"] = beban_keuangan
    if beban_pph:
        biaya["beban_pajak_penghasilan"] = beban_pph

    def label(kd):
        if kd in kategori:
            return kategori[kd]["label"]
        return label_ekstra.get(kd, kd)

    total_biaya = sum(biaya.values())
    biaya_urut = sorted(biaya.items(), key=lambda x: -x[1])
    per_kategori = []
    for kd, info in kategori.items():
        n = sum(1 for t in trx if t["kode"] == kd)
        if n:
            per_kategori.append({"kode": kd, "label": info["label"], "jumlah_transaksi": n, "total": total[kd]})

    # --- Laporan arus kas (metode langsung, basis kas; transfer antar rekening sendiri tidak dihitung)
    kelompok_ak = {"aset_tetap": "investasi", "jual_aset": "investasi", "modal": "pendanaan", "prive": "pendanaan",
                   "pinjaman_masuk": "pendanaan", "bayar_pinjaman": "pendanaan", "transfer": None}
    arus_kas = OrderedDict((k, OrderedDict()) for k in ("operasi", "investasi", "pendanaan"))
    for t in trx:
        jenis = kategori[t["kode"]]["jenis"] if t["kode"] else None
        grup = kelompok_ak.get(jenis, "operasi")
        if grup is None:
            continue
        lbl = (label(t["kode"]) if t["kode"] else "Belum terklasifikasi (perlu dicek)") + \
            (" (masuk)" if t["arah"] == "masuk" else "")
        arus_kas[grup][lbl] = arus_kas[grup].get(lbl, 0) + (t["nilai"] if t["arah"] == "masuk" else -t["nilai"])
    bersih_ak = {g: sum(v.values()) for g, v in arus_kas.items()}
    kenaikan_kas = sum(bersih_ak.values())
    laporan_arus_kas = {
        "kas_awal": kas_awal,
        "rincian": {g: [{"pos": k, "nilai": v} for k, v in sorted(arus_kas[g].items(), key=lambda x: -x[1])]
                    for g in arus_kas},
        "bersih": bersih_ak, "kenaikan_kas": kenaikan_kas, "kas_akhir_buku": kas_awal + kenaikan_kas,
        "selisih_kas_nyata": (kas_neraca - kas_hitung) if kas_neraca != kas_hitung else 0,
        "kas_akhir": kas_neraca,
        "cocok_dengan_buku": kas_awal + kenaikan_kas == kas_hitung,
    }

    hasil = {
        "versi_script": VERSI,
        "modal_negatif": modal_negatif,
        "arus_kas": laporan_arus_kas,
        "nama_usaha": a.nama_usaha,
        "file": data["nama_file"],
        "periode": {"awal": p_awal.isoformat(), "akhir": p_akhir.isoformat(),
                    "teks": "{} s.d. {}".format(tgl_indo(p_awal), tgl_indo(p_akhir)), "jumlah_bulan": n_bulan},
        "status": "SEMENTARA" if (tak_terklasifikasi or data["bermasalah"] or selisih_neraca or pertanyaan)
                  else ("LENGKAP (dengan asumsi)" if any(("tidak diberikan" in x or "BELUM dihitung" in x)
                                                        for x in asumsi) else "LENGKAP"),
        "anomali": anomali,
        "pertanyaan": pertanyaan,
        "jumlah_transaksi": len(trx),
        "total_masuk": total_masuk, "total_keluar": total_keluar,
        "laba_rugi": {
            "penjualan_tunai": pend_usaha_tunai, "penjualan_tempo": penjualan_kredit,
            "pendapatan_usaha": pendapatan_usaha, "retur_penjualan": retur,
            "pendapatan_usaha_bersih": pendapatan_bersih,
            "persediaan_awal": persediaan_awal, "pembelian_tunai": pembelian_tunai,
            "pembelian_tempo": pembelian_kredit, "pembelian": total_pembelian,
            "persediaan_akhir": persediaan_akhir, "beban_pokok_penjualan": hpp, "laba_kotor": laba_kotor,
            "beban_usaha": [{"kode": kd, "label": label(kd), "nilai": v} for kd, v in beban_rinci.items()],
            "total_beban_usaha": total_beban_usaha, "laba_usaha": laba_usaha,
            "pendapatan_lain": [{"kode": kd, "label": label(kd), "nilai": v} for kd, v in pend_lain_rinci.items()],
            "total_pendapatan_lain": total_pend_lain, "beban_keuangan": beban_keuangan,
            "laba_sebelum_pajak": laba_sebelum_pajak, "beban_pajak_penghasilan": beban_pph,
            "laba_bersih": laba_bersih,
        },
        "posisi_keuangan": {
            "tanggal": p_akhir.isoformat(),
            "aset": {"kas_dan_setara_kas": kas_neraca, "kas_menurut_buku": kas_buku_akhir - dana_lain_awal,
                     "dana_di_rekening_lain": dana_lain_awal + dana_di_rekening_lain, "piutang_usaha": piutang_akhir,
                     "piutang_lain": piutang_lain_akhir,
                     "persediaan": persediaan_akhir, "aset_tetap_awal": aset_tetap_awal,
                     "pembelian_aset_tetap": total_beli_aset, "penyusutan_periode_ini": penyusutan,
                     "aset_tetap_nilai_buku": aset_tetap_akhir, "total_aset": total_aset},
            "liabilitas": {"utang_usaha": utang_usaha_akhir, "utang_bank_pinjaman": utang_bank_akhir,
                           "utang_pajak_daerah_titipan": titipan_pajak_akhir,
                           "total_liabilitas": total_liab},
            "ekuitas": {"modal_awal": modal_awal, "setoran_modal": setoran_modal, "prive": prive,
                        "laba_bersih": laba_bersih, "modal_akhir": modal_akhir},
            "total_liabilitas_dan_ekuitas": total_liab + modal_akhir,
            "seimbang": selisih_neraca == 0 and not anomali,
            "seimbang_hitungan": selisih_neraca == 0, "selisih": selisih_neraca, "penyebab_selisih": penyebab,
            "kas_akhir_hitung": kas_hitung, "kas_akhir_aktual": kas_aktual, "selisih_kas": selisih_kas,
        },
        "saldo_awal": {"kas": kas_awal, "piutang": piutang_awal, "piutang_lain": piutang_lain_awal,
                       "titipan_pajak": titipan_pajak_awal, "persediaan": persediaan_awal,
                       "aset_tetap": aset_tetap_awal, "utang_usaha": utang_usaha_awal,
                       "utang_bank": utang_bank_awal, "modal": modal_awal},
        "arus_non_laba": {"setoran_modal": setoran_modal, "prive": prive, "pinjaman_diterima": pinjaman_masuk,
                          "bayar_pokok_pinjaman": bayar_pinjaman, "bayar_utang_pemasok": bayar_utang_usaha,
                          "terima_piutang": terima_piutang, "beli_aset_tetap": total_beli_aset,
                          "transfer_internal_bersih_keluar": dana_di_rekening_lain},
        "per_kategori": per_kategori,
        "jadwal_penyusutan": jadwal_penyusutan,
        "pengeluaran_terbesar": [{"kode": kd, "label": label(kd), "nilai": v,
                                  "persen_dari_total_biaya": round(v * 100.0 / total_biaya, 1) if total_biaya else 0}
                                 for kd, v in biaya_urut[:5]],
        "tren": list(tren.values()),
        "tak_terklasifikasi": [{"baris": t["baris"], "tanggal": t["tanggal"].isoformat(),
                                "keterangan": t["keterangan"], "arah": t["arah"], "nilai": t["nilai"]}
                               for t in tak_terklasifikasi],
        "baris_bermasalah": data["bermasalah"],
        "baris_dilewati": data["dilewati"],
        "peringatan": peringatan,
        "asumsi": asumsi,
        "rincian_transaksi": [{"baris": t["baris"], "tanggal": t["tanggal"].isoformat(),
                               "keterangan": t["keterangan"], "arah": t["arah"], "nilai": t["nilai"],
                               "kategori": t["kode"], "sumber_kategori": t["sumber"]} for t in trx],
    }
    hasil["ringkasan_awam"] = ringkasan_awam(hasil)
    return hasil


def ringkasan_awam(h):
    lr, pk = h["laba_rugi"], h["posisi_keuangan"]
    kal = []
    lb = lr["laba_bersih"]
    per = h["periode"]["teks"]
    if lb > 0:
        kal.append("Usaha kamu UNTUNG {} selama {}.".format(rp(lb), per))
    elif lb < 0:
        kal.append("Usaha kamu RUGI {} selama {}.".format(rp(-lb), per))
    else:
        kal.append("Usaha kamu impas (tidak untung, tidak rugi) selama {}.".format(per))
    if lr["pendapatan_usaha_bersih"] > 0:
        margin = lb * 100.0 / lr["pendapatan_usaha_bersih"]
        if lb >= 0:
            kal.append("Dari penjualan bersih {}, yang tersisa jadi laba sekitar {}% (setiap Rp 100.000 "
                       "penjualan, labanya sekitar {}).".format(rp(lr["pendapatan_usaha_bersih"]),
                                                                 "{:.1f}".format(margin).replace(".", ","),
                                                                 rp(bulat(Decimal(margin) * 1000))))
        else:
            kal.append("Dari penjualan bersih {}, setiap Rp 100.000 penjualan usaha rugi sekitar {}.".format(
                rp(lr["pendapatan_usaha_bersih"]), rp(bulat(Decimal(-margin) * 1000))))
    if h["pengeluaran_terbesar"]:
        b = h["pengeluaran_terbesar"][0]
        kal.append("Pengeluaran terbesar: {} sebesar {} ({}% dari total biaya).".format(
            b["label"].lower(), rp(b["nilai"]), str(b["persen_dari_total_biaya"]).replace(".", ",")))
    tren = h["tren"]
    if len(tren) > 1:
        terbaik = max(tren, key=lambda r: r["selisih"])
        terburuk = min(tren, key=lambda r: r["selisih"])
        kal.append("Arus kas usaha terbaik di {} ({}), terendah di {} ({}).".format(
            terbaik["periode"], rp(terbaik["selisih"]), terburuk["periode"], rp(terburuk["selisih"])))
    pv = pk["ekuitas"]["prive"]
    if pv:
        kal.append("Kamu mengambil {} untuk keperluan pribadi (prive). Ini tidak mengurangi laba, tetapi "
                   "mengurangi modal usaha.".format(rp(pv)))
    kal.append("Uang kas di akhir periode: {}.".format(rp(pk["aset"]["kas_dan_setara_kas"])))
    if h["tak_terklasifikasi"] or h["pertanyaan"]:
        kal.append("Ada {} hal yang perlu kamu jawab dulu (lihat 'Perlu dicek'), jadi angka ini masih "
                   "SEMENTARA.".format(len(h["tak_terklasifikasi"]) + len(h["pertanyaan"])))
    return " ".join(kal)


# ---------------------------------------------------------------------------
# Tampilan teks (Markdown)
# ---------------------------------------------------------------------------
def tabel(baris, header=("Pos", "Jumlah")):
    out = ["| {} | {} |".format(*header), "|---|---:|"]
    for kiri, kanan in baris:
        out.append("| {} | {} |".format(kiri, kanan))
    return "\n".join(out)


def cetak_teks(h):
    lr, pk = h["laba_rugi"], h["posisi_keuangan"]
    nama = h["nama_usaha"]
    per = h["periode"]["teks"]
    tgl_akhir = tgl_indo(datetime.strptime(pk["tanggal"], "%Y-%m-%d").date())
    o = []
    o.append("# Laporan Keuangan {}".format(nama))
    o.append("Periode {} · disusun mengacu pada SAK EMKM · status: **{}**".format(per, h["status"]))
    o.append("")
    o.append("## Ringkasan untuk pemilik")
    o.append(h["ringkasan_awam"])
    o.append("")
    o.append("## 1. Laporan Laba Rugi")
    o.append("{} — untuk periode {}".format(nama, per))
    o.append("")
    b = [("**Pendapatan usaha**", "")]
    if lr["penjualan_tempo"]:
        b.append(("Penjualan tunai/transfer", rp(lr["penjualan_tunai"])))
        b.append(("Penjualan tempo (piutang)", rp(lr["penjualan_tempo"])))
    b.append(("Penjualan / pendapatan usaha", rp(lr["pendapatan_usaha"])))
    if lr["retur_penjualan"]:
        b.append(("Retur & pengembalian dana", rp_kurang(lr["retur_penjualan"])))
    b.append(("**Pendapatan usaha bersih**", "**{}**".format(rp(lr["pendapatan_usaha_bersih"]))))
    b.append(("**Beban pokok penjualan**", ""))
    b.append(("Persediaan awal", rp(lr["persediaan_awal"])))
    b.append(("Pembelian bahan/barang dagangan", rp(lr["pembelian"])))
    b.append(("Persediaan akhir", rp_kurang(lr["persediaan_akhir"])))
    b.append(("Beban pokok penjualan", rp_kurang(lr["beban_pokok_penjualan"])))
    b.append(("**Laba kotor**", "**{}**".format(rp(lr["laba_kotor"]))))
    b.append(("**Beban usaha**", ""))
    for x in lr["beban_usaha"]:
        b.append((x["label"], rp(x["nilai"])))
    b.append(("Total beban usaha", rp_kurang(lr["total_beban_usaha"])))
    b.append(("**Laba (rugi) usaha**", "**{}**".format(rp(lr["laba_usaha"]))))
    for x in lr["pendapatan_lain"]:
        b.append((x["label"], rp(x["nilai"])))
    if lr["beban_keuangan"]:
        b.append(("Beban bunga & biaya bank (beban keuangan)", rp_kurang(lr["beban_keuangan"])))
    b.append(("**Laba (rugi) sebelum pajak**", "**{}**".format(rp(lr["laba_sebelum_pajak"]))))
    b.append(("Beban pajak penghasilan", rp_kurang(lr["beban_pajak_penghasilan"])))
    b.append(("**LABA (RUGI) BERSIH**", "**{}**".format(rp(lr["laba_bersih"]))))
    o.append(tabel(b))
    o.append("")
    o.append("## 2. Laporan Posisi Keuangan (Neraca)")
    o.append("{} — per {}".format(nama, tgl_akhir))
    o.append("")
    s = pk["aset"]
    b = [("**ASET**", "")]
    if s["dana_di_rekening_lain"]:
        b.append(("Kas menurut buku", rp(s["kas_menurut_buku"])))
        b.append(("Dana dipindah ke kas/rekening lain", rp(s["dana_di_rekening_lain"])))
    b.append(("Kas dan setara kas", rp(s["kas_dan_setara_kas"])))
    b.append(("Piutang usaha", rp(s["piutang_usaha"])))
    if s["piutang_lain"]:
        b.append(("Kasbon karyawan & piutang lain-lain", rp(s["piutang_lain"])))
    b.append(("Persediaan", rp(s["persediaan"])))
    lancar = s["kas_dan_setara_kas"] + s["piutang_usaha"] + s["piutang_lain"] + s["persediaan"]
    b.append(("_Jumlah aset lancar_", "_{}_".format(rp(lancar))))
    b.append(("_Aset tidak lancar_", ""))
    if s["aset_tetap_awal"] or s["pembelian_aset_tetap"]:
        b.append(("Aset tetap (awal + pembelian {})".format(rp(s["pembelian_aset_tetap"])),
                  rp(s["aset_tetap_awal"] + s["pembelian_aset_tetap"])))
        b.append(("Penyusutan periode ini", rp_kurang(s["penyusutan_periode_ini"])))
    b.append(("Aset tetap (nilai buku)", rp(s["aset_tetap_nilai_buku"])))
    b.append(("**Total aset**", "**{}**".format(rp(s["total_aset"]))))
    l, e = pk["liabilitas"], pk["ekuitas"]
    b.append(("**LIABILITAS**", ""))
    b.append(("Utang usaha (ke pemasok)", rp(l["utang_usaha"])))
    b.append(("Utang bank / pinjaman", rp(l["utang_bank_pinjaman"])))
    if l["utang_pajak_daerah_titipan"]:
        b.append(("Utang pajak daerah (titipan PB1/PBJT)", rp(l["utang_pajak_daerah_titipan"])))
    b.append(("Total liabilitas", rp(l["total_liabilitas"])))
    b.append(("**EKUITAS**", ""))
    b.append(("Modal awal", rp(e["modal_awal"])))
    if e["setoran_modal"]:
        b.append(("Tambahan modal", rp(e["setoran_modal"])))
    b.append(("Laba (rugi) bersih periode ini", rp(e["laba_bersih"])))
    b.append(("Prive (pengambilan pribadi)", rp_kurang(e["prive"])))
    b.append(("Modal akhir", rp(e["modal_akhir"])))
    b.append(("**Total liabilitas + ekuitas**", "**{}**".format(rp(pk["total_liabilitas_dan_ekuitas"]))))
    o.append(tabel(b))
    o.append("")
    if pk["seimbang_hitungan"] and h["anomali"]:
        o.append("⚠ **Cek keseimbangan:** secara hitungan Aset = Liabilitas + Ekuitas ({}), TETAPI ada angka "
                 "mustahil sehingga laporan belum layak dipakai:".format(rp(s["total_aset"])))
        for x in h["anomali"]:
            o.append("- " + x)
    elif pk["seimbang"]:
        o.append("✔ **Cek keseimbangan:** Aset = Liabilitas + Ekuitas ({}). Neraca seimbang.".format(
            rp(s["total_aset"])))
    else:
        o.append("✘ **Cek keseimbangan: TIDAK SEIMBANG.** Selisih {} (aset {} vs liabilitas + ekuitas {}).".format(
            rp(pk["selisih"]), rp(s["total_aset"]), rp(pk["total_liabilitas_dan_ekuitas"])))
        for p in pk["penyebab_selisih"]:
            o.append("- " + p)
    o.append("")
    ak = h["arus_kas"]
    nama_grup = {"operasi": "Arus kas dari kegiatan usaha (operasi)", "investasi": "Arus kas dari investasi (aset tetap)",
                 "pendanaan": "Arus kas dari pendanaan (modal, prive, pinjaman)"}
    o.append("## Laporan Arus Kas (ringkas, metode langsung — tambahan, tidak diwajibkan SAK EMKM)")
    o.append("{} — untuk periode {}".format(nama, per))
    o.append("")
    b = []
    for g, rinci in ak["rincian"].items():
        b.append(("**{}**".format(nama_grup[g]), ""))
        for x in rinci:
            b.append((x["pos"], rp(x["nilai"]) if x["nilai"] >= 0 else rp_kurang(-x["nilai"])))
        nilai_g = ak["bersih"][g]
        b.append(("_Kas bersih {}_".format(g), "_{}_".format(rp(nilai_g) if nilai_g >= 0 else rp_kurang(-nilai_g))))
    b.append(("**Kenaikan (penurunan) kas**", "**{}**".format(
        rp(ak["kenaikan_kas"]) if ak["kenaikan_kas"] >= 0 else rp_kurang(-ak["kenaikan_kas"]))))
    b.append(("Kas awal periode", rp(ak["kas_awal"])))
    if ak["selisih_kas_nyata"]:
        b.append(("Selisih kas nyata vs buku", rp(ak["selisih_kas_nyata"]) if ak["selisih_kas_nyata"] >= 0
                  else rp_kurang(-ak["selisih_kas_nyata"])))
    b.append(("**Kas akhir periode**", "**{}**".format(rp(ak["kas_akhir"]))))
    o.append(tabel(b))
    o.append("")
    o.append("## 3. Catatan atas Laporan Keuangan (ringkas)")
    o.extend(catatan(h))
    o.append("")
    if len(h["tren"]) > 1:
        o.append("## Tren per periode (arus kas usaha, sebelum penyesuaian stok/piutang/penyusutan)")
        o.append("")
        o.append("| Periode | Uang masuk usaha | Uang keluar usaha | Selisih | Prive |")
        o.append("|---|---:|---:|---:|---:|")
        for r in h["tren"]:
            o.append("| {} | {} | {} | {} | {} |".format(r["periode"], rp(r["pendapatan"]),
                                                        rp(r["pengeluaran_usaha"]), rp(r["selisih"]),
                                                        rp(r["prive"])))
        o.append("")
    if h["tak_terklasifikasi"] or h["baris_bermasalah"] or h["peringatan"] or h["baris_dilewati"] or h["pertanyaan"]:
        o.append("## Perlu dicek")
        if h["pertanyaan"]:
            o.append("**Pertanyaan untuk pemilik** (jawab agar laporan final):")
            for i, q in enumerate(h["pertanyaan"], 1):
                o.append("{}. {}".format(i, q))
            o.append("")
        if h["tak_terklasifikasi"]:
            o.append("**Transaksi belum terklasifikasi** — mohon jelaskan untuk apa:")
            o.append("")
            o.append("| Baris | Tanggal | Keterangan | Masuk/Keluar | Nominal |")
            o.append("|---:|---|---|---|---:|")
            for t in h["tak_terklasifikasi"]:
                o.append("| {} | {} | {} | {} | {} |".format(t["baris"], t["tanggal"], t["keterangan"] or "-",
                                                             t["arah"], rp(t["nilai"])))
            o.append("")
        if h["baris_bermasalah"]:
            o.append("**Baris yang tidak bisa dibaca (tidak dihitung):**")
            for x in h["baris_bermasalah"]:
                o.append("- Baris {}: {} ({})".format(x["baris"], x["alasan"], x["keterangan"] or "-"))
            o.append("")
        if h["baris_dilewati"]:
            o.append("**Baris yang sengaja dilewati:** " + "; ".join(
                "{} ({} baris)".format(k, v) for k, v in h["baris_dilewati"].items()))
            o.append("")
        if h["peringatan"]:
            o.append("**Peringatan:**")
            for p in h["peringatan"]:
                o.append("- " + p)
            o.append("")
    if h["asumsi"]:
        o.append("## Asumsi yang dipakai")
        for p in h["asumsi"]:
            o.append("- " + p)
        o.append("")
    o.append("---")
    o.append("_Laporan ini disusun dari data yang Anda berikan dan mengacu pada SAK EMKM. Ini BUKAN laporan "
             "yang telah diaudit akuntan publik dan bukan nasihat pajak. Untuk pengajuan kredit, tender, atau "
             "pelaporan pajak, mintalah akuntan/konsultan pajak untuk memeriksa. Nominal dibulatkan ke rupiah "
             "terdekat._")
    return "\n".join(o)


def catatan(h):
    lr, pk, sa = h["laba_rugi"], h["posisi_keuangan"], h["saldo_awal"]
    s, l, e = pk["aset"], pk["liabilitas"], pk["ekuitas"]
    n = []
    n.append("**1. Umum.** {} adalah usaha yang laporan keuangannya disusun untuk periode {}. "
             "[Lengkapi: bentuk usaha (perorangan/CV/dll.), alamat, dan kegiatan usaha utama.]".format(
                 h["nama_usaha"], h["periode"]["teks"]))
    n.append("**2. Dasar penyusunan.** Laporan keuangan disusun mengacu pada Standar Akuntansi Keuangan "
             "Entitas Mikro, Kecil, dan Menengah (SAK EMKM), dengan dasar akrual dan konsep biaya historis, "
             "dalam mata uang Rupiah. Laporan disusun dari catatan buku kas pemilik, dengan penyesuaian akhir "
             "periode untuk piutang, persediaan, utang usaha, dan penyusutan sesuai informasi yang tersedia. "
             "Harta dan transaksi pribadi pemilik dipisahkan dari usaha (pengambilan pribadi dicatat sebagai prive).")
    n.append("**3. Kas dan setara kas** per akhir periode {} (saldo awal {}, total uang masuk {}, total uang "
             "keluar {}).".format(rp(s["kas_dan_setara_kas"]), rp(sa["kas"]), rp(h["total_masuk"]),
                                  rp(h["total_keluar"])))
    n.append("**4. Piutang usaha** {} (awal {}). Piutang dicatat sebesar jumlah tagihan kepada pelanggan.".format(
        rp(s["piutang_usaha"]), rp(sa["piutang"])))
    n.append("**5. Persediaan** {} (awal {}). Persediaan dicatat sebesar biaya perolehan; beban pokok penjualan "
             "= persediaan awal + pembelian - persediaan akhir = {}.".format(
                 rp(s["persediaan"]), rp(sa["persediaan"]), rp(lr["beban_pokok_penjualan"])))
    n.append("**6. Aset tetap** nilai buku {} (awal {}, pembelian periode ini {}, penyusutan periode ini {}). "
             "Aset tetap dicatat sebesar biaya perolehan dikurangi akumulasi penyusutan.".format(
                 rp(s["aset_tetap_nilai_buku"]), rp(sa["aset_tetap"]), rp(s["pembelian_aset_tetap"]),
                 rp(s["penyusutan_periode_ini"])))
    if h.get("jadwal_penyusutan"):
        baris = ["| Harga perolehan | Mulai disusutkan | Penyusutan/bulan | Bulan di periode ini |", "|---:|---|---:|---:|"]
        for j in h["jadwal_penyusutan"]:
            baris.append("| {} | {} | {} | {} |".format(rp(j["harga_perolehan"]), j["mulai_disusutkan"],
                                                       rp(j["per_bulan"]), j["bulan_dalam_periode"]))
        n.append("Jadwal penyusutan per aset (garis lurus, total per bulan dibulatkan ke rupiah):\n\n" + "\n".join(baris))
    n.append("**7. Liabilitas.** Utang usaha {} dan utang bank/pinjaman {}{} (pinjaman diterima {}, pembayaran "
             "pokok {}).".format(rp(l["utang_usaha"]), rp(l["utang_bank_pinjaman"]),
                                 (", serta utang pajak daerah titipan PB1/PBJT {}".format(
                                     rp(l["utang_pajak_daerah_titipan"])) if l["utang_pajak_daerah_titipan"] else ""),
                                 rp(h["arus_non_laba"]["pinjaman_diterima"]),
                                 rp(h["arus_non_laba"]["bayar_pokok_pinjaman"])))
    n.append("**8. Ekuitas.** Modal awal {} + tambahan modal {} + laba bersih {} - prive {} = modal akhir {}.".format(
        rp(e["modal_awal"]), rp(e["setoran_modal"]), rp(e["laba_bersih"]), rp(e["prive"]), rp(e["modal_akhir"])))
    if h.get("modal_negatif"):
        n.append("**Catatan modal negatif.** " + h["modal_negatif"])
    n.append("**9. Pendapatan** diakui saat barang/jasa diserahkan; pendapatan usaha bersih periode ini {}.".format(
        rp(lr["pendapatan_usaha_bersih"])))
    n.append("**10. Beban** diakui saat terjadi. Total beban usaha {}, beban keuangan {}, beban pajak "
             "penghasilan {}. [Lengkapi status perpajakan usaha bila perlu, mis. memakai PPh final UMKM.]".format(
                 rp(lr["total_beban_usaha"]), rp(lr["beban_keuangan"]), rp(lr["beban_pajak_penghasilan"])))
    return [x + "\n" for x in n]


def _inline_html(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w])_(.+?)_(?![\w])", r"<em>\1</em>", t)
    return t


def ke_html(md, nama_usaha):
    """Ubah keluaran Markdown script menjadi HTML mandiri siap cetak (Ctrl+P → Simpan sebagai PDF)."""
    out, tabel_buka, list_buka, baris_tabel = [], False, False, 0
    for baris in md.split("\n"):
        b = baris.rstrip()
        if b.startswith("|"):
            sel = [x.strip() for x in b.strip("|").split("|")]
            if all(re.fullmatch(r":?-{3,}:?", x) for x in sel if x):
                continue
            if not tabel_buka:
                out.append("<table>")
                tabel_buka, baris_tabel = True, 0
            tag = "th" if baris_tabel == 0 else "td"
            out.append("<tr>" + "".join('<{0}{1}>{2}</{0}>'.format(
                tag, ' class="n"' if i > 0 else "", _inline_html(x)) for i, x in enumerate(sel)) + "</tr>")
            baris_tabel += 1
            continue
        if tabel_buka:
            out.append("</table>")
            tabel_buka = False
        if b.startswith("- "):
            if not list_buka:
                out.append("<ul>")
                list_buka = True
            out.append("<li>" + _inline_html(b[2:]) + "</li>")
            continue
        if list_buka:
            out.append("</ul>")
            list_buka = False
        if b.startswith("## "):
            out.append("<h2>" + _inline_html(b[3:]) + "</h2>")
        elif b.startswith("# "):
            out.append("<h1>" + _inline_html(b[2:]) + "</h1>")
        elif b == "---":
            out.append("<hr>")
        elif b:
            out.append("<p>" + _inline_html(b) + "</p>")
    if tabel_buka:
        out.append("</table>")
    if list_buka:
        out.append("</ul>")
    ttd = ('<div class="ttd"><p>[isi: kota], [isi: tanggal]</p><p>Pemilik {},</p><br><br><br>'
           '<p>( [isi: nama pemilik] )</p></div>').format(html.escape(nama_usaha))
    gaya = ("body{font-family:Arial,Helvetica,sans-serif;font-size:12px;color:#111;background:#fff;max-width:800px;"
            "margin:24px auto;padding:0 16px}h1{font-size:20px}h2{font-size:15px;margin-top:22px;border-bottom:1px "
            "solid #999}table{border-collapse:collapse;width:100%;margin:8px 0}td,th{border:1px solid #bbb;"
            "padding:4px 6px;text-align:left;vertical-align:top}.n{text-align:right;white-space:nowrap}"
            ".ttd{margin-top:36px;width:260px;margin-left:auto}@media print{h2{page-break-after:avoid}"
            "table{page-break-inside:auto}tr{page-break-inside:avoid}}")
    return ('<!doctype html>\n<html lang="id"><head><meta charset="utf-8"><title>Laporan Keuangan {}</title>'
            '<style>{}</style></head><body>\n{}\n{}\n</body></html>\n').format(
                html.escape(nama_usaha), gaya, "\n".join(out), ttd)


def cetak_daftar_kategori(path_pemetaan):
    kategori, aturan = siapkan_aturan(path_pemetaan)
    kata = defaultdict(list)
    kustom = set()
    if path_pemetaan:
        with open(path_pemetaan, encoding="utf-8-sig") as f:
            for kode, isi in json.load(f).items():
                if str(kode).startswith("_"):
                    continue
                daftar = isi.get("kata", isi.get("kata_kunci", [])) if isinstance(isi, dict) else isi
                kata[kode].extend([daftar] if isinstance(daftar, str) else daftar)
                kustom.add(kode)
    for kode, daftar in ATURAN_BAWAAN:
        kata[kode].extend(daftar)
    print("Kode kategori (aturan dicek berurutan; kata kunci kustom dicek paling dulu):\n")
    for kode, info in kategori.items():
        print("- {} [uang {}] - {}{}".format(kode, info["arah"], info["label"],
                                              " (ada kata kunci kustom)" if kode in kustom else ""))
        if kata.get(kode):
            print("    kata kunci: " + ", ".join(kata[kode]))


class ParserID(argparse.ArgumentParser):
    def error(self, message):
        pesan = message.replace("the following arguments are required", "argumen wajib belum diisi") \
                       .replace("unrecognized arguments", "argumen tidak dikenal") \
                       .replace("invalid choice", "pilihan tidak valid") \
                       .replace("expected one argument", "butuh satu nilai").replace("choose from", "pilih dari")
        sys.stderr.write("GALAT: {}\nKetik --help untuk melihat cara pakai.\n".format(pesan))
        sys.exit(2)


def main(argv=None):
    p = ParserID(description="Laporan keuangan SAK EMKM dari buku kas (CSV / tabel teks).")
    p.add_argument("file", nargs="?", help="File CSV/teks tabel buku kas. Pakai '-' untuk membaca dari stdin.")
    p.add_argument("--nama-usaha", default="[Nama Usaha]")
    p.add_argument("--periode-awal", help="YYYY-MM-DD (default: tanggal 1 bulan transaksi pertama)")
    p.add_argument("--periode-akhir", help="YYYY-MM-DD (default: akhir bulan transaksi terakhir)")
    p.add_argument("--rekap", choices=["bulan", "kuartal", "tahun"], default="bulan")
    for nama in ("kas-awal", "piutang-awal", "piutang-akhir", "persediaan-awal", "persediaan-akhir",
                 "aset-tetap-awal", "utang-usaha-awal", "utang-usaha-akhir", "utang-bank-awal",
                 "modal-awal", "kas-akhir-aktual", "penyusutan"):
        p.add_argument("--" + nama, help="nominal, mis. 'Rp 1.500.000'")
    p.add_argument("--umur-aset-tahun", type=float, help="umur manfaat aset tetap (tahun) untuk penyusutan")
    p.add_argument("--pemetaan", help="file JSON kata kunci tambahan: {\"prive\": [\"jajan\"], ...}")
    p.add_argument("--tetapkan", action="append", metavar="BARIS=KODE",
                   help="tetapkan kategori baris tertentu, mis. --tetapkan 12=prive (boleh berulang)")
    for peran in ("tanggal", "keterangan", "masuk", "keluar", "kategori", "jumlah", "jenis", "saldo"):
        p.add_argument("--kolom-" + peran, help="nama kolom {} bila tidak terdeteksi otomatis".format(peran))
    p.add_argument("--debit-artinya", choices=["masuk", "keluar"])
    p.add_argument("--bunga", action="append", metavar="BARIS=NOMINAL",
                   help="pisahkan bunga dari angsuran, mis. --bunga 25=208.334 (0 = pokok saja); boleh berulang")
    p.add_argument("--catat-selisih-kas", action="store_true",
                   help="catat selisih kas nyata vs buku sebagai beban/pendapatan lain (setelah dikonfirmasi pemilik)")
    p.add_argument("--piutang-awal-periode", help="piutang pelanggan per --periode-awal (menimpa hasil gulir)")
    p.add_argument("--utang-usaha-awal-periode", help="utang pemasok per --periode-awal (menimpa hasil gulir)")
    p.add_argument("--piutang-lain-awal", help="saldo kasbon karyawan/piutang lain awal")
    p.add_argument("--titipan-pajak-awal", help="PB1/PBJT yang sudah dipungut tetapi belum disetor, per awal data "
                   "(atau per awal periode dengan --saldo-awal-per awal-periode)")
    p.add_argument("--abaikan-kas-minus", action="store_true",
                   help="pemilik mengonfirmasi kas minus sementara hanya karena urutan pencatatan")
    p.add_argument("--saldo-awal-per", choices=["awal-file", "awal-periode"],
                   help="saldo awal yang diberikan berlaku per awal data file (default, digulirkan) atau per --periode-awal")
    p.add_argument("--format", choices=["teks", "json"], default="teks")
    p.add_argument("--html", metavar="FILE", help="simpan juga laporan siap cetak (HTML; buka di browser → Cetak → PDF)")
    p.add_argument("--csv-arus-kas", metavar="FILE", help="simpan laporan arus kas ke CSV (bisa dibuka di Excel)")
    p.add_argument("--daftar-kategori", action="store_true", help="tampilkan kode kategori & kata kunci")
    a = p.parse_args(argv)
    try:
        if a.daftar_kategori:
            cetak_daftar_kategori(a.pemetaan)
            return 0
        if not a.file:
            raise GalatInput("Sebutkan file buku kas. Contoh: python3 laporan_emkm.py buku-kas.csv")
        h = hitung(a)
    except GalatInput as e:
        if a.format == "json":
            sys.stderr.write(json.dumps({"error": str(e)}, ensure_ascii=False) + "\n")
        else:
            sys.stderr.write("GALAT: {}\n".format(e))
        return 1
    try:
        if a.html:
            with open(a.html, "w", encoding="utf-8") as f:
                f.write(ke_html(cetak_teks(h), h["nama_usaha"]))
        if a.csv_arus_kas:
            with open(a.csv_arus_kas, "w", newline="", encoding="utf-8-sig") as f:
                w = csv.writer(f)
                w.writerow(["kelompok", "pos", "nilai_rupiah"])
                for g, rinci in h["arus_kas"]["rincian"].items():
                    for x in rinci:
                        w.writerow([g, x["pos"], x["nilai"]])
                    w.writerow([g, "Kas bersih " + g, h["arus_kas"]["bersih"][g]])
                w.writerow(["", "Kenaikan (penurunan) kas", h["arus_kas"]["kenaikan_kas"]])
                w.writerow(["", "Kas awal periode", h["arus_kas"]["kas_awal"]])
                if h["arus_kas"]["selisih_kas_nyata"]:
                    w.writerow(["", "Selisih kas nyata vs buku", h["arus_kas"]["selisih_kas_nyata"]])
                w.writerow(["", "Kas akhir periode", h["arus_kas"]["kas_akhir"]])
    except OSError as e:
        sys.stderr.write("GALAT: gagal menyimpan file ekspor: {}\n".format(e))
        return 1
    if a.format == "json":
        print(json.dumps(h, ensure_ascii=False, indent=2))
    else:
        print(cetak_teks(h))
        for f_, ket in ((a.html, "Laporan siap cetak (HTML)"), (a.csv_arus_kas, "Arus kas (CSV)")):
            if f_:
                print("\n{} disimpan: {}".format(ket, f_))
    return 0


if __name__ == "__main__":
    for _aliran in (sys.stdout, sys.stderr):
        try:
            _aliran.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            pass
    sys.exit(main())
