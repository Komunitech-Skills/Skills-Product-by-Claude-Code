# Uji 03 — Cek kebijakan privasi hasil salinan template luar negeri (mode CEK)

> Penguji independen, 2026-09-25. `claude-code (simulasi agent)`. Mengikuti SKILL.md Mode 3: simpan teks → `cek_kebijakan.py` → baca manual dengan checklist bagian C → laporan + teks perbaikan.

## Input pengguna
> Tolong cek kebijakan privasi toko herbal aku ini, dulu aku ambil dari template luar terus diterjemahin sebagian. Udah sesuai UU PDP belum?
```markdown
# Kebijakan Privasi Toko Herbal Sehat Alami

Terakhir diperbarui: 1 Maret 2024

Selamat datang di Sehat Alami. Kami menghargai privasi Anda. Dengan menggunakan situs ini, persetujuan dianggap diberikan untuk semua pengumpulan dan penggunaan informasi sebagaimana dijelaskan dalam kebijakan ini.

## Informasi yang Kami Kumpulkan
Kami dapat mengumpulkan nama, alamat email, nomor telepon, alamat pengiriman, riwayat pembelian, serta informasi tentang keluhan kesehatan yang Anda sampaikan saat konsultasi produk. Kami juga mengumpulkan cookie dan data perangkat.

## Bagaimana Kami Menggunakan Informasi
Informasi digunakan untuk memproses pesanan, meningkatkan layanan, mengirimkan materi pemasaran, dan keperluan bisnis lainnya.

## Berbagi Informasi
We may sell your data to trusted partners for marketing purposes. Kami juga dapat membagikan informasi kepada pihak ketiga mana pun yang kami anggap perlu.

## Hak Anda berdasarkan GDPR
Jika Anda penduduk European Economic Area, Anda berhak mengakses, memperbaiki, atau menghapus data Anda. Penduduk California memiliki hak tambahan berdasarkan CCPA.

## Keamanan
Data Anda 100% aman bersama kami. Namun, kami tidak bertanggung jawab atas kebocoran data yang disebabkan pihak ketiga.

## Perubahan
Kami dapat mengubah kebijakan ini sewaktu-waktu tanpa pemberitahuan.

## Kontak
Hubungi kami di halo@sehatalami.example.
```

## Keluaran script (lengkap)
```
PEMERIKSAAN KEBIJAKAN PRIVASI (UU 27/2022 PDP) — salinan.md
Skor kelengkapan: 47/100  |  Status: KURANG LENGKAP  |  178 kata

UNSUR:
  [ ] Identitas pengendali data (nama usaha/pemilik) — TIDAK ADA
  [v] Kontak yang bisa dihubungi (email/WA/alamat) — ADA
  [v] Jenis data pribadi yang dikumpulkan — ADA
  [v] Tujuan pemrosesan — ADA
  [ ] Dasar pemrosesan (persetujuan, perjanjian, kewajiban hukum, dll.) — TIDAK ADA
  [v] Pihak yang menerima data (kurir, payment gateway, marketplace, cloud, iklan) — ADA
  [ ] Transfer/penyimpanan data di luar negeri — TIDAK ADA
  [ ] Masa simpan (retensi) data — TIDAK ADA
  [~] Hak subjek data (akses, koreksi, hapus, tarik persetujuan) — SEBAGIAN (kurang: tarik persetujuan)
  [v] Cara mengajukan permintaan hak & batas waktu tanggapan — ADA
  [ ] Langkah keamanan data — TIDAK ADA
  [ ] Pemberitahuan bila terjadi kebocoran (kegagalan pelindungan data) — TIDAK ADA
  [v] Tanggal berlaku / terakhir diperbarui — ADA
  [ ] Cara memberi tahu perubahan kebijakan — TIDAK ADA
  [ ] Data spesifik (kesehatan, biometrik, keuangan, dll.): perlakuan khusus — TIDAK ADA

YANG PERLU DITAMBAHKAN:
  1. Sebutkan nama usaha/badan usaha dan nama pemilik atau penanggung jawab sebagai pengendali data. [UU 27/2022 Pasal 21 & 31 (pengendali wajib jelas identitasnya)]
  2. Sebutkan dasar pemrosesan per tujuan: persetujuan, pelaksanaan perjanjian/pesanan, kewajiban hukum (mis. pajak), atau kepentingan yang sah. [UU 27/2022 Pasal 20 ayat (2) & Pasal 21 ayat (1) huruf a]
  3. Jelaskan apakah data disimpan/diproses di luar Indonesia (mis. Google Drive, Meta/WhatsApp, layanan cloud) dan pelindungannya. [UU 27/2022 Pasal 56]
  4. Tulis berapa lama data disimpan per jenis (mis. data pesanan 10 tahun untuk pembukuan pajak, chat CS 1 tahun) lalu dihapus. [UU 27/2022 Pasal 21 ayat (1) huruf d & f, Pasal 43–44]
  5. Tuliskan hak-hak berikut dengan bahasa sederhana: mengakses & minta salinan, memperbaiki, menghapus, menarik persetujuan (juga: keberatan atas keputusan otomatis, membatasi pemrosesan, gugat ganti rugi). [UU 27/2022 Pasal 5–13 & Pasal 21 ayat (1) huruf g]
  6. Jelaskan langkah keamanan secara jujur dan umum (akses dibatasi, kata sandi + verifikasi 2 langkah, perangkat terkunci, cadangan). [UU 27/2022 Pasal 35–39]
  7. Tulis bahwa bila terjadi kegagalan pelindungan data, Anda akan memberi tahu pelanggan secara tertulis paling lambat 3×24 jam. [UU 27/2022 Pasal 46]
  8. Tulis bahwa perubahan akan diberitahukan SEBELUM berlaku (mis. lewat website/WA/email). [UU 27/2022 Pasal 21 ayat (2)]
  9. Sebut jelas bahwa data kesehatan/biometrik/keuangan/anak adalah data spesifik, diproses dengan persetujuan eksplisit terpisah dan akses yang lebih ketat. [UU 27/2022 Pasal 4 ayat (2), Pasal 20 & 34 (penilaian dampak bila berisiko tinggi)]

FRASA BERISIKO:
  - [TINGGI] baris 5: "Selamat datang di Sehat Alami. Kami menghargai privasi Anda. Dengan menggunakan situs ini, persetujuan dianggap diberikan untuk semua pengumpulan dan penggun..."
      Alasan: Persetujuan harus eksplisit, tertulis/terekam, untuk tujuan tertentu (Pasal 20 ayat (2) huruf a & Pasal 22). Persetujuan 'dianggap' tidak memenuhi.
      Saran : Ganti dengan kotak centang/balasan "SETUJU" yang aktif dari pelanggan, per tujuan.
  - [TINGGI] baris 14: "We may sell your data to trusted partners for marketing purposes. Kami juga dapat membagikan informasi kepada pihak ketiga mana pun yang kami anggap perlu."
      Alasan: Unlawful disclosure/use of personal data is prohibited (Art. 65) and criminally sanctioned (Art. 67) under Law 27/2022.
      Saran : Remove; state "We do not sell your personal data."
  - [TINGGI] baris 20: "Data Anda 100% aman bersama kami. Namun, kami tidak bertanggung jawab atas kebocoran data yang disebabkan pihak ketiga."
      Alasan: Pengendali tetap bertanggung jawab atas pemrosesan & wajib melindungi data (Pasal 35, 46, 47). Klausul lepas tanggung jawab tidak menghapus kewajiban ini dan merusak kepercayaan.
      Saran : Hapus. Ganti dengan komitmen menjaga keamanan dan memberi tahu paling lambat 3×24 jam bila terjadi kebocoran.
  - [SEDANG] baris 5: "Selamat datang di Sehat Alami. Kami menghargai privasi Anda. Dengan menggunakan situs ini, persetujuan dianggap diberikan untuk semua pengumpulan dan penggun..."
      Alasan: 'Dengan memakai layanan, Anda setuju' bukan persetujuan eksplisit per tujuan (Pasal 20 & 22). Boleh untuk menyatakan telah membaca kebijakan, bukan sebagai dasar pemrosesan data.
      Saran : Ubah menjadi pemberitahuan ("Kebijakan ini menjelaskan...") dan minta persetujuan terpisah untuk promosi/data spesifik.
  - [SEDANG] baris 14: "We may sell your data to trusted partners for marketing purposes. Kami juga dapat membagikan informasi kepada pihak ketiga mana pun yang kami anggap perlu."
      Alasan: Berbagi data tanpa batas penerima & tujuan tidak memenuhi prinsip terbatas dan spesifik (Pasal 16 ayat (2)).
      Saran : Sebutkan penerima secara spesifik (kategori + tujuan).
  - [SEDANG] baris 16: "## Hak Anda berdasarkan GDPR"
      Alasan: Tampaknya disalin dari kebijakan luar negeri (GDPR/CCPA). Hak & kewajiban di Indonesia mengikuti UU 27/2022.
      Saran : Tulis ulang dengan rujukan UU 27/2022 (batas 3×24 jam, pemberitahuan kebocoran, dasar pemrosesan Pasal 20).
  - [SEDANG] baris 17: "Jika Anda penduduk European Economic Area, Anda berhak mengakses, memperbaiki, atau menghapus data Anda. Penduduk California memiliki hak tambahan berdasarka..."
      Alasan: Tampaknya disalin dari kebijakan luar negeri (GDPR/CCPA). Hak & kewajiban di Indonesia mengikuti UU 27/2022.
      Saran : Tulis ulang dengan rujukan UU 27/2022 (batas 3×24 jam, pemberitahuan kebocoran, dasar pemrosesan Pasal 20).
  - [SEDANG] baris 20: "Data Anda 100% aman bersama kami. Namun, kami tidak bertanggung jawab atas kebocoran data yang disebabkan pihak ketiga."
      Alasan: Klaim keamanan mutlak menyesatkan dan bertentangan dengan kewajiban menyiapkan penanganan kebocoran (Pasal 46).
      Saran : Ganti dengan langkah keamanan nyata yang dilakukan.
  - [SEDANG] baris 23: "Kami dapat mengubah kebijakan ini sewaktu-waktu tanpa pemberitahuan."
      Alasan: Pengendali wajib memberi tahu subjek data SEBELUM informasi pemrosesan berubah (Pasal 21 ayat (2)).
      Saran : Ganti: "Perubahan akan kami umumkan paling lambat [isi: 7] hari sebelum berlaku."

CATATAN:
  - Info: tidak ada kontak PPDP/DPO. Wajib hanya bila memenuhi Pasal 53 (layanan publik, pemantauan skala besar, atau data spesifik skala besar); UMKM biasa cukup narahubung.

⚠ Pemeriksa bantu berbasis kata kunci, bukan penilaian hukum. Kata kunci yang ditemukan belum tentu isinya memadai.
```

## Output agent ke pengguna

⚠ Hasil ini bukan nasihat hukum.

**Skor kelengkapan: 47/100 · Status: KURANG LENGKAP · Frasa berisiko: 3 TINGGI, 6 SEDANG** (beberapa baris kena dua pola)

| Unsur | Status | Dasar |
|---|---|---|
| Identitas pengendali | TIDAK ADA (hanya nama toko di judul; tidak ada pemilik/badan usaha/alamat) | Ps. 21 |
| Kontak | ADA (email) — tidak ada WA/alamat | Ps. 21 |
| Jenis data | ADA | Ps. 21 (1) c, e |
| Tujuan | ADA, tetapi "keperluan bisnis lainnya" **terlalu luas** (penilaian manual) | Ps. 16 (2) |
| Dasar pemrosesan | TIDAK ADA | Ps. 20 (2) |
| Penerima | ADA, tetapi isinya bermasalah ("menjual", "pihak mana pun") | Ps. 16, 65 |
| Transfer luar negeri | TIDAK ADA | Ps. 56 |
| Masa simpan | TIDAK ADA | Ps. 21, 43 |
| Hak subjek data | SEBAGIAN — hanya untuk "penduduk EEA"; tarik persetujuan tidak ada | Ps. 5–13 |
| Cara mengajukan & 3×24 jam | Script: ADA · **Penilaian manual: TIDAK ADA** — "Hubungi kami di …" hanya kontak, tanpa prosedur & tenggat | Ps. 30, 32, 40 |
| Keamanan | TIDAK ADA (hanya klaim "100% aman") | Ps. 35–39 |
| Pemberitahuan kebocoran | TIDAK ADA (malah lepas tanggung jawab) | Ps. 46 |
| Tanggal diperbarui | ADA (1 Maret 2024 — sudah lama, sebelum UU PDP berlaku penuh) | Ps. 21 (2) |
| Pemberitahuan perubahan | TIDAK ADA ("tanpa pemberitahuan") | Ps. 21 (2) |
| Data spesifik (keluhan kesehatan) | TIDAK ADA perlakuan khusus | Ps. 4 (2) |

**Frasa berisiko:**
- [TINGGI] "Dengan menggunakan situs ini, persetujuan dianggap diberikan…" → persetujuan harus eksplisit & terekam (Ps. 20, 22) → ganti: *"Kebijakan ini menjelaskan cara kami memproses data Anda. Untuk promosi dan data kesehatan, kami meminta persetujuan terpisah."*
- [TINGGI] "We may sell your data to trusted partners…" → mengungkapkan data secara melawan hukum dilarang (Ps. 65 ayat (2)), ancaman pidana Ps. 67 → ganti: *"Kami tidak menjual data pribadi Anda."*
- [TINGGI] "kami tidak bertanggung jawab atas kebocoran data…" → kewajiban pengendali tidak bisa dilepas (Ps. 35, 46, 47) → ganti dengan komitmen pemberitahuan 3×24 jam.
- [SEDANG] "pihak ketiga mana pun" → sebut penerima spesifik (kurir, payment gateway…).
- [SEDANG] "GDPR", "European Economic Area", "California/CCPA" → salinan luar negeri; **penilaian manual (checklist C): TINGGI** → tulis ulang sesuai UU PDP.
- [SEDANG] "100% aman" → klaim menyesatkan.
- [SEDANG] "diubah sewaktu-waktu tanpa pemberitahuan" → wajib beri tahu sebelum berubah.

**Temuan manual tambahan (checklist C):** keluhan kesehatan pelanggan saat "konsultasi produk" = **data spesifik** tanpa persetujuan eksplisit — risiko TINGGI; kebijakan campur bahasa Inggris; tidak menyebut layanan asing yang kemungkinan dipakai (hosting, WA, Google).

**Usulan teks perbaikan (siap tempel):**
```markdown
## Siapa kami
Sehat Alami dikelola oleh [isi: nama pemilik/badan usaha], [isi: alamat], sebagai pengendali data pribadi. Kontak urusan data: halo@sehatalami.example · WhatsApp [isi: nomor].

## Dasar pemrosesan & masa simpan
| Data | Untuk apa | Dasar | Disimpan |
|---|---|---|---|
| Nama, no. HP, email, alamat, riwayat pembelian | Memproses & mengirim pesanan | Pelaksanaan perjanjian | 10 tahun untuk catatan transaksi (pembukuan pajak) |
| Keluhan kesehatan saat konsultasi produk | Menyarankan produk | Persetujuan eksplisit terpisah (data spesifik, UU PDP Pasal 4 ayat (2)) | [isi: mis. 1 tahun], lalu dihapus |
| Email, no. WA | Promo | Persetujuan Anda (bisa ditarik) | Sampai persetujuan ditarik |

## Berbagi data
Kami tidak menjual data pribadi Anda. Data dibagikan seperlunya kepada kurir [isi], penyedia pembayaran [isi], dan penyedia hosting/aplikasi [isi].

## Penyimpanan di luar negeri
Sebagian layanan yang kami gunakan ([isi: mis. hosting, WhatsApp, Google]) dapat menyimpan data di luar Indonesia; kami memilih penyedia dengan pelindungan memadai sesuai UU PDP Pasal 56.

## Hak Anda & cara mengajukan
Anda berhak mengakses & meminta salinan, memperbaiki, menghapus data, menarik persetujuan, membatasi pemrosesan, dan menggugat ganti rugi (UU PDP Pasal 5–13). Kirim permintaan ke halo@sehatalami.example atau WhatsApp [isi]; kami tanggapi paling lambat 3×24 jam.

## Keamanan & kebocoran
Kami menjaga data dengan [isi: langkah nyata]. Bila terjadi kegagalan pelindungan data, kami memberi tahu Anda dan lembaga berwenang secara tertulis paling lambat 3×24 jam (UU PDP Pasal 46).

## Perubahan
Perubahan kebijakan kami umumkan di website dan WhatsApp paling lambat [isi: 7] hari sebelum berlaku.
```
Tawaran: saya bisa menyusun ulang versi lengkap (mode SUSUN) memakai isi lama yang masih benar.

_Disclaimer: mengacu pada UU 27/2022 (dicek 25 September 2026). PP 33/2026 berlaku 16 Januari 2027; lembaga pengawas PDP belum terbentuk saat pengecekan. Bukan nasihat hukum._

## Verifikasi skor manual (penguji)
Bobot berlaku = 14 unsur (13×1 + hak subjek 2) = 15, + data spesifik (terpicu "kesehatan") 1 = **16**.
Terpenuhi: kontak 1 + jenis 1 + tujuan 1 + penerima 1 + hak subjek 2×3/4 = 1,5 + cara ajukan 1 + tanggal 1 = **7,5**.
Skor = 7,5 ÷ 16 × 100 = 46,875 → dibulatkan **47** ✅ cocok dengan script.

## Penilaian penguji
- ✅ Tiga frasa TINGGI yang diminta terdeteksi semua ("we may sell your data", "persetujuan dianggap diberikan", lepas tanggung jawab); masa simpan kosong terdeteksi; GDPR/CCPA terdeteksi.
- ⚠ **Salah-positif:** "cara mengajukan" dianggap ADA hanya karena "Hubungi kami di …" (pola `hubungi kami (melalui|di|lewat|untuk)`) — agent harus mengoreksi manual.
- ⚠ **Salah-negatif:** tujuan kabur "keperluan bisnis lainnya" tidak ditandai; tingkat GDPR di script SEDANG tetapi checklist C bilang TINGGI (tidak konsisten).
- ⚠ Alasan frasa "We may sell…" ditampilkan dalam bahasa Inggris untuk pengguna Indonesia.
- ℹ Baris yang sama muncul dua kali (TINGGI + SEDANG) — agak berisik, tapi informatif.
