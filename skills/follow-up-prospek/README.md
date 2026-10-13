# Follow-up Prospek Tanpa Terkesan Mengejar

**Calon pembeli diam setelah ditawari? Dapat 4 pesan follow-up sopan lengkap dengan tanggal kirimnya.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Urutan pesan WhatsApp dan email hari ke-1, 3, 7, dan 14 yang sudah siap salin-kirim
- ✅ Beda situasi, beda pesan: setelah kirim penawaran, setelah demo, setelah dijawab "nanti dulu", atau setelah tanya harga lalu hilang
- ✅ Tanggal kirim dihitung otomatis, digeser dari akhir pekan atau hari libur tanpa membuat pesan menumpuk
- ✅ Setiap pesan membawa alasan baru untuk membalas, bukan sekadar "gimana, Kak?"
- ✅ Dilengkapi cara menjawab keberatan umum seperti "mahal" atau "tanya atasan dulu"

## Cocok untuk siapa
- Pemilik usaha dan tim sales B2B yang sering mengirim penawaran ke kantor, hotel, atau sekolah
- Penyedia jasa (desain, katering, laundry, konsultan) yang calon kliennya sering menghilang
- Admin online shop yang banyak menerima "tanya harga" tanpa kelanjutan

## Contoh sebelum & sesudah
**Sebelum:** Ragu mau follow-up karena takut dianggap mengganggu, akhirnya prospek dibiarkan dan hilang.

**Sesudah (cukup ketik):** "Penawaran laundry seragam ke Pak Made Hotel Taman Sari tanggal 23 September belum dibalas, bikinin follow-up"
→ Jadwal 24 Sep, 28 Sep, 2 Okt, 9 Okt (jarak antar-pesan tetap terjaga) beserta 4 pesan WA: cek diterima, gambaran layanan, tawaran uji coba 1 minggu, dan pesan pamit yang sopan.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Klien bilang nanti dulu karena belum ada budget, bikin follow-up yang sopan"
- "Habis demo aplikasi kasir ke resto, mereka belum ada kabar. Buat follow-up WA + email"
- "Banyak yang tanya harga gamis terus hilang, buat pesan follow-up-nya"

## Instalasi singkat
Salin folder `follow-up-prospek` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap per platform (termasuk Windows): lihat `docs/instalasi.md` dan `CARA-INSTAL.md` di paket.

**Hasil uji (angka nyata):** uji OpenClaw (home terisolasi), 1 Okt 2026 (v1.0.4), skor 1–10 penguji independen: tanpa skill **6,25** → dengan skill **8,0** (LULUS). Sumber: `examples/00-openclaw-sebelum-sesudah.md`. Tanpa skill, 3 dari 4 tanggal follow-up salah nama hari dan ada urgensi karangan; dengan skill, tanggal dihitung script, hari benar, tawaran baru diberi label *usulan — konfirmasi dulu*.

**Status uji (jujur):** sudah diuji di OpenClaw (uji sebelum/sesudah otomatis agent, 2026-10-01) dan Claude Code (simulasi agent). Codex dan Cursor memakai format SKILL.md yang sama; belum uji platform asli di kedua platform itu.

## FAQ
**Apakah pesannya dikirim otomatis?**
Tidak. Kamu tinggal menyalin dan mengirim sendiri sesuai tanggal yang tertera, jadi tetap terkendali.

**Kalau prospek membalas di tengah jalan?**
Hentikan urutannya dan tanggapi balasannya. Skill ini juga menyediakan contoh jawaban untuk keberatan umum.

**Apakah saya harus kasih diskon supaya prospek mau?**
Tidak. Pesan dibuat dengan nilai tambah lain seperti info, contoh hasil, atau uji coba. Diskon hanya dimasukkan jika kamu memintanya.

## Riwayat perubahan

Versi terkini: **1.0.4**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
