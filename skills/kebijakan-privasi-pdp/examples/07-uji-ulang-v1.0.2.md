# 07 — Uji ulang independen v1.0.2 (penguji ke-3)

- **Tanggal:** 2026-09-25 · **Penguji:** agent independen (bukan pembuat/perevisi/penguji sebelumnya) · simulasi agent Claude Code
- **Lokasi uji:** salinan skill di scratchpad (`uji3-pdp/skill`), bukan di repo.
- **Anti-overfitting:** seluruh set di bawah (44 kalimat + 2 dokumen + label unsur) ditulis & disimpan **sebelum** membuka `scripts/`, `tests/`, `examples/`, bahkan sebelum membaca SKILL.md. Tidak ada penyetelan setelahnya.

## 1. Set buta A — 44 kalimat berlabel

Komposisi: 22 berisiko, 14 patuh, 8 netral (termasuk jebakan kata "jual", "selamanya", "pihak ketiga"). ID & EN; gaya formal hukum, santai UMKM, terjemahan mesin, kalimat majemuk panjang, pasif, eufemisme, negasi ganda. "Terdeteksi" = `risiko` JSON tidak kosong.

| ID | Label | Gaya | Kalimat | Script | Hasil |
|---|---|---|---|---|---|
| B01 | berisiko | formal hukum ID | Pengendali Data berhak mengalihkan, memindahtangankan, dan/atau mengkomersialisasikan basis data Pelanggan kepada pihak mana pun tanpa pemberitahuan terlebih dahulu. | SEDANG:kepada pihak mana pun | OK |
| B02 | berisiko | santai UMKM | Nomor WA kakak nanti kita titip juga ke partner jualan kita ya biar promonya makin banyak hehe. | - | SALAH | |
| B03 | berisiko | eufemisme | Kami dapat memonetisasi wawasan yang diperoleh dari profil Anda bersama mitra strategis kami. | - | SALAH | |
| B04 | berisiko | pasif | Data yang telah dikumpulkan akan disimpan untuk selamanya dan tidak akan dihapus. | TINGGI:disimpan untuk selamanya | OK |
| B05 | berisiko | negasi ganda | Tidak ada ketentuan yang melarang kami untuk tidak memberitahukan Anda apabila terjadi kebocoran data. | TINGGI:tidak memberitahukan anda apabila terjadi kebocoran | OK |
| B06 | berisiko | formal hukum ID | Pengguna dengan ini melepaskan segala hak untuk menuntut Perusahaan atas kebocoran, kehilangan, atau penyalahgunaan data pribadi dalam bentuk apa pun. | - | SALAH | |
| B07 | berisiko | persetujuan diam | Dengan tetap membuka halaman ini, Anda dianggap menyetujui seluruh pemrosesan data termasuk data kesehatan dan biometrik. | TINGGI:dianggap menyetujui | OK |
| B08 | berisiko | terjemahan mesin | Kami boleh berbagi informasi pribadi Anda dengan pihak ketiga untuk tujuan apa pun yang kami anggap sesuai. | SEDANG:untuk tujuan apa pun | OK |
| B09 | berisiko | kalimat majemuk panjang | Untuk meningkatkan layanan, dan mengingat perkembangan bisnis kami yang dinamis, kami dapat sewaktu-waktu mengubah tujuan pemrosesan data Anda tanpa meminta persetujuan ulang dan perubahan tersebut berlaku segera sejak diputuskan oleh manajemen. | - | SALAH | |
| B10 | berisiko | santai UMKM | Foto KTP yang dikirim buat daftar member kita simpen aja terus di HP admin, jaga-jaga kalau perlu. | - | SALAH | |
| B11 | berisiko | anak | Anak-anak berusia 10 tahun ke atas dapat langsung mendaftar dan mengisi data dirinya sendiri tanpa perlu izin orang tua. | - | SALAH | |
| B12 | berisiko | transfer luar negeri | Data Anda dapat dipindahkan ke server di negara mana pun tanpa jaminan perlindungan yang setara. | - | SALAH | |
| B13 | berisiko | hak dihapus | Permintaan penghapusan data tidak dapat dilayani dalam keadaan apa pun. | - | SALAH | |
| B14 | berisiko | EN formal | We may sell, rent, or lease your personal information to third parties. | TINGGI:sell, rent, or lease your personal information | OK |
| B15 | berisiko | EN casual | Heads up: we pass your contact list to our ad buddies so they can reach out to you directly. | - | SALAH | |
| B16 | berisiko | EN passive | Personal data collected through the app will be retained indefinitely. | TINGGI:retained indefinitely | OK |
| B17 | berisiko | EN legal | The Company shall bear no liability whatsoever for any unauthorized access to or disclosure of User data. | - | SALAH | |
| B18 | berisiko | EN implied consent | Your continued silence after receiving this notice shall constitute consent to the processing of your sensitive data. | TINGGI:silence after receiving this notice shall constitute consent | OK |
| B19 | berisiko | EN euphemism | We may share aggregated and individual-level insights about you with our data partners for their own marketing. | SEDANG:share aggregated and individual-level insights about you with our data partners for their own marketing | OK |
| B20 | berisiko | lokasi terus-menerus | Aplikasi akan terus merekam lokasi Anda di latar belakang meskipun aplikasi tidak digunakan, dan fitur ini tidak dapat dimatikan. | - | SALAH | |
| B21 | berisiko | penarikan persetujuan | Persetujuan yang telah diberikan bersifat final dan tidak dapat ditarik kembali. | - | SALAH | |
| B22 | berisiko | santai UMKM eufemisme | Data pembeli juga kami bantu salurkan ke rekan bisnis yang butuh database, lumayan buat nambah pemasukan toko. | - | SALAH | |
| P01 | patuh | formal | Kami tidak menjual, menyewakan, atau memperdagangkan data pribadi Anda kepada pihak mana pun. | SEDANG:kepada pihak mana pun | SALAH |
| P02 | patuh | formal | Anda dapat menarik kembali persetujuan kapan saja dengan menghubungi kami melalui email privasi@contoh.id, dan penarikan tidak memengaruhi pemrosesan sebelumnya. | - | OK | |
| P03 | patuh | retensi | Data transaksi kami simpan selama 10 tahun sesuai kewajiban pembukuan, lalu dihapus atau dianonimkan. | - | OK | |
| P04 | patuh | kebocoran | Jika terjadi kegagalan pelindungan data pribadi, kami akan memberitahukan Anda secara tertulis paling lambat 3 x 24 jam. | - | OK | |
| P05 | patuh | anak | Layanan ini tidak ditujukan bagi anak; pendaftaran pengguna di bawah umur memerlukan persetujuan orang tua atau wali. | - | OK | |
| P06 | patuh | negasi ganda patuh | Tidak ada data yang kami bagikan kepada pihak ketiga tanpa persetujuan Anda, kecuali diwajibkan oleh peraturan perundang-undangan. | - | OK | |
| P07 | patuh | santai UMKM | Nomor WA kakak cuma kami pakai buat konfirmasi pesanan dan kirim resi, nggak kami kasih ke siapa-siapa. | - | OK | |
| P08 | patuh | EN | We do not sell your personal data, and we never share it with advertisers. | - | OK | |
| P09 | patuh | EN | You may request access to, correction of, or deletion of your personal data at any time, and we will respond within 3 x 24 hours. | - | OK | |
| P10 | patuh | EN transfer | Where data is transferred outside Indonesia, we ensure the recipient country or recipient provides an equal or higher level of protection. | - | OK | |
| P11 | patuh | pasif | Data kesehatan pasien hanya diproses setelah persetujuan tertulis diberikan dan dibatasi untuk keperluan perawatan. | - | OK | |
| P12 | patuh | kalimat panjang | Apabila tujuan pemrosesan berubah, kami akan memberitahukan Anda terlebih dahulu dan meminta persetujuan baru sebelum data digunakan untuk tujuan tersebut. | - | OK | |
| P13 | patuh | EN legal | The Company shall not disclose User data to any third party except processors bound by written agreements, or as required by law. | - | OK | |
| P14 | patuh | kontak | Pertanyaan tentang data pribadi dapat dikirim ke petugas pelindungan data kami di dpo@tokocontoh.id. | - | OK | |
| N01 | netral | umum | Toko kami buka setiap hari Senin sampai Sabtu pukul 08.00-17.00 WIB. | - | OK | |
| N02 | netral | umum | Kebijakan ini berlaku sejak 1 Oktober 2026. | - | OK | |
| N03 | netral | EN | This policy explains how we handle information on our website. | - | OK | |
| N04 | netral | umum | Pengiriman dilakukan melalui kurir JNE, J&T, dan SiCepat. | - | OK | |
| N05 | netral | jebakan kata jual | Kami menjual kue kering dan kue basah untuk acara keluarga. | - | OK | |
| N06 | netral | jebakan kata selamanya | Pelanggan setia adalah sahabat kami selamanya. | - | OK | |
| N07 | netral | EN jebakan | We sell handmade leather bags and ship worldwide. | - | OK | |
| N08 | netral | jebakan pihak ketiga | Pembayaran diproses oleh pihak ketiga penyedia gerbang pembayaran berlisensi Bank Indonesia. | - | OK | |

**Hasil script (`cek_kebijakan.py` v1.0.2):**

| Metrik | Nilai |
|---|---|
| Akurasi keseluruhan | **30/44 (68%)** |
| Recall frasa berisiko | **9/22 (41%)** — 13 salah-negatif |
| Presisi | 9/10 (90%) — 1 salah-positif |
| Patuh/netral benar | 21/22 (95%) |

**Salah-negatif (13):** B02 titip nomor ke partner jualan (santai) · B03 "memonetisasi wawasan" · B06 "melepaskan segala hak untuk menuntut" (padahal ada di checklist B!) · B09 ubah tujuan tanpa persetujuan ulang · B10 simpan foto KTP terus · B11 anak 10 th daftar tanpa izin ortu · B12 pindah ke negara mana pun tanpa jaminan · B13 penghapusan tidak dilayani · B15 "pass your contact list to our ad buddies" · B17 "bear no liability whatsoever for … disclosure" · B20 lokasi latar belakang tak bisa dimatikan · B21 "persetujuan bersifat final dan tidak dapat ditarik kembali" (padahal ada di checklist B!) · B22 "salurkan ke rekan bisnis … nambah pemasukan".

**Salah-positif (1):** P01 "Kami **tidak** menjual, menyewakan, atau memperdagangkan data pribadi Anda kepada pihak mana pun." → SEDANG `kepada pihak mana pun`. Negasi di awal kalimat tidak dipakai untuk pola "pihak mana pun" — varian T-1 yang kambuh, dan justru kalimat yang disarankan skill sendiri.

**Pola kegagalan:** script hanya menangkap frasa yang mirip daftar kata kuncinya. Parafrasa sederhana dengan makna sama ("final dan tidak dapat ditarik kembali" vs "tidak dapat ditarik"; "melepaskan segala hak untuk menuntut" vs "melepaskan hak menuntut") lolos. Kategori yang sama sekali tidak ada polanya: pembatasan hak hapus, anak tanpa izin wali, transfer LN tanpa jaminan, perubahan tujuan, pelacakan lokasi, eufemisme penjualan ("salurkan", "kolaborasikan", "monetisasi wawasan").

## 2. Set buta B — 2 dokumen utuh berlabel

### Dok A — `Madu Hutan Nusantara` (ID, UMKM, 174 kata)
Label risiko: R1 "daftar kontak pelanggan … kami kolaborasikan dengan jaringan UMKM binaan" (berbagi untuk pemasaran pihak lain) · R2 "Foto KTP reseller kami arsipkan tanpa batas waktu" · R3 "Dengan melakukan chat … dianggap telah menyetujui … termasuk menerima promo" · R4 "tidak bertanggung jawab jika terjadi kebocoran akibat peretasan" · R5 swafoto + KTP untuk reseller (data berlebih, manual).
Script: skor 40, KURANG LENGKAP. Risiko tertangkap **R3, R4 (2/4 kalimat)**; R1 & R2 lolos. Unsur 12/14 benar (salah: hak koreksi "boleh minta data Anda diperbaiki" tidak terbaca; cara ajukan via WA dianggap TIDAK ADA). Catatan transfer LN hanya menyebut WhatsApp, tidak Google Sheets.

### Dok B — `SehatPrima Physiotherapy` (EN, klinik, data kesehatan, 201 kata)
Label risiko: R1 "made available to our affiliates and business partners to support the development of their wellness products" · R2 "Progress photos may be used in our social media testimonials unless you object in writing" (opt-out data kesehatan) · R3 "deletion … at the Clinic's sole discretion" · R4 "patients under 18 may register themselves" · R5 hosting Singapura tanpa jaminan setara.
Script: skor 59, KURANG LENGKAP, **"FRASA BERISIKO: tidak ditemukan" (0/5)**. Unsur 12/16 benar — salah: identitas TIDAK ADA (padahal "SehatPrima Physiotherapy ("the Clinic"), Jl. Merdeka 21"), tujuan TIDAK ADA (padahal "Purpose: …"), penerima TIDAK ADA (padahal ada butir Sharing), transfer LN ADA hanya karena kata "Singapore" tanpa menilai jaminan. Hak hapus dihitung ADA walau dibatasi diskresi.

**Total dokumen:** risiko 2/9 kalimat berlabel tertangkap script; unsur 24/30 (80%).

## 3. Uji alur skill (mode CEK sebagai agent)

Yang diperintahkan SKILL.md Mode 3: (1) jalankan script, (2) "Baca juga isinya secara manual dengan `references/checklist-uu-pdp.md` bagian C … kalimat berbagi data yang tidak lazim tetap harus dibaca manual", (3) laporkan skor, tabel unsur, frasa berisiko, usulan teks.

**Penilaian:**
- (+) Ada perintah membaca manual, dan batasan menyebut script "pemeriksa kata kunci". Agent yang teliti (penguji ini) dengan mengikuti langkah 2 menangkap semua R1–R5 di kedua dokumen, plus: dokumen B tanpa versi Bahasa Indonesia, tanpa cara ajukan hak & 3×24 jam, tanpa cara tarik persetujuan.
- (−) Tetapi alur **tidak memastikan** hal itu:
  1. Urutan script → manual + format output "Frasa berisiko: [tingkat] "kutipan"" membuat agent cenderung menyalin daftar script. Untuk Dok B script mencetak "FRASA BERISIKO: tidak ditemukan" — agent yang menyalinnya akan melaporkan klinik yang **membagikan data kesehatan ke mitra bisnis** sebagai tanpa frasa berisiko.
  2. Checklist C yang dirujuk tidak mencakup kategori yang terlewat (pembatasan hak, anak mendaftar sendiri, opt-out untuk data spesifik/foto, transfer LN tanpa jaminan, retensi eufemistis "arsipkan tanpa batas waktu", eufemisme berbagi/monetisasi, data berlebih). Penguji ini menangkapnya karena membaca bebas, bukan karena checklist.
  3. Tidak ada perintah mengoreksi status unsur script yang salah (Dok B: identitas/tujuan/penerima "TIDAK ADA" padahal ada) → tabel unsur ke pengguna bisa keliru dan usulan perbaikan meminta menambah hal yang sudah ada.
  4. Output script sendiri tidak memperingatkan bahwa "tidak ditemukan" ≠ aman.
- **Keterbatasan simulasi:** penguji juga penulis label, jadi keberhasilan agent di atas adalah batas atas. Agent yang tidak tahu labelnya kemungkinan besar tetap menangkap R3/R4 Dok A (sudah dari script) tetapi berisiko melewatkan R1 Dok A dan R1–R3 Dok B bila menyalin script.

**Ringkasan keluaran agent (mengikuti SKILL.md + baca manual), Dok B:**
Skor 59/100 · KURANG LENGKAP · Frasa berisiko (manual): 4 TINGGI (R1 berbagi data kesehatan ke mitra untuk produk mereka — Ps. 16, 20, 22, 65; R2 foto perkembangan pasien untuk testimoni dengan opt-out — data kesehatan wajib persetujuan eksplisit; R3 hak hapus "sole discretion" — Ps. 8, 43; R4 anak < 18 daftar sendiri — Ps. 25), 1 SEDANG (R5 Singapura tanpa jaminan — Ps. 56). Unsur dikoreksi manual: identitas/tujuan/penerima ADA. Tambahan: tanpa versi ID, tanpa cara ajukan & 3×24 jam, tanpa tarik persetujuan & keberatan; klinik data kesehatan → label "WAJIB DITINJAU KONSULTAN HUKUM".

## 4. Regresi temuan lama

| Temuan | Uji | Hasil |
|---|---|---|
| T-1 negasi "tidak akan dijual"/"tidak dapat dijual" | 2 kalimat | ✅ tidak ditandai — **tetapi** varian P01 ("tidak menjual … kepada pihak mana pun") salah-positif SEDANG |
| T-2 "tidak akan memberi tahu bila bocor" | unsur kebocoran | ✅ TIDAK ADA + risiko TINGGI |
| B-1 "tidak menjual…, tetapi dapat membagikannya ke mitra iklan" / "teruskan kepada agensi iklan" | 2 kalimat | ✅ SEDANG — namun parafrasa "rekan bisnis", "partner jualan", "jaringan UMKM binaan" lolos |
| B-2 "sell or rent aggregated and personal information" / "share … with advertisers" | 2 kalimat | ✅ TINGGI/SEDANG — "ad buddies", "data partners … affiliates" (Dok B) lolos |
| Template kosong ID & EN | 2 file | ✅ 84/100 BELUM SIAP (56 & 40 isian) |
| Usia 13 (EN & ID) | 2 kalimat | ✅ SEDANG |
| Tes bawaan `tests/uji_regresi.py` | — | ✅ LULUS 239 uji (tabel akurasi internal 100% di semua set yang sudah dikenal — bukti set tersebut sudah dipakai menyetel) |

## 5. Kesimpulan
Akurasi nyata script pada teks yang belum pernah dilihat: **recall 41%** (kalimat) dan **2/9** (dokumen); angka 85% sebelumnya dan 100% di tes bawaan mencerminkan set yang sudah dipakai menyetel pola. Script cocok sebagai pemeriksa struktur & penanda awal, **tidak** sebagai penyaring risiko. Keamanan skill bergantung pada pembacaan manual oleh agent, yang saat ini diperintahkan tetapi tidak dipaksa → temuan TINGGI U3-1 (lihat HASIL-UJI.md, "Uji ulang v1.0.2").

## Lampiran — teks lengkap dokumen buta

### Dok A
```markdown
# Kebijakan Privasi Madu Hutan Nusantara

Terakhir diperbarui: 20 September 2026

Madu Hutan Nusantara ("kami") adalah usaha perorangan milik Ibu Sari Lestari, beralamat di Jl. Kenanga No. 5, Bogor. Kami menjual madu hutan secara online lewat WhatsApp dan Instagram.

## Data yang kami kumpulkan
Nama, nomor WhatsApp, alamat pengiriman, dan bukti transfer. Untuk program reseller, kami juga meminta foto KTP dan swafoto sambil memegang KTP.

## Untuk apa data dipakai
Memproses pesanan, mengirim barang, dan menghubungi Anda soal promo.

## Berbagi data
Alamat dan nomor Anda kami berikan ke kurir supaya paket sampai. Selain itu, daftar kontak pelanggan juga kami kolaborasikan dengan jaringan UMKM binaan kami agar pelanggan mendapat penawaran produk lain yang relevan.

## Penyimpanan
Data disimpan di Google Sheets dan HP admin. Foto KTP reseller kami arsipkan tanpa batas waktu sebagai dokumentasi usaha.

## Hak Anda
Anda boleh minta data Anda diperbaiki lewat WhatsApp 0812-0000-1111.

## Persetujuan
Dengan melakukan chat kepada admin, Anda dianggap telah menyetujui kebijakan ini termasuk menerima promo.

## Keamanan
Kami berusaha menjaga data Anda, namun kami tidak bertanggung jawab jika terjadi kebocoran akibat peretasan.
```

### Dok B
```markdown
# Privacy Notice - SehatPrima Physiotherapy Clinic

Effective date: 1 August 2026

SehatPrima Physiotherapy ("the Clinic"), Jl. Merdeka 21, Bandung, processes personal data of patients in accordance with Law No. 27 of 2022 on Personal Data Protection.

1. Data we collect: name, date of birth, phone number, medical history, physiotherapy assessment notes, and progress photos.
2. Purpose: to provide treatment, schedule appointments, and send reminders via WhatsApp.
3. Legal basis: explicit consent for health data; contract performance for scheduling.
4. Sharing: we use a cloud-based clinic management system hosted in Singapore. Data may also be made available to our affiliates and business partners to support the development of their wellness products.
5. Retention: medical records are kept as required by health regulations. Progress photos may be used in our social media testimonials unless you object in writing.
6. Your rights: you may access and correct your data. Requests for deletion will be considered at the Clinic's sole discretion.
7. Children: patients under 18 may register themselves using their own phone number.
8. Security: we apply access controls and encryption. In case of a data breach, the Clinic will notify affected patients within 3 x 24 hours.
9. Contact: privacy@sehatprima.example
```
