# Uji jadwal Telegram sungguhan (2026-10-13)

**Skill:** `siyuan-sop` v1.0.10 (catalog; SKILL.md tidak diubah)  
**Penguji:** penguji otomatis Komunitech, independen  
**Bot:** bot uji Komunitech (gateway uji internal)  
**Grup uji:** grup uji Telegram internal  
**Verdik:** **LOLOS**

## Ringkasan

| Pertanyaan | Hasil |
|---|---|
| Jadwal terbuat (automations one-shot ~5 menit)? | Ya — job `b565e07c-a1c3-47f8-95c5-e482f085ba88`, `--at 5m`, `--delete-after-run` |
| Pesan jadwal tiba di grup uji Telegram internal? | Ya — pesan bot terkirim (log gateway: `outbound send ok`) |
| Tepat waktu? | Ya — run `2026-10-13T13:43:48Z` (~5 menit setelah pembuatan jadwal) |
| Isi sesuai (angka benar)? | Ya — **2 dokumen** basi, hook **UJI-JADWAL-HOOK-9922** cocok mock SiYuan uji & `siyuan.py lama --hari 90` independen |

## Cuplikan isi pesan terjadwal (dari log automations + verifikasi independen)

```
DOKUMEN BELUM DIPERBARUI > 90 HARI (2 dokumen)
- /SOP/UJI-JADWAL-HOOK-9922  (terakhir: 20260115080000)
- /SOP/Packing Pesanan  (terakhir: 20260601090000)
```

## Lingkungan uji

- Mock kernel SiYuan di `127.0.0.1:6806` (2 SOP basi, salah satunya dokumen penanda uji jadwal; kunci uji di `~/.komunitech/siyuan-kunci.txt` HOME gateway).  
- Skill aktif di home gateway (`siyuan-sop` disalin ke `~/.openclaw/skills/`).  
- Pola `references/openclaw-jadwal.md`: `openclaw automations add --at 5m` + `--command-argv` `siyuan.py --url http://127.0.0.1:6806 lama --hari 90` + `--announce --channel telegram --to <ID-grup-uji> --thread-id <ID-thread-uji>`.  
- Job dihapus otomatis setelah run (`deleteAfterRun: true`).

## Cacat / catatan

- Cron **Senin 08.00 WIB** berulang (§ openclaw-jadwal) **tidak** diuji run ini (fokus one-shot command-argv; sama pola uji jadwal skill lain).  
- Mock API, bukan SiYuan desktop asli — cukup membuktikan jadwal + pengiriman Telegram + isi `lama`.  
- Hanya **satu** pesan Telegram terjadwal (tanpa pesan tester tambahan).

## Pesan Telegram dalam uji

1. Bot → daftar SOP basi terjadwal (delivered ke grup uji Telegram internal).
