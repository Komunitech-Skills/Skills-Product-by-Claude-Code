# Uji 03 (Normal) — PT kecil: kalender setahun 2027 termasuk SPT Tahunan Badan

> Penguji independen, 2026-09-25.

## Permintaan pengguna
> "PT saya kecil, sudah PKP, karyawan 8 orang, sering bayar sewa dan jasa yang dipotong pajak. Minta kalender pajak lengkap tahun 2027, termasuk SPT Tahunan badan. Kalau bisa bentuk checklist per bulan buat admin."

## Langkah agent
Profil: `badan-pkp,pemberi-kerja,pemotong`. Asumsi: PT tarif umum, tahun buku Januari–Desember.
```bash
python3 scripts/kalender_pajak.py --profil badan-pkp,pemberi-kerja,pemotong --tahun 2027
python3 scripts/kalender_pajak.py --profil badan-pkp,pemberi-kerja,pemotong --tahun 2027 --format checklist
```
Kode keluar 0; 73 baris tenggat.

## Output script — tabel (apa adanya)
## Kalender Pajak Januari 2027 - Desember 2027 - badan-pkp, pemberi-kerja, pemotong

Kewajiban: PPN (PKP), PPh 25 (angsuran bulanan), SPT Tahunan PPh Badan, PPh 21/26 (pemberi kerja), Bukti potong PPh 21 tahunan (BPA1, dulu 1721-A1), PPh Unifikasi (PPh 4(2), 15, 22, 23, 26 non-pegawai)

| Tanggal | Kegiatan | Keterangan |
|---|---|---|
| Jumat, 15 Januari 2027 | SETOR PPh 21/26 (pemberi kerja) masa Des 2026 | - |
| Jumat, 15 Januari 2027 | SETOR PPh Unifikasi (PPh 4(2), 15, 22, 23, 26 non-pegawai) masa Des 2026 | - |
| Jumat, 15 Januari 2027 | SETOR PPh 25 (angsuran bulanan) masa Des 2026 | - |
| Rabu, 20 Januari 2027 | LAPOR SPT Masa PPh 21/26 masa Des 2026 | - |
| Rabu, 20 Januari 2027 | LAPOR SPT Masa PPh Unifikasi masa Des 2026 | - |
| Minggu, 31 Januari 2027 | BERIKAN bukti potong BPA1 ke karyawan tahun pajak 2026 | jatuh pada hari libur (Minggu) dan TIDAK bergeser - selesaikan hari kerja sebelumnya |
| Senin, 1 Februari 2027 | SETOR & LAPOR PPN masa Des 2026 | bergeser dari 31 Jan (31 Jan Minggu) |
| Senin, 15 Februari 2027 | SETOR PPh 21/26 (pemberi kerja) masa Jan 2027 | - |
| Senin, 15 Februari 2027 | SETOR PPh Unifikasi (PPh 4(2), 15, 22, 23, 26 non-pegawai) masa Jan 2027 | - |
| Senin, 15 Februari 2027 | SETOR PPh 25 (angsuran bulanan) masa Jan 2027 | - |
| Senin, 22 Februari 2027 | LAPOR SPT Masa PPh 21/26 masa Jan 2027 | bergeser dari 20 Feb (20 Feb Sabtu; 21 Feb Minggu) |
| Senin, 22 Februari 2027 | LAPOR SPT Masa PPh Unifikasi masa Jan 2027 | bergeser dari 20 Feb (20 Feb Sabtu; 21 Feb Minggu) |
| Senin, 1 Maret 2027 | SETOR & LAPOR PPN masa Jan 2027 | bergeser dari 28 Feb (28 Feb Minggu) |
| Selasa, 16 Maret 2027 | SETOR PPh 21/26 (pemberi kerja) masa Feb 2027 | bergeser dari 15 Mar (15 Mar Cuti bersama Idulfitri 1448 H) |
| Selasa, 16 Maret 2027 | SETOR PPh Unifikasi (PPh 4(2), 15, 22, 23, 26 non-pegawai) masa Feb 2027 | bergeser dari 15 Mar (15 Mar Cuti bersama Idulfitri 1448 H) |
| Selasa, 16 Maret 2027 | SETOR PPh 25 (angsuran bulanan) masa Feb 2027 | bergeser dari 15 Mar (15 Mar Cuti bersama Idulfitri 1448 H) |
| Senin, 22 Maret 2027 | LAPOR SPT Masa PPh 21/26 masa Feb 2027 | bergeser dari 20 Mar (20 Mar Sabtu; 21 Mar Minggu) |
| Senin, 22 Maret 2027 | LAPOR SPT Masa PPh Unifikasi masa Feb 2027 | bergeser dari 20 Mar (20 Mar Sabtu; 21 Mar Minggu) |
| Rabu, 31 Maret 2027 | SETOR & LAPOR PPN masa Feb 2027 | - |
| Kamis, 15 April 2027 | SETOR PPh 21/26 (pemberi kerja) masa Mar 2027 | - |
| Kamis, 15 April 2027 | SETOR PPh Unifikasi (PPh 4(2), 15, 22, 23, 26 non-pegawai) masa Mar 2027 | - |
| Kamis, 15 April 2027 | SETOR PPh 25 (angsuran bulanan) masa Mar 2027 | - |
| Selasa, 20 April 2027 | LAPOR SPT Masa PPh 21/26 masa Mar 2027 | - |
| Selasa, 20 April 2027 | LAPOR SPT Masa PPh Unifikasi masa Mar 2027 | - |
| Jumat, 30 April 2027 | SETOR & LAPOR PPN masa Mar 2027 | - |
| Jumat, 30 April 2027 | LAPOR SPT Tahunan PPh Badan tahun pajak 2026 | - |
| Jumat, 21 Mei 2027 | SETOR PPh 21/26 (pemberi kerja) masa Apr 2027 | bergeser dari 15 Mei (15 Mei Sabtu; 16 Mei Minggu; 17 Mei Iduladha 1448 H; 18 Mei Cuti bersama Iduladha 1448 H; 19 Mei Cuti bersama Hari Raya Waisak 2571 BE; 20 Mei Hari Raya Waisak 2571 BE) |
| Jumat, 21 Mei 2027 | SETOR PPh Unifikasi (PPh 4(2), 15, 22, 23, 26 non-pegawai) masa Apr 2027 | bergeser dari 15 Mei (15 Mei Sabtu; 16 Mei Minggu; 17 Mei Iduladha 1448 H; 18 Mei Cuti bersama Iduladha 1448 H; 19 Mei Cuti bersama Hari Raya Waisak 2571 BE; 20 Mei Hari Raya Waisak 2571 BE) |
| Jumat, 21 Mei 2027 | SETOR PPh 25 (angsuran bulanan) masa Apr 2027 | bergeser dari 15 Mei (15 Mei Sabtu; 16 Mei Minggu; 17 Mei Iduladha 1448 H; 18 Mei Cuti bersama Iduladha 1448 H; 19 Mei Cuti bersama Hari Raya Waisak 2571 BE; 20 Mei Hari Raya Waisak 2571 BE) |
| Jumat, 21 Mei 2027 | LAPOR SPT Masa PPh 21/26 masa Apr 2027 | bergeser dari 20 Mei (20 Mei Hari Raya Waisak 2571 BE) |
| Jumat, 21 Mei 2027 | LAPOR SPT Masa PPh Unifikasi masa Apr 2027 | bergeser dari 20 Mei (20 Mei Hari Raya Waisak 2571 BE) |
| Senin, 31 Mei 2027 | SETOR & LAPOR PPN masa Apr 2027 | - |
| Selasa, 15 Juni 2027 | SETOR PPh 21/26 (pemberi kerja) masa Mei 2027 | - |
| Selasa, 15 Juni 2027 | SETOR PPh Unifikasi (PPh 4(2), 15, 22, 23, 26 non-pegawai) masa Mei 2027 | - |
| Selasa, 15 Juni 2027 | SETOR PPh 25 (angsuran bulanan) masa Mei 2027 | - |
| Senin, 21 Juni 2027 | LAPOR SPT Masa PPh 21/26 masa Mei 2027 | bergeser dari 20 Jun (20 Jun Minggu) |
| Senin, 21 Juni 2027 | LAPOR SPT Masa PPh Unifikasi masa Mei 2027 | bergeser dari 20 Jun (20 Jun Minggu) |
| Rabu, 30 Juni 2027 | SETOR & LAPOR PPN masa Mei 2027 | - |
| Kamis, 15 Juli 2027 | SETOR PPh 21/26 (pemberi kerja) masa Jun 2027 | - |
| Kamis, 15 Juli 2027 | SETOR PPh Unifikasi (PPh 4(2), 15, 22, 23, 26 non-pegawai) masa Jun 2027 | - |
| Kamis, 15 Juli 2027 | SETOR PPh 25 (angsuran bulanan) masa Jun 2027 | - |
| Selasa, 20 Juli 2027 | LAPOR SPT Masa PPh 21/26 masa Jun 2027 | - |
| Selasa, 20 Juli 2027 | LAPOR SPT Masa PPh Unifikasi masa Jun 2027 | - |
| Senin, 2 Agustus 2027 | SETOR & LAPOR PPN masa Jun 2027 | bergeser dari 31 Jul (31 Jul Sabtu; 1 Agu Minggu) |
| Senin, 16 Agustus 2027 | SETOR PPh 21/26 (pemberi kerja) masa Jul 2027 | bergeser dari 15 Agu (15 Agu Minggu) |
| Senin, 16 Agustus 2027 | SETOR PPh Unifikasi (PPh 4(2), 15, 22, 23, 26 non-pegawai) masa Jul 2027 | bergeser dari 15 Agu (15 Agu Minggu) |
| Senin, 16 Agustus 2027 | SETOR PPh 25 (angsuran bulanan) masa Jul 2027 | bergeser dari 15 Agu (15 Agu Minggu) |
| Jumat, 20 Agustus 2027 | LAPOR SPT Masa PPh 21/26 masa Jul 2027 | - |
| Jumat, 20 Agustus 2027 | LAPOR SPT Masa PPh Unifikasi masa Jul 2027 | - |
| Selasa, 31 Agustus 2027 | SETOR & LAPOR PPN masa Jul 2027 | - |
| Rabu, 15 September 2027 | SETOR PPh 21/26 (pemberi kerja) masa Agu 2027 | - |
| Rabu, 15 September 2027 | SETOR PPh Unifikasi (PPh 4(2), 15, 22, 23, 26 non-pegawai) masa Agu 2027 | - |
| Rabu, 15 September 2027 | SETOR PPh 25 (angsuran bulanan) masa Agu 2027 | - |
| Senin, 20 September 2027 | LAPOR SPT Masa PPh 21/26 masa Agu 2027 | - |
| Senin, 20 September 2027 | LAPOR SPT Masa PPh Unifikasi masa Agu 2027 | - |
| Kamis, 30 September 2027 | SETOR & LAPOR PPN masa Agu 2027 | - |
| Jumat, 15 Oktober 2027 | SETOR PPh 21/26 (pemberi kerja) masa Sep 2027 | - |
| Jumat, 15 Oktober 2027 | SETOR PPh Unifikasi (PPh 4(2), 15, 22, 23, 26 non-pegawai) masa Sep 2027 | - |
| Jumat, 15 Oktober 2027 | SETOR PPh 25 (angsuran bulanan) masa Sep 2027 | - |
| Rabu, 20 Oktober 2027 | LAPOR SPT Masa PPh 21/26 masa Sep 2027 | - |
| Rabu, 20 Oktober 2027 | LAPOR SPT Masa PPh Unifikasi masa Sep 2027 | - |
| Senin, 1 November 2027 | SETOR & LAPOR PPN masa Sep 2027 | bergeser dari 31 Okt (31 Okt Minggu) |
| Senin, 15 November 2027 | SETOR PPh 21/26 (pemberi kerja) masa Okt 2027 | - |
| Senin, 15 November 2027 | SETOR PPh Unifikasi (PPh 4(2), 15, 22, 23, 26 non-pegawai) masa Okt 2027 | - |
| Senin, 15 November 2027 | SETOR PPh 25 (angsuran bulanan) masa Okt 2027 | - |
| Senin, 22 November 2027 | LAPOR SPT Masa PPh 21/26 masa Okt 2027 | bergeser dari 20 Nov (20 Nov Sabtu; 21 Nov Minggu) |
| Senin, 22 November 2027 | LAPOR SPT Masa PPh Unifikasi masa Okt 2027 | bergeser dari 20 Nov (20 Nov Sabtu; 21 Nov Minggu) |
| Selasa, 30 November 2027 | SETOR & LAPOR PPN masa Okt 2027 | - |
| Rabu, 15 Desember 2027 | SETOR PPh 21/26 (pemberi kerja) masa Nov 2027 | - |
| Rabu, 15 Desember 2027 | SETOR PPh Unifikasi (PPh 4(2), 15, 22, 23, 26 non-pegawai) masa Nov 2027 | - |
| Rabu, 15 Desember 2027 | SETOR PPh 25 (angsuran bulanan) masa Nov 2027 | - |
| Senin, 20 Desember 2027 | LAPOR SPT Masa PPh 21/26 masa Nov 2027 | - |
| Senin, 20 Desember 2027 | LAPOR SPT Masa PPh Unifikasi masa Nov 2027 | - |
| Jumat, 31 Desember 2027 | SETOR & LAPOR PPN masa Nov 2027 | - |

**Catatan per kewajiban**
- PPN (PKP): Setor paling lambat akhir bulan berikutnya DAN sebelum SPT Masa PPN dikirim. PKP tetap lapor walau nihil. Besarannya: skill hitung-ppn.
- PPh 25 (angsuran bulanan): Setor yang tervalidasi dianggap sudah lapor SPT Masa PPh 25 (PERLU REVIEW). Angsuran nihil tidak perlu setor.
- SPT Tahunan PPh Badan: Paling lambat akhir bulan ke-4 setelah akhir tahun buku (dianggap tahun buku Januari-Desember). Kurang bayar (PPh 29) dilunasi SEBELUM SPT dikirim. Tidak bergeser walau jatuh di hari libur.
- PPh 21/26 (pemberi kerja): Besarannya: skill pph21-ter. Bukti potong dibuat di Coretax.
- Bukti potong PPh 21 tahunan (BPA1, dulu 1721-A1): Paling lama 1 bulan setelah masa pajak terakhir (PER-2/PJ/2024). Karyawan butuh ini untuk SPT Tahunan. Tanggal ditampilkan tanpa pergeseran (PERLU REVIEW).
- PPh Unifikasi (PPh 4(2), 15, 22, 23, 26 non-pegawai): Untuk pemotong/pemungut, mis. potong PPh 23 jasa atau PPh 4(2) sewa.

**Aturan pergeseran:** tenggat setor & lapor bulanan yang jatuh pada Sabtu, Minggu, libur nasional, atau cuti bersama bergeser ke hari kerja berikutnya (PMK 81/2024). Tenggat SPT Tahunan tidak bergeser. Sebaiknya setor/lapor 2-3 hari sebelum tenggat.

_Bukan nasihat pajak. Dasar: PMK 81/2024 (berlaku 1 Jan 2025), PP 55/2022 jo. PP 20/2026, PER-2/PJ/2024, SKB 3 Menteri libur nasional & cuti bersama; dicek 2026-09-25 dari sumber sekunder (naskah resmi belum dibaca langsung). DJP kadang memundurkan tenggat lewat pengumuman khusus - cek pengumuman DJP terbaru (pajak.go.id, Kring Pajak 1500200). Pembulatan/perhitungan pajak tidak dilakukan skill ini dan belum dicocokkan dengan Coretax. Untuk kasus Anda, konsultasikan dengan konsultan pajak atau Account Representative (AR)._

## Output script — checklist (cuplikan Jan–Mei)
## Checklist Pajak Bulanan - badan-pkp, pemberi-kerja, pemotong


### Januari 2027
- [ ] **Jum 15 Jan** - SETOR PPh 21/26 (pemberi kerja) masa Des 2026
- [ ] **Jum 15 Jan** - SETOR PPh Unifikasi (PPh 4(2), 15, 22, 23, 26 non-pegawai) masa Des 2026
- [ ] **Jum 15 Jan** - SETOR PPh 25 (angsuran bulanan) masa Des 2026
- [ ] **Rab 20 Jan** - LAPOR SPT Masa PPh 21/26 masa Des 2026
- [ ] **Rab 20 Jan** - LAPOR SPT Masa PPh Unifikasi masa Des 2026
- [ ] **Min 31 Jan** - BERIKAN bukti potong BPA1 ke karyawan tahun pajak 2026 (jatuh pada hari libur (Minggu) dan TIDAK bergeser - selesaikan hari kerja sebelumnya)

### Februari 2027
- [ ] **Sen 1 Feb** - SETOR & LAPOR PPN masa Des 2026 (bergeser dari 31 Jan (31 Jan Minggu))
- [ ] **Sen 15 Feb** - SETOR PPh 21/26 (pemberi kerja) masa Jan 2027
- [ ] **Sen 15 Feb** - SETOR PPh Unifikasi (PPh 4(2), 15, 22, 23, 26 non-pegawai) masa Jan 2027
- [ ] **Sen 15 Feb** - SETOR PPh 25 (angsuran bulanan) masa Jan 2027
- [ ] **Sen 22 Feb** - LAPOR SPT Masa PPh 21/26 masa Jan 2027 (bergeser dari 20 Feb (20 Feb Sabtu; 21 Feb Minggu))
- [ ] **Sen 22 Feb** - LAPOR SPT Masa PPh Unifikasi masa Jan 2027 (bergeser dari 20 Feb (20 Feb Sabtu; 21 Feb Minggu))

### Maret 2027
- [ ] **Sen 1 Mar** - SETOR & LAPOR PPN masa Jan 2027 (bergeser dari 28 Feb (28 Feb Minggu))
- [ ] **Sel 16 Mar** - SETOR PPh 21/26 (pemberi kerja) masa Feb 2027 (bergeser dari 15 Mar (15 Mar Cuti bersama Idulfitri 1448 H))
- [ ] **Sel 16 Mar** - SETOR PPh Unifikasi (PPh 4(2), 15, 22, 23, 26 non-pegawai) masa Feb 2027 (bergeser dari 15 Mar (15 Mar Cuti bersama Idulfitri 1448 H))
- [ ] **Sel 16 Mar** - SETOR PPh 25 (angsuran bulanan) masa Feb 2027 (bergeser dari 15 Mar (15 Mar Cuti bersama Idulfitri 1448 H))
- [ ] **Sen 22 Mar** - LAPOR SPT Masa PPh 21/26 masa Feb 2027 (bergeser dari 20 Mar (20 Mar Sabtu; 21 Mar Minggu))
- [ ] **Sen 22 Mar** - LAPOR SPT Masa PPh Unifikasi masa Feb 2027 (bergeser dari 20 Mar (20 Mar Sabtu; 21 Mar Minggu))
- [ ] **Rab 31 Mar** - SETOR & LAPOR PPN masa Feb 2027

### April 2027
- [ ] **Kam 15 Apr** - SETOR PPh 21/26 (pemberi kerja) masa Mar 2027
- [ ] **Kam 15 Apr** - SETOR PPh Unifikasi (PPh 4(2), 15, 22, 23, 26 non-pegawai) masa Mar 2027
- [ ] **Kam 15 Apr** - SETOR PPh 25 (angsuran bulanan) masa Mar 2027
- [ ] **Sel 20 Apr** - LAPOR SPT Masa PPh 21/26 masa Mar 2027
- [ ] **Sel 20 Apr** - LAPOR SPT Masa PPh Unifikasi masa Mar 2027
- [ ] **Jum 30 Apr** - SETOR & LAPOR PPN masa Mar 2027
- [ ] **Jum 30 Apr** - LAPOR SPT Tahunan PPh Badan tahun pajak 2026

### Mei 2027

## Jawaban agent (ringkas)
- "SPT Tahunan PPh Badan tahun pajak 2026 paling lambat **Jumat 30 April 2027**; tenggat ini tidak bergeser. Lunasi PPh 29 sebelum mengirim SPT."
- "Hati-hati Mei 2027: setor PPh masa April bergeser sampai **Jumat 21 Mei** karena 15–20 Mei berturut-turut akhir pekan, Iduladha, cuti bersama, dan Waisak — tetapi lebih aman setor sebelum 14 Mei."
- "Maret 2027: setor masa Februari bergeser ke 16 Maret (15 Maret cuti bersama Idulfitri)."

## Penilaian penguji
- 73 tenggat 2027 cocok 100% dengan penghitung independen (HASIL-UJI §3), termasuk rantai libur 15→21 Mei 2027, Feb non-kabisat 28 Feb (Minggu) → 1 Mar, 31 Jan (Minggu) → 1 Feb, 31 Jul (Sabtu) → 2 Agu, 31 Okt (Minggu) → 1 Nov.
- Catatan: "Kalender 2027" menampilkan tenggat **yang jatuh** di 2027 (masa Des 2026 s.d. Nov 2027). Masa Desember 2027 (Jan 2028) dan SPT Tahunan 2027 (2028) tidak tampil — wajar, tetapi sebaiknya disebut di output (P3).
- PKP: **tidak ada batas unggah faktur keluaran tgl 20** (P1, sama dengan uji 02). Kalender pesaing (Metro TV/Ortax/Pajakku) mencantumkannya.
- Hasil: **LULUS** (dengan catatan P1).
