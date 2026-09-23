# Resep laporan: Stok Menipis

_Salin ke `laporan/RESEP-stok-menipis.md`, isi bagian `<isi>`. Skill ini TIDAK punya database
stok sendiri -- sumbernya adalah ekspor CSV dari aplikasi kasir/inventori yang sudah dipakai
pengguna (termasuk aplikasi "buku stok" bila sudah terpasang) atau catatan manual._

## Sumber data
- Folder: `<isi>` · Pola file: `<isi, mis. stok*.csv>`
- Kolom wajib: nama produk, stok saat ini. Kolom opsional: stok minimum/ambang (kalau tidak
  ada di file, tanyakan angka ambang ke pengguna per kategori produk, atau pakai default yang
  pengguna sebutkan sekali lalu dicatat di file ini).

## Jadwal
- `<isi -- mis. Setiap hari 07:00 WIB>` · Zona waktu: Asia/Jakarta (default)

## Langkah hitung
1. Cek kesiapan data:
   ```bash
   python3 <folder-skill-laporan-otomatis-terjadwal>/scripts/cek_sumber_data.py \
     --folder "<folder sumber>" --pola "<isi>" --label "stok" --maks-umur-hari 2
   ```
2. **Tidak ada script hitung khusus** -- baca CSV, filter baris dengan
   `stok saat ini <= stok minimum/ambang`, urutkan dari yang paling kritis (selisih terbesar di
   bawah ambang). Ini perbandingan angka sederhana; boleh dilakukan langsung tanpa script
   tambahan, TAPI **wajib membaca angka apa adanya dari file**, tidak menaksir.
3. Kalau tidak ada baris yang menipis: itu **hasil yang valid**, bukan error -- laporkan
   "Tidak ada produk menipis hari ini", jangan diam atau mengarang daftar.

## Format pesan (lewat scripts/susun_pesan.py)
- Judul: "Stok Menipis"
- Baris angka: Jumlah produk menipis
- Daftar: "Produk menipis" -- tiap item format `Nama -- sisa X -- ambang Y`, urut paling kritis
  dulu, batasi 10 item pertama (sebutkan jumlah sisanya bila lebih dari 10)
- Catatan: umur data (dari `cek_sumber_data.py`) supaya pengguna tahu keakuratan angka per jam
  berapa data terakhir diperbarui.

## Tujuan kirim
- Kanal: `<isi -- Telegram (default) atau WhatsApp nomor terpisah>`
- Penerima: `<isi -- pemilik/admin/bagian gudang>`
