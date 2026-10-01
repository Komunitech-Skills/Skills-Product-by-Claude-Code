# Uji ulang ke-3 — Konsultan 02 · Surat penawaran harga non-PKP (surat-penawaran-harga 1.0.4)

Tanggal: 2026-10-01 (Asia/Jakarta) · Penguji independen ke-3 (bukan pembuat skill). OpenClaw asli lokal (`openclaw agent --local`), model router Komunitech (`ninerouter/komunitech`, jawaban `claude-sonnet-5`), sama dengan bot member. Home `sol3-konsultan` direset (`reset3-*.sh`, skill terbaru dari repo) sebelum skenario, sesi baru, hanya sisi SESUDAH. Pesan member (dan jawaban lanjutan) **sama persis** dengan uji pertama. Argumen tool call tidak dibaca (database sesi tidak dibuka), jadi `find /` atau instalasi paket hanya bisa dideteksi dari teks balasan dan jumlah/jenis alat: **tidak ada tanda instalasi paket atau `find /`** di skenario ini (tidak ada balasan/berkas yang menyinggungnya).

## Pesan member giliran 1 (sama persis)

> Bikinin surat penawaran harga ke CV Berkah Jaya Bakery dong. Jasa desain logo + brand guideline Rp 7,5 jt, desain template feed IG 12 desain @150rb, kasih diskon 10% dari total. Saya freelancer, belum PKP. DP 50%, penawaran berlaku 14 hari. Nama saya Dita Rahmawati.

## Pesan member giliran 2 (sama persis)

> Kota Bandung, WA 0812-0000-1111. PIC nggak tahu. Rekening BCA 9876543210 a.n. Dita Rahmawati. Pengerjaan 14 hari kerja setelah DP. Sisanya pakai default aja, langsung jadiin.

## Balasan SESUDAH (ulang ke-3) — giliran 1 (utuh)

_alat: `read, exec` · 3 panggilan, 0 gagal · durasi 52 dtk_

> Berikut Surat Penawaran Harga untuk CV Berkah Jaya Bakery. Saya pakai asumsi untuk beberapa detail yang belum disebutkan — tinggal isi bagian `[...]` ya.
>
> ---
>
> **DITA RAHMAWATI — Jasa Desain Freelance**
> [Alamat] · WA [isi nomor WA] · [isi email]
> ---------------------------------------------
> Nomor    : 001/SPH/DR/X/2026
> Lampiran : -
> Perihal  : Penawaran Harga Jasa Desain Logo, Brand Guideline & Konten Feed Instagram
>
> Jakarta, 1 Oktober 2026
>
> Kepada Yth.
> Bapak/Ibu Pimpinan
> CV Berkah Jaya Bakery
> di tempat
>
> Dengan hormat,
> Menindaklanjuti kebutuhan Bapak/Ibu akan jasa desain untuk CV Berkah Jaya Bakery, dengan ini kami sampaikan penawaran harga sebagai berikut.
>
> | No | Uraian | Qty | Satuan | Harga Satuan | Diskon | Jumlah |
> |---|---|---|---|---|---|---|
> | 1 | Jasa desain logo + brand guideline | 1 | paket | Rp 7.500.000 | - | Rp 7.500.000 |
> | 2 | Desain template feed IG | 12 | desain | Rp 150.000 | - | Rp 1.800.000 |
>
> | | |
> |---|---|
> | Subtotal | Rp 9.300.000 |
> | Diskon (10%) | −Rp 930.000 |
> | **TOTAL** | **Rp 8.370.000** |
>
> Terbilang: *Delapan Juta Tiga Ratus Tujuh Puluh Ribu Rupiah*
>
> **Syarat & ketentuan**
> 1. Harga final; penjual bukan PKP sehingga tidak memungut PPN.
> 2. Penawaran berlaku sampai dengan 15 Oktober 2026.
> 3. Pembayaran: DP 50% (Rp 4.185.000) saat penawaran disetujui/PO, pelunasan sisa Rp 4.185.000 saat hasil akhir diserahkan, ke [Bank – No. Rek – a.n. Dita Rahmawati].
> 4. Pengerjaan: logo & brand guideline estimasi [isi berapa hari kerja], dilanjutkan 12 desain template feed IG estimasi [isi berapa hari kerja], dimulai setelah DP diterima. Revisi: [isi, mis. maks. 2x revisi per item].
> 5. File hasil akhir diserahkan dalam format [isi, mis. AI/PDF/PNG/JPG siap pakai].
>
> Besar harapan kami penawaran ini dapat menjadi pertimbangan Bapak/Ibu. Kami siap menerima konfirmasi dan menjawab pertanyaan lebih lanjut.
>
> Hormat kami,
>
> Dita Rahmawati
> Freelance Designer
>
> **Asumsi yang dipakai** (tolong cek/sesuaikan):
> - Alamat, WA, email Dita belum diisi — isi bagian `[...]` di kop surat.
> - PIC di CV Berkah Jaya Bakery belum diketahui → pakai sapaan "Bapak/Ibu Pimpinan".
> - Rekening bank belum diisi.
> - Timeline pengerjaan & jumlah revisi belum disebutkan — saya kosongkan sebagai `[isi]`, sebaiknya diisi supaya SPH tidak menimbulkan ekspektasi tak terbatas.
> - Format file hasil akhir belum disebutkan.
>
> **Catatan:** Skill ini tidak membuat PDF. Setelah bagian `[isi]` dilengkapi, tempel surat ini ke Word/Google Docs lalu *File → Download/Save as PDF*.
>
> ---
>
> **Teks WhatsApp:**
> ```
> Selamat siang, Bapak/Ibu 🙏
> Berikut penawaran harga dari Dita Rahmawati (Freelance Designer) untuk CV Berkah Jaya Bakery:
> • Jasa desain logo + brand guideline – Rp 7.500.000
> • Desain template feed IG – 12 desain × Rp 150.000
> Diskon 10%, Total: *Rp 8.370.000* (harga final, bukan PKP, tanpa PPN)
> Berlaku s.d. 15 Oktober 2026. DP 50% di awal, pelunasan saat hasil diserahkan.
> Surat penawaran resminya menyusul ya. Kalau ada yang ingin disesuaikan, kabari saja 🙏
> ```
>
> Mau saya isikan alamat/WA/email, timeline pengerjaan, jumlah revisi, dan rekening banknya sekalian? Kasih infonya aja, nanti saya update surat ini.

## Balasan SESUDAH (ulang ke-3) — giliran 2 (utuh)

_alat: `tidak ada` · 0 panggilan, 0 gagal · durasi 46 dtk_

> Siap, sudah saya lengkapi sesuai info dari Mbak Dita. Ini versi final:
>
> ---
>
> **DITA RAHMAWATI — Jasa Desain Freelance**
> Bandung · WA 0812-0000-1111
> ---------------------------------------------
> Nomor    : 001/SPH/DR/X/2026
> Lampiran : -
> Perihal  : Penawaran Harga Jasa Desain Logo, Brand Guideline & Konten Feed Instagram
>
> Bandung, 1 Oktober 2026
>
> Kepada Yth.
> Bapak/Ibu Pimpinan
> CV Berkah Jaya Bakery
> di tempat
>
> Dengan hormat,
> Menindaklanjuti kebutuhan Bapak/Ibu akan jasa desain untuk CV Berkah Jaya Bakery, dengan ini kami sampaikan penawaran harga sebagai berikut.
>
> | No | Uraian | Qty | Satuan | Harga Satuan | Diskon | Jumlah |
> |---|---|---|---|---|---|---|
> | 1 | Jasa desain logo + brand guideline | 1 | paket | Rp 7.500.000 | - | Rp 7.500.000 |
> | 2 | Desain template feed IG | 12 | desain | Rp 150.000 | - | Rp 1.800.000 |
>
> | | |
> |---|---|
> | Subtotal | Rp 9.300.000 |
> | Diskon (10%) | −Rp 930.000 |
> | **TOTAL** | **Rp 8.370.000** |
>
> Terbilang: *Delapan Juta Tiga Ratus Tujuh Puluh Ribu Rupiah*
>
> **Syarat & ketentuan**
> 1. Harga final; penjual bukan PKP sehingga tidak memungut PPN.
> 2. Penawaran berlaku sampai dengan 15 Oktober 2026.
> 3. Pembayaran: DP 50% (Rp 4.185.000) saat penawaran disetujui/PO, pelunasan sisa Rp 4.185.000 saat hasil akhir diserahkan, ke rekening BCA 9876543210 a.n. Dita Rahmawati.
> 4. Pengerjaan: 14 hari kerja sejak DP diterima, mencakup desain logo, brand guideline, dan 12 desain template feed IG. Revisi: maksimal 2x revisi minor per item; perubahan konsep besar di luar itu dikenakan biaya tambahan sesuai kesepakatan.
> 5. File hasil akhir diserahkan dalam format digital siap pakai (vector AI/PDF serta PNG/JPG resolusi tinggi).
>
> Besar harapan kami penawaran ini dapat menjadi pertimbangan Bapak/Ibu. Kami siap menerima konfirmasi dan menjawab pertanyaan lebih lanjut.
>
> Hormat kami,
>
> Dita Rahmawati
> Freelance Designer
>
> **Catatan:** Skill ini tidak membuat PDF. Tempel surat ini ke Word/Google Docs lalu *File → Download/Save as PDF* untuk kirim ke klien. Perhitungan tidak melibatkan PPN karena Mbak Dita belum PKP (tidak ada kewajiban pungut PPN).
>
> ---
>
> **Teks WhatsApp (siap kirim):**
> ```
> Selamat siang, Bapak/Ibu 🙏
> Berikut penawaran harga dari Dita Rahmawati (Freelance Designer) untuk CV Berkah Jaya Bakery:
> • Jasa desain logo + brand guideline – Rp 7.500.000
> • Desain template feed IG – 12 desain × Rp 150.000
> Diskon 10%, Total: *Rp 8.370.000* (harga final, bukan PKP, tanpa PPN)
> Berlaku s.d. 15 Oktober 2026. DP 50% (Rp 4.185.000) di awal, pelunasan saat hasil diserahkan. Pengerjaan 14 hari kerja setelah DP.
> Surat penawaran resminya menyusul ya. Kalau ada yang ingin disesuaikan, kabari saja 🙏
> ```
>
> Siap dikirim. Kalau mau diubah lagi (misal revisi jumlah revisi gratis, atau tambah item), tinggal bilang saja.

## Cacat lama — hilang?

Uji pertama: [02-surat-penawaran-harga.md](02-surat-penawaran-harga.md) · uji ulang ke-2: [02-surat-penawaran-harga-ulang.md](02-surat-penawaran-harga-ulang.md). Hanya 2 giliran (tidak perlu giliran tambahan seperti di uji ulang ke-2).

| Cacat dilaporkan (uji ulang ke-2) | Hilang? | Bukti (kutipan) |
|---|---|---|
| Surat hanya disimpan ke file, tidak tampil di chat | **Ya** | Kedua giliran menampilkan surat **utuh** di chat; tidak ada file di workspace (hanya AGENTS/IDENTITY/SOUL/USER). |
| Teks WA tidak dibuat sampai diminta | **Ya** | Kedua giliran memuat *"Teks WhatsApp (siap kirim)"*. |
| `[Nama PIC]` padahal member menjawab "PIC nggak tahu" | **Ya** | *"Kepada Yth. Bapak/Ibu Pimpinan, CV Berkah Jaya Bakery"* (README menyebut default "Bagian Pengadaan"; "Pimpinan" juga wajar). |
| WA non-PKP "(belum kena PPN)" | **Ya** | Surat: *"Harga final; penjual bukan PKP sehingga tidak memungut PPN."* WA: *"(harga final, bukan PKP, tanpa PPN)"*. |
| WA menyebut "PDF terlampir" (uji pertama) | **Ya** | *"Surat penawaran resminya menyusul ya"* + *"Skill ini tidak membuat PDF … File → Download/Save as PDF"*. |

## Verifikasi angka (Python penguji)

Python: 7.500.000 + 12 × 150.000 = 9.300.000 ✓; diskon 10% = 930.000 ✓; total 8.370.000 ✓ (tabel = terbilang = WA); DP/pelunasan 4.185.000 / 4.185.000 ✓; berlaku 14 hari → 15 Okt 2026 ✓.

## Regresi / temuan baru

- **Regresi nyata (giliran 1): kota dikarang.** Agent tidak lagi bertanya; langsung menyusun surat dengan placeholder `[...]`, tetapi menulis **"Jakarta, 1 Oktober 2026"** — member tidak pernah menyebut kota, dan "Jakarta" tidak ada di daftar asumsi. Agent bilang *"tinggal isi bagian `[...]` ya"*, jadi member yang langsung memakai surat giliran 1 akan mengirim kota yang salah. Di giliran 2 dikoreksi ke Bandung setelah member menyebutnya.
- Giliran 2 menambah syarat yang tidak diberikan member: *"maksimal 2x revisi minor per item; perubahan konsep besar … biaya tambahan"* dan format file *"vector AI/PDF serta PNG/JPG"*. Member memang berkata "sisanya pakai default aja", jadi default boleh, tetapi giliran 2 **tidak lagi mencantumkan daftar asumsi** (giliran 1 masih).
- Jabatan "Freelance Designer" diasumsikan (wajar, disebut di asumsi giliran 1).
- Tidak bertanya sekali di awal (uji sebelumnya bertanya) — sah menurut prinsip "pakai default bila ingin cepat", tetapi member tidak meminta cepat.

## Nilai

| | Sesudah lama | Sesudah baru (ulang ke-3) |
|---|---|---|
| Skor | 8 (uji pertama) / 7,5 (ulang ke-2) | **8** |

Semua cacat yang dilaporkan hilang: surat + WA tampil di chat sejak giliran 1, PIC tanpa placeholder, kalimat non-PKP benar, angka benar. Tetapi muncul satu regresi nyata: kota "Jakarta" dikarang di surat giliran 1 tanpa ditandai. **LULUS uji ulang ke-3 untuk cacat yang dilaporkan, dengan 1 regresi yang perlu patch kecil** (kota tidak diketahui → `[Kota]`; default yang dipakai di giliran mana pun wajib tercantum di daftar asumsi).
