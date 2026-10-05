# Laporan Kantor Rapi dalam Hitungan Detik

**Dari chat berantakan jadi laporan siap kirim ke atasan, tim, atau klien — tanpa ngarang angka.**

## Manfaat
- ✅ Ubah catatan chat/poin acak/transkrip voice note jadi laporan 3P (Progres-Rencana-Kendala) yang rapi
- ✅ Satu skill untuk 9 jenis komunikasi kantor: laporan mingguan, harian, newsletter, pengumuman, FAQ, memo, laporan insiden
- ✅ Format siap tempel langsung ke WA grup kantor/Telegram (`*tebal*`, bullet pendek) atau email formal
- ✅ Tidak pernah mengarang progres/angka — info yang kurang ditandai jelas atau ditanyakan
- ✅ Nada otomatis menyesuaikan: sopan-formal khas kantor Indonesia atau santai-profesional ala startup

## Cocok untuk siapa
- Pemilik UMKM/usaha kecil-menengah yang minta tim lapor progres mingguan
- Admin/office manager yang bertugas menyusun newsletter atau pengumuman internal
- Team lead yang harus laporan ke atasan/klien tapi tidak sempat menyusun format rapi
- HR yang sering menjawab pertanyaan berulang karyawan (cuti, THR, jam kerja)
- Siapa saja yang WFH/WFO dan diminta laporan harian singkat

## Contoh sebelum & sesudah
**Sebelum:** Catatan chat tim berantakan — "udah kelar redesign landing page", "fitur
checkout masih nunggu API vendor", "server sempet down 2 jam Selasa udah difix", "minggu
depan mulai notifikasi WA".

**Sesudah (cukup ketik):** "Buatin laporan mingguan ke bos dari chat ini, tim Produk."
→
```
🧩 *Tim Produk* — 15–19 Sep 2026
*Progres:* Redesign landing page selesai. Sempat ada gangguan server ±2 jam pada Selasa
akibat disk penuh, sudah diperbaiki.
*Rencana:* Mulai mengerjakan fitur notifikasi WA minggu depan.
*Kendala:* Fitur checkout masih menunggu API payment dari vendor, perkiraan selesai
minggu depan.
```
Siap tempel langsung ke WA grup atau email — tidak perlu dirapikan lagi.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Buatkan laporan 3P mingguan untuk tim Marketing dari poin-poin ini: ..."
- "Rapikan jadi newsletter kantor bulan ini dari chat grup HR"
- "Buat pengumuman libur Idul Fitri, kantor libur 20-24 Sep"
- "Tolong susun FAQ karyawan dari pertanyaan-pertanyaan ini soal cuti dan THR"
- "Buat laporan insiden: server down 2 jam kemarin, sudah diperbaiki"

Jika info penting kurang (nama tim, periode, penerima), agent akan tanya sekali dalam satu
pesan singkat — bukan bolak-balik tanya jawab.

## Instalasi singkat
Salin folder `laporan-status-kantor` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

## FAQ
**Apakah skill ini menghitung nominal THR atau gaji?**
Tidak. Skill ini hanya menyusun teks pengumuman/laporan. Untuk menghitung nominal, gunakan
skill `hitung-thr` atau skill hitung terkait, lalu hasilnya bisa dimasukkan ke pengumuman.

**Apakah harus punya akses Slack/Google Drive/email seperti versi aslinya (sumber
internasional)?**
Tidak perlu. Skill ini dirancang untuk bekerja langsung dari bahan yang kamu berikan
(tempel chat, ketik poin-poin, atau tempel transkrip voice note) — tanpa integrasi apa pun.

**Bisa untuk kantor yang santai/startup, bukan cuma yang formal?**
Bisa. Sebut saja "santai" atau "gaya startup" saat minta, atau agent akan mengikuti gaya
bahan mentah yang kamu berikan. Defaultnya sopan-formal karena mayoritas kantor Indonesia
lebih aman dengan nada itu, terutama untuk laporan ke atasan/pemilik dan klien.

## Catatan revisi 1.0.3 (2026-10-01)
- Dari uji OpenClaw sebelum/sesudah: AI sempat memasukkan gaji dan THR per orang ke teks pengumuman grup dan menghitung THR sendiri. Kini pengumuman grup tidak pernah memuat nominal per orang (hanya tanggal bayar & dasar aturan); rincian per orang hanya lewat pesan pribadi/HR. Perhitungan THR diarahkan ke skill `hitung-thr` bila terpasang; bila tidak, AI menjelaskan nominal perlu dihitung terpisah.

## Catatan revisi 1.0.4 (2026-10-02)
- Aturan privasi pengumuman grup kini ditaruh paling atas dan **tetap berlaku walau skill lain ikut dipakai** (mis. `hitung-thr`, `gaji-umkm`): gaji/THR per orang tidak pernah masuk teks grup; rincian per orang dipisah di blok khusus pemilik/HR. (Temuan uji 2026-10-02: saat dipasang bersama `hitung-thr`, nominal per orang sempat masuk teks grup.)
- AI tidak menawarkan menyambungkan WhatsApp atau kirim otomatis ke grup — hasilnya draf yang kamu tempel sendiri.
- Tanggal libur/cuti bersama yang tidak kamu sebut: maksimal satu pencarian, selebihnya ditandai `[isi: ...]` agar balasan tidak macet.
