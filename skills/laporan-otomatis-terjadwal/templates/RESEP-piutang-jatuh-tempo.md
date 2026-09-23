# Resep laporan: Piutang Jatuh Tempo

_Salin ke `laporan/RESEP-piutang-jatuh-tempo.md`, isi bagian `<isi>`._

## Sumber data
- Folder: `<isi>` · Pola file: `<isi, mis. piutang*.csv>`
- Kolom wajib CSV: `pelanggan,no_invoice,nominal,jatuh_tempo,dibayar` (opsional:
  `sudah_diingatkan`) -- lihat `tagih-piutang/SKILL.md`.

## Jadwal
- `<isi -- mis. Setiap hari 08:00 WIB>` · Zona waktu: Asia/Jakarta (default)

## Langkah hitung
1. Cek kesiapan data:
   ```bash
   python3 <folder-skill-laporan-otomatis-terjadwal>/scripts/cek_sumber_data.py \
     --folder "<folder sumber>" --pola "<isi>" --label "piutang" --maks-umur-hari 3
   ```
2. Jalankan (lihat `tagih-piutang/SKILL.md` untuk detail argumen lengkap):
   ```bash
   python3 <folder-skill-tagih-piutang>/scripts/hitung_telat.py --file "<file piutang>" \
     --tanggal <tanggal hari ini> --format json
   ```
3. Ambil dari hasil: **jumlah** tagihan per tahap (jatuh tempo hari ini, terlambat, H-1) dan
   **total nominal** per kelompok. **Jangan** cantumkan nama pelanggan satu per satu di pesan
   ringkas ini (UU PDP) -- cukup jumlah & total. Detail per pelanggan tetap ada di file arsip
   lokal untuk dibuka manual oleh pemilik saat menindaklanjuti.

## Format pesan (lewat scripts/susun_pesan.py)
- Judul: "Piutang Jatuh Tempo Hari Ini"
- Baris angka: Jatuh tempo hari ini (jumlah & total Rupiah), Terlambat (jumlah & total Rupiah),
  H-1 (jumlah & total Rupiah)
- Catatan: "Detail per pelanggan + draf pesan tagih ada di file `<path arsip>` -- buka manual
  untuk menindaklanjuti" (draf pesan tagih dibuat lewat skill `tagih-piutang`, dikirim manual
  oleh pemilik, **bukan** otomatis oleh jadwal ini)
- Kalau tidak ada piutang jatuh tempo: tulis eksplisit "Tidak ada piutang jatuh tempo/terlambat
  hari ini", jangan diam saja.

## Tujuan kirim
- Kanal: `<isi -- Telegram (default) atau WhatsApp nomor terpisah>`
- Penerima: `<isi -- pemilik/admin sendiri, BUKAN pelanggan>`
