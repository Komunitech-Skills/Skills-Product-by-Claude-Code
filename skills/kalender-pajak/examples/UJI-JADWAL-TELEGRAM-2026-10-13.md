# Uji jadwal Telegram sungguhan — C13 (2026-10-13)

**Skill:** `kalender-pajak` v1.0.7 (catalog; SKILL.md tidak diubah)  
**Penguji:** Akun C (Cursor Cloud), independen  
**Bot:** @KTclaude1_bot (gateway VM Cursor)  
**Grup uji:** `-1004407409583`, topik forum **1387** — `C13 kalender-pajak — jadwal`  
**Verdik:** **LOLOS**

## Ringkasan

| Pertanyaan | Hasil |
|---|---|
| Jadwal terbuat (automations one-shot ~5 menit)? | Ya — job `656743c0-626c-424f-b24a-4f1df0443147`, `--at 5m`, `--delete-after-run` (dihapus setelah uji) |
| Pesan jadwal tiba di topik uji? | Ya — pesan bot **1388** (log gateway: `outbound send ok`, `deliveryStatus: delivered`, `threadId=1387`) |
| Tepat waktu? | Ya — run manual verifikasi `2026-10-13T14:39:11Z` (~5 menit setelah pembuatan jadwal; jadwal asli `--at` 14:44Z) |
| Isi sesuai (angka benar)? | Ya — **4 baris tenggat** (15 & 20 Okt 2026) + tenggat berikutnya **2 Nov 2026** cocok `kalender_pajak.py` independen (`--profil badan-pkp,pemberi-kerja --hari-ini 2026-10-13 --rentang 10`) |

## Cuplikan isi pesan terjadwal (msg 1388, dari summary automations)

```
## Tenggat pajak 10 hari ke depan (Selasa, 13 Oktober 2026 s.d. Jumat, 23 Oktober 2026) - badan-pkp, pemberi-kerja
| 2 hari lagi | Kamis, 15 Oktober 2026 | SETOR PPh 21/26 (pemberi kerja) masa Sep 2026 |
| 7 hari lagi | Selasa, 20 Oktober 2026 | UNGGAH faktur pajak keluaran bulan Sep 2026 (batas persetujuan DJP) |
Tenggat berikutnya … Senin, 2 November 2026 … SETOR & LAPOR PPN masa Sep 2026
```

## Lingkungan uji

- Skill aktif di home gateway (`kalender-pajak` disalin ke `~/.openclaw/skills/`).  
- Pola **§2** `references/openclaw-jadwal.md` (command-argv, tanpa AI): `openclaw automations add --at 5m` + `--command-argv` `kalender_pajak.py --profil badan-pkp,pemberi-kerja --hari-ini hari-ini --rentang 10` + `--announce --channel telegram --to -1004407409583 --thread-id 1387`.  
- Job dihapus setelah uji (`automations rm`).

## Cacat / catatan

- Cron **tanggal 1/10/24, 07.00 WIB** berulang (§2 a–c) **tidak** diuji run ini (fokus one-shot command-argv; sama pola C13 skill script lain).  
- Alur konfirmasi "Lanjut? (ya/tidak)" lewat chat bot **tidak** diuji (jadwal dibuat langsung setelah skill siap).  
- Hanya **satu** pesan Telegram terjadwal (tanpa pesan tester tambahan).

## Pesan Telegram (≤3 untuk skill)

1. Bot → tabel tenggat pajak terjadwal (msg **1388**, delivered ke topik 1387).
