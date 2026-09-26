# Contoh 1 — Pesanan Salah Kirim Massal

## Input pengguna
> "Buatin laporan insiden. Kemarin pas promo 9.9, 40 pesanan label alamatnya kesalahan gara-gara admin salin data dari sheet lama. Ketahuan jam 14.00 pas ada komplain masuk 5 pelanggan, packing mulai jam 09.00. Kita udah hubungin kurir buat batalin 25 paket yang belum diambil, 15 sisanya udah terlanjur jalan. Kerugian ongkir kirim ulang sekitar Rp1.500.000. Toko namanya Kedai Rempah Bu Sri."

## Output skill

# Laporan Insiden: Pesanan Salah Kirim Massal Saat Promo 9.9

**Tanggal kejadian:** 9 September 2026 · **Ketahuan:** 14.00 · **Status:** Sebagian ditangani, sisanya masih berjalan

## Kronologi
09.00 — Tim packing mulai mencetak label pengiriman untuk pesanan promo 9.9.
14.00 — Komplain masuk dari 5 pelanggan yang menerima paket dengan alamat tidak sesuai.
14.00–14.30 — Dicek, ditemukan 40 pesanan memakai label dengan alamat salah karena data disalin dari sheet alamat versi lama.
14.30 — Tim menghubungi kurir: 25 paket berhasil dibatalkan sebelum diambil kurir, 15 paket lainnya sudah terlanjur dikirim.

## Dampak
- Pelanggan/pesanan terdampak: 40 pesanan
- Kerugian: sekitar Rp1.500.000 (ongkir kirim ulang)
- Lainnya: 5 komplain pelanggan masuk langsung, berpotensi bertambah dari 15 paket yang masih di jalan

## Akar Masalah (5 Kenapa)
1. Kenapa 40 pesanan salah alamat? → Karena label dicetak dari data alamat yang sudah tidak terbaru.
2. Kenapa datanya tidak terbaru? → Karena admin menyalin dari sheet alamat versi lama, bukan versi yang sudah diperbarui.
3. Kenapa tidak ketahuan sebelum dicetak? → Karena tidak ada langkah cek ulang sebelum cetak label saat volume pesanan tinggi.
4. Kenapa langkah cek ulang itu tidak ada? → Karena SOP packing belum disesuaikan sejak volume pesanan naik signifikan saat periode promo.

**Akar masalah:** SOP packing belum mencakup langkah verifikasi data alamat sebelum cetak label massal saat volume promo tinggi.

## Tindakan Cepat (sudah/sedang dilakukan)
- Membatalkan 25 paket yang belum diambil kurir
- Menghubungi 15 pelanggan yang paketnya sudah terlanjur jalan untuk koordinasi ulang alamat/pengambilan
- Membalas 5 komplain yang sudah masuk dengan permintaan maaf dan solusi (lihat draf di bawah)

## Rencana Pencegahan
| Tindakan | Penanggung jawab | Tenggat |
|---|---|---|
| Tambahkan langkah "cek ulang data alamat dari sistem pesanan terbaru, bukan sheet manual" di SOP packing | Supervisor Gudang | [isi: tenggat] |
| Matikan akses ke sheet alamat lama / arsipkan agar tidak terpakai lagi | Admin | [isi: tenggat] |
| Sediakan checklist cetak label khusus periode promo (verifikasi jumlah & sampel cek 1 dari 10 label) | Supervisor Gudang | [isi: tenggat] |

## Draf Permintaan Maaf ke Pelanggan

**Versi lengkap (email/DM):**

Halo Kak [Nama],

Mohon maaf, pesanan Kakak dari Kedai Rempah Bu Sri terkirim dengan alamat yang tidak sesuai akibat kesalahan pada data pengiriman kami saat periode promo kemarin. Kami memahami ini merepotkan dan kami sedang membenahi proses verifikasi alamat sebelum pengiriman agar hal ini tidak terulang.

Untuk pesanan Kakak, kami akan [isi: langkah konkret — kirim ulang / bantu koordinasi pengambilan / kompensasi jika ada]. Silakan balas pesan ini atau hubungi kami di [isi: kontak] agar bisa segera kami bantu.

Terima kasih atas pengertiannya.
Kedai Rempah Bu Sri

**Versi pendek (broadcast/status WA):**

Mohon maaf ke pelanggan yang pesanannya salah alamat pada promo 9.9 kemarin. Kami sedang menghubungi satu per satu untuk membantu penyelesaiannya. Terima kasih atas kesabarannya 🙏 — Kedai Rempah Bu Sri

## Ringkasan untuk Tim/Pemilik (WA)

*Insiden: Salah Kirim Massal Promo 9.9*
Apa: 40 pesanan salah label alamat, data dari sheet lama
Dampak: ±Rp1,5jt ongkir kirim ulang, 5 komplain masuk
Status: 25 paket dibatalkan, 15 masih ditangani
Pencegahan: SOP cek ulang alamat sebelum cetak label — PJ: Supervisor Gudang, tenggat [isi]
