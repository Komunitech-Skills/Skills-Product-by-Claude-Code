# Paket Onboarding Karyawan Baru, Siap Pakai dalam 1 Menit

**Karyawan baru masuk Senin? Checklist, jadwal 90 hari, pesan sambutan, buku saku, dan formulir evaluasi langsung jadi — tinggal cetak.**

Diuji AI penguji independen di OpenClaw: 6,5 → 9,0 dari 10 (tanpa skill tanggal 30/60/90 hari hanya perkiraan dan BPJS ditulis "sesuai kebijakan toko"; dengan skill tanggal dihitung skrip dan BPJS diperlakukan wajib dengan tenggat).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- Checklist pra-hari-pertama lengkap: dokumen, pendaftaran BPJS, kontrak, perangkat kerja — supaya tidak ada yang kelewat
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

Cuplikan jadwal (dipotong; contoh dengan data fiktif, keluaran nyata skrip `jadwal_onboarding.py`):
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

**Hasil uji (angka nyata):** dua sumber, skor 1–10.
- **Uji OpenClaw otomatis agent, Sep 2026** (v1.0.6; angka dari `examples/00-openclaw-sebelum-sesudah.md`): tanpa skill **6,5** → dengan skill **9,0** (LULUS).
- **Uji bot Telegram asli, gelombang 10 (2026-10-05):** **6,5** → **8,0**. Dengan skill jadwal masa percobaan, evaluasi, dan BPJS dihitung skrip; tanpa skill tanggal evaluasi melewati batas masa percobaan.

**Status uji (jujur):** sudah diuji OpenClaw (sebelum/sesudah otomatis 2026-10-01; muat CLI) dan bot Telegram asli (gelombang 10). Claude Code (simulasi agent). Codex dan Cursor belum uji platform asli. PERLU REVIEW: dasar hukum dari sumber sekunder.

## FAQ
**Skill ini bikin kontrak kerja juga?**
Tidak. Untuk kontrak kerja karyawan kontrak (PKWT), pakai skill `kontrak-kerja-pkwt` (pembuat kontrak karyawan kontrak) — skill onboarding ini hanya mengingatkan kelengkapannya di checklist, termasuk aturan bahwa PKWT dilarang punya masa percobaan.

**Masa percobaan wajib 3 bulan?**
Masa percobaan hanya berlaku untuk karyawan tetap (PKWTT) dan **maksimal** 3 bulan (boleh lebih pendek), dengan upah tidak boleh di bawah upah minimum (UU 13/2003 Pasal 60 jo. UU 6/2023). Karyawan kontrak (PKWT) sama sekali tidak boleh dikenai masa percobaan.

**Bisa dipakai untuk usaha dengan banyak cabang atau shift?**
Bisa. Sebutkan jumlah shift dan cabang saat meminta, jadwal dan buku saku akan disesuaikan; script jadwal juga mendukung 5 atau 6 hari kerja per minggu, libur nasional bawaan 2026/2027, dan file libur tambahan perusahaan.

## Riwayat perubahan

Versi terkini: **1.0.6**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
