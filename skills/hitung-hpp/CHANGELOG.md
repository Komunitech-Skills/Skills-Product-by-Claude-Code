# Riwayat perubahan — hitung-hpp

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.3 (2026-10-01)
- Opsi baru **banding harga** (`--banding-harga "18000;19500"`): setiap harga yang disarankan AI kini dihitung script lengkap dengan laba, margin, dan BEP — tidak lagi ditaksir (temuan uji OpenClaw: BEP Rp18.000 ditaksir ~460, seharusnya 501 gelas).
- Blok baru **Porsi biaya dalam HPP** (per kategori, variabel vs tetap, komponen terbesar) agar klaim "biaya terbesar" berasal dari angka script.
- Instruksi: script dijalankan dari subfolder `scripts/` di folder skill (tidak mencari ke seluruh disk); angka script disalin apa adanya ke chat. 5 tes otomatis baru (`tests/`).

## Catatan revisi 1.0.4 (2026-10-01)
- Aturan kutip angka diperketat: semua angka BEP (unit, rupiah, % dari rencana produksi), laba, margin, dan porsi biaya di balasan AI wajib disalin **persis** dari keluaran script, tanpa dihitung atau dibulatkan ulang. BEP selalu dibulatkan ke atas oleh script (temuan uji ulang OpenClaw: BEP Rp19.000 & Rp20.000 ditulis 450 & 409, padahal script 451 & 410).
- Script tidak berubah selain nomor versi; semua tes otomatis lulus.
