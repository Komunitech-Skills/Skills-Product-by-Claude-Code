# Uji ulang 01 — Invoice PKP + PPN + PPh 23 (buat-invoice 1.0.3)

Tanggal uji ulang: 2026-10-01 (Asia/Jakarta) · Penguji independen (bukan pembuat skill) · OpenClaw lokal (`openclaw agent --local`), model router Komunitech `ninerouter/komunitech` (jawaban dilayani `claude-sonnet-5`). Home baru `sol2-konsultan` (paket skill solusi, dibuat ulang lewat script reset sebelum skenario). Hanya sisi SESUDAH. Pesan member **identik** dengan uji pertama ([01-invoice-ppn-pph23.md](01-invoice-ppn-pph23.md)). Balasan disalin utuh tanpa suntingan. Semua angka dihitung ulang penguji dengan Python. Argumen tool call tidak dapat diaudit (hanya nama tool dari JSON keluaran).

## Pesan member (giliran 1)
```
Halo, tolong bikinin invoice buat PT Sinar Abadi Logistik ya. Jasa konsultasi pajak bulan September Rp 8.750.000, sama pendampingan pemeriksaan pajak 2 hari @ Rp 2.375.000. Saya sudah PKP (CV Arta Konsulindo). Mereka biasanya potong PPh 23. Jatuh tempo 14 hari. Rekening BCA 1234567890 a.n. CV Arta Konsulindo.
```

## Giliran 1 — alat `read, ls` (28 dtk)
> Sebelum saya buatkan, ada 3 hal yang perlu dipastikan dulu (biar angkanya akurat dan nggak asal karang):
>
> 1. **PPN 11%** — karena CV Arta Konsulindo sudah PKP, apakah invoice ini perlu mencantumkan PPN 11%, atau memang disepakati tanpa PPN dengan klien?
> 2. **Nomor invoice terakhir** — biar nomornya lanjut urut. Kalau belum pernah bikin invoice bernomor sebelumnya, saya mulai dari `INV/2026/10/0001`.
> 3. **Kota & nama penanda tangan** untuk invoice ini (mis. "Jakarta, [Nama Anda], Direktur") — kalau tidak diisi, bagian ini saya kosongkan dengan tanda "PERLU DIISI".
>
> Boleh dijawab singkat ya, lalu langsung saya buatkan invoice-nya.

## Giliran 2
Uji pertama tidak punya giliran 2 (agent langsung membuat invoice). Penguji menjawab sekali sebagai member: *"Iya pakai PPN, kan saya sudah PKP. Belum pernah bikin invoice bernomor, mulai dari 0001 aja. Kota sama penanda tangan kosongin dulu."* Alat `write, exec` (29 dtk).

> Invoice sudah jadi. Ini yang dikirim ke PT Sinar Abadi Logistik:
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
> |---|---|---|---|---|
> | 1 | Jasa konsultasi pajak bulan September | 1 paket | Rp 8.750.000 | Rp 8.750.000 |
> | 2 | Pendampingan pemeriksaan pajak | 2 hari | Rp 2.375.000 | Rp 4.750.000 |
>
> - Subtotal: Rp 13.500.000
> - DPP (nilai lain 11/12): Rp 12.375.000
> - PPN 12%: Rp 1.485.000
> - **TOTAL: Rp 14.985.000**
>
> Terbilang: *Empat Belas Juta Sembilan Ratus Delapan Puluh Lima Ribu Rupiah*
>
> *Info PPh 23 (dipotong & disetor oleh PT Sinar Abadi Logistik, tidak mengurangi total tagihan): 2% x Rp 13.500.000 = Rp 270.000. Estimasi diterima bersih: Rp 14.715.000. Mohon kirimkan bukti potong PPh 23.*
>
> **Pembayaran ke:** BCA 1234567890 a.n. CV Arta Konsulindo
>
> [isi kota], 1 Oktober 2026
> **[isi nama penanda tangan]** — CV Arta Konsulindo
>
> ---
>
> **Catatan untuk Anda (tidak usah ikut dikirim):**
> - Kota dan nama penanda tangan belum diisi karena Anda minta dikosongkan — tolong lengkapi manual sebelum dikirim.
> - Tidak wajib meterai (invoice ini belum menyatakan uang diterima >Rp5 juta). Nanti kalau sudah bayar lunas/kuitansi di atas Rp5 juta, baru wajib meterai Rp10.000.
> - PPN dihitung pakai DPP nilai lain 11/12 sesuai aturan terbaru — invoice ini bukan faktur pajak, tetap buat faktur pajaknya di Coretax.
> - Saya sarankan tambahkan NPWP CV Arta Konsulindo di invoice berikutnya (kolom masih kosong).
>
> File HTML siap cetak sudah dibuat: `invoice-INV-0001.html` (buka di browser → Print → Save as PDF).

## Verifikasi independen
Subtotal 13.500.000 ✔; DPP nilai lain 11/12 = 12.375.000 ✔; PPN 12% = 1.485.000 ✔ (dibulatkan ke bawah, tepat); total 14.985.000 ✔; PPh 23 2% × 13.500.000 = **270.000** ✔; estimasi diterima bersih **14.715.000** ✔; jatuh tempo 15 Okt 2026 ✔; terbilang ✔; meterai tidak wajib untuk invoice ✔.

## Penilaian
- **Cacat lama hilang: YA.** (1) PPh 23 & neto kini dihitung script: *"2% x Rp 13.500.000 = Rp 270.000. Estimasi diterima bersih: Rp 14.715.000. Mohon kirimkan bukti potong PPh 23."* (2) Invoice lengkap ditulis di chat, bukan hanya path file. (Lampiran file ke chat tidak bisa dinilai di mode lokal tanpa kanal; path HTML tetap disebut.)
- **Regresi baru:** agent **bertanya dulu** di giliran 1 padahal data sudah lengkap dan member menyebut "Saya sudah PKP" — uji pertama langsung membuat invoice. Pertanyaannya juga memakai label usang: *"apakah invoice ini perlu mencantumkan **PPN 11%**"* (format PMK 131/2024 = PPN 12% × DPP nilai lain). Bagi awam ini menambah satu giliran dan membingungkan soal tarif. Penyebab kemungkinan: tabel input SKILL.md menulis default PPN "Tanpa PPN" dan rumus "= 11% × DPP".
- **Skor: 8/10** (uji pertama SESUDAH: 8). Angka kini lengkap dan benar, tetapi friksi giliran tambahan + label "PPN 11%" menahan skor.
- Saran: di SKILL.md, "penjual menyebut PKP + jasa ke klien badan → PPN aktif secara default, sebut asumsinya; jangan bertanya". Nomor & kota/penanda tangan cukup jadi placeholder (seperti versi 1.0.2). Jangan pernah menyebut "PPN 11%" ke pengguna.
