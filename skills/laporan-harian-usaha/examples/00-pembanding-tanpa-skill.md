# Uji A/B — Skenario 01 tanpa skill vs dengan skill

**Penguji:** agent independen, 2026-09-24. Data: "Kedai Kopi Senja" (fiktif, skenario 01).
**Permintaan sama:** "Laporan usaha hari ini dong." Agent diberi lokasi `kasir.db`, `stok.db`, `absensi.db`, `pengingat/DAFTAR.csv`.

## A. TANPA skill (agent umum, tanpa SKILL.md & script)
Simulasi jujur, disertai query yang benar-benar dijalankan penguji pada DB yang sama untuk melihat angka yang biasanya keluar.

Yang biasanya dilakukan agent umum:
1. Membuka tiap DB (`sqlite3` / Python), membaca `sqlite_master`, lalu menebak arti kolom. Sekitar 10–20 panggilan alat sebelum ada jawaban.
2. Kasir: tabel `nota` memiliki `bruto/netto/dpp/ppn/total` dan baris `void`/`retur` bernilai negatif. Pilihan query yang wajar dan hasilnya:
   - `SUM(total) WHERE jenis='jual'` → **Rp 414.040** (termasuk PBJT dan nota yang di-void) → omzet **lebih besar Rp 67.640 (19,5%)**.
   - `SUM(total)` semua baris → Rp 381.040 = uang diterima termasuk PBJT, dilabeli "omzet" → lebih besar Rp 34.640.
   - Jumlah nota `COUNT(*)` jual = 7 (nota void ikut dihitung), rata-rata jadi salah.
   - Tabel `sesi` (selisih kas) jarang dilirik jika tidak diminta; **kurang Rp 12.000 tidak dilaporkan**.
3. Stok: `SELECT … WHERE stok <= stok_min` pada `produk` biasanya benar (RTB −5, TEH 0, MCH 4). Tetapi hubungan kasir → buku-stok (nota 24/9 belum diimpor, jadi stok di layar terlalu tinggi) **tidak diketahui**.
4. Absensi: tabel `tap` berisi waktu mentah + `shift`. Agent harus menghitung terlambat sendiri (toleransi tidak diketahui), dan sering menyebut Yoga "lembur 2 jam 40 menit" dari jam pulang, padahal lembur tanpa persetujuan **bukan** lembur (PP 35/2021 Pasal 28, aturan absensi-lokal).
5. Pengingat: membaca CSV lalu menulis **"Bu Wulan belum bayar Rp 1,75 jt (katering arisan INV-031), CV Rekaan Jaya Rp 3,2 jt…"**, yaitu nama pelanggan, perihal, dan catatan pribadi masuk ke pesan yang nantinya dikirim ke Telegram.
6. Tiap malam (bila dijadwalkan lewat agent) query ditebak ulang, sehingga format dan cara hitung bisa berbeda dari hari ke hari.

Contoh output tipikal tanpa skill (disusun dari query di atas):
```
Ringkasan Kedai Kopi Senja - 24 Sep 2026
Omzet: Rp 414.040 dari 7 transaksi (rata-rata Rp 59.149)
Pembayaran: tunai, QRIS, transfer
Stok hampir habis: Roti Bakar (-5), Es Teh (0), Matcha (4)
Karyawan: Dimas, Lala, Yoga masuk. Lala telat. Yoga lembur 2 jam 40 menit.
Piutang: Bu Wulan Rp 1.750.000 (telat), CV Rekaan Jaya Rp 3.200.000 (hari ini)
```

## B. DENGAN skill
Output lengkap: `01-kafe-harian-empat-alat.md`. Ringkas: omzet bersih **Rp 346.400** (uang diterima Rp 381.040 dipisah dan selisih PBJT dijelaskan), 6 nota sah (+1 dibatalkan), rata-rata Rp 57.733, % vs kemarin dan vs Kamis lalu, per metode bayar, terlaris, retur/void, stok minus/habis/menipis + jumlah restock, kehadiran lengkap (sakit/alpa/belum absen), "lembur perlu keputusan" (bukan dihitung lembur), tagihan tanpa nama pelanggan, dan 6 butir PERLU PERHATIAN (selisih kas, void/retur, belum impor ke buku-stok, stok minus, lembur, piutang terlambat).

## Perbandingan
| Kriteria | Tanpa skill | Dengan skill |
|---|---|---|
| Omzet benar (tanpa pajak, setelah void/retur) | ❌ 414.040 / 381.040 (salah label) | ✅ 346.400 |
| Rata-rata per nota | ❌ membagi 7 nota termasuk void | ✅ 57.733 |
| Perbandingan % kemarin / minggu lalu | biasanya tidak ada atau dihitung kira-kira | ✅ 260,8% / 349,9% (rumus tertulis) |
| Selisih kas laci | ❌ terlewat | ✅ KURANG Rp 12.000 |
| Penjualan belum memotong buku-stok | ❌ tidak terdeteksi | ✅ terdeteksi (untuk hari yang belum diimpor sama sekali) |
| Lembur | ❌ lembur dari jam pulang (bertentangan dengan PP 35/2021) | ✅ "perlu keputusan" |
| Privasi pelanggan | ❌ nama + perihal pelanggan di pesan | ✅ hanya `#id jenis nominal` |
| Data asli aman | tidak dijamin (koneksi tulis biasa) | ✅ read-only + salinan, hash sama |
| Konsisten tiap malam / jadwal tanpa AI | ❌ | ✅ perintah langsung di OpenClaw, tanpa kuota model |
| Waktu | 10–20 panggilan alat | 1 perintah, 0,6 detik |

**Kesimpulan:** dengan skill **jelas lebih baik**: angka inti benar, masalah penting muncul otomatis, dan privasi terjaga. Syarat A/B terpenuhi.
