# HASIL UJI — follow-up-prospek

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Lingkungan:** folder kerja sementara `/tmp/uji-follow-up-prospek/`, Python 3 standar
- **Skenario:** 01–05 + uji A/B (`00-pembanding-tanpa-skill.md`) + banding pesaing (`00-banding-pesaing.md`)

## Audit keamanan
- `scripts/jadwal_followup.py`: hanya `argparse, json, sys, datetime`. Tidak ada jaringan, file, subprocess, kredensial.
- SKILL.md/README/references: tidak ada prompt injection; ada prinsip privasi (UU PDP), larangan urgensi palsu, dan berhenti bila diminta. **Aman.**

## Verifikasi angka/tanggal (independen)
- Script terpisah (`verif.py`) membandingkan 300 jadwal acak (tanggal mulai 2026–2027, 1–6 offset, libur acak, dengan/tanpa akhir pekan) dengan implementasi terpisah berbasis `datetime` → **0 selisih**. Nama hari diperiksa manual (23 Sep 2026 = Rabu, 22 Sep = Selasa, 22 Nov = Minggu).
- Contoh SKILL.md/README (24 Sep, 28 Sep, 30 Sep, 7 Okt 2026) → benar.
- Data rusak/tepi: tanggal 2026-02-30, tanggal kosong, `--hari "1;3;7"`, `0`, `200`, kosong, 9 offset, "H+1,H+3", libur tak valid → semua ditolak dengan `ERROR:` jelas. Format `23/09/2026` diterima.
- **Temuan:** (a) mulai hari Jumat → H+1 dan H+3 jatuh Senin & Selasa berturut-turut (jarak "1 lalu 3 hari" runtuh menjadi 2 pesan di 2 hari berturut); mulai 23 Des dengan libur 24–25 Des dan `--hari 1,2,3` → 3 pesan di 28, 29, 30 Des. (b) Tanggal mulai di masa lalu (mis. 2026-09-10) menghasilkan jadwal yang sudah lewat tanpa peringatan.

## Skor

| Kriteria | Skor (1–10) | Alasan singkat |
|---|---|---|
| Pemicu (description) | 9 | Kata kunci ghosting/belum balas/follow up/chasing a lead; batas dengan tagih-piutang & broadcast jelas |
| Kemudahan awam | 9 | Satu kalimat cukup; tahap mudah dipilih |
| Kualitas output | 9 | Pesan bertujuan berbeda, pamit sopan, bank balasan keberatan; sangat siap kirim |
| Akurasi (angka/fakta) | 8 | Tanggal benar; pergeseran bentrok bisa merapatkan jarak; tidak ada peringatan tanggal lampau |
| Penanganan input kurang | 9 | Tanya sekali dengan pilihan tahap a–d |
| Penanganan di luar cakupan | 8 | Mengarahkan ke tagih-piutang; tanpa pesan cadangan bila skill rujukan tidak ada |
| Keamanan | 10 | Bersih |

## SKOR AKHIR: **8 / 10** — LULUS

Uji A/B: skill jelas lebih baik (tanggal pasti, tanpa promo/urgensi karangan, ada pesan pamit). Banding pesaing: `sales-followup` (zubair-trabzada/ai-sales-team-claude, MIT) kuat secara teknik tetapi berbasis email/LinkedIn/SMS gaya AS dan tanpa kalender hari kerja — skill kita menang untuk pasar Indonesia (WA-first). Tidak ada cacat berat.

## Daftar cacat & saran perbaikan

### Berat
- Tidak ada.

### Sedang
1. **Pergeseran jadwal merapatkan jarak antar-pesan** (script baris 72–78: `while not hari_kerja(d) or d in terpakai`). Mulai Jumat → pesan ke-1 Senin, ke-2 Selasa; bertentangan dengan prinsip "tidak mengejar-ngejar". **Saran:** setelah menggeser, pastikan jarak minimal ke pesan sebelumnya ≥ selisih offset asli atau minimal 2 hari kerja (mis. `d = max(d, jadwal_sebelumnya + (n - n_sebelumnya) hari)` lalu geser ke hari kerja), dan beri kolom catatan "digeser untuk menjaga jarak".

### Ringan
2. Tidak ada peringatan bila tanggal kirim sudah lewat / hari ini (script baris 54 dst.). **Saran:** tandai "sudah lewat" dan sarankan memulai urutan dari hari ini; di SKILL.md langkah 2 tambahkan "jika H+0 sudah lama, mulai dari pesan yang sesuai hari ini".
3. Tahap C ("nanti dulu") hanya memberi `--hari "7,21,45"`; untuk waktu yang disebut prospek (mis. "awal November") agent harus menghitung offset manual. **Saran:** tambah opsi `--tanggal 2026-11-02` (tanggal absolut) di script.
4. "Aturan main" hanya jam kantor; untuk B2C (tahap D) jam malam 19.00–20.30 lebih efektif. **Saran:** tambahkan baris jam kirim B2C di Format output.
5. Kolom `alasan_geser` selalu "akhir pekan/libur/bentrok" tanpa membedakan penyebab. **Saran:** isi alasan spesifik (Sabtu/Minggu/libur/bentrok).
6. Tidak ada pesan cadangan bila `tagih-piutang`/`broadcast-wa` tidak terpasang (bagian "Kapan TIDAK digunakan"). **Saran:** satu kalimat cadangan.
7. Dari banding pesaing: pertimbangkan naskah voice note WA 20–30 detik dan matriks jarak berdasarkan "temperatur" prospek (ide, bukan salinan).
