---
name: laporan-insiden-usaha
description: Menyusun laporan insiden operasional usaha (retur/pesanan salah kirim massal, stok habis saat promo, komplain viral di medsos, mesin kasir/QRIS error, karyawan telat buka toko, data pribadi pelanggan bocor/salah kirim) berisi kronologi, dampak berangka, akar masalah tanpa menyalahkan orang (5 kenapa), tindakan cepat, rencana pencegahan dengan penanggung jawab & tenggat, draf permintaan maaf ke pelanggan, dan ringkasan singkat untuk WA tim/pemilik; untuk kebocoran data pribadi ditambah tenggat pemberitahuan 3×24 jam UU PDP Pasal 46 dan draf pemberitahuan ke pelanggan terdampak. Gunakan saat pengguna minta laporan insiden, postmortem toko/usaha, kronologi kejadian, incident report UMKM, draf minta maaf ke pelanggan setelah masalah operasional, atau data breach notification UMKM.
---

# Laporan Insiden Usaha

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya (kecuali di kanal chat: lampirkan berkasnya, jangan menyebut jalur folder), dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

> **Aturan balasan (kanal chat: Telegram/WhatsApp):** laporan ditulis utuh di chat, tanpa kata proses (skill, script, file, path, folder, JSON, "saya cek", "menjalankan"). Bila jawaban lebih dari **4.000 karakter**, pecah berdasar bagian dengan judul jelas (mis. "(1/3) Kronologi & Dampak", "(2/3) Penyebab & Tindakan", "(3/3) Draf Maaf & Ringkasan WA"; jangan memotong di tengah bagian) **atau** lampirkan laporan lengkap sebagai berkas dan kirim ringkasannya di chat. Jalur folder tidak pernah disebut; bila berkas tidak bisa dilampirkan, pakai pemecahan per bagian dan tawarkan "balas 'kirim file'".

## Tujuan
Mengubah kejadian buruk operasional (bukan bencana besar, bukan tuntutan hukum) jadi satu dokumen rapi: apa yang terjadi, siapa/berapa yang terdampak, kenapa bisa terjadi (tanpa berburu kambing hitam), apa yang sudah dilakukan, dan apa yang dilakukan supaya tidak terulang — plus draf siap kirim (permintaan maaf ke pelanggan, ringkasan ke tim/pemilik via WA).

## Kapan digunakan
- Pesanan salah kirim/tertukar massal, retur menumpuk
- Stok habis mendadak saat promo/live/flash sale
- Komplain pelanggan viral di medsos/marketplace
- Mesin kasir, aplikasi kasir, atau QRIS error saat jam sibuk
- Karyawan telat buka toko/gerai
- Data pelanggan bocor ringan (mis. file pesanan salah kirim ke grup lain, nomor WA pelanggan tersebar tanpa sengaja)
- Masalah operasional lain yang menimbulkan kerugian, komplain, atau risiko reputasi tapi **bukan** kejadian yang mengancam nyawa/butuh penanganan darurat

## Kapan TIDAK digunakan
- Notulen rapat rutin (bukan insiden) → `notulen-rapat`
- Balasan chat komplain satuan/harian (bukan insiden besar) → `balas-chat-cs`
- Laporan status kerja mingguan biasa → `laporan-status-kantor`
- Surat peringatan ke karyawan tertentu → `surat-peringatan-karyawan` (skill ini sengaja **tidak menyalahkan individu** — lihat Batasan)
- Keluhan kesehatan pelanggan/karyawan (mis. dugaan keracunan makanan): skill ini hanya menyusun kronologi, tindakan operasional (tarik/musnahkan stok terduga, catat pemasok & jam), dan komunikasi sopan. **Tidak memberi diagnosis atau saran medis, tidak menyimpulkan penyebab penyakit**; arahkan yang sakit ke fasilitas kesehatan.
- Ancaman pidana, kecelakaan kerja, atau kebakaran/bencana: skill ini hanya bantu menyusun kronologi & komunikasi dasar. **Bukan nasihat hukum, bukan nasihat K3/keselamatan.**
- Kebocoran data pribadi **tetap dikerjakan** lewat cabang khusus (Langkah 6) — termasuk kewajiban pemberitahuan 3×24 jam. Untuk kebocoran skala besar/data sensitif (kesehatan, keuangan, KTP massal), tetap susun laporan + pemberitahuan, lalu sarankan segera libatkan konsultan hukum/DPO.

## Input
Tanyakan **sekali** dalam satu pesan bila belum lengkap:
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Apa yang terjadi (kronologi kasar) | Ya | — (tanyakan) |
| Kapan (tanggal & jam mulai/ketahuan/selesai) | Ya | — (tanyakan) |
| Siapa/berapa yang terdampak (jumlah pesanan, pelanggan, atau omzet) | Tidak, tapi diminta jika ada | Ditandai `[isi: jumlah]` — **tidak pernah dikarang** |
| Bagaimana ketahuan & bagaimana ditangani sejauh ini | Tidak | Ditandai `[isi: ...]` |
| Apakah menyangkut data pribadi pelanggan (+ jam ketahuan, data apa saja, berapa orang, siapa penerimanya) | Ya, khusus dicek | Jika tidak disebut, dianggap tidak — tapi ingatkan sekali untuk dicek |
| Nama usaha/toko (untuk draf minta maaf) | Tidak | `[Nama Usaha]` |

## Langkah Kerja
1. **Kumpulkan fakta dulu, jangan simpulkan sebab dulu.** Susun kronologi berurutan waktu: kapan mulai, kapan ketahuan, kapan mulai ditangani, kapan selesai/masih berjalan. Pakai jam yang disebutkan pengguna, jangan mengarang jam.
2. **Hitung dampak dari angka yang diberikan pengguna, jangan mengira-ngira.** Jumlah pesanan/pelanggan terdampak, estimasi kerugian (jika ada angka), waktu operasional yang hilang. Kalau pengguna tidak kasih angka, tulis `[isi: jumlah]` — jangan isi angka perkiraan sendiri.
3. **Cari akar masalah pakai 5 Kenapa, arahnya ke sistem/proses, bukan ke orang.** Tanya "kenapa" berulang sampai ketemu penyebab yang bisa diperbaiki (proses, alat, SOP yang tidak ada/tidak diikuti) — bukan berhenti di "karena karyawan X lalai". Contoh arah yang benar: "kenapa salah kirim → kenapa tidak dicek ulang → kenapa tidak ada langkah cek ulang di SOP packing". Lihat `references/panduan-5-kenapa.md` untuk contoh lengkap & kalimat yang harus dihindari.
   - **Pisahkan fakta dari dugaan.** Hanya penyebab yang **disebut pengguna** (mis. "admin salin data dari sheet lama") yang boleh ditulis sebagai fakta. **Setiap langkah "kenapa" dan akar masalah yang tidak disebut pengguna WAJIB ditandai `(dugaan, perlu dikonfirmasi)`** — termasuk dugaan soal SOP ("SOP belum diperbarui"), kebiasaan kerja ("memakai file lama sebagai jalan cepat"), alat, atau beban kerja. Dugaan yang masuk akal tetap dugaan, bukan kenyataan.
   - **Akar masalah = hipotesis sampai pemilik mengonfirmasi.** Tulis "Dugaan akar masalah (belum dikonfirmasi pemilik): …", lalu tutup bagian ini dengan 1–2 pertanyaan konfirmasi singkat (mis. "Benar SOP packing belum mengatur sumber data alamat?").
4. **Tindakan cepat — dua daftar terpisah, jangan dicampur:**
   - **Sudah dilakukan:** HANYA tindakan yang **disebut pengguna** dengan kata-katanya (kutip atau parafrase setia). Tindakan yang masuk akal tapi tidak disebut (memantau paket, minta maaf ke pelanggan, kirim ulang, koordinasi tim, cek stok) **bukan** "sudah dilakukan": pindahkan ke "Disarankan (belum dilakukan)" atau tulis `[isi: tindakan yang sudah dilakukan]`.
   - **Hasil yang belum dikonfirmasi tetap ditulis belum dikonfirmasi.** Tulis persis sesuai pesan: pengguna bilang "sudah menghubungi kurir untuk membatalkan 25 pesanan" → "sudah menghubungi kurir untuk membatalkan 25 pesanan; hasil pembatalan: `[isi: berapa yang berhasil dihentikan]`", **bukan** "25 paket berhasil dibatalkan".
   - **Status yang belum diketahui** ditulis "belum ada kabar", bukan "masih dalam penanganan kurir", "sedang diproses", atau "dipantau".
   - **Disarankan (belum dilakukan):** langkah untuk menghentikan kerugian lanjutan (mis. hubungi kurir, hentikan promo sementara, restart mesin kasir, ganti channel bayar cadangan). **Hubungi proaktif SEMUA yang terdampak, bukan hanya yang sudah komplain** — mis. 18 paket tertukar tapi baru 4 yang komplain → rencanakan pesan ke 14 pembeli lainnya juga, sebelum mereka kecewa duluan (asumsi satu pesanan = satu pembeli; sebutkan asumsinya).
5. **Rencana pencegahan**: minimal 2–4 tindakan konkret, masing-masing dengan **penanggung jawab** (jabatan, bukan wajib nama pribadi) dan **tenggat** (tanggal). Kalau pengguna tidak sebut siapa, tulis `[isi: penanggung jawab]` dan `[isi: tenggat]` — jangan mengarang nama.
6. **Cabang khusus — insiden DATA PRIBADI** (nama, nomor HP/WA, alamat, riwayat belanja, foto KTP, dll. terkirim/terlihat oleh pihak yang tidak berhak, sekecil apa pun). Baca `references/insiden-data-pribadi.md`, lalu tambahkan bagian "Kewajiban Pemberitahuan Data Pribadi" yang memuat:
   - **Fakta aturan, ditulis jelas (bukan dikaburkan):** UU 27/2022 tentang Pelindungan Data Pribadi, **Pasal 46 ayat (1)**: bila terjadi kegagalan pelindungan data pribadi, pengendali data (usaha yang menyimpan data pelanggan) **wajib memberi tahu secara tertulis paling lambat 3×24 jam** kepada **subjek data (pelanggan terdampak)** dan **lembaga** pelindungan data pribadi. Ayat (2): isi minimal = data apa yang terungkap, kapan & bagaimana terungkap, upaya penanganan & pemulihan. Ayat (3): dalam hal tertentu wajib juga memberi tahu masyarakat.
   - **Tenggat dihitung** dari jam usaha mengetahui kejadian (pakai jam dari pengguna): "Ketahuan [tgl jam] → batas pemberitahuan [tgl+3 hari, jam sama]". Jika jam ketahuan tidak diberikan, tulis `[isi: jam ketahuan]` — jangan dikarang.
   - **Draf pemberitahuan tertulis ke pelanggan terdampak** (per orang, lewat kanal asal datanya: chat WA pribadi / chat marketplace per pesanan / email) berisi 3 unsur ayat (2) + kontak yang bisa dihubungi + saran kewaspadaan (mis. hati-hati telepon/chat yang mengaku dari toko). Bukan broadcast ke semua kontak.
   - **Catatan untuk lembaga:** ringkasan yang sama dalam format tertulis untuk lembaga pelindungan data pribadi **bila sudah terbentuk/ada kanal resminya** — minta pengguna cek kanal resmi (situs Komdigi/lembaga PDP); jangan mengarang alamat/formulir. Bila kanal belum ada, simpan catatan bertanggal sebagai bukti itikad baik.
   - **Penanganan penerima yang tidak berhak:** hubungi orang/grup yang menerima data, minta hapus dan konfirmasi tertulis.
   - **Jika pemilik ingin menyembunyikan** ("tidak usah kasih tahu pelanggan", "diam saja", "toh cuma sedikit"): **jangan mengikuti begitu saja dan jangan mencatatnya sebagai "keputusan sadar" lalu menutup kasus.** Koreksi dengan sopan dan tenang, mis.: "Saya paham niatnya supaya tidak bikin heboh. Tapi untuk kebocoran data pribadi, UU PDP Pasal 46 mewajibkan pemberitahuan tertulis ke pelanggan terdampak paling lambat 3×24 jam. Memberi tahu dengan jujur dan cepat justru biasanya menjaga kepercayaan — drafnya sudah saya siapkan, tinggal dicek." Status laporan tetap **"Masih ditangani"** sampai pemberitahuan terkirim.
   - **Nada:** tidak menakut-nakuti — jangan menyebut ancaman sanksi/denda/pidana kecuali pengguna bertanya; fokus ke langkah yang harus dilakukan dan tenggatnya.
   - Tutup bagian ini dengan: "⚠️ PERLU REVIEW HUKUM — ini ringkasan aturan, bukan nasihat hukum. Untuk kepastian penerapan pada kasus Anda (apakah termasuk kegagalan pelindungan, siapa lembaganya, format laporan), konsultasikan ke konsultan hukum/DPO; untuk kebijakan privasi lengkap → `kebijakan-privasi-pdp`."
7. **Susun draf permintaan maaf ke pelanggan**: sopan, mengakui masalah secara spesifik, tanpa menyalahkan pelanggan, tanpa janji berlebihan (jangan janji "tidak akan pernah terjadi lagi" — janji "kami sedang benahi [X]"), sertakan langkah konkret yang sudah/akan dilakukan untuk pelanggan yang terdampak. Sertakan juga versi pendek untuk DM. **Pilih kanal sesuai asal pelanggan:** pembeli marketplace → chat marketplace per pesanan; pelanggan WA → chat WA pribadi; jangan sarankan broadcast/status WA untuk mengumumkan masalah yang hanya menyangkut sebagian pelanggan (apalagi kebocoran data). Siapkan dua versi bila perlu: untuk yang sudah komplain dan untuk yang terdampak tapi belum komplain (proaktif). **Hanya fakta yang disebut pengguna yang masuk draf**; dugaan penyebab tidak dimasukkan (tulis "kami sedang menelusuri penyebabnya").
8. **Susun ringkasan singkat untuk tim/pemilik via WA** (format tebal-pendek, siap tempel): apa yang terjadi, dampak, status sekarang (yang belum diketahui: "belum ada kabar"), tindakan pencegahan + siapa pegang apa. Tindakan "sudah dilakukan" hanya yang disebut pengguna; dugaan penyebab tidak ikut.
9. Jika kejadian di luar cakupan (mengancam nyawa, kebakaran, kecelakaan kerja, ancaman pidana serius) → hentikan, sampaikan bahwa ini di luar cakupan skill dan arahkan ke pihak berwenang/profesional yang tepat, jangan paksakan format ini.
10. **Cek konsistensi angka sebelum mengirim** (semua bagian: laporan, draf maaf, ringkasan WA):
   - Daftar dulu angka kunci dari pengguna (total terdampak, sudah komplain, belum komplain, dibatalkan, terlanjur jalan, kerugian) dan pakai **angka serta satuan yang sama** di setiap bagian; jangan menukar paket/pesanan/pelanggan.
   - Hitung ulang: total terdampak = sudah komplain + belum komplain; total = dibatalkan + terlanjur jalan (bila keduanya disebut); sisa yang dihubungi proaktif = total − sudah komplain. Contoh: 40 terdampak, 5 komplain → **35** belum komplain di semua bagian, bukan 15 di satu tempat dan 35 di tempat lain.
   - Bila angka dari pengguna sendiri tidak cocok (mis. dibatalkan 25 + terlanjur jalan 10 ≠ total 40), jangan memilih salah satu: tulis `[isi: ...]` dan tanyakan.
   - **Satu fakta = satu kalimat.** Jangan menumpuk beberapa fakta dalam satu kalimat dan jangan mengulang fakta yang sama dengan angka berbeda di bagian lain.
   - Periksa ulang: tidak ada tindakan "sudah dilakukan" di luar pesan pengguna, dan setiap sebab di luar pesan pengguna bertanda `(dugaan, perlu dikonfirmasi)`.

## Format Output
Berikan dalam urutan ini (boleh dipersingkat untuk kejadian kecil, tapi urutan tetap):

```
# Laporan Insiden: [Judul singkat kejadian]

**Tanggal kejadian:** [tanggal] · **Ketahuan:** [jam] · **Status:** [Selesai / Masih ditangani / belum ada kabar]

## Kronologi
[HH:MM] — [kejadian]
[HH:MM] — [kejadian]
...

## Dampak
- Pelanggan/pesanan terdampak: [angka atau [isi: jumlah]]
- Kerugian/omzet: [angka atau [isi: jumlah]]
- Lainnya: [operasional, reputasi, dll]

## Akar Masalah (5 Kenapa)
1. Kenapa [gejala]? → [penyebab yang disebut pengguna]
2. Kenapa ...? → ... (dugaan, perlu dikonfirmasi)
**Dugaan akar masalah (belum dikonfirmasi pemilik):** [satu kalimat, fokus sistem/proses]
Mohon konfirmasi: [1–2 pertanyaan singkat]

## Tindakan Cepat
**Sudah dilakukan (sesuai keterangan Anda):**
- [tindakan yang disebut pengguna; hasil yang belum pasti: `[isi: hasil]`]

**Disarankan (belum dilakukan):**
- [tindakan]

## Rencana Pencegahan (usulan)
| Tindakan | Penanggung jawab | Tenggat |
|---|---|---|
| ... | [jabatan] | [tanggal] |

## [Jika menyangkut data pribadi] Kewajiban Pemberitahuan Data Pribadi
- Dasar: UU 27/2022 Pasal 46 — pemberitahuan tertulis paling lambat 3×24 jam ke pelanggan terdampak & lembaga
- Ketahuan: [tgl jam] → **batas pemberitahuan: [tgl+3 hari jam sama]**
- Status: [sudah/belum dikirim ke N pelanggan] · Lembaga: [catatan siap / cek kanal resmi]
[Draf pemberitahuan ke pelanggan terdampak] · [Catatan untuk lembaga]
⚠️ PERLU REVIEW HUKUM — bukan nasihat hukum

## Draf Permintaan Maaf ke Pelanggan
[versi lengkap: email/DM/chat marketplace per pesanan]

[versi pendek: DM ke pelanggan terdampak — termasuk yang belum komplain]

## Ringkasan untuk Tim/Pemilik (WA)
*[Judul singkat]*
Apa: ...
Dampak: ...
Status: ...
Pencegahan: [tindakan] — PJ: [jabatan], tenggat [tanggal]
```

## Contoh
Lihat `examples/01-pesanan-salah-kirim-massal.md` dan `examples/02-qris-error-jam-sibuk.md` untuk kasus lengkap dari kronologi mentah sampai draf jadi.

## Batasan & Penanganan Error
- **Tidak menyalahkan individu.** Akar masalah selalu diarahkan ke proses/sistem, bukan ke nama karyawan tertentu, kecuali pengguna secara eksplisit minta bagian terpisah untuk tindak lanjut kedisiplinan — itu pun diarahkan ke `surat-peringatan-karyawan`, bukan ditulis di laporan insiden ini.
- **Tidak mengarang angka maupun tindakan.** Semua dampak (jumlah pesanan, kerugian, waktu) dan tindakan yang "sudah dilakukan" harus dari input pengguna. Yang tidak diberikan ditandai `[isi: ...]` (atau asumsi yang disebut jelas), tidak diisi kira-kira. Ini berlaku juga untuk **status dan hasil** ("berhasil dibatalkan", "masih dalam penanganan", "dipantau" hanya bila pengguna yang bilang) dan untuk **sebab** (dugaan wajib bertanda `(dugaan, perlu dikonfirmasi)`; akar masalah tetap hipotesis sampai pemilik mengonfirmasi).
- **Bukan nasihat hukum, bukan nasihat K3/keselamatan, bukan kalkulator/skrining medis apa pun.** Untuk kebocoran data pribadi, skill ini **menyebut fakta pasal apa adanya** (UU 27/2022 Pasal 46: tertulis, paling lambat 3×24 jam, ke subjek data & lembaga), menghitung tenggatnya, dan menyiapkan draf — tetapi penerapan pada kasus tertentu tetap ditandai **PERLU REVIEW HUKUM** dan diarahkan ke konsultan hukum/DPO. Tidak mengarang alamat/formulir lembaga.
- **Tidak membantu menyembunyikan kebocoran data pribadi.** Bila pengguna minta tidak memberi tahu pelanggan terdampak, skill mengoreksi dengan sopan (lihat Langkah 6) dan tetap menyiapkan draf pemberitahuan.
- **Di luar cakupan:** kejadian yang mengancam keselamatan jiwa, kebakaran, kecelakaan kerja berat, dugaan tindak pidana (pencurian besar, kekerasan) — untuk kejadian ini skill berhenti dan mengarahkan ke pihak berwenang/profesional, tidak memaksakan format laporan insiden usaha biasa.
  - Khusus **kecelakaan kerja**: cukup sebutkan bahwa pemberi kerja wajib melapor ke BPJS Ketenagakerjaan dan Dinas Provinsi/unit pengawasan ketenagakerjaan setempat paling lama 2×24 jam sejak kejadian (Permenaker 5/2021 Pasal 8 ayat 1–2, laporan tahap I), lalu arahkan ke BPJS Ketenagakerjaan/pengawas ketenagakerjaan untuk formulir & penerapannya. Jangan merujuk Permenaker 5/2018 untuk hal ini (aturan itu tentang K3 lingkungan kerja, bukan tata cara lapor kecelakaan). Skill tidak mengisi formulir K3/kecelakaan kerja.
- **Draf permintaan maaf tidak pernah membuat janji yang tidak bisa dipastikan** (mis. kompensasi, tenggat perbaikan pasti) kecuali pengguna sendiri yang menyebutkannya.
