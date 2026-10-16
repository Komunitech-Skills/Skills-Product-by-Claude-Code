# Follow-up Prospek Tanpa Terkesan Mengejar

**Calon pembeli diam setelah ditawari? Dapat 4 pesan follow-up sopan lengkap dengan tanggal kirimnya.**

Diuji AI penguji independen di OpenClaw: 6,25 → 8,0 dari 10 pada uji ulang v1.0.4 (1 Okt 2026; uji pertama 6,25 → 7,75 belum lulus). Dengan skill: tanggal kirim dihitung dengan skrip (program hitung kecil) sehingga nama harinya benar dan tawaran baru diberi label usulan. Tanpa skill: 3 dari 4 tanggal salah nama hari dan ada kesan mendesak yang dikarang.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Urutan pesan WhatsApp dan email hari ke-1, 3, 7, dan 14 yang sudah siap salin-kirim
- ✅ Beda situasi, beda pesan: setelah kirim penawaran, setelah demo, setelah dijawab "nanti dulu", atau setelah tanya harga lalu hilang
- ✅ Tanggal kirim dihitung otomatis, digeser dari akhir pekan dan dari hari libur yang Anda sebutkan, dengan jarak antar-pesan dijaga agar tidak menumpuk
- ✅ Setiap pesan dirancang membawa alasan baru untuk membalas, bukan sekadar "gimana, Kak?"
- ✅ Dilengkapi cara menjawab keberatan umum seperti "mahal" atau "tanya atasan dulu"

## Cocok untuk siapa
- Pemilik usaha dan tim penjualan ke perusahaan (B2B) yang sering mengirim penawaran ke kantor, hotel, atau sekolah
- Penyedia jasa (desain, katering, laundry, konsultan) yang calon kliennya sering menghilang
- Admin online shop yang banyak menerima "tanya harga" tanpa kelanjutan

## Contoh sebelum & sesudah
**Sebelum:** Ragu mau follow-up karena takut dianggap mengganggu, akhirnya prospek dibiarkan dan hilang.

**Sesudah (cukup ketik):** "Kemarin (22 Sept) saya demo aplikasi kasir KasirPintar Fiktif ke Pak Joni, pemilik Resto Padang Rasa Minang Fiktif di Depok. Paket 199rb/bulan, gratis setup. Dia bilang bagus, tapi mau diskusi dulu sama istrinya yang pegang keuangan. Dia sempat nanya apakah bisa cetak struk ke printer lama mereka (Epson TM-U220) — jawabannya bisa. Nama saya Rudi. Bikinin follow-up WA ya."

Cuplikan hasil (dipotong; dari uji simulasi Claude Code oleh penguji independen, 23 Sep 2026, data fiktif, `examples/01-setelah-demo-aplikasi-kasir.md`; H+1 = 1 hari setelah kontak terakhir):
> ### Jadwal follow-up – Pak Joni, Resto Padang Rasa Minang Fiktif (setelah demo)
> Kontak terakhir (H+0): Selasa, 22 September 2026
>
> | Ke | Rencana | Tanggal kirim | Catatan |
> |---|---|---|---|
> | 1 | H+1 | Rabu, 23 September 2026 (hari ini) | - |
> | 2 | H+3 | Jumat, 25 September 2026 | - |
> | 3 | H+7 | Selasa, 29 September 2026 | - |
> | 4 | H+14 | Selasa, 6 Oktober 2026 | - |
>
> …
>
> ### Pesan ke-1 · Rabu, 23 September 2026 · WA
> Selamat siang, Pak Joni 🙏 Saya Rudi dari KasirPintar Fiktif, terima kasih atas waktunya kemarin. Ringkasnya: paket Rp 199.000/bulan, setup gratis, dan bisa langsung cetak struk ke printer Epson TM-U220 yang sudah ada di resto. Ada poin yang ingin Bapak tambahkan sebelum dibahas dengan Ibu?

Hasil lengkapnya juga memuat tiga pesan berikutnya dan aturan main (jam kirim, cara menjawab "mahal" atau "nanti dulu").

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Klien bilang nanti dulu karena belum ada budget, bikin follow-up yang sopan"
- "Habis demo aplikasi kasir ke resto, mereka belum ada kabar. Buat follow-up WA + email"
- "Banyak yang tanya harga gamis terus hilang, buat pesan follow-up-nya"

## Instalasi singkat
Salin folder `follow-up-prospek` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** uji OpenClaw otomatis oleh agent penguji (lingkungan uji terpisah), 1 Okt 2026 (v1.0.4), skor 1–10 penguji independen: tanpa skill **6,25** → dengan skill **8,0** (LULUS). Sumber: `examples/00-openclaw-sebelum-sesudah.md`. Tanpa skill, 3 dari 4 tanggal follow-up salah nama hari dan ada kesan mendesak yang dikarang; dengan skill, tanggal dihitung skrip, hari benar, tawaran baru diberi label *usulan — konfirmasi dulu*. Catatan jujur: uji pertama (sebelum perbaikan) 6,25 → 7,75 belum lulus, angka di atas dari uji ulang. Pada skenario prospek yang minta tidak dihubungi, kedua sisi sama-sama menolak dengan benar (tanpa skill 7, dengan skill 7,5) dan skill tidak dibaca oleh AI.

**Status uji (jujur):** sudah diuji di OpenClaw (uji sebelum/sesudah otomatis agent, 2026-10-01) dan Claude Code (simulasi agent). Codex dan Cursor memakai format skill yang sama; belum uji platform asli di kedua platform itu. Bot Telegram asli belum diuji.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji internal Komunitech, 16 Okt 2026) dengan pesan yang sama: "Kemarin (22 Sept) saya demo aplikasi kasir KasirPintar Fiktif ke Pak Joni, pemilik Resto Padang Rasa Minang Fiktif di Depok. Paket 199rb/bulan, gratis setup. Dia bilang bagus, tapi mau diskusi dulu sama istrinya yang pegang…". Tanpa skill skor **6,5** → dengan skill skor **8,5** (selisih +2, lulus acuan kami). Dengan skill, bot sadar demo sudah 25 hari lewat, lalu menyusun 4 pesan WA bertanggal pasti (Senin 19 Okt s.d. Senin 2 Nov), termasuk ajakan telepon 10 menit bersama Bapak & Ibu. Tanpa skill, bot hanya membuat satu pesan yang masih menulis "terima kasih … kemarin", seolah demo baru sehari lalu. Catatan jujur: Hasilnya berupa urutan 4 pesan lengkap dengan aturan main, lebih panjang dari satu pesan WA yang diminta. Pesan ke-2 memuat contoh fitur (laporan penjualan di HP) yang perlu Anda pastikan memang ada di produk sebelum dikirim, dan jadwal disusun dengan anggapan belum pernah ada follow-up sebelumnya.

## FAQ
**Apakah pesannya dikirim otomatis?**
Tidak. Anda tinggal menyalin dan mengirim sendiri sesuai tanggal yang tertera, jadi tetap terkendali.

**Kalau prospek membalas di tengah jalan?**
Hentikan urutannya dan tanggapi balasannya. Skill ini juga menyediakan contoh jawaban untuk keberatan umum.

**Apakah saya harus kasih diskon supaya prospek mau?**
Tidak. Pesan dibuat dengan nilai tambah lain seperti info, contoh hasil, atau uji coba. Diskon hanya dimasukkan jika Anda memintanya.

## Riwayat perubahan

Versi terkini: **1.0.4**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
