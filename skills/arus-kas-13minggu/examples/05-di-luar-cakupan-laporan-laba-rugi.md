# 05 — Di luar cakupan: minta laporan laba rugi bulan lalu

## Skenario
S5 — permintaan di luar cakupan. Pengguna ingin laporan laba rugi dari transaksi yang **sudah terjadi**. Skill ini untuk proyeksi kas ke depan, jadi harus mengarahkan ke `laporan-keuangan-emkm` tanpa memaksakan tabel 13 minggu.

## Input pengguna
> Tolong bikinin laporan laba rugi bulan Agustus dong buat diajukan ke bank. Omzet Agustus 62 juta, belanja bahan 31 juta, gaji 12 juta, sewa 5 juta, listrik 1,8 juta, cicilan mobil 3,2 juta.

## Output
Untuk **laporan laba rugi bulan Agustus** (transaksi yang sudah terjadi), yang cocok adalah skill **`laporan-keuangan-emkm`**, bukan proyeksi arus kas. Laporan laba rugi untuk bank perlu format standar (SAK EMKM) dan pemisahan yang benar. Contohnya, **cicilan mobil tidak seluruhnya dicatat sebagai biaya**: bagian pokoknya mengurangi utang, dan hanya bunganya yang menjadi beban. Karena itu saya tidak menghitungnya di sini supaya laporan ke bank tidak keliru.

Kalau skill `laporan-keuangan-emkm` sudah terpasang, cukup ketik: *"Buatkan laporan laba rugi Agustus dari data ini"* dengan data yang sama. Siapkan juga rincian cicilan (pokok vs bunga) dari jadwal angsuran leasing.

Setelah laporannya jadi, saya bisa bantu satu hal yang biasanya juga diminta bank: **proyeksi kas 13 minggu ke depan**, untuk menunjukkan Anda sanggup membayar cicilan baru. Kalau mau, kirim saldo kas hari ini, perkiraan penjualan per minggu, dan jadwal pengeluaran rutinnya.

## Catatan penguji
- Sesuai bagian "Kapan TIDAK digunakan" di SKILL.md: laporan laba rugi diarahkan ke `laporan-keuangan-emkm`. Tidak ada tabel 13 minggu yang dipaksakan.
- Alasan yang diberikan konkret (cicilan = pokok + bunga) dan berguna bagi pengguna awam.
- Menawarkan kaitan yang relevan (proyeksi kas untuk bank), sejalan dengan tujuan pengguna.
- Kurang (ringan): SKILL.md tidak punya kalimat cadangan bila skill rujukan tidak terpasang pada pembeli. Saran: satu baris di "Kapan TIDAK digunakan", misalnya "jika skill rujukan tidak ada, jelaskan singkat kenapa di luar cakupan dan beri langkah umum/penyedia layanan yang tepat".
