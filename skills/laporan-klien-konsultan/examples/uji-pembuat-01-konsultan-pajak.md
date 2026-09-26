# Contoh 01 — Konsultan pajak, laporan mingguan untuk satu klien

> Dijalankan sendiri oleh pembuat skill saat pengembangan (bukan uji independen Tahap 6
> `CLAUDE.md` — itu perlu agent/sesi terpisah yang belum dilakukan untuk skill ini). Disertakan
> agar pembeli/reviewer bisa melihat contoh nyata input → output sebelum memakainya. Semua nama
> klien dan angka **fiktif**.

## Skenario
Konsultan pajak lepas mencatat tiga pekerjaan untuk kliennya, PT Maju Jaya, sepanjang minggu
(21-27 September 2026), lalu meminta draf laporan mingguan pada hari Jumat.

## Perintah 1-3: mencatat pekerjaan (sepanjang minggu, saat progres terjadi)
```bash
python3 scripts/laporan_klien.py --file contoh.csv catat --klien "PT Maju Jaya" \
  --proyek "Pembukuan bulanan" --pekerjaan "Rekonsiliasi bank September" \
  --jam 2.5 --status selesai --tanggal 2026-09-22

python3 scripts/laporan_klien.py --file contoh.csv catat --klien "PT Maju Jaya" \
  --proyek "Pembukuan bulanan" --pekerjaan "Susun draf SPT Masa PPN" --status berjalan \
  --butuh-klien "Faktur pajak masukan Oktober belum dikirim" --tanggal 2026-09-24 --jam 1.5

python3 scripts/laporan_klien.py --file contoh.csv catat --klien "PT Maju Jaya" \
  --proyek "Konsultasi pajak" --pekerjaan "Diskusi strategi PPh Badan" --status terkendala \
  --kendala "Menunggu data laba rugi Q3 dari klien" --tanggal 2026-09-25
```
(Entri ketiga sengaja tidak diberi `--jam` — mensimulasikan konsultan yang lupa mencatat jamnya.)

## Isi `contoh.csv` setelah tiga baris di atas
```csv
tanggal,klien,proyek,pekerjaan,jam,status,kendala,butuh_dari_klien
2026-09-22,PT Maju Jaya,Pembukuan bulanan,Rekonsiliasi bank September,2.5,selesai,,
2026-09-24,PT Maju Jaya,Pembukuan bulanan,Susun draf SPT Masa PPN,1.5,berjalan,,Faktur pajak masukan Oktober belum dikirim
2026-09-25,PT Maju Jaya,Konsultasi pajak,Diskusi strategi PPh Badan,,terkendala,Menunggu data laba rugi Q3 dari klien,
```

## Perintah 4: susun draf laporan mingguan (Jumat, 26 Sep 2026)
```bash
python3 scripts/laporan_klien.py --file contoh.csv laporan --klien "PT Maju Jaya" \
  --periode mingguan --tanggal-acuan 2026-09-26
```
(`--tanggal-acuan` dipakai di contoh ini supaya periode "minggu ini" tidak bergantung pada tanggal
sungguhan saat file ini dibaca; dalam pemakaian nyata parameter ini dikosongkan dan script memakai
tanggal hari itu.)

## Output (apa adanya dari script, tanpa `--json`)
```
=== VERSI EMAIL ===

Subjek: Laporan Progres Minggu ini -- PT Maju Jaya (21 September 2026 - 27 September 2026)

Yth. Bapak/Ibu PT Maju Jaya,

Berikut laporan progres untuk periode 21 September 2026 - 27 September 2026.

Ringkasan: Periode minggu ini (21 September 2026 - 27 September 2026): 1 pekerjaan selesai, 1 sedang berjalan, 1 terkendala. Total jam tercatat: 4 jam.

Yang sudah selesai:
- Rekonsiliasi bank September (Pembukuan bulanan, 2,5 jam)

Yang sedang berjalan:
- Susun draf SPT Masa PPN (Pembukuan bulanan, 1,5 jam)

Terkendala:
- Diskusi strategi PPh Badan (Konsultasi pajak)

Mohon bantuan/keputusan dari Bapak/Ibu untuk:
- Faktur pajak masukan Oktober belum dikirim

Rencana berikutnya:
- Lanjutkan: Susun draf SPT Masa PPN (Pembukuan bulanan)

Demikian laporan ini kami sampaikan. Silakan hubungi kami bila ada pertanyaan.

Hormat kami,
[Nama Anda]

=== VERSI WA/TELEGRAM ===

*Laporan Progres -- PT Maju Jaya*
_Minggu ini, 21 September 2026 - 27 September 2026_

Periode minggu ini (21 September 2026 - 27 September 2026): 1 pekerjaan selesai, 1 sedang berjalan, 1 terkendala. Total jam tercatat: 4 jam.

*Selesai:*
- Rekonsiliasi bank September (Pembukuan bulanan, 2,5 jam)

*Berjalan:*
- Susun draf SPT Masa PPN (Pembukuan bulanan, 1,5 jam)

*Terkendala:*
- Diskusi strategi PPh Badan (Konsultasi pajak)

*Butuh dari Bapak/Ibu:*
- Faktur pajak masukan Oktober belum dikirim

*Rencana berikutnya:*
- Lanjutkan: Susun draf SPT Masa PPN (Pembukuan bulanan)

=== VERSI MARKDOWN (dokumen) ===

# Laporan Progres -- PT Maju Jaya
**Periode:** Minggu ini (21 September 2026 - 27 September 2026)

## Ringkasan
Periode minggu ini (21 September 2026 - 27 September 2026): 1 pekerjaan selesai, 1 sedang berjalan, 1 terkendala. Total jam tercatat: 4 jam.

## Yang Selesai
- Rekonsiliasi bank September (Pembukuan bulanan, 2026-09-22, 2,5 jam)

## Yang Sedang Berjalan
- Susun draf SPT Masa PPN (Pembukuan bulanan, 2026-09-24, 1,5 jam)

## Terkendala
- Diskusi strategi PPh Badan (Konsultasi pajak, 2026-09-25)

## Butuh dari Klien
- Faktur pajak masukan Oktober belum dikirim

## Kendala Saat Ini
- Menunggu data laba rugi Q3 dari klien

## Rencana Berikutnya
- Lanjutkan: Susun draf SPT Masa PPN (Pembukuan bulanan)

## Total Jam
**Total: 4 jam** (dari 2 entri berjam; 1 entri tanpa jam tidak dihitung)
- Pembukuan bulanan: 4 jam

---
_Draf disusun otomatis dari catatan kerja lokal. Tinjau sebelum dikirim ke klien._

--- CATATAN ---
- 1 dari 3 entri tidak mencatat jam -- total jam di bawah TIDAK termasuk entri tersebut (bukan dianggap 0).
```

## Verifikasi manual angka
- Total jam = 2,5 (rekonsiliasi) + 1,5 (draf SPT) = **4 jam**. Entri ketiga (Diskusi PPh Badan)
  sengaja tanpa jam, dan benar ditandai "1 entri tanpa jam tidak dihitung" (bukan dianggap 0 jam).
- `Kendala Saat Ini` hanya menampilkan kendala dari entri Diskusi PPh Badan (entri lain tidak
  mengisi `--kendala`).
- `Butuh dari Klien` hanya menampilkan permintaan faktur pajak dari entri draf SPT.
- `Rencana Berikutnya` diturunkan otomatis dari satu-satunya entri berstatus `berjalan` (draf
  SPT), sesuai desain: tanpa `--rencana`, rencana = "Lanjutkan: <pekerjaan berjalan>".
- Tidak ada kode keluar 3 pada contoh ini karena tidak ada pola data pribadi/rahasia terdeteksi di
  kolom teks manapun (lihat contoh deteksi ini di `04-input-buruk.md` bila sudah tersedia dari
  penguji independen).

## Catatan tambahan yang dicek pembuat
- Ganti `--periode mingguan` dengan `--rencana "Kirim draf SPT ke klien" --rencana "Follow up
  faktur pajak"` menghasilkan bagian "Rencana Berikutnya" persis dua butir itu (rencana manual
  menggantikan yang diturunkan otomatis) — sudah diverifikasi lewat `tests/uji_regresi.py`
  (`test_rencana_manual_dipakai_bukan_turunan`).
- Mencatat pekerjaan dengan nomor HP di dalamnya (mis. "Hubungi klien di 0812-3456-7890") tetap
  tercatat, tapi script keluar kode 3 dengan pesan di stderr — lihat
  `test_deteksi_data_sensitif_exit_3_tapi_tetap_tercatat` di `tests/uji_regresi.py`.
