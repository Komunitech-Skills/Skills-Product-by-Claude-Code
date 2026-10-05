# Asumsi, Kriteria, Keputusan, dan Pivot

## 1. Daftar asumsi paling berisiko (contoh frozen food)
Format tiap asumsi: "Kami berasumsi bahwa ... " + cara membuktikan salah.

| # | Kelompok | Asumsi | Dampak (1-5) | Ketidakpastian (1-5) | Skor | Eksperimen |
|---|---|---|---|---|---|---|
| 1 | Minat | Pelanggan dimsum ayam mau varian mentai | 5 | 4 | 20 | Pre-order WA |
| 2 | Harga | Mau bayar Rp45.000 per 10 pcs | 5 | 4 | 20 | Banding harga A/B |
| 3 | Produksi/kirim | Tetap beku dan enak setelah dikirim 2 hari | 5 | 3 | 15 | Kirim 5 paket uji ke luar kota |
| 4 | Untung | Margin > 30% setelah kemasan, es gel, ongkir | 4 | 3 | 12 | Hitung dengan hitung-hpp |
| 5 | Ulang | Pembeli pesan lagi dalam 30 hari | 4 | 4 | 16 | Sampel bazar, tanya niat + cek pesanan ke-2 |
| 6 | Jangkauan | Kontak WA cukup untuk 100 pembeli/bulan | 3 | 3 | 9 | Hitung dari hasil PO |
| 7 | Izin | PIRT/label halal bisa diurus sebelum jual luas | 4 | 2 | 8 | Cek persyaratan, tunda uji |

Urutkan menurut skor. Uji yang teratas dulu, satu-dua per putaran. Asumsi "produksi/kirim" sering terlewat padahal paling sering membunuh usaha makanan beku.

Tiga sudut pikir untuk menemukan asumsi: **pembeli** (kenapa mereka tidak mau?), **operasional** (kenapa tidak bisa kita buat/kirim?), **uang** (kenapa tidak untung?).

## 2. Kriteria sukses: cara menulis
"Eksperimen [nama] dianggap LULUS jika **[jumlah aksi]** dari **[jumlah ditawari]** orang **[aksi nyata]** sebelum **[tanggal]**. Jika kurang dari **[S]%**: STOP. Di antaranya: UBAH [variabel]."

Patokan awal (heuristik praktis, bukan angka baku; sesuaikan dengan margin dan pengalaman):

| Eksperimen | Ukuran sukses | T (lanjut) | S (stop) |
|---|---|---|---|
| Pre-order WA ke kontak hangat | Bayar/DP ÷ ditawari | 15% | 7-8% |
| Sistem PO | Pesanan terbayar sampai tenggat ÷ ditawari | 10-15% | 5% |
| Sampel/tester bazar | Beli atau minta kontak pesan ulang ÷ yang mencoba | 30% | 15% |
| Landing page + link WA | Chat WA ÷ pengunjung | 5% | 2% |
| Listing marketplace uji | Pesanan ÷ pengunjung listing | 2% | 0,5% |
| Konten TikTok | Komentar/klik ke WA ÷ tayangan | 1% | 0,3% |
| Survei Google Form | "Mau beli" ÷ responden (pelengkap) | 40% | 20% (dan tetap butuh uji bayar) |

Semua angka di atas kasar dan bergantung kategori; kalau pengguna punya data sendiri (penjualan sebelumnya), pakai itu.

## 3. Aturan praktis jumlah sampel
- Rumus kasar: n = 3,84 x p x (1 - p) ÷ margin^2 (p = perkiraan konversi, margin dalam desimal). Contoh: p 20%, margin +-10 poin -> 3,84 x 0,16 ÷ 0,01 = 61,5, jadi 62 orang. Tanpa perkiraan pakai p = 50%: margin +-10 -> 97 orang; +-5 -> 385 orang.
- Skala UMKM: 30 (minimum arah), 50-100 (cukup untuk lanjut/stop kasar), 100+ (baru layak untuk selisih kecil).
- Konversi rendah (1-5%): margin sekitar separuh perkiraan (mis. p 4%, margin 2 -> 3,84 x 0,04 x 0,96 ÷ 0,0004 = 368,6, jadi 369 orang). Margin yang sama atau lebih besar dari perkiraan membuat rentang menyentuh 0% dan tidak berguna.
- Dua varian: di bawah 50 per varian hanya sinyal arah. Jumlah **per varian** agar selisih terdeteksi dengan power 80% dan alfa 5% (dua sisi), rumus n = [1,96 x akar(2 x p̄ x (1 - p̄)) + 0,8416 x akar(pA(1 - pA) + pB(1 - pB))]^2 ÷ (pA - pB)^2, p̄ = rata-rata pA dan pB:

| Varian A vs B | Orang per varian | Total |
|---|---|---|
| 5% vs 10% | 435 | 870 |
| 10% vs 20% | 199 | 398 |
| 15% vs 25% | 250 | 500 |
| 10% vs 15% | 686 | 1.372 |
| 20% vs 25% | 1.094 | 2.188 |

  Power 80% artinya: kalau selisih sebenarnya memang sebesar itu, uji menemukannya kira-kira 8 dari 10 kali. Hitung kasus lain: `python3 scripts/hasil_eksperimen.py sampel --banding --a 15 --b 25`.
- Sampel kecil (< 50 per varian atau ada sel harapan < 5): script memakai uji Fisher tepat, bukan uji z, dan tidak menyatakan pemenang pasti. Contoh: 0/10 vs 4/10 terlihat jauh (0% vs 40%), tapi p Fisher = 0,087, jadi belum meyakinkan.
- Lebih baik dua uji bersih yang sama besar daripada sepuluh uji kecil-kecil yang tercampur.
- Sampel harus **tidak bias**: jangan hanya menawari teman dekat; jangan menawari varian B ke orang yang lebih royal.
- Hitung tepat: `python3 scripts/hasil_eksperimen.py sampel --margin 10 --perkiraan 20`.

## 4. Aturan keputusan
| Kondisi | Keputusan |
|---|---|
| konversi >= T, batas bawah Wilson >= T, sampel >= 30 | LANJUT (kuat) |
| konversi >= T, batas bawah < T (atau sampel < 30) | LANJUT BERTAHAP / tambah sampel |
| S <= konversi < T | UBAH satu variabel, uji ulang (maks. 2 kali) |
| konversi < S | STOP atau pivot |
| Sampel < 30 | Sinyal arah saja; putuskan hanya untuk langkah kecil |

Setelah dua putaran UBAH tanpa perbaikan, anggap STOP atau pivot besar.
Bias yang harus diwaspadai: memilih angka target sesudah tahu hasil; menghitung "minat" sebagai pembeli; membuang orang yang menolak dari hitungan; menghentikan uji tepat saat hasil terlihat bagus.

## 5. Opsi pivot (pilih satu, uji lagi)
Tanya dulu: siapa yang **justru** bereaksi baik? Apa alasan penolakan yang paling sering?
| Pivot | Pertanyaan pemicu | Contoh frozen food |
|---|---|---|
| Pembeli | Siapa yang antusias walau bukan target awal? | Dari ibu rumah tangga ke pemilik kafe/kantin |
| Masalah | Masalah apa yang mereka sebut sendiri? | Dari "lauk keluarga" ke "stok praktis anak kos" |
| Penawaran | Apakah harga/ukuran/paket yang jadi penghalang? | Paket 5 pcs coba-coba; langganan mingguan |
| Kanal | Di mana pembeli sebenarnya berada? | Dari WA pribadi ke marketplace atau titip kantin |
| Produk | Isi apa yang mereka minta? | Varian pedas, bukan mentai |
| Stop bersih | Tidak ada pola positif sama sekali | Catat pelajaran, kembalikan DP, ganti ide |
Ubah hanya **satu** hal per putaran supaya penyebab perbaikan jelas.
