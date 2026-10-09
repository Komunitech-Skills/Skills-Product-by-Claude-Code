# Uji 04 - Input tidak lengkap: hanya kode saham

> Uji independen, 2026-09-29, claude-code (simulasi agent).

## 4a. Pengguna hanya menulis kode
**Input:** "BBCA"

**Perilaku yang diminta SKILL.md:** info kurang -> tanya **sekali**, bernomor, maks. 4.

**Output agent:**
> Siap bantu riset **BBCA** (PT Bank Central Asia Tbk). Supaya tepat, boleh jawab singkat:
> 1. Fokusnya apa: berita terbaru, aksi korporasi/dividen, laporan keuangan & rasio, atau semuanya?
> 2. Laporan keuangan periode mana? (default: yang terbaru yang saya temukan)
> 3. Punya harga saham + tanggalnya? (untuk PER/PBV/imbal dividen; kalau tidak, saya cari di sumber publik dan saya tulis tanggalnya)
>
> Kalau mau cepat, balas "langsung saja": saya buatkan semua bagian dari laporan terbaru yang ditemukan + berita 30 hari terakhir (maks. 5).
>
> _Bukan nasihat investasi. Keputusan & risiko sepenuhnya di tangan Anda. Cek prospektus/laporan resmi di idx.co.id & situs emiten; info izin & pengaduan: OJK (kontak 157)._

Penilaian: pertanyaan no. 1 SKILL.md ("Kode saham apa?") dilewati karena kode sudah ada - wajar. Satu pesan, 3 pertanyaan. Lolos.

## 4b. Pengguna memberi nama yang ambigu
**Input:** "riset saham indofood"

**Output agent (sesuai "Kode tidak ditemukan / nama mirip: jangan menebak"):**
> Ada dua emiten Indofood di BEI: **INDF** (PT Indofood Sukses Makmur Tbk, induk) dan **ICBP** (PT Indofood CBP Sukses Makmur Tbk, produk konsumen bermerek). Yang mana yang Anda maksud? Sekalian: fokusnya berita, dividen, rasio LK, atau semuanya?
>
> _Bukan nasihat investasi. Keputusan & risiko sepenuhnya di tangan Anda. Cek prospektus/laporan resmi di idx.co.id & situs emiten; info izin & pengaduan: OJK (kontak 157)._

Lolos.

## 4c. Pengguna menjawab "langsung saja" tapi web tidak tersedia
**Output agent (Batas Tegas #5):**
> Asumsi: semua bagian, LK terbaru, berita 30 hari. Namun saya **tidak bisa membuka situs** bursa/berita dari sini (idx.co.id memblokir akses otomatis). Saya tidak akan menulis berita atau angka dari ingatan. Silakan tempel: (a) ringkasan LK terbaru (pendapatan, laba, ekuitas, liabilitas, jumlah saham, satuan "dalam jutaan/miliar"), (b) harga + tanggal, (c) judul/tautan berita yang ingin dirangkum.
>
> _Bukan nasihat investasi. Keputusan & risiko sepenuhnya di tangan Anda. Cek prospektus/laporan resmi di idx.co.id & situs emiten; info izin & pengaduan: OJK (kontak 157)._

## 4d. Data parsial dijalankan ke script (`data/d5_kurang.json`: hanya laba 9 bulan, ekuitas, harga)
Hasil script (exit 0) - rasio yang datanya kurang ditulis "tidak dihitung, butuh: ...":
```
| ROE | 19,05% | laba bersih total 9 bulan x 12/9 (disetahunkan sederhana, abaikan musim) / total ekuitas (akhir periode) x 100% |
| EPS | - | tidak dihitung, butuh: Saham beredar |
| PER | - | tidak dihitung, butuh: EPS (laba & saham beredar) |
Kesegaran data:
- Tanggal laporan tidak diisi: kesegaran data tidak bisa dicek.
- Tanggal harga tidak diisi: PER, PBV, kapitalisasi & imbal dividen memakai harga tanpa tanggal.
Sumber laporan: TIDAK DICANTUMKAN
```
Verifikasi independen: 1,2 T x 12/9 / 8,4 T = 19,0476% -> 19,05%. Cocok.

Penilaian: penanganan input kurang jelas, tidak ada angka dikarang. Lolos.
