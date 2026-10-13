# Uji jadwal Telegram sungguhan — C13 (2026-10-13)

**Skill:** `siyuan-sop` v1.0.10 (catalog; SKILL.md tidak diubah)  
**Penguji:** Akun C (Cursor Cloud), independen  
**Bot:** @KTclaude1_bot (gateway VM Cursor)  
**Grup uji:** `-1004407409583`, topik forum **1380** — `C13 siyuan-sop — jadwal`  
**Verdik:** **LOLOS**

## Ringkasan

| Pertanyaan | Hasil |
|---|---|
| Jadwal terbuat (automations one-shot ~5 menit)? | Ya — job `b565e07c-a1c3-47f8-95c5-e482f085ba88`, `--at 5m`, `--delete-after-run` |
| Pesan jadwal tiba di topik uji? | Ya — pesan bot **1381** (log gateway: `outbound send ok`, `threadId=1380`) |
| Tepat waktu? | Ya — run `2026-10-13T13:43:48Z` (~5 menit setelah pembuatan jadwal) |
| Isi sesuai (angka benar)? | Ya — **2 dokumen** basi, hook **C13-JADWAL-HOOK-9922** cocok mock SiYuan uji & `siyuan.py lama --hari 90` independen |

## Cuplikan isi pesan terjadwal (msg 1381, dari log automations + verifikasi independen)

```
DOKUMEN BELUM DIPERBARUI > 90 HARI (2 dokumen)
- /SOP/C13-JADWAL-HOOK-9922  (terakhir: 20260115080000)
- /SOP/Packing Pesanan  (terakhir: 20260601090000)
```

## Lingkungan uji

- Mock kernel SiYuan di `127.0.0.1:6806` (2 SOP basi + hook C13; kunci uji di `~/.komunitech/siyuan-kunci.txt` HOME gateway).  
- Skill aktif di home gateway (`siyuan-sop` disalin ke `~/.openclaw/skills/`).  
- Pola `references/openclaw-jadwal.md`: `openclaw automations add --at 5m` + `--command-argv` `siyuan.py --url http://127.0.0.1:6806 lama --hari 90` + `--announce --channel telegram --to -1004407409583 --thread-id 1380`.  
- Job dihapus otomatis setelah run (`deleteAfterRun: true`).

## Cacat / catatan

- Cron **Senin 08.00 WIB** berulang (§ openclaw-jadwal) **tidak** diuji run ini (fokus one-shot command-argv; sama pola C13 skill lain).  
- Mock API, bukan SiYuan desktop asli — cukup membuktikan jadwal + pengiriman Telegram + isi `lama`.  
- Hanya **satu** pesan Telegram terjadwal (tanpa pesan tester tambahan).

## Pesan Telegram (≤3 untuk skill)

1. Bot → daftar SOP basi terjadwal (msg **1381**, delivered ke topik 1380).
