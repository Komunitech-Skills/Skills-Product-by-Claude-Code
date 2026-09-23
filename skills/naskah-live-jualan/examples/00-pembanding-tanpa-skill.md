# 00 — Uji A/B: S1 dengan vs tanpa skill

**Input pengguna (sama persis dengan S1):**
> Bikinin script live TikTok 1 jam ya, mulai jam 8 malam. Toko Batik Lestari dari Pekalongan. Produk: Kemeja batik cap pria katun primisima, normal 185rb, pas live 149rb, beli 2 jadi 280rb. Daster batik rayon allsize (LD 120), 95rb diskon 15%. Kain batik tulis 2 meter pewarna alam, 650rb gak diskon, stoknya emang cuma 5 lembar bulan ini. Kirim tiap hari dari Pekalongan, gak ada COD. Retur boleh kalau salah kirim, wajib video unboxing.

## Output TANPA skill (AI agent biasa, tanpa membaca skill apa pun)
```
SCRIPT LIVE TIKTOK – BATIK LESTARI (20.00–21.00)

20.00–20.05 | OPENING
"Halo semuanya, selamat malam! Selamat datang di live Batik Lestari, batik asli Pekalongan! Jangan lupa tap-tap layarnya,
follow, dan share ke teman-teman ya! Malam ini banyak promo spesial, jadi jangan ke mana-mana!"

20.05–20.20 | PRODUK 1: KEMEJA BATIK CAP PRIA
"Kemeja batik cap dari katun primisima premium, adem, nyaman, dan tidak luntur. Cocok untuk kerja maupun kondangan.
Harga normal Rp185.000, khusus live cuma Rp149.000! Diskon hampir 20%! Beli 2 cuma Rp280.000, jadi lebih hemat lagi!
Stok terbatas ya kak, buruan checkout sebelum kehabisan!"

20.20–20.35 | PRODUK 2: DASTER BATIK
"Daster batik rayon allsize, LD 120 cm, adem dan cocok untuk di rumah. Harga normal Rp95.000, diskon 15% jadi Rp80.750!
Langsung klik keranjang kuning ya!"

20.35–20.50 | PRODUK 3: KAIN BATIK TULIS
"Kain batik tulis asli 2 meter dengan pewarna alam, dibuat tangan oleh pengrajin berpengalaman. Stok hanya 5 lembar,
siapa cepat dia dapat! Harga Rp650.000."

20.50–21.00 | CLOSING & Q&A
"Terima kasih sudah menonton! Yang belum checkout, buruan sebelum promo berakhir. Pengiriman setiap hari dari Pekalongan.
Retur bisa jika salah kirim dengan video unboxing. Sampai jumpa di live berikutnya!"

Tips: Gunakan hitung mundur untuk menciptakan urgensi, sapa penonton dengan nama, dan sering ulangi promo.
```

## Output DENGAN skill
Lihat `01-tiktok-live-batik-60-menit.md` (rundown per menit 24 segmen, tabel angka promo dari script, naskah siap ucap per segmen dengan
arahan aksi, rekap penonton baru, bank jawaban 10 pertanyaan, catatan host).

## Berdampingan

| Aspek | TANPA skill | DENGAN skill |
|---|---|---|
| Rundown | 4 blok besar 15 menit | 24 segmen per menit (hook, demo, harga, CTA, tanya-jawab per produk) + putaran 2 produk andalan |
| Harga daster | "Rp80.750" — angka ganjil yang belum tentu bisa dipasang di keranjang; host bilang "diskon 15%" | Rp 81.000 (dibulatkan ke atas), host diarahkan bilang "hemat Rp 14.000", **bukan** 15% |
| Paket isi 2 | "lebih hemat lagi" tanpa angka | Rp 140.000/pcs, hemat Rp 90.000 vs 2× normal (terverifikasi) |
| Urgensi | "Stok terbatas, buruan sebelum kehabisan!" untuk kemeja (tidak ada data stok) + tips "hitung mundur" | Hanya stok nyata kain tulis (5 lembar) & `[stok nyata]` dari layar |
| Klaim | "premium", "tidak luntur", "batik asli", "pengrajin berpengalaman" — **tidak diberikan pengguna** | Tidak ada klaim karangan; data yang kurang ditandai `[isi: …]` |
| COD | Tidak disebut (penonton akan bertanya) | Disebut jelas "belum ada COD" di CTA & bank jawaban |
| Penonton baru | Tidak ada rekap | Rekap di menit 25 + tanya-jawab bebas & rekap |
| Cara checkout | "klik keranjang kuning" | Langkah konkret: keranjang → nomor produk → ukuran/varian paket → checkout |
| Bank jawaban | Tidak ada | 10 pertanyaan umum siap jawab |

## Penilaian
- **Lebih baik berkat skill:** (1) kejujuran: tanpa skill muncul kelangkaan palsu ("stok terbatas", saran hitung mundur) dan 4 klaim karangan
  ("tidak luntur" berisiko komplain); (2) angka promo yang bisa diucapkan dengan jujur (15% vs 14% setelah pembulatan); (3) rundown per menit
  yang benar-benar bisa dibaca host; (4) bank jawaban & info COD mencegah host gelagapan.
- **Setara:** harga live dan harga normal kemeja sama-sama benar.
- **Kesimpulan:** hasil dengan skill **jelas lebih baik** dan lebih aman bagi penjual.
