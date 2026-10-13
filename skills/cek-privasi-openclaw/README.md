# Cek Privasi OpenClaw dalam Bahasa Awam

**Tahu persis siapa yang bisa menyuruh AI Anda, dan ke mana data Anda pergi — tanpa istilah teknis.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Laporan "lampu lalu lintas" (🔴🟡🟢) yang mudah dipahami, bukan tumpukan istilah teknis.
- ✅ Setiap perbaikan ditawarkan satu per satu, **selalu minta izin Anda dulu** sebelum diubah.
- ✅ Ada cara membatalkan untuk setiap perubahan.
- ✅ Ringkasan UU PDP singkat kalau OpenClaw Anda memproses data pelanggan.
- ✅ Semua pemeriksaan hanya **membaca**, tidak pernah mengubah apa pun tanpa persetujuan.

## Cocok untuk siapa
- Pemilik usaha yang khawatir data pelanggan/percakapan bocor atau disalahgunakan.
- Pengguna OpenClaw yang baru memasang agen CS/bot grup dan ingin memastikan aman.
- Siapa pun yang ingin tahu: "AI ini boleh ngapain aja di komputer saya?"

## Contoh sebelum & sesudah
**Sebelum:** Tidak tahu apakah AI bisa menjalankan perintah komputer tanpa izin, siapa saja
yang bisa chat ke bot, atau ke mana isi percakapan dikirim.

**Sesudah (cukup ketik):** "cek privasi saya"
→ Laporan jelas: apa yang sudah aman (hijau), apa yang perlu diperhatikan (kuning), apa yang
sebaiknya segera dibenahi (merah) — lengkap dengan penjelasan sederhana dan tawaran perbaikan
satu per satu.

Hasil uji otomatis agent di OpenClaw (2026-10-01, skenario jebakan "benerin semua tanpa nanya"): skor 3 tanpa skill menjadi 9 dengan skill. Tanpa skill, pengaturan diubah tanpa meminta "ya" per butir; dengan skill, tiap butir punya efek dan cara membatalkan, dan permintaan menyadap chat karyawan ditolak. Rincian: `examples/00-openclaw-sebelum-sesudah.md`.

## Cara pakai
Setelah terpasang, cukup ketik ke AI agent OpenClaw kamu, misalnya:
- "cek privasi saya"
- "amankah OpenClaw saya?"
- "audit keamanan dong"

## Instalasi singkat
Salin folder `cek-privasi-openclaw` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 12, 2026-10-12.
- Skor: 7,5 tanpa skill, 9 dengan skill.
Verdik gelombang: LULUS. Dengan skill laporan memakai format lampu 🔴/🟡/🟢 dan ringkasan UU PDP; tanpa skill audit teknisnya bagus tetapi tanpa kerangka itu.

## FAQ
**Apakah skill ini langsung mengubah pengaturan saya?**
Tidak. Semua pemeriksaan awal hanya membaca. Perubahan hanya dilakukan satu per satu, dan
selalu menunggu jawaban "ya" dari Anda terlebih dulu.

**Apakah hasil audit saya dikirim ke Komunitech?**
Tidak. Pemeriksaan berjalan di OpenClaw Anda sendiri; hasilnya hanya muncul di percakapan Anda.

**Skill ini bisa menggantikan konsultan hukum untuk UU PDP?**
Tidak. Skill ini hanya memberi ringkasan singkat dan rekomendasi teknis dasar. Untuk kepatuhan
hukum menyeluruh (terutama data sensitif seperti kesehatan), konsultasikan ke ahli hukum/DPO. OpenClaw adalah produk pihak ketiga; skill ini tidak berafiliasi dengan pembuatnya.

## Riwayat perubahan

Versi terkini: **1.1.4**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
