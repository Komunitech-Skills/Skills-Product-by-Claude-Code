---
name: kebijakan-privasi-pdp
description: Menyusun Kebijakan Privasi sesuai UU 27/2022 Pelindungan Data Pribadi (UU PDP) untuk website, toko online, aplikasi, akun WhatsApp Business, klinik atau jasa (Bahasa Indonesia, versi Inggris opsional), membuat pemberitahuan & formulir persetujuan (consent) singkat untuk formulir, WA, dan Google Form, memeriksa kebijakan privasi yang sudah ada dengan skor kelengkapan & frasa berisiko, serta template tanggapan permintaan hak subjek data (akses, koreksi, hapus, tarik persetujuan) dan checklist kebocoran data 3x24 jam. Gunakan saat pengguna minta kebijakan privasi, privacy policy, consent form, persetujuan data, cek kepatuhan PDP, data breach, permintaan hapus data. Bukan audit keamanan OpenClaw (pakai cek-privasi-openclaw) dan bukan nasihat hukum.
---

# Kebijakan Privasi & Kepatuhan UU PDP untuk Usaha

## Tujuan
Membantu UMKM dan usaha Indonesia memenuhi kewajiban dasar UU 27/2022 tentang Pelindungan Data Pribadi (UU PDP) lewat dokumen yang siap tempel: kebijakan privasi, pemberitahuan & persetujuan, tanggapan permintaan pelanggan, dan langkah bila data bocor. Isinya mengikuti praktik usaha yang sebenarnya, tidak ada yang dikarang, dan dasar aturannya disebut. Ini draf, **bukan nasihat hukum**.

## Kapan digunakan (4 mode)
1. **SUSUN** — "Buatkan kebijakan privasi untuk toko online/website/aplikasi/WA Business/klinik saya."
2. **PERSETUJUAN** — "Buat kalimat persetujuan data untuk Google Form / pesan salam WA / formulir pendaftaran / pasien."
3. **CEK** — "Tolong cek kebijakan privasi saya, sudah sesuai UU PDP?" (teks ditempel atau file .md/.txt).
4. **TANGGAPI** — "Pelanggan minta datanya dihapus, balas gimana?" / "Data pelanggan kami bocor, harus apa?"

## Kapan TIDAK digunakan
- Audit pengaturan keamanan OpenClaw/AI agent milik pengguna → `cek-privasi-openclaw`.
- Kontrak/NDA dengan mitra → `perjanjian-sederhana` (klausul data bisa ditambahkan di sana).
- Sengketa, gugatan, pemeriksaan oleh otoritas, pemerasan oleh peretas, atau kebocoran besar → beri checklist darurat (mode 4), lalu **arahkan ke konsultan hukum**, polisi (bila ada kejahatan), dan ahli keamanan.
- Informed consent tindakan medis, perjanjian pemrosesan data (DPA) antarperusahaan, transfer data lintas negara berskala besar, atau kebijakan untuk bank/fintech/asuransi → di luar cakupan. Boleh beri daftar hal yang perlu ditanyakan ke konsultan.
- Permintaan membuat kebijakan yang menutupi praktik melanggar (mis. menjual data pelanggan, mengumpulkan data diam-diam) → tolak bagian itu dan jelaskan risikonya (UU PDP Pasal 65 & 67).

## Input (mode SUSUN)
| Info | Wajib? | Jika tidak diberikan |
|---|---|---|
| Nama usaha (+ nama pemilik/badan usaha) | Ya | `[isi: nama usaha]` |
| Jenis usaha & kanal: website/toko online/aplikasi/WA Business/marketplace/klinik/jasa | Ya | Tanyakan |
| Data yang dikumpulkan | Ya | Saran dari `references/pilihan-per-jenis-usaha.md`, **wajib dikonfirmasi** |
| Untuk apa data dipakai | Ya | Saran per jenis usaha, dikonfirmasi |
| Dibagi ke siapa (kurir, payment gateway, marketplace, jasa iklan/pixel, cloud, AI chatbot) | Ya | `[isi: ...]` per kategori yang relevan |
| Disimpan berapa lama | Tidak | Saran default dari tabel masa simpan, ditandai "saran" |
| Kontak urusan data (email/WA) & alamat | Ya | `[isi: ...]` |
| Data anak / data kesehatan / keuangan / biometrik? | Ya | Tanyakan, ini menentukan bagian khusus |
| Versi Inggris? | Tidak | Hanya Bahasa Indonesia |

Jika info wajib kurang, tanyakan **sekali** dalam satu pesan berisi daftar bernomor singkat, misalnya:
1. Nama usaha dan nama pemilik/PT/CV-nya?
2. Jualan/layanan lewat mana saja? (website, marketplace, WA Business, aplikasi, klinik/jasa tatap muka)
3. Data pelanggan apa saja yang dicatat? **Apakah ada data kesehatan, data anak (< 18 th), keuangan, atau biometrik?** (nama, no. WA, alamat, email, foto, dll.)
4. Dipakai untuk apa saja? (kirim pesanan, CS, promo, pengingat, dll.)
5. Data dibagikan ke siapa? (nama kurir, payment gateway, marketplace, Meta/Google/TikTok pixel, Google Drive/cloud, chatbot AI)
6. Disimpan berapa lama? (kalau belum tahu, saya pakai saran umum)
7. Email/WA untuk urusan data pribadi, dan alamat usaha?
8. Perlu versi bahasa Inggris?

Jika pengguna ingin cepat: katakan "cukup jawab no. 1–3 dulu", lalu buat draf dengan saran default, biarkan data yang tidak diketahui sebagai `[isi: ...]`, dan tulis daftar asumsi.

## Langkah kerja

### Mode 1 — SUSUN kebijakan privasi
1. **Saring cakupan** (lihat "Kapan TIDAK digunakan"). Bila ada data spesifik skala besar (mis. klinik dengan ribuan pasien, aplikasi kesehatan, layanan anak), tetap buat draf tetapi beri label **"DRAF — WAJIB DITINJAU KONSULTAN HUKUM"** dan ingatkan kemungkinan wajib DPO (Pasal 53 + Putusan MK 151/PUU-XXII/2024) dan penilaian dampak (Pasal 34).
2. **Petakan data** dalam tabel: Data → Tujuan → Dasar pemrosesan (Pasal 20 ayat (2): persetujuan / pelaksanaan perjanjian / kewajiban hukum / kepentingan vital / tugas umum / kepentingan sah) → Penerima → Masa simpan. Aturan:
   - Pesanan & pengiriman = **pelaksanaan perjanjian** (bukan persetujuan).
   - Promo/newsletter, testimoni, foto = **persetujuan** eksplisit terpisah. Data spesifik yang menjadi syarat layanan (mis. rekam medis klinik) = pelaksanaan perjanjian + kewajiban hukum, dengan akses terbatas; persetujuan eksplisit untuk pemakaian tambahannya.
   - Catatan transaksi = **kewajiban hukum** (pembukuan pajak 10 tahun, UU KUP Pasal 28 ayat (11)).
3. **Transfer luar negeri:** bila pengguna memakai WhatsApp/Meta, Google (Drive/Form/Sheets), Shopify, cloud atau AI asing → pakai opsi 5(a) (Pasal 56). Jangan menulis "semua data di Indonesia" kecuali pengguna memastikannya.
4. **Isi template** `templates/kebijakan-privasi.md` (dan `templates/kebijakan-privasi-en.md` bila diminta; versi Indonesia berlaku bila berbeda). Pilih isi per jenis usaha dari `references/pilihan-per-jenis-usaha.md`. Hapus blok PANDUAN AGENT dan bagian `{JIKA ...}` yang tidak berlaku. **Jangan mengarang** nama penyedia, alamat, email, masa simpan, atau langkah keamanan yang tidak dilakukan pengguna: pakai `[isi: ...]`.
5. **Periksa dengan script** (path relatif terhadap folder SKILL.md ini; Windows: ganti `python3` dengan `python` atau `py`):
   ```bash
   python3 <folder-skill-ini>/scripts/cek_kebijakan.py draf-kebijakan.md
   ```
   Target: skor struktur 100, tanpa frasa berisiko. Selama masih ada `[isi: ...]`, status = `BELUM SIAP` (kecuali strukturnya pun < 60 → `KURANG LENGKAP`; urutan status: `--daftar` / kunci JSON `alasan_status`) dan skor dibatasi maks. 84 (unsur yang isinya masih kosong ditandai `BELUM DIISI`); sebutkan daftar isian ke pengguna. Skor = **kelengkapan struktur**, bukan jaminan isi benar.
6. **Sajikan** sesuai format output, lalu tawarkan: pemberitahuan singkat (mode 2) untuk formulir/WA, dan template tanggapan hak subjek (mode 4).

### Mode 2 — PEMBERITAHUAN & PERSETUJUAN
Pakai `templates/pemberitahuan-persetujuan.md` (A website, B pesan salam WA, C Google Form, D klinik/data kesehatan, E English). Aturan wajib:
- Persetujuan **aktif** (centang kosong / ketik SETUJU), **per tujuan**, bisa ditolak tanpa kehilangan layanan inti, dan **terekam** (Pasal 20 & 22). Dilarang kotak tercentang otomatis dan kalimat "dengan mengisi, Anda dianggap setuju".
- Maksimal ±60 kata untuk pemberitahuan singkat, dan sertakan tautan kebijakan lengkap.
- Persetujuan **bukan syarat layanan** untuk data yang memang diperlukan layanan: pakai dasar pelaksanaan perjanjian/kewajiban hukum + pemberitahuan; persetujuan hanya untuk tujuan tambahan.
- Data anak → tambahkan persetujuan orang tua/wali (Pasal 25). Data kesehatan → template D (kertas/tablet) atau D-online (Google Form, tanpa tanda tangan, ada pilihan "isi langsung di klinik") + saran konsultasi.
- Ingatkan menyimpan bukti persetujuan (screenshot chat, kolom timestamp Google Form).

### Mode 3 — CEK kebijakan yang sudah ada
1. Simpan teks pengguna ke file lalu jalankan `python3 <folder-skill-ini>/scripts/cek_kebijakan.py file.md` (atau `--format json`).
2. **Baca juga isinya secara manual** dengan `references/checklist-uu-pdp.md` bagian C: kecocokan dengan praktik nyata, salinan GDPR/luar negeri, batas usia anak 13 tahun (COPPA; di Indonesia < 18 tahun), klaim "100% aman", data spesifik lewat Google Form/WA. Script mendeteksi pola umum saja; kalimat berbagi data yang tidak lazim tetap harus dibaca manual.
3. Laporkan: skor + status, tabel unsur (ADA/SEBAGIAN/TIDAK ADA), frasa berisiko dengan tingkat (TINGGI/SEDANG) + kutipan + saran pengganti, lalu **usulan teks perbaikan siap tempel** untuk tiap kekurangan.
4. Tawarkan versi lengkap yang sudah diperbaiki (mode 1 memakai isi lama).

### Mode 4 — TANGGAPI hak subjek data & kebocoran
- **Permintaan pelanggan** (akses, koreksi, hapus, tarik persetujuan): pakai `templates/tanggapan-hak-subjek.md`. Hitung tenggat = waktu diterima + 72 jam, lalu tulis tanggal-jamnya. Jelaskan data yang wajib tetap disimpan (pajak/rekam medis) beserta alasannya. Ingatkan tempat data tersembunyi (kontak HP, label WA, Sheets, backup, memori AI agent).
- **Kebocoran data**: pakai `templates/checklist-kebocoran.md`. Hitung tenggat 3×24 jam sejak insiden diketahui, pandu langkah jam 0–6 (amankan) dulu, lalu siapkan draf pemberitahuan ke pelanggan & lembaga (Pasal 46). **Bila tenggat sudah lewat:** tetap kirim pemberitahuan secepatnya (jangan ditunda lagi), tulis jujur kapan insiden diketahui dan alasan keterlambatan, catat kronologinya, dan sarankan segera konsultan hukum. Sampaikan bahwa lembaga pengawas PDP **belum terbentuk** per 25 Sep 2026 (sementara Kemkomdigi) dan kanal resmi perlu dicek. Untuk kebocoran data spesifik/berskala besar/pemerasan → sarankan segera konsultan hukum & polisi.

### Fallback jika Python tidak bisa dijalankan
Periksa manual dengan tabel unsur di `references/checklist-uu-pdp.md` (14 unsur + 2 bersyarat, bobot sama). Skor = bobot terpenuhi ÷ bobot berlaku × 100. Cari frasa berisiko di bagian B. Beri tahu pengguna bahwa pemeriksaan dilakukan manual.

## Format output

**Mode SUSUN:**
```
⚠ Draf ini bukan nasihat hukum. Status: [SIAP DITINJAU / BELUM SIAP (n isian kosong)] · Skor cek: [n]/100 (struktur [m]/100)

--- (Kebijakan Privasi lengkap, siap tempel) ---

### Yang masih perlu dilengkapi
- [isi: ...] yang tersisa

### Asumsi yang saya pakai
- mis. masa simpan chat 1 tahun (saran), promo hanya dengan persetujuan

### Langkah berikutnya (3–5 poin)
- Pasang tautan kebijakan di website/bio/profil WA Business · pasang pemberitahuan singkat di formulir · siapkan email/WA khusus data · catat log permintaan

_Disclaimer: Disusun otomatis dari informasi Anda, mengacu pada UU 27/2022 (dicek 25 September 2026). PP 33/2026 berlaku 16 Januari 2027; lembaga pengawas PDP belum terbentuk saat pengecekan. Bukan nasihat hukum. Usaha yang memproses data kesehatan, anak, atau keuangan dalam skala besar sebaiknya meminta peninjauan konsultan hukum._
```

**Mode CEK:**
```
Skor kelengkapan: [n]/100 · Status: [..] · Frasa berisiko: [x TINGGI, y SEDANG]
(Skor mengukur kelengkapan struktur berbasis kata kunci & polaritas kalimat, bukan kebenaran isi.)
| Unsur | Status | Dasar |
Frasa berisiko: [tingkat] "kutipan" → masalah → ganti dengan "..."
Usulan teks perbaikan (siap tempel): ...
Disclaimer (sama seperti di atas)
```

## Contoh
**Input:** "Bikinin kebijakan privasi buat toko kue online aku, Dapur Bu Sari. Jualan lewat website sama WA, kirim pakai kurir, bayar lewat transfer bank & payment gateway, ada Meta Pixel."

**Output (dipotong):**
```
⚠ Draf ini bukan nasihat hukum. Status: BELUM SIAP (3 isian kosong) · Skor cek: 84/100 (struktur 100/100)
# Kebijakan Privasi Dapur Bu Sari
...
| Nama, no. WA, alamat | Memproses & mengirim pesanan | Pelaksanaan perjanjian | 10 tahun untuk catatan transaksi (pajak) |
| No. WA | Promo | Persetujuan Anda | Sampai persetujuan ditarik |
...
## 5. Penyimpanan data di luar negeri
Sebagian layanan yang kami gunakan (WhatsApp/Meta, Meta Pixel, [isi: layanan cloud]) dapat menyimpan data di luar Indonesia...
### Yang masih perlu dilengkapi
- [isi: nama payment gateway] · [isi: email urusan data] · [isi: alamat]
```

**Di luar cakupan:** "Buatkan kebijakan yang bilang kami boleh jual data pelanggan ke mitra" → tolak bagian itu, jelaskan larangan Pasal 65 dan ancaman Pasal 67, tawarkan alternatif (kerja sama promosi dengan persetujuan eksplisit pelanggan).

## Checklist sebelum mengirim hasil
- [ ] Tidak ada nama penyedia/alamat/email/masa simpan karangan; semua yang tidak diketahui = `[isi: ...]`.
- [ ] Setiap data punya tujuan, dasar pemrosesan, dan masa simpan; promo & data spesifik memakai persetujuan terpisah.
- [ ] Transfer luar negeri jujur sesuai layanan yang dipakai; ada kalimat "Kami tidak menjual data pribadi Anda."
- [ ] Hak subjek data + cara mengajukan + 3×24 jam; pemberitahuan kebocoran 3×24 jam.
- [ ] `cek_kebijakan.py` tanpa frasa berisiko; skor dan sisa isian disebutkan.
- [ ] Disclaimer + tanggal cek + status PP 33/2026 & lembaga pengawas tercantum.

## Batasan & penanganan error
- Script keluar kode 2 dengan pesan `GALAT: ...` untuk file tidak ada, folder, file kosong, file > 5 MB, .docx/.pdf, atau file biner. Encoding UTF-8/BOM/cp1252 dan UTF-16 (dengan atau tanpa BOM) terbaca otomatis; HTML mentah (tag, `&nbsp;`) dibersihkan dulu. Minta pengguna menempel teks bila file tidak bisa dibaca.
- Script hanya **pemeriksa kata kunci + polaritas kalimat** (kalimat yang disangkal, mis. "Data Anda tidak akan dijual", tidak ditandai; "kami tidak akan memberi tahu bila bocor" tidak dihitung sebagai unsur): kata kunci ada bukan berarti isinya benar. Penilaian akhir tetap oleh agent (checklist bagian C) dan, bila perlu, konsultan hukum.
- Dasar hukum, status verifikasi pasal, dan item **PERLU REVIEW**: `references/dasar-hukum.md`. Jangan mengutip nomor pasal PP 33/2026 di dokumen pengguna sampai naskah resminya diverifikasi.
- Uji regresi script: `python3 <folder-skill-ini>/tests/uji_regresi.py`.
- Data pelanggan yang ditempel pengguna hanya dipakai untuk menyusun dokumen. Jangan disimpan atau dikirim ke tempat lain.
