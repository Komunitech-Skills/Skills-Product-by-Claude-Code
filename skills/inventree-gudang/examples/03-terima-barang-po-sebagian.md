# Uji 03 — Normal: terima barang dari PO sebagian (batch & kedaluwarsa, kemasan pemasok)

**Server/data:** sama dengan Uji 01. PO-0002 (CV Warna Paku Sejahtera, Placed, target 25 Sep → TERLAMBAT): CT-05 24, PK-05 30 kg, PK-05B 10 kg, RL-09 2 kemasan (1 kemasan = 6).
**Permintaan:** "Barang dari CV Warna Paku datang: cat tembok 5 kg 12 kaleng batch CTW-2610 kedaluwarsa Okt 2028, paku 5 cm 20 kg, roller 1 dus."

## Percobaan sesuai SKILL.md
```
po-terbuka --pemasok warna               -> PO-0002, 4 baris terbuka ✔
terima-barang --po PO-0002 --baris "Cat Tembok Putih 5 kg=12; Paku 5 cm=20; Roller=1" --batch CTW-2610
GALAT: 'Paku 5 cm' cocok dengan lebih dari satu baris PO. Pakai kode (IPN) persis.   [exit 7]
terima-barang --po PO-0002 --baris "CT-05=12; PK-05=20; RL-09=1" --batch CTW-2610
GALAT: 'PK-05' cocok dengan lebih dari satu baris PO. Pakai kode (IPN) persis.        [exit 7]  <-- BUG
terima-barang --po PO-0002 --baris "#17=20"   -> '#17' tidak ada di baris terbuka      [exit 2]
```
**BUG MAYOR:** `urai/cocok` di `cmd_terima_barang` memakai pencocokan *substring* (`kecil in IPN` / `kecil in nama`) tanpa mendahulukan yang persis. IPN `PK-05` ikut cocok dengan `PK-05B`, dan nama "Paku 5 cm" cocok dengan "Paku 5 cm Beton". Pesan galat menyuruh "Pakai kode (IPN) persis" — padahal itu yang sudah dipakai → jalan buntu; `#id` juga tidak didukung di `--baris`. Varian bernama mirip (paku 5 cm / 5 cm beton, besi 8/10 mm, cat 5/25 kg) sangat umum di toko bangunan & distributor. Satu-satunya jalan keluar yang ditemukan penguji: SKU pemasok persis (`WP-PK5`) — tidak didokumentasikan dan tidak ditampilkan oleh `po-terbuka`.

Juga: `--batch` hanya satu untuk semua baris; batch cat akan ikut menempel ke paku. Agent (penguji) memecah jadi 3 perintah — SKILL.md sebaiknya menyuruh ini secara eksplisit.

## Alur yang akhirnya dijalankan (pratinjau → "ya")
```
terima-barang --po PO-0002 --baris "CT-05=12" --batch CTW-2610 --kedaluwarsa 2028-10-01
  PRATINJAU ... Masuk ke lokasi: Gudang Utama/Rak A / Kode batch: CTW-2610
  - Cat Tembok Putih 5 kg [CT-05]: terima 12 (sisa pesanan 24)
terima-barang --po PO-0002 --baris "RL-09=1"
  - Roller Cat 9 inci [RL-09]: terima 1 kemasan pemasok (sisa pesanan 2)
  PERHATIAN: Roller Cat 9 inci: 1 kemasan pemasok = 6; jumlah di atas dalam KEMASAN.   ✔
terima-barang --po PO-0002 --baris "WP-PK5=20"     (jalan keluar SKU)
  - Paku 5 cm [PK-05]: terima 20 kg (sisa pesanan 30)
```
Setelah 3 pratinjau: `received` semua baris PO tetap 0 ✔ (tidak ada penulisan tanpa `--ya`). Lebih dari sisa (`CT-05=30`) → ditolak "melebihi sisa pesanan 24" ✔.

Lalu ketiganya + `--ya` (token gudang) → `TERSIMPAN: 1 baris diterima dari PO-0002 ke Gudang Utama/Rak A (batch CTW-2610)` dst.

## Verifikasi independen (API admin)
| Cek | Hasil API | Cocok |
|---|---|---|
| Baris PO: CT-05 / PK-05 / PK-05B / RL-09 `received` | 12 / 20 / 0 / 1 | ✔ |
| Item stok baru CT-05 | id 29, Rak A, 12, batch CTW-2610, exp 2028-10-01, purchase_order=2 | ✔ |
| Item stok baru RL-09 | id 30, Rak A, **6** (1 kemasan × 6) | ✔ |
| Item stok baru PK-05 | id 31, Rak A, 20 | ✔ |
| `stok CT-05` total | 42 = 13 + 11 + 12 + 6 | ✔ |
| `po-terbuka` sisa | 12 / 10 kg / 10 kg / 1 | ✔ |
| Status PO | tetap Placed (belum lengkap) | ✔ |

**Temuan (RENDAH):** pesan TERSIMPAN untuk roller menulis "+1" padahal stok bertambah 6 (pratinjau sudah memperingatkan, tapi ringkasan akhir sebaiknya "+1 kemasan = 6").

**Hasil: LULUS BERSYARAT** — angka & keamanan tulis benar, tetapi pencocokan barang PO gagal untuk IPN yang merupakan awalan IPN lain (wajib diperbaiki).
