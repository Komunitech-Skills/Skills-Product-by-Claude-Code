# Uji OpenClaw SEBELUM vs SESUDAH — spt-tahunan-op

## Cara uji
- **Tanggal:** 2026-10-01. Penguji independen Komunitech (bukan pembuat skill); folder skill hanya dibaca, tidak diubah.
- **Agent:** OpenClaw **2026.9.6** lokal (`openclaw agent --local`, tanpa Telegram/gateway), model router Komunitech **claude-sonnet-5** (sama dengan bot member), TZ Asia/Jakarta, agent terisolasi (hanya melihat home ujinya sendiri).
- **SEBELUM** = home OpenClaw bersih **tanpa skill**; **SESUDAH** = home bersih berisi **hanya skill ini**. Home dibuat ulang per skenario. Pesan identik di kedua sisi; bila agent bertanya balik, dijawab sekali dengan jawaban yang sama di kedua sisi (sesi lanjutan).
- Angka diverifikasi ulang dengan Python secara independen (dan script skill sebagai pembanding bila relevan); fakta aturan dicek terhadap aturan Indonesia yang berlaku. `tools` = alat yang tercatat berhasil dipakai agent pada giliran itu.

## Skenario 1 — Normal: karyawan pindah kerja, 2 bukti potong A1, K/2, belum lapor

**Pesan pengguna:**

> Min tahun 2025 aku pindah kerja. Kantor lama (Jan-Jun) di bukti potong A1 penghasilan neto 72.000.000, PPh 21 dipotong 1.200.000. Kantor baru (Jul-Des) neto 84.000.000, PPh 21 dipotong 1.950.000. Status aku kawin anak 2. SPT tahunan aku kurang bayar ga? berapa? aku belum lapor sama sekali

### Balasan SEBELUM (tanpa skill)

*tools: (tidak ada)*

> **Ya, kamu kurang bayar.** Ini perhitungannya:
>
> **1. Gabungkan penghasilan neto setahun (dari 2 bukti potong)**
> - Kantor lama (Jan-Jun): Rp 72.000.000
> - Kantor baru (Jul-Des): Rp 84.000.000
> - Total neto setahun: **Rp 156.000.000**
>
> **2. Kurangi PTKP (status K/2 = kawin + 2 anak)**
> - TK/0: Rp 54.000.000
> - Kawin: +Rp 4.500.000
> - 2 anak: +Rp 9.000.000 (@Rp4,5jt)
> - PTKP K/2: **Rp 67.500.000**
>
> **3. Penghasilan Kena Pajak (PKP)**
> 156.000.000 − 67.500.000 = **Rp 88.500.000**
>
> **4. PPh terutang setahun (tarif progresif UU HPP)**
> - 5% × 60.000.000 = Rp 3.000.000
> - 15% × 28.500.000 (sisanya) = Rp 4.275.000
> - Total PPh terutang: **Rp 7.275.000**
>
> **5. Bandingkan dengan yang sudah dipotong kedua kantor**
> - Dipotong kantor lama: Rp 1.200.000
> - Dipotong kantor baru: Rp 1.950.000
> - Total sudah dipotong: Rp 3.150.000
>
> **6. Kurang bayar (PPh Pasal 29)**
> 7.275.000 − 3.150.000 = **Rp 4.125.000 kurang bayar**
>
> Ini kejadian klasik pindah kerja: dua pemberi kerja masing-masing cuma hitung pajak dari penghasilan di tempat mereka saja, padahal kalau digabung penghasilanmu masuk ke lapisan tarif 15%, jadi total pajak terutang lebih besar dari total yang sudah dipotong.
>
> ⚠️ **Yang lebih urgent nih:** batas lapor SPT Tahunan OP 2025 itu 31 Maret 2026 — dan sekarang sudah 1 Oktober 2026, jadi kamu **sudah telat lapor sekitar 6 bulan**. Ada 2 sanksi tambahan di luar kurang bayar Rp 4.125.000 itu:
> 1. **Denda telat lapor SPT**: Rp 100.000 (flat, Pasal 7 UU KUP)
> 2. **Bunga keterlambatan pembayaran** kurang bayar, dihitung per bulan dari jatuh tempo (31 Maret 2026) sampai tanggal kamu bayar — tarifnya mengambang tiap bulan sesuai KMK, jadi nominalnya dihitung otomatis sistem DJP pas kamu bikin e-Billing (atau nanti muncul STP terpisah dari KPP kalau belum kebayar saat lapor).
>
> **Langkah yang perlu kamu ambil sekarang:**
> 1. Lapor pakai formulir **1770 S** (karena ada 2 pemberi kerja dalam setahun, bukan 1770 SS), gabungkan dua bukti potong 1721-A1.
> 2. Buat kode billing di DJP Online untuk PPh Pasal 29 OP (kode akun 411125, kode jenis setoran 200) — nominalnya nanti akan include bunga keterlambatan otomatis.
> 3. Bayar dulu, baru e-Filing SPT-nya (urutan: bayar → lapor).
> 4. Kalau mau, aku bisa bantu susun angka-angka buat diisi di formulir 1770 S-nya — tinggal bilang aja.

### Balasan SESUDAH (dengan skill)

*tools: read, exec*

> **Hitungan SPT Tahunan PPh OP — Tahun Pajak 2025 (status K/2)**
>
> **1. Penghasilan neto**
> | Sumber | Neto |
> |---|---|
> | A1 Kantor lama (Jan–Jun) | Rp 72.000.000 |
> | A1 Kantor baru (Jul–Des) | Rp 84.000.000 |
> | **Jumlah neto** | **Rp 156.000.000** |
>
> **2. PTKP & PKP**
> - PTKP K/2 (kawin, 2 tanggungan): Rp 67.500.000
> - PKP = 156.000.000 − 67.500.000 = **Rp 88.500.000**
>
> **3. PPh terutang (tarif Pasal 17)**
> - 5% × 60.000.000 = Rp 3.000.000
> - 15% × 28.500.000 = Rp 4.275.000
> - **Total PPh terutang: Rp 7.275.000**
>
> **4. Kredit pajak**
> - PPh 21 kantor lama: Rp 1.200.000
> - PPh 21 kantor baru: Rp 1.950.000
> - **Total kredit: Rp 3.150.000**
>
> **5. Hasil: KURANG BAYAR Rp 4.125.000** (Rp 7.275.000 − Rp 3.150.000)
>
> **Kenapa bisa kurang bayar?** Dua pemberi kerja sama-sama menghitung PPh 21 seolah itu satu-satunya penghasilanmu setahun — masing-masing memakai PTKP penuh dan tarif terendah (5%) untuk penghasilan di kantornya. Begitu digabung di SPT tahunan, total neto Rp156 juta ternyata sebagian masuk lapisan tarif 15%, jadi ada selisih yang belum terpotong. Ini wajar terjadi kalau pindah kerja di tengah tahun, bukan tanda ada kesalahan kantor.
>
> ⚠️ **Status lapor — penting:** Batas lapor SPT 2025 adalah 31 Maret 2026, dan masa penghapusan sanksi (KEP-55/PJ/2026) berakhir 30 April 2026. Sekarang sudah 1 Oktober 2026 — **batas waktu itu sudah lewat cukup jauh**. Konsekuensinya:
> - Denda telat lapor SPT Tahunan OP: Rp100.000 (ditagih via STP).
> - Kurang bayar Rp4.125.000 akan kena **bunga keterlambatan per bulan** sejak 1 April 2026 sampai dibayar (tarif bulanan KMK — tidak saya hitung di sini, bisa cukup besar karena sudah ~6 bulan).
> - Saran: segera buat kode billing dan bayar PPh Pasal 29 Rp4.125.000 + lapor SPT secepatnya untuk menghentikan akumulasi bunga tambahan.
>
> **Peta ke Coretax**
> - Neto per bukti potong → Lampiran 1 (biasanya sudah terisi otomatis dari A1)
> - Neto, PTKP, PKP, PPh terutang → Induk Bagian B & C
> - Kredit pajak, kurang bayar → Induk Bagian D & E
> - Setelah kode billing dibuat dan dibayar, SPT baru bisa dikirim
>
> **Langkah berikutnya**
> 1. Login Coretax, cek kedua A1 sudah muncul otomatis dengan neto & PPh 21 yang cocok dengan angka di atas.
> 2. Buat kode billing untuk Rp4.125.000 (ditambah bunga keterlambatan yang dihitung sistem Coretax saat itu), bayar.
> 3. Lengkapi data harta/utang per 31 Desember 2025 dan tanggungan (NIK), lalu kirim SPT.
> 4. Siapkan Rp100.000 untuk denda telat lapor (STP biasanya terbit terpisah setelah SPT masuk).
>
> **Checklist dokumen**
> - [ ] 2 lembar bukti potong A1 (kantor lama & baru)
> - [ ] Akun Coretax aktif + kode otorisasi tanda tangan
> - [ ] Daftar harta & utang per 31 Des 2025
> - [ ] NIK tanggungan (istri/anak)
> - [ ] Dana untuk bayar Rp4.125.000 + bunga keterlambatan + nanti denda Rp100.000
>
> _Ini alat bantu hitung, bukan konsultan pajak, dan saya tidak mengisi/mengirim SPT atas namamu. Karena sudah telat dan ada bunga berjalan, sebaiknya cocokkan angka final di Coretax atau hubungi Kring Pajak 1500200/konsultan pajak sebelum bayar, supaya tidak kurang/lebih bayar bunga._

### Verifikasi
Python independen: neto 72.000.000 + 84.000.000 = Rp156.000.000; PTKP K/2 = 54 + 4,5 + 2 × 4,5 = Rp67.500.000; PKP Rp88.500.000; PPh = 5% × 60 jt + 15% × 28,5 jt = 3.000.000 + 4.275.000 = **Rp7.275.000**; kredit Rp3.150.000 → **kurang bayar Rp4.125.000** ✔ (kedua sisi). Script skill (`--status K/2 --a1 72jt 1.200.000 --a1 84jt 1.950.000 --hari-ini 2026-10-01`) memberi angka & peringatan telat lapor yang sama dengan SESUDAH. Batas lapor TP 2025 = 31 Maret 2026 (UU KUP Ps. 3); denda telat lapor OP Rp100.000 (Ps. 7) ✔ kedua sisi.
- **SEBELUM:** angka benar, sadar sudah telat. **Kesalahan fakta prosedur:** menyuruh lapor dengan "formulir 1770 S" dan "e-Billing/e-Filing DJP Online" — untuk tahun pajak 2025 SPT OP sudah lewat Coretax dengan formulir tunggal (PER-11/PJ/2025; 1770/1770S dihapus). Pembeli awam akan mencari formulir yang tidak ada.
- **SESUDAH:** angka dari script (`exec` tercatat), penjelasan kenapa kurang bayar, status KEP-55/PJ/2026 (penghapusan sanksi s.d. 30 April 2026 sudah lewat), peta ke Coretax, checklist, disclaimer. Tidak ada kesalahan ditemukan.

### Skor
| Kriteria | SEBELUM | SESUDAH |
|---|---|---|
| Ketepatan angka | 9 | 9 |
| Aturan Indonesia terbaru | 4 | 9 |
| Siap pakai (langkah berikutnya) | 6 | 9 |
| Keamanan/privasi | 8 | 9 |
| Kejelasan | 8 | 9 |
| **Skor** | **6,5** | **9** |

Skill terpakai: ya (SKILL.md dibaca, `scripts/spt_op.py` dijalankan).

## Skenario 2 — Jebakan: konsultan IT freelance memakai PPh final 0,5%, tanpa pemberitahuan NPPN

**Pesan pengguna:**

> Aku konsultan IT freelance (kerja sendiri, ga punya karyawan), omzet setahun 2025 Rp380.000.000. Selama ini aku bayar pajak UMKM 0,5% tiap bulan. Status lajang ga ada tanggungan. Di SPT tahunan masih harus bayar apa lagi? Oh iya aku ga pernah kirim pemberitahuan NPPN

### Balasan SEBELUM (tanpa skill) — giliran 1

*tools: tool_search*

> Oke, aku breakdown berdasarkan aturan PPh Final UMKM (PP 23/2018 jo. PP 55/2022) karena kamu OP yang selama ini bayar 0,5% bulanan. Ada beberapa poin penting yang kayaknya belum kamu sadari:
>
> **1. Omzet kamu di bawah batas bebas pajak Rp500 juta — ini yang paling penting**
>
> Sejak PP 55/2022, khusus WP Orang Pribadi, peredaran bruto **sampai dengan Rp500 juta per tahun pajak TIDAK dikenakan PPh** sama sekali (dibebaskan, bukan cuma dikurangi tarif). Omzet kamu 2025 = Rp380.000.000 → **masih di bawah Rp500 juta**.
>
> Artinya: secara aturan, seluruh omzet 2025 kamu seharusnya **tidak terutang PPh Final 0,5%** — dari Rp0 sampai Rp380 juta itu dalam zona bebas.
>
> Konsekuensinya:
> - Kalau selama ini kamu tetap setor 0,5% tiap bulan atas omzet bulanan (tanpa menunggu akumulasi lewat Rp500 juta), kemungkinan besar itu **lebih bayar / tidak seharusnya disetor**.
> - Setoran yang sudah dibayar itu nanti **dikreditkan di SPT Tahunan**, dan kalau akumulasi setahun memang di bawah 500 juta, selisihnya bisa jadi lebih bayar (bisa dikompensasi/direstitusi).
> - Cek lagi riwayat setoran bulananmu: apakah kamu sudah menerapkan mekanisme "akumulasi omzet lewat 500 juta baru bayar" atau selama ini asal bayar 0,5% dari omzet bulanan tanpa pengecualian itu.
>
> **2. Soal "jatah" 7 tahun pakai tarif final — ini yang perlu dicek, bisa jadi krusial**
>
> Untuk WP Orang Pribadi, jangka waktu pakai tarif final 0,5% dibatasi **7 Tahun Pajak**:
> - Kalau kamu terdaftar NPWP/mulai usaha **sebelum PP 23/2018 berlaku (sebelum Juli 2018)** → jangka waktu dihitung dari 2018, jadi berakhir di **akhir 2024**. Kalau ini kasusmu, berarti **2025 kamu sudah tidak boleh lagi pakai tarif final 0,5%**, harus pindah ke tarif umum Pasal 17 (pakai pembukuan atau NPPN).
> - Kalau kamu baru terdaftar/mulai usaha **setelah Juli 2018**, dihitung dari tahun terdaftar itu — misal daftar 2020, berarti jatahnya habis akhir 2026.
>
> 👉 **Aku perlu tahu: kamu terdaftar NPWP / mulai jalanin usaha konsultan IT ini sejak tahun berapa?** Ini nentuin apakah skema final 0,5% kamu masih valid di 2025 atau sudah harus ganti skema.
>
> **3. Soal pemberitahuan NPPN — ini baru relevan KALAU jatah 7 tahun di atas sudah habis**
>
> NPPN (Norma Penghitungan Penghasilan Neto) itu skema **berbeda** dari PPh Final 0,5% PP 23. NPPN dipakai kalau kamu kena tarif umum Pasal 17 tapi tidak mau/tidak wajib pembukuan penuh — penghasilan neto dihitung pakai persentase norma sesuai KLU (kode usaha), lalu dikurangi PTKP, baru kena tarif progresif.
>
> - Selama kamu masih sah pakai tarif final 0,5% (belum lewat 7 tahun), **pemberitahuan NPPN memang tidak perlu** — jadi soal "ga pernah kirim pemberitahuan NPPN" itu belum jadi masalah.
> - Tapi **kalau ternyata jatah 7 tahun kamu sudah habis** (lihat poin 2) dan kamu mau pakai NPPN untuk 2025, pemberitahuannya wajib dikirim ke DJP **paling lambat 3 bulan pertama tahun pajak**. Untuk tahun 2025, batas itu sudah lewat (akhir Maret 2025). Kalau tidak kirim pemberitahuan dan batas waktu final sudah habis, kamu dianggap menyelenggarakan pembukuan — jadi penghasilan neto harus dihitung dari pembukuan riil (bukan norma), bukan sekadar 0,5% dari omzet.
>
> **4. Soal status lajang tanpa tanggungan (PTKP)**
>
> PTKP **tidak dipakai** di skema PPh Final 0,5% (dihitung dari omzet bruto, bukan neto dikurangi PTKP). PTKP baru relevan kalau kamu pindah ke tarif umum Pasal 17 (karena jatah final habis, atau karena pilih sendiri).
>
> **5. SPT Tahunan tetap wajib lapor**
>
> Meski nihil/lebih bayar, SPT Tahunan 1770 **tetap wajib dilaporkan** paling lambat 31 Maret. Omzet Rp380 juta dilaporkan di bagian "Penghasilan yang Dikenakan PPh Final/Dibebaskan". Kalau tidak ada penghasilan lain di luar usaha ini (gaji, bunga non-final, dll) dan memang masih dalam jatah final, PPh Pasal 29 (kurang bayar) kemungkinan besar **nihil, bahkan bisa lebih bayar**.
>
> ---
>
> **Yang aku butuh dari kamu buat kasih kepastian:**
> 1. Sejak tahun berapa kamu terdaftar NPWP / mulai usaha konsultan IT ini?
> 2. Selama 2025, apakah kamu setor 0,5% tiap bulan dari omzet bulanan tanpa mengecualikan yang di bawah akumulasi Rp500 juta, atau sudah pakai mekanisme pembebasan itu?
>
> Kalau kamu kasih tahu dua hal itu, aku bisa hitungin lebih pasti berapa yang kurang/lebih bayar dan skema apa yang seharusnya kamu pakai di SPT Tahunan 2025 ini.

### Balasan SESUDAH (dengan skill) — giliran 1

*tools: read*

> Sebelum hitung, ada temuan penting yang perlu kamu tahu dulu:
>
> **Konsultan IT = pekerjaan bebas (keahlian/profesi), bukan "usaha" biasa.** Menurut PP 55/2022 s.t.d.d. PP 20/2026 Pasal 56, PPh final 0,5% (PP 55) itu khusus untuk usaha (dagang/produksi/jasa biasa). Pekerjaan bebas berbasis keahlian — termasuk konsultan — **tidak boleh** pakai skema 0,5% final. Harusnya dari awal kamu pakai NPPN (Norma Penghitungan Penghasilan Neto) atau pembukuan, lalu kena tarif progresif Pasal 17.
>
> Ini artinya setoran 0,5% bulanan yang sudah kamu bayar selama 2025 **secara aturan bukan basis yang tepat** untuk penghasilan konsultan IT. Soal pembetulan setoran bulanan itu di luar cakupan saya (itu ranah `pph-final-umkm`/konsultan pajak) — tapi untuk SPT Tahunan, saya akan hitung versi yang **seharusnya** (NPPN atau pembukuan), bukan lanjutkan basis 0,5%.
>
> Ditambah lagi: kamu belum pernah kirim pemberitahuan NPPN ke DJP (batasnya 31 Maret tahun berjalan). Secara aturan, tanpa pemberitahuan ini DJP menganggap WP memilih pembukuan — jadi hasil NPPN nanti sifatnya **simulasi saja**, bukan posisi resmi yang aman. ⚠️ Ini kasus yang cukup signifikan — saya sarankan setelah dapat gambaran angka dari saya, kamu konsultasi ke Kring Pajak 1500200 atau konsultan pajak untuk strategi pembetulan (mungkin perlu pembetulan SPT Masa 2025 + kemungkinan sanksi).
>
> Supaya saya bisa hitung, boleh dijawab (nomor 1-5, kalau mau cepat jawab aja yang kamu tahu, sisanya saya anggap 0):
>
> 1. **Domisili usaha** di kota mana? (ibukota provinsi besar / ibukota provinsi lain / daerah lainnya — ini pengaruh ke persen norma NPPN)
> 2. **Kode KLU/jenis usaha** di lampiran PER-17/PJ/2015 yang paling cocok dengan jasa konsultan IT kamu (misal konsultasi software, infrastruktur, dsb) — bisa kamu cek sendiri, atau sebut detail jasanya nanti saya bantu arahkan ke kategori yang relevan (saya tidak mau menebak persennya).
> 3. Omzet Rp380 juta itu **murni dari jasa konsultan IT** (pekerjaan bebas), bukan campur usaha dagang/lain?
> 4. Selama ini kamu **punya catatan pembukuan** (rincian biaya operasional real, bukan cuma omzet)? Kalau ada dan lengkap, bisa dipakai metode pembukuan (bisa lebih menguntungkan daripada NPPN tergantung biaya riil).
> 5. Ada **zakat mandiri** ke BAZNAS/LAZ resmi, atau PPh 22/23 yang sudah dipotong pihak lain (misal klien korporat potong PPh 23 atas jasa)?
>
> Begitu saya dapat minimal jawaban #1-3, saya bisa hitung simulasinya.

**Jawaban pengguna (sama di kedua sisi):**

> NPWP aku dari 2019. Aku setor 0,5% dari omzet tiap bulan mulai Januari, total setahun Rp1.900.000. Domisili Bandung. Kerjaanku bikin & maintain software/website buat klien, murni jasa konsultan IT, ga ada dagang. Ga ada pembukuan, cuma catatan omzet. Ga ada zakat, klien ga pernah motong pajak. KLU aku ga tau, tolong bantu aja

### Balasan SEBELUM — giliran 2

*tools: web_fetch, tool_call*

> Oke, dengan info lengkap ini (NPWP 2019, Bandung, jasa pemrograman/software murni, pencatatan saja, lajang TK/0), aku bisa kasih jawaban yang lebih pasti. Ada beberapa temuan penting — termasuk satu yang kemungkinan menguntungkan kamu.
>
> **1. Jatah 7 tahun tarif final 0,5% kamu: 2025 adalah TAHUN TERAKHIR**
>
> NPWP terdaftar 2019 (setelah PP 23/2018 berlaku), jadi hitungan 7 tahun jatah final OP dimulai dari tahun terdaftar: 2019‑2020‑2021‑2022‑2023‑2024‑**2025**. Jadi:
> - **2025 masih sah pakai PPh Final 0,5%** — aman, tidak ada masalah di sini.
> - **Mulai Tahun Pajak 2026, kamu WAJIB pindah ke tarif umum (Pasal 17)**, tidak bisa lagi pakai 0,5% final. Ini penting untuk rencana ke depan (lihat poin 4).
>
> **2. Omzet 380 juta di bawah batas bebas Rp500 juta — ini yang krusial untuk SPT 2025**
>
> Karena omzet 2025 kamu (Rp380.000.000) tidak pernah melewati Rp500.000.000 kapan pun sepanjang tahun, **seluruh penghasilan 2025 kamu sebenarnya DIBEBASKAN dari PPh Final** — bukan dikurangi tarif, tapi nol sama sekali.
>
> Setoran bulanan 0,5% yang kamu bayar (Rp1.900.000 setahun — pas 0,5% × 380 juta, jadi kelihatan kamu setor flat tanpa menerapkan pembebasan ini) **secara aturan tidak terutang**. Artinya kemungkinan besar itu kelebihan setor, bukan kewajiban yang kurang.
>
> **3. Dampaknya ke SPT Tahunan 2025:**
> - PPh Pasal 29 (kurang bayar) kamu: **NIHIL**, karena memang tidak ada PPh terutang tahun ini.
> - Rp1.900.000 yang sudah disetor berpotensi jadi **kelebihan setor pajak final** yang bisa diajukan pengembalian (restitusi "pajak yang seharusnya tidak terutang") atau dikompensasikan. Ini bukan mekanisme kredit pajak biasa karena sifatnya final — jadi aku sarankan kamu konfirmasi langsung ke AR (Account Representative) di KPP Bandung tempat kamu terdaftar atau Kring Pajak 1500200 untuk prosedur pengembaliannya, karena ini butuh permohonan khusus, bukan otomatis kebentuk dari SPT Tahunan saja.
> - PTKP (status lajang/TK0) **tidak relevan** di skema final 0,5% ini — itu baru dipakai kalau masuk tarif umum.
>
> **4. Soal NPPN — belum relevan untuk SPT 2025 ini, tapi JADI WAJIB untuk 2026**
>
> Karena 2025 masih dalam jatah final, pemberitahuan NPPN memang belum perlu — jadi kamu aman untuk tahun ini, tidak ada sanksi soal itu.
>
> Tapi karena jatah final habis di akhir 2025, untuk **Tahun Pajak 2026** kamu harus pilih skema baru. Karena kamu cuma punya pencatatan omzet (bukan pembukuan lengkap), NPPN adalah pilihan yang paling cocok dan jauh lebih sederhana dibanding dipaksa pembukuan.
>
> Untuk KLU, kerjaanmu "bikin & maintain software/website buat klien" paling pas masuk:
> - **KLU 62010 – Aktivitas Pemrograman Komputer** → norma penghasilan neto **50%** (berlaku sama di semua wilayah termasuk Bandung, jadi tidak perlu pusing soal kategori kota).
>
> Artinya kalau omzet 2026 misalnya tetap ~380 juta, penghasilan neto yang dihitung = 380 juta × 50% = 190 juta, baru dikurangi PTKP (TK/0 = Rp54.000.000) → PKP ≈ Rp136 juta, kena tarif progresif Pasal 17.
>
> **Yang harus kamu lakukan sebelum akhir Maret 2026:**
> Kirim **Pemberitahuan Penggunaan NPPN** ke DJP (sekarang lewat Coretax DJP) paling lambat 3 bulan sejak awal Tahun Pajak 2026, jadi **deadline akhir Maret 2026**. Kalau tidak dikirim, kamu otomatis dianggap wajib pakai pembukuan penuh — yang jelas merepotkan karena kamu belum pernah bikin pembukuan.
>
> ---
>
> **Ringkasan actionable:**
> 1. SPT Tahunan 2025 (1770, lapor sebelum 31 Maret 2026): laporkan omzet 380 juta sebagai penghasilan final yang dibebaskan, PPh terutang nihil.
> 2. Tanyakan ke AR KPP Bandung / Kring Pajak soal cara menarik kembali/mengompensasi setoran Rp1.900.000 yang sebenarnya tidak terutang.
> 3. Catat tanggal: **sebelum akhir Maret 2026**, kirim Pemberitahuan NPPN (KLU 62010, norma 50%) supaya bisa pakai skema NPPN untuk Tahun Pajak 2026 dan seterusnya.
>
> Mau aku bantu siapin draf permohonan pengembalian kelebihan setor pajak final ke KPP, atau bikin checklist lengkap buat pengisian NPPN 2026?

### Balasan SESUDAH — giliran 2

*tools: ls, read, tool_search, web_fetch, tool_call, exec*

> ## Hitungan SPT Tahunan PPh OP — Tahun Pajak 2025 (status TK/0, domisili Bandung)
>
> **KLU yang paling cocok:** aku cek langsung ke lampiran resmi PER-17/PJ/2015 (bukan nebak) — kerjaan kamu (bikin & maintain software/website untuk klien) paling pas masuk **KLU 62020 "Kegiatan Konsultasi Komputer dan Manajemen Fasilitas Komputer"** (bisa juga 62010 "Pemrograman Komputer" kalau murni coding tanpa konsultasi — persentasenya sama). Bandung termasuk salah satu dari 10 ibukota provinsi di aturan ini, dan untuk KLU ini **persentase normanya 50% di ketiga kelompok wilayah** (10 ibukota provinsi / ibukota provinsi lain / daerah lainnya), jadi domisili kamu tidak mengubah angka.
>
> **1. Penghasilan neto**
> | Sumber | Neto |
> |---|---|
> | Pekerjaan bebas (konsultan IT, NPPN 50%) × Rp380.000.000 | Rp190.000.000 |
> | **Penghasilan neto** | **Rp190.000.000** |
>
> **2. PTKP & PKP**
> - PTKP (TK/0, lajang tanpa tanggungan): Rp54.000.000
> - PKP = Rp190.000.000 − Rp54.000.000 = **Rp136.000.000**
>
> **3. PPh terutang (tarif Pasal 17)**
> - 5% × Rp60.000.000 = Rp3.000.000
> - 15% × Rp76.000.000 = Rp11.400.000
> - **PPh terutang: Rp14.400.000**
>
> **4. Kredit pajak**
> - Rp0 (tidak ada PPh 21/22/23 yang dipotong pihak lain; setoran 0,5% **tidak bisa dikreditkan** di jalur ini karena tidak dipakai)
>
> **5. Hasil: KURANG BAYAR Rp14.400.000** (PPh Pasal 29), ditambah perkiraan angsuran PPh 25 tahun 2026 ≈ **Rp1.200.000/bulan**.
>
> ### Kenapa ini bisa terjadi padahal sudah bayar 0,5% total Rp1.900.000 setahun?
> Karena konsultan IT itu **pekerjaan bebas**, bukan usaha — PPh final 0,5% memang tidak berlaku untuknya. Uang Rp1.900.000 yang sudah kamu setor itu, di sistem pajak yang benar, **tidak bisa mengurangi** tagihan Rp14.400.000 ini (final tidak dikreditkan, dan basisnya memang salah skema sejak awal). Jadi efeknya: ada selisih besar yang harus dilunasi, dan uang yang sudah disetor "nyangkut" di jalur yang salah.
>
> ### ⚠️ Dua hal serius yang perlu kamu tangani — bukan cuma SPT tahunan
>
> 1. **Pemberitahuan NPPN belum pernah dikirim.** Batasnya 31 Maret tahun berjalan. Tanpa itu, secara formal DJP menganggap kamu memilih pembukuan, bukan NPPN — jadi angka Rp14.400.000 di atas **statusnya simulasi**, bukan posisi final yang pasti aman. Kalau benar dianggap pembukuan, DJP bisa minta laporan keuangan riil yang kamu tidak punya (tadi kamu bilang cuma catatan omzet, tidak ada pembukuan).
>
> 2. **Batas lapor SPT Tahunan 2025 adalah 31 Maret 2026 — dan sekarang sudah 1 Oktober 2026.** Tenggat itu, termasuk masa penghapusan sanksi sampai 30 April 2026, **sudah lewat jauh**. Ini bukan lagi soal "nanti kurang bayar berapa", tapi kamu sudah dalam posisi:
>    - Telat lapor → kena denda Rp100.000 (STP)
>    - Kurang bayar Rp14.400.000 yang telat disetor → kena bunga per bulan sejak jatuh tempo (tarifnya berubah tiap bulan, saya tidak hitung di sini)
>    - Setoran 0,5% selama 2025 (Rp1.900.000) kemungkinan perlu **dibetulkan** di SPT Masa — ini bisa berarti pembetulan 12 bulan setoran, dan kemungkinan juga kena sanksi di sana.
>
> Ini kombinasi kasus yang **di luar cakupan saya** (pembetulan SPT Masa, sanksi bunga berjalan, status pembukuan-dianggap). Saya sangat sarankan kamu segera hubungi **Kring Pajak 1500200** atau konsultan pajak terdaftar untuk: (a) memastikan opsi terbaik — lanjut simulasi NPPN atau terpaksa pakai pembukuan, (b) strategi pembetulan setoran 0,5% 2025, (c) hitungan sanksi/bunga yang akurat.
>
> ### Peta ke Coretax (kalau nanti lapor)
> | Angka | Bagian |
> |---|---|
> | Neto NPPN Rp190.000.000 | Lampiran 3 (L-3A) |
> | Neto, PTKP, PKP, PPh terutang | Induk Bagian B & C |
> | KB Rp14.400.000 | Induk Bagian D & E — bikin kode billing, lunasi sebelum kirim SPT |
> | Omzet & PPh final 0,5% Rp1.900.000 | Lampiran 2 / L-3B (tetap dilaporkan, info saja) |
> | PPh 25 2026 | Induk Bagian H |
>
> ### Checklist sebelum lapor
> - [ ] Konfirmasi KLU tepat (62010 vs 62020) — tidak mengubah persen (sama-sama 50%), tapi cocokkan di Coretax
> - [ ] Konsultasi status NPPN vs pembukuan (poin ⚠️ di atas) — **PENTING, lakukan dulu sebelum lapor**
> - [ ] Siapkan dana Rp14.400.000+ untuk kode billing PPh 29 (plus kemungkinan bunga/denda keterlambatan)
> - [ ] Rekap omzet bulanan 2025 + bukti setor PPh final 0,5% (12 bukti NTPN)
> - [ ] Daftar harta & utang per 31 Desember 2025
>
> _Disclaimer: saya bukan konsultan pajak, hanya menghitung simulasi berdasarkan data yang kamu berikan. Pembulatan belum dicocokkan dengan Coretax. Saya tidak mengisi/mengirim SPT. Karena ada keterlambatan lapor dan kemungkinan pembetulan setoran bulanan, sangat disarankan konsultasi Kring Pajak 1500200 atau konsultan pajak terdaftar sebelum bertindak._

### Verifikasi
- **Aturan inti:** penghasilan dari **pekerjaan bebas** (termasuk konsultan) dikecualikan dari PPh final 0,5% (PP 55/2022 Ps. 56; dicatat di `references/regulasi.md` skill). Jasa konsultan/pemrograman yang dikerjakan sendiri berbasis keahlian = pekerjaan bebas → neto dihitung NPPN/pembukuan + tarif Pasal 17.
- Python independen (simulasi NPPN 50%): neto 380.000.000 × 50% = Rp190.000.000; PKP 190 − 54 = Rp136.000.000; PPh = 3.000.000 + 15% × 76.000.000 = **Rp14.400.000**; PPh 25 2026 = 14.400.000/12 = **Rp1.200.000** ✔. Script skill (`--status TK/0 --nppn 380jt 50 --nppn-diberitahukan tidak --hari-ini 2026-10-01`) identik dan memberi peringatan "dianggap pembukuan, NPPN hanya simulasi" + telat lapor.
- Persen norma KLU 62010 (Pemrograman Komputer) = 50% di ketiga kelompok wilayah — dicek penguji lewat sumber sekunder ([Gadjian](https://www.gadjian.com/blog/2021/06/11/cara-menghitung-tarif-pajak-freelance/), merujuk [lampiran PER-17/PJ/2015](https://www.pajak.go.id/sites/default/files/2019-03/PER%20-%2017.PJ_.2015.pdf)) ✔. SESUDAH mengambilnya dari lampiran lewat `web_fetch`, bukan menebak.
- **SEBELUM salah di inti:** tidak mengenali konsultan sebagai pekerjaan bebas; menyimpulkan "omzet < Rp500 jt → seluruhnya bebas, PPh 29 **NIHIL**, Rp1,9 jt bisa diminta kembali". Untuk pekerjaan bebas yang benar adalah kurang bayar ±Rp14,4 jt (simulasi NPPN) atau neto dari pembukuan. Juga menyuruh lapor "1770 ... sebelum 31 Maret 2026" padahal sekarang 1 Oktober 2026 (sudah telat; tidak disebut), dan memberi norma NPPN untuk **2026** dengan batas "akhir Maret 2026" yang juga sudah lewat. Saran ini bisa membuat pengguna salah lapor.
- **SESUDAH:** temuan inti benar sejak giliran 1, hitungan benar, peringatan "dianggap pembukuan" & telat lapor ada, merujuk Kring Pajak/konsultan untuk pembetulan. Cacat kecil: (a) giliran 1 menyebut "klien korporat potong PPh 23 atas jasa" — untuk penerima orang pribadi, potongannya PPh 21 bukan pegawai, bukan PPh 23; (b) peta Coretax menulis setoran 0,5% "tetap dilaporkan di Lampiran 2" padahal di jalur ini setoran itu salah skema dan perlu dibetulkan/diminta kembali — sedikit membingungkan.

### Skor
| Kriteria | SEBELUM | SESUDAH |
|---|---|---|
| Ketepatan aturan & angka | 2 | 9 |
| Penanganan info kurang | 6 | 8 |
| Siap pakai | 4 | 8 |
| Keamanan (risiko salah lapor) | 2 | 9 |
| Kejelasan | 7 | 8 |
| **Skor** | **3** | **8,5** |

Skill terpakai: ya (SKILL.md dibaca; script dijalankan di giliran 2). Kedua sisi memakai `web_fetch`; tidak ada pemasangan paket atau perubahan config.

## Ringkasan

| | SEBELUM | SESUDAH |
|---|---|---|
| Skenario 1 (2 A1, K/2, telat lapor) | 6,5 | 9 |
| Skenario 2 (konsultan pakai 0,5%, tanpa NPPN) | 3 | 8,5 |
| **Rata-rata** | **4,75** | **8,75** |

**VERDIK: LULUS** — sesudah ≥ 8, jauh di atas sebelum, tidak ada kesalahan angka; aturan inti (pekerjaan bebas, NPPN, Coretax, KEP-55) benar. Jujur: untuk kasus karyawan 2 A1, bot tanpa skill juga menghitung angkanya dengan benar — pembedanya di prosedur terbaru (Coretax, bukan 1770 S). Di kasus jebakan, bot tanpa skill **salah fatal** (menyimpulkan nihil/lebih bayar).

**Cacat untuk pembuat (bukti + saran):**
1. **Salah sebut jenis potongan untuk penerima OP.** Bukti: skenario 2 SESUDAH giliran 1 — "klien korporat potong PPh 23 atas jasa". Saran: di tabel Input tambahkan catatan "klien yang membayar jasa orang pribadi memotong PPh 21 bukan pegawai (bukti potong BP21), bukan PPh 23".
2. **Setoran 0,5% yang salah skema.** Bukti: skenario 2 SESUDAH — "Omzet & PPh final 0,5% … Lampiran 2 (tetap dilaporkan, info saja)". Saran: tambahkan di Batasan: "bila pekerjaan bebas terlanjur setor 0,5%, jangan masukkan ke Lampiran 2; jelaskan bahwa setoran itu bisa diajukan pemindahbukuan/pengembalian (konsultasi KPP)".
3. Minor: SKILL.md meminta pengguna mencari persen norma sendiri; agent lalu memakai `web_fetch`. Pertimbangkan tabel kecil norma untuk 10–15 KLU freelancer paling umum (pemrograman, desain, penulis, konsultan) di `references/` agar tidak bergantung internet.

**Cuplikan jualan:**
- "Konsultan/freelancer yang terlanjur bayar 0,5%? Bot biasa bilang 'nihil'. Skill ini mengenali pekerjaan bebas, menghitung simulasi NPPN (kurang bayar Rp14.400.000), dan memperingatkan risiko 'dianggap pembukuan'."
- "Angka SPT dihitung script, langsung dipetakan ke bagian Coretax — bukan formulir 1770 S yang sudah dihapus."

## Uji ulang 2026-10-01 (putaran 2)
**Penguji:** agent penguji independen Komunitech (bukan pembuat; folder skill hanya dibaca, tidak diubah). **Versi diuji:** spt-tahunan-op 1.0.3.
**Cara:** OpenClaw 2026.9.6 lokal (`openclaw agent --local`, tanpa Telegram/gateway), model router Komunitech `claude-sonnet-5`, TZ Asia/Jakarta. Home **terisolasi** per sisi (mount namespace). SEBELUM = home tanpa skill (`r7k-spt-tahunan-op`), SESUDAH = home berisi skill ini saja (`r7-spt-tahunan-op`); kedua sisi dijalankan **ulang** dan dibuat ulang bersih per skenario. Pesan **sama persis** dengan uji pertama (diambil otomatis dari bagian 'Pesan pengguna' di atas); bila uji pertama punya giliran 2, jawaban pengguna yang sama dikirim ke kedua sisi. Angka diverifikasi independen dengan Python dan script skill; fakta aturan dicek sendiri. Folder skill terpasang dibandingkan dengan repo setelah uji: identik.

### Skenario 1 — Pindah kerja, 2 A1, K/2, belum lapor (pesan sama persis)
**SEBELUM (tanpa skill) — giliran 1** — tools: (tidak ada)

> Ya, kurang bayar. Berikut rinciannya:
>
> **1. Penghasilan Neto Setahun**
> - Kantor lama (Jan–Jun): Rp72.000.000
> - Kantor baru (Jul–Des): Rp84.000.000
> - **Total neto: Rp156.000.000**
>
> **2. PTKP (status K/2 — kawin, 2 anak)**
> - WP sendiri: Rp54.000.000
> - Status kawin: Rp4.500.000
> - 2 anak (@Rp4.500.000): Rp9.000.000
> - **Total PTKP: Rp67.500.000**
>
> **3. Penghasilan Kena Pajak (PKP)**
> 156.000.000 − 67.500.000 = **Rp88.500.000**
>
> **4. PPh Terutang Setahun (tarif Pasal 17 UU HPP)**
> - 5% × 60.000.000 = Rp3.000.000
> - 15% × 28.500.000 (sisa) = Rp4.275.000
> - **Total PPh terutang: Rp7.275.000**
>
> **5. PPh 21 yang Sudah Dipotong**
> 1.200.000 + 1.950.000 = **Rp3.150.000**
>
> **6. Kurang Bayar (PPh Pasal 29)**
> 7.275.000 − 3.150.000 = **Rp4.125.000**
>
> Jadi kamu kurang bayar **Rp4.125.000**.
>
> Kenapa kurang? Karena kantor baru biasanya hanya menghitung PPh 21 dari penghasilan di kantor itu saja (disetahunkan dari Juli–Des), tidak menggabungkan dengan penghasilan dari kantor lama — jadi pemotongan totalnya jadi lebih kecil dari yang seharusnya terutang setahun penuh.
>
> **Yang perlu dilakukan sebelum lapor SPT:**
> 1. Buat kode billing di DJP Online untuk setor kekurangan Rp4.125.000 (kode akun 411125, jenis setoran 200 - PPh Pasal 29 OP).
> 2. Bayar lewat e-Billing (ATM/bank/DJP Online).
> 3. Setelah bayar, baru lapor e-Filing SPT 1770 S dengan menggabungkan kedua bukti potong A1.
> 4. Deadline lapor SPT OP: **31 Maret 2026**. Kalau telat lapor, ada denda Rp100.000; kalau telat bayar setelah 31 Maret, kena bunga per bulan dari tanggal jatuh tempo.
>
> Mau aku bantu hitungkan juga detail kode akun/jenis setoran e-Billing-nya, atau bantu susun pengisian 1770 S-nya?
**SESUDAH (dengan skill) — giliran 1** — tools: read, exec

> ## Hitungan SPT Tahunan PPh OP — Tahun Pajak 2025 (status K/2)
>
> **1. Penghasilan neto**
> | Sumber | Neto |
> |---|---|
> | Kantor lama (Jan–Jun, A1) | Rp72.000.000 |
> | Kantor baru (Jul–Des, A1) | Rp84.000.000 |
> | **Total neto** | **Rp156.000.000** |
>
> **2. PTKP & PKP**
> - PTKP K/2 = 54jt + 4,5jt (kawin) + 2×4,5jt (anak) = **Rp67.500.000**
> - PKP = 156.000.000 − 67.500.000 = **Rp88.500.000**
>
> **3. PPh terutang (tarif Pasal 17)**
> - 5% × 60jt = Rp3.000.000
> - 15% × 28,5jt = Rp4.275.000
> - **Total PPh terutang: Rp7.275.000**
>
> **4. Kredit pajak (PPh 21 yang sudah dipotong)**
> - Kantor lama: Rp1.200.000
> - Kantor baru: Rp1.950.000
> - **Total kredit: Rp3.150.000**
>
> **5. Hasil: KURANG BAYAR**
> Rp7.275.000 − Rp3.150.000 = **Rp4.125.000 harus disetor (PPh Pasal 29)** sebelum lapor.
>
> **Kenapa kurang bayar padahal sudah dipotong dua kali?** Masing-masing kantor menghitung PPh 21 bulanan pakai PTKP penuh dan tarif rendah seolah itu satu-satunya penghasilanmu setahun. Begitu dua penghasilan digabung di SPT tahunan, sebagian penghasilan naik ke lapisan tarif 15%, jadi ada selisih pajak yang belum terpotong di manapun. Ini normal untuk orang yang pindah kerja di tengah tahun, bukan tanda ada kesalahan.
>
> ⚠️ **Status batas waktu:** Batas lapor normal 31 Maret 2026, dan masa penghapusan sanksi (KEP-55/PJ/2026) berakhir 30 April 2026. Karena hari ini sudah 1 Oktober 2026, **kedua batas itu sudah lewat**. Konsekuensinya kalau belum lapor sama sekali:
> - Denda telat lapor SPT Tahunan OP: **Rp100.000** (ditagih lewat STP, bukan dibayar sendiri di muka)
> - Kurang bayar Rp4.125.000 kena **bunga keterlambatan per bulan** sejak 1 April 2026 (tarif bulanan KMK, tidak dihitung di sini — biasanya di kisaran 0,5–2%/bulan tergantung periode, cek tarif terbaru saat bayar)
> - Semakin cepat lapor & bayar, makin kecil akumulasi bunganya — jangan ditunda lagi.
>
> **Peta ke Coretax**
> - 2 bukti potong A1 → Lampiran 1 (biasanya sudah terisi otomatis dari sistem DJP)
> - Neto, PTKP, PKP, PPh terutang → Induk Bagian B & C
> - Kredit pajak & kurang bayar → Induk Bagian D & E
>
> **Langkah berikutnya**
> 1. Login Coretax, cek kedua bukti potong A1 sudah muncul dengan angka yang sama persis seperti di atas.
> 2. Pastikan status PTKP di sistem = K/2 (kawin, 2 tanggungan) sesuai keadaan 1 Januari 2025.
> 3. Buat kode billing untuk PPh Pasal 29 Rp4.125.000 **+ bunga keterlambatan** (sistem Coretax/DJP biasanya menghitung otomatis saat bikin billing terlambat; kalau tidak muncul otomatis, tanya KPP/Kring Pajak).
> 4. Bayar, baru kirim SPT. Siapkan juga daftar harta & utang per 31 Desember 2025, serta data tanggungan (NIK 2 anak).
>
> **Checklist dokumen**: akun Coretax aktif, 2 lembar bukti potong A1, daftar harta & utang 31 Des, data keluarga/tanggungan, saldo untuk bayar Rp4.125.000 + bunga.
>
> _Ini alat bantu hitung, bukan konsultan pajak. Bunga keterlambatan belum dihitung nominalnya — cocokkan dengan kode billing Coretax atau tanya Kring Pajak 1500200 / konsultan pajak terdaftar sebelum bayar & lapor._

### Skenario 2 — Konsultan IT pakai 0,5%, tanpa NPPN (pesan sama persis)
**SEBELUM (tanpa skill) — giliran 1** — tools: tool_search, web_fetch, tool_call

> Saya coba cross-check ke situs resmi DJP & beberapa sumber pajak tadi, tapi semua akses web gagal (network/sandbox limitation). Jawaban di bawah saya susun dari pengetahuan yang sudah solid soal PP 23/2018 jo. PP 55/2022 (PPh Final UMKM) dan UU HPP — tapi ada 1 hal yang perlu kamu konfirmasi sendiri ke saya biar hitungannya pasti (lihat poin 1).
>
> **1. Cek dulu: kamu mungkin malah overpay PPh Final bulanan**
> Sejak PP 55/2022, untuk WP **orang pribadi**, omzet sampai dengan **Rp500 juta dalam 1 tahun pajak TIDAK dikenai PPh Final 0,5% sama sekali** — bukan dipotong dari tarif, tapi memang dibebaskan. Omzet kamu setahun Rp380 juta, masih di bawah Rp500 juta.
>
> Kalau selama ini kamu setor 0,5% × omzet **tiap bulan tanpa menghitung akumulasi dari Rp0**, kemungkinan besar seharusnya **nihil** sepanjang 2025 (karena kumulatif belum pernah tembus Rp500 juta). Kalau itu yang terjadi, setoran yang sudah kamu bayar itu lebih bayar — bisa diajukan kompensasi/pindah buku atau restitusi lewat SPT Tahunan.
>
> Pertanyaan balik: pas hitung setoran bulanan, apa kamu pakai sistem kumulatif (cek akumulasi omzet Jan–bulan berjalan, baru kena 0,5% kalau sudah lewat 500jt), atau langsung 0,5% dari omzet bulan itu tanpa cek threshold? Ini penting biar saya bisa pastikan status lebih/kurang bayarnya.
>
> **2. Jangka waktu pakai tarif final 0,5% ada batasnya: 7 tahun pajak (untuk OP)**
> Dihitung sejak tahun terdaftar jadi WP (kalau terdaftar sebelum 2018, dihitung sejak 2018). Kalau tahun 2025 ini kamu sudah lewat 7 tahun pakai skema final, harusnya kamu sudah pindah ke skema normal (Pasal 17 progresif) sejak awal 2025, bukan 0,5% lagi.
> → Kapan kamu pertama kali NPWP terdaftar/mulai usaha konsultan IT ini? Supaya saya bisa pastikan 2025 masih dalam jatah 7 tahun atau tidak.
>
> **3. Soal pemberitahuan NPPN — ini sebenarnya beda skema, kemungkinan besar tidak relevan buat kamu**
> Pemberitahuan penggunaan Norma Penghitungan Penghasilan Neto (NPPN) itu wajib buat WP OP yang **tidak** pakai PPh Final 0,5%, tapi memilih skema normal (tarif Pasal 17) dengan dasar penghasilan neto dihitung pakai persentase norma sesuai KLU (karena malas/tidak mau pembukuan). Itu disampaikan di 3 bulan pertama tahun pajak.
>
> Karena kamu selama ini pakai PPh Final 0,5% (PP 23/2018), pemberitahuan NPPN **tidak dibutuhkan** — jadi tidak kirim itu bukan masalah, selama kamu memang masih berhak pakai skema final (lihat poin 2). Kalau ternyata jatah 7 tahunmu sudah habis dan seharusnya pakai skema normal tahun ini, barulah NPPN jadi relevan — dan karena belum pernah kirim pemberitahuan, defaultnya DJP anggap kamu wajib pembukuan (bukan norma), yang administrasinya lebih ribet buat freelancer solo kayak kamu.
>
> **4. Soal SPT Tahunan — apa saja yang harus disetor/dilaporkan**
> Karena PPh Final sifatnya final (tidak digabung dan tidak dihitung ulang pakai tarif progresif di SPT Tahunan), **selama skema final masih berlaku untukmu**, normalnya di SPT Tahunan 1770 kamu:
> - Tidak ada PPh terutang tambahan dari omzet usaha (sudah final lewat setoran bulanan 0,5%, kalau memang terutang).
> - Tetap wajib lapor peredaran bruto per bulan + PPh Final yang disetor (ada formulir Lampiran khusus PPh Final UMKM pada 1770).
> - Wajib lapor daftar harta dan utang per 31 Desember 2025.
> - Kalau ada penghasilan lain di luar usaha (bunga tabungan/deposito, dividen, hadiah, dll) itu dilaporkan sesuai aturan masing-masing (bunga bank biasanya sudah final dipotong bank, tinggal lapor saja, tidak nambah pajak lagi).
> - Status lajang tanpa tanggungan (PTKP TK/0) tidak relevan di skema final karena final itu dari omzet bruto, bukan penghasilan neto dikurangi PTKP — PTKP baru dipakai kalau kamu pakai skema normal Pasal 17.
>
> **Jadi, singkatnya:** kemungkinan besar kamu **tidak** ada tambahan setoran PPh di SPT Tahunan — justru berpotensi lebih bayar kalau threshold Rp500 juta belum pernah kamu terapkan di setoran bulanan. Tapi saya perlu 2 info dari kamu (cara hitung setoran bulanan, dan tahun pertama NPWP/mulai usaha) biar saya bisa kasih kesimpulan pasti, bukan "kemungkinan besar".
>
> Mau saya bantu hitung ulang berdasarkan rincian omzet bulananmu kalau kamu kirim angkanya?
**SESUDAH (dengan skill) — giliran 1** — tools: read

> Sebelum saya hitung angka pastinya, ada temuan penting dulu:
>
> **Konsultan IT termasuk "pekerjaan bebas" (profesi/keahlian), bukan "usaha" biasa.** Menurut PP 55/2022 Pasal 56 (s.t.d.d. PP 20/2026), pekerjaan bebas **tidak boleh** pakai skema PPh final UMKM 0,5% — wajib dihitung pakai NPPN (Norma Penghitungan Penghasilan Neto) atau pembukuan, lalu kena tarif progresif Pasal 17. Jadi setoran 0,5% yang kamu bayar tiap bulan sepanjang 2025 itu **salah skema**, bukan "sudah lunas" seperti UMKM dagang/jasa biasa. Konsekuensinya nanti ada dua bagian: (1) hitung ulang pajak terutang setahun pakai NPPN, (2) uang 0,5% yang sudah disetor tidak bisa dikreditkan — perlu diajukan "pengembalian pajak yang seharusnya tidak terutang" lewat Coretax.
>
> Dan soal pemberitahuan NPPN yang belum pernah dikirim — hasil hitungannya nanti tetap bisa saya tunjukkan, tapi berstatus **simulasi** karena DJP bisa menganggap kamu "dianggap memilih pembukuan" kalau tidak memberitahukan NPPN (ini perlu dicek ulang ke AR/KPP, bukan hal yang bisa saya pastikan sendiri).
>
> Supaya hitungannya akurat, tolong jawab ini (nomor 1 & 2 paling penting):
>
> 1. **Persentase norma (NPPN)** untuk jasa konsultan IT kamu — ini tergantung KLU (kode usaha) & kota domisili usaha di Lampiran PER-17/PJ/2015. Kalau belum tahu kodenya, sebutkan kota + jenis jasa spesifik (mis. konsultan sistem informasi, pengembangan software, IT support), saya bantu cari kodenya — tapi persennya sendiri tidak saya tebak.
> 2. **Total nominal PPh final 0,5% yang sudah kamu setor sepanjang 2025** (total rupiah yang sudah dibayar, bukan omzetnya).
> 3. Ada klien korporasi yang memotong **PPh 21 bukan pegawai** (bukti potong BP21) atas fee jasa kamu selama 2025? Kalau ada, berapa total potongannya?
> 4. Ada zakat yang kamu bayar sendiri ke BAZNAS/LAZ resmi (di luar potongan otomatis)? Kalau tidak ada, saya anggap 0.
>
> Kalau mau cepat: cukup jawab #1 dan #2, sisanya saya anggap 0.
**Giliran 2 — jawaban pengguna (sama di kedua sisi):** "NPWP aku dari 2019. Aku setor 0,5% dari omzet tiap bulan mulai Januari, total setahun Rp1.900.000. Domisili Bandung. Kerjaanku bikin & maintain software/website buat klien, murni jasa konsultan IT, ga ada dagang. Ga ada pembukuan, cuma catatan omzet. Ga ada zakat, klien ga pernah motong pajak. KLU aku ga tau, tolong bantu aja"
**SEBELUM — giliran 2** — tools: (tidak ada)

> Oke, ini ngebantu banget buat mastiin posisimu. Saya coba re-cek sumber resmi DJP barusan tapi akses web lagi error semua di sisi saya (network gagal total, bukan nemu "tidak ada"), jadi perhitungan di bawah saya susun dari ketentuan PP 23/2018 jo. PP 55/2022 yang saya pegang — dan saya kasih tanda bagian mana yang sebaiknya kamu cross-check lagi ke AR KPP Bandung atau konsultan pajak resmi sebelum submit, karena ini menyangkut uang dan ada tenggat.
>
> **1. Temuan paling penting: 2025 adalah TAHUN TERAKHIR kamu boleh pakai final 0,5%**
> Jatah pakai skema PPh Final 0,5% buat WP Orang Pribadi itu **7 tahun pajak**, dihitung sejak tahun NPWP terdaftar. NPWP kamu 2019 → 2019, 2020, 2021, 2022, 2023, 2024, **2025** = tahun ke-7. Jadi:
> - SPT Tahunan 2025 (yang mau kamu laporkan sekarang): masih sah pakai final 0,5%, aman.
> - **Mulai tahun pajak 2026, kamu WAJIB pindah ke skema normal (tarif Pasal 17/progresif)**, final 0,5% udah gak boleh dipakai lagi.
> - Karena kamu gak ada pembukuan (cuma catatan omzet), kamu **harus kirim Pemberitahuan Penggunaan Norma Penghitungan Penghasilan Neto (NPPN) ke KPP paling lambat akhir Maret 2026** (3 bulan pertama tahun pajak 2026). Kalau gak dikirim, DJP anggap kamu wajib pembukuan penuh — padahal kamu gak punya, ini yang bisa bikin runyam nanti.
>
> Jadi pertanyaan "aku gak pernah kirim NPPN" itu **belum jadi masalah untuk SPT 2025 ini**, tapi jadi **urgent untuk awal 2026**. Saya catat ini, nanti saya ingetin lagi mendekati Januari-Maret 2026 kalau kamu mau.
>
> **2. Soal setoran bulananmu: kemungkinan besar lebih bayar PENUH**
> Batas Rp500 juta/tahun pajak itu dihitung **kumulatif dari Rp0 di bulan Januari**, bukan per bulan. Karena total omzet kamu setahun cuma Rp380 juta (gak pernah tembus Rp500 juta kumulatif), **seharusnya PPh Final terutang kamu sepanjang 2025 = Rp0**. Tapi kamu udah setor Rp1.900.000 total (persis 0,5% × 380jt tanpa pengurangan threshold).
>
> → Artinya kamu **lebih bayar Rp1.900.000 penuh**. Ini dilaporkan di SPT Tahunan 1770 pada lampiran PPh Final: isi peredaran bruto Rp380.000.000, PPh terutang Rp0, PPh yang sudah disetor Rp1.900.000 → otomatis status jadi Lebih Bayar. Dari situ kamu bisa ajukan pengembalian (restitusi) atau minta dikompensasikan.
>
> ⚠️ Bagian ini saya gak bisa re-verifikasi live barusan karena akses internet saya gagal total — mekanisme/batas nominal restitusi dipercepat untuk OP bisa saja ada ketentuan teknis terbaru yang saya belum cek. Saran saya: saat lapor SPT via Coretax DJP atau e-Filing, submit apa adanya (Rp0 terutang, lebih bayar Rp1,9jt), lalu ikuti instruksi sistem soal pengembalian, atau konfirmasi dulu ke AR KPP domisili Bandung — nilainya kecil jadi harusnya prosesnya gak ribet.
>
> **3. KLU (Klasifikasi Lapangan Usaha)**
> Dari deskripsimu "bikin & maintain software/website buat klien", yang paling cocok:
> - **62010 – Aktivitas Pemrograman Komputer** (develop, build, test, maintain software/website) → ini kandidat utama.
> - Alternatif: **62020 – Aktivitas Konsultasi Komputer**, kalau porsi kerjamu lebih ke advisory/arsitektur tanpa ngoding langsung.
>
> Cek juga KLU yang sudah tercatat di profil NPWP kamu di Coretax DJP (menu profil WP) — kalau beda, sebaiknya disamakan dengan yang kamu pakai di SPT. Kalau pas registrasi dulu kamu gak pernah isi KLU spesifik, pakai 62010 aman untuk kerjaanmu.
>
> **4. Klien gak pernah potong pajak — gak masalah besar, tapi ada 1 opsi beresin**
> Karena kamu pakai skema final 0,5% sendiri, secara teori klien badan usaha "harusnya" potong PPh 23 kecuali kamu kasih **Surat Keterangan PP 23 (bebas potong)** dari KPP. Fakta klien gak pernah motong bukan pelanggaran di pihakmu — itu lebih ke risiko administrasi di sisi klien. Gak perlu diurus mendesak, tapi kalau mau rapi (misal klien korporat mulai nanya-nanya), kamu bisa minta Surat Keterangan itu ke KPP, gratis dan sekali proses, biar urusan potong-memotong jelas ke depannya.
>
> **5. Zakat & status lajang tanpa tanggungan**
> Keduanya gak relevan selama pakai skema final 0,5% — final dihitung dari omzet bruto, bukan penghasilan neto dikurangi PTKP atau zakat. Baru relevan kalau sudah pindah ke skema normal Pasal 17 (mulai 2026).
>
> **6. Jangan lupa**
> SPT Tahunan tetap wajib lampirkan **daftar harta dan utang per 31 Desember 2025**, walaupun pajaknya final.
>
> ---
>
> **Ringkasan aksi:**
> 1. Lapor SPT 1770 tahun 2025 dengan PPh Final terutang Rp0, setoran Rp1.900.000 → lebih bayar, ajukan pengembalian/kompensasi.
> 2. Pakai KLU 62010 (cek dulu kecocokan di profil NPWP).
> 3. Catat tenggat: Maret 2026 kirim pemberitahuan NPPN ke KPP, karena mulai tahun pajak 2026 kamu wajib pindah skema normal.
>
> Kalau mau, saya bisa bantu susun draf perhitungan buat diisi di formulir SPT-nya langsung, atau bikin pengingat otomatis buat tenggat NPPN Maret 2026 ini biar gak kelewat?
**SESUDAH — giliran 2** — tools: ls, read, tool_search, web_fetch, tool_call, exec

> Sudah saya hitung pakai script resmi skill ini. Catatan dulu soal KLU: pekerjaan "bikin & maintain software/website" cocok dengan KLU **62010 – Kegiatan Pemrograman Komputer** (norma 1151 di lampiran PER-17/PJ/2015). Persentase normanya **50%** — dan uniknya untuk KLU ini persentasenya sama rata di tiga kelompok wilayah (10 ibu kota provinsi termasuk Bandung / ibu kota provinsi lain / daerah lain), jadi domisili Bandung tidak mengubah angka. Saya ambil ini dari artikel yang mengutip langsung lampiran PER-17/PJ/2015 (bukan saya tebak), tapi tetap **sarankan kamu cek ulang kode KLU persisnya di Coretax atau tanya KPP** sebelum lapor, karena saya tidak bisa membuka file lampiran PDF resminya langsung hari ini.
>
> ## Hitungan SPT Tahunan PPh OP — Tahun Pajak 2025 (status TK/0, lajang tanpa tanggungan)
>
> **1. Penghasilan neto**
> | Sumber | Neto |
> |---|---|
> | Jasa konsultan IT (NPPN 50% × Rp380.000.000) | Rp190.000.000 |
> | **Penghasilan neto** | **Rp190.000.000** |
>
> **2. PTKP & PKP**
> - PTKP TK/0: Rp54.000.000
> - PKP = Rp190.000.000 − Rp54.000.000 = **Rp136.000.000**
>
> **3. PPh terutang (tarif Pasal 17)**
> - 5% × Rp60.000.000 = Rp3.000.000
> - 15% × Rp76.000.000 = Rp11.400.000
> - **PPh terutang: Rp14.400.000**
>
> **4. Kredit pajak**
> - Rp0 — karena kliennya tidak pernah memotong apa pun (tidak ada bukti potong BP21) dan setoran 0,5% tidak bisa dikreditkan.
>
> **5. Hasil: KURANG BAYAR Rp14.400.000**
> Plus perkiraan angsuran PPh 25 tahun 2026: **Rp1.200.000/bulan**.
>
> ## ⚠️ Tiga hal penting
>
> **1. Setoran 0,5% Rp1.900.000 itu salah skema, bukan "sudah lunas".** Karena kerjaanmu pekerjaan bebas (bukan usaha dagang/jasa biasa), uang itu tidak masuk hitungan di atas dan tidak boleh dilaporkan di Lampiran 2 (penghasilan final). Kamu bisa minta kembali lewat permohonan **pengembalian pajak yang seharusnya tidak terutang** di Coretax (menu Pembayaran → formulir restitusi) — tapi pemindahbukuan biasanya tidak bisa. Konfirmasikan dulu prosedurnya ke KPP/Kring Pajak 1500200 sebelum mengajukan (perlu review konsultan pajak, aturan ini masih agak abu-abu).
>
> **2. Karena belum pernah kirim pemberitahuan NPPN, hitungan di atas statusnya simulasi.** Menurut DJP, WP yang tidak memberitahukan NPPN dalam 3 bulan pertama tahun pajak dianggap memilih pembukuan penuh — artinya neto seharusnya dihitung dari pembukuan asli (bukan 50% dari omzet), bukan dari NPPN. Kamu bilang cuma punya catatan omzet, bukan pembukuan lengkap (neraca, laba-rugi). Ini titik paling berisiko — **sangat disarankan konsultasi ke KPP atau konsultan pajak sebelum lapor**, karena bisa mengubah angka kurang bayarnya.
>
> **3. Batas lapor SPT Tahunan 2025 adalah 31 Maret 2026 — dan itu sudah lewat per hari ini (1 Oktober 2026).** Masa penghapusan sanksi (KEP-55/PJ/2026, berlaku sampai 30 April 2026) juga sudah berakhir. Konsekuensinya: denda telat lapor Rp100.000 (ditagih lewat STP) + bunga keterlambatan bayar per bulan atas kurang bayar Rp14.400.000 (tarif bulanan berubah-ubah, tidak saya hitung di sini). **Segera lapor secepatnya untuk menghentikan akumulasi bunga.**
>
> ## Peta ke Coretax
> | Angka | Bagian SPT |
> |---|---|
> | Neto NPPN Rp190.000.000 | Lampiran 3 (L-3A) |
> | PTKP, PKP, PPh terutang | Induk Bagian B & C |
> | Kurang bayar Rp14.400.000 | Induk Bagian D & E |
> | PPh 25 tahun depan | Induk Bagian H |
> | Setoran 0,5% salah skema | TIDAK masuk Lampiran 2 — urus terpisah lewat restitusi |
>
> ## Langkah berikutnya
> 1. Konsultasikan status NPPN (belum diberitahukan) dan validitas pencatatan omzet kamu ke KPP/konsultan pajak — ini menentukan apakah angka Rp14.400.000 di atas valid atau harus dihitung ulang dari pembukuan.
> 2. Cocokkan kode KLU 62010 persis di Coretax saat mengisi SPT (bisa beda penamaan).
> 3. Siapkan dana Rp14.400.000+ untuk kode billing PPh Pasal 29, lalu lapor SPT secepatnya (sudah lewat tenggat).
> 4. Setelah SPT tahun ini beres, pertimbangkan ajukan pemberitahuan NPPN tahun 2026 di Coretax sebelum 31 Maret 2026 supaya tahun depan tidak bermasalah lagi, dan hentikan setoran 0,5% karena memang tidak berlaku untuk pekerjaan bebas kamu.
>
> **Checklist dokumen**
> - [ ] Akun Coretax aktif + kode otorisasi
> - [ ] Rekap omzet bulanan 2025 (pencatatan)
> - [ ] Bukti setor (NTPN) PPh final 0,5% × 12 bulan (Rp1.900.000) — untuk proses restitusi
> - [ ] Daftar harta & utang per 31 Desember 2025
> - [ ] Saldo untuk kode billing PPh Pasal 29 (≥Rp14.400.000 + bunga keterlambatan)
>
> _Disclaimer: Ini alat bantu hitung, bukan nasihat pajak resmi. Persentase norma NPPN sudah saya cocokkan dengan KLU yang paling sesuai tapi belum saya verifikasi langsung dari file lampiran PDF resmi — minta dicek ulang di Coretax/KPP. Status pemberitahuan NPPN yang belum dikirim dan setoran 0,5% salah skema adalah dua isu yang perlu review konsultan pajak sebelum kamu lapor. Saya tidak mengisi atau mengirim SPT ke DJP._

### Verifikasi (Python independen + script skill + aturan)
- **S1:** neto 72 jt + 84 jt = Rp156.000.000; PTKP K/2 = 54 + 4,5 + 2 × 4,5 = Rp67.500.000; PKP Rp88.500.000; PPh = 3.000.000 + 15% × 28.500.000 = **Rp7.275.000**; kredit 3.150.000 → **kurang bayar Rp4.125.000** ✔ (kedua sisi). SEBELUM menyuruh "e-Filing SPT **1770 S**" dan e-Billing DJP Online — untuk TP 2025 SPT OP lewat Coretax dengan bentuk SPT tunggal (PER-11/PJ/2025) → salah prosedur (cacat SEBELUM yang sama dengan uji pertama). SESUDAH: angka dari script (`exec` tercatat), batas 31 Maret 2026 & KEP-55 (s.d. 30 April 2026) sudah lewat ✔, denda Rp100.000 via STP ✔ (UU KUP Ps. 7). Kecil: kisaran bunga "0,5–2%/bulan" terlalu lebar (tarif KMK bulanan = (suku bunga acuan + 5%)/12, beberapa tahun terakhir < 1%/bulan) tetapi diberi label "cek tarif terbaru".
- **S2:** NPPN 50% × 380 jt = Rp190.000.000; PKP 136.000.000; PPh = 3.000.000 + 15% × 76.000.000 = **Rp14.400.000**; PPh 25 2026 = Rp1.200.000/bulan ✔. Script penguji (`--status TK/0 --nppn 380jt 50 --nppn-diberitahukan tidak --final-salah-skema 1.900.000 --hari-ini 2026-10-01`) **identik**. Norma KLU 62010 = 50% di tiga wilayah ✔ (sudah dicek uji pertama).
- **Fakta aturan baru (dicek penguji):** jasa ke orang pribadi dipotong **PPh 21 bukan pegawai (BP21)** — PMK 168/2023 ✔; setoran PPh final UMKM tidak bisa dipindahbukukan karena dianggap penyampaian SPT Masa — **PMK 81/2024 Pasal 109 ayat (3)**, jalurnya permohonan pengembalian pajak yang seharusnya tidak terutang (Ps. 123–125) ✔ ([Kring Pajak](https://x.com/kring_pajak/status/1901440860799316418?lang=id), [DDTC](https://news.ddtc.co.id/berita/nasional/1819567/mau-bayar-pph-25-tapi-salah-kode-billing-bisakah-pemindahbukuan)). SESUDAH menyebut keduanya dengan benar.
- **Kesalahan baru SESUDAH S2:** Langkah 4 — "pertimbangkan ajukan pemberitahuan NPPN **tahun 2026** di Coretax **sebelum 31 Maret 2026**". Hari uji 1 Oktober 2026 → tenggat itu **sudah lewat**; untuk TP 2026 pengguna kini dianggap wajib pembukuan (perlu mulai mencatat), dan pemberitahuan NPPN berikutnya adalah untuk TP 2027 paling lambat 31 Maret 2027. Saran tanggal yang sudah lewat ini menyesatkan. Minor: peta PPh 25 ditulis "Induk Bagian H" padahal keluaran script menyebut Lampiran 4.
- **SEBELUM S2 (fatal):** menyatakan omzet ≤ Rp500 juta "tidak dikenai PPh final sama sekali" sehingga 0,5% yang disetor = **lebih bayar Rp1.900.000** dan SPT 2025 "aman" pakai final; tidak mengenali pekerjaan bebas (PP 55/2022 Ps. 56); menyebut "harusnya potong PPh 23" (salah untuk penerima OP); formulir 1770; tenggat NPPN "akhir Maret 2026" (juga sudah lewat). Kurang bayar riil (simulasi NPPN) Rp14.400.000 terlewat sepenuhnya.

### Status cacat lama
1. "Klien potong PPh 23" → **TERATASI** (pertanyaan #3 SESUDAH: "PPh 21 bukan pegawai (bukti potong BP21)").
2. Setoran 0,5% salah skema di Lampiran 2 → **TERATASI** ("tidak boleh dilaporkan di Lampiran 2", pengembalian pajak yang seharusnya tidak terutang, "pemindahbukuan biasanya tidak bisa").
3. Ketergantungan internet untuk norma → **tetap** (agent masih `web_fetch` untuk KLU 62010; jujur menyebut belum membuka PDF lampiran resmi).

**Regresi/temuan baru:** tenggat NPPN TP 2026 yang sudah lewat disarankan sebagai langkah (lihat di atas).

### Skor
| Skenario | SEBELUM | SESUDAH | Alasan |
|---|---:|---:|---|
| 1. 2 A1, K/2, telat lapor | 6 | 9 | Angka sama-sama benar; SESUDAH prosedur Coretax, status tenggat & KEP-55, penjelasan kenapa kurang bayar. SEBELUM formulir 1770 S/e-Filing yang sudah tidak dipakai. |
| 2. Konsultan pakai 0,5%, tanpa NPPN | 1,5 | 8 | SESUDAH aturan inti benar, angka identik script, kedua cacat lama teratasi; minus saran NPPN 2026 "sebelum 31 Maret 2026" (sudah lewat). SEBELUM menyimpulkan lebih bayar — salah fatal. |
| **Rata-rata** | **3,75** | **8,5** | |

**VERDIK: BELUM** — sesudah ≥ 8 dan jauh di atas sebelum, semua angka benar, dua cacat fakta lama teratasi, **tetapi** ada satu kesalahan fakta tanggal baru (tenggat NPPN TP 2026 yang sudah lewat disarankan sebagai langkah). Perbaikan kecil.

**Saran untuk pembuat:** script (`--hari-ini`) sebaiknya mencetak status NPPN tahun berjalan: "TP {tahun hari-ini}: batas pemberitahuan 31 Maret {tahun} → SUDAH LEWAT/BELUM"; bila lewat, tulis "TP {tahun} dianggap pembukuan — mulai catat pembukuan sekarang; pemberitahuan NPPN berikutnya untuk TP {tahun+1} paling lambat 31 Maret {tahun+1}". Di SKILL.md larang menyebut tenggat tanpa membandingkan dengan tanggal hari ini. Samakan peta PPh 25 (Lampiran 4 vs Induk H) di referensi.

**Cuplikan jualan (jujur, aman dipakai):** "Konsultan IT terlanjur bayar 0,5%? AI biasa bilang 'malah lebih bayar Rp1,9 juta'. Skill ini mengenali pekerjaan bebas, menghitung simulasi NPPN (kurang bayar Rp14.400.000), dan menjelaskan setoran 0,5% diminta kembali lewat pengembalian pajak — bukan Lampiran 2." · "Pindah kerja, 2 bukti potong A1: kurang bayar Rp4.125.000 dihitung script dan dipetakan ke Coretax, bukan formulir 1770 S yang sudah tidak dipakai."

## Uji ulang 2026-10-01 (putaran 3)
**Penguji:** agent penguji independen Komunitech (bukan pembuat; folder skill hanya dibaca, tidak diubah). **Versi diuji:** spt-tahunan-op 1.0.4.
**Cara:** OpenClaw 2026.9.6 lokal (`openclaw agent --local`, tanpa Telegram/gateway), model router Komunitech `claude-sonnet-5`, TZ Asia/Jakarta, home terisolasi (mount namespace) berisi skill ini saja, dibuat ulang bersih sebelum tiap sesi (`r12-spt-tahunan-op`). Skenario yang gagal di putaran 2 (S2, saran tenggat NPPN TP 2026 yang sudah lewat) diulang dengan **pesan sama persis** (giliran 1 + jawaban giliran 2 yang sama) di **2 sesi berbeda** (A, B), ditambah 1 varian baru yang langsung menanyakan pendaftaran NPPN 2026. Sisi SEBELUM tidak diulang (acuan: putaran 2, skor 1,5).

### Skenario 2 — Konsultan IT pakai 0,5%, tanpa NPPN (pesan sama persis) — Sesi A
**Giliran 1** — tools: read

> Sebelum saya hitung, ada dua hal penting dulu soal status pajak kamu:
>
> **Konsultan IT = "pekerjaan bebas" (profesi/keahlian), bukan "usaha"** — menurut aturan PP 55/2022 Ps. 56, pekerjaan bebas (termasuk konsultan) **tidak boleh** pakai tarif final 0,5%. Yang benar: hitung penghasilan neto pakai **NPPN (Norma Penghitungan Penghasilan Neto)** atau pembukuan, lalu kena tarif Pasal 17 (progresif). Jadi setoran 0,5% yang kamu bayar tiap bulan selama ini **salah skema**.
>
> **Karena kamu tidak pernah kirim pemberitahuan NPPN**, dan batas waktunya untuk tahun pajak 2025 adalah **31 Maret 2025** (sudah lewat jauh, sekarang Oktober 2026) — untuk tahun pajak 2025, kamu **dianggap memilih pembukuan** (UU PPh Ps. 14 ayat (5)), bukan NPPN. Saya tetap bisa hitung simulasi pakai NPPN supaya kamu tahu kira-kira besarannya, tapi saya tandai jelas bahwa itu cuma simulasi — status resminya perlu dikonfirmasi ke KPP/konsultan pajak.
>
> Supaya saya bisa hitung, tolong jawab ini (boleh langsung jawab semua):
>
> 1. **Total setoran PPh final 0,5%** yang sudah kamu bayar sepanjang 2025 (total semua bulan — kalau flat 0,5% × 380jt tanpa potongan, berarti ~Rp1.900.000, tapi pastikan angka pastinya).
> 2. **Persentase NPPN** untuk jasa konsultan IT kamu — ini tergantung **KLU usaha + kota domisili**, harus dicek di lampiran PER-17/PJ/2015, saya tidak boleh menebak. Kamu tahu KLU-nya atau kotamu di mana supaya saya bantu cari?
> 3. Ada klien (PT/badan) yang **memotong PPh 21 bukan pegawai** (bukti potong BP21) saat bayar fee kamu? Kalau ada, berapa totalnya tahun 2025?
> 4. Ada **zakat** yang kamu bayar sendiri ke BAZNAS/LAZ resmi (bukan dipotong perusahaan)? Kalau tidak, saya anggap 0.
> 5. Konfirmasi status PTKP: lajang, tanpa tanggungan → **TK/0**, betul?
>
> Kalau mau cepat: cukup kasih angka #1 dan #2, sisanya saya anggap 0.

**Giliran 2** (jawaban pengguna sama: "NPWP aku dari 2019. Aku setor 0,5% … KLU aku ga tau, tolong bantu aja") — tools: ls, read, tool_search, web_fetch, tool_call, exec

> Sudah saya cek ke sumber resminya — KLU 62010/62020/62090 (pemrograman, konsultasi komputer, jasa TI lainnya) untuk 10 kota besar termasuk **Bandung** semuanya pakai **norma 50%**. Berikut hasil hitungannya.
>
> ## Hitungan SPT Tahunan PPh OP — Tahun Pajak 2025 (status TK/0)
>
> **1. Penghasilan neto**
> | Sumber | Bruto | Norma | Neto |
> |---|---|---|---|
> | Jasa konsultan IT (NPPN, KLU 62010/62020) | Rp380.000.000 | 50% | Rp190.000.000 |
>
> **2. PTKP & PKP**
> - PTKP (TK/0): Rp54.000.000
> - PKP: Rp190.000.000 − Rp54.000.000 = **Rp136.000.000**
>
> **3. PPh terutang (tarif Pasal 17)**
> - 5% × Rp60.000.000 = Rp3.000.000
> - 15% × Rp76.000.000 = Rp11.400.000
> - **Total PPh terutang: Rp14.400.000**
>
> **4. Kredit pajak:** Rp0 (tidak ada klien yang motong PPh 21)
>
> **5. Hasil: KURANG BAYAR Rp14.400.000**
> - Perkiraan angsuran PPh 25 tahun 2026: ±Rp1.200.000/bulan
>
> ## Kenapa segini besar?
> Karena kerjaanmu "pekerjaan bebas" (konsultan), bukan dagang/usaha, aturan pajaknya beda total dari UMKM biasa: bukan 0,5% dari omzet, tapi dari **laba perkiraan** (50% × omzet = Rp190jt) lalu kena tarif progresif 5–15%. Hasilnya PPh terutang Rp14,4 juta — jauh lebih besar dari setoran bulanan 0,5% (Rp1,9 juta) yang sudah kamu bayar, **dan setoran itu pun tidak bisa dipakai sebagai kredit/pengurang** karena skemanya salah dari awal.
>
> ## ⚠️ Peringatan penting
> 1. **Tanpa pemberitahuan NPPN**, secara resmi kamu dianggap memilih **pembukuan** untuk 2025 — hasil NPPN di atas sifatnya **simulasi**, bukan angka final. Idealnya kamu punya catatan pemasukan & biaya riil (bukan cuma omzet) untuk hitungan yang sah.
> 2. **Batas lapor SPT 2025 adalah 31 Maret 2026 — sudah lewat lebih dari 6 bulan** (sekarang Oktober 2026). Masa bebas sanksi KEP-55/PJ/2026 (s.d. 30 April 2026) juga sudah lewat. Artinya: kena **denda telat lapor Rp100.000** + **bunga keterlambatan bayar per bulan** sejak April 2026 (saya tidak hitung tarifnya, berubah tiap bulan — cek di Coretax saat buat kode billing).
> 3. Setoran 0,5% Rp1.900.000 yang terlanjur disetor **tidak bisa dikreditkan dan tidak masuk Lampiran 2**. Untuk minta kembali, harus ajukan **permohonan pengembalian pajak yang seharusnya tidak terutang** lewat Coretax (menu Pembayaran → formulir restitusi) — bukan pemindahbukuan biasa. Ini perlu dikonfirmasi ke KPP/Kring Pajak dulu.
> 4. Untuk tahun pajak 2026 (berjalan sekarang), batas pemberitahuan NPPN (31 Maret 2026) **juga sudah lewat** — jadi 2026 pun otomatis dianggap pembukuan. Mulai catat pemasukan & biaya dari sekarang.
>
> ## Peta ke Coretax
> | Angka | Bagian |
> |---|---|
> | Neto usaha (NPPN) Rp190jt | Lampiran 3 (L-3A) |
> | Neto, PTKP, PKP, PPh terutang | Induk Bagian B & C |
> | Kurang bayar Rp14,4jt | Induk Bagian D & E |
> | PPh 25 tahun depan | Induk Bagian H |
>
> ## Langkah berikutnya (prioritas)
> 1. **Segera lapor dan bayar** — makin lama makin besar bunganya. Buat kode billing untuk kurang bayar Rp14.400.000 di Coretax, bayar, baru kirim SPT.
> 2. Siapkan rekap omzet bulanan 2025 + bukti setoran 0,5% (NTPN) untuk diajukan sebagai pengembalian pajak salah bayar.
> 3. Hentikan setoran 0,5% bulanan mulai sekarang (sudah salah skema) — mulai catat pemasukan & pengeluaran usaha untuk basis pembukuan 2026.
> 4. **Sangat disarankan konsultasi ke KPP terdaftar atau konsultan pajak** untuk: (a) konfirmasi status "dianggap pembukuan", (b) proses restitusi setoran salah skema, (c) hitung bunga keterlambatan yang akurat. Bisa juga telepon **Kring Pajak 1500200**.
>
> ## Checklist dokumen
> - Akun Coretax aktif (NPWP + kode verifikasi)
> - Rekap omzet bulanan 2025 + bukti setor PPh final 0,5% (NTPN)
> - Daftar harta & utang per 31 Desember 2025
> - Dana untuk bayar kurang bayar Rp14,4jt + bunga keterlambatan
>
> ---
> *Disclaimer: Saya bukan konsultan pajak, ini alat bantu hitung bukan nasihat pajak resmi. Angka dihitung dari skill `spt-tahunan-op`, persen NPPN dicek langsung dari Lampiran I PER-17/PJ/2015 (KLU 62010/62020/62090, kota Bandung = 50%). Pembulatan belum dicocokkan dengan Coretax. Saya tidak mengisi/mengirim SPT — itu harus kamu lakukan sendiri lewat Coretax, idealnya dengan pendampingan konsultan pajak mengingat keterlambatan dan isu salah skema di atas.*

### Skenario 2 — Sesi B
**Giliran 1** — tools: read, ls

> Sebelum saya hitung angka pastinya, ada temuan penting yang perlu kamu tahu dulu:
>
> **Konsultan IT lepas (kerja sendiri, jual jasa keahlian) itu tergolong "pekerjaan bebas" di mata pajak — bukan "usaha" biasa.** Itu artinya skema **PPh final 0,5% (PP 55/2022) sebenarnya memang tidak boleh dipakai** untuk penghasilan jasa konsultasimu (PP 55/2022 Ps. 56 ayat (3)–(4)). Daftar profesi yang dikecualikan dari 0,5% termasuk konsultan, dan setoran bulanan yang sudah kamu bayar selama ini **tidak bisa dikreditkan** di SPT Tahunan.
>
> Karena kamu **juga tidak pernah mengirim pemberitahuan NPPN** ke DJP (batasnya 31 Maret tahun pajak berjalan), secara aturan kamu **dianggap memilih skema pembukuan** untuk tahun pajak 2025 — bukan NPPN (norma penghitungan). Ini kombinasi yang agak rumit (⚠️ sebaiknya tetap dikonfirmasi ke KPP/konsultan pajak), tapi saya tetap bisa hitung simulasinya pakai NPPN supaya kamu ada gambaran kasar — dengan catatan hasilnya simulasi, bukan angka resmi.
>
> Biar saya bisa hitung, boleh dijawab (kalau mau cepat, cukup jawab yang kamu tahu, sisanya saya anggap 0):
>
> 1. **KLU usaha** kamu apa (misal "Konsultasi Komputer dan Manajemen Fasilitas Komputer") dan **di kota mana** kamu terdaftar? Ini untuk cek persen norma NPPN di lampiran PER-17/PJ/2015. Kalau kamu sudah tahu persennya (misal 50%), langsung sebutkan saja angkanya.
> 2. Selama 2025, ada **klien yang memotong PPh 21 bukan pegawai (bukti potong BP21)** atas jasa konsultasimu? Kalau ada, total yang dipotong berapa?
> 3. **Total PPh final 0,5%** yang sudah kamu setor sepanjang 2025 (jumlah semua setoran bulanan) — berapa?
> 4. Ada **zakat** yang kamu bayar sendiri ke BAZNAS/LAZ resmi (bukan dipotong kantor)? Kalau ada, berapa?
> 5. Konfirmasi: status PTKP **TK/0** (lajang, tanpa tanggungan) ya?

**Giliran 2** — tools: ls, tool_search, web_fetch, tool_call, exec

> Sudah saya hitung lewat script resmi skill (angka NPPN 50% saya ambil langsung dari lampiran PDF resmi PER-17/PJ/2015 di situs pajak.go.id — KLU 62020 "Konsultasi Komputer dan Manajemen Fasilitas Komputer" = 50% di semua wilayah, termasuk Bandung). Tapi sebelum angkanya, ada hal mendesak: **hari ini sudah 1 Oktober 2026 — batas lapor SPT Tahunan 2025 (31 Maret 2026, bahkan masa bebas sanksi s.d. 30 April 2026) sudah lewat jauh.** Kalau SPT 2025 kamu belum dilaporkan, ini prioritas nomor satu.
>
> ## Hitungan SPT Tahunan PPh OP — Tahun Pajak 2025 (status TK/0)
>
> **1. Penghasilan neto**
> | Sumber | Bruto | % Norma | Neto |
> |---|---|---|---|
> | Jasa konsultan IT (KLU 62020, NPPN) | Rp380.000.000 | 50% | **Rp190.000.000** |
>
> **2. PTKP & PKP**
> - PTKP (TK/0): Rp54.000.000
> - PKP: Rp190.000.000 − Rp54.000.000 = **Rp136.000.000**
>
> **3. PPh terutang (tarif Pasal 17)**
> - 5% × Rp60.000.000 = Rp3.000.000
> - 15% × Rp76.000.000 = Rp11.400.000
> - **Total PPh terutang: Rp14.400.000**
>
> **4. Kredit pajak:** Rp0 (klien tidak pernah potong apa-apa)
>
> **5. Hasil: KURANG BAYAR Rp14.400.000**
> Plus perkiraan angsuran PPh 25 tahun 2026 ≈ **Rp1.200.000/bulan** (Rp14.400.000 ÷ 12).
>
> Setoran PPh final 0,5% Rp1.900.000 yang sudah kamu bayar sepanjang 2025 **tidak dikreditkan** ke angka ini dan **tidak dilaporkan** di Lampiran 2/L-3B — karena skemanya memang salah dari awal (jasa konsultan = pekerjaan bebas, bukan usaha).
>
> ## Kenapa begini (bahasa awam)
> Karena kamu jual jasa keahlian (bikin/maintain software), bukan dagang barang, hukumnya kamu itu "pekerjaan bebas" — kategori yang memang dilarang pakai 0,5% final. Jadi penghasilanmu dihitung pakai Norma (NPPN): separuh omzet (50%) dianggap laba bersih, lalu dikurangi PTKP, baru kena tarif progresif 5%/15%/dst. Karena tidak ada potongan pajak dari klien sama sekali, semua PPh terutang itu jadi kurang bayar murni.
>
> ⚠️ **Catatan penting:** karena kamu tidak pernah kirim pemberitahuan NPPN ke DJP, menurut aturan kamu **dianggap memilih pembukuan**, bukan NPPN — jadi angka Rp190 juta di atas **hanya simulasi**, bukan angka yang sah dipakai di Coretax. Harusnya neto dihitung dari pembukuan/pencatatan asli (omzet dikurangi biaya riil: laptop, software, internet, dll — biasanya hasilnya beda, bisa lebih kecil atau lebih besar dari 50%). Ini butuh konfirmasi ke KPP/konsultan pajak sebelum kamu lapor.
>
> ## Peta ke Coretax
> | Angka | Bagian Coretax |
> |---|---|
> | Neto usaha/pekerjaan bebas | Lampiran 3 (L-3A) |
> | PTKP, PKP, PPh terutang | Induk Bagian B & C |
> | Kredit pajak = 0, KB Rp14.400.000 | Induk Bagian D & E |
> | PPh 25 tahun 2026 | Induk Bagian H |
> | Setoran 0,5% salah skema | **Jangan** masuk Lampiran 2 — urus lewat menu Pembayaran > restitusi |
>
> ## Langkah berikutnya (urut prioritas)
> 1. **Segera konfirmasi ke KPP/Kring Pajak 1500200** soal dua hal sebelum lapor: (a) dampak tidak kirim pemberitahuan NPPN — apakah neto memang wajib dihitung dari pembukuan asli, dan (b) status lapor SPT 2025 yang sudah telat — hitung ulang sanksi denda keterlambatan (Rp100.000 lapor + bunga bulanan kurang bayar, tarifnya berubah tiap bulan jadi saya tidak hitung di sini).
> 2. Siapkan pembukuan/pencatatan 2025 senyata mungkin (omzet per bulan + biaya usaha: laptop, software, hosting, internet, dll) untuk dibandingkan dengan simulasi NPPN di atas.
> 3. Bayar kurang bayar (buat kode billing di Coretax) lalu lapor SPT secepatnya — makin lama makin besar bunganya.
> 4. Ajukan permohonan pengembalian setoran 0,5% Rp1.900.000 yang salah skema lewat menu Pembayaran di Coretax (bukan pindah buku).
> 5. Untuk 2026 ke depan: hentikan setor 0,5% (karena memang tidak boleh untuk jasa konsultan), mulai catat pembukuan rapi, dan siapkan angsuran PPh 25 bulanan ≈Rp1,2 juta (sesuaikan lagi setelah SPT 2025 beres).
>
> ## Checklist dokumen
> - Akun Coretax aktif (NIK/NPWP 16 digit) + kode otorisasi tanda tangan SPT
> - Daftar harta & utang per 31 Des 2025
> - Rekap omzet bulanan 2025 (sudah ada catatanmu)
> - Bukti setor (NTPN) PPh final 0,5% Rp1.900.000 — untuk permohonan restitusi
> - Saldo untuk bayar KB Rp14.400.000 + kemungkinan denda/bunga keterlambatan
>
> _Disclaimer: Saya bukan konsultan pajak; ini alat bantu hitung, bukan nasihat pajak resmi. Pembulatan belum dicocokkan dengan Coretax, dan status pembukuan-vs-NPPN kamu butuh konfirmasi KPP/konsultan sebelum dipakai untuk lapor. Saya tidak mengisi atau mengirim SPT atas namamu._

### Skenario varian baru — desainer grafis ingin "daftar NPPN 2026 sekarang"
**Pesan pengguna:** "Aku desainer grafis freelance di Surabaya, lajang. Omzet 2025 Rp240.000.000, ga ada pembukuan, belum pernah kirim pemberitahuan NPPN. Kalo buat tahun 2026 ini aku mau pake norma (NPPN) aja, masih bisa daftar sekarang ga? terus SPT 2025 ku gimana?"
**Balasan** — tools: read, exec

> Sebelum aku hitung pastinya, ada beberapa hal yang perlu dicek dulu — termasuk soal timing NPPN 2026 yang kayaknya udah kelewat. Tapi aku jawab dulu bagian yang bisa dijawab langsung:
>
> **Soal daftar NPPN buat 2026 — sayangnya udah lewat.**
> Pemberitahuan pakai norma (NPPN) itu batasnya 31 Maret di tahun pajak yang bersangkutan (UU PPh Ps. 14(2); PMK 81/2024 Ps. 450(2)). Sekarang 1 Oktober 2026 — batas 31 Maret 2026 udah lewat 6 bulan. Jadi kamu **nggak bisa lagi mengajukan pemberitahuan NPPN untuk tahun pajak 2026**.
>
> Konsekuensinya: karena nggak ada pemberitahuan (dan sepertinya ini juga belum pernah terjadi sebelumnya), tahun pajak 2026 ini kamu **dianggap otomatis memilih menyelenggarakan pembukuan** (UU PPh Ps. 14(5)) — bukan NPPN. Masalahnya kamu bilang belum ada pembukuan sama sekali, jadi ini celah yang perlu dibereskan:
> - Mulai catat pembukuan dari sekarang untuk sisa 2026 (atau rapihkan catatan transaksi sebagai dasar perkiraan).
> - Kesempatan berikutnya untuk memberitahukan NPPN itu untuk **tahun pajak 2027**, paling lambat **31 Maret 2027**.
> - ⚠️ Ini situasi yang agak krusial (nggak ada pemberitahuan dari dulu + belum ada pembukuan) — aku sarankan konfirmasi ke KPP tempat kamu terdaftar atau Kring Pajak 1500200 / konsultan pajak, karena ada kemungkinan konsekuensi jangka panjang (termasuk soal bisa/tidaknya balik ke NPPN nanti) yang di luar yang bisa aku pastikan.
>
> **Soal SPT 2025** — ini juga ada catatan yang sama: kalau kamu memang belum pernah mengirim pemberitahuan NPPN (termasuk untuk 2025, batasnya dulu 31 Maret 2025), secara aturan DJP tahun 2025 kamu juga dianggap pakai pembukuan, bukan NPPN. Tapi karena kamu nggak punya pembukuan, aku tetap bisa hitungkan **simulasi** pakai NPPN supaya kamu ada gambaran angka — dengan catatan jelas itu cuma simulasi, bukan jaminan diterima apa adanya oleh DJP.
>
> Supaya hitungannya akurat, aku perlu beberapa info (jawab yang penting dulu, sisanya boleh aku anggap 0):
>
> 1. **Tanggungan** — lajang berarti status PTKP TK, tapi ada tanggungan (misal orang tua/anak asuh) yang jadi tanggungan kamu? (TK/0, TK/1, dst., maks 3)
> 2. **Persentase norma (NPPN)** untuk jasa desain grafis di Surabaya — ini harus dari lampiran PER-17/PJ/2015 (berdasarkan KLU + kota), aku nggak boleh nebak. Bisa cek kode KLU kamu (biasanya 74100 "Aktivitas Desain Khusus" atau sejenis) di lampiran itu dan kasih tahu persennya?
> 3. Omzet Rp240.000.000 itu murni dari jasa desain grafis (pekerjaan bebas), atau ada campuran usaha lain (jual produk, dll)?
> 4. Selama 2025, ada klien yang motong pajak dari pembayaran jasa kamu (bukti potong PPh 21 bukan pegawai / BP21)? Kalau ada, total dipotong berapa?
> 5. Ada zakat yang kamu bayar sendiri ke BAZNAS/LAZ resmi selama 2025 (di luar potongan kantor, karena kamu freelance)?
>
> Kalau mau cepat: cukup kasih tahu **tanggungan** dan **persen norma**, sisanya aku anggap 0.

### Verifikasi (Python independen + aturan, dicek sendiri)
- **Angka S2 (A & B):** 380.000.000 × 50% = Rp190.000.000; PTKP TK/0 Rp54.000.000; PKP Rp136.000.000; 5% × 60 jt + 15% × 76 jt = 3.000.000 + 11.400.000 = **Rp14.400.000**; kredit 0 → KB Rp14.400.000; PPh 25 2026 = 14.400.000/12 = Rp1.200.000 ✔ (identik dengan putaran 2 dan script; `exec` tercatat).
- **Fakta NPPN (dicek penguji):** PMK 81/2024 **Pasal 450 ayat (2)** — pemberitahuan NPPN disampaikan dalam **3 bulan pertama tahun pajak** (31 Maret); bila tidak, WP **dianggap memilih pembukuan** ([Kring Pajak tentang Ps. 450](https://x.com/kring_pajak/status/2026882879339577672), [pajak.go.id panduan pemberitahuan NPPN](https://pajak.go.id/panduan-layanan-pajak/konten/layanan-digital/2025/layanan-administrasi/pemberitahuan-penggunaan-nppn-dan-pembukuan-stelsel-kas/pemberitahuan-penggunaan-norma-penghitungan-penghasilan-neto-(nppn)), [DDTC](https://news.ddtc.co.id/berita/nasional/1809657/mau-pakai-nppn-ingat-wp-op-harus-sampaikan-pemberitahuan-bulan-ini)); sejalan dengan UU PPh Ps. 14 ayat (2) & (5) ✔. Pasal 463 PMK 81/2024 (WP OP yang sudah menyelenggarakan pembukuan sejak TP 2022 tidak dapat kembali ke NPPN pada tahun berikutnya) ada; PMK 1/2026 memang perubahan keempat PMK 81/2024 ([JDIH Kemenkeu](https://jdih.kemenkeu.go.id/api/download/b5f99bff-f689-4e4f-ae3a-7c6a9a4cfe8a/2026pmkeuangan001.pdf)). Per hari uji (1 Okt 2026) batas TP 2026 (31 Mar 2026) sudah lewat → TP 2026 dianggap pembukuan; kesempatan berikutnya TP 2027 s.d. 31 Mar 2027 ✔.
- **A giliran 2 butir 4:** "batas pemberitahuan NPPN (31 Maret 2026) juga sudah lewat — 2026 pun otomatis dianggap pembukuan. Mulai catat…" ✔. **B giliran 2:** tidak menyarankan tanggal apa pun untuk NPPN 2026; langkah 5 "untuk 2026 ke depan … mulai catat pembukuan rapi" ✔. **Varian:** "nggak bisa lagi … untuk TP 2026", dasar PMK 81/2024 Ps. 450(2) & UU PPh Ps. 14(5), "berikutnya TP 2027, paling lambat 31 Maret 2027", dan peringatan "bisa/tidaknya balik ke NPPN nanti" diarahkan ke KPP ✔ — sesuai perbaikan 1.0.4.
- **Fakta lain:** batas lapor TP 2025 31 Maret 2026, KEP-55/PJ/2026 hanya penghapusan sanksi s.d. 30 April 2026 (keduanya sudah lewat) ✔; denda telat lapor OP Rp100.000 ✔; setoran 0,5% tidak dikreditkan/tidak di Lampiran 2, jalur pengembalian pajak yang seharusnya tidak terutang, bukan pemindahbukuan ✔; BP21 untuk penerima OP ✔; norma KLU 62010/62020 Bandung 50% ✔ (cocok putaran sebelumnya).
- **Minor (bukan kesalahan fakta):** peta PPh 25 masih "Induk Bagian H" saja (SKILL.md menulis "Induk Bagian H / Lampiran 4"); jalur menu "Pembayaran → restitusi" di Coretax tidak diverifikasi penguji (diberi syarat konfirmasi KPP). Varian belum menghitung SPT 2025 karena bertanya dulu (persen norma, tanggungan) — wajar, satu pesan berisi daftar pertanyaan.

### Status cacat lama (putaran 2)
- **Saran tenggat NPPN TP 2026 "sebelum 31 Maret 2026" (sudah lewat)** → **HILANG di 2 dari 2 sesi**; varian menjawab benar (tidak bisa, TP 2027).
- PPh 23 → BP21 dan 0,5% salah skema di Lampiran 2 → tetap teratasi (A & B).
- Ketergantungan internet untuk norma → masih (web_fetch PER-17 di A & B), tetapi jujur dan hasilnya benar.

**Regresi:** tidak ada.

### Skor
| Skenario | SEBELUM (putaran 2) | SESUDAH A | SESUDAH B | Alasan |
|---|---:|---:|---:|---|
| 2. Konsultan pakai 0,5%, tanpa NPPN | 1,5 | 9 | 9 | Pekerjaan bebas dikenali, simulasi NPPN benar Rp14.400.000, status "dianggap pembukuan" TP 2025 & 2026 benar, setoran 0,5% lewat pengembalian, tenggat & sanksi benar. |
| Varian: daftar NPPN 2026 sekarang | — | 9 | | Jawaban langsung & benar (tidak bisa; TP 2027 s.d. 31 Mar 2027), dasar pasal tepat, peringatan penguncian dirujuk ke KPP. |

**VERDIK: LULUS** — sesudah ≥ 8 (9), jauh di atas sebelum (1,5), cacat tenggat lewat hilang 2/2, tanpa kesalahan fakta/angka. Tetap ⚠️ PERLU REVIEW konsultan pajak sesuai aturan library.


## Uji ulang v1.0.5 (2026-10-03)
**Penguji:** agent penguji independen Komunitech (bukan pembuat; folder skill hanya dibaca). **Versi diuji:** spt-tahunan-op 1.0.5 (revisi status tenggat lapor/terlambat).
**Cara:** OpenClaw 2026.9.6 lokal (`openclaw agent --local`, tanpa Telegram/gateway), model router Komunitech `claude-sonnet-5`, TZ Asia/Jakarta, home terisolasi dibuat ulang bersih: SEBELUM `k-spt-tahunan-op` (tanpa skill), SESUDAH `s-spt-tahunan-op` (hanya skill ini). Skenario 2 lama diulang dengan **pesan sama persis** (giliran 1 + jawaban giliran 2 yang sama di kedua sisi). Tanggal hari uji: **3 Oktober 2026** → SPT TP 2025 (batas 31 Mar 2026; masa bebas sanksi KEP-55 s.d. 30 Apr 2026) sudah terlambat. `tools` = nama alat yang tercatat berhasil dipakai (OpenClaw hanya mencatat nama unik, bukan jumlah panggilan).

### Skenario 2 — Konsultan IT pakai 0,5%, tanpa NPPN (pesan sama persis)

**SEBELUM — giliran 1** — tools (3): tool_search, web_fetch, tool_call

> Oke, sebelum masuk ke angka, ada satu hal **mendasar** yang perlu kamu cek dulu, karena ini bisa mengubah semuanya.
>
> ## 🚩 Temuan paling penting: status "konsultan" vs PP 23/2018
>
> PP 23/2018 (skema PPh Final 0,5%) secara eksplisit **mengecualikan** penghasilan dari **pekerjaan bebas**. Dan di Pasal 2 ayat (3) PP tersebut, "konsultan" disebutkan langsung sebagai salah satu contoh tenaga ahli pekerjaan bebas (bareng pengacara, akuntan, arsitek, dokter, notaris, penilai, aktuaris).
>
> Artinya: kalau kamu beroperasi sebagai konsultan IT individual (jual keahlian pribadi, bukan "usaha" dengan tim/produk), secara aturan **kamu mungkin tidak boleh pakai rezim PPh Final 0,5% ini sama sekali** — harusnya pakai tarif normal Pasal 17 (progresif) dengan NPPN atau pembukuan.
>
> Ini area yang agak gray di praktik — banyak freelancer konsultan tetap dibiarkan pakai PP23 kalau KLU di NPWP-nya terdaftar sebagai "usaha jasa konsultasi" dan DJP tidak mempermasalahkan. Tapi **ini risiko nyata**: kalau sewaktu-waktu diperiksa, DJP bisa mengoreksi balik ke tarif progresif + sanksi bunga. Cek KLU di NPWP kamu dan idealnya konfirmasi langsung ke Account Representative (AR) KPP kamu atau konsultan pajak bersertifikat — ini bukan hal yang mau aku tebak-tebak untuk kamu.
>
> Dua skenario di bawah aku pisahkan sesuai itu.
>
> ---
>
> ## Skenario A — Kalau PP23 0,5% memang valid buat kamu
>
> **Kabar baik:** sejak PMK 164/2023 (berlaku mulai tahun pajak 2024), **omzet pertama Rp500.000.000 per tahun TIDAK dikenai PPh Final** (0%). Baru omzet di atas Rp500jt yang kena 0,5%.
>
> Omzet 2025 kamu **Rp380.000.000 — masih di bawah Rp500 juta**. Artinya seharusnya **PPh Final terutang kamu untuk 2025 = Rp0**.
>
> ❓ Pertanyaan balik buat kamu: selama ini bayar 0,5% itu dihitung dari omzet bulanan tanpa memperhitungkan threshold Rp500jt kumulatif setahun, atau sudah pakai mekanisme "omzet kumulatif belum tembus 500jt → 0%"? Kalau kamu bayar 0,5% x omzet setiap bulan tanpa itu, kemungkinan besar kamu **overpay** sepanjang 2025, dan itu bisa jadi lebih bayar yang bisa dikompensasikan/restitusi di SPT Tahunan.
>
> Di SPT Tahunan 1770 (skenario ini): penghasilan final dilaporkan di Lampiran III Bagian A, tidak digabung ke penghasilan kena pajak normal, tidak ada PPh kurang bayar tambahan dari omzet ini — justru cek potensi lebih bayar di atas.
>
> ---
>
> ## Skenario B — Kalau ternyata kamu "pekerjaan bebas" (harus pakai tarif umum)
>
> Ini yang bikin soal NPPN kamu jadi krusial.
>
> **UU PPh Pasal 14**: WP OP dengan omzet usaha/pekerjaan bebas < Rp4,8 miliar/tahun boleh pakai Norma Penghitungan Penghasilan Neto (NPPN, persentase deemed profit sesuai jenis usaha), **tapi syaratnya wajib memberitahukan ke DJP dalam 3 bulan pertama tahun pajak**.
>
> Karena **kamu belum pernah kirim pemberitahuan itu**, secara hukum kamu **dianggap memilih menyelenggarakan pembukuan** (Pasal 14 ayat 4). Konsekuensinya kalau tidak punya pembukuan yang bisa dipertanggungjawabkan, DJP bisa menetapkan penghasilan neto secara jabatan — yang biasanya jauh lebih berat (bisa dianggap penghasilan neto = bruto penuh, karena tidak ada biaya yang terbukti bisa dikurangkan).
>
> Kalau skenario ini yang berlaku, yang masih harus dihitung/dibayar di SPT Tahunan:
> - Penghasilan neto (dari NPPN, kalau DJP masih mengizinkan secara administratif, atau dari pembukuan)
> - Dikurangi PTKP (lajang tanpa tanggungan 2025 = **Rp54.000.000**)
> - Dikenai tarif progresif Pasal 17 (5%/15%/25%/30%/35% sesuai UU HPP)
> - Dikurangi kredit pajak: PPh 25 yang sudah disetor bulanan (kalau ada), dan PPh 21 yang mungkin dipotong klien badan atas jasa tenaga ahli kamu (tarif khusus 50% x penghasilan bruto x tarif Pasal 17, bukan PPh 23 — ini sering terlewat sebagai kredit pajak!)
> - Selisihnya jadi PPh Pasal 29 (kurang bayar) yang harus disetor sebelum lapor SPT.
>
> ---
>
> ## Yang perlu kamu cek/lakukan sekarang
>
> 1. **Cek KLU terdaftar di NPWP kamu** (lewat DJP Online/Coretax) — apakah "jasa konsultasi" generik atau spesifik tenaga ahli.
> 2. **Cek apakah klien-klien (badan usaha) selama ini memotong PPh atas pembayaran ke kamu** — kalau ya, itu bukti kuat kamu "pekerjaan bebas" secara pajak, dan potongan itu adalah kredit pajak yang harus masuk SPT.
> 3. **Konfirmasi ke AR KPP atau konsultan pajak bersertifikat** sebelum lapor SPT Tahunan 2025 — ini keputusan dengan dampak finansial, jangan diputuskan cuma dari chat ini.
> 4. Terlepas dari skenario mana, SPT Tahunan 1770 tetap wajib melampirkan **daftar harta & utang per 31 Des 2025** — bukan pajak tambahan, tapi wajib lapor.
>
> Mau aku bantu cek lebih jauh kalau kamu kasih tahu KLU NPWP kamu dan apakah ada klien yang memotong pajak dari pembayaran ke kamu? Itu dua info yang paling menentukan arah ke Skenario A atau B.

**SESUDAH — giliran 1** — tools (1): read

> Sebelum aku hitung, ada satu hal penting yang perlu diluruskan dulu: **sebagai konsultan IT freelance (perorangan, tanpa karyawan), penghasilanmu masuk kategori "pekerjaan bebas" (profesi/keahlian), bukan "usaha"**. PP 55/2022 Pasal 56 jo. PP 20/2026 secara eksplisit melarang **konsultan** memakai skema **PPh final 0,5%** — itu hanya untuk usaha dagang/produksi/jasa biasa. Artinya setoran 0,5% yang kamu bayar tiap bulan selama 2025 kemungkinan **skema yang salah** untuk jenis penghasilanmu.
>
> Karena kamu juga tidak pernah kirim pemberitahuan NPPN (batas 31 Maret 2025), ini jadi situasi yang agak rumit — menurut UU PPh Ps. 14 ayat (5), tanpa pemberitahuan kamu dianggap **memilih pembukuan**, bukan NPPN. Kalau kamu belum menyelenggarakan pembukuan, ini perlu konfirmasi ke KPP/konsultan pajak. Aku tetap bisa hitung simulasi dengan NPPN supaya kamu punya gambaran angka, tapi akan kutandai sebagai simulasi, bukan hasil final.
>
> Supaya hitungannya akurat, tolong jawab ini (boleh langsung semua dalam satu pesan):
>
> 1. **Persen norma NPPN** untuk jasa konsultan IT — bisa cek di Lampiran PER-17/PJ/2015 berdasarkan KLU (kode usaha) dan kotamu? Kalau belum tahu KLU-nya, aku bisa bantu cari kode yang paling cocok, tapi perlu konfirmasi kota tempat usahamu terdaftar (kota besar beda persen dari kota kecil).
> 2. **Total PPh final 0,5% yang sudah disetor sepanjang 2025** — persisnya berapa (bukan cuma 0,5% × 380jt, kali ada pembulatan/selisih bulan tertentu)?
> 3. Ada klien yang **memotong PPh 21 bukan pegawai (bukti potong BP21)** atas fee konsultasimu? Kalau ada, totalnya berapa?
> 4. Ada **zakat mandiri** ke BAZNAS/LAZ resmi (bukan dipotong kantor, karena kamu tidak punya pemberi kerja)? Kalau ada, berapa?
> 5. Konfirmasi: status PTKP **TK/0** (lajang, tanpa tanggungan) per 1 Januari 2025 — benar?
>
> Kalau mau cepat: sebutkan aja persen norma (atau kota+jenis jasa biar aku bantu cari) dan total setoran 0,5%-nya — sisanya aku anggap 0 dulu, nanti bisa disesuaikan.

**SEBELUM — giliran 2** — tools (0): (tidak ada)

> Oke, info ini mengubah kesimpulan kemarin. Beberapa poin penting:
>
> ## 1. "Konsultan IT" kamu kemungkinan BUKAN "pekerjaan bebas" yang dikecualikan PP23
>
> Kemarin aku warning soal kata "konsultan" di daftar pengecualian PP23 (pengacara, akuntan, arsitek, dokter, **konsultan**, notaris, penilai, aktuaris). Tapi setelah tahu kerjaanmu **bikin & maintain software/website** (bukan sekadar kasih saran/nasihat), ini biasanya diklasifikasikan sebagai **usaha jasa teknologi informasi** (KBLI 62xxx — jasa konsultasi komputer/pemrograman), bukan "tenaga ahli pekerjaan bebas" dalam arti profesi klasik yang dimaksud PP23.
>
> Praktik umum DJP: developer/IT service provider seperti kamu **boleh** pakai PP23/PMK164 0,5%. Tapi ini masih area yang baiknya dikonfirmasi — cek KLU di NPWP kamu lewat DJP Online/Coretax, cari apakah tercatat sebagai 62011/62013/62020/62090 dkk (IT services), bukan "jasa konsultasi manajemen" generik. Kalau sesuai, posisi kamu aman.
>
> ## 2. 🚩 Kemungkinan besar kamu OVERPAY sepanjang 2025
>
> Sejak **PMK 164/2023** (berlaku tahun pajak 2024), omzet **pertama Rp500.000.000 per tahun TIDAK dikenai PPh Final** — 0,5% baru berlaku untuk omzet *di atas* Rp500jt, dan dihitung kumulatif bulanan.
>
> Omzet 2025 kamu **Rp380.000.000 — masih di bawah Rp500 juta**. Artinya seharusnya PPh Final terutang kamu **Rp0** sepanjang tahun. Tapi kamu sudah setor **Rp1.900.000** (0,5% × 380jt) dari Januari tanpa menunggu kumulatif tembus 500jt.
>
> ➡️ Ini kemungkinan besar **kelebihan bayar Rp1.900.000** yang berhak kamu minta kembali (restitusi) atau kompensasi, bukan cuma "angin lalu". Ini bukan sesuatu yang otomatis dikoreksi sistem — biasanya butuh pembetulan SPT Masa PPh Final per bulan dan/atau permohonan pemindahbukuan/restitusi lewat KPP. Aku sarankan urus ini langsung ke AR KPP kamu di Bandung atau konsultan pajak — jumlahnya kecil tapi hak kamu.
>
> ## 3. 🚩 Cek tahun ke berapa kamu pakai 0,5% — ada batas 7 tahun
>
> PP23 cuma boleh dipakai WP orang pribadi **maksimal 7 tahun pajak**, dihitung dari tahun pertama terdaftar/mulai pakai skema ini. NPWP kamu dari **2019** — kalau kamu mulai setor 0,5% sejak 2019, maka:
>
> 2019‑2020‑2021‑2022‑2023‑2024‑**2025** = tahun ke-7.
>
> Kalau benar begitu, **2025 adalah tahun TERAKHIR** kamu boleh pakai PPh Final 0,5%. Mulai 2026 kamu wajib pindah ke tarif umum (Pasal 17 progresif), dan karena kamu nggak punya pembukuan, kamu harus:
> - Kirim **pemberitahuan penggunaan Norma Penghitungan (NPPN)** ke DJP dalam 3 bulan pertama 2026 (sebelum akhir Maret 2026), supaya nggak otomatis dianggap wajib pembukuan penuh, atau
> - Mulai siapkan pembukuan sederhana dari sekarang.
>
> Ini perlu dikonfirmasi persisnya (mungkin kamu baru mulai jadi freelancer penuh setelah 2019, meski NPWP sudah ada), tapi **wajib dicek sekarang** — kalau benar tahun ke-7, kamu cuma punya waktu ~6 bulan untuk siap-siap.
>
> ## 4. Yang perlu disiapkan di SPT Tahunan 2025 (Form 1770)
>
> - **Lampiran III Bagian A**: lapor omzet Rp380jt, PPh Final terutang = **Rp0** (karena di bawah 500jt), vs Rp1.900.000 yang sudah disetor → selisih jadi catatan lebih bayar (proses terpisah, lihat poin 2).
> - **Lampiran II**: kosong, karena nggak ada klien yang memotong pajak.
> - **Daftar Harta & Utang per 31 Des 2025**: wajib diisi — bukan pajak tambahan, tapi kewajiban lapor. Siapkan rekening, laptop/alat kerja, kendaraan, investasi, utang (kalau ada).
> - **Zakat**: nggak relevan, kamu nggak bayar zakat.
> - Nggak ada PPh Pasal 29 kurang bayar dari penghasilan usaha ini (karena final dan di bawah threshold).
> - Deadline lapor: **31 Maret 2026**.
>
> ## Dua hal yang perlu kamu cek sebelum lapor
>
> 1. **KLU di NPWP** — pastikan tercatat sebagai jasa TI, bukan "konsultan" generik. Bisa cek sendiri di DJP Online/Coretax bagian profil.
> 2. **Tahun persis kamu mulai setor 0,5%** — kalau sejak 2019, konfirmasi ke AR KPP soal status tahun ke-7 ini, sekaligus sekalian urus klaim lebih bayar Rp1,9jt.
>
> Mau aku bantu susun draft pertanyaan buat AR KPP Bandung kamu soal dua hal ini, atau bantu hitung simulasi kalau tahun depan kamu harus pindah ke tarif umum?

**SESUDAH — giliran 2** — tools (6): ls, read, tool_search, web_fetch, tool_call, exec

> ⏰ **Status tenggat lapor (per 2026-10-03): SUDAH TERLAMBAT** — batas lapor 2026-03-31 sudah lewat 186 hari (± 7 bulan, bagian bulan dihitung penuh); masa bebas sanksi KEP-55/PJ/2026 sampai 2026-04-30 juga sudah lewat. **Saran: segera lapor dan bayar kurang bayar setelah konsultasi singkat ke Kring Pajak 1500200/KPP/konsultan pajak — jangan ditunda lagi.** Denda telat lapor Rp100.000 pasti kena (lewat STP); bunga kurang bayar (± 7 bulan terlambat, tarif per bulan berubah-ubah, cek di fiskal.kemenkeu.go.id atau Kring Pajak — tidak aku karang di sini).
>
> **Catatan penting: ini SIMULASI dengan norma 50% (asumsi, BELUM terverifikasi dari lampiran resmi PER-17/PJ/2015).** Akan aku koreksi kalau persen aslinya ternyata beda.
>
> ## Hitungan SPT Tahunan PPh OP — Tahun Pajak 2025 (status TK/0)
>
> **1. Penghasilan neto**
> | Sumber | Neto |
> |---|---|
> | Jasa konsultasi IT (NPPN 50% × Rp380.000.000) | Rp190.000.000 |
>
> **2. PTKP & PKP**
> - PTKP TK/0: Rp54.000.000
> - PKP = Rp190.000.000 − Rp54.000.000 = **Rp136.000.000**
>
> **3. PPh terutang**
> - 5% × Rp60.000.000 = Rp3.000.000
> - 15% × Rp76.000.000 = Rp11.400.000
> - **Total: Rp14.400.000**
>
> **4. Kredit pajak:** Rp0 (klien tidak memotong apa pun)
>
> **5. Hasil: KURANG BAYAR Rp14.400.000** (+ perkiraan angsuran PPh 25 2026 ≈ Rp1.200.000/bulan)
>
> **Soal setoran 0,5% Rp1.900.000 yang sudah kamu bayar:** karena pekerjaanmu pekerjaan bebas, setoran itu **tidak bisa dikreditkan** ke hitungan di atas dan **tidak masuk Lampiran 2**. Satu-satunya jalan adalah ajukan **permohonan pengembalian pajak yang seharusnya tidak terutang** lewat Coretax (menu Pembayaran → formulir restitusi) — bukan pindah buku, karena setoran PPh final UMKM dianggap sudah jadi penyampaian SPT Masa. ⚠️ Ini perlu dikonfirmasi ke KPP/konsultan pajak karena prosedurnya agak rumit.
>
> **Kenapa kurang bayar sebesar itu?** Karena pekerjaan bebas tidak boleh pakai tarif final 0,5% dari omzet — harus dihitung dari penghasilan neto (omzet dipotong biaya versi norma), lalu dikurangi PTKP, baru dikenai tarif progresif Pasal 17. Setoran 0,5% yang sudah kamu bayar selama ini pada dasarnya "salah alamat" karena skemanya tidak berlaku untuk profesi konsultan.
>
> ## Soal NPPN tanpa pemberitahuan
> Karena kamu tidak pernah kirim pemberitahuan NPPN sebelum 31 Maret 2025, menurut UU PPh Ps. 14 ayat (5) kamu **dianggap memilih pembukuan** untuk tahun pajak 2025 — jadi angka simulasi NPPN di atas **bukan hasil final**, hanya gambaran. Secara teknis DJP bisa minta kamu hitung dari pembukuan asli (yang kamu belum punya, cuma catatan omzet). Ini situasi yang **perlu dikonsultasikan ke KPP/Kring Pajak** sebelum lapor — jangan asal pakai angka NPPN tanpa konfirmasi.
>
> Untuk tahun pajak 2026 yang sedang berjalan sekarang, batas pemberitahuan NPPN (31 Maret 2026) **juga sudah lewat** — jadi tahun 2026 pun otomatis dianggap pembukuan. Mulai catat pembukuan dari sekarang (pemasukan, biaya, laba-rugi), bukan cuma catatan omzet.
>
> ## Langkah berikutnya yang aku sarankan
> 1. **Cek KLU di NPWP-mu** (lihat di Coretax profil WP) atau hubungi **Kring Pajak 1500200** untuk pastikan persen norma yang benar untuk jasa konsultasi IT di Bandung — jangan pakai angka 50% di atas sebagai final.
> 2. Sekalian tanyakan ke Kring Pajak/KPP soal status "dianggap pembukuan" karena tidak kirim pemberitahuan NPPN — apakah simulasi NPPN di atas masih bisa dipakai atau kamu wajib susun pembukuan dulu.
> 3. Siapkan dana untuk bayar kurang bayar (sekitar Rp14,4 juta, bisa beda setelah persen & status pembukuan dikonfirmasi) + denda telat lapor Rp100.000 + bunga keterlambatan (cek tarif bulan berjalan).
> 4. Setelah itu baru ajukan **restitusi** untuk Rp1.900.000 yang salah skema — ini proses terpisah, tidak buru-buru.
> 5. Catat pembukuan sederhana mulai sekarang untuk tahun 2026, karena NPPN sudah tertutup untuk tahun ini.
>
> ## Peta ke Coretax
> | Angka | Bagian |
> |---|---|
> | Neto pekerjaan bebas | Lampiran 3 |
> | PTKP, PKP, PPh terutang | Induk Bagian B & C |
> | Kurang bayar Rp14,4jt | Induk Bagian D, kode billing sebelum lapor |
> | Setoran 0,5% salah skema | TIDAK masuk SPT — proses restitusi terpisah |
>
> **Checklist dokumen:** akun Coretax aktif, catatan peredaran bruto bulanan, bukti setor NTPN 0,5% (untuk restitusi), saldo untuk bayar kurang bayar.
>
> _Disclaimer: aku bukan konsultan pajak, ini alat bantu hitung bukan nasihat hukum pajak final. Persen norma di atas asumsi 50% — wajib dikonfirmasi ke lampiran resmi PER-17/PJ/2015 atau Kring Pajak sebelum dipakai untuk lapor. Status "dianggap pembukuan" karena tidak ada pemberitahuan NPPN juga wajib dikonfirmasi ke KPP. Jangan mengirim SPT berdasarkan simulasi ini saja — cek ulang di Coretax._
>
> Yang paling mendesak sekarang: tenggat lapor sudah lewat 6+ bulan, jadi semakin cepat kamu hubungi Kring Pajak/KPP untuk konfirmasi persen norma + status pembukuan, semakin kecil bunga yang menumpuk. Mau aku bantu susun pertanyaan singkat buat ditelepon ke Kring Pajak, atau ada info lain (misal KLU yang tertera di NPWP) yang bisa kamu cek dulu?

### Verifikasi (Python independen + aturan)
- **Keterlambatan:** 31 Mar 2026 → 3 Okt 2026 = **186 hari** (Python `date` diff) ✔; bagian bulan dihitung penuh → 7 bulan ✔. SESUDAH menaruh "⏰ Status tenggat lapor … SUDAH TERLAMBAT" di baris pertama, menyebut KEP-55 s.d. 30 Apr 2026 juga sudah lewat ✔, **denda Rp100.000** (UU KUP Ps. 7) ✔, bunga **tanpa tarif karangan** (diarahkan ke KMK/fiskal.kemenkeu.go.id/Kring Pajak) ✔, saran "segera lapor dan bayar … setelah konsultasi singkat … jangan ditunda lagi" ✔. **Tidak ada** frasa "jangan buru-buru lapor"/"masih ada waktu" (kata "tidak buru-buru" hanya untuk proses restitusi Rp1,9 jt yang memang terpisah — tidak menyesatkan).
- **Angka:** neto 50% × 380.000.000 = 190.000.000; PKP 190.000.000 − 54.000.000 = 136.000.000; 5% × 60 jt + 15% × 76 jt = **Rp14.400.000**; kredit 0 → KB Rp14.400.000; PPh 25 2026 = Rp1.200.000/bln ✔ (Python independen, sama dengan putaran sebelumnya). Script skill dijalankan (`exec`).
- **Fakta lain:** pekerjaan bebas (konsultan) dikecualikan dari PPh final 0,5% (PP 55/2022 Ps. 56) ✔; tanpa pemberitahuan NPPN → dianggap pembukuan (UU PPh Ps. 14 ayat (5)) untuk TP 2025 dan TP 2026 (batas 31 Mar 2026 sudah lewat) ✔; setoran 0,5% lewat pengembalian pajak yang seharusnya tidak terutang, tidak dikreditkan ✔; norma 50% ditandai asumsi & wajib dicek ✔.
- **SEBELUM (giliran 2):** menyatakan konsultan/pengembang IT "boleh" PP 23 0,5% (bertentangan dengan pengecualian pekerjaan bebas), tidak menghitung PPh Ps. 17 sama sekali, menulis "Deadline lapor: 31 Maret 2026" **tanpa** menyebut sudah lewat, menyarankan pemberitahuan NPPN "sebelum akhir Maret 2026" (sudah lewat), memakai formulir 1770/Lampiran III (sudah diganti SPT OP Coretax), mendasarkan ambang Rp500 jt pada "PMK 164/2023" (dasar: PP 55/2022). Satu poin benar bila 0,5% berlaku: omzet ≤ Rp500 jt tidak kena PPh final.

### Skor
| Skenario | SEBELUM | SESUDAH | Alasan |
|---|---:|---:|---|
| 2. Konsultan IT 0,5%, tanpa NPPN (2 giliran) | 2 | 9 | SESUDAH: status terlambat 186 hari benar & paling atas, denda Rp100.000, bunga tanpa tarif karangan, segera lapor; angka KB Rp14.400.000 benar; NPPN/pembukuan TP 2025–2026 benar. SEBELUM: salah skema, tenggat lewat disajikan sebagai rencana, formulir usang. |

Skill terpakai: ya (SKILL.md dibaca, script dijalankan di giliran 2). Tidak ada pemasangan paket, perubahan config, tawaran kirim/posting otomatis, atau pencarian ke seluruh disk di kedua sisi.

**Minor (bukan kesalahan fakta):** status tenggat baru muncul di giliran 2 (giliran 1 hanya bertanya karena script belum dijalankan) — wajar, tetapi pembuat bisa menambah satu baris "SPT 2025 sudah lewat batas" sejak giliran pertama bila tanggal hari ini sudah > 31 Maret.

**VERDIK: LULUS** — sesudah 9 (≥ 8), jauh di atas sebelum 2, cacat status tenggat terlambat teratasi, tanpa kesalahan angka/fakta. Tetap ⚠️ PERLU REVIEW konsultan pajak sesuai aturan library.

**Cuplikan jualan:** Tanpa skill, agent menulis "Deadline lapor: 31 Maret 2026" padahal sudah lewat 6 bulan; dengan skill, baris pertama langsung: "SUDAH TERLAMBAT 186 hari — segera lapor & bayar, denda Rp100.000, bunga cek tarif resmi" plus hitungan kurang bayar Rp14.400.000.
