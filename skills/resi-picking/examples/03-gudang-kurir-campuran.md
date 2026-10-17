# Skenario 03 — Gudang kecil, kurir campuran JNE/J&T/SiCepat/SPX + cross-check stok (normal)

Data rekaan: 6 pesanan, header standar (mudah dideteksi otomatis — auto-deteksi kolom **berhasil
penuh** tanpa override, berbeda dengan skenario 02), file stok disertakan, 1 SKU sengaja "hantu"
(tidak ada di file stok) dan 3 SKU sengaja dibuat stoknya kurang dari kebutuhan.

## Perintah
```
python3 scripts/resi.py in_gudang_kecil.csv --stok stok_gudang.csv --json
```

## Hasil
- `jumlah_pesanan_total` = `jumlah_pesanan_aktif` = 6 (semua "Perlu Dikirim")
- `total_barang` = 23 pcs, kurir: JNE 2, J&T Express 1, SiCepat 1, SPX Express 2
- Peringatan yang muncul:
  - SKU tidak ada di file stok: `SKU-GHOST-99` ✅ (memang sengaja tidak didaftarkan)
  - Stok kurang `BOTOL-500`: butuh 7, stok 6 ✅ (2 pesanan: qty 2 + 5 = 7)
  - Stok kurang `TUMBLER-01`: butuh 3, stok 2 ✅
  - Stok kurang `TOTEBAG-01`: butuh 10, stok 3 ✅

## Verifikasi independen
Dihitung ulang manual dari 6 baris CSV: total qty = 2+1+3+5+10+2 = 23 ✅. Kebutuhan `BOTOL-500` =
2 (G-5001) + 5 (G-5004) = 7 vs stok 6 → kurang 1, sesuai peringatan. Kurir per pesanan unik: JNE
(G-5001, G-5006) = 2, J&T (G-5002) = 1, SiCepat (G-5003) = 1, SPX (G-5004, G-5005) = 2 — cocok.

`urutan-resi.md` mengelompokkan per kurir dengan urutan JNE, J&T Express, SiCepat, SPX Express dan
di dalam tiap kelompok terurut nomor resi menaik — sesuai dokumentasi. Catatan pembeli ("Tolong
bubble wrap") muncul tepat di baris pesanan SiCepat yang benar.

## Kesimpulan skenario 03
Semua angka, pengelompokan kurir, dan peringatan stok/SKU tidak dikenal 100% benar pada uji ini.
Ini skenario dengan header paling "ramah" (mirip persis daftar sinonim bawaan) — kontras dengan
skenario 02 yang headernya lebih dekat ke nama kolom marketplace asli.

## Penyegaran v1.0.5 (2026-10-17)
> Hasil dan skor uji asli di atas **tidak diubah**. File input (`in_gudang_kecil.csv`, `stok_gudang.csv`) tidak disimpan di repo, jadi skrip tidak dijalankan ulang. Dengan file stok, v1.0.5 menambah bagian **Stok setelah dikemas** (field `stok_setelah` / `status_stok_setelah`). Dari angka di atas: BOTOL-500 stok 6 → −1 (kurang 1), TUMBLER-01 2 → −1 (kurang 1), TOTEBAG-01 3 → −7 (kurang 7), dan SKU-GHOST-99 disebut terpisah karena tidak ada di file stok (dihitung ulang: 6 − 7, 2 − 3, 3 − 10). Baris "Pesanan di file: 6 (6 diproses)" dan "Dilewati: tidak ada." juga wajib ditulis.
