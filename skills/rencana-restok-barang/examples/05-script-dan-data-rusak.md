# Contoh 5: script dengan data skenario 1, data rusak, dan verifikasi angka independen

> Uji penguji independen, 14 Okt 2026. Data fiktif di `data/`. Semua perintah dijalankan dari folder skill (Windows: `python` atau `py`).

## 1. Uji regresi bawaan
`python3 tests/uji_regresi.py` → **113 cek OK, 0 gagal** ("SEMUA LULUS").

## 2. Data skenario 1 apa adanya (seperti dikirim pengguna)
```bash
python3 scripts/rencana_restok.py --file penjualan-90hari.csv --barang stok-sekarang.csv \
  --pemasok pemasok.csv --hari-ini 2026-10-14 --format teks      # pemasok.csv: CV Grosir Bunda;3 / PT Ceria Distribusi;10
```
- Tanggal campur (`2026-09-01` dan `01/09/2026`) dan nama huruf kecil terbaca benar; rentang 16 Jul–13 Okt (90 hari).
- **Nama beda tulis tidak dicocokkan:** "Kaos Kaki Bayi (isi 3)" di data stok dianggap barang lain → muncul sebagai **BARANG MATI palsu** ("belum pernah terjual selama 90 hari", modal tertahan Rp900.000) dan "Kaos Kaki Bayi isi 3" jadi STOK BELUM DIKETAHUI (lead time default 7 hari). Script memberi catatan "1 barang di daftar barang tidak muncul … samakan penulisannya", dan agent di semua jalan uji memperbaikinya, tetapi pencocokan yang mengabaikan tanda kurung akan lebih aman.
- Kelipatan dus 12 belum terpakai karena tidak ada kolomnya (disebut pengguna di chat); agent harus menambahkannya, dan memang melakukannya.

## 3. Data skenario 1 setelah dirapikan (seperti yang dilakukan agent)
Tabel barang ditambah kolom `Kelipatan` (12 untuk PT Ceria) dan nama Kaos Kaki disamakan:
```
RENCANA RESTOK per 14 Okt 2026 | data 16 Jul 2026 - 13 Okt 2026 (90 hari, per hari)
Asumsi: tingkat layanan 95% (z 1,65), lead time default 7 hari, stok cukup 14 hari setelah barang datang, faktor musim 1, barang mati = tidak laku >= 60 hari

RINGKASAN: 12 barang | pesan sekarang 4 (Rp9.799.000) | minggu depan 3 (Rp3.351.000) | aman 3 | barang mati 1 (modal tertahan Rp2.775.000)

PESAN SEKARANG (4)
- Bedak Bayi 150g | stok 9 | laku ±3,11/hari | habis ±2 hari (16 Okt 2026) | PESAN 49 pcs | Rp539.000 | pesan ulang bila stok ≤ 15, stok pengaman 5, stok target 58 | pemasok CV Grosir Bunda, lead time 3 hari (data pemasok) | stok diperkirakan habis ±2 hari lagi, sebelum barang datang (3 hari)
- Popok Celana Bayi M isi 34 | stok 22 | laku ±5,53/hari | habis ±3 hari (17 Okt 2026) | PESAN 79 pcs | Rp4.898.000 | pesan ulang bila stok ≤ 24, stok pengaman 7, stok target 101 | pemasok CV Grosir Bunda, lead time 3 hari (data pemasok)
- Botol Susu Anti Kolik 250ml | stok 38 | laku ±3,92/hari, tren naik 79% | habis ±9 hari (23 Okt 2026) | PESAN 72 pcs = 6 x 12 (dibulatkan ke kelipatan 12) | Rp3.240.000 | pesan ulang bila stok ≤ 54, stok pengaman 15, stok target 109 | pemasok PT Ceria Distribusi, lead time 10 hari (data pemasok) | stok diperkirakan habis ±9 hari lagi, sebelum barang datang (10 hari)
- Tisu Basah Bayi 50 lembar | stok 110 | laku ±9,2/hari | habis ±11 hari (25 Okt 2026) | PESAN 132 pcs = 11 x 12 (dibulatkan ke kelipatan 12) | Rp1.122.000 | pesan ulang bila stok ≤ 109, stok pengaman 17, stok target 238 | pemasok PT Ceria Distribusi, lead time 10 hari (data pemasok)

PESAN MINGGU DEPAN (3)
- Sabun Cair Bayi 200ml | stok 70 | laku ±6,89/hari, tren naik 30% | habis ±10 hari (24 Okt 2026) | PESAN 94 pcs | Rp1.833.000 | pesan ±17 Okt 2026 | pesan ulang bila stok ≤ 46, stok pengaman 26, stok target 143 | pemasok CV Grosir Bunda, lead time 3 hari (data pemasok) | LONJAKAN 2026-09-20: 65 (biasanya 4)
- Minyak Telon 60ml | stok 40 | laku ±4,28/hari | habis ±9 hari (23 Okt 2026) | PESAN 57 pcs | Rp798.000 | pesan ±18 Okt 2026 | pesan ulang bila stok ≤ 19, stok pengaman 6, stok target 79 | pemasok CV Grosir Bunda, lead time 3 hari (data pemasok)
- Kaos Kaki Bayi isi 3 | stok 60 | laku ±2,93/hari, tren naik 46% | habis ±20 hari (3 Nov 2026) | PESAN 48 pcs = 4 x 12 (dibulatkan ke kelipatan 12) | Rp720.000 | pesan ±20 Okt 2026 | pesan ulang bila stok ≤ 42, stok pengaman 13, stok target 83 | pemasok PT Ceria Distribusi, lead time 10 hari (data pemasok)

AMAN (3)
- Selimut Bayi Bulu | stok 8 | laku ±0,39/hari | habis ±20 hari (3 Nov 2026) | pesan ulang bila stok ≤ 4, stok pengaman 2, stok target 9 | pemasok CV Grosir Bunda, lead time 3 hari (data pemasok)
- Pelampung Leher Bayi | stok 55 | laku ±1,14/hari, tren turun -73% | habis ±48 hari (1 Des 2026) | pesan ulang bila stok ≤ 18, stok pengaman 6, stok target 34 | pemasok PT Ceria Distribusi, lead time 10 hari (data pemasok)
- Dot Bayi Silikon isi 2 | stok 260 | laku ±1,66/hari | habis ±157 hari (20 Mar 2027) | pesan ulang bila stok ≤ 24, stok pengaman 7, stok target 47 | pemasok PT Ceria Distribusi, lead time 10 hari (data pemasok) | STOK BERLEBIH, kelebihan 213 pcs (Rp1.917.000) | stok cukup untuk ±157 hari: jangan ditambah dulu

DATA BELUM CUKUP (1)
- Teether Silikon Buah | stok 24 | pemasok PT Ceria Distribusi | barang ini baru tercatat sejak 4 Okt 2026 (10 hari); barang baru atau jarang laku | teramati 37 pcs dalam 10 hari (laju sementara ±3,7/hari); dengan laju itu stok habis ±6 hari; jumlah pesan belum dihitung

BARANG MATI (1)
- Gendongan Hipseat | stok 15 | pemasok CV Grosir Bunda | tidak terjual 70 hari (terakhir 4 Agu 2026) | modal tertahan Rp2.775.000

PESANAN PER PEMASOK
* CV Grosir Bunda - PESAN SEKARANG - total Rp5.437.000
    Bedak Bayi 150g: 49 pcs = Rp539.000
    Popok Celana Bayi M isi 34: 79 pcs = Rp4.898.000
  Draf WA:
    Halo CV Grosir Bunda, saya [isian: nama Anda] dari [isian: nama toko]. Mau pesan barang berikut:
    1. Bedak Bayi 150g: 49 pcs, harga terakhir Rp11.000/pcs
    2. Popok Celana Bayi M isi 34: 79 pcs, harga terakhir Rp62.000/pcs
    Mohon dikonfirmasi ketersediaan, total harga, dan perkiraan tanggal kirim. Bila bisa, barang tiba paling lambat [isian: tanggal]. Terima kasih.
* PT Ceria Distribusi - PESAN SEKARANG - total Rp4.362.000
    Botol Susu Anti Kolik 250ml: 72 pcs = Rp3.240.000
    Tisu Basah Bayi 50 lembar: 132 pcs = Rp1.122.000
  Draf WA:
    Halo PT Ceria Distribusi, saya [isian: nama Anda] dari [isian: nama toko]. Mau pesan barang berikut:
    1. Botol Susu Anti Kolik 250ml: 72 pcs, harga terakhir Rp45.000/pcs
    2. Tisu Basah Bayi 50 lembar: 132 pcs, harga terakhir Rp8.500/pcs
    Mohon dikonfirmasi ketersediaan, total harga, dan perkiraan tanggal kirim. Bila bisa, barang tiba paling lambat [isian: tanggal]. Terima kasih.
* CV Grosir Bunda - PESAN MINGGU DEPAN - total Rp2.631.000
    Sabun Cair Bayi 200ml: 94 pcs = Rp1.833.000
    Minyak Telon 60ml: 57 pcs = Rp798.000
* PT Ceria Distribusi - PESAN MINGGU DEPAN - total Rp720.000
    Kaos Kaki Bayi isi 3: 48 pcs = Rp720.000

Barang paling laris (untuk paket bundling barang mati): Tisu Basah Bayi 50 lembar, Sabun Cair Bayi 200ml, Popok Celana Bayi M isi 34

PERTANYAAN USULAN (maks 3):
  1. Tanggal 20 Sep 2026 Sabun Cair Bayi 200ml terjual 65 (biasanya ±4). Itu pesanan borongan sekali? Bila ya, hitungan bisa diulang tanpa lonjakan itu.
  2. Apakah Teether Silikon Buah barang baru? Bila barang lama yang jarang laku, sebutkan agar dihitung dari awal data.
  3. Ada barang yang sudah dipesan tapi belum datang? Jumlahnya akan dikurangkan dari pesanan.

CATATAN
  - Kolom penjualan dipakai: tanggal='Tanggal', nama='Nama Produk', qty='Qty'

Rencana ini perkiraan dari pola penjualan sebelumnya, bukan jaminan. Cocokkan dulu dengan stok fisik, harga, dan kesanggupan pemasok sebelum memesan; promo, musim, dan libur bisa mengubah permintaan.
```

### Hitung ulang independen
Skrip Python terpisah (tidak mengimpor script skill) menghitung: deret harian 90 hari dengan hari tanpa penjualan = 0, rata-rata, simpangan baku sampel (n − 1), tren = rata-rata 28 hari terakhir ÷ rata-rata 90 hari (dibatasi 0,5–1,5 bila ≥ 1,2 atau ≤ 0,8), SS = 1,65 × sd × √lead time, ROP = laku × LT + SS, target = laku × (LT + 14) + SS (dibulatkan ke atas), kelompok, hari ke ROP, jumlah pesan → kelipatan 12, nilai Rupiah, hari sampai habis (ke bawah) + tanggal, stok berlebih, barang mati, laju sementara barang baru.

**Hasil: 125 angka dibandingkan, 0 beda** (termasuk rata-rata, simpangan, laku dipakai, SS, ROP, target, habis, tanggal habis, tanggal pesan, jumlah pesan, jumlah dus, nilai, modal tertahan, kelebihan stok). Dengan `--abaikan-lonjakan`: **121 angka, 0 beda**.

Contoh baris hitungan (Tisu Basah, PT Ceria, LT 10): μ = 828 ÷ 90 = 9,2; sd = 3,1056; tren 9,5 ÷ 9,2 = 1,03 (stabil); SS = 1,65 × 3,1056 × √10 = 16,20 → 17; ROP = 9,2 × 10 + 16,20 = 108,2 → 109; target = 9,2 × 24 + 16,20 = 237,0 → 238; stok 110 > 109 tetapi (110 − 109) ÷ 9,2 = 0,1 hari → PESAN SEKARANG; 238 − 110 = 128 → kelipatan 12 → **132 pcs (11 dus)** × Rp8.500 = **Rp1.122.000**; habis 110 ÷ 9,2 = 11,96 → 11 hari (25 Okt).

Angka yang dikutip agent di jawaban SESUDAH skenario 1 (lokal dan Telegram) dan skenario 2 identik dengan hasil ini. Skenario 2 (data mingguan) juga dihitung ulang independen: μ = total ÷ 56, sd harian = sd laju mingguan × √7, tren = 4 minggu terakhir ÷ μ → Beras 47, Minyak 71, Gula 75 (pesan ±15 Okt), Telur ROP 28/target 139, Mie ROP 5/target 18: cocok.

### Lonjakan
Sabun Cair 20 Sep = 65 pcs; median hari laku = 4 → 65 ≥ 4 × 4 dan ≥ 4 + 10 → ditandai (benar). Karena tanggalnya di dalam 28 hari terakhir, lonjakan ini juga membuat tren Sabun "naik 30 %" (6,89 ÷ 5,31). Bila pengguna membenarkan borongan (`--abaikan-lonjakan`): laku 4,63/hari, stabil, ROP 21, target 86, habis 15 hari → **AMAN** (pesan berikutnya ±24 Okt), bukan pesan 94 pcs Rp1.833.000. Script tidak menyebut bahwa "tren naik" itu akibat lonjakan.

## 4. Data rusak (`data/penjualan-rusak.csv`)
Disisipkan: tanggal kosong, qty "lima", tanggal "32/13/2026", qty kosong, nama kosong, baris "TOTAL", qty "2 pcs", qty "1 lusin".
- rc = 0; **6 baris dilewati dengan alasan per baris** (baris 6 tanggal tidak terbaca ''; baris 10 jumlah tidak terbaca 'lima'; baris 13 tanggal tidak terbaca '32/13/2026'; baris 21 jumlah kosong; baris 26 nama kosong; baris 784 baris total).
- "2 pcs" → 2 dan "1 lusin" → 12 terbaca: Tisu 830 (= 828 + 2), Popok 510 (= 498 + 12) → Popok pesan 83, Tisu 132; **cocok dengan hitung ulang independen** atas baris yang sah.

| Uji lain | Hasil |
|---|---|
| Kolom qty dihapus | rc 2: "kolom penjualan tidak lengkap: qty. Judul kolom yang terbaca: ['Tanggal', 'Nama Produk']" + saran |
| Kolom tanggal dihapus | rc 2: "kolom penjualan tidak lengkap: tanggal" + saran |
| Semua tanggal kosong | rc 2: "tidak ada baris penjualan yang terbaca", contoh baris + saran format tanggal |
| File kosong / tidak ada | rc 2: "data kosong" / "file tidak bisa dibuka" + saran |
| Stok "sembilan" | diabaikan + catatan "Isian berikut tidak terbaca: stok 'sembilan' (Bedak Bayi 150g)"; Bedak jadi STOK BELUM DIKETAHUI (benar, tanpa jumlah pesan) |
| Stok −5 | PESAN SEKARANG 106 pcs (= 101 − (−5)) + catatan stok minus untuk dicocokkan dengan stok fisik |

Kecil: tanpa tabel barang, nama tampilan diambil dari kemunculan pertama ("sabun cair bayi 200ml" huruf kecil); satuan default "pcs" untuk karung/kg; `--lead-time` dari pengguna tetap dilabeli "default" sehingga pertanyaan usulan menanyakan lead time lagi.

## 5. Konsistensi rumus SKILL.md / references / script
- Rumus μ, sd (n − 1), tren (28 hari ÷ μ, perlu ≥ 42 hari, batas 0,5–1,5), z (1,28/1,65/2,33), SS, ROP, target, posisi, kelompok (≤ ROP atau < 1 hari → sekarang; 1–7 hari → minggu depan), jumlah minggu depan, pembulatan (atas → MOQ → kelipatan), habis (ke bawah), barang mati (≥ 60 hari), stok berlebih (> 90 hari), data belum cukup (< 14 hari), lonjakan (≥ 4 × median & ≥ median + 10, ≥ 5 hari laku): **sama** di SKILL.md, `references/rumus-dan-istilah.md`, dan docstring/kode script.
- Contoh hitung di references (SS 9,6 → 10; ROP 37,6 → 38; target 93,6 → 94; 74 → 84 pcs = 7 dus; SS 90 % = 8, 99 % = 14) dicek ulang: benar.
- SKILL.md menulis "Habis dalam = stok ÷ μ"; script memakai laku/hari yang sudah dikali tren (sesuai references "stok ÷ laku/hari"). Tidak salah, tetapi SKILL.md bisa diperjelas.

<details><summary>Kode hitung ulang independen (dipakai penguji)</summary>

```python
# Hitung ulang independen (tidak mengimpor script skill)
import csv, sys, math, datetime as dt, statistics as st, re, json
def parse_date(s):
    s=s.strip()
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}",s): return dt.date.fromisoformat(s)
    d,m,y=s.split('/'); return dt.date(int(y),int(m),int(d))
def load(path):
    rows=list(csv.DictReader(open(path)))
    sales={}
    for r in rows:
        t=parse_date(r['Tanggal']); n=' '.join(r['Nama Produk'].split()).lower(); q=int(r['Qty'])
        sales.setdefault(n,{}); sales[n][t]=sales[n].get(t,0)+q
    return sales
Z={90:1.28,95:1.65,99:2.33}
def hitung(sales, stok, lead, kel, harga, awal, akhir, acuan, horizon=14, z=1.65, abaikan_lonjakan=False):
    N=(akhir-awal).days+1
    out={}
    for n,d in sales.items():
        first=min(d); last=max(t for t,q in d.items() if q>0)
        deret=[d.get(awal+dt.timedelta(days=i),0) for i in range(N)]
        r={'nama':n,'total':sum(deret),'N':N,'pertama':first.isoformat(),'terakhir':last.isoformat(),'tanpa_jual':(akhir-last).days}
        if (akhir-first).days+1<14:
            hari=(akhir-first).days+1; tot=sum(q for t,q in d.items() if t>=first)
            r.update(kelompok='DATA_BELUM_CUKUP',hari_amat=hari,terjual=tot,laju=tot/hari)
            s=stok.get(n); 
            if s is not None: r['habis_laju_sementara']=math.floor(s/(tot/hari))
            out[n]=r; continue
        isi=[x for x in deret if x>0]; med=st.median(isi)
        lonj=[(awal+dt.timedelta(days=i)).isoformat() for i,x in enumerate(deret) if x>=4*med and x>=med+10]
        r['lonjakan']=lonj; r['median_hari_laku']=med
        if abaikan_lonjakan:
            deret=[med if (x>=4*med and x>=med+10) else x for x in deret]
        mu=sum(deret)/N; sd=st.stdev(deret)
        mu28=sum(deret[-28:])/28; f=mu28/mu
        tren='naik' if f>=1.2 else 'turun' if f<=0.8 else 'stabil'
        fp=min(max(f,0.5),1.5) if tren!='stabil' else 1.0
        mup=mu*fp; sdp=sd*fp
        r.update(mu=mu,sd=sd,mu28=mu28,faktor=f,tren=tren,f_pakai=fp,mu_p=mup,sd_p=sdp)
        if r['tanpa_jual']>=60:
            r['kelompok']='BARANG_MATI'; s=stok.get(n); r['modal_tertahan']=s*harga[n] if s is not None else None; out[n]=r; continue
        L=lead[n]
        ss=z*sdp*math.sqrt(L); rop=mup*L+ss; T=mup*(L+horizon)+ss
        r.update(ss_x=ss,rop_x=rop,T_x=T,SS=math.ceil(ss-1e-12),ROP=math.ceil(rop-1e-12),T=math.ceil(T-1e-12),L=L)
        s=stok.get(n)
        if s is None: r['kelompok']='STOK_BELUM_DIKETAHUI'; out[n]=r; continue
        habis=math.floor(s/mup); r['habis']=habis; r['tgl_habis']=(acuan+dt.timedelta(days=habis)).isoformat()
        pos=s
        hk=0 if pos<=r['ROP'] else math.floor((pos-r['ROP'])/mup)
        r['hari_ke_rop']=hk
        if hk<1:
            r['kelompok']='PESAN_SEKARANG'; kurang=r['T']-pos; r['kosong_sebelum_datang']=habis<L
        elif hk<=7:
            r['kelompok']='PESAN_MINGGU_DEPAN'; kurang=r['T']-(pos-mup*hk); r['tgl_pesan']=(acuan+dt.timedelta(days=hk)).isoformat()
        else:
            r['kelompok']='AMAN'; r['tgl_pesan_berikut']=(acuan+dt.timedelta(days=hk)).isoformat()
            if habis>90: r['stok_berlebih']=True; r['kelebihan']=s-r['T']; r['nilai_kelebihan']=round((s-r['T'])*harga[n])
            out[n]=r; continue
        q=math.ceil(kurang-1e-12); r['qty_hitung']=q
        k=kel.get(n) or 1
        q2=math.ceil(q/k)*k; r['qty']=q2; r['dus']=q2//k if kel.get(n) else None; r['nilai']=q2*harga[n]
        out[n]=r
    return out
```
</details>
