# 06 - Skenario normal 1: toko hijab online di Shopee + WhatsApp (usaha FIKTIF)

> Uji independen Tahap 6 (2026-09-30), dijalankan dari salinan skill di scratchpad. Penguji bertindak sebagai agent yang memakai skill. Semua angka rupiah berasal dari `scripts/hitung_referral.py` (keluaran di bawah) dan sudah diverifikasi ulang secara independen (lihat `HASIL-UJI.md`).

**Permintaan pengguna:** "Saya jualan hijab di Shopee sama WA, namanya Kerudung Nara. Rata-rata sekali belanja Rp145.000, untung kotor 38%. Mau bikin program ajak teman: teman dapat diskon 10%, yang ngajak dapat Rp20.000. Kartu ajakan di paket modalnya Rp1.500. Pelanggan sekitar 850, biasanya beli lagi tiap 2 bulan. Iklan sekarang Rp55.000 per pembeli baru, anggaran hadiah maks Rp750.000 sebulan. Aman nggak? Kalau dinaikin jadi Rp50.000 + 20% gimana?"

## Perhitungan (script)
```
$ python3 scripts/hitung_referral.py biaya --aov 145rb --margin 38 --hadiah-pemberi 20rb --hadiah-teman 10% --biaya-lain 1.500 --anggaran 750rb --cac-iklan 55rb
BIAYA PER REFERRAL BERHASIL (dibayar hanya bila teman benar-benar membeli)
Nilai pesanan pertama rata-rata : Rp145.000  |  margin kotor 38%
Laba kotor pesanan pertama      : Rp55.100 (sebelum hadiah)
Hadiah pemberi (perujuk)        : Rp20.000
Hadiah/diskon teman             : Rp14.500
Biaya lain per referral         : Rp1.500
BIAYA PER REFERRAL              : Rp36.000 = 24,83% dari nilai pesanan, 65,34% dari laba kotor
Laba pesanan pertama setelah hadiah: Rp19.100
Anggaran Rp750.000 cukup untuk maksimal 20 referral berhasil.
Pembanding: biaya per pelanggan baru dari iklan Rp55.000 -> referral LEBIH MURAH (selisih Rp19.000).
Hadiah berupa produk sendiri: isi dengan modal (HPP) produk, bukan harga jual.
(kode keluar 0)

$ python3 scripts/hitung_referral.py impas --aov 145rb --margin 38 --hadiah-pemberi 20rb --hadiah-teman 10% --biaya-lain 1.500 --frekuensi-bulan 0,5 --umur-bulan 12
TITIK IMPAS HADIAH REFERRAL
Laba kotor per pesanan          : Rp55.100 (nilai pesanan Rp145.000, margin 38%)
Biaya per referral              : Rp36.000 (pemberi Rp20.000 + teman Rp14.500 + lain Rp1.500)
Balik modal setelah             : pesanan ke-1 milik teman (langsung di pesanan pertama)
Hadiah maks agar impas di pesanan pertama: Rp55.100 (total pemberi + teman + lain)
Perkiraan laba kotor seumur pelanggan: Rp330.600 (6 pesanan; asumsi 0,5x per bulan selama 12 bulan)
Batas hadiah aman (30% dari laba seumur pelanggan): Rp99.180 total per referral
Hadiah pemberi maksimal (bila hadiah teman & biaya lain tetap): Rp83.180
STATUS: AMAN
Asumsi frekuensi, umur pelanggan, dan porsi 30% adalah aturan praktis/perkiraan, bukan kepastian; cek dengan data penjualan Anda.
(kode keluar 0)

$ python3 scripts/hitung_referral.py biaya --aov 145rb --margin 38 --hadiah-pemberi 50rb --hadiah-teman 20%
BIAYA PER REFERRAL BERHASIL (dibayar hanya bila teman benar-benar membeli)
Nilai pesanan pertama rata-rata : Rp145.000  |  margin kotor 38%
Laba kotor pesanan pertama      : Rp55.100 (sebelum hadiah)
Hadiah pemberi (perujuk)        : Rp50.000
Hadiah/diskon teman             : Rp29.000
Biaya lain per referral         : Rp0
BIAYA PER REFERRAL              : Rp79.000 = 54,48% dari nilai pesanan, 143,38% dari laba kotor
Laba pesanan pertama setelah hadiah: -Rp23.900
PERHATIAN: hadiah lebih besar dari laba kotor pesanan pertama (rugi Rp23.900 per referral). Balik modal hanya bila teman membeli lagi, minimal 1 pesanan ulang.
Hadiah berupa produk sendiri: isi dengan modal (HPP) produk, bukan harga jual.
(kode keluar 0)

$ python3 scripts/hitung_referral.py simulasi --pelanggan-aktif 850 --aov 145rb --margin 38 --hadiah-pemberi 20rb --hadiah-teman 10% --biaya-lain 1.500 --pesanan-ulang 1 --anggaran 750rb --cac-iklan 55rb
SIMULASI REFERRAL (ESTIMASI, bukan kepastian) - 850 pelanggan aktif
Biaya per referral berhasil Rp36.000; laba kotor per pesanan Rp55.100; pesanan ulang per teman baru: 1
- konservatif: 43 perujuk -> 43 teman diajak -> 9 pembeli baru | omzet Rp2.610.000 | biaya hadiah Rp324.000 | laba kotor Rp991.800 | laba setelah hadiah Rp667.800 | ROI 206,11%
- realistis: 85 perujuk -> 170 teman diajak -> 43 pembeli baru | omzet Rp12.470.000 | biaya hadiah Rp1.548.000 | laba kotor Rp4.738.600 | laba setelah hadiah Rp3.190.600 | ROI 206,11%
  PERHATIAN: biaya Rp1.548.000 melebihi anggaran Rp750.000; pasang batas kuota hadiah.
- optimis: 128 perujuk -> 256 teman diajak -> 77 pembeli baru | omzet Rp22.330.000 | biaya hadiah Rp2.772.000 | laba kotor Rp8.485.400 | laba setelah hadiah Rp5.713.400 | ROI 206,11%
  PERHATIAN: biaya Rp2.772.000 melebihi anggaran Rp750.000; pasang batas kuota hadiah.
Pembanding iklan: Rp55.000 per pelanggan baru -> referral lebih murah (Rp36.000 per pembeli baru).
Angka skenario adalah asumsi awal, bukan patokan pasar; ganti dengan data Anda setelah 1 bulan berjalan.
(kode keluar 0)

```

## Jawaban skill

### 1. Ringkasan
- **Program:** referral dua sisi. Teman baru dapat **potongan 10% (rata-rata Rp14.500)** di pesanan pertama; pengajak dapat **voucher Rp20.000** setelah pesanan teman selesai dan lewat masa retur.
- **Aman.** Biaya per referral **Rp36.000** (24,83% dari pesanan, 65,34% dari laba kotor); laba pesanan pertama tetap **Rp19.100**, balik modal langsung di pesanan pertama. Lebih murah dari iklan (Rp55.000), selisih Rp19.000.
- **Usulan Rp50.000 + 20% tidak disarankan untuk program rutin:** biaya Rp79.000, **rugi Rp23.900 per referral** di pesanan pertama; hanya balik modal bila teman membeli lagi.

### 2. Asumsi
Margin 38% dan biaya iklan dari Anda. Beli ulang 0,5x per bulan (tiap 2 bulan) selama 12 bulan: asumsi. Batas aman 30% dari laba seumur pelanggan = aturan praktis, bukan hukum.

### 3. Tabel angka (dari script)
| Hal | Nilai |
|---|---|
| Laba kotor per pesanan | Rp55.100 |
| Biaya per referral (Rp20.000 + Rp14.500 + kartu Rp1.500) | Rp36.000 |
| Laba pesanan pertama setelah hadiah | Rp19.100 |
| Batas hadiah aman per referral | Rp99.180 (STATUS: AMAN) |
| Kuota dengan anggaran Rp750.000 | maksimal 20 referral berhasil per bulan |
| Opsi Rp50.000 + 20% | biaya Rp79.000; laba pesanan pertama -Rp23.900 (PERHATIAN) |

### 4. Aturan program
- Teman = nomor/akun Shopee yang **belum pernah** beli di Kerudung Nara. Nomor, alamat kirim, atau nama penerima yang sama dengan pengajak = tidak sah.
- Voucher pengajak cair setelah pesanan teman **selesai + 7 hari tanpa retur**. Maks. 5 hadiah per pengajak per bulan, kuota 20 per bulan, voucher berlaku 30 hari, **tidak bisa diuangkan**.
- **Shopee:** ikuti aturan platform. Jangan menulis nomor WA di kartu dalam paket atau mengajak pembeli Shopee pindah transaksi ke WA. Untuk pembeli Shopee: kartu berisi ajakan "cari toko Kerudung Nara di Shopee, chat toko sebut nama pengajak" dan hadiah lewat **voucher toko Shopee** (bila fitur tersedia). Untuk pembeli WA: program penuh lewat WA.
- Data yang dicatat: nama panggilan, nomor WA/username, kode, tanggal, status hadiah (`templates/lembar-catatan-referral.csv`).

### 5. Syarat & ketentuan (siap tempel, dari `templates/syarat-ketentuan.md`)
1. Berlaku untuk pelanggan Kerudung Nara yang pernah belanja (Pengajak) dan teman yang belum pernah belanja (Teman Baru).
2. Teman Baru menghubungi kami (chat toko Shopee atau WA) dan menyebut nama/kode Pengajak **sebelum** memesan.
3. Teman Baru: potongan 10% untuk pesanan pertama. Pengajak: voucher Rp20.000 per Teman Baru yang pesanannya selesai.
4. Voucher Pengajak diberikan setelah pesanan Teman Baru selesai dan lewat 7 hari tanpa retur/pembatalan; berupa voucher belanja, bukan uang tunai.
5. Maksimal 5 hadiah per Pengajak per bulan; kuota 20 hadiah per bulan (bila habis, program dijeda sampai bulan berikutnya); voucher berlaku 30 hari.
6. Tidak berlaku bila nomor/alamat/akun sama, pesanan dibatalkan/diretur, atau ada indikasi akun ganda. Kami menjelaskan alasan bila hadiah ditolak.
7. Dilarang menyebarkan kode ke orang yang tidak dikenal, jual-beli kode, atau membuat akun palsu.
8. Data (nama panggilan, nomor WA/username, kode, tanggal, status hadiah) hanya untuk program ini, tidak dibagikan, dihapus 12 bulan setelah program selesai atau lebih cepat bila diminta. Balas "STOP" untuk berhenti menerima info.
9. Kerudung Nara dapat mengubah/menghentikan program dengan pemberitahuan di IG dan WA; hadiah yang sudah berhak tetap diberikan.

### 6. Teks ajakan (kirim satu per satu, bukan blast)
**WA ke pelanggan yang baru bilang puas:**
> Halo Kak Sari, makasih sudah belanja di Kerudung Nara. Senang pashmina-nya cocok ya. Kalau ada teman yang mungkin suka, boleh dibagikan: teman Kakak dapat potongan 10% di pesanan pertama, dan Kakak dapat voucher Rp20.000 setelah pesanannya selesai. Cukup minta temannya chat kami dan sebut nama Kakak. Syarat lengkap balas "S&K". Tidak mau dapat info seperti ini? Balas "STOP" ya.

**Teks siap diteruskan pelanggan ke temannya:**
> Aku langganan Kerudung Nara, bahannya adem. Kalau mau coba, chat tokonya dan sebut namaku (Sari), kamu dapat potongan 10% di pesanan pertama.

**Kartu di dalam paket (aman untuk Shopee):**
> Suka kerudungnya? Bagikan ke teman. Teman dapat potongan 10% pesanan pertama, kamu dapat voucher Rp20.000. Teman cukup chat toko Kerudung Nara dan sebut namamu. Syarat berlaku.

### 7. Simulasi (ESTIMASI, bukan kepastian)
Dengan 850 pelanggan dan 1 pesanan ulang per teman baru: konservatif 9 pembeli baru (laba setelah hadiah Rp667.800), realistis 43 (Rp3.190.600), optimis 77 (Rp5.713.400). Skenario realistis dan optimis **melebihi anggaran Rp750.000**, jadi kuota 20 hadiah per bulan wajib dipasang. Angka skenario adalah asumsi awal; ganti dengan data Anda setelah 1 bulan.

### 8. Langkah minggu ini
1. Pilih 15 pelanggan yang pernah memberi ulasan bintang 5; kirim teks WA satu per satu.
2. Cetak 100 kartu paket (modal Rp1.500/lembar sudah masuk hitungan).
3. Siapkan lembar catatan referral; tambahkan pertanyaan "Tahu kami dari mana?" di chat pertama.
4. Tempel S&K di highlight IG dan balasan cepat WA.
5. Minggu ke-4: hitung ulang biaya per referral dengan data nyata.

### 9. Catatan
Angka dihitung dengan script dari data yang Anda berikan. Keputusan besar hadiah tetap di tangan Anda. Promo harus jelas syaratnya (UU 8/1999 Perlindungan Konsumen); data pelanggan dicatat seminimal mungkin dan tidak dibagikan (UU 27/2022 PDP). Skill ini tidak berafiliasi dengan Shopee.

## Catatan penguji
- Semua angka cocok dengan hitungan independen. Langkah kerja 1-9 dan format output diikuti.
- Catatan kecil: `simulasi` menghitung omzet dari nilai pesanan penuh (Rp145.000) walau teman mendapat potongan 10% di pesanan pertama; laba sudah benar (diskon masuk biaya), hanya omzet sedikit lebih tinggi (Rp14.500 per pembeli baru).
