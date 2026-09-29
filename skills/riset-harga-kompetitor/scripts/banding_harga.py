#!/usr/bin/env python3
"""Bandingkan harga produk kita dengan harga pesaing, lalu hitung rekomendasi harga jual.

Input : file CSV atau JSON berisi daftar pesaing (satu baris = satu produk pesaing),
        plus data produk kita (HPP, ukuran, biaya marketplace, target margin) lewat argumen
        atau kunci "produk_kita" di file JSON.
Output: tabel pembanding (harga setara ukuran kita), statistik pasar (terendah, P25, median,
        P75, tertinggi), posisi harga kita, harga minimum (HPP + biaya + margin), dan rentang
        harga rekomendasi. Format Markdown (default) atau JSON (--format json).

Aturan hitung (ditulis juga di hasil):
- Semua hitungan memakai Decimal tanpa pembulatan; tampilan dibulatkan ke rupiah terdekat.
- Harga minimum = (HPP + biaya tetap per barang) / (1 - total biaya marketplace % - target margin %),
  dibulatkan KE ATAS ke rupiah penuh supaya target margin tidak pernah kurang.
- Margin = laba / harga jual (bukan markup).
- Harga rentang "49.900-59.900" memakai harga terendah (bisa diubah dengan --rentang).
- Ukuran berbeda disetarakan: harga setara = harga / isi pesaing x isi produk kita (satuan g, ml, atau pcs).
- Ukuran seperti "1/2 kg", "setengah kilo", "250 g x 2", "isi 2 @250gr", "250 g + 250 g", "500 gr isi 2", "2 pack 500 gr" dibaca lengkap.
- Harga setara yang di bawah setengah atau di atas dua kali median (min. 3 pesaing) TIDAK ikut statistik
  (tetap tampil di tabel), kecuali --pakai-semua.
- Persentil memakai interpolasi linear (sama dengan PERCENTILE.INC di Excel/Google Sheets).
- HPP kosong -> mode "pasar saja": hanya statistik harga pasar, tanpa batas harga & rekomendasi.

Hanya library standar Python 3.8+. TIDAK ada akses jaringan: script ini tidak membuka link apa pun.

Contoh:
  python3 banding_harga.py pesaing.csv --hpp 38.000 --ukuran "250 gr" --harga-kita 65.000 \
      --biaya-persen 8 --biaya-persen 4 --biaya-persen 0,5 --biaya-tetap 1.250 --margin 20
  python3 banding_harga.py pesaing.json --format json
"""
import argparse
import csv
import io
import json
import re
import sys
from datetime import date, datetime
from decimal import Decimal, ROUND_CEILING, ROUND_HALF_UP, InvalidOperation
from urllib.parse import urlsplit

BATAS_ATAS = Decimal(10) ** 12
MAKS_BARIS = 500
HARI_DATA_LAMA = 30
STRATEGI = ("murah", "tengah", "premium")
KOLOM_LEBIH, KOLOM_KURANG, KOLOM_HEADER = "__kolom_lebih__", "__kolom_kurang__", "__kolom_header__"


class InputError(ValueError):
    """Kesalahan input yang harus dijelaskan ke pengguna."""


# ------------------------------------------------------------------ angka format Indonesia
_SUFIKS = [("miliar", 10 ** 9), ("milyar", 10 ** 9), ("juta", 10 ** 6), ("jt", 10 ** 6),
           ("ribu", 10 ** 3), ("rb", 10 ** 3), ("k", 10 ** 3)]
_POLA_SUFIKS = re.compile(r"(miliar|milyar|juta|jt|ribu|rb|k)$")


def _grup_ribuan_ok(grup):
    return 1 <= len(grup[0]) <= 3 and all(len(g) == 3 for g in grup[1:])


def parse_angka(nilai, nama="angka"):
    """Baca angka gaya Indonesia: 'Rp49.900', 'Rp 1,2 jt', '49,9rb', '1rb+', '49900', '4,9'.

    Aturan pemisah: grup 3 digit = ribuan ('49.900' atau '49,900'); dengan akhiran rb/jt/k,
    pemisah diikuti 1-2 digit = desimal ('49,9rb' = 49.900). Tanpa akhiran, angka seperti
    '49,9' dianggap ambigu untuk rupiah dan ditolak oleh parse_rupiah (lihat izinkan_desimal).
    """
    return _parse(nilai, nama, izinkan_desimal=True)


def parse_rupiah(nilai, nama="harga"):
    """Seperti parse_angka tetapi menolak desimal tanpa akhiran ('49,9' ambigu) dan nilai <= 0."""
    v = _parse(nilai, nama, izinkan_desimal=False)
    if v <= 0:
        raise InputError("{}: harus lebih dari 0".format(nama))
    if v > BATAS_ATAS:
        raise InputError("{}: '{}' terlalu besar".format(nama, nilai))
    return v


def _parse(nilai, nama, izinkan_desimal):
    if nilai is None or isinstance(nilai, bool):
        raise InputError("{}: kosong".format(nama))
    if isinstance(nilai, Decimal):
        return nilai
    if isinstance(nilai, int):
        return Decimal(nilai)
    if isinstance(nilai, float):
        return Decimal(str(nilai))
    asli = str(nilai)
    s = asli.strip().lower().replace(" ", "").replace(" ", "")
    s = re.sub(r"^(rp|idr)\.?", "", s)
    s = re.sub(r"([,.]-+|,00)$", "", s)
    if s.startswith("-") and re.search(r"\d", s):
        raise InputError("{}: '{}' tidak boleh negatif".format(nama, asli))
    if not s:
        raise InputError("{}: kosong".format(nama))
    pengali = 1
    m = _POLA_SUFIKS.search(s)
    if m:
        pengali = dict(_SUFIKS)[m.group(1)]
        s = s[: m.start()].rstrip(".")
    if not re.fullmatch(r"\d+([.,]\d+)*", s):
        raise InputError("{}: '{}' bukan angka yang dikenali".format(nama, asli))
    pemisah = re.findall(r"[.,]", s)
    grup = re.split(r"[.,]", s)
    if not pemisah:
        angka = Decimal(s)
    elif len(set(pemisah)) == 1 and _grup_ribuan_ok(grup):
        angka = Decimal("".join(grup))          # 49.900 / 49,900 / 1.250.000
    else:
        idx = max(s.rfind("."), s.rfind(","))
        kepala, ekor = s[:idx], s[idx + 1:]
        sep_desimal = s[idx]
        sep_kepala = set(re.findall(r"[.,]", kepala))
        kepala_ok = not sep_kepala or (sep_desimal not in sep_kepala and len(sep_kepala) == 1
                                       and _grup_ribuan_ok(re.split(r"[.,]", kepala)))
        boleh = pengali > 1 or izinkan_desimal or bool(sep_kepala)
        if not (kepala_ok and boleh and (1 <= len(ekor) <= 2 or pengali > 1)):
            raise InputError("{}: '{}' ambigu. Tulis lengkap, mis. 49.900 atau 49,9rb".format(nama, asli))
        angka = Decimal(re.sub(r"[.,]", "", kepala) + "." + ekor)
    return angka * pengali


_POLA_RENTANG = re.compile(r"\s*(?:–|—|~|\bs\.?/?d\.?(?=\s|\d|rp)|\bsampai\b|\bhingga\b|-)\s*", re.I)


HARGA_MIN = Decimal(100)


def cek_harga_wajar(v, nama, asli):
    """Harga rupiah di bawah Rp 100 hampir pasti salah tulis (mis. 49,9 = 49.900?)."""
    if v < HARGA_MIN:
        raise InputError("{}: '{}' terlalu kecil untuk harga rupiah (di bawah Rp 100). Maksudnya ribuan? "
                         "Tulis lengkap, mis. 49.900 atau 49,9rb".format(nama, asli))
    return v


def parse_harga(nilai, nama="harga"):
    """parse_rupiah + tolak nilai di bawah Rp 100 (berlaku juga untuk angka JSON seperti 49.9)."""
    return cek_harga_wajar(parse_rupiah(nilai, nama), nama, nilai)


def parse_rentang(teks, nama="harga"):
    """'Rp49.900 - Rp59.900' / '49-59rb' / '49.900 s/d 59.900' -> (terendah, tertinggi). Harga < Rp 100 ditolak."""
    if isinstance(teks, (int, float, Decimal)) and not isinstance(teks, bool):
        v = parse_harga(teks, nama)
        return v, v
    t = str(teks or "").strip()
    t = re.sub(r"[,.]-+(?!\s*\d)", "", t)          # buang ',-' seperti 'Rp49.900,-'
    if re.match(r"(?:rp|idr)?\.?\s*-\s*\d", t, re.I):
        raise InputError("{}: '{}' tidak boleh negatif".format(nama, teks))
    bagian = [b for b in _POLA_RENTANG.split(t) if b and b.strip()]
    if not bagian:
        raise InputError("{}: kosong".format(nama))
    if len(bagian) > 2:
        raise InputError("{}: '{}' tidak dikenali sebagai harga atau rentang harga".format(nama, teks))
    if len(bagian) == 2:
        a, b = bagian
        suf_b = _POLA_SUFIKS.search(b.strip().lower().replace(" ", ""))
        suf_a = _POLA_SUFIKS.search(a.strip().lower().replace(" ", ""))
        if suf_b and not suf_a:
            coba = parse_rupiah(a, nama)
            if coba < 1000:
                a = a.strip() + suf_b.group(1)          # '49-59rb' -> 49rb - 59rb
        lo, hi = sorted((parse_rupiah(a, nama), parse_rupiah(b, nama)))
        return cek_harga_wajar(lo, nama, teks), hi
    v = parse_rupiah(bagian[0], nama)
    return cek_harga_wajar(v, nama, teks), v


def parse_terjual(teks):
    """'1rb+ terjual' -> 1000, '2,3RB' -> 2300, '500+' -> 500. None bila kosong."""
    if teks is None or str(teks).strip() == "":
        return None
    t = str(teks).lower()
    t = re.sub(r"terjual|sold|ulasan|review(s)?|penilaian|rating|[+()]", "", t).strip()
    if not t:
        return None
    return int(parse_angka(t, "terjual"))


def parse_rating(teks):
    if teks is None or str(teks).strip() == "":
        return None
    m = re.search(r"\d+(?:[.,]\d+)?", str(teks))
    if not m:
        raise InputError("rating: '{}' tidak dikenali".format(teks))
    v = Decimal(m.group(0).replace(",", "."))
    if not 0 <= v <= 5:
        raise InputError("rating: '{}' di luar 0-5".format(teks))
    return v


# ------------------------------------------------------------------ ukuran & satuan
_SATUAN = {
    "mg": ("g", Decimal("0.001")), "g": ("g", 1), "gr": ("g", 1), "grm": ("g", 1), "gram": ("g", 1),
    "ons": ("g", 100), "kg": ("g", 1000), "kilo": ("g", 1000), "kilogram": ("g", 1000),
    "ml": ("ml", 1), "cc": ("ml", 1), "l": ("ml", 1000), "lt": ("ml", 1000), "ltr": ("ml", 1000),
    "liter": ("ml", 1000),
    "pcs": ("pcs", 1), "pc": ("pcs", 1), "buah": ("pcs", 1), "bh": ("pcs", 1), "biji": ("pcs", 1),
    "lembar": ("pcs", 1), "lbr": ("pcs", 1), "sachet": ("pcs", 1), "butir": ("pcs", 1),
    "pasang": ("pcs", 1), "tablet": ("pcs", 1), "kapsul": ("pcs", 1), "roll": ("pcs", 1),
    "lusin": ("pcs", 12), "kodi": ("pcs", 20),
}
_SAT_RE = "|".join(sorted(_SATUAN, key=len, reverse=True))
_SAT_NON_PCS = "|".join(sorted((k for k, v in _SATUAN.items() if v[0] != "pcs"), key=len, reverse=True))
# kata kemasan yang boleh menempel pada pengali: "2 pcs @ 250 gr", "250 gr x 2 pcs", "isi 2 bungkus @250gr"
_KEMASAN = ("pcs|pc|buah|bh|biji|bungkus|bks|pack|pak|pax|sachet|botol|btl|pouch|toples|jar|box|dus|kotak|"
            "kaleng|cup|pasang|lembar|lbr|roll|tube")
_NUM = r"\d+(?:[.,]\d+)?"
# pecahan (1/2 kg, 1 1/2 kg) atau angka biasa (250 gr, 0,5 kg, 1.000 ml)
_POLA_UKUR = re.compile(r"(?<![\d.,/])(?:(?:(\d+)\s+)?(\d+)\s*/\s*(\d+)|(%s))\s*(%s)\b" % (_NUM, _SAT_RE))
_POLA_DEPAN = re.compile(r"(?<![\d.,/])(\d+)\s*(?:(?:%s)\s*)?(?:[x*]\s*@?|@)\s*$" % _KEMASAN)
_POLA_BELAKANG = re.compile(r"\s*[x*]\s*(\d+)(?![\d.,/])(?!\s*(?:%s)\b)(?:\s*(?:%s)\b)?" % (_SAT_NON_PCS, _KEMASAN))
_POLA_ISI = re.compile(r"\bisi\s*(\d+)\b(?!\s*(?:%s)\b)" % _SAT_RE)
# v1.0.2 (U1): pengali tanpa 'x'/'@'. Kemasan penuh (bukan pcs/biji/buah = butir isi) di depan ukuran:
# '2 pack 500 gr', '3 botol 250 ml'. 'isi N' tepat di belakang ukuran: '500 gr isi 2', '250gr (isi 2)',
# 'isi 2 pack'. 'isi 10 pcs 250 gr' / '250 gr isi 10 pcs' = jumlah butir di dalam, TIDAK dikalikan.
_KEMASAN_PENUH = ("bungkus|bks|pack|pak|pax|sachet|botol|btl|pouch|toples|jar|box|dus|kotak|kaleng|cup|tube|"
                  "renceng|karton")
_POLA_DEPAN_KEMASAN = re.compile(r"(?<![\d.,/])(?<!isi )(?<!isi)(\d+)\s*(?:%s)\s*$" % _KEMASAN_PENUH)
_POLA_BELAKANG_ISI = re.compile(r"\s*[(\[,-]?\s*isi\s*(\d+)(?![\d.,/])(?!\s*(?:%s|pcs|pc|buah|bh|biji|butir|"
                                r"lembar|lbr|potong|keping|keping|slice)\b)(?:\s*(?:%s)\b)?\s*[)\]]?" %
                                (_SAT_RE, _KEMASAN_PENUH))
_KATA = [(r"\bsetengah\s*", "1/2 "), (r"\bseperempat\s*", "1/4 "), (r"\btiga\s+perempat\s*", "3/4 "),
         ("½", " 1/2"), ("¼", " 1/4"), ("¾", " 3/4"), ("×", "x")]


def _angka_ukuran(s):
    if re.fullmatch(r"\d{1,3}([.,]\d{3})+", s):
        return Decimal(re.sub(r"[.,]", "", s))       # 1.000 ml
    return Decimal(s.replace(",", "."))               # 0,5 kg / 1.5 kg


def _pecahan(utuh, pembilang, penyebut, asli):
    pb, py = int(pembilang), int(penyebut)
    sisa = py
    for f in (2, 5):
        while sisa and sisa % f == 0:
            sisa //= f
    if py == 0 or sisa != 1:
        raise InputError("pecahan '{}' tidak bisa dipakai; tulis dalam gram/ml, mis. 500 gr".format(asli.strip()))
    return Decimal(int(utuh or 0)) + Decimal(pb) / Decimal(py)


def baca_ukuran(teks, dim_pilih=None):
    """Baca ukuran dari teks bebas. Kembalikan ((dim, jumlah) atau None, [catatan]).

    Dikenali: '250 gr', '1/2 kg', 'setengah kilo', '1 1/2 kg', '12 x 25 g', '250 g x 2', '250gr x 2 pcs',
    'isi 2 @250gr', 'Paket 2 pcs @ 250 gr', '250 g + 250 g', 'isi 12'. Bila teks memuat beberapa ukuran
    berbeda (mis. 'isi 10 pcs 250 gr'), dipilih yang satuannya sama dengan dim_pilih (satuan produk kita).
    InputError bila ukuran jelas ada tetapi tidak bisa dibaca dengan aman (pecahan aneh, g + ml).
    """
    if teks is None or str(teks).strip() == "":
        return None, []
    t = str(teks).lower()
    for pola, ganti in _KATA:
        t = re.sub(pola, ganti, t)
    grup, habis, catatan_kali = [], 0, []
    for m in _POLA_UKUR.finditer(t):
        if m.start() < habis:
            continue
        dim, kali = _SATUAN[m.group(5)]
        if m.group(4) is not None:
            qty = _angka_ukuran(m.group(4))
        else:
            qty = _pecahan(m.group(1), m.group(2), m.group(3), m.group(0))
        qty = qty * Decimal(kali)
        mulai, akhir, jumlah_kemasan = m.start(), m.end(), None
        d = _POLA_DEPAN.search(t, 0, m.start())
        tanpa_kali = False
        if not d:
            d = _POLA_DEPAN_KEMASAN.search(t, habis, m.start())       # v1.0.2: '2 pack 500 gr'
            tanpa_kali = bool(d)
        if d:
            mulai, jumlah_kemasan = d.start(), int(d.group(1))
            grup = [g for g in grup if g["akhir"] <= mulai]          # '2 pcs' di '2 pcs @ 250 gr' ikut terpakai
        bl = _POLA_BELAKANG.match(t, m.end())
        if not bl:
            bl = _POLA_BELAKANG_ISI.match(t, m.end())                 # v1.0.2: '500 gr isi 2', '250gr (isi 2)'
            tanpa_kali = tanpa_kali or bool(bl)
        if bl:
            akhir = bl.end()
            jumlah_kemasan = (jumlah_kemasan or 1) * int(bl.group(1))
        if not jumlah_kemasan:
            ik = re.search(r"\bisi\s*(\d+)\s*(?:%s)\s*$" % _KEMASAN_PENUH, t[habis:m.start()])
            if ik and int(ik.group(1)) > 1:                          # 'isi 2 pack 500 gr': dibaca total, beri tahu
                catatan_kali.append("'{}' dibaca total {}; cek: bila {} itu per kemasan, tulis '{} x {}'".format(
                    (ik.group(0) + t[m.start():m.end()]).strip(), teks_ukuran(dim, qty), teks_ukuran(dim, qty),
                    ik.group(1), teks_ukuran(dim, qty)))
        if tanpa_kali and jumlah_kemasan and jumlah_kemasan > 1:
            catatan_kali.append("'{}' dibaca {} kemasan x {} = {}; cek: bila angka itu sudah total, tulis ulang "
                                "ukurannya".format(re.sub(r"[()\[\]]", "", t[mulai:akhir]).strip(" ,-"), jumlah_kemasan,
                                                   teks_ukuran(dim, qty), teks_ukuran(dim, qty * jumlah_kemasan)))
        if jumlah_kemasan:
            qty = qty * jumlah_kemasan
        sek = [("pcs", Decimal(jumlah_kemasan))] if jumlah_kemasan and dim != "pcs" else []
        # '250 g + 250 g': gabungkan dengan grup sebelumnya
        if grup and re.fullmatch(r"\s*\+\s*", t[grup[-1]["akhir"]:mulai]):
            sebelum = grup[-1]
            if sebelum["dim"] != dim:
                raise InputError("ukuran '{}' menjumlahkan satuan berbeda ({} + {})".format(
                    str(teks).strip(), sebelum["dim"], dim))
            sebelum["qty"] += qty
            sebelum["akhir"] = akhir
            sebelum["sek"] = []
        else:
            grup.append({"dim": dim, "qty": qty, "mulai": mulai, "akhir": akhir, "sek": sek})
        habis = akhir
    if not grup:
        m = _POLA_ISI.search(t)
        return (("pcs", Decimal(m.group(1))), []) if m else (None, [])
    pilih, catatan = grup[0], list(catatan_kali)
    if dim_pilih:
        cocok = [g for g in grup if g["dim"] == dim_pilih]
        if cocok:
            pilih = cocok[0]
        else:
            sek = [s for g in grup for s in g["sek"] if s[0] == dim_pilih]
            if sek:
                catatan.append("dibaca sebagai {} kemasan".format(fmt_desimal(sek[0][1])))
                return sek[0], catatan
    beda = []
    for g in grup:
        if (g["dim"], g["qty"]) not in beda:
            beda.append((g["dim"], g["qty"]))
    if len(beda) > 1:
        catatan.append("teks memuat beberapa ukuran ({}), dipakai {}".format(
            ", ".join(teks_ukuran(*u) for u in beda), teks_ukuran(pilih["dim"], pilih["qty"])))
    return (pilih["dim"], pilih["qty"]), catatan


def parse_ukuran(teks, dim_pilih=None):
    """'250 gr' -> ('g', 250); '1/2 kg' -> ('g', 500); '250 g x 2' -> ('g', 500); 'isi 12' -> ('pcs', 12)."""
    return baca_ukuran(teks, dim_pilih)[0]


def teks_ukuran(dim, qty):
    q = qty.normalize()
    if dim == "g" and qty >= 1000 and qty % 100 == 0:
        return "{} kg".format(fmt_desimal(qty / 1000))
    if dim == "ml" and qty >= 1000 and qty % 100 == 0:
        return "{} L".format(fmt_desimal(qty / 1000))
    return "{} {}".format(fmt_desimal(q), dim)


# ------------------------------------------------------------------ format & statistik
def bulat(x):
    return x.quantize(Decimal(1), rounding=ROUND_HALF_UP)


def rp(x):
    if x is None:
        return "-"
    n = int(bulat(x))
    s = "{:,}".format(abs(n)).replace(",", ".")
    return ("-Rp " if n < 0 else "Rp ") + s


def fmt_desimal(x, digit=2):
    x = Decimal(x)
    if x == x.to_integral_value():
        return "{:,}".format(int(x)).replace(",", ".")
    s = "{:.{}f}".format(x, digit).rstrip("0").rstrip(".")
    return s.replace(".", ",")


def persen(x):
    return fmt_desimal(bulat_ke(x * 100, "0.01")) + "%"


def bulat_ke(x, q):
    return x.quantize(Decimal(q), rounding=ROUND_HALF_UP)


def persentil(urut, p):
    """Interpolasi linear (PERCENTILE.INC). urut harus sudah terurut naik."""
    if not urut:
        raise InputError("tidak ada data harga")
    pos = (len(urut) - 1) * Decimal(p)
    bawah = int(pos)
    atas = min(bawah + 1, len(urut) - 1)
    return urut[bawah] + (urut[atas] - urut[bawah]) * (pos - bawah)


# ------------------------------------------------------------------ baca input
_ALIAS = {
    "nama": ("nama", "produk", "nama_produk", "judul", "product", "name"),
    "toko": ("toko", "penjual", "seller", "nama_toko", "shop"),
    "platform": ("platform", "marketplace", "kanal"),
    "varian": ("varian", "variasi", "variant", "tipe"),
    "ukuran": ("ukuran", "isi", "berat", "volume", "size", "netto"),
    "harga": ("harga", "harga_jual", "harga_tayang", "harga_promo", "price"),
    "harga_coret": ("harga_coret", "harga_asli", "harga_normal", "harga_sebelum_diskon", "coret",
                    "original_price"),
    "promo": ("promo", "promo_ongkir", "gratis_ongkir", "catatan_promo", "voucher", "catatan"),
    "rating": ("rating", "bintang", "nilai"),
    "terjual": ("terjual", "sold", "jumlah_terjual"),
    "ulasan": ("ulasan", "review", "reviews", "jumlah_ulasan", "penilaian"),
    "lokasi": ("lokasi", "kota", "asal", "dikirim_dari", "location"),
    "sumber": ("sumber", "link", "url", "tautan"),
    "tanggal": ("tanggal", "tanggal_cek", "dicek", "tgl", "date"),
}
_ALIAS_BALIK = {a: k for k, daftar in _ALIAS.items() for a in daftar}


def _kunci(k):
    return re.sub(r"[^a-z0-9]+", "_", str(k).strip().lower()).strip("_")


def normalisasi_baris(d):
    hasil = {}
    for k, v in d.items():
        kk = _ALIAS_BALIK.get(_kunci(k))
        if kk and kk not in hasil:
            hasil[kk] = v.strip() if isinstance(v, str) else v
    return hasil


def _dekode(path, data):
    """Kembalikan (teks, [info]). Coba UTF-8 (dengan/tanpa BOM), UTF-16 ber-BOM, lalu ANSI Windows (cp1252)."""
    if data.startswith(b"PK\x03\x04") or data.startswith(b"\xd0\xcf\x11\xe0"):
        raise InputError("file '{}' adalah file Excel, bukan CSV. Di Excel pilih File > Save As > "
                         "'CSV UTF-8 (Comma delimited)', lalu kirim file CSV-nya.".format(path))
    if data.startswith((b"\xff\xfe", b"\xfe\xff")):
        try:
            return data.decode("utf-16"), []
        except UnicodeDecodeError:
            pass
    if b"\x00" in data:
        raise InputError("file '{}' bukan file teks CSV/JSON (berisi data biner). Simpan ulang sebagai "
                         "'CSV UTF-8' atau tempel datanya sebagai teks.".format(path))
    try:
        return data.decode("utf-8-sig"), []
    except UnicodeDecodeError:
        pass
    try:
        return data.decode("cp1252"), ["File dibaca sebagai ANSI/Windows-1252 (bukan UTF-8). Cek huruf khusus "
                                       "di tabel; bila ada yang aneh, simpan ulang sebagai 'CSV UTF-8'."]
    except UnicodeDecodeError:
        raise InputError("file '{}' memakai encoding yang tidak dikenali. Simpan ulang sebagai 'CSV UTF-8' "
                         "(Excel: File > Save As > CSV UTF-8).".format(path))


def baca_file(path):
    """Kembalikan (daftar baris pesaing, dict produk_kita dari file atau {}, [info untuk 'Perlu dicek'])."""
    try:
        with open(path, "rb") as f:
            data = f.read()
    except OSError as e:
        raise InputError("file '{}' tidak bisa dibaca: {}".format(path, e))
    teks, info = _dekode(path, data)
    if teks.startswith("\ufeff"):
        teks = teks[1:]
    if path.lower().endswith(".json") or teks.lstrip().startswith(("[", "{")):
        try:
            data = json.loads(teks)
        except ValueError as e:
            raise InputError("JSON tidak valid: {}".format(e))
        produk = {}
        if isinstance(data, dict):
            produk = data.get("produk_kita") or {}
            data = data.get("pesaing", [])
        if not isinstance(data, list) or not all(isinstance(x, dict) for x in data):
            raise InputError("JSON harus berupa daftar objek atau {\"produk_kita\": {...}, \"pesaing\": [...]}")
        return data, produk, info
    if not teks.strip():
        raise InputError("file kosong")
    try:
        dialek = csv.Sniffer().sniff(teks.splitlines()[0], delimiters=",;\t")
    except csv.Error:
        dialek = csv.excel
    baris = []
    try:
        pembaca = csv.DictReader(io.StringIO(teks), dialect=dialek)
        n_kolom = len(pembaca.fieldnames or [])
        for row in pembaca:
            lebih = [x for x in (row.pop(None, None) or []) if str(x).strip()]
            if lebih:
                row[KOLOM_LEBIH] = n_kolom + len(lebih)
            if any(v is None for v in row.values()):
                row = {k: ("" if v is None else v) for k, v in row.items()}
                if any(str(v).strip() for k, v in row.items() if k != KOLOM_LEBIH):
                    row[KOLOM_KURANG] = True
            row[KOLOM_HEADER] = n_kolom
            baris.append(row)
    except csv.Error as e:
        raise InputError("CSV tidak bisa dibaca: {}".format(e))
    return baris, {}, info


def parse_tanggal(teks):
    if not teks:
        return None
    for pola in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d/%m/%y"):
        try:
            return datetime.strptime(str(teks).strip(), pola).date()
        except ValueError:
            pass
    return None


def kunci_duplikat(b):
    if b.get("sumber"):
        u = urlsplit(str(b["sumber"]).strip())
        if u.netloc:
            return ("url", u.netloc.lower().replace("www.", ""), u.path.rstrip("/").lower())
    return tuple(re.sub(r"\s+", " ", str(b.get(k) or "")).strip().lower()
                 for k in ("toko", "nama", "varian", "ukuran", "harga"))


# ------------------------------------------------------------------ inti analisis
_PILIH_STRATEGI = {"murah": ("terendah", "p25", "p25"), "tengah": ("p25", "p75", "median"),
                   "premium": ("p75", "p90", "p75")}
_DASAR_STRATEGI = {"murah": "terendah - P25, titik P25", "tengah": "P25 - P75, titik median",
                   "premium": "P75 - P90, titik P75"}


def olah(baris_mentah, produk, strategi="tengah", mode_rentang="min", hari_ini=None, pakai_semua=False):
    hari_ini = hari_ini or date.today()
    if strategi not in STRATEGI:
        raise InputError("strategi harus salah satu dari: " + ", ".join(STRATEGI))
    if len(baris_mentah) > MAKS_BARIS:
        raise InputError("maksimal {} baris pesaing".format(MAKS_BARIS))
    if not baris_mentah:
        raise InputError("file tidak berisi data pesaing (hanya judul kolom atau daftar kosong). "
                         "Isi minimal satu baris: toko, ukuran, harga.")
    normal = [normalisasi_baris(m) for m in baris_mentah]
    if not any("harga" in b for b in normal):
        kolom = [str(k) for k in baris_mentah[0] if not str(k).startswith("__kolom_")]
        raise InputError("kolom harga tidak ditemukan (kolom yang terbaca: {}). Beri judul kolom 'harga' "
                         "pada kolom harga tayang.".format(", ".join(kolom) or "-"))

    # ---- produk kita
    hpp_ada = produk.get("hpp") not in (None, "")
    hpp = parse_rupiah(produk["hpp"], "HPP") if hpp_ada else None
    tetap = parse_angka(produk.get("biaya_tetap") or 0, "biaya tetap")
    if tetap < 0:
        raise InputError("biaya tetap tidak boleh negatif")
    daftar_biaya = produk.get("biaya_persen") or []
    if not isinstance(daftar_biaya, list):
        daftar_biaya = [daftar_biaya]
    biaya_persen = Decimal(0)
    for b in daftar_biaya:
        v = parse_angka(str(b).replace("%", ""), "biaya persen")
        if v < 0 or v >= 100:
            raise InputError("biaya persen harus 0 sampai di bawah 100 (dapat: {})".format(b))
        biaya_persen += v
    margin_diberikan = produk.get("margin") not in (None, "")
    margin = parse_angka(str(produk["margin"]).replace("%", ""), "margin") if margin_diberikan else Decimal(20)
    if margin < 0 or margin >= 100:
        raise InputError("target margin harus 0 sampai di bawah 100%")
    if biaya_persen + margin >= 100:
        raise InputError("total biaya marketplace ({}%) + target margin ({}%) >= 100%: target mustahil"
                         .format(fmt_desimal(biaya_persen), fmt_desimal(margin)))
    f, m = biaya_persen / 100, margin / 100
    ukuran_kita = None
    if produk.get("ukuran"):
        try:
            ukuran_kita = parse_ukuran(produk.get("ukuran"))
        except InputError as e:
            raise InputError("ukuran produk kita: {}".format(e))
        if not ukuran_kita:
            raise InputError("ukuran produk kita '{}' tidak dikenali (contoh: 250 gr, 1 kg, 500 ml, 12 pcs; "
                             "produk satuan: 1 pcs)".format(produk.get("ukuran")))
    dim_kita = ukuran_kita[0] if ukuran_kita else None
    harga_kita = parse_harga(produk["harga_kita"], "harga kita") if produk.get("harga_kita") not in (None, "") else None

    if hpp_ada:
        balik_modal = ((hpp + tetap) / (1 - f)).quantize(Decimal(1), rounding=ROUND_CEILING)
        minimum = ((hpp + tetap) / (1 - f - m)).quantize(Decimal(1), rounding=ROUND_CEILING)
    else:
        balik_modal = minimum = None

    def laba(p):
        if not hpp_ada:
            return None, None
        l = p - p * f - hpp - tetap
        return l, (l / p)

    # ---- pesaing
    peringatan, dilewati, duplikat, pesaing = [], [], [], []
    if not hpp_ada:
        peringatan.append("HPP/modal per barang belum diisi: yang dihitung hanya harga pasar. Batas untung dan "
                          "rekomendasi harga jual muncul setelah HPP diisi (tawarkan skill hitung-hpp).")
    elif biaya_persen == 0 and tetap == 0:
        peringatan.append("Biaya marketplace dianggap 0 (jualan langsung). Kalau jualan di Shopee/Tokopedia/TikTok "
                          "Shop, isi persen biaya admin/layanan/PPh 22 agar harga minimum tidak terlalu rendah.")
    terlihat = {}
    for no, (mentah, b) in enumerate(zip(baris_mentah, normal), start=1):
        label = b.get("toko") or b.get("nama") or "baris {}".format(no)
        if not any(str(v or "").strip() for v in b.values()):
            continue
        if mentah.get(KOLOM_LEBIH):
            dilewati.append("baris {} ({}): jumlah kolom {} padahal judul kolom {}. Kemungkinan ada nilai berkoma "
                            "tanpa tanda kutip (mis. 1,2RB terjual atau 4,9) sehingga kolom bergeser. Beri tanda "
                            "kutip pada nilai itu (\"4,9\") atau pakai file JSON".format(
                                no, label, mentah[KOLOM_LEBIH], mentah.get(KOLOM_HEADER, "?")))
            continue
        if mentah.get(KOLOM_KURANG):
            peringatan.append("Baris {} ({}): jumlah kolom lebih sedikit dari judul kolom; cek apakah isinya "
                              "bergeser.".format(no, label))
        k = kunci_duplikat(b)
        harga_teks = re.sub(r"\s+", " ", str(b.get("harga") or "")).strip()
        if k in terlihat:
            no_awal, harga_awal = terlihat[k]
            beda = "" if harga_teks == harga_awal else "; harga beda ({} vs {}), dipakai baris {} - pastikan mana " \
                                                       "yang terbaru".format(harga_awal, harga_teks, no_awal)
            duplikat.append("baris {} ({}) sama dengan baris {}{}".format(no, label, no_awal, beda))
            continue
        terlihat[k] = (no, harga_teks)
        try:
            lo, hi = parse_rentang(b.get("harga"), "harga")
        except InputError as e:
            dilewati.append("baris {} ({}): {}".format(no, label, e))
            continue
        catatan = []
        if lo != hi:
            harga = {"min": lo, "maks": hi, "tengah": (lo + hi) / 2}[mode_rentang]
            catatan.append("rentang {}-{}, dipakai {}".format(rp(lo), rp(hi),
                           {"min": "terendah", "maks": "tertinggi", "tengah": "nilai tengah"}[mode_rentang]))
        else:
            harga = lo
        coret = None
        if str(b.get("harga_coret") or "").strip():
            try:
                coret = parse_rentang(b["harga_coret"], "harga coret")[1]
                if coret <= harga:
                    catatan.append("harga coret <= harga, diabaikan")
                    coret = None
            except InputError:
                catatan.append("harga coret tidak terbaca")
        rating = terjual = ulasan = None
        for fld in ("rating", "terjual", "ulasan"):
            try:
                if fld == "rating":
                    rating = parse_rating(b.get("rating"))
                elif fld == "terjual":
                    terjual = parse_terjual(b.get("terjual"))
                else:
                    ulasan = parse_terjual(b.get("ulasan"))
            except InputError:
                catatan.append("{} tidak terbaca".format(fld))
        # ukuran: kolom ukuran dulu, lalu varian, lalu nama; utamakan satuan yang sama dengan produk kita
        calon = []
        for fld in ("ukuran", "varian", "nama"):
            if b.get(fld):
                try:
                    uk, cat = baca_ukuran(b[fld], dim_kita)
                except InputError as e:
                    calon.append((fld, None, ["ukuran tidak jelas: {}".format(e)]))
                    continue
                if uk:
                    calon.append((fld, uk, cat))
        ukuran, asal_ukuran = None, None
        pilihan = [c for c in calon if c[1] and (not dim_kita or c[1][0] == dim_kita)] or \
                  [c for c in calon if c[1]] or calon
        if pilihan:
            asal_ukuran, ukuran, cat = pilihan[0]
            catatan += cat
            catatan += [c for fld, uk, cc in calon if uk is None and fld != asal_ukuran for c in cc]
            if ukuran and calon and calon[0][1] and calon[0][0] != asal_ukuran:
                catatan.append("{} di kolom {} tidak sesatuan dengan produk kamu".format(
                    teks_ukuran(*calon[0][1]), calon[0][0]))
        if ukuran and asal_ukuran != "ukuran":
            catatan.append("ukuran dibaca dari {}".format(asal_ukuran))
        tgl = parse_tanggal(b.get("tanggal"))
        if tgl and (hari_ini - tgl).days > HARI_DATA_LAMA:
            catatan.append("data lama ({})".format(tgl.isoformat()))
        teks_all = " ".join(str(b.get(x) or "") for x in ("nama", "varian", "promo")).lower()
        bundling = bool(re.search(r"bundl|paket|beli\s*\d|buy\s*\d|\bfree\b|gratis\s+(?!ongkir)|bonus|hemat\s*\d", teks_all))
        pesaing.append({
            "no": no, "toko": b.get("toko") or "", "nama": b.get("nama") or "", "platform": b.get("platform") or "",
            "varian": b.get("varian") or "", "ukuran_teks": b.get("ukuran") or "",
            "ukuran": ukuran, "harga": harga, "harga_coret": coret,
            "promo": b.get("promo") or "", "rating": rating, "terjual": terjual, "ulasan": ulasan,
            "lokasi": b.get("lokasi") or "", "sumber": b.get("sumber") or "",
            "tanggal": tgl.isoformat() if tgl else (b.get("tanggal") or ""), "bundling": bundling,
            "catatan": catatan, "dihitung": False,
        })

    # ---- penyetaraan ukuran
    ukuran_pesaing = {p["ukuran"] for p in pesaing if p["ukuran"]}
    tanpa_ukuran = [p for p in pesaing if not p["ukuran"]]
    if ukuran_kita:
        dasar = "harga setara {} (ukuran produk kamu)".format(teks_ukuran(*ukuran_kita))
        for p in pesaing:
            if not p["ukuran"]:
                p["setara"] = None
                p["catatan"].append("ukuran tidak diketahui, tidak ikut dihitung" +
                                    (" (produk satuan? tulis 1 pcs)" if dim_kita == "pcs" else ""))
            elif p["ukuran"][0] != ukuran_kita[0]:
                p["setara"] = None
                p["catatan"].append("satuan beda ({} vs {}), tidak ikut dihitung".format(p["ukuran"][0], ukuran_kita[0]))
            else:
                p["setara"] = p["harga"] / p["ukuran"][1] * ukuran_kita[1]
    else:
        dasar = "harga tayang apa adanya (ukuran produk kamu tidak disebut)"
        for p in pesaing:
            p["setara"] = p["harga"]
        if len(ukuran_pesaing) > 1:
            peringatan.append("Ukuran pesaing berbeda-beda ({}) tetapi ukuran produk kamu belum disebut, "
                              "jadi harga dibandingkan apa adanya dan bisa menyesatkan. Sebutkan ukuran produkmu."
                              .format(", ".join(sorted(teks_ukuran(*u) for u in ukuran_pesaing))))
        elif ukuran_pesaing and tanpa_ukuran:
            peringatan.append("{} pesaing mencantumkan ukuran/isi ({}) dan {} tidak. Bila produknya satuan, tulis "
                              "ukuran '1 pcs' untuk produkmu dan pesaing; bila ada paket (mis. 2 pcs), sebutkan "
                              "ukuran produkmu supaya harga disetarakan.".format(
                                  len(pesaing) - len(tanpa_ukuran),
                                  ", ".join(sorted(teks_ukuran(*u) for u in ukuran_pesaing)), len(tanpa_ukuran)))
    for p in pesaing:
        if p["ukuran"]:
            basis = Decimal(100) if p["ukuran"][0] in ("g", "ml") else Decimal(1)
            p["per_satuan"] = p["harga"] / p["ukuran"][1] * basis
            p["label_satuan"] = "per 100 {}".format(p["ukuran"][0]) if basis == 100 else "per pcs"
        else:
            p["per_satuan"], p["label_satuan"] = None, ""

    dipakai = [p for p in pesaing if p["setara"] is not None]
    if not dipakai:
        raise InputError("tidak ada harga pesaing yang bisa dipakai (semua baris kosong, rusak, atau ukurannya "
                         "tidak bisa disetarakan). Minta pengguna menempel harga + ukuran pesaing.")

    # ---- pencilan: jauh dari median -> keluar dari statistik (tetap tampil di tabel)
    pencilan = []
    if len(dipakai) >= 3:
        med0 = persentil(sorted(p["setara"] for p in dipakai), "0.5")
        jauh = [p for p in dipakai if p["setara"] < med0 / 2 or p["setara"] > med0 * 2]
        for p in jauh:
            if pakai_semua:
                p["catatan"].append("jauh dari median {}, tetap dihitung (--pakai-semua)".format(rp(med0)))
            else:
                p["catatan"].append("jauh dari median {}: TIDAK ikut statistik; cek varian/ukuran/keaslian"
                                    .format(rp(med0)))
        if jauh and not pakai_semua:
            pencilan = jauh
            dipakai = [p for p in dipakai if p not in jauh]
            peringatan.append("{} pesaing jauh dari median awal {} (di bawah separuh atau di atas dua kali lipat) "
                              "TIDAK ikut statistik: {}. Tanyakan ke pengguna apakah harga/ukurannya benar dan "
                              "sebanding; bila benar, jalankan ulang dengan --pakai-semua.".format(
                                  len(jauh), rp(med0), "; ".join("baris {} ({}, setara {})".format(
                                      p["no"], p["toko"] or p["nama"] or "-", rp(p["setara"])) for p in jauh)))
    for p in dipakai:
        p["dihitung"] = True
    urut = sorted(p["setara"] for p in dipakai)
    stat = {"n": len(urut), "terendah": urut[0], "p25": persentil(urut, "0.25"), "median": persentil(urut, "0.5"),
            "p75": persentil(urut, "0.75"), "p90": persentil(urut, "0.9"), "tertinggi": urut[-1]}
    if len(urut) < 3:
        peringatan.append("Hanya {} pesaing yang bisa dibandingkan: rekomendasi kurang andal, tambah data "
                          "(idealnya 5-20 pesaing).".format(len(urut)))
    elif len(urut) < 5:
        peringatan.append("Baru {} pesaing: cukup untuk gambaran, lebih andal bila 5-20.".format(len(urut)))

    posisi = None
    if harga_kita is not None:
        lebih_murah = sum(1 for x in urut if x > harga_kita)
        sama = sum(1 for x in urut if x == harga_kita)
        lebih_mahal = sum(1 for x in urut if x < harga_kita)
        l, mg = laba(harga_kita)
        posisi = {"harga": harga_kita, "lebih_murah_dari": lebih_murah, "sama_dengan": sama,
                  "lebih_mahal_dari": lebih_mahal,
                  "persentil": (Decimal(lebih_mahal) + Decimal(sama) / 2) / len(urut) * 100,
                  "laba": l, "margin": mg, "di_bawah_minimum": hpp_ada and harga_kita < minimum}

    # ---- rekomendasi (hanya bila HPP ada)
    rekom = None
    if hpp_ada:
        pilih = _PILIH_STRATEGI[strategi]

        def jaga(x):
            return max(minimum, bulat(x))

        r_lo, r_hi, r_titik = jaga(stat[pilih[0]]), jaga(stat[pilih[1]]), jaga(stat[pilih[2]])
        r_hi = max(r_hi, r_lo)
        cantik = harga_cantik(r_lo, r_hi, r_titik)
        tanda = []
        if stat["p75"] < minimum:
            tanda.append("PASAR_DI_BAWAH_MINIMUM")
        elif stat["median"] < minimum:
            tanda.append("MEDIAN_DI_BAWAH_MINIMUM")
        if posisi and posisi["di_bawah_minimum"]:
            tanda.append("HARGA_KITA_DI_BAWAH_MINIMUM")
        rekom = {"strategi": strategi, "dasar": _DASAR_STRATEGI[strategi], "rentang_bawah": r_lo,
                 "rentang_atas": r_hi, "titik": r_titik, "harga_cantik": cantik, "tanda": tanda}
        rekom["laba_titik"], rekom["margin_titik"] = laba(r_titik)
        if cantik:
            rekom["laba_cantik"], rekom["margin_cantik"] = laba(cantik)

    # ---- promo & bundling (semua pesaing di tabel)
    diskon = [(p["harga_coret"] - p["harga"]) / p["harga_coret"] for p in pesaing if p["harga_coret"]]
    promo = {
        "harga_coret": len(diskon), "rata_diskon": (sum(diskon) / len(diskon)) if diskon else None,
        "promo_ongkir": sum(1 for p in pesaing if re.search(r"ongkir|free\s*ship", p["promo"].lower())),
        "bundling": [p["toko"] or p["nama"] for p in pesaing if p["bundling"]],
        "total": len(pesaing),
    }
    terlaris = max((p for p in dipakai if p["terjual"] is not None), key=lambda p: p["terjual"], default=None)

    return {
        "mode": "lengkap" if hpp_ada else "pasar_saja",
        "produk": {"nama": produk.get("nama") or "Produk kamu", "hpp": hpp, "biaya_tetap": tetap,
                   "biaya_persen": biaya_persen, "margin": margin, "margin_default": not margin_diberikan,
                   "ukuran": ukuran_kita, "harga_kita": harga_kita, "balik_modal": balik_modal, "minimum": minimum},
        "dasar": dasar, "pesaing": pesaing, "stat": stat, "posisi": posisi, "rekomendasi": rekom,
        "promo": promo, "terlaris": terlaris, "peringatan": peringatan, "dilewati": dilewati,
        "duplikat": duplikat, "pencilan": [p["no"] for p in pencilan], "baris_total": len(baris_mentah),
        "mode_rentang": mode_rentang, "tanggal": hari_ini.isoformat(),
    }


def harga_cantik(lo, hi, titik):
    """Harga berakhiran 900 (mis. 54.900) di dalam [lo, hi] yang paling dekat ke titik. None bila tidak ada."""
    if hi < 2000:
        return None
    bawah = ((int(titik) + 100) // 1000) * 1000 - 100
    calon = [Decimal(c) for c in (bawah, bawah + 1000) if lo <= c <= hi]
    return min(calon, key=lambda c: (abs(c - titik), c)) if calon else None


# ------------------------------------------------------------------ keluaran
def _sel(x):
    return str(x).replace("|", "/").replace("\n", " ").strip() or "-"


def ke_markdown(h):
    pr, st, rk = h["produk"], h["stat"], h["rekomendasi"]
    ukuran = teks_ukuran(*pr["ukuran"]) if pr["ukuran"] else None
    o = ["## Riset Harga Pesaing: {}{}".format(pr["nama"], " ({})".format(ukuran) if ukuran else ""), ""]
    if h["mode"] == "pasar_saja":
        o += ["**Mode harga pasar saja** (HPP belum diisi: batas untung & rekomendasi harga belum dihitung).", ""]
    o.append("Tanggal analisis: {} | Pesaing dibandingkan: **{}** dari {} baris ({} duplikat dibuang, "
             "{} baris dilewati{})".format(h["tanggal"], st["n"], h["baris_total"], len(h["duplikat"]),
                                           len(h["dilewati"]),
                                           ", {} jauh dari median tidak dihitung".format(len(h["pencilan"]))
                                           if h["pencilan"] else ""))
    o.append("Dasar banding: {}".format(h["dasar"]))
    o += ["", "| # | Toko / Produk | Varian / Ukuran | Harga tayang | Harga coret | Harga setara | Per satuan | "
              "Rating | Terjual | Lokasi | Catatan |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for i, p in enumerate(h["pesaing"], 1):
        nama = " - ".join(x for x in (p["toko"], p["nama"]) if x) or "-"
        var = " / ".join(x for x in (p["varian"], p["ukuran_teks"]) if x) or (teks_ukuran(*p["ukuran"]) if p["ukuran"] else "-")
        per = "{} {}".format(rp(p["per_satuan"]), p["label_satuan"]) if p["per_satuan"] is not None else "-"
        terj = fmt_desimal(p["terjual"]) if p["terjual"] is not None else "-"
        o.append("| {} | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(
            i, _sel(nama), _sel(var), rp(p["harga"]), rp(p["harga_coret"]),
            rp(p["setara"]) if p["setara"] is not None else "-", per,
            "{:.1f}".format(p["rating"]).replace(".", ",") if p["rating"] is not None else "-", terj, _sel(p["lokasi"]),
            _sel("; ".join(p["catatan"]))))
    o += ["", "### Ringkasan harga pasar", "",
          "| Terendah | Kuartil bawah (P25) | Median (tengah) | Kuartil atas (P75) | Tertinggi |",
          "|---|---|---|---|---|",
          "| {} | {} | **{}** | {} | {} |".format(rp(st["terendah"]), rp(st["p25"]), rp(st["median"]),
                                                  rp(st["p75"]), rp(st["tertinggi"])), ""]
    ps = h["posisi"]
    if ps:
        kalimat = ("- Harga kamu sekarang **{}**: lebih murah dari {} pesaing, sama dengan {}, lebih mahal dari {} "
                   "(posisi sekitar persentil {}).".format(
                       rp(ps["harga"]), ps["lebih_murah_dari"], ps["sama_dengan"], ps["lebih_mahal_dari"],
                       fmt_desimal(bulat(ps["persentil"]))))
        if ps["laba"] is not None:
            kalimat += " Laba {} per barang (margin {}).".format(rp(ps["laba"]), persen(ps["margin"]))
        o.append(kalimat)
    if h["terlaris"]:
        t = h["terlaris"]
        o.append("- Pesaing paling laris: {} (sekitar {} terjual) di harga setara {}.".format(
            _sel(t["toko"] or t["nama"]), fmt_desimal(t["terjual"]), rp(t["setara"])))
    if rk is None:
        o += ["", "### Batas harga & rekomendasi", "",
              "- **Belum dihitung: HPP/modal per barang belum diisi.** Kirim modal per barang (bahan + kemasan), "
              "persen biaya marketplace, dan target untung; lalu jalankan ulang dengan `--hpp`. Tanpa HPP, "
              "harga pasar di atas belum menjamin untung."]
    else:
        o += ["", "### Batas harga kamu", "",
              "| Komponen | Nilai |", "|---|---|",
              "| HPP/modal per barang | {} |".format(rp(pr["hpp"])),
              "| Biaya tetap per barang (mis. biaya proses pesanan) | {} |".format(rp(pr["biaya_tetap"])),
              "| Total biaya marketplace (% dari harga jual) | {}% |".format(fmt_desimal(pr["biaya_persen"])),
              "| Target margin (laba / harga jual) | {}%{} |".format(fmt_desimal(pr["margin"]),
                                                                    " (default)" if pr["margin_default"] else ""),
              "| Harga balik modal (laba 0) | {} |".format(rp(pr["balik_modal"])),
              "| **Harga minimum sesuai target margin** | **{}** |".format(rp(pr["minimum"])), ""]
        nama_s = {"murah": "murah (bersaing harga)", "tengah": "tengah pasar",
                  "premium": "premium (di atas kuartil atas)"}[rk["strategi"]]
        o += ["### Rekomendasi harga (strategi {})".format(nama_s), "",
              "- **Rentang harga: {} - {}** (dasar: {} pasar)".format(
                  rp(rk["rentang_bawah"]), rp(rk["rentang_atas"]), rk["dasar"]),
              "- Titik rekomendasi: **{}** (laba {} per barang, margin {})".format(
                  rp(rk["titik"]), rp(rk["laba_titik"]), persen(rk["margin_titik"]))]
        if rk["harga_cantik"]:
            o.append("- Harga cantik terdekat (masih di dalam rentang): **{}** (laba {}, margin {})".format(
                rp(rk["harga_cantik"]), rp(rk["laba_cantik"]), persen(rk["margin_cantik"])))
        pesan = {
            "PASAR_DI_BAWAH_MINIMUM": "PERHATIAN: sebagian besar pesaing (sampai kuartil atas) menjual di bawah harga "
                                      "minimum kamu {}. Jangan ikut banting harga; pertimbangkan menekan HPP, bundling, "
                                      "ukuran berbeda, atau menonjolkan keunggulan.".format(rp(pr["minimum"])),
            "MEDIAN_DI_BAWAH_MINIMUM": "PERHATIAN: median pasar {} di bawah harga minimum kamu {}. Rekomendasi "
                                       "dinaikkan ke batas minimum; kamu akan tampil lebih mahal dari separuh pesaing."
                                       .format(rp(st["median"]), rp(pr["minimum"])),
            "HARGA_KITA_DI_BAWAH_MINIMUM": "PERHATIAN: harga kamu sekarang di bawah harga minimum; margin target "
                                           "tidak tercapai.",
        }
        for t in rk["tanda"]:
            o.append("- " + pesan[t])
    pm = h["promo"]
    o += ["", "### Promo & bundling pesaing", "",
          "- {} dari {} pesaing di tabel memasang harga coret{}.".format(
              pm["harga_coret"], pm["total"],
              " (diskon rata-rata {})".format(persen(pm["rata_diskon"])) if pm["rata_diskon"] is not None else ""),
          "- {} dari {} pesaing di tabel mencantumkan promo/gratis ongkir.".format(pm["promo_ongkir"], pm["total"])]
    if pm["bundling"]:
        o.append("- Terlihat bundling/paket/bonus: {}.".format(", ".join(_sel(x) for x in pm["bundling"])))
    if h["peringatan"] or h["dilewati"] or h["duplikat"]:
        o += ["", "### Perlu dicek"]
        o += ["- " + x for x in h["peringatan"] + h["dilewati"] + h["duplikat"]]
    o += ["", "### Catatan & asumsi",
          "- Harga pesaing = harga yang tampil saat dicek (setelah diskon toko), belum termasuk ongkir dan voucher "
          "platform; bisa berubah kapan saja.",
          "- Harga rentang memakai harga {}.".format({"min": "terendah", "maks": "tertinggi", "tengah": "nilai tengah"}[h["mode_rentang"]]),
          "- Statistik hanya memakai pesaing yang ukurannya bisa disetarakan dan tidak jauh dari median "
          "(di bawah separuh / di atas dua kali lipat median dikeluarkan bila ada minimal 3 pesaing).",
          "- Persentil: interpolasi linear (seperti PERCENTILE.INC di Excel)."]
    if rk is not None:
        o += ["- Harga minimum = (HPP + biaya tetap) / (1 - biaya marketplace % - target margin %), dibulatkan ke atas "
              "ke rupiah penuh. Nilai lain dibulatkan ke rupiah terdekat.",
              "- Rekomendasi tidak pernah di bawah harga minimum. Ini bahan keputusan, bukan jaminan laku."]
    return "\n".join(o)


def _json_aman(x):
    if isinstance(x, Decimal):
        return str(bulat_ke(x, "0.01"))
    if isinstance(x, tuple):
        return {"satuan": x[0], "jumlah": _json_aman(x[1])}
    if isinstance(x, dict):
        return {k: _json_aman(v) for k, v in x.items()}
    if isinstance(x, list):
        return [_json_aman(v) for v in x]
    return x


# ------------------------------------------------------------------ CLI
def main(argv=None):
    ap = argparse.ArgumentParser(description="Bandingkan harga pesaing & hitung rekomendasi harga jual")
    ap.add_argument("file", help="CSV atau JSON daftar pesaing")
    ap.add_argument("--nama", help="nama produk kita")
    ap.add_argument("--hpp", help="HPP/modal per barang, mis. 38.000 (kosong = mode harga pasar saja)")
    ap.add_argument("--ukuran", help="ukuran produk kita, mis. '250 gr', '1 L', '12 pcs'")
    ap.add_argument("--harga-kita", help="harga jual kita sekarang (opsional)")
    ap.add_argument("--margin", help="target margin %% dari harga jual (default 20)")
    ap.add_argument("--biaya-persen", action="append", help="biaya marketplace %% (boleh diulang: admin, layanan, PPh 22, dll.)")
    ap.add_argument("--biaya-tetap", help="biaya tetap per barang dalam Rp (mis. biaya proses pesanan)")
    ap.add_argument("--strategi", default="tengah", choices=STRATEGI)
    ap.add_argument("--rentang", default="min", choices=("min", "tengah", "maks"),
                    help="harga yang dipakai untuk rentang '49.900-59.900' (default min)")
    ap.add_argument("--pakai-semua", action="store_true",
                    help="ikutkan pesaing yang jauh dari median ke statistik (setelah dikonfirmasi benar)")
    ap.add_argument("--tanggal", help="tanggal analisis YYYY-MM-DD (default hari ini)")
    ap.add_argument("--format", default="md", choices=("md", "json"))
    a = ap.parse_args(argv)
    try:
        baris, produk, info = baca_file(a.file)
        produk = dict(produk)
        for kunci, nilai in (("nama", a.nama), ("hpp", a.hpp), ("ukuran", a.ukuran), ("harga_kita", a.harga_kita),
                             ("margin", a.margin), ("biaya_persen", a.biaya_persen), ("biaya_tetap", a.biaya_tetap)):
            if nilai not in (None, "", []):
                produk[kunci] = nilai
        hari = parse_tanggal(a.tanggal) if a.tanggal else date.today()
        if a.tanggal and not hari:
            raise InputError("--tanggal harus YYYY-MM-DD")
        hasil = olah(baris, produk, a.strategi, a.rentang, hari, a.pakai_semua)
        hasil["peringatan"] = info + hasil["peringatan"]
    except (InputError, InvalidOperation) as e:
        print("ERROR: {}".format(e), file=sys.stderr)
        return 2
    if a.format == "json":
        print(json.dumps(_json_aman(hasil), ensure_ascii=False, indent=2))
    else:
        print(ke_markdown(hasil))
    return 0


if __name__ == "__main__":
    sys.exit(main())
