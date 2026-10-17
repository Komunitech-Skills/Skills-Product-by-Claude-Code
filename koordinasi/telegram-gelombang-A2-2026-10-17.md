# Gelombang Telegram A2 — 2026-10-17 (bot pertama)

Uji di grup Telegram sungguhan, bot pertama, OpenClaw 2026.10.2. Bot uji `@KTclaude1_bot` (Akun A), dikirim oleh bot penguji kedua Akun A, 17 Okt 2026 04:22–04:30 UTC, topik baru 1924–1927. Ini kiriman ulang: kiriman pertama di topik yang sama (03:49–03:56 UTC) gagal karena router membalas HTTP 530 (lihat "Catatan router"). Pesan uji identik di sisi TANPA (topik dengan `skills: []`) dan DENGAN skill. Permintaan: `tender-checklist` 1.0.9 kedua sisi (baris "Untuk Akun A — uji ulang Telegram (Akun B, 2026-10-16 18:45 UTC)" di `koordinasi/papan-tugas.md`) dan `cek-risiko-dan-asuransi-usaha` 1.0.3 kedua sisi. Penilai independen (bukan pembuat skill), skala dan kriteria `koordinasi/alat-uji/brief/tester-umum.md` bagian "Penilaian". Semua angka kunci dihitung ulang dengan Decimal; rincian tender dihitung ulang dari `koordinasi/alat-uji/pilot/data/g22/rincian-atk.csv`. Bukti pengiriman dicocokkan ke log gateway (`gw-20261017-0349.log`). Pesan pengguna yang tampil dua kali dan jawaban ganda berturut yang identik di transkrip adalah salinan log dan hanya dihitung sekali.

Acuan: **LULUS** bila DENGAN ≥ 8 DAN selisih ≥ 1,5 DAN tanpa salah angka kunci (salah angka kunci = maks 5).

## Skor & verdik

| Skill | Versi | Topik (TANPA/DENGAN) | TANPA | DENGAN | Selisih | Verdik | Pembeda (bahasa awam) |
|---|---|---|---|---|---|---|---|
| tender-checklist | 1.0.9 | 1924 / 1925 | 6,0 | 8,5 | +2,5 | **LULUS** | Dengan skill, Anda langsung diberi tahu batas unggah sudah lewat, lalu tetap mendapat total penawaran lengkap dengan PPN (Rp44.142.480 = 23,86 % HPS), checklist dokumen yang bisa dicentang, daftar "awas gugur", dan pengingat potongan PPh 22 saat dibayar. Tanpa skill, PPN tidak dihitung dan Anda malah disuruh mengecek tarifnya sendiri. |
| cek-risiko-dan-asuransi-usaha | 1.0.3 | 1926 / 1927 | 7,0 | 8,0 | +1,0 | **BELUM** (selisih < 1,5) | Dengan skill, risiko kafe diurutkan dengan skor (banjir TINGGI 12 paling atas) dan kekurangan dana darurat dihitung pasti: kurang Rp39.400.000, atau menabung ±Rp6.566.667/bulan selama 6 bulan. Namun jawaban tanpa skill juga sudah benar hitungannya dan lebih tegas soal BPJS Ketenagakerjaan, jadi selisihnya kecil. |

Pembanding gelombang lama: tender-checklist G22 (16 Okt, bot kedua, 1.0.8) 5 → 7,5 BELUM (checklist dokumen tidak muncul, dasar aturan & PPh 22 hilang, jaminan rancu). Semua cacat G22 itu teratasi di 1.0.9. cek-risiko-dan-asuransi-usaha sudah pernah diuji di bot asli: gelombang 14 (12 Okt, bot kedua, versi 1.0.2 menurut riwayat CHANGELOG) 6,5 → 8,5 LULUS (`koordinasi/telegram-gelombang-14-2026-10-12.md`; koreksi Akun B 2026-10-17, kalimat awal laporan ini keliru menulis "belum pernah tampil di bot asli"). Uji internal (`examples/01-kafe-ruko-dekat-kali.md`) 6,5 → 8.

Catatan lintas skill:
- **Istilah proses yang tampil:** sisi TANPA tender membuka dengan "Saya sudah cek file `data/rincian-atk.csv`" dan menulis "akses pencarian web sedang nonaktif di sisi saya". Sisi DENGAN kedua skill bersih dari kata proses (tanpa skill/script/cek file).
- **Jalur berkas:** hanya di sisi TANPA tender (`data/rincian-atk.csv`, `rincian-atk.csv`). Sisi DENGAN tidak menyebut jalur.
- **Tabel Markdown mentah:** tidak ada di keempat jawaban. Tender DENGAN memakai kotak centang `- [ ]` / `[-]`, yang tampil sebagai teks biasa di Telegram (masih terbaca).
- **Jargon:** tender DENGAN memakai "LDK", "SPSE", "SIKaP", "TOTP", "DPP" tanpa penjelasan; cek-risiko TANPA memakai istilah Inggris ("flood extension", "business interruption", "public liability", "company-paid", "downtime", "worth it").
- **Terpotong:** tidak ada. Semua jawaban 1 bagian (`chunkCount=1`). cek-risiko DENGAN sengaja berhenti di 4 risiko dan menawarkan "Balas *lanjut*".

## Rincian per skill

### tender-checklist 1.0.9 — TANPA 6,0 → DENGAN 8,5 (+2,5) LULUS

**Bukti kirim:** topik 1925, pesan **1943** (04:26:58 UTC, `chunkCount=1`). TANPA: topik 1924, pesan **1940** (04:25:24 UTC).

**Angka kunci (dihitung ulang dari CSV g22):** 150 × 52.500 = 7.875.000; 24 × 1.250.000 = 30.000.000; 500 × 3.750 = 1.875.000; 1,5 × 12.000 = 18.000. DPP **Rp39.768.000**. PPN = 39.768.000 × 11/12 × 12 % = **Rp4.374.480** (pas, tanpa sisa pembulatan). Total **Rp44.142.480** = **23,86 %** dari HPS Rp185.000.000; ambang 80 % = Rp148.000.000. PPh 22 1,5 % × DPP = Rp596.520 (tidak disebut nominalnya, hanya tarifnya). Semua angka DENGAN benar; terbilang total juga benar.

Kutipan DENGAN (pesan 1943):
> Batas unggah **sudah lewat** — 14 Oktober 2026 pukul 15.00, sementara hari ini sudah 17 Oktober. … Bagian lain tetap saya lengkapi untuk persiapan tender berikutnya atau bila jadwalnya diperpanjang.
> **1. Kelayakan: IKUT DENGAN SYARAT** …
> - Subtotal (DPP): **Rp39.768.000**. PPN 11% efektif: **Rp4.374.480**. **Total: Rp44.142.480** …
> - Ini **23,86% dari HPS Rp185.000.000** — jauh di bawah batas 80% HPS (Rp148.000.000). …
> - Jaminan penawaran: tidak disyaratkan (barang, bukan konstruksi/terintegrasi).
> - Jaminan pelaksanaan: kontrak s.d. Rp200 juta umumnya tidak diwajibkan — cek dokumen pemilihan.
> - Saat dibayar nanti: bendahara memungut PPN dan memotong PPh Pasal 22 1,5% dari harga tanpa PPN …
> **3. Checklist dokumen (tender pascakualifikasi, barang)** …

**Alasan skor DENGAN 8,5:**
- (+) Semua kunci terpenuhi: tenggat lewat disebut di kalimat pertama DAN checklist dokumen tetap muncul (administrasi, teknis, harga); angka DPP/PPN/total/persen HPS benar; jaminan penawaran "tidak disyaratkan", jaminan pelaksanaan dikaitkan ke batas Rp200 jt; baris dasar aturan bertanggal + "Bukan nasihat hukum/pajak"; pengingat PPN dipungut & PPh 22 dipotong bendahara beserta dampaknya ke arus kas.
- (+) Peringatan tepat bahwa total 23,86 % HPS berisiko dianggap tidak wajar dan perlu bukti harga pemasok; daftar "Awas gugur" 7 butir praktis.
- (−) Asumsi "HPS belum termasuk PPN" di akhir tidak konsisten dengan perbandingan total-termasuk-PPN terhadap HPS (dan HPS lazimnya sudah termasuk PPN). Tidak mengubah verdik karena perbandingan yang dipakai benar.
- (−) Jargon tanpa penjelasan: LDK, SPSE, SIKaP, TOTP, DPP.
- (−) Harga tinta Rp1,25 jt/botol dan paper clip 1,5 lusin tidak dipertanyakan (sisi TANPA justru menangkapnya). Bukti setor pajak/SPT tidak muncul eksplisit di checklist.

**Alasan skor TANPA 6,0:** Tenggat lewat juga disebut di awal, kelayakan usaha kecil benar, dan daftar dokumen cukup lengkap; DPP Rp39.768.000 benar dan dua kejanggalan data (tinta, paper clip) ditangkap. Namun PPN tidak dihitung ("jangan asumsikan 11% begitu saja"), total dan persen HPS tidak ada, jaminan tidak dibahas, tidak ada dasar aturan/penafian dan tidak ada pengingat PPh 22. Ada kata proses dan jalur berkas, serta istilah "before-tax". Sedikit lebih baik dari G22 (5) karena checklist dokumen muncul.

### cek-risiko-dan-asuransi-usaha 1.0.3 — TANPA 7,0 → DENGAN 8,0 (+1,0) BELUM

**Bukti kirim:** topik 1927, pesan **1948** (04:30:13 UTC, `chunkCount=1`). TANPA: topik 1926, pesan **1945** (04:28:13 UTC, `text delivery ok`).

**Angka kunci (dihitung ulang):** biaya tetap 4.500.000 + 3 × 2.800.000 + 1.700.000 + 1.200.000 = **15.800.000**; target 3 bulan **47.400.000**; kekurangan dari kas 8 jt **39.400.000**; 8 / 15,8 = 0,51 bulan; cicilan 6 bulan 6.566.666,67 → ±Rp6.566.667. Sisi TANPA: 6 × 15,8 jt = 94,8 jt (ditulis "95jt", wajar), iuran JKK+JKM 0,54 % × 2,8 jt = Rp15.120 ("~15rb", benar). Kedua sisi tanpa salah angka; tidak ada rekomendasi merek/produk asuransi dan tidak ada klaim pasti cair.

Kutipan DENGAN (pesan 1948):
> **3 prioritas teratas:**
> 1. Banjir (dekat kali, pernah 2020) · TINGGI (skor 12)
> 2. Kebakaran/korsleting listrik · SEDANG (skor 8)
> 3. Bergantung pada satu barista/koki kunci · SEDANG (skor 6)
> **Dana darurat:**
> - Biaya tetap per bulan: Rp15.800.000 (sewa 4,5jt + gaji 3x2,8jt + listrik/gas 1,7jt + cicilan mesin 1,2jt)
> - Target (3 bulan): Rp47.400.000
> - Kas sekarang: Rp8.000.000 → baru cukup 0,5 bulan, kurang Rp39.400.000
> - Kalau mau dicicil 6 bulan: nabung ±Rp6.566.667/bulan
> …
> - Sikap: Kurangi dulu (naikkan barang) + alihkan ke asuransi kebakaran/properti dengan perluasan banjir (cek per polis — tidak otomatis termasuk)
> …
> Ini bukan nasihat asuransi/keuangan resmi, hanya pemetaan awam.

**Alasan skor DENGAN 8,0:**
- (+) Angka kunci lengkap dan benar, termasuk kekurangan dan cicilan menabung; risiko berskor dan berprioritas; tiap risiko punya langkah murah konkret dan "sikap" (kurangi/alihkan); perluasan banjir "tidak otomatis termasuk, cek per polis"; penafian ada.
- (−) BPJS Ketenagakerjaan baru muncul di butir 4 dan ditulis berhati-hati ("kewajiban pemberi kerja bertahap sesuai skala usaha, perlu dicek"), padahal ini kewajiban yang paling jelas dan murah. Sisi TANPA lebih tegas dan menghitung iurannya.
- (−) Hanya 4 risiko yang dirinci; perlindungan gangguan usaha dan tanggung gugat pelanggan (relevan untuk F&B) tidak muncul di pesan ini, tertahan di balik "Balas *lanjut*". Tidak ada pertanyaan penutup.
- (−) Dampak "setara ~1 bulan biaya tetap" untuk barista kunci adalah perkiraan tanpa label asumsi.

**Alasan skor TANPA 7,0:** Biaya tetap Rp15,8 jt, rentang dana darurat Rp47,4–95 jt, dan "kas cuma cukup ±2 minggu" semuanya benar. Saran BPJS TK tegas dengan iuran terhitung, empat jenis perlindungan relevan (termasuk gangguan usaha dan tanggung gugat), urutan prioritas jelas, dan mitigasi murah "pindahkan ke lantai 2". Kekurangannya: kekurangan dana Rp39,4 jt tidak dihitung, tidak ada skor/urutan risiko di luar asuransi (kebakaran, ketergantungan orang), saran "incer 70–95jt" terasa berat untuk kas 8 jt, banyak istilah Inggris, dan tanpa penafian.

**Perbaikan paling berdampak (BELUM):**
1. Angkat BPJS Ketenagakerjaan (JKK + JKM minimal) ke 3 prioritas teratas bila karyawan belum terdaftar, dengan kalimat tegas dan perkiraan iuran per orang dihitung dari gaji.
2. Tampilkan semua risiko penting dalam satu pesan (ringkas per risiko) atau setidaknya sebut perlindungan gangguan usaha dan tanggung gugat pelanggan untuk usaha makanan/minuman sebelum "Balas lanjut".
3. Beri label "perkiraan" pada dampak yang tidak berasal dari pengguna, dan tutup dengan maks. 3 pertanyaan yang benar-benar mengubah hasil (mis. tinggi lantai dasar, nilai peralatan).
4. Untuk uji berikutnya pilih kasus yang lebih sulit bagi model dasar (mis. banyak risiko dengan data kurang lengkap atau biaya tetap campur harian/bulanan) agar nilai tambah skor & hitungan terukur.

## Catatan router

- Kiriman pertama 03:49–03:56 UTC (10:49–10:56 WIB) di topik 1924–1927: router `ninerouter/komunitech` membalas **HTTP 530** (Cloudflare) berulang, `model fallback decision … next=none`; bot hanya mengirim pesan galat "Couldn't reach the AI service" (pesan 1929, 1931, 1933, 1936). Pesan galat itu tidak dinilai.
- Kiriman ulang 04:22–04:30 UTC (11:22–11:30 WIB) di topik yang sama: semua panggilan model `status=200`; jawaban terkirim di pesan 1940, 1943, 1945, 1948. Konteks sesi topik tidak berisi jawaban lama yang berhasil (run pertama gagal total), jadi kiriman ulang dinilai sebagai jawaban pertama.
