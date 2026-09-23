# 02 — "bikinin dong" kuitansi pelunasan Rp7,5 juta (wajib meterai)

**Skenario:** S2 — permintaan singkat/malas.

**Input pengguna (persis):**
> bikinin dong kuitansi pelunasan 7,5jt dari bu sari fiktif buat pesanan kue ultah. usaha saya dapur rina fiktif

**Yang dilakukan agent:** kuitansi tanpa daftar pembayaran = dianggap lunas penuh; tanggal hari ini.
```bash
python3 <folder-skill>/scripts/buat_invoice.py --file kuitansi-sari.json --html kuitansi-sari.html
```

## Output

# KUITANSI

**No.:** KWT/2026/09/0001  
**Tanggal:** 23 September 2026  
**Status:** LUNAS

Telah terima dari: **Ibu Sari Fiktif**  
Uang sejumlah: **Rp 7.500.000**  
Terbilang: _Tujuh Juta Lima Ratus Ribu Rupiah_  
Untuk pembayaran: Pelunasan pesanan kue ulang tahun

**Dari:**  
**Dapur Rina Fiktif**

**Kepada:**  
**Ibu Sari Fiktif**

| No | Deskripsi | Qty | Harga | Diskon | Jumlah |
|---:|---|---:|---:|---:|---:|
| 1 | Pelunasan pesanan kue ulang tahun | 1 paket | Rp 7.500.000 | - | Rp 7.500.000 |

| | |
|---|---:|
| Subtotal | Rp 7.500.000 |
| **TOTAL** | **Rp 7.500.000** |

Terbilang: _Tujuh Juta Lima Ratus Ribu Rupiah_

23 September 2026
[ Meterai Rp10.000 ]


**Dapur Rina Fiktif**

---
Info untuk penjual (jangan ikut dikirim):
- Bea meterai: Dokumen ini menyatakan penerimaan uang Rp 7.500.000 (> Rp5.000.000). Bea meterai Rp10.000 terutang (UU 10/2020): tempel meterai atau bubuhkan e-meterai sebelum ditandatangani.
- Pembulatan: jumlah baris & diskon dibulatkan ke rupiah terdekat.
- PERHATIAN: Nomor urut memakai 0001. Sebutkan nomor dokumen terakhir Anda agar nomor berurutan (--nomor-terakhir) atau pakai --counter-file.
- Versi HTML siap cetak disimpan di: kuitansi-sari.html

**Catatan untuk Anda:**
- Nilai Rp7.500.000 **di atas Rp5 juta → wajib meterai Rp10.000** (tempel atau e-meterai) sebelum tanda tangan.
- Nomor saya isi KWT/2026/09/0001. Kalau Anda punya nomor kuitansi terakhir, sebutkan supaya saya urutkan.
- Versi cetak: buka `kuitansi-sari.html` di browser → Cetak → Simpan PDF.

## Catatan penguji
- Meterai benar (> Rp5.000.000). Batas diuji terpisah: kuitansi **tepat Rp5.000.000 → tidak wajib**; Rp5.000.001 → wajib. Benar.
- Terbilang "Tujuh Juta Lima Ratus Ribu Rupiah" benar.
- Ringan: terbilang tercetak dua kali (di blok "Telah terima dari" dan di bawah tabel). Untuk kuitansi, blok bawah bisa dihilangkan.
- Pengingat nomor urut muncul otomatis — bagus.
