# Kerangka & bank kalimat SPH

## Penomoran surat
Pola umum: `<nomor urut 3 digit>/<kode surat>/<kode usaha>/<bulan romawi>/<tahun>` → `012/SPH/MKS/IX/2026`.
Script membuatnya otomatis dengan `--nomor-urut 12 --kode "SPH/MKS"`. Jika usaha sudah punya pola sendiri, ikuti pola pengguna.

## Kalimat pembuka (pilih sesuai konteks)
- **Menjawab permintaan:** "Menindaklanjuti permintaan Bapak/Ibu melalui WhatsApp pada [tanggal], bersama ini kami sampaikan penawaran harga [barang/jasa] sebagai berikut:"
- **Setelah pertemuan/survei:** "Terima kasih atas waktu yang diberikan pada pertemuan/survei lokasi tanggal [tanggal]. Berdasarkan kebutuhan yang telah dibahas, kami sampaikan penawaran harga sebagai berikut:"
- **Penawaran proaktif:** "Perkenalkan, kami [nama usaha], [deskripsi singkat 1 kalimat]. Bersama ini kami sampaikan penawaran harga [produk] yang dapat mendukung kebutuhan [perusahaan/instansi] Bapak/Ibu:"
- **Revisi:** "Menindaklanjuti masukan Bapak/Ibu atas penawaran kami nomor [nomor lama], berikut kami sampaikan penawaran harga revisi:"
  (Pakai nomor surat baru atau tambahkan `-R1`; sebutkan bahwa penawaran sebelumnya tidak berlaku.)

## Syarat & ketentuan — pilihan kalimat
**Pembayaran**
- "Pembayaran DP 50% saat Purchase Order (PO) diterima, pelunasan 50% sebelum barang dikirim."
- "Pembayaran penuh paling lambat [N] hari setelah invoice diterima (tempo [N] hari)." — untuk pelanggan korporat langganan.
- "Pembayaran 100% di muka." — untuk pesanan custom/kecil.
- Selalu cantumkan rekening atas nama usaha; jangan mengarang nomor rekening.

**Pengiriman**
- "Barang dikirim [N] hari kerja setelah DP diterima."
- "Harga franco [kota/alamat pembeli]" (ongkir sudah termasuk) atau "Harga loco gudang [kota]" (belum termasuk ongkir).
- Jasa: "Pekerjaan dimulai [N] hari setelah PO dan selesai dalam [N] hari kerja."

**Lain-lain (hanya jika diberikan pengguna)**
- Garansi: "[N] bulan untuk cacat produksi, tidak termasuk kerusakan karena pemakaian."
- Harga dapat berubah jika jumlah/spesifikasi berubah.
- Penawaran tidak mengikat sebelum PO/konfirmasi tertulis.

## Kalimat penutup
- "Demikian penawaran ini kami sampaikan. Besar harapan kami dapat bekerja sama dengan [nama perusahaan]. Untuk konfirmasi pesanan atau pertanyaan, Bapak/Ibu dapat menghubungi [nama] di [WA]."

## Nada per jenis pembeli
| Pembeli | Nada | Catatan |
|---|---|---|
| Instansi pemerintah/BUMN | Sangat formal, "Yth.", "dengan hormat" | Cantumkan NPWP bila ada; rujuk nomor surat permintaan mereka |
| Perusahaan swasta | Formal-ringkas | Fokus total, masa berlaku, termin |
| EO/UKM/perorangan | Semi-formal | Teks WA lebih penting dari PDF |
| Sekolah/yayasan | Formal-hangat | Sebutkan kepala sekolah/bendahara sebagai penerima |

## Contoh kasus lokal lain
1. **Katering kantor (bukan PKP):** "Dapur Bu Sri, Bekasi" menawarkan 150 nasi box ayam bakar @35rb + 150 air mineral @4rb ke panitia seminar, diskon 5%. Total Rp 5.557.500, tanpa PPN.
2. **Toko bangunan (PKP):** "TB Sumber Rejeki, Sidoarjo" menawarkan 100 sak semen @72.500 + 50 batang besi 10mm @98.000 diskon 2% ke kontraktor. Subtotal Rp 12.052.000, PPN Rp 1.325.720, total Rp 13.377.720.
3. **Jasa (harga sudah termasuk PPN):** konsultan IT PKP menawarkan paket Rp 11.100.000 termasuk PPN → DPP Rp 10.000.000, PPN Rp 1.100.000.
