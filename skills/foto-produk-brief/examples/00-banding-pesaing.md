# 00 — Uji banding pesaing (S1)

## Pencarian
- Kata kunci: "SKILL.md product photography", "product photography brief shot list claude skill", "smartphone product photo skill", "foto produk HP skill".
- Sumber dicek: github.com/anthropics/skills (tidak ada; `canvas-design`/`brand-guidelines` tidak relevan), github.com/manairalabs/bicara-skills & github.com/alvinindra/bahasa-skills (tidak ada skill foto), github.com/VoltAgent/awesome-openclaw-skills (yang ada `eachlabs-product-visuals`, `bria-ai-*`: pembuat gambar lewat API berbayar, bukan brief memotret), github.com/kostja94/marketing-skills (`visual-content`, `image-optimization`: SEO/visual umum), pencarian web (nanoskill "amazon product photography skill", katalog tertutup, tidak dibaca).
- **Pesaing paling sebanding:** `product-shots-main-image` + hub `product-shots`, dari github.com/motiful/product-shots, **lisensi MIT**. Pendekatannya: brief & prompt untuk **gambar yang dibuat AI** (Amazon + platform sosial), dengan daftar foto sekunder per kategori.
- Script & panggilan API pihak ketiga **tidak dijalankan**. Isi tidak disalin.

## Output dengan instruksi pesaing (disimulasikan, input S1)
Instruksi: hub bertanya satu dimensi per giliran (maks. 5 putaran: platform → aset visual → tujuan → gaya), lalu merutekan ke `product-shots-main-image`, yang menetapkan aturan foto utama Amazon (putih murni RGB 255, produk ≥ 85% bingkai, tanpa teks/logo) dan paket foto sekunder kategori apparel: Multi-angle + Detail Shot + Lifestyle + Variants. Gambar lalu dibuat lewat skill `product-shots-image-gen` (butuh API key).

> *(Putaran 1)* "Platform apa yang dituju? <suggestion>Amazon</suggestion> <suggestion>TikTok Shop</suggestion> <suggestion>Instagram</suggestion>…"
> *(setelah 3–4 putaran)* **Brief:**
> - Main image: hijab voal, pure white background RGB(255,255,255), product fills ≥85% of frame, even studio lighting, no text/logo. Apparel: real model standing or flat lay, no mannequin.
> - Secondary: (1) multi-angle, (2) detail shot of voal texture, (3) lifestyle, woman wearing hijab in café, (4) variants: 4 colors in a row.
> - Negative prompt: "social media UI, screenshot, watermark, messy background, distorted text, phone frame, app interface".
> - Route → `product-shots-main-image` → generate via image-gen (1024×1024, 1:1), secondary images referencing the main image URL.

## Output dengan skill kita
Lihat `01-hijab-voal-4-warna.md`.

## Penilaian
| Kriteria | Pesaing (`product-shots`) | Skill kita (`foto-produk-brief`) |
|---|---|---|
| Kesesuaian tugas (memotret sendiri dengan HP) | Rendah: menghasilkan gambar AI, butuh foto referensi & API key | Tinggi: lembar kerja memotret dengan HP, jendela, karton |
| Kejujuran visual | Risiko: gambar AI bisa berbeda dari barang asli. Aturannya sendiri menulis "real product photo only", bertentangan dengan pendekatannya | Menekankan warna/ukuran asli, tes warna, larangan filter & klaim |
| Konteks Indonesia | Amazon-sentris (aturan ≥ 85%, "delisting"); tidak mengenal Shopee/TikTok Shop Indonesia | Shopee/TikTok Shop, keranjang kuning, ketentuan platform diarahkan ke Seller Center |
| Akurasi aturan platform | Menerapkan angka Amazon sebagai "MUST" universal | Tidak mengarang angka platform |
| Siap pakai untuk awam | Klarifikasi 5 putaran; hasil berupa prompt berbahasa Inggris | Satu lembar berbahasa Indonesia, langsung dikerjakan |
| Video | Tidak menjadi fokus (ada skill terpisah) | 2 storyboard per detik |
| **Keseluruhan** | – | **Skill kita menang** untuk tugas ini |

## Yang bisa dipelajari dari pesaing (ide, bukan salinan)
1. **Paket foto sekunder per kategori** yang eksplisit (mis. apparel = multi-angle + detail + lifestyle + varian). Kita sudah punya per kategori di `shot-list-kategori.md`, tapi urutan prioritas slot per kategori bisa dibuat lebih tegas.
2. **Konsistensi antar-foto berjangkar foto utama**: aturan "setting kamera, jarak & cahaya dikunci dari foto utama untuk semua varian" bisa ditulis sebagai satu butir checklist.
3. **Ukuran teks minimum di infografik** agar terbaca di layar HP (pesaing punya batas minimum). Tambahkan panduan "teks infografik ≤ 4 poin, cukup besar dibaca di HP tanpa zoom".
4. **Pilihan jawaban singkat saat bertanya** (opsi yang bisa diklik) untuk mempercepat pengguna awam menjawab pertanyaan S4.
