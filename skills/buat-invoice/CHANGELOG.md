# Riwayat perubahan — buat-invoice

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.3 (2026-10-01)
- **PPh 23 untuk klien badan yang membayar jasa** (`"pph23": true`): invoice menampilkan potongan PPh 23 2% (4% bila tanpa NPWP) dan **estimasi diterima bersih**, tanpa mengubah total tagihan. Contoh: tagihan Rp14.985.000 (termasuk PPN) → PPh 23 Rp270.000 → diterima bersih Rp14.715.000.
- AI kini menulis invoice lengkap di chat (pengguna Telegram/WhatsApp tidak bisa membuka path file di komputer) dan melampirkan file HTML bila platform mendukung.
- Instruksi: script dijalankan dari subfolder `scripts/` di folder skill. 19 uji otomatis lulus (4 uji baru PPh 23).

## Catatan revisi 1.0.4 (2026-10-01)
- Bila kamu sudah menyebut **PKP**, AI langsung membuat invoice ber-PPN **12% dengan DPP nilai lain 11/12** (PMK 131/2024) dan menyebut asumsinya, tanpa bertanya ulang. Label "PPN 11%" tidak dipakai lagi (temuan uji ulang OpenClaw: agent sempat bertanya "PPN 11%?" padahal member sudah PKP).
- Nomor, kota, dan penanda tangan yang belum disebut cukup diisi placeholder, bukan alasan bertanya.
- Script tidak berubah selain nomor versi; semua tes otomatis lulus.
