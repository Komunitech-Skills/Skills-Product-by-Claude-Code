# Privasi Data Kesehatan, Kerahasiaan Medis & Aturan Iklan Layanan Kesehatan

Disclaimer umum: ringkasan ini **bukan nasihat hukum**. Untuk kepatuhan penuh, klinik tetap
perlu konsultasi ke konsultan hukum/kepatuhan atau organisasi profesi terkait.
Status verifikasi tiap poin ditulis apa adanya — bagian yang ditandai **PERLU DICEK** belum
dikonfirmasi dari naskah resmi (peraturan.bpk.go.id / JDIH) dalam sesi penyusunan skill ini
dan wajib diverifikasi ulang sebelum dijadikan dasar klaim hukum di materi jualan.

## 1. Data kesehatan = data pribadi bersifat spesifik (UU PDP 27/2022)

**Status: TERVERIFIKASI (rujukan umum UU, bukan nomor pasal persis).**

- UU Pelindungan Data Pribadi (UU No. 27 Tahun 2022) berlaku penuh sejak Oktober 2024.
  Data kesehatan termasuk kategori **data pribadi yang bersifat spesifik**, yang perlindungannya
  lebih ketat daripada data pribadi umum (perlu dasar pemrosesan yang lebih kuat, umumnya
  persetujuan eksplisit).
- Peraturan pelaksana **PP 33/2026** (tentang Peraturan Pelaksanaan UU PDP) sudah diundangkan
  **16 Juli 2026** dan **berlaku 16 Januari 2027**. Sebelum itu, acuan utama tetap UU 27/2022.
  Isi PP 33/2026 yang relevan (dari sumber sekunder, naskah resmi belum dibaca langsung dalam
  penyusunan skill ini): persetujuan eksplisit per tujuan pemrosesan, notifikasi kegagalan
  pelindungan data pribadi **paling lambat 3×24 jam** ke subjek data & lembaga pengawas, dan
  aturan perjanjian pengendali–prosesor data.
- **Praktik wajar untuk klinik pengguna skill ini:**
  1. Basis pengetahuan (FAQ, template) **tidak berisi data pasien sungguhan** — hanya info umum
     klinik.
  2. Draf/rekap operasional **tidak menyertakan nama, NIK, tanggal lahir, diagnosis** — lihat
     `scripts/rekap_kunjungan.py` yang otomatis mengabaikan kolom semacam itu.
  3. Jangan menempelkan rekam medis, hasil lab, atau catatan diagnosis pasien ke chat AI dalam
     bentuk apa pun (termasuk untuk membuat leaflet) — cukup salin poin instruksi umum dokter
     (mis. "boleh makan lunak", "kontrol 1 minggu"), bukan isi rekam medis lengkap.
  4. Sebutkan ke pasien di awal chat bahwa mereka berbicara dengan asisten (bila dipakai lewat
     WA/chat otomatis), dan mereka boleh minta bicara dengan staf/dokter.
  5. Transkrip chat & data operasional tersimpan lokal (di komputer/Gateway klinik) — jaga
     keamanan fisik & akses komputer tersebut.

## 2. Kerahasiaan medis (UU Kesehatan 17/2023)

**Status: PERLU DICEK.** Nomor pasal spesifik tentang kewajiban rahasia kedokteran/rekam medis
di UU No. 17 Tahun 2023 tentang Kesehatan **belum diverifikasi dari naskah resmi** (peraturan.bpk.go.id
atau JDIH Kemenkes) dalam penyusunan skill ini. Yang bisa ditulis dengan aman:

> "Tenaga kesehatan dan fasilitas pelayanan kesehatan memiliki kewajiban menjaga kerahasiaan
> data dan informasi kesehatan pasien sebagaimana diatur dalam peraturan perundang-undangan di
> bidang kesehatan (termasuk UU No. 17 Tahun 2023 tentang Kesehatan) dan UU PDP. **Nomor pasal
> persis perlu dicek ulang** di peraturan.bpk.go.id/JDIH Kemenkes sebelum dikutip di materi
> resmi/kontrak."

**Jangan** mengutip nomor pasal spesifik UU 17/2023 di materi jualan atau dokumen legal klinik
sebelum diverifikasi dari naskah resmi. Skill ini sengaja tidak mencantumkan nomor pasal untuk
menghindari kutipan yang salah.

## 3. Iklan/promosi layanan kesehatan

**Status: PERLU DICEK.** Ketentuan spesifik (mis. peraturan Kementerian Kesehatan tentang iklan
dan publikasi pelayanan kesehatan, kode etik organisasi profesi seperti IDI/PDGI/IDAI) **belum
diverifikasi naskah resminya** dalam penyusunan skill ini. Prinsip aman yang dipakai skill ini
tanpa perlu menunggu verifikasi pasal (karena sejalan dengan etika kedokteran & perlindungan
konsumen yang berlaku umum):

- **Tidak membuat/menyetujui klaim "menyembuhkan", "100% berhasil", atau janji hasil medis
  pasti.** Gunakan bahasa informatif ("dapat membantu", "salah satu pilihan penanganan"), bukan
  janji.
- **Tidak membuat/memasang testimoni pasien atau foto before-after** tanpa persetujuan tertulis
  eksplisit dari pasien yang bersangkutan untuk keperluan promosi. Jika klinik memberi testimoni
  yang sudah punya izin, skill hanya merapikan bahasa — tidak menambah klaim di luar yang
  diberikan.
- **Tidak mengklaim status/izin yang belum dikonfirmasi klinik** (mis. "terakreditasi",
  "bersertifikat BPOM", "kerja sama resmi dengan RS X") kecuali klinik menyatakan itu benar dan
  bisa dibuktikan.
- Konten edukasi medsos tetap berupa **edukasi**, bukan iklan tindakan tertentu dengan harga
  promo dan urgensi palsu ("buruan, kuota terbatas hari ini saja" untuk tindakan medis).
- Sebelum kampanye iklan berbayar (Meta/Google Ads) untuk layanan kesehatan, klinik disarankan
  cek kebijakan platform iklan (biasanya ada pembatasan khusus kategori kesehatan) dan, bila
  perlu, konsultasi ke organisasi profesi/konsultan kepatuhan setempat.

## Ringkasan sikap skill ini
- Menulis materi berdasarkan **fakta yang diberikan klinik**, bukan mengarang klaim medis.
- Tidak pernah menyalin data pasien individual ke output.
- Menandai bagian hukum yang **PERLU DICEK** apa adanya, tidak berpura-pura sudah pasti.
- Untuk kasus di luar cakupan (kontrak kerja sama, sengketa, audit kepatuhan penuh) → arahkan ke
  konsultan hukum/kepatuhan kesehatan.
