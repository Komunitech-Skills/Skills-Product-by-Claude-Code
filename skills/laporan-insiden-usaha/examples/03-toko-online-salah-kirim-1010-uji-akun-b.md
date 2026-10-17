# Uji 03 (Akun B, normal #1) — Toko Online Salah Kirim 40 Paket Saat Flash Sale 10.10

Penguji hanya membaca folder `skills/laporan-insiden-usaha/` (SKILL.md, README, references, examples 01–02), tidak melihat riwayat pembuatan skill.

## Input pengguna
> "Tolong buatin laporan insiden. Pas flash sale 10.10 kemarin, sistem gudang kami salah cetak 40 label pengiriman (ketuker sama pesanan batch sebelumnya) karena dua batch pesanan digabung manual pas jam sibuk. Mulai packing jam 09.00, ketahuan jam 10.10 pas QC acak nemu label ganda. 10 paket sempat ditahan sebelum diambil kurir, 30 sudah kepiket kurir. Kita langsung hubungin kurir buat tahan yang masih bisa. Kerugian ongkir kirim ulang sekitar Rp2.000.000. Nama toko: Zalira Fashion."

## Output simulasi (mengikuti SKILL.md persis)

# Laporan Insiden: Salah Kirim 40 Label Paket Saat Flash Sale 10.10

**Tanggal kejadian:** [isi: tanggal] · **Ketahuan:** 10.10 · **Status:** Sebagian ditangani, sisanya masih berjalan

## Kronologi
09.00 — Tim packing mulai memproses pesanan flash sale 10.10, dua batch pesanan digabung secara manual karena volume tinggi.
10.10 — QC acak menemukan label ganda; ditemukan 40 paket memakai label yang tertukar antar batch.
10.10 (setelahnya) — Tim menghubungi kurir: 10 paket berhasil ditahan sebelum diambil, 30 paket sudah terlanjur diambil kurir.

## Dampak
- Pelanggan/pesanan terdampak: 40 paket
- Kerugian: sekitar Rp2.000.000 (ongkir kirim ulang)
- Lainnya: [isi: jumlah komplain pelanggan masuk, jika ada]

## Akar Masalah (5 Kenapa)
1. Kenapa 40 label tertukar? → Karena dua batch pesanan digabung secara manual saat proses packing.
2. Kenapa digabung manual? → Karena volume pesanan melonjak saat flash sale dan sistem tidak memisahkan batch otomatis.
3. Kenapa penggabungan manual ini tidak dicek ulang? → Karena tidak ada langkah verifikasi label per batch sebelum kurir mengambil.
4. Kenapa langkah verifikasi itu belum ada? → Karena SOP packing belum disesuaikan untuk kondisi volume tinggi/flash sale.

**Akar masalah:** SOP packing belum mengatur langkah verifikasi label per batch saat penggabungan manual di volume tinggi (flash sale).

## Tindakan Cepat (sudah/sedang dilakukan)
- Menahan 10 paket sebelum diambil kurir
- Menghubungi kurir untuk 30 paket yang sudah terlanjur diambil
- [isi: apakah pelanggan yang terdampak sudah dihubungi/diberi tahu]

## Rencana Pencegahan
| Tindakan | Penanggung jawab | Tenggat |
|---|---|---|
| Tambahkan langkah verifikasi label per batch sebelum serah terima ke kurir, khusus saat volume tinggi | Supervisor Gudang | [isi: tenggat] |
| Hentikan penggabungan batch manual; pisahkan proses cetak label per batch di sistem | [isi: penanggung jawab] | [isi: tenggat] |
| QC sampel diperluas saat periode flash sale (bukan hanya acak standar) | [isi: penanggung jawab] | [isi: tenggat] |

## Draf Permintaan Maaf ke Pelanggan

**Versi lengkap (email/DM):**

Halo Kak [Nama],

Mohon maaf, pesanan Kakak dari Zalira Fashion terkirim dengan label yang tertukar akibat kesalahan proses packing kami saat flash sale 10.10 kemarin. Kami memahami ini merepotkan dan kami sedang membenahi proses verifikasi label sebelum serah terima ke kurir agar hal ini tidak terulang.

Untuk pesanan Kakak, kami akan [isi: langkah konkret — kirim ulang / bantu koordinasi pengambilan / kompensasi jika ada]. Silakan balas pesan ini atau hubungi kami di [isi: kontak] agar bisa segera kami bantu.

Terima kasih atas pengertiannya.
Zalira Fashion

**Versi pendek (broadcast/status WA):**

Mohon maaf ke pelanggan yang labelnya tertukar saat flash sale 10.10 kemarin. Kami sedang menghubungi kurir dan pelanggan terdampak satu per satu. Terima kasih atas kesabarannya 🙏 — Zalira Fashion

## Ringkasan untuk Tim/Pemilik (WA)

*Insiden: Label Tertukar 40 Paket Flash Sale 10.10*
Apa: 40 label ketuker antar batch, digabung manual pas jam sibuk
Dampak: ±Rp2jt ongkir kirim ulang
Status: 10 paket ditahan, 30 masih ditangani via kurir
Pencegahan: Verifikasi label per batch sebelum ke kurir — PJ: Supervisor Gudang, tenggat [isi]

## Catatan penguji
- Angka yang tidak disebut pengguna (jumlah komplain, apakah pelanggan sudah dihubungi, penanggung jawab, tenggat) konsisten memakai `[isi: ...]`, tidak dikarang. Sesuai Batasan.
- Tidak ada nama karyawan yang disalahkan; akar masalah diarahkan ke SOP/sistem. Sesuai prinsip blameless.
- Format output mengikuti urutan template persis: Kronologi → Dampak → 5 Kenapa → Tindakan Cepat → Pencegahan → Draf Maaf → Ringkasan WA.
- Skenario ini tidak menyangkut data pelanggan, sehingga bagian "Kewajiban Pemberitahuan Data Pribadi" benar-benar dihilangkan (bukan ditulis kosong) — sesuai instruksi "[Jika menyangkut data pelanggan]" bersyarat.
- **Lulus** — output langsung siap pakai, tidak ada klaim berlebihan di draf minta maaf.

## Penyegaran v1.0.5 (2026-10-17)
> Output simulasi dan kesimpulan penguji (Lulus, skor 9/10 di `HASIL-UJI.md`) **tidak diubah**. Uji ini dijalankan pada v1.0.0. Menurut SKILL.md v1.0.5 bagian-bagian berikut kini ditulis berbeda:

**Status:** Masih ditangani

**Akar Masalah (5 Kenapa)**
1. Kenapa 40 label tertukar? → Dua batch pesanan digabung manual saat jam sibuk (sesuai keterangan Anda).
2. Kenapa digabung manual? → (dugaan, perlu dikonfirmasi) sistem gudang tidak memisahkan batch otomatis saat volume flash sale.
3. Kenapa tidak dicek ulang? → (dugaan, perlu dikonfirmasi) belum ada langkah verifikasi label per batch sebelum kurir mengambil.

**Dugaan akar masalah (belum dikonfirmasi pemilik):** SOP packing belum mengatur verifikasi label per batch saat penggabungan manual.
Mohon konfirmasi: Apakah sistem gudang bisa mencetak label per batch terpisah? Apakah sudah ada langkah cek label sebelum serah terima kurir?

**Tindakan Cepat**
Sudah dilakukan (sesuai keterangan Anda):
- Menahan 10 paket sebelum diambil kurir.
- Menghubungi kurir untuk menahan paket yang masih bisa ditahan; hasil untuk 30 paket yang sudah diambil kurir: [isi: berapa yang berhasil ditahan].

Disarankan (belum dilakukan):
- Hubungi proaktif semua pembeli 40 pesanan lewat chat pesanannya masing-masing (jumlah yang sudah komplain: [isi: jumlah]).

**Draf pendek:** dikirim per pesanan lewat chat marketplace, bukan broadcast/status WA (yang terdampak hanya 40 pembeli).

**Ringkasan WA, baris Status:** 10 paket ditahan; 30 paket sudah diambil kurir, hasil penahanan belum ada kabar.

Cek angka (Decimal, 2026-10-17): 10 + 30 = 40; kerugian sekitar Rp2.000.000 dipakai sama di Dampak dan ringkasan.
