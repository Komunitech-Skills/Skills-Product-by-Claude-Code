# Surat Peringatan Karyawan yang Adil dan Rapi

**Ceritakan masalahnya, dapat SP1/SP2/SP3 lengkap dengan fakta, dasar aturan, dan masa berlaku yang tepat.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Tingkat SP disarankan secara proporsional (bukan emosi), lengkap dengan alasannya
- ✅ Keluhan seperti "dia malas" diubah menjadi fakta terukur: tanggal, jumlah, dan bukti
- ✅ Tanggal berakhir SP dihitung otomatis dengan script, dan bisa mengecek apakah SP lama masih berlaku
- ✅ Bonus draf Berita Acara Klarifikasi dan catatan proses: panggil dulu, dengar penjelasan, lalu minta tanda tangan
- ✅ Dasar aturan terbaru (PP 35/2021) beserta disclaimer. Untuk urusan PHK, kamu diarahkan ke ahli hukum

## Cocok untuk siapa
- Pemilik UMKM, toko, restoran, dan bengkel yang mengelola karyawan sendiri
- Staf HR/admin personalia di usaha kecil dan menengah
- Supervisor yang perlu menegur timnya secara tertulis dan profesional

## Contoh sebelum & sesudah
**Sebelum:** SP ditulis saat emosi ("kamu malas, kalau begini lagi dipecat!"). Tidak ada tanggal kejadian dan masa berlakunya tidak jelas, jadi lemah bila dipersoalkan.

**Sesudah (cukup ketik):** "Buatin SP buat Rina, kasir, bulan ini telat 6 kali lebih dari 30 menit, sudah ditegur lisan 2x"
→ SP1 lengkap dengan tanggal keterlambatan, dasar aturan, harapan perbaikan yang terukur, masa berlaku "23 September 2026 s.d. 22 Maret 2027", kolom tanda tangan dan saksi, serta berita acara klarifikasi.

**Hasil uji (angka nyata):** uji di OpenClaw, 1 Okt 2026 (v1.0.6), skor 1-10 dari agen penguji independen: tanpa skill 3 → dengan skill 8,6.
- Tugas 1: minta SP2, padahal SP1 (10 Maret 2026) sudah berakhir 9 September 2026. Tanpa skill, AI langsung membuat SP2. Dengan skill, masa berlaku dicek: SP1 lama sudah tidak berlaku, jadi yang aman SP1 baru (berlaku s.d. 31 Maret 2027) lengkap dengan berita acara klarifikasi.
- Tugas 2: kasir mengambil uang laci Rp500.000 dan pemilik minta "langsung SP3 dan surat PHK". Tanpa skill, AI membuat dan menyimpan SK PHK yang berlaku hari itu juga. Dengan skill, AI tidak menyusun SP3/surat PHK, tetapi menawarkan kronologi, berita acara klarifikasi, dan skorsing dengan upah tetap dibayar, serta menyebut syarat PP 35/2021 Pasal 52 ayat (2).
- Jujur: isi hukumnya belum ditinjau ahli hukum ketenagakerjaan, jadi pakai sebagai draf.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Karyawan gudang saya salah kirim paket 5 kali, dia masih kena SP1 bulan Juli. Buatkan SP berikutnya."
- "SP1 terbit 2 Januari 2026, sekarang dia melanggar lagi. Masih berlaku nggak?"
- "Template SP3 untuk pelanggaran merokok di area bengkel"

## Syarat
Hitung masa berlaku memakai Python (biasanya sudah ada di Mac/Linux; di Windows bisa dipasang gratis dari python.org). Tanpa Python, tanggal tetap dihitung manual dengan rumus yang jelas.

## Instalasi singkat
Salin folder `surat-peringatan-karyawan` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis oleh agen AI, bukan oleh manusia) dan Claude Code (simulasi agen penguji). Codex dan Cursor memakai format SKILL.md yang sama, tetapi belum kami uji langsung.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 4, 2026-10-03.
- Tanpa skill: https://t.me/c/4407409583/584/606 — skor: lihat catatan gelombang
- Dengan skill: https://t.me/c/4407409583/585/609 — skor: lihat catatan gelombang
Verdik gelombang: — — TANPA langsung membuat SP2; DENGAN menahan karena SP1 sudah berakhir masa berlakunya dan menyarankan SP1 baru kecuali peraturan perusahaan mengatur lain (beda paling jelas).

## Catatan penting
- Draf ini bantuan administrasi, **bukan nasihat hukum**. Masa berlaku SP 6 bulan mengikuti PP 35/2021 Pasal 52 (per 23 September 2026), kecuali perjanjian kerja / peraturan perusahaan / PKB mengatur lain.
- Isinya belum ditinjau ahli hukum ketenagakerjaan. Untuk pencurian, kekerasan, atau PHK, konsultasikan ke ahli hukum atau Disnaker sebelum bertindak.

## FAQ
**Apakah SP selalu berlaku 6 bulan?**
Menurut PP 35/2021, masing-masing SP berlaku paling lama 6 bulan kecuali Perjanjian Kerja/Peraturan Perusahaan/PKB mengatur lain. Jika aturan perusahaanmu berbeda, sebutkan saja, nanti masa berlakunya menyesuaikan.

**Bisa buatkan surat PHK sekalian?**
Tidak. PHK punya prosedur dan hak pekerja yang wajib dipenuhi, sehingga sebaiknya ditangani ahli hukum ketenagakerjaan atau Disnaker. Skill ini membantu sampai tahap SP3.

**Bagaimana kalau karyawan menolak tanda tangan?**
Skill memberi langkahnya: catat penolakan, minta saksi tanda tangan, dan simpan bukti penyerahan.

## Riwayat perubahan

Versi terkini: **1.0.6**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
