# Uji A/B — skenario 01 (Shopee 40 pesanan), tanpa skill vs dengan skill

## Metodologi
Perbandingan dilakukan dengan menilai bagaimana agent generik (tanpa skill, tanpa izin menjalankan
skrip apa pun — hanya membaca 81 baris CSV lewat konteks percakapan) akan realistis menjawab
"buatkan daftar ambil barang dari file ini", dibandingkan hasil skill yang sudah diverifikasi
independen 100% cocok di `01-toko-shopee-40-pesanan.md`. Ini bukan transkrip agent kedua yang
sungguh dijalankan buta (tidak ada mekanisme di sesi ini untuk itu), tapi penilaian berbasis fakta
yang sudah diverifikasi: 40 pesanan x rata-rata 2 item = 81 baris mentah untuk dijumlah manual
per SKU/varian & per kurir, sesuatu yang mudah salah hitung tanpa alat.

## Tanpa skill (perkiraan realistis)
- Agent harus menjumlah 81 baris dengan mata/mental, per 8 kombinasi SKU+varian → risiko salah
  jumlah tinggi tanpa alat bantu hitung, apalagi memisahkan status batal/belum bayar (6 pesanan)
  dari yang aktif. Tidak ada jaminan pengelompokan per kurir konsisten atau lengkap.
- Kemungkinan besar output berupa ringkasan umum/perkiraan, bukan angka pasti per SKU dengan
  jumlah pesanan yang mendukungnya, dan format tidak konsisten dengan format checklist gudang
  yang siap tempel/print.
- Tidak ada mekanisme deteksi pesanan duplikat, resi kosong, atau validasi status secara sistematis.

## Dengan skill
- `total_barang = 133 pcs` per 8 SKU, jumlah pesanan per kurir, dan grup rak — **diverifikasi
  independen 100% cocok** (lihat `01-toko-shopee-40-pesanan.md`).
- Format checklist Markdown siap cetak/tempel WA, dengan bagian "catatan khusus" tersendiri dan
  peringatan status batal/belum bayar eksplisit.
- Waktu eksekusi skrip < 1 detik untuk 81 baris; scaling ke ratusan pesanan tidak butuh usaha
  tambahan dari agent.

## Kesimpulan uji A/B
Skill jelas unggul untuk tugas berbasis hitungan pasti (qty per SKU, jumlah pesanan per kurir) —
ini persis kelas masalah yang rentan salah bila dikerjakan manual oleh LLM tanpa alat hitung.
Nilai tambah **signifikan**, bukan skor maksimal 6.
