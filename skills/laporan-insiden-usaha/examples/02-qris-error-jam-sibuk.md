# Contoh 2 — Mesin Kasir/QRIS Error Saat Jam Sibuk

## Input pengguna
> "QRIS di toko error total dari jam 12 siang sampe jam 1, pas lagi rame jam makan siang. Kasir cuma bisa terima cash, ada sekitar 15 pelanggan yang batal beli karena cuma bawa uang digital. Internet toko emang sering putus-nyambung, cuma pake 1 provider. Ini toko roti "Roti Manis Ibu Nur", ga ada data pelanggan yang kebobol."

## Output skill

# Laporan Insiden: QRIS Error Saat Jam Makan Siang

**Tanggal kejadian:** [isi: tanggal] · **Ketahuan:** 12.00 · **Status:** Selesai (internet kembali jam 13.00)

## Kronologi
12.00 — QRIS mulai tidak bisa memproses pembayaran, bersamaan dengan jam makan siang yang ramai.
12.00–13.00 — Kasir hanya bisa menerima pembayaran tunai; sekitar 15 pelanggan membatalkan pembelian karena hanya membawa uang digital.
13.00 — Koneksi internet toko kembali normal, QRIS berfungsi lagi.

## Dampak
- Pelanggan terdampak: sekitar 15 pelanggan batal beli
- Kerugian: [isi: estimasi omzet hilang, jika ada]
- Lainnya: potensi kekecewaan pelanggan yang datang khusus jam makan siang

## Akar Masalah (5 Kenapa)
1. Kenapa QRIS error? → Karena koneksi internet toko terputus.
2. Kenapa koneksi terputus? → Karena internet toko sering putus-nyambung.
3. Kenapa hal ini bisa mengganggu operasional total? → Karena toko hanya mengandalkan satu provider internet tanpa cadangan.

**Akar masalah:** Tidak ada koneksi internet/pembayaran cadangan saat provider utama bermasalah, sehingga satu gangguan koneksi langsung menghentikan seluruh pembayaran non-tunai.

## Tindakan Cepat (sudah/sedang dilakukan)
- Mengarahkan pelanggan ke pembayaran tunai selama gangguan
- Menunggu koneksi internet pulih (kembali normal jam 13.00)

## Rencana Pencegahan
| Tindakan | Penanggung jawab | Tenggat |
|---|---|---|
| Siapkan internet cadangan (paket data/modem kedua) khusus untuk mesin QRIS | Pemilik/Supervisor | [isi: tenggat] |
| Siapkan QRIS statis cetak (dari bank/penyedia lain) sebagai cadangan manual saat sistem utama down | Kasir/Supervisor | [isi: tenggat] |
| Buat pengumuman singkat di kasir "sedang gangguan sistem, mohon bayar tunai" untuk dipasang saat kejadian serupa terjadi lagi | Kasir | [isi: tenggat] |

*(Kejadian ini tidak menyangkut data pelanggan — bagian kewajiban pemberitahuan data pribadi tidak berlaku.)*

## Draf Permintaan Maaf ke Pelanggan

**Versi lengkap (untuk dipasang di toko/medsos jika diperlukan):**

Halo Kak,

Mohon maaf atas gangguan pembayaran QRIS yang terjadi hari ini sekitar jam 12.00–13.00 di Roti Manis Ibu Nur. Gangguan ini disebabkan masalah koneksi internet toko dan sudah teratasi. Kami sedang menyiapkan sistem pembayaran cadangan agar gangguan seperti ini tidak mengganggu kenyamanan Kakak lagi.

Terima kasih atas pengertiannya, dan sampai jumpa di kunjungan berikutnya!
Roti Manis Ibu Nur

**Versi pendek (status WA/medsos):**

Mohon maaf atas gangguan QRIS tadi siang (12.00–13.00). Sudah normal kembali. Kami sedang siapkan sistem cadangan supaya lebih lancar ke depannya 🙏 — Roti Manis Ibu Nur

## Ringkasan untuk Tim/Pemilik (WA)

*Insiden: QRIS Error Jam Makan Siang*
Apa: QRIS down 1 jam (12.00–13.00) akibat internet putus, hanya 1 provider
Dampak: ±15 pelanggan batal beli
Status: Selesai, internet sudah normal
Pencegahan: Siapkan internet & QRIS cadangan — PJ: Pemilik/Supervisor, tenggat [isi]
