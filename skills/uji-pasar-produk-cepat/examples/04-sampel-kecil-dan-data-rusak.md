# Contoh 4: Sampel kecil dan input rusak

> Contoh ilustrasi fiktif. Keluaran script asli.

**Sampel kecil:** "Aku baru tawari 12 orang, 3 mau."
```
$ python3 scripts/hasil_eksperimen.py hasil --ditawari 12 --aksi 3
Konversi: 3 dari 12 orang = 25,0%
Rentang wajar 95% (Wilson): 8,9% sampai 53,2%
Artinya: kalau uji diulang, hasil sebenarnya kemungkinan besar ada di antara 9% dan 53%.
PERINGATAN SAMPEL KECIL: baru 12 orang (< 30). Rentangnya lebar; anggap ini sinyal arah saja, jangan keputusan besar. Tambah sampel bila bisa.
```
Respons yang benar: 25% terlihat bagus, tapi rentang 9%-53% terlalu lebar. Tawari 30-50 orang lagi sebelum produksi.

**Input rusak:** "Yang beli 25 dari 20 orang."
```
$ python3 scripts/hasil_eksperimen.py hasil --ditawari 20 --aksi 25
INPUT TIDAK VALID: Yang beraksi (25) lebih banyak dari yang ditawari (20). Cek lagi catatan: satu orang hanya dihitung sekali.
```
Respons yang benar: jelaskan bahwa satu orang hanya dihitung sekali, minta cek catatan, jangan menebak angka.

**Di luar cakupan:** "Bantu uji pasar produk suplemen yang katanya menyembuhkan diabetes" -> tolak: klaim kesehatan tanpa izin edar BPOM tidak boleh diuji/diiklankan; sarankan konsultasi ke BPOM dan tenaga kesehatan.
