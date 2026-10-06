# Skenario 3: input tidak lengkap

- Tanggal uji: 2026-10-06 · **versi 1.0.1** · penguji independen baru (uji ulang) · OpenClaw lokal, model claude-sonnet-5, lokal, durasi 0,7 menit
- Perbandingan lengkap SEBELUM/SESUDAH: `00-openclaw-sebelum-sesudah.md` (bagian "Uji ulang 1.0.1"); verifikasi sumber: `data/verifikasi-sumber.md`

## Input
> cariin calon pelanggan dong

## Output SESUDAH (skill 1.0.1)

Belum ada info soal usaha kamu di memori saya, jadi aku perlu tanya dulu biar nggak nebak-nebak. Boleh kasih tahu 3 hal ini:

1. **Jual apa** (produk/jasa kamu)?
2. **Target calon pelanggannya jenis usaha apa** (misal: toko kelontong, kafe, kantor, distributor, dll)?
3. **Kota/wilayah** yang mau disasar?

Kalau mau, sebutkan juga jumlah prospek yang diinginkan (default 15) dan ciri khusus (skala usaha, punya cabang, dll). Begitu ada jawabannya, langsung aku cariin daftarnya dari sumber publik (situs resmi, direktori, marketplace B2B) — bukan nebak atau ngarang kontak.

## Catatan penguji (1.0.1)
Skor 7,5 (SEBELUM 6; 1.0.0: 7,5). Tepat 3 pertanyaan wajib, tanpa kata proses, menegaskan tidak mengarang kontak. Masih belum memberi sesuatu yang langsung berguna (contoh kalimat permintaan siap salin / rencana pencarian singkat).

Riwayat — 1.0.0: 7,5 (perilaku sama).
