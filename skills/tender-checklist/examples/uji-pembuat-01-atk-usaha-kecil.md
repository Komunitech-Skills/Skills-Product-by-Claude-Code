# Uji pembuat 01 — Tender ATK, CV usaha kecil non-PKP

> Uji oleh **pembuat skill** (bukan penguji independen), 2026-09-25. Output script di bawah adalah hasil eksekusi nyata `scripts/cek_penawaran.py`. Uji independen (01–05, A/B, banding pesaing) belum dilakukan.

## Input pengguna
"CV saya usaha kecil, KBLI 47611, bukan PKP. Mau ikut tender ATK di LPSE kabupaten, HPS Rp45 juta, pagu Rp50 juta, batas unggah 15/10/2026 jam 14.00. Rincian: kertas HVS 150 rim @52.500, tinta 24 botol @Rp1.250.000,00, map 500 @3.750. Di Excel saya totalnya 39.750.000."

## CSV yang dibuat agent (baris total ikut tertempel)
```
Uraian;Volume;Satuan;Harga Satuan
Kertas HVS A4 70 gsm;150;rim;52.500
Tinta printer original hitam;24;botol;Rp1.250.000,00
Map snelhecter plastik;500;buah;3.750
Total;;;39.750.000
```

## Perintah
```
python3 scripts/cek_penawaran.py harga atk.csv --hps 45jt --pagu 50jt
python3 scripts/cek_penawaran.py jadwal --batas "15/10/2026 14.00" --hari-ini 2026-09-25
```

## Output script (apa adanya)
```
RINCIAN PENAWARAN HARGA (hasil hitung script)

 No  Uraian                            Volume  Sat             Harga Satuan              Jumlah
  1  Kertas HVS A4 70 gsm                 150  rim                 Rp52.500         Rp7.875.000
  2  Tinta printer original hitam          24  botol            Rp1.250.000        Rp30.000.000
  3  Map snelhecter plastik               500  buah                 Rp3.750         Rp1.875.000

Subtotal (DPP)                     : Rp39.750.000
PPN (tidak dipungut: bukan PKP)    : Rp0
TOTAL PENAWARAN                    : Rp39.750.000
Terbilang: Tiga Puluh Sembilan Juta Tujuh Ratus Lima Puluh Ribu Rupiah

HPS                                : Rp45.000.000
Penawaran terhadap HPS             : 88,33%
Batas 80% HPS                      : Rp36.000.000
Selisih (HPS - penawaran)          : Rp5.250.000

Info:
  - Baris 'Total' di file (Rp39.750.000) cocok dengan hitungan script.
  - Pagu s.d. Rp15 miliar: paket barang/konstruksi/jasa lainnya pada dasarnya dicadangkan untuk usaha mikro, usaha kecil, dan koperasi (Perpres 16/2018 jo. 46/2025 Pasal 65), kecuali paket yang menuntut kemampuan teknis yang tidak dapat dipenuhi UMK.
  - Tanpa PPN (penyedia bukan PKP). Jika Anda PKP, jalankan ulang dengan --ppn nonmewah.

Baris dilewati:
  - baris 5: 'Total' dianggap baris total/pajak -> tidak dihitung ulang

Pembulatan: jumlah baris ke rupiah terdekat; PPN dihitung persis dari DPP lalu dibulatkan ke bawah. Belum dicocokkan dengan Coretax/SPSE. Pastikan format & aturan pembulatan mengikuti dokumen pemilihan.

JADWAL MUNDUR PENAWARAN - batas unggah Kamis, 15 Oktober 2026 pukul 14:00
Hari ini: Jumat, 25 September 2026 | sisa hari kerja sebelum hari batas: 14
Hari kerja: Senin-Jumat; libur nasional/cuti bersama BELUM dimasukkan (tambahkan --libur)

[ ] H-7          Selasa, 6 Oktober 2026
      Kumpulkan dokumen: NIB & KBLI (OSS), NPWP, status PKP, akta & pengesahan, pengalaman/kontrak, tenaga ahli & peralatan. Cek masa berlaku semua izin/sertifikat.
[ ] H-5          Kamis, 8 Oktober 2026
      Susun dokumen teknis: spesifikasi/brosur, metode pelaksanaan, jadwal, surat dukungan (bila diminta). Minta harga tertulis dari pemasok.
[ ] H-3          Senin, 12 Oktober 2026
      Finalisasi harga: jalankan cek_penawaran.py (volume x harga, PPN, total, % HPS, terbilang). Siapkan surat penawaran (masa berlaku sesuai dokumen), tanda tangan pihak berwenang.
[ ] H-2          Selasa, 13 Oktober 2026
      Pemeriksaan silang: checklist administrasi/teknis/harga; cocokkan nama paket, kode tender, nilai angka vs terbilang; cek format & ukuran file.
[ ] H-1          Rabu, 14 Oktober 2026
      UNGGAH penawaran lengkap di SPSE (jangan tunggu hari terakhir). Simpan bukti/tanda terima unggah; cek file terbaca.
[ ] H            Kamis, 15 Oktober 2026
      Batas akhir unggah pukul 14:00. Hanya perbaikan darurat; unggah ulang paling lambat beberapa jam sebelum batas. Pastikan status penawaran 'terkirim'.

Jadwal resmi selalu yang tertera di SPSE (bisa berubah lewat adendum). Cek ulang setiap hari.
```

## Verifikasi manual (independen dari script)
- 150 × 52.500 = 7.875.000; 24 × 1.250.000 = 30.000.000; 500 × 3.750 = 1.875.000 → 39.750.000 ✔ (sama dengan total Excel pengguna).
- Bukan PKP → PPN 0; total 39.750.000.
- 39.750.000 ÷ 45.000.000 = 0,88333… → 88,33% ✔; 80% × 45.000.000 = 36.000.000 ✔ (penawaran di atas batas, di bawah HPS).
- Kalender: 15/10/2026 Kamis. Mundur hari kerja: 14 (Rabu) H-1, 13 H-2, 12 (Senin) H-3, 9 H-4, 8 (Kamis) H-5, 7 H-6, 6 (Selasa) H-7 ✔.

## Jawaban agent yang diharapkan (ringkas)
1. **Kelayakan: IKUT DENGAN SYARAT** — ✅ usaha kecil & paket < Rp15 M (dicadangkan UMK, Pasal 65); ❓ KBLI 47611 perlu dicocokkan dengan KBLI di LDK; ✅ tanpa PPN karena bukan PKP (jangan mencantumkan PPN); catatan: nilai < Rp200 jt biasanya pengadaan langsung/e-purchasing — pastikan metode di SPSE.
2. Checklist tender barang (administrasi/teknis/harga) dari `references/checklist-dokumen.md` B1 + C.
3. Jadwal H-7 s.d. H seperti output; minta pengguna menyebut libur/cuti bersama bila ada.
4. Harga: tabel di atas, total **Rp39.750.000**, terbilang, 88,33% HPS → aman.
5. Awas gugur: surat penawaran tidak ditandatangani, masa berlaku penawaran kurang, spesifikasi kertas/tinta di bawah syarat, angka ≠ terbilang, unggah mepet.
6. Disclaimer + dasar aturan (dicek 2026-09-25).
