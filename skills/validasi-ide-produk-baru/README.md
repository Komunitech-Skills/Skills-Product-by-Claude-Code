# Tes Ide Sebelum Modal Habis

**Tahu ide jualan laku atau enggak dalam 7 hari — tanpa produksi massal, tanpa modal besar.**

## Manfaat
- ✅ Ubah ide satu kalimat jadi rencana uji yang jelas: siapa yang ditawari, apa yang diukur, kapan berhenti.
- ✅ Pakai kanal yang sudah kamu punya (kontak WA, follower IG, pelanggan tetap, warung langganan) — tidak perlu budget iklan.
- ✅ Keputusan LANJUT/UBAH/HENTIKAN dari angka pasti, bukan feeling atau "kayaknya laku".
- ✅ Template pesan siap kirim (broadcast WA, story IG, listing PO marketplace, titip warung) — tinggal isi.
- ✅ Skrip hitung otomatis: konversi, margin, dan apakah biaya uji sudah balik modal — hanya dari pesanan yang sudah bayar/DP; vote/like dilaporkan terpisah sebagai minat, jadi tidak ada klaim "balik modal" palsu.

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

## Catatan revisi 1.0.4 (2026-10-01)
Hasil uji sebelum/sesudah di OpenClaw (`examples/00-openclaw-sebelum-sesudah.md`) menemukan salah hitung: 52 vote polling IG dijumlahkan dengan 4 PO berbayar sehingga muncul klaim "balik modal +Rp416.000" (yang benar −Rp26.000). Perbaikan:
- **Aturan hitung baru di SKILL.md:** hanya pesanan berkomitmen (PO sudah transfer/DP/bayar, checkout, laku terjual) yang masuk konversi, pendapatan, margin, dan balik modal. Vote/like/komentar/"mau" = **minat**, dilaporkan terpisah dan tidak pernah dijumlahkan dengan pesanan. Instruksi lama "gabungkan metode jadi satu total" dihapus.
- `scripts/hitung_validasi.py`: argumen `--minat`, mode JSON `kanal` (pesanan & minat per kanal dipisah otomatis), status "BELUM BISA DINILAI" bila hanya ada minat, rumus ditampilkan di setiap baris uang, format rugi `-Rp26.000`.
- Untung/rugi wajib lewat script atau rumus eksplisit yang ditampilkan; satu set ambang ditetapkan di awal sesuai harga.
- `references/menu-uji-murah.md` dan `templates/form-pencatatan.md` memisahkan kolom pesanan vs minat.
- `tests/uji_regresi.py`: +17 cek regresi (kasus keripik: 4 pesanan, −Rp26.000, tidak boleh muncul 56/416).

## Riwayat versi

- **1.0.1** (2026-09-26) — Revisi hasil uji independen Tahap 6 (skor 7,5/10, lihat `examples/HASIL-UJI.md`):
  - **Bug diperbaiki:** `scripts/hitung_validasi.py` salah membaca harga format Indonesia bertitik ribuan (mis. `25.000` terbaca `25`, salah 1000x diam-diam). Fungsi `parse_uang` baru kini mendukung `Rp25.000`, `150.000`, `1.234.567`, singkatan `25rb`/`1jt`/`1,5jt`, dan **menolak** pola ambigu (`25.5`, `1.234,56`, `25,000` tanpa singkatan) dengan pesan jelas alih-alih menebak. Tes regresi baru: `tests/uji_regresi.py` (23 kasus, 14 diterima + 9 ditolak).
  - `templates/pesan-uji-murah.md`: template #1 (broadcast WA pre-order) dan #4 (listing PO marketplace) kini menyebutkan eksplisit kebijakan batal/refund (uang kembali 100% bila batch tidak jadi diproduksi atau pembeli batal sebelum masa produksi, dengan batas waktu pengembalian) — sebelumnya tidak disebut sama sekali.
  - `ATTRIBUTION.md`: commit hash sumber diverifikasi ulang (`1cef1a9eae10017389863d51e289e0ae41e17fcb`, 40 karakter SHA-1, sesuai `git rev-parse HEAD` repo sumber).
- **1.0.0** (2026-09-26) — Rilis awal (status `draft`, hasil ATM dari `product-on-purpose/pm-skills`, Apache-2.0).
