# Contoh 1: pemilik usaha tas kanvas, 10 email campur

> Contoh rancangan pembuat dengan email fiktif; bukan hasil uji platform. Hari ini Selasa, 2026-10-06.

## Masukan pengguna
"Ini 10 email pagi ini. Mana yang duluan dibalas? Siapkan balasannya." (isi email: `data/pemilik-usaha-10-email.csv`)

## Keluaran di chat

**Waspada dulu (2 email dicurigai phishing, jangan dibalas atau diklik)**
- **E2 "Layanan BCA"**: nama pengirim menyebut bank, tetapi alamatnya dari situs lain berakhiran `.top`; tautannya dipendekkan sehingga tujuan aslinya tidak terlihat; meminta PIN dan OTP dengan ancaman akun diblokir hari ini. Bank resmi tidak meminta PIN/OTP lewat email. Laporkan sebagai phishing di aplikasi email dan hapus.
- **E7 "Mas Agus", rekening baru**: isinya meminta transfer ke rekening baru dan menyebut rekening lama ditutup, dengan tekanan "segera". Ini modus umum penipuan tagihan. Domainnya sama dengan vendor Anda di E3, tetapi akun bisa saja diretas atau dipalsukan. Jangan transfer; telepon Mas Agus ke nomor yang sudah Anda simpan dan tanyakan dulu.

**Ringkasan:** 10 email: 2 dicurigai phishing, 3 perlu tindakan hari ini atau besok (P1), 2 perlu balasan (P2-P3), 3 cukup diarsipkan.

| Urut. | Email | Prioritas dan alasan | Ringkasan dan tindakan |
|---|---|---|---|
| 1 | E3 Pak Hendra, tagihan | P1: jatuh tempo 8 Okt (2 hari), Rp7.450.000 | Menagih INV-0417. Cocokkan dengan catatan, konfirmasi atau bayar sebelum 8 Okt (tenggat dari email) |
| 2 | E6 Dina Lestari, komplain | P1: pesanan 6 hari belum sampai, mengancam refund | Cek resi hari ini, kabari Dina siang ini (saran) |
| 3 | E1 Bu Ratna, penawaran | P2: calon klien, acara 20 Okt, anggaran Rp18.000.000 | Minta harga dan jadwal kirim 200 tas kanvas. Kirim penawaran besok (saran) |
| 4 | E9 Pak Joko, jadwal | P3: tanpa tenggat tegas | Mengusulkan bertemu Jumat 9 Okt pukul 10.00 soal kontrak. Konfirmasi hari ini atau besok |

**Draf balasan**

E3 (Pak Hendra)
> Subjek: Re: Tagihan INV-0417 jatuh tempo
> Selamat siang Pak Hendra, terima kasih atas tagihannya. Kami catat invoice INV-0417 sebesar Rp7.450.000, jatuh tempo 8 Oktober 2026. Pembayaran kami jadwalkan [isian: tanggal bayar]; bukti transfer kami kirim setelahnya. Hormat saya, [isian: nama]

E6 (Dina Lestari)
> Subjek: Re: Komplain pesanan
> Halo Kak Dina, mohon maaf pesanannya belum sampai dan pasti membuat khawatir. Kami cek ke kurir hari ini dan kabari Kakak sebelum [isian: jam]. Boleh kirim nomor pesanan atau tangkapan layar resinya? Soal refund, [KEPUTUSAN PENGGUNA]. Terima kasih sudah sabar.

E1 (Bu Ratna)
> Subjek: Re: Penawaran 200 pcs tas kanvas
> Selamat siang Bu Ratna, terima kasih sudah menghubungi kami. Untuk 200 pcs tas kanvas, harga satuan [isian: harga] dan estimasi kirim [isian: tanggal], supaya bisa tiba sebelum acara 20 Oktober. Mohon info warna, apakah memakai sablon, dan alamat tujuan. Kami tunggu kabarnya.

E9 (Pak Joko)
> Subjek: Re: Jadwal ketemu
> Selamat siang Pak Joko, Jumat 9 Oktober pukul 10.00 [isian: setuju / usul waktu lain]. Mohon info lokasinya. Terima kasih.

E7 (verifikasi, bukan setuju)
> Subjek: Re: Rekening baru
> Mas Agus, terima kasih infonya. Sesuai prosedur kami, perubahan rekening kami konfirmasi lewat telepon ke nomor yang sudah kami simpan. Kami hubungi Mas hari ini sebelum memproses pembayaran berikutnya.

**Arsipkan:** E4 (laporan penjualan, 12 pesanan baru), E10 (stok tas kanvas tersisa 14 pcs; catat karena E1 butuh 200 pcs, perlu produksi tambahan), E5 dan E8 (promosi).

**Pola:** pesan E1 butuh 200 pcs sedangkan stok 14, jadi harga dan jadwal kirim sebaiknya dipastikan ke produksi dulu.

**Asumsi:** hari ini 6 Okt 2026; "nominal besar" Rp10.000.000; balasan formal. Boleh saya tahu: (1) harga satuan dan tanggal kirim untuk E1? (2) kebijakan refund toko untuk E6? (3) sudah ada konfirmasi ke Mas Agus lewat telepon?
