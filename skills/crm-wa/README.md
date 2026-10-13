# CRM WhatsApp Tanpa Langganan, Cukup Lewat Chat

**Calon pembeli tercatat rapi, tiap pagi tahu siapa yang harus disapa, dan pesan follow-up sudah disiapkan. Data tetap di komputer Anda sendiri.**

Diuji AI penguji independen di OpenClaw: 4,5 → 9,0 dari 10 (draf WhatsApp siap kirim dengan tautan wa.me dan nilai prospek yang dihitung; tanpa skill menyarankan broadcast otomatis yang berisiko). Uji ulang setelah perbaikan: 5,0 → 8,5; uji ringkas terakhir (v1.0.8, satu skenario): 7 → 8.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Calon pembeli lebih kecil kemungkinan terlupa.** Setiap pagi Anda bisa menerima daftar "terlambat", "hari ini", dan "besok", lengkap dengan catatan obrolan terakhir dan nilai potensinya. Bisa dijadwalkan terkirim ke Telegram Anda (jadwal otomatis ke Telegram belum diuji langsung).
- ✅ **Pesan follow-up siap kirim dalam satu klik.** Draf yang sopan dan tidak memaksa disesuaikan dengan tahapnya: sapaan awal, lanjutan, "balas 1/2/3", sampai pesan pamit. Tinggal klik tautan, WhatsApp terbuka dengan teks terisi, periksa, lalu tekan Kirim sendiri. Tidak ada kiriman otomatis, sehingga risiko nomor Anda diblokir jauh lebih kecil (tetap tidak ada jaminan).
- ✅ **Cukup cerita seperti biasa.** "Pak Budi nawar jadi 4 juta, follow-up Jumat" langsung tercatat: tahapnya berubah, nilainya tersimpan, jadwalnya terpasang. Nomor dalam berbagai format (0812…, +62…, pakai spasi/strip) dirapikan otomatis, dan nomor yang sudah ada tidak dicatat dobel.
- ✅ **Tahu jualan Anda jalan ke mana.** Rekap berisi jumlah & nilai per tahap, deal (transaksi jadi) bulan ini, konversi (persen calon pembeli yang jadi order), rata-rata lama sampai deal, alasan batal terbanyak, dan **sumber pembeli paling menghasilkan** (IG, TikTok, marketplace, referensi, walk-in). Angka dihitung dengan skrip (program hitung kecil) dan rumusnya bisa ditampilkan.
- ✅ **Tanpa biaya bulanan.** Pengganti fitur dasar CRM (aplikasi pencatat calon pembeli dan pelanggan) berlangganan, mis. Qontak CRM yang pada September 2026 kami catat mulai sekitar Rp400 ribu/bulan (harga bisa berubah, cek situs mereka), untuk usaha yang jualannya lewat chat. Bisa impor/ekspor Excel (CSV, yaitu file tabel) dan ada cadangan otomatis.

## Cocok untuk siapa
- Usaha yang jualannya lewat chat WhatsApp: katering, kue & hampers, jasa (desain, servis, tukang, wedding organizer, travel), properti, otomotif, reseller/grosir, toko online yang banyak ditanya lewat DM.
- Pemilik atau admin sales yang selama ini mencatat calon pembeli di kepala, buku, atau label chat WA.
- Member yang memakai OpenClaw dan ingin daftar follow-up masuk Telegram tiap pagi (jadwal otomatis belum diuji langsung).

**Kurang cocok:** tim sales besar yang butuh banyak pengguna sekaligus di perangkat berbeda, atau yang ingin mengirim promo massal otomatis (skill ini sengaja tidak mengirim apa pun).

## Contoh sebelum & sesudah
**Sebelum:** calon pembeli tersebar di chat WA, DM IG, dan catatan HP. Yang minta "nanti saya kabari" sering terlupa. Akhir bulan tidak tahu berapa yang jadi order dan dari mana pembeli terbaik datang.

**Sesudah (cukup ketik):** "Hari ini saya harus follow-up siapa?"
```
FOLLOW-UP CRM - Kamis, 24 September 2026 (WIB)
Terlambat: 0 | Hari ini: 2 | Besok: 1 | Belum dijadwalkan: 0
Nilai prospek yang perlu disapa: Rp 6.450.000

HARI INI (2)
1. K0006 Kak Nia | Instagram | Baru | Rp 6.000.000 | hampers lebaran 30 paket | FU 24 Sep (hari ini)
2. K0001 Bu Rina | Instagram | Baru | Rp 450.000 | kue ulang tahun 2 tingkat | FU 24 Sep (hari ini)

K0006 Kak Nia [sapaan-awal]:
Halo Kak Nia, terima kasih sudah menghubungi Dapur Bu Sari. Saya Sari. Soal hampers lebaran 30 paket,
boleh saya bantu jelaskan pilihan dan harganya? Kira-kira dibutuhkan untuk kapan ya?
https://wa.me/6281200001006?text=Halo%20Kak%20Nia...
```
Akhir bulan: "rekap CRM bulan ini" → rekap yang antara lain memuat: calon pembeli (lead) masuk 6, deal 2 senilai Rp 5.525.000, konversi 33,3%, sumber terbaik: Referensi.
(Cuplikan di atas dipersingkat dari keluaran asli skrip pada data fiktif, dijalankan pembuat skill, bukan hasil uji independen. Contoh lengkap: `examples/contoh-sesi-toko-kue.md`.)

## Cara pakai
Setelah terpasang, cukup ketik ke AI agent Anda, misalnya:
- "Pakai CRM untuk usaha saya, nama usahanya Dapur Bu Sari" (sekali di awal)
- "Catat: Bu Rina dari IG, 0812-xxxx-xxxx, tanya kue ulang tahun, sekitar 450 ribu"
- "Pak Budi nawar jadi 4 juta, follow-up Jumat" / "Bu Rina jadi order 4,2 juta" / "Dewi batal, sudah beli di tempat lain"
- "Follow-up hari ini siapa saja?" → klik tautan, kirim sendiri, lalu bilang "sudah kukirim ke Bu Rina"
- "Rekap CRM bulan ini" / "sumber pembeli paling bagus dari mana?"
- "Masukkan daftar kontak ini" (kirim file CSV dari Excel/Google Contacts) / "cek nomor dobel"
- "Kirim daftar follow-up ke Telegram saya tiap pagi jam 8" (OpenClaw; jadwal otomatisnya belum diuji langsung)

## Instalasi singkat
Salin folder `crm-wa` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

Butuh **Python 3.8+** (gratis di python.org; Mac/Linux biasanya sudah ada). Tidak butuh internet, akun, atau API key. Data tersimpan di folder `KomunitechData/crm/` di komputer Anda, dengan cadangan otomatis di `KomunitechData/crm/backup-crm/`. Tanpa Python pun skill tetap membantu dengan tabel CRM manual di Excel.

**Hasil uji (angka nyata):** uji OpenClaw (uji otomatis agent, folder kerja bersih terpisah untuk tiap skenario), skor 1–10 penguji independen. Sumber semua angka: `examples/00-openclaw-sebelum-sesudah.md`.
- 1 Okt 2026, uji pertama (dua skenario; versi skill saat itu tidak tercatat): tanpa skill **4,5** → dengan skill **9,0** (LULUS).
- 2 Okt 2026, uji ulang v1.0.7 (dua skenario): **5,0** → **8,5** (LULUS).
- 2 Okt 2026, uji ulang v1.0.8 (satu skenario): **7** → **8** (LULUS).

Dengan skill: draf WA + tautan WhatsApp (wa.me), kontak batal dikecualikan, total nilai prospek dihitung; tanpa skill: menyarankan broadcast otomatis yang berisiko. Di bot Telegram uji (2026-10-02): selisih positif, draf terstruktur (lihat bagian Bukti uji di bawah).

**Status uji (jujur):** sudah diuji di OpenClaw (uji muat CLI, uji platform otomatis agent, uji sebelum/sesudah 2026-10-01) dan Claude Code (simulasi agent). Codex dan Cursor belum kami uji langsung.

## Yang perlu Anda tahu (jujur)
- **Tidak mengirim pesan sendiri.** Skill hanya menyiapkan draf + tautan wa.me; Anda yang menekan Kirim. Ini disengaja: kiriman otomatis lewat WhatsApp tidak resmi bisa membuat nomor diblokir.
- **Tidak membaca chat WhatsApp otomatis.** Perkembangan dicatat dari cerita Anda (atau chat yang Anda tempel ke agent).
- **Satu komputer, satu file data (database).** Jangan buka file yang sama dari dua komputer lewat Google Drive/Dropbox.
- **Data pribadi pelanggan.** Nomor HP tersimpan hanya di komputer Anda. Jika pengingat dikirim ke Telegram, isinya (nama, nomor, tautan) tersimpan di chat Telegram Anda; ada pilihan versi disamarkan. Pelanggan minta datanya dihapus? Cukup bilang "hapus data Bu Rina".
- Pengingat terjadwal hanya berjalan saat komputer dan Gateway OpenClaw (program OpenClaw yang berjalan di latar belakang) menyala.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji internal Komunitech), 2026-10-02 (tiga giliran uji bot-ke-bot). Versi skill saat uji: 1.0.6 (versi terkini saat dibaca: lihat baris Versi terkini di bawah).
- Tanpa skill: (pesan di grup uji internal Komunitech) — skor angka tidak dicatat di catatan uji itu
- Dengan skill: (pesan di grup uji internal Komunitech) — skor angka tidak dicatat di catatan uji itu
Verdik: DENGAN (giliran 1–2) mendeteksi nama ganda dan mencatat status Deal + DP; TANPA mencatat ke CSV buatan sendiri. Catatan jujur: giliran 3 DENGAN salah karena tercampur data uji lama usaha lain, sehingga draf bertanda tangan orang lain dan prospek usaha lain ikut direkap.

Diperbaiki di versi 1.0.7 (cek identitas usaha sebelum mencatat; versi terkini 1.0.10), belum diuji ulang di bot Telegram.

## FAQ
**Apakah data pelanggan saya dikirim ke internet?**
Tidak. Script CRM tidak memakai internet sama sekali; semuanya ada di satu file di komputer Anda. Yang keluar hanya teks yang Anda minta dikirim ke Telegram Anda sendiri (lewat OpenClaw), dan pesan yang Anda kirim sendiri lewat WhatsApp. Seperti percakapan AI lainnya, apa yang Anda ketik ke AI agent tetap diproses oleh penyedia model AI yang Anda pakai.

**Bisa kirim pesan ke semua pelanggan sekaligus?**
Tidak, dan itu disengaja. Setiap pesan dikirim manusia satu per satu supaya risiko nomor WhatsApp Anda diblokir lebih kecil dan pesannya tetap personal. Promo hanya untuk pelanggan yang sudah setuju dikabari (ditandai label `setuju-promo`); agent menyiapkan draf + tautan per orang, Anda kirim satu per satu. Pembeli marketplace (Shopee/Tokopedia) dianggap belum setuju, jadi promo untuk mereka lewat fitur voucher/promosi di dalam marketplace. (Skill Broadcast WA terpisah, bila Anda punya, hanya membantu menulis variasi teks — tetap dikirim satu per satu.)

**Saya sudah punya daftar pelanggan di Excel/HP. Harus ketik ulang?**
Tidak. Simpan sebagai CSV (Excel: *Save As → CSV*; Google Contacts: *Export → Google CSV*), kirim ke agent, lalu periksa pratinjaunya. Nomor dirapikan otomatis, nomor dobel dan baris yang bermasalah dilewati dan disebutkan barisnya.

## Riwayat perubahan

Versi terkini: **1.0.10**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
