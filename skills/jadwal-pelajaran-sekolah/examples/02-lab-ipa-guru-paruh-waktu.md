# Contoh 2: 4 kelas, guru paruh waktu, Lab IPA satu ruang (uji ulang v1.0.1, 2026-10-12)

> Data fiktif (`data/kebutuhan-b.csv`, `data/info-b.txt`). Rincian utuh di `00-openclaw-sebelum-sesudah.md`.

## Masukan pengguna
"Ini kebutuhan jadwal semester depan SMP Cahaya Nusantara, datanya di kebutuhan-b.csv dan info-b.txt. Tolong susunkan jadwal per kelas dan per guru. Perhatikan Pak Budi cuma bisa hadir Selasa dan Kamis, dan Lab IPA cuma satu ruang."

## Keluaran dengan skill (ringkas)
Ringkasan 88/88 JP; grid 4 kelas; tabel 7 guru dengan total JP; CSV 88 baris dengan kolom Ruang; asumsi dan 3 pertanyaan; penutup "Balas kirim file ...".

## Verifikasi independen (python)
88/88 tepat, bentrok guru/kelas 0, Lab IPA tidak ganda, Pak Budi hanya Selasa dan Kamis (fitur skrip 1.0.1 terbukti). **Satu sel grid salah**: 8A Senin jam 2 tertulis "IPS" padahal CSV "Bahasa Inggris". Klaim "3 slot kosong" salah (sisa 28 slot).

## Catatan
Skor SESUDAH 7,0 vs SEBELUM 5,0 (agent tanpa skill: jadwal benar tetapi hanya di berkas .md, chat berisi nama berkas dan jargon). Jumat kosong total di 3 dari 4 kelas.
