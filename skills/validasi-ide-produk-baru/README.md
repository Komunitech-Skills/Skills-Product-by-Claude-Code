# Tes Ide Sebelum Modal Habis

**Tahu ide jualan laku atau enggak dalam 7 hari — tanpa produksi massal, tanpa modal besar.**

## Manfaat
- ✅ Ubah ide satu kalimat jadi rencana uji yang jelas: siapa yang ditawari, apa yang diukur, kapan berhenti.
- ✅ Pakai kanal yang sudah kamu punya (kontak WA, follower IG, pelanggan tetap, warung langganan) — tidak perlu budget iklan.
- ✅ Keputusan LANJUT/UBAH/HENTIKAN dari angka pasti, bukan feeling atau "kayaknya laku".
- ✅ Template pesan siap kirim (broadcast WA, story IG, listing PO marketplace, titip warung) — tinggal isi.
- ✅ Skrip hitung otomatis: konversi, margin, dan apakah biaya uji sudah balik modal.

## Cocok untuk siapa
- Pemilik UMKM yang mau coba produk/menu/jasa baru tapi ragu invest modal besar dari awal.
- Pemilik usaha yang sudah berjalan dan mau tahu apakah ide diversifikasi/produk sampingan layak dikembangkan.
- Siapa pun yang sudah punya SATU ide konkret (bukan lagi tahap "bingung mau jualan apa" — untuk itu ada `brainstorming-ide-usaha`).

## Contoh sebelum & sesudah
**Sebelum:** "Saya mau jual kopi susu gula aren literan, tapi ragu, takut rugi kalau ternyata gak ada yang beli."

**Sesudah (cukup ketik):** "Saya mau coba jual kopi susu gula aren kemasan literan, punya 150 kontak WA, rencana harga Rp45.000."
→ Dapat hipotesis lengkap, pesan pre-order siap kirim, kriteria lulus (≥15% konversi dari 60 kontak yang ditawari), dan setelah 7 hari: hasil "LULUS, konversi 18,3%, margin Rp253.000, sudah balik modal uji Rp30.000 — LANJUT ke produksi rutin."

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Saya mau coba jual [ide produk], gimana cara tes minatnya dulu sebelum produksi banyak?"
- "Saya sudah tes ide saya, dari 30 orang yang ditawari ada 5 yang pre-order, ini worth dilanjutin gak?"

## Instalasi singkat
Salin folder `validasi-ide-produk-baru` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket pembelian.

## FAQ
**Apakah saya butuh install Python atau aplikasi lain?**
Tidak wajib. Skill ini tetap berguna hanya lewat percakapan dengan AI agent kamu. Skrip Python (`scripts/hitung_validasi.py`) bersifat pelengkap untuk hitung otomatis lebih presisi — kalau tidak bisa dijalankan, agent tetap bisa hitung manual dengan rumus di `SKILL.md`.

**Ambang 15%/8% itu dari mana, apa pasti akurat?**
Itu heuristik praktis Komunitech berdasarkan pengalaman uji pasar UMKM skala kecil-menengah, bukan rumus ilmiah baku. Boleh disesuaikan sesuai jenis produk (harga rendah/impulsif vs harga tinggi/pertimbangan lama) — skill akan menjelaskan kapan dan kenapa perlu disesuaikan.

**Kalau hasilnya GAGAL, apa artinya usaha saya gagal total?**
Tidak. GAGAL artinya ide dalam bentuk sekarang (harga, penawaran, target pembeli) belum menunjukkan minat cukup kuat — bukan vonis usaha kamu gagal. Skill akan membantu kamu lihat alasan penolakan dan menyarankan revisi atau ide lain lewat `brainstorming-ide-usaha`.
