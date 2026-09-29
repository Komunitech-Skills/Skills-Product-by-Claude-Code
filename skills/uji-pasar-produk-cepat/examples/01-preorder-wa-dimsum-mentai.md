# Contoh 1: Pre-order WA varian dimsum mentai

> Contoh ilustrasi fiktif ("Dapur Bu Rina", dimsum beku). Bukan hasil uji independen; angka keluaran script asli.

**Pengguna:** "Aku jualan dimsum ayam beku, mau tambah varian mentai. Punya sekitar 200 kontak WA pelanggan. Harga rencana Rp45.000 isi 10. HPP sekitar Rp27.000."

**Asumsi & prioritas (ringkas):** minat (20), harga (20), kirim beku 2 hari (15), ulang beli (16), untung (12). Putaran 1: uji minat+harga lewat pre-order WA (asumsi 1-2).

**Kriteria dikunci sebelum uji:** ditawari 80 kontak pelanggan lama yang pernah beli; aksi = transfer DP Rp15.000 dalam 5 hari; lanjut jika >= 15%, stop jika < 7,5%; margin kotor kasar (45.000-27.000)/45.000 = 40%.

**Hasil:** 14 DP dari 80.
```
$ python3 scripts/hasil_eksperimen.py hasil --ditawari 80 --aksi 14 --target 15
Konversi: 14 dari 80 orang = 17,5%
Rentang wajar 95% (Wilson): 10,7% sampai 27,3%
Artinya: kalau uji diulang, hasil sebenarnya kemungkinan besar ada di antara 11% dan 27%.
Kriteria (ditetapkan SEBELUM uji): lanjut jika >= 15,0%, stop jika < 7,5%.
KEPUTUSAN: LANJUT DENGAN CATATAN: angka mencapai target, tapi batas bawah rentang (10,7%) masih di bawah target. Lanjut bertahap kecil (mis. produksi batch kecil) atau tambah sampel dulu.
```

**Keputusan:** LANJUT DENGAN CATATAN. Produksi batch 40 pack (bukan 200), kirim ke 14 pembeli, lalu uji asumsi berikutnya (kualitas setelah kirim beku, beli ulang). Catatan: 80 orang adalah pelanggan lama, jadi hasil dari pembeli baru bisa lebih rendah.

**Baris log:** `#1 | 2026-09-01 | minat+harga | PO WA | 80 | 14 | 17,5% | LANJUT bertahap`
