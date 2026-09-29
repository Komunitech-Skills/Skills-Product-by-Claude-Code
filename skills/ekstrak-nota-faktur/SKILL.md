---
name: ekstrak-nota-faktur
description: Membaca foto/teks nota, struk, kuitansi, invoice, dan faktur pajak Coretax yang diberikan pengguna menjadi tabel rapi, CSV siap tempel ke Excel, dan JSON; mengecek hitungan item, subtotal, PPN 12% DPP nilai lain 11/12, total, terbilang, format NPWP/NITKU/nomor seri faktur, lalu merekap banyak nota jadi rekap pengeluaran. Gunakan saat pengguna bilang "ketik ulang nota ini", "cek faktur pajak", "rekap nota belanja", "input struk ke Excel", atau receipt/invoice OCR, extract invoice data, expense recap. Membuat tagihan baru pakai buat-invoice; hitung PPN saja pakai hitung-ppn.
---

# Ekstrak Nota & Faktur

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Mengubah tumpukan nota, struk, kuitansi, invoice, dan faktur pajak (foto atau teks) menjadi data rapi yang sudah dicek angkanya: tabel ringkas, CSV siap tempel ke Excel/Google Sheets, JSON, dan rekap pengeluaran. Kolom yang tidak terbaca ditandai, **tidak ditebak**.

## Kapan digunakan
- "Tolong ketik ulang nota-nota ini ke Excel" / "input struk belanja bulan ini".
- "Cek faktur pajak dari supplier ini, PPN-nya benar nggak?"
- "Rekap pengeluaran dari 12 foto nota ini per kategori."
- "Ambil NPWP, DPP, PPN dari faktur ini" / "extract this invoice to JSON".

## Kapan TIDAK digunakan
- Membuat invoice/kuitansi baru → skill `buat-invoice`.
- Hanya menghitung PPN dari satu harga → skill `hitung-ppn`.
- Mencocokkan mutasi rekening dengan catatan → skill `rekonsiliasi-bank`.
- Rekap **penjualan** dari file kasir → skill `rekap-penjualan-csv`.
- Menyusun laporan keuangan → skill `laporan-keuangan-emkm` (hasil rekap skill ini bisa jadi bahannya).
- Memastikan faktur pajak asli/sah, mengkreditkan PPN masukan, atau lapor SPT → arahkan ke Coretax/DJP (Kring Pajak 1500200) atau konsultan pajak.
- **Bila skill rujukan di atas tidak terpasang:** jangan menolak. Untuk hitung PPN satu harga, pakai rumus di bagian "Rumus cek" (non-mewah: PPN = 11% × harga, bulatkan ke bawah; mewah: 12%) dan tulis langkahnya. Untuk tugas lain (membuat invoice, rekonsiliasi, laporan keuangan), jelaskan singkat bahwa itu di luar skill ini dan tawarkan hasil ekstraksi/CSV sebagai bahan awalnya.

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Foto/teks/PDF dokumen (satu atau banyak), **atau** angka yang diketik pengguna | Ya | — (minta dikirim) |
| Kategori pengeluaran tiap dokumen | Tidak | Ditebak dari isi (Bahan baku, Operasional, Jasa, …) dan disebut sebagai asumsi |
| Barang/jasa biasa atau barang mewah | Tidak | Biasa (non-mewah) |
| Pemisah CSV | Tidak | `;` (Excel berbahasa Indonesia). `,` untuk Google Sheets/Excel Inggris; `tab` untuk tempel langsung |
| Output yang diinginkan | Tidak | Tabel ringkas + hasil cek + CSV. JSON bila diminta atau pengguna teknis |

Bila pengguna hanya **mengetik angka** tanpa foto (mis. "DPP 10 juta, PPN 1,2 juta, total 11,2 juta, benar?"), langsung isi JSON dari angka itu, isi yang tidak disebut dengan `null`, jalankan cek, dan sebutkan bahwa cek hanya berdasarkan angka yang diketik (bukan dokumen).

Jika dokumen belum dikirim atau tidak bisa dibuka, tanyakan **sekali** dalam satu pesan bernomor (maks. 5 pertanyaan). Jangan bertanya hal yang ada defaultnya.

## Langkah kerja
1. **Baca tiap dokumen** dan isi data mengikuti `references/skema-data.md` (contoh lengkap: `templates/contoh-input.json`). Aturan membaca:
   - Salin angka, nomor, NPWP, dan terbilang **persis** seperti tertulis.
   - Kolom yang tidak ada di dokumen → `null`. Kolom yang ada tapi buram/terpotong → `"TIDAK_TERBACA"`, lalu tulis bagian yang terlihat di `catatan` (mis. "total terlihat 3?1.500"). **Jangan menebak digit, jangan mengarang item.**
   - Penjual = yang menerima uang ("Pengusaha Kena Pajak" di faktur). Pembeli = pengguna/usahanya.
   - Struk kasir yang mencetak DPP & PPN di bawah total → `"harga_termasuk_ppn": true`.
   - Bukti transfer atas nota yang juga dikirim → biarkan `jenis: "bukti_transfer"` (otomatis tidak dihitung dobel).
   - Invoice: salin juga `jatuh_tempo` dan `rekening_tujuan` bila ada (berguna untuk jadwal bayar dan mewaspadai modus "ganti rekening").
2. **Simpan** data ke file JSON sementara (mis. `nota.json`) di folder kerja pengguna.
3. **Jalankan cek angka & format** (path relatif terhadap folder SKILL.md ini; Windows: ganti `python3` dengan `python` atau `py`):
   ```bash
   python3 <folder-skill-ini>/scripts/cek_nota.py nota.json
   ```
   - CSV per dokumen: `--format csv --pemisah ";"` (atau `","`, `tab`); CSV per item: `--csv item`; simpan ke file: `--output rekap-nota.csv` (UTF-8 dengan BOM, rapi di Excel).
   - JSON lengkap berisi hasil cek & rekap: `--format json`.
   - Terbilang untuk satu angka: `--terbilang "1.250.000"`.
   - Kode keluar: `0` = semua dokumen dicek; `1` = sebagian dokumen **INPUT TIDAK VALID** (dilewati, dokumen lain tetap dicek & direkap, pesan per dokumen); `2` = file/argumen rusak, tidak ada yang dicek.
4. **Tulis hasil** dengan format di bawah. Pakai status, selisih, `ppn_seharusnya`, `total_seharusnya`, dan rekap dari script **apa adanya** (jangan menghitung sendiri). Terjemahkan hasil cek ke bahasa sehari-hari.
   - Angka yang tidak tertulis di dokumen tapi dihitung script (`subtotal_dihitung`, `dpp_dihitung`, total faktur "(dihitung)") selalu disebut "dihitung", tidak pernah disajikan sebagai angka dokumen.
   - Info "Ada PPN tapi NPWP penjual tidak tercantum" **abaikan** bila data berasal dari ketikan pengguna, bukan dari dokumen.
5. Bila ada `ADA SELISIH`, `ADA YANG TIDAK TERBACA`, atau `INPUT TIDAK VALID`, sebutkan apa yang perlu dicek pengguna di dokumen asli (atau minta foto ulang yang lebih jelas).
6. **Fallback tanpa Python:** hitung manual dengan rumus di bawah, tulis tiap langkah, dan beri tahu pengguna bahwa hasil dihitung manual.
7. Periksa checklist sebelum mengirim.

## Rumus cek (untuk hitung manual)
Dasar: UU HPP & PMK 131/2024, berlaku per 23 September 2026. Detail & sumber: `references/regulasi.md`.
- **Per item:** qty × harga satuan − diskon item = jumlah (toleransi ±Rp1).
- **Subtotal:** jumlah semua item = subtotal (toleransi ±Rp1 per baris).
- **PPN barang/jasa biasa, tanggal ≥ 1 Jan 2025:** DPP nilai lain = 11/12 × DPP; PPN = 12% × DPP nilai lain = **11% × DPP**, dibulatkan ke bawah ke rupiah penuh (toleransi ±Rp1).
- **PPN barang mewah (sejak 1 Feb 2025):** 12% × DPP.
- **Dokumen lama:** 1 Apr 2022–31 Des 2024 → 11% × DPP; sebelum 1 Apr 2022 → 10% × DPP.
- **Harga sudah termasuk PPN:** DPP ≈ harga × 100/111; DPP + PPN = harga (toleransi ±Rp2).
- **Total:** (subtotal − diskon) + PPN + PPnBM + biaya lain − potongan lain. Juga cocok bila PPh sudah dipotong (− PPh) atau meterai ditagihkan (+ Rp10.000).
- **Terbilang:** baca kalimat terbilang jadi angka, harus sama persis dengan total.
- Contoh: DPP Rp 4.500.000 → DPP nilai lain Rp 4.125.000 → PPN 12% = Rp 495.000 (= 11% × 4.500.000).

- **Uji regresi script:** `python3 <folder-skill-ini>/scripts/test_cek_nota.py`.

**Peringatan penting:** PPN = 12% × DPP penuh untuk barang/jasa **biasa** adalah kekeliruan yang sering terjadi sejak 2025 (lebih bayar 1% dari DPP). Laporkan sebagai "perlu ditanyakan ke penjual", bukan tuduhan.

**Format identitas (BELUM TERVERIFIKASI dari dokumen primer, hanya peringatan):** NPWP 16 digit (15 digit = format lama; wajar untuk dokumen sebelum 2025), NITKU 22 digit (16 digit NPWP + 6 digit), nomor seri faktur Coretax 17 digit (2 kode transaksi + 2 kode status + 13 nomor seri). Panjang berbeda → "perlu dicek ulang". **Jangan pernah menolak dokumen atau menyebutnya palsu karena panjang digit.**

## Format output
````
**Hasil baca & cek <n> dokumen**

| # | Tanggal | Penjual | Jenis | Total | Status |
|---|---|---|---|---|---|
| N1 | 02-09-2026 | Toko Sembako Bu Yati | Nota | TIDAK TERBACA | ⚠️ Ada yang tidak terbaca |
| F1 | 10-09-2026 | PT Kemasan Prima Nusantara | Faktur pajak | Rp 4.995.000 | ✅ Cocok |

**Yang perlu Anda cek**
- N1: jumlah telur dan total tidak terbaca (terlihat "3?1.500"). Mohon cek nota aslinya atau kirim foto ulang.
- I1: PPN ditulis 12% penuh (Rp 960.000). Untuk jasa biasa seharusnya Rp 880.000. Tanyakan ke penjual sebelum membayar.

**Rekap pengeluaran** (bila > 1 dokumen)
Total: Rp ... · PPN tercantum: Rp ... · per kategori / per penjual / per bulan (tabel)
Belum masuk total: <id dokumen yang totalnya tidak terbaca>

**CSV (siap tempel ke Excel, pemisah ;)**
```csv
<keluaran script --format csv>
```
<JSON bila diminta>

_Dasar PPN: UU HPP & PMK 131/2024, per 23 September 2026. Format NPWP/NITKU/nomor faktur: belum terverifikasi dari dokumen resmi, hanya peringatan. Alat bantu cek, bukan nasihat pajak; untuk kepastian hubungi DJP (Kring Pajak 1500200) atau konsultan pajak._
````
- Tabel untuk dibaca; CSV untuk disalin. Tanggal di tabel `DD-MM-YYYY`, di CSV/JSON `YYYY-MM-DD`.
- Kolom CSV Subtotal/DPP/PPN/Total = angka **dokumen** saja. Hasil script ada di kolom terpisah: Subtotal/DPP Dihitung Script, PPN Seharusnya, Total Seharusnya, Total Untuk Rekap. Kolom tak terbaca berisi `TIDAK_TERBACA`.
- Angka di CSV tanpa titik ribuan (agar Excel membacanya sebagai angka). NPWP/nomor murni angka ditulis `="0012…"` agar angka 0 di depan tidak hilang di Excel (`--id-polos` untuk mematikan).
- Cara tempel: simpan CSV sebagai file `.csv` lalu buka di Excel, atau pakai `--pemisah tab` lalu tempel langsung ke sel A1.

## Contoh
**Input pengguna:** (foto invoice) "Tolong cek invoice jasa website ini, terus masukin ke tabel."

Isi dokumen: jasa website Rp 8.000.000, PPN 12% Rp 960.000, PPh 23 dipotong Rp 160.000, total Rp 8.800.000, NPWP penjual 01.234.567.8-901.234, terbilang "Delapan juta delapan ratus ribu rupiah".

**Output (ringkas):**
```
| # | Tanggal | Penjual | Jenis | Total | Status |
|---|---|---|---|---|---|
| I1 | 12-09-2026 | PT Solusi Digital Kreatif | Invoice | Rp 8.800.000 | ⚠️ Perlu dicek |

Yang perlu Anda cek
- PPN Rp 960.000 dihitung 12% dari harga penuh. Untuk jasa biasa sejak 2025 seharusnya
  12% × 11/12 × Rp 8.000.000 = Rp 880.000. Selisih Rp 80.000 — tanyakan ke penjual.
- NPWP penjual masih format lama 15 digit. Minta NPWP 16 digit bila Anda butuh faktur pajaknya.
- Total Rp 8.800.000 cocok (sudah dipotong PPh 23 Rp 160.000; PPh ini wajib Anda setor ke negara).
- Terbilang cocok.

CSV:
No;ID;Tanggal;Jenis;Nomor Dokumen;Penjual;NPWP Penjual;...;PPN;PPh;Biaya Lain;Total;...
1;I1;2026-09-12;invoice;INV/2026/09/015;PT Solusi Digital Kreatif;01.234.567.8-901.234;...;960000;160000;;8800000;...
```

## Checklist sebelum mengirim hasil
- [ ] Setiap angka berasal dari dokumen; tidak ada digit yang ditebak. Kolom buram = TIDAK TERBACA.
- [ ] Status & selisih diambil dari script (atau ditandai "dihitung manual").
- [ ] PPN non-mewah diuji dengan 11/12; PPN 12% penuh pada barang biasa diberi peringatan, bukan tuduhan.
- [ ] Format NPWP/NITKU/nomor faktur hanya peringatan; tidak ada kata "palsu"/"tidak sah".
- [ ] Rekap menyebut dokumen yang belum masuk total dan dokumen yang kemungkinan dobel.
- [ ] CSV memakai pemisah yang diminta; Rupiah di teks `Rp 1.250.000`.
- [ ] Disclaimer + tanggal berlaku ada. Data pengguna tidak dikirim ke mana pun.

## Batasan & penanganan error
- Satu dokumen dengan angka/tanggal tidak valid (mis. format Inggris `1,250,000.00`, tanggal 31/02) diberi status `INPUT TIDAK VALID` beserta alasannya; dokumen lain tetap diproses (kode keluar 1). JSON rusak atau file tidak ada → `ERROR: ...` kode 2. Perbaiki data (bukan menebak), lalu jalankan ulang.
- Foto terlalu buram/terpotong untuk dibaca sama sekali → minta foto ulang: tegak, terang, seluruh kertas masuk bingkai.
- Tulisan tangan sulit dibaca → isi yang pasti saja, sisanya TIDAK_TERBACA; sarankan pengguna mengetik angka yang ragu.
- PPN dengan DPP/besaran khusus (kendaraan bekas, emas, pulsa), PPnBM, fasilitas dibebaskan/DTP → tidak dihitung ulang; ikuti dokumen dan arahkan ke DJP/konsultan.
- Skill tidak bisa memastikan keaslian faktur (cek lewat Coretax/QR code resmi) dan tidak memutuskan PPN bisa dikreditkan.
- Dokumen berisi data pribadi (nama, NIK, rekening): proses hanya untuk keperluan pengguna, jangan disebarkan.
