# Pilah Keluhan, Balas yang Mendesak Dulu

**Puluhan keluhan masuk sekaligus? Tempel saja, dan dapatkan urutan kerja P1-P3 (P1 = paling mendesak), tindakan pertama, serta draf balasan siap kirim untuk tiap keluhan.**

Diuji AI penguji independen di OpenClaw: 4,5 → 8,4 dari 10 (urutan prioritas dengan batas waktu platform yang sesuai referensi, dan draf balasan tanpa janji refund yang belum Anda putuskan). Di bot Telegram asli selisihnya lebih kecil: 7,5 → 8,5.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) hanya bila Anda menyerahkan file tabel (CSV) berisi banyak keluhan; untuk keluhan yang ditempel di chat, Python tidak diperlukan. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Tahu mana yang dibalas dulu.** Keluhan yang mengancam lapor/bintang 1, menyangkut keamanan, mendekati tenggat platform, atau bernilai besar naik ke atas daftar, lengkap dengan alasan pendek.
- ✅ **Dikelompokkan menurut penyebab:** barang rusak/tidak sesuai, belum sampai/kurir, salah kirim, COD gagal/ditolak, komplain layanan, minta retur/refund, atau memang bukan keluhan.
- ✅ **Draf balasan siap kirim** untuk tiap keluhan: empati yang menyebut masalahnya, langkah nyata, dan janji waktu yang bisa ditepati (`[isian]` = tanda kosong untuk Anda isi, bila Anda belum menyebutnya). Tidak menjanjikan refund atau ganti sebelum Anda memutuskan.
- ✅ **Daftar keputusan untuk pemilik** dan **pola** (tiga keluhan sebab sama berarti ada akar masalah), supaya masalah yang sama tidak terulang.
- ✅ **Menjaga privasi dan etika:** rekap untuk grup dirancang tanpa nama, nomor HP, atau alamat pelanggan (tetap periksa sebelum dibagikan); tidak membantu menghapus ulasan atau menyamar jadi pembeli; fakta toko tidak dikarang.

## Cocok untuk siapa
- Pemilik toko online di Shopee, Tokopedia, TikTok Shop, WhatsApp, atau Instagram yang punya admin sedikit.
- Pemilik kafe/restoran yang mengurus ulasan Google, GoFood, GrabFood.
- Jasa (servis AC, salon, bengkel, klinik non-medis) yang menerima komplain lewat WA.
- Pemilik yang ingin tahu keluhan mana yang harus ia pegang sendiri.
- **Bukan untuk:** membalas satu chat biasa (pakai skill Balas Chat CS, `balas-chat-cs`), menulis balasan ulasan satu per satu dengan nada merek (skill Balas Ulasan Bintang 1, `balas-ulasan-pelanggan`), atau nasihat hukum.

## Contoh sebelum & sesudah
**Sebelum:** 8 keluhan masuk dari 5 aplikasi. Admin membalas dari yang paling atas, sehingga pembeli yang mengancam lapor ke Shopee baru dibalas siang, dan pembeli COD bernilai Rp875.000 tertunda sampai besok.

**Sesudah (cukup tempel keluhannya):** cuplikan keluarannya (contoh rancangan pembuat dengan data fiktif, bukan hasil uji platform; dari `examples/01-toko-fashion-8-keluhan-campur.md`):

```
**Ringkasan:** 8 masuk: 3 P1, 4 P2, 1 pertanyaan biasa (bukan keluhan). 3 perlu keputusan Anda (K5, K2, K8).

| Urut. | Keluhan | Prioritas dan alasan |
|---|---|---|
| 1 | K5 COD ditolak, set gamis | P1: nilai Rp875.000 di atas batas Rp500.000, paket sudah kembali ke toko |
| 2 | K2 belum sampai (Shopee) | P1: ancam lapor dan bintang 1, sudah menunggu 3 hari, mengulang keluhan |
| 3 | K8 blouse sobek, ulasan bintang 1 | P1: tuduhan penipuan di ulasan publik |
…
**K2 (Shopee)**
> Halo Kak, mohon maaf paketnya belum sampai dan kabarnya terlambat dari kami. Itu pasti bikin cemas. Hari ini kami hubungi ekspedisi dan kabari Kakak lagi sebelum [isian: jam, mis. 16.00]. Boleh kirim tangkapan layar status resinya, Kak?
…
```

Disusul draf balasan untuk semua keluhan dan 3 hal yang perlu keputusan pemilik.

## Cara pakai
Setelah terpasang, tempel keluhan dan ceritakan singkat usahanya, misalnya:
- "Ini 8 keluhan hari ini dari Shopee dan WA. Mana yang duluan dibalas? Siapkan balasannya."
- "Ada 5 ulasan bintang 1-2 baru di kafe saya. Tolong pilah dan buatkan balasannya."
- "Banyak yang minta refund minggu ini, tolong urutkan."

Tidak perlu lengkap. Info yang kurang ditandai `[isian: ...]`, lalu ditanyakan maksimal tiga hal di akhir. Anda yang membaca dan mengirim balasannya satu per satu; skill ini tidak mengirim apa pun sendiri.

## Instalasi singkat
Salin folder `triase-keluhan-pelanggan` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` yang disertakan dalam paket. Python tidak wajib; hanya dipakai bila Anda menyerahkan berkas CSV (file tabel dari Excel) berisi banyak keluhan.

**Hasil uji (OpenClaw, uji otomatis agent, diuji pada v1.0.1; versi terkini 1.0.2):** rata-rata nilai 4,5 tanpa skill menjadi 8,4 dengan skill (skala 10), dari 8 keluhan campur dan permintaan yang menjebak (hapus ulasan, balas pakai akun lain, minta nomor pembeli). Rincian dan balasan utuh: `examples/00-openclaw-sebelum-sesudah.md`. Diuji langsung di OpenClaw saja; Claude Code, Codex, dan Cursor belum diuji langsung (format skill-nya sama). Angka di bagian "Bukti uji di bot Telegram" di bawah berasal dari uji tersendiri (satu skenario dengan topik lain), jadi tidak sama dengan angka ini.

## Bukti uji di bot Telegram

Uji terakhir: 10 Oktober 2026, di bot Telegram sungguhan (OpenClaw) di grup uji internal Komunitech, memakai skill versi 1.0.2. Pesan yang sama dikirim di dua percakapan baru, sekali tanpa skill dan sekali dengan skill, lalu dinilai 1–10 oleh penilai AI.
- Skor: tanpa skill **7,5** → dengan skill **8,5** (selisih +1,0).
- Hasil: **belum lulus acuan kami** (acuan: skor dengan skill minimal 8 dan selisih minimal 1,5). Skor 8,5 sudah tercapai, tetapi selisihnya baru +1,0.

Dengan skill, keluhan diurutkan P1/P2 lengkap dengan batas waktu tiap platform, ada draf balasan untuk tiap keluhan, dan nomor HP pembeli disamarkan. Tanpa skill, urutannya sudah benar tetapi drafnya lebih tipis, sehingga bedanya baru 1,0 poin.

Uji sebelumnya (6 Oktober 2026): dengan skill mendapat skor 8,5, tetapi jawaban tanpa skill tidak tercatat sehingga selisihnya belum bisa dinilai.

## FAQ
**Apakah skill ini yang membalas pelanggan?**
Tidak. Skill ini menyiapkan urutan kerja dan draf. Anda yang mengirim, satu per satu, lewat aplikasi tempat keluhan masuk.

**Bisakah membantu menghapus ulasan buruk atau meminta pelanggan mengganti bintang?**
Tidak. Yang bisa: menyelesaikan masalahnya, membalas ulasan secara sopan, dan melaporkan ulasan yang benar-benar melanggar aturan platform lewat fitur laporan platform.

**Apakah tenggat retur/refund Shopee, Tokopedia, dan TikTok Shop sudah pasti?**
Tidak pasti: platform sering mengubahnya. Skill ini memakai ketentuan umum yang dicek per 2026-10-05 dan mengingatkan Anda mencocokkan dengan Pusat Penjual sebelum menjanjikan sesuatu ke pelanggan. Angka yang belum terkonfirmasi di halaman resmi platform sengaja tidak dipakai sebagai batas waktu.

## Catatan
Bukan nasihat hukum. Ringkasan aturan di `references/dasar-hukum-dan-platform.md` membantu menulis dengan hati-hati, bukan pengganti konsultasi hukum.

Skill ini adaptasi (dengan perubahan besar dan penambahan lokal) dari skill `ticket-triage` dan `customer-escalation` di `anthropics/knowledge-work-plugins` (Apache-2.0). Tidak berafiliasi dengan Anthropic, Shopee, Tokopedia, TikTok, Google, atau GoFood; nama dipakai sekadar menyebut produk. Lihat `ATTRIBUTION.md`, `NOTICE`, dan `LICENSE-APACHE`.

## Riwayat perubahan

Versi terkini: **1.0.2**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
