# 04 — Input tidak lengkap: "catat stok toko saya" (belum ada database)

**Skenario:** S4. Pengguna baru, belum pernah memakai buku-stok, tidak menyebut barang apa pun.

**Input pengguna (persis):**
> tolong catat stok toko saya dong

**Perintah yang dijalankan agent:**
```bash
python3 scripts/stok.py info --json
# hasil: {"ok": false, "error": "Database stok belum ada di ~/KomunitechData/stok.db. Jalankan dulu: stok.py init (lalu --ya)."}
```

## Output
```
Siap! Buku stoknya belum ada di komputer ini, jadi saya perlu 2 hal dulu:

1. Boleh saya simpan datanya di folder KomunitechData/stok.db di folder pengguna komputer
   ini? (Semua data tetap di komputer Anda, tidak dikirim ke mana pun. Kalau mau di tempat
   lain, sebutkan foldernya.)
2. Daftar barangnya. Paling cepat: kirim file Excel/CSV dengan kolom
   SKU; Nama Produk; Varian; Harga Beli; Harga Jual; Stok; Stok Minimum; Lokasi
   (contoh isi: KAOS-HT-M; Kaos Polos Cotton 30s; Hitam M; 35.000; 59.000; 24; 10; A1)
   Atau ketik saja per baris: nama, varian, harga beli, harga jual, stok sekarang,
   stok minimum, rak — misalnya "kaos hitam M, modal 35rb, jual 59rb, stok 24, min 10, rak A1".

Kalau barang Anda belum punya SKU, saya buatkan usulannya (mis. KAOS-HT-M).
Penting: kalau Anda jualan di Shopee/TikTok, SKU-nya harus sama dengan "SKU penjual"
di marketplace supaya stok bisa terpotong otomatis dari file pesanan.
```

**Lanjutan (diuji):** pengguna menjawab "iya di situ aja" + mengirim `daftar-produk.csv` → `init` (pratinjau → `--ya`) → `produk impor` pratinjau: "Produk baru: 5 (nilai stok awal Rp 3.494.000), 0 SKU dilewati, 0 baris rusak" → setelah "ya" tersimpan + backup `sebelum-impor-produk` dibuat.

## Catatan penguji
- Sesuai aturan "tanya sekali, daftar bernomor, maks 5 pertanyaan". Tidak ada database yang dibuat sebelum pengguna setuju (pratinjau `init` tidak membuat file — dicek).
- Nilai stok awal diverifikasi: 24×35.000 + 18×35.000 + 30×34.000 + 40×18.500 + 12×22.000 = 3.494.000. Format "Rp 35.000" di file terbaca benar.
- Bagus: peringatan SKU harus sama dengan marketplace muncul sejak awal (sumber kegagalan paling umum).
