# Uji jadwal Telegram sungguhan — C13 (2026-10-13)

**Skill:** `buku-piutang` v1.0.4 (catalog; SKILL.md tidak diubah)  
**Penguji:** Akun C (Cursor Cloud), independen  
**Bot:** @KTclaude1_bot (gateway VM Cursor)  
**Grup uji:** `-1004407409583`, topik forum **1359** — `C13 buku-piutang — jadwal`  
**Verdik:** **LOLOS**

## Ringkasan

| Pertanyaan | Hasil |
|---|---|
| Jadwal terbuat (automations one-shot ~5 menit)? | Ya — job `3ceb04fb-f348-4234-9e40-cf3f5bc966d7`, `--at 5m`, `--delete-after-run` |
| Pesan jadwal tiba di topik uji? | Ya — log gateway: `deliveryStatus: delivered`, thread 1359 |
| Tepat waktu? | Ya — run `2026-10-13T10:13:00Z` (~5 menit setelah pembuatan jadwal) |
| Isi sesuai (angka benar)? | Ya — **total piutang Rp 1.300.000**, **terlewat Rp 800.000** cocok database uji & `piutang.py ringkasan --samarkan` independen |

## Cuplikan isi pesan terjadwal

```
RINGKASAN PIUTANG Toko C13 Uji - Selasa, 13 Oktober 2026 (WIB)
Total piutang: Rp 1.300.000 (2 nota, 2 pelanggan)
Terlewat: Rp 800.000 (1 nota) | Hari ini: Rp 0 (0) | 7 hari ke depan: Rp 0 (0)
…
TERLEWAT (1 nota, Rp 800.000)
1. B-C13-2 | Kafe S. (P0002) | sisa Rp 800.000 | JT 8 Okt 2026 (lewat 5 hari)
```

## Lingkungan uji

- Database fiktif: `KomunitechData/piutang/piutang-c13.db` di HOME gateway (init + 2 nota bon).  
- Skill aktif di home gateway (`buku-piutang` disalin ke `~/.openclaw/skills/`).  
- Pola **Pilihan 1** `references/openclaw-jadwal.md`: `openclaw automations add` + `--command-argv` `ringkasan --samarkan --db …` + `--announce --channel telegram --to -1004407409583 --thread-id 1359`.  
- Config topik 1359: hanya skill `buku-piutang` (backup `openclaw.json.bak-c13-piutang-*` di HOME uji, tidak di repo).

## Cacat / catatan

- Alur konfirmasi "Lanjut? (ya/tidak)" lewat chat bot **tidak** diuji run ini (jadwal payload perintah langsung; sesuai pola C13 skill lain).  
- Hanya **satu** pesan Telegram terjadwal (tanpa pesan tester tambahan).

## Pesan Telegram (≤3 untuk skill)

1. Bot → ringkasan piutang terjadwal (delivered ke topik 1359).
