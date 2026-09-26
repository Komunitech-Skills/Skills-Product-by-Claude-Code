#!/usr/bin/env python3
"""Fixture uji ulang v1.0.6 (penguji independen ke-7). Fokus: subtotal/rumus XLSX, rumus BUKAN agregat,
ekspor kasir, mutasi bank multi-halaman (header berulang), dua tabel satu file, gaji "Total Divisi",
nilai negatif (retur), duplikat sah. kunci-v106.json dihitung dari data sumber di script ini
(tanpa membaca kode skill). Pakai: python3 buat_fixture_uji_v106.py [folder]"""
import json, sys, zipfile
from pathlib import Path
from xml.sax.saxutils import escape

O = Path(sys.argv[1] if len(sys.argv) > 1 else "fixture-v106"); O.mkdir(parents=True, exist_ok=True)
K = {}

def col(i):
    s = ""; i += 1
    while i: i, r = divmod(i - 1, 26); s = chr(65 + r) + s
    return s

def xlsx(nama, rows, sheet="Data"):
    """rows: list of list; sel = None | str | angka | ("f", rumus, nilai_cache)."""
    xs = []
    for r, row in enumerate(rows, 1):
        cs = []
        for c, v in enumerate(row):
            ref = f"{col(c)}{r}"
            if v is None or v == "": continue
            if isinstance(v, tuple):
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
        z.writestr("xl/workbook.xml", f'<?xml version="1.0" encoding="UTF-8"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="{sheet}" sheetId="1" r:id="rId1"/></sheets></workbook>')
        z.writestr("xl/_rels/workbook.xml.rels", '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/></Relationships>')
        z.writestr("xl/worksheets/sheet1.xml", sh)

def csv(nama, teks):
    (O / nama).write_text(teks, encoding="utf-8")

# ---- S1 XLSX subtotal kelompok: SUM atas sebagian baris, label "Subtotal X" + GRAND TOTAL =C5+C9+C12 (bukan SUM)
data = {"Cabang A": [1200000, 800000, 450000], "Cabang B": [2000000, 350000, 125000], "Cabang C": [600000, 900000]}
rows = [["Cabang", "Kasir", "Omzet"]]; subs = []
for cab, vals in data.items():
    a = len(rows) + 1
    for i, v in enumerate(vals): rows.append([cab, f"Kasir {i+1}", v])
    b = len(rows); rows.append([f"Subtotal {cab}", None, ("f", f"SUM(C{a}:C{b})", sum(vals))]); subs.append(len(rows))
tot = sum(sum(v) for v in data.values())
rows.append(["GRAND TOTAL", None, ("f", "+".join(f"C{s}" for s in subs), tot)])
xlsx("S1-subtotal-sum-berlabel.xlsx", rows)
K["S1"] = {"baris": 8, "total": tot, "per_cabang": {k: sum(v) for k, v in data.items()}}

# ---- S1b sama tapi subtotal TANPA label (hanya rumus SUM) dan grand total =SUM(C5,C9,C12) tanpa label
rows = [["Cabang", "Kasir", "Omzet"]]; subs = []
for cab, vals in data.items():
    a = len(rows) + 1
    for i, v in enumerate(vals): rows.append([cab, f"Kasir {i+1}", v])
    b = len(rows); rows.append([None, None, ("f", f"SUM(C{a}:C{b})", sum(vals))]); subs.append(len(rows))
rows.append([None, None, ("f", "SUM(" + ",".join(f"C{s}" for s in subs) + ")", tot)])
xlsx("S1b-subtotal-sum-tanpa-label.xlsx", rows)
K["S1b"] = {"baris": 8, "total": tot}

# ---- S1c grand total berupa =C5+C9+C12 TANPA label (rumus penjumlahan, bukan fungsi agregat)
rows = rows[:-1] + [[None, None, ("f", "+".join(f"C{s}" for s in subs), tot)]]
xlsx("S1c-grandtotal-plus-tanpa-label.xlsx", rows)
K["S1c"] = {"baris": 8, "total": tot, "harapan": "subtotal SUM dibuang; grand total =C5+C9+C12 tanpa label: dibuang ATAU dihitung + peringatan tegas dg alternatif benar"}

# ---- S2 XLSX rumus BUKAN agregat: Total =B*C per baris, dan SUM mendatar (=SUM(B2:D2)) per baris = DATA
peg = [("Andi", 150000, 200000, 50000), ("Budi", 90000, 200000, 50000), ("Citra", 0, 200000, 75000),
       ("Dewi", 120000, 180000, 50000), ("Eko", 150000, 200000, 50000)]
rows = [["Nama", "Transport", "Makan", "Pulsa", "Total"]]
for i, (n, t, m, p) in enumerate(peg, 2):
    rows.append([n, t, m, p, ("f", f"SUM(B{i}:D{i})", t + m + p)])
xlsx("S2-sum-mendatar-per-baris.xlsx", rows)
K["S2"] = {"baris": 5, "total": sum(t + m + p for _, t, m, p in peg), "transport": sum(x[1] for x in peg)}

# ---- S2b rumus perkalian per baris + total berlabel di ekor
brg = [("Semen 40kg", 20, 65000), ("Pasir (m3)", 3, 250000), ("Bata merah", 1000, 900), ("Cat 5kg", 4, 185000), ("Paku 1kg", 5, 28000)]
rows = [["Barang", "Qty", "Harga", "Subtotal"]]
for i, (b, q, h) in enumerate(brg, 2): rows.append([b, q, h, ("f", f"B{i}*C{i}", q * h)])
n = len(rows)
rows.append(["TOTAL", ("f", f"SUM(B2:B{n})", sum(q for _, q, _ in brg)), None, ("f", f"SUM(D2:D{n})", sum(q * h for _, q, h in brg))])
xlsx("S2b-rumus-kali-per-baris.xlsx", rows)
K["S2b"] = {"baris": 5, "total": sum(q * h for _, q, h in brg), "qty": sum(q for _, q, _ in brg)}

# ---- S2c AVERAGE mendatar per baris (nilai rata-rata siswa) = DATA
sis = [("Ayu", 80, 90, 85), ("Bima", 70, 75, 80), ("Caca", 95, 85, 90), ("Doni", 60, 70, 65)]
rows = [["Nama", "UH1", "UH2", "UTS", "Rata-rata"]]
for i, (n_, a, b, c) in enumerate(sis, 2):
    rows.append([n_, a, b, c, ("f", f"AVERAGE(B{i}:D{i})", (a + b + c) / 3)])
xlsx("S2c-average-mendatar-nilai-siswa.xlsx", rows)
K["S2c"] = {"baris": 4, "jumlah_UH1": sum(x[1] for x in sis), "jumlah_rata": round(sum((a + b + c) / 3 for _, a, b, c in sis), 4)}

# ---- S3 XLSX ekspor kasir TANPA rumus: judul di atas, baris total & rincian pembayaran di bawah
trx = [("TRX-0001", "08:05", "Kopi Susu", 2, 36000), ("TRX-0002", "08:20", "Roti Bakar", 1, 22000),
       ("TRX-0003", "09:10", "Kopi Susu", 1, 18000), ("TRX-0004", "09:45", "Es Teh", 3, 15000),
       ("TRX-0005", "10:30", "Nasi Goreng", 2, 50000), ("TRX-0006", "11:00", "Kopi Susu", 1, 18000)]
T = sum(x[4] for x in trx)
rows = [["LAPORAN PENJUALAN - KEDAI SENJA"], ["Periode: 20/09/2026 - 20/09/2026"], [],
        ["No Transaksi", "Jam", "Item", "Qty", "Total"]]
for t in trx: rows.append(list(t))
rows += [[], ["Total Penjualan", None, None, sum(x[3] for x in trx), T], ["Tunai", None, None, None, 64000],
         ["QRIS", None, None, None, T - 64000]]
xlsx("S3-ekspor-kasir-tanpa-rumus.xlsx", rows, "Laporan")
K["S3"] = {"baris": 6, "total": T, "qty": sum(x[3] for x in trx),
           "harapan": "Tunai/QRIS (rincian pembayaran) di ekor = ringkasan; ikut dihitung diam-diam = c"}

# ---- S4 CSV mutasi bank multi-halaman: header berulang di tengah + teks halaman
hal1 = [("01/09/2026", "TRSF E-BANKING CR 0109/ANDI", "1.500.000,00", "CR"),
        ("02/09/2026", "BIAYA ADM", "15.000,00", "DB"),
        ("03/09/2026", "TARIKAN ATM 03/09", "500.000,00", "DB"),
        ("05/09/2026", "TRSF E-BANKING CR 0509/BUDI", "750.000,00", "CR")]
hal2 = [("07/09/2026", "BYR VIA E-BANKING PLN", "320.000,00", "DB"),
        ("10/09/2026", "SETORAN TUNAI", "2.000.000,00", "CR"),
        ("12/09/2026", "TRSF E-BANKING DB 1209/TOKO", "1.250.000,00", "DB")]
H = "Tanggal,Keterangan,Jumlah,Jenis"
t = ["MUTASI REKENING,,,", "No. Rekening: 1234xxxx90,,,", ",,,", H]
t += [",".join(f'"{c}"' if "," in c else c for c in r) for r in hal1]
t += [",,,", "Halaman 1 dari 2,,,", ",,,", "MUTASI REKENING,,,", H]
t += [",".join(f'"{c}"' if "," in c else c for c in r) for r in hal2]
t += [",,,", "Halaman 2 dari 2,,,"]
csv("S4-mutasi-multi-halaman.csv", "\n".join(t) + "\n")
num = lambda s: int(s.split(",")[0].replace(".", ""))
allr = hal1 + hal2
K["S4"] = {"baris": 7, "jumlah": sum(num(r[2]) for r in allr), "CR": sum(num(r[2]) for r in allr if r[3] == "CR"),
           "DB": sum(num(r[2]) for r in allr if r[3] == "DB"),
           "harapan": "7 transaksi; header berulang & 'Halaman x dari y' tidak jadi data; data halaman 2 tidak hilang"}

# ---- S5 CSV dua tabel dalam satu file
p = [("2026-09-01", "Kaos", 3, 225000), ("2026-09-02", "Topi", 2, 90000), ("2026-09-03", "Kaos", 1, 75000)]
q = [("2026-09-01", "Sewa lapak", 500000), ("2026-09-02", "Plastik", 35000)]
t = ["Tanggal,Produk,Qty,Nominal"] + [",".join(map(str, r)) for r in p] + [",,,", "PENGELUARAN,,,", "Tanggal,Keterangan,Nominal,"] + [",".join(map(str, r)) + "," for r in q]
csv("S5-dua-tabel.csv", "\n".join(t) + "\n")
K["S5"] = {"baris_tabel1": 3, "total_tabel1": sum(r[3] for r in p), "total_tabel2": sum(r[2] for r in q),
           "harapan": "tabel 1 saja + info tabel kedua, ATAU GAGAL/peringatan tegas; angka pengeluaran tercampur diam-diam = c"}

# ---- S6 CSV gaji dengan baris "Total Divisi" per divisi + Grand Total
div = {"Produksi": [("Rudi", 4500000, 500000), ("Sari", 4200000, 500000), ("Tono", 4800000, 750000)],
       "Gudang": [("Umar", 3900000, 300000)],
       "Admin": [("Vina", 5000000, 600000), ("Wawan", 4600000, 400000)]}
t = ["Divisi,Nama,Gaji Pokok,Tunjangan"]
for d, ps in div.items():
    for n_, g, tj in ps: t.append(f"{d},{n_},{g},{tj}")
    t.append(f",Total Divisi {d},{sum(x[1] for x in ps)},{sum(x[2] for x in ps)}")
G = sum(x[1] for ps in div.values() for x in ps); TJ = sum(x[2] for ps in div.values() for x in ps)
t.append(f",GRAND TOTAL,{G},{TJ}")
csv("S6-gaji-total-divisi.csv", "\n".join(t) + "\n")
K["S6"] = {"baris": 6, "gaji_pokok": G, "tunjangan": TJ, "per_divisi_gaji": {d: sum(x[1] for x in ps) for d, ps in div.items()},
           "harapan": "6 pegawai; Total Divisi dibuang+disebut ATAU dihitung + PERINGATAN TEGAS dg total alternatif benar"}

# ---- S6b sama, tetapi label "Total Divisi X" di kolom PERTAMA (Divisi) dan Nama kosong
t = ["Divisi,Nama,Gaji Pokok,Tunjangan"]
for d, ps in div.items():
    for n_, g, tj in ps: t.append(f"{d},{n_},{g},{tj}")
    t.append(f"Total Divisi {d},,{sum(x[1] for x in ps)},{sum(x[2] for x in ps)}")
csv("S6b-gaji-total-divisi-kolom1-tanpa-grand.csv", "\n".join(t) + "\n")
K["S6b"] = {"baris": 6, "gaji_pokok": G, "tunjangan": TJ,
            "harapan": "baris terakhir 'Total Divisi Admin' di ekor boleh dibuang; Total Divisi tengah -> tegas + alternatif"}

# ---- S7 CSV nilai negatif (retur), format -150000, (75.000), -Rp 50.000
t = ["Tanggal;Produk;Qty;Nilai",
     "01/09/2026;Sepatu A;2;700000", "02/09/2026;Sepatu B;1;450000", "03/09/2026;Retur Sepatu A;-1;-350000",
     "04/09/2026;Sandal;3;(75.000)", "05/09/2026;Sepatu B;2;900000", "06/09/2026;Retur Sandal;-1;-Rp 50.000",
     "07/09/2026;Kaos kaki;4;100000"]
csv("S7-retur-negatif.csv", "\n".join(t) + "\n")
K["S7"] = {"baris": 7, "nilai_bersih_bila_kurung_negatif": 700000 + 450000 - 350000 - 75000 + 900000 - 50000 + 100000,
           "catatan": "'(75.000)' = negatif gaya akuntansi (data 'Sandal' 3 pcs sebenarnya jual, tetapi file menulis kurung); dibaca -75.000 atau dilaporkan tidak valid = OK; dibaca +75.000 diam-diam = c",
           "retur": -400000}

# ---- S8 CSV duplikat sah + nilai berulang
t = ["Tanggal,Pelanggan,Barang,Jumlah",
     "2026-09-10,Bu Rina,Galon,20000", "2026-09-10,Bu Rina,Galon,20000", "2026-09-10,Pak Joko,Gas 3kg,22000",
     "2026-09-11,Bu Rina,Galon,20000", "2026-09-11,Pak Joko,Gas 3kg,22000", "2026-09-11,Pak Joko,Gas 3kg,22000",
     "2026-09-12,Bu Sri,Galon,20000", "2026-09-12,Bu Sri,Beras 5kg,68000"]
csv("S8-duplikat-sah.csv", "\n".join(t) + "\n")
K["S8"] = {"baris": 8, "total": 20000 * 4 + 22000 * 3 + 68000, "harapan": "duplikat tetap dihitung (boleh info)"}

# ---- S9 XLSX total di ATAS data (baris 2 tepat di bawah header) dengan rumus SUM berlabel "Jumlah"
it = [("Listrik", 850000), ("Air", 210000), ("Internet", 450000), ("Kebersihan", 50000)]
rows = [["Pos", "Biaya"], ["Jumlah", ("f", f"SUM(B3:B{2+len(it)})", sum(v for _, v in it))]] + [list(x) for x in it]
xlsx("S9-total-di-atas-rumus.xlsx", rows)
K["S9"] = {"baris": 4, "total": sum(v for _, v in it)}

# ---- S10 CSV transaksi kebetulan = jumlah di atas, lalu Total berlabel di ekor
t = ["Tanggal,Keterangan,Nominal", "2026-09-01,Beli pulsa,100000", "2026-09-02,Bensin,200000",
     "2026-09-03,Servis motor,300000", "Total,,600000"]
csv("S10-kebetulan-lalu-total.csv", "\n".join(t) + "\n")
K["S10"] = {"baris": 3, "total": 600000}

# ---- S11 XLSX gaya Excel Data > Subtotal: "A Total" dg SUBTOTAL(9,..) di tengah, "Grand Total" SUBTOTAL(9, seluruh)
grp = {"Jakarta": [3100000, 2750000], "Bandung": [1800000], "Surabaya": [2200000, 950000, 400000]}
rows = [["Kota", "Sales", "Penjualan"]]; first = 2
for kota, vals in grp.items():
    a = len(rows) + 1
    for i, v in enumerate(vals): rows.append([kota, f"S{i+1}", v])
    rows.append([f"{kota} Total", None, ("f", f"SUBTOTAL(9,C{a}:C{len(rows)})", sum(vals))])
last = len(rows)
TT = sum(sum(v) for v in grp.values())
rows.append(["Grand Total", None, ("f", f"SUBTOTAL(9,C2:C{last})", TT)])
xlsx("S11-excel-data-subtotal.xlsx", rows)
K["S11"] = {"baris": 6, "total": TT, "per_kota": {k: sum(v) for k, v in grp.items()}}

# ---- S12 CSV versi nilai polos dari S11 (disalin "Paste Values" lalu Save As CSV)
t = ["Kota,Sales,Penjualan"]
for kota, vals in grp.items():
    for i, v in enumerate(vals): t.append(f"{kota},S{i+1},{v}")
    t.append(f"{kota} Total,,{sum(vals)}")
t.append(f"Grand Total,,{TT}")
csv("S12-data-subtotal-nilai-polos.csv", "\n".join(t) + "\n")
K["S12"] = {"baris": 6, "total": TT, "harapan": "Grand Total ekor dibuang; 'X Total' tengah dibuang ATAU tegas + alternatif benar"}

(O / "kunci-v106.json").write_text(json.dumps(K, indent=1, ensure_ascii=False), encoding="utf-8")
print(f"{len(K)} fixture ditulis ke {O}")
