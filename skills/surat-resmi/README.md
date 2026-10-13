# Surat Resmi Rapi Sesuai EYD, Siap Cetak

**Sebut keperluannya, dapat surat resmi lengkap dengan kop, nomor, perihal, dan tanda tangan yang benar.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Enam jenis surat paling sering dipakai: permohonan, pemberitahuan, undangan, surat kuasa, surat keterangan, dan surat pengantar
- ✅ Ejaan mengikuti EYD Edisi V: "Yth.", "izin", "pukul 09.00", "di tempat", dan tanpa kalimat bertele-tele
- ✅ Nomor surat bulan Romawi dan nama hari dihitung otomatis, jadi tidak ada lagi "Sabtu, 3 Oktober" yang ternyata hari Jumat
- ✅ Format siap tempel ke Word/Google Docs lalu dicetak
- ✅ Catatan meterai dan batasan hukum yang jujur (kapan harus ke notaris)

## Cocok untuk siapa
- Pemilik usaha, admin kantor, dan sekretaris
- Pengurus RT/RW, karang taruna, koperasi, yayasan, dan komite sekolah
- Profesional yang sesekali harus menulis surat resmi dan ingin hasilnya rapi

## Contoh sebelum & sesudah
**Sebelum:** Mencari contoh surat di Google, menyalin, lalu mengganti isinya. Hasilnya masih memakai "Kepada Yth. :", "ijin", dan tanggal "03-10-2026".

**Sesudah (cukup ketik):** "Buatin surat undangan rapat anggota koperasi, Sabtu 3 Oktober 2026 jam 9 di balai RW, yang tanda tangan ketua Pak Hendra"
→ Surat undangan lengkap dengan kop, nomor `012/UND/KSB/IX/2026`, rincian acara, dan blok tanda tangan, siap dicetak.

**Hasil uji (OpenClaw, uji otomatis agent, 2026-10-01):** rata-rata nilai 6,75 tanpa skill menjadi 8,75 dengan skill (skala 10). Pembeda terbesar: ketepatan hari, tanggal, dan nomor surat (nilai 5 menjadi 9 pada skenario undangan yang sengaja memuat hari salah) serta format EYD V siap cetak. Jujur: menolak membuat surat keterangan kerja palsu setara (8,5 vs 8,5), karena AI biasa pun menolak. Rincian: `examples/00-openclaw-sebelum-sesudah.md`.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Surat kuasa ambil BPKB di leasing untuk staf saya"
- "Surat keterangan kerja untuk mantan karyawan, kerja dari Maret 2023 sampai Agustus 2026"
- "Surat pemberitahuan ke pelanggan: toko libur 3 hari"
- "Tolong rapikan surat saya ini sesuai EYD"

## Syarat
Nomor dan tanggal dibuat dengan Python (biasanya sudah ada di Mac/Linux; di Windows bisa dipasang gratis dari python.org). Tanpa Python, surat tetap dibuat dan kamu diingatkan untuk mengecek nama hari.

## Instalasi singkat
Salin folder `surat-resmi` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

## FAQ
**Apakah surat kuasa wajib pakai meterai?**
Meterai adalah pajak atas dokumen yang dipakai sebagai bukti, bukan syarat sahnya surat. Untuk surat kuasa dan surat keterangan yang akan diserahkan ke instansi, sebaiknya tetap dibubuhi meterai Rp10.000. Tanyakan juga ke instansi tujuan.

**Bisa pakai format nomor surat kantor saya sendiri?**
Bisa. Sebutkan saja polanya, misalnya "nomor urut/HRD/bulan Romawi/tahun".

**Bisa untuk surat dinas instansi pemerintah?**
Bisa sebagai draf. Instansi pemerintah punya pedoman tata naskah dinas sendiri, jadi sesuaikan kop dan kodenya.
