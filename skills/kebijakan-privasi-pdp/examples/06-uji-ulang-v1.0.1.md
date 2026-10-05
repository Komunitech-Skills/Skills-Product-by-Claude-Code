# Uji 06 — Uji ulang independen v1.0.1 (Tahap 6 butir 7)

- **Tanggal:** 2026-09-25 · **Penguji:** agent terpisah (bukan pembuat, bukan perevisi) · **Platform:** `claude-code (simulasi agent)`
- **Lokasi uji:** salinan skill di scratchpad `.../scratchpad/uji2-pdp/kebijakan-privasi-pdp/`; semua script dijalankan dari salinan. Script `cek_kebijakan.py` v1.0.1, Python 3 (Linux).
- **Anti-overfitting:** set uji di bawah ditulis penguji **sebelum** membuka `tests/` atau `tests/data/`. Tidak ada kalimat yang disalin dari set uji pertama (§2b–2c HASIL-UJI) maupun dari tes bawaan.
- **Tes bawaan** `tests/uji_regresi.py`: **LULUS 133 uji** (klaim perevisi 45/45 & 13/13 pada set lama terkonfirmasi; set lama ≠ set baru).
- **SKILL.md:** 149 baris (< 300) ✅

## 1. Set uji frasa BARU (48 kalimat, satu kalimat per file, `--format json`, dinilai dari ada/tidaknya entri `risiko`)
Label: **B** = berisiko (harus ditandai) · **P** = patuh (tidak boleh ditandai) · **N** = netral (tidak boleh ditandai).

| # | Label | Kalimat | Hasil script | Nilai |
|---|---|---|---|---|
| f01 | B | Kami tidak menjual data, tetapi dapat membagikannya ke mitra iklan. | – | ❌ FN |
| f02 | B | Data Anda dapat dialihkan kepada pihak lain dengan imbalan. | – | ❌ FN |
| f03 | B | Data pelanggan dapat dimonetisasi untuk mendukung operasional kami. | TINGGI | ✅ |
| f04 | B | Kami bekerja sama dengan pihak ketiga untuk tujuan pemasaran dan dapat memberikan data Anda kepada mereka. | – | ❌ FN |
| f05 | B | Dengan menggunakan situs ini, Anda dianggap telah menyetujui seluruh isi kebijakan ini. | TINGGI | ✅ |
| f06 | B | Data Anda akan kami simpan tanpa batas waktu. | TINGGI | ✅ |
| f07 | B | Kami berhak mengubah kebijakan ini kapan saja tanpa pemberitahuan. | SEDANG | ✅ |
| f08 | B | Kami tidak bertanggung jawab atas kebocoran data dalam bentuk apa pun. | TINGGI | ✅ |
| f09 | B | Sistem kami dijamin 100% aman dari peretasan. | SEDANG | ✅ |
| f10 | B | Database pelanggan kami dapat diperjualbelikan kepada perusahaan rekanan. | TINGGI | ✅ |
| f11 | B | Kami boleh menyewakan daftar kontak pelanggan kepada pengiklan. | TINGGI | ✅ |
| f12 | B | Bukan tidak mungkin kami menjual data Anda kepada mitra. *(negasi ganda = positif)* | – | ❌ FN |
| f13 | B | Informasi pribadi Anda bisa kami bagikan ke pihak ketiga untuk keperluan iklan tanpa persetujuan Anda. | – | ❌ FN |
| f14 | B | Diamnya Anda setelah menerima pesan ini kami anggap sebagai persetujuan. | – | ❌ FN |
| f15 | B | Data pribadi Anda disimpan selamanya di server kami. | TINGGI | ✅ |
| f16 | B | We may sell, rent or lease your personal information to third parties. | TINGGI | ✅ |
| f17 | B | We do not sell your data; however, we may share it with advertising partners for marketing purposes. | SEDANG | ✅ |
| f18 | B | Your personal data may be transferred to third parties in exchange for compensation. | TINGGI | ✅ |
| f19 | B | By continuing to browse, you are deemed to have consented to this policy. | TINGGI + SEDANG | ✅ (dobel) |
| f20 | B | We reserve the right to modify this policy at any time without notice. | SEDANG | ✅ |
| f21 | B | We are not liable for any unauthorized access to your data. | TINGGI | ✅ |
| f22 | B | We may monetize your data through our partners. | TINGGI | ✅ |
| f23 | B | This policy is governed by the GDPR and California Consumer Privacy Act (CCPA). | SEDANG | ✅ |
| f24 | P | Kami tidak menjual, menyewakan, atau memperdagangkan data pribadi Anda. | – | ✅ |
| f25 | P | Data Anda tidak akan pernah dijual kepada siapa pun. | – | ✅ |
| f26 | P | Tidak ada data pelanggan yang kami jual kepada pihak ketiga. | – | ✅ |
| f27 | P | Kami tidak membagikan data Anda kepada mitra iklan tanpa persetujuan eksplisit Anda. | – | ✅ |
| f28 | P | Persetujuan tidak pernah kami anggap diberikan hanya karena Anda mengisi formulir. | – | ✅ |
| f29 | P | Kami tidak akan mengubah kebijakan ini tanpa memberi tahu Anda terlebih dahulu melalui email. | – | ✅ |
| f30 | P | Tidak ada sistem yang 100% aman, tetapi kami menerapkan enkripsi dan pembatasan akses. | – | ✅ |
| f31 | P | Data tidak kami simpan tanpa batas waktu; data dihapus setelah 2 tahun. | – | ✅ |
| f32 | P | Kami tidak pernah tidak meminta persetujuan Anda sebelum mengirim promo. *(negasi ganda)* | – | ✅ |
| f33 | P | Bila terjadi kebocoran, kami tidak akan menyembunyikannya dan akan memberi tahu Anda paling lambat 3x24 jam. | – | ✅ |
| f34 | P | Data Anda dapat diakses, diperbaiki, atau dihapus atas permintaan Anda. | – | ✅ |
| f35 | P | Data Anda dapat dibagikan kepada kurir hanya untuk mengirim pesanan. | – | ✅ |
| f36 | P | We never sell or rent your personal data. | – | ✅ |
| f37 | P | Your information will not be sold, traded or rented to anyone. | – | ✅ |
| f38 | P | We will not share your data with advertisers unless you opt in. | – | ✅ |
| f39 | P | No method of transmission over the internet is 100% secure. | – | ✅ |
| f40 | P | We will notify you before any material change to this policy takes effect. | – | ✅ |
| f41 | N | Toko kami menjual kue kering dan roti. | – | ✅ |
| f42 | N | Kami bekerja sama dengan JNE dan J&T untuk pengiriman. | – | ✅ |
| f43 | N | We sell handmade batik products online. | – | ✅ |
| f44 | N | Pembayaran diproses oleh payment gateway berlisensi Bank Indonesia. | – | ✅ |
| f45 | N | Harga dapat berubah sewaktu-waktu mengikuti harga bahan baku. | – | ✅ |
| f46 | N | Jam operasional toko dapat berubah tanpa pemberitahuan pada hari libur nasional. | SEDANG | ❌ FP |
| f47 | N | Paket data internet tidak termasuk dalam harga layanan. | – | ✅ |
| f48 | N | Pelanggan dapat menjual kembali produk kami sebagai reseller. | – | ✅ |

**Akurasi frasa: 41/48 (85%) · salah-positif 1 (f46) · salah-negatif 6 (f01, f02, f04, f12, f13, f14).**
- Semua 17 kalimat patuh & 7 dari 8 kalimat netral benar → negasi (termasuk negasi ganda f32 dan klausa majemuk f33) kini **andal**; T-1/S-5 tidak kambuh pada kalimat baru.
- Pola kelemahan yang konsisten: **berbagi data untuk iklan/pemasaran dalam Bahasa Indonesia** tidak punya pola (f01, f04, f13), padahal padanan Inggrisnya (f17) tertangkap. Contoh majemuk yang diminta ("tidak menjual…, tetapi dapat membagikannya ke mitra iklan") **lolos**. Juga "dialihkan … dengan imbalan" (f02) lolos, padahal padanan EN (f18) tertangkap.

## 2. Set uji unsur BARU
### 2a. Kalimat tunggal (22 kalimat)
**Benar 20/22.** Yang benar mencakup: identitas "CV … pemilik toko", "Bengkel … milik Bapak Hendra"; transfer LN "server Google Cloud … di Singapura" (ADA) vs "server … di Jakarta, Indonesia" (TIDAK ADA ✅); masa simpan "hapus setelah 12 bulan", "keep order records for 10 years"; "Hubungi kami di 0812… untuk pemesanan kue" → cara mengajukan TIDAK ADA ✅; kebocoran & perubahan yang **dinegasikan** (ID & EN) → TIDAK ADA ✅.
Salah (FN):
- "Data tersebut **kami gunakan untuk** memproses pesanan dan mengirim barang." → *tujuan* TIDAK ADA.
- "Some of our providers store data in the **United States**." → *transfer LN* TIDAK ADA (pola nama negara hanya ID).

### 2b. Tiga dokumen utuh (label ditentukan penguji sebelum menjalankan)
| Dokumen | Label penguji | Hasil script | Unsur benar |
|---|---|---|---|
| **D1** Kedai Kopi Senja — lengkap & patuh (303 kata, susunan kalimat sendiri, bukan dari template skill) | 14 unsur ADA, 0 frasa, CUKUP LENGKAP | 100/100, CUKUP LENGKAP, 0 frasa; "Tidak ada sistem yang 100% aman" tidak ditandai | **14/14** ✅ |
| **D2** Laundry — setengah jadi, 5 `[isi: …]` | identitas & kontak **BELUM DIISI**, penerima/masa simpan/tanggal BELUM DIISI, hak SEBAGIAN, 7 TIDAK ADA, 0 frasa, status BELUM SIAP | 40/100 (struktur 50), **KURANG LENGKAP**; identitas **ADA** (bukti: "kebijakan ini berlaku untuk" — tanpa nama); kontak **ADA** (bukti: kata "whatsapp" dari daftar data "nomor WhatsApp") | **12/14** |
| **D3** Template AS/EN (browse-wrap, "We may sell or rent aggregated and personal information", "share … with … advertisers", CCPA/GDPR, "under the age of 13", "no method … 100% secure") | identitas, dasar, LN, masa simpan, cara, kebocoran, perubahan, anak-ortu = TIDAK ADA; keamanan TIDAK ADA (tak ada langkah nyata); hak SEBAGIAN; risiko: browse-wrap, **jual/sewa**, **berbagi ke pengiklan**, GDPR/CCPA | 44/100 KURANG LENGKAP; unsur sesuai kecuali keamanan = ADA (bukti "security of your data is important"); risiko: browse-wrap SEDANG + 3× GDPR/CCPA SEDANG; **"may sell or rent aggregated and personal information" TIDAK ditandai; "may share … with advertisers" TIDAK ditandai**; "100% secure" jujur tidak ditandai ✅ | **14/15** |

**Akurasi unsur total: 60/65 (92%)** — salah-positif 3 (D2 identitas, D2 kontak, D3 keamanan), salah-negatif 2 (tujuan "kami gunakan untuk", transfer LN "United States").
**Frasa di dokumen D3:** 2 dari 4 risiko nyata terlewat — keduanya justru inti "salinan template luar" (jual data & berbagi ke pengiklan). Status akhir tetap KURANG LENGKAP karena skornya rendah, tetapi laporan script tidak menyebut praktik jual data sama sekali; hanya pembacaan manual agent (checklist C) yang akan menangkapnya.

## 3. Status temuan uji pertama
| Temuan | Cek ulang | Status |
|---|---|---|
| **T-1** "tidak akan dijual"/"tidak dapat dijual" → TINGGI | Kedua kalimat lama + f25, f26, f37 (baru) tidak ditandai | ✅ Beres |
| **T-2** negasi dihitung unsur ADA | "Kami tidak akan memberi tahu … kebocoran" → unsur TIDAK ADA **dan** frasa TINGGI; kalimat baru ID/EN (kebocoran & perubahan) benar | ✅ Beres |
| **S-1** "may sell or rent", "share and sell", memperdagangkan/monetisasi | Kasus lama tertangkap; f16, f22, f03, f10 (baru) tertangkap. **Masih lolos:** kata sisipan ("sell or rent *aggregated and* personal information"), "dialihkan … dengan imbalan", berbagi ke mitra iklan/pemasaran (ID) | ⚠ Sebagian (lihat B-1, B-2) |
| **S-2** template kosong 100/100 | `templates/kebijakan-privasi.md` → 84/100 (struktur 100) · **BELUM SIAP** · 56 isian; versi EN 84/100 BELUM SIAP · 40 isian; SKILL.md menjelaskan skor = struktur | ✅ Beres |
| **S-3** unsur rapuh untuk kalimat ID biasa | Singapura, "menyimpan … selama/hapus setelah", "mencabut persetujuan", "Penggunaan Informasi", "di bawah 18 tahun", "berlaku untuk [nama]", "Hubungi kami di … (pemesanan)" kini benar. Sisa: "kami gunakan untuk", negara dalam EN, dan FP baru (B-3) | ⚠ Sebagian besar beres |
| **S-4** template D klinik | D: layanan & rekam medis berdasar pelaksanaan perjanjian + kewajiban hukum (Ps. 20 (2) b, c); centang hanya untuk tujuan tambahan "boleh dikosongkan — pelayanan tetap diberikan"; PP 33/2026 soal persetujuan eksplisit data kesehatan ditandai PERLU REVIEW. **D-online** (Google Form): tanpa tanda tangan, pilihan "isi langsung di klinik", pertanyaan wajib = pernyataan telah membaca, bukan syarat layanan; timestamp = bukti (Ps. 24); wali untuk < 18 th (Ps. 25). Selaras dengan aturan Mode 2 & langkah 2 Mode 1 | ✅ Beres |
| **S-5** "Tidak ada sistem yang 100% aman" | f30, f39, D1, D3 tidak ditandai; f09 "dijamin 100% aman" tetap SEDANG | ✅ Beres |
| **R-1** kinerja kuadratik / daftar tak terbatas | 2 MB penuh frasa berisiko: **1,97 dtk**, 60 temuan (maks. 20/pola) + catatan; 5,7 MB → GALAT batas 5 MB, exit 2 | ✅ Beres |
| **R-2** HTML mentah | `<b>dapat</b> menjual` & `dapat&nbsp;menjual` tertangkap; isi `<script>` dibuang; 11 kata (tag tidak dihitung) | ✅ Beres |
| **R-3** UTF-16 tanpa BOM | UTF-16-LE & UTF-16-BE tanpa BOM terbaca, frasa tertangkap | ✅ Beres |
| **R-4** rujukan pasal identitas/kontak | Identitas: Ps. 5 (kejelasan identitas) & Ps. 21 (1); kontak: Ps. 5 & 21 (1) huruf g + narahubung PP 33/2026 "belum diverifikasi" | ✅ Beres (huruf g = hak subjek; penalaran "agar dapat memakai haknya" wajar) |
| **R-5** Ps. 68 PERLU REVIEW | references: 6 th / Rp6 M ✅ | ✅ Beres |
| **R-6** GDPR/CCPA SEDANG vs TINGGI | Script & checklist C sama-sama SEDANG, naik TINGGI bila memuat praktik terlarang | ✅ Beres |
| **R-7** alasan berbahasa Inggris | "We may sell your data…" → alasan & saran berbahasa Indonesia (+ contoh EN) | ✅ Beres |
| **R-8** tenggat terlewat, opsi cepat, pertanyaan data spesifik | SKILL.md: paragraf "Bila tenggat sudah lewat", "cukup jawab no. 1–3", pertanyaan 3 menyebut kesehatan/anak < 18/keuangan/biometrik | ✅ Beres |
| **R-9** CARA-INSTAL.md vs docs/instalasi.md | `scripts/build.py` menulis `docs/instalasi.md` ke ZIP sebagai `CARA-INSTAL.md` → README benar | ✅ Beres |
| Skor 03 salah-positif "cara ajukan" | Kini TIDAK ADA; skor 03 turun 47 → **41** (hitung manual: 5 + 1,5 = 6,5 ÷ 16 = 40,6 → 41 ✅) | ✅ Beres |

## 4. Klaim hukum (web search 2026-09-25)
| Klaim | Hasil | Status |
|---|---|---|
| Identitas pengendali: UU 27/2022 Ps. 5 (hak atas informasi kejelasan identitas…) & Ps. 21 (1) | Ps. 5 cocok (pasal.id). Ps. 21 (1) = informasi wajib bila berdasar persetujuan (legalitas, tujuan, jenis & relevansi, retensi, rincian, jangka waktu, hak subjek); ayat (2) = beri tahu sebelum berubah | ✅ |
| Ps. 68 pemalsuan: maks. 6 tahun dan/atau Rp6 miliar | Tempo, IDN Times, Hukumonline Klinik, pasal.id | ✅ |
| Ps. 46 (1): tertulis ≤ 3×24 jam kepada subjek data **dan** lembaga | pasal.id, Hukumonline, ABNR | ✅ |
| PP 33/2026: ditetapkan & diundangkan 16 Juli 2026, berlaku 16 Jan 2027 | Hukumonline Pro, Justisio, Meridian, depositobpr | ✅ (CNBC menulis "Agustus 2026 disahkan" — minoritas) |
| PP 33/2026 LN 2026 No. 88 | Kini muncul di beberapa ringkasan sekunder; skill tetap menandai PERLU REVIEW & melarang dikutip | ✅ sikap hati-hati tepat |
| Lembaga pengawas belum terbentuk; sementara Kemkomdigi (Ditjen Pengawasan Ruang Digital) | CNBC 16 Sep 2026, Bisnis 13 Sep 2026, Kompas 27 Jul 2026 | ✅ |

## 5. Ulang skenario 03 (cek salinan template luar — toko herbal) mengikuti SKILL.md v1.0.1
Input sama dengan `03-cek-salinan-template-luar.md`. Langkah Mode 3: simpan → script → baca manual checklist C → laporan.

**Keluaran script:** skor **41/100 · KURANG LENGKAP** · 3 TINGGI ("persetujuan dianggap diberikan", "We may sell your data…", "tidak bertanggung jawab atas kebocoran") + 7 SEDANG (browse-wrap, "pihak ketiga mana pun", 3× GDPR/EEA/CCPA, "100% aman", "sewaktu-waktu tanpa pemberitahuan"). Unsur ADA: kontak, jenis, tujuan, penerima, tanggal; hak SEBAGIAN (kurang tarik persetujuan); cara mengajukan kini benar TIDAK ADA; data spesifik (kesehatan) terpicu = TIDAK ADA.

**Laporan agent (ringkas, format Mode CEK):**
```
Skor kelengkapan: 41/100 · Status: KURANG LENGKAP · Frasa berisiko: 3 TINGGI, 7 SEDANG
(Skor mengukur kelengkapan struktur berbasis kata kunci & polaritas kalimat, bukan kebenaran isi.)
Temuan manual (checklist C):
- TINGGI: data keluhan kesehatan dari konsultasi produk = data spesifik (Ps. 4 (2)) tanpa persetujuan eksplisit & pembatasan akses.
- TINGGI (dinaikkan dari SEDANG): salinan GDPR/CCPA sekaligus memuat praktik terlarang (jual data).
- SEDANG: tujuan "keperluan bisnis lainnya" tidak spesifik (Ps. 16 (2)); tidak ada info transfer LN padahal kemungkinan memakai layanan asing (tanyakan).
- Kalimat campuran EN di dokumen berbahasa Indonesia.
Usulan teks perbaikan (siap tempel): kebijakan ini adalah pemberitahuan; promo & data kesehatan hanya dengan persetujuan aktif terpisah; "Kami tidak menjual data pribadi Anda."; penerima spesifik (kurir, payment gateway: [isi]); hak subjek + cara ajukan + 3×24 jam; kebocoran → pemberitahuan tertulis ≤ 3×24 jam; perubahan diumumkan [isi: 7] hari sebelum berlaku; identitas "[isi: nama pemilik/badan usaha] pemilik Toko Herbal Sehat Alami".
Disclaimer: bukan nasihat hukum; UU 27/2022 dicek 25 Sep 2026; PP 33/2026 berlaku 16 Jan 2027; lembaga pengawas belum terbentuk.
```
Hasil: ✅ Lulus. Catatan: identitas dinilai TIDAK ADA padahal judul memuat "Toko Herbal Sehat Alami" (nama toko ada, pemilik/badan usaha tidak) — dapat diterima, agent menjelaskannya. Kalimat "persetujuan dianggap…" muncul dua kali (TINGGI + SEDANG) — duplikasi (B-5).

## 6. Bug / temuan BARU (berprioritas)
### SEDANG
- **B-1 Berbagi data ke mitra iklan/pemasaran (Bahasa Indonesia) tidak terdeteksi.** f01 "…tetapi dapat membagikannya ke mitra iklan", f04 "bekerja sama dengan pihak ketiga untuk tujuan pemasaran dan dapat memberikan data Anda", f13 "bisa kami bagikan ke pihak ketiga untuk keperluan iklan tanpa persetujuan Anda". Padanan EN (f17) tertangkap. Lokasi: `RISIKO` di `scripts/cek_kebijakan.py` (belum ada pola ID untuk bagikan/berikan/serahkan + iklan/pemasaran/pengiklan/mitra iklan). Saran: pola `(bagikan|membagikan|berikan|memberikan|serahkan|menyerahkan)[^.\n]{0,60}(mitra iklan|pengiklan|iklan|pemasaran|promosi pihak)` tingkat SEDANG dengan cek negasi per klausa (agar f27 tetap lolos) + "dialihkan/diserahkan … dengan imbalan" TINGGI (f02). Tambah checklist B baris ID yang setara.
- **B-2 "sell/share" EN dengan kata sisipan lolos di template luar (D3).** "We may sell or rent **aggregated and** personal information to third parties" dan "We may share your personal information with our affiliates, business partners **and advertisers**" tidak ditandai, padahal "sell or rent personal information" tertangkap. Ini inti skenario salinan template luar. Saran: izinkan 0–3 kata sifat sebelum `(personal )?(data|information)` dan cek "advertisers" di mana pun dalam klausa `share … with`.
### RENDAH
- **B-3 Salah-positif unsur pada dokumen setengah jadi:** identitas ADA dari "Kebijakan ini berlaku untuk layanan … kami" (tanpa nama); kontak ADA dari kata "WhatsApp" di daftar data/kanal pesanan ("Kami menerima pesanan lewat WhatsApp") padahal bagian Kontak = `[isi: …]`; keamanan ADA dari "The security of your data is important to us" (tanpa langkah nyata). Saran: identitas butuh kata setelah "berlaku untuk" yang bukan "layanan/situs/kami"; kontak butuh email/nomor/`wa.me`, bukan kata "WhatsApp" saja.
- **B-4 Status vs SKILL.md:** SKILL.md langkah 5 menulis "Selama masih ada `[isi: ...]`, status = BELUM SIAP", tetapi D2 (5 isian, skor 40) berstatus KURANG LENGKAP. Urutan prioritas (KURANG LENGKAP mengalahkan BELUM SIAP) masuk akal, tetapi perlu ditulis di SKILL.md/`--daftar`.
- **B-5 Temuan ganda** untuk satu kalimat browse-wrap (TINGGI "dianggap" + SEDANG "dengan menggunakan…") — gabungkan per kalimat, ambil tingkat tertinggi.
- **B-6 FP/FN kecil:** f46 "Jam operasional … berubah tanpa pemberitahuan" (bukan soal kebijakan) → SEDANG; f12 "Bukan tidak mungkin kami menjual" (negasi ganda) dianggap negasi; f14 "kami anggap sebagai persetujuan" (bentuk aktif) lolos; unsur tujuan "kami gunakan untuk" dan transfer LN "United States" (EN) FN.
- **B-7 Batas usia anak ala COPPA:** "under the age of 13" di template luar tidak diberi catatan bahwa UU PDP memakai anak < 18 tahun (script & checklist C). Saran: tambahkan ke checklist C / catatan script.
- **B-8 (kosmetik) JSON:** unsur `hak_subjek` tidak punya kunci `bukti` (unsur lain punya) — konsumen JSON bisa `KeyError`.

## 7. Ringkasan angka
| Ukuran | Set baru penguji ulang |
|---|---|
| Frasa (48 kalimat) | **41/48 (85%)** · FP 1 · FN 6 |
| Unsur (22 kalimat + 43 unsur di 3 dokumen) | **60/65 (92%)** · FP 3 · FN 2 |
| Risiko di dokumen D3 | 2/4 tertangkap (+ GDPR/CCPA) |
| Tes bawaan | LULUS 133 |
| Kinerja 2 MB penuh risiko | 1,97 dtk |
