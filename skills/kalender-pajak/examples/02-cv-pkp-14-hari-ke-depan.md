# Uji 02 (Normal) — CV PKP: "apa saja yang jatuh tempo 14 hari ke depan?" per 25 Sep 2026

> Penguji independen, 2026-09-25.

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
