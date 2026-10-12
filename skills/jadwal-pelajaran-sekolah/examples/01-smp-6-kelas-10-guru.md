# Contoh 1: SMP 6 kelas, 10 guru, Jumat pendek (uji ulang v1.0.1, 2026-10-12)

> Data fiktif (`data/kebutuhan-mengajar.csv`, `data/info-sekolah.txt`). Hasil uji sungguhan penguji independen; rincian utuh di `00-openclaw-sebelum-sesudah.md`. Hasil 1.0.0 di `00-openclaw-sebelum-sesudah-v1.0.0.md`.

## Masukan pengguna
"Tolong buatkan jadwal pelajaran SMP kami dari file kebutuhan-mengajar.csv dan info-sekolah.txt. Saya mau jadwal per kelas dan per guru, dan jangan sampai ada guru atau kelas yang bentrok. Kalau bisa ada file yang bisa saya cetak."

## Keluaran dengan skill (ringkas)
- Chat memuat grid 6 kelas, tabel 10 guru, dan CSV 158 baris UTUH (mode biasa dan konteks Telegram); tanpa nama berkas; Telegram ditutup "Balas kirim file bila perlu versi CSV terpisah untuk dicetak."
- Ringkasan: **158/168 JP**, bentrok 0, 10 JP "belum muat" (9A/9B Bahasa Indonesia, 8A/8B PPKn dan PJOK).

## Verifikasi independen (python)
Bentrok guru 0, bentrok kelas 0, tabel kelas/guru cocok dengan CSV, maks 2 JP mapel sama per hari terpenuhi. **Tetapi 10 JP tidak terjadwal padahal jadwal penuh 168/168 ada** (agent tanpa skill menghasilkannya); PJOK 8A 0 JP.

## Catatan
- Kemajuan dari 1.0.0: utuh di chat, tanpa "file terlampir/workspace" di Telegram, tanpa blok 4 JP berurutan.
- Cacat: penjadwal berhenti di 158/168, alasan "slot nyaris penuh" keliru; mode biasa menulis "Saya juga lampirkan file CSV-nya" tanpa lampiran. Skor SESUDAH 6,0 (mode biasa) / 6,5 (Telegram) vs SEBELUM 5,5 / 4,5.
