# HASIL UJI — buku-stok v1.1.0 (uji ulang)

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Versi diuji:** v1.1.0 (commit `639c0f4`; catalog 1.1.0). Uji pertama v1.0.0 → skor 6 (REVISI), 1 cacat berat + 4 sedang + 5 ringan.
- **Lingkungan:** Python 3.11; semua DB di `/tmp/uji-buku-stok/v11/` (`--db`); model independen penguji `acak.py` (HPP) dan `acak2.py` (HPP + pesanan + laporan).

## Uji ulang cacat v1.0.0
| Cacat v1.0.0 | Uji ulang v1.1.0 | Status |
|---|---|---|
| **B-1** pesanan batal setelah impor tetap dihitung di laporan | DB v1.0.0 asli (dibuat skrip v1.0.0, berisi 0002CD batal setelah impor) dibuka v1.1.0 → migrasi otomatis menambah `mutasi.dibatalkan` & menandai 1 mutasi. `laporan ringkas 23/09`: **5 barang, omzet Rp 243.000, HPP Rp 132.500, laba Rp 110.500**, KAOS-PT-M hilang dari terlaris (cocok hitungan manual). `laporan mutasi` Sep: penjualan **Rp 406.000**, HPP Rp 224.500 (cocok). Backup v1.0.0 di-restore lalu diimpor lanjut → tetap Rp 243.000 | **Beres** |
| **S-1** item SKU tak dikenal tidak pernah terpotong | `--lewati-tak-dikenal` → daftar KAOS-HT-XL → impor ulang: pratinjau "HT-XL -1 (10 → 9)" + peringatan item lama terpotong; picking kini menampilkan HT-XL di Rak A1; impor ketiga tidak memotong lagi; laporan 24/09 omzet Rp 61.000 | **Beres**, tetapi lihat cacat baru **B-2** |
| **S-2** batal diajukan → stok kembali; bila ditolak tidak dipotong ulang | Siklus Perlu Dikirim → Pembatalan Diajukan → Perlu Dikirim → Batal → Perlu Dikirim → Batal: stok MUG 12 → 10 → 10 → 10 → 12 → 10 → 12 (benar di setiap langkah); peringatan "AKTIF lagi" & "DIAJUKAN" muncul | **Beres** |
| **S-3** harga TikTok tidak terbaca | "SKU Subtotal After Discount" terpetakan sebagai subtotal (harga = subtotal ÷ qty); "SKU Unit Original Price" (sebelum diskon) tidak dipakai | **Beres** |
| **S-4** TikTok versi Indonesia | "Akan dikirim" → masuk picking; "ID Pelacakan", "Nama Penyedia Pengiriman", "Waktu Dibuat" dikenali; "Harga Satuan Asli SKU" tidak dipakai; platform = tiktok. references/marketplace.md jujur menandai nama kolom versi Indonesia belum dicocokkan dengan file asli | **Beres** (perlu file asli dari beta tester) |
| R-1 teks laporan ringkas | "Terjual: 12 barang (marketplace 6 dari 2 pesanan, toko/offline 6)"; restock "(Rp 1.725.000, termasuk ongkir/biaya tambahan)" — benar (50 × 34.500). *Koreksi penguji:* catatan v1.0.0 bahwa angka restock "tanpa ongkir" keliru; angka itu memang sudah termasuk ongkir | Beres |
| R-2 Tokopedia "Menunggu Konfirmasi Penjual" | kini `perlu_kirim`, masuk picking | Beres |
| R-3 kolom tipe/jumlah retur | TikTok "Completed" + "Return/Refund" → peringatan "ada tanda retur" | Beres |
| R-4 backup tertinggal saat `--ya` gagal | opname tanpa alasan `--ya` → jumlah file backup tetap 2 | Beres |
| R-5 `--tools` di jadwal | SKILL.md kini memakai `--session isolated --tools exec,read` (kedua flag ada di `automations add --help` 2026.9.5 dan sudah dijalankan di Gateway uji pada uji pertama) | Beres |

## Uji menyeluruh
| Uji | Hasil |
|---|---|
| `scripts/uji_regresi.py` | **37 tes OK** (8,5 dtk) |
| `acak.py` (HPP): 2 × 2.000 langkah (masuk tunggal/multi-item + biaya tambahan, keluar, opname, stok kurang) | HPP selisih 0, stok cocok, nilai persediaan identik (Rp 80.647.850; Rp 74.483.811); 122 penolakan stok kurang benar |
| `acak2.py` (model independen baru): 4 × 1.500 + 3 × 400 langkah — masuk, keluar, opname (memperhitungkan pesanan belum dikemas), pendaftaran SKU baru di tengah jalan, dan ±2.000 impor pesanan dengan status acak (Perlu Dikirim/Selesai/Batal/Pembatalan Diajukan/Belum Bayar/Pengembalian, impor ulang pesanan lama, batal → aktif lagi → batal) | Stok, HPP, nilai persediaan, **omzet/HPP/qty `laporan ringkas` untuk setiap tanggal (25–27 tanggal per seed)** dan penjualan/HPP `laporan mutasi` bulanan **cocok 100%**; ±1.200 mutasi & ±100 penjualan dibatalkan per seed; stok = Σ mutasi di semua DB |
| Impor Shopee CSV/XLSX, TikTok (EN & ID), Tokopedia XLSX | Pemetaan & angka benar (lihat 01) |
| Pratinjau tanpa `--ya` | tidak menyimpan (uji pertama md5; uji ulang: pratinjau impor ulang tidak memotong XL sebelum `--ya`) |
| Keamanan | Tidak berubah: library standar, tanpa jaringan/subprocess/eval, SQL berparameter. Migrasi hanya `ALTER TABLE` + penandaan, tidak mengubah angka stok |

## Skor
| Kriteria | Skor |
|---|---|
| Pemicu (description tepat) | 9 |
| Kemudahan awam | 8 |
| Kualitas output | 9 |
| Akurasi (angka/fakta) | 7 |
| Penanganan input kurang | 9 |
| Penanganan di luar cakupan | 9 |
| Keamanan | 9 |
| **SKOR AKHIR** | **6 / 10 — REVISI** |

Alasan: semua cacat v1.0.0 beres dan lolos ±10.000 langkah acak terhadap model independen, termasuk laporan per tanggal. Namun perbaikan S-1 memunculkan **cacat baru yang memotong stok barang yang salah** (B-2) pada input yang didukung resmi (file tanpa kolom nama produk). Sesuai aturan brief (angka salah = cacat berat, skor ≤ 6) statusnya tetap REVISI. Perbaikannya kecil (1–2 baris). Setelah itu, cukup uji ulang kasus B-2 dan regresi; perkiraan skor 9.

## Daftar cacat tersisa

### Berat
**B-2 (baru di v1.1.0). Impor ulang memotong stok produk yang salah bila file tidak punya kolom nama produk.**
Uji: file `No. Pesanan;SKU;Qty;Status` berisi pesanan WA-001 = MUG-KRM ×1 + GELAS-01 ×2 (belum terdaftar), diimpor dengan `--lewati-tak-dikenal` (MUG 12 → 11). Impor ulang file yang sama: item GELAS-01 "dicocokkan" ke baris **MUG-KRM** dan MUG dipotong **2 lagi** (11 → 9), padahal GELAS-01 belum terdaftar. Model acak menemukan pola yang sama (seed 1, langkah 32). Kasus ini terjadi di file SKU-saja, termasuk rekap pesanan WA/kasir, yang resmi didukung (`references/marketplace.md`: "Wajib: No. pesanan, Jumlah, dan SKU **atau** Nama produk"). Mengimpor ulang file yang sama adalah hal yang dijanjikan aman.
*Penyebab:* `cmd_impor_pesanan`, blok "Item yang dulu dilewati" (stok.py ±baris 1473–1476):
`sumber = next((f for f in ps["item"] if (f["sku"] and f["sku"] == it["sku_mp"]) or ("%s %s" % (f["nama"], f["varian"])).strip() == it["nama_mp"]), None)` — bila nama & varian kosong, `"" == ""` cocok dengan item pertama pesanan.
*Perbaikan:* cocokkan berdasarkan SKU bila `it["sku_mp"]` ada; pakai nama hanya bila `it["sku_mp"]` kosong **dan** `it["nama_mp"]` tidak kosong. Setelah itu, pastikan juga `sumber["sku"] == it["sku_mp"]` sebelum `_cocokkan_produk`. Tambahkan tes regresi "file SKU-saja, 1 SKU dikenal + 1 tak dikenal, impor ulang 2× → stok SKU dikenal hanya terpotong sekali".

### Sedang
Tidak ada.

### Ringan
- R-6. `VERSI = "1.0.0"` di stok.py baris 37 belum dinaikkan (`info --json` menampilkan `versi_alat: 1.0.0`), sedangkan catalog 1.1.0. Naikkan ke 1.1.0.
- R-7. Pesanan **baru** berstatus "Pembatalan Diajukan" memotong stok (sesuai tabel di marketplace.md: "stok dipotong, pesanan masih sah"), tetapi peringatan script berbunyi "belum pasti batal; **stok tidak diubah**" (uji X2: MUG 12 → 11 dengan peringatan itu). Bedakan teks untuk pesanan baru ("stok dipotong, tidak masuk daftar ambil") dan pesanan lama ("stok tidak diubah").
- R-8. Migrasi skema berjalan saat perintah baca pertama (mis. `laporan stok`) tanpa backup lebih dulu. Risikonya kecil (hanya `ALTER TABLE` + penandaan dalam transaksi), tetapi demi konsistensi dengan aturan "setiap perubahan dibackup", buat backup `sebelum-migrasi` sekali sebelum `ALTER`.
- R-9 (bawaan). Nama kolom TikTok versi Indonesia masih tebakan (sudah diakui di references). Minta 1 file ekspor asli dari beta tester sebelum rilis.

## Verifikasi angka independen
**Ya.** Sekitar 10.000 langkah acak dibandingkan dengan model penguji yang ditulis terpisah: HPP, stok, nilai persediaan, laporan ringkas per tanggal, dan laporan mutasi bulanan. Kasus Rp 243.000 dan migrasi DB v1.0.0 dihitung ulang secara manual.
