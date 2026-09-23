# Contoh 04 – Input tidak lengkap: file tanpa kolom harga/total

## Skenario
S4, input tidak lengkap. File hanya berisi Tanggal, Menu, dan Porsi, tanpa harga maupun total. Omzet tidak bisa dihitung. Skill harus bertanya sekali, bukan mengarang harga.

## Input pengguna
```
tolong bikinin laporan omzet warung minggu ini dari file ini ya (penjualan-warung.csv)
```
Cuplikan file:
```
Tanggal,Menu,Porsi
2026-09-01,Nasi Goreng,16
2026-09-01,Mie Ayam,17
2026-09-01,Es Teh,15
```

## Output

Aku sudah cek file-nya. Isinya **Tanggal, Menu, dan Porsi** (1–7 September 2026, 3 menu), tapi **tidak ada kolom harga atau total**. Tanpa harga, omzet belum bisa dihitung, dan aku tidak mau menebak angkanya.

Pilih salah satu yang paling gampang:
1. **Kirim harga per porsi** tiap menu, contoh:
   - Nasi Goreng = Rp …
   - Mie Ayam = Rp …
   - Es Teh = Rp …
2. **Kirim file lain** (ekspor kasir/spreadsheet) yang sudah ada kolom harga atau total.

Begitu harganya ada, aku langsung buatkan rekap omzet, menu terlaris, dan hari paling ramai.

## Catatan penguji
- Perilaku agent: membaca header (langkah 1 SKILL.md), melihat kolom wajib "total harga" tidak ada, lalu bertanya sekali dengan daftar singkat. Bila script tetap dijalankan dengan kolom tebakan, hasilnya error yang jelas: `{"error": "Kolom tidak ditemukan", "hilang": ["Harga"], "kolom_tersedia": ["Tanggal", "Menu", "Porsi"]}`.
- Bagus: tidak mengarang harga, sesuai aturan "Jangan mengarang angka".
- Kurang (ringan): SKILL.md tidak menjelaskan apa yang harus dilakukan bila kolom wajib tidak ada. Perilaku di atas berasal dari penilaian agent. Script juga tidak mendukung penerapan daftar harga per produk (misalnya `--harga-produk "Nasi Goreng=15000,..."`). Setelah pengguna mengirim harga, agent harus membuat CSV baru sendiri, dan langkah ini tidak dijelaskan di SKILL.md.
- **Uji ulang v1.1.0 (2026-09-23):** perilaku sama, dan error script tetap jelas. SKILL.md v1.1.0 **masih belum** mengatur langkah bila kolom wajib (total/harga) tidak ada, dan belum ada opsi daftar harga per produk. Catatan "Kurang (ringan)" di atas masih berlaku.
- **Uji ulang v1.2.0 (2026-09-23):** perilaku sama. SKILL.md v1.2.0 masih belum mengatur langkah bila kolom total maupun harga tidak ada (R1). Agent tetap bertanya dengan benar atas inisiatif sendiri.
