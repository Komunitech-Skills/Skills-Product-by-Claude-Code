# Skenario 2: Normal kedua: onboarding admin gudang 30 hari

**Platform:** claude-code (simulasi agent), bukan OpenClaw asli.

**Input:** "Senin depan 12 Okt ada anak baru masuk, Bagas, jadi admin gudang di toko bahan kue saya. Timnya 6 orang. Pendampingnya Bu Wati. Bikinin rencananya ya."

## Output dengan skill

**Onboarding Bagas, Admin Gudang, mulai Senin 12 Oktober 2026 (pendamping: Bu Wati)**

**Hari pertama (Senin 12 Okt)**
- Sambut di pintu, kenalkan ke 6 rekan (nama dan tugas masing-masing), makan siang bersama.
- Siapkan sebelum datang: tempat duduk/loker, akses [isian: aplikasi stok/WA], seragam, nomor penting.
- Jelaskan jam kerja, istirahat, cara izin/sakit, aturan grup WA tim.
- Tugas kecil yang selesai hari itu: [isian: mis. mencatat barang masuk hari itu bersama Bu Wati], supaya pulang dengan rasa "saya sudah berguna".

**Minggu 1 (12-17 Okt), Mengamati:** ikut Bu Wati, pahami alur barang masuk-keluar. Cek hari ke-7 (Minggu 18 Okt jatuh libur, jadi Senin 19 Okt, 15 menit): "Apa yang membingungkan?"
**Minggu 2 (19-24 Okt), Mencoba didampingi:** catat stok sendiri, Bu Wati koreksi di tempat. Cek hari ke-14 (Senin 26 Okt; hari ke-14 = Minggu 25 Okt).
**Minggu 3 (26-31 Okt), Mandiri sebagian:** tugas rutin mandiri, tanya hanya bila ragu. Umpan balik tertulis singkat dari Bu Wati.
**Minggu 4 (2-7 Nov), Mandiri dan evaluasi:** cek hari ke-30 (Selasa 10 Nov, 30 menit): yang lancar, yang masih sulit, harapan dua arah, rencana bulan berikutnya.
*(Tanggal cek dihitung dari hari pertama = hari ke-1; sesuaikan bila ada libur.)*

**Tujuan akhir bulan:** [isian: mis. mencatat stok masuk-keluar sendiri tanpa dicek].

**Pesan WA sambutan (kirim Minggu 11 Okt)**
"Halo Bagas, besok kita ketemu di toko jam [isian: jam]. Bawa [isian: dokumen]. Nanti Bu Wati yang dampingi. Santai ya, hari pertama kita kenalan dulu. Sampai besok!"

**Pesan WA untuk Bu Wati:** "Bu Wati, Senin 12 Okt Bagas mulai. Mohon dampingi dulu, tugas kecil hari pertama: [isian]. Kita cek bareng tiap Senin, 15 menit ya."

**Asumsi:** jam kerja normal Senin-Sabtu, pendamping penuh Bu Wati. **Pertanyaan:** (1) Jam masuk Bagas dan dokumen yang dibawa? (2) Aplikasi/akses apa yang dipakai? (3) Apa target akhir bulan?

## Catatan

Nilai sebelum 7 / sesudah 8.5. Sebelum: rencana ringkas bagus tetapi mengarang masa percobaan 3 bulan, jam 08.00, 'bawa KTP dan NPWP', tanpa tanggal cek. Sesudah: tanggal tiap minggu dan cek hari ke-7/14/30 dihitung benar dengan kalender 2026 (hari ke-7 dan ke-14 jatuh Minggu, digeser ke Senin), pesan untuk Bagas dan Bu Wati, `[isian]` untuk dokumen/jam. Kurang: tidak menanyakan jam kerja gudang sebelumnya; aturan geser hari libur dibuat sendiri oleh agent, bukan dari skill.

Perbandingan lengkap dengan hasil tanpa skill: `00-openclaw-sebelum-sesudah.md`.
