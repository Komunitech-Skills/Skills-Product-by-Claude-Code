# Uji jadwal Telegram sungguhan — C13 (2026-10-13)

**Skill:** `absensi-lokal` v1.0.7 (catalog; SKILL.md tidak diubah)  
**Penguji:** Akun C (Cursor Cloud), independen  
**Bot:** @KTclaude1_bot (gateway VM Cursor)  
**Grup uji:** `-1004407409583`, topik forum **1362** — `C13 absensi-lokal — jadwal`  
**Verdik:** **LOLOS**

## Ringkasan

| Pertanyaan | Hasil |
|---|---|
| Jadwal terbuat (automations one-shot ~5 menit)? | Ya — job `ad37ed17-a790-4a33-b9ec-c00d1d098d6c`, `--at 5m`, `--delete-after-run` |
| Pesan jadwal tiba di topik uji? | Ya — pesan bot **1363** (log gateway: `deliveryStatus: delivered`, `threadId=1362`) |
| Tepat waktu? | Ya — run `2026-10-13T10:42:34Z` (~5 menit setelah pembuatan jadwal) |
| Isi sesuai (angka benar)? | Ya — **Hadir 1 dari 1**, **Terlambat 10 menit** cocok database uji & `absensi.py harian` independen |

## Cuplikan isi pesan terjadwal (msg 1363)

```
ABSENSI SELASA, 13/10/2026 (per 17.42)
Hadir 1 dari 1 karyawan terjadwal
Terlambat: Andi C13 08.10 (10 menit)
```

## Lingkungan uji

- Database fiktif: `KomunitechData/absensi/absensi-c13.db` di HOME gateway (init + 1 karyawan + tap masuk 08.10).  
- Skill aktif di home gateway (`absensi-lokal` disalin ke `~/.openclaw/skills/`).  
- Pola **Pilihan 1** `references/openclaw-jadwal.md`: `openclaw automations add` + `--command-argv` `harian --db …` + `--announce --channel telegram --to -1004407409583 --thread-id 1362`.  
- Config topik 1362: default grup (tidak perlu skill agent untuk payload perintah).

## Cacat / catatan

- Alur konfirmasi "Lanjut? (ya/tidak)" lewat chat bot **tidak** diuji run ini (jadwal payload perintah langsung; sesuai pola C13 skill lain).  
- Hanya **satu** pesan Telegram terjadwal (tanpa pesan tester tambahan).

## Pesan Telegram (≤3 untuk skill)

1. Bot → rekap harian terjadwal (msg **1363**, delivered ke topik 1362).
