# Contoh 2: Normal kedua: onboarding admin gudang 30 hari

> Hasil uji OpenClaw asli (2026-10-12, model claude-sonnet-5, uji otomatis agent). Perbandingan lengkap sebelum/sesudah: `00-openclaw-sebelum-sesudah.md`.

## Masukan pengguna
"Senin depan 12 Okt ada anak baru masuk, Bagas, jadi admin gudang di toko bahan kue saya. Timnya 6 orang. Pendampingnya Bu Wati. Bikinin rencananya ya."

## Keluaran di chat (dengan skill)

> # Rencana Onboarding 30 Hari — Bagas (Admin Gudang)
>
> **Mulai:** Senin, 12 Oktober 2026
> **Pendamping:** Bu Wati
> **Tim:** 6 orang
> **Tujuan akhir bulan:** Bagas bisa jalankan tugas admin gudang (stok masuk-keluar, pencatatan, pengecekan bahan kue) sendiri tanpa dicek terus oleh Bu Wati.
>
> ## Hari pertama (Senin, 12 Okt)
> - Siapkan sebelum dia datang: meja/area kerja gudang, akses yang dibutuhkan [isian: akses sistem pencatatan stok/kunci gudang], seragam kalau ada, nomor WA grup tim.
> - Sambut di pintu, kenalkan ke semua 6 orang tim (nama + tugas masing-masing).
> - Jelaskan: jam kerja, jam istirahat, cara izin/sakit, aturan grup WA tim.
> - Bu Wati jelaskan alur kerja gudang secara garis besar: alur bahan masuk, cara simpan, cara catat.
> - Satu tugas kecil yang selesai hari itu juga: [isian, misalnya — catat ulang stok 1 rak bahan bersama Bu Wati], supaya Bagas pulang dengan rasa sudah berguna.
> - Makan siang bersama tim kalau memungkinkan.
>
> ## Minggu 1 (12–18 Okt) — Mengamati
> Bagas ikut Bu Wati, mengamati alur kerja gudang: terima barang, cek kesesuaian nota, simpan sesuai tempat, catat di buku/sistem.
> **Cek hari ke-7 — Senin, 19 Okt (15 menit):** Bu Wati tanya ke Bagas: "Apa yang masih membingungkan?"
>
> ## Minggu 2 (19–25 Okt) — Mencoba didampingi
> Bagas mulai pegang tugas sendiri (misal: input stok harian, cek kadaluarsa bahan), Bu Wati mengoreksi langsung di tempat kalau ada yang kurang pas.
> **Cek hari ke-14 — Senin, 26 Okt (15 menit).**
>
> ## Minggu 3 (26 Okt – 1 Nov) — Mandiri sebagian
> Tugas rutin (input stok, laporan harian, cek fisik bahan) dikerjakan mandiri, tanya Bu Wati hanya kalau ragu-ragu. Bu Wati kasih umpan balik tertulis singkat seminggu sekali.
>
> ## Minggu 4 (2–8 Nov) — Mandiri & evaluasi
> Bagas pegang gudang sepenuhnya dengan pengawasan ringan.
> **Cek hari ke-30 — Rabu, 11 Nov (30 menit):** bahas apa yang sudah lancar, apa yang masih sulit, harapan dua arah (Bagas ke toko, toko ke Bagas), rencana bulan berikutnya.
>
> ## Pesan WA sambutan (kirim H-1, Minggu 11 Okt malam)
> "Halo Bagas, besok kita ketemu di toko jam [isian: jam masuk]. Bawa [isian: dokumen yang diperlukan]. Nanti Bu Wati yang dampingi kamu di gudang. Santai ya, hari pertama kita kenalan dulu. Sampai besok!"
>
> ## Naskah pengenalan ke tim (lisan, Senin pagi)
> "Teman-teman, mulai hari ini kita kedatangan anggota baru, Bagas, yang akan bantu di bagian admin gudang. Bu Wati yang akan dampingi dia beberapa minggu ke depan. Tolong dibantu kalau Bagas masih belum hafal alur kerja kita ya."
>
> ---
>
> **Asumsi yang dipakai:**
> - Tanggal mulai saya pakai persis sesuai pesan Anda (Senin, 12 Oktober 2026) — meski ini bertepatan dengan hari ini. Kalau maksudnya Senin *minggu depan* (19 Oktober), tinggal geser semua tanggal cek +1 minggu.
> - Tugas hari pertama dan akses yang dibutuhkan saya kosongkan `[isian]` karena belum tahu detail sistem pencatatan gudang Anda.
>
> **Pertanyaan (jawab kalau mau saya lengkapi):**
> 1. Bagas pakai sistem pencatatan stok manual (buku) atau aplikasi/Excel?
> 2. Jam masuk kerja dan dokumen yang perlu dia bawa hari pertama apa saja?

## Catatan penguji
Skor sebelum 4.0 / sesudah 8.5. SESUDAH (8,5): rencana utuh hari pertama + minggu 1-4, pendamping Bu Wati, cek hari ke-7 = Senin 19 Okt (hari ke-7 jatuh Minggu 18 Okt, digeser; benar), hari ke-14 = Senin 26 Okt (Minggu 25 Okt digeser; benar), pesan WA sambutan, naskah perkenalan ke tim, `[isian]` untuk jam/dokumen/akses, asumsi tanggal disebut, 2 pertanyaan. Kurang: cek "hari ke-30 = Rabu 11 Nov" padahal hari ke-30 (hari pertama = hari ke-1) adalah Selasa 10 Nov (11 Nov = 30 hari setelah mulai); tidak ada pesan untuk Bu Wati.
