# Uji jadwal Telegram sungguhan — C13 (2026-10-13)

**Skill:** `fider-masukan-pelanggan` v1.0.9 (catalog; SKILL.md tidak diubah)  
**Penguji:** Akun C (Cursor Cloud), independen  
**Bot:** @KTclaude1_bot (gateway VM Cursor)  
**Grup uji:** `-1004407409583`, topik forum **1377** — `C13 fider-masukan-pelanggan — jadwal`  
**Verdik:** **LOLOS**

## Ringkasan

| Pertanyaan | Hasil |
|---|---|
| Jadwal terbuat (automations one-shot ~5 menit)? | Ya — job `f6d1dab8-9a37-4c68-abc4-24d5858720ac`, `--at 5m`, `--delete-after-run` |
| Pesan jadwal tiba di topik uji? | Ya — pesan bot **1378** (log gateway: `outbound send ok`, `threadId=1377`) |
| Tepat waktu? | Ya — run `2026-10-13T13:15:07Z` (~5 menit setelah pembuatan jadwal) |
| Isi sesuai (angka benar)? | Ya — **total 28 suara**, top **#4 C13-JADWAL-HOOK-8831** (11 suara) cocok mock Fider uji & `fider.py ringkasan-mingguan` independen |

## Cuplikan isi pesan terjadwal (msg 1378, dari keluaran command + verifikasi independen)

```
RINGKASAN MASUKAN PELANGGAN - 7 hari terakhir (per 13 Okt 2026)
- Pos aktif (terbuka/direncanakan/dikerjakan): 4, total 28 suara
…
TOP 5 SUARA TERBANYAK
1. #4 C13-JADWAL-HOOK-8831 fitur export CSV - 11 suara  (+11 minggu ini) [Terbuka]
2. #3 Laporan bulanan PDF - 9 suara  (+9 minggu ini) [Direncanakan]
…
```

## Lingkungan uji

- Mock Fider v0.38 tiruan di `127.0.0.1:3000` (data uji + pos hook C13; kunci uji di `~/.komunitech/fider-kunci.txt` HOME gateway).  
- Skill aktif di home gateway (`fider-masukan-pelanggan` disalin ke `~/.openclaw/skills/`).  
- Pola perintah langsung `references/openclaw-jadwal.md`: `openclaw automations add --at 5m` + `--command-argv` `fider.py ringkasan-mingguan --top 5 --url http://127.0.0.1:3000` + `--announce --channel telegram --to -1004407409583 --thread-id 1377`.  
- Job dihapus otomatis setelah run (`deleteAfterRun: true`).

## Cacat / catatan

- Cron **Senin 07.00 WIB** berulang (§ openclaw-jadwal) **tidak** diuji run ini (fokus one-shot command-argv; sama pola C13 skill lain).  
- Mock API, bukan Fider Docker asli di VPS — cukup membuktikan jadwal + pengiriman Telegram + isi `ringkasan-mingguan`.  
- Hanya **satu** pesan Telegram terjadwal (tanpa pesan tester tambahan).

## Pesan Telegram (≤3 untuk skill)

1. Bot → ringkasan mingguan terjadwal (msg **1378**, delivered ke topik 1377).
