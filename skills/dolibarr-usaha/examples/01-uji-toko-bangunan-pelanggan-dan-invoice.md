# 01 (uji independen) — Toko bangunan: cek → cari/tambah pelanggan → draf invoice 3 baris + diskon + PPN

**Penguji:** agent penguji independen (Claude Code, simulasi agent), 2026-09-24. Bukan pembuat skill.
**Lingkungan:** Dolibarr **24.0.1 asli** (tag git resmi, dipasang ulang dari nol oleh penguji lewat installer web `install/step1→step5`), PHP 8.4.19 `php -S` (`date.timezone=Asia/Jakarta`), MariaDB 10.11.14 baru di scratchpad. Negara Indonesia (118), IDR, tarif PPN 11/12/0 ditambahkan ke kamus. Skill disalin ke scratchpad, `HOME` palsu. Data fiktif: "Toko Bangunan Sumber Makmur".
**Kunci:** user `api_tulis` (non-admin) dengan hak persis panduan §6 langkah 2+3: 121, 262, 11, 31, 1001, 122, 12. Disimpan lewat `simpan-kunci` (stdin) → file `~/.komunitech/dolibarr-kunci.txt` izin **600**, folder **700**.

## Permintaan pengguna
> "Tolong cek Dolibarr saya nyambung. Terus buatkan invoice buat UD Sinar Bangunan (pelanggan baru, 0813-2222-1111, Sragen): semen Tiga Roda 20 sak, cat tembok putih 4 kaleng harga 87.500 diskon 7,5%, ongkir truk 150 ribu. Tempo 30 hari."

## 1. `cek`
```
CEK DOLIBARR
Alamat: http://127.0.0.1:8098/dolibarr
Versi Dolibarr: 24.0.1
Kunci API: ****5Wf1 (dari file .../home/.komunitech/dolibarr-kunci.txt)
MODUL
- Pihak Ketiga (pelanggan): aktif, bisa dibaca
- Nota/Invoice pelanggan: aktif, bisa dibaca
- Produk: aktif, bisa dibaca
- Stok (gudang): aktif, bisa dibaca
CATATAN
1. Daftar hak akses tidak bisa dibaca (user API tidak punya hak 'Buat/ubah pengguna sendiri'). ...
```
Dengan kunci **admin**: muncul "User API: admin (ADMIN)", daftar hak `[x]`, dan 2 CATATAN (admin + 7 hak berisiko). ✅

## 2. Pelanggan
| Perintah | Hasil | Nilai |
|---|---|---|
| `pelanggan cari "maju jaya"` | ID 1 CV Maju Jaya Konstruksi, ID 5 Toko Maju Jaya Makmur | ✅ 2 hasil → agent harus bertanya yang mana |
| `pelanggan cari "081234560002"` | ID 2 Pak Budi Santoso | ✅ |
| `pelanggan cari "0812-3456-0002"` | **Tidak ada pelanggan yang cocok** | ❌ nomor berformat strip tidak ketemu (cacat S4) |
| `pelanggan tambah --nama "Budi Santoso" --telepon "0812 3456 0099"` | "Sudah ada pelanggan dengan nama mirip: ID 2 Pak Budi Santoso … Tidak dibuat" | ✅ cegah ganda |
| `pelanggan tambah --nama "Ibu Rina Wati" --telepon 081234560004` (nomor **sama** dengan "Bu Rina Wati" ID 4) | Pratinjau biasa, **tidak ada peringatan** | ❌ ganda lolos (cacat S4) |
| `pelanggan tambah --nama "UD Sinar Bangunan" --telepon "0813-2222-1111" --kota Sragen` | PRATINJAU, "Belum disimpan … ulangi dengan --ya" | ✅ tidak menulis (DB: 5 pelanggan tetap) |
| sama + `--ya` | `TERSIMPAN: ID 6 kode CU2609-00006` | ✅ telepon dinormalisasi `081322221111`, negara Indonesia |

## 3. Draf invoice — pratinjau
`invoice buat --pelanggan 6 --item "@SMN-40|20" --item "Cat Tembok Putih 5kg|4|87500|7,5" --item "Ongkos kirim truk|1|150000" --jatuh-tempo 30`
```
PRATINJAU DRAF INVOICE
Pelanggan: UD Sinar Bangunan (ID 6)
Tanggal: 2026-09-24 | jatuh tempo: 2026-10-24 (30 hari)

1. Semen Tiga Roda 40kg - 20 x Rp 62.500 = Rp 1.250.000
2. Cat Tembok Putih 5kg - 4 x Rp 87.500 diskon 7,5% = Rp 323.750
3. Ongkos kirim truk - 1 x Rp 150.000 = Rp 150.000

Hitungan Komunitech (PPN 12% x DPP nilai lain 11/12 (efektif 11%)):
DPP (jumlah harga sebelum pajak): Rp 1.723.750
DPP nilai lain 11/12 (informasi faktur): Rp 1.580.104,17
PPN: Rp 189.612 (dari Rp 189.612,50 dibulatkan ke bawah)
TOTAL: Rp 1.913.362

Belum dikirim ke Dolibarr. Jika sudah benar, ulangi perintah yang sama dengan --ya.
Invoice akan dibuat sebagai DRAF (belum sah, belum bernomor final, tidak dikirim ke pelanggan).
```
Harga semen diambil dari produk Dolibarr (62.500). Jumlah invoice di DB sebelum/sesudah pratinjau: 10 → 10 ✅.

## 4. `--ya` → draf + pencocokan
```
TERSIMPAN SEBAGAI DRAF: (PROV11) (ID 11), status Dolibarr: draf
Angka di Dolibarr: DPP Rp 1.723.750 | PPN Rp 189.612,50 | total Rp 1.913.362,50
BEDA dengan hitungan Komunitech: PPN +Rp 0,50; TOTAL +Rp 0,50
Sebab umum: Dolibarr menghitung PPN per baris lalu membulatkan ke terdekat ... Draf TIDAK diubah otomatis; pemilik memutuskan. Nilai PPN resmi mengikuti faktur di Coretax.
Langkah berikut dilakukan MANUSIA di Dolibarr: periksa draf > Validasi > kirim/cetak.
```
Query DB (`llx_facturedet`): semen `fk_product=11`, 20 × 62.500, tva 11 → 1.250.000 / 137.500; cat 4 × 87.500 diskon 7,5 → 323.750 / 35.612,50; ongkir 150.000 / 16.500. `fk_statut=0` (draf), `datef=2026-09-24`, `date_lim_reglement=2026-10-24`. ✅

Mengulang perintah yang sama dengan `--ya` → `DIBATALKAN: sudah ada draf untuk pelanggan ini dengan jumlah sama: (PROV11) (ID 11)` ✅ (kode keluar 0; judul masih "DRAF INVOICE", kosmetik).

## 5. Kasus tambahan (mewah, harga bersen, jasa)
| Perintah | Komunitech | Dolibarr | Pesan |
|---|---|---|---|
| `--pelanggan 5 --item "@BSI-10|3||5" --item "@PIP-3|7|71750|2,5" --ppn mewah --ya` | DPP 727.194; PPN 87.263 (87.263,28↓); total 814.457 | DPP 727.193,74; PPN 87.263,25; total 814.456,99 | "BEDA: DPP -Rp 0,26; PPN +Rp 0,25; TOTAL -Rp 0,01" + catatan "tarif PPN produk di Dolibarr 11%, invoice memakai 12%" ✅. Penjelasan hanya menyebut pembulatan PPN, padahal DPP juga beda karena total baris dibulatkan ke rupiah vs 2 desimal (R4) |
| `--pelanggan 5 --item "Jasa pasang keramik|12|45833|0" --jasa --ya` | DPP 549.996; DPP 11/12 504.163; PPN 60.499; total 610.495 | PPN 60.499,56; total 610.495,56 | BEDA PPN +0,56 ✅; `product_type=1` ✅ |

## Verifikasi angka independen (Decimal, rumus sendiri, bukan kode skill)
| Besaran | Hitung penguji | Script | Dolibarr (DB) |
|---|---|---|---|
| Total baris cat 4 × 87.500 × 92,5% | 323.750 | 323.750 | 323.750,00 |
| DPP | 1.723.750 | 1.723.750 | 1.723.750,00 |
| DPP nilai lain 11/12 | 1.580.104,1667 → 1.580.104,17 | 1.580.104,17 | – |
| PPN tepat = DPP × 11% (= 12% × 11/12) | 189.612,50 | 189.612,50 | 189.612,50 (per baris) |
| PPN dibulatkan ke bawah sekali | 189.612 | 189.612 | – |
| Total | 1.913.362 | 1.913.362 | 1.913.362,50 |
| Besi 3 × 83.333,33 × 95% | 237.499,9905 → 237.500 | 237.500 | 237.499,99 |
| Mewah PPN 727.194 × 12% | 87.263,28 → 87.263 | 87.263 | 87.263,25 |
Semua angka script = hitung ulang penguji (0 beda). Selisih dengan Dolibarr (Rp 0,01–0,56) **dilaporkan jujur** dan tidak "diperbaiki" diam-diam. Standar pembulatan library (PPN dari DPP persis, ke bawah sekali; total baris ke rupiah terdekat) **dipatuhi**. Pernyataan Coretax ada di pesan BEDA dan SKILL.md:114.

**Hasil skenario: LULUS**, dengan catatan S4 (pencarian/cek ganda berdasar nomor telepon) dan R4 (penjelasan selisih DPP).
