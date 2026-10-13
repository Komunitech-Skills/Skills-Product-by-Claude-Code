# 04 — Input kurang: "Cukup nggak sampai Lebaran?"

## Skenario
S4 — input tidak lengkap. Pengguna hanya memberi saldo. Penjualan dan pengeluaran rutin, yang wajib, tidak disebut, jadi skill harus bertanya **sekali** dengan maksimal 5 pertanyaan bernomor. Selain itu, Lebaran 2027 (tanggal resmi menunggu pengumuman pemerintah) berada di luar 13 minggu dari hari ini (23 Sep 2026).

## Input pengguna
> Uang usaha saya sekarang 40 juta. Cukup nggak ya sampai Lebaran? Takut nggak bisa bayar THR.

## Output
Bisa saya hitungkan per minggu. Supaya angkanya tepat, saya perlu beberapa data dulu. Jawab singkat saja, perkiraan kasar juga boleh:

1. Kira-kira **penjualan tunai/transfer per minggu** berapa? (Kalau naik-turun, sebutkan rata-ratanya; kalau menjelang Lebaran penjualan Anda naik, sebutkan juga.)
2. Ada **tagihan pelanggan** yang akan dibayar? (nama, nominal, perkiraan tanggal)
3. **Pengeluaran rutin:** belanja bahan/stok per minggu, gaji (tanggal berapa, total), sewa, cicilan, pajak, listrik/lainnya (tanggal berapa)?
4. **THR:** berapa karyawan dan berapa total THR-nya? (Menurut Permenaker No. 6 Tahun 2016: THR = 1 bulan upah untuk masa kerja ≥ 12 bulan, proporsional untuk masa kerja 1–<12 bulan, dibayar paling lambat 7 hari sebelum hari raya.)
5. Ada **pengeluaran besar sekali saja** sebelum Lebaran (renovasi, alat, stok besar untuk musim Lebaran)?

Catatan: tanggal Lebaran 2027 belum pasti — ikuti pengumuman resmi pemerintah, atau sebutkan tanggal yang ingin Anda pakai. Bila perkiraan kalender (sekitar Maret 2027) dipakai, jaraknya kira-kira 24 minggu dari minggu depan (Senin 28 Sep 2026). Rentang standar skill ini 13 minggu (sampai 27 Des 2026), jadi saya akan memperpanjang proyeksi sampai sekitar **24 minggu** (disesuaikan dengan tanggal resmi) agar THR masuk hitungan.

Uang saat ini saya catat **Rp 40.000.000** per hari ini. Batas aman (saldo minimum) saya pakai rata-rata pengeluaran 1 minggu, kecuali Anda punya angka sendiri.

## Catatan penguji
- Sesuai SKILL.md: bertanya sekali, 5 pertanyaan bernomor, tidak menanyakan hal yang ada defaultnya (batas aman, tanggal mulai).
- Pertanyaan 4 (THR) disesuaikan dengan kekhawatiran pengguna. Ini baik; template pertanyaan di SKILL.md bersifat umum.
- **Kurang (ringan):** SKILL.md tidak menyebut opsi `--jumlah-minggu` (script menerima 4–26 minggu). Agent baru tahu dari `--help` script. Pertanyaan seperti "sampai Lebaran/akhir tahun/6 bulan" sering muncul. Saran: di Langkah kerja 2 tambahkan "`--jumlah-minggu 26` bila pengguna bertanya lebih dari 13 minggu (maks. 26); sebutkan bahwa makin jauh makin kasar".
- Kurang (ringan): tidak ada panduan THR (jatuh tempo H-7, besaran 1 bulan upah untuk masa kerja ≥ 12 bulan; dasar Permenaker No. 6 Tahun 2016) di `references/opsi-tindakan.md` (kini sudah ditambahkan di bagian D), padahal THR disebut di README dan SKILL.md. Tanggal Lebaran tidak boleh dipastikan; di sini ditulis "belum pasti, ikuti pengumuman resmi pemerintah" dan pengguna diminta menyebut tanggal yang dipakai.
