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
- Persentil memakai interpolasi linear (sama dengan PERCENTILE.INC di Excel/Google Sheets).

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


def parse_rentang(teks, nama="harga"):
    """'Rp49.900 - Rp59.900' / '49-59rb' / '49.900 s/d 59.900' -> (terendah, tertinggi)."""
    if isinstance(teks, (int, float, Decimal)) and not isinstance(teks, bool):
        v = parse_rupiah(teks, nama)
        return v, v
    t = str(teks or "").strip()
    t = re.sub(r"[,.]-+(?!\s*\d)", "", t)          # buang ',-' seperti 'Rp49.900,-'
    if t.startswith("-"):
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
        return lo, hi
    v = parse_rupiah(bagian[0], nama)
    return v, v


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
_NUM = r"\d+(?:[.,]\d+)?"
_POLA_KALI = re.compile(r"(?<![\d.,])(%s)\s*[x×*]\s*(%s)\s*(%s)\b" % (_NUM, _NUM, _SAT_RE))
_POLA_UKURAN = re.compile(r"(?<![\d.,])(%s)\s*(%s)\b" % (_NUM, _SAT_RE))
_POLA_ISI = re.compile(r"\bisi\s*(\d+)\b(?!\s*(?:%s)\b)" % _SAT_RE)


def _angka_ukuran(s):
    if re.fullmatch(r"\d{1,3}([.,]\d{3})+", s):
        return Decimal(re.sub(r"[.,]", "", s))       # 1.000 ml
    return Decimal(s.replace(",", "."))               # 0,5 kg / 1.5 kg


def parse_ukuran(teks):
    """'250 gr' -> ('g', 250); '1 L' -> ('ml', 1000); '12 x 25 g' -> ('g', 300); 'isi 12' -> ('pcs', 12)."""
    if teks is None:
        return None
    t = str(teks).lower().replace("×", "x")
    m = _POLA_KALI.search(t)
    if m:
        dim, kali = _SATUAN[m.group(3)]
        return dim, _angka_ukuran(m.group(1)) * _angka_ukuran(m.group(2)) * Decimal(kali)
    m = _POLA_UKURAN.search(t)
    if m:
        dim, kali = _SATUAN[m.group(2)]
        return dim, _angka_ukuran(m.group(1)) * Decimal(kali)
    m = _POLA_ISI.search(t)
    if m:
        return "pcs", Decimal(m.group(1))
    return None


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


def baca_file(path):
    """Kembalikan (daftar baris pesaing, dict produk_kita dari file atau {})."""
    try:
        with open(path, encoding="utf-8-sig") as f:
            teks = f.read()
    except OSError as e:
        raise InputError("file '{}' tidak bisa dibaca: {}".format(path, e))
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
        return data, produk
    if not teks.strip():
        raise InputError("file kosong")
    try:
        dialek = csv.Sniffer().sniff(teks.splitlines()[0], delimiters=",;\t")
    except csv.Error:
        dialek = csv.excel
    return list(csv.DictReader(io.StringIO(teks), dialect=dialek)), {}


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
def olah(baris_mentah, produk, strategi="tengah", mode_rentang="min", hari_ini=None):
    hari_ini = hari_ini or date.today()
    if strategi not in STRATEGI:
        raise InputError("strategi harus salah satu dari: " + ", ".join(STRATEGI))
    if len(baris_mentah) > MAKS_BARIS:
        raise InputError("maksimal {} baris pesaing".format(MAKS_BARIS))

    # ---- produk kita
    if produk.get("hpp") in (None, ""):
        raise InputError("HPP/modal per barang belum diisi. Tanyakan ke pengguna (atau hitung dengan skill hitung-hpp).")
    hpp = parse_rupiah(produk["hpp"], "HPP")
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
    ukuran_kita = parse_ukuran(produk.get("ukuran")) if produk.get("ukuran") else None
    if produk.get("ukuran") and not ukuran_kita:
        raise InputError("ukuran produk kita '{}' tidak dikenali (contoh: 250 gr, 1 kg, 500 ml, 12 pcs)"
                         .format(produk.get("ukuran")))
    harga_kita = parse_rupiah(produk["harga_kita"], "harga kita") if produk.get("harga_kita") not in (None, "") else None

    balik_modal = ((hpp + tetap) / (1 - f)).quantize(Decimal(1), rounding=ROUND_CEILING)
    minimum = ((hpp + tetap) / (1 - f - m)).quantize(Decimal(1), rounding=ROUND_CEILING)

    def laba(p):
        l = p - p * f - hpp - tetap
        return l, (l / p)

    # ---- pesaing
    peringatan, dilewati, duplikat, pesaing = [], [], [], []
    if biaya_persen == 0 and tetap == 0:
        peringatan.append("Biaya marketplace dianggap 0 (jualan langsung). Kalau jualan di Shopee/Tokopedia/TikTok "
                          "Shop, isi persen biaya admin/layanan/PPh 22 agar harga minimum tidak terlalu rendah.")
    terlihat = {}
    for no, mentah in enumerate(baris_mentah, start=1):
        b = normalisasi_baris(mentah)
        label = b.get("toko") or b.get("nama") or "baris {}".format(no)
        if not any(str(v or "").strip() for v in b.values()):
            continue
        k = kunci_duplikat(b)
        if k in terlihat:
            duplikat.append("baris {} ({}) sama dengan baris {}".format(no, label, terlihat[k]))
            continue
        terlihat[k] = no
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
        ukuran, asal_ukuran = None, None
        for fld in ("ukuran", "varian", "nama"):
            if b.get(fld):
                ukuran = parse_ukuran(b[fld])
                if ukuran:
                    asal_ukuran = fld
                    break
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
            "catatan": catatan,
        })

    # ---- penyetaraan ukuran
    ukuran_pesaing = {p["ukuran"] for p in pesaing if p["ukuran"]}
    if ukuran_kita:
        dasar = "harga setara {} (ukuran produk kamu)".format(teks_ukuran(*ukuran_kita))
        for p in pesaing:
            if not p["ukuran"]:
                p["setara"] = None
                p["catatan"].append("ukuran tidak diketahui, tidak ikut dihitung")
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
    urut = sorted(p["setara"] for p in dipakai)
    stat = {"n": len(urut), "terendah": urut[0], "p25": persentil(urut, "0.25"), "median": persentil(urut, "0.5"),
            "p75": persentil(urut, "0.75"), "tertinggi": urut[-1]}
    for p in dipakai:
        if p["setara"] < stat["median"] / 2 or p["setara"] > stat["median"] * 2:
            p["catatan"].append("jauh dari median, cek varian/ukuran/keaslian")
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
                  "laba": l, "margin": mg, "di_bawah_minimum": harga_kita < minimum}

    # ---- rekomendasi
    pilih = {"murah": ("terendah", "p25", "p25"), "tengah": ("p25", "p75", "median"),
             "premium": ("median", "p75", "p75")}[strategi]

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
    rekom = {"strategi": strategi, "rentang_bawah": r_lo, "rentang_atas": r_hi, "titik": r_titik,
             "harga_cantik": cantik, "tanda": tanda}
    rekom["laba_titik"], rekom["margin_titik"] = laba(r_titik)
    if cantik:
        rekom["laba_cantik"], rekom["margin_cantik"] = laba(cantik)

    # ---- promo & bundling
    diskon = [(p["harga_coret"] - p["harga"]) / p["harga_coret"] for p in pesaing if p["harga_coret"]]
    promo = {
        "harga_coret": len(diskon), "rata_diskon": (sum(diskon) / len(diskon)) if diskon else None,
        "promo_ongkir": sum(1 for p in pesaing if re.search(r"ongkir|free\s*ship", p["promo"].lower())),
        "bundling": [p["toko"] or p["nama"] for p in pesaing if p["bundling"]],
        "total": len(pesaing),
    }
    terlaris = max((p for p in dipakai if p["terjual"] is not None), key=lambda p: p["terjual"], default=None)

    return {
        "produk": {"nama": produk.get("nama") or "Produk kamu", "hpp": hpp, "biaya_tetap": tetap,
                   "biaya_persen": biaya_persen, "margin": margin, "margin_default": not margin_diberikan,
                   "ukuran": ukuran_kita, "harga_kita": harga_kita, "balik_modal": balik_modal, "minimum": minimum},
        "dasar": dasar, "pesaing": pesaing, "stat": stat, "posisi": posisi, "rekomendasi": rekom,
        "promo": promo, "terlaris": terlaris, "peringatan": peringatan, "dilewati": dilewati,
        "duplikat": duplikat, "baris_total": len(baris_mentah), "mode_rentang": mode_rentang,
        "tanggal": hari_ini.isoformat(),
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
    o.append("Tanggal analisis: {} | Pesaing dibandingkan: **{}** dari {} baris ({} duplikat dibuang, "
             "{} baris dilewati)".format(h["tanggal"], st["n"], h["baris_total"], len(h["duplikat"]), len(h["dilewati"])))
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
        o.append("- Harga kamu sekarang **{}**: lebih murah dari {} pesaing, sama dengan {}, lebih mahal dari {} "
                 "(posisi sekitar persentil {}). Laba {} per barang (margin {}).".format(
                     rp(ps["harga"]), ps["lebih_murah_dari"], ps["sama_dengan"], ps["lebih_mahal_dari"],
                     fmt_desimal(bulat(ps["persentil"])), rp(ps["laba"]), persen(ps["margin"])))
    if h["terlaris"]:
        t = h["terlaris"]
        o.append("- Pesaing paling laris: {} (sekitar {} terjual) di harga setara {}.".format(
            _sel(t["toko"] or t["nama"]), fmt_desimal(t["terjual"]), rp(t["setara"])))
    o += ["", "### Batas harga kamu", "",
          "| Komponen | Nilai |", "|---|---|",
          "| HPP/modal per barang | {} |".format(rp(pr["hpp"])),
          "| Biaya tetap per barang (mis. biaya proses pesanan) | {} |".format(rp(pr["biaya_tetap"])),
          "| Total biaya marketplace (% dari harga jual) | {}% |".format(fmt_desimal(pr["biaya_persen"])),
          "| Target margin (laba / harga jual) | {}%{} |".format(fmt_desimal(pr["margin"]),
                                                                " (default)" if pr["margin_default"] else ""),
          "| Harga balik modal (laba 0) | {} |".format(rp(pr["balik_modal"])),
          "| **Harga minimum sesuai target margin** | **{}** |".format(rp(pr["minimum"])), ""]
    nama_s = {"murah": "murah (bersaing harga)", "tengah": "tengah pasar", "premium": "premium"}[rk["strategi"]]
    o += ["### Rekomendasi harga (strategi {})".format(nama_s), "",
          "- **Rentang harga: {} - {}**".format(rp(rk["rentang_bawah"]), rp(rk["rentang_atas"])),
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
          "- {} dari {} pesaing memasang harga coret{}.".format(
              pm["harga_coret"], pm["total"],
              " (diskon rata-rata {})".format(persen(pm["rata_diskon"])) if pm["rata_diskon"] is not None else ""),
          "- {} pesaing mencantumkan promo/gratis ongkir.".format(pm["promo_ongkir"])]
    if pm["bundling"]:
        o.append("- Terlihat bundling/paket/bonus: {}.".format(", ".join(_sel(x) for x in pm["bundling"])))
    if h["peringatan"] or h["dilewati"] or h["duplikat"]:
        o += ["", "### Perlu dicek"]
        o += ["- " + x for x in h["peringatan"] + h["dilewati"] + h["duplikat"]]
    o += ["", "### Catatan & asumsi",
          "- Harga pesaing = harga yang tampil saat dicek (setelah diskon toko), belum termasuk ongkir dan voucher "
          "platform; bisa berubah kapan saja.",
          "- Harga rentang memakai harga {}.".format({"min": "terendah", "maks": "tertinggi", "tengah": "nilai tengah"}[h["mode_rentang"]]),
          "- Harga minimum = (HPP + biaya tetap) / (1 - biaya marketplace % - target margin %), dibulatkan ke atas "
          "ke rupiah penuh. Nilai lain dibulatkan ke rupiah terdekat.",
          "- Persentil: interpolasi linear (seperti PERCENTILE.INC di Excel).",
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
    ap.add_argument("--hpp", help="HPP/modal per barang, mis. 38.000")
    ap.add_argument("--ukuran", help="ukuran produk kita, mis. '250 gr', '1 L', '12 pcs'")
    ap.add_argument("--harga-kita", help="harga jual kita sekarang (opsional)")
    ap.add_argument("--margin", help="target margin %% dari harga jual (default 20)")
    ap.add_argument("--biaya-persen", action="append", help="biaya marketplace %% (boleh diulang: admin, layanan, PPh 22, dll.)")
    ap.add_argument("--biaya-tetap", help="biaya tetap per barang dalam Rp (mis. biaya proses pesanan)")
    ap.add_argument("--strategi", default="tengah", choices=STRATEGI)
    ap.add_argument("--rentang", default="min", choices=("min", "tengah", "maks"),
                    help="harga yang dipakai untuk rentang '49.900-59.900' (default min)")
    ap.add_argument("--tanggal", help="tanggal analisis YYYY-MM-DD (default hari ini)")
    ap.add_argument("--format", default="md", choices=("md", "json"))
    a = ap.parse_args(argv)
    try:
        baris, produk = baca_file(a.file)
        produk = dict(produk)
        for kunci, nilai in (("nama", a.nama), ("hpp", a.hpp), ("ukuran", a.ukuran), ("harga_kita", a.harga_kita),
                             ("margin", a.margin), ("biaya_persen", a.biaya_persen), ("biaya_tetap", a.biaya_tetap)):
            if nilai not in (None, "", []):
                produk[kunci] = nilai
        hari = parse_tanggal(a.tanggal) if a.tanggal else date.today()
        if a.tanggal and not hari:
            raise InputError("--tanggal harus YYYY-MM-DD")
        hasil = olah(baris, produk, a.strategi, a.rentang, hari)
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
