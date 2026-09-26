# Uji Pembuat 01 — Toko kue online (mode SUSUN + CEK)

> Uji oleh **pembuat skill** (bukan penguji independen), 2026-09-25. Belum termasuk uji Tahap 6 (01–05, A/B, banding pesaing).
> Script: `scripts/cek_kebijakan.py` v1.0.0, Python 3, Linux. Tes regresi `tests/uji_regresi.py`: LULUS 53 uji.

## Bagian A — Mode SUSUN

**Input pengguna:**
> Bikinin kebijakan privasi buat toko kue online aku, Dapur Bu Sari (pemiliknya aku, Sari Wulandari). Jualan lewat website dapurbusari.id sama WA 0812-0000-0000, kirim pakai kurir, bayar transfer bank & payment gateway, website pakai Meta Pixel. Promo kadang lewat WA.

**Perilaku agent:** info wajib yang kurang (email urusan data, alamat, nama kurir & payment gateway, masa simpan data pixel, jumlah admin) **tidak dikarang** → dibiarkan `[isi: ...]`. Masa simpan transaksi 10 tahun (UU KUP Ps. 28 ayat (11)) dan chat 1 tahun ditulis sebagai saran default. Transfer luar negeri memakai opsi 5(a) karena WhatsApp/Meta Pixel.

**Output (draf lengkap):**

```markdown
# Kebijakan Privasi Dapur Bu Sari

**Berlaku sejak:** 1 Oktober 2026
**Terakhir diperbarui:** 25 September 2026

Kebijakan Privasi ini menjelaskan data pribadi apa yang kami kumpulkan, untuk apa, kepada siapa data dibagikan, berapa lama disimpan, dan hak-hak Anda. Kebijakan ini disusun dengan mengacu pada Undang-Undang Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP).

## 1. Siapa kami (pengendali data)
Dapur Bu Sari ("kami") adalah pengendali data pribadi untuk website dapurbusari.id dan akun WhatsApp Business kami.
- Pemilik / penanggung jawab: Sari Wulandari
- Alamat: [isi: alamat usaha]
- Kontak urusan data pribadi: [isi: email] · WhatsApp 0812-0000-0000

## 2. Data pribadi yang kami kumpulkan
**Data yang Anda berikan langsung:** nama, nomor WhatsApp, alamat pengiriman, catatan pesanan (mis. tulisan di kue), bukti transfer, dan isi percakapan layanan pelanggan.
**Data yang terkumpul otomatis:** alamat IP, jenis perangkat, halaman yang dikunjungi, serta cookie dan Meta Pixel di website.

Kami hanya mengumpulkan data yang diperlukan untuk tujuan di bawah ini.

## 3. Tujuan, dasar pemrosesan, dan masa simpan
| Data | Untuk apa | Dasar pemrosesan (UU PDP Pasal 20) | Disimpan berapa lama |
|---|---|---|---|
| Nama, no. WA, alamat, catatan pesanan | Memproses & mengirim pesanan | Pelaksanaan perjanjian (pesanan Anda) | 10 tahun untuk catatan transaksi (kewajiban pembukuan pajak) |
| Bukti transfer | Mencocokkan pembayaran | Pelaksanaan perjanjian & kewajiban hukum | 10 tahun (pembukuan pajak) |
| Isi chat WhatsApp | Menjawab pertanyaan & keluhan | Pelaksanaan perjanjian / kepentingan yang sah | 1 tahun sejak chat terakhir |
| No. WA | Mengirim info promo | Persetujuan Anda (bisa ditarik kapan saja) | Sampai Anda menarik persetujuan |
| Data kunjungan website (cookie, Meta Pixel) | Mengukur & menampilkan iklan | Persetujuan Anda (banner cookie) | [isi: sesuai pengaturan Meta, mis. 180 hari] |

Setelah masa simpan berakhir atau tujuan tercapai, data kami hapus atau musnahkan, kecuali wajib disimpan lebih lama menurut peraturan perundang-undangan.

## 4. Kepada siapa data dibagikan
Kami **tidak menjual** data pribadi Anda. Data hanya kami bagikan seperlunya kepada:
| Penerima | Data yang diberikan | Tujuan |
|---|---|---|
| Jasa kurir: [isi: nama kurir] | Nama, no. HP, alamat | Mengirim pesanan |
| Payment gateway: [isi: nama payment gateway] dan bank penerima transfer | Nama, nominal, data transaksi | Memproses pembayaran |
| Meta (WhatsApp Business, Meta Pixel) | No. WA, isi chat, data kunjungan website | Layanan pesan & iklan |
| Penyedia hosting website: [isi: nama] | Data pesanan di website | Menjalankan website |
| Instansi berwenang | Sesuai permintaan resmi | Memenuhi kewajiban hukum |

Pihak yang memproses data atas nama kami (prosesor data) wajib menjaga kerahasiaan dan keamanan data sesuai perintah kami.

## 5. Penyimpanan data di luar negeri
Sebagian layanan yang kami gunakan (WhatsApp/Meta, Meta Pixel, [isi: hosting bila di luar negeri]) dapat menyimpan atau memproses data di server di luar Indonesia. Kami memilih penyedia yang memiliki standar pelindungan data yang memadai dan, bila diperlukan, meminta persetujuan Anda sesuai UU PDP Pasal 56.

## 6. Hak Anda
Sesuai UU PDP Pasal 5–13, Anda berhak:
1. Mendapat informasi tentang identitas kami, tujuan, dan dasar pemrosesan data Anda.
2. **Mengakses** dan meminta **salinan** data pribadi Anda.
3. **Memperbaiki**, melengkapi, atau memperbarui data yang salah atau tidak lengkap.
4. **Menghapus** data atau meminta kami mengakhiri pemrosesannya.
5. **Menarik persetujuan** yang pernah Anda berikan (mis. untuk promo).
6. Menunda atau membatasi pemrosesan.
7. Menggugat dan menerima ganti rugi atas pelanggaran pemrosesan data Anda.

## 7. Cara mengajukan permintaan
Kirim permintaan ke [isi: email] atau WhatsApp 0812-0000-0000 dengan menyebut nama, nomor WA yang dipakai memesan, dan hak yang ingin digunakan. Kami tidak meminta foto KTP untuk permintaan ini.
Kami menanggapi paling lambat **3×24 jam** sejak permintaan diterima untuk permintaan akses, perbaikan, dan penarikan persetujuan (UU PDP Pasal 30, 32, 40). Bila permintaan tidak dapat dipenuhi (mis. catatan transaksi wajib disimpan untuk pajak), kami menjelaskan alasannya secara tertulis.

## 8. Keamanan data
Kami menjaga data dengan langkah yang wajar: akses WhatsApp Business dan admin website hanya untuk pemilik dan [isi: jumlah] admin, kata sandi kuat + verifikasi dua langkah, dan HP toko terkunci dengan PIN.

## 9. Jika terjadi kebocoran data
Jika terjadi kegagalan pelindungan data pribadi (mis. kebocoran atau akses tanpa izin), kami akan memberi tahu Anda dan lembaga yang berwenang secara tertulis **paling lambat 3×24 jam**, berisi: data apa yang terungkap, kapan dan bagaimana terjadinya, serta langkah penanganan dan pemulihan (UU PDP Pasal 46).

## 10. Cookie dan piksel iklan
Website kami menggunakan cookie yang diperlukan agar situs berjalan dan Meta Pixel untuk iklan. Anda dapat menolak Meta Pixel melalui banner cookie saat pertama berkunjung atau lewat pengaturan browser.

## 11. Perubahan kebijakan
Jika kebijakan ini berubah, kami akan memberitahukannya **sebelum** perubahan berlaku melalui website dan WhatsApp, paling lambat 7 hari sebelumnya.

## 12. Hubungi kami
Pertanyaan tentang kebijakan ini: [isi: email] · WhatsApp 0812-0000-0000 · [isi: alamat].
```

**Hasil `cek_kebijakan.py` atas draf:**
```
PEMERIKSAAN KEBIJAKAN PRIVASI (UU 27/2022 PDP) — draf-dapur.md
Skor kelengkapan: 100/100  |  Status: PERLU DILENGKAPI  |  740 kata

UNSUR:
  [v] Identitas pengendali data (nama usaha/pemilik) — ADA
  [v] Kontak yang bisa dihubungi (email/WA/alamat) — ADA
  [v] Jenis data pribadi yang dikumpulkan — ADA
  [v] Tujuan pemrosesan — ADA
  [v] Dasar pemrosesan (persetujuan, perjanjian, kewajiban hukum, dll.) — ADA
  [v] Pihak yang menerima data (kurir, payment gateway, marketplace, cloud, iklan) — ADA
  [v] Transfer/penyimpanan data di luar negeri — ADA
  [v] Masa simpan (retensi) data — ADA
  [v] Hak subjek data (akses, koreksi, hapus, tarik persetujuan) — ADA
  [v] Cara mengajukan permintaan hak & batas waktu tanggapan — ADA
  [v] Langkah keamanan data — ADA
  [v] Pemberitahuan bila terjadi kebocoran (kegagalan pelindungan data) — ADA
  [v] Tanggal berlaku / terakhir diperbarui — ADA
  [v] Cara memberi tahu perubahan kebijakan — ADA

FRASA BERISIKO: tidak ditemukan.

CATATAN:
  - Masih ada 11 isian kosong (mis. [isi: alamat usaha]). Lengkapi sebelum dipublikasikan.
  - Info: tidak ada kontak PPDP/DPO. Wajib hanya bila memenuhi Pasal 53 (layanan publik, pemantauan skala besar, atau data spesifik skala besar); UMKM biasa cukup narahubung.

⚠ Pemeriksa bantu berbasis kata kunci, bukan penilaian hukum. Kata kunci yang ditemukan belum tentu isinya memadai.
```

**Yang masih perlu dilengkapi (disampaikan ke pengguna):** email urusan data, alamat usaha, nama kurir, nama payment gateway, penyedia hosting, masa simpan data Meta Pixel, jumlah admin.

**Pesan salam WA (mode 2, template B):**
> Halo, terima kasih sudah menghubungi Dapur Bu Sari 🙏
> Untuk melayani pesanan, kami akan mencatat nama, nomor WA, dan alamat Anda. Data hanya dipakai untuk pesanan ini dan dibagikan ke kurir seperlunya. Kebijakan privasi: dapurbusari.id/privasi
> Ingin juga menerima info promo? Balas **SETUJU PROMO**. Bisa berhenti kapan saja dengan membalas **STOP**.

## Bagian B — Mode CEK (kebijakan lama hasil salin-tempel)

**Input (file `lama.md`):**
```
KEBIJAKAN PRIVASI TOKO SEJAHTERA ABADI

Kami menghargai privasi Anda. Dengan menggunakan website ini, Anda dianggap telah menyetujui kebijakan privasi ini.

Informasi yang kami kumpulkan: nama, email, nomor telepon, alamat.

Kami menggunakan informasi untuk memproses pesanan dan mengirimkan penawaran. Informasi dapat kami bagikan kepada mitra bisnis kami dan pihak ketiga mana pun yang bekerja sama dengan kami.

Kami menjaga data Anda dengan sistem yang 100% aman. Namun kami tidak bertanggung jawab atas kebocoran data akibat serangan pihak luar.

Sesuai GDPR, Anda dapat meminta penghapusan data dengan menghubungi kami di cs@tokosejahtera.co.id.

Kebijakan ini dapat diubah sewaktu-waktu tanpa pemberitahuan.
```

**Hasil `cek_kebijakan.py`:**
```
PEMERIKSAAN KEBIJAKAN PRIVASI (UU 27/2022 PDP) — lama.md
Skor kelengkapan: 37/100  |  Status: KURANG LENGKAP  |  100 kata

UNSUR:
  [ ] Identitas pengendali data (nama usaha/pemilik) — TIDAK ADA
  [v] Kontak yang bisa dihubungi (email/WA/alamat) — ADA
  [v] Jenis data pribadi yang dikumpulkan — ADA
  [v] Tujuan pemrosesan — ADA
  [ ] Dasar pemrosesan (persetujuan, perjanjian, kewajiban hukum, dll.) — TIDAK ADA
  [v] Pihak yang menerima data (kurir, payment gateway, marketplace, cloud, iklan) — ADA
  [ ] Transfer/penyimpanan data di luar negeri — TIDAK ADA
  [ ] Masa simpan (retensi) data — TIDAK ADA
  [~] Hak subjek data (akses, koreksi, hapus, tarik persetujuan) — SEBAGIAN (kurang: akses, koreksi, tarik persetujuan)
  [v] Cara mengajukan permintaan hak & batas waktu tanggapan — ADA
  [ ] Langkah keamanan data — TIDAK ADA
  [ ] Pemberitahuan bila terjadi kebocoran (kegagalan pelindungan data) — TIDAK ADA
  [ ] Tanggal berlaku / terakhir diperbarui — TIDAK ADA
  [ ] Cara memberi tahu perubahan kebijakan — TIDAK ADA

YANG PERLU DITAMBAHKAN:
  1. Sebutkan nama usaha/badan usaha dan nama pemilik atau penanggung jawab sebagai pengendali data. [UU 27/2022 Pasal 21 & 31 (pengendali wajib jelas identitasnya)]
  2. Sebutkan dasar pemrosesan per tujuan: persetujuan, pelaksanaan perjanjian/pesanan, kewajiban hukum (mis. pajak), atau kepentingan yang sah. [UU 27/2022 Pasal 20 ayat (2) & Pasal 21 ayat (1) huruf a]
  3. Jelaskan apakah data disimpan/diproses di luar Indonesia (mis. Google Drive, Meta/WhatsApp, layanan cloud) dan pelindungannya. [UU 27/2022 Pasal 56]
  4. Tulis berapa lama data disimpan per jenis (mis. data pesanan 10 tahun untuk pembukuan pajak, chat CS 1 tahun) lalu dihapus. [UU 27/2022 Pasal 21 ayat (1) huruf d & f, Pasal 43–44]
  5. Tuliskan hak-hak berikut dengan bahasa sederhana: mengakses & minta salinan, memperbaiki, menghapus, menarik persetujuan (juga: keberatan atas keputusan otomatis, membatasi pemrosesan, gugat ganti rugi). [UU 27/2022 Pasal 5–13 & Pasal 21 ayat (1) huruf g]
  6. Jelaskan langkah keamanan secara jujur dan umum (akses dibatasi, kata sandi + verifikasi 2 langkah, perangkat terkunci, cadangan). [UU 27/2022 Pasal 35–39]
  7. Tulis bahwa bila terjadi kegagalan pelindungan data, Anda akan memberi tahu pelanggan secara tertulis paling lambat 3×24 jam. [UU 27/2022 Pasal 46]
  8. Tulis "Berlaku sejak: [tanggal]" dan "Terakhir diperbarui: [tanggal]" di bagian atas. [UU 27/2022 Pasal 21 ayat (2) (perubahan informasi)]
  9. Tulis bahwa perubahan akan diberitahukan SEBELUM berlaku (mis. lewat website/WA/email). [UU 27/2022 Pasal 21 ayat (2)]

FRASA BERISIKO:
  - [TINGGI] baris 3: "Kami menghargai privasi Anda. Dengan menggunakan website ini, Anda dianggap telah menyetujui kebijakan privasi ini."
      Alasan: Persetujuan diam-diam/dianggap tidak memenuhi syarat persetujuan eksplisit (Pasal 20 & 22).
      Saran : Minta persetujuan aktif (centang/ketik SETUJU), dan untuk pemrosesan wajib (pesanan) gunakan dasar 'pelaksanaan perjanjian'.
  - [TINGGI] baris 9: "Kami menjaga data Anda dengan sistem yang 100% aman. Namun kami tidak bertanggung jawab atas kebocoran data akibat serangan pihak luar."
      Alasan: Pengendali tetap bertanggung jawab atas pemrosesan & wajib melindungi data (Pasal 35, 46, 47). Klausul lepas tanggung jawab tidak menghapus kewajiban ini dan merusak kepercayaan.
      Saran : Hapus. Ganti dengan komitmen menjaga keamanan dan memberi tahu paling lambat 3×24 jam bila terjadi kebocoran.
  - [SEDANG] baris 9: "Kami menjaga data Anda dengan sistem yang 100% aman. Namun kami tidak bertanggung jawab atas kebocoran data akibat serangan pihak luar."
      Alasan: Klaim keamanan mutlak menyesatkan dan bertentangan dengan kewajiban menyiapkan penanganan kebocoran (Pasal 46).
      Saran : Ganti dengan langkah keamanan nyata yang dilakukan.
  - [SEDANG] baris 11: "Sesuai GDPR, Anda dapat meminta penghapusan data dengan menghubungi kami di cs@tokosejahtera.co.id."
      Alasan: Tampaknya disalin dari kebijakan luar negeri (GDPR/CCPA). Hak & kewajiban di Indonesia mengikuti UU 27/2022.
      Saran : Tulis ulang dengan rujukan UU 27/2022 (batas 3×24 jam, pemberitahuan kebocoran, dasar pemrosesan Pasal 20).
  - [SEDANG] baris 13: "Kebijakan ini dapat diubah sewaktu-waktu tanpa pemberitahuan."
      Alasan: Pengendali wajib memberi tahu subjek data SEBELUM informasi pemrosesan berubah (Pasal 21 ayat (2)).
      Saran : Ganti: "Perubahan akan kami umumkan paling lambat [isi: 7] hari sebelum berlaku."

CATATAN:
  - Teks sangat pendek (100 kata). Kebijakan privasi yang memadai biasanya > 400 kata.
  - Info: tidak ada kontak PPDP/DPO. Wajib hanya bila memenuhi Pasal 53 (layanan publik, pemantauan skala besar, atau data spesifik skala besar); UMKM biasa cukup narahubung.

⚠ Pemeriksa bantu berbasis kata kunci, bukan penilaian hukum. Kata kunci yang ditemukan belum tentu isinya memadai.
```

**Pemeriksaan manual tambahan (checklist bagian C):** menyebut GDPR (disalin dari luar negeri); klaim "100% aman"; tidak ada nama pemilik/alamat; tidak jelas apakah memakai layanan asing. Kesimpulan: **tulis ulang** memakai mode SUSUN; kalimat pengganti siap tempel:
- "Dengan menggunakan website ini, Anda dianggap telah menyetujui..." → "Kebijakan ini menjelaskan cara Toko Sejahtera Abadi mengelola data pribadi Anda. Untuk promo, kami meminta persetujuan terpisah yang dapat Anda tarik kapan saja."
- "...dibagikan kepada mitra bisnis kami dan pihak ketiga mana pun..." → "Kami tidak menjual data pribadi Anda. Data hanya kami bagikan kepada kurir [isi], penyedia pembayaran [isi], dan penyedia layanan [isi] untuk memproses pesanan."
- "...100% aman. Namun kami tidak bertanggung jawab atas kebocoran..." → "Kami membatasi akses data dan memakai verifikasi dua langkah. Jika terjadi kebocoran, kami memberi tahu Anda secara tertulis paling lambat 3×24 jam."
- "Dapat diubah sewaktu-waktu tanpa pemberitahuan" → "Perubahan kami umumkan paling lambat 7 hari sebelum berlaku."

## Catatan pembuat
- Deteksi negasi bekerja: "Kami **tidak menjual** data" tidak ditandai; "diubah … **tanpa** pemberitahuan" dan "tidak bertanggung jawab atas **kebocoran**" tidak dihitung sebagai unsur terpenuhi.
- Keterbatasan: pemeriksa berbasis kata kunci; draf yang menyebut unsur secara tidak lazim bisa terlewat. Penilaian akhir tetap oleh agent.
