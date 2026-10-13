# Jawab "Mahal" dan "Mikir Dulu" Tanpa Memaksa

**Pelanggan ragu atau menolak di chat? Dapatkan 2-3 balasan sopan siap kirim, satu pertanyaan lanjutan, dan kepastian kapan berhenti, tanpa urgensi palsu dan tanpa bohong.**

## Manfaat
- ✅ Langsung dapat **2-3 balasan WA siap kirim**, pendek dan sopan, beda arah (ringan, menggali, menawarkan opsi). Tinggal salin.
- ✅ Keberatan **dikenali jenisnya**: harga, waktu, kepercayaan, kebutuhan, "tanya suami/istri/bos dulu", atau pesaing, jadi jawabannya tepat sasaran, bukan satu kalimat untuk semua.
- ✅ Alur tiga langkah yang terbukti: **akui perasaannya, tanya alasan sebenarnya, tawarkan opsi**. Pelanggan tidak merasa didesak.
- ✅ **Jujur dan aman**: tidak ada stok/diskon/testimoni karangan, tidak menjelekkan pesaing. Data produk yang belum Anda berikan ditandai `[isian: ...]`, bukan dikarang.
- ✅ Ada **pertanyaan lanjutan** dan aturan **kapan berhenti follow-up**, jadi Anda tidak mengejar pelanggan terlalu lama.
- ✅ Angka dihitung, bukan dikira: harga per hari/pemakaian, perbandingan dengan pesaing (termasuk ongkir), cicilan bila Anda menyediakannya. Bila harga Anda memang lebih mahal, skill ini jujur mengatakannya dan membantu menjawab dengan nilai lain.

## Cocok untuk siapa
- Penjual online (WhatsApp, DM Instagram, Shopee, Tokopedia, TikTok Shop) yang sering dibilang "mahal, di sebelah lebih murah".
- Konsultan, freelancer, dan pemilik jasa yang dijawab "pikir-pikir dulu" lalu diam.
- Supplier/B2B yang menghadapi "sudah ada supplier tetap".
- Pemilik usaha yang jujur dan tidak mau memakai taktik menekan.
- **Bukan untuk:** pesan pertama ke kontak baru (`pesan-prospek-wa`), urutan follow-up terjadwal (`follow-up-prospek`), atau komplain pembeli yang sudah membeli (`balas-chat-cs`).

## Contoh sebelum & sesudah
**Sebelum:** Pelanggan: "Wah mahal ya kak, di toko sebelah 85 ribu". Penjual langsung membalas "Ini kualitasnya beda kak, harga segini sudah murah, stok tinggal sedikit lho!" Pelanggan merasa ditekan dan menghilang.

**Sesudah (cukup ketik):** "Calon pembeli bilang 'mahal, di toko sebelah 85 ribu'. Tas saya Rp129.000, kulit sintetis tebal, jahitan double."
→ Balasan seperti: "Betul Kak, selisihnya terasa ya. Boleh tahu tas yang 85 ribu itu bahannya apa dan jahitannya seperti apa? Supaya saya bisa bandingkan yang setara, bukan cuma harga." Plus pilihan balasan lain, satu pertanyaan lanjutan, dan kapan berhenti. Contoh lengkap: `examples/01-toko-online-tas-mahal.md`.

## Cara pakai
Setelah terpasang, tempel kalimat pelanggan dan ceritakan singkat produknya, misalnya:
- "Pelanggan bilang 'kemahalan kak'. Aku jual [produk] Rp[harga]."
- "Klien jawab 'saya pikir-pikir dulu'. Gimana balasnya?"
- "Calon pembeli mau tapi tanya suami dulu."
- "Dia bilang takut tipu-tipu, apa jawabnya?"

Tidak perlu lengkap. AI langsung memberi balasan dengan `[isian]` untuk data yang belum ada, lalu menanyakan maksimal tiga hal di akhir. Anda yang mengirim balasan ke pelanggan; skill ini tidak mengirim apa pun sendiri.

## Instalasi singkat
Salin folder `tangani-keberatan-pelanggan` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` yang disertakan dalam paket.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 11, 2026-10-06.
- Tanpa skill: https://t.me/c/4407409583/906/946 — skor 6,5
- Dengan skill: https://t.me/c/4407409583/907/948 — skor 8,5
Verdik gelombang: LULUS — Tanpa skill satu draf defensif yang menyiratkan barang pesaing "gampang melar/tipis" (tanpa dasar); dengan skill perbandingan jujur (pesaing tetap ±Rp15 rb lebih murah), 3 pilihan balasan termasuk opsi tanpa memaksa, kapan berhenti, dan ongkir pesaing ditandai perkiraan.

- Pilot 26 (kirim ulang 4 pesan di topik baru, 2026-10-12, dijalankan Akun C): skor 6,5 → 8,5, verdik LULUS — hasil sama dengan gelombang 11 dan 11b (`koordinasi/telegram-gelombang-11b-pilot-2026-10-12.md`; tautan pesan tidak tercatat di log).

## FAQ
**Apakah skill ini bisa membuat pelanggan "takut kehabisan" supaya cepat beli?**
Tidak. Stok, hitung mundur, diskon, atau testimoni yang tidak nyata berisiko melanggar UU Perlindungan Konsumen dan merusak kepercayaan. Skill ini menawarkan alternatif jujur: info stok/promo yang benar-benar nyata, atau ajakan tanpa tekanan.

**Apakah skill ini yang mengirim pesan ke pelanggan?**
Tidak. Skill ini menyiapkan balasan; Anda yang membaca dan mengirimnya satu per satu. Untuk promo ke banyak orang, pakai `broadcast-wa` dengan persetujuan penerima.

**Bagaimana kalau pelanggan terus menolak?**
Setiap jawaban menyertakan aturan kapan berhenti (mis. menolak dua kali atau tidak membalas setelah dua pesan). Hormati itu; pelanggan yang dihormati lebih mungkin kembali.

## Catatan
Bukan nasihat hukum. Ringkasan aturan di `references/etika-keberatan.md` membantu menulis dengan aman, bukan pengganti konsultasi hukum.

Skill ini adaptasi (dengan perubahan besar dan penambahan lokal) dari skill `handle-objection` di `anthropics/knowledge-work-plugins` (Apache-2.0). Lihat `ATTRIBUTION.md`, `NOTICE`, dan `LICENSE-APACHE`.
