# Catatan uji pembuat — inventree-gudang v1.0.0

**Penguji:** pembuat skill (agent sesi Komunitech Skills Factory, Akun A), 2026-09-29.
**Catatan peran:** ini uji oleh **pembuat sendiri**, bukan uji independen. Uji independen (5 skenario, A/B tanpa skill, banding pesaing, `HASIL-UJI.md`) **belum** dikerjakan — status katalog `uji`.

## 1. InvenTree ASLI yang dipakai
- **InvenTree 1.5.6** (API 530), tag resmi `1.5.6` commit `284a670413cc` (rilis 26 Sep 2026), dipasang manual: Python 3.12 venv + `pip install --require-hashes -r src/backend/requirements.txt` (Django 5.2.16, DRF 3.17.1), SQLite, `manage.py migrate`, gunicorn terikat **127.0.0.1:8000**, plugin dimatikan. `tasks.py` tidak dijalankan (audit: (riset internal kurator, tidak disertakan dalam paket) §3).
- Data **fiktif** "UD Sumber Rasa" (pabrik keripik): lokasi Gudang Utama/Rak A/Rak B, Ruang Produksi, Toko Depan; bahan baku (kg/L), kemasan, 2 produk rakitan + BOM, 2 pemasok fiktif, PO-0001 & PO-0002 (Placed), BO-0001.
- Akun: `agen-baca` (grup Agen Baca: view) dan `agen-gudang` (grup Agen Gudang: + add/change Stock Items & Purchase Orders), token masing-masing (tidak disimpan di repo).

## 2. Transkrip nyata
`transkrip-inventree-1.5.6.txt` — 33 perintah dijalankan berurutan (lewat proxy perekam lokal di port 8100 yang meneruskan apa adanya ke InvenTree 127.0.0.1:8000; rekamannya menjadi `tests/fixtures/inventree-1.5.6.json`). Baris `$ python3 inventree.py ...` di transkrip menampilkan argumen tanpa tanda kutip (keterbatasan `echo`), perintah aslinya memakai kutip, mis. `--baris "BB-001=150; minyak=40"`.
Lembar opname yang diisi "petugas": `contoh-lembar-opname-rak-a-terisi.csv`.

Yang terbukti di server asli:
| Perintah | Hasil |
|---|---|
| `cek` (baca / gudang) | versi 1.5.6 API 530, hak per role benar; akun gudang diberi peringatan "BISA MENULIS" |
| `cari`, `stok`, `lokasi`, `stok-menipis`, `po-terbuka`, `bom`, `produksi-ringkas`, `laporan-harian`, `ekspor-csv` | angka cocok dengan data seed (lihat §3) |
| `stok singkong` | ditolak kode 7, menampilkan 3 pilihan (tidak menebak) |
| `opname --ya` dengan token baca | **403** dari InvenTree, tidak ada perubahan |
| `opname --ya` dengan token gudang | tersimpan; riwayat InvenTree mencatat "Opname 2026-09-29 via Komunitech inventree-gudang: opname akhir bulan"; stok Rak A singkong 60 → 57 |
| `opname --ya` lembar yang sama diulang | **BERHENTI** (stok berubah sejak lembar dibuat), tidak ada yang dikirim |
| `terima-barang` tanpa baris / melebihi sisa | ditolak kode 2 sebelum menghubungi endpoint tulis |
| `terima-barang ... --ya` | stok baru batch SK-2909 kedaluwarsa 6 Okt 2026 di Rak A, sisa PO-0001 singkong 50 |
| token salah / server mati / URL internet | 401 kode 5 / kode 4 / ditolak kode 2 tanpa koneksi |

## 3. Verifikasi angka independen (hitung tangan dari data seed)
- Stok singkong awal: 60 (Rak A) + 25 (Produksi) = **85 kg** ✔.
- BOM PJ-001 per bungkus: singkong 0,3; minyak 0,05; bumbu 0,02; pouch 1; label 1. Maks produksi = min(⌊85/0,3⌋=283, ⌊28/0,05⌋=560, ⌊12,5/0,02⌋=625, 1.200, 300) = **283** ✔.
- 300 bungkus: singkong 300×0,3 = 90 kg vs 85 → **kurang 5 kg** ✔; label 300 vs 300 → cukup ✔.
- Setelah opname (57) + terima 150: singkong 57 + 150 + 25 = **232 kg** ✔. 1.000 bungkus PJ-002: 300 kg vs 232 → kurang 68 ✔; label 1.000 vs 300 → kurang 700, maks = min(⌊232/0,3⌋=773, ⌊67,5/0,05⌋=1.350, 1.200, 300) = **300** ✔.
- Stok menipis PJ-002: min 150 − stok 90 − dipesan 0 − diproduksi 0 = **60** ✔; kebutuhan BO-0001 singkong 100 × 0,3 = **30 kg** ✔.

## 4. Uji regresi otomatis
`python3 tests/uji_regresi.py` → **61 test, semua lulus** (server tiruan memutar ulang jawaban rekaman InvenTree 1.5.6): angka gaya Indonesia (baca & tulis), URL/keamanan, anti-rumus CSV, lembar opname (titik koma/koma, kosong, negatif, ganda, kolom hilang), token (izin 600, tidak tercetak, tidak menimpa tanpa `--ya`, urutan sumber), semua perintah baca dengan angka dihitung ulang dari fixture, paginasi 150 baris, 401/403/404/server mati/timeout baca, opname (draf, pratinjau tanpa tulis, body `/stock/count/` persis, berhenti bila berubah, lembar rusak tanpa koneksi, 400, **500 & timeout saat menulis → kode 8 tanpa mengulang**), terima barang (body `/receive/` persis, melebihi sisa, baris lengkap, status PO bukan Placed).

## 5. Uji muat OpenClaw
`bash scripts/uji_openclaw.sh` → OpenClaw 2026.9.6: eligible/modelVisible/commandVisible **97/97** (termasuk `inventree-gudang`).

## 6. Belum diuji (jujur)
Docker (bagian 2 panduan — cara utama pembeli), Windows/macOS, tampilan web InvenTree, worker, jadwal OpenClaw & pengiriman Telegram sungguhan, barang ber-nomor seri, kemasan pemasok ≠ 1, sub-kategori varian/pengganti BOM.
