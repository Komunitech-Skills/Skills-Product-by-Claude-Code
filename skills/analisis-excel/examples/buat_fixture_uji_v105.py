#!/usr/bin/env python3
"""Fixture uji ulang v1.0.5 (penguji independen ke-6). Python standar, deterministik.
Fokus: risiko BARU v1.0.5 - baris data ASLI ikut terbuang karena dikira baris ringkasan (Total/Rata-rata/SUM tanpa
label) atau catatan kaki. Data asli yang KEBETULAN sama dengan jumlah/rata-rata baris di atasnya, nama produk/kategori
berisi kata Total/Jumlah/Rata-rata/Saldo, catatan kaki berangka, subtotal per kelompok, plus ekspor realistis.
kunci-v105.json = kunci independen (dihitung dari data sumber di script ini, TANPA membaca kode skill).
Pakai: python3 buat_fixture_uji_v105.py [folder]"""
import csv, io, json, sys, zipfile
from datetime import date, timedelta
from pathlib import Path
from xml.sax.saxutils import escape

O = Path(sys.argv[1] if len(sys.argv) > 1 else "fixture-v105"); O.mkdir(parents=True, exist_ok=True)
K = {}


def csvtext(rows, delim=",", term="\r\n"):
    b = io.StringIO(); w = csv.writer(b, delimiter=delim, lineterminator=term); w.writerows(rows); return b.getvalue()


def simpan(nama, rows, delim=",", enc="utf-8"):
    (O / nama).write_bytes(csvtext(rows, delim).encode(enc))


def col(i):
    s = ""; i += 1
    while i: i, r = divmod(i - 1, 26); s = chr(65 + r) + s
    return s


NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NSR = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def xlsx(path, sheets):
    """sheets: [(nama, rows)]; sel: None | str | int/float | date | ("f", rumus, nilai_tersimpan)"""
    xs = []
    for _, rws in sheets:
        out = []
        for ri, row in enumerate(rws, 1):
            cs = []
            for ci, v in enumerate(row):
                ref = "%s%d" % (col(ci), ri)
                if v is None or v == "":
                    continue
                if isinstance(v, str):
                    cs.append('<c r="%s" t="inlineStr"><is><t xml:space="preserve">%s</t></is></c>' % (ref, escape(v)))
                elif isinstance(v, tuple):
                    cs.append('<c r="%s" s="2"><f>%s</f><v>%s</v></c>' % (ref, escape(v[1]), v[2]))
                elif isinstance(v, date):
                    cs.append('<c r="%s" s="1"><v>%d</v></c>' % (ref, (v - date(1899, 12, 30)).days))
                else:
                    cs.append('<c r="%s" s="2"><v>%s</v></c>' % (ref, v))
            out.append('<row r="%d">%s</row>' % (ri, "".join(cs)))
        xs.append('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<worksheet xmlns="%s" xmlns:r="%s"><sheetData>%s</sheetData></worksheet>' % (NS, NSR, "".join(out)))
    styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<styleSheet xmlns="%s"><fonts count="1"><font><sz val="11"/><name val="Calibri"/></font></fonts>'
              '<fills count="1"><fill><patternFill patternType="none"/></fill></fills><borders count="1"><border/></borders>'
              '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
              '<cellXfs count="3"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>'
              '<xf numFmtId="14" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/>'
              '<xf numFmtId="3" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/></cellXfs></styleSheet>' % NS)
    n = len(sheets)
    wbs = "".join('<sheet name="%s" sheetId="%d" r:id="rId%d"/>' % (escape(s[0]), i + 1, i + 1) for i, s in enumerate(sheets))
    wb = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<workbook xmlns="%s" xmlns:r="%s"><sheets>%s</sheets></workbook>' % (NS, NSR, wbs)
    rels = "".join('<Relationship Id="rId%d" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet%d.xml"/>' % (i + 1, i + 1) for i in range(n))
    rels += '<Relationship Id="rId%d" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>' % (n + 1)
    ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'
          '<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>'
          + "".join('<Override PartName="/xl/worksheets/sheet%d.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' % (i + 1) for i in range(n))
          + '<Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/></Types>')
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("_rels/.rels", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>')
        z.writestr("xl/workbook.xml", wb)
        z.writestr("xl/_rels/workbook.xml.rels", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">%s</Relationships>' % rels)
        z.writestr("xl/styles.xml", styles)
        for i, x in enumerate(xs):
            z.writestr("xl/worksheets/sheet%d.xml" % (i + 1), x)


D0 = date(2026, 9, 1)

# R1 tabel bernomor, semua kolom angka (No, Qty, Harga, Total). Baris ke-3 = baris 1 + baris 2 di SEMUA kolom
#    (No 3 = 1+2, Qty 3 = 1+2, ...), baris 2 = baris 1 di Qty/Harga/Total. Semua 10 baris DATA ASLI.
qty = [2, 2, 4, 1, 3, 5, 2, 6, 1, 3]; hrg = [25000] * 10
rows = [["No", "Qty", "Harga", "Total"]] + [[i + 1, q, h, q * h] for i, (q, h) in enumerate(zip(qty, hrg))]
simpan("R1-bernomor-baris3-jumlah.csv", rows)
K["R1"] = {"baris": 10, "total": sum(q * h for q, h in zip(qty, hrg)), "qty": sum(qty), "harapan": "10 baris; tidak ada yang dibuang"}

# R2 daftar satu kolom (tempel nominal dari WA), nilai berlipat ganda: 25rb, 25rb (=baris1), 50rb (=1+2), 100rb (=jumlah di atas)
vals = [25000, 25000, 50000, 100000, 35000, 40000, 75000, 20000]
simpan("R2-satu-kolom-nominal.csv", [["Nominal"]] + [[v] for v in vals])
K["R2"] = {"baris": 8, "total": sum(vals), "harapan": "8 baris, total 370.000; baris 2-4 kebetulan = jumlah/rata-rata di atasnya tapi DATA"}

# R3 buku kas: tanggal & keterangan hanya ditulis di transaksi pertama tiap hari (gaya sel gabungan di CSV).
#    Transaksi ke-2 hari pertama bernilai sama (baris 3 = baris 2 = jumlah di atasnya).
kas = [(D0, "Beli galon", 20000), (None, None, 20000), (D0 + timedelta(1), "Bensin motor", 30000), (None, None, 70000),
       (D0 + timedelta(2), "Parkir", 5000), (None, "Fotokopi", 8000), (D0 + timedelta(3), "Snack rapat", 45000), (None, None, 198000)]
rows = [["Tanggal", "Keterangan", "Keluar"]] + [[d.isoformat() if d else "", k or "", v] for d, k, v in kas]
simpan("R3-kas-tanggal-sekali.csv", rows)
K["R3"] = {"baris": 8, "total": sum(v for *_, v in kas),
           "catatan": "baris 3 (20000) = jumlah di atas & rata-rata; baris 5 (70000) = jumlah di atas (20000+20000+30000); baris 9 (198000) = jumlah di atas. Semua DATA ASLI (label kosong krn gaya gabung sel)",
           "harapan": "8 baris 396.000 ATAU minimal setiap baris dibuang disebut dg isinya (b)"}

# R4 kolom Masuk/Keluar dengan banyak 0, sel label kosong pada beberapa baris
mk = [("2026-09-01", "Setoran awal kas", 500000, 0), ("2026-09-02", "Beli ATK", 0, 45000), ("", "", 0, 45000),
      ("2026-09-03", "Jual kardus bekas", 20000, 0), ("", "", 0, 0), ("2026-09-04", "Bayar listrik", 0, 250000),
      ("", "", 0, 340000), ("2026-09-05", "Terima iuran", 75000, 0)]
rows = [["Tanggal", "Uraian", "Masuk", "Keluar"]] + [list(x) for x in mk]
simpan("R4-masuk-keluar-banyak-nol.csv", rows)
K["R4"] = {"baris": 8, "masuk": sum(x[2] for x in mk), "keluar": sum(x[3] for x in mk),
           "catatan": "baris 4 (0|45000) = baris 3; baris 8 (0|340000) = jumlah Keluar di atas (45+45+250rb) tapi Masuk 0 != 520000; baris 6 (0|0) baris nol",
           "harapan": "Masuk 595.000, Keluar 680.000"}

# R5 nama produk / keterangan berisi kata ringkasan
prod = [("Paket Total Care", 150000), ("Jumlah Besar Sabun Cuci 5L", 85000), ("Setoran Saldo Awal Bulan", 500000),
        ("Grand Total Kids Toy", 99000), ("Subtotal Snack Box", 45000), ("Rata-rata Air Mineral (dus campur)", 38000),
        ("TOTAL", 60000), ("Jumlah", 12000), ("Kopi Susu", 18000), ("Teh Tarik", 15000)]
rows = [["Tanggal", "Nama Produk", "Harga"]] + [[(D0 + timedelta(i)).isoformat(), p, v] for i, (p, v) in enumerate(prod)]
simpan("R5-produk-bernama-total.csv", rows)
K["R5"] = {"baris": 10, "total": sum(v for _, v in prod),
           "catatan": "baris 8 nama produk 'TOTAL' (merek) & baris 9 'Jumlah' (ambigu); keduanya BERTANGGAL & tidak = jumlah di atas",
           "total_tanpa_baris_TOTAL_Jumlah": sum(v for p, v in prod if p not in ("TOTAL", "Jumlah")),
           "harapan": "idealnya 10 baris 1.022.000; baris ber-tanggal berlabel persis TOTAL boleh dibuang HANYA dengan peringatan berisi isinya"}

# R6 kategori penilaian kinerja HR: "Rata-rata", "Di atas rata-rata", "Di bawah rata-rata"; kolom Bonus
hr = [("Pegawai 01", "Di atas rata-rata", 1500000), ("Pegawai 02", "Rata-rata", 750000), ("Pegawai 03", "Rata-rata", 750000),
      ("Pegawai 04", "Di bawah rata-rata", 0), ("Pegawai 05", "Rata-rata", 750000), ("Pegawai 06", "Di atas rata-rata", 1500000),
      ("Pegawai 07", "Rata-rata", 750000), ("Pegawai 08", "Di bawah rata-rata", 0)]
rows = [["Nama", "Penilaian", "Bonus"]] + [list(x) for x in hr]
simpan("R6-kategori-rata-rata.csv", rows)
K["R6"] = {"baris": 8, "total": sum(x[2] for x in hr), "per_penilaian": {"Rata-rata": 3000000, "Di atas rata-rata": 3000000, "Di bawah rata-rata": 0},
           "harapan": "8 baris, 6.000.000; kategori 'Rata-rata' 4 baris 3.000.000"}

# R7 klaim asuransi kendaraan: kolom Jenis Kerusakan = Total / Sebagian (label di kolom tengah)
kl = [("KLM-001", "Sebagian", 3500000), ("KLM-002", "Total", 85000000), ("KLM-003", "Sebagian", 1200000), ("KLM-004", "Total", 120000000), ("KLM-005", "Sebagian", 800000)]
rows = [["No Klaim", "Jenis Kerusakan", "Nilai Klaim"]] + [list(x) for x in kl]
simpan("R7-kerusakan-total.csv", rows)
K["R7"] = {"baris": 5, "total": sum(x[2] for x in kl), "harapan": "5 baris, 210.500.000; 'Total' = kategori"}

# R8 catatan kaki berisi angka (di kolom nilai) + teks
it = [("2026-09-0%d" % (i + 1), "Pesanan %02d" % (i + 1), v) for i, v in enumerate([120000, 95000, 210000, 80000, 150000, 60000])]
rows = [["Tanggal", "Pesanan", "Nominal"]] + [list(x) for x in it] + [[], ["Catatan: 2 pesanan retur senilai", "", "150000"], ["Harga sudah termasuk PPN 11%"]]
simpan("R8-catatan-kaki-berangka.csv", rows)
K["R8"] = {"baris": 6, "total": sum(x[2] for x in it), "harapan": "6 baris 715.000; catatan berangka tidak masuk data (atau disebut tegas)"}

# R9 subtotal per cabang BERLABEL, cabang B hanya 1 baris (subtotal B = baris B)
grp = {"Cabang A": [300000, 250000, 450000], "Cabang B": [400000], "Cabang C": [150000, 150000]}
rows = [["Cabang", "Tanggal", "Omzet"]]
for g, vs in grp.items():
    for i, v in enumerate(vs): rows.append([g, "2026-09-%02d" % (i + 1), v])
    rows.append(["Subtotal " + g, "", sum(vs)])
rows.append(["Grand Total", "", sum(sum(v) for v in grp.values())])
simpan("R9-subtotal-berlabel-kelompok-1-baris.csv", rows)
K["R9"] = {"baris": 6, "total": 1700000, "per_cabang": {g: sum(v) for g, v in grp.items()}, "harapan": "6 baris 1.700.000"}

# R10 subtotal per kelompok TANPA label (baris rumus SUM kosong labelnya), kelompok B 1 baris
rows = [["Cabang", "Tanggal", "Omzet"]]
for g, vs in grp.items():
    for i, v in enumerate(vs): rows.append([g, "2026-09-%02d" % (i + 1), v])
    rows.append(["", "", sum(vs)])
simpan("R10-subtotal-tanpa-label.csv", rows)
K["R10"] = {"baris": 6, "total": 1700000, "harapan": "6 baris 1.700.000 (3 baris subtotal tanpa label dibuang+disebut) atau peringatan tegas; ikut dijumlah diam-diam = c"}

# R11 XLSX buku kas + SUM (rumus, nilai tersimpan) tanpa label + AVERAGE tanpa label; baris data kedua = baris pertama tanpa label
kx = [(date(2026, 9, 1), "Gaji kurir", 1500000), (None, None, 1500000), (date(2026, 9, 2), "Sewa gudang", 2000000),
      (date(2026, 9, 3), "Bensin", 350000), (None, None, 5350000)]
rws = [["Tanggal", "Keterangan", "Biaya"]] + [[d, k, v] for d, k, v in kx]
s = sum(v for *_, v in kx)
rws += [[None, None, ("f", "SUM(C2:C6)", s)], [None, None, ("f", "AVERAGE(C2:C6)", s / 5)]]
xlsx(O / "R11-kas-sum-average.xlsx", [("Kas", rws)])
K["R11"] = {"baris": 5, "total": s, "catatan": "baris 3 = baris 2 (tanpa label), baris 6 = jumlah di atas (tanpa label) - keduanya DATA; baris 7 SUM, baris 8 AVERAGE",
            "harapan": "5 baris 10.700.000"}

# R12 bulan sebagai ANGKA (1..12) + penjualan; Mar = Jan + Feb (Bulan 3 = 1+2 juga!)
pj = [4000000, 3500000, 7500000, 5000000, 6200000, 4800000, 5100000, 5900000, 6100000, 7000000, 6600000, 9000000]
rows = [["Tahun", "Bulan", "Penjualan"]] + [[2025, i + 1, v] for i, v in enumerate(pj)]
simpan("R12-bulan-angka.csv", rows)
K["R12"] = {"baris": 12, "total": sum(pj), "harapan": "12 baris 70.700.000"}

# R12b sama tanpa kolom Tahun (hanya Bulan & Penjualan) - semua sel angka
simpan("R12b-bulan-angka-tanpa-tahun.csv", [["Bulan", "Penjualan"]] + [[i + 1, v] for i, v in enumerate(pj)])
K["R12b"] = {"baris": 12, "total": sum(pj), "harapan": "12 baris 70.700.000"}

# R13 transaksi bernilai sama berulang, satu kolom label kosong di baris-baris tertentu (pembeli anonim)
tr = [("2026-09-01 08:00", "", 15000), ("2026-09-01 08:05", "", 15000), ("2026-09-01 08:09", "", 15000), ("2026-09-01 08:20", "Bu Ani", 45000)]
rows = [["Waktu", "Pembeli", "Bayar"]] + [list(x) for x in tr]
simpan("R13-waktu-pembeli-kosong.csv", rows)
K["R13"] = {"baris": 4, "total": 90000, "harapan": "4 baris 90.000 (baris 5 Bu Ani 45000 = jumlah di atas, BERLABEL)"}

# R14 XLSX: kolom Nama kosong (belum diisi) pada transaksi yang nilainya = rata-rata di atas
rws = [["Tanggal", "Nama", "Iuran"]]
iu = [(date(2026, 9, 1), "Warga 01", 50000), (date(2026, 9, 1), "Warga 02", 100000), (None, None, 75000), (date(2026, 9, 2), "Warga 04", 50000)]
rws += [[d, n, v] for d, n, v in iu]
xlsx(O / "R14-iuran-baris-belum-lengkap.xlsx", [("Iuran", rws)])
K["R14"] = {"baris": 4, "total": 275000, "catatan": "baris 4 (tanpa tanggal/nama) 75000 = rata-rata di atasnya tapi DATA (iuran belum dicatat namanya)",
            "harapan": "4 baris 275.000 ATAU baris 4 dibuang dg peringatan berisi isinya"}

# ---- Positif: pola ekspor nyata ----
# P1 Shopee-like: kolom lengkap, beberapa pesanan dengan Total Pembayaran sama dan satu = jumlah dua sebelumnya
hdr = ["No. Pesanan", "Status Pesanan", "Waktu Pesanan Dibuat", "Nama Produk", "Jumlah", "Harga Awal", "Total Pembayaran", "Kota/Kabupaten"]
ps = []
amts = [89000, 89000, 178000, 45000, 89000, 134000, 267000, 45000, 90000, 89000]
for i, a in enumerate(amts):
    ps.append(["2609%02dABCD%03d" % (i + 1, i), "Selesai", "2026-09-%02d 1%d:2%d" % (i + 1, i % 10, i % 6), "Paket Total Care %d" % (i % 3) if i % 4 == 0 else "Jumlah Besar Hemat", 1 + i % 3, a, a, "KOTA BANDUNG"])
simpan("P1-shopee-nilai-berulang.csv", [hdr] + ps)
K["P1"] = {"baris": 10, "total": sum(amts), "qty": sum(1 + i % 3 for i in range(10)), "harapan": "10 baris 1.115.000"}

# P2 Tokopedia-like dengan judul di atas, "Rp" dan baris ringkasan berlabel di bawah
tk = [("INV/20260901/MPL/0001", "Kaos Polos", "Rp150.000"), ("INV/20260902/MPL/0002", "Kaos Polos", "Rp150.000"), ("INV/20260903/MPL/0003", "Celana Chino", "Rp300.000"),
      ("INV/20260904/MPL/0004", "Topi", "Rp75.000"), ("INV/20260905/MPL/0005", "Kaos Polos", "Rp150.000")]
rows = [["Laporan Penjualan Toko Sejahtera"], ["Periode: 1-30 September 2026"], [], ["Invoice", "Produk", "Total Penjualan (IDR)"]] + [list(x) for x in tk]
rows += [[], ["Total Penjualan", "", "Rp825.000"], ["Rata-rata per pesanan", "", "Rp165.000"]]
simpan("P2-tokopedia-ringkasan-bawah.csv", rows)
K["P2"] = {"baris": 5, "total": 825000, "harapan": "5 baris 825.000; 2 baris ringkasan dibuang & disebut"}

# P3 mutasi BCA-like: saldo per baris, CR/DB, satu transaksi berketerangan 'SALDO' (TRSF ... SALDO AWAL ARISAN)
bca = [("01/09", "SETORAN TUNAI", "1.000.000,00", "CR", "11.000.000,00"), ("02/09", "TRSF E-BANKING DB SALDO AWAL ARISAN", "500.000,00", "DB", "10.500.000,00"),
       ("03/09", "BIAYA ADM", "10.000,00", "DB", "10.490.000,00"), ("04/09", "TRSF E-BANKING CR TOTAL BAYAR PESANAN", "10.000,00", "CR", "10.500.000,00")]
rows = [["Informasi Rekening - Mutasi Rekening"], ["No. rekening : 1234xxxx90"], ["Nama : TOKO CONTOH"], ["Periode : 01/09/2026 - 30/09/2026"], [],
        ["Tanggal Transaksi", "Keterangan", "Jumlah", "", "Saldo"]] + [list(x) for x in bca]
rows += [[], ["Saldo Awal :", "10.000.000,00"], ["Mutasi Kredit :", "1.010.000,00", "2"], ["Mutasi Debet :", "510.000,00", "2"], ["Saldo Akhir :", "10.500.000,00"]]
simpan("P3-bca-keterangan-saldo-total.csv", rows)
K["P3"] = {"baris": 4, "jumlah": 1520000, "CR": 1010000, "DB": 510000,
           "catatan": "baris 'BIAYA ADM' 10.000 dan baris CR 10.000 bernilai sama; keterangan berisi SALDO AWAL / TOTAL BAYAR = transaksi",
           "harapan": "4 baris, Jumlah 1.520.000"}

# P4 Google Form: timestamp, nama, nominal - satu responden bayar = jumlah dua sebelumnya
gf = [("01/09/2026 10:11:12", "Andi", 50000), ("01/09/2026 10:15:40", "Budi", 50000), ("01/09/2026 11:02:03", "Citra", 100000),
      ("02/09/2026 08:00:00", "Dedi", 200000), ("02/09/2026 09:30:00", "Eka", 100000)]
rows = [["Timestamp", "Nama Lengkap", "Nominal Donasi"]] + [list(x) for x in gf]
simpan("P4-google-form-donasi.csv", rows)
K["P4"] = {"baris": 5, "total": 500000, "harapan": "5 baris 500.000"}

# ---- Varian tambahan (ad hoc penguji) ----
rws = [["Tanggal", "Keterangan", "Biaya"], [date(2026, 9, 1), "Gaji kurir", 1500000], [date(2026, 9, 2), "Sewa gudang", 2000000], [date(2026, 9, 3), "Bensin", 350000],
       [None, None, ("f", "SUM(C2:C4)", 3850000)], [None, None, ("f", "AVERAGE(C2:C4)", 3850000 / 3)]]
xlsx(O / "R11b-sum-average-biasa.xlsx", [("Kas", rws)]); K["R11b"] = {"baris": 3, "total": 3850000}
simpan("R3c-kas-akhir-sama-jumlah.csv", [["Tanggal", "Keterangan", "Keluar"], ["2026-09-01", "Beli galon", 20000], ["2026-09-02", "Bensin", 30000],
                                          ["2026-09-03", "Parkir", 10000], ["", "", 60000]])
K["R3c"] = {"baris": 4, "total": 120000, "catatan": "baris 5 tanpa label (transaksi lanjutan hari 3) kebetulan = jumlah di atas; data"}
rws = [["Tanggal", "Barang", "Nilai"], [date(2026, 9, 1), "Semen", 650000], [date(2026, 9, 1), "Pasir", 400000], [None, None, 1050000], [date(2026, 9, 2), "Bata", 300000]]
xlsx(O / "R16-nilai-polos-sama-jumlah.xlsx", [("Sheet1", rws)])
K["R16"] = {"baris": 4, "total": 2400000, "catatan": "baris 4 nilai POLOS (bukan rumus) tanpa label = jumlah di atas; data"}
simpan("R8d-catatan-berangka-3-sel.csv", [["Tanggal", "Pesanan", "Nominal"]] + [list(x) for x in it] + [[], ["Catatan: 2 pesanan retur senilai", "", "150000"]])
K["R8d"] = {"baris": 6, "total": 715000, "harapan": "catatan berangka 3 sel di bawah tabel tidak dijumlah (atau disebut tegas)"}
simpan("R8c-catatan-1-sel-berangka.csv", [["Tanggal", "Pesanan", "Nominal"]] + [list(x) for x in it] + [[], ["Ongkir 15000 ditanggung penjual"], ["Harga sudah termasuk PPN 11%"]])
K["R8c"] = {"baris": 6, "total": 715000, "harapan": "2 catatan kaki 1 sel (berisi angka) diabaikan + info"}
simpan("R6b-penilaian-kolom-1.csv", [["Penilaian", "Nama", "Bonus"], ["Baik", "P1", 1000000], ["Rata-rata", "P2", 500000], ["Rata-rata", "P3", 500000], ["Baik", "P4", 1000000]])
K["R6b"] = {"baris": 4, "total": 3000000}

(O / "kunci-v105.json").write_text(json.dumps(K, indent=1, ensure_ascii=False), encoding="utf-8")
print("OK", O)
