# Uji A/B — Skenario 01 TANPA skill vs DENGAN skill

> Penguji independen, 2026-09-25. Fixture: `Penjualan 2026.xlsx` dari `buat_fixture_uji.py`.
> Pertanyaan: *"Kategori apa paling laku, tren per bulan, dan banding Q2 vs Q3?"*

## A. Tanpa skill (simulasi agent umum)
Lingkungan uji tidak punya openpyxl/pandas (kondisi umum di laptop pembeli). Agent tanpa skill menulis
parser zipfile cepat — pendekatan paling wajar yang bisa dilakukan tanpa instal paket:
```python
# Simulasi pendekatan agent umum TANPA skill: tanpa openpyxl/pandas, tulis parser zipfile cepat.
import zipfile, re, xml.etree.ElementTree as ET
from datetime import date, timedelta
from collections import defaultdict
ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
z=zipfile.ZipFile('fx/Penjualan 2026.xlsx')
ss=[ ''.join(t.text or '' for t in si.iter('{%s}t'%ns['m'])) for si in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si',ns)]
kat=defaultdict(float); bln=defaultdict(float); q=defaultdict(float)
for i in (2,3,4):   # agent melihat 4 sheet, melewati 'Master Barang'
    root=ET.fromstring(z.read('xl/worksheets/sheet%d.xml'%i))
    for row in root.find('m:sheetData',ns):
        vals={}
        for c in row:
            col=re.match(r'[A-Z]+',c.get('r')).group(); v=c.find('m:v',ns)
            if v is None: continue
            vals[col]= ss[int(v.text)] if c.get('t')=='s' else v.text
        if int(row.get('r'))<=3: continue
        try: tot=float(vals.get('G'))
        except (TypeError,ValueError): continue    # teks "Rp ..." / "(185.000)" / kosong terlewat
        try: tg=date(1899,12,30)+timedelta(days=int(float(vals['A'])))
        except (KeyError,ValueError): tg=None       # baris TOTAL: tanggal tidak ada
        k=vals.get('C','?')
        kat[k]+=tot
        if tg: bln[tg.strftime('%Y-%m')]+=tot; q[(tg.month-1)//3+1]+=tot
print('per kategori:',sorted(kat.items(),key=lambda x:-x[1]))
print('per bulan:',sorted(bln.items()))
print('per Q:',dict(q), 'Q3 vs Q2 %:', round((q[3]-q[2])/q[2]*100,1))
print('grand total (sum kategori):',sum(kat.values()))
```
Keluaran nyata:
```
per kategori: [('?', 232532000.0), ('Semen', 83532000.0), ('Keramik', 29915000.0), ('Cat', 29447000.0), ('Besi', 21321000.0), ('Pipa & Sanitasi', 21251000.0), ('SEMEN', 10944000.0), ('semen ', 9794000.0), ('Alat & Perkakas', 7143000.0), ('CAT', 6894000.0), ('pipa & sanitasi', 4202000.0), ('besi', 4107000.0), ('KERAMIK', 2870000.0), ('alat & perkakas', 1016000.0), (' cat', 96000.0)]
per bulan: [('2026-01', 23917000.0), ('2026-02', 17208500.0), ('2026-03', 25507500.0), ('2026-04', 34340000.0), ('2026-05', 30672500.0), ('2026-06', 32100000.0), ('2026-07', 17661000.0), ('2026-08', 26143000.0), ('2026-09', 24982500.0)]
per Q: {1: 66633000.0, 2: 97112500.0, 3: 68786500.0} Q3 vs Q2 %: -29.2
grand total (sum kategori): 465064000.0
```
Jawaban yang akan diberikan agent: "Total penjualan Rp 465.064.000; kategori terbesar '?' ..."
atau—bila agent jeli membuang '?'—"Semen Rp 83.532.000, SEMEN Rp 10.944.000, semen Rp 9.794.000 ..."
dan "Q3 turun 29,2%".

## B. Dengan skill
Lihat `01-toko-bangunan-xlsx-3-sheet.md` (perintah & keluaran lengkap).

## Perbandingan
| Aspek | Tanpa skill | Dengan skill | Kunci |
|---|---|---|---|
| Grand total | Rp 465.064.000 (baris TOTAL ikut → **dobel**) | Rp 233.556.000 | 233.556.000 |
| Semen | 83.532.000 + varian SEMEN/semen terpisah (3 baris) | Rp 105.444.000 (varian digabung + dilaporkan) | 105.444.000 |
| Teks "Rp 1.250.000" (4 transaksi) & retur "(185.000)" | **diam-diam dilewati** | terbaca sebagai angka | — |
| Feb / Jul / Agu / Sep | 17.208.500 / 17.661.000 / 26.143.000 / 24.982.500 ✘ | 17.888.500 / 17.476.000 / 26.433.000 / 25.221.500 ✔ | sama dgn skill |
| Q3 vs Q2 | −29,2% ✘ | −28,8% ✔ | −28,81% |
| 3 rumus tanpa nilai tersimpan | tidak disadari | dilaporkan per sel (G68, G79, G98) | — |
| Sheet tersembunyi / merge / header baris 3 | di-hardcode manual | otomatis + dilaporkan | — |
| Format jawaban | angka mentah float | tabel siap tempel, temuan, saran grafik, "Perlu dicek" | — |
| Gabung 3 sheet | ✔ (loop sheet sendiri) | ✘ perlu improvisasi (bersihkan → gabung CSV) | — |

**Kesimpulan:** dengan skill **jelas lebih baik** — semua angka cocok kunci, sedangkan tanpa skill total
salah 2× lipat dan 4 bulan meleset. Satu-satunya keunggulan pendekatan tanpa skill: bebas menggabung
sheet — kekurangan skill yang dicatat di HASIL-UJI #1.

## Bahan "sebelum/sesudah" README
Sebelum: "Total penjualan Rp 465 juta" (baris TOTAL terhitung dua kali, SEMEN & Semen dianggap beda).
Sesudah: "Semen Rp 105.444.000 dari total Rp 233.556.000; Q3 turun 28,8% dari Q2; 3 sel rumus tanpa nilai perlu dicek."
