---
name: program-referral-loyalitas
description: Merancang program referral ("ajak teman dapat hadiah"), poin/stempel loyalitas, dan member untuk UMKM Indonesia (toko online, kafe, jasa, reseller/dropship; klinik/praktik kesehatan hanya versi tanpa imbalan: edukasi & pengingat kontrol) lengkap dengan hitungan pasti - biaya per referral, titik impas hadiah dari margin, nilai poin dan liability poin, simulasi skenario - plus aturan anti-curang (akun ganda, self-referral), syarat dan ketentuan siap tempel, teks ajakan WhatsApp/Instagram siap kirim satu per satu (tanpa blast), dan kepatuhan (promo tidak menyesatkan, UU PDP). Gunakan saat pengguna bilang "bikin program referral", "ajak teman dapat diskon", "kartu member/poin/stempel", "pelanggan biar balik lagi", "hadiah aman berapa", "program reseller/komisi", "kode referral", atau referral program, loyalty program, points, retention, refer a friend, word of mouth.
---

# Program Referral & Loyalitas

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Membantu pemilik usaha membuat program **"pelanggan mengajak pelanggan"** dan **"pelanggan balik lagi"** yang benar-benar untung: jenis program yang cocok, besar hadiah yang **dihitung dari margin** (bukan dikira), aturan anti-curang, syarat & ketentuan, dan teks ajakan siap kirim. Hasil akhir: **satu paket program siap jalan + tabel angka + teks WA/IG + rencana uji 30 hari**.

## Kapan digunakan
- Ingin pelanggan lama membawa pelanggan baru (referral, kode teman, voucher "ajak teman").
- Ingin pelanggan lebih sering beli: poin, kartu stempel digital/kertas, tingkat member (Silver/Gold), voucher ulang tahun.
- Program komisi sederhana untuk reseller/dropshipper (satu tingkat, dari penjualan barang nyata).
- Mengecek program yang sudah ada: "hadiah saya kebesaran nggak?", "poin saya jadi utang berapa?".

## Kapan TIDAK digunakan (arahkan ke skill lain)
- Menghitung HPP/margin produk -> **hitung-hpp**; harga dan promo diskon umum -> **strategi-harga-produk**, **promo-kalender**.
- Rencana marketing menyeluruh -> **rencana-marketing-usaha**; caption/konten -> **caption-sosmed-umkm**; pesan ke prospek -> **pesan-prospek-wa**; catatan kontak pelanggan -> **crm-wa**; kebijakan privasi -> **kebijakan-privasi-pdp**.
- **Ditolak dengan sopan:** kirim pesan massal otomatis/blast ke daftar kontak (skill ini hanya menyiapkan teks yang dikirim pemilik satu per satu ke orang yang pernah berhubungan/setuju), hadiah untuk merekrut anggota bertingkat atau bayar-untuk-ikut (skema piramida/MLM), ulasan/like berbayar yang disamarkan, referral berimbalan/diskon/poin/komisi untuk **layanan kesehatan** (lihat "Fasilitas kesehatan" di bawah), membeli data kontak.

## Input
| Data | Wajib? | Jika tidak ada |
|---|---|---|
| Jenis usaha & produk/jasa utama | Ya | Tanyakan |
| Nilai pesanan rata-rata (AOV) | Ya untuk angka | Minta perkiraan, tandai "perkiraan" |
| Margin kotor % (atau modal/HPP) | Ya untuk angka | Sarankan **hitung-hpp**; bila cepat, pakai default: makanan/minuman 55%, fesyen/toko online 40%, jasa 50%, dan sebutkan asumsinya |
| Seberapa sering pelanggan beli (per bulan) & berapa lama bertahan | Tidak | Default 1x per bulan, 6 bulan (asumsi) |
| Kanal jual (WA, IG, marketplace, toko fisik) | Tidak | Anggap WhatsApp + toko sendiri |
| Anggaran hadiah per bulan | Tidak | Hitung batas aman saja |
| Biaya iklan per pelanggan baru sekarang (CAC) | Tidak | Lewati pembanding iklan |
| Ada catatan pelanggan? (bentuk, jumlah) | Tidak | Mulai dari buku catatan sederhana (`templates/lembar-catatan-referral.csv`) |

Jika data wajib kurang, tanyakan **sekali** dalam satu pesan (maks. 5 pertanyaan singkat). Jika pengguna ingin cepat, pakai default dan tulis asumsinya di bagian atas jawaban.

## Langkah kerja

> **Lokasi script:** semua script skill ini ada di subfolder `scripts/` di folder yang sama dengan SKILL.md ini (folder skill). Jalankan dari sana; jangan mencari script atau file pengguna ke seluruh disk (mis. `find /`) — itu lambat dan menyentuh data pribadi di luar folder kerja.

### 1. Pilih jenis program (lihat `references/pola-per-usaha.md`)
| Usaha | Pola utama | Alasan singkat |
|---|---|---|
| Toko online / fesyen | Referral dua sisi (voucher teman + saldo/voucher perujuk) | Beli tidak tiap minggu; rekomendasi teman berpengaruh |
| Kafe / warung / F&B | Poin atau stempel + "traktir teman" | Sering datang; hadiah murah karena margin besar |
| Klinik, praktik dokter/dokter gigi/bidan, apotek, lab (fasilitas kesehatan) | **Tanpa imbalan untuk merujuk:** edukasi, pengingat kontrol, kartu info | Permenkes 1787/2010 Pasal 5 & kode etik profesi melarang promosi penjualan/diskon/imbalan layanan kesehatan |
| Salon, spa, barbershop (bukan tindakan medis) | Referral + paket langganan (pola jasa) | Bukan fasilitas kesehatan; tetap tanpa klaim kesehatan |
| Jasa (laundry, bengkel, salon, servis) | Referral + paket langganan | Kepercayaan tinggi, frekuensi sedang |
| Reseller / dropship | Komisi satu tingkat dari penjualan nyata | Bukan rekrutmen bertingkat |
Boleh gabungan (mis. poin + referral). Satu program sederhana yang dijalankan lebih baik daripada tiga yang rumit.

### 2. Tentukan momen ajakan
Minta rekomendasi **saat pelanggan sedang puas**: barang baru diterima dan cocok, ulasan bagus, kopi ke-5, setelah masalah teratasi cepat, hasil perawatan terlihat. Bukan saat pelanggan baru komplain. Satu ajakan lembut, bukan pengingat tiap hari.

### 3. Hitung dengan script (WAJIB untuk setiap angka uang)
```
python3 <folder-skill-ini>/scripts/hitung_referral.py <perintah> [opsi]
```
Windows: ganti `python3` dengan `py` atau `python`. Uang boleh ditulis `60.000`, `Rp60.000`, `60rb`, `1,2jt`, `1.500.000`. Jumlah poin/orang/referral boleh ditulis `40.000`, `40000`, atau `40rb` (tanpa "Rp"). Desimal pakai **koma** (`0,25` kali per bulan, `12,5` persen). Persen ditulis angka biasa (`55` = 55%). Hadiah boleh rupiah (`15rb`) atau persen pesanan (`10%`). Angka yang bisa dibaca dua arah (mis. frekuensi `1.000`, jumlah `1,000`, rupiah `12,5`) ditolak `GAGAL`; tanyakan maksudnya ke pengguna, jangan menebak.

| Kebutuhan | Perintah |
|---|---|
| Biaya per referral & laba pesanan pertama | `biaya --aov 60rb --margin 55 --hadiah-pemberi 10rb --hadiah-teman 10% [--biaya-lain 2rb --jumlah-referral 20 --anggaran 500rb --cac-iklan 25rb]` |
| Titik impas & batas hadiah aman | `impas --aov 60rb --margin 55 --hadiah-pemberi 40rb --hadiah-teman 10% [--frekuensi-bulan 2 --umur-bulan 6 --porsi-ltv 30]` |
| Nilai poin & liability | `poin --belanja-per-poin 10rb --nilai-poin 250 --margin 40 [--aov 85rb --omzet-bulan 80jt --breakage 20 --poin-beredar 40000 --minimum-tukar 40]` |
| Simulasi skenario (ESTIMASI) | `simulasi --pelanggan-aktif 400 --aov 60rb --margin 55 --hadiah-pemberi 10rb --hadiah-teman 10% [--skenario nama:%merujuk:teman:%beli --pesanan-ulang 1 --anggaran 300rb --cac-iklan 25rb]` |

Aturan penting:
- **Setiap angka rupiah/persen di ringkasan, tabel, dan teks siap tempel WAJIB dari keluaran script.** Jangan menghitung sendiri walau terlihat sederhana. Satu perintah boleh dijalankan berkali-kali (mis. tiga pilihan hadiah).
- Hadiah dibayar **hanya setelah teman benar-benar membeli** (dan lewat masa retur/pembatalan), sehingga biaya = jumlah referral **berhasil** x biaya per referral.
- Hadiah berupa produk sendiri dihitung dengan **modal (HPP)**, bukan harga jual (isi opsi hadiah dengan HPP).
- `impas`: baris **BATAS ATAS hadiah pemberi** adalah plafon teoretis, **bukan anjuran**; yang disarankan ke pengguna adalah baris **Hadiah pemberi SARAN** (konservatif: total hadiah maks. 50% laba pesanan pertama). Status `RUGI DI PESANAN PERTAMA` wajib disampaikan apa adanya (jangan ditulis "aman").
- `impas`: batas aman **30%** dari laba kotor seumur pelanggan dan status poin ("perhatian" bila hadiah > 50% margin) adalah **aturan praktis**, bukan hukum; sebutkan itu. Frekuensi dan umur pelanggan adalah **asumsi** sampai ada data.
- `simulasi`: skenario bawaan (konservatif/realistis/optimis) hanya **asumsi awal**, bukan patokan pasar; selalu tulis "ESTIMASI" dan sarankan mengganti dengan data setelah 1 bulan.
- Bila script tidak bisa dijalankan (tidak ada Python): hitung dengan rumus di `references/rumus-dan-acuan.md`, tampilkan rumusnya, dan tulis "dihitung manual". Jika script bisa dijalankan, tulisan itu tidak boleh muncul.

### 4. Rancang hadiah
- **Dua sisi** (perujuk dan teman) biasanya lebih menarik daripada satu sisi; teman mendapat alasan mencoba, perujuk tidak terkesan "jualan".
- Bentuk hadiah dari yang paling aman: voucher belanja berikutnya / produk kecil bermodal rendah / poin, **bukan uang tunai** (uang tunai mengundang orang yang hanya memburu hadiah dan bisa menimbulkan urusan pajak).
- Beri **batas**: masa berlaku (mis. 30-60 hari), maksimal hadiah per orang per bulan, kuota program, minimal belanja. Angka batas dihitung dari `impas`/`biaya --anggaran`.
- Tampilkan hadiah dengan **angka yang terasa lebih besar**: harga di bawah sekitar Rp100.000 lebih jelas dalam rupiah ("potongan Rp15.000"), harga di atas itu uji persen.
- Bila hadiah > laba kotor pesanan pertama: boleh, **hanya bila** `impas` menunjukkan balik modal di pesanan ke-2/3 yang realistis; tandai jelas.

### 5. Aturan anti-curang (lihat `references/anti-curang-dan-kepatuhan.md`)
Minimum untuk usaha kecil: (1) **teman = pelanggan yang belum pernah beli** (cek buku catatan/nomor); (2) **dilarang self-referral** (nomor/alamat/akun yang sama); (3) hadiah cair **setelah pesanan selesai** dan lewat masa retur; (4) batas hadiah per orang per bulan; (5) pemilik boleh menolak/menarik hadiah bila ada indikasi akun ganda, dengan alasan yang dijelaskan sopan; (6) satu kode per perujuk, dicatat di lembar catatan.

### 6. Syarat & ketentuan
Tempelkan `templates/syarat-ketentuan.md` dan isi kurung siku dengan angka dari script. Wajib memuat: siapa yang berhak, bentuk dan nilai hadiah, kapan cair, masa berlaku, batas, larangan curang, hak usaha mengubah/menghentikan program (dengan pemberitahuan), data pribadi yang dicatat dan untuk apa, kontak.

### 7. Teks ajakan (lihat `templates/teks-ajakan.md`)
Sediakan 3 varian singkat (WA personal, status/story IG, kartu/brosur) dengan bahasa hangat. **Pengiriman dilakukan pemilik satu per satu** kepada pelanggan yang memang sudah berhubungan; **jangan** menawarkan kirim massal otomatis. Perujuk yang membagikan ke temannya sendiri; usaha **tidak meminta nomor teman**, teman yang menghubungi lebih dulu dengan menyebut nama/kode perujuk.

### 8. Kepatuhan
- **Promo tidak menyesatkan** (UU 8/1999 tentang Perlindungan Konsumen): tulis syarat penting di tempat yang terbaca, jangan klaim "gratis" bila ada syarat tersembunyi, jangan harga coret palsu, jangan sembunyikan batas kuota.
- **Data pribadi** (UU 27/2022 tentang Pelindungan Data Pribadi): catat seminimal mungkin (nama panggilan, nomor WA, kode, tanggal, status hadiah), beri tahu tujuannya, jangan kirim promosi ke orang yang tidak setuju atau sudah berhenti, jangan bagikan daftar ke pihak lain, simpan aman. Jangan minta pelanggan mengunggah nomor teman-temannya.
- **Marketplace:** ikuti aturan platform; jangan mengajak pembeli pindah transaksi di luar platform bila dilarang. Hadiah lewat voucher toko/produk setelah pesanan selesai.
- **Reseller:** komisi hanya dari penjualan barang nyata, satu tingkat; jangan ada biaya pendaftaran atau imbalan merekrut anggota (UU 7/2014 tentang Perdagangan melarang skema piramida).
- **Fasilitas kesehatan (klinik, RS, praktik dokter/dokter gigi/bidan, apotek, lab, fisioterapi, klinik kecantikan dengan tindakan medis) - PERLU REVIEW tenaga medis/hukum:** Permenkes 1787/2010 tentang Iklan dan Publikasi Pelayanan Kesehatan Pasal 5 melarang iklan/publikasi promosi penjualan **dalam bentuk apa pun**, termasuk diskon, imbalan atas pelayanan kesehatan, dan MLM (masih berlaku lewat UU 17/2023 Pasal 453; tidak ditemukan pencabutan di PP 28/2024; dicek 2026-09-30). Kode etik profesi (KODEKGI PDGI, KODEKI IDI) melarang dokter/dokter gigi memberi janji atau diskon agar pasien datang. Maka skill **tidak** merancang hadiah/diskon/poin/komisi untuk merujuk pasien, juga tidak hadiah "non-medis" untuk pengajak. Rancang: (1) program edukasi (kelas/materi kesehatan umum), (2) pengingat kontrol yang dikirim staf (skill `pengingat-pasien-klinik`), (3) kartu info klinik untuk pasien sendiri **tanpa imbalan** (klinik tidak meminta/mendorong pasien menyebarkannya; dokter gigi/dokter: KODEKGI 2020 Pasal 3 butir 1.2.4 & Pasal 5, KODEKI Pasal 3), (4) informasi layanan dan tarif yang jujur, tanpa testimoni dan pujian berlebihan. Hitungan `biaya`/`impas` tidak dipakai untuk imbalan rujukan. Bila pemilik tetap ingin hadiah, minta konfirmasi tertulis dari dinas kesehatan/organisasi profesi dulu. Rincian: `references/pola-per-usaha.md` bagian 3.
- **Pajak:** hadiah tunai atau komisi bernilai besar dapat punya konsekuensi pajak; skill ini tidak menghitung pajak, tanyakan konsultan pajak.

### 9. Ukur & rencana uji 30 hari
Catat: jumlah perujuk aktif, teman yang membeli, biaya per referral (script), porsi pelanggan baru yang "tahu dari teman" (tanyakan saat pesan pertama: "Tahu kami dari mana?"). Minggu 1 uji ke 10-20 pelanggan terbaik; minggu 2-3 sebar bertahap; minggu 4 tinjau angka. **Hentikan/ubah** bila biaya per referral melebihi batas aman, banyak indikasi curang, atau perujuk aktif < 3 setelah 4 minggu (ubah momen atau hadiah, bukan langsung menaikkan).

## Format output
Selalu urutan ini, bahasa sederhana:
1. **Ringkasan 3 baris:** program yang disarankan, hadiah, alasan utama.
2. **Asumsi** (margin default? frekuensi beli? biaya iklan?).
3. **Tabel angka** dari script: biaya per referral, laba pesanan pertama setelah hadiah, balik modal, batas aman, status; untuk poin: persen hadiah, porsi margin, liability.
4. **Aturan program** (siapa, hadiah, kapan cair, batas, anti-curang).
5. **Syarat & ketentuan** siap tempel.
6. **Teks ajakan** WA/IG siap kirim (dengan angka dari script).
7. **Simulasi** (bila diminta) berlabel **ESTIMASI**.
8. **Langkah minggu ini** (maks. 5 butir) + lembar catatan.
9. Catatan: "Angka dihitung dengan script dari data yang Anda berikan. Keputusan besar hadiah tetap di tangan Anda." + catatan kepatuhan yang relevan.

## Contoh
**Input:** "Toko hijab online saya, pesanan rata-rata Rp180.000, untung kotor 40%. Mau program ajak teman, hadiah Rp15.000 untuk dua-duanya. Aman nggak?"

**Output (ringkas):**
- Ringkasan: referral dua sisi, voucher Rp15.000 untuk teman dan Rp15.000 untuk perujuk setelah pesanan teman selesai. Biaya per referral Rp30.000 (16,67% dari pesanan, 41,67% dari laba kotor). Laba pesanan pertama tetap Rp42.000.
- Balik modal langsung di pesanan pertama; batas hadiah aman Rp129.600 per referral (asumsi 0,5x per bulan, 12 bulan). Lebih murah dari iklan Rp45.000 per pelanggan baru.
- Kuota: anggaran Rp600.000 cukup untuk 20 referral berhasil per bulan. Lengkap dengan S&K dan teks WA.
Contoh lengkap: `examples/`.

## Batasan & penanganan error
- Script keluar dengan `GAGAL: ...` (kode 2) untuk input tidak terbaca, ambigu, atau mustahil (mis. `12.5`, margin 0% atau 100%, hadiah persen di atas 100%, jumlah orang pecahan). Jelaskan dengan bahasa awam dan minta angka yang benar; **jangan menebak**.
- Baris `PERHATIAN:` (hadiah lebih besar dari laba pesanan pertama, melebihi anggaran, poin melebihi margin) wajib disampaikan, bukan disembunyikan.
- Skill tidak menjamin pelanggan akan mengajak teman; tingkat merujuk bergantung pada produk, layanan, dan momen. Jangan menjanjikan kenaikan omzet.
- Skill tidak mengirim pesan, tidak mengelola kontak otomatis, dan tidak memasang aplikasi. Semua pengiriman oleh pemilik.
- Bukan nasihat hukum, pajak, atau profesi kesehatan; arahkan ke profesional untuk kasus khusus. Bagian fasilitas kesehatan berstatus **PERLU REVIEW tenaga medis/hukum**.
- Nama marketplace/aplikasi hanya penyebut kanal; skill ini tidak berafiliasi dengan pihak mana pun.
