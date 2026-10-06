# Alur status pesanan & penanganan pesanan tidak jelas

## Alur status
| Status | Artinya | Yang dicek sebelum naik ke status berikutnya | Pesan yang disiapkan |
|---|---|---|---|
| **Baru** | Chat pesanan masuk | Item & varian ada di katalog, jumlah jelas, stok cukup, harga diketahui | - |
| **Dikonfirmasi** | Rekap & total sudah dikirim ke pelanggan | Ongkir sudah pasti (atau ditandai `[isian: ongkir]`), alamat lengkap (jalan/no, RT/RW, kel, kec, kota, kode pos), HP penerima, kurir & layanan dipilih, COD/non-COD | Pesan konfirmasi |
| **Dibayar** | Pembayaran diterima | **Pemilik toko mengecek mutasi rekening/QRIS sendiri** lalu memberi tahu "sudah masuk". Nominal sama dengan total; kurang/lebih dicatat. COD melompati tahap ini (dibayar saat paket diterima) | Pengingat bayar bila belum; ucapan terima kasih bila lunas |
| **Dikemas** | Barang disiapkan | Isi paket cocok dengan rekap (varian, warna, ukuran, jumlah), catatan pelanggan (bungkus kado, dll.), label tertempel | Label pengiriman |
| **Dikirim** | Diserahkan ke kurir | Paket tercatat di daftar serah-terima per kurir; nomor resi dari kurir/aplikasi kurir dicatat | Pesan "pesanan dikirim + resi" |
| **Selesai** | Diterima pelanggan | Status pelacakan "diterima"; COD: uang sudah cair dari kurir | (opsional) terima kasih + minta ulasan |
| **Retur/batal** | Dikembalikan atau dibatalkan | Alasan, kondisi barang, siapa menanggung ongkir balik, uang dikembalikan atau tukar barang (keputusan pemilik: `[KEPUTUSAN PEMILIK]`) | Pesan tanggapan retur (tanpa janji di luar keputusan pemilik) |

Catatan:
- Pesanan yang belum dibayar **jangan** dikemas/dikirim kecuali COD atau pemilik memutuskan lain.
- Batas waktu bayar (mis. 1×24 jam) adalah kebijakan toko: tulis `[isian: batas waktu bayar]` bila pemilik belum menyebutnya.
- COD (syarat umum): ada kurir yang melayani COD untuk alamat tujuan, nilai COD = total yang harus dibayar penerima, biasanya ada biaya layanan COD yang dipotong kurir dari pencairan (besarnya `[isian: biaya COD]`, cek di aplikasi kurir), dan risiko paket ditolak/retur. Jangan mengutip tarif atau persentase.
- Kurir umum: JNE, J&T, SiCepat, AnterAja, Pos Indonesia; instan/sameday: GoSend (Gojek), GrabExpress. Ongkir selalu dari pengguna atau aplikasi kurir: `[isian: tarif]`.

## Pesanan tidak jelas
Prinsip: **proses yang sudah jelas, tandai yang belum, tanya di akhir maks. 3 hal per pesanan** (di pesan konfirmasi ke pelanggan) dan maks. 3 hal ke pemilik toko.

| Kasus | Yang dilakukan |
|---|---|
| Varian tidak ada di katalog ("yang ungu" padahal hanya merah/biru) | Item tidak dihitung; di pesan konfirmasi tawarkan varian yang ada. Jangan mengganti varian diam-diam |
| Nama barang mirip beberapa produk ("kaos" padahal ada polos & sablon) | Tanya pilihan; jangan menebak harga |
| Jumlah tidak disebut ("mau yang merah") | Tulis asumsi 1 pcs di rekap **dan** tanyakan di konfirmasi; atau biarkan "jumlah tidak jelas" bila konteks tidak mendukung |
| Stok habis/kurang (katalog punya kolom stok) | Tandai; pesan konfirmasi menawarkan jumlah yang tersedia, varian lain, atau tunggu restok `[isian: tanggal restok]` |
| Harga tidak ada di katalog dan tidak disebut | `[isian: harga]`; total ditahan sampai harga diisi |
| Alamat kurang (tanpa kode pos/kecamatan/no rumah) | Label tetap dibuat dengan `[isian: lengkapi alamat/kode pos]`; minta pelanggan melengkapi |
| HP penerima kosong/salah digit | Minta nomor HP penerima yang aktif (kurir butuh untuk menghubungi) |
| Kurir tidak dipilih | Tawarkan pilihan kurir yang dipakai toko `[isian: pilihan kurir]`; ongkir menyusul |
| Pesanan dobel (tempelan sama dua kali / pelanggan kirim ulang) | Dihitung sekali; sebut ke pemilik "dianggap pesanan yang sama, benar?" |
| Pelanggan menambah/mengubah pesanan di chat berikutnya | Pakai versi terakhir; sebut perubahan di rekap |
| Bayar kurang/lebih dari total | Sebut selisihnya persis; pemilik yang memutuskan (tagih sisa/kembalikan) |
