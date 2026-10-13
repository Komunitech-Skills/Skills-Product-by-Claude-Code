# Uji jadwal Telegram sungguhan (2026-10-13)

**Skill:** `kasir-lokal` v1.1.7 (catalog; SKILL.md tidak diubah)  
**Penguji:** penguji otomatis Komunitech, independen  
**Bot:** bot uji Komunitech (gateway uji internal)  
**Grup uji:** grup uji Telegram internal  
**Verdik:** **LOLOS**

## Ringkasan

| Pertanyaan | Hasil |
|---|---|
| Jadwal terbuat (automations one-shot ~5 menit)? | Ya — job `a9882e2e-6581-4e58-a10b-396f896a6005`, `--at 5m`, `--delete-after-run` |
| Pesan jadwal tiba di grup uji Telegram internal? | Ya — pesan bot terkirim (log gateway: `deliveryStatus: delivered`) |
| Tepat waktu? | Ya — run `2026-10-13T09:23:18Z` (~5 menit setelah pembuatan jadwal) |
| Isi sesuai (angka benar)? | Ya — **penjualan bersih Rp 51.000**, 1 nota, produk terlaris Kopi Susu/Roti Bakar cocok database uji & `kasir.py rekap` independen |

## Cuplikan isi pesan terjadwal

```
REKAP KASIR Selasa, 13/10/2026
Warung UJI Uji
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

- Database fiktif di folder data skill (`KomunitechData/kasir/`) pada HOME gateway (init, buka kasir Rp 200.000, 1 transaksi tunai).  
- Skill aktif di home gateway (`skills install` kasir-lokal).  
- Pola **Pilihan 1** `references/openclaw-jadwal.md`: `openclaw automations add` + `--command-argv` `rekap --tanggal hari-ini --db …` + `--announce --channel telegram --to <ID-grup-uji> --thread-id <ID-thread-uji>`.  
- Konfigurasi grup uji: hanya skill `kasir-lokal` (cadangan konfigurasi: catatan internal kurator, tidak disertakan dalam paket).

## Cacat / catatan

- Alur konfirmasi "Lanjut? (ya/tidak)" lewat chat bot **tidak** diuji run ini (jadwal dibuat langsung penguji setelah data siap; pola produksi memakai payload perintah tanpa model).  
- Selain laporan terjadwal, ada satu pesan balasan bot terhadap permintaan penguji (pesan terpisah).

## Pesan Telegram dalam uji

1. Penguji → grup uji Telegram internal: konteks uji jadwal.  
2. Bot → balasan singkat (dari log gateway).  
3. Bot → rekap terjadwal.
