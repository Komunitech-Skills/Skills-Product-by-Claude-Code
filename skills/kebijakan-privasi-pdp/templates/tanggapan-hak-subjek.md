<!-- PANDUAN AGENT (hapus sebelum diserahkan)
- Template balasan untuk permintaan pelanggan atas data pribadinya. Bisa dikirim lewat WA atau email.
- Batas waktu yang disebut UU 27/2022: akses (Pasal 32), perbaikan/pembaruan (Pasal 30), penghentian karena
  penarikan persetujuan (Pasal 40) → paling lambat 3×24 jam sejak permintaan diterima. Untuk hak lain, tetap
  pakai 3×24 jam sebagai target aman dan beri kabar perkembangan bila perlu waktu lebih.
- Hitung tenggat: jam & tanggal permintaan diterima + 72 jam. Tulis tanggal-jamnya secara eksplisit di log.
- Verifikasi identitas secukupnya: cocokkan nomor WA/email yang terdaftar. Jangan minta foto KTP kalau tidak perlu.
- Data yang WAJIB disimpan (mis. catatan transaksi untuk pajak, rekam medis) boleh tidak dihapus — jelaskan
  alasannya, batasi pemakaiannya, dan hapus data lain yang tidak wajib.
-->

## 0. Log permintaan (untuk arsip usaha, bukan dikirim)
| No | Diterima (tgl & jam) | Nama / kontak | Jenis hak | Tenggat 3×24 jam | Tindakan | Selesai (tgl & jam) | Petugas |
|---|---|---|---|---|---|---|---|
| 1 | [isi] | [isi] | [akses/koreksi/hapus/tarik persetujuan/lainnya] | [isi] | [isi] | [isi] | [isi] |

## 1. Tanda terima (kirim segera)
> Halo [isi: nama], permintaan Anda untuk [isi: mengakses/memperbaiki/menghapus data / berhenti menerima promo] sudah kami terima pada [isi: tanggal, jam]. Kami akan menyelesaikannya paling lambat [isi: tanggal, jam = +3×24 jam]. Untuk memastikan ini benar Anda, mohon konfirmasi [isi: mis. nomor pesanan terakhir / email terdaftar]. Terima kasih.

## 2. Akses / salinan data
> Halo [isi: nama], berikut data pribadi Anda yang kami simpan:
> - Nama: [isi] · No. WA: [isi] · Email: [isi] · Alamat: [isi]
> - Riwayat pesanan: [isi: jumlah & periode]
> - Dipakai untuk: [isi: tujuan] · Dibagikan ke: [isi: kurir/payment gateway] · Disimpan sampai: [isi]
> Jika ada yang salah atau ingin dihapus, cukup balas pesan ini.

## 3. Perbaikan / pembaruan data
> Halo [isi: nama], data Anda sudah kami perbarui: [isi: data lama → data baru] pada [isi: tanggal, jam]. Perubahan juga kami teruskan ke [isi: pihak terkait, bila ada].

## 4. Penghapusan data
**Bila dapat dihapus seluruhnya:**
> Halo [isi: nama], data pribadi Anda ([isi: jenis data]) telah kami hapus dari [isi: daftar pelanggan, WA Business label/katalog, spreadsheet, CRM] pada [isi: tanggal]. Anda tidak akan lagi menerima pesan dari kami kecuali Anda menghubungi kami lagi.

**Bila sebagian wajib disimpan:**
> Halo [isi: nama], kami telah menghapus [isi: nomor WA dari daftar promo, alamat, riwayat chat]. Catatan transaksi (nama, tanggal, nominal) masih kami simpan karena wajib untuk pembukuan pajak selama [isi: 10 tahun menurut UU KUP Pasal 28 ayat (11)] dan hanya dipakai untuk keperluan itu. Setelah masa tersebut, data akan dimusnahkan.

## 5. Penarikan persetujuan (berhenti promo)
> Halo [isi: nama], mulai [isi: tanggal] Anda tidak akan menerima pesan promo dari kami lagi. Nomor Anda sudah kami keluarkan dari daftar promo. Pesan terkait pesanan yang masih berjalan tetap kami kirim.

## 6. Permintaan ditolak / tidak dapat dipenuhi
> Halo [isi: nama], mohon maaf, permintaan [isi] belum dapat kami penuhi karena [isi: alasan yang jujur — mis. identitas belum dapat diverifikasi / data wajib disimpan menurut aturan / permintaan menyangkut data orang lain]. Yang dapat kami lakukan: [isi: alternatif]. Jika ada pertanyaan, hubungi [isi: kontak].

*Catatan internal:* setelah menghapus data, cek juga tempat lain: kontak HP, label WA Business, grup, Google Sheets, marketplace chat, cadangan (backup), dan memori AI agent/asisten (bila ada).

## 7. English (optional)
> Hello [fill: name], we received your request to [fill: access/correct/delete your data / stop promotions] on [fill: date, time]. We will complete it by [fill: date, time + 72 hours]. To confirm it is you, please reply with [fill: last order number / registered email].
