# Pra-cek konteks Telegram gelombang 7 (2026-10-05)

Metode: `uji-tg.sh` (konteks kanal Telegram, tanpa kirim), 1 kali per skill, dinilai hanya dari isi balasan chat.

| skill | skor internal | skor konteks Telegram | MASALAH TELEGRAM? | catatan |
|---|---|---|---|---|
| tulisan-tanpa-kesan-ai | 8,7 | 8,0 | Tidak | Satu caption siap tempel, harga/ukuran utuh, daftar "yang diubah". Cacat kecil: "kami pilih langsung" menyiratkan klaim sumber langsung yang tidak ada di draf asli. |
| luncurkan-produk-baru | 9,0 | 7,0 | YA (bertanya padahal info cukup) | Gerbang BPOM benar (12 Okt = teaser/daftar tunggu, bukan jual). Namun tidak ada rencana sama sekali; hanya 5 pertanyaan, padahal ada default yang ditawarkan sendiri. |
| proposal-kerjasama | 8,33 | 6,5 | YA (bertanya padahal info cukup) | Menolak klaim "sudah BPOM"/"paling laris" dengan tepat, tetapi tidak ada proposal dan tidak memperingatkan porsi 35% rugi (Rp15.000 x 35% = Rp5.250 untuk toko). Hanya 4 pertanyaan. |
| pengajuan-kur | 9,0 | 9,0 | Tidak | Lengkap di chat, angka benar, opsi tenor 60 bulan, peringatan flat vs efektif, tanpa agunan <= Rp100 jt. |
| uji-pasar-produk-cepat | 9,0 | 9,0 | Tidak | Keputusan tegas ULANGI UJI, Wilson 0%-24% benar, langkah DP konkret. |
| pesan-prospek-wa (cadangan) | 9,0 | 7,0 | YA (bertanya padahal info cukup) | Koreksi zona waktu benar (19.30 WIB = 20.30 WITA, usul 19.00 WIB), tetapi tidak ada draf pesan sama sekali; 5 pertanyaan. |
| pph21-ter (cadangan) | 9,25 | 8,5 | Tidak | Jawaban lengkap di chat, dua skenario DTP, angka benar. Hanya minta konfirmasi KLU (wajar). |

Tidak ada balasan terpotong, timeout, "lihat file", atau kebocoran proses internal.

## Verifikasi angka (python)
- Anuitas Rp75.000.000, 6% efektif, 36 bln = Rp2.281.645,31 (cocok); 35,10% dari laba Rp6,5 jt (cocok); sisa Rp4.218.355 (cocok).
- 60 bln = Rp1.449.960,11 (cocok); 22,31% (cocok).
- Plafon rasio 30%: Rp64.098.481 (balasan Rp64.098.000, cocok).
- Flat 6% 36 bln = Rp2.458.333/bln, setara efektif 11,08% (cocok "±11%").
- Wilson 95% untuk 0/12: 0%-24,25% (cocok); 5/12 = 41,7% (cocok).
- Bunga KUR: Permenko 1/2026, Mikro/Kecil sektor produksi 6% efektif (web 2026-10-05, bisnis.com / investor.id). Bengkel (jasa) diasumsikan 6%; balasan sudah berlabel "acuan, konfirmasi ke bank".

## Rekomendasi
Layak tampil (skor >= 8, tanpa masalah): pengajuan-kur, uji-pasar-produk-cepat, tulisan-tanpa-kesan-ai (8,0 mepet). Tahan luncurkan-produk-baru dan proposal-kerjasama: pada konteks Telegram skill bertanya dulu dan tidak memberi hasil; perlu satu pesan pemicu yang memberi default atau tinjau instruksi "tanya sekali" (jangan ubah skill tanpa persetujuan).

## Tambahan cadangan
- PPh 21 TER kategori A (TK/0), PMK 168/2023: bruto Rp6.000.000 ada di lapisan >5,95 jt s.d. 6,3 jt = 0,75% -> Rp45.000 (cocok); diterima Rp5.955.000 (cocok).
- DTP 2026 (PMK 105/2025, web 2026-10-05: ortax, pasardana, dwpconsulting): lima sektor padat karya termasuk tekstil & pakaian jadi, penghasilan bruto tetap <= Rp10 jt/bln, DTP dibayar tunai ke pegawai dan bukan penghasilan kena pajak. Skenario B balasan (Rp6.045.000) konsisten.
- Rekomendasi cadangan: pph21-ter layak tampil (8,5); pesan-prospek-wa tahan.

## Uji ulang setelah perbaikan (penguji independen, 2026-10-05)
| skill | versi | skor 3 percobaan | rata-rata | lulus | verdik |
|---|---|---|---|---|---|
| luncurkan-produk-baru | 1.0.5 | 8,5 / 8,5 / 8,5 | 8,5 | 3/3 | LULUS (rencana lengkap + gerbang BPOM, tanggal & stok cocok python, 3 pertanyaan di akhir) |
| proposal-kerjasama | 1.0.8 | 8,3 / 9,0 / 8,0 | 8,43 | 3/3 | LULUS (proposal lengkap, klaim palsu ditangani, Rp5.250/Rp9.750 benar; 1 timeout model diulang) |
Keduanya layak masuk daftar tampil Telegram. Catatan kecil proposal-kerjasama: percobaan 1 memakai "termasuk yang paling laris" dengan slot bukti.
