# Uji 06 (Penguji Independen) — Input Tidak Lengkap

## Skenario
Pengguna hanya menyebut ingin lapor, tanpa angka, tanpa penerima, tanpa tujuan jelas.

## Input pengguna (simulasi)
> "Bikinin laporan buat atasan dong."

## Perilaku yang diharapkan (sesuai SKILL.md bagian Input & langkah kerja)
Info wajib yang hilang: (1) angka/data itu sendiri — **wajib**, tidak ada default
(harus ditanya, dilarang mengarang); (2) untuk siapa — ada di teks pengguna ("atasan")
tapi generik; (3) tujuan — tidak disebut, boleh ditebak dari data (tapi data belum ada).

Karena angka wajib dan tidak boleh diasumsikan/dikarang ("Jangan pernah mengisi angka
yang tidak disebutkan/tidak ada di data, sekalipun terdengar masuk akal" — langkah 1),
skill **harus berhenti dan bertanya sekali** dalam satu pesan gabungan, bukan langsung
membuat laporan dengan angka fiktif.

## Output yang benar (simulasi respons skill)
```
Baik, saya bisa bantu buatkan laporan untuk atasan. Sebelum itu, boleh dilengkapi
sekali ini saja:
1. Angka/datanya yang mana yang mau disampaikan? (boleh kirim file atau ketik
   angkanya langsung, mis. omzet, biaya, atau data lain)
2. Laporan ini untuk siapa — atasan langsung, investor, bank, atau klien?
3. Tujuannya apa — lapor rutin, minta keputusan/persetujuan, atau minta dana/pinjaman?

Kalau mau cepat, saya bisa pakai asumsi: penerima = atasan langsung, tujuan = lapor
kondisi terkini — tinggal kasih angkanya saja.
```

## Penilaian penguji
- Sesuai instruksi: hanya **satu kali** bertanya, dalam **satu pesan** berisi daftar
  pertanyaan singkat (bukan bertanya berulang satu-satu).
- Menawarkan jalan pintas dengan asumsi wajar bagi pengguna yang terburu-buru, sesuai
  baris "Bila pengguna terburu-buru dan hanya memberi angka mentah, buat asumsi wajar...
  dan sebutkan di akhir hasil" — namun tetap tidak bisa membuat laporan **tanpa angka
  sama sekali**, karena itu satu-satunya input yang benar-benar wajib tanpa default.
- Tidak mengarang angka contoh/placeholder yang bisa disalahartikan sebagai data asli.
  Ini konsisten dengan Batasan & Penanganan Error di SKILL.md.
