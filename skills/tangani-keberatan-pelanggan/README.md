# Jawab "Mahal" dan "Mikir Dulu" Tanpa Memaksa

**Pelanggan ragu atau menolak di chat? Dapatkan 2-3 balasan sopan siap kirim, satu pertanyaan lanjutan, dan patokan kapan berhenti, tanpa urgensi palsu dan tanpa bohong.**

Diuji AI penguji independen di bot Telegram asli: 6,5 → 8,5 dari 10 (tanpa skill satu draf defensif yang menyiratkan barang pesaing "gampang melar/tipis" tanpa dasar; dengan skill perbandingan jujur dan 3 pilihan balasan).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Langsung dapat **2-3 balasan WA siap kirim**, pendek dan sopan, beda arah (ringan, menggali, menawarkan opsi). Tinggal salin.
- ✅ Keberatan **dikenali jenisnya**: harga, waktu, kepercayaan, kebutuhan, "tanya suami/istri/bos dulu", atau pesaing, jadi jawabannya tepat sasaran, bukan satu kalimat untuk semua.
- ✅ Alur tiga langkah yang sederhana: **akui perasaannya, tanya alasan sebenarnya, tawarkan opsi**, supaya pelanggan tidak merasa didesak.
- ✅ **Jujur dan hati-hati**: skill dirancang tidak mengarang stok/diskon/testimoni dan tidak menjelekkan pesaing. Data produk yang belum Anda berikan ditandai `[isian: ...]`, bukan dikarang.
- ✅ Ada **pertanyaan lanjutan** dan aturan **kapan berhenti menghubungi ulang (follow-up)**, supaya Anda tidak mengejar pelanggan terlalu lama.
- ✅ Angka dihitung, bukan dikira: harga per hari/pemakaian, perbandingan dengan pesaing (termasuk ongkir), cicilan bila Anda menyediakannya. Bila harga Anda memang lebih mahal, skill ini jujur mengatakannya dan membantu menjawab dengan nilai lain.

## Cocok untuk siapa
- Penjual online (WhatsApp, pesan langsung/DM Instagram, Shopee, Tokopedia, TikTok Shop) yang sering dibilang "mahal, di sebelah lebih murah".
- Konsultan, freelancer, dan pemilik jasa yang dijawab "pikir-pikir dulu" lalu diam.
- Pemasok/B2B (jualan ke perusahaan lain) yang menghadapi "sudah ada supplier tetap".
- Pemilik usaha yang jujur dan tidak mau memakai taktik menekan.
- **Bukan untuk:** pesan pertama ke kontak baru (pakai skill Pesan Prospek WA), urutan pesan susulan terjadwal (skill Follow-up Prospek), atau komplain pembeli yang sudah membeli (skill Balas Chat CS).

## Contoh sebelum & sesudah
**Sebelum:** Pelanggan: "Wah mahal ya kak, di toko sebelah 85 ribu". Penjual langsung membalas "Ini kualitasnya beda kak, harga segini sudah murah, stok tinggal sedikit lho!" Pelanggan merasa ditekan dan menghilang.

**Sesudah (cukup ketik):** "Calon pembeli bilang 'mahal, di toko sebelah 85 ribu'. Tas saya Rp129.000, kulit sintetis tebal, jahitan double."

Cuplikan dari contoh (kasus fiktif, dipotong; `examples/01-toko-online-tas-mahal.md`):

```
Balasan 1 - ringan
> Betul Kak, selisihnya terasa ya. Silakan dibandingkan dulu, nggak apa-apa 🙏 Kalau mau, saya bantu cek apakah yang itu setara.

Balasan 2 - menggali
> Wajar kalau dipikirkan, Kak. Boleh tahu tas yang 85 ribu itu bahannya apa dan jahitannya seperti apa? Supaya saya bisa bandingkan yang setara, bukan cuma harga.

Balasan 3 - opsi
> Kak, tas ini kulit sintetis tebal dengan jahitan double. Kalau dipakai setahun, hitungannya sekitar Rp353 per hari. Mau saya kirim foto jahitan dan bagian dalam tasnya supaya Kakak bisa lihat sendiri? Kalau ternyata belum cocok juga tidak apa-apa.

Pertanyaan lanjutan (kalau dia membalas): "Biasanya tas dipakai untuk kerja atau jalan-jalan, Kak? Supaya saya sarankan yang paling pas."

Kapan berhenti: kalau dia menjawab "oke, saya beli di sebelah", ucapkan terima kasih dan selesai. Kalau diam, boleh satu pesan lagi 2-3 hari kemudian ...
```

## Cara pakai
Setelah terpasang, tempel kalimat pelanggan dan ceritakan singkat produknya, misalnya:
- "Pelanggan bilang 'kemahalan kak'. Aku jual [produk] Rp[harga]."
- "Klien jawab 'saya pikir-pikir dulu'. Gimana balasnya?"
- "Calon pembeli mau tapi tanya suami dulu."
- "Dia bilang takut tipu-tipu, apa jawabnya?"

Tidak perlu lengkap. AI langsung memberi balasan dengan `[isian]` untuk data yang belum ada, lalu menanyakan maksimal tiga hal di akhir. Anda yang mengirim balasan ke pelanggan; skill ini tidak mengirim apa pun sendiri.

## Instalasi singkat
Salin folder `tangani-keberatan-pelanggan` ke folder skills AI agent Anda:

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
Tidak. Skill ini menyiapkan balasan; Anda yang membaca dan mengirimnya satu per satu. Untuk promo ke banyak orang, pakai skill Broadcast WA dengan persetujuan penerima.

**Bagaimana kalau pelanggan terus menolak?**
Setiap jawaban menyertakan aturan kapan berhenti (mis. menolak dua kali atau tidak membalas setelah dua pesan). Hormati itu; pelanggan yang dihormati lebih mungkin kembali.

## Catatan
Bukan nasihat hukum. Ringkasan aturan di `references/etika-keberatan.md` membantu menulis dengan lebih hati-hati, bukan pengganti konsultasi hukum.

Skill ini adaptasi (dengan perubahan besar dan penambahan lokal) dari skill `handle-objection` di `anthropics/knowledge-work-plugins` (Apache-2.0). Lihat `ATTRIBUTION.md`, `NOTICE`, dan `LICENSE-APACHE`.
