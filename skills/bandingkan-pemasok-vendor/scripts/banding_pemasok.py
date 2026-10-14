#!/usr/bin/env python3
"""Bandingkan penawaran pemasok / supplier / vendor untuk UMKM (supplier quotation comparison).

Hanya library standar Python 3.8+. Tidak ada akses jaringan. Hanya membaca --file / --data / stdin;
tidak menulis file apa pun. Windows: jalankan dengan `python` atau `py`.

Rumus (Komunitech):
  qty_beli       = maks(qty_butuh, MOQ efektif), dibulatkan ke atas ke kelipatan kemasan, lalu dinaikkan
                   per kelipatan sampai minimal belanja (Rp) terpenuhi.
  harga berlaku  = harga tingkat tertinggi yang min_qty <= qty_beli, berlaku untuk SEMUA unit (gaya grosir);
                   tingkat berbentuk persen = harga dasar x (1 - persen/100).
  subtotal       = harga berlaku x qty_beli (rupiah terdekat)
  diskon         = subtotal x diskon% (rupiah terdekat) + diskon Rp (maks. sebesar subtotal)
  tagihan        = subtotal - diskon + ongkir yang ditagih pemasok + biaya lain dari pemasok
  PPN (pemasok PKP, barang non-mewah) = 12% x 11/12 x DPP = 11% x DPP, dibulatkan ke bawah sekali
      harga belum termasuk PPN : DPP = tagihan, PPN ditambahkan
      harga termasuk PPN       : DPP = rupiah bulat terbesar dengan DPP + PPN <= tagihan; sisa ditampilkan
  total bayar    = bayar ke pemasok + ongkir yang dibayar ke ekspedisi + biaya yang dikeluarkan sendiri
  biaya pembanding = total bayar - PPN yang bisa dikreditkan (hanya bila pembeli PKP DAN pemasok PKP)
                     [- manfaat tempo + biaya dana DP, hanya bila --bunga-modal diisi]
  biaya per unit = biaya pembanding / qty_butuh
  Skor 0-100 per kriteria (bobot default biaya 40, lead time 20, termin 15, kualitas 15, MOQ 10):
      biaya    = 100 x biaya termurah / biaya pemasok
      lead     = 100 x (hari tercepat + 1) / (hari pemasok + 1); 0 bila melewati tenggat; 50 bila belum diketahui
      termin   = 50 + hari bayar rata-rata x 50/30, dibatasi 0-100 (tunai saat terima = 50, tempo 30 hari = 100)
                 hari bayar rata-rata = -DP% x lead time + (1 - DP%) x tempo
      kualitas = nilai 1-5 x 20 (belum dinilai = 3 -> 60)
      MOQ      = 100 x qty_butuh / qty_beli
  Skor total = jumlah(bobot x skor) / jumlah bobot (bobot dinormalisasi otomatis).
  Peringkat: yang tepat waktu dulu (skor tertinggi), lalu yang melewati tenggat. Rekomendasi = peringkat 1.
  Keluaran teks memuat RINGKASAN SIAP SALIN: kalimat bersubjek "A lebih MURAH/MAHAL RpX daripada B",
  sensitivitas, batas ongkir (ongkir impas) untuk ongkir yang belum diketahui, skenario status PKP, dan
  asumsi pajak yang ditulis terbuka. Kolom ppn: termasuk | belum | non-pkp | bebas | ? (lihat --contoh).
Keluar kode 2 (JSON {"error","saran"} di stderr) bila data tidak bisa dihitung sama sekali.
"""
import argparse
import csv
import io
import json
import re
import sys
from decimal import ROUND_CEILING, ROUND_FLOOR, ROUND_HALF_UP, Decimal, InvalidOperation, getcontext

getcontext().prec = 40
VERSI = "1.0.1"
TARIF_PPN = Decimal(11) / Decimal(100)  # 12% x 11/12 (DPP nilai lain, barang non-mewah)
LABEL_AGENT = ("[UNTUK AGENT SAJA - jangan disalin apa adanya; sampaikan dengan bahasa awam, "
               "tanpa menyebut script/file/proses]")
DISCLAIMER = ("Perbandingan ini alat bantu keputusan pembelian, bukan nasihat pajak atau hukum. Angka hanya "
              "dari penawaran yang diberikan; pastikan harga, PPN, dan syarat tertulis di penawaran resmi/faktur.")
CATATAN_PPN = ("PPN pemasok PKP dihitung 12% x 11/12 x DPP (efektif 11%, barang non-mewah, PMK 131/2024), "
               "dibulatkan ke bawah sekali; belum dicocokkan dengan Coretax.")
KRITERIA = ["biaya", "lead_time", "termin", "kualitas", "moq"]
# Barang kebutuhan pokok yang umumnya dibebaskan PPN (PP 49/2022) - PERLU REVIEW konsultan pajak.
BAHAN_POKOK = (r"\b(beras|gabah|jagung|sagu|kedelai|garam|daging|telur|susu segar|susu murni|buah|sayur|sayuran|"
               r"ubi|singkong|talas|bumbu|cabai|cabe|bawang|gula pasir|gula konsumsi|gula kristal|gula)\b")
NAMA_KRITERIA = {"biaya": "biaya", "lead_time": "lead time", "termin": "termin", "kualitas": "kualitas",
                 "moq": "MOQ"}
BOBOT_DEFAULT = {"biaya": Decimal(40), "lead_time": Decimal(20), "termin": Decimal(15),
                 "kualitas": Decimal(15), "moq": Decimal(10)}
KOSONG = {"", "-", "—", "n/a", "na", "?", "belum", "belum tahu", "tidak tahu", "tdk tahu", "null", "none",
          "tbd", "belum ada", "x"}


class Galat(Exception):
    def __init__(self, pesan, saran=""):
        super().__init__(pesan)
        self.pesan, self.saran = pesan, saran


# ------------------------------------------------------------------ parsing angka & teks
PENGALI = {"rb": 10**3, "ribu": 10**3, "k": 10**3, "jt": 10**6, "juta": 10**6,
           "m": 10**9, "miliar": 10**9, "milyar": 10**9}
SATUAN = (r"(?:pcs|pc|unit|buah|bh|kg|gr|gram|ons|liter|ltr|ml|dus|box|pak|pack|lusin|kodi|rim|roll|"
          r"lembar|lbr|meter|mtr|botol|sak|karung|set|pasang|psg|porsi|cup|bks|bungkus|ikat|ekor|"
          r"kemasan|karton|ctn|item|biji|kaleng|tabung|galon)")


def kosong(teks):
    return teks is None or (isinstance(teks, str) and teks.strip().lower() in KOSONG)


def parse_angka(teks, nama, boleh_kosong=True):
    """'Rp 12.500/pcs' | '11,5rb' | '1,2 jt' | '45,000' | 12500 -> Decimal, atau None bila kosong."""
    if isinstance(teks, bool):
        raise Galat(f"{nama}: nilai '{teks}' bukan angka", "Tulis angka, mis. 12.500 atau 11,5rb.")
    if isinstance(teks, int):
        return Decimal(teks)
    if isinstance(teks, float):
        return Decimal(str(teks))
    if isinstance(teks, Decimal):
        return teks
    if kosong(teks):
        if boleh_kosong:
            return None
        raise Galat(f"{nama}: kosong", "Isi angkanya, mis. 12.500 atau 11,5rb.")
    asli = str(teks)
    s = asli.strip().lower().replace(" ", " ")
    s = re.sub(r"^\s*(rp|idr)\.?\s*", "", s)
    s = re.sub(r"\s*(/|per)\s*" + SATUAN + r"\.?\s*$", "", s)
    s = re.sub(r"\s+" + SATUAN + r"\.?\s*$", "", s)
    s = re.sub(r"[,.]-+$", "", s).strip()
    negatif = False
    if s.startswith("(") and s.endswith(")"):
        negatif, s = True, s[1:-1].strip()
    if s.startswith("-"):
        negatif, s = True, s[1:].strip()
    s = re.sub(r"^\s*(rp|idr)\.?\s*", "", s).replace(" ", "")
    m = re.fullmatch(r"([0-9][0-9.,]*)(rb|ribu|k|jt|juta|m|miliar|milyar)?", s)
    if not m:
        raise Galat(f"{nama}: angka '{asli}' tidak terbaca", "Tulis seperti 12500, 12.500, 11,5rb, atau 1,2jt.")
    num, suf = m.group(1).strip(".,"), m.group(2)
    if "," in num and "." in num:
        num = num.replace(".", "").replace(",", ".") if num.rfind(",") > num.rfind(".") else num.replace(",", "")
    elif "," in num:
        b = num.split(",")
        if len(b) > 2 or (len(b[1]) == 3 and not suf):
            num = num.replace(",", "")  # 45,000 gaya Excel Inggris = ribuan
        else:
            num = num.replace(",", ".")
    elif "." in num:
        b = num.split(".")
        if len(b) > 2 or len(b[1]) == 3:
            num = num.replace(".", "")
    try:
        v = Decimal(num) * Decimal(PENGALI[suf] if suf else 1)
    except InvalidOperation:
        raise Galat(f"{nama}: angka '{asli}' tidak terbaca", "Contoh: 12.500")
    return -v if negatif else v


HITUNGAN_BAKU = {"lusin": 12, "kodi": 20, "gross": 144, "gros": 144}
KEMASAN = r"(dus|box|karton|ctn|pak|pack|kemasan|bal|rim|sak|karung|ikat|bungkus|bks)"


def parse_qty(teks, nama, satuan_butuh, ada_isi, catatan):
    """Jumlah (MOQ/kelipatan). '2 lusin' -> 24; '5 dus' tanpa isi per dus -> Galat (tidak ditebak)."""
    if kosong(teks) or not isinstance(teks, str):
        return parse_angka(teks, nama)
    s = teks.strip().lower()
    m = re.search(r"([a-z]+)\.?\s*$", s)
    unit = m.group(1) if m else ""
    sb = (satuan_butuh or "").strip().lower()
    v = parse_angka(re.sub(r"\s*(lusin|kodi|gross|gros)\.?\s*$", "", s), nama)
    if unit in HITUNGAN_BAKU and unit != sb and v is not None:
        catatan.append(f"{nama} '{teks}' dibaca {fmt_q(v * HITUNGAN_BAKU[unit])} (1 {unit} = {HITUNGAN_BAKU[unit]})")
        return v * HITUNGAN_BAKU[unit]
    if re.fullmatch(KEMASAN, unit) and unit != sb and not ada_isi:
        raise Galat(f"{nama} '{teks}' memakai satuan {unit}, isi per {unit} belum diketahui",
                    f"Isi isi_kemasan (jumlah {sb or 'unit'} per {unit}) atau tulis dalam {sb or 'unit kebutuhan'}.")
    return v


TIDAK_TAHU = {"belum tahu", "blm tahu", "belum jelas", "belum pasti", "tidak tahu", "tdk tahu", "?", "",
              "-", "n/a", "null", "none", "tbd"}


def parse_ppn_status(teks):
    """Kolom 'ppn' (kamus tetap) -> (pkp, harga_termasuk_ppn, bebas_ppn).

    termasuk / sudah / incl      -> pemasok PKP, harga SUDAH termasuk PPN
    belum / blm / excl / +ppn    -> pemasok PKP, harga BELUM termasuk PPN (ditambah 11%)
    non-pkp / tanpa ppn / tidak  -> bukan PKP, tanpa PPN
    bebas                         -> barang dibebaskan PPN (tanpa PPN)
    pkp / ya                      -> PKP, sudah/belum termasuk belum jelas (dianggap belum + [isian])
    ? / kosong / belum tahu       -> belum jelas -> [isian]
    """
    if isinstance(teks, bool):
        return (True, None, False) if teks else (False, None, False)
    if teks is None:
        return None, None, False
    s = str(teks).strip().lower()
    if s in TIDAK_TAHU:
        return None, None, False
    if "bebas" in s:
        return None, None, True
    if re.search(r"\bnon\b|bukan pkp|(belum|blm|tidak|tdk) pkp|tanpa ppn|(tidak|tdk|ga|gak|nggak) ada ppn|"
                 r"\bno ppn\b|^(tidak|tdk|t|n|no|non)$", s):
        return False, None, False
    if re.search(r"\b(belum|blm|excl|exclude|ex)\b|\+\s*ppn|plus ppn", s):
        return True, False, False
    if re.search(r"termasuk|sudah|\bincl|include|\binc\b", s):
        return True, True, False
    if re.search(r"\bpkp\b|^(ya|y|iya)$", s):
        return True, None, False
    raise Galat(f"kolom PPN '{teks}' tidak dikenali",
                "Isi salah satu: termasuk, belum, non-pkp, bebas, atau ? (belum jelas).")


def parse_ya(teks):
    """ya/tidak/tidak diketahui -> True/False/None. 'non-PKP', 'belum termasuk' -> False."""
    if isinstance(teks, bool):
        return teks
    if teks is None:
        return None
    s = str(teks).strip().lower()
    if s in TIDAK_TAHU:
        return None
    if re.search(r"\b(belum|blm)\b", s):
        return False  # 'belum' = belum termasuk / belum PKP, BUKAN data kosong
    if s in KOSONG:
        return None
    if s in ("0", "n", "t") or re.search(
            r"\b(non|bukan|tidak|tdk|tak|no|false|exclude|excl|ex|ga|gak|nggak|tanpa)\b", s):
        return False
    if s in ("1", "y") or re.search(r"\b(ya|iya|yes|true|sudah|termasuk|include|incl|inc|pkp)\b", s):
        return True
    return None


def parse_ongkir(teks):
    """-> (Decimal|None, jenis) ; jenis 'franco' (ditanggung pemasok), 'loco' (ambil sendiri) atau None."""
    if teks is None or isinstance(teks, (int, float, Decimal)) and not isinstance(teks, bool):
        return (None if teks is None else Decimal(str(teks))), None
    s = str(teks).strip().lower()
    if s in KOSONG:
        return None, None
    if re.search(r"gratis|free|franco|frangko|ditanggung (pemasok|penjual|supplier|toko)|termasuk ongkir", s):
        return Decimal(0), "franco"
    if re.search(r"loco|ambil sendiri|ambil di|diambil|pick ?up", s):
        return Decimal(0), "loco"
    if re.search(r"(/|\bper)\s*(" + SATUAN[3:-1] + r"|lusin|kodi|bal)\.?\s*$", s):
        return parse_angka(re.sub(r"\s*(/|\bper)\s*(lusin|kodi|bal)\.?\s*$", "", s), "ongkir"), "per_unit"
    return parse_angka(teks, "ongkir"), None


def parse_lead(teks):
    """'5' | '3-5 hari' (ambil 5) | '2 minggu' (14) -> (Decimal|None, catatan|None)."""
    if teks is None:
        return None, None
    if isinstance(teks, (int, float, Decimal)) and not isinstance(teks, bool):
        return Decimal(str(teks)), None
    s = str(teks).strip().lower()
    if s in KOSONG:
        return None, None
    kali = 7 if re.search(r"minggu|pekan|week", s) else (30 if re.search(r"bulan|month", s) else 1)
    angka = re.findall(r"\d+(?:[.,]\d+)?", s)
    if not angka:
        if re.search(r"hari ini|same ?day", s):
            return Decimal(0), None
        if re.search(r"besok", s):
            return Decimal(1), None
        return None, f"lead time '{teks}' tidak berupa jumlah hari"
    nilai = max(Decimal(a.replace(",", ".")) for a in angka) * kali
    cat = f"lead time '{teks}' dibaca {fmt_q(nilai)} hari (angka terlama)" if len(angka) > 1 else None
    if kali == 1 and re.search(r"hari kerja|working day|business day", s):
        nilai = (nilai * 7 / 5).to_integral_value(rounding=ROUND_CEILING)
        cat = f"lead time '{teks}' (hari kerja) dibaca {fmt_q(nilai)} hari kalender"
    return nilai, cat


def parse_termin(teks):
    """Teks termin -> (dp_persen, tempo_hari) atau None bila tidak terbaca."""
    if kosong(teks):
        return None
    s = str(teks).strip().lower()
    dp = tempo = None
    if re.search(r"\bcod\b|bayar di tempat|cash on delivery|tunai saat|bayar (saat|waktu|ketika) (barang )?"
                 r"(datang|tiba|terima|diterima|sampai)|\bcash\b|\btunai\b", s):
        dp, tempo = Decimal(0), Decimal(0)
    if re.search(r"(lunas|bayar|transfer|full|100\s*%)\s*(di ?muka|dulu|di ?depan|sebelum)|\bcbd\b|"
                 r"cash before", s):
        dp, tempo = Decimal(100), Decimal(0)
    m = re.search(r"(dp|uang muka|down ?payment)\s*:?\s*(\d+(?:[.,]\d+)?)\s*%", s)
    if m:
        dp = Decimal(m.group(2).replace(",", "."))
        tempo = tempo if tempo is not None else Decimal(0)
    m = (re.search(r"(tempo|\btop\b|\bnet\b|jatuh tempo|kredit)\s*:?\s*(\d+)\s*(hari|hr|h\b|minggu|pekan|bulan)?", s)
         or re.search(r"()(\d+)\s*(hari|hr|minggu|pekan|bulan)\s*(setelah|sesudah|dari|sejak)", s)
         or re.search(r"()\bh\s*\+\s*(\d+)()", s))
    if m:
        kali = {"minggu": 7, "pekan": 7, "bulan": 30}.get(m.group(3) or "", 1)
        tempo = Decimal(m.group(2)) * kali
        dp = dp if dp is not None else Decimal(0)
    if dp is None and tempo is None:
        return None
    return dp, tempo


def parse_tingkat(nilai, nama):
    """Harga bertingkat -> list (min_qty, nilai, 'harga'|'persen') urut min_qty.

    Teks: '100:11.500; 500:10.800' | '1-99=12rb | 100-499=11rb | 500+=10rb' | '>=200: 5%'.
    JSON: [{"min": 100, "harga": 11500}, {"min": 500, "diskon_persen": 5}] atau [[100, 11500], ...].
    """
    if kosong(nilai):
        return []
    hasil = {}
    if isinstance(nilai, list):
        for it in nilai:
            if isinstance(it, dict):
                k = {norm(a): b for a, b in it.items()}
                mn = parse_angka(k.get("min", k.get("min qty", k.get("qty", k.get("dari")))), f"{nama} tingkat")
                if "diskon persen" in k or "persen" in k:
                    v = parse_angka(str(k.get("diskon persen", k.get("persen"))).replace("%", ""), f"{nama} tingkat")
                    jenis = "persen"
                else:
                    v = parse_angka(k.get("harga", k.get("harga satuan")), f"{nama} tingkat")
                    jenis = "harga"
            elif isinstance(it, (list, tuple)) and len(it) == 2:
                mn = parse_angka(it[0], f"{nama} tingkat")
                teks_v = str(it[1])
                jenis = "persen" if "%" in teks_v else "harga"
                v = parse_angka(teks_v.replace("%", "").replace("diskon", "").strip(), f"{nama} tingkat")
            else:
                raise Galat(f"{nama}: format tingkat harga tidak dikenali", "Contoh: [{\"min\": 100, \"harga\": 11500}]")
            if mn is None or v is None:
                raise Galat(f"{nama}: tingkat harga tidak lengkap", "Tiap tingkat butuh jumlah minimal dan harga.")
            hasil[mn] = (mn, v, jenis)
    else:
        for seg in re.split(r"\s*[;|\n]\s*|\s+/\s+", str(nilai)):
            seg = seg.strip().strip(",")
            if not seg:
                continue
            if re.match(r"^\s*(<|di ?bawah|kurang dari)", seg, re.I):
                v_teks = re.split(r"[:=@]|->|→", seg, maxsplit=1)
                if len(v_teks) < 2:
                    raise Galat(f"{nama}: tingkat '{seg}' tidak terbaca", "Contoh: 1-99: 12.000; 100+: 11.000")
                mn, v_raw = Decimal(1), v_teks[1].strip()
            else:
                m = re.match(r"^\s*(?:>=|≥|>|min(?:imal|imum)?\.?|mulai|di\s*atas|beli|order|qty)?\s*"
                             r"(\d[\d.,]*)\s*(?:(?:-|–|s/?d|sampai)\s*\d[\d.,]*)?\s*(?:" + SATUAN + r")?\s*"
                             r"(?:\+|ke\s*atas|keatas|lebih)?\s*(?:[:=@]|->|→)?\s*(.+?)\s*$", seg, re.I)
                if not m:
                    raise Galat(f"{nama}: tingkat '{seg}' tidak terbaca", "Contoh: 1-99: 12.000; 100+: 11.000")
                mn, v_raw = parse_angka(m.group(1), f"{nama} tingkat"), m.group(2)
            if "%" in v_raw:
                jenis = "persen"
                v = parse_angka(re.sub(r"diskon|disc|potongan|%", "", v_raw, flags=re.I).strip(), f"{nama} tingkat")
            else:
                jenis = "harga"
                v = parse_angka(v_raw, f"{nama} tingkat")
            if v is None:
                raise Galat(f"{nama}: tingkat '{seg}' tanpa harga", "Contoh: 100: 11.500")
            hasil[mn] = (mn, v, jenis)
    out = sorted(hasil.values(), key=lambda t: t[0])
    for mn, v, jenis in out:
        if mn <= 0 or v < 0 or (jenis == "persen" and v >= 100):
            raise Galat(f"{nama}: tingkat harga tidak wajar ({fmt_q(mn)} -> {v})",
                        "Jumlah minimal > 0, harga >= 0, diskon persen < 100.")
    return out


def bulat(x):
    return Decimal(x).quantize(Decimal(1), rounding=ROUND_HALF_UP)


def satu_desimal(x):
    return Decimal(x).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)


def rp(n):
    n = bulat(n)
    return ("-" if n < 0 else "") + "Rp" + f"{int(abs(n)):,}".replace(",", ".")


def rp_unit(x):
    """Per unit: rupiah terdekat; di bawah Rp1.000 tampil 2 desimal."""
    x = Decimal(x)
    if abs(x) < 1000:
        q = x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        if q != q.to_integral_value():
            return "Rp" + f"{q:.2f}".replace(".", ",")
    return rp(x)


def fmt_q(x):
    x = Decimal(x)
    if x == x.to_integral_value():
        return f"{int(x):,}".replace(",", ".")
    return f"{x.normalize():f}".replace(".", ",")


def fmt_d(x):
    return f"{satu_desimal(x):f}".replace(".", ",")


def jnum(x):
    if x is None:
        return None
    x = Decimal(x)
    return int(x) if x == x.to_integral_value() else float(x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


# ------------------------------------------------------------------ kolom & input
KOLOM = {
    "nama": ["nama", "pemasok", "supplier", "vendor", "toko", "nama pemasok", "nama supplier", "penjual"],
    "harga_satuan": ["harga satuan", "harga", "harga unit", "unit price", "price", "harga dasar", "harga per unit",
                     "harga ecer"],
    "tingkat_harga": ["tingkat harga", "harga bertingkat", "harga grosir", "tier", "tingkat", "diskon bertingkat",
                      "grosir", "harga tingkat"],
    "diskon_persen": ["diskon persen", "diskon %", "diskon", "discount", "disc", "potongan persen"],
    "diskon_rp": ["diskon rp", "potongan", "potongan rp", "diskon nominal"],
    "moq": ["moq", "min order", "minimal order", "minimum order", "min beli", "minimal beli", "min qty",
            "minimal pembelian", "minimum pembelian"],
    "kelipatan": ["kelipatan", "kelipatan order", "kelipatan beli"],
    "isi_kemasan": ["isi kemasan", "isi per dus", "isi dus", "isi per kemasan", "isi"],
    "min_belanja": ["min belanja", "minimal belanja", "minimum belanja", "min order rp", "minimal order rp",
                    "min transaksi"],
    "ongkir": ["ongkir", "ongkos kirim", "biaya kirim", "shipping", "ongkir rp", "biaya pengiriman"],
    "ongkir_per_unit": ["ongkir per unit", "ongkir unit", "ongkir per dus", "ongkir per pcs"],
    "ongkir_ditagih_pemasok": ["ongkir ditagih pemasok", "ongkir lewat pemasok", "ongkir via pemasok"],
    "ppn": ["ppn", "status ppn", "pkp ppn", "pajak", "status pajak", "ppn?"],
    "pkp": ["pkp", "status pkp", "pemasok pkp", "kena ppn", "pkp?"],
    "harga_termasuk_ppn": ["harga termasuk ppn", "termasuk ppn", "incl ppn", "sudah ppn", "include ppn",
                           "harga sudah termasuk ppn", "ppn termasuk"],
    "biaya_lain": ["biaya lain", "biaya lain lain", "biaya tambahan", "packing", "biaya packing",
                   "biaya lain pemasok"],
    "biaya_luar": ["biaya luar", "biaya sendiri", "biaya ambil", "biaya bongkar", "biaya lain sendiri"],
    "lead_time_hari": ["lead time hari", "lead time", "leadtime", "waktu kirim", "estimasi kirim", "lama kirim",
                       "waktu produksi", "estimasi", "lama", "lead"],
    "dp_persen": ["dp persen", "dp", "dp %", "uang muka", "uang muka persen"],
    "tempo_hari": ["tempo hari", "tempo", "top", "jatuh tempo", "term of payment"],
    "termin": ["termin", "termin bayar", "pembayaran", "cara bayar", "payment terms", "syarat bayar"],
    "nilai_kualitas": ["nilai kualitas", "kualitas", "rating", "rekam jejak", "skor kualitas", "mutu"],
    "garansi": ["garansi", "retur", "garansi retur", "garansi/retur", "kebijakan retur"],
    "catatan": ["catatan", "keterangan", "note", "notes", "ket"],
}


def norm(h):
    return re.sub(r"\s+", " ", re.sub(r"[_\-/().:?%]+", " ", str(h).strip().lower())).strip()


ALIAS = {}
for _k, _al in KOLOM.items():
    ALIAS[norm(_k)] = _k
    for _a in _al:
        ALIAS.setdefault(norm(_a), _k)


def kanonik(rec):
    out, tak = {}, []
    for k, v in rec.items():
        if k is None:
            continue
        kk = ALIAS.get(norm(k))
        if kk is None:
            tak.append(str(k))
            continue
        if kk not in out or kosong(out[kk]):
            out[kk] = v
    return out, tak


def baca_tabel(teks):
    baris = [b for b in teks.replace("\r\n", "\n").split("\n") if b.strip()]
    if not baris:
        raise Galat("data kosong", "Tempel penawaran pemasok (minimal nama dan harga).")
    if sum(1 for b in baris if b.strip().startswith("|")) >= 2:
        rows = []
        for b in baris:
            b = b.strip()
            if not b.startswith("|"):
                continue
            sel = [c.strip() for c in b.strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in sel if c):
                continue
            rows.append(sel)
    else:
        kepala = baris[0]
        delim = "\t" if "\t" in kepala else (";" if ";" in kepala else ("|" if "|" in kepala else ","))
        rows = list(csv.reader(io.StringIO("\n".join(baris)), delimiter=delim))
    if len(rows) < 2:
        raise Galat("tabel hanya berisi judul kolom", "Tambahkan minimal satu baris pemasok di bawah judul.")
    head = rows[0]
    hasil = []
    for r in rows[1:]:
        if not any(c.strip() for c in r):
            continue
        hasil.append({head[i]: (r[i] if i < len(r) else "") for i in range(len(head))})
    return hasil


def muat_input(teks):
    s = teks.strip().lstrip("﻿")
    if not s:
        raise Galat("data kosong", "Tempel penawaran pemasok atau beri file JSON/CSV.")
    if s[0] in "[{":
        try:
            data = json.loads(s)
        except ValueError as e:
            raise Galat(f"JSON tidak terbaca: {e}", "Periksa tanda kurung/koma, atau kirim sebagai CSV.")
        if isinstance(data, list):
            return {}, data
        if not isinstance(data, dict):
            raise Galat("JSON harus objek atau daftar", "Contoh: {\"kebutuhan\": {...}, \"pemasok\": [...]}")
        pem = None
        for k in ("pemasok", "supplier", "vendor", "penawaran"):
            if k in data:
                pem = data[k]
                break
        if not isinstance(pem, list):
            raise Galat("daftar pemasok tidak ditemukan", "Isi kunci \"pemasok\" berupa daftar penawaran.")
        keb = data.get("kebutuhan") or {}
        if not isinstance(keb, dict):
            raise Galat("'kebutuhan' harus objek", "Contoh: {\"qty\": 300, \"butuh_dalam_hari\": 14}")
        return keb, pem
    return {}, baca_tabel(s)


# ------------------------------------------------------------------ siapkan pemasok
def siapkan_pemasok(rec, no, satuan_butuh=""):
    """Rekaman mentah -> dict pemasok tervalidasi (raise Galat bila harus dilewati)."""
    if not isinstance(rec, dict):
        raise Galat(f"pemasok ke-{no} bukan objek", "Tiap pemasok berupa {\"nama\": ..., \"harga_satuan\": ...}")
    r, tak = kanonik(rec)
    nama = str(r.get("nama") or "").strip() or f"Pemasok {no}"
    p = {"nama": nama, "kolom_tak_dikenal": tak, "catatan_input": [], "isian": []}

    def angka(k, label, boleh_negatif=False):
        v = parse_angka(r.get(k), f"{nama} {label}")
        if v is not None and v < 0 and not boleh_negatif:
            raise Galat(f"{nama}: {label} negatif ({v})", f"Isi {label} dengan angka 0 atau lebih.")
        return v

    harga = angka("harga_satuan", "harga satuan")
    tingkat = parse_tingkat(r.get("tingkat_harga"), nama)
    if harga is None and not tingkat:
        raise Galat(f"{nama}: harga kosong atau tidak terbaca", "Isi harga satuan atau harga bertingkat.")
    if harga is not None and harga <= 0:
        raise Galat(f"{nama}: harga satuan harus lebih dari 0", "Periksa harga di penawaran.")
    if harga is None and any(t[2] == "persen" for t in tingkat):
        raise Galat(f"{nama}: diskon bertingkat persen butuh harga dasar", "Isi harga satuan dasar.")
    isi = angka("isi_kemasan", "isi kemasan")
    if isi is not None and isi <= 0:
        raise Galat(f"{nama}: isi kemasan harus lebih dari 0", "Mis. 24 (pcs per dus).")
    moq = parse_qty(r.get("moq"), "MOQ", satuan_butuh, bool(isi), p["catatan_input"])
    kel = parse_qty(r.get("kelipatan"), "kelipatan", satuan_butuh, bool(isi), p["catatan_input"])
    for v_, lab in ((moq, "MOQ"), (kel, "kelipatan")):
        if v_ is not None and v_ < 0:
            raise Galat(f"{nama}: {lab} negatif", f"Isi {lab} 0 atau lebih.")
    ong_unit = angka("ongkir_per_unit", "ongkir per unit")
    ongkir, jenis_ongkir = parse_ongkir(r.get("ongkir"))
    if jenis_ongkir == "per_unit":
        # '15rb/dus' di kolom ongkir = ongkir per kemasan/unit, bukan sekali kirim
        teks_ong = str(r.get("ongkir")).lower()
        m_unit = re.search(r"(?:/|\bper)\s*([a-z]+)\.?\s*$", teks_ong)
        unit_ong = m_unit.group(1) if m_unit else ""
        per_kemasan = (re.fullmatch(KEMASAN + r"|lusin|kodi", unit_ong) is not None
                       and unit_ong != (satuan_butuh or "").strip().lower())
        if per_kemasan and not isi:
            raise Galat(f"{nama}: ongkir '{r.get('ongkir')}' per {unit_ong}, isi per {unit_ong} belum diketahui",
                        "Isi isi_kemasan atau tulis ongkir total untuk pesanan ini.")
        ong_unit = (ong_unit or Decimal(0)) + (ongkir / isi if (isi and per_kemasan) else ongkir) * (isi or 1)
        ongkir, jenis_ongkir = None, None
        p["catatan_input"].append(f"ongkir '{r.get('ongkir')}' dibaca per {'kemasan' if per_kemasan else 'unit'}")
    if isi:
        # Semua jumlah & harga pemasok ini dibaca per kemasan -> ubah ke unit kebutuhan.
        harga = harga / isi if harga is not None else None
        tingkat = [(mn * isi, (v / isi if j == "harga" else v), j) for mn, v, j in tingkat]
        moq = moq * isi if moq is not None else None
        kel = (kel or 1) * isi
        ong_unit = ong_unit / isi if ong_unit is not None else None
        p["catatan_input"].append(f"harga per kemasan isi {fmt_q(isi)}; dihitung per unit")
    if kel is not None and kel <= 0:
        kel = None
    if ongkir is not None and ongkir < 0:
        raise Galat(f"{nama}: ongkir negatif", "Isi ongkir 0 atau lebih.")
    lead, cat_lead = parse_lead(r.get("lead_time_hari"))
    if lead is not None and lead < 0:
        raise Galat(f"{nama}: lead time negatif", "Isi jumlah hari 0 atau lebih.")
    if cat_lead:
        p["catatan_input"].append(cat_lead)
    dp = angka("dp_persen", "DP")
    tempo = angka("tempo_hari", "tempo")
    termin_teks = r.get("termin")
    if dp is None and tempo is None and not kosong(termin_teks):
        t = parse_termin(termin_teks)
        if t is None:
            p["catatan_input"].append(f"termin '{termin_teks}' tidak terbaca; dianggap tunai saat barang diterima")
        else:
            dp, tempo = t
    termin_diketahui = dp is not None or tempo is not None
    if dp is not None and dp > 100:
        raise Galat(f"{nama}: DP lebih dari 100%", "Isi DP 0-100.")
    disk_rp = angka("diskon_rp", "diskon Rp")
    disk_pct, d_raw = None, r.get("diskon_persen")
    if not kosong(d_raw):
        d_teks = str(d_raw)
        nilai_d = parse_angka(d_teks.replace("%", "").strip(), f"{nama} diskon")
        if nilai_d is not None and nilai_d < 0:
            raise Galat(f"{nama}: diskon negatif", "Isi diskon 0 atau lebih.")
        if "%" not in d_teks and (re.search(r"rp|rb|ribu|jt|juta", d_teks, re.I) or (nilai_d or 0) >= 100):
            disk_rp = (disk_rp or Decimal(0)) + nilai_d  # kolom 'diskon' berisi rupiah, bukan persen
            p["catatan_input"].append(f"diskon '{d_teks}' dibaca sebagai potongan rupiah")
        else:
            disk_pct = nilai_d
    kual = parse_angka(r.get("nilai_kualitas"), f"{nama} kualitas") if not kosong(r.get("nilai_kualitas")) else None
    if kual is not None and not (1 <= kual <= 5):
        p["catatan_input"].append(f"nilai kualitas {kual} di luar 1-5; diabaikan (dianggap 3)")
        kual = None
    p.update({
        "harga_dasar": harga, "tingkat": tingkat, "isi_kemasan": isi, "moq": moq, "kelipatan": kel,
        "min_belanja": angka("min_belanja", "minimal belanja"),
        "diskon_persen": disk_pct, "diskon_rp": disk_rp,
        "ongkir": ongkir, "jenis_ongkir": jenis_ongkir, "ongkir_per_unit": ong_unit,
        "ongkir_ditagih_pemasok": parse_ya(r.get("ongkir_ditagih_pemasok")),
        "pkp": parse_ya(r.get("pkp")), "termasuk_ppn": parse_ya(r.get("harga_termasuk_ppn")), "bebas_ppn": False,
        "biaya_lain": angka("biaya_lain", "biaya lain"), "biaya_luar": angka("biaya_luar", "biaya sendiri"),
        "lead": lead, "dp": dp if dp is not None else Decimal(0), "tempo": tempo if tempo is not None else Decimal(0),
        "termin_diketahui": termin_diketahui, "kualitas": kual,
        "garansi": None if kosong(r.get("garansi")) else str(r.get("garansi")).strip(),
        "catatan": None if kosong(r.get("catatan")) else str(r.get("catatan")).strip(),
    })
    if p["diskon_persen"] is not None and not (0 <= p["diskon_persen"] < 100):
        raise Galat(f"{nama}: diskon persen harus 0-99", "Mis. 5 untuk diskon 5%.")
    if p["ongkir_ditagih_pemasok"] is None:
        p["ongkir_ditagih_pemasok"] = True
    if p["tempo"] < 0:
        raise Galat(f"{nama}: tempo negatif", "Isi jumlah hari 0 atau lebih.")
    if r.get("ppn") is not None:
        try:
            pkp_k, ter_k, bebas_k = parse_ppn_status(r.get("ppn"))
        except Galat as e:
            raise Galat(f"{nama}: {e.pesan}", e.saran)
        if p["pkp"] is None:
            p["pkp"] = pkp_k
        if p["termasuk_ppn"] is None:
            p["termasuk_ppn"] = ter_k
        p["bebas_ppn"] = bebas_k
    # Status PPN: 'termasuk/belum termasuk PPN' tanpa status PKP -> dianggap PKP.
    if p["pkp"] is None and p["termasuk_ppn"] is not None and not p["bebas_ppn"]:
        p["pkp"] = True
        p["catatan_input"].append("menyebut PPN tanpa status PKP; dianggap pemasok PKP")
    return p


# ------------------------------------------------------------------ hitung satu pemasok
def ppn_dari_dpp(dpp):
    return (Decimal(dpp) * TARIF_PPN).to_integral_value(rounding=ROUND_FLOOR)


def pisah_termasuk_ppn(gross):
    """DPP = rupiah bulat terbesar dengan DPP + PPN(DPP) <= gross."""
    gross = Decimal(gross)
    d = (gross / (1 + TARIF_PPN)).to_integral_value(rounding=ROUND_FLOOR) + 2
    while d > 0 and d + ppn_dari_dpp(d) > gross:
        d -= 1
    d = max(d, Decimal(0))
    ppn = ppn_dari_dpp(d)
    return d, ppn, gross - d - ppn


def harga_pada(p, q):
    pilih = None
    for t in p["tingkat"]:
        if q >= t[0]:
            pilih = t
    if pilih is None:
        return p["harga_dasar"], None
    mn, v, jenis = pilih
    if jenis == "persen":
        return p["harga_dasar"] * (1 - v / 100), mn
    return v, mn


def barang_bersih(p, q):
    harga, tmin = harga_pada(p, q)
    subtotal = bulat(harga * q)
    diskon = (bulat(subtotal * (p["diskon_persen"] or 0) / 100) if p["diskon_persen"] else Decimal(0))
    diskon += bulat(p["diskon_rp"] or 0)
    diskon = min(diskon, subtotal)
    return harga, tmin, subtotal, diskon


def naik_kelipatan(q, kel):
    if kel:
        return (Decimal(q) / kel).to_integral_value(rounding=ROUND_CEILING) * kel
    return Decimal(q)


def hitung(p, qty, ctx, paksa_qty=None):
    """Biaya mendarat satu pemasok untuk qty_butuh. paksa_qty: hitung tepat pada jumlah beli itu."""
    moq_eff = p["moq"] or Decimal(0)
    if p["harga_dasar"] is None and p["tingkat"]:
        moq_eff = max(moq_eff, p["tingkat"][0][0])
    if paksa_qty is not None:
        q = Decimal(paksa_qty)
    else:
        q = naik_kelipatan(max(Decimal(qty), moq_eff), p["kelipatan"])
        if p["min_belanja"]:
            langkah = p["kelipatan"] or Decimal(1)
            for _ in range(200000):
                _, _, sub, dis = barang_bersih(p, q)
                if sub - dis >= p["min_belanja"]:
                    break
                q += langkah
            else:
                raise Galat(f"{p['nama']}: minimal belanja tidak tercapai", "Periksa angka minimal belanja.")
    harga, tmin, subtotal, diskon = barang_bersih(p, q)
    ong_tetap = bulat(p["ongkir"] or 0)
    ong_total = ong_tetap + bulat((p["ongkir_per_unit"] or 0) * q)
    ong_pemasok = ong_total if p["ongkir_ditagih_pemasok"] else Decimal(0)
    ong_luar = ong_total - ong_pemasok
    biaya_lain = bulat(p["biaya_lain"] or 0)
    tagihan = subtotal - diskon + ong_pemasok + biaya_lain
    dpp, ppn, sisa, potensi_ppn, ppn_ongkir = None, Decimal(0), Decimal(0), None, Decimal(0)
    bebas = bool(ctx.get("bebas_ppn") or p.get("bebas_ppn"))
    if bebas:
        bayar_pemasok = tagihan
    elif p["pkp"] is True:
        if p["termasuk_ppn"] is True:
            dpp, ppn, sisa = pisah_termasuk_ppn(tagihan)
            bayar_pemasok = tagihan
        else:
            dpp, ppn = tagihan, ppn_dari_dpp(tagihan)
            bayar_pemasok = tagihan + ppn
            ppn_ongkir = ppn - ppn_dari_dpp(tagihan - ong_pemasok)
    else:
        bayar_pemasok = tagihan
        if p["pkp"] is None and not ctx.get("mungkin_bebas"):
            potensi_ppn = ppn_dari_dpp(tagihan)
    biaya_luar = bulat(p["biaya_luar"] or 0)
    total_bayar = bayar_pemasok + ong_luar + biaya_luar
    ppn_kredit = ppn if (ctx["pembeli_pkp"] and p["pkp"] is True and not bebas) else Decimal(0)
    biaya_bersih = total_bayar - ppn_kredit
    manfaat_tempo = biaya_dana_dp = Decimal(0)
    if ctx["bunga"]:
        b = ctx["bunga"] / 100
        manfaat_tempo = bulat(bayar_pemasok * (100 - p["dp"]) / 100 * b * p["tempo"] / 30)
        biaya_dana_dp = bulat(bayar_pemasok * p["dp"] / 100 * b * (p["lead"] or 0) / 30)
    pembanding = biaya_bersih - manfaat_tempo + biaya_dana_dp
    qty = Decimal(qty)
    per_unit = pembanding / qty
    per_unit_beli = pembanding / q if q else per_unit
    kelebihan = q - qty if q > qty else Decimal(0)
    return {
        "qty_butuh": qty, "qty_beli": q, "kelebihan": kelebihan,
        "nilai_kelebihan": bulat(per_unit_beli * kelebihan),
        "moq_efektif": moq_eff,
        "harga_berlaku": harga, "tingkat_min": tmin, "subtotal": subtotal, "diskon": diskon,
        "ongkir_pemasok": ong_pemasok, "ongkir_luar": ong_luar, "biaya_lain": biaya_lain, "tagihan": tagihan,
        "dpp": dpp, "ppn": ppn, "sisa_pembulatan": sisa, "potensi_ppn": potensi_ppn, "ppn_ongkir": ppn_ongkir,
        "bebas_ppn": bebas,
        "bayar_pemasok": bayar_pemasok, "biaya_luar": biaya_luar, "total_bayar": total_bayar,
        "ppn_dikreditkan": ppn_kredit, "biaya_bersih": biaya_bersih, "manfaat_tempo": manfaat_tempo,
        "biaya_dana_dp": biaya_dana_dp, "biaya_pembanding": pembanding, "per_unit": per_unit,
        "per_unit_beli": per_unit_beli,
    }


def saran_tingkat(p, qty, ctx, h):
    """Tingkat harga berikutnya: apakah membeli sampai batas tingkat itu justru lebih murah total?"""
    for mn, _, _ in p["tingkat"]:
        if mn > h["qty_beli"]:
            q2 = naik_kelipatan(mn, p["kelipatan"])
            h2 = hitung(p, qty, ctx, paksa_qty=q2)
            return {"qty_beli": q2, "tambahan_unit": q2 - h["qty_beli"], "harga_berlaku": h2["harga_berlaku"],
                    "total_bayar": h2["total_bayar"], "biaya_pembanding": h2["biaya_pembanding"],
                    "selisih_total": h2["biaya_pembanding"] - h["biaya_pembanding"],
                    "biaya_per_unit_tambahan": (h2["biaya_pembanding"] - h["biaya_pembanding"]) / (q2 - h["qty_beli"]),
                    "lebih_murah_total": h2["biaya_pembanding"] <= h["biaya_pembanding"]}
    return None


# ------------------------------------------------------------------ skor & peringkat
def clamp(x, lo=Decimal(0), hi=Decimal(100)):
    return max(lo, min(hi, x))


def beri_skor(daftar, ctx, lead_ubah=None):
    """daftar: list (p, h). Kembalikan list dict skor per pemasok (urutan sama)."""
    lead_ubah = lead_ubah or {}
    min_biaya = min(h["biaya_pembanding"] for _, h in daftar)
    leads = {p["nama"]: lead_ubah.get(p["nama"], p["lead"]) for p, _ in daftar}
    diketahui = [v for v in leads.values() if v is not None]
    min_lead = min(diketahui) if diketahui else None
    bobot = ctx["bobot"]
    tot_w = sum(bobot.values())
    out = []
    for p, h in daftar:
        b = h["biaya_pembanding"]
        s_biaya = Decimal(100) if b <= 0 else clamp(Decimal(100) * max(min_biaya, Decimal(0)) / b)
        lead = leads[p["nama"]]
        telat = ctx["tenggat"] is not None and lead is not None and lead > ctx["tenggat"]
        if lead is None:
            s_lead = Decimal(50)
        elif telat:
            s_lead = Decimal(0)
        else:
            s_lead = clamp(Decimal(100) * (min_lead + 1) / (lead + 1))
        hari_bayar = -p["dp"] / 100 * (lead or 0) + (1 - p["dp"] / 100) * p["tempo"]
        s_termin = clamp(Decimal(50) + hari_bayar * Decimal(50) / Decimal(30))
        s_kual = (p["kualitas"] if p["kualitas"] is not None else Decimal(3)) * 20
        s_moq = clamp(Decimal(100) * h["qty_butuh"] / h["qty_beli"]) if h["qty_beli"] else Decimal(100)
        skor = {"biaya": s_biaya, "lead_time": s_lead, "termin": s_termin, "kualitas": s_kual, "moq": s_moq}
        total = sum(bobot[k] * skor[k] for k in KRITERIA) / tot_w
        out.append({"nama": p["nama"], "skor": skor, "total": total, "telat": telat, "lead": lead,
                    "hari_bayar": hari_bayar})
    return out


def urutkan(daftar, skor):
    """Peringkat: yang tepat waktu dulu (skor tertinggi), lalu yang melewati tenggat. Peringkat 1 = rekomendasi."""
    idx = sorted(range(len(daftar)),
                 key=lambda i: (skor[i]["telat"], -satu_desimal(skor[i]["total"]),
                                daftar[i][1]["biaya_pembanding"], daftar[i][0]["nama"]))
    return idx


def pilih_rekomendasi(daftar, skor, urut):
    tepat = [i for i in urut if not skor[i]["telat"]]
    calon = tepat or urut
    return urut[0], calon, not tepat


# ------------------------------------------------------------------ analisis lengkap
def analisis(keb_json, pemasok_raw, arg):
    ctx_raw = {norm(k): v for k, v in (keb_json or {}).items()}

    def ambil(nilai_cli, *kunci):
        if nilai_cli is not None:
            return nilai_cli
        for k in kunci:
            if norm(k) in ctx_raw:
                return ctx_raw[norm(k)]
        return None

    qty = parse_angka(ambil(arg.qty, "qty", "jumlah", "jumlah beli", "qty butuh", "kebutuhan"), "jumlah beli")
    if qty is None or qty <= 0:
        raise Galat("jumlah yang mau dibeli belum diisi (atau 0)",
                    "Isi --qty (mis. --qty 300) atau \"kebutuhan\": {\"qty\": 300}.")
    satuan = str(ambil(arg.satuan, "satuan", "unit") or "unit").strip() or "unit"
    tenggat = ambil(arg.butuh_hari, "butuh dalam hari", "tenggat hari", "tenggat", "butuh hari")
    tenggat, _ = parse_lead(tenggat)
    pembeli_pkp = parse_ya(ambil(arg.pembeli_pkp, "pembeli pkp")) is True
    bunga = parse_angka(str(ambil(arg.bunga_modal, "bunga modal persen per bulan", "bunga modal") or "").replace("%", ""),
                        "bunga modal")
    if bunga is not None and bunga < 0:
        raise Galat("bunga modal negatif", "Isi persen per bulan, mis. 1,5.")
    telat_hari = parse_angka(ambil(arg.telat_hari, "telat hari"), "telat hari")
    telat_hari = Decimal(7) if telat_hari is None else telat_hari
    biaya_telat = parse_angka(ambil(arg.biaya_telat_per_hari, "biaya telat per hari"), "biaya telat per hari")
    bagi = parse_angka(str(ambil(arg.bagi, "bagi persen", "bagi") or "70").replace("%", ""), "bagi persen")
    if bagi is None or not (50 <= bagi < 100):
        raise Galat("persen bagi pesanan harus 50-99", "Mis. --bagi 70 (70% ke pemasok utama).")
    bobot = baca_bobot(ambil(arg.bobot, "bobot"))
    barang = str(ambil(arg.barang, "barang", "nama barang", "produk") or "").strip()
    bebas_ppn = parse_ya(ambil(arg.bebas_ppn, "bebas ppn")) is True
    mungkin_bebas = bool(barang) and re.search(BAHAN_POKOK, barang.lower()) is not None
    pilihan = str(ambil(arg.pilihan, "pilihan", "pilihan pengguna") or "").strip()
    ctx = {"pembeli_pkp": pembeli_pkp, "bunga": bunga, "tenggat": tenggat, "bobot": bobot,
           "bebas_ppn": bebas_ppn, "mungkin_bebas": mungkin_bebas and not bebas_ppn, "barang": barang,
           "satuan": satuan}

    if not isinstance(pemasok_raw, list) or not pemasok_raw:
        raise Galat("tidak ada penawaran pemasok", "Beri minimal satu pemasok (idealnya 2-6).")
    daftar, dilewati = [], []
    for i, rec in enumerate(pemasok_raw, start=1):
        try:
            p = siapkan_pemasok(rec, i, satuan)
            h = hitung(p, qty, ctx)
            daftar.append((p, h))
        except Galat as e:
            nama = None
            if isinstance(rec, dict):
                nama = str(kanonik(rec)[0].get("nama") or "").strip() or None
            nama = nama or f"Pemasok {i}"
            alasan = e.pesan[len(nama):].lstrip(": ").strip() if e.pesan.startswith(nama) else e.pesan
            dilewati.append({"pemasok": nama, "alasan": alasan, "saran": e.saran})
    if not daftar:
        raise Galat("tidak ada penawaran yang bisa dihitung: " + "; ".join(d["alasan"] for d in dilewati),
                    "Lengkapi minimal nama dan harga satuan tiap pemasok.")
    nama_dup = {}
    for p, _ in daftar:
        nama_dup[p["nama"]] = nama_dup.get(p["nama"], 0) + 1
        if nama_dup[p["nama"]] > 1:
            p["nama"] = f"{p['nama']} ({nama_dup[p['nama']]})"

    skor = beri_skor(daftar, ctx)
    urut = urutkan(daftar, skor)
    rek, calon, semua_telat = pilih_rekomendasi(daftar, skor, urut)
    min_biaya = min(h["biaya_pembanding"] for _, h in daftar)
    termurah = [p["nama"] for p, h in daftar if h["biaya_pembanding"] == min_biaya]

    pemasok_out, isian, catatan = [], [], []
    for i, (p, h) in enumerate(daftar):
        s = skor[i]
        selisih = h["biaya_pembanding"] - min_biaya
        persen = satu_desimal(selisih * 100 / min_biaya) if min_biaya > 0 else Decimal(0)
        st = saran_tingkat(p, qty, ctx, h) if p["tingkat"] else None
        flag = []
        if h["kelebihan"] > 0:
            flag.append("moq_tidak_terpenuhi")
        if s["telat"]:
            flag.append("melewati_tenggat")
        if p["ongkir"] is None and p["ongkir_per_unit"] is None:
            flag.append("ongkir_belum_ada")
            isian.append({"pemasok": p["nama"], "data": "ongkir ke alamat Anda",
                          "dampak": "belum dihitung; total bisa naik"})
        if p["jenis_ongkir"] == "loco" and not p["biaya_luar"]:
            flag.append("ambil_sendiri_belum_dihitung")
            isian.append({"pemasok": p["nama"], "data": "biaya ambil barang sendiri (loco)",
                          "dampak": "belum dihitung"})
        if p["pkp"] is None and not h["bebas_ppn"]:
            flag.append("status_pkp_belum_jelas")
            isian.append({"pemasok": p["nama"], "data": "status PKP & apakah harga sudah termasuk PPN",
                          "dampak": (f"bila PKP dan harga belum termasuk PPN, total naik {rp(h['potensi_ppn'])}"
                                     if h["potensi_ppn"] is not None else
                                     "barang kemungkinan bebas PPN (bahan pokok); pastikan")})
        elif p["pkp"] is True and p["termasuk_ppn"] is None and not h["bebas_ppn"]:
            flag.append("ppn_dianggap_belum_termasuk")
            isian.append({"pemasok": p["nama"], "data": "harga sudah/belum termasuk PPN",
                          "dampak": f"dianggap belum termasuk; bila sudah termasuk, total turun {rp(h['ppn'])}"})
        if p["pkp"] is False and p["termasuk_ppn"] is True:
            flag.append("non_pkp_menyebut_ppn")
            catatan.append(f"{p['nama']} bukan PKP tetapi menyebut harga termasuk PPN: pengusaha non-PKP tidak "
                           "memungut PPN; minta klarifikasi dan rincian harga.")
        if p["lead"] is None:
            flag.append("lead_time_belum_ada")
            isian.append({"pemasok": p["nama"], "data": "lead time (berapa hari sampai barang tiba)",
                          "dampak": "skor lead time dianggap netral 50"})
        if not p["termin_diketahui"]:
            flag.append("termin_belum_ada")
            isian.append({"pemasok": p["nama"], "data": "termin bayar (DP/tempo)",
                          "dampak": "dianggap tunai saat barang diterima"})
        if p["kualitas"] is None:
            flag.append("kualitas_belum_dinilai")
        if p["moq"] is None and p["harga_dasar"] is not None:
            flag.append("moq_dianggap_tidak_ada")
        for c in p["catatan_input"]:
            catatan.append(f"{p['nama']}: {c}")
        if p["kolom_tak_dikenal"]:
            catatan.append(f"{p['nama']}: kolom tidak dikenali dan diabaikan: {', '.join(p['kolom_tak_dikenal'])}")
        pemasok_out.append({
            "nama": p["nama"], "peringkat": urut.index(i) + 1,
            "qty_butuh": jnum(h["qty_butuh"]), "qty_beli": jnum(h["qty_beli"]), "kelebihan_unit": jnum(h["kelebihan"]),
            "nilai_kelebihan": jnum(h["nilai_kelebihan"]), "moq_efektif": jnum(h["moq_efektif"]),
            "harga_berlaku": jnum(h["harga_berlaku"]), "tingkat_min_qty": jnum(h["tingkat_min"]),
            "subtotal": jnum(h["subtotal"]), "diskon": jnum(h["diskon"]),
            "ongkir_pemasok": jnum(h["ongkir_pemasok"]), "ongkir_ekspedisi": jnum(h["ongkir_luar"]),
            "jenis_ongkir": p["jenis_ongkir"], "biaya_lain": jnum(h["biaya_lain"]),
            "pkp": p["pkp"], "harga_termasuk_ppn": p["termasuk_ppn"], "bebas_ppn": h["bebas_ppn"],
            "dpp": jnum(h["dpp"]), "ppn": jnum(h["ppn"]), "ppn_atas_ongkir": jnum(h["ppn_ongkir"]),
            "sisa_pembulatan": jnum(h["sisa_pembulatan"]), "potensi_ppn": jnum(h["potensi_ppn"]),
            "bayar_ke_pemasok": jnum(h["bayar_pemasok"]), "biaya_sendiri": jnum(h["biaya_luar"]),
            "total_bayar": jnum(h["total_bayar"]), "ppn_dikreditkan": jnum(h["ppn_dikreditkan"]),
            "manfaat_tempo": jnum(h["manfaat_tempo"]), "biaya_dana_dp": jnum(h["biaya_dana_dp"]),
            "biaya_pembanding": jnum(h["biaya_pembanding"]), "per_unit": jnum(h["per_unit"]),
            "per_unit_dibeli": jnum(h["per_unit_beli"]),
            "selisih_vs_termurah_rp": jnum(selisih), "selisih_vs_termurah_persen": jnum(persen),
            "lead_time_hari": jnum(p["lead"]), "dp_persen": jnum(p["dp"]), "tempo_hari": jnum(p["tempo"]),
            "hari_bayar_rata2": jnum(satu_desimal(s["hari_bayar"])), "nilai_kualitas": jnum(p["kualitas"]),
            "garansi": p["garansi"], "catatan": p["catatan"],
            "skor": {k: jnum(satu_desimal(v)) for k, v in s["skor"].items()},
            "skor_total": jnum(satu_desimal(s["total"])),
            "saran_tingkat": None if st is None else {k: (jnum(v) if isinstance(v, Decimal) else v) for k, v in st.items()},
            "tanda": flag,
        })

    # Rekomendasi & alasan
    p_rek = daftar[rek][0]
    alasan = [f"peringkat 1, skor {fmt_d(skor[rek]['total'])}"]
    if p_rek["nama"] in termurah:
        alasan.append("termurah")
    else:
        h_rek = daftar[rek][1]
        alasan.append(f"lebih MAHAL {rp(h_rek['biaya_pembanding'] - min_biaya)} daripada termurah")
    hampir_seri = None
    if len(calon) > 1 and calon[0] == rek:
        kedua = calon[1]
        beda = satu_desimal(skor[rek]["total"]) - satu_desimal(skor[kedua]["total"])
        if beda < 2:
            hampir_seri = daftar[kedua][0]["nama"]
            alasan.append(f"skor sama dengan {hampir_seri}, dipilih yang lebih murah" if beda == 0 else
                          f"hampir seri dengan {hampir_seri} (beda {fmt_d(beda)} poin)")
    if semua_telat:
        catatan.append("Semua pemasok melewati tenggat; peringkat 1 = skor tertinggi, tanyakan percepatan kirim.")
    telat_list = [daftar[i][0]["nama"] for i in range(len(daftar)) if skor[i]["telat"]]

    sens = sensitivitas(daftar, skor, rek, calon, qty, ctx, telat_hari, biaya_telat, bagi, min_biaya)
    sementara = sorted({p["nama"] for p, h in daftar if p["nama"] in termurah and termurah_belum_pasti(p, h)})
    ringkasan = buat_ringkasan(daftar, skor, urut, rek, calon, qty, ctx, sens, min_biaya, termurah, sementara,
                               semua_telat, hampir_seri, pilihan)

    asumsi = []
    asumsi.append("Pembeli PKP: PPN dari pemasok PKP dikreditkan (tidak dihitung sebagai biaya; uang keluar tetap "
                  "termasuk PPN)." if pembeli_pkp else
                  "Pembeli dianggap bukan PKP: PPN dari pemasok PKP dihitung sebagai biaya.")
    asumsi.append("Bobot skor: " + ", ".join(f"{NAMA_KRITERIA[k]} {fmt_q(bobot[k])}" for k in KRITERIA)
                  + (" (default, bisa diubah)." if bobot == BOBOT_DEFAULT else " (diubah pengguna)."))
    asumsi.append("Harga bertingkat berlaku untuk seluruh jumlah yang dibeli (gaya grosir).")
    if any(p["kualitas"] is None for p, _ in daftar):
        asumsi.append("Kualitas/rekam jejak yang belum dinilai dianggap 3 dari 5 (netral).")
    if any(h["kelebihan"] > 0 for _, h in daftar):
        asumsi.append("Bila jumlah di bawah minimal order/kelipatan, dihitung membeli sesuai minimal order.")
    if any(not p["termin_diketahui"] for p, _ in daftar):
        asumsi.append("Termin yang belum disebut dianggap tunai saat barang diterima.")
    if bunga:
        asumsi.append(f"Bunga modal {fmt_d(bunga)}% per bulan: tempo mengurangi biaya, DP menambah biaya dana.")
    if tenggat is None:
        asumsi.append("Tenggat belum disebut: lead time dinilai relatif (tercepat = 100).")
    if bebas_ppn:
        asumsi.append("Barang dinyatakan dibebaskan PPN: PPN tidak dihitung untuk semua pemasok.")

    return {
        "versi": VERSI,
        "kebutuhan": {"qty": jnum(qty), "satuan": satuan, "tenggat_hari": jnum(tenggat), "pembeli_pkp": pembeli_pkp,
                      "bunga_modal_persen_per_bulan": jnum(bunga), "barang": barang or None,
                      "bebas_ppn": bebas_ppn, "mungkin_bahan_pokok_bebas_ppn": ctx["mungkin_bebas"]},
        "bobot": {k: jnum(v) for k, v in bobot.items()},
        "dasar_pembanding": ("biaya bersih (PPN dikreditkan)" if pembeli_pkp else "total bayar")
                            + (" setelah nilai tempo/DP" if bunga else ""),
        "pemasok": sorted(pemasok_out, key=lambda x: x["peringkat"]),
        "peringkat": [daftar[i][0]["nama"] for i in urut],
        "termurah": termurah, "termurah_sementara": sementara,
        "ringkasan_siap_salin": ringkasan,
        "rekomendasi": {"nama": p_rek["nama"], "alasan": alasan, "hampir_seri_dengan": hampir_seri,
                        "semua_melewati_tenggat": semua_telat},
        "melewati_tenggat": telat_list,
        "sensitivitas": sens,
        "isian": isian, "asumsi": asumsi, "catatan": catatan, "dilewati": dilewati,
        "catatan_ppn": CATATAN_PPN, "disclaimer": DISCLAIMER,
    }


def termurah_belum_pasti(p, h):
    """Termurah 'sementara' bila ongkir/biaya ambil belum diketahui atau status PPN belum jelas."""
    return ((p["ongkir"] is None and p["ongkir_per_unit"] is None)
            or (p["jenis_ongkir"] == "loco" and not p["biaya_luar"])
            or h["potensi_ppn"] is not None)


def banding(a, biaya_a, b, biaya_b, akhiran=""):
    """Kalimat bersubjek: 'A lebih MURAH RpX daripada B' / 'A lebih MAHAL RpX (y%) daripada B'.

    Persen hanya pada 'lebih MAHAL' dan selalu terhadap yang lebih murah (B), sama dengan kolom tabel
    "selisih vs termurah", agar tidak ada dua persen berbeda untuk selisih rupiah yang sama.
    """
    d = Decimal(biaya_a) - Decimal(biaya_b)
    if d == 0:
        return f"{a} sama biayanya dengan {b}{akhiran}"
    if d < 0:
        return f"{a} lebih MURAH {rp(-d)} daripada {b}{akhiran}"
    pct = f" ({fmt_d(d * 100 / Decimal(biaya_b))}%)" if biaya_b else ""
    return f"{a} lebih MAHAL {rp(d)}{pct} daripada {b}{akhiran}"


def ongkir_impas(p, qty, ctx, target, kolom="ongkir"):
    """Ongkir (atau biaya ambil sendiri, kolom='biaya_luar') terbesar agar biaya pemasok p masih <= target.
    Ongkir yang ditagih pemasok PKP ikut kena PPN, jadi dihitung lewat hitung() penuh, bukan dikira."""
    def biaya(o):
        if kolom == "ongkir":
            p2 = dict(p, ongkir=Decimal(o), ongkir_per_unit=None, jenis_ongkir=None)
        else:
            p2 = dict(p, biaya_luar=Decimal(o))
        return hitung(p2, qty, ctx)["biaya_pembanding"]
    if biaya(0) > target:
        return None
    lo, hi = 0, int(target) * 2 + 10
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if biaya(mid) <= target:
            lo = mid
        else:
            hi = mid - 1
    return Decimal(lo)


def pembanding_terdekat(daftar, skor, j, calon):
    """Pemasok lain termurah, utamakan yang tepat waktu."""
    pool = [i for i in calon if i != j] or [i for i in range(len(daftar)) if i != j]
    if not pool:
        return None
    return min(pool, key=lambda i: (daftar[i][1]["biaya_pembanding"], daftar[i][0]["nama"]))


def kriteria_beda(sa, sb):
    unggul = [NAMA_KRITERIA[k] for k in KRITERIA if sa["skor"][k] - sb["skor"][k] >= Decimal("0.05")]
    kalah = [NAMA_KRITERIA[k] for k in KRITERIA if sb["skor"][k] - sa["skor"][k] >= Decimal("0.05")]
    return unggul, kalah


def buat_ringkasan(daftar, skor, urut, rek, calon, qty, ctx, sens, min_biaya, termurah, sementara,
                   semua_telat, hampir_seri, pilihan):
    """Kalimat utuh bersubjek, arah selisih eksplisit. Agent WAJIB menyalin apa adanya."""
    sat = ctx["satuan"]
    utk = f" untuk {fmt_q(qty)} {sat}"
    nm = lambda i: daftar[i][0]["nama"]  # noqa: E731
    by = lambda i: daftar[i][1]["biaya_pembanding"]  # noqa: E731
    L = []
    # 1) Peringkat & rekomendasi
    L.append("Peringkat: " + ", ".join(
        f"{k + 1}. {nm(i)} (skor {fmt_d(skor[i]['total'])}{', melewati tenggat' if skor[i]['telat'] else ''})"
        for k, i in enumerate(urut)) + ".")
    kal = f"Rekomendasi: {nm(rek)} (peringkat 1)."
    if hampir_seri:
        beda = satu_desimal(skor[rek]["total"]) - satu_desimal(skor[urut[1]]["total"])
        kal += (f" Skornya sama dengan {hampir_seri}; dipilih yang lebih murah." if beda == 0 else
                f" Skornya hampir seri dengan {hampir_seri} (beda {fmt_d(beda)} poin).")
    if semua_telat:
        kal += " Semua pemasok melewati tenggat; minta percepatan kirim sebelum memesan."
    L.append(kal)
    # 2) Biaya rekomendasi dibanding termurah / termurah berikutnya
    i_ter = min(range(len(daftar)), key=lambda i: (by(i), nm(i)))
    def tanda_sem(i):
        p, h = daftar[i]
        sebab = []
        if p["ongkir"] is None and p["ongkir_per_unit"] is None:
            sebab.append("ongkir belum diketahui")
        if p["jenis_ongkir"] == "loco" and not p["biaya_luar"]:
            sebab.append("biaya ambil belum dihitung")
        if h["potensi_ppn"] is not None:
            sebab.append("status PPN belum jelas")
        return f" (sementara: {', '.join(sebab)})" if sebab else ""
    if by(rek) == min_biaya:
        lain = [i for i in range(len(daftar)) if i != rek]
        if lain:
            j = min(lain, key=lambda i: (by(i), nm(i)))
            L.append(f"{nm(rek)} adalah yang termurah{tanda_sem(rek)}: "
                     + banding(nm(rek), by(rek), nm(j), by(j), utk) + f", termurah berikutnya.")
        else:
            L.append(f"Hanya ada satu penawaran ({nm(rek)}); minta 2 penawaran lagi agar bisa dibandingkan.")
    else:
        alasan = (f"{nm(i_ter)} melewati tenggat" if skor[i_ter]["telat"] else
                  "skor gabungannya lebih tinggi")
        unggul, _ = kriteria_beda(skor[rek], skor[i_ter])
        if not skor[i_ter]["telat"] and unggul:
            alasan += " (unggul di " + ", ".join(unggul) + ")"
        L.append(banding(nm(rek), by(rek), nm(i_ter), by(i_ter), utk)
                 + f". {nm(i_ter)} adalah termurah{tanda_sem(i_ter)}; {nm(rek)} dipilih karena {alasan}.")
        if skor[i_ter]["telat"] and not semua_telat:
            i_ok = min(calon, key=lambda i: (by(i), nm(i)))
            if i_ok == rek:
                L.append(f"{nm(rek)} adalah yang termurah di antara pemasok yang tepat waktu.")
            else:
                unggul, _ = kriteria_beda(skor[rek], skor[i_ok])
                L.append(banding(nm(rek), by(rek), nm(i_ok), by(i_ok), utk)
                         + f". {nm(i_ok)} adalah termurah yang tepat waktu{tanda_sem(i_ok)}; {nm(rek)} dipilih karena "
                         "skor gabungannya lebih tinggi" + (" (unggul di " + ", ".join(unggul) + ")" if unggul else "")
                         + ".")
    # 3) Sensitivitas: jumlah 2x
    q2 = sens.get("qty_2x")
    if q2:
        biaya2 = {x["nama"]: Decimal(str(x["biaya_pembanding"])) for x in q2["pemasok"]}
        t2 = q2["termurah"][0]
        kal = (f"Bila jumlahnya 2x ({fmt_q(Decimal(str(q2['qty'])))} {sat}): termurah {t2} "
               f"({rp(biaya2[t2])}); ")
        if q2["rekomendasi_berubah"]:
            kal += (f"rekomendasi berubah menjadi {q2['rekomendasi']} ("
                    + banding(q2["rekomendasi"], biaya2[q2["rekomendasi"]], nm(rek), biaya2[nm(rek)],
                              f" untuk {fmt_q(Decimal(str(q2['qty'])))} {sat}") + ").")
        else:
            kal += f"rekomendasi tetap {nm(rek)}."
        L.append(kal)
    # 4) Sensitivitas: termurah (tepat waktu) telat
    t = sens.get("termurah_telat")
    if t:
        label = "termurah" if t["termurah_keseluruhan"] else "termurah yang tepat waktu"
        tiba = (f"tiba hari ke-{fmt_q(Decimal(str(t['lead_time_menjadi'])))}" if t["lead_time_awal"] is not None
                else f"baru tiba setelah {fmt_q(Decimal(str(t['lead_time_menjadi'])))} hari")
        if t["melewati_tenggat"]:
            tiba += f", melewati tenggat {fmt_q(Decimal(str(jnum(ctx['tenggat']))))} hari"
        kal = f"Bila {t['pemasok']} ({label}) telat {fmt_q(Decimal(str(t['telat_hari'])))} hari ({tiba}): "
        if t["rekomendasi_berubah"]:
            kal += (f"rekomendasi pindah ke {t['rekomendasi_menjadi']}, yang "
                    + banding("", Decimal(str(t["biaya_rekomendasi_baru"])), t["pemasok"],
                              Decimal(str(t["biaya_pemasok"]))).strip() + ".")
        else:
            kal += f"rekomendasi tetap {t['rekomendasi_menjadi']}."
        L.append(kal)
        if "hari_impas" in t:
            L.append(f"Bila kerugian akibat telat {rp(Decimal(str(t['biaya_telat_per_hari'])))} per hari: "
                     f"{t['pemasok']} {rp(Decimal(str(t['hemat_vs_termurah_kedua'])))} lebih murah daripada "
                     f"{t['termurah_kedua']}, dan keunggulan itu habis bila telat lebih dari "
                     f"{fmt_q(Decimal(str(t['hari_impas'])))} hari (telat {fmt_q(Decimal(str(t['telat_hari'])))} "
                     f"hari = rugi {rp(Decimal(str(t['kerugian_bila_telat'])))}).")
    # 5) Bagi pesanan
    b = sens.get("bagi_pesanan")
    if b:
        pu = Decimal(str(b["persen_utama"]))
        bagian = (f"{b['utama']} {fmt_q(Decimal(str(b['qty_utama'])))} {sat} + {b['cadangan']} "
                  f"{fmt_q(Decimal(str(b['qty_cadangan'])))} {sat}")
        paksa = []
        if b["beli_utama"] != b["qty_utama"]:
            paksa.append(f"{b['utama']} wajib beli {fmt_q(Decimal(str(b['beli_utama'])))} {sat}")
        if b["beli_cadangan"] != b["qty_cadangan"]:
            paksa.append(f"{b['cadangan']} wajib beli {fmt_q(Decimal(str(b['beli_cadangan'])))} {sat}")
        if paksa:
            bagian += "; " + " dan ".join(paksa) + " karena minimal order/kelipatan"
        tot = Decimal(str(b["total"]))
        L.append(f"Bila pesanan dibagi {fmt_q(pu)}/{fmt_q(100 - pu)} ({bagian}): total {rp(tot)}, "
                 + banding("", tot, f"membeli semua dari {b['utama']}", by(rek)).strip() + ".")
    # 6) Data kosong: ongkir impas
    n_ong = 0
    for i in urut:
        p, h = daftar[i]
        if not (p["ongkir"] is None and p["ongkir_per_unit"] is None) or n_ong >= 3:
            continue
        j = pembanding_terdekat(daftar, skor, i, calon)
        if j is None:
            L.append(f"Ongkir {p['nama']} belum diketahui; total di atas belum termasuk ongkir.")
            continue
        n_ong += 1
        imp = ongkir_impas(p, qty, ctx, by(j))
        if imp is None:
            L.append(f"Ongkir {p['nama']} belum diketahui; walau tanpa ongkir, "
                     + banding(p["nama"], by(i), nm(j), by(j)) + ".")
        else:
            L.append(f"Ongkir {p['nama']} belum diketahui (total di atas belum termasuk ongkir): {p['nama']} tetap "
                     f"tidak lebih mahal daripada {nm(j)} selama ongkirnya maksimal {rp(imp)}{utk} "
                     f"(setara {rp_unit(imp / qty)} per {sat}).")
    for i in urut:
        p, h = daftar[i]
        if not (p["jenis_ongkir"] == "loco" and not p["biaya_luar"]) or n_ong >= 3:
            continue
        j = pembanding_terdekat(daftar, skor, i, calon)
        if j is None:
            continue
        n_ong += 1
        imp = ongkir_impas(p, qty, ctx, by(j), kolom="biaya_luar")
        if imp is None:
            L.append(f"Biaya ambil sendiri ke {p['nama']} belum dihitung; walau tanpa biaya ambil, "
                     + banding(p["nama"], by(i), nm(j), by(j)) + ".")
        else:
            L.append(f"Biaya ambil sendiri ke {p['nama']} belum dihitung: {p['nama']} tetap tidak lebih mahal daripada "
                     f"{nm(j)} selama biaya ambilnya (bensin, sewa angkutan, waktu) maksimal {rp(imp)}{utk}.")
    # 7) Data kosong: status PKP belum jelas (termurah & rekomendasi saja)
    for i in sorted({i_ter, rek}, key=lambda x: urut.index(x)):
        p, h = daftar[i]
        if h["potensi_ppn"] is None:
            continue
        p2 = dict(p, pkp=True, termasuk_ppn=False)
        h2 = hitung(p2, qty, ctx)
        d2 = list(daftar)
        d2[i] = (p2, h2)
        sk2 = beri_skor(d2, ctx)
        ur2 = urutkan(d2, sk2)
        j = pembanding_terdekat(d2, sk2, i, [x for x in ur2 if not sk2[x]["telat"]])
        kal = (f"Bila {p['nama']} ternyata PKP dan harga belum termasuk PPN: total {p['nama']} menjadi "
               f"{rp(h2['biaya_pembanding'])} (naik {rp(h2['biaya_pembanding'] - h['biaya_pembanding'])})")
        if j is not None:
            kal += "; " + banding(p["nama"], h2["biaya_pembanding"], nm(j), d2[j][1]["biaya_pembanding"])
        if d2[ur2[0]][0]["nama"] == nm(rek):
            kal += f"; rekomendasi tetap {nm(rek)}."
        else:
            r2 = ur2[0]
            kal += f"; rekomendasi berubah menjadi {d2[r2][0]['nama']} karena skor gabungannya lebih tinggi"
            if r2 != i:
                unggul, _ = kriteria_beda(sk2[r2], sk2[i])
                if unggul:
                    kal += " (unggul di " + ", ".join(unggul) + ")"
            kal += "."
        L.append(kal)
    # 8) Asumsi pajak yang terbuka
    for i in urut:
        p, h = daftar[i]
        if p["pkp"] is True and not h["bebas_ppn"] and h["ongkir_pemasok"] > 0:
            if p["termasuk_ppn"] is True:
                L.append(f"Asumsi pajak: ongkir {p['nama']} dianggap bagian dari harga yang sudah termasuk PPN.")
            else:
                L.append(f"Asumsi pajak: ongkir {p['nama']} ikut kena PPN karena ditagih di faktur pemasok PKP "
                         f"(PPN atas ongkir {rp(h['ppn_ongkir'])}); bila ongkir itu hanya titipan biaya ekspedisi "
                         f"atas nama Anda, total {p['nama']} turun {rp(h['ppn_ongkir'])}.")
    if ctx["pembeli_pkp"] and any(h["ppn_dikreditkan"] > 0 for _, h in daftar):
        L.append("Asumsi pajak: PPN pemasok PKP dianggap bisa dikreditkan karena usaha Anda PKP; syaratnya faktur "
                 "pajak sah atas nama dan NPWP usaha Anda, dan pembelian dipakai untuk kegiatan usaha yang "
                 "terutang PPN. Bila tidak memenuhi, PPN menjadi biaya.")
    if ctx["mungkin_bebas"]:
        L.append(f"{ctx['barang'][:1].upper()}{ctx['barang'][1:]} kemungkinan termasuk bahan pokok yang dibebaskan "
                 "PPN (PP 49/2022), jadi PPN tidak ditambahkan untuk pemasok yang status PKP-nya belum jelas; "
                 "cek status barang Anda.")
    elif not ctx["barang"] and any(h["potensi_ppn"] is not None for _, h in daftar):
        L.append("Beberapa bahan pokok (mis. beras, gula konsumsi, daging, telur) dibebaskan PPN menurut PP 49/2022; "
                 "cek status barang Anda (bila dibebaskan, tambahan PPN di atas tidak berlaku).")
    # 9) Pilihan pengguna
    if pilihan:
        cocok = [i for i in range(len(daftar)) if nm(i).lower() == pilihan.lower()] or \
                [i for i in range(len(daftar)) if pilihan.lower() in nm(i).lower()]
        if not cocok:
            L.append(f"Pemasok '{pilihan}' tidak ada di penawaran yang dihitung.")
        elif cocok[0] == rek:
            L.append(f"Pemasok yang Anda condongi, {nm(rek)}, sama dengan peringkat 1.")
        else:
            i = cocok[0]
            unggul, kalah = kriteria_beda(skor[i], skor[rek])
            kal = (f"Pemasok yang Anda condongi, {nm(i)}, ada di peringkat {urut.index(i) + 1}"
                   + (" (melewati tenggat)" if skor[i]["telat"] else "") + ": "
                   + banding(nm(i), by(i), nm(rek), by(rek)) + f" (peringkat 1); skor {fmt_d(skor[i]['total'])} "
                   f"vs {fmt_d(skor[rek]['total'])}")
            if unggul:
                kal += "; unggul di " + ", ".join(unggul)
            if kalah:
                kal += "; kalah di " + ", ".join(kalah)
            L.append(kal + ".")
    return L


def sensitivitas(daftar, skor, rek, calon, qty, ctx, telat_hari, biaya_telat, bagi, min_biaya):
    out = {}
    # 1) Jumlah 2x
    qty2 = qty * 2
    d2 = []
    for p, _ in daftar:
        try:
            d2.append((p, hitung(p, qty2, ctx)))
        except Galat:
            pass
    if d2:
        sk2 = beri_skor(d2, ctx)
        ur2 = urutkan(d2, sk2)
        rek2, _, _ = pilih_rekomendasi(d2, sk2, ur2)
        mb2 = min(h["biaya_pembanding"] for _, h in d2)
        out["qty_2x"] = {
            "qty": jnum(qty2),
            "termurah": [p["nama"] for p, h in d2 if h["biaya_pembanding"] == mb2],
            "rekomendasi": d2[rek2][0]["nama"],
            "rekomendasi_berubah": d2[rek2][0]["nama"] != daftar[rek][0]["nama"],
            "pemasok": [{"nama": d2[i][0]["nama"], "biaya_pembanding": jnum(d2[i][1]["biaya_pembanding"]),
                         "per_unit": jnum(d2[i][1]["per_unit"]), "skor_total": jnum(satu_desimal(sk2[i]["total"]))}
                        for i in ur2],
        }
    # 2) Pemasok termurah telat
    # Subjek = pemasok termurah yang tepat waktu (yang termurah tapi sudah telat tidak relevan).
    i_min = min(calon, key=lambda i: (daftar[i][1]["biaya_pembanding"], daftar[i][0]["nama"]))
    p_min, h_min = daftar[i_min]
    lead_baru = (p_min["lead"] or Decimal(0)) + telat_hari
    sk_t = beri_skor(daftar, ctx, lead_ubah={p_min["nama"]: lead_baru})
    ur_t = urutkan(daftar, sk_t)
    rek_t, _, _ = pilih_rekomendasi(daftar, sk_t, ur_t)
    pool = [j for j in calon if j != i_min] or [j for j in range(len(daftar)) if j != i_min]
    lain = sorted((daftar[j][1]["biaya_pembanding"], daftar[j][0]["nama"]) for j in pool)
    tel = {"pemasok": p_min["nama"], "termurah_keseluruhan": h_min["biaya_pembanding"] == min_biaya,
           "lead_time_awal": jnum(p_min["lead"]), "biaya_pemasok": jnum(h_min["biaya_pembanding"]),
           "biaya_rekomendasi_baru": jnum(daftar[rek_t][1]["biaya_pembanding"]),
           "telat_hari": jnum(telat_hari), "lead_time_menjadi": jnum(lead_baru),
           "melewati_tenggat": ctx["tenggat"] is not None and lead_baru > ctx["tenggat"],
           "rekomendasi_menjadi": daftar[rek_t][0]["nama"],
           "rekomendasi_berubah": daftar[rek_t][0]["nama"] != daftar[rek][0]["nama"]}
    if lain:
        hemat = lain[0][0] - h_min["biaya_pembanding"]
        tel["termurah_kedua"] = lain[0][1]
        tel["hemat_vs_termurah_kedua"] = jnum(hemat)
        if biaya_telat and biaya_telat > 0:
            tel["biaya_telat_per_hari"] = jnum(biaya_telat)
            tel["hari_impas"] = jnum((hemat / biaya_telat).to_integral_value(rounding=ROUND_FLOOR))
            tel["kerugian_bila_telat"] = jnum(bulat(biaya_telat * telat_hari))
            tel["masih_untung_bila_telat"] = biaya_telat * telat_hari < hemat
    out["termurah_telat"] = tel
    # 3) Bagi pesanan (kurangi ketergantungan satu pemasok): cadangan = calon lain dengan total gabungan termurah
    if len(calon) > 1:
        p_a, h_a = daftar[rek]
        qa = bulat(qty * bagi / 100) if qty == qty.to_integral_value() else qty * bagi / 100
        qb = qty - qa
        terbaik = None
        if qb > 0 and qa > 0:
            try:
                ha = hitung(p_a, qa, ctx)
            except Galat:
                ha = None
            for j in calon[1:]:
                p_b = daftar[j][0]
                try:
                    hb = hitung(p_b, qb, ctx)
                except Galat:
                    continue
                if ha is None:
                    break
                total = ha["biaya_pembanding"] + hb["biaya_pembanding"]
                if terbaik is None or total < terbaik[0]:
                    terbaik = (total, p_b, hb)
        if terbaik is not None:
            total, p_b, hb = terbaik
            tambah = total - h_a["biaya_pembanding"]
            out["bagi_pesanan"] = {
                "utama": p_a["nama"], "qty_utama": jnum(qa), "beli_utama": jnum(ha["qty_beli"]),
                "cadangan": p_b["nama"], "qty_cadangan": jnum(qb), "beli_cadangan": jnum(hb["qty_beli"]),
                "total": jnum(total), "tambahan_vs_satu_pemasok": jnum(tambah),
                "tambahan_persen": jnum(satu_desimal(tambah * 100 / h_a["biaya_pembanding"]))
                if h_a["biaya_pembanding"] > 0 else None,
                "moq_memaksa_beli_lebih": ha["kelebihan"] > 0 or hb["kelebihan"] > 0,
                "persen_utama": jnum(bagi),
            }
    return out


def baca_bobot(nilai):
    bobot = dict(BOBOT_DEFAULT)
    if kosong(nilai):
        return bobot
    alias = {"biaya": "biaya", "harga": "biaya", "cost": "biaya", "lead": "lead_time", "lead time": "lead_time",
             "leadtime": "lead_time", "waktu": "lead_time", "kirim": "lead_time", "kecepatan": "lead_time",
             "termin": "termin", "bayar": "termin", "pembayaran": "termin", "tempo": "termin",
             "kualitas": "kualitas", "mutu": "kualitas", "rekam jejak": "kualitas", "rekam": "kualitas",
             "moq": "moq", "fleksibilitas": "moq", "fleksibel": "moq"}
    if isinstance(nilai, dict):
        pasang = list(nilai.items())
    else:
        pasang = []
        for seg in re.split(r"[,;/]", str(nilai)):
            if not seg.strip():
                continue
            m = re.match(r"^\s*([a-z _-]+?)\s*[=:]?\s*(\d+(?:[.,]\d+)?)\s*%?\s*$", seg.strip().lower())
            if not m:
                raise Galat(f"bobot '{seg.strip()}' tidak terbaca", "Contoh: --bobot \"biaya=50,lead=20,termin=10,kualitas=10,moq=10\"")
            pasang.append((m.group(1), m.group(2)))
    for k, v in pasang:
        kk = alias.get(norm(k).replace("_", " "), alias.get(norm(k)))
        if kk is None:
            raise Galat(f"kriteria bobot '{k}' tidak dikenal", "Pakai: biaya, lead, termin, kualitas, moq.")
        try:
            angka = Decimal(str(v).replace(",", "."))
        except InvalidOperation:
            raise Galat(f"bobot '{k}' bukan angka", "Contoh: biaya=40")
        if angka < 0:
            raise Galat(f"bobot '{k}' negatif", "Bobot 0 atau lebih.")
        bobot[kk] = angka
    if sum(bobot.values()) <= 0:
        raise Galat("semua bobot nol", "Beri minimal satu kriteria bobot > 0.")
    return bobot


# ------------------------------------------------------------------ keluaran teks
def teks_termin(dp, tempo):
    if dp >= 100:
        return "bayar penuh di muka"
    if dp == 0:
        return "tunai saat barang diterima" if tempo == 0 else f"tempo {fmt_q(tempo)} hari"
    return (f"DP {fmt_q(dp)}%, pelunasan saat barang diterima" if tempo == 0 else
            f"DP {fmt_q(dp)}%, sisa tempo {fmt_q(tempo)} hari")


def teks(h):
    k = h["kebutuhan"]
    sat = k["satuan"]
    L = [LABEL_AGENT]
    L.append(f"Kebutuhan: {fmt_q(Decimal(str(k['qty'])))} {sat}"
             + (f" {k['barang']}" if k.get("barang") else "")
             + (f" | tenggat {fmt_q(Decimal(str(k['tenggat_hari'])))} hari" if k["tenggat_hari"] is not None else "")
             + (" | pembeli PKP" if k["pembeli_pkp"] else " | pembeli bukan PKP (PPN = biaya)")
             + " | bobot: " + ", ".join(f"{NAMA_KRITERIA[x]} {fmt_q(Decimal(str(h['bobot'][x])))}" for x in KRITERIA))
    if k["pembeli_pkp"]:
        kepala = "Biaya bersih tanpa PPN" + (" & setelah nilai tempo" if k["bunga_modal_persen_per_bulan"] else "")
    else:
        kepala = "Biaya setelah nilai tempo" if k["bunga_modal_persen_per_bulan"] else "Total bayar"
    L.append("")
    L.append("TABEL SIAP TEMPEL (salin apa adanya; urut peringkat, peringkat 1 = rekomendasi)")
    L.append(f"| Pemasok | {kepala} (per {sat}) | Selisih vs termurah | Skor (peringkat) |")
    L.append("|---|---|---|---|")
    for p in h["pemasok"]:
        if p["selisih_vs_termurah_rp"] == 0:
            sel = "termurah sementara" if p["nama"] in h["termurah_sementara"] else "termurah"
        else:
            sel = (f"lebih mahal {rp(Decimal(str(p['selisih_vs_termurah_rp'])))} "
                   f"({fmt_d(Decimal(str(p['selisih_vs_termurah_persen'])))}%)")
        tanda = ", telat" if "melewati_tenggat" in p["tanda"] else ""
        L.append(f"| {p['nama']} | {rp(Decimal(str(p['biaya_pembanding'])))} "
                 f"({rp_unit(Decimal(str(p['per_unit'])))}) | {sel} | "
                 f"{fmt_d(Decimal(str(p['skor_total'])))} ({p['peringkat']}{tanda}) |")
    L.append("")
    L.append("RINGKASAN SIAP SALIN (WAJIB disalin apa adanya; jangan dihitung ulang, dibalik, atau ditafsir sendiri)")
    for x in h["ringkasan_siap_salin"]:
        L.append(f"- {x}")
    L.append("")
    L.append("RINCIAN PER PEMASOK (bahan 1 baris per pemasok)")
    for p in h["pemasok"]:
        D = lambda key: Decimal(str(p[key])) if p[key] is not None else None  # noqa: E731
        L.append(f"{p['peringkat']}. {p['nama']}")
        beli = f"   Beli {fmt_q(D('qty_beli'))} {sat} x {rp_unit(D('harga_berlaku'))}"
        if p["tingkat_min_qty"] is not None:
            beli += f" (harga tingkat >= {fmt_q(D('tingkat_min_qty'))})"
        beli += f" = {rp(D('subtotal'))}"
        if p["kelebihan_unit"]:
            beli += (f" | minimal order/kelipatan: sisa {fmt_q(D('kelebihan_unit'))} {sat}, modal tertahan "
                     f"{rp(D('nilai_kelebihan'))}")
        L.append(beli)
        ong = "BELUM DIKETAHUI (belum dihitung)" if "ongkir_belum_ada" in p["tanda"] else (
            "gratis (franco)" if p["jenis_ongkir"] == "franco" else (
                "ambil sendiri (loco)" if p["jenis_ongkir"] == "loco" else rp(D("ongkir_pemasok") + D("ongkir_ekspedisi"))))
        if p["bebas_ppn"]:
            ppn = "tanpa PPN (barang dibebaskan PPN)"
        elif p["pkp"] is True:
            ppn = (f"PPN {rp(D('ppn'))} (DPP {rp(D('dpp'))}"
                   + (", sudah termasuk harga" if p["harga_termasuk_ppn"] else ", ditambahkan")
                   + (f", sisa pembulatan {rp(D('sisa_pembulatan'))}" if p["sisa_pembulatan"] else "") + ")")
        elif p["pkp"] is False:
            ppn = "tanpa PPN (bukan PKP)"
        elif p["potensi_ppn"] is not None:
            ppn = f"status PPN belum jelas (bila PKP & belum termasuk PPN: +{rp(D('potensi_ppn'))})"
        else:
            ppn = "status PPN belum jelas (barang kemungkinan bebas PPN)"
        diskon = f"Diskon {rp(D('diskon'))} | " if p["diskon"] else ""
        lain = f" | Biaya lain {rp(D('biaya_lain'))}" if p["biaya_lain"] else ""
        L.append(f"   {diskon}Ongkir {ong}{lain} | {ppn}"
                 + (f" | Biaya sendiri {rp(D('biaya_sendiri'))}" if p["biaya_sendiri"] else ""))
        tot = f"   Total bayar {rp(D('total_bayar'))}"
        if p["ppn_dikreditkan"]:
            tot += f" | PPN dikreditkan {rp(D('ppn_dikreditkan'))} -> biaya bersih {rp(D('total_bayar') - D('ppn_dikreditkan'))}"
        if p["manfaat_tempo"] or p["biaya_dana_dp"]:
            tot += f" | nilai tempo dikurangi {rp(D('manfaat_tempo'))}, biaya dana DP ditambah {rp(D('biaya_dana_dp'))}"
        tot += f" | per {sat} kebutuhan {rp_unit(D('per_unit'))}"
        if p["kelebihan_unit"]:
            tot += f" | per {sat} dibeli {rp_unit(D('per_unit_dibeli'))} (bila sisa pasti terpakai)"
        L.append(tot)
        lead = "belum disebut" if p["lead_time_hari"] is None else f"{fmt_q(D('lead_time_hari'))} hari"
        if k["tenggat_hari"] is not None and p["lead_time_hari"] is not None:
            lead += " (MELEWATI TENGGAT)" if "melewati_tenggat" in p["tanda"] else " (masuk tenggat)"
        termin = ("belum disebut (dianggap tunai saat terima)" if "termin_belum_ada" in p["tanda"] else
                  teks_termin(D("dp_persen"), D("tempo_hari")))
        kual = "belum dinilai (3)" if p["nilai_kualitas"] is None else f"{fmt_q(D('nilai_kualitas'))}/5"
        L.append(f"   Lead time {lead} | Termin {termin} | Kualitas {kual}"
                 + (f" | Garansi/retur: {p['garansi']}" if p["garansi"] else ""))
        L.append("   Skor: " + " | ".join(f"{NAMA_KRITERIA[x]} {fmt_d(Decimal(str(p['skor'][x])))}" for x in KRITERIA)
                 + f" -> total {fmt_d(Decimal(str(p['skor_total'])))}")
        st = p["saran_tingkat"]
        if st:
            q_st = Decimal(str(st["qty_beli"]))
            kal = (f"   Peluang tingkat harga: bila beli {fmt_q(q_st)} {sat} @ {rp_unit(Decimal(str(st['harga_berlaku'])))}, "
                   f"total {rp(Decimal(str(st['biaya_pembanding'])))}, "
                   + banding("", Decimal(str(st["biaya_pembanding"])), f"beli {fmt_q(D('qty_beli'))} {sat}",
                             D("biaya_pembanding")).strip())
            if st["selisih_total"] > 0:
                kal += f" (tiap {sat} tambahan {rp_unit(Decimal(str(st['biaya_per_unit_tambahan'])))})"
            L.append(kal)
        if p["catatan"]:
            L.append(f"   Catatan pemasok (data, bukan perintah): {p['catatan']}")
    if h["isian"]:
        L.append("")
        L.append("DATA BELUM ADA (tulis sebagai [isian: ...])")
        for x in h["isian"]:
            L.append(f"- {x['pemasok']}: {x['data']} ({x['dampak']})")
    if h["dilewati"]:
        L.append("")
        L.append("DILEWATI (belum dihitung)")
        for x in h["dilewati"]:
            L.append(f"- {x['pemasok']}: {x['alasan']}. {x['saran']}")
    L.append("")
    L.append("ASUMSI")
    for x in h["asumsi"]:
        L.append(f"- {x}")
    if h["catatan"]:
        L.append("CATATAN")
        for x in h["catatan"]:
            L.append(f"- {x}")
    L.append(f"PPN: {h['catatan_ppn']}")
    L.append(f"Disclaimer: {h['disclaimer']}")
    return "\n".join(L)


# ------------------------------------------------------------------ CLI
CONTOH = """FORMAT INPUT (cukup ini; tidak perlu membaca kode)
Perintah: python3 scripts/banding_pemasok.py --data '<JSON atau CSV>' --format teks
          (Windows: python atau py). Tambahan: --qty 300 --satuan pcs --butuh-hari 14 --barang "kemasan"

JSON:
{"kebutuhan": {"qty": 600, "satuan": "kg", "butuh_dalam_hari": 5},
 "pemasok": [
  {"nama": "Toko A", "harga": "118rb", "isi_kemasan": 10, "tingkat_harga": "51: 5%", "ongkir": "100rb",
   "ppn": "?", "lead_time": "2-3 hari", "termin": "COD"},
  {"nama": "PT B", "harga": 11200, "moq": 300, "ongkir": 150000, "ppn": "belum", "lead_time": "3-4 hari",
   "termin": "tempo 30 hari"},
  {"nama": "CV C", "harga": 11900, "ongkir": "franco", "ppn": "non-pkp", "lead_time": "5-7 hari",
   "termin": "bayar di muka"}]}

CSV (pemisah ; dan tingkat harga dipisah |):
nama;harga;tingkat harga;moq;ongkir;ppn;lead time;termin;kualitas
CV A;4.500;250: 4.200 | 500: 3.900;100;85rb;belum;5-7 hari;DP 50%;4

KAMUS KOLOM
nama            nama pemasok
harga           harga satuan dasar (12.500 / 12,5rb / Rp12.500/pcs)
tingkat_harga   'min: harga' dipisah ; atau | ('100: 11.000; 500: 10.000'); persen = diskon ('51: 5%')
isi_kemasan     isi per dus/pak bila harga ditulis per dus (harga, MOQ, tingkat, ongkir '/dus' lalu dibaca per dus)
moq / kelipatan / min_belanja   minimal order, kelipatan pesan, minimal belanja Rp ('2 lusin' = 24)
diskon          '5%' (persen) atau 'Rp25.000' (rupiah)
ongkir          Rp sekali kirim | 'franco'/'gratis' | 'loco'/'ambil sendiri' | 'Rp500/pcs', '15rb/dus' | kosong = BELUM DIKETAHUI
ongkir_ditagih_pemasok  'tidak' bila ongkir dibayar langsung ke ekspedisi (tidak kena PPN pemasok)
ppn             termasuk = PKP, harga SUDAH termasuk PPN
                belum    = PKP, harga BELUM termasuk PPN (ditambah 11%)
                non-pkp  = bukan PKP, tanpa PPN
                bebas    = barang dibebaskan PPN
                ? / kosong = belum jelas -> [isian]
biaya_lain      biaya lain di faktur pemasok;  biaya_luar = biaya yang dikeluarkan sendiri (ambil barang)
lead_time       '3', '3-5 hari' (diambil 5), '2 minggu', '5 hari kerja' (= 7 hari kalender)
termin          'COD', 'tempo 30 hari', 'DP 50% sisa H+30', 'bayar di muka'
kualitas        1-5 dari info pengguna (kosong = 3 netral);  garansi, catatan = teks bebas
Opsi: --pembeli-pkp ya | --bobot "biaya=40,lead=20,termin=15,kualitas=15,moq=10" | --telat-hari 7
      --biaya-telat-per-hari 200rb | --bunga-modal 1,5 | --bagi 70 | --barang "gula pasir" | --bebas-ppn ya
      --pilihan "nama pemasok yang dicondongi pengguna"
Keluaran --format teks: TABEL SIAP TEMPEL + RINGKASAN SIAP SALIN (disalin apa adanya) + rincian."""

class Parser(argparse.ArgumentParser):
    def error(self, message):
        print(json.dumps({"error": message, "saran": "Lihat --help untuk contoh pemakaian."}, ensure_ascii=False),
              file=sys.stderr)
        sys.exit(2)


def main(argv=None):
    ap = Parser(description="Bandingkan penawaran pemasok: biaya mendarat, per unit, skor tertimbang, sensitivitas.")
    ap.add_argument("--file", help="File JSON atau CSV penawaran")
    ap.add_argument("--data", help="Teks JSON/CSV/tabel markdown langsung")
    ap.add_argument("--qty", help="Jumlah yang dibutuhkan, mis. 300")
    ap.add_argument("--satuan", help="Satuan, mis. pcs/kg/dus")
    ap.add_argument("--butuh-hari", dest="butuh_hari", help="Barang harus tiba dalam berapa hari")
    ap.add_argument("--pembeli-pkp", dest="pembeli_pkp", help="ya bila usaha pembeli PKP (PPN bisa dikreditkan)")
    ap.add_argument("--bobot", help="mis. \"biaya=40,lead=20,termin=15,kualitas=15,moq=10\"")
    ap.add_argument("--telat-hari", dest="telat_hari", help="Skenario telat pemasok termurah (default 7)")
    ap.add_argument("--biaya-telat-per-hari", dest="biaya_telat_per_hari", help="Perkiraan rugi per hari telat (Rp)")
    ap.add_argument("--bunga-modal", dest="bunga_modal", help="Biaya modal %% per bulan (opsional)")
    ap.add_argument("--bagi", help="Persen ke pemasok utama saat dibagi dua (default 70)")
    ap.add_argument("--barang", help="Nama barang, mis. 'gula pasir' (bahan pokok -> kemungkinan bebas PPN)")
    ap.add_argument("--bebas-ppn", dest="bebas_ppn", help="ya bila barang dibebaskan PPN (PPN tidak dihitung)")
    ap.add_argument("--pilihan", help="Pemasok yang dicondongi pengguna (dibandingkan dengan peringkat 1)")
    ap.add_argument("--contoh", action="store_true", help="Cetak format input + kamus kolom, lalu keluar")
    ap.add_argument("--format", choices=["json", "teks"], default="json")
    a = ap.parse_args(argv)
    if a.contoh:
        print(CONTOH)
        return
    try:
        if a.file:
            try:
                with open(a.file, encoding="utf-8-sig") as f:
                    isi = f.read()
            except OSError as e:
                raise Galat(f"file tidak bisa dibuka: {e.strerror}", "Periksa nama/lokasi file.")
        elif a.data is not None:
            isi = a.data.replace("\\n", "\n")
        else:
            isi = sys.stdin.read()
        keb, pem = muat_input(isi)
        hasil = analisis(keb, pem, a)
    except Galat as e:
        print(json.dumps({"error": e.pesan, "saran": e.saran}, ensure_ascii=False), file=sys.stderr)
        sys.exit(2)
    if a.format == "teks":
        print(teks(hasil))
    else:
        print(json.dumps(hasil, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
