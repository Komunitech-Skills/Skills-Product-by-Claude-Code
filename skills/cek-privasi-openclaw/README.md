# Cek Privasi OpenClaw dalam Bahasa Awam

**Tahu persis siapa yang bisa menyuruh AI Anda, dan ke mana data Anda pergi — tanpa istilah teknis.**

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

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

## FAQ
**Apakah skill ini langsung mengubah pengaturan saya?**
Tidak. Semua pemeriksaan awal hanya membaca. Perubahan hanya dilakukan satu per satu, dan
selalu menunggu jawaban "ya" dari Anda terlebih dulu.

**Apakah hasil audit saya dikirim ke Komunitech?**
Tidak. Pemeriksaan berjalan di OpenClaw Anda sendiri; hasilnya hanya muncul di percakapan Anda.

**Skill ini bisa menggantikan konsultan hukum untuk UU PDP?**
Tidak. Skill ini hanya memberi ringkasan singkat dan rekomendasi teknis dasar. Untuk kepatuhan
hukum menyeluruh (terutama data sensitif seperti kesehatan), konsultasikan ke ahli hukum/DPO.

## Catatan revisi 1.1.4 (2026-10-01)
- Uji OpenClaw 2026-10-01: agent sempat menjalankan `chmod` sebelum menampilkan daftar perbaikan. Kini semua perubahan (config, `chmod`/izin file, `--fix`) hanya dijalankan setelah daftar lengkap ditampilkan dan pemilik menjawab "ya"; "gak usah nanya" sebelum melihat daftar bukan persetujuan.
- Permintaan menyadap/memata-matai chat orang lain: penolakan kini wajib ditulis lengkap & sopan di balasan itu sendiri (alasan UU ITE Pasal 31 & UU PDP + alternatif sah), bukan hanya "tetap saya tolak".
