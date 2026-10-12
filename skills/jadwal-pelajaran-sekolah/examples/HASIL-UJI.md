# Hasil uji: jadwal-pelajaran-sekolah v1.0.1

- **Tanggal:** 2026-10-12
- **Penguji:** agent penguji independen Komunitech (bukan pembuat); uji ulang setelah revisi 1.0.1 (hasil 1.0.0 di `HASIL-UJI-v1.0.0.md`, nilai dihitung ulang dari nol)
- **Platform:** openclaw (uji otomatis agent), OpenClaw 2026.9.6 lokal, model router Komunitech claude-sonnet-5; skenario 1 juga di konteks kanal Telegram (tanpa mengirim), kedua sisi
- **Rincian:** `00-openclaw-sebelum-sesudah.md`

## Skor kualitas: 6,8/10 (BELUM)

| Skenario | Tanpa skill | Dengan skill | Skor 1.0.0 (tanpa -> dengan) |
|---|---|---|---|
| 1. SMP 6 kelas, 10 guru, Jumat pendek (mode biasa 5,5 -> 6,0; Telegram 4,5 -> 6,5) | 5,0 | 6,25 | 5,0 -> 6,25 |
| 2. 4 kelas, guru paruh waktu, Lab IPA satu ruang | 5,0 | 7,0 | 5,0 -> 7,5 |
| 3. Input tidak lengkap ("bikinin jadwal pelajaran") | 6,0 | 8,0 | 6,0 -> 8,0 |
| 4. Jebakan: tanpa istirahat, JP > slot, jadwal Dinas, kirim WA otomatis | 4,0 | 6,0 | 4,0 -> 7,0 |
| Rata-rata | 5,0 | 6,81 | 5,0 -> 7,19 |

**VERDIK uji OpenClaw: BELUM** (sesudah 6,81 < 8; selisih +1,81 memenuhi >= 1,5; TETAPI ada kesalahan jumlah JP/fakta: S1 hanya 158 dari 168 JP padahal jadwal penuh ada, S2 satu sel grid salah, S4 PJOK 0 JP).

## Verifikasi angka (python independen)
- Bentrok guru 0 dan bentrok kelas 0 di semua jadwal kedua sisi; maks 2 JP mapel sama per hari per kelas terpenuhi di semua jadwal SESUDAH (0 pelanggaran); tidak ada slot di luar batas.
- **S1 SESUDAH (mode biasa dan Telegram, jadwal identik): 158/168 JP.** Kurang: 9A dan 9B Bahasa Indonesia (4 jadi 2), 8A PPKn 1 dari 2, 8B PPKn 0 dari 2, 8A PJOK 0 dari 2, 8B PJOK 1 dari 2. Jadwal penuh 168/168 terbukti ada (agent tanpa skill menghasilkannya). Penjelasan di jawaban ("kapasitas tidak cukup", disarankan tambah jam atau kurangi JP) keliru karena 28 JP muat di 29 slot.
- S2 SESUDAH: 88/88, Lab IPA tidak ganda, Pak Budi hanya Selasa/Kamis (fitur skrip 1.0.1 bekerja). Grid kelas 8A Senin jam 2 tertulis "IPS" tetapi CSV dan tabel guru "Bahasa Inggris" (1 dari 88 sel salah); klaim "3 slot kosong" salah (sisa 28 dari 116).
- S4 SESUDAH: 60/72, angka kekurangan benar, namun PJOK 0 JP di 7A dan 7B (8 JP hilang total) sementara Seni Budaya penuh.
- Tabel kelas dan tabel guru di chat cocok dengan blok CSV pada S1 (kedua mode) dan S4; pada S2 beda 1 sel (di atas).
- Skrip: `python3 -I tests/uji_regresi.py` OK (8 tes). Data uji: S1 158/168 (kode keluar 2), S2 88/88 (kode keluar 0), S4 60/72 (kode keluar 2). Data rusak (JSON terpotong, `jam_per_hari` "enam", `jp` 2.5, guru kosong/jp 0/jp teks, `hari` bukan daftar, berkas tidak ada): semua ditolak dengan pesan jelas, tanpa traceback, kode keluar 1 -- perbaikan dari 1.0.0 (traceback, jp desimal, kode 0) terkonfirmasi. Sisa cacat kecil: JSON akar daftar (`[1,2]`) pada `susun_jadwal.py` masih traceback (`validasi_input.py` benar).
- Kata proses/berkas di jawaban: S1/S1-Telegram/S2 bersih (tidak ada nama berkas/folder); S1 mode biasa berisi klaim keliru "Saya juga lampirkan file CSV-nya" tanpa lampiran dan "cek otomatis"; S4 berisi "dari script" dan `kebutuhan-d.csv`.

## Alasan skor
- (+) Pembeda penyajian kini kuat dan konsisten: jadwal SEMUA kelas, ringkasan SEMUA guru, dan CSV utuh di chat (S1 kedua mode, S2, S4); di Telegram tanpa "file terlampir/workspace" dan dengan tawaran "balas kirim file". Agent tanpa skill hanya menyimpan jadwal di PDF/CSV/MD dan menyebut nama berkas.
- (+) Kemampuan ketersediaan guru dan ruang (kolom Ruang) kini nyata di skrip dan terbukti benar (S2). Skrip menolak data buruk dengan pesan jelas.
- (+) Menolak kirim otomatis ke orang tua dan menyatakan belum bisa mencocokkan jadwal Dinas; input kosong ditangani dengan contoh format dan default.
- (-) **Penjadwal berhenti di 158/168** pada S1 padahal solusi penuh ada: algoritme backtracking tidak cukup kuat. Ini cacat berat karena pengguna diberi alasan keliru dan disuruh menambah jam.
- (-) Saat kapasitas memang kurang (S4), skrip menghabiskan slot mapel awal dan menyisakan PJOK 0 JP; SKILL.md tidak mewajibkan kekurangan dibagi adil atau PJOK/mapel wajib dijaga.
- (-) Grid di chat dibuat agent dari tabel sendiri (bukan dicetak dari penempatan skrip), sehingga satu sel menyimpang dari CSV (S2); tidak ada langkah cocokkan grid dengan CSV.
- (-) Mutu sebaran: Jumat kosong penuh di beberapa kelas (S2: 3 dari 4 kelas; S1: 8A/8B jam 1-4) sementara hari lain padat; model dasar dengan solver lebih merata.
- (-) Penolakan "tanpa istirahat" ada tetapi terselip di Asumsi; kata proses/nama berkas muncul di S4 dan klaim lampiran keliru di S1 mode biasa.
- Catatan jujur: model dasar di lingkungan uji punya `ortools` sehingga menghasilkan 168/168 dengan sebaran rapi (S1); di komputer pembeli awam belum tentu. Keunggulan skill ada pada penyajian utuh di chat, ketaatan aturan, dan penolakan aman, belum pada mutu penjadwalan.

## PERLU REVIEW (perbaikan konkret, urut dampak)
1. Perkuat penjadwal agar 168/168 tercapai di S1 (urutan kegiatan paling terbatas dulu / MRV, atau acak berulang dengan batas waktu; jalankan ulang bila `belum_terpenuhi` tidak kosong sebelum menyimpulkan kapasitas kurang); SKILL.md: dilarang menyebut "slot tidak cukup" kecuali total JP per kelas > kapasitas.
2. Saat kapasitas benar-benar kurang: bagi kekurangan merata antar mapel/guru (round-robin), jangan pernah membiarkan mapel 0 JP; tampilkan catatan aturan yang dipakai di bagian depan.
3. Wajibkan grid dan tabel guru DICETAK dari data skrip (mis. skrip mengeluarkan tabel markdown siap tempel) dan agent hanya menyalin; tambahkan pemeriksaan grid = CSV.
4. Sebar sehat: minimalkan hari kosong/jam bolong per kelas (preferensi hari penuh merata, Jumat tidak kosong) dan blok > 2 JP; tulis penolakan "tanpa istirahat" di baris pertama.
5. Larang kalimat "lampirkan file" di kanal tanpa lampiran, kata "script" dan nama berkas dalam jawaban; perbaiki traceback JSON akar daftar di `susun_jadwal.py`.
