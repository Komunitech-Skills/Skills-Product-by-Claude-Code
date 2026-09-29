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
import difflib
import io
import json
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from pathlib import Path
from xml.sax.saxutils import escape

VERSI = "1.0.0"
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
    neg = t.startswith("-") or (t.startswith("(") and t.endswith(")"))
    t = re.sub(r"(?i)\b(rp|idr)\.?", "", t)
    t = t.replace("%", "").replace(" ", "").replace(" ", "").strip("()+-")
    t = re.sub(r"(?i)x$", "", t)
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
    d = Decimal(t)
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


def rencana_periode(rencana, periode):
    """Baris rencana yang berlaku untuk periode ini (baris khusus periode menggantikan baris umum)."""
    per_pemilik = {}
    for b in rencana:
        per_pemilik.setdefault(pemilik_kunci(b), []).append(b)
    hasil = []
    for pk, bs in per_pemilik.items():
        khusus = [b for b in bs if b["periode"] == periode]
        hasil += khusus if khusus else [b for b in bs if not b["periode"]]
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
        if norm(r.get("status_draf")) == "perlu konfirmasi":
            masalah.append("%s: masih DRAF dari teks (status_draf = PERLU KONFIRMASI) -> dilewati. Setelah "
                           "pemilik/manajer memastikan angkanya, ubah status_draf menjadi 'dikonfirmasi'." % label)
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


def kpi_terlemah(o, n=1):
    ada = [k for k in o["kpi"] if not k["kosong"] and k["capaian"] is not None]
    ada.sort(key=lambda k: (k["capaian"], norm(k["kpi"])))
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
        info = fmt_skor(d["skor"]) if d["skor"] is not None else "belum lengkap"
        ext = ""
        if d["sebagian"]:
            ext = " (tanpa %s)" % ", ".join(d["belum_lengkap"])
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
            if lemah and lemah[0]["status"] != "hijau":
                catat = " — perlu perhatian: %s %s" % (lemah[0]["kpi"], fmt_pct(lemah[0]["capaian_mentah"]))
            if o["dasar"] == "bobot-ulang":
                catat += " (dihitung dari %s%% bobot)" % fmt_angka(o["bobot_tersedia"] * D100 / o["bobot_total"], 0)
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
            L.append("⚪ %s — belum ada data (bobot %s%%, target %s)" % (k["kpi"], fmt_angka(k["bobot"]),
                                                                     fmt_nilai(k["target"], k["satuan"])))
            continue
        arah = "↑" if k["arah"] == "naik" else "↓"
        tc = fmt_tren(k.get("tren_capaian"))
        batas = " (dibatasi %s%%)" % fmt_angka(k["maks_capai"], 0) if k["capaian_mentah"] > k["capaian"] else ""
        L.append("%s %s %s: %s dari target %s → capaian %s%s, bobot %s%%, nilai %s%s"
                 % (IKON[k["status"]], k["kpi"], arah, fmt_nilai(k["realisasi"], k["satuan"]),
                    fmt_nilai(k["target"], k["satuan"]), fmt_pct(k["capaian_mentah"]), batas,
                    fmt_angka(k["bobot"]), fmt_skor(k["kontribusi"]), " " + tc if tc else ""))
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
            rencana.append({"periode": a.periode or "", "divisi": t.get("divisi", "") or peran.title(),
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
    h = hitung_periode(rencana, realisasi, periode, a, peringatan)
    if h is None:
        raise Gagal("Tidak ada rencana KPI untuk periode %s." % periode)
    ada_data = any(not k["kosong"] for o in h["orang"] for k in o["kpi"]) or \
        any(not k["kosong"] for d in h["divisi"] for k in d["kpi"])
    if not ada_data:
        raise Gagal("Belum ada satu pun realisasi untuk periode %s. Laporan tidak dibuat (tidak mengirim angka nol)." % periode)
    lalu = a.periode_lalu or periode_sebelumnya(periodes, periode)
    h["periode_lalu"] = None
    if lalu:
        hl = hitung_periode(rencana, realisasi, lalu, a, [], periksa=False)
        if hl:
            tambah_tren(h, hl)
            h["periode_lalu"] = lalu
    for o in h["orang"]:
        if o["skor"] is None and a.data_kosong == "tandai":
            peringatan.append("%s belum lengkap (tidak ikut rata-rata divisi): belum ada data %s."
                              % (o["nama"], ", ".join(o["kurang"])))
        elif o["dasar"] == "bobot-ulang":
            peringatan.append("%s: skor dihitung ulang dari KPI yang ada (%s%% bobot); belum ada data %s."
                              % (o["nama"], fmt_angka(o["bobot_tersedia"] * D100 / o["bobot_total"], 1), ", ".join(o["kurang"])))
        elif o["kurang"] and a.data_kosong == "nol":
            peringatan.append("%s: KPI tanpa data dihitung 0%% (--data-kosong nol): %s." % (o["nama"], ", ".join(o["kurang"])))
    for d in h["divisi"]:
        if d["dasar_skor"] == "kpi-divisi" and d["kurang"]:
            peringatan.append("KPI divisi %s belum ada data: %s." % (d["nama"], ", ".join(d["kurang"])))
    aturan = {"cap": a.cap, "hijau": a.hijau, "kuning": a.kuning, "data_kosong": a.data_kosong,
              "min_bobot": a.min_bobot, "duplikat": a.duplikat}
    if a.csv_keluar:
        tulis_csv(a.csv_keluar, KOLOM_HASIL, baris_csv_hasil(h))
    data = {"ok": True, "versi": VERSI, "aturan": aturan, "catatan_rencana": cat, "peringatan": peringatan}
    data.update(h)
    if a.tanpa_nama:
        data.pop("orang")
        data["peringatan"] = [w for w in peringatan if not any(norm(o["nama"]) in norm(w) for o in h["orang"])]
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


def pecah_klausa(baris):
    return [k.strip() for k in re.split(r"[;,]\s+|\s+dan\s+|\s+&\s+|\n", baris) if k.strip()]


POLA_ANGKA = re.compile(r"(?<![\w.,])(\d+(?:[.,]\d+)*)\s*(jt|juta|rb|ribu|k|m|%)?(?![\w])", re.I)
POLA_WA = re.compile(r"^\[?\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4}[, ]+\d{1,2}[.:]\d{2}(?:[.:]\d{2})?\]?\s*(?:-\s*)?([^:]{1,40}):\s*(.*)$")


def ambil_angka(klausa):
    """Kembalikan list (Decimal, posisi_awal, kata_sebelum)."""
    hasil = []
    for m in POLA_ANGKA.finditer(klausa):
        try:
            v = angka(m.group(1))
        except Gagal:
            continue
        suf = (m.group(2) or "").lower()
        if suf in ("jt", "juta", "m"):
            v = v * Decimal(1000000)
        elif suf in ("rb", "ribu", "k"):
            v = v * Decimal(1000)
        sebelum = klausa[max(0, m.start() - 12):m.start()].lower()
        hasil.append((v, m.start(), sebelum))
    return hasil


def cmd_baca_teks(a):
    rencana, err, _ = baca_rencana(a.rencana)
    if err:
        raise Gagal("Rencana KPI belum valid:\n- " + "\n- ".join(err))
    rp = rencana_periode(rencana, a.periode)
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
    draf, gagal = [], []
    for baris_asli in teks.splitlines():
        baris = baris_asli.strip()
        if not baris:
            continue
        pengirim = None
        m = POLA_WA.match(baris)
        if m:
            pengirim, baris = m.group(1).strip(), m.group(2).strip()
        kini = None
        for kl in pecah_klausa(baris):
            low = kl.lower()
            ditemukan = [n for p_, n in sorted(panggilan.items(), key=lambda x: -len(x[0]))
                         if re.search(r"(?<!\w)%s(?!\w)" % re.escape(p_), low)]
            if ditemukan:
                kini = ditemukan[0]
            elif kini is None and pengirim and norm(pengirim) in panggilan:
                kini = panggilan[norm(pengirim)]
            nums = ambil_angka(kl)
            if not nums:
                continue
            if all("target" in sb for _, _, sb in nums) and draf and draf[-1]["_kutipan"] == baris_asli.strip():
                # "..., target 15" -> target yang disebut untuk klausa sebelumnya
                sebelumnya = draf[-1]
                if nums[0][0] != sebelumnya["_target"]:
                    sebelumnya["cek"] = "; ".join(x for x in (sebelumnya["cek"], "target di chat %s berbeda dari rencana %s"
                                                              % (fmt_angka(nums[0][0]), fmt_angka(sebelumnya["_target"]))) if x)
                continue
            if kini is None:
                gagal.append({"kutipan": baris_asli.strip(), "alasan": "nama orang tidak dikenali"})
                continue
            kandidat = []
            for b in orang[kini]:
                kata = [k.strip().lower() for k in str(b.get("kata_kunci") or "").split(";") if k.strip()]
                kata += [w for w in norm(b["kpi"]).split() if len(w) >= 4]
                skor = sum(len(k) for k in set(kata) if re.search(r"(?<!\w)%s" % re.escape(k), low))
                if skor:
                    kandidat.append((skor, b))
            kandidat.sort(key=lambda x: -x[0])
            if not kandidat or (len(kandidat) > 1 and kandidat[0][0] == kandidat[1][0]):
                gagal.append({"kutipan": baris_asli.strip(),
                              "alasan": "KPI tidak jelas" if not kandidat else "cocok ke lebih dari satu KPI"})
                continue
            b = kandidat[0][1]
            target_sebut = [v for v, _, sb in nums if "target" in sb]
            real = [v for v, _, sb in nums if "target" not in sb]
            if not real:
                gagal.append({"kutipan": baris_asli.strip(), "alasan": "hanya ada angka target, realisasi tidak ada"})
                continue
            cat = []
            if len(real) > 1:
                cat.append("ada %d angka, dipakai yang pertama (%s)" % (len(real), fmt_angka(real[0])))
            if target_sebut and target_sebut[0] != b["target"]:
                cat.append("target di chat %s berbeda dari rencana %s" % (fmt_angka(target_sebut[0]), fmt_angka(b["target"])))
            draf.append({"periode": a.periode, "divisi": b["divisi"], "orang": b["orang"], "kpi": b["kpi"],
                         "realisasi": s_dec(real[0]), "catatan": "dari teks: " + baris_asli.strip()[:120],
                         "status_draf": "PERLU KONFIRMASI", "cek": "; ".join(cat),
                         "_kutipan": baris_asli.strip(), "_target": b["target"]})
    if a.keluar:
        tulis_csv(a.keluar, ["periode", "divisi", "orang", "kpi", "realisasi", "catatan", "status_draf", "cek"], draf)
    data = {"ok": True, "draf": ke_json(draf), "tidak_terbaca": gagal, "file": a.keluar}
    satuan = {(norm(b["orang"]), norm(b["kpi"])): b["satuan"] for b in rp}
    L = ["DRAF realisasi dari teks — WAJIB dicek sebelum dipakai:"]
    for d in draf:
        nilai = fmt_nilai(Decimal(d["realisasi"]), satuan.get((norm(d["orang"]), norm(d["kpi"])), ""))
        L.append("- %s | %s = %s%s" % (d["orang"], d["kpi"], nilai, " (cek: %s)" % d["cek"] if d["cek"] else ""))
    if gagal:
        L.append("Tidak terbaca (isi manual):")
        for g in gagal:
            L.append("- \"%s\" → %s" % (g["kutipan"][:80], g["alasan"]))
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
                          " (waktu berjalan %s)" % fmt_angka(bulat(jalan, 2), 2) if jalan is not None else "")]
    for v in hasil:
        L.append("%s %s — %s: %s" % (IKON[v["status"]], v["pemilik"], v["objective"], fmt_angka(bulat(v["progres"], 2), 2)))
        for k in v["key_results"]:
            L.append("   %s %s: %s" % (IKON[k["status"]], k["key_result"], fmt_angka(bulat(k["progres"], 2), 2)))
    if cat:
        L += ["⚠️ " + c for c in cat]
    L.append("Progres 0-1,0. " + ("🟢 ≥ waktu berjalan, 🟡 ≥ 70% dari itu, 🔴 di bawahnya." if jalan is not None
                                  else "🟢 ≥0,7 🟡 ≥0,4 🔴 <0,4 (akhir periode). OKR tidak untuk menilai gaji."))
    cetak(a, {"ok": True, "periode": a.periode, "waktu_berjalan": jalan, "objectives": hasil, "catatan": cat}, "\n".join(L))
    return 0


def _status_okr(p, jalan):
    if jalan is None:
        return "hijau" if p >= Decimal("0.7") else ("kuning" if p >= Decimal("0.4") else "merah")
    if p >= jalan:
        return "hijau"
    return "kuning" if p >= jalan * Decimal("0.7") else "merah"


# ---------------------------------------------------------------------------
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

    p = sub.add_parser("okr", help="Progres OKR ringan")
    p.add_argument("--okr", required=True)
    p.add_argument("--periode")
    p.add_argument("--jalan", help="Bagian waktu periode yang sudah lewat, 0-1 (mis. 0,5)")
    umum(p)
    return ap


PERINTAH = {"katalog": cmd_katalog, "template": cmd_template, "cek": cmd_cek, "baca-teks": cmd_baca_teks,
            "skor": cmd_skor, "okr": cmd_okr}


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
    sys.exit(main())
