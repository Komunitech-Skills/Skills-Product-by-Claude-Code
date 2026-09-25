# Contoh 01 (Normal) — "CV saya PKP, karyawan 3, sering potong PPh 23. Jadwal pajak Oktober–Desember 2026"

> Dibuat oleh **pembuat skill** untuk verifikasi awal (menjalankan script sungguhan dan memeriksa hasilnya dengan kalender secara independen), **bukan pengganti** pengujian independen Tahap 6 CLAUDE.md. Tanggal uji: 2026-09-25, Python 3 (Linux).

## Permintaan pengguna
> "Saya punya CV kecil, sudah PKP, karyawan 3 orang, dan sering bayar jasa yang dipotong PPh 23. Tolong jadwal pajak Oktober sampai Desember 2026, sekalian file buat Google Calendar."

## Langkah 1 — Tentukan profil
CV PKP → `badan-pkp` (PPN + PPh 25 + SPT Tahunan badan); karyawan → `pemberi-kerja`; PPh 23 → `pemotong`.
Asumsi disebut ke pengguna: CV memakai tarif umum (bukan PPh final 0,5% — PP 20/2026 mengeluarkan CV dari skema 0,5% dengan masa transisi; cek skill `pph-final-umkm`), tahun buku Januari–Desember.

## Langkah 2 — Jalankan script
```bash
python3 scripts/kalender_pajak.py --profil badan-pkp,pemberi-kerja,pemotong --tahun 2026 --bulan-mulai 10 --jumlah-bulan 3
```
Output (tabel, apa adanya):

| Tanggal | Kegiatan | Keterangan |
|---|---|---|
| Kamis, 15 Oktober 2026 | SETOR PPh 21/26 (pemberi kerja) masa Sep 2026 | - |
| Kamis, 15 Oktober 2026 | SETOR PPh Unifikasi (PPh 4(2), 15, 22, 23, 26 non-pegawai) masa Sep 2026 | - |
| Kamis, 15 Oktober 2026 | SETOR PPh 25 (angsuran bulanan) masa Sep 2026 | - |
| Selasa, 20 Oktober 2026 | LAPOR SPT Masa PPh 21/26 masa Sep 2026 | - |
| Selasa, 20 Oktober 2026 | LAPOR SPT Masa PPh Unifikasi masa Sep 2026 | - |
| Senin, 2 November 2026 | SETOR & LAPOR PPN masa Sep 2026 | bergeser dari 31 Okt (31 Okt Sabtu; 1 Nov Minggu) |
| Senin, 16 November 2026 | SETOR PPh 21/26 (pemberi kerja) masa Okt 2026 | bergeser dari 15 Nov (15 Nov Minggu) |
| Senin, 16 November 2026 | SETOR PPh Unifikasi (PPh 4(2), 15, 22, 23, 26 non-pegawai) masa Okt 2026 | bergeser dari 15 Nov (15 Nov Minggu) |
| Senin, 16 November 2026 | SETOR PPh 25 (angsuran bulanan) masa Okt 2026 | bergeser dari 15 Nov (15 Nov Minggu) |
| Jumat, 20 November 2026 | LAPOR SPT Masa PPh 21/26 masa Okt 2026 | - |
| Jumat, 20 November 2026 | LAPOR SPT Masa PPh Unifikasi masa Okt 2026 | - |
| Senin, 30 November 2026 | SETOR & LAPOR PPN masa Okt 2026 | - |
| Selasa, 15 Desember 2026 | SETOR PPh 21/26 (pemberi kerja) masa Nov 2026 | - |
| Selasa, 15 Desember 2026 | SETOR PPh Unifikasi (PPh 4(2), 15, 22, 23, 26 non-pegawai) masa Nov 2026 | - |
| Selasa, 15 Desember 2026 | SETOR PPh 25 (angsuran bulanan) masa Nov 2026 | - |
| Senin, 21 Desember 2026 | LAPOR SPT Masa PPh 21/26 masa Nov 2026 | bergeser dari 20 Des (20 Des Minggu) |
| Senin, 21 Desember 2026 | LAPOR SPT Masa PPh Unifikasi masa Nov 2026 | bergeser dari 20 Des (20 Des Minggu) |
| Kamis, 31 Desember 2026 | SETOR & LAPOR PPN masa Nov 2026 | - |

(+ catatan per kewajiban, aturan pergeseran, disclaimer — lihat output lengkap script.)

## Langkah 3 — Verifikasi independen oleh pembuat
Hari dalam seminggu dicek dengan `datetime` Python terpisah (bukan kode skill):
- 31 Okt 2026 = Sabtu, 1 Nov = Minggu → PPN masa Sep bergeser ke Senin 2 Nov ✅
- 15 Nov 2026 = Minggu → Senin 16 Nov ✅; 20 Des 2026 = Minggu → Senin 21 Des ✅
- 30 Nov 2026 = Senin, 31 Des 2026 = Kamis (bukan libur; 24–25 Des cuti/libur Natal tidak kena) ✅
- Tidak ada libur nasional/cuti bersama 2026 di Okt–Nov; Des hanya 24–25 → tidak memengaruhi tgl 15/20/31 ✅
- Tidak ada SPT Tahunan badan di rentang ini (jatuh 30 Apr 2027) dan BPA1 (31 Jan 2027) — benar tidak muncul ✅

## Langkah 4 — File kalender
```bash
python3 scripts/kalender_pajak.py --profil badan-pkp,pemberi-kerja,pemotong --tahun 2026 --bulan-mulai 10 --jumlah-bulan 3 --format ics --keluar kalender-pajak.ics
```
→ `Tersimpan: kalender-pajak.ics (18 tenggat)`. Diperiksa: diawali `BEGIN:VCALENDAR` + CRLF, 18 `VEVENT`, tiap acara `DTSTART;VALUE=DATE` + `DTEND` hari berikutnya, dua `VALARM` (`TRIGGER:-P2DT15H` = H-3 pukul 09.00, `TRIGGER:-PT15H` = H-1 pukul 09.00), koma/titik koma di-escape (`badan-pkp\, pemberi-kerja`), baris dilipat ≤ 75 oktet. Impor ke Google Calendar belum diuji di aplikasi sungguhan (hanya validasi format oleh tes regresi).

Jawaban ke pengguna (ringkas): tabel di atas + "PPN masa September boleh disetor & dilapor sampai Senin 2 November karena 31 Oktober hari Sabtu — tapi lebih aman selesaikan Jumat 30 Oktober. Impor file `kalender-pajak.ics` lewat Google Calendar → Setelan → Impor & ekspor. Untuk besaran PPh 21 dan PPN, pakai skill pph21-ter dan hitung-ppn." + disclaimer.

## Langkah 5 — Cek cepat mode lain
- `--hari-ini 2026-10-10` → 5 tenggat: 3× "5 hari lagi" (15 Okt), 2× "10 hari lagi" (20 Okt) ✅
- `--profil cv-pkp` → `ERROR: profil/kewajiban 'cv-pkp' tidak dikenal. Pilihan profil: ...` exit 2, tanpa traceback ✅
- `--tahun 2028` → tetap jalan + PERINGATAN data libur 2028 belum ada ✅

## Tes regresi
`python3 tests/uji_regresi.py` → **33 tes OK** (pergeseran Sabtu/Minggu/libur/cuti bersama, dua patokan yang dikonfirmasi DDTC: 25 Mar 2026 & 18 Mei 2026, Februari biasa & kabisat 2028, masa Desember → Januari tahun berikutnya, SPT Tahunan tidak bergeser, validitas .ics, UID stabil, input buruk tanpa traceback).
