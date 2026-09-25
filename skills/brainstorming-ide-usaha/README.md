# Sesi Brainstorming Ide Usaha yang Beneran Bisa Dieksekusi

**Ceritakan kebuntuanmu — ide produk baru, promo, nama usaha, diversifikasi, atau masalah operasional — dapat beberapa ide tersaring dengan skor terhitung, rencana uji murah, dan langkah aksi 7 hari, bukan sekadar daftar ide acak.**

## Manfaat
- ✅ Menggali tujuan & batasan nyata (modal, waktu, SDM, lokasi, musim) dulu sebelum melempar ide — supaya ide yang keluar memang bisa kamu kerjakan, bukan wacana
- ✅ Teknik ide terstruktur (SCAMPER, gabung-kombinasi, pembalikan masalah) dijelaskan bahasa sehari-hari dengan contoh usahamu sendiri
- ✅ Ide disaring pakai **skor tertimbang yang dihitung script**, bukan feeling — kamu tentukan kriteria & bobotnya, hasilnya angka + peringkat
- ✅ Setiap ide terpilih dilengkapi rencana uji murah (pre-order WA, tes 1 minggu, target jelas) plus titik impas kasar bila perlu modal awal
- ✅ Ditutup dengan **Rencana Aksi 7 Hari** — tabel harian siap dikerjakan, bukan cuma ide di kepala
- ✅ Ada jalur cepat kalau kamu cuma butuh beberapa opsi nama/judul tanpa proses panjang

## Cocok untuk siapa
- Pemilik UMKM yang usahanya sepi/stagnan dan butuh ide tambahan produk, promo, atau perbaikan operasional
- Yang mau mulai usaha sampingan tapi bingung mau jualan apa
- Pemilik usaha yang mau diversifikasi/buka lini baru dan butuh cara menyaring beberapa opsi secara adil
- Siapa pun yang butuh ide nama usaha/produk dengan beberapa pendekatan sekaligus
- **Bukan untuk:** kalau idemu sudah satu dan tinggal dieksekusi — pakai skill spesifiknya (`promo-kalender` untuk promo, `hitung-hpp` untuk modal produk, `riset-calon-pelanggan` untuk cari pelanggan, `proposal-kerjasama` untuk kemitraan)

## Contoh sebelum & sesudah
**Sebelum:** "Usaha laundry saya sepi, ada ide tambahan nggak?" → dijawab asal seperti "coba buka cabang baru" atau "kasih diskon aja" — tanpa mempertimbangkan modal, waktu, atau kenapa omzet turun.

**Sesudah (cukup ketik permintaan yang sama):** skill menggali dulu modal/waktu/SDM yang tersedia, memunculkan 5 ide pakai SCAMPER, menyaringnya dengan skor tertimbang terhitung (skor 4,28 untuk ide terbaik vs 2,78 untuk yang terlemah), lalu menutup dengan rencana uji 1 minggu (target 10 pendaftar) dan tabel Rencana Aksi 7 Hari. Lihat contoh penuh di `examples/uji-pembuat-01-diversifikasi-laundry.md`.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Usaha saya sepi, ada ide tambahan produk/jasa?"
- "Butuh ide nama untuk toko roti baru saya."
- "Mau diversifikasi dari jualan baju ke lini produk lain, ide apa yang cocok?"
- "Stok bahan sering sisa/basi, ada ide solusinya?"

AI akan mengelompokkan permintaanmu (cepat / perlu diuji / perlu rencana) dan bilang ke kamu supaya bisa dikoreksi. Kalau info usahamu belum lengkap, AI tanya secukupnya — satu topik per pesan untuk yang penting. Kalau kamu buru-buru, bilang saja "langsung kasih ide aja" — nanti dipakai asumsi wajar dan disebutkan di akhir.

## Instalasi singkat
Salin folder `brainstorming-ide-usaha` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` yang disertakan dalam paket.

## FAQ
**Apakah skor idenya dikira-kira AI atau benar-benar dihitung?**
Benar-benar dihitung lewat script Python (`scripts/skor_ide.py`) dari nilai 1–5 per kriteria dan bobot yang kamu sepakati — bukan tebakan. Kalau Python tidak tersedia di perangkatmu, AI tetap menghitung manual dengan rumus yang sama dan menunjukkan cara hitungnya.

**Skill ini menjamin idenya pasti laku?**
Tidak. Ini alat bantu menyaring & menyusun rencana uji **murah** supaya kamu bisa tahu cepat apakah ide itu layak dilanjutkan atau tidak — bukan riset pasar profesional atau jaminan hasil. Setiap ide tetap perlu diuji nyata ke pelanggan.

**Harus tahu istilah bisnis rumit dulu?**
Tidak. SCAMPER, skor tertimbang, titik impas — semuanya dijelaskan dengan bahasa sehari-hari dan contoh dari usahamu sendiri, bukan jargon konsultan.
