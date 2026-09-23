#!/usr/bin/env python3
"""Cek konsistensi angka & format nota / kuitansi / invoice / faktur pajak, lalu ekspor CSV/JSON/rekap.

Input: file JSON hasil ekstraksi (lihat templates/contoh-input.json). Satu dokumen atau banyak
(kunci "dokumen": [...]). Nilai yang tidak terbaca ditulis "TIDAK_TERBACA"; nilai yang memang tidak
ada di dokumen ditulis null.

Yang dicek (angka dihitung dengan Decimal, bukan dikira):
- qty x harga satuan - diskon item = jumlah per baris
- jumlah semua item = subtotal
- DPP, DPP nilai lain 11/12, PPN 12% (efektif 11%) untuk barang/jasa biasa; 12% penuh untuk mewah
- total = dasar + PPN + PPnBM + biaya lain - potongan (juga dikenali bila PPh dipotong / meterai ditagihkan)
- terbilang di dokumen dibaca jadi angka lalu dibandingkan dengan total
- format NPWP (15/16 digit), NITKU (22 digit), nomor seri faktur Coretax (17 digit):
  hanya PERINGATAN, tidak pernah menolak dokumen (format belum terverifikasi dari dokumen primer)
- dokumen dobel dalam satu batch, meterai untuk kuitansi > Rp5.000.000

Dasar aturan & status: references/regulasi.md (berlaku per 2026-09-23).
Hanya library standar Python 3.8+. Tidak ada akses jaringan. Tidak membaca file selain yang diberikan.

Contoh:
  python3 cek_nota.py data.json                      # laporan teks + rekap
  python3 cek_nota.py data.json --format json        # hasil lengkap JSON
  python3 cek_nota.py data.json --format csv --pemisah ";" --output rekap.csv
  python3 cek_nota.py data.json --format csv --csv item --pemisah tab
  python3 cek_nota.py --terbilang "Rp 1.250.000"
"""
import argparse
import csv
import datetime as dt
import io
import json
import re
import sys
from collections import OrderedDict
from decimal import Decimal, InvalidOperation, ROUND_FLOOR, ROUND_HALF_UP

TANGGAL_ATURAN = "2026-09-23"
TIDAK_TERBACA = "TIDAK_TERBACA"
_PENANDA_TT = {"tidak_terbaca", "tidak terbaca", "?", "??", "???", "buram", "tidak jelas"}
JENIS_DOK = {"nota", "struk", "kuitansi", "invoice", "faktur_pajak", "bukti_transfer", "lainnya"}
JENIS_PPN = {"umum", "mewah", "tidak_ada", "dibebaskan", "lainnya", ""}
BATAS_METERAI = Decimal(5000000)
TGL_PPN_12 = dt.date(2025, 1, 1)
TGL_PPN_11 = dt.date(2022, 4, 1)
TGL_MEWAH_PENUH = dt.date(2025, 2, 1)
BELUM_VERIF = "BELUM TERVERIFIKASI"


class GalatInput(Exception):
    pass


# ================================================================ angka
_PENGALI = [("miliar", 10 ** 9), ("milyar", 10 ** 9), ("juta", 10 ** 6), ("ribu", 10 ** 3),
            ("jt", 10 ** 6), ("rb", 10 ** 3), ("k", 10 ** 3)]


def _cek_ribuan(bagian, asli, nama):
    if not (1 <= len(bagian[0]) <= 3) or any(len(b) != 3 for b in bagian[1:]):
        raise GalatInput("{}: '{}' tidak dikenali. Pakai titik untuk ribuan dan koma untuk desimal, "
                         "mis. 1.250.000 atau 1.250.000,50".format(nama, asli))


def parse_angka(nilai, nama="angka"):
    """Format Indonesia: 'Rp 15.000', '15.000,50', '15.000,-', '1,5jt', 15000. Titik = ribuan, koma = desimal."""
    if isinstance(nilai, bool):
        raise GalatInput("{}: nilai '{}' bukan angka".format(nama, nilai))
    if isinstance(nilai, int):
        return Decimal(nilai)
    if isinstance(nilai, float):
        return Decimal(str(nilai))
    if isinstance(nilai, Decimal):
        return nilai
    asli = str(nilai)
    s = asli.strip().lower().replace(" ", "").replace(" ", "")
    s = re.sub(r"^(rp|idr)\.?", "", s)
    s = re.sub(r"[,.]-+$", "", s)
    s = s.rstrip("-") if s.endswith("-") and len(s) > 1 else s
    pengali = 1
    for akhiran, kali in _PENGALI:
        if s.endswith(akhiran):
            s, pengali = s[: -len(akhiran)], kali
            break
    negatif = s.startswith("-") or (s.startswith("(") and s.endswith(")"))
    s = s.strip("-()")
    if not s or not re.fullmatch(r"[\d.,]+", s) or not re.search(r"\d", s):
        raise GalatInput("{}: '{}' bukan angka yang valid".format(nama, asli))
    if "," in s and "." in s:
        if s.rfind(",") < s.rfind("."):
            raise GalatInput("{}: '{}' memakai format Inggris. Tulis 1.250.000,50 (titik ribuan, koma desimal)"
                             .format(nama, asli))
        utuh, _, desimal = s.rpartition(",")
        _cek_ribuan(utuh.split("."), asli, nama)
        s = utuh.replace(".", "") + "." + desimal
    elif "," in s:
        bagian = s.split(",")
        if len(bagian) == 2 and len(bagian[1]) != 3:
            s = (bagian[0] or "0") + "." + bagian[1]
        elif len(bagian) == 2 and len(bagian[1]) == 3 and bagian[0] in ("", "0"):
            s = "0." + bagian[1]
        else:
            _cek_ribuan(bagian, asli, nama)
            s = s.replace(",", "")
    elif "." in s:
        bagian = s.split(".")
        if len(bagian) == 2 and (len(bagian[1]) != 3 or bagian[0] in ("", "0")):
            s = (bagian[0] or "0") + "." + bagian[1]
        else:
            _cek_ribuan(bagian, asli, nama)
            s = s.replace(".", "")
    try:
        d = Decimal(s) * pengali
    except InvalidOperation:
        raise GalatInput("{}: '{}' bukan angka yang valid".format(nama, asli))
    return -d if negatif else d


def tidak_terbaca(v):
    return isinstance(v, str) and v.strip().lower() in _PENANDA_TT


def kosong(v):
    return v is None or (isinstance(v, str) and v.strip() in ("", "-", "--"))


class Nilai:
    """Pembungkus nilai angka: ada (Decimal), tidak ada (None), atau tidak terbaca."""
    __slots__ = ("angka", "tt")

    def __init__(self, angka=None, tt=False):
        self.angka, self.tt = angka, tt

    @property
    def ada(self):
        return self.angka is not None


def baca_nilai(obj, kunci, label, catat_tt):
    v = obj.get(kunci) if isinstance(obj, dict) else None
    if kosong(v):
        return Nilai()
    if tidak_terbaca(v):
        catat_tt.append(label)
        return Nilai(tt=True)
    return Nilai(parse_angka(v, label))


def format_rp(d):
    if d is None:
        return "-"
    d = Decimal(d)
    if d != d.to_integral_value():
        q = d.quantize(Decimal("0.01"), ROUND_HALF_UP)
        utuh, pecahan = "{:.2f}".format(abs(q)).split(".")
        teks = "{:,}".format(int(utuh)).replace(",", ".") + "," + pecahan
    else:
        teks = "{:,}".format(int(abs(d))).replace(",", ".")
    return ("-" if d < 0 else "") + "Rp " + teks


def ke_json(d):
    if isinstance(d, Decimal):
        return int(d) if d == d.to_integral_value() else float(d.quantize(Decimal("0.01"), ROUND_HALF_UP))
    if isinstance(d, (dt.date,)):
        return d.isoformat()
    raise TypeError(str(type(d)))


def floor(d):
    return Decimal(d).quantize(Decimal(1), ROUND_FLOOR)


def dekat(a, b, tol=1):
    return abs(Decimal(a) - Decimal(b)) <= Decimal(tol)


# ================================================================ terbilang
_SATUAN = ["", "satu", "dua", "tiga", "empat", "lima", "enam", "tujuh", "delapan", "sembilan",
           "sepuluh", "sebelas"]


def _tb(n):
    if n < 12:
        return _SATUAN[n]
    if n < 20:
        return _tb(n - 10) + " belas"
    if n < 100:
        return _tb(n // 10) + " puluh " + _tb(n % 10)
    if n < 200:
        return "seratus " + _tb(n - 100)
    if n < 1000:
        return _tb(n // 100) + " ratus " + _tb(n % 100)
    if n < 2000:
        return "seribu " + _tb(n - 1000)
    for skala, kata in ((10 ** 12, "triliun"), (10 ** 9, "miliar"), (10 ** 6, "juta"), (10 ** 3, "ribu")):
        if n >= skala:
            return _tb(n // skala) + " " + kata + " " + _tb(n % skala)
    return ""


def terbilang(nilai):
    d = Decimal(nilai).quantize(Decimal("0.01"), ROUND_HALF_UP)
    if d < 0:
        raise GalatInput("terbilang: angka tidak boleh negatif")
    if d >= Decimal(10) ** 15:
        raise GalatInput("terbilang: angka terlalu besar")
    rupiah = int(d)
    sen = int((d - rupiah) * 100)
    teks = (re.sub(r"\s+", " ", _tb(rupiah)).strip() or "nol") + " rupiah"
    if sen:
        teks += " " + re.sub(r"\s+", " ", _tb(sen)).strip() + " sen"
    return teks[0].upper() + teks[1:]


_KATA_ANGKA = {"nol": 0, "kosong": 0, "satu": 1, "dua": 2, "tiga": 3, "empat": 4, "lima": 5, "enam": 6,
               "tujuh": 7, "delapan": 8, "sembilan": 9, "sepuluh": 10, "sebelas": 11}
_SKALA = {"ribu": 10 ** 3, "juta": 10 ** 6, "miliar": 10 ** 9, "milyar": 10 ** 9, "triliun": 10 ** 12}


def _kata_ke_int(kata):
    total, grup, n = 0, 0, 0
    for k in kata:
        if k in ("se",):
            n = 1
        elif k in _KATA_ANGKA:
            n = _KATA_ANGKA[k]
        elif k == "belas":
            grup += n + 10
            n = 0
        elif k == "puluh":
            grup += n * 10
            n = 0
        elif k == "ratus":
            grup += n * 100
            n = 0
        elif k in _SKALA:
            total += (grup + n) * _SKALA[k]
            grup = n = 0
        else:
            return None
    return total + grup + n


def baca_terbilang(teks):
    """Ubah terbilang dokumen ('Satu juta dua ratus ribu rupiah') jadi Decimal. None bila tak bisa dibaca."""
    t = re.sub(r"[#*=.,:;/()\-]", " ", teks.lower())
    t = re.sub(r"\bse(ratus|ribu|puluh|belas|juta)\b", r"se \1", t)
    buang = {"dan", "rp", "idr", "saja", "sejumlah", "uang", "terbilang", "sen"}
    bagian = re.split(r"\brupiah\b", t)
    rp = [k for k in bagian[0].split() if k not in buang]
    sen = [k for k in " ".join(bagian[1:]).split() if k not in buang]
    if not rp:
        return None
    r = _kata_ke_int(rp)
    s = _kata_ke_int(sen) if sen else 0
    if r is None or s is None:
        return None
    return Decimal(r) + Decimal(s) / 100


# ================================================================ tanggal
_BULAN = {"januari": 1, "jan": 1, "februari": 2, "feb": 2, "pebruari": 2, "maret": 3, "mar": 3, "april": 4,
          "apr": 4, "mei": 5, "juni": 6, "jun": 6, "juli": 7, "jul": 7, "agustus": 8, "agu": 8, "agt": 8,
          "ags": 8, "aug": 8, "september": 9, "sep": 9, "sept": 9, "oktober": 10, "okt": 10, "oct": 10,
          "november": 11, "nov": 11, "nop": 11, "desember": 12, "des": 12, "dec": 12, "may": 5}


def parse_tanggal(v):
    """'2026-09-01', '01/09/2026', '1-9-26', '1 September 2026', '01 Sep 2026' -> date."""
    s = str(v).strip().lower()
    m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", s)
    if m:
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
    else:
        m = re.fullmatch(r"(\d{1,2})[/.\-](\d{1,2})[/.\-](\d{2}|\d{4})", s)
        if m:
            d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        else:
            m = re.fullmatch(r"(\d{1,2})[\s\-]+([a-z]+)\.?[\s\-]+(\d{2}|\d{4})", s)
            if not m or m.group(2) not in _BULAN:
                raise GalatInput("tanggal '{}' tidak dikenali. Pakai 2026-09-01 atau 01/09/2026".format(v))
            d, mo, y = int(m.group(1)), _BULAN[m.group(2)], int(m.group(3))
    if y < 100:
        y += 2000
    try:
        return dt.date(y, mo, d)
    except ValueError:
        raise GalatInput("tanggal '{}' tidak valid (hari/bulan di luar rentang)".format(v))


# ================================================================ identitas pajak
def hanya_digit(v):
    return re.sub(r"\D", "", str(v))


def cek_npwp(v, label, hasil):
    if kosong(v):
        return None
    if tidak_terbaca(v):
        return None
    dig = hanya_digit(v)
    if len(dig) == 16:
        hasil.append(("ok", "{}: 16 digit (format NPWP/NIK baru)".format(label)))
    elif len(dig) == 15:
        hasil.append(("peringatan", "{}: 15 digit = format NPWP lama. Sejak Coretax, NPWP badan umumnya "
                      "16 digit (NPWP lama diawali angka 0) dan orang pribadi memakai NIK. Minta penjual "
                      "memperbarui identitas bila dokumen bertanggal 2025 ke atas ({})."
                      .format(label, BELUM_VERIF)))
    else:
        hasil.append(("peringatan", "{}: {} digit, panjang tidak biasa (umumnya 16; format lama 15). Cek ulang "
                      "angka di dokumen; mungkin ada digit yang salah baca ({}).".format(label, len(dig), BELUM_VERIF)))
    return dig


def cek_nitku(v, npwp_digit, label, hasil):
    if kosong(v) or tidak_terbaca(v):
        return None
    dig = hanya_digit(v)
    if len(dig) != 22:
        hasil.append(("peringatan", "{}: {} digit. NITKU era Coretax umumnya 22 digit (16 digit NPWP + 6 digit "
                      "kode tempat usaha). Jangan ditolak hanya karena ini; cek ulang ({})."
                      .format(label, len(dig), BELUM_VERIF)))
    elif npwp_digit and len(npwp_digit) == 16 and dig[:16] != npwp_digit:
        hasil.append(("peringatan", "{}: 16 digit awal NITKU berbeda dengan NPWP di dokumen yang sama. "
                      "Cek ulang salah satunya ({}).".format(label, BELUM_VERIF)))
    else:
        hasil.append(("ok", "{}: 22 digit".format(label)))
    return dig


_KODE_TRX = {"01": "penyerahan biasa (PPN dipungut penjual)", "02": "ke pemungut PPN instansi pemerintah",
             "03": "ke pemungut PPN selain instansi pemerintah", "04": "DPP nilai lain",
             "05": "besaran tertentu", "06": "ke turis / lainnya sesuai aturan", "07": "PPN tidak dipungut / DTP",
             "08": "PPN dibebaskan", "09": "penyerahan aktiva (Pasal 16D)", "10": "penyerahan lainnya"}


def cek_nsfp(v, tanggal, hasil):
    if kosong(v):
        hasil.append(("peringatan", "Nomor seri faktur pajak tidak tercantum/tidak diisi. Faktur pajak sah "
                      "selalu punya nomor seri; minta salinan dari penjual bila memang tidak ada."))
        return None
    if tidak_terbaca(v):
        return None
    dig = hanya_digit(v)
    if len(dig) == 17:
        kode, status, tahun = dig[:2], dig[2:4], dig[4:6]
        arti = _KODE_TRX.get(kode)
        pesan = "Nomor seri faktur 17 digit (format Coretax): kode transaksi {}{}, kode status {} ({})".format(
            kode, " = " + arti if arti else " (tidak dikenal)", status,
            "normal" if status == "00" else "faktur pengganti ke-{}".format(int(status)))
        hasil.append(("ok" if arti else "peringatan", pesan + " — arti kode: " + BELUM_VERIF))
        if tanggal and "20" + tahun != str(tanggal.year):
            hasil.append(("peringatan", "Digit tahun di nomor seri ({}) berbeda dengan tahun tanggal faktur ({}). "
                          "Cek ulang ({}).".format("20" + tahun, tanggal.year, BELUM_VERIF)))
        if kode in ("07", "08"):
            hasil.append(("info", "Kode {} berarti PPN tidak dipungut/dibebaskan; PPN di faktur biasanya "
                          "tidak bisa dibayar ke penjual.".format(kode)))
    elif len(dig) == 16:
        if tanggal and tanggal >= TGL_PPN_12:
            hasil.append(("peringatan", "Nomor seri faktur 16 digit = format e-Faktur lama. Faktur bertanggal 2025 "
                          "ke atas di Coretax umumnya 17 digit. Tanyakan ke penjual ({}).".format(BELUM_VERIF)))
        else:
            hasil.append(("ok", "Nomor seri faktur 16 digit (format e-Faktur sebelum Coretax)"))
    else:
        hasil.append(("peringatan", "Nomor seri faktur {} digit, panjang tidak biasa (Coretax umumnya 17, format "
                      "lama 16). Cek ulang angka, jangan langsung dianggap palsu ({}).".format(len(dig), BELUM_VERIF)))
    return dig


# ================================================================ inti pengecekan
def ppn_seharusnya(dpp, jenis, tanggal):
    """Kembalikan (ppn, penjelasan, dpp_nilai_lain|None) sesuai tanggal & jenis."""
    if tanggal and tanggal < TGL_PPN_11:
        return floor(dpp * Decimal("0.10")), "10% x DPP (aturan sebelum 1 April 2022)", None
    if tanggal and tanggal < TGL_PPN_12:
        return floor(dpp * Decimal("0.11")), "11% x DPP (aturan 1 April 2022 - 31 Desember 2024)", None
    if jenis == "mewah":
        if tanggal and tanggal < TGL_MEWAH_PENUH:
            dnl = dpp * 11 / 12
            return floor(dpp * Decimal("0.11")), "masa transisi Januari 2025: 12% x 11/12 x DPP", dnl
        return floor(dpp * Decimal("0.12")), "12% x DPP penuh (barang mewah)", None
    dnl = dpp * 11 / 12
    return floor(dpp * Decimal("0.11")), "12% x DPP nilai lain (11/12 x DPP) = efektif 11%", dnl


def str_bersih(v):
    if kosong(v):
        return None
    return TIDAK_TERBACA if tidak_terbaca(v) else str(v).strip()


def cek_dokumen(dok, urut, hari_ini):
    if not isinstance(dok, dict):
        raise GalatInput("dokumen ke-{} harus berupa objek JSON {{...}}".format(urut))
    tt, hasil = [], []  # tt = daftar kolom tidak terbaca; hasil = (level, pesan)
    ident = str(dok.get("id") or "D{}".format(urut))
    jenis = str(dok.get("jenis") or "lainnya").strip().lower().replace(" ", "_")
    if jenis == "kwitansi":
        jenis = "kuitansi"
    if jenis not in JENIS_DOK:
        hasil.append(("info", "Jenis '{}' tidak dikenal; diperlakukan sebagai 'lainnya'".format(jenis)))
        jenis = "lainnya"

    # --- tanggal
    tanggal = None
    tv = dok.get("tanggal")
    if tidak_terbaca(tv):
        tt.append("tanggal")
    elif not kosong(tv):
        tanggal = parse_tanggal(tv)
        if tanggal > hari_ini:
            hasil.append(("peringatan", "Tanggal {} ada di masa depan; cek ulang (mungkin salah baca)".format(tanggal)))
    else:
        hasil.append(("info", "Tanggal tidak tercantum; aturan PPN diasumsikan yang berlaku sekarang"))

    penjual = dok.get("penjual") or {}
    pembeli = dok.get("pembeli") or {}
    if not isinstance(penjual, dict) or not isinstance(pembeli, dict):
        raise GalatInput("dokumen {}: 'penjual' dan 'pembeli' harus objek, mis. {{\"nama\": \"...\"}}".format(ident))
    for peran, obj in (("penjual", penjual), ("pembeli", pembeli)):
        for k in ("nama", "npwp", "nitku", "alamat"):
            if tidak_terbaca(obj.get(k)):
                tt.append("{}.{}".format(peran, k))
    for k in ("nomor", "nsfp", "terbilang", "metode_bayar"):
        if tidak_terbaca(dok.get(k)):
            tt.append(k)

    # --- item
    items_out, jumlah_items, item_lengkap = [], Decimal(0), True
    items = dok.get("item") or []
    if not isinstance(items, list):
        raise GalatInput("dokumen {}: 'item' harus daftar [...]".format(ident))
    for i, it in enumerate(items, 1):
        if not isinstance(it, dict):
            raise GalatInput("dokumen {}: item ke-{} harus objek".format(ident, i))
        lab = "item {}".format(i)
        if tidak_terbaca(it.get("nama")):
            tt.append(lab + ".nama")
        qty = baca_nilai(it, "qty", lab + ".qty", tt)
        harga = baca_nilai(it, "harga_satuan", lab + ".harga_satuan", tt)
        disk = baca_nilai(it, "diskon", lab + ".diskon", tt)
        jml = baca_nilai(it, "jumlah", lab + ".jumlah", tt)
        hitung = None
        if qty.ada and harga.ada and not disk.tt:
            hitung = qty.angka * harga.angka - (disk.angka or 0)
            if jml.ada and not dekat(hitung, jml.angka):
                hasil.append(("selisih", "Item {} '{}': {} x {}{} = {}, tapi tertulis {} (selisih {})".format(
                    i, it.get("nama"), qty.angka.normalize(), format_rp(harga.angka),
                    " - diskon " + format_rp(disk.angka) if disk.ada else "", format_rp(hitung),
                    format_rp(jml.angka), format_rp(jml.angka - hitung))))
        nilai_baris = jml.angka if jml.ada else (hitung if not jml.tt else None)
        if nilai_baris is None:
            item_lengkap = False
        else:
            jumlah_items += nilai_baris
        items_out.append(OrderedDict([
            ("nama", str_bersih(it.get("nama"))), ("qty", TIDAK_TERBACA if qty.tt else qty.angka),
            ("satuan", str_bersih(it.get("satuan"))),
            ("harga_satuan", TIDAK_TERBACA if harga.tt else harga.angka),
            ("diskon", TIDAK_TERBACA if disk.tt else disk.angka),
            ("jumlah", TIDAK_TERBACA if jml.tt else (jml.angka if jml.ada else hitung)),
            ("jumlah_dihitung_script", not jml.ada and hitung is not None)]))

    # --- angka ringkasan
    f = {}
    for k in ("subtotal", "diskon", "dpp", "dpp_nilai_lain", "ppn", "ppnbm", "pph", "biaya_lain",
              "potongan_lain", "meterai", "total"):
        f[k] = baca_nilai(dok, k, k, tt)
    termasuk = bool(dok.get("harga_termasuk_ppn"))
    jenis_ppn = str(dok.get("jenis_ppn") or "").strip().lower()
    if jenis_ppn not in JENIS_PPN:
        hasil.append(("info", "jenis_ppn '{}' tidak dikenal; dianggap belum diketahui".format(jenis_ppn)))
        jenis_ppn = ""

    # subtotal vs item
    subtotal = f["subtotal"].angka
    if items and item_lengkap:
        tol = max(1, len(items))
        if f["subtotal"].ada:
            if dekat(jumlah_items, subtotal, tol):
                hasil.append(("ok", "Jumlah {} item = subtotal {}".format(len(items), format_rp(subtotal))))
            else:
                hasil.append(("selisih", "Jumlah semua item {} tidak sama dengan subtotal tertulis {} (selisih {})"
                              .format(format_rp(jumlah_items), format_rp(subtotal), format_rp(subtotal - jumlah_items))))
        elif not f["subtotal"].tt:
            subtotal = jumlah_items
    elif items and not item_lengkap:
        hasil.append(("info", "Ada angka item yang tidak terbaca; cek jumlah item vs subtotal dilewati"))

    dasar = None
    if subtotal is not None and not f["diskon"].tt:
        dasar = subtotal - (f["diskon"].angka or 0)

    # --- PPN
    dpp = f["dpp"].angka
    ppn = f["ppn"].angka
    ppn_label = None
    if termasuk:
        if dpp is not None and ppn is not None and dasar is not None:
            if dekat(dpp + ppn, dasar, 2):
                hasil.append(("ok", "Harga sudah termasuk PPN: DPP {} + PPN {} = {}".format(
                    format_rp(dpp), format_rp(ppn), format_rp(dasar))))
            else:
                hasil.append(("selisih", "Harga termasuk PPN: DPP + PPN = {}, tapi dasar harga {}".format(
                    format_rp(dpp + ppn), format_rp(dasar))))
        elif dpp is None and dasar is not None and jenis_ppn in ("umum", ""):
            dpp_kira = (dasar * 100 / 111).quantize(Decimal(1), ROUND_HALF_UP)
            hasil.append(("info", "DPP tidak tercantum. Bila barang biasa: DPP = {} x 100/111 = {} dan PPN di "
                          "dalamnya +- {} (dihitung script, bukan dari dokumen)".format(
                              format_rp(dasar), format_rp(dpp_kira), format_rp(floor(dpp_kira * Decimal("0.11"))))))
    elif dpp is None and not f["dpp"].tt and dasar is not None and (ppn is not None or jenis_ppn in ("umum", "mewah")):
        dpp = dasar
        hasil.append(("info", "DPP tidak tertulis; dipakai subtotal setelah diskon {}".format(format_rp(dpp))))
    elif dpp is not None and dasar is not None and not dekat(dpp, dasar):
        hasil.append(("peringatan", "DPP {} berbeda dengan subtotal setelah diskon {}. Wajar bila ada uang muka "
                      "atau potongan lain; bila tidak, cek ulang.".format(format_rp(dpp), format_rp(dasar))))

    if dpp is not None and jenis_ppn in ("tidak_ada", "dibebaskan"):
        if ppn:
            hasil.append(("selisih", "Dokumen ditandai PPN {} tapi ada PPN {}".format(
                "dibebaskan" if jenis_ppn == "dibebaskan" else "tidak ada", format_rp(ppn))))
    elif dpp is not None and jenis_ppn == "lainnya":
        hasil.append(("info", "PPN memakai DPP/besaran khusus: di luar cakupan cek otomatis. Tanyakan ke konsultan/DJP"))
    elif dpp is not None and ppn is not None:
        jenis_uji = jenis_ppn or "umum"
        harus, cara, dnl = ppn_seharusnya(dpp, jenis_uji, tanggal)
        if dekat(harus, ppn):
            ppn_label = cara
            hasil.append(("ok", "PPN {} cocok: {}".format(format_rp(ppn), cara)))
        else:
            penuh = floor(dpp * Decimal("0.12"))
            if (not jenis_ppn or jenis_ppn == "umum") and (tanggal is None or tanggal >= TGL_PPN_12) and dekat(penuh, ppn):
                hasil.append(("peringatan", "PPN {} = 12% x DPP penuh. Ini benar HANYA untuk barang mewah (kena PPnBM). "
                              "Untuk barang/jasa biasa seharusnya {} (12% x 11/12 x DPP, efektif 11%). "
                              "Tanyakan ke penjual sebelum membayar.".format(format_rp(ppn), format_rp(harus))))
            elif jenis_uji == "mewah" and dekat(floor(dpp * Decimal("0.11")), ppn):
                hasil.append(("peringatan", "PPN {} = efektif 11%, padahal ditandai barang mewah (seharusnya 12% penuh "
                              "= {}). Cek apakah barang ini memang mewah.".format(format_rp(ppn), format_rp(harus))))
            else:
                hasil.append(("selisih", "PPN tertulis {}, hitungan script {} ({}); selisih {}".format(
                    format_rp(ppn), format_rp(harus), cara, format_rp(ppn - harus))))
        if dnl is not None and f["dpp_nilai_lain"].ada and not dekat(dnl, f["dpp_nilai_lain"].angka):
            hasil.append(("selisih", "DPP nilai lain tertulis {}, seharusnya 11/12 x DPP = {}".format(
                format_rp(f["dpp_nilai_lain"].angka), format_rp(dnl.quantize(Decimal(1), ROUND_HALF_UP)))))
    elif dpp is not None and ppn is None and not f["ppn"].tt and jenis in ("faktur_pajak",):
        hasil.append(("peringatan", "Faktur pajak tanpa angka PPN; cek ulang dokumen"))

    npwp_penjual = cek_npwp(penjual.get("npwp"), "NPWP penjual", hasil)
    npwp_pembeli = cek_npwp(pembeli.get("npwp"), "NPWP/NIK pembeli", hasil)
    cek_nitku(penjual.get("nitku"), npwp_penjual, "NITKU penjual", hasil)
    cek_nitku(pembeli.get("nitku"), npwp_pembeli, "NITKU pembeli", hasil)
    if jenis == "faktur_pajak":
        cek_nsfp(dok.get("nsfp"), tanggal, hasil)
        if kosong(penjual.get("npwp")):
            hasil.append(("peringatan", "Faktur pajak tanpa NPWP penjual; faktur pajak sah selalu mencantumkannya"))
    if ppn and not termasuk and jenis != "faktur_pajak" and kosong(penjual.get("npwp")) and jenis != "struk":
        hasil.append(("info", "Ada PPN tapi NPWP penjual tidak tercantum. Hanya PKP yang boleh memungut PPN; "
                      "bila perlu dikreditkan, minta faktur pajak ke penjual."))

    # --- total
    total = f["total"].angka
    if total is not None and not any(f[k].tt for k in ("ppn", "ppnbm", "biaya_lain", "potongan_lain")):
        basis = dasar if dasar is not None else dpp
        if basis is not None:
            harap = basis + (0 if termasuk else (ppn or 0)) + (f["ppnbm"].angka or 0) + \
                (f["biaya_lain"].angka or 0) - (f["potongan_lain"].angka or 0)
            pph, met = f["pph"].angka, f["meterai"].angka
            kandidat = [(harap, None)]
            if pph:
                kandidat.append((harap - pph, "total sudah dipotong PPh {}".format(format_rp(pph))))
            if met:
                kandidat.append((harap + met, "meterai {} ditagihkan ke pembeli".format(format_rp(met))))
            if pph and met:
                kandidat.append((harap - pph + met, "dipotong PPh dan meterai ditagihkan"))
            cocok = [k for k in kandidat if dekat(k[0], total)]
            if cocok:
                hasil.append(("ok", "Total {} cocok{}".format(format_rp(total), " (" + cocok[0][1] + ")" if cocok[0][1] else "")))
            else:
                hasil.append(("selisih", "Total tertulis {}, hitungan script {} (selisih {})".format(
                    format_rp(total), format_rp(harap), format_rp(total - harap))))
    elif total is None and not f["total"].tt and jenis not in ("faktur_pajak",):
        hasil.append(("peringatan", "Total tidak tercantum di dokumen"))
    total_rekap = total
    if total is None and not f["total"].tt and jenis == "faktur_pajak" and dpp is not None and ppn is not None \
            and not f["ppnbm"].tt:
        total_rekap = dpp + ppn + (f["ppnbm"].angka or 0)
        hasil.append(("info", "Faktur pajak tidak mencantumkan total; untuk rekap dipakai DPP + PPN = {} "
                      "(dihitung script)".format(format_rp(total_rekap))))

    # --- terbilang
    tb = dok.get("terbilang")
    if not kosong(tb) and not tidak_terbaca(tb) and total is not None:
        angka_tb = baca_terbilang(str(tb))
        if angka_tb is None:
            hasil.append(("peringatan", "Terbilang tidak bisa dibaca otomatis; bandingkan manual. Seharusnya: '{}'"
                          .format(terbilang(total))))
        elif dekat(angka_tb, total, 0):
            hasil.append(("ok", "Terbilang cocok dengan total"))
        else:
            hasil.append(("selisih", "Terbilang tertulis bernilai {}, tapi total {}. Terbilang yang benar: '{}'".format(
                format_rp(angka_tb), format_rp(total), terbilang(total))))

    # --- meterai
    if jenis == "kuitansi" and total is not None and total > BATAS_METERAI and f["meterai"].angka is None \
            and not dok.get("ada_meterai"):
        hasil.append(("info", "Kuitansi di atas Rp5.000.000 wajib bermeterai Rp10.000 (UU 10/2020). "
                      "Pastikan meterai tertempel; bila tidak, minta penjual melengkapi."))

    for k in tt:
        hasil.append(("tidak_terbaca", "Kolom '{}' tidak terbaca — tidak ditebak, mohon dicek dari dokumen asli".format(k)))

    level = {h[0] for h in hasil}
    if "selisih" in level:
        status = "ADA SELISIH"
    elif "tidak_terbaca" in level:
        status = "ADA YANG TIDAK TERBACA"
    elif "peringatan" in level:
        status = "PERLU DICEK"
    elif "ok" in level:
        status = "COCOK"
    else:
        status = "TERCATAT"  # tidak ada angka yang bisa dicocokkan (mis. hanya total)

    def out(n):
        return TIDAK_TERBACA if n.tt else n.angka

    rapi = OrderedDict([
        ("id", ident), ("jenis", jenis), ("nomor", str_bersih(dok.get("nomor"))),
        ("tanggal", tanggal.isoformat() if tanggal else (TIDAK_TERBACA if tidak_terbaca(tv) else None)),
        ("penjual", OrderedDict((k, str_bersih(penjual.get(k))) for k in ("nama", "npwp", "nitku", "alamat", "telepon"))),
        ("pembeli", OrderedDict((k, str_bersih(pembeli.get(k))) for k in ("nama", "npwp", "nitku", "alamat"))),
        ("nsfp", str_bersih(dok.get("nsfp"))), ("kategori", str_bersih(dok.get("kategori")) or "Belum dikategorikan"),
        ("item", items_out),
        ("subtotal", TIDAK_TERBACA if f["subtotal"].tt else subtotal), ("diskon", out(f["diskon"])),
        ("dpp", TIDAK_TERBACA if f["dpp"].tt else dpp), ("dpp_nilai_lain", out(f["dpp_nilai_lain"])),
        ("ppn", out(f["ppn"])), ("jenis_ppn", jenis_ppn or None), ("harga_termasuk_ppn", termasuk),
        ("ppnbm", out(f["ppnbm"])), ("pph", out(f["pph"])), ("jenis_pph", str_bersih(dok.get("jenis_pph"))),
        ("biaya_lain", out(f["biaya_lain"])), ("potongan_lain", out(f["potongan_lain"])),
        ("meterai", out(f["meterai"])), ("total", out(f["total"])), ("total_rekap", total_rekap),
        ("terbilang", str_bersih(tb)), ("metode_bayar", str_bersih(dok.get("metode_bayar"))),
        ("catatan", str_bersih(dok.get("catatan"))),
        ("ikut_rekap", bool(dok.get("ikut_rekap", jenis != "bukti_transfer"))),
        ("status_cek", status),
        ("hasil_cek", [OrderedDict([("level", h[0]), ("pesan", h[1])]) for h in hasil]),
        ("kolom_tidak_terbaca", tt),
    ])
    return rapi


def cari_dobel(docs):
    catatan, lihat = [], {}
    for d in docs:
        pj = (d["penjual"]["nama"] or "").strip().lower()
        kunci = []
        if d["nomor"] and d["nomor"] != TIDAK_TERBACA:
            kunci.append(("nomor", pj, d["nomor"].strip().lower()))
        if isinstance(d["total_rekap"], Decimal) and d["tanggal"] and d["tanggal"] != TIDAK_TERBACA:
            kunci.append(("tgl-total", pj, d["tanggal"], d["total_rekap"]))
        for k in kunci:
            if k in lihat and lihat[k]["id"] != d["id"]:
                lain = lihat[k]
                dasar = "nomor" if k[0] == "nomor" else "tanggal & total"
                if lain["ikut_rekap"] and d["ikut_rekap"]:
                    catatan.append("[!] {} dan {} kemungkinan transaksi yang sama (penjual, {} sama; mis. invoice + "
                                   "faktur pajaknya). Keduanya ikut dihitung di rekap. Bila memang sama, tandai salah "
                                   "satu \"ikut_rekap\": false.".format(lain["id"], d["id"], dasar))
                else:
                    catatan.append("[i] {} dan {} tampaknya transaksi yang sama (penjual, {} sama); hanya satu yang "
                                   "dihitung di rekap.".format(lain["id"], d["id"], dasar))
                break
            lihat.setdefault(k, d)
    return catatan


def rekap(docs):
    ikut = [d for d in docs if d["ikut_rekap"]]
    r = OrderedDict()
    r["jumlah_dokumen"] = len(docs)
    r["dokumen_direkap"] = len(ikut)
    r["tidak_direkap"] = [d["id"] for d in docs if not d["ikut_rekap"]]
    tanpa_total = [d["id"] for d in ikut if not isinstance(d["total_rekap"], Decimal)]
    r["tanpa_total_terbaca"] = tanpa_total

    def jumlah(kunci, sumber):
        return sum((d[kunci] for d in sumber if isinstance(d[kunci], Decimal)), Decimal(0))

    r["total_pengeluaran"] = jumlah("total_rekap", ikut)
    r["total_ppn_tercantum"] = jumlah("ppn", ikut)
    r["ppn_dari_faktur_pajak"] = jumlah("ppn", [d for d in ikut if d["jenis"] == "faktur_pajak"])
    r["total_pph_dipotong"] = jumlah("pph", ikut)
    for nama, fungsi in (("per_kategori", lambda d: d["kategori"]),
                         ("per_penjual", lambda d: d["penjual"]["nama"] or "(tanpa nama)"),
                         ("per_bulan", lambda d: d["tanggal"][:7] if d["tanggal"] and d["tanggal"] != TIDAK_TERBACA
                          else "(tanpa tanggal)")):
        grup = OrderedDict()
        for d in ikut:
            if isinstance(d["total_rekap"], Decimal):
                k = fungsi(d)
                g = grup.setdefault(k, {"jumlah_dokumen": 0, "total": Decimal(0)})
                g["jumlah_dokumen"] += 1
                g["total"] += d["total_rekap"]
        if nama == "per_bulan":
            r[nama] = OrderedDict(sorted(grup.items()))
        else:
            r[nama] = OrderedDict(sorted(grup.items(), key=lambda kv: -kv[1]["total"]))
    status = OrderedDict()
    for d in docs:
        status[d["status_cek"]] = status.get(d["status_cek"], 0) + 1
    r["ringkasan_status"] = status
    r["kemungkinan_dobel"] = cari_dobel(docs)
    return r


# ================================================================ keluaran
_IKON = {"ok": "[OK]", "info": "[i]", "peringatan": "[!]", "selisih": "[X]", "tidak_terbaca": "[?]"}


def teks_laporan(docs, rk):
    b = []
    b.append("HASIL CEK NOTA/FAKTUR ({} dokumen)".format(len(docs)))
    b.append("")
    b.append("| # | Tanggal | Penjual | Jenis | Total | Status |")
    b.append("|---|---|---|---|---|---|")
    for d in docs:
        tot = d["total"] if d["total"] is not None else d["total_rekap"]
        b.append("| {} | {} | {} | {} | {} | {} |".format(
            d["id"], d["tanggal"] or "-", d["penjual"]["nama"] or "-", d["jenis"],
            "TIDAK TERBACA" if tot == TIDAK_TERBACA else format_rp(tot), d["status_cek"]))
    b.append("")
    for d in docs:
        b.append("{} - {} ({})".format(d["id"], d["penjual"]["nama"] or "-", d["status_cek"]))
        for h in d["hasil_cek"]:
            b.append("  {} {}".format(_IKON[h["level"]], h["pesan"]))
        b.append("")
    if len(docs) > 1:
        b.append("REKAP PENGELUARAN ({} dokumen direkap)".format(rk["dokumen_direkap"]))
        b.append("- Total pengeluaran: {}".format(format_rp(rk["total_pengeluaran"])))
        b.append("- PPN tercantum di semua dokumen: {} (dari faktur pajak: {})".format(
            format_rp(rk["total_ppn_tercantum"]), format_rp(rk["ppn_dari_faktur_pajak"])))
        if rk["total_pph_dipotong"]:
            b.append("- PPh dipotong: {} (sudah dikurangkan dari total; wajib disetor ke negara oleh pihak "
                     "yang memotong, jadi siapkan dananya)".format(format_rp(rk["total_pph_dipotong"])))
        for judul, kunci in (("Per kategori", "per_kategori"), ("Per penjual", "per_penjual"), ("Per bulan", "per_bulan")):
            b.append("")
            b.append("{}:".format(judul))
            b.append("| {} | Dokumen | Total |".format(judul.split()[1].capitalize()))
            b.append("|---|---|---|")
            for k, g in rk[kunci].items():
                b.append("| {} | {} | {} |".format(k, g["jumlah_dokumen"], format_rp(g["total"])))
        if rk["tanpa_total_terbaca"]:
            b.append("")
            b.append("Belum masuk total (total tidak terbaca/tidak ada): " + ", ".join(rk["tanpa_total_terbaca"]))
        if rk["tidak_direkap"]:
            b.append("Tidak direkap (bukti transfer/ditandai ikut_rekap=false): " + ", ".join(rk["tidak_direkap"]))
        for c in rk["kemungkinan_dobel"]:
            b.append(c)
    b.append("")
    b.append("Dasar aturan PPN: UU HPP & PMK 131/2024, berlaku per {}. Format NPWP/NITKU/nomor seri faktur: {} "
             "(hanya peringatan). Alat bantu cek, bukan nasihat pajak.".format(TANGGAL_ATURAN, BELUM_VERIF))
    return "\n".join(b)


def _angka_csv(v, desimal):
    if v is None:
        return ""
    if v == TIDAK_TERBACA:
        return "TIDAK TERBACA"
    if isinstance(v, Decimal):
        if v == v.to_integral_value():
            return str(int(v))
        s = "{:.2f}".format(v)
        return s.replace(".", ",") if desimal == "koma" else s
    return str(v)


def _id_csv(v, polos):
    if v is None:
        return ""
    if v == TIDAK_TERBACA:
        return "TIDAK TERBACA"
    return v if polos or not re.fullmatch(r"\d+", v) else '="{}"'.format(v)


def ke_csv(docs, mode, pemisah, desimal, id_polos):
    buf = io.StringIO()
    w = csv.writer(buf, delimiter=pemisah, lineterminator="\n")
    if mode == "dokumen":
        w.writerow(["No", "ID", "Tanggal", "Jenis", "Nomor Dokumen", "Penjual", "NPWP Penjual", "Pembeli",
                    "Kategori", "Subtotal", "Diskon", "DPP", "PPN", "PPh", "Biaya Lain", "Total", "Metode Bayar",
                    "Status Cek", "Kolom Tidak Terbaca", "Catatan"])
        for i, d in enumerate(docs, 1):
            w.writerow([i, d["id"], d["tanggal"] or "", d["jenis"], _id_csv(d["nomor"] or d["nsfp"], id_polos), d["penjual"]["nama"] or "",
                        _id_csv(d["penjual"]["npwp"], id_polos), d["pembeli"]["nama"] or "", d["kategori"]] +
                       [_angka_csv(d[k], desimal) for k in ("subtotal", "diskon", "dpp", "ppn", "pph", "biaya_lain")] +
                       [_angka_csv(d["total"] if d["total"] is not None else d["total_rekap"], desimal)] +
                       [d["metode_bayar"] or "", d["status_cek"], ", ".join(d["kolom_tidak_terbaca"]), d["catatan"] or ""])
    else:
        w.writerow(["ID", "Tanggal", "Penjual", "Nomor Dokumen", "Kategori", "Nama Item", "Qty", "Satuan",
                    "Harga Satuan", "Diskon", "Jumlah"])
        for d in docs:
            for it in d["item"]:
                w.writerow([d["id"], d["tanggal"] or "", d["penjual"]["nama"] or "", d["nomor"] or "", d["kategori"],
                            it["nama"] or "", _angka_csv(it["qty"], desimal), it["satuan"] or "",
                            _angka_csv(it["harga_satuan"], desimal), _angka_csv(it["diskon"], desimal),
                            _angka_csv(it["jumlah"], desimal)])
    return buf.getvalue()


def main(argv=None):
    ap = argparse.ArgumentParser(description="Cek angka & format nota/faktur, ekspor CSV/JSON, rekap pengeluaran.")
    ap.add_argument("file", nargs="?", help="file JSON hasil ekstraksi ('-' = baca dari stdin)")
    ap.add_argument("--format", choices=["teks", "json", "csv"], default="teks")
    ap.add_argument("--csv", dest="csv_mode", choices=["dokumen", "item"], default="dokumen",
                    help="CSV satu baris per dokumen (default) atau per item")
    ap.add_argument("--pemisah", default=";", help="pemisah CSV: ';' (default, Excel Indonesia), ',' atau 'tab'")
    ap.add_argument("--desimal", choices=["koma", "titik"], help="tanda desimal di CSV (default ikut pemisah)")
    ap.add_argument("--id-polos", action="store_true",
                    help="tulis NPWP apa adanya (tanpa =\"...\" yang menjaga angka 0 di depan di Excel)")
    ap.add_argument("--output", help="simpan hasil ke file ini (CSV disimpan UTF-8 dengan BOM agar rapi di Excel)")
    ap.add_argument("--hari-ini", help="tanggal acuan (YYYY-MM-DD), default tanggal komputer")
    ap.add_argument("--terbilang", metavar="ANGKA", help="hanya cetak terbilang untuk angka ini")
    a = ap.parse_args(argv)
    try:
        if a.terbilang is not None:
            print(terbilang(parse_angka(a.terbilang, "angka terbilang")))
            return 0
        if not a.file:
            raise GalatInput("sebutkan file JSON hasil ekstraksi, mis. python3 cek_nota.py nota.json")
        pem = {"tab": "\t", "\\t": "\t", "titikkoma": ";", "koma": ","}.get(a.pemisah, a.pemisah)
        if pem not in (";", ",", "\t", "|"):
            raise GalatInput("pemisah harus ';', ',', 'tab' atau '|'")
        desimal = a.desimal or ("titik" if pem == "," else "koma")
        if pem == "," and desimal == "koma":
            raise GalatInput("pemisah ',' tidak bisa dipakai bersama desimal koma; pakai --pemisah ';'")
        hari_ini = parse_tanggal(a.hari_ini) if a.hari_ini else dt.date.today()
        try:
            if a.file == "-":
                data = json.load(sys.stdin)
            else:
                with open(a.file, encoding="utf-8-sig") as fh:
                    data = json.load(fh)
        except FileNotFoundError:
            raise GalatInput("file '{}' tidak ditemukan".format(a.file))
        except json.JSONDecodeError as e:
            raise GalatInput("file bukan JSON yang valid (baris {}, kolom {}): {}".format(e.lineno, e.colno, e.msg))
        if isinstance(data, dict) and "dokumen" in data:
            daftar = data["dokumen"]
        elif isinstance(data, list):
            daftar = data
        elif isinstance(data, dict):
            daftar = [data]
        else:
            raise GalatInput("isi JSON harus objek dokumen atau {\"dokumen\": [...]}")
        if not isinstance(daftar, list) or not daftar:
            raise GalatInput("tidak ada dokumen untuk dicek")
        docs = [cek_dokumen(d, i, hari_ini) for i, d in enumerate(daftar, 1)]
        rk = rekap(docs)
        if a.format == "json":
            keluar = json.dumps(OrderedDict([("dokumen", docs), ("rekap", rk),
                                             ("dasar_aturan", "UU HPP & PMK 131/2024, per " + TANGGAL_ATURAN)]),
                                ensure_ascii=False, indent=2, default=ke_json)
        elif a.format == "csv":
            keluar = ke_csv(docs, a.csv_mode, pem, desimal, a.id_polos)
        else:
            keluar = teks_laporan(docs, rk)
        if a.output:
            with open(a.output, "w", encoding="utf-8-sig" if a.format == "csv" else "utf-8", newline="") as fh:
                fh.write(keluar)
            print("Tersimpan: {}".format(a.output))
        else:
            sys.stdout.write(keluar if keluar.endswith("\n") else keluar + "\n")
        return 0
    except GalatInput as e:
        sys.stderr.write("ERROR: {}\n".format(e))
        return 2


if __name__ == "__main__":
    sys.exit(main())
