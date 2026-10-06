# Skenario 3: input tidak lengkap

- Tanggal uji: 2026-10-06 · penguji independen · OpenClaw lokal, model claude-sonnet-5
- Perbandingan lengkap SEBELUM/SESUDAH: `00-openclaw-sebelum-sesudah.md`; verifikasi sumber: `data/verifikasi-sumber.md`

## Input
> cariin calon pelanggan dong

## Output SESUDAH (dengan skill)

Belum ada info usaha Bapak/Ibu di memori saya, jadi saya butuh sedikit konteks dulu biar hasilnya pas (dan supaya langsung kerja, bukan asal tebak):

1. Jual apa — produk/jasa apa yang ditawarkan?
2. Target calon pelanggannya jenis usaha apa (toko, kantor, restoran, pabrik, dst)?
3. Kota/wilayah mana yang mau disasar?

Kalau mau, boleh juga sebut ukuran/ciri khusus (misal: "resto skala menengah, 1-5 cabang") dan jumlah prospek yang diinginkan (default 15). Begitu saya punya ini, langsung saya carikan daftarnya lengkap dengan kontak dan sumbernya.

## Catatan penguji
Skor 7,5 (SEBELUM 6). Tepat 3 pertanyaan wajib, tanpa kata proses. SEBELUM bertanya 4 hal, membocorkan "IDENTITY.md", dan menawarkan mencari lewat grup WA/Telegram. Bisa lebih baik: sertakan contoh kalimat permintaan siap salin atau rencana pencarian singkat agar pengguna tidak pulang dengan tangan kosong.
