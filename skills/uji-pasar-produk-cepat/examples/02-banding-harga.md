# Contoh 2: Bandingkan dua harga (A/B)

> Contoh ilustrasi fiktif. Angka keluaran script asli.

**Pengguna:** "Aku coba dua penawaran ke dua kelompok kontak: A = 10 pcs Rp35.000, B = 10 pcs Rp45.000 (tambah isi mentai lebih banyak). Masing-masing 60 orang, dipilih acak dari daftar. A: 9 bayar, B: 15 bayar. Mana yang menang?"

**Kriteria dikunci:** ukuran = bayar DP ÷ ditawari; pemenang hanya bila selisih meyakinkan (p < 0,05); jika tidak, pilih yang margin lebih tinggi dan uji ulang.

```
$ python3 scripts/hasil_eksperimen.py banding --a-ditawari 60 --a-aksi 9 --b-ditawari 60 --b-aksi 15
Varian A: 9/60 = 15,0% (rentang wajar 8,1% - 26,1%)
Varian B: 15/60 = 25,0% (rentang wajar 15,8% - 37,2%)
Selisih B - A: +10,0 poin persen
Nilai z = 1,37; p = 0,1709
Artinya: ada kecenderungan, tapi BELUM meyakinkan (p antara 0,05 dan 0,20). Tambah sampel atau ulang uji sebelum memutuskan.
```

**Keputusan:** belum ada pemenang pasti (selisih 10 poin, p = 0,17). Karena B pembelinya lebih banyak (bukan lebih sedikit) dan margin per pack lebih tinggi, pilih B sebagai acuan, lalu **uji ulang** dengan sampel lebih besar (mis. 140 dan 130 orang):

```
$ python3 scripts/hasil_eksperimen.py banding --a-ditawari 140 --a-aksi 17 --b-ditawari 130 --b-aksi 31
Varian A: 17/140 = 12,1% (rentang wajar 7,7% - 18,6%)
Varian B: 31/130 = 23,8% (rentang wajar 17,3% - 31,9%)
Selisih B - A: +11,7 poin persen
Nilai z = 2,51; p = 0,0120
Artinya: selisih ini cukup jelas (p < 0,05). Varian B memang lebih baik, bukan kebetulan (dengan keyakinan sekitar 95%).
```

Kesimpulan putaran kedua: B unggul jelas. Ambil Rp45.000.
