#!/usr/bin/env python3
"""Fixture uji ulang v1.0.7 (penguji independen ke-8). Python standar, deterministik.
Fokus tata letak BARU: stok dengan baris judul kategori + subtotal TERISI LENGKAP, pivot Excel disalin sebagai nilai
(ID & EN, bentuk ringkas dengan subtotal di ATAS kelompok), absensi dengan "Jumlah Hadir" per karyawan, jurnal umum
dengan baris TOTAL terisi lengkap, penjualan per cabang dengan "Subtotal Cabang" terisi lengkap, e-Faktur CSV
(rekaman FK/LT/OF), daftar faktur Coretax, ekspor GoBiz & GrabMerchant (gaya angka Inggris), CSV koma desimal Eropa,
bulan melebar Jan..Des, tabel tanpa judul kolom, + 3 tabel rapi kontrol. Bentuk file meniru pola umum (bukan salinan
file asli). kunci-v107.json dihitung dari data sumber di script ini, TANPA membaca kode skill.
Pakai: python3 buat_fixture_uji_v107.py [folder]"""
import json, sys, zipfile
from pathlib import Path
from xml.sax.saxutils import escape
from decimal import Decimal as D

O = Path(sys.argv[1] if len(sys.argv) > 1 else "fixture-v107"); O.mkdir(parents=True, exist_ok=True)
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


def idr(n):
    return f"{n:,}".replace(",", ".")


# V1 stok: judul kategori (satu sel) + subtotal TERISI LENGKAP (nilai, bukan rumus) + TOTAL
kel = {"SEMEN": [("SM-01", "Semen Tiga Roda 50kg", "sak", 40, 62000), ("SM-02", "Semen Gresik 40kg", "sak", 25, 55000)],
       "CAT": [("CT-01", "Cat Avian 1kg", "kaleng", 30, 45000), ("CT-02", "Cat Dulux 2,5L", "kaleng", 12, 145000),
               ("CT-03", "Cat Nippon 5kg", "pail", 6, 310000)],
       "BESI": [("BS-01", "Besi beton 10mm", "batang", 100, 72000), ("BS-02", "Besi beton 8mm", "batang", 80, 48000)]}
rows = [["Kode", "Nama Barang", "Satuan", "Stok", "Harga Beli", "Nilai Stok"]]
tot_s = tot_n = 0
for k, items in kel.items():
    rows.append([k])
    ss = sn = 0
    for kd, nm, sat, st, hb in items:
        rows.append([kd, nm, sat, st, hb, st * hb]); ss += st; sn += st * hb
    rows.append([k[:2] + "-SUB", f"Subtotal {k.title()}", items[0][2], ss, round(sn / ss), sn])
    tot_s += ss; tot_n += sn
rows.append(["TOTAL", "Total Nilai Stok", "-", tot_s, "-", tot_n])
xlsx("V1-stok-kategori-subtotal-lengkap.xlsx", rows)
K["V1"] = {"baris": 7, "stok": tot_s, "nilai": tot_n, "harapan": "judul kategori & subtotal terisi lengkap tidak boleh ikut diam-diam"}

# V2 pivot Excel ID disalin sebagai nilai
piv = {"Kopi Susu": [1200000, 1350000, 1500000], "Roti Bakar": [800000, 750000, 900000], "Teh Tarik": [400000, 500000, 450000]}
rows = [["Jumlah dari Penjualan", "Label Kolom"], ["Label Baris", "Jul", "Agu", "Sep", "Total Keseluruhan"]]
for p, v in piv.items(): rows.append([p] + v + [sum(v)])
colsum = [sum(v[i] for v in piv.values()) for i in range(3)]
rows.append(["Total Keseluruhan"] + colsum + [sum(colsum)])
xlsx("V2-pivot-nilai-id.xlsx", rows)
K["V2"] = {"baris": 3, "jul": colsum[0], "agu": colsum[1], "sep": colsum[2], "total": sum(colsum)}

# V3 pivot EN bentuk ringkas (compact): subtotal kelompok di ATAS anak-anaknya, tanpa kata Total
tulis("V3-pivot-ringkas-en.csv", [["Row Labels", "Sum of Amount"], ["Jawa", 5000000], ["Kopi", 3000000], ["Teh", 2000000],
                                   ["Sumatra", 2500000], ["Kopi", 1500000], ["Teh", 1000000], ["Grand Total", 7500000]])
K["V3"] = {"baris_daun": 4, "total": 7500000, "harapan": "baris Jawa/Sumatra = subtotal di atas; dihitung diam-diam (15.000.000) = c"}

# V4 absensi dengan baris "Jumlah Hadir" per karyawan (terisi lengkap)
ab = {"Budi": [("H", 8), ("H", 8), ("S", 0), ("H", 8), ("H", 7)], "Sari": [("H", 8), ("H", 8), ("H", 8), ("I", 0), ("H", 8)],
      "Andi": [("H", 8), ("A", 0), ("H", 8), ("H", 8), ("H", 6)]}
rows = [["Nama", "Tanggal", "Status", "Jam Kerja"]]; jam = 0
for n, hs in ab.items():
    for i, (s, j) in enumerate(hs): rows.append([n, f"2026-09-0{i+1}", s, j]); jam += j
    rows.append([n, "Jumlah Hadir", sum(1 for s, _ in hs if s == "H"), sum(j for _, j in hs)])
tulis("V4-absensi-jumlah-hadir.csv", rows)
K["V4"] = {"baris": 15, "jam": jam, "hadir_H": sum(1 for hs in ab.values() for s, _ in hs if s == "H")}

# V5 jurnal umum ; + angka ID, baris TOTAL terisi di semua kolom
ju = [("01/09/2026", "JU-001", "Kas", "Setoran modal", 50000000, 0), ("01/09/2026", "JU-001", "Modal", "Setoran modal", 0, 50000000),
      ("03/09/2026", "JU-002", "Persediaan", "Beli barang", 12500000, 0), ("03/09/2026", "JU-002", "Kas", "Beli barang", 0, 12500000),
      ("10/09/2026", "JU-003", "Kas", "Penjualan tunai", 8750000, 0), ("10/09/2026", "JU-003", "Penjualan", "Penjualan tunai", 0, 8750000),
      ("15/09/2026", "JU-004", "Beban Sewa", "Sewa September", 3000000, 0), ("15/09/2026", "JU-004", "Kas", "Sewa September", 0, 3000000),
      ("30/09/2026", "JU-005", "Beban Gaji", "Gaji September", 6500000, 0), ("30/09/2026", "JU-005", "Kas", "Gaji September", 0, 6500000)]
rows = [["Tanggal", "No Bukti", "Akun", "Keterangan", "Debit", "Kredit"]]
for t, b, a, k, d, c in ju: rows.append([t, b, a, k, idr(d) if d else "", idr(c) if c else ""])
td = sum(x[4] for x in ju); tk = sum(x[5] for x in ju)
rows.append(["30/09/2026", "JU-TOTAL", "TOTAL", "Total jurnal September", idr(td), idr(tk)])
tulis("V5-jurnal-umum-total-lengkap.csv", rows, ";")
K["V5"] = {"baris": 10, "debit": td, "kredit": tk, "kas_debit": 58750000}

# V6 penjualan per cabang, "Subtotal Cabang X" terisi lengkap + Grand Total terisi lengkap
cab = {"Bekasi": [("02/09/2026", "Kopi", 5, 750000), ("05/09/2026", "Roti", 6, 540000), ("09/09/2026", "Teh", 3, 270000)],
       "Bogor": [("03/09/2026", "Kopi", 4, 600000), ("06/09/2026", "Roti", 2, 180000), ("12/09/2026", "Teh", 7, 630000)],
       "Depok": [("04/09/2026", "Kopi", 8, 1200000), ("08/09/2026", "Roti", 5, 450000)]}
rows = [["Tanggal", "Cabang", "Produk", "Qty", "Omzet"]]; tq = to = 0
for c, it in cab.items():
    for t, p, q, o in it: rows.append([t, c, p, q, o])
    sq = sum(x[2] for x in it); so = sum(x[3] for x in it); tq += sq; to += so
    rows.append(["30/09/2026", c, f"Subtotal Cabang {c}", sq, so])
rows.append(["30/09/2026", "Semua Cabang", "Grand Total", tq, to])
tulis("V6-cabang-subtotal-lengkap.csv", rows)
K["V6"] = {"baris": 8, "qty": tq, "omzet": to, "per_cabang": {c: sum(x[3] for x in it) for c, it in cab.items()}}

# V7 e-Faktur (format lama) CSV: 3 jenis rekaman FK/LT/OF dengan jumlah kolom berbeda
fk_h = ["FK", "KD_JENIS_TRANSAKSI", "FG_PENGGANTI", "NOMOR_FAKTUR", "MASA_PAJAK", "TAHUN_PAJAK", "TANGGAL_FAKTUR", "NPWP", "NAMA",
        "ALAMAT_LENGKAP", "JUMLAH_DPP", "JUMLAH_PPN", "JUMLAH_PPNBM", "ID_KETERANGAN_TAMBAHAN", "FG_UANG_MUKA", "UANG_MUKA_DPP",
        "UANG_MUKA_PPN", "UANG_MUKA_PPNBM", "REFERENSI"]
lt_h = ["LT", "NPWP", "NAMA", "JALAN", "BLOK", "NOMOR", "RT", "RW", "KECAMATAN", "KELURAHAN", "KABUPATEN", "PROPINSI", "KODE_POS", "NOMOR_TELEPON"]
of_h = ["OF", "KODE_OBJEK", "NAMA", "HARGA_SATUAN", "JUMLAH_BARANG", "HARGA_TOTAL", "DISKON", "DPP", "PPN", "TARIF_PPNBM", "PPNBM"]
fak = [("0100026000001", "01/09/2026", "012345678901000", "PT Maju Jaya", [("Kursi kantor", 1500000, 4), ("Meja kerja", 2000000, 2)]),
       ("0100026000002", "08/09/2026", "023456789012000", "CV Sentosa", [("Lemari arsip", 2500000, 2)]),
       ("0100026000003", "15/09/2026", "034567890123000", "UD Berkah", [("Rak besi", 750000, 2), ("Kursi tunggu", 500000, 2)])]
rows = [fk_h, lt_h, of_h]; tdpp = tppn = 0
for no, tg, npwp, nama, its in fak:
    dpp = sum(h * q for _, h, q in its); ppn = dpp * 11 // 100; tdpp += dpp; tppn += ppn
    rows.append(["FK", "01", "0", no, "9", "2026", tg, npwp, nama, "Jl. Contoh No. 1, Bekasi", dpp, ppn, 0, "", "0", 0, 0, 0, ""])
    for nm, h, q in its:
        rows.append(["OF", "", nm, h, q, h * q, 0, h * q, h * q * 11 // 100, 0, 0])
tulis("V7-efaktur-fk-of.csv", rows)
K["V7"] = {"faktur": 3, "dpp": tdpp, "ppn": tppn, "harapan": "GAGAL jelas / peringatan; menjumlah kolom tercampur FK+OF diam-diam = c"}

# V8 daftar faktur keluaran gaya Coretax (datar)
cx = [("0012345678901000", "PT Maju Jaya", "04", "04002600000101", "2026-09-02", "APPROVED", 10000000),
      ("0023456789012000", "CV Sentosa", "04", "04002600000102", "2026-09-05", "APPROVED", 2500000),
      ("0034567890123000", "UD Berkah", "04", "04002600000103", "2026-09-11", "APPROVED", 7200000),
      ("0045678901234000", "Toko Sinar", "04", "04002600000104", "2026-09-18", "APPROVED", 1200000),
      ("0056789012345000", "PT Cahaya", "04", "04002600000105", "2026-09-25", "CANCELED", 3000000)]
rows = [["NPWP Pembeli", "Nama Pembeli", "Kode Transaksi", "Nomor Faktur Pajak", "Tanggal Faktur Pajak", "Masa Pajak", "Tahun",
         "Status Faktur", "Harga Jual/Penggantian/DPP", "DPP Nilai Lain", "PPN", "PPnBM"]]
sd = sdl = sp = 0; sp_ok = 0
for npwp, nm, kt, no, tg, st, dpp in cx:
    dl = (D(dpp) * 11 / 12).quantize(D(1)); ppn = int(D(dl) * 12 / 100)  # dibulatkan ke bawah
    rows.append([npwp, nm, kt, no, tg, "9", "2026", st, dpp, int(dl), ppn, 0]); sd += dpp; sdl += int(dl); sp += ppn
    if st == "APPROVED": sp_ok += ppn
tulis("V8-coretax-faktur-keluaran.csv", rows)
K["V8"] = {"baris": 5, "dpp": sd, "dpp_nilai_lain": sdl, "ppn": sp, "ppn_approved": sp_ok, "harapan": "NPWP & nomor faktur = kode (tidak dijumlah)"}

# V9 ekspor GoBiz-gaya: waktu ISO+zona, "Rp45.000", komisi negatif "-Rp9.000"
gb = [("2026-09-01T11:23:45+07:00", "F-2451837363", 45000, 0), ("2026-09-01T12:05:10+07:00", "F-2451840012", 78000, 0),
      ("2026-09-02T09:41:02+07:00", "F-2451902231", 32000, 0), ("2026-09-02T19:15:33+07:00", "F-2451955870", 120000, 10000),
      ("2026-09-03T13:02:19+07:00", "F-2452011104", 56000, 0), ("2026-09-03T20:48:51+07:00", "F-2452063390", 64000, 0)]
rows = [["Waktu Transaksi", "ID Pesanan", "Tipe Layanan", "Metode Pembayaran", "Harga Kotor", "Diskon Merchant", "Komisi", "Pendapatan Bersih", "Status"]]
sg = sk = sb = sdk = 0
for w, i, g, d in gb:
    k = g * 20 // 100; b = g - d - k
    rows.append([w, i, "GoFood", "GoPay", f"Rp{idr(g)}", f"-Rp{idr(d)}" if d else "Rp0", f"-Rp{idr(k)}", f"Rp{idr(b)}", "Selesai"])
    sg += g; sk += k; sb += b; sdk += d
tulis("V9-gobiz-transaksi.csv", rows)
K["V9"] = {"baris": 6, "kotor": sg, "komisi": -sk, "diskon": -sdk, "bersih": sb}

# V10 ekspor GrabMerchant-gaya: angka gaya Inggris "52,000.00"
gr = [("01 Sep 2026 11:23", "A-6X2K9P1", 52000), ("01 Sep 2026 18:40", "A-6X2M3Q7", 37500), ("02 Sep 2026 12:10", "A-6X3A8R2", 88000),
      ("03 Sep 2026 10:05", "A-6X4C1T5", 41000), ("03 Sep 2026 19:55", "A-6X4F7W9", 69500)]
rows = [["Date", "Booking ID", "Category", "Gross Sales (IDR)", "Commission (IDR)", "Net Sales (IDR)"]]
g2 = c2 = n2 = 0
for t, i, g in gr:
    c = g * 20 // 100; n = g - c; g2 += g; c2 += c; n2 += n
    rows.append([t, i, "GrabFood", f"{g:,.2f}", f"{c:,.2f}", f"{n:,.2f}"])
tulis("V10-grabmerchant-angka-inggris.csv", rows)
K["V10"] = {"baris": 5, "gross": g2, "komisi": c2, "net": n2, "harapan": "52,000.00 dibaca 52 diam-diam = c; tidak valid/tanya = b"}

# V11 CSV Eropa: ; + koma desimal + titik ribuan
eu = [("2026-09-02", "Schrauben M6", "2,5", "12,40"), ("2026-09-03", "Dübel 8mm", "10", "3,05"), ("2026-09-04", "Kabel 3x1,5", "0,75", "120,00"),
      ("2026-09-07", "Kabelbinder", "1.200", "0,85"), ("2026-09-08", "Bohrmaschine", "3", "1.049,99")]
def eud(s): return D(s.replace(".", "").replace(",", "."))
rows = [["Datum", "Artikel", "Menge", "Einzelpreis", "Betrag"]]; sm = sb2 = D(0)
for t, a, m, p in eu:
    b = (eud(m) * eud(p)).quantize(D("0.01")); sm += eud(m); sb2 += b
    rows.append([t, a, m, p, f"{b:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")])
tulis("V11-eropa-koma-desimal.csv", rows, ";")
K["V11"] = {"baris": 5, "menge": str(sm), "betrag": str(sb2)}

# V12 bulan melebar Jan..Des + kolom Total + baris TOTAL (nilai)
bl = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
pr = {"Beras 5kg": 1000000, "Minyak 2L": 600000, "Gula 1kg": 350000, "Telur 1kg": 450000}
rows = [["Produk"] + bl + ["Total"]]; cs = [0] * 12
for i, (p, base) in enumerate(pr.items()):
    v = [base + ((m * 37 + i * 11) % 9) * 25000 for m in range(12)]
    rows.append([p] + v + [sum(v)]); cs = [a + b for a, b in zip(cs, v)]
rows.append(["TOTAL"] + cs + [sum(cs)])
xlsx("V12-bulan-melebar.xlsx", rows)
K["V12"] = {"baris": 4, "per_bulan": dict(zip(bl, cs)), "total": sum(cs), "bulan_tertinggi": bl[cs.index(max(cs))]}

# V13 tabel tanpa judul kolom
nh = [("2026-09-01", "Bu Ani", "Kue Lapis", 2, 150000), ("2026-09-02", "Pak Dedi", "Bolu Pandan", 1, 85000),
      ("2026-09-02", "Bu Rina", "Kue Lapis", 3, 225000), ("2026-09-04", "Bu Ani", "Brownies", 2, 140000),
      ("2026-09-05", "Pak Dedi", "Kue Lapis", 1, 75000), ("2026-09-06", "Bu Sari", "Bolu Pandan", 4, 340000)]
tulis("V13-tanpa-header.csv", [list(x) for x in nh])
K["V13"] = {"baris": 6, "total": sum(x[4] for x in nh), "harapan": "baris 1 dipakai jadi judul kolom diam-diam (hilang 150.000) = c"}

# K1–K3 kontrol rapi
kb = [("2026-09-%02d" % (i + 1), ["Listrik", "Transport", "ATK", "Konsumsi"][i % 4], f"Biaya {i+1}", 50000 + i * 12500) for i in range(15)]
tulis("K1-kontrol-biaya.csv", [["Tanggal", "Kategori", "Keterangan", "Nominal"]] + [list(x) for x in kb])
K["K1"] = {"baris": 15, "total": sum(x[3] for x in kb), "per_kategori": {c: sum(x[3] for x in kb if x[1] == c) for c in ["Listrik", "Transport", "ATK", "Konsumsi"]}}
ks = [(f"BRG-{i:03d}", f"Barang {i}", 5 + i * 3, 10000 + i * 2500) for i in range(1, 11)]
xlsx("K2-kontrol-stok.xlsx", [["Kode", "Nama", "Stok", "Harga"]] + [list(x) for x in ks])
K["K2"] = {"baris": 10, "stok": sum(x[2] for x in ks), "harga": sum(x[3] for x in ks)}
kn = [("Ayu", "7A", "85,5"), ("Bima", "7A", "78"), ("Citra", "7B", "92,25"), ("Dodi", "7B", "66,75"), ("Eka", "7A", "88")]
tulis("K3-kontrol-nilai-siswa.csv", [["Nama", "Kelas", "Nilai"]] + [list(x) for x in kn], ";")
sn = sum(eud(x[2]) for x in kn)
K["K3"] = {"baris": 5, "jumlah": str(sn), "rata": str(sn / 5), "rata_7A": str(sum(eud(x[2]) for x in kn if x[1] == "7A") / 3)}

(O / "kunci-v107.json").write_text(json.dumps(K, ensure_ascii=False, indent=1), encoding="utf-8")
print("OK", O)
