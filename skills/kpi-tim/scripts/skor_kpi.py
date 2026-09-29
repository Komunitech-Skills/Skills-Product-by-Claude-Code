#!/usr/bin/env python3
"""skor_kpi.py -- KPI & target tim untuk UMKM (Komunitech, kpi-tim).

Hanya library standar Python 3.8+. Tidak butuh internet, akun, atau API key.
Semua data dibaca dari file lokal (CSV / XLSX ekspor Excel/Google Sheets) dan
hasil hanya ditulis ke layar atau ke file yang diminta.

Perintah:
  katalog     Daftar KPI bawaan per peran (sales, cs, produksi, gudang, keuangan,
              marketing, admin, kurir, kasir).
  template    Buat rencana KPI (CSV + XLSX) dan lembar realisasi kosong dari daftar tim.
  cek         Periksa rencana KPI (bobot = 100, target, arah, ambang).
  baca-teks   Ubah teks laporan grup WA ("Andi closing 12 deal, target 15") menjadi
              DRAF baris realisasi yang WAJIB dikonfirmasi pengguna.
  skor        Hitung capaian, skor tertimbang per orang/divisi/perusahaan, status,
              dan tren dibanding periode sebelumnya.
  rekap-log   Rekap log operasional harian (komplain, respons CS, pengiriman, produksi)
              menjadi baris realisasi (jumlah / rata-rata / persen ya).
  ekspor-db   Tulis rencana + skor + riwayat semua periode ke kpi.db (SQLite lokal, dibaca
              dasbor-lokal/Datasette read-only) + kpi-metadata.yml; --anonim (kode P01..),
              --grist (CSV per tabel untuk Grist).
  okr         Hitung progres OKR ringan (objective + 2-4 key result, 0-1,0).

Aturan hitung lengkap: references/aturan-skor.md. Ringkas:
  arah naik : capaian = realisasi / target x 100
  arah turun: capaian = (2 - realisasi / target) x 100   (target > 0)
              target = 0 -> 100 jika realisasi 0, selain itu 0   (aturan "nol kejadian")
  capaian dibatasi 0 .. maks_capai (default 120).
  skor orang = jumlah(bobot x capaian) / jumlah(bobot)   (bobot wajib total 100)
  Semua dihitung dengan Decimal; dibulatkan SEKALI saat ditampilkan (1 desimal, half-up).

Exit code: 0 = berhasil, 1 = input/validasi gagal (lihat pesan).
"""
import argparse
import csv
import datetime
import difflib
import io
import json
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from pathlib import Path
from xml.sax.saxutils import escape

VERSI = "1.1.0"
D0 = Decimal(0)
D100 = Decimal(100)


class Gagal(Exception):
    """Kesalahan input yang dijelaskan dengan bahasa awam."""


# ---------------------------------------------------------------------------
# Katalog KPI bawaan (ringkas). Versi lengkap + penjelasan: references/katalog-kpi.md
# (kpi, satuan, arah, bobot usulan, target contoh, kata kunci teks WA, sumber data)
# ---------------------------------------------------------------------------
KATALOG = {
    "sales": [
        ("Omzet penjualan", "Rp", "naik", 40, 150000000, "omzet;penjualan;jualan;sales", "kasir-lokal / rekap-penjualan-csv / crm-wa"),
        ("Jumlah closing", "deal", "naik", 25, 15, "closing;deal;closingan", "crm-wa (rekap tahap deal)"),
        ("Konversi prospek", "%", "naik", 20, 25, "konversi;conversion", "crm-wa (deal / prospek baru x 100)"),
        ("Follow-up tepat waktu", "%", "naik", 15, 90, "follow-up;follow up;fu", "crm-wa (hari-ini / terlambat)"),
    ],
    "cs": [
        ("Waktu respons pertama", "menit", "turun", 30, 10, "respons;respon;balas;response", "catatan chat CS / agen-cs-toko"),
        ("Komplain selesai <=2 hari", "%", "naik", 30, 90, "komplain selesai;selesai;resolved", "log komplain (templates/log-operasional.csv)"),
        ("Rating kepuasan", "skala 1-5", "naik", 25, 4.7, "rating;bintang;kepuasan;ulasan", "analisis-ulasan / ulasan marketplace"),
        ("Chat terjawab hari yang sama", "%", "naik", 15, 95, "terjawab;chat", "catatan chat CS"),
    ],
    "produksi": [
        ("Output produksi", "unit", "naik", 35, 5000, "output;produksi;hasil;unit", "catatan produksi harian (log-operasional.csv)"),
        ("Tingkat reject", "%", "turun", 30, 2, "reject;cacat;rusak;afkir", "catatan QC (reject / output x 100)"),
        ("Produksi tepat jadwal", "%", "naik", 20, 95, "tepat jadwal;on time;jadwal", "jadwal produksi vs realisasi"),
        ("Kecelakaan kerja", "kejadian", "turun", 15, 0, "kecelakaan;insiden;cedera", "laporan-insiden-usaha"),
    ],
    "gudang": [
        ("Akurasi stok", "%", "naik", 35, 99, "akurasi;opname;selisih stok", "buku-stok (stock opname)"),
        ("Pesanan dikemas hari yang sama", "%", "naik", 30, 95, "dikemas;packing;kemas;packing hari", "buku-stok impor-pesanan / resi-picking"),
        ("Salah kirim", "pesanan", "turun", 20, 3, "salah kirim;salah ambil;salah barang", "log komplain / retur"),
        ("Item stok habis", "SKU", "turun", 15, 5, "stok habis;kosong;out of stock", "buku-stok laporan menipis"),
    ],
    "keuangan": [
        ("Hari tutup buku", "hari", "turun", 30, 5, "tutup buku;closing buku;laporan bulanan", "laporan-keuangan-emkm / hledger-usaha"),
        ("Piutang lewat 30 hari", "%", "turun", 30, 10, "piutang;overdue;macet", "buku-piutang (umur piutang)"),
        ("Tagihan terkirim tepat waktu", "%", "naik", 20, 95, "tagihan;invoice;faktur", "buat-invoice / buku-piutang"),
        ("Selisih kas", "Rp", "turun", 20, 50000, "selisih kas;selisih", "kas-umkm (opname)"),
    ],
    "marketing": [
        ("Leads masuk", "lead", "naik", 30, 300, "lead;leads;prospek masuk;chat masuk", "crm-wa (sumber lead) / laporan-iklan-mingguan"),
        ("Biaya per lead", "Rp", "turun", 25, 15000, "cpl;biaya per lead;cost per lead", "laporan-iklan-mingguan"),
        ("ROAS", "x", "naik", 25, 4, "roas", "laporan-iklan-mingguan"),
        ("Konten terbit sesuai kalender", "%", "naik", 20, 90, "konten;posting;upload", "kalender-konten-30hari / konten-mingguan"),
    ],
    "admin": [
        ("Tugas selesai tepat waktu", "%", "naik", 40, 90, "tugas;selesai tepat;deadline", "vikunja-tugas / notulen-rapat"),
        ("Kesalahan input data", "kesalahan", "turun", 30, 3, "salah input;kesalahan input;typo", "pengecekan admin / absensi-lokal (PERLU DICEK)"),
        ("Nota diarsip lengkap", "%", "naik", 15, 95, "nota;arsip;dokumen", "arsip-nota"),
        ("Kehadiran tepat waktu", "%", "naik", 15, 95, "hadir;kehadiran;tepat waktu;telat", "absensi-lokal (rekap)"),
    ],
    "kurir": [
        ("Pengiriman tepat waktu", "%", "naik", 40, 95, "tepat waktu;on time;terkirim tepat", "catatan pengiriman (log-operasional.csv)"),
        ("Paket gagal kirim", "%", "turun", 25, 3, "gagal kirim;retur;gagal", "catatan pengiriman"),
        ("Jumlah pengiriman", "paket", "naik", 20, 600, "kirim;paket;antar;drop", "catatan pengiriman / resi-picking"),
        ("Setoran COD pas", "%", "naik", 15, 100, "cod;setoran", "kas-umkm"),
    ],
    "kasir": [
        ("Hari tanpa selisih kas", "%", "naik", 35, 95, "selisih kas;tanpa selisih;kas pas", "kasir-lokal (tutup-kasir)"),
        ("Transaksi per shift", "transaksi", "naik", 25, 80, "transaksi;struk;nota", "kasir-lokal (rekap)"),
        ("Void tanpa alasan sah", "kali", "turun", 20, 2, "void;batal;retur", "kasir-lokal (void/retur)"),
        ("Kehadiran tepat waktu", "%", "naik", 20, 95, "hadir;kehadiran;tepat waktu;telat", "absensi-lokal (rekap)"),
    ],
}
ALIAS_PERAN = {
    "penjualan": "sales", "marketing sales": "sales", "salesman": "sales", "sales lapangan": "sales",
    "customer service": "cs", "layanan pelanggan": "cs", "admin chat": "cs", "admin cs": "cs",
    "pabrik": "produksi", "operator": "produksi", "operator produksi": "produksi",
    "warehouse": "gudang", "logistik": "gudang", "staf gudang": "gudang",
    "finance": "keuangan", "akuntansi": "keuangan", "accounting": "keuangan",
    "pemasaran": "marketing", "digital marketing": "marketing", "iklan": "marketing",
    "administrasi": "admin", "staf admin": "admin",
    "driver": "kurir", "pengirim": "kurir", "sopir": "kurir",
    "cashier": "kasir", "kasir toko": "kasir",
}

ARAH = {
    "naik": "naik", "tinggi": "naik", "lebih tinggi": "naik", "semakin tinggi": "naik",
    "higher": "naik", "up": "naik", "max": "naik", "maks": "naik", "maximize": "naik", "↑": "naik",
    "turun": "turun", "rendah": "turun", "lebih rendah": "turun", "semakin rendah": "turun",
    "lower": "turun", "down": "turun", "min": "turun", "minimize": "turun", "↓": "turun",
}

KOLOM_ALIAS = {
    "nama": "orang", "karyawan": "orang", "pegawai": "orang", "staf": "orang", "pic": "orang",
    "orang": "orang", "person": "orang", "name": "orang",
    "divisi": "divisi", "bagian": "divisi", "departemen": "divisi", "tim": "divisi", "division": "divisi",
    "kpi": "kpi", "indikator": "kpi", "nama_kpi": "kpi", "key_result": "key_result", "kr": "key_result",
    "satuan": "satuan", "unit": "satuan",
    "arah": "arah", "polaritas": "arah", "direction": "arah",
    "bobot": "bobot", "bobot_%": "bobot", "bobot_(%)": "bobot", "weight": "bobot",
    "target": "target",
    "ambang": "ambang", "batas_minimal": "ambang", "batas_min": "ambang", "batas_maks": "ambang", "threshold": "ambang",
    "maks_capai": "maks_capai", "cap": "maks_capai", "batas_capaian": "maks_capai",
    "periode": "periode", "bulan": "periode", "minggu": "periode", "period": "periode",
    "kata_kunci": "kata_kunci", "keyword": "kata_kunci",
    "sumber": "sumber", "sumber_data": "sumber",
    "realisasi": "realisasi", "aktual": "realisasi", "actual": "realisasi", "hasil": "realisasi",
    "catatan": "catatan", "keterangan": "catatan",
    "peran": "peran", "jabatan": "peran", "posisi": "peran", "role": "peran",
    "pemilik": "pemilik", "owner": "pemilik", "objective": "objective", "tujuan": "objective",
    "awal": "awal", "baseline": "awal", "sekarang": "sekarang", "saat_ini": "sekarang", "current": "sekarang",
    "progres": "progres", "progress": "progres",
}


# ---------------------------------------------------------------------------
# Utilitas angka & teks
# ---------------------------------------------------------------------------
class Num(str):
    """Nilai angka mentah dari sel XLSX (titik = desimal, tanpa pemisah ribuan)."""


def norm(s):
    return " ".join(str(s or "").strip().lower().split())


def angka(s, label="angka"):
    """Ubah teks angka gaya Indonesia/Inggris menjadi Decimal. None jika kosong."""
    if s is None:
        return None
    if isinstance(s, Decimal):
        return s
    if isinstance(s, (int, float)):
        return Decimal(str(s))
    if isinstance(s, Num):
        try:
            return Decimal(str(s))
        except InvalidOperation:
            raise Gagal("%s '%s' bukan angka." % (label, s))
    t = str(s).strip()
    if t in ("", "-", "—", "–"):
        return None
    t = re.sub(r"\s", "", t).replace("−", "-")
    neg = False
    # Tanda minus boleh sebelum atau sesudah "Rp": "-Rp5jt", "Rp -5.000.000", "(5.000.000)", "Rp(5.000)"
    for _ in range(3):
        awal = t
        if t.startswith("(") and t.endswith(")"):
            neg, t = True, t[1:-1]
        if t.startswith("-"):
            neg, t = True, t[1:]
        t = re.sub(r"(?i)^(rp|idr)\.?", "", t)
        if t == awal:
            break
    t = t.lstrip("+").replace("%", "")
    t = re.sub(r"(?i)x$", "", t)
    kali = Decimal(1)
    m_suf = re.search(r"(?i)(jt|juta|rb|ribu|miliar)$", t)
    if m_suf:
        kali = {"jt": Decimal(10) ** 6, "juta": Decimal(10) ** 6, "rb": Decimal(1000), "ribu": Decimal(1000),
                "miliar": Decimal(10) ** 9}[m_suf.group(1).lower()]
        t = t[:m_suf.start()]
    if not t:
        return None
    if "," in t and "." in t:
        if t.rfind(",") > t.rfind("."):
            t = t.replace(".", "").replace(",", ".")
        else:
            t = t.replace(",", "")
    elif "," in t:
        t = t.replace(",", "") if t.count(",") > 1 else t.replace(",", ".")
    elif "." in t:
        if t.count(".") > 1 or re.fullmatch(r"[1-9]\d{0,2}(\.\d{3})+", t):
            t = t.replace(".", "")
    if not re.fullmatch(r"\d+(\.\d+)?", t):
        raise Gagal("%s '%s' bukan angka yang bisa dibaca." % (label, s))
    d = Decimal(t) * kali
    return -d if neg else d


def bulat(d, n=1):
    if d is None:
        return None
    q = Decimal(1).scaleb(-n)
    return d.quantize(q, rounding=ROUND_HALF_UP)


def fmt_angka(d, desimal=2, tetap=False):
    """1234567.5 -> '1.234.567,5' (tanpa nol di belakang, kecuali tetap=True)."""
    if d is None:
        return "-"
    d = bulat(d, desimal)
    neg = d < 0
    d = abs(d)
    s = format(d, "f")
    if "." in s:
        bulat_, pecahan = s.split(".")
        pecahan = pecahan if tetap else pecahan.rstrip("0")
    else:
        bulat_, pecahan = s, ""
    grup = []
    while len(bulat_) > 3:
        grup.insert(0, bulat_[-3:])
        bulat_ = bulat_[:-3]
    grup.insert(0, bulat_)
    hasil = ".".join(grup) + ("," + pecahan if pecahan else "")
    return ("-" if neg else "") + hasil


def fmt_nilai(d, satuan):
    if d is None:
        return "-"
    sat = (satuan or "").strip()
    if sat.lower() in ("rp", "rupiah", "idr"):
        return "Rp " + fmt_angka(bulat(d, 0), 0)
    if sat == "%":
        return fmt_angka(d) + "%"
    if sat.lower() == "x":
        return fmt_angka(d) + "x"
    return fmt_angka(d) + (" " + sat if sat else "")


def fmt_pct(d):
    return "-" if d is None else fmt_angka(bulat(d, 1), 1, True) + "%"


def fmt_skor(d):
    return "-" if d is None else fmt_angka(bulat(d, 1), 1, True)


def fmt_tren(d):
    if d is None:
        return ""
    d = bulat(d, 1)
    if d > 0:
        return "▲" + fmt_angka(d, 1, True)
    if d < 0:
        return "▼" + fmt_angka(-d, 1, True)
    return "＝0,0"


def s_dec(d, n=4):
    """Decimal -> string untuk JSON (dibulatkan n desimal, tanpa nol berlebih)."""
    if d is None:
        return None
    s = format(bulat(d, n), "f")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    return s


# ---------------------------------------------------------------------------
# Membaca & menulis tabel
# ---------------------------------------------------------------------------
BATAS_UKURAN = 50 * 1024 * 1024
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
      "pr": "http://schemas.openxmlformats.org/package/2006/relationships"}


def _kolom_ke_indeks(ref):
    hf = re.match(r"[A-Z]+", ref or "")
    if not hf:
        return None
    k = 0
    for ch in hf.group(0):
        k = k * 26 + (ord(ch) - 64)
    return k - 1


def baca_xlsx(path):
    try:
        z = zipfile.ZipFile(str(path))
    except (zipfile.BadZipFile, OSError):
        raise Gagal("File '%s' rusak atau bukan Excel asli. Simpan ulang sebagai CSV." % Path(path).name)
    with z:
        nama = set(z.namelist())
        if any(i.file_size > BATAS_UKURAN for i in z.infolist()):
            raise Gagal("Isi file Excel terlalu besar untuk dibaca.")
        shared = []
        if "xl/sharedStrings.xml" in nama:
            for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
                shared.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
        sheet = "xl/worksheets/sheet1.xml"
        try:
            wb = ET.fromstring(z.read("xl/workbook.xml"))
            pertama = wb.find("m:sheets/m:sheet", NS)
            rid = pertama.get("{%s}id" % NS["r"]) if pertama is not None else None
            for rel in ET.fromstring(z.read("xl/_rels/workbook.xml.rels")).findall("pr:Relationship", NS):
                if rel.get("Id") == rid:
                    tg = rel.get("Target").lstrip("/")
                    sheet = tg if tg.startswith("xl/") else "xl/" + tg
        except (KeyError, ET.ParseError, AttributeError):
            pass
        if sheet not in nama:
            raise Gagal("Sheet pertama tidak ditemukan di file Excel. Simpan ulang sebagai CSV.")
        akar = ET.fromstring(z.read(sheet))
    baris = []
    for row in akar.iter("{%s}row" % NS["m"]):
        isi = {}
        for c in row.findall("m:c", NS):
            kol = _kolom_ke_indeks(c.get("r"))
            if kol is None:
                kol = len(isi)
            tipe = c.get("t")
            v = c.find("m:v", NS)
            if tipe == "s" and v is not None and v.text:
                i = int(v.text)
                nilai = shared[i] if i < len(shared) else ""
            elif tipe == "inlineStr":
                nilai = "".join(t.text or "" for t in c.iter("{%s}t" % NS["m"]))
            elif v is not None and v.text is not None:
                nilai = v.text if tipe in ("str", "e", "b") else Num(v.text)
            else:
                nilai = ""
            isi[kol] = nilai
        baris.append([isi.get(i, "") for i in range(max(isi) + 1)] if isi else [])
    return baris


def baca_csv_teks(teks):
    contoh = teks[:4096]
    baris1 = contoh.splitlines()[0] if contoh.splitlines() else ""
    pemisah = ";" if baris1.count(";") > baris1.count(",") else ("\t" if baris1.count("\t") > baris1.count(",") else ",")
    return [r for r in csv.reader(io.StringIO(teks), delimiter=pemisah)]


def baca_tabel(path):
    """Kembalikan list of dict dengan nama kolom yang sudah dinormalkan."""
    p = Path(path).expanduser()
    if not p.is_file():
        raise Gagal("File '%s' tidak ditemukan." % path)
    if p.stat().st_size == 0:
        raise Gagal("File '%s' kosong." % p.name)
    if p.stat().st_size > BATAS_UKURAN:
        raise Gagal("File '%s' terlalu besar (> 50 MB)." % p.name)
    if p.suffix.lower() == ".xls":
        raise Gagal("Format .xls (Excel lama) tidak didukung. Simpan ulang sebagai .xlsx atau CSV.")
    mentah = p.read_bytes()
    if p.suffix.lower() in (".xlsx", ".xlsm") or mentah[:2] == b"PK":
        rows = baca_xlsx(p)
    else:
        for enc in ("utf-8-sig", "cp1252"):
            try:
                teks = mentah.decode(enc)
                break
            except UnicodeDecodeError:
                continue
        rows = baca_csv_teks(teks)
    rows = [r for r in rows if any(str(x).strip() for x in r)]
    if not rows:
        raise Gagal("File '%s' tidak berisi data." % p.name)
    header = []
    for h in rows[0]:
        k = re.sub(r"\s+", "_", norm(h))
        header.append(KOLOM_ALIAS.get(k, k))
    hasil = []
    for no, r in enumerate(rows[1:], start=2):
        d = {"_baris": no}
        for i, h in enumerate(header):
            if h:
                val = r[i] if i < len(r) else ""
                d[h] = val if isinstance(val, Num) else str(val).strip()
        hasil.append(d)
    return header, hasil


def tulis_csv(path, kolom, baris):
    p = Path(path).expanduser()
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(kolom)
        for b in baris:
            w.writerow(["" if b.get(k) is None else b.get(k) for k in kolom])


def _sel(ref, nilai, gaya=0):
    s = ' s="%d"' % gaya if gaya else ""
    if isinstance(nilai, (int, Decimal)) and not isinstance(nilai, bool):
        return '<c r="%s"%s><v>%s</v></c>' % (ref, s, nilai)
    teks = escape(str(nilai))
    return '<c r="%s" t="inlineStr"%s><is><t xml:space="preserve">%s</t></is></c>' % (ref, s, teks)


def _huruf(i):
    s = ""
    i += 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


def _xml_sheet(baris, lebar):
    cols = "".join('<col min="%d" max="%d" width="%d" customWidth="1"/>' % (i + 1, i + 1, w)
                   for i, w in enumerate(lebar))
    isi = []
    for r, row in enumerate(baris, start=1):
        sel = "".join(_sel(_huruf(c) + str(r), v, 1 if r == 1 else 0)
                      for c, v in enumerate(row) if v is not None and v != "")
        isi.append('<row r="%d">%s</row>' % (r, sel))
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
            '<sheetViews><sheetView workbookViewId="0"><pane ySplit="1" topLeftCell="A2" activePane="bottomLeft" state="frozen"/></sheetView></sheetViews>'
            '<cols>%s</cols><sheetData>%s</sheetData></worksheet>') % (cols, "".join(isi))


def tulis_xlsx(path, lembar):
    """lembar: list of (nama_sheet, baris(list of list), lebar_kolom(list int))."""
    p = Path(path).expanduser()
    p.parent.mkdir(parents=True, exist_ok=True)
    ct = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          '<Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
          '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>']
    sheets, rels = [], []
    for i, (nama, _, _) in enumerate(lembar, start=1):
        ct.append('<Override PartName="/xl/worksheets/sheet%d.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' % i)
        sheets.append('<sheet name="%s" sheetId="%d" r:id="rId%d"/>' % (escape(nama[:31]), i, i))
        rels.append('<Relationship Id="rId%d" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet%d.xml"/>' % (i, i))
    n = len(lembar)
    rels.append('<Relationship Id="rId%d" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>' % (n + 1))
    ct.append("</Types>")
    styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
              '<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
              '<fonts count="2"><font><sz val="11"/><name val="Calibri"/></font><font><b/><sz val="11"/><name val="Calibri"/></font></fonts>'
              '<fills count="3"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill>'
              '<fill><patternFill patternType="solid"><fgColor rgb="FFDDEBF7"/><bgColor indexed="64"/></patternFill></fill></fills>'
              '<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>'
              '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
              '<cellXfs count="2"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>'
              '<xf numFmtId="0" fontId="1" fillId="2" borderId="0" xfId="0" applyFont="1" applyFill="1"/></cellXfs>'
              '<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles>'
              '</styleSheet>')
    with zipfile.ZipFile(str(p), "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", "".join(ct))
        z.writestr("_rels/.rels",
                   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                   '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>'
                   '</Relationships>')
        z.writestr("xl/workbook.xml",
                   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
                   'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
                   '<sheets>%s</sheets></workbook>' % "".join(sheets))
        z.writestr("xl/_rels/workbook.xml.rels",
                   '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                   '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">%s</Relationships>' % "".join(rels))
        z.writestr("xl/styles.xml", styles)
        for i, (_, baris, lebar) in enumerate(lembar, start=1):
            z.writestr("xl/worksheets/sheet%d.xml" % i, _xml_sheet(baris, lebar))


# ---------------------------------------------------------------------------
# Rencana KPI
# ---------------------------------------------------------------------------
KOLOM_RENCANA = ["periode", "divisi", "orang", "kpi", "satuan", "arah", "bobot", "target",
                 "ambang", "maks_capai", "kata_kunci", "sumber"]


def pemilik_kunci(r):
    return ("orang", norm(r["orang"])) if norm(r.get("orang")) else ("divisi", norm(r["divisi"]))


def baca_rencana(path):
    """Baca & validasi rencana. Kembalikan (daftar baris, error, catatan)."""
    header, rows = baca_tabel(path)
    wajib = {"divisi", "kpi", "arah", "bobot", "target"}
    kurang = wajib - set(header)
    if kurang:
        raise Gagal("Rencana KPI kurang kolom: %s. Kolom minimal: divisi, orang, kpi, arah, bobot, target "
                    "(lihat templates/rencana-kpi-contoh.csv)." % ", ".join(sorted(kurang)))
    err, cat, hasil = [], [], []
    divisi_orang = {}
    for r in rows:
        no = r["_baris"]
        if not norm(r.get("kpi")) and not str(r.get("target", "")).strip():
            continue
        b = {k: r.get(k, "") for k in KOLOM_RENCANA}
        b["_baris"] = no
        b["periode"] = str(b["periode"]).strip()
        b["divisi"] = " ".join(str(b["divisi"]).split())
        b["orang"] = " ".join(str(b["orang"]).split())
        if b["orang"] in ("-", "—"):
            b["orang"] = ""
        b["kpi"] = " ".join(str(b["kpi"]).split())
        label = "Rencana baris %d (%s / %s)" % (no, b["orang"] or b["divisi"] or "?", b["kpi"] or "?")
        try:
            urai_periode_rencana(b["periode"])
        except Gagal as e:
            err.append("%s: %s" % (label, e))
        if not b["divisi"]:
            err.append("%s: kolom divisi kosong." % label)
        if not b["kpi"]:
            err.append("%s: nama KPI kosong." % label)
        arah = ARAH.get(norm(b["arah"]))
        if not arah:
            err.append("%s: arah '%s' tidak dikenal. Isi 'naik' (makin tinggi makin baik) atau "
                       "'turun' (makin rendah makin baik)." % (label, b["arah"]))
        b["arah"] = arah
        try:
            b["bobot"] = angka(b["bobot"], "bobot")
            b["target"] = angka(b["target"], "target")
            b["ambang"] = angka(b["ambang"], "ambang")
            b["maks_capai"] = angka(b["maks_capai"], "maks_capai")
        except Gagal as e:
            err.append("%s: %s" % (label, e))
            continue
        if b["bobot"] is None or b["bobot"] <= 0:
            err.append("%s: bobot harus lebih dari 0." % label)
        if b["target"] is None:
            err.append("%s: target kosong." % label)
        elif b["target"] < 0:
            err.append("%s: target tidak boleh negatif." % label)
        elif b["target"] == 0 and arah == "naik":
            err.append("%s: target 0 untuk KPI arah 'naik' tidak bisa dihitung (pembagian dengan nol). "
                       "Isi target lebih dari 0." % label)
        elif b["target"] == 0 and arah == "turun":
            cat.append("%s: target 0 (arah turun) memakai aturan 'nol kejadian': capaian 100%% jika "
                       "realisasi 0, selain itu 0%%." % label)
        if b["ambang"] is not None and b["target"] is not None and arah:
            if b["ambang"] < 0:
                err.append("%s: ambang tidak boleh negatif." % label)
            elif arah == "naik" and b["ambang"] > b["target"]:
                err.append("%s: untuk arah 'naik', ambang (batas minimal) harus <= target." % label)
            elif arah == "turun" and b["ambang"] < b["target"]:
                err.append("%s: untuk arah 'turun', ambang (batas maksimal) harus >= target." % label)
        if b["maks_capai"] is not None and b["maks_capai"] < 100:
            err.append("%s: maks_capai minimal 100 (persen)." % label)
        if b["orang"]:
            k = norm(b["orang"])
            if k in divisi_orang and divisi_orang[k] != norm(b["divisi"]):
                err.append("%s: %s tercatat di dua divisi berbeda. Satu orang = satu divisi." % (label, b["orang"]))
            divisi_orang.setdefault(k, norm(b["divisi"]))
        hasil.append(b)
    if not hasil and not err:
        err.append("Rencana KPI tidak berisi baris KPI.")
    # Bobot pecahan (0,4) -> persen, per pemilik & periode
    grup = {}
    for b in hasil:
        grup.setdefault((b["periode"], pemilik_kunci(b)), []).append(b)
    for (per, pk), bs in grup.items():
        if any(b["bobot"] is None for b in bs):
            continue
        nama_pk = bs[0]["orang"] or ("divisi " + bs[0]["divisi"])
        total = sum(b["bobot"] for b in bs)
        if all(b["bobot"] <= 1 for b in bs) and total == 1:
            for b in bs:
                b["bobot"] = b["bobot"] * D100
            cat.append("Bobot %s ditulis sebagai pecahan (total 1); dibaca sebagai persen (total 100)." % nama_pk)
            total = D100
        if total != D100:
            err.append("Bobot KPI %s%s berjumlah %s, harus tepat 100. Ubah bobot lalu cek lagi."
                       % (nama_pk, " (periode %s)" % per if per else "", fmt_angka(total)))
        nama_kpi = [norm(b["kpi"]) for b in bs]
        for k in set(nama_kpi):
            if nama_kpi.count(k) > 1:
                err.append("KPI '%s' untuk %s muncul lebih dari sekali%s." % (k, nama_pk, " (periode %s)" % per if per else ""))
        if len(bs) > 7:
            cat.append("%s punya %d KPI. Saran: 3-5 KPI per orang supaya fokus." % (nama_pk, len(bs)))
    return hasil, err, cat


POLA_RENTANG = re.compile(r"^\s*([0-9A-Za-z-]+)?\s*(?:\.\.|s/d|sd|sampai)\s*([0-9A-Za-z-]+)?\s*$", re.I)


def urai_periode_rencana(teks):
    """'' -> semua; '2026-10' -> tepat; '2026-10..' / '2026-10..2026-12' / '2026-10 s/d 2026-12' -> rentang.
    Kembalikan (jenis, awal, akhir) atau raise Gagal."""
    t = str(teks or "").strip()
    if not t:
        return ("semua", None, None)
    m = POLA_RENTANG.match(t)
    if m:
        a, b = (m.group(1) or "").strip(), (m.group(2) or "").strip()
        if not a and not b:
            raise Gagal("periode '%s' tidak lengkap." % t)
        if a and b and (_pola_periode(a) != _pola_periode(b) or a > b):
            raise Gagal("rentang periode '%s' tidak valid (format berbeda atau awal > akhir)." % t)
        return ("rentang", a or None, b or None)
    if re.fullmatch(r"[0-9A-Za-z-]+", t):
        return ("tepat", t, t)
    raise Gagal("periode '%s' tidak dikenali. Contoh: 2026-10, 2026-10.. (mulai Oktober), "
                "2026-10..2026-12, atau kosong (semua periode)." % t)


def berlaku_untuk(teks, periode):
    """Prioritas kecocokan baris rencana dengan periode: 3 tepat, 2 rentang, 1 kosong, 0 tidak berlaku."""
    jenis, a, b = urai_periode_rencana(teks)
    if jenis == "semua":
        return 1
    if jenis == "tepat":
        return 3 if a == periode else 0
    patokan = a or b
    if _pola_periode(patokan) != _pola_periode(periode):
        return 0
    if (a is None or a <= periode) and (b is None or periode <= b):
        return 2
    return 0


def rencana_periode(rencana, periode):
    """Baris rencana yang berlaku untuk periode ini. Per orang/divisi dipakai SATU kelompok baris
    (nilai kolom periode yang sama): tepat > rentang > kosong, supaya bobot tetap 100."""
    per_pemilik = {}
    for b in rencana:
        per_pemilik.setdefault(pemilik_kunci(b), []).append(b)
    hasil = []
    for pk, bs in per_pemilik.items():
        kelompok = {}
        for b in bs:
            pr = berlaku_untuk(b["periode"], periode)
            if pr:
                kelompok.setdefault((pr, b["periode"]), []).append(b)
        if not kelompok:
            continue
        top = max(k[0] for k in kelompok)
        pilihan = [k for k in kelompok if k[0] == top]
        if len(pilihan) > 1:
            raise Gagal("Rencana %s punya beberapa rentang periode yang sama-sama berlaku untuk %s (%s). "
                        "Rapikan kolom periode supaya tidak tumpang tindih."
                        % (bs[0]["orang"] or "divisi " + bs[0]["divisi"], periode,
                           ", ".join(k[1] for k in pilihan)))
        hasil += kelompok[pilihan[0]]
    return hasil


# ---------------------------------------------------------------------------
# Perhitungan
# ---------------------------------------------------------------------------
def hitung_capaian(arah, target, real, cap):
    """Kembalikan (capaian_mentah, capaian_terbatas) dalam persen (Decimal)."""
    if arah == "naik":
        mentah = real / target * D100
    elif target == 0:
        mentah = D100 if real == 0 else D0
    else:
        mentah = (Decimal(2) - real / target) * D100
    terbatas = min(max(mentah, D0), cap)
    return mentah, terbatas


def status_kpi(arah, target, ambang, real, mentah, kuning):
    if mentah >= D100:
        return "hijau"
    if ambang is not None:
        ok = real >= ambang if arah == "naik" else real <= ambang
        return "kuning" if ok else "merah"
    return "kuning" if mentah >= kuning else "merah"


def status_skor(skor, hijau, kuning):
    if skor is None:
        return "belum"
    if skor >= hijau:
        return "hijau"
    return "kuning" if skor >= kuning else "merah"


IKON = {"hijau": "🟢", "kuning": "🟡", "merah": "🔴", "belum": "⚪"}


def baca_realisasi(path, periode_default, izinkan_minus):
    header, rows = baca_tabel(path)
    if "kpi" not in header or "realisasi" not in header:
        raise Gagal("File realisasi minimal punya kolom: periode, orang, kpi, realisasi "
                    "(lihat templates/realisasi-contoh.csv).")
    hasil, masalah = [], []
    for r in rows:
        no = r["_baris"]
        per = str(r.get("periode", "")).strip() or (periode_default or "")
        teks_real = r.get("realisasi", "")
        if not norm(r.get("kpi")) and not str(teks_real).strip():
            continue
        label = "Realisasi baris %d (%s / %s)" % (no, r.get("orang") or r.get("divisi") or "?", r.get("kpi") or "?")
        st_draf = norm(r.get("status_draf"))
        if st_draf and st_draf not in ("dikonfirmasi", "konfirmasi", "ok", "oke", "benar"):
            masalah.append("%s: status_draf '%s' -> dilewati. Hanya baris kosong atau 'dikonfirmasi' yang dihitung. "
                           "Setelah pemilik/manajer memastikan angkanya, ubah status_draf menjadi 'dikonfirmasi'."
                           % (label, r.get("status_draf")))
            continue
        try:
            t = str(teks_real).strip()
            m = re.fullmatch(r"\s*([\d.,]+)\s*/\s*([\d.,]+)\s*", t) if not isinstance(teks_real, Num) else None
            if m:
                a, b = angka(m.group(1)), angka(m.group(2))
                if b == 0:
                    raise Gagal("pembagi 0 pada '%s'" % t)
                val = a / b * D100
            else:
                val = angka(teks_real, "realisasi")
        except Gagal as e:
            masalah.append("%s: %s -> dilewati." % (label, e))
            continue
        if val is None:
            continue
        if val < 0 and not izinkan_minus:
            masalah.append("%s: realisasi negatif (%s) -> dilewati. Jika memang minus (mis. rugi), "
                           "jalankan dengan --izinkan-minus." % (label, fmt_angka(val)))
            continue
        orang = " ".join(str(r.get("orang", "")).split())
        hasil.append({"_baris": no, "periode": per, "orang": "" if orang in ("-", "—") else orang,
                      "divisi": " ".join(str(r.get("divisi", "")).split()),
                      "kpi": " ".join(str(r.get("kpi", "")).split()), "realisasi": val,
                      "rasio": bool(m) if not isinstance(teks_real, Num) else False,
                      "catatan": str(r.get("catatan", "")).strip()})
    return hasil, masalah


def pasangkan(rencana_p, realisasi, periode, duplikat, peringatan, periksa_tak_dikenal=True):
    """Kembalikan dict (pemilik_kunci, norm kpi) -> realisasi Decimal untuk periode."""
    kunci_rencana = {(pemilik_kunci(b), norm(b["kpi"])): b for b in rencana_p}
    kpi_per_pemilik = {}
    for b in rencana_p:
        kpi_per_pemilik.setdefault(pemilik_kunci(b), []).append(b["kpi"])
    orang_ke_divisi = {norm(b["orang"]): norm(b["divisi"]) for b in rencana_p if b["orang"]}
    nilai, sumber = {}, {}
    for r in realisasi:
        if r["periode"] != periode:
            continue
        pk = ("orang", norm(r["orang"])) if r["orang"] else ("divisi", norm(r["divisi"]))
        k = (pk, norm(r["kpi"]))
        if k not in kunci_rencana:
            if not periksa_tak_dikenal:
                continue
            siapa = r["orang"] or ("divisi " + r["divisi"])
            if pk not in kpi_per_pemilik:
                peringatan.append("Realisasi baris %d: '%s' tidak ada di rencana KPI periode %s -> dilewati."
                                  % (r["_baris"], siapa, periode))
            else:
                mirip = difflib.get_close_matches(r["kpi"], kpi_per_pemilik[pk], n=1, cutoff=0.5)
                saran = " Mungkin maksudnya '%s'? Perbaiki nama KPI di file realisasi." % mirip[0] if mirip else ""
                peringatan.append("Realisasi baris %d: KPI '%s' untuk %s tidak ada di rencana -> dilewati.%s"
                                  % (r["_baris"], r["kpi"], siapa, saran))
            continue
        if r["orang"] and norm(r["divisi"]) and orang_ke_divisi.get(norm(r["orang"])) != norm(r["divisi"]):
            peringatan.append("Realisasi baris %d: divisi '%s' untuk %s berbeda dari rencana; dipakai divisi di rencana."
                              % (r["_baris"], r["divisi"], r["orang"]))
        if k in nilai:
            if duplikat == "tolak":
                raise Gagal("Realisasi ganda untuk %s / %s periode %s (baris %d dan %d). Hapus salah satu, "
                            "atau jalankan dengan --duplikat jumlah (dijumlahkan) atau --duplikat terakhir."
                            % (r["orang"] or r["divisi"], r["kpi"], periode, sumber[k], r["_baris"]))
            if duplikat == "jumlah":
                satuan = kunci_rencana[k]["satuan"]
                if satuan == "%" or r["rasio"]:
                    raise Gagal("KPI '%s' bersatuan %% tidak boleh dijumlahkan (baris %d dan %d). "
                                "Hitung ulang persennya dari angka mentah." % (r["kpi"], sumber[k], r["_baris"]))
                nilai[k] = nilai[k] + r["realisasi"]
            else:
                nilai[k] = r["realisasi"]
            sumber[k] = r["_baris"]
            continue
        nilai[k] = r["realisasi"]
        sumber[k] = r["_baris"]
    return nilai


def skor_pemilik(bs, nilai, a):
    """Hitung satu pemilik (orang atau divisi). Kembalikan dict."""
    kpi_out, tersedia, jumlah = [], D0, D0
    kurang = []
    for b in bs:
        pk = pemilik_kunci(b)
        real = nilai.get((pk, norm(b["kpi"])))
        cap = b["maks_capai"] if b["maks_capai"] is not None else a.cap
        item = {"kpi": b["kpi"], "satuan": b["satuan"], "arah": b["arah"], "bobot": b["bobot"],
                "target": b["target"], "ambang": b["ambang"], "maks_capai": cap, "realisasi": real,
                "sumber": b.get("sumber", "")}
        if real is None:
            kurang.append(b["kpi"])
            if a.data_kosong == "nol":
                item.update(capaian_mentah=None, capaian=D0, status="merah", kontribusi=D0, kosong=True)
                tersedia += b["bobot"]
            else:
                item.update(capaian_mentah=None, capaian=None, status="belum", kontribusi=None, kosong=True)
            kpi_out.append(item)
            continue
        mentah, capaian = hitung_capaian(b["arah"], b["target"], real, cap)
        st = status_kpi(b["arah"], b["target"], b["ambang"], real, mentah, a.kuning)
        kontribusi = b["bobot"] * capaian / D100
        tersedia += b["bobot"]
        jumlah += b["bobot"] * capaian
        item.update(capaian_mentah=mentah, capaian=capaian, status=st, kontribusi=kontribusi, kosong=False)
        kpi_out.append(item)
    total_bobot = sum(b["bobot"] for b in bs)
    hasil = {"kpi": kpi_out, "bobot_total": total_bobot, "bobot_tersedia": tersedia, "kurang": kurang}
    sementara = (jumlah / tersedia) if tersedia > 0 else None
    if not kurang or a.data_kosong == "nol":
        hasil.update(skor=jumlah / total_bobot, lengkap=True, dasar="lengkap" if not kurang else "kosong=0")
    elif a.data_kosong == "bobot-ulang" and tersedia * D100 / total_bobot >= a.min_bobot:
        hasil.update(skor=sementara, lengkap=False, dasar="bobot-ulang")
    else:
        hasil.update(skor=None, lengkap=False, dasar="belum-lengkap")
    hasil["skor_sementara"] = sementara if kurang else None
    hasil["status"] = status_skor(hasil["skor"], a.hijau, a.kuning)
    return hasil


def hitung_periode(rencana, realisasi, periode, a, peringatan, periksa=True):
    rp = rencana_periode(rencana, periode)
    if not rp:
        return None
    nilai = pasangkan(rp, realisasi, periode, a.duplikat, peringatan, periksa)
    per_pemilik = {}
    for b in rp:
        per_pemilik.setdefault(pemilik_kunci(b), []).append(b)
    orang, divisi_kpi = [], {}
    for pk, bs in per_pemilik.items():
        h = skor_pemilik(bs, nilai, a)
        if pk[0] == "orang":
            h.update(nama=bs[0]["orang"], divisi=bs[0]["divisi"])
            orang.append(h)
        else:
            h.update(nama=bs[0]["divisi"], divisi=bs[0]["divisi"])
            divisi_kpi[norm(bs[0]["divisi"])] = h
    orang.sort(key=lambda o: (norm(o["divisi"]), norm(o["nama"])))
    nama_divisi = {}
    for b in rp:
        nama_divisi.setdefault(norm(b["divisi"]), b["divisi"])
    divisi = []
    for dk in sorted(nama_divisi):
        anggota = [o for o in orang if norm(o["divisi"]) == dk]
        lengkap = [o for o in anggota if o["skor"] is not None]
        belum = [o["nama"] for o in anggota if o["skor"] is None]
        rata = (sum(o["skor"] for o in lengkap) / len(lengkap)) if lengkap else None
        d = {"nama": nama_divisi[dk], "jumlah_orang": len(anggota), "rata_individu": rata,
             "belum_lengkap": belum}
        if dk in divisi_kpi:
            h = divisi_kpi[dk]
            d.update(skor=h["skor"], dasar_skor="kpi-divisi", kpi=h["kpi"], kurang=h["kurang"],
                     skor_sementara=h["skor_sementara"])
        else:
            d.update(skor=rata, dasar_skor="rata-rata individu", kpi=[], kurang=[], skor_sementara=None)
        d["status"] = status_skor(d["skor"], a.hijau, a.kuning)
        d["sebagian"] = bool(belum) and d["dasar_skor"] == "rata-rata individu" and rata is not None
        divisi.append(d)
    # perusahaan
    bobot_div = a.bobot_divisi_map
    ada = [d for d in divisi if d["skor"] is not None]
    kosong = [d["nama"] for d in divisi if d["skor"] is None]
    if bobot_div:
        tak_ada = [d["nama"] for d in divisi if norm(d["nama"]) not in bobot_div]
        if tak_ada:
            raise Gagal("--bobot-divisi belum mengisi bobot untuk: %s." % ", ".join(tak_ada))
        tb = sum(bobot_div[norm(d["nama"])] for d in ada)
        skor_p = (sum(bobot_div[norm(d["nama"])] * d["skor"] for d in ada) / tb) if tb > 0 else None
        dasar_p = "rata-rata tertimbang divisi"
    else:
        skor_p = (sum(d["skor"] for d in ada) / len(ada)) if ada else None
        dasar_p = "rata-rata divisi (bobot sama)"
    perusahaan = {"skor": skor_p, "status": status_skor(skor_p, a.hijau, a.kuning), "dasar": dasar_p,
                  "divisi_tanpa_skor": kosong,
                  "sebagian": bool(kosong) or any(d["sebagian"] for d in divisi)}
    return {"periode": periode, "perusahaan": perusahaan, "divisi": divisi, "orang": orang}


def tambah_tren(kini, lalu):
    if not lalu:
        return
    kini["perusahaan"]["tren"] = _selisih(kini["perusahaan"]["skor"], lalu["perusahaan"]["skor"])
    dl = {norm(d["nama"]): d for d in lalu["divisi"]}
    for d in kini["divisi"]:
        p = dl.get(norm(d["nama"]))
        d["tren"] = _selisih(d["skor"], p["skor"] if p else None)
    ol = {norm(o["nama"]): o for o in lalu["orang"]}
    for o in kini["orang"]:
        p = ol.get(norm(o["nama"]))
        o["tren"] = _selisih(o["skor"], p["skor"] if p else None)
        pk = {norm(k["kpi"]): k for k in (p["kpi"] if p else [])}
        for k in o["kpi"]:
            q = pk.get(norm(k["kpi"]))
            k["tren_capaian"] = _selisih(k["capaian"], q["capaian"] if q else None) if not k["kosong"] else None


def _selisih(a, b):
    return None if a is None or b is None else a - b


def periode_sebelumnya(periodes, periode):
    kandidat = sorted(p for p in periodes if p and p < periode and _pola_periode(p) == _pola_periode(periode))
    return kandidat[-1] if kandidat else None


def _pola_periode(p):
    return re.sub(r"\d", "9", p)


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------
def ke_json(obj):
    if isinstance(obj, Decimal):
        return s_dec(obj)
    if isinstance(obj, dict):
        return {k: ke_json(v) for k, v in obj.items() if not k.startswith("_")}
    if isinstance(obj, list):
        return [ke_json(v) for v in obj]
    return obj


def fmt_capaian(k):
    """Capaian untuk dibaca manusia: tidak pernah menampilkan persen minus."""
    m = k.get("capaian_mentah")
    if m is None:
        return "tanpa data (dihitung 0,0%)" if k.get("capaian") is not None else "-"
    if m < 0:
        return "0,0% (batas bawah; realisasi jauh dari target)"
    return fmt_pct(m)


def kpi_terlemah(o, n=1):
    """KPI dengan capaian terendah; bila seri (mis. beberapa KPI tanpa data = 0% di mode nol), yang BOBOTNYA
    terbesar didahulukan (v1.0.2), lalu nama."""
    ada = [k for k in o["kpi"] if k["capaian"] is not None]
    ada.sort(key=lambda k: (k["capaian"], -k["bobot"], norm(k["kpi"])))
    return ada[:n]


def laporan_teks(h, a, peringatan):
    per = h["periode"]
    L = []
    judul = a.judul or "Laporan KPI Tim"
    L.append("📊 *%s — %s*" % (judul, per))
    p = h["perusahaan"]
    tren = fmt_tren(p.get("tren"))
    L.append("Perusahaan: %s %s%s%s" % (IKON[p["status"]], fmt_skor(p["skor"]) if p["skor"] is not None else "belum bisa dihitung",
                                        " (%s vs %s)" % (tren, h.get("periode_lalu")) if tren else "",
                                        " — sebagian" if p["sebagian"] else ""))
    L.append("")
    L.append("*Divisi*")
    for d in h["divisi"]:
        tr = fmt_tren(d.get("tren"))
        info = fmt_skor(d["skor"]) if d["skor"] is not None else (
            "tidak ditampilkan (1 orang dinilai)" if d.get("disembunyikan") else "belum lengkap")
        ext = ""
        if d["sebagian"]:
            ext = (" (%d orang belum lengkap)" % len(d["belum_lengkap"]) if a.tanpa_nama
                   else " (tanpa %s)" % ", ".join(d["belum_lengkap"]))
        L.append("%s %s: %s%s%s" % (IKON[d["status"]], d["nama"], info, " " + tr if tr else "", ext))
    if not a.tanpa_nama:
        L.append("")
        L.append("*Per orang* (urut divisi & nama, bukan peringkat)")
        for o in h["orang"]:
            if o["skor"] is None:
                L.append("⚪ %s (%s): belum lengkap — belum ada data: %s"
                         % (o["nama"], o["divisi"], ", ".join(o["kurang"])))
                continue
            tr = fmt_tren(o.get("tren"))
            lemah = kpi_terlemah(o)
            catat = ""
            if lemah and (lemah[0]["status"] == "merah" or (o["status"] != "hijau" and lemah[0]["status"] != "hijau")):
                catat = " — perlu perhatian: %s %s" % (lemah[0]["kpi"], fmt_capaian(lemah[0]))
                lain_kosong = [k for k in o["kpi"] if k["kosong"] and k is not lemah[0]]
                if lemah[0]["kosong"] and lain_kosong:
                    catat += " (+%d KPI lain tanpa data)" % len(lain_kosong)
            if o["dasar"] == "bobot-ulang":
                catat += " (dihitung dari %s%% bobot)" % fmt_angka(o["bobot_tersedia"] * D100 / o["bobot_total"], 1)
            L.append("%s %s (%s): %s%s%s" % (IKON[o["status"]], o["nama"], o["divisi"], fmt_skor(o["skor"]),
                                             " " + tr if tr else "", catat))
    if peringatan:
        L.append("")
        for w in peringatan[:a.maks_peringatan]:
            L.append("⚠️ " + w)
        if len(peringatan) > a.maks_peringatan:
            L.append("⚠️ ...dan %d catatan lain (lihat --json)." % (len(peringatan) - a.maks_peringatan))
    L.append("")
    L.append("Skor 100 = rata-rata target tercapai (maks %s%% per KPI). 🟢 ≥%s 🟡 ≥%s 🔴 <%s. "
             "Bahan diskusi, bukan dasar sanksi otomatis." % (fmt_angka(a.cap, 0), fmt_angka(a.hijau, 0),
                                                              fmt_angka(a.kuning, 0), fmt_angka(a.kuning, 0)))
    return "\n".join(L)


def laporan_orang(h, nama, a):
    o = next((x for x in h["orang"] if norm(x["nama"]) == norm(nama)), None)
    if o is None:
        d = next((x for x in h["divisi"] if norm(x["nama"]) == norm(nama) and x["kpi"]), None)
        if d is None:
            raise Gagal("'%s' tidak ada di rencana KPI periode %s." % (nama, h["periode"]))
        o = dict(d, divisi=d["nama"], dasar=d["dasar_skor"], bobot_tersedia=None, bobot_total=None)
    L = ["*Rincian KPI %s (%s) — %s*" % (o["nama"], o["divisi"], h["periode"])]
    if o["skor"] is not None:
        tr = fmt_tren(o.get("tren"))
        L.append("Skor: %s %s%s" % (IKON[status_skor(o["skor"], a.hijau, a.kuning)], fmt_skor(o["skor"]),
                                    " (%s vs %s)" % (tr, h.get("periode_lalu")) if tr else ""))
    else:
        L.append("Skor: ⚪ belum lengkap (sementara %s dari KPI yang ada)" % fmt_skor(o.get("skor_sementara")))
    L.append("")
    for k in o["kpi"]:
        if k["kosong"]:
            L.append("%s %s — belum ada data%s (bobot %s%%, target %s)"
                     % (IKON[k["status"]], k["kpi"], ", dihitung 0%" if k["capaian"] is not None else "",
                        fmt_angka(k["bobot"]), fmt_nilai(k["target"], k["satuan"])))
            continue
        arah = "↑" if k["arah"] == "naik" else "↓"
        tc = fmt_tren(k.get("tren_capaian"))
        batas = " (dibatasi %s%%)" % fmt_angka(k["maks_capai"], 0) if k["capaian_mentah"] > k["capaian"] else ""
        L.append("%s %s %s: %s dari target %s → capaian %s%s, bobot %s%%, nilai %s%s"
                 % (IKON[k["status"]], k["kpi"], arah, fmt_nilai(k["realisasi"], k["satuan"]),
                    fmt_nilai(k["target"], k["satuan"]), fmt_capaian(k), batas,
                    fmt_angka(k["bobot"]), fmt_skor(k["kontribusi"]),
                    " (capaian %s poin vs %s)" % (tc, h.get("periode_lalu")) if tc else ""))
    return "\n".join(L)


def baris_csv_hasil(h):
    out = []
    for o in h["orang"]:
        for k in o["kpi"]:
            out.append({"periode": h["periode"], "divisi": o["divisi"], "orang": o["nama"], "kpi": k["kpi"],
                        "satuan": k["satuan"], "arah": k["arah"], "bobot": s_dec(k["bobot"]),
                        "target": s_dec(k["target"]), "realisasi": s_dec(k["realisasi"]),
                        "capaian_persen": s_dec(bulat(k["capaian_mentah"], 1)) if k["capaian_mentah"] is not None else "",
                        "capaian_dipakai": s_dec(bulat(k["capaian"], 1)) if k["capaian"] is not None else "",
                        "nilai": s_dec(bulat(k["kontribusi"], 2)) if k["kontribusi"] is not None else "",
                        "status_kpi": k["status"],
                        "skor_orang": s_dec(bulat(o["skor"], 1)) if o["skor"] is not None else "",
                        "status_orang": o["status"]})
    for d in h["divisi"]:
        for k in d["kpi"]:
            out.append({"periode": h["periode"], "divisi": d["nama"], "orang": "", "kpi": k["kpi"],
                        "satuan": k["satuan"], "arah": k["arah"], "bobot": s_dec(k["bobot"]),
                        "target": s_dec(k["target"]), "realisasi": s_dec(k["realisasi"]),
                        "capaian_persen": s_dec(bulat(k["capaian_mentah"], 1)) if k["capaian_mentah"] is not None else "",
                        "capaian_dipakai": s_dec(bulat(k["capaian"], 1)) if k["capaian"] is not None else "",
                        "nilai": s_dec(bulat(k["kontribusi"], 2)) if k["kontribusi"] is not None else "",
                        "status_kpi": k["status"],
                        "skor_orang": s_dec(bulat(d["skor"], 1)) if d["skor"] is not None else "",
                        "status_orang": d["status"]})
    return out


KOLOM_HASIL = ["periode", "divisi", "orang", "kpi", "satuan", "arah", "bobot", "target", "realisasi",
               "capaian_persen", "capaian_dipakai", "nilai", "status_kpi", "skor_orang", "status_orang"]


def cetak(a, data, teks):
    if a.json:
        print(json.dumps(ke_json(data), ensure_ascii=False, indent=2))
    else:
        print(teks)


# ---------------------------------------------------------------------------
# Perintah
# ---------------------------------------------------------------------------
def cari_peran(peran):
    k = norm(peran)
    k = ALIAS_PERAN.get(k, k)
    return k if k in KATALOG else None


def cmd_katalog(a):
    data = {}
    teks = []
    perans = [cari_peran(a.peran)] if a.peran else sorted(KATALOG)
    if a.peran and perans[0] is None:
        raise Gagal("Peran '%s' belum ada di katalog bawaan. Pilihan: %s. Untuk peran lain, susun KPI "
                    "sendiri dari references/katalog-kpi.md." % (a.peran, ", ".join(sorted(KATALOG))))
    for p in perans:
        data[p] = [{"kpi": k, "satuan": s, "arah": ar, "bobot_usulan": bo, "target_contoh": t,
                    "kata_kunci": kk, "sumber_data": sb} for k, s, ar, bo, t, kk, sb in KATALOG[p]]
        teks.append("*%s*" % p)
        for k, s, ar, bo, t, kk, sb in KATALOG[p]:
            teks.append("- %s (%s, %s) bobot %d%%, contoh target %s — sumber: %s"
                        % (k, s, "makin tinggi makin baik" if ar == "naik" else "makin rendah makin baik",
                           bo, fmt_nilai(Decimal(str(t)), s), sb))
    cetak(a, {"ok": True, "katalog": data}, "\n".join(teks))
    return 0


def cmd_template(a):
    _, tim = baca_tabel(a.tim)
    if not tim or "orang" not in tim[0]:
        raise Gagal("File tim minimal punya kolom: nama, divisi, peran (lihat templates/tim-contoh.csv).")
    rencana, lewati = [], []
    for t in tim:
        nama = " ".join(str(t.get("orang", "")).split())
        if not nama:
            continue
        peran = cari_peran(t.get("peran", ""))
        if not peran:
            lewati.append("%s: peran '%s' tidak ada di katalog (%s) -> isi KPI-nya manual."
                          % (nama, t.get("peran", ""), ", ".join(sorted(KATALOG))))
            continue
        for k, s, ar, bo, tg, kk, sb in KATALOG[peran]:
            rencana.append({"periode": (a.periode + "..") if a.periode else "", "divisi": t.get("divisi", "") or peran.title(),
                            "orang": nama, "kpi": k, "satuan": s, "arah": ar, "bobot": bo,
                            "target": tg, "ambang": "", "maks_capai": "", "kata_kunci": kk, "sumber": sb})
    if not rencana:
        raise Gagal("Tidak ada orang dengan peran yang dikenali. " + " ".join(lewati))
    folder = Path(a.keluar).expanduser()
    folder.mkdir(parents=True, exist_ok=True)
    f_csv = folder / "rencana-kpi.csv"
    f_xlsx = folder / "rencana-kpi.xlsx"
    f_real = folder / ("realisasi-%s.csv" % (a.periode or "periode"))
    for f in (f_csv, f_xlsx, f_real):
        if f.exists() and not a.timpa:
            raise Gagal("File '%s' sudah ada. Pakai --timpa untuk menimpa, atau pilih folder lain." % f)
    tulis_csv(f_csv, KOLOM_RENCANA, rencana)
    petunjuk = [
        ["Petunjuk mengisi rencana KPI (Komunitech kpi-tim)"],
        ["1. Satu baris = satu KPI untuk satu orang. Kosongkan kolom 'orang' untuk KPI milik divisi."],
        ["   Kolom periode: '2026-10..' = berlaku mulai Oktober dan bulan-bulan berikutnya; '2026-10..2026-12' = rentang; kosong = semua periode; '2026-10' = hanya bulan itu."],
        ["2. Bobot per orang WAJIB berjumlah 100. Saran 3-5 KPI per orang."],
        ["3. Arah: 'naik' = makin tinggi makin baik (omzet); 'turun' = makin rendah makin baik (komplain, reject)."],
        ["4. Target: angka saja, tanpa 'Rp' atau titik ribuan boleh. Target 0 hanya untuk arah 'turun' (nol kejadian)."],
        ["5. Ambang (opsional): batas kuning/merah. Arah naik = nilai minimal; arah turun = nilai maksimal."],
        ["6. maks_capai (opsional): batas capaian per KPI, default 120 (%)."],
        ["7. Target di katalog hanya CONTOH. Ganti sesuai data 3 bulan terakhir usaha Anda."],
        ["8. Google Sheets: File > Impor > Unggah file ini. Setelah diisi: File > Download > .xlsx atau .csv."],
        ["9. Nilai KPI adalah bahan diskusi & pembinaan, bukan dasar PHK/sanksi otomatis."],
    ]
    isi = [KOLOM_RENCANA] + [[r[k] if not isinstance(r[k], (int, float)) else Decimal(str(r[k])) for k in KOLOM_RENCANA]
                             for r in rencana]
    tulis_xlsx(f_xlsx, [("Rencana KPI", isi, [10, 16, 14, 30, 10, 8, 8, 12, 10, 11, 30, 34]),
                        ("Petunjuk", petunjuk, [110])])
    real = [{"periode": a.periode or "", "divisi": r["divisi"], "orang": r["orang"], "kpi": r["kpi"],
             "realisasi": "", "catatan": ""} for r in rencana]
    tulis_csv(f_real, ["periode", "divisi", "orang", "kpi", "realisasi", "catatan"], real)
    data = {"ok": True, "file": [str(f_csv), str(f_xlsx), str(f_real)], "jumlah_baris": len(rencana),
            "dilewati": lewati}
    teks = "Dibuat:\n- %s\n- %s\n- %s\n%d baris KPI.%s" % (f_csv, f_xlsx, f_real, len(rencana),
                                                        ("\nPerlu diisi manual:\n- " + "\n- ".join(lewati)) if lewati else "")
    cetak(a, data, teks)
    return 0


def cmd_cek(a):
    rencana, err, cat = baca_rencana(a.rencana)
    orang = sorted({b["orang"] for b in rencana if b["orang"]})
    divisi = sorted({b["divisi"] for b in rencana})
    data = {"ok": not err, "error": err, "catatan": cat, "jumlah_kpi": len(rencana),
            "orang": orang, "divisi": divisi}
    if err:
        teks = "❌ Rencana KPI belum bisa dipakai:\n- " + "\n- ".join(err)
    else:
        teks = "✅ Rencana KPI valid: %d KPI, %d orang, %d divisi." % (len(rencana), len(orang), len(divisi))
    if cat:
        teks += "\nCatatan:\n- " + "\n- ".join(cat)
    cetak(a, data, teks)
    return 1 if err else 0


def siapkan_aturan(a):
    a.cap = angka(a.cap, "--cap")
    a.hijau = angka(a.hijau, "--hijau")
    a.kuning = angka(a.kuning, "--kuning")
    a.min_bobot = angka(a.min_bobot, "--min-bobot")
    if a.cap < 100:
        raise Gagal("--cap minimal 100.")
    if a.kuning > a.hijau:
        raise Gagal("--kuning harus <= --hijau.")
    a.bobot_divisi_map = {}
    if a.bobot_divisi:
        for bag in a.bobot_divisi.split(","):
            if "=" not in bag:
                raise Gagal("Format --bobot-divisi: \"Sales=50,Gudang=30,Keuangan=20\".")
            n, v = bag.rsplit("=", 1)
            a.bobot_divisi_map[norm(n)] = angka(v, "bobot divisi")
        if sum(a.bobot_divisi_map.values()) != D100:
            raise Gagal("--bobot-divisi harus berjumlah 100 (sekarang %s)." % fmt_angka(sum(a.bobot_divisi_map.values())))


def cmd_skor(a):
    siapkan_aturan(a)
    rencana, err, cat = baca_rencana(a.rencana)
    if err:
        raise Gagal("Rencana KPI belum valid:\n- " + "\n- ".join(err))
    realisasi, masalah = baca_realisasi(a.realisasi, a.periode_default, a.izinkan_minus)
    periodes = {r["periode"] for r in realisasi}
    periode = a.periode
    if not periode:
        pilihan = sorted(p for p in periodes if p)
        if not pilihan:
            raise Gagal("Periode tidak diketahui. Isi kolom 'periode' di file realisasi atau pakai --periode 2026-09.")
        periode = pilihan[-1]
    peringatan = list(masalah)
    umum = []          # peringatan tanpa nama orang (boleh tampil di --tanpa-nama)
    h = hitung_periode(rencana, realisasi, periode, a, peringatan)
    if h is None:
        raise Gagal("Tidak ada rencana KPI yang berlaku untuk periode %s. Kolom 'periode' di rencana: kosongkan "
                    "(berlaku semua periode), atau isi rentang mis. '2026-10..' (mulai Oktober) atau "
                    "'2026-10..2026-12'." % periode)
    ada_data = any(not k["kosong"] for o in h["orang"] for k in o["kpi"]) or \
        any(not k["kosong"] for d in h["divisi"] for k in d["kpi"])
    if not ada_data:
        raise Gagal("Belum ada satu pun realisasi untuk periode %s. Laporan tidak dibuat (tidak mengirim angka nol)." % periode)
    seharusnya = periode_seharusnya_lalu(periode)
    lalu = a.periode_lalu or periode_sebelumnya(periodes, periode)
    h["periode_lalu"] = None
    if not lalu:
        umum.append("Tren tidak dihitung: file realisasi tidak berisi periode sebelumnya%s."
                    % (" (%s)" % seharusnya if seharusnya else ""))
    else:
        if not a.periode_lalu and seharusnya and lalu != seharusnya:
            umum.append("Periode %s tidak ada di data; tren dibandingkan dengan %s." % (seharusnya, lalu))
        hl = hitung_periode(rencana, realisasi, lalu, a, [], periksa=False)
        if hl is None:
            umum.append("Tren tidak dihitung: rencana KPI tidak berlaku untuk %s (cek kolom periode di rencana, "
                        "mis. kosongkan atau isi rentang '%s..')." % (lalu, lalu))
        elif not any(o["skor"] is not None for o in hl["orang"]) and not any(d["skor"] is not None for d in hl["divisi"]):
            umum.append("Tren tidak dihitung: tidak ada skor lengkap di periode %s." % lalu)
        else:
            tambah_tren(h, hl)
            h["periode_lalu"] = lalu
            for d in h["divisi"]:
                dl = next((x for x in hl["divisi"] if norm(x["nama"]) == norm(d["nama"])), None)
                if dl and d["dasar_skor"] == "rata-rata individu" and d.get("tren") is not None:
                    n_kini = d["jumlah_orang"] - len(d["belum_lengkap"])
                    n_lalu = dl["jumlah_orang"] - len(dl["belum_lengkap"])
                    if n_kini != n_lalu:
                        umum.append("Tren divisi %s membandingkan jumlah orang dinilai yang berbeda (%s: %d orang, "
                                    "%s: %d orang)." % (d["nama"], lalu, n_lalu, periode, n_kini))
    for o in h["orang"]:
        if o["skor"] is None:
            alasan = ("bobot berdata %s%% < --min-bobot %s%%" % (fmt_angka(o["bobot_tersedia"] * D100 / o["bobot_total"], 1),
                                                               fmt_angka(a.min_bobot))
                      if a.data_kosong == "bobot-ulang" else "mode tandai")
            peringatan.append("%s belum lengkap (tidak ikut rata-rata divisi; %s): belum ada data %s."
                              % (o["nama"], alasan, ", ".join(o["kurang"])))
        elif o["dasar"] == "bobot-ulang":
            peringatan.append("%s: skor dihitung ulang dari KPI yang ada (%s%% bobot); belum ada data %s."
                              % (o["nama"], fmt_angka(o["bobot_tersedia"] * D100 / o["bobot_total"], 1), ", ".join(o["kurang"])))
        elif o["kurang"] and a.data_kosong == "nol":
            peringatan.append("%s: KPI tanpa data dihitung 0%% (--data-kosong nol): %s." % (o["nama"], ", ".join(o["kurang"])))
        for k in o["kpi"]:
            m = k.get("capaian_mentah")
            if m is not None and k["arah"] == "naik" and (m < 1 or m > 1000):
                peringatan.append("%s / %s: capaian %s tidak wajar. Cek penulisan angka/satuan (mis. '1,250' dibaca "
                                  "1,25; tulis 1.250 untuk seribu dua ratus lima puluh)." % (o["nama"], k["kpi"], fmt_pct(m)))
    for d in h["divisi"]:
        if d["dasar_skor"] == "kpi-divisi" and d["kurang"]:
            umum.append("KPI divisi %s belum ada data: %s." % (d["nama"], ", ".join(d["kurang"])))
    aturan = {"cap": a.cap, "hijau": a.hijau, "kuning": a.kuning, "data_kosong": a.data_kosong,
              "min_bobot": a.min_bobot, "duplikat": a.duplikat}
    if a.csv_keluar:
        tulis_csv(a.csv_keluar, KOLOM_HASIL, baris_csv_hasil(h))
    if a.tanpa_nama and not a.orang:
        h = anonim_divisi(h, a, umum)                      # v1.0.2: divisi 1 orang digabung/disembunyikan
    data = {"ok": True, "versi": VERSI, "aturan": aturan, "catatan_rencana": cat, "peringatan": umum + peringatan}
    data.update(h)
    if a.tanpa_nama:
        data = versi_tanpa_nama(data, h, umum, peringatan)
    if a.orang:
        teks = laporan_orang(h, a.orang, a)
        if a.json:
            o = next((x for x in h["orang"] if norm(x["nama"]) == norm(a.orang)), None)
            data = {"ok": True, "periode": periode, "periode_lalu": h["periode_lalu"], "aturan": aturan,
                    "orang": o or next((x for x in h["divisi"] if norm(x["nama"]) == norm(a.orang)), None)}
    else:
        teks = laporan_teks(h, a, data["peringatan"])
    cetak(a, data, teks)
    return 0


MIN_ORANG_ANONIM = 2


def anonim_divisi(h, a, umum):
    """v1.0.2 (--tanpa-nama): skor divisi yang hanya berisi 1 orang dinilai = skor pribadi orang itu. Divisi seperti
    itu DIGABUNG menjadi "Gabungan divisi kecil" (bila gabungannya >= 2 orang) atau DISEMBUNYIKAN dengan catatan.
    Skor perusahaan tidak diubah. Kembalikan salinan h dengan daftar divisi baru."""
    def n_dinilai(d):
        if d["dasar_skor"] == "rata-rata individu":
            return d["jumlah_orang"] - len(d["belum_lengkap"])
        return d["jumlah_orang"] if d["jumlah_orang"] else MIN_ORANG_ANONIM   # KPI divisi tanpa daftar orang
    kecil = [d for d in h["divisi"] if d["skor"] is not None and n_dinilai(d) < MIN_ORANG_ANONIM]
    if not kecil:
        return h
    tampil = [d for d in h["divisi"] if not any(d is k for k in kecil)]
    n_total = sum(max(n_dinilai(d), 1) for d in kecil)
    nama = ", ".join(d["nama"] for d in kecil)
    if len(kecil) >= 2 and n_total >= MIN_ORANG_ANONIM:
        skor = sum(d["skor"] for d in kecil) / len(kecil)
        tampil.append({"nama": "Gabungan divisi kecil (%s)" % nama, "jumlah_orang": n_total, "skor": skor,
                       "status": status_skor(skor, a.hijau, a.kuning), "dasar_skor": "gabungan divisi kecil",
                       "kpi": [], "kurang": [], "skor_sementara": None, "belum_lengkap": [], "sebagian": False})
        umum.append("Divisi %s hanya berisi 1 orang yang dinilai, jadi skornya digabung (rata-rata divisi) agar skor "
                    "pribadi tidak terlihat di laporan tanpa nama." % nama)
    else:
        for d in kecil:
            tampil.append({"nama": d["nama"], "jumlah_orang": d["jumlah_orang"], "skor": None, "status": "belum",
                           "dasar_skor": "disembunyikan (1 orang dinilai)", "kpi": [], "kurang": [],
                           "skor_sementara": None, "belum_lengkap": list(d["belum_lengkap"]),
                           "sebagian": d["sebagian"], "disembunyikan": True})
        umum.append("Skor divisi %s tidak ditampilkan: hanya 1 orang yang dinilai, sehingga skor divisi = skor "
                    "pribadi. Skor perusahaan tetap menghitungnya; bila divisinya sedikit, pertimbangkan menggabungkan "
                    "divisi kecil di rencana KPI sebelum dikirim ke grup." % nama)
    urut = {norm(d["nama"]): i for i, d in enumerate(h["divisi"])}
    tampil.sort(key=lambda d: urut.get(norm(d["nama"]), len(urut)))
    h2 = dict(h)
    h2["divisi"] = tampil
    return h2


def versi_tanpa_nama(data, h, umum, peringatan):
    """Hapus semua nama orang: hanya perusahaan, divisi, dan hitungan agregat."""
    bersih = {k: v for k, v in data.items() if k not in ("orang", "catatan_rencana", "divisi", "peringatan")}
    divisi = []
    for d in h["divisi"]:
        dd = {k: v for k, v in d.items() if k not in ("belum_lengkap", "rata_individu")}
        dd["jumlah_belum_lengkap"] = len(d["belum_lengkap"])
        divisi.append(dd)
    bersih["divisi"] = divisi
    w = list(umum)
    n_belum = sum(1 for o in h["orang"] if o["skor"] is None)
    n_ulang = sum(1 for o in h["orang"] if o["dasar"] == "bobot-ulang")
    if n_belum:
        w.append("%d orang belum lengkap datanya (tidak ikut rata-rata divisi)." % n_belum)
    if n_ulang:
        w.append("%d orang dihitung dari sebagian KPI (--data-kosong bobot-ulang)." % n_ulang)
    sisa = len(peringatan) - n_belum - n_ulang
    if sisa > 0:
        w.append("%d catatan data lain perlu dicek pemilik (lihat laporan lengkap)." % sisa)
    bersih["peringatan"] = w
    return bersih


def periode_seharusnya_lalu(p):
    m = re.fullmatch(r"(\d{4})-(\d{2})", p)
    if m:
        y, mo = int(m.group(1)), int(m.group(2))
        return "%d-%02d" % ((y - 1, 12) if mo == 1 else (y, mo - 1))
    m = re.fullmatch(r"(\d{4})-W(\d{2})", p)
    if m:
        try:
            senin = datetime.date.fromisocalendar(int(m.group(1)), int(m.group(2)), 1)
        except (ValueError, AttributeError):
            return None
        iso = (senin - datetime.timedelta(days=7)).isocalendar()
        return "%d-W%02d" % (iso[0], iso[1])
    m = re.fullmatch(r"(\d{4})-Q([1-4])", p)
    if m:
        y, q = int(m.group(1)), int(m.group(2))
        return "%d-Q%d" % ((y - 1, 4) if q == 1 else (y, q - 1))
    return None


def pecah_klausa(baris):
    return [k.strip() for k in re.split(r"[;,]\s+|\s+dan\s+|\s+&\s+|\n", baris) if k.strip()]


POLA_ANGKA = re.compile(r"(?:(?<=[Rr][Pp])|(?<=[Rr][Pp]\.)|(?<![\w.,]))(\d+(?:[.,]\d+)*)\s*(jt|juta|rb|ribu|k|%|x)?(?!\w)", re.I)
POLA_WA = re.compile(r"^\[?\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4}[, ]+\d{1,2}[.:]\d{2}(?:[.:]\d{2})?\]?\s*(?:-\s*)?([^:]{1,40}):\s*(.*)$")
POLA_KE_DEPAN = re.compile(r"(?<!\w)(bulan depan|minggu depan|tahun depan|besok|lusa|nanti|rencana|rencananya|akan|mau|target baru)(?!\w)", re.I)
POLA_MASING = re.compile(r"(?<!\w)(masing|masing2|msg2|masing-masing|keduanya|berdua|bertiga|semuanya|tiap orang|"
                         r"per orang|sama sama|sama-sama|sama2)(?!\w)", re.I)
POLA_BUKAN_HASIL = re.compile(r"(?<!\w)(libur|izin|ijin|sakit|cuti|off|absen|lembur)(?!\w)", re.I)
KATA_UMUM = {"yang", "sama", "dari", "untuk", "dengan", "tanpa", "waktu", "hari", "jumlah", "tepat", "lewat",
             "total", "rata", "per", "bulan", "minggu", "selesai"}
KATA_SATUAN = {"dus", "pcs", "paket", "hari", "jam", "menit", "kali", "deal", "toko", "transaksi", "pesanan",
               "sku", "unit", "lead", "leads", "karton", "kg", "orang", "nota", "struk", "chat", "item", "kejadian"}


def ambil_angka(klausa):
    """Kembalikan list dict: nilai, sufiks, rp (didahului 'Rp'), target (kata 'target' sebelumnya), satuan_teks."""
    hasil = []
    for m in POLA_ANGKA.finditer(klausa):
        try:
            v = angka(m.group(1))
        except Gagal:
            continue
        suf = (m.group(2) or "").lower()
        if suf in ("jt", "juta"):
            v = v * Decimal(1000000)
        elif suf in ("rb", "ribu", "k"):
            v = v * Decimal(1000)
        sebelum = klausa[:m.start()].lower()
        if re.search(r"(?:^|[\s:(])-\s*(?:rp\.?\s*)?$|rp\.?\s*-\s*$", sebelum):
            v = -v
        berikut = re.match(r"\s*([a-zA-Z]+)", klausa[m.end():])
        hasil.append({"nilai": v, "sufiks": suf, "rp": bool(re.search(r"rp\.?\s*-?\s*$", sebelum)),
                      "target": "target" in sebelum,
                      "satuan_teks": berikut.group(1).lower() if berikut else ""})
    return hasil


def cek_satuan(n, b):
    """Catatan 'cek' bila angka di teks tidak cocok dengan satuan KPI."""
    sat = norm(b["satuan"])
    cat = []
    if sat == "%":
        if n["sufiks"] != "%":
            cat.append("pastikan %s%s = persen (KPI dalam %%)"
                       % (fmt_angka(n["nilai"]), " " + n["satuan_teks"] if n["satuan_teks"] else ""))
    elif sat in ("rp", "rupiah", "idr"):
        if not n["rp"] and n["sufiks"] not in ("jt", "juta", "rb", "ribu", "k") and abs(n["nilai"]) < 1000:
            cat.append("nilai rupiah %s sangat kecil; maksudnya ribu atau juta?" % fmt_angka(n["nilai"]))
    else:
        if n["rp"] or n["sufiks"] in ("jt", "juta", "rb", "ribu", "k"):
            cat.append("angka rupiah di chat, padahal satuan KPI '%s'" % b["satuan"])
        if n["sufiks"] == "%" and sat != "%":
            cat.append("angka persen di chat, padahal satuan KPI '%s'" % b["satuan"])
        if n["sufiks"] == "x" and sat != "x":
            cat.append("angka 'x' di chat, padahal satuan KPI '%s'" % b["satuan"])
    if n["satuan_teks"] in KATA_SATUAN and n["satuan_teks"] not in sat.split() and \
            not (n["satuan_teks"] == "leads" and "lead" in sat.split()):
        cat.append("satuan di chat '%s' berbeda dari satuan KPI '%s'" % (n["satuan_teks"], b["satuan"]))
    return cat


def cmd_baca_teks(a):
    rencana, err, _ = baca_rencana(a.rencana)
    if err:
        raise Gagal("Rencana KPI belum valid:\n- " + "\n- ".join(err))
    rp = rencana_periode(rencana, a.periode)
    if not rp:
        raise Gagal("Tidak ada rencana KPI yang berlaku untuk periode %s." % a.periode)
    if a.teks == "-":
        teks = sys.stdin.read()
    else:
        p = Path(a.teks).expanduser()
        if not p.is_file():
            raise Gagal("File teks '%s' tidak ditemukan." % a.teks)
        teks = p.read_text(encoding="utf-8", errors="replace")
    orang = {}
    for b in rp:
        if b["orang"]:
            orang.setdefault(norm(b["orang"]), []).append(b)
    panggilan = {}
    for n in orang:
        panggilan.setdefault(n, n)
        depan = n.split()[0]
        if len([m for m in orang if m.split()[0] == depan]) == 1:
            panggilan.setdefault(depan, n)

    def kata_kpi(b):
        kata = [k.strip().lower() for k in str(b.get("kata_kunci") or "").split(";") if k.strip()]
        return kata + [w for w in re.findall(r"[a-z]+", norm(b["kpi"])) if len(w) >= 4 and w not in KATA_UMUM]

    semua_kata = {k for b in rp for k in kata_kpi(b)}

    def ada_kata(k, low):
        return re.search(r"(?<!\w)%s" % re.escape(k), low) is not None

    draf, gagal, diabaikan = [], [], []

    def buat_draf(kunci, kl, low, nums, kutip, masing=False, banyak_orang=False):
        """Buat satu draf untuk orang `kunci`. Kembalikan alasan gagal (str) atau None."""
        kandidat = []
        for b in orang[kunci]:
            skor = sum(len(k) for k in set(kata_kpi(b)) if ada_kata(k, low))
            if skor:
                kandidat.append((skor, b))
        kandidat.sort(key=lambda x: -x[0])
        if not kandidat or (len(kandidat) > 1 and kandidat[0][0] == kandidat[1][0]):
            return "KPI tidak jelas" if not kandidat else "cocok ke lebih dari satu KPI"
        b = kandidat[0][1]
        target_sebut = [n["nilai"] for n in nums if n["target"]]
        real = [n for n in nums if not n["target"]]
        cat = []
        if len(real) > 1:
            cat.append("ada %d angka, dipakai yang pertama (%s)" % (len(real), fmt_angka(real[0]["nilai"])))
        if target_sebut and target_sebut[0] != b["target"]:
            cat.append("target di chat %s berbeda dari rencana %s" % (fmt_angka(target_sebut[0]), fmt_angka(b["target"])))
        if banyak_orang:
            cat.append("klausa menyebut lebih dari satu orang; dipakai %s" % b["orang"])
        if masing:
            cat.append("angka 'masing-masing' dipakai untuk tiap orang yang disebut")
        cat += cek_satuan(real[0], b)
        if real[0]["nilai"] < 0:
            cat.append("angka minus")
        draf.append({"periode": a.periode, "divisi": b["divisi"], "orang": b["orang"], "kpi": b["kpi"],
                     "realisasi": s_dec(real[0]["nilai"]), "catatan": "dari teks: " + kutip[:120],
                     "status_draf": "PERLU KONFIRMASI", "cek": "; ".join(cat),
                     "_kutipan": kutip, "_target": b["target"]})
        return None

    for baris_asli in teks.splitlines():
        baris = baris_asli.strip()
        if not baris:
            continue
        kutip = baris_asli.strip()
        pengirim = None
        m = POLA_WA.match(baris)
        if m:
            pengirim, baris = m.group(1).strip(), m.group(2).strip()
        kini = None
        tercatat = False        # baris ini menghasilkan draf atau catatan "tidak terbaca"
        relevan = False         # baris menyebut orang/KPI/angka

        def tolak(alasan):
            gagal.append({"kutipan": kutip, "alasan": alasan})

        antre = []              # v1.0.2: nama yang disebut tanpa angka ("Wulan & Rudi void masing2 1")
        for kl in pecah_klausa(baris):
            low = kl.lower()
            ditemukan = [n for p_, n in sorted(panggilan.items(), key=lambda x: -len(x[0]))
                         if re.search(r"(?<!\w)%s(?!\w)" % re.escape(p_), low)]
            if ditemukan:
                kini = ditemukan[0]
            elif kini is None and pengirim and norm(pengirim) in panggilan:
                kini = panggilan[norm(pengirim)]
            nums = ambil_angka(kl)
            punya_kata = any(ada_kata(k, low) for k in semua_kata)
            if ditemukan or nums or punya_kata:
                relevan = True
            if not nums:
                if ditemukan and not punya_kata and not POLA_BUKAN_HASIL.search(low):
                    antre += [n_ for n_ in ditemukan if n_ not in antre]
                    continue
                if punya_kata and not POLA_BUKAN_HASIL.search(low):
                    tolak("menyebut orang/KPI tetapi tidak ada angka yang terbaca: \"%s\"" % kl[:60])
                    tercatat = True
                continue
            if POLA_BUKAN_HASIL.search(low):
                tolak("bukan angka hasil kerja (libur/izin/sakit/cuti): \"%s\"" % kl[:60])
                tercatat = True
                continue
            if POLA_KE_DEPAN.search(low):
                tolak("rencana/target ke depan, bukan realisasi: \"%s\"" % kl[:60])
                tercatat = True
                continue
            if all(n["target"] for n in nums):
                if draf and draf[-1]["_kutipan"] == kutip:
                    # "..., target 15" -> target yang disebut untuk klausa sebelumnya
                    sebelumnya = draf[-1]
                    if nums[0]["nilai"] != sebelumnya["_target"]:
                        sebelumnya["cek"] = "; ".join(x for x in (sebelumnya["cek"], "target di chat %s berbeda dari rencana %s"
                                                                  % (fmt_angka(nums[0]["nilai"]), fmt_angka(sebelumnya["_target"]))) if x)
                else:
                    tolak("hanya angka target, tidak ada realisasi: \"%s\"" % kl[:60])
                tercatat = True
                continue
            if kini is None:
                tolak("nama orang tidak dikenali")
                tercatat = True
                continue
            # v1.0.2: "Wulan & Rudi void masing2 1" -> nama tanpa angka di klausa sebelumnya ikut klausa ini
            untuk = []
            for n_ in antre + (ditemukan if POLA_MASING.search(low) else []) + [kini]:
                if n_ not in untuk:
                    untuk.append(n_)
            antre = []
            if len(untuk) > 1 and not POLA_MASING.search(low):
                tolak("angka untuk %s tidak jelas: masing-masing atau total bersama? Tanyakan, lalu tulis per orang "
                      "(mis. \"%s 1, %s 1\"): \"%s\"" % (" & ".join(orang[n_][0]["orang"] for n_ in untuk),
                                                            orang[untuk[0]][0]["orang"], orang[untuk[1]][0]["orang"],
                                                            kl[:60]))
                tercatat = True
                continue
            for n_ in untuk:
                alasan = buat_draf(n_, kl, low, nums, kutip, masing=len(untuk) > 1,
                                   banyak_orang=len(ditemukan) > 1 and len(untuk) == 1)
                if alasan:
                    tolak(alasan if len(untuk) == 1 else "%s: %s" % (orang[n_][0]["orang"], alasan))
            tercatat = True
        if antre and tercatat:
            tolak("%s disebut tanpa angka hasil" % " & ".join(orang[n_][0]["orang"] for n_ in antre))
        if relevan and not tercatat:
            tolak("menyebut orang/KPI tetapi tidak ada angka hasil yang terbaca")
        elif not relevan:
            diabaikan.append(kutip)
    if a.keluar:
        tulis_csv(a.keluar, ["periode", "divisi", "orang", "kpi", "realisasi", "catatan", "status_draf", "cek"], draf)
    data = {"ok": True, "draf": ke_json(draf), "tidak_terbaca": gagal, "diabaikan": diabaikan, "file": a.keluar}
    satuan = {(norm(b["orang"]), norm(b["kpi"])): b["satuan"] for b in rp}
    L = ["DRAF realisasi dari teks — WAJIB dicek sebelum dipakai:"]
    for d in draf:
        nilai = fmt_nilai(Decimal(d["realisasi"]), satuan.get((norm(d["orang"]), norm(d["kpi"])), ""))
        L.append("- %s | %s = %s%s" % (d["orang"], d["kpi"], nilai, " (CEK: %s)" % d["cek"] if d["cek"] else ""))
    if gagal:
        L.append("Tidak terbaca (tanyakan/isi manual):")
        for g in gagal:
            L.append("- \"%s\" → %s" % (g["kutipan"][:80], g["alasan"]))
    if diabaikan:
        L.append("%d baris obrolan tanpa nama/KPI/angka diabaikan." % len(diabaikan))
    cetak(a, data, "\n".join(L))
    return 0


def cmd_okr(a):
    _, rows = baca_tabel(a.okr)
    jalan = angka(a.jalan, "--jalan") if a.jalan is not None else None
    if jalan is not None and jalan > 1:
        jalan = jalan / D100
    if jalan is not None and not (D0 < jalan <= 1):
        raise Gagal("--jalan adalah bagian waktu yang sudah lewat, 0-1 (mis. 0,5 = separuh periode).")
    obj, err, cat = {}, [], []
    for r in rows:
        per = str(r.get("periode", "")).strip()
        if a.periode and per and per != a.periode:
            continue
        o = " ".join(str(r.get("objective", "")).split())
        kr = " ".join(str(r.get("key_result", "")).split())
        if not o and not kr:
            continue
        label = "OKR baris %d (%s)" % (r["_baris"], kr or o)
        if not o or not kr:
            err.append("%s: objective dan key_result wajib diisi." % label)
            continue
        try:
            prog = angka(r.get("progres"), "progres")
            awal = angka(r.get("awal"), "awal")
            target = angka(r.get("target"), "target")
            skrg = angka(r.get("sekarang"), "sekarang")
        except Gagal as e:
            err.append("%s: %s" % (label, e))
            continue
        cara = "progres"
        if prog is not None:
            if "%" in str(r.get("progres")) or prog > 1:
                prog = prog / D100
            if not (D0 <= prog <= 1):
                err.append("%s: progres harus 0-1,0 (atau 0-100%%)." % label)
                continue
        elif None not in (awal, target, skrg):
            if target == awal:
                err.append("%s: target sama dengan nilai awal, progres tidak bisa dihitung." % label)
                continue
            mentah = (skrg - awal) / (target - awal)
            prog = min(max(mentah, D0), Decimal(1))
            cara = "(sekarang-awal)/(target-awal)"
            if mentah > 1:
                cat.append("%s: melampaui target (%s), progres dibatasi 1,0." % (label, fmt_angka(mentah)))
        else:
            err.append("%s: isi kolom progres (0-1,0), atau awal + target + sekarang." % label)
            continue
        kunci = (norm(r.get("pemilik")), o)
        obj.setdefault(kunci, {"pemilik": " ".join(str(r.get("pemilik", "")).split()) or "-", "objective": o,
                               "key_results": []})
        obj[kunci]["key_results"].append({"key_result": kr, "awal": awal, "target": target, "sekarang": skrg,
                                          "progres": prog, "cara": cara})
    if err:
        raise Gagal("Data OKR belum valid:\n- " + "\n- ".join(err))
    if not obj:
        raise Gagal("Tidak ada OKR yang terbaca%s." % (" untuk periode %s" % a.periode if a.periode else ""))
    hasil = []
    for (_, _), v in obj.items():
        n = len(v["key_results"])
        if n < 2 or n > 4:
            cat.append("Objective '%s' punya %d key result. Saran OKR ringan: 2-4 key result." % (v["objective"], n))
        p = sum(k["progres"] for k in v["key_results"]) / n
        for k in v["key_results"]:
            k["status"] = _status_okr(k["progres"], jalan)
        v.update(progres=p, status=_status_okr(p, jalan))
        hasil.append(v)
    L = ["🎯 *OKR%s*%s" % (" — " + a.periode if a.periode else "",
                          " (waktu berjalan %s)" % fmt_angka(bulat(jalan, 2), 2, True) if jalan is not None else "")]
    for v in hasil:
        L.append("%s %s — %s: %s" % (IKON[v["status"]], v["pemilik"], v["objective"], fmt_angka(bulat(v["progres"], 2), 2, True)))
        for k in v["key_results"]:
            L.append("   %s %s: %s" % (IKON[k["status"]], k["key_result"], fmt_angka(bulat(k["progres"], 2), 2, True)))
    if cat:
        L += ["⚠️ " + c for c in cat]
    L.append("Progres 0-1,0. " + ("🟢 ≥ waktu berjalan, 🟡 ≥ 70% dari itu, 🔴 di bawahnya." if jalan is not None
                                  else "🟢 ≥0,7 🟡 ≥0,4 🔴 <0,4 (akhir periode). OKR tidak untuk menilai gaji."))
    cetak(a, {"ok": True, "periode": a.periode, "waktu_berjalan": jalan, "objectives": hasil, "catatan": cat}, "\n".join(L))
    return 0


def _tanggal(t):
    t = str(t).strip()
    m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})(?:[ T].*)?", t)
    if m:
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
    else:
        m = re.fullmatch(r"(\d{1,2})[/.-](\d{1,2})[/.-](\d{2,4})(?:\s.*)?", t)
        if not m:
            return None
        d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        y = y + 2000 if y < 100 else y
    try:
        return datetime.date(y, mo, d)
    except ValueError:
        return None


def cmd_rekap_log(a):
    """Log operasional harian (komplain, respons CS, pengiriman, produksi) -> baris realisasi."""
    _, rows = baca_tabel(a.log)
    grup, err = {}, []
    for r in rows:
        if not norm(r.get("kpi")):
            continue
        label = "Log baris %d" % r["_baris"]
        tg = _tanggal(r.get("tanggal", ""))
        if tg is None:
            err.append("%s: tanggal '%s' tidak terbaca (pakai 2026-09-30 atau 30/09/2026)." % (label, r.get("tanggal", "")))
            continue
        if a.per == "minggu":
            iso = tg.isocalendar()
            per = "%d-W%02d" % (iso[0], iso[1])
        else:
            per = "%d-%02d" % (tg.year, tg.month)
        if a.periode and per != a.periode:
            continue
        cara = norm(r.get("cara")) or "jumlah"
        cara = {"rata": "rata-rata", "rata2": "rata-rata", "average": "rata-rata", "sum": "jumlah",
                "persen-ya": "persen", "%": "persen"}.get(cara, cara)
        if cara not in ("jumlah", "rata-rata", "persen"):
            err.append("%s: cara '%s' tidak dikenal (jumlah / rata-rata / persen)." % (label, r.get("cara")))
            continue
        nilai_t = norm(r.get("nilai"))
        if cara == "persen":
            if nilai_t in ("ya", "y", "1", "ok", "tepat", "selesai", "yes", "true"):
                v = Decimal(1)
            elif nilai_t in ("tidak", "t", "0", "no", "false", "gagal", "telat", "belum"):
                v = D0
            else:
                err.append("%s: cara 'persen' butuh nilai ya/tidak (sekarang '%s')." % (label, r.get("nilai")))
                continue
        else:
            try:
                v = angka(r.get("nilai"), "nilai") if nilai_t else Decimal(1)
            except Gagal as e:
                err.append("%s: %s" % (label, e))
                continue
            if v < 0:
                err.append("%s: nilai negatif." % label)
                continue
        orang = " ".join(str(r.get("orang", "")).split())
        k = (per, " ".join(str(r.get("divisi", "")).split()), orang, " ".join(str(r.get("kpi")).split()))
        g = grup.setdefault(k, {"cara": cara, "nilai": [], "baris": []})
        if g["cara"] != cara:
            err.append("%s: KPI '%s' untuk %s memakai cara berbeda (%s vs %s) di periode yang sama."
                       % (label, k[3], orang or k[1], g["cara"], cara))
            continue
        g["nilai"].append(v)
        g["baris"].append(r["_baris"])
    if err:
        raise Gagal("Log belum bisa direkap:\n- " + "\n- ".join(err[:20]))
    if not grup:
        raise Gagal("Tidak ada baris log%s." % (" untuk periode %s" % a.periode if a.periode else ""))
    hasil = []
    for (per, div, orang, kpi), g in sorted(grup.items()):
        n = len(g["nilai"])
        if g["cara"] == "jumlah":
            v = sum(g["nilai"])
        elif g["cara"] == "rata-rata":
            v = sum(g["nilai"]) / n
        else:
            v = sum(g["nilai"]) / n * D100
        hasil.append({"periode": per, "divisi": div, "orang": orang, "kpi": kpi, "realisasi": s_dec(bulat(v, 2), 2),
                      "catatan": "dari log: %d catatan (%s)" % (n, g["cara"])})
    kolom = ["periode", "divisi", "orang", "kpi", "realisasi", "catatan"]
    if a.keluar:
        tulis_csv(a.keluar, kolom, hasil)
    L = ["Rekap log → realisasi%s:" % (" (disimpan ke %s)" % a.keluar if a.keluar else "")]
    for h in hasil:
        L.append("- %s | %s | %s = %s (%s)" % (h["periode"], h["orang"] or h["divisi"], h["kpi"], h["realisasi"], h["catatan"]))
    cetak(a, {"ok": True, "realisasi": hasil, "file": a.keluar}, "\n".join(L))
    return 0


def _status_okr(p, jalan):
    if jalan is None:
        return "hijau" if p >= Decimal("0.7") else ("kuning" if p >= Decimal("0.4") else "merah")
    if p >= jalan:
        return "hijau"
    return "kuning" if p >= jalan * Decimal("0.7") else "merah"


# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# ekspor-db: rencana + skor + riwayat -> SQLite lokal (dasbor-lokal/Datasette) + CSV Grist
# ---------------------------------------------------------------------------
SKEMA_DB = """
CREATE TABLE meta (kunci TEXT PRIMARY KEY, nilai TEXT);
CREATE TABLE rencana (
  periode_berlaku TEXT, divisi TEXT, orang TEXT, kpi TEXT, satuan TEXT, arah TEXT,
  bobot REAL, target REAL, ambang REAL, maks_capai REAL, sumber TEXT);
CREATE TABLE skor_kpi (
  periode TEXT NOT NULL, tingkat TEXT NOT NULL, divisi TEXT, orang TEXT, kpi TEXT, satuan TEXT, arah TEXT,
  bobot REAL, target REAL, ambang REAL, realisasi REAL, capaian_persen REAL, capaian_dipakai REAL,
  nilai REAL, status TEXT, tren_capaian REAL);
CREATE TABLE skor_orang (
  periode TEXT NOT NULL, divisi TEXT, orang TEXT, skor REAL, status TEXT, tren REAL, lengkap INTEGER,
  dasar TEXT, jumlah_kpi INTEGER, jumlah_kpi_kosong INTEGER, jumlah_kpi_merah INTEGER);
CREATE TABLE skor_divisi (
  periode TEXT NOT NULL, divisi TEXT, skor REAL, status TEXT, tren REAL, dasar_skor TEXT,
  jumlah_orang INTEGER, jumlah_belum_lengkap INTEGER, sebagian INTEGER);
CREATE TABLE skor_perusahaan (
  periode TEXT NOT NULL, skor REAL, status TEXT, tren REAL, dasar TEXT,
  jumlah_divisi_tanpa_skor INTEGER, sebagian INTEGER);
CREATE INDEX i_skor_kpi ON skor_kpi(periode, status);
CREATE INDEX i_skor_orang ON skor_orang(periode, divisi);
"""
TABEL_EKSPOR = ["rencana", "skor_kpi", "skor_orang", "skor_divisi", "skor_perusahaan"]
PERINGATAN_LOKAL = ("Dasbor ini HANYA untuk komputer ini (127.0.0.1). Jangan dibuka ke jaringan/internet "
                    "(tanpa 0.0.0.0, port-forward, atau tunnel) dan jangan dibagikan: skor per orang adalah "
                    "data pribadi karyawan, bahan diskusi, bukan dasar sanksi/PHK.")


def _r(d, n):
    return None if d is None else float(bulat(d, n))


def _baca_kunci(path):
    peta = {"orang": {}, "divisi": {}}
    if path.is_file():
        with path.open(encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                if r.get("jenis") in peta and r.get("nama") and r.get("kode"):
                    peta[r["jenis"]][norm(r["nama"])] = r["kode"]
    return peta


def _buat_kode(jenis, nama_asli, peta, awalan, lebar):
    """Beri kode acak (bukan urut abjad) ke nama yang belum punya; kode lama dipertahankan."""
    import random
    dipakai = set(peta[jenis].values())
    baru = [n for n in nama_asli if norm(n) not in peta[jenis]]
    kandidat = [awalan + str(i).zfill(lebar) for i in range(1, len(dipakai) + len(baru) + 1)]
    kandidat = [k for k in kandidat if k not in dipakai]
    random.SystemRandom().shuffle(kandidat)
    for n, k in zip(baru, kandidat):
        peta[jenis][norm(n)] = k


def _tulis_csv_lurus(path, kolom, baris):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(kolom)
        for b in baris:
            w.writerow(["" if v is None else v for v in b])


def bangun_tabel_ekspor(rencana, per_periode, ok, dv):
    """Susun baris tiap tabel dari hasil hitung_periode (ok/dv = fungsi penamaan orang/divisi)."""
    T = {t: [] for t in TABEL_EKSPOR}
    for b in rencana:
        T["rencana"].append((b["periode"], dv(b["divisi"]), ok(b["orang"]) if b["orang"] else None, b["kpi"],
                             b["satuan"], b["arah"], _r(b["bobot"], 4), _r(b["target"], 4), _r(b["ambang"], 4),
                             _r(b["maks_capai"], 4), b.get("sumber", "")))

    def baris_kpi(p, tingkat, divisi, orang, k):
        return (p, tingkat, divisi, orang, k["kpi"], k["satuan"], k["arah"], _r(k["bobot"], 4), _r(k["target"], 4),
                _r(k["ambang"], 4), _r(k["realisasi"], 4), _r(k["capaian_mentah"], 1), _r(k["capaian"], 1),
                _r(k["kontribusi"], 2), k["status"], _r(k.get("tren_capaian"), 1))
    for p, h in per_periode:
        for o in h["orang"]:
            for k in o["kpi"]:
                T["skor_kpi"].append(baris_kpi(p, "orang", dv(o["divisi"]), ok(o["nama"]), k))
            T["skor_orang"].append((p, dv(o["divisi"]), ok(o["nama"]), _r(o["skor"], 1), o["status"],
                                    _r(o.get("tren"), 1), int(bool(o["lengkap"])), o["dasar"], len(o["kpi"]),
                                    sum(1 for k in o["kpi"] if k["kosong"]),
                                    sum(1 for k in o["kpi"] if k["status"] == "merah")))
        for d in h["divisi"]:
            for k in d["kpi"]:
                T["skor_kpi"].append(baris_kpi(p, "divisi", dv(d["nama"]), None, k))
            T["skor_divisi"].append((p, dv(d["nama"]), _r(d["skor"], 1), d["status"], _r(d.get("tren"), 1),
                                     d["dasar_skor"], d["jumlah_orang"], len(d["belum_lengkap"]), int(d["sebagian"])))
        c = h["perusahaan"]
        T["skor_perusahaan"].append((p, _r(c["skor"], 1), c["status"], _r(c.get("tren"), 1), c["dasar"],
                                     len(c["divisi_tanpa_skor"]), int(c["sebagian"])))
    return T


def cmd_ekspor_db(a):
    import sqlite3
    import shutil
    siapkan_aturan(a)
    rencana, err, cat = baca_rencana(a.rencana)
    if err:
        raise Gagal("Rencana KPI belum valid:\n- " + "\n- ".join(err))
    realisasi, masalah = baca_realisasi(a.realisasi, a.periode_default, a.izinkan_minus)
    periodes = sorted({r["periode"] for r in realisasi if r["periode"]})
    if not periodes:
        raise Gagal("Tidak ada periode di file realisasi. Isi kolom 'periode' atau pakai --periode-default 2026-09.")
    folder = Path(a.keluar).expanduser()
    file_db = folder / "kpi.db"
    if file_db.exists() and not a.timpa:
        raise Gagal("%s sudah ada. Pakai --timpa untuk menggantinya (database ini hanya ringkasan; "
                    "sumber aslinya tetap file rencana & realisasi)." % file_db)
    peringatan = list(masalah)
    hitung = {}
    for p in periodes:
        h = hitung_periode(rencana, realisasi, p, a, peringatan)
        if h is None:
            continue
        ada = any(not k["kosong"] for o in h["orang"] for k in o["kpi"]) or \
            any(not k["kosong"] for d in h["divisi"] for k in d["kpi"])
        if ada:
            hitung[p] = h
    dilewati = [p for p in periodes if p not in hitung]
    if not hitung:
        raise Gagal("Tidak ada periode yang bisa dihitung (rencana tidak berlaku atau realisasi kosong). "
                    "Tidak ada database dibuat.")
    for p, h in hitung.items():          # tren: aturan sama dengan perintah skor
        lalu = periode_sebelumnya(periodes, p)
        hl = hitung.get(lalu) if lalu else None
        h["periode_lalu"] = None
        if hl is not None and (any(o["skor"] is not None for o in hl["orang"]) or
                               any(d["skor"] is not None for d in hl["divisi"])):
            tambah_tren(h, hl)
            h["periode_lalu"] = lalu
    ok, dv = (lambda x: x), (lambda x: x)
    kunci_path = folder / "kunci-kode-RAHASIA.csv"
    peta = None
    if a.anonim:
        peta = _baca_kunci(kunci_path)
        semua_orang = sorted({b["orang"] for b in rencana if b["orang"]})
        semua_divisi = sorted({b["divisi"] for b in rencana})
        _buat_kode("orang", semua_orang, peta, "P", max(2, len(str(len(semua_orang) + len(peta["orang"])))))
        if a.anonim_divisi:
            _buat_kode("divisi", semua_divisi, peta, "D", 2)
        ok = lambda x: peta["orang"][norm(x)] if x else x
        dv = (lambda x: peta["divisi"][norm(x)]) if a.anonim_divisi else (lambda x: x)
    T = bangun_tabel_ekspor(rencana, list(hitung.items()), ok, dv)
    if a.anonim:                          # urutan sisip tidak boleh membocorkan urutan abjad nama asli
        for t in T:
            T[t].sort(key=lambda r: tuple("" if v is None else str(v) for v in r))
    folder.mkdir(parents=True, exist_ok=True)
    if file_db.exists():
        file_db.unlink()
    conn = sqlite3.connect(str(file_db))
    try:
        conn.execute("PRAGMA journal_mode=DELETE")
        conn.executescript(SKEMA_DB)
        kolom = {}
        for t, baris in T.items():
            kolom[t] = [x[1] for x in conn.execute("PRAGMA table_info(%s)" % t)]
            if baris:
                conn.executemany("INSERT INTO %s VALUES (%s)" % (t, ",".join("?" * len(baris[0]))), baris)
        meta = {"skema": "1", "dibuat_oleh": "kpi-tim %s" % VERSI, "anonim": "ya" if a.anonim else "tidak",
                "divisi_anonim": "ya" if (a.anonim and a.anonim_divisi) else "tidak",
                "periode": ",".join(hitung), "hijau": s_dec(a.hijau), "kuning": s_dec(a.kuning),
                "cap": s_dec(a.cap), "data_kosong": a.data_kosong, "peringatan_lokal": PERINGATAN_LOKAL,
                "dibuat_pada": datetime.date.today().isoformat()}
        conn.executemany("INSERT INTO meta VALUES (?,?)", list(meta.items()))
        conn.commit()
    finally:
        conn.close()
    berkas = [str(file_db)]
    tpl = Path(__file__).resolve().parent.parent / "templates" / "metadata-kpi.yml"
    if tpl.is_file():
        shutil.copyfile(str(tpl), str(folder / "kpi-metadata.yml"))
        berkas.append(str(folder / "kpi-metadata.yml"))
    if a.anonim:
        with kunci_path.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["jenis", "kode", "nama"])
            asli = {"orang": {norm(b["orang"]): b["orang"] for b in rencana if b["orang"]},
                    "divisi": {norm(b["divisi"]): b["divisi"] for b in rencana}}
            for jenis in ("orang", "divisi"):
                for n, kode in sorted(peta[jenis].items(), key=lambda kv: kv[1]):
                    w.writerow([jenis, kode, asli[jenis].get(n, n)])
        berkas.append(str(kunci_path))
    if a.grist:
        gd = folder / "grist"
        gd.mkdir(parents=True, exist_ok=True)
        for t in TABEL_EKSPOR:
            _tulis_csv_lurus(str(gd / (t + ".csv")), kolom[t], T[t])
            berkas.append(str(gd / (t + ".csv")))
        (gd / "PETUNJUK-IMPOR-GRIST.md").write_text(PETUNJUK_GRIST, encoding="utf-8")
        berkas.append(str(gd / "PETUNJUK-IMPOR-GRIST.md"))
    perintah = 'datasette -i "%s" -m "%s" --host 127.0.0.1' % (file_db, folder / "kpi-metadata.yml")
    data = {"ok": True, "versi": VERSI, "db": str(file_db), "periode": list(hitung), "periode_dilewati": dilewati,
            "anonim": bool(a.anonim), "jumlah_baris": {t: len(T[t]) for t in T}, "berkas": berkas,
            "peringatan_data_jumlah": len(peringatan), "perintah_datasette": perintah,
            "peringatan_lokal": PERINGATAN_LOKAL}
    L = ["✅ Database KPI ditulis: %s" % file_db,
         "Periode: %s%s" % (", ".join(hitung), " (dilewati, tanpa data/rencana: %s)" % ", ".join(dilewati) if dilewati else ""),
         "Baris: " + ", ".join("%s %d" % (t, len(T[t])) for t in T),
         "Mode: %s" % ("ANONIM (kode P01.., nama ada di kunci-kode-RAHASIA.csv; simpan terpisah, jangan dibagikan)"
                       if a.anonim else "dengan nama orang (data pribadi karyawan)")]
    if peringatan:
        L.append("⚠️ %d peringatan data (nama KPI salah ketik, duplikat, dll.); jalankan 'skor' untuk rinciannya."
                 % len(peringatan))
    L += ["", "Buka dasbor (hanya di komputer ini, baca-saja):", "  " + perintah, "  lalu buka http://127.0.0.1:8001",
          "⚠️ " + PERINGATAN_LOKAL]
    if a.grist:
        L.append("CSV untuk Grist: %s (petunjuk: PETUNJUK-IMPOR-GRIST.md)" % (folder / "grist"))
    cetak(a, data, "\n".join(L))
    return 0


PETUNJUK_GRIST = """# Impor KPI Tim ke Grist (untuk yang sudah memakai Grist)

File di folder ini = satu CSV per tabel, isinya sama dengan database `kpi.db`
(angka sudah dihitung `skor_kpi.py`; Grist hanya menampilkan, jangan menghitung ulang).

| File | Isi |
|---|---|
| skor_perusahaan.csv | skor perusahaan per periode |
| skor_divisi.csv | skor tiap divisi per periode |
| skor_orang.csv | skor tiap orang per periode |
| skor_kpi.csv | rincian tiap KPI (target, realisasi, capaian, status) |
| rencana.csv | rencana KPI (bobot, target, ambang) |

## Langkah (Grist Desktop atau Grist di komputer sendiri)
1. Buka Grist, buat dokumen kosong: **Add New > Add Empty Document**, beri nama "KPI Tim".
2. **Add New > Import from file**, pilih `skor_perusahaan.csv`. Di layar pratinjau biarkan
   pilihan bawaan, klik **Import**. Ulangi untuk keempat file lainnya (satu tabel per file).
3. Kolom `periode` dibiarkan bertipe Teks (contoh 2026-09). Kolom angka (skor, target, ...)
   otomatis terbaca Angka. Kolom `status` berisi hijau/kuning/merah/belum.
4. Warna semaphore: pilih kolom `status` > **Column Options > Cell Style** > **Add another rule**,
   isi kondisi `$status == "merah"` (warna merah), lalu `"kuning"` dan `"hijau"`.
5. Grafik tren: **Add New > Add Page > Select Widget: Chart**, sumber `skor_perusahaan`,
   sumbu X `periode`, sumbu Y `skor`. Per divisi: sumber `skor_divisi`, satu seri per `divisi`.
6. Bulan berikutnya: jalankan lagi `skor_kpi.py ekspor-db ... --timpa --grist`, lalu di Grist hapus
   isi tiap tabel dan **Import from file** lagi (paling sederhana), atau pakai **Update existing
   table** dengan kunci `periode` (+ `divisi`/`orang`/`kpi` bila ada).

## Yang perlu diingat
- Grist hanya di komputer sendiri (alamat `localhost`). Jangan buka ke internet atau tautan
  publik: isinya skor per orang = data pribadi karyawan.
- Lebih aman: ekspor dengan `--anonim` (nama diganti kode P01, P02, ...). Tabel kuncinya ada di
  `kunci-kode-RAHASIA.csv` (bukan di folder ini); simpan terpisah dan jangan dibagikan.
- Skor adalah bahan diskusi, bukan dasar sanksi atau PHK.
- Panduan Grist: `docs/panduan-grist.md`. Skill `grist-usaha` membantu tabel/rumus tambahan.
  Perintah `impor-csv` miliknya hanya untuk tabel yang SUDAH ada di Grist dan butuh REST API
  (Docker), jadi untuk pertama kali pakai langkah Import di atas.
"""


def buat_parser():
    ap = argparse.ArgumentParser(prog="skor_kpi.py", description="KPI & target tim UMKM (Komunitech kpi-tim)")
    ap.add_argument("--versi", action="version", version=VERSI)
    sub = ap.add_subparsers(dest="cmd")

    def umum(p):
        p.add_argument("--json", action="store_true", help="Output JSON")

    p = sub.add_parser("katalog", help="Daftar KPI bawaan per peran")
    p.add_argument("--peran")
    umum(p)

    p = sub.add_parser("template", help="Buat rencana KPI CSV+XLSX dari daftar tim")
    p.add_argument("--tim", required=True, help="CSV/XLSX: nama, divisi, peran")
    p.add_argument("--periode", default="", help="mis. 2026-10 (bulanan), 2026-W41 (mingguan), 2026-Q4")
    p.add_argument("--keluar", required=True, help="Folder hasil")
    p.add_argument("--timpa", action="store_true")
    umum(p)

    p = sub.add_parser("cek", help="Periksa rencana KPI")
    p.add_argument("--rencana", required=True)
    umum(p)

    p = sub.add_parser("baca-teks", help="Teks grup WA -> draf realisasi (perlu konfirmasi)")
    p.add_argument("--rencana", required=True)
    p.add_argument("--teks", required=True, help="File .txt atau '-' untuk stdin")
    p.add_argument("--periode", required=True)
    p.add_argument("--keluar", help="Tulis draf ke CSV ini")
    umum(p)

    p = sub.add_parser("skor", help="Hitung skor KPI")
    p.add_argument("--rencana", required=True)
    p.add_argument("--realisasi", required=True)
    p.add_argument("--periode", help="Periode yang dinilai (default: periode terbaru di file realisasi)")
    p.add_argument("--periode-lalu", help="Periode pembanding tren (default: periode sebelumnya di file)")
    p.add_argument("--periode-default", help="Periode untuk baris realisasi yang kolom periodenya kosong")
    p.add_argument("--data-kosong", choices=["tandai", "bobot-ulang", "nol"], default="tandai")
    p.add_argument("--min-bobot", default="50", help="Mode bobot-ulang: minimal %% bobot yang ada datanya (default 50)")
    p.add_argument("--cap", default="120", help="Batas capaian per KPI dalam %% (default 120)")
    p.add_argument("--hijau", default="100")
    p.add_argument("--kuning", default="80")
    p.add_argument("--bobot-divisi", help="\"Sales=50,Gudang=30,Keuangan=20\" (default: bobot sama)")
    p.add_argument("--duplikat", choices=["tolak", "jumlah", "terakhir"], default="tolak")
    p.add_argument("--izinkan-minus", action="store_true")
    p.add_argument("--orang", help="Rincian satu orang (bahan 1:1)")
    p.add_argument("--tanpa-nama", action="store_true", help="Hanya perusahaan & divisi")
    p.add_argument("--csv-keluar", help="Simpan rincian skor ke CSV")
    p.add_argument("--judul", default="")
    p.add_argument("--maks-peringatan", type=int, default=5)
    umum(p)

    p = sub.add_parser("ekspor-db", help="Tulis rencana+skor+riwayat ke SQLite lokal (dasbor-lokal/Datasette) & CSV Grist")
    p.add_argument("--rencana", required=True)
    p.add_argument("--realisasi", required=True)
    p.add_argument("--keluar", required=True, help="Folder hasil (kpi.db, kpi-metadata.yml, ...)")
    p.add_argument("--periode-default", help="Periode untuk baris realisasi yang kolom periodenya kosong")
    p.add_argument("--data-kosong", choices=["tandai", "bobot-ulang", "nol"], default="tandai")
    p.add_argument("--min-bobot", default="50")
    p.add_argument("--cap", default="120")
    p.add_argument("--hijau", default="100")
    p.add_argument("--kuning", default="80")
    p.add_argument("--bobot-divisi")
    p.add_argument("--duplikat", choices=["tolak", "jumlah", "terakhir"], default="tolak")
    p.add_argument("--izinkan-minus", action="store_true")
    p.add_argument("--anonim", action="store_true", help="Ganti nama orang dengan kode P01.. (kunci di file terpisah)")
    p.add_argument("--anonim-divisi", action="store_true", help="Dengan --anonim: nama divisi juga jadi kode D01..")
    p.add_argument("--grist", action="store_true", help="Tulis juga satu CSV per tabel + petunjuk impor Grist")
    p.add_argument("--timpa", action="store_true", help="Ganti kpi.db yang sudah ada")
    umum(p)

    p = sub.add_parser("rekap-log", help="Log operasional harian -> baris realisasi")
    p.add_argument("--log", required=True, help="CSV/XLSX: tanggal, divisi, orang, kpi, nilai, cara")
    p.add_argument("--per", choices=["bulan", "minggu"], default="bulan")
    p.add_argument("--periode", help="Hanya periode ini (mis. 2026-09 atau 2026-W40)")
    p.add_argument("--keluar", help="Tulis hasil ke CSV (format realisasi)")
    umum(p)

    p = sub.add_parser("okr", help="Progres OKR ringan")
    p.add_argument("--okr", required=True)
    p.add_argument("--periode")
    p.add_argument("--jalan", help="Bagian waktu periode yang sudah lewat, 0-1 (mis. 0,5)")
    umum(p)
    return ap


PERINTAH = {"katalog": cmd_katalog, "template": cmd_template, "cek": cmd_cek, "baca-teks": cmd_baca_teks,
            "skor": cmd_skor, "ekspor-db": cmd_ekspor_db, "okr": cmd_okr, "rekap-log": cmd_rekap_log}


def main(argv=None):
    ap = buat_parser()
    a = ap.parse_args(argv)
    if not a.cmd:
        ap.print_help()
        return 1
    try:
        return PERINTAH[a.cmd](a)
    except (Gagal, OSError) as e:
        pesan = str(e)
        if isinstance(e, OSError):
            pesan = ("File/folder tidak bisa dibaca atau ditulis (%s). Jika file sedang dibuka di Excel, "
                     "tutup dulu, atau pilih lokasi lain." % (getattr(e, "filename", None) or e))
        if getattr(a, "json", False):
            print(json.dumps({"ok": False, "error": pesan}, ensure_ascii=False, indent=2))
        else:
            print("❌ " + pesan)
        return 1


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except (ValueError, OSError):
            pass
    try:
        kode = main()
        sys.stdout.flush()
    except BrokenPipeError:
        # output dipotong (mis. "| head"): diam, bukan traceback
        try:
            sys.stdout = open(os.devnull, "w")
        except OSError:
            pass
        kode = 0
    sys.exit(kode)
