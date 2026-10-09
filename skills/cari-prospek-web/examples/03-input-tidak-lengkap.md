# Skenario 3: input tidak lengkap

- Tanggal uji: 2026-10-06 · **versi 1.0.2** · penguji independen ketiga · OpenClaw lokal, model claude-sonnet-5, lokal, durasi 0,6 menit
- Perbandingan lengkap SEBELUM/SESUDAH: `00-openclaw-sebelum-sesudah.md` (bagian "Uji ulang 1.0.2"); verifikasi sumber: `data/verifikasi-sumber.md`

## Input
> cariin calon pelanggan dong

## Output SESUDAH (skill 1.0.2)

Belum nemu di memory soal produk/jasa yang kamu jual atau target usahanya. Biar aku bisa langsung cari di web, tolong isi dulu:

1. **Jual apa** — produk/jasa apa yang kamu tawarkan?
2. **Jenis usaha target** — calon pelanggannya usaha seperti apa (misal: kafe, toko kelontong, pabrik makanan, dll)?
3. **Kota/wilayah** — mau dicari di kota/area mana?

(Opsional: ukuran/skala usaha target, dan jumlah prospek yang diinginkan — default 15.)

Begitu infonya ada, aku langsung eksekusi pencarian dan kasih tabel prospek + CSV siap pakai.

## Catatan penguji (1.0.2)
Skor 7 (SEBELUM 6). Tepat 3 pertanyaan wajib + default 15. Kata proses kecil "di memory". Belum ada contoh kalimat permintaan siap salin (saran uji 1.0.1 belum diterapkan).

Riwayat — 1.0.1: 7,5. 1.0.0: 7,5 (perilaku sama).
