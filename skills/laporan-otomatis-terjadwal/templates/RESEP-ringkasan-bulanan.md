# Resep laporan: Ringkasan Bulanan (Keuangan)

_Salin ke `laporan/RESEP-ringkasan-bulanan.md`, isi bagian `<isi>`._

## Sumber data
- Buku kas (CSV/tabel teks): `<isi>` -- kolom tanggal, keterangan, masuk/keluar (lihat
  `laporan-keuangan-emkm/SKILL.md` untuk format lengkap & pemetaan kategori)
- Saldo awal/akhir, piutang, persediaan, dll. (kalau ada, sesuai kebutuhan skill sumber): `<isi>`

## Jadwal
- `<isi -- mis. Tanggal 1 tiap bulan, 07:00 WIB>` (untuk laporan bulan sebelumnya) · Zona waktu:
  Asia/Jakarta (default)

## Langkah hitung
1. Cek kesiapan data:
   ```bash
   python3 <folder-skill-laporan-otomatis-terjadwal>/scripts/cek_sumber_data.py \
     --folder "<folder sumber>" --pola "<isi>" --label "buku kas" --maks-umur-hari 35
   ```
2. Jalankan (lihat `laporan-keuangan-emkm/SKILL.md` untuk detail argumen lengkap):
   ```bash
   python3 <folder-skill-laporan-keuangan-emkm>/scripts/laporan_emkm.py "<file buku kas>" \
     --nama-usaha "<isi>" --periode-awal <YYYY-MM-01> --periode-akhir <YYYY-MM-akhir> \
     --format json
   ```
3. Ambil dari hasil: total pendapatan, total beban, laba/rugi bersih bulan berjalan, dan
   perbandingan singkat terhadap bulan sebelumnya bila tersedia.

## Format pesan (lewat scripts/susun_pesan.py)
- Judul: "Ringkasan Keuangan Bulan <nama bulan>"
- Baris angka: Pendapatan (Rupiah), Beban (Rupiah), Laba/rugi bersih (Rupiah, tulis "(rugi)"
  bila negatif)
- Catatan: sebutkan asumsi/disclaimer pembulatan dari skill sumber (belum dicocokkan Coretax),
  dan arahkan ke file laporan lengkap untuk lampiran/keperluan resmi.

## Tujuan kirim
- Kanal: `<isi -- Telegram (default) atau WhatsApp nomor terpisah>`
- Penerima: `<isi -- pemilik/admin sendiri>`
