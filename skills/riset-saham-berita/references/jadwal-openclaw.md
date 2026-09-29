# Jadwal cek level harga di OpenClaw (opsional)

Ditulis 2026-09-29 (v1.0.1). **Status: belum diuji di Gateway OpenClaw untuk skill ini.** Bentuk
perintah `automations add` di bawah mengikuti pola yang sudah terbukti jalan di Gateway uji
OpenClaw 2026.9.5 untuk skill Komunitech lain (laporan terjadwal). Bila versi OpenClaw pengguna
berbeda, jalankan `openclaw automations add --help` dulu dan sesuaikan; beri tahu pengguna.

## 1. Kenapa jadwalnya berupa pesan ke agent (bukan script saja)
`scripts/rasio_saham.py` **tidak mengambil harga dari internet**. Jadi setiap giliran jadwal,
agent yang harus: (1) membuka halaman harga publik tanpa login, (2) memperbarui kolom
`harga_sekarang`, `tanggal_harga`, `sumber_harga` di `saham/WATCHLIST.csv`, (3) menjalankan
perintah `level`, (4) melapor sesuai kode keluar. Level di file tetap milik pengguna; agent
tidak boleh mengubah kolom `level_atas`/`level_bawah`.

## 2. Contoh perintah (Telegram ke pemilik sendiri)
```bash
openclaw automations add "10 16 * * 1-5" "Pakai skill riset-saham-berita langkah E: perbarui harga penutupan tiap kode di saham/WATCHLIST.csv dari halaman publik tanpa login (tulis tanggal & sumber), jangan ubah kolom level, lalu jalankan rasio_saham.py level saham/WATCHLIST.csv. Kode 0: balas persis NO_REPLY. Kode 2 atau 3: kirim hasilnya apa adanya termasuk baris Ringkasan dan disclaimer. Tanpa rekomendasi beli/jual." \
  --tz "Asia/Jakarta" --name "Cek level watchlist saham" --session isolated \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```
- `"10 16 * * 1-5"` = Senin-Jumat 16.10 WIB (setelah penutupan bursa); ubah sesuai keinginan pengguna.
  Hindari jadwal terlalu rapat: halaman publik bisa memblokir akses berulang.
- `--tz "Asia/Jakarta"` wajib, supaya jam mengikuti WIB, bukan zona waktu komputer.
- WhatsApp hanya dengan **nomor terpisah** + persetujuan risiko tertulis pengguna. Tidak ada
  pengiriman ke grup/broadcast.

## 3. Arti kode keluar untuk laporan
| Kode | Arti | Yang dikirim |
|---|---|---|
| 0 | Semua baris dicek, tidak ada level tersentuh | `NO_REPLY` (tidak ada pesan) |
| 2 | Ada level tersentuh | Tabel hasil + disclaimer |
| 3 | Ada baris gagal dicek (harga tak terambil/rusak, level kosong/terbalik) | **Selalu dikirim**: ringkasan + daftar baris gagal; jangan dianggap aman |
| 1 | File/input salah | Pesan galat apa adanya |

Bila agent gagal membuka semua sumber harga, ia harus mengosongkan `harga_sekarang` baris itu
(bukan memakai harga lama diam-diam) sehingga script mengembalikan kode 3.

## 4. Cara uji sebelum diaktifkan
1. Jalankan manual sekali: `python3 <folder-skill-ini>/scripts/rasio_saham.py level saham/WATCHLIST.csv; echo $?`
   (Windows PowerShell: `py ...` lalu `echo $LASTEXITCODE`). Pastikan kode 0/2/3 sesuai isi file.
2. Setelah jadwal dibuat, jalankan sekali dengan `openclaw automations run <id> --wait` dan
   periksa pesan di Telegram. Catatan: perintah ini memaksa job berjalan, jadi hanya menguji isi
   pesan, bukan ketepatan jam.
3. Jelaskan cara menjeda/menghapus: `openclaw automations disable <id>` / `openclaw automations rm <id>`.

Bila pengguna tidak memakai OpenClaw (Claude Code, Codex, Cursor), tidak ada jadwal otomatis:
tawarkan perintah "cek level watchlist saya" yang dijalankan manual kapan saja.
