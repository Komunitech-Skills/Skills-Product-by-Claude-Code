# Tes Ide Sebelum Modal Habis

**Tahu ide jualan laku atau enggak dalam 7 hari — tanpa produksi massal, tanpa modal besar.**

*Diuji AI penguji independen di OpenClaw: 7,5 → 8,25 dari 10. Selisihnya kecil: untuk membaca hasil tes, AI tanpa skill pun sudah menghitung dengan benar; pembedanya ada pada rancangan tes siap pakai (kriteria lulus berangka yang ditetapkan di awal dan teks WA/IG siap kirim).*

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Ubah ide satu kalimat jadi rencana uji yang jelas: siapa yang ditawari, apa yang diukur, kapan berhenti.
- ✅ Pakai jalur yang sudah Anda punya (kontak WA, follower IG, pelanggan tetap, warung langganan) — tidak perlu budget iklan.
- ✅ Keputusan LANJUT/UBAH/HENTIKAN berdasarkan angka hasil uji Anda, bukan feeling atau "kayaknya laku".
- ✅ Template pesan siap kirim (pesan WA ke kontak pilihan Anda, story IG, pre-order di marketplace, titip warung) — tinggal isi, dikirim oleh Anda sendiri.
- ✅ Skrip hitung otomatis: konversi (berapa persen yang benar-benar membeli), margin, dan apakah biaya uji sudah balik modal — hanya dari pesanan yang sudah bayar atau uang muka (DP); vote/like dilaporkan terpisah sebagai minat, supaya risiko klaim "balik modal" yang keliru lebih kecil.

## Cocok untuk siapa
- Pemilik UMKM yang mau coba produk/menu/jasa baru tapi ragu invest modal besar dari awal.
- Pemilik usaha yang sudah berjalan dan mau tahu apakah ide produk tambahan atau sampingan layak dikembangkan.
- Siapa pun yang sudah punya SATU ide konkret (bukan lagi tahap "bingung mau jualan apa").

## Contoh sebelum & sesudah
**Sebelum:** "Saya mau jual kopi susu gula aren literan, tapi ragu, takut rugi kalau ternyata gak ada yang beli."

**Sesudah (cukup ketik):** "Saya mau coba jual kopi susu gula aren kemasan literan, punya 150 kontak WA, rencana harga Rp45.000."
→ Dapat rumusan dugaan yang diuji (hipotesis) lengkap, pesan pre-order siap kirim, dan kriteria lulus (≥15% konversi dari 60 kontak yang ditawari). Setelah 7 hari, Anda kirim angkanya (60 ditawari, 11 pre-order), dan skrip menghitung:

```
=== HASIL VALIDASI IDE ===
Ditawari       : 60 orang/tampilan
Pre-order/beli : 11
Konversi       : 18.3%
Ambang         : LULUS >= 15% | LULUS BERSYARAT >= 8% | GAGAL < 8%
Klasifikasi    : LULUS
...
=== MARGIN & BIAYA UJI ===
Margin per unit      : Rp23.000  (Rp45.000 - Rp22.000)
Total margin preorder: Rp253.000  (23000 x 11 unit)
Biaya uji            : Rp30.000
Selisih              : Rp223.000  (SUDAH balik modal uji)
```
(Contoh dengan data fiktif dari `examples/01-kopi-susu-literan.md`, dipotong.) Keputusannya: LANJUT ke produksi rutin.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Saya mau coba jual [ide produk], gimana cara tes minatnya dulu sebelum produksi banyak?"
- "Saya sudah tes ide saya, dari 30 orang yang ditawari ada 5 yang pre-order, ini worth dilanjutin gak?"

## Instalasi singkat
Salin folder `validasi-ide-produk-baru` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` yang disertakan dalam paket.

**Hasil uji (angka nyata):** uji OpenClaw otomatis agent, Okt 2026 (diuji pada v1.0.4; v1.0.5 hanya merapikan rujukan antar-skill, logika dan skrip tidak berubah), skor 1–10: tanpa skill **7,5** → dengan skill **8,25** (LULUS). Contoh keripik tempe: konversi bayar **4/45 = 8,9%** dipisah dari 52 vote IG (minat, bukan pesanan); selisih tes **−Rp26.000** → keputusan UBAH, bukan produksi 200 bungkus. Catatan jujur: pada skenario hasil campuran ini AI tanpa skill pun menghitung benar (8 vs 8,5); nilai tambah utama ada di skenario rancangan tes (7 → 8). Sumber skor: `examples/00-openclaw-sebelum-sesudah.md`. Contoh kopi susu di atas adalah hasil skrip pada data fiktif, bukan dari uji OpenClaw.

**Status uji (jujur):** sudah diuji OpenClaw (sebelum/sesudah otomatis 2026-10-01; muat CLI) dan Claude Code (simulasi agent; skor 9/10 di `examples/HASIL-UJI.md` berasal dari simulasi ini, bukan dari uji OpenClaw). Codex dan Cursor belum uji platform asli. Skill kurasi Apache-2.0 (product-on-purpose/pm-skills) — lihat `ATTRIBUTION.md`. Ambang 15%/8% heuristik praktis, bukan rumus ilmiah baku.

## FAQ
**Apakah saya butuh install Python atau aplikasi lain?**
Tidak wajib. Skill ini tetap berguna hanya lewat percakapan dengan AI agent Anda. Skrip Python (`scripts/hitung_validasi.py`) bersifat pelengkap untuk hitung otomatis lebih presisi — kalau tidak bisa dijalankan, agent tetap bisa hitung manual dengan rumus di `SKILL.md`.

**Ambang 15%/8% itu dari mana, apa pasti akurat?**
Itu patokan praktis yang kami tetapkan sendiri (heuristik), bukan rumus ilmiah baku. Boleh disesuaikan sesuai jenis produk (harga rendah/impulsif vs harga tinggi/pertimbangan lama) — skill akan menjelaskan kapan dan kenapa perlu disesuaikan. Dalam uji, AI kadang memilih ambang yang berbeda untuk produk yang sama; karena itu tetapkan ambangnya di awal, sebelum melihat hasil.

**Kalau hasilnya GAGAL, apa artinya usaha saya gagal total?**
Tidak. GAGAL artinya ide dalam bentuk sekarang (harga, penawaran, target pembeli) belum menunjukkan minat cukup kuat — bukan vonis bahwa usaha Anda gagal. Skill akan membantu Anda melihat alasan penolakan dan menyarankan revisi (harga, penawaran, atau calon pembeli) atau ide lain.

## Riwayat perubahan

Versi terkini: **1.0.7**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
