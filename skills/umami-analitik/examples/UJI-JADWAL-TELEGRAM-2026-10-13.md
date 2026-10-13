# Uji jadwal Telegram sungguhan — C13 (2026-10-13)

**Skill:** `umami-analitik` v1.0.6 (catalog; SKILL.md tidak diubah)  
**Penguji:** Akun C (Cursor Cloud), independen  
**Bot:** @KTclaude1_bot (gateway VM Cursor)  
**Grup uji:** `-1004407409583`, topik forum **1390** — `C13 umami-analitik — jadwal`  
**Verdik:** **LOLOS**

## Ringkasan

| Pertanyaan | Hasil |
|---|---|
| Jadwal terbuat (automations one-shot ~5 menit)? | Ya — job `026bdfb1-51e0-4f5c-9516-3d2c85f50ba2`, `--at 5m`, `--delete-after-run` |
| Pesan jadwal tiba di topik uji? | Ya — pesan bot **1391** (log gateway: `outbound send ok`, `deliveryStatus: delivered`, `threadId=1390`) |
| Tepat waktu? | Ya — run `2026-10-13T15:13:25Z` (~5 menit setelah pembuatan jadwal) |
| Isi sesuai (angka benar)? | Ya — **11 pengunjung unik**, **12 kunjungan**, **23 tayangan** cocok `umami.py laporan-mingguan` independen (mock Umami 3.4.0, `--sekarang 2026-09-29T16:00`) |

## Cuplikan isi pesan terjadwal (msg 1391, dari summary automations)

```
Laporan web Keripik Bu Sri (landing) (keripikbusri.contoh.id)
Periode: minggu lalu, Senin 21 Sep 2026 - Minggu 27 Sep 2026
…
- Pengunjung unik       : 11   (sebelumnya 4; naik 7 (+175%))
- Kunjungan             : 12   (sebelumnya 4; naik 8 (+200%))
- Tayangan halaman      : 23   (sebelumnya 6; naik 17 (+283%))
…
- klik-wa: 3x oleh 3 pengunjung (27,3%); sebelumnya 1x
```

## Lingkungan uji

- Mock Umami 3.4.0 tiruan di `127.0.0.1:3000` (fixture `tests/fixtures/umami-3.4.0.json`; kunci view-only uji di `~/.komunitech/umami-kunci.txt` HOME gateway).  
- Skill aktif di home gateway (`umami-analitik` disalin ke `~/.openclaw/skills/`).  
- Pola **Pilihan 1** `references/openclaw-jadwal.md` (command-argv, tanpa AI): `openclaw automations add --at 5m` + `--command-argv` `umami.py laporan-mingguan --situs keripikbusri.contoh.id --sekarang 2026-09-29T16:00 --url http://127.0.0.1:3000` + `--command-env UMAMI_URL=…` + `--announce --channel telegram --to -1004407409583 --thread-id 1390`.  
- Job dihapus otomatis setelah run (`deleteAfterRun: true`).

## Cacat / catatan

- Cron **Senin 07.00 WIB** berulang (§ openclaw-jadwal Pilihan 1) **tidak** diuji run ini (fokus one-shot command-argv; sama pola C13 skill lain).  
- Mock API, bukan Umami Docker asli di komputer pembeli — cukup membuktikan jadwal + pengiriman Telegram + isi `laporan-mingguan`.  
- Hanya **satu** pesan Telegram terjadwal (tanpa pesan tester tambahan).

## Pesan Telegram (≤3 untuk skill)

1. Bot → laporan web mingguan terjadwal (msg **1391**, delivered ke topik 1390).
