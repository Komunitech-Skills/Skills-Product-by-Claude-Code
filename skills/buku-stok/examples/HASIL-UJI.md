# HASIL UJI — buku-stok

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Lingkungan:** Python 3.11, DB sementara di `/tmp/uji-buku-stok/*/stok.db` (`--db`), OpenClaw 2026.9.5 dengan Gateway lokal uji (HOME terpisah, tanpa model/kanal)
- **Versi skill:** 1.0.0 (catalog: draft)

## Yang diuji
| Uji | Hasil |
|---|---|
| `scripts/uji_regresi.py` | 30 tes OK (7,5 dtk; 2.750 mutasi, impor 1.500 baris 0,09 dtk) |
| HPP rata-rata tertimbang — 3 × 400 transaksi acak (masuk tunggal/multi-item + biaya tambahan dibagi sesuai nilai, keluar, opname, penolakan stok kurang) vs model independen penguji | HPP selisih 0; stok cocok; nilai persediaan identik (Rp 79.355.691 / 36.963.451 / 38.744.925); 46 penolakan stok kurang benar |
| Stok = Σ mutasi; `stok_sesudah` = saldo kumulatif | 0 pelanggaran |
| Pratinjau tanpa `--ya` tidak menyimpan | md5 DB identik sebelum/sesudah pratinjau impor; `init` pratinjau tidak membuat file |
| Impor Shopee CSV (35 kolom, status campuran, baris kembar, nomor `2.60923E+17`) | Benar (lihat 01) |
| Impor ulang file sama | 0 pesanan baru, 4 dilewati |
| Shopee XLSX hari berikutnya (openpyxl): batal setelah impor, belum bayar → dibayar, dikirim → pengembalian, SKU belum terdaftar | Stok batal dikembalikan +3; pesanan dibayar terpotong; retur hanya dilaporkan; SKU asing ditolak saat `--ya` sampai `--lewati-tak-dikenal` |
| TikTok Shop CSV (header Inggris + baris keterangan kolom) | Pemetaan benar, baris keterangan dilewati, Cancelled/Unpaid diabaikan |
| TikTok Shop CSV versi UI bahasa Indonesia (nama kolom **tebakan penguji**) | Lihat cacat S-4 |
| Tokopedia XLSX (2 baris judul di atas header, "Nomor Invoice", "Jumlah Produk Dibeli", "Harga Jual (IDR)") | Header ditemukan di baris 4, pemetaan benar; "Menunggu Konfirmasi Penjual" & "Pesanan Dikomplain" → dihitung terjual + peringatan |
| Opname (file template, selisih tanpa alasan, pesanan belum dikemas) | Selisih & nilai benar; `--ya` ditolak bila alasan kosong; pesanan belum dikemas ikut dihitung (sistem 9 + 2 = 11) |
| Backup/restore | Backup manual & otomatis; restore pratinjau tidak mengubah DB; restore `--ya` memulihkan + backup "sebelum-restore"; file bukan DB ditolak |
| Input buruk | qty 0 ditolak; `15.000.00` ditolak; `Rp 1.500.000,50` benar; file kosong & kolom wajib hilang → pesan jelas; SKU huruf kecil diterima |
| Perintah OpenClaw di SKILL.md (`automations add --name --cron --tz --message --announce --channel telegram --to`) | Dijalankan sungguhan di Gateway uji: job tercipta, `0 21 * * *` @ Asia/Jakarta, delivery `announce -> telegram`. `list/run/disable/rm <id>` valid (`--help`) |
| Audit keamanan | Hanya library standar; tidak ada jaringan/subprocess/eval; tidak membaca kredensial; SQL berparameter; tidak ada prompt injection. Data pembeli di file tidak dicetak ke output |

## Skor
| Kriteria | Skor |
|---|---|
| Pemicu (description tepat) | 9 |
| Kemudahan awam | 8 |
| Kualitas output | 8 |
| Akurasi (angka/fakta) | 6 |
| Penanganan input kurang | 9 |
| Penanganan di luar cakupan | 9 |
| Keamanan | 9 |
| **SKOR AKHIR** | **6 / 10 — REVISI** |

Alasan: mesin stok & HPP sangat solid (terverifikasi independen), jauh di atas pesaing dan jawaban tanpa skill. Tetapi ada **angka laporan yang salah** saat pesanan batal setelah diimpor (kejadian harian di Shopee/TikTok), dan laporan itulah yang dijadwalkan terkirim ke Telegram. Sesuai aturan brief, cacat berat membatasi skor ≤ 6. Perbaikannya kecil; setelah diperbaiki, skill ini layak 8–9.

## Daftar cacat

### Berat
**B-1. Pesanan batal setelah impor tetap dihitung sebagai penjualan di laporan.**
Uji: 0002CD (3 × KAOS-PT-M @ Rp 57.000) diimpor lalu batal di file berikutnya. `laporan ringkas --tanggal 2026-09-23` → "Terjual 8 barang dari 2 pesanan", omzet Rp 414.000, HPP Rp 234.500, KAOS-PT-M (3) di "Terlaris" (seharusnya 5 barang, omzet Rp 243.000, HPP Rp 132.500). `laporan mutasi` mengurangi HPP batal (`hpp_batal`) tetapi "Penjualan tercatat" tetap Rp 577.000 (lebih Rp 171.000) → laba kotor terlalu besar.
*Perbaikan:* di `lap_ringkas` (stok.py ±baris 1776–1790) dan `lap_mutasi` (±baris 1752–1755), kecualikan mutasi `jual-mp` yang `ref`-nya pesanan `dibatalkan=1` (JOIN `pesanan` via `pesanan_item.mutasi_id`), atau kurangi `batal-pesanan` dari qty/omzet/top memakai harga jual asli (`pesanan_item.harga`). Tambahkan tes regresi "batal setelah impor → laporan ringkas & mutasi".

### Sedang
**S-1. Pesanan yang diimpor dengan `--lewati-tak-dikenal` tidak pernah terpotong walau SKU kemudian didaftarkan.** Uji: 2609240008OP (KAOS-HT-XL) → `produk tambah KAOS-HT-XL` → impor ulang: "Pesanan baru: 0", stok XL tetap 10, tanpa peringatan; picking tetap menandai "belum terdaftar".
*Perbaikan:* di `cmd_impor_pesanan` cabang `lama is not None` (±baris 1372), untuk `pesanan_item` dengan `produk_id IS NULL` coba `_cocokkan_produk` lagi → bila cocok, catat mutasi keluar + isi `produk_id/mutasi_id`, dan laporkan "N item pesanan lama kini terpotong". Sebutkan di SKILL.md bagian C.4.

**S-2. "Pembatalan diajukan" langsung dianggap batal; bila pembatalan ditolak, stok tidak pernah dipotong ulang.** Uji: X1 Perlu Dikirim (MUG 12→10) → "Pembatalan Diajukan" (stok kembali 12) → "Perlu Dikirim" lagi: stok tetap 12, tanpa peringatan. Sama untuk "Cancellation requested".
*Perbaikan:* `kategori_status` (±baris 1211): status mengandung "diajukan/requested/permintaan/menunggu" + batal → kategori `batal_diajukan` (diperlakukan seperti "lainnya": tidak mengubah stok, beri peringatan). Di cabang pesanan lama `dibatalkan=1` yang kini perlu_kirim/dikirim/selesai → potong ulang + peringatan.

**S-3. TikTok Shop: harga tidak terpetakan → omzet TikTok Rp 0 di laporan.** Kolom ekspor TikTok memakai "SKU Unit Original Price" / "SKU Subtotal After Discount"; tidak ada sinonim yang cocok, jadi semua baris "jual tanpa harga".
*Perbaikan:* tambahkan sinonim `SINONIM_PESANAN["harga"]` untuk "sku unit original price", "sku subtotal after discount" (dibagi qty — perlu opsi "harga adalah subtotal"), dan dokumentasikan di `references/marketplace.md`.

**S-4. Ekspor TikTok Shop dengan UI bahasa Indonesia (perlu dicek dengan file asli; nama kolom di uji ini tebakan penguji):** status "Akan dikirim" → kategori `dikirim` (karena mengandung "dikirim") sehingga **tidak masuk daftar ambil**; kolom "ID Pelacakan", "Nama Penyedia Pengiriman", "Waktu Dibuat" tidak dikenali (urutan resi kosong); harga memetakan "Harga Satuan Asli SKU" (sebelum diskon); platform terbaca "lainnya".
*Perbaikan:* tambah "akan dikirim", "menunggu pengiriman" ke `KATA_PERLU_KIRIM` (diperiksa sebelum `KATA_DIKIRIM`); sinonim "id pelacakan", "nama penyedia pengiriman", "waktu dibuat"; mintalah contoh ekspor asli dari beta tester untuk ketiga marketplace dan simpan sebagai fixture tes.

### Ringan
- R-1. Teks `laporan ringkas` "Terjual: 12 barang dari 2 pesanan marketplace" padahal 6 barang dari penjualan offline; "Restock ... (Rp 1.725.000)" tanpa biaya tambahan. SKILL.md menyuruh mengirim teks apa adanya → pisahkan "marketplace" vs "toko", dan tampilkan nilai restock termasuk biaya (±baris 1802–1808).
- R-2. Tokopedia "Menunggu Konfirmasi Penjual" dipotong sebagai "lainnya" dan tidak masuk picking; pertimbangkan kategori `perlu_kirim` atau abaikan sampai diterima (tetap dengan peringatan).
- R-3. TikTok "Completed" dengan "Cancelation/Return Type = Return/Refund" dihitung terjual tanpa peringatan; kolom tipe batal/retur & "Returned quantity" (Shopee) belum dibaca.
- R-4. `--ya` yang gagal (mis. opname tanpa alasan) tetap membuat file backup (backup dibuat sebelum transaksi di `jalankan_tulis`) → folder backup bertambah file tak berguna.
- R-5. Jadwal OpenClaw yang dibuat berjalan dengan `toolsAllow: ["*"]` (terlihat di hasil `automations add`); pembatasan "hanya baca" hanya lewat teks prompt. Sarankan menambah `--tools exec,read` (flag ada di `automations add --help`) dan `--session isolated` di contoh SKILL.md bagian "Laporan terjadwal".

## Verifikasi angka independen
**Ya.** HPP, stok, nilai persediaan (1.200 transaksi acak), impor 3 marketplace, opname, laporan ringkas & menipis dihitung ulang dengan Python terpisah.
