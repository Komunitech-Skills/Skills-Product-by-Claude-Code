# Uji 03 — Jasa laundry: 2 bulan, impor kasir-lokal, ekspor ke emkm & arus kas (normal)

Penguji independen Akun B, 2026-09-26. Data rekaan dibangkitkan skrip penguji (`bangun.py`, di scratchpad) lewat perintah `kas.py` biasa; nilai harapan disimpan terpisah lalu dihitung ulang dengan `Decimal`.

## Data
- "Laundry Bersih Kilat", mulai 01/08/2026, laci 1 jt, Mandiri 4 jt (penampung QRIS).
- Setiap hari 01/08–24/09: jualan tunai 250.000 + (tgl mod 5)×20.000, QRIS 120.000 + (tgl mod 3)×15.000.
- Senin: deterjen 180.000 tunai. Tgl 1 sewa 1,5 jt, tgl 5 listrik/PDAM 450.000, tgl 10 PPh final 60.000, tgl 28 gaji 2 jt (transfer Mandiri). Tgl 15 prive 800.000 tunai. Tiap Sabtu setor laci → Mandiri 500.000.
- 25/09 dan 26/09 dari **kasir-lokal 1.1.1** (salinan): 4 nota + 1 retur transfer (25/09); retur QRIS + 2 nota tunai (26/09).

## Impor kasir-lokal
`kasir.py rekap --tanggal 25/09/2026 --json` → `per_metode {Tunai 72000, QRIS 59000, Transfer 35000}`, total 166.000.
```
Impor rekap kasir-lokal Jumat, 25/09/2026 (uang diterima Rp 166.000):
- MASUK  Rp 72.000 | Penjualan | Tunai -> Laci kas
- MASUK  Rp 59.000 | Penjualan | QRIS -> Mandiri
- MASUK  Rp 35.000 | Penjualan | Transfer -> Mandiri
Pengeluaran laci (kasir.py kas --keluar) TIDAK ikut; ...
```
- Impor ulang → `GAGAL: Rekap kasir 25/09/2026 sudah pernah diimpor (#144, #145, #146) ... --ganti`. Benar.
- 26/09 `per_metode {QRIS -35000, Tunai 16000}` → `KELUAR Rp 35.000 Retur/refund penjualan (QRIS -> Mandiri)` + `MASUK Rp 16.000`. Setelah 1 nota tambahan, `--ganti` membatalkan #147, #148 dan mencatat Tunai 24.000. Rekap 26/09: hasil usaha −Rp 11.000. Benar.
- Rekap kasir **bulanan** ditolak ("Impor per HARI agar tanggal kas tepat"). Benar.

## Rekap & verifikasi independen (Decimal)
| Pos | Penguji | Script | Cocok |
|---|---|---|---|
| Saldo akhir Laci / Mandiri (26/09, sebelum impor 26/09) | 10.002.000 / 9.499.000, total 19.501.000 | sama | ya |
| Agustus: penjualan / hasil usaha / prive % | 13.155.000 / 8.245.000 / 9,7% | sama | ya |
| September: penjualan / hasil usaha / prive % | 10.406.000 / 7.856.000 / 10,2% | sama | ya |
| Saldo awal gabungan September | 12.445.000 | 12.445.000 | ya |
| Pindah dana bersih (8 kali) | 0 → tidak mengubah hasil usaha | tidak ikut di hasil usaha | ya |

## Ekspor ke laporan-keuangan-emkm (salinan, tidak diubah)
`kas.py ekspor --format emkm --bulan 08/2026 --csv kas-emkm-2026-08.csv` → `Tanggal;Keterangan;Masuk;Keluar;Kategori`, baris `Saldo awal;5000000`, kategori `pendapatan_usaha`, `beban_sewa`, `pembelian_bahan`, `beban_utilitas`, `beban_gaji`, `prive`; PPh final dikosongkan kategorinya. Pindah dana tidak ditulis.

Perintah yang disarankan script dijalankan apa adanya:
```
laporan_emkm.py kas-emkm-2026-08.csv --nama-usaha "Laundry Bersih Kilat" --periode-awal 2026-08-01 --periode-akhir 2026-08-31 --kas-akhir-aktual 12445000
```
Hasil emkm: `LABA (RUGI) BERSIH Rp 8.245.000` (= hasil usaha kas-umkm), PPh final 60.000 diklasifikasi emkm sebagai "Beban pajak penghasilan", Kas Rp 12.445.000, **neraca seimbang**. September: laba 7.856.000, kas 19.501.000, seimbang.
Catatan: teks ekspor menyebut "Pindah dana antar akun (10 baris)" — maksudnya 5 pindah × 2 sisi; bisa membingungkan awam (kosmetik).

## Ekspor ke arus-kas-13minggu (salinan, tidak diubah)
`kas.py ekspor --format arus-kas --csv rencana-kas.csv`:
```
semua;masuk;Penjualan (rata-rata riwayat);2975000;rata-rata 7 minggu (03/08/2026 - 20/09/2026)
semua;keluar;Beli stok (bahan/supplier);180000
tgl:28;keluar;Gaji karyawan;2000000;"... hanya sekali - pastikan memang bulanan";ya
tgl:5;keluar;Listrik/air;450000;ya | tgl:1;keluar;Sewa tempat;1500000;ya | tgl:10;keluar;Pajak;60000;ya
semua;keluar;Prive (ambil pribadi);228571;tidak
```
- Jendela 7 minggu penuh benar (01/08 = Sabtu, minggu penuh pertama mulai Senin 03/08); script memberi catatan "diminta 8".
- Penguji: penjualan 03/08–20/09 = 20.825.000 / 7 = 2.975.000; prive 1.600.000 / 7 = 228.571,43 → 228.571. Cocok.
- `proyeksi_kas.py rencana-kas.csv --saldo-awal 19501000 --mulai 2026-09-28` berjalan tanpa error; minggu 1 keluar 3.908.571 = 180.000 + 228.571 + sewa 1.500.000 (1/10) + gaji 2.000.000 (28/9). Cocok.
- Temuan kecil: prive yang nyatanya bulanan (tgl 15) diratakan per minggu (228.571), sehingga minggu tertentu di proyeksi terlihat lebih rendah/lebih tinggi dari kenyataan. Total 13 minggu tetap wajar; teks script sudah meminta agent menanyakan rencana khusus.

**Hasil: LULUS (9/10).** Rantai kasir-lokal → kas-umkm → emkm/arus-kas berjalan dan angkanya cocok ke rupiah.
