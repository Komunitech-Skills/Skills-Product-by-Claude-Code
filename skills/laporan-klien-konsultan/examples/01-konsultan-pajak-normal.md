# Skenario 01 (normal) — Konsultan pajak, laporan mingguan satu klien

> Dijalankan ulang secara **independen** oleh penguji (Akun B, sesi terpisah dari pembuat skill),
> di folder scratchpad terisolasi (bukan `.claude/skills/`). Data rekaan. Mengulang skenario yang
> sama dengan `uji-pembuat-01-konsultan-pajak.md` untuk memverifikasi hasil pembuat, plus
> memverifikasi angka secara independen.

## Perintah
```bash
python3 scripts/laporan_klien.py --file run01/log.csv catat --klien "PT Maju Jaya" \
  --proyek "Pembukuan bulanan" --pekerjaan "Rekonsiliasi bank September" \
  --jam 2.5 --status selesai --tanggal 2026-09-22

python3 scripts/laporan_klien.py --file run01/log.csv catat --klien "PT Maju Jaya" \
  --proyek "Pembukuan bulanan" --pekerjaan "Susun draf SPT Masa PPN" --status berjalan \
  --butuh-klien "Faktur pajak masukan Oktober belum dikirim" --tanggal 2026-09-24 --jam 1.5

python3 scripts/laporan_klien.py --file run01/log.csv catat --klien "PT Maju Jaya" \
  --proyek "Konsultasi pajak" --pekerjaan "Diskusi strategi PPh Badan" --status terkendala \
  --kendala "Menunggu data laba rugi Q3 dari klien" --tanggal 2026-09-25

python3 scripts/laporan_klien.py --file run01/log.csv laporan --klien "PT Maju Jaya" \
  --periode mingguan --tanggal-acuan 2026-09-26 --json
```

## Output (ringkas, field JSON kunci)
```
total_jam 4.0
jumlah_entri 3
```
Field lengkap (`teks_email`, `teks_wa`, `markdown`, `kendala`, `butuh_dari_klien`, `rencana_berikutnya`)
sama persis strukturnya dengan `examples/uji-pembuat-01-konsultan-pajak.md`.

## Verifikasi independen
- Total jam = 2,5 (rekonsiliasi) + 1,5 (draf SPT) = **4,0 jam** — cocok dengan output script.
  Entri ketiga (Diskusi PPh Badan) sengaja tanpa `--jam`, benar tidak ikut dijumlah.
- `jumlah_entri` = 3, sesuai jumlah baris yang dicatat.
- Hasil **identik** dengan yang diklaim pembuat skill di `uji-pembuat-01-konsultan-pajak.md` —
  tidak ditemukan penyimpangan.

## Status
**Lulus.** Angka, format tiga versi, dan struktur bagian sesuai `SKILL.md` § Format Output.
