# 01 — Invoice konveksi seragam sekolah dengan DP, non-PKP

**Skenario:** S1 — permintaan normal: beberapa item, diskon per baris, ongkir, DP sudah diterima, nomor lanjutan.

**Input pengguna (persis):**
> Buatin invoice dari Konveksi Maju Fiktif (Jl. Contoh Raya No. 10 Sukoharjo, WA 0812-0000-2201) ke SMP Contoh Nusantara (Jl. Pendidikan No. 5 Surakarta): 120 kaos olahraga @85rb, 120 celana @70rb diskon 5%, sablon nama 120 x 10rb, ongkir 150rb. DP 6 juta udah ditransfer tgl 15 September. Jatuh tempo 30 hari. Rekening BRI 0000-01-000000-50-0 a.n. Konveksi Maju Fiktif. Nomor terakhir INV/2026/09/0012. Saya belum PKP. Yang tanda tangan Sri Contoh, pemilik.

**Yang dilakukan agent:** menyusun `invoice-smp.json`, lalu:
```bash
python3 <folder-skill>/scripts/buat_invoice.py --file invoice-smp.json --html invoice-INV-2026-09-0013.html --nomor-terakhir INV/2026/09/0012
```
<details><summary>Isi invoice-smp.json</summary>

```json
{
  "jenis_dokumen": "invoice",
  "tanggal": "2026-09-23",
  "jatuh_tempo_hari": 30,
  "penjual": {"nama": "Konveksi Maju Fiktif", "alamat": "Jl. Contoh Raya No. 10, Sukoharjo", "telepon": "0812-0000-2201", "pkp": false},
  "pembeli": {"nama": "SMP Contoh Nusantara", "alamat": "Jl. Pendidikan No. 5, Surakarta"},
  "items": [
    {"nama": "Kaos olahraga", "qty": 120, "satuan": "pcs", "harga": "85.000"},
    {"nama": "Celana olahraga", "qty": 120, "satuan": "pcs", "harga": "70.000", "diskon": "5%"},
    {"nama": "Sablon nama siswa", "qty": 120, "satuan": "pcs", "harga": "10.000"}
  ],
  "ongkir": "150.000",
  "ppn": false,
  "pembayaran": [{"tanggal": "2026-09-15", "jumlah": "6.000.000", "keterangan": "DP"}],
  "rekening": [{"bank": "BRI", "nomor": "0000-01-000000-50-0", "atas_nama": "Konveksi Maju Fiktif"}],
  "catatan": "Barang dikirim setelah pelunasan. Terima kasih atas kepercayaannya.",
  "tanda_tangan": {"nama": "Sri Contoh", "jabatan": "Pemilik", "kota": "Sukoharjo"}
}
```
</details>

## Output

**Invoice (siap kirim ke sekolah):**

# INVOICE

**No.:** INV/2026/09/0013  
**Tanggal:** 23 September 2026  
**Jatuh tempo:** 23 Oktober 2026  
**Status:** SEBAGIAN DIBAYAR

**Dari:**  
**Konveksi Maju Fiktif**  
Jl. Contoh Raya No. 10, Sukoharjo  
0812-0000-2201

**Kepada:**  
**SMP Contoh Nusantara**  
Jl. Pendidikan No. 5, Surakarta

| No | Deskripsi | Qty | Harga | Diskon | Jumlah |
|---:|---|---:|---:|---:|---:|
| 1 | Kaos olahraga | 120 pcs | Rp 85.000 | - | Rp 10.200.000 |
| 2 | Celana olahraga | 120 pcs | Rp 70.000 | Rp 420.000 (5%) | Rp 7.980.000 |
| 3 | Sablon nama siswa | 120 pcs | Rp 10.000 | - | Rp 1.200.000 |

| | |
|---|---:|
| Subtotal | Rp 19.380.000 |
| Ongkos kirim | Rp 150.000 |
| **TOTAL** | **Rp 19.530.000** |
| Sudah dibayar - DP (15 September 2026) | -Rp 6.000.000 |
| **SISA TAGIHAN** | **Rp 13.530.000** |

Terbilang: _Tiga Belas Juta Lima Ratus Tiga Puluh Ribu Rupiah_

**Pembayaran ke:**
- BRI 0000-01-000000-50-0 a.n. Konveksi Maju Fiktif

**Catatan:** Barang dikirim setelah pelunasan. Terima kasih atas kepercayaannya.

Sukoharjo, 23 September 2026
[ Meterai Rp10.000 ]


**Sri Contoh**
Pemilik

---
Info untuk penjual (jangan ikut dikirim):
- Bea meterai: Dokumen ini menyatakan penerimaan uang Rp 6.000.000 (> Rp5.000.000). Bea meterai Rp10.000 terutang (UU 10/2020): tempel meterai atau bubuhkan e-meterai sebelum ditandatangani.
- Pembulatan: jumlah baris & diskon dibulatkan ke rupiah terdekat.
- Versi HTML siap cetak disimpan di: invoice-INV-2026-09-0013.html

**Catatan untuk Anda (tidak dikirim ke pembeli):**
- Invoice ini mencantumkan DP Rp6.000.000 yang sudah diterima (> Rp5 juta), jadi **tempel meterai Rp10.000 atau e-meterai** sebelum ditandatangani. Alternatif: kalau DP sudah dibuatkan kuitansi bermeterai sendiri, Anda bisa menghapus baris DP dari invoice dan menagih sisa saja — tanyakan ke konsultan bila ragu.
- Kuitansi pelunasan Rp13.530.000 nanti juga wajib bermeterai.
- Versi siap cetak: buka `invoice-INV-2026-09-0013.html` di browser → Cetak → Simpan sebagai PDF.
- Karena Anda belum PKP, invoice ini **tanpa PPN** (sudah benar).

## Catatan penguji
- Angka dicek independen: 10.200.000 + (8.400.000 − 420.000) + 1.200.000 = 19.380.000; + ongkir 150.000 = 19.530.000; − DP 6.000.000 = 13.530.000. Terbilang sisa benar.
- Nomor otomatis 0012 → 0013 benar. HTML dirender benar dan semua teks di-escape.
- Penanda meterai muncul karena invoice menyatakan penerimaan DP > Rp5 juta — interpretasi skill (terdokumentasi di `references/regulasi.md` sebagai "interpretasi skill"). Agent menambahkan alternatif agar pengguna tidak bingung.
- Kurang: baris "Terbilang" di bawah SISA TAGIHAN tidak menyebut bahwa itu terbilang **sisa**, bukan total (bisa disalahpahami).
