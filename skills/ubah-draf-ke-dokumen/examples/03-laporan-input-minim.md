# Skenario 3: input tidak lengkap (satu kalimat jadi laporan)

- **Tanggal uji:** 2026-10-12 (OpenClaw 2026.9.6 lokal, model claude-sonnet-5; detail sebelum/sesudah lengkap di `00-openclaw-sebelum-sesudah.md`)
- **Data pesan:** `data/pesan-3-laporan-minim.txt`

## Input (pesan pengguna)

```
Tolong jadikan ini laporan resmi buat atasan saya: bulan ini penjualan lumayan, ada kendala pengiriman, tim kerja bagus.
```

## Output SESUDAH (skill aktif)

> # LAPORAN BULANAN PENJUALAN DAN OPERASIONAL
>
> [isi kop usaha — nama usaha, alamat, kontak]
>
> **Kepada Yth.:** [isi: nama/jabatan atasan]
> **Dari:** [isi: nama/jabatan pelapor]
> **Periode:** Oktober 2026
> **Tanggal:** 12 Oktober 2026
>
> ---
>
> ## I. Ringkasan Eksekutif
>
> Secara umum, kinerja bulan ini menunjukkan hasil yang cukup baik. Penjualan tercatat lumayan meningkat dibandingkan periode sebelumnya, meskipun terdapat kendala pada proses pengiriman yang perlu mendapat perhatian. Di sisi lain, kinerja tim kerja berjalan dengan baik dan menjadi faktor pendukung utama pencapaian bulan ini.
>
> ## II. Penjualan
>
> Penjualan bulan ini berada pada level yang cukup baik dan menunjukkan tren positif. [isi: angka/persentase penjualan jika tersedia, misal nilai omzet atau perbandingan dengan bulan sebelumnya].
>
> ## III. Kendala Pengiriman
>
> Terdapat kendala pada proses pengiriman yang berdampak pada [isi: dampak kendala — misal keterlambatan, komplain pelanggan, biaya tambahan]. Kendala ini perlu ditindaklanjuti agar tidak berulang pada periode berikutnya.
>
> **Tindak lanjut yang diusulkan:**
> - [isi: langkah perbaikan, misal evaluasi mitra ekspedisi]
> - [isi: langkah perbaikan tambahan]
>
> ## IV. Kinerja Tim
>
> Tim kerja menunjukkan performa yang baik sepanjang bulan ini, dengan koordinasi dan tanggung jawab yang terjaga dalam menjalankan operasional sehari-hari.
>
> ## V. Kesimpulan dan Rekomendasi
>
> Secara keseluruhan, bulan ini mencatatkan hasil yang positif dari sisi penjualan dan kinerja tim, dengan satu area yang perlu perbaikan yaitu proses pengiriman. Direkomendasikan agar kendala pengiriman segera dievaluasi agar tidak mempengaruhi kepuasan pelanggan pada periode berikutnya.
>
> Demikian laporan ini disampaikan untuk menjadi bahan evaluasi dan tindak lanjut.
>
> Hormat kami,
>
> [Nama, Jabatan]
>
> ---
>
> **Perubahan yang dilakukan:**
> - Mengubah poin singkat menjadi laporan formal berstruktur (judul, periode, ringkasan eksekutif, isi per bab, kesimpulan)
> - Menambahkan bagian "Tindak Lanjut" untuk kendala pengiriman agar laporan lebih actionable
> - Menambahkan placeholder `[isi: ...]` untuk data yang belum ada di draf (angka penjualan, detail kendala, nama/jabatan)
> - Menyusun format kop, penerima, dan tanda tangan sesuai standar laporan resmi
>
> **Asumsi & pertanyaan (maks. 3):**
> 1. Siapa nama/jabatan atasan penerima laporan, dan nama/jabatan Anda sebagai pelapor?
> 2. Ada angka konkret untuk penjualan (nominal/persentase kenaikan) dan detail kendala pengiriman (apa penyebabnya) yang ingin dicantumkan?
> 3. Perlu kop usaha (nama, alamat, kontak) resmi, atau biarkan sebagai placeholder?
>
> Isi lengkap sudah ada di atas. Kalau perlu file Word, balas 'kirim file' — saya coba lampirkan.

## Catatan

- Skor SEBELUM 5,5 -> SESUDAH 7,5. Bekerja dulu dengan `[isi: ...]` untuk angka/dampak/nama dan tepat 3 pertanyaan di akhir.
- Cacat: "meningkat dibandingkan periode sebelumnya" dan "tren positif" bukan dari draf; periode Oktober 2026 diasumsikan.
