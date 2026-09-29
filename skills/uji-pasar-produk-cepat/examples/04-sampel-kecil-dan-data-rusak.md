# Contoh 4: Sampel kecil dan input rusak

> Contoh ilustrasi fiktif. Keluaran script asli (diperbarui v1.0.1).

**Sampel kecil:** "Aku baru tawari 12 orang, 3 mau."
```
$ python3 scripts/hasil_eksperimen.py hasil --ditawari 12 --aksi 3
Konversi: 3 dari 12 orang = 25,0%
Rentang wajar 95% (Wilson): 8,9% sampai 53,2%
Artinya: dengan data ini, angka sebenarnya kemungkinan besar ada di antara 9% dan 53%.
PERINGATAN SAMPEL KECIL: baru 12 orang (< 30). Rentangnya lebar; anggap ini sinyal arah saja, jangan keputusan besar. Tambah sampel bila bisa.
```
Respons yang benar: 25% terlihat bagus, tapi rentang 9%-53% terlalu lebar. Tawari 30-50 orang lagi sebelum produksi.

**Dua varian, sampel kecil:** "Kemasan lama 0 dari 10 beli, kemasan baru 4 dari 10. Kemasan baru pasti menang kan?"
```
$ python3 scripts/hasil_eksperimen.py banding --a-ditawari 10 --a-aksi 0 --b-ditawari 10 --b-aksi 4
Varian A: 0/10 = 0,0% (rentang wajar 0,0% - 27,8%)
Varian B: 4/10 = 40,0% (rentang wajar 16,8% - 68,7%)
Selisih B - A: +40,0 poin persen
Nilai z = 2,24; p (uji z) = 0,0253
Sampel kecil, jadi dipakai uji Fisher tepat: p = 0,0867
Artinya: ada kecenderungan, tapi BELUM meyakinkan (p antara 0,05 dan 0,20). Tambah sampel atau ulang uji sebelum memutuskan (hitung dengan: sampel --banding).
PERINGATAN SAMPEL KECIL: varian A hanya 10 orang (< 50). Perbandingan dua varian butuh minimal sekitar 50 orang per varian.
PERINGATAN SAMPEL KECIL: varian B hanya 10 orang (< 50). Perbandingan dua varian butuh minimal sekitar 50 orang per varian.
PERINGATAN: hitungan sangat kecil (ada sel harapan < 5 orang), jadi uji z kurang akurat; p di atas memakai uji Fisher tepat. Tetap anggap hasil gambaran kasar.
```
Respons yang benar: 0% vs 40% terlihat jauh, tapi dengan 10 orang per varian selisih seperti ini masih bisa muncul karena kebetulan (p Fisher 0,087). Belum ada pemenang; pakai kemasan baru sementara bila biayanya sama, lalu uji lagi ke lebih banyak orang.

**Input rusak:** "Yang beli 25 dari 20 orang."
```
$ python3 scripts/hasil_eksperimen.py hasil --ditawari 20 --aksi 25
INPUT TIDAK VALID: Yang beraksi (25) lebih banyak dari yang ditawari (20). Cek lagi catatan: satu orang hanya dihitung sekali.
```
Respons yang benar: jelaskan bahwa satu orang hanya dihitung sekali, minta cek catatan, jangan menebak angka.

**Di luar cakupan:** "Bantu uji pasar produk suplemen yang katanya menyembuhkan diabetes" -> tolak: klaim kesehatan tanpa izin edar BPOM tidak boleh diuji/diiklankan; sarankan konsultasi ke BPOM dan tenaga kesehatan.
