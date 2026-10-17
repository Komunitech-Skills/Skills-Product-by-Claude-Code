# 04 — Input tidak lengkap: "catat stok toko saya" (belum ada buku stok)

> **Dibuat ulang untuk v1.1.7.** Rekaman uji sebelum v1.1.7 menanyakan "boleh saya simpan di folder ..." dan menyebut letak berkas ke pemilik toko. Itu sudah tidak berlaku: sejak v1.1.7 balasan tidak pernah menyebut letak file/folder atau nama perintah, dan lokasi simpan tidak ditanyakan (pakai default).

**Skenario:** S4. Pengguna baru, belum pernah memakai buku-stok, tidak menyebut barang apa pun.

**Input pengguna (persis):**
> tolong catat stok toko saya dong

**Perintah yang dijalankan agent (hanya untuk agent, tidak disebut ke pengguna):**
```bash
python3 scripts/stok.py info --json
# hasil: {"ok": false, "error": "Buku stok belum disiapkan di komputer ini.", "langkah_agen": "Jalankan init (pratinjau), gabungkan dalam satu konfirmasi dengan daftar barang ..."}
```

## Output

**Balasan agent 1 (satu permintaan: daftar barang):**
```
Siap! Buku stoknya belum ada di komputer ini, jadi saya perlu daftar barangnya dulu.

Paling cepat: kirim file Excel/CSV daftar barang Anda (kolom: kode barang, nama, varian, harga beli, harga jual, stok). Atau ketik saja per barang, misalnya "kaos hitam M, modal 35rb, jual 59rb, stok 24".

Semua data tersimpan di komputer Anda sendiri, tidak dikirim ke mana pun. Kalau barang Anda belum punya kode barang (SKU), saya buatkan. Kalau Anda jualan di Shopee/TikTok, kode barangnya sebaiknya sama dengan "SKU penjual" di marketplace supaya stok bisa terpotong otomatis dari file pesanan.
```

**Pengguna:** (mengirim `daftar-produk.csv`)

**Balasan agent 2 (satu persetujuan, buku stok disiapkan sekalian):**
```
Saya akan menyiapkan buku stok dan mencatat 5 barang dari file Anda (belum disimpan):
- Kaos Polos Cotton 30s Hitam M, Hitam L, Putih M; Tote Bag Kanvas Natural; Mug Keramik Putih
- Nilai stok awal (total modal yang tertahan di stok): Rp 3.494.000
- Tidak ada baris yang dilewati atau rusak

Simpan? Balas "ya" untuk menyimpan.
```

**Pengguna:** ya → (di balik layar: buku stok disiapkan, daftar barang disimpan; hasil impor memuat `backup`)
```
Sudah tersimpan: 5 barang, nilai persediaan Rp 3.494.000. Cadangan otomatis sudah dibuat. Catatan stok Anda tersimpan di komputer ini. Setiap barang datang atau terjual, cukup bilang ke saya.
```

## Catatan penguji
- Sesuai aturan "satu permintaan per pesan": pesan pertama hanya meminta daftar barang (tidak menanyakan lokasi simpan, stok minimum, atau rak); pesan kedua hanya satu persetujuan. Tidak ada buku stok yang dibuat sebelum pengguna setuju (pratinjau impor dihitung di catatan sementara di memori; dicek: tidak ada berkas atau folder yang muncul).
- Nilai stok awal diverifikasi: 24×35.000 + 18×35.000 + 30×34.000 + 40×18.500 + 12×22.000 = 3.494.000. Format "Rp 35.000" di file terbaca benar.
- Kalimat "Cadangan otomatis sudah dibuat" boleh muncul di sini karena impor barang memang membuat cadangan (hasil `--ya` memuat `backup`). Untuk barang masuk/keluar biasa kalimat itu tidak boleh dipakai.
- Peringatan "kode barang harus sama dengan SKU penjual di marketplace" muncul sejak awal (sumber kegagalan paling umum).
