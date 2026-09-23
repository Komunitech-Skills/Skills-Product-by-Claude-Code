# Resep laporan: Kas / Arus Kas Mingguan

_Salin ke `laporan/RESEP-kas-mingguan.md`, isi bagian `<isi>`._

## Sumber data
- Rencana kas: `<isi -- path file rencana-kas.csv>` (lihat `arus-kas-13minggu/templates/rencana-kas.csv`
  untuk format kolom `minggu;jenis;kategori;nominal;keterangan;kritis`)
- Saldo kas+bank hari ini (diperbarui manual tiap minggu sebelum jadwal jalan, atau dari file
  terpisah `<isi>` yang dicek dengan `cek_sumber_data.py`)
- Batas aman: `<isi, opsional -- default rata-rata pengeluaran 1 minggu>`

## Jadwal
- `<isi -- mis. Setiap Senin 07:00 WIB>` · Zona waktu: Asia/Jakarta (default)

## Langkah hitung
1. Cek kesiapan file rencana kas:
   ```bash
   python3 <folder-skill-laporan-otomatis-terjadwal>/scripts/cek_sumber_data.py \
     --folder "<folder sumber>" --pola "rencana-kas*.csv" --label "rencana kas" --maks-umur-hari 14
   ```
2. Jalankan (lihat `arus-kas-13minggu/SKILL.md` untuk detail argumen lengkap):
   ```bash
   python3 <folder-skill-arus-kas-13minggu>/scripts/proyeksi_kas.py "<file rencana kas>" \
     --saldo-awal "<isi, mis. Rp 20.000.000>" --mulai <tanggal Senin ini> --jumlah-minggu 4 \
     --format json
   ```
3. Ambil dari hasil JSON: saldo minggu berjalan, minggu terdekat yang di bawah batas aman
   (kalau ada) beserta selisihnya, dan ringkasan 1-2 opsi tindakan bila kas negatif.

## Format pesan (lewat scripts/susun_pesan.py)
- Judul: "Laporan Kas Mingguan"
- Baris angka: Saldo saat ini (Rupiah), proyeksi saldo akhir 4 minggu (Rupiah), minggu
  terdekat di bawah batas aman (kalau ada, dengan nominal kekurangannya)
- Daftar (opsional): 1-2 opsi tindakan bila ada minggu kritis
- Catatan: kalau tidak ada minggu kritis, tulis eksplisit "Aman -- tidak ada minggu di bawah
  batas dalam 4 minggu ke depan", **jangan** biarkan kosong tanpa keterangan.

## Tujuan kirim
- Kanal: `<isi -- Telegram (default) atau WhatsApp nomor terpisah>`
- Penerima: `<isi -- pemilik/admin sendiri>`
