#!/usr/bin/env python3
"""Fixture uji ulang v1.0.8 (penguji independen ke-9). Python standar, deterministik.
Fokus: tabel TANPA judul kolom (baris 1 = data: angka, tanggal, teks), tabel yang judul kolomnya memang angka
(tahun 2024/2025, nomor bulan 1..12), subtotal terisi penuh di banyak kolom, data rapi dengan KEBETULAN x+y=z di
2 kolom (tidak boleh dibuang diam-diam), pivot bentuk ringkas & tabular, + 3 tabel rapi kontrol.
kunci-v108.json dihitung dari data sumber di script ini, TANPA membaca kode skill.
Pakai: python3 buat_fixture_uji_v108.py [folder]"""
import json, sys, zipfile
from pathlib import Path
from xml.sax.saxutils import escape
from datetime import date

O = Path(sys.argv[1] if len(sys.argv) > 1 else "fixture-v108"); O.mkdir(parents=True, exist_ok=True)
K = {}
def col(i):
    s = ""; i += 1
    while i: i, r = divmod(i - 1, 26); s = chr(65 + r) + s
    return s


def xlsx(nama, rows, sheet="Sheet1"):
    xs = []
    for r, row in enumerate(rows, 1):
        cs = []
        for c, v in enumerate(row):
            ref = f"{col(c)}{r}"
            if v is None or v == "": continue
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
        z.writestr("xl/workbook.xml", f'<?xml version="1.0" encoding="UTF-8"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="{sheet}" sheetId="1" r:id="rId1"/></sheets></workbook>')
        z.writestr("xl/_rels/workbook.xml.rels", '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/></Relationships>')
        z.writestr("xl/worksheets/sheet1.xml", sh)


def tulis(nama, baris, delim=",", enc="utf-8"):
    def sel(x):
        x = "" if x is None else str(x)
        return '"' + x.replace('"', '""') + '"' if (delim in x or '"' in x) else x
    (O / nama).write_text("\r\n".join(delim.join(sel(c) for c in b) for b in baris) + "\r\n", encoding=enc)


def serial(d):  # tanggal -> serial Excel sistem 1900
    return (d - date(1899, 12, 30)).days


# W1 tanpa header, baris 1 = teks + angka (nama pelanggan pertama)
w1 = [("Budi Santoso", "Jakarta", "Kaos Polos", 3, 75000), ("Sari Dewi", "Bandung", "Kemeja Batik", 1, 185000),
      ("Andi Wijaya", "Surabaya", "Kaos Polos", 5, 75000), ("Rina Marlina", "Jakarta", "Celana Chino", 2, 160000),
      ("Doni Pratama", "Medan", "Kemeja Batik", 2, 185000), ("Maya Sari", "Bandung", "Kaos Polos", 4, 75000),
      ("Tono Hartono", "Jakarta", "Jaket Denim", 1, 275000)]
tulis("W1-tanpa-header-teks-dulu.csv", [[a, b, c, q, h, q * h] for a, b, c, q, h in w1])
K["W1"] = {"baris": 7, "qty": sum(r[3] for r in w1), "total": sum(r[3] * r[4] for r in w1),
           "harapan": "7 baris (Budi ikut), total dihitung dari 7 baris; peringatan tanpa judul kolom"}

# W2 tanpa header, baris 1 = nomor urut + tanggal ID + teks + angka ID, pemisah ;
w2 = [(1, "01/09/2026", "Semen Gresik", 10, 55000), (2, "02/09/2026", "Pasir Cor", 3, 350000),
      (3, "02/09/2026", "Besi 10mm", 20, 78000), (4, "05/09/2026", "Semen Gresik", 15, 55000),
      (5, "07/09/2026", "Batu Split", 2, 420000), (6, "09/09/2026", "Besi 12mm", 12, 112000)]
tulis("W2-tanpa-header-no-urut.csv", [[n, t, b, q, f"{h:,}".replace(",", "."), f"{q*h:,}".replace(",", ".")] for n, t, b, q, h in w2], delim=";")
K["W2"] = {"baris": 6, "qty": sum(r[3] for r in w2), "total": sum(r[3] * r[4] for r in w2)}

# W3 tanpa header XLSX, baris 1 = tanggal serial + teks + angka
w3 = [(date(2026, 9, 1), "Listrik", 850000), (date(2026, 9, 3), "Internet", 450000), (date(2026, 9, 5), "ATK", 125000),
      (date(2026, 9, 10), "Transport", 300000), (date(2026, 9, 15), "ATK", 90000), (date(2026, 9, 20), "Konsumsi", 275000)]
xlsx("W3-tanpa-header-tanggal.xlsx", [[serial(d), k, n] for d, k, n in w3])
K["W3"] = {"baris": 6, "total": sum(r[2] for r in w3), "ATK": 215000,
           "catatan": "xlsx tanpa style: tanggal tampil sebagai angka serial (tanpa format tanggal)"}

# W4 judul kolom = tahun (teks CSV)
w4 = [("Kopi Susu", 12500000, 15800000), ("Es Teh", 6200000, 7100000), ("Roti Bakar", 8400000, 7900000),
      ("Pisang Goreng", 3100000, 4050000), ("Mie Rebus", 5600000, 6300000)]
tulis("W4-header-tahun.csv", [["Produk", "2024", "2025"]] + [list(r) for r in w4])
K["W4"] = {"baris": 5, "2024": sum(r[1] for r in w4), "2025": sum(r[2] for r in w4),
           "harapan": "2024/2025 tetap judul kolom (5 baris), bukan tabel tanpa judul"}

# W5 judul kolom = nomor bulan 1..12 (angka numerik di XLSX), isi = jumlah kunjungan (bilangan kecil)
w5 = [("Klinik A", [30, 28, 35, 31, 29, 33, 36, 34, 30, 32, 27, 38]), ("Klinik B", [12, 15, 11, 14, 13, 16, 12, 15, 14, 13, 12, 17]),
      ("Klinik C", [8, 9, 10, 7, 11, 9, 8, 10, 12, 9, 8, 11])]
xlsx("W5-header-nomor-bulan.xlsx", [["Unit"] + list(range(1, 13))] + [[n] + v for n, v in w5])
K["W5"] = {"baris": 3, "per_bulan": {str(i + 1): sum(v[i] for _, v in w5) for i in range(12)},
           "total": sum(sum(v) for _, v in w5)}

# W5b judul kolom tahun numerik di XLSX, isi = bilangan kecil juga (jumlah karyawan)
w5b = [("Produksi", 42, 45, 48), ("Gudang", 12, 13, 13), ("Admin", 8, 8, 9), ("Sales", 15, 18, 21)]
xlsx("W5b-header-tahun-numerik.xlsx", [["Divisi", 2023, 2024, 2025]] + [list(r) for r in w5b])
K["W5b"] = {"baris": 4, "2023": sum(r[1] for r in w5b), "2024": sum(r[2] for r in w5b), "2025": sum(r[3] for r in w5b)}

# W6 subtotal terisi penuh di BANYAK kolom (tanggal, wilayah, qty, omzet, hpp, laba) + grand total terisi penuh
w6 = {"Barat": [("Kemeja", 10, 1500000, 900000), ("Celana", 6, 1080000, 660000), ("Jaket", 3, 870000, 540000)],
      "Timur": [("Kemeja", 8, 1200000, 720000), ("Celana", 4, 720000, 440000)],
      "Tengah": [("Kemeja", 5, 750000, 450000), ("Celana", 7, 1260000, 770000), ("Jaket", 2, 580000, 360000)]}
rows = [["Periode", "Wilayah", "Keterangan", "Qty", "Omzet", "HPP", "Laba"]]
g = [0, 0, 0]; n = 0
for w, it in w6.items():
    s = [0, 0, 0]
    for p, q, o, h in it:
        rows.append(["Sep 2026", w, p, q, o, h, o - h]); s = [s[0] + q, s[1] + o, s[2] + h]; n += 1
    rows.append(["Sep 2026", w, f"Total {w}", s[0], s[1], s[2], s[1] - s[2]]); g = [g[0] + s[0], g[1] + s[1], g[2] + s[2]]
rows.append(["Sep 2026", "Semua", "Total Semua Wilayah", g[0], g[1], g[2], g[1] - g[2]])
tulis("W6-subtotal-penuh-multikolom.csv", rows)
K["W6"] = {"baris": n, "qty": g[0], "omzet": g[1], "hpp": g[2], "laba": g[1] - g[2],
           "per_wilayah_omzet": {w: sum(x[2] for x in it) for w, it in w6.items()}}

# W7 data rapi, KEBETULAN baris 3 = baris 1 + baris 2 di Qty DAN Total (bukan ringkasan)
w7 = [("2026-09-01", "INV-001", "Toko Makmur", 4, 200000), ("2026-09-01", "INV-002", "CV Sinar", 6, 300000),
      ("2026-09-02", "INV-003", "UD Jaya", 10, 500000), ("2026-09-03", "INV-004", "Toko Makmur", 3, 150000),
      ("2026-09-04", "INV-005", "PT Anugerah", 12, 540000), ("2026-09-05", "INV-006", "CV Sinar", 7, 315000),
      ("2026-09-06", "INV-007", "UD Jaya", 5, 225000)]
tulis("W7-kebetulan-x-plus-y.csv", [["Tanggal", "No Faktur", "Pelanggan", "Qty", "Total"]] + [list(r) for r in w7])
K["W7"] = {"baris": 7, "qty": sum(r[3] for r in w7), "total": sum(r[4] for r in w7),
           "harapan": "a; paling buruk b (TEGAS, tetap dihitung). Dibuang diam-diam = c"}

# W7b data rapi, KEBETULAN baris 4 = jumlah baris 1..3 (Qty & Nominal), di tengah tabel
w7b = [("2026-09-02", "Andi", "Grosir", 2, 100000), ("2026-09-03", "Budi", "Eceran", 3, 150000),
       ("2026-09-04", "Cici", "Eceran", 5, 250000), ("2026-09-05", "Dedi", "Grosir", 10, 500000),
       ("2026-09-06", "Euis", "Eceran", 1, 60000), ("2026-09-07", "Fajar", "Grosir", 4, 210000),
       ("2026-09-08", "Gita", "Eceran", 2, 95000)]
xlsx("W7b-kebetulan-jumlah-blok.xlsx", [["Tanggal", "Sales", "Jenis", "Qty", "Nominal"]] + [list(r) for r in w7b])
K["W7b"] = {"baris": 7, "qty": sum(r[3] for r in w7b), "nominal": sum(r[4] for r in w7b)}

# W8 pivot bentuk ringkas ID (Label Baris) dua kolom nilai, satu kelompok hanya 1 anak
w8 = {"Bekasi": [("Kopi", 12, 1800000), ("Teh", 8, 640000)], "Bogor": [("Kopi", 9, 1350000)],
      "Depok": [("Kopi", 7, 1050000), ("Teh", 5, 400000), ("Roti", 10, 900000)]}
rows = [["Label Baris", "Jumlah dari Qty", "Jumlah dari Omzet"]]
for c, it in w8.items():
    rows.append([c, sum(x[1] for x in it), sum(x[2] for x in it)])
    rows += [[p, q, o] for p, q, o in it]
rows.append(["Total Keseluruhan", sum(x[1] for it in w8.values() for x in it), sum(x[2] for it in w8.values() for x in it)])
xlsx("W8-pivot-ringkas-id.xlsx", rows)
K["W8"] = {"daun": 6, "qty": sum(x[1] for it in w8.values() for x in it), "omzet": sum(x[2] for it in w8.values() for x in it)}

# W9 pivot tabular: Cabang di kolom 1 (diulang), "X Total" per cabang (kolom 2 kosong), Grand Total
rows = [["Cabang", "Produk", "Sum of Omzet"]]
for c, it in w8.items():
    rows += [[c, p, o] for p, q, o in it]
    rows.append([f"{c} Total", "", sum(x[2] for x in it)])
rows.append(["Grand Total", "", K["W8"]["omzet"]])
tulis("W9-pivot-tabular.csv", rows)
K["W9"] = {"daun": 6, "omzet": K["W8"]["omzet"], "per_cabang": {c: sum(x[2] for x in it) for c, it in w8.items()}}

# W10 pivot ringkas tanpa kata kunci pivot (judul "Wilayah / Produk"), 3 kelompok, tanpa Grand Total
w10 = {"Jawa Barat": [("Beras", 4200000), ("Gula", 1800000), ("Minyak", 2500000)],
       "Jawa Tengah": [("Beras", 3900000), ("Gula", 1600000)], "Jawa Timur": [("Beras", 4500000), ("Minyak", 2700000)]}
rows = [["Wilayah / Produk", "Penjualan"]]
for c, it in w10.items():
    rows.append([c, sum(x[1] for x in it)]); rows += [[p, v] for p, v in it]
tulis("W10-pivot-ringkas-tanpa-kata-kunci.csv", rows)
K["W10"] = {"daun": 7, "total": sum(x[1] for it in w10.values() for x in it)}

# W11-W13 kontrol rapi
w11 = [("2026-08-%02d" % (i + 1), ["Makan", "Transport", "Pulsa"][i % 3], 25000 + 5000 * (i % 4)) for i in range(20)]
tulis("W11-kontrol-uang-saku.csv", [["Tanggal", "Pos", "Jumlah"]] + [list(r) for r in w11])
K["W11"] = {"baris": 20, "total": sum(r[2] for r in w11), "per_pos": {p: sum(r[2] for r in w11 if r[1] == p) for p in ["Makan", "Transport", "Pulsa"]}}
w12 = [("A-01", "Pulpen", 144, 2500), ("A-02", "Buku Tulis", 60, 4500), ("A-03", "Penggaris", 30, 3000),
       ("A-04", "Spidol", 48, 8500), ("A-05", "Map Plastik", 100, 1500)]
xlsx("W12-kontrol-stok-atk.xlsx", [["Kode", "Barang", "Stok", "Harga"]] + [list(r) for r in w12])
K["W12"] = {"baris": 5, "stok": sum(r[2] for r in w12), "nilai": sum(r[2] * r[3] for r in w12)}
w13 = [("Ani", "XI IPA 1", "88,5"), ("Bayu", "XI IPA 1", "76"), ("Citra", "XI IPA 2", "91,25"), ("Dimas", "XI IPA 2", "69,5"),
       ("Eka", "XI IPA 1", "82")]
tulis("W13-kontrol-nilai.csv", [["Nama", "Kelas", "Nilai Akhir"]] + [list(r) for r in w13], delim=";")
K["W13"] = {"baris": 5, "total": "407.25", "rata_IPA1": "82.17"}

(O / "kunci-v108.json").write_text(json.dumps(K, ensure_ascii=False, indent=1), encoding="utf-8")
print("OK", O)
