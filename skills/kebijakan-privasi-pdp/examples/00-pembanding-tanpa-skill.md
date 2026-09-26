# 00 — Uji A/B: skenario 01 TANPA skill vs DENGAN skill

> Penguji independen, 2026-09-25. Input sama persis dengan `01-toko-fashion-susun-id-en.md` (Kirana Wear: WooCommerce + WA, Midtrans, JNE/J&T, Meta Pixel, GA, hosting Singapura, minta ID+EN).
> **Keterbatasan metode (jujur):** jawaban "tanpa skill" ditulis oleh penguji yang sama sebagai simulasi respons agent umum tanpa membaca skill (tidak ada sesi terpisah yang tersedia). Ada risiko bias; untuk mengurangi, jawaban tanpa skill dibuat "rapi dan wajar" (bukan sengaja buruk) dan kedua versi juga dinilai dengan script yang sama. Output DENGAN skill = draf lengkap di file 01.

## Output TANPA skill (lengkap)
```markdown
# Kebijakan Privasi Kirana Wear

Terakhir diperbarui: 25 September 2026

Kirana Wear ("kami") yang dikelola oleh CV Kirana Busana Nusantara menghormati privasi Anda. Kebijakan Privasi ini menjelaskan bagaimana kami mengumpulkan, menggunakan, dan melindungi informasi pribadi Anda saat Anda mengunjungi kiranawear.id atau menghubungi kami melalui WhatsApp. Kebijakan ini disusun sesuai dengan Undang-Undang Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi.

Dengan menggunakan situs kami, Anda menyetujui pengumpulan dan penggunaan informasi sesuai dengan kebijakan ini.

## 1. Informasi yang Kami Kumpulkan
- Informasi pribadi: nama, alamat email, nomor telepon/WhatsApp, alamat pengiriman.
- Informasi transaksi: detail pesanan dan pembayaran yang diproses melalui Midtrans.
- Informasi teknis: alamat IP, jenis browser, perangkat, dan halaman yang dikunjungi melalui cookie, Meta Pixel, dan Google Analytics.

## 2. Penggunaan Informasi
Kami menggunakan informasi Anda untuk:
- Memproses dan mengirimkan pesanan Anda;
- Berkomunikasi terkait pesanan melalui WhatsApp atau email;
- Mengirimkan informasi promosi dan penawaran (Anda dapat berhenti berlangganan kapan saja);
- Menganalisis penggunaan situs dan meningkatkan layanan kami;
- Menampilkan iklan yang relevan melalui platform Meta.

## 3. Berbagi Informasi
Kami tidak menjual informasi pribadi Anda. Kami dapat membagikan informasi kepada:
- Mitra pengiriman (JNE dan J&T Express) untuk mengirimkan pesanan;
- Penyedia pembayaran (Midtrans) untuk memproses pembayaran;
- Penyedia layanan analitik dan iklan (Google, Meta);
- Pihak berwenang apabila diwajibkan oleh hukum.

## 4. Penyimpanan dan Keamanan Data
Data Anda disimpan pada server hosting yang berlokasi di Singapura. Kami menerapkan langkah-langkah keamanan yang wajar, termasuk enkripsi SSL, untuk melindungi data Anda. Namun, tidak ada metode transmisi melalui internet yang 100% aman. Kami menyimpan data Anda selama diperlukan untuk tujuan yang dijelaskan dalam kebijakan ini atau sebagaimana diwajibkan oleh hukum.

## 5. Cookie
Situs kami menggunakan cookie untuk meningkatkan pengalaman Anda. Anda dapat menonaktifkan cookie melalui pengaturan browser, namun beberapa fitur situs mungkin tidak berfungsi dengan baik.

## 6. Hak Anda
Sesuai UU PDP, Anda berhak untuk:
- Mengakses data pribadi Anda;
- Memperbaiki data yang tidak akurat;
- Meminta penghapusan data;
- Menarik persetujuan pemrosesan data.
Untuk menggunakan hak ini, silakan hubungi kami melalui kontak di bawah.

## 7. Perubahan Kebijakan
Kami dapat memperbarui Kebijakan Privasi ini dari waktu ke waktu. Perubahan akan dipublikasikan di halaman ini.

## 8. Hubungi Kami
Email: [email]
WhatsApp: 0813-0000-1111
Alamat: [alamat]

---
# Privacy Policy — Kirana Wear (English)
Last updated: 25 September 2026
Kirana Wear, operated by CV Kirana Busana Nusantara, respects your privacy. By using our website, you agree to the collection and use of information in accordance with this policy. We collect your name, email, phone/WhatsApp number and delivery address, transaction details processed by Midtrans, and technical data via cookies, Meta Pixel and Google Analytics. We use it to process and deliver orders, communicate with you, send promotions (you may unsubscribe at any time), analyse site usage and show relevant ads. We do not sell your personal information; we share it with JNE and J&T Express, Midtrans, Google and Meta, and authorities when required by law. Your data is stored on servers located in Singapore and protected with SSL encryption. We keep your data as long as necessary. You have the right to access, correct, delete your data and withdraw consent. We may update this policy from time to time. Contact: [email] · WhatsApp 0813-0000-1111.
```

## Hasil script pada output TANPA skill
```
PEMERIKSAAN KEBIJAKAN PRIVASI (UU 27/2022 PDP) — tanpa-skill.md
Skor kelengkapan: 67/100  |  Status: PERLU PERBAIKAN  |  521 kata

UNSUR:
  [v] Identitas pengendali data (nama usaha/pemilik) — ADA
  [v] Kontak yang bisa dihubungi (email/WA/alamat) — ADA
  [v] Jenis data pribadi yang dikumpulkan — ADA
  [v] Tujuan pemrosesan — ADA
  [ ] Dasar pemrosesan (persetujuan, perjanjian, kewajiban hukum, dll.) — TIDAK ADA
  [v] Pihak yang menerima data (kurir, payment gateway, marketplace, cloud, iklan) — ADA
  [ ] Transfer/penyimpanan data di luar negeri — TIDAK ADA
  [ ] Masa simpan (retensi) data — TIDAK ADA
  [v] Hak subjek data (akses, koreksi, hapus, tarik persetujuan) — ADA
  [v] Cara mengajukan permintaan hak & batas waktu tanggapan — ADA
  [v] Langkah keamanan data — ADA
  [ ] Pemberitahuan bila terjadi kebocoran (kegagalan pelindungan data) — TIDAK ADA
  [v] Tanggal berlaku / terakhir diperbarui — ADA
  [ ] Cara memberi tahu perubahan kebijakan — TIDAK ADA

YANG PERLU DITAMBAHKAN:
  1. Sebutkan dasar pemrosesan per tujuan: persetujuan, pelaksanaan perjanjian/pesanan, kewajiban hukum (mis. pajak), atau kepentingan yang sah. [UU 27/2022 Pasal 20 ayat (2) & Pasal 21 ayat (1) huruf a]
  2. Jelaskan apakah data disimpan/diproses di luar Indonesia (mis. Google Drive, Meta/WhatsApp, layanan cloud) dan pelindungannya. [UU 27/2022 Pasal 56]
  3. Tulis berapa lama data disimpan per jenis (mis. data pesanan 10 tahun untuk pembukuan pajak, chat CS 1 tahun) lalu dihapus. [UU 27/2022 Pasal 21 ayat (1) huruf d & f, Pasal 43–44]
  4. Tulis bahwa bila terjadi kegagalan pelindungan data, Anda akan memberi tahu pelanggan secara tertulis paling lambat 3×24 jam. [UU 27/2022 Pasal 46]
  5. Tulis bahwa perubahan akan diberitahukan SEBELUM berlaku (mis. lewat website/WA/email). [UU 27/2022 Pasal 21 ayat (2)]

FRASA BERISIKO:
  - [SEDANG] baris 7: "Dengan menggunakan situs kami, Anda menyetujui pengumpulan dan penggunaan informasi sesuai dengan kebijakan ini."
      Alasan: 'Dengan memakai layanan, Anda setuju' bukan persetujuan eksplisit per tujuan (Pasal 20 & 22). Boleh untuk menyatakan telah membaca kebijakan, bukan sebagai dasar pemrosesan data.
      Saran : Ubah menjadi pemberitahuan ("Kebijakan ini menjelaskan...") dan minta persetujuan terpisah untuk promosi/data spesifik.
  - [SEDANG] baris 30: "Data Anda disimpan pada server hosting yang berlokasi di Singapura. Kami menerapkan langkah-langkah keamanan yang wajar, termasuk enkripsi SSL, untuk melindu..."
      Alasan: Klaim keamanan mutlak menyesatkan dan bertentangan dengan kewajiban menyiapkan penanganan kebocoran (Pasal 46).
      Saran : Ganti dengan langkah keamanan nyata yang dilakukan.
  - [SEDANG] baris 54: "Kirana Wear, operated by CV Kirana Busana Nusantara, respects your privacy. By using our website, you agree to the collection and use of information in accor..."
      Alasan: Browse-wrap consent is not explicit consent per purpose (Art. 20 & 22).
      Saran : Use it only as notice; collect separate opt-in consent.

CATATAN:
  - Teks menyebut layanan 'WhatsApp' yang umumnya menyimpan data di luar Indonesia; jelaskan transfer ke luar negeri (Pasal 56).
  - Info: tidak ada kontak PPDP/DPO. Wajib hanya bila memenuhi Pasal 53 (layanan publik, pemantauan skala besar, atau data spesifik skala besar); UMKM biasa cukup narahubung.

⚠ Pemeriksa bantu berbasis kata kunci, bukan penilaian hukum. Kata kunci yang ditemukan belum tentu isinya memadai.
```
Output DENGAN skill: **100/100**, 0 frasa berisiko, status PERLU DILENGKAPI (15 isian) — lihat file 01.
Catatan: frasa "tidak ada metode … yang 100% aman" pada versi tanpa skill sebenarnya **salah-positif** script (kalimat negasi yang justru jujur), jadi tidak dihitung sebagai kelemahan.

## Penilaian berdampingan (1–5)
| Kriteria | Tanpa skill | Dengan skill | Catatan |
|---|---|---|---|
| Dasar pemrosesan per data (Ps. 20) | 1 | 5 | Tanpa skill: tidak ada; dengan skill: tabel data–tujuan–dasar–masa simpan |
| Persetujuan sah (bukan "dengan menggunakan situs Anda setuju") | 2 | 5 | Tanpa skill memakai browse-wrap di ID & EN |
| Masa simpan konkret | 1 | 4 | "selama diperlukan" vs 10 th (UU KUP), 1 th chat, sampai tarik persetujuan; GA/Pixel masih [isi] |
| Transfer LN (hosting SG, Meta, Google) + Ps. 56 | 3 | 5 | Tanpa skill menyebut Singapura sekilas, tanpa pelindungan/Pasal 56 |
| Hak subjek + cara & tenggat 3×24 jam | 2 | 5 | Tanpa skill 4 hak, tanpa tenggat; dengan skill 8 hak + prosedur + 3×24 jam |
| Pemberitahuan kebocoran 3×24 jam (Ps. 46) | 1 | 5 | Tidak ada vs ada |
| Perubahan diberitahukan sebelum berlaku | 2 | 5 | "dipublikasikan di halaman ini" vs "sebelum berlaku, min. 7 hari" |
| Cookie/pixel dengan pilihan menolak | 2 | 4 | Tanpa skill: "nonaktifkan lewat browser"; dengan skill: opt-in banner (perlu dipastikan teknis) |
| Kejujuran (tidak mengarang) | 4 | 5 | Keduanya pakai placeholder; dengan skill mencantumkan daftar isian & asumsi |
| Versi EN setara | 2 | 5 | Tanpa skill: 1 paragraf ringkas; dengan skill: bagian per bagian + klausul ID berlaku |
| Panduan langkah berikutnya & disclaimer | 1 | 5 | Tanpa skill: tidak ada disclaimer/status PP & lembaga |
| **Total (maks 55)** | **21** | **53** | |
| Skor script | 67/100, 3 frasa SEDANG | 100/100, 0 frasa | |

## Kesimpulan
**Dengan skill jelas lebih baik** (53 vs 21). Nilai tambah utama: pemetaan dasar pemrosesan, masa simpan berbasis aturan, 3×24 jam (hak & kebocoran), transfer LN jujur, persetujuan aktif, dan paket "yang perlu dilengkapi + langkah berikutnya + disclaimer". Bahan sebelum/sesudah untuk README: kalimat "Dengan menggunakan situs kami, Anda menyetujui…" → diganti tabel dasar pemrosesan + banner cookie opt-in.
