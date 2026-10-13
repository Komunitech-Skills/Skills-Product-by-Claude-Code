# Follow-up Prospek Tanpa Terkesan Mengejar

**Calon pembeli diam setelah ditawari? Dapat 4 pesan follow-up sopan lengkap dengan tanggal kirimnya.**

Diuji AI penguji independen di OpenClaw: 6,25 → 8,0 dari 10 (tanggal kirim dihitung dengan skrip sehingga nama harinya benar dan tawaran baru diberi label usulan; tanpa skill 3 dari 4 tanggal salah nama hari dan ada urgensi karangan).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Urutan pesan WhatsApp dan email hari ke-1, 3, 7, dan 14 yang sudah siap salin-kirim
- ✅ Beda situasi, beda pesan: setelah kirim penawaran, setelah demo, setelah dijawab "nanti dulu", atau setelah tanya harga lalu hilang
- ✅ Tanggal kirim dihitung otomatis, digeser dari akhir pekan dan dari hari libur yang Anda sebutkan, tanpa membuat pesan menumpuk
- ✅ Setiap pesan dirancang membawa alasan baru untuk membalas, bukan sekadar "gimana, Kak?"
- ✅ Dilengkapi cara menjawab keberatan umum seperti "mahal" atau "tanya atasan dulu"

## Cocok untuk siapa
- Pemilik usaha dan tim penjualan ke perusahaan (B2B) yang sering mengirim penawaran ke kantor, hotel, atau sekolah
- Penyedia jasa (desain, katering, laundry, konsultan) yang calon kliennya sering menghilang
- Admin online shop yang banyak menerima "tanya harga" tanpa kelanjutan

## Contoh sebelum & sesudah
**Sebelum:** Ragu mau follow-up karena takut dianggap mengganggu, akhirnya prospek dibiarkan dan hilang.

**Sesudah (cukup ketik):** "Kemarin (22 Sept) saya demo aplikasi kasir KasirPintar Fiktif ke Pak Joni, pemilik Resto Padang Rasa Minang Fiktif di Depok. Paket 199rb/bulan, gratis setup. Dia bilang bagus, tapi mau diskusi dulu sama istrinya yang pegang keuangan. Dia sempat nanya apakah bisa cetak struk ke printer lama mereka (Epson TM-U220) — jawabannya bisa. Nama saya Rudi. Bikinin follow-up WA ya."

Cuplikan hasil (contoh dengan data fiktif; dipotong dari `examples/01-setelah-demo-aplikasi-kasir.md`; H+1 = 1 hari setelah kontak terakhir):
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

**Hasil uji (angka nyata):** uji OpenClaw (home terisolasi), 1 Okt 2026 (v1.0.4), skor 1–10 penguji independen: tanpa skill **6,25** → dengan skill **8,0** (LULUS). Sumber: `examples/00-openclaw-sebelum-sesudah.md`. Tanpa skill, 3 dari 4 tanggal follow-up salah nama hari dan ada urgensi karangan; dengan skill, tanggal dihitung script, hari benar, tawaran baru diberi label *usulan — konfirmasi dulu*.

**Status uji (jujur):** sudah diuji di OpenClaw (uji sebelum/sesudah otomatis agent, 2026-10-01) dan Claude Code (simulasi agent). Codex dan Cursor memakai format SKILL.md yang sama; belum uji platform asli di kedua platform itu.

## FAQ
**Apakah pesannya dikirim otomatis?**
Tidak. Anda tinggal menyalin dan mengirim sendiri sesuai tanggal yang tertera, jadi tetap terkendali.

**Kalau prospek membalas di tengah jalan?**
Hentikan urutannya dan tanggapi balasannya. Skill ini juga menyediakan contoh jawaban untuk keberatan umum.

**Apakah saya harus kasih diskon supaya prospek mau?**
Tidak. Pesan dibuat dengan nilai tambah lain seperti info, contoh hasil, atau uji coba. Diskon hanya dimasukkan jika Anda memintanya.

## Riwayat perubahan

Versi terkini: **1.0.4**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
