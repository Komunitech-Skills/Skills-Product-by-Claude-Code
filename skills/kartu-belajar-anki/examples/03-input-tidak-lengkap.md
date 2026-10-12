# Skenario 3: input kurang

**Input:** `bikinin kartu belajar`

## Output SESUDAH (skill aktif, kartu-belajar-anki 1.0.1)

> Belum ada materi yang ditempel, jadi ini **contoh deck fiktif** (topik dasar usaha UMKM) sambil nunggu materi aslinya.
>
> **Ringkasan:** 10 kartu basic, tag `umkm-dasar` / `umkm-keuangan` / `umkm-legalitas`, asumsi: materi umum seputar dasar usaha kecil karena belum ada bahan spesifik.
>
> **Pratinjau:**
>
> | Depan | Belakang | Tag |
> |---|---|---|
> | Apa itu modal kerja? | Dana untuk operasional sehari-hari | umkm-dasar |
> | Apa bedanya omzet dan laba? | Omzet = total penjualan; laba = omzet - biaya | umkm-dasar |
> | Apa itu BEP? | Titik impas, pendapatan = biaya | umkm-keuangan |
> | Apa itu NIB? | Identitas resmi usaha dari OSS | umkm-legalitas |
> | Kenapa perlu NPWP? | Untuk pajak & syarat tender/pinjaman | umkm-legalitas |
>
> **Rencana belajar:** 10 kartu, 20 menit/hari → 10 kartu baru selesai dalam **1 hari**; setelah itu cukup 5–10 menit review per hari.
>
> **Kartu lengkap (TSV, siap tempel ke file .tsv):**
> ```
> Apa itu modal kerja dalam usaha kecil?	Dana yang dipakai untuk operasional sehari-hari (stok, bahan baku, gaji)	umkm-dasar
> Apa bedanya omzet dan laba?	Omzet = total penjualan; laba = omzet dikurangi semua biaya	umkm-dasar
> Apa fungsi buku kas harian?	Mencatat semua uang masuk dan keluar setiap hari	umkm-dasar
> Kapan sebaiknya memisahkan rekening pribadi dan usaha?	Sejak awal usaha berjalan, agar keuangan tidak tercampur	umkm-dasar
> Apa itu BEP (Break Even Point)?	Titik impas — saat total pendapatan sama dengan total biaya	umkm-keuangan
> Apa itu markup harga?	Tambahan persentase di atas harga modal untuk menentukan harga jual	umkm-keuangan
> Apa tujuan membuat laporan laba rugi sederhana?	Mengetahui apakah usaha untung atau rugi dalam periode tertentu	umkm-keuangan
> Apa itu piutang usaha?	Uang yang belum dibayar pelanggan atas barang/jasa yang sudah diterima	umkm-keuangan
> Apa itu NIB (Nomor Induk Berusaha)?	Identitas resmi pelaku usaha yang diterbitkan lewat OSS	umkm-legalitas
> Kenapa UMKM perlu NPWP?	Untuk keperluan pajak dan syarat ikut tender/pinjaman	umkm-legalitas
> ```
>
> **Cara impor:** Anki → File → Import → pilih file → pemisah **Tab** → kolom 1 = Front, kolom 2 = Back, kolom 3 = Tags → Import.
>
> Biar bisa bikin yang beneran sesuai kebutuhan, tolong balas dengan:
> 1. **Materi aslinya** (tempel catatan/istilah/SOP yang mau dihafal)
> 2. **Tujuan belajar** (CPNS, sertifikasi, SOP karyawan, bahasa, dll — atau "umum" aja)
> 3. **Jenis kartu**: basic (tanya-jawab) atau cloze (isian kalimat)?

## Catatan penguji

- Deck contoh fiktif 10 kartu diberi label jelas; validasi ok (`data/v101-sesudah-3-contoh.tsv`); rencana 1 hari: cocok.
- **Cacat:** tidak ada "contoh isian siap balas (3 baris)" seperti diminta SKILL.md; hanya 3 pertanyaan bernomor.
- Nilai: SESUDAH 7,5 (SEBELUM 5,5).

Rincian dua sisi: `00-openclaw-sebelum-sesudah.md`.
