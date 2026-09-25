#!/usr/bin/env python3
"""Fixture uji ulang v1.0.3 (penguji independen ke-4). Python standar, deterministik.
Fokus "angka salah diam-diam": kutip nyasar di berbagai posisi, CSV sah mirip rusak, XLSX dengan sheet rekap
bernama biasa, sheet 'Rekap' berisi data, sheet bulan kosong. kunci-v103.json = kunci independen (dari data sumber,
tanpa membaca kode skill). Pakai: python3 buat_fixture_uji_v103.py [folder]"""
import csv, io, json, random, sys, zipfile
from pathlib import Path
from xml.sax.saxutils import escape

O = Path(sys.argv[1] if len(sys.argv) > 1 else "fixture-v103"); O.mkdir(parents=True, exist_ok=True)
r = random.Random(20260926); K = {}
HDR = ["Tanggal", "Pelanggan", "Barang", "Jumlah"]


def data(n, bulan=9):
    out = []
    for i in range(n):
        out.append([f"2026-{bulan:02d}-{r.randint(1, 28):02d}", r.choice(["Bu Rina", "Pak Joko", "Toko Makmur", "CV Sinar"]),
                    r.choice(["Beras 5kg", "Gula 1kg", "Minyak 2L", "Telur 1kg"]), r.randint(1, 40) * 1000])
    return out


def tulis_csv(nama, rows, hdr=HDR):
    b = io.StringIO(); w = csv.writer(b, lineterminator="\n"); w.writerow(hdr); w.writerows(rows)
    return b.getvalue()


def simpan(nama, teks):
    (O / nama).write_text(teks, encoding="utf-8", newline="")


def sisip_kutip(teks, baris_fisik, kolom_awal=True, tutup_di=None):
    """Sisipkan kutip nyasar di awal kolom ke-2 baris fisik N (1=judul). tutup_di: baris fisik yang diberi \" di akhir sel Barang."""
    L = teks.split("\n")
    p = L[baris_fisik - 1].split(",", 1); L[baris_fisik - 1] = p[0] + ',"' + p[1]
    if tutup_di:
        q = L[tutup_di - 1].split(","); q[2] = q[2] + ' 14"'; L[tutup_di - 1] = ",".join(q)
    return "\n".join(L)

# C1 kutip nyasar di baris data PERTAMA (baris 2), "tertutup" oleh tanda inci di baris 3 -> 1 baris tertelan
rows = data(20); K["C1"] = {"baris": 20, "total": sum(x[3] for x in rows), "harapan": "GAGAL/peringatan tegas"}
simpan("C1-kutip-awal.csv", sisip_kutip(tulis_csv("", rows), 2, tutup_di=3))
# C2 kutip nyasar di tengah (baris 11), tertutup 2 baris kemudian (baris 13) -> 2 baris tertelan
rows = data(20); K["C2"] = {"baris": 20, "total": sum(x[3] for x in rows), "harapan": "GAGAL/peringatan tegas"}
simpan("C2-kutip-tengah.csv", sisip_kutip(tulis_csv("", rows), 11, tutup_di=13))
# C3 kutip nyasar di baris TERAKHIR, tak tertutup
rows = data(20); K["C3"] = {"baris": 20, "total": sum(x[3] for x in rows), "harapan": "GAGAL/peringatan tegas"}
simpan("C3-kutip-akhir.csv", sisip_kutip(tulis_csv("", rows), 21).rstrip("\n") + "\n")

# C4 file dengan alamat multi-baris SAH + "" di banyak baris, dan SATU kutip nyasar di kolom Alamat
H4 = ["Tanggal", "Pelanggan", "Alamat", "Jumlah"]
rows4 = []
for i in range(24):
    al = f"Jl. Melati No. {i+1}, RT 0{i%9+1}/RW 02\nKel. Sukajadi, Kec. \"\"Kota\"\" Baru\nBandung, 40{100+i}" if i % 2 == 0 else f"Ruko \"Blok A\" No. {i}"
    rows4.append([f"2026-09-{i+1:02d}", f"Pelanggan {i+1}", al, (i + 1) * 2500])
b = io.StringIO(); w = csv.writer(b, lineterminator="\n"); w.writerow(H4)
for i, x in enumerate(rows4):
    if i == 15:  # baris data ke-16: alamat satu baris diberi kutip pembuka nyasar, ditutup kutip di sel alamat baris berikutnya
        b.write(f'{x[0]},{x[1]},"Gg. Mawar 3,{x[3]}\n'); continue
    w.writerow(x)
simpan("C4-alamat-sah-plus-nyasar.csv", b.getvalue())
K["C4"] = {"baris": 24, "total": sum(x[3] for x in rows4), "harapan": "GAGAL/peringatan tegas"}

# C5 SAH: alamat 3 baris berkoma + "" + catatan multi-baris (tanpa kutip nyasar)
H5 = ["No", "Tanggal", "Pelanggan", "Alamat", "Catatan", "Total"]
rows5 = []
for i in range(30):
    al = f"Jl. Kenanga No. {i+3}, Blok {chr(65+i%5)}, RT 03/RW 07\nKel. Cempaka Putih, Kec. Cempaka\nJakarta Pusat, 10{510+i}"
    cat = ["", "Kirim sore, jangan \"lempar\" paket", "Titip satpam\nHubungi 0812xxxx dulu, 2x", "Bayar: transfer, 50%\nsisa: COD"][i % 4]
    rows5.append([i + 1, f"2026-09-{i%28+1:02d}", f"Pembeli {i+1}", al, cat, 10000 + i * 1750])
simpan("C5-sah-alamat-3-baris.csv", tulis_csv("", rows5, H5))
K["C5"] = {"baris": 30, "total": sum(x[5] for x in rows5), "harapan": "benar, tidak ditolak"}

# C6 SAH mirip rusak: HANYA 1 sel catatan multi-baris di seluruh file, baris keduanya mirip baris data
H6 = ["Tanggal", "Barang", "Catatan", "Jumlah"]
rows6 = [[f"2026-09-{i+1:02d}", r.choice(["Kopi", "Teh", "Gula"]), "", r.randint(5, 60) * 1000] for i in range(18)]
rows6[7][2] = "ganti barang:\n2026-09-09,Teh,retur,12000"
simpan("C6-sah-satu-catatan-mirip-data.csv", tulis_csv("", rows6, H6))
K["C6"] = {"baris": 18, "total": sum(x[3] for x in rows6), "harapan": "benar, atau ditolak DENGAN jalan keluar --paksa yang lalu benar"}

# C7 SAH: catatan berbaris baru biasa (tidak mirip data) di 2 baris; kolom catatan biasanya kosong
rows7 = [[f"2026-09-{i+1:02d}", r.choice(["Kopi", "Teh"]), "", r.randint(5, 60) * 1000] for i in range(15)]
rows7[3][2] = "barang datang telat\nsudah dikomplain"; rows7[11][2] = "Diskon, karena\nkemasan penyok"
simpan("C7-sah-catatan-baris-baru.csv", tulis_csv("", rows7, H6))
K["C7"] = {"baris": 15, "total": sum(x[3] for x in rows7), "harapan": "benar, tidak ditolak"}


# C8 satu baris KURANG sel (kolom Barang terlewat, angka bergeser ke kolom Barang) - tanpa kutip sama sekali
rows8 = data(20); t8 = tulis_csv("", rows8).split("\n"); x = rows8[9]; t8[10] = f"{x[0]},{x[1]},{x[3]}"
simpan("C8-baris-kurang-sel.csv", "\n".join(t8))
K["C8"] = {"baris": 20, "total": sum(x[3] for x in rows8), "harapan": "peringatan tegas baris 11 kurang sel"}

# ---------- XLSX minimal (sharedStrings), angka sebagai angka
def xlsx(nama, sheets):
    ss, idx = [], {}
    def si(t):
        if t not in idx: idx[t] = len(ss); ss.append(t)
        return idx[t]
    def col(c):
        s = ""; c += 1
        while c: c, m = divmod(c - 1, 26); s = chr(65 + m) + s
        return s
    z = zipfile.ZipFile(O / nama, "w", zipfile.ZIP_DEFLATED)
    sx = []
    for n, (sn, rows) in enumerate(sheets, 1):
        body = []
        for ri, row in enumerate(rows, 1):
            cs = []
            for ci, v in enumerate(row):
                ref = f"{col(ci)}{ri}"
                if v is None or v == "": continue
                if isinstance(v, (int, float)): cs.append(f'<c r="{ref}"><v>{v}</v></c>')
                else: cs.append(f'<c r="{ref}" t="s"><v>{si(str(v))}</v></c>')
            body.append(f'<row r="{ri}">{"".join(cs)}</row>')
        z.writestr(f"xl/worksheets/sheet{n}.xml", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>' + "".join(body) + "</sheetData></worksheet>")
        sx.append(sn)
    z.writestr("[Content_Types].xml", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>' + "".join(f'<Override PartName="/xl/worksheets/sheet{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>' for i in range(1, len(sx) + 1)) + "</Types>")
    z.writestr("_rels/.rels", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>')
    z.writestr("xl/workbook.xml", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets>' + "".join(f'<sheet name="{escape(s)}" sheetId="{i}" r:id="rId{i}"/>' for i, s in enumerate(sx, 1)) + "</sheets></workbook>")
    z.writestr("xl/_rels/workbook.xml.rels", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + "".join(f'<Relationship Id="rId{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet{i}.xml"/>' for i in range(1, len(sx) + 1)) + f'<Relationship Id="rId{len(sx)+1}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/></Relationships>')
    z.writestr("xl/sharedStrings.xml", '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><sst xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">' + "".join(f"<si><t xml:space=\"preserve\">{escape(t)}</t></si>" for t in ss) + "</sst>")
    z.close()

HX = ["Tanggal", "Kategori", "Jumlah"]
KAT = ["ATK", "Listrik", "Transport", "Konsumsi"]
def bulan(m, n): return [[f"2026-{m:02d}-{r.randint(1, 28):02d}", r.choice(KAT), r.randint(5, 90) * 5000] for _ in range(n)]
def per_kat(rs): return {k: sum(x[2] for x in rs if x[1] == k) for k in KAT}

# X1 Sep/Okt/Nov data + "Sheet4" (sheet terakhir) = rekap per kategori, JUDUL KOLOM SAMA
s9, s10, s11 = bulan(9, 15), bulan(10, 18), bulan(11, 12); semua = s9 + s10 + s11
rek = [["", k, v] for k, v in per_kat(semua).items()]
xlsx("X1-rekap-bernama-Sheet4.xlsx", [("Sep", [HX] + s9), ("Okt", [HX] + s10), ("Nov", [HX] + s11), ("Sheet4", [HX] + rek)])
K["X1"] = {"baris": len(semua), "total": sum(x[2] for x in semua), "per_kategori": per_kat(semua)}

# X2 Sheet1/Sheet2/Sheet3 data + "Okt" = rekap per sheet (Tanggal=nama bulan) dengan judul kolom sama
a, b2, c = bulan(7, 14), bulan(8, 16), bulan(9, 13); semua2 = a + b2 + c
rek2 = [["Juli", "Semua", sum(x[2] for x in a)], ["Agustus", "Semua", sum(x[2] for x in b2)], ["September", "Semua", sum(x[2] for x in c)]]
xlsx("X2-rekap-bernama-Okt.xlsx", [("Sheet1", [HX] + a), ("Sheet2", [HX] + b2), ("Sheet3", [HX] + c), ("Okt", [HX] + rek2)])
K["X2"] = {"baris": len(semua2), "total": sum(x[2] for x in semua2)}

# X3 sheet bernama "Rekap Des" yang sebenarnya DATA transaksi Desember (harus bisa ikut dengan --sertakan)
o, n, d = bulan(10, 10), bulan(11, 11), bulan(12, 12)
xlsx("X3-Rekap-berisi-data.xlsx", [("Okt", [HX] + o), ("Nov", [HX] + n), ("Rekap Des", [HX] + d)])
K["X3"] = {"tanpa_sertakan": {"baris": 21, "total": sum(x[2] for x in o + n)},
           "dengan_sertakan": {"baris": 33, "total": sum(x[2] for x in o + n + d)}}

# X4 Jan/Feb/Mar/Apr kolom sama, Feb KOSONG (judul saja)
j, m, ap = bulan(1, 9), bulan(3, 11), bulan(4, 8)
xlsx("X4-satu-bulan-kosong.xlsx", [("Jan", [HX] + j), ("Feb", [HX]), ("Mar", [HX] + m), ("Apr", [HX] + ap)])
K["X4"] = {"baris": 28, "total": sum(x[2] for x in j + m + ap), "per_bulan": {"01": sum(x[2] for x in j), "03": sum(x[2] for x in m), "04": sum(x[2] for x in ap)}}

# X5 rekap bernama "Sheet4" yang TIDAK tepat = jumlah (satu kategori dibulatkan/ketinggalan update), judul sama
rek5 = [["", k, v] for k, v in per_kat(semua).items()]; rek5[0][2] += 5000
xlsx("X5-rekap-tidak-persis.xlsx", [("Sep", [HX] + s9), ("Okt", [HX] + s10), ("Nov", [HX] + s11), ("Sheet4", [HX] + rek5)])
K["X5"] = {"baris": len(semua), "total": sum(x[2] for x in semua)}

(O / "kunci-v103.json").write_text(json.dumps(K, indent=1, ensure_ascii=False), encoding="utf-8")
print("OK", O)
