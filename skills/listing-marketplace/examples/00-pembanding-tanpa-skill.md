# 00 — Uji A/B: S1 dengan vs tanpa skill

**Input pengguna (sama persis dengan S1):**
> Bikinin listing buat gamis busui aku, namanya Gamis Alya dari Rumah Alya (Solo). Bahan katun rayon, ada resleting depan buat menyusui. Ukuran M (LD 100, PB 135), L (LD 106, PB 137), XL (LD 112, PB 139). Warna navy, sage, mocca. Mau upload di Shopee, Tokopedia, sama TikTok Shop.

## Output TANPA skill (AI agent biasa, tanpa membaca skill apa pun)
```
JUDUL PRODUK
Gamis Busui Alya Premium Katun Rayon Resleting Depan Wudhu Friendly Tidak Menerawang Busana Muslim Wanita Terbaru 2026 Navy Sage Mocca M L XL

DESKRIPSI PRODUK
✨ GAMIS ALYA – Tampil Anggun Sambil Menyusui ✨

Gamis Alya hadir untuk Bunda yang ingin tetap stylish sekaligus praktis saat menyusui! Terbuat dari bahan katun rayon premium
yang adem, lembut, tidak menerawang, dan nyaman dipakai seharian. 💕

🌸 Keunggulan:
- Resleting depan, busui friendly
- Wudhu friendly (lengan bisa dilipat)
- Bahan premium, adem & tidak panas
- Jahitan rapi & kuat
- Cocok untuk acara formal maupun santai

📏 Size Chart:
M: LD 100 cm, PB 135 cm
L: LD 106 cm, PB 137 cm
XL: LD 112 cm, PB 139 cm

🎨 Pilihan warna: Navy, Sage, Mocca

📦 Dikirim dari Solo
💬 Ada pertanyaan? Chat kami ya, Bunda!

#gamisbusui #gamismurah #gamiskatun #busanamuslim #gamisterbaru

(Judul dan deskripsi ini bisa dipakai untuk Shopee, Tokopedia, dan TikTok Shop.)
```

## Output DENGAN skill
Lihat `01-gamis-busui-tiga-platform.md` (kata kunci 3 lapis, 3 judul per platform dengan panjang dicek, deskripsi Shopee/Tokopedia + versi ringkas
TikTok Shop, hasil cek script, daftar `[isi: …]`).

## Berdampingan

| Aspek | TANPA skill | DENGAN skill |
|---|---|---|
| Panjang judul | **141 karakter** (dihitung) — melebihi batas aman Tokopedia 70 dan Shopee/TikTok 100; akan terpotong/ditolak | 80 / 57 / 68, lulus cek, diberi label "cek batas terbaru" |
| Satu judul untuk 3 platform | Ya | Judul berbeda per platform (Tokopedia paling ringkas) |
| Klaim karangan | "premium", "tidak menerawang", "wudhu friendly (lengan bisa dilipat)", "jahitan rapi & kuat", "terbaru 2026" — **tidak diberikan pengguna** | Tidak ada; data kosong ditandai `[isi: …]` |
| Format deskripsi | Hashtag di deskripsi marketplace, emoji dekoratif di judul-level | Teks polos siap tempel, emoji ✅ hanya penanda poin |
| Info yang hilang | Tidak ada isi paket, perawatan, retur | Bagian lengkap dengan `[isi: …]` agar pengguna ingat melengkapi |
| Kata kunci | Tidak ada daftar | Utama/pendukung/ekor panjang + posisi kata kunci utama dicek |

## Penilaian
- **Lebih baik berkat skill:** (1) judul tanpa skill 141 karakter — gagal di ketiga platform; (2) lima klaim karangan yang bisa memicu komplain
  ("tidak menerawang", "wudhu friendly" padahal lengan tidak disebut bisa dilipat); (3) judul per platform + label batas; (4) deskripsi polos siap tempel.
- **Setara:** tabel ukuran dan warna sama-sama benar.
- **Kesimpulan:** hasil dengan skill **jelas lebih baik** — lebih aman dan langsung bisa diunggah.
