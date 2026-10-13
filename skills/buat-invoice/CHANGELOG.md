# Riwayat perubahan — buat-invoice

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.5 (2026-10-13)
- **Nomor invoice tidak dobel lagi saat membuat beberapa invoice berturut-turut.** Temuan uji platform OpenClaw 2026-09-29 (v1.0.1): invoice bernomor sama dengan nomor yang sudah ada. Sejak 1.0.2 script mencetak `Nomor terakhir dibaca: X -> nomor baru: Y` dan SKILL.md mewajibkan nomor terakhir disalin persis, tetapi script belum mengingat nomor yang sudah dibuat: uji ulang 2026-10-13 menunjukkan dua invoice berturut-turut dengan `--nomor-terakhir INV/2026/10/0012` yang sama sama-sama mendapat `INV/2026/10/0013`, dan `--counter-file` yang dipakai bersama `--nomor-terakhir` tidak diperbarui (lalu mulai lagi dari 0001).
- `--counter-file` kini mencatat setiap nomor yang dibuat beserta nama pembeli (`"terbit"`) dan bisa digabung dengan `--nomor-terakhir`/`nomor`: nomor yang sudah dipakai pembeli lain otomatis naik ke nomor berikutnya yang belum terpakai (dengan PERHATIAN), nomor sama untuk pembeli yang sama = revisi (nomor tetap), nomor manual yang bentrok ditolak. Counter per bulan ikut maju dan ditulis aman (file sementara lalu diganti). Lokasi lengkap file counter dicetak agar dipakai file yang sama dari folder kerja mana pun.
- SKILL.md: selalu pakai `--counter-file` di folder kerja yang disepakati; invoice kedua dst. memakai nomor yang baru dibuat script sebagai nomor terakhir.
- Logika hitung (diskon, PPN, PPh 23, meterai, pembulatan) tidak berubah. 26 uji otomatis lulus (7 uji baru penomoran tidak dobel).

## Catatan revisi 1.0.3 (2026-10-01)
- **PPh 23 untuk klien badan yang membayar jasa** (`"pph23": true`): invoice menampilkan potongan PPh 23 2% (4% bila tanpa NPWP) dan **estimasi diterima bersih**, tanpa mengubah total tagihan. Contoh: tagihan Rp14.985.000 (termasuk PPN) → PPh 23 Rp270.000 → diterima bersih Rp14.715.000.
- AI kini menulis invoice lengkap di chat (pengguna Telegram/WhatsApp tidak bisa membuka path file di komputer) dan melampirkan file HTML bila platform mendukung.
- Instruksi: script dijalankan dari subfolder `scripts/` di folder skill. 19 uji otomatis lulus (4 uji baru PPh 23).

## Catatan revisi 1.0.4 (2026-10-01)
- Bila kamu sudah menyebut **PKP**, AI langsung membuat invoice ber-PPN **12% dengan DPP nilai lain 11/12** (PMK 131/2024) dan menyebut asumsinya, tanpa bertanya ulang. Label "PPN 11%" tidak dipakai lagi (temuan uji ulang OpenClaw: agent sempat bertanya "PPN 11%?" padahal member sudah PKP).
- Nomor, kota, dan penanda tangan yang belum disebut cukup diisi placeholder, bukan alasan bertanya.
- Script tidak berubah selain nomor versi; semua tes otomatis lulus.
