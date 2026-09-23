# Etika Promo & Urgensi Jujur di Live Jualan

Dicatat 2026-09-23. Ini panduan praktis, bukan nasihat hukum.

## Dasar aturan
- **UU No. 8 Tahun 1999 tentang Perlindungan Konsumen.** Pelaku usaha dilarang menawarkan/mengiklankan
  dengan pernyataan tidak benar atau menyesatkan mengenai harga, potongan harga, atau hadiah (lihat Pasal 9
  dan 10), serta dilarang menawarkan harga khusus dalam waktu/jumlah tertentu bila tidak bermaksud
  melaksanakannya sesuai waktu/jumlah yang ditawarkan (lihat Pasal 12).
  Teks resmi: cari "UU 8 Tahun 1999" di https://peraturan.bpk.go.id
- **Kebijakan komunitas & penjual TikTok Shop / Shopee Live**: umumnya melarang informasi palsu,
  mengarahkan transaksi ke luar platform, dan produk terlarang. Detail berubah — cek pusat edukasi penjual.

## Urgensi yang BOLEH (karena benar)
| Jenis | Syarat | Contoh kalimat |
|---|---|---|
| Stok live terbatas | Angka stok nyata di sistem/etalase | "Stok harga live di keranjang tinggal 12 ya, angkanya kelihatan di layar." |
| Batas waktu promo | Voucher/flash sale memang berakhir jam itu | "Voucher live berlaku sampai live selesai jam 21.00." |
| Kuota voucher | Kuota voucher memang dibatasi sistem | "Voucher potongan Rp 10.000 kuotanya 50, sekarang sisa 18." |
| Bonus terbatas | Jumlah bonus nyata | "Bonus inner untuk 20 checkout pertama — saya sebut nama yang dapat ya." |
| Stok produksi | Memang produksi terbatas (batik tulis, pre-order) | "Batik tulis ini dikerjakan tangan, bulan ini cuma ada 8 lembar." |

## Urgensi yang DILARANG (kelangkaan palsu)
- Menyebut "tinggal 3!" padahal stok banyak, atau angka sisa stok yang dikarang.
- Hitung mundur yang diulang terus ("5 menit lagi harga naik" tapi tidak pernah naik).
- Harga coret yang dinaikkan dulu supaya diskon terlihat besar.
- "Udah 500 orang checkout" / testimoni / nama pembeli yang dikarang.
- "Besok harga naik" bila tidak ada rencana nyata.
- "Harga termurah se-Indonesia", "paling laris" tanpa data.
- Klaim kesehatan/kecantikan berlebihan ("pasti putih dalam 3 hari", "menyembuhkan").

Jika pengguna meminta taktik di atas: tolak dengan sopan, jelaskan risikonya (keluhan pembeli, penalti
akun, sanksi UU Perlindungan Konsumen), lalu tawarkan versi jujur dari tabel "BOLEH".

## Aturan angka di naskah
- Semua harga, potongan, persen, dan harga per pcs bundling dihitung dengan `scripts/hitung_promo.py`.
- Persen hemat diucapkan dibulatkan ke bawah ("hemat 22%", bukan 23% untuk 22,47%).
- Angka stok/kuota ditulis sebagai `[stok nyata]` di naskah; host membacanya dari layar saat live.
