# Skenario 2: notulen rapat dengan tabel tindak lanjut (normal kedua)

- **Tanggal uji:** 2026-10-12 (OpenClaw 2026.9.6 lokal, model claude-sonnet-5; detail sebelum/sesudah lengkap di `00-openclaw-sebelum-sesudah.md`)
- **Data pesan:** `data/pesan-2-notulen.txt`

## Input (pesan pengguna)

```
notulen rapat tim ya, tolong rapikan jadi dokumen notulen formal, ada tabel tindak lanjutnya.

rapat evaluasi bulanan Jumat 2 Okt 2026 jam 14.00-15.30 di ruang meeting lt 2 CV Maju Sentosa.
hadir: Pak Hendra (direktur) pimpin, Bu Ratna (keuangan), Dimas (gudang), Sinta (marketing), notulis saya Wulan.
bahasan:
1. penjualan sept Rp186.400.000 naik 8% dari agustus, terbesar dari toko online
2. stok gudang: kardus kemasan menipis tinggal sekitar 2 minggu, perlu pesan ulang. Dimas yg urus pesan ke supplier paling lambat 8 okt
3. Sinta mau bikin promo harbolnas 11.11, materi iklan selesai tgl 24 okt
4. Bu Ratna bilang piutang 3 pelanggan blm lunas total Rp27.500.000, ditagih minggu depan - belum ditentuin siapa yg nagih
keputusan: promo disetujui, anggaran iklan Rp5.000.000
rapat berikutnya awal November, tanggal belum fix
```

## Output SESUDAH (skill aktif)

> # NOTULEN RAPAT EVALUASI BULANAN
>
> **CV MAJU SENTOSA**
> [isi: alamat lengkap] · [isi: nomor telepon] · [isi: email]
> ────────────────────────────────────────
>
> ## I. Keterangan Umum
>
> | Keterangan | Detail |
> |---|---|
> | Agenda | Rapat Evaluasi Bulanan |
> | Hari/Tanggal | Jumat, 2 Oktober 2026 |
> | Waktu | 14.00 – 15.30 WIB |
> | Tempat | Ruang Meeting Lantai 2, CV Maju Sentosa |
> | Pemimpin Rapat | Bapak Hendra (Direktur) |
> | Notulis | Wulan |
>
> ## II. Peserta yang Hadir
>
> 1. Bapak Hendra — Direktur (Pemimpin Rapat)
> 2. Ibu Ratna — Bagian Keuangan
> 3. Dimas — Bagian Gudang
> 4. Sinta — Bagian Marketing
>
> ## III. Pembahasan
>
> **1. Evaluasi Penjualan Bulan September**
> Penjualan bulan September 2026 tercatat sebesar Rp186.400.000, naik 8% dibandingkan bulan Agustus. Kontribusi terbesar berasal dari penjualan melalui toko online.
>
> **2. Kondisi Stok Gudang**
> Stok kardus kemasan di gudang menipis dan diperkirakan hanya cukup untuk sekitar 2 minggu ke depan. Diperlukan pemesanan ulang segera kepada supplier. Dimas ditugaskan untuk mengurus pemesanan tersebut, paling lambat tanggal 8 Oktober 2026.
>
> **3. Rencana Promo Harbolnas 11.11**
> Sinta mengusulkan rencana promo dalam rangka Harbolnas (11.11). Materi iklan ditargetkan selesai pada tanggal 24 Oktober 2026.
>
> **4. Piutang Pelanggan**
> Ibu Ratna melaporkan bahwa piutang dari 3 pelanggan belum lunas, dengan total Rp27.500.000. Penagihan direncanakan dilakukan minggu depan, namun penanggung jawab penagihan belum ditentukan dalam rapat ini.
>
> ## IV. Keputusan Rapat
>
> 1. Rencana promo Harbolnas 11.11 **disetujui**.
> 2. Anggaran untuk iklan promo ditetapkan sebesar **Rp5.000.000**.
>
> ## V. Tindak Lanjut
>
> | No | Tindak Lanjut | Penanggung Jawab | Tenggat Waktu | Keterangan |
> |---|---|---|---|---|
> | 1 | Memesan ulang kardus kemasan ke supplier | Dimas | Paling lambat 8 Oktober 2026 | Stok menipis, sisa ±2 minggu |
> | 2 | Menyelesaikan materi iklan promo Harbolnas 11.11 | Sinta | 24 Oktober 2026 | Anggaran Rp5.000.000 telah disetujui |
> | 3 | Menagih piutang 3 pelanggan (total Rp27.500.000) | [isi: belum ditentukan] | Minggu depan | PIC penagihan perlu ditentukan |
> | 4 | Menjadwalkan rapat evaluasi bulan November | [isi: belum ditentukan] | [isi: tanggal belum fix] | Rapat berikutnya awal November |
>
> ## VI. Penutup
>
> Rapat ditutup pukul 15.30 WIB. Demikian notulen ini dibuat untuk digunakan sebagaimana mestinya.
>
> Mengetahui,
>
> [Hendra, Direktur]					[Wulan, Notulis]
>
> ---
>
> **Perubahan yang dirapikan:**
> - Disusun dalam format notulen resmi dengan kop, bagian keterangan umum, peserta, pembahasan bernomor, keputusan, dan tabel tindak lanjut.
> - Tabel tindak lanjut dibuat dengan kolom PIC, tenggat, dan keterangan agar mudah dipantau.
> - Bagian yang belum jelas dari draf (PIC penagihan piutang, tanggal rapat berikutnya, alamat/kontak perusahaan) ditandai `[isi: ...]`, bukan dikarang.
> - Format tanggal dan Rupiah dirapikan sesuai EYD (contoh: "Rp186.400.000", "2 Oktober 2026").
>
> **Asumsi & pertanyaan:**
> 1. Alamat/telepon/email CV Maju Sentosa untuk kop belum saya isi — boleh dikirim datanya?
> 2. Siapa yang akan menagih piutang 3 pelanggan tersebut?
> 3. Apakah tanggal pasti rapat bulan November sudah ada, atau tetap dibiarkan "belum fix" di dokumen?
>
> Isi lengkap sudah ada di atas. Kalau perlu file Word, balas 'kirim file' — saya coba lampirkan.

## Catatan

- Skor SEBELUM 5 -> SESUDAH 8,5. Semua angka (Rp186.400.000, 8%, Rp27.500.000, Rp5.000.000), nama, tanggal (2 Oktober, 8 Oktober, 24 Oktober 2026) benar.
- Hal yang belum diputuskan (PIC penagihan, tanggal rapat November) ditandai `[isi: ...]`, tidak dikarang. Tanpa skill: PIC dan tenggat ditebak, dan dokumen hanya di file (2 dari 2 run).
- Cacat kecil: butir tindak lanjut ke-4 ditambah sendiri.
