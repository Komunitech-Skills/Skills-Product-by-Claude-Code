# Cara kerja skor prioritas

## RICE (bila ada angka perkiraan)
`skor = jangkauan x dampak x (keyakinan/100) / usaha`
- **Jangkauan:** perkiraan berapa orang/pembeli tersentuh dalam satu periode (mis. 3 bulan). Contoh: pengikut yang bisa dijangkau, jumlah pesanan/bulan.
- **Dampak:** 0,25 (kecil sekali), 0,5 (kecil), 1 (sedang), 2 (besar), 3 (sangat besar) per orang.
- **Keyakinan:** persen (100 = ada data/uji; 80 = cukup yakin; 50 = tebakan; di bawah itu = hampir spekulasi).
- **Usaha:** total orang-hari kerja (riset, uji, produksi awal, desain, promosi).

## ICE (bila hanya punya perasaan)
`skor = dampak x keyakinan x kemudahan`, masing-masing 1-10 (kemudahan 10 = sangat mudah/murah).

## Cara membaca
Skor tinggi = layak lebih dulu. Skor hanya membandingkan **ide di daftar yang sama** dengan metode yang sama. Dua ide seri: yang usahanya lebih kecil didahulukan. Ide berskor tinggi tapi keyakinan rendah: uji kecil dulu.

## Format CSV
RICE: `nama,jangkauan,dampak,keyakinan,usaha`. ICE: `nama,dampak,keyakinan,kemudahan`. Pemisah `,` `;` atau tab. Desimal `0,5` atau `0.5`; ribuan `1.500` (titik + tepat 3 angka) dibaca 1500.

## Rumus manual (bila script tidak bisa jalan)
Contoh RICE: jangkauan 500, dampak 1, keyakinan 80%, usaha 4 orang-hari: 500 x 1 x 0,8 / 4 = 100.

## Kerangka pendukung (opsional)
- Prioritaskan **masalah pembeli**, bukan daftar fitur; tanya "pembeli mana yang kesulitan apa, seberapa sering?"
- MoSCoW (Harus/Sebaiknya/Bisa/Tidak sekarang) boleh dipakai sebagai penyaring awal untuk fitur pengiriman ke pihak lain.
- Kano (dasar/kinerja/kejutan): untuk memahami harapan pembeli, bukan untuk mengurutkan.
