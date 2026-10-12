# Contoh 2: 4 kelas, guru paruh waktu, Lab IPA satu ruang (uji OpenClaw 2026-10-12)

> Data fiktif (`data/kebutuhan-b.csv`, `data/info-b.txt`). Rincian utuh di `00-openclaw-sebelum-sesudah.md`.

## Masukan pengguna
"Ini kebutuhan jadwal semester depan SMP Cahaya Nusantara, datanya di kebutuhan-b.csv dan info-b.txt. Tolong susunkan jadwal per kelas dan per guru. Perhatikan Pak Budi cuma bisa hadir Selasa dan Kamis, dan Lab IPA cuma satu ruang."

## Keluaran dengan skill (ringkas)
88/88 JP; 4 grid kelas utuh; ringkasan guru; CSV 88 baris utuh dengan kolom Ruang; langkah cetak/kirim manual; asumsi dan 3 pertanyaan.

## Verifikasi independen (python)
Bentrok guru 0, bentrok kelas 0, Lab IPA tidak pernah ganda, Pak Budi hanya Selasa/Kamis, jumlah per kegiatan cocok semua.

## Catatan
- Skrip skill tidak mendukung ruang/ketersediaan guru (diuji terpisah: Pak Budi jatuh ke Senin/Jumat bila memakai skrip apa adanya); agent menambahkan sendiri dan hasilnya benar, tetapi tidak dijamin oleh skrip.
- Jumat kosong di semua kelas; blok 3-4 jam pelajaran sama berturut-turut; tabel ringkas guru berantakan.
