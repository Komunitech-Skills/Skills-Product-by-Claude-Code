#!/usr/bin/env python3
"""Fixture uji ulang v1.0.11 (penguji independen ke-12, cek singkat). Python standar, deterministik.
Fokus regresi B35 (blok EKOR membuang baris data berlabel "Total "/dst tanpa syarat seperti _label_nama_data)
di berbagai posisi (awal, akhir, setelah baris kosong, tengah) DAN baris Total/Grand Total SUNGGUHAN
(termasuk label berdiri sendiri tapi kolom lain terisi penuh) yang tetap wajib dikeluarkan + pengaman silang COCOK.
kunci-uji12-v1011.json dihitung dari data sumber di script ini, TANPA membaca kode skill.
Pakai: python3 buat_fixture_uji12_v1011.py [folder]"""
import json, zipfile, csv, sys
from pathlib import Path
from xml.sax.saxutils import escape

O = Path(sys.argv[1] if len(sys.argv) > 1 else 'fixture-uji12-v1011'); O.mkdir(parents=True, exist_ok=True)
K = {}


def col(i):
    s = ""; i += 1
    while i:
        i, r = divmod(i - 1, 26); s = chr(65 + r) + s
    return s


def xlsx(nama, rows):
    xs = []
    for r, row in enumerate(rows, 1):
        cs = []
        for c, v in enumerate(row):
            ref = f"{col(c)}{r}"
            if v is None or v == "":
                continue
            if isinstance(v, str):
                cs.append(f'<c r="{ref}" t="inlineStr"><is><t>{escape(v)}</t></is></c>')
            else:
                cs.append(f'<c r="{ref}"><v>{v}</v></c>')
        xs.append(f'<row r="{r}">{"".join(cs)}</row>')
    sh = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
          f'<sheetData>{"".join(xs)}</sheetData></worksheet>')
    with zipfile.ZipFile(O / nama, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/></Types>')
        z.writestr("_rels/.rels", '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>')
        z.writestr("xl/workbook.xml", '<?xml version="1.0" encoding="UTF-8"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Data" sheetId="1" r:id="rId1"/></sheets></workbook>')
        z.writestr("xl/_rels/workbook.xml.rels", '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/></Relationships>')
        z.writestr("xl/worksheets/sheet1.xml", sh)


def csvw(nama, rows, sep=","):
    with open(O / nama, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=sep)
        for r in rows:
            w.writerow(["" if v is None else v for v in r])


# ---------------------------------------------------------------------------
# Z1 — "Total Care" di BARIS PERTAMA tabel data (bukan tengah/ekor), terisi penuh, tanpa baris total.
rows = [["Produk", "Stok", "Harga"],
        ["Total Care Shampoo", 10, 25000],
        ["Sabun Cair", 20, 8000],
        ["Sikat Gigi", 15, 5000],
        ["Pasta Gigi", 12, 7000]]
xlsx("Z1-total-care-baris-pertama.xlsx", rows)
K["Z1"] = dict(baris=4, stok=10 + 20 + 15 + 12, harap="4 baris, stok 57; baris 'Total Care Shampoo' TIDAK dikeluarkan (bukan ringkasan)")

# ---------------------------------------------------------------------------
# Z2 — "Jumlah Besar Deterjen" di BARIS TERAKHIR, terisi penuh, tanpa baris total lain.
rows = [["Produk", "Stok", "Harga"],
        ["Deterjen", 30, 18000],
        ["Sabun Mandi", 25, 4500],
        ["Jumlah Besar Deterjen", 40, 22000]]
csvw("Z2-jumlah-besar-ekor.csv", rows)
K["Z2"] = dict(baris=3, stok=30 + 25 + 40, harap="3 baris, stok 95; baris 'Jumlah Besar Deterjen' di ekor TIDAK dikeluarkan")

# ---------------------------------------------------------------------------
# Z3 — "Grand Prix Helm" SETELAH baris kosong (gap di tengah tabel), terisi penuh.
rows = [["Produk", "Stok", "Harga"],
        ["Helm A", 20, 150000],
        ["Helm B", 15, 175000],
        ["", "", ""],
        ["Grand Prix Helm", 18, 210000],
        ["Helm C", 22, 165000]]
xlsx("Z3-grand-prix-setelah-kosong.xlsx", rows)
K["Z3"] = dict(baris=4, stok=20 + 15 + 18 + 22, harap="4 baris data (baris kosong dilewati), stok 75; 'Grand Prix Helm' TIDAK dikeluarkan")

# ---------------------------------------------------------------------------
# Z4 — "Subtotal Kit Sparepart" di TENGAH tabel (bukan awal/akhir/setelah kosong), terisi penuh.
rows = [["Produk", "Stok", "Harga"],
        ["Kit A", 10, 90000],
        ["Subtotal Kit Sparepart", 25, 110000],
        ["Kit B", 30, 95000]]
csvw("Z4-subtotal-kit-tengah.csv", rows)
K["Z4"] = dict(baris=3, stok=10 + 25 + 30, harap="3 baris, stok 65; 'Subtotal Kit Sparepart' di tengah TIDAK dikeluarkan")

# ---------------------------------------------------------------------------
# Z5 — Grand Total SUNGGUHAN di akhir (label jelas "Grand Total"), harus DIKELUARKAN + pengaman silang COCOK.
dat = [100, 150, 200]
rows = [["Produk", "Stok", "Nilai"],
        ["Barang A", dat[0], dat[0] * 1000],
        ["Barang B", dat[1], dat[1] * 1000],
        ["Barang C", dat[2], dat[2] * 1000],
        ["Grand Total", sum(dat), sum(dat) * 1000]]
xlsx("Z5-grand-total-sungguhan.xlsx", rows)
K["Z5"] = dict(baris=3, stok=sum(dat), nilai=sum(dat) * 1000,
               harap="Baris 'Grand Total' DIKELUARKAN; hitungan = 450 stok / 450000 nilai; pengaman silang harus COCOK (tanpa peringatan)")

# ---------------------------------------------------------------------------
# Z6 — Total SUNGGUHAN, label "Total" BERDIRI SENDIRI (bukan "Total <produk>") tapi SEMUA kolom lain terisi
# penuh seperti baris data (tidak ada sel kosong) — kasus yang mirip pola data penuh B34/B35 tapi memang ringkasan.
dat = [50, 70, 30]
rows = [["Produk", "Stok", "Harga"],
        ["Barang X", dat[0], 12000],
        ["Barang Y", dat[1], 9000],
        ["Barang Z", dat[2], 15000],
        ["Total", sum(dat), 12000 + 9000 + 15000]]
csvw("Z6-total-label-sendiri-penuh.csv", rows)
K["Z6"] = dict(baris=3, stok=sum(dat), harga=12000 + 9000 + 15000,
               harap="Baris 'Total' (label sendiri, semua kolom terisi & = jumlah blok di atas) DIKELUARKAN; hitungan = 150 stok; pengaman silang COCOK")

# ---------------------------------------------------------------------------
# Z7 — Kontrol tabel rapi #1 (kas kecil harian), tanpa jebakan.
dat = [(46280, "Beli ATK", 75000), (46281, "Transport", 50000), (46282, "Makan Tim", 120000), (46283, "Fotokopi", 25000)]
rows = [["Tanggal", "Keterangan", "Nominal"]] + [list(x) for x in dat]
xlsx("Z7-kontrol-kas-harian.xlsx", rows)
K["Z7"] = dict(baris=len(dat), total=sum(x[2] for x in dat), harap="4 baris, total 270.000, tanpa peringatan apa pun")

# ---------------------------------------------------------------------------
# Z8 — Kontrol tabel rapi #2 (stok gudang sparepart), tanpa jebakan.
dat = [("Baut M6", 500, 500), ("Mur M6", 480, 480), ("Ring Plat", 620, 620), ("Sekrup Kayu", 310, 310)]
rows = [["Nama Barang", "Stok Awal", "Stok Akhir"]] + [list(x) for x in dat]
csvw("Z8-kontrol-gudang-sparepart.csv", rows, sep=";")
K["Z8"] = dict(baris=len(dat), stok_akhir=sum(x[2] for x in dat), harap="4 baris, stok akhir total 1.910, tanpa peringatan apa pun")

with open(O / "kunci-uji12-v1011.json", "w", encoding="utf-8") as f:
    json.dump(K, f, ensure_ascii=False, indent=2)

print(f"OK {len(K)} file baru -> {O}")
