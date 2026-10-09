# Template pesan ke pelanggan (siap kirim lewat WhatsApp/DM)

Aturan: sapaan memakai nama panggilan dari chat; angka disalin persis dari rekap; yang belum diketahui `[isian: ...]`; maks. 3 pertanyaan; tanpa janji di luar kebijakan toko. Huruf tebal WhatsApp memakai `*teks*`. Satu pesan per pelanggan; pemilik toko yang mengirim.

## 1. Konfirmasi pesanan
```
Halo Kak [nama panggilan], terima kasih sudah order di [nama toko] 🙏
Pesanannya kami rekap ya:

[kode pesanan]
• [nama barang] x[qty] = [total baris]
• ...
Subtotal: [subtotal]
Diskon [label]: -[diskon]          ← hapus baris bila tidak ada
Ongkir [kurir layanan]: [ongkir atau [isian: ongkir]]
*Total: [total]*

Pembayaran via transfer ke:
[bank] [no rekening] a.n. [nama pemilik rekening]
Mohon transfer sesuai total, lalu kirim bukti transfernya di chat ini ya, Kak. [batas waktu bayar bila ada]

[Bila data kirim kurang — maks. 3 pertanyaan:]
Supaya paket tidak nyasar, boleh dilengkapi:
1. [mis. alamat lengkap: jalan & nomor rumah, RT/RW, kelurahan, kecamatan, kota, kode pos]
2. [mis. nomor HP penerima yang aktif]
3. [mis. pilih kurir: JNE / J&T / SiCepat]

Terima kasih, Kak 😊
```
Versi COD: ganti blok pembayaran dengan "Pembayaran *COD* sebesar [nilai COD] dibayar ke kurir saat paket diterima. Mohon pastikan ada yang menerima di alamat ya, Kak." Versi ambil sendiri: "Pesanan bisa diambil di [isian: alamat toko/jam ambil]."

Bila total belum bisa dihitung (harga/ongkir belum ada), jangan menulis total karangan: "Total akan kami kabari setelah ongkir dicek, ya Kak" dan baris `Ongkir: [isian: ongkir]`.

## 2. Pengingat pembayaran (sopan, satu kali, tanpa ancaman)
```
Halo Kak [nama panggilan], sekadar mengingatkan pesanan [kode pesanan] ([ringkas isi]) sebesar *[sisa tagihan]* belum kami terima pembayarannya.
Transfer ke [bank] [no rekening] a.n. [nama]. Kalau sudah transfer, boleh kirim bukti transfernya ya, Kak, biar langsung kami kemas.
Kalau ada perubahan pesanan, kabari saja. Terima kasih 🙏
```
Bayar sebagian: sebut "sudah kami terima [dibayar], kurang [sisa]".

## 3. Pesanan dikirim + resi
```
Halo Kak [nama panggilan], pesanan [kode pesanan] sudah kami kirim hari ini lewat [kurir layanan] 📦
No. resi: [isian: resi]
Bisa dilacak di aplikasi/situs resmi [kurir]. [COD: Siapkan pembayaran [nilai COD] untuk kurir ya, Kak.]
Terima kasih sudah belanja di [nama toko]!
```
Resi **tidak pernah** dikarang; selalu `[isian: resi]` sampai pemilik memberikan nomor dari kurir.
