# Skenario 04 (Input Tidak Lengkap) — "Cek SEO toko saya dong"

> Dibuat oleh **penguji independen** (agent terpisah, simulasi Claude Code), sesuai Tahap 6 CLAUDE.md.

## Permintaan pengguna
> "Cek SEO toko saya dong"

Tidak ada URL, tidak ada HTML yang ditempel, tidak ada nama usaha, tidak ada kata kunci — hanya kalimat pemicu skill tanpa info wajib.

## Yang seharusnya dilakukan (mengikuti SKILL.md)
Menurut tabel **Input** dan bagian "Kalau info wajib (halaman) belum ada" di SKILL.md: info wajib satu-satunya adalah **URL atau isi halaman**. Kalau belum ada, skill **harus bertanya SEKALI dalam satu pesan** yang berisi daftar pertanyaan singkat sekaligus (link/HTML, plus sekalian tanya nama usaha & lokasi fisik kalau relevan) — bukan mengarang jawaban, bukan meminta info satu-satu berkali-kali, dan bukan langsung menjalankan skrip tanpa data.

## Respons yang benar (simulasi agent mengikuti SKILL.md persis)
> "Boleh kirim link halamannya, atau tempel teks/HTML-nya di sini? Kalau mau saya sekalian cek Google Bisnisku, sebutkan juga nama usaha & apakah punya toko/area layanan fisik."

Ini persis kalimat template dari SKILL.md baris "Kalau info wajib (halaman) belum ada" — dipakai apa adanya karena sudah singkat, satu pesan, dan mencakup semua yang dibutuhkan (link/HTML, opsional nama usaha, opsional info lokasi fisik) sekaligus, sesuai prinsip "instan: tanya SEKALI dalam satu pesan" (CLAUDE.md §1).

**Yang TIDAK boleh dilakukan** (diverifikasi tidak terjadi kalau instruksi diikuti benar):
- ❌ Tidak boleh mengarang/menebak URL atau isi halaman.
- ❌ Tidak boleh menjalankan `scripts/cek_halaman.py` tanpa file HTML (script memang akan gagal jelas kalau dipaksa jalan tanpa argumen file — sudah diverifikasi di uji ketahanan script, lihat `HASIL-UJI.md`).
- ❌ Tidak boleh bertanya lebih dari satu kali berturut-turut sebelum pengguna sempat menjawab (mis. tanya link dulu, lalu setelah dijawab baru tanya nama usaha terpisah) — harus digabung jadi satu pesan sesuai instruksi.
- ❌ Tidak boleh langsung mengasumsikan skill lain yang tidak diminta (mis. langsung membuat listing marketplace) karena kalimatnya ambigu.

## Hasil uji
**Lulus.** Instruksi SKILL.md sudah menyediakan kalimat tanya yang tepat, singkat, satu pesan, dan sesuai prinsip "tanya sekali" di CLAUDE.md §1. Tidak ditemukan celah yang membuat agent kebingungan atau berisiko mengarang data karena SKILL.md eksplisit menyediakan kalimat siap pakai untuk kasus ini (bukan hanya instruksi abstrak "tanyakan info yang kurang").
