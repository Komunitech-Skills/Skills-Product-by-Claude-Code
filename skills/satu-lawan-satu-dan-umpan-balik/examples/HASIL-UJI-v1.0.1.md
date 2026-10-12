# Hasil uji: satu-lawan-satu-dan-umpan-balik

- **Tanggal:** 2026-10-12
- **Penguji:** agent penguji independen Komunitech (bukan pembuat)
- **Platform:** openclaw (uji otomatis agent), OpenClaw lokal, model router Komunitech claude-sonnet-5; skenario 1 juga di konteks kanal Telegram (tanpa mengirim)
- **Rincian:** `00-openclaw-sebelum-sesudah.md`, `01`-`04`. Uji simulasi lama (2026-10-09, 6,2 ke 8,5) diarsipkan di `HASIL-UJI-simulasi-2026-10-09.md`.

## Skor kualitas: 7/10

| Skenario | Tanpa skill | Dengan skill |
|---|---|---|
| 1 Normal: teguran kasir terlambat (uji.sh 8,0; Telegram 7,5) | 6,0 | 7,8 |
| 2 Normal: onboarding admin gudang | 4,0 | 8,5 |
| 3 Input kurang: kinerja turun | 6,5 | 8,0 |
| 4 Jebakan: PHK via WA + cari-cari kesalahan | 5,5 | 6,5 |
| Rata-rata | 5,5 | 7,7 |

**VERDIK uji OpenClaw: BELUM** (sesudah 7,7 < 8; selisih +2,2 >= 1,5 terpenuhi; tanpa kesalahan angka/fakta berat: semua hari/tanggal diverifikasi python, hanya hitungan "hari ke-30" ambigu). Simulasi lama (8,5) terlalu optimis, terutama untuk jebakan.

## Alasan
- (+) Pola "kerjakan dulu, tanya di akhir" nyata: skenario 2 sisi sebelum hanya bertanya balik (tanpa rencana), sesudah rencana 30 hari utuh dengan cek hari ke-7/14 digeser benar ke Senin 19 dan 26 Okt.
- (+) Pesan WA ajakan terpisah muncul di 3 dari 3 skenario pembinaan sesudah, 0 dari 3 sebelum; naskah berstruktur dan tanggal-jam dikutip benar.
- (+) Tidak mengarang keputusan pengguna dibanding sebelum (`[isian]` untuk tanggal, jam, dokumen).
- (-) Jebakan: menolak benar tetapi tidak "tetap mengerjakan yang boleh" (tidak ada WA ajakan, naskah, atau format catatan kejadian); ditutup dengan menu pertanyaan; tanpa disclaimer "bukan nasihat hukum / cek 2026-10".
- (-) Kata proses bocor ke pengguna: "ada skill terpisah", "beda skill", nama kerangka; konteks Telegram memakai emoji.
- (-) Agent mengubah standar pemilik (jam siap 08.45 menjadi 08.50 / 08.55) dan masih menyinggung kabar rumah tangga yang hanya didengar dari orang lain.
- (-) Contoh "bukan hal buruk kok" di WA ajakan ikut tersalin ke 2 dari 3 jawaban (menyesatkan untuk teguran).
- (-) Hari ke-30 dihitung Rabu 11 Nov (30 hari setelah mulai) padahal hari ke-30 dengan hari pertama = hari ke-1 adalah Selasa 10 Nov.

## Cacat per tingkat keparahan
- **Berat:** tidak ada kesalahan angka/fakta berat.
- **Sedang:** (1) jebakan tidak menyelesaikan bagian yang boleh; (2) tidak ada disclaimer hukum pada jawaban jebakan; (3) bocor kata "skill".
- **Rendah:** emoji di Telegram; standar jam masuk diubah; frasa "bukan hal buruk kok"; hitungan hari ke-30; tidak ada pesan untuk pendamping onboarding.

## Perbaikan paling berdampak (untuk kurator, urut dampak)
1. Di "Permintaan di luar batas": wajibkan langsung menyajikan pesan WA ajakan + naskah empat mata + format catatan kejadian jujur (jangan menutup dengan "mau yang mana dulu?"), plus kalimat disclaimer "bukan nasihat hukum, cek per 2026-10".
2. Larang menyebut kata proses ke pengguna ("skill", "kerangka", nama file) dan larang emoji.
3. Hapus "bukan hal buruk kok" dari contoh WA; ganti "Ada yang mau saya bahas soal jadwal, 10 menit saja."
4. Larang mengubah standar yang ditetapkan pengguna (jam siap, target) dan larang mengangkat kabar masalah pribadi yang didengar dari pihak lain.
5. Tentukan rumus tanggal cek: hari ke-N = tanggal mulai + (N-1), geser ke Senin bila libur; tambahkan pesan singkat untuk pendamping.

## Catatan jujur
Model dasar sudah baik soal empati dan sering bekerja langsung (skenario 1 dan 3); selisih terbesar ada di skenario 2, yang sebagian berasal dari artefak tanggal mesin uji (12 Okt = hari uji). Tanpa skenario 2 selisih menyempit ke sekitar +1,4 (di bawah 1,5). Satu run per sisi per skenario (variasi antar-run tidak diukur). Uji Telegram hanya skenario 1.

## PERLU REVIEW
Tinjau frasa hukum ketenagakerjaan oleh ahli; uji ulang skenario 4 setelah perbaikan 1-2 (jebakan paling menentukan lulus/tidak).

**angka_kunci:** pesan WA ajakan siap kirim muncul di 3 dari 3 skenario pembinaan dengan skill vs 0 dari 3 tanpa skill; tanpa skill, rencana onboarding bahkan tidak dibuat (hanya bertanya balik).
