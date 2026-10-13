# Uji 02 (Normal) — CV PKP: "apa saja yang jatuh tempo 14 hari ke depan?" per 25 Sep 2026

> Penguji independen, 2026-09-25.

> **Catatan pembaruan (2026-10-13):** keluaran di bawah berasal dari uji awal (skill v1.0.0) dan belum memuat baris "Tenggat berikutnya", sumber data libur, maupun batas unggah faktur pajak keluaran tanggal 20 untuk PKP (ditambahkan sejak v1.0.1). Keluaran skill versi terbaru (v1.0.7) untuk perintah yang sama ada di bagian "Keluaran skill versi terbaru (v1.0.7)" di akhir berkas.

## Permintaan pengguna
> "CV saya sudah PKP, ada karyawan, potong PPh 23 ke vendor jasa, dan bayar angsuran PPh 25. Hari ini 25 September 2026 — pajak apa saja yang jatuh tempo 2 minggu ke depan?"

## Langkah agent
Profil: `badan-pkp` (PPN + PPh 25 + SPT badan) + `pemberi-kerja` + `pemotong`. Asumsi: CV tarif umum (PP 20/2026 tidak lagi memberi 0,5% untuk CV peserta baru), tahun buku kalender.
```bash
python3 scripts/kalender_pajak.py --profil badan-pkp,pemberi-kerja,pemotong --hari-ini 2026-09-25
```
Kode keluar 0.

## Output script (apa adanya)
## Tenggat pajak 14 hari ke depan (Jumat, 25 September 2026 s.d. Jumat, 9 Oktober 2026) - badan-pkp, pemberi-kerja, pemotong

| Sisa | Tanggal | Kegiatan | Keterangan |
|---|---|---|---|
| 5 hari lagi | Rabu, 30 September 2026 | SETOR & LAPOR PPN masa Agu 2026 | - |

_Bukan nasihat pajak. Dasar: PMK 81/2024 (berlaku 1 Jan 2025), PP 55/2022 jo. PP 20/2026, PER-2/PJ/2024, SKB 3 Menteri libur nasional & cuti bersama; dicek 2026-09-25 dari sumber sekunder (naskah resmi belum dibaca langsung). DJP kadang memundurkan tenggat lewat pengumuman khusus - cek pengumuman DJP terbaru (pajak.go.id, Kring Pajak 1500200). Pembulatan/perhitungan pajak tidak dilakukan skill ini dan belum dicocokkan dengan Coretax. Untuk kasus Anda, konsultasikan dengan konsultan pajak atau Account Representative (AR)._

## Tambahan agent
Karena hanya 1 butir, agent menjalankan ulang `--rentang 30` agar pengguna tahu tenggat berikutnya:
| Sisa | Tanggal | Kegiatan | Keterangan |
|---|---|---|---|
| 5 hari lagi | Rabu, 30 September 2026 | SETOR & LAPOR PPN masa Agu 2026 | - |
| 20 hari lagi | Kamis, 15 Oktober 2026 | SETOR PPh 21/26 (pemberi kerja) masa Sep 2026 | - |
| 20 hari lagi | Kamis, 15 Oktober 2026 | SETOR PPh Unifikasi (PPh 4(2), 15, 22, 23, 26 non-pegawai) masa Sep 2026 | - |
| 20 hari lagi | Kamis, 15 Oktober 2026 | SETOR PPh 25 (angsuran bulanan) masa Sep 2026 | - |
| 25 hari lagi | Selasa, 20 Oktober 2026 | LAPOR SPT Masa PPh 21/26 masa Sep 2026 | - |
| 25 hari lagi | Selasa, 20 Oktober 2026 | LAPOR SPT Masa PPh Unifikasi masa Sep 2026 | - |

_Bukan nasihat pajak. Dasar: PMK 81/2024 (berlaku 1 Jan 2025), PP 55/2022 jo. PP 20/2026, PER-2/PJ/2024, SKB 3 Menteri libur nasional & cuti bersama; dicek 2026-09-25 dari sumber sekunder (naskah resmi belum dibaca langsung). DJP kadang memundurkan tenggat lewat pengumuman khusus - cek pengumuman DJP terbaru (pajak.go.id, Kring Pajak 1500200). Pembulatan/perhitungan pajak tidak dilakukan skill ini dan belum dicocokkan dengan Coretax. Untuk kasus Anda, konsultasikan dengan konsultan pajak atau Account Representative (AR)._

Jawaban agent: "Dalam 14 hari ke depan hanya satu: setor & lapor SPT Masa PPN masa Agustus, paling lambat Rabu 30 September 2026 (5 hari lagi). Setor PPN dulu sebelum SPT dikirim, dan tetap lapor walau nihil. Setelah itu: 15 Oktober setor PPh 21, Unifikasi (PPh 23), dan PPh 25 masa September; 20 Oktober lapor SPT Masa PPh 21 dan Unifikasi."

## Penilaian penguji
- 30 Sep 2026 = Rabu, bukan libur → benar. 15 & 20 Okt 2026 benar.
- Hitungan "5 hari lagi" benar.
- Kekurangan: (a) untuk PKP tidak ada butir **batas unggah faktur pajak keluaran tgl 20** (PER-11/PJ/2025) — untuk masa September jatuh 20 Okt (di luar 14 hari, tetapi kewajiban ini tidak pernah muncul di skill) → temuan P1. (b) Bila rentang kosong/sedikit, script tidak menyebut tenggat berikutnya; agent harus inisiatif menjalankan ulang (P3).
- Hasil: **LULUS** (dengan catatan P1).
- Catatan pembaruan (2026-10-13): kekurangan (a) batas unggah faktur dan (b) tenggat berikutnya di atas sudah diperbaiki sejak v1.0.1; lihat keluaran terbaru di bagian berikut.

## Keluaran skill versi terbaru (v1.0.7) — perintah sama, data fiktif

> Dijalankan ulang pada 2026-10-13 dengan perintah dan tanggal acuan yang sama seperti di atas. Profil dan tanggal acuan ini fiktif (contoh), tidak memakai data pembeli. Keluaran disalin apa adanya dari `scripts/kalender_pajak.py`.

Perintah 1 (14 hari ke depan, bawaan):
```bash
python3 scripts/kalender_pajak.py --profil badan-pkp,pemberi-kerja,pemotong --hari-ini 2026-09-25
```

## Tenggat pajak 14 hari ke depan (Jumat, 25 September 2026 s.d. Jumat, 9 Oktober 2026) - badan-pkp, pemberi-kerja, pemotong

| Sisa | Tanggal | Kegiatan | Keterangan |
|---|---|---|---|
| 5 hari lagi | Rabu, 30 September 2026 | SETOR & LAPOR PPN masa Agu 2026 | - |

Tenggat berikutnya sesudah rentang ini: **Kamis, 15 Oktober 2026** (20 hari lagi) - SETOR PPh 21/26 (pemberi kerja) masa Sep 2026; SETOR PPh Unifikasi (PPh 4(2), 15, 22, 23, 26 non-pegawai) masa Sep 2026; SETOR PPh 25 (angsuran bulanan) masa Sep 2026

Data libur: SKB 3 Menteri libur nasional & cuti bersama 2026, 2027 (file: libur-nasional-2026.csv, libur-nasional-2027.csv).

_Bukan nasihat pajak. Dasar: PMK 81/2024 (berlaku 1 Jan 2025), PP 55/2022 jo. PP 20/2026, PER-2/PJ/2024, PER-11/PJ/2025, SKB 3 Menteri libur nasional & cuti bersama; dicek 2026-09-26 (pasal tenggat PMK 81/2024 & PER-11/PJ/2025 dicocokkan dengan naskah resmi di pajak.go.id; sebagian butir lain dari sumber sekunder). DJP kadang memundurkan tenggat lewat pengumuman khusus - cek pengumuman DJP terbaru (pajak.go.id, Kring Pajak 1500200). Pembulatan/perhitungan pajak tidak dilakukan skill ini dan belum dicocokkan dengan Coretax. Untuk kasus Anda, konsultasikan dengan konsultan pajak atau Account Representative (AR)._

Perintah 2 (30 hari ke depan; kini memuat baris UNGGAH faktur):
```bash
python3 scripts/kalender_pajak.py --profil badan-pkp,pemberi-kerja,pemotong --hari-ini 2026-09-25 --rentang 30
```

## Tenggat pajak 30 hari ke depan (Jumat, 25 September 2026 s.d. Minggu, 25 Oktober 2026) - badan-pkp, pemberi-kerja, pemotong

| Sisa | Tanggal | Kegiatan | Keterangan |
|---|---|---|---|
| 5 hari lagi | Rabu, 30 September 2026 | SETOR & LAPOR PPN masa Agu 2026 | - |
| 20 hari lagi | Kamis, 15 Oktober 2026 | SETOR PPh 21/26 (pemberi kerja) masa Sep 2026 | - |
| 20 hari lagi | Kamis, 15 Oktober 2026 | SETOR PPh Unifikasi (PPh 4(2), 15, 22, 23, 26 non-pegawai) masa Sep 2026 | - |
| 20 hari lagi | Kamis, 15 Oktober 2026 | SETOR PPh 25 (angsuran bulanan) masa Sep 2026 | - |
| 25 hari lagi | Selasa, 20 Oktober 2026 | LAPOR SPT Masa PPh 21/26 masa Sep 2026 | - |
| 25 hari lagi | Selasa, 20 Oktober 2026 | LAPOR SPT Masa PPh Unifikasi masa Sep 2026 | - |
| 25 hari lagi | Selasa, 20 Oktober 2026 | UNGGAH faktur pajak keluaran bulan Sep 2026 (batas persetujuan DJP) | - |

Tenggat berikutnya sesudah rentang ini: **Senin, 2 November 2026** (38 hari lagi) - SETOR & LAPOR PPN masa Sep 2026

Data libur: SKB 3 Menteri libur nasional & cuti bersama 2026, 2027 (file: libur-nasional-2026.csv, libur-nasional-2027.csv).

_Bukan nasihat pajak. Dasar: PMK 81/2024 (berlaku 1 Jan 2025), PP 55/2022 jo. PP 20/2026, PER-2/PJ/2024, PER-11/PJ/2025, SKB 3 Menteri libur nasional & cuti bersama; dicek 2026-09-26 (pasal tenggat PMK 81/2024 & PER-11/PJ/2025 dicocokkan dengan naskah resmi di pajak.go.id; sebagian butir lain dari sumber sekunder). DJP kadang memundurkan tenggat lewat pengumuman khusus - cek pengumuman DJP terbaru (pajak.go.id, Kring Pajak 1500200). Pembulatan/perhitungan pajak tidak dilakukan skill ini dan belum dicocokkan dengan Coretax. Untuk kasus Anda, konsultasikan dengan konsultan pajak atau Account Representative (AR)._

Catatan: batas unggah faktur pajak keluaran bulan September (Selasa, 20 Oktober 2026) tidak tampil di rentang 14 hari karena baru jatuh 25 hari dari tanggal acuan; ia tampil di rentang 30 hari. Tanggal-tanggal ini diambil dari keluaran script, bukan dihitung manual.
