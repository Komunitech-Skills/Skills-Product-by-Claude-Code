# Uji ulang 2 — Invoice PKP + PPN + PPh 23 (buat-invoice 1.0.4)

Tanggal uji ulang: 2026-10-01 (Asia/Jakarta) · Penguji independen (bukan pembuat skill) · OpenClaw lokal asli (`openclaw agent --local`), model router Komunitech `ninerouter/komunitech`. Home `sol2-konsultan` direset lewat script reset tepat sebelum skenario (tidak ada file data yang perlu dibuat ulang; semua data ada di pesan). Hanya sisi SESUDAH. Pesan member **identik** dengan uji pertama dan uji ulang 1 ([01-invoice-ppn-pph23.md](01-invoice-ppn-pph23.md), [01-invoice-ppn-pph23-ulang.md](01-invoice-ppn-pph23-ulang.md)). Balasan disalin utuh tanpa suntingan. Semua angka dihitung ulang penguji dengan Python dan script skill dijalankan ulang oleh penguji. Argumen tool call tidak dapat diaudit (hanya nama tool dari JSON keluaran). Keluaran mentah: `hasil/ulang4-*.txt`.

## Cacat sisa dari uji ulang 1 (versi 1.0.3)
Agent bertanya dulu di giliran 1 (*"apakah invoice ini perlu mencantumkan PPN 11%"*, nomor, kota/penanda tangan) padahal member sudah menyebut PKP dan data lengkap; label "PPN 11%" usang.

## Pesan member (giliran 1)
```
Halo, tolong bikinin invoice buat PT Sinar Abadi Logistik ya. Jasa konsultasi pajak bulan September Rp 8.750.000, sama pendampingan pemeriksaan pajak 2 hari @ Rp 2.375.000. Saya sudah PKP (CV Arta Konsulindo). Mereka biasanya potong PPh 23. Jatuh tempo 14 hari. Rekening BCA 1234567890 a.n. CV Arta Konsulindo.
```

Jawaban lanjutan member dari uji ulang 1 **tidak diperlukan**: invoice langsung jadi di giliran 1.

## Giliran 1 — alat `read, ls, write, exec`
> Invoice sudah dibuat. Berikut hasilnya:
>
> # INVOICE
>
> **No.:** INV/2026/10/0001
> **Tanggal:** 1 Oktober 2026
> **Jatuh tempo:** 15 Oktober 2026
> **Status:** BELUM DIBAYAR
>
> **Dari:** CV Arta Konsulindo
> **Kepada:** PT Sinar Abadi Logistik
>
> | No | Deskripsi | Qty | Harga | Jumlah |
> |---:|---|---:|---:|---:|
> | 1 | Jasa konsultasi pajak bulan September | 1 paket | Rp 8.750.000 | Rp 8.750.000 |
> | 2 | Pendampingan pemeriksaan pajak | 2 hari | Rp 2.375.000 | Rp 4.750.000 |
>
> | | |
> |---|---:|
> | Subtotal | Rp 13.500.000 |
> | DPP nilai lain (11/12) | Rp 12.375.000 |
> | PPN 12% | Rp 1.485.000 |
> | **TOTAL** | **Rp 14.985.000** |
>
> Terbilang: *Empat Belas Juta Sembilan Ratus Delapan Puluh Lima Ribu Rupiah*
>
> *Info PPh 23 (dipotong & disetor oleh PT Sinar Abadi Logistik, tidak mengurangi total tagihan): 2% × Rp 13.500.000 = Rp 270.000. Estimasi diterima bersih: Rp 14.715.000. Mohon kirimkan bukti potong PPh 23.*
>
> **Pembayaran ke:**
> - BCA 1234567890 a.n. CV Arta Konsulindo
>
> [isi kota], 1 Oktober 2026
>
> **[isi nama penanda tangan]**
> CV Arta Konsulindo
>
> ---
>
> **Catatan untuk Anda (bukan buat dikirim ke klien):**
> 1. **Nomor invoice**: karena saya belum tahu nomor terakhir Anda, saya mulai dari `INV/2026/10/0001`. Kalau Anda sudah punya nomor sebelumnya, kasih tahu saya biar lanjut berurutan.
> 2. **Perlu diisi manual** sebelum dikirim: kota dan nama penanda tangan (saya tidak mengarang data ini).
> 3. **PPN**: saya pakai PPN 12% dengan DPP nilai lain 11/12 (sesuai PMK 131/2024) karena Anda sebut sudah PKP. Kalau transaksi ini disepakati tanpa PPN, kabari saya.
> 4. **PPh 23**: saya aktifkan asumsi tarif 2% (dengan NPWP) karena klien badan untuk jasa. Kalau ternyata mereka motong tanpa NPWP (4%) atau Anda sudah pakai PPh final UMKM dengan Surat Keterangan PP 55, kabari ya — angkanya beda.
> 5. **Meterai**: tidak wajib di invoice ini karena belum ada penerimaan uang di atas Rp5 juta tercatat. Nanti kuitansi pelunasan (Rp14.985.000) wajib meterai Rp10.000.
> 6. Invoice ini bukan faktur pajak — faktur pajak resmi tetap dibuat terpisah di Coretax.
>
> File HTML siap cetak tersimpan di `invoice-INV-0001.html` (folder kerja saya) — kalau mau saya kirimkan filenya atau isi dulu kota/nama penanda tangannya, tinggal bilang.

## Verifikasi independen
Python: subtotal 8.750.000 + 2 × 2.375.000 = **13.500.000** ✔; DPP nilai lain 13.500.000 × 11/12 = **12.375.000** ✔; PPN 12% = **1.485.000** (bulat, pembulatan ke bawah tidak berpengaruh) ✔; total **14.985.000** ✔; PPh 23 2% × 13.500.000 = **270.000** ✔ (dasar = DPP jasa tanpa PPN); estimasi diterima bersih **14.715.000** ✔; jatuh tempo 1 Okt + 14 hari = **15 Okt 2026** ✔; terbilang ✔; meterai Rp10.000 untuk kuitansi > Rp5 juta (UU 10/2020) ✔. File `invoice-INV-0001.html` dan `invoice-sinar-abadi.json` ada di workspace.

## Penilaian
- **Cacat sisa hilang: YA.** Tidak bertanya; PPN langsung aktif dengan asumsi disebut: *"saya pakai PPN 12% dengan DPP nilai lain 11/12 (sesuai PMK 131/2024) karena Anda sebut sudah PKP. Kalau transaksi ini disepakati tanpa PPN, kabari saya."* Label "PPN 11%" tidak muncul. Nomor, kota, penanda tangan diisi placeholder (`INV/2026/10/0001`, `[isi kota]`, `[isi nama penanda tangan]`).
- **Regresi:** tidak ada. Catatan tambahan baru tentang tarif 4% tanpa NPWP dan Surat Keterangan PP 55 relevan dan tidak mengubah angka.
- **Skor: 9/10** (uji ulang 1: 8). **LULUS.**
