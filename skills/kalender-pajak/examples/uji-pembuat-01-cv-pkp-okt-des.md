# Contoh 01 (Normal) — "CV saya PKP, karyawan 3, sering potong PPh 23. Jadwal pajak Oktober–Desember 2026"

> Dibuat oleh **pembuat skill** untuk verifikasi awal (menjalankan script sungguhan dan memeriksa hasilnya dengan kalender secara independen), **bukan pengganti** pengujian independen Tahap 6 CLAUDE.md. Tanggal uji: 2026-09-25, Python 3 (Linux).

> **Catatan pembaruan (2026-10-13):** tabel di bawah berasal dari verifikasi awal (skill v1.0.0; 18 baris) dan belum memuat baris unggah faktur pajak keluaran tanggal 20 untuk PKP (ditambahkan sejak v1.0.1). Keluaran skill versi terbaru (v1.0.7) untuk perintah yang sama (21 baris) ada di bagian "Keluaran skill versi terbaru (v1.0.7)" di akhir berkas; contoh ini juga dirujuk dari SKILL.md.

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

## Keluaran skill versi terbaru (v1.0.7) — perintah sama, data fiktif

> Dijalankan ulang pada 2026-10-13 dengan perintah dan tanggal acuan yang sama seperti di atas. Profil dan tanggal acuan ini fiktif (contoh), tidak memakai data pembeli. Keluaran disalin apa adanya dari `scripts/kalender_pajak.py`.

Perintah:
```bash
python3 scripts/kalender_pajak.py --profil badan-pkp,pemberi-kerja,pemotong --tahun 2026 --bulan-mulai 10 --jumlah-bulan 3
```

## Kalender Pajak Oktober 2026 - Desember 2026 - badan-pkp, pemberi-kerja, pemotong

Kewajiban: PPN (PKP), PPh 25 (angsuran bulanan), SPT Tahunan PPh Badan, PPh 21/26 (pemberi kerja), Bukti potong PPh 21 tahunan (BPA1, dulu 1721-A1), PPh Unifikasi (PPh 4(2), 15, 22, 23, 26 non-pegawai)

Cakupan: tenggat yang **jatuh** pada Kamis, 1 Oktober 2026 s.d. Kamis, 31 Desember 2026 (termasuk tenggat masa pajak bulan sebelum periode). Tenggat masa pajak Desember 2026 dan sesudahnya jatuh setelah periode ini; begitu juga kewajiban tahunan untuk tahun pajak 2026 - buat kalender periode berikutnya untuk melihatnya.
Data libur: SKB 3 Menteri libur nasional & cuti bersama 2026, 2027 (file: libur-nasional-2026.csv, libur-nasional-2027.csv).

| Tanggal | Kegiatan | Keterangan |
|---|---|---|
| Kamis, 15 Oktober 2026 | SETOR PPh 21/26 (pemberi kerja) masa Sep 2026 | - |
| Kamis, 15 Oktober 2026 | SETOR PPh Unifikasi (PPh 4(2), 15, 22, 23, 26 non-pegawai) masa Sep 2026 | - |
| Kamis, 15 Oktober 2026 | SETOR PPh 25 (angsuran bulanan) masa Sep 2026 | - |
| Selasa, 20 Oktober 2026 | LAPOR SPT Masa PPh 21/26 masa Sep 2026 | - |
| Selasa, 20 Oktober 2026 | LAPOR SPT Masa PPh Unifikasi masa Sep 2026 | - |
| Selasa, 20 Oktober 2026 | UNGGAH faktur pajak keluaran bulan Sep 2026 (batas persetujuan DJP) | - |
| Senin, 2 November 2026 | SETOR & LAPOR PPN masa Sep 2026 | bergeser dari 31 Okt (31 Okt: Sabtu; 1 Nov: Minggu) |
| Senin, 16 November 2026 | SETOR PPh 21/26 (pemberi kerja) masa Okt 2026 | bergeser dari 15 Nov (15 Nov: Minggu) |
| Senin, 16 November 2026 | SETOR PPh Unifikasi (PPh 4(2), 15, 22, 23, 26 non-pegawai) masa Okt 2026 | bergeser dari 15 Nov (15 Nov: Minggu) |
| Senin, 16 November 2026 | SETOR PPh 25 (angsuran bulanan) masa Okt 2026 | bergeser dari 15 Nov (15 Nov: Minggu) |
| Jumat, 20 November 2026 | LAPOR SPT Masa PPh 21/26 masa Okt 2026 | - |
| Jumat, 20 November 2026 | LAPOR SPT Masa PPh Unifikasi masa Okt 2026 | - |
| Jumat, 20 November 2026 | UNGGAH faktur pajak keluaran bulan Okt 2026 (batas persetujuan DJP) | - |
| Senin, 30 November 2026 | SETOR & LAPOR PPN masa Okt 2026 | - |
| Selasa, 15 Desember 2026 | SETOR PPh 21/26 (pemberi kerja) masa Nov 2026 | - |
| Selasa, 15 Desember 2026 | SETOR PPh Unifikasi (PPh 4(2), 15, 22, 23, 26 non-pegawai) masa Nov 2026 | - |
| Selasa, 15 Desember 2026 | SETOR PPh 25 (angsuran bulanan) masa Nov 2026 | - |
| Minggu, 20 Desember 2026 | UNGGAH faktur pajak keluaran bulan Nov 2026 (batas persetujuan DJP) | jatuh pada hari libur (Minggu) dan TIDAK bergeser - selesaikan paling lambat hari kerja sebelumnya: Jumat, 18 Desember 2026 |
| Senin, 21 Desember 2026 | LAPOR SPT Masa PPh 21/26 masa Nov 2026 | bergeser dari 20 Des (20 Des: Minggu) |
| Senin, 21 Desember 2026 | LAPOR SPT Masa PPh Unifikasi masa Nov 2026 | bergeser dari 20 Des (20 Des: Minggu) |
| Kamis, 31 Desember 2026 | SETOR & LAPOR PPN masa Nov 2026 | - |

**Catatan per kewajiban**
- PPN (PKP): Setor paling lambat akhir bulan berikutnya DAN sebelum SPT Masa PPN dikirim. PKP tetap lapor walau nihil. Faktur pajak keluaran wajib diunggah & mendapat persetujuan DJP paling lambat tgl 20 bulan berikutnya setelah tanggal pembuatan faktur (PER-11/PJ/2025 Ps. 44 ayat 1); faktur yang tidak disetujui bukan faktur pajak sah. Batas unggah faktur TIDAK bergeser walau tgl 20 hari libur (PER-11/PJ/2025 tidak memuat ketentuan pergeseran; PERLU REVIEW) - unggah sebelum tgl 20. Besarannya: skill hitung-ppn (bila terpasang).
- PPh 25 (angsuran bulanan): Batas lapor SPT Masa PPh 25 tgl 20, tetapi setoran yang tervalidasi (ada NTPN) dianggap sudah lapor pada tanggal setor (PMK 81/2024 Ps. 171 ayat 10) - jadi cukup setor paling lambat tgl 15. Angsuran nihil tidak perlu setor.
- SPT Tahunan PPh Badan: Paling lambat akhir bulan ke-4 setelah akhir tahun buku (dianggap tahun buku Januari-Desember). Kurang bayar (PPh 29) dilunasi SEBELUM SPT dikirim. Tidak bergeser meski hari libur (PMK 81/2024 Ps. 169); lapor lebih awal.
- PPh 21/26 (pemberi kerja): Besarannya: skill pph21-ter (bila terpasang). Bukti potong dibuat di Coretax.
- Bukti potong PPh 21 tahunan (BPA1, dulu 1721-A1): Paling lama 1 bulan setelah masa pajak terakhir (PER-2/PJ/2024). Karyawan butuh ini untuk SPT Tahunan. Tanggal ditampilkan tanpa pergeseran (PERLU REVIEW).
- PPh Unifikasi (PPh 4(2), 15, 22, 23, 26 non-pegawai): Untuk pemotong/pemungut, mis. potong PPh 23 jasa atau PPh 4(2) sewa.

**Aturan pergeseran:** tenggat setor & lapor bulanan yang jatuh pada Sabtu, Minggu, libur nasional, atau cuti bersama bergeser ke hari kerja berikutnya (PMK 81/2024). SPT Tahunan dan batas unggah faktur pajak ditampilkan tanpa pergeseran (lebih aman bila ternyata boleh bergeser); bila jatuh di hari libur, disebutkan hari kerja sebelumnya. Sebaiknya setor/lapor 2-3 hari sebelum tenggat.

_Bukan nasihat pajak. Dasar: PMK 81/2024 (berlaku 1 Jan 2025), PP 55/2022 jo. PP 20/2026, PER-2/PJ/2024, PER-11/PJ/2025, SKB 3 Menteri libur nasional & cuti bersama; dicek 2026-09-26 (pasal tenggat PMK 81/2024 & PER-11/PJ/2025 dicocokkan dengan naskah resmi di pajak.go.id; sebagian butir lain dari sumber sekunder). DJP kadang memundurkan tenggat lewat pengumuman khusus - cek pengumuman DJP terbaru (pajak.go.id, Kring Pajak 1500200). Pembulatan/perhitungan pajak tidak dilakukan skill ini dan belum dicocokkan dengan Coretax. Untuk kasus Anda, konsultasikan dengan konsultan pajak atau Account Representative (AR)._

Perintah file kalender (.ics):
```bash
python3 scripts/kalender_pajak.py --profil badan-pkp,pemberi-kerja,pemotong --tahun 2026 --bulan-mulai 10 --jumlah-bulan 3 --format ics --keluar kalender-pajak.ics
```
Keluaran pertama: `Tersimpan: kalender-pajak.ics (21 tenggat)` (sebelumnya 18).

**Pemeriksaan tambahan atas 3 baris UNGGAH faktur (2026-10-13):** dicek dengan skrip terpisah yang hanya memakai `datetime` dan berkas libur di `references/`. Hasil: 20 Oktober 2026 adalah Selasa dan 20 November 2026 adalah Jumat (hari kerja, tanpa label); 20 Desember 2026 adalah Minggu sehingga diberi label "TIDAK bergeser" dengan hari kerja sebelumnya Jumat, 18 Desember 2026 — semuanya cocok dengan keluaran script.
