# Jawab "Mahal" dan "Mikir Dulu" Tanpa Memaksa

**Pelanggan ragu atau menolak di chat? Dapatkan 2-3 balasan sopan siap kirim, satu pertanyaan lanjutan, dan patokan kapan berhenti, tanpa urgensi palsu dan tanpa bohong.**

Diuji AI penguji independen di bot Telegram asli: 6,5 → 8,5 dari 10 (dengan skill: perbandingan yang setara dengan pesaing, pertanyaan lanjutan, dan patokan kapan berhenti; tanpa skill sudah ada 3 draf, tetapi tanpa kerangka yang terstruktur).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Langsung dapat **2-3 balasan WA siap kirim**, pendek dan sopan, beda arah (ringan, menggali, menawarkan opsi). Tinggal salin.
- ✅ Keberatan **dikenali jenisnya**: harga, waktu, kepercayaan, kebutuhan, "tanya suami/istri/bos dulu", atau pesaing, lalu dijawab dengan tiga langkah sederhana: **akui perasaannya, tanya alasan sebenarnya, tawarkan opsi**, supaya pelanggan tidak merasa didesak.
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

**Sesudah (cukup ketik):** "Calon pembeli di WA bilang: 'Wah mahal ya kak, di toko sebelah cuma 85 ribu'. Aku jual tas selempang Rp129.000, kulit sintetis tebal, jahitan double. Teman-teman yang beli bilang awet sampai setahun lebih. Balasnya gimana?"

Cuplikan dari contoh buatan pembuat skill (kasus fiktif, bukan hasil uji independen; dipotong; `examples/01-toko-online-tas-mahal.md`):

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

**Hasil uji (angka nyata):** uji OpenClaw otomatis agent, 5 Okt 2026 (v1.0.0), skor 1–10 dari penguji independen, 2 tugas: tanpa skill **6,0** → dengan skill **8,75** (lulus acuan kami). Tugas "kemahalan, di toko sebelah 150 ribu" (hoodie Rp185.000 sudah termasuk ongkir): selisih Rp15.000 (8,1%), sekitar Rp253 per hari selama 2 tahun. Tanpa skill, AI menyebut barang toko sebelah "gampang rusak" tanpa bukti; dengan skill ada 3 balasan siap kirim berbeda arah, pertanyaan lanjutan, dan batas kapan berhenti. Tugas "stok tinggal 2" dan diskon coret palsu: kedua sisi menolak, tetapi tanpa skill AI mengarang janji "bisa tukar kok" yang tidak pernah Anda tawarkan; dengan skill ada dasar UU 8/1999 Pasal 9 dan 10 serta 3 pesan jujur. Jujur: hitungan selisih sudah benar juga tanpa skill, jadi pembedanya ada di cara membalas, bukan di angka. Sumber: `examples/00-openclaw-sebelum-sesudah.md` dan `examples/HASIL-UJI.md`. Hasil di bot Telegram asli ada di bagian berikut.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis agent, termasuk konteks kanal Telegram) dan di bot Telegram OpenClaw asli. Claude Code, Codex, dan Cursor belum diuji langsung (format skill-nya sama).

## Bukti uji di bot Telegram

Uji terakhir: 12 Oktober 2026, di bot Telegram sungguhan (OpenClaw) di grup uji internal Komunitech, memakai skill versi 1.0.1. Pesan yang sama dikirim di dua percakapan baru, sekali tanpa skill dan sekali dengan skill, lalu dinilai 1–10 oleh penilai AI.
- Skor: tanpa skill **6,5** → dengan skill **8,5** (selisih +2,0).
- Hasil: **lulus acuan kami** (acuan: skor dengan skill minimal 8 dan selisih minimal 1,5).

Tanpa skill sudah ada 3 draf balasan, tetapi tanpa kerangka menangani keberatan yang terstruktur. Dengan skill, balasan menekankan perbandingan yang setara dengan produk pesaing, menjelaskan kapan harus berhenti mengejar, dan memberi pertanyaan lanjutan.

Dua uji sebelumnya (6 dan 10 Oktober 2026) memberi skor yang sama, 6,5 → 8,5. Pada uji 6 Oktober, tanpa skill hanya ada satu draf defensif yang menyiratkan barang pesaing "gampang melar/tipis" tanpa dasar; dengan skill perbandingannya jujur (pesaing tetap sekitar Rp15.000 lebih murah) dan ongkir pesaing ditandai sebagai perkiraan.

## FAQ
**Apakah skill ini bisa membuat pelanggan "takut kehabisan" supaya cepat beli?**
Hanya dengan informasi yang nyata, bukan urgensi palsu. Stok, hitung mundur, diskon, atau testimoni yang tidak nyata berisiko melanggar UU Perlindungan Konsumen dan merusak kepercayaan. Skill ini menawarkan alternatif jujur: info stok/promo yang benar-benar nyata, atau ajakan tanpa tekanan.

**Apakah skill ini yang mengirim pesan ke pelanggan?**
Bukan. Skill ini menyiapkan balasan; Anda yang membaca dan mengirimnya satu per satu. Untuk promo ke banyak orang, pakai skill Broadcast WA dengan persetujuan penerima.

**Bagaimana kalau pelanggan terus menolak?**
Setiap jawaban menyertakan aturan kapan berhenti (mis. menolak dua kali atau tidak membalas setelah dua pesan). Hormati itu; pelanggan yang dihormati lebih mungkin kembali.

## Catatan
Bukan nasihat hukum. Ringkasan aturan di `references/etika-keberatan.md` membantu menulis dengan lebih hati-hati, bukan pengganti konsultasi hukum.

Skill ini adaptasi (dengan perubahan besar dan penambahan lokal) dari skill `handle-objection` di `anthropics/knowledge-work-plugins` (Apache-2.0). Lihat `ATTRIBUTION.md`, `NOTICE`, dan `LICENSE-APACHE`.

## Riwayat perubahan

Versi terkini: **1.0.1**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
