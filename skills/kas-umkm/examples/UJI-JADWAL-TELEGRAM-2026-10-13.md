# Uji jadwal Telegram sungguhan — C13 (2026-10-13)

**Skill:** `kas-umkm` v1.0.12 (catalog; SKILL.md tidak diubah)  
**Penguji:** Akun C (Cursor Cloud), independen  
**Bot:** @KTclaude1_bot (gateway VM Cursor)  
**Grup uji:** `-1004407409583`, topik forum **1331** — `C13 kas-umkm — jadwal`  
**Verdik:** **LOLOS**

## Ringkasan

| Pertanyaan | Hasil |
|---|---|
| Jadwal terbuat (automations one-shot ~5 menit)? | Ya — job `143c62a6-4076-4d4a-8dd6-ba1bb189703d`, `--at 5m`, `--delete-after-run` |
| Pesan jadwal tiba di topik uji? | Ya — pesan bot **1335** (log gateway: `deliveryStatus: delivered`) |
| Tepat waktu? | Ya — run `2026-10-13T08:19:33Z` (~5 menit setelah pembuatan jadwal) |
| Isi sesuai (angka benar)? | Ya — **HASIL USAHA Rp 900.000**, total saldo **Rp 1.400.000** cocok database uji & hitungan independen `kas.py rekap` |

## Cuplikan isi pesan terjadwal (msg 1335)

```
BUKU KAS Warung C13 Uji
Rekap harian Selasa, 13/10/2026

UANG MASUK: Rp 975.000
UANG KELUAR: Rp 75.000
HASIL USAHA …: Rp 900.000
…
Total: Rp 1.400.000 (awal periode Rp 500.000, naik Rp 900.000)
```

## Lingkungan uji

- Database fiktif: `~/KomunitechData/kas/kas-c13.db` di HOME gateway (init + 3 transaksi + akun BRI/QRIS).  
- Skill aktif di home gateway (symlink `kas-umkm`).  
- Pola **Pilihan 1** `references/openclaw-jadwal.md`: `openclaw automations add` + `--command-argv` `rekap --tanggal hari-ini` + `--announce --channel telegram --to -1004407409583 --thread-id 1331`.  
- Config topik 1331: hanya skill `kas-umkm` (backup `openclaw.json.bak-c13-*` di HOME uji, tidak di repo).

## Cacat / catatan

- Alur konfirmasi "Lanjut? (ya/tidak)" lewat chat bot **tidak** diuji run ini (jadwal dibuat langsung setelah data uji siap; isi delivery identik dengan skill).  
- Pesan **1334** = balasan bot terhadap permintaan uji tester (**1332**); laporan terjadwal = **1335**.

## Pesan Telegram (≤3 untuk skill)

1. Tester → topik 1331: permintaan uji C13 + konteks data (msg **1332**).  
2. Bot → balasan singkat (msg **1334**, log gateway).  
3. Bot → rekap terjadwal (msg **1335**).
