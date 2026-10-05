# Pra-cek konteks Telegram, gelombang 9 (2026-10-05)

Alat: `uji-tg.sh` (`--channel telegram`, tanpa kirim). Masing-masing 1 kali, pesan persis dari `scratchpad/pilot/teks-g9.json`. Nilai hanya dari isi chat.

| skill | skor internal (promosi/sebelum-sesudah.jsonl) | skor konteks Telegram | MASALAH? | catatan |
|---|---|---|---|---|
| sop-onboarding (1.0.4) | 6,5 -> 9,0 LULUS | 5 | MASALAH TELEGRAM | Hanya bertanya (6 pertanyaan) padahal info inti cukup; tidak ada paket onboarding atau jadwal 30/60/90 di chat. Kata proses bocor ("sudah saya cek"). Konten yang ada benar (PKWTT, Senin 12 Okt 2026, ingat UMK). |
| strategi-konten-iklan (1.0.4) | 6,5 -> 9,0 LULUS | 6,5 | MASALAH TELEGRAM (ringan) | Menolak/memperingatkan "turun 5kg seminggu" dengan benar (klaim tak terbukti, risiko iklan & UU Perlindungan Konsumen), tetapi tidak menyebut BPOM. Hanya bertanya AOV, padahal ROAS impas 2,5x bisa langsung diberikan. Kata proses bocor ("pakai script", "dijalankan script"). |
| laporan-status-kantor (1.0.4) | 6,3 -> 9,0 LULUS | 8,5 | tidak | Isi utuh di chat, siap tempel. Tidak mencantumkan THR per karyawan di grup (privasi, nominal lewat chat pribadi). Tanggal cuti benar. Catatan kecil: menyebut skill `hitung-thr` "belum terpasang" (bocor ringan, tidak mengganggu). |

## Verifikasi angka (python + web)
- 12 Okt 2026 = Senin (benar). Masa percobaan 3 bulan berakhir 11 Jan 2027 (hari ke-90 = 10 Jan 2027; 30 hari = 11 Nov, 60 hari = 11 Des). Balasan sop-onboarding tidak memuat jadwal, jadi tidak ada angka salah, tetapi juga tidak ada jadwal.
- ROAS impas = 1/margin = 1/0,4 = 2,5x. Balasan strategi-konten-iklan tidak menyebut angka (menunggu AOV).
- Cuti bersama Natal 2026 = Kamis 24 Des; Natal Jumat 25 Des; Tahun Baru Jumat 1 Jan 2027 (SKB 3 Menteri, 19 Sep 2025; setneg.go.id, detik.com). Balasan laporan-status-kantor cocok. THR paling lambat H-7 = Jumat 18 Des 2026 (benar). Kembali kerja Senin 4 Jan 2027 (benar).
- Masa percobaan hanya untuk PKWTT (PP 35/2021): balasan menyebut karyawan tetap (PKWTT), benar.

## Catatan
proposal-kerjasama 1.0.9, agen-cs-toko 1.0.9, dan naskah-live-jualan 1.0.7 sudah lulus uji ulang konteks Telegram; rujuk `skills/proposal-kerjasama/examples/00-openclaw-sebelum-sesudah.md`, `skills/agen-cs-toko/examples/00-openclaw-sebelum-sesudah.md`, `skills/naskah-live-jualan/examples/00-openclaw-sebelum-sesudah.md`.

## Rekomendasi
Layak tampil: laporan-status-kantor. Belum layak: sop-onboarding (hanya bertanya) dan strategi-konten-iklan (hanya bertanya + kata "script"); ganti cadangan atau perbaiki lalu ulang pra-cek.
