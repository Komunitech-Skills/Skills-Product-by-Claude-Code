# Skenario 03 (normal) — Fisioterapi, sesi lanjutan

Hari ini (acuan uji): 26 September 2026.

**Input pengguna:** "Pak Joko fisioterapi hari ini, nomor +6281298765432, boleh diingatkan.
Setelah ini jadwalkan lagi 1 minggu lagi ya."

**Perintah:**
```bash
python3 scripts/pengingat_pasien.py --hari-ini 2026-09-26 tambah --nama "Pak Joko" \
  --wa "+6281298765432" --jenis "fisioterapi" --tanggal "hari ini" --persetujuan ya
python3 scripts/pengingat_pasien.py --hari-ini 2026-09-26 ubah-status --id 3 --status datang \
  --berikutnya "1 minggu lagi"
```

**Output nyata:**
```
Tersimpan #3: Pak Joko | Fisioterapi | 26 Sep 2026 | persetujuan: ya
#3 Pak Joko: status -> dijadwalkan | jadwal berikutnya 3 Okt 2026
```

**Verifikasi independen tanggal:** 26 Sep 2026 + 7 hari = 3 Oktober 2026. Benar (26+7=33 → 33−30
hari di September = 3 Oktober, karena September punya 30 hari).

**Verifikasi alur status:** setelah `ubah-status --status datang --berikutnya`, status kembali
`dijadwalkan` (bukan tetap "datang"), `diingatkan_pada` dikosongkan lagi, dan catatan otomatis
mencatat "kunjungan sebelumnya Sabtu, 26 September 2026 selesai" — cocok untuk pola sesi
fisioterapi berkelanjutan tanpa perlu mencatat ulang nama/WA pasien. Lulus.
