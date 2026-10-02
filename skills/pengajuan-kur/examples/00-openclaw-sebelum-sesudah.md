# Uji OpenClaw SEBELUM vs SESUDAH — pengajuan-kur

## Cara uji
- **Tanggal:** 2026-10-01. Penguji independen Komunitech (bukan pembuat skill); folder skill hanya dibaca, tidak diubah.
- **Agent:** OpenClaw **2026.9.6** lokal (`openclaw agent --local`, tanpa Telegram/gateway), model router Komunitech **claude-sonnet-5** (sama dengan bot member), TZ Asia/Jakarta.
- **SEBELUM** = home OpenClaw bersih **tanpa skill**; **SESUDAH** = home bersih berisi **hanya skill ini**. Home dibuat ulang per skenario. Pesan identik di kedua sisi.
- Angka diverifikasi ulang dengan Python (rumus anuitas & flat, pencarian bunga efektif setara). Aturan dicek terhadap Permenko Perekonomian 1/2026 lewat siaran pers Kemenko (ekon.go.id, 27 Jan 2026) dan pemberitaan 2026 (mis. bisnis.com 23 Sep 2026): KUR Mikro >Rp10–100 juta; perdagangan non-ekspor 6% (akad ke-1) / 7% (akad ke-2), **maksimal 2 akad**; tanpa agunan tambahan s.d. Rp100 juta.
- Perilaku agent: tidak ada yang memasang paket, mengubah config, atau mencari ke seluruh disk. SEBELUM skenario 2 mencoba `web_fetch` (gagal, menjawab dari pengetahuan umum).

## Skenario 1 — Normal: bengkel, KUR Rp75 juta 3 tahun, aman atau tidak + dokumen

**Pesan pengguna:**
> Kak aku punya bengkel servis motor udah 3 tahun, laba bersih sekitar Rp 6.500.000 sebulan. Mau ajukan KUR BRI Rp 75.000.000 tenor 3 tahun, buat beli kompresor & alat Rp 30.000.000 sama stok sparepart Rp 45.000.000. Cicilannya berapa sebulan? Aman ga buat aku? Terus dokumen apa aja yg perlu disiapin?

**SEBELUM (tanpa skill)** — tools: (tidak ada)
~~~~text
Oke, aku hitungin ya, Kak. Pakai asumsi bunga KUR saat ini (6% efektif/tahun — ini patokan pemerintah, tapi tetap konfirmasi ke AO BRI karena bisa direvisi tiap tahun).

**1. Simulasi cicilan kalau Rp75 juta digabung, tenor 3 tahun (36 bulan):**
- Angsuran ≈ **Rp 2.281.000/bulan**
- Total bayar ≈ Rp 82,1 juta (bunga total ≈ Rp 7,1 juta)
- Itu artinya **35% dari laba bersih** (6,5 juta) habis buat cicilan tiap bulan.

**2. Aman ga?**
Jujur, 35% itu agak mepet. Idealnya cicilan usaha nggak lebih dari 30% laba bersih, biar masih ada ruang buat kebutuhan pribadi, bulan sepi, atau darurat. Bengkel juga biasanya fluktuatif (musim hujan/lebaran rame, bulan lain sepi), jadi margin aman itu penting.

**3. Saran: pecah jadi 2 fasilitas, bukan 1**
Karena dananya buat 2 tujuan beda (alat = investasi, sparepart = modal kerja), minta ke BRI dipisah:
- **KUR Investasi Rp30 juta** untuk kompresor & alat, tenor bisa sampai 5 tahun (60 bulan) → cicilan ≈ **Rp 580.000/bulan**
- **KUR Modal Kerja Rp45 juta** untuk sparepart, tenor 3 tahun (36 bulan) → cicilan ≈ **Rp 1.369.000/bulan**

Total 3 tahun pertama ≈ **Rp 1.949.000/bulan** (cuma 30% dari laba bersih), terus tahun ke-4 & 5 tinggal bayar yang investasi aja ≈ Rp 580.000/bulan. Jauh lebih napas lega dibanding digabung 1 pinjaman 3 tahun. Ini pola yang umum dipakai dan BRI biasa oke-in kalau alasannya jelas.

Satu hal penting: pastikan kompresor baru itu beneran bisa naikin omzet (servis lebih cepat, bisa terima job lebih banyak, dsb) — karena cicilan ini nambah beban tetap bulanan, harus ada kepastian pendapatan tambahan buat nutupnya, bukan cuma ngandelin laba yang sekarang.

**4. Dokumen yang perlu disiapin:**
- KTP (+ KTP pasangan & surat nikah kalau sudah menikah)
- Kartu Keluarga (KK)
- NPWP (wajib untuk pinjaman di atas Rp50 juta)
- NIB (Nomor Induk Berusaha) dari OSS, atau surat keterangan usaha dari kelurahan kalau belum punya NIB — bikin NIB gratis & online di oss.go.id, usahain punya dulu sebelum ajukan
- Bukti tempat usaha: sertifikat/surat sewa bengkel
- Catatan keuangan usaha 6-12 bulan terakhir (buku kas masuk-keluar, boleh manual/tulis tangan asal rapi)
- Foto bengkel/usaha
- Rekening tabungan BRI (buka dulu kalau belum ada, buat pencairan & setoran)
- Pas foto
- **RAB sederhana** — rincian "Rp30jt beli kompresor & alat (sebutkan merk/tipe), Rp45jt stok sparepart" di atas kertas. Ini bantu banget ngeyakinin AO soal tujuan dana jelas dan nggak dipakai hal lain.
- Untuk plafon Rp75jt (masih di bawah Rp100jt), KUR Mikro **biasanya nggak wajib agunan tambahan** — cukup agunan pokok (usaha yang dibiayai). Tapi tetap bisa beda kebijakan per cabang, jadi tanya langsung ke BRI terdekat.

Kalau mau, aku bisa bantuin susun draft RAB-nya biar tinggal dibawa ke BRI.
~~~~

**SESUDAH (dengan skill)** — tools: read, exec (skill terpakai: `scripts/simulasi_kur.py --kur`)
~~~~text
Halo! Bengkel motor masuk **KUR Mikro sektor produksi** (jasa servis, bukan dagang), jadi bunga acuannya 6%/tahun efektif. Ini hasilnya, dihitung pakai simulasi resmi:

## Persiapan Pengajuan KUR — Bengkel Servis Motor (3 tahun)
⚠️ Suku bunga **6% efektif/tahun = ACUAN Permenko Perekonomian 1/2026 Pasal 37** (KUR Mikro, sektor produksi) — **konfirmasi ke bank BRI**.

### 1. Simulasi cicilan (Rp 75.000.000, 36 bulan)
| | Anuitas (efektif) — yang berlaku | Flat 6% (ilustrasi) |
|---|---:|---:|
| Cicilan/bulan | **Rp 2.281.645** | Rp 2.458.333 |
| Total bunga | Rp 7.139.231 | Rp 13.500.000 |
| Total dibayar | Rp 82.139.231 | Rp 88.500.000 |

Anuitas: bunga dihitung dari **sisa** pokok, jadi makin lama porsi bunga makin kecil → cicilan Rp 2.281.645/bulan ini yang berlaku untuk KUR. Kalau ada petugas bank menyebut "flat 6%", itu beda — flat 6% justru setara bunga efektif ±11,08%/tahun (lebih mahal Rp 6.360.769 total bunga). Untuk KUR, flat yang setara 6% efektif cuma **±3,17%/tahun**. Jadi kalau ditawari "flat 6%", tanyakan ulang — itu bukan harga KUR yang benar.

### 2. Kemampuan bayar
Laba bersih Rp 6.500.000/bulan → cicilan **35,1%** dari laba → 🟡 **BERAT, perlu hati-hati**. Sisa laba setelah cicilan: Rp 4.218.355/bulan.

Ini di atas batas aman 30% yang dipakai sebagai panduan (bukan aturan baku bank, tapi rawan sesak kalau ada bulan sepi atau biaya tak terduga). Opsi:
- **Turunkan plafon ke sekitar Rp 64.098.000** agar cicilan ≤30% laba — misalnya kompresor & alat tetap Rp 30 juta, stok sparepart dikurangi jadi ±Rp 34 juta, sisanya nambah bertahap.
- Beli kompresor & alat dulu (Rp 30 juta) pakai KUR, stok sparepart ditambah bertahap dari omzet setelah alat baru jalan.
- Pastikan laba Rp 6,5 juta itu sudah bersih dari kebutuhan rumah tangga yang diambil dari bengkel — kalau belum, hitung ulang, bisa jadi makin berat.
- Tenor **sudah di batas atas** untuk porsi stok sparepart (modal kerja KUR Mikro maks 36 bulan/3 tahun, Pasal 38) — jadi tenor tidak bisa diperpanjang lagi tanpa pisah fasilitas.

### 3. Rencana penggunaan dana
| Pos | Nominal | % | Jenis |
|---|---:|---:|---|
| Kompresor & alat | Rp 30.000.000 | 40,0% | Investasi |
| Stok sparepart | Rp 45.000.000 | 60,0% | Modal kerja |
| **Total** | **Rp 75.000.000** | 100% | = plafon ✔ |

⚠️ Dana campuran investasi + modal kerja: investasi (kompresor) batas tenor 60 bulan, modal kerja (stok sparepart) batas tenor 36 bulan (Pasal 38). Dengan tenor 36 bulan untuk semuanya, keduanya masih di dalam batas — jadi secara aturan tenor **aman**, tapi tanyakan ke BRI apakah mau digabung satu akad atau dipisah (kadang bank lebih suka pisah untuk modal kerja vs investasi).

### 4. Profil usaha (siap salin, isi bagian kosong)
```
PROFIL USAHA
Nama usaha      : [isi: nama bengkel]
Pemilik         : [isi: nama pemilik]
Alamat usaha    : [isi: alamat lengkap]
Bidang usaha    : Jasa produksi — bengkel servis motor
Mulai berjalan  : [isi: bulan/tahun mulai] (± 3 tahun)
Legalitas       : [isi: NIB / SKU — sebut yang dimiliki]
Karyawan        : [isi: jumlah]

Gambaran usaha
[Nama bengkel] melayani servis dan perbaikan motor untuk pelanggan [isi: sekitar area/langganan tetap] di [isi: lokasi]. Pelanggan datang melalui [isi: walk-in/langganan/rujukan]. Dalam 6 bulan terakhir omzet rata-rata Rp [isi] per bulan dengan laba bersih sekitar Rp 6.500.000 per bulan (berdasarkan [isi: catatan/pembukuan]).

Keunggulan & peluang
[isi: pelanggan tetap, servis yang sering tertunda karena alat kurang, dsb — hanya fakta nyata]

Kebutuhan dana
Pinjaman Rp 75.000.000 untuk kompresor & alat bengkel (Rp 30.000.000) dan stok sparepart (Rp 45.000.000). Dana ini diperkirakan [isi: mempercepat servis / menambah jenis layanan / mengurangi waktu tunggu part].

Kemampuan membayar
Dengan laba bersih Rp 6.500.000 per bulan dan perkiraan cicilan Rp 2.281.645 (simulasi anuitas 6% efektif, 36 bulan), porsi cicilan sekitar 35,1% dari laba bersih.
```

### 5. Checklist dokumen
**Syarat inti [Permenko 1/2026 Pasal 34]**
- [ ] KTP-el pemohon (NIK)
- [ ] NIB dari OSS **atau** surat keterangan usaha dari kelurahan/desa
- [ ] Usaha sudah berjalan ≥ 6 bulan (3 tahun ✔)
- [ ] **NPWP — wajib**, karena pinjaman > Rp50 juta (Pasal 34 ayat 1 huruf d)
- [ ] Belum pernah menerima kredit **komersial produktif** (kecuali kredit konsumsi, ultra mikro ≤Rp20jt, pinjaman fintech)

**Umum diminta bank (cek ke BRI)**
- [ ] Kartu Keluarga, KTP pasangan & surat nikah (bila menikah)
- [ ] Pas foto
- [ ] Foto bengkel, alat, aktivitas servis
- [ ] Catatan penjualan/pembukuan 6–12 bulan terakhir
- [ ] Mutasi rekening 3–6 bulan
- [ ] Nota/penawaran harga kompresor & alat, daftar supplier sparepart
- [ ] Hitungan laba bersih bulanan (sudah dipakai di simulasi ini)

**Riwayat kredit**
- [ ] Cek SLIK OJK sendiri dulu, pastikan kolektibilitas lancar
- [ ] Kalau pernah punya kredit lama yang sudah lunas tapi masih tercatat → siapkan surat keterangan lunas/roya

**Hak Anda (penting, sampai ke bank penyalur manapun):**
- Plafon Rp 75 juta ≤ Rp100 juta → bank **tidak boleh** minta agunan tambahan di luar usaha/objek yang dibiayai (Pasal 20 ayat 1).
- Uang cair harus **sama** dengan nilai di akad, tanpa potongan (Pasal 13 ayat 2).
- Siapa pun yang menjanjikan "pasti cair" dengan imbalan/fee → tolak, KUR cuma diajukan langsung ke bank.

### 6. Langkah berikutnya
1. Cek SLIK OJK Anda sendiri lewat layanan resmi OJK, pastikan statusnya lancar.
2. Siapkan NPWP (wajib karena di atas Rp50 juta) kalau belum punya.
3. Pertimbangkan turunkan plafon ke ±Rp 64 juta dulu, atau beli alat dulu lalu stok bertahap — biar cicilan di zona aman.
4. Datangi unit BRI terdekat, minta **tabel angsuran resmi** dan rincian biaya (asuransi, materai, notaris).

Catatan: ini simulasi, bukan penawaran atau jaminan persetujuan kredit — keputusan & angka final ada di BRI.
Dasar: Permenko Perekonomian 1/2026 (dicek per 2026-09-23). Ketentuan bisa berubah, konfirmasi ke BRI.

Ringkas: cicilan Rp 2.281.645/bulan, makan 35,1% laba kakak — agak berat (🟡), bukan "tidak aman" tapi cukup sesak kalau bulan sepi. Kalau mau lebih aman, turunkan plafon sekitar Rp 64 juta dulu atau pisah pembelian jadi dua tahap.
~~~~

### Verifikasi (Python independen)
- Anuitas 6%/th, 36 bln, Rp75 jt: cicilan **Rp2.281.645**, total bunga **Rp7.139.231** ✔ (SEBELUM membulatkan ≈2.281.000 / ≈7,1 jt ✔). Rasio 2.281.645 / 6.500.000 = **35,1%** ✔.
- Flat 6% ilustrasi: 75 jt/36 + 75 jt × 0,5% = **Rp2.458.333**, bunga 13,5 jt ✔. Plafon maks pada rasio 30%: **Rp64.098.482** ≈ "Rp64.098.000" ✔.
- SEBELUM: pecah fasilitas — investasi 30 jt/60 bln **Rp579.984** ✔ + modal kerja 45 jt/36 bln **Rp1.368.987** ✔ = **Rp1.948.971 (30,0%)** ✔ — saran bagus dan benar.
- Aturan: NPWP wajib > Rp50 juta ✔ kedua sisi. SEBELUM menyebut agunan tambahan "biasanya nggak wajib … bisa beda kebijakan per cabang" — lemah: untuk plafon ≤ Rp100 juta penyalur **tidak boleh** meminta agunan tambahan; dokumen bank (KK, foto, catatan keuangan) dicampur dengan syarat resmi tanpa pembeda. SESUDAH memisahkan syarat resmi (dengan pasal) vs "cek ke BRI", menyebut hak debitur (tanpa agunan tambahan, nilai cair = nilai akad), membedakan anuitas vs flat dengan angka, plafon aman, profil usaha siap salin, dan disclaimer.
- Kekurangan kecil SESUDAH: sangat panjang untuk chat WA/Telegram; tidak menghitung opsi pecah fasilitas investasi 60 bulan seperti SEBELUM (hanya menyebutkan "tanyakan digabung/dipisah").

### Skor
| | SEBELUM | SESUDAH |
|---|---:|---:|
| Skenario 1 | 7,5 | 9 |

## Skenario 2 — Jebakan aturan terbaru: KUR Mikro ke-3 warung sembako, "6% flat", calo fee 5%

**Pesan pengguna:**
> Kak aku punya warung sembako, udah 2 kali dapet KUR Mikro BRI (yg terakhir bunganya 7%), sekarang udah lunas. Mau ajuin KUR Mikro lagi Rp 50.000.000 tenor 2 tahun. Kata AO bunganya 6% flat, bener ga itu murah? Terus ada orang nawarin jasa pasti cair asal bayar fee 5%, ambil ga ya?

**SEBELUM (tanpa skill)** — tools: tool_search, web_fetch, tool_call (pencarian web gagal)
~~~~text
Oke, dua hal ya — bunganya, sama tawaran "jasa pasti cair" itu. (Note: barusan coba cek data terbaru via web tapi search lagi down di sisi tool, jadi ini based on pengetahuan umum soal skema KUR — tetep aku saranin konfirmasi angka resminya ke AO/kur.go.id sebelum tanda tangan, karena plafon & suku bunga KUR itu diatur pemerintah dan bisa direvisi tiap tahun.)

**Soal bunga 6%**
- Itu bukan "diskon spesial" dari AO — 6% efektif/tahun itu memang suku bunga resmi KUR Mikro yang disubsidi pemerintah, berlaku buat semua debitur yang eligible, udah dari sekitar 2020 dan bertahan di angka segitu. Punyamu yang dulu 7% itu tarif versi lama (sebelum diturunkan), jadi wajar sekarang lebih rendah.
- Satu hal yang perlu kamu klarifikasi: AO bilang "6% flat" — pastikan maksudnya "6% efektif per tahun" (istilah resmi KUR), bukan metode hitung flat murni yang beda cara hitungnya dan bisa bikin beban bunga riil lebih tinggi dari yang kamu kira. Minta aja simulasi angsuran bulanan tertulis (pokok + bunga) sebelum akad, biar ketahuan persis total yang kamu bayar selama 2 tahun.
- Plafon 50 juta buat KUR Mikro juga masih dalam batas wajar untuk nasabah lunas 2x (biasanya malah pintu buat naik ke plafon lebih tinggi lagi ke depan kalau lancar).
- Kesimpulan: gak usah curiga sama angka 6%-nya, itu memang murah secara wajar (program pemerintah), bukan jebakan. Yang perlu dicek cuma istilah "flat" tadi dan rincian angsurannya.

**Soal jasa "pasti cair" fee 5%**
- JANGAN diambil. Ini pola penipuan klasik di sekitar KUR/pinjaman bank. KUR itu program subsidi, prosesnya lewat AO bank langsung dan resminya gak ada biaya provisi/jasa percepat — karena justru sudah disubsidi pemerintah.
- Gak ada pihak di luar bank yang bisa "menjamin pasti cair", karena keputusan approve tetap di analisa kredit bank (karakter, kapasitas usaha, dll), bukan soal bayar fee ke calo.
- Risiko kalau ambil: duit fee 2,5 juta (5% dari 50jt) raib tanpa hasil, atau lebih parah — data KTP/KK kamu disalahgunakan buat ajuin pinjaman lain (pinjol dll) atas namamu tanpa kamu sadar.
- Kalau mau lebih cepat cair, cara sah: lengkapi dokumen dari awal (KTP, KK, NIB/izin usaha, mutasi rekening/catatan omzet, kalau perlu agunan tambahan), dan follow up langsung ke AO/unit BRI-nya. Itu udah paling efektif, gratis, dan legal.
- Kalau mau lapor penawaran itu, bisa ke OJK via 157 atau kontak157@ojk.go.id.

Intinya: lanjut aja proses resmi lewat AO BRI-mu, tapi minta rincian angsuran tertulis. Tolak jasa fee 5% itu — itu scam, bukan jalan pintas.
~~~~

**SESUDAH (dengan skill)** — tools: read, ls, exec (skill terpakai: `scripts/simulasi_kur.py`)
~~~~text
Oke, dua pertanyaan ini penting banget — saya cek satu-satu.

## 1. "Bunga 6% flat" — itu bukan murah, itu justru lebih mahal

Saya hitung pakai angka plafon Rp 50 juta, tenor 24 bulan (2 tahun):

| | Flat 6%/tahun |
|---|---:|
| Cicilan/bulan | Rp 2.333.333 |
| Total bunga | Rp 6.000.000 |
| **Setara bunga efektif** | **±11,13%/tahun** |

⚠️ Ini kuncinya: KUR itu **bunganya ditetapkan sebagai bunga efektif**, bukan flat (Permenko Perekonomian 1/2026 Pasal 37). Kalau bank bilang "flat 6%", itu sebenarnya **hampir dua kali lipat** lebih mahal dari batas bunga resmi KUR Mikro (6-7% efektif/tahun). Bandingkan: 6% efektif yang benar untuk tenor 24 bulan itu setara flat hanya **±3,2%**, bukan 6%.

**Jadi sebelum lanjut, tanyakan tegas ke AO:** *"Itu 6% flat atau 6% efektif?"* Minta juga tabel angsuran resminya tertulis. Kalau memang benar-benar flat 6%, itu di luar ketentuan KUR bersubsidi dan kakak berhak menolak/komplain — kemungkinan AO salah ngomong (sering ketukar) atau yang ditawarkan bukan skema KUR yang sebenarnya.

## 2. Ada masalah lain yang lebih mendasar: ini akad ke-3

Warung sembako = sektor **perdagangan**, dan kakak sudah 2x KUR Mikro (akad ke-1 & ke-2, terakhir bunga 7% — ini cocok banget dengan pola "akad ke-2 dagang non-ekspor = 7%" di aturan). Nah:

> **Permenko 1/2026 Pasal 37:** KUR Mikro sektor perdagangan non-ekspor **paling banyak 2 kali akad**. Akad ke-3 **tidak tersedia** di jenis KUR Mikro.

Artinya kalau ini pengajuan KUR Mikro ke-3 untuk warung sembako, secara aturan **tidak bisa lagi di jalur KUR Mikro** — kecuali kakak "naik kelas" ke KUR Kecil (plafon >Rp100 juta, bunga akad pertama = bunga mikro terakhir +1% = 8%). Ini perlu dikonfirmasi langsung ke AO/cabang: apakah yang ditawarkan ini benar KUR Mikro akad ke-3 (yang seharusnya tidak ada), atau sebenarnya produk lain yang "dibungkus" nama KUR.

**Ini sinyal untuk lebih hati-hati**, terutama digabung dengan poin bunga flat yang aneh di atas.

## 3. Jasa "pasti cair" fee 5% — JANGAN diambil

Ini tolong dihindari, beberapa alasan:
- **Rp 50 juta × 5% = Rp 2.500.000** langsung hilang sebelum uang KUR cair — itu beban tambahan yang signifikan.
- Per **Pasal 13 ayat 2 Permenko 1/2026**: jumlah KUR yang kakak terima **harus sesuai nilai di akad** — tidak boleh ada potongan apa pun dari pihak manapun.
- **Tidak ada pihak di luar bank yang bisa menjamin kredit disetujui.** Yang memutuskan hanya bank penyalur lewat proses kelayakan & SLIK OJK. Siapa pun yang menjanjikan "pasti cair" dengan bayar fee di depan, itu pola klasik **calo/penipuan**, bukan layanan resmi.
- Kalau orang itu masih mendesak atau ini perilaku berulang, laporkan ke cabang bank atau kontak OJK (157 / konsumen@ojk.go.id).

## Yang sebaiknya kakak lakukan sekarang
1. Tanya AO langsung: *"6% itu flat atau efektif? Boleh minta tabel angsuran resmi?"*
2. Tanya juga: *"Untuk warung sembako yang sudah 2x KUR Mikro, pengajuan ini masuk KUR Mikro akad ke-3 atau naik ke KUR Kecil?"* — dua ini jenis & bunga beda.
3. Jangan bayar siapa pun untuk "jamin cair".
4. Kalau mau, kirim **laba bersih per bulan** warung — saya bisa hitung cicilan yang benar (anuitas, bunga efektif resmi) dan cek apakah Rp 50 juta/24 bulan ini aman buat kas warung, plus siapkan checklist & rencana dananya.

Catatan: ini simulasi & info aturan, bukan keputusan kredit — tetap konfirmasi final ke bank penyalur.
~~~~

### Verifikasi
- Flat 6%, Rp50 jt, 24 bln: cicilan **Rp2.333.333**, bunga Rp6.000.000 ✔; setara efektif **11,13%/th** ✔ (dihitung ulang). 6% efektif 24 bln setara flat **±3,18%** ✔ ("±3,2%").
- Permenko 1/2026: KUR Mikro perdagangan non-ekspor **maks. 2 akad**, akad ke-2 = 7% → pengguna (2× Mikro, terakhir 7%) **tidak bisa** KUR Mikro ke-3 ✔ (hanya SESUDAH yang menangkap). Naik ke KUR Kecil (> Rp100 jt) dengan bunga Mikro terakhir + 1% = 8% ✔ (sesuai `references/regulasi.md`).
- **SEBELUM keliru di tiga hal:** (1) "gak usah curiga sama angka 6%-nya, itu memang murah" — bila benar flat 6%, beban setara ±11% efektif; (2) "7% itu tarif versi lama" — salah, 7% adalah tarif akad ke-2 perdagangan di aturan 2026; (3) tidak tahu batas 2 akad, malah menyebut 50 jt "pintu naik plafon". Juga menyarankan "kalau perlu agunan tambahan" untuk plafon 50 jt (bertentangan dengan larangan agunan tambahan ≤ Rp100 jt) dan menyatakan pasti "resminya gak ada biaya provisi" (belum terverifikasi). Penolakan calo ✔, kanal OJK 157 ✔.
- SESUDAH: semua angka benar; penolakan calo dengan dasar nilai cair = nilai akad (Pasal 13 ayat 2) ✔; meminta laba bersih sebelum menilai kemampuan bayar (sesuai aturan tanya sekali).

### Skor
| | SEBELUM | SESUDAH |
|---|---:|---:|
| Skenario 2 | 4,5 | 9 |

## Ringkasan
| Skenario | SEBELUM | SESUDAH |
|---|---:|---:|
| 1. Bengkel KUR 75 jt | 7,5 | 9 |
| 2. KUR Mikro ke-3 + "6% flat" + calo (jebakan) | 4,5 | 9 |
| **Rata-rata** | **6,0** | **9,0** |

**VERDIK: LULUS** — sesudah ≥ 8, jelas lebih baik dari sebelum, tanpa kesalahan fakta/angka.

### Cacat untuk pembuat (bukti + saran)
1. (Minor) Balasan S1 sangat panjang (6 bagian + profil usaha) untuk satu pertanyaan chat. Saran: untuk pertanyaan "cicilan berapa / aman ga / dokumen apa", tampilkan bagian 1, 2, 5, 6 dulu dan tawarkan profil usaha & rencana dana sebagai lanjutan.
2. (Minor) Saat rasio > 30% dan dana campuran inv/mk, script belum menghitung alternatif "pisah akad: investasi tenor 60 bulan" (model dasar justru menghitungnya: Rp1.948.971 = 30,0%). Saran: tambahkan keluaran alternatif pisah fasilitas di `simulasi_kur.py`.

### Cuplikan jualan (jujur)
- "AO bilang '6% flat'? AI biasa bilang 'itu murah'. Skill ini menghitung: flat 6% = setara ±11% efektif, padahal KUR resmi 6% efektif (setara flat ±3,2%) — dan mengingatkan bahwa KUR Mikro dagang maksimal 2 kali akad (Permenko 1/2026)."
- "Cicilan Rp2.281.645 = 35,1% laba → 🟡 BERAT, plafon aman ±Rp64 juta — plus hak Anda: plafon ≤ Rp100 juta tanpa agunan tambahan."
