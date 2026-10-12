# Skenario 3: input tidak lengkap (satu kalimat jadi laporan resmi)

- **Tanggal uji:** 2026-10-12 (versi 1.0.1; OpenClaw 2026.9.6 lokal, model claude-sonnet-5; detail sebelum/sesudah lengkap di `00-openclaw-sebelum-sesudah.md`)
- **Data pesan:** `data/pesan-3-laporan-minim.txt`

## Input (pesan pengguna)

```
Tolong jadikan ini laporan resmi buat atasan saya: bulan ini penjualan lumayan, ada kendala pengiriman, tim kerja bagus.
```

## Output SESUDAH (skill aktif) - biasa

> Laporan Oktober 2026 ini saya susun jadi dokumen resmi siap salin. Karena belum ada data detail (angka penjualan, jenis kendala pengiriman, dll.), saya pakai placeholder `[isi: ...]` di bagian yang perlu dilengkapi — tidak saya karang.
>
> ---
>
> **[isi kop usaha: Nama Usaha, Alamat, Kontak]**
> ────────────────────────────────────────
>
> **LAPORAN BULANAN**
> **Bulan: Oktober 2026**
>
> Kepada Yth.
> [isi: Nama/Jabatan Atasan]
> di tempat
>
> Dari: [isi: Nama Pelapor/Jabatan]
> Perihal: Laporan Kinerja Bulan Oktober 2026
>
> Dengan hormat,
>
> Bersama ini kami sampaikan laporan perkembangan usaha untuk bulan Oktober 2026 sebagai berikut:
>
> **1. Penjualan**
> Penjualan bulan ini berjalan cukup baik dengan tren yang positif. [isi: rincian angka penjualan/omzet bila ingin dicantumkan, mis. Rp___ atau jumlah unit terjual]
>
> **2. Kendala Operasional**
> Terdapat kendala pada proses pengiriman barang kepada pelanggan. [isi: detail kendala, misalnya keterlambatan ekspedisi, kapasitas armada, atau wilayah yang terdampak] Hal ini menjadi perhatian untuk ditindaklanjuti agar tidak berulang pada bulan berikutnya.
>
> **3. Kinerja Tim**
> Tim kerja menunjukkan performa yang baik sepanjang bulan ini, dengan koordinasi dan dedikasi yang mendukung kelancaran operasional usaha.
>
> **4. Penutup**
> Demikian laporan ini kami sampaikan sebagai bahan evaluasi dan tindak lanjut. Kami terbuka terhadap arahan lebih lanjut, khususnya terkait penyelesaian kendala pengiriman di atas.
>
> Hormat kami,
>
> [Nama, Jabatan]
>
> ---
>
> Daftar perubahan yang saya rapikan:
> - Mengubah 3 poin singkat jadi struktur laporan resmi (kop, judul, perihal, isi bernomor, penutup, tanda tangan).
> - Memisahkan isi jadi 3 bagian: Penjualan, Kendala Operasional, Kinerja Tim.
> - Menambahkan placeholder `[isi: ...]` untuk data yang belum ada (nama atasan/pelapor, angka penjualan, detail kendala pengiriman) — tidak saya karang angkanya.
> - Menambahkan kalimat penutup formal yang mengarah ke tindak lanjut kendala pengiriman.
>
> Asumsi & pertanyaan (maks. 3):
> 1. Siapa nama/jabatan atasan yang dituju, dan nama/jabatan Anda sebagai pelapor?
> 2. Apakah ada angka penjualan (Rp atau unit) yang ingin dicantumkan, atau tetap kualitatif seperti draf?
> 3. Mau saya tambahkan kop usaha asli (nama, alamat, kontak)?
>
> Isi lengkap sudah ada di atas. Kalau perlu file Word, balas 'kirim file' — saya coba lampirkan.

## Catatan penguji
- Skor: SEBELUM 5,0 -> SESUDAH 7,0.
- Kerja dulu, placeholder `[isi: ...]`, 3 pertanyaan di akhir: baik.
- Karangan kecil yang tersisa: "tren yang positif", "koordinasi dan dedikasi yang mendukung kelancaran operasional", "menjadi perhatian untuk ditindaklanjuti agar tidak berulang". Bertentangan dengan aturan "dilarang menambah klaim kualitatif".

