---
name: buat-invoice
description: Membuat invoice/tagihan atau kuitansi profesional berbahasa Indonesia dengan nomor otomatis, daftar item, diskon, ongkir, PPN opsional khusus PKP (DPP nilai lain 11/12), DP/termin, sisa tagihan, terbilang, rekening, jatuh tempo, dan penanda bea meterai Rp10.000 bila penerimaan uang di atas Rp5 juta; output Markdown rapi plus HTML siap cetak. Gunakan saat pengguna minta "buatkan invoice", "nota tagihan", "kuitansi DP/lunas", atau invoice generator, receipt, billing. Menagih ulang piutang pakai tagih-piutang; penawaran harga pakai surat-penawaran-harga.
---

# Buat Invoice & Kuitansi

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
| Tanggal & jatuh tempo | Tidak | Hari ini; jatuh tempo 14 hari |
| Diskon total, ongkir | Tidak | 0 |
| PPN (hanya jika penjual PKP) + jenis (umum/mewah) | Tidak | Tanpa PPN |
| DP/pembayaran yang sudah diterima, termin | Tidak | Belum ada |
| Rekening, alamat/kontak, NPWP, catatan, penanda tangan | Tidak | Dikosongkan |

Jika info wajib kurang, tanyakan **sekali** dalam satu pesan bernomor (maks. 5 pertanyaan). Jika pengguna minta PPN, pastikan ia **PKP**; jika tidak, jelaskan bahwa PPN tidak boleh dicantumkan.

## Langkah kerja
1. Susun data ke file JSON di folder kerja pengguna mengikuti `templates/contoh-invoice.json` (penjelasan kolom: `references/format-input.md`).
2. Jalankan script (path relatif terhadap folder SKILL.md ini; Windows: `python` atau `py`):
   ```bash
   python3 <folder-skill-ini>/scripts/buat_invoice.py --file invoice.json --html invoice-INV-0008.html --nomor-terakhir INV/2026/09/0007
   ```
   - `--nomor-terakhir` → nomor berikutnya otomatis (angka urut terakhir ditambah 1).
   - `--counter-file nomor-invoice.json` → nomor urut per bulan disimpan di file itu (jalankan sekali per dokumen final).
   - `--html <file>` → versi HTML siap cetak (buka di browser → Cetak → Simpan sebagai PDF).
   - `--format json` → angka mentah.
3. Kirim bagian Markdown (di atas garis `---`) sebagai invoice. Bagian "Info untuk penjual" **jangan** ikut dikirim ke pembeli; sampaikan ke pengguna sebagai catatan (meterai, PPN, peringatan).
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
- [ ] PPN hanya muncul bila penjual PKP; tidak ada PPN untuk non-PKP.
- [ ] Nomor dokumen benar/berurutan; jatuh tempo tidak lebih awal dari tanggal dokumen.
- [ ] Penanda meterai sesuai (> Rp5.000.000 penerimaan uang).
- [ ] Rekening & nama penerima benar; tidak ada data pribadi yang tidak diminta.
- [ ] Bagian "Info untuk penjual" tidak ikut dikirim ke pembeli.

## Batasan & penanganan error
- Script keluar kode 2 + `ERROR: ...` bila: PPN diaktifkan tetapi penjual bukan PKP, item kosong, qty ≤ 0, harga/diskon bukan angka, diskon melebihi nilai, diskon persen > 100%, total persen termin ≠ 100%, jumlah termin ≠ total, tanggal tidak valid, jatuh tempo sebelum tanggal dokumen, atau JSON rusak. Jelaskan dengan bahasa sederhana dan perbaiki datanya.
- Pembayaran melebihi total → tetap dibuat dengan peringatan "lebih bayar".
- Satu jenis PPN per invoice (umum atau mewah). Barang dengan PPN khusus/dibebaskan, PPnBM, dan faktur pajak di luar cakupan → arahkan ke konsultan/DJP.
- Script hanya menulis file HTML/counter ke path yang diberikan pengguna; tidak ada akses internet.
