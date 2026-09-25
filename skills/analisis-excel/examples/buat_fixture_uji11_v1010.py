#!/usr/bin/env python3
"""Fixture uji ulang v1.0.10 (penguji independen ke-11, cek singkat). Python standar, deterministik.
Fokus: B33 (Total di FILE salah karena angka-teks -> pesan tidak boleh menawarkan angka file sebagai jawaban;
Total file BENAR tapi tepat 2x subtotal -> tetap ditawarkan) dan B34 (produk "Total Care"/"Jumlah Besar" di
TENGAH tabel dan di BARIS TERAKHIR tabel -> tidak boleh jadi kandidat ringkasan palsu) + 2 tabel rapi kontrol.
kunci-uji11-v1010.json dihitung dari data sumber di script ini, TANPA membaca kode skill.
Pakai: python3 buat_fixture_uji11_v1010.py [folder]"""
import json, zipfile, csv, sys
from pathlib import Path
from xml.sax.saxutils import escape
O = Path(sys.argv[1] if len(sys.argv) > 1 else 'fixture-uji11-v1010'); O.mkdir(parents=True, exist_ok=True)
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
            if isinstance(v, tuple):  # ('f', formula, cached)
                cs.append(f'<c r="{ref}"><f>{escape(v[1])}</f><v>{v[2]}</v></c>')
            elif isinstance(v, str):
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


def rp(n):
    return f"{n:,}".replace(",", ".")


# Y1 — Total di FILE SALAH karena 2 sel angka bertipe teks (SUM Excel melewatkannya).
# Kunci independen: total hitungan yang BENAR = sum(vals). Total di file (SUM Excel) lebih kecil.
vals = [980000, 1450000, 640000, 275000, 1200000, 530000, 815000]
teks_idx = {1, 4}   # baris data ke-2 dan ke-5 (0-based) diketik sebagai teks "Rp ..."
rows = [["Tanggal", "Keterangan", "Nominal"]]
for i, v in enumerate(vals):
    rows.append([46270 + i, f"Beban {i+1}", f"Rp {rp(v)}" if i in teks_idx else v])
sum_excel = sum(v for i, v in enumerate(vals) if i not in teks_idx)
rows.append(["TOTAL", "", ("f", "SUM(C2:C8)", sum_excel)])
xlsx("Y1-total-file-salah-angka-teks.xlsx", rows)
K["Y1"] = dict(baris=len(vals), total_benar=sum(vals), total_di_file=sum_excel, teks_baris_data=[i + 2 for i in sorted(teks_idx)],
               harap="Hitungan script = total_benar (jumlah SEMUA 7 baris data). Pesan TIDAK BOLEH menawarkan "
                     "total_di_file sebagai jawaban alternatif; harus menyatakan Total di file perlu dicek / kemungkinan salah.")

# Y2 — Total di FILE BENAR, tapi terhitung 2x karena subtotal tersembunyi (label netral) ikut dijumlah.
dat = [("Toko A", "Beras", 320000), ("Toko A", "Minyak", 145000), ("Toko B", "Beras", 410000),
       ("Toko B", "Gula", 90000), ("Toko C", "Minyak", 260000)]
rows = [["Cabang", "Produk", "Omzet"]] + [list(x) for x in dat]
subtotal_a = dat[0][2] + dat[1][2]
subtotal_b = dat[2][2] + dat[3][2]
subtotal_c = dat[4][2]
rows.append(["Toko A", "(semua produk)", subtotal_a])
rows.append(["Toko B", "(semua produk)", subtotal_b])
rows.append(["Toko C", "(semua produk)", subtotal_c])
total_benar = sum(x[2] for x in dat)
rows.append(["Grand Total", "", total_benar])
csvw("Y2-total-file-tepat-2x-subtotal.csv", rows)
K["Y2"] = dict(baris=len(dat), total_benar=total_benar,
               harap="Hitungan script mentah = 2x total_benar (subtotal ikut terhitung); PENGAMAN SILANG harus "
                     "TEGAS 'DOBEL HITUNG' dan menawarkan total_benar (= angka Grand Total di file) sebagai alternatif.")

# Y3 — produk "Total Care"/"Jumlah Besar" DI TENGAH tabel, baris terisi penuh seperti data lain, TANPA total baris.
dat3 = [("Sabun Cair", 12, 18000), ("Total Care Shampoo", 8, 32000), ("Sikat Gigi", 25, 6000),
        ("Jumlah Besar Deterjen", 5, 45000), ("Pasta Gigi", 15, 12000), ("Sabun Batang", 20, 4000)]
rows = [["Produk", "Stok", "Harga"]] + [list(x) for x in dat3]
csvw("Y3-produk-total-care-tengah.csv", rows)
K["Y3"] = dict(baris=len(dat3), stok=sum(x[1] for x in dat3),
               harap="Semua 6 baris = data; TIDAK boleh ada kandidat/baris dikeluarkan karena label 'Total Care "
                     "Shampoo' atau 'Jumlah Besar Deterjen' di tengah tabel.")

# Y4 — produk berawalan "Total " persis DI BARIS TERAKHIR tabel (ekor), baris terisi penuh seperti data lain,
# TANPA baris ringkasan lain di mana pun (menguji khusus "blok EKOR" yang terpisah dari _label_nama_data).
dat4 = [("Sabun Cair", 12, 18000), ("Sikat Gigi", 25, 6000), ("Pasta Gigi", 15, 12000),
        ("Sabun Batang", 20, 4000), ("Total Care Body Lotion", 5, 45000)]
rows = [["Produk", "Stok", "Harga"]] + [list(x) for x in dat4]
csvw("Y4-produk-total-care-di-ekor.csv", rows)
K["Y4"] = dict(baris=len(dat4), stok=sum(x[1] for x in dat4),
               harap="Semua 5 baris = data (baris terakhir 'Total Care Body Lotion' adalah NAMA PRODUK, bukan "
                     "baris ringkasan). TIDAK boleh dikeluarkan / TIDAK boleh ada PERINGATAN TEGAS palsu.")

# Y5 — kontrol rapi: kas kecil kantor
dat5 = [("2026-09-01", "ATK", 150000), ("2026-09-03", "Konsumsi Rapat", 275000), ("2026-09-05", "Parkir", 25000),
        ("2026-09-08", "ATK", 90000), ("2026-09-12", "Konsumsi Rapat", 340000), ("2026-09-15", "Fotokopi", 60000),
        ("2026-09-18", "Parkir", 30000), ("2026-09-20", "ATK", 120000), ("2026-09-23", "Konsumsi Rapat", 410000)]
rows = [["Tanggal", "Kategori", "Nominal"]] + [list(x) for x in dat5]
csvw("Y5-kontrol-kas-kecil.csv", rows)
per_kat = {}
for _, k, v in dat5:
    per_kat[k] = per_kat.get(k, 0) + v
K["Y5"] = dict(baris=len(dat5), total=sum(x[2] for x in dat5), per_kategori=per_kat)

# Y6 — kontrol rapi xlsx: stok gudang
dat6 = [("Kabel HDMI", 40, 55000), ("Kabel USB", 65, 22000), ("Charger", 30, 85000),
        ("Powerbank", 18, 210000), ("Earphone", 50, 45000)]
rows = [["Barang", "Stok", "Harga"]] + [list(x) for x in dat6]
xlsx("Y6-kontrol-gudang.xlsx", rows)
K["Y6"] = dict(baris=len(dat6), stok=sum(x[1] for x in dat6), nilai=sum(x[1] * x[2] for x in dat6))

(O / "kunci-uji11-v1010.json").write_text(json.dumps(K, indent=2, ensure_ascii=False), encoding="utf-8")
print("OK 6 file baru ->", O)
