# Pilah Keluhan, Balas yang Mendesak Dulu

**Puluhan keluhan masuk sekaligus? Tempel saja, dan dapatkan urutan kerja P1-P3, tindakan pertama, serta draf balasan siap kirim untuk tiap keluhan.**

## Manfaat
- ✅ **Tahu mana yang dibalas dulu.** Keluhan yang mengancam lapor/bintang 1, menyangkut keamanan, mendekati tenggat platform, atau bernilai besar naik ke atas daftar, lengkap dengan alasan pendek.
- ✅ **Dikelompokkan menurut penyebab:** barang rusak/tidak sesuai, belum sampai/kurir, salah kirim, COD gagal/ditolak, komplain layanan, minta retur/refund, atau memang bukan keluhan.
- ✅ **Draf balasan siap kirim** untuk tiap keluhan: empati yang menyebut masalahnya, langkah nyata, dan janji waktu yang bisa ditepati (`[isian]` bila Anda belum menyebutnya). Tidak menjanjikan refund atau ganti sebelum Anda memutuskan.
- ✅ **Daftar keputusan untuk pemilik** dan **pola** (tiga keluhan sebab sama berarti ada akar masalah), supaya masalah yang sama tidak terulang.
- ✅ **Aman:** rekap untuk grup tanpa nama, nomor HP, atau alamat pelanggan; tidak membantu menghapus ulasan atau menyamar jadi pembeli; fakta toko tidak dikarang.

## Cocok untuk siapa
- Pemilik toko online di Shopee, Tokopedia, TikTok Shop, WhatsApp, atau Instagram yang punya admin sedikit.
- Pemilik kafe/restoran yang mengurus ulasan Google, GoFood, GrabFood.
- Jasa (servis AC, salon, bengkel, klinik non-medis) yang menerima komplain lewat WA.
- Pemilik yang ingin tahu keluhan mana yang harus ia pegang sendiri.
- **Bukan untuk:** membalas satu chat biasa (pakai `balas-chat-cs`), menulis balasan ulasan satu per satu dengan nada brand (`balas-ulasan-pelanggan`), atau nasihat hukum.

## Contoh sebelum & sesudah
**Sebelum:** 8 keluhan masuk dari 5 aplikasi. Admin membalas dari yang paling atas, sehingga pembeli yang mengancam lapor ke Shopee baru dibalas siang, dan pembeli COD bernilai Rp875.000 tertunda sampai besok.

**Sesudah (cukup tempel keluhannya):** daftar kerja berurutan: COD Rp875.000 dan ancaman lapor dikerjakan pertama, pertanyaan stok paling akhir; draf balasan untuk semuanya; 3 hal yang perlu keputusan pemilik. Contoh lengkap: `examples/01-toko-fashion-8-keluhan-campur.md`.

## Cara pakai
Setelah terpasang, tempel keluhan dan ceritakan singkat usahanya, misalnya:
- "Ini 8 keluhan hari ini dari Shopee dan WA. Mana yang duluan dibalas? Siapkan balasannya."
- "Ada 5 ulasan bintang 1-2 baru di kafe saya. Tolong pilah dan buatkan balasannya."
- "Banyak yang minta refund minggu ini, tolong urutkan."

Tidak perlu lengkap. Info yang kurang ditandai `[isian: ...]`, lalu ditanyakan maksimal tiga hal di akhir. Anda yang membaca dan mengirim balasannya satu per satu; skill ini tidak mengirim apa pun sendiri.

## Instalasi singkat
Salin folder `triase-keluhan-pelanggan` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` yang disertakan dalam paket. Python tidak wajib; hanya dipakai bila Anda menyerahkan berkas CSV berisi banyak keluhan.

## FAQ
**Apakah skill ini yang membalas pelanggan?**
Tidak. Skill ini menyiapkan urutan kerja dan draf. Anda yang mengirim, satu per satu, lewat aplikasi tempat keluhan masuk.

**Bisakah membantu menghapus ulasan buruk atau meminta pelanggan mengganti bintang?**
Tidak. Yang bisa: menyelesaikan masalahnya, membalas ulasan secara sopan, dan melaporkan ulasan yang benar-benar melanggar aturan platform lewat fitur laporan platform.

**Apakah tenggat retur/refund Shopee, Tokopedia, dan TikTok Shop sudah pasti?**
Tidak pasti: platform sering mengubahnya. Skill ini memakai ketentuan umum yang dicek per 2026-10-05 dan selalu mengingatkan Anda mencocokkan dengan Pusat Penjual sebelum menjanjikan sesuatu ke pelanggan.

## Catatan versi
- **1.0.1 (2026-10-05):** permintaan seperti "hapus ulasan", "balas pakai akun lain", atau "minta nomor pembeli" kini memicu skill: ditolak singkat dengan alasan, lalu tetap disiapkan draf balasan resmi dan langkah melaporkan ulasan. Setiap keluhan P1/P2 marketplace kini memuat baris "Batas waktu" (Shopee dan TikTok Shop, terkonfirmasi di halaman resmi, dicek 2026-10-05). Draf balasan tidak lagi berisi kalimat membela diri, permintaan menunda lapor, atau klaim perbaikan yang belum terjadi.
- **1.0.0 (2026-10-05):** rilis awal.

## Catatan
Bukan nasihat hukum. Ringkasan aturan di `references/dasar-hukum-dan-platform.md` membantu menulis dengan aman, bukan pengganti konsultasi hukum.

Skill ini adaptasi (dengan perubahan besar dan penambahan lokal) dari skill `ticket-triage` dan `customer-escalation` di `anthropics/knowledge-work-plugins` (Apache-2.0). Tidak berafiliasi dengan Anthropic, Shopee, Tokopedia, TikTok, Google, atau GoFood; nama dipakai sekadar menyebut produk. Lihat `ATTRIBUTION.md`, `NOTICE`, dan `LICENSE-APACHE`.
