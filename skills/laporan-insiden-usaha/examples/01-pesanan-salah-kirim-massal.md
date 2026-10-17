# Contoh 1 — Pesanan Salah Kirim Massal

## Input pengguna
> "Buatin laporan insiden. Kemarin pas promo 9.9, 40 pesanan label alamatnya kesalahan gara-gara admin salin data dari sheet lama. Ketahuan jam 14.00 pas ada komplain masuk 5 pelanggan, packing mulai jam 09.00. Kita udah hubungin kurir buat batalin 25 paket yang belum diambil, 15 sisanya udah terlanjur jalan. Kerugian ongkir kirim ulang sekitar Rp1.500.000. Toko namanya Kedai Rempah Bu Sri."

## Output skill

# Laporan Insiden: Pesanan Salah Kirim Massal Saat Promo 9.9

**Tanggal kejadian:** 9 September 2026 · **Ketahuan:** 14.00 · **Status:** Sebagian ditangani, sisanya masih berjalan

## Kronologi
09.00 — Tim packing mulai mencetak label pengiriman untuk pesanan promo 9.9.
14.00 — Komplain masuk dari 5 pelanggan yang menerima paket dengan alamat tidak sesuai.
[isian: jam] — Dicek, ditemukan 40 pesanan memakai label dengan alamat salah karena data disalin dari sheet alamat versi lama.
[isian: jam] — Tim menghubungi kurir: 25 paket berhasil dibatalkan sebelum diambil kurir, 15 paket lainnya sudah terlanjur dikirim.

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
- [isian: tindakan yang sudah Anda lakukan, selain membatalkan 25 paket]

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
Status: 25 paket dibatalkan, 15 sudah terlanjur jalan
Pencegahan: SOP cek ulang alamat sebelum cetak label — PJ: Supervisor Gudang, tenggat [isi]

## Penyegaran v1.0.5 (2026-10-17)
> Output di atas adalah contoh pembuat sebelum v1.0.5 (terakhir disunting v1.0.3) dan **tidak diubah**. Di bawah ini bagian-bagian yang kini ditulis berbeda menurut SKILL.md v1.0.5. Bagian lain (Rencana Pencegahan, draf maaf versi lengkap) tetap sama polanya. Ini penyegaran dokumentasi, bukan uji ulang.

Yang berubah: (1) tindakan dipisah **Sudah dilakukan** (hanya yang disebut pengguna) dan **Disarankan (belum dilakukan)**; hasil yang belum dikonfirmasi tidak ditulis sebagai hasil ("25 paket berhasil dibatalkan" di atas tidak didukung pesan pengguna); (2) langkah "kenapa" yang tidak disebut pengguna bertanda `(dugaan, perlu dikonfirmasi)` dan akar masalah ditulis sebagai dugaan + pertanyaan konfirmasi; (3) 35 pelanggan yang belum komplain dihubungi proaktif; (4) draf pendek lewat chat per pesanan, bukan broadcast/status WA; (5) angka dicek konsisten di semua bagian.

**Status:** Masih ditangani

**Kronologi (baris yang berubah)**
[isi: jam] — Pemilik/tim menghubungi kurir untuk membatalkan 25 paket yang belum diambil; 15 paket sudah terlanjur jalan. Hasil pembatalan: [isi: berapa yang dikonfirmasi berhasil dibatalkan kurir].

**Dampak**
- Pesanan dengan label alamat salah: 40 pesanan (25 diminta dibatalkan + 15 terlanjur jalan)
- Sudah komplain: 5 pelanggan
- Belum komplain, perlu dihubungi proaktif: 35 pesanan (asumsi 1 pesanan = 1 pembeli)
- Kerugian: sekitar Rp1.500.000 (ongkir kirim ulang)

**Akar Masalah (5 Kenapa)**
1. Kenapa 40 pesanan salah alamat? → Label dicetak dari data yang disalin admin dari sheet lama (sesuai keterangan Anda).
2. Kenapa admin memakai sheet lama? → (dugaan, perlu dikonfirmasi) sheet lama dan sheet terbaru sama-sama tersedia, tanpa penanda mana yang berlaku.
3. Kenapa tidak ketahuan sebelum dicetak? → (dugaan, perlu dikonfirmasi) tidak ada langkah cek ulang alamat sebelum cetak label saat volume promo tinggi.
4. Kenapa langkah cek ulang itu tidak ada? → (dugaan, perlu dikonfirmasi) SOP packing belum disesuaikan untuk periode promo.

**Dugaan akar masalah (belum dikonfirmasi pemilik):** SOP packing belum mengatur sumber data alamat yang berlaku dan langkah cek ulang sebelum cetak label massal.
Mohon konfirmasi: Benar ada lebih dari satu sheet alamat yang dipakai bergantian? Apakah SOP packing sudah punya langkah cek alamat sebelum cetak?

**Tindakan Cepat**
Sudah dilakukan (sesuai keterangan Anda):
- Menghubungi kurir untuk membatalkan 25 paket yang belum diambil; hasil pembatalan: [isi: berapa yang dikonfirmasi berhasil dibatalkan].

Disarankan (belum dilakukan):
- Balas 5 pelanggan yang sudah komplain lewat chat pesanannya masing-masing.
- Hubungi proaktif 35 pembeli lain yang pesanannya ikut terdampak, sebelum mereka komplain.
- Lacak 15 paket yang terlanjur jalan bersama kurir: status sekarang belum ada kabar.

**Draf pendek (chat marketplace/WA per pesanan, untuk 35 pembeli yang belum komplain):**
Halo Kak [Nama], kami dari Kedai Rempah Bu Sri. Mohon maaf, label alamat pesanan Kakak pada promo 9.9 ternyata salah cetak. Kami sedang mengurusnya dengan kurir dan akan [isi: langkah untuk pesanan Kakak — kirim ulang/ganti]. Boleh konfirmasi alamat lengkap Kakak? 🙏

**Ringkasan untuk Tim/Pemilik (WA)**
*Insiden: Salah Label Alamat 40 Pesanan Promo 9.9*
Apa: 40 pesanan memakai label dari sheet alamat lama
Dampak: 5 pelanggan komplain, 35 belum komplain; ±Rp1,5 jt ongkir kirim ulang
Status: kurir sudah dihubungi untuk membatalkan 25 paket, hasilnya belum ada kabar; 15 paket terlanjur jalan
Pencegahan: cek ulang alamat sebelum cetak label — PJ: [isi: jabatan], tenggat [isi: tanggal]

Cek angka (Decimal, 2026-10-17): 25 + 15 = 40; 40 − 5 = 35; dipakai sama di Dampak, Tindakan, draf, dan ringkasan.

Rujukan bot Telegram asli (skenario yang sama, v1.0.5): `koordinasi/telegram-gelombang-A1-2026-10-17.md` — topik 1884/1885, TANPA 6,0 → DENGAN 8,5 (+2,5) **LULUS**; 35 pelanggan proaktif dan tanda dugaan muncul. Sisa temuan di sana: ringkasan WA bot menulis "25 paket berhasil dihentikan" (tidak konsisten dengan bagian Tindakan), dan ada satu frasa rusak.
