#!/usr/bin/env python3
"""Fixture uji ulang v1.0.1 (penguji independen ke-2) untuk skill analisis-excel.

Python standar saja, deterministik. Menghasilkan di folder tujuan (default ./fixture-ulang):
  A. "Koperasi Maju Bersama 2026.xlsx" - 6 sheet: Ringkasan (struktur beda, sheet PERTAMA),
     TW1..TW4 (transaksi per triwulan; TW3 urutan kolom beda + kolom tambahan + judul huruf kecil;
     TW4 tanpa kolom Keterangan + tanggal teks), "Arsip 2025" tersembunyi (struktur sama).
     Baris penutup tiap TW: "Jumlah", "Total", "Subtotal", "TOTAL TW4". String inline (bukan sharedStrings).
  B. "pesanan-marketplace-sep.csv" - UTF-8, koma, alamat multi-baris dalam kutip, emoji di produk,
     variasi kota "Jakarta Selatan"/"JAKARTA SELATAN"/"Jakarta  Selatan"/"JakartaSelatan".
  C. "anggota-koperasi.csv" - pemisah ;, angka format Indonesia, NIK/HP/email/rekening,
     golongan "Gol A"/"GolA"/"gol a", 2 baris duplikat persis, 1 simpanan kosong.
  D. file rusak baru.
  kunci-ulang.json - kunci jawaban dihitung dari data sumber (tanpa script skill).
"""
import json
import random
import sys
import zipfile
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "fixture-ulang")
OUT.mkdir(parents=True, exist_ok=True)
rnd = random.Random(7250926)
NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NSR = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def col(i):
    s, i = "", i + 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


def ser(d):
    return (d - date(1899, 12, 30)).days


def xlsx(path, sheets):
    """sheets: [{nama, hidden, baris}] ; sel: None|str|("n",v)|("d",date)"""
    xs = []
    for sh in sheets:
        rows = []
        for ri, row in enumerate(sh["baris"], 1):
            cs = []
            for ci, v in enumerate(row):
                ref = "%s%d" % (col(ci), ri)
                if v is None:
                    continue
                if isinstance(v, str):
                    cs.append('<c r="%s" t="inlineStr"><is><t xml:space="preserve">%s</t></is></c>' % (ref, escape(v)))
                elif v[0] == "n":
                    cs.append('<c r="%s" s="2"><v>%s</v></c>' % (ref, v[1]))
                elif v[0] == "d":
                    cs.append('<c r="%s" s="1"><v>%d</v></c>' % (ref, ser(v[1])))
            rows.append('<row r="%d">%s</row>' % (ri, "".join(cs)))
        xs.append('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<worksheet xmlns="%s" xmlns:r="%s"><sheetData>%s</sheetData></worksheet>' % (NS, NSR, "".join(rows)))
    styles = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<styleSheet xmlns="%s"><fonts count="1"><font><sz val="11"/><name val="Calibri"/></font></fonts>'
              '<fills count="1"><fill><patternFill patternType="none"/></fill></fills><borders count="1"><border/></borders>'
              '<cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>'
              '<cellXfs count="3"><xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>'
              '<xf numFmtId="14" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/>'
              '<xf numFmtId="3" fontId="0" fillId="0" borderId="0" xfId="0" applyNumberFormat="1"/></cellXfs></styleSheet>' % NS)
    wbs = "".join('<sheet name="%s" sheetId="%d"%s r:id="rId%d"/>' % (escape(s["nama"]), i + 1, ' state="hidden"' if s.get("hidden") else "", i + 1) for i, s in enumerate(sheets))
    wb = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<workbook xmlns="%s" xmlns:r="%s"><sheets>%s</sheets></workbook>' % (NS, NSR, wbs)
    n = len(sheets)
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


def rp(v):
    return "Rp " + "{:,}".format(v).replace(",", ".")


kunci = {}

# ------------------------------------------------------------------ A. Koperasi 4 triwulan
AKUN = {"Pendapatan": [("Jasa Pinjaman", 800000, 4500000), ("Provisi", 100000, 600000), ("Penjualan Toko", 1500000, 9000000)],
        "Beban": [("Gaji Pengurus", 3000000, 3000000), ("Listrik & Air", 350000, 900000), ("ATK", 50000, 400000), ("Rapat Anggota", 500000, 5000000)]}
trx = []
for bln in range(1, 13):
    last = (date(2026, bln + 1, 1) - timedelta(days=1)).day if bln < 12 else 31
    for jenis, akuns in AKUN.items():
        for akun, lo, hi in akuns:
            k = rnd.choice([1, 2, 2, 3]) if akun != "Gaji Pengurus" else 1
            for _ in range(k):
                v = 3000000 if akun == "Gaji Pengurus" else rnd.randrange(lo, hi + 1, 5000)
                trx.append(dict(tgl=date(2026, bln, rnd.randint(1, last)), akun=akun, jenis=jenis, ket="%s %s" % (akun, bln), v=v))
trx.sort(key=lambda t: (t["tgl"], t["akun"]))
tw = lambda t: (t["tgl"].month - 1) // 3 + 1
# TW2: 3 nilai sebagai teks "Rp x.xxx.xxx"; 1 baris duplikat persis
tw2 = [t for t in trx if tw(t) == 2]
for t in rnd.sample(tw2, 3):
    t["teks"] = True
dup = dict(tw2[5])
dup["dup"] = True
trx.append(dup)
trx.sort(key=lambda t: (t["tgl"], t["akun"], t.get("dup", False)))

PENUTUP = {1: "Jumlah", 2: "Total", 3: "Subtotal", 4: "TOTAL TW4"}
sheets = []
# Ringkasan: struktur beda, sheet pertama (jebakan default sheet)
rk = [["RINGKASAN SHU 2026"], ["Triwulan", "Pendapatan", "Beban", "SHU"]]
for q in range(1, 5):
    p = sum(t["v"] for t in trx if tw(t) == q and t["jenis"] == "Pendapatan")
    b = sum(t["v"] for t in trx if tw(t) == q and t["jenis"] == "Beban")
    rk.append(["TW%d" % q, ("n", p), ("n", b), ("n", p - b)])
sheets.append({"nama": "Ringkasan", "baris": rk})
for q in range(1, 5):
    rows = [t for t in trx if tw(t) == q]
    if q == 3:
        hdr = ["akun", "tanggal", "JUMLAH", "jenis", "keterangan", "Catatan Pengurus"]
        body = [[t["akun"], ("d", t["tgl"]), ("n", t["v"]), t["jenis"], t["ket"], "ok" if i % 5 == 0 else None] for i, t in enumerate(rows)]
        tot = [PENUTUP[q], None, ("n", sum(t["v"] for t in rows))]
    elif q == 4:
        hdr = ["Tanggal", "Akun", "Jenis", "Jumlah"]  # tanpa Keterangan; tanggal teks dd/mm/yyyy
        body = [[t["tgl"].strftime("%d/%m/%Y"), t["akun"], t["jenis"], ("n", t["v"])] for t in rows]
        tot = [PENUTUP[q], None, None, ("n", sum(t["v"] for t in rows))]
    else:
        hdr = ["Tanggal", "Akun", "Jenis", "Keterangan", "Jumlah"]
        body = [[("d", t["tgl"]), t["akun"], t["jenis"], t["ket"], rp(t["v"]) if t.get("teks") else ("n", t["v"])] for t in rows]
        tot = [PENUTUP[q], None, None, None, ("n", sum(t["v"] for t in rows))]
    sheets.append({"nama": "TW%d" % q, "baris": [["KOPERASI MAJU BERSAMA - BUKU KAS TW%d 2026" % q], hdr] + body + [tot]})
sheets.append({"nama": "Arsip 2025", "hidden": True,
               "baris": [["Tanggal", "Akun", "Jenis", "Keterangan", "Jumlah"], [("d", date(2025, 12, 1)), "ATK", "Beban", "x", ("n", 999999)]]})
xlsx(OUT / "Koperasi Maju Bersama 2026.xlsx", sheets)


def agg(rows, key):
    d = defaultdict(int)
    for t in rows:
        d[key(t)] += t["v"]
    return dict(sorted(d.items(), key=lambda x: -x[1]))


kA = {"baris_per_tw": {q: sum(1 for t in trx if tw(t) == q) for q in range(1, 5)},
      "jumlah_per_tw": {q: sum(t["v"] for t in trx if tw(t) == q) for q in range(1, 5)},
      "jumlah_semua": sum(t["v"] for t in trx),
      "per_jenis": agg(trx, lambda t: t["jenis"]),
      "per_jenis_tw123": agg([t for t in trx if tw(t) < 4], lambda t: t["jenis"]),
      "per_akun": agg(trx, lambda t: t["akun"]),
      "per_bulan": dict(sorted(agg(trx, lambda t: "%02d" % t["tgl"].month).items())),
      "top3_beban_akun": list(agg([t for t in trx if t["jenis"] == "Beban"], lambda t: t["akun"]).items())[:3],
      "pendapatan_tw2": sum(t["v"] for t in trx if tw(t) == 2 and t["jenis"] == "Pendapatan"),
      "pendapatan_tw3": sum(t["v"] for t in trx if tw(t) == 3 and t["jenis"] == "Pendapatan"),
      "duplikat_tw2": 1, "teks_rp_tw2": 3}
kunci["A"] = kA

# ------------------------------------------------------------------ B. marketplace multi-baris + emoji
PROD = [("Kaos Polos 👕 Hitam", 45000), ("Hijab Voal 🌸 Motif", 65000), ("Tumbler 500ml ☕", 89000), ("Sandal Jepit 🩴", 25000), ("Masker Kain 😷 isi 3", 15000)]
KOTA = {"Jakarta Selatan": ["JAKARTA SELATAN", "Jakarta  Selatan", "JakartaSelatan"], "Bandung": ["bandung"], "Surabaya": [], "Medan": [], "Kab. Bogor": []}
B = []
for i in range(1, 61):
    tgl = date(2026, 9, rnd.randint(1, 30))
    nama, h = rnd.choice(PROD)
    q = rnd.choice([1, 1, 2, 3, 5])
    kota = rnd.choice(list(KOTA))
    tk = rnd.choice(KOTA[kota]) if KOTA[kota] and rnd.random() < 0.35 else kota
    alamat = "Jl. Melati No. %d, RT 0%d/RW 0%d" % (i, rnd.randint(1, 9), rnd.randint(1, 9))
    if i % 4 == 0:
        alamat += "\nKel. Sukamaju, Kec. %s\n(patokan: \"warung biru\", samping masjid)" % kota  # multi-baris, kutip ganda, koma
    B.append(dict(no="MP-%04d" % i, tgl=tgl, nama="Pembeli %d" % i, alamat=alamat, prod=nama, q=q, h=h, tot=q * h, kota=kota, tk=tk))
import csv
with open(OUT / "pesanan-marketplace-sep.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["No Pesanan", "Tanggal Pesan", "Nama Pembeli", "Alamat Kirim", "Produk", "Qty", "Harga", "Total Bayar", "Kota"])
    for b in B:
        w.writerow([b["no"], b["tgl"].strftime("%d-%m-%Y"), b["nama"], b["alamat"], b["prod"], b["q"], b["h"], b["tot"], b["tk"]])
kunci["B"] = {"baris": len(B), "multibaris": sum(1 for b in B if "\n" in b["alamat"]),
              "total": sum(b["tot"] for b in B), "per_kota": agg([dict(v=b["tot"], k=b["kota"]) for b in B], lambda t: t["k"]),
              "baris_per_kota": {k: sum(1 for b in B if b["kota"] == k) for k in KOTA},
              "per_produk": agg([dict(v=b["tot"], k=b["prod"]) for b in B], lambda t: t["k"]),
              "qty_per_produk": {p: sum(b["q"] for b in B if b["prod"] == p) for p, _ in PROD},
              "per_minggu_iso": dict(sorted(agg([dict(v=b["tot"], k=b["tgl"].isocalendar()[1]) for b in B], lambda t: t["k"]).items())),
              "sep1_15": sum(b["tot"] for b in B if b["tgl"].day <= 15), "sep16_30": sum(b["tot"] for b in B if b["tgl"].day > 15)}

# ------------------------------------------------------------------ C. anggota NIK/HP
GOL = {"Gol A": ["GolA", "gol a", "GOL  A"], "Gol B": ["GolB"], "Gol C": []}
C = []
for i in range(1, 41):
    g = rnd.choice(list(GOL))
    tg = rnd.choice(GOL[g]) if GOL[g] and rnd.random() < 0.3 else g
    nik = "3201%02d%06d%04d" % (rnd.randint(1, 40), rnd.randint(100000, 999999), rnd.randint(1, 9999))
    hp = "0812%08d" % rnd.randint(0, 99999999)
    pokok = 100000
    wajib = rnd.randrange(600000, 2400001, 50000)
    C.append(dict(no=i, nama="Anggota %02d" % i, nik=nik, hp=hp, email="anggota%02d@contoh.id" % i, rek="1234%06d" % rnd.randint(0, 999999),
                  g=g, tg=tg, pokok=pokok, wajib=wajib, tgl=date(2020 + i % 6, 1 + i % 12, 1 + i % 28)))
C[7]["wajib"] = None  # 1 kosong
rows_c = C + [dict(C[3]), dict(C[11])]  # 2 duplikat persis
with open(OUT / "anggota-koperasi.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["No", "Nama", "NIK", "No HP", "Email", "No Rekening", "Golongan", "Simpanan Pokok", "Simpanan Wajib", "Tanggal Gabung"])
    for c in rows_c:
        w.writerow([c["no"], c["nama"], c["nik"], c["hp"], c["email"], c["rek"], c["tg"],
                    "{:,}".format(c["pokok"]).replace(",", "."), "" if c["wajib"] is None else "{:,}".format(c["wajib"]).replace(",", "."),
                    c["tgl"].strftime("%d/%m/%Y")])
kunci["C"] = {"baris_termasuk_dup": len(rows_c), "wajib_total_dengan_dup": sum(c["wajib"] or 0 for c in rows_c),
              "wajib_total_tanpa_dup": sum(c["wajib"] or 0 for c in C),
              "per_gol_dengan_dup": agg([dict(v=c["wajib"] or 0, k=c["g"]) for c in rows_c], lambda t: t["k"]),
              "baris_per_gol_dengan_dup": {g: sum(1 for c in rows_c if c["g"] == g) for g in GOL},
              "top3_wajib": sorted([(c["nama"], c["nik"], c["wajib"]) for c in C if c["wajib"]], key=lambda x: -x[2])[:3]}

# ------------------------------------------------------------------ D. data rusak baru
lines = ["Nama,Nominal"] + ["Orang %d,%d" % (i, 1000 * i) for i in range(1, 11)]
lines.insert(6, '"Rusak di tengah,5000')  # baris 7 file
(OUT / "kutip-tengah.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")
(OUT / "kutip-tertutup-jauh.csv").write_text('Nama,Nominal\nA,1000\n"B,2000\nC,3000\nD",4000\nE,5000\n', encoding="utf-8")
(OUT / "kutip-di-akhir.csv").write_text('Nama,Nominal\nA,1000\nB,2000\n"C,3000\n', encoding="utf-8")
(OUT / "alamat-sah.csv").write_text('Nama,Alamat,Nominal\nA,"Jl. X\nRT 1",1000\nB,"Jl. Y, No. 2\nKel. Z, Kec. W",2000\nC,Jl. Z,3000\n', encoding="utf-8")
xlsx(OUT / "semua-beda.xlsx", [{"nama": "Satu", "baris": [["Nama", "Nilai"], ["a", ("n", 1)]]},
                                 {"nama": "Dua", "baris": [["Kota", "Stok", "Harga"], ["b", ("n", 2), ("n", 3)]]},
                                 {"nama": "Kosong", "baris": []},
                                 {"nama": "Judul Saja", "baris": [["Nama", "Nilai"]]},
                                 {"nama": "Jan, Feb", "baris": [["Nama", "Nilai"], ["c", ("n", 5)], ["d", ("n", 7)]]}])
(OUT / "kunci-ulang.json").write_text(json.dumps(kunci, indent=1, ensure_ascii=False, default=str), encoding="utf-8")
print("OK", OUT)
