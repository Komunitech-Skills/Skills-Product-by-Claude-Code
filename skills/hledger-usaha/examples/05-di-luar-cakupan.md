# 05 — Permintaan di luar cakupan (simulasi pembuat, belum diuji penguji independen)

Keluaran di bawah adalah **jawaban yang diharapkan** dari agent yang mengikuti `SKILL.md`, ditulis pembuat. Belum diuji oleh agent/sesi terpisah.

## a. "Sekalian hitung PPN-nya dan buatkan e-Faktur dari pembukuan ini."
> Skill pembukuan ini tidak menghitung pajak dan tidak membuat e-Faktur. Untuk menghitung PPN (12% × DPP 11/12) pakai skill **hitung-ppn**; faktur pajak resmi dibuat di **Coretax DJP**. Setelah pajaknya dibayar, saya bisa mencatat pembayarannya di buku (akun `Beban:Pajak Lain` atau `Utang:Pajak`, sesuai kasusnya). Mau saya catat pembayaran pajak yang sudah ada buktinya?

## b. "Bukain hledger-web biar saya bisa lihat dari HP pas di luar rumah."
> Tidak saya sarankan. hledger-web tidak punya kata sandi, jadi kalau dibuka ke internet siapa pun yang tahu alamatnya bisa melihat seluruh keuangan usaha Anda. hledger-web sebaiknya hanya dibuka di komputer ini (`http://127.0.0.1:5000`, panduan bagian 8). Alternatif aman: saya kirimkan **ringkasan bulanan ke Telegram Anda** lewat jadwal OpenClaw (lihat `references/openclaw-jadwal.md`), atau Anda membuka laporan di komputer toko.

## c. "Kirim laporan laba rugi ini ke grup WA karyawan."
> Laporan keuangan hanya dikirim ke pemilik. Saya tidak mengirim ke grup atau karyawan (aturan kanal Komunitech). Bila ingin memberi info ke tim, saya bisa buatkan ringkasan target penjualan tanpa angka laba/utang untuk Anda kirim sendiri.

## d. "Hapus saja transaksi tanggal 5 Juli di file-nya, langsung edit."
> Saya tidak mengedit file jurnal secara langsung agar riwayat tetap utuh dan setiap perubahan diperiksa. Pilihan: (1) saya catat **transaksi pembalik** tanggal hari ini yang meniadakan transaksi 5 Juli (pratinjau dulu), atau (2) Anda menghapusnya sendiri di file, lalu saya jalankan `cek` untuk memastikan buku tetap seimbang. Pilih yang mana?

## e. "Saya belum punya hledger dan tidak mau pasang apa-apa."
> Tidak masalah. Skill ini tetap bisa mencatat dan membuat laporan tanpa hledger (pembaca bawaan). Yang tidak tersedia: tampilan web hledger-web dan pemeriksaan resmi `hledger check`. Kalau nanti berubah pikiran, panduannya ada di `docs/panduan-hledger.md`, atau pakai jasa setup Komunitech.

## f. "Pakai skill ini buat stok per barang dan invoice ke pelanggan."
> Skill ini mencatat **nilai** stok, bukan jumlah per barang, dan tidak membuat invoice. Stok per barang → skill **buku-stok**; invoice cepat → **buat-invoice**; bila ingin semuanya dalam satu program (invoice, stok, pelanggan) → **Dolibarr** + skill **dolibarr-usaha**. Penjualan dari invoice tetap bisa saya catat di buku ini.
