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

## 2. Kerahasiaan medis (UU Kesehatan 17/2023 & PP 28/2024)

**Status: TERVERIFIKASI (naskah resmi dibaca langsung).**
Sumber: UU No. 17 Tahun 2023 tentang Kesehatan — PDF resmi
https://farmalkes.kemkes.go.id/en/unduh/uu-17-2023/ ; PP No. 28 Tahun 2024 (aturan pelaksana
UU 17/2023) — PDF resmi https://farmalkes.kemkes.go.id/en/unduh/pp-28-2024/.
(peraturan.bpk.go.id sempat menolak akses/403 saat verifikasi; sumber di atas dipakai sebagai
gantinya. Bila mengutip di dokumen resmi/kontrak, cocokkan sekali lagi dengan salinan di
jdih.kemkes.go.id.)

- **Pasal 4 ayat (1) huruf i, UU 17/2023:** setiap orang berhak memperoleh kerahasiaan data dan
  informasi kesehatan pribadinya.
- **Pasal 4 ayat (4):** hak kerahasiaan itu boleh dikecualikan hanya untuk: penegakan hukum;
  KLB/wabah/bencana; pendidikan & penelitian terbatas; perlindungan orang lain; kepentingan
  pengobatan pasien sendiri; **permintaan pasien sendiri**; kepentingan administratif/asuransi/
  jaminan kesehatan; dan kepentingan lain menurut peraturan perundang-undangan.
- **Pasal 274 huruf c:** tenaga medis & tenaga kesehatan wajib "menjaga rahasia Kesehatan
  Pasien" dalam menjalankan praktik.
- **Pasal 296 ayat (5):** rekam medis wajib disimpan dan dijaga kerahasiaannya oleh tenaga
  medis, tenaga kesehatan, dan pimpinan fasilitas pelayanan kesehatan.
- **Pasal 297 ayat (3):** fasyankes wajib menjaga keamanan, keutuhan, kerahasiaan, dan
  ketersediaan data dalam dokumen rekam medis.
- **Pasal 301:** ayat (1) tenaga medis/kesehatan wajib menyimpan rahasia kesehatan pribadi
  pasien; ayat (2) pembukaan rahasia hanya untuk kepentingan sebagaimana Pasal 4 ayat (4); ayat
  (3) diatur lebih lanjut dengan Peraturan Pemerintah.
- **PP 28/2024 Pasal 788:** ayat (1) setiap fasyankes harus menyimpan rahasia kesehatan pribadi
  pasien; ayat (3) rahasia itu meliputi identitas pasien, data & informasi kesehatan (anamnesis,
  pemeriksaan, penunjang, diagnosis, pengobatan/tindakan), dan hal lain terkait pasien.
- **PP 28/2024 Pasal 789:** pihak yang wajib menyimpan rahasia mencakup tenaga medis/kesehatan,
  pimpinan & manajemen, tenaga pembiayaan, **"tenaga lainnya yang memiliki data pasien"**, dan
  pihak lain yang terlibat. **Ini mencakup admin/staf non-medis klinik yang mengoperasikan
  skill ini** — kewajiban rahasia berlaku untuk mereka juga, bukan hanya dokter.

Kalimat siap pakai untuk dokumen klinik:
> "Tenaga medis, tenaga kesehatan, dan tenaga lainnya yang memiliki akses ke data pasien
> (termasuk staf admin) wajib menjaga kerahasiaan data dan informasi kesehatan pasien sesuai
> UU No. 17 Tahun 2023 tentang Kesehatan (Pasal 4 ayat (1) huruf i & ayat (4), Pasal 274 huruf c,
> Pasal 296 ayat (5), Pasal 297 ayat (3), Pasal 301) dan PP No. 28 Tahun 2024 (Pasal 788–789),
> selain kewajiban UU PDP. Pembukaan data hanya untuk kepentingan yang diatur Pasal 4 ayat (4)
> UU 17/2023 (mis. permintaan pasien sendiri, penegakan hukum, kepentingan pengobatan)."

Ini kutipan isi pasal, **bukan analisis hukum lengkap** — untuk kasus spesifik (mis. permintaan
pihak ketiga atas data pasien) tetap konsultasikan ke ahli hukum kesehatan.

## 3. Iklan/promosi layanan kesehatan (Permenkes 1787/MENKES/PER/XII/2010)

**Status: TERVERIFIKASI isi pasal (naskah resmi dibaca langsung); status berlaku PERLU DICEK.**
Sumber: Berita Negara RI 2010 No. 673 — salinan PDF resmi
https://www.kemhan.go.id/itjen/wp-content/uploads/2017/03/bn673-2010.pdf ; salinan kompilasi
Kemenkes: https://kms.kemkes.go.id/contents/1715917225382-bukuperaturaniklanpublikasikes.pdf.

- **Pasal 3 ayat (2):** iklan/publikasi pelayanan kesehatan harus sesuai kode etik rumah sakit,
  kode etik tenaga kesehatan, kode etik periklanan (Etika Pariwara Indonesia), dan peraturan
  perundang-undangan.
- **Pasal 4 ayat (1):** iklan/publikasi harus akurat, berbasis bukti, informatif, edukatif, dan
  bertanggung jawab.
- **Pasal 4 ayat (2):** **wajib mencantumkan nama dan alamat fasilitas pelayanan kesehatan serta
  tanggal publikasi**. Di naskah, kewajiban ini berlaku untuk iklan/publikasi **melalui media
  cetak, media elektronik, dan media luar ruang** — bukan "setiap iklan/publikasi" tanpa syarat.
  Skill ini tetap menerapkannya ke **semua** konten medsos yang dibuat (termasuk yang mungkin di
  luar cakupan literal tiga jenis media itu) sebagai **praktik aman**, bukan karena naskah
  mewajibkannya secara harfiah untuk setiap kanal — ditulis jujur di sini supaya tidak dikira
  kutipan pasal yang persis.
- **Pasal 5** — iklan/publikasi TIDAK DIPERBOLEHKAN bila, antara lain (dikutip sedekat mungkin
  dengan rumusan naskah, bukan diperluas/dipersempit): (b) tidak benar atau menyesatkan; (c)
  menciptakan pengharapan yang tidak tepat; (d) **"membandingkan mutu pelayanan fasilitas
  pelayanan kesehatan lain"** (naskah hanya menyebut fasyankes lain, bukan tenaga kesehatan
  lain); (e) memuji diri berlebihan (superlatif) atau mengklaim "satu-satunya"; (f)
  mempromosikan metode/obat yang belum terbukti secara ilmiah; (h) mengiklankan layanan tanpa
  izin resmi; (l) **"memberi informasi kepada masyarakat dengan cara yang bersifat mendorong
  penggunaan jasa tenaga kesehatan di fasilitas pelayanan kesehatan tersebut"** (naskah tidak
  memuat syarat tambahan seperti "di luar kebutuhan medis" — larangannya seluas rumusan itu);
  **(m) berisi promosi penjualan termasuk pemberian diskon**; **(n) memberi testimoni dalam
  bentuk iklan atau publikasi di media massa** (larangan ini **tanpa pengecualian izin
  tertulis**); (o) **"menggunakan gelar akademis dan/atau sebutan profesi di bidang
  kesehatan"** (naskah tidak membatasi ini hanya "untuk tujuan promosi" — larangannya berlaku
  atas penggunaan gelar/sebutan itu sendiri dalam iklan/publikasi).
- **Status berlaku:** UU 17/2023 Pasal 453 menyatakan peraturan pelaksana UU kesehatan lama
  tetap berlaku sepanjang tidak bertentangan; PP 28/2024 tidak memuat bab khusus iklan
  pelayanan fasyankes (hanya Pasal 424 untuk iklan sediaan farmasi/alkes/PKRT). Sampai
  verifikasi ini, **belum ditemukan pencabutan** Permenkes 1787/2010. **Status berlaku tetap
  PERLU DICEK ulang di jdih.kemkes.go.id** sebelum dijadikan dasar tunggal keputusan hukum, dan
  apakah media sosial otomatis termasuk "media massa" di Pasal 5 huruf n juga perlu dicek —
  sikap aman skill ini: **perlakukan media sosial sama seperti media massa.**

**Praktik skill ini (sejalan dengan Pasal 4–5 di atas):**
- Skill **tidak pernah membuat testimoni pasien atau foto before-after untuk iklan/publikasi**
  — bukan karena kurang izin, tapi karena Pasal 5 huruf n melarangnya tanpa pengecualian. Kalau
  pengguna meminta, skill menolak dan menjelaskan dasar ini, bukan menawarkan "asal ada izin".
  Foto/video pasien tetap butuh izin tertulis terpisah untuk keperluan apa pun (dasar UU PDP),
  tapi izin itu **tidak membuat testimoni jadi boleh diiklankan**.
- Skill **tidak membuat promosi diskon/potongan harga untuk tindakan medis** dalam bentuk
  iklan/publikasi (Pasal 5 huruf m) — pembahasan harga tetap boleh untuk FAQ informatif
  (bukan format iklan berpromosi).
- Skill **tidak membuat klaim "menyembuhkan"/"100% berhasil", superlatif ("terbaik",
  "satu-satunya"), atau perbandingan mutu pelayanan** dengan fasilitas kesehatan lain (Pasal 5
  huruf c, d, e).
- Skill **tidak mencantumkan gelar akademis/sebutan profesi di bidang kesehatan** dalam materi
  iklan/publikasi (Pasal 5 huruf o — larangan berlaku umum, bukan hanya bila diniatkan promosi).
- Skill **tidak menulis ajakan yang bersifat mendorong penggunaan jasa** tenaga
  kesehatan/fasyankes (Pasal 5 huruf l) — konten tetap berupa edukasi umum, bukan ajakan
  memakai layanan tertentu.
- Skill **tidak mengklaim status/izin yang belum dikonfirmasi klinik** (mis. "terakreditasi",
  "kerja sama resmi dengan RS X") kecuali klinik menyatakan itu benar dan bisa dibuktikan.
- **Setiap konten medsos yang dibuat skill ini mencantumkan nama & alamat klinik serta tanggal
  publikasi** (Pasal 4 ayat (2)) — lihat format di `bahasa-awam-pasien.md` dan checklist
  SKILL.md.
- Sebelum kampanye iklan berbayar (Meta/Google Ads) untuk layanan kesehatan, klinik disarankan
  cek kebijakan platform iklan (biasanya ada pembatasan khusus kategori kesehatan) dan, bila
  perlu, konsultasi ke organisasi profesi (IDI/PDGI/dst.)/konsultan kepatuhan setempat.

## Ringkasan sikap skill ini
- Menulis materi berdasarkan **fakta yang diberikan klinik**, bukan mengarang klaim medis.
- Tidak pernah menyalin data pasien individual ke output.
- Mengutip pasal yang **sudah diverifikasi dari naskah resmi** (bagian 1–3 di atas), dan
  menandai bagian yang **PERLU DICEK** (status berlaku Permenkes 1787/2010) apa adanya, tidak
  berpura-pura sudah pasti.
- Untuk kasus di luar cakupan (kontrak kerja sama, sengketa, audit kepatuhan penuh, tafsir kasus
  spesifik) → arahkan ke konsultan hukum/kepatuhan kesehatan.
