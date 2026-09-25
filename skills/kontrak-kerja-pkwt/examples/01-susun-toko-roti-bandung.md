# Uji 01 — Mode Susun: toko roti di Bandung, 2 karyawan produksi, kontrak 1 tahun

> Penguji independen (Tahap 6), 25 September 2026. Agent hanya membaca folder skill `kontrak-kerja-pkwt/`.
> Script dijalankan dari salinan di scratchpad (`uji-pkwt/`), bukan dari repo.

## Input pengguna
> "Saya punya toko roti di Bandung (Roti Hangat, Jl. Sukajadi). Mau rekrut 2 orang bagian produksi, Asep dan Rina, kontrak 1 tahun mulai 1 Oktober 2026. Gaji pokok 3,9 juta + tunjangan tetap 250 ribu, uang makan 20 ribu per hari masuk. Kerja Senin–Sabtu jam 7 pagi sampai 3 sore. Alasannya kami buka lini baru roti beku (frozen) untuk dijual ke kafe, masih uji pasar setahun. Tolong bikinin kontraknya dan hitung kompensasi akhirnya."

## Proses agent (mengikuti SKILL.md)
1. Mode **Susun** + **Hitung**. Data cukup untuk 7 dari 8 butir pertanyaan; yang kurang (nama penanda tangan, UMK, tanggal gajian, identitas pekerja) diberi `[isi: ...]` sesuai aturan "jangan mengarang".
2. **Uji kelayakan PKWT**: produksi roti umumnya pekerjaan tetap, tetapi pengguna memberi alasan jujur "produk baru yang masih uji pasar" (PP 35/2021 Pasal 5 / UU 13/2003 Pasal 59 ayat (1) huruf d) → PKWT boleh, alasan ditulis di Pasal 1 ayat (3), ditandai 🟠 bila Asep/Rina ternyata juga mengerjakan roti reguler.
3. **Varian A** (jangka waktu) 12 bulan.
4. **Script**:
```bash
python3 scripts/hitung_pkwt.py --periode "1 Oktober 2026 s.d. 30 September 2027" --gaji-pokok 3,9jt --tunjangan-tetap 250rb
```
Output apa adanya:
```
HITUNG KOMPENSASI AKHIR PKWT
Upah 1 bulan : Rp4.150.000 (gaji pokok Rp3.900.000 + tunjangan tetap Rp250.000)
Total PKWT   : 1 Oktober 2026 s.d. 30 September 2027 = 12 bulan (batas 5 tahun: s.d. 30 September 2031) OK

| Periode | Kontrak | Dijalani | Masa kerja | Bulan | Rumus | Kompensasi |
|---|---|---|---|---|---|---|
| 1 | 1 Oktober 2026 s.d. 30 September 2027 | s.d. 30 September 2027 | 12 bulan | 12 | 12 bulan: 1 x upah = Rp4.150.000 | Rp4.150.000 |

TOTAL KOMPENSASI (dibayar pengusaha ke pekerja): Rp4.150.000
...
```
5. **Cek upah**: UMK Kota Bandung 2026 tidak diberikan pengguna → tidak dikarang; ditulis `[isi: ...]` + peringatan untuk dicek (upah Rp4.150.000 perlu dibandingkan). Uang makan harian **tidak** masuk dasar kompensasi (tergantung kehadiran). Upah pokok 3,9 jt = 94% dari upah tetap (≥ 75%, OK).
6. **Jam kerja**: Senin–Sabtu 07.00–15.00 dengan istirahat 1 jam = 7 jam × 6 hari = **42 jam/minggu > 40 jam**. Agent mengusulkan Sabtu 07.00–12.00 (5 jam) agar total 40 jam. *(Catatan penguji: ini tertangkap dari rumus di `dasar-hukum.md` §4 no. 7 "40 jam/minggu"; checklist B7 justru menulis "7 jam × 6 hari" yang = 42 jam — lihat HASIL-UJI temuan S2.)*

## Output agent

Sebelum drafnya, dua hal penting:
- **Alasan kontrak** sudah saya tulis di Pasal 1 ayat (3): lini produk baru roti beku yang masih uji pasar. Pastikan Asep dan Rina memang ditugaskan di lini itu. Kalau mereka juga membuat roti harian toko (pekerjaan yang ada terus), kontrak ini berisiko dianggap karyawan tetap (PKWTT).
- **Jam kerja** Senin–Sabtu 07.00–15.00 = 42 jam/minggu, melebihi batas 40 jam. Saya ubah Sabtu menjadi 07.00–12.00. Kalau Sabtu tetap sampai 15.00, 2 jam kelebihannya dihitung lembur.

PKWT dibuat **per orang**. Di bawah ini draf untuk Asep; untuk Rina, salin draf yang sama dan ganti bagian identitas PIHAK KEDUA serta nomor perjanjian.

---

# PERJANJIAN KERJA WAKTU TERTENTU (PKWT)
**Nomor: [isi: nomor, mis. 001/PKWT/RH/X/2026]**

Pada hari ini, [isi: hari], tanggal [isi: tanggal terbilang] ([isi: tanggal angka]), bertempat di Bandung, yang bertanda tangan di bawah ini:

**I. [isi: nama pemilik/penanda tangan]**
Jabatan: [isi: Pemilik]
dalam hal ini bertindak untuk dan atas nama **Roti Hangat**, usaha toko roti dan produksi roti, beralamat di Jl. Sukajadi [isi: nomor, kelurahan], Kota Bandung,
selanjutnya disebut **PIHAK PERTAMA (Pengusaha)**.

**II. Asep [isi: nama lengkap]**
Jenis kelamin: L · Tempat/tanggal lahir: [isi] (umur [isi] tahun)
NIK: [isi: NIK] · Alamat: [isi: alamat]
dalam hal ini bertindak untuk dan atas nama diri sendiri, selanjutnya disebut **PIHAK KEDUA (Pekerja)**.

PIHAK PERTAMA dan PIHAK KEDUA (bersama-sama disebut **Para Pihak**) sepakat membuat Perjanjian Kerja Waktu Tertentu dengan ketentuan sebagai berikut:

## Pasal 1 — Jabatan, Jenis Pekerjaan, dan Tempat Kerja
1. PIHAK PERTAMA mempekerjakan PIHAK KEDUA sebagai **Staf Produksi Roti Beku** dengan uraian tugas: menyiapkan adonan, membentuk, memanggang sebagian, membekukan, dan mengemas produk roti beku sesuai standar resep dan kebersihan pangan.
2. Tempat kerja: dapur produksi Roti Hangat, Jl. Sukajadi [isi: nomor], Kota Bandung.
3. Pekerjaan ini bersifat **tidak tetap** karena: berhubungan dengan **produk baru (lini roti beku untuk kafe) yang masih dalam masa percobaan/uji pasar** selama 12 bulan.

## Pasal 2 — Jangka Waktu
1. Perjanjian ini berlaku selama **12 (dua belas) bulan**, terhitung mulai **1 Oktober 2026** sampai dengan **30 September 2027**.
2. Perjanjian ini dapat diperpanjang berdasarkan kesepakatan tertulis Para Pihak, dengan ketentuan jangka waktu seluruh PKWT beserta perpanjangannya **tidak melebihi 5 (lima) tahun**.
3. Perjanjian ini **tidak mensyaratkan masa percobaan kerja**.

## Pasal 3 — Waktu Kerja dan Lembur
1. Waktu kerja: 40 jam seminggu untuk 6 hari kerja, yaitu Senin–Jumat pukul 07.00–15.00 dengan istirahat 1 jam (7 jam kerja), dan Sabtu pukul 07.00–12.00 (5 jam kerja).
2. Kerja lembur hanya dengan persetujuan PIHAK KEDUA, paling lama 4 jam sehari dan 18 jam seminggu, dan dibayar upah lembur sesuai peraturan (upah sejam = 1/173 × upah sebulan).

## Pasal 4 — Upah
1. PIHAK KEDUA menerima upah per bulan sebesar:
   - Gaji pokok: **Rp3.900.000 (tiga juta sembilan ratus ribu rupiah)**
   - Tunjangan tetap: **Rp250.000 (dua ratus lima puluh ribu rupiah)**
   - Jumlah upah tetap: **Rp4.150.000 (empat juta seratus lima puluh ribu rupiah)**
   - Tunjangan tidak tetap: uang makan **Rp20.000 (dua puluh ribu rupiah)** per hari hadir.
2. Upah tidak lebih rendah dari upah minimum yang berlaku di Kota Bandung tahun 2026, yaitu **Rp[isi: UMK Kota Bandung 2026 — cek situs Disnaker]**.
3. Upah dibayarkan setiap tanggal **[isi: tanggal gajian]** melalui [isi: transfer ke rekening atas nama PIHAK KEDUA / tunai dengan tanda terima], disertai slip upah.
4. Potongan upah hanya untuk hal yang diatur peraturan atau disepakati tertulis, termasuk iuran BPJS bagian pekerja dan PPh 21.

## Pasal 5 — Jaminan Sosial, THR, dan Cuti
1. PIHAK PERTAMA mendaftarkan PIHAK KEDUA sebagai peserta **BPJS Ketenagakerjaan** dan **BPJS Kesehatan** paling lambat [isi: tanggal, disarankan sebelum/saat 1 Oktober 2026], dengan iuran sesuai porsi yang ditentukan peraturan.
2. PIHAK KEDUA yang telah bekerja paling sedikit 1 (satu) bulan terus-menerus berhak atas **Tunjangan Hari Raya (THR) Keagamaan** sesuai peraturan.
3. PIHAK KEDUA berhak atas istirahat mingguan, hari libur resmi, dan **cuti tahunan paling sedikit 12 (dua belas) hari kerja** setelah bekerja 12 (dua belas) bulan terus-menerus, serta cuti lain sesuai peraturan (sakit, haid, melahirkan, dll.).

## Pasal 6 — Hak dan Kewajiban
1. PIHAK PERTAMA wajib: membayar upah tepat waktu; menyediakan alat, perlengkapan, dan tempat kerja yang aman (K3), termasuk sarung tangan tahan panas dan alat pelindung di area oven dan freezer; memberi perlakuan tanpa diskriminasi; mencatatkan perjanjian ini ke instansi ketenagakerjaan.
2. PIHAK KEDUA wajib: melaksanakan tugas sesuai Pasal 1 dengan baik; mematuhi tata tertib kebersihan dan keamanan pangan yang telah diberitahukan tertulis; menjaga barang milik PIHAK PERTAMA; menjaga kerahasiaan resep dan data usaha.

## Pasal 7 — Berakhirnya Perjanjian dan Uang Kompensasi
1. Perjanjian ini berakhir apabila: jangka waktu berakhir; PIHAK KEDUA meninggal dunia; ada putusan pengadilan yang berkekuatan hukum tetap.
2. Saat perjanjian berakhir, PIHAK PERTAMA memberikan **uang kompensasi** kepada PIHAK KEDUA yang telah bekerja paling sedikit 1 (satu) bulan terus-menerus, sebesar **masa kerja (bulan) ÷ 12 × 1 bulan upah** (upah = gaji pokok + tunjangan tetap), atau 1 bulan upah untuk masa kerja 12 bulan. Perkiraan untuk perjanjian ini: **Rp4.150.000** (empat juta seratus lima puluh ribu rupiah).
3. Jika perjanjian diperpanjang, uang kompensasi untuk jangka waktu sebelum perpanjangan dibayar saat jangka waktu itu selesai.

## Pasal 8 — Pengakhiran Sebelum Waktunya
1. Pihak yang mengakhiri perjanjian sebelum jangka waktu berakhir, di luar alasan Pasal 7 ayat (1), wajib membayar **ganti rugi** kepada pihak lainnya sebesar **upah PIHAK KEDUA sampai batas waktu berakhirnya jangka waktu perjanjian**.
2. Dalam hal pengakhiran sebelum waktunya, PIHAK PERTAMA tetap memberikan uang kompensasi yang dihitung dari jangka waktu yang telah dijalani PIHAK KEDUA.
3. Pihak yang ingin mengakhiri memberi tahu secara tertulis paling lambat 14 (empat belas) hari sebelumnya, dan Para Pihak menyelesaikan serah terima pekerjaan serta barang milik PIHAK PERTAMA.

## Pasal 9 — Tata Tertib dan Sanksi
Pelanggaran tata tertib ditangani secara bertahap melalui teguran dan Surat Peringatan sesuai tata tertib tertulis Roti Hangat. Tidak ada denda atau penahanan dokumen pribadi (ijazah, KTP asli, dll.).

## Pasal 10 — Kerahasiaan
Selama dan setelah perjanjian berakhir, PIHAK KEDUA tidak membocorkan resep, daftar pelanggan kafe, harga pokok, dan data rahasia usaha lainnya yang diketahui karena pekerjaannya.

## Pasal 11 — Penyelesaian Perselisihan
Perselisihan diselesaikan secara musyawarah (bipartit) paling lama 30 hari. Jika tidak tercapai, Para Pihak menempuh penyelesaian perselisihan hubungan industrial sesuai peraturan (mediasi di Dinas Tenaga Kerja Kota Bandung, lalu Pengadilan Hubungan Industrial).

## Pasal 12 — Penutup
1. Hal yang belum diatur mengikuti peraturan perundang-undangan ketenagakerjaan yang berlaku.
2. Perjanjian ini dibuat dalam bahasa Indonesia dan huruf latin, rangkap 2 (dua) asli bermeterai cukup dengan kekuatan hukum yang sama, masing-masing untuk PIHAK PERTAMA dan PIHAK KEDUA, serta dicatatkan PIHAK PERTAMA ke instansi ketenagakerjaan paling lambat 3 (tiga) hari kerja setelah ditandatangani.
3. Para Pihak telah membaca, memahami, dan menandatangani perjanjian ini dalam keadaan sadar tanpa paksaan.

| PIHAK PERTAMA | PIHAK KEDUA |
|---|---|
| Roti Hangat | |
| [meterai Rp10.000] | [meterai Rp10.000] |
| **[isi: nama pemilik]** — Pemilik | **Asep [isi: nama lengkap]** |

---
CATATAN PENGISIAN (jangan dicetak)
- Masih kosong: nomor perjanjian, hari/tanggal tanda tangan, nama & jabatan penanda tangan, alamat lengkap usaha, identitas lengkap Asep (dan Rina), **UMK Kota Bandung 2026**, tanggal gajian, cara bayar, tanggal pendaftaran BPJS.
- Asumsi: Varian A (jangka waktu 12 bulan); Sabtu 5 jam agar total 40 jam/minggu; uang makan tidak masuk dasar kompensasi; pemberitahuan pengakhiran 14 hari.
- Hitungan script: total PKWT 1 Okt 2026–30 Sep 2027 = 12 bulan; batas 5 tahun s.d. 30 September 2031; kompensasi **Rp4.150.000 per orang** (12 bulan = 1 × upah Rp4.150.000). Untuk 2 orang: **Rp8.300.000**, dibayar 30 September 2027.
- Peringatan: (1) cek upah Rp4.150.000 ≥ UMK Kota Bandung 2026 di situs Disnaker; bila di bawah UMK, naikkan (dilarang membayar di bawah upah minimum, kecuali usaha mikro/kecil dengan ketentuan khusus). (2) Alasan "produk baru" hanya aman bila Asep/Rina benar-benar di lini roti beku.

CHECKLIST SEBELUM TANDA TANGAN
[ ] Pekerja membaca seluruh isi & diberi waktu bertanya   [ ] Semua [isi: ...] sudah terisi
[ ] Upah ≥ UMK Kota Bandung 2026 (dicek di situs Disnaker) [ ] Paraf tiap halaman, 2 rangkap asli, meterai Rp10.000
[ ] Daftarkan BPJS TK & Kesehatan                            [ ] Catatkan PKWT daring maks. 3 hari kerja
[ ] Simpan salinan KTP/NIK secara terbatas (data pribadi)

Disclaimer: Draf/hasil ini bantuan administrasi, bukan nasihat hukum. Dasar: UU 13/2003 sebagaimana diubah UU 6/2023, PP 35/2021, dan Putusan MK 168/PUU-XXI/2023 (dicek 25 September 2026). MK memerintahkan UU Ketenagakerjaan baru paling lambat Oktober 2026; per tanggal cek, RUU Pelindungan Ketenagakerjaan belum disahkan, sehingga aturan PKWT bisa berubah. Sebelum ditandatangani, konsultasikan ke Disnaker setempat atau konsultan hukum ketenagakerjaan.

## Verifikasi independen (penguji)
- 1 Okt 2026 s.d. 30 Sep 2027 inklusif = 365 hari = tepat 12 bulan kalender → PP 35/2021 Pasal 16 ayat (1) huruf a: 1 × upah = 3.900.000 + 250.000 = **4.150.000** ✅ (Fraction(12)/12 × 4.150.000 = 4.150.000).
- Batas 5 tahun: 1 Okt 2026 + 60 bulan − 1 hari = 30 Sep 2031 ✅.
- 2 orang × 4.150.000 = 8.300.000 ✅.

## Penilaian
Lulus. Semua `[isi: ...]` benar, UMK tidak dikarang, tanpa masa percobaan/denda, kompensasi dari script, disclaimer lengkap. Catatan: skill tidak memberi panduan eksplisit untuk **lebih dari satu pekerja** (agent menanganinya sendiri: satu PKWT per orang) dan temuan jam kerja 42 jam hanya tertangkap karena agent teliti, bukan karena checklist.
