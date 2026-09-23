# Surat Peringatan Karyawan yang Adil dan Rapi

**Ceritakan masalahnya, dapat SP1/SP2/SP3 lengkap dengan fakta, dasar aturan, dan masa berlaku yang tepat.**

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

## FAQ
**Apakah SP selalu berlaku 6 bulan?**
Menurut PP 35/2021, masing-masing SP berlaku paling lama 6 bulan kecuali Perjanjian Kerja/Peraturan Perusahaan/PKB mengatur lain. Jika aturan perusahaanmu berbeda, sebutkan saja, nanti masa berlakunya menyesuaikan.

**Bisa buatkan surat PHK sekalian?**
Tidak. PHK punya prosedur dan hak pekerja yang wajib dipenuhi, sehingga sebaiknya ditangani ahli hukum ketenagakerjaan atau Disnaker. Skill ini membantu sampai tahap SP3.

**Bagaimana kalau karyawan menolak tanda tangan?**
Skill memberi langkahnya: catat penolakan, minta saksi tanda tangan, dan simpan bukti penyerahan.
