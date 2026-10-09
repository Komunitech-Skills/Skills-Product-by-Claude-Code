# 02 — Surat penawaran harga jasa desain (non-PKP, diskon, DP)

Tanggal uji: 2026-10-01 (Asia/Jakarta). OpenClaw lokal (`openclaw agent --local`), model router Komunitech (`ninerouter/komunitech`, sama dengan bot). SEBELUM = home `kosong-konsultan` (tanpa skill). SESUDAH = home `sol-konsultan` (paket skill solusi konsultan terpasang). Pesan identik di kedua sisi.

## Pesan member (giliran 1)

```
Bikinin surat penawaran harga ke CV Berkah Jaya Bakery dong. Jasa desain logo + brand guideline Rp 7,5 jt, desain template feed IG 12 desain @150rb, kasih diskon 10% dari total. Saya freelancer, belum PKP. DP 50%, penawaran berlaku 14 hari. Nama saya Dita Rahmawati.
```

## Pesan member (giliran 2)

```
Kota Bandung, WA 0812-0000-1111. PIC nggak tahu. Rekening BCA 9876543210 a.n. Dita Rahmawati. Pengerjaan 14 hari kerja setelah DP. Sisanya pakai default aja, langsung jadiin.
```

## SEBELUM (tanpa skill)

### Giliran 1 — tools: ['tool_search', 'memory_search', 'tool_call']; lampiran file ke chat: tidak; durasi 36 dtk

````markdown
Berikut draf **Surat Penawaran Harga (SPH)** untuk CV Berkah Jaya Bakery. Saya hitungkan totalnya dan isi sesuai detail yang kamu kasih — tinggal lengkapi bagian `[...]` (alamat/kontak) ya, soalnya saya belum punya data itu di memori.

**Rincian perhitungan:**
- Jasa desain logo + brand guideline: Rp 7.500.000
- Desain template feed IG: 12 desain × Rp 150.000 = Rp 1.800.000
- Subtotal: Rp 9.300.000
- Diskon 10%: − Rp 930.000
- **Total setelah diskon: Rp 8.370.000**
- DP 50%: Rp 4.185.000 | Pelunasan 50%: Rp 4.185.000

---

```
SURAT PENAWARAN HARGA
No: 001/SPH/DR/X/2026

Jakarta, 1 Oktober 2026

Kepada Yth.
Pimpinan CV Berkah Jaya Bakery
[Alamat CV Berkah Jaya Bakery]

Hal: Penawaran Harga Jasa Desain

Dengan hormat,

Bersama surat ini, saya mengajukan penawaran harga untuk jasa desain sebagai berikut:

No | Item | Qty | Harga Satuan | Subtotal
1  | Jasa Desain Logo + Brand Guideline | 1 paket | Rp 7.500.000 | Rp 7.500.000
2  | Desain Template Feed Instagram | 12 desain | Rp 150.000 | Rp 1.800.000
   |                                             | Subtotal | Rp 9.300.000
   |                                             | Diskon 10% | (Rp 930.000)
   |                                             | TOTAL | Rp 8.370.000

Catatan:
- Harga sudah termasuk diskon 10% dari total.
- Saya adalah penyedia jasa perorangan (freelancer), belum PKP, sehingga harga di atas belum termasuk PPN.
- Pembayaran: DP 50% (Rp 4.185.000) di muka sebagai tanda jadi, pelunasan 50% (Rp 4.185.000) saat pekerjaan selesai/sebelum file final diserahkan.
- Penawaran ini berlaku selama 14 (empat belas) hari kalender sejak tanggal surat, yaitu hingga 15 Oktober 2026.

Demikian penawaran ini saya sampaikan. Besar harapan saya dapat bekerja sama dengan CV Berkah Jaya Bakery. Terima kasih atas perhatiannya.

Hormat saya,


Dita Rahmawati
[No. HP/WA] | [Email]
```

---

Mau saya lengkapi juga nomor HP/WA, email, dan alamat kamu? Kalau dikasih, biar saya update dan jadikan langsung siap kirim (atau sekalian saya convert ke PDF).
````

### Giliran 2 — tools: ['write', 'exec']; lampiran file ke chat: ya (SPH-CV-Berkah-Jaya-Bakery.pdf); durasi 122 dtk

````markdown
PDF surat penawaran harganya sudah jadi.


**Ringkasan isi:**
- Logo + brand guideline: Rp 7.500.000
- Template feed IG 12× @150rb: Rp 1.800.000
- Subtotal Rp 9.300.000 → diskon 10% → **Total Rp 8.370.000**
- DP 50% (Rp 4.185.000) → transfer BCA 9876543210 a.n. Dita Rahmawati
- Pengerjaan 14 hari kerja sejak DP masuk
- Belum PKP (harga belum termasuk PPN)
- Berlaku s/d 15 Oktober 2026
- PIC CV Berkah Jaya Bakery saya kosongkan (ditujukan umum "Pimpinan CV Berkah Jaya Bakery") karena belum ada namanya — tinggal isi manual kalau sudah tahu.

Siap dikirim via WA/email ke calon klien.
````

**Jejak tool (sebelum):** Giliran 1: memory_search, langsung membuat draf. Giliran 2: tulis `.md`/`.html`, mencoba LibreOffice (gagal), lalu **`pip install weasyprint` tanpa bertanya ke member**, membuat PDF dan mengirimnya sebagai lampiran chat. Tidak ada skill.

## SESUDAH (dengan paket skill)

### Giliran 1 — tools: ['read']; lampiran file ke chat: tidak; durasi 18 dtk

````markdown
Siap, saya buatkan. Sebelum saya jalankan perhitungannya, boleh dilengkapi beberapa hal (biar suratnya rapi dan nggak ada "[isi]" kosong)?

1. **Kota & kontak Anda** untuk kop surat (WA dan/atau email)?
2. **Nama PIC** di CV Berkah Jaya Bakery (kalau tahu) — kalau tidak tahu, saya tulis "Kepada Yth. Pimpinan CV Berkah Jaya Bakery" saja.
3. **Nomor rekening** untuk syarat pembayaran (Bank – No. Rek – a.n.) — kalau belum mau dicantumkan, saya tulis `[isi rekening]`.
4. **Estimasi waktu pengerjaan** untuk logo+brand guideline dan untuk 12 desain feed IG (mis. "10 hari kerja setelah DP" dan "7 hari kerja setelah DP")? Kalau belum ada perkiraan, saya pakai default umum dan tandai sebagai asumsi.

Kalau mau cepat, bilang saja "pakai default" — saya lengkapi dengan placeholder yang jelas dan daftar asumsi di akhir surat.
````

### Giliran 2 — tools: ['exec', 'read']; lampiran file ke chat: tidak; durasi 35 dtk

````markdown
# (A) Surat Penawaran Harga

**DITA RAHMAWATI — Freelance Designer**
Bandung · WA 0812-0000-1111
---------------------------------------------
Nomor    : 001/SPH/DR/X/2026
Lampiran : -
Perihal  : Penawaran Harga Jasa Desain Logo, Brand Guideline & Template Feed Instagram

Bandung, 1 Oktober 2026

Kepada Yth.
Pimpinan CV Berkah Jaya Bakery
di tempat

Dengan hormat,
Bersama surat ini, kami sampaikan penawaran harga untuk jasa desain logo, brand guideline, dan template feed Instagram sesuai kebutuhan branding CV Berkah Jaya Bakery.

| No | Uraian | Qty | Satuan | Harga Satuan | Diskon | Jumlah |
|---|---|---|---|---|---|---|
| 1 | Jasa desain logo + brand guideline | 1 | paket | Rp 7.500.000 | - | Rp 7.500.000 |
| 2 | Desain template feed Instagram | 12 | desain | Rp 150.000 | - | Rp 1.800.000 |

| | |
|---|---|
| Subtotal | Rp 9.300.000 |
| Diskon (10%) | −Rp 930.000 |
| **TOTAL** | **Rp 8.370.000** |

Terbilang: *Delapan Juta Tiga Ratus Tujuh Puluh Ribu Rupiah*

**Syarat & ketentuan**
1. Harga tidak dikenakan PPN (bukan Pengusaha Kena Pajak).
2. Penawaran berlaku sampai dengan 15 Oktober 2026.
3. Pembayaran: DP 50% (Rp 4.185.000) saat konfirmasi/PO, pelunasan sisa 50% (Rp 4.185.000) saat hasil akhir diserahkan — ditransfer ke BCA 9876543210 a.n. Dita Rahmawati.
4. Pengerjaan: logo + brand guideline dan 12 desain template feed Instagram diselesaikan dalam 14 hari kerja setelah DP diterima.
5. Revisi: maksimal 2 kali putaran revisi per item untuk masing-masing jasa; revisi di luar ketentuan dikenakan biaya tambahan sesuai kesepakatan.

Demikian penawaran ini kami sampaikan. Kami siap membantu mewujudkan identitas visual yang kuat untuk CV Berkah Jaya Bakery. Mohon konfirmasi jika Bapak/Ibu berkenan melanjutkan ke tahap pengerjaan.

Hormat kami,

Dita Rahmawati
Freelance Designer

---

## (B) Teks WhatsApp

```
Selamat siang, Bapak/Ibu 🙏
Berikut penawaran harga dari Dita Rahmawati untuk kebutuhan branding CV Berkah Jaya Bakery:
• Jasa desain logo + brand guideline – 1 paket × Rp 7.500.000
• Desain template feed Instagram – 12 desain × Rp 150.000
Diskon 10% dari total
Total: *Rp 8.370.000* (tanpa PPN)
Berlaku s.d. 15 Oktober 2026.
Pembayaran: DP 50% (Rp 4.185.000) di awal, sisanya saat hasil diserahkan.
Pengerjaan 14 hari kerja setelah DP.
Surat penawaran resmi (PDF) terlampir. Kalau ada yang ingin disesuaikan, kabari saja ya 🙏
```

---

**Asumsi yang dipakai** (karena tidak disebutkan):
- Nama PIC CV Berkah Jaya Bakery tidak diketahui → surat ditujukan ke "Pimpinan CV Berkah Jaya Bakery".
- Revisi dibatasi 2 kali putaran per item (standar umum jasa desain) — silakan ubah jika ketentuan revisi Anda berbeda.
- Rekening pembayaran: BCA 9876543210 a.n. Dita Rahmawati (sesuai yang Anda berikan).

**Catatan:** Tidak ada PPN karena Anda belum PKP. Total & pembagian DP sudah dihitung dari script, bukan manual.

Kalau mau, saya bisa sesuaikan lagi (ganti nama PIC kalau sudah tahu, ubah jumlah revisi, atau buatkan versi PDF/HTML siap cetak).
````

**Jejak tool (sesudah):** Giliran 1: baca `surat-penawaran-harga/SKILL.md`, bertanya sekali (4 butir + opsi "pakai default"). Giliran 2: baca `scripts/hitung_sph.py`, jalankan `hitung_sph.py --item ... --diskon-total 10% --ppn tidak`. **Skill terpakai, angka dari script.** Tidak membuat file PDF/HTML.

## Verifikasi independen

| Pos | Benar | SEBELUM | SESUDAH |
|---|---|---|---|
| Subtotal (7.500.000 + 12 × 150.000) | 9.300.000 | ✔ | ✔ |
| Diskon 10% | 930.000 | ✔ | ✔ |
| Total | 8.370.000 | ✔ | ✔ |
| DP 50% / pelunasan | 4.185.000 / 4.185.000 | ✔ | ✔ |
| Berlaku 14 hari | s.d. 15 Okt 2026 | ✔ | ✔ |
| PPN | tidak ada (bukan PKP) | "harga **belum termasuk** PPN" — menyiratkan PPN bisa ditambah ✘ (kecil) | "tidak dikenakan PPN (bukan PKP)" ✔ |

Tidak ada pihak yang menyinggung bahwa klien berbentuk CV yang membayar jasa orang pribadi umumnya memotong **PPh 21 bukan pegawai** (bukan PPh 23) — informasi berguna bagi freelancer, tidak diminta, tidak dinilai sebagai kesalahan.
SESUDAH: teks WA menulis "Surat penawaran resmi (PDF) terlampir" padahal tidak ada PDF yang dibuat — inkonsistensi.

## Nilai

| Aspek | SEBELUM | SESUDAH |
|---|---|---|
| Ketepatan angka | Benar | Benar (script) |
| Siap pakai | Draf langsung di giliran 1; PDF jadi & terlampir di giliran 2 | Surat + versi WA + terbilang + syarat revisi; tidak ada file cetak; WA menyebut PDF yang tidak ada |
| Kepatuhan aturan ID | Kalimat PPN kurang tepat | Tepat |
| Keamanan/privasi | Memasang paket Python dari internet tanpa izin member | Aman |
| Kejelasan | Baik | Baik, asumsi dicantumkan |
| **Total (1–10)** | **7** | **8** |

Angka sama-sama benar. SESUDAH unggul di kelengkapan isi (terbilang, versi WA, syarat revisi, daftar asumsi, PPN tepat) dan bertanya sekali sesuai prinsip "instan". SEBELUM unggul praktis karena menghasilkan PDF terlampir — tetapi dengan `pip install` tanpa izin, yang tidak boleh terjadi di komputer member. Selisih kecil; jujurnya ini bukan kemenangan telak.
