#!/usr/bin/env python3
"""Hitung HPP (harga pokok produksi) per unit, harga jual (margin/markup), dan BEP.

Cocok untuk produk (makanan, fashion, kerajinan) maupun jasa (1 unit = 1 proyek/sesi).

Komponen HPP per unit:
  bahan baku  (resep/BOM, dengan konversi satuan: beli 1 kg, pakai 250 g)
+ tenaga kerja
+ overhead    (listrik, gas, sewa, dll. yang dialokasikan)
+ kemasan
+ penyusutan alat (garis lurus: (harga - nilai sisa) / umur bulan / produksi per bulan)

Setiap biaya punya 'per': 'unit', 'batch' (1x produksi/resep), atau 'bulan'.
  per unit  = biaya                     (biaya variabel)
  per batch = biaya / hasil_per_batch   (biaya variabel)
  per bulan = biaya / produksi_per_bulan (biaya tetap yang dialokasikan)

Harga jual:
  dari target MARGIN  (persen dari harga jual) : harga = HPP / (1 - margin%)
  dari MARKUP         (persen dari HPP)        : harga = HPP x (1 + markup%)
BEP (titik impas) per bulan:
  BEP unit   = biaya tetap bulanan / (harga jual - biaya variabel per unit)   -> dibulatkan ke atas
  BEP rupiah = biaya tetap bulanan / ((harga jual - biaya variabel) / harga jual)

Input: file JSON (disarankan) atau CSV sederhana. Hanya library standar Python 3.8+.

Contoh:
  python3 hitung_hpp.py --file brownies.json
  python3 hitung_hpp.py --file bahan.csv --hasil-per-batch 16 --produksi-per-bulan 400 --margin 40
"""
import argparse
import csv
import json
import re
import sys
from decimal import Decimal, ROUND_CEILING, ROUND_HALF_UP, InvalidOperation

VERSI = "1.0.3"

# ---------------------------------------------------------------- satuan
SATUAN = {
    # massa (dasar gram)
    "mg": ("massa", Decimal("0.001")), "g": ("massa", Decimal(1)), "gr": ("massa", Decimal(1)),
    "gram": ("massa", Decimal(1)), "ons": ("massa", Decimal(100)), "kg": ("massa", Decimal(1000)),
    "kilo": ("massa", Decimal(1000)), "ton": ("massa", Decimal(1000000)),
    # volume (dasar ml)
    "ml": ("volume", Decimal(1)), "cc": ("volume", Decimal(1)), "l": ("volume", Decimal(1000)),
    "liter": ("volume", Decimal(1000)), "ltr": ("volume", Decimal(1000)),
    # panjang (dasar cm)
    "mm": ("panjang", Decimal("0.1")), "cm": ("panjang", Decimal(1)), "m": ("panjang", Decimal(100)),
    "meter": ("panjang", Decimal(100)), "yard": ("panjang", Decimal("91.44")), "yd": ("panjang", Decimal("91.44")),
    "inci": ("panjang", Decimal("2.54")), "inch": ("panjang", Decimal("2.54")),
    # jumlah (dasar pcs)
    "pcs": ("jumlah", Decimal(1)), "pc": ("jumlah", Decimal(1)), "buah": ("jumlah", Decimal(1)),
    "bh": ("jumlah", Decimal(1)), "biji": ("jumlah", Decimal(1)), "butir": ("jumlah", Decimal(1)),
    "lembar": ("jumlah", Decimal(1)), "lbr": ("jumlah", Decimal(1)), "unit": ("jumlah", Decimal(1)),
    "item": ("jumlah", Decimal(1)), "lusin": ("jumlah", Decimal(12)), "kodi": ("jumlah", Decimal(20)),
    "gross": ("jumlah", Decimal(144)), "rim": ("jumlah", Decimal(500)),
}


def faktor_satuan(beli, pakai, nama):
    """Berapa 'satuan pakai' dalam 1 'satuan beli'. Satuan tak dikenal boleh jika sama persis."""
    b, p = str(beli).strip().lower(), str(pakai).strip().lower()
    if b == p:
        return Decimal(1)
    if b not in SATUAN or p not in SATUAN:
        tidak = b if b not in SATUAN else p
        raise ValueError("{}: satuan '{}' tidak dikenal. Pakai g/kg/ons, ml/liter, cm/m/yard, pcs/lusin/kodi, "
                         "atau samakan satuan beli dan satuan pakai (mis. sdm -> ubah ke gram).".format(nama, tidak))
    jb, fb = SATUAN[b]
    jp, fp = SATUAN[p]
    if jb != jp:
        raise ValueError("{}: tidak bisa mengubah {} ({}) ke {} ({}). Isi dengan satuan sejenis, "
                         "mis. timbang dulu berapa gram per ml.".format(nama, b, jb, p, jp))
    return fb / fp


# ---------------------------------------------------------------- angka & format
_PENGALI = [("miliar", 10 ** 9), ("milyar", 10 ** 9), ("juta", 10 ** 6), ("ribu", 10 ** 3),
            ("jt", 10 ** 6), ("rb", 10 ** 3), ("k", 10 ** 3)]


def _cek_ribuan(bagian, asli, nama):
    if not (1 <= len(bagian[0]) <= 3) or any(len(b) != 3 for b in bagian[1:]):
        raise ValueError("{}: '{}' tidak dikenali. Pakai titik untuk ribuan dan koma untuk desimal, "
                         "mis. 1.250.000 atau 1.250.000,50".format(nama, asli))


def parse_angka(nilai, nama="angka"):
    """Baca angka format Indonesia: 'Rp 15.000', '15.000,50', '1,5 jt', '0,25', '15000'."""
    if isinstance(nilai, bool) or nilai is None:
        raise ValueError("{}: nilai kosong atau tidak valid".format(nama))
    if isinstance(nilai, Decimal):
        return nilai
    if isinstance(nilai, int):
        return Decimal(nilai)
    if isinstance(nilai, float):
        return Decimal(str(nilai))
    asli = str(nilai)
    s = asli.strip().lower().replace("\u00a0", "").replace(" ", "")
    s = re.sub(r"^(rp|idr)\.?", "", s)
    s = re.sub(r"[,.]-+$", "", s)
    if s.endswith("%"):
        s = s[:-1]
    pengali = 1
    for akhiran, kali in _PENGALI:
        if s.endswith(akhiran):
            s, pengali = s[: -len(akhiran)], kali
            break
    negatif = s.startswith("-")
    if negatif:
        s = s[1:]
    if not s or not re.fullmatch(r"[\d.,]+", s) or not re.search(r"\d", s):
        raise ValueError("{}: '{}' bukan angka yang valid".format(nama, asli))
    if "," in s and "." in s:
        if s.rfind(",") < s.rfind("."):
            raise ValueError("{}: '{}' memakai format Inggris. Tulis dengan titik untuk ribuan dan koma "
                             "untuk desimal, mis. 1.250.000,50".format(nama, asli))
        utuh, _, desimal = s.rpartition(",")
        _cek_ribuan(utuh.split("."), asli, nama)
        s = utuh.replace(".", "") + "." + desimal
    elif "," in s:
        bagian = s.split(",")
        if len(bagian) == 2:
            s = (bagian[0] or "0") + "." + bagian[1]
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
        raise ValueError("{}: '{}' bukan angka yang valid".format(nama, asli))
    return -d if negatif else d


def format_rp(d, desimal=False):
    d = Decimal(d).quantize(Decimal("0.01") if desimal else Decimal(1), ROUND_HALF_UP)
    neg = d < 0
    d = abs(d)
    teks = "{:,}".format(int(d)).replace(",", ".")
    if desimal:
        pecahan = "{:.2f}".format(d).split(".")[1]
        if pecahan != "00":
            teks += "," + pecahan
    return ("-" if neg else "") + "Rp " + teks


def format_angka(d):
    d = Decimal(d).quantize(Decimal("0.001"), ROUND_HALF_UP).normalize()
    teks = "{:f}".format(d)
    utuh, _, pecahan = teks.partition(".")
    return "{:,}".format(int(utuh)).replace(",", ".") + ("," + pecahan if pecahan else "")


def format_persen(d):
    d = Decimal(d).quantize(Decimal("0.01"), ROUND_HALF_UP).normalize()
    return "{:f}".format(d).replace(".", ",") + "%"


def ke_json(d):
    if isinstance(d, Decimal):
        return int(d) if d == d.to_integral_value() else float(d.quantize(Decimal("0.01"), ROUND_HALF_UP))
    raise TypeError(str(type(d)))


# ---------------------------------------------------------------- perhitungan
KATEGORI = {"bahan": "Bahan baku", "tenaga_kerja": "Tenaga kerja", "overhead": "Overhead",
            "kemasan": "Kemasan", "alat": "Penyusutan alat"}
PER_DEFAULT = {"bahan": "batch", "tenaga_kerja": "batch", "overhead": "batch", "kemasan": "unit"}


def ambil(item, kunci, nama, default=None, wajib=False):
    v = item.get(kunci)
    if v is None or (isinstance(v, str) and not v.strip()):
        if wajib:
            raise ValueError("{}: '{}' wajib diisi".format(nama, kunci))
        return default
    return parse_angka(v, "{} ({})".format(nama, kunci))


def nilai_item(item, kategori, no):
    """Kembalikan (nilai per 'per', per, keterangan cara hitung)."""
    nama = str(item.get("nama") or "{} ke-{}".format(KATEGORI[kategori], no))
    per = str(item.get("per") or PER_DEFAULT[kategori]).strip().lower()
    if per not in ("unit", "batch", "bulan"):
        raise ValueError("{}: 'per' harus unit, batch, atau bulan (bukan '{}')".format(nama, per))
    if item.get("biaya") not in (None, ""):
        nilai = ambil(item, "biaya", nama)
        ket = "biaya langsung"
    elif item.get("upah_per_jam") not in (None, ""):
        upah = ambil(item, "upah_per_jam", nama)
        jam = ambil(item, "jam", nama, wajib=True)
        nilai = upah * jam
        ket = "{}/jam x {} jam".format(format_rp(upah, True), format_angka(jam))
    elif item.get("harga_beli") not in (None, ""):
        harga = ambil(item, "harga_beli", nama)
        isi = ambil(item, "isi_beli", nama, Decimal(1))
        pakai = ambil(item, "pakai", nama, wajib=True)
        sb = item.get("satuan_beli") or item.get("satuan_pakai") or "pcs"
        sp = item.get("satuan_pakai") or sb
        if isi <= 0:
            raise ValueError("{}: isi_beli harus lebih dari 0".format(nama))
        faktor = faktor_satuan(sb, sp, nama)
        nilai = harga / (isi * faktor) * pakai
        ket = "{} / {} {} x pakai {} {}".format(format_rp(harga, True), format_angka(isi), sb,
                                                 format_angka(pakai), sp)
        if pakai < 0:
            raise ValueError("{}: jumlah pakai tidak boleh negatif".format(nama))
    else:
        raise ValueError("{}: isi 'biaya', atau 'harga_beli' + 'pakai', atau 'upah_per_jam' + 'jam'".format(nama))
    if nilai < 0:
        raise ValueError("{}: biaya tidak boleh negatif".format(nama))
    return nama, nilai, per, ket


def hitung(d):
    hasil_batch = ambil(d, "hasil_per_batch", "hasil_per_batch", Decimal(1))
    if hasil_batch <= 0:
        raise ValueError("hasil_per_batch harus lebih dari 0")
    produksi = ambil(d, "produksi_per_bulan", "produksi_per_bulan")
    if produksi is not None and produksi <= 0:
        raise ValueError("produksi_per_bulan harus lebih dari 0")
    susut = ambil(d, "susut_bahan_persen", "susut_bahan_persen", Decimal(0))
    if not 0 <= susut < 100:
        raise ValueError("susut_bahan_persen harus 0 sampai di bawah 100")

    rincian = []
    variabel = Decimal(0)
    tetap_bulanan_hpp = Decimal(0)
    per_kategori = {k: Decimal(0) for k in KATEGORI}

    def butuh_produksi(nama):
        if produksi is None:
            raise ValueError("{} dihitung per bulan, jadi 'produksi_per_bulan' (jumlah unit per bulan) wajib diisi"
                             .format(nama))
        return produksi

    for kategori in ("bahan", "tenaga_kerja", "overhead", "kemasan"):
        daftar = d.get(kategori) or []
        if not isinstance(daftar, list):
            raise ValueError("'{}' harus berupa daftar".format(kategori))
        for no, item in enumerate(daftar, 1):
            if not isinstance(item, dict):
                raise ValueError("{} ke-{} harus berupa objek".format(KATEGORI[kategori], no))
            nama, nilai, per, ket = nilai_item(item, kategori, no)
            if kategori == "bahan" and susut:
                nilai = nilai * (1 + susut / 100)
                ket += " + susut {}".format(format_persen(susut))
            if per == "unit":
                per_unit = nilai
            elif per == "batch":
                per_unit = nilai / hasil_batch
            else:
                per_unit = nilai / butuh_produksi(nama)
                tetap_bulanan_hpp += nilai
            if per != "bulan":
                variabel += per_unit
            per_kategori[kategori] += per_unit
            rincian.append({"kategori": KATEGORI[kategori], "nama": nama, "cara_hitung": ket, "per": per,
                            "biaya_per_periode": nilai, "biaya_per_unit": per_unit,
                            "jenis_biaya": "tetap" if per == "bulan" else "variabel"})

    penyusutan_bulanan = Decimal(0)
    for no, item in enumerate(d.get("alat") or [], 1):
        if not isinstance(item, dict):
            raise ValueError("alat ke-{} harus berupa objek".format(no))
        nama = str(item.get("nama") or "Alat ke-{}".format(no))
        harga = ambil(item, "harga", nama)
        if harga is None:
            harga = ambil(item, "harga_beli", nama, wajib=True)
        umur = ambil(item, "umur_bulan", nama, wajib=True)
        sisa = ambil(item, "nilai_sisa", nama, Decimal(0))
        if umur <= 0:
            raise ValueError("{}: umur_bulan harus lebih dari 0".format(nama))
        if harga < 0 or sisa < 0 or sisa > harga:
            raise ValueError("{}: harga/nilai sisa tidak valid (nilai sisa harus 0 s.d. harga)".format(nama))
        per_bulan = (harga - sisa) / umur
        penyusutan_bulanan += per_bulan
        per_unit = per_bulan / butuh_produksi(nama)
        per_kategori["alat"] += per_unit
        rincian.append({"kategori": KATEGORI["alat"], "nama": nama,
                        "cara_hitung": "({} - sisa {}) / {} bulan".format(format_rp(harga), format_rp(sisa),
                                                                        format_angka(umur)),
                        "per": "bulan", "biaya_per_periode": per_bulan, "biaya_per_unit": per_unit,
                        "jenis_biaya": "tetap"})

    tetap_lain = Decimal(0)
    daftar_tetap_lain = []
    for no, item in enumerate(d.get("biaya_tetap_lain") or [], 1):
        if not isinstance(item, dict):
            raise ValueError("biaya_tetap_lain ke-{} harus berupa objek".format(no))
        nama = str(item.get("nama") or "Biaya tetap ke-{}".format(no))
        nilai = ambil(item, "biaya", nama, wajib=True)
        if nilai < 0:
            raise ValueError("{}: biaya tidak boleh negatif".format(nama))
        tetap_lain += nilai
        daftar_tetap_lain.append({"nama": nama, "biaya_bulanan": nilai})

    if not rincian:
        raise ValueError("belum ada komponen biaya. Isi minimal 'bahan' (atau 'tenaga_kerja' untuk jasa).")

    hpp = sum(per_kategori.values(), Decimal(0))
    biaya_tetap_bulanan = tetap_bulanan_hpp + penyusutan_bulanan + tetap_lain
    porsi = None
    if hpp > 0:
        urut_kat = sorted(((KATEGORI[k], v) for k, v in per_kategori.items() if v), key=lambda x: -x[1])
        terbesar = max(rincian, key=lambda r: r["biaya_per_unit"])
        porsi = {
            "per_kategori": [{"kategori": k, "per_unit": v, "persen_hpp": v / hpp * 100} for k, v in urut_kat],
            "variabel_per_unit": variabel, "variabel_persen_hpp": variabel / hpp * 100,
            "tetap_per_unit": hpp - variabel, "tetap_persen_hpp": (hpp - variabel) / hpp * 100,
            "komponen_terbesar": {"nama": terbesar["nama"], "kategori": terbesar["kategori"],
                                  "per_unit": terbesar["biaya_per_unit"],
                                  "persen_hpp": terbesar["biaya_per_unit"] / hpp * 100},
        }
    return {
        "nama_produk": d.get("nama_produk") or "Produk",
        "jenis": d.get("jenis") or "produk",
        "satuan_produk": d.get("satuan_produk") or "unit",
        "hasil_per_batch": hasil_batch,
        "produksi_per_bulan": produksi,
        "susut_bahan_persen": susut,
        "rincian": rincian,
        "per_kategori": {KATEGORI[k]: v for k, v in per_kategori.items()},
        "hpp_per_unit": hpp,
        "biaya_variabel_per_unit": variabel,
        "biaya_tetap_dialokasikan_per_unit": hpp - variabel,
        "biaya_tetap_lain": daftar_tetap_lain,
        "porsi_biaya": porsi,
        "biaya_tetap_bulanan": {
            "dari_hpp_per_bulan": tetap_bulanan_hpp,
            "penyusutan": penyusutan_bulanan,
            "lain_di_luar_hpp": tetap_lain,
            "total": biaya_tetap_bulanan,
        },
    }


def bulatkan_atas(nilai, kelipatan):
    return (Decimal(nilai) / kelipatan).quantize(Decimal(1), ROUND_CEILING) * kelipatan


def analisis_harga(h, harga):
    hpp = h["hpp_per_unit"]
    laba = harga - hpp
    return {"harga": harga, "laba_per_unit": laba,
            "margin_persen": laba / harga * 100 if harga > 0 else None,
            "markup_persen": laba / hpp * 100 if hpp > 0 else None}


def hitung_bep(h, harga):
    tetap = h["biaya_tetap_bulanan"]["total"]
    kontribusi = harga - h["biaya_variabel_per_unit"]
    if tetap == 0:
        return {"status": "tanpa_biaya_tetap", "biaya_tetap_bulanan": tetap, "margin_kontribusi_per_unit": kontribusi}
    if kontribusi <= 0:
        return {"status": "tidak_tercapai", "biaya_tetap_bulanan": tetap, "margin_kontribusi_per_unit": kontribusi}
    unit_tepat = tetap / kontribusi
    rupiah = (tetap / (kontribusi / harga)).quantize(Decimal(1), ROUND_CEILING)
    hasil = {"status": "ok", "biaya_tetap_bulanan": tetap, "margin_kontribusi_per_unit": kontribusi,
             "bep_unit_tepat": unit_tepat.quantize(Decimal("0.01"), ROUND_HALF_UP),
             "bep_unit": unit_tepat.quantize(Decimal(1), ROUND_CEILING), "bep_rupiah": rupiah}
    if h["produksi_per_bulan"]:
        hasil["persen_dari_produksi"] = unit_tepat / h["produksi_per_bulan"] * 100
    return hasil


def susun_harga(h, d):
    kelipatan = ambil(d, "bulatkan", "bulatkan", Decimal(500))
    if kelipatan < 1 or kelipatan != kelipatan.to_integral_value():
        raise ValueError("bulatkan harus bilangan bulat >= 1")
    hpp = h["hpp_per_unit"]
    margin = ambil(d, "target_margin_persen", "target_margin_persen")
    markup = ambil(d, "markup_persen", "markup_persen")
    harga_jual = ambil(d, "harga_jual", "harga_jual")
    if margin is not None and markup is not None:
        raise ValueError("pilih salah satu: target_margin_persen ATAU markup_persen")
    out = {"kelipatan_pembulatan": kelipatan}
    if margin is not None:
        if not 0 <= margin < 100:
            raise ValueError("target margin harus 0 sampai di bawah 100%")
        tepat = hpp / (1 - margin / 100)
        out["metode"] = {"jenis": "margin", "persen": margin, "harga_tepat": tepat,
                         "setara_markup_persen": margin / (100 - margin) * 100}
    elif markup is not None:
        if markup < 0:
            raise ValueError("markup tidak boleh negatif")
        tepat = hpp * (1 + markup / 100)
        out["metode"] = {"jenis": "markup", "persen": markup, "harga_tepat": tepat,
                         "setara_margin_persen": markup / (100 + markup) * 100}
    else:
        tepat = None
    if tepat is not None:
        rek = bulatkan_atas(tepat, kelipatan)
        out["harga_rekomendasi"] = analisis_harga(h, rek)
    if harga_jual is not None:
        if harga_jual <= 0:
            raise ValueError("harga_jual harus lebih dari 0")
        out["harga_saat_ini"] = analisis_harga(h, harga_jual)
    if tepat is None and harga_jual is None:
        out["pilihan_margin"] = []
        for m in (Decimal(20), Decimal(30), Decimal(40), Decimal(50)):
            harga = bulatkan_atas(hpp / (1 - m / 100), kelipatan)
            a = analisis_harga(h, harga)
            a["target_margin_persen"] = m
            a["bep"] = hitung_bep(h, harga)
            out["pilihan_margin"].append(a)
    banding = d.get("banding_harga")
    if banding not in (None, "", []):
        if isinstance(banding, (str, int, float, Decimal)) and not isinstance(banding, bool):
            banding = [b for b in re.split(r"[;/|]|,\s+|(?<![A-Za-z.])\s+(?=\d)", str(banding)) if b.strip()] \
                if isinstance(banding, str) else [banding]
        if not isinstance(banding, list):
            raise ValueError("banding_harga harus daftar harga, mis. [18000, 19500]")
        out["banding_harga"] = []
        for no, b in enumerate(banding, 1):
            harga = parse_angka(b, "banding_harga ke-{}".format(no))
            if harga <= 0:
                raise ValueError("banding_harga ke-{} harus lebih dari 0".format(no))
            a = analisis_harga(h, harga)
            a["bep"] = hitung_bep(h, harga)
            out["banding_harga"].append(a)
    # BEP memakai harga saat ini jika ada, jika tidak harga rekomendasi
    acuan = out.get("harga_saat_ini") or out.get("harga_rekomendasi")
    if acuan:
        out["bep"] = hitung_bep(h, acuan["harga"])
        out["bep"]["harga_acuan"] = acuan["harga"]
    return out


# ---------------------------------------------------------------- input CSV
def baca_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        isi = f.read()
    if not isi.strip():
        raise ValueError("file '{}' kosong".format(path))
    try:
        dialek = csv.Sniffer().sniff(isi[:2048], delimiters=";,\t|")
    except csv.Error:
        dialek = csv.excel
    rows = list(csv.DictReader(isi.splitlines(), dialect=dialek))
    if not rows or "kategori" not in [re.sub(r"\s+", "_", (k or "").strip().lower()) for k in rows[0]]:
        raise ValueError("CSV wajib punya kolom 'kategori' (bahan/tenaga_kerja/overhead/kemasan/alat/biaya_tetap_lain). "
                         "Lihat templates/contoh-hpp.csv")
    d = {}
    alias = {"tenaga": "tenaga_kerja", "tenaga_kerja": "tenaga_kerja", "tk": "tenaga_kerja", "bahan": "bahan",
             "bahan_baku": "bahan", "overhead": "overhead", "kemasan": "kemasan", "packaging": "kemasan",
             "alat": "alat", "penyusutan": "alat", "biaya_tetap": "biaya_tetap_lain",
             "biaya_tetap_lain": "biaya_tetap_lain"}
    for no, r in enumerate(rows, 2):
        item = {re.sub(r"\s+", "_", (k or "").strip().lower()): (v or "").strip() for k, v in r.items() if k}
        kat = re.sub(r"\s+", "_", item.pop("kategori", "").lower())
        if not kat:
            continue
        if kat not in alias:
            raise ValueError("baris {}: kategori '{}' tidak dikenal".format(no, kat))
        d.setdefault(alias[kat], []).append({k: v for k, v in item.items() if v != ""})
    return d


# ---------------------------------------------------------------- output teks
def teks(h, hg):
    s = h["satuan_produk"]
    out = ["## HPP {} (per {})".format(h["nama_produk"], s), ""]
    info = "Hasil per batch: {} {}".format(format_angka(h["hasil_per_batch"]), s)
    if h["produksi_per_bulan"]:
        info += " | Produksi per bulan: {} {}".format(format_angka(h["produksi_per_bulan"]), s)
    out += [info, "", "| Kategori | Komponen | Cara hitung | Biaya | Per {} |".format(s), "|---|---|---|---:|---:|"]
    for r in h["rincian"]:
        out.append("| {} | {} | {} | {} /{} | {} |".format(
            r["kategori"], r["nama"], r["cara_hitung"], format_rp(r["biaya_per_periode"], True), r["per"],
            format_rp(r["biaya_per_unit"], True)))
    out += ["", "**Ringkasan HPP per {}**".format(s), ""]
    for k, v in h["per_kategori"].items():
        if v:
            out.append("- {}: {}".format(k, format_rp(v, True)))
    out.append("- **HPP per {}: {}**".format(s, format_rp(h["hpp_per_unit"], True)))
    out.append("  - biaya variabel {} + biaya tetap dialokasikan {}".format(
        format_rp(h["biaya_variabel_per_unit"], True), format_rp(h["biaya_tetap_dialokasikan_per_unit"], True)))
    pr = h.get("porsi_biaya")
    if pr:
        out += ["", "**Porsi biaya dalam HPP** (urut dari terbesar)", ""]
        for k in pr["per_kategori"]:
            out.append("- {}: {} ({} dari HPP)".format(k["kategori"], format_rp(k["per_unit"], True),
                                                     format_persen(k["persen_hpp"])))
        out.append("- Biaya variabel (habis per unit/batch): {} ({}); biaya tetap bulanan yang dialokasikan: {} ({})"
                   .format(format_rp(pr["variabel_per_unit"], True), format_persen(pr["variabel_persen_hpp"]),
                           format_rp(pr["tetap_per_unit"], True), format_persen(pr["tetap_persen_hpp"])))
        t = pr["komponen_terbesar"]
        out.append("- Komponen tunggal terbesar: {} ({}) {} per {} ({} dari HPP)".format(
            t["nama"], t["kategori"], format_rp(t["per_unit"], True), s, format_persen(t["persen_hpp"])))
    out.append("")
    out.append("**Harga jual** (dibulatkan ke atas kelipatan {})".format(format_rp(hg["kelipatan_pembulatan"])))
    out.append("")
    m = hg.get("metode")
    if m:
        if m["jenis"] == "margin":
            out.append("- Target margin {} -> harga = HPP / (1 - {}) = {} (setara markup {})".format(
                format_persen(m["persen"]), format_persen(m["persen"]), format_rp(m["harga_tepat"], True),
                format_persen(m["setara_markup_persen"])))
        else:
            out.append("- Markup {} -> harga = HPP x (1 + {}) = {} (setara margin {})".format(
                format_persen(m["persen"]), format_persen(m["persen"]), format_rp(m["harga_tepat"], True),
                format_persen(m["setara_margin_persen"])))
        r = hg["harga_rekomendasi"]
        out.append("- **Harga rekomendasi: {}** -> laba kotor {} per {} (margin {}, markup {})".format(
            format_rp(r["harga"]), format_rp(r["laba_per_unit"], True), s,
            format_persen(r["margin_persen"]) if r["margin_persen"] is not None else "-",
            format_persen(r["markup_persen"]) if r["markup_persen"] is not None else "-"))
    if hg.get("harga_saat_ini"):
        r = hg["harga_saat_ini"]
        out.append("- Harga saat ini {}: laba kotor {} per {} (margin {}, markup {}){}".format(
            format_rp(r["harga"], True), format_rp(r["laba_per_unit"], True), s,
            format_persen(r["margin_persen"]), format_persen(r["markup_persen"]) if r["markup_persen"] is not None else "-",
            " - RUGI!" if r["laba_per_unit"] < 0 else ""))
    if hg.get("pilihan_margin"):
        out += ["Target margin belum ditentukan. Pilihan harga:", "",
                "| Target margin | Harga jual | Laba kotor per {} | Markup setara | BEP per bulan |".format(s),
                "|---:|---:|---:|---:|---:|"]
        for r in hg["pilihan_margin"]:
            b = r["bep"]
            bep = ("{} {}".format(format_angka(b["bep_unit"]), s) if b["status"] == "ok"
                   else "tanpa biaya tetap" if b["status"] == "tanpa_biaya_tetap" else "tidak tercapai")
            out.append("| {} | {} | {} | {} | {} |".format(
                format_persen(r["target_margin_persen"]), format_rp(r["harga"]), format_rp(r["laba_per_unit"], True),
                format_persen(r["markup_persen"]) if r["markup_persen"] is not None else "-", bep))
    if hg.get("banding_harga"):
        out += ["", "**Banding harga yang dibahas** (dihitung script)", "",
                "| Harga jual | Laba kotor per {} | Margin | Markup | BEP per bulan | BEP % rencana produksi |".format(s),
                "|---:|---:|---:|---:|---:|---:|"]
        for r in hg["banding_harga"]:
            b = r["bep"]
            if b["status"] == "ok":
                bep = "{} {} (tepatnya {})".format(format_angka(b["bep_unit"]), s, format_angka(b["bep_unit_tepat"]))
                persen = format_persen(b["persen_dari_produksi"]) if "persen_dari_produksi" in b else "-"
            else:
                bep = "tanpa biaya tetap" if b["status"] == "tanpa_biaya_tetap" else "tidak tercapai"
                persen = "-"
            out.append("| {} | {} | {} | {} | {} | {} |".format(
                format_rp(r["harga"], True), format_rp(r["laba_per_unit"], True),
                format_persen(r["margin_persen"]),
                format_persen(r["markup_persen"]) if r["markup_persen"] is not None else "-", bep, persen))
    b = hg.get("bep")
    t = h["biaya_tetap_bulanan"]
    if b:
        out += ["", "**Titik impas (BEP) per bulan** pada harga {}".format(format_rp(b["harga_acuan"], True)), ""]
        out.append("- Biaya tetap bulanan: {} (biaya bulanan dalam HPP {} + penyusutan {} + biaya tetap lain {})".format(
            format_rp(t["total"], True), format_rp(t["dari_hpp_per_bulan"], True), format_rp(t["penyusutan"], True),
            format_rp(t["lain_di_luar_hpp"], True)))
        out.append("- Margin kontribusi per {}: {} (harga - biaya variabel {})".format(
            s, format_rp(b["margin_kontribusi_per_unit"], True), format_rp(h["biaya_variabel_per_unit"], True)))
        if b["status"] == "ok":
            out.append("- **BEP: {} {} per bulan** (tepatnya {}), atau omzet **{}** per bulan".format(
                format_angka(b["bep_unit"]), s, format_angka(b["bep_unit_tepat"]), format_rp(b["bep_rupiah"])))
            if "persen_dari_produksi" in b:
                out.append("- BEP = {} dari rencana produksi {} {}".format(
                    format_persen(b["persen_dari_produksi"]), format_angka(h["produksi_per_bulan"]), s))
                if b["persen_dari_produksi"] > 100:
                    out.append("- PERHATIAN: BEP melebihi rencana produksi. Pada volume ini usaha masih rugi; "
                               "naikkan harga, tambah volume, atau tekan biaya tetap.")
        elif b["status"] == "tidak_tercapai":
            out.append("- BEP TIDAK TERCAPAI: harga jual tidak menutup biaya variabel. Naikkan harga atau tekan biaya.")
        else:
            out.append("- Tidak ada biaya tetap bulanan, jadi setiap penjualan di atas biaya variabel langsung untung.")
    return "\n".join(out)


class ParserID(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write("ERROR: argumen tidak valid ({}).\nLihat bantuan: python3 hitung_hpp.py --help\n"
                         .format(message))
        sys.exit(2)


def main(argv=None):
    p = ParserID(description="Hitung HPP per unit, harga jual (margin/markup), dan BEP.")
    p.add_argument("--file", required=True, help="File JSON (disarankan) atau CSV berisi komponen biaya")
    p.add_argument("--nama-produk")
    p.add_argument("--satuan-produk", help="mis. pcs, loyang, kemeja, sesi")
    p.add_argument("--hasil-per-batch", help="Jumlah unit jadi per 1x produksi/resep")
    p.add_argument("--produksi-per-bulan", help="Jumlah unit yang dibuat/dijual per bulan")
    p.add_argument("--susut", help="Cadangan bahan terbuang/susut (%%)")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--margin", help="Target margin %% dari harga jual")
    g.add_argument("--markup", help="Markup %% dari HPP")
    p.add_argument("--harga-jual", help="Harga jual saat ini (untuk cek laba & BEP)")
    p.add_argument("--banding-harga", help="Daftar harga yang ingin dibandingkan, dipisah ';' atau spasi, "
                                           "mis. \"18000;19500\" (laba, margin, BEP tiap harga)")
    p.add_argument("--bulatkan", help="Kelipatan pembulatan ke atas harga rekomendasi (default 500)")
    p.add_argument("--format", choices=["teks", "json"], default="teks")
    a = p.parse_args(argv)

    try:
        if a.file.lower().endswith(".csv"):
            d = baca_csv(a.file)
        else:
            try:
                with open(a.file, encoding="utf-8-sig") as f:
                    d = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError("JSON tidak valid (baris {}, kolom {}): {}".format(e.lineno, e.colno, e.msg))
            if not isinstance(d, dict):
                raise ValueError("isi JSON harus berupa objek {...}. Lihat templates/contoh-hpp.json")
        for kunci, nilai in (("nama_produk", a.nama_produk), ("satuan_produk", a.satuan_produk),
                             ("hasil_per_batch", a.hasil_per_batch), ("produksi_per_bulan", a.produksi_per_bulan),
                             ("susut_bahan_persen", a.susut), ("harga_jual", a.harga_jual), ("bulatkan", a.bulatkan),
                             ("banding_harga", a.banding_harga)):
            if nilai is not None:
                d[kunci] = nilai
        if a.margin is not None:
            d["target_margin_persen"], d["markup_persen"] = a.margin, None
        if a.markup is not None:
            d["markup_persen"], d["target_margin_persen"] = a.markup, None
        h = hitung(d)
        hg = susun_harga(h, d)
    except OSError as e:
        sys.stderr.write("ERROR: file '{}' tidak bisa dibaca: {}\n".format(a.file, e.strerror or e))
        return 2
    except ValueError as e:
        sys.stderr.write("ERROR: {}\n".format(e))
        return 2

    catatan = [
        "HPP ditampilkan sampai 2 angka desimal; harga rekomendasi dibulatkan KE ATAS ke kelipatan {} "
        "agar margin tidak kurang dari target.".format(format_rp(hg["kelipatan_pembulatan"])),
        "Biaya 'per bulan' dan penyusutan dibagi ke produksi per bulan. Jika penjualan lebih sedikit dari itu, "
        "HPP per unit sebenarnya naik.",
        "Margin = laba / harga jual. Markup = laba / HPP. Margin 30% setara markup 42,86%.",
        "'Laba kotor' = harga jual - HPP per unit. Angka ini BELUM dikurangi biaya tetap lain di luar HPP "
        "(mis. admin, internet, marketing) dan belum dikurangi pajak; biaya tetap lain sudah diperhitungkan di BEP.",
    ]
    if not (d.get("tenaga_kerja") or []):
        catatan.insert(0, "Upah/gaji pemilik dan tenaga kerja BELUM dihitung (tidak ada data tenaga kerja). Jika Anda "
                          "mengerjakan sendiri, masukkan upah wajar per jam agar HPP tidak terlalu rendah.")
    if a.format == "json":
        print(json.dumps({"hpp": h, "harga": hg, "catatan": catatan}, default=ke_json, ensure_ascii=False, indent=2))
    else:
        print(teks(h, hg))
        print("")
        print("**Catatan**")
        for c in catatan:
            print("- " + c)
    return 0


if __name__ == "__main__":
    sys.exit(main())
