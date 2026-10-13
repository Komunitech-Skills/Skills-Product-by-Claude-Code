# Uji jadwal Telegram sungguhan — C13 (2026-10-13)

**Skill:** `vikunja-tugas` v1.0.13 (catalog; SKILL.md tidak diubah)  
**Penguji:** Akun C (Cursor Cloud), independen  
**Bot:** @KTclaude1_bot (gateway VM Cursor)  
**Grup uji:** `-1004407409583`, topik forum **1393** — `C13 vikunja-tugas — jadwal`  
**Verdik:** **LOLOS**

## Ringkasan

| Pertanyaan | Hasil |
|---|---|
| Jadwal terbuat (automations one-shot ~5 menit)? | Ya — job `99cb652d-6132-4613-8f74-155e7b11c719`, `--at 5m`, `--delete-after-run` |
| Pesan jadwal tiba di topik uji? | Ya — pesan bot **1394** (log gateway: `outbound send ok`, `threadId=1393`) |
| Tepat waktu? | Ya — run ~15:43 UTC (WIB 22:43), ~5 menit setelah pembuatan jadwal |
| Isi sesuai (angka benar)? | Ya — **1 tugas terlambat**, judul **Tagih pelanggan telat**, proyek **Toko Bangunan Sinar Jaya**, PIC **budi** cocok `vikunja.py terlambat` independen (mock Vikunja 2.6.0 tiruan, `127.0.0.1:3456`) |

## Cuplikan isi pesan terjadwal (msg 1394, dari output command + log delivery)

```
TUGAS TERLAMBAT
Proyek: semua proyek
Jumlah: 1
…
- Tagih pelanggan telat (jatuh tempo 3 Okt 2026; proyek: Toko Bangunan Sinar Jaya; PIC: budi)
```

## Lingkungan uji

- Mock Vikunja tiruan di `127.0.0.1:3456` (fixture `tests/fixtures/vikunja-2.6.0.json`, handler sama `uji_regresi.py`).  
- Token baca-saja uji di `~/.komunitech/vikunja-kunci.txt` HOME gateway (bukan token produksi).  
- Skill aktif di home gateway (`vikunja-tugas` disalin ke `~/.openclaw/skills/`).  
- Pola **Pilihan 1** `references/openclaw-jadwal.md`: `openclaw automations add --at 5m` + `--command-argv` `vikunja.py terlambat --tz WIB` + `--announce --channel telegram --to -1004407409583 --thread-id 1393`.  
- Job dihapus otomatis setelah run (`deleteAfterRun: true`).

## Cacat / catatan

- Cron **07.00 / 07.05 WIB** berulang (§ openclaw-jadwal) **tidak** diuji run ini (fokus one-shot `terlambat`; `hari-ini` kosong pada mock default).  
- Mock API, bukan Vikunja binary asli — cukup membuktikan jadwal + pengiriman Telegram + isi perintah baca.  
- Hanya **satu** pesan Telegram terjadwal (tanpa pesan tester tambahan).

## Pesan Telegram (≤3 untuk skill)

1. Bot → laporan `terlambat` terjadwal (msg **1394**, delivered ke topik 1393).
