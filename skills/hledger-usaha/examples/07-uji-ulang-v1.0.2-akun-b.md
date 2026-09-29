# 07 — Uji ulang v1.0.2 (penguji independen Akun B, 26-09-2026)

> Uji perawatan atas perbaikan temuan uji ulang v1.0.1 (U19): `cek_tunai` tertipu tarik/setor tunai [SEDANG] dan `--pph23` pada `--jenis jual` [RENDAH]. Skill disalin ke scratchpad `rt-u19b/sk/`, data **fiktif**, perintah dijalankan langsung (simulasi agent `claude-code`). Kode skill tidak diubah.
> **hledger asli 1.52.4**: `hledger-linux-x64.tar.gz` **diunduh ulang** dari github.com/hledgerorg/hledger/releases/download/1.52.4 (HTTP 200) ke scratchpad; SHA-256 `f76a2e4088e162b7658e43077502569d5a6fdacd219b19bfb9aab6588b69643a` = tabel `docs/panduan-hledger.md` = unduhan uji sebelumnya. API rilis GitHub tidak bisa dibaca dari sesi ini (akses repo tidak aktif), jadi digest halaman rilis tidak dicek ulang. `hledger --version` → `hledger 1.52.4, linux-x86_64`. Tidak dipasang ke sistem.

## 1. CATATAN "penjualan tunai belum dicatat" di laba rugi (temuan SEDANG)
| Jurnal | Isi kas periode itu | v1.0.1 | v1.0.2 |
|---|---|---|---|
| Impor BCA Agustus (uji 06, berisi `TARIKAN ATM 07/08`) | hanya tarik tunai | tanpa CATATAN | **CATATAN muncul** ✅ |
| Jurnal skenario 03 v1.0.0 (asal temuan; `TARIKAN ATM 20/09` + `Setor Tunai di ATM`) — `laba-rugi` & `bulanan` Sept | hanya pindah dana | tanpa CATATAN | **CATATAN muncul** (dua perintah) ✅ |
| **Data baru "Bengkel Uji Fiktif"** (lihat bawah) | 2× TARIKAN ATM + SETOR TUNAI dari mutasi, `catat --jenis tarik-tunai`, `catat --jenis setor-tunai`, prive tunai | — | **CATATAN muncul** (hledger & `--mesin bawaan`) ✅ |
| Sama + `catat --jenis jual 175rb --via kas` | ada penjualan tunai | — | CATATAN hilang ✅ |
| Rentang `--dari/--sampai` Okt tanpa penjualan tunai | — | — | CATATAN muncul ✅ |
| Tahun 2026 (ada biaya tunai 30/09) | ada biaya tunai | — | tanpa CATATAN (benar) ✅ |
| Jurnal skenario 01/02 v1.0.0 (ada penjualan tunai) | — | — | tanpa CATATAN (benar) ✅ |

Data baru: saldo awal 30/09 Kas 1.500.000, BCA 8.000.000; mutasi BCA Oktober 6 baris (QRIS +3.250.000, sewa −2.000.000, TARIKAN ATM −500.000, SETOR TUNAI +1.200.000, BIAYA ADM −15.000, TARIKAN ATM −300.000); pratinjau impor: "Uji silang aturan dengan hledger: COCOK (6 baris)", saldo cocok, pengingat "INGAT: mutasi bank hanya berisi…" tampil.
Verifikasi Decimal (hitung dari input, bukan dari script) vs hledger asli (`hledger is/bal/bs`):
| Besaran | Penguji | Skill | hledger |
|---|---:|---:|---:|
| Kas 31/10 sebelum jual tunai = 1,5 jt +0,5 −1,2 +0,3 +0,25 −0,1 −0,05 −0,04 jt | 1.160.000 | — | 1.160.000 |
| BCA = 8 jt +3,25 −2 −0,5 +1,2 −0,015 −0,3 −0,25 +0,1 jt | 9.485.000 | — | 9.485.000 |
| Laba Okt (sebelum jual tunai) = 3.250.000 − 2.015.000 | 1.235.000 | 1.235.000 | 1.235.000 |
| Pendapatan Okt akhir (3.250.000 + 175.000 + 3.333.333 + 1.000.000 + 500.000) | 8.258.333 | 8.258.333 (hledger & bawaan) | — |
| Laba Okt akhir | 6.243.333 | 6.243.333 (hledger & bawaan) | — |
| Total aset 31/10 = modal 9.500.000 − prive 50.000 − beban Sep 40.000 + laba 6.243.333 | 15.653.333 | 15.653.333, SEIMBANG (hledger & bawaan) | 1.335.000 + 13.731.667 + 500.000 + 86.666 |
`hledger check` lulus.

## 2. `--pph23`/`--diterima` pada penjualan barang (temuan RENDAH)
| Perintah | Hasil |
|---|---|
| `catat --jenis jual --via kas --pph23 2% --ya` / `--diterima 980rb` / `--pph23 20rb` | GAGAL exit 2, pesan jelas: PPh 23 untuk jasa/sewa/royalti (UU PPh Ps. 23), arahkan ke `--jenis jasa`, sebut PPh 22 instansi → konsultan ✅ |
| alias `--jenis penjualan --via bank --pph23 2%` (pratinjau) | ditolak sama ✅ |
| `--jenis jual --via tempo --pph23 2%` | ditolak ✅ |
| `--batch` JSON `{"jenis":"jual",…,"pph23":"2%"}` | ditolak, exit 2 ✅ |
| Jurnal setelah semua penolakan | `cmp` identik ✅ |
| `--jenis jasa --nominal 3.333.333 --pph23 2%` | PPh 23 66.666 (2% = 66.666,66 dibulatkan ke bawah), bank 3.266.667, pendapatan bruto — hitung sendiri cocok ✅ |
| `terima-piutang 1jt --diterima 980rb` | BCA 980.000 / PPh 23 20.000 / piutang −1.000.000 ✅ |

Sisa kecil **[RENDAH]**: piutang yang berasal dari `--jenis jual` (barang, `--via tempo`) lalu dilunasi dengan `terima-piutang --diterima 490rb` tetap dicatat sebagai PPh 23 tanpa peringatan (script tidak melihat asal piutang). Pengaruh kecil (tetap seimbang, pengingat bukti potong tampil); saran: bila piutang pihak itu hanya dari transaksi `Pendapatan:Penjualan`, tambahkan PERHATIAN "PPh 23 bukan untuk penjualan barang".

## 3. Tanpa regresi
- `HLEDGER=<scratch>/bin/hledger python3 tests/uji_regresi.py` → **38 tes OK** (salinan & repo); tanpa hledger (PATH bersih) → **38 OK (5 dilewati)**.
- Angka kunci v1.0.0 atas salinan jurnal lama: skenario 01 laba **914.749,50**; 02 laba **19.880.000**; 03 rugi **−6.832.354,67**, total aset **21.167.645,33**, SEIMBANG — sama persis.
- `python3 scripts/validate.py --skill hledger-usaha` → ✅ valid.

**Skor: 9/10.**
