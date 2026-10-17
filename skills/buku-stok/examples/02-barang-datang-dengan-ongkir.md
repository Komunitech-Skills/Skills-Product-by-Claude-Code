# 02 — Barang datang, ongkir kulakan masuk ke HPP

**Skenario:** S2 (normal, bahasa sehari-hari). Stok Kaos Hitam M saat ini 24 pcs dengan HPP Rp 35.000. Supplier mengirim 50 pcs @ Rp 34.000, ongkir kulakan Rp 25.000.

**Input pengguna (persis):**
> barang dateng nih, kaos item M 50 pcs harga 34rb, ongkirnya 25rb. nota dari supplier no 0923

**Perintah yang dijalankan agent:**
```bash
python3 scripts/stok.py produk cari hitam --json      # memastikan SKU "kaos item M" = KAOS-HT-M
python3 scripts/stok.py masuk --sku KAOS-HT-M --qty 50 --harga 34000 --biaya-tambahan 25000 --ref "Nota-Supplier-0923" --json
# setelah "ya":
python3 scripts/stok.py masuk --sku KAOS-HT-M --qty 50 --harga 34000 --biaya-tambahan 25000 --ref "Nota-Supplier-0923" --ya --json
```

## Output

**Balasan agent 1:**
```
Saya akan mencatat (belum disimpan):
- Kaos Polos Cotton 30s Hitam M, kode barang (SKU) KAOS-HT-M: barang datang +50 @ Rp 34.000
  (+ ongkir Rp 25.000, jadi Rp 34.500 per pcs)
  Stok 24 -> 74
  Modal rata-rata per barang (HPP) Rp 35.000 -> Rp 34.662
- Total nilai masuk: Rp 1.725.000 (sudah termasuk ongkir)
- No. nota: Nota-Supplier-0923

"Kaos item M" saya cocokkan ke Kaos Polos Cotton 30s Hitam M (kode KAOS-HT-M).
Simpan? Balas "ya" untuk menyimpan.
```

**Pengguna:** ya

**Balasan agent 2:**
```
Sudah tersimpan. Stok Kaos Hitam M sekarang 74 pcs, modal rata-rata Rp 34.662.
Harga beli terakhir juga diperbarui menjadi Rp 34.000.
```

## Catatan penguji
- Verifikasi independen: (24 × 35.000 + 50 × (34.000 + 25.000/50)) ÷ 74 = 2.565.000 ÷ 74 = 34.662,16 → tampil Rp 34.662. Benar.
- Verifikasi massal: 3 × 400 transaksi acak (masuk tunggal & nota multi-item dengan biaya tambahan dibagi sesuai nilai, keluar, opname, penolakan stok kurang) dibandingkan dengan model HPP rata-rata tertimbang yang ditulis penguji sendiri → selisih HPP 0, stok 0, nilai persediaan sama persis (mis. Rp 79.355.691), stok produk = Σ mutasi, dan kolom `stok_sesudah` tiap mutasi = saldo kumulatif.
- Bagus: agent mencocokkan "item" = hitam lewat `produk cari`, dan tetap menyebut SKU yang dipakai sebelum menyimpan.
- Koreksi penguji: "Total nilai masuk Rp 1.725.000" **sudah termasuk** ongkir (50 × Rp 34.500 = 50 × Rp 34.000 + Rp 25.000). Catatan di laporan uji v1.0.0 yang menyebut sebaliknya keliru.
- Uji ulang v1.1.0: output identik (stok 24 → 74, HPP Rp 34.662).
- Teks balasan disesuaikan ke v1.1.7 (HPP dan SKU dijelaskan saat pertama muncul). Barang masuk biasa **tidak** membuat cadangan, jadi balasan 2 sengaja tidak menyebut cadangan (di rekaman tidak ada kunci `backup` pada hasil `--ya`).
