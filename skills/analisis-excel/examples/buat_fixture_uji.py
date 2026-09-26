#!/usr/bin/env python3
"""Pembuat fixture uji independen (Tahap 6) untuk skill analisis-excel.

Dibuat oleh PENGUJI independen (bukan pembuat skill). Hanya Python standar.
Menghasilkan (di folder tujuan, default ./fixture-uji):
  - "Penjualan 2026.xlsx"   skenario 01 (XLSX tulis-tangan meniru keluaran Excel: sharedStrings,
                              styles numFmt tanggal & Rp, sheet tersembunyi, sel gabungan, rumus
                              dengan & tanpa nilai tersimpan, baris TOTAL)
  - "Penjualan 2026 (1904).xlsx"  sama, sistem tanggal 1904
  - "lembur-sep-2026.csv"   skenario 02 (cp1252, pemisah ;)
  - "iuran-komite.csv"      skenario 03 (header baris 4, sel kosong, duplikat)
  - file rusak untuk uji data buruk
  - "kunci-jawaban.json"    angka kebenaran, dihitung dari data sumber (tidak memakai script skill)

Jalankan: python3 buat_fixture_uji.py [folder_tujuan]   (Windows: py buat_fixture_uji.py)
Deterministik (random.seed tetap) sehingga angka di examples/01-05 bisa diulang.
"""
import json
import random
import sys
import zipfile
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path
from statistics import median
from xml.sax.saxutils import escape

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "fixture-uji")
OUT.mkdir(parents=True, exist_ok=True)
rnd = random.Random(20260925)

# ---------------------------------------------------------------- XLSX writer (gaya Excel 365)
NS_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def col(i):
    s, i = "", i + 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


def serial(d, d1904=False):
    base = date(1904, 1, 1) if d1904 else date(1899, 12, 30)
    return (d - base).days


# style index (cellXfs): 0 umum, 1 tanggal kustom dd/mm/yyyy (164), 2 Rp akuntansi (165),
# 3 tanggal bawaan 14, 4 #,##0 (3), 5 bold judul
STYLES = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="%s"><numFmts count="2"><numFmt numFmtId="164" formatCode="dd/mm/yyyy;@"/><numFmt numFmtId="165" formatCode="_-&quot;Rp&quot;* #,##0_-;\\-&quot;Rp&quot;* #,##0_-;_-&quot;Rp&quot;* &quot;-&quot;_-;_-@_-"/></numFmts>
<fonts count="2"><font><sz val="11"/><name val="Calibri"/><family val="2"/><scheme val="minor"/></font><font><b/><sz val="14"/><name val="Calibri"/><family val="2"/><scheme val="minor"/></font></fonts>
<fills count="2"><fill><patternFill patternType="none"/></fill><fill><patternFill patternType="gray125"/></fill></fills>
<borders count="1"><border><left/><right/><top/><bottom/><diagonal/></border></borders>
<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
<cellXfs count="6"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/><xf numFmtId="164" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/><xf numFmtId="165" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/><xf numFmtId="14" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/><xf numFmtId="3" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/><xf numFmtId="0" fontId="1" fillId="0" borderId="0" xfId="0" applyFont="1"/></cellXfs>
<cellStyles count="1"><cellStyle name="Normal" xfId="0" builtinId="0"/></cellStyles></styleSheet>""" % NS_MAIN


def tulis_xlsx(path, sheets, d1904=False):
    """sheets: list {nama, hidden, baris:[[sel]], gabung:[...]}.
    sel: None | str | ("n", num, style) | ("f", rumus, nilai|None, style) | ("fs", rumus, teks)."""
    shared, idx = [], {}

    def si(t):
        if t not in idx:
            idx[t] = len(shared)
            shared.append(t)
        return idx[t]

    n_ref = 0
    sheet_xmls = []
    for sh in sheets:
        rows = []
        for ri, row in enumerate(sh["baris"], 1):
            cs = []
            for ci, v in enumerate(row):
                if v is None:
                    continue
                ref = "%s%d" % (col(ci), ri)
                if isinstance(v, str):
                    n_ref += 1
                    cs.append('<c r="%s" t="s"><v>%d</v></c>' % (ref, si(v)))
                elif v[0] == "n":
                    cs.append('<c r="%s" s="%d"><v>%s</v></c>' % (ref, v[2], v[1]))
                elif v[0] == "f":
                    val = "" if v[2] is None else "<v>%s</v>" % v[2]
                    cs.append('<c r="%s" s="%d"><f>%s</f>%s</c>' % (ref, v[3], escape(v[1]), val))
                elif v[0] == "fs":
                    cs.append('<c r="%s" t="str"><f>%s</f><v>%s</v></c>' % (ref, escape(v[1]), escape(v[2])))
            rows.append('<row r="%d">%s</row>' % (ri, "".join(cs)))
        ncol = max(len(r) for r in sh["baris"])
        dim = "A1:%s%d" % (col(ncol - 1), len(sh["baris"]))
        merge = ""
        if sh.get("gabung"):
            merge = '<mergeCells count="%d">%s</mergeCells>' % (
                len(sh["gabung"]), "".join('<mergeCell ref="%s"/>' % g for g in sh["gabung"]))
        sheet_xmls.append(
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<worksheet xmlns="%s" xmlns:r="%s">'
            '<dimension ref="%s"/><sheetViews><sheetView workbookViewId="0"/></sheetViews>'
            '<sheetFormatPr defaultRowHeight="15"/><sheetData>%s</sheetData>%s'
            '<pageMargins left="0.7" right="0.7" top="0.75" bottom="0.75" header="0.3" footer="0.3"/></worksheet>'
            % (NS_MAIN, NS_R, dim, "".join(rows), merge))
    sst = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<sst xmlns="%s" count="%d" uniqueCount="%d">%s</sst>' % (
        NS_MAIN, n_ref, len(shared),
        "".join('<si><t xml:space="preserve">%s</t></si>' % escape(t) for t in shared))
    wb_sheets = "".join('<sheet name="%s" sheetId="%d"%s r:id="rId%d"/>' % (
        escape(s["nama"]), i + 1, ' state="hidden"' if s.get("hidden") else "", i + 1)
        for i, s in enumerate(sheets))
    wbpr = '<workbookPr date1904="1" defaultThemeVersion="166925"/>' if d1904 else '<workbookPr defaultThemeVersion="166925"/>'
    workbook = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<workbook xmlns="%s" xmlns:r="%s">%s'
                '<bookViews><workbookView xWindow="0" yWindow="0" windowWidth="28800" windowHeight="12300" activeTab="1"/></bookViews>'
                '<sheets>%s</sheets><calcPr calcId="191029"/></workbook>' % (NS_MAIN, NS_R, wbpr, wb_sheets))
    rels = "".join('<Relationship Id="rId%d" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet%d.xml"/>' % (i + 1, i + 1) for i in range(len(sheets)))
    n = len(sheets)
    rels += '<Relationship Id="rId%d" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>' % (n + 1)
    rels += '<Relationship Id="rId%d" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/>' % (n + 2)
    wb_rels = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">%s</Relationships>' % rels
    ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
          + "".join('<Override PartName="/xl/worksheets/sheet%d.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' % (i + 1) for i in range(n))
          + '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>'
          '<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/></Types>')
    root_rels = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
                 '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>')
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("_rels/.rels", root_rels)
        z.writestr("xl/workbook.xml", workbook)
        z.writestr("xl/_rels/workbook.xml.rels", wb_rels)
        z.writestr("xl/styles.xml", STYLES)
        z.writestr("xl/sharedStrings.xml", sst)
        for i, x in enumerate(sheet_xmls):
            z.writestr("xl/worksheets/sheet%d.xml" % (i + 1), x)


# ---------------------------------------------------------------- Skenario 01: toko bangunan
BARANG = {
    "Semen": [("Semen Tiga Roda 50kg", 68000), ("Semen Gresik 40kg", 58000)],
    "Cat": [("Cat Avian 5kg Putih", 185000), ("Cat Dulux 2,5L", 142000), ("Plamir 1kg", 32000)],
    "Besi": [("Besi Beton 10mm", 92000), ("Besi Beton 8mm", 61000), ("Hollow 4x4", 48000)],
    "Pipa & Sanitasi": [("Pipa PVC 3/4\" Rucika", 38500), ("Kran Air Onda", 45000), ("Closet Duduk Ina", 1250000)],
    "Keramik": [("Keramik 40x40 Roman (dus)", 72000), ("Granit 60x60 (dus)", 215000)],
    "Alat & Perkakas": [("Paku 5cm (kg)", 21000), ("Gergaji Kayu", 65000), ("Meteran 5m", 35000)],
}
VARIAN = {"Semen": ["SEMEN", "semen "], "Cat": ["CAT", " cat"], "Besi": ["besi"],
          "Keramik": ["KERAMIK"], "Pipa & Sanitasi": ["pipa & sanitasi"], "Alat & Perkakas": ["alat & perkakas"]}
BOBOT = {"Semen": 30, "Cat": 15, "Besi": 18, "Pipa & Sanitasi": 12, "Keramik": 12, "Alat & Perkakas": 13}
PELANGGAN = ["Umum", "CV Karya Mandiri", "Pak Darto (mandor)", "PT Griya Asri", "Bu Sri", "Umum"]
BULAN_BARIS = {1: 48, 2: 44, 3: 55, 4: 52, 5: 58, 6: 61, 7: 57, 8: 63, 9: 60}  # total 498

transaksi = []  # kebenaran: dicatat SEBELUM ditulis ke XLSX
no = 0
for bln, jml in BULAN_BARIS.items():
    last = (date(2026, bln + 1, 1) - timedelta(days=1)).day if bln < 12 else 31
    days = sorted(rnd.randint(1, last) for _ in range(jml))
    for d in days:
        no += 1
        kat = rnd.choices(list(BOBOT), weights=list(BOBOT.values()))[0]
        nama, harga = rnd.choice(BARANG[kat])
        qty = rnd.choice([1, 1, 2, 3, 5, 10, 20, 50]) if kat == "Semen" else rnd.choice([1, 1, 2, 3, 4, 6, 10])
        if harga > 1000000:
            qty = 1
        tulis_kat = kat
        if rnd.random() < 0.12:
            tulis_kat = rnd.choice(VARIAN[kat])
        transaksi.append(dict(tgl=date(2026, bln, d), nota="NT-%04d" % no, kat=kat, tulis_kat=tulis_kat,
                              barang=nama, qty=qty, harga=harga, total=qty * harga,
                              pel=rnd.choice(PELANGGAN), jenis="normal"))

# anomali realistis (dicatat di kebenaran)
# a) 3 baris Total berupa rumus TANPA nilai tersimpan (file pernah disimpan aplikasi lain) -> tak terhitung
for t in rnd.sample([t for t in transaksi if t["tgl"].month in (5, 8)], 3):
    t["jenis"] = "rumus_kosong"
# b) 4 baris Harga & Total diketik sebagai TEKS "Rp 1.250.000" (bukan angka)
for t in rnd.sample([t for t in transaksi if t["jenis"] == "normal"], 4):
    t["jenis"] = "teks_rp"
# c) 1 retur: qty negatif, total negatif sebagai teks akuntansi "(185.000)"
retur = dict(tgl=date(2026, 7, 21), nota="NT-R01", kat="Cat", tulis_kat="Cat", barang="Cat Avian 5kg Putih",
             qty=-1, harga=185000, total=-185000, pel="Bu Sri", jenis="teks_kurung")
transaksi.append(retur)
transaksi.sort(key=lambda t: (t["tgl"], t["nota"]))

JUDUL = ["Tanggal", "No Nota", "Kategori", "Barang", "Qty", "Harga Satuan", "Total", "Pelanggan"]


def sel_transaksi(t, ri, d1904):
    tg = ("n", serial(t["tgl"], d1904), 1 if t["tgl"].day % 7 else 3)  # campur format 164 & bawaan 14
    if t["jenis"] == "teks_rp":
        harga = "Rp %s" % "{:,}".format(t["harga"]).replace(",", ".")
        total = "Rp %s" % "{:,}".format(t["total"]).replace(",", ".")
    elif t["jenis"] == "teks_kurung":
        harga = ("n", t["harga"], 2)
        total = "(%s)" % "{:,}".format(-t["total"]).replace(",", ".")
    else:
        harga = ("n", t["harga"], 2)
        total = ("f", "E%d*F%d" % (ri, ri), None if t["jenis"] == "rumus_kosong" else t["total"], 2)
    return [tg, t["nota"], t["tulis_kat"], t["barang"], ("n", t["qty"], 0), harga, total, t["pel"]]


def buat_penjualan(path, d1904=False):
    per_q = {1: [], 2: [], 3: []}
    for t in transaksi:
        per_q[(t["tgl"].month - 1) // 3 + 1].append(t)
    sheets = [{"nama": "Master Barang", "hidden": True,
               "baris": [["Kategori", "Barang", "Harga"]] + [[k, b, ("n", h, 2)] for k, v in BARANG.items() for b, h in v]}]
    for q, rows in per_q.items():
        baris = [["TOKO BANGUNAN SUMBER REJEKI - PENJUALAN Q%d 2026" % q], ["Jl. Raya Parung No. 12, Bogor"], JUDUL]
        gabung = ["A1:H1", "A2:H2"]
        for t in rows:
            ri = len(baris) + 1
            baris.append(sel_transaksi(t, ri, d1904))
        last = len(baris)
        cached = sum(t["total"] for t in rows if t["jenis"] in ("normal",))  # Excel SUM mengabaikan teks & kosong
        baris.append(["TOTAL", None, None, None, ("f", "SUM(E4:E%d)" % last, sum(t["qty"] for t in rows if t["jenis"] != "teks_kurung"), 0),
                      None, ("f", "SUM(G4:G%d)" % last, cached, 2), None])
        # sel gabungan vertikal di kolom Pelanggan untuk 3 baris pertama transaksi (gaya buatan tangan)
        baris[3][7], baris[4][7], baris[5][7] = "PT Griya Asri", None, None
        gabung.append("H4:H6")
        sheets.append({"nama": "Q%d" % q, "baris": baris, "gabung": gabung})
    tulis_xlsx(path, sheets, d1904)


buat_penjualan(OUT / "Penjualan 2026.xlsx")
buat_penjualan(OUT / "Penjualan 2026 (1904).xlsx", d1904=True)

# kebenaran skenario 01: nilai "Total" yang terbaca (rumus_kosong = tidak ada nilai)
def total_terbaca(t):
    return None if t["jenis"] == "rumus_kosong" else t["total"]


def ringkas_set(rows):
    vals = [total_terbaca(t) for t in rows if total_terbaca(t) is not None]
    kat, bln = {}, {}
    for t in rows:
        v = total_terbaca(t)
        if v is None:
            continue
        kat[t["kat"]] = kat.get(t["kat"], 0) + v
        k = "%04d-%02d" % (t["tgl"].year, t["tgl"].month)
        bln[k] = bln.get(k, 0) + v
    return {"baris": len(rows), "nilai_terisi": len(vals), "jumlah": sum(vals),
            "rata": str(Decimal(sum(vals)) / len(vals)), "median": median(vals),
            "min": min(vals), "max": max(vals), "per_kategori": dict(sorted(kat.items(), key=lambda x: -x[1])),
            "per_bulan": dict(sorted(bln.items())),
            "qty_per_kategori": {k: sum(t["qty"] for t in rows if t["kat"] == k) for k in BOBOT},
            "baris_per_kategori": {k: sum(1 for t in rows if t["kat"] == k) for k in BOBOT},
            "rumus_kosong": [t["nota"] for t in rows if t["jenis"] == "rumus_kosong"],
            "teks_rp": [t["nota"] for t in rows if t["jenis"] == "teks_rp"]}


kunci = {"01": {"semua": ringkas_set(transaksi)}}
for q in (1, 2, 3):
    kunci["01"]["Q%d" % q] = ringkas_set([t for t in transaksi if (t["tgl"].month - 1) // 3 + 1 == q])

# ---------------------------------------------------------------- Skenario 02: lembur (cp1252 ;)
DIVISI = {"Produksi": 14, "Gudang": 8, "Admin": 5, "Sales": 7, "QC": 4}
NAMA = ["Agus Salim", "Budi Hartono", "Citra Dewi", "Dédé Kurnia", "Eko Prasetyo", "Fajar Nugroho", "Gita Anggraini",
        "Hendra Wijaya", "Indah Permata", "Joko Susilo", "Kartika Sari", "Lukman Hakim", "Maria Ulfa", "Nanda Putra",
        "Oktaviani", "Putu Ayu", "Rizky Ramadhan", "Siti Nurhaliza", "Taufik Hidayat", "Udin Sedunia", "Vina Marlina",
        "Wahyu Setiawan", "Yogi Pratama", "Zainal Arifin", "André Gunawan", "Bella Saputri", "Candra Kirana",
        "Dimas Anggara", "Erna Wati", "Ferry Irawan", "Gilang Ramadhan", "Hana Pertiwi", "Irfan Bachdim",
        "Jessica Tan", "Kevin Sanjaya", "Lina Marlina", "Mulyadi", "Nurul Fitri"]
karyawan = []
i = 0
for dv, n in DIVISI.items():
    for _ in range(n):
        nik = "32010%011d" % rnd.randint(10 ** 9, 10 ** 10)
        karyawan.append(dict(nama=NAMA[i], divisi=dv, nik=nik))
        i += 1
lembur_rows = []
for k in karyawan:
    for d in range(1, 31):
        tg = date(2026, 9, d)
        if tg.weekday() == 6:
            continue
        if rnd.random() < 0.35:
            jam = rnd.choice([Decimal("0.5"), Decimal("1"), Decimal("1.5"), Decimal("2"), Decimal("3"), Decimal("4")])
            if k["divisi"] == "Produksi":
                jam += Decimal("0.5")
            lembur_rows.append(dict(k, tgl=tg, jam=jam))
        elif rnd.random() < 0.08:
            lembur_rows.append(dict(k, tgl=tg, jam=Decimal("0")))  # tercatat hadir, lembur 0
# 1 duplikat input, 3 baris Jam Lembur kosong (lupa isi)
lembur_rows.append(dict(lembur_rows[10]))
for r in rnd.sample(lembur_rows, 3):
    r["jam"] = None
UPAH_JAM = 17340  # 1/173 x UMK contoh 3.000.000 (dibulatkan) -- hanya ilustrasi kolom uang
with open(OUT / "lembur-sep-2026.csv", "w", encoding="cp1252", newline="") as f:
    f.write("NIK;Nama Karyawan;Divisi;Tanggal;Jam Lembur;Uang Lembur;Keterangan\r\n")
    for r in lembur_rows:
        jam = "" if r["jam"] is None else ("{:f}".format(r["jam"].normalize()).replace(".", ","))
        uang = "" if r["jam"] is None else "Rp {:,}".format(int(r["jam"] * UPAH_JAM)).replace(",", ".")
        ket = "Lembur shift malam" if (r["jam"] or 0) >= 3 else ("Hadir" if r["jam"] == 0 else "")
        f.write("%s;%s;%s;%s;%s;%s;%s\r\n" % (r["nik"], r["nama"], r["divisi"], r["tgl"].strftime("%d/%m/%Y"), jam, uang, ket))

rows_valid = [r for r in lembur_rows if r["jam"] is not None]
k02 = {"baris": len(lembur_rows), "kosong": sum(1 for r in lembur_rows if r["jam"] is None),
       "rata_per_baris_divisi": {}, "rata_per_karyawan_divisi": {}, "total_per_divisi": {}, "top5_total_karyawan": []}
for dv in DIVISI:
    v = [r["jam"] for r in rows_valid if r["divisi"] == dv]
    k02["total_per_divisi"][dv] = str(sum(v))
    k02["rata_per_baris_divisi"][dv] = str(sum(v) / len(v))
    k02["baris_divisi"] = k02.get("baris_divisi", {})
    k02["baris_divisi"][dv] = len(v)
    orang = [k for k in karyawan if k["divisi"] == dv]
    k02["rata_per_karyawan_divisi"][dv] = str(sum(v) / len(orang))
tot = {}
for r in rows_valid:
    tot[r["nama"]] = tot.get(r["nama"], Decimal(0)) + r["jam"]
k02["top5_total_karyawan"] = [(n, str(v)) for n, v in sorted(tot.items(), key=lambda x: -x[1])[:6]]
k02["total_semua"] = str(sum(r["jam"] for r in rows_valid))
k02["rata_semua_baris"] = str(sum(r["jam"] for r in rows_valid) / len(rows_valid))
k02["rata_tanpa_nol"] = str(sum(r["jam"] for r in rows_valid if r["jam"] > 0) / sum(1 for r in rows_valid if r["jam"] > 0))
kunci["02"] = k02

# ---------------------------------------------------------------- Skenario 03: iuran komite
siswa = []
for kls in ["4A", "4B", "5A", "5B"]:
    for j in range(8):
        siswa.append(dict(nis="2023%03d" % (len(siswa) + 1), nama="Siswa %s-%02d" % (kls, j + 1), kelas=kls))
iuran = []
for s in siswa:
    for bln in ["Juli", "Agustus", "September"]:
        r = rnd.random()
        if r < 0.12:
            continue  # belum bayar
        nominal = 75000 if s["kelas"].startswith("5") else 50000
        tulis_kelas = rnd.choice([s["kelas"], s["kelas"], s["kelas"], s["kelas"][0] + " " + s["kelas"][1], s["kelas"].lower()])
        gaya = rnd.choice(["Rp {:,}", "{}", "{:,},-", "Rp. {:,}"])
        teks = gaya.format(nominal).replace(",", ".").replace(".-", ",-") if "{:,}" in gaya else str(nominal)
        iuran.append(dict(nis=s["nis"], nama=s["nama"], kelas=s["kelas"], tulis_kelas=tulis_kelas, bulan=bln,
                          nominal=nominal, teks=teks, ket=""))
# sel kosong: 2 nominal kosong (ditandai "belum setor"), 1 kelas kosong
iuran[5]["teks"] = ""; iuran[5]["nominal"] = None; iuran[5]["ket"] = "belum setor ke bendahara"
iuran[17]["teks"] = ""; iuran[17]["nominal"] = None
iuran[23]["tulis_kelas"] = ""
# duplikat: 3 baris persis sama (kepencet paste), 1 duplikat NIS+bulan dengan nomor berbeda
dups = [dict(iuran[2]), dict(iuran[40]), dict(iuran[41])]
iuran_out = iuran[:] + dups
iuran_out.insert(30, dict(iuran[30], ket="dobel input?"))
with open(OUT / "iuran-komite.csv", "w", encoding="utf-8-sig", newline="") as f:
    f.write("SD NEGERI 5 CIBINONG;;;;;;\r\nREKAP IURAN KOMITE SEMESTER GANJIL 2026/2027;;;;;;\r\n;;;;;;\r\n")
    f.write("NIS;Nama Siswa;Kelas;Bulan;Tanggal Bayar;Nominal;Keterangan\r\n")
    for r in iuran_out:
        tb = {"Juli": "2026-07-1%d", "Agustus": "2026-08-1%d", "September": "2026-09-1%d"}[r["bulan"]] % (int(r["nis"][-1]))
        f.write("%s;%s;%s;%s;%s;%s;%s\r\n" % (r["nis"], r["nama"], r["tulis_kelas"], r["bulan"], tb, r["teks"], r["ket"]))
    f.write(";;;;TOTAL;;\r\n")
uniq, seen = [], set()
for r in iuran_out:
    key = (r["nis"], r["nama"], r["tulis_kelas"], r["bulan"], r["teks"], r["ket"])
    if key in seen:
        continue
    seen.add(key)
    uniq.append(r)
def agg03(rows):
    vals = [r["nominal"] for r in rows if r["nominal"] is not None]
    per_kelas, per_bulan = {}, {}
    for r in rows:
        if r["nominal"] is None:
            continue
        per_kelas[r["kelas"]] = per_kelas.get(r["kelas"], 0) + r["nominal"]
        per_bulan[r["bulan"]] = per_bulan.get(r["bulan"], 0) + r["nominal"]
    return {"baris": len(rows), "terisi": len(vals), "jumlah": sum(vals), "per_kelas_asli": per_kelas, "per_bulan": per_bulan}
kunci["03"] = {"mentah": agg03(iuran_out), "tanpa_duplikat_persis": agg03(uniq),
               "tanpa_duplikat_nis_bulan": agg03(list({(r["nis"], r["bulan"]): r for r in iuran_out}.values())),
               "belum_bayar_siswa_bulan": 32 * 3 - len({(r["nis"], r["bulan"]) for r in iuran_out if r["nominal"] is not None})}

# ---------------------------------------------------------------- file rusak
(OUT / "kosong.csv").write_bytes(b"")
(OUT / "korup.xlsx").write_bytes(b"PK\x03\x04" + b"\x00garbage" * 50)
(OUT / "bukan-excel.xlsx").write_text("ini sebenarnya teks biasa\n", encoding="utf-8")
(OUT / "semua-teks.csv").write_text("Nama,Kota,Catatan\nAni,Bogor,ok\nBudi,Depok,-\nCici,Bekasi,baik\n", encoding="utf-8")
(OUT / "kutip-rusak.csv").write_text('Nama,Nominal\n"Ani,5000\nBudi,6000\n', encoding="utf-8")
with zipfile.ZipFile(OUT / "tanpa-sheet.xlsx", "w") as z:
    z.writestr("[Content_Types].xml", "<Types/>")
    z.writestr("xl/workbook.xml", '<workbook xmlns="%s"><sheets/></workbook>' % NS_MAIN)

(OUT / "kunci-jawaban.json").write_text(json.dumps(kunci, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
print("Fixture dibuat di", OUT.resolve())
