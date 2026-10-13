# Temukan & Prioritaskan Calon Pelanggan

**Susun profil pelanggan ideal, cari calon pelanggan dari sumber publik, dan tahu siapa yang paling layak dihubungi dulu.**

## Manfaat
- ✅ Profil pelanggan ideal (ICP) tersusun jelas, bukan sekadar tebakan
- ✅ Arahan sumber pencarian publik & sah — tanpa scraping ilegal, tanpa beli database
- ✅ Skor kualifikasi prospek dihitung script, bukan dikira-kira, langsung terurut Panas/Hangat/Dingin
- ✅ Draf sapaan singkat per prospek (WA/email/LinkedIn) yang patuh UU PDP — untuk pesan pertama lengkap 3 varian + cek otomatis, pakai `pesan-prospek-wa`
- ✅ Terhubung ke `follow-up-prospek` dan `proposal-kerjasama` untuk tahap berikutnya

## Cocok untuk siapa
- Pemilik UMKM yang mau ekspansi ke pelanggan baru tapi belum tahu mulai dari mana
- Tim sales B2B yang punya banyak nama calon klien tapi bingung mana yang diprioritaskan
- Freelancer/agensi kecil yang mencari klien baru secara mandiri

## Contoh sebelum & sesudah
**Sebelum:** Menghubungi siapa saja tanpa arah, banyak waktu terbuang ke prospek yang tidak cocok.

**Sesudah (cukup ketik):** "Bantu saya cari calon pelanggan untuk jasa cleaning kantor di Surabaya, sekalian bikin pesan WA pembukanya"
→ ICP, daftar sumber pencarian, dan pesan pembuka siap kirim.

**Hasil uji (OpenClaw, uji otomatis agent, v1.0.4):** rata-rata nilai 7,75 tanpa skill menjadi 8,5 dengan skill (skala 10). Dari file CSV 8 kafe di Bekasi, skor berbobot dihitung script dan hasilnya terurut dari Rumah Kopi Kemang Pratama (96, Panas) sampai Kafe Sudut Pekayon (34, Dingin); sapaan WA-nya sopan, jujur, dan memberi opsi "boleh diabaikan". Tanpa skill, nilai hanya dijumlah tanpa bobot dan sapaan WA mengarang klaim "langsung dari petani". Catatan jujur: bedanya tipis, karena tanpa skill pun AI sudah menolak scraping dan beli database, dan tiga prospek teratasnya sama. Rincian: `examples/00-openclaw-sebelum-sesudah.md`. Claude Code diuji lewat simulasi agent; Codex dan Cursor belum diuji langsung (format skill-nya sama).

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Bantu susun ICP untuk produk kemasan makanan ramah lingkungan"
- "Saya punya 30 nama perusahaan di CSV, mana yang paling prioritas dihubungi?"
- "Bikinkan pesan pembuka LinkedIn yang sopan buat calon klien baru"

## Instalasi singkat
Salin folder `riset-calon-pelanggan` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

## FAQ
**Apakah skill ini mengambil data otomatis dari internet?**
Tidak. Skill ini tidak melakukan koneksi internet atau scraping. Kamu yang mengumpulkan data dari sumber publik (Google Maps, situs perusahaan, dll.) sesuai arahan, lalu skill membantu menyusun dan menskor.

**Skor kualifikasi prospek itu dihitung dari mana?**
Dari penilaian 0-5 yang kamu/tim sales isi sendiri untuk 4 hal: kecocokan profil ideal, kejelasan kebutuhan, kemampuan bayar, dan akses ke pengambil keputusan. Script menghitung skor akhirnya secara konsisten, bukan agent menebak.

**Bedanya dengan `follow-up-prospek`?**
Skill ini untuk **mencari & menyaring** calon pelanggan baru, plus draf sapaan singkat. Untuk menyusun & memeriksa pesan pertama ke satu prospek secara mendalam → `pesan-prospek-wa`. `follow-up-prospek` dipakai setelah prospek sudah dihubungi tapi belum deal/belum balas.

## Catatan revisi 1.0.4 (2026-10-01)
- Dari uji OpenClaw sebelum/sesudah: AI sempat menyarankan memasang skill lain "dari ClawHub" (keliru). Kini hanya menyebut nama skill Komunitech terkait bila relevan dan sudah terpasang, tanpa menyebut cara/sumber instalasi.
