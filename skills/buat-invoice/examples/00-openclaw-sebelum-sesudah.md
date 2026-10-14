# Uji OpenClaw SEBELUM vs SESUDAH: buat-invoice

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
