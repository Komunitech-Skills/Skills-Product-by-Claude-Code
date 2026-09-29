# Cara menyusun prioritas (ringkas)

## Rumus skor dari script
`skor = jumlah keluhan x dampak (1-5)`. Dampak bawaan: keamanan pangan/kebersihan 5; ketepatan pesanan 4; rasa 4; kualitas 4;
pengiriman/kemasan/porsi/layanan/pembayaran 3; harga/stok/varian 2. Ubah lewat `--tema tema.json` (`"dampak"`).
Frekuensi tanpa dampak menyesatkan: 1 laporan rambut di makanan lebih mendesak daripada 5 keluhan harga.

## Lapisan penyesuaian oleh agent (jelaskan alasannya)
1. **Keamanan/kesehatan** selalu "Segera" walau 1 laporan.
2. **Jangkauan:** muncul di >= 2 kanal = sinyal lebih kuat (bukan suara satu orang/satu grup).
3. **Tren:** naik dua bulan berturut-turut naikkan satu tingkat; turun sesudah perbaikan = bukti perbaikan berhasil.
4. **Pelanggan bernilai:** keluhan pelanggan langganan/korporat boleh diberi bobot, tapi sebut sebagai penilaian, bukan angka script.
5. **Usaha (1-5):** 1 = bisa besok sendiri (ubah deskripsi, tambah isolasi), 3 = butuh pemasok/kurir/biaya kecil, 5 = ubah proses/produk besar.

## Prioritas akhir = dampak dan usaha
| | Usaha kecil (1-2) | Usaha besar (4-5) |
|---|---|---|
| Dampak/skor tinggi | KERJAKAN MINGGU INI | Jadwalkan bulan ini, pecah jadi langkah kecil |
| Dampak/skor rendah | Kerjakan bila senggang | Tunda / tolak dengan alasan |

## Masukan berupa permintaan ("tambah menu X")
Jangan langsung menuruti solusi pelanggan. Cari masalah di baliknya (mis. "tidak ada menu vegetarian" = kebutuhan makan tanpa daging
untuk acara kantor). Beri 2-3 alternatif solusi, uji murah dulu (pesan uji 10 porsi, tanya 5 pelanggan) sebelum investasi.
Pertimbangkan: berapa orang yang minta, di kanal berapa, dan apakah cocok dengan arah usaha.

## Ukuran keberhasilan (wajib per perbaikan)
Tulis angka yang bisa dicek dari data bulan depan, mis. "keluhan pengiriman turun dari 21% menjadi < 10% masukan". Bandingkan dengan
`selisih_persen_poin` dari script bulan berikutnya. Data < 5 masukan per bulan = jangan menyimpulkan tren.
