# Uji ulang v1.0.3 — mode CEK dengan set buta baru (penguji independen ke-4, 2026-09-25)

Penguji: agent terpisah dari pembuat, perevisi, dan penguji v1.0.0–v1.0.2. Skill disalin ke scratchpad (`uji4-pdp/`) dan dijalankan dari sana.
Urutan: (1) hanya SKILL.md dibaca → (2) tiga dokumen buta + kunci ditulis **sebelum** membuka `references/`, `scripts/`, `tests/`, `examples/` → (3) alur Mode 3 diikuti persis (baca per kategori K1–K16 → script → selisih → output) → (4) tes bawaan & verifikasi pasal.

**Keterbatasan jujur:** penguji juga penulis kunci, sehingga "pembacaan agent" pada langkah 3 tidak sepenuhnya buta (penguji tahu kalimat mana yang ditanam). Yang diuji secara objektif: (a) apakah setiap risiko tertanam **tercakup** oleh kategori K1–K16 dan bisa dikenali dari definisi/parafrasanya, (b) apakah format & aturan skill mencegah klaim "aman" dan memaksa selisih dijelaskan, (c) recall script mentah. Sebaiknya uji berikutnya memakai dokumen yang ditulis orang lain.

---

## 1. Dokumen buta

### Dokumen A — ID santai (UMKM kopi)
```markdown
# Kebijakan Privasi Kopi Senja Nusantara

Halo kak! Makasih udah belanja di Kopi Senja Nusantara (usaha milik Rina Kartika, Jl. Melati No. 8, Yogyakarta). Di sini kami jelasin data apa aja yang kami catat.

## Data yang kami catat
Nama, nomor WA, alamat kirim, email, dan riwayat belanja kakak. Kalau pakai aplikasi Kopi Senja, kami juga pantau lokasi HP kakak terus selama aplikasi terpasang biar ongkir selalu akurat.

## Buat apa datanya
- Proses dan kirim pesanan kakak.
- Nomor WA kakak dibagikan ke kurir JNE hanya untuk pengantaran paket.
- Info kakak bisa kami manfaatkan bareng rekanan brand kami buat kirim penawaran yang pas sama selera kakak.
- Promo via WA hanya kami kirim kalau kakak balas SETUJU, dan bisa berhenti kapan aja dengan ketik STOP.

## Persetujuan
Dengan order di toko kami, kakak otomatis setuju sama semua isi kebijakan ini ya.

## Keamanan
Kami tidak akan pernah menjual data kakak ke siapa pun. Kalau ada kejadian di luar kendali kami (misalnya server dibobol orang), itu di luar tanggung jawab kami ya kak.

## Penyimpanan
Data disimpan selama masih dibutuhkan usaha kami.

## Member & anak
Anak di bawah umur boleh daftar member sendiri, cukup centang kotak "umur saya cukup".

## Hak kakak
Kakak boleh minta lihat atau ubah data kapan aja lewat WA 0812-0000-1111. Mau hapus data? Chat admin, nanti diproses maksimal 90 hari kerja dan ada biaya admin Rp25.000 per permintaan.

## Kontak
WA 0812-0000-1111 · email halo@kopisenja.example
```

### Dokumen B — EN terjemahan kaku (klinik)
```markdown
# Privacy Policy of Klinik Sehat Prima

Klinik Sehat Prima ("the Clinic"), located at Jl. Kenanga No. 21, Bandung, hereby conveys the Privacy Policy as follows.

## 1. Data Collected
The Clinic collects name, NIK, date of birth, telephone number, address, and medical record including diagnosis, laboratory results and prescription.

## 2. Consent
By continuing to use the services of the Clinic, the Patient is deemed to have agreed to the processing of all personal data including the medical record as described herein.

## 3. Purposes of Use
Personal data is used for providing health services, billing, and appointment reminders. Health information of the Patient may be utilized for research and other purposes which the Clinic deems appropriate from time to time.

The Clinic does not share patient data with advertisers.

## 4. Storage and Transfer
Medical records are retained in accordance with the regulation of the Ministry of Health and thereafter destroyed. Data may be stored on servers of technology partners of the Clinic located abroad.

In the event of corporate action such as merger, acquisition or divestment, data assets may be transferred to the successor entity.

## 5. Security
The systems of the Clinic are fully secured and guaranteed free from any leakage. Notification of any data incident shall be made at the discretion of the Clinic when deemed necessary.

## 6. Rights of the Patient
The Patient may request a copy of the personal data; the Clinic shall respond within 3x24 hours. Requests for correction may be submitted at the front desk.

## 7. Amendment
The Clinic reserves the right to amend this Policy at any time without prior notice, and continued visits shall constitute acceptance of the amended Policy.

## 8. Contact
Email: admin@sehatprima.example · Tel. 022-000-1234
```

### Dokumen C — campuran ID/EN, salinan template SaaS
```markdown
# Kebijakan Privasi / Privacy Policy — KasirKu

Terakhir diperbarui / Last updated: 1 Januari 2026

KasirKu ("kami", "we") adalah aplikasi kasir untuk UMKM yang dikelola PT Kasir Digital Nusantara, Jakarta.

## Information We Collect
We collect your contacts list, SMS, and precise location as required for app functionality. Kami juga mengumpulkan data transaksi toko Anda dan data pelanggan yang Anda input (nama, nomor HP).

## Penggunaan Data
- Menjalankan fitur kasir dan laporan.
- We use anonymized, aggregated statistics to improve the service, which cannot identify you.
- Kami dapat memberikan info pelanggan Anda kepada partner analitik dan periklanan kami untuk membangun profil minat.
- Kami dapat mengkomersialkan data agregat maupun data individual kepada pihak ketiga.

## Pembayaran
Pembayaran diproses oleh payment gateway berizin Bank Indonesia; kami tidak menyimpan nomor kartu.

## Retensi / Retention
Kami menyimpan data transaksi selama 10 tahun sesuai kewajiban pembukuan pajak. Data akun yang dihapus tetap kami simpan dalam arsip untuk keperluan internal tanpa batas waktu.

## Your Rights
Sesuai GDPR dan CCPA, Anda memiliki hak untuk mengakses dan memperbaiki data Anda. California residents may request disclosure of categories of personal information sold. Pengguna tidak dapat menarik kembali persetujuan setelah akun diaktifkan.

## Governing Law
This Policy shall be governed by the laws of the State of Delaware, USA.

## Contact
privacy@kasirku.example
```

---

## 2. Kunci jawaban (ditulis sebelum membuka references/)

21 risiko tertanam + 9 kalimat patuh pengecoh. Kategori K diisi setelah membaca `kategori-risiko-cek.md` (pemetaan saja, kalimat tidak diubah).

| # | Dok | Kalimat (ringkas) | Risiko | K | Script? |
|---|---|---|---|---|---|
| A1 | A | "Dengan order … otomatis setuju sama semua isi kebijakan" | persetujuan tersirat & dibundel | K3 | ✗ |
| A2 | A | "Info kakak bisa kami manfaatkan bareng rekanan brand … penawaran yang pas" | berbagi ke pihak lain untuk pemasaran | K2 | ✗ |
| A3 | A | "Data disimpan selama masih dibutuhkan usaha kami" | masa simpan samar | K7 | ✗ |
| A4 | A | "hapus … maksimal 90 hari kerja dan ada biaya admin Rp25.000" | syarat hak berlebihan (waktu & biaya) | K9 | ✗ |
| A5 | A | "pantau lokasi HP kakak terus selama aplikasi terpasang" | lokasi terus-menerus, tak bisa dimatikan | K12 | ✗ |
| A6 | A | "server dibobol … di luar tanggung jawab kami" | lepas tanggung jawab kebocoran | K8 | ✗ |
| A7 | A | "Anak di bawah umur boleh daftar member sendiri, cukup centang" | anak tanpa izin wali | K10 | ✗ |
| B1 | B | "By continuing … deemed to have agreed … including the medical record" | persetujuan tersirat untuk data kesehatan | K3+K11 | ✓ |
| B2 | B | "Health information … utilized for research and other purposes which the Clinic deems appropriate" | tujuan tak terbatas, data spesifik | K4+K11 | ✗ |
| B3 | B | "corporate action … data assets may be transferred to the successor entity" | pengalihan tanpa pemberitahuan | K5 | ✗ |
| B4 | B | "stored on servers of technology partners … located abroad" | transfer LN tanpa jaminan (data kesehatan) | K6 | ✗ |
| B5 | B | "amend … without prior notice … continued visits constitute acceptance" | perubahan sepihak + persetujuan tersirat | K13 | ✓ |
| B6 | B | "Notification of any data incident … at the discretion of the Clinic when deemed necessary" | pemberitahuan kebocoran diskresi | K8 | ✗ |
| B7 | B | "fully secured and guaranteed free from any leakage" | klaim keamanan mutlak | K15 | ✓ |
| C1 | C | "mengkomersialkan data agregat maupun data individual kepada pihak ketiga" | monetisasi data | K1 | ✓ |
| C2 | C | "governed by the laws of the State of Delaware, USA" | hukum asing | K14 | ✗ |
| C3 | C | "tidak dapat menarik kembali persetujuan setelah akun diaktifkan" | menghapus hak tarik persetujuan | K9 | ✗ |
| C4 | C | "contacts list, SMS, and precise location as required for app functionality" (aplikasi kasir) | data berlebih/akses perangkat | K12 | ✗ |
| C5 | C | "info pelanggan … kepada partner analitik dan periklanan … profil minat" | berbagi untuk iklan/profiling | K2 | ✓ |
| C6 | C | "Sesuai GDPR dan CCPA …" / "California residents … sold" | salinan template luar, UU PDP tak disebut | K16 (+K14) | ✓ (C-CCPA salah dikategorikan K1) |
| C7 | C | "Data akun yang dihapus tetap kami simpan … tanpa batas waktu" | masa simpan tak terbatas | K7 | ✓ |

**Kalimat patuh pengecoh (harus TIDAK ditandai):** A-P1 "tidak akan pernah menjual data kakak ke siapa pun"; A-P2 "Nomor WA … dibagikan ke kurir JNE hanya untuk pengantaran"; A-P3 "Promo via WA hanya kalau kakak balas SETUJU … ketik STOP"; B-P1 "Medical records are retained in accordance with the regulation of the Ministry of Health and thereafter destroyed"; B-P2 "request a copy … respond within 3x24 hours"; B-P3 "does not share patient data with advertisers"; C-P1 "data transaksi selama 10 tahun sesuai kewajiban pembukuan pajak"; C-P2 "payment gateway berizin Bank Indonesia; kami tidak menyimpan nomor kartu"; C-P3 "anonymized, aggregated statistics … cannot identify you".

---

## 3. Output skill ke pengguna (alur Mode 3 diikuti persis)

### 3A. Dokumen A — Kopi Senja Nusantara

```
Ringkasan: 5 TINGGI, 3 SEDANG temuan dari pembacaan per kategori · Skor kelengkapan script: 31/100 (terkoreksi manual ±50) · Status: KURANG LENGKAP

1. Temuan pembacaan (per kategori)
| Kategori | Kutipan kalimat | Tingkat | Risiko & dasar | Perbaikan siap tempel | Script? |
|---|---|---|---|---|---|
| K3 Persetujuan tersirat/dibundel | "Dengan order di toko kami, kakak otomatis setuju sama semua isi kebijakan ini ya." | TINGGI | Persetujuan harus eksplisit, per tujuan, terekam; order hanya dasar "pelaksanaan perjanjian" untuk kirim pesanan (Ps. 20 ayat (2), Ps. 22) | "Data yang diperlukan untuk memproses dan mengirim pesanan kami olah untuk melaksanakan pesanan kakak. Untuk hal di luar itu (promo, testimoni) kami minta persetujuan terpisah yang boleh kakak tolak." | tidak dikenali pola |
| K2 Berbagi untuk pemasaran pihak lain | "Info kakak bisa kami manfaatkan bareng rekanan brand kami buat kirim penawaran yang pas sama selera kakak." | TINGGI | Penerima & tujuan tidak spesifik, tanpa persetujuan aktif (Ps. 16 ayat (2), 20, 21, 22) | Hapus, atau: "Kami tidak membagikan data kakak ke brand/mitra lain untuk promosi mereka. Bila suatu saat ada kerja sama, kami minta persetujuan kakak dulu (balas SETUJU) dan menyebut nama mitranya." | tidak dikenali pola |
| K12 Lokasi tak bisa dimatikan | "…kami juga pantau lokasi HP kakak terus selama aplikasi terpasang biar ongkir selalu akurat." | TINGGI | Ongkir cukup alamat kirim; pelacakan terus-menerus berlebihan & tidak bisa ditolak (Ps. 16 ayat (2) huruf a, Ps. 5–13) | "Aplikasi hanya memakai lokasi saat kakak menekan tombol 'Pakai lokasi saya' untuk mengisi alamat. Izin lokasi bisa dimatikan kapan saja di pengaturan HP; pesanan tetap bisa dibuat dengan mengetik alamat." | tidak dikenali pola |
| K8 Lepas tanggung jawab kebocoran | "Kalau ada kejadian di luar kendali kami (misalnya server dibobol orang), itu di luar tanggung jawab kami ya kak." | TINGGI | Pengendali tetap bertanggung jawab & wajib memberi tahu ≤ 3×24 jam (Ps. 35–39, 46, 47) | "Kami menjaga data dengan akses terbatas untuk admin, kata sandi kuat + verifikasi 2 langkah, dan HP kerja terkunci. Bila terjadi kebocoran, kami memberi tahu kakak dan lembaga berwenang secara tertulis paling lambat 3×24 jam, berisi data yang terdampak, kapan & bagaimana terjadi, serta langkah penanganannya." | tidak dikenali pola |
| K10 Anak tanpa izin wali | "Anak di bawah umur boleh daftar member sendiri, cukup centang kotak 'umur saya cukup'." | TINGGI | Data anak (< 18 th) wajib persetujuan orang tua/wali (Ps. 25; UU 35/2014 Ps. 1 angka 1) | "Pendaftaran member untuk usia di bawah 18 tahun harus dilakukan atau disetujui orang tua/wali. Kami meminta nama dan nomor WA orang tua/wali serta konfirmasi persetujuannya." | tidak dikenali pola |
| K9 Syarat hak berlebihan | "…diproses maksimal 90 hari kerja dan ada biaya admin Rp25.000 per permintaan." | SEDANG→TINGGI (biaya menghambat hak) | Hapus/akhiri pemrosesan wajib dilayani; perbaikan/akses/penarikan ≤ 3×24 jam (hak Ps. 5–13; Ps. 30, 32, 40, 43) | "Kakak bisa minta lihat, perbaiki, atau hapus data, dan menarik persetujuan promo lewat WA 0812-0000-1111 atau email halo@kopisenja.example, gratis. Kami tanggapi paling lambat 3×24 jam. Catatan transaksi tetap kami simpan 10 tahun karena kewajiban pajak." | tidak dikenali pola |
| K7 Masa simpan samar | "Data disimpan selama masih dibutuhkan usaha kami." | SEDANG | Jangka retensi wajib diinformasikan (Ps. 16 ayat (2), 21 ayat (1), 43) | "Catatan transaksi: 10 tahun (kewajiban pembukuan pajak). Chat WA & alamat kirim: [isi: 1 tahun] setelah pesanan terakhir. Data promo: sampai kakak berhenti (STOP). Data member: sampai keanggotaan berakhir." | tidak dikenali pola (script menganggap unsur retensi ADA) |
| K6 Transfer LN tidak disebut | (tidak ada kalimat) — usaha memakai WhatsApp (Meta, server luar negeri) | SEDANG | Ps. 56 | "Kami memakai WhatsApp (Meta) dan [isi: layanan lain] yang dapat menyimpan data di luar Indonesia. Kami hanya memakai penyedia yang menerapkan pelindungan data yang memadai." | script: unsur TIDAK ADA ✓ |
Kategori yang diperiksa tanpa temuan: K1 (kalimat "tidak akan pernah menjual" = patuh), K4, K5, K11, K13, K14, K15, K16. Kalimat patuh yang dinilai aman: berbagi ke kurir JNE "hanya untuk pengantaran"; promo WA dengan SETUJU/STOP.

2. Pemeriksa kedua (script)
Skor 31/100 · Status KURANG LENGKAP — skor = kelengkapan struktur berbasis kata kunci, bukan kebenaran isi.
| Unsur | Status | Dasar |
| Identitas, kontak, jenis data, penerima | ADA | |
| Tujuan pemrosesan | ADA (dikoreksi manual: bagian "Buat apa datanya") | Ps. 16, 21 |
| Dasar pemrosesan | TIDAK ADA | Ps. 20 ayat (2) |
| Transfer LN | TIDAK ADA | Ps. 56 |
| Masa simpan | ADA (isinya bermasalah → K7) | |
| Hak subjek data | SEBAGIAN (dikoreksi manual: lihat/ubah/hapus ada; tarik persetujuan hanya untuk promo) | Ps. 5–13 |
| Cara mengajukan & batas waktu | SEBAGIAN (dikoreksi manual: kanal WA ada; batas 3×24 jam tidak ada, 90 hari → K9) | Ps. 30, 32, 40 |
| Keamanan, kebocoran, tanggal berlaku, cara memberi tahu perubahan, data anak | TIDAK ADA | |
Selisih dengan script: script mencetak "tidak ada pola yang cocok … BUKAN jaminan kebijakan aman"; ke-8 temuan di atas tidak dikenali pola kata kunci (parafrasa santai). Tiga status unsur dikoreksi manual (tujuan, hak, cara mengajukan), sehingga skor terkoreksi lebih tinggi dari 31 (±50), status tetap KURANG LENGKAP.

Usulan teks perbaikan (siap tempel): lihat kolom Perbaikan, ditambah:
- Dasar pemrosesan: "Nama, no. WA, dan alamat kami olah untuk melaksanakan pesanan kakak; catatan transaksi karena kewajiban pajak; promo WA hanya dengan persetujuan kakak."
- Tanggal: "Berlaku sejak: [isi: tanggal] · Terakhir diperbarui: [isi: tanggal]"
- Perubahan: "Bila kebijakan ini berubah, kami umumkan lewat WA/website paling lambat [isi: 7] hari sebelum berlaku."
Tawaran: saya bisa menyusun ulang versi lengkap (Mode SUSUN) memakai isi lama ini.

Disclaimer: Disusun otomatis … mengacu pada UU 27/2022 (dicek 25 September 2026). PP 33/2026 berlaku 16 Januari 2027; lembaga pengawas PDP belum terbentuk saat pengecekan. Bukan nasihat hukum.
```

### 3B. Dokumen B — Klinik Sehat Prima (EN)

```
Ringkasan: 5 TINGGI, 3 SEDANG temuan dari pembacaan per kategori · Skor kelengkapan script: 41/100 (terkoreksi manual ±50) · Status: KURANG LENGKAP · DRAF — WAJIB DITINJAU KONSULTAN HUKUM (data kesehatan)

1. Temuan pembacaan (per kategori)
| Kategori | Kutipan | Tingkat | Risiko & dasar | Perbaikan siap tempel (EN; versi ID wajib disiapkan, UU 24/2009) | Script? |
|---|---|---|---|---|---|
| K3+K11 Persetujuan tersirat untuk data kesehatan | "By continuing to use the services of the Clinic, the Patient is deemed to have agreed to the processing of all personal data including the medical record as described herein." | TINGGI | Data kesehatan = data spesifik (Ps. 4 ayat (2)); "deemed" bukan persetujuan eksplisit (Ps. 20, 22) | "We process your identity data and medical record to provide care and to meet our legal obligation to keep medical records. Any other use (e.g. testimonials, photos, research) requires your separate written consent, which you may refuse without affecting your treatment." | ✓ TINGGI |
| K4+K11 Tujuan tak terbatas | "Health information of the Patient may be utilized for research and other purposes which the Clinic deems appropriate from time to time." | TINGGI | Tujuan harus spesifik; data spesifik (Ps. 16 ayat (2) huruf b, 20, 21 ayat (2), 34) | Delete, or: "Your health information is used only for your care, billing and appointment reminders. We will not use it for research unless you give separate written consent for a specific study, and identifiable data will not be published." | tidak dikenali pola |
| K8 Pemberitahuan kebocoran diskresi | "Notification of any data incident shall be made at the discretion of the Clinic when deemed necessary." | TINGGI | Wajib tertulis ≤ 3×24 jam ke pasien & lembaga (Ps. 46) | "If a personal data breach occurs, we will notify you and the competent authority in writing no later than 3×24 hours, stating the data affected, when and how it happened, and the steps taken to handle and recover." | tidak dikenali pola (script malah menandai unsur kebocoran ADA) |
| K6 Transfer LN tanpa jaminan | "Data may be stored on servers of technology partners of the Clinic located abroad." | TINGGI (data kesehatan) | Ps. 56: negara setara, atau pelindungan memadai & mengikat, atau persetujuan | "Our [fill: system name] provider stores data in [fill: country]. We only use providers bound by a written agreement to protect data at least to the standard of Law 27/2022; where this is not possible, we ask for your consent first." | tidak dikenali pola |
| K5 Pengalihan saat aksi korporasi | "In the event of corporate action such as merger, acquisition or divestment, data assets may be transferred to the successor entity." | SEDANG | UU PDP Ps. 48: pemberitahuan pengalihan kepada subjek data **sebelum dan sesudah** penggabungan/pengambilalihan dsb. | "If the Clinic merges, is acquired or restructured, we will notify you before and after your data is transferred, and the new entity will remain bound by this Policy." | tidak dikenali pola |
| K15 Klaim keamanan mutlak | "The systems of the Clinic are fully secured and guaranteed free from any leakage." | SEDANG | Ps. 35, 46 | "We protect patient data with role-based access, [fill: measures actually used], and staff confidentiality obligations. No system is 100% secure, so we also keep a breach response procedure." | ✓ SEDANG |
| K13 Perubahan sepihak | "The Clinic reserves the right to amend this Policy at any time without prior notice, and continued visits shall constitute acceptance …" | SEDANG | Ps. 21 ayat (2) | "We will announce changes at the front desk and on [fill: channel] at least [fill: 7] days before they take effect." | ✓ SEDANG |
| K9 Hak tidak lengkap | (hapus, tarik persetujuan, keberatan tidak ada; koreksi hanya "at the front desk" tanpa batas waktu) | SEDANG | Ps. 5–13, 30, 40, 43 | "You may access, correct, or request deletion of your data and withdraw consent via admin@sehatprima.example, 022-000-1234 or the front desk. We respond within 3×24 hours. Medical records must be kept for the period required by health regulations and cannot be deleted before then; we will explain this in our reply." | script: SEBAGIAN |
Kategori tanpa temuan: K1, K2 ("does not share patient data with advertisers" = patuh), K7 (retensi rekam medis mengikuti aturan Kemenkes = patuh; sebaiknya sebut masa simpan konkret, lihat catatan), K10, K12, K14, K16.
Catatan: klinik yang memproses data kesehatan dalam skala besar mungkin wajib menunjuk Pejabat PDP (Ps. 53 + Putusan MK 151/PUU-XXII/2024) dan melakukan penilaian dampak (Ps. 34). WAJIB DITINJAU KONSULTAN HUKUM.

2. Pemeriksa kedua (script)
Skor 41/100 · Status KURANG LENGKAP.
| Identitas pengendali | ADA (dikoreksi manual: "Klinik Sehat Prima ("the Clinic"), located at Jl. Kenanga No. 21, Bandung") |
| Hak subjek data | SEBAGIAN (dikoreksi manual: akses ADA — "request a copy"; kurang: hapus, tarik persetujuan) |
| Pemberitahuan kebocoran | ADA menurut script, tetapi isinya bermasalah → K8 |
| Pihak penerima | SEBAGIAN (dikoreksi manual: "technology partners" disebut tanpa nama/tujuan) |
| Dasar pemrosesan, keamanan, tanggal, cara memberi tahu perubahan, perlakuan data spesifik, cara mengajukan & batas waktu | TIDAK ADA |
Selisih dengan script: script menangkap 3 dari 8 temuan (K3, K15, K13); 5 lainnya tidak dikenali pola kata kunci (parafrasa bahasa hukum EN). Identitas & akses dikoreksi manual (jangan tambahkan identitas, sudah ada).

Usulan teks perbaikan: lihat kolom Perbaikan + tambahan "Effective date: [fill]" dan paragraf data spesifik: "Your health data is sensitive (specific) personal data under Law 27/2022. Access is limited to the doctors and staff treating you."
Disclaimer (sama) + WAJIB DITINJAU KONSULTAN HUKUM.
```

### 3C. Dokumen C — KasirKu (campuran ID/EN, template SaaS)

```
Ringkasan: 5 TINGGI, 3 SEDANG temuan dari pembacaan per kategori · Skor kelengkapan script: 57/100 · Status: KURANG LENGKAP

1. Temuan pembacaan (per kategori)
| Kategori | Kutipan | Tingkat | Risiko & dasar | Perbaikan siap tempel | Script? |
|---|---|---|---|---|---|
| K1 Monetisasi | "Kami dapat mengkomersialkan data agregat maupun data individual kepada pihak ketiga." | TINGGI | Ps. 65 ayat (2)–(3), 67, 20 | "Kami tidak menjual, menyewakan, atau memperdagangkan data pribadi Anda maupun data pelanggan Anda. Kami hanya dapat memakai statistik agregat yang telah dianonimkan dan tidak dapat mengidentifikasi siapa pun." | ✓ TINGGI |
| K2 Berbagi untuk iklan/profiling | "Kami dapat memberikan info pelanggan Anda kepada partner analitik dan periklanan kami untuk membangun profil minat." | TINGGI (data pelanggan milik merchant, tanpa persetujuan) | Ps. 16 ayat (2), 20, 21, 22; KasirKu memproses data pelanggan merchant atas perintah merchant (prosesor, Ps. 51) | "Data pelanggan yang Anda masukkan hanya kami proses untuk menjalankan fitur kasir atas perintah Anda. Kami tidak memberikannya kepada pengiklan atau pihak analitik untuk profil iklan." | ✓ SEDANG (tingkat dinaikkan manual) |
| K12 Data berlebih | "We collect your contacts list, SMS, and precise location as required for app functionality." | TINGGI | Aplikasi kasir tidak memerlukan kontak & SMS; lokasi presisi tidak perlu (Ps. 16 ayat (2) huruf a) | "Aplikasi hanya meminta izin kamera (pindai barcode) dan [isi: izin lain yang benar-benar dipakai]. Kami tidak mengakses daftar kontak atau SMS Anda. Lokasi hanya dipakai bila Anda mengaktifkan fitur [isi: …] dan bisa dimatikan." | tidak dikenali pola |
| K9 Tarik persetujuan ditiadakan | "Pengguna tidak dapat menarik kembali persetujuan setelah akun diaktifkan." | TINGGI | Ps. 40 (tarik persetujuan, berhenti ≤ 3×24 jam) | "Anda dapat menarik persetujuan kapan saja melalui privacy@kasirku.example; kami menghentikan pemrosesan terkait paling lambat 3×24 jam. Penarikan tidak memengaruhi pemrosesan yang sudah dilakukan sebelumnya." | tidak dikenali pola |
| K7 Arsip tanpa batas | "Data akun yang dihapus tetap kami simpan dalam arsip untuk keperluan internal tanpa batas waktu." | TINGGI | Ps. 43, 21 | "Setelah akun dihapus, data akun dihapus dalam [isi: 30] hari, kecuali catatan transaksi yang wajib disimpan 10 tahun untuk pajak." | ✓ TINGGI |
| K14 Hukum asing | "This Policy shall be governed by the laws of the State of Delaware, USA." | SEDANG | Ps. 2 (ruang lingkup UU PDP: pemrosesan yang berakibat hukum di Indonesia / WNI) | "Kebijakan ini tunduk pada hukum Republik Indonesia, termasuk UU 27/2022 tentang Pelindungan Data Pribadi." | tidak dikenali pola |
| K16 Salinan template luar | "Sesuai GDPR dan CCPA, Anda memiliki hak…" · "California residents may request disclosure of categories of personal information sold." | SEDANG | Ps. 16 ayat (2), 21; hak PDP tidak disebut | "Sesuai UU 27/2022, Anda berhak: mengakses & mendapat salinan data, memperbaiki, menghapus, menarik persetujuan, mengajukan keberatan atas keputusan otomatis, menunda/membatasi pemrosesan, dan menggugat ganti rugi. Ajukan lewat privacy@kasirku.example; kami tanggapi paling lambat 3×24 jam." | ✓ (baris CCPA ditandai K1 "sold" — lihat selisih) |
| K8 Kebocoran tidak disebut | (tidak ada kalimat) | SEDANG | Ps. 46 | (teks pemberitahuan 3×24 jam seperti dok A) | script: unsur TIDAK ADA ✓ |
Kategori tanpa temuan: K3, K4, K5, K6 (tidak disebut; bila server di luar negeri wajib ditulis — tanyakan), K10, K11, K13, K15. Kalimat patuh: retensi 10 tahun pajak; payment gateway berizin BI; statistik agregat anonim.

2. Pemeriksa kedua (script)
Skor 57/100 · Status KURANG LENGKAP. Unsur: dasar pemrosesan, transfer LN, cara mengajukan & batas waktu, keamanan, kebocoran, cara memberi tahu perubahan = TIDAK ADA; hak = SEBAGIAN.
Selisih dengan script:
- Script menangkap 5 dari 8 temuan; K12, K9 (tarik persetujuan), K14 tidak dikenali pola kata kunci.
- Script menandai "California residents … sold" sebagai TINGGI kategori jual data. Saya tidak setuju dengan kategorinya: kalimat itu sisa template CCPA (K16), bukan bukti KasirKu menjual data; penjualan data sudah dicatat di K1 dari kalimat "mengkomersialkan".
- Catatan script "Teks menyebut layanan 'aws'" keliru: tidak ada AWS di dokumen; itu cocokan dari kata "laws". Transfer LN tetap perlu dijelaskan bila server memang di luar negeri.
Disclaimer (sama).
```

---

## 4. Penilaian

### 4a. Tangkapan risiko
| | Dok A (7) | Dok B (7) | Dok C (7) | Total (21) |
|---|---|---|---|---|
| **Output akhir alur skill** (baca per K1–K16 → script → selisih) | 7 | 7 | 7 | **21/21 (100%)** + 3 temuan tambahan sah (A: transfer LN tidak disebut; B: hak tidak lengkap; C: kebocoran tidak disebut) |
| **Script mentah** | 0 | 3 | 4 | **7/21 (33%)** |
| Salah-positif alur skill (9 kalimat patuh) | 0 | 0 | 0 | **0/9** |
| Salah-positif script (9 kalimat patuh) | 0 | 0 | 0 | 0/9, tetapi 1 salah kategori (CCPA → K1) dan 1 catatan palsu ("aws" dari "laws") |

Semua 21 risiko jatuh tepat ke salah satu K1–K16, dan 14 di antaranya punya parafrasa yang dekat di tabel kategori (mis. "selama diperlukan", "biaya administrasi", "hari kerja", "deemed", "at our discretion", "Delaware", "register themselves"). Tabel kategori terbukti cukup luas untuk set ini. **Catatan bias:** angka 21/21 dicapai penguji yang juga menulis kunci; angka realistis untuk agent pengguna lebih rendah, tetapi v1.0.2 sudah mencatat agent yang membaca bebas menangkap 9/9, jadi arah hasilnya konsisten.

### 4b. Klaim "aman"
- Dok A (script 0 temuan) → script sendiri mencetak "Ini BUKAN jaminan kebijakan aman … Baca seluruh dokumen secara manual". Format output skill menaruh temuan agent di bagian 1, dan langkah 4 SKILL.md melarang klaim aman berbasis script. Output di atas tidak memuat klaim aman yang tidak berdasar. ✅
- Aturan "Kategori yang diperiksa tanpa temuan: …" memaksa agent menyebut kategori, sehingga "aman" tidak bisa ditulis secara umum. ✅

### 4c. Kebenaran & kesiapan perbaikan
- Teks perbaikan dari `kategori-risiko-cek.md` benar arah hukumnya dan bisa langsung ditempel setelah `[isi: …]` dilengkapi.
- **Kurang tepat (SEDANG):** perbaikan K5 hanya "memberi tahu Anda **sebelum** data dialihkan"; Ps. 48 ayat (1)–(2) UU PDP mewajibkan pemberitahuan **sebelum dan sesudah** penggabungan/pemisahan/pengambilalihan/peleburan, dan ayat (3)–(4) juga soal pembubaran (penyimpanan/transfer/penghapusan wajib diberitahukan). Pada output 3B penguji menulis "before and after", tetapi agent yang menyalin teks K5 akan kehilangan "sesudah".
- Tidak ada teks perbaikan EN siap tempel di `kategori-risiko-cek.md`; agent harus menerjemahkan sendiri untuk dokumen EN (dok B). Tidak fatal.

### 4d. Tes bawaan & regresi
- `python3 tests/uji_regresi.py` → **LULUS: 255 uji** (v1.0.2: 239).
- T-1 ✅, T-2 ✅, B-1 ✅, B-2 ✅ (tercakup di 255 uji). Template kosong ID & EN → **84/100 BELUM SIAP** (struktur 100 bila 56/40 isian dilengkapi) ✅.
- Pesan "Ini BUKAN jaminan kebijakan aman" muncul saat tidak ada pola cocok (dok A) ✅; pesan "penanda awal … TIDAK lengkap" muncul saat ada pola (dok B, C) ✅.
- SKILL.md 162 baris (< 300) ✅.

### 4e. Temuan baru
| ID | Prioritas | Temuan | Usulan |
|---|---|---|---|
| U4-1 | SEDANG | Perbaikan K5 hanya "sebelum" pengalihan; Ps. 48 mewajibkan sebelum **dan** sesudah, dan pembubaran juga wajib diberitahukan | Ubah teks perbaikan K5: "…kami memberi tahu Anda sebelum dan sesudah data dialihkan…"; di `dasar-hukum.md` Ps. 48 bisa naik ke ✅ (dasar K5 boleh dikutip "Pasal 48") |
| U4-2 | RENDAH | `LAYANAN_LN` di `scripts/cek_kebijakan.py` (baris ±496) tanpa batas kata: "laws" → 'aws', "metadata" → 'meta', "driver" → 'drive' memicu catatan transfer LN palsu | Tambahkan `\b…\b` di sekitar alternatif; tambahkan tes regresi untuk tiga kata ini |
| U4-3 | RENDAH | Status unsur script masih keliru pada teks santai/EN: "Buat apa datanya" (tujuan), "boleh minta lihat atau ubah … hapus" (hak), "request a copy" (akses), identitas "X ("the Clinic")" | Tidak wajib diperbaiki; alur "(dikoreksi manual)" sudah menangani. Jangan setel pola ke kalimat set ini |
| U4-4 | RENDAH | Baris CCPA "…personal information sold" ditandai K1 TINGGI; seharusnya K16 | Aturan selisih sudah cukup (agent menjelaskan); opsional: bila kalimat mengandung "California/CCPA", laporkan hanya sebagai template luar |
| U4-5 | INFO | Ps. 2, 47, 48 bertanda ⚠️ di `dasar-hukum.md` sudah **cocok** dengan ≥2 sumber (lihat 4f) | Naikkan ke ✅; tambahkan Ps. 2 ayat (2) (tidak berlaku untuk kegiatan pribadi/rumah tangga) sebagai catatan |

### 4f. Verifikasi pasal (web search 2026-09-25; pasal.id terblokir langsung, dicek lewat cuplikan hasil pencarian)
- **Ps. 2 ayat (1)** — berlaku bagi Setiap Orang, Badan Publik, Organisasi Internasional di wilayah RI dan di luar wilayah RI yang berakibat hukum di RI dan/atau bagi subjek data WNI di luar negeri; **ayat (2)** tidak berlaku untuk pemrosesan oleh perseorangan dalam kegiatan pribadi/rumah tangga. Cocok dengan `dasar-hukum.md`. Sumber: Tirto (isi UU PDP), pasal.id/pasal-2, ABNR (naskah ID-EN). ✅
- **Ps. 47** — pengendali wajib bertanggung jawab atas pemrosesan dan menunjukkan pertanggungjawaban dalam pemenuhan kewajiban pelaksanaan prinsip PDP. Cocok. Sumber: uupdp-info.id/pasal-47, pasal.id/pasal-47, Hukumonline Klinik. ✅
- **Ps. 48** — pengendali berbentuk badan hukum yang melakukan penggabungan, pemisahan, pengambilalihan, peleburan, atau pembubaran wajib memberi tahu pengalihan data kepada subjek data, sebelum dan sesudah; pembubaran: penyimpanan/transfer/penghapusan/pemusnahan sesuai aturan dan diberitahukan. Isi cocok, tetapi teks perbaikan K5 kurang "sesudah" (U4-1). Sumber: uupdp-info.id/pasal-48, pasal.id/pasal-48, ABNR. ✅
- Pasal lain di tabel kategori (16, 20, 21, 22, 25, 30, 32, 40, 43, 46, 53, 56, 65, 67) sesuai `dasar-hukum.md` yang sudah diverifikasi penguji sebelumnya; tidak ditemukan salah pasal baru.

Sumber: https://tirto.id/isi-uu-perlindungan-data-pribadi-undang-undang-no-27-tahun-2022-gFk7 · https://uupdp-info.id/pasal-47/ · https://uupdp-info.id/pasal-48/ · https://www.abnrlaw.com/lib/files/IND-ENG-UU%2027-2022%20Pelindungan%20Data%20Pribadi%20(ABNR).pdf · https://www.hukumonline.com/klinik/a/uu-pdp--landasan-hukum-pelindungan-data-pribadi-lt5d588c1cc649e/ · https://pasal.id/peraturan/uu/uu-no-27-tahun-2022/pasal-48

### Skor: **8/10** — LULUS (lihat `HASIL-UJI.md`, bagian "Uji ulang v1.0.3")
