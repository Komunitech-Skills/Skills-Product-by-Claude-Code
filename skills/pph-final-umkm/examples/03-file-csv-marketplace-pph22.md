# 03 — Dari file CSV, penjual marketplace dengan PPh 22

**Skenario:** S3 — permintaan normal dengan file. Penjual Shopee perorangan; Agustus–September sudah dipotong PPh 22 marketplace.

**Input pengguna (persis):**
> Ini rekap omzet saya dari Seller Center, saya simpan di omzet-2026.csv. Agustus sama September kepotong PPh 22 sama Shopee. Tolong hitungin PPh final saya, saya pribadi.

**Isi file `omzet-2026.csv` (fiktif):**
```
bulan;omzet;pph22
Januari;Rp 41.250.000;
Februari;Rp 39.800.000;
Maret;Rp 52.300.000;
April;Rp 48.900.000;
Mei;Rp 57.150.000;
Juni;Rp 63.400.000;
Juli;Rp 66.000.000;
Agustus;Rp 71.500.000;Rp 357.500
September;Rp 78.200.000;Rp 391.000
```

**Perintah yang dijalankan agent:**
```bash
python3 <folder-skill>/scripts/pph_final.py --jenis op --tahun 2026 --file omzet-2026.csv
```

## Output

## PPh Final UMKM 0,5% - Tahun 2026 (Orang pribadi)

| Bulan | Omzet | Omzet kumulatif | Omzet kena pajak | PPh final 0,5% | PPh 22 marketplace (info) | Setor paling lambat | Keterangan |
|---|---:|---:|---:|---:|---:|---|---|
| Januari | Rp 41.250.000 | Rp 41.250.000 | Rp 0 | Rp 0 | - | 2026-02-15 | masih dalam Rp500 juta bebas |
| Februari | Rp 39.800.000 | Rp 81.050.000 | Rp 0 | Rp 0 | - | 2026-03-15 | masih dalam Rp500 juta bebas |
| Maret | Rp 52.300.000 | Rp 133.350.000 | Rp 0 | Rp 0 | - | 2026-04-15 | masih dalam Rp500 juta bebas |
| April | Rp 48.900.000 | Rp 182.250.000 | Rp 0 | Rp 0 | - | 2026-05-15 | masih dalam Rp500 juta bebas |
| Mei | Rp 57.150.000 | Rp 239.400.000 | Rp 0 | Rp 0 | - | 2026-06-15 | masih dalam Rp500 juta bebas |
| Juni | Rp 63.400.000 | Rp 302.800.000 | Rp 0 | Rp 0 | - | 2026-07-15 | masih dalam Rp500 juta bebas |
| Juli | Rp 66.000.000 | Rp 368.800.000 | Rp 0 | Rp 0 | - | 2026-08-15 | masih dalam Rp500 juta bebas |
| Agustus | Rp 71.500.000 | Rp 440.300.000 | Rp 0 | Rp 0 | Rp 357.500 | 2026-09-15 | masih dalam Rp500 juta bebas |
| September | Rp 78.200.000 | Rp 518.500.000 | Rp 18.500.000 | Rp 92.500 | Rp 391.000 | 2026-10-15 | melewati Rp500 juta; hanya Rp 18.500.000 yang kena pajak |
| **Total** | **Rp 518.500.000** | | | **Rp 92.500** | Rp 748.500 | | |

**Ringkasan**
- Omzet kumulatif tahun 2026: Rp 518.500.000
- Total PPh final periode ini: Rp 92.500
- Batas Rp500 juta bebas pajak sudah terlewati (September).
- Sisa ruang sebelum batas Rp4,8 miliar: Rp 4.281.500.000

**Catatan penting**
- Orang pribadi: omzet s.d. Rp500 juta setahun tidak dikenai PPh final. Batas ini untuk total omzet SEMUA usaha Anda dalam setahun.
- PPh 22 marketplace yang tercatat (Rp 748.500) hanya informasi. DJP menyebut pungutan ini bukan pajak baru dan dapat diperhitungkan, tetapi cara memperhitungkannya dengan PPh final Anda perlu dicek ke DJP/konsultan. Angka PPh final di atas BELUM dikurangi PPh 22.
- Tarif 0,5% dihitung dari OMZET (peredaran bruto), bukan dari laba.
- Pembulatan: PPh tiap bulan dibulatkan ke bawah ke rupiah penuh (pecahan rupiah dibuang).
- Batas setor tercantum = tanggal 15 bulan berikutnya (ketentuan umum PMK 81/2024); cek DJP bila jatuh di hari libur.
- PP 20/2026: ketentuan masa transisi untuk CV/firma/PT dan batas jangka waktu pemakaian tarif 0,5% belum kami verifikasi. Cek pajak.go.id atau Kring Pajak 1500200 sebelum mengambil keputusan.
- Tidak berlaku untuk penghasilan dari jasa pekerjaan bebas (mis. dokter, notaris, konsultan) dan penghasilan lain yang dikecualikan PP 55/2022.

_Dasar: PP 55/2022 jo. PP 20/2026 (PPh Final UMKM 0,5%); PMK 37/2025 (PPh 22 marketplace). Berlaku per 2026-09-23. Ini alat bantu hitung, bukan nasihat pajak. Untuk kepastian, hubungi DJP (Kring Pajak 1500200 / pajak.go.id) atau konsultan pajak._

**Penjelasan singkat:**
- Omzet kumulatif Anda baru melewati Rp500 juta di **September** (Rp518,5 juta), jadi PPh final September hanya atas Rp18,5 juta → **Rp92.500**, setor paling lambat 15 Oktober 2026.
- Shopee sudah memungut PPh 22 total **Rp748.500** (Agustus–September). Angka PPh final di atas **belum** dikurangi PPh 22 itu; cara memperhitungkannya (apakah bisa mengurangi PPh final, atau diperhitungkan di SPT) perlu dipastikan ke DJP/konsultan.
- Pelajaran untuk tahun depan: selama omzet setahun masih ≤ Rp500 juta, penjual orang pribadi bisa dikecualikan dari pungutan PPh 22 dengan **menyampaikan surat pernyataan** ke marketplace. Karena Agustus Anda masih di bawah Rp500 juta, pungutan Rp357.500 itu sebenarnya bisa dihindari bila surat pernyataan sudah diserahkan.

## Catatan penguji
- CSV dengan format "Rp 41.250.000" dan kolom PPh 22 kosong terbaca benar. Angka dicek independen: kumulatif s.d. Agustus 440,3 jt; September 518,5 jt → kena 18,5 jt → Rp92.500. PPh 22 Agustus = 0,5% × 71,5 jt = 357.500 (konsisten).
- PPh 22 tidak dikurangkan otomatis dan tidak dinyatakan pasti bisa dikreditkan — sesuai checklist.
- Saran surat pernyataan disusun agent dari `references/regulasi.md` (berstatus terverifikasi di dokumen skill).
