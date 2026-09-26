# Skenario 03 (normal) — Arsitek freelance, periode kustom, alias status & jam koma

## Skenario
Arsitek freelance mencatat 4 pekerjaan untuk klien perorangan "Bapak Handoko" pada dua proyek
(Renovasi rumah tinggal, Izin IMB), memakai **alias status** (`done`, `stuck`, `progress`) dan
**jam berformat koma** (`4,5`), lalu minta laporan periode kustom 19-25 September tanpa
menyebutkan rencana berikutnya (harus diturunkan otomatis).

## Perintah
```bash
python3 scripts/laporan_klien.py --file run03/log.csv catat --klien "Bapak Handoko" \
  --proyek "Renovasi rumah tinggal" --pekerjaan "Gambar denah revisi 2" --jam "4,5" \
  --status done --tanggal 2026-09-19
python3 scripts/laporan_klien.py --file run03/log.csv catat --klien "Bapak Handoko" \
  --proyek "Renovasi rumah tinggal" --pekerjaan "Survey lokasi & ukur ulang" --jam 2 \
  --status selesai --tanggal 2026-09-21
python3 scripts/laporan_klien.py --file run03/log.csv catat --klien "Bapak Handoko" \
  --proyek "Renovasi rumah tinggal" --pekerjaan "Konsultasi material atap" --status stuck \
  --kendala "Menunggu sampel material dari supplier" --tanggal 2026-09-23
python3 scripts/laporan_klien.py --file run03/log.csv catat --klien "Bapak Handoko" \
  --proyek "Izin IMB" --pekerjaan "Susun dokumen pengajuan IMB" --jam 3 --status progress \
  --butuh-klien "Sertifikat tanah asli untuk dilampirkan" --tanggal 2026-09-24

python3 scripts/laporan_klien.py --file run03/log.csv laporan --klien "Bapak Handoko" \
  --dari 2026-09-19 --sampai 2026-09-25 --json
```

## Output kunci
```
jumlah_entri 4
total_jam 9.5
jam_per_proyek {'Renovasi rumah tinggal': 6.5, 'Izin IMB': 3.0}
entri_tanpa_jam 1
selesai ['Gambar denah revisi 2', 'Survey lokasi & ukur ulang']
berjalan ['Susun dokumen pengajuan IMB']
terkendala ['Konsultasi material atap']
rencana ['Lanjutkan: Susun dokumen pengajuan IMB (Izin IMB)']
```

## Verifikasi independen
- Alias status `done`→`selesai`, `stuck`→`terkendala`, `progress`→`berjalan` semua dinormalisasi
  dengan benar (dikonfirmasi lewat pengelompokan `selesai`/`berjalan`/`terkendala` di output).
- Total jam = 4,5 + 2 + 3 = **9,5 jam** (entri "Konsultasi material atap" tanpa jam, benar
  dikeluarkan, `entri_tanpa_jam` = 1).
- `jam_per_proyek`: Renovasi rumah tinggal = 4,5 + 2 = **6,5 jam**; Izin IMB = **3 jam**. Cocok.
- Rencana Berikutnya **diturunkan otomatis** dari satu-satunya entri `berjalan` ("Susun dokumen
  pengajuan IMB") persis format "Lanjutkan: <pekerjaan> (<proyek>)" sesuai `SKILL.md` — tidak
  diberi `--rencana` sama sekali pada perintah ini.
- Klien perorangan (nama orang, bukan PT/CV) diperlakukan sama seperti klien korporasi — tidak
  ada perlakuan khusus format nama, sesuai harapan (skill tidak membedakan jenis klien).

## Status
**Lulus.** Alias status dan format jam koma bekerja benar; rencana turunan otomatis akurat.
