#!/usr/bin/env python3
"""Fixture uji ulang v1.0.9 (penguji independen ke-10). Python standar, deterministik.
Fokus: PENGAMAN SILANG Grand Total (cocok, salah di file karena angka-teks / baris terlewat, subtotal tersembunyi 2x/3x,
tanpa Grand Total, label EN di kolom lain, beberapa kolom angka) + 3 tabel rapi kontrol.
kunci-v109.json dihitung dari data sumber di script ini, TANPA membaca kode skill.
Pakai: python3 buat_fixture_uji_v109.py [folder]"""
import json, zipfile, csv, sys
from pathlib import Path
from xml.sax.saxutils import escape
O=Path(sys.argv[1] if len(sys.argv)>1 else 'fixture-v109'); O.mkdir(parents=True, exist_ok=True); K={}
def col(i):
    s="";i+=1
    while i: i,r=divmod(i-1,26); s=chr(65+r)+s
    return s
def xlsx(nama, rows):
    xs=[]
    for r,row in enumerate(rows,1):
        cs=[]
        for c,v in enumerate(row):
            ref=f"{col(c)}{r}"
            if v is None or v=="": continue
            if isinstance(v,tuple):  # ('f', formula, cached)
                cs.append(f'<c r="{ref}"><f>{escape(v[1])}</f><v>{v[2]}</v></c>')
            elif isinstance(v,str): cs.append(f'<c r="{ref}" t="inlineStr"><is><t>{escape(v)}</t></is></c>')
            else: cs.append(f'<c r="{ref}"><v>{v}</v></c>')
        xs.append(f'<row r="{r}">{"".join(cs)}</row>')
    sh=('<?xml version="1.0" encoding="UTF-8" standalone="yes"?><worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">'
        f'<sheetData>{"".join(xs)}</sheetData></worksheet>')
    with zipfile.ZipFile(O/nama,"w",zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml",'<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/><Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/></Types>')
        z.writestr("_rels/.rels",'<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/></Relationships>')
        z.writestr("xl/workbook.xml",'<?xml version="1.0" encoding="UTF-8"?><workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Data" sheetId="1" r:id="rId1"/></sheets></workbook>')
        z.writestr("xl/_rels/workbook.xml.rels",'<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/></Relationships>')
        z.writestr("xl/worksheets/sheet1.xml",sh)
def csvw(nama, rows, sep=","):
    with open(O/nama,"w",newline="",encoding="utf-8") as f:
        w=csv.writer(f,delimiter=sep)
        for r in rows: w.writerow(["" if v is None else v for v in r])
def rp(n): return f"{n:,}".replace(",",".")

# X1 rapi + Grand Total benar
d=[("2026-09-0%d"%(i+1),p,q,h) for i,(p,q,h) in enumerate([("Kaos",3,75000),("Topi",2,45000),("Kaos",5,75000),("Jaket",1,250000),("Topi",4,45000),("Celana",2,180000),("Jaket",2,250000),("Kaos",1,75000)])]
rows=[["Tanggal","Produk","Qty","Harga","Total"]]+[[a,b,q,h,q*h] for a,b,q,h in d]
tq=sum(x[2] for x in d); tt=sum(x[2]*x[3] for x in d)
rows.append(["Grand Total","",tq,"",tt]); csvw("X1-gt-benar-rapi.csv",rows)
K["X1"]=dict(baris=8,qty=tq,total=tt,harap="COCOK")

# X2 xlsx, 2 angka diketik teks, TOTAL = SUM Excel (lewati teks)
vals=[1250000,875000,430000,2100000,660000,315000,990000,1480000]
teks={2,5}
rows=[["Tanggal","Keterangan","Nominal"]]
for i,v in enumerate(vals):
    rows.append([46266+i,f"Biaya {i+1}", f"Rp {rp(v)}" if i in teks else v])
sumexcel=sum(v for i,v in enumerate(vals) if i not in teks)
rows.append(["TOTAL","",("f","SUM(C2:C9)",sumexcel)]); xlsx("X2-gt-salah-angka-teks.xlsx",rows)
K["X2"]=dict(baris=8,total=sum(vals),total_di_file=sumexcel,harap="PERINGATAN: script benar, total file kurang 2 sel teks")

# X3 subtotal cabang ditaruh di bawah data (label netral), lalu Grand Total benar -> 2x
dat=[("Bekasi","Kopi",120000),("Bekasi","Teh",85000),("Bekasi","Susu",43000),("Bogor","Kopi",210000),("Bogor","Teh",67000),("Depok","Kopi",155000),("Depok","Susu",99000)]
rows=[["Cabang","Produk","Omzet"]]+[list(x) for x in dat]
cab={}
for c,p,v in dat: cab[c]=cab.get(c,0)+v
for c in cab: rows.append([c,"(semua produk)",cab[c]])
gt=sum(v for *_,v in dat); rows.append(["Grand Total","",gt]); csvw("X3-subtotal-terpisah-gt.csv",rows)
K["X3"]=dict(baris=7,total=gt,harap="2x tertangkap",salah=2*gt)

# X4 rekap per cabang + per produk di bawah -> 3x, label netral, xlsx
rows=[["Cabang","Produk","Omzet"]]+[list(x) for x in dat]
for c in cab: rows.append([c,"Semua",cab[c]])
prod={}
for c,p,v in dat: prod[p]=prod.get(p,0)+v
for p in prod: rows.append(["Semua",p,prod[p]])
rows.append(["Total Keseluruhan",None,gt]); xlsx("X4-rekap-ganda-3x.xlsx",rows)
K["X4"]=dict(baris=7,total=gt,salah=3*gt,harap="3x tertangkap")

# X5 tanpa GT
rows=[["Tanggal","Pemasok","Jumlah (Rp)"]]+[[f"0{i+1}/09/2026",n,v] for i,(n,v) in enumerate([("CV Maju",1500000),("PT Sinar",2750000),("UD Berkah",640000),("CV Maju",980000),("Toko Abadi",315000)])]
csvw("X5-tanpa-gt.csv",rows,sep=";"); K["X5"]=dict(baris=5,total=6185000,harap="tanpa pesan silang")

# X6 EN, label Grand Total di kolom C (A,B kosong), angka D,E
dd=[("North","Widget","Q3",12,3600000),("North","Gadget","Q3",7,2450000),("South","Widget","Q3",9,2700000),("South","Gizmo","Q3",4,1880000),("East","Gadget","Q3",11,3850000)]
rows=[["Region","Item","Quarter","Units","Revenue"]]+[list(x) for x in dd]
rows.append([None,None,"Grand Total",sum(x[3] for x in dd),sum(x[4] for x in dd)]); xlsx("X6-gt-kolom-c-en.xlsx",rows)
K["X6"]=dict(baris=5,units=43,revenue=sum(x[4] for x in dd),harap="COCOK")

# X7 3 kolom angka; Total benar di Qty & Omzet, salah ketik di Diskon
d7=[("A01",5,500000,25000),("A02",3,420000,0),("A03",8,960000,48000),("A04",2,150000,7500),("A05",6,780000,39000),("A06",4,300000,15000)]
rows=[["Kode","Qty","Omzet","Diskon"]]+[list(x) for x in d7]
dq=sum(x[1] for x in d7); do=sum(x[2] for x in d7); ds=sum(x[3] for x in d7)
rows.append(["Total",dq,do,ds+10000]); csvw("X7-gt-satu-kolom-salah.csv",rows)
K["X7"]=dict(baris=6,qty=dq,omzet=do,diskon=ds,diskon_file=ds+10000,harap="PERINGATAN sebagian kolom")

# X8 Total + Rata-rata di ekor, benar
nil=[78,85,92,66,88,74,90]
rows=[["NIS","Nama","Nilai"]]+[[f"10{i:02d}",f"Siswa {chr(65+i)}",v] for i,v in enumerate(nil)]
rows.append(["","Jumlah",sum(nil)]); rows.append(["","Rata-rata",round(sum(nil)/len(nil),2)])
csvw("X8-jumlah-rata-ekor.csv",rows); K["X8"]=dict(baris=7,jumlah=sum(nil),harap="COCOK, rata-rata tidak memicu")

# X9 Total di file lupa baris terakhir (baris ditambah setelah SUM)
v9=[450000,1200000,380000,760000,905000,2300000]
rows=[["Tanggal","Uraian","Pengeluaran"]]+[[f"{i+10}/09/2026",f"Belanja {i+1}",v] for i,v in enumerate(v9)]
rows.append(["","TOTAL",sum(v9[:-1])]); csvw("X9-total-lupa-baris-akhir.csv",rows)
K["X9"]=dict(baris=6,total=sum(v9),total_file=sum(v9[:-1]),harap="PERINGATAN beda; script benar")

# X10 JUMLAH dengan desimal koma ID, benar
v10=["12,5","8,75","10","7,25","15,5"]
rows=[["Nama","Jam Lembur"]]+[[f"Karyawan {i+1}",v] for i,v in enumerate(v10)]
rows.append(["JUMLAH","54"]); csvw("X10-jumlah-desimal.csv",rows,sep=";")
K["X10"]=dict(baris=5,jam="54",harap="COCOK")

# X11 subtotal per bulan di bawah + GT; xlsx, 2 kolom angka, label "Rekap Juli" kata kunci? pakai label bulan saja
d11=[("Jul","Iklan",1000000,2),("Jul","Sewa",3000000,1),("Agu","Iklan",1200000,3),("Agu","Sewa",3000000,1),("Sep","Iklan",900000,2),("Sep","Sewa",3000000,1)]
rows=[["Bulan","Pos","Biaya","Frekuensi"]]+[list(x) for x in d11]
for b in ("Jul","Agu","Sep"):
    rows.append([b,"Semua pos",sum(x[2] for x in d11 if x[0]==b),sum(x[3] for x in d11 if x[0]==b)])
rows.append(["Grand Total","",sum(x[2] for x in d11),sum(x[3] for x in d11)]); xlsx("X11-subtotal-bulan-bawah-2kolom.xlsx",rows)
K["X11"]=dict(baris=6,biaya=sum(x[2] for x in d11),frek=10,harap="2x tertangkap")

# kontrol
csvw("K1-kontrol-kas.csv",[["Tanggal","Keterangan","Masuk","Keluar"],["01/09/2026","Setoran",500000,0],["02/09/2026","Beli ATK",0,85000],["03/09/2026","Jual",275000,0],["04/09/2026","Listrik",0,410000]])
K["K1"]=dict(masuk=775000,keluar=495000)
xlsx("K2-kontrol-produk-total-care.xlsx",[["Produk","Stok","Harga"],["Total Care Shampoo",24,32000],["Sabun Mandi",40,5500],["Total Care Sampo Anak",12,28500],["Pasta Gigi",30,12000]])
K["K2"]=dict(stok=106,harap="nama produk berawalan Total bukan ringkasan")
with open(O/"K3-kontrol-absen.tsv","w",encoding="utf-8") as f:
    f.write("Nama\tDivisi\tHadir\n"+"".join(f"P{i}\t{dv}\t{h}\n" for i,(dv,h) in enumerate([("Gudang",22),("Kantor",21),("Gudang",20),("Toko",23),("Kantor",19)])))
K["K3"]=dict(hadir=105)
(O/"kunci-v109.json").write_text(json.dumps(K,indent=1))
