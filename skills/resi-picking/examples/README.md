# Contoh pemakaian resi-picking

Contoh ini dibuat dengan menjalankan `scripts/resi.py` langsung (bukan ditulis tangan), untuk
menunjukkan format input/output yang sebenarnya. Data pesanan/pembeli di sini **fiktif**.

- `01-picking-dasar/` — skenario normal: file pesanan Shopee (dengan pesanan batal, jumlah 0, baris
  duplikat, dan baris "Total" ikut disertakan untuk menunjukkan cara alat menanganinya) + file lokasi
  rak + file stok (format `buku-stok laporan stok --csv`). Berisi input, ringkasan JSON, dan kedua
  dokumen Markdown hasilnya.
- `02-input-tidak-lengkap/` — file pesanan tanpa kolom Jumlah -> alat menolak dengan jelas dan
  menyebut kolom apa yang hilang, bukan menebak-nebak.
- `03-di-luar-cakupan/` — file yang bukan ekspor pesanan (laporan omzet harian) -> alat menolak karena
  kolom wajib tidak ditemukan, sesuai batasan di SKILL.md.

Pengujian mutu independen (uji A/B tanpa-skill, uji banding pesaing, skor kualitas, uji platform asli)
adalah tanggung jawab penguji terpisah sesuai `pedoman kurasi Komunitech` Tahap 6 dan belum dilakukan pada draf ini.
