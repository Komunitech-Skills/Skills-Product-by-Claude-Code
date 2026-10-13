# Uji jadwal Telegram sungguhan — C13 (2026-10-13)

**Skill:** `kasir-lokal` v1.1.7 (catalog; SKILL.md tidak diubah)  
**Penguji:** Akun C (Cursor Cloud), independen  
**Bot:** @KTclaude1_bot (gateway VM Cursor)  
**Grup uji:** `-1004407409583`, topik forum **1343** — `C13 kasir-lokal — jadwal`  
**Verdik:** **LOLOS**

## Ringkasan

| Pertanyaan | Hasil |
|---|---|
| Jadwal terbuat (automations one-shot ~5 menit)? | Ya — job `a9882e2e-6581-4e58-a10b-396f896a6005`, `--at 5m`, `--delete-after-run` |
| Pesan jadwal tiba di topik uji? | Ya — pesan bot **1346** (log gateway: `deliveryStatus: delivered`) |
| Tepat waktu? | Ya — run `2026-10-13T09:23:18Z` (~5 menit setelah pembuatan jadwal) |
| Isi sesuai (angka benar)? | Ya — **penjualan bersih Rp 51.000**, 1 nota, produk terlaris Kopi Susu/Roti Bakar cocok database uji & `kasir.py rekap` independen |

## Cuplikan isi pesan terjadwal (msg 1346)

```
REKAP KASIR Selasa, 13/10/2026
Warung C13 Uji
Nota jual: 1
Penjualan kotor : Rp 51.000
…
Penjualan bersih: Rp 51.000
…
Produk terlaris (penjualan bersih):
1. Kopi Susu - 2 pcs - Rp 36.000
2. Roti Bakar - 1 pcs - Rp 15.000
```

## Lingkungan uji

- Database fiktif: `KomunitechData/kasir/kasir-c13.db` di HOME gateway (init, buka kasir Rp 200.000, 1 transaksi tunai).  
- Skill aktif di home gateway (`skills install` kasir-lokal).  
- Pola **Pilihan 1** `references/openclaw-jadwal.md`: `openclaw automations add` + `--command-argv` `rekap --tanggal hari-ini --db …` + `--announce --channel telegram --to -1004407409583 --thread-id 1343`.  
- Config topik 1343: hanya skill `kasir-lokal` (backup `openclaw.json.bak-c13-kasir-*` di HOME uji, tidak di repo).

## Cacat / catatan

- Alur konfirmasi "Lanjut? (ya/tidak)" lewat chat bot **tidak** diuji run ini (jadwal dibuat langsung penguji setelah data siap; pola produksi memakai payload perintah tanpa model).  
- Pesan **1347** = balasan bot terhadap permintaan tester (**1344**); laporan terjadwal = **1346**.

## Pesan Telegram (≤3 untuk skill)

1. Tester → topik 1343: konteks uji C13 (msg **1344**).  
2. Bot → balasan singkat (msg **1347**, log gateway).  
3. Bot → rekap terjadwal (msg **1346**).
