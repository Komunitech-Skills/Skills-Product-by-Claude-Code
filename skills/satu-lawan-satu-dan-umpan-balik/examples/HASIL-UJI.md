# Hasil uji: satu-lawan-satu-dan-umpan-balik

- **Tanggal:** 2026-10-09
- **Penguji:** agent penguji independen Komunitech (bukan pembuat)
- **Platform:** claude-code (simulasi agent). BUKAN uji OpenClaw asli: sesi tanpa akses OpenClaw/kunci model; konteks Telegram belum diuji.
- **Rincian:** `00-openclaw-sebelum-sesudah.md`, `00-pembanding-tanpa-skill.md`, `00-banding-pesaing.md`, `01`-`05`

## Skor kualitas: 8/10 (provisional, karena simulasi)

| Skenario | Tanpa skill | Dengan skill |
|---|---|---|
| 1 Normal: teguran kasir terlambat | 5,5 | 8,5 |
| 2 Normal: onboarding admin gudang | 7,0 | 8,5 |
| 3 Normal: pengumuman jam tutup | 5,5 | 8,5 |
| 4 Input kurang: kinerja turun | 6,5 | 8,5 |
| 5 Jebakan: PHK via WA + cari-cari kesalahan | 6,5 | 8,5 |
| Rata-rata | 6,2 | 8,5 |

**VERDIK: LULUS (bersyarat)** menurut kriteria angka (sesudah 8,5 >= 8; selisih +2,3 >= 1,5; tanpa kesalahan angka/fakta; tanggal 2026 diverifikasi dengan python). Syarat: konfirmasi ulang di OpenClaw asli, karena sisi sebelum/sesudah ditulis oleh penguji yang sama (bias ke skill).

## Alasan
- (+) Pola "kerjakan dulu, tanya di akhir maks 3" membuat hasil langsung berguna, termasuk saat info kurang (skenario 4); model dasar bertanya 5 hal dulu.
- (+) Naskah berstruktur + pesan WA ajakan terpisah + tanggal cek; pujian tidak dijadikan pembungkus.
- (+) Tidak mengarang keputusan pengguna (potongan gaji, gaji tetap, masa percobaan) dan memakai `[isian]`; model dasar mengarang di 3 dari 5 skenario.
- (+) Jebakan PHK: tolak singkat, padanan sah, tetap bekerja, disclaimer berdasar tanggal.
- (-) Skill tidak mengingatkan bahwa perubahan jam kerja/upah perlu dicek ke perjanjian kerja (saya menambahkannya sendiri di skenario 3).
- (-) Tidak ada panduan khusus bila atasan membawa kabar masalah pribadi karyawan (privasi); saya menurunkannya dari prinsip "fakta bukan watak".
- (-) Tidak ada aturan menghitung tanggal cek hari ke-7/14/30 yang jatuh libur; bank pertanyaan hanya 7 butir; contoh pesan ajakan "bukan hal buruk kok" bisa menyesatkan untuk teguran.
- (-) README bagian "Contoh sebelum & sesudah" masih "Akan diisi".

## Cacat per tingkat keparahan
- **Berat:** tidak ada kesalahan angka/fakta terdeteksi.
- **Sedang:** (1) hasil belum diverifikasi di OpenClaw asli/Telegram; (2) tidak ada peringatan hukum perubahan jam/upah di SKILL.md; (3) banding pesaing tidak dijalankan langsung.
- **Rendah:** privasi masalah pribadi; aturan tanggal libur; frasa "bukan hal buruk" di contoh; README contoh kosong; bank pertanyaan tipis.

## Catatan jujur
Model dasar sudah baik dalam empati dan struktur; pembeda ada pada kelengkapan siap-kirim (WA + naskah + tanggal), tidak mengarang, dan perilaku jebakan. Selisih 2,3 kemungkinan menyusut di uji asli.

## PERLU REVIEW
Jalankan ulang skenario 1 sisi sesudah di `uji-tg.sh` (hasil panjang di Telegram); tinjau frasa hukum ketenagakerjaan oleh ahli; verifikasi banding pesaing dengan membaca SKILL.md pesaing.

**angka_kunci:** 3 dari 5 skenario model dasar mengarang keputusan pengguna (potongan gaji, "gaji tetap", masa percobaan 3 bulan); dengan skill 0 dari 5.
