# Uji 01 (Normal) — Pemilik warung OP UMKM 0,5% + 3 karyawan, kalender Okt 2026–Mar 2027 + file .ics

> Penguji independen (Tahap 6), 2026-09-25. Skill disalin ke scratchpad dan script dijalankan dari sana (Python 3, Linux). Output di bawah disalin apa adanya.

> **Catatan pembaruan (2026-10-13):** keluaran di bawah berasal dari uji awal (skill v1.0.0). Keluaran skill versi terbaru (v1.0.7) untuk perintah yang sama ada di bagian "Keluaran skill versi terbaru (v1.0.7)" di akhir berkas. Bedanya: ada baris "Cakupan" dan "Data libur", tanggal bukti potong BPA1 yang jatuh di hari libur menyebut hari kerja sebelumnya (Jumat, 29 Januari 2027), dan keterangan pergeseran memakai titik dua (mis. "15 Nov: Minggu"). Profil ini bukan PKP, jadi memang tidak ada baris unggah faktur pajak keluaran.

## Permintaan pengguna
> "Saya punya warung sembako, bayar pajak 0,5% yang UMKM itu, karyawan 3 orang. Tolong bikinin jadwal pajak dari Oktober sampai Maret tahun depan, sekalian file buat Google Calendar di HP."

## Langkah agent
1. Profil: orang pribadi + PPh final 0,5% → `op-umkm`; punya karyawan → `pemberi-kerja`. Asumsi disebut: belum PKP, tidak memotong PPh 23/4(2), tahun buku = kalender.
2. Perintah:
```bash
python3 scripts/kalender_pajak.py --profil op-umkm,pemberi-kerja --tahun 2026 --bulan-mulai 10 --jumlah-bulan 6
python3 scripts/kalender_pajak.py --profil op-umkm,pemberi-kerja --tahun 2026 --bulan-mulai Okt --jumlah-bulan 6 --format ics --keluar kalender-pajak.ics
```
Kode keluar 0 untuk keduanya; `Tersimpan: kalender-pajak.ics (20 tenggat)`.

## Output script (tabel, apa adanya)
## Kalender Pajak Oktober 2026 - Maret 2027 - op-umkm, pemberi-kerja

Kewajiban: PPh Final UMKM 0,5% (PP 55/2022), SPT Tahunan PPh Orang Pribadi, PPh 21/26 (pemberi kerja), Bukti potong PPh 21 tahunan (BPA1, dulu 1721-A1)

| Tanggal | Kegiatan | Keterangan |
|---|---|---|
| Kamis, 15 Oktober 2026 | SETOR PPh Final UMKM 0,5% (PP 55/2022) masa Sep 2026 | - |
| Kamis, 15 Oktober 2026 | SETOR PPh 21/26 (pemberi kerja) masa Sep 2026 | - |
| Selasa, 20 Oktober 2026 | LAPOR SPT Masa PPh 21/26 masa Sep 2026 | - |
| Senin, 16 November 2026 | SETOR PPh Final UMKM 0,5% (PP 55/2022) masa Okt 2026 | bergeser dari 15 Nov (15 Nov Minggu) |
| Senin, 16 November 2026 | SETOR PPh 21/26 (pemberi kerja) masa Okt 2026 | bergeser dari 15 Nov (15 Nov Minggu) |
| Jumat, 20 November 2026 | LAPOR SPT Masa PPh 21/26 masa Okt 2026 | - |
| Selasa, 15 Desember 2026 | SETOR PPh Final UMKM 0,5% (PP 55/2022) masa Nov 2026 | - |
| Selasa, 15 Desember 2026 | SETOR PPh 21/26 (pemberi kerja) masa Nov 2026 | - |
| Senin, 21 Desember 2026 | LAPOR SPT Masa PPh 21/26 masa Nov 2026 | bergeser dari 20 Des (20 Des Minggu) |
| Jumat, 15 Januari 2027 | SETOR PPh Final UMKM 0,5% (PP 55/2022) masa Des 2026 | - |
| Jumat, 15 Januari 2027 | SETOR PPh 21/26 (pemberi kerja) masa Des 2026 | - |
| Rabu, 20 Januari 2027 | LAPOR SPT Masa PPh 21/26 masa Des 2026 | - |
| Minggu, 31 Januari 2027 | BERIKAN bukti potong BPA1 ke karyawan tahun pajak 2026 | jatuh pada hari libur (Minggu) dan TIDAK bergeser - selesaikan hari kerja sebelumnya |
| Senin, 15 Februari 2027 | SETOR PPh Final UMKM 0,5% (PP 55/2022) masa Jan 2027 | - |
| Senin, 15 Februari 2027 | SETOR PPh 21/26 (pemberi kerja) masa Jan 2027 | - |
| Senin, 22 Februari 2027 | LAPOR SPT Masa PPh 21/26 masa Jan 2027 | bergeser dari 20 Feb (20 Feb Sabtu; 21 Feb Minggu) |
| Selasa, 16 Maret 2027 | SETOR PPh Final UMKM 0,5% (PP 55/2022) masa Feb 2027 | bergeser dari 15 Mar (15 Mar Cuti bersama Idulfitri 1448 H) |
| Selasa, 16 Maret 2027 | SETOR PPh 21/26 (pemberi kerja) masa Feb 2027 | bergeser dari 15 Mar (15 Mar Cuti bersama Idulfitri 1448 H) |
| Senin, 22 Maret 2027 | LAPOR SPT Masa PPh 21/26 masa Feb 2027 | bergeser dari 20 Mar (20 Mar Sabtu; 21 Mar Minggu) |
| Rabu, 31 Maret 2027 | LAPOR SPT Tahunan PPh Orang Pribadi tahun pajak 2026 | - |

**Catatan per kewajiban**
- PPh Final UMKM 0,5% (PP 55/2022): Setor yang tervalidasi dianggap sudah lapor SPT Masa (PMK 81/2024). Hanya bila ada PPh terutang: orang pribadi tidak setor selama omzet kumulatif setahun masih <= Rp500 juta. Besarannya: skill pph-final-umkm.
- SPT Tahunan PPh Orang Pribadi: Paling lambat 3 bulan setelah akhir tahun pajak. Kurang bayar (PPh 29) dilunasi SEBELUM SPT dikirim. Tenggat SPT Tahunan TIDAK bergeser walau jatuh di hari libur.
- PPh 21/26 (pemberi kerja): Besarannya: skill pph21-ter. Bukti potong dibuat di Coretax.
- Bukti potong PPh 21 tahunan (BPA1, dulu 1721-A1): Paling lama 1 bulan setelah masa pajak terakhir (PER-2/PJ/2024). Karyawan butuh ini untuk SPT Tahunan. Tanggal ditampilkan tanpa pergeseran (PERLU REVIEW).

**Aturan pergeseran:** tenggat setor & lapor bulanan yang jatuh pada Sabtu, Minggu, libur nasional, atau cuti bersama bergeser ke hari kerja berikutnya (PMK 81/2024). Tenggat SPT Tahunan tidak bergeser. Sebaiknya setor/lapor 2-3 hari sebelum tenggat.

_Bukan nasihat pajak. Dasar: PMK 81/2024 (berlaku 1 Jan 2025), PP 55/2022 jo. PP 20/2026, PER-2/PJ/2024, SKB 3 Menteri libur nasional & cuti bersama; dicek 2026-09-25 dari sumber sekunder (naskah resmi belum dibaca langsung). DJP kadang memundurkan tenggat lewat pengumuman khusus - cek pengumuman DJP terbaru (pajak.go.id, Kring Pajak 1500200). Pembulatan/perhitungan pajak tidak dilakukan skill ini dan belum dicocokkan dengan Coretax. Untuk kasus Anda, konsultasikan dengan konsultan pajak atau Account Representative (AR)._

## Cuplikan file .ics (1 acara)
```
BEGIN:VEVENT
UID:effc6647e8542fe585cd@kalender-pajak.komunitech
DTSTAMP:20260925T082005Z
DTSTART;VALUE=DATE:20261015
DTEND;VALUE=DATE:20261016
SUMMARY:Pajak: SETOR PPh Final UMKM 0\,5% (PP 55/2022) masa Sep 2026
DESCRIPTION:SETOR PPh Final UMKM 0\,5% (PP 55/2022) masa Sep 2026\nMasa: Se
 p 2026\nSetor yang tervalidasi dianggap sudah lapor SPT Masa (PMK 81/2024)
 . Hanya bila ada PPh terutang: orang pribadi tidak setor selama omzet kumu
 latif setahun masih <= Rp500 juta. Besarannya: skill pph-final-umkm.\nTida
 k bergeser.\nTenggat normal: Kamis\, 15 Oktober 2026\n\nBukan nasihat paja
 k. Dasar: PMK 81/2024 (berlaku 1 Jan 2025)\, PP 55/2022 jo. PP 20/2026\, P
 ER-2/PJ/2024\, SKB 3 Menteri libur nasional & cuti bersama\; dicek 2026-09
 -25 dari sumber sekunder (naskah resmi belum dibaca langsung). DJP kadang 
 memundurkan tenggat lewat pengumuman khusus - cek pengumuman DJP terbaru (
 pajak.go.id\, Kring Pajak 1500200). Pembulatan/perhitungan pajak tidak dil
 akukan skill ini dan belum dicocokkan dengan Coretax. Untuk kasus Anda\, k
 onsultasikan dengan konsultan pajak atau Account Representative (AR).
CATEGORIES:Pajak
TRANSP:TRANSPARENT
BEGIN:VALARM
ACTION:DISPLAY
TRIGGER:-P2DT15H
DESCRIPTION:3 hari lagi: SETOR PPh Final UMKM 0\,5% (PP 55/2022) masa Sep 2
 026
END:VALARM
BEGIN:VALARM
ACTION:DISPLAY
TRIGGER:-PT15H
DESCRIPTION:besok: SETOR PPh Final UMKM 0\,5% (PP 55/2022) masa Sep 2026
```
Validasi (parser penguji): 20 VEVENT, 20 UID unik & stabil antar-run, semua baris CRLF, ≤75 oktet, lipatan tidak memotong karakter UTF-8, DTSTART;VALUE=DATE + DTEND = +1 hari, 2 VALARM per acara (−P2DT15H = H-3 09.00, −PT15H = H-1 09.00), koma/titik koma di-escape.

## Jawaban agent ke pengguna (ringkas)
- Tabel di atas + penjelasan: "Setor PPh 0,5% dan PPh 21 masa Oktober bergeser ke Senin 16 November karena 15 November hari Minggu. Setor masa Februari 2027 bergeser ke Selasa 16 Maret 2027 karena 15 Maret cuti bersama Idulfitri."
- "Bukti potong BPA1 untuk karyawan paling lambat 31 Januari 2027 (hari Minggu) — tidak bergeser, jadi berikan Jumat 29 Januari."
- "PPh 0,5% hanya disetor bila omzet setahun sudah lewat Rp500 juta. Besarannya bisa dihitung dengan skill pph-final-umkm; PPh 21 dengan pph21-ter."
- Cara impor .ics: Google Calendar (web) → Setelan → Impor & ekspor → Impor.
- Disclaimer script disertakan.

## Penilaian penguji
- Semua 20 tanggal cocok dengan penghitung independen penguji (lihat HASIL-UJI.md §3).
- Pergeseran dijelaskan per baris; SPT Tahunan OP 31 Mar 2027 (Rabu) benar.
- Catatan: pengingat VALARM kemungkinan **tidak ikut** bila diimpor ke Google Calendar (terutama ke kalender non-utama) — klaim README "pengingat H-3/H-1 ikut terpasang" perlu dilunakkan (temuan P2).
- Hasil: **LULUS**.

## Keluaran skill versi terbaru (v1.0.7) — perintah sama, data fiktif

> Dijalankan ulang pada 2026-10-13 dengan perintah dan tanggal acuan yang sama seperti di atas. Profil dan tanggal acuan ini fiktif (contoh), tidak memakai data pembeli. Keluaran disalin apa adanya dari `scripts/kalender_pajak.py`.

Perintah:
```bash
python3 scripts/kalender_pajak.py --profil op-umkm,pemberi-kerja --tahun 2026 --bulan-mulai 10 --jumlah-bulan 6
```

## Kalender Pajak Oktober 2026 - Maret 2027 - op-umkm, pemberi-kerja

Kewajiban: PPh Final UMKM 0,5% (PP 55/2022), SPT Tahunan PPh Orang Pribadi, PPh 21/26 (pemberi kerja), Bukti potong PPh 21 tahunan (BPA1, dulu 1721-A1)

Cakupan: tenggat yang **jatuh** pada Kamis, 1 Oktober 2026 s.d. Rabu, 31 Maret 2027 (termasuk tenggat masa pajak bulan sebelum periode). Tenggat masa pajak Maret 2027 dan sesudahnya jatuh setelah periode ini; begitu juga kewajiban tahunan untuk tahun pajak 2027 - buat kalender periode berikutnya untuk melihatnya.
Data libur: SKB 3 Menteri libur nasional & cuti bersama 2026, 2027 (file: libur-nasional-2026.csv, libur-nasional-2027.csv).

| Tanggal | Kegiatan | Keterangan |
|---|---|---|
| Kamis, 15 Oktober 2026 | SETOR PPh Final UMKM 0,5% (PP 55/2022) masa Sep 2026 | - |
| Kamis, 15 Oktober 2026 | SETOR PPh 21/26 (pemberi kerja) masa Sep 2026 | - |
| Selasa, 20 Oktober 2026 | LAPOR SPT Masa PPh 21/26 masa Sep 2026 | - |
| Senin, 16 November 2026 | SETOR PPh Final UMKM 0,5% (PP 55/2022) masa Okt 2026 | bergeser dari 15 Nov (15 Nov: Minggu) |
| Senin, 16 November 2026 | SETOR PPh 21/26 (pemberi kerja) masa Okt 2026 | bergeser dari 15 Nov (15 Nov: Minggu) |
| Jumat, 20 November 2026 | LAPOR SPT Masa PPh 21/26 masa Okt 2026 | - |
| Selasa, 15 Desember 2026 | SETOR PPh Final UMKM 0,5% (PP 55/2022) masa Nov 2026 | - |
| Selasa, 15 Desember 2026 | SETOR PPh 21/26 (pemberi kerja) masa Nov 2026 | - |
| Senin, 21 Desember 2026 | LAPOR SPT Masa PPh 21/26 masa Nov 2026 | bergeser dari 20 Des (20 Des: Minggu) |
| Jumat, 15 Januari 2027 | SETOR PPh Final UMKM 0,5% (PP 55/2022) masa Des 2026 | - |
| Jumat, 15 Januari 2027 | SETOR PPh 21/26 (pemberi kerja) masa Des 2026 | - |
| Rabu, 20 Januari 2027 | LAPOR SPT Masa PPh 21/26 masa Des 2026 | - |
| Minggu, 31 Januari 2027 | BERIKAN bukti potong BPA1 ke karyawan tahun pajak 2026 | jatuh pada hari libur (Minggu) dan TIDAK bergeser - selesaikan paling lambat hari kerja sebelumnya: Jumat, 29 Januari 2027 |
| Senin, 15 Februari 2027 | SETOR PPh Final UMKM 0,5% (PP 55/2022) masa Jan 2027 | - |
| Senin, 15 Februari 2027 | SETOR PPh 21/26 (pemberi kerja) masa Jan 2027 | - |
| Senin, 22 Februari 2027 | LAPOR SPT Masa PPh 21/26 masa Jan 2027 | bergeser dari 20 Feb (20 Feb: Sabtu; 21 Feb: Minggu) |
| Selasa, 16 Maret 2027 | SETOR PPh Final UMKM 0,5% (PP 55/2022) masa Feb 2027 | bergeser dari 15 Mar (15 Mar: Cuti bersama Idulfitri 1448 H) |
| Selasa, 16 Maret 2027 | SETOR PPh 21/26 (pemberi kerja) masa Feb 2027 | bergeser dari 15 Mar (15 Mar: Cuti bersama Idulfitri 1448 H) |
| Senin, 22 Maret 2027 | LAPOR SPT Masa PPh 21/26 masa Feb 2027 | bergeser dari 20 Mar (20 Mar: Sabtu; 21 Mar: Minggu) |
| Rabu, 31 Maret 2027 | LAPOR SPT Tahunan PPh Orang Pribadi tahun pajak 2026 | - |

**Catatan per kewajiban**
- PPh Final UMKM 0,5% (PP 55/2022): Setor yang tervalidasi dianggap sudah lapor SPT Masa (PMK 81/2024). Hanya bila ada PPh terutang: orang pribadi tidak setor selama omzet kumulatif setahun masih <= Rp500 juta. Besarannya: skill pph-final-umkm (bila terpasang).
- SPT Tahunan PPh Orang Pribadi: Paling lambat 3 bulan setelah akhir tahun pajak. Kurang bayar (PPh 29) dilunasi SEBELUM SPT dikirim. Tidak bergeser meski hari libur (PMK 81/2024 Ps. 169); lapor lebih awal. DJP kadang memberi perpanjangan khusus lewat pengumuman.
- PPh 21/26 (pemberi kerja): Besarannya: skill pph21-ter (bila terpasang). Bukti potong dibuat di Coretax.
- Bukti potong PPh 21 tahunan (BPA1, dulu 1721-A1): Paling lama 1 bulan setelah masa pajak terakhir (PER-2/PJ/2024). Karyawan butuh ini untuk SPT Tahunan. Tanggal ditampilkan tanpa pergeseran (PERLU REVIEW).

**Aturan pergeseran:** tenggat setor & lapor bulanan yang jatuh pada Sabtu, Minggu, libur nasional, atau cuti bersama bergeser ke hari kerja berikutnya (PMK 81/2024). SPT Tahunan dan batas unggah faktur pajak ditampilkan tanpa pergeseran (lebih aman bila ternyata boleh bergeser); bila jatuh di hari libur, disebutkan hari kerja sebelumnya. Sebaiknya setor/lapor 2-3 hari sebelum tenggat.

_Bukan nasihat pajak. Dasar: PMK 81/2024 (berlaku 1 Jan 2025), PP 55/2022 jo. PP 20/2026, PER-2/PJ/2024, PER-11/PJ/2025, SKB 3 Menteri libur nasional & cuti bersama; dicek 2026-09-26 (pasal tenggat PMK 81/2024 & PER-11/PJ/2025 dicocokkan dengan naskah resmi di pajak.go.id; sebagian butir lain dari sumber sekunder). DJP kadang memundurkan tenggat lewat pengumuman khusus - cek pengumuman DJP terbaru (pajak.go.id, Kring Pajak 1500200). Pembulatan/perhitungan pajak tidak dilakukan skill ini dan belum dicocokkan dengan Coretax. Untuk kasus Anda, konsultasikan dengan konsultan pajak atau Account Representative (AR)._
