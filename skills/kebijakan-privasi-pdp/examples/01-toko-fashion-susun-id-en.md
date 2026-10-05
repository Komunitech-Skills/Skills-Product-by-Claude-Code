# Uji 01 — Toko online fashion (mode SUSUN, ID + EN)

> Penguji independen (bukan pembuat skill), 2026-09-25. Agent membaca hanya folder skill (SKILL.md, templates/, references/). Skill disalin ke scratchpad; script dijalankan dari salinan. Platform: `claude-code (simulasi agent)`.

## Input pengguna
> Kak, bikinin kebijakan privasi buat toko baju muslim aku, **Kirana Wear** (CV Kirana Busana Nusantara). Jualan lewat website kiranawear.id (WooCommerce) sama WA 0813-0000-1111. Bayar pakai Midtrans, kirim JNE & J&T. Di website pasang Meta Pixel dan Google Analytics. Hostingnya di Singapura. Minta versi Indonesia dan Inggris ya.

## Perilaku agent (mengikuti SKILL.md Mode 1)
1. **Saring cakupan:** toko online biasa, tidak ada data spesifik/anak → tidak perlu label "WAJIB DITINJAU KONSULTAN".
2. **Info wajib yang kurang:** email urusan data, alamat, nama penanggung jawab, nama penyedia hosting. Karena pengguna sudah memberi info inti, agent **tidak bertanya ulang**; membuat draf dan menandai `[isi: ...]` (SKILL.md: "Jika pengguna ingin cepat…"). Catatan penguji: SKILL.md tidak tegas kapan harus bertanya vs langsung draf bila hanya sebagian info kurang — agent memilih draf.
3. **Pemetaan data** Pasal 20: pesanan = pelaksanaan perjanjian; promo, GA, Meta Pixel = persetujuan; transaksi = kewajiban hukum (10 th, UU KUP).
4. **Transfer LN:** hosting Singapura + Meta + Google → opsi 5(a), disebut eksplisit "Singapura".
5. Nama penyedia yang disebut pengguna (Midtrans, JNE, J&T, Meta, Google) dipakai; penyedia hosting tidak disebut → `[isi]`. Tidak ada yang dikarang.
6. `cek_kebijakan.py` dijalankan pada kedua versi.

## Output agent (lengkap)

⚠ Draf ini bukan nasihat hukum. Status: **PERLU DILENGKAPI** · Skor cek: **100/100** (ID) · **100/100** (EN)

### Versi Bahasa Indonesia
```markdown
# Kebijakan Privasi Kirana Wear

**Berlaku sejak:** [isi: tanggal mulai berlaku]
**Terakhir diperbarui:** 25 September 2026

Kebijakan Privasi ini menjelaskan data pribadi apa yang kami kumpulkan, untuk apa, kepada siapa data dibagikan, berapa lama disimpan, dan hak-hak Anda. Kebijakan ini disusun dengan mengacu pada Undang-Undang Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP).

## 1. Siapa kami (pengendali data)
Kirana Wear, dikelola oleh CV Kirana Busana Nusantara ("kami"), adalah pengendali data pribadi untuk toko online kiranawear.id dan akun WhatsApp Business kami.
- Penanggung jawab: [isi: nama pemilik/direktur CV]
- Alamat: [isi: alamat usaha]
- Kontak urusan data pribadi: [isi: email] · WhatsApp 0813-0000-1111

## 2. Data pribadi yang kami kumpulkan
**Data yang Anda berikan langsung:**
- Nama, nomor WhatsApp/HP, email, alamat pengiriman, ukuran/catatan pesanan.
- Isi percakapan layanan pelanggan (WhatsApp, email) dan foto produk yang Anda kirim saat retur/keluhan.
- Data akun toko (nama pengguna, kata sandi yang disimpan dalam bentuk tersandi) bila Anda membuat akun.

**Data yang terkumpul otomatis** (website):
- Alamat IP, jenis perangkat & browser, halaman yang dikunjungi, sumber kunjungan, cookie, Meta Pixel, dan Google Analytics.

**Data dari pihak lain:**
- Status pembayaran dari Midtrans (kami tidak menerima nomor kartu lengkap Anda).
- Status & nomor resi pengiriman dari JNE dan J&T Express.

Kami hanya mengumpulkan data yang diperlukan untuk tujuan di bawah ini.

## 3. Tujuan, dasar pemrosesan, dan masa simpan
| Data | Untuk apa | Dasar pemrosesan (UU PDP Pasal 20) | Disimpan berapa lama |
|---|---|---|---|
| Nama, no. WA/HP, email, alamat, detail pesanan | Memproses & mengirim pesanan | Pelaksanaan perjanjian (pesanan Anda) | 10 tahun untuk catatan transaksi (saran — kewajiban pembukuan pajak, UU KUP Pasal 28 ayat (11)) |
| Status pembayaran Midtrans | Mencocokkan pembayaran | Pelaksanaan perjanjian & kewajiban hukum | 10 tahun (saran — pembukuan pajak) |
| Isi chat & email CS, foto retur | Menjawab pertanyaan, keluhan, retur | Pelaksanaan perjanjian / kepentingan yang sah | 1 tahun sejak percakapan terakhir (saran) |
| Data akun toko | Mengelola akun & riwayat belanja | Pelaksanaan perjanjian | Sampai akun Anda hapus, lalu [isi: mis. 30 hari] |
| No. WA, email | Mengirim promo & info produk baru | Persetujuan Anda (bisa ditarik kapan saja) | Sampai Anda menarik persetujuan |
| Data kunjungan (cookie analitik, Google Analytics) | Memahami cara website dipakai | Persetujuan Anda (banner cookie) | [isi: sesuai pengaturan retensi Google Analytics, mis. 14 bulan] |
| Data kunjungan (Meta Pixel) | Mengukur & menampilkan iklan | Persetujuan Anda (banner cookie) | [isi: sesuai pengaturan Meta] |

Setelah masa simpan berakhir atau tujuan tercapai, data kami hapus atau musnahkan, kecuali wajib disimpan lebih lama menurut peraturan perundang-undangan.

## 4. Kepada siapa data dibagikan
Kami **tidak menjual** data pribadi Anda. Data hanya kami bagikan seperlunya kepada:
| Penerima | Data yang diberikan | Tujuan |
|---|---|---|
| Jasa kurir: JNE dan J&T Express | Nama, no. HP, alamat | Mengirim pesanan |
| Payment gateway: Midtrans | Nama, email, no. HP, nominal & data transaksi | Memproses pembayaran |
| Penyedia hosting website: [isi: nama penyedia hosting] (server di Singapura) | Seluruh data di website toko | Menjalankan website WooCommerce |
| Meta Platforms (WhatsApp Business, Meta Pixel) | No. WA, isi chat, data kunjungan website | Layanan pesan & iklan |
| Google (Google Analytics) | Data kunjungan/perangkat | Analisis kunjungan website |
| Instansi berwenang | Sesuai permintaan resmi | Memenuhi kewajiban hukum |

Pihak yang memproses data atas nama kami (prosesor data) wajib menjaga kerahasiaan dan keamanan data sesuai perintah kami.

## 5. Penyimpanan data di luar negeri
Website kami di-hosting di server yang berada di Singapura, dan sebagian layanan yang kami gunakan (WhatsApp/Meta, Meta Pixel, Google Analytics) dapat menyimpan atau memproses data di server di luar Indonesia. Kami memilih penyedia yang memiliki standar pelindungan data yang memadai dan, bila diperlukan, meminta persetujuan Anda sesuai UU PDP Pasal 56.

## 6. Hak Anda
Sesuai UU PDP Pasal 5–13, Anda berhak:
1. Mendapat informasi tentang identitas kami, tujuan, dan dasar pemrosesan data Anda.
2. **Mengakses** dan meminta **salinan** data pribadi Anda.
3. **Memperbaiki**, melengkapi, atau memperbarui data yang salah atau tidak lengkap.
4. **Menghapus** data atau meminta kami mengakhiri pemrosesannya.
5. **Menarik persetujuan** yang pernah Anda berikan (mis. untuk promosi atau cookie iklan).
6. Menunda atau membatasi pemrosesan.
7. Menggugat dan menerima ganti rugi atas pelanggaran pemrosesan data Anda.
8. Memperoleh dan menggunakan data Anda dalam bentuk yang umum dipakai.

## 7. Cara mengajukan permintaan
Kirim permintaan ke [isi: email] atau WhatsApp 0813-0000-1111 dengan menyebut: nama, nomor HP/email yang terdaftar, dan hak yang ingin digunakan. Untuk keamanan, kami dapat meminta verifikasi identitas secukupnya (tanpa meminta foto KTP bila tidak perlu).
Kami menanggapi paling lambat **3×24 jam** sejak permintaan diterima untuk permintaan akses, perbaikan, dan penarikan persetujuan (UU PDP Pasal 30, 32, 40). Bila permintaan tidak dapat dipenuhi (mis. data wajib disimpan untuk pajak), kami menjelaskan alasannya secara tertulis.

## 8. Keamanan data
Kami menjaga data dengan langkah yang wajar, antara lain: [isi: pilih yang benar-benar dilakukan — akses admin WooCommerce dibatasi; kata sandi kuat + verifikasi dua langkah; HTTPS/SSL; plugin & WordPress diperbarui berkala; cadangan data berkala].

## 9. Jika terjadi kebocoran data
Jika terjadi kegagalan pelindungan data pribadi (mis. kebocoran atau akses tanpa izin), kami akan memberi tahu Anda dan lembaga yang berwenang secara tertulis **paling lambat 3×24 jam**, berisi: data apa yang terungkap, kapan dan bagaimana terjadinya, serta langkah penanganan dan pemulihan (UU PDP Pasal 46).

## 10. Cookie dan piksel iklan
Website kami menggunakan cookie yang diperlukan agar keranjang & checkout berjalan, cookie analitik (Google Analytics), dan piksel iklan (Meta Pixel). Cookie analitik dan piksel iklan hanya aktif setelah Anda menyetujuinya melalui [isi: banner cookie]; Anda dapat menolaknya tanpa kehilangan fitur belanja, atau mengubah pilihan kapan saja melalui [isi: tautan pengaturan cookie/pengaturan browser].

## 11. Perubahan kebijakan
Jika kebijakan ini berubah, kami akan memberitahukannya **sebelum** perubahan berlaku melalui website dan WhatsApp, paling lambat [isi: 7] hari sebelumnya.

## 12. Hubungi kami
Pertanyaan tentang kebijakan ini: [isi: email] · WhatsApp 0813-0000-1111 · [isi: alamat].
```

### English version
```markdown
# Privacy Policy — Kirana Wear

**Effective date:** [fill: date]
**Last updated:** 25 September 2026

This Privacy Policy explains what personal data we collect, why, who we share it with, how long we keep it, and your rights, with reference to Indonesian Law No. 27 of 2022 on Personal Data Protection ("PDP Law"). If this English version differs from the Indonesian version, the Indonesian version prevails.

## 1. Who we are (data controller)
Kirana Wear, operated by CV Kirana Busana Nusantara ("we"), is the personal data controller for the online store kiranawear.id and our WhatsApp Business account.
- Person in charge: [fill: name]
- Address: [fill: address]
- Privacy contact: [fill: email] · WhatsApp 0813-0000-1111

## 2. Personal data we collect
- Data you give us: name, WhatsApp/phone number, email, delivery address, size/order notes, customer-service chats, photos sent for returns, store account data (password stored in hashed form).
- Data collected automatically: IP address, device and browser type, pages visited, referral source, cookies, Meta Pixel and Google Analytics.
- Data from others: payment status from Midtrans (we do not receive your full card number); shipment status and tracking numbers from JNE and J&T Express.

## 3. Purposes, legal basis and retention
| Data | Purpose | Legal basis (Art. 20) | Retention |
|---|---|---|---|
| Name, phone, email, address, order details | Process and deliver orders | Performance of a contract | 10 years for transaction records (tax bookkeeping) |
| Midtrans payment status | Match payments | Contract & legal obligation | 10 years (tax bookkeeping) |
| CS chats/emails, return photos | Answer questions, complaints, returns | Contract / legitimate interest | 1 year after the last conversation |
| Store account data | Manage your account | Performance of a contract | Until you delete the account, then [fill: e.g. 30 days] |
| WhatsApp number, email | Promotions and new-product news | Your consent (withdrawable at any time) | Until you withdraw consent |
| Analytics cookies (Google Analytics) | Understand how the website is used | Your consent (cookie banner) | [fill: GA retention setting, e.g. 14 months] |
| Meta Pixel | Measure and show ads | Your consent (cookie banner) | [fill: per Meta settings] |

When the retention period ends or the purpose is fulfilled, we delete or destroy the data unless the law requires us to keep it longer.

## 4. Who we share data with
We **do not sell** your personal data. We share it only as needed with: couriers (JNE, J&T Express), our payment gateway (Midtrans), our web hosting provider ([fill: provider name], servers in Singapore), Meta Platforms (WhatsApp Business, Meta Pixel), Google (Google Analytics) and competent authorities when legally required. Processors acting on our behalf must keep the data confidential and secure.

## 5. Transfers outside Indonesia
Our website is hosted on servers in Singapore, and some providers we use (WhatsApp/Meta, Meta Pixel, Google Analytics) may store or process data on servers outside Indonesia. We use providers with adequate protection and, where required, ask for your consent (Article 56).

## 6. Your rights (Articles 5–13)
You may: obtain information about our processing; access and obtain a copy of your data; correct or update it; request deletion or end of processing; withdraw consent; delay or restrict processing; claim compensation for violations; and obtain and use your data in a commonly used format.

## 7. How to make a request
Contact [fill: email] or WhatsApp 0813-0000-1111 with your name, registered phone/email and the right you want to exercise. We respond within **3×24 hours** for access, correction and consent-withdrawal requests (Articles 30, 32, 40), or explain in writing why a request cannot be fulfilled.

## 8. Security
[fill: only measures actually taken — restricted WooCommerce admin access, strong passwords + two-step verification, HTTPS, regular plugin updates and backups].

## 9. Data breach notification
If a personal data protection failure occurs, we will notify you and the competent authority in writing **within 3×24 hours**, stating what data was exposed, when and how, and the steps taken (Article 46).

## 10. Cookies and ad pixels
We use cookies needed for the cart and checkout, analytics cookies (Google Analytics) and an ad pixel (Meta Pixel). Analytics cookies and the pixel run only after you accept them via [fill: cookie banner]; you can refuse without losing shopping features.

## 11. Changes to this policy
We will announce changes **before** they take effect via our website and WhatsApp, at least [fill: 7] days in advance.

## 12. Contact us
[fill: email] · WhatsApp 0813-0000-1111 · [fill: address]
```

### Yang masih perlu dilengkapi
- Tanggal mulai berlaku · nama penanggung jawab · alamat usaha · email urusan data
- Nama penyedia hosting (server Singapura)
- Masa simpan akun setelah dihapus, retensi Google Analytics & Meta Pixel (cek di pengaturan masing-masing)
- Langkah keamanan yang **benar-benar** dilakukan (bagian 8)
- Nama/tautan banner cookie (bagian 10) dan jumlah hari pemberitahuan perubahan

### Asumsi yang saya pakai
- Catatan transaksi disimpan 10 tahun (saran, kewajiban pembukuan pajak UU KUP Ps. 28 ayat (11)); chat CS 1 tahun (saran).
- Promo lewat WA/email hanya untuk yang setuju; GA & Meta Pixel memakai persetujuan lewat banner cookie.
- Tidak ada data anak/kesehatan; tidak ada chatbot AI (bila ada, tambahkan ke bagian 4 & 5).
- Kartu kredit diproses Midtrans; toko tidak menyimpan nomor kartu lengkap — **mohon dipastikan**.

### Langkah berikutnya
- Pasang tautan kebijakan di footer website, halaman checkout, dan profil WA Business.
- Pasang banner cookie yang benar-benar menahan GA/Meta Pixel sebelum disetujui (plugin consent WooCommerce), atau ubah bagian 10 bila tidak.
- Tambahkan pemberitahuan singkat + centang promo (template A) di checkout, dan pesan salam WA (template B).
- Siapkan email/WA khusus data + log permintaan (template tanggapan hak subjek).
- Cek apakah website wajib mendaftar PSE Lingkup Privat di pse.komdigi.go.id.

_Disclaimer: Disusun otomatis dari informasi Anda, mengacu pada UU 27/2022 (dicek 25 September 2026). PP 33/2026 berlaku 16 Januari 2027; lembaga pengawas PDP belum terbentuk saat pengecekan. Bukan nasihat hukum. Usaha yang memproses data kesehatan, anak, atau keuangan dalam skala besar sebaiknya meminta peninjauan konsultan hukum._

## Keluaran script
```
PEMERIKSAAN KEBIJAKAN PRIVASI (UU 27/2022 PDP) — kebijakan-id.md
Skor kelengkapan: 100/100  |  Status: PERLU DILENGKAPI  |  922 kata

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
  - Masih ada 15 isian kosong (mis. [isi: tanggal mulai berlaku]). Lengkapi sebelum dipublikasikan.
  - Info: tidak ada kontak PPDP/DPO. Wajib hanya bila memenuhi Pasal 53 (layanan publik, pemantauan skala besar, atau data spesifik skala besar); UMKM biasa cukup narahubung.

⚠ Pemeriksa bantu berbasis kata kunci, bukan penilaian hukum. Kata kunci yang ditemukan belum tentu isinya memadai.

PEMERIKSAAN KEBIJAKAN PRIVASI (UU 27/2022 PDP) — kebijakan-en.md
Skor kelengkapan: 100/100  |  Status: PERLU DILENGKAPI  |  716 kata

```

## Penilaian penguji
- ✅ Tidak ada karangan: semua info yang tidak diberikan tetap `[isi]`/`[fill]`.
- ✅ Hosting Singapura disebut eksplisit di bagian transfer LN; dasar pemrosesan per data benar (pixel/GA = persetujuan, bukan "kepentingan sah").
- ✅ Versi EN setara bagian per bagian + klausul "versi Indonesia berlaku".
- ⚠ Script memberi **100/100** meski 15 isian kosong — status "PERLU DILENGKAPI" menyelamatkan, tetapi angka 100 bisa menyesatkan pengguna awam (lihat HASIL-UJI temuan S-2).
- ⚠ Template tidak punya slot untuk menyebut bahwa **pengguna dapat mengajukan keluhan ke lembaga/Kemkomdigi** — praktik baik, tidak wajib.
