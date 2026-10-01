---
name: laporan-insiden-usaha
description: Menyusun laporan insiden operasional usaha (retur/pesanan salah kirim massal, stok habis saat promo, komplain viral di medsos, mesin kasir/QRIS error, karyawan telat buka toko, data pribadi pelanggan bocor/salah kirim) berisi kronologi, dampak berangka, akar masalah tanpa menyalahkan orang (5 kenapa), tindakan cepat, rencana pencegahan dengan penanggung jawab & tenggat, draf permintaan maaf ke pelanggan, dan ringkasan singkat untuk WA tim/pemilik; untuk kebocoran data pribadi ditambah tenggat pemberitahuan 3×24 jam UU PDP Pasal 46 dan draf pemberitahuan ke pelanggan terdampak. Gunakan saat pengguna minta laporan insiden, postmortem toko/usaha, kronologi kejadian, incident report UMKM, draf minta maaf ke pelanggan setelah masalah operasional, atau data breach notification UMKM.
---

# Laporan Insiden Usaha

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

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
4. **Tindakan cepat**: apa yang sudah/perlu dilakukan SEKARANG untuk menghentikan kerugian lanjutan (mis. hubungi kurir, hentikan promo sementara, restart mesin kasir, ganti channel bayar cadangan). **Hubungi proaktif SEMUA yang terdampak, bukan hanya yang sudah komplain** — mis. 18 paket tertukar tapi baru 4 yang komplain → rencanakan pesan ke 14 pembeli lainnya juga, sebelum mereka kecewa duluan.
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
7. **Susun draf permintaan maaf ke pelanggan**: sopan, mengakui masalah secara spesifik, tanpa menyalahkan pelanggan, tanpa janji berlebihan (jangan janji "tidak akan pernah terjadi lagi" — janji "kami sedang benahi [X]"), sertakan langkah konkret yang sudah/akan dilakukan untuk pelanggan yang terdampak. Sertakan juga versi pendek untuk DM. **Pilih kanal sesuai asal pelanggan:** pembeli marketplace → chat marketplace per pesanan; pelanggan WA → chat WA pribadi; jangan sarankan broadcast/status WA untuk mengumumkan masalah yang hanya menyangkut sebagian pelanggan (apalagi kebocoran data). Siapkan dua versi bila perlu: untuk yang sudah komplain dan untuk yang terdampak tapi belum komplain (proaktif).
8. **Susun ringkasan singkat untuk tim/pemilik via WA** (format tebal-pendek, siap tempel): apa yang terjadi, dampak, status sekarang, tindakan pencegahan + siapa pegang apa.
9. Jika kejadian di luar cakupan (mengancam nyawa, kebakaran, kecelakaan kerja, ancaman pidana serius) → hentikan, sampaikan bahwa ini di luar cakupan skill dan arahkan ke pihak berwenang/profesional yang tepat, jangan paksakan format ini.

## Format Output
Berikan dalam urutan ini (boleh dipersingkat untuk kejadian kecil, tapi urutan tetap):

```
# Laporan Insiden: [Judul singkat kejadian]

**Tanggal kejadian:** [tanggal] · **Ketahuan:** [jam] · **Status:** [Selesai / Masih ditangani]

## Kronologi
[HH:MM] — [kejadian]
[HH:MM] — [kejadian]
...

## Dampak
- Pelanggan/pesanan terdampak: [angka atau [isi: jumlah]]
- Kerugian/omzet: [angka atau [isi: jumlah]]
- Lainnya: [operasional, reputasi, dll]

## Akar Masalah (5 Kenapa)
1. Kenapa [gejala]? → ...
2. ...
**Akar masalah:** [satu kalimat, fokus sistem/proses]

## Tindakan Cepat (sudah/sedang dilakukan)
- [tindakan]

## Rencana Pencegahan
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
- **Tidak mengarang angka.** Semua dampak (jumlah pesanan, kerugian, waktu) harus dari input pengguna. Yang tidak diberikan ditandai `[isi: ...]`, tidak diisi kira-kira.
- **Bukan nasihat hukum, bukan nasihat K3/keselamatan, bukan kalkulator/skrining medis apa pun.** Untuk kebocoran data pribadi, skill ini **menyebut fakta pasal apa adanya** (UU 27/2022 Pasal 46: tertulis, paling lambat 3×24 jam, ke subjek data & lembaga), menghitung tenggatnya, dan menyiapkan draf — tetapi penerapan pada kasus tertentu tetap ditandai **PERLU REVIEW HUKUM** dan diarahkan ke konsultan hukum/DPO. Tidak mengarang alamat/formulir lembaga.
- **Tidak membantu menyembunyikan kebocoran data pribadi.** Bila pengguna minta tidak memberi tahu pelanggan terdampak, skill mengoreksi dengan sopan (lihat Langkah 6) dan tetap menyiapkan draf pemberitahuan.
- **Di luar cakupan:** kejadian yang mengancam keselamatan jiwa, kebakaran, kecelakaan kerja berat, dugaan tindak pidana (pencurian besar, kekerasan) — untuk kejadian ini skill berhenti dan mengarahkan ke pihak berwenang/profesional, tidak memaksakan format laporan insiden usaha biasa.
- **Draf permintaan maaf tidak pernah membuat janji yang tidak bisa dipastikan** (mis. kompensasi, tenggat perbaikan pasti) kecuali pengguna sendiri yang menyebutkannya.
