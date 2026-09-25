#!/usr/bin/env python3
"""Fixture uji ulang v1.0.2 (penguji independen ke-3). Python standar, deterministik.
F1 ekspor marketplace (BOM, alamat 3 baris berkoma+angka, "" di sel, emoji, baris kosong); F2 rekap WA (;, 1.234,00, catatan multi-baris);
F3/F3b/F3c CSV rusak (kutip terbuka di tengah); F4 XLSX Ringkasan + Jan..Apr + Rekap Akhir; F4b rekap berjudul kolom mirip data;
F5 sel multi-baris sah mirip baris data. kunci-baru.json = kunci independen. Pakai: python3 buat_fixture_uji_v102.py [folder]"""
import csv, io, json, random, zipfile
from datetime import date, timedelta
from pathlib import Path
from xml.sax.saxutils import escape
import sys
O = Path(sys.argv[1] if len(sys.argv) > 1 else "fixture-v102"); O.mkdir(parents=True, exist_ok=True)
r = random.Random(20260925); K = {}
def rp(v): return "Rp " + f"{v:,}".replace(",", ".")
# ---------- F1: ekspor marketplace, UTF-8 BOM, koma, alamat 3 baris berkoma+angka, "" di sel, emoji, baris kosong antar rekaman
kota = ["Kab. Bogor", "Kota Depok", "Bekasi", "Tangerang Selatan"]
prod = ["Gamis \"Syar'i\" 🌙", "Kopi Gayo 250gr ☕", "Sambal Roa 🌶️ 2 btl", "Kerudung Pashmina, Motif 💐"]
rows = []
for i in range(1, 41):
    k = r.choice(kota); p = r.choice(prod); q = r.randint(1, 4); h = r.choice([35000, 49900, 75000, 120000])
    tgl = date(2026, 9, 1) + timedelta(days=r.randint(0, 29))
    al = f"Jl. Mawar No. {r.randint(1,99)}, RT {r.randint(1,9):02d}/RW {r.randint(1,9):02d}\nKel. Sukamaju, Kec. Cibinong\n{k}, Jawa Barat {16900+i}"
    if i % 5 == 0: al = f"Perum Griya Asri Blok C{i}, No. 7"  # satu baris
    cat = r.choice(["", "Tolong \"cepat\" ya kak 🙏, makasih", "Bungkus kado, 2 lapis\nKartu ucapan: \"Selamat, sukses!\"", "COD, jam 10.00"])
    rows.append([f"2609{i:05d}", tgl.strftime("%d/%m/%Y %H:%M") if False else tgl.strftime("%Y-%m-%d"), f"Pembeli {i} 😊", al, k, p, q, rp(q*h), cat])
buf = io.StringIO(); w = csv.writer(buf, lineterminator="\r\n")
w.writerow(["No. Pesanan", "Tanggal Pesanan", "Nama Pembeli", "Alamat Pengiriman", "Kota", "Produk", "Jumlah", "Total Bayar", "Catatan Pembeli"])
for j, row in enumerate(rows):
    w.writerow(row)
    if j % 7 == 3: buf.write("\r\n")  # baris kosong
buf.write("\r\n\r\n")
(O / "F1-ekspor-marketplace.csv").write_text("﻿" + buf.getvalue(), encoding="utf-8", newline="")
tot = lambda rs, key: {k2: sum(int(x[7][3:].replace(".", "")) for x in rs if key(x) == k2) for k2 in sorted({key(x) for x in rs})}
K["F1"] = {"baris": len(rows), "total_bayar": sum(int(x[7][3:].replace(".", "")) for x in rows), "qty": sum(x[6] for x in rows),
           "per_kota": tot(rows, lambda x: x[4]), "per_produk": tot(rows, lambda x: x[5]),
           "sel_multibaris": sum(1 for x in rows for c in x if "\n" in str(c))}
# ---------- F2: rekap WA, ;, angka Indonesia desimal, "" di sel, catatan multi-baris berisi ; dan angka
rows2 = []
for i in range(1, 26):
    nm = r.choice(["Bu Rina", "Pak Joko", "Mbak Sari", "Koh Ahmad"])
    v = r.randint(10, 500) * 1000 + r.choice([0, 500])
    note = r.choice(["", "Transfer BCA; sisa 50.000 besok", "DP 30%\nPelunasan 15/09; 2 termin", "Katanya \"nanti sore\"; oke 👍"])
    rows2.append([str(i), nm, (date(2026, 8, 20) + timedelta(days=r.randint(0, 40))).strftime("%d/%m/%Y"), f"{v:,}".replace(",", ".") + (",00" if i % 3 else ""), note])
buf = io.StringIO(); w = csv.writer(buf, delimiter=";", lineterminator="\n")
w.writerow(["No", "Pelanggan", "Tanggal", "Nominal", "Catatan WA"])
for row in rows2: w.writerow(row)
(O / "F2-rekap-wa.csv").write_text(buf.getvalue(), encoding="utf-8", newline="")
vals2 = [int(x[3].split(",")[0].replace(".", "")) for x in rows2]
K["F2"] = {"baris": 25, "total": sum(vals2), "per_pelanggan": {n: sum(v for x, v in zip(rows2, vals2) if x[1] == n) for n in sorted({x[1] for x in rows2})},
           "agu": sum(v for x, v in zip(rows2, vals2) if x[2][3:5] == "08"), "sep": sum(v for x, v in zip(rows2, vals2) if x[2][3:5] == "09")}
# ---------- F3: CSV rusak sungguhan: kutip terbuka di tengah, ditutup 4 baris kemudian (field count cocok)
L = ["No,Nama,Kota,Total"] + [f"{i},Orang {i},Bogor,{i*1000}" for i in range(1, 21)]
L[5] = '5,"Orang 5,Bogor,5000'; L[9] = '9,Orang 9",Bogor,9000'
(O / "F3-rusak-tertutup-jauh.csv").write_text("\n".join(L) + "\n", encoding="utf-8")
# F3b: kutip terbuka, tertutup di baris berikutnya (hanya 1 baris tertelan, jumlah sel cocok) -> jebakan senyap
L = ["No,Nama,Kota,Total"] + [f"{i},Orang {i},Bogor,{i*1000}" for i in range(1, 21)]
L[5] = '5,"Orang 5,Bogor,5000'; L[6] = '6,Orang 6",Bogor,6000'
(O / "F3b-rusak-satu-baris.csv").write_text("\n".join(L) + "\n", encoding="utf-8")
# F3c: kutip terbuka di tengah, tak pernah ditutup
L = ["No,Nama,Kota,Total"] + [f"{i},Orang {i},Bogor,{i*1000}" for i in range(1, 21)]
L[10] = '10,"Orang 10,Bogor,10000'
(O / "F3c-rusak-terbuka.csv").write_text("\n".join(L) + "\n", encoding="utf-8")
K["F3"] = {"benar_total_semua": sum(i*1000 for i in range(1, 21)), "harapan": "GAGAL atau peringatan tegas, bukan angka diam-diam"}
# ---------- F4: XLSX 6 sheet: Ringkasan (pertama), Jan..Apr (data + TOTAL), Rekap Akhir (terakhir, struktur beda)
def col(i): return chr(65 + i)
def xlsx(path, sheets):
    z = zipfile.ZipFile(path, "w")
    z.writestr("[Content_Types].xml", '<?xml version="1.0"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>' + "".join(f'<Override PartName="/xl/worksheets/sheet{i+1}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' for i in range(len(sheets))) + '</Types>')
    z.writestr("_rels/.rels", '<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>')
    z.writestr("xl/workbook.xml", '<?xml version="1.0"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>' + "".join(f'<sheet name="{escape(n)}" sheetId="{i+1}" r:id="rId{i+1}"/>' for i, (n, _) in enumerate(sheets)) + '</sheets></workbook>')
    z.writestr("xl/_rels/workbook.xml.rels", '<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + "".join(f'<Relationship Id="rId{i+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i+1}.xml"/>' for i in range(len(sheets))) + '</Relationships>')
    for i, (n, rs) in enumerate(sheets):
        x = []
        for ri, row in enumerate(rs, 1):
            cs = []
            for ci, v in enumerate(row):
                ref = f"{col(ci)}{ri}"
                if v is None: continue
                if isinstance(v, int): cs.append(f'<c r="{ref}"><v>{v}</v></c>')
                else: cs.append(f'<c r="{ref}" t="inlineStr"><is><t>{escape(v)}</t></is></c>')
            x.append(f'<row r="{ri}">' + "".join(cs) + '</row>')
        z.writestr(f"xl/worksheets/sheet{i+1}.xml", '<?xml version="1.0"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>' + "".join(x) + '</sheetData></worksheet>')
    z.close()
kat = ["Bahan Baku", "Gaji", "Sewa", "Listrik"]
data = {}; sheets = []
for m, bl in enumerate(["Jan", "Feb", "Mar", "Apr"], 1):
    rs = [[f"{d:02d}/{m:02d}/2026", r.choice(kat), f"Belanja {bl} #{d}", r.randint(5, 300) * 5000] for d in range(1, r.randint(15, 25))]
    data[bl] = rs
    sheets.append((bl, [["Tanggal", "Kategori", "Keterangan", "Jumlah"]] + rs + [["TOTAL", None, None, sum(x[3] for x in rs)]]))
ring = [["Bulan", "Total Biaya", "Catatan"]] + [[b, sum(x[3] for x in data[b]), "ok"] for b in data] + [["TOTAL", sum(x[3] for b in data for x in data[b]), None]]
rek = [["Kategori", "Jan", "Feb", "Mar", "Apr"]] + [[k2] + [sum(x[3] for x in data[b] if x[1] == k2) for b in data] for k2 in kat]
xlsx(O / "F4-biaya-4-bulan.xlsx", [("Ringkasan", ring)] + sheets + [("Rekap Akhir", rek)])
allr = [x for b in data for x in data[b]]
K["F4"] = {"baris_per_sheet": {b: len(data[b]) for b in data}, "baris": len(allr), "total": sum(x[3] for x in allr),
           "per_sheet": {b: sum(x[3] for x in data[b]) for b in data}, "per_kategori": {k2: sum(x[3] for x in allr if x[1] == k2) for k2 in kat},
           "pivot_kat_x_sheet": {k2: {b: sum(x[3] for x in data[b] if x[1] == k2) for b in data} for k2 in kat}}
# F4b: jebakan — rekap terakhir berjudul kolom mirip data (Tanggal, Kategori, Jumlah) -> harus tidak menggandakan diam-diam
rek2 = [["Tanggal", "Kategori", "Jumlah"]] + [[f"30/04/2026", k2, K["F4"]["per_kategori"][k2]] for k2 in kat]
xlsx(O / "F4b-rekap-mirip.xlsx", [("Ringkasan", ring)] + sheets + [("Rekap Kategori", rek2)])
# ---------- F5: sel multi-baris SAH yang isinya mirip baris data (rincian pesanan)
L5 = [["Tanggal", "Pelanggan", "Rincian", "Total"]]
tot5 = 0
for i in range(1, 11):
    t = 100000 + i * 1000; tot5 += t
    rinc = f"Kaos, 2, 50000\nTopi, 1, 30000\nOngkir, 1, {20000 + i*1000}" if i % 3 == 0 else "Kaos, 1"
    L5.append([f"2026-09-{i:02d}", f"Toko {i}", rinc, t])
buf = io.StringIO(); csv.writer(buf, lineterminator="\n").writerows(L5)
(O / "F5-rincian-mirip-data.csv").write_text(buf.getvalue(), encoding="utf-8")
K["F5"] = {"baris": 10, "total": tot5}
(O / "kunci-baru.json").write_text(json.dumps(K, indent=1, ensure_ascii=False))
print(json.dumps(K, ensure_ascii=False))
