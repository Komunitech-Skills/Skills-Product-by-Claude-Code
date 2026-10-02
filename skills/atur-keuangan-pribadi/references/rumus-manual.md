# Rumus Manual (bila script tidak bisa dijalankan)

Semua rumus di bawah sama persis dengan yang dipakai `scripts/keuangan.py`. Tunjukkan langkah hitung ke pengguna; jangan membulatkan di tengah jalan kecuali disebut.

## Aturan pembulatan
- Bunga bulanan utang: dibulatkan ke **rupiah terdekat** (0,5 ke atas) setiap bulan.
- Pemasukan musiman per bulan (THR/bonus ÷ 12): dibulatkan **ke bawah** (konservatif).
- Tabungan bulanan yang dibutuhkan: dibulatkan **ke atas** (agar target tidak kurang Rp1).
- Lama mencapai target dana darurat: bulan dibulatkan **ke atas**.

## 1. Anggaran zero-based
```
Pemasukan/bulan = Σ pemasukan bersih rutin + floor(Σ pemasukan tahunan ÷ 12)
Sisa            = Pemasukan/bulan − Σ semua pos
Target          : Sisa = Rp0 (setiap rupiah punya tugas)
Pola 50/30/20   : Batas kebutuhan = 50% × Pemasukan; keinginan 30%; tabungan 20%
Sisa rutin      = Σ pemasukan bersih rutin − Σ semua pos   ← batas setoran/transfer BULANAN
THR/bonus       = disetor SEKALIGUS saat cair (nominal penuh), tidak ditambahkan lagi ke setoran bulanan
Bila sisa rutin < 0: kekurangan/bulan ditambal THR; THR cukup floor(THR ÷ kekurangan) bulan
Rasio cicilan   = Σ cicilan ÷ Pemasukan RUTIN (tanpa THR/12) × 100%   (patokan umum ≤ 30%)
```
Contoh: gaji 7.500.000; THR 7.500.000 + bonus 5.000.000 → 12.500.000 ÷ 12 = 1.041.666,67 → **1.041.666**. Pemasukan/bulan = 8.541.666 (gambaran setahun).

Contoh THR jangan dihitung dua kali: gaji 12.500.000, pos 11.670.000, THR 12.500.000 → sisa rutin **830.000/bulan** (inilah setoran bulanan) + THR **12.500.000 sekali saat cair**. Salah: memindah 1.871.666/bulan (830.000 + THR/12) **dan** menyimpan THR lagi. Rasio cicilan 4.300.000 ÷ 12.500.000 = **34,4%** (bukan 31,8% terhadap 13.541.666).

## 2. Dana darurat
```
Pokok/bulan = kebutuhan wajib + SEMUA cicilan/utang minimum (PayLater, kartu kredit, KPR, motor, KTA, pinjol)
              + kiriman keluarga yang tidak bisa ditunda (bukan jajan/hiburan/top-up investasi)
Target      = Pengeluaran pokok/bulan × N bulan
              (PNS 3–6 | lajang 3–6 | menikah 6–9 | punya anak/tanggungan 9–12 | pekerja lepas/usaha 12)
Kekurangan  = max(Target − Saldo, 0)
Lama (bulan)= ceil(Kekurangan ÷ Setoran/bulan)      (Setoran = dari gaji saja)
Dengan THR  : bulan m terkecil dengan Setoran × m + THR × (jumlah THR cair s.d. bulan m) ≥ Kekurangan
Progres     = Saldo ÷ Target × 100%
```
Contoh: pokok 4.500.000, status punya anak (9 bulan) → 40.500.000; saldo 6.000.000, setor 750.000 → 34.500.000 ÷ 750.000 = **46 bulan**.

## 3. Bunga per bulan dari berbagai satuan
```
Per tahun  : bunga/bulan = % per tahun ÷ 12        (24%/th → 2%/bln)
Per bulan  : langsung                               (1,75%/bln)
Per hari   : bunga/bulan = % per hari × 30          (0,1%/hari → 3%/bln)
```

## 4. Pelunasan utang (bunga efektif = dari sisa saldo)
Untuk tiap bulan:
```
1. Bunga_i   = round(Saldo_i × bunga_bulanan_i)      untuk setiap utang yang belum lunas
2. Saldo_i   = Saldo_i + Bunga_i
3. Bayar minimum ke setiap utang: min(Minimum_i, Saldo_i)
4. Sisa anggaran (anggaran − total yang sudah dibayar) → utang PRIORITAS pertama yang belum lunas,
   kelebihannya ke prioritas berikutnya
5. Anggaran tetap tiap bulan → cicilan minimum utang yang sudah lunas otomatis "menggelinding"
```
- **Avalanche:** prioritas = bunga bulanan tertinggi dulu (seri → saldo lebih kecil dulu).
- **Snowball:** prioritas = saldo awal terkecil dulu (seri → bunga lebih tinggi dulu).
- Tidak akan lunas bila: Minimum ≤ Bunga bulan pertama (untuk utang itu saja) atau Anggaran ≤ total bunga bulan pertama.

Contoh satu utang: saldo 1.000.000, 2%/bln, bayar 300.000/bln.
| Bulan | Bunga | Bayar | Sisa |
|---:|---:|---:|---:|
| 1 | 20.000 | 300.000 | 720.000 |
| 2 | 14.400 | 300.000 | 434.400 |
| 3 | 8.688 | 300.000 | 143.088 |
| 4 | 2.862 (2.861,76) | 145.950 | 0 |
Total bunga **45.950**, lunas bulan ke-4.

## 5. Flat → efektif
```
Cicilan flat   = Pokok ÷ Tenor + Pokok × bunga_flat_tahunan ÷ 12
Total bunga    = Cicilan × Tenor − Pokok
Bunga efektif r (per bulan) = r yang memenuhi  Pokok = Cicilan × (1 − (1+r)^−Tenor) ÷ r
                  (dicari coba-coba/bisection; di spreadsheet: =RATE(Tenor; −Cicilan; Pokok))
Efektif per tahun = r × 12
Perkiraan sisa pokok setelah k kali bayar = Cicilan × (1 − (1+r)^−(Tenor−k)) ÷ r
```
Contoh: 10.000.000, flat 10%/th, 12 bulan → cicilan 833.333 + 83.333 = **916.667** → efektif ≈ **17,97%/th**.
Contoh: 18.000.000, flat 12%/th, 24 bulan → cicilan **930.000** → efektif ≈ **21,57%/th**.

Mengapa flat terlihat murah: bunga flat dihitung dari **pokok awal** sepanjang tenor, padahal pokok yang Anda pinjam terus berkurang. Karena itu bunga efektifnya hampir dua kali angka flat.

## 6. Target keuangan (nilai waktu uang sederhana)
```
i = inflasi_tahunan ÷ 12        r = imbal_hasil_tahunan ÷ 12        n = jumlah bulan
Biaya nanti      = round(Biaya hari ini × (1 + i)^n)
Terkumpul nanti  = Terkumpul × (1 + r)^n
Tabungan/bulan   = ceil( (Biaya nanti − Terkumpul nanti) × r ÷ ((1 + r)^n − 1) )     (setor akhir bulan)
Jika r = 0       : ceil( (Biaya nanti − Terkumpul) ÷ n )
Pensiun          : Biaya hari ini = Pengeluaran bulanan × 12 × lama pensiun (tahun)
                   (asumsi: selama pensiun imbal hasil = inflasi)
```
Di spreadsheet: `=PMT(r; n; Terkumpul; −Biaya_nanti)` (hasil negatif = setoran).

Contoh: DP rumah 60.000.000 hari ini, 5 tahun (60 bulan), inflasi 4%, imbal 5%, sudah ada 10.000.000 →
biaya nanti **73.259.796**; tabungan 10 jt tumbuh jadi 12.833.587; butuh **888.542/bulan**.

Semua angka inflasi & imbal hasil adalah **asumsi** yang disebut terang-terangan, bukan janji atau rekomendasi produk.
