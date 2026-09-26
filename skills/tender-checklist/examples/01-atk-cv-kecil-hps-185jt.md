# Skenario 01 — CV usaha kecil, tender ATK dinas kabupaten (HPS Rp185 juta, PKP)

> Uji independen Tahap 6, 2026-09-25. Penguji bukan pembuat skill; hanya membaca folder skill. Script dijalankan dari salinan di scratchpad. Output script di bawah **apa adanya**; bagian lain adalah jawaban agent yang mengikuti SKILL.md.

## Input pengguna
"Saya punya CV (usaha kecil di NIB, KBLI 47612 & 46900, sudah PKP). Mau ikut tender Pengadaan ATK Dinas Pendidikan Kabupaten, HPS Rp185 juta, pagu Rp190 juta, pascakualifikasi. Pengumuman 28/9, penjelasan 2/10, batas unggah 14 Oktober 2026 jam 15.00. Layak ikut nggak? Dokumen apa saja? Tolong cek juga rincian harga saya (12 barang), harga belum termasuk PPN."

## CSV rincian (dibuat agent dari tabel pengguna; format rupiah Indonesia)
```
No;Uraian;Volume;Satuan;Harga Satuan
1;Kertas HVS A4 80 gsm;600;rim;Rp58.750
2;Kertas HVS F4 70 gsm;250;rim;Rp56.300
3;Tinta printer original hitam 70 ml;120;botol;Rp118.500
4;Tinta printer original warna 70 ml;90;botol;Rp121.250
5;Toner laser 85A;35;pcs;Rp1.187.500,00
6;Map snelhecter plastik;2.000;buah;Rp3.450
7;Ordner besar 7 cm;400;buah;Rp37.800
8;Pulpen gel 0,5 mm;144;lusin;Rp42.600
9;Stapler HD-10 + isi;150;set;Rp28.750
10;Amplop putih 110 dus isi 100;80;dus;Rp41.900
11;Flashdisk 32 GB;60;pcs;Rp92.400
12;Buku agenda folio 100 lbr;250;buah;Rp24.650
```

## Perintah
```
python3 scripts/cek_penawaran.py harga s01.csv --ppn nonmewah --hps "Rp185.000.000" --pagu "Rp190.000.000"
python3 scripts/cek_penawaran.py jadwal --batas "2026-10-14 15:00" --pengumuman 2026-09-28 --penjelasan 2026-10-02 --hari-ini 2026-09-25
```

## Output script — harga
```
RINCIAN PENAWARAN HARGA (hasil hitung script)

 No  Uraian                                  Volume  Sat             Harga Satuan              Jumlah
  1  Kertas HVS A4 80 gsm                       600  rim                 Rp58.750        Rp35.250.000
  2  Kertas HVS F4 70 gsm                       250  rim                 Rp56.300        Rp14.075.000
  3  Tinta printer original hitam 70 ml         120  botol              Rp118.500        Rp14.220.000
  4  Tinta printer original warna 70 ml          90  botol              Rp121.250        Rp10.912.500
  5  Toner laser 85A                             35  pcs              Rp1.187.500        Rp41.562.500
  6  Map snelhecter plastik                   2.000  buah                 Rp3.450         Rp6.900.000
  7  Ordner besar 7 cm                          400  buah                Rp37.800        Rp15.120.000
  8  Pulpen gel 0,5 mm                          144  lusin               Rp42.600         Rp6.134.400
  9  Stapler HD-10 + isi                        150  set                 Rp28.750         Rp4.312.500
 10  Amplop putih 110 dus isi 100                80  dus                 Rp41.900         Rp3.352.000
 11  Flashdisk 32 GB                             60  pcs                 Rp92.400         Rp5.544.000
 12  Buku agenda folio 100 lbr                  250  buah                Rp24.650         Rp6.162.500

Subtotal (DPP)                     : Rp163.545.400
PPN 12% x 11/12 DPP (efektif 11%)  : Rp17.989.994
TOTAL PENAWARAN                    : Rp181.535.394
Terbilang: Seratus Delapan Puluh Satu Juta Lima Ratus Tiga Puluh Lima Ribu Tiga Ratus Sembilan Puluh Empat Rupiah

HPS                                : Rp185.000.000
Penawaran terhadap HPS             : 98,13%
Batas 80% HPS                      : Rp148.000.000
Selisih (HPS - penawaran)          : Rp3.464.606

Info:
  - Pagu s.d. Rp15 miliar: paket barang/konstruksi/jasa lainnya pada dasarnya dicadangkan untuk usaha mikro, usaha kecil, dan koperasi (Perpres 16/2018 jo. 46/2025 Pasal 65), kecuali paket yang menuntut kemampuan teknis yang tidak dapat dipenuhi UMK.

Pembulatan: jumlah baris ke rupiah terdekat; PPN dihitung persis dari DPP lalu dibulatkan ke bawah. Belum dicocokkan dengan Coretax/SPSE. Pastikan format & aturan pembulatan mengikuti dokumen pemilihan.
```

## Output script — jadwal
```
JADWAL MUNDUR PENAWARAN - batas unggah Rabu, 14 Oktober 2026 pukul 15:00
Hari ini: Jumat, 25 September 2026 | sisa hari kerja sebelum hari batas: 13
Hari kerja: Senin-Jumat; libur nasional/cuti bersama BELUM dimasukkan (tambahkan --libur)

[ ] Pengumuman   Senin, 28 September 2026
      Unduh dokumen pemilihan dari SPSE; baca syarat kualifikasi, KBLI/SBU, metode evaluasi, HPS, jadwal. Putuskan ikut/tidak (cek kelayakan).
[ ] Penjelasan   Jumat, 2 Oktober 2026
      Ikuti pemberian penjelasan (aanwijzing) di SPSE; ajukan pertanyaan tertulis sebelum sesi ditutup.
[ ] Penjelasan+1 Senin, 5 Oktober 2026
      Cek Berita Acara Pemberian Penjelasan & adendum dokumen pemilihan; sesuaikan rencana penawaran.
[ ] H-7          Senin, 5 Oktober 2026
      Kumpulkan dokumen: NIB & KBLI (OSS), NPWP, status PKP, akta & pengesahan, pengalaman/kontrak, tenaga ahli & peralatan. Cek masa berlaku semua izin/sertifikat.
[ ] H-5          Rabu, 7 Oktober 2026
      Susun dokumen teknis: spesifikasi/brosur, metode pelaksanaan, jadwal, surat dukungan (bila diminta). Minta harga tertulis dari pemasok.
[ ] H-3          Jumat, 9 Oktober 2026
      Finalisasi harga: jalankan cek_penawaran.py (volume x harga, PPN, total, % HPS, terbilang). Siapkan surat penawaran (masa berlaku sesuai dokumen), tanda tangan pihak berwenang.
[ ] H-2          Senin, 12 Oktober 2026
      Pemeriksaan silang: checklist administrasi/teknis/harga; cocokkan nama paket, kode tender, nilai angka vs terbilang; cek format & ukuran file.
[ ] H-1          Selasa, 13 Oktober 2026
      UNGGAH penawaran lengkap di SPSE (jangan tunggu hari terakhir). Simpan bukti/tanda terima unggah; cek file terbaca.
[ ] H            Rabu, 14 Oktober 2026
      Batas akhir unggah pukul 15:00. Hanya perbaikan darurat; unggah ulang paling lambat beberapa jam sebelum batas. Pastikan status penawaran 'terkirim'.

Jadwal resmi selalu yang tertera di SPSE (bisa berubah lewat adendum). Cek ulang setiap hari.
```

## Jawaban agent (mengikuti Format Output SKILL.md)

### Ringkasan paket
| Data | Isi |
|---|---|
| Paket | Pengadaan ATK Dinas Pendidikan Kabupaten — tender barang, pascakualifikasi |
| HPS / pagu | Rp185.000.000 / Rp190.000.000 |
| Kualifikasi usaha | Usaha kecil [cek di LDK] |
| Batas unggah | Rabu, 14 Oktober 2026 pukul 15.00 |
| Jaminan penawaran | Tidak wajib (HPS ≤ Rp10 miliar) — ikuti LDP |

### 1. Kelayakan: **IKUT DENGAN SYARAT**
| Butir | Status | Catatan |
|---|---|---|
| Kualifikasi usaha kecil | ✅ | Pagu ≤ Rp15 M → dicadangkan UMK & koperasi (Pasal 65) |
| KBLI 47612 / 46900 | ❓ | Cocokkan dengan KBLI yang diminta LDK |
| NIB aktif (OSS RBA) | ❓ | Cetak NIB terbaru |
| NPWP & PKP | ✅ | PKP → PPN wajib dicantumkan |
| Pengalaman | ❓ | Cek syarat pengalaman di LDK |
| Daftar hitam | ❓ | Cek portal daftar hitam INAPROC |
| Modal kerja | ❓ | Uang diterima ≈ Rp181,5 jt − PPN Rp17,99 jt (dipungut bendahara) − PPh 22 1,5% × DPP (Rp2.453.181) |
Catatan: HPS Rp185 jt di bawah batas pengadaan langsung barang (Rp200 jt) — pastikan metodenya memang tender (bisa saja tender karena kebijakan instansi).

### 2. Checklist dokumen (B1 + C) — ringkas
Administrasi: [ ] isian kualifikasi SPSE, [ ] surat penawaran (masa berlaku, tanggal, TTD direktur), [ ] pakta integritas, [ ] surat kuasa bila bukan direktur.
Teknis: [ ] spesifikasi ditawarkan ≥ diminta (merek/tipe tiap item), [ ] jadwal kirim ≤ ditetapkan, [ ] surat dukungan/garansi (jika diminta), [ ] bukti TKDN/PDN (jika diminta).
Harga: [ ] rincian 12 baris (volume = dokumen), [ ] total ≤ HPS, [ ] angka = terbilang.
Akhir: [ ] nama paket/kode tender benar, [ ] file terbuka, [ ] kolom unggah benar, [ ] bukti unggah.

### 3. Jadwal mundur — lihat output script (H-7 Senin 5/10 … H-1 Selasa 13/10 unggah). Tidak ada libur nasional Oktober 2026 yang diketahui; pengguna diminta menyebutkan libur daerah bila ada.

### 4. Cek harga
Subtotal (DPP) **Rp163.545.400**, PPN 12% × 11/12 **Rp17.989.994**, total **Rp181.535.394** (Seratus Delapan Puluh Satu Juta Lima Ratus Tiga Puluh Lima Ribu Tiga Ratus Sembilan Puluh Empat Rupiah) = **98,13% HPS** → aman (≤ HPS, ≥ 80%). Selisih ke HPS tipis (Rp3,46 jt) — tidak ada ruang kesalahan hitung.

### 5. Awas gugur (relevan)
1) Surat penawaran tidak ditandatangani/masa berlaku kurang; 2) KBLI tidak sesuai; 3) spesifikasi di bawah minimal (tinta/toner "original" vs kompatibel); 4) total > HPS; 5) angka ≠ terbilang; 6) PPN tidak dicantumkan padahal PKP; 7) unggah mepet.

Asumsi: harga belum termasuk PPN; barang non-mewah; tidak ada libur tambahan.
Dasar aturan (dicek 2026-09-25) + disclaimer: dicantumkan sesuai SKILL.md.

## Verifikasi independen (penguji, Decimal, tanpa membaca kode script)
Jumlah baris: 35.250.000; 14.075.000; 14.220.000; 10.912.500; 41.562.500; 6.900.000; 15.120.000; 6.134.400; 4.312.500; 3.352.000; 5.544.000; 6.162.500 → Σ **163.545.400** ✅. PPN = floor(163.545.400 × 11/12 × 12%) = floor(17.989.994,00) = **17.989.994** ✅. Total **181.535.394** ✅. Terbilang ✅. %HPS = 98,13 ✅. Batas 80% = 148.000.000 ✅. Jadwal: batas Rabu 14/10 → H-1 Sel 13, H-2 Sen 12, H-3 Jum 9, H-5 Rab 7, H-7 Sen 5 ✅; sisa hari kerja (termasuk hari ini) 13 ✅.
