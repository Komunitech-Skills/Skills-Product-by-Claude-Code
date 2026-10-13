# Uji jadwal Telegram sungguhan — C13 (2026-10-13)

**Skill:** `buku-stok` v1.1.6 (catalog; SKILL.md tidak diubah)  
**Penguji:** Akun C (Cursor Cloud), independen  
**Bot:** @KTclaude1_bot (gateway VM Cursor)  
**Grup uji:** `-1004407409583`, topik forum **1353** — `C13 buku-stok — jadwal`  
**Verdik:** **LOLOS**

## Ringkasan

| Pertanyaan | Hasil |
|---|---|
| Jadwal terbuat (automations one-shot ~5 menit)? | Ya — job `04d9a585-089b-4562-b090-a22fcf0e8025`, `--at 5m`, `--delete-after-run` |
| Pesan jadwal tiba di topik uji? | Ya — pesan bot **1357** (log gateway: `deliveryStatus: delivered`) |
| Tepat waktu? | Ya — run `2026-10-13T09:41:42Z` (~5 menit setelah pembuatan jadwal) |
| Isi sesuai (angka benar)? | Ya — **omzet Rp 150.000**, terjual 3 pcs, HPP Rp 90.000 cocok database uji & `stok.py laporan ringkas` independen |

## Cuplikan isi pesan terjadwal (msg 1357)

```
Laporan Stok Harian - 13/10/2026
Terjual: 3 barang (marketplace 0 dari 0 pesanan, toko/offline 3)
Omzet tercatat: Rp 150.000 | HPP: Rp 90.000 | Laba kotor (perkiraan): Rp 60.000
Terlaris: KAOS-C13 (3)
…
Nilai persediaan: Rp 510.000
```

## Lingkungan uji

- Database fiktif: `KomunitechData/stok/stok-c13.db` di HOME gateway (init + 1 SKU + 3 pcs keluar jual).  
- Skill aktif di home gateway (`skills install` buku-stok).  
- Pola **command-argv** (setara Pilihan 1 kasir/kas-umkm): `openclaw automations add` + `laporan ringkas --db …` + `--announce --channel telegram --to -1004407409583 --thread-id 1353`.  
- Config topik 1353: hanya skill `buku-stok` (backup `openclaw.json.bak-c13-bukustok-*` di HOME uji, tidak di repo).

## Cacat / catatan

- Alur konfirmasi "Lanjut? (ya/tidak)" lewat chat bot **tidak** diuji run ini (jadwal payload perintah langsung; SKILL.md juga menawarkan jalur agentTurn — keduanya hanya baca laporan).  
- Pesan **1356** = balasan bot terhadap permintaan tester (**1354**); laporan terjadwal = **1357**.

## Pesan Telegram (≤3 untuk skill)

1. Tester → topik 1353: konteks uji C13 (msg **1354**).  
2. Bot → balasan singkat (msg **1356**, log gateway).  
3. Bot → laporan terjadwal (msg **1357**).
