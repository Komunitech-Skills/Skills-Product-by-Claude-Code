# 06 — Uji ulang independen tender-checklist v1.0.1

- Tanggal: 2026-09-25 · Penguji: agent independen baru (bukan pembuat, perevisi, atau penguji v1.0.0), claude-code (simulasi agent)
- Salinan uji: scratchpad `uji2-tender/` (skill disalin, dijalankan dari salinan; repo tidak disentuh selain folder `examples/`)
- Tes bawaan `tests/uji_regresi.py`: **38/38 OK**. `scripts/validate.py`: 68 skill valid. SKILL.md: **100 baris** (< 300).

## 1. Repro bug v1.0.0

| Bug | Repro | Hasil v1.0.1 |
|---|---|---|
| 1 Total tanpa PPN dinyatakan "cocok" | `Total;;;5.000.000`, 100 rim × 50.000, `--ppn nonmewah` | ✅ PERINGATAN "Total di file BELUM TERMASUK PPN: total yang benar Rp5.550.000 (sebelum PPN Rp5.000.000 + PPN Rp550.000)". Tidak ada "cocok". |
| 2 Baris salah hitung tidak ditunjuk | Skenario 03 varian A/B/C (lemari 25 × 2.975.000 ditulis 47.375.000) | ✅ "Baris salah hitung: baris 4 (item 3 'Lemari arsip besi 4 laci'): file Rp47.375.000 != hitung 25 x Rp2.975.000 = Rp74.375.000 (selisih Rp27.000.000)" di ketiga varian, plus jumlah kolom file vs script. |
| 3 Alarm palsu TOTAL di kolom lain | Varian A `;;;;TOTAL;Rp341.775.000` | ✅ Dikenali sebagai baris total, dibandingkan dengan total sesudah PPN (tidak cocok, selisih Rp67.565.250) + catatan "masih SEBELUM PPN dan ikut salah hitung". Tidak ada lagi "uraian kosong"/TOTAL BELUM FINAL palsu; exit 0. |
| 4 HPS "2,4 M" | `parse_angka(besar=True)` untuk "2,4 M", "Rp2,4 M", "2,4M", "2.4M", "2.4 m", "Rp2,4 miliar", "2,4 milyar", "2.400.000.000", "Rp 2.400.000.000,-" | ✅ Semua jadi 2.400.000.000. |
| 5 Jaminan pelaksanaan > Rp200 jt | t07/t09 | ✅ < 80% dan > 200 jt → 5% HPS; 80–100% → 5% nilai kontrak (Rp103.336.074 di t09); ≤ 200 jt → "umumnya tidak diberlakukan". |
| 6 Label jadwal | penjelasan 23/9, hari ini 25/9 | ✅ "SUDAH LEWAT - baca Berita Acara Penjelasan & adendum"; pengumuman "SUDAH LEWAT - pastikan dokumen ... diunduh". |
| 7 Pesan PPN, label kosong, exit code | varian B/C | ✅ PPN hitungan script ditampilkan; label di kolom No tampil ('Total (dari Excel)'); belum final → exit 3. |
| 8 PPh final konstruksi | SKILL.md langkah 5 | ✅ satu kalimat PP 9/2022 + arahkan ke konsultan pajak. |
| Pasal 31 | references/dasar-aturan.md | ✅ dikoreksi jadi Pasal 31. |

## 2. Uji 13 CSV baru buatan penguji (meniru kebiasaan Excel Indonesia)

Kunci jawaban dihitung terpisah (`kunci.py`: Decimal, jumlah baris dibulatkan setengah ke atas, PPN non-mewah = floor(DPP × 11/12 × 12%) dengan aritmetika bilangan bulat, mewah = floor(12% × DPP), mode termasuk PPN = DPP bulat terbesar dengan DPP + PPN ≤ harga, dicari mundur satu per satu). Script dijalankan dengan `--json` lalu dibandingkan otomatis.

**Angka: 12/12 berkas cocok dengan kunci** (setiap jumlah baris, subtotal, DPP, PPN, total, sisa). t13 dicek manual, juga cocok. **Tidak ada ketidakcocokan angka.**

| # | Pola yang diuji | Kunci (total) | Temuan script | Exit | Nilai |
|---|---|---|---|---|---|
| t01 | Pemisah `,`, sel bertanda kutip, "Rp 1.250.000,-", volume "2,5"/"12,75"/"48,6", satuan m3/m2/ls, baris kosong, Sub Total/PPN 12% (DPP 11/12)/Grand Total semua benar | 25.774.571 | 3× "cocok" (benar) | 0 | ✅ |
| t02 | PKP, "Jumlah Total" = sebelum PPN | 63.543.337 | "BELUM TERMASUK PPN, total yang benar Rp63.543.337" | 0 | ✅ |
| t03 | "PPN 12%" = 12% × DPP penuh (lupa 11/12) + "TOTAL + PPN 12%" | 140.276.250 | Keduanya tidak cocok; selisih −Rp1.268.550 | 0 | ✅ |
| t04 | Label Jumlah/PPN 11%/Total di kolom Harga Satuan; 1 baris rumus salah (60 × 48.750 ditulis 2.295.000) | 58.091.850 | Baris 4 ditunjuk (selisih Rp630.000); 3 baris ringkasan tidak cocok, masing-masing dengan selisih | 0 | ✅ |
| t05 | Pembulatan per baris (2,5 × 1.333 = 3.332,5 → 3.333; 37,5 × 98.765,50), non-PKP | 4.286.852 | Tidak ada alarm salah hitung; Subtotal cocok | 0 | ✅ |
| t06 | Harga termasuk PPN, baris DPP/PPN kosong, "Total (termasuk PPN)" | DPP 65.335.586, PPN 7.186.914, sisa 0 | Cocok; baris kosong dilewati | 0 | ✅ |
| t07 | Tanpa judul kolom, "28.750" kg, "1.120" m2, "312,5" m3, TOTAL di kolom No, HPS "2,4 miliar" lalu "Rp1,2 M" | 1.245.200.000 | Total file salah terdeteksi; 51,88% → klarifikasi + 5% HPS Rp120.000.000; HPS 1,2 M → MELEBIHI HPS Rp45.200.000 (103,77%) | 0 | ✅ |
| t08 | Harga "menyusul" + baris Total | 45.200.000 (sementara) | TOTAL BELUM FINAL, baris 3 ditunjuk; **tetapi juga Info "Total ... cocok"** dengan total sementara | 3 | ⚠ (rendah) |
| t09 | Mewah 12%, "Rp 612.345.678,-", HPS "Rp2,4 M" | 2.066.721.478 (86,11%) | Grand Total salah (−Rp885.923) terdeteksi; info jaminan 5% kontrak Rp103.336.074 | 0 | ✅ |
| t10 | Pemisah TAB, baris kosong, Sub Total/PPN 11%/Total benar, "Dibulatkan" 278.061.000, baris Terbilang | 278.061.660 | 3 cocok; Dibulatkan dilaporkan tidak cocok (selisih Rp660) — benar secara fakta | 0 | ✅ |
| t11 | **"Total Harga Sebelum PPN"** (benar) + **"DPP Nilai Lain (11/12)"** 27.729.167 (benar) + PPN 12% + "Total Harga Setelah PPN" | 33.577.500 | **2 ALARM PALSU**: "Total Harga Sebelum PPN ... BELUM TERMASUK PPN – perbaiki" dan "DPP Nilai Lain ... tidak cocok, selisih Rp2.520.833, cek rumus" | 0 | ❌ |
| t12 | Layout umum barang: `Nama Barang;Jumlah;Satuan;Harga Satuan;Jumlah Harga`; baris 2 salah (150 × 52.500 ditulis 7.785.000) | 12.750.000 | "Jumlah" dipakai sebagai volume (benar), **tetapi kolom "Jumlah Harga" diabaikan → baris salah hitung TIDAK ditunjuk**; hanya Total salah (selisih Rp90.000) | 0 | ⚠ (sedang) |
| t13 | "Harga Total" (tidak dikenali pola) + "Jumlah Harga Termasuk PPN" | 19.011.525 | "Jumlah Harga Termasuk PPN" cocok (benar); **"Harga Total" diam-diam dianggap judul bagian**, nilainya tidak diperiksa | 0 | ⚠ (rendah) |

Tidak ditemukan satu pun "cocok" palsu untuk total yang salah basis (bug 1 benar-benar tertutup). t08 "cocok" hanya terhadap total sementara, dengan TOTAL BELUM FINAL di atasnya.

## 3. Temuan baru (berprioritas)

1. **[SEDANG] Alarm palsu untuk label yang menyebut basisnya sendiri** (t11). `jenis_total()` menggolongkan "Total Harga Sebelum PPN" / "Total sebelum pajak" / "Total DPP" sebagai `total`, sehingga keluar "BELUM TERMASUK PPN – perbaiki" padahal file benar. Perbaikan: label berisi "sebelum ppn/sebelum pajak/belum termasuk ppn/dpp/excl" → `subtotal`; "setelah/sesudah/termasuk/incl ppn" → `total`.
2. **[SEDANG] Baris "DPP Nilai Lain (11/12)" dianggap subtotal** (t11). Sejak PMK 131/2024 banyak Excel PKP memuat baris ini. Perbaikan: label berisi "nilai lain" atau "11/12" → bandingkan dengan floor/bulat(11/12 × DPP) (terima selisih ≤ Rp1 karena Excel membulatkan), jangan dengan DPP.
3. **[SEDANG] Kolom "Jumlah Harga" diabaikan bila "Jumlah" = banyaknya** (t12, layout tabel barang yang umum). `kenali_header()` memasukkan "Jumlah" ke kunci `jumlah` lebih dulu, lalu "Jumlah Harga" dilewati. Perbaikan: jika ada dua kolom yang cocok ke `jumlah`, yang ber-"harga/total/rp" menjadi `jumlah`, yang polos menjadi `volume`. Tambah tes regresi.
4. **[RENDAH] Baris ringkasan yang labelnya tidak dikenali** ("Harga Total", "Nilai Penawaran", "Total Keseluruhan" sudah ok) tapi punya angka di kolom Jumlah tanpa volume/harga → saat ini "judul bagian" tanpa peringatan (t13). Sebaiknya: uraian + angka di kolom Jumlah tanpa volume/harga → Info "baris ini tampak seperti total, tidak diperiksa".
5. **[RENDAH] "cocok" saat TOTAL BELUM FINAL** (t08): ubah menjadi "cocok dengan total SEMENTARA (ada baris tak terbaca)".
6. **[RENDAH] Kode keluar**: baris salah hitung / total tidak cocok / melebihi HPS tetap exit 0 (hanya belum final = 3, GALAT = 1, argparse = 2). Tidak salah karena SKILL.md menyuruh membaca PERINGATAN, tetapi exit 2 untuk "ada PERINGATAN" akan membantu agent/otomasi. Opsional.

## 4. Verifikasi aturan (web search 2026-09-25)

| Klaim | Hasil | Sumber |
|---|---|---|
| Jaminan penawaran: HPS > Rp10 M, 1–3% HPS; terintegrasi 1–3% pagu — **Pasal 31** Perpres 12/2021 | ✅ (referensi sudah dikoreksi ke Pasal 31) | peraturan.go.id/files/ps12-2021.pdf; pasal.id …/pasal-31 |
| Jaminan pelaksanaan: kontrak barang/konstruksi/jasa lainnya > Rp200 jt; 80–100% HPS → 5% nilai kontrak; < 80% → 5% HPS — **Pasal 33** | ✅ | pasal.id …/pasal-33; bantuan.inaproc.id (Jaminan Pelaksanaan) |
| < 80% HPS → klarifikasi kewajaran; wajar → jaminan pelaksanaan 5% HPS; tidak wajar → gugur | ✅ | klc2.kemenkeu.go.id; bpbjsetda.bulelengkab.go.id; simantu.pu.go.id |
| PPh final jasa konstruksi PP 9/2022 (tarif tergantung kualifikasi/SBU: mis. 1,75% SBU kecil, 4% tanpa SBU, 2,65% lainnya; berlaku 21 Feb 2022) | ✅ skill hanya mengingatkan & tidak menghitung — sudah tepat | pajak.go.id/en/node/76970; peraturan.bpk.go.id/Details/199710 |

Catatan: butir yang sudah bertanda PERLU REVIEW di v1.0.0 (perubahan pasca-Perpres 46/2025, SKP, pengecualian pengalaman < 3 tahun) tidak diverifikasi ulang di sini dan tetap bertanda.

## 5. Skenario 03 diulang mengikuti SKILL.md v1.0.1

Input sama ("PKP, mebel kantor, HPS Rp538 juta, total Rp379.370.250 sudah termasuk PPN, 70% HPS, aman?"). Agent menjalankan `harga s03.csv --ppn nonmewah --hps "Rp538.000.000"` (varian A). Output yang kini langsung bisa disampaikan tanpa hitung manual:
- **Baris salah hitung (dari script):** baris 4 lemari arsip, file Rp47.375.000 ≠ 25 × Rp2.975.000 = Rp74.375.000 (selisih Rp27.000.000).
- Kolom Jumlah file Rp341.775.000 vs script Rp368.775.000; baris TOTAL file masih sebelum PPN dan ikut salah.
- DPP Rp368.775.000, PPN Rp40.565.250, total **Rp409.340.250** (Empat Ratus Sembilan Juta Tiga Ratus Empat Puluh Ribu Dua Ratus Lima Puluh Rupiah) = **76,09% HPS**, batas 80% Rp430.400.000 → klarifikasi kewajaran; jika wajar & menang, jaminan pelaksanaan 5% HPS = **Rp26.900.000**.
- Varian B: baris Jumlah/PPN 11%/Total ditandai tidak cocok, dan PPN hitungan script Rp40.565.250 ikut ditampilkan. Varian C: 'Total (dari Excel)' dibandingkan dengan benar.
Semua angka cocok dengan verifikasi Decimal di `03-76persen-hps-salah-hitung.md`. ✅ Temuan v1.0.0 (agent harus membandingkan manual) sudah tidak berlaku.

## Lampiran — isi CSV uji (TAB ditulis `<TAB>`)
### t01.csv
```
No,Uraian Pekerjaan,Vol,Sat,Harga Satuan (Rp),Jumlah Harga (Rp)

1,Galian tanah pondasi,"2,5",m3,"Rp 1.250.000,-","Rp 3.125.000,-"
2,Pasangan batu kali,"12,75",m3,"Rp 985.500,-","Rp 12.565.125,-"

3,Plester dinding,"48,6",m2,"Rp 62.350,-","Rp 3.030.210,-"
4,Mobilisasi,1,ls,"Rp 4.500.000,-","Rp 4.500.000,-"
,Sub Total,,,,"Rp 23.220.335,-"
,PPN 12% (DPP 11/12),,,,"Rp 2.554.236,-"
,Grand Total,,,,"Rp 25.774.571,-"
```
### t02.csv
```
No;Nama Barang;Qty;Satuan;Harga Satuan;Jumlah
1;Laptop 14 inci i5;4;unit;Rp 12.350.000;Rp 49.400.000
2;Printer laser A4;2;unit;Rp 3.275.000;Rp 6.550.000
3;Kabel LAN Cat6;305;m;Rp 4.250;Rp 1.296.250
;Jumlah Total;;;;Rp 57.246.250
```
### t03.csv
```
Uraian;Volume;Satuan;Harga Satuan;Jumlah
Seragam dinas PDH;150;stel;Rp 385.000;Rp 57.750.000
Topi lapangan;150;buah;Rp 45.500;Rp 6.825.000
Sepatu PDL;150;pasang;Rp 412.000;Rp 61.800.000
PPN 12%;;;;Rp 15.169.800
TOTAL + PPN 12%;;;;Rp 141.544.800
```
### t04.csv
```
No;Uraian;Volume;Satuan;Harga Satuan;Jumlah
1;Cat tembok 25 kg;40;pail;Rp1.150.000;Rp46.000.000
2;Kuas 4 inci;60;buah;Rp27.500;Rp1.650.000
3;Rol cat;60;buah;Rp48.750;Rp2.295.000
4;Amplas;200;lembar;Rp3.200;Rp640.000
5;Thinner;35;liter;Rp32.000;Rp1.120.000
;;;;Jumlah;Rp51.705.000
;;;;PPN 11%;Rp5.687.550
;;;;Total;Rp57.392.550
```
### t05.csv
```
Uraian;Volume;Satuan;Harga Satuan;Jumlah
Kabel NYM 3x2,5;2,5;roll;1.333;3.333
Pipa conduit;0,75;batang;12.345;9.259
Besi beton 10 mm;37,5;batang;98.765,50;3.703.706
Upah pasang;3,25;OH;175.555;570.554
Subtotal;;;;4.286.852
```
### t06.csv
```
Uraian;Volume;Satuan;Harga Satuan
Kursi lipat;75;unit;Rp 287.600
Meja lipat;25;unit;Rp 1.118.900
Tenda 3x3;4;unit;Rp 5.745.000
DPP;;;
PPN;;;
Total (termasuk PPN);;;Rp 72.522.500
```
### t07.csv
```
1;Pekerjaan persiapan;1;ls;45.000.000
2;Pekerjaan beton K-250;312,5;m3;1.485.000
3;Pekerjaan besi tulangan;28.750;kg;16.450
4;Pekerjaan bekisting;1.120;m2;235.000
TOTAL;;;;1.713.550.625
```
### t08.csv
```
Uraian;Volume;Satuan;Harga Satuan;Jumlah
Beras premium 5 kg;400;karung;Rp 78.500;Rp 31.400.000
Minyak goreng 2 L;400;pouch;menyusul;
Gula pasir 1 kg;800;kg;Rp 17.250;Rp 13.800.000
Total;;;;Rp 45.200.000
```
### t09.csv
```
Uraian;Volume;Satuan;Harga Satuan;Jumlah
Kendaraan dinas SUV;3;unit;Rp 612.345.678,-;Rp 1.837.037.034,-
Karpet dasar;3;set;Rp 2.750.000,-;Rp 8.250.000,-
Grand Total;;;;Rp 2.067.607.401,-
```
### t10.csv
```
No<TAB>Uraian<TAB>Volume<TAB>Satuan<TAB>Harga Satuan<TAB>Jumlah Harga
1<TAB>Jasa kebersihan gedung<TAB>12<TAB>bulan<TAB>Rp 18.750.000<TAB>Rp 225.000.000
2<TAB>Bahan pembersih<TAB>12<TAB>bulan<TAB>Rp 2.125.500<TAB>Rp 25.506.000

<TAB>Sub Total<TAB><TAB><TAB><TAB>Rp 250.506.000
<TAB>PPN 11%<TAB><TAB><TAB><TAB>Rp 27.555.660
<TAB>Total<TAB><TAB><TAB><TAB>Rp 278.061.660
<TAB>Dibulatkan<TAB><TAB><TAB><TAB>Rp 278.061.000
<TAB>Terbilang: Dua Ratus Tujuh Puluh Delapan Juta Enam Puluh Satu Ribu Rupiah<TAB><TAB><TAB><TAB>
```
### t11.csv
```
Uraian;Volume;Satuan;Harga Satuan;Jumlah
Snack rapat;500;kotak;Rp 18.500;Rp 9.250.000
Makan siang;500;kotak;Rp 42.000;Rp 21.000.000
Total Harga Sebelum PPN;;;;Rp 30.250.000
DPP Nilai Lain (11/12);;;;Rp 27.729.167
PPN 12%;;;;Rp 3.327.500
Total Harga Setelah PPN;;;;Rp 33.577.500
```
### t12.csv
```
No;Nama Barang;Jumlah;Satuan;Harga Satuan;Jumlah Harga
1;Map plastik;500;pcs;Rp 3.750;Rp 1.875.000
2;Kertas HVS A4 70g;150;rim;Rp 52.500;Rp 7.785.000
3;Tinta printer;24;botol;Rp 125.000;Rp 3.000.000
;Total;;;;Rp 12.660.000
```
### t13.csv
```
Uraian;Volume;Satuan;Harga Satuan;Jumlah
Pagar BRC;42,5;m;Rp 385.000,-;Rp 16.362.500,-
Cat pagar;42,5;m;Rp 18.000,-;Rp 765.000,-
Harga Total;;;;Rp 17.127.500,-
Jumlah Harga Termasuk PPN;;;;Rp 19.011.525,-
```

### kunci.py (kunci jawaban independen)
```python
# Kunci jawaban independen (Decimal/integer), tanpa memakai kode script
from decimal import Decimal as D, ROUND_HALF_UP
def r(x): return int(D(x).quantize(D(1), rounding=ROUND_HALF_UP))
def ppn(dpp, mode):  # floor, integer arithmetic
    return {"tidak":0, "nonmewah": dpp*11*12//(12*100), "mewah": dpp*12//100}[mode]
def dpp_incl(b, mode):
    d = b
    while d + ppn(d, mode) > b: d -= 1
    return d
K = {
 "t01": ("nonmewah", [("2.5","1250000"),("12.75","985500"),("48.6","62350"),("1","4500000")], False),
 "t02": ("nonmewah", [("4","12350000"),("2","3275000"),("305","4250")], False),
 "t03": ("nonmewah", [("150","385000"),("150","45500"),("150","412000")], False),
 "t04": ("nonmewah", [("40","1150000"),("60","27500"),("60","48750"),("200","3200"),("35","32000")], False),
 "t05": ("tidak", [("2.5","1333"),("0.75","12345"),("37.5","98765.50"),("3.25","175555")], False),
 "t06": ("nonmewah", [("75","287600"),("25","1118900"),("4","5745000")], True),
 "t07": ("tidak", [("1","45000000"),("312.5","1485000"),("28750","16450"),("1120","235000")], False),
 "t08": ("tidak", [("400","78500"),("800","17250")], False),
 "t09": ("mewah", [("3","612345678"),("3","2750000")], False),
 "t10": ("nonmewah", [("12","18750000"),("12","2125500")], False),
 "t11": ("nonmewah", [("500","18500"),("500","42000")], False),
 "t12": ("tidak", [("500","3750"),("150","52500"),("24","125000")], False),
}
import json; out={}
for k,(m,rows,incl) in K.items():
    js=[r(D(v)*D(h)) for v,h in rows]; s=sum(js)
    if incl: dpp=dpp_incl(s,m); p=ppn(dpp,m); tot=s
    else: dpp=s; p=ppn(s,m); tot=s+p
    out[k]=dict(jumlah=js,subtotal=s,dpp=dpp,ppn=p,total=tot,sisa=tot-dpp-p)
    print(k,out[k])
json.dump(out,open("kunci.json","w"))
for hps,t in ((2400000000,out["t07"]["total"]),(1200000000,out["t07"]["total"]),(2400000000,out["t09"]["total"])):
    print(hps, (D(t)/D(hps)*100).quantize(D("0.01"),ROUND_HALF_UP), hps*8//10, hps*5//100, r(D(t)*5/100))
```
