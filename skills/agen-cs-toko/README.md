# Karyawan CS AI yang Hafal Isi Toko Anda

**Draf balasan pelanggan siap tempel dalam hitungan detik — Anda tetap yang memutuskan dan mengirim.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Basis pengetahuan toko (harga, stok, ongkir, retur, FAQ) ditulis sekali, dipakai berulang — jawaban konsisten, tidak beda-beda tiap admin.
- ✅ Draf balasan lengkap dengan **tingkat keyakinan** dan **daftar yang perlu dicek**, jadi Anda tahu kapan harus konfirmasi manual.
- ✅ Aturan eskalasi otomatis: komplain berat, refund, ancaman, data sensitif, dan pertanyaan medis/hukum langsung ditandai untuk Anda tangani sendiri.
- ✅ Aman: tidak pernah mengarang harga/stok, dan tidak pernah mengirim pesan sendiri ke pelanggan lewat WhatsApp Web — 100% mode Copilot.
- ✅ Rekap harian pertanyaan terbanyak & pertanyaan yang belum ada jawabannya, jadi FAQ Anda makin lengkap dari hari ke hari.

## Cocok untuk siapa
- Pemilik toko online/offline dengan chat pelanggan yang sering menumpuk (WhatsApp, Shopee, Tokopedia).
- Klinik/praktik kecil yang ingin membalas pertanyaan jadwal & info umum lebih cepat, dengan aturan tegas: tidak memberi saran medis (aturan medisnya belum direview tenaga medis).
- Siapa pun yang sudah pakai OpenClaw dan ingin laporan CS otomatis dikirim ke Telegram tiap hari.

## Contoh sebelum & sesudah
**Sebelum:** Admin membaca ulang daftar harga tiap kali ada pertanyaan, kadang lupa update stok, balasan beda gaya antar admin, dan komplain berat kadang dibalas buru-buru tanpa dicek dulu ke pemilik.

**Sesudah (cukup ketik):** "Ini chat pelanggan: 'Kak espresso 250ml sama americano beda harga gak? Bisa COD area Bintaro?'"
→
```
**Keyakinan:** Tinggi
**Eskalasi:** Tidak

**Draf 1:**
Halo Kak! Beda ya — espresso 250ml Rp 22.000, americano 250ml Rp 20.000 🙏
Untuk COD, area Bintaro termasuk yang kami layani. Mau pesan berapa cup, Kak?

**Perlu dicek admin sebelum kirim:**
- (tidak ada — semua fakta ada di basis pengetahuan)
```
Tinggal tempel ke WhatsApp/marketplace, kirim.

**Hasil uji (OpenClaw, uji otomatis agent, 2026-10-01):** rata-rata nilai 6,0 tanpa skill menjadi 8,75 dengan skill (skala 10), pada dua skenario (membangun CS toko hijab; komplain dengan ancaman, data KTP/rekening, dan permintaan bot WA auto-reply). Tanpa skill, agent menawarkan memasang auto-reply di nomor WA pribadi tanpa peringatan risiko; dengan skill, ada penolakan beralasan, mode Copilot, eskalasi ke pemilik, dan draf penahan. Rincian: `examples/00-openclaw-sebelum-sesudah.md`.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Siapkan asisten CS toko saya, ini daftar harganya..."
- "Ini chat pelanggan, buatkan draf balasannya."
- "Buatkan rekap harian pertanyaan CS ke Telegram saya tiap jam 8 malam."

## Instalasi singkat
Salin folder `agen-cs-toko` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 9, 2026-10-05.
- Tanpa skill: https://t.me/c/4407409583/829/842 — skor 4,5
- Dengan skill: https://t.me/c/4407409583/830/846 — skor 8,5
Verdik gelombang: LULUS — DENGAN menolak auto-balas WA dengan alasan yang benar (WhatsApp Web tidak resmi, nomor bisa diblokir), langsung menawarkan mode Copilot, dan menyerahkan 7 template balasan + aturan nada + alur admin; TANPA hanya bertanya, tidak memberi satu template pun, dan menawarkan memandu pairing WA, plus pesan sistem/gateway bocor ke chat.

## FAQ
**Apakah bot ini otomatis membalas pelanggan di WhatsApp?**
Tidak. Skill ini bekerja mode **Copilot**: bot menyiapkan draf, Anda yang menempel dan mengirim. Ini sengaja, karena WhatsApp Web bukan kanal resmi dan berisiko nomor diblokir bila dipakai kirim otomatis.

**Apakah bot bisa mengarang harga atau stok kalau saya belum isi datanya?**
Tidak. Jika info belum ada di basis pengetahuan, draf akan menandai bagian itu "perlu dicek admin" — tidak pernah mengira-ngira.

**Bisa dipakai untuk klinik/praktik dokter?**
Bisa, untuk info jadwal, cara daftar, dan edukasi umum. Bot **tidak akan** memberi diagnosis, saran dosis, atau triase — pertanyaan medis selalu diarahkan ke dokter. Batas medis ini belum direview tenaga medis, jadi draf untuk pasien tetap dicek staf atau dokter sebelum dikirim.

## Riwayat perubahan

Versi terkini: **1.0.11**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
