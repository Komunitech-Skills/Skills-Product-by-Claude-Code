# Paket Onboarding Karyawan Baru, Siap Pakai dalam 1 Menit

**Karyawan baru masuk Senin? Checklist, jadwal 90 hari, pesan sambutan, buku saku, dan formulir evaluasi langsung jadi — tinggal cetak.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- Checklist pra-hari-pertama lengkap: dokumen, pendaftaran BPJS, kontrak, perangkat kerja — tidak ada yang kelewat
- Jadwal onboarding H1, minggu 1, dan checkpoint 30-60-90 hari dengan **tanggal dihitung otomatis** (bukan dikira-kira, termasuk libur nasional & cuti bersama 2026/2027 bawaan), lengkap dengan penanggung jawab
- Khusus karyawan tetap (PKWTT): **batas hukum akhir masa percobaan dan tanggal evaluasi keputusannya dihitung terpisah**, evaluasi selalu dijadwalkan sebelum batas hukum — bukan sekadar checkpoint 90 hari yang bisa kelewat
- Panduan buddy singkat, jadwal check-in mingguan, dan target per jabatan (kasir, barista, mekanik, dll.) supaya karyawan baru tidak merasa dilepas begitu saja
- Pesan sambutan WhatsApp/email siap kirim ke karyawan baru + pengumuman ke tim
- Buku saku karyawan ringkas (jam kerja, cuti, seragam, aturan HP) yang mudah dipahami karyawan awam
- Formulir evaluasi akhir orientasi/masa percobaan yang objektif (versi terpisah untuk PKWT tanpa istilah "lulus masa percobaan"), plus retrospektif onboarding untuk perbaikan proses berikutnya
- Varian siap pakai untuk toko, kafe, bengkel, klinik, kantor jasa, dan gudang

## Cocok untuk siapa
- Pemilik UMKM dan kantor kecil yang baru pertama kali merekrut karyawan
- Staf HR/admin personalia yang ingin proses onboarding lebih rapi dan konsisten
- Manajer/supervisor yang bertanggung jawab menyambut dan membimbing karyawan baru

## Contoh sebelum & sesudah
**Sebelum:** Karyawan baru datang, diperkenalkan seadanya, langsung disuruh kerja tanpa panduan tertulis. Dokumen BPJS baru diurus setelah ditegur, dan tidak ada evaluasi jelas di akhir masa percobaan.

**Sesudah (cukup ketik):** "Buatin paket onboarding buat kasir baru namanya Sinta, mulai Senin 28 September 2026, PKWTT, kerja 6 hari seminggu"
→ Checklist dokumen & BPJS, jadwal lengkap dengan tanggal pasti (checkpoint 90 hari 26 Desember 2026 sebagai pemantauan rutin, **batas hukum akhir masa percobaan 27 Desember 2026**, dan evaluasi keputusan lanjut/tidak dijadwalkan 19 Desember 2026 — sebelum batas hukum), pesan WA sambutan, buku saku, panduan buddy & target, dan formulir evaluasi — semua siap pakai (hasil nyata dari script, lihat `SKILL.md` bagian Contoh).

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Buatkan paket onboarding lengkap untuk barista baru di kafe saya, mulai bulan depan."
- "Bikin rencana 30-60-90 hari untuk mekanik baru di bengkel, kerja PKWT 6 bulan."
- "Tolong buatkan buku saku karyawan untuk toko kelontong saya."
- "Formulir evaluasi akhir masa percobaan untuk admin kantor."

## Syarat
Jadwal onboarding dihitung otomatis memakai Python (biasanya sudah ada di Mac/Linux; di Windows bisa dipasang gratis dari python.org). Tanpa Python, tanggal tetap dihitung manual dengan rumus yang jelas — skill tetap berguna.

## Instalasi singkat
Salin folder `sop-onboarding` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 10, 2026-10-05.
- Tanpa skill: https://t.me/c/4407409583/865/871 — skor 6,5
- Dengan skill: https://t.me/c/4407409583/866/874 — skor 8
Verdik gelombang: LULUS — DENGAN memberi paket utuh dengan jadwal yang tepat (checkpoint, batas masa percobaan 11 Jan 2027, evaluasi keputusan 6 Jan 2027), SOP kasir 7 langkah, checklist BPJS, dan cek UMK; TANPA menulis evaluasi "paling lambat 12 Jan 2027" yang melewati batas 11 Jan buatannya sendiri.

## FAQ
**Skill ini bikin kontrak kerja juga?**
Tidak. Untuk kontrak kerja karyawan kontrak (PKWT), pakai skill `kontrak-kerja-pkwt` — skill onboarding ini hanya mengingatkan kelengkapannya di checklist, termasuk aturan bahwa PKWT dilarang punya masa percobaan.

**Masa percobaan wajib 3 bulan?**
Masa percobaan hanya berlaku untuk karyawan tetap (PKWTT) dan **maksimal** 3 bulan (boleh lebih pendek), dengan upah tidak boleh di bawah upah minimum (UU 13/2003 Pasal 60 jo. UU 6/2023). Karyawan kontrak (PKWT) sama sekali tidak boleh dikenai masa percobaan.

**Bisa dipakai untuk usaha dengan banyak cabang atau shift?**
Bisa. Sebutkan jumlah shift dan cabang saat meminta, jadwal dan buku saku akan disesuaikan; script jadwal juga mendukung 5 atau 6 hari kerja per minggu, libur nasional bawaan 2026/2027, dan file libur tambahan perusahaan.

## Riwayat perubahan

Versi terkini: **1.0.6**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
