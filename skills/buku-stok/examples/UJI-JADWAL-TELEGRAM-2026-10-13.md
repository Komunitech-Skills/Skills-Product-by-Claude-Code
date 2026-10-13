# Uji jadwal Telegram sungguhan (2026-10-13)

**Skill:** `buku-stok` v1.1.6 (catalog; SKILL.md tidak diubah)  
**Penguji:** penguji otomatis Komunitech, independen  
**Bot:** bot uji Komunitech (gateway uji internal)  
**Grup uji:** grup uji Telegram internal  
**Verdik:** **LOLOS**

## Ringkasan

| Pertanyaan | Hasil |
|---|---|
| Jadwal terbuat (automations one-shot ~5 menit)? | Ya — job `04d9a585-089b-4562-b090-a22fcf0e8025`, `--at 5m`, `--delete-after-run` |
| Pesan jadwal tiba di grup uji Telegram internal? | Ya — pesan bot terkirim (log gateway: `deliveryStatus: delivered`) |
| Tepat waktu? | Ya — run `2026-10-13T09:41:42Z` (~5 menit setelah pembuatan jadwal) |
| Isi sesuai (angka benar)? | Ya — **omzet Rp 150.000**, terjual 3 pcs, HPP Rp 90.000 cocok database uji & `stok.py laporan ringkas` independen |

## Cuplikan isi pesan terjadwal

```
Laporan Stok Harian - 13/10/2026
Terjual: 3 barang (marketplace 0 dari 0 pesanan, toko/offline 3)
Omzet tercatat: Rp 150.000 | HPP: Rp 90.000 | Laba kotor (perkiraan): Rp 60.000
Terlaris: KAOS-UJI (3)
…
Nilai persediaan: Rp 510.000
```

## Lingkungan uji

- Database fiktif di folder data skill (`KomunitechData/stok/`) pada HOME gateway (init + 1 SKU + 3 pcs keluar jual).  
- Skill aktif di home gateway (`skills install` buku-stok).  
- Pola **command-argv** (setara Pilihan 1 kasir/kas-umkm): `openclaw automations add` + `laporan ringkas --db …` + `--announce --channel telegram --to <ID-grup-uji> --thread-id <ID-thread-uji>`.  
- Konfigurasi grup uji: hanya skill `buku-stok` (cadangan konfigurasi: catatan internal kurator, tidak disertakan dalam paket).

## Cacat / catatan

- Alur konfirmasi "Lanjut? (ya/tidak)" lewat chat bot **tidak** diuji run ini (jadwal payload perintah langsung; SKILL.md juga menawarkan jalur agentTurn — keduanya hanya baca laporan).  
- Selain laporan terjadwal, ada satu pesan balasan bot terhadap permintaan penguji (pesan terpisah).

## Pesan Telegram dalam uji

1. Penguji → grup uji Telegram internal: konteks uji jadwal.  
2. Bot → balasan singkat (dari log gateway).  
3. Bot → laporan terjadwal.
