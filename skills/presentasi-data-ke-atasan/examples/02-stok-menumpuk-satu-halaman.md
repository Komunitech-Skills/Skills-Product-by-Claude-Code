# Contoh 2 — Stok Menumpuk, 1 Halaman Eksekutif untuk Owner (Minta Keputusan)

## Input pengguna
> "Bikinkan 1 halaman eksekutif buat owner. Nilai stok gudang naik terus 6 minggu
> terakhir: 18 juta, 24 juta, 29 juta, 33 juta, 37 juta, 41 juta (dalam jutaan rupiah).
> Ini untuk minta keputusan soal stok yang menumpuk."

## Langkah kerja
1. Sumber angka: disebutkan langsung pengguna (deret mingguan).
2. Hitung lewat script:
   ```bash
   python3 scripts/hitung_perubahan.py \
     --pasangan "Nilai stok:18000000:41000000" \
     --daftar "Stok mingguan=18jt,24jt,29jt,33jt,37jt,41jt"
   ```
   Hasil: nilai stok naik dari Rp18.000.000 ke Rp41.000.000 (**+127,8%** dalam 6 minggu);
   total 6 minggu Rp182.000.000, rata-rata Rp30.333.333, minimum Rp18.000.000 (minggu 1),
   maksimum Rp41.000.000 (minggu 6).
   (Revisi 2026-10-13: angka daftar dimasukkan dalam Rupiah penuh/`jt`; versi lama memakai
   satuan juta sehingga rata-rata terbulatkan jadi "Rp30 juta". 182.000.000 ÷ 6 =
   30.333.333,33 → Rp30.333.333.)
3. Kalimat inti: "Nilai stok gudang naik lebih dari 2 kali lipat dalam 6 minggu (Rp18
   juta → Rp41 juta) — perlu keputusan soal barang mana yang ditahan atau didiskon."
4. 3 angka pendukung: nilai stok awal→akhir (+127,8%), rata-rata mingguan (Rp30.333.333),
   kenaikan konsisten 6 minggu berturut-turut (tren, bukan lonjakan sesaat).
5. Grafik: garis 6 titik waktu (mingguan) — tren naik konsisten, judul grafik = "Nilai
   Stok Naik 6 Minggu Berturut-turut", bukan "Nilai Stok per Minggu".
6. Risiko: modal semakin terkunci di stok yang belum terjual; makin lama makin berisiko
   barang usang/kadaluarsa (bila relevan) atau butuh diskon besar untuk dihabiskan.
7. Rekomendasi: audit stok per kategori untuk cari barang paling lambat bergerak +
   pertimbangkan diskon/promo untuk barang tersebut dalam 2 minggu.

## Output — Satu halaman eksekutif
```
Kinerja Stok Gudang — 6 Minggu Terakhir

KESIMPULAN
Nilai stok gudang naik lebih dari 2 kali lipat dalam 6 minggu (Rp18 juta
menjadi Rp41 juta) — perlu keputusan soal barang yang ditahan atau
didiskon sebelum modal makin terkunci.

ANGKA KUNCI
┌───────────────────────┬───────────────────────┬───────────────────────┐
│ Nilai stok saat ini    │ Kenaikan 6 minggu      │ Rata-rata mingguan    │
│ Rp41.000.000           │ +127,8% (dari Rp18jt)  │ Rp30.333.333          │
└───────────────────────┴───────────────────────┴───────────────────────┘

GRAFIK
Grafik garis: Nilai Stok Naik 6 Minggu Berturut-turut (Minggu 1–6, Rp18jt
→ Rp41jt) — 6 titik waktu berurutan, garis naik konsisten tanpa penurunan.

RISIKO
- Modal makin terkunci di stok yang belum terjual; makin lama makin
  berisiko perlu diskon besar untuk dihabiskan, menekan margin ke depan.

REKOMENDASI
1. Audit stok per kategori untuk mengidentifikasi barang paling lambat
   bergerak — PIC: [isian: nama/jabatan], tenggat: 1 minggu.
2. Siapkan promo/diskon untuk barang lambat bergerak hasil audit — PIC:
   [isian: nama/jabatan], tenggat: 2 minggu setelah hasil audit.

────────────────────────────────────────────────────────────────
Sumber data: dilaporkan langsung oleh pengguna (data mingguan gudang).
Periode: 6 minggu terakhir. Dibuat: 2026-09-26.
```

## Asumsi yang disebutkan ke pengguna
- Penerima: owner (sesuai permintaan)
- Kategori barang penyebab stok menumpuk **tidak disebutkan pengguna** — rekomendasi
  #1 sengaja berupa "audit dulu", bukan menyebut kategori barang tertentu, karena data
  itu tidak tersedia (sesuai Batasan: tidak boleh mengarang detail yang tidak ada).
- PIC tidak disebutkan pengguna → ditulis `[isian: nama/jabatan]`, diisi pengguna sebelum
  dikirim.
