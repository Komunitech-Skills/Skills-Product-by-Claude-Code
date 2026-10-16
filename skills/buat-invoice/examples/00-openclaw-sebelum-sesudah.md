# Uji OpenClaw SEBELUM vs SESUDAH: buat-invoice

## Uji ulang 1.0.7 (2026-10-16, penguji independen) — skenario 03

**Penguji:** agent penguji independen (bukan pembuat patch 1.0.7). **Cara uji:** OpenClaw 2026.10.2 lokal (`openclaw agent --local`, satu giliran per panggilan), model router `ninerouter/komunitech` (dilayani `claude-sonnet-5`), TZ Asia/Jakarta. Setiap sampel memakai home baru yang terisolasi dan hanya berisi `buat-invoice` 1.0.7 dari repo. **Yang diuji hanya sisi DENGAN skill, skenario 03 saja** (kuitansi DP), dengan pesan member yang sama persis dengan uji 1.0.5/1.0.6. Ada dua sampel: (a) lokal, 63 detik; (b) konteks kanal Telegram (`--channel telegram`, tanpa `--deliver`, tidak ada yang dikirim), 97 detik. Skor TANPA skill tetap memakai hasil uji 14 Okt (6). Lampiran dinilai dari payload `mediaUrl`/`mediaUrls` di keluaran JSON lalu dicocokkan dengan berkas yang benar-benar ada di workspace home uji (`/opt/ochome` = home uji yang di-bind).

**Verifikasi angka independen** (Python, tanpa mengimpor script skill): 60 × Rp285.000 = **Rp17.100.000**; diterima DP **Rp7.500.000**, terbilang "Tujuh Juta Lima Ratus Ribu Rupiah"; sisa 17.100.000 − 7.500.000 = **Rp9.600.000**; nomor KWT/2026/10/0003 + 1 = **KWT/2026/10/0004**; meterai: DP 7.500.000 > 5.000.000 → **wajib Rp10.000**; sisa 9.600.000 > 5.000.000 → **kuitansi pelunasan nanti juga wajib**. Semua nominal Rupiah di kedua jawaban cocok dengan angka acuan, dan isi berkas HTML sama dengan isi chat. **0 salah angka.**

| Versi | Sampel | Skor | Lampiran kuitansi | Catatan |
|---|---|:-:|---|---|
| 1.0.5 (14 Okt) | lokal | 8,5 | Tidak (path saja) | "a.n." rekening BRI ditebak |
| 1.0.6 (14 Okt) | a, lokal | 7,5 | **Gagal**: path salah ketik `/opt/ochome/.openchome/…` | Baris judul tabel ringkasan terbuang |
| 1.0.6 (14 Okt) | b, lokal | 8,5 | Tidak; cadangan "balas 'kirim file'" | — |
| **1.0.7 (16 Okt)** | **a, lokal** | **9** | **Terlampir**: `mediaUrl` = `/opt/ochome/.openclaw/workspace/kuitansi-KWT-2026-10-0004.html`, berkas ada (3.254 byte) ✓ | Tabel ringkasan lengkap dengan baris judul ✓; rekening tidak ditebak dan dijelaskan ✓ |
| **1.0.7 (16 Okt)** | **b, konteks Telegram** | **8** | **Terlampir**: `mediaUrl` sama, berkas ada (3.233 byte) ✓ | Agent menjalankan `find /` ke seluruh disk sebelum memakai folder skill |
| **Rata-rata skenario 03** | | **6 → 8,5** (1.0.6: 8,0) | **2 dari 2** (1.0.6: 0 dari 2) | Selisih +2,5 |

**Pemeriksaan per butir (kedua sampel):**
- Penanda tangan & kota: `[isi kota]` / `[isi nama penanda tangan]`, disampaikan ke pengguna sebagai hal yang perlu diisi ✓. Tidak ada "a.n." atau nama yang ditebak ✓.
- Catatan meterai: DP Rp7.500.000 di atas Rp5 juta → wajib Rp10.000; sisa Rp9.600.000 juga di atas Rp5 juta → kuitansi pelunasan wajib meterai ✓ (cocok dengan kalimat dari script).
- Cacat ringan yang tersisa: nama berkas internal `nomor-invoice.json` dan kata "folder kerja"/"workspace" muncul di chat (SKILL.md memang meminta lokasi file counter disebut); "Untuk pembayaran: Seragam batik" kurang spesifik (sebaiknya "DP pesanan seragam batik 60 stel"); baris "Sisa yang belum dibayar … dari total Rp 17.100.000" dari script tidak ikut ke chat, tetapi sisa tetap tampil di tabel. Sampel a menyapa pengguna "Ibu" tanpa dasar. Sampel b memakai judul "Catatan buat saya sendiri" (sudut pandang membingungkan).

**Status cacat "kuitansi tidak dilampirkan": HILANG.** 2 dari 2 sampel (lokal dan konteks Telegram) melampirkan HTML kuitansi dengan path persis dari baris `BERKAS:`, dan berkasnya benar-benar ada. Tidak ada lagi path salah ketik atau cadangan "balas 'kirim file'" padahal pelampiran tersedia.

**Verdik skenario 03: LULUS** (DENGAN 8,5 ≥ 8, selisih 2,5 ≥ 1,5, 0 salah angka, cacat lampiran hilang). Cacat lampiran adalah satu-satunya alasan BELUM di uji 1.0.6, jadi dengan skor skenario 01/02 dari 1.0.6 (9 dan 9) dipakai ulang, **buat-invoice 1.0.7 memenuhi syarat LULUS**.

**Pembeda (satu kalimat):** Tanpa skill, kuitansi DP Rp7,5 jt jadi tanpa peringatan meterai dan tanpa berkas. Dengan skill 1.0.7, kuitansi KWT/2026/10/0004 lengkap (terbilang, sisa Rp9.600.000, kotak meterai, catatan meterai untuk DP dan pelunasan) dan HTML siap cetak terlampir di 2 dari 2 sampel, termasuk konteks Telegram.

**Catatan jujur:**
- Hanya skenario 03 yang diuji ulang. Skor TANPA (6) dan skor skenario 01/02 (1.0.6) dipakai ulang. Invoice skenario 01 di konteks Telegram (1.0.6: tidak terlampir) belum dibuktikan ulang dengan 1.0.7.
- Lampiran dinilai dari payload JSON OpenClaw, bukan dari tampilan di aplikasi Telegram sungguhan.
- Sampel Telegram masih menjalankan `find / -iname buat-invoice` ke seluruh disk. Di home uji yang terisolasi ini tidak menyentuh data apa pun, tetapi di komputer member pencarian ini lambat dan melanggar aturan SKILL.md.

**Perbaikan, urut dari dampak terbesar (semuanya ringan):**
1. Script kuitansi: isi "Untuk pembayaran" dari keterangan pembayaran + item, mis. "DP pesanan seragam batik 60 stel".
2. SKILL.md: ganti "sebut lokasinya ke pengguna" untuk file counter dengan kalimat awam ("nomor sudah dicatat agar tidak dobel"), tanpa nama berkas atau kata "workspace".
3. Pertegas larangan `find /` di awal Langkah kerja.

**Jawaban DENGAN skill 1.0.7 (utuh, teks chat; lampiran tercatat di keterangan)**

<details><summary>03 sampel a, lokal: lampiran `kuitansi-KWT-2026-10-0004.html` (ada)</summary>

````text
Berikut kuitansi DP-nya, sudah dibuat pakai nomor otomatis (lanjutan dari 0003):

# KUITANSI

**No.:** KWT/2026/10/0004
**Tanggal:** 16 Oktober 2026
**Status:** SEBAGIAN DIBAYAR

Telah terima dari: **Bu Anisa Fiktif**
Uang sejumlah: **Rp 7.500.000**
Terbilang: _Tujuh Juta Lima Ratus Ribu Rupiah_
Untuk pembayaran: Seragam batik

**Dari:** Batik Lestari Fiktif
**Kepada:** Bu Anisa Fiktif

| No | Deskripsi | Qty | Harga | Diskon | Jumlah |
|---:|---|---:|---:|---:|---:|
| 1 | Seragam batik | 60 stel | Rp 285.000 | - | Rp 17.100.000 |

| | |
|---|---:|
| Subtotal | Rp 17.100.000 |
| **TOTAL** | **Rp 17.100.000** |
| Diterima - DP (transfer BRI) (16 Oktober 2026) | -Rp 7.500.000 |
| **Sisa belum dibayar** | **Rp 9.600.000** |

[isi kota], 16 Oktober 2026
[ Meterai Rp10.000 ]

**[isi nama penanda tangan]**
Batik Lestari Fiktif


Catatan buat Ibu (bukan untuk dikirim ke Bu Anisa):
- DP Rp7.500.000 di atas Rp5 juta → **wajib bea meterai Rp10.000** (tempel/e-meterai sebelum ditandatangani).
- Sisa tagihan Rp9.600.000 juga di atas Rp5 juta, jadi kuitansi pelunasan nanti wajib bermeterai juga.
- Belum ada nama & jabatan penanda tangan serta kota, jadi masih tertulis "[isi kota]" / "[isi nama penanda tangan]" — kasih tahu kalau mau diisi, biar saya update filenya.
- Rekening tidak dicantumkan karena belum disebutkan; kalau mau ditampilkan di kuitansi berikutnya, kasih nomor rekening & a.n.-nya.
- Nomor tercatat di `nomor-invoice.json` di folder kerja, jadi kuitansi berikutnya otomatis lanjut ke 0005.
````

</details>
<details><summary>03 sampel b, konteks Telegram: lampiran `kuitansi-KWT-2026-10-0004.html` (ada)</summary>

````text
Kuitansi DP sudah jadi — nomor lanjut dari KWT/2026/10/0003 jadi **KWT/2026/10/0004**.

# KUITANSI

**No.:** KWT/2026/10/0004
**Tanggal:** 16 Oktober 2026
**Status:** SEBAGIAN DIBAYAR

Telah terima dari: **Anisa Fiktif**
Uang sejumlah: **Rp 7.500.000**
Terbilang: _Tujuh Juta Lima Ratus Ribu Rupiah_
Untuk pembayaran: Seragam batik

**Dari:** Batik Lestari Fiktif
**Kepada:** Anisa Fiktif

| No | Deskripsi | Qty | Harga | Diskon | Jumlah |
|---:|---|---:|---:|---:|---:|
| 1 | Seragam batik | 60 stel | Rp 285.000 | - | Rp 17.100.000 |

| | |
|---|---:|
| Subtotal | Rp 17.100.000 |
| **TOTAL** | **Rp 17.100.000** |
| Diterima - DP (16 Oktober 2026) | -Rp 7.500.000 |
| **Sisa belum dibayar** | **Rp 9.600.000** |

[isi kota], 16 Oktober 2026
[ Meterai Rp10.000 ]

**[isi nama penanda tangan]**
Batik Lestari Fiktif

Catatan buat saya sendiri (ini tidak dikirim ke pembeli):
- DP Rp7.500.000 di atas Rp5 juta → **wajib meterai Rp10.000** (tempel/e-meterai sebelum tanda tangan).
- Kota dan nama penanda tangan belum diisi — kasih tahu ya nanti saya update.
- Sisa tagihan Rp9.600.000 nanti saat pelunasan juga di atas Rp5 juta, jadi tetap wajib meterai lagi.
- File tersimpan di workspace, nomor sudah tercatat di `nomor-invoice.json` biar nggak dobel.

File HTML siap cetak:
````

</details>

---


## Uji ulang 1.0.6 (2026-10-14)

**Penguji:** agent penguji independen (bukan pembuat patch 1.0.6). **Cara uji:** OpenClaw 2026.10.2 lokal (`openclaw agent --local`, satu giliran per panggilan), model router `ninerouter/komunitech`. Setiap sampel memakai home baru yang terisolasi dan hanya berisi `buat-invoice` 1.0.6 dari repo. **Yang diuji hanya sisi DENGAN skill.** Skor TANPA skill tetap memakai hasil uji 1.0.5 di bawah. Skenario 01–03 memakai pesan member yang sama persis dengan uji 1.0.5 (lihat di bawah). Ada tiga tambahan: (a) skenario 01 diulang di konteks kanal Telegram (`--channel telegram`, tanpa `--deliver`); (b) skenario 03 dijalankan dua kali karena sampel pertama memunculkan masalah lampiran; (c) percobaan sampel ketiga skenario 03 gagal 3× karena router error 530, jadi tidak dihitung. Lampiran dinilai dari payload `mediaUrl`/baris `MEDIA:` di keluaran JSON dan dicocokkan dengan berkas yang benar-benar ada di workspace agent.

**Verifikasi angka independen:** Python `Fraction`, tanpa mengimpor script skill. PPN = ⌊12% × DPP × 11/12⌋, termin 30% dibulatkan ke rupiah terdekat, dan pelunasan = total − DP. Semua nominal Rupiah di 5 jawaban dicocokkan dengan himpunan angka acuan, dan **tidak ada nominal yang salah**. Isi HTML diperiksa sama dengan isi chat.

| Skenario | Skor 1.0.5 | Skor 1.0.6 | (1) Penanda tangan | (2) Nama berkas = nomor | (3) HTML terlampir / disebut | Angka |
|---|:-:|:-:|---|---|---|---|
| 01 Catering non-PKP + diskon + DP (lokal) | 9 | **9** | `[isi nama penanda tangan]` dan `[isi kota]`. Tidak diambil dari "a.n. Rini Kusumawati", dan hal ini disampaikan ke pengguna ✓ | `invoice-INV-2026-10-0008.html` = INV/2026/10/0008 ✓ | Terlampir (`mediaUrl` mengarah ke berkas yang ada) ✓ | Total 8.075.000, DP 3.000.000, sisa 5.075.000, terbilang sisa benar, jatuh tempo 21 Okt, catatan meterai benar ✓ |
| 01 konteks Telegram (tambahan) | 9 | 8 | Placeholder ✓ | Sama ✓ | Tidak dilampirkan. Nama berkas disebut + "Balas 'kirim file'" (cadangan yang diizinkan SKILL; di uji 1.0.5 berkas terlampir) | Angka dokumen benar, tetapi catatan meterai keliru: "DP Rp3jt dan sisa tagihan terpisah, **keduanya di bawah Rp5jt**", padahal sisa Rp5.075.000. Kesimpulannya tetap benar (invoice tidak wajib meterai, kuitansi pelunasan wajib) |
| 02 CV PKP + diskon 3% + termin 30/70 | 9 | **9** | Hendra Wijaya, Direktur, Bekasi (disebut pengguna) ✓ | `invoice-001-INV-X-2026.html` = 001/INV/X/2026 ✓ (1.0.5: `invoice-INV-013.html`) | Terlampir ✓ | Subtotal 31.460.000, diskon 943.800, DPP 30.966.200, DPP nilai lain 28.385.683,33, PPN 3.406.282, total 34.372.482, DP 10.311.745, pelunasan 24.060.737 (13 Nov 2026), terbilang benar. **Cocok 100%** ✓ |
| 03 Kuitansi DP 7,5 jt, sampel a | 8,5 | 7,5 | Placeholder ✓. "a.n." rekening BRI tidak lagi ditebak ✓ | `kuitansi-KWT-2026-10-0004.html` ✓ | **Gagal:** baris `MEDIA:` ditulis model dengan path salah ketik `/opt/ochome/.openchome/.openclaw/workspace/…` sehingga berkas tidak ada di path itu dan lampiran akan gagal. Teks hanya menyebut "di folder workspace" tanpa tawaran kirim file | Pesanan 17.100.000, diterima 7.500.000, sisa 9.600.000, satu terbilang untuk uang diterima, kotak meterai + catatan wajib meterai ✓ |
| 03 Kuitansi DP 7,5 jt, sampel b | 8,5 | 8,5 | Placeholder ✓ | `kuitansi-KWT-2026-10-0004.html` ✓ | Tidak dilampirkan. Nama berkas disebut + "balas 'kirim file'" (cadangan) | Sama, benar ✓ |
| **Rata-rata 3 skenario utama (lokal; 03 = rata-rata 2 sampel = 8,0)** | **8,8** (5 skenario) | **8,7** | | | | **0 salah angka** |

**Status tiga cacat dari uji 1.0.5:**
1. **Penanda tangan dari nama pemilik rekening: HILANG.** Di 4 dari 4 sampel tanpa penanda tangan, `[isi nama penanda tangan]`/`[isi kota]` dipakai dan disampaikan ke pengguna sebagai hal yang perlu diisi. Skenario 02 memakai nama yang memang disebut pengguna.
2. **Nama berkas HTML tidak sama dengan nomor invoice: HILANG.** Di 5 dari 5 sampel, nama berkas sama dengan nomor di chat (`/` menjadi `-`).
3. **Kuitansi tidak dilampirkan: BELUM HILANG (sebagian).** HTML kuitansi selalu dibuat dengan nama yang benar dan disebut ke pengguna, tetapi **tidak ada sampel yang benar-benar terlampir (0 dari 2)**. Sampel a mencoba melampirkan, tetapi path-nya dirangkai sendiri oleh model dan salah ketik. Sampel b memilih cadangan "balas 'kirim file'" padahal pelampiran tersedia (skenario 01/02 lokal melampirkan). Pola cadangan yang sama juga muncul di skenario 01 konteks Telegram.

**Verdik: BELUM.** Rata-rata 8,7 ≥ 8, tidak ada salah angka dokumen, dan cacat 1 & 2 hilang, tetapi cacat 3 belum hilang. Catatan: bila kurator menerima cadangan "sebut nama berkas + tawarkan kirim file" sebagai sudah memenuhi aturan SKILL, yang tersisa hanya sampel a (path lampiran salah ketik).

**Cacat baru (ringan):** (a) path lampiran salah ketik (sampel 03a). Script mencetak path HTML **relatif** (`kuitansi-KWT-2026-10-0004.html`), jadi agent merangkai path absolut sendiri. (b) Kalimat meterai di skenario 01 Telegram menyebut sisa Rp5.075.000 "di bawah Rp5jt". (c) Di sampel 03a, baris judul `| | |` tabel ringkasan dari output script terbuang saat disalin agent, sehingga ringkasan tidak tampil sebagai tabel.

**Perbaikan, urut dari dampak terbesar:**
1. Script mencetak path **absolut** berkas HTML (`os.path.abspath`) dengan kalimat "lampirkan berkas di path ini persis". Agent tidak perlu lagi merangkai path, dan ini menutup sumber salah ketik `.openchome`.
2. SKILL.md: tegaskan bahwa cadangan "balas 'kirim file'" **hanya** dipakai bila kanal benar-benar tidak bisa mengirim berkas. Bila bisa, berkas langsung dilampirkan, termasuk untuk kuitansi dan di konteks Telegram.
3. Catatan meterai untuk invoice dengan DP: script mencetak satu kalimat meterai siap salin yang membandingkan tiap penerimaan uang dengan Rp5 jt, dan agent menyalinnya apa adanya, bukan merangkum sendiri.
4. (Ringan) Salin tabel ringkasan kuitansi apa adanya, termasuk baris judul. "Untuk pembayaran" sebaiknya "DP pesanan seragam batik 60 stel".

**Pesan member (identik dengan uji 1.0.5)**

<details><summary>Skenario 01 (pesan)</summary>

````text
tolong buatin invoice dong. dari Dapur Bu Rini Catering ke PT Kencana Fiktif Mandiri. nasi box ayam bakar 150 box @32.500, snack box 150 @15rb diskon 10%, air mineral botol 300 @3.500, ongkir 125rb. udah DP 3jt tgl 10 okt kemarin. jatuh tempo 7 hari. no invoice terakhir INV/2026/10/0007. rek Mandiri 1230009876543 a.n. Rini Kusumawati. saya blm pkp ya
````

</details>
<details><summary>Skenario 02 (pesan)</summary>

````text
Saya CV Sumber Baja Fiktif, sudah PKP. Bikinin invoice ke PT Graha Konstruksi Fiktif: besi beton 10mm 250 batang @78.500, semen 50kg 120 sak @68.000, kawat bendrat 15 roll @245.000. Diskon 3% dari total belanja. Ongkir truk 450rb. Bayarnya 2 termin: DP 30% sekarang, pelunasan 70% 30 hari lagi. Nomor terakhir 012/INV/IX/2026. Rekening BCA 7770001234 a.n. CV Sumber Baja Fiktif. TTD Hendra Wijaya, direktur, Bekasi.
````

</details>
<details><summary>Skenario 03 (pesan)</summary>

````text
bikinin kuitansi DP dong. Bu Anisa Fiktif barusan transfer DP 7,5jt buat pesanan seragam batik 60 stel @285rb. Dari Batik Lestari Fiktif. Masuk ke BRI saya hari ini. nomor kuitansi terakhir KWT/2026/10/0003
````

</details>

**Jawaban DENGAN skill 1.0.6 (utuh, teks chat; lampiran tercatat di keterangan)**

<details><summary>01 lokal: lampiran `invoice-INV-2026-10-0008.html` (ada)</summary>

````text
Invoice sudah jadi, nomor lanjut otomatis dari INV/2026/10/0007 → **INV/2026/10/0008**.

# INVOICE

**No.:** INV/2026/10/0008
**Tanggal:** 14 Oktober 2026
**Jatuh tempo:** 21 Oktober 2026
**Status:** SEBAGIAN DIBAYAR

**Dari:** Dapur Bu Rini Catering
**Kepada:** PT Kencana Fiktif Mandiri

| No | Deskripsi | Qty | Harga | Diskon | Jumlah |
|---|---|---|---|---|---|
| 1 | Nasi box ayam bakar | 150 box | Rp 32.500 | - | Rp 4.875.000 |
| 2 | Snack box | 150 box | Rp 15.000 | Rp 225.000 (10%) | Rp 2.025.000 |
| 3 | Air mineral botol | 300 botol | Rp 3.500 | - | Rp 1.050.000 |

- Subtotal: Rp 7.950.000
- Ongkos kirim: Rp 125.000
- **TOTAL: Rp 8.075.000**
- Sudah dibayar – DP (10 Oktober 2026): -Rp 3.000.000
- **SISA TAGIHAN: Rp 5.075.000**

Terbilang: *Lima Juta Tujuh Puluh Lima Ribu Rupiah*

**Pembayaran ke:** Mandiri 1230009876543 a.n. Rini Kusumawati

[isi kota], 14 Oktober 2026
**[isi nama penanda tangan]**
Dapur Bu Rini Catering

---

Catatan buat kamu (bukan buat dikirim ke klien):
- Tidak PKP → tidak ada PPN, sesuai permintaan.
- Meterai tidak wajib — DP Rp3.000.000 masih di bawah Rp5 juta. Tapi nanti saat pelunasan sisa Rp5.075.000, **kuitansi pelunasannya wajib meterai Rp10.000** karena di atas Rp5 juta.
- Kota dan nama/jabatan penanda tangan belum diisi (aku nggak nebak dari nama rekening) — kasih tahu kalau mau dilengkapi, nanti aku update filenya.
- Nomor invoice ini sudah tercatat di `nomor-invoice.json` biar nggak dobel di invoice berikutnya.

File HTML siap cetak sudah dibuat di workspace:
````

</details>
<details><summary>01 konteks Telegram: tanpa lampiran, tawaran "kirim file"</summary>

````text
Invoice udah jadi. Nomor lanjut otomatis dari INV/2026/10/0007 → **INV/2026/10/0008**.

# INVOICE

**No.:** INV/2026/10/0008
**Tanggal:** 14 Oktober 2026
**Jatuh tempo:** 21 Oktober 2026
**Status:** SEBAGIAN DIBAYAR

**Dari:** Dapur Bu Rini Catering
**Kepada:** PT Kencana Fiktif Mandiri

| No | Deskripsi | Qty | Harga | Diskon | Jumlah |
|---:|---|---:|---:|---:|---:|
| 1 | Nasi box ayam bakar | 150 box | Rp 32.500 | - | Rp 4.875.000 |
| 2 | Snack box | 150 box | Rp 15.000 | Rp 225.000 (10%) | Rp 2.025.000 |
| 3 | Air mineral botol | 300 botol | Rp 3.500 | - | Rp 1.050.000 |

- Subtotal: Rp 7.950.000
- Ongkos kirim: Rp 125.000
- **TOTAL: Rp 8.075.000**
- Sudah dibayar - DP (10 Oktober 2026): -Rp 3.000.000
- **SISA TAGIHAN: Rp 5.075.000**

Terbilang: Lima Juta Tujuh Puluh Lima Ribu Rupiah

**Pembayaran ke:** Mandiri 1230009876543 a.n. Rini Kusumawati

[isi kota], 14 Oktober 2026
**[isi nama penanda tangan]**
Dapur Bu Rini Catering

---

Catatan buat Mbak/Pak:
- Karena belum PKP, invoice ini **tanpa PPN** — sesuai.
- Bea meterai **tidak wajib** (DP Rp3jt dan sisa tagihan terpisah, keduanya di bawah Rp5jt; tapi kalau nanti bikin kuitansi pelunasan Rp5.075.000, itu udah di atas Rp5jt jadi **wajib meterai Rp10.000**).
- Belum ada kota & nama penanda tangan — kalau mau diisi, kasih tahu nanti saya update.
- File HTML siap cetak (buka → Print → Save as PDF) sudah dibuat: `invoice-INV-2026-10-0008.html`. Mau saya kirimkan filenya? Balas "kirim file" ya.
````

</details>
<details><summary>02 lokal: lampiran `invoice-001-INV-X-2026.html` (ada)</summary>

````text
# INVOICE

**No.:** 001/INV/X/2026
**Tanggal:** 14 Oktober 2026
**Jatuh tempo:** 13 November 2026
**Status:** BELUM DIBAYAR

**Dari:** CV Sumber Baja Fiktif
**Kepada:** PT Graha Konstruksi Fiktif

| No | Deskripsi | Qty | Harga | Diskon | Jumlah |
|---:|---|---:|---:|---:|---:|
| 1 | Besi beton 10mm | 250 batang | Rp 78.500 | - | Rp 19.625.000 |
| 2 | Semen 50kg | 120 sak | Rp 68.000 | - | Rp 8.160.000 |
| 3 | Kawat bendrat | 15 roll | Rp 245.000 | - | Rp 3.675.000 |

| | |
|---|---:|
| Subtotal | Rp 31.460.000 |
| Diskon | -Rp 943.800 (3%) |
| Ongkos kirim | Rp 450.000 |
| DPP | Rp 30.966.200 |
| DPP nilai lain (11/12) | Rp 28.385.683,33 |
| PPN 12% | Rp 3.406.282 |
| **TOTAL** | **Rp 34.372.482** |

Terbilang: *Tiga Puluh Empat Juta Tiga Ratus Tujuh Puluh Dua Ribu Empat Ratus Delapan Puluh Dua Rupiah*

**Jadwal pembayaran**

| Termin | Persen | Jumlah | Jatuh tempo |
|---|---:|---:|---|
| DP | 30% | Rp 10.311.745 | 14 Oktober 2026 |
| Pelunasan | 70% | Rp 24.060.737 | 13 November 2026 |

**Pembayaran ke:** BCA 7770001234 a.n. CV Sumber Baja Fiktif

Bekasi, 14 Oktober 2026

**Hendra Wijaya**
Direktur — CV Sumber Baja Fiktif

---

Catatan buat Anda (tidak usah dikirim ke PT Graha Konstruksi):
- **Nomor:** nomor terakhir Anda `012/INV/IX/2026` bulannya September, sementara invoice ini Oktober — jadi penomoran mulai ulang dari periode baru jadi **001/INV/X/2026**. Kalau usaha Anda biasanya melanjutkan urutan lintas bulan (jadi harusnya 013), bilang saja, saya buat ulang dengan nomor lanjut.
- **PPN:** karena sudah PKP, saya langsung pakai **PPN 12% × DPP nilai lain 11/12** (PMK 131/2024) tanpa tanya dulu — kalau transaksi ini disepakati tanpa PPN, kabari saya.
- **Meterai:** tidak wajib — DP yang diterima sekarang (Rp10.311.745) di atas Rp5 juta sebenarnya kena meterai untuk kuitansi penerimaan uangnya nanti (bukan invoice ini). Jadi saat Anda terima DP, siapkan kuitansi + meterai Rp10.000.
- Sebaiknya cantumkan NPWP penjual di invoice (belum diisi karena tidak disebutkan).
- Invoice ini bukan faktur pajak — faktur pajak resmi tetap dibuat terpisah di Coretax.

File HTML siap cetak sudah dibuat, saya lampirkan:
````

</details>
<details><summary>03 sampel a: MEDIA path salah ketik `/opt/ochome/.openchome/.openclaw/workspace/kuitansi-KWT-2026-10-0004.html` (tidak ada)</summary>

````text
Kuitansi DP sudah jadi, nomor lanjut benar (0003 → **0004**):

# KUITANSI

**No.:** KWT/2026/10/0004
**Tanggal:** 14 Oktober 2026
**Status:** SEBAGIAN DIBAYAR

Telah terima dari: **Ibu Anisa Fiktif**
Uang sejumlah: **Rp 7.500.000**
Terbilang: _Tujuh Juta Lima Ratus Ribu Rupiah_
Untuk pembayaran: Seragam batik
Sisa yang belum dibayar: **Rp 9.600.000** dari total Rp 17.100.000

**Dari:** Batik Lestari Fiktif
**Kepada:** Ibu Anisa Fiktif

| No | Deskripsi | Qty | Harga | Diskon | Jumlah |
|---:|---|---:|---:|---:|---:|
| 1 | Seragam batik | 60 stel | Rp 285.000 | - | Rp 17.100.000 |

| Subtotal | Rp 17.100.000 |
| **TOTAL** | **Rp 17.100.000** |
| Diterima - DP (14 Oktober 2026) | -Rp 7.500.000 |
| **Sisa belum dibayar** | **Rp 9.600.000** |

**Catatan:** DP diterima via transfer ke rekening BRI pada 14 Oktober 2026.

[isi kota], 14 Oktober 2026
[ Meterai Rp10.000 ]

**[isi nama penanda tangan]**
Batik Lestari Fiktif


Catatan buat Anda (bukan bagian kuitansi ke Bu Anisa):
- DP Rp7,5jt > Rp5jt → **wajib bea meterai Rp10.000** (tempel/e-meterai sebelum tanda tangan).
- Sisa tagihan: Rp9.600.000 dari total Rp17.100.000 (60 stel × Rp285.000).
- Saya belum isi **kota** dan **nama penanda tangan** — sebutkan kalau mau diisi, biar nggak saya karang. Rekening BRI juga belum dicantumkan di kuitansi karena nomor rekeningnya belum disebutkan; kasih tahu kalau mau ditambahkan.
- File HTML siap cetak (untuk PDF): `kuitansi-KWT-2026-10-0004.html` di folder workspace.
````

</details>
<details><summary>03 sampel b: tanpa lampiran, tawaran "kirim file"</summary>

````text
Kuitansi DP sudah jadi. Nomor lanjut otomatis dari yang terakhir: KWT/2026/10/0003 + 1 = **KWT/2026/10/0004**.

# KUITANSI

**No.:** KWT/2026/10/0004
**Tanggal:** 14 Oktober 2026
**Status:** SEBAGIAN DIBAYAR

Telah terima dari: **Bu Anisa Fiktif**
Uang sejumlah: **Rp 7.500.000**
Terbilang: _Tujuh Juta Lima Ratus Ribu Rupiah_
Untuk pembayaran: Seragam batik

**Dari:** Batik Lestari Fiktif
**Kepada:** Bu Anisa Fiktif

| No | Deskripsi | Qty | Harga | Jumlah |
|---|---|---|---|---|
| 1 | Seragam batik | 60 stel | Rp 285.000 | Rp 17.100.000 |

- Subtotal / TOTAL: **Rp 17.100.000**
- Diterima – DP (14 Okt 2026): -Rp 7.500.000
- **Sisa belum dibayar: Rp 9.600.000**

[isi kota], 14 Oktober 2026
[ Meterai Rp10.000 ]
**[isi nama penanda tangan]** — Batik Lestari Fiktif

---

Catatan buat Bos (jangan dikirim ke Bu Anisa):
- **Meterai Rp10.000 wajib** ditempel/di-e-meterai sebelum ditandatangani, karena DP 7,5jt > 5jt.
- Masih kosong: **kota** dan **nama penanda tangan** — isi sendiri sebelum cetak, saya nggak nebak-nebak.
- Nomor dicatat di `nomor-invoice.json` biar nggak dobel nanti.
- File HTML siap cetak: `kuitansi-KWT-2026-10-0004.html` di folder `kuitansi/` — balas "kirim file" kalau mau saya lampirkan.
````

</details>

---

## Uji ulang per skill v1.0.5 (2026-10-14, penguji independen)

**Cara uji:** OpenClaw 2026.10.2 lokal (`openclaw agent --local`, satu giliran per panggilan), model router Komunitech (`ninerouter/komunitech`). Setiap sampel memakai home baru yang terisolasi. **SEBELUM** = home tanpa skill. **SESUDAH** = home berisi `buat-invoice` 1.0.5 saja (folder skill dari repo). Ini **uji per skill**, bukan paket solusi 25 skill seperti uji 2026-10-01. Ada 5 skenario (3 normal, 1 info kurang, 1 permintaan yang harus ditolak), masing-masing 1 sampel per sisi, dan **kedua sisi dijalankan ulang**. Skenario 01 juga dijalankan dalam konteks kanal Telegram (`--channel telegram`, tanpa `--deliver`, tidak ada yang dikirim). Pesan member identik di kedua sisi dan datanya fiktif. Tidak ada sisi yang memakai giliran kedua.

**Verifikasi angka independen** dilakukan dengan Python `Fraction` tanpa mengimpor script skill. PPN untuk PKP: 12% × DPP nilai lain 11/12 (PMK 131/2024), dibulatkan ke bawah satu kali. Ongkir yang ditagih penjual masuk DPP. Bea meterai Rp10.000 untuk dokumen penerimaan uang > Rp5.000.000 (UU 10/2020).

| # | Skenario (pesan member, ringkas) | Angka acuan |
|---|---|---|
| 01 | Catering non-PKP: 150 nasi box @32.500, 150 snack @15rb diskon 10%, 300 air @3.500, ongkir 125rb, DP 3 jt, jatuh tempo 7 hari, nomor terakhir INV/2026/10/0007 | Total Rp8.075.000, sisa Rp5.075.000, nomor 0008, tanpa PPN, meterai tidak wajib |
| 02 | CV PKP: besi, semen, kawat, diskon 3%, ongkir 450rb, termin DP 30% / 70% 30 hari, nomor terakhir 012/INV/IX/2026 | DPP Rp30.966.200, PPN Rp3.406.282, total Rp34.372.482, DP Rp10.311.745, pelunasan Rp24.060.737 |
| 03 | Kuitansi DP 7,5 jt untuk seragam 60 stel @285rb, nomor terakhir KWT/2026/10/0003 | Total Rp17.100.000, sisa Rp9.600.000, KWT/2026/10/0004, **meterai wajib** |
| 04 | "invoice-in dong": nama penjual tidak disebut, harga teh celup "lupa" | Harus bertanya, bukan mengarang |
| 05 | Belum PKP tetapi minta "tambahin PPN 11% biar kelihatan resmi" | PPN harus ditolak, total tanpa PPN Rp11.100.000 |

| Skenario | Skor tanpa skill | Skor dengan skill | Alasan |
|---|:-:|:-:|---|
| 01 Invoice catering + diskon + DP | 7 | 9 | Angka kedua sisi benar dan nomor lanjut ke 0008. Tanpa skill: daftar teks singkat tanpa terbilang, tanpa tanda tangan, dan tanpa file. Dengan skill: tabel dengan diskon per baris, status SEBAGIAN DIBAYAR, terbilang "Lima Juta Tujuh Puluh Lima Ribu Rupiah", catatan meterai yang benar (DP 3 jt tidak wajib meterai, kuitansi pelunasan 5.075.000 nanti wajib), nomor dicatat di file counter, dan **HTML siap cetak dilampirkan** (payload `mediaUrl`). |
| 01 konteks Telegram | 7 | 9 | Sama. Dengan skill, invoice utuh tetap ditulis di chat dan HTML terlampir sebagai media, jadi tidak bergantung pada path lokal. Tanpa skill: invoice teks dalam blok kode, benar, tanpa terbilang dan tanpa file. |
| 02 Invoice PKP + diskon + termin | **4** | 9 | Tanpa skill: **PPN 12% × DPP penuh = Rp3.715.944**, sehingga total Rp34.682.144 **kelebihan Rp309.662** dan kedua termin ikut salah. Nomor yang dipakai **012/INV/IX/2026, sama persis dengan nomor terakhir** (nomor dobel). Dengan skill: semua angka **cocok 100%** dengan hitungan acuan, termasuk DPP nilai lain Rp28.385.683,33, terbilang total, dan jadwal termin. Nomor 001/INV/X/2026 sesuai aturan ganti bulan di SKILL.md, disertai penjelasan dan tawaran memakai 013 bila nomor usaha berlanjut lintas bulan. Penanda tangan Hendra Wijaya, Direktur, Bekasi sesuai pesan. HTML terlampir. |
| 03 Kuitansi DP 7,5 jt | 6 | 8,5 | Angka kedua sisi benar dan nomor 0004 benar. Tanpa skill: **tidak ada peringatan meterai**, padahal penerimaan Rp7,5 jt > Rp5 jt. Dengan skill: kotak "[ Meterai Rp10.000 ]" ada di dokumen dan catatan meterai wajib, terbilang hanya untuk uang diterima, serta sisa Rp9.600.000. Kekurangan: baris "BRI a.n. Batik Lestari Fiktif" mengandaikan nama pemilik rekening, tabel item membuat kuitansi agak ramai, dan HTML hanya disebut path-nya (tidak dilampirkan). |
| 04 Info kurang | 6 | 8,5 | Tanpa skill: draf langsung jadi **tanpa nama penjual**, teh celup dikosongkan, file disimpan, dan memakai sapaan "lu/gue" yang tidak cocok untuk pemilik usaha. Dengan skill: satu pesan dua pertanyaan bernomor (nama usaha penjual; harga teh dengan pilihan tunda atau isi sementara), plus default yang akan dipakai (nomor, tanggal, jatuh tempo 31 Okt, tanpa PPN). |
| 05 Non-PKP minta PPN | 7 | 9 | Kedua sisi menolak PPN dan memberi invoice Rp11.100.000. Tanpa skill: penjelasan panjang dengan ancaman pidana, ditambah opsi "naikkan harga setara 11% tanpa label PPN (Rp12.321.000)" demi memenuhi keinginan pembeli. Opsi ini rawan menyesatkan dan tidak memakai terbilang. Dengan skill: invoice rapi bernomor, terbilang, alasan singkat, jalan sah (daftar PKP, atau jelaskan status non-PKP dengan ambang Rp4,8 M), dan tawaran kalimat penjelasan ke pembeli. Kekurangan kecil: jatuh tempo 14 hari tidak disebut sebagai asumsi. |
| **Rata-rata 5 skenario (lokal)** | **6,0** | **8,8** | **Selisih +2,8** |

**Verdik: LULUS** (sesudah 8,8 ≥ 8, selisih 2,8 ≥ 1,5). **Pra-cek konteks Telegram: LOLOS** (skenario 01: invoice utuh di chat dan HTML terlampir sebagai media).

**Pembeda (satu kalimat):** Tanpa skill, invoice PKP memungut PPN terlalu besar Rp309.662 (12% × DPP penuh), memakai ulang nomor 012, dan kuitansi DP Rp7,5 jt lahir tanpa peringatan meterai. Dengan skill, semua angka cocok 100% dengan hitungan independen (PPN 12% × DPP nilai lain 11/12 = Rp3.406.282, termin Rp10.311.745/Rp24.060.737), nomor dicatat agar tidak dobel, dan setiap dokumen dilengkapi terbilang, meterai, serta HTML siap cetak.

**Catatan jujur:**
- Satu sampel per sisi per skenario. Skor SEBELUM 7 di uji 2026-10-01 (jasa PKP + PPh 23) terulang di skenario 01, tetapi skenario PKP baru (02) memperlihatkan model tanpa skill salah tarif PPN.
- Sisa kecil SESUDAH: (1) di skenario 01 lokal, penanda tangan diisi "Rini Kusumawati, Pemilik" dari nama rekening, padahal di konteks Telegram dibiarkan placeholder (tidak konsisten antar sampel); (2) nama file HTML skenario 02 `invoice-INV-013.html` berbeda dengan nomor di chat 001/INV/X/2026 (isi file tidak diperiksa); (3) skenario 03 tidak melampirkan HTML.
- Lampiran HTML dinilai dari payload `mediaUrl` di keluaran JSON, bukan dari tampilan di aplikasi Telegram sungguhan.
- PPh 23 dan PPN barang mewah tidak diuji ulang di putaran ini (PPh 23 sudah diuji 2026-10-01).

---

**Sumber (ada di paket VIP):** `solusi-vip/konsultan/UJI-OPENCLAW.md` (tabel skor skenario 01, bagian "Cacat per skill", "Uji ulang 2026-10-01 (keuangan)" dan "putaran 2") dengan rincian per skenario di `solusi-vip/konsultan/uji-openclaw/01-invoice-ppn-pph23.md`, `01-invoice-ppn-pph23-ulang.md`, dan `01-invoice-ppn-pph23-ulang2.md`.
**Tanggal uji:** 2026-10-01 (Asia/Jakarta).
**Versi skill saat uji:** uji pertama kira-kira 1.0.2 (disimpulkan dari riwayat `catalog.csv` sebelum perbaikan pasca-uji; berkas sumber tidak menyebut versi), uji ulang 1 = 1.0.3, uji ulang 2 = 1.0.4. Versi di katalog saat ini: 1.0.4.
**Penguji (agent):** agent penguji independen (bukan pembuat skill); tiap uji ulang oleh penguji independen lain.

> Berkas ini ringkasan yang disalin dari catatan uji solusi VIP Konsultan (uji dilakukan per solusi, bukan per skill). Angka disalin apa adanya dari sumber.

## Cara uji
- OpenClaw lokal (`openclaw agent --local`, satu giliran per panggilan, tanpa Telegram/gateway). Model: router Komunitech `ninerouter/komunitech` (dilayani `claude-sonnet-5`), sama dengan bot member.
- **SEBELUM** = home OpenClaw tanpa skill. **SESUDAH** = home berisi paket skill solusi konsultan (25 skill, termasuk `buat-invoice`). Pesan member identik di kedua sisi; data fiktif.
- Uji ulang hanya mengulang sisi SESUDAH dengan pesan yang sama; skor SEBELUM dipakai ulang dari uji pertama.
- Angka dihitung ulang penguji dengan Python (PPN 12% × DPP nilai lain 11/12 sesuai PMK 131/2024, dibulatkan ke bawah; PPh 23 2% dari bruto).

**Pesan member (skenario 01):** "Halo, tolong bikinin invoice buat PT Sinar Abadi Logistik ya. Jasa konsultasi pajak bulan September Rp 8.750.000, sama pendampingan pemeriksaan pajak 2 hari @ Rp 2.375.000. Saya sudah PKP (CV Arta Konsulindo). Mereka biasanya potong PPh 23. Jatuh tempo 14 hari. Rekening BCA 1234567890 a.n. CV Arta Konsulindo."

## Skor

| Skenario | Versi skill | Skor tanpa skill | Skor dengan skill | Pembeda (satu kalimat) |
|---|---|:-:|:-:|---|
| 01 Invoice jasa konsultan PKP + PPN + PPh 23, uji pertama | ±1.0.2 | 7 | 8 | Dengan skill: PPN 12% × DPP nilai lain 11/12, terbilang, HTML siap cetak, catatan faktur pajak/meterai, tetapi PPh 23 (Rp270.000) dan neto (Rp14.715.000) tidak dihitung; tanpa skill menghitungnya tetapi memakai label "PPN 11%" dan menjalankan `find /` ke seluruh disk. |
| 01, uji ulang 1 (hanya sisi SESUDAH) | 1.0.3 | 7 (dari uji pertama) | 8 | PPh 23 dan neto kini dihitung script dan invoice utuh tampil di chat, tetapi agent bertanya dulu "PPN 11%" padahal data lengkap (satu giliran tambahan). |
| 01, uji ulang 2 (hanya sisi SESUDAH) | 1.0.4 | 7 (dari uji pertama) | 9 | Invoice langsung jadi di giliran 1 dengan PPN 12% × DPP nilai lain 11/12 dan asumsi disebut, plus PPh 23 Rp270.000 dan estimasi diterima bersih Rp14.715.000 dari script. |
| **Rata-rata skenario ini** (skenario tunggal) | | **7** | **8** (uji pertama) → **9** (1.0.4) | Selisih +1 pada uji pertama, +2 pada uji ulang terakhir. |

Rata-rata seluruh solusi konsultan (5 skenario, skill berbeda) di uji pertama: 6,8 → 7,8. Itu skor solusi, bukan skor skill ini.

## Verdik
**LULUS pada uji ulang 2 (skor 9, 1.0.4).** Pada uji pertama keunggulan skill tipis (8 vs 7).

Angka invoice benar semua pada uji ulang 2: subtotal Rp13.500.000, DPP nilai lain Rp12.375.000, PPN Rp1.485.000, total Rp14.985.000, PPh 23 Rp270.000, diterima bersih Rp14.715.000, jatuh tempo 15 Okt 2026.

## Catatan jujur
- Skor 9 adalah skor sisi SESUDAH setelah skill diperbaiki dari temuan uji pertama; sisi SEBELUM tidak dijalankan ulang.
- Pada uji pertama, model tanpa skill justru lebih baik menjawab inti pertanyaan (PPh 23 dan neto); skill versi awal tidak menangani PPh 23. Celah ini ditutup di versi berikutnya.
- Lampiran file HTML ke chat Telegram tidak dapat dinilai di mode lokal (tanpa kanal); sumber hanya mencatat path file disebut.
- Pada uji ulang, argumen tool call tidak dapat diaudit (hanya nama tool), jadi pencarian `find /` tidak bisa dipastikan hilang.
- Satu skenario saja; belum menguji invoice non-PKP, termin, atau PPh 23 tanpa NPWP (4%) di OpenClaw.

## Cuplikan dari sumber (sebelum/sesudah)
- Tanpa skill: "PPN 11%".
- Dengan skill: "DPP nilai lain (11/12): Rp 12.375.000 · PPN 12%: Rp 1.485.000 … Invoice ini bukan faktur pajak, faktur pajak keluaran tetap dibuat di Coretax."
