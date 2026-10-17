# Paket Onboarding Karyawan Baru, Siap Pakai

**Karyawan baru masuk Senin? Checklist, jadwal 90 hari, pesan sambutan, buku saku, dan formulir evaluasi langsung jadi — tinggal isi data yang ditandai, lalu cetak.**

Diuji AI penguji independen di OpenClaw: 6,5 → 9,0 dari 10 (tanpa skill tanggal 30/60/90 hari hanya perkiraan dan BPJS ditulis "sesuai kebijakan toko"; dengan skill tanggal jadwal dihitung skrip, dan BPJS ditulis wajib dengan tenggat 30 hari sesuai aturan).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- Checklist pra-hari-pertama lengkap: dokumen, pendaftaran BPJS, kontrak, perangkat kerja — supaya tidak mudah ada yang terlewat
- Jadwal orientasi (onboarding) hari pertama, minggu 1, dan checkpoint 30-60-90 hari dengan **tanggal dihitung otomatis** (bukan dikira-kira, termasuk libur nasional & cuti bersama 2026/2027 bawaan), lengkap dengan penanggung jawab
- Khusus karyawan tetap (PKWTT): **batas hukum akhir masa percobaan dan tanggal evaluasi keputusannya dihitung terpisah**, evaluasi dijadwalkan sebelum batas hukum — bukan sekadar checkpoint 90 hari yang bisa kelewat
- Panduan rekan pendamping (buddy) singkat, jadwal check-in mingguan, dan target per jabatan (kasir, barista, mekanik, dll.) supaya karyawan baru tidak merasa dilepas begitu saja
- Pesan sambutan WhatsApp/email siap kirim ke karyawan baru + pengumuman ke tim
- Buku saku karyawan ringkas (jam kerja, cuti, seragam, aturan HP) yang mudah dipahami karyawan awam
- Formulir evaluasi akhir orientasi/masa percobaan yang objektif (versi terpisah untuk karyawan kontrak/PKWT tanpa istilah "lulus masa percobaan"), plus catatan evaluasi proses orientasi untuk perbaikan berikutnya
- Varian siap pakai untuk toko, kafe, bengkel, klinik, kantor jasa, dan gudang

## Cocok untuk siapa
- Pemilik UMKM dan kantor kecil yang baru pertama kali merekrut karyawan
- Staf HR/admin personalia yang ingin proses onboarding lebih rapi dan konsisten
- Manajer/supervisor yang bertanggung jawab menyambut dan membimbing karyawan baru

## Contoh sebelum & sesudah
**Sebelum:** Karyawan baru datang, diperkenalkan seadanya, langsung disuruh kerja tanpa panduan tertulis. Dokumen BPJS baru diurus setelah ditegur, dan tidak ada evaluasi jelas di akhir masa percobaan.

**Sesudah (cukup ketik):** "Buatin paket onboarding buat kasir baru namanya Sinta, mulai Senin 28 September 2026, PKWTT, kerja 6 hari seminggu"

Cuplikan jadwal (dipotong; contoh dengan data fiktif, hasil hitung nyata dari alat hitung bawaan skill):
```
| Tahap | Tanggal target | Tanggal disesuaikan | Digeser? | Penanggung jawab | Kegiatan |
| Hari pertama (H1) | 28 September 2026 | 28 September 2026 | Tidak | Pemilik/Atasan langsung | Penyambutan, serah terima perangkat & akun, penjelasan buku saku karyawan |
| Checkpoint 90 hari | 26 Desember 2026 | 26 Desember 2026 | Tidak | Pemilik/Atasan | Evaluasi checkpoint orientasi |
| Batas hukum akhir masa percobaan (PKWTT) | 27 Desember 2026 | 27 Desember 2026 | Tidak | - | Tanggal hukum tetap (informasi, bukan tanggal kegiatan) -- TIDAK PERNAH digeser walau jatuh di hari libur. |
| Evaluasi keputusan akhir masa percobaan (PKWTT) | 19 Desember 2026 | 19 Desember 2026 | Tidak | Pemilik/Atasan | Isi formulir evaluasi & putuskan lanjut sebagai karyawan tetap atau tidak, SELALU sebelum/tepat batas hukum di atas (5 hari kerja lebih awal, supaya keputusan sempat diproses). |
```
Hasil lengkapnya juga memuat checklist dokumen & BPJS, pesan WA sambutan, buku saku, panduan rekan pendamping & target, dan formulir evaluasi.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Buatkan paket onboarding lengkap untuk barista baru di kafe saya, mulai bulan depan."
- "Bikin rencana 30-60-90 hari untuk mekanik baru di bengkel, kerja PKWT 6 bulan."
- "Tolong buatkan buku saku karyawan untuk toko kelontong saya."
- "Formulir evaluasi akhir masa percobaan untuk admin kantor."

## Syarat
Jadwal onboarding dihitung otomatis memakai Python (biasanya sudah ada di Mac/Linux; di Windows bisa dipasang gratis dari python.org). Tanpa Python, tanggal tetap dihitung manual dengan rumus yang jelas — skill tetap berguna.

## Instalasi singkat
Salin folder `sop-onboarding` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** skor 1–10. Uji di bot Telegram asli ada di bagian "Bukti uji di bot Telegram" di bawah.
- **Uji OpenClaw otomatis oleh AI penguji, 1 Oktober 2026** (pada versi skill yang lebih lama; angka dari `examples/00-openclaw-sebelum-sesudah.md`): tanpa skill **6,5** → dengan skill **9,0** (selisih +2,5, lulus acuan kami).

**Status uji (jujur):** sudah diuji OpenClaw (sebelum/sesudah otomatis 2026-10-01; muat CLI) dan bot Telegram asli (5 Oktober 2026). Claude Code baru diuji lewat simulasi AI. Codex dan Cursor belum diuji di platform aslinya. Dasar aturan utama (masa percobaan, larangan percobaan PKWT, tenggat 30 hari BPJS Ketenagakerjaan) sudah dicocokkan dengan naskah resmi di JDIH Kemnaker, dicek ulang 15 Oktober 2026; rincian sanksi BPJS dan cara menghitung tanggal batas 3 bulan masih PERLU REVIEW (tafsir, bukan pasal eksplisit).

## Bukti uji di bot Telegram

Diuji di bot Telegram uji (bot OpenClaw asli di grup uji internal Komunitech), 5 Oktober 2026, versi 1.0.5, dengan pesan yang sama untuk dua sisi (tanpa skill dan dengan skill): paket onboarding kasir minimarket, karyawan tetap, masa percobaan 3 bulan, mulai Senin 12 Oktober 2026. Skor 1–10 dari penilai independen: tanpa skill **6,5** → dengan skill **8** (selisih +1,5), **lulus acuan kami** (dengan skill minimal 8 dan selisih minimal 1,5; hasil ini tepat di batas keduanya).

Dengan skill, paket tampil utuh dengan jadwal yang tepat (titik cek 10 November, 10 Desember, dan 9 Januari; batas masa percobaan 11 Januari 2027; evaluasi keputusan Rabu 6 Januari 2027, sebelum batas itu), SOP kasir 7 langkah, daftar BPJS, dan pengingat cek UMK. Tanpa skill, bot menulis evaluasi "paling lambat 12 Januari 2027" yang melewati batas masa percobaan dan salah menghitung jumlah hari kerja di bulan pertama.

Catatan jujur: tabel jadwal 6 kolom kurang nyaman dibaca di ponsel, urutan baris evaluasi keputusan terhadap batas masa percobaan sempat membingungkan, dan pesan sambutan WA baru dibuat bila diminta. Pengingat BPJS sudah benar di kedua sisi, jadi bukan pembeda di uji ini. Setelah uji ini skill diperbaiki (jadwal di chat kini berupa daftar bernomor urut tanggal) dan belum diuji ulang di bot Telegram. Uji sebelumnya: uji OpenClaw otomatis 1 Oktober 2026, 6,5 → 9,0 (lihat di atas).

## FAQ
**Skill ini bikin kontrak kerja juga?**
Skill ini tidak menyusun kontrak kerja; ia hanya mengingatkan kelengkapannya di checklist, termasuk aturan bahwa PKWT dilarang punya masa percobaan (PP 35/2021 Pasal 12). Untuk kontrak karyawan kontrak (PKWT), pakai skill `kontrak-kerja-pkwt`.

**Masa percobaan wajib 3 bulan?**
Masa percobaan hanya berlaku untuk karyawan tetap (PKWTT) dan **maksimal** 3 bulan (boleh lebih pendek), dengan upah tidak boleh di bawah upah minimum (UU 13/2003 Pasal 60, tetap berlaku setelah UU 6/2023). Karyawan kontrak (PKWT) sama sekali tidak boleh dikenai masa percobaan (PP 35/2021 Pasal 12); bila tetap ditulis di kontrak, klausul itu batal demi hukum dan masa kerjanya tetap dihitung. Pendaftaran BPJS tidak menunggu masa percobaan selesai: BPJS Ketenagakerjaan paling lambat 30 hari sejak mulai kerja (PP 45/2015 Pasal 4 ayat (2)), BPJS Kesehatan didaftarkan terpisah. Ringkasan ini bukan nasihat hukum; untuk kasus khusus tanyakan ke Disnaker atau konsultan ketenagakerjaan.

**Bisa dipakai untuk usaha dengan banyak cabang atau shift?**
Untuk usaha dengan shift, bisa: sebutkan jumlah shift saat meminta, lalu jadwal dan buku saku disesuaikan. Skrip jadwal juga mendukung 5 atau 6 hari kerja per minggu, libur nasional bawaan 2026/2027, dan file libur tambahan perusahaan. Untuk beberapa cabang, sebutkan perbedaan tiap cabang (misalnya jam kerja dan penanggung jawab) saat meminta; belum ada template khusus multi-cabang.

## Riwayat perubahan

Versi terkini: **1.0.7**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
