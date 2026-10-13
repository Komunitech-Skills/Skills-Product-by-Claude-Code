# Skenario 2: notulen rapat dengan tabel tindak lanjut (normal kedua)

- **Tanggal uji:** 2026-10-12 (versi 1.0.1; OpenClaw 2026.9.6 lokal, model claude-sonnet-5; detail sebelum/sesudah lengkap di `00-openclaw-sebelum-sesudah.md`)
- **Data pesan:** `data/pesan-2-notulen.txt`
- **Data fiktif:** Pak Hendra, Bu Ratna, Dimas, Sinta, dan Wulan (nama fiktif), serta CV Maju Sentosa dan angka-angkanya hanya contoh.

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

## Output SESUDAH (skill aktif) - biasa

> Berikut notulen rapat yang sudah dirapikan — tinggal salin ke Word:
>
> ---
>
> **CV MAJU SENTOSA**
> [isi: alamat lengkap] · [isi: kota, kode pos]
> Tel. [isi: nomor] · [isi: email] · [isi: website opsional]
> ────────────────────────────────────────
>
> # NOTULEN RAPAT EVALUASI BULANAN
>
> **Hari/Tanggal:** Jumat, 2 Oktober 2026
> **Waktu:** 14.00 – 15.30 WIB
> **Tempat:** Ruang Meeting Lantai 2, CV Maju Sentosa
> **Pimpinan Rapat:** Bapak Hendra (Direktur)
> **Notulis:** Wulan
>
> **Peserta yang hadir:**
> 1. Bapak Hendra — Direktur (memimpin rapat)
> 2. Ibu Ratna — Keuangan
> 3. Dimas — Gudang
> 4. Sinta — Marketing
> 5. Wulan — Notulis
>
> ## 1. Agenda
> 1. Evaluasi penjualan bulan September 2026
> 2. Kondisi stok gudang
> 3. Persiapan promo Harbolnas 11.11
> 4. Status piutang pelanggan
>
> ## 2. Pembahasan
>
> ### 2.1 Evaluasi Penjualan September
> Penjualan bulan September 2026 tercatat sebesar Rp186.400.000, naik 8% dibandingkan bulan Agustus. Kontribusi terbesar berasal dari penjualan melalui toko online.
>
> ### 2.2 Stok Gudang
> Dimas melaporkan bahwa stok kardus kemasan menipis dan diperkirakan hanya cukup untuk sekitar 2 minggu ke depan. Diperlukan pemesanan ulang ke supplier sesegera mungkin.
>
> ### 2.3 Promo Harbolnas 11.11
> Sinta mengusulkan rencana promo untuk Harbolnas (11.11). Materi iklan ditargetkan selesai pada tanggal 24 Oktober 2026.
>
> ### 2.4 Piutang Pelanggan
> Ibu Ratna melaporkan terdapat piutang dari 3 pelanggan dengan total Rp27.500.000 yang belum lunas. Penagihan direncanakan dilakukan minggu depan; penanggung jawab penagihan belum ditentukan dalam rapat.
>
> ## 3. Keputusan
> 1. Promo Harbolnas 11.11 disetujui untuk dijalankan.
> 2. Anggaran iklan promo ditetapkan sebesar Rp5.000.000.
>
> ## 4. Tindak Lanjut
>
> | No | Tindakan | PIC | Tenggat |
> |---|---|---|---|
> | 1 | Memesan ulang stok kardus kemasan ke supplier | Dimas | Paling lambat 8 Oktober 2026 |
> | 2 | Menyelesaikan materi iklan promo Harbolnas 11.11 | Sinta | 24 Oktober 2026 |
> | 3 | Menagih piutang 3 pelanggan (total Rp27.500.000) | [isi: belum ditentukan] | Minggu depan |
>
> ## 5. Penutup
> Rapat ditutup pukul 15.30 WIB. Rapat evaluasi berikutnya dijadwalkan pada awal November 2026, tanggal pasti [isi: belum ditentukan].
>
> Ruang Meeting Lt. 2, 2 Oktober 2026
> Notulis,
>
> Wulan
>
> ---
>
> **Perubahan yang dilakukan:**
> - Ditambahkan kop usaha CV Maju Sentosa (alamat/kontak masih placeholder)
> - Pembahasan dipecah per topik dengan sub-heading (2.1–2.4)
> - Tabel tindak lanjut dibuat dengan PIC dan tenggat
> - Tanggal ditulis format Indonesia, Rupiah diformat konsisten
> - Poin piutang yang belum ada PIC ditandai `[isi: belum ditentukan]`, bukan dikarang
>
> **Asumsi & pertanyaan:**
> 1. Alamat/telepon/email CV Maju Sentosa untuk kop — mau saya isi apa?
> 2. Siapa PIC penagihan piutang 3 pelanggan itu?
> 3. Tanggal pasti rapat berikutnya awal November — sudah ada atau tetap `[isi: belum ditentukan]`?
>
> Isi lengkap sudah ada di atas. Kalau perlu file Word, balas 'kirim file' — saya coba lampirkan.

## Catatan penguji
- Skor: SEBELUM 5,0 -> SESUDAH 8,5.
- Angka/tanggal benar; PIC dan tanggal yang belum diputuskan = `[isi: belum ditentukan]`; tabel 3 baris tanpa butir karangan.
- Karangan kecil: "Dimas melaporkan bahwa ..." (draf tidak menyebut siapa yang melapor stok), "sesegera mungkin".
- SEBELUM hanya menulis file di workspace; isi tidak ada di chat.

