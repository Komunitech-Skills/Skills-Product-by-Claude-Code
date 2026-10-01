---
name: buat-invoice
description: Membuat invoice/tagihan atau kuitansi profesional berbahasa Indonesia dengan nomor otomatis, daftar item, diskon, ongkir, PPN opsional khusus PKP (DPP nilai lain 11/12), DP/termin, sisa tagihan, terbilang, rekening, jatuh tempo, dan penanda bea meterai Rp10.000 bila penerimaan uang di atas Rp5 juta; output Markdown rapi plus HTML siap cetak. Gunakan saat pengguna minta "buatkan invoice", "nota tagihan", "kuitansi DP/lunas", atau invoice generator, receipt, billing. Menagih ulang piutang pakai tagih-piutang; penawaran harga pakai surat-penawaran-harga.
---

# Buat Invoice & Kuitansi

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Menghasilkan invoice atau kuitansi yang rapi, angkanya pasti benar (dihitung script), dan siap dikirim lewat WhatsApp/email atau dicetak — tanpa aplikasi akuntansi.

## Kapan digunakan
- "Buatkan invoice untuk PT X: 100 kaos @65 ribu, diskon 5%, ongkir 75 ribu, DP sudah 3 juta."
- "Buat kuitansi pelunasan Rp7.500.000 untuk Bu Sari."
- Invoice dengan termin (DP 30% – termin 30% – pelunasan 40%).
- Invoice ber-PPN untuk penjual PKP.

## Kapan TIDAK digunakan
- Mengingatkan/menagih pelanggan yang telat bayar → skill `tagih-piutang`.
- Penawaran harga sebelum deal → skill `surat-penawaran-harga`.
- Faktur pajak resmi → dibuat di Coretax; invoice ini bukan faktur pajak.
- Hanya ingin tahu PPN suatu harga → skill `hitung-ppn`.

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Nama penjual (usaha) | Ya | — (tanyakan) |
| Nama pembeli | Ya | — (tanyakan) |
| Item: nama, jumlah, harga satuan (+ diskon per item) | Ya | — (tanyakan) |
| Jenis dokumen: invoice atau kuitansi | Tidak | Invoice |
| Nomor terakhir / nomor yang diinginkan | Tidak | `INV/<tahun>/<bulan>/0001` + pengingat |
| Kota & nama penanda tangan | Tidak | `[isi kota]`, `[isi nama penanda tangan]` — **jangan dikarang** |
| Tanggal & jatuh tempo | Tidak | Hari ini; jatuh tempo 14 hari |
| Diskon total, ongkir | Tidak | 0 |
| PPN (hanya jika penjual PKP) + jenis (umum/mewah) | Tidak | Tanpa PPN |
| Pembeli memotong PPh 23 (klien badan/PT/CV membayar **jasa**) | Tidak | Bila pengguna menyebut "dipotong PPh 23" atau klien badan untuk jasa: **aktifkan** `"pph23": true` (2% dari nilai jasa tanpa PPN; tanpa NPWP 4%) dan sebut asumsinya |
| DP/pembayaran yang sudah diterima, termin | Tidak | Belum ada |
| Rekening, alamat/kontak, NPWP, catatan, jabatan | Tidak | Dikosongkan |

Jika info wajib kurang, tanyakan **sekali** dalam satu pesan bernomor (maks. 5 pertanyaan). Jika pengguna minta PPN, pastikan ia **PKP**; jika tidak, jelaskan bahwa PPN tidak boleh dicantumkan.

**Jangan mengarang data.** Kota, nama penanda tangan, alamat, rekening, NPWP hanya diisi bila pengguna menyebutnya. Bila tidak, biarkan kosong di JSON: script menulis `[isi kota]` / `[isi nama penanda tangan]` dan baris "PERLU DIISI" — sampaikan ke pengguna.

**Penomoran (wajib persis):** salin nomor terakhir **huruf demi huruf** dari pesan pengguna ke `--nomor-terakhir` (jangan dikurangi/ditebak). Nomor baru = nomor terakhir **+ 1** (`INV/2026/09/0012` → `INV/2026/09/0013`). Cocokkan baris `Nomor terakhir dibaca: X -> nomor baru: Y` di output script dengan pesan pengguna sebelum menampilkan invoice.
- Bulan/tahun dokumen berganti dari nomor terakhir → script mengganti periode dan mulai lagi dari `0001` (`INV/2026/09/0012` + tanggal Oktober → `INV/2026/10/0001`). Jika usaha pengguna melanjutkan nomor lintas bulan, tambah `--urut-lanjut` (→ `INV/2026/10/0013`). Bila tidak jelas, sebutkan aturan yang dipakai.
- Format lain dikenali: `012/INV/IX/2026` (bulan Romawi, urut di depan), `INV-2026-0012` (nomor tahunan).
- Tanggal dokumen lebih lama dari periode nomor terakhir → script menolak (nomor mundur); tanyakan ke pengguna.

## Langkah kerja
1. Susun data ke file JSON di folder kerja pengguna mengikuti `templates/contoh-invoice.json` (penjelasan kolom: `references/format-input.md`).
   - PPh 23: `"pph23": true` (default 2% × subtotal setelah diskon, tanpa PPN & ongkir) atau `{"tanpa_npwp": true}` (4%) / `{"dasar": "<nilai jasa saja>"}` bila invoice juga berisi barang. Ini **info** "estimasi diterima bersih"; total tagihan tidak berubah. Penjual PPh final 0,5% yang sudah memberi Surat Keterangan PP 55 ke klien → jangan diaktifkan.
2. Jalankan script. Script ada di subfolder `scripts/` di folder yang sama dengan SKILL.md ini (folder skill); jalankan dari sana, jangan mencari ke seluruh disk (`find /`). Windows: `python` atau `py`:
   ```bash
   python3 <folder-skill-ini>/scripts/buat_invoice.py --file invoice.json --html invoice-INV-0008.html --nomor-terakhir INV/2026/09/0007
   ```
   - `--nomor-terakhir` → nomor terakhir + 1 (aturan ganti bulan/tahun di atas; `--urut-lanjut` bila nomor tidak di-reset).
   - `--counter-file nomor-invoice.json` → nomor urut per bulan disimpan di file itu (jalankan sekali per dokumen final).
   - `--html <file>` → versi HTML siap cetak (buka di browser → Cetak → Simpan sebagai PDF).
   - `--format json` → angka mentah.
   - Kuitansi DP/cicilan: isi `pembayaran` dengan uang yang diterima sekarang; kuitansi menampilkan uang diterima, baris diterima & sisa belum dibayar, dan **satu** terbilang untuk uang yang diterima.
3. **Tulis invoice lengkap di balasan chat** (bagian Markdown di atas garis `---`, apa adanya: nomor, item, subtotal, DPP, PPN, TOTAL, info PPh 23 & estimasi diterima bersih, terbilang, rekening). Pengguna di Telegram/WhatsApp **tidak bisa membuka path file lokal**, jadi jangan hanya menyebut lokasi file. File HTML: **lampirkan ke chat bila platform mendukung kirim file**; bila tidak, sebut lokasinya sebagai tambahan dan cara mencetaknya. Bagian "Info untuk penjual" **jangan** ikut dikirim ke pembeli; sampaikan ke pengguna sebagai catatan (meterai, PPN, PPh 23, peringatan) — salin angkanya apa adanya.
4. Bila meterai wajib: ingatkan untuk menempel meterai Rp10.000 atau e-meterai sebelum tanda tangan.
5. **Fallback tanpa Python:** hitung dengan rumus di bawah, tulis invoice dengan format yang sama, dan beri tahu pengguna bahwa angka dihitung manual (cek ulang sebelum dikirim).

## Rumus (untuk hitung manual)
```
jumlah baris   = qty × harga − diskon baris        (diskon % dari qty × harga; dibulatkan ke rupiah terdekat)
subtotal       = jumlah semua baris
setelah diskon = subtotal − diskon total           (diskon % dari subtotal; dibulatkan ke rupiah terdekat)
DPP            = setelah diskon + ongkir           (ongkir tidak dimasukkan bila "ongkir_kena_ppn": false)
PPN (PKP saja) = non-mewah: 12% × (11/12 × DPP) = 11% × DPP; mewah: 12% × DPP; dibulatkan KE BAWAH
TOTAL          = setelah diskon + ongkir + PPN
PPh 23 (info)  = 2% × nilai jasa tanpa PPN (default subtotal setelah diskon, tanpa ongkir); tanpa NPWP 4%;
                 dibulatkan KE BAWAH. Estimasi diterima bersih = TOTAL − PPh 23 (TOTAL tagihan tidak berubah;
                 dasar: UU PPh Pasal 23 ayat (1) huruf c & ayat (1a))
sisa tagihan   = TOTAL − pembayaran yang sudah diterima
termin persen  = TOTAL × persen, dibulatkan ke rupiah terdekat; termin terakhir = sisa agar jumlahnya pas
Bea meterai    = wajib Rp10.000 bila dokumen menyatakan penerimaan uang > Rp5.000.000
                 (kuitansi senilai uang diterima; invoice yang mencantumkan DP/pembayaran diterima)
                 tepat Rp5.000.000 → tidak wajib
```
Dasar aturan & sumber: `references/regulasi.md` (berlaku per 2026-09-23).

## Format output
```
# INVOICE / KUITANSI
No., Tanggal, Jatuh tempo, Status (BELUM DIBAYAR / SEBAGIAN DIBAYAR / LUNAS)
Dari: <penjual>   Kepada: <pembeli>
| No | Deskripsi | Qty | Harga | Diskon | Jumlah |
Subtotal, Diskon, Ongkir, [DPP, DPP nilai lain, PPN 12%], TOTAL, [Sudah dibayar, SISA TAGIHAN]
Terbilang, [Jadwal termin], Pembayaran ke, Catatan, Kota & tanggal, [Meterai], Tanda tangan
---
Info untuk penjual (meterai, PPN, pembulatan, peringatan)
```

## Contoh
**Input pengguna:** "Buat invoice dari CV Contoh Kreasi ke PT Pelanggan Contoh: 100 kaos sablon @65 ribu diskon 5%, biaya desain 500 ribu, ongkir 75 ribu. DP 3 juta sudah masuk tanggal 20 September. Rekening BCA 0000000000."

**Output (dipersingkat, dari `templates/contoh-invoice.json`):**
```
# INVOICE
**No.:** INV/2026/09/0001 · **Tanggal:** 23 September 2026 · **Jatuh tempo:** 7 Oktober 2026 · **Status:** SEBAGIAN DIBAYAR

| 1 | Kaos sablon custom | 100 pcs | Rp 65.000 | Rp 325.000 (5%) | Rp 6.175.000 |
| 2 | Biaya desain | 1 paket | Rp 500.000 | - | Rp 500.000 |
Subtotal Rp 6.675.000 · Ongkos kirim Rp 75.000 · **TOTAL Rp 6.750.000**
Sudah dibayar - DP (20 September 2026) -Rp 3.000.000 · **SISA TAGIHAN Rp 3.750.000**
Terbilang: Tiga Juta Tujuh Ratus Lima Puluh Ribu Rupiah
```
Catatan ke pengguna: DP Rp3.000.000 tidak melewati Rp5 juta, jadi meterai tidak wajib; kuitansi pelunasan nanti juga di bawah Rp5 juta. Sebutkan nomor invoice terakhir agar nomor berurutan.

## Checklist sebelum mengirim hasil
- [ ] Semua angka dari script; total, sisa tagihan, dan terbilang cocok.
- [ ] Klien badan + jasa + disebut "potong PPh 23" → PPh 23 & estimasi diterima bersih ikut tampil (dari script).
- [ ] Invoice lengkap ditulis di chat; file HTML dilampirkan bila bisa (bukan hanya path).
- [ ] PPN hanya muncul bila penjual PKP; tidak ada PPN untuk non-PKP.
- [ ] Nomor = nomor terakhir dari pengguna + 1 (cek baris "Nomor terakhir dibaca"); jatuh tempo tidak lebih awal dari tanggal dokumen.
- [ ] Tidak ada data karangan: kota/penanda tangan yang tidak disebut tetap `[isi ...]` dan disampaikan ke pengguna.
- [ ] Penanda meterai sesuai (> Rp5.000.000 penerimaan uang).
- [ ] Rekening & nama penerima benar; tidak ada data pribadi yang tidak diminta.
- [ ] Bagian "Info untuk penjual" tidak ikut dikirim ke pembeli.

## Batasan & penanganan error
- Script keluar kode 2 + `ERROR: ...` bila: PPN diaktifkan tetapi penjual bukan PKP, item kosong, qty ≤ 0, harga/diskon bukan angka, diskon melebihi nilai, diskon persen > 100%, total persen termin ≠ 100%, jumlah termin ≠ total, tanggal tidak valid, jatuh tempo sebelum tanggal dokumen, nomor terakhir tanpa angka urut, tanggal dokumen lebih lama dari periode nomor terakhir, atau JSON rusak. Jelaskan dengan bahasa sederhana dan perbaiki datanya.
- Pembayaran melebihi total → tetap dibuat dengan peringatan "lebih bayar".
- Satu jenis PPN per invoice (umum atau mewah). Barang dengan PPN khusus/dibebaskan, PPnBM, dan faktur pajak di luar cakupan → arahkan ke konsultan/DJP.
- Script hanya menulis file HTML/counter ke path yang diberikan pengguna; tidak ada akses internet.
