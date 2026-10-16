# Surat Peringatan Karyawan yang Adil dan Rapi

**Ceritakan masalahnya, dapat SP1/SP2/SP3 (Surat Peringatan pertama, kedua, ketiga) lengkap dengan fakta, dasar aturan, dan masa berlaku yang dihitung.**

Diuji AI penguji independen di OpenClaw: 3 → 8,6 dari 10 (tanpa skill, SP2 langsung dibuat padahal SP1 sebelumnya sudah berakhir masa berlakunya; dengan skill, masa berlaku dicek dulu).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Tingkat SP disarankan secara proporsional (bukan emosi), lengkap dengan alasannya
- ✅ Keluhan seperti "dia malas" diubah menjadi fakta terukur: tanggal, jumlah, dan bukti
- ✅ Tanggal berakhir SP dihitung otomatis dengan script (program kecil), dan bisa mengecek apakah SP lama masih berlaku
- ✅ Bonus draf Berita Acara Klarifikasi (catatan resmi bahwa karyawan sudah dipanggil dan didengar penjelasannya) dan catatan proses: panggil dulu, dengar penjelasan, lalu minta tanda tangan
- ✅ Dasar aturan (PP 35/2021, berlaku per 23 September 2026) beserta disclaimer. Untuk urusan PHK (pemutusan hubungan kerja), Anda diarahkan ke ahli hukum

## Cocok untuk siapa
- Pemilik UMKM, toko, restoran, dan bengkel yang mengelola karyawan sendiri
- Staf HR/admin personalia di usaha kecil dan menengah
- Supervisor yang perlu menegur timnya secara tertulis dan profesional

## Contoh sebelum & sesudah
**Sebelum:** SP ditulis saat emosi ("kamu malas, kalau begini lagi dipecat!"). Tidak ada tanggal kejadian dan masa berlakunya tidak jelas, jadi lemah bila dipersoalkan.

**Sesudah (cukup ketik):** "Tolong buatkan SP lanjutan untuk Bayu Pratama, staf packing di online shop skincare saya (Glowria Skin, Tangerang). Dia masih kena SP1 nomor 004/SP-1/GS/VII/2026 tanggal 14 Juli 2026 karena salah kirim juga. Sekarang salah kirim lagi 5 paket: tanggal 8, 10, 11, 15, dan 17 September, … Kemarin (21 Sept) sudah saya panggil … Saya pemiliknya, Rudi Hartono."
→ AI mengecek dulu apakah SP1 lama masih berlaku, menentukan tingkat SP berikutnya, lalu menyusun surat dan berita acara klarifikasi. Cuplikan dari uji simulasi Claude Code, `examples/01-sp2-staf-packing-salah-kirim.md` (data fiktif; di contoh ini SP1 masih berlaku):
```
Tingkat SP yang disarankan: SP2 (Surat Peringatan Kedua).
Alasannya, SP1 tanggal 14 Juli 2026 berlaku sampai 13 Januari 2027 (dicek dengan script).
Kelima pelanggaran (8–17 September 2026) terjadi saat SP1 masih aktif, dan jenis pelanggarannya sama. …
…
A. Pelanggaran
Berdasarkan laporan komplain pembeli dan rekaman video packing, Saudara tercatat salah
mengirim barang sebanyak 5 (lima) paket, yaitu pada tanggal 8, 10, 11, 15, dan 17 September
2026 (daftar nomor pesanan dan komplain terlampir).
…
D. Masa berlaku
Surat Peringatan ini berlaku selama 6 (enam) bulan terhitung sejak tanggal 23 September 2026
sampai dengan 22 Maret 2027.
…
```
(Surat lengkap dengan kolom tanda tangan, saksi, dan berita acara klarifikasi ada di folder `examples/`.)

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Karyawan gudang saya salah kirim paket 5 kali, dia masih kena SP1 bulan Juli. Buatkan SP berikutnya."
- "SP1 terbit 2 Januari 2026, sekarang dia melanggar lagi. Masih berlaku nggak?"
- "Template SP3 untuk pelanggaran merokok di area bengkel"

## Syarat
Hitung masa berlaku memakai Python (biasanya sudah ada di Mac/Linux; di Windows bisa dipasang gratis dari python.org). Tanpa Python, tanggal tetap dihitung manual dengan rumus yang jelas.

## Instalasi singkat
Salin folder `surat-peringatan-karyawan` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex (belum diuji langsung) | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor (belum diuji langsung) | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

## Hasil uji (jujur)

**Hasil uji (angka nyata):** uji di OpenClaw, 1 Okt 2026 (v1.0.6), skor 1-10 dari agen penguji independen: tanpa skill 3 → dengan skill 8,6.
- Tugas 1: minta SP2, padahal SP1 (10 Maret 2026) sudah berakhir 9 September 2026. Tanpa skill, AI langsung membuat SP2. Dengan skill, masa berlaku dicek: SP1 lama sudah tidak berlaku, jadi yang lebih tepat SP1 baru (berlaku s.d. 31 Maret 2027) lengkap dengan berita acara klarifikasi.
- Tugas 2: kasir mengambil uang laci Rp500.000 dan pemilik minta "langsung SP3 dan surat PHK". Tanpa skill, AI membuat dan menyimpan SK PHK (surat keputusan pemutusan hubungan kerja) yang berlaku hari itu juga. Dengan skill, AI tidak menyusun SP3/surat PHK, tetapi menawarkan kronologi, berita acara klarifikasi, dan skorsing (dibebastugaskan sementara) dengan upah tetap dibayar, serta menyebut syarat PP 35/2021 Pasal 52 ayat (2).
- Jujur: skor tanpa skill (3) dan dengan skill (8,6) berasal dari putaran uji yang berbeda di hari yang sama: sisi tanpa skill dari putaran ketiga, sisi dengan skill dari putaran keempat (4 sesi tugas 2, semuanya memicu skill dan tanpa kesalahan hukum). Sumber: `examples/00-openclaw-sebelum-sesudah.md`.
- Jujur: isi hukumnya belum ditinjau ahli hukum ketenagakerjaan, jadi pakai sebagai draf.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis oleh agen AI, bukan oleh manusia) dan Claude Code (simulasi agen penguji). Codex dan Cursor memakai format SKILL.md yang sama, tetapi belum kami uji langsung.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji internal Komunitech), 2026-10-03.
- Tanpa skill: skor tidak dicatat
- Dengan skill: skor tidak dicatat
(Uji ini tidak memberi skor angka.) Hasil: TANPA langsung membuat SP2; DENGAN menahan karena SP1 sudah berakhir masa berlakunya dan menyarankan SP1 baru kecuali peraturan perusahaan mengatur lain (beda paling jelas).

## Catatan penting
- Draf ini bantuan administrasi, **bukan nasihat hukum**. Masa berlaku SP 6 bulan mengikuti PP 35/2021 Pasal 52 (per 23 September 2026), kecuali perjanjian kerja / peraturan perusahaan / PKB mengatur lain.
- Isinya belum ditinjau ahli hukum ketenagakerjaan. Untuk pencurian, kekerasan, atau PHK, konsultasikan ke ahli hukum atau Disnaker (Dinas Tenaga Kerja) sebelum bertindak.

## FAQ
**Berapa lama masa berlaku SP?**
Menurut PP 35/2021, masing-masing SP berlaku paling lama 6 bulan kecuali Perjanjian Kerja/Peraturan Perusahaan/PKB mengatur lain. Jika aturan perusahaan Anda berbeda, sebutkan saja, nanti masa berlakunya menyesuaikan.

**Bisa buatkan surat PHK sekalian?**
Belum, dan itu disengaja. PHK punya prosedur dan hak pekerja yang wajib dipenuhi, sehingga sebaiknya ditangani ahli hukum ketenagakerjaan atau Disnaker. Skill ini membantu sampai tahap SP3.

**Bagaimana kalau karyawan menolak tanda tangan?**
Skill memberi langkahnya: catat penolakan, minta saksi tanda tangan, dan simpan bukti penyerahan.

## Riwayat perubahan

Versi terkini: **1.0.6**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
