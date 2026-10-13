# Uji jadwal Telegram sungguhan (2026-10-13)

**Skill:** `laporan-iklan-mingguan` v1.0.10 (catalog; SKILL.md tidak diubah)  
**Penguji:** penguji otomatis Komunitech, independen  
**Bot:** bot uji Komunitech (gateway uji internal)  
**Grup uji:** grup uji Telegram internal  
**Verdik:** **LOLOS**

## Ringkasan

| Pertanyaan | Hasil |
|---|---|
| Jadwal terbuat (automations one-shot ~5 menit)? | Ya — job `51a48287-5f8a-4593-b655-fe37f23b0ad3`, `--at 5m`, `--delete-after-run` |
| Pesan jadwal tiba di grup uji Telegram internal? | Ya — pesan bot terkirim (log gateway: `outbound send ok`, `deliveryStatus: delivered`) |
| Tepat waktu? | Ya — run `2026-10-13T14:13:41Z` (~5 menit setelah pembuatan jadwal) |
| Isi sesuai (angka benar)? | Ya — **Rp 250.000** belanja, **10 pesan WA**, hook **UJI-JADWAL-HOOK-5544** cocok CSV uji & `laporan_iklan.py` independen |

## Cuplikan isi pesan terjadwal (dari riwayat run automations)

```
LAPORAN IKLAN MINGGUAN — Meta Ads (Facebook/Instagram)
Periode: 2026-10-06 s.d. 2026-10-12
…
Total belanja iklan: Rp 250.000
… Pesan WA: 10
Biaya per pesan WA: Rp 25.000
…
1. UJI-JADWAL-HOOK-5544: Rp 25.000/pesan WA (10 pesan WA, Rp 250.000)
```

## Lingkungan uji

- Ekspor Meta fiktif: `laporan/masuk/iklan/meta-minggu-ini.csv` + `meta-minggu-lalu.csv` di HOME gateway (1 iklan dengan hook uji per file).  
- Skill aktif di home gateway (`laporan-iklan-mingguan` disalin ke `~/.openclaw/skills/`).  
- Pola **§3a** `references/openclaw-jadwal.md` (command-argv, tanpa AI): `openclaw automations add --at 5m` + `--command-argv` `laporan_iklan.py analisis … --sebelumnya … --nama-hasil "pesan WA"` + `--announce --channel telegram --to <ID-grup-uji> --thread-id <ID-thread-uji>`.  
- Job dihapus otomatis setelah run (`deleteAfterRun: true`).

## Cacat / catatan

- Cron **Senin 07.50 WIB** berulang (§3a) dan Bentuk A (agent isolated) **tidak** diuji run ini (fokus one-shot command-argv; sama pola uji jadwal skill script lain).  
- Hanya **satu** pesan Telegram terjadwal (tanpa pesan tester tambahan).

## Pesan Telegram dalam uji

1. Bot → laporan iklan mingguan terjadwal (delivered ke grup uji Telegram internal).
