# Uji A/B — Skenario 01 Tanpa Skill vs Dengan Skill

Penguji independen (Tahap 6), 25 September 2026.
Prompt sama dengan `01-kafe-yogyakarta-2-barista-pkwtt.md`:
> "Kafe saya di Yogyakarta nerima 2 barista baru, statusnya karyawan tetap (PKWTT). Mulai Senin 5 Oktober
> 2026. Kerja 6 hari seminggu, ada shift pagi & sore. Tolong bikinin paket onboarding lengkap."

**Keterbatasan metode (jujur):** penguji tidak punya alat untuk memanggil agent kedua yang benar-benar
"bersih". Output "tanpa skill" di bawah ditulis penguji sebagai jawaban khas model umum yang kuat tanpa
instruksi khusus (pola yang biasa muncul: checklist generik, tanggal dihitung di kepala, hukum disebut
sekilas). Pemilik disarankan mengulang uji A/B ini di sesi terpisah tanpa skill terpasang.

## A. Tanpa skill (ringkasan output)
```
# Paket Onboarding Barista Baru

## Sebelum hari pertama
- Siapkan kontrak kerja, seragam/apron, jadwal shift, akun kasir
- Minta dokumen: KTP, KK, NPWP, rekening, ijazah, SKCK, pas foto
- Daftarkan BPJS

## Hari 1 (Senin, 5 Oktober 2026)
08.00 Penyambutan & tur kafe · 09.00 Pengenalan menu · 11.00 Shadowing barista senior · 15.00 Review

## Minggu 1: latihan espresso, milk steaming, SOP kebersihan, kasir
## 30 hari (5 November 2026): hafal semua menu, bisa pegang bar dengan pengawasan
## 60 hari (5 Desember 2026): mandiri di shift biasa, latte art dasar
## 90 hari (5 Januari 2027): mandiri di jam sibuk; evaluasi akhir masa probation 3 bulan

## Pesan sambutan WA
"Halo! Selamat bergabung di tim kami. Senin 5 Oktober jam 7 pagi ya, pakai kaos hitam..."

## Aturan kerja
- Jam kerja 07.00–15.00 (shift pagi) & 14.00–22.00 (shift sore)
- Cuti 12 hari/tahun, telat max 15 menit
```

## B. Dengan skill
Lihat `01-kafe-yogyakarta-2-barista-pkwtt.md` (checklist 4 bagian, tabel jadwal dari script, WA + pengumuman
tim untuk 2 orang, buku saku dengan `[isi: ...]`, formulir evaluasi, disclaimer).

## Kriteria & skor (0–2 per kriteria)
| # | Kriteria | Tanpa skill | Dengan skill | Catatan |
|---|---|---|---|---|
| 1 | Tanggal benar & dapat diverifikasi | 0 | 2 | Tanpa skill: "30 hari = 5 Nov" (sebenarnya hari ke-32), "90 hari = 5 Jan 2027" **melewati** batas percobaan 4 Jan 2027. Dengan skill: tanggal dari script, cocok verifikasi mandiri penguji |
| 2 | Batas masa percobaan tegas (tanggal hukum + evaluasi sebelum batas) | 0 | 2 | Tanpa skill: evaluasi "akhir probation" dijadwalkan setelah batas hukum |
| 3 | Kewajiban BPJS (wajib, batas 30 hari, Ketenagakerjaan & Kesehatan) | 1 | 2 | Tanpa skill hanya "Daftarkan BPJS" |
| 4 | Minimisasi data (PDP) | 0 | 2 | Tanpa skill minta KK & SKCK untuk semua, tanpa alasan/penyimpanan aman |
| 5 | Tidak mengarang aturan usaha | 0 | 2 | Tanpa skill mengarang jam shift, cuti 12 hari "per tahun" tanpa syarat 12 bulan, toleransi telat |
| 6 | Kelengkapan paket (checklist, jadwal+PJ, pesan+pengumuman, buku saku, evaluasi) | 1 | 2 | Tanpa skill tidak ada formulir evaluasi & pengumuman tim, PJ tidak jelas |
| 7 | Konteks 2 orang & shift/buddy | 1 | 2 | Dengan skill: buddy per shift, pesan per orang |
| 8 | Disclaimer & dasar hukum bertanggal | 0 | 2 | |
| 9 | Kepraktisan konten peran (hari 1 per jam, target keterampilan barista) | 2 | 1 | Tanpa skill lebih konkret soal jadwal H1 per jam & latihan teknis; skill hanya memberi kegiatan generik, target barista ditambah agent |
| | **Total** | **5/18** | **17/18** | |

## Kesimpulan
Dengan skill **jelas lebih baik**, terutama pada hal yang berisiko bagi pemilik usaha: tanggal evaluasi
sebelum batas percobaan, BPJS, PDP, dan tidak mengarang aturan. Kelemahan skill: jadwal H1 per jam dan
target keterampilan per jabatan tidak disediakan template/script — bahan perbaikan.

**Bahan README (sebelum/sesudah):** "Tanpa skill: evaluasi akhir probation dijadwalkan 5 Januari 2027 —
sehari setelah masa percobaan habis. Dengan skill: batas hukum 4 Januari 2027, evaluasi Sabtu 2 Januari."
