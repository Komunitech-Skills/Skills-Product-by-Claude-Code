# Skenario 02 (normal) — Agensi digital, laporan bulanan, dua proyek per klien

## Skenario
Freelancer digital marketing mencatat 5 pekerjaan untuk klien "Kopi Senja" pada dua proyek
berbeda (Kampanye Instagram Q3, Iklan Meta Ads) sepanjang Agustus-September, lalu minta laporan
**bulanan** untuk September (tanggal acuan 26 Sep 2026, jadi "bulan-ini" = September).

## Perintah
```bash
python3 scripts/laporan_klien.py --file run02/log.csv catat --klien "Kopi Senja" \
  --proyek "Kampanye Instagram Q3" --pekerjaan "Riset konten & kalender posting Oktober" \
  --jam 3 --status selesai --tanggal 2026-09-01
python3 scripts/laporan_klien.py --file run02/log.csv catat --klien "Kopi Senja" \
  --proyek "Kampanye Instagram Q3" --pekerjaan "Desain 10 materi feed" --jam 6 \
  --status selesai --tanggal 2026-09-10
python3 scripts/laporan_klien.py --file run02/log.csv catat --klien "Kopi Senja" \
  --proyek "Iklan Meta Ads" --pekerjaan "Setup campaign awareness" --jam 2 --status berjalan \
  --butuh-klien "Approval budget iklan Rp5 juta" --tanggal 2026-09-15
python3 scripts/laporan_klien.py --file run02/log.csv catat --klien "Kopi Senja" \
  --proyek "Iklan Meta Ads" --pekerjaan "Optimasi audience" --status terkendala \
  --kendala "Akun iklan ditinjau ulang oleh Meta" --tanggal 2026-09-20
python3 scripts/laporan_klien.py --file run02/log.csv catat --klien "Kopi Senja" \
  --proyek "Kampanye Instagram Q3" --pekerjaan "Laporan performa Agustus" --jam 1.5 \
  --status selesai --tanggal 2026-08-05

python3 scripts/laporan_klien.py --file run02/log.csv laporan --klien "Kopi Senja" \
  --periode bulanan --tanggal-acuan 2026-09-26 \
  --rencana "Ajukan ulang review akun Meta Ads" --rencana "Kirim laporan performa September" --json
```

## Output kunci
```
periode {'label': 'Bulan September 2026', 'awal': '2026-09-01', 'akhir': '2026-09-30'}
jumlah_entri 4
total_jam 11.0
jam_per_proyek {'Kampanye Instagram Q3': 9.0, 'Iklan Meta Ads': 2.0}
entri_tanpa_jam 1
rencana ['Ajukan ulang review akun Meta Ads', 'Kirim laporan performa September']
kendala ['Akun iklan ditinjau ulang oleh Meta']
butuh ['Approval budget iklan Rp5 juta']
```

## Verifikasi independen
- Entri 5 September Agustus (tanggal 2026-08-05) **benar dikeluarkan** dari periode bulanan
  September — `jumlah_entri` = 4, bukan 5. Ini membuktikan filter periode bekerja lintas bulan
  dengan benar, tidak sekadar mengambil semua baris klien.
- Total jam = 3 + 6 + 2 = **11 jam** (entri "Optimasi audience" tanpa jam, benar tidak dihitung
  dan tercatat di `entri_tanpa_jam` = 1).
- `jam_per_proyek`: Kampanye Instagram Q3 = 3 + 6 = **9 jam**; Iklan Meta Ads = **2 jam**. Cocok.
- `--rencana` manual (dua butir) dipakai apa adanya, menggantikan turunan otomatis dari status
  `berjalan` — sesuai desain di `SKILL.md`.
- Hanya satu klien muncul di `daftar-klien` meski ada 2 proyek berbeda — kolom `proyek` dipakai
  sebagai sub-pengelompokan, bukan pemisah klien. Sesuai desain ("satu file untuk semua klien,
  dipilah lewat kolom `klien`").

## Status
**Lulus.** Perhitungan lintas-bulan dan multi-proyek per klien akurat.
