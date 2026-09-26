# Skenario 01 — Draf invoice dengan produk, jasa, diskon (normal)

**Penguji:** pembuat skill (BUKAN penguji independen), 2026-09-24. Dolibarr **asli** 24.0.1 di container Linux (PHP 8.4, MariaDB 10.11), zona PHP Asia/Jakarta. Data fiktif.

## Permintaan pengguna
> "Buatkan invoice untuk CV Maju Jaya: gula aren GLA-1KG 10, jasa sangrai 5 kali 45 ribu, standing pouch 50 biji 1.250 diskon 10%. Tempo 30 hari."

## Langkah agent
1. `pelanggan cari "maju"`
```
CARI PELANGGAN: 'maju'
- ID 1: CV Maju Jaya | CU2609-00001 | 081234567890 | maju@contoh.id | Bandung
```
2. Pratinjau: `invoice buat --pelanggan 1 --item "@GLA-1KG|10" --item "Jasa sangrai kopi|5|45000" --item "Kemasan standing pouch|50|1.250|10" --jatuh-tempo 30`
```
PRATINJAU DRAF INVOICE
Pelanggan: CV Maju Jaya (ID 1)
Tanggal: 2026-09-24 | jatuh tempo: 2026-10-24 (30 hari)

1. Gula Aren 1kg - 10 x Rp 32.500 = Rp 325.000
2. Jasa sangrai kopi - 5 x Rp 45.000 = Rp 225.000
3. Kemasan standing pouch - 50 x Rp 1.250 diskon 10% = Rp 56.250

Hitungan Komunitech (PPN 12% x DPP nilai lain 11/12 (efektif 11%)):
DPP (jumlah harga sebelum pajak): Rp 606.250
DPP nilai lain 11/12 (informasi faktur): Rp 555.729,17
PPN: Rp 66.687 (dari Rp 66.687,50 dibulatkan ke bawah)
TOTAL: Rp 672.937

Belum dikirim ke Dolibarr. Jika sudah benar, ulangi perintah yang sama dengan --ya.
Invoice akan dibuat sebagai DRAF (belum sah, belum bernomor final, tidak dikirim ke pelanggan).
```
3. Pengguna menjawab "ya" → perintah yang sama + `--ya` (kode keluar 0):
```
DRAF INVOICE
Pelanggan: CV Maju Jaya (ID 1)
Tanggal: 2026-09-24 | jatuh tempo: 2026-10-24 (30 hari)

1. Gula Aren 1kg - 10 x Rp 32.500 = Rp 325.000
2. Jasa sangrai kopi - 5 x Rp 45.000 = Rp 225.000
3. Kemasan standing pouch - 50 x Rp 1.250 diskon 10% = Rp 56.250

Hitungan Komunitech (PPN 12% x DPP nilai lain 11/12 (efektif 11%)):
DPP (jumlah harga sebelum pajak): Rp 606.250
DPP nilai lain 11/12 (informasi faktur): Rp 555.729,17
PPN: Rp 66.687 (dari Rp 66.687,50 dibulatkan ke bawah)
TOTAL: Rp 672.937

TERSIMPAN SEBAGAI DRAF: (PROV10) (ID 10), status Dolibarr: draf
Angka di Dolibarr: DPP Rp 606.250 | PPN Rp 66.687,50 | total Rp 672.937,50
BEDA dengan hitungan Komunitech: PPN +Rp 0,50; TOTAL +Rp 0,50
Sebab umum: Dolibarr menghitung PPN per baris lalu membulatkan ke terdekat (2 desimal, atau sesuai pengaturan 'Maks. desimal untuk harga total'), sedangkan standar Komunitech menghitung PPN dari total DPP lalu membulatkan ke bawah sekali. Selisih kecil (Rp 0-beberapa rupiah) wajar. Draf TIDAK diubah otomatis; pemilik memutuskan. Nilai PPN resmi mengikuti faktur di Coretax.
Langkah berikut dilakukan MANUSIA di Dolibarr: periksa draf > Validasi > kirim/cetak.
```

## Verifikasi angka independen (hitung manual)
| Item | Hitungan | Hasil |
|---|---|---|
| Gula | 10 × 32.500 | 325.000 |
| Jasa | 5 × 45.000 | 225.000 |
| Pouch | 50 × 1.250 × 90% | 56.250 |
| DPP | jumlah | **606.250** ✓ |
| DPP nilai lain | 606.250 × 11/12 = 555.729,166… | **555.729,17** ✓ |
| PPN (standar library) | 606.250 × 11% = 66.687,5 → ke bawah | **66.687** ✓ |
| PPN Dolibarr (per baris, 2 desimal) | 35.750 + 24.750 + 6.187,50 | **66.687,50** ✓ selisih 0,50 dilaporkan |

Draf tercatat di Dolibarr dengan status 0 (draf), ref sementara `(PROV10)`. Tidak ada panggilan validasi/pembayaran (dipastikan juga oleh uji regresi `cek_tanpa_aksi_terlarang`).
