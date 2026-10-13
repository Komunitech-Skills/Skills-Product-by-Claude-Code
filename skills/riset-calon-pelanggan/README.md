# Temukan & Prioritaskan Calon Pelanggan

**Susun profil pelanggan ideal, cari calon pelanggan dari sumber publik, dan tahu siapa yang paling layak dihubungi dulu.**

Diuji AI penguji independen di OpenClaw: 7,75 → 8,5 dari 10 (selisih tipis: keduanya menolak menyedot data situs otomatis dan beli database, tetapi hanya dengan skill skor prospek berbobot dihitung skrip dan sapaan WA tidak mengarang klaim).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Profil pelanggan ideal (ICP) tersusun jelas, bukan sekadar tebakan
- ✅ Arahan sumber pencarian publik & sah — tanpa menyedot data situs secara ilegal (scraping), tanpa beli database
- ✅ Skor kualifikasi prospek dihitung script, bukan dikira-kira, langsung terurut Panas/Hangat/Dingin
- ✅ Draf sapaan singkat per prospek (WA/email/LinkedIn) yang memperhatikan UU PDP (Pelindungan Data Pribadi); untuk pesan pertama yang lengkap (3 varian + pengecekan otomatis), pakai skill "Pesan Pertama ke Calon Pelanggan" (`pesan-prospek-wa`)
- ✅ Bisa dilanjutkan dengan skill "Follow-up Prospek" (`follow-up-prospek`) dan "Proposal Kerja Sama" (`proposal-kerjasama`) untuk tahap berikutnya

## Cocok untuk siapa
- Pemilik UMKM yang mau ekspansi ke pelanggan baru tapi belum tahu mulai dari mana
- Tim sales B2B yang punya banyak nama calon klien tapi bingung mana yang diprioritaskan
- Freelancer/agensi kecil yang mencari klien baru secara mandiri

## Contoh sebelum & sesudah
**Sebelum:** Menghubungi siapa saja tanpa arah, banyak waktu terbuang ke prospek yang tidak cocok.

**Sesudah (cukup ketik):** "Kak aku jualan kopi bubuk arabika & robusta buat kafe di Bekasi. Ini aku udah punya daftar 8 kafe di file prospek-kafe.csv, udah aku nilai sendiri 0-5. Mana yang harus aku samperin/chat duluan? Sekalian bikinin sapaan WA singkat buat yang paling prioritas ya. Nama aku Dimas dari Kopi Gunung Halu"

Cuplikan balasan (dipotong; ICP = profil pelanggan ideal, PIC = orang yang berwenang memutuskan; dari `examples/00-openclaw-sebelum-sesudah.md`):
```
Udah aku hitung skor kualifikasi dari CSV kamu (`prospek-kafe.csv`) pakai script skill, bobot default: Cocok ICP 30%, Kebutuhan 30%, Kemampuan Bayar 20%, Akses PIC 20%. Semua 8 baris kehitung, gak ada yang dilewati.

🔥 Panas — samperin/chat duluan (urutan prioritas):
1. Rumah Kopi Kemang Pratama (Rawalumbu) — skor 96
2. Kopi Senja Harapan Indah (Bekasi Utara) — skor 86
3. Kedai Kopi Lima Langkah (Bekasi Barat) — skor 82
…
❄️ Dingin — skip dulu:
8. Kafe Sudut Pekayon (Bekasi Selatan) — skor 34 (cocok ICP & kebutuhan sama-sama rendah)

Draf sapaan WA — Rumah Kopi Kemang Pratama:
Selamat siang Kak, perkenalkan saya Dimas dari Kopi Gunung Halu. Saya lihat Rumah Kopi Kemang Pratama salah satu kafe di area Rawalumbu, Bekasi — kami supply kopi bubuk arabika & robusta untuk kafe. Kalau saat ini terbuka untuk kenalan supplier baru, boleh saya kirim info produk & harganya? Mohon maaf kalau kurang berkenan, boleh diabaikan saja.
```

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Bantu susun ICP untuk produk kemasan makanan ramah lingkungan"
- "Saya punya 30 nama perusahaan di CSV, mana yang paling prioritas dihubungi?"
- "Bikinkan pesan pembuka LinkedIn yang sopan buat calon klien baru"

## Instalasi singkat
Salin folder `riset-calon-pelanggan` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** satu sumber, skor 1–10.
- **Uji OpenClaw, uji otomatis agent, v1.0.4** (angka dari `examples/00-openclaw-sebelum-sesudah.md`): rata-rata nilai 7,75 tanpa skill menjadi 8,5 dengan skill. Dari file CSV 8 kafe di Bekasi, skor berbobot dihitung script dan hasilnya terurut dari Rumah Kopi Kemang Pratama (96, Panas) sampai Kafe Sudut Pekayon (34, Dingin); sapaan WA-nya sopan, jujur, dan memberi opsi "boleh diabaikan". Tanpa skill, nilai hanya dijumlah tanpa bobot dan sapaan WA mengarang klaim "langsung dari petani". Catatan jujur: bedanya tipis, karena tanpa skill pun AI sudah menolak scraping dan beli database, dan tiga prospek teratasnya sama.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis agent) dan Claude Code (simulasi agent); Codex dan Cursor belum diuji langsung (format skill-nya sama).

## FAQ
**Apakah skill ini mengambil data otomatis dari internet?**
Tidak. Skill ini tidak melakukan koneksi internet atau scraping. Anda yang mengumpulkan data dari sumber publik (Google Maps, situs perusahaan, dll.) sesuai arahan, lalu skill membantu menyusun dan menskor.

**Skor kualifikasi prospek itu dihitung dari mana?**
Dari penilaian 0-5 yang Anda/tim sales isi sendiri untuk 4 hal: kecocokan profil ideal, kejelasan kebutuhan, kemampuan bayar, dan akses ke pengambil keputusan. Script menghitung skor akhirnya secara konsisten, bukan agent menebak.

**Bedanya dengan `follow-up-prospek`?**
Skill ini untuk **mencari & menyaring** calon pelanggan baru, plus draf sapaan singkat. Untuk menyusun & memeriksa pesan pertama ke satu prospek secara mendalam → skill "Pesan Pertama ke Calon Pelanggan" (`pesan-prospek-wa`). `follow-up-prospek` dipakai setelah prospek sudah dihubungi tapi belum deal/belum balas.

## Riwayat perubahan

Versi terkini: **1.0.4**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
