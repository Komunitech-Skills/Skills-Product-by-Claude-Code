# Uji jadwal Telegram sungguhan (2026-10-13)

**Skill:** `absensi-lokal` v1.0.7 (catalog; SKILL.md tidak diubah)  
**Penguji:** penguji otomatis Komunitech, independen  
**Bot:** bot uji Komunitech (gateway uji internal)  
**Grup uji:** grup uji Telegram internal  
**Verdik:** **LOLOS**

## Ringkasan

| Pertanyaan | Hasil |
|---|---|
| Jadwal terbuat (automations one-shot ~5 menit)? | Ya — job `ad37ed17-a790-4a33-b9ec-c00d1d098d6c`, `--at 5m`, `--delete-after-run` |
| Pesan jadwal tiba di grup uji Telegram internal? | Ya — pesan bot terkirim (log gateway: `deliveryStatus: delivered`) |
| Tepat waktu? | Ya — run `2026-10-13T10:42:34Z` (~5 menit setelah pembuatan jadwal) |
| Isi sesuai (angka benar)? | Ya — **Hadir 1 dari 1**, **Terlambat 10 menit** cocok database uji & `absensi.py harian` independen |

## Cuplikan isi pesan terjadwal

```
ABSENSI SELASA, 13/10/2026 (per 17.42)
Hadir 1 dari 1 karyawan terjadwal
Terlambat: Andi UJI 08.10 (10 menit)
```

## Lingkungan uji

- Database fiktif di folder data skill (`KomunitechData/absensi/`) pada HOME gateway (init + 1 karyawan + tap masuk 08.10).  
- Skill aktif di home gateway (`absensi-lokal` disalin ke `~/.openclaw/skills/`).  
- Pola **Pilihan 1** `references/openclaw-jadwal.md`: `openclaw automations add` + `--command-argv` `harian --db …` + `--announce --channel telegram --to <ID-grup-uji> --thread-id <ID-thread-uji>`.  
- Konfigurasi grup uji: memakai pengaturan bawaan grup (tidak perlu skill agent untuk payload perintah).

## Cacat / catatan

- Alur konfirmasi "Lanjut? (ya/tidak)" lewat chat bot **tidak** diuji run ini (jadwal payload perintah langsung; sesuai pola uji jadwal skill lain).  
- Hanya **satu** pesan Telegram terjadwal (tanpa pesan tester tambahan).

## Pesan Telegram dalam uji

1. Bot → rekap harian terjadwal (delivered ke grup uji Telegram internal).
