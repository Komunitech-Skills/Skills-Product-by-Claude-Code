# Skenario 03 (uji Akun B) — Notulen rapat konsultan → simpan ke SiYuan (normal)

**Penguji:** Akun B, kernel tiruan `127.0.0.1:16806`.

## Permintaan pengguna
> "Ini notulen rapat sama klien Ani (sudah dirapikan skill notulen-rapat), simpan ke SiYuan buku Notulen Konsultan."

## Langkah & hasil nyata
```
$ python3 scripts/siyuan.py ... buat --notebook 20260101000002-konsulbx \
    --path "/Notulen/2026-09-26 Rapat Klien Ani" --md-file notulen.md --ya
TERSIMPAN: dokumen '/Notulen/2026-09-26 Rapat Klien Ani' dibuat di SiYuan (id 2026092609000500-mock005).
```
`baca --notebook 20260101000002-konsulbx --path "/Notulen/2026-09-26 Rapat Klien Ani"` mengembalikan
isi Markdown persis sama dengan file sumber (keputusan retainer Rp5.000.000/bulan, tindak lanjut
draf kontrak) — tidak ada perubahan makna, hanya heading path ditambahkan di depan sesuai format
`p_baca`.

## Verifikasi independen
- `--md-file` bekerja (jalur input Markdown dari file, bukan hanya `--md`).
- Pemisahan tanggung jawab sesuai SKILL.md §Kapan TIDAK digunakan: skill ini **hanya menyimpan**
  notulen yang sudah jadi (dari `notulen-rapat`), tidak merapikan catatan mentah — pengujian ini
  memakai notulen yang sudah terstruktur, sesuai batasan yang didokumentasikan.

## Kesimpulan
Sesuai dokumentasi. Tidak ada temuan baru.
