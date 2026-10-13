# Uji jadwal Telegram sungguhan — C13 (2026-10-13)

**Skill:** `laporan-iklan-mingguan` v1.0.10 (catalog; SKILL.md tidak diubah)  
**Penguji:** Akun C (Cursor Cloud), independen  
**Bot:** @KTclaude1_bot (gateway VM Cursor)  
**Grup uji:** `-1004407409583`, topik forum **1384** — `C13 laporan-iklan-mingguan — jadwal`  
**Verdik:** **LOLOS**

## Ringkasan

| Pertanyaan | Hasil |
|---|---|
| Jadwal terbuat (automations one-shot ~5 menit)? | Ya — job `51a48287-5f8a-4593-b655-fe37f23b0ad3`, `--at 5m`, `--delete-after-run` |
| Pesan jadwal tiba di topik uji? | Ya — pesan bot **1385** (log gateway: `outbound send ok`, `deliveryStatus: delivered`, `threadId=1384`) |
| Tepat waktu? | Ya — run `2026-10-13T14:13:41Z` (~5 menit setelah pembuatan jadwal) |
| Isi sesuai (angka benar)? | Ya — **Rp 250.000** belanja, **10 pesan WA**, hook **C13-JADWAL-HOOK-5544** cocok CSV uji & `laporan_iklan.py` independen |

## Cuplikan isi pesan terjadwal (msg 1385, dari riwayat run automations)

```
LAPORAN IKLAN MINGGUAN — Meta Ads (Facebook/Instagram)
Periode: 2026-10-06 s.d. 2026-10-12
…
Total belanja iklan: Rp 250.000
… Pesan WA: 10
Biaya per pesan WA: Rp 25.000
…
1. C13-JADWAL-HOOK-5544: Rp 25.000/pesan WA (10 pesan WA, Rp 250.000)
```

## Lingkungan uji

- Ekspor Meta fiktif: `laporan/masuk/iklan/meta-minggu-ini.csv` + `meta-minggu-lalu.csv` di HOME gateway (1 iklan hook C13 per file).  
- Skill aktif di home gateway (`laporan-iklan-mingguan` disalin ke `~/.openclaw/skills/`).  
- Pola **§3a** `references/openclaw-jadwal.md` (command-argv, tanpa AI): `openclaw automations add --at 5m` + `--command-argv` `laporan_iklan.py analisis … --sebelumnya … --nama-hasil "pesan WA"` + `--announce --channel telegram --to -1004407409583 --thread-id 1384`.  
- Job dihapus otomatis setelah run (`deleteAfterRun: true`).

## Cacat / catatan

- Cron **Senin 07.50 WIB** berulang (§3a) dan Bentuk A (agent isolated) **tidak** diuji run ini (fokus one-shot command-argv; sama pola C13 skill script lain).  
- Hanya **satu** pesan Telegram terjadwal (tanpa pesan tester tambahan).

## Pesan Telegram (≤3 untuk skill)

1. Bot → laporan iklan mingguan terjadwal (msg **1385**, delivered ke topik 1384).
