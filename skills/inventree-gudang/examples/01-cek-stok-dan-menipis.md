# Uji 01 — Normal: cek stok & stok menipis (+ BOM/produksi)

**Penguji:** agent independen (bukan pembuat), 29 Sep 2026. **Server:** InvenTree **1.5.6 ASLI via Docker resmi** (panduan §2: postgres 17, redis, caddy, worker; port `127.0.0.1:80/443` saja), dipasang penguji di folder baru. **Data fiktif penguji:** "UD Sinar Bangun Jaya" (toko bangunan/distributor) — 4 lokasi (`Gudang Utama` → `Rak A`, `Rak B`; `Toko Depan`), 25 barang (IPN SM-01…PKT-01, satuan `sak`/`dus` custom, kg, L), 28 item stok ber-batch & kedaluwarsa, 1 BOM `PKT-01 Paket Cat Kamar 3x3` (2 cat 5 kg + kuas + roller + 4 amplas + lakban habis pakai), 1 perintah produksi BO-0001 (4 unit, Pending), 2 PO berstatus Placed (PO-0001 semen; PO-0002 cat/paku/roller — roller 1 kemasan = 6). Token akun `agen-baca` (grup hanya-lihat).

**Permintaan pengguna:** "Stok semen berapa, di rak mana saja? Terus barang apa yang hampir habis?"

## Yang dijalankan agent (mengikuti SKILL.md)
```
inventree.py cari semen          -> 2 barang (SM-01 di bawah minimum)
inventree.py stok semen          -> GALAT kode 7: cocok 2 barang (agent bertanya "yang mana?")  ✔ tidak menebak
inventree.py stok SM-01
inventree.py stok-menipis
```

## Output skill (dipotong)
```
STOK Semen Portland 50 kg [SM-01]
Total: 93 sak (3 item stok)
Minimum: 100 sak - DI BAWAH MINIMUM
Gudang Utama/Rak A: 85 sak
  - 60 sak (batch SMN-2608; kedaluwarsa 20 Des 2026) [id stok 1]
  - 25 sak (batch SMN-2609; kedaluwarsa 15 Jan 2027) [id stok 2]
Toko Depan: 8 sak
  - 8 sak (batch SMN-2608; kedaluwarsa 20 Des 2026) [id stok 3]

STOK MENIPIS (di bawah minimum): 9 barang
Bahan Bangunan:
- Kawat Bendrat [KW-01]: stok 18,5 kg, minimum 25 kg, kurang 6,5 kg (perlu dipesan lagi min. 6,5 kg)
- Pasir Cor [PS-01]: stok 1.500 kg, minimum 2.000 kg, kurang 500 kg (perlu dipesan lagi min. 500 kg)
- Besi Beton 10 mm [BS-10]: stok 120, minimum 150, kurang 30 (perlu dipesan lagi min. 30)
- Semen Portland 50 kg [SM-01]: stok 93 sak, minimum 100 sak, kurang 7 sak (sedang dipesan 100 sak; kekurangan terhadap minimum sudah tertutup ...)
Cat & Kimia: Waterproofing 9/12 (pesan 3); Thinner 17,5/20 L (pesan 2,5 L)
Paket Rakitan: Paket Cat Kamar 3x3 0/5 (perlu diproduksi lagi min. 5)
Paku & Perkakas: Roller Cat 9/12 (sedang dipesan 12; dibutuhkan produksi 4; tertutup); Paku 5 cm 42,5/50 kg (dipesan 30 kg; tertutup)
```
BOM & produksi: `bom PKT-01` → maks 9 unit (roller 9 pembatas); `produksi-ringkas --produk PKT-01 --jumlah 12` → cat butuh 24/30 CUKUP, roller butuh 12/9 KURANG 3 (sedang dipesan 12), amplas 48/240, lakban "habis pakai"; kesimpulan BELUM CUKUP, maks 9.

## Verifikasi independen (API admin, dihitung ulang penguji)
| Angka | Skill | Data InvenTree / hitung ulang | Cocok |
|---|---|---|---|
| SM-01 total | 93 | 60 + 25 + 8 (id 1,2,3) | ✔ |
| Jumlah barang di bawah minimum | 9 | hitung manual dari `total_in_stock < minimum_stock` = 9 (CT-05 30 = min 30 → benar tidak masuk) ; `?low_stock=true` = 9 | ✔ |
| RL-09 "sedang dipesan 12" | 12 | `ordering`=12 (2 kemasan × 6) | ✔ |
| RL-09 dibutuhkan produksi | 4 | `required_for_build_orders`=4 (BO 4 × 1) | ✔ |
| Saran SM-01/PK-05/RL-09 | 0 (tertutup) | 100−93−100, 50−42,5−30, 12−9−12 < 0 | ✔ |
| Lokasi: Gudang Utama 19 / Rak A 12 / Rak B 6 / Toko 9 item | sama | dihitung dari daftar stok penguji | ✔ |
| BOM maks | 9 | min(30/2=15, 50, 9, 240/4=60) | ✔ |
| Butuh 12 unit | 24/12/12/48 | per unit × 12 | ✔ |

**Temuan:** (a) PKT-01 "perlu diproduksi lagi min. 5" padahal BO-0001 (4 unit, status Pending) sudah ada — InvenTree memberi `building`=0 untuk BO Pending, skill tidak menyebut produksi terbuka di baris itu (RENDAH). (b) `po-terbuka` menampilkan RL-09 "dipesan 2, sisa 2" (dalam kemasan) tanpa keterangan kemasan, sementara `stok-menipis` bilang "sedang dipesan 12" — membingungkan pengguna awam (RENDAH).

**Hasil: LULUS.**
