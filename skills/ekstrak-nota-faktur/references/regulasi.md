# Dasar aturan untuk cek nota & faktur (berlaku per 23 September 2026)

> Ringkasan untuk alat bantu cek, bukan nasihat pajak. Aturan bisa berubah. Cek sumber resmi sebelum mengambil keputusan.
> Kolom **Status** menjelaskan seberapa yakin kami. Item **BELUM TERVERIFIKASI** hanya boleh memicu *peringatan*, tidak boleh dipakai untuk menolak dokumen.

## 1. Tarif & hitungan PPN

| Hal | Ketentuan | Status |
|---|---|---|
| Tarif PPN | 12% (UU HPP) | Terverifikasi |
| Barang/jasa **biasa (non-mewah)** | PPN = 12% × DPP nilai lain. DPP nilai lain = **11/12 × harga jual/penggantian**, jadi efektif **11% dari harga** (PMK 131/2024, berlaku 1 Januari 2025) | Terverifikasi |
| Barang **mewah** (kena PPnBM) | PPN = 12% × harga penuh sejak 1 Februari 2025. Januari 2025 masa transisi (12% × 11/12) | Terverifikasi |
| Barang/jasa dengan DPP nilai lain atau besaran tertentu sendiri (mis. kendaraan bekas, emas, pulsa) | Tidak memakai 11/12. Di luar cakupan cek otomatis (`jenis_ppn: "lainnya"`) | Terverifikasi |
| Dokumen bertanggal 1 April 2022 s.d. 31 Desember 2024 | PPN 11% × DPP | Terverifikasi (UU HPP) |
| Dokumen bertanggal sebelum 1 April 2022 | PPN 10% × DPP | Terverifikasi (UU PPN lama) |
| Yang boleh memungut PPN | Hanya PKP. Faktur pajak dibuat lewat Coretax / e-Faktur Desktop / H2H (KEP-54/PJ/2025) | Terverifikasi |
| Barang/jasa dibebaskan atau PPN ditanggung pemerintah (DTP), mis. sebagian bahan pokok | Ada, tapi daftarnya panjang dan berubah. Skill **tidak** menentukan sendiri apakah suatu barang bebas PPN; ikuti yang tertulis di dokumen | Sengaja tidak dirinci |

### Pembulatan (keputusan desain, sama dengan skill `hitung-ppn`)
- PPN yang diharapkan = 11% × DPP (non-mewah) atau 12% × DPP (mewah), **dibulatkan ke bawah** ke rupiah penuh. Hasilnya sama dengan 12% × 11/12 × DPP, tanpa pembulatan berantai.
- Selisih **±Rp1** dianggap cocok karena sistem kasir/Coretax bisa membulatkan berbeda. Perilaku pembulatan Coretax sendiri **belum diverifikasi**.
- Jumlah item vs subtotal: toleransi ±Rp1 per baris item.
- Harga sudah termasuk PPN (struk minimarket): DPP + PPN harus sama dengan harga (toleransi ±Rp2).

## 2. Identitas pajak & nomor faktur (era Coretax)

Situs resmi (pajak.go.id, jdih.kemenkeu.go.id) dan artikel konsultan **tidak bisa dibuka langsung** saat riset 23 September 2026; yang terbaca hanya cuplikan hasil pencarian. Cuplikan dari beberapa sumber berbeda konsisten satu sama lain, tetapi dokumen primernya belum dibaca. Karena itu semua format di bawah **BELUM TERVERIFIKASI**. Script hanya memberi **peringatan** dan tidak pernah menolak dokumen karena panjang digit.

| Hal | Yang dilaporkan sumber | Status |
|---|---|---|
| NPWP orang pribadi | NIK 16 digit dipakai sebagai NPWP | BELUM TERVERIFIKASI (cuplikan) |
| NPWP badan | 16 digit = NPWP lama 15 digit ditambah angka **0 di depan** (PMK 112/2022 diubah PMK 136/2023; format 16 digit berlaku penuh sejak 1 Juli 2024 menurut cuplikan) | BELUM TERVERIFIKASI (cuplikan) |
| NITKU | **22 digit** = 16 digit NPWP + 6 digit kode tempat kegiatan usaha | BELUM TERVERIFIKASI (cuplikan) |
| Nomor seri faktur pajak (NSFP) Coretax | **17 digit** = 2 digit kode transaksi + 2 digit kode status + 13 digit nomor seri dari DJP (2 digit pertama nomor seri = tahun). Diberikan otomatis oleh Coretax. Dasar: PER-11/PJ/2025 Pasal 37 ayat (1) menurut cuplikan | BELUM TERVERIFIKASI (cuplikan) |
| Kode status | `00` = faktur normal; `01`, `02`, … = faktur pengganti ke-1, ke-2, … | BELUM TERVERIFIKASI (cuplikan) |
| Kode transaksi | 10 kode (`01`–`10`). `01` = penyerahan biasa (PPN dipungut penjual), `02` = ke pemungut PPN instansi pemerintah. Arti kode lain di script adalah perkiraan dari format e-Faktur lama | BELUM TERVERIFIKASI |
| Format e-Faktur lama | Nomor seri 16 digit (`010.000-25.12345678`), NPWP 15 digit | Dipakai sebelum Coretax |

**Aturan untuk agent:** jika panjang digit tidak sesuai, tulis "perlu dicek ulang" dan sarankan tanya penjual. Jangan pernah menulis "faktur palsu" atau "tidak sah".

## 3. Bea meterai (UU 10/2020)
- Tarif tunggal **Rp10.000** (tempel atau e-meterai).
- Wajib untuk dokumen yang menyatakan **penerimaan uang dengan nilai > Rp5.000.000** (mis. kuitansi), serta surat perjanjian. Script hanya memberi *info* bila kuitansi > Rp5 juta dan kolom meterai kosong.

## 4. PPh yang sering muncul di invoice
- Invoice jasa ke badan usaha sering dipotong **PPh 23** oleh pembeli. Script mengenali bila total = dasar + PPN − PPh.
- Tarif PPh tidak dihitung ulang oleh skill ini karena bergantung pada jenis jasa dan status penerima. Ikuti yang tertulis di dokumen, dan arahkan ke konsultan bila ragu.

## Sumber
- DJP, PPN 12% & DPP nilai lain: https://www.pajak.go.id/en/node/113453
- PMK 131/2024 (JDIH BPK): https://peraturan.bpk.go.id/Details/311485/pmk-no-131-tahun-2024
- DDTC, PPN 12% barang mewah 2026: https://news.ddtc.co.id/berita/nasional/1812992/tak-berubah-tarif-ppn-12-tetap-berlaku-untuk-barang-mewah-di-2026
- DJP, Coretax & faktur (KEP-54/PJ/2025): https://pajak.go.id/en/node/115238
- PER-11/PJ/2025 (JDIH Kemenkeu, belum terbaca): https://jdih.kemenkeu.go.id/dok/per-11pj2025
- DDTC, PER-11/PJ/2025 kode & nomor seri faktur (cuplikan): https://news.ddtc.co.id/berita/nasional/1811127/per-11pj2025-pertegas-ketentuan-kode-dan-nomor-seri-faktur-pajak
- IKPI, NSFP 17 digit (cuplikan): https://ikpi.or.id/en/format-baru-nsfp-era-coretax-kini-17-digit-dan-diberikan-otomatis/
- DJP, Coretax & NPWP 16 digit (cuplikan): https://pajak.go.id/en/node/114311
- DDTC, NIK sebagai NPWP, NPWP 16 digit, NITKU (cuplikan): https://news.ddtc.co.id/literasi/kamus/1803684/apa-beda-nik-sebagai-npwp-npwp-16-digit-dan-nitku
- Bea meterai: https://www.online-pajak.com/pajak/materai-10000/

Kontak resmi: Kring Pajak 1500200, https://www.pajak.go.id
