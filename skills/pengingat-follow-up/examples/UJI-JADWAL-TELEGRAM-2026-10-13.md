# Uji jadwal Telegram sungguhan (2026-10-13)

**Skill:** `pengingat-follow-up` v1.0.6 (catalog; SKILL.md tidak diubah)  
**Penguji:** penguji otomatis Komunitech, independen  
**Bot:** bot uji Komunitech (gateway uji internal)  
**Grup uji:** grup uji Telegram internal  
**Verdik:** **LOLOS**

## Ringkasan

| Pertanyaan | Hasil |
|---|---|
| Jadwal terbuat (automations one-shot ~5 menit)? | Ya — job `138f81fc-8189-4959-a95d-903cd595a159`, `--at 5m`, `--delete-after-run` |
| Pesan jadwal tiba di grup uji Telegram internal? | Ya — pesan bot terkirim (log gateway: `deliveryStatus: delivered`) |
| Tepat waktu? | Ya — run `2026-10-13T11:13:37Z` (~5 menit setelah pembuatan jadwal) |
| Isi sesuai (angka benar)? | Ya — **total piutang Rp 5.300.000** (terlambat Rp 800.000 + hari ini Rp 4.500.000) cocok `cek_jatuh_tempo.py --teks rekap` independen |

## Cuplikan isi pesan terjadwal

```
PENGINGAT FOLLOW-UP - Selasa, 13 Oktober 2026

TERLAMBAT (1)
1. #1 Piutang - Toko UJI | Rp 800.000 | nota B-UJI-1 | lewat 5 hari (jatuh tempo 8 Okt 2026)

HARI INI (1)
1. #2 Piutang - Bu Rina UJI | Rp 4.500.000 | INV-UJI | jatuh tempo hari ini

Total piutang tertunggak (terlambat + hari ini): Rp 5.300.000
…
```

## Lingkungan uji

- Data fiktif: `pengingat/DAFTAR.csv` di workspace gateway (2 piutang aktif, `--hari-ini 2026-10-13`).  
- Skill aktif di home gateway (`pengingat-follow-up` disalin ke `~/.openclaw/skills/`).  
- Pola **§2** `references/openclaw-jadwal.md` (tanpa AI): `openclaw automations add` + `--command` `cek_jatuh_tempo.py --teks rekap` + `--announce --channel telegram --to <ID-grup-uji> --thread-id <ID-thread-uji>`.  
- Job dihapus otomatis setelah run (`deleteAfterRun: true`).

## Cacat / catatan

- Alur konfirmasi "Lanjut? (ya/tidak)" lewat chat bot **tidak** diuji run ini (payload perintah langsung; sesuai pola uji jadwal skill lain).  
- Hanya **satu** pesan Telegram terjadwal (tanpa pesan tester tambahan).

## Pesan Telegram dalam uji

1. Bot → rekap pengingat terjadwal (delivered ke grup uji Telegram internal).
