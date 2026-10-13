# Uji jadwal Telegram sungguhan (2026-10-13)

**Skill:** `umami-analitik` v1.0.6 (catalog; SKILL.md tidak diubah)  
**Penguji:** penguji otomatis Komunitech, independen  
**Bot:** bot uji Komunitech (gateway uji internal)  
**Grup uji:** grup uji Telegram internal  
**Verdik:** **LOLOS**

## Ringkasan

| Pertanyaan | Hasil |
|---|---|
| Jadwal terbuat (automations one-shot ~5 menit)? | Ya — job `026bdfb1-51e0-4f5c-9516-3d2c85f50ba2`, `--at 5m`, `--delete-after-run` |
| Pesan jadwal tiba di grup uji Telegram internal? | Ya — pesan bot terkirim (log gateway: `outbound send ok`, `deliveryStatus: delivered`) |
| Tepat waktu? | Ya — run `2026-10-13T15:13:25Z` (~5 menit setelah pembuatan jadwal) |
| Isi sesuai (angka benar)? | Ya — **11 pengunjung unik**, **12 kunjungan**, **23 tayangan** cocok `umami.py laporan-mingguan` independen (mock Umami 3.4.0, `--sekarang 2026-09-29T16:00`) |

## Cuplikan isi pesan terjadwal (dari summary automations)

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
- Pola **Pilihan 1** `references/openclaw-jadwal.md` (command-argv, tanpa AI): `openclaw automations add --at 5m` + `--command-argv` `umami.py laporan-mingguan --situs keripikbusri.contoh.id --sekarang 2026-09-29T16:00 --url http://127.0.0.1:3000` + `--command-env UMAMI_URL=…` + `--announce --channel telegram --to <ID-grup-uji> --thread-id <ID-thread-uji>`.  
- Job dihapus otomatis setelah run (`deleteAfterRun: true`).

## Cacat / catatan

- Cron **Senin 07.00 WIB** berulang (§ openclaw-jadwal Pilihan 1) **tidak** diuji run ini (fokus one-shot command-argv; sama pola uji jadwal skill lain).  
- Mock API, bukan Umami Docker asli di komputer pembeli — cukup membuktikan jadwal + pengiriman Telegram + isi `laporan-mingguan`.  
- Hanya **satu** pesan Telegram terjadwal (tanpa pesan tester tambahan).

## Pesan Telegram dalam uji

1. Bot → laporan web mingguan terjadwal (delivered ke grup uji Telegram internal).
