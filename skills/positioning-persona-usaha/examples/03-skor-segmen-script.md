# Contoh 03 — Skor segmen lewat script (FIKTIF)

Berkas `segmen.csv`:
```
segmen,ukuran,daya_beli,kebutuhan,jangkauan_kanal,kecocokan_produk,persaingan,kemampuan_layani
Karyawati muda kantoran,4,4,4,5,5,2,4
Ibu muda pengajian/arisan,3,3,4,4,4,3,5
Mahasiswi,5,2,3,5,3,2,4
Reseller kecil,3,3,3,4,4,2,2
```
Perintah: `python3 scripts/skor_segmen.py segmen.csv`
```
Bobot: ukuran 15, daya_beli 20, kebutuhan 20, jangkauan_kanal 15, kecocokan_produk 15, persaingan 10, kemampuan_layani 5
#  Segmen                              Skor  Saran
1  Karyawati muda kantoran             82.0  Utama (layani duluan)  [lemah: persaingan]
2  Ibu muda pengajian/arisan           72.0  Kandidat (uji kecil dulu)
3  Mahasiswi                           67.0  Kandidat (uji kecil dulu)  [lemah: daya_beli, persaingan]
4  Reseller kecil                      63.0  Kandidat (uji kecil dulu)  [lemah: persaingan, kemampuan_layani]
```
Cek manual segmen 2: (15x3 + 20x3 + 20x4 + 15x4 + 15x4 + 10x3 + 5x5) = 360; 360 / 100 x 20 = 72,0.

Data rusak (mis. nilai 6 pada `ukuran`): `GAGAL: Baris 2 (A): 'ukuran' harus 1-5, ditemukan 6` dan kode keluar 2; tidak ada skor palsu.
