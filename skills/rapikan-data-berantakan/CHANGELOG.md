# Riwayat perubahan — rapikan-data-berantakan

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.2 (2026-10-05)
- Balasan dibuat lebih ringkas: blok angka ditulis sekali (pasangan nomor sama atau nama mirip tidak diulang di bagian lain), nama kolom teknis (mis. `_telepon_rumah`, `YYYY-MM-DD`) diganti kata biasa ("telepon rumah/kantor", "tahun-bulan-tanggal") di balasan ke pengguna, dan sasaran panjang di chat di bawah 2.500 karakter.

## Catatan revisi 1.0.1 (2026-10-05)
- Nomor baris di balasan kini selalu disalin dari laporan alat (bukan kolom "No" atau dihitung sendiri).
- Telepon rumah/kantor (021, 022, 0274, ...) tidak lagi masuk kolom HP/WhatsApp, dipisah ke kolom `_telepon_rumah`.
- Sel berisi dua nomor dipisah (nomor seluler pertama jadi HP, sisanya dicatat).
- Ringkasan angka tetap ("blok angka") yang wajib disalin utuh, juga di chat Telegram/WhatsApp.
- Daftar baris kembar tetap dari alat walau sebagian permintaan ditolak.

## Catatan revisi 1.0.0 (2026-10-05)
- Rilis awal.
