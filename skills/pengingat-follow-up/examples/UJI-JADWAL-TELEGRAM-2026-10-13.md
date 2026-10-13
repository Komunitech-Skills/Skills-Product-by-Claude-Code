# Uji jadwal Telegram sungguhan — C13 (2026-10-13)

**Skill:** `pengingat-follow-up` v1.0.6 (catalog; SKILL.md tidak diubah)  
**Penguji:** Akun C (Cursor Cloud), independen  
**Bot:** @KTclaude1_bot (gateway VM Cursor)  
**Grup uji:** `-1004407409583`, topik forum **1365** — `C13 pengingat-follow-up — jadwal`  
**Verdik:** **LOLOS**

## Ringkasan

| Pertanyaan | Hasil |
|---|---|
| Jadwal terbuat (automations one-shot ~5 menit)? | Ya — job `138f81fc-8189-4959-a95d-903cd595a159`, `--at 5m`, `--delete-after-run` |
| Pesan jadwal tiba di topik uji? | Ya — pesan bot **1366** (log gateway: `deliveryStatus: delivered`, `threadId=1365`) |
| Tepat waktu? | Ya — run `2026-10-13T11:13:37Z` (~5 menit setelah pembuatan jadwal) |
| Isi sesuai (angka benar)? | Ya — **total piutang Rp 5.300.000** (terlambat Rp 800.000 + hari ini Rp 4.500.000) cocok `cek_jatuh_tempo.py --teks rekap` independen |

## Cuplikan isi pesan terjadwal (msg 1366)

```
PENGINGAT FOLLOW-UP - Selasa, 13 Oktober 2026

TERLAMBAT (1)
1. #1 Piutang - Toko C13 | Rp 800.000 | nota B-C13-1 | lewat 5 hari (jatuh tempo 8 Okt 2026)

HARI INI (1)
1. #2 Piutang - Bu Rina C13 | Rp 4.500.000 | INV-C13 | jatuh tempo hari ini

Total piutang tertunggak (terlambat + hari ini): Rp 5.300.000
…
```

## Lingkungan uji

- Data fiktif: `pengingat/DAFTAR.csv` di workspace gateway (2 piutang aktif, `--hari-ini 2026-10-13`).  
- Skill aktif di home gateway (`pengingat-follow-up` disalin ke `~/.openclaw/skills/`).  
- Pola **§2** `references/openclaw-jadwal.md` (tanpa AI): `openclaw automations add` + `--command` `cek_jatuh_tempo.py --teks rekap` + `--announce --channel telegram --to -1004407409583 --thread-id 1365`.  
- Job dihapus otomatis setelah run (`deleteAfterRun: true`).

## Cacat / catatan

- Alur konfirmasi "Lanjut? (ya/tidak)" lewat chat bot **tidak** diuji run ini (payload perintah langsung; sesuai pola C13 skill lain).  
- Hanya **satu** pesan Telegram terjadwal (tanpa pesan tester tambahan).

## Pesan Telegram (≤3 untuk skill)

1. Bot → rekap pengingat terjadwal (msg **1366**, delivered ke topik 1365).
