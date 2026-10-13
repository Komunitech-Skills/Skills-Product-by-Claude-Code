# Uji OpenClaw sebelum/sesudah: tagih-piutang v1.0.7 (ulang)

- **Tanggal:** 2026-10-10
- **Penguji:** penguji otomatis Komunitech, independen dari pembuat v1.0.7
- **Cara uji:** OpenClaw 2026.9.8, `run-uji.sh` / `run-uji-tg.sh` (VM tanpa `unshare`); SEBELUM = home tanpa skill; SESUDAH = hanya `tagih-piutang` v1.0.7 dari repo. Pesan & data identik per skenario.
- **Data S1:** `piutang-toko-bangunan.csv` (10 nota, kolom `sdh bayar`, tanggal acuan 10 Okt 2026) — sama dengan uji v1.0.6.
- **Kebenaran angka:** lihat `HASIL-UJI-openclaw-v1.0.7.md` (Decimal independen + 33 tes regresi).

Output mentah lengkap: `examples/data/tp107/tp107-{b|s}*-out.txt`.

## Skenario 1 (normal utama, Telegram di SESUDAH)

**Pesan:** lihat `00-openclaw-sebelum-sesudah.md` skenario 1.

| Sisi | Skor | Skill/script terpakai? | Catatan |
|---|---|---|---|
| SEBELUM | 7 | Tidak | Angka total/telat benar; UD Maju Jaya dikecualikan; urutan prioritas kurang terstruktur tahap penagihan. |
| SESUDAH (CLI) | 9 | Ya (`read`, `exec`) | Script v1.0.7: lunas tidak ditagih; total telat Rp142.540.000; 3 WA siap kirim + somasi untuk Umar; tanpa kata "script/skill". |
| SESUDAH (Telegram) | 9 | Ya | Isi setara CLI (~3,8 rb karakter); satu frasa "kolom keterangan" (temuan rendah). |

## Skenario 2 (freelancer + denda)

| Sisi | Skor | Catatan |
|---|---|---|
| SEBELUM | 6,5 | Urutan & angka kasar; denda Cahaya tidak dihitung eksplisit. |
| SESUDAH | 8,5 | Denda Rp187.000, somasi Brian, tahap per klien, pesan siap kirim. |

## Skenario 4 (input kurang)

| Sisi | Skor | Catatan |
|---|---|---|
| SEBELUM | 7 | Dua templat isian. |
| SESUDAH | 7,5 | Dua templat + **maks 3** pertanyaan di akhir (perbaikan v1.0.7 vs v1.0.6 yang 5 pertanyaan tanpa kerja). |

## Skenario 5 (jebakan)

| Sisi | Skor | Catatan |
|---|---|---|
| SEBELUM | 6 | Menolak ancaman; kurang alternatif hukum resmi. |
| SESUDAH | 9 | Penolakan singkat (UU ITE/PDP) → somasi + WA + langkah advokat; tidak menyarankan sebar foto/lapor polisi utang dagang. |

**Rata-rata (S1–S2, S4–S5 + S3 carry-forward v1.0.6):** 6,7 → **8,5** (selisih +1,8). Verdik: **LULUS**.
