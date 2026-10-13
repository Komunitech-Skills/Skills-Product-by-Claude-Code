# Uji jadwal Telegram sungguhan (2026-10-13)

**Skill:** `kas-umkm` v1.0.12 (catalog; SKILL.md tidak diubah)  
**Penguji:** penguji otomatis Komunitech, independen  
**Bot:** bot uji Komunitech (gateway uji internal)  
**Grup uji:** grup uji Telegram internal  
**Verdik:** **LOLOS**

## Ringkasan

| Pertanyaan | Hasil |
|---|---|
| Jadwal terbuat (automations one-shot ~5 menit)? | Ya — job `143c62a6-4076-4d4a-8dd6-ba1bb189703d`, `--at 5m`, `--delete-after-run` |
| Pesan jadwal tiba di grup uji Telegram internal? | Ya — pesan bot terkirim (log gateway: `deliveryStatus: delivered`) |
| Tepat waktu? | Ya — run `2026-10-13T08:19:33Z` (~5 menit setelah pembuatan jadwal) |
| Isi sesuai (angka benar)? | Ya — **HASIL USAHA Rp 900.000**, total saldo **Rp 1.400.000** cocok database uji & hitungan independen `kas.py rekap` |

## Cuplikan isi pesan terjadwal

```
BUKU KAS Warung UJI Uji
Rekap harian Selasa, 13/10/2026

UANG MASUK: Rp 975.000
UANG KELUAR: Rp 75.000
HASIL USAHA …: Rp 900.000
…
Total: Rp 1.400.000 (awal periode Rp 500.000, naik Rp 900.000)
```

## Lingkungan uji

- Database fiktif di folder data skill (`~/KomunitechData/kas/`) pada HOME gateway (init + 3 transaksi + akun BRI/QRIS).  
- Skill aktif di home gateway (symlink `kas-umkm`).  
- Pola **Pilihan 1** `references/openclaw-jadwal.md`: `openclaw automations add` + `--command-argv` `rekap --tanggal hari-ini` + `--announce --channel telegram --to <ID-grup-uji> --thread-id <ID-thread-uji>`.  
- Konfigurasi grup uji: hanya skill `kas-umkm` (cadangan konfigurasi: catatan internal kurator, tidak disertakan dalam paket).

## Cacat / catatan

- Alur konfirmasi "Lanjut? (ya/tidak)" lewat chat bot **tidak** diuji run ini (jadwal dibuat langsung setelah data uji siap; isi delivery identik dengan skill).  
- Selain laporan terjadwal, ada satu pesan balasan bot terhadap permintaan uji penguji (pesan terpisah).

## Pesan Telegram dalam uji

1. Penguji → grup uji Telegram internal: permintaan uji jadwal + konteks data.  
2. Bot → balasan singkat (dari log gateway).  
3. Bot → rekap terjadwal.
