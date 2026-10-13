# Riwayat perubahan — strategi-merek-usaha

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Riwayat versi
### Catatan revisi 1.0.4 (2026-10-01)
- Penjelasan "3 konsonan berturut" kini menyebut huruf dan katanya dengan tepat (mis. 'ncl' di 'Kinclong'), sehingga alasan di jawaban tidak lagi keliru menunjuk huruf. Nilai skor tidak berubah.
- Tes regresi bertambah 2.

### Catatan revisi 1.0.3 (2026-10-01)
- Cek nama kini membandingkan **bunyi**, bukan hanya ejaan: nama yang terdengar sama dengan pesaing yang Anda sebut (mis. "Kicks Klin" vs "Kick Clean") langsung ditandai.
- Nama yang terbaca seperti kata Inggris berkonotasi buruk (mis. "Sneakuy" ~ "sneaky" = licik) ditandai dan tidak direkomendasikan.
- Klaim produk (ukuran, bahan, "tanpa pengawet") yang tidak Anda sebut ditulis sebagai `[isi: …]`, bukan dikarang.
- File kerja disimpan di folder kerja Anda (bukan folder skill) dan lokasinya disebutkan; nomor kelas merek (Nice) disebut di jawaban.
- Tes regresi bertambah dari 25 menjadi 28.

### Catatan revisi 1.0.1 (2026-09-30)
- Penghitung penawaran kini membaca nominal format Indonesia (`38.000`, `Rp38.000`, `38rb`, `1,5jt`, `38.000,50`); bentuk ambigu (`38.5`) ditolak dengan pesan jelas, harga sangat kecil diberi peringatan.
- Tabel kelas Nice ditambah kelas 5, 37, 44 dan diperiksa ulang terhadap Nice Classification edisi ke-13 (versi 2026).
- Ringkasan Pasal 17 UU 8/1999 diperjelas: berlaku untuk pelaku usaha periklanan.
- Nama tanpa huruf ditolak; "eu" (Sunda) dihitung satu vokal; kata generik (kopi, toko, warung, dst.) tidak lagi membuat semua nama tertandai mirip (opsi `--generik`, `--tanpa-generik`).
- Tes regresi bertambah dari 17 menjadi 25.
