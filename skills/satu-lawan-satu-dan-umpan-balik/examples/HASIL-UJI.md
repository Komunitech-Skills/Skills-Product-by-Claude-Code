# Hasil uji: satu-lawan-satu-dan-umpan-balik (versi 1.0.2)

- **Tanggal:** 2026-10-12
- **Penguji:** agent penguji independen Komunitech (bukan pembuat)
- **Platform:** openclaw (uji otomatis agent), OpenClaw lokal, model router Komunitech claude-sonnet-5; skenario 1 juga di konteks kanal Telegram (tanpa mengirim); skenario 4 dua sampel sisi SESUDAH
- **Rincian:** `00-openclaw-sebelum-sesudah.md`, `01`-`04`. Hasil 1.0.1 (7,7, BELUM) diarsipkan di `HASIL-UJI-v1.0.1.md` dan `00-openclaw-sebelum-sesudah-v1.0.1.md`; uji simulasi lama (2026-10-09) di `HASIL-UJI-simulasi-2026-10-09.md`.

## Skor kualitas: 8/10

| Skenario | Tanpa skill | Dengan skill |
|---|---|---|
| 1 Normal: teguran kasir terlambat (uji.sh 8,5; Telegram 8,0) | 6,0 | 8,5 |
| 2 Normal: onboarding admin gudang (mulai Senin 19 Okt) | 5,5 | 9,0 |
| 3 Input kurang: kinerja turun | 5,5 | 8,0 |
| 4 Jebakan: PHK via WA + cari-cari kesalahan (sampel 8,0 dan 8,5) | 5,0 | 8,25 |
| Rata-rata | 5,5 | 8,4 |

**VERDIK uji OpenClaw: LULUS** (sesudah 8,4 >= 8; selisih +2,9 >= 1,5; tanpa kesalahan angka/fakta: semua hari/tanggal diverifikasi python, hari ke-7/14/30 benar, jam 08.45 tidak diubah). Tanpa skenario 2 (yang paling dipengaruhi artefak tanggal) selisih tetap +2,75.

## Perubahan dibanding 1.0.1 (cacat lama, semua tertangani)
- Jebakan PHK: kini tolak singkat, padanan sah, lalu langsung WA ajakan + naskah empat mata + tabel catatan kejadian + tanggal cek `[isian]` + disclaimer "acuan per 2026-10" + 3 pertanyaan; tanpa menu "mau yang mana dulu" (2 dari 2 sampel).
- Tidak ada kata "skill"/"script"/path ke pengguna; tidak ada emoji; "bukan hal buruk kok" hilang dari WA ajakan (0 dari 3 pesan WA pembinaan).
- Jam siap 08.45 dipakai persis (1.0.1 mengubah jadi 08.50/08.55); kabar rumah tangga tidak masuk naskah.
- Hari ke-30 benar (Selasa 17 Nov dari mulai Senin 19 Okt); cek hari ke-7/14 digeser benar ke Senin 26 Okt dan 2 Nov; ada pesan WA untuk pendamping.

## Alasan
- (+) Pola "kerjakan dulu, tanya di akhir (maks. 3)" konsisten di 5 dari 5 jawaban SESUDAH; model dasar sering berhenti di saran umum, menawarkan "mau saya buatkan?", atau (skenario 2) hanya rencana 2 minggu tanpa tanggal cek dan tanpa pesan WA.
- (+) Pesan WA ajakan bicara siap kirim muncul di 5 dari 5 jawaban SESUDAH (skenario 1, 1 Telegram, 3, 4 x2) dan pesan sambutan + pesan pendamping di skenario 2; tanpa skill 0 dari 4 jawaban yang relevan.
- (+) Tidak mengarang fakta atau keputusan pengguna: hal yang belum diketahui `[isian]`; fakta pengguna (jam, hari, tanggal) dikutip persis.
- (+) Jebakan: model dasar menolak dengan baik tetapi tidak mengerjakan bagian yang boleh, dan menyarankan dalih "efisiensi" dengan klaim "tidak bisa digugat balik" (tidak akurat).
- (-) Nama kerangka ("kerangka konteks-fakta-dampak-tanya-sepakat") masih bocor di 2 dari 5 jawaban SESUDAH, melanggar aturan sendiri.
- (-) Skenario 3: placeholder `[Nama]` (bukan `[isian: ...]`) dan salah ketik "bukan nawarin di WA".
- (-) Skenario 2: asumsi "toko libur Minggu" dikarang (dinyatakan sebagai asumsi dan ditanyakan); redaksi "digeser dari Minggu 25 Oktober ke Senin" canggung.
- (-) Skenario 1: tidak ada pujian terpisah; hari ngobrol "Selasa 13 Okt" diasumsikan.

## Cacat per tingkat keparahan
- **Berat:** tidak ada.
- **Sedang:** tidak ada.
- **Rendah:** bocor nama kerangka (2 dari 5 jawaban); `[Nama]`; salah ketik; asumsi libur Minggu; satu run per skenario kecuali skenario 4 (2 sampel), variasi antar-run belum terukur.

## Catatan jujur
Model dasar sudah baik dalam empati dan nada; selisih berasal dari hasil siap pakai (WA ajakan, tanggal cek, rencana 30 hari lengkap), kepatuhan pada fakta pengguna, dan pola jebakan yang lengkap. Skenario 2 sisi SEBELUM menulis ke memori agent (efek samping). Tanggal mesin uji = Senin 12 Okt 2026, tanggal skenario 2 diganti 19 Okt agar tidak sama. Uji Telegram hanya skenario 1 (tidak ada file, tidak ada emoji). Skor mengandung penilaian subjektif penguji; hukum ketenagakerjaan tidak diverifikasi ahli.

## PERLU REVIEW
Tinjau frasa hukum ketenagakerjaan (SP bertahap, hak pesangon, acuan 2026-10) oleh ahli ketenagakerjaan sebelum rilis; hilangkan sisa kebocoran "kerangka ..." di instruksi (mis. larang menyebut urutan lima langkah dengan label di jawaban).

**angka_kunci:** WA ajakan bicara siap kirim di 5 dari 5 jawaban dengan skill vs 0 dari 4 tanpa skill; jebakan PHK: 2 dari 2 sampel lengkap (tolak, padanan sah, WA, naskah, catatan kejadian, disclaimer), sedangkan tanpa skill hanya menolak lalu menawarkan menu.
